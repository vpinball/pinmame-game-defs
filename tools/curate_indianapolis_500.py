"""Curate the physical Bally Indianapolis 500 (1995) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal below, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: the manual prints no general-illumination bulb list, so the playfield G.I. emitters
# come only from the retained table's G.I. collections and stay `observed`; the race-track reflector
# bulbs have no printed count; and switches 54 and 75 fail the factory switch-drawing check.
PARTIAL_PATH = ROOT / "machines/partial/bally/indianapolis-500-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/indianapolis-500-1995.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/indianapolis-500-1995.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/indianapolis-500-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/indianapolis-500-1995.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts/bally.indianapolis-500.1995"
EXCERPT_PREFIX = "evidence/excerpts/bally.indianapolis-500.1995"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
HANDBOOK_SOURCE = "manual.bally.indianapolis-500.1995.operators-handbook"
MANUAL_SOURCE = "manual.bally.indianapolis-500.1995.operations-manual"
VPX_TABLE_SOURCE = "vpx-table.indianapolis-500-dozer-1-1-rtm"
VPX_SCRIPT_SOURCE = "vpx-script.indianapolis-500-dozer-1-1-rtm"
VPX_EXTRACTION_SOURCE = "vpx-extraction.indianapolis-500-dozer-1-1-rtm"
VPW_SCRIPT_SOURCE = "vpx-script.indianapolis-500-vpw-1-36"

HANDBOOK_SHA256 = "537bf77824588e57e34b58a995611b850b25a0445ea2d8b9401a2fd9c50ffdda"
MANUAL_SHA256 = "89d0cb19701e21b6136d073a270d774c2304775655fe29e70e6b802f657df808"
TABLE_SHA256 = "a009c201fa4956ee086243486465e08917540c9a5044f5f14b88e24e704e2aeb"
SCRIPT_SHA256 = "bbb957330598291fbd8be3d89e6de2c6f4c541f417f66d443809ff2fe8302f72"
VPW_SCRIPT_SHA256 = "3398dc8c812b952bfb0ce6ed31fad6ff81657652e7adb062bef2d03b6253ed7e"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

EXTRACTION_RELATIVE_PATH = Path("bally/indianapolis-500-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/indianapolis-500-1995/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "1febbab77b92e2cd5d2f0ad4cfedb2d8eb6768e38aeefb3bf1f087af8b44dba1"
EXTRACTION_FILE_COUNT = 1031
EXTRACTION_TOTAL_BYTES = 152451195

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

DRIVER_IDS = ("i500_11r", "i500_11b", "i500_10r")
DRIVER_COMPATIBILITY = {
	"i500_11r": ("identical", "Bally 1.1R game ROM; the parent of the i500 clone tree and the firmware both retained scripts run."),
	"i500_11b": ("identical", "Bally 1.1 Belgian game ROM for the same physical machine. It is declared with the same wpc_mSecurityS machine driver, shares the parent's i500GameData and sound ROMs, and changes no public address."),
	"i500_10r": ("identical", "Bally 1.0R earlier game ROM for the same physical machine, sharing the parent's i500GameData and sound ROMs."),
}

# --- Printed switch matrix (handbook printed page 4; the full manual repeats it on printed 2-40).
SWITCH_LABELS = {
	11: "Ball Launch", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Left Outlane", 16: "Left Flipper Lane",
	17: "Right Flipper Lane", 18: "Right Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In Button", 24: "Always Closed", 25: "Shooter Lane",
	26: "Left Slingshot", 27: "Right Slingshot", 28: "Three Bank Upper",
	31: "Three Bank Center", 32: "Three Bank Lower", 34: "Right Flipper Wrench", 35: "Left Ramp Enter",
	36: "Left Ramp Made", 37: "Left Loop", 38: "Right Loop",
	41: "Top Trough", 42: "Trough 1 (Right)", 43: "Trough 2", 44: "Trough 3", 45: "Trough 4 (Left)",
	46: "Left Ramp Standup", 47: "Turbo Wrench", 48: "Jet Bumper Wrench",
	51: "Left Lane", 52: "Center Lane", 53: "Right Lane", 54: "Ten Point", 55: "Left Ramp Wrench",
	56: "Left Lightup", 57: "Center Lightup", 58: "Right Lightup",
	61: "Upper Popper", 62: "Turbo Popper", 63: "Turbo Ball Sense", 64: "Upper Eject", 65: "Lower Kicker",
	66: "Turbo Index",
	72: "Left Jet", 73: "Right Jet", 74: "Center Jet", 75: "Right Ramp Enter", 76: "Right Ramp Made",
}
# Printed "Not Used" on the matrix and "---"/"Not Used" in the switch-locations list.
UNUSED_MATRIX_ADDRESSES = {12, 33, 67, 68, 71, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# Shaded "Opto, Typically Closed" on the printed matrix (41-45, 56-58, 61-63) plus 66, which both
# printed matrices leave unshaded although its part (A-20047) is the Turbo Opto PCB Assembly.
OPTO_SWITCHES = {41, 42, 43, 44, 45, 56, 57, 58, 61, 62, 63, 66}
PRINTED_SHADED_OPTOS = OPTO_SWITCHES - {66}
# i500GameData's inverted-switch mask {0x00,0x00,0x00,0x00,0x1f,0xe0,0x27,0x00,...} is indexed by
# matrix column: 0x1f normalizes 41-45, 0xe0 normalizes 56-58 and 0x27 normalizes 61-63 and 66.
PINMAME_INVERTED_MASK = (0x00, 0x00, 0x00, 0x00, 0x1F, 0xE0, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00)
# vpmTimer.PulseSw callers in the retained script (targets, slingshots, bumpers, the Ten Point rubber
# and the Top Trough pulse on each trough eject).
PULSED_SWITCHES = {26, 27, 28, 31, 32, 34, 41, 46, 47, 48, 54, 55, 56, 57, 58, 72, 73, 74}

SWITCH_TYPES = {
	11: "button", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "tilt", 22: "microswitch", 23: "button", 24: "other", 25: "microswitch",
	26: "leaf", 27: "leaf", 28: "leaf", 31: "leaf", 32: "leaf", 34: "leaf", 35: "microswitch",
	36: "microswitch", 37: "microswitch", 38: "microswitch",
	41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto", 46: "leaf", 47: "leaf", 48: "leaf",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "leaf", 55: "leaf",
	56: "opto", 57: "opto", 58: "opto", 61: "opto", 62: "opto", 63: "opto", 64: "microswitch",
	65: "microswitch", 66: "opto", 72: "leaf", 73: "leaf", 74: "leaf", 75: "microswitch", 76: "microswitch",
}
SWITCH_PARTS = {
	11: "20-9663-B-3", 13: "20-9663-1", 14: "A-15361", 15: "5647-12693-19", 16: "5647-12693-19",
	17: "5647-12693-19", 18: "5647-12693-19", 21: "A-17238", 22: "5643-09288-00", 23: "20-9663-21",
	24: "5643-09112-00", 25: "5647-12693-32", 26: "SW-1A-114 (kicker) with SW-1A-120 (score)",
	27: "SW-1A-114 (kicker) with SW-1A-120 (score)", 28: "A-18019-20", 31: "A-18019-20", 32: "A-18019-20",
	34: "A-18019-6", 35: "5647-12693-11", 36: "5647-12693-11", 37: "5647-12693-19", 38: "5647-12693-19",
	41: "A-18617-1 LED with A-18618-1 transistor", 42: "A-18617-1 LED with A-18618-1 transistor",
	43: "A-18617-1 LED with A-18618-1 transistor", 44: "A-18617-1 LED with A-18618-1 transistor",
	45: "A-18617-1 LED with A-18618-1 transistor", 46: "A-18530-1", 47: "A-18019-6", 48: "A-18019-6",
	51: "5647-12693-19", 52: "5647-12693-19", 53: "5647-12693-19", 54: "SW-1A-120", 55: "A-18017-6",
	56: "A-19823", 57: "A-19823", 58: "A-19823", 61: "A-16908 with A-16909", 62: "A-16908 with A-16909",
	63: "A-14231 with A-14232", 64: "5647-12133-11", 65: "5647-12693-53", 66: "A-20047",
	72: "SW-11A-37-1", 73: "SW-11A-37-1", 74: "SW-11A-37-1", 75: "5647-12693-11", 76: "5647-12693-11",
}
TARGET_COLORS = {28: "Orange", 31: "Orange", 32: "Orange", 34: "Yellow", 46: "Blue", 47: "Yellow", 48: "Yellow", 55: "Yellow"}

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
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"),
	4: ("Orange-Yellow", "J205-4"), 5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Printed Normal Function Ser Credits, Test Function Esc."),
	6: ("Volume Down / Down", "service.down", "Printed Normal Function Vol Down, Test Function Down."),
	7: ("Volume Up / Up", "service.up", "Printed Normal Function Vol Up, Test Function Up."),
	8: ("Begin Test / Enter", "service.enter", "Printed Normal Function Begin Test, Test Function Enter."),
}
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "leaf", "SW-1A-194", "Black-Green", "J906-1"),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", "opto", "A-17316", "Black-Violet", "J905-1"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "leaf", "SW-1A-194", "Black-Blue", "J906-3"),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", "opto", "A-17316", "Black-Gray", "J905-2"),
	115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "leaf", "SW-1A-194", "Black-Violet", "J906-4"),
	116: ("Upper Right Flipper Button", "flipper.upper.right.button", "opto", "A-17316", "Black-Yellow", "J905-3"),
}
UNUSED_FLIPPER_SWITCHES = {117: ("Black-Gray", "J906-5", "Upper Left Flipper EOS"), 118: ("Black-Blue", "J905-5", "Upper Left Flipper Opto")}

# --- Normalized playfield coordinates from the retained Dozer VPX 1.1 RTM extraction, x/952 and
# y/2162 (review-artifacts/indianapolis-500/device-positions.txt).
SWITCH_POSITIONS = {
	15: (0.051227, 0.795559), 16: (0.135473, 0.795385), 17: (0.77664, 0.793731), 18: (0.861924, 0.793723),
	25: (0.940197, 0.97121), 26: (0.236383, 0.784032), 27: (0.67537, 0.785082),
	28: (0.131919, 0.614177), 31: (0.123225, 0.637377), 32: (0.11494, 0.66062), 34: (0.827932, 0.627456),
	35: (0.199831, 0.377514), 36: (0.40402, 0.152116), 37: (0.061966, 0.258039), 38: (0.941106, 0.188446),
	41: (0.870708, 0.944752), 42: (0.870708, 0.944752), 43: (0.870708, 0.944752), 44: (0.870708, 0.944752),
	45: (0.870708, 0.944752),
	46: (0.186266, 0.460745), 47: (0.297656, 0.224879), 48: (0.558203, 0.180658),
	51: (0.636719, 0.125116), 52: (0.729752, 0.126017), 53: (0.820739, 0.126017), 54: (0.840209, 0.334314),
	55: (0.341789, 0.416632), 56: (0.369975, 0.201299), 57: (0.578454, 0.380641), 58: (0.64837, 0.401483),
	61: (0.368421, 0.033714), 62: (0.242218, 0.276607), 63: (0.220005, 0.187016), 64: (0.465882, 0.120149),
	65: (0.648403, 0.334714), 66: (0.220005, 0.187016),
	72: (0.625063, 0.211391), 73: (0.839686, 0.211582), 74: (0.733556, 0.299211),
	75: (0.792015, 0.390206), 76: (0.615021, 0.040241),
}
SWITCH_OBJECTS = {
	15: "Trigger sw15", 16: "Trigger sw16", 17: "Trigger sw17", 18: "Trigger sw18", 25: "Trigger SW25",
	26: "Wall LeftSlingShot (bounding-box center of its six drag points)",
	27: "Wall RightSlingShot (bounding-box center of its six drag points)",
	28: "HitTarget sw28", 31: "HitTarget sw31", 32: "HitTarget sw32", 34: "HitTarget sw34",
	35: "Trigger sw35", 36: "Trigger sw36", 37: "Trigger sw37", 38: "Trigger sw38",
	46: "HitTarget sw46", 47: "HitTarget sw47", 48: "HitTarget sw48",
	51: "Trigger sw51", 52: "Trigger sw52", 53: "Trigger sw53",
	54: "Wall sw54 (bounding-box center of its four drag points)", 55: "HitTarget sw55",
	56: "Wall sw56 (bounding-box center of its four-point target face)",
	57: "Wall sw57 (bounding-box center of its four-point target face)",
	58: "Wall sw58 (bounding-box center of its four-point target face)",
	61: "Kicker sw61", 62: "Kicker sw62", 64: "Kicker sw64", 65: "Kicker sw65",
	72: "Bumper Bumper1", 73: "Bumper Bumper2", 74: "Bumper Bumper3", 75: "Trigger sw75", 76: "Trigger sw76",
}
# Switch placements the factory switch-location drawing downgrades. The reconciliation
# (external:pinmame-review-artifacts/indianapolis-500/manual-reconciliation.md) refits both drawings by
# least squares and applies one rule: a measured placement agrees when its callout reaches the same
# physical feature within 0.07 normalized units, inclusive; any read above the limit keeps it observed.
OBSERVED_SWITCHES = {
	54: "The handbook switch-location drawing's callout 54 ends 0.075 normalized from this wall's centre through the refitted drawing transform (external:pinmame-review-artifacts/indianapolis-500/manual-reconciliation.md), above the 0.07 limit, although it points at the same rubber switch beside the lower kicker.",
	75: "The handbook switch-location drawing's callout 75 ends at the right ramp's entrance posts, 0.064-0.078 normalized from this trigger on three reads through the refitted transform (external:pinmame-review-artifacts/indianapolis-500/manual-reconciliation.md), above the 0.07 limit on one of them.",
}
SWITCH_PROJECTIONS = {
	41: "Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmTrough keeps the balls virtually and pulses Top Trough on each Trough (solenoid 13) eject, so no table object represents the individual trough opto positions; the manual draws 41-45 along the A-19963 outhole ball trough at the lower right.",
	42: "Projected onto the trough eject kicker (Kicker BallRelease); the retained script's cvpmTrough.InitSwitches Array(42, 43, 44, 45) models the four ball positions virtually.",
	43: "Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.",
	44: "Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.",
	45: "Projected onto the trough eject kicker (Kicker BallRelease); see switch 42.",
	63: "Projected onto the turbo housing (Primitive Turbo_Bottom, table object center): the sensor is the A-14231/A-14232 LED/phototransistor pair mounted through the A-20065 turbo housing wall, and the retained script sets public 63 from its own turbo simulator (CloseBallSense/OpenBallSense) rather than from a playfield object.",
	66: "Projected onto the turbo housing (Primitive Turbo_Bottom, table object center): the sensor is the A-20047 Turbo Opto PCB mounted under the impeller inside the A-20038 Turbo Motor Assembly, and the retained script sets public 66 from its own turbo simulator (CloseTurboIndex/OpenTurboIndex).",
}

SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Upper Popper", 3: "Upper Eject", 4: "Lower Eject", 5: "Turbo Popper",
	7: "Knocker", 8: "Left Jet", 9: "Right Jet", 10: "Center Jet", 11: "Left Slingshot", 12: "Right Slingshot",
	13: "Trough", 14: "Upper Popper Flasher", 15: "Top Left Corner Flasher", 16: "Top Right Corner Flasher",
	17: "Turbo Motor", 18: "Race Track Motor", 19: "Orange Car Flasher", 20: "Yellow Car Flasher",
	21: "Blue Car Flasher", 22: "Green Car Flasher", 23: "Left Jet Flasher", 24: "Right Jet Flasher",
	25: "Center Jet Flasher", 26: "Right Side Flasher", 27: "Left Side Flasher", 28: "Right Ramp Enter Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Pit Ramp Diverter Power", 36: "Pit Ramp Diverter Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
FLASHERS = {14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28}
MOTORS = {17, 18}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "WPC Game-On State", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40",
	41: "Unused WPC-Security Output 41", 42: "Unused WPC-Security Output 42",
	43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> (printed type, voltage connection, transistor, drive connection, drive wire, part/lamp)
SOLENOID_WIRING = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "Vio-Brn", "AE-23-800"),
	2: ("High Power", "J107-2", "Q80", "J130-2", "Vio-Red", "AE-24-900"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "Vio-Org", "AE-26-1200"),
	4: ("High Power", "J107-2", "Q76", "J130-5", "Vio-Yel", "AE-28-1500"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "Vio-Grn", "AE-24-900"),
	6: ("High Power", None, "Q66", None, None, None),
	7: ("High Power", "J107-2 (Backbox)", "Q68", "J130-8 (Backbox)", "Vio-Blk", "AE-23-800"),
	8: ("High Power", "J107-2", "Q70", "J130-9", "Vio-Gry", "AE-26-1200"),
	9: ("Low Power", "J107-3", "Q58", "J127-1", "Brn-Blk", "AE-26-1200"),
	10: ("Low Power", "J107-3", "Q56", "J127-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "Brn-Org", "AE-26-1200"),
	12: ("Low Power", "J107-3", "Q52", "J127-5", "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J107-3", "Q50", "J127-6", "Brn-Grn", "AE-26-1500"),
	14: ("Low Power", "J107-6", "Q48", "J127-7", "Brn-Blu", "#906"),
	15: ("Low Power", "J107-6", "Q46", "J127-8", "Brn-Vio", "#906"),
	16: ("Low Power", "J107-6", "Q44", "J127-9", "Brn-Gry", "#906"),
	17: ("Flasher", "J116-2", "Q42", "J126-1", "Blk-Brn", "14-8021.1"),
	18: ("Flasher", "J116-2", "Q40", "J126-2", "Blk-Red", "14-8022"),
	19: ("Flasher", "J107-6", "Q38", "J126-3", "Blk-Org", "#906"),
	20: ("Flasher", "J107-6", "Q36", "J126-4", "Blk-Yel", "#906"),
	21: ("Flasher", "J107-6", "Q28", "J126-5", "Blu-Grn", "#906"),
	22: ("Flasher", "J107-6", "Q30", "J126-6", "Blu-Blk", "#906"),
	23: ("Flasher", "J107-6", "Q34", "J126-7", "Blu-Vio", "#906"),
	24: ("Flasher", "J107-6", "Q32", "J126-8", "Blu-Gry", "#906"),
	25: ("Gen. Purpose", "J107-6", "Q26", "J122-1", "Blu-Brn", "#906"),
	26: ("Gen. Purpose", "J107-6", "Q24", "J122-2", "Blu-Red", "#906"),
	27: ("Gen. Purpose", "J107-6", "Q22", "J122-3", "Blu-Org", "#906 (2)"),
	28: ("Gen. Purpose", "J107-6", "Q20", "J122-4", "Blu-Yel", "#906"),
	33: ("Fliptronic power", "J907-6 (Red-Vio)", "Q2", "J902-6", "Yel-Vio", "FL-11629"),
	34: ("Fliptronic hold", "J907-6 (Red-Vio)", "Q7", "J902-4", "Org-Vio", "FL-11629"),
	35: ("High Power", "J907-8,9", "Q1", "J902-3", "Yel-Gry", "A-20099"),
	36: ("Low Power", "J907-8,9", "Q5", "J902-1", "Org-Gry", "A-20099"),
	45: ("Fliptronic power", "J907-1 (Red-Grn)", "Q4", "J902-13", "Yel-Grn", "FL-11629"),
	46: ("Fliptronic hold", "J907-1 (Red-Grn)", "Q11", "J902-11", "Org-Grn", "FL-11629"),
	47: ("Fliptronic power", "J907-4 (Red-Blu)", "Q3", "J902-9", "Yel-Blu", "FL-11629"),
	48: ("Fliptronic hold", "J907-4 (Red-Blu)", "Q9", "J902-7", "Org-Blu", "FL-11629"),
}
# Printed flipper-circuit numbers (manual.address aliases) for the public Fliptronic addresses.
PRINTED_FLIPPER_CIRCUITS = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
SOLENOID_ASSEMBLIES = {
	1: "A-14525", 2: "A-20235", 3: "B-9361-R-1", 4: "A-20451", 5: "A-20159", 7: "B-10686-1",
	8: "A-9415-2", 9: "A-9415-2", 10: "A-9415-2", 11: "B-9362-L-2", 12: "B-9362-R-3", 13: "A-19963",
	14: "A-19980", 15: "A-19980", 16: "A-19980", 17: "A-20038", 18: "A-20169", 19: "A-17802",
	20: "A-17802", 21: "A-17802", 22: "A-17802", 23: "A-20432-5", 24: "A-20432-5", 25: "A-20432-5",
	26: "C-13337", 27: "C-13337 with A-19979", 28: "A-19980", 33: "A-14876-R-3", 34: "A-14876-R-3",
	35: "A-19978", 36: "A-19978", 45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
SOLENOID_CALLBACKS = {
	1: "SolPlungBall (fires Plunger1)", 2: "SolTopPopper (bsTBP at sw61)", 3: "UpMidSaucer (bsUE at sw64)",
	4: "slot_kicker (bsLE at sw65)", 5: "SolBottomPopper (bsBBP at sw62, feeding the turbo)", 7: "Knocker",
	13: "SolBallRelease (bsTrough, pulses switch 41)", 14: "Sol14 (SolModCallback)", 15: "Sol15 (SolModCallback)",
	16: "Sol16 (SolModCallback)", 18: "SolTopCar (spins the race-track car)", 19: "Sol19 (SolModCallback)",
	20: "Sol20 (SolModCallback)", 21: "Sol21 (SolModCallback)", 22: "Sol22 (SolModCallback)",
	23: "Sol23 (SolModCallback)", 24: "Sol24 (SolModCallback)", 25: "Sol25 (SolModCallback)",
	26: "Sol26 (SolModCallback)", 27: "Sol27 (SolModCallback)", 28: "Sol28 (SolModCallback)",
	36: "SolDiverterHold (rotates the pit-ramp diverter car Indy_Bottom and swaps DiverterOn/DiverterOff walls)",
	46: "SolRFlipper through SolCallback(sLRFlipper), which also swings the upper right flipper RightFlipper2",
	48: "SolLFlipper through SolCallback(sLLFlipper)",
}
SOLENOID_POSITIONS = {
	1: [(0.940197, 0.97121)], 2: [(0.368421, 0.033714)], 3: [(0.465882, 0.120149)], 4: [(0.648403, 0.334714)],
	5: [(0.242218, 0.276607)], 8: [(0.625063, 0.211391)], 9: [(0.839686, 0.211582)], 10: [(0.733556, 0.299211)],
	11: [(0.236383, 0.784032)], 12: [(0.67537, 0.785082)], 13: [(0.870708, 0.944752)],
	14: [(0.243384, 0.036205)], 15: [(0.071582, 0.08609)], 16: [(0.924492, 0.060377)],
	17: [(0.220005, 0.187016)], 18: [(0.773813, 0.055574)],
	19: [(0.091748, 0.424107)], 20: [(0.29853, 0.495452)], 21: [(0.703366, 0.501659)], 22: [(0.909898, 0.419345)],
	23: [(0.624029, 0.211219)], 24: [(0.839486, 0.211219)], 25: [(0.733674, 0.299339)],
	26: [(0.895114, 0.636363)], 27: [(0.029254, 0.283195), (0.065982, 0.579625)], 28: [(0.971444, 0.291928)],
	33: [(0.895129, 0.544263)], 34: [(0.895129, 0.544263)], 35: [(0.11504, 0.622629)], 36: [(0.11504, 0.622629)],
	45: [(0.624039, 0.900775)], 46: [(0.624039, 0.900775)], 47: [(0.288178, 0.900775)], 48: [(0.288178, 0.900775)],
}
# Solenoid placements projected onto a switch's table object; they inherit that switch's status.
SOLENOID_SWITCH_ANCHORS = {1: 25}
SOLENOID_OBJECTS = {
	1: "projected onto Trigger SW25 (see note)", 2: "Kicker sw61", 3: "Kicker sw64", 4: "Kicker sw65",
	5: "Kicker sw62", 8: "Bumper Bumper1", 9: "Bumper Bumper2", 10: "Bumper Bumper3",
	11: "Wall LeftSlingShot bounding-box center", 12: "Wall RightSlingShot bounding-box center",
	13: "Kicker BallRelease", 14: "Light F14_Lamp2", 15: "Light F15_Lamp2", 16: "Light F16_Lamp2",
	17: "Primitive Turbo_Bottom", 18: "Primitive Indy_Top", 19: "Light f19", 20: "Light f20", 21: "Light f21",
	22: "Light f22", 23: "Light Flash23_Lamp2", 24: "Light Flash24_Lamp2", 25: "Light Flash25_Lamp2",
	26: "Light F26_Lamp1", 27: "Light F27_Lamp3 (upper socket) and Light F27_Lamp5 (lower socket)",
	28: "Light F28_Lamp1", 33: "Flipper RightFlipper2", 34: "Flipper RightFlipper2",
	35: "Primitive Indy_Bottom", 36: "Primitive Indy_Bottom", 45: "Flipper RightFlipper", 46: "Flipper RightFlipper",
	47: "Flipper LeftFlipper", 48: "Flipper LeftFlipper",
}

# --- Lamp matrix (handbook printed pages 2-3).
LAMP_LABELS = {
	11: "Left Lane", 12: "Center Lane", 13: "Right Lane", 14: "Upper Eject Top", 15: "Jet Wrench",
	16: "Extra Ball", 17: "Victory Lap", 18: "Turbo Wrench",
	21: "Turbo Lock 1", 22: "Turbo Lock 2", 23: "Turbo Lock 3", 24: "Light Lock Lamp", 25: "Light Speedway",
	26: "\"Pass\"", 27: "Left Ramp Wrench", 28: "Left Ramp Standup",
	31: "Hit The \"Wall\"", 32: "Hit \"The\" Wall", 33: "\"Hit\" The Wall", 34: "Left Ramp Jackpot",
	35: "Increase Boost", 36: "Souvenir Lamp", 37: "Left Flipper Lane", 38: "Left Outlane",
	41: "Super Jets", 42: "Turbo Boost", 43: "Checkered Flag", 44: "Go For The Pole", 45: "Quick Pit",
	46: "3X Playfield", 47: "Upper Right Flipper Wrench", 48: "Right Flipper Lane",
	51: "Dueling Drivers", 52: "Super Lightups", 53: "Caution Flag", 54: "Extra Ball Flag", 55: "Wrong Turn",
	56: "Gasoline Alley", 57: "Right Outlane", 58: "Shoot Again",
	61: "Change Setup", 62: "Award Speedway", 63: "Hit The Wall", 64: "Right Ramp Jackpot", 65: "Pit Stop",
	66: "Fast Laps",
	71: "Lightup 1 Lower Right", 72: "Lightup 1 Upper Right", 73: "Lightup 1 Upper Left", 74: "Lightup 1 Lower Left",
	75: "Lightup 2 Lower Right", 76: "Lightup 2 Upper Right", 77: "Lightup 2 Upper Left", 78: "Lightup 2 Lower Left",
	81: "Lightup 3 Lower Right", 82: "Lightup 3 Upper Right", 83: "Lightup 3 Upper Left", 84: "Lightup 3 Lower Left",
	86: "Launch Button", 87: "Buy-In Button", 88: "Start Button",
}
UNUSED_LAMPS = {67, 68, 85}
LAMP_BULBS = {address: "#44" for address in (18, 27, 28, 37, 38, 47, 48, 57, 58)}
LAMP_ASSEMBLIES = {
	11: "A-20108", 12: "A-20108", 13: "A-20108", 14: "A-20104", 15: "A-20104", 16: "A-20104", 17: "A-20104",
	18: "A-17835", 21: "A-20107", 22: "A-20107", 23: "A-20107", 24: "A-20105", 25: "A-20105", 26: "A-20105",
	27: "A-17835", 28: "A-17835", 31: "A-20106", 32: "A-20106", 33: "A-20106", 34: "A-20105", 35: "A-20105",
	36: "A-20105", 37: "A-17835", 38: "A-17835", 41: "A-20103", 42: "A-20103", 43: "A-20103", 44: "A-20103",
	45: "A-20103", 46: "A-20103", 47: "A-17835", 48: "A-17835", 51: "A-20103", 52: "A-20103", 53: "A-20103",
	54: "A-20103", 55: "A-20103", 56: "A-20103", 57: "A-17835", 58: "A-17835", 61: "A-20105", 62: "A-20105",
	63: "A-20105", 64: "A-20105", 65: "A-20105", 66: "A-20105",
	**{address: "A-19823" for address in (71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84)},
	86: "20-9663-B-3", 87: "20-9663-21", 88: "20-9663-1",
}
LAMP_CONNECTOR_NOTE = (
	" Connectors follow the lamp matrix; the power driver board connector list (manual printed 3-26) instead puts "
	"the rows on J135 and the columns on J138 (J135-3 and J138-8 are keys) and marks J133 and J137 Not Used, with the "
	"same wire colours."
)
LIGHTUP_TARGETS = {
	71: 56, 72: 56, 73: 56, 74: 56, 75: 57, 76: 57, 77: 57, 78: 57, 81: 58, 82: 58, 83: 58, 84: 58,
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
LAMP_POSITIONS = {
	11: (0.637064, 0.071669), 12: (0.730135, 0.071057), 13: (0.82088, 0.07033), 14: (0.467166, 0.167618),
	15: (0.533764, 0.232561), 16: (0.457975, 0.203293), 17: (0.434796, 0.23983), 18: (0.366921, 0.279337),
	21: (0.319549, 0.332596), 22: (0.403174, 0.372886), 23: (0.487701, 0.415304), 24: (0.118221, 0.462094),
	25: (0.140278, 0.488455), 26: (0.16599, 0.515517), 27: (0.411691, 0.452197), 28: (0.218689, 0.486497),
	31: (0.190755, 0.69197), 32: (0.203077, 0.657396), 33: (0.214327, 0.623333), 34: (0.323058, 0.532252),
	35: (0.343654, 0.559788), 36: (0.361794, 0.587984), 37: (0.13663, 0.737307), 38: (0.052499, 0.737548),
	41: (0.364203, 0.647275), 42: (0.340418, 0.691308), 43: (0.340495, 0.738431), 44: (0.339481, 0.784654),
	45: (0.362927, 0.828075), 46: (0.455513, 0.84029), 47: (0.744493, 0.652269), 48: (0.776401, 0.737641),
	51: (0.457298, 0.636253), 52: (0.550627, 0.647113), 53: (0.572665, 0.690777), 54: (0.573075, 0.738019),
	55: (0.573145, 0.784389), 56: (0.54762, 0.828445), 57: (0.861725, 0.73773), 58: (0.456595, 0.947391),
	61: (0.888798, 0.457078), 62: (0.864376, 0.48417), 63: (0.838899, 0.510862), 64: (0.670096, 0.536667),
	65: (0.646625, 0.563516), 66: (0.621694, 0.590848),
}
# Script-bound duplicate render lights excluded from placements (Lights(n)=Array(Lnn, Lnna)).
LAMP_HELPERS = {14: "L14a", 16: "L16a", 17: "L17a", 21: "L21a", 22: "L22a", 23: "L23a"}

GI_STRINGS = {
	0: ("Upper Left Playfield", "J121-1 (Playfield) / J120-1 (Backbox)", "Q18", "J121-7 (Playfield) / J120-7 (Backbox)", "Wht-Brn", "#44 playfield, #555 backbox"),
	1: ("Upper Right Playfield", "J121-2 (Playfield)", "Q10", "J121-8 (Playfield)", "Wht-Org", "#44, #555 playfield"),
	2: ("Lower Playfield", "J121-3 (Playfield) / J120-3 (Backbox)", "Q14", "J121-9 (Playfield) / J120-9 (Backbox)", "Wht-Yel", "#44 playfield, #555 backbox"),
	3: ("Backbox-Coindoor", "J120-5 (Backbox)", "Q16", "J120-10 (Backbox)", "Wht-Grn", "#555 backbox"),
	4: ("Backbox Title", "J120-6 (Backbox)", "Q12", "J120-11 (Backbox)", "Wht-Vio", "#555 backbox"),
}
GI_COLLECTIONS = {0: "GITL", 1: "GITR", 2: "GIB"}
# Distinct bulb-mesh Light members of each G.I. collection; co-located duplicates share one entry
# (review-artifacts/indianapolis-500/gi-emitters.txt).
GI_POSITIONS = {
	0: [
		(0.224097, 0.030382), (0.063178, 0.102178), (0.366436, 0.139181), (0.125718, 0.288231),
		(0.229397, 0.402596), (0.07367, 0.036469),
	],
	1: [
		(0.734118, 0.298988), (0.840864, 0.21139), (0.624281, 0.210535), (0.590822, 0.123598),
		(0.865267, 0.124358), (0.776838, 0.124358), (0.683497, 0.124358), (0.745509, 0.345287),
		(0.581801, 0.327265), (0.857525, 0.414901), (0.884735, 0.259732), (0.927048, 0.027571),
	],
	2: [
		(0.061671, 0.514521), (0.064472, 0.605562), (0.079878, 0.689435), (0.218645, 0.813879),
		(0.150194, 0.855929), (0.216061, 0.87676), (0.189089, 0.780714), (0.72602, 0.771979),
		(0.767077, 0.857253), (0.69867, 0.814955), (0.710485, 0.876011), (0.039262, 0.43535),
		(0.986155, 0.37801), (0.971728, 0.449045), (0.929758, 0.537982), (0.931507, 0.602085),
		(0.929758, 0.672928), (0.214237, 0.786372), (0.702383, 0.787964), (0.082496, 0.61564),
		(0.139834, 0.571961), (0.856922, 0.628973), (0.290275, 0.900529), (0.627343, 0.900529),
		(0.947078, 0.669593),
	],
}
GI_EXCLUDED = {
	0: "t2 (no bulb mesh)",
	1: "Light14-Light20 and Light22-Light25 duplicates and F16_Lamp3/F16_Lamp4/F16_Lamp5, none of which has a bulb mesh (the F16_Lamp3/4/5 lights are named after flasher 16 but only this string's UpdateGI case drives them)",
	2: "Light2, Light4, Light5, Light41, Light59 (no bulb mesh) and the 500-unit ambient fills Light11 and Light64",
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _text_sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Indianapolis 500 retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Indianapolis 500 extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Indianapolis 500 retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Indianapolis 500 retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Indianapolis 500 retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
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
				"provenance": provenance(*source_refs, status=status),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# (excerpt id suffix, source, locator, image derivation)
HANDBOOK_EXCERPTS = (
	("lamp-matrix", "PDF page 4, printed page 2, LAMP MATRIX", "Indianapolis_500_OPS.pdf page 4, crop box 0.08,0.15,0.88,0.5, scanned page rendered at its native resolution (embedded image xref 15, 1536px across 5.12in), rendered at 220 dpi, capped to 900px wide, grayscale, 900x629 WebP quality 80"),
	("lamp-locations", "PDF page 4, printed page 2, LAMP LOCATIONS items 11-58", "Indianapolis_500_OPS.pdf page 4, crop box 0.06,0.53,0.95,0.84, scanned page rendered at its native resolution (embedded image xref 15, 1536px across 5.12in), rendered at 219 dpi, capped to 1000px wide, grayscale, 1001x557 WebP quality 80"),
	("lamp-locations-continued", "PDF page 5, printed page 3, LAMP LOCATIONS CONTINUED items 61-88", "Indianapolis_500_OPS.pdf page 5, crop box 0.1,0.61,0.92,0.82, scanned page rendered at its native resolution (embedded image xref 20, 1668px across 5.56in), rendered at 300 dpi, grayscale, 1369x513 WebP quality 80"),
	("switch-matrix", "PDF page 6, printed page 4, SWITCH MATRIX", "Indianapolis_500_OPS.pdf page 6, crop box 0.05,0.15,0.93,0.55, scanned page rendered at its native resolution (embedded image xref 25, 1456px across 4.85in), rendered at 176 dpi, capped to 750px wide, grayscale, 751x583 WebP quality 80"),
	("switch-locations", "PDF page 6, printed page 4, SWITCH LOCATIONS items F1-48", "Indianapolis_500_OPS.pdf page 6, crop box 0.05,0.56,0.95,0.86, scanned page rendered at its native resolution (embedded image xref 25, 1456px across 4.85in), rendered at 252 dpi, capped to 1100px wide, grayscale, 1101x628 WebP quality 80"),
	("switch-locations-continued", "PDF page 7, printed page 5, SWITCH LOCATIONS CONTINUED items 51-88", "Indianapolis_500_OPS.pdf page 7, crop box 0.12,0.62,0.95,0.87, scanned page rendered at its native resolution (embedded image xref 30, 1712px across 5.71in), rendered at 300 dpi, grayscale, 1422x622 WebP quality 80"),
	("solenoid-flasher-table", "PDF page 8, printed page 6, SOLENOID/FLASHER TABLE rows 01-36", "Indianapolis_500_OPS.pdf page 8, crop box 0.04,0.15,0.96,0.505, scanned page rendered at its native resolution (embedded image xref 35, 1536px across 5.12in), rendered at 180 dpi, capped to 850px wide, grayscale, 851x522 WebP quality 80"),
	("gi-and-flipper-circuits", "PDF page 8, printed page 6, SOLENOID/FLASHER TABLE General Illumination and Flipper Circuits blocks", "Indianapolis_500_OPS.pdf page 8, crop box 0.04,0.49,0.96,0.68, scanned page rendered at its native resolution (embedded image xref 35, 1536px across 5.12in), rendered at 300 dpi, grayscale, 1414x465 WebP quality 80"),
	("solenoid-flasher-locations", "PDF page 8, printed page 6, SOLENOID/FLASHER LOCATIONS items 01-20", "Indianapolis_500_OPS.pdf page 8, crop box 0.05,0.68,0.95,0.87, scanned page rendered at its native resolution (embedded image xref 35, 1536px across 5.12in), rendered at 300 dpi, grayscale, 1384x464 WebP quality 80"),
	("solenoid-flasher-locations-continued", "PDF page 9, printed page 7, SOLENOID/FLASHER LOCATIONS CONTINUED, G.I. circuits and flipper coils", "Indianapolis_500_OPS.pdf page 9, crop box 0.06,0.65,0.94,0.87, scanned page rendered at its native resolution (embedded image xref 40, 1604px across 5.35in), rendered at 300 dpi, grayscale, 1412x541 WebP quality 80"),
	("upper-playfield-parts-1", "PDF page 10, printed page 8, UPPER PLAYFIELD PARTS left column items 1-24", "Indianapolis_500_OPS.pdf page 10, crop box 0.06,0.12,0.51,0.49, scanned page rendered at its native resolution (embedded image xref 45, 1520px across 5.07in), rendered at 300 dpi, grayscale, 685x910 WebP quality 80"),
	("upper-playfield-parts-2", "PDF page 10, printed page 8, UPPER PLAYFIELD PARTS left column items 21-41", "Indianapolis_500_OPS.pdf page 10, crop box 0.06,0.48,0.51,0.85, scanned page rendered at its native resolution (embedded image xref 45, 1520px across 5.07in), rendered at 300 dpi, grayscale, 685x910 WebP quality 80"),
	("upper-playfield-parts-3", "PDF page 10, printed page 8, UPPER PLAYFIELD PARTS right column items 42-67, Not Shown and Miscellaneous", "Indianapolis_500_OPS.pdf page 10, crop box 0.49,0.12,0.96,0.72, scanned page rendered at its native resolution (embedded image xref 45, 1520px across 5.07in), rendered at 231 dpi, capped to 550px wide, grayscale, 551x1136 WebP quality 80"),
	("lower-playfield-parts", "PDF page 12, printed page 10, LOWER PLAYFIELD PARTS item table", "Indianapolis_500_OPS.pdf page 12, crop box 0.06,0.6,0.94,0.85, scanned page rendered at its native resolution (embedded image xref 55, 1536px across 5.12in), rendered at 266 dpi, capped to 1200px wide, grayscale, 1201x550 WebP quality 80"),
)
MANUAL_EXCERPTS = (
	("illuminated-target-pcb", "PDF page 87, printed page 2-13, A-19823 4-LED Illuminated Target PCB Assembly", "indy500manualfull.original-scan.pdf page 87, crop box 0.1,0.03,0.97,0.48, scanned page rendered at its native resolution (embedded image xref 516, 2544px across 8.47in), rendered at 190 dpi, capped to 1400px wide, grayscale, 1401x939 WebP quality 80"),
	("turbo-opto-pcb", "PDF page 88, printed page 2-14, A-20047 Turbo Opto PCB Assembly", "indy500manualfull.original-scan.pdf page 88, crop box 0.05,0.03,0.97,0.38, scanned page rendered at its native resolution (embedded image xref 522, 2544px across 8.47in), rendered at 300 dpi, grayscale, 2341x1154 WebP quality 80"),
	("pit-ramp-diverter-assembly", "PDF page 96, printed page 2-22, A-19978 Pit Ramp Diverter Assembly parts tables", "indy500manualfull.original-scan.pdf page 96, crop box 0.08,0.62,0.98,0.95, scanned page rendered at its native resolution (embedded image xref 570, 2544px across 8.47in), rendered at 184 dpi, capped to 1400px wide, grayscale, 1401x665 WebP quality 80"),
	("turbo-motor-assembly", "PDF page 97, printed page 2-23, A-20038 Turbo Motor Assembly parts table", "indy500manualfull.original-scan.pdf page 97, crop box 0.49,0.1,0.98,0.52, scanned page rendered at its native resolution (embedded image xref 576, 2544px across 8.47in), rendered at 241 dpi, capped to 1000px wide, grayscale, 1000x1111 WebP quality 80"),
	("race-track-assembly", "PDF page 103, printed page 2-29, A-20169 Race Track Assembly parts table", "indy500manualfull.original-scan.pdf page 103, crop box 0.08,0.63,0.97,0.84, scanned page rendered at its native resolution (embedded image xref 612, 2544px across 8.47in), rendered at 186 dpi, capped to 1400px wide, grayscale, 1401x429 WebP quality 80"),
	("turbo-multiball-rules", "PDF page 17, game rules, TURBO MULTI-BALL paragraph", "indy500manualfull.original-scan.pdf page 17, crop box 0.08,0.1,0.95,0.27, scanned page rendered at its native resolution (embedded image xref 96, 2544px across 8.47in), rendered at 217 dpi, capped to 1600px wide, grayscale, 1601x406 WebP quality 80"),
	("race-track-wiring-drawing", "PDF page 103, printed page 2-29, A-20169 Race Track Assembly front view with the reflector socket leads", "indy500manualfull.original-scan.pdf page 103, crop box 0.55,0.22,0.99,0.53, scanned page rendered at its native resolution (embedded image xref 612, 2544px across 8.47in), rendered at 300 dpi, grayscale, 1120x1023 WebP quality 80"),
	("flasher-wiring", "PDF page 125, printed page 3-7, FLASHER WIRING", "indy500manualfull.original-scan.pdf page 125, crop box 0.1,0.08,0.95,0.86, scanned page rendered at its native resolution (embedded image xref 744, 2544px across 8.47in), rendered at 194 dpi, capped to 1400px wide, grayscale, 1401x1665 WebP quality 80"),
	("power-driver-connectors-3-25-left", "PDF page 143, printed page 3-25, power driver board connectors J113-J120", "indy500manualfull.original-scan.pdf page 143, crop box 0.09,0.07,0.53,0.82, scanned page rendered at its native resolution (embedded image xref 852, 2544px across 8.47in), rendered at 134 dpi, capped to 500px wide, grayscale, 501x1104 WebP quality 80"),
	("power-driver-connectors-3-25-right", "PDF page 143, printed page 3-25, power driver board connectors J121-J129", "indy500manualfull.original-scan.pdf page 143, crop box 0.52,0.07,0.9,0.85, scanned page rendered at its native resolution (embedded image xref 852, 2544px across 8.47in), rendered at 155 dpi, capped to 500px wide, grayscale, 501x1330 WebP quality 80"),
	("power-driver-connectors-3-26", "PDF page 144, printed page 3-26, power driver board connectors J130-J138", "indy500manualfull.original-scan.pdf page 144, crop box 0.09,0.08,0.85,0.44, scanned page rendered at its native resolution (embedded image xref 858, 2544px across 8.47in), rendered at 155 dpi, capped to 1000px wide, grayscale, 1001x614 WebP quality 80"),
	("ten-opto-pcb", "PDF page 138, printed page 3-20, A-18159 10 Opto P.C.B. connector list", "indy500manualfull.original-scan.pdf page 138, crop box 0.08,0.4,0.87,0.87, scanned page rendered at its native resolution (embedded image xref 822, 2544px across 8.47in), rendered at 149 dpi, capped to 1000px wide, grayscale, 1001x772 WebP quality 80"),
)
# The upper-playfield parts page is one transcription with three crops.
EXCERPT_TRANSCRIPTIONS = {
	"upper-playfield-parts-1": "upper-playfield-parts.md",
	"upper-playfield-parts-2": "upper-playfield-parts.md",
	"upper-playfield-parts-3": "upper-playfield-parts.md",
}


def _excerpts(entries: tuple[tuple[str, str, str], ...]) -> list[dict[str, Any]]:
	records = []
	for suffix, locator, derivation in entries:
		transcription = EXCERPT_TRANSCRIPTIONS.get(suffix, f"{suffix}.md")
		records.append(
			{
				"id": f"excerpt.indianapolis-500.{suffix}",
				"locator": locator,
				"path": f"{EXCERPT_PREFIX}/{transcription}",
				"sha256": _text_sha256(EXCERPT_DIRECTORY / transcription),
				"image": f"{EXCERPT_PREFIX}/{suffix}.webp",
				"image_sha256": _file_sha256(EXCERPT_DIRECTORY / f"{suffix}.webp"),
				"image_derivation": derivation,
				"method": "manual",
				"transcribed_by": "curator, read from the native-resolution render",
				"reviewed": True,
			}
		)
	return records


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames records for i500_11r, i500_11b and i500_10r",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/i500.c: CORE_GAMEDEF(i500,11r) and CORE_CLONEDEF(i500,11b/10r) all with "
				"wpc_mSecurityS; i500GameData GEN_WPCSECURITY with wpc_dispDMD, FLIP_SW(FLIP_L|FLIP_U)|"
				"FLIP_SOL(FLIP_L|FLIP_UR), the inverted-switch mask {0x00,0x00,0x00,0x00,0x1f,0xe0,0x27,0x00,0x00,"
				"0x00,0x00,0x00}, no custom solenoids and no wpc_set_fastflip_addr call; i500_handleMech/i500_getMech "
				"(turbo speed from core_getPulsedSol(17) pulse spacing, 64-step turbo position, switch 66 driven "
				"only when mechanics handling bits 0 and 1 are both enabled); the *** PRELIMINARY *** simulator's "
				"#define block and i500_stateDef are cross-reference only. src/wpc/core.h CORE_FIRSTUFLIPSOL=33, "
				"CORE_FIRSTLFLIPSOL=45, sURFlip=34, sLRFlip=46, sLLFlip=48, CORE_URFLIPSOLBITS=0x30, "
				"CORE_LRFLIPSOLBITS=0x03, CORE_LLFLIPSOLBITS=0x0c. src/wpc/core.c core_getSol (29-32 J111/GameOn "
				"remap, 33-36 solenoids2 with the upper-right flipper mask because FLIP_SOL(FLIP_UR) is set and raw "
				"bits 6/7 at 35/36 because FLIP_SOL(FLIP_UL) is not, 37-44 zero outside WPC-95/System 11, 45-48 "
				"lower flippers). src/wpc/wpc.c WPC_FLIPPERS complement read for non-WPC-95 generations and the "
				"always-closed switch 24 set at machine reset (coreGlobals.swMatrix[2] |= 0x08)."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-security.json",
			"revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp and five-string G.I. address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": HANDBOOK_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.indianapolis-500.1995/Indianapolis_500_OPS.pdf",
			"original_filename": "Indianapolis_500_OPS.pdf",
			"sha256": HANDBOOK_SHA256,
			"acquired_at": "2026-09-25T10:44:12Z",
			"locator": (
				"16-page Midway Manufacturing Company Indianapolis 500 Operators Handbook, 16-10140, July 1995. "
				"Internet Archive item arcademanual_Indianapolis_500_OPS (https://archive.org/details/"
				"arcademanual_Indianapolis_500_OPS), file https://archive.org/download/arcademanual_Indianapolis_500_OPS/"
				"Indianapolis_500_OPS.pdf, uploader manuallibrary@textfiles.com, collections arcademanuals/manuals, no "
				"rights metadata. Image-only 300 dpi scan: printed pages 2-3 lamp matrix and locations, 4-5 switch "
				"matrix and locations, 6-7 solenoid/flasher table, G.I. and flipper circuits and locations, 8 and 10 "
				"upper/lower playfield parts."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(HANDBOOK_EXCERPTS),
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.indianapolis-500.1995/ipdb-2853/indy500manualfull.original-scan.pdf",
			"original_filename": "indy500manualfull.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T11:02:09Z",
			"locator": (
				"152-page image-only Indianapolis 500 operations manual, IPDB machine 2853 (https://www.ipdb.org/"
				"machine.cgi?id=2853, Midway 'Indianapolis 500', June 1995, model 50026, WPC-S), resource "
				"https://www.ipdb.org/files/2853/indy500manualfull.pdf, downloaded through an authenticated browser. "
				"The untouched download is retained under this hash; a contributor-made Acrobat OCR copy "
				"(indy500manualfull.pdf, SHA-256 2cd7354de4744fcc84078dd98cb6b544bebc38780e8daf52d1454c6962340e13) "
				"is retained beside it for text search only. Section 2 printed 2-13/2-14 (A-19823 4-LED Illuminated "
				"Target PCB, A-20047 Turbo Opto PCB), 2-22 (A-19978 Pit Ramp Diverter), 2-23 (A-20038 Turbo Motor), "
				"2-29 (A-20169 Race Track); "
				"the game rules (PDF page 17, Turbo Multi-Ball); Section 3 printed 3-7 (flasher wiring), 3-20 (A-18159 10 "
				"Opto P.C.B.) and 3-25/3-26 (power driver board connector lists)."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(MANUAL_EXCERPTS),
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/indianapolis-500-1995/source/Indianapolis_500_VPX_1.1_RTM.vpx",
			"original_filename": "Indianapolis_500_VPX_1.1_RTM.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working Indianapolis 500 VPX 1.1 RTM (JPSalas VP9, Dozer VPX conversion, ramps by "
				f"Flupper, released 18 Aug 2017), VPX 10.4. Exact playfield bounds are {TABLE_BOUNDS}; normalized "
				"coordinates are x/952 and y/2162. Geometry authority for named table objects only. The contributor's "
				"collection also holds two 2020 4K MOD derivatives of this table; they are the same lineage and add "
				"no independent geometry."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, Dozer and Flupper",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/indianapolis-500-1995/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script of the retained table (53,729 bytes): cGameName = "i500_11r", UseSolenoids = 1, '
				"UseLamps = 1, HandleMechanics = 1; SolCallback/SolModCallback for solenoids 1-5, 7, 13-16, 18-28 and 36; "
				"cvpmTrough on switches 42-45 pulsing 41 on each eject; saucers/poppers on 61, 62, 64, 65; Dorsola/"
				"Dozer turbo simulator reading Controller.GetMech(0) and driving switches 63 and 66; UpdateGI dispatch "
				"Case 0 'top left' (GITL), Case 1 'top right' (GITR), Case 2 'bottom' (GIB); Lights(n) lamp bindings."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, Dorsola and Dozer",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/indianapolis-500-1995/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPW_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/Indianapolis%20500%20%28Bally%201995%29%20v1.36.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": VPW_SCRIPT_SHA256,
			"locator": (
				"Indianapolis 500 (Bally 1995) v1.36.vbs (142,080 bytes), the April 2023 TastyWasps/VPW enhancement of "
				'the same Dozer table: cGameName = "i500_11r", UseSolenoids = 2, the same SolCallback table for 1-5, 7, '
				"13-16, 18-28 and 36, the same switch handlers and turbo simulator, and additionally SolCallback(sURFlipper) "
				'= "SolURFlipper" driving the upper right flipper on its own; its KeyUpperRight key handler also calls '
				"SolURFlipper 1/0 directly (a staged-flipper convenience that bypasses the ROM). Script only; its table is "
				"not retained."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, Dorsola, Dozer and TastyWasps (VPW); corpus by sverrewl",
			"rights": "NOASSERTION",
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


def _switch_notes(address: int, column: int, row: int) -> str:
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	if address in PRINTED_SHADED_OPTOS:
		notes += (
			' Printed shaded "Opto, Typically Closed" on the switch matrix. Pinned PinMAME\'s i500GameData '
			"inverted-switch mask normalizes this address, so the public state is already normalized (1 = beam "
			"interrupted / ball present) and must not be inverted again."
		)
	if address in {41, 42, 43, 44, 45}:
		notes += " Trough LED/phototransistor pair served by the A-18159 10 Opto P.C.B. (manual printed 3-20)."
	if address in {56, 57, 58}:
		notes += (
			" The A-19823 4-LED Illuminated Target PCB carries this target's OPTO1 interrupter together with the four "
			"red LEDs of its Lightup lamps (manual printed 2-13)."
		)
	if address in {61, 62, 63}:
		notes += " Served by the A-18159 10 Opto P.C.B. (manual printed 3-20)."
	if address == 63:
		notes += (
			" The handbook and the A-20038 turbo assembly (items 12c/12d) print the LED/phototransistor pair as "
			"A-14231/A-14232, while the 10 Opto P.C.B. connector list prints A-16908/A-16909 for switch 63; both "
			"describe an opto mounted through the turbo housing wall."
		)
	if address == 66:
		notes += (
			" Both printed switch matrices (handbook printed 4 and manual printed 2-40) leave this cell unshaded, but "
			"its printed part A-20047 is the Turbo Opto PCB Assembly, whose parts list is an OPTO1 'Opto Integrated "
			"10mA' (manual printed 2-14), mounted as item 3 of the A-20038 Turbo Motor Assembly with its H-20206 "
			"Turbo Index Cable (printed 2-23). The missing shading is a printing omission: pinned PinMAME's "
			"i500GameData mask normalizes 66 exactly as it does the shaded turbo optos 61-63, so the public state "
			"is already normalized and must not be inverted again."
		)
	if address in TARGET_COLORS:
		notes += f" Stationary target, {TARGET_COLORS[address]} (upper-playfield parts list)."
	if address in {26, 27}:
		notes += " The slingshot kicker switch (SW-1A-114) and the separate score switch (SW-1A-120) share this address."
	if address == 54:
		notes += " Rubber-mounted scoring switch; the retained script pulses it from the sw54 wall's Slingshot event."
	if address == 24:
		notes += (
			" Physical part 5643-09112-00 is a permanently closed link that proves the matrix is connected; pinned "
			"PinMAME sets it closed at machine reset. The retained script writes Controller.Switch(24) = 0 in "
			"Table1_Init under the comment 'door always closed', a defect in that table rather than a fact about "
			"the machine."
		)
	if address == 22:
		notes += " Closed while the coin door is closed."
	if address == 11:
		notes += " Cabinet Launch Button (lamp 86 lights it); the retained script sets it from the plunger key."
	if address in SWITCH_PROJECTIONS:
		notes += " " + SWITCH_PROJECTIONS[address]
	elif address in SWITCH_OBJECTS:
		notes += f" Placement: retained table object {SWITCH_OBJECTS[address]}."
	return notes


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address,
				"optional" if address == 4 else "used", (HANDBOOK_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", HANDBOOK_SOURCE),
			)
		)

	cabinet_roles = {11: "cabinet.launch", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"switch.matrix-{address}"
			physical: dict[str, Any] = {}
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if address in UNUSED_MATRIX_ADDRESSES:
				physical["notes"] = f"Printed switch-matrix drive column {column}, return row {row}. The printed matrix and the switch-locations list both mark this position Not Used."
				extra["spatial"] = not_applicable("unused", HANDBOOK_SOURCE)
				items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (HANDBOOK_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			label = SWITCH_LABELS[address]
			physical["notes"] = _switch_notes(address, column, row)
			refs: tuple[str, ...] = (HANDBOOK_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address in OPTO_SWITCHES or address in {63, 66}:
				refs = (HANDBOOK_SOURCE, MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address == 24:
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", HANDBOOK_SOURCE, CORE_SOURCE)
				items.append(_device(identifier, label, "constant", "pinmame.input.switch", address, "used", (HANDBOOK_SOURCE, CORE_SOURCE), **extra))
				continue
			extra["normally_closed"] = address in OPTO_SWITCHES
			if address in PULSED_SWITCHES:
				extra["pulse"] = True
			if address in cabinet_roles:
				extra["roles"] = [cabinet_roles[address]]
				physical["location"] = "cabinet" if address in {11, 13, 23} else "cabinet interior"
				extra["spatial"] = not_applicable("cabinet_or_service", HANDBOOK_SOURCE)
				if address == 22:
					extra["initial_active"] = True
			else:
				coordinate_refs = (VPX_TABLE_SOURCE, HANDBOOK_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
				status = "observed" if address in OBSERVED_SWITCHES else "validated"
				if address in OBSERVED_SWITCHES:
					physical["notes"] += " " + OBSERVED_SWITCHES[address] + " The placement stays observed."
				extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address]], *coordinate_refs, status=status)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, **extra))

	for address, (label, role, switch_type, part, wire, connection) in FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		notes = f"Printed Fliptronic grounded switch {position} ({wire}, {connection}); switch-locations part {part}."
		if switch_type == "opto":
			notes += (
				" Printed shaded as an opto (A-17316 Flipper Opto PCB Assembly, cabinet mounted). On this generation "
				"PinMAME's WPC_FLIPPERS register read returns the complement of the whole Fliptronic column, so the "
				"public state is already normalized (1 = button pressed) and must not be inverted again."
			)
			if address == 116:
				notes += " The upper right flipper has its own cabinet opto position on the right flipper button."
		else:
			notes += " Plain end-of-stroke leaf switch (SW-1A-194) on the flipper assembly."
		items.append(
			_device(
				f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "used",
				(HANDBOOK_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				roles=[role],
				normally_closed=False,
				physical={
					"location": "cabinet flipper button" if switch_type == "opto" else "flipper assembly",
					"switch_type": switch_type,
					"part_number": part,
					"notes": notes,
				},
				wiring={"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service" if switch_type == "opto" else "internal_nonvisual", HANDBOOK_SOURCE),
			)
		)
	for address, (wire, connection, printed) in UNUSED_FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		items.append(
			_device(
				f"switch.generic-{address}", f"Not Used Upper Left Flipper Position {position}", "switch",
				"pinmame.input.switch", address, "unused", (HANDBOOK_SOURCE, CONTROLLER_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				physical={"location": "not installed", "notes": f"Printed Fliptronic grounded switch {position} '{printed}' ({wire}, {connection}) marked NOT USED; the switch-locations list prints {position} Not Used. Indianapolis 500 has no upper left flipper."},
				spatial=not_applicable("unused", HANDBOOK_SOURCE),
			)
		)

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country/option configuration bit)", "dip_switch",
				"pinmame.input.dip", address, "used", (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={
					"location": "WPC-Security CPU board",
					"switch_type": "dip",
					"notes": "WPC-Security CPU-board country/option configuration DIP bank. The retained manuals print no country-setting chart for this machine, so no ON/OFF combination is asserted here.",
				},
				spatial=not_applicable("dip_switch", CORE_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace(chr(39), '')}"


def _solenoid_notes(address: int, printed_type: str) -> str:
	printed_number = PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")
	notes = f"Printed solenoid/flasher table entry {printed_number} ({printed_type})."
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
	if address in {8, 9, 10, 11, 12}:
		notes += " The retained script binds no callback; the table's own bumper/slingshot physics fire on contact and pulse the switch."
	if address == 1:
		notes += (
			" A-14525 Kicker Bracket Assembly at the foot of the shooter lane. The retained Plunger1 object sits "
			"below the playfield bounds (normalized y 1.009131), so the placement is projected onto the shooter-lane "
			"switch SW25 directly above it; the handbook's callout 01 reaches that kicker bracket at the foot of the "
			"lane, and the placement inherits switch 25's status."
		)
	if address == 7:
		notes += " Backbox-mounted knocker (printed backbox voltage and drive connections)."
	if address == 14:
		notes += " Top-rear dome beside the upper popper; the manual's flasher drawing puts callout 14 immediately right of the top-left corner dome 15."
	if address == 17:
		notes += (
			" Printed in the Flasher category but its part is 14-8021.1 Turbo Gearmotor, 12VDC (A-20038 Turbo Motor "
			"Assembly), fed from J116-2. Pinned PinMAME's i500_handleMech models turbo speed from the spacing of "
			"pulses on this output (core_getPulsedSol(17)): no pulse for 60 updates is stopped, closely spaced "
			"pulses are fast. The upper-playfield parts list also names an A-20189 Motor EMI w/Delay Brake P.C.B."
		)
	if address == 18:
		notes += (
			" Printed in the Flasher category but its part is 14-8022 Race Track Gear Motor (A-20169 Race Track "
			"Assembly): an upright arched track at the rear of the playfield on which the motor turns a small car "
			"around a hub. The retained script spins the Indy_Top car while this output is on; its Indy_up_Flash timer also strobes the IU1-IU5 lights and car shadows as a visual effect of the spinning car. The track's reflector fixtures are wired to G.I. string 02 (see that output)."
		)
	if address == 12:
		notes += " The solenoid/flasher locations list prints this assembly as A-9362-R-3; both playfield parts lists print B-9362-R-3, which is recorded."
	if address in {19, 20, 21, 22}:
		notes += " One of the four coloured car flashers (A-17802) under the playfield car inserts."
	if address in {23, 24, 25}:
		notes += " Jet-bumper flasher in the A-20432-5 bumper wafer, placed at its bumper's retained flasher light."
	if address == 27:
		notes += (
			" Printed '#906 (2)' and 'Left Side Flasher (2)' with two assemblies (C-13337 and A-19979); the flasher "
			"drawing draws two callouts 27, one on the upper left side above the left loop and one on the lower "
			"left beside the three-bank targets, so two placements are recorded."
		)
	if address == 16:
		notes += " The retained Sol16 callback drives F16_Lamp1, F16_Lamp2 and F16_Side_Flash1; the table's F16_Lamp3/4/5 lights belong only to its G.I. string 2 collection."
	if address in {14, 15, 16}:
		notes += " The full manual's flasher wiring drawing (printed 3-7) prints the J127-7/8/9 wires as Black-Yellow/Blue-Gray/Blue-Gray; the solenoid table and the power driver board connector list (printed 3-25) both print Brown-Blue/Brown-Violet/Brown-Gray, which is recorded."
	if address in {33, 34}:
		notes += (
			" Upper right flipper (A-14876-R-3, FL-11629 coil), a real Fliptronic flipper on the right side of the "
			"playfield. i500GameData sets FLIP_SOL(FLIP_UR), so core_getSol reports public 33 as the power winding "
			"alone and public 34 as power OR hold (CORE_URFLIPSOLBITS 0x30). The Dozer 1.1 RTM script drives this "
			"flipper from the lower right flipper callback; the VPW 1.36 script binds SolCallback(sURFlipper) (34)."
		)
	if address in {35, 36}:
		notes += (
			" Printed Upper Left flipper circuit (Q1/Q5, J902-3/J902-1) whose coil cell reads 'SEE ABOVE': the "
			"Fliptronic upper-left circuit drives the A-20099 coil of the A-19978 Pit Ramp Diverter Assembly. "
			"FLIP_SOL(FLIP_UL) is not set, so PinMAME publishes the raw power (35) and hold (36) bits here. The "
			"diverter plunger turns a drive arm and the A-20413 Divertor Blade & Car Assembly; the master spring "
			"returns it when the coil is off."
		)
	if address in {45, 46, 47, 48}:
		notes += (
			f" Printed flipper circuit {printed_number}; PinMAME publishes the lower flippers at 45-48, odd addresses "
			"the power winding alone and even addresses power OR hold."
		)
	if address in SOLENOID_OBJECTS and address not in {7, 6}:
		notes += f" Placement: retained table object {SOLENOID_OBJECTS[address]}."
	return notes


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address == 6:
			items.append(
				_device(
					"device.not-used-solenoid-6", "Not Used Solenoid 6", "coil", "pinmame.output.solenoid", 6, "unused",
					(HANDBOOK_SOURCE, CORE_SOURCE),
					aliases=[{"namespace": "pinmame.solenoid", "value": "6"}, {"namespace": "manual.address", "value": "06"}],
					physical={"notes": "Printed '06 Not Used', High Power, with transistor Q66 populated but no voltage connection, drive connection, wire or coil; the locations list prints item 06 Not Used."},
					wiring={"board": "WPC-Security power driver board", "driver_transistor": "Q66"},
					spatial=not_applicable("unused", HANDBOOK_SOURCE),
				)
			)
			continue
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_WIRING[address]
			kind = "flasher" if address in FLASHERS else "motor" if address in MOTORS else "coil"
			physical: dict[str, Any] = {}
			if part and not part.startswith("#"):
				physical["part_number"] = part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if kind == "flasher":
				physical["quantity"] = 2 if address == 27 else 1
			physical["notes"] = _solenoid_notes(address, printed_type) + (f" Printed flashlamp type {part}." if part and part.startswith("#") else "")
			wiring: dict[str, Any] = {"board": "Fliptronic II board" if address in PRINTED_FLIPPER_CIRCUITS else "WPC-Security power driver board", "driver_transistor": transistor}
			if voltage:
				wiring["power_connection"] = voltage
			if drive:
				wiring["control_connection"] = drive
			if wire:
				wiring["control_wire"] = wire
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")}]
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", HANDBOOK_SOURCE)
			else:
				role = "emitter" if kind == "flasher" else "effect"
				refs = (VPX_TABLE_SOURCE, HANDBOOK_SOURCE) if address in {1, 14, 15, 16, 19, 20, 21, 22, 26, 27, 28} else (VPX_TABLE_SOURCE,)
				anchor = SOLENOID_SWITCH_ANCHORS.get(address)
				status = "observed" if anchor in OBSERVED_SWITCHES else "validated"
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *refs, status=status)
			refs = (HANDBOOK_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {17, 18, 33, 34, 35, 36}:
				refs = refs + (MANUAL_SOURCE,) if address != 33 and address != 34 else refs + (VPW_SCRIPT_SOURCE,)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not an Indianapolis 500 playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not an Indianapolis 500 playfield device.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the Game-On / flipper-enable state because i500.c configures no fast-flip address.",
			32: "PinMAME reports this WPC state channel as always zero; i500GameData declares no use for it.",
			49: "PinMAME's simulator-only ball-shooter channel; Indianapolis 500's auto plunger is solenoid 1 and has no output here.",
			50: "Reserved PinMAME output position before the first custom-output boundary; i500GameData declares no custom solenoids.",
		}.get(address, "Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and System 11.")
		roles = ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
		items.append(
			_device(
				output_id(label), label, "virtual", "pinmame.output.solenoid", address, "used" if used else "unused",
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
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			wiring = {
				"board": "WPC-Security power driver board",
				"drive_wire": drive_wire,
				"drive_connection": drive_connection,
				"return_wire": return_wire,
				"return_connection": return_connection,
				"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
			}
			aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
			if address in UNUSED_LAMPS:
				items.append(
					_device(
						identifier, f"Not Used Lamp {address}", "lamp", "pinmame.output.lamp", address, "unused", (HANDBOOK_SOURCE, CONTROLLER_SOURCE),
						aliases=aliases, wiring=wiring,
						physical={"notes": f"Printed lamp-matrix column {column}, row {row}: NOT USED on the matrix and 'Not Used' with no bulb or assembly in the lamp-locations list."},
						spatial=not_applicable("unused", HANDBOOK_SOURCE),
					)
				)
				continue
			physical: dict[str, Any] = {"quantity": 1, "assembly_part_number": LAMP_ASSEMBLIES[address]}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}." + LAMP_CONNECTOR_NOTE
			refs: tuple[str, ...] = (HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring, "physical": physical}
			if address in LIGHTUP_TARGETS:
				target = LIGHTUP_TARGETS[address]
				notes += (
					f" Red LED on the A-19823 4-LED Illuminated Target PCB of the lightup target at switch {target}; "
					"the lamp-locations list prints no bulb number. The four LEDs sit in a 2x2 group on the upright "
					"board (printed LED3 top left, LED2 top right, LED4 bottom left, LED1 bottom right), so upper/lower "
					"differ in height above the playfield, not in playfield position. The retained table renders each "
					"address with two offset glow lights; the placement is projected onto the target face itself "
					f"(Wall sw{target} bounding-box center)."
				)
				refs = (HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
				status = "observed" if target in OBSERVED_SWITCHES else "validated"
				if target in OBSERVED_SWITCHES:
					notes += f" Observed only, like switch {target}'s own placement."
				extra["spatial"] = located(identifier, "emitter", [SWITCH_POSITIONS[target]], VPX_TABLE_SOURCE, MANUAL_SOURCE, status=status)
			elif address in {86, 87, 88}:
				notes += " Lamp inside the illuminated cabinet button assembly; the manual draws its callout below the cabinet outline. The power driver board connector list routes rows 6-8 to the cabinet lamps through J134-7/8/9."
				extra["roles"] = ["cabinet.launch" if address == 86 else "cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", HANDBOOK_SOURCE)
				refs = (HANDBOOK_SOURCE, CORE_SOURCE)
			else:
				bulb = LAMP_BULBS.get(address, "#555")
				notes += f" Printed bulb {'24-6549' if bulb == '#44' else '24-8768'} ({bulb})."
				if address == 18:
					notes += " The lamp-locations list prints item 18 'Left Ramp Wrench' and item 27 'Turbo Wrench', swapping the two names against the lamp matrix; the matrix labels are used because the retained table places 18 beside the turbo (and its Turbo Wrench target 47) and 27 beside the Left Ramp Wrench target 55."
				if address == 27:
					notes += " See lamp 18: the lamp-locations list swaps the two wrench names."
				if address in LAMP_HELPERS:
					notes += f" The retained script binds a second render light {LAMP_HELPERS[address]} to this address at a different position; the manual prints one bulb, so only the primary insert light is placed."
				notes += f" Placement: retained table Light l{address}."
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE)
			physical["notes"] = notes
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, voltage, transistor, drive, wire, bulbs) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} '{label}' (G.I. String {address + 1}); printed lamps {bulbs}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}],
			"wiring": {"board": "WPC-Security power driver board", "power_connection": voltage, "driver_transistor": transistor, "control_connection": drive, "control_wire": wire},
		}
		physical: dict[str, Any] = {}
		refs: tuple[str, ...] = (HANDBOOK_SOURCE, CORE_SOURCE, MANUAL_SOURCE)
		notes += (
			" The power driver board connector list (manual printed 3-25) labels J120 'to playfield' and J121 'to "
			"insert', the reverse of the handbook table's Playfield/Backbox columns; the handbook's per-string names, "
			"the retained script's per-string playfield dispatch and the race-track reflector wiring (G.I. string 02 "
			"colours on the playfield) all follow the handbook table, which is recorded."
		)
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				f" The manual prints no per-string bulb list or count, so the quantity counts playfield sockets "
				f"only and every coordinate comes from the retained table's {GI_COLLECTIONS[address]} collection, "
				f"which the retained script's UpdateGI dispatches for this string. Distinct bulb-mesh lights are placed "
				f"once each; excluded: {GI_EXCLUDED[address]}. These placements are observed, not validated: no "
				"factory source lists the sockets."
			)
			if address == 1:
				notes += (
					" This string also lights the race track: the A-20169 Race Track Assembly drawing (manual printed "
					"2-29) shows two 04-10094 reflector socket assemblies at the top corners of the arch, each drawn with "
					"two reflector cones, with every socket lead labelled ORG and ORG/WHT. ORG is read as this string's "
					"Orange return (J121-2) and ORG/WHT as its White-Orange 6.8VAC feed (J121-8); that is an inference, "
					"since the connector list prints White-Orange and this manual elsewhere distinguishes reversed colour "
					"orders, but it is supported by string 02 being the only string that prints #555 bulbs on the "
					"playfield. The drawing prints no bulb count, so the quantity counts "
					"the placed sockets only and the race-track bulbs are neither counted nor placed. The retained table "
					"lights the track's left corner from this string's collection (F16_Lamp4, no bulb mesh) and strobes "
					"separate IU1-IU5 lights with the spinning car (solenoid 18) as an effect."
				)
			if address in {0, 2}:
				notes += " The printed string also feeds #555 backbox bulbs (backbox connections), which are not placed."
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, status="observed")
			refs = (HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		else:
			notes += " Backbox string (printed backbox connections only); the retained script's UpdateGI implements no case for it."
			if address in {3, 4}:
				notes += (
					" Which backbox string also feeds the coin door is not settled: the handbook names string 04 "
					"'Backbox-Coindoor', while the power driver board connector list (printed 3-25) routes a White-Violet "
					"6.8VAC / Violet return G.I. pair through J119 to the A-17051-1 coin door interface board (J2-3/J2-5), "
					"and White-Violet is string 05's printed drive-wire colour. That colour match is only an inference, "
					"so neither string is given a coin-door role."
				)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", HANDBOOK_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", refs, **extra))
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
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": pdesc} for pid, plabel, psensors, pdesc in positions]
		return record

	return [
		mechanism(
			"mechanism.trough", "Four-ball trough", "kicker", [output_id("Trough")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44", "switch.matrix-45"],
			"Four balls rest on the trough optos 42 (Trough 1, right, nearest the eject) to 45 (Trough 4, left); 41 "
			"(Top Trough) is the fifth opto position on the same A-19963 outhole ball trough. All five are "
			"LED/phototransistor pairs on the A-18159 10 Opto P.C.B. and are normalized by PinMAME. Solenoid 13 "
			"(Trough) ejects the ball on 42 into the shooter lane. The retained script's cvpmTrough holds the balls "
			"on 42-45 and pulses 41 in the same event as each eject; pinned PinMAME's preliminary simulator calls 41 "
			"'Trough Jam' and routes the ejected ball through it to the shooter lane.",
			[
				("ball-1", "Trough 1 (eject position)", ["switch.matrix-42"], "Ball nearest the eject coil."),
				("ball-2", "Trough 2", ["switch.matrix-43"], "Second trough position."),
				("ball-3", "Trough 3", ["switch.matrix-44"], "Third trough position."),
				("ball-4", "Trough 4 (left)", ["switch.matrix-45"], "Fourth trough position, at the drain entrance."),
				("top", "Top Trough", ["switch.matrix-41"], "Top trough opto; pulsed with each eject by the retained script."),
			],
			HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-19963",
		),
		mechanism(
			"mechanism.auto-plunger", "Shooter lane and auto plunger", "kicker", [output_id("Auto Plunger")],
			["switch.matrix-25", "switch.matrix-11"],
			"A ball served from the trough rests on Shooter Lane (25). The ROM fires solenoid 1, the A-14525 kicker "
			"bracket at the foot of the lane, to launch it, either automatically or when the player presses the "
			"cabinet Ball Launch button (11, lit by lamp 86). There is no manual plunger; the retained script's "
			"Plunger1 object stands in for the auto-launch kicker.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-25"], "Shooter lane switch.")],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.turbo", "Turbo ball lock", "motorized",
			[output_id("Turbo Popper"), output_id("Turbo Motor")],
			["switch.matrix-62", "switch.matrix-63", "switch.matrix-66"],
			"A ball entering the turbo popper at the upper left (opto 62, A-20159 Ball Popper Assembly) is raised by "
			"solenoid 5 up the A-20407 Turbo Feed Wire Ramp into the turbo: a horizontal impeller (03-9343) inside the "
			"A-20065 housing, turned by the 12VDC 14-8021.1 gearmotor of the A-20038 Turbo Motor Assembly on "
			"solenoid 17. The manual's rules lock two balls to start a 3-ball multiball, award the Super Jackpot for re-locking "
			"the third, and serve an extra ball when every ball in play is locked (four balls at most); the manual "
			"prints no physical capacity. Turbo Ball Sense (63) is the "
			"LED/phototransistor pair through the housing wall; Turbo Index (66) is the A-20047 Turbo Opto PCB under "
			"the impeller. Turned slowly the turbo stores balls; spun up it throws them out onto the 12-7273.2 Turbo "
			"Exhaust Ramp. Pinned PinMAME models speed from the spacing of solenoid-17 pulses (stopped after 60 "
			"updates without a pulse, fast when pulses arrive within two updates) and a 64-step position that "
			"closes 66 for the first three of every sixteen steps. The retained script's own Dorsola/Dozer simulator "
			"reads Controller.GetMech(0) for the speed, advances a four-position model, opens 66 once per quadrant "
			"and closes it for the other three sub-steps, closes 63 when a ball sits in the sensed quadrant, and "
			"ejects the ball there at fast speed. The two duty cycles for 66 differ; the definition asserts only "
			"that 66 is an index opto read by the ROM, not its duty cycle.",
			[
				("entry", "Ball at the turbo popper", ["switch.matrix-62"], "Turbo Popper opto."),
				("ball-sense", "Ball sensed in the turbo", ["switch.matrix-63"], "Turbo Ball Sense opto through the housing wall."),
				("index", "Turbo index", ["switch.matrix-66"], "Turbo Index opto under the impeller."),
			],
			HANDBOOK_SOURCE, MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20038",
		),
		mechanism(
			"mechanism.race-track", "Race track car", "motorized", [output_id("Race Track Motor")], [],
			"The A-20169 Race Track Assembly is an upright arched weldment at the rear of the playfield. Solenoid 18 "
			"drives its 14-8022 gear motor, which turns a hub carrying a small car and driver around the face of the "
			"arch; a 04-10094 reflector fixture sits at each top corner, wired ORG and ORG/WHT, the colours of G.I. string 02 "
			"(Upper Right Playfield); each assembly is drawn with two reflector cones and the drawing prints no bulb "
			"count. No switch reports the car's position. The retained script rotates the Indy_Top car while the "
			"output is on and strobes its IU1-IU5 lights and car shadows with it as an effect.",
			[],
			HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20169",
		),
		mechanism(
			"mechanism.pit-ramp-diverter", "Pit ramp diverter", "gate",
			[output_id("Pit Ramp Diverter Power"), output_id("Pit Ramp Diverter Hold")], [],
			"The A-19978 Pit Ramp Diverter Assembly on the left of the playfield is a plunger coil (A-20099) on the "
			"Fliptronic upper-left circuits: 35 is the power winding and 36 the hold winding. The plunger turns a "
			"drive arm and the A-20413 blade carrying a large car and driver; the master spring returns it when the "
			"coil is released. No switch senses its position. The retained script binds only the hold winding (36): "
			"energized it lowers the Indy_Bottom car and raises the DiverterOn wall, released it restores the "
			"DiverterOff wall.",
			[],
			HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-19978",
		),
		mechanism(
			"mechanism.upper-popper", "Upper popper", "kicker", [output_id("Upper Popper")], ["switch.matrix-61"],
			"A ball dropping into the upper popper at the rear (opto 61, A-20235 Ball Popper Assembly) is raised by "
			"solenoid 2 onto the 12-7282 Rear Wire Ramp; the retained script lifts it from sw61 to sw61a and kicks it on.",
			[("ball", "Ball in the upper popper", ["switch.matrix-61"], "Upper Popper opto.")],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20235",
		),
		mechanism(
			"mechanism.upper-eject", "Upper eject", "kicker", [output_id("Upper Eject")], ["switch.matrix-64"],
			"A saucer at the top centre (switch 64, A-17985-R Eject Switch Assembly) kicked by solenoid 3 (B-9361-R-1 "
			"Ball Eject Assembly).",
			[("ball", "Ball in the upper eject", ["switch.matrix-64"], "Upper Eject switch.")],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="B-9361-R-1",
		),
		mechanism(
			"mechanism.lower-eject", "Lower eject (lower kicker)", "kicker", [output_id("Lower Eject")], ["switch.matrix-65"],
			"A kicker in the right-centre of the playfield (switch 65 Lower Kicker, A-20406 switch and bracket) "
			"kicked by solenoid 4 (A-20450 Kicker Assembly with A-20451 coil and bracket); the retained script "
			"animates a hammer arm while ejecting.",
			[("ball", "Ball in the lower kicker", ["switch.matrix-65"], "Lower Kicker switch.")],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20450",
		),
		mechanism(
			"mechanism.lightup-targets", "Lightup targets", "other", [],
			["switch.matrix-56", "switch.matrix-57", "switch.matrix-58"],
			"Three A-19820-1 Illuminated Target Assemblies (left, center, right), each with an A-19823 board that "
			"carries the target's OPTO1 interrupter (switches 56-58) and four red LEDs driven as lamp-matrix "
			"addresses (Lightup 1 = 71-74, Lightup 2 = 75-78, Lightup 3 = 81-84).",
			[
				("left", "Left Lightup", ["switch.matrix-56"], "Lightup 1 LEDs 71-74."),
				("center", "Center Lightup", ["switch.matrix-57"], "Lightup 2 LEDs 75-78."),
				("right", "Right Lightup", ["switch.matrix-58"], "Lightup 3 LEDs 81-84."),
			],
			HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-19820-1",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other",
			[output_id("Left Jet"), output_id("Right Jet"), output_id("Center Jet")],
			["switch.matrix-72", "switch.matrix-73", "switch.matrix-74"],
			"Three A-9415-2 jet bumpers with A-12030-3 switch assemblies and A-20432-5 flasher wafers (flashers 23-25). "
			"The retained script's Bumper1/Bumper2/Bumper3 handlers pulse 72/73/74, matching the printed Left/Right/"
			"Center names to the objects' positions.",
			[
				("left", "Left jet", ["switch.matrix-72"], "Table object Bumper1."),
				("right", "Right jet", ["switch.matrix-73"], "Table object Bumper2."),
				("center", "Center jet", ["switch.matrix-74"], "Table object Bumper3, below the other two."),
			],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-26", "switch.matrix-27"],
			"A-17811 slingshot kicker assemblies; each carries a kicker switch (SW-1A-114) and a score switch (SW-1A-120) "
			"on one address.",
			[("left", "Left slingshot", ["switch.matrix-26"], "Left slingshot."), ("right", "Right slingshot", ["switch.matrix-27"], "Right slingshot.")],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-17811",
		),
		mechanism(
			"mechanism.flippers", "Three flippers", "other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
				output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114", "switch.generic-115", "switch.generic-116"],
			"Lower right (A-15849-R-2), lower left (A-15849-L-2) and upper right (A-14876-R-3) Fliptronic flippers, all "
			"FL-11629 blue coils with separate power and hold windings, each with a cabinet opto (112, 114, 116) and an "
			"end-of-stroke leaf switch (111, 113, 115). The upper right flipper sits on the right side at "
			"mid-playfield below the right ramp. The ROM energizes the power and hold windings on the button and "
			"switches the power transistor off when it reads the end-of-stroke input close; the hold winding keeps "
			"the flipper up while the button stays pressed.",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112, EOS 111."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114, EOS 113."),
				("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button opto 116, EOS 115."),
			],
			HANDBOOK_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, VPW_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [output_id("Knocker")], [],
			"Solenoid 7 fires the B-10686-1 knocker in the backbox.",
			[],
			HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="B-10686-1",
		),
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
			"id": "bally.indianapolis-500.1995",
			"name": "Indianapolis 500",
			"manufacturer": "Bally",
			"year": 1995,
			"kind": "physical_pinball",
			"ipdb_id": 2853,
			"opdb_id": "Gr8l3-MDWr0",
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
				"spatial_placement": "observed",
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
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/indianapolis-500-1995.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Indianapolis 500 device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	observed_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
			continue
		placement_count += len(spatial["placements"])
		(observed_inputs if spatial["status"] == "observed" else located_inputs).append(address)
	located_outputs: list[dict[str, Any]] = []
	observed_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
			continue
		placement_count += len(spatial["placements"])
		(observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
	order = lambda item: (item["group"], item["address"])  # noqa: E731
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "observed",
		"blockers": [
			"Playfield general illumination (G.I. strings 1-3, public 0-2) has no factory socket list: the manuals "
			"print only the string names, connectors and bulb types. Every playfield G.I. coordinate therefore comes "
			"from the retained table's GITL/GITR/GIB collections that its UpdateGI dispatches per string, reduced to "
			"distinct bulb-mesh lights, and stays observed. Promotion needs a socket-level G.I. survey of a real "
			"machine, or a factory drawing that assigns each playfield G.I. socket to its string.",
			"The race track's two reflector fixtures belong to G.I. string 2 by their factory wire colours, but the "
			"drawing prints no bulb count and the retained table models no bulb there, so they are neither counted "
			"nor placed.",
			"Switches 54 (Ten Point) and 75 (Right Ramp Enter) stay observed: through the refitted handbook switch "
			"drawing, callout 54 ends 0.075 from its wall and callout 75 0.064-0.078 from its trigger, above the "
			"0.07 limit.",
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
			"manifest_uri": "external:pinmame-vpx-sources/bally/indianapolis-500-1995/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"handbook_sha256": HANDBOOK_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"manual_reconciliation": {
			"artifact": "external:pinmame-review-artifacts/indianapolis-500/manual-reconciliation.md",
			"artifact_sha256": "f17854d1855d8b40243376c36a26a40d2e535066db6efdf32591fe5aae23623c",
			"overlay_images": {
				"external:pinmame-review-artifacts/indianapolis-500/switch-drawing-overlay.png": "ae8fca87f22222326ca7e52182036c74ef0737e901dd4f8ccbf2f00523208685",
				"external:pinmame-review-artifacts/indianapolis-500/switch-drawing-overlay-0.png": "89aa6bed040faaeb860cbe9e9d83baf6b31b839bb5c1e75e3805efc80597d9f5",
				"external:pinmame-review-artifacts/indianapolis-500/switch-drawing-overlay-1.png": "aa041b17a37be08d182d2f57d6aad4a48b711d48bff580f7568556fb326ad439",
				"external:pinmame-review-artifacts/indianapolis-500/switch-drawing-overlay-2.png": "ab5797393c2c3b2c92c97aa2dc146f3b5cf7d6c8979b65f38e5c9c25422cdd05",
			},
			"coil_and_flasher_callouts": "All 28 callouts on the handbook's solenoid/flasher location drawing (printed 7) were measured through a least-squares refit; every one reaches its table object within 0.07 normalized (largest 18 at 0.064 and the lower 27 socket at 0.065) except 01, the documented auto-plunger projection.",
			"switch_callouts": "Every placed switch was overlaid on the handbook's switch-location drawing (printed 5) through a seven-point fit and ends on or within about a marker width of its marker; the four closest calls (25, 35, 54, 75) were re-measured through a ten-point least-squares refit, which keeps 54 (0.075) and 75 (0.064-0.078) observed. The other switches were not re-measured through the refit. The documented projections (trough optos 41-45, turbo optos 63/66) are exempt from the distance rule; their callouts reach the trough and the turbo.",
			"transforms": "Both drawings are normalized through least-squares refits recorded in the artifact: page 9 through its 19 originally measured callouts, page 7 through ten leader endpoints including three in the lower third.",
			"rule": "A measured placement agrees when the drawing callout reaches the same physical feature within 0.07 normalized units, inclusive; a placement with any read above the limit is kept observed, and so is anything projected onto an observed placement.",
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"observed_input_addresses": sorted(observed_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=order),
		"observed_output_bindings": sorted(observed_outputs, key=order),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [
			{"group": "pinmame.output.lamp", "address": address, "reason": f"Lightup LED projected onto its target face, Wall sw{target}."}
			for address, target in sorted(LIGHTUP_TARGETS.items())
		]
		+ [{"group": "pinmame.output.solenoid", "address": 1, "reason": "Auto plunger projected onto shooter-lane switch SW25; the Plunger1 object lies below the playfield bounds."}],
		"coordinate_origins": {
			"bounding_box_centers": ["Wall LeftSlingShot (switch 26, solenoid 11)", "Wall RightSlingShot (switch 27, solenoid 12)", "Wall sw54", "Wall sw56", "Wall sw57", "Wall sw58"],
			"object_centers": "every other placement uses its retained object's own center",
		},
		"excluded_object_classes": [
			"Second render lights bound to lamps 14, 16, 17, 21, 22 and 23 (L14a, L16a, L17a, L21a, L22a, L23a); the manual prints one bulb per lamp.",
			"Both glow lights per Lightup LED address (L71-L74 with L71x-L74x, L75x-L84x with L75x1-L84x1); the LEDs are projected onto their target face.",
			"G.I. collection members without a bulb mesh, including F16_Lamp3/4/5 in GITR (named after flasher 16 but driven only as G.I.).",
			"Race-track lights IU1-IU5, a strobe effect the retained script runs with the spinning car (solenoid 18).",
			"The ToyMod duplicates Track1, Track3, Indy_Shaft1, Indy_Shaft3 and TopCar_Base2 (invisible option objects at the upper left).",
			"Plunger1 (normalized y 1.009131, below the playfield bounds).",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Indianapolis 500 (Bally, 1995) spatial review",
		"",
		f"Status: {report['status']}. Every switch, coil, flasher, motor and lamp is placed from the retained table "
		"or carries a controlled `not_applicable` record. The playfield general-illumination strings are placed but "
		"only `observed`, switches 54 and 75 are `observed`, and the race track's G.I. reflector bulbs are not placed, which "
		"keeps the record at "
		"`machines/partial/bally/indianapolis-500-1995.json`.",
		"",
		f"The geometry source is the retained known-working `Indianapolis_500_VPX_1.1_RTM.vpx` (SHA-256 "
		f"`{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding authority. Exact "
		f"playfield bounds are `{TABLE_BOUNDS}`; every coordinate is x/952 and y/2162 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime authority; the July 1995 Operators Handbook and the 152-page operations "
		"manual are the physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; "
		"the retained table supplies geometry.",
		f"- Manual reconciliation (`{report['manual_reconciliation']['artifact']}`): "
		f"{report['manual_reconciliation']['coil_and_flasher_callouts']} {report['manual_reconciliation']['switch_callouts']}",
		"- Sensors inside a mechanism (the trough optos, the turbo's ball-sense and index optos) and the Lightup LEDs "
		"are documented projections onto the mechanism or target that carries them.",
		"- Left Side Flasher 27 has two sockets and two placements; every other flasher has one.",
		"- G.I. strings 4 and 5 and the backbox bulbs of strings 1 and 3 are backbox devices and are not placed.",
		"",
		"## Blockers",
		"",
	]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Explicit projections", ""]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
		f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
		f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
		f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
	]
	lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
	lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Refused. `coverage.missing` is `[\"spatial_placement\"]`: the playfield G.I. sockets are known only from one "
		"community table's light collections, the race-track reflector bulbs are neither counted nor placed, and "
		"switches 54 and 75 fail the factory switch-drawing check.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Handbook SHA-256 `{HANDBOOK_SHA256}`; operations manual SHA-256 `{MANUAL_SHA256}`.",
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
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("Stale Indianapolis 500 author-ready definition is still present")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"Indianapolis 500 artifact is missing: {path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Indianapolis 500 definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Indianapolis 500 seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Indianapolis 500 spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Indianapolis 500 spatial review drifted from its deterministic curator: {markdown_path}")
	print("Indianapolis 500 definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, seed and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		print(f"Indianapolis 500 extraction manifest written: {write_extraction_manifest(root)}")
	elif args.verify_extraction:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		verify_extraction_manifest(root)
		print("Indianapolis 500 retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
