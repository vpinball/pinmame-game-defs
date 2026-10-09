"""Derive the compact The Sopranos runtime evidence from the retained raw harness runs.

Each raw run is a ``run.json`` the pinned LibPinMAME build wrote under the external review-artifacts root
(``the-sopranos-2005/harness/<run>/``), beside a copy of its scenario and a canonical directory manifest. This tool
checks that every run executed the committed scenario on the pinned binary with built-in mechanisms disabled and
without a failure block, then writes the per-step output transitions a curator cites. ``--check`` refuses drift
between the raw runs and the committed document.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.the-sopranos.2005"
GAME = "sopranos"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "4d32c78ad266b18aa9abb508c63f924b92bdd8e88f933ff4e93a0a70d686a401"
HARNESS_DIRECTORY = "the-sopranos-2005/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/whitestar"
EVIDENCE_PATH = ROOT / "evidence/runtime/whitestar/the-sopranos-stacking-opto-and-gameplay.json"
# Retained run directory -> SHA-256 of its manifest.json.
RUNS = {
	"sopranos-stacking-opto": "de91a43d8bc616768c3652f5204c4e461d467198be86c98bc60d5e2dd0475b3f",
	"sopranos-stacking-opto-boot-active": "7e9ea152c884fed50d69b9bf663ce86222e65cd990cd753da1715dc8df8edd64",
	"sopranos-gameplay": "042fdd91dd534fd2f6c0e22119f2a859660a594def07993730daf483f27b9ec2",
}
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch "
	"writes are host stimuli, never ROM observations. Each run directory's manifest (tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes. The run "
	"directories were created under the working root's runtime-evidence folder and moved unchanged to review-artifacts, so "
	"the work_dir and output paths recorded inside each run.json name the original location."
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def review_artifacts_root(required: bool) -> Path | None:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_REVIEW_ARTIFACTS_ROOT is required to read the retained The Sopranos harness runs")
		return None
	return Path(value).expanduser().resolve()


def _load_run(root: Path, name: str) -> tuple[dict[str, Any], str]:
	directory = root / HARNESS_DIRECTORY / name
	manifest = directory / "manifest.json"
	if _sha256(manifest) != RUNS[name]:
		raise RuntimeError(f"{name}: retained manifest does not match its pinned SHA-256")
	listed = {entry["path"]: entry["sha256"] for entry in load_json(manifest)["files"]}
	for relative, digest in listed.items():
		if _sha256(directory / relative) != digest:
			raise RuntimeError(f"{name}: retained file {relative} changed")
	run = load_json(directory / "run.json")
	scenario = ROOT / SCENARIO_DIRECTORY / f"{name}.json"
	if load_json(directory / "scenario.json") != load_json(scenario):
		raise RuntimeError(f"{name}: the retained scenario differs from the committed one")
	if run.get("failure") is not None or run.get("game") != GAME or run.get("library_sha256") != LIBRARY_SHA256 or run.get("handle_mechanics") != 0:
		raise RuntimeError(f"{name}: not a successful pinned run of {GAME} with built-in mechanisms disabled")
	return run, listed["run.json"]


def _actions(name: str, run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One named-action observation per scenario step, in order, with every solenoid that changed during it."""
	scenario = load_json(ROOT / SCENARIO_DIRECTORY / f"{name}.json")
	if len(scenario["actions"]) != len(run["steps"]):
		raise RuntimeError(f"{name}: the run's steps do not match the scenario's actions")
	stimulus = sorted({item["switch"] for item in scenario.get("initial_switches", [])} | {action["switch"] for action in scenario["actions"] if "switch" in action})
	observations = []
	for action, step in zip(scenario["actions"], run["steps"]):
		transitions = step.get("transitions", {})
		changed = sorted(item["number"] for item in transitions.get("solenoids", []))
		active = sorted(item["number"] for item in transitions.get("solenoids", []) if any(item["states"]))
		label = f"{name} step {step['step']}: {step['label']}"
		gi = [item for item in transitions.get("gis", []) if item["number"] == 0]
		if gi:
			label += f"; GI 0 states during the step: {', '.join(str(state) for state in gi[0]['states'])}"
		observations.append({
			"label": label,
			"input_kind": "switch",
			"input_address": action.get("switch", 15),
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": stimulus,
			"active_solenoid_addresses": active,
			"transitioned_solenoid_addresses": changed,
			"result": "observed" if changed else "no_matching_transition",
		})
	return observations


def _addresses(run: dict[str, Any], kind: str) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == kind})


def build(root: Path) -> dict[str, Any]:
	raw_runs = []
	observations: list[dict[str, Any]] = []
	lamps: set[int] = set()
	solenoids: set[int] = set()
	gis: set[int] = set()
	displays: set[int] = set()
	for name in RUNS:
		run, run_sha256 = _load_run(root, name)
		scenario_path = f"{SCENARIO_DIRECTORY}/{name}.json"
		raw_runs.append({
			"name": name,
			"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{name}/run.json",
			"sha256": run_sha256,
			"scenario_path": scenario_path,
			"scenario_sha256": _sha256(ROOT / scenario_path),
			"initial_switches": run["initial_switches"],
			"nvram_initialization": "empty; each run created its own isolated PinMAME state directory",
			"action_count": len(run["steps"]),
			"self_test_pulses": 0,
		})
		observations.extend(_actions(name, run))
		lamps.update(_addresses(run, "lamp"))
		solenoids.update(_addresses(run, "solenoid"))
		gis.update(_addresses(run, "gi"))
		displays.update(event["index"] for event in run["events"] if event["event"] == "display_available")
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"machine_ids": [MACHINE_ID],
		"driver_ids": [GAME],
		"extractor": {"id": "tools/sopranos_runtime_evidence.py", "version": 1},
		"switches": [],
		"outputs": [],
		"mechanisms": [],
		"states": [],
		"recreation_notes": [],
		"runtime": {
			"game": GAME,
			"command_template": (
				"python tools/run_pinmame_harness.py --library <libpinmame> --game sopranos --rom-path <vpinmame-roms> --work-dir "
				"<new-isolated-state> --ready-timeout 30 --scenario tools/harness-scenarios/whitestar/<run>.json --dmd-dir "
				"<external-dmd-dir> --output <external-run.json>; built-in mechanisms stay disabled (--handle-mechanics 0) and "
				"keyboard handling stays off"
			),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
			"raw_runs": raw_runs,
			"observations": {
				"display_indices_seen": sorted(displays),
				"lamp_addresses_seen": sorted(lamps),
				"solenoid_addresses_seen": sorted(solenoids),
				"gi_addresses_seen": sorted(gis),
				"named_action_observations": observations,
			},
		},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}",
			"sha256": RUNS["sopranos-gameplay"],
			"license": "NOASSERTION",
			"quality": "validated",
			"attribution": ATTRIBUTION,
		},
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="Refuse drift between the raw runs and the committed evidence")
	args = parser.parse_args()
	root = review_artifacts_root(required=True)
	assert root is not None
	document = build(root)
	if args.check:
		if not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != canonical_bytes(document):
			raise SystemExit(f"The Sopranos runtime evidence drift: {EVIDENCE_PATH}")
		print("The Sopranos runtime evidence matches the retained raw runs.")
		return
	write_json(EVIDENCE_PATH, document)
	print(f"Wrote {EVIDENCE_PATH}")


if __name__ == "__main__":
	main()
