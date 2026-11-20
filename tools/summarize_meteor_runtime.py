#!/usr/bin/env python3
"""Summarize the eleven retained Meteor harness runs into compact derived evidence.

The raw runs (``run.json`` plus the isolated PinMAME state) stay under the working root; this tool reads them and writes
``evidence/runtime/stern/meteor-diagnostics-and-gameplay.json``. ``--check`` recomputes the summary from the raw runs and refuses drift
from the committed file. Digits are decoded from the seven-segment displays with the comma bit (0x80) masked. Every display frame the
evidence cites (the solenoid-test driver numbers, the switch-test readings, the credit display after each coin and the bookkeeping
functions that count the coins) is pinned by the SHA-256 of its segment words in ``tools/seeds/stern/meteor-1979-frame-readings.json``
together with the curator's reading, and a run whose cited frame differs is refused.

Usage:
    python tools/summarize_meteor_runtime.py --runs <harness-root> --write
    python tools/summarize_meteor_runtime.py --runs <harness-root> --check
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
OUTPUT_PATH = ROOT / "evidence/runtime/stern/meteor-diagnostics-and-gameplay.json"
FRAME_READINGS_PATH = ROOT / "tools/seeds/stern/meteor-1979-frame-readings.json"
MACHINE_ID = "stern.meteor.1979"
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVES = {
	"meteor": "ee849e28a5edd2832012c433e6e71713f8c8773c874139ea24bc6d4bb9529438",
	"meteora": "7feebe36b85a3742daf3d2282e3ea4b9c37471e487d076fb96899d145f0f3f15",
	"meteorb": "8df1732f9e9211396b6d3df71dd66b6ac573d1213c4274277f2ce524a5ac9d70",
	"meteorbf": "d743bea66b310693638a51850feeb4c56671191baee0239e4e9f8b6f3580abf9",
	"meteorc": "d8f572bb4e42ba16e2eddb0f846eabf2a94c112ed48c63f183ae038722ba0d27",
	"meteord": "97609378f403a6a8ac7d56eea6d4679a89f906c7f251378ab49cc03c6844798d",
	"meteorfp": "c7b549daa9acdb8d220ee44a815f4384a51a836d9e5f8c6b1495a5133e1ea4fe",
}
# run name -> (driver, scenario file stem)
RUNS: dict[str, tuple[str, str]] = {
	"self-test": ("meteor", "meteor-self-test"),
	"solenoid-test": ("meteor", "meteor-solenoid-test"),
	"switch-test": ("meteor", "meteor-switch-test"),
	"coin-bookkeeping": ("meteor", "meteor-coin-bookkeeping"),
	"gameplay": ("meteor", "meteor-gameplay"),
	**{f"{driver}-variant-io": (driver, f"{driver}-variant-io") for driver in ("meteora", "meteorb", "meteorbf", "meteorc", "meteord", "meteorfp")},
}
RUN_NAMES = tuple(RUNS)
SERVICE_RUNS = ("self-test", "solenoid-test", "switch-test", "coin-bookkeeping")
VARIANT_RUNS = tuple(name for name in RUN_NAMES if name.endswith("-variant-io"))
# Seven-segment code (low seven bits) to digit.
DIGITS = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
DECODER_HOLES = (16, 32, 48, 64)
CONTINUOUS = (17, 18, 19, 20)
# The METEOR bank from left to right: letter -> (target switch, knock-down coil, drop lamp). Which target the ROM picks to spot is its own choice.
METEOR_BANK = {"M": (32, 4, 58), "first E": (31, 5, 42), "T": (30, 8, 26), "second E": (29, 11, 10), "O": (28, 12, 57), "R": (27, 14, 41)}
KNOCK_DOWN_COILS = tuple(coil for _, coil, _ in METEOR_BANK.values())
# The steps of a variant run that drain the ball and serve the next one; the bonus count and the target memory make their timing depend on the game.
DRAIN_STEPS = ("ball 1: ball drains into the outhole", "ball 2: served ball leaves the outhole")
# Coin steps of the coin-bookkeeping run, and the bookkeeping presses that show the three chute counters.
COIN_STEPS = ("coin switch 1, once", "coin switch 2, coin 1", "coin switch 2, coin 2", "coin switch 3, coin 1", "coin switch 3, coin 2", "coin switch 3, coin 3")
BOOKKEEPING_PRESSES = ("self test press 14", "self test press 15", "self test press 16")
# The gameplay steps whose spot lamp the ROM puts out, by switch.
SPOT_STEPS = {4: "stand-up target sw4", 38: "upper roll-over button sw38", 40: "lower roll-over button sw40"}


def read_digits(segments: list[int]) -> str:
	return "".join(DIGITS.get(value & 0x7F, "?") for value in segments)


def segments_sha256(segments: list[int]) -> str:
	return hashlib.sha256(json.dumps(segments, separators=(",", ":")).encode("utf-8")).hexdigest()


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


def _load_run(runs_root: Path, name: str) -> dict[str, Any]:
	"""One retained run; a separate function so a test can substitute a run's content."""
	return load_json(runs_root / name / "run.json")


