from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from .errors import DefinitionError
from .identifiers import slug
from .jsonio import file_sha256, load_json, write_json

EXTRACTOR_VERSION = 1
DEFINE_PATTERN = re.compile(r"^\s*#\s*define\s+([A-Za-z][A-Za-z0-9_]*)\s+(-?\d+)\s*(?://.*)?$")
GAMEDEF_PATTERN = re.compile(r"\bCORE_(?:GAMEDEF|CLONEDEF)\s*\(\s*([a-z0-9_]+)\s*,\s*([a-z0-9_]+)", re.IGNORECASE)
GAMEDEF_NV_PATTERN = re.compile(r"\bCORE_(?:GAMEDEFNV|CLONEDEFNV)\s*\(\s*([a-z0-9_]+)", re.IGNORECASE)
STATE_PATTERN = re.compile(r'^\s*\{\s*"([^"]+)"\s*,(.*)')
MECH_PATTERN = re.compile(r"\b(mech_add(?:Long)?|mech_tInitData|mech_tMotorData|mech_tSwData)\b")
COMMENT_PATTERN = re.compile(r"/\*(.*?)\*/", re.DOTALL)


def _revision(source_root: Path) -> str:
	try:
		result = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
	except (OSError, subprocess.CalledProcessError) as error:
		raise DefinitionError(f"Unable to resolve PinMAME revision from {source_root}: {error}") from error
	return result.stdout.strip().lower()


def _symbol_label(symbol: str) -> str:
	value = symbol[2:] if symbol.startswith("sw") else symbol[1:] if symbol.startswith("s") else symbol
	value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
	value = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", value)
	value = value.replace("_", " ")
	return " ".join(value.split()) or symbol


def _comment_text(raw: str) -> str:
	lines: list[str] = []
	for line in raw.splitlines():
		line = re.sub(r"^\s*\*?\s?", "", line).rstrip()
		if line and not set(line) <= {"-", "*", "/"}:
			lines.append(line)
	return "\n".join(lines).strip()


def _read_source(path: Path) -> tuple[str, str]:
	data = path.read_bytes()
	try:
		return data.decode("utf-8"), "utf-8"
	except UnicodeDecodeError:
		return data.decode("windows-1252"), "windows-1252"


def _opening_note(text: str) -> list[dict[str, Any]]:
	for match in COMMENT_PATTERN.finditer(text):
		note = _comment_text(match.group(1))
		if len(note) < 80 or "license:" in note.casefold():
			continue
		line_start = text.count("\n", 0, match.start()) + 1
		line_end = line_start + match.group(0).count("\n")
		return [{"text": note, "line_start": line_start, "line_end": line_end, "status": "candidate"}]
	return []


def _parse_states(lines: list[str], addresses: dict[str, int]) -> list[dict[str, Any]]:
	states: list[dict[str, Any]] = []
	inside = False
	for line_number, line in enumerate(lines, start=1):
		if re.search(r"\bsim_tState\s+\w+\s*\[\s*\]\s*=", line):
			inside = True
			continue
		if inside and re.match(r"^\s*};", line):
			break
		if not inside:
			continue
		match = STATE_PATTERN.match(line)
		if match is None:
			continue
		fields = [field.strip() for field in match.group(2).split(",")]
		state: dict[str, Any] = {"label": match.group(1), "line": line_number, "raw": line.strip()}
		if len(fields) >= 2:
			switch_symbol = fields[1]
			if switch_symbol in addresses:
				state["switch_symbol"] = switch_symbol
				state["switch_address"] = addresses[switch_symbol]
		if len(fields) >= 3:
			output_symbol = fields[2]
			if output_symbol in addresses:
				state["exit_output_symbol"] = output_symbol
				state["exit_output_address"] = addresses[output_symbol]
		if len(fields) >= 4 and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", fields[3]):
			state["next_state"] = fields[3]
		states.append(state)
	return states


def _parse_mechanisms(lines: list[str]) -> list[dict[str, Any]]:
	result: list[dict[str, Any]] = []
	for line_number, line in enumerate(lines, start=1):
		match = MECH_PATTERN.search(line)
		if match is None:
			continue
		result.append({"kind": match.group(1), "line": line_number, "raw": line.strip(), "status": "candidate"})
	return result


