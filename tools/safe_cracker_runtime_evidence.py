"""Derive the compact Safe Cracker runtime evidence from the retained raw harness runs.

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
MACHINE_ID = "bally.safe-cracker.1996"
GAME = "sc_18s11"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "e3a65641cb5957e11354aa7a538325849aeff672d4e80d98e7fd08b71d38ebdc"
HARNESS_DIRECTORY = "safe-cracker-1996/harness"
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
IDENTIFICATION_LABEL = "Enter 1 (game identification)"
IDENTIFICATION = "SAFE CRACKER / 90003 REV. 1.8"
COMMAND = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game sc_18s11 --rom-path <vpinmame-roms> "
	"--work-dir <new-isolated-state> --handle-mechanics {mech} --scenario {scenario} --dmd-dir <external-dmd-dir> --output <external-run.json>. "
)
# The LPDC lines 37-40 (and their 41-44 mirrors) carry the serial auxiliary-lamp stream in every menu, and 29/31 are PinMAME's
# state channels; observations about named coils ignore them.
BACKGROUND = frozenset({29, 31, 37, 38, 39, 40, 41, 42, 43, 44})

# --- T.1 SWITCH EDGES sweep ----------------------------------------------------------------------------
# The name the ROM prints on the top display line while it reads the switch as active (read from the retained frames).
EDGE_NAMES = {
	11: "TP TROUGH (ROOF)", 12: "TP TROUGH (MOVE)", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "RIGHT ORBIT", 16: "LEFT OUTLANE",
	17: "RIGHT OUTLANE", 18: "BALLSHOOTER", 21: "SLAM TILT", 22: "COIN DOOR CLOSED", 23: "UNUSED", 24: "ALWAYS CLOSED",
	25: "UR FLIP ROLLOVER", 26: "LEFT RETURN", 27: "RIGHT RETURN", 28: "LEFT ORBIT", 31: "TROUGH EJECT *", 32: "TROUGH BALL 1 *",
	33: "TROUGH BALL 2 *", 34: "TROUGH BALL 3 *", 35: "TROUGH BALL 4 *", 36: "LOCKUP 1 FRONT *", 37: "LOCKUP 2 REAR *", 38: "UNUSED",
	41: "KICKBACK *", 42: "LEFT BIG KICK *", 43: "TOKN CHUTE EXIT*", 44: "LEFT JET", 45: "RIGHT JET", 46: "TOP JET",
	47: "LEFT SLINGSHOT", 48: "RIGHT SLINGSHOT", 51: "(A)LARM STANDUP", 52: "A(L)ARM STANDUP", 53: "AL(A)RM STANDUP",
	54: "ALA(R)M STANDUP", 55: "ALAR(M) STANDUP", 56: "MOVNG TARGET C", 57: "MOVNG TARGET B", 58: "MOVNG TARGET A",
	61: "TL 3BANK TOP", 62: "TL 3BANK MIDDLE", 63: "TL 3BANK BOTTOM", 64: "TR 3BANK BOTTOM", 65: "TR 3BANK MIDDLE", 66: "TR 3BANK TOP",
	67: "TOP LEFT LANE", 68: "TOP POPPER", 71: "BL 3BANK TOP", 72: "BL 3BANK MIDDLE", 73: "BL 3BANK BOTTOM", 74: "BR 3BANK BOTTOM",
	75: "BR 3BANK MIDDLE", 76: "BR 3BANK TOP", 77: "BANK KICKOUT", 78: "TOP RIGHT LANE", 81: "LEFT TOKEN LVL.", 82: "RIGHT TOKEN LVL.",
	83: "RAMP ENTRANCE", 84: "RAMP MADE", 85: "WHEEL CHANNEL A", 86: "WHEEL CHANNEL B", 87: "UNUSED", 88: "UNUSED",
}
# The ROM names these on the 1 -> 0 edge instead: 24 rests at public 1 from power-up, and 43 is masked by PinMAME.
NAMED_AT_ZERO = frozenset({24, 43})
# The wire colours the ROM prints for a matrix switch: row wire first, then the column wire.
EDGE_ROW_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
EDGE_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "YEL", 5: "BLK", 6: "BLU", 7: "VIO", 8: "GRY"}
# Fliptronic column: printed position, wire, and the name the ROM shows while the host holds the address at 1 (None: no name).
FLIPPER_EDGES = {
	111: ("F1", "BLK-GRN ORN", None), 112: ("F1", "BLK-GRN ORN", "R FLIPPER EOS"), 113: ("F3", "BLK-BLU ORN", None),
	114: ("F3", "BLK-BLU ORN", "L FLIPPER EOS"), 115: ("F5", "BLK-VIO ORN", None), 116: ("F5", "BLK-VIO ORN", "UR FLIPPER EOS"),
	117: ("F5", "BLK-VIO ORN", None), 118: ("F8", "BLK-BLU ORN", "TOKEN COIN SLOT"),
}
SWEPT = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9)) + tuple(range(111, 119))
# PinMAME rewrites the end-of-stroke bits of the flippers scGameData declares with FLIP_SOL (lower pair and upper right).
SYNTHESIZED = frozenset({111, 113, 115})
# Fliptronic button positions whose closure makes the ROM fire flipper windings.
FLIPPER_FIRES = {112: {45, 46}, 114: {47, 48}, 116: {33, 34, 45, 46}}
# Playfield switches whose closure makes the ROM fire their own coil even inside T.1 (jet bumpers and slingshots).
SWITCH_FIRES = {44: (12, "left jet bumper"), 45: (13, "right jet bumper"), 46: (14, "top jet bumper"), 47: (10, "left slingshot"), 48: (11, "right slingshot")}
PINMAME_MASKED = (31, 32, 33, 34, 35, 36, 37, 42, 43, 56, 57, 58, 61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76)


def _matrix_wires(address: int) -> str:
	column, row = divmod(address, 10)
	return f"WHT-{EDGE_ROW_WIRES[row]} GRN-{EDGE_COLUMN_WIRES[column]}"


def _edge_reading(address: int, level: int) -> str:
	idle = "SWITCH EDGES"
	if address in FLIPPER_EDGES:
		position, wires, name = FLIPPER_EDGES[address]
		return f"{name if level and name else idle} / T.1 LAST SW {position} / {wires}"
	if address in NAMED_AT_ZERO:
		if level == 0:
			return f"{EDGE_NAMES[address]} / T.1 LAST SW {address} / {_matrix_wires(address)}"
		previous = address - 1
		return f"{idle} / T.1 LAST SW {previous} / {_matrix_wires(previous)}"
	return f"{EDGE_NAMES[address] if level else idle} / T.1 LAST SW {address} / {_matrix_wires(address)}"


# --- T.4 SOLENOID TEST, T.5 FLASHER TEST, T.12 FLIPPER COIL TEST, T.6 GI, T.8 LAMPS ----------------------
T4_ORDER = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 25, 26, 27, 28, 35, 36)
T4_NAMES = {
	1: ("BIG KICK", "VIO-BRN RED-BRN"), 2: ("RIGHT TOKEN TUBE", "VIO-RED RED-BRN"), 3: ("MOVE TGT. RESET", "VIO-ORN RED-BRN"),
	4: ("LEFT TOKEN TUBE", "VIO-YEL RED-BRN"), 5: ("BANK KICK", "VIO-GRN RED-BRN"), 6: ("TOP POPPER UP", "VIO-BLU RED-BRN"),
	7: ("RAMP DIVERTOR", "VIO-BLK RED-BRN"), 8: ("KICKBACK (RAMP)", "VIO-GRY RED-BRN"), 9: ("TROUGH EJECT", "BRN-BLK RED-BLK"),
	10: ("LEFT SLINGSHOT", "BRN-RED RED-BLK"), 11: ("RIGHT SLINGSHOT", "BRN-ORN RED-BLK"), 12: ("LEFT JET", "BRN-YEL RED-BLK"),
	13: ("RIGHT JET", "BRN-GRN RED-BLK"), 14: ("TOP JET", "BRN-BLU RED-BLK"), 15: ("TOP. L. 3 BANK", "BRN-VIO RED-BLK"),
	16: ("TOP. R. 3 BANK", "BRN-GRY RED-BLK"), 25: ("TOP POPPER EJECT", "BLU-BRN RED-ORN"), 26: ("TOP LIGHT+MOTOR", "BLU-RED RED-ORN"),
	27: ("BOT. L. 3 BANK", "BLU-ORN RED-ORN"), 28: ("BOT. R. 3 BANK", "BLU-YEL RED-ORN"), 35: ("AUTO PLUNGER", "YEL-GRY RED-GRY"),
	36: ("LOCKUP RELEASE", "ORN-GRY RED-GRY"),
}
T4_LABELS = {1: "Enter (start T.4 SOLENOID TEST, repeat mode)", 17: "T.4 item 17 frame 0", 21: "T.4 item 21 frame 0"}
T5_ORDER = (17, 18, 19, 20, 21, 22, 23, 24)
T5_NAMES = {
	17: ("BACK LEFT", "BLK-BRN RED-WHT"), 18: ("JETS + BK RT. (2)", "BLK-RED RED-WHT"), 19: ("RIGHT MIDDLE", "BLK-ORN RED-WHT"),
	20: ("RIGHT BOTTOM", "BLK-YEL RED-WHT"), 21: ("LEFT MIDDLE", "BLU-GRN RED-WHT"), 22: ("LEFT BOTTOM", "BLU-BLK RED-WHT"),
	23: ("LIGHT ROPE 1", "BLU-VIO RED-WHT"), 24: ("LIGHT ROPE 2", "BLU-GRY RED-WHT"),
}
T12_ORDER = (
	(1, "R. FLIP. POWER", "YEL-GRN RED-GRN", {45, 46}), (2, "R. FLIP. HOLD", "ORN-GRN RED-GRN", {46}),
	(3, "L. FLIP. POWER", "YEL-BLU RED-BLU", {47, 48}), (4, "L. FLIP. HOLD", "ORN-BLU RED-BLU", {48}),
	(5, "U.R. FLIP. POWER", "YEL-VIO RED-VIO", {33, 34}), (6, "U.R. FLIP. HOLD", "ORN-VIO RED-VIO", {34}),
)
# T.6: the item whose frame names each string, its printed mode and wires, and the public GI channel the next items dim alone.
GI_STRINGS = (
	(9, "ILLUM. STRING 1", "BRIGHT=1", "WHT-BRN BRN", 0), (17, "AUX. LAMP 1 POWER", "BRIGHT=1", "WHT-ORN ORN", 1),
	(25, "ILLUM. STRING 3", "BRIGHT=1", "WHT-YEL YEL", 2), (33, "AUX. LAMP 2 POWER", "ON ONLY", "WHT-GRN GRN", 3),
	(34, "AUX. LAMP 3 POWER", "ON ONLY", "WHT-VIO VIO", 4),
)
LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
MATRIX_LAMPS = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
AUX_LAMPS = tuple(column * 10 + row for column in range(9, 15) for row in range(1, 9))
# T.8 SINGLE LAMPS names, read from the retained frames (the name line blinks; each step's lit frame is pinned).
LAMP_NAMES = {
	11: "LITE DEPOSIT", 12: 'CTR. TIMER "10"', 13: "DISABLE COMPUTER", 14: 'CTR. TIMER "5"', 15: 'CTR. TIMER "0"', 16: "LITE LOCK",
	17: 'CTR. TIMER "55"', 18: 'CTR. TIMER "50"', 21: 'CTR. TIMER "15"', 22: 'CTR. TIMER "20"', 23: 'CTR. TIMER "25"', 24: 'CTR. TIMER "30"',
	25: 'CTR. TIMER "35"', 26: "CALL GUARD", 27: 'CTR. TIMER "45"', 28: 'CTR. TIMER "40"', 31: "ARMOR CAR-CELLAR", 32: "ARMOR CAR-ROOF",
	33: "ARMOR CAR-MAIN", 34: "BONUS 2X", 35: "(A)LARM STANDUP", 36: "ATM CARD", 37: "A(L)ARM STANDUP", 38: "RAMP JACKPOT",
	41: "BONUS 5X+OUTLANE", 42: "BONUS 5X", 43: "BONUS 4X", 44: "BONUS 3X", 45: "RAMP LOCK", 46: "AL(A)RM STANDUP", 47: "ALA(R)M STANDUP",
	48: "ALAR(M) STANDUP", 51: "WHEEL ARROW", 52: "LITE OUTLANES", 53: "VAULT LETTER", 54: "EXPLOSIVES", 55: "NOTE TO TELLER",
	56: "TOP LEFT LANE", 57: "TOP MIDDLE LANE", 58: "TOP RIGHT LANE", 61: "TR. 3BANK TOP", 62: "TR. 3BANK MIDDLE", 63: "TR. 3BANK BOTTOM",
	64: "TL. 3BANK TOP", 65: "TL. 3BANK MIDDLE", 66: "TL. 3BANK BOTTOM", 67: 'RT. "EXTRA TIME"', 68: "RIGHT RETURN", 71: "BR. 3BANK TOP",
	72: "BR. 3BANK MIDDLE", 73: "BR. 3BANK BOTTOM", 74: "BL. 3BANK TOP", 75: "BL. 3BANK MIDDLE", 76: "BL. 3BANK BOTTOM", 77: "LEFT RETURN",
	78: 'LT. "EXTRA TIME"', 81: "TOP JET (YELLOW)", 82: "LEFT JET (CLEAR)", 83: "RIGHT JET (RED)", 84: "BANK LEFT", 85: "BANK RIGHT",
	86: "MOVNG BREAK IN", 87: "ROOF BREAK IN", 88: "START BUTTON",
}
# Auxiliary P.C.B. lamps: public address -> (L number, quoted name, the lamp-power wire the ROM prints).
AUX_LAMP_NAMES = {
	91: (24, "!", "WHT-VIO"), 92: (23, "TELLER", "WHT-VIO"), 93: (22, "DOG", "WHT-VIO"), 94: (21, "?", "WHT-VIO"), 95: (20, "ALARM 3", "WHT-VIO"),
	96: (19, "$", "WHT-VIO"), 97: (18, "DOG", "WHT-VIO"), 98: (17, "CANDY", "WHT-VIO"), 101: (16, "$", "WHT-VIO"), 102: (15, "?", "WHT-VIO"),
	103: (14, "ALARM 2", "WHT-VIO"), 104: (13, "#", "WHT-VIO"), 105: (12, "<-->", "WHT-VIO"), 106: (11, "TELLER", "WHT-VIO"),
	107: (10, "BRIBE", "WHT-VIO"), 108: (9, "?", "WHT-VIO"), 111: (8, "ALARM 1", "WHT-GRN"), 112: (7, "$", "WHT-GRN"), 113: (6, "DOG", "WHT-GRN"),
	114: (5, "CANDY", "WHT-GRN"), 115: (4, "$", "WHT-GRN"), 116: (3, "?", "WHT-GRN"), 117: (2, "ALARM 4", "WHT-GRN"), 118: (1, "$", "WHT-GRN"),
	121: (48, "BRIBE", "WHT-GRN"), 122: (47, "?", "WHT-GRN"), 123: (46, "$", "WHT-GRN"), 124: (45, "?", "WHT-GRN"), 125: (44, "CELLAR", "WHT-GRN"),
	126: (43, "$", "WHT-GRN"), 127: (42, "?", "WHT-GRN"), 128: (41, "?", "WHT-GRN"), 131: (40, "VAULT", "WHT-ORN"), 132: (39, "GATE 1", "WHT-ORN"),
	133: (38, "?", "WHT-ORN"), 134: (37, "GATE 2", "WHT-ORN"), 135: (36, "?", "WHT-ORN"), 136: (35, "GATE 3", "WHT-ORN"), 137: (34, "GATE 4", "WHT-ORN"),
	138: (33, "?", "WHT-ORN"), 141: (32, "?", "WHT-ORN"), 142: (31, "BRIBE", "WHT-ORN"), 143: (30, "ROOF", "WHT-ORN"), 144: (29, "BRIBE", "WHT-ORN"),
	145: (28, "$", "WHT-ORN"), 146: (27, "?", "WHT-ORN"), 147: (26, "$", "WHT-ORN"), 148: (25, "MAIN", "WHT-ORN"),
}


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
		raise ValueError(f"not a successful Safe Cracker {GAME} run: {run_path}")
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


def _named_coils(step: dict[str, Any]) -> set[int]:
	return _risen(step) - BACKGROUND


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


def _observation(label: str, inputs: list[int], solenoids: set[int] | list[int]) -> dict[str, Any]:
	return {
		"active_solenoid_addresses": [],
		"host_stimulus_switch_addresses": inputs, "input_address": inputs[0], "input_kind": "switch",
		"label": label, "observed_switch_addresses": [], "result": "observed",
		"transitioned_solenoid_addresses": sorted(solenoids),
	}


def _document(name: str, directory: str, scenario: str, mechanics: int, run: dict[str, Any], observations: dict[str, Any], command: str) -> dict[str, Any]:
	return {
		"driver_ids": [GAME],
		"extractor": {"id": "tools/safe_cracker_runtime_evidence.py", "version": 1},
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


def _base(run: dict[str, Any]) -> dict[str, str]:
	return {IDENTIFICATION_LABEL: IDENTIFICATION}


# --- Builders ------------------------------------------------------------------------------------------
def build_edges(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for address in SWEPT:
		for level in (1, 0):
			readings[f"{address} -> {level}"] = _edge_reading(address, level)
		held = {item["number"]: item["state"] for item in _snapshot(run, f"{address} -> 1")["watched_switches"]}
		if held[address] != (0 if address in SYNTHESIZED else 1):
			raise ValueError(f"unexpected observed level of {address} after the host wrote 1")
		risen = _named_coils(_step(run, f"{address} -> 1"))
		expected = FLIPPER_FIRES.get(address) or ({SWITCH_FIRES[address][0]} if address in SWITCH_FIRES else set())
		if risen != expected:
			raise ValueError(f"T.1 at public {address} published {sorted(risen)}, expected {sorted(expected)}")
		if address in FLIPPER_FIRES:
			named.append(_observation(
				f"T.1 with host public {address} set to 1: the ROM fires public {', '.join(map(str, sorted(risen)))} and names "
				f"{FLIPPER_EDGES[address][2]!r} ({FLIPPER_EDGES[address][0]}); the hold windings drop at 0", [address], risen))
		elif address in SWITCH_FIRES:
			named.append(_observation(
				f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and the ROM fires the {SWITCH_FIRES[address][1]} coil, "
				f"public {SWITCH_FIRES[address][0]}, on the closure", [address], risen))
		elif address in NAMED_AT_ZERO:
			continue
		elif address in EDGE_NAMES:
			named.append(_observation(f"T.1 names {EDGE_NAMES[address]!r} while host public {address} is 1 and clears it at 0", [address], set()))
		elif address == 118:
			named.append(_observation("T.1 names 'TOKEN COIN SLOT' (F8) while host public 118 is 1 and clears it at 0", [118], set()))
	named.append(_observation("Public 24 rests at 1 from power-up; T.1 shows no new name for the redundant 1 and names 'ALWAYS CLOSED' on the 1 -> 0 edge", [24], set()))
	named.append(_observation("Public 43 rests at 0; T.1 shows no new name when the host sets it to 1 and names 'TOKN CHUTE EXIT*' on the 1 -> 0 edge", [43], set()))
	named.append(_observation("Public 111, 113 and 115: a host write of 1 reads back 0, because PinMAME rewrites the end-of-stroke bits of the FLIP_SOL flippers from their coil state on every update, and T.1 names nothing", [111, 113, 115], set()))
	named.append(_observation("Public 117 (F7) round-trips at 1 and T.1 names nothing for it", [117], set()))
	observations = {
		"diagnostic_snapshots": _diagnostics(run, readings, frozenset(f"{address} -> 1" for address in SWEPT)),
		"named_action_observations": named,
		"solenoid_addresses_seen": _seen(run),
	}
	command = (
		"Built-in mechanisms stay disabled. Each set_switch holds one public level for 2 s; the snapshot after it records the ROM's T.1 "
		"display and the watched public switch levels. The ROM names a switch on its top line on the edge it treats as active, and marks "
		"the ten optos of the 10-opto board with '*'. PinMAME's scGameData mask inverts public "
		f"{', '.join(map(str, PINMAME_MASKED))}; every one of them except 43 is named at public 1."
	)
	return observations, command


def build_solenoids(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for index, address in enumerate(T4_ORDER, start=1):
		step_label = "Enter (start T.4 SOLENOID TEST, repeat mode)" if index == 1 else f"Up (T.4 item {index})"
		name, wires = T4_NAMES[address]
		readings[T4_LABELS.get(index, step_label)] = f"{name} / T.4 {address:02d} REPEAT / {wires}"
		item_steps = [step for step in run["steps"] if step["label"] == step_label or step["label"].startswith(f"T.4 item {index} frame")]
		if index == 1:
			item_steps += [step for step in run["steps"] if step["label"].startswith("T.4 first item frame")]
		risen = set().union(*(_named_coils(step) for step in item_steps))
		if risen != {address}:
			raise ValueError(f"T.4 item {index} ({address}) published {sorted(risen)}")
		named.append(_observation(f"T.4 SOLENOID TEST item {index} selects {address:02d} ({name}, {wires}): the ROM pulses public {address} repeatedly", [8 if index == 1 else 7], risen))
	if _named_coils(_step(run, f"Up (T.4 item {len(T4_ORDER) + 1})")) != {1}:
		raise ValueError("T.4 must wrap to solenoid 1 after 36")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	command = (
		"Each Up press selects the next T.4 item; in repeat mode the ROM pulses it until the next press (26, the top light and motor, "
		"stays on while selected). The test walks 1-16, 25-28, 35 and 36 and wraps to 1. Four frames 0.25 s apart at each item catch "
		"the blinking name in its lit phase."
	)
	return observations, command


def build_flashers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for index, address in enumerate(T5_ORDER, start=1):
		step_label = "Enter (start T.5 FLASHER TEST, repeat mode)" if index == 1 else f"Up (T.5 item {index})"
		name, wires = T5_NAMES[address]
		readings[step_label] = f"{name} / T.5 {address} REPEAT / {wires}"
		risen = _named_coils(_step(run, step_label))
		if risen != {address}:
			raise ValueError(f"T.5 item {index} published {sorted(risen)}, not {address}")
		named.append(_observation(f"T.5 FLASHER TEST item {index} selects {address} ({name}, {wires}): the ROM pulses it repeatedly", [8 if index == 1 else 7], risen))
	if _named_coils(_step(run, "Up (T.5 item 9)")) != {17}:
		raise ValueError("T.5 must wrap to 17 after 24")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next flasher; the test walks 17-24 and wraps to 17."


def build_flippers(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for number, name, wires, published in T12_ORDER:
		step_label = "Enter (start T.12 FLIPPER COIL)" if number == 1 else f"Up (T.12 item {number})"
		readings[step_label] = f"{name} / T.12 {number:02d} REPEAT / {wires}"
		risen = _named_coils(_step(run, step_label))
		if risen != published:
			raise ValueError(f"T.12 item {number} published {sorted(risen)}, not {sorted(published)}")
		named.append(_observation(f"T.12 FLIPPER COIL TEST item {number:02d} {name} ({wires}) drives public {', '.join(map(str, sorted(published)))}", [8 if number == 1 else 7], risen))
	if _named_coils(_step(run, "Up (T.12 item 7)")) != {45, 46}:
		raise ValueError("T.12 must wrap to the right flipper power item")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The test walks the lower right, lower left and upper right flippers (power drives both windings, hold the hold winding) and wraps; it offers no item for 35 and 36."


def build_gi(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	readings["Enter (start T.6 GEN'L ILLUM.)"] = "ALL ILLUMINATION / T.6 BRIGHT=1 STOP"
	named = []
	if _changed(_step(run, "Enter (start T.6 GEN'L ILLUM.)"), "gis") != {0, 1, 2}:
		raise ValueError("T.6 ALL ILLUMINATION must dim public GI 0, 1 and 2 together")
	named.append(_observation("T.6 ALL ILLUMINATION steps the brightness of public GI 0, 1 and 2 together", [8], set()))
	for item, name, mode, wires, channel in GI_STRINGS:
		readings[f"Up (T.6 item {item})"] = f"{name} / T.6 {mode} STOP / {wires}"
		if mode == "BRIGHT=1":
			following = [_changed(_step(run, f"Up (T.6 item {item + offset})"), "gis") for offset in range(1, 6)]
			if any(changed != {channel} for changed in following):
				raise ValueError(f"T.6 {name} must dim public GI {channel} alone, saw {following}")
			named.append(_observation(f"T.6 {name} ({wires}): the next Up presses step the brightness of public GI {channel} alone", [7], set()))
		else:
			named.append(_observation(f"T.6 {name} ({wires}) is printed ON ONLY and steps no brightness", [7], set()))
	for snapshot in run["snapshots"]:
		if not {3, 4} <= set(snapshot["active_gis"]):
			raise ValueError(f"public GI 3 and 4 must stay on throughout, not at {snapshot['label']!r}")
	if any({3, 4} & _changed(step, "gis") for step in run["steps"] if "transitions" in step):
		raise ValueError("public GI 3 and 4 must never change")
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "T.6 stop mode first steps all illumination through eight brightness levels, then each dimmable string; public GI 3 and 4 stay on in every snapshot."


def _lamp_reading(step: int, address: int) -> str:
	number = f"T.8. {step:02d}" if step < 100 else f"T.8.{step}"
	if address in LAMP_NAMES:
		column, row = divmod(address, 10)
		return f"{LAMP_NAMES[address]} / {number} LAMP {address} / RED-{LAMP_ROW_WIRES[row]} YEL-{LAMP_COLUMN_WIRES[column]}"
	lamp, name, wire = AUX_LAMP_NAMES[address]
	return f'L{lamp} "{name}" / {number} AUX P.C.B. / AUX LP {wire}'


def _lamp_label(step: int) -> str:
	return "T.8 step 1 frame 1" if step == 1 else f"Up (T.8 step {step})"


def build_lamps(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	order = MATRIX_LAMPS + AUX_LAMPS
	for step, address in enumerate(order, start=1):
		readings[_lamp_label(step)] = _lamp_reading(step, address)
		labels = ["Enter (start T.8 SINGLE LAMPS)"] if step == 1 else [f"Up (T.8 step {step})"]
		labels += [f"T.8 step {step} frame {frame}" for frame in (0, 1)]
		changed = set().union(*(_changed(_step(run, label), "lamps") for label in labels))
		if address not in changed:
			raise ValueError(f"T.8 step {step} did not light public lamp {address}")
	if 11 not in _changed(_step(run, f"Up (T.8 step {len(order) + 1})"), "lamps") | _changed(_step(run, f"T.8 step {len(order) + 1} frame 0"), "lamps"):
		raise ValueError("T.8 must wrap to lamp 11 after 148")
	named = [
		_observation("T.8 SINGLE LAMPS TEST lights public lamps 11-88 one at a time in matrix order while printing each name, its number and its row and column wires", [7], set()),
		_observation("T.8 then lights public lamps 91-148 one at a time in the same column order, printing them as the AUX P.C.B. lamps L24-L1 (91-118) and L48-L25 (121-148) with each name and the lamp-power wire, and wraps to lamp 11", [7], set()),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each Up press selects the next lamp; the name line blinks, so each step's lit frame is pinned."


MOVING_TARGET_READINGS = {
	"T.16 start frame 0": 'MOVING TARGET TEST 0 / SWITCH "C" (#56) CLOSED / SWITCH "B" (#57) CLOSED / SWITCH "A" (#58) CLOSED / PRESS "ENTER" TO RESET',
	"56 -> 1": 'MOVING TARGET TEST 7 / SWITCH "C" (#56) OPEN / SWITCH "B" (#57) CLOSED / SWITCH "A" (#58) CLOSED / PRESS "ENTER" TO RESET',
	"57 -> 1": 'MOVING TARGET TEST 3 / SWITCH "C" (#56) CLOSED / SWITCH "B" (#57) OPEN / SWITCH "A" (#58) CLOSED / PRESS "ENTER" TO RESET',
	"58 -> 1": 'MOVING TARGET TEST 1 / SWITCH "C" (#56) CLOSED / SWITCH "B" (#57) CLOSED / SWITCH "A" (#58) OPEN / PRESS "ENTER" TO RESET',
	"Enter (reset the moving target)": 'MOVING TARGET TEST 0 / SWITCH "C" (#56) CLOSED / SWITCH "B" (#57) CLOSED / SWITCH "A" (#58) CLOSED / RESETTING MOVING TARGET',
}


def build_moving_target(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **MOVING_TARGET_READINGS}
	reset = _named_coils(_step(run, "Enter (reset the moving target)"))
	if reset != {3}:
		raise ValueError(f"the moving target reset must fire solenoid 3, saw {sorted(reset)}")
	named = [
		_observation("T.16 MOVING TARGET TEST shows switches C (#56), B (#57) and A (#58) CLOSED while the host holds public 56, 57 and 58 at 0, and each one OPEN while the host holds it at 1; the number at the top right reads 0 with all three closed, 7 with C open, 3 with B open and 1 with A open", [56, 57, 58], set()),
		_observation("Enter in T.16 shows RESETTING MOVING TARGET and pulses public 3", [8], reset),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The host sets each moving-target switch to 1 and back with frames at each level, then presses Enter once."


MOVING_TARGET_CODES = {
	"56+57": ("4", "OPEN", "OPEN", "CLOSED"),
	"57+58": ("2", "CLOSED", "OPEN", "OPEN"),
	"56+58": ("6", "OPEN", "CLOSED", "OPEN"),
	"56+57+58": ("5", "OPEN", "OPEN", "OPEN"),
}


def build_moving_target_codes(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), "T.16 start frame 0": MOVING_TARGET_READINGS["T.16 start frame 0"]}
	for combo, (number, c, b, a) in MOVING_TARGET_CODES.items():
		readings[f"{combo} at 1 frame 0"] = f'MOVING TARGET TEST {number} / SWITCH "C" (#56) {c} / SWITCH "B" (#57) {b} / SWITCH "A" (#58) {a} / PRESS "ENTER" TO RESET'
	named = [
		_observation(
			"T.16 MOVING TARGET TEST reads 4 while the host holds public 56 and 57 at 1, 2 for 57 and 58, 6 for 56 and 58 and 5 for all three; "
			"with the single-switch readings of the moving-target test (0 none, 7 for 56, 3 for 57, 1 for 58) the ROM decodes every combination "
			"as the reflected binary (Gray) code of a position 0-7 with 58 (A) as the least significant bit",
			[56, 57, 58], set()),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "The host sets each two- and three-switch combination of 56, 57 and 58 to 1 and back, with frames while held and after release."


def build_tokens(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), "Enter (start T.17 TOKEN TEST)": "TOKEN TUBE DISPENSE TEST / PRESS ENTER TO / DISPENSE A TOKEN"}
	fired = []
	for press in range(1, 5):
		labels = [f"Enter {press} (dispense a token)"] + [f"T.17 after Enter {press} frame {frame}" for frame in range(6)]
		fired.append(set().union(*(_named_coils(_step(run, label)) for label in labels)))
	if any(not item <= {2, 4} for item in fired) or set().union(*fired) != {2, 4} or fired[1] or sum(1 for item in fired if item) != 3:
		raise ValueError(f"T.17 dispenses must fire only the token tubes 2 and 4, and ignore the press during a dispense: {fired}")
	named = [
		_observation("T.17 TOKEN TUBE DISPENSE TEST: each Enter press dispenses through the token tubes, pulsing public 4 (LEFT TOKEN TUBE) and public 2 (RIGHT TOKEN TUBE) one after the other; the second press, which came while the first dispense was still running, fired nothing", [8], {2, 4}),
		_observation("The T.17 display shows no switch state; host writes of 1 and 0 to public 81, 82, 43 and 118 change nothing on it", [81, 82, 43, 118], set()),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Four Enter presses with six frames 0.5 s apart after each, then each token input set to 1 and back."


LIGHT_ROPE_READINGS = {
	"Enter (start T.18 LIGHT ROPE)": "LIGHT ROPE TEST / OFF / USE +/- TO TEST",
	"Up 1 (next rope selection)": 'LIGHT ROPE TEST / LIGHT ROPE 1 / PRESS "ENTER" TO FLASH',
	"Up 2 (next rope selection)": 'LIGHT ROPE TEST / LIGHT ROPE 2 / PRESS "ENTER" TO FLASH',
	"Up 3 (next rope selection)": 'LIGHT ROPE TEST / BOTH / PRESS "ENTER" TO FLASH',
	"T.18 flashing 3 frame 0": 'LIGHT ROPE TEST / BOTH / PRESS "ENTER" STOP FLASHING',
}


def build_light_ropes(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **LIGHT_ROPE_READINGS}
	def selection(index: int) -> set[int]:
		labels = [f"Up {index} (next rope selection)", f"Enter (flash selection {index})", f"Enter (stop selection {index})"]
		labels += [f"T.18 selection {index} frame {frame}" for frame in range(2)] + [f"T.18 flashing {index} frame {frame}" for frame in range(6)]
		return set().union(*(_named_coils(_step(run, label)) for label in labels))
	ropes = [selection(index) for index in (1, 2, 3)]
	if not ({23} <= ropes[0] <= {23, 24} and 24 in ropes[1] and ropes[2] == {23, 24}):
		raise ValueError(f"T.18 must flash 23 for LIGHT ROPE 1, 24 for LIGHT ROPE 2 and both for BOTH: {ropes}")
	named = [
		_observation("T.18 LIGHT ROPE TEST selects LIGHT ROPE 1, LIGHT ROPE 2 and BOTH with Up and flashes them: public 23 is light rope 1, public 24 light rope 2, and BOTH flashes 23 and 24", [7, 8], {23, 24}),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each selection is chosen with Up and started and stopped with Enter; a selection left flashing can still toggle as the next one is chosen."


DROP_BANKS = (
	("LOWER LEFT", ("LOW", 73), ("MID", 72), ("UPR", 71), 27, (74, 75, 76)),
	("UPPER LEFT", ("LOW", 63), ("MID", 62), ("UPR", 61), 15, (64, 65, 66)),
	("UPPER RIGHT", ("UPR", 66), ("MID", 65), ("LOW", 64), 16, (61, 62, 63)),
	("LOWER RIGHT", ("UPR", 76), ("MID", 75), ("LOW", 74), 28, (71, 72, 73)),
)


def _bank_text(name: str, cells: tuple[tuple[str, int], ...], marked: int | None, footer: str) -> str:
	boxes = " ".join(f"[{'x' if address == marked else ' '}] {position}-{address}" for position, address in cells)
	return f"DROP TARGET TEST / {name} BANK ACTIVE / {boxes} / {footer}"


def build_drop_targets(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = _base(run)
	named = []
	for index, (name, *cells, reset_coil, lamps) in enumerate(DROP_BANKS, start=1):
		cells = tuple(cells)
		entry = "Enter (start T.19 DROP TARGET)" if index == 1 else f"Up (bank {index})"
		readings[entry] = _bank_text(name, cells, None, 'PRESS "ENTER" TO RESET')
		for position, address in cells:
			readings[f"{address} -> 1"] = _bank_text(name, cells, address, 'PRESS "ENTER" TO RESET')
		readings[f"Enter (reset bank {index})"] = _bank_text(name, cells, None, "RESETTING DROP TARGETS")
		fired = _named_coils(_step(run, f"Enter (reset bank {index})"))
		if fired != {reset_coil}:
			raise ValueError(f"T.19 {name} reset must fire {reset_coil}, saw {sorted(fired)}")
		flashing = {item for item in _changed(_step(run, f"Enter (reset bank {index})"), "lamps") if item < 91}
		if flashing != set(lamps):
			raise ValueError(f"T.19 {name} must flash lamps {lamps}, saw {sorted(flashing)}")
		addresses = [address for _, address in cells]
		named.append(_observation(
			f"T.19 {name} BANK: the ROM shows {', '.join(f'{position}-{address}' for position, address in cells)}, marks each target while the host holds it at 1, "
			f"flashes lamps {', '.join(map(str, lamps))} and fires public {reset_coil} on Enter", addresses, fired))
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Up selects the next bank; each target switch is held at 1 and released, and Enter fires the selected bank's reset coil."


TOP_TROUGH_READINGS = {
	"Enter (start T.20 TOP TROUGH)": "TOP TROUGH TEST / [ ] TOP BALL POPPER-68 / [ ] TR1-11 [ ] TR2-12 [ ] TR3-77 / PUT BALL IN TOP POPPER",
	"68 -> 1": "TOP TROUGH TEST / [x] TOP BALL POPPER-68 / [ ] TR1-11 [ ] TR2-12 [ ] TR3-77 / KICKING BALL FROM POPPER",
	"77 -> 1": "TOP TROUGH TEST / [ ] TOP BALL POPPER-68 / [x] TR1-11 [x] TR2-12 [x] TR3-77 / KICKING BALL FROM EJECT",
}


def build_top_trough(run: dict[str, Any]) -> tuple[dict[str, Any], str]:
	readings = {**_base(run), **TOP_TROUGH_READINGS}
	popper = set().union(*(_named_coils(_step(run, f"T.20 ball in popper frame {frame}")) for frame in range(10)))
	bank = set().union(*(_named_coils(_step(run, f"T.20 ball at bank frame {frame}")) for frame in range(10)))
	if popper != {6} or bank != {5}:
		raise ValueError(f"T.20 must fire 6 for the popper and 5 for the bank kickout: {sorted(popper)}, {sorted(bank)}")
	named = [
		_observation("T.20 TOP TROUGH TEST shows TOP BALL POPPER-68 and the underground trough switches TR1-11, TR2-12 and TR3-77; while the host holds public 68 at 1 the ROM shows KICKING BALL FROM POPPER and pulses public 6 (TOP POPPER UP) repeatedly", [68], popper),
		_observation("While the host holds public 77 at 1 the ROM shows KICKING BALL FROM EJECT and pulses public 5 (BANK KICK) repeatedly", [77], bank),
	]
	observations = {"diagnostic_snapshots": _diagnostics(run, readings), "named_action_observations": named, "solenoid_addresses_seen": _seen(run)}
	return observations, "Each of 68, 11, 12 and 77 is set to 1 and back; then 68 and 77 are each held at 1 for 5 s to watch the coil the ROM fires. The TR boxes latch after release (at '77 -> 1' the boxes of 11 and 12, released before, are still marked), so the boxes are not read as levels; the coils are read from the transitions."


Builder = Callable[[dict[str, Any]], tuple[dict[str, Any], str]]
RUNS: dict[str, tuple[str, str, int, Builder]] = {
	"safe-cracker-sc_18s11-switch-edges-sweep.json": ("switch-edges-sweep", "sc-switch-edges-sweep", 0, build_edges),
	"safe-cracker-sc_18s11-solenoid-test.json": ("solenoid-test", "sc-solenoid-test", 0, build_solenoids),
	"safe-cracker-sc_18s11-flasher-test.json": ("flasher-test", "sc-flasher-test", 0, build_flashers),
	"safe-cracker-sc_18s11-flipper-coil-test.json": ("flipper-coil-test", "sc-flipper-coil-test", 0, build_flippers),
	"safe-cracker-sc_18s11-gi-test.json": ("gi-test", "sc-gi-test", 0, build_gi),
	"safe-cracker-sc_18s11-single-lamps.json": ("single-lamps", "sc-single-lamps", 0, build_lamps),
	"safe-cracker-sc_18s11-moving-target-test.json": ("moving-target-test", "sc-moving-target-test", 0, build_moving_target),
	"safe-cracker-sc_18s11-moving-target-codes.json": ("moving-target-codes", "sc-moving-target-codes", 0, build_moving_target_codes),
	"safe-cracker-sc_18s11-token-test.json": ("token-test", "sc-token-test", 0, build_tokens),
	"safe-cracker-sc_18s11-light-rope-test.json": ("light-rope-test", "sc-light-rope-test", 0, build_light_ropes),
	"safe-cracker-sc_18s11-drop-target-test.json": ("drop-target-test", "sc-drop-target-test", 0, build_drop_targets),
	"safe-cracker-sc_18s11-top-trough-test.json": ("top-trough-test", "sc-top-trough-test", 0, build_top_trough),
}


def build(review_root: Path) -> dict[str, dict[str, Any]]:
	documents: dict[str, dict[str, Any]] = {}
	for filename, (directory, scenario, mechanics, builder) in RUNS.items():
		path = review_root / HARNESS_DIRECTORY / directory
		run = _load_run(path, scenario, mechanics)
		observations, command = builder(run)
		document = _document(filename.removeprefix("safe-cracker-").removesuffix(".json"), directory, scenario, mechanics, run, observations, command)
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
			raise ValueError(f"Safe Cracker compact runtime evidence drift: {path}")


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
		print("Safe Cracker compact runtime evidence matches the retained runs.")


if __name__ == "__main__":
	main()
