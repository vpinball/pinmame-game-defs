from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

from .errors import DefinitionError
from .identifiers import slug
from .jsonio import file_sha256, load_json, write_json
from .pinmame_source import _read_source, _symbol_label
from .scope import is_in_scope_driver

EXTRACTOR_VERSION = 1
GAME_NAME_PATTERN = re.compile(r'^\s*(?:Const\s+)?cGameName\s*=\s*"([a-z0-9_]+)"', re.IGNORECASE | re.MULTILINE)
CONST_SWITCH_PATTERN = re.compile(r"^\s*(?:Const\s+)?(sw[A-Za-z0-9_]+)\s*=\s*(-?\d+)\b", re.IGNORECASE)
CONST_OUTPUT_PATTERN = re.compile(r"^\s*(?:Const\s+)?(s[A-Z][A-Za-z0-9_]*)\s*=\s*(-?\d+)\b")
SUB_PATTERN = re.compile(r"^\s*(?:(?:Public|Private)\s+)?Sub\s+([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE)
END_SUB_PATTERN = re.compile(r"^\s*End\s+Sub\b", re.IGNORECASE)
SWITCH_REF_PATTERN = re.compile(r"Controller\s*\.\s*Switch\s*\(\s*(-?\d+)\s*\)", re.IGNORECASE)
PULSE_SWITCH_PATTERN = re.compile(r"\bPulseSw(?:itch)?\s*(?:\(\s*)?(-?\d+)", re.IGNORECASE)
SOL_CALLBACK_PATTERN = re.compile(r"\bSol(?:Mod)?Callback\s*\(\s*(\d+)\s*\)\s*=\s*\"([^\"]+)\"", re.IGNORECASE)
LAMP_PATTERNS = (
	re.compile(r"\bLampz\s*\.\s*MassAssign\s*\(?\s*(\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE),
	re.compile(r"\b(?:NFadeL|NFadeLm|SetLamp|SetLampMod)\s*\(?\s*(\d+)\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", re.IGNORECASE),
)
GI_PATTERN = re.compile(r"\b(?:UpdateGI|GIUpdate|GICallback\w*)\s*\(?\s*(\d+)\b", re.IGNORECASE)
MECH_PATTERN = re.compile(r"\b(?:New\s+cvpmMech|cvpmMech|mech\w*\.(?:Sol1|Sol2|AddSw|MType|Length|Steps)|cvpmMagnet)\b", re.IGNORECASE)
COMMENT_LINE_PATTERN = re.compile(r"^\s*'\s?(.*)$")


def _revision(source_root: Path) -> str:
	try:
		result = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True)
	except (OSError, subprocess.CalledProcessError) as error:
		raise DefinitionError(f"Unable to resolve VPX-script revision from {source_root}: {error}") from error
	return result.stdout.strip().lower()


def _handler_label(handler: str) -> str:
	value = re.sub(r"_(?:Hit|UnHit|Timer|Spin|Slingshot)$", "", handler, flags=re.IGNORECASE)
	if re.fullmatch(r"sw-?\d+", value, re.IGNORECASE):
		return value
	return _symbol_label(value)


def _header_note(lines: list[str]) -> list[dict[str, Any]]:
	start: int | None = None
	values: list[str] = []
	end = 0
	for line_number, line in enumerate(lines[:250], start=1):
		match = COMMENT_LINE_PATTERN.match(line)
		if match:
			if start is None:
				start = line_number
			values.append(match.group(1).rstrip())
			end = line_number
		elif values and line.strip():
			break
	text = "\n".join(values).strip()
	if start is None or len(text) < 40:
		return []
	return [{"text": text[:20000], "line_start": start, "line_end": end, "status": "candidate"}]


def _candidate(
	*, symbol: str, address: int, label: str, group: str, line: int, state_labels: set[str] | None = None
) -> dict[str, Any]:
	result: dict[str, Any] = {"symbol": symbol, "address": address, "label": label, "group": group, "line": line, "status": "candidate"}
	if state_labels:
		result["state_labels"] = sorted(state_labels)
	return result


def extract_vpx_file(
	path: Path,
	source_root: Path,
	revision: str,
	repository_url: str,
	catalog: dict[str, Any],
	source_content: tuple[str, str] | None = None,
) -> dict[str, Any]:
	text, encoding = source_content or _read_source(path)
	lines = text.splitlines()
	driver_ids = sorted(set(GAME_NAME_PATTERN.findall(text)))
	driver_by_casefold = {driver["id"].casefold(): driver for driver in catalog["drivers"]}
	matched_driver_ids = sorted({driver_by_casefold[driver_id.casefold()]["id"] for driver_id in driver_ids if driver_id.casefold() in driver_by_casefold})
	machine_by_driver = {driver["id"]: driver["machine_id"] for driver in catalog["drivers"]}
	switch_candidates: dict[tuple[str, int], dict[str, Any]] = {}
	output_candidates: dict[tuple[str, int, str], dict[str, Any]] = {}
	current_sub: str | None = None
	mechanisms: list[dict[str, Any]] = []
	mechanism_note_lines: list[dict[str, Any]] = []
	for line_number, line in enumerate(lines, start=1):
		sub_match = SUB_PATTERN.match(line)
		if sub_match:
			current_sub = sub_match.group(1)
		elif END_SUB_PATTERN.match(line):
			current_sub = None
		match = CONST_SWITCH_PATTERN.match(line)
		if match:
			symbol, address = match.group(1), int(match.group(2))
			switch_candidates.setdefault((symbol.casefold(), address), _candidate(symbol=symbol, address=address, label=_symbol_label(symbol), group="pinmame.input.switch", line=line_number))
		match = CONST_OUTPUT_PATTERN.match(line)
		if match:
			symbol, address = match.group(1), int(match.group(2))
			output_candidates.setdefault(("pinmame.output.solenoid", address, symbol.casefold()), _candidate(symbol=symbol, address=address, label=_symbol_label(symbol), group="pinmame.output.solenoid", line=line_number))
		for pattern in (SWITCH_REF_PATTERN, PULSE_SWITCH_PATTERN):
			for ref_match in pattern.finditer(line):
				address = int(ref_match.group(1))
				symbol = current_sub or f"switch_{address}"
				key = (symbol.casefold(), address)
				candidate = switch_candidates.get(key)
				label = _handler_label(symbol)
				if candidate is None:
					candidate = _candidate(symbol=symbol, address=address, label=label, group="pinmame.input.switch", line=line_number)
					switch_candidates[key] = candidate
				elif current_sub:
					candidate.setdefault("state_labels", [])
					if label not in candidate["state_labels"]:
						candidate["state_labels"].append(label)
		for callback_match in SOL_CALLBACK_PATTERN.finditer(line):
			address = int(callback_match.group(1))
			handler = callback_match.group(2)
			key = ("pinmame.output.solenoid", address, handler.casefold())
			output_candidates.setdefault(key, _candidate(symbol=handler, address=address, label=_handler_label(handler), group="pinmame.output.solenoid", line=line_number))
		for lamp_pattern in LAMP_PATTERNS:
			for lamp_match in lamp_pattern.finditer(line):
				address = int(lamp_match.group(1))
				symbol = lamp_match.group(2)
				key = ("pinmame.output.lamp", address, symbol.casefold())
				output_candidates.setdefault(key, _candidate(symbol=symbol, address=address, label=_symbol_label(symbol), group="pinmame.output.lamp", line=line_number))
		for gi_match in GI_PATTERN.finditer(line):
			address = int(gi_match.group(1))
			symbol = current_sub or f"gi_{address}"
			key = ("pinmame.output.gi", address, symbol.casefold())
			output_candidates.setdefault(key, _candidate(symbol=symbol, address=address, label=_handler_label(symbol), group="pinmame.output.gi", line=line_number))
		mech_match = MECH_PATTERN.search(line)
		if mech_match:
			mechanisms.append({"kind": mech_match.group(0), "line": line_number, "raw": line.strip(), "status": "candidate"})
			context_start = max(0, line_number - 3)
			comments = [COMMENT_LINE_PATTERN.match(lines[index]).group(1).strip() for index in range(context_start, line_number) if COMMENT_LINE_PATTERN.match(lines[index])]
			if comments:
				mechanism_note_lines.append({"text": " ".join(comments), "line_start": context_start + 1, "line_end": line_number, "status": "candidate"})
	relative_path = path.relative_to(source_root).as_posix()
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "vpx-vbscript", "version": EXTRACTOR_VERSION},
		"source": {
			"kind": "vpx_script",
			"repository": repository_url,
			"revision": revision,
			"path": relative_path,
			"sha256": file_sha256(path),
			"license": "NOASSERTION",
			"attribution": f"Authors credited in {relative_path} and repository contributors",
			"quality": "candidate",
			"encoding": encoding,
		},
		"driver_ids": matched_driver_ids,
		"machine_ids": sorted({machine_by_driver[driver_id] for driver_id in matched_driver_ids}),
		"switches": sorted(switch_candidates.values(), key=lambda candidate: (candidate["address"], candidate["symbol"].casefold(), candidate["line"])),
		"outputs": sorted(output_candidates.values(), key=lambda candidate: (candidate["group"], candidate["address"], candidate["symbol"].casefold(), candidate["line"])),
		"states": [],
		"mechanisms": mechanisms,
		"recreation_notes": [*_header_note(lines), *mechanism_note_lines],
	}


