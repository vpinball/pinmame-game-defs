"""Summarize retained Earthshaker harness runs into committed runtime evidence.

Reads the raw run records written by ``tools/s11_service_display_probe.py`` and
``tools/earthshaker_building_experiment.py`` from one retained directory per driver, writes a
canonical ``manifest.json`` over each directory, and emits one compact ``pinmame-machine-evidence``
document per driver. Only hashes and derived observations are committed; the raw runs stay under
the working root.

    python tools/earthshaker_summarize_runtime_evidence.py --runs <retained-dir> --game esha_la3 \
        --library <dll> --rom <esha_la3.zip> --coil-names <rom-name-tables/esha_la3.json> --output <evidence.json>
    python tools/earthshaker_summarize_runtime_evidence.py --runs <retained-dir> --game esha_la3 \
        --coil-names <rom-name-tables/esha_la3.json> --output <evidence.json> --check

The coil-test pairing uses the ROM's own coil name table (``tools/s11_rom_name_tables.py``) in
table order: the Auto Burn-in coil test fires one public address per step in the same order, so
step ``k`` pairs the table's ``k``-th name with the ``k``-th address the ROM pulsed. Each pairing
is checked against the decoded display text of that step before it is accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact UTF-8 bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF; it lists every <run>.json file in source.path as {path, sha256, size}, "
	"sorted by path."
)
# The WPC-style alphanumeric decoder table renders these glyph pairs identically.
LOOKALIKE = str.maketrans({"0": "O", "5": "S", "1": "?", "/": "?"})


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _loose(text: str) -> str:
	return "".join(character for character in text.translate(LOOKALIKE) if character.isalnum() or character == "?")


def _display_matches(displayed: str, rom_text: str) -> bool:
	shown = _loose(displayed.replace(".", ""))
	stored = _loose(rom_text.replace(".", ""))
	if len(shown) != len(stored):
		return False
	return all(a == b or a == "?" or b == "?" for a, b in zip(shown, stored))


def coil_test_pairs(run: dict[str, Any], coil_names: list[str]) -> list[dict[str, Any]]:
	"""Pair each Auto Burn-in coil-test step with the public address the ROM pulsed."""
	events = run["events"]
	start = next(event["t"] for event in events if event["kind"] == "display" and event["index"] == 0 and "COIL TEST" in event["text"])
	end = next((event["t"] for event in events if event["kind"] == "display" and event["index"] == 0 and event["t"] > start and "MUSIC TEST" in event["text"]), float("inf"))
	window = [event for event in events if start <= event["t"] < end]
	pulses: list[tuple[float, int]] = []
	for index, event in enumerate(window):
		if event["kind"] != "solenoid" or not event["state"]:
			continue
		if event["number"] == 12:
			# Relay 12 selects the C side before a C-side flash; it is a step of its own only when no
			# C-side output (25-32) follows it inside the same step.
			following = [other for other in window[index + 1:] if other["kind"] == "solenoid" and other["state"] and other["t"] - event["t"] < 0.4]
			if any(25 <= other["number"] <= 32 for other in following):
				continue
		pulses.append((event["t"], event["number"]))
	pairs = []
	for step, ((time, address), name) in enumerate(zip(pulses, coil_names), start=1):
		shown = [event["text"] for event in window if event["kind"] == "display" and event["index"] == 0 and event["t"] <= time + 0.1]
		match = next((text for text in reversed(shown) if _display_matches(text, name)), None)
		if match is None:
			raise RuntimeError(f"coil-test step {step} (address {address}) never displayed the ROM name {name!r}")
		pairs.append({"step": step, "address": address, "rom_name": name, "displayed": match.strip()})
	if len(pairs) != len(coil_names):
		raise RuntimeError(f"coil test paired {len(pairs)} steps against {len(coil_names)} ROM names")
	return pairs


def _actions(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [event for event in run["events"] if event["kind"] == "action"]


def _count_on(run: dict[str, Any], address: int, start: float, end: float = float("inf")) -> int:
	return sum(1 for event in run["events"] if event["kind"] == "solenoid" and event["number"] == address and event["state"] and start <= event["t"] < end)


def _game_phase_times(run: dict[str, Any]) -> tuple[float, float]:
	"""Return (game-over entry, start-button press) for the Ad 70 exit scenario."""
	presses = [event for event in _actions(run) if event.get("type") == "press"]
	advance = [event for event in presses if event["switch"] == -7]
	start = [event for event in presses if event["switch"] == 3]
	return advance[-1]["t"], (start[-1]["t"] if start else float("inf"))


def _solenoid_spans(run: dict[str, Any], address: int) -> list[tuple[float, float]]:
	spans, begin = [], None
	for event in run["events"]:
		if event["kind"] == "solenoid" and event["number"] == address:
			if event["state"] and begin is None:
				begin = event["t"]
			elif not event["state"] and begin is not None:
				spans.append((begin, event["t"]))
				begin = None
	return spans


def _open_spans(run: dict[str, Any], address: int) -> str:
	"""Describe every on-span of address, including one still open when the run ends."""
	spans = [f"{begin:.2f}-{end:.2f}s" for begin, end in _solenoid_spans(run, address)]
	changes = [event for event in run["events"] if event["kind"] == "solenoid" and event["number"] == address]
	if changes and changes[-1]["state"]:
		spans.append(f"{changes[-1]['t']:.2f}s-end")
	first_sample = min((event["t"] for event in run["events"] if event["kind"] == "solenoid"), default=None)
	lead = f" (first solenoid sample {first_sample:.2f}s)" if first_sample is not None else ""
	return (", ".join(spans) or "none") + lead


def summarize(name: str, run: dict[str, Any], coil_names: list[str]) -> dict[str, Any]:
	if name.endswith("burnin-coil-test"):
		pairs = coil_test_pairs(run, coil_names)
		return {
			"ordered_solenoid_on_sequence": [pair["address"] for pair in pairs],
			"note": "Auto Burn-in coil test, steps in order as step:address=ROM name: " + "; ".join(f"{pair['step']}:{pair['address']}={pair['rom_name']}" for pair in pairs) + ".",
			"limitation": (
				"Names come from the ROM's own coil table in table order and are accepted only when the decoded display text of that step "
				"agrees; the decoder draws 0 like O and 5 like S and prints 1 and / as '?'. Relay 12 selects each C-side step and is counted "
				"as a step only for the A/C SELECT entry."
			),
		}
	if name.startswith("building-model"):
		spans = _solenoid_spans(run, 9)
		changes = [event for event in run["events"] if event["kind"] == "building"]
		first_on, first_off = spans[0]
		edges = []
		previous = changes[0]
		for change in changes[1:]:
			if first_on <= change["t"] <= first_off:
				edges.append(f"{change['t'] - first_on:.2f}s ({previous['sw25']}{previous['sw26']}->{change['sw25']}{change['sw26']})")
			previous = change
		return {
			"solenoid_addresses_seen": sorted({event["number"] for event in run["events"] if event["kind"] == "solenoid" and event["state"]}),
			"note": (
				f"Modelled building, (25,26) patterns top to bottom {run['pattern_top_to_bottom']}, start position {run['initial_position']}, "
				f"{run['travel_s']} s per full travel while 9 is on. Solenoid 9 energized {first_on:.2f}s and released {first_off - first_on:.2f}s later; "
				f"switch changes presented while it ran (time after 9 on, (25,26) before->after): {', '.join(edges)}."
			),
			"limitation": "Switches 25 and 26 were written by the host from a hypothetical positioner model; the run shows only which presented changes the ROM accepts as a stop.",
		}
	game_over, started = _game_phase_times(run)
	initial = {int(item.split(":")[0]): int(item.split(":")[1]) for item in run["initial_switches"]}
	spans = _solenoid_spans(run, 9)
	observation = {
		"solenoid_addresses_seen": sorted({event["number"] for event in run["events"] if event["kind"] == "solenoid" and event["state"]}),
		"note": (
			f"Initial switches {', '.join(f'{switch}={state}' for switch, state in sorted(initial.items()))}. Game-Over mode entered "
			f"{game_over:.2f}s (Ad 70 exit); two coins and Start pressed by {started:.2f}s. Drop Target Reset (3) fired "
			f"{_count_on(run, 3, game_over, started)} time(s) between Game-Over entry and Start and {_count_on(run, 3, started)} time(s) after Start. "
			f"Solenoid 9 on-spans: {', '.join(f'{begin:.2f}-{end:.2f}s' for begin, end in spans) or 'none'}. "
			f"Game-on enable (23) on-spans: {_open_spans(run, 23)}."
		),
		"limitation": "The harness never moves a ball or a drop target, so repeated resets and ball releases are ROM retries against host-held switch states.",
	}
	return observation

def manifest_bytes_for(runs_dir: Path) -> bytes:
	files = sorted(path for path in runs_dir.glob("*.json") if path.name != "manifest.json")
	manifest = {"files": [{"path": path.name, "sha256": _sha256(path), "size": path.stat().st_size} for path in files]}
	return (json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def build_evidence(runs_dir: Path, game: str, coil_names_path: Path, library_sha256: str, rom_sha256: str) -> tuple[bytes, dict[str, Any]]:
	"""Return (manifest.json bytes, evidence document) derived from the raw runs in ``runs_dir``."""
	runs_dir = runs_dir.resolve()
	files = sorted(path for path in runs_dir.glob("*.json") if path.name != "manifest.json")
	manifest_bytes = manifest_bytes_for(runs_dir)
	coil_names = [entry["text"] for entry in json.loads(coil_names_path.read_text(encoding="utf-8"))["coil_table"]["entries"]]
	raw_runs, observed, solenoids = [], {}, set()
	for path in files:
		run = json.loads(path.read_text(encoding="utf-8"))
		if run["library_sha256"] != library_sha256 or run["rom_archive_sha256"] != rom_sha256 or run["game"] != game:
			raise RuntimeError(f"{path.name} was not produced by the pinned library, ROM, and game")
		name = path.stem.removeprefix(f"{game}-")
		entry: dict[str, Any] = {
			"name": name,
			"sha256": _sha256(path),
			"self_test_pulses": sum(1 for event in run["events"] if event["kind"] == "action" and event.get("type") == "press" and event.get("switch") == -7),
			"nvram_initialization": "new empty isolated state directory; the ROM starts from its factory settings",
			"boot_wait_s": float(run["boot_wait_s"]),
		}
		if "initial_switches" in run:
			entry["initial_switches"] = [{"switch": int(item.split(":")[0]), "state": int(item.split(":")[1])} for item in run["initial_switches"]]
		raw_runs.append(entry)
		observed[name] = summarize(name, run, coil_names)
		solenoids.update(event["number"] for event in run["events"] if event["kind"] == "solenoid" and event["state"])
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "earthshaker-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"path": f"external:pinmame-review-artifacts/earthshaker/{runs_dir.name}",
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [game],
		"machine_ids": ["williams.earthshaker.1989"],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": game,
			"rom_archive_sha256": rom_sha256,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": library_sha256},
			"raw_runs": raw_runs,
			"command_template": (
				"python tools/s11_service_display_probe.py --library <libpinmame> --rom-path <vpinmame-roms> --game <driver> --work-dir "
				"<new-empty-dir> --output <external-json> --boot-wait <s> --initial-switch=<switch>:<state> ... --action press:<switch>:<hold_ms>:<settle_s> "
				"| set:<switch>:<state> | wait:<s> ... for the service and game-start runs, and python tools/earthshaker_building_experiment.py "
				"--library <libpinmame> --rom-path <vpinmame-roms> --work-dir <new-empty-dir> --output <external-json> --pattern <p,p,p,p> "
				"--initial-position <0-1> --start-game for the building-model runs. A fresh ROM boots to FACTORY SETTING and waits; the "
				"scenarios reach Game-Over mode with Manual-Down (-6 = 0), Advance twice (Game ID, then Ad 70), Auto-Up (-6 = 1), Advance, "
				"and reach the Auto Burn-in coil test with Manual-Down, Advance five times to Ad 67, Credit (3) to select YES, Auto-Up, Advance."
			),
			"observations": {
				"solenoid_addresses_seen": sorted(solenoids),
				"service_language": "English",
				"runs": observed,
			},
		},
	}
	return manifest_bytes, evidence


def check(runs_dir: Path, game: str, coil_names_path: Path, output: Path) -> None:
	"""Re-derive ``output`` and the runs' manifest from the raw runs and refuse any drift.

	The library and ROM hashes are taken from the committed evidence; every raw run must carry
	exactly those hashes. tests/test_earthshaker.py pins the committed hashes to the pinned library
	build and the ROM archives the evidence names.
	"""
	committed = json.loads(output.read_text(encoding="utf-8"))
	manifest_bytes, evidence = build_evidence(
		runs_dir, game, coil_names_path, committed["runtime"]["emulator"]["sha256"], committed["runtime"]["rom_archive_sha256"]
	)
	manifest_path = runs_dir / "manifest.json"
	if not manifest_path.is_file() or manifest_path.read_bytes() != manifest_bytes:
		raise RuntimeError(f"{manifest_path} does not match the raw runs beside it")
	if output.read_bytes() != canonical_bytes(evidence):
		raise RuntimeError(f"{output} is not the summary of the raw runs in {runs_dir}")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--runs", type=Path, required=True)
	parser.add_argument("--game", required=True)
	parser.add_argument("--library", type=Path)
	parser.add_argument("--rom", type=Path)
	parser.add_argument("--coil-names", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--check", action="store_true", help="re-derive the committed evidence and manifest and fail on drift; writes nothing")
	args = parser.parse_args()
	if args.check:
		check(args.runs.resolve(), args.game, args.coil_names, args.output)
		print(f"{args.output} matches {args.runs}")
		return
	if args.library is None or args.rom is None:
		parser.error("--library and --rom are required unless --check is given")
	runs_dir = args.runs.resolve()
	manifest_bytes, evidence = build_evidence(runs_dir, args.game, args.coil_names, _sha256(args.library), _sha256(args.rom))
	(runs_dir / "manifest.json").write_bytes(manifest_bytes)
	write_json(args.output, evidence)
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
