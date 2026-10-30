#!/usr/bin/env python3
"""Summarize the six retained Galaxy harness runs into compact derived evidence.

The raw runs (``run.json`` plus the isolated PinMAME state) stay under the working root; this tool reads them and writes
``evidence/runtime/stern/galaxy-diagnostics-and-gameplay.json``. ``--check`` recomputes the summary from the raw runs and refuses drift
from the committed file. Digits are decoded from the seven-segment displays with the comma bit (0x80) masked, and every figure in an
observation label or note is recomputed from the runs here rather than typed by hand.

Usage:
    python tools/summarize_galaxy_runtime.py --runs <harness-root> --write
    python tools/summarize_galaxy_runtime.py --runs <harness-root> --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "evidence/runtime/stern/galaxy-diagnostics-and-gameplay.json"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "b7857639b384d7b25d398ac925833a607185fce5e231c56ee31be486c5d9937a"
CLONE_ROM_ARCHIVE_SHA256 = "cfba29a71b9fe8e0d108527773f0a5b988078591c88493f4e1a1be720fc4ed52"
RUN_NAMES = ("self-test", "solenoid-test", "switch-test", "gameplay", "game-over-and-slam", "galaxyb-solenoid-test")
RUN_GAMES = {name: "galaxyb" if name.startswith("galaxyb-") else "galaxy" for name in RUN_NAMES}
# Seven-segment code (low seven bits) to digit.
DIGITS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
LAMP_ADDRESSES = [*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)]
UNLISTED_LAMPS = (14, 15, 29, 30, 31, 46, 47, 62)


def read_digits(segments: list[int]) -> str:
	return "".join(DIGITS.get(value & 0x7F, "?") for value in segments)


def file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def directory_manifest_sha256(directory: Path) -> tuple[str, int, int]:
	paths = sorted((path for path in directory.rglob("*") if path.is_file()), key=lambda path: path.relative_to(directory).as_posix())
	files = [{"path": path.relative_to(directory).as_posix(), "sha256": file_sha256(path), "size": path.stat().st_size} for path in paths]
	payload = json.dumps(files, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
	return hashlib.sha256(payload).hexdigest(), len(files), sum(item["size"] for item in files)


def self_test_presses(run: dict[str, Any]) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == -7 and event["state"] == 1]


def display_timeline(run: dict[str, Any], index: int) -> list[tuple[float, str]]:
	return [(event["time_s"], read_digits(event["segments"])) for event in run["events"]
		if event["event"] == "display" and event.get("index") == index and "segments" in event]


def display_at(timeline: list[tuple[float, str]], time_s: float) -> str:
	value = ""
	for event_time, text in timeline:
		if event_time > time_s:
			break
		value = text
	return value


def on_intervals(run: dict[str, Any], address: int) -> list[tuple[float, float | None]]:
	intervals: list[tuple[float, float | None]] = []
	start = None
	for event in run["events"]:
		if event["event"] != "solenoid" or event["number"] != address:
			continue
		if event["state"] and start is None:
			start = event["time_s"]
		elif not event["state"] and start is not None:
			intervals.append((start, event["time_s"]))
			start = None
	if start is not None:
		intervals.append((start, None))
	return intervals


def solenoid_test_pairs(run: dict[str, Any]) -> list[tuple[int, int]]:
	"""(displayed driver number, public address) for every pulse after the fourth Self Test press, display read 0.25 s after the pulse."""
	fourth = self_test_presses(run)[3]
	timeline = display_timeline(run, 0)
	pairs = []
	for event in run["events"]:
		if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > fourth:
			pairs.append((int(display_at(timeline, event["time_s"] + 0.25).strip()), event["number"]))
	return pairs


def switch_test_readings(run: dict[str, Any]) -> dict[int, str]:
	readings: dict[int, str] = {}
	for snapshot in run["snapshots"]:
		label = snapshot["label"]
		if label.startswith("close "):
			readings[int(label.split()[1])] = read_digits(snapshot["displays"][0]["segments"]).strip().lstrip("0") or "0"
	return readings


# Cabinet and service inputs, the out-hole (whose closure adds the bonus) and the start button: their score changes are not a switch's own
# award, so no delta is reported for them.
NO_DELTA_SWITCHES = {1, 2, 3, 6, 7, 8, 33}


def settled_score(segments: list[int]) -> int | None:
	"""Player 1's score when the display shows one unbroken, right-aligned run of digits (a score always ends in the units position);
	None for a blank, flashing or partly drawn frame such as `  67   `."""
	text = read_digits(segments)
	digits = text.strip()
	return int(digits) if digits and digits.isdigit() and not text.endswith(" ") else None


# The ROM counts a large award up on the display in steps, so a frame can catch a score part-way through. A snapshot's score counts only when
# Player 1's display has not changed for this long before the snapshot (each snapshot is taken just before the next step's press, so what
# follows it belongs to the next step).
SCORE_QUIET_S = 0.5


def stable_score(timeline: list[tuple[float, str]], snapshot: dict[str, Any]) -> int | None:
	"""The snapshot's settled score, or None while the display was still changing just before it."""
	score = settled_score(snapshot["displays"][0]["segments"])
	time_s = snapshot["time_s"]
	if score is None or any(0 <= time_s - event_time < SCORE_QUIET_S for event_time, _ in timeline):
		return None
	return score