def frame_readings() -> dict[str, dict[str, dict[str, str]]]:
	seed = load_json(FRAME_READINGS_PATH)
	if seed.get("format") != "pinmame-frame-readings" or seed.get("machine_id") != MACHINE_ID:
		raise RuntimeError("the Meteor frame-readings seed is not the expected document")
	return seed["runs"]


def pinned_reading(run: str, label: str, segments: list[int]) -> str:
	"""The curator's reading of a cited frame, refusing a frame other than the one that was read."""
	pin = frame_readings().get(run, {}).get(label)
	if pin is None:
		raise RuntimeError(f"{run}: no pinned reading for {label!r}")
	if segments_sha256(segments) != pin["segments_sha256"]:
		raise RuntimeError(f"{run}: {label!r} does not carry the frame the curator read as {pin['reading']!r}")
	if read_digits(segments).strip() != pin["reading"]:
		raise RuntimeError(f"{run}: {label!r} decodes differently from its pinned reading")
	return pin["reading"]


def self_test_presses(run: dict[str, Any]) -> list[float]:
	return [event["time_s"] for event in run["events"] if event["event"] == "switch" and event["number"] == -7 and event["state"] == 1]


def display_frames(run: dict[str, Any], index: int) -> list[tuple[float, list[int]]]:
	return [(event["time_s"], event["segments"]) for event in run["events"] if event["event"] == "display" and event.get("index") == index and "segments" in event]


def frame_at(frames: list[tuple[float, list[int]]], time_s: float) -> list[int]:
	value: list[int] = []
	for event_time, segments in frames:
		if event_time > time_s:
			break
		value = segments
	return value


def snapshot(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["snapshots"] if item["label"] == label]
	if len(matches) != 1:
		raise RuntimeError(f"run has {len(matches)} snapshots labelled {label!r}")
	return matches[0]


def snapshot_display(item: dict[str, Any], index: int) -> list[int]:
	return next(display["segments"] for display in item["displays"] if display.get("index") == index)


def solenoid_test_pairs(run: dict[str, Any]) -> list[tuple[int, int]]:
	"""(displayed driver number, public address) for every pulse after the last Self Test press; display 0 is read 0.25 s after each pulse,
	and every frame must be the pinned frame of its position in the 19-step cycle."""
	last = self_test_presses(run)[-1]
	frames = display_frames(run, 0)
	pulses = [event for event in run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > last]
	pairs = []
	for index, event in enumerate(pulses):
		reading = pinned_reading("solenoid-test", f"pulse {index % 19 + 1}", frame_at(frames, event["time_s"] + 0.25))
		pairs.append((int(reading), event["number"]))
	return pairs


def switch_test_readings(run: dict[str, Any]) -> dict[int, str]:
	readings: dict[int, str] = {}
	for item in run["snapshots"]:
		label = item["label"]
		if label.startswith("close "):
			readings[int(label.split()[1])] = pinned_reading("switch-test", label, snapshot_display(item, 0)).lstrip("0") or "0"
	return readings


def coin_readings(run: dict[str, Any]) -> tuple[list[str], dict[str, int]]:
	"""The credit display after each coin, and the coin count the ROM shows for bookkeeping functions 09, 10 and 11."""
	credits = [pinned_reading("coin-bookkeeping", f"credits after {label}", snapshot_display(snapshot(run, label), 4)) for label in COIN_STEPS]
	counts: dict[str, int] = {}
	for label in BOOKKEEPING_PRESSES:
		item = snapshot(run, label)
		function = pinned_reading("coin-bookkeeping", f"{label} function", snapshot_display(item, 5))
		counts[function] = int(pinned_reading("coin-bookkeeping", f"{label} count", snapshot_display(item, 0)))
	return credits, counts


