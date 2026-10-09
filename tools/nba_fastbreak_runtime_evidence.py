"""Derive the compact NBA Fastbreak runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism mask, and writes the derived
observations beside the other WPC-95 runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's visual
reading of that snapshot's retained DMD frame, pinned by its pixel SHA-256; readings of one text must come from identical
frames. The tool refuses a raw run whose transitions no longer support a stated observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

from pinmame_game_defs.jsonio import canonical_bytes, write_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.nba-fastbreak.1997"
GAME = "nbaf_31"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "d5fd2c89752419a77d84965ac4cbe05d42d5c373337241cc0265b403e3bfc2fa"
HARNESS_DIRECTORY = "nba-fastbreak-1997/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-95"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-95"
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
IDENTIFICATION = "NBA FASTBREAK / 50053 REV. 3.1"
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game nbaf_31 --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics {mech} --scenario {scenario} --dmd-dir <external-dmd-dir> --output <external-run.json>. "
)

# --- T.1 SWITCH EDGES sweep ----------------------------------------------------------------------------
# The name the ROM prints on the top display line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	11: "BALL LAUNCH", 12: "BACKBOX BASKET", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "SHOOTER LANE", 16: "LT. RETURN LANE",
	17: "RT. RETURN LANE", 18: "L. R. STANDUP", 21: "SLAM TILT", 22: "COIN DOOR CLOSED", 23: "RIGHT JET", 24: "ALWAYS CLOSED",
	25: "EJECT HOLE", 26: "LEFT OUT LANE", 27: "RIGHT OUTLANE", 28: "U. R. STANDUP", 31: "TROUGH EJECT", 32: "TROUGH BALL 1",
	33: "TROUGH BALL 2", 34: "TROUGH BALL 3", 35: "TROUGH BALL 4", 36: "CENTER RAMP OPTO", 37: "R. LOOP ENT. OPTO",
	38: "RIGHT LOOP EXIT", 41: "STANDUP '3'", 42: "STANDUP 'P'", 43: "STANDUP 'T'", 44: "RIGHT RAMP ENTER", 45: "LEFT RAMP ENTER",
	46: "LEFT RAMP MADE", 47: "LEFT LOOP ENTER", 48: "LEFT LOOP MADE", 51: "DEFENDER POS. 4", 52: "DEFENDER POS. 3",
	53: "DEFEND. LOCK POS", 54: "DEFENDER POS. 2", 55: "DEFENDER POS. 1", 56: "JETS BALL DRAIN", 57: "L. SLINGSHOT",
	58: "R. SLINGSHOT", 61: "LEFT JET", 62: "MIDDLE JET", 63: "L. LOOP RAMP EXIT", 64: "RIGHT RAMP MADE", 65: '"IN THE PAINT" 4',
	66: '"IN THE PAINT" 3', 67: '"IN THE PAINT" 2', 68: '"IN THE PAINT" 1',
}
# The wire colours the ROM prints for a matrix switch: row wire first, then the column wire. The ROM prints GRN-WHT for
# column 4, where the manual's switch matrix prints Green-Yellow.
EDGE_ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
EDGE_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "WHT", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# Fliptronic column: printed position, wire, and the name the ROM shows while the host holds the address at 1.
FLIPPER_EDGES = {
	111: ("F1", "BLK-GRN ORN", None), 112: ("F1", "BLK-GRN ORN", "R. FLIPPER EOS."), 113: ("F3", "BLK-BLU ORN", None),
	114: ("F3", "BLK-BLU ORN", "L. FLIPPER EOS."), 115: ("F5", "BLK-VIO ORN", "BASKET MADE"), 116: ("F1", "BLK-GRN ORN", "R. FLIPPER EOS."),
	117: ("F7", "BLK-GRY ORN", "BASKET HOLD"), 118: ("F3", "BLK-BLU ORN", "L. FLIPPER EOS."),
}
SWEPT = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9)) + tuple(range(111, 119))
# Fliptronic button positions whose closure makes the ROM fire a lower flipper (power and hold windings).
FLIPPER_FIRES = {112: {45, 46}, 114: {47, 48}, 116: {45, 46}, 118: {47, 48}}
# Playfield switches whose closure makes the ROM fire their own coil even inside T.1 (jet bumpers and slingshots).
SWITCH_FIRES = {23: (14, "right jet bumper"), 57: (10, "left slingshot"), 58: (11, "right slingshot"), 61: (12, "left jet bumper"), 62: (13, "middle jet bumper")}
PINMAME_MASKED = (31, 32, 33, 34, 35, 36, 37, 115)


def _matrix_wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{EDGE_ROW_WIRES[row]} GRN-{EDGE_COLUMN_WIRES[column]}"


def _edge_reading(address: int, level: int) -> str:
	idle = "SWITCH EDGES"
	if address in FLIPPER_EDGES:
		position, wires, name = FLIPPER_EDGES[address]
		return f"{name if level and name else idle} / T.1 LAST SW {position} / {wires}"
	if address >= 71:
		return f"{idle} / T.1 LAST SW 68 / {_matrix_wires(68)}"
	if address == 24:
		# 24 rests at public 1 from power-up; the ROM names it on the 1 -> 0 edge and shows nothing new for the redundant 1.
		return f"{EDGE_NAMES[24]} / T.1 LAST SW 24 / {_matrix_wires(24)}" if level == 0 else f"{idle} / T.1 LAST SW 23 / {_matrix_wires(23)}"
	return f"{EDGE_NAMES[address] if level else idle} / T.1 LAST SW {address} / {_matrix_wires(address)}"


# --- T.4 SOLENOID TEST, T.5 FLASHER TEST, T.12 FLIPPER COIL TEST ---------------------------------------
T4_ORDER = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 25, 26, 27, 28, 33, 34, 35, 36, 37, 38, 39, 40, 41)
T4_NAMES = {
	1: ("AUTOPLUNGER", "VIO-BRN RED-BRN"), 3: ("L. RAMP DIVERTER", "VIO-ORN RED-BRN"), 4: ("R. LOOP DIVERTER", "VIO-YEL RED-BRN"),
	5: ("EJECT", "VIO-GRN RED-BRN"), 6: ("LOOP GATE", "VIO-BLU RED-BRN"), 7: ("BACKBOX FLIPPER", "VIO-BLK RED-BRN"),
	8: ("BALL CATCH MAG.", "VIO-GRY RED-BRN"), 9: ("TROUGH EJECT", "BRN-BLK RED-BLK"), 10: ("LEFT SLING", "BRN-RED RED-BLK"),
	11: ("RIGHT SLING", "BRN-ORN RED-BLK"), 12: ("LEFT JET", "BRN-YEL RED-BLK"), 13: ("MIDDLE JET", "BRN-GRN RED-BLK"),
	14: ("RIGHT JET", "BRN-BLU RED-BLK"), 15: ("PASS RIGHT 2", "BRN-VIO RED-BLK"), 16: ("PASS LEFT 2", "BRN-GRY RED-BLK"),
	25: ("PASS RIGHT 1", "BLU-BRN RED-ORN"), 26: ("PASS LEFT 3", "BLU-RED RED-ORN"), 27: ("PASS RIGHT 3", "BLU-ORN RED-ORN"),
	28: ("PASS LEFT 4", "BLU-YEL RED-ORN"), 33: ("SHOOT 1", "YEL-VIO RED-VIO"), 34: ("SHOOT 2", "ORN-VIO RED-VIO"),
	35: ("SHOOT 3", "YEL-GRY RED-GRY"), 36: ("SHOOT 4", "ORN-GRY RED-GRY"), 37: ("MOTOR ENABLE", "BRN-WHT GRY-YEL"),
	38: ("MOTOR DIRECTION", "ORN-WHT GRY-YEL"), 39: ("SHOT CLK ENABLE", "YEL-WHT GRY-YEL"), 40: ("SHOT CLK COUNT", "GRN-WHT GRY-YEL"),
	41: ("COIN METER", "BLK-WHT GRY-YEL"),
}
# Public addresses PinMAME publishes for each T.4 selection (the WPC-95 37-40 outputs are mirrored at 41-44); the ROM's
# 41 COIN METER selection publishes nothing.
T4_PUBLISHED = {address: {address} for address in T4_ORDER}
T4_PUBLISHED.update({37: {37, 41}, 38: {38, 42}, 39: {39, 43}, 40: {40, 44}, 41: set()})
T5_ORDER = (17, 18, 19, 20, 22, 24)
T5_NAMES = {
	17: ("EJECT KICKOUT", "BLK-BRN RED-WHT"), 18: ("LEFT JET BUMPER", "BLK-RED RED-WHT"), 19: ("UPPER LEFT", "BLK-ORN RED-WHT"),
	20: ("UPPER RIGHT", "BLK-YEL RED-WHT"), 22: ("TROPHY INSERT", "BLU-BLK RED-WHT"), 24: ("LOWER LEFT/RIGHT", "BLU-GRY RED-WHT"),
}
T12_ORDER = ((1, "R. FLIP. POWER", "YEL-GRN RED-GRN", {45, 46}), (2, "R. FLIP. HOLD", "ORN-GRN RED-GRN", {46}),
	(3, "L. FLIP. POWER", "YEL-BLU RED-BLU", {47, 48}), (4, "L. FLIP. HOLD", "ORN-BLU RED-BLU", {48}))
# T.6: the step whose frame names each string, its printed wires, the public GI channel the following steps dim alone.
GI_STRINGS = ((8, 1, "BRIGHT=1", "WHT-BRN BRN", 0), (16, 2, "BRIGHT=1", "WHT-ORN ORN", 1), (24, 3, "BRIGHT=1", "WHT-YEL YEL", 2),
	(32, 4, "ON ONLY", "WHT-GRN GRN", 3), (33, 5, "ON ONLY", "WHT-VIO VIO", 4))
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMPS = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))


# --- Shared helpers ------------------------------------------------------------------------------------
def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path, scenario: str, mechanics: int) -> dict[str, Any]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{scenario}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful NBA Fastbreak {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != mechanics:
		raise ValueError(f"unexpected built-in mechanism mask in {run_path}")
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
	"""Addresses whose recorded transitions during the step include an active state."""
	return {item["number"] for item in step["transitions"][channel] if any(item["states"])}


def _changed(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"][channel]}


def _diagnostics(run: dict[str, Any], readings: dict[str, str], grid_marked: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
	"""Pin each reading to its frame; one interpreted text must always come from one frame.

	``grid_marked`` names T.1 frames taken while a switch is held: the switch grid on the left of the display marks that raw cell,
	so frames whose top-line text agrees may still differ there, and they are exempt from the one-text-one-frame rule.
	"""
	result = []
	by_text: dict[str, str] = {}
	for label, text in readings.items():
		snapshot = _snapshot(run, label)
		displays = [item for item in snapshot["displays"] if item["index"] == 0]
		if len(displays) != 1:
			raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
		pixel = displays[0]["pixel_sha256"]
		if label not in grid_marked and by_text.setdefault(text, pixel) != pixel:
			raise ValueError(f"the reading {text!r} is pinned to two different frames (at {label!r})")
		result.append({
			"active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
			"display_index": 0,
			"interpreted_text": text,
			"label": label,
			"nonzero_pixels": displays[0]["nonzero_pixels"],
			"pixel_sha256": pixel,
		})
	return result


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _observation(label: str, inputs: list[int], solenoids: set[int] | list[int], *, active: list[int] | None = None) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": active or [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": sorted(solenoids),
	}


def _document(name: str, directory: str, scenario: str, mechanics: int, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/nba_fastbreak_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": COMMAND.format(mech=mechanics, scenario=f"{SCENARIO_DIRECTORY}/{scenario}.json") + command,
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"game": GAME,
			"observations": observations,
			"raw_runs": [
				{
					"action_count": run["scenario"]["action_count"],
					"initial_switches": run["initial_switches"],
					"name": name,
					"nvram_initialization": NVRAM_NOTE,
					"retained_from": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}/run.json",
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
			"path": f"external:pinmame-review-artifacts/{HARNESS_DIRECTORY}/{directory}",
			"quality": "validated",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
		},
		"states": [],
		"switches": [],
		"version": 1,
	}


# --- Builders ------------------------------------------------------------------------------------------
def build_edges(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	named = []
	for address in SWEPT:
		for level in (1, 0):
			readings[f"{address} -> {level}"] = _edge_reading(address, level)
		held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> 1")["watched_switches"]}
		if held[address] != (0 if address in (111, 113) else 1):
			raise ValueError(f"unexpected observed level of {address} after the host wrote 1")
		risen = _risen(_step(run, f"{address} -> 1"))
		expected = FLIPPER_FIRES.get(address) or ({SWITCH_FIRES[address][0]} if address in SWITCH_FIRES else set())
		if risen != expected:
			raise ValueError(f"T.1 at public {address} published {sorted(risen)}, expected {sorted(expected)}")
		if address in FLIPPER_FIRES:
			named.append(_observation(
				f"T.1 with host public {address} set to 1: the ROM fires the lower {'right' if address in (112, 116) else 'left'} flipper "
				f"(power and hold) and names {FLIPPER_EDGES[address][2]!r}; the hold winding drops at 0", [address], risen))
		elif address in SWITCH_FIRES:
			named.append(_observation(
				f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and the ROM fires the {SWITCH_FIRES[address][1]} coil, "
				f"public {SWITCH_FIRES[address][0]}, on the closure", [address], risen))
		elif address in EDGE_NAMES and address != 24:
			named.append(_observation(f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and clears it at 0", [address], set()))
		elif address in (115, 117):
			named.append(_observation(f"T.1 names {FLIPPER_EDGES[address][2]!r} ({FLIPPER_EDGES[address][0]}) while host public {address} is 1 and clears it at 0", [address], set()))
	named.append(_observation("Public 24 rests at 1 from power-up; T.1 shows no new name for the redundant 1 and names 'ALWAYS CLOSED' on the 1 -> 0 edge", [24], set()))
	named.append(_observation("Public 71-88 at either level: T.1 names nothing and keeps showing the last named switch, 68", [71], set()))
	named.append(_observation("Public 111 and 113: a host write of 1 reads back 0 and T.1 names nothing, because PinMAME rewrites the end-of-stroke bits from the flipper coil state on every update", [111, 113], set()))
	observations = {
		"diagnostic_snapshots": _diagnostics(run, readings, frozenset(f"{address} -> 1" for address in SWEPT)),
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = (
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 2 s; the snapshot after it records the ROM's T.1 "
		"display and the watched public switch levels. The ROM names a switch on its top line while it reads the switch as active. "
		f"PinMAME's nbafGameData mask inverts public {', '.join(map(str, PINMAME_MASKED))}; every one of them is still named at public 1."
	)
	return observations, command


def build_solenoids(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	named = []
	for index, address in enumerate(T4_ORDER):
		label = "Enter (start T.4 SOLENOID TEST)" if index == 0 else f"T.4 step {index}"
		name, wires = T4_NAMES[address]
		if address != 25:
			readings[label] = f"{name} / T.4 {address:02d} REPEAT / {wires}"
		risen = _risen(_step(run, label))
		if risen != T4_PUBLISHED[address]:
			raise ValueError(f"T.4 step {index} ({address}) published {sorted(risen)}, not {sorted(T4_PUBLISHED[address])}")
		named.append(_observation(
			f"T.4 SOLENOID TEST selects {address:02d} ({name}, {wires})" + (": PinMAME publishes no output for it" if address == 41 else ": the ROM pulses it repeatedly"),
			[8 if index == 0 else 7], risen))
	if _risen(_step(run, f"T.4 step {len(T4_ORDER)}")) != {1}:
		raise ValueError("T.4 must wrap to solenoid 1 after 41")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"Each Up press selects the next T.4 item; in repeat mode the ROM pulses it until the next press. The test walks 1, 3-16, 25-28, "
		"33-41 and wraps to 1; it skips 2 and offers 41 COIN METER, for which PinMAME publishes nothing. 37-40 are mirrored at 41-44 by "
		"core_getSol. Solenoid 25's name was dark in both of this run's frames and is read from the blinked-names run."
	)
	return observations, command


def build_blinked(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {
		"Enter 2 (game identification)": IDENTIFICATION,
		"T.4 at solenoid 25, frame 3": "PASS RIGHT 1 / T.4 25 REPEAT / BLU-BRN RED-ORN",
		"T.5 at flasher 24, frame 3": "LOWER LEFT/RIGHT / T.5 24 REPEAT / BLU-GRY RED-WHT",
	}
	# T.4's 1 s steps are shorter than its pulse period, so the 25 pulse lands in the checkpoint that waits for it.
	if _risen(_step(run, "checkpoint: T.4 step 15 pulses solenoid 25")) != {25} or _risen(_step(run, "T.5 step 5")) != {24}:
		raise ValueError("the blinked-names run must pulse 25 in T.4 and 24 in T.5")
	named = [
		_observation("T.4 SOLENOID TEST at its fifteenth item pulses public 25 and names it PASS RIGHT 1 (BLU-BRN RED-ORN)", [7], {25}),
		_observation("T.5 FLASHER TEST at its sixth item pulses public 24 and names it LOWER LEFT/RIGHT (BLU-GRY RED-WHT)", [7], {24}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Eight frames 0.25 s apart at each item catch the blinking name in its lit phase."


def build_flashers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	named = []
	for index, address in enumerate(T5_ORDER):
		label = "Enter (start T.5 FLASHER TEST)" if index == 0 else f"T.5 step {index}"
		name, wires = T5_NAMES[address]
		if address not in (17, 24):
			readings[label] = f"{name} / T.5 {address} REPEAT / {wires}"
		risen = _risen(_step(run, label))
		if risen != {address}:
			raise ValueError(f"T.5 step {index} published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.5 FLASHER TEST selects {address} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 0 else 7], risen))
	readings["T.5 step 0, second frame"] = f"{T5_NAMES[17][0]} / T.5 17 REPEAT / {T5_NAMES[17][1]}"
	if _risen(_step(run, "T.5 step 6")) != {17}:
		raise ValueError("T.5 must wrap to 17 after 24")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next flasher; the test walks 17, 18, 19, 20, 22 and 24 and wraps to 17. Flasher 24's name is read from the blinked-names run."


def build_flippers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	named = []
	for index, (number, name, wires, published) in enumerate(T12_ORDER):
		label = "Enter (start T.12 FLIPPER COIL TEST)" if index == 0 else f"T.12 step {index}"
		readings[label] = f"{name} / T.12 {number:02d} REPEAT / {wires}"
		risen = _risen(_step(run, label))
		if risen != published:
			raise ValueError(f"T.12 item {number} published {sorted(risen)}, not {sorted(published)}")
		named.append(_observation(f"T.12 FLIPPER COIL TEST item {number:02d} {name} ({wires}) drives public {', '.join(map(str, sorted(published)))}", [8 if index == 0 else 7], risen))
	if _risen(_step(run, "T.12 step 4")) != {45, 46}:
		raise ValueError("T.12 must wrap to the right flipper power item")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The test walks only the four lower-flipper items (power drives both windings, hold the hold winding) and wraps; it offers no item for 33-36."


def build_gi(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	named = []
	for step, string, mode, wires, channel in GI_STRINGS:
		readings[f"T.6 step {step}"] = f"STRING {string} / T.6 {mode} STOP / {wires}"
		if mode == "BRIGHT=1":
			following = [_changed(_step(run, f"T.6 step {step + offset}"), "gis") for offset in range(1, 6)]
			if any(item != {channel} for item in following):
				raise ValueError(f"T.6 string {string} must dim public GI {channel} alone, saw {following}")
			named.append(_observation(f"T.6 STRING {string} ({wires}): the next Up presses step the brightness of public GI {channel} alone", [7], set()))
		else:
			named.append(_observation(f"T.6 STRING {string} ({wires}) is printed ON ONLY and steps no brightness", [7], set()))
	for snapshot in run["snapshots"]:
		if not {3, 4} <= set(snapshot["active_gis"]):
			raise ValueError(f"public GI 3 and 4 must stay on throughout, not at {snapshot['label']!r}")
	if any({3, 4} & _changed(step, "gis") for step in run["steps"] if "transitions" in step):
		raise ValueError("public GI 3 and 4 must never change")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "T.6 stop mode first steps all illumination through eight brightness levels, then each dimmable string; public GI 3 and 4 stay on in every snapshot."


def build_lamps(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION}
	for index, address in enumerate(LAMPS):
		label = "T.8 started" if index == 0 else f"T.8 step {index}"
		column, row = divmod(address, 10)
		readings[label] = f"T.8. LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"
		lit = _snapshot(run, label)["active_lamps"]
		if address not in _risen(_step(run, label), "lamps") and address not in lit:
			raise ValueError(f"T.8 step {index} did not light public lamp {address}")
	named = [_observation("T.8 SINGLE LAMPS TEST lights public lamps 11-88 one at a time in matrix order while printing each number and its row and column wires", [7], set())]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next lamp; the name line blinks, the number and wire lines do not."


MOTOR_READINGS = {
	"Enter (start T.16 MOTOR TEST)": "MOTOR TEST / POS 1 POS 2 LOCK POS 3 POS 4, none marked / SELF TEST",
	"T.16 self-test, frame 3": "MOTOR TEST / POS 4 marked / SELF TEST",
	"T.16 item 2 selected, frame 2": "MOTOR TEST / POS 4 marked / MOVE LEFT",
	"T.16 item 2 running, frame 2": "MOTOR TEST / POS 3 marked / MOVE LEFT",
	"T.16 item 3 selected, frame 2": "MOTOR TEST / POS 3 marked / MOVE RIGHT",
	"T.16 item 3 running, frame 2": "MOTOR TEST / POS 4 marked / MOVE RIGHT",
	"T.16 item 4 selected, frame 2": "MOTOR TEST / CYCLES: 0 / AUTO RUN",
	"T.16 item 4 running, frame 6": "MOTOR TEST / CYCLES: 1 / AUTO RUN",
}


def build_motor(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 1 (game identification)": IDENTIFICATION, **MOTOR_READINGS}
	left = _risen(_step(run, "Enter (run T.16 item 2)"))
	right = _risen(_step(run, "Enter (run T.16 item 3)"))
	if left != {37, 41} or right != {37, 38, 41, 42}:
		raise ValueError(f"MOVE LEFT must drive 37 alone and MOVE RIGHT 37 with 38: {sorted(left)}, {sorted(right)}")
	if not {39, 40} <= _risen(_step(run, "T.16 self-test, frame 9")):
		raise ValueError("the shot clock outputs must pulse during T.16")
	digits = [tuple(item["segments"]) for snapshot in run["snapshots"] for item in snapshot["displays"] if item["index"] == 1]
	if (91, 79) not in digits or (6, 6) not in digits:
		raise ValueError("the shot clock display must show 23 and 11 during T.16")
	named = [
		_observation("T.16 self-test runs the defender to POS 4 with the motor (37) and direction (38) outputs, mirrored at 41 and 42", [8], _risen(_step(run, "Enter (start T.16 MOTOR TEST)")) & {37, 38, 41, 42}),
		_observation("T.16 MOVE LEFT drives the motor enable 37 alone (mirror 41) and the marked position moves from POS 4 to POS 3", [8], left),
		_observation("T.16 MOVE RIGHT drives 37 with the direction line 38 (mirrors 41, 42) and the marked position moves from POS 3 back to POS 4", [8], right),
		_observation("During T.16 the ROM pulses the shot clock enable (39) and count (40) lines; PinMAME's nbaf.c turns them into the two-digit display 1, which counts down (23, 22, ... 11, ...)", [8], {39, 40}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"PinMAME's built-in defender mechanism (mech slot 0, handle-mechanics 1) answers the motor outputs with the position switches "
		"51-55, so the run shows the ROM's own contract with that model: which outputs it drives for each named move and which position "
		"the model then reports. It is a synthetic probe, not a measurement of the physical defender."
	)
	return observations, command


BACKBOX_READINGS = {
	"T.17 started": "BACKBOX TEST / BACKBOX [ ] SHOOT [ ] / (CLOSE COIN DOOR, dark phase)",
	"Enter (start T.17 BACKBOX TEST)": "BACKBOX TEST / BACKBOX [ ] SHOOT [ ] / CLOSE COIN DOOR",
	"Shoot button 11 press 1, coin door open (held)": "BACKBOX TEST / BACKBOX [ ] SHOOT [x] / CLOSE COIN DOOR",
	"12 -> 1": "BACKBOX TEST / BACKBOX [x] SHOOT [ ] / CLOSE COIN DOOR",
	"Shoot button 11 press 1, coin door closed (held)": "BACKBOX TEST / BACKBOX [ ] SHOOT [ ] / PRESS 'SHOOT' BUTTON",
	"Shoot button 11 press 2, coin door closed (held)": "BACKBOX TEST / BACKBOX [ ] SHOOT [x] / PRESS 'SHOOT' BUTTON",
}


def build_backbox(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {"Enter 2 (game identification)": IDENTIFICATION, **BACKBOX_READINGS}
	for label in ("Shoot button 11 press 1, coin door open", "Shoot button 11 press 2, coin door open",
			"Shoot button 11 press 1, coin door closed", "Shoot button 11 press 2, coin door closed"):
		if _risen(_step(run, label)) != {7}:
			raise ValueError(f"T.17 must fire solenoid 7 for {label!r}")
	for address in (112, 114, 116, 118):
		if _risen(_step(run, f"{address} press")):
			raise ValueError(f"T.17 must not fire anything for {address}")
	named = [
		_observation("T.17 BACKBOX TEST: each press of public 11 (the Shoot button) fires solenoid 7, the backbox flipper, with the coin door open or closed", [11], {7}),
		_observation("T.17 marks BACKBOX while host public 12 is 1", [12], set()),
		_observation("T.17 fires nothing for the Fliptronic button addresses 112, 114, 116 and 118", [112, 114, 116, 118], set()),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The SHOOT and BACKBOX boxes are filled while the ROM reads public 11 and 12 as closed; with the coin door closed the prompt changes to PRESS 'SHOOT' BUTTON."


Builder = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]
RUNS: dict[str, tuple[str, str, int, Builder]] = {
	"nba-fastbreak-nbaf_31-switch-edges-sweep.json": ("switch-edges-sweep", "nbaf-switch-edges-sweep", 0, build_edges),
	"nba-fastbreak-nbaf_31-solenoid-test.json": ("solenoid-test", "nbaf-solenoid-test", 0, build_solenoids),
	"nba-fastbreak-nbaf_31-blinked-names.json": ("blinked-names", "nbaf-blinked-names", 0, build_blinked),
	"nba-fastbreak-nbaf_31-flasher-test-sweep.json": ("flasher-test-sweep", "nbaf-flasher-test-sweep", 0, build_flashers),
	"nba-fastbreak-nbaf_31-flipper-coil-test.json": ("flipper-coil-test", "nbaf-flipper-coil-test", 0, build_flippers),
	"nba-fastbreak-nbaf_31-gi-test.json": ("gi-test-full", "nbaf-gi-test", 0, build_gi),
	"nba-fastbreak-nbaf_31-single-lamps.json": ("single-lamps", "nbaf-single-lamps", 0, build_lamps),
	"nba-fastbreak-nbaf_31-motor-test.json": ("motor-test", "nbaf-motor-test", 1, build_motor),
	"nba-fastbreak-nbaf_31-backbox-test.json": ("backbox-test", "nbaf-backbox-test", 0, build_backbox),
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, (directory, scenario, mechanics, builder) in RUNS.items():
		path = review_root / HARNESS_DIRECTORY / directory
		run = _load_run(path, scenario, mechanics)
		observations, command = builder(run)
		document = _document(filename.removeprefix("nba-fastbreak-").removesuffix(".json"), directory, scenario, mechanics, run, observations, command)
		run_sha = _sha256(path / "run.json")
		manifest_sha = _sha256(path / "manifest.json")
		document["runtime"]["raw_runs"][0]["sha256"] = run_sha
		document["source"]["sha256"] = run_sha
		document["source"]["attribution"] += f" Exact external directory manifest {directory}/manifest.json SHA-256 {manifest_sha}."
		documents[filename] = document
	return documents


def write(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		write_json(EVIDENCE_DIRECTORY / filename, document)


def check(review_root: Path) -> None:
	for filename, document in build(review_root).items():
		path = EVIDENCE_DIRECTORY / filename
		if not path.is_file() or path.read_bytes() != canonical_bytes(document):
			raise ValueError(f"NBA Fastbreak compact runtime evidence drift: {path}")


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
		print("NBA Fastbreak compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
