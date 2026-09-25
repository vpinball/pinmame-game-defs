"""Summarize retained Bride of Pinbot head/helmet harness runs into committed runtime evidence.

Reads the raw run records written by ``tools/bop_head_mech_experiment.py`` from a retained
directory, writes a canonical ``manifest.json`` over them, and emits the compact
``pinmame-machine-evidence`` document the definition cites. Only hashes and derived observations
are committed; the raw runs stay under the working root.

    python tools/bop_summarize_runtime_evidence.py --runs <retained-run-dir> --library <dll> \
        --rom <bop_l7.zip> --output evidence/runtime/wpc-alpha/bride-of-pinbot-head-helmet-and-service-names.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import write_json

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
RUN_ORDER = (
	"helmet-single-lamp", "head-cycle-vpw", "head-cycle-pinned", "head-cycle-faces-open",
	"head-coils-vpw-start-0", "head-coils-vpw-start-90", "head-coils-vpw-start-180", "head-coils-vpw-start-270",
	"lamp-names", "solenoid-names", "switch-names", "flasher-names",
)
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact UTF-8 bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF; it lists every <run>.json file in source.path as {path, sha256, size}, "
	"sorted by path."
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def _checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [event for event in run["events"] if event["kind"] == "checkpoint"]


def _top_line(screen: str) -> str:
	return screen.split(" / ")[0].strip()


def summarize_run(name: str, run: dict[str, Any]) -> dict[str, Any]:
	checkpoints = _checkpoints(run)
	observation: dict[str, Any] = {}
	if name == "helmet-single-lamp":
		first_up = next(event["t"] for event in run["events"] if event["kind"] == "pulse" and event["t"] >= _checkpoint_time(checkpoints, "helmet_single_lamp"))
		state: dict[int, int] = {}
		for change in run["helmet_lamp_changes"]:
			if change["t"] < first_up:
				state[change["lamp"]] = change["state"]
		lit = sorted(lamp for lamp, value in state.items() if value)
		stepped = [change["lamp"] for change in run["helmet_lamp_changes"] if change["state"] and change["t"] >= first_up]
		observation["note"] = (
			f"After Enter selected SINGLE LAMP only public lamp(s) {', '.join(str(lamp) for lamp in lit)} stayed lit; successive Up "
			f"presses then lit {', '.join(str(lamp) for lamp in stepped)}."
		)
		observation["diagnostic_checkpoints"] = [
			{"matched_text": "HELMET LIGHT TST", "after_service_pulses": _pulses_before(run, _checkpoint_time(checkpoints, "head_test_entered"))},
			{"matched_text": "SINGLE LAMP", "after_service_pulses": _pulses_before(run, _checkpoint_time(checkpoints, "helmet_single_lamp"))},
		]
	elif name.startswith("head-"):
		kicks = [edge for edge in run["kicker_edges"] if edge["state"]]
		sequence: list[int] = []
		for edge in kicks:
			if not sequence or sequence[-1] != edge["solenoid"]:
				sequence.append(edge["solenoid"])
		stops = [edge for edge in run["motor_edges"] if not edge["motor"]]
		observation["ordered_solenoid_on_sequence"] = sequence
		observation["solenoid_addresses_seen"] = sorted({edge["solenoid"] for edge in kicks} | {28} | ({27} if any(edge["relay"] for edge in run["motor_edges"]) else set()))
		observation["note"] = (
			f"Model {run['model']}, head start angle {run['initial_angle']} degrees. Motor stops at modelled angles "
			f"{', '.join(format(edge['angle'], '.2f') for edge in stops)}; head kickers first fired at angles "
			+ ", ".join(f"{edge['solenoid']}@{edge['angle']:.2f}" for edge in _first_kicks(kicks))
			+ "."
		)
		observation["limitation"] = "Switch 67 is written by the host from a synthetic model; the run shows what the ROM accepts, not the physical cam profile."
	else:
		screens = [" ".join(event["screen"].split()) for event in checkpoints if event["name"].startswith(("after_up", "switch_", "head_test_entered"))]
		observation["note"] = (
			"Service-test screens in display order (upper line / lower line; the lower line carries the test number and the "
			"lamp, solenoid, or switch number shown with each name): " + "; ".join(screens)
		)
		observation["limitation"] = (
			"Text is decoded from the sixteen-segment frames with the harness font table plus the period bit: the WPC "
			"alphanumeric font draws 5 like S and 0 like O, and the table has no entry for the 1 glyph, which prints as '?'. "
			"So 'CIRCLE SOK' reads 50K and 'LEFT LOOP SOOK' reads 500K; in the lower line 'O' before a digit is the leading zero of the step number."
		)
	if "diagnostic_checkpoints" not in observation:
		entered = next(event for event in checkpoints if event["name"] == "head_test_entered")
		observation["diagnostic_checkpoints"] = [{"matched_text": _top_line(entered["screen"]), "after_service_pulses": _pulses_before(run, entered["t"])}]
	return observation


def _checkpoint_time(checkpoints: list[dict[str, Any]], name: str) -> float:
	return next(event["t"] for event in checkpoints if event["name"] == name)


def _pulses_before(run: dict[str, Any], time: float) -> int:
	return sum(1 for event in run["events"] if event["kind"] == "pulse" and event["t"] < time)


def _first_kicks(kicks: list[dict[str, Any]]) -> list[dict[str, Any]]:
	result: list[dict[str, Any]] = []
	last = None
	for edge in kicks:
		key = (edge["solenoid"], edge["angle"])
		if key != last:
			result.append(edge)
			last = key
	return result


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True)
	parser.add_argument("--library", type=Path, required=True)
	parser.add_argument("--rom", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	args = parser.parse_args()
	runs_dir = args.runs.resolve()
	files = sorted(runs_dir.glob("*.json"))
	files = [path for path in files if path.name != "manifest.json"]
	manifest = {"files": [{"path": path.name, "sha256": _sha256(path), "size": path.stat().st_size} for path in files]}
	manifest_bytes = (json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
	(runs_dir / "manifest.json").write_bytes(manifest_bytes)
	raw_runs = []
	runs: dict[str, Any] = {}
	solenoids: set[int] = set()
	lamps: set[int] = set()
	display_indices: set[int] = set()
	for name in RUN_ORDER:
		path = runs_dir / f"{name}.json"
		run = json.loads(path.read_text(encoding="utf-8"))
		pulses = sum(1 for event in run["events"] if event["kind"] == "pulse")
		raw_runs.append({
			"name": name,
			"sha256": _sha256(path),
			"self_test_pulses": pulses,
			"nvram_initialization": "new empty isolated state directory; no NVRAM inherited",
			"boot_wait_s": 30.0,
		})
		runs[name] = summarize_run(name, run)
		solenoids.update(edge["solenoid"] for edge in run.get("kicker_edges", []) if edge["state"])
		if run.get("motor_edges"):
			solenoids.add(28)
			if any(edge["relay"] for edge in run["motor_edges"]):
				solenoids.add(27)
		lamps.update(change["lamp"] for change in run.get("helmet_lamp_changes", []) if change["state"])
		display_indices.update(event["index"] for event in run["events"] if event["kind"] == "display")
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "bop-head-mech-experiment", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"path": "external:pinmame-review-artifacts/bride-of-pinbot/harness-runs",
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": ["bop_l7"],
		"machine_ids": ["williams.the-machine-bride-of-pinbot.1991"],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": "bop_l7",
			"rom_archive_sha256": _sha256(args.rom),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": _sha256(args.library)},
			"raw_runs": raw_runs,
			"command_template": (
				"python tools/bop_head_mech_experiment.py --library <libpinmame> --rom-path <vpinmame-roms> --work-dir <new-empty-dir> "
				"--output <external-json> --model <vpw|pinned|faces-open> --initial-angle <deg> --test <helmet|cycle|coils|lamp-names|"
				"solenoid-names|switch-names|flasher-names> --boot-wait 30 --settle <s> --steps <n>. Each run starts from a new empty "
				"state directory; the tool closes the coin door for the boot wait, opens it, and walks the service menu with the "
				"coin-door buttons (switches 5-8)."
			),
			"observations": {
				"solenoid_addresses_seen": sorted(solenoids),
				"lamp_addresses_seen": sorted(lamps),
				"service_language": "English",
				"display_indices_seen": sorted(display_indices),
				"runs": runs,
			},
		},
	}
	write_json(args.output, evidence)
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