GAME_END_STEP = "ball 3 drains and the game ends"
BEFORE_GAME_END_STEP = "ball 3: left flipper button after the tilt"


def game_end_readings(run: dict[str, Any]) -> dict[str, str]:
	"""Player 1's score, the match number and the credits at the game end, and the credits just before the last drain."""
	before = snapshot(run, BEFORE_GAME_END_STEP)
	after = snapshot(run, GAME_END_STEP)
	return {
		"credits_before": pinned_reading("gameplay", "credits before the last drain", snapshot_display(before, 4)),
		"credits_after": pinned_reading("gameplay", "credits at the game end", snapshot_display(after, 4)),
		"score": pinned_reading("gameplay", "player 1 score at the game end", snapshot_display(after, 0)),
		"match": pinned_reading("gameplay", "match number at the game end", snapshot_display(after, 5)),
	}


def step_windows(run: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any], float, float]]:
	"""(step, end snapshot, start time, end time); snapshot 0 is taken at boot and snapshot i + 1 at the end of step i."""
	snapshots = run["snapshots"]
	if len(snapshots) != len(run["steps"]) + 1:
		raise RuntimeError("run snapshots do not follow its steps")
	windows = []
	for index, step in enumerate(run["steps"]):
		if snapshots[index + 1]["label"] != step["label"]:
			raise RuntimeError(f"snapshot {index + 1} does not close step {step['label']!r}")
		windows.append((step, snapshots[index + 1], snapshots[index]["time_s"], snapshots[index + 1]["time_s"]))
	return windows


def describe_on_order(addresses: list[int]) -> str:
	order: list[int] = []
	counts: dict[int, int] = {}
	for address in addresses:
		if address not in counts:
			order.append(address)
		counts[address] = counts.get(address, 0) + 1
	return ", ".join(f"{address}" + (f" x{counts[address]}" if counts[address] > 1 else "") for address in order)


def lamp_changes(run: dict[str, Any], start: float, end: float) -> tuple[list[int], list[int]]:
	"""Lamps that turned on in the window and were on at its end, and lamps that were on at its start, turned off in it and never came back on in it."""
	before: dict[int, int] = {}
	inside: dict[int, list[int]] = {}
	for event in run["events"]:
		if event["event"] != "lamp":
			continue
		if event["time_s"] <= start:
			before[event["number"]] = event["state"]
		elif event["time_s"] <= end:
			inside.setdefault(event["number"], []).append(event["state"])
	lit = sorted(address for address, states in inside.items() if states[-1])
	out = sorted(address for address, states in inside.items() if before.get(address) and not any(states))
	return lit, out


