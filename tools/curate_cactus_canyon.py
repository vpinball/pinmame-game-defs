"""Curate the physical Bally Cactus Canyon (1998) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed
label, wiring detail, and normalized coordinate as a literal, so regeneration
reproduces the canonical artifact byte-for-byte without reading the external
evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only
path that writes the canonical definition and its pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept under machines/partial: flasher addresses 24 and 26 each drive a documented
# playfield+insert-panel bulb pair, but the retained VPX table renders only one
# resolvable coordinate cluster for each, so spatial placement stays a candidate
# rather than validated. See conflicts()/coverage below.
PARTIAL_PATH = ROOT / "machines/partial/bally/cactus-canyon-1998.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/cactus-canyon-1998.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/cactus-canyon-1998.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/cactus-canyon-1998.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/cactus-canyon-1998.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.bally.cactus-canyon.1998"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.cactus-canyon.1998"
VPX_TABLE_SOURCE = "vpx-table.cc-vpw-1-0-2"
VPX_SCRIPT_SOURCE = "vpx-script.cc-vpw-1-0-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.cc-vpw-1-0-2"

TABLE_SHA256 = "2e93faec289ce517a30f7285187d9eedca4652417ea2744e381c04a2e94e371b"
SCRIPT_SHA256 = "7b07f1492c5db71dd7acc33c8c5875cfbbe7a799092722b2372784149cd06313"
MANUAL_SHA256 = "dfd55dad3d85899c6e6b8a392f7965dff41ffade91587ba1b145762b7d6e1015"
MANUAL_TRANSCRIPTION_SHA256 = "68119b41c5bc5cada849c64ea0fc105262394eaaa71f0f5704f4c43b1efe2904"
VPX_GEOMETRY_SHA256 = "2f4ae8806e56d6ab75b82d24481efaf28f8bb18e601981e029c2adc9837af8aa"

EXTRACTION_RELATIVE_PATH = Path("bally/cactus-canyon-1998/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/cactus-canyon-1998/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "a0f7c251d961e72d588951496cbafd73ff9836475c5bc006cc44e63906aaa8bb"
EXTRACTION_FILE_COUNT = 1268
EXTRACTION_TOTAL_BYTES = 139765398

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"
TABLE_WIDTH = 952.0
TABLE_HEIGHT = 2162.0

DRIVER_IDS = ("cc_10", "cc_104", "cc_12", "cc_13", "cc_13k")
DRIVER_COMPATIBILITY = {
	"cc_10": ("identical", "Bally game ROM 1.0 for the same physical Cactus Canyon machine; switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged."),
	"cc_104": ("identical", "Bally / The Pinball Factory 1.04 Test 0.2 game ROM; a later test firmware revision of the same physical machine."),
	"cc_12": ("identical", "Bally game ROM 1.2; a later firmware revision of the same physical machine with no controller-address or playfield change."),
	"cc_13": ("identical", "Bally production 1.3 game ROM shipped with the physical machine. This is the driver the retained known-working VPW table binds to (cGameName = \"cc_13\")."),
	"cc_13k": ("identical", "Bally 1.3 \"Real Knocker\" patch ROM. A community patch of the same 1.3 firmware that changes the knocker driver behavior for operators who field-install a real knocker coil on public solenoid 7 (fitted with a drive transistor but no coil on the standard machine, see solenoid 7 below); it does not add or remove any playfield device."),
}

# --- Printed switch matrix (manual pages 2-38/2-39 parts list, 2-43 wiring).
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "Mine Entrance", 16: "Left Outlane",
	17: "Right Return Lane", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed",
	26: "Left Return Lane", 27: "Right Outlane", 28: "Bottom Right Standup",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3", 35: "Trough Ball 4",
	36: "Left Loop Bottom", 37: "Right Loop Bottom",
	41: "Mine Popper", 42: "Saloon Popper", 44: "Top Right Standup",
	46: "Beer Mug Switch", 47: "Left Bonus 'X' Lane", 48: "Jet Exit",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Left Jet Bumper", 54: "Right Jet Bumper",
	55: "Bottom Jet Bumper", 56: "Right Loop Top", 57: "Right Bonus 'X' Lane", 58: "Left Loop Top",
	61: "Drop Target 1 (Left)", 62: "Drop Target 2 (Left Center)", 63: "Drop Target 3 (Right Center)",
	64: "Drop Target 4 (Right)", 65: "Right Ramp Make", 66: "Right Ramp Enter", 67: "Skill Bowl",
	68: "Bottom Right Ramp",
	71: "Train Encoder", 72: "Train Home", 73: "Saloon Gate", 75: "Saloon Bart Toy",
	77: "Mine Home", 78: "Mine Encoder",
	82: "Center Ramp Enter", 83: "Left Ramp Make", 84: "Center Ramp Make", 85: "Left Ramp Enter",
	86: "Top Left Standup", 87: "Bottom Left Standup",
}
# Printed matrix positions marked "NOT USED" on both the switch-locations parts list
# (2-38/2-39) and the switch matrix (2-43).
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 25, 38, 43, 45, 74, 76, 81, 88}
# 24 (Always Closed) is a permanently-closed dedicated diagnostic jumper, not a rounding
# curiosity: it proves the matrix column is wired even with no ball/lamp evidence.
CONSTANT_CLOSED_ADDRESS = 24

# Every switch identified as opto by the union of BOTH manual cues -- shaded "OPTO,
# TYPICALLY CLOSED" on the printed switch matrix (2-43) AND an Opto Assembly Part
# Number with a blank Switch Part Number on the switch-locations parts list (2-38/39),
# cross-checked against the board-assembly pages (2-10 through 2-13: Trough IR LED/
# Photo Transistor PCB, Train Single Opto, Mine Dual Opto PCB). See
# review-artifacts/cactus-canyon-1998/manual-transcription.md "Opto sweep" section.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 41, 42, 71, 77, 78}
# ccGameData's inverted-switch mask ({0x00,0x00,0x00,0x7f,0x03,0x00,0x00,0xc1,...})
# covers column 3 bits 0-6 (31-37), column 4 bits 0-1 (41-42), and column 7 bits 0,6,7
# (71,77,78) -- exactly this set. Unlike Monster Bash's column 7 (0x00), every printed
# opto here is normalized by the emulator: no conflict.
PINMAME_NORMALIZED_OPTO_SWITCHES = set(OPTO_SWITCHES)
# vpmTimer.PulseSw / momentary callers in the retained VPW script.
PULSED_SWITCHES = {31, 71, 78}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "leaf", 22: "microswitch", 24: "other",
	26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto",
	41: "opto", 42: "opto", 44: "microswitch",
	46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf", 55: "leaf",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "microswitch",
	71: "opto", 72: "microswitch", 73: "microswitch", 75: "microswitch",
	77: "opto", 78: "opto",
	82: "microswitch", 83: "microswitch", 84: "microswitch", 85: "microswitch",
	86: "microswitch", 87: "microswitch",
}

# address -> (assembly_or_opto_part_number, switch_part_number), transcribed verbatim
# from printed 2-38/2-39.
SWITCH_PARTS = {
	13: ("20-9663-16", None), 14: (None, "04-10346"), 15: (None, "20-10293 (2)"),
	16: ("A-17813", "5647-12693-19"), 17: ("A-17813", "5647-12693-19"),
	18: (None, "5647-12693-68"), 21: ("A-17238", None), 22: (None, "5643-09268-00"),
	24: (None, "5643-15190-00"),
	26: ("A-17813", "5647-12693-19"), 27: ("A-17813", "5647-12693-19"),
	28: ("A-20499-12", None),
	31: ("A-18617-1 (LED) with A-18618-1 (photo trans)", None),
	32: ("A-18617-1 (LED) with A-18618-1 (photo trans)", None),
	33: ("A-18617-1 (LED) with A-18618-1 (photo trans)", None),
	34: ("A-18617-1 (LED) with A-18618-1 (photo trans)", None),
	35: ("A-18617-1 (LED) with A-18618-1 (photo trans)", None),
	36: ("A-16908 (LED) with A-16909 (photo trans)", None),
	37: ("A-16908 (LED) with A-16909 (photo trans)", None),
	41: ("A-16908 (LED) with A-16909 (photo trans)", None),
	42: ("A-16908 (LED) with A-16909 (photo trans)", None),
	44: ("A-20499-12", None),
	46: ("A-20783-7", None), 47: ("A-17813", "5647-12693-19"), 48: ("A-17813-1", "5647-12693-19"),
	51: ("A-17801", "A-17800 (kick) with A-17794 (score)"),
	52: ("A-17801", "A-17800 (kick) with A-17794 (score)"),
	53: ("B-12030-2", "A-16443"), 54: ("B-12030-2", "A-16443"),
	55: ("A-23146", "A-17800 (kick) with A-20979 (score)"),
	56: (None, "20-10293"), 57: ("A-17813", "5647-12693-19"), 58: ("A-17813", "5647-12693-19"),
	61: ("A-22296-1", "5647-12693-21"), 62: ("A-22296-2", "5647-12693-21"),
	63: ("A-22296-1", "5647-12693-21"), 64: ("A-22296-2", "5647-12693-21"),
	65: ("A-23028-2", "5647-12693-21"), 66: (None, "20-10293"), 67: (None, "5647-12693-21"),
	68: ("A-23028-4", "5647-12693-21"),
	71: ("A-22407", None), 72: (None, "5647-12693-66"), 73: (None, "5647-12693-11"),
	75: (None, "5647-12693-58"), 77: ("A-22443", None), 78: ("A-22443", None),
	82: ("A-22431", "5647-12693-11"), 83: ("A-23028-3", "5647-12693-21"),
	84: ("A-23028-4", "5647-12693-21"), 85: ("A-23028-3", "5647-12693-21"),
	86: ("A-20499-12", None), 87: ("A-20499-12", None),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-White", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Coin Chute 1 (Left)", "cabinet.coin.1", "Left coin chute."),
	2: ("Coin Chute 2 (Center)", "cabinet.coin.2", "Center coin chute."),
	3: ("Coin Chute 3 (Right)", "cabinet.coin.3", "Right coin chute."),
	4: ("Coin Chute 4", "cabinet.coin.4", "4th coin chute; not fitted on every configuration."),
	5: ("Service Credits / Escape", "service.escape", "Normal function Service Credits; test-menu function Escape."),
	6: ("Volume Down / Down", "service.down", "Normal function Volume Down; test-menu function Down."),
	7: ("Volume Up / Up", "service.up", "Normal function Volume Up; test-menu function Up."),
	8: ("Begin Test / Enter", "service.enter", "Normal function Begin Test; test-menu function Enter."),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"),
	4: ("Orange-Yellow", "J205-4"), 5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Blue-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Normalized playfield coordinates derived from the retained VPW 1.0.2 extraction
# (x/952, y/2162; review-artifacts/cactus-canyon-1998/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.340872, 0.277488)],
	16: [(0.053992, 0.792572)], 17: [(0.779548, 0.740259)], 18: [(0.940126, 0.888645)],
	26: [(0.127763, 0.738802)], 27: [(0.852574, 0.793002)], 28: [(0.851555, 0.563645)],
	31: [(0.876597, 0.851637)], 32: [(0.805462, 0.876267)], 33: [(0.727773, 0.898048)],
	34: [(0.652899, 0.918455)], 35: [(0.577111, 0.937599)], 36: [(0.122132, 0.363215)],
	37: [(0.790704, 0.205712)],
	41: [(0.320893, 0.234685)], 42: [(0.514286, 0.089672)], 44: [(0.82792, 0.524269)],
	46: [(0.201103, 0.400259)], 47: [(0.183708, 0.071059)], 48: [(0.131565, 0.22803)],
	51: [(0.231313, 0.73056)], 52: [(0.676576, 0.732493)],
	53: [(0.160294, 0.164186)], 54: [(0.337731, 0.124639)], 55: [(0.27542, 0.206512)],
	56: [(0.463172, 0.036193)], 57: [(0.276008, 0.066253)], 58: [(0.072742, 0.086147)],
	61: [(0.231922, 0.438821)], 62: [(0.406481, 0.434278)], 63: [(0.610021, 0.366785)],
	64: [(0.7677, 0.393316)], 65: [(0.844538, 0.131244)], 66: [(0.938435, 0.168673)],
	67: [(0.881828, 0.466929)], 68: [(0.84729, 0.536716)],
	73: [(0.636029, 0.204727)], 75: [(0.651366, 0.120467)],
	82: [(0.477374, 0.211864)], 83: [(0.05541, 0.627373)], 84: [(0.849002, 0.041166)],
	85: [(0.059086, 0.337997)], 86: [(0.144853, 0.544186)], 87: [(0.144853, 0.575504)],
}
SWITCH_PROJECTIONS = {
	71: "Projected onto the Train mechanism's own retained table objects (Primitives Train and Train1, table object center): the retained script's sw71 object is a VPX Timer, not a Hit trigger, and its sw71_Timer handler pulses public switch 71 once per encoder step while the Train primitive is in motion (\"Dozer - Encoder Pulse which runs with Train Mech.\"); there is no separate playfield sensor object.",
	72: "Projected onto the Train mechanism's own retained table object (Primitive Train, table object center): the retained script's PROC=0 TrainF/TrainB handlers never set Controller.Switch(72) at all (only the PROC=1 Polly_Timer path does), so there is no VPX object of any kind bound to this address under the physical ROM's normal operating path; the manual and PinMAME's own switch matrix are the only evidence this switch exists, at the position of the mechanism whose motion it senses.",
	77: "Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): like switch 72, the retained script's PROC=0 MoveMine/MineTimer_Timer handlers never set Controller.Switch(77) (only the PROC=1 Sw15_Timer path does); the manual and PinMAME are the only evidence for this address, recorded at the position of the mechanism it senses.",
	78: "Projected onto the Mine mechanism's own retained table object (Primitive MineSign, table object center): the retained script's PROC=0 path has no object bound to public switch 78 either (only the PROC=1 sw15b_Timer path pulses it, \"Dozer - Encoder Pulse which runs with Mine Mech.\"); recorded at the position of the mechanism it senses.",
}

SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Left Drop Target", 3: "Left Center Drop Target",
	4: "Right Center Drop Target", 5: "Right Drop Target", 6: "Mine Popper",
	8: "Saloon Popper", 9: "Trough Eject",
	10: "Left Slingshot", 11: "Right Slingshot", 12: "Left Jet Bumper", 13: "Right Jet Bumper",
	14: "Left Gunfight Post", 15: "Right Gunfight Post", 16: "Bottom Jet Bumper",
	17: "Mine Motor", 18: "Mine Flasher", 19: "Front Left Flasher", 20: "Front Right Flasher",
	21: "Left Loop Gate", 22: "Right Loop Gate",
	24: "Beacon Flasher", 25: "Middle Right Flasher", 26: "Saloon Flasher",
	27: "Back Right Flasher", 28: "Back Left Flasher",
	33: "Move Bart Toy", 36: "Bart Toy Hat",
	37: "Train Reverse", 38: "Train Forward",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
# Populated drive transistor with no voltage/drive connection in any playfield, insert,
# or cabinet column -- proves nothing is fitted, the same signature as Monster Bash's
# knocker circuit (address 7 here too).
NOT_FITTED_SOLENOID_LABELS = {
	7: "Not Used Solenoid 7 (Knocker Driver, Unfitted)",
	23: "Not Used Solenoid 23",
	34: "Not Used Solenoid 34 (Move Bart Toy Hold)",
	35: "Not Used Solenoid 35 (Bart Toy Hat Power)",
}
SOLENOID_ASSEMBLIES = {
	1: "A-21022-1", 2: "A-22296-1", 3: "A-22296-2", 4: "A-22296-1", 5: "A-22296-2",
	6: "A-22467", 8: "A-22435", 9: "A-19963", 10: "A-22207-2", 11: "A-22206-2",
	12: "A-22205-2", 13: "A-22205-2", 14: "A-22465", 15: "A-22465", 16: "A-22206-2",
	17: "A-22404", 18: "04-12478-12", 19: "04-11221-12", 20: "04-11221-12",
	21: "A-22482", 22: "A-22482", 24: "A-17802", 33: "A-22432", 36: "A-22432",
	37: "A-22271", 38: "A-22271",
	45: "A-14876-R", 46: "A-14876-R", 47: "A-15849-L", 48: "A-15849-L",
}
# address -> (printed voltage/type, part number)
SOLENOID_WIRING = {
	1: {"printed_type": "High Power", "part_number": "AE-23-800", "driver_transistor": "Q72", "power_connection": "J133-2", "control_connection": "J116-1"},
	2: {"printed_type": "High Power", "part_number": "AE-26-1500", "driver_transistor": "Q68", "power_connection": "J133-2", "control_connection": "J116-2"},
	3: {"printed_type": "High Power", "part_number": "AE-26-1500", "driver_transistor": "Q71", "power_connection": "J133-2", "control_connection": "J116-4"},
	4: {"printed_type": "High Power", "part_number": "AE-26-1500", "driver_transistor": "Q67", "power_connection": "J133-2", "control_connection": "J116-5"},
	5: {"printed_type": "High Power", "part_number": "AE-26-1500", "driver_transistor": "Q70", "power_connection": "J133-2", "control_connection": "J116-6"},
	6: {"printed_type": "High Power", "part_number": "AE-24-900", "driver_transistor": "Q66", "power_connection": "J133-2", "control_connection": "J116-7"},
	7: {"printed_type": "High Power", "driver_transistor": "Q69"},
	8: {"printed_type": "High Power", "part_number": "AE-26-1500", "driver_transistor": "Q65", "power_connection": "J133-2", "control_connection": "J116-9"},
	9: {"printed_type": "Low Power", "part_number": "AE-26-1500", "driver_transistor": "Q44", "power_connection": "J133-3", "control_connection": "J113-1"},
	10: {"printed_type": "Low Power", "part_number": "AE-26-1200", "driver_transistor": "Q48", "power_connection": "J133-3", "control_connection": "J113-3"},
	11: {"printed_type": "Low Power", "part_number": "AE-26-1200", "driver_transistor": "Q43", "power_connection": "J133-3", "control_connection": "J113-4"},
	12: {"printed_type": "Low Power", "part_number": "AE-26-1200", "driver_transistor": "Q47", "power_connection": "J133-3", "control_connection": "J113-5"},
	13: {"printed_type": "Low Power", "part_number": "AE-26-1200", "driver_transistor": "Q42", "power_connection": "J133-3", "control_connection": "J113-6"},
	14: {"printed_type": "Low Power", "part_number": "AE-26-1500", "driver_transistor": "Q46", "power_connection": "J133-3", "control_connection": "J113-7"},
	15: {"printed_type": "Low Power", "part_number": "AE-26-1500", "driver_transistor": "Q41", "power_connection": "J133-3", "control_connection": "J113-8"},
	16: {"printed_type": "Low Power", "part_number": "AE-26-1200", "driver_transistor": "Q45", "power_connection": "J133-3", "control_connection": "J113-9"},
	17: {"printed_type": "Flasher", "part_number": "14-8015", "driver_transistor": "Q28", "power_connection": "J140-2", "control_connection": "J111-1"},
	18: {"printed_type": "Flasher", "part_number": "#906", "driver_transistor": "Q32", "power_connection": "J133-6", "control_connection": "J111-2"},
	19: {"printed_type": "Flasher", "part_number": "#906", "driver_transistor": "Q27", "power_connection": "J133-6", "control_connection": "J111-3"},
	20: {"printed_type": "Flasher", "part_number": "#906", "driver_transistor": "Q31", "power_connection": "J133-6", "control_connection": "J111-4"},
	21: {"printed_type": "Flasher", "part_number": "A-14406", "driver_transistor": "Q26", "power_connection": "J133-1", "control_connection": "J111-5"},
	22: {"printed_type": "Flasher", "part_number": "A-14406", "driver_transistor": "Q30", "power_connection": "J133-1", "control_connection": "J111-6"},
	23: {"printed_type": "Flasher", "driver_transistor": "Q25"},
	24: {"printed_type": "Flasher", "part_number": "#906 / #906", "driver_transistor": "Q29", "power_connection": "J133-6 and J134-5", "control_connection": "J111-8 and J112-9"},
	25: {"printed_type": "Gen. Purpose", "part_number": "#906", "driver_transistor": "Q16", "power_connection": "J133-6", "control_connection": "J109-1"},
	26: {"printed_type": "Gen. Purpose", "part_number": "#906 / #906", "driver_transistor": "Q15", "power_connection": "J133-6 and J134-5", "control_connection": "J109-2 and J108-2"},
	27: {"printed_type": "Gen. Purpose", "part_number": "#906 / #906", "driver_transistor": "Q14", "power_connection": "J133-6 and J134-5", "control_connection": "J109-3 and J108-3"},
	28: {"printed_type": "Gen. Purpose", "part_number": "#906 / #906", "driver_transistor": "Q13", "power_connection": "J133-6 and J134-5", "control_connection": "J109-5 and J108-5"},
	33: {"printed_type": "Power", "part_number": "AE-26-1500", "driver_transistor": "Q84", "power_connection": "J119-6 (RED-VIO)", "control_connection": "J120-6"},
	34: {"printed_type": "Hold", "driver_transistor": "Q86", "power_connection": "J119-6 (RED-VIO)", "control_connection": "J120-4"},
	35: {"printed_type": "Power", "driver_transistor": "Q81", "power_connection": "J119-8 (RED-GRY)", "control_connection": "J120-3"},
	36: {"printed_type": "Hold", "part_number": "AE-26-1500", "driver_transistor": "Q83", "power_connection": "J119-8 (RED-GRY)", "control_connection": "J120-1"},
	37: {"printed_type": "Low Power", "part_number": "14-8015", "driver_transistor": "gates U3A/U3B", "control_connection": "J110-1"},
	38: {"printed_type": "Low Power", "driver_transistor": "gates U3C/U3D", "control_connection": "J110-3"},
	45: {"printed_type": "Power", "part_number": "FL-11630", "driver_transistor": "Q90", "power_connection": "J119-1 (RED-GRN)", "control_connection": "J120-13"},
	46: {"printed_type": "Hold", "driver_transistor": "Q92", "power_connection": "J119-1 (RED-GRN)", "control_connection": "J120-11"},
	47: {"printed_type": "Power", "part_number": "FL-11630", "driver_transistor": "Q87", "power_connection": "J119-4 (RED-BLU)", "control_connection": "J120-9"},
	48: {"printed_type": "Hold", "driver_transistor": "Q89", "power_connection": "J119-4 (RED-BLU)", "control_connection": "J120-7"},
}
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}
SOLENOID_CALLBACKS = {
	1: 'SolCallback(1) = "AutoPlunger"', 2: 'SolCallback(2) = "Drop1"', 3: 'SolCallback(3) = "Drop2"',
	4: 'SolCallback(4) = "Drop3"', 5: 'SolCallback(5) = "Drop4"', 6: 'SolCallback(6) = "SolMinePopper"',
	8: 'SolCallback(8) = "SolSaloonPopper"', 9: 'SolCallback(9) = "ReleaseBall"',
	14: 'SolCallback(14) = "GunPostLeft"', 15: 'SolCallback(15) = "GunPostRight"',
	17: 'SolCallBack(17) = "MoveMine" (PROC=0 branch)',
	21: 'SolCallback(21) = "LGate"', 22: 'SolCallback(22) = "RGate"',
	33: 'SolCallback(33) = "MoveBart"', 36: 'SolCallback(36) = "MoveHat"',
	37: 'SolCallback(37) = "TrainB" (PROC=0 branch)', 38: 'SolCallback(38) = "TrainF" (PROC=0 branch)',
	45: 'SolCallback(sLRFlipper) = "SolRFlipper"', 46: 'SolCallback(sLRFlipper) = "SolRFlipper"',
	47: 'SolCallback(sLLFlipper) = "SolLFlipper"', 48: 'SolCallback(sLLFlipper) = "SolLFlipper"',
}
FLIPPER_DRIVE_WIRE = {45: "YEL-GRN", 46: "ORG-GRN", 47: "YEL-BLU", 48: "ORG-BLU"}

SOLENOID_POSITIONS = {
	1: [(0.9402, 0.965772)],
	2: [(0.231922, 0.438821)], 3: [(0.406481, 0.434278)], 4: [(0.610021, 0.366785)], 5: [(0.7677, 0.393316)],
	6: [(0.320893, 0.234685)], 8: [(0.514286, 0.089672)], 9: [(0.876597, 0.851637)],
	10: [(0.231313, 0.73056)], 11: [(0.676576, 0.732493)], 12: [(0.160294, 0.164186)], 13: [(0.337731, 0.124639)],
	14: [(0.225315, 0.790648)], 15: [(0.68334, 0.790883)], 16: [(0.27542, 0.206512)],
	17: [(0.343487, 0.310939)],
	21: [(0.110221, 0.052128)], 22: [(0.362857, 0.026739)],
	33: [(0.648277, 0.116346)], 36: [(0.667384, 0.077539)],
	37: [(0.739496, 0.342276)], 38: [(0.739496, 0.342276)],
	45: [(0.622071, 0.844588)], 46: [(0.622071, 0.844588)], 47: [(0.287847, 0.844588)], 48: [(0.287847, 0.844588)],
}
# Flasher addresses use a light-cluster centroid or, where two distinct rendered
# positions exist, both -- see review-artifacts/cactus-canyon-1998/vpx-geometry.txt.
FLASHER_POSITIONS = {
	18: [(0.322517, 0.302535)],
	19: [(0.091456, 0.827937)],
	20: [(0.810374, 0.83104)],
	24: [(0.6428, 0.571628)],
	25: [(0.9536, 0.36775)],
	26: [(0.757863, 0.19034)],
	27: [(0.847689, 0.009251), (0.994748, 0.032234)],
	28: [(0.160714, 0.007863), (0.002101, 0.175301)],
}
FLASHER_QUANTITY = {18: 1, 19: 1, 20: 1, 24: 2, 25: 1, 26: 2, 27: 2, 28: 2}

LAMP_LABELS = {
	11: "Rank: Stranger", 12: "Rank: Partner", 13: "Rank: Deputy", 14: "Rank: Sheriff",
	15: "Rank: Marshall", 16: "Star: Mother Lode", 17: "Left Bonus 'X' Lane", 18: "Right Bonus 'X' Lane",
	21: "Bounty Beacon", 22: "Jackpot Beacon", 23: "Shoot To Collect", 24: "Extra Ball Lit Beacon",
	25: "Bounty (Saloon)", 26: "Saloon Arrow", 27: "Extra Ball", 28: "Mine Lock",
	31: "Right Center Drop: Bad Guy 3", 32: "Left Drop: Bad Guy 1", 33: "Left Standup",
	34: "Right Ramp: Sound Alarm", 35: "Right Ramp: Shoot Out", 36: "Right Ramp: Save Polly",
	37: "Right Ramp: Jackpot", 38: "Right Ramp: Combo",
	41: "Right Loop: Combo", 42: "Right Loop: Jackpot", 43: "Right Loop: Marksman",
	44: "Right Loop: Gunslinger", 45: "Right Loop: Good Shot",
	46: "Left Return: Quick Draw", 47: "Left Gunfight Pin", 48: "Left Out: Gunfight",
	51: "Right Drop: Bad Guy 4", 52: "Bottom Right Standup", 53: "Top Right Standup",
	54: "Center Ramp: Catch Train", 55: "Center Ramp: Stop Train", 56: "Center Ramp: Save Polly",
	57: "Center Ramp: Jackpot", 58: "Center Ramp: Combo",
	61: "Left Ramp: Whitewater", 62: "Left Ramp: Waterfall", 63: "Left Ramp: Save Polly",
	64: "Left Ramp: Jackpot", 65: "Left Ramp: Combo",
	66: "Right Return: Quick Draw", 67: "Right Out: Special", 68: "Right Gunfight Pin",
	71: "Star: Stampede", 72: "Star: Combo", 73: "Star: High Noon",
	74: "Left Loop: Combo", 75: "Left Loop: Jackpot", 76: "Left Loop: Ride 'Em",
	77: "Left Loop: Wild Ride", 78: "Left Loop: Buck'n Bronco",
	81: "Star: Bart Brothers", 82: "Shoot Again", 83: "Star: Showdown",
	84: "Left Center Drop: Bad Guy 2", 87: "Not Used Lamp Position 87", 88: "Start Button",
}
LAMP_UNUSED_ADDRESSES = {85, 86, 87}
LAMP_ASSEMBLIES = {
	11: ("04-12351", "#555"), 12: ("04-12351", "#555"), 13: ("04-12351", "#555"),
	14: ("04-12351", "#555"), 15: ("04-12351", "#555"), 16: ("04-12351", "#555"),
	17: ("04-10254", "#44"), 18: ("04-10254", "#44"),
	21: ("04-12353", "#555"), 22: ("04-12353", "#555"), 23: ("04-12353", "#555"), 24: ("04-12353", "#555"),
	25: ("A-17835", "#44"), 26: ("A-17835", "#44"), 27: ("A-17835", "#44"), 28: ("A-17807", "#44"),
	31: ("A-17807", "#44"), 32: ("A-17807", "#44"), 33: ("A-17835", "#44"),
	34: ("04-12354", "#555"), 35: ("04-12354", "#555"), 36: ("04-12354", "#555"),
	37: ("04-12354", "#555"), 38: ("04-12354", "#555"),
	41: ("04-12352", "#555"), 42: ("04-12352", "#555"), 43: ("04-12352", "#555"),
	44: ("04-12352", "#555"), 45: ("04-12352", "#555"),
	46: ("A-17835", "#44"), 47: ("A-17807", "#44"), 48: ("A-17835", "#44"),
	51: ("A-17807", "#44"), 52: ("A-17835", "#44"), 53: ("A-17835", "#44"),
	54: ("04-12354", "#555"), 55: ("04-12354", "#555"), 56: ("04-12354", "#555"),
	57: ("04-12354", "#555"), 58: ("04-12354", "#555"),
	61: ("04-12354", "#555"), 62: ("04-12354", "#555"), 63: ("04-12354", "#555"),
	64: ("04-12354", "#555"), 65: ("04-12354", "#555"),
	66: ("A-17835", "#44"), 67: ("A-17807", "#44"), 68: ("A-17807", "#44"),
	71: ("A-17807", "#44"), 72: ("A-17807", "#44"), 73: ("A-17835", "#44"),
	74: ("04-12352", "#555"), 75: ("04-12352", "#555"), 76: ("04-12352", "#555"),
	77: ("04-12352", "#555"), 78: ("04-12352", "#555"),
	81: ("A-17807", "#44"), 82: ("A-17807", "#44"), 83: ("A-17835", "#44"), 84: ("A-17807", "#44"),
	88: ("20-9663-16", "Not Sold Separate"),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
	3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Black", "J121-4", "Q99"),
	5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
	3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
	5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}
# l23/l23a are two genuinely different retained VPX coordinates bound to the same
# lamp address, but the manual's Lamp Locations entry for item 23 (Shoot To Collect)
# shows exactly one bulb/socket/assembly. l23a is treated as a table-only second
# render object and excluded, matching the manual's single-bulb quantity.
LAMP_RENDER_DOUBLES = {23}

GI_STRINGS = {
	0: ("Illumination String 1", "J105-1", "Q5", "J105-7", "#44"),
	1: ("Illumination String 2", "J105-2", "Q4", "J105-8", "#44"),
	2: ("Illumination String 3", "J105-3", "Q3", "J105-9", "#44"),
	3: ("Illumination String 4", "J106-5", "Q2", "J106-10", "#555"),
	4: ("All Illumination", "J106-6 and J104-3", "Q1", "J106-11 and J104-1", "#555"),
}
LAMP_POSITIONS = {
	11: [(0.286334, 0.674251)], 12: [(0.359737, 0.647488)], 13: [(0.455315, 0.639607)],
	14: [(0.551565, 0.647868)], 15: [(0.625956, 0.674986)], 16: [(0.454779, 0.667109)],
	17: [(0.184559, 0.040874)], 18: [(0.276061, 0.03555)],
	21: [(0.643824, 0.617858)], 22: [(0.586744, 0.60179)], 23: [(0.668067, 0.587137)],
	24: [(0.518697, 0.593279)], 25: [(0.611639, 0.268423)], 26: [(0.602101, 0.310971)],
	27: [(0.363088, 0.364764)], 28: [(0.381544, 0.408964)],
	31: [(0.593267, 0.409237)], 32: [(0.260284, 0.481041)], 33: [(0.191912, 0.568159)],
	34: [(0.693582, 0.547521)], 35: [(0.725189, 0.516809)], 36: [(0.752952, 0.486378)],
	37: [(0.789664, 0.450842)], 38: [(0.829454, 0.409505)],
	41: [(0.781029, 0.275333)], 42: [(0.752616, 0.315569)], 43: [(0.717721, 0.350463)],
	44: [(0.705074, 0.372919)], 45: [(0.687468, 0.395005)],
	46: [(0.128897, 0.687368)], 47: [(0.181933, 0.784348)], 48: [(0.052342, 0.742049)],
	51: [(0.729401, 0.437729)], 52: [(0.806124, 0.572539)], 53: [(0.781492, 0.533876)],
	54: [(0.473634, 0.44876)], 55: [(0.473542, 0.414718)], 56: [(0.473086, 0.380248)],
	57: [(0.475777, 0.331528)], 58: [(0.475191, 0.295121)],
	61: [(0.374714, 0.565566)], 62: [(0.354741, 0.53314)], 63: [(0.33581, 0.500364)],
	64: [(0.315079, 0.466631)], 65: [(0.288901, 0.418246)],
	66: [(0.781794, 0.687186)], 67: [(0.858805, 0.743445)], 68: [(0.727321, 0.784766)],
	71: [(0.312573, 0.712045)], 72: [(0.597989, 0.71183)], 73: [(0.457313, 0.728813)],
	74: [(0.135169, 0.418527)], 75: [(0.172366, 0.464332)], 76: [(0.199069, 0.495909)],
	77: [(0.218747, 0.519036)], 78: [(0.238291, 0.541605)],
	81: [(0.541663, 0.784597)], 82: [(0.453897, 0.87491)], 83: [(0.366839, 0.784829)],
	84: [(0.409018, 0.479513)],
	88: [(0.940126, 0.888645)],
}
GI_POSITIONS = {
	0: [
		(0.066907, 0.400675), (0.07146, 0.607051), (0.098183, 0.454017), (0.117679, 0.559022),
		(0.126261, 0.909269), (0.130987, 0.504269), (0.140158, 0.798691), (0.190462, 0.719611),
		(0.212253, 0.820456), (0.218503, 0.763594),
	],
	1: [
		(0.692111, 0.763691), (0.69605, 0.823784), (0.721728, 0.722387), (0.77041, 0.801249),
		(0.772584, 0.909806), (0.846507, 0.500793), (0.855704, 0.457858), (0.875063, 0.535779),
		(0.888535, 0.418941), (0.893367, 0.762909), (0.893519, 0.671124), (0.894102, 0.592817),
	],
	2: [
		(0.114286, 0.099311), (0.133587, 0.009389), (0.133661, 0.124063), (0.134055, 0.259662),
		(0.159398, 0.167049), (0.202479, 0.251031), (0.230063, 0.063432), (0.32697, 0.063844),
		(0.337353, 0.127939), (0.423451, 0.179221), (0.476297, 0.124258), (0.767542, 0.02049),
		(0.852363, 0.046792), (0.92385, 0.075694), (0.925672, 0.218159), (0.93386, 0.127419),
	],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Cactus Canyon retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Cactus Canyon extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Cactus Canyon retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Cactus Canyon retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Cactus Canyon retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": provenance(*source_refs),
			}
		)
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the cc_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/cc.c ccGameData GEN_WPC95 with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x7f,0x03,0x00,0x00,0xc1,0x00,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), "
				"swStart/swTilt/swSlamTilt/swCoinDoor/swTicket defines, sKnocker=7/sTrough=9/sLeftSling=10/sRightSling=11/"
				"sLeftJet=12/sRightJet=13/sBottomJet=16 (preliminary ball-simulator scaffolding only), and init_cc's "
				"wpc_set_fastflip_addr(0x87); src/wpc/core.h WPC solenoid numbering, WPC_swF1..WPC_swF8, and "
				"CORE_FLIPPERSWCOL=11 with CORE_SW*FLIPBUTBIT/CORE_SW*FLIPEOSBIT bit assignments; src/wpc/core.c "
				"core_getSol WPC95 37..40 to 41..44 duplication and core_getSw/core_updateSw invSw XOR semantics; "
				"src/wpc/wpc.c WPC_FLIPPERSW95 hardware inversion (line ~630); src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WPC95=0x80"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-95.json",
			"revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.cactus-canyon.1998/ipdb/Cactus_Canyon_Manual.pdf",
			"original_filename": "Cactus_Canyon_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"135-page OCR'd scan of the Bally Cactus Canyon operations manual (part number 16-50066-101, "
				"January 1999 Final), scanned by flipperspill.com. Printed pages 2-34 through 2-43 carry the "
				"lamp/switch/solenoid location parts lists and their matrix and solenoid/flasher wiring tables; "
				"printed pages 2-10 through 2-13 carry the opto-board assembly parts that fix opto construction "
				"(Trough IR LED/Photo Transistor PCB, Train Single Opto, Flipper Opto PCB, 10-Opto PCB, Mine Dual "
				"Opto PCB); printed page 1-45 carries Opto Theory."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by flipperspill.com",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.cactus-canyon.switch-matrix",
					"locator": "PDF page 101, printed page 2-43, SWITCH MATRIX table",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/switch-matrix.md",
					"sha256": "799e5a6ce7f488969b30b812c820eac4b42d3ee373dddfc39df35835b3420571",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/switch-matrix.webp",
					"image_sha256": "0a641495ee5d8e3260a85427a7d7304a03c4cd6afdac830b5a7ac2f5f4947599",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 101, crop box 0.02,0.055,0.985,0.605 of the page, rendered at 300 dpi with pdftoppm, reduced to 800px wide grayscale, quality 75 WebP",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.switch-locations",
					"locator": "PDF pages 96-97, printed 2-38/2-39, switch-locations parts list plus opto sweep",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/switch-locations.md",
					"sha256": "e182f7f597b90363608a6b2bdaac86852ee071f4d2e42183d8505cf93968c2c2",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/switch-locations.webp",
					"image_sha256": "5a61ccb4506fd1e0a4b08f1b497fbaebc577491cf9dfa6e66371643811d26dd4",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 96, crop box 0.03,0.03,0.985,0.98, scanned page rendered at its native resolution (embedded image xref 395, 1551px across 7.76in), rendered at 200 dpi, 1482x2044 WebP quality 80",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.opto-board-assemblies",
					"locator": "PDF page 55 (printed 1-45, Opto Theory) and PDF pages 68-71 (printed 2-10 through 2-13, opto board assemblies)",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/opto-board-assemblies.md",
					"sha256": "c8ce76bd28068ed4e7e8030c5f402279a15149c7e10223ac25bf3d44a4038932",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/opto-board-assemblies.webp",
					"image_sha256": "dbb68592dbc8508685407743819d3795b181e1b696e44e2ff9611e0291c1732b",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 70, crop box 0.03,0.02,0.97,0.615, scanned page rendered at its native resolution (embedded image xref 284, 1547px across 7.74in), rendered at 200 dpi, 1455x1279 WebP quality 80; the assembly drawings on PDF pages 68-71 are the dominant factual content this excerpt transcribes (page 55 supplies only incidental Opto Theory prose), and A-20246 (10-Opto PCB Assembly w/Bracket, printed 2-12) is the single most complete crop, serving nine of the fourteen normally-closed opto switches this excerpt documents (31-35 trough, 36-37 loop bottoms, 41-42 poppers)",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.lamp-locations",
					"locator": "PDF page 92, printed 2-34, Lamp Locations parts list",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/lamp-locations.md",
					"sha256": "201f5bbb71b3201ce319dc68ef0740c847a3151c2ac9393c5c5622d0a842849e",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/lamp-locations.webp",
					"image_sha256": "d3b6ed2984ba1238a90350dccd63f4ea155dc183027f359b9ce334471990a712",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 92, crop box 0.03,0.03,0.985,0.945, scanned page rendered at its native resolution (embedded image xref 378, 1551px across 7.76in), rendered at 200 dpi, 1482x1965 WebP quality 80",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.lamp-matrix",
					"locator": "PDF page 99, printed 2-41, Lamp Matrix",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/lamp-matrix.md",
					"sha256": "a528e1fb93c9ca47decd0b477fc352dd94b1d06c3e0b73acfc9f94740ca71b50",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/lamp-matrix.webp",
					"image_sha256": "6d3516342356ad47556385f96147aa59b5010972550ea201fe739115b927abee",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 99, crop box 0.05,0.03,0.98,0.575, scanned page rendered at its native resolution (embedded image xref 408, 1551px across 7.76in), rendered at 118 dpi, capped to 850px wide, 851x690 WebP quality 80",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.solenoid-flasher-locations",
					"locator": "PDF page 94, printed 2-36, Solenoid/Flasher Locations plus Flippers and Train Motor",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/solenoid-flasher-locations.md",
					"sha256": "f1e0e2a9094bb63fca5e5b5c06f92243c754bcb5e9231230742bceccd497dd46",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/solenoid-flasher-locations.webp",
					"image_sha256": "444a2650df681b1ca0e5853aaeee33a869505b33082d2ef32d7edc45085b22c4",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 94, crop box 0.03,0.02,0.985,0.69, scanned page rendered at its native resolution (embedded image xref 387, 1551px across 7.76in), rendered at 200 dpi, 1482x1440 WebP quality 80; cropped to the Solenoid/Flasher Locations, Flippers and Train Motor Circuits blocks only, excluding the General Illumination block printed lower on the same page (see excerpt.cactus-canyon.general-illumination)",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.solenoid-flasher-wiring",
					"locator": "PDF page 100, printed 2-42, Solenoid/Flasher Table wiring",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/solenoid-flasher-wiring.md",
					"sha256": "aad436975f4dc6c8c814de5100809eabdd7ad7044d4095c535da790ecf1bd629",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/solenoid-flasher-wiring.webp",
					"image_sha256": "6f0dba7668654954000f5059ab18272f1629c9c447d1ded15a68e8f9bd3c53a2",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 100, crop box 0.03,0.02,0.985,0.59, scanned page rendered at its native resolution (embedded image xref 412, 1551px across 7.76in), rendered at 200 dpi, 1482x1225 WebP quality 80; cropped to the Solenoid/Flasher Table, Flipper Circuits and Train Motor blocks only, excluding the General Illumination block printed lower on the same page (see excerpt.cactus-canyon.general-illumination)",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cactus-canyon.general-illumination",
					"locator": "PDF pages 94 and 100, printed 2-36 and 2-42, General Illumination location and wiring",
					"path": "evidence/excerpts/bally.cactus-canyon.1998/general-illumination.md",
					"sha256": "67c6345ab223dbb8c3a2f4033cd9b81db454745d40cbf8af7f54fc9458fdb283",
					"image": "evidence/excerpts/bally.cactus-canyon.1998/general-illumination.webp",
					"image_sha256": "fa0703431ea4bf913e677a0192e17344603f2da3f065bcb4577322842ab94ed8",
					"image_derivation": "Cactus_Canyon_Manual.pdf page 100, crop box 0.03,0.585,0.985,0.745, scanned page rendered at its native resolution (embedded image xref 412, 1551px across 7.76in), rendered at 200 dpi, 1482x345 WebP quality 80; the printed 2-42 wiring block is the more complete of the two General Illumination pages (it alone carries the *always-on footnote and the bulb-code reference box), so this crops the General Illumination sub-table at the bottom of page 100, distinct from and below the Solenoid/Flasher Table crop used by excerpt.cactus-canyon.solenoid-flasher-wiring on the same page",
					"method": "mixed",
					"transcribed_by": "curator, OCR text extracted then confirmed against the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/cactus-canyon-1998/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every table used by this definition, cross-checked against the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/bally.cactus-canyon.1998/, "
				"including the full opto-cue sweep reconciled column by column against ccGameData's inverted-"
				"switch mask."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/cactus-canyon-1998/source/Cactus%20Canyon%20%28Bally%201998%29%20VPW%201.0.2.vpx",
			"original_filename": "Cactus Canyon (Bally 1998) VPW 1.0.2.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW 1.0.2 recreation of the physical machine (internal table_version "
				"metadata reads \"2.0\"). Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/2162. Geometry authority only for named "
				"table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW (ninuzzu & tom tower)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/cactus-canyon-1998/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (3,711 lines). Runtime and mechanism-causality authority: '
				'Const cGameName = "cc_13" binds the original Bally ROM; Const B2ScGameName = "Proc_CC" is only a '
				"shared backglass-server profile name and does not gate behavior; Const PROC = 0 is the compiled "
				"default (\"1=Use PROC, 0=Use VPinMAME\") followed throughout this definition, with every PROC=1 "
				"branch belonging to the community P-ROC \"Cactus Canyon Continued\" hardware path and out of "
				"scope. The SolCallback table for solenoids 1-38 (PROC=0 branch), InitLamps binding Lights(i) = "
				"Array(Li, Lia) for i=0..127, GiCallback2 UpdateGI mapping GI 0/1/2 to LeftGI/RightGI/TopGI, and "
				"the TrainF/TrainB/MoveMine/MoveBart/MoveHat mechanism handlers are the causal authority."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/cactus-canyon-1998/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_component = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC-95 CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == CONSTANT_CLOSED_ADDRESS else "switch"
			assembly, part_number = SWITCH_PARTS.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed switch-locations parts list and switch matrix both mark this position Not Used."
				if address == 38:
					notes += (
						" It sits in the same column-3 opto strobe as 31-37 and the matrix page shades it \"OPTO, "
						"TYPICALLY CLOSED\" like its neighbors, but the switch-locations parts list marks both the "
						"assembly and switch-part columns Not Used, so no tenth opto is fitted on the 10-Opto board "
						"template's spare position."
					)
			elif address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed as an opto that rests closed on the board-assembly pages 2-10 through 2-13 (Trough IR "
					"LED/Photo Transistor PCB, Train Single Opto, or Mine Dual Opto PCB) with the Switch Part Number "
					"column blank; ccGameData's inverted-switch mask "
					"({0x00,0x00,0x00,0x7f,0x03,0x00,0x00,0xc1,...}) normalizes it, so the public switch state is "
					"already normalized and must not be inverted again."
				)
			if address == CONSTANT_CLOSED_ADDRESS:
				notes += " Physical part 5643-15190-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CONTROLLER_SOURCE)
				label = label or f"Not Used Matrix Position {address}"
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				if address in PULSED_SWITCHES:
					extra["pulse"] = True
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address == 13 else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				elif address == 18:
					extra["roles"] = ["cabinet.launch"]
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					if address in SWITCH_POSITIONS:
						extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
					elif address in SWITCH_PROJECTIONS:
						projection_target = {
							71: [(0.739496, 0.342276)], 72: [(0.739496, 0.342276)],
							77: [(0.343487, 0.310939)], 78: [(0.343487, 0.310939)],
						}[address]
						extra["spatial"] = located(identifier, "sensor", projection_target, VPX_TABLE_SOURCE)
					else:
						raise RuntimeError(f"switch {address} has no spatial evidence")
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None, True),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316", True),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None, True),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316", True),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, False),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, None, False),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, False),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, None, False),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly, keep_wiring) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" Cactus Canyon has no upper flippers: ccGameData declares FLIP_SOL(FLIP_L) only (lower-flipper "
				"coils), and the switch-locations parts list on manual page 2-38 marks both the assembly and switch "
				"part columns Not Used for this position."
			)
			physical["location"] = "not installed"
		elif switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed (shaded on the switch matrix, printed under the Opto "
				"Assembly Part Number column as A-17316 Flipper Opto PCB Assembly with a blank Switch Part Number). "
				"WPC-95 reads the flipper column through WPC_FLIPPERSW95 with a hardware inversion, so the public "
				"switch state is already normalized; this same claim holds for Medieval Madness, Attack From Mars, "
				"and Monster Bash, all of which leave this array index at 0x00 too."
			)
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
		}
		if keep_wiring:
			extra["wiring"] = {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			if normally_closed is not None:
				extra["normally_closed"] = bool(normally_closed)
		else:
			extra["normally_closed"] = bool(normally_closed)
			if role.endswith(".button"):
				extra["spatial"] = located(f"switch.generic-{address}", "sensor", [(0.622071, 0.844588) if address == 112 else (0.287847, 0.844588)], VPX_TABLE_SOURCE)
			else:
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				**extra,
			)
		)

	dip_labels = {n: f"CPU DIP {n} (country/option configuration bit)" for n in range(1, 9)}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				dip_labels[address],
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-95 CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-95 CPU-board country/option configuration DIP bank. The retained transcription of this "
						"manual's printed DIP chart (page 1-1) records only the AMERICA row's ON/OFF pattern, not the "
						"full per-country combination table, so no specific ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			kind = (
				"flasher" if 17 <= address <= 28 and address not in {21, 22}
				else "coil" if address in {21, 22}
				else "motor" if address in {17, 37, 38}
				else "coil"
			)
			if address == 17:
				kind = "motor"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind not in {"flasher"}:
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher":
				quantity = FLASHER_QUANTITY.get(address, 1)
				physical["quantity"] = quantity
				if part_number:
					notes += f" Printed flashlamp complement: {part_number}."
				if quantity == 2:
					notes += (
						" The solenoid-locations list prints this address twice (Playfield and Insert Panel), so "
						"two bulbs are fitted."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address == 7:
				notes += (
					" The printed table shows a populated power-driver transistor (Q69) with no voltage connection "
					"and no drive connection in any playfield, insert, or cabinet column, so no coil is fitted here "
					"on the standard machine. Pinned PinMAME's cc.c nonetheless defines #define sKnocker 7, consumed "
					"only by its preliminary ball simulator; the WPC-95 operating system uses driver 7 as its "
					"standard knocker output and the ROM pulses it regardless. The cc_13k \"Real Knocker patch\" "
					"driver exists specifically for operators who field-install a real knocker coil on this circuit; "
					"the standard cc_13 machine ships with none. All sources are cited and no physical knocker device "
					"is claimed for the base machine."
				)
			if address == 23:
				notes += (
					" The printed table shows a populated power-driver transistor (Q25) with no voltage or drive "
					"connection in any column, so no flasher is fitted here."
				)
			if address in {34, 35}:
				notes += (
					" Fliptronic upper-flipper circuit; Cactus Canyon has no upper flippers, and unlike its sibling "
					"address (33 Move Bart Toy power / 36 Bart Toy Hat hold) this half of the pair is not repurposed."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias."
				)
			if address in {37, 38}:
				notes += (
					" WPC-95 LPDC output; PinMAME duplicates it at public address "
					f"{41 if address == 37 else 42}, so a recreation must treat {address} and "
					f"{41 if address == 37 else 42} as one physical DC-motor drive line, not an additional device. "
					"The A-22271 Train Motor Circuits assembly (gates U3A/U3B for reverse, U3C/U3D for forward) "
					"drives the train motor as an H-bridge."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-95 power driver board", "driver_transistor": wiring_data["driver_transistor"]}
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			if address in FLIPPER_DRIVE_WIRE:
				wiring["control_wire"] = FLIPPER_DRIVE_WIRE[address]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if not fitted:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				if address in FLASHER_POSITIONS:
					extra["spatial"] = located(identifier, role, FLASHER_POSITIONS[address], VPX_TABLE_SOURCE)
				else:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {7, 23}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = {
			29: "WPC J111 General-Purpose Mirror A", 30: "WPC J111 General-Purpose Mirror B",
			31: "PinMAME Game-On State", 32: "PinMAME Reserved State",
			39: "Unused LPDC Output 39", 40: "Unused LPDC Output 40",
			41: "Train Reverse LPDC Mirror", 42: "Train Forward LPDC Mirror",
			43: "Unused LPDC Mirror 43", 44: "Unused LPDC Mirror 44",
			49: "PinMAME Simulator Ball Shooter", 50: "Reserved Custom-Output Boundary",
			**{n: f"Unused Custom Solenoid {n}" for n in range(51, 65)},
		}[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41, 42} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Cactus Canyon playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Cactus Canyon playfield device.",
			31: "PinMAME's synthetic game-on state. Cactus Canyon sets wpc_set_fastflip_addr(0x87), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			39: "Unused WPC-95 LPDC general-purpose output; Cactus Canyon populates only LPDC outputs 37 and 38.",
			40: "Unused WPC-95 LPDC general-purpose output; Cactus Canyon populates only LPDC outputs 37 and 38.",
			41: "PinMAME's backward-compatibility mirror of LPDC output 37 (Train Reverse). It reports the same physical H-bridge drive line and is not an additional device.",
			42: "PinMAME's backward-compatibility mirror of LPDC output 38 (Train Forward); see 41.",
			43: "Unused WPC-95 LPDC mirror of output 39.",
			44: "Unused WPC-95 LPDC mirror of output 40.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. ccGameData declares no custSol.",
		}.get(address, "Unused above the custom-output boundary; ccGameData declares no custSol.")
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42} else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in MANUAL_SOLENOID_ALIASES:
			virtual_aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=virtual_aliases,
				roles=roles,
				physical={"notes": notes},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			unused = address in LAMP_UNUSED_ADDRESSES
			label = SWITCH_LABELS.get(address) if False else LAMP_LABELS.get(address)
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES.get(address, (None, None))
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address == 23:
				notes += (
					" The retained VPX table binds a second Light object (l23a) at a genuinely different "
					"coordinate, but the manual's Lamp Locations entry for this item (04-12353, one #555 bulb, one "
					"24-8767 socket) documents exactly one physical bulb; l23a is excluded as a table-only second "
					"render object, not promoted to a second placement."
				)
			physical["notes"] = notes

			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": {
					"board": "WPC-95 power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The lamp-locations parts list marks this position Not Used."
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					availability,
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-95 power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter "
				"coordinate come from the retained table's GI emitter collection for this string (UpdateGI in the "
				"retained script). GI address 0 drives collection LeftGI (10 physical bulb positions from 19 raw "
				"members, clustered within 25px); GI address 1 drives RightGI (12 from 24 raw members, one an "
				"authoring duplicate); GI address 2 drives TopGI plus TopGI2 (16 from 32 raw members; TopGI2's "
				"three members are additional VR-room-only render duplicates of three TopGI bulbs, not new "
				"positions)."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination; the retained script's UpdateGI handles only GI addresses 0-2 "
				"(Case 0/1/2), so this string has no playfield coordinate."
			)
			if address == 4:
				notes += " This string additionally feeds cabinet bulbs through J104, the only cabinet connection on the printed general-illumination wiring page."
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(
			_device(
				identifier,
				label,
				"gi",
				"pinmame.output.gi",
				address,
				"used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
				**extra,
			)
		)
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(
		identifier: str,
		label: str,
		kind: str,
		actuators: list[str],
		sensors: list[str],
		behavior: str,
		positions: list[tuple[str, str, list[str], str]],
		*refs: str,
		assembly_part_number: str | None = None,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [
				{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
				for position_id, position_label, position_sensors, description in positions
			]
		return record

	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on trough optos 32-35, with Trough Ball 1 (32) nearest the eject coil and Trough Ball 4 "
			"(35, drain entrance) furthest. Solenoid 9 (ReleaseBall) ejects the resting ball; the retained script's "
			"UpdateTrough/ReleaseBall handlers manage the shift and pulse trough-eject opto 31 as the ejected ball "
			"leaves. All five positions are printed optos on the A-18617-1/A-18618-1 Trough IR LED/Photo Transistor "
			"PCB pair, rest closed, and are normalized by ccGameData's inverted-switch mask (column 3, bits 0-4).",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"The ball ejected from the trough rests on shooter-lane switch 18 and auto-plunger coil 1 (AutoPlunger "
			"callback) launches it; there is no manual plunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21022-1",
		),
		mechanism(
			"mechanism.drop-target-bank",
			"Four-target drop bank",
			"drop_target_bank",
			[output_id("Left Drop Target"), output_id("Left Center Drop Target"), output_id("Right Center Drop Target"), output_id("Right Drop Target")],
			["switch.matrix-61", "switch.matrix-62", "switch.matrix-63", "switch.matrix-64"],
			"Four independent drop targets in ascending playfield-x order (61 Left, 62 Left Center, 63 Right Center, "
			"64 Right), each with its own reset coil (solenoids 2-5, callbacks Drop1-Drop4) and mechanical switch "
			"(A-22296-1/-2, part 5647-12693-21).",
			[
				("left", "Drop target 1 (left)", ["switch.matrix-61"], "Leftmost target."),
				("left-center", "Drop target 2 (left center)", ["switch.matrix-62"], "Left-center target."),
				("right-center", "Drop target 3 (right center)", ["switch.matrix-63"], "Right-center target."),
				("right", "Drop target 4 (right)", ["switch.matrix-64"], "Rightmost target."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22296",
		),
		mechanism(
			"mechanism.mine-popper",
			"Mine popper",
			"kicker",
			[output_id("Mine Popper")],
			["switch.matrix-41"],
			"A ball resting in the mine hole on opto 41 (Mine Popper) is kicked back to the playfield by solenoid 6 "
			"(SolMinePopper callback); the retained script's MineHole_Hit/MinePopper_Hit handlers animate the "
			"kickout.",
			[("held", "Ball in the mine popper", ["switch.matrix-41"], "Mine popper opto.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22467",
		),
		mechanism(
			"mechanism.saloon-popper",
			"Saloon popper",
			"kicker",
			[output_id("Saloon Popper")],
			["switch.matrix-42"],
			"A ball resting in the saloon hole on opto 42 (Saloon Popper) is kicked back to the playfield by "
			"solenoid 8 (SolSaloonPopper callback); the retained script's BartHole_Hit/BartPopper_Hit handlers "
			"animate the kickout. The retained table names the physical kicker object \"bartpopper\" and adds a "
			"co-located script-only \"secretentrance\" kicker at the identical coordinate, which is excluded here "
			"as a duplicate of the same physical device rather than a second one.",
			[("held", "Ball in the saloon popper", ["switch.matrix-42"], "Saloon popper opto.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22435",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot assembly (A-17801) carries a kick switch (A-17800/SW-1A-114) and a separate scored "
			"switch (A-17794/SW-1A-120) with a diode attached, matching switch matrix rows 51/52.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17801",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-55"],
			"Left (B-12030-2/A-16443, switch 53) and Right (B-12030-2/A-16443, switch 54) are native round VPX "
			"Bumper objects; Bottom (A-23146, switch 55) is modeled in the retained table as a slingshot-style Wall "
			"object (sw55, with its own sw55_Slingshot/sw55_Timer handlers) rather than a round bumper ring -- a "
			"table-authoring choice, not a missing device, and it is grouped with the two true slingshots in "
			"vpmNudge.TiltObj. By normalized x, Left (0.1603) sits left of Right (0.3377); Bottom's y (0.2065) is "
			"greater than both (0.1642, 0.1246), i.e. closer to the player, matching its name.",
			[
				("left", "Left jet bumper", ["switch.matrix-53"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-54"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-55"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.gunfight-posts",
			"Left and right gunfight posts",
			"gate",
			[output_id("Left Gunfight Post"), output_id("Right Gunfight Post")],
			[],
			"Solenoids 14/15 (GunPostLeft/GunPostRight callbacks) raise and lower two posts (retained table objects "
			"LPin/RPin) that block the Left Out/Right Out lanes; there is no printed switch dedicated to either "
			"post.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22465",
		),
		mechanism(
			"mechanism.loop-gates",
			"Left and right loop gates",
			"gate",
			[output_id("Left Loop Gate"), output_id("Right Loop Gate")],
			[],
			"Solenoids 21/22 (LGate/RGate callbacks) operate one-way gates admitting a ball into the left/right "
			"loops; the printed solenoid table classifies their driver circuit as \"Flasher\" type rather than a "
			"coil, consistent with a brief pulsed gate rather than a sustained-current device.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22482",
		),
		mechanism(
			"mechanism.mine-sign",
			"Motorized mine entrance sign",
			"motorized",
			[output_id("Mine Motor")],
			["switch.matrix-77", "switch.matrix-78", "switch.matrix-15"],
			"Solenoid 17 (MoveMine callback in the retained script's PROC=0 branch) raises and lowers the Mine sign "
			"(retained Primitive MineSign) between a low and high position via MineTimer_Timer, which also drops or "
			"raises the Mine Entrance wall (switch 15's IsDropped flag) as the sign passes a threshold. Mine Home "
			"(77) and Mine Encoder (78) are the printed position/step optos on the A-22443 Mine Dual Opto PCB, but "
			"the retained script's PROC=0 path (MoveMine/MineTimer_Timer) never sets Controller.Switch for either "
			"address -- only the PROC=1 path (Sw15_Timer/sw15b_Timer, community P-ROC hardware) exercises them -- so "
			"their causal timing here rests on the manual and PinMAME's addressing rather than an observed script "
			"behavior under the physical ROM's normal path.",
			[
				("home", "Mine sign home/lowered", ["switch.matrix-77"], "Position opto."),
				("encoder", "Mine motor encoder pulse", ["switch.matrix-78"], "Step/encoder opto."),
				("entrance", "Mine entrance wall", ["switch.matrix-15"], "Drops/raises with sign position."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22404",
		),
		mechanism(
			"mechanism.train",
			"Motorized train on tracks",
			"motorized",
			[output_id("Train Reverse"), output_id("Train Forward")],
			["switch.matrix-71", "switch.matrix-72"],
			"Solenoids 37/38 (TrainB/TrainF callbacks in the retained script's PROC=0 branch) drive the Train "
			"primitive back and forth along the track via an H-bridge (A-22271 Train Motor Circuits assembly, gates "
			"U3A/U3B reverse and U3C/U3D forward) toward TrainMech.Position; TrainTimer_Timer animates the running "
			"gears and stops the motor once the target position is reached and the solenoid is released. Train "
			"Encoder (71) is pulsed once per timer tick by a dedicated VPX Timer object (sw71) while the train is "
			"in motion (\"Dozer - Encoder Pulse which runs with Train Mech.\"). Train Home (72) is never set by the "
			"retained script's PROC=0 path at all (only the PROC=1 Polly_Timer path, community P-ROC hardware, sets "
			"it); its causal timing here rests on the manual and PinMAME's addressing.",
			[
				("encoder", "Train motor encoder pulse", ["switch.matrix-71"], "Pulsed each timer tick while running."),
				("home", "Train home position", ["switch.matrix-72"], "Home/rest position opto."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22271",
		),
		mechanism(
			"mechanism.bart-toy",
			"Bart figure and hat toy",
			"motorized",
			[output_id("Move Bart Toy"), output_id("Bart Toy Hat")],
			["switch.matrix-75"],
			"Solenoid 33 (MoveBart callback) oscillates the Bart figure left/right along the X axis for as long as "
			"it is held on (Bart1_Timer); solenoid 36 (MoveHat callback) lifts the hat and returns it (Bart2_Timer/"
			"BHit_Timer sine-style Y animation). Saloon Bart Toy switch 75 senses a ball hitting the figure "
			"(BartHole_Hit). Both solenoids repurpose printed Fliptronic upper-flipper circuit positions (33/34 "
			"would be upper-right flipper power/hold, 35/36 upper-left) because the machine has no upper flippers; "
			"only one half of each pair is actually used (33 power, 36 hold), leaving 34/35 genuinely unused.",
			[("hit", "Ball strikes the Bart figure", ["switch.matrix-75"], "Saloon Bart Toy switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22432",
		),
		mechanism(
			"mechanism.saloon-gate",
			"Saloon gate",
			"gate",
			[],
			["switch.matrix-73"],
			"A mechanical switch (part 5647-12693-11) on a gate near the saloon; the retained table has no "
			"dedicated solenoid driving this gate, only the sensing switch.",
			[("sensed", "Ball passes the saloon gate", ["switch.matrix-73"], "Saloon gate switch.")],
			MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two flippers (A-14876-R right, A-15849-L left, coil FL-11630) on Fliptronic circuits. Each flipper has "
			"a separate power and hold winding: the ROM energizes the power winding on the cabinet button opto (112 "
			"right, 114 left), then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 "
			"left) closes. There are no upper flippers; the upper-flipper Fliptronic circuits (33-36, 115, 116, "
			"117, 118) are either unfitted or repurposed for the Bart toy.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14876-R right with A-15849-L left",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough Eject"),
			"destination": "switch.matrix-31",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return []


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items: list[dict[str, Any]] = []
	for driver_id in DRIVER_IDS:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		items.append(item)
	return items


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "bally.cactus-canyon.1998",
			"name": "Cactus Canyon",
			"manufacturer": "Bally",
			"year": 1998,
			"kind": "physical_pinball",
			"ipdb_id": 4445,
			"opdb_id": "G4835-Mb5eO",
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-95",
			"hardware_generation": "0x80",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/cactus-canyon-1998.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Cactus Canyon device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	for device in definition["inputs"]:
		if device["spatial"]["status"] != "not_applicable":
			placement_count += len(device["spatial"]["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"Flasher addresses 24 (Beacon Flasher) and 26 (Saloon Flasher) each drive a documented playfield-plus-"
			"insert-panel bulb pair (Solenoid/Flasher Locations page 2-36 lists each twice), but the retained VPX "
			"table's Light-object clusters for both addresses are co-located or only a few pixels apart, so only "
			"one resolvable coordinate is recorded for each rather than two. No coordinate was invented to fill the "
			"gap. Every other spatial dimension this report audits is complete.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2162.0},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/cactus-canyon-1998/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.cactus-canyon.1998/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/cactus-canyon-1998/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"vpx_geometry": {
				"path": "external:pinmame-review-artifacts/cactus-canyon-1998/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"l23a co-located-but-distinct second Light object bound to lamp 23 (manual documents one bulb)",
			"secretentrance Kicker (co-located duplicate of bartpopper/switch 42, solenoid 8)",
			"l1, l2 Light objects (never referenced by SetLamp/SetLampMod; no valid WPC-95 lamp address)",
			"light006, light007, light034 (TopGI2 VR-room-only render duplicates of light16, light17, light15)",
			"light004 listed twice in the RightGI collection (authoring duplicate, one physical bulb)",
		],
		"unresolved": [
			"Flasher 24 (Beacon Flasher) insert-panel bulb coordinate distinct from its playfield bulb.",
			"Flasher 26 (Saloon Flasher) insert-panel bulb coordinate distinct from its playfield bulb.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Cactus Canyon (Bally, 1998) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete except two flasher "
		"addresses (24, 26) whose second documented bulb has no independently resolvable coordinate; the physical "
		"machine record stays `partial` at `machines/partial/bally/cactus-canyon-1998.json` for that reason alone "
		"-- no polarity conflict was found for this machine (see the opto sweep in the manual transcription).",
		"",
		"The matching source is the retained known-working `Cactus Canyon (Bally 1998) VPW 1.0.2.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and y/2162 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Bally operations manual is "
		"the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; "
		"the retained table supplies geometry.",
		"- The retained manual PDF has a fresh OCR text layer, so every printed table used here was extracted with "
		"`pdftotext -layout` and then confirmed against the rendered page image; the transcription in "
		"`external:pinmame-review-artifacts/cactus-canyon-1998/manual-transcription.md` is the source of record "
		"whenever OCR and the rendered page disagree.",
		"- The opto sweep checked both manual cues (matrix shading and a populated Opto Assembly Part Number with "
		"a blank Switch Part Number, cross-referenced against the board-assembly pages) column by column against "
		"ccGameData's inverted-switch mask and found full agreement: every physically normally-closed opto switch "
		"(31-37, 41-42, 71, 77, 78, plus the Fliptronic 112/114 button optos handled by WPC-95's own hardware "
		"inversion) is normalized by the emulator. No `conflict.*-opto-not-normalized` entry was needed.",
		"- Switches 71/72 (Train Encoder/Home) and 77/78 (Mine Home/Encoder) have no dedicated playfield trigger "
		"object because the retained script's PROC=0 (physical ROM) path either drives them from a Timer object "
		"tied to mechanism motion (71) or does not set them at all (72, 77, 78 -- only the PROC=1 community P-ROC "
		"path does). All four are documented projections onto the Train or Mine mechanism's own retained table "
		"object.",
		"- GI strings 0-2 use the retained table's LeftGI/RightGI/TopGI(+TopGI2) emitter collections, matching the "
		"retained script's `UpdateGI` dispatch exactly; each collection's members were clustered within 25px to "
		"collapse render-doubled Light objects into one placement per physical bulb. GI strings 3 and 4 are "
		"backbox insert-panel/cabinet circuits and take a controlled `cabinet_or_service` record.",
		"- Solenoids 41/42 are PinMAME's LPDC mirror of the physical train-motor drive lines 37/38 and are declared "
		"virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No switch-polarity conflict, unnamed required address, or missing physical/controller variant remains for "
		"this machine, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. However, flasher addresses 24 and 26 each document two fitted bulbs (playfield plus "
		"insert-panel) on the printed Solenoid/Flasher Locations page, and the retained table's Light-object "
		"evidence for both addresses cannot be split into two independently resolvable coordinates -- inventing a "
		"second coordinate is explicitly forbidden, so each keeps exactly one placement. `coverage.missing` is "
		"`[\"spatial_placement\"]` and `coverage.dimensions.spatial_placement = \"candidate\"`, so promotion to "
		"`author_ready` is refused; the record stays `partial` until a second distinguishable insert-panel bulb "
		"position is found (a higher-resolution table revision, a playfield photograph, or a runtime harness trace "
		"that separately drives the two physical lamps).",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- Retained VPX geometry dump of every named object used by this definition, SHA-256 "
		f"`{VPX_GEOMETRY_SHA256}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale_author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready.exists():
		stale_author_ready.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_author_ready_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready_path.exists():
		raise RuntimeError(f"Stale Cactus Canyon author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Cactus Canyon definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Cactus Canyon seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Cactus Canyon definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Cactus Canyon seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Cactus Canyon spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Cactus Canyon spatial review drifted from its deterministic curator: {markdown_path}")
	print("Cactus Canyon definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Cactus Canyon extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Cactus Canyon retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