def extract_sim_file(path: Path, source_root: Path, revision: str, catalog: dict[str, Any]) -> dict[str, Any]:
	text, encoding = _read_source(path)
	lines = text.splitlines()
	addresses: dict[str, int] = {}
	line_by_symbol: dict[str, int] = {}
	for line_number, line in enumerate(lines, start=1):
		match = DEFINE_PATTERN.match(line)
		if match is None:
			continue
		symbol, raw_address = match.groups()
		if symbol.startswith("sw") or (symbol.startswith("s") and len(symbol) > 1 and symbol[1].isupper()):
			addresses[symbol] = int(raw_address)
			line_by_symbol[symbol] = line_number
	states = _parse_states(lines, addresses)
	state_labels: dict[str, set[str]] = defaultdict(set)
	for state in states:
		if state.get("switch_symbol"):
			state_labels[state["switch_symbol"]].add(state["label"])
	driver_ids = sorted({f"{prefix}_{suffix}" for prefix, suffix in GAMEDEF_PATTERN.findall(text)} | set(GAMEDEF_NV_PATTERN.findall(text)))
	catalog_driver_ids = {driver["id"] for driver in catalog["drivers"]}
	driver_ids = [driver_id for driver_id in driver_ids if driver_id in catalog_driver_ids]
	machine_by_driver = {driver["id"]: driver["machine_id"] for driver in catalog["drivers"]}
	relative_path = path.relative_to(source_root).as_posix()
	quality = "preliminary" if "/prelim/" in f"/{relative_path}" else "full"
	switches = []
	outputs = []
	for symbol, address in sorted(addresses.items(), key=lambda item: (item[1], item[0])):
		candidate = {"symbol": symbol, "address": address, "label": _symbol_label(symbol), "group": "pinmame.input.switch" if symbol.startswith("sw") else "pinmame.output.solenoid", "line": line_by_symbol[symbol], "status": "candidate"}
		if symbol in state_labels:
			candidate["state_labels"] = sorted(state_labels[symbol])
		if symbol.startswith("sw"):
			switches.append(candidate)
		else:
			outputs.append(candidate)
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "pinmame-sim-source", "version": EXTRACTOR_VERSION},
		"source": {
			"kind": "pinmame_sim",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": revision,
			"path": relative_path,
			"sha256": file_sha256(path),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
			"quality": quality,
			"encoding": encoding,
		},
		"driver_ids": driver_ids,
		"machine_ids": sorted({machine_by_driver[driver_id] for driver_id in driver_ids}),
		"switches": switches,
		"outputs": outputs,
		"states": states,
		"mechanisms": _parse_mechanisms(lines),
		"recreation_notes": _opening_note(text),
	}


def extract_pinmame_simulations(source_root: Path, repository_root: Path) -> dict[str, Any]:
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	revision = _revision(source_root)
	sims_root = source_root / "src" / "wpc" / "sims"
	paths = sorted(path for path in sims_root.glob("**/*.c") if "template" not in path.relative_to(sims_root).parts)
	entries: list[dict[str, Any]] = []
	for path in paths:
		evidence = extract_sim_file(path, source_root, revision, catalog)
		relative = path.relative_to(sims_root).with_suffix(".json")
		output_path = repository_root / "evidence" / "pinmame-sim" / relative
		write_json(output_path, evidence)
		entries.append(
			{
				"source": evidence["source"]["path"],
				"evidence": output_path.relative_to(repository_root).as_posix(),
				"quality": evidence["source"]["quality"],
				"driver_ids": evidence["driver_ids"],
				"machine_ids": evidence["machine_ids"],
				"switch_count": len(evidence["switches"]),
				"output_count": len(evidence["outputs"]),
				"state_count": len(evidence["states"]),
				"mechanism_candidate_count": len(evidence["mechanisms"]),
			}
		)
	queue_order = {machine["id"]: machine["processing_order"] for machine in catalog["machines"]}
	entries.sort(key=lambda entry: (min((queue_order.get(machine_id, 10**9) for machine_id in entry["machine_ids"]), default=10**9), entry["source"]))
	report = {
		"format": "pinmame-simulation-extraction-report",
		"version": 1,
		"pinmame_revision": revision,
		"file_count": len(entries),
		"full_count": sum(entry["quality"] == "full" for entry in entries),
		"preliminary_count": sum(entry["quality"] == "preliminary" for entry in entries),
		"mapped_file_count": sum(bool(entry["driver_ids"]) for entry in entries),
		"named_switch_candidate_count": sum(entry["switch_count"] for entry in entries),
		"named_output_candidate_count": sum(entry["output_count"] for entry in entries),
		"entries": entries,
	}
	write_json(repository_root / "reports" / "pinmame-sim-extraction.json", report)
	return report
