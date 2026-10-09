"""Derive the compact Black Rose runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts root),
checks that it ran the committed scenario, the pinned binary and the br_l4 ROM with built-in mechanisms disabled, and writes the
derived observations beside the other runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's visual reading
of that snapshot's retained DMD frame; its ``pixel_sha256`` pins the frame. The tool refuses a raw run whose transitions no longer
support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.black-rose.1992"
GAME = "br_l4"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "8b66e2656562c39590033f51253bb630220178457b1c1c6e09ac023fc1a540a3"
HARNESS_DIRECTORY = "black-rose-1992/harness"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-fliptronic"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-fliptronic"
FRAME_READINGS_PATH = ROOT / "tools/seeds/bally/black-rose-1992-frame-readings.json"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The exact external directory manifest (built by tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM performed its own factory reset before the "
	"scenario left the message loop with Escape"
)
IDENTIFICATION = "BLACK ROSE / 20013 REV. L-4"
IDENTIFICATION_LABEL = "Enter 1 (game identification)"


def _command(scenario: str, extra: str) -> str:
	return (
		"python tools/run_pinmame_harness.py --library <libpinmame> --game br_l4 --rom-path <vpinmame-roms> --work-dir <new-isolated-state> "
		f"--handle-mechanics 0 --scenario {SCENARIO_DIRECTORY}/{scenario}.json --dmd-dir <external-dmd-dir> --output <external-run.json>. "
		+ extra
	)


# --- T.1 SWITCH EDGES ----------------------------------------------------------------------------------
ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# The name the ROM prints on the top line while it reads the switch as active (read from the retained frames). 37's frame clips
# the first letter of RIGHT RETURN LANE at the display edge.
EDGE_NAMES = {
	14: "PLUMB BOB TILT", 15: "OUTHOLE", 16: "RIGHT TROUGH", 17: "CENTER TROUGH", 18: "LEFT TROUGH", 25: "SHOOTER",
	26: "LEFT OUTLANE", 27: "LEFT RETURN LANE", 28: "LEFT SLINGSHOT", 31: "BOT. STANDUPS BOT", 32: "BOT. STANDUPS MID",
	33: "BOT. STANDUPS TOP", 34: "FIRE BUTTON", 35: "CANNON KICKER", 36: "RIGHT OUTLANE", 37: "IGHT RETURN LANE",
	38: "RIGHT SLINGSHOT", 41: "MID. STANDUPS TOP", 42: "MID. STANDUPS MID", 43: "MID. STANDUPS BOT", 44: "L. RAMP ENTER",
	45: "TOP LEFT LOOP", 46: "LEFT JET", 47: "RIGHT JET", 48: "BOTTOM JET", 51: "TOP STANDUPS BOT", 52: "TOP STANDUPS MID",
	53: "TOP STANDUPS TOP", 54: "RAMP DOWN", 55: "BALL POPPER", 56: "R. RAMP MADE", 57: "JETS EXIT", 58: "JETS ENTER",
	61: "SUBWAY TOP", 62: "BACKBOARD RAMP", 63: "LOCKUP 1", 64: "LOCKUP 2", 65: "R. SINGLE STANDUP", 66: "SUBWAY BOTTOM",
	71: "LOCKUP ENTER", 72: "MIDDLE RAMP", 76: "R. RAMP ENTER",
}
EDGE_SWITCHES = tuple(EDGE_NAMES) + (112, 114, 116)
# The Fliptronic buttons: pressing one fires its flipper, PinMAME synthesizes the end-of-stroke bit, and the ROM names that.
FLIPPER_EDGES = {
	112: ("R. FLIPPER EOS", "F1", "BLK-GRN BLK", {45, 46}),
	114: ("L. FLIPPER EOS", "F3", "BLK-BLU BLK", {47, 48}),
	116: ("UR FLIPPER EOS", "F5", "BLK-VIO BLK", {33, 34}),
}
# Switches whose closure the ROM answers with a coil even inside T.1: the slingshots and the jet bumpers.
EDGE_COILS = {28: 6, 38: 5, 46: 13, 47: 14, 48: 15}


def _wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{ROW_WIRES[row]} GRN-{COLUMN_WIRES[column]}"


def _edge_reading(label: str) -> str | None:
	if label == "T.1 started, every watched switch at public 0":
		return "SWITCH EDGES / T.1"
	if label == IDENTIFICATION_LABEL:
		return IDENTIFICATION
	parts = label.split(" -> ")
	if len(parts) != 2:
		return None
	address, level = int(parts[0]), int(parts[1])
	if address in FLIPPER_EDGES:
		name, last, wires, _ = FLIPPER_EDGES[address]
		return f"{name} / T.1 LAST SW {last} / {wires}" if level else f"SWITCH EDGES / T.1 LAST SW {last} / {wires}"
	head = EDGE_NAMES[address] if level else "SWITCH EDGES"
	return f"{head} / T.1 LAST SW {address} / {_wires(address)}"


# --- T.1 on the unfitted upper left flipper ------------------------------------------------------------
UPPER_LEFT_READINGS = {
	"T.1 started, every watched switch at public 0": "SWITCH EDGES / T.1 (switch grid: the Fliptronic column shows no closed position)",
	"T.1 with 118 at 1, frame 2": "SWITCH EDGES / T.1 (no switch named; the switch grid marks one Fliptronic-column position closed)",
	"T.1 with 118 at 0, frame 2": "SWITCH EDGES / T.1 (the Fliptronic-column mark is gone)",
	"T.1 with 117 at 1, frame 2": "SWITCH EDGES / T.1 (no switch named; the switch grid marks one Fliptronic-column position closed)",
	"T.1 with 117 at 0, frame 2": "SWITCH EDGES / T.1 (the Fliptronic-column mark is gone)",
	IDENTIFICATION_LABEL: IDENTIFICATION,
}

# --- T.4 SOLENOID TEST ---------------------------------------------------------------------------------
T4_ORDER = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15)
T4_NAMES = {
	1: "BALL POPPER", 2: "OUTHOLE", 3: "CANNON MOTOR", 4: "BALL RELEASE", 5: "RIGHT SLINGSHOT", 6: "LEFT SLINGSHOT", 7: "KNOCKER",
	8: "CANNON KICKER", 9: "BALL LOCKUP", 10: "RAMP UP", 11: "RAMP DOWN", 13: "LEFT JET", 14: "RIGHT JET", 15: "BOTTOM JET",
}
T4_WIRES = {
	1: "VIO-BRN VIO-YEL", 2: "VIO-RED VIO-YEL", 3: "VIO-ORN VIO-YEL", 4: "VIO-YEL VIO-YEL", 5: "VIO-GRN VIO-YEL", 6: "VIO-BLU VIO-YEL",
	7: "VIO-BLK VIO-YEL", 8: "VIO-GRY VIO-YEL", 9: "BRN-BLK VIO-ORN", 10: "BRN-RED VIO-ORN", 11: "BRN-ORN VIO-ORN",
	13: "BRN-GRN VIO-ORN", 14: "BRN-BLU VIO-ORN", 15: "BRN-VIO VIO-ORN",
}

# --- T.5 FLASHER TEST ----------------------------------------------------------------------------------
T5_ORDER = tuple(range(17, 29))
T5_NAMES = {
	17: "LEFT BOTTOM", 18: "LEFT TOP", 19: "RIGHT BOTTOM", 20: "RIGHT TOP", 21: "RIGHT RAMP", 22: "LEFT RAMP", 23: "LOCKER OPEN",
	24: "LEFT SWORD", 25: "TOP POPPER", 26: "CANNON", 27: "FIRE BUTTON", 28: "RIGHT SWORD",
}
T5_WIRES = {
	17: "BLK-BRN", 18: "BLK-RED", 19: "BLK-ORN", 20: "BLK-YEL", 21: "BLU-GRN", 22: "BLU-BLK", 23: "BLU-VIO", 24: "BLU-GRY",
	25: "BLU-BRN", 26: "BLU-RED", 27: "BLU-ORN", 28: "BLU-YEL",
}
# The frame of each step whose blinking name was legible.
T5_FRAMES = {17: "T.5 step 0, frame 1", **{address: f"T.5 step {address - 17}, frame 3" for address in range(18, 29)}}

# --- T.6 GENERAL ILLUMINATION --------------------------------------------------------------------------
GI_NAMES = {0: "JETS & BACK RAMP", 1: "TOP PLAYFIELD", 2: "BOT. PLAYFIELD", 3: "LEFT/TOP INSERT", 4: "RIGHT INSERT"}
GI_WIRES = {0: "WHT-BRN BRN", 1: "WHT-ORN ORN", 2: "WHT-YEL YEL", 3: "WHT-GRN GRN", 4: "WHT-VIO VIO"}

# --- T.8 SINGLE LAMPS ----------------------------------------------------------------------------------
LAMP_ORDER = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
T8_NAMES = {
	11: "SPECIAL", 12: "JET ENTER 8K", 13: "JET ENTER 4K", 14: "JET ENTER 2K", 15: "JET ENTER 1K", 16: "JET ENTER JEWEL",
	17: "COMBO SHOT RIGHT", 18: "R. SINGLE STANDUP", 21: "LETTER (S)INK", 22: "LETTER S(I)NK", 23: "LETTER SI(N)K",
	24: "LETTER SIN(K)", 25: "LETTER (S)HIP", 26: "LETTER S(H)IP", 27: "LETTER SH(I)P", 28: "LETTER SHI(P)",
	31: "BOT. STANDUPS BOT.", 32: "BOT. STANDUPS MID.", 33: "BOT. STANDUPS TOP", 34: "RGT RAMP 100K", 35: "RGT RAMP 200K",
	36: "RGT RAMP 300K", 37: "RGT RAMP 400K", 38: "RGT RAMP MILL.", 41: "MID. STANDUPS TOP", 42: "MID. STANDUPS MID.",
	43: "MID. STANDUPS BOT.", 44: "LEFT OUTLANE", 45: "LEFT RETURN LANE", 46: "IGHT RETURN LANE", 47: "RIGHT OUTLANE",
	48: "SHOOT AGAIN", 51: "TOP STANDUPS BOT.", 52: "TOP STANDUPS MID.", 53: "TOP STANDUPS TOP", 54: "LOCKUP 1", 55: "LOCKUP 2",
	56: "LOCKUP JEWEL", 57: "LEFT RAMP COINS", 58: "BOT. STNDUP JEWEL", 61: "MID. RAMP JEWEL", 62: "TOP LOOP JEWEL",
	63: "TOP STNDUP JEWEL", 64: "BROADSIDE JEWEL", 65: "BOT. STNDUP JEWEL", 66: "R. RAMP COINS", 67: "COMBO SHOT LEFT",
	68: "MULTIBALL READY", 71: "MILLIONS", 72: "RIGGING SWING", 73: "TREASURE CHEST", 74: "WALK THE PLANK", 75: "INSTANT MULTI",
	76: "KNIFE THROW", 77: "POLLY", 78: "INSERT LEFT", 81: "SKILL (OPEN)", 82: "SKILL (LOCKER)", 83: "MID. RAMP 200K",
	84: "MID. RAMP 300K", 85: "MID. RAMP 400K", 86: "JACKPOT", 87: "INSERT RIGHT", 88: "CREDIT BUTTON",
}
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}

# --- T.12 FLIPPER COIL TEST ----------------------------------------------------------------------------
T12_ORDER = (45, 46, 47, 48, 33, 34)
T12_NAMES = {45: "R. FLIP. POWER", 46: "R. FLIP. HOLD", 47: "L. FLIP. POWER", 48: "L. FLIP. HOLD", 33: "U.R. FLIP. POWER", 34: "U.R. FLIP. HOLD"}
T12_WIRES = {45: "BLU-VIO BLU-YEL", 46: "ORN-GRN BLU-YEL", 47: "BLU-GRY GRY-YEL", 48: "ORN-BLU GRY-YEL", 33: "BLK-YEL BLU-YEL", 34: "ORN-VIO BLU-YEL"}
# A power step publishes the hold winding with the power winding; a hold step publishes the hold winding alone.
T12_PUBLISHED = {45: {45, 46}, 46: {46}, 47: {47, 48}, 48: {48}, 33: {33, 34}, 34: {34}}
T12_FRAMES = {45: "T.12 step 6, frame 3", 46: "T.12 step 1, frame 3", 47: "T.12 step 2, frame 3", 48: "T.12 step 3, frame 3", 33: "T.12 step 4, frame 3", 34: "T.12 step 5, frame 3"}

# --- T.14 CANNON TEST ----------------------------------------------------------------------------------
CANNON_READINGS = {
	IDENTIFICATION_LABEL: IDENTIFICATION,
	"T.14 menu item, frame 1": "TEST MENU / T.14 CANNON TEST",
	"T.14 started, frame 1": "T.12 MOTOR = OFF / SW.35 CANNON = OPEN",
	"T.14 with 35 at 1, frame 1": "CANNON TEST / T.12 MOTOR = OFF / SW.35 CANNON = CLOSED",
	"T.14 with 35 at 0, frame 1": "T.12 MOTOR = OFF / SW.35 CANNON = OPEN",
	"T.14 after the first toggle, frame 3": "CANNON TEST / T.12 MOTOR = ON / SW.35 CANNON = OPEN",
	"T.14 after the second toggle, frame 3": "CANNON TEST / T.12 MOTOR = OFF / SW.35 CANNON = OPEN",
}


# --- Shared helpers ------------------------------------------------------------------------------------
def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(review_root: Path, directory: str, scenario: str) -> dict[str, Any]:
	run_directory = review_root / HARNESS_DIRECTORY / directory / GAME
	run_path = run_directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{scenario}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Black Rose {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(run_directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
		raise ValueError(f"built-in mechanisms must be disabled: {run_path}")
	run["_directory"] = run_directory
	run["_pins"] = json.loads(FRAME_READINGS_PATH.read_bytes())["runs"][directory]
	return run


def _snapshot(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["snapshots"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one snapshot labelled {label!r}, found {len(matches)}")
	return matches[0]


def _step(run: dict[str, Any], label: str) -> dict[str, Any]:
	matches = [item for item in run["steps"] if item["label"] == label]
	if len(matches) != 1:
		raise ValueError(f"expected one step labelled {label!r}, found {len(matches)}")
	return matches[0]


def _risen(step: dict[str, Any], channel: str = "solenoids") -> set[int]:
	"""Addresses whose recorded transitions during the step include an active state, without 31 (the WPC GILAMPS bit-7 mirror)."""
	return {item["number"] for item in step["transitions"][channel] if any(item["states"])} - {31}


def _window(run: dict[str, Any], prefix: str, channel: str = "solenoids") -> set[int]:
	"""Rising addresses over a step and the frames taken after it."""
	return set().union(*(_risen(step, channel) for step in run["steps"] if step["label"] == prefix or step["label"].startswith(prefix + ", frame")))


def _matched(run: dict[str, Any], label: str) -> set[int]:
	"""Outputs a wait_until_output checkpoint saw active, refused when the checkpoint never matched."""
	matched = {item["number"] for item in _step(run, label).get("matched_outputs") or []}
	if not matched:
		raise ValueError(f"checkpoint {label!r} saw none of its outputs")
	return matched


def _diagnostic(run: dict[str, Any], label: str, text: str) -> dict[str, Any]:
	"""A visual reading of one retained frame, refused unless that frame's own PGM file carries the snapshot's pixels and is not blank."""
	snapshot = _snapshot(run, label)
	displays = [item for item in snapshot["displays"] if item["index"] == 0]
	if len(displays) != 1:
		raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
	frame = run["_directory"] / "dmd" / Path(displays[0]["artifact"].replace("\\", "/")).name
	data = frame.read_bytes()
	pixels = data[len(data) - 128 * 32:]
	if not data.startswith(b"P5\n128 32\n") or hashlib.sha256(pixels).hexdigest() != displays[0]["pixel_sha256"]:
		raise ValueError(f"retained frame for {label!r} does not carry the snapshot's pixels: {frame}")
	if displays[0]["nonzero_pixels"] == 0 or not any(pixels):
		raise ValueError(f"a reading cannot cite a blank frame: {label!r}")
	pin = run["_pins"].get(label)
	if pin is None or pin["pixel_sha256"] != displays[0]["pixel_sha256"] or pin["reading"] != text:
		raise ValueError(f"snapshot {label!r} does not carry the frame the curator read as {text!r}")
	return {
		"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
		"display_index": 0,
		"interpreted_text": text,
		"label": label,
		"nonzero_pixels": displays[0]["nonzero_pixels"],
		"pixel_sha256": displays[0]["pixel_sha256"],
	}


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _observation(label: str, stimulus: list[int], solenoids: list[int] | None = None, **extra: Any) -> dict[str, Any]:
	record = {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": stimulus,
		"input_address": stimulus[-1],
		"input_kind": "switch",
		"label": label,
		"observed_switch_addresses": [],
		"result": "observed",
		"transitioned_solenoid_addresses": solenoids or [],
	}
	record.update(extra)
	return record


def _document(directory: str, scenario: str, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/black_rose_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": f"br-l4-{directory}",
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/{GAME}/run.json",
					"scenario_path": f"{SCENARIO_DIRECTORY}/{scenario}.json",
					"scenario_sha256": run["scenario"]["sha256"],
					"self_test_pulses": 0,
					"snapshot_count": len(run["snapshots"]),
					"watch_switches": run["watch_switches"],
				}
			],
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
		},
		"source": {
			"attribution": ATTRIBUTION,
			"kind": "runtime_scenario",
			"license": "NOASSERTION",
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/{GAME}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


# --- Builders ------------------------------------------------------------------------------------------
def build_edges(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "switch-edges", "br-switch-edges")
	snapshots = [_diagnostic(run, snapshot["label"], text) for snapshot in run["snapshots"] if (text := _edge_reading(snapshot["label"])) is not None]
	named = []
	for address in EDGE_SWITCHES:
		rising = _risen(_step(run, f"{address} -> 1"))
		for level in (1, 0):
			held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> {level}")["watched_switches"]}
			if held.get(address) != level:
				raise ValueError(f"host did not drive {address} to {level}")
		# Both the name at 1 and its release at 0 must come from read frames.
		readings = {item["label"] for item in snapshots}
		if {f"{address} -> 1", f"{address} -> 0"} - readings:
			raise ValueError(f"T.1 frames for both levels of {address} are required")
		if address in FLIPPER_EDGES:
			name, last, _, coils = FLIPPER_EDGES[address]
			if rising != coils:
				raise ValueError(f"public {address} fired {sorted(rising)}, not the flipper {sorted(coils)}")
			named.append(_observation(
				f"T.1 with host public {address} set to 1: the ROM fires the flipper ({'/'.join(map(str, sorted(coils)))}) and names {last} ({name}); at 0 the name clears",
				[address], sorted(rising),
			))
			continue
		expected = {EDGE_COILS[address]} if address in EDGE_COILS else set()
		if rising != expected:
			raise ValueError(f"public {address} fired {sorted(rising)}, expected {sorted(expected)}")
		label = f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and clears it at 0"
		if expected:
			label += f"; the ROM fires solenoid {EDGE_COILS[address]} on the closure"
		named.append(_observation(label, [address], sorted(rising)))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-switch-edges",
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 1.5 s; the snapshot after it records the ROM's "
		"T.1 display and the watched public switch levels. The ROM names a switch on its top line while it reads the switch as active and "
		"prints its row and column wire colours; a Fliptronic button fires its flipper and the ROM names the synthesized end-of-stroke bit.",
	)
	return _document("switch-edges", "br-switch-edges", run, observations, command)


def build_upper_left(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "switch-edges-upper-left", "br-switch-edges-upper-left")
	snapshots = [_diagnostic(run, label, text) for label, text in UPPER_LEFT_READINGS.items()]
	named = []
	for address in (118, 117):
		for level in (1, 0):
			if _risen(_step(run, f"{address} -> {level}")) or _window(run, f"T.1 with {address} at {level}"):
				raise ValueError(f"public {address} at {level} moved an output")
		on = _snapshot(run, f"T.1 with {address} at 1, frame 2")["displays"][0]["pixel_sha256"]
		off = _snapshot(run, f"T.1 with {address} at 0, frame 2")["displays"][0]["pixel_sha256"]
		start = _snapshot(run, "T.1 started, every watched switch at public 0")["displays"][0]["pixel_sha256"]
		if on == off or off != start:
			raise ValueError(f"public {address} must change the switch grid at 1 and restore it at 0")
		named.append(_observation(
			f"T.1 with host public {address} at 1: the switch grid marks it closed, the ROM names no switch and drives no output; at 0 the mark clears",
			[address],
		))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-switch-edges-upper-left",
		"The scenario drives public 118 and 117, the Fliptronic positions of an upper left flipper that brGameData does not declare, to 1 "
		"and back to 0 in T.1 SWITCH EDGES. The frames at 1 differ from the frames at 0 only in the switch grid; the frame at 0 equals the "
		"frame before the first write.",
	)
	return _document("switch-edges-upper-left", "br-switch-edges-upper-left", run, observations, command)


def build_solenoids(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "solenoid-test", "br-solenoid-test")
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL, IDENTIFICATION)]
	named = []
	if {item["number"] for item in _step(run, "checkpoint: T.4 pulses solenoid 1")["matched_outputs"]} != {1}:
		raise ValueError("T.4 must pulse solenoid 1 first")
	for index, address in enumerate(T4_ORDER):
		neighbours = {T4_ORDER[index - 1] if index else T4_ORDER[-1], address, T4_ORDER[(index + 1) % len(T4_ORDER)]}
		start = "Enter (start T.4 SOLENOID TEST)"
		window = _window(run, f"T.4 step {index}") | (set() if index else _risen(_step(run, start)) | _matched(run, "checkpoint: T.4 pulses solenoid 1"))
		if address not in window or not window <= neighbours:
			raise ValueError(f"T.4 step {index} pulsed {sorted(window)}, not {address}")
		frame = "T.4 step 14, frame 3" if address == 1 else f"T.4 step {index}, frame 3"
		snapshots.append(_diagnostic(run, frame, f"{T4_NAMES[address]} / T.4 {address:02d} REPEAT / {T4_WIRES[address]}"))
		named.append(_observation(
			f"T.4 SOLENOID TEST selects public {address} ({T4_NAMES[address]}, {T4_WIRES[address]}): the ROM pulses it repeatedly",
			[7] if index else [8], [address],
		))
	# The walk wraps after 15 to 1, skipping 12 and 16.
	if 1 not in _window(run, "T.4 step 14") or {12, 16} & set(_seen(run)):
		raise ValueError("T.4 must wrap to 1 and never pulse 12 or 16")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-solenoid-test",
		"Each Up press selects the next solenoid; in repeat mode the ROM pulses it until the next press. The test cycles fourteen coils "
		"(1-11, 13, 14 and 15), skipping 12 and 16, and then repeats; the selected name blinks, so the frame that shows it is cited.",
	)
	return _document("solenoid-test", "br-solenoid-test", run, observations, command)


def build_flashers(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "flasher-test-names", "br-flasher-test-names")
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL, IDENTIFICATION)]
	if _matched(run, "checkpoint: T.5 pulses flasher 17") != {17}:
		raise ValueError("T.5 must pulse flasher 17 first")
	named = []
	for index, address in enumerate(T5_ORDER):
		neighbours = {address - 1, address, address + 1} | ({28} if address == 17 else set())
		window = _window(run, f"T.5 step {index}") | (set() if index else _risen(_step(run, "Enter (start T.5 FLASHER TEST)")) | _matched(run, "checkpoint: T.5 pulses flasher 17"))
		if address not in window or not window <= neighbours:
			raise ValueError(f"T.5 step {index} pulsed {sorted(window)}, not {address}")
		snapshots.append(_diagnostic(run, T5_FRAMES[address], f"{T5_NAMES[address]} / T.5 {address} REPEAT / {T5_WIRES[address]} RED-WHT"))
		named.append(_observation(
			f"T.5 FLASHER TEST selects public {address} ({T5_NAMES[address]}, {T5_WIRES[address]} RED-WHT): the ROM pulses it repeatedly",
			[7] if index else [8], [address],
		))
	if 17 not in _window(run, "T.5 step 12"):
		raise ValueError("T.5 must wrap to 17")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-flasher-test-names",
		"Each Up press selects the next flasher; in repeat mode the ROM pulses it until the next press. The test walks 17-28 and wraps; "
		"the selected name blinks, so the frame that shows it is cited.",
	)
	return _document("flasher-test-names", "br-flasher-test-names", run, observations, command)


def build_gi(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "gi-test", "br-gi-test")
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL, IDENTIFICATION)]
	if set(_snapshot(run, "T.6 step 7, frame 2")["active_gis"]) != {0, 1, 2, 3, 4}:
		raise ValueError("T.6 must light every string during ALL ILLUMINATION")
	snapshots.append(_diagnostic(run, "T.6 step 7, frame 2", "ALL ILLUMINATION / T.6 BRIGHT=8 STOP"))
	named = []
	for string in range(5):
		for step in range(8 + 8 * string, 16 + 8 * string):
			for frame in (1, 2):
				active = set(_snapshot(run, f"T.6 step {step}, frame {frame}")["active_gis"])
				if active != {string}:
					raise ValueError(f"T.6 step {step} lit {sorted(active)}, not string {string}")
		label = f"T.6 step {8 + 8 * string}, frame 2"
		snapshots.append(_diagnostic(run, label, f"{GI_NAMES[string]} / T.6 BRIGHT=1 STOP / {GI_WIRES[string]}"))
		named.append(_observation(
			f"T.6 GENERAL ILLUMINATION lights public GI {string} alone at brightness 1 to 8 and names it {GI_NAMES[string]} ({GI_WIRES[string]})",
			[7],
		))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-gi-test",
		"In stop mode each Up press advances the test: ALL ILLUMINATION at brightness 1 to 8, then each circuit alone at brightness 1 to 8. "
		"Every frame taken while a circuit is shown has exactly that public GI string active.",
	)
	return _document("gi-test", "br-gi-test", run, observations, command)


def build_lamps(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "single-lamps", "br-single-lamps")
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL, IDENTIFICATION)]
	named = []
	for index, address in enumerate(LAMP_ORDER):
		first = "Enter (start T.8 SINGLE LAMPS)" if index == 0 else f"T.8 step {index}"
		labels = [first] + [f"T.8 step {index}, frame {frame}" for frame in (1, 2)]
		# The lamp blinks: every snapshot of the step shows it or nothing, and it rises in the frames after the pulse
		# when no snapshot caught it lit. The pulse's own window can still carry the previous lamp going dark.
		shown = set().union(*(set(_snapshot(run, label)["active_lamps"]) for label in labels))
		frames = set().union(*(_risen(_step(run, label), "lamps") for label in labels[1:]))
		lit = shown | frames
		if lit != {address}:
			raise ValueError(f"T.8 step {index} lit {sorted(lit)}, not {address}")
		best = max(labels, key=lambda label: _snapshot(run, label)["displays"][0]["nonzero_pixels"])
		column, row = divmod(address, 10)
		text = f"{T8_NAMES[address]} / T.8 {index + 1:02d} LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"
		snapshots.append(_diagnostic(run, best, text))
		named.append(_observation(f"T.8 SINGLE LAMPS lights public lamp {address} alone and names it {T8_NAMES[address]}", [7] if index else [8]))
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-single-lamps",
		"Each Up press selects the next lamp in matrix order 11-88; the selected lamp blinks, so the union of the lamps active in the step's "
		"snapshot and its two frames is exactly that lamp, and the cited frame is the step's frame with the most lit pixels.",
	)
	return _document("single-lamps", "br-single-lamps", run, observations, command)


def build_flippers(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "flipper-coil-test", "br-flipper-coil-test")
	snapshots = [_diagnostic(run, IDENTIFICATION_LABEL, IDENTIFICATION)]
	named = []
	for index, address in enumerate(T12_ORDER):
		risen = _risen(_step(run, "checkpoint: T.12 pulses solenoid 45")) if index == 0 else _risen(_step(run, f"T.12 step {index}"))
		if risen != T12_PUBLISHED[address]:
			raise ValueError(f"T.12 step {index} published {sorted(risen)}, not {sorted(T12_PUBLISHED[address])}")
		snapshots.append(_diagnostic(run, T12_FRAMES[address], f"{T12_NAMES[address]} / T.12 {index + 1:02d} REPEAT / {T12_WIRES[address]}"))
		named.append(_observation(
			f"T.12 FLIPPER COIL TEST selects {T12_NAMES[address]} ({T12_WIRES[address]}): PinMAME publishes {'/'.join(map(str, sorted(T12_PUBLISHED[address])))}",
			[7] if index else [8], sorted(T12_PUBLISHED[address]),
		))
	if {35, 36} & set(_seen(run)) or _risen(_step(run, "T.12 step 6")) != {45, 46}:
		raise ValueError("T.12 must never drive 35/36 and must wrap to the right flipper")
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-flipper-coil-test",
		"T.12 FLIPPER COIL TEST is the L-4 ROM's twelfth test (the manual's list predates it). Each Up press selects the next winding of the "
		"lower right, lower left and upper right flippers and the ROM pulses it until the next press; it walks six windings and wraps, and "
		"never drives an upper left flipper.",
	)
	return _document("flipper-coil-test", "br-flipper-coil-test", run, observations, command)


def build_cannon(review_root: Path) -> dict[str, Any]:
	run = _load_run(review_root, "cannon-test", "br-cannon-test")
	snapshots = [_diagnostic(run, label, text) for label, text in CANNON_READINGS.items()]
	if _risen(_step(run, "35 -> 1")) != {8} or _window(run, "T.14 started"):
		raise ValueError("T.14 must fire the cannon kicker (8) when 35 closes, and nothing before")
	if _risen(_step(run, "Enter (toggle the cannon motor)")) != {3}:
		raise ValueError("the first T.14 toggle must start the cannon motor (3)")
	# The second toggle must stop it: public 3 falls during that step and stays off in every frame after it.
	stop = [item["states"] for item in _step(run, "Enter (toggle the cannon motor again)")["transitions"]["solenoids"] if item["number"] == 3]
	if not stop or stop[0][-1] != 0 or any(stop[0]):
		raise ValueError("the second T.14 toggle must turn the cannon motor (3) off")
	for frame in (1, 2, 3):
		if 3 in _snapshot(run, f"T.14 after the second toggle, frame {frame}")["active_solenoids"]:
			raise ValueError("the cannon motor (3) must stay off after the second toggle")
	if 3 not in _snapshot(run, "T.14 after the first toggle, frame 3")["active_solenoids"]:
		raise ValueError("the cannon motor (3) must be on after the first toggle")
	named = [
		_observation("T.14 CANNON TEST shows SW.35 CANNON = CLOSED while host public 35 is 1 and OPEN at 0, and fires the cannon kicker (8) on the closure", [35], [8]),
		_observation("T.14 CANNON TEST: Enter toggles the cannon motor; MOTOR = ON drives public 3 and the second toggle stops it", [8], [3]),
	]
	observations = {"diagnostic_snapshots": snapshots, "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = _command(
		"br-cannon-test",
		"T.14 CANNON TEST is the L-4 ROM's fourteenth test (its own screen still prints T.12, the number the manual gives it). It shows the "
		"cannon kicker switch state and the motor state; with built-in mechanisms disabled no ball is in the cannon or the lockup.",
	)
	return _document("cannon-test", "br-cannon-test", run, observations, command)


BUILDERS = {
	"black-rose-br_l4-switch-edges.json": ("switch-edges", build_edges),
	"black-rose-br_l4-switch-edges-upper-left.json": ("switch-edges-upper-left", build_upper_left),
	"black-rose-br_l4-solenoid-test.json": ("solenoid-test", build_solenoids),
	"black-rose-br_l4-flasher-test-names.json": ("flasher-test-names", build_flashers),
	"black-rose-br_l4-gi-test.json": ("gi-test", build_gi),
	"black-rose-br_l4-single-lamps.json": ("single-lamps", build_lamps),
	"black-rose-br_l4-flipper-coil-test.json": ("flipper-coil-test", build_flippers),
	"black-rose-br_l4-cannon-test.json": ("cannon-test", build_cannon),
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	pins = json.loads(FRAME_READINGS_PATH.read_bytes())["runs"]
	if set(pins) != {directory for directory, _ in BUILDERS.values()}:
		raise ValueError("the frame readings must cover exactly the documented runs")
	for filename, (directory, builder) in BUILDERS.items():
		document = builder(review_root)
		cited = {item["label"] for item in document["runtime"]["observations"]["diagnostic_snapshots"]}
		if cited != set(pins[directory]):
			raise ValueError(f"{directory}: the cited frames differ from the pinned readings: {sorted(set(pins[directory]) ^ cited)}")
		run_directory = review_root / HARNESS_DIRECTORY / directory / GAME
		run_sha = _sha256(run_directory / "run.json")
		manifest_sha = _sha256(run_directory / "manifest.json")
		document["runtime"]["raw_runs"][0]["sha256"] = run_sha
		document["source"]["sha256"] = run_sha
		document["source"]["attribution"] += f" Exact external directory manifest {GAME}/manifest.json SHA-256 {manifest_sha}."
		documents[filename] = document
	return documents


def write(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		write_json(EVIDENCE_DIRECTORY / filename, document)


def check(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		path = EVIDENCE_DIRECTORY / filename
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise ValueError(f"Black Rose compact runtime evidence drift: {path}")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--review-root", type=Path, default=None)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true")
	mode.add_argument("--write", action="store_true")
	args = parser.parse_args()
	root = args.review_root or (Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT") else None)
	if root is None:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT or --review-root is required")
	if args.write:
		write(root)
	else:
		check(root)
		print("Black Rose compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