def action_observations(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One observation per switch step. Score deltas are reported only in a game (after the credit button starts one), only for playfield
	switches, and only between two consecutive switch steps whose scores are both stable: a frame caught while the display counts is not a
	score, a delta across a step whose score was not stable would merge two awards, and the attract mode's animations are not scores either."""
	timeline = display_timeline(run, 0)
	snapshots = {snapshot["label"]: snapshot for snapshot in run["snapshots"]}
	observations: list[dict[str, Any]] = []
	previous_score: int | None = None
	in_game = False
	previous_credits = "00"
	for step in run["steps"]:
		label = step["label"]
		snapshot = snapshots.get(label)
		switch = step.get("switch")
		if snapshot is None or switch is None:
			continue
		score = stable_score(timeline, snapshot)
		delta = None
		if switch == 6 and "starts" in label:
			in_game, previous_score = True, 0
		elif in_game and switch not in NO_DELTA_SWITCHES and score is not None and previous_score is not None:
			delta = score - previous_score
		if switch == 8:
			in_game = False
		previous_score = score
		transitioned = sorted(item["number"] for item in step["transitions"]["solenoids"])
		lit = sorted(item["number"] for item in step["transitions"]["lamps"] if item["states"] and item["states"][-1] == 1)
		credits = read_digits(snapshot["displays"][4]["segments"])
		credits_changed = credits != previous_credits
		previous_credits = credits
		parts = [f"{label}: score {score if score is not None else 'not settled'}" + (f" ({delta:+d})" if delta else "")]
		if credits_changed:
			parts.append(f"credits {credits}")
		parts.append(f"solenoids {transitioned}" if transitioned else "no solenoid change")
		if lit:
			parts.append(f"lamps lit {lit}")
		observations.append({
			"label": ", ".join(parts),
			"input_kind": "switch",
			"input_address": switch,
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [switch],
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"transitioned_solenoid_addresses": transitioned,
			"result": "observed" if transitioned or credits_changed or delta or lit else "no_matching_transition",
		})
	return observations


def describe_intervals(run: dict[str, Any], address: int) -> str:
	timeline = display_timeline(run, 0)
	parts = []
	for start, end in on_intervals(run, address):
		length = "until the end of the run" if end is None else f"{end - start:.2f} s"
		parts.append(f"{start:.2f} s for {length} (Player 1 display `{display_at(timeline, start + 0.06).strip() or 'blank'}`)")
	return "; ".join(parts) or "never"


def build(runs_root: Path) -> dict[str, Any]:
	runs = {name: load_json(runs_root / name / "run.json") for name in RUN_NAMES}
	for name, run in runs.items():
		if run.get("failure") is not None:
			raise RuntimeError(f"run {name} failed: {run['failure']}")
		if run["library_sha256"] != LIBRARY_SHA256:
			raise RuntimeError(f"run {name} used an unpinned library")
		if run["game"] != RUN_GAMES[name]:
			raise RuntimeError(f"run {name} booted {run['game']}")
	self_run = runs["self-test"]
	press = self_test_presses(self_run)[0]
	self_sequence = [event["number"] for event in self_run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > press - 0.5]
	self_lamps = sorted({event["number"] for event in self_run["events"] if event["event"] == "lamp"})

	pairs = solenoid_test_pairs(runs["solenoid-test"])
	first_cycle = pairs[:19]
	if [number for number, _ in first_cycle] != list(range(1, 20)):
		raise RuntimeError(f"solenoid test did not show drivers 1-19 in order: {first_cycle}")
	cycles = [pairs[index:index + 19] for index in range(0, len(pairs) - 18, 19)]
	if any(cycle != first_cycle for cycle in cycles):
		raise RuntimeError("solenoid test cycles disagree")
	physical_to_public = {str(number): address for number, address in first_cycle}
	clone_pairs = solenoid_test_pairs(runs["galaxyb-solenoid-test"])
	clone_cycles = [clone_pairs[index:index + 19] for index in range(0, len(clone_pairs) - 18, 19)]
	if not clone_cycles or any(cycle != first_cycle for cycle in clone_cycles):
		raise RuntimeError("the galaxyb solenoid test disagrees with the production ROM's")

	readings = switch_test_readings(runs["switch-test"])
	if any(readings.get(address) != str(address) for address in range(1, 41)):
		raise RuntimeError(f"switch test readings disagree with the addresses: {readings}")

	play_runs = ("gameplay", "game-over-and-slam")
	outside = sorted({event["number"] for name in play_runs for event in runs[name]["events"] if event["event"] == "lamp"})
	unlisted_outside = [address for address in UNLISTED_LAMPS if address in outside]
	if unlisted_outside:
		raise RuntimeError(f"unlisted lamps driven outside the self test: {unlisted_outside}")

	manifest_sha, file_count, total_bytes = directory_manifest_sha256(runs_root)
	raw_runs = []
	for name in RUN_NAMES:
		run = runs[name]
		scenario_name = name if name.startswith("galaxyb-") else f"galaxy-{name}"
		scenario_path = ROOT / f"tools/harness-scenarios/stern/{scenario_name}.json"
		scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
		if file_sha256(scenario_path) != run["scenario"]["sha256"]:
			raise RuntimeError(f"scenario for {name} no longer matches the run")
		raw_runs.append({
			"name": name,
			"sha256": file_sha256(runs_root / name / "run.json"),
			"scenario_path": f"tools/harness-scenarios/stern/{scenario_name}.json",
			"scenario_sha256": run["scenario"]["sha256"],
			"action_count": len(scenario["actions"]),
			"self_test_pulses": sum(1 for action in scenario["actions"] if action.get("type") == "pulse" and action.get("switch") == -7),
			"nvram_initialization": "empty; the isolated PinMAME state directory was created from scratch for this run",
			"initial_switches": [{"switch": item["switch"], "state": item["state"]} for item in scenario.get("initial_switches", [])],
			"snapshot_count": len(run["snapshots"]),
		})
	all_solenoids = sorted({event["number"] for name in RUN_NAMES if RUN_GAMES[name] == "galaxy" for event in runs[name]["events"] if event["event"] == "solenoid"})
	play_solenoids = sorted({event["number"] for name in play_runs for event in runs[name]["events"] if event["event"] == "solenoid"})
	continuous_note = (
		f"Continuous public 17 is on in the gameplay run {describe_intervals(runs['gameplay'], 17)}, and in the game-over and slam run "
		f"{describe_intervals(runs['game-over-and-slam'], 17)}. "
		f"Public 20 is on in the gameplay run {describe_intervals(runs['gameplay'], 20)}, and in the game-over and slam run {describe_intervals(runs['game-over-and-slam'], 20)}."
	)
	return {
		"driver_ids": ["galaxy", "galaxyb"],
		"extractor": {"id": "tools/summarize_galaxy_runtime.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": ["stern.galaxy.1980"],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game galaxy --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/stern/galaxy-<run>.json --output <external-run.json>, "
				"for run in self-test, solenoid-test, switch-test, gameplay and game-over-and-slam, and the same with --game galaxyb and tools/harness-scenarios/stern/galaxyb-solenoid-test.json. Each scenario starts with a 25 s wait for the ROM's power-up test.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": LIBRARY_SHA256},
			"game": "galaxy",
			"observations": {
				"lamp_addresses_driven_outside_self_test": outside,
				"lamp_addresses_seen": self_lamps,
				"lamp_decoder_holes_not_seen": [address for address in (16, 32, 48, 64) if address not in self_lamps],
				"physical_service_solenoid_to_public": physical_to_public,
				"public_solenoid_decoder_holes_not_seen": [16] if 16 not in all_solenoids else [],
				"runs": {
					"self-test": {
						"ordered_solenoid_on_sequence": self_sequence,
						"solenoid_addresses_seen": sorted(set(self_sequence)),
						"note": f"One Self Test press starts the burn-in test. All sixty lamp addresses ({len(self_lamps)} seen) are driven and the four decoder holes 16, 32, 48 and 64 never are; "
							"the solenoids fire in a repeating 19-step cycle.",
						"limitation": "The burn-in drives the displays with digit-cycling frames, so the driver numbers are read from the solenoid-test run instead.",
					},
					"solenoid-test": {
						"ordered_solenoid_on_sequence": [address for _, address in pairs],
						"solenoid_addresses_seen": sorted({address for _, address in pairs}),
						"note": f"Four Self Test presses start the solenoid test, which pulses one driver at a time and shows its number on the Player displays (read 0.25 s after each pulse). "
							f"Over {len(cycles)} complete cycles, driver numbers 1-19 pair with public addresses "
							+ ", ".join(f"{number}->{address}" for number, address in first_cycle) + ".",
					},
					"switch-test": {
						"note": "Five Self Test presses reach the switch test; with each matrix address 1-40 closed alone, the Player 1 display read that address's own number: "
							+ ", ".join(f"{address}->{reading}" for address, reading in sorted(readings.items())) + ".",
					},
					"gameplay": {
						"named_action_observations": action_observations(runs["gameplay"]),
						"solenoid_addresses_seen": sorted({event["number"] for event in runs["gameplay"]["events"] if event["event"] == "solenoid"}),
						"note": continuous_note,
					},
					"galaxyb-solenoid-test": {
						"ordered_solenoid_on_sequence": [address for _, address in clone_pairs],
						"solenoid_addresses_seen": sorted({address for _, address in clone_pairs}),
						"note": f"Driver galaxyb (the seven-digit conversion clone, ROM archive SHA-256 {CLONE_ROM_ARCHIVE_SHA256}), the same four Self Test presses and the same reading: over {len(clone_cycles)} complete cycles "
							"its solenoid test pairs driver numbers 1-19 with the same public addresses as the production ROM's. Every other run boots galaxy.",
					},
					"game-over-and-slam": {
						"named_action_observations": action_observations(runs["game-over-and-slam"]),
						"solenoid_addresses_seen": sorted({event["number"] for event in runs["game-over-and-slam"]["events"] if event["event"] == "solenoid"}),
						"note": "Three balls are served, scored and drained until game over, the ROM is left in attract mode for 90 s, a second game is started and the slam switch (public 8) is closed. "
							f"Lamps {list(UNLISTED_LAMPS)} never change outside the self test in this run or the gameplay run; solenoid addresses seen in the two play runs: {play_solenoids}.",
					},
				},
				"solenoid_addresses_seen": all_solenoids,
			},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and raw NVRAM remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": "source.sha256 is a directory manifest digest, not a file hash: list every file below source.path as {path, size, sha256} with path relative and POSIX-separated, sort by path, serialise as compact canonical JSON (indent=None, separators=(',',':'), sort_keys=True, ensure_ascii=False), encode UTF-8 and take the SHA-256. "
				f"At capture time the tree held {file_count} files totalling {total_bytes} bytes. Individual run hashes are in runtime.raw_runs[].sha256.",
			"path": "external:pinmame-review-artifacts/galaxy-1980/harness",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"sha256": manifest_sha,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--runs", type=Path, required=True, help="directory holding the six run folders")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	summary = build(args.runs)
	if args.write:
		write_json(OUTPUT_PATH, summary)
		print(f"Wrote {OUTPUT_PATH}")
	else:
		if OUTPUT_PATH.read_bytes() != canonical_bytes(summary):
			raise SystemExit(f"{OUTPUT_PATH} does not match the retained runs")
		print("Galaxy runtime summary matches the retained runs.")


if __name__ == "__main__":
	main()
