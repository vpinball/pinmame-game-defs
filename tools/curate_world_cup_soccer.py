"""Curate the physical Bally/Midway World Cup Soccer (1994) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail,
and normalized coordinate as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: switches 112/114 (Fliptronic F2/F4) are printed opto interrupters that pinned
# PinMAME's wcsGameData inverted-switch mask does not normalize (column 11 is 0x00), and solenoid
# 34 (Loop Gate) has no VPX object or script reference of any kind, so its spatial key is omitted
# entirely rather than fabricated -- see conflict.flipper-cabinet-opto-not-normalized below.
PARTIAL_PATH = ROOT / "machines/partial/midway/world-cup-soccer-1994.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/midway/world-cup-soccer-1994.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/midway/world-cup-soccer-1994.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/midway/world-cup-soccer-1994.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/midway/world-cup-soccer-1994.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
MANUAL_SOURCE = "manual.midway.world-cup-soccer.1994"
MANUAL_SUPPORT_SOURCE = "manual-support.midway.world-cup-soccer.1994"
VPX_TABLE_SOURCE = "vpx-table.wcs-vpw-1-5"
VPX_SCRIPT_SOURCE = "vpx-script.wcs-vpw-1-5"
VPX_EXTRACTION_SOURCE = "vpx-extraction.wcs-vpw-1-5"

TABLE_SHA256 = "ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d"
SCRIPT_SHA256 = "c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5"
MANUAL_SHA256 = "29fd3c44c9ddcf5f965270011c71d34a701c13095cbeb286e26e62201931e48e"
MANUAL_TRANSCRIPTION_SHA256 = "7055d31403f69bedd4dffa94aad45952c18e75065941e204338eb9a818690f75"

EXTRACTION_RELATIVE_PATH = Path("midway/world-cup-soccer-1994/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("midway/world-cup-soccer-1994/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "eab6beeaca073c66c01cacaee71d605f3629832062e56f67d92a31405d438032"
EXTRACTION_FILE_COUNT = 2588
EXTRACTION_TOTAL_BYTES = 773038506

TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=2152.941"

DRIVER_IDS = (
	"wcs_l2", "wcs_l3c", "wcs_la2", "wcs_l1", "wcs_la1", "wcs_d2",
	"wcs_p2", "wcs_p5", "wcs_p3", "wcs_p6",
	"wcs_f10", "wcs_f50", "wcs_f62", "wcs_f62b",
)
DRIVER_COMPATIBILITY = {
	"wcs_l2": ("identical", "Bally production LX-2 game ROM shipped with the physical machine; the parent of the wcs clone tree."),
	"wcs_l3c": ("identical", "2016 community LX-3C 'Competition MOD' firmware; a later firmware revision for the identical physical hardware and controller addresses, not a new machine."),
	"wcs_la2": ("identical", "Bally LA-2 language/region firmware revision of the same physical machine."),
	"wcs_l1": ("identical", "Bally LX-1 earlier firmware revision of the same physical machine."),
	"wcs_la1": ("identical", "Bally LA-1 earlier language/region firmware revision of the same physical machine."),
	"wcs_d2": ("identical", "Bally DX-2 'LED Ghost Fix' firmware revision of the same physical machine."),
	"wcs_p2": ("identical", "Bally PA-2 prototype game ROM for the same physical machine."),
	"wcs_p5": ("identical", "Bally PA-5 'LED Ghost Fix' prototype-lineage firmware revision of the same physical machine."),
	"wcs_p3": ("identical", "Bally PX-3 prototype game ROM for the same physical machine."),
	"wcs_p6": ("identical", "Bally PX-6 'LED Ghost Fix' prototype-lineage firmware revision of the same physical machine."),
	"wcs_f10": ("compatible", "FreeWPC 0.10 community firmware; a from-scratch reimplementation that runs on the identical physical WPC-Security hardware and controller addresses."),
	"wcs_f50": ("compatible", "FreeWPC 0.50 community firmware for the identical physical hardware."),
	"wcs_f62": ("compatible", "FreeWPC 0.62 community firmware for the identical physical hardware."),
	"wcs_f62b": ("compatible", "FreeWPC 0.62b (2020) community firmware for the identical physical hardware."),
}

# --- Printed switch matrix (manual page 2-46 wiring, 2-46/2-47 switch-locations parts list).
SWITCH_LABELS = {
	12: "Magna Goalie Button", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Left Flipper Lane",
	16: "Striker 3 (High)", 17: "Right Return Lane", 18: "Right Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy Extra Ball", 24: "Always Closed",
	25: "Free Kick Target", 26: "Kickback Upper", 27: "Spinner", 28: "Light Kickback",
	31: "Trough 1 (Right)", 32: "Trough 2", 33: "Trough 3", 34: "Trough 4", 35: "Trough 5 (Left)",
	36: "Trough Stack", 37: "Light Magna Goalie", 38: "Ball Shooter",
	41: "Goal Trough", 42: "Goal Popper Opto", 43: "Goalie Is Left", 44: "Goalie Is Right",
	45: "TV Ball Popper", 47: "Travel Lane Rollover", 48: "Goalie Target",
	51: "Skill Shot Front", 52: "Skill Shot Center", 53: "Skill Shot Rear",
	54: "Right Eject Hole", 55: "Upper Eject Hole", 56: "Left Eject Hole",
	61: "Rollover 1 (High)", 62: "Rollover 2", 63: "Rollover 3", 64: "Rollover 4 (Low)",
	65: "Tackle Switch", 66: "Striker 1 (Left)", 67: "Striker 2 (Center)",
	71: "Left Ramp Diverted", 72: "Left Ramp Entrance", 74: "Left Ramp Exit",
	75: "Right Ramp Entrance", 76: "Lock Mech. Low", 77: "Lock Mech. High", 78: "Right Ramp Exit",
	81: "Left Jet Bumper", 82: "Upper Jet Bumper", 83: "Lower Jet Bumper",
	84: "Left Slingshot", 85: "Right Slingshot", 86: "Kickback",
	87: "Upper Left Lane", 88: "Upper Right Lane",
}
# Printed matrix positions marked "Not Used" on both the switch-matrix page (2-46) and the
# switch-locations parts list (2-46/2-47).
UNUSED_MATRIX_ADDRESSES = {11, 46, 57, 58, 68, 73}
# Every switch shaded "Opto, Typically Closed" on the printed switch matrix (2-46): trough optos,
# the Goal/Goalie hole optos, and the Skill Shot optos. All physically normally-closed.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 51, 52, 53}
# wcsGameData's inverted-switch mask {0x00,0x00,0x00,0x3f,0x1f,0x07,...} covers columns 3, 4, and
# 5 in full -- exactly the same fourteen addresses shaded on the printed matrix. Zero disagreement
# in the ordinary 8x8 matrix (see conflict.flipper-cabinet-opto-not-normalized for the Fliptronic
# column, which is a separate, twelfth mask element).
PINMAME_NORMALIZED_OPTO_SWITCHES = set(OPTO_SWITCHES)
# vpmTimer.PulseSw / momentary-target callers in the retained VPW script.
PULSED_SWITCHES = {36, 48, 84, 85}

SWITCH_TYPES = {
	12: "button", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch",
	17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch", 23: "button",
	24: "other", 25: "microswitch", 26: "microswitch", 27: "other", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto",
	37: "microswitch", 38: "microswitch",
	41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto",
	47: "microswitch", 48: "microswitch",
	51: "opto", 52: "opto", 53: "opto",
	54: "microswitch", 55: "microswitch", 56: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch",
	65: "leaf", 66: "microswitch", 67: "microswitch",
	71: "microswitch", 72: "microswitch", 74: "microswitch", 75: "microswitch",
	76: "microswitch", 77: "microswitch", 78: "microswitch",
	81: "leaf", 82: "leaf", 83: "leaf", 84: "leaf", 85: "leaf",
	86: "microswitch", 87: "microswitch", 88: "microswitch",
}

# address -> (assembly/part-number transcription, description) from switch-locations.md.
SWITCH_PARTS = {
	12: "SW-1A-195", 13: "20-9663-1", 14: "A-15361", 15: "5647-12693-19", 16: "A-18530-4",
	17: "5647-12693-19", 18: "5647-12693-19", 21: "A-17238", 22: "5643-09288-00",
	23: "20-9663-D-1", 24: "5643-09112-00", 25: "A-18504", 26: "5647-12693-19",
	27: "5647-12133-08", 28: "A-18059-4",
	31: "A-18618 Transistor with A-18617 LED", 32: "A-18618 Transistor with A-18617 LED",
	33: "A-18618 Transistor with A-18617 LED", 34: "A-18618 Transistor with A-18617 LED",
	35: "A-18618 Transistor with A-18617 LED", 36: "A-18618 Transistor with A-18617 LED",
	37: "A-18059-4", 38: "5647-12693-32",
	41: "A-16908 LED with A-16909 Transistor", 42: "A-16908 LED with A-16909 Transistor",
	43: "A-16908 LED with A-16909 Transistor", 44: "A-16908 LED with A-16909 Transistor",
	45: "A-16908 LED with A-16909 Transistor",
	47: "5647-12693-19", 48: "A-17779",
	51: "A-16908 LED with A-16909 Transistor", 52: "A-16908 LED with A-16909 Transistor",
	53: "A-16908 LED with A-16909 Transistor",
	54: "5647-12133-11", 55: "5647-12133-11", 56: "5647-12133-11",
	61: "SW-11A-37", 62: "SW-11A-37", 63: "SW-11A-37", 64: "SW-11A-37",
	65: "SW-1A-120", 66: "A-18530-15", 67: "A-18530-15",
	71: "5647-12693-21", 72: "5647-12693-11", 74: "5647-12693-21", 75: "5647-12693-11",
	76: "5647-12693-17", 77: "5647-12693-17", 78: "5647-12693-21",
	81: "SW-11A-37", 82: "SW-11A-37", 83: "SW-11A-37",
	84: "SW-1A-114 (kicker) with SW-1A-120 (score)", 85: "SW-1A-114 (kicker) with SW-1A-120 (score)",
	86: "5647-12693-19", 87: "5647-12693-19", 88: "5647-12693-19",
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"),
	3: ("Green-Orange", "J207-3", "U20-16"), 4: ("Green-Yellow", "J207-4", "U20-15"),
	5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"),
	3: ("White-Orange", "J209-3", "U18-5"), 4: ("White-Yellow", "J209-4", "U18-7"),
	5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
}

# --- Normalized playfield coordinates from the retained VPWmod v1.5 extraction, x/952.941,
# y/2152.941 (review-artifacts/world-cup-soccer/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.142011, 0.723795)], 16: [(0.587716, 0.190379)], 17: [(0.797591, 0.740516)],
	18: [(0.869199, 0.73387)], 25: [(0.615848, 0.383632)], 26: [(0.05614, 0.583273)],
	27: [(0.137125, 0.370745)], 28: [(0.158295, 0.578902)],
	31: [(0.866298, 0.871273)], 32: [(0.804222, 0.884604)], 33: [(0.743689, 0.899022)],
	34: [(0.681109, 0.914307)], 35: [(0.615701, 0.929855)],
	36: [(0.866298, 0.871273)],
	37: [(0.828183, 0.59066)], 38: [(0.936637, 0.885851)],
	41: [(0.452139, 0.105679)], 42: [(0.551305, 0.094105)],
	43: [(0.392886, 0.130754)], 44: [(0.392886, 0.130754)],
	45: [(0.666035, 0.42875)], 47: [(0.09245, 0.180697)], 48: [(0.936637, 0.885851)],
	51: [(0.940379, 0.656217)], 52: [(0.940414, 0.619239)], 53: [(0.941414, 0.583052)],
	54: [(0.811735, 0.513571)], 55: [(0.333895, 0.233738)], 56: [(0.183415, 0.543272)],
	61: [(0.442139, 0.253514)], 62: [(0.445228, 0.334186)], 63: [(0.476917, 0.413224)],
	64: [(0.534627, 0.489792)], 65: [(0.342183, 0.300407)], 66: [(0.2381, 0.41726)],
	67: [(0.358816, 0.376317)],
	71: [(0.063638, 0.132172)], 72: [(0.270678, 0.338593)],
	74: [(0.934231, 0.195316)], 75: [(0.80764, 0.425492)],
	76: [(0.090145, 0.608522)], 77: [(0.089815, 0.584659)], 78: [(0.063323, 0.427613)],
	81: [(0.835502, 0.119845)], 82: [(0.819085, 0.214142)], 83: [(0.63906, 0.159845)],
	84: [(0.24397, 0.729801)], 85: [(0.695279, 0.730838)],
	86: [(0.057698, 0.776961)], 87: [(0.656175, 0.075897)], 88: [(0.746263, 0.076408)],
}
SWITCH_PROJECTIONS = {
	36: "Projected onto the trough eject Kicker (Trigger/Kicker sw31, table object center): the retained script's SolTrough handler fires sw31.kick and vpmTimer.PulseSw 36 in the same event (no separate playfield object represents Trough Stack), and pinned PinMAME's own sim ball-routing table (wcs_stateDef) places the 'Trough stack' state immediately after the 'Trough 1' eject state in the ball's path toward the shooter lane.",
	43: "Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center): the retained script's InitGoalie sets BP_goalkeeper.x=376/.y=280, matching this primitive's own position (374.4,281.5) almost exactly, and wcs_handleMech sets public switches 43/44 directly from the DC-motor position counter (mech_getPos(0)) rather than from a fixed playfield sensor object.",
	44: "Projected onto the rotating goalie figure (Primitive BM_goalkeeper, table object center); see switch 43.",
	48: "Projected onto the shooter-lane switch/plunger position (Trigger.swPlunger, identical coordinates to Trigger.sw38): the retained script's GWalls_Hit handler (triggered when a ball strikes the goalie's 35-segment target-wall ring) pulses public switch 48 without a dedicated playfield sensor object of its own; the coordinate used here is the nearest fixed reference in the same script region rather than an invented target-wall centroid.",
}

SOLENOID_LABELS = {
	1: "Goal Popper", 2: "TV Popper", 3: "Kickback", 4: "Lock Release", 5: "Upper Eject Hole",
	6: "Trough", 7: "Knocker", 8: "Ramp Diverter",
	9: "Left Jet Bumper", 10: "Upper Jet Bumper", 11: "Lower Jet Bumper",
	12: "Left Slingshot", 13: "Right Slingshot", 14: "Right Eject Hole", 15: "Left Eject Hole",
	16: "Diverter Hold",
	17: "Goal Cage Top", 18: "Goal", 19: "Skill Shot", 20: "Jet Bumpers", 21: "Goalie Drive",
	22: "Spinning Ball", 23: "Ball Clockwise", 24: "Ball Counter-Clockwise",
	25: "Left Ramp Entrance", 26: "Lock Area", 27: "Flipper Lanes", 28: "Ramp Rear",
	33: "Magna Goalie", 34: "Loop Gate", 35: "Lock Magnet",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {36: "Not Used Upper Left Flipper Hold"}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40",
	41: "Unused WPC-Security Output 41", 42: "Unused WPC-Security Output 42",
	43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
	51: "Ramp Diverter State (custom mirror of solenoids 8 and 16)",
}
# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(control_connection="J107-2", driver_transistor="Q82", power_connection="J130-1", part_number="AE-23-800", printed_type="High Power"),
	2: dict(control_connection="J107-2", driver_transistor="Q80", power_connection="J130-2", part_number="AE-26-1500", printed_type="High Power"),
	3: dict(control_connection="J107-2", driver_transistor="Q78", power_connection="J130-4", part_number="AE-23-800", printed_type="High Power"),
	4: dict(control_connection="J107-2", driver_transistor="Q76", power_connection="J130-5", part_number="AE-26-1500", printed_type="High Power"),
	5: dict(control_connection="J107-2", driver_transistor="Q64", power_connection="J130-6", part_number="AE-26-1200", printed_type="High Power"),
	6: dict(control_connection="J107-2", driver_transistor="Q66", power_connection="J130-7", part_number="AE-26-1500", printed_type="High Power"),
	7: dict(control_connection="J107-2 (Backbox)", driver_transistor="Q68", power_connection="J130-8 (Backbox)", part_number="AE-23-800", printed_type="High Power (Backbox)"),
	8: dict(control_connection="J107-2", driver_transistor="Q70", power_connection="J130-9", part_number="FL-11753-1", printed_type="High Power"),
	9: dict(control_connection="J107-3", driver_transistor="Q58", power_connection="J127-1", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(control_connection="J107-3", driver_transistor="Q56", power_connection="J127-3", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(control_connection="J107-3", driver_transistor="Q54", power_connection="J127-4", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(control_connection="J107-3", driver_transistor="Q52", power_connection="J127-5", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J107-3", driver_transistor="Q50", power_connection="J127-6", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J107-3", driver_transistor="Q48", power_connection="J127-7", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J107-3", driver_transistor="Q46", power_connection="J127-8", part_number="AE-26-1200", printed_type="Low Power"),
	16: dict(control_connection="J107-2", driver_transistor="Q44", power_connection="J127-9", part_number="FL-11753-1", printed_type="Low Power"),
	17: dict(control_connection="J107-6 / J106-5", driver_transistor="Q42", power_connection="J126-1 / J125-1", printed_type="Flasher"),
	18: dict(control_connection="J107-6 / J106-5", driver_transistor="Q40", power_connection="J126-2 / J125-2", printed_type="Flasher"),
	19: dict(control_connection="J107-6 / J106-5", driver_transistor="Q38", power_connection="J126-3 / J125-3", printed_type="Flasher"),
	20: dict(control_connection="J107-6 / J106-5", driver_transistor="Q36", power_connection="J126-4 / J125-5", printed_type="Flasher"),
	21: dict(control_connection="J116-2", driver_transistor="Q28", power_connection="J126-5", part_number="14-7997", printed_type="Flasher (printed category; +12VDC motor drive line)"),
	22: dict(control_connection="J107-6", driver_transistor="Q30", power_connection="J126-6", printed_type="Flasher"),
	23: dict(control_connection="J116-2", driver_transistor="Q34", power_connection="J126-7", part_number="14-7996", printed_type="Flasher (printed category; +12VDC motor drive line)"),
	24: dict(control_connection="J116-2", driver_transistor="Q32", power_connection="J126-8", part_number="14-7996", printed_type="Flasher (printed category; +12VDC motor drive line)"),
	25: dict(control_connection="J107-6 / J106-5", driver_transistor="Q26", power_connection="J122-1 / J124-1", printed_type="Gen. Purpose"),
	26: dict(control_connection="J107-6 / J106-5", driver_transistor="Q24", power_connection="J122-2 / J124-2", printed_type="Gen. Purpose"),
	27: dict(control_connection="J107-6 / J106-5", driver_transistor="Q22", power_connection="J122-3 / J124-3", printed_type="Gen. Purpose"),
	28: dict(control_connection="J107-6 / J106-5", driver_transistor="Q20", power_connection="J122-4 / J124-5", printed_type="Gen. Purpose"),
	33: dict(control_connection="J907-6,7", driver_transistor="Q2", power_connection="J902-6", part_number="20-9247", printed_type="High Power"),
	34: dict(control_connection="J907-6,7", driver_transistor="Q7", power_connection="J902-4", part_number="A-14406", printed_type="Low Power"),
	35: dict(control_connection="J907-8,9", driver_transistor="Q1", power_connection="J902-3", part_number="20-9247", printed_type="High Power"),
	45: dict(control_connection="J907-1", driver_transistor="Q4", power_connection="J902-11", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(control_connection="J907-1", driver_transistor="Q11", power_connection="J902-11", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(control_connection="J907-4", driver_transistor="Q3", power_connection="J902-7", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(control_connection="J907-4", driver_transistor="Q9", power_connection="J902-7", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "Yel-Grn", 46: "Org-Grn", 47: "Yel-Blu", 48: "Org-Blu", 33: "Yel-Vio", 34: "Org-Vio", 35: "Yel-Gry"}

SOLENOID_ASSEMBLIES = {
	1: "A-17839", 2: "A-18213", 3: "B-11873", 4: "A-18155", 5: "B-9362-R-3", 6: "A-16765",
	7: "B-10686-1", 8: "A-18138", 9: "A-9415-2", 10: "A-9415-2", 11: "A-9415-2",
	12: "B-9362-L-2", 13: "B-9362-R-3", 14: "B-9362-L-2", 15: "B-9362-L-2", 16: "A-18138",
	17: "A-12336-1", 18: "A-18384 with A-17803", 19: "A-12336-1 with A-17803", 20: "A-17803",
	21: "A-17741", 22: "A-17983", 23: "A-17569", 24: "A-17569", 25: "A-17983",
	26: "A-12336-1", 27: "A-17983", 28: "A-12336-1", 33: None, 34: "A-17796", 35: "A-18222",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
SOLENOID_CALLBACKS = {
	1: "SolGoalPopper", 2: "SolTVPopper", 3: "SolKickBack", 4: "SolLockRelease",
	5: "SolUpperEject", 6: "SolTrough", 7: "SolKnocker", 8: "SolRampDiverter",
	16: "SolRampDiverterHold", 17: "SolFlash17", 18: "SolFlash18", 19: "SolFlash19",
	20: "SolFlash20", 21: "SolGoalie", 22: "SolFlash22", 23: "SolBallMotorCW",
	24: "SolBallMotorCCW", 25: "SolFlash25", 26: "SolFlash26", 27: "SolFlash27",
	28: "SolFlash28", 47: "SolLFlipper (core.vbs sLLFlipper = 47)",
	45: "SolRFlipper (core.vbs sLRFlipper = 45)",
}
FLASHER_POSITIONS = {
	17: (0.353159, 0.116211), 18: (0.355793, 0.048587), 19: (0.837432, 0.945536),
	20: (0.745649, 0.161683), 22: (0.837775, 0.358024), 25: (0.233232, 0.300368),
	26: (0.042769, 0.273634), 27: (0.130976, 0.791652), 28: (0.168768, 0.029932),
}

SOLENOID_POSITIONS = {
	1: [(0.551305, 0.094105)], 2: [(0.666035, 0.42875)], 3: [(0.057771, 0.843687)],
	4: [(0.089815, 0.584659)], 5: [(0.333895, 0.233738)], 6: [(0.866298, 0.871273)],
	8: [(0.063638, 0.132172)],
	9: [(0.835502, 0.119845)], 10: [(0.819085, 0.214142)], 11: [(0.63906, 0.159845)],
	12: [(0.24397, 0.729801)], 13: [(0.695279, 0.730838)],
	14: [(0.811735, 0.513571)], 15: [(0.183415, 0.543272)], 16: [(0.063638, 0.132172)],
	17: [(0.353159, 0.116211)], 18: [(0.355793, 0.048587)], 19: [(0.837432, 0.945536)],
	20: [(0.745649, 0.161683)], 21: [(0.392886, 0.130754)], 22: [(0.837775, 0.358024)],
	23: [(0.704165, 0.318222)], 24: [(0.704165, 0.318222)],
	25: [(0.233232, 0.300368)], 26: [(0.042769, 0.273634)], 27: [(0.130976, 0.791652)],
	28: [(0.168768, 0.029932)],
	33: [(0.397875, 0.809245)], 35: [(0.117205, 0.499209)],
	45: [(0.641564, 0.846426)], 46: [(0.641564, 0.846426)],
	47: [(0.302754, 0.846244)], 48: [(0.302754, 0.846244)],
}

# --- Lamp matrix (manual page 2-44 wiring/locations, 2-45 continued).
LAMP_LABELS = {
	11: "Chicago \"P\"", 12: "Dallas \"U\"", 13: "Boston \"C\"", 14: "New York \"D\"",
	15: "Orlando \"L\"", 16: "Washington D.C. \"R\"", 17: "San Francisco \"O\"", 18: "Detroit \"W\"",
	21: "1 Goal", 22: "2 Goals", 23: "3 Goals", 24: "4 Goals Light TV", 25: "Speed (Ball)",
	26: "Spirit (Ball)", 27: "Skill (Ball)", 28: "Left Ticket Half",
	31: "Free Kick", 32: "TV Award", 33: "Ultra Ball", 34: "Ultra Ramps (Playfield)",
	35: "Strength (Ball)", 36: "Stamina (Ball)", 37: "Right Ticket Half", 38: "Tackle",
	41: "Kickback Low", 42: "Kickback Center", 43: "Kickback High", 44: "Right Ramp Build Lock",
	45: "Right Ramp Lock", 46: "Ultra Spinner (2)", 47: "Ultra Jets (2)", 48: "Striker Billboard",
	51: "Goal Jackpot", 52: "Extra Ball", 53: "Goal (2)", 54: "Upper Build Lock",
	55: "Light Magna Goalie", 56: "Right Flipper Lane", 57: "Shoot Again", 58: "Right Special",
	61: "Left Ramp Build Lock", 62: "Spinner Build Lock", 63: "Travel", 64: "Los Angeles",
	65: "Left Ramp Lock", 66: "Upper Left Lane", 67: "Upper Right Lane", 68: "Skill Shot Front",
	71: "Light Jackpot (2)", 72: "Final Draw", 73: "Magna-Goal Save", 74: "Left Flipper Lane",
	75: "Light Kickback", 76: "Left Ramp Buy Ticket", 77: "Right Ramp Buy Ticket",
	78: "Ultra Ramps (2)",
	81: "Rollover 1 (High)", 82: "Rollover 2", 83: "Rollover 3", 84: "Rollover 4 (Low)",
	85: "Skill Shot Rear", 86: "Skill Shot Center", 87: "Buy-in Button", 88: "Start Button",
}
LAMP_BULBS = {
	11: "#555", 12: "#555", 13: "#555", 14: "#555", 15: "#555", 16: "#555", 17: "#555", 18: "#555",
	21: "#555", 22: "#555", 23: "#555", 24: "#555", 25: "#555", 26: "#555", 27: "#555", 28: "#555",
	31: "#44", 32: "#44", 33: "#555", 34: "#555", 35: "#555", 36: "#555", 37: "#555", 38: "#44",
	41: "#555", 42: "#555", 43: "#555", 44: "#555", 45: "#555", 46: "#555 and #44", 47: "#44 and #555", 48: "#44",
	51: "#555", 52: "#555", 53: "#555", 54: "#555", 55: "#44", 56: "#44", 57: "#44", 58: "#44",
	61: "#555", 62: "#555", 63: "#555", 64: "#555", 65: "#555", 66: "#44", 67: "#44", 68: "#555",
	71: "#555", 72: "#44", 73: "#44", 74: "#44", 75: "#44", 76: "#555", 77: "#555", 78: "#555",
	81: "#44", 82: "#44", 83: "#44", 84: "#44", 85: "#555", 86: "#555",
}
LAMP_ASSEMBLIES = {
	11: "A-18068", 12: "A-18068", 13: "A-18068", 14: "A-18068", 15: "A-18068", 16: "A-18068",
	17: "A-18068", 18: "A-18068", 21: "A-18068", 22: "A-18068", 23: "A-18068", 24: "A-18068",
	25: "A-18068", 26: "A-18068", 27: "A-18068", 28: "A-18068",
	31: "A-17835", 32: "A-17835", 33: "A-18068", 34: "A-18068", 35: "A-18068", 36: "A-18068",
	37: "A-18068", 38: "A-17835",
	41: "A-18071", 42: "A-18071", 43: "A-18071", 44: "A-18067", 45: "A-18067",
	46: "A-18067 with A-17835", 47: "A-17807 with A-18067", 48: "A-17826",
	51: "A-18384", 52: "A-18384", 53: "A-18384", 54: "A-18384", 55: "A-17835", 56: "A-17835",
	57: "A-17835", 58: "A-17835",
	61: "A-18072", 62: "A-18072", 63: "A-18072", 64: "A-18072", 65: "A-18072", 66: "A-17835",
	67: "A-17835", 68: "A-18495",
	71: "C-12709", 72: "A-17835", 73: "A-17835", 74: "A-17835", 75: "A-17807", 76: "C-12709",
	77: "C-12709", 78: "C-12709",
	81: "A-17807", 82: "A-17807", 83: "A-17807", 84: "A-17807", 85: "A-18495", 86: "A-18495",
	87: None, 88: None,
}
LAMP_QUANTITIES = {46: 2, 47: 2, 71: 2, 78: 2}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J138-1", "Q98"), 2: ("Yellow-Red", "J138-2", "Q97"),
	3: ("Yellow-Orange", "J138-3", "Q96"), 4: ("Yellow-Black", "J138-4", "Q95"),
	5: ("Yellow-Green", "J138-5", "Q94"), 6: ("Yellow-Blue", "J138-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J135-1", "Q90"), 2: ("Red-Black", "J135-2", "Q89"),
	3: ("Red-Orange", "J135-4", "Q88"), 4: ("Red-Yellow", "J135-5", "Q87"),
	5: ("Red-Green", "J135-6", "Q86"), 6: ("Red-Blue", "J134-7 / J135-7", "Q85"),
	7: ("Red-Violet", "J134-8 / J135-8", "Q84"), 8: ("Red-Gray", "J134-9 / J135-9", "Q83"),
}

GI_STRINGS = {
	0: ("Playfield Left", "J121-1", "Q18", "J121-7", "#44, #555"),
	1: ("Playfield Right", "J121-2", "Q10", "J121-8", "#44, #555"),
	2: ("Insert Background", "J120-3 (Backbox)", "Q14", "J120-9 (Backbox)", "#555 (Backbox only)"),
	3: ("Insert Title", "J120-5 (Backbox)", "Q16", "J120-10 (Backbox)", "#555 (Backbox only)"),
	4: ("Playfield Top", "J121-6", "Q12", "J121-11", "#555 (Playfield only)"),
}
# GI collections from the retained table's collections.json, verified against script.vbs's
# GIUpdate2 dispatch (Case 0 -> GILeft, Case 1 -> GIRight, Case 4 -> GITop; no Case 2/3).
GI_POSITIONS = {
	0: [
		(0.224357, 0.822069), (0.164231, 0.803509), (0.230686, 0.763939), (0.192712, 0.720167),
		(0.108982, 0.598604), (0.117685, 0.566038), (0.043904, 0.497315), (0.053398, 0.445839),
		(0.0621, 0.394713), (0.182037, 0.541803), (0.038116, 0.422781),
	],
	1: [
		(0.714834, 0.823233), (0.77496, 0.803973), (0.702175, 0.764754), (0.74727, 0.721682),
		(0.881469, 0.62118), (0.880678, 0.570055), (0.880842, 0.435375), (0.880842, 0.38425),
		(0.880842, 0.332073), (0.811667, 0.513005), (0.938176, 0.724349),
	],
	4: [
		(0.276404, 0.295378), (0.269284, 0.262812), (0.137163, 0.248455), (0.151404, 0.196979),
		(0.067543, 0.148304), (0.068334, 0.096828), (0.066912, 0.04616), (0.354887, 0.021998),
		(0.344602, 0.084329), (0.416595, 0.077676), (0.608842, 0.076275), (0.700615, 0.076625),
		(0.791062, 0.076355), (0.865429, 0.076355), (0.241622, 0.033129),
		(0.34679, 0.0), (0.479012, 0.0), (0.609136, 0.0),
		(0.333148, 0.235246), (0.832139, 0.12164), (0.638028, 0.160818), (0.818163, 0.214431),
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
		raise RuntimeError(f"World Cup Soccer retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained World Cup Soccer extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"World Cup Soccer retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"World Cup Soccer retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"World Cup Soccer retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


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
	def excerpt(id_suffix: str, locator: str, filename: str, sha256: str, *, image: str | None = None, image_sha256: str | None = None, image_derivation: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": f"excerpt.world-cup-soccer.{id_suffix}",
			"locator": locator,
			"path": f"evidence/excerpts/midway.world-cup-soccer.1994/{filename}",
			"sha256": sha256,
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		}
		if image:
			record["image"] = f"evidence/excerpts/midway.world-cup-soccer.1994/{image}"
			record["image_sha256"] = image_sha256
			record["image_derivation"] = image_derivation
		return record

	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the wcs_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/wcs.c wcsGameData GEN_WPCSECURITY with wpc_dispDMD, the inverted-switch "
				"mask {0x00,0x00,0x00,0x3f,0x1f,0x07,0x00,0x00,0x00,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_U)|"
				"FLIP_SOL(FLIP_L) (no upper-flipper solenoid), every swXxx/sXxx #define, wcs_getSol (sLRampDiv = "
				"CORE_CUSTSOLNO(1) = 51, dispatched via core_getSol's unconditional hw.getSol branch for solNo>50 "
				"regardless of the driver's hw.custSol=0), wcs_goalieMech (MECH_LINEAR|MECH_REVERSE|MECH_ONESOL, "
				"WCS_GOALIETIME=50, WCS_GOALIESLACK=10) and wcs_handleMech (sets switches 43/44 from mech_getPos(0) "
				"only while solenoid 21 is active), wcs_ballMech (MECH_LINEAR|MECH_CIRCLE|MECH_TWODIRSOL) and "
				"wcs_getMech, wcs_stateDef/wcs_inportData (PinMAME's own internal ball-routing simulator, cited "
				"only for switch/solenoid name cross-reference, never as physical mechanism authority), and "
				"init_wcs (no wpc_set_fastflip_addr call, unlike several other WPC-Security/WPC-95 games); "
				"src/wpc/core.h WPC solenoid/switch numbering, CORE_FIRSTUFLIPSOL/CORE_FIRSTLFLIPSOL, "
				"CORE_CUSTSOLNO/CORE_FIRSTCUSTSOL, CORE_MAXSWCOL=16, CORE_SWxxFLIPxxBIT bit layout; src/wpc/core.c "
				"core_getSol full dispatch (29-32 GEN_ALLWPC J111 remap, 33-36 driver-specific solenoids2 bits "
				"unless FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL), 37-44 branch gated on GEN_WPC95/GEN_WPC95DCS/"
				"GEN_ALLS11 only -- returns 0 for GEN_WPCSECURITY, 45-48 lower flippers, 49-50 sim_getSol, 51+ "
				"unconditional hw.getSol), core_getSw/core_setSw/core_updInvSw (swNo translated to (swNo/10)*8+"
				"(swNo%10-1) before generic column/8 indexing, so invSw is indexed by WPC switch-matrix column "
				"including index 11 for the Fliptronic column), core.c's flipMask construction (locals.flipMask "
				"includes CORE_SWURFLIPBUTBIT/CORE_SWULFLIPBUTBIT because FLIP_SW(FLIP_U) is set, but excludes "
				"CORE_SWURFLIPEOSBIT/CORE_SWULFLIPEOSBIT because only FLIP_SOL(FLIP_L) is set); src/wpc/wpc.c "
				"GENWPC_HASFLIPTRON/GENWPC_HASWPC95/GENWPC_HASPIC and WPC_FLIPPERS unconditional-complement read; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCSECURITY=0x20"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-security.json",
			"revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp, and five-GI address rules, including the no-LPDC 37-44 note",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/midway.world-cup-soccer.1994/archive-arcademanual_World_Cup_Soccer_OPS/World_Cup_Soccer_OPS.pdf",
			"original_filename": "World_Cup_Soccer_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"152-page Midway Manufacturing Company Operations Manual, document 16-50031-101, May 1994 "
				"(Internet Archive item arcademanual_World_Cup_Soccer_OPS). Printed pages 2-44 through 2-49 carry "
				"the lamp/switch/solenoid location parts lists and their matrix and solenoid/flasher wiring "
				"tables and the general-illumination summary; printed pages 2-12, 2-14, and 2-15 carry the "
				"opto-board and DC-motor-control assembly parts that fix device construction; printed page 2-42 "
				"carries the Lower Playfield Parts list identifying the goalie, motor, and gate mechanisms. Page "
				"3 confirms the WPC Security CPU Board directly in the manual's own text."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				excerpt(
					"switch-matrix", "PDF page 112, printed page 2-46, SWITCH MATRIX table",
					"switch-matrix.md", "3172b24bb89752f827b0344d4bf659e7206bcdc828a5703fc67f8ff7c1084d94",
					image="switch-matrix.webp", image_sha256="81d523facac36cfc1aa2c383a37790955ca3859b186462b801883c097ad7d52e",
					image_derivation="World_Cup_Soccer_OPS.pdf page 112, crop box 0.14,0.09,0.99,0.46 of the page, rendered at 300 dpi with pdftoppm, reduced to 1000px wide grayscale, quality 75 WebP",
				),
				excerpt(
					"switch-locations", "PDF pages 112-113, printed pages 2-46/2-47, switch-locations parts list",
					"switch-locations.md", "80522bb19ee82917a86a9e95163f94638272cc1884a17a3bd591c12681bb0ba5",
				),
				excerpt(
					"lamp-matrix", "PDF page 110, printed page 2-44, LAMP MATRIX table",
					"lamp-matrix.md", "d7f630b73fc01e3b828aebc8552acede5c1dde9b416919a4ad5fa62632e517e4",
				),
				excerpt(
					"lamp-locations", "PDF pages 110-111, printed pages 2-44/2-45, lamp-locations parts list",
					"lamp-locations.md", "f671dd2f014c20bce60e6f033a89c1a4a49580c51e42f858d8ed0f8d03659abf",
				),
				excerpt(
					"solenoid-flasher-wiring", "PDF page 114, printed page 2-48, SOLENOID/FLASHER TABLE and Flipper Circuits",
					"solenoid-flasher-wiring.md", "b2f0f78cb29275bf6632b319cab584e23e602341e7eb5cc698d88cd6d4ce1ded",
				),
				excerpt(
					"solenoid-flasher-locations", "PDF page 114, printed page 2-48, SOLENOID/FLASHER LOCATIONS parts list",
					"solenoid-flasher-locations.md", "6abb4566d87e3016b5d865ec0d0d384a8fb1abefc28647878c1bb25b36e97a81",
				),
				excerpt(
					"general-illumination", "PDF page 115, printed page 2-49, General Illumination Circuits summary",
					"general-illumination.md", "02eb1bd6a9ad5efeb7b73b5be731cc6ba725d358c148999aef84137c485f8cd4",
				),
				excerpt(
					"boards-and-assemblies", "PDF pages 78, 80, 81, 108, printed 2-12/2-14/2-15/2-42, opto/motor board and Lower Playfield Parts pages",
					"boards-and-assemblies.md", "3577ac6493066b82c552f7dfc5a0961cfe233cad44c29f66274fcd1061a456b1",
				),
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription index of every rendered manual table used by this definition, "
				"together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/midway.world-cup-soccer.1994/. The retained PDF carries a "
				"real (if unreliable on multi-column tables) OCR text layer; this transcription and its "
				"per-table excerpts are the source of record, not the OCR text."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/midway/world-cup-soccer-1994/source/World%20Cup%20Soccer%20%28Bally%201994%29%20VPW%20v1.5.vpx",
			"original_filename": "World Cup Soccer (Bally 1994) VPW v1.5.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW v1.5 recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952.941 and y/2152.941. Geometry authority only "
				"for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/midway/world-cup-soccer-1994/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (245,232 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "wcs_l2", Const UseSolenoids = 2 (fast flips), Const UseLamps = 1 (built-in VPX '
				"light-number lamp handling), Const UseSync = 0, the SolCallback/SolModCallback table for "
				"solenoids 1-28, the ball-motion turntable (cvpmTurnTable on SoccerBall, solenoids 23/24), two "
				"magnets (cvpmMagnet on MagnaGoalie solenoid 33 and on LockMagnet solenoid 35, GrabCenter=True), "
				"the goalie's own independent sinusoidal position simulator (UpdateGoalie, unrelated to PinMAME's "
				"own wcs_handleMech/mech_getPos mechanism model) directly asserting switches 43/44, the trough "
				"ball-release chain (UpdateTroughTimer, SolTrough pulsing switch 36), and GiCallback2 = GIUpdate2 "
				"implementing only GI cases 0/1/4 (GILeft/GIRight/GITop), matching the manual's playfield-vs-"
				"backbox GI wiring exactly."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/midway/world-cup-soccer-1994/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. Bounds are "
				f"{TABLE_BOUNDS}."
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
		"board": "WPC-Security CPU board",
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
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address,
				"optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			physical: dict[str, Any] = {}
			part = SWITCH_PARTS.get(address)
			if part:
				physical["part_number"] = part
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					' Printed shaded "Opto, Typically Closed" on the switch matrix (2-46) and built from an LED/'
					"photo-transistor pair per the switch-locations parts list. Pinned PinMAME's wcsGameData "
					"inverted-switch mask normalizes this address, so the public switch state is already "
					"normalized and must not be inverted again."
				)
			if address == 24:
				notes += " Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if address == 26:
				notes += " Also serves as the Header Lane sensor in PinMAME's own internal ball-routing simulator (wcs_stateDef), which shares this physical switch with the Kickback Upper rollover."
			if address == 48:
				notes += ' PinMAME\'s own #define aliases this address as both swGoalie and swRTopRoll -- the same physical switch is reused for two logical purposes in the driver source.'
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
				label = f"Not Used Matrix Position {address}"
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
				if address in {12, 13, 14, 21, 22, 23}:
					role = {
						12: "cabinet.magna-goalie", 13: "cabinet.start", 14: "cabinet.tilt",
						21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {12, 13, 23} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "leaf", "internal_nonvisual"),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "opto", "cabinet_or_service"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "leaf", "internal_nonvisual"),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "opto", "cabinet_or_service"),
	}
	for address, (label, role, switch_type, reason) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		normally_closed = switch_type == "opto"
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed (assembly A-17316, Flipper Opto PCB Assembly, "
				"confirmed a genuine LED/phototransistor pair on the board's own parts breakdown). Pinned "
				"PinMAME's wcsGameData inverted-switch mask has twelve elements (one per switch-matrix column); "
				"its twelfth element -- index 11, the Fliptronic column -- is 0x00, so this printed opto address "
				"is not emulator-normalized despite the physical construction; see "
				"conflict.flipper-cabinet-opto-not-normalized."
			)
		else:
			notes += " Printed as a plain (non-opto) end-of-stroke leaf switch (SW-1A-194)."
		physical: dict[str, Any] = {
			"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly",
			"switch_type": switch_type,
			"notes": notes,
		}
		items.append(
			_device(
				f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"F{address - 110}"},
				],
				roles=[role],
				normally_closed=normally_closed,
				physical=physical,
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable(reason, MANUAL_SOURCE),
			)
		)
	for address in (115, 116, 117, 118):
		items.append(
			_device(
				f"switch.generic-{address}", f"Not Used Upper Flipper Position F{address - 110}", "switch",
				"pinmame.input.switch", address, "unused",
				(MANUAL_SOURCE, CONTROLLER_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"F{address - 110}"},
				],
				physical={"location": "not installed", "notes": "Printed Fliptronic grounded switch position, marked Not Used on the switch matrix and switch-locations parts list. World Cup Soccer has no upper flippers."},
				spatial=not_applicable("unused", MANUAL_SOURCE),
			)
		)

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country/option configuration bit)", "dip_switch",
				"pinmame.input.dip", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-Security CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-Security CPU-board country/option configuration DIP bank. The manual's own fold-out "
						"quick-reference page (PDF page 2) prints a partial SW4-SW8 country chart (America/"
						"European/French/German/Spain), but its scan quality is too degraded to transcribe with "
						"confidence, so no specific ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace(chr(39), '')}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 52):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING.get(address, {})
			kind = "flasher" if 17 <= address <= 20 or address == 22 or 25 <= address <= 28 else "motor" if address in {21, 23, 24} else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number:
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES and SOLENOID_ASSEMBLIES[address]:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d}" + (f" ({printed_type})" if printed_type else "") + "."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if address == 7:
				notes += " Backbox-mounted; unlike some other WPC-era games curated in this project, World Cup Soccer genuinely ships a knocker coil on this circuit."
			if address == 21:
				notes += (
					' Printed under the Flasher category column with a "* +12VDC" footnote rather than a normal '
					"flashlamp part number, but pinned PinMAME's #define sGoalieMot 21 and the retained script's "
					'SolGoalie handler (playing "fx_goaliedrive", a motor sound) both independently confirm this '
					"is the goalie DC gearmotor's drive line, not a flash effect. The manual's own category column "
					"is a printed-table quirk, not a genuine conflict: two independent sources agree on the real "
					"function."
				)
			if address in {23, 24}:
				notes += (
					" Similarly printed under the Flasher category with a \"* +12VDC\" footnote; this is the "
					"spinning-ball turntable motor's clockwise/counter-clockwise drive line (wcs_ballMech, "
					"MECH_TWODIRSOL), not a flash effect."
				)
			if address in {33, 34, 35}:
				notes += (
					" Fliptronic upper-flipper driver-transistor circuit repurposed for a non-flipper device: World "
					"Cup Soccer has no upper flippers (FLIP_SOL(FLIP_L) only), and this solenoid's driver "
					"transistor and drive connection are identical to the generic Flipper Circuits table's "
					f"{'Upper Right Power' if address == 33 else 'Upper Right Hold' if address == 34 else 'Upper Left Power'} "
					"position -- see solenoid-flasher-wiring.md for the full cross-reference."
				)
			if address == 34:
				notes += (
					" No VPX object of any kind and no script reference exists for this address in the retained "
					"table (grepped exhaustively); its spatial placement is not asserted rather than invented -- "
					"see coverage.missing."
				)
			if address == 36:
				notes += " Fourth upper-flipper driver-transistor position (Up Lt. Hold); no coil is printed anywhere on the solenoid/flasher table."
			if address in {45, 46, 47, 48}:
				notes += " PinMAME's public lower-flipper addresses are 45-48, matching the manual's own printed circuit numbers exactly for this generation (no LPDC remap)."
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-Security power driver board"}
			if "driver_transistor" in wiring_data:
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			if address in FLIPPER_DRIVE_WIRE:
				wiring["control_wire"] = FLIPPER_DRIVE_WIRE[address]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
			if wiring:
				extra["wiring"] = wiring
			if not fitted:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				if address == 7:
					extra["roles"] = ["cabinet.knocker"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				elif address == 34:
					pass  # spatial key deliberately omitted -- no evidence of any kind.
				else:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		# 31 is deliberately "unused": unlike several other WPC-Security/WPC-95 games in this project,
		# wcs.c's init_wcs never calls wpc_set_fastflip_addr, so no ROM flag ever populates this channel here.
		availability = "used" if address in {29, 30, 51} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a World Cup Soccer playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a World Cup Soccer playfield device.",
			31: "PinMAME's synthetic fast-flip game-on state. Unlike several other WPC-Security/WPC-95 games in this project, wcs.c's init_wcs never calls wpc_set_fastflip_addr, so this channel is not populated by any ROM flag for this game even though the retained script sets Const UseSolenoids = 2 (fast flips) independently.",
			32: "PinMAME reports this WPC state channel as always zero; wcsGameData declares no game-specific use for it.",
			37: "Unused WPC-Security output; this generation has no integrated LPDC board (unlike WPC-95/WPC-95DCS), so core_getSol returns constant 0 for solenoids 37-44 on GEN_WPCSECURITY.",
			38: "Unused WPC-Security output; see 37.",
			39: "Unused WPC-Security output; see 37.",
			40: "Unused WPC-Security output; see 37.",
			41: "Unused WPC-Security output; see 37.",
			42: "Unused WPC-Security output; see 37.",
			43: "Unused WPC-Security output; see 37.",
			44: "Unused WPC-Security output; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; World Cup Soccer has an automatic impulse plunger (cvpmImpulseP on switch 38) with no WPC-Security hardware output of its own.",
			50: "Reserved PinMAME output position before the first custom-output boundary. wcsGameData declares custSol=0.",
			51: (
				"PinMAME dispatches this address through wcs_getSol regardless of wcsGameData's declared custSol=0, "
				"because core_getSol's solNo>50 branch unconditionally calls hw.getSol. wcs_getSol's own body "
				"returns core_getSol(sDivHold) || core_getSol(sRampDiv) -- a live OR-combination readout of "
				"solenoids 16 and 8, not a distinct physical control line. This is a genuinely dispatched public "
				"address with no device behind it, the same class of fact Cirqus Voltaire's preliminary custom-"
				"solenoid readout established elsewhere in this project, but implemented as a direct OR mirror "
				"rather than a decaying counter."
			),
		}[address]
		roles = ["internal.duplicate.mirror"] if address == 51 else ["internal.wpc-state"] if address in {29, 30, 31, 32} else ["internal.unused.wpc-output"]
		items.append(
			_device(
				identifier, label, "virtual", "pinmame.output.solenoid", address, availability,
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly = LAMP_ASSEMBLIES.get(address)
			bulb = LAMP_BULBS.get(address)
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += (
					f" The printed lamp-locations map marks this insert with a bulb quantity of "
					f"{LAMP_QUANTITIES[address]} and prints a distinct assembly number for each bulb. Unlike some "
					"other WPC-era games curated in this project, the retained table's second Light object for "
					"this address is not a co-located brightness double: it sits at a genuinely different "
					"playfield position, so both are recorded as real, independent placements."
				)
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated buy-in/start button assembly; the retained table places this Light object off the playfield surface (normalized y > 1), consistent with cabinet mounting."
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
					"board": "WPC-Security power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in {87, 88}:
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra)
			)
	return items


LAMP_POSITIONS = {
	11: [(0.417838, 0.761764)], 12: [(0.398669, 0.731144)], 13: [(0.378665, 0.69868)],
	14: [(0.355328, 0.668061)], 15: [(0.335325, 0.635596)], 16: [(0.312313, 0.605702)],
	17: [(0.293143, 0.573976)], 18: [(0.271473, 0.543725)],
	21: [(0.474097, 0.718417)], 22: [(0.474514, 0.692778)], 23: [(0.47368, 0.667323)],
	24: [(0.475347, 0.642237)], 25: [(0.459836, 0.607915)], 26: [(0.405661, 0.582092)],
	27: [(0.444833, 0.551841)], 28: [(0.442333, 0.518639)],
	31: [(0.586288, 0.403784)], 32: [(0.64853, 0.439297)], 33: [(0.559527, 0.659576)],
	34: [(0.604534, 0.641499)], 35: [(0.532347, 0.593528)], 36: [(0.522346, 0.559588)],
	37: [(0.498175, 0.517532)], 38: [(0.375465, 0.308021)],
	41: [(0.056532, 0.742212)], 42: [(0.057782, 0.698496)], 43: [(0.059032, 0.659207)],
	44: [(0.727378, 0.510892)], 45: [(0.687371, 0.552579)],
	46: [(0.658709, 0.597968), (0.135272, 0.364567)],
	47: [(0.637039, 0.621578), (0.745695, 0.166207)],
	48: [(0.547777, 0.11084)],
	51: [(0.425258, 0.210069)], 52: [(0.532774, 0.211176)], 53: [(0.415256, 0.16912)],
	54: [(0.541109, 0.163955)], 55: [(0.774561, 0.627481)], 56: [(0.797898, 0.675254)],
	57: [(0.68538, 0.798655)], 58: [(0.869159, 0.779287)],
	61: [(0.316967, 0.434291)], 62: [(0.170277, 0.414001)], 63: [(0.214451, 0.467862)],
	64: [(0.247302, 0.508678)], 65: [(0.344471, 0.480405)], 66: [(0.654456, 0.038096)],
	67: [(0.745303, 0.037727)], 68: [(0.901518, 0.650774)],
	71: [(0.832993, 0.399357), (0.260137, 0.33364)],
	72: [(0.620192, 0.467334)], 73: [(0.262814, 0.799208)], 74: [(0.141545, 0.674701)],
	75: [(0.202547, 0.625032)], 76: [(0.268471, 0.352086)], 77: [(0.806322, 0.425181)],
	78: [(0.817157, 0.413376), (0.264304, 0.343232)],
	81: [(0.441309, 0.253422)], 82: [(0.443809, 0.333476)], 83: [(0.477104, 0.412638)],
	84: [(0.534613, 0.488634)], 85: [(0.899018, 0.586215)], 86: [(0.900685, 0.62163)],
}


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
				"board": "WPC-Security power driver board",
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
				"coordinate come from the retained table's GI emitter collection for this string, matching the "
				"retained script's GIUpdate2 dispatch exactly (Case 0 -> GILeft, Case 1 -> GIRight, Case 4 -> "
				"GITop)."
			)
			if address == 4:
				notes += (
					" Three GITop members (GI034, GI035, GI036) sit at normalized y=-0.021148, just outside the "
					"retained table's 0..1 playfield bounds near the top rail. Their y is clamped to the "
					"schema-valid boundary 0.000000 with the raw offset disclosed here rather than either "
					"fabricating a different coordinate or excluding three real bulbs."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite; the retained script's GIUpdate2 "
				"implements only GI cases 0, 1, and 4, matching this string's Backbox-only printed wiring exactly."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
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
		identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str,
		positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
			"behavior": behavior, "provenance": provenance(*refs),
		}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [
				{"id": pid, "label": plabel, "sensors": psensors, "description": pdesc}
				for pid, plabel, psensors, pdesc in positions
			]
		return record

	return [
		mechanism(
			"mechanism.trough", "Six-position ball trough and stack",
			"kicker",
			[output_id("Trough")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35", "switch.matrix-36"],
			"Five balls rest on trough optos 31-35 (31 nearest the eject coil, 35 nearest the drain entrance), all "
			"printed opto that rest closed and normalized by PinMAME's inverted-switch mask. Solenoid 6 (Trough) "
			"ejects the ball on 31 toward the shooter lane; the retained script's SolTrough handler fires that "
			"kick and pulses Trough Stack (36) in the same event. Pinned PinMAME's own internal ball-routing "
			"simulator (wcs_stateDef) places the 'Trough stack' state immediately after the trough-1 eject state "
			"and before the shooter-lane skill states, confirming Trough Stack senses the ball's staging position "
			"between the trough and the shooter lane rather than a sixth ball resting in the trough itself.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-31"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-32"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-33"], "Third trough position."),
				("ball-4", "Trough Ball 4", ["switch.matrix-34"], "Fourth trough position."),
				("ball-5", "Trough Ball 5 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fifth trough position."),
				("stack", "Ball staged toward the shooter lane", ["switch.matrix-36"], "Pulsed by the same event that ejects Trough Ball 1."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16765",
		),
		mechanism(
			"mechanism.shooter-lane", "Shooter lane and automatic impulse plunger",
			"kicker",
			[],
			["switch.matrix-38"],
			"World Cup Soccer has an automatic plunger (wcsSimData declares automatic plunger = TRUE, and no "
			"cabinet Launch Ball switch exists in the matrix). A ball ejected from the trough rests on shooter-"
			"lane switch 38 (Ball Shooter); the retained script's cvpmImpulseP helper (InitImpulseP swPlunger) "
			"auto-fires an impulse coil with no distinct public WPC-Security solenoid address of its own.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-38"], "Shooter-lane switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.skill-shot", "Skill Shot optical lane",
			"other",
			[],
			["switch.matrix-51", "switch.matrix-52", "switch.matrix-53"],
			"Three printed optos (A-16908 LED with A-16909 Transistor, the same construction as the Goal/Goalie "
			"hole optos) trip in sequence as the ball travels down the skill-shot lane -- Front (51), Center (52), "
			"then Rear (53) -- rewarding a timed shot with no motorized or magnetic component.",
			[
				("front", "Skill Shot Front", ["switch.matrix-51"], "First opto in the lane."),
				("center", "Skill Shot Center", ["switch.matrix-52"], "Second opto in the lane."),
				("rear", "Skill Shot Rear", ["switch.matrix-53"], "Third opto in the lane."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.goalie", "Motorized goalie figure",
			"motorized",
			[output_id("Goalie Drive")],
			["switch.matrix-43", "switch.matrix-44", "switch.matrix-48"],
			"A DC gearmotor (A-17741 Goalie Unit Assembly) drives the goalie figure back and forth one-"
			"directionally, reversing at each end of travel (pinned PinMAME's wcs_goalieMech: "
			"MECH_LINEAR|MECH_REVERSE|MECH_ONESOL, WCS_GOALIETIME=50, WCS_GOALIESLACK=10). wcs_handleMech sets "
			"public switches 43 (Goalie Is Left) and 44 (Goalie Is Right) directly from the motor's position "
			"counter (mech_getPos(0)), but only while solenoid 21 is actively driving the motor. The five printed "
			"'Flasher' category solenoid 21 is in fact this motor's +12VDC drive line, not a flash effect -- "
			"confirmed independently by wcs.c's #define sGoalieMot 21 and the retained script's SolGoalie sound "
			"handler. The retained VPW script does not read PinMAME's mechanism position at all: its own "
			"UpdateGoalie routine runs an independent sinusoidal simulation and asserts switches 43/44 directly "
			"from that simulation's angle, so both switches are documented projections onto the goalie figure's "
			"own table object rather than fixed playfield sensors. The goalie's 35-segment target-wall ring "
			"(GoalieWalls, HitTarget.GT006-GT040) surrounds the figure; GWalls_Hit pulses Goalie Target (48) "
			"whenever a ball strikes whichever single segment is currently collidable, matching the manual's "
			"A-17779-part 'Goalie Target' switch and the Dracula-target-ring pattern already documented elsewhere "
			"in this project for a rotating figure with a segmented hit ring.",
			[
				("left", "Goalie at left", ["switch.matrix-43"], "Motor position counter below center."),
				("right", "Goalie at right", ["switch.matrix-44"], "Motor position counter above center."),
				("struck", "Goalie target ring struck", ["switch.matrix-48"], "One of 35 target-wall segments surrounding the figure."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17741",
		),
		mechanism(
			"mechanism.spinning-ball", "Spinning soccer ball turntable",
			"motorized",
			[output_id("Ball Clockwise"), output_id("Ball Counter-Clockwise")],
			[],
			"A DC gearmotor turntable (A-17569 Motor Assembly with A-16120 DC Motor Control Assembly H-bridge "
			"driver board) spins a small soccer ball toy under a plastic dome. Pinned PinMAME's wcs_ballMech "
			"(MECH_LINEAR|MECH_CIRCLE|MECH_TWODIRSOL) models it as a two-direction continuous rotation with no "
			"discrete position switch; the retained script's cvpmTurnTable helper (InitTurnTable SoccerBall, "
			"strength 240) drives the visual spin directly from solenoids 23 (clockwise) and 24 "
			"(counter-clockwise), both printed under the Flasher category with a '* +12VDC' footnote despite "
			"being motor drive lines, not flash effects.",
			[],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17569",
		),
		mechanism(
			"mechanism.magna-goalie", "Magna Goalie magnet",
			"other",
			[output_id("Magna Goalie")],
			[],
			"Solenoid 33 energizes a playfield magnet (cvpmMagnet on the retained table's MagnaGoalie trigger, "
			"strength 16, GrabCenter=False) that deflects or catches the ball to help the player save a shot that "
			"would otherwise drain, as lit by lamp 55 (Light Magna Goalie) and the cabinet Magna Goalie Button "
			"(switch 12). No dedicated playfield switch senses this magnet directly; its state is tracked in "
			"game software.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="20-9247",
		),
		mechanism(
			"mechanism.lock-magnet", "Lock Magnet ball lock",
			"other",
			[output_id("Lock Magnet")],
			[],
			"Solenoid 35 energizes a second playfield magnet (cvpmMagnet on the retained table's LockMagnet "
			"trigger, strength 40, GrabCenter=True -- captures the ball at the magnet's center and halts its "
			"motion, unlike the Magna Goalie magnet's deflect-only behavior) that holds a locked ball for the "
			"multiball/lock feature. No dedicated playfield switch senses this magnet directly.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-18222",
		),
		mechanism(
			"mechanism.ramp-lock-post", "Left ramp lock post (mechanical)",
			"gate",
			[output_id("Lock Release")],
			["switch.matrix-76", "switch.matrix-77"],
			"Solenoid 4 (Lock Release) retracts a post (A-18155 Up/Down Post Unit Assy.) that otherwise holds a "
			"ball captured on the left ramp; Lock Mech. Low (76) and Lock Mech. High (77) sense a ball held at "
			"the post in its two stacking positions. This is a mechanical ramp lock distinct from the Lock "
			"Magnet's magnetic lock feature above.",
			[
				("low", "Ball locked, low position", ["switch.matrix-76"], "Lower of the two lock positions."),
				("high", "Ball locked, high position", ["switch.matrix-77"], "Upper of the two lock positions."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-18155",
		),
		mechanism(
			"mechanism.ramp-diverter", "Left ramp diverter",
			"gate",
			[output_id("Ramp Diverter"), output_id("Diverter Hold")],
			["switch.matrix-71"],
			"Solenoid 8 (Ramp Diverter) swings a diverter flap (A-18138 Diverter Assembly) to route the ball, and "
			"solenoid 16 (Diverter Hold) holds it in the diverted position; the retained script toggles two "
			"collision walls (diverterwall_open/diverterwall_closed) together. Left Ramp Diverted (71) is the "
			"printed switch for this mechanism, and pinned PinMAME's own wcs_getSol dispatches a synthetic "
			"combined-state address (public solenoid 51, CORE_CUSTSOLNO(1)) that ORs solenoids 8 and 16 together "
			"with no separate physical control line of its own.",
			[("diverted", "Ball routed by the diverter", ["switch.matrix-71"], "Left Ramp Diverted switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-18138",
		),
		mechanism(
			"mechanism.loop-gate", "Loop Gate / Lock Gate ball gate",
			"gate",
			[output_id("Loop Gate")],
			[],
			"Solenoid 34 operates a ball gate actuator (A-17796 Ball Gate Actuator Assy., per the Lower Playfield "
			"Parts list) that the manual's own two tables name inconsistently -- 'Loop Gate' on the primary "
			"Solenoid/Flasher Table (matching wcs.c's own #define sLoopGate 34) and 'Lock Gate' on the Solenoid/"
			"Flasher Locations parts list for the identical coil part and assembly number. Unlike the ramp "
			"diverter and lock post above, no VPX object of any kind (Gate, Flipper, Wall, Trigger, or Light) and "
			"no script reference exists anywhere in the retained table for this address, and no printed switch is "
			"associated with it either. Its playfield location is not asserted.",
			[],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.goal-tv-poppers", "Goal and TV ball poppers",
			"kicker",
			[output_id("Goal Popper"), output_id("TV Popper")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-45"],
			"A ball resting on opto 42 (Goal Popper Opto) is kicked by solenoid 1; Goal Trough (41) senses a ball "
			"that scored a goal en route to this popper. A ball resting on opto 45 (TV Ball Popper) is kicked by "
			"solenoid 2 to award the TV feature.",
			[
				("goal", "Ball at the goal popper", ["switch.matrix-42"], "Goal Popper Opto."),
				("tv", "Ball at the TV popper", ["switch.matrix-45"], "TV Ball Popper opto."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17839",
		),
		mechanism(
			"mechanism.eject-holes", "Upper, left, and right eject holes",
			"kicker",
			[output_id("Upper Eject Hole"), output_id("Left Eject Hole"), output_id("Right Eject Hole")],
			["switch.matrix-54", "switch.matrix-55", "switch.matrix-56"],
			"Three ordinary VUK-style kickers: solenoid 5 kicks a ball resting on Upper Eject Hole (55, PinMAME's "
			"own internal simulator calls this the 'Assist Hole'); solenoid 14 kicks Right Eject Hole (54); "
			"solenoid 15 kicks Left Eject Hole (56). wcs.c's own #define names (swLHole/swRHole) additionally "
			"associate 56/54 with the printed 'Left/Right Free Kick Hole' feature.",
			[
				("upper", "Ball in the upper eject hole", ["switch.matrix-55"], "Upper Eject Hole / Assist Hole."),
				("left", "Ball in the left eject hole", ["switch.matrix-56"], "Left Eject Hole / Free Kick Hole."),
				("right", "Ball in the right eject hole", ["switch.matrix-54"], "Right Eject Hole / Free Kick Hole."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers", "Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Upper Jet Bumper"), output_id("Lower Jet Bumper")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-83"],
			"Three A-9415-2 jet bumpers. The retained script's Bumper1_Hit/Bumper2_Hit/Bumper3_Hit handlers pulse "
			"switches 82, 81, and 83 respectively and fire coils 10, 9, and 11 -- table object Bumper2 is the "
			"printed 'Left' jet bumper and Bumper1 is the printed 'Upper' jet bumper, a naming/object-index "
			"crossing confirmed directly from the script rather than assumed from either label alone.",
			[
				("left", "Left jet bumper", ["switch.matrix-81"], "Table object Bumper2."),
				("upper", "Upper jet bumper", ["switch.matrix-82"], "Table object Bumper1."),
				("lower", "Lower jet bumper", ["switch.matrix-83"], "Table object Bumper3."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-84", "switch.matrix-85"],
			"Each slingshot assembly carries a direct-fire kicker switch (SW-1A-114) and a separate debounced "
			"score switch (SW-1A-120) wired to one public matrix address. The retained script's "
			"LeftSlingShot_Slingshot/RightSlingShot_Slingshot handlers pulse matrix addresses 84 and 85 and fire "
			"coils 12/13 in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-84"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-85"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-L-2 (left) with B-9362-R-3 (right)",
		),
		mechanism(
			"mechanism.kickback", "Left outlane kickback",
			"kicker",
			[output_id("Kickback")],
			["switch.matrix-26", "switch.matrix-86"],
			"A ball in the left outlane trips Kickback (86); when the Light Kickback feature (lit via switch 28) "
			"is active, solenoid 3 fires the kickback plunger (B-11873) to return the ball to play. Kickback "
			"Upper (26) senses the ball's return path and, per PinMAME's own internal simulator naming, doubles "
			"as the Header Lane sensor for the same physical lane.",
			[
				("outlane", "Ball in the left outlane", ["switch.matrix-86"], "Kickback switch."),
				("return", "Ball on the kickback return path", ["switch.matrix-26"], "Kickback Upper / Header Lane switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-11873",
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker",
			"other",
			[output_id("Knocker")],
			[],
			"Solenoid 7 fires a backbox-mounted knocker (B-10686-1) for match and replay effects. No dedicated "
			"playfield switch is associated with it.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="B-10686-1",
		),
		mechanism(
			"mechanism.lower-flippers", "Lower flipper pair",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two FL-11629 (Blue) flippers on Fliptronic circuits. Each flipper has a separate power and hold "
			"winding: the ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then "
			"drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. World Cup "
			"Soccer runs Const UseSolenoids = 2 fast flips. There are no upper flippers; the upper-flipper "
			"Fliptronic circuits (33-36 and Fliptronic positions 115-118) are either repurposed for other devices "
			"(33/34/35) or entirely unfitted (36, 115-118).",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15849-R-2 right with A-15849-L-2 left",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-stack-pulse",
			"kind": "pulse",
			"source": output_id("Trough"),
			"destination": "switch.matrix-36",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.flipper-cabinet-opto-not-normalized",
			"path": "inputs[binding.device=112,114]",
			"description": (
				"The switch-matrix page (2-46) shades the Fliptronic Grounded Switches cells for public 112 and "
				"114 (printed F2/F4, the lower-right/lower-left flipper cabinet buttons) exactly like the ordinary "
				"opto columns, and prints them 'Right/Left Flipper Opto'. The board/assembly page for A-17316 "
				"(the assembly wired at both positions) independently confirms genuine opto-interrupter "
				"construction: item 1 is a '03-9001 Interrupter Flip-Opto' and item 2 is an 'A-16384 Flipper Opto "
				"Switch Assembly' built from an 'Opto Inter Lg. 10mA' component -- so the switch-locations parts "
				"list's plainer 'Lower Right/Left Flipper Cabinet' description is not a contradiction, just a "
				"less specific label for the identical opto hardware. Pinned PinMAME's wcsGameData inverted-"
				"switch mask has twelve elements (columns 0-11, one per switch-matrix column including the "
				"Fliptronic column at index 11); its twelfth element is 0x00, so unlike the fourteen ordinary-"
				"matrix opto addresses (31-36, 41-45, 51-53), the public state of 112/114 is not emulator-"
				"normalized despite the confirmed physical construction. The manual is physical-construction "
				"ground truth and pinned PinMAME is public-address and emulator-normalization ground truth, and "
				"the two disagree on whether a recreation must invert these two addresses. Resolution path: run "
				"the implemented LibPinMAME gameplay harness against a legal wcs_l2 ROM, press and release both "
				"lower flipper buttons, and observe the idle and active public state of 112 and 114. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		},
	]


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
			"id": "midway.world-cup-soccer.1994",
			"name": "World Cup Soccer",
			"manufacturer": "Bally",
			"year": 1994,
			"kind": "physical_pinball",
			"ipdb_id": 2361,
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-security",
			"hardware_generation": "0x20",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/world-cup-soccer.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"World Cup Soccer device identifiers are not unique: {duplicates}")
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
	no_spatial_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			no_spatial_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
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
			"Public switches 112 and 114 (Fliptronic F2/F4, the lower flipper cabinet buttons) are printed opto "
			"interrupters that pinned PinMAME's wcsGameData inverted-switch mask does not normalize (its twelfth "
			"element, the Fliptronic column, is 0x00). This is a polarity conflict, not a spatial gap for those "
			"two addresses -- both take a controlled not_applicable spatial record regardless of polarity -- but "
			"it is recorded as conflict.flipper-cabinet-opto-not-normalized and keeps the machine record partial.",
			"Solenoid 34 (Loop Gate / Lock Gate) has no VPX object of any kind and no script reference anywhere "
			"in the retained table, and the manual gives no playfield-diagram position for it. Its spatial key is "
			"omitted from the definition entirely rather than a coordinate being invented or a status the schema "
			"does not define being used.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.941, "bottom": 2152.941},
			"x": "x/952.941; 0=left, 1=right",
			"y": "y/2152.941; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/midway/world-cup-soccer-1994/extracted-vpxtool.manifest.json",
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
		"no_spatial_key_outputs": sorted(no_spatial_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/midway.world-cup-soccer.1994/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"GITop members GI034/GI035/GI036 (raw normalized y=-0.021148, outside the 0..1 playfield bounds near "
			"the top rail) -- y clamped to the schema-valid boundary 0.000000 with the raw offset disclosed here "
			"rather than fabricating a coordinate or excluding three real bulbs",
			"Flipper.DiverterFlipper001 (raw normalized x=-0.139891, far outside playfield bounds, likely a "
			"parented-local-origin artifact) and Primitive.diverterwall_open/diverterwall_closed (raw position "
			"exactly 0,0,0) -- not used for solenoid 8/16 placement; that mechanism is projected onto switch 71's "
			"own validated position instead",
		],
		"unresolved": [
			{"group": "pinmame.output.solenoid", "address": 34, "reason": "no_evidence"},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# World Cup Soccer (Bally/Midway, 1994) spatial review",
		"",
		f"Status: {report['status']}. Every switch and lamp address in this audit is fully placed or carries a "
		"controlled `not_applicable` record; the one gap is a single solenoid (34, Loop Gate) with no evidence "
		"of any kind for its playfield location, which keeps the machine record `partial` at "
		"`machines/partial/midway/world-cup-soccer-1994.json` alongside the unresolved Fliptronic opto-polarity "
		"conflict recorded separately below.",
		"",
		"The matching source is the retained known-working `World Cup Soccer (Bally 1994) VPW v1.5.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained `vpxtool` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952.941 and y/2152.941 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Midway operations manual "
		"is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- The retained manual PDF carries a genuine but unreliable OCR text layer on multi-column tables; every "
		"printed table used here was read from rendered pages and transcribed into "
		"`external:pinmame-review-artifacts/world-cup-soccer/manual-transcription.md` and its per-table excerpts.",
		"- Several switches have no dedicated playfield trigger object because the retained script sets their "
		"public state directly from another mechanism's continuous position (the goalie's own independent "
		"sinusoidal simulator, or the trough-eject event) rather than from a Hit/Trigger event. Those addresses "
		"are explicit documented projections onto the real table object that carries the underlying mechanism "
		"state.",
		"- Lamp addresses with a printed bulb quantity of two (46, 47, 71, 78) are two genuinely separate "
		"playfield placements, not co-located brightness doubles: the manual prints a distinct assembly number "
		"for each bulb, and the retained table's second Light object for each address sits at a materially "
		"different coordinate.",
		"- GI strings 0, 1, and 4 use the retained table's GILeft/GIRight/GITop emitter collections, matching the "
		"retained script's GIUpdate2 dispatch exactly. GI strings 2 and 3 are backbox insert-panel circuits and "
		"take a controlled `cabinet_or_service` record.",
		"- The synthetic solenoid mirror at public address 51 (wcs_getSol's OR of solenoids 8 and 16) is declared "
		"virtual with a `virtual` spatial record so no duplicate diverter mechanism is ever placed on the "
		"playfield.",
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
		f"- Outputs with no spatial key at all: {len(report['no_spatial_key_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses "
		"this audit can place, and the deterministic curator reproduces the canonical artifact and its pinned "
		"seed byte-for-byte. However, two blockers keep this record `partial`: public switches 112/114 are "
		"printed opto interrupters that pinned PinMAME does not normalize (`conflict.flipper-cabinet-opto-not-"
		"normalized`, unresolved), and solenoid 34 has no evidence of any kind for its playfield location. The "
		"definition therefore carries a non-empty `conflicts` array, `coverage.dimensions.physical_wiring = "
		"\"conflicted\"`, and `coverage.missing = [\"spatial_placement\", \"unresolved_conflicts\"]`, so promotion "
		"to `author_ready` is refused until a LibPinMAME harness trace resolves the polarity question and further "
		"evidence (a wiring diagram, a differently-authored VPX table, or a physical-machine inspection) resolves "
		"solenoid 34's location.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription index of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
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
		raise RuntimeError(f"Stale World Cup Soccer author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"World Cup Soccer definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"World Cup Soccer seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"World Cup Soccer definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"World Cup Soccer seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"World Cup Soccer spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"World Cup Soccer spatial review drifted from its deterministic curator: {markdown_path}")
	print("World Cup Soccer definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"World Cup Soccer extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("World Cup Soccer retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
