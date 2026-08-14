"""Curate the physical Williams White Water (1993) machine definition.

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
# White Water is kept `partial`: lamps 17 and 55 drive dedicated image-cycling
# primitives that sit at a raw local origin in the retained extraction rather
# than a playfield coordinate, so neither has an asserted position. Every
# other dimension, including the switch-matrix opto polarity sweep, is
# validated with zero disagreement.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/white-water-1993.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/white-water-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/white-water-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/white-water-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/white-water-1993.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.williams.white-water.1993"
HANDBOOK_SOURCE = "manual-support.williams.white-water.1993.handbook"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.white-water.1993"
VPX_TABLE_SOURCE = "vpx-table.ww-flupper"
VPX_SCRIPT_SOURCE = "vpx-script.ww-flupper"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ww-flupper"

TABLE_SHA256 = "7c59095e9c6a7e100e79f80d7d83497b1c87817bc9daf939721f1a8727a781cd"
SCRIPT_SHA256 = "0676acb1e610bda8f42f94a915a70bb1b71b6e48462326dd43083a3ab4fa0096"
MANUAL_SHA256 = "919f057184916e5ba43141eee7ccf3955a4aae9dfb22118033888d39eea888c0"
HANDBOOK_SHA256 = "e133b899641bfa71b844f8eb42c00b1ac4a2ac6f273ee7153c7569bce5fc7f85"
MANUAL_TRANSCRIPTION_SHA256 = "0c55e5c896738526846d9a04b3b96f5ca61fbfbd5dc85fdd3516c29f1f94a64f"

EXTRACTION_RELATIVE_PATH = Path("williams/white-water-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/white-water-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "0ec3e7f0c856de3767d1f7e3bf285cd14e533501c798fedcf316833962076b59"
EXTRACTION_FILE_COUNT = 1166
EXTRACTION_TOTAL_BYTES = 141788903

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2092"

DRIVER_IDS = (
	"ww_l5", "ww_d5", "ww_lh5", "ww_lh6", "ww_lh6c", "ww_l4", "ww_d4", "ww_l3", "ww_d3",
	"ww_l2", "ww_d2", "ww_p8", "ww_p9", "ww_p6",
	"ww_bfr01", "ww_bfr01b", "ww_bfr01c", "ww_bfr01d", "ww_bfr01e",
)
DRIVER_COMPATIBILITY = {
	"ww_l5": ("identical", "Williams production L-5 game ROM shipped with the physical machine."),
	"ww_d5": ("identical", "Williams D-5 LED Ghost Fix game ROM; a later firmware revision of the same physical machine with no controller-address or playfield change."),
	"ww_lh5": ("identical", "Williams LH-5 Home ROM; a later firmware revision of the same physical machine with no controller-address or playfield change."),
	"ww_lh6": ("identical", "Williams LH-6 Home ROM. This is the driver the retained known-working VPX table binds to (cGameName = \"ww_lh6\"), a 2000 home-conversion revision of the identical physical hardware and I/O inventory as L-5."),
	"ww_lh6c": ("identical", "Williams LH-6 Coin Play Home ROM; a coin-play variant of ww_lh6 on the identical physical machine."),
	"ww_l4": ("identical", "Williams L-4 game ROM; an earlier firmware revision of the same physical machine."),
	"ww_d4": ("identical", "Williams D-4 LED Ghost Fix game ROM; an earlier firmware revision of the same physical machine."),
	"ww_l3": ("identical", "Williams L-3 game ROM; an earlier firmware revision of the same physical machine."),
	"ww_d3": ("identical", "Williams D-3 LED Ghost Fix game ROM; an earlier firmware revision of the same physical machine."),
	"ww_l2": ("identical", "Williams L-2 game ROM; an earlier firmware revision of the same physical machine."),
	"ww_d2": ("identical", "Williams D-2 LED Ghost Fix game ROM; an earlier firmware revision of the same physical machine."),
	"ww_p8": ("identical", "Williams P-8 prototype game ROM for the same physical White Water machine; the switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged."),
	"ww_p9": ("identical", "Williams P-9 prototype LED Ghost Fix game ROM for the same physical machine."),
	"ww_p6": ("identical", "Williams P-6 prototype game ROM for the same physical machine."),
	"ww_bfr01": ("compatible", "FreeWPC/Bigfoot community firmware R0.1 for the same physical machine and controller hardware."),
	"ww_bfr01b": ("compatible", "FreeWPC/Bigfoot community firmware R0.1b for the same physical machine and controller hardware."),
	"ww_bfr01c": ("compatible", "FreeWPC/Bigfoot community firmware R0.1c for the same physical machine and controller hardware."),
	"ww_bfr01d": ("compatible", "FreeWPC/Bigfoot community firmware R0.1d for the same physical machine and controller hardware."),
	"ww_bfr01e": ("compatible", "FreeWPC/Bigfoot community firmware R0.1e for the same physical machine and controller hardware, a later community revision."),
}

# --- Printed switch matrix (manual pages 2-42 parts list, 3-4 wiring; both transcribed
# in evidence/excerpts/williams.white-water.1993/switch-locations.md and switch-matrix.md).
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "Outhole", 16: "Left Jet Bumper",
	17: "Right Jet Bumper", 18: "Center Jet Bumper",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Opto", 24: "Always Closed",
	25: "Left Outlane", 26: "Left Flipper Lane", 27: "Right Flipper Lane", 28: "Right Outlane",
	31: "River \"R2\"", 32: "River \"E\"", 33: "River \"V\"", 34: "River \"I\"", 35: "River \"R1\"",
	36: "3-Bank Top", 37: "3-Bank Center", 38: "3-Bank Lower",
	41: "Light Lock Left", 42: "Light Lock Right", 43: "Left Loop", 44: "Right Loop",
	45: "Secret Passage", 46: "Left Ramp Enter", 47: "Rapids Enter", 48: "Canyon Entrance",
	51: "Left Sling", 52: "Right Sling", 53: "Ball Shooter", 54: "Lower Jet Arena",
	55: "Right Jet Arena", 56: "Extra Ball", 57: "Canyon Main", 58: "Bigfoot Cave",
	61: "Whirlpool Popper", 62: "Whirlpool Exit", 63: "Lockup Right", 64: "Lockup Center",
	65: "Lockup Left", 66: "Left Ramp Main", 68: "Disaster Drop Enter",
	71: "Rapids Ramp Main", 73: "Hot Foot Upper", 74: "Hot Foot Lower",
	75: "Disaster Drop Main", 76: "Right Trough", 77: "Center Trough", 78: "Left Trough",
	86: "Bigfoot Opto 1", 87: "Bigfoot Opto 2",
}
# Printed matrix positions marked "Not Used" on both the switch-locations parts list
# (2-42) and the switch-matrix wiring page (3-4).
UNUSED_MATRIX_ADDRESSES = {11, 12, 67, 72, 81, 82, 83, 84, 85, 88}
# Every switch built from the A-14315 (LED) + A-14316 (Trans) pair, or from the single
# part 5490-12451-00, per the switch-locations parts list: physically opto/proximity
# construction with no mechanical switch part.
OPTO_SWITCHES = {61, 62, 63, 64, 65, 66, 68, 86, 87}
# PinMAME's wwGameData inverted-switch mask covers column 6 (0xbf = 0b10111111: bits
# 0-5 and 7 set, i.e. rows 1-6 and 8 = switches 61-66, 68) and column 8 (0x60 =
# 0b01100000: bits 5-6 set, i.e. rows 6-7 = switches 86, 87). The only column-6 bit
# left clear is bit 6 (row 7 = switch 67), which is printed "Not Used" anyway, so
# this sweep found zero disagreement between the manual's opto construction and
# PinMAME's normalization -- every address in OPTO_SWITCHES is covered.
PINMAME_NORMALIZED_OPTO_SWITCHES = {61, 62, 63, 64, 65, 66, 68, 86, 87}
# vpmTimer.PulseSw / momentary-target callers in the retained script.
PULSED_SWITCHES = {25, 26, 27, 28, 31, 62}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "leaf", 22: "microswitch", 23: "other", 24: "other",
	25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "microswitch", 32: "microswitch", 33: "microswitch", 34: "microswitch", 35: "microswitch",
	36: "microswitch", 37: "microswitch", 38: "microswitch",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch",
	45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "leaf", 52: "leaf", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "opto", 62: "opto", 63: "opto", 64: "opto", 65: "opto", 66: "opto", 68: "opto",
	71: "microswitch", 73: "microswitch", 74: "microswitch", 75: "microswitch",
	76: "microswitch", 77: "microswitch", 78: "microswitch",
	86: "opto", 87: "opto",
}

# address -> (assembly/part number or LED+Trans pair, notes suffix)
SWITCH_PARTS = {
	13: "20-9663-1", 14: "20-9502-A", 15: "5647-12133-12",
	16: "SW-11A-37", 17: "SW-11A-37", 18: "SW-11A-37",
	21: "SW-1A-117", 22: "5643-09288-00", 24: "A-8630",
	25: "5647-12693-19", 26: "5647-12693-19", 27: "5647-12693-19", 28: "5647-12693-19",
	31: "B-12912-10", 32: "B-12912-10", 33: "B-12912-10", 34: "B-12912-10", 35: "B-12912-10",
	36: "B-12912-23", 37: "B-12912-23", 38: "B-12912-23",
	41: "A-14604-11", 42: "A-14604-11", 43: "5647-12693-19", 44: "5647-12693-19",
	45: "5647-12693-19", 46: "5647-12693-11", 47: "5647-12693-11", 48: "5647-12693-11",
	51: "SW-1A-114 (kick) with SW-1A-120 (score)", 52: "SW-1A-114 (kick) with SW-1A-120 (score)",
	53: "5647-12693-04", 54: "SW-1A-120", 55: "SW-1A-120", 56: "A-14604-12",
	57: "5647-12693-21", 58: "5647-12693-13",
	61: "A-14315 (LED) with A-14316 (Trans)", 62: "A-14315 (LED) with A-14316 (Trans)",
	63: "A-14315 (LED) with A-14316 (Trans)", 64: "A-14315 (LED) with A-14316 (Trans)",
	65: "A-14315 (LED) with A-14316 (Trans)", 66: "A-14315 (LED) with A-14316 (Trans)",
	68: "A-14315 (LED) with A-14316 (Trans)",
	71: "5647-12693-21", 73: "B-12912-24", 74: "B-12912-24", 75: "5647-12693-21",
	76: "5647-12693-08", 77: "5647-09957-00", 78: "5647-09957-00",
	86: "5490-12451-00", 87: "5490-12451-00",
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
# Fliptronic F1-F8 wiring, printed 3-4. Only F1-F6 have a matching row on the
# Switch Locations parts list (2-42); F7/F8 print the generic template with no part.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J905-1"), 112: ("Blue-Violet", "J905-2"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J905-5"),
}

# --- Printed solenoid/flasher table (manual pages 2-41 locations, 3-8 wiring).
SOLENOID_LABELS = {
	1: "Outhole", 2: "Ball Serve", 3: "Whirlpool Popper", 4: "Lockup Popper",
	5: "Kickback", 6: "Ramp Diverter", 7: "Knocker",
	8: "Backglass Flasher", 9: "Wet Willie Head Flasher",
	10: "Left Sling", 11: "Right Sling", 12: "Left Jet Bumper", 13: "Right Jet Bumper",
	14: "Center Jet Bumper", 15: "Backglass Raft Flasher", 16: "Backglass Riders Flasher",
	17: "Bigfoot Body Flasher", 18: "Right Mountains Flasher", 19: "Left Mountains Flasher",
	20: "Upper Left Playfield Flasher", 21: "Insanity Falls Flasher",
	22: "Whirlpool Popper Flasher", 23: "Whirlpool Enter Flasher", 24: "Bigfoot Cave Flasher",
	25: "Bigfoot Drive", 26: "Bigfoot Enable", 27: "Chase Lamp Clock", 28: "Chase Lamp Data",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {
	35: "Not Used Upper Left Flipper Power", 36: "Not Used Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose Relay Bit A", 30: "WPC J111 General-Purpose Relay Bit B",
	31: "WPC State Channel 31", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Address 37", 38: "Unused WPC-Fliptronic Address 38",
	39: "Unused WPC-Fliptronic Address 39", 40: "Unused WPC-Fliptronic Address 40",
	41: "Unused WPC-Fliptronic Address 41", 42: "Unused WPC-Fliptronic Address 42",
	43: "Unused WPC-Fliptronic Address 43", 44: "Unused WPC-Fliptronic Address 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}

SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", power_connection="J107-3", part_number="AE-27-1200", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", power_connection="J107-3", part_number="AE-26-1200", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", power_connection="J107-3", part_number="AE-26-1200", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	8: dict(control_connection="J131-5", driver_transistor="Q70", power_connection="J106-5", printed_type="High Power"),
	9: dict(control_connection="J129-1", driver_transistor="Q58", power_connection="J106-5", printed_type="Low Power"),
	10: dict(control_connection="J127-3", driver_transistor="Q56", power_connection="J107-2", part_number="AE-27-1200", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", power_connection="J107-2", part_number="AE-27-1200", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J128-3", driver_transistor="Q46", power_connection="J106-5", printed_type="Low Power"),
	16: dict(control_connection="J128-5", driver_transistor="Q44", power_connection="J106-5", printed_type="Low Power"),
	17: dict(control_connection="J126-1", driver_transistor="Q42", power_connection="J107-6", printed_type="Flasher"),
	18: dict(control_connection="J126-2", driver_transistor="Q40", power_connection="J107-6", printed_type="Flasher"),
	19: dict(control_connection="J126-3", driver_transistor="Q38", power_connection="J107-6", printed_type="Flasher"),
	20: dict(control_connection="J126-4", driver_transistor="Q36", power_connection="J107-6", printed_type="Flasher"),
	21: dict(control_connection="J126-5", driver_transistor="Q28", power_connection="J107-6", printed_type="Flasher"),
	22: dict(control_connection="J126-6", driver_transistor="Q30", power_connection="J107-6", printed_type="Flasher"),
	23: dict(control_connection="J126-7", driver_transistor="Q34", power_connection="J107-6", printed_type="Flasher"),
	24: dict(control_connection="J126-8", driver_transistor="Q32", power_connection="J107-6", printed_type="Flasher"),
	25: dict(control_connection="J122-1", driver_transistor="Q26", power_connection="J118-2,3", part_number="A-15680", printed_type="Low Power motor"),
	26: dict(control_connection="J122-2", driver_transistor="Q24", power_connection="J118-2,3", part_number="A-15680", printed_type="Low Power motor"),
	27: dict(control_connection="J123-4", driver_transistor="Q22", power_connection="J105-4,5; J118-2,3", part_number="A-15761", printed_type="Low Power shift-register clock"),
	28: dict(control_connection="J123-5", driver_transistor="Q20", power_connection="J105-4,5; J118-2,3", part_number="A-15761", printed_type="Low Power shift-register data"),
	33: dict(control_connection="J907-4,5", driver_transistor="Q2", power_connection=None, printed_type="Fliptronic power"),
	34: dict(control_connection="J907-4,5", driver_transistor="Q7", power_connection=None, printed_type="Fliptronic hold"),
	45: dict(control_connection="J907-8,9", driver_transistor="Q4", power_connection=None, part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(control_connection="J907-8,9", driver_transistor="Q11", power_connection=None, part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(control_connection="J907-6,7", driver_transistor="Q3", power_connection=None, part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(control_connection="J907-6,7", driver_transistor="Q9", power_connection=None, part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {33: "Blu-Yel", 34: "Org-Vio", 45: "Blu-Yel", 46: "Blu-Vio", 47: "Gry-Yel", 48: "Org-Blu"}

SOLENOID_ASSEMBLIES = {
	1: "A-8039-3", 2: "B-9362-R-3", 3: "A-15758", 4: "A-15769", 5: "B-11873", 6: "A-15573",
	7: "B-10686-1", 10: "A-15749", 11: "A-14369-R", 12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2",
	17: "A-14342", 18: "A-11541", 19: "A-8798", 20: "A-8798", 21: "A-11541", 22: "A-11541",
	23: "A-8798", 24: "A-8798", 25: "A-15680", 26: "A-15680", 27: "A-15761", 28: "A-15761",
	45: "A-15205-R-2", 46: "A-15205-R-2", 47: "A-15205-L-2", 48: "A-15205-L-2",
	33: "A-15843", 34: "A-15843",
}
# Retained script callbacks/drivers, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "kisort", 2: "KickBallToLane", 3: "KickPopper", 4: "KickBallUp", 5: "SolKick",
	6: "SolDiv", 7: 'vpmSolSound "Knocker"', 8: "Flasherset8", 9: "Flasherset9",
	10: "LeftSlingShot_Slingshot", 11: "RightSlingShot_Slingshot",
	12: "Bumper1_Hit (pulses switch 16)", 13: "Bumper2_Hit (pulses switch 17)",
	14: "Bumper3_Hit (pulses switch 18)",
	15: "Flasherset15", 16: "Flasherset16", 17: "Flasherset17", 18: "Flasherset18",
	19: "Flasherset19", 20: "Flasherset20", 21: "Flasherset21", 22: "Flasherset22",
	23: "Flasherset23", 24: "Flasherset24",
	25: "SolBigFootDrive (BigTimer.Enabled)", 26: "SolBigFootEnable (BigDir = ABS(Enabled))",
	46: "SolRFlipper", 48: "SolLFlipper",
}

FLASHER_BULBS = {
	8: ("(2) #906 on the backbox", 2, 0), 9: ("(1) #906 on the backbox", 1, 0),
	15: ("(2) #906 on the backbox", 2, 0), 16: ("(2) #906 on the backbox", 2, 0),
	17: ("(1) #89 on the playfield and (1) #906 on the backbox", 2, 1),
	18: ("(1) #89 on the playfield and (1) #906 on the backbox", 2, 1),
	19: ("(1) #89 on the playfield", 1, 1),
	20: ("(1) #89 on the playfield and (1) #906 on the backbox", 2, 1),
	21: ("(1) #89 on the playfield", 1, 1),
	22: ("(1) #89 on the playfield", 1, 1),
	23: ("(1) #89 on the playfield", 1, 1),
	24: ("(1) #89 on the playfield and (1) #906 on the backbox", 2, 1),
}

# --- Printed lamp matrix (manual page 2-40 locations, 3-2 wiring).
LAMP_LABELS = {
	11: "Shoot Again", 12: "Kickback", 13: "Left Outlane", 14: "Left Flipper Lane",
	15: "Right Flipper Lane", 16: "Right Outlane", 17: "Lights Whirlpool", 18: "6X Multiplier",
	21: "River \"R1\"", 22: "River \"I\"", 23: "River \"V\"", 24: "River \"E\"", 25: "River \"R2\"",
	26: "Hazzard 3", 27: "Lock 1", 28: "Lock 2",
	31: "Raft 7", 32: "Raft 8", 33: "Wet Willie", 34: "Ramps Millions", 35: "Hazzard 4",
	36: "Left Light Lock", 37: "2X Multiplier", 38: "3X Multiplier",
	41: "3-Bank Center", 42: "3-Bank Lower", 43: "Lock Release", 44: "3-Bank Top",
	45: "Hazzard 4", 46: "Right Light Lock", 47: "4X Multiplier", 48: "5X Multiplier",
	51: "Hazzard 1", 52: "Hazzard 5", 53: "Hazzard 6", 54: "Hazzard 7", 55: "Whirlpool Lit",
	56: "Extra Ball", 57: "Whirl Challange", 58: "Boulder Man Over",
	61: "Raft 1", 62: "Raft 2", 63: "Raft 3", 64: "Raft 4", 65: "Raft 5", 66: "Raft 6",
	67: "2-Bank Upper", 68: "2-Bank Lower",
	71: "Whirlpool 1", 72: "Whirlpool 2", 73: "Whirlpool 3", 74: "Whirlpool 4",
	75: "Whirlpool 5", 76: "Whirlpool 6", 77: "Multi Jackpot", 78: "Bigfoot Jackpot",
	81: "Light Extra Ball", 82: "Advance Raft", 83: "Mystery", 84: "Boulder 5X Award",
	88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-11754", "#44"), 12: ("A-11754", "#44"), 13: ("A-11271", "#44"),
	14: ("A-11271", "#44"), 15: ("A-11754", "#4"), 16: ("A-11754", "#44"),
	17: ("A-11754", "#44"), 18: ("A-11754", "#44"),
	21: ("A-15763", "#555"), 22: ("A-15763", "#555"), 23: ("A-15763", "#555"),
	24: ("A-15763", "#555"), 25: ("A-15763", "#555"), 26: ("A-15766", "#555"),
	27: ("A-15766", "#555"), 28: ("A-15766", "#555"),
	31: ("A-15767", "#555"), 32: ("A-15767", "#555"), 33: ("A-15767", "#555"),
	34: ("A-15767", "#555"), 35: ("A-15767", "#555"), 36: ("A-15767", "#555"),
	37: ("A-11271", "#555"), 38: ("A-11754", "#44"),
	41: ("A-15767", "#555"), 42: ("A-15767", "#555"), 43: ("A-15767", "#555"),
	44: ("A-15767", "#555"), 45: ("A-15767", "#555"), 46: ("A-15767", "#555"),
	47: ("A-11754", "#44"), 48: ("A-11271", "#44"),
	51: ("A-11271", "#44"), 52: ("A-11271", "#44"), 53: ("A-11905", "#44"),
	54: ("A-11905", "#44"), 55: (None, None), 56: ("A-15764", "#555"),
	57: ("A-15764", "#555"), 58: ("A-15764", "#555"),
	61: ("A-15764", "#555"), 62: ("A-15764", "#555"), 63: ("A-15764", "#555"),
	64: ("A-15764", "#555"), 65: ("A-15764", "#555"), 66: ("A-15764", "#555"),
	67: ("A-15764", "#555"), 68: ("A-15764", "#555"),
	71: ("A-15768", "#555"), 72: ("A-15768", "#555"), 73: ("A-15768", "#555"),
	74: ("A-15768", "#555"), 75: ("A-15768", "#555"), 76: ("A-15768", "#555"),
	77: ("A-11905", "#44"), 78: ("A-11905", "#44"),
	81: ("A-11271", "#44"), 82: ("A-11754", "#44"), 83: ("A-11754", "#44"),
	84: ("A-11271", "#44"), 88: (None, None),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

GI_STRINGS = {
	0: ("Playfield Upper", "J120-1", "Q18", "Wht-Brn", "#44 (playfield)"),
	1: ("Playfield Center", "J120-2", "Q10", "Wht-Org", "#44 (playfield)"),
	2: ("Playfield Lower", "J120-3 / J121-3", "Q14", "Wht-Yel", "#44 (playfield) / #555 (backbox)"),
	3: ("Backglass Boat", "J121-5", "Q16", "Wht-Grn", "#555 (backbox)"),
	4: ("Backglass Sky", "J121-6 / J119-3", "Q12", "Wht-Vio", "#555 (backbox)"),
}

# --- Normalized playfield coordinates derived from the retained VPX extraction
# (x/952, y/2092; see review-artifacts/white-water/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.499215, 0.961038)], 16: [(0.686754, 0.48341)], 17: [(0.908207, 0.482965)],
	18: [(0.808768, 0.568005)],
	25: [(0.053448, 0.788561)], 26: [(0.146367, 0.734668)], 27: [(0.762698, 0.733357)],
	28: [(0.846864, 0.734798)],
	31: [(0.135574, 0.577772)], 32: [(0.131311, 0.553003)], 33: [(0.127049, 0.528533)],
	34: [(0.122786, 0.503167)], 35: [(0.118196, 0.477653)],
	36: [(0.580704, 0.363876)], 37: [(0.593942, 0.387451)], 38: [(0.607222, 0.411717)],
	41: [(0.309172, 0.316379)], 42: [(0.451459, 0.311159)],
	43: [(0.057634, 0.203817)], 44: [(0.942396, 0.226237)], 45: [(0.248231, 0.158665)],
	46: [(0.215275, 0.271259)], 47: [(0.323162, 0.179004)], 48: [(0.404967, 0.13748)],
	51: [(0.229235, 0.730515)], 52: [(0.676448, 0.730377)], 53: [(0.938317, 0.884692)],
	54: [(0.904126, 0.622177)], 55: [(0.941479, 0.544775)],
	56: [(0.749854, 0.604407)], 57: [(0.663283, 0.03151)], 58: [(0.867285, 0.409925)],
	61: [(0.166481, 0.628184)], 62: [(0.723889, 0.408041)], 63: [(0.653491, 0.098234)],
	64: [(0.591746, 0.087434)], 65: [(0.536605, 0.078469)], 66: [(0.942203, 0.116991)],
	68: [(0.525009, 0.267147)],
	71: [(0.05648, 0.131631)], 73: [(0.609679, 0.504908)], 74: [(0.633578, 0.52383)],
	75: [(0.114134, 0.053198)], 76: [(0.865391, 0.863494)], 77: [(0.815577, 0.877575)],
	78: [(0.761013, 0.891168)],
	86: [(0.813025, 0.176864)], 87: [(0.813025, 0.176864)],
}
SWITCH_PROJECTIONS = {
	86: "Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center): the two head-position optos 86/87 are printed on a board mounted inside the Bigfoot mechanism, not as separate playfield objects, and PinMAME's ww_handleMech reads them from a single 7-bit motor-position counter (locals.bigfootPos) rather than from any Trigger/Kicker on the retained table.",
	87: "Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); see switch 86.",
}

SOLENOID_POSITIONS = {
	1: [(0.499215, 0.961038)], 2: [(0.865391, 0.863494)], 3: [(0.166481, 0.628184)],
	4: [(0.653491, 0.098234)], 5: [(0.05714, 0.80622)], 6: [(0.694655, 0.139067)],
	10: [(0.229235, 0.730515)], 11: [(0.676448, 0.730377)],
	12: [(0.686754, 0.48341)], 13: [(0.908207, 0.482965)], 14: [(0.808768, 0.568005)],
	17: [(0.757729, 0.128745)], 18: [(0.787258, 0.091191)], 19: [(0.266794, 0.098698)],
	20: [(0.055373, 0.07929)], 21: [(0.198704, 0.536541)], 22: [(0.183539, 0.647809)],
	23: [(0.664359, 0.362722)], 24: [(0.942258, 0.389003)],
	25: [(0.813025, 0.176864)], 26: [(0.813025, 0.176864)],
	33: [(0.858037, 0.307226)], 34: [(0.858037, 0.307226)],
	45: [(0.624182, 0.839867)], 46: [(0.624182, 0.839867)],
	47: [(0.283103, 0.839867)], 48: [(0.283103, 0.839867)],
}
SOLENOID_PROJECTION_NOTES = {
	21: "Coordinate taken from Flasher16, the one positioned VPX object toggled by the retained script's Flasherset21 routine alongside the off-table Flasherlight21/FlasherFlash21 helper objects (both of which sit outside the 0..1 playfield bounds and are excluded as table-modeling anomalies).",
	25: "Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); solenoid 25 is the H-bridge-style drive pulse for the head motor.",
	26: "Projected onto the rotating Bigfoot figure (Primitive Primitive_BigFoot, table object center); solenoid 26 sets the head motor's rotation direction.",
}

LAMP_POSITIONS = {
	11: [(0.4534, 0.880172)], 12: [(0.066086, 0.746302)], 13: [(0.055706, 0.684453)],
	14: [(0.144936, 0.686242)], 15: [(0.766112, 0.686207)], 16: [(0.848533, 0.685643)],
	18: [(0.251685, 0.646762)],
	21: [(0.17323, 0.475439)], 22: [(0.177602, 0.501969)], 23: [(0.183673, 0.527146)],
	24: [(0.189016, 0.55308)], 25: [(0.194237, 0.576301)], 26: [(0.373067, 0.265755)],
	27: [(0.378808, 0.297313)], 28: [(0.383341, 0.316563)],
	31: [(0.327233, 0.506402)], 32: [(0.437606, 0.450079)], 33: [(0.394347, 0.377416)],
	34: [(0.287459, 0.424096)], 35: [(0.26929, 0.382471)], 36: [(0.322259, 0.351274)],
	37: [(0.340742, 0.765235)], 38: [(0.318709, 0.735606)],
	41: [(0.542478, 0.414373)], 42: [(0.555416, 0.439036)], 43: [(0.387415, 0.336295)],
	44: [(0.529751, 0.391373)], 45: [(0.515512, 0.356785)], 46: [(0.458267, 0.346133)],
	47: [(0.296758, 0.706826)], 48: [(0.274074, 0.676761)],
	51: [(0.873287, 0.415787)], 52: [(0.085266, 0.289901)], 53: [(0.474803, 0.235217)],
	54: [(0.603343, 0.230433)], 56: [(0.698845, 0.63783)], 57: [(0.622676, 0.608994)],
	58: [(0.6464, 0.575266)],
	61: [(0.425673, 0.728322)], 62: [(0.58137, 0.687443)], 63: [(0.516022, 0.635645)],
	64: [(0.401889, 0.662585)], 65: [(0.438514, 0.603356)], 66: [(0.471799, 0.560258)],
	67: [(0.550535, 0.550979)], 68: [(0.57987, 0.573061)],
	71: [(0.722464, 0.381942)], 72: [(0.673959, 0.394899)], 73: [(0.67394, 0.421259)],
	74: [(0.722108, 0.433864)], 75: [(0.771416, 0.421392)], 76: [(0.771299, 0.395056)],
	77: [(0.593509, 0.28394)], 78: [(0.669727, 0.262663)],
	81: [(0.719074, 0.566069)], 82: [(0.729762, 0.522935)], 83: [(0.818066, 0.505273)],
	84: [(0.81348, 0.45773)],
}

GI_POSITIONS = {
	0: [
		(0.087768, 0.046739), (0.156972, 0.165839), (0.949528, 0.172781),
		(0.500934, 0.17127), (0.03325, 0.171647), (0.445069, 0.284591),
		(0.583642, 0.280899), (0.16121, 0.301875), (0.297612, 0.296548),
		(0.291449, 0.235733), (0.531567, 0.252904), (0.211018, 0.257772),
		(0.071922, 0.037981), (0.777527, 0.011309), (0.927014, 0.061507),
		(0.59706, 0.170695), (0.735779, 0.24742), (0.803991, 0.168412),
		(0.896998, 0.261682),
		(0.069905, 0.049364), (0.14703, 0.284223), (0.297868, 0.284726),
		(0.289015, 0.219512), (0.445662, 0.273675), (0.889077, 0.270185),
		(0.597949, 0.170504), (0.925596, 0.062205), (0.76403, 0.038537),
		(0.734704, 0.234431),
	],
	1: [
		(0.019375, 0.585759), (0.945523, 0.500925), (0.836596, 0.577636),
		(0.888975, 0.490684), (0.919223, 0.42354), (0.514063, 0.535199),
		(0.655133, 0.497766), (0.625817, 0.404355), (0.617241, 0.370678),
		(0.777285, 0.340462), (0.647258, 0.305841),
	],
	2: [
		(0.803874, 0.744388), (0.757241, 0.795849), (0.69655, 0.81497),
		(0.102635, 0.74384), (0.210608, 0.815112), (0.149606, 0.79585),
		(0.647251, 0.783311), (0.688053, 0.756178), (0.709601, 0.721011),
		(0.688127, 0.75645), (0.21871, 0.757883), (0.191395, 0.715705),
		(0.218784, 0.758951), (0.26215, 0.782933), (0.825724, 0.852329),
		(0.447147, 0.829842), (0.087058, 0.855326), (0.146171, 0.66734),
		(0.481949, 0.960968), (0.03408, 0.906581), (0.79583, 0.949803),
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
		raise RuntimeError(f"White Water retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained White Water extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"White Water retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"White Water retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"White Water retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the ww_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/ww.c wwGameData GEN_WPCFLIPTRON with wpc_dispDMD, hw = "
				"{FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR), swCol=0, lampCol=2, custSol=0}, the "
				"inverted-switch mask {0},{0x00,0x00,0x00,0x00,0x00,0x00,0xbf,0x00,0x60,0x00,0x00,0x00} "
				"(column 6 = 0xbf, column 8 = 0x60), swStart/swTilt/swSlamTilt/swCoinDoor/swOutHole/"
				"swLeftJet/swRightJet/swCenterJet/swBigFoot1/swBigFoot2 defines, sOutHole/sTrough/"
				"sWpoolPopper/sLockupPopper/sKickBack/sDiverter/sKnocker/sLeftSling/sRightSling/sLeftJet/"
				"sRightJet/sCenterJet/sMotor/sMotorDriver defines, ww_handleMech's 7-bit locals.bigfootPos "
				"counter driving core_setSw(swBigFoot1/swBigFoot2) from (bigfootPos/32+1), and init_ww "
				"selecting wwGameData for driver years starting '19' and lh5GameData (same I/O, longer GI "
				"smoothing delay) for years starting '20'; src/wpc/core.h WPC solenoid numbering, "
				"CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, CORE_MAXSWCOL/invSw indexing; src/wpc/core.c "
				"core_getSol's GEN_ALLWPC 29-32 J111 GPIO remap and its GEN_WPC95/GEN_WPC95DCS-only 37-44 "
				"LPDC branch (this generation is neither, so 37-44 is unused address space here); "
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
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules; no LPDC board, so 37-44 is unused address space rather than a duplicated range",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.white-water.1993/ipdb/Williams_1993_White_Water_English_Manual.pdf",
			"original_filename": "Williams_1993_White_Water_English_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"154-page scanned Williams White Water operations manual with a real but column-scrambled "
				"text layer. Printed pages 2-40 through 2-42 carry the lamp/switch location parts lists; "
				"printed pages 3-2, 3-4, and 3-8 carry the lamp matrix, switch matrix, and solenoid/flasher/"
				"GI/flipper wiring tables; printed pages 1-13/1-16 carry the switch-matrix addressing "
				"convention and the Bigfoot diagnostic test; PDF page 66 carries the Backbox Assembly parts "
				"breakdown; PDF page 132 carries the Chase Lamp/8-lamp board schematic."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.white-water.switch-locations",
					"locator": "PDF page 104, printed 2-42, Switch Locations parts list",
					"path": "evidence/excerpts/williams.white-water.1993/switch-locations.md",
					"sha256": "c5a03e4ff240404b69fe7a0f33750667bfa51b52e9223a6ab29cc6089b4fdc9c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.switch-matrix",
					"locator": "PDF page 114, printed 3-4, Switch Matrix wiring table",
					"path": "evidence/excerpts/williams.white-water.1993/switch-matrix.md",
					"sha256": "ecfd03dde08a8c9cf68323169dc8b9c2a3db16104977ba48334de08e43866496",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.lamp-locations",
					"locator": "PDF page 102, printed 2-40, Lamp Locations parts list",
					"path": "evidence/excerpts/williams.white-water.1993/lamp-locations.md",
					"sha256": "35a7e458ed7b555a5c409fc5d118fdfe61dd8727dab74cf1b5a3a0a83efc4b9b",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.lamp-matrix",
					"locator": "PDF page 112, printed 3-2, Lamp Matrix wiring table",
					"path": "evidence/excerpts/williams.white-water.1993/lamp-matrix.md",
					"sha256": "d46305621711584725cb313f787167d3a46cf769705c6fd76d22442d7ca3b66c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.solenoid-flasher-locations",
					"locator": "PDF page 103, printed 2-41, Solenoid/Flasher Locations parts list",
					"path": "evidence/excerpts/williams.white-water.1993/solenoid-flasher-locations.md",
					"sha256": "7f6a2e068151adc2ba11c6214bbd2398727849800f7c6ab7b578ede0d334dbd7",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.solenoid-flasher-wiring",
					"locator": "PDF page 118, printed 3-8, Solenoid/Flasher Table, General Illumination, Flipper Circuits",
					"path": "evidence/excerpts/williams.white-water.1993/solenoid-flasher-wiring.md",
					"sha256": "9a1e1e0350f3130990219765acdbe993116d09b47cdc011d09406ed87b646b12",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.chase-lamp-board",
					"locator": "PDF pages 66 and 132, Backbox Assembly parts breakdown and Chase Lamp/8-lamp board schematic",
					"path": "evidence/excerpts/williams.white-water.1993/chase-lamp-board.md",
					"sha256": "95cc596079318f3dea0912da603b6fbe69d8d1df8d644fd903fcaa8cc12523aa",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.white-water.bigfoot-test",
					"locator": "PDF pages 33 and 36, printed 1-13/1-16, switch/lamp addressing convention and T.14 Bigfoot Test",
					"path": "evidence/excerpts/williams.white-water.1993/bigfoot-test.md",
					"sha256": "40555c988e99648086914d0601d4683980fa2c7fc5ee59c8a9a510f3eb2d1a1e",
					"method": "manual",
					"transcribed_by": "curator, read from the retained text layer and cross-checked against the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": HANDBOOK_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.white-water.1993/ipdb/Williams_1993_White_Water_Operators_Handbook.pdf",
			"original_filename": "Williams_1993_White_Water_Operators_Handbook.pdf",
			"sha256": HANDBOOK_SHA256,
			"locator": "15-page Operator's Handbook; consulted for a Bigfoot Mech. Assembly parts reference. Contributes no fact not already established with better provenance by the main manual.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/white-water/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription index for every rendered manual table used by this "
				"definition, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/williams.white-water.1993/. The retained manual carries "
				"a real text layer, but Section 2/3 tables scramble under column-aware extraction, so this "
				"transcription (and the excerpt files it indexes) is the source of record."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/white-water-1993/source/Whitewater%20%28Williams%201993%29.vpx",
			"original_filename": "Whitewater (Williams 1993).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working recreation of the physical machine by Flupper (VPX version 10.x), "
				f"header-dated for IPDB No. 2768, January 1993. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/952 and y/2092. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "Flupper",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/white-water-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (95,093 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "ww_lh6", Const UseSolenoids = 1, Const UseLamps = 0, Const UseSync = 0, the '
				"SolCallback/SolModCallback table for solenoids 1-9, 15-26, and 31, the Controller.Switch "
				"and vpmTimer.PulseSw switch semantics for the trough/whirlpool/lockup/Bigfoot state "
				"machines, UpdateGI dispatching public GI addresses 0-2 to GIUpperFade/GIMiddleFade/"
				"GILowerFade with no case for addresses 3/4, LampTimer_Timer's per-address special cases for "
				"lamps 12, 13, 17, 52, 55, and 71-76, and the BigTimer_Timer 96-step Bigfoot head-position "
				"state machine setting switches 86/87 at steps 24, 45, 72, and 7."
			),
			"license": "NOASSERTION",
			"attribution": "Flupper (VPX table authors)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/white-water-1993/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} "
				f"files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. "
				f"Bounds are {TABLE_BOUNDS}."
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
		"board": "WPC Fliptronic CPU board",
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
				wiring={"board": "WPC Fliptronic CPU board", "drive_wire": wire, "drive_connection": connection},
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
			part_number = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed with A-14315 (LED)/A-14316 (Trans) or 5490-12451-00 opto/proximity "
					"construction; PinMAME's wwGameData inverted-switch mask (column 6 = 0xbf, column 8 = "
					"0x60) covers it, so the public switch state is already normalized and must not be "
					"inverted again."
				)
			if address == 24:
				notes += " Physical part A-8630 is a permanently closed link used to prove the matrix is connected."
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
				if address in {13, 14, 21, 22, 23}:
					role = {
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
						23: "cabinet.service",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address == 13 else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, None, "SW-1A-193", None, True),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "5490-12451-00", True),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, None, "SW-1A-193", None, True),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "5490-12451-00", True),
		115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "used", False, None, "SW-1A-193", None, True),
		116: ("Upper Right Flipper Button", "flipper.upper.right.button", "used", True, "opto", None, "5490-12451-00", True),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, True),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None, True),
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
				" White Water has no upper-left flipper: the Switch Locations parts list (page 2-42) has "
				"no F7/F8 row at all (no assembly, no part number), the Solenoid/Flasher Locations page "
				"lists only three flipper assemblies (Lower Right, Upper Right, Lower Left), and "
				"wwGameData's own FLIP_SW/FLIP_SOL declarations set only FLIP_L|FLIP_UR. The switch-matrix "
				"wiring page nonetheless prints the generic F7/F8 column template."
			)
			physical["location"] = "not installed"
		elif switch_type == "opto":
			notes += (
				" Printed as an opto/proximity sensor (5490-12451-00, the same part used by Bigfoot Opto "
				"1/2). WPC Fliptronic reads the flipper column with an unconditional hardware complement, "
				"so the public switch state is already normalized."
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
			extra["wiring"] = {"board": "WPC Fliptronic CPU board", "drive_wire": wire, "drive_connection": connection}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			extra["normally_closed"] = bool(normally_closed)
			extra["spatial"] = not_applicable(
				"cabinet_or_service" if role.endswith(".button") else "internal_nonvisual",
				MANUAL_SOURCE,
			)
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
					"location": "WPC CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC CPU-board country/option configuration DIP bank. The retained transcription of "
						"this manual does not include the per-country switch-combination chart, so no "
						"specific ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


AUX_LAMP_ADDRESSES = tuple(range(91, 99)) + tuple(range(101, 109))


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING.get(address, {})
			if 8 <= address <= 9 or 15 <= address <= 24:
				kind = "flasher"
			elif address in {25, 26}:
				kind = "motor"
			elif address in {27, 28}:
				kind = "control_signal"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})." if fitted else f"Printed Fliptronic upper-left flipper circuit {address:02d}."
			if kind == "flasher":
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" Only the playfield bulb has a playfield placement; backbox bulbs are behind the "
						"translite and are deliberately not given a playfield coordinate."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {35, 36}:
				notes += (
					" Fliptronic upper-left-flipper circuit with no coil or switch part printed; White "
					"Water has no upper-left flipper (wwGameData declares FLIP_SOL(FLIP_L|FLIP_UR) only) "
					"and no other device is wired through this circuit."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48; the printed table has no separate "
					"circuit-number column for these rows (unlike some later WPC manuals), identifying them "
					"only by function and driver-transistor number."
				)
			if address in {33, 34}:
				notes += (
					" wwGameData sets FLIP_SOL(FLIP_UR), so this Fliptronic upper-flipper circuit is "
					"genuinely fitted, driving the mini-playfield's Upper Right Flipper (FL-11630, assembly "
					"A-15843) rather than being repurposed for a non-flipper device."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC power driver board"}
			if wiring_data.get("driver_transistor"):
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
			if wiring_data.get("control_connection"):
				wiring["control_connection"] = wiring_data["control_connection"]
			if wiring_data.get("power_connection"):
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
				if address in {7, 8, 9, 15, 16, 27, 28}:
					extra["roles"] = ["cabinet.backbox" if address != 7 else "cabinet.knocker"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				else:
					coordinate_refs = (VPX_TABLE_SOURCE,) if address not in SOLENOID_PROJECTION_NOTES else (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
					if address in SOLENOID_PROJECTION_NOTES:
						notes += " " + SOLENOID_PROJECTION_NOTES[address]
						physical["notes"] = notes
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *coordinate_refs)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME publishes the first of the WPC J111 general-purpose state bits here; it is meaningful public state but not a separate physical relay on this machine.",
			30: "PinMAME publishes the second of the WPC J111 general-purpose state bits here; it is meaningful public state but not a separate physical relay on this machine.",
			31: 'ww.c does not configure wpc_set_fastflip_addr, so PinMAME mirrors WPC_GILAMPS bit 7 here on White Water. Pinned wpc.c explicitly says this Fliptronic generation has no physical Game-On solenoid because the flippers are ROM controlled. The retained script binds SolCallback(31)="TiltSol" with the comment \'31 for WPC\', which proves the callback is consumed but does not identify a physical relay or other accessory.',
			32: "PinMAME's WPC remap has no fourth J111 state bit; this public address is constant zero and is not a physical relay.",
			37: "Unused WPC-Fliptronic address; this hardware generation has no LPDC board, so core_getSol's 37-44 branch (gated on GEN_WPC95/GEN_WPC95DCS) never serves this address here.",
			38: "Unused WPC-Fliptronic address; see 37.",
			39: "Unused WPC-Fliptronic address; see 37.",
			40: "Unused WPC-Fliptronic address; see 37.",
			41: "Unused WPC-Fliptronic address; see 37.",
			42: "Unused WPC-Fliptronic address; see 37.",
			43: "Unused WPC-Fliptronic address; see 37.",
			44: "Unused WPC-Fliptronic address; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-Fliptronic hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. wwGameData declares custSol = 0.",
		}[address]
		roles = ["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CONTROLLER_SOURCE, CORE_SOURCE) if address not in {31} else (CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
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
			label = LAMP_LABELS.get(address)
			unused = label is None
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES.get(address, (None, None))
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address == 35 or address == 45:
				notes += (
					" The lamp-matrix wiring page (3-2) prints \"Hazzard 4\" at both 35 and 45 -- a genuine "
					"duplicate label on the printed page, not a transcription error."
				)
			if address in {17, 55}:
				notes += (
					" The Lamp Locations parts list (2-40) marks this position \"Not Used\" with every field "
					"blank, but the Lamp Matrix wiring page (3-2) prints a real feature name here and the "
					"retained script's LampTimer_Timer special-cases this exact address by name "
					f"({'upf_yellow_light, Primitive99' if address == 17 else 'upf_red_light, Primitive100'}), "
					"driving a dedicated image-cycling primitive rather than a simple Light object. Two "
					"agreeing sources (the wiring page and the runtime script) resolve the position as "
					"fitted despite the Lamp Locations blank row."
				)
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated start button assembly, sharing its assembly part number with switch 13." if address == 88 else ""
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
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The lamp-locations parts list marks this position Not Used and the lamp-matrix wiring page agrees."
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in (17, 55):
				availability = "used"
				# Both drive a dedicated image-cycling Primitive (Primitive99/Primitive100) rather than a
				# positioned Light object, and both retained primitives sit at raw (0,0) -- a local origin,
				# not a playfield coordinate. Rather than invent a position or a status the schema does not
				# define, the spatial key is omitted entirely (the same allowance Star Trek: The Next
				# Generation's still-unresolved lamps 53/85/86 already established).
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

	for address in AUX_LAMP_ADDRESSES:
		identifier = f"lamp.chase-{address}"
		items.append(
			_device(
				identifier,
				f"Chase Lamp Board Output {address}",
				"lamp",
				"pinmame.output.lamp",
				address,
				"used",
				(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				roles=["cabinet.chase-lamp"],
				physical={
					"quantity": 1,
					"notes": (
						"wwGameData declares hw.lampCol = 2, publishing this second lamp column; the "
						"retained script's ww_wpc_w handler shifts a 16-bit register serially in from "
						"WPC_SOLENOID1 (solenoids 27 'Chase Lamp Clock'/28 'Chase Lamp Data') and writes it "
						"to coreGlobals.tmpLampMatrix[8]/[9], publishing addresses 91-98 and 101-108. The "
						"Backbox Assembly parts breakdown (PDF page 66) lists both the A-15761 Chase Light "
						"PC Board and two A-15765 8-Lamp Board Assemblies as backbox items; the retained VPX "
						"table's InsertLights collection has no member for any of these sixteen addresses, "
						"so this recreation does not model their individual bulbs. There is no printed "
						"evidence for which physical byte (low/high) feeds which of the two 8-lamp boards, "
						"so the sixteen addresses are enumerated generically rather than split into "
						"unsubstantiated Left/Right groups."
					),
				},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, wire, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC power driver board",
				"control_connection": drive_connection,
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
				"coordinate come from the retained table's GI emitter collections for this string "
				"(UpdateGI in the retained script). GI address 0 drives collections GIupper plus "
				"GIupperbulbs; GI address 1 drives GImiddle; GI address 2 drives GIlower."
			)
			if address == 1:
				notes += (
					" GImiddle contains 17 members; one (Light2, at normalized x=-0.041783) sits outside "
					"the retained table's playfield bounds and is excluded here as a table modeling "
					"anomaly, and five more (l21b2..l21b6) are brightness-doubling copies of lamp 21 rather "
					"than distinct GI bulbs, leaving 11 placements."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox illumination behind the translite; the retained script's UpdateGI handles only "
				"GI addresses 0-2, so this string has no playfield coordinate, matching the manual's own "
				"wiring table which prints no Playfield connection for this string."
			)
			extra["roles"] = ["cabinet.backbox"]
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
			"Three-position ball trough, outhole, and ball serve",
			"kicker",
			[output_id("Outhole"), output_id("Ball Serve")],
			["switch.matrix-15", "switch.matrix-76", "switch.matrix-77", "switch.matrix-78"],
			"A drained ball enters the merged Drain/Outhole kicker (switch 15); solenoid 1 (Outhole) kicks "
			"it into the three-position trough. Right Trough (76) is nearest the eject end, Center Trough "
			"(77) and Left Trough (78) queue behind it nearest the drain entrance. Solenoid 2 (Ball Serve) "
			"ejects the ball resting at 76 into the shooter lane.",
			[
				("outhole", "Ball in outhole/drain", ["switch.matrix-15"], "Merged drain/outhole kicker."),
				("right", "Right Trough (eject position)", ["switch.matrix-76"], "Ball nearest the ball-serve coil."),
				("center", "Center Trough", ["switch.matrix-77"], "Second trough position."),
				("left", "Left Trough (drain entrance)", ["switch.matrix-78"], "Drain entrance and third trough position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.shooter-lane",
			"Manual plunger shooter lane",
			"other",
			[],
			["switch.matrix-53"],
			"White Water has a manual pull-back plunger (VPX Plunger object); there is no auto-plunger "
			"solenoid in wwGameData. Switch 53 (Ball Shooter) senses the ball resting in the shooter lane.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-53"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.whirlpool",
			"Whirlpool hole, underground tunnel, and popper",
			"kicker",
			[output_id("Whirlpool Popper")],
			["switch.matrix-61", "switch.matrix-62"],
			"A ball that falls into the Whirlpool hole (opto 61) travels an underground tunnel and is "
			"kicked back to the playfield by solenoid 3 at a different, distant location sensed by opto 62 "
			"(Whirlpool Exit) -- the retained script's FallThrough2_Hit handler pulses switch 62 as the "
			"ball re-emerges. Flasher solenoid 22 (Whirlpool Popper) and 23 (Whirlpool Enter) light the "
			"entry and exit locations.",
			[
				("popper", "Ball in Whirlpool hole", ["switch.matrix-61"], "Opto at the Whirlpool entry."),
				("exit", "Ball at Whirlpool tunnel exit", ["switch.matrix-62"], "Opto at the underground tunnel's far end."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15758",
		),
		mechanism(
			"mechanism.lockup",
			"Three-ball lockup lane and popper",
			"kicker",
			[output_id("Lockup Popper")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-65"],
			"A ball enters the lockup lane at Lockup Left (opto 65, outermost), passes Lockup Center (opto "
			"64, which drops a gate: multiballwall65.isDropped = false) and comes to rest at Lockup Right "
			"(opto 63), a physical VPX Kicker held until solenoid 4 (Lockup Popper) kicks it back to the "
			"playfield. The retained script's own inline comment marks this the '*** three ball lock ***'.",
			[
				("left", "Ball entering at Lockup Left", ["switch.matrix-65"], "Outermost lock position."),
				("center", "Ball passing Lockup Center", ["switch.matrix-64"], "Opens the gate toward the popper."),
				("right", "Ball held at Lockup Right", ["switch.matrix-63"], "Popper kicker position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15769",
		),
		mechanism(
			"mechanism.bigfoot-head",
			"Rotating Bigfoot head and drive motor",
			"motorized",
			[output_id("Bigfoot Drive"), output_id("Bigfoot Enable")],
			["switch.matrix-86", "switch.matrix-87"],
			"A DC gearmotor rotates the Bigfoot figure on the mini-playfield through a 96-step cycle. "
			"Solenoid 25 (Bigfoot Drive) pulses one motor step per pulse; solenoid 26 (Bigfoot Enable) sets "
			"the rotation direction. Two head-position optos (86 'Bigfoot Opto 1', 87 'Bigfoot Opto 2') "
			"report a coarse 2-bit position code. The retained script's BigTimer_Timer sets switches 86/87 "
			"at four named 96-step positions: step 24 sets {86=1,87=0} ('Left'/Diverter), step 45 sets "
			"{86=0,87=1} ('Up'), step 72 sets {86=0,87=0} ('Right'/Unknown), and step 7 sets {86=1,87=1} "
			"('Down'/Player); pinned PinMAME's own ww_handleMech instead derives the same two bits directly "
			"from a 7-bit locals.bigfootPos counter as (bigfootPos/32+1) & {0x02,0x01} -- a different "
			"resolution (128 steps in 4 quadrants) of the identical two-sensor hardware. The manual's own "
			"T.14 Bigfoot Test independently names the two sensors 'Opto 1'/'Opto 2' and confirms a single "
			"reversible drive motor with named head positions, matching this structure.",
			[
				("left-diverter", "Head position: Left / Diverter", ["switch.matrix-86"], "Script step 24: {86=1, 87=0}."),
				("up", "Head position: Up", ["switch.matrix-87"], "Script step 45: {86=0, 87=1}."),
				("right-unknown", "Head position: Right / Unknown", [], "Script step 72: {86=0, 87=0}."),
				("down-player", "Head position: Down / Player", ["switch.matrix-86", "switch.matrix-87"], "Script step 7: {86=1, 87=1}."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15573",
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Canyon ramp diverter",
			"diverter",
			[output_id("Ramp Diverter")],
			[],
			"Solenoid 6 (Ramp Diverter) routes a ball entering the Canyon ramp between two downstream "
			"paths. Pinned PinMAME's own ww_handleBallState checks core_getSol(sDiverter) directly to "
			"choose between its two simulated ramp-continuation states, and the retained script's SolDiv "
			"handler animates a companion playfield flap object in step with the coil.",
			[],
			CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15573",
		),
		mechanism(
			"mechanism.kickback",
			"Left outlane kickback",
			"kicker",
			[output_id("Kickback")],
			["switch.matrix-25"],
			"A ball that drains down the Left Outlane (switch 25) can be returned to play by solenoid 5 "
			"(Kickback); the retained script's Kickback_Hit handler fires the kicker only while it is "
			"enabled by the SolKick callback.",
			[("outlane", "Ball in left outlane", ["switch.matrix-25"], "Left outlane switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-11873",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Sling"), output_id("Right Sling")],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot carries a kick switch (SW-1A-114) and a separate scored switch (SW-1A-120) with "
			"a diode across it. The retained script's LeftSlingShot_Slingshot/RightSlingShot_Slingshot "
			"handlers pulse matrix addresses 51/52 and fire coils 10/11 in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15749",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Center Jet Bumper")],
			["switch.matrix-16", "switch.matrix-17", "switch.matrix-18"],
			"Three A-9415-2 jet bumpers. The retained script's Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit "
			"handlers pulse switches 16, 17, and 18 and fire coils 12, 13, and 14 respectively, matching "
			"printed Left/Right/Center Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-16"], "First bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-17"], "Second bumper of the nest."),
				("center", "Center jet bumper", ["switch.matrix-18"], "Third bumper of the nest."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
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
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold "
			"winding: the ROM energizes the power winding on the cabinet button opto (112 right, 114 "
			"left), then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 "
			"left) closes.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 right with A-15205-L-2 left",
		),
		mechanism(
			"mechanism.upper-right-flipper",
			"Upper right (mini-playfield) flipper",
			"other",
			[output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold")],
			["switch.generic-115", "switch.generic-116"],
			"A single FL-11630 flipper on the mini-playfield near the Bigfoot mechanism, genuinely fitted "
			"(wwGameData sets FLIP_SOL(FLIP_UR)); driven by cabinet button opto 116 and end-of-stroke "
			"switch 115, the same Fliptronic power/hold pattern as the lower flippers. Unlike some other "
			"WPC games, White Water has no upper-left flipper, so this is the mini-playfield's only "
			"flipper.",
			[("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button opto 116 and end-of-stroke switch 115.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15843",
		),
		mechanism(
			"mechanism.chase-lamp-board",
			"Backbox chase-lamp animation",
			"other",
			[output_id("Chase Lamp Clock"), output_id("Chase Lamp Data")],
			[],
			"Solenoids 27/28 clock a 16-bit value serially into the A-15761 Chase Light PC Board, which "
			"drives two backbox-mounted A-15765 8-lamp boards (16 #194 bulbs total). PinMAME publishes the "
			"resulting state at lamp addresses 91-98 and 101-108 (wwGameData's hw.lampCol = 2). The Backbox "
			"Assembly parts breakdown lists both boards among the CPU/sound/power-driver backbox hardware, "
			"confirming the placement; no printed source names an individual bulb.",
			[],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15761",
		),
		mechanism(
			"mechanism.knocker",
			"Cabinet knocker",
			"other",
			[output_id("Knocker")],
			[],
			"Solenoid 7 pulses a cabinet-mounted knocker (B-10686-1) on award/replay events; the retained "
			"script's SolCallback(7) plays the knocker sound effect.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="B-10686-1",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.whirlpool-tunnel-exit",
			"kind": "pulse",
			"source": "switch.matrix-61",
			"destination": "switch.matrix-62",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	# The switch-matrix opto polarity sweep (every address in OPTO_SWITCHES, checked against
	# wwGameData's inverted-switch mask column by column) found zero disagreement: the manual's nine
	# opto/proximity addresses (61-65, 66, 68, 86, 87) are exactly the nine addresses PinMAME's mask
	# normalizes, matching the same clean result already established for Bally Kiss, Bally The
	# Addams Family, and Williams Star Trek: The Next Generation.
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
			"id": "williams.white-water.1993",
			"name": "White Water",
			"manufacturer": "Williams",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 2768,
			"opdb_id": "GRQKz-MyNXz",
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
		"knowledge": {"path": "knowledge/williams/white-water.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"White Water device identifiers are not unique: {duplicates}")
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
	unresolved_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
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
		"status": "candidate",
		"blockers": [
			"Lamps 17 (Lights Whirlpool) and 55 (Whirlpool Lit) drive dedicated image-cycling Primitive "
			"objects rather than positioned Light objects, and both retained primitives sit at a raw local "
			"origin (0,0) rather than a playfield coordinate, so no position is asserted for either address; "
			"see the unresolved list below. This is the only outstanding gap -- every other dimension this "
			"report audits, including the switch-matrix opto polarity sweep, is complete and validated "
			"with zero disagreement.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2092.0},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2092; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/white-water-1993/extracted-vpxtool.manifest.json",
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
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTION_NOTES.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.white-water.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/white-water/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"GImiddle member Light2 (normalized x=-0.041783, outside the 0..1 playfield bounds) -- table modeling anomaly, not a distinct physical bulb",
			"GImiddle members l21b2..l21b6 -- brightness-doubling copies of lamp 21, not distinct GI bulbs",
			"Flasherlight21/FlasherFlash21 helper objects (both outside the 0..1 playfield bounds); solenoid 21's placement uses the positioned Flasher16 object the same routine also toggles",
		],
		"unresolved": [
			{
				"group": binding["group"],
				"address": binding["address"],
				"reason": (
					"Drives a dedicated image-cycling Primitive (Primitive99 for lamp 17, Primitive100 for "
					"lamp 55) rather than a positioned Light object; both retained primitives sit at raw "
					"(0,0), a local origin rather than a playfield coordinate, so no position is asserted."
				),
			}
			for binding in sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"]))
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# White Water (Williams, 1993) spatial review",
		"",
		f"Status: {report['status']}. Two lamp addresses (17, 55) have no resolvable playfield coordinate "
		"and are listed under Unresolved placements below; every other spatial dimension audited here is "
		"complete. The physical machine record itself remains `partial` at "
		"`machines/partial/williams/white-water-1993.json` for that reason alone -- every other coverage "
		"dimension, including the switch-matrix opto polarity sweep, is validated with zero disagreement; "
		"see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Whitewater (Williams 1993).vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and y/2092 rounded to at "
		"most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual carries a real text layer, but its Section 2/3 tables scramble under "
		"column-aware `pdftotext -layout` extraction, so every printed table used here was read from "
		"200 dpi renders and transcribed by hand into "
		"`external:pinmame-review-artifacts/white-water/manual-transcription.md` and the excerpt files it "
		"indexes.",
		"- Switches 86/87 (the Bigfoot head-position optos) have no dedicated playfield trigger object: "
		"the retained script sets them directly from an internal motor-step counter, matching pinned "
		"PinMAME's own ww_handleMech. Both are documented projections onto the Bigfoot figure's own "
		"retained primitive.",
		"- Solenoids 25/26 (Bigfoot Drive/Enable) project onto the same Bigfoot figure primitive for the "
		"same reason. Solenoid 21 (Insanity Falls flasher) uses the one positioned Flasher object "
		"(Flasher16) that its own script routine also toggles, because its dedicated helper objects "
		"(Flasherlight21/FlasherFlash21) sit outside the retained table's playfield bounds.",
		"- GImiddle member Light2 sits at normalized x=-0.041783, outside the retained table's 0..1 "
		"playfield bounds, and is excluded as a table modeling anomaly; five more GImiddle members "
		"(l21b2..l21b6) are lamp-21 brightness doublers, not distinct GI bulbs, leaving 11 placements for "
		"GI address 1.",
		"- GI strings 3 and 4 (Backglass Boat, Backglass Sky) print no Playfield connection at all on the "
		"solenoid/flasher wiring page, and the retained script's UpdateGI has no case for public GI "
		"addresses 3/4 -- full agreement between the manual and the runtime script -- so both take a "
		"controlled `cabinet_or_service` record.",
		"- The sixteen auxiliary lamp addresses (91-98, 101-108) published through wwGameData's "
		"`hw.lampCol = 2` are backbox chase-lamp hardware per the Backbox Assembly parts breakdown; the "
		"retained table does not model their individual bulbs, so all sixteen take a controlled "
		"`cabinet_or_service` record with no fabricated coordinate.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with "
		"both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group'].rsplit('.', 1)[-1].capitalize()} {entry['address']}: {entry['reason']}")
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
	if report["unresolved"]:
		lines += ["", "## Unresolved placements", ""]
		for entry in report["unresolved"]:
			lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every authoring-critical placement, quantity, and semantic question is resolved for the "
		"addresses this audit covers except one: lamps 17 and 55 drive dedicated image-cycling "
		"primitives that sit at a raw local origin rather than a playfield coordinate, so neither has an "
		"asserted position. The switch-matrix opto polarity sweep found zero disagreement (every address "
		"in `OPTO_SWITCHES` is covered by `wwGameData`'s inverted-switch mask), so `conflicts` is empty and "
		"`coverage.dimensions.physical_wiring = \"validated\"`. The deterministic curator reproduces the "
		"canonical artifact and its pinned seed byte-for-byte, but the unpositioned lamp pair is still an "
		"authoring-relevant gap, so promotion to `author_ready` is refused; the record stays `partial` "
		"with `coverage.missing = [\"spatial_placement\"]` until a positioned proxy for lamps 17/55 is "
		"established.",
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
		raise RuntimeError(f"Stale White Water author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"White Water definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"White Water seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"White Water definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"White Water seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"White Water spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"White Water spatial review drifted from its deterministic curator: {markdown_path}")
	print("White Water definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"White Water extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("White Water retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
