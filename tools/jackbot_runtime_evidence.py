"""Derive the compact Jack*Bot runtime evidence from the retained raw harness runs.

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
MACHINE_ID = "williams.jackbot.1995"
GAME = "jb_10r"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "182acb5047d5ccfd0a795a8c705d375856a4ae7fd134bf9595523f323b8a4238"
HARNESS_DIRECTORY = "jackbot-1995/harness"
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
IDENTIFICATION = "JACK•BOT / 50051 REV. 1.0 R"
IDENTIFICATION_LABEL = "Enter 1 (game identification)"
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game jb_10r --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics 0 --scenario {scenario} --dmd-dir <external-dmd-dir> --output <external-run.json>. "
)

# --- T.1 SWITCH EDGES sweep ----------------------------------------------------------------------------
# The name the ROM prints on the top display line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	11: "L. LEFT 10 POINT", 12: "U. LEFT 10 POINT", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "RAMP IS DOWN",
	16: "HIGH DROP TARGET", 17: "CENT. DROP TARGET", 18: "LOW DROP TARGET", 21: "SLAM TILT", 22: "COIN DOOR CLOSED",
	23: "BUY EXTRA BALL", 25: "LEFT OUTLANE", 26: "L. FLIPPER LANE", 27: "R. FLIPPER LANE", 28: "RIGHT OUTLANE", 31: "TROUGH JAM",
	32: "TROUGH 1 (RIGHT)", 33: "TROUGH 2", 34: "TROUGH 3", 35: "TROUGH 4 (LEFT)", 36: "RAMP EXIT", 37: "RAMP ENTRANCE",
	38: "TARG. UNDER RAMP", 41: "VISOR 1 (LEFT)", 42: "VISOR 2", 43: "VISOR 3", 44: "VISOR 4", 45: "VISOR 5 (RIGHT)",
	46: "GAME SAUCER", 47: "LEFT EJECT HOLE", 48: "RIGHT EJECT HOLE", 51: "5-BANK 1 (UPPER)", 52: "5-BANK TARGET 2",
	53: "5-BANK TARGET 3", 54: "5-BANK TARGET 4", 55: "5-BANK 5 (LOWER)", 56: "VORTEX UPPER", 57: "VORTEX CENTER",
	58: "VORTEX LOWER", 61: "UPPER JET BUMPER", 62: "LEFT JET BUMPER", 63: "LOWER JET BUMPER", 64: "RIGHT SLINGSHOT",
	65: "LEFT SLINGSHOT", 66: "RIGHT 10 POINT", 67: "HIT ME TARGET", 68: "BALL SHOOTER",
}
COIN_EDGES = {1: ("LEFT COIN SLOT", "ORN-BRN BLACK"), 2: ("CENTER COIN SLOT", "ORN-RED BLACK"), 3: ("RIGHT COIN SLOT", "ORN-BLK BLACK"), 4: ("4TH COIN OPTION", "ORN-YEL BLACK")}
# The wire colours the ROM prints for a matrix switch: row wire first, then the column wire.
EDGE_ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
EDGE_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# Fliptronic column: printed position, wire, and the name the ROM shows while the host holds the address at 1.
FLIPPER_EDGES = {
	111: ("F1", "BLK-GRN ORN", None), 112: ("F1", "BLK-GRN ORN", "R. FLIPPER EOS."), 113: ("F3", "BLK-BLU ORN", None),
	114: ("F3", "BLK-BLU ORN", "L. FLIPPER EOS."), 115: ("F5", "BLK-VIO ORN", "VISOR IS CLOSED"), 116: ("F1", "BLK-GRN ORN", "R. FLIPPER EOS."),
	117: ("F7", "BLK-GRY ORN", "VISOR IS OPEN"), 118: ("F3", "BLK-BLU ORN", "L. FLIPPER EOS."),
}
SWEPT = (1, 2, 3, 4) + tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9)) + tuple(range(111, 119))
# Fliptronic button positions whose closure makes the ROM fire a lower flipper (power and hold windings).
FLIPPER_FIRES = {112: {45, 46}, 114: {47, 48}, 116: {45, 46}, 118: {47, 48}}
# Playfield switches whose closure makes the ROM fire their own coil even inside T.1 (jet bumpers and slingshots).
SWITCH_FIRES = {61: (13, "upper jet bumper"), 62: (12, "left jet bumper"), 63: (11, "lower jet bumper"), 64: (10, "right slingshot"), 65: (9, "left slingshot")}
PINMAME_MASKED = (16, 17, 18, 31, 32, 33, 34, 35)


def _matrix_wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{EDGE_ROW_WIRES[row]} GRN-{EDGE_COLUMN_WIRES[column]}"


def _edge_reading(address: int, level: int) -> str:
	idle = "SWITCH EDGES"
	if address in COIN_EDGES:
		name, wires = COIN_EDGES[address]
		return f"{name if level else idle} / T.1 LAST SW D{address} / {wires}"
	if address in FLIPPER_EDGES:
		position, wires, name = FLIPPER_EDGES[address]
		return f"{name if level and name else idle} / T.1 LAST SW {position} / {wires}"
	if address >= 71:
		return f"{idle} / T.1 LAST SW 68 / {_matrix_wires(68)}"
	if address == 24:
		# 24 rests at public 1 from power-up; the ROM names it on the 1 -> 0 edge and shows nothing new for the redundant 1.
		return f"ALWAYS CLOSED / T.1 LAST SW 24 / {_matrix_wires(24)}" if level == 0 else f"{idle} / T.1 LAST SW 23 / {_matrix_wires(23)}"
	return f"{EDGE_NAMES[address] if level else idle} / T.1 LAST SW {address} / {_matrix_wires(address)}"


# --- T.4 SOLENOID TEST, T.5 FLASHER TEST, T.12 FLIPPER COIL TEST ---------------------------------------
T4_ORDER = (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
T4_NAMES = {
	1: ("BALL RELEASE", "VIO-BRN RED-BRN"), 3: ("GAME SAUCER", "VIO-ORN RED-BRN"), 4: ("DROP TARGETS", "VIO-YEL RED-BRN"),
	5: ("RIGHT EJECT HOLE", "VIO-GRN RED-BRN"), 6: ("RAISE RAMP", "VIO-BLU RED-BRN"), 7: ("KNOCKER", "VIO-BLK RED-BRN"),
	8: ("LEFT EJECT HOLE", "VIO-GRY RED-BRN"), 9: ("LEFT SLINGSHOT", "BRN-BLK RED-BLK"), 10: ("RIGHT SLINGSHOT", "BRN-RED RED-BLK"),
	11: ("LOWER JET BUMPER", "BRN-ORN RED-BLK"), 12: ("LEFT JET BUMPER", "BRN-YEL RED-BLK"), 13: ("UPPER JET BUMPER", "BRN-GRN RED-BLK"),
	14: ("DROP RAMP", "BRN-BLU RED-BLK"),
}
T5_ORDER = tuple(range(15, 28))
T5_NAMES = {
	15: ("RIGHT VISOR", "BRN-VIO RED-WHT"), 16: ("LEFT VISOR", "BRN-GRY RED-WHT"), 17: ("CENTER VISOR", "BLK-BRN RED-WHT"),
	18: ("PINBOT FACE", "BLK-RED RED-WHT"), 19: ("JET BUMPERS", "BLK-ORN RED-WHT"), 20: ("LOWER LEFT", "BLK-YEL RED-WHT"),
	21: ("MID LEFT", "BLU-GRN RED-WHT"), 22: ("LOWER RIGHT", "BLU-BLK RED-WHT"), 23: ("BACK PANEL 1 (L)", "BLU-VIO RED-WHT"),
	24: ("BACK PANEL 2", "BLU-GRY RED-WHT"), 25: ("BACK PANEL 3", "BLU-BRN RED-WHT"), 26: ("BACK PANEL 4", "BLU-RED RED-WHT"),
	27: ("BACK PANEL 5 (R)", "BLU-ORN RED-WHT"),
}
T12_ORDER = ((1, "R. FLIP. POWER", "YEL-GRN RED-GRN", {45, 46}), (2, "R. FLIP. HOLD", "ORN-GRN RED-GRN", {46}),
	(3, "L. FLIP. POWER", "YEL-BLU RED-BLU", {47, 48}), (4, "L. FLIP. HOLD", "ORN-BLU RED-BLU", {48}))
# T.6: the step whose frame names each string, its printed wires, the public GI channel the following steps dim alone.
GI_STRINGS = ((8, "PLAYFIELD LOWER", "WHT-BRN BRN", 0), (16, "PLAYFIELD LEFT", "WHT-ORN ORN", 1), (24, "PLAYFIELD UPPER", "WHT-YEL YEL", 2),
	(32, "PLAYFIELD RIGHT", "WHT-GRN GRN", 3), (40, "INSERT", "WHT-VIO VIO", 4))
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMPS = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
LAMP_NAMES = {
	11: "YELLOW ARROW", 12: "YELLOW 1 (HI)", 13: "YELLOW 2", 14: "YELLOW 3", 15: "YELLOW 4", 16: "YELLOW 5 (LOW)",
	17: "LEFT OUTLANE", 18: "L. FLIPPER LANE", 21: "BLUE ARROW", 22: "BLUE 1 (HI)", 23: "BLUE 2", 24: "BLUE 3", 25: "BLUE 4",
	26: "BLUE 5 (LOW)", 27: "BONUS 2X", 28: "BONUS 4X", 31: "AMBER ARROW", 32: "AMBER 1 (HI)", 33: "AMBER 2", 34: "AMBER 3",
	35: "AMBER 4", 36: "AMBER 5 (LOW)", 37: "SHOOT AGAIN", 38: "BONUS 5X", 41: "GREEN ARROW", 42: "GREEN 1 (HI)", 43: "GREEN 2",
	44: "GREEN 3", 45: "GREEN 4", 46: "GREEN 5 (LOW)", 47: "BONUS 3X", 48: "JACK*BOT TARGET", 51: "RED ARROW", 52: "RED 1 (HI)",
	53: "RED 2", 54: "RED 3", 55: "RED 4", 56: "RED 5 (LOW)", 57: "R. FLIPPER LANE", 58: "RIGHT OUTLANE", 61: "CARD 1 (L)",
	62: "CARD 2", 63: "CARD 3", 64: "CARD 4", 65: "CARD 5 (R)", 66: "CASINO RUN", 67: "HIT ME", 68: "LOW DROP TARGET",
	71: "CASHIER MINI-P.F.", 72: "MEG. RAMP MINI-P.F.", 73: "LITE EXTRA BALL", 74: "JACK*BOT MINI-P.F.", 75: "GAME SAUCER",
	76: "MEGA RAMP", 77: "HIGH DROP TARGET", 78: "CENT. DROP TARGET", 81: "PINBOT POKER", 82: "SLOT MACHINE", 83: "ROLL THE DICE",
	84: "KENO", 85: "CASHIER", 86: "JACK*BOT (RAMP)", 87: "BUY IN BUTTON", 88: "START BUTTON",
}


# --- Shared helpers ------------------------------------------------------------------------------------
def _sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for chunk in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(chunk)
	return digest.hexdigest()


def _load_run(directory: Path, scenario: str) -> dict[str, Any]:
	run_path = directory / "run.json"
	run = json.loads(run_path.read_bytes())
	scenario_path = ROOT / SCENARIO_DIRECTORY / f"{scenario}.json"
	if run.get("failure") is not None or run.get("game") != GAME:
		raise ValueError(f"not a successful Jack*Bot {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != 0:
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


def _risen_from(run: dict[str, Any], label: str) -> set[int]:
	"""Solenoids raised during the step labelled ``label`` and every later step (the power-up homing is excluded)."""
	start = next(index for index, step in enumerate(run["steps"]) if step["label"] == label)
	return set().union(*(_risen(step) for step in run["steps"][start:] if "transitions" in step))


def _seen(run: dict[str, Any]) -> list[int]:
	return sorted({event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]})


def _observation(label: str, inputs: list[int], solenoids: set[int] | list[int], *, active: list[int] | None = None) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": active or [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": sorted(solenoids),
	}


def _document(name: str, directory: str, scenario: str, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/jackbot_runtime_evidence.py", "version": 1},
		"format": "pinmame-machine-evidence",
		"machine_ids": [MACHINE_ID],
		"mechanisms": [],
		"outputs": [],
		"recreation_notes": [],
		"runtime": {
			"command_template": COMMAND.format(scenario=f"{SCENARIO_DIRECTORY}/{scenario}.json") + command,
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
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
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
		elif address in COIN_EDGES:
			named.append(_observation(f"T.1 names {COIN_EDGES[address][0]!r} (D{address}) while host public {address} is 1 and clears it at 0", [address], set()))
		elif address in EDGE_NAMES:
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
		f"PinMAME's jbGameData mask inverts public {', '.join(map(str, PINMAME_MASKED))}; every one of them is still named at public 1."
	)
	return observations, command


def build_solenoids(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
	named = []
	for index, address in enumerate(T4_ORDER):
		label = "Enter (start T.4 SOLENOID TEST)" if index == 0 else f"T.4 step {index}"
		name, wires = T4_NAMES[address]
		readings[label] = f"{name} / T.4 {address:02d} REPEAT / {wires}"
		risen = _risen(_step(run, label))
		if risen != {address}:
			raise ValueError(f"T.4 step {index} ({address}) published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.4 SOLENOID TEST selects {address:02d} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 0 else 7], risen))
	for lap in (1, 2):
		for index, address in enumerate(T4_ORDER):
			step = lap * len(T4_ORDER) + index
			if step > 40:
				break
			if _risen(_step(run, f"T.4 step {step}")) != {address}:
				raise ValueError(f"T.4 step {step} must repeat solenoid {address} on lap {lap + 1}")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"Each Up press selects the next T.4 item; in repeat mode the ROM pulses it until the next press. The test walks 1 and 3-14 and wraps "
		"to 1 (the run steps it 40 times, three laps); it skips 2, the flashers 15-27, the visor motor 28 and 37-44."
	)
	return observations, command


def build_flashers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
	named = []
	for index, address in enumerate(T5_ORDER):
		label = "Enter (start T.5 FLASHER TEST)" if index == 0 else f"T.5 step {index}"
		name, wires = T5_NAMES[address]
		readings[label] = f"{name} / T.5 {address} REPEAT / {wires}"
		risen = _risen(_step(run, label))
		if risen != {address}:
			raise ValueError(f"T.5 step {index} published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.5 FLASHER TEST selects {address} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 0 else 7], risen))
	if _risen(_step(run, f"T.5 step {len(T5_ORDER)}")) != {T5_ORDER[0]}:
		raise ValueError("T.5 must wrap to its first flasher")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, f"Each Up press selects the next flasher; the test walks {', '.join(map(str, T5_ORDER))} and wraps."


def build_flippers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
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
	if set(_seen(run)) & {33, 34, 35, 36}:
		raise ValueError("no run may publish the unfitted upper-flipper circuits 33-36")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The test walks only the four lower-flipper items (power drives both windings, hold the hold winding) and wraps; it offers no item for 33-36."


def build_gi(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
	named = []
	for step, name, wires, channel in GI_STRINGS:
		readings[f"T.6 step {step}"] = f"{name} / T.6 BRIGHT=1 STOP / {wires}"
		following = [_changed(_step(run, f"T.6 step {step + offset}"), "gis") for offset in range(1, 6)]
		if any(item != {channel} for item in following):
			raise ValueError(f"T.6 string {name} must dim public GI {channel} alone, saw {following}")
		named.append(_observation(f"T.6 {name} ({wires}): the next Up presses step the brightness of public GI {channel} alone", [7], set()))
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "T.6 stop mode first steps all illumination through its brightness levels, then each of the five strings alone; every string dims."


def build_lamps(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION}
	for index, address in enumerate(LAMPS):
		label = "T.8 started" if index == 0 else f"T.8 step {index}"
		column, row = divmod(address, 10)
		frame = "T.8 step 64, frame 2" if index == 0 else f"T.8 step {index}, frame 2"
		readings[frame] = f"{LAMP_NAMES[address]} / T.8 {index + 1:02d} LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"
		lit = _snapshot(run, label)["active_lamps"]
		if address not in _risen(_step(run, label), "lamps") and address not in lit:
			raise ValueError(f"T.8 step {index} did not light public lamp {address}")
	if 11 not in _risen(_step(run, "T.8 step 64"), "lamps"):
		raise ValueError("T.8 must wrap to lamp 11 after 88")
	named = [_observation("T.8 SINGLE LAMPS test lights public lamps 11-88 one at a time in matrix order while printing each name, its test number and its row and column wires", [7], set())]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next lamp; the name line blinks and is read on each step's second frame (lamp 11's on the wrap, step 64)."


RAMP_READINGS: dict[str, str] = {}
VISOR_READINGS: dict[str, str] = {}


RAMP_READINGS = {
	"Enter (start T.16 RAMP TEST)": "RAMP DOWN / T.16 02 RUNNING",
	"T.16 started, frame 2": "RAMP UP / T.16 01 RUNNING",
	"15 -> 1": "RAMP DOWN / T.16 02 RUNNING / RAMP DOWN SW.",
	"15 held, frame 2": "RAMP UP / T.16 01 RUNNING / RAMP DOWN SW.",
	"Enter (repeat 01 RAMP UP)": "RAMP UP / T.16 01 REPEAT",
	"Up (select 02 RAMP DOWN, repeat)": "RAMP DOWN / T.16 02 REPEAT",
	"Enter (stop)": "RAMP DOWN / T.16 02 STOPPED",
}
# Steps whose recorded transitions pulse exactly one ramp coil, with the item the frame after the step shows.
RAMP_PULSES = (
	("T.16 started, frame 2", 6), ("15 -> 1", 14), ("15 held, frame 2", 6), ("15 held, frame 3", 14), ("15 -> 0", 6),
	("15 released, frame 2", 14), ("Enter (repeat 01 RAMP UP)", 6), ("01 RAMP UP repeat, frame 2", 6),
)


def build_ramp(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION, **RAMP_READINGS}
	for label, address in RAMP_PULSES:
		if _risen(_step(run, label)) != {address}:
			raise ValueError(f"T.16 step {label!r} must pulse solenoid {address} alone, saw {sorted(_risen(_step(run, label)))}")
	repeat_down = [_risen(_step(run, label)) for label in ("Up (select 02 RAMP DOWN, repeat)", "02 RAMP DOWN repeat, frame 1", "02 RAMP DOWN repeat, frame 2", "02 RAMP DOWN repeat, frame 3")]
	if not any(repeat_down) or any(item - {14} for item in repeat_down):
		raise ValueError(f"02 RAMP DOWN in repeat must pulse only solenoid 14, saw {repeat_down}")
	if _risen_from(run, "Enter (start T.16 RAMP TEST)") - {29, 31} != {6, 14}:
		raise ValueError(f"T.16 must drive only the ramp coils, saw {sorted(_risen_from(run, 'Enter (start T.16 RAMP TEST)'))}")
	named = [
		_observation("T.16 RAMP TEST running alternates 01 RAMP UP, which pulses public 6, and 02 RAMP DOWN, which pulses public 14", [8], {6, 14}),
		_observation("While host public 15 is 1, T.16 adds 'RAMP DOWN SW.' to the display (the ramp-down switch read closed) and keeps cycling; the line is gone at 0", [15], {6, 14}),
		_observation("T.16 in repeat mode pulses only the selected coil: 01 RAMP UP public 6, 02 RAMP DOWN public 14", [7, 8], {6, 14}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"T.16 starts running, cycling the ramp up and down without waiting for the ramp switch; Up selects an item and Enter steps "
		"through RUNNING, REPEAT and STOPPED. The bottom display line reads RAMP DOWN SW. while the ROM reads public 15 closed."
	)
	return observations, command


def _visor(test: str, state: str, opened: bool, closed: bool) -> str:
	return f"VISOR TEST / TEST = {test} / {state} / OPEN [{'x' if opened else ' '}] CLOSED [{'x' if closed else ' '}]"


VISOR_READINGS = {
	"Enter (start T.17 VISOR TEST)": _visor("OPEN", "STOPPED", False, False),
	"Enter (run OPEN)": _visor("OPEN", "RUNNING", False, False),
	"115 -> 1 while OPEN runs": _visor("OPEN", "RUNNING", False, True),
	"117 -> 1 while OPEN runs": _visor("OPEN", "RUNNING", True, True),
	"Up (CLOSE)": _visor("CLOSE", "STOPPED", False, False),
	"Enter (run CLOSE)": _visor("CLOSE", "RUNNING", False, False),
	"117 -> 1 while CLOSE runs": _visor("CLOSE", "RUNNING", True, False),
	"115 -> 1 while CLOSE runs": _visor("CLOSE", "RUNNING", True, True),
}
# (step label, whether the visor motor output 28 is on in the snapshot after the step)
VISOR_MOTOR = (
	("Enter (start T.17 VISOR TEST)", False), ("Enter (run OPEN)", True), ("115 -> 1 while OPEN runs", True),
	("117 -> 1 while OPEN runs", False), ("117 -> 0", True), ("Enter (stop)", False), ("Up (CLOSE)", False),
	("Enter (run CLOSE)", True), ("117 -> 1 while CLOSE runs", True), ("115 -> 1 while CLOSE runs", False), ("115 -> 0 in CLOSE", True),
)


def build_visor(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {IDENTIFICATION_LABEL: IDENTIFICATION, **VISOR_READINGS}
	for label, on in VISOR_MOTOR:
		if (28 in _snapshot(run, label)["active_solenoids"]) != on:
			raise ValueError(f"visor motor 28 must be {'on' if on else 'off'} after {label!r}")
	if _risen_from(run, "Enter (start T.17 VISOR TEST)") - {29, 31} != {28}:
		raise ValueError(f"T.17 must drive only the visor motor, saw {sorted(_risen_from(run, 'Enter (start T.17 VISOR TEST)'))}")
	named = [
		_observation("T.17 VISOR TEST running OPEN drives the visor motor output 28; with public 115 held at 1 it keeps running and marks CLOSED", [115], {28}, active=[28]),
		_observation("T.17 running OPEN stops output 28 as soon as public 117 is 1 and marks OPEN; releasing 117 starts the motor again", [117], {28}),
		_observation("T.17 running CLOSE drives output 28; with public 117 held at 1 it keeps running and marks OPEN", [117], {28}, active=[28]),
		_observation("T.17 running CLOSE stops output 28 as soon as public 115 is 1 and marks CLOSED; releasing 115 starts the motor again", [115], {28}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"T.17 starts at TEST = OPEN, STOPPED; Enter toggles RUNNING and STOPPED and Up selects the next mode. One output, 28, drives the "
		"motor in both modes. The OPEN and CLOSED boxes are filled while the ROM reads public 117 and 115 as closed; the display keeps "
		"showing RUNNING after the ROM drops the motor at the selected end switch."
	)
	return observations, command


Builder = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]
RUNS: dict[str, tuple[str, str, Builder]] = {
	"jackbot-jb_10r-switch-edges-sweep.json": ("switch-edges-sweep", "jb-switch-edges-sweep", build_edges),
	"jackbot-jb_10r-solenoid-test.json": ("solenoid-test", "jb-solenoid-test", build_solenoids),
	"jackbot-jb_10r-flasher-test.json": ("flasher-test", "jb-flasher-test", build_flashers),
	"jackbot-jb_10r-flipper-coil-test.json": ("flipper-coil-test", "jb-flipper-coil-test", build_flippers),
	"jackbot-jb_10r-gi-test.json": ("gi-test", "jb-gi-test", build_gi),
	"jackbot-jb_10r-single-lamps.json": ("single-lamps", "jb-single-lamps", build_lamps),
	"jackbot-jb_10r-ramp-test.json": ("ramp-test", "jb-ramp-test", build_ramp),
	"jackbot-jb_10r-visor-test.json": ("visor-test", "jb-visor-test", build_visor),
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, (directory, scenario, builder) in RUNS.items():
		path = review_root / HARNESS_DIRECTORY / directory
		run = _load_run(path, scenario)
		observations, command = builder(run)
		document = _document(filename.removeprefix("jackbot-").removesuffix(".json"), directory, scenario, run, observations, command)
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
			raise ValueError(f"Jack*Bot compact runtime evidence drift: {path}")


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
		print("Jack*Bot compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
