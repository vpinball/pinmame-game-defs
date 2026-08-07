"""Curate the physical Bally The Addams Family (1992) machine definition.

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
DEFINITION_PATH = ROOT / "machines/partial/bally/the-addams-family-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/the-addams-family-1992.json"
SEED_PATH = ROOT / "tools/seeds/bally/the-addams-family-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/the-addams-family-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/the-addams-family-1992.md"
STUB_PATH = ROOT / "machines/stubs/taf_l5.json"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.bally.the-addams-family.1992.ops"
MANUAL_HANDBOOK_SOURCE = "manual.bally.the-addams-family.1992.handbook"
MANUAL_SCHEMATIC_SOURCE = "manual.bally.the-addams-family.1992.wpc-schematic"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.the-addams-family.1992"
VPX_TABLE_SOURCE = "vpx-table.taf-g5k-2-3-2"
VPX_SCRIPT_SOURCE = "vpx-script.taf-g5k-2-3-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.taf-g5k-2-3-2"
IPDB_SOURCE = "ipdb.bally.the-addams-family.1992"

TABLE_SHA256 = "85af088f0ed6d59c83599102e6245cc2eab5674e69d29882db6f0eaacf05e858"
SCRIPT_SHA256 = "c5f1aedc5f05c277459d97be18046f07e2617522841545317ebdfad4ec34e2fc"
OPS_MANUAL_SHA256 = "3cca7c4adc6280f42515fcc117457e32bf723b3d3a7005123d8094b3c65e2662"
HANDBOOK_SHA256 = "76c468eb747a61a176874d3b02cb495451eea9b5f9268a69ba58603bc8a9cf8f"
SCHEMATIC_SHA256 = "074431d774b1410fd6d38191ace4150866023c66e2d3a5185361f114ca4afedd"
MANUAL_TRANSCRIPTION_SHA256 = "17e8aed2524e79b671633026c0872cda8c6724d5d2e3b2bf9d6c49018fb5462e"

EXTRACTION_RELATIVE_PATH = Path("bally/the-addams-family-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/the-addams-family-1992/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "d79a5a3723fbd4041460764ec598a78683963370566033d0701cacc93ad1d4dc"
EXTRACTION_FILE_COUNT = 1277
EXTRACTION_TOTAL_BYTES = 415715342

TABLE_BOUNDS = "left=0 top=0 right=952.965 bottom=2164.76"
BOUNDS_X = 952.965
BOUNDS_Y = 2164.76

DRIVER_IDS = (
	"taf_l5", "taf_p2", "taf_p3", "taf_l1", "taf_d1", "taf_l2", "taf_d2", "taf_l3", "taf_d3",
	"taf_l4", "taf_d4", "taf_l5c", "taf_l7", "taf_d7", "taf_d7bs", "taf_l6", "taf_d6", "taf_h4",
	"taf_i4", "taf_d5",
)
DRIVER_COMPATIBILITY = {
	"taf_l5": (
		"identical",
		"Bally production L-5 game ROM shipped with the physical machine; the switch matrix, lamp "
		"matrix, solenoid/flasher table, and playfield hardware documented here are unchanged across "
		"the whole taf_* clone tree.",
	),
	"taf_p2": ("identical", "P-2 prototype ROM (WPC 20017 SYS 2.19 REV 13.2), an early prototype revision of the same physical machine."),
	"taf_p3": ("identical", "P-3 prototype ROM with the LED Ghost Fix (WPC 20017 SYS 2.19 REV 13.3)."),
	"taf_l1": ("identical", "L-1 production game ROM (SYS 2.21 REV 0.1), an early production firmware revision."),
	"taf_d1": ("identical", "D-1 LED Ghost Fix ROM pairing with L-1 (SYS 2.21 REV 7.6)."),
	"taf_l2": ("identical", "L-2 production game ROM (SYS 2.25 REV 0.2)."),
	"taf_d2": ("identical", "D-2 LED Ghost Fix ROM pairing with L-2 (SYS 2.25 REV 7.6)."),
	"taf_l3": ("identical", "L-3 production game ROM (SYS 2.28 REV 0.3)."),
	"taf_d3": ("identical", "D-3 LED Ghost Fix ROM pairing with L-3 (SYS 2.28 REV 7.6)."),
	"taf_l4": ("identical", "L-4 production game ROM (SYS 2.31 REV 0.4)."),
	"taf_d4": ("identical", "D-4 LED Ghost Fix ROM pairing with L-4 (SYS 2.31 REV 7.6)."),
	"taf_l5c": ("identical", "L-5C Competition ROM (LED Ghost MOD, patch 3901); a home/competition patch of L-5 for the same physical machine (SYS 2.48 REV 0.5)."),
	"taf_l7": (
		"identical",
		"Internally named L-7, a later prototype revision (SYS 2.43 REV 0.7). Pinned PinMAME's own "
		"comment: its internal name was apparently L-7, but the officially released L-5 folds in all "
		"the changes up to an internal L-5 prototype named L-8. This is the driver the retained "
		"known-working VPX table binds to (cGameName = \"TAF_L7\"), so it is this definition's primary "
		"cross-check target.",
	),
	"taf_d7": ("identical", "D-7 LED Ghost Fix ROM pairing with the L-7 prototype (SYS 2.43 REV 7.6)."),
	"taf_d7bs": (
		"compatible",
		"Community 2026 RedBall patch of the L-7 prototype adding a configurable ball-saver feature "
		"(Adjustment A.2, setting 33) plus the No-Ghosting patch; a firmware modification of the same "
		"physical machine's ROM, not a different physical edition.",
	),
	"taf_l6": ("identical", "L-6 game ROM released only to a German distributor (SYS 2.55 REV 0.6)."),
	"taf_d6": ("identical", "D-6 LED Ghost Fix ROM pairing with L-6 (SYS 2.55 REV 7.6)."),
	"taf_h4": ("identical", "H-4 game ROM (SYS 3.21 REV 0.6), the newest known TAF revision with additional home settings."),
	"taf_i4": ("identical", "I-4 LED Ghost Fix ROM pairing with H-4 (SYS 3.21 REV 7.6)."),
	"taf_d5": (
		"identical",
		"D-5 LED Ghost Fix ROM (SYS 2.43 REV 0.5). Pinned PinMAME's own comment: this one is a weird "
		"one, appearing closer to L-7 than L-5, seemingly a version of taf_l7 with slightly different "
		"German translations.",
	),
}

# ---------------------------------------------------------------------------
# Printed Switch Locations parts list (Operations Manual printed 2-39), the
# preferred label source. Values are (assembly_part_number, switch_part_number).
# ---------------------------------------------------------------------------
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Trough", 16: "Center Trough", 17: "Right Trough", 18: "Outhole",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Opto", 24: "Always Closed",
	25: "Right Flipper Lane", 26: "Right Outlane", 27: "Ball Shooter",
	31: "Upper Left Jet", 32: "Upper Right Jet", 33: "Center Left Jet", 34: "Center Right Jet", 35: "Lower Jet",
	36: "Left Slingshot", 37: "Right Slingshot", 38: "Upper Left Loop",
	41: 'Grave "G"', 42: 'Grave "R"', 43: "Chair Kickout", 44: "Cousin It",
	45: "Lower Swamp Million", 47: "Center Swamp Million", 48: "Upper Swamp Million",
	51: "Shooter Lane",
	53: "Bookcase Opto 1", 54: "Bookcase Opto 2", 55: "Bookcase Opto 3", 56: "Bookcase Opto 4",
	57: "Bumper Lane Opto", 58: "Right Ramp Exit",
	61: "Left Ramp Enter", 62: "Train Wreck", 63: "Thing Eject Lane", 64: "Right Ramp Enter",
	65: "Right Ramp Top", 66: "Left Ramp Top", 67: "Upper Right Loop", 68: "Vault",
	71: "Swamp Lock Upper", 72: "Swamp Lock Center", 73: "Swamp Lock Lower", 74: "Lockup Kickout",
	75: "Left Outlane", 76: "Left Flipper Lane 2", 77: "Thing Kickout", 78: "Left Flipper Lane 1",
	81: "Bookcase Open", 82: "Bookcase Closed", 84: "Thing Down Opto", 85: "Thing Up Opto",
	86: 'Grave "A"', 87: "Thing Eject Hole",
}
# Printed "Not Used" on the Switch Locations parts list (2-39) and the Switch Matrix (handbook p.9-10).
# 23 (Ticket Opto) is included: both its Switch Number and Switch Assy print blank/"Not Used".
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 28, 46, 52, 83, 88}
# Opto sweep (Non-negotiable #1): blank Switch Number + populated (paired) opto assembly part number,
# with "Opto" in the printed description. Cross-checked column-by-column against tafGameData's
# inverted-switch mask below with full agreement -- no conflict recorded.
OPTO_SWITCHES = {53, 54, 55, 56, 57, 84, 85}
PINMAME_NORMALIZED_OPTO_SWITCHES = OPTO_SWITCHES

SWITCH_TYPES = {
	13: "button", 14: "tilt", 24: "other",
	41: "leaf", 42: "leaf", 44: "leaf", 45: "leaf", 47: "leaf", 48: "leaf", 62: "leaf", 86: "leaf",
	53: "opto", 54: "opto", 55: "opto", 56: "opto", 57: "opto", 84: "opto", 85: "opto",
}

# address -> (assembly_part_number, switch_part_number), transcribed verbatim from printed 2-39.
SWITCH_PARTS = {
	13: (None, "20-9663-1"), 14: (None, "20-6502-A"),
	15: ("B-8925", "5647-09957-00"), 16: ("B-8925", "5647-09957-00"),
	17: ("A-11680", "5647-12693-08"), 18: ("A-10417", "5647-12133-12"),
	21: (None, "27-1066"), 22: (None, "A-8630"), 24: (None, "A-8630"),
	25: ("A-12688", "5647-12693-19"), 26: ("A-12688", "5647-12693-19"), 27: ("A-11619", "5647-12693-04"),
	31: ("B-12030-2", "SW-11A-37"), 32: ("B-12030-2", "SW-11A-37"), 33: ("B-12030-2", "SW-11A-37"),
	34: ("B-12030-2", "SW-11A-37"), 35: ("B-12030-2", "SW-11A-37"),
	36: ("B-8284-1", "SW-1A-114"), 37: ("A-11539-1", "SW-1A-120"), 38: ("A-12688", "5647-12693-19"),
	41: ("B-11696-1", None), 42: ("B-11696-1", None), 43: ("A-14962", "5647-12693-25"),
	44: ("B-11696-4 (a1/a2) with B-12583-4 (b1/b2)", None),
	45: ("B-11696-15", None), 47: ("B-11696-15", None), 48: ("B-11696-15", None),
	51: ("A-15372", "5647-12693-19"),
	53: ("A-15017/A-15018", None), 54: ("A-15017/A-15018", None), 55: ("A-15017/A-15018", None),
	56: ("A-15017/A-15018", None), 57: ("A-14231/A-14232", None), 58: ("A-14972", "5647-12693-21"),
	61: ("A-14492", "5647-12693-11"), 62: ("B-11696-5", None), 63: ("A-12688", "5647-12693-19"),
	64: ("A-13627-2", "5647-12693-11"), 65: ("A-15047", "5647-12693-21"), 66: ("A-15047", "5647-12693-21"),
	67: ("A-12688", "5647-12693-19"), 68: ("A-15070", "5647-12693-08"),
	71: ("A-14964", "5647-12693-25"), 72: ("A-14964", "5647-12693-25"), 73: ("A-14964", "5647-12693-25"),
	74: ("A-14964", "5647-12693-25"), 75: ("A-12688", "5647-12693-19"), 76: ("A-12688", "5647-12693-19"),
	77: ("A-15200", "5647-12693-25"), 78: ("A-12688", "5647-12693-19"),
	81: ("A-14970", "5647-12693-08"), 82: ("A-14970", "5647-12693-08"),
	84: ("A-15285", None), 85: ("A-15285", None), 86: ("B-12583-1", None), 87: ("A-9381-R", "5647-12133-11"),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"),
	3: ("Orange-Black", "J205-3"), 4: ("Orange-Yellow", "J205-4"),
	5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
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
# Fliptronic F1-F8 wiring, Operator's Handbook printed page 9-10 (right-hand block).
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J806-1"), 112: ("Blue-Violet", "J805-1"),
	113: ("Black-Blue", "J806-3"), 114: ("Blue-Gray", "J805-2"),
	115: ("Black-Violet", "J806-4"), 116: ("Black-Yellow", "J805-3"),
	117: ("Black-Gray", "J806-5"), 118: ("Black-Blue", "J805-5"),
}

# ---------------------------------------------------------------------------
# Printed Solenoid Table (Operator's Handbook printed page 5).
# ---------------------------------------------------------------------------
SOLENOID_LABELS = {
	1: "Chair Kickout", 2: "Thing Knocker", 3: "Ramp Diverter", 4: "Ball Release", 5: "Outhole",
	6: "Thing Magnet", 7: "Thing Kickout", 8: "Lockup Kickout",
	9: "Upper Left Jet", 10: "Upper Right Jet", 11: "Center Left Jet", 12: "Center Right Jet", 13: "Lower Jet",
	14: "Left Slingshot", 15: "Right Slingshot", 16: "Left Magnet",
	17: "Telephone/Upper Right Ramp Flasher", 18: "Train/Upper Left Ramp Flasher",
	19: "Lower Ramp/Jet Bumpers Flasher", 20: "Left Lightning Bolt/Mini Flipper Flasher",
	21: "Right Lightning Bolt/Swamp Flasher", 22: "The Power/Backbox Cloud Flasher",
	23: "Upper Magnet", 24: "Right Magnet", 25: "Thing Motor", 26: "Thing Eject Hole",
	27: "Bookcase Motor", 28: "Swamp Release",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC GameOn GI Register Bit A", 30: "WPC GameOn GI Register Bit B", 31: "WPC GameOn GI Register Bit C",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Address 37", 38: "Unused WPC-Fliptronic Address 38",
	39: "Unused WPC-Fliptronic Address 39", 40: "Unused WPC-Fliptronic Address 40",
	41: "Unused WPC-Fliptronic Address 41", 42: "Unused WPC-Fliptronic Address 42",
	43: "Unused WPC-Fliptronic Address 43", 44: "Unused WPC-Fliptronic Address 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}

SOLENOID_WIRING = {
	1: dict(wire="Vio-Brn", connection="J130-1", driver_transistor="Q82", part_number="AE-26-1200", printed_type="High Power"),
	2: dict(wire="Vio-Red", connection="J132-2", driver_transistor="Q80", part_number="AE-23-800", printed_type="High Power"),
	3: dict(wire="Vio-Orn", connection="J130-4", driver_transistor="Q78", part_number="AE-26-1500", printed_type="High Power"),
	4: dict(wire="Vio-Yel", connection="J130-5", driver_transistor="Q76", part_number="AE-26-1200", printed_type="High Power"),
	5: dict(wire="Vio-Grn", connection="J130-6", driver_transistor="Q64", part_number="AE-27-1200", printed_type="High Power"),
	6: dict(wire="Vio-Blu", connection="J130-7", driver_transistor="Q66", part_number="A-12158-1", printed_type="High Power"),
	7: dict(wire="Vio-Blk", connection="J130-8", driver_transistor="Q68", part_number="AE-23-800", printed_type="High Power"),
	8: dict(wire="Vio-Gry", connection="J130-9", driver_transistor="Q70", part_number="AE-26-1200", printed_type="High Power"),
	9: dict(wire="Brn-Blk", connection="J127-1", driver_transistor="Q58", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(wire="Brn-Red", connection="J127-3", driver_transistor="Q56", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(wire="Brn-Org", connection="J127-4", driver_transistor="Q54", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(wire="Brn-Yel", connection="J127-5", driver_transistor="Q52", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(wire="Brn-Grn", connection="J127-6", driver_transistor="Q50", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(wire="Brn-Blu", connection="J127-7", driver_transistor="Q48", part_number="AE-27-1200", printed_type="Low Power"),
	15: dict(wire="Brn-Vio", connection="J127-8", driver_transistor="Q46", part_number="AE-27-1200", printed_type="Low Power"),
	16: dict(wire="Brn-Gry", connection="J127-9", driver_transistor="Q44", part_number="20-9247 12V", printed_type="Low Power"),
	17: dict(wire="Blk-Brn", connection="J126-1 / J125-1", driver_transistor="Q42", part_number="#906", printed_type="Flasher"),
	18: dict(wire="Blk-Red", connection="J126-2 / J125-2", driver_transistor="Q40", part_number="#906", printed_type="Flasher"),
	19: dict(wire="Blk-Org", connection="J126-3 / J125-3", driver_transistor="Q38", part_number="#906", printed_type="Flasher"),
	20: dict(wire="Blk-Yel", connection="J126-4 / J125-5", driver_transistor="Q36", part_number="#906", printed_type="Flasher"),
	21: dict(wire="Blu-Grn", connection="J126-5 / J125-6", driver_transistor="Q28", part_number="#906", printed_type="Flasher"),
	22: dict(wire="Blu-Blk", connection="J126-6 / J125-7", driver_transistor="Q30", part_number="#906", printed_type="Flasher"),
	23: dict(wire="Blu-Vio", connection="J126-7 / J125-8", driver_transistor="Q34", part_number="20-9247 12V", printed_type="Low Power"),
	24: dict(wire="Blu-Gry", connection="J126-8 / J125-9", driver_transistor="Q32", part_number="20-9247 12V", printed_type="Low Power"),
	25: dict(wire="Blu-Brn", connection="J122-1", driver_transistor="Q26", part_number="14-7966 12V", printed_type="Flasher-column motor"),
	26: dict(wire="Blu-Red", connection="J122-2", driver_transistor="Q24", part_number="AE-30-2000", printed_type="Flasher-column kicker"),
	27: dict(wire="Blu-Org", connection="J122-3", driver_transistor="Q22", part_number="14-7969 12V", printed_type="Flasher-column motor"),
	28: dict(wire="Blu-Yel", connection="J122-4", driver_transistor="Q20", part_number="AE-30-2000", printed_type="Flasher-column kicker"),
	33: dict(wire="Blu-Yel", connection="J109-7", part_number="FL-11630", printed_type="Fliptronic power"),
	34: dict(wire="Blu-Yel", connection="J109-7", part_number="FL-11630", printed_type="Fliptronic hold"),
	35: dict(wire="Gry-Yel", connection="J109-5", part_number="FL-11753", printed_type="Fliptronic power"),
	36: dict(wire="Gry-Yel", connection="J109-5", part_number="FL-11753", printed_type="Fliptronic hold"),
	45: dict(wire="Blu-Yel", connection="J109-7", part_number="FL-15411", printed_type="Fliptronic power"),
	46: dict(wire="Blu-Yel", connection="J109-7", part_number="FL-15411", printed_type="Fliptronic hold"),
	47: dict(wire="Gry-Yel", connection="J109-5", part_number="FL-15411", printed_type="Fliptronic power"),
	48: dict(wire="Gry-Yel", connection="J109-5", part_number="FL-15411", printed_type="Fliptronic hold"),
}
# Retained VPX script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "Chair (ChairKicker.TimerEnabled)", 2: "Knocker", 3: "DivertRamp (Diverter.RotateToEnd/Start)",
	4: "BallKick (BallRelease.KickZ)", 5: "Outhole (via Drain_Hit/Outhole.enabled)",
	6: "ThingMagnet (ThingSaucer.KickZ)", 7: "ThingKickout (ThingKickOutKicker.Kick)",
	8: "LockupKickout (SwampLockUp.TimerEnabled)",
	9: "Bumper1_Hit (vpmTimer.PulseSw 31)", 10: "Bumper2_Hit (vpmTimer.PulseSw 32)",
	11: "Bumper3_Hit (vpmTimer.PulseSw 33)", 12: "Bumper4_Hit (vpmTimer.PulseSw 34)", 13: "Bumper5_Hit (vpmTimer.PulseSw 35)",
	14: "LeftSlingShot_Slingshot (vpmTimer.pulsesw 36)", 15: "RightSlingShot_Slingshot (vpmTimer.pulsesw 37)",
	16: "cvpmMagnet LeftMagnet (InitMagnet LMagnet, .solenoid = 16)",
	17: "TelephoneFlasher", 18: "TrainFlasher", 19: "LowerRampFlasher",
	20: "LlightningBoltFlasher", 21: "RlightningBoltFlasher", 22: "ThePowerFlasher",
	23: "cvpmMagnet UpperMagnet (InitMagnet UMagnet, .solenoid = 23)",
	24: "cvpmMagnet RightMagnet (InitMagnet RMagnet, .solenoid = 24)",
	25: "ThingMotor (mechanism callback; rotates Thing/handMAGNET/thingBox)",
	26: "ThingEjectHole (ThingSaucer.KickZ)",
	27: "BookCaseMotor (mechanism callback; rotates vault_base/vault_*)",
	28: "SwampRelease (SwampReleaseKicker.TimerEnabled)",
	33: "SolURFlipper (rotates Flipper1)", 34: "SolURFlipper (rotates Flipper1)",
	35: "SolULFlipper (rotates Flipper2)", 36: "SolULFlipper (rotates Flipper2)",
	45: "SolRFlipper (rotates RightFlipper)", 46: "SolRFlipper (rotates RightFlipper)",
	47: "SolLFlipper (rotates LeftFlipper)", 48: "SolLFlipper (rotates LeftFlipper)",
}
FLASHER_LIGHT_OBJECTS = {
	17: ["Light18", "Light5"],
	18: ["Light3", "Light3c", "Light35"],
	19: ["Light12", "Light24", "Light24b"],
	20: ["LLightning", "LLightningb", "Light13c", "Light15", "Light25"],
	21: ["RLightning", "RLightningb", "Light6"],
	22: ["ThePower", "ThePowerb"],
}

# --- Printed lamp matrix (Operator's Handbook printed page 7). First digit is the column.
LAMP_LABELS = {
	11: "Thing Multiball", 12: "Extra Ball", 13: "Jackpot", 14: 'Grave "A"', 15: "Stars",
	16: "Super Jackpot", 17: 'Grave "V"', 18: "Upper Swamp Million",
	21: "Upper Left Jet", 22: "Upper Right Jet", 23: "Center Left Jet", 24: "Center Right Jet",
	25: "Lower Jet", 26: "Cousin It", 27: "2 Bear Kicks", 28: "Thing Flips",
	31: 'G-R-E-E-D "G"', 32: 'G-R-E-E-D "R"', 33: 'G-R-E-E-D "E"-1', 34: 'G-R-E-E-D "E"-2',
	35: 'G-R-E-E-D "D"', 36: "5X Graveyard", 37: "Center Swamp Million", 38: "Lower Swamp Million",
	42: "Advance X", 43: 'Grave "G"', 44: 'Grave "R"', 45: "The Mamushku", 46: "Swamp Lock",
	47: "Electric Chair Red", 48: 'Grave "E"',
	51: "Thing", 52: "Raise The Dead", 53: "Lite Extra Ball", 54: "House 6 Million",
	55: "Quick Multiball", 56: "Fester's Tunnel Hunt", 57: "House Seance", 58: "Hit Cousin It",
	61: "Left Special", 62: "Lite Thing Flips", 63: "Lite 2 Bear Kicks", 64: "Electric Chair Yellow",
	65: 'House "?"', 66: "House 9 Million", 67: "Graveyard At Max", 68: "House 3 Million",
	71: "Lite Advance X", 72: "Right Special", 73: "Shoot Again", 74: "Vault Green",
	75: "Vault Red", 77: "Thing Yellow", 78: "Thing Green",
	81: '"Thing" (star 1)', 82: '"Thing" "T"', 83: '"Thing" "H"', 84: '"Thing" "I"',
	85: '"Thing" "N"', 86: '"Thing" "G"', 87: '"Thing" (star 2)', 88: "Credit Button",
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

# --- Normalized playfield coordinates derived from the retained VPX extraction
# (x/952.965, y/2164.76); see review-artifacts/the-addams-family-1992/vpx-geometry.txt.
SWITCH_POSITIONS = {
	15: [(0.768016, 0.889057)], 16: [(0.822636, 0.877220)], 17: [(0.875221, 0.864668)], 18: [(0.532209, 0.945011)],
	25: [(0.802269, 0.737602)], 26: [(0.876733, 0.752127)], 27: [(0.946435, 0.884874)],
	31: [(0.080870, 0.350382)], 32: [(0.287630, 0.360883)], 33: [(0.147905, 0.436595)],
	34: [(0.353365, 0.447142)], 35: [(0.201791, 0.517748)],
	36: [(0.284486, 0.731861)], 37: [(0.712021, 0.734633)], 38: [(0.145582, 0.062502)],
	41: [(0.208960, 0.567603)], 42: [(0.268314, 0.555149)], 43: [(0.393380, 0.524971)],
	44: [(0.410921, 0.409696), (0.429220, 0.464520), (0.407507, 0.390292), (0.419829, 0.428275)],
	45: [(0.756738, 0.554864)], 47: [(0.775826, 0.533600)], 48: [(0.820621, 0.479513)],
	51: [(0.937748, 0.543127)],
	53: [(0.671766, 0.316946)], 54: [(0.699932, 0.320449)], 55: [(0.730484, 0.323798)], 56: [(0.760205, 0.327478)],
	57: [(0.118866, 0.566634)], 58: [(0.815335, 0.653082)],
	61: [(0.281173, 0.294738)], 62: [(0.217015, 0.107305)], 63: [(0.472610, 0.102363)], 64: [(0.568012, 0.224237)],
	65: [(0.127909, 0.063571)], 66: [(0.067643, 0.172669)], 67: [(0.549601, 0.065510)], 68: [(0.807968, 0.220256)],
	71: [(0.854371, 0.570083)], 72: [(0.831307, 0.605648)], 73: [(0.812176, 0.618820)], 74: [(0.759503, 0.609147)],
	75: [(0.059151, 0.748106)], 76: [(0.192840, 0.723691)], 77: [(0.955526, 0.108429)], 78: [(0.126673, 0.723460)],
	86: [(0.502819, 0.262116)], 87: [(0.678051, 0.158279)],
}
# Documented mechanism-position projections (not centroids of other devices): 81/82 onto the
# Bookcase assembly's own retained primitive (vault_base); 84/85 onto the Thing hand assembly's own
# retained primitive (Thing). PinMAME synthesizes these four switches purely from taf_handleMech's
# internal position counters; the retained script never calls Controller.Switch on any of them.
SWITCH_PROJECTIONS = {
	81: "Projected onto the Bookcase assembly (A-14970, retained primitive vault_base center): taf_handleMech sets swBookOpen/swBookClose from locals.bookPos alone (a 0-199 tick motor-position counter incremented while solenoid 27 is asserted), and the retained VPX script never calls Controller.Switch(81); it only reads mechanism position via Controller.GetMech to rotate the visible vault_base/vault_* assembly.",
	82: "Projected onto the Bookcase assembly (A-14970, retained primitive vault_base center); see switch 81.",
	84: "Projected onto the Thing hand assembly (A-14711 Hand Drive Assembly, retained primitive Thing center): taf_handleMech sets swThingDn/swThingUp from locals.thingPos alone (a 0-399 tick motor-position counter incremented while solenoid 25 is asserted), and the retained VPX script never calls Controller.Switch(84); it only reads mechanism position via Controller.GetMech to rotate the visible Thing/handMAGNET/thingBox assembly.",
	85: "Projected onto the Thing hand assembly (A-14711 Hand Drive Assembly, retained primitive Thing center); see switch 84.",
}

SOLENOID_POSITIONS = {
	1: [(0.393380, 0.524971)], 3: [(0.009688, 0.324926)], 4: [(0.875221, 0.864668)], 5: [(0.534068, 0.944550)],
	6: [(0.678051, 0.158279)], 7: [(0.955526, 0.108429)], 8: [(0.759503, 0.609147)],
	9: [(0.080870, 0.350382)], 10: [(0.287630, 0.360883)], 11: [(0.147905, 0.436595)],
	12: [(0.353365, 0.447142)], 13: [(0.201791, 0.517748)],
	14: [(0.284486, 0.731861)], 15: [(0.712021, 0.734633)], 16: [(0.395915, 0.647921)],
	17: [(0.903283, 0.149195), (0.596308, 0.066336)],
	18: [(0.199444, 0.081034), (0.202071, 0.080414), (0.053701, 0.049063)],
	19: [(0.145307, 0.310942), (0.260506, 0.419084), (0.260555, 0.422800)],
	20: [(0.398092, 0.601363), (0.395958, 0.596119), (0.055628, 0.568056), (0.055577, 0.566464), (0.054035, 0.568601)],
	21: [(0.600292, 0.599023), (0.598056, 0.595024), (0.868432, 0.605016)],
	22: [(0.497045, 0.627316), (0.498562, 0.624361)],
	23: [(0.503892, 0.567339)], 24: [(0.607614, 0.648680)],
	25: [(0.746292, 0.111334)], 26: [(0.678051, 0.158279)], 27: [(0.749526, 0.306757)], 28: [(0.812176, 0.618820)],
	33: [(0.864264, 0.399865)], 34: [(0.864264, 0.399865)], 35: [(0.076604, 0.600657)], 36: [(0.076604, 0.600657)],
	45: [(0.667413, 0.839356)], 46: [(0.667413, 0.839356)], 47: [(0.327417, 0.839356)], 48: [(0.327417, 0.839356)],
}
SOLENOID_PROJECTIONS = {
	25: "Projected onto the Thing hand assembly (A-14711 Hand Drive Assembly, retained primitive Thing center): ThingMotor(aNewPos,...) rotates Thing.RotY/handMAGNET.RotY/thingBox.Rotx directly from Controller.GetMech position, with no separate motor object in the retained table.",
	27: "Projected onto the Bookcase assembly (A-14970, retained primitive vault_base center): BookCaseMotor(aNewPos,...) rotates vault_base.rotZ (and the sibling vault_* parts) directly from Controller.GetMech position, with no separate motor object in the retained table.",
}

LAMP_POSITIONS = {
	11: [(0.420933, 0.213342)], 12: [(0.430050, 0.251946)], 13: [(0.442655, 0.295400)], 14: [(0.500776, 0.287372)],
	15: [(0.400271, 0.328554)], 16: [(0.483703, 0.348946)], 17: [(0.540003, 0.370590)], 18: [(0.740890, 0.494243)],
	21: [(0.081035, 0.350873)], 22: [(0.288809, 0.360560)], 23: [(0.356624, 0.448536)], 24: [(0.150607, 0.441540)],
	25: [(0.198512, 0.514860)], 26: [(0.472387, 0.411888)], 27: [(0.529166, 0.414460)], 28: [(0.515362, 0.454203)],
	31: [(0.607048, 0.382828)], 32: [(0.628088, 0.404429)], 33: [(0.648392, 0.425357)], 34: [(0.671251, 0.445843)],
	35: [(0.689791, 0.465393)], 36: [(0.673508, 0.522421)], 37: [(0.700303, 0.538549)], 38: [(0.679826, 0.560072)],
	42: [(0.323345, 0.538968)], 43: [(0.257225, 0.609204)], 44: [(0.297257, 0.587697)],
	45: [(0.624846, 0.798709)], 46: [(0.592783, 0.535828)], 47: [(0.452741, 0.496669)], 48: [(0.680447, 0.600384)],
	51: [(0.435328, 0.723380)], 52: [(0.495638, 0.719451)], 53: [(0.558182, 0.720952)], 54: [(0.372828, 0.757130)],
	55: [(0.435620, 0.757527)], 56: [(0.498430, 0.758184)], 57: [(0.559500, 0.758039)], 58: [(0.557130, 0.796254)],
	61: [(0.058926, 0.706648)], 62: [(0.128176, 0.679938)], 63: [(0.191785, 0.677816)], 64: [(0.327948, 0.495596)],
	65: [(0.495912, 0.677789)], 66: [(0.373104, 0.722815)], 67: [(0.435058, 0.796891)], 68: [(0.372264, 0.796508)],
	71: [(0.803046, 0.690315)], 72: [(0.878624, 0.707679)], 73: [(0.496642, 0.870405)], 74: [(0.757221, 0.231583)],
	75: [(0.756602, 0.231583)], 77: [(0.364397, 0.125649)], 78: [(0.412777, 0.125820)],
	# 81-87: raw normalized y is slightly negative (-0.029..-0.029), just beyond the table's own
	# top=0 edge, matching the manual's Lamp Locations diagram drawing these seven "THING" name-chase
	# inserts in a row above the cabinet outline (a header strip mounted above the play surface).
	# Clamped to the schema-valid boundary y=0.000000; see vpx-geometry.txt for the raw offsets.
	81: [(0.685100, 0.000000)], 82: [(0.710075, 0.000000)], 83: [(0.733456, 0.000000)], 84: [(0.757833, 0.000000)],
	85: [(0.783004, 0.000000)], 86: [(0.806122, 0.000000)], 87: [(0.830433, 0.000000)],
}
LAMP_NOTES = {
	45: (
		"The retained table has two candidate bulb objects at this insert, L45old (x=0.620718 "
		"y=0.797016) and L45bold (x=0.624846 y=0.798709, used here), roughly a bulb diameter apart; "
		"there is no plain \"L45\" object and neither name is referenced anywhere in script.vbs, so "
		"binding relies on VPinMAME's default name-prefix lamp matching rather than an explicit Sub. "
		"L45bold is treated as the current art revision and L45old as a superseded duplicate, "
		"consistent with this table's general pattern of stacking a second co-located Light object at "
		"every lamp address purely for rendering."
	),
}

GI_POSITIONS = {
	0: [
		(0.031398, 0.630616), (0.289265, 0.772326), (0.208699, 0.087164), (0.392345, 0.531989),
		(0.139574, 0.787142), (0.203375, 0.806706), (0.264427, 0.826142),
	],
	4: [
		(0.713202, 0.763337), (0.790885, 0.798621), (0.734294, 0.816670), (0.878497, 0.438714),
	],
}
GI_LABELS = {
	0: "Left Playfield String", 1: "Insert House String", 2: "Insert People String",
	3: "Not Used", 4: "Right Playfield String",
}
GI_WIRING = {
	0: ("Brown", "J120-1", "Q18", "#44"), 1: ("Orange", "J120-2", "Q10", "#555"),
	2: ("Yellow", "J120-3", "Q14", "#555"), 3: ("Green", "J121-5", "Q16", None),
	4: ("Violet", "J121-6", "Q12", "#44"),
}

FLIPPER_INPUTS = {
	111: ("Right Flipper End of Stroke", "internal.flipper.lower.right.eos", False, "leaf", "SW-1A-193"),
	112: ("Right Flipper Button", "flipper.lower.right.button", True, "leaf", None),
	113: ("Left Flipper End of Stroke", "internal.flipper.lower.left.eos", False, "leaf", "SW-1A-193"),
	114: ("Left Flipper Button", "flipper.lower.left.button", True, "leaf", None),
	115: ("Upper Right Flipper End of Stroke", "internal.flipper.upper.right.eos", False, "leaf", "SW-1A-193"),
	116: ("Upper Right Flipper Button", "flipper.upper.right.button", True, "leaf", None),
	117: ("Upper Left Flipper End of Stroke", "internal.flipper.upper.left.eos", False, "leaf", "SW-1A-193"),
	118: ("Upper Left Flipper Button", "flipper.upper.left.button", True, "leaf", None),
}
FLIPPER_POSITIONS = {
	111: (0.667413, 0.839356), 112: (0.667413, 0.839356),
	113: (0.327417, 0.839356), 114: (0.327417, 0.839356),
	115: (0.864264, 0.399865), 116: (0.864264, 0.399865),
	117: (0.076604, 0.600657), 118: (0.076604, 0.600657),
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Addams Family retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Addams Family extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Addams Family retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Addams Family retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Addams Family retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the taf_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/taf.c tafGameData GEN_WPCFLIPTRON with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x00,0x00,0x7c,0x00,0x00,0x18,0x00,0x00,0x00}, "
				"FLIP_BUT(FLIP_L)|FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U), swStart/swTilt/swSlamTilt/"
				"swCoinDoor/swBuyIn defines, taf_handleMech (locals.bookPos 0-199 driving swBookOpen/swBookClose, "
				"locals.thingPos 0-399 driving swThingDn/swThingUp), taf_stateDef's stTFlip case (the only runtime "
				"reference to any upper-flipper solenoid, core_getSol(sULFlip), confirming the AI-only upper-left "
				"'Thing' flip path), and CORE_GAMEDEF/CORE_CLONEDEF driver table with ROM/SYS revision comments; "
				"src/wpc/core.h WPC solenoid numbering, CORE_FIRSTUFLIPSOL=33/CORE_FIRSTLFLIPSOL=45, and WPC_swF1..F8; "
				"src/wpc/wpc.c 'check flippers we have' FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) gating; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCFLIPTRON=0x8"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-fliptronic.json",
			"revision": "repository",
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules, reused unchanged from Twilight Zone's curation",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.the-addams-family.1992/ipdb/Bally_1992_The_Addams_Family_Operations_Manual_January_1992_includes_schematics_OCR_searchable.pdf",
			"original_filename": "Bally_1992_The_Addams_Family_Operations_Manual_January_1992_includes_schematics_OCR_searchable.pdf",
			"sha256": OPS_MANUAL_SHA256,
			"locator": (
				"124-page Bally/Midway Operations Manual (part 16-20017-101, January 1992) with an OCR text layer; "
				"cover verified visually as the physical 1992 Bally machine, not the 1994 Williams Gold reissue. "
				"Printed page 2-39 carries the authoritative Switch Locations parts list (assembly/switch part "
				"numbers); other printed pages carry the illustrated Flipper Assembly parts breakdowns (upper-left "
				"A-15205-L-1, upper-right A-15205-R, lower A-15205-L-4/A-15205-R), the 'Thing Flips' automatic-"
				"calibration rules text, and Section 3 schematics."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company, manufacturers of Bally amusement games",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.addams-family.switch-locations",
					"locator": "Printed page 2-39, Switch Locations parts list, plus the opto-determination sweep and PinMAME mask cross-check",
					"path": "evidence/excerpts/bally.the-addams-family.1992/switch-locations.md",
					"sha256": "209b9687e06ae02a77985afe62201d6e47a66e7008bc37ed3d88300f7d7e47c8",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.addams-family.flipper-assembly-and-thing-flips",
					"locator": "Printed pages ~2-74 (Flipper Assembly Notes), 6 ('Thing Flips' Automatic Calibration), and ~2-14 (ball-path narrative)",
					"path": "evidence/excerpts/bally.the-addams-family.1992/flipper-assembly-and-thing-flips.md",
					"sha256": "928346368bc49fb0599dee35c65ba6b0afa75b2668f433f9f10cb9a76ea8799c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_HANDBOOK_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.the-addams-family.1992/ipdb/Bally_1992_The_Addams_Family_Operator_s_Handbook_January_1991_OCR_searchable_has_lamp_and_switch_matrices.pdf",
			"original_filename": "Bally_1992_The_Addams_Family_Operator_s_Handbook_January_1991_OCR_searchable_has_lamp_and_switch_matrices.pdf",
			"sha256": HANDBOOK_SHA256,
			"locator": (
				"12-page Operator's Handbook (part 16-20017-103, January 1991) with an OCR text layer; carries the "
				"Solenoid Table (printed p.5), Lamp Matrix (p.7), and Switch Matrix wiring (p.9-10) used for column/"
				"row wire colors and connectors."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company, manufacturers of Bally amusement games",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.addams-family.solenoid-flasher-table",
					"locator": "Printed page 5, Solenoid Table and Flipper Coils list",
					"path": "evidence/excerpts/bally.the-addams-family.1992/solenoid-flasher-table.md",
					"sha256": "2f21364f1a5bf2d855e73733ffa23914540cdbf9bf328d33fa2e8bf369357281",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.addams-family.general-illumination",
					"locator": "Printed page 5, General Illumination Circuits",
					"path": "evidence/excerpts/bally.the-addams-family.1992/general-illumination.md",
					"sha256": "b9dc0b005514a8b67f487ea945434901f6a472f0872f006e89fb17fb43314798",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.addams-family.lamp-matrix",
					"locator": "Printed page 7, Lamp Matrix",
					"path": "evidence/excerpts/bally.the-addams-family.1992/lamp-matrix.md",
					"sha256": "1de81d75364e7a724854b8ada4835bbca7f5a27241ad827d40310fe22fb7c3b4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.addams-family.switch-matrix",
					"locator": "Printed pages 9-10, Switch Matrix wiring",
					"path": "evidence/excerpts/bally.the-addams-family.1992/switch-matrix.md",
					"sha256": "6b53246ded9ff9bfd3890177efdc5f12bd95e47d9b6525974f736196d63aecfc",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SCHEMATIC_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.the-addams-family.1992/ipdb/Bally_1992_The_Addams_Family_WPC_Schematic_Manual_January_1992_OCR_searchable.pdf",
			"original_filename": "Bally_1992_The_Addams_Family_WPC_Schematic_Manual_January_1992_OCR_searchable.pdf",
			"sha256": SCHEMATIC_SHA256,
			"locator": "14-page WPC Schematic Manual (part 16-20017-102A, January 1992); identity-checked only (cover confirms the same 16-20017 part-number family).",
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company, manufacturers of Bally amusement games",
			"rights": "NOASSERTION",
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/the-addams-family-1992/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition (the OCR text "
				"layer is a search aid only and is not authoritative for any mapping decision), together with the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/bally.the-addams-family.1992/ and "
				"the full retained-table geometry dump at "
				"external:pinmame-review-artifacts/the-addams-family-1992/vpx-geometry.txt."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/the-addams-family-1992/source/The%20Addams%20Family%20%28Bally1992%29%20v2.3.2%20%28g5k%29.vpx",
			"original_filename": "The Addams Family (Bally1992) v2.3.2 (g5k).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working v2.3.2 recreation of the physical machine by g5k, Sliderpoint and 3rdaxis, "
				f"released January 2022 (table save revision 9, table_version 2.3.1). Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952.965 and y/2164.76. Geometry authority only for "
				"named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "g5k, Sliderpoint and 3rdaxis",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/the-addams-family-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (92,132 bytes). Runtime and mechanism-causality authority: cGameName = '
				'"TAF_L7", Const UseSolenoids = 2 (fast flips), Const UseSync = 0; the SolCallback/SolModCallback '
				"table for solenoids 1-28 plus core.vbs sLRFlipper/sLLFlipper/sURFlipper/sULFlipper; explicit "
				"Controller.Switch calls for most matrix switches, vpmTimer.PulseSw for opto/rollover switches, and "
				"the cvpmMagnet class instances (LeftMagnet/UpperMagnet/RightMagnet) bound to solenoids 16/23/24; "
				"the BookCaseMotor and ThingMotor mechanism callbacks that read Controller.GetMech and never touch "
				"Controller.Switch(81/82/84/85) directly; UpdateGI mapping GI Case 0/4 to the GILeftString/"
				"GIRightString playfield emitter collections with no Case block for GI 1/2/3."
			),
			"license": "NOASSERTION",
			"attribution": "g5k, Sliderpoint and 3rdaxis",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/the-addams-family-1992/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=20",
			"locator": (
				"IPDB machine #20, 'The Addams Family' (Bally, 1992). IPDB itself returned HTTP 403 (Cloudflare) in "
				"this session; identity was independently cross-checked via the Open Pinball Database mirror "
				"(https://opdb.org/machines/170), which lists manufacturer Bally, date January 1992, cites "
				"'IPDB no. 20', and separately lists 'The Addams Family Gold (Bally, 1994)' (IPDB #21) as the "
				"related but distinct machine-group entry."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors",
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
		"board": "WPC CPU board",
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
				(MANUAL_HANDBOOK_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_HANDBOOK_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			assembly, part_number = SWITCH_PARTS.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			elif not unused:
				physical["switch_type"] = "leaf"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if address == 23:
				notes += (
					' Printed switch-locations item 23 reads "*Ticket Opto." in the description column, but both '
					'the Switch Number and Switch Assy columns read blank/"Not Used" -- unlike the seven genuinely '
					"fitted optos below, no opto assembly part number is printed here, so this position is "
					"enumerated but not physically installed."
				)
			elif unused:
				notes += " The printed Switch Locations parts list and the Switch Matrix wiring page both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					' Printed with a blank Switch Number and a populated opto-pair assembly part number under the '
					'"Switch Assy." column, with "Opto" in the description -- the same signature used across the '
					"whole parts list to mark an opto interrupter. tafGameData's inverted-switch mask "
					"({0x00,0x00,0x00,0x00,0x00,0x7c,0x00,0x00,0x18,0x00,0x00,0x00}) covers exactly this column/row "
					"pair (column 5 bits 2-6 = 53-57, column 8 bits 3-4 = 84-85), so the public switch state is "
					"already normalized by the emulator and must not be inverted again; physical.normally_closed "
					"records the real hardware sense separately. Full agreement between the manual and PinMAME here "
					"-- no conflict."
				)
			if address == 34:
				notes += (
					' The Operator\'s Handbook Switch Matrix page (printed p.9-10) renders this cell identically to '
					'row 3 ("Center Left Jet"), but the Operations Manual\'s Switch Locations parts list (2-39) '
					'names item 34 "Center Right Jet", and the retained script\'s own comment on Bumper4_Hit (the '
					"handler that pulses switch 34) reads the same: vpmTimer.PulseSw 34 'Center Right Jet'. Two "
					"independent sources against one page reading resolve this as Center Right Jet, matching the "
					"natural Upper-Left/Upper-Right/Center-Left/Center-Right/Lower naming of the five-bumper "
					"cluster."
				)
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if address == 44:
				notes += (
					" Public switch 44 is shared by four standup targets (44a1, 44a2, 44b1, 44b2) on one 'Cousin "
					"It' figure, all pulsed to the same address by the retained script; the printed parts list "
					'marks this "Cousin It (2)" / "(2)" across two item rows (44a, 44b) totaling four targets.'
				)
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, MANUAL_HANDBOOK_SOURCE, CONTROLLER_SOURCE)
				label = f"Not Used Matrix Position {address}"
			elif address == 23:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE)
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address == 13 else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				elif address in SWITCH_PROJECTIONS:
					extra["roles"] = ["internal.mechanism-position"]
					extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address == 34 else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	for address, (label, role, is_button, switch_type, part_number) in FLIPPER_INPUTS.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if is_button else "flipper assembly", "switch_type": switch_type}
		if part_number:
			physical["part_number"] = part_number
		notes = f"Printed Fliptronic grounded switch F{address - 110}. Printed as a plain (non-opto) leaf end-of-stroke/button, not shaded as an opto anywhere in this manual."
		if address in (115, 116, 117, 118):
			notes += (
				" Confirmed fitted (not a repurposed or unfitted position like Monster Bash's upper-right Fliptronic "
				"block): tafGameData sets both FLIP_SW(FLIP_U) and FLIP_SOL(FLIP_U), the Operations Manual prints a "
				"full illustrated parts breakdown for both A-15205-R (Upper Right) and A-15205-L-1 (Upper Left) "
				"flipper assemblies with real EOS switch and coil part numbers, and the retained script wires both "
				"SolURFlipper and SolULFlipper to independently animated table objects."
			)
		physical["notes"] = notes
		extra = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
			"normally_closed": False,
		}
		if is_button:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_HANDBOOK_SOURCE)
		else:
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_HANDBOOK_SOURCE)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_HANDBOOK_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
				**extra,
			)
		)

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				f"CPU DIP {address} (country/option configuration bit)",
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used",
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={
					"location": "WPC CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC country/option configuration DIP bank. The retained transcription of this manual does "
						"not include a per-country switch-combination chart, so no specific ON/OFF combination is "
						"asserted here."
					),
				},
				spatial=not_applicable("dip_switch", CORE_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	flipper_kinds = {33, 34, 35, 36, 45, 46, 47, 48}
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			if address in flipper_kinds:
				kind = "coil"
			elif 17 <= address <= 22:
				kind = "flasher"
			elif address in {25, 27}:
				kind = "motor"
			elif address in {16, 23, 24}:
				kind = "magnet"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid table entry {address:02d} ({printed_type})."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if kind == "flasher":
				lights = FLASHER_LIGHT_OBJECTS.get(address, [])
				physical["quantity"] = len(lights)
				notes += f" Retained flasher bulb objects: {', '.join(lights)}."
			if address in {25, 27}:
				notes += " " + SOLENOID_PROJECTIONS[address]
			if address in flipper_kinds:
				side = "upper right" if address in (33, 34) else "upper left (\"Thing\")" if address in (35, 36) else "lower right" if address in (45, 46) else "lower left"
				notes += f" Fliptronic {side} flipper circuit; printed flipper table below the GI block, no printed solenoid number."
				if address in (35, 36):
					notes += (
						" This is THING'S MINI-FLIPPER: the Operations Manual's 'Thing Flips' automatic-calibration "
						"section describes it as an AI-aimed automatic flip (not simply mirroring the left player "
						"button), and taf_stateDef's stTFlip case is the only place any upper-flipper solenoid is "
						"read in the driver's own ball-routing logic (core_getSol(sULFlip))."
					)
				if address in (33, 34):
					notes += (
						" Documented here as ordinary Fliptronic flipper hardware (own EOS/button pair, own coil "
						"FL-11630); this project has not independently confirmed from static sources alone whether "
						"the ROM ties its firing unconditionally to the right flip button or gates it further, which "
						"is not required to recreate the physical device correctly."
					)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC power driver board", "control_wire": wiring_data["wire"]}
			if "connection" in wiring_data:
				wiring["control_connection"] = wiring_data["connection"]
			if "driver_transistor" in wiring_data:
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in {33, 34, 35, 36, 45, 46, 47, 48}:
				printed = {33: "33", 34: "34", 35: "35", 36: "36", 45: "29", 46: "30", 47: "31", 48: "32"}[address]
				aliases.append({"namespace": "manual.address", "value": printed})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			availability = "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 2:
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_HANDBOOK_SOURCE)
			else:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_HANDBOOK_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		notes = {
			29: "PinMAME publishes one of the three highest bits of the WPC GameOn/GI register here; not a TAF playfield device.",
			30: "PinMAME publishes the second of the three GameOn/GI register bits here; not a TAF playfield device.",
			31: "PinMAME publishes the third of the three GameOn/GI register bits here; not a TAF playfield device.",
			32: "PinMAME reports this WPC state channel as always zero.",
			37: "Unused address space on this generation: unlike WPC-95, WPC-Fliptronic has no integrated LPDC board, and pinned PinMAME's core_getSol dispatch only serves the 37-44 branch for GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11, so this address is simply unclaimed here.",
			38: "Unused address space on this generation; see 37.",
			39: "Unused address space on this generation; see 37.",
			40: "Unused address space on this generation; see 37.",
			41: "Unused address space on this generation; see 37.",
			42: "Unused address space on this generation; see 37.",
			43: "Unused address space on this generation; see 37.",
			44: "Unused address space on this generation; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; no WPC hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. tafGameData declares custSol = 0, so this machine claims no custom solenoids at all.",
		}[address]
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				"unused",
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=["internal.wpc-state" if address in {29, 30, 31, 32} else "internal.unused.wpc-output"],
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
			label = LAMP_LABELS.get(address)
			unused = label is None
			identifier = f"lamp.matrix-{address}"
			physical: dict[str, Any] = {"quantity": 1}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if address in LAMP_NOTES:
				notes += " " + LAMP_NOTES[address]
			if address in {87, 88}:
				notes += ' Cabinet apron lamp ("Thing" name-chase star / Credit Button); no dedicated playfield Light object beyond the header row for 81-87.'
			if address in {81, 82, 83, 84, 85, 86, 87}:
				notes += (
					" This is one of the seven \"THING\" name-chase header lamps; the retained table places it at a "
					"small negative normalized y (just beyond the table's own top=0 edge), matching a plastic "
					"header strip drawn above the cabinet outline on the manual's Lamp Locations page. The "
					"placement below clamps y to 0.000000; the raw offset is disclosed in vpx-geometry.txt."
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
					"board": "WPC power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_HANDBOOK_SOURCE)
				label = f"Not Used Lamp Position {address}"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The printed lamp matrix marks this position Not Used."
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.credit-button"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_HANDBOOK_SOURCE)
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
					(MANUAL_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(5):
		label = GI_LABELS[address]
		identifier = f"gi.string-{address + 1}"
		wire, connection, transistor, bulb = GI_WIRING[address]
		notes = f"Printed general-illumination string {address + 1:02d} ({label})."
		if bulb:
			notes += f" Printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC power driver board",
				"control_connection": connection,
				"driver_transistor": transistor,
				"control_wire": wire,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter "
				"coordinate come from the retained table's UpdateGI handler: Case 0 drives collection "
				"GILeftString, Case 4 drives GIRightString. UpdateGI has no Case block for GI 1, 2, or 3."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
			availability = "used"
		elif address == 3:
			notes += " The manual itself prints this string \"Not Used\" (blank bulb-type column), matching UpdateGI's missing Case 3 block."
			extra["roles"] = ["internal.unused.gi-string"]
			extra["spatial"] = not_applicable("unused", MANUAL_HANDBOOK_SOURCE)
			availability = "unused"
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite; the retained script's UpdateGI handles "
				"only GI addresses 0 and 4, so this string has no playfield coordinate."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_HANDBOOK_SOURCE)
			availability = "used"
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(
			_device(
				identifier,
				label,
				"gi",
				"pinmame.output.gi",
				address,
				availability,
				(MANUAL_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
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
			"mechanism.bookcase",
			"Motorized rotating bookcase (Vault)",
			"motorized",
			[output_id("Bookcase Motor")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-53", "switch.matrix-54", "switch.matrix-55", "switch.matrix-56"],
			"Solenoid 27 drives a gearmotor that rotates the bookcase (Vault) assembly. taf_handleMech tracks the "
			"position with an internal 0-199 tick counter (locals.bookPos, incremented while solenoid 27 is "
			"asserted, wrapping at TAF_BOOKTICKS=200): swBookOpen (81) is asserted for bookPos < 15 and swBookClose "
			"(82) for 100 <= bookPos < 115, so there is no discrete playfield sensor for either state -- both are "
			"derived purely from motor position and PinMAME sets them internally (the retained script never calls "
			"Controller.Switch(81) or (82), only Controller.GetMech to animate vault_base/vault_plastic/vault_post/"
			"vault_screws/vault_upright rotation and swap the vault_base shadow image). Four bookcase-position "
			"optos (53-56, Bookcase Opto 1-4) are separate fixed playfield sensors near the loop habitrail, not "
			"part of the rotation counter, and calibrate ball detection around the bookcase rather than its own "
			"open/closed state.",
			[
				("open", "Bookcase open", ["switch.matrix-81"], "bookPos < 15 ticks."),
				("closed", "Bookcase closed", ["switch.matrix-82"], "100 <= bookPos < 115 ticks."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14970",
		),
		mechanism(
			"mechanism.thing-hand",
			"Motorized raising/lowering Thing hand",
			"motorized",
			[output_id("Thing Motor")],
			["switch.matrix-84", "switch.matrix-85"],
			"Solenoid 25 drives a gearmotor that raises and lowers 'The Thing' hand figure. taf_handleMech tracks "
			"the position with an internal 0-399 tick counter (locals.thingPos, incremented while solenoid 25 is "
			"asserted, wrapping at TAF_THINGTICKS=400): swThingDn (84) is asserted for thingPos < 15 and swThingUp "
			"(85) for 200 <= thingPos < 215, again derived purely from motor position rather than a discrete "
			"sensor -- the retained script never calls Controller.Switch(84) or (85), only Controller.GetMech to "
			"drive Thing.RotY, handMAGNET.RotY, and a non-linear thingBox.Rotx/ThingBOXmods.Rotx lookup table so "
			"the visible box lid tracks the hand's rise smoothly. This is a separate mechanism from the upper-left "
			"'Thing' mini-flipper (mechanism.upper-left-flipper): the hand rises out of a box to grab a captured "
			"ball (see mechanism.thing-saucer) while the mini-flipper is a distinct Fliptronic flipper elsewhere "
			"on the playfield.",
			[
				("down", "Thing hand down", ["switch.matrix-84"], "thingPos < 15 ticks."),
				("up", "Thing hand up", ["switch.matrix-85"], "200 <= thingPos < 215 ticks."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14711",
		),
		mechanism(
			"mechanism.chair-kickout",
			"Electric Chair kickout",
			"kicker",
			[output_id("Chair Kickout")],
			["switch.matrix-43"],
			"A ball resting on switch 43 (Chair Kickout) is kicked back to the playfield by solenoid 1 "
			"(ChairKicker.TimerEnabled in the retained script). Both the switch and the solenoid are printed "
			"'Chair Kickout' on their respective tables.",
			[("held", "Ball in the Chair kickout hole", ["switch.matrix-43"], "Chair Kickout switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14962",
		),
		mechanism(
			"mechanism.cabinet-knocker",
			"Cabinet knocker",
			"other",
			[output_id("Thing Knocker")],
			[],
			"Solenoid 2 (Thing Knocker) is a standard cabinet-mounted knocker that raps against the cabinet "
			"body on match/replay/special, themed in name only ('Thing Knocker') like every other Bally/Williams "
			"WPC knocker. It has no printed sensor switch and no playfield position.",
			[],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.thing-saucer",
			"Thing eject saucer, magnet grab, and kickout",
			"kicker",
			[output_id("Thing Magnet"), output_id("Thing Eject Hole")],
			["switch.matrix-87"],
			"A ball entering the Thing saucer closes switch 87 (Thing Eject Hole). Solenoid 6 (Thing Magnet) then "
			"energizes a magnet under the saucer so the Thing hand mechanism (mechanism.thing-hand) appears to "
			"grab the captured ball; solenoid 26 (Thing Eject Hole) kicks the ball back out. All three devices "
			"share the retained script's single ThingSaucer kicker object.",
			[("held", "Ball captured in the Thing saucer", ["switch.matrix-87"], "Thing Eject Hole switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15368",
		),
		mechanism(
			"mechanism.thing-kickout",
			"Thing kickout hole",
			"kicker",
			[output_id("Thing Kickout")],
			["switch.matrix-77"],
			"A ball resting on switch 77 (Thing Kickout) is kicked back to the playfield by solenoid 7.",
			[("held", "Ball in the Thing kickout hole", ["switch.matrix-77"], "Thing Kickout switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15200",
		),
		mechanism(
			"mechanism.swamp-lock",
			"Swamp lock (three-ball lock) and release",
			"kicker",
			[output_id("Lockup Kickout"), output_id("Swamp Release")],
			["switch.matrix-71", "switch.matrix-72", "switch.matrix-73", "switch.matrix-74"],
			"Balls lock in sequence at Swamp Lock Upper (71), Center (72), and Lower (73) as they travel down the "
			"Vault habitrail; SwampLockUp_Hit additionally drops Wall70 to hold a ball at the middle position and "
			"SwampReleaseKicker_Hit drops Wall69 to hold one at the lower position. Solenoid 28 (Swamp Release) "
			"releases locked balls into the Lockup Kickout hole (switch 74), and solenoid 8 (Lockup Kickout) then "
			"kicks the released ball back to the playfield.",
			[
				("upper", "Ball at Swamp Lock Upper", ["switch.matrix-71"], "Uppermost lock position."),
				("center", "Ball at Swamp Lock Center", ["switch.matrix-72"], "Middle lock position; Wall70 drops to hold the ball."),
				("lower", "Ball at Swamp Lock Lower", ["switch.matrix-73"], "Lowest lock position; Wall69 drops to hold the ball."),
				("kickout", "Ball at the Lockup Kickout hole", ["switch.matrix-74"], "Released balls collect here before solenoid 8 kicks them out."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14964",
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Center ramp diverter",
			"gate",
			[output_id("Ramp Diverter")],
			[],
			"Solenoid 3 rotates a diverter flap (Diverter) between the center ramp and the bumper lane, dropping a "
			"companion wall (DiverterWall) in step so a ball on the ramp is redirected into the jet bumper nest "
			"instead of continuing up the ramp. There is no dedicated printed switch for the diverter itself.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15040",
		),
		mechanism(
			"mechanism.trough-and-shooter",
			"Ball trough, outhole, and ball release",
			"kicker",
			[output_id("Ball Release"), output_id("Outhole")],
			["switch.matrix-15", "switch.matrix-16", "switch.matrix-17", "switch.matrix-18", "switch.matrix-27"],
			"Balls drain through the Outhole (18) into a three-position trough: Left Trough (15) nearest the "
			"drain, Center Trough (16), and Right Trough (17) at the ball-release position. Solenoid 5 kicks a "
			"ball resting on the outhole into the trough; solenoid 4 (Ball Release) kicks the ball resting at the "
			"trough's Right Trough position into the shooter lane, where it rests on switch 27 (Ball Shooter) "
			"until the player pulls the manual plunger.",
			[
				("left", "Left Trough", ["switch.matrix-15"], "Nearest the drain."),
				("center", "Center Trough", ["switch.matrix-16"], "Middle trough position."),
				("right", "Right Trough (release position)", ["switch.matrix-17"], "Ball Release kicks from here into the shooter lane."),
				("outhole", "Outhole", ["switch.matrix-18"], "Drain kicker feeding the trough."),
				("shooter", "Ball in shooter lane", ["switch.matrix-27"], "Awaiting the manual plunger."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Five-bumper jet nest",
			"other",
			[
				output_id("Upper Left Jet"), output_id("Upper Right Jet"), output_id("Center Left Jet"),
				output_id("Center Right Jet"), output_id("Lower Jet"),
			],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Five B-12030-2 jet bumpers. The retained script's Bumper1_Hit through Bumper5_Hit handlers pulse "
			"switches 31-35 and fire coils 9-13 respectively, matching printed Upper Left/Upper Right/Center Left/"
			"Center Right/Lower Jet (see switch 34's label note for how Center Right was resolved).",
			[
				("upper-left", "Upper Left Jet", ["switch.matrix-31"], "Bumper1."),
				("upper-right", "Upper Right Jet", ["switch.matrix-32"], "Bumper2."),
				("center-left", "Center Left Jet", ["switch.matrix-33"], "Bumper3."),
				("center-right", "Center Right Jet", ["switch.matrix-34"], "Bumper4."),
				("lower", "Lower Jet", ["switch.matrix-35"], "Bumper5."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="B-12030-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-36", "switch.matrix-37"],
			"The retained script's LeftSlingShot_Slingshot and RightSlingShot_Slingshot handlers pulse switches 36 "
			"and 37 and animate the sling rubber (sling1/sling2 TransX) in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-36"], "Left slingshot leaf switch."),
				("right", "Right slingshot", ["switch.matrix-37"], "Right slingshot leaf switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.magnets",
			"Left, upper, and right under-playfield magnets",
			"other",
			[output_id("Left Magnet"), output_id("Upper Magnet"), output_id("Right Magnet")],
			[],
			"Three under-playfield magnets (solenoids 16, 23, 24) are implemented in the retained script through "
			"the shared cvpmMagnet helper class: LeftMagnet.InitMagnet LMagnet with .solenoid=16, UpperMagnet."
			"InitMagnet UMagnet with .solenoid=23, RightMagnet.InitMagnet RMagnet with .solenoid=24. Unlike the "
			"Thing magnet (mechanism.thing-saucer, a scripted kicker sequence), these three are generic ball-"
			"holding/redirecting magnets with no dedicated printed sensor switch.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
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
			"Two FL-15411 flippers on Fliptronic circuits 45/46 (right) and 47/48 (left). Each flipper has a "
			"separate power and hold winding: FLIP_BUT(FLIP_L) gives these two positions the direct hardware "
			"button-to-coil bypass circuit, so the cabinet flip buttons (112 right, 114 left) fire the coils with "
			"minimum latency, dropping to the hold winding once the end-of-stroke leaf switch closes (111 right, "
			"113 left). The retained table runs Const UseSolenoids = 2 (fast flips).",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button 114 and end-of-stroke switch 113."),
			],
			MANUAL_HANDBOOK_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R right with A-15205-L-4 left",
		),
		mechanism(
			"mechanism.upper-right-flipper",
			"Upper right flipper",
			"other",
			[output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold")],
			["switch.generic-115", "switch.generic-116"],
			"An FL-11630 flipper on Fliptronic circuits 33 (power) / 34 (hold), fitted at the upper-right of the "
			"playfield (retained table object Flipper1). tafGameData sets FLIP_SOL(FLIP_UR), so the WPC core drives "
			"it as a real 2-state PWM flipper output, but FLIP_BUT(FLIP_L) does not include the upper positions, "
			"so (unlike the lower flippers) it is CPU/software-timed rather than hardware-bypassed. taf.c's own "
			"ball-routing simulator never reads this solenoid's state, so this project has not independently "
			"confirmed from static sources alone whether the ROM ties its firing unconditionally to the right flip "
			"button or gates it further; the retained script always mirrors whatever the ROM asserts on solenoid "
			"34 by rotating Flipper1 (SolURFlipper).",
			[("eos", "Upper right flipper at end of stroke", ["switch.generic-115"], "End-of-stroke leaf switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R",
		),
		mechanism(
			"mechanism.upper-left-flipper",
			"Upper left \"Thing's Mini-Flipper\"",
			"other",
			[output_id("Upper Left Flipper Power"), output_id("Upper Left Flipper Hold")],
			["switch.generic-117", "switch.generic-118", "switch.matrix-57", "switch.matrix-45", "switch.matrix-47", "switch.matrix-48", "switch.matrix-71"],
			"An FL-11753 flipper on Fliptronic circuits 35 (power) / 36 (hold), fitted at the upper-left of the "
			"playfield (retained table object Flipper2, rendered with 'Thing' hand art). Marketed in the "
			"Operations Manual as \"the 'Thing Flips' feature\", \"an exclusive Williams/Bally pinball innovation\": "
			"an AI-calibrated automatic flip, not a normal player-controlled flipper. The feature is enabled by "
			"the far-left flipper return lane (lights 'Lite Thing Flips', lamp 62); hitting the center ramp while "
			"lit diverts the ball to this flipper and the game attempts to shoot it into the swamp, self-"
			"calibrating over time to a 50-60% success rate. taf_stateDef's stTFlip ball-routing case is the only "
			"place in the driver's own logic that reads any upper-flipper solenoid state "
			"(core_getSol(sULFlip)), confirming the asymmetry with the upper-right flipper. The manual names this "
			"feature's own calibration inputs explicitly: the Bumper Lane Opto (57, 'above the upper left mini-"
			"flipper'), the three Swamp Million targets (45/47/48), and the Swamp Lock Upper switch (71).",
			[("eos", "Upper left flipper at end of stroke", ["switch.generic-117"], "End-of-stroke leaf switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-L-1",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.outhole-to-trough",
			"kind": "direct",
			"source": output_id("Outhole"),
			"destination": "switch.matrix-15",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.ball-release-to-shooter",
			"kind": "direct",
			"source": output_id("Ball Release"),
			"destination": "switch.matrix-27",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.swamp-release-to-lockup-kickout",
			"kind": "direct",
			"source": output_id("Swamp Release"),
			"destination": "switch.matrix-74",
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
			"id": "bally.the-addams-family.1992",
			"name": "The Addams Family",
			"manufacturer": "Bally",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 20,
		},
		"coverage": {
			"status": "partial",
			"missing": ["recreation_notes"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "candidate",
				"spatial_placement": "validated",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-fliptronic",
			"hardware_generation": "0x8",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/the-addams-family-1992.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Addams Family device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the remaining blocker to promotion is auditable."""
	resolved_input_addresses: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			resolved_input_addresses.append(address)
	resolved_output_bindings: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	placement_count = 0
	for device in definition["inputs"] + definition["outputs"]:
		spatial = device["spatial"]
		if spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])
	for device in definition["outputs"]:
		address = int(device["binding"]["device"])
		group = device["binding"]["group"]
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append({"group": group, "address": address})
		else:
			resolved_output_bindings.append({"group": group, "address": address})

	projections = [
		{"device": "switch.matrix-81", "projected_onto": "vault_base (Bookcase assembly primitive center)", "reason": "taf_handleMech synthesizes swBookOpen purely from motor position; no discrete playfield sensor."},
		{"device": "switch.matrix-82", "projected_onto": "vault_base (Bookcase assembly primitive center)", "reason": "taf_handleMech synthesizes swBookClose purely from motor position; no discrete playfield sensor."},
		{"device": "switch.matrix-84", "projected_onto": "Thing (Thing hand assembly primitive center)", "reason": "taf_handleMech synthesizes swThingDn purely from motor position; no discrete playfield sensor."},
		{"device": "switch.matrix-85", "projected_onto": "Thing (Thing hand assembly primitive center)", "reason": "taf_handleMech synthesizes swThingUp purely from motor position; no discrete playfield sensor."},
		{"device": output_id("Thing Motor"), "projected_onto": "Thing (Thing hand assembly primitive center)", "reason": "ThingMotor mechanism callback rotates Thing/handMAGNET/thingBox directly; no separate motor object in the retained table."},
		{"device": output_id("Bookcase Motor"), "projected_onto": "vault_base (Bookcase assembly primitive center)", "reason": "BookCaseMotor mechanism callback rotates vault_base directly; no separate motor object in the retained table."},
	]
	excluded_object_classes = [
		"L11b, L12b, ... L87b-style co-located brightness-doubling Light objects at every lamp address (render doubling, not a second physical bulb)",
		"L45old (superseded art duplicate of L45bold at the same 'The Mamushku' insert)",
		"GILeftPrims / GIRightPrims collection members (shaded plastics that dim with GI, not individual bulb sockets)",
	]

	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": definition["coverage"]["status"],
		"blockers": [
			"coverage.missing = [\"recreation_notes\"]: knowledge/bally/the-addams-family-1992.md documents every "
			"mechanism this definition references, but as a single unreviewed curation pass it has not had the "
			"independent high-tier review this project requires before a knowledge note counts as validated "
			"recreation_knowledge. No conflict, unresolved address, or missing spatial placement remains -- this "
			"is the sole reason the record stays partial rather than a genuine gap in the electrical or spatial "
			"evidence.",
		],
		"unresolved": [],
		"placement_count": placement_count,
		"coordinate_convention": {
			"space": "playfield",
			"x": "x/952.965; 0=left, 1=right",
			"y": "y/2164.76; 0=rear/backglass, 1=apron/player",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": BOUNDS_X, "bottom": BOUNDS_Y},
		},
		"resolved_input_addresses": sorted(resolved_input_addresses),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"resolved_output_bindings": sorted(resolved_output_bindings, key=lambda item: (item["group"], item["address"])),
		"not_applicable_outputs": {
			reason: sorted(items, key=lambda item: (item["group"], item["address"]))
			for reason, items in sorted(not_applicable_outputs.items())
		},
		"projections": projections,
		"excluded_object_classes": excluded_object_classes,
		"extraction": {
			"vpxtool_version": "vpxtool git:v0.33.3",
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/the-addams-family-1992/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"fail_closed": True,
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"ops_manual_sha256": OPS_MANUAL_SHA256,
			"handbook_sha256": HANDBOOK_SHA256,
			"wpc_schematic_manual_sha256": SCHEMATIC_SHA256,
		},
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.the-addams-family.1992/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/the-addams-family-1992/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		f"# Spatial audit -- {report['machine_id']}",
		"",
		f"Coverage status: `{report['status']}`",
		"",
		"## Blockers",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += ["", "## Evidence", ""]
	lines.append(f"- VPX table SHA-256 `{report['source_hashes']['table_sha256']}`")
	lines.append(f"  - Bounds `{TABLE_BOUNDS}`; normalization `{report['coordinate_convention']['x']}` / `{report['coordinate_convention']['y']}`")
	extraction = report["extraction"]
	lines.append(
		f"- Extraction manifest `{extraction['manifest_uri']}`, SHA-256 `{extraction['manifest_sha256']}`, "
		f"{extraction['file_count']} files, {extraction['total_bytes']} bytes ({extraction['vpxtool_version']})"
	)
	cache = report["visual_review_cache"]
	lines.append(f"- Manual transcription `{cache['transcription']['path']}`, SHA-256 `{cache['transcription']['sha256']}`")
	lines.append(f"- Rendered page cache `{cache['root']}`")
	lines += ["", f"## Resolved input addresses ({len(report['resolved_input_addresses'])})", ""]
	lines.append(", ".join(str(address) for address in report["resolved_input_addresses"]) or "(none)")
	lines += ["", "## Not-applicable inputs by reason", ""]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- `{reason}`: {', '.join(str(address) for address in addresses)}")
	lines += ["", f"## Resolved output bindings ({len(report['resolved_output_bindings'])})", ""]
	by_group: dict[str, list[int]] = {}
	for item in report["resolved_output_bindings"]:
		by_group.setdefault(item["group"], []).append(item["address"])
	for group, addresses in sorted(by_group.items()):
		lines.append(f"- `{group}`: {', '.join(str(address) for address in sorted(addresses))}")
	lines += ["", "## Not-applicable outputs by reason", ""]
	for reason, items in report["not_applicable_outputs"].items():
		formatted = ", ".join(f"{item['group']}:{item['address']}" for item in items)
		lines.append(f"- `{reason}`: {formatted}")
	lines += ["", "## Projections (documented, onto the device's own mechanism assembly)", ""]
	for projection in report["projections"]:
		lines.append(f"- `{projection['device']}` -> {projection['projected_onto']}: {projection['reason']}")
	lines += ["", "## Excluded object classes", ""]
	for excluded in report["excluded_object_classes"]:
		lines.append(f"- {excluded}")
	lines += ["", f"## Placement count: {report['placement_count']}", ""]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(DEFINITION_PATH, definition)
	write_json(SEED_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	return DEFINITION_PATH


def check(root: Path = ROOT) -> None:
	definition = build()
	on_disk = load_json(DEFINITION_PATH)
	if canonical_bytes(on_disk) != canonical_bytes(definition):
		raise RuntimeError(f"{DEFINITION_PATH} is out of date; run --regenerate")
	seed = load_json(SEED_PATH)
	if canonical_bytes(seed) != canonical_bytes(definition):
		raise RuntimeError(f"{SEED_PATH} is out of date or diverges from the definition; run --regenerate")
	if AUTHOR_READY_PATH.is_file():
		raise RuntimeError(f"{AUTHOR_READY_PATH} exists but this game is not promoted; refusing to leave a duplicate definition")
	report = build_spatial_report(definition)
	report_on_disk = load_json(SPATIAL_REPORT_PATH)
	if canonical_bytes(report_on_disk) != canonical_bytes(report):
		raise RuntimeError(f"{SPATIAL_REPORT_PATH} is out of date; run --regenerate")
	markdown_on_disk = SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
	if markdown_on_disk != render_spatial_report(report):
		raise RuntimeError(f"{SPATIAL_REPORT_MARKDOWN_PATH} is out of date; run --regenerate")
	if STUB_PATH.is_file():
		raise RuntimeError(f"{STUB_PATH} should have been pruned by catalog regeneration once this definition claims taf_l5")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, seed, and spatial report")
	mode.add_argument("--check", action="store_true", help="Verify the on-disk artifacts match the deterministic build with no drift")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		print(f"Addams Family extraction manifest written: {write_extraction_manifest(source_root)}")
		return
	if args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		verify_extraction_manifest(source_root)
		print("Addams Family retained extraction matches its pinned manifest identity.")
		return
	if args.regenerate:
		path = generate(ROOT)
		print(f"Addams Family definition written: {path}")
		return
	check(ROOT)
	print("Addams Family definition matches the deterministic build (no drift).")


if __name__ == "__main__":
	main()