def windowed_actions(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""One entry per host switch step; its response window runs from the step's start to the end of the wait steps that follow it, so a coil
	the scenario waited for is credited to the stimulus before it."""
	windows = step_windows(run)
	actions: list[dict[str, Any]] = []
	for index, (step, _, start, _) in enumerate(windows):
		switch = step.get("switch")
		if switch is None:
			continue
		last = index
		while last + 1 < len(windows) and windows[last + 1][0].get("switch") is None:
			last += 1
		end_snapshot, end = windows[last][1], windows[last][3]
		steps = [windows[position][0] for position in range(index, last + 1)]
		on_order = [event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"] == 1 and start < event["time_s"] <= end]
		lit, out = lamp_changes(run, start, end)
		actions.append({
			"step": step, "switch": switch, "start": start, "end": end, "end_snapshot": end_snapshot, "on_order": on_order, "lit": lit, "out": out,
			"transitioned": sorted({change["number"] for item in steps for change in item["transitions"]["solenoids"]}),
		})
	return actions


def action_observations(run: dict[str, Any]) -> list[dict[str, Any]]:
	observations: list[dict[str, Any]] = []
	for action in windowed_actions(run):
		step = action["step"]
		closes = step.get("state", step.get("active_state", 1))
		stimulus = f"host {'pulses' if step['type'].startswith('pulse') else ('closes' if closes else 'opens')} switch {action['switch']}"
		label = f"{step['label']} ({stimulus}): " + (f"solenoids on, in first-seen order with pulse counts {describe_on_order(action['on_order'])}" if action["on_order"]
			else ("solenoids off " + str(action["transitioned"]) if action["transitioned"] else "no solenoid change"))
		if action["lit"]:
			label += f"; lamps lit {action['lit']}"
		if action["out"]:
			label += f"; lamps out {action['out']}"
		observations.append({
			"label": label,
			"input_kind": "switch",
			"input_address": action["switch"],
			"observed_switch_addresses": [],
			"host_stimulus_switch_addresses": [action["switch"]],
			"active_solenoid_addresses": sorted(action["end_snapshot"]["active_solenoids"]),
			"transitioned_solenoid_addresses": action["transitioned"],
			"result": "observed" if action["transitioned"] or action["lit"] or action["out"] else "no_matching_transition",
		})
	return observations


def intervals(run: dict[str, Any], address: int) -> list[tuple[float, float | None]]:
	result: list[tuple[float, float | None]] = []
	start = None
	for event in run["events"]:
		if event["event"] != "solenoid" or event["number"] != address:
			continue
		if event["state"] and start is None:
			start = event["time_s"]
		elif not event["state"] and start is not None:
			result.append((start, event["time_s"]))
			start = None
	if start is not None:
		result.append((start, None))
	return result


def initialisation_pulses(name: str, run: dict[str, Any], expected: int) -> list[float]:
	"""The ROM's initialisation of the four continuous lines: every on-interval of the unused drivers 17 and 20 must start together with
	an on-transition of 17, 18, 19 and 20 alike, and the run must hold ``expected`` such starts."""
	starts = {address: [start for start, _ in intervals(run, address)] for address in CONTINUOUS}
	for address in (17, 20):
		if len(starts[address]) != expected:
			raise RuntimeError(f"{name}: public {address} turned on {len(starts[address])} times, not only at the {expected} initialisation(s)")
	pulses = []
	for start in starts[17]:
		if not all(any(abs(other - start) < 0.05 for other in starts[address]) for address in CONTINUOUS):
			raise RuntimeError(f"{name}: public 17 at {start:.2f} s is not part of an initialisation of all four continuous lines")
		pulses.append(start)
	if [round(start, 2) for start in starts[20]] != [round(start, 2) for start in pulses]:
		raise RuntimeError(f"{name}: public 20 and 17 do not turn on together")
	return pulses


def build(runs_root: Path) -> dict[str, Any]:
	runs = {name: _load_run(runs_root, name) for name in RUN_NAMES}
	for name, run in runs.items():
		if run.get("failure") is not None:
			raise RuntimeError(f"run {name} failed: {run['failure']}")
		if run["library_sha256"] != LIBRARY_SHA256:
			raise RuntimeError(f"run {name} used an unpinned library")
		if run["game"] != RUNS[name][0]:
			raise RuntimeError(f"run {name} booted {run['game']}")

	self_run = runs["self-test"]
	press = self_test_presses(self_run)[0]
	self_sequence = [event["number"] for event in self_run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > press - 0.5]
	self_lamps = sorted({event["number"] for event in self_run["events"] if event["event"] == "lamp"})
	if [address for address in DECODER_HOLES if address in self_lamps] or len(self_lamps) != 60:
		raise RuntimeError(f"burn-in lamps are not the sixty SCR outputs: {self_lamps}")

	solenoid_run = runs["solenoid-test"]
	first_step = solenoid_run["steps"][1]
	ignored = [check["after_pulses"] for check in first_step.get("pulse_checks", []) if not check["matched_outputs"]]
	pairs = solenoid_test_pairs(solenoid_run)
	first_cycle = pairs[:19]
	if [number for number, _ in first_cycle] != list(range(1, 20)):
		raise RuntimeError(f"solenoid test did not show drivers 1-19 in order: {first_cycle}")
	cycles = [pairs[index:index + 19] for index in range(0, len(pairs) - 18, 19)]
	if any(cycle != first_cycle for cycle in cycles):
		raise RuntimeError("solenoid test cycles disagree")
	physical_to_public = {str(number): address for number, address in first_cycle}

	readings = switch_test_readings(runs["switch-test"])
	if sorted(readings) != list(range(1, 41)) or any(readings[address] != str(address) for address in range(1, 41)):
		raise RuntimeError(f"switch test readings disagree with the addresses: {readings}")

	credits, chute_counts = coin_readings(runs["coin-bookkeeping"])
	if chute_counts != {"09": 1, "10": 2, "11": 3}:
		raise RuntimeError(f"bookkeeping chute counts are not one, two and three coins: {chute_counts}")

	all_lamps = sorted({event["number"] for name in RUN_NAMES for event in runs[name]["events"] if event["event"] == "lamp"})
	if [address for address in DECODER_HOLES if address in all_lamps]:
		raise RuntimeError("a lamp decoder hole changed state")
	outside = sorted({event["number"] for event in runs["gameplay"]["events"] if event["event"] == "lamp"})

	gameplay_actions = windowed_actions(runs["gameplay"])
	by_label = {action["step"]["label"]: action for action in gameplay_actions}
	named: dict[str, int] = {}
	for switch, label in SPOT_STEPS.items():
		action = by_label[label]
		coils = [address for address in action["on_order"] if address in KNOCK_DOWN_COILS]
		if len(action["out"]) < 1 or len(coils) != 1:
			raise RuntimeError(f"gameplay: {label} did not spot one METEOR target and put a lamp out: {action['on_order']} {action['out']}")
		if len(action["out"]) != 1:
			raise RuntimeError(f"gameplay: {label} put out {action['out']}")
		named[f"switch-{switch}-spot-lamp"] = action["out"][0]
		named[f"switch-{switch}-spot-coil"] = coils[0]
	# Each METEOR target held down puts out its own drop lamp; the sixth completes the bank, which relights them all.
	for letter, (switch, _, lamp) in METEOR_BANK.items():
		action = next(item for item in gameplay_actions if item["step"]["label"].startswith("six-bank:") and item["switch"] == switch and item["step"].get("state", 1))
		expected = [] if letter == "R" else [lamp]
		if action["out"] != expected:
			raise RuntimeError(f"gameplay: METEOR {letter} target down put out {action['out']}, not {expected}")
		if letter != "R":
			named[f"meteor-{letter.replace(' ', '-').lower()}-drop-lamp"] = lamp
	# After a drain the ROM knocks down again the targets whose drop lamps are out: the bank's memory.
	drain = by_label["ball 1: ball drains into the outhole"]
	lamp_state: dict[int, int] = {}
	for event in runs["gameplay"]["events"]:
		if event["event"] == "lamp" and event["time_s"] <= drain["start"]:
			lamp_state[event["number"]] = event["state"]
	made = [letter for letter, (_, _, lamp) in METEOR_BANK.items() if not lamp_state.get(lamp)]
	restored = sorted({address for label in DRAIN_STEPS for address in by_label[label]["on_order"] if address in KNOCK_DOWN_COILS})
	if not made or restored != sorted(METEOR_BANK[letter][1] for letter in made):
		raise RuntimeError(f"gameplay: the drain restored coils {restored}, not the made targets {made}")
	if "R" in made:
		named["meteor-r-drop-lamp"] = METEOR_BANK["R"][2]
	game_end = by_label[GAME_END_STEP]
	if game_end["on_order"] != [6] or not {45, 63} <= set(game_end["lit"]) or 19 in game_end["end_snapshot"]["active_solenoids"]:
		raise RuntimeError(f"gameplay: the game end fired {game_end['on_order']} and lit {game_end['lit']}")
	# The knocker at the game end is the match award: the score's last two digits are the match number and a credit is added.
	ending = game_end_readings(runs["gameplay"])
	if ending["score"][-2:] != ending["match"] or int(ending["credits_after"]) != int(ending["credits_before"]) + 1:
		raise RuntimeError(f"gameplay: the game end is not a match award: {ending}")
	tilt = by_label["ball 2: tilt sw7"]
	if tilt["lit"] != [61] or 19 not in tilt["transitioned"] or 19 in tilt["end_snapshot"]["active_solenoids"]:
		raise RuntimeError(f"gameplay: the tilt did not drop 19 and light 61 alone: {tilt['lit']} {tilt['transitioned']}")
	named["tilt-lamp"] = 61
	tilted_sling = by_label["ball 2: right slingshot while tilted"]
	if tilted_sling["on_order"]:
		raise RuntimeError("gameplay: the tilted slingshot fired a solenoid")

	power_ups: dict[str, list[float]] = {"gameplay": initialisation_pulses("gameplay", runs["gameplay"], 2)}
	for name in VARIANT_RUNS:
		power_ups[name] = initialisation_pulses(name, runs[name], 1)
	slam = by_label["second game: slam sw8"]
	if not slam["start"] < power_ups["gameplay"][1] <= slam["end"]:
		raise RuntimeError("gameplay: the second initialisation is not in the slam step")

	comparisons: dict[str, dict[str, Any]] = {}
	knock_downs = set(KNOCK_DOWN_COILS)
	reference_drain = {address for label in DRAIN_STEPS for address in by_label[label]["on_order"]} - knock_downs
	if reference_drain != {3, 7, 9, 13, 15}:
		raise RuntimeError(f"gameplay: the first drain and serve fire {sorted(reference_drain)} besides the knock-down coils")
	# The variant note says meteor fires only target restores after the release, so the window must hold restores and nothing else.
	release = set(by_label[DRAIN_STEPS[1]]["on_order"])
	if not release or release - knock_downs:
		raise RuntimeError(f"gameplay: the served ball's release fires {sorted(release)}, not target restores alone")
	for name in VARIANT_RUNS:
		actions = windowed_actions(runs[name])
		same: list[str] = []
		spot: dict[str, int] = {}
		for action in actions:
			label = action["step"]["label"]
			if label in DRAIN_STEPS:
				continue
			reference = by_label.get(label)
			if reference is None:
				raise RuntimeError(f"{name}: step {label!r} has no gameplay counterpart")
			if set(action["on_order"]) == set(reference["on_order"]) and action["transitioned"] == reference["transitioned"]:
				same.append(label)
			elif (set(action["on_order"]) - knock_downs == set(reference["on_order"]) - knock_downs
					and len([address for address in action["on_order"] if address in knock_downs]) == len([address for address in reference["on_order"] if address in knock_downs]) == 1):
				spot[label] = next(address for address in action["on_order"] if address in knock_downs)
			else:
				raise RuntimeError(f"{name}: step {label!r} fires {action['on_order']}, meteor {reference['on_order']}")
		targets = {switch for switch, _, _ in METEOR_BANK.values()}
		if any(action["switch"] in targets for action in actions):
			raise RuntimeError(f"{name}: a METEOR target switch is operated, so its drain is not comparable without a restore")
		drained = {address for action in actions if action["step"]["label"] in DRAIN_STEPS for address in action["on_order"]}
		if drained - knock_downs != reference_drain or drained & knock_downs:
			raise RuntimeError(f"{name}: the drain and serve fire {sorted(drained)}, not meteor's {sorted(reference_drain)} without a restore")
		# Each window on its own must carry the kick and the four resets: the note says the variant fires them in the drain window and again after the release.
		for window in DRAIN_STEPS:
			fired = {address for action in actions if action["step"]["label"] == window for address in action["on_order"]}
			if fired != reference_drain:
				raise RuntimeError(f"{name}: step {window!r} fires {sorted(fired)}, not the outhole kick and the bank resets {sorted(reference_drain)}")
		comparisons[name] = {"same": same, "spot": spot}
	if set(by_label[DRAIN_STEPS[0]]["on_order"]) - knock_downs != reference_drain:
		raise RuntimeError("gameplay: the drain window does not fire the outhole kick and the bank resets before the served ball leaves")

	manifest_sha, file_count, total_bytes = directory_manifest_sha256(runs_root)
	raw_runs = []
	for name in RUN_NAMES:
		run = runs[name]
		scenario_path = ROOT / f"tools/harness-scenarios/stern/{RUNS[name][1]}.json"
		scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
		if file_sha256(scenario_path) != run["scenario"]["sha256"]:
			raise RuntimeError(f"scenario for {name} no longer matches the run")
		record: dict[str, Any] = {
			"name": name,
			"sha256": file_sha256(runs_root / name / "run.json"),
			"scenario_path": f"tools/harness-scenarios/stern/{RUNS[name][1]}.json",
			"scenario_sha256": run["scenario"]["sha256"],
			"action_count": len(scenario["actions"]),
			"self_test_pulses": len(self_test_presses(run)),
			"nvram_initialization": "empty; the isolated PinMAME state directory was created from scratch for this run",
			"initial_switches": [{"switch": item["switch"], "state": item["state"]} for item in scenario.get("initial_switches", [])],
			"snapshot_count": len(run["snapshots"]),
		}
		if run.get("watch_switches"):
			record["watch_switches"] = sorted(set(run["watch_switches"]))
		raw_runs.append(record)

	all_solenoids = sorted({event["number"] for name in RUN_NAMES for event in runs[name]["events"] if event["event"] == "solenoid"})
	play_solenoids = sorted({event["number"] for name in ("gameplay", *VARIANT_RUNS) for event in runs[name]["events"] if event["event"] == "solenoid"})
	held = {address: [(start, end) for start, end in intervals(runs["gameplay"], address)] for address in (18, 19)}

	def seen(name: str) -> list[int]:
		return sorted({event["number"] for event in runs[name]["events"] if event["event"] == "solenoid"})

	def spans(address: int) -> str:
		return "; ".join(f"{start:.2f}-{end:.2f} s" if end is not None else f"{start:.2f} s to the end" for start, end in held[address])

	def variant_note(name: str) -> str:
		driver = RUNS[name][0]
		comparison = comparisons[name]
		text = (f"The {driver} ROM set on the same hardware: a credited game, the thumper, both slingshots, the stand-up target, the right three-bank held down and raised, both flipper "
			"buttons, a drain and the next serve. The four continuous lines are pulsed together once, at "
			f"{power_ups[name][0]:.2f} s. Every step before the drain fires the same set of solenoids as the same step of the meteor gameplay run (sets compared; firing order, "
			"timing and lamp changes are not)")
		for label, coil in comparison["spot"].items():
			reference = next(address for address in by_label[label]["on_order"] if address in KNOCK_DOWN_COILS)
			text += f", except that `{label}` spots its METEOR target with knock-down coil {coil} where meteor fired {reference} (the ROM picks the target it spots)"
		return text + (". The drain and the next serve taken together fire the outhole kicker (15) and the bank resets " + ", ".join(str(address) for address in sorted(reference_drain - {15}))
			+ " as in meteor, though not in the same windows: meteor fires them before the served ball leaves the outhole and only target restores after it, this run fires them "
			"again after it. No METEOR target switch closed in this run (the harness does not drop a target when the ROM fires its knock-down coil), and no knock-down coil fired at the "
			"drain or the serve; meteor's run, with four METEOR targets down, also restored those four there.")

	return {
		"driver_ids": sorted({driver for driver, _ in RUNS.values()}),
		"extractor": {"id": "tools/summarize_meteor_runtime.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <vpinmame-roms> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/stern/<scenario>.json --output <external-run.json>, "
				"for the five meteor runs (self-test, solenoid-test, switch-test, coin-bookkeeping, gameplay) and one variant run each of meteora, meteorb, meteorbf, meteorc, meteord and meteorfp. "
				"ROM archives: " + ", ".join(f"{driver} {digest}" for driver, digest in ROM_ARCHIVES.items()) + ". Each scenario starts with a 25 s wait for the ROM's power-up test. "
				"Each set_switch or pulse is a host stimulus, never a ROM observation; display readings are seven-segment words read as digits.",
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": PINMAME_REVISION, "sha256": LIBRARY_SHA256},
			"game": "meteor",
			"observations": {
				"lamp_addresses_driven_outside_self_test": outside,
				"lamp_addresses_seen": self_lamps,
				"lamp_decoder_holes_not_seen": [address for address in DECODER_HOLES if address not in all_lamps],
				"named_output_addresses": dict(sorted(named.items())),
				"physical_service_solenoid_to_public": physical_to_public,
				"public_solenoid_decoder_holes_not_seen": [16] if 16 not in all_solenoids else [],
				"runs": {
					"self-test": {
						"ordered_solenoid_on_sequence": self_sequence,
						"solenoid_addresses_seen": sorted(set(self_sequence)),
						"note": f"One Self Test press starts the burn-in test. All sixty lamp addresses ({len(self_lamps)} seen) are driven and the four decoder holes 16, 32, 48 and 64 never are; "
							f"the solenoids fire in a repeating 19-step cycle that starts with public {self_sequence[0]}.",
						"limitation": "The burn-in drives the displays with test frames, so the driver numbers are read from the solenoid-test run instead.",
					},
					"solenoid-test": {
						"ordered_solenoid_on_sequence": [address for _, address in pairs],
						"solenoid_addresses_seen": sorted({address for _, address in pairs}),
						"note": "Four Self Test presses start the solenoid test, which pulses one driver at a time and shows its number on the player displays (read 0.25 s after each pulse; every frame read "
							"is pinned in the frame-readings seed). " + (f"The ROM ignored press {', '.join(str(number) for number in ignored)} of the first step. " if ignored else "The ROM accepted every press. ")
							+ f"Over {len(cycles)} complete cycles, driver numbers 1-19 pair with public addresses " + ", ".join(f"{number}->{address}" for number, address in first_cycle) + ".",
					},
					"switch-test": {
						"note": "Five Self Test presses reach the switch test; with each matrix address 1-40 closed alone, the player 1 display read that address's own number (every frame pinned in the "
							"frame-readings seed): " + ", ".join(f"{address}->{reading}" for address, reading in sorted(readings.items())) + ".",
					},
					"coin-bookkeeping": {
						"named_action_observations": action_observations(runs["coin-bookkeeping"]),
						"solenoid_addresses_seen": seen("coin-bookkeeping"),
						"note": "Coin input 1 is closed once, coin input 2 twice and coin input 3 three times at PinMAME's default option switches (S20 and S21 ON, the rest OFF). The credit "
							"display read after each coin: " + ", ".join(credits) + " (maximum-credits switches 17-19 OFF cap credits at 5). Sixteen Self Test presses then reach the bookkeeping functions; the match/ball-in-play display "
							"shows the function number and player 1 its count: " + ", ".join(f"function {function} -> {count}" for function, count in sorted(chute_counts.items()))
							+ ". Every frame read is pinned in the frame-readings seed.",
					},
					"gameplay": {
						"named_action_observations": action_observations(runs["gameplay"]),
						"solenoid_addresses_seen": seen("gameplay"),
						"note": "A credited game on the single-ball outhole: each scoring switch is closed alone, each three-target bank is held down and raised, the six-target METEOR bank is held down in "
							"order M to R and raised, both flipper buttons are pressed, the ball drains, ball 2 is tilted, ball 3 drains to end the game, and a second game is started and slammed. "
							"Knock-down coils are not answered, so a target the ROM spots is never seen down. Each METEOR target held down puts out its own drop lamp ("
							+ ", ".join(f"{letter} {lamp}" for letter, (_, _, lamp) in METEOR_BANK.items() if letter != "R") + "; the sixth, R, completes the bank and relights them). At the first drain "
							"the drop lamps of " + ", ".join(made) + " were out, and the ROM fired exactly those targets' knock-down coils " + str(restored) + " around the serve: the bank's memory. "
							"After the last drain the outhole kicker does not fire; public 19 drops and 45 and 63 light. Player 1's final score " + ending["score"] + " ends in the match number "
							+ ending["match"] + ", the credits go from " + ending["credits_before"] + " to " + ending["credits_after"] + ", and the knocker (6) fires once: a match award "
							"(option switch 21, ON at PinMAME's default). The scenario labels the tilted ball's serve step as bonus collection; the manual says a tilt forfeits the bonus, and the "
							"step observes only the serve. The four continuous lines are pulsed together at "
							+ " and ".join(f"{start:.2f} s" for start in power_ups["gameplay"]) + " (power-up, and the slam); public 18 is on " + spans(18) + " and public 19 " + spans(19)
							+ f". Every lamp address this run drives ({len(outside)}) is listed as driven outside the self test.",
					},
					**{name: {"named_action_observations": action_observations(runs[name]), "solenoid_addresses_seen": seen(name), "note": variant_note(name)} for name in VARIANT_RUNS},
				},
				"solenoid_addresses_seen": all_solenoids,
			},
			"raw_runs": raw_runs,
			"rom_archive_sha256": ROM_ARCHIVES["meteor"],
		},
		"source": {
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and raw NVRAM remain external",
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"manifest_algorithm": "source.sha256 is a directory manifest digest, not a file hash: list every file below source.path as {path, size, sha256} with path relative and POSIX-separated, sort by path, serialise as compact canonical JSON (indent=None, separators=(',',':'), sort_keys=True, ensure_ascii=False), encode UTF-8 and take the SHA-256. "
				f"At capture time the tree held {file_count} files totalling {total_bytes} bytes. Individual run hashes are in runtime.raw_runs[].sha256. Play runs observed solenoid addresses {play_solenoids}.",
			"path": "external:pinmame-review-artifacts/meteor-1979/harness",
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
	parser.add_argument("--runs", type=Path, required=True, help="directory holding the eleven run folders")
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true")
	mode.add_argument("--check", action="store_true")
	args = parser.parse_args()
	summary = build(args.runs)
	if args.write:
		write_json(OUTPUT_PATH, summary)
		print(f"Wrote {OUTPUT_PATH}")
	else:
		if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_bytes() != canonical_bytes(summary):
			raise SystemExit(f"{OUTPUT_PATH} does not match the retained runs")
		print("Meteor runtime summary matches the retained runs.")


if __name__ == "__main__":
	main()