def extract_vpx_corpora(corpora: list[tuple[str, Path, str]], repository_root: Path) -> dict[str, Any]:
	catalog = load_json(repository_root / "catalog" / "pinmame.json")
	entries: list[dict[str, Any]] = []
	for corpus_id, source_root, repository_url in corpora:
		revision = _revision(source_root)
		for path in sorted(source_root.glob("**/*.vbs")):
			text, encoding = _read_source(path)
			declared_driver_ids = sorted(set(GAME_NAME_PATTERN.findall(text)))
			if declared_driver_ids and all(not is_in_scope_driver(driver_id) for driver_id in declared_driver_ids):
				continue
			evidence = extract_vpx_file(path, source_root, revision, repository_url, catalog, (text, encoding))
			driver_folder = evidence["driver_ids"][0] if evidence["driver_ids"] else "unmatched"
			output_path = repository_root / "evidence" / "vpx" / slug(corpus_id) / driver_folder / f"{evidence['source']['sha256'][:16]}.json"
			write_json(output_path, evidence)
			entries.append(
				{
					"corpus": corpus_id,
					"revision": revision,
					"source": evidence["source"]["path"],
					"evidence": output_path.relative_to(repository_root).as_posix(),
					"declared_driver_ids": [driver_id for driver_id in declared_driver_ids if is_in_scope_driver(driver_id)],
					"driver_ids": evidence["driver_ids"],
					"machine_ids": evidence["machine_ids"],
					"switch_candidate_count": len(evidence["switches"]),
					"output_candidate_count": len(evidence["outputs"]),
					"mechanism_candidate_count": len(evidence["mechanisms"]),
				}
			)
	queue_order = {machine["id"]: machine["processing_order"] for machine in catalog["machines"]}
	entries.sort(key=lambda entry: (min((queue_order.get(machine_id, 10**9) for machine_id in entry["machine_ids"]), default=10**9), entry["corpus"], entry["source"]))
	report = {
		"format": "vpx-script-extraction-report",
		"version": 1,
		"corpora": [{"id": corpus_id, "revision": _revision(source_root), "repository": repository_url} for corpus_id, source_root, repository_url in corpora],
		"script_count": len(entries),
		"declared_game_count": sum(bool(entry["declared_driver_ids"]) for entry in entries),
		"mapped_script_count": sum(bool(entry["driver_ids"]) for entry in entries),
		"unmapped_script_count": sum(bool(entry["declared_driver_ids"]) and not entry["driver_ids"] for entry in entries),
		"switch_candidate_count": sum(entry["switch_candidate_count"] for entry in entries),
		"output_candidate_count": sum(entry["output_candidate_count"] for entry in entries),
		"mechanism_candidate_count": sum(entry["mechanism_candidate_count"] for entry in entries),
		"entries": entries,
	}
	write_json(repository_root / "reports" / "vpx-script-extraction.json", report)
	return report
