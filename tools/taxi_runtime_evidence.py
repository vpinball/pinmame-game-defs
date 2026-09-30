"""Derive compact Taxi evidence from successful, independently pinned raw runs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes
from run_pinmame_harness import SEGMENT_16_CHARACTERS

REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
HARNESS_REVISION = "409403c8afd22fcc3abdbd339f6517f2286a1882"
LIBRARY_SHA256 = "ca33d8fd92ff8f797db2628604db50ae02c8d6b95cd0d6718ce74833980d145d"
ROM_SHA256 = "30f21e3aa2ed62e93d38953e410b0c92679f264b7252d0408aad1d3eb991c03c"
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = Path("evidence/runtime/system-11/taxi-l4-service.json")


def alpha_text(segments: list[int]) -> str:
	"""Keep decimal attributes and unknown transient glyphs visible.

	Taxi uses an alternate seven-segment 1 (0x0006). Its alpha decimal is
	bit15: e.g. HI. SCORE's 0xa209 is I (0x2209) plus the decimal. No
	unrecognized pattern is silently discarded. O/0 share a glyph in this
	ROM; the numeric address is decoded from the separate numeric line.
	"""
	return "".join(
		({0x0006: "1"}.get(value & 0x7FFF, SEGMENT_16_CHARACTERS.get(value & 0x7FFF, "?")))
		+ ("." if value & 0x8000 else "") for value in segments
	).strip()


def _load_run(path: Path, scenario: Path) -> dict:
	run = json.loads(path.read_bytes())
	if run.get("failure") is not None or run.get("game") != "taxi_l4":
		raise ValueError(f"Not a successful Taxi L4 run: {path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"Wrong pinned emulator binary: {path}")
	if run.get("scenario", {}).get("sha256") != hashlib.sha256(scenario.read_bytes()).hexdigest():
		raise ValueError(f"Scenario identity drift: {path}")
	return run


def _checkpoints(run: dict) -> list[dict]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
		for step in run["steps"] if step["type"] == "pulse_until_display"]


def build(review_root: Path) -> dict:
	runtime = review_root / "taxi-1988/runtime"
	names = [("l4-init", "taxi-nvram-init"), ("l4-coil", "taxi-coil-test"),
		("l4-labels-v3", "taxi-service-labels")]
	runs = {name: _load_run(runtime / (name + ".json"), ROOT / "tools/harness-scenarios/system-11" / (scenario + ".json"))
		for name, scenario in names}
	coil, labels = runs["l4-coil"], runs["l4-labels-v3"]
	if _checkpoints(coil) != [{"matched_text": "COIL TEST", "after_service_pulses": 5}]:
		raise ValueError("Taxi coil diagnostic checkpoint drift")
	if [x["matched_text"] for x in _checkpoints(labels)] != ["SINGLE LAMPS", "SWITCH EDGES"]:
		raise ValueError("Taxi service label diagnostic checkpoint drift")
	coil_seen = sorted({x["number"] for x in coil["events"] if x["event"] == "solenoid" and x["state"]})
	lamp_seen = sorted({x["number"] for x in labels["events"] if x["event"] == "lamp" and x["state"]})
	if not (set(range(1, 23)) | set(range(25, 33))) <= set(coil_seen) or lamp_seen != list(range(1, 65)):
		raise ValueError("Taxi complete service output sweep is missing addresses")
	checks = []
	for n in range(27, 33):
		active = next(x for x in labels["snapshots"] if x["label"] == f"switch {n} active stimulus")
		release = next(x for x in labels["snapshots"] if x["label"] == f"switch {n} release stimulus")
		texts = [alpha_text(next(x for x in s["displays"] if x["index"] == 0)["segments"]) for s in [active, release]]
		if not texts[0] or "?" in texts[0] or texts[1]:
			raise ValueError(f"Drop sensor {n} active/release ROM response is not proved")
		checks.append({"label": f"drop sensor {n}: ROM names public1 and clears public0", "input_kind": "switch",
			"input_address": n, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [n], "result": "observed"})
	for host, copied, synthetic, label in [(82, 57, [45, 46], "right"), (84, 58, [47, 48], "left")]:
		held = next(x for x in labels["snapshots"] if x["label"] == f"{label} cabinet flipper column stimulus (held)")
		states = {x["number"]: x["state"] for x in held["watched_switches"]}
		if states.get(copied) != 1 or not set(synthetic) <= set(held["active_solenoids"]):
			raise ValueError("Cabinet flipper copy/synthetic output did not answer host input")
		checks.append({"label": label + " cabinet input copy", "input_kind": "switch", "input_address": host,
			"observed_switch_addresses": [copied], "host_stimulus_switch_addresses": [host],
			"held_synthetic_solenoid_addresses": synthetic, "result": "observed"})
	raw_runs = []
	for name, scenario in names:
		run = runs[name]
		raw_runs.append({"name": name, "sha256": hashlib.sha256((runtime / (name + ".json")).read_bytes()).hexdigest(),
			"scenario_path": f"tools/harness-scenarios/system-11/{scenario}.json", "scenario_sha256": run["scenario"]["sha256"],
			"action_count": run["scenario"]["action_count"], "watch_switches": run["watch_switches"],
			"self_test_pulses": sum(x["after_service_pulses"] for x in _checkpoints(run)), "boot_wait_s": 0,
			"nvram_initialization": "Fresh empty state; one retained initialization scenario." if name == "l4-init" else
			"Fresh state; copied only l4-init-state/nvram/taxi_l4.nv from the separately hashed initialization run.",
			"snapshot_count": len(run["snapshots"]), "retained_from": f"taxi-1988/runtime/{name}.json"})
	return {"format": "pinmame-machine-evidence", "version": 1, "extractor": {"id": "taxi-runtime-evidence", "version": 1},
		"source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame-game-defs",
			"revision": HARNESS_REVISION, "path": "tools/run_pinmame_harness.py", "sha256": hashlib.sha256((ROOT / "tools/run_pinmame_harness.py").read_bytes()).hexdigest(), "license": "MIT", "quality": "full"},
		"driver_ids": ["taxi_l4"], "machine_ids": ["williams.taxi.1988"], "switches": [], "outputs": [], "states": [], "mechanisms": [],
		"recreation_notes": [],
		"runtime": {"game": "taxi_l4", "rom_archive_sha256": ROM_SHA256,
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": REVISION},
			"raw_runs": raw_runs, "command_template": "python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game taxi_l4 --rom-path <legal-ROM-root> --work-dir <fresh-state> --scenario <recorded-scenario> --boot-wait 0 --output <external-run>; each scenario deliberately stabilizes for8s; diagnostic states inherit only the retained initialization NVRAM.",
			"observations": {"service_language": "English", "solenoid_addresses_seen": coil_seen, "lamp_addresses_seen": lamp_seen,
				"display_indices_seen": [0, 1, 2, 3], "ordered_solenoid_on_sequence": [x["number"] for x in coil["events"] if x["event"] == "solenoid" and x["state"]],
				"runs": {"l4-coil": {"diagnostic_checkpoints": _checkpoints(coil), "solenoid_addresses_seen": coil_seen},
					"l4-labels-v3": {"diagnostic_checkpoints": _checkpoints(labels), "named_action_observations": checks,
						"limitation": "Static host stimuli; physical movement, socket population and prototype hardware are not measured."}}}}}


def check(review_root: Path) -> None:
	if (ROOT / EVIDENCE_PATH).read_bytes() != canonical_bytes(build(review_root)):
		raise ValueError("Taxi compact runtime evidence drift")


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("review_root", type=Path)
	args = parser.parse_args()
	check(args.review_root)
	print("Taxi compact runtime evidence matches the successful retained runs.")
