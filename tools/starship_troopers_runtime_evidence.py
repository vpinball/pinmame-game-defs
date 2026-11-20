"""Derive the compact Starship Troopers runtime evidence from the retained raw harness runs.

Each raw run is a ``run.json`` the pinned LibPinMAME build wrote under the external review-artifacts root
(``starship-troopers-1997/harness/<run>/``), beside a copy of its scenario and a canonical directory manifest. This tool
checks that every run executed the committed scenario on the pinned binary with built-in mechanisms disabled and
without a failure block, then writes the per-step output transitions a curator cites: one document for the startrp
(2.01) run and one for the startrp2 (2.00) run, because a runtime record carries one game. ``--check`` refuses drift
between the raw runs and the committed documents.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "sega.starship-troopers.1997"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
HARNESS_DIRECTORY = "starship-troopers-1997/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/whitestar"
# Document -> (game, ROM archive SHA-256, {retained run directory: SHA-256 of its manifest.json}).
DOCUMENTS = {
	"evidence/runtime/whitestar/starship-troopers-startrp-gameplay.json": (
		"startrp", "128e61465d43dc6188ac8c0e358f1a97de9513e3170cc82e75cba46ffa98b648", {
			"startrp-gameplay": "ca4dff02c54bbf4f10661d1832a2077174faa52530a7484d4e3f051041311fd6",
		},
	),
	"evidence/runtime/whitestar/starship-troopers-startrp2-gameplay.json": (
		"startrp2", "13cf7c70ba7eeaa9211b860b031ea2ae3c0074e927fd7b63b61499189dab9a26", {
			"startrp2-gameplay": "f11b88f3bb849debe95b0a38279ff457e8f08ced02a9a9764dcfc2eab7cbc810",
		},
	),
}
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch "
	"writes are host stimuli, never ROM observations. Each run directory's manifest (tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)


def _sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def review_artifacts_root(required: bool) -> Path | None:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_REVIEW_ARTIFACTS_ROOT is required to read the retained Starship Troopers harness runs")
		return None
	return Path(value).expanduser().resolve()


def _load_run(root: Path, name: str, game: str, manifest_sha256: str) -> tuple[dict[str, Any], str]:
	directory = root / HARNESS_DIRECTORY / name
	manifest = directory / "manifest.json"
	if _sha256(manifest) != manifest_sha256:
		raise RuntimeError(f"{name}: retained manifest does not match its pinned SHA-256")
	listed = {entry["path"]: entry["sha256"] for entry in load_json(manifest)["files"]}
	for relative, digest in listed.items():
		if _sha256(directory / relative) != digest:
			raise RuntimeError(f"{name}: retained file {relative} changed")
	run = load_json(directory / "run.json")
	scenario = ROOT / SCENARIO_DIRECTORY / f"{name}.json"
	if load_json(directory / "scenario.json") != load_json(scenario):
		raise RuntimeError(f"{name}: the retained scenario differs from the committed one")
	if run.get("failure") is not None or run.get("game") != game or run.get("library_sha256") != LIBRARY_SHA256 or run.get("handle_mechanics") != 0:
		raise RuntimeError(f"{name}: not a successful pinned run of {game} with built-in mechanisms disabled")
	return run, listed["run.json"]


def _actions(name: str, run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One named-action observation per scenario step, in order, with every solenoid that changed during it.

	A step is observed when a solenoid or G.I. string 0 changed during it. The label carries each changed solenoid's states in the order the run recorded them, so the direction of a
	transition survives in the compact document. A step that writes no switch, the boot wait, is recorded as a
	key input with no host address rather than attributed to a switch. The host stimulus of a step is the one switch
	that step writes; the scenario's initial switch states stay in the raw run's ``initial_switches``.
	"""
	scenario = load_json(ROOT / SCENARIO_DIRECTORY / f"{name}.json")
	if len(scenario["actions"]) != len(run["steps"]):
		raise RuntimeError(f"{name}: the run's steps do not match the scenario's actions")
	observations = []
	for action, step in zip(scenario["actions"], run["steps"]):
		transitions = step.get("transitions", {})
		solenoid_states = sorted((item["number"], item["states"]) for item in transitions.get("solenoids", []))
		changed = [number for number, _ in solenoid_states]
		active = [number for number, states in solenoid_states if any(states)]
		label = f"{name} step {step['step']}: {step['label']}"
		if solenoid_states:
			label += "; solenoid states during the step: " + "; ".join(
				f"{number} = {', '.join(str(state) for state in states)}" for number, states in solenoid_states
			)
		gi = [item for item in transitions.get("gis", []) if item["number"] == 0]
		if gi:
			label += f"; GI 0 states during the step: {', '.join(str(state) for state in gi[0]['states'])}"
		observation: dict[str, Any] = {"label": label}
		if "switch" in action:
			observation.update({"input_kind": "switch", "input_address": action["switch"]})
		else:
			observation.update({"input_kind": "key", "input_name": f"{action['type']} with no host input"})
		observation.update({
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [action["switch"]] if "switch" in action else [],
			"active_solenoid_addresses": active,
			"transitioned_solenoid_addresses": changed,
			"result": "observed" if changed or gi else "no_matching_transition",
		})
		observations.append(observation)
	return observations


def _addresses(run: dict[str, Any], kind: str) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == kind})


def build(root: Path, game: str, rom_archive_sha256: str, runs: dict[str, str]) -> dict[str, Any]:
	raw_runs = []
	observations: list[dict[str, Any]] = []
	lamps: set[int] = set()
	solenoids: set[int] = set()
	gis: set[int] = set()
	displays: set[int] = set()
	for name, manifest_sha256 in runs.items():
		run, run_sha256 = _load_run(root, name, game, manifest_sha256)
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
	last = list(runs)[-1]
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"machine_ids": [MACHINE_ID],
		"driver_ids": [game],
		"extractor": {"id": "tools/starship_troopers_runtime_evidence.py", "version": 5},
		"switches": [],
		"outputs": [],
		"mechanisms": [],
		"states": [],
		"recreation_notes": [],
		"runtime": {
			"game": game,
			"command_template": (
				f"python tools/run_pinmame_harness.py --library <libpinmame> --game {game} --rom-path <vpinmame-roms> --work-dir "
				"<new-isolated-state> --scenario tools/harness-scenarios/whitestar/<run>.json --dmd-dir <external-dmd-dir> --output "
				"<external-run.json>; built-in mechanisms stay disabled (--handle-mechanics 0) and keyboard handling stays off"
			),
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"rom_archive_sha256": rom_archive_sha256,
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
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{last}/manifest.json",
			"sha256": runs[last],
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
	for relative, (game, rom_archive_sha256, runs) in DOCUMENTS.items():
		path = ROOT / relative
		document = build(root, game, rom_archive_sha256, runs)
		if args.check:
			if not path.is_file() or path.read_bytes() != canonical_bytes(document):
				raise SystemExit(f"Starship Troopers runtime evidence drift: {path}")
			continue
		write_json(path, document)
		print(f"Wrote {path}")
	if args.check:
		print("Starship Troopers runtime evidence matches the retained raw runs.")


if __name__ == "__main__":
	main()
