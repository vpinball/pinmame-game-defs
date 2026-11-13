"""Derive the compact No Fear: Dangerous Sports runtime evidence from the retained raw harness runs.

Each document reads one successful run of the pinned LibPinMAME build (a ``run.json`` under the external review-artifacts
root), checks that it ran the committed scenario, the pinned binary and the expected mechanism mask, and writes the derived
observations beside the other WPC-Security runtime evidence. A diagnostic snapshot's ``interpreted_text`` is the curator's
visual reading of that snapshot's retained DMD frame, pinned by its pixel SHA-256; readings of one text must come from identical
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
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.no-fear-dangerous-sports.1995"
GAME = "nf_23x"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "bc63ce9b07ae781c7f5a767422c1e109a118fb4195165221ee5d9feb07c047ee"
HARNESS_DIRECTORY = "williams.no-fear-dangerous-sports.1995/harness"
SCENARIO_DIRECTORY = "tools/harness-scenarios/wpc-security"
EVIDENCE_DIRECTORY = ROOT / "evidence/runtime/wpc-security"
# Every diagnostic reading pinned to the frame the curator read: document -> label -> {pixel_sha256, reading}. A run whose
# frame or reading differs is refused until the new frame has been read again and the seed updated by hand.
FRAME_SEED_PATH = ROOT / "tools/seeds/williams/no-fear-dangerous-sports-1995-frames.json"
ATTRIBUTION = (
	"Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external. Public switch writes are "
	"host stimuli, never ROM observations. The runner can checkpoint only segment-display text, so the DMD service-menu navigation "
	"is counted pulses; every diagnostic snapshot's interpreted_text is the curator's visual reading of its retained DMD frame, "
	"identified by its pixel SHA-256. The exact external directory manifest (built by tools/build_external_evidence_manifest.py) "
	"lists the raw trace, the copied scenario, the DMD frames and the isolated mutable state, with no ROM bytes."
)
NVRAM_NOTE = (
	"empty; the run created its own isolated PinMAME state directory, so the ROM restored its factory settings before the "
	"scenario left the message loop with Escape"
)
IDENTIFICATION_LABEL = "Enter 1 (game identification)"
IDENTIFICATION = "NO FEAR PINBALL / 50025 REV. 2.3 X"
MECHANICS = 0
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game nf_23x --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics 0 --scenario {scenario} --dmd-dir <external-dmd-dir> --output <external-run.json>. "
)
# PinMAME's state channels change in every menu; observations about named coils ignore them.
BACKGROUND = frozenset({29, 30, 31})

# --- T.1 SWITCH EDGES sweep ----------------------------------------------------------------------------
# The name the ROM prints on the top display line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	11: "BALL LAUNCH", 12: "UNUSED", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "SHOOTER LANE", 16: "SPINNER",
	17: "RIGHT OUTLANE", 18: "RIGHT RETURN", 21: "SLAM TILT", 23: "BUY EXTRA BALL", 24: "ALWAYS CLOSED", 25: "KICKBACK",
	26: "LEFT RETURN", 27: "LEFT SLINGSHOT", 28: "RIGHT SLINGSHOT", 31: "TROUGH STACK", 32: "TROUGH 1 (RIGHT)", 33: "TROUGH 2",
	34: "TROUGH 3", 35: "TROUGH 4", 36: "UNUSED", 37: "CENTER TR. ENTR.", 38: "LEFT TR. ENTR.", 41: "RIGHT POPPER 1",
	42: "RIGHT POPPER 2", 43: "UNUSED", 44: "UNUSED", 45: "UNUSED", 46: "LEFT MAGNET", 47: "CENTER MAGNET", 48: "RIGHT MAGNET",
	51: "DROP TARGET", 52: "UNUSED", 53: "UNUSED", 54: "LEFT WIREFORM", 55: "INNER LOOP", 56: "LIGHT KB. BOTTOM",
	57: "LIGHT KB. TOP", 58: "RIGHT LOOP", 61: "EJECT HOLE", 62: "LEFT LOOP", 63: "LEFT RAMP ENTER", 64: "LEFT RMP. MIDDLE",
	65: "UNUSED", 66: "RIGHT RMP. ENTER", 67: "RIGHT RAMP EXIT", 68: "UNUSED",
}
# The ROM names 24 on the 1 -> 0 edge instead: PinMAME holds it at public 1 from power-up.
NAMED_AT_ZERO = frozenset({24})
EDGE_ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
EDGE_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# The ROM reports no edge in matrix columns 7 and 8: T.1 keeps the last line it showed for 68.
UNSCANNED = tuple(column * 10 + row for column in (7, 8) for row in range(1, 9))
# Fliptronic column: the position and wires the ROM shows after each host level, and the name while the host holds 1 (None: no name).
FLIPPER_EDGES = {
	111: ("F1", "BLK-GRN ORN", None), 112: ("F1", "BLK-GRN ORN", "R. FLIPPER E.O.S."), 113: ("F3", "BLK-BLU ORN", None),
	114: ("F3", "BLK-BLU ORN", "L. FLIPPER E.O.S."), 115: ("F5", "BLK-VIO ORN", None), 116: ("F5", "BLK-VIO ORN", "U.R. FLIPPER E.O.S."),
	117: ("F5", "BLK-VIO ORN", None), 118: ("F3", "BLK-BLU ORN", "L. FLIPPER E.O.S."),
}
SWEPT = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9) if column * 10 + row != 22) + tuple(range(111, 119))
# PinMAME rewrites the end-of-stroke bits of the flippers nfGameData declares with FLIP_SOL (the lower pair and upper right).
SYNTHESIZED = frozenset({111, 113, 115})
FLIPPER_FIRES = {112: {45, 46}, 114: {47, 48}, 116: {33, 34, 45, 46}, 118: {47, 48}}
# The power windings of those flippers; the others are their hold windings.
FLIPPER_POWER = frozenset({33, 45, 47})
SWITCH_FIRES = {27: (11, "left slingshot"), 28: (10, "right slingshot")}
# nfGameData inverted switches {0x00,0x00,0x00,0xff,0xe3,0x00,...} through wpc_sw2m.
PINMAME_MASKED = (31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 46, 47, 48)


def _matrix_wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{EDGE_ROW_WIRES[row]} GRN-{EDGE_COLUMN_WIRES[column]}"


def _edge_reading(address: int, level: int) -> str:
	idle = "SWITCH EDGES"
	if address in FLIPPER_EDGES:
		position, wires, name = FLIPPER_EDGES[address]
		return f"{name if level and name else idle} / T.1 LAST SW. {position} / {wires}"
	if address in UNSCANNED:
		return f"{idle} / T.1 LAST SW. 68 / {_matrix_wires(68)}"
	if address == 24:
		if level == 0:
			return f"{EDGE_NAMES[24]} / T.1 LAST SW. 24 / {_matrix_wires(24)}"
		return f"{idle} / T.1 LAST SW. F3 / BLK-BLU ORN"
	return f"{EDGE_NAMES[address] if level else idle} / T.1 LAST SW. {address} / {_matrix_wires(address)}"


# --- T.4 SOLENOID TEST, T.5 FLASHER TEST, T.12 FLIPPER COIL TEST, T.6 GI, T.8 LAMPS ----------------------
T4_NAMES = {
	1: ("RIGHT POPPER", "VIO-BRN RED-BRN"), 2: ("AUTO PLUNGER", "VIO-RED RED-BRN"), 3: ("RIGHT MAGNET", "VIO-ORN RED-BRN"),
	4: ("KICKBACK", "VIO-YEL RED-BRN"), 5: ("CENTER MAGNET", "VIO-GRN RED-BRN"), 6: ("LEFT MAGNET", "VIO-BLU RED-BRN"),
	7: ("KNOCKER", "VIO-BLK RED-BRN"), 8: ("DROP TARGET DOWN", "VIO-GRY RED-BRN"), 9: ("UNUSED", "BRN-BLK RED-BLK"),
	10: ("RIGHT SLINGSHOT", "BRN-RED RED-BLK"), 11: ("LEFT SLINGSHOT", "BRN-ORN RED-BLK"), 12: ("DROP TARGET UP", "BRN-YEL RED-BLK"),
	13: ("UNUSED", "BRN-GRN RED-BLK"), 14: ("TROUGH", "BRN-BLU RED-BLK"), 15: ("EJECT", "BRN-VIO RED-BLK"),
	16: ("SKULL MOUTH", "BRN-GRY RED-BLK"),
}
T4_ORDER = tuple(T4_NAMES)
T5_NAMES = {
	17: ("FLS.(2) FLPR. RTRN.", "BLK-BRN RED-WHT"), 18: ("FLS. SPINNER", "BLK-RED RED-WHT"), 19: ("FLS. NO FEAR", "BLK-ORN RED-WHT"),
	20: ("FLS.(3) RT. RAMP", "BLK-YEL RED-WHT"), 21: ("FLS.(2) SKULL", "BLU-GRN RED-WHT"), 22: ("FLS. BKBOX EXPL.", "BLU-BLK RED-WHT"),
	23: ("FLS.(3) LEFT RAMP", "BLU-VIO RED-WHT"), 24: ("FLS. TOP LEFT", "BLU-GRY RED-WHT"), 25: ("FLS.(2) AUTO-FIRE", "BLU-BRN RED-WHT"),
	26: ("FLS. BKBOX L TOP", "BLU-RED RED-WHT"), 27: ("FLS. BKBOX R TOP", "BLU-ORN RED-WHT"), 28: ("FLS. RT. POPPER", "BLU-YEL RED-WHT"),
}
T5_ORDER = tuple(T5_NAMES)
# The frame read for each T.5 item (the name blinks): the brightest of the six frames taken after the press that selects it.
T5_FRAME = {1: 0, 2: 5, 3: 5, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 3, 11: 3, 12: 5}
T12_ORDER = (
	(1, "R. FLIP. POWER", "YEL-GRN RED-GRN", {45, 46}), (2, "R. FLIP. HOLD", "ORN-GRN RED-GRN", {46}),
	(3, "L. FLIP. POWER", "YEL-BLU RED-BLU", {47, 48}), (4, "L. FLIP. HOLD", "ORN-BLU RED-BLU", {48}),
	(5, "U.R. FLIP. POWER", "YEL-VIO RED-VIO", {33, 34}), (6, "U.R. FLIP. HOLD", "ORN-VIO RED-VIO", {34}),
)
# T.6: (public GI string, snapshot read, ROM text, the Up presses whose transitions dim that string alone).
GI_STRINGS = (
	(0, "T.6 Up 9 (held)", "PLAYFIELD TOP / T.6 BRIGHT=2 STOP / WHT-BRN BRN", range(9, 15)),
	(1, "T.6 Up 17 (held)", "PLAYFIELD RIGHT / T.6 BRIGHT=2 STOP / WHT-ORN ORN", range(17, 23)),
	(2, "T.6 Up 25 (held)", "PLAYFIELD LEFT / T.6 BRIGHT=2 STOP / WHT-YEL YEL", range(25, 31)),
	(3, "T.6 Up 33 (held)", "INSERT TITLE / T.6 BRIGHT=2 STOP / WHT-GRN GRN", range(33, 39)),
	(4, "T.6 Up 41 (held)", "INSERT BKGROUND / T.6 BRIGHT=2 STOP / WHT-VIO VIO", range(41, 47)),
)
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
MATRIX_LAMPS = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
# T.8 SINGLE LAMPS names, read from the retained frames taken while each Up press was held.
LAMP_NAMES = {
	11: "15 MILLION", 12: "10 MILLION", 13: "5 MILLION", 14: "L. OVER THE EDGE", 15: "DIRT", 16: "ASPHALT", 17: "NO LIMITS",
	18: "WATER", 21: "NO FEAR", 22: "20 MILLION", 23: "LIGHT EXTRA BALL", 24: "R. OVER THE EDGE", 25: "AIR", 26: "SNOW",
	27: "FEAR FEST", 28: "MEET YOUR MAKER", 31: "SKULL", 32: "R. TRACK", 33: "CENTER JACKPOT", 34: "EXTRA BALL",
	35: "START CHALLENGE", 36: "CENTER LOCK", 37: "R. AUTOFIRE (2)", 38: "L. HURRY UP", 41: "L. TRACK", 42: "1ST", 43: "2ND",
	44: "3RD", 45: "SKYDIVE", 46: "DROP JACKPOT", 47: "DROP LOCK", 48: "L. AUTOFIRE (2)", 51: "RACEWAY", 52: 'L. RAMP "TURN"',
	53: "SUPER SPIN", 54: 'L. RAMP "START"', 55: 'L. RAMP "WIN!"', 56: "HILL CLIMB", 57: "SCREAMER", 58: "UNUSED", 61: "TUBE",
	62: "VIDEO MODE", 63: 'R. RAMP "WIN!"', 64: 'R. RAMP "TURN"', 65: 'R. RAMP "START"', 66: "L. FLIPPER LANE", 67: "L. OUTLANE",
	68: "KICKBACK", 71: "LIGHT KB. TOP", 72: "LIGHT KB. BOTTOM", 73: "R. FLIPPER LANE", 74: "R. OUTLANE", 75: "HAIRPIN",
	76: "DOWNHILL", 77: "SUMMIT", 78: "R. HURRY UP", 81: "SHOOT AGAIN", 82: "L. SKULL EYE", 83: "JUMP NOW", 84: "SUPER JACKPOT",
	85: "R. SKULL EYE", 86: "BALL LAUNCH", 87: "BUY-IN BUTTON", 88: "START BUTTON",
}

# --- T.16 BALL ACCELERATOR TEST ----------------------------------------------------------------------------
# The test draws one icon per ramp magnet over its name: a magnet symbol while the magnet is enabled (filled while the ROM
# energizes it), a cross once Enter disables it (with a bar while its opto is blocked); a frame surrounds the selected magnet.
ACCELERATOR_READINGS = {
	"Enter (start T.16)": "LEFT boxed magnet / CENTER magnet / RIGHT magnet / BALL ACCELERATOR TEST",
	"46 with all three magnets enabled (held)": "LEFT boxed magnet filled / CENTER magnet / RIGHT magnet / BALL ACCELERATOR TEST",
	"Enter (disable LEFT)": "LEFT boxed cross / CENTER magnet / RIGHT magnet / BALL ACCELERATOR TEST",
	"46 with LEFT disabled (held)": "LEFT boxed cross with bar / CENTER magnet / RIGHT magnet / BALL ACCELERATOR TEST",
	"48 with LEFT disabled (held)": "LEFT boxed cross / CENTER magnet / RIGHT magnet filled / BALL ACCELERATOR TEST",
	"Enter (disable CENTER)": "LEFT cross / CENTER boxed cross / RIGHT magnet / BALL ACCELERATOR TEST",
	"47 with LEFT and CENTER disabled (held)": "LEFT cross / CENTER boxed cross with bar / RIGHT magnet / BALL ACCELERATOR TEST",
	"Enter (disable RIGHT)": "LEFT cross / CENTER cross / RIGHT boxed cross / BALL ACCELERATOR TEST",
	"48 with all three disabled (held)": "LEFT cross / CENTER cross / RIGHT boxed cross with bar / BALL ACCELERATOR TEST",
	"Enter (enable RIGHT)": "LEFT cross / CENTER cross / RIGHT boxed magnet / BALL ACCELERATOR TEST",
	"48 with RIGHT enabled again (held)": "LEFT cross / CENTER cross / RIGHT boxed magnet filled / BALL ACCELERATOR TEST",
}
# Each opto pulse: (step label, the magnet coil it must fire, or None when that magnet is disabled).
ACCELERATOR_PULSES = (
	("46 with all three magnets enabled", 6), ("46 with LEFT disabled", None), ("47 with LEFT disabled", 5),
	("48 with LEFT disabled", 3), ("47 with LEFT and CENTER disabled", None), ("48 with LEFT and CENTER disabled", 3),
	("48 with all three disabled", None), ("48 with RIGHT enabled again", 3),
)
ACCELERATOR_SILENT = ("Enter (start T.16)", "Enter (disable LEFT)", "Up (select CENTER)", "Enter (disable CENTER)", "Up (select RIGHT)", "Enter (disable RIGHT)", "Enter (enable RIGHT)")

# --- T.18 UNDERGROUND TROUGH TEST ----------------------------------------------------------------------------
TROUGH_BOXES = ("LEFT ENTR.", "CTR. ENTR.", "POPPER 2", "POPPER 1")


def _trough_reading(mode: str, marked: str | None = None) -> str:
	boxes = " ".join(f"[{'x' if name == marked else ' '}] {name}" for name in TROUGH_BOXES)
	return f"TROUGH TEST ({mode}) / {boxes}"


TROUGH_READINGS = {
	"Enter (start T.18, MANUAL)": _trough_reading("MANUAL"),
	"MANUAL 38 -> 1": _trough_reading("MANUAL", "LEFT ENTR."),
	"MANUAL 37 -> 1": _trough_reading("MANUAL", "CTR. ENTR."),
	"MANUAL 42 -> 1": _trough_reading("MANUAL", "POPPER 2"),
	"MANUAL 41 -> 1": _trough_reading("MANUAL", "POPPER 1"),
	"Enter (AUTOMATIC)": _trough_reading("AUTOMATIC"),
	"AUTOMATIC: right popper": _trough_reading("AUTOMATIC", "POPPER 1"),
}
# The automatic cycle: (step label, the named coils that must rise in it).
TROUGH_CYCLE = (
	("Enter (AUTOMATIC)", {14}), ("AUTOMATIC: trough eject", {14}), ("trough 35 -> 0 (one ball leaves)", set()),
	("shooter 15 -> 1", set()), ("AUTOMATIC: auto plunger", {2}), ("shooter 15 -> 0", set()), ("left trough entrance 38", set()),
	("center trough entrance 37", set()), ("right popper 2 opto 42", set()), ("right popper 1 opto 41 -> 1", set()),
	("AUTOMATIC: right popper", {1}), ("right popper 1 opto 41 -> 0", set()), ("AUTOMATIC after the cycle", {14}),
)
# Each held coil: (public coil, step on which the ROM turns it on, step on which the ROM releases it).
TROUGH_HOLDS = (
	(14, "AUTOMATIC: trough eject", "trough 35 -> 0 (one ball leaves)"),
	(2, "AUTOMATIC: auto plunger", "shooter 15 -> 0"),
	(1, "AUTOMATIC: right popper", "right popper 1 opto 41 -> 0"),
)

# --- T.19 SKULL TEST -------------------------------------------------------------------------------------
SKULL_READINGS = {"Enter (start T.19)": "SKULL TEST / T.19", "T.19 frame 7": "SKULL TEST / T.19"}


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
		raise ValueError(f"not a successful No Fear {GAME} run: {run_path}")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise ValueError(f"wrong pinned emulator binary: {run_path}")
	if run["scenario"]["sha256"] != _sha256(scenario_path) or _sha256(directory / "scenario.json") != _sha256(scenario_path):
		raise ValueError(f"scenario identity drift: {run_path}")
	if run.get("handle_mechanics") != MECHANICS:
		raise ValueError(f"unexpected built-in mechanism mask in {run_path}")
	run["_directory"] = directory
	return run


def _frame_matches(run: dict[str, Any], display: dict[str, Any]) -> bool:
	"""Whether the retained PGM frame reproduces the snapshot's pixel SHA-256.

	run_pinmame_harness.py hashes the raw levels and writes them to the PGM unchanged when any exceeds the layout's depth, or
	scaled to 0-255 (level * 255 / max_level) otherwise; either encoding is accepted.
	"""
	path = run["_directory"] / "dmd" / display["artifact"].replace("\\", "/").rsplit("/", 1)[1]
	layout = display["layout"]
	header = f"P5\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
	data = path.read_bytes()
	if not data.startswith(header) or len(data) != len(header) + layout["width"] * layout["height"]:
		raise ValueError(f"unexpected DMD frame file: {path}")
	payload = data[len(header):]
	max_level = max((1 << max(int(layout.get("depth", 1)), 1)) - 1, 1)
	candidates = {hashlib.sha256(payload).hexdigest(), hashlib.sha256(bytes(round(value * max_level / 255) for value in payload)).hexdigest()}
	return display["pixel_sha256"] in candidates


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


def _states(step: dict[str, Any], channel: str, number: int) -> list[int]:
	for item in step["transitions"][channel]:
		if item["number"] == number:
			return list(item["states"])
	return []


def _named_coils(step: dict[str, Any]) -> set[int]:
	return _risen(step) - BACKGROUND


def _changed(step: dict[str, Any], channel: str) -> set[int]:
	return {item["number"] for item in step["transitions"][channel]}


def _diagnostics(run: dict[str, Any], readings: dict[str, str], grid_marked: frozenset[str] = frozenset()) -> list[dict[str, Any]]:
	"""Pin each reading to its frame; one interpreted text must always come from one frame.

	``grid_marked`` names T.1 frames taken while a switch is held: the switch grid on the left of the display marks that raw cell,
	so frames whose text agrees may still differ there, and they are exempt from the one-text-one-frame rule.
	"""
	result = []
	by_text: dict[str, str] = {}
	for label, text in readings.items():
		snapshot = _snapshot(run, label)
		displays = [item for item in snapshot["displays"] if item["index"] == 0]
		if len(displays) != 1:
			raise ValueError(f"snapshot {label!r} must carry display 0 exactly once")
		pixel = displays[0]["pixel_sha256"]
		if not _frame_matches(run, displays[0]):
			raise ValueError(f"retained DMD frame of snapshot {label!r} does not reproduce its pixel SHA-256")
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


def _observation(label: str, inputs: list[int], solenoids: set[int] | list[int]) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": sorted(solenoids),
	}


def _document(name: str, directory: str, scenario: str, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/no_fear_runtime_evidence.py", "version": 1},
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


def _base() -> dict[str, str]:
	return {IDENTIFICATION_LABEL: IDENTIFICATION}


def _result(run: dict[str, Any], readings: dict[str, str], named: list[dict[str, Any]], grid_marked: frozenset[str] = frozenset()) -> dict[str, Any]:
	return {"diagnostic_snapshots": _diagnostics(run, readings, grid_marked), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}


# --- Builders ------------------------------------------------------------------------------------------
def build_edges(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	named = []
	for address in SWEPT:
		for level in (1, 0):
			readings[f"{address} -> {level}"] = _edge_reading(address, level)
		held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> 1")["watched_switches"]}
		if held[address] != (0 if address in SYNTHESIZED else 1):
			raise ValueError(f"unexpected observed level of {address} after the host wrote 1")
		risen = _named_coils(_step(run, f"{address} -> 1")) | _named_coils(_step(run, f"{address} -> 0"))
		expected = FLIPPER_FIRES.get(address) or ({SWITCH_FIRES[address][0]} if address in SWITCH_FIRES else set())
		if risen != expected:
			raise ValueError(f"T.1 at public {address} published {sorted(risen)}, expected {sorted(expected)}")
		if address in FLIPPER_FIRES:
			pressed, released = _step(run, f"{address} -> 1"), _step(run, f"{address} -> 0")
			powers, holds = sorted(risen & FLIPPER_POWER), sorted(risen - FLIPPER_POWER)
			for coil in powers:
				if _states(pressed, "solenoids", coil) != [1, 0] or _states(released, "solenoids", coil):
					raise ValueError(f"T.1 at public {address}: power winding {coil} must pulse once while 1 is held and stay off at 0")
			for coil in holds:
				if _states(pressed, "solenoids", coil) != [1] or _states(released, "solenoids", coil) != [0]:
					raise ValueError(f"T.1 at public {address}: hold winding {coil} must stay on while 1 is held and drop at 0")
			position, _, name = FLIPPER_EDGES[address]
			named.append(_observation(
				f"T.1 with host public {address} set to 1: the ROM names {name!r} ({position}), pulses the power "
				f"{'winding' if len(powers) == 1 else 'windings'} public {' and '.join(map(str, powers))} once and holds public "
				f"{' and '.join(map(str, holds))} on until the host writes 0", [address], risen))
		elif address in SWITCH_FIRES:
			named.append(_observation(
				f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and the ROM fires the {SWITCH_FIRES[address][1]} coil, "
				f"public {SWITCH_FIRES[address][0]}, on the closure", [address], risen))
		elif address in NAMED_AT_ZERO or address in FLIPPER_EDGES or address in UNSCANNED:
			continue
		elif EDGE_NAMES[address] == "UNUSED":
			named.append(_observation(f"T.1 shows 'UNUSED' while host public {address} is 1 and clears it at 0: the ROM scans the position without a device", [address], set()))
		else:
			named.append(_observation(f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and clears it at 0", [address], set()))
	named.append(_observation("Public 24 rests at 1 from power-up; T.1 shows no new name for the redundant 1 and names 'ALWAYS CLOSED' on the 1 -> 0 edge", [24], set()))
	named.append(_observation("Public 71-78 and 81-88: T.1 names nothing at either level and keeps its last line for 68, so the ROM reports no edge in matrix columns 7 and 8", list(UNSCANNED), set()))
	named.append(_observation("Public 111, 113 and 115: a host write of 1 reads back 0, because PinMAME rewrites the end-of-stroke bits of the FLIP_SOL flippers from their coil state on every update, and T.1 names nothing", [111, 113, 115], set()))
	named.append(_observation("Public 117 (F7) round-trips at 1 and T.1 names nothing for it; its last-switch line stays at F5", [117], set()))
	command = (
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 1.5 s; the snapshot after it records the ROM's T.1 "
		"display and the watched public switch levels. The ROM names a switch on its top line on the edge it treats as active. PinMAME's "
		f"nfGameData mask inverts public {', '.join(map(str, PINMAME_MASKED))}; every one of them is named at public 1."
	)
	return _result(run, readings, named, frozenset(f"{address} -> 1" for address in SWEPT)), command


def build_solenoids(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	named = []
	for index, address in enumerate(T4_ORDER, start=1):
		name, wires = T4_NAMES[address]
		label = f"T.4 Up {len(T4_ORDER)}" if index == 1 else f"T.4 Up {index - 1}"
		readings[label] = f"{name} / T.4 {address:02d} REPEAT / {wires}"
		if index == 1:
			selected = _named_coils(_step(run, "Enter (start T.4)"))
			late = _named_coils(_step(run, "T.4 Up 1"))
		else:
			selected = _named_coils(_step(run, f"T.4 Up {index - 1}")) | _named_coils(_step(run, f"T.4 after Up {index - 1}"))
			late = _named_coils(_step(run, f"T.4 Up {index}"))
		previous = T4_ORDER[index - 2] if index > 1 else None
		if not selected <= {address, previous} or address not in selected | late:
			raise ValueError(f"T.4 item {index} ({address}) published {sorted(selected)} then {sorted(late)}")
		named.append(_observation(f"T.4 SOLENOID TEST item {index} selects {address:02d} ({name}, {wires}): the ROM pulses public {address} repeatedly", [8 if index == 1 else 7], {address}))
	wrap = _named_coils(_step(run, f"T.4 Up {len(T4_ORDER)}")) | _named_coils(_step(run, f"T.4 after Up {len(T4_ORDER)}"))
	if 1 not in wrap:
		raise ValueError("T.4 must wrap to solenoid 1 after 16")
	command = (
		"Each Up press selects the next T.4 item; in repeat mode the ROM pulses it until the next press. The test walks 01-16, "
		"offering 09 and 13 as UNUSED, and wraps to 01. A frame is taken while each press is held, after its 2.5 s settle and 0.7 s "
		"later; the one after the settle is read (item 01 from the wrap-around press)."
	)
	return _result(run, readings, named), command


def build_flashers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	named = []
	for index, address in enumerate(T5_ORDER, start=1):
		name, wires = T5_NAMES[address]
		readings[f"T.5 item {index} frame {T5_FRAME[index]}"] = f"{name} / T.5 {address} REPEAT / {wires}"
		labels = ["Enter (start T.5)"] if index == 1 else [f"T.5 Up {index - 1}"]
		labels += [f"T.5 item {index} frame {frame}" for frame in range(6)]
		risen = set().union(*(_named_coils(_step(run, label)) for label in labels))
		previous = T5_ORDER[index - 2] if index > 1 else None
		if address not in risen or not risen <= {address, previous}:
			raise ValueError(f"T.5 item {index} published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.5 FLASHER TEST item {index} selects {address} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 1 else 7], {address}))
	wrap = set().union(*(_named_coils(_step(run, label)) for label in [f"T.5 Up {len(T5_ORDER)}"] + [f"T.5 item {len(T5_ORDER) + 1} frame {frame}" for frame in range(6)]))
	if 17 not in wrap:
		raise ValueError("T.5 must wrap to 17 after 28")
	return _result(run, readings, named), "Each Up press selects the next flasher; six frames 0.25 s apart catch the blinking name lit. The test walks 17-28 and wraps to 17."


def build_flippers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	named = []
	for position, (number, name, wires, published) in enumerate(T12_ORDER, start=1):
		label = f"T.12 Up {len(T12_ORDER)} (held)" if position == 1 else f"T.12 Up {position - 1} (held)"
		readings[label] = f"{name} / T.12 {number:02d} REPEAT / {wires}"
		labels = ["Enter (start T.12)"] if position == 1 else [f"T.12 Up {position - 1}", f"T.12 after Up {position - 1}"]
		risen = set().union(*(_named_coils(_step(run, label)) for label in labels))
		if risen != published:
			raise ValueError(f"T.12 item {number} published {sorted(risen)}, not {sorted(published)}")
		named.append(_observation(f"T.12 FLIPPER COIL TEST item {number:02d} {name} ({wires}) drives public {', '.join(map(str, sorted(published)))}", [8 if position == 1 else 7], risen))
	if _named_coils(_step(run, f"T.12 Up {len(T12_ORDER)}")) != {45, 46}:
		raise ValueError("T.12 must wrap to the right flipper power item")
	command = (
		"The test walks items 01-06 (power drives both windings, hold the hold winding) and wraps; it offers no upper-left item, "
		"so nothing drives 35 or 36. The frame taken while each press is held is read (the name blinks; item 01 from the wrap-around press)."
	)
	return _result(run, readings, named), command


def build_gi(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	readings["T.6 Up 1 (held)"] = "ALL ILLUMINATION / T.6 BRIGHT=2 STOP"
	named = []
	for press in range(1, 7):
		if _changed(_step(run, f"T.6 Up {press}"), "gis") != {0, 1, 2, 3, 4}:
			raise ValueError("T.6 ALL ILLUMINATION must dim public GI 0-4 together")
	named.append(_observation("T.6 ALL ILLUMINATION steps the brightness of public GI 0, 1, 2, 3 and 4 together", [8], set()))
	for channel, label, text, presses in GI_STRINGS:
		readings[label] = text
		changed = [_changed(_step(run, f"T.6 Up {press}"), "gis") for press in presses]
		if any(item != {channel} for item in changed):
			raise ValueError(f"T.6 {text} must dim public GI {channel} alone, saw {changed}")
		named.append(_observation(f"T.6 {text.split(' / ')[0]} ({text.split(' / ')[-1]}): Up steps the brightness of public GI {channel} alone", [7], set()))
	return _result(run, readings, named), "T.6 stop mode first steps all illumination through its brightness levels, then each string in turn; every string dims."


def _lamp_reading(step: int, address: int) -> str:
	column, row = divmod(address, 10)
	return f"{LAMP_NAMES[address]} / T.8 {step:02d} LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"


def build_lamps(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base()
	for step, address in enumerate(MATRIX_LAMPS, start=1):
		label = "T.8 Up 64 (held)" if step == 1 else f"T.8 Up {step - 1} (held)"
		readings[label] = _lamp_reading(step, address)
		step_label = "Enter (start T.8)" if step == 1 else f"T.8 Up {step - 1}"
		previous = MATRIX_LAMPS[step - 2] if step > 1 else None
		window = _step(run, step_label)
		risen = _risen(window, "lamps")
		if address not in risen or not risen <= {address, previous}:
			raise ValueError(f"T.8 step {step} must light public lamp {address} and no lamp but the one it leaves, saw {sorted(risen)}")
		if previous is not None and (_states(window, "lamps", previous) or [0])[-1] != 0:
			raise ValueError(f"T.8 step {step} must leave lamp {previous} off")
		if not set(_snapshot(run, label)["active_lamps"]) <= {address}:
			raise ValueError(f"T.8 step {step} shows lamps other than {address} lit")
	if 11 not in _risen(_step(run, "T.8 Up 64"), "lamps"):
		raise ValueError("T.8 must wrap to lamp 11 after 88")
	named = [_observation("T.8 SINGLE LAMPS TEST lights public lamps 11-88 one at a time in matrix order while printing each name, its number and its row and column wires, and wraps to lamp 11", [7], set())]
	return _result(run, readings, named), "Each Up press, held 0.4 s, selects the next lamp; the frame taken while it is held is read (lamp 11 from the wrap-around press)."


def build_accelerator(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(), **ACCELERATOR_READINGS}
	for label in ACCELERATOR_SILENT:
		if _named_coils(_step(run, label)):
			raise ValueError(f"T.16 {label!r} must fire no coil")
	named = []
	for label, coil in ACCELERATOR_PULSES:
		address = int(label.split()[0])
		risen = _named_coils(_step(run, label))
		if risen != ({coil} if coil else set()):
			raise ValueError(f"T.16 {label!r} published {sorted(risen)}, expected {coil}")
		if coil:
			if _states(_step(run, label), "solenoids", coil) != [1, 0]:
				raise ValueError(f"T.16 {label!r} must pulse public {coil} exactly once and release it")
			named.append(_observation(f"T.16 with the magnet enabled, a 150 ms pulse of ramp opto {address} ({label}) makes the ROM fire public {coil} once", [address], {coil}))
		else:
			named.append(_observation(f"T.16 with that magnet disabled, a pulse of ramp opto {address} ({label}) fires nothing", [address], set()))
	command = (
		"The test starts with all three magnets enabled and LEFT selected; Up selects the next magnet and Enter toggles the selected "
		"one. The host pulses each ramp opto at public 1 for 150 ms; the ROM answers left opto 46 with public 6, centre opto 47 with 5 "
		"and right opto 48 with 3, each only while its magnet is enabled. Readings describe the icons: a magnet symbol, filled while "
		"the coil is energized, or a cross for a disabled magnet with a bar while its opto is blocked; 'boxed' is the selection frame."
	)
	return _result(run, readings, named), command


def build_trough(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(), **TROUGH_READINGS}
	start = _named_coils(_step(run, "Enter (start T.18, MANUAL)"))
	left = _named_coils(_step(run, "MANUAL 38 -> 1"))
	if start != {8} or left != {8}:
		raise ValueError(f"T.18 MANUAL must pulse public 8 as it starts and when 38 closes, saw {sorted(start)} and {sorted(left)}")
	quiet = ["MANUAL 38 -> 0"] + [f"MANUAL {address} -> {level}" for address in (37, 42, 41) for level in (1, 0)] + [f"trough {address} -> 1" for address in (32, 33, 34, 35)]
	if any(_named_coils(_step(run, label)) for label in quiet):
		raise ValueError("T.18 MANUAL must fire nothing for 37, 42, 41 or the loaded trough")
	for label, expected in TROUGH_CYCLE:
		risen = _named_coils(_step(run, label))
		if risen != expected:
			raise ValueError(f"T.18 AUTOMATIC {label!r} published {sorted(risen)}, expected {sorted(expected)}")
	labels = [item["label"] for item in run["steps"]]
	for coil, start, release in TROUGH_HOLDS:
		first, last = labels.index(start), labels.index(release)
		window = [_states(step, "solenoids", coil) for step in run["steps"][first:last + 1]]
		if last <= first or window[0] != [1] or window[-1] != [0] or any(window[1:-1]):
			raise ValueError(
				f"T.18 must hold public {coil} on from {start!r} without interruption and release it on {release!r}, saw {window}"
			)
	named = [
		_observation("T.18 UNDERGROUND TROUGH TEST starts in MANUAL and pulses public 8 (drop target down) repeatedly; closing the left trough entrance 38 pulses 8 again", [8, 38], {8}),
		_observation("In MANUAL the display marks LEFT ENTR., CTR. ENTR., POPPER 2 and POPPER 1 while host public 38, 37, 42 and 41 are 1; 37, 42 and 41 fire nothing", [38, 37, 42, 41], set()),
		_observation("Switched to AUTOMATIC with the trough loaded (32-35 at public 1), the ROM fires the trough eject, public 14, and holds it until trough 4 (35) opens", [8, 35], {14}),
		_observation("With the shooter lane switch 15 closed the ROM fires the auto plunger, public 2, and drops it when 15 opens", [15], {2}),
		_observation("After the left (38) and centre (37) trough entrances and right popper opto 2 (42) are pulsed, holding right popper opto 1 (41) makes the ROM fire the right popper, public 1, until 41 opens; it then fires the trough eject 14 for the next ball", [38, 37, 42, 41], {1, 14}),
	]
	command = (
		"Built-in mechanisms stay disabled, so the host plays the ball: it loads the trough, releases trough 4 after the eject, closes "
		"the shooter lane until the auto plunger fires, and pulses the underground trough switches in the order a ball passes them."
	)
	return _result(run, readings, named), command


def build_skull(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(), **SKULL_READINGS}
	risen = set().union(*(_named_coils(_step(run, f"T.19 frame {frame}")) for frame in range(8)))
	if risen != {16, 21}:
		raise ValueError(f"T.19 must drive public 16 and 21 only, saw {sorted(risen)}")
	for coil in sorted(risen):
		states = [state for frame in range(8) for state in _states(_step(run, f"T.19 frame {frame}"), "solenoids", coil)]
		pulses = sum(1 for before, after in zip(states, states[1:]) if before and not after)
		if pulses < 2 or any(before == after for before, after in zip(states, states[1:])):
			raise ValueError(f"T.19 must pulse public {coil} on and off repeatedly, saw {states}")
	named = [_observation("T.19 SKULL TEST pulses the skull mouth coil, public 16, and the skull flashers, public 21, repeatedly and drives no other coil", [8], risen)]
	return _result(run, readings, named), "Eight frames 1 s apart; the display shows SKULL TEST throughout, and the run does not record sound."


Builder = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]
RUNS: dict[str, tuple[str, Builder]] = {
	"no-fear-nf_23x-switch-edges.json": ("nf-switch-edges", build_edges),
	"no-fear-nf_23x-solenoid-test.json": ("nf-solenoid-test", build_solenoids),
	"no-fear-nf_23x-flasher-names.json": ("nf-flasher-names", build_flashers),
	"no-fear-nf_23x-flipper-coil-test.json": ("nf-flipper-coil-test", build_flippers),
	"no-fear-nf_23x-gi-test.json": ("nf-gi-test", build_gi),
	"no-fear-nf_23x-single-lamps.json": ("nf-single-lamps", build_lamps),
	"no-fear-nf_23x-ball-accelerator-test.json": ("nf-ball-accelerator-test", build_accelerator),
	"no-fear-nf_23x-underground-trough-test.json": ("nf-underground-trough-test", build_trough),
	"no-fear-nf_23x-skull-test.json": ("nf-skull-test", build_skull),
}


def _check_pinned_frames(filename: str, observations: dict[str, Any]) -> None:
	pinned = json.loads(FRAME_SEED_PATH.read_bytes())[filename]
	read = {item["label"]: {"pixel_sha256": item["pixel_sha256"], "reading": item["interpreted_text"]} for item in observations["diagnostic_snapshots"]}
	if read != pinned:
		changed = sorted(label for label in set(read) | set(pinned) if read.get(label) != pinned.get(label))
		raise ValueError(f"{filename}: readings or frames differ from the pinned seed at {changed[:5]}")


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, (directory, builder) in RUNS.items():
		path = review_root / HARNESS_DIRECTORY / directory
		check_manifest(path, GAME)
		run = _load_run(path, directory)
		observations, command = builder(run)
		_check_pinned_frames(filename, observations)
		document = _document(filename.removeprefix("no-fear-").removesuffix(".json"), directory, directory, run, observations, command)
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
			raise ValueError(f"No Fear compact runtime evidence drift: {path}")


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
		print("No Fear compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
