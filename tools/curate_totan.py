"""Curate the physical Williams Tales of the Arabian Nights (1996) machine definition.

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
# GI address 2 (printed String 3) is documented backbox-only by the manual's own wiring table, but
# the retained script's Sub UpdateGI binds ONLY that address to a broad playfield-wide dimming effect
# while the manual's two genuine playfield strings (addresses 3 and 4) receive no script binding at
# all (conflict.gi-string-3-playfield-binding, unresolved), so the record lives under machines/partial.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/tales-of-the-arabian-nights-1996.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/tales-of-the-arabian-nights-1996.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/tales-of-the-arabian-nights-1996.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/tales-of-the-arabian-nights-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/tales-of-the-arabian-nights-1996.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.tales-of-the-arabian-nights.1996"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.tales-of-the-arabian-nights.1996"
VPX_TABLE_SOURCE = "vpx-table.totan-jpsalas-flupper-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.totan-jpsalas-flupper-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.totan-jpsalas-flupper-1-0"

TABLE_SHA256 = "487375925e6f44998cd416b6d28983f08144d2bfe7a1432ac9ad16af7b23fec0"
SCRIPT_SHA256 = "c4a742f2188c9e3dcba70a7717d5b8985bbd1d913cc05c17df3b2f9d341b876b"
MANUAL_SHA256 = "ac5120a92c71108baf77ec33b8687e1ae35e633d9d390b64149cca3ba0821357"
MANUAL_TRANSCRIPTION_SHA256 = "fd33e241ed3715c93213ced0f051df1a72a1d042eb9dda0536273eb3b84ac176"

EXTRACTION_RELATIVE_PATH = Path("williams/tales-of-the-arabian-nights-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/tales-of-the-arabian-nights-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "761846f3369203502a9083c19e46a0da046893a46df43abc734a53c61b19a04d"
EXTRACTION_FILE_COUNT = 944
EXTRACTION_TOTAL_BYTES = 128702095

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2164"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2164.0

DRIVER_IDS = ("totan_04", "totan_12", "totan_13", "totan_14", "totan_15c")
DRIVER_COMPATIBILITY = {
	"totan_04": (
		"identical",
		"Williams 0.4 prototype game ROM for the same physical Tales of the Arabian Nights machine; the "
		"switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged.",
	),
	"totan_12": (
		"identical",
		"Williams 1.2 game ROM; an earlier production firmware revision of the same physical machine with "
		"no controller-address or playfield change.",
	),
	"totan_13": (
		"identical",
		"Williams 1.3 game ROM; a later production firmware revision of the same physical machine with no "
		"controller-address or playfield change.",
	),
	"totan_14": (
		"identical",
		"Williams production 1.4 game ROM shipped with the physical machine. This is the driver the "
		"retained known-working table binds to (cGameName = \"totan_14\").",
	),
	"totan_15c": (
		"compatible",
		"Community \"Competition MOD\" 1.5C ruleset ROM (2016) built on the 1.4/S1.1 codebase; it runs on "
		"the same documented physical hardware and controller addresses as the production driver, changing "
		"only rules/scoring, so it remains a driver variant of the physical machine rather than a distinct "
		"game.",
	),
}

# --- Printed switch matrix (manual printed 2-38 wiring page, 2-39 parts list).
SWITCH_LABELS = {
	11: "Harem Passage", 12: "Vanish Tunnel", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Ramp Enter", 16: "Left Outlane", 17: "Right Inlane", 18: "Ball Shooter",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Genie Standup Target", 24: "Always Closed",
	25: "Bazaar Eject", 26: "Left Inlane", 27: "Right Outlane", 28: "Left Wire Make",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Left Cage Opto", 37: "Right Cage Opto", 38: "Left Eject",
	41: "Ramp Made Left", 42: "Genie Target", 43: "Left Loop", 44: "Inner Loop Left",
	45: "Inner Loop Right", 46: "Mini Standups", 47: "Ramp Made Right", 48: "Right Captive Ball",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Left Jet Bumper", 54: "Right Jet Bumper",
	55: "Middle Jet Bumper", 56: "Lamp Spin CCW", 57: "Lamp Spin CW", 58: "Left Captive Ball",
	61: "Left Standups", 62: "Right Standups", 63: "Top Skill Shot", 64: "Middle Skill Shot",
	65: "Bottom Skill Shot", 66: "Lock 1 (Bottom)", 67: "Lock 2 (Middle)", 68: "Lock 3 (Top)",
}
# Printed matrix columns 7 and 8 (all rows) are marked "NOT USED" on both the switch matrix (2-38) and
# the switch-locations parts list ("71 to 88 Not Used", 2-39).
UNUSED_MATRIX_ADDRESSES = {71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# Every switch shaded "OPTO, TYPICALLY CLOSED" on the printed matrix page (2-38): matrix column 3, rows
# 1-7 (addresses 31-37). Confirmed against the parts list (2-39): 31-35 use A-18617-1 LED/A-18618-1
# photo transistor, 36/37 use A-16908 LED/A-16909 photo transistor; every other fitted switch in the
# matrix uses a mechanical part number. Address 38 (row 8, same column) is A-17985-R, not an opto.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37}
# PinMAME's totanGameData inverted-switch mask index 3 (matrix column 3) is 0x7f: bits 0-6 set = rows
# 1-7 = addresses 31-37, exactly the printed opto set. Zero disagreement between the manual and PinMAME.
PINMAME_NORMALIZED_OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37}
# vpmTimer.PulseSw / momentary callers in the retained script.
PULSED_SWITCHES = {12, 15, 16, 17, 18, 23, 26, 27, 28, 31, 41, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65}

SWITCH_TYPES = {
	11: "microswitch", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch",
	23: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	28: "microswitch", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto",
	36: "opto", 37: "opto", 38: "microswitch",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch", 45: "microswitch",
	46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "leaf", 52: "leaf", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "leaf", 57: "leaf", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch",
	66: "microswitch", 67: "microswitch", 68: "microswitch",
}

# address -> (assembly_part_number / opto assembly, switch part number), transcribed from printed 2-39.
SWITCH_PARTS = {
	11: ("A-12238", None), 12: ("A-12238", None), 13: (None, "20-9663-1"),
	14: (None, "04-10346"), 15: (None, "5647-12693-36"),
	16: (None, "A-16443"), 17: (None, "A-17813"), 18: (None, "A-20842"),
	21: (None, "A-17238"), 22: (None, "5643-09268-00"),
	23: (None, "A-18530-6"), 24: (None, "5643-09112-00"),
	25: (None, "5647-12693-13"), 26: (None, "A-17813-1"), 27: (None, "A-16443"),
	28: (None, "5647-12693-21"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16908 LED with A-16909 photo transistor", None),
	37: ("A-16908 LED with A-16909 photo transistor", None),
	38: (None, "A-17985-R"),
	41: ("A-12238", None), 42: ("SW-1A-207 (left) with SW-1A-208 (right)", None),
	43: (None, "A-17813"), 44: (None, "A-17813"), 45: (None, "A-17813"),
	46: (None, "A-18017-6"), 47: ("A-12238", None), 48: (None, "A-18530-6"),
	51: (None, "A-17800 (kick) with A-17793 (score)"), 52: (None, "A-17800 (kick) with A-17793 (score)"),
	53: (None, "A-16443"), 54: (None, "A-16443"), 55: (None, "A-16443"),
	56: (None, "SW-1A-206"), 57: (None, "SW-1A-206"), 58: (None, "A-18530-6"),
	61: (None, "A-20846-9 (top), A-20499-9 (middle), A-20499-9 (bottom)"),
	62: (None, "A-20846-9 (top), A-20499-9 (middle), A-20499-9 (bottom)"),
	63: (None, "SW-1A-202-15"), 64: (None, "SW-1A-202-15"), 65: (None, "SW-1A-202-15"),
	66: (None, "A-17985-R"), 67: (None, "A-14820"), 68: (None, "A-14820"),
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
# Fliptronic F1-F8 wiring, printed 2-38.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed solenoid/flasher table (manual printed 2-40 wiring, 2-41 locations).
SOLENOID_LABELS = {
	1: "Left Cage", 2: "Right Cage", 3: "Vanish Drop", 4: "Lock Eject", 5: "Bazaar Eject",
	6: "Lock Magnet", 7: "Knocker", 8: "Ramp Magnet Coil", 9: "Trough Eject",
	10: "Left Slingshot", 11: "Right Slingshot", 12: "Left Jet Bumper", 13: "Right Jet Bumper",
	14: "Middle Jet Bumper", 15: "Left Kicker", 16: "Left Eject Flasher", 17: "Inlane Flashers",
	18: "Final Battle Flasher", 19: "Left Loop Flasher", 20: "Bazaar Flasher", 21: "Ramp Diverter",
	22: "Rub Lamp Flasher", 23: "Magic Lamp Flashers", 24: "Right Loop Flasher",
	25: "Start Tale Flashers", 26: "Jet Flashers", 27: "Top Loop Flasher", 28: "Ramp Flasher",
	33: "Left Diverter Power", 34: "Left Diverter Hold", 35: "Vanish Magnet", 36: "Loop Post Diverter",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-95 LPDC Output 37", 38: "Unused WPC-95 LPDC Output 38",
	39: "Unused WPC-95 LPDC Output 39", 40: "Unused WPC-95 LPDC Output 40",
	41: "Unused WPC-95 LPDC Mirror 41", 42: "Unused WPC-95 LPDC Mirror 42",
	43: "Unused WPC-95 LPDC Mirror 43", 44: "Unused WPC-95 LPDC Mirror 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
for _n in range(51, 65):
	VIRTUAL_SOLENOID_LABELS[_n] = f"Unused Custom-Solenoid Position {_n}"
# Manual solenoid/flasher table addresses that differ from the PinMAME public address. Printed 29-32 are
# NOT public addresses (CORE_FIRSTLFLIPSOL=45): printed 29 -> public 45, 30 -> 46, 31 -> 47, 32 -> 48.
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}

# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(control_connection="J116-1", driver_transistor="Q72", power_connection="J133-2", part_number="A-20099", printed_type="High Power"),
	2: dict(control_connection="J116-2", driver_transistor="Q68", power_connection="J133-2", part_number="A-20099", printed_type="High Power"),
	3: dict(control_connection="J116-4", driver_transistor="Q71", power_connection="J133-2", part_number="FL-11753", printed_type="High Power"),
	4: dict(control_connection="J116-5", driver_transistor="Q67", power_connection="J133-2", part_number="AE-27-1200", printed_type="High Power"),
	5: dict(control_connection="J116-6", driver_transistor="Q70", power_connection="J133-2", part_number="AE-25-1000", printed_type="High Power"),
	6: dict(control_connection="J116-7", driver_transistor="Q66", power_connection="J133-2", part_number="20-10197", printed_type="High Power"),
	7: dict(control_connection="J116-8", driver_transistor="Q69", power_connection="J133-2", part_number="AE-23-800", printed_type="High Power"),
	8: dict(control_connection="J116-9", driver_transistor="Q65", power_connection="J133-1", part_number="20-10179", printed_type="High Power"),
	9: dict(control_connection="J113-1", driver_transistor="Q44", power_connection="J133-3", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(control_connection="J113-3", driver_transistor="Q48", power_connection="J133-3", part_number="AE-27-1200", printed_type="Low Power"),
	11: dict(control_connection="J113-4", driver_transistor="Q43", power_connection="J133-3", part_number="AE-27-1200", printed_type="Low Power"),
	12: dict(control_connection="J113-5", driver_transistor="Q47", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J113-6", driver_transistor="Q42", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J113-7", driver_transistor="Q46", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J113-8", driver_transistor="Q41", power_connection="J133-3", part_number="AE-27-1200", printed_type="Low Power"),
	16: dict(control_connection="J113-9", driver_transistor="Q45", power_connection="J133-6", printed_type="Low Power"),
	17: dict(control_connection="J111-1", driver_transistor="Q28", power_connection="J133-6", printed_type="Flasher"),
	18: dict(control_connection="J111-2", driver_transistor="Q32", power_connection="J133-6", printed_type="Flasher"),
	19: dict(control_connection="J111-3", driver_transistor="Q27", power_connection="J133-6", printed_type="Flasher"),
	20: dict(control_connection="J111-4", driver_transistor="Q31", power_connection="J133-6", printed_type="Flasher"),
	21: dict(control_connection="J111-5", driver_transistor="Q26", power_connection="J133-2", part_number="AE-30-2000", printed_type="Low Power"),
	22: dict(control_connection="J111-6", driver_transistor="Q30", power_connection="J133-6", printed_type="Flasher"),
	23: dict(control_connection="J111-7", driver_transistor="Q25", power_connection="J133-6", printed_type="Flasher"),
	24: dict(control_connection="J111-8", driver_transistor="Q29", power_connection="J133-6", printed_type="Flasher"),
	25: dict(control_connection="J109-1", driver_transistor="Q16", power_connection="J133-6", printed_type="Gen. Purpose"),
	26: dict(control_connection="J109-2", driver_transistor="Q15", power_connection="J133-6", printed_type="Gen. Purpose"),
	27: dict(control_connection="J109-3", driver_transistor="Q14", power_connection="J133-6", printed_type="Gen. Purpose"),
	28: dict(control_connection="J109-4", driver_transistor="Q13", power_connection="J133-6", printed_type="Gen. Purpose"),
	33: dict(control_connection="J120-6", driver_transistor="Q84", power_connection="J119-6", part_number="FL-11753", printed_type="Fliptronic power"),
	34: dict(control_connection="J120-4", driver_transistor="Q86", power_connection="J119-6", printed_type="Fliptronic hold"),
	35: dict(control_connection="J120-3", driver_transistor="Q81", power_connection="J119-8", part_number="20-10197", printed_type="Fliptronic power"),
	36: dict(control_connection="J120-1", driver_transistor="Q83", power_connection="J119-8", part_number="AE-27-1200", printed_type="Fliptronic hold"),
	45: dict(control_connection="J120-13", driver_transistor="Q90", power_connection="J119-1", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(control_connection="J120-11", driver_transistor="Q92", power_connection="J119-1", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(control_connection="J120-9", driver_transistor="Q87", power_connection="J119-4", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(control_connection="J120-7", driver_transistor="Q89", power_connection="J119-4", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "YEL-GRN", 46: "ORG-GRN", 47: "YEL-BLU", 48: "ORG-BLU", 33: "YEL-VIO", 34: "ORG-VIO", 35: "YEL-GRY", 36: "ORG-GRY"}

SOLENOID_ASSEMBLIES = {
	1: "A-20693", 2: "A-20693", 3: "A-20644", 4: "B-9362-L-3", 5: "A-16434-2",
	8: "A-20839", 9: "A-19963-1", 10: "B-9362-L-3", 11: "B-9362-L-3", 12: "A-9415-2",
	13: "A-9415-2", 14: "A-9415-2", 15: "B-9362-L-3", 16: "A-17983 (2)", 17: "A-17983 (2)",
	18: "A-17802", 19: "A-17802", 20: "A-17983", 21: "A-20626", 22: "A-17802", 23: "A-17802",
	24: "A-17802", 25: "A-17802", 26: "A-17802", 27: "A-17802", 28: "A-17802",
	33: "A-20642", 34: "A-20642", 35: "A-20644", 36: "A-17932-1",
	45: "A-14876-R-3", 46: "A-14876-R-3", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
# Retained VPW... (community) script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "SolSpikerLeft", 2: "SolSpikerRight", 3: "SolVanishDrop", 4: "SolLockRelease",
	5: "SolBazaarKick", 6: "SolLockMagnet", 7: 'vpmSolSound SoundFX("fx_Knocker",DOFKnocker)',
	8: "SolRampMagnet", 9: "SolRelease", 15: "SolLeftKicker", 21: "RampDiverter",
	16: "SolModCallback(16) = SetModLamp 116", 17: "SolModCallback(17) = SetModLamp 117",
	18: "SolModCallback(18) = SetModLamp 118", 19: "SolModCallback(19) = SetModLamp 119",
	20: "SolModCallback(20) = SetModLamp 120", 22: "SolModCallback(22) = SetModLamp 122",
	23: "SolModCallback(23) = SetModLamp 123", 24: "SolModCallback(24) = SetModLamp 124",
	25: "SolModCallback(25) = SetModLamp 125", 26: "SolModCallback(26) = SetModLamp 126",
	27: "SolModCallback(27) = SetModLamp 127", 28: "SolModCallback(28) = SetModLamp 128",
	34: "SolPlayFDiv (address 33 unscripted; shares the same physical diverter coil pair)",
	35: "SolVanishMagnet", 36: "SolLoopDiv",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
}

FLASHER_BULBS = {
	16: ("#89 (2) on the playfield and #906 (1) on the insert panel", 3, 2),
	17: ("#89 (2) on the playfield", 2, 2),
	18: ("#906 (1) on the playfield", 1, 1),
	19: ("#906 (1) on the playfield", 1, 1),
	20: ("#89 (1) on the playfield", 1, 1),
	22: ("#906 (1) on the playfield", 1, 1),
	23: ("#906 (1) on the playfield", 1, 1),
	24: ("#906 (1) on the playfield", 1, 1),
	25: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	26: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	27: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	28: ("#906 (1) on the playfield", 1, 1),
}

# --- Printed lamp matrix (manual printed 2-36 wiring, 2-37 locations). First digit is the column.
LAMP_LABELS = {
	11: "Jewel 1 (Left)", 12: "Jewel 2", 13: "Jewel 3", 14: "Jewel 4", 15: "Jewel 5",
	16: "Jewel 6", 17: "Jewel 7 (Right)", 18: "Shoot Again",
	21: "Jackpot", 22: "(G)enie", 23: "G(E)nie", 24: "Ge(N)ie", 25: "Gen(I)e", 26: "Geni(E)",
	27: "Multiball", 28: "Outlane Special",
	31: "Magic Carpet", 32: "Action 3", 33: "Ramp Arrow Right", 34: "Ramp Arrow Left",
	35: "Smoke 1 (Bottom)", 36: "Smoke 2", 37: "Smoke 3", 38: "Amulet",
	41: "Smoke 6", 42: "Smoke 7", 43: "Smoke 8", 44: "Smoke 9", 45: "Smoke 10",
	46: "Smoke 11", 47: "Smoke 12", 48: "Smoke 13",
	51: "Smoke 14 (Top)", 52: "Lamp-15", 53: "Lamp-30", 54: "Lamp-60", 55: "Smoke 4",
	56: "Smoke 5", 57: "Shoot Star Right", 58: "Shoot Star Left",
	61: "Make A Wish", 62: "(B)azaar", 63: "B(A)zaar", 64: "Ba(Z)aar", 65: "Baz(A)ar",
	66: "Baza(A)r", 67: "Bazaa(R)", 68: "Center Lock",
	71: "Action 2", 72: "Left Lock", 73: "Harem Advance", 74: "Left Tiger Loop", 75: "Action 1",
	76: "Wish 1", 77: "Wish 2", 78: "Wish 3",
	81: "Extra Ball", 82: "Action 5", 83: "Right Lock", 84: "Right Tiger Loop",
	85: "Captive Ball Right", 86: "Action 4", 87: "Captive Ball Left", 88: "Start Button",
}
LAMP_BULBS = {
	18: "#44", 27: "#44", 28: "#44", 38: "#44", 58: "#44", 68: "#44", 86: "#44", 87: "#44",
}
LAMP_QUANTITIES = {28: 2}
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
# Co-located "LightNN"/"f1"/"f16" objects stacked purely for brightness (max pairwise distance under 38
# raw units, i.e. well under 4% of playfield width, at every address except 28); the primary "lNN"
# object is used and the duplicate is documented render doubling.
LAMP_RENDER_DOUBLES = set(range(11, 19)) | {21, 22, 23, 24, 25, 26, 27} | set(range(32, 39)) | \
	set(range(41, 49)) | set(range(51, 59)) | set(range(61, 69)) | set(range(71, 79)) | set(range(81, 88))
LAMP_RENDER_DOUBLES -= {28}

GI_STRINGS = {
	0: ("Illumination String 1", "J106-1", "Q5", "J106-7", "#44"),
	1: ("Illumination String 2", "J106-2", "Q4", "J106-8", "#44"),
	2: ("Illumination String 3", "J106-3", "Q3", "J106-9", "#44"),
	3: ("Illumination String 4", "J105-5", "Q2", "J105-10", "#555"),
	4: ("Illumination String 5", "J105-6 and J104-3", "Q1", "J105-11 and J104-1", "#555"),
}

# --- Normalized playfield coordinates derived from the retained VPX extraction (x/952, y/2164;
# vpx-geometry.txt is the full transcription of this dump).
SWITCH_POSITIONS = {
	11: [(0.486966, 0.062083)], 12: [(0.405323, 0.227388)], 15: [(0.228992, 0.244801)],
	16: [(0.057706, 0.807508)], 17: [(0.778416, 0.729398)], 18: [(0.943919, 0.899145)],
	23: [(0.488971, 0.128466)], 25: [(0.713456, 0.402253)], 26: [(0.133694, 0.729011)],
	27: [(0.853514, 0.808432)], 28: [(0.157313, 0.173825)],
	31: [(0.824045, 0.877819)],
	32: [(0.824045, 0.877819)], 33: [(0.765591, 0.892284)], 34: [(0.708674, 0.907534)],
	35: [(0.47697, 0.964243)], 36: [(0.132346, 0.664849)], 37: [(0.77861, 0.664849)],
	38: [(0.215861, 0.437962)], 41: [(0.165146, 0.071681)], 42: [(0.368736, 0.111185)],
	43: [(0.074261, 0.124101)], 44: [(0.284691, 0.075378)], 45: [(0.727416, 0.20517)],
	46: [(0.314606, 0.275278), (0.743124, 0.455869)], 47: [(0.733121, 0.109877)],
	48: [(0.882737, 0.459214)], 51: [(0.219179, 0.738381)], 52: [(0.697164, 0.733766)],
	53: [(0.614988, 0.070183)], 54: [(0.81877, 0.182475)], 55: [(0.825335, 0.075843)],
	56: [(0.535714, 0.38817)], 57: [(0.535714, 0.38817)],
	58: [(0.172875, 0.351134)],
	61: [(0.08913, 0.571883), (0.092627, 0.537649), (0.096708, 0.503799)],
	62: [(0.619937, 0.30869), (0.581568, 0.280972), (0.553296, 0.249612)],
	63: [(0.982929, 0.28124)], 64: [(0.982099, 0.351708)], 65: [(0.982929, 0.420169)],
	66: [(0.637408, 0.269564)], 67: [(0.607223, 0.244843)], 68: [(0.606996, 0.217458)],
}
SWITCH_PROJECTIONS = {
	31: "Projected onto the trough Ball 1 kicker position (sw32): the retained script's ball-release "
	"handler (SolRelease) kicks the ball resting on switch 32 and pulses trough-eject opto 31 in the "
	"same event (vpmTimer.PulseSw 31), and the manual switch-location map places the trough-eject opto "
	"immediately outboard of Trough Ball 1.",
	42: "Projected onto the Genie figure (Primitive GenieP, table object center): public switch 42 (Genie "
	"Target) is set from UpdateGenie's rocking-angle threshold (GenieAngle > 4.5) on the figure itself, "
	"not from a discrete trigger-hit event on either physical target blade.",
	56: "Projected onto the Spinning Lamp Unit disc center (Primitive LampPr/LampPr1/LampPr3, table "
	"object center at raw (510, 840)): SpinnerBallTimer_Timer pulses public switch 56 (Lamp Spin CCW) "
	"whenever the disc's simulated rotation crosses a position threshold while spinning counter-"
	"clockwise; there is no fixed sensor object.",
	57: "Projected onto the Spinning Lamp Unit disc center; see switch 56. SpinnerBallTimer_Timer pulses "
	"public switch 57 (Lamp Spin CW) at the same thresholds while the disc spins clockwise.",
}

SOLENOID_POSITIONS = {
	1: [(0.132346, 0.664849)], 2: [(0.77861, 0.664849)], 3: [(0.405462, 0.227241)],
	4: [(0.637408, 0.269564)], 5: [(0.713456, 0.402253)], 6: [(0.606355, 0.14799)],
	8: [(0.147861, 0.124768)], 9: [(0.824045, 0.877819)], 10: [(0.219179, 0.738381)],
	11: [(0.697164, 0.733766)], 12: [(0.614988, 0.070183)], 13: [(0.81877, 0.182475)],
	14: [(0.825335, 0.075843)], 15: [(0.215861, 0.437962)],
	16: [(0.073732, 0.525976)], 17: [(0.177926, 0.793129)], 18: [(0.455134, 0.886146)],
	19: [(0.107609, 0.245069)], 20: [(0.774349, 0.486703)], 21: [(0.563399, 0.113176)],
	22: [(0.517595, 0.465573)], 23: [(0.535756, 0.387972)], 24: [(0.811427, 0.314526)],
	25: [(0.257076, 0.218886)], 26: [(0.913816, 0.144904)], 27: [(0.420897, 0.074442)],
	28: [(0.248776, 0.407198)],
	33: [(0.099942, 0.135705)], 34: [(0.099942, 0.135705)], 35: [(0.404904, 0.227162)],
	36: [(0.846989, 0.025026)],
	45: [(0.621639, 0.843993)], 46: [(0.621639, 0.843993)],
	47: [(0.290126, 0.843993)], 48: [(0.290126, 0.843993)],
}

GI_POSITIONS: dict[int, list[tuple[float, float]]] = {}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Tales of the Arabian Nights retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained totan extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Tales of the Arabian Nights retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Tales of the Arabian Nights retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Tales of the Arabian Nights retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the totan_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/totan.c totanGameData GEN_WPC95 with wpc_dispDMD, the "
				"inverted-switch mask {0x00,0x00,0x00,0x7f,0x00,...}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL"
				"(FLIP_L), hw.swCol=hw.lampCol=hw.custSol=0, swStart/swTilt/swSlamTilt/swCoinDoor "
				"comSw defines, and init_totan's wpc_set_fastflip_addr(0x7b); src/wpc/core.h "
				"CORE_FIRSTUFLIPSOL=33/CORE_FIRSTLFLIPSOL=45/CORE_FIRSTCUSTSOL=51/CORE_FLIPPERSWCOL=11/"
				"CORE_CUSTSWCOL=CORE_STDSWCOLS=12; src/wpc/core.c core_getSol WPC95 33-36 generic-bit path "
				"(no FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) declared) and 37-44 LPDC 37..40/41..44 duplication "
				"(unused here, custSol=0); src/wpc/wpc.c WPC_FLIPPERSW95 blanket column inversion (always "
				"applied on GEN_WPC95 regardless of FLIP_L/FLIP_U); src/wpc/wpc.h WPC_swF1..WPC_swF8; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95=0x80"
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
			"uri": "external:pinmame-manuals/by-machine/williams.tales-of-the-arabian-nights.1996/archive-Williams_Tales_of_the_Arabian_Nights_Operations_Manual/Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf",
			"original_filename": "Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"160-page OCR'd scan of the Williams Tales of the Arabian Nights operations manual "
				"(Internet Archive item Williams_Tales_of_the_Arabian_Nights_Operations_Manual). Printed "
				"pages 2-36 through 2-42 carry the lamp/switch/solenoid location parts lists and their "
				"matrix and solenoid/flasher wiring tables; page 1 carries the DIP switch country chart; "
				"Section 3 (printed 3-1 onward) carries Game Wiring and Schematics."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.totan.dip-switch-country-chart",
					"locator": "PDF page 1, DIP switch country chart",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/dip-switch-country-chart.md",
					"sha256": "ca37fa8539adfa7534036b9c8a8e77dd502043a9851789f44f6e2ef1d62041e2",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.switch-matrix",
					"locator": "PDF page 120, printed 2-38, Switch Matrix",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/switch-matrix.md",
					"sha256": "f208f7ae06e854451013212252ee97b6f563fdfeda16f5953ecc703dae2dd041",
					"image": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/switch-matrix.webp",
					"image_sha256": "6294445802ff295efd3009ce7b259634c35f3de4d64e78a91f13cef5d6fbb983",
					"image_derivation": "Williams_1996_Tales_of_the_Arabian_Nights_Manual.pdf page 120, crop box 0.08,0.035,0.985,0.575 of the page, rendered at 300 dpi with pdftoppm, reduced to 700px wide grayscale, quality 75 WebP",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.switch-locations",
					"locator": "PDF page 121, printed 2-39, Switch Locations parts list plus opto cross-check",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/switch-locations.md",
					"sha256": "80bdf761c572c3227748712b81b71eb1cc6e38e7a8fbd128f0cf570212093791",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.lamp-matrix-and-locations",
					"locator": "PDF pages 118-119, printed 2-36/2-37, Lamp Matrix and Lamp Locations",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/lamp-matrix-and-locations.md",
					"sha256": "c1680be0c412c1f25499da1292cee6021bffb01a5dbb77e426e52f14035ab11e",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.solenoid-flasher-wiring",
					"locator": "PDF page 122, printed 2-40, Solenoid/Flasher Table and Flipper circuits",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/solenoid-flasher-wiring.md",
					"sha256": "69911b8fe2d3e8db5905da5ed21975dbde58b99b4710e09b345e0548cede0853",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.general-illumination",
					"locator": "PDF page 122, printed 2-40, General Illumination",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/general-illumination.md",
					"sha256": "e6491d8c499213be0d585071e7ba3fc4dbf732cfc9f2b2e956f2219638a5ebc2",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.solenoid-flashlamp-locations",
					"locator": "PDF page 123, printed 2-41, Solenoid/Flashlamp Locations parts list",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/solenoid-flashlamp-locations.md",
					"sha256": "53a210ad2429b69579aaa18485e3d688e6129e277f82cb85e509963dcc72aa93",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.totan.ramps",
					"locator": "PDF page 124, printed 2-42, Ramps assembly parts list",
					"path": "evidence/excerpts/williams.tales-of-the-arabian-nights.1996/ramps.md",
					"sha256": "e40837cf45d42c2b647e5851b87cd5ca6405037486ac141a24de7f55e8dbaa25",
					"method": "mixed",
					"transcribed_by": "curator, OCR text located the page then re-verified against the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, "
				"together with the rendered PNG page cache under external:pinmame-manuals/rendered/"
				"williams.tales-of-the-arabian-nights.1996/. The retained PDF carries a genuine OCR text "
				"layer, but pdftotext -layout badly garbles the multi-column tables, so every table was "
				"re-verified visually against the 300 dpi rendered pages; this transcription is the "
				"source of record."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/source/Tales%20of%20the%20Arabian%20Nights%20%28Williams%201996%29.vpx",
			"original_filename": "Tales of the Arabian Nights (Williams 1996).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working recreation of the physical machine by JPSalas (2015) with later "
				"work by flupper and rothbauerw (2019), released August 2019, based on 944 extracted "
				"files (no VPW authorship). Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/2164 -- note the y divisor is "
				"2164, not the 2162 several other curated WPC games use. Geometry authority only for "
				"named table objects; this is a smaller, older table than the VPW mods used for recently "
				"curated games, and its object set does not support a validated placement for every "
				"device (see GI addresses 3 and 4)."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, flupper, rothbauerw",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (97,833 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "totan_14", Const UseSolenoids = 2 (fast flips), Const UseLamps = 0, '
				"the SolCallback/SolModCallback table for solenoids 1-28 and 34 plus core.vbs "
				"sLRFlipper/sLLFlipper, the Controller.Switch and vpmTimer.PulseSw switch semantics for "
				"the trough/cage/vanish/lock/Genie/Spinning-Lamp-Unit state machines, and Sub UpdateGI "
				"mapping only public GI address 2 to a playfield-wide dimming effect (GI addresses 0, 1, "
				"3, and 4 have no case and thus no visual effect in this table)."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, flupper, rothbauerw",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 "
				f"under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
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
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
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
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
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
			assembly, part_number = SWITCH_PARTS.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used (\"71 to 88 Not Used\")."
			if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed as an opto that is typically closed; PinMAME's totanGameData inverted-switch "
					"mask ({0x00,0x00,0x00,0x7f,...}, column 3 bits 0-6) covers it, so the public switch "
					"state is already normalized and must not be inverted again."
				)
			if address == 24:
				notes += (
					" Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is connected."
				)
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 42:
				notes += " Double target assembly (SW-1A-207 left, SW-1A-208 right) read as one address."
			if address == 46:
				notes += (
					" The manual prints \"Mini Standups (3)\" but the retained table models only two target "
					"objects (sw46, sw46b) sharing this address; the third physical target has no distinct "
					"evidenced coordinate."
				)
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
				if address in {11, 13, 14, 21, 22}:
					role = {
						11: "cabinet.launch",
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {11, 13} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None, True),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316", True),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None, True),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316", True),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, True),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, "A-17316", True),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, True),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, "A-17316", True),
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
				" Tales of the Arabian Nights has no upper flippers and the switch-locations parts list "
				"on manual page 2-39 marks this position Not Used."
			)
			physical["location"] = "not installed"
			notes += (
				" The switch-matrix wiring page (2-38) nonetheless draws this position's template wire "
				"colors and connector pins, so its printed construction is recorded even though no "
				"physical switch is installed."
			)
		elif switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed. WPC-95 reads the flipper column through "
				"WPC_FLIPPERSW95 with a blanket hardware inversion applied to the whole eight-position "
				"column regardless of fitment, so the public switch state is already normalized."
			)
		else:
			notes += (
				" Printed as a plain end-of-stroke leaf switch (not opto); the same blanket "
				"WPC_FLIPPERSW95 column inversion applies to this position too."
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

	dip_country_chart = (
		"Printed DIP country chart (manual page 1): SW1-SW8 Off/Off/On/On/On/On/On/On = AMERICA; "
		"Off/Off/On/On/On/Off/On/On = EUROPEAN; Off/Off/On/On/On/On/Off/Off = FRENCH; "
		"Off/Off/On/On/On/On/On/Off = GERMAN; Off/Off/On/On/Off/On/On/On = SPAIN."
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
						f"WPC-95 CPU-board country/option configuration DIP bank, bit {address} of 8. "
						f"{dip_country_chart}"
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
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			kind = "flasher" if address in FLASHER_BULBS else "motor" if address == 21 else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher":
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" Only the playfield bulb(s) have a playfield placement; the insert-panel bulb is "
						"backbox hardware behind the translite and is deliberately not given a playfield "
						"coordinate."
					)
				if address in (16, 17) and playfield_emitters == 2:
					notes += (
						" The manual prints two playfield bulbs for this circuit but the retained table "
						"models only one Light object at this address; the second playfield bulb has no "
						"distinct evidenced coordinate, so only one placement is recorded."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address == 21:
				notes += (
					" Not a flasher despite sitting among the flasher-numbered range: the retained script's "
					"RampDiverter/RampDiv_Timer handlers animate a physically rotating diverter post over "
					"multiple steps, matching the manual's \"Low Power\" solenoid type (not \"Flasher\") and "
					"its own AE-30-2000 coil part number."
				)
			if address in (33, 34):
				notes += (
					" Fliptronic upper-right power/hold circuit repurposed for a non-flipper device: the "
					"printed \"Upr. Rt. Power/Hold\" column labels are the standard WPC flipper-circuit "
					"template carried over from the schematic, not evidence of a power-then-hold "
					"relationship between two different toys."
				)
			if address in (45, 46, 47, 48):
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers "
					"the same circuits 29-32; the manual address is preserved as an alias."
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
			role = "emitter" if kind == "flasher" else "effect"
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address == 7:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Tales of the Arabian Nights playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a playfield device.",
			31: "PinMAME's synthetic game-on state. Tales of the Arabian Nights sets wpc_set_fastflip_addr(0x7b), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			37: "Unused WPC-95 LPDC general-purpose output; totanGameData declares no custSol and no LPDC device.",
			38: "Unused WPC-95 LPDC general-purpose output.",
			39: "Unused WPC-95 LPDC general-purpose output.",
			40: "Unused WPC-95 LPDC general-purpose output.",
			41: "Unused WPC-95 LPDC mirror of output 37 (PinMAME duplicates 37-40 at 41-44 on this hardware generation; nothing is fitted at either address).",
			42: "Unused WPC-95 LPDC mirror of output 38.",
			43: "Unused WPC-95 LPDC mirror of output 39.",
			44: "Unused WPC-95 LPDC mirror of output 40.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. totanGameData declares no custSol.",
		}.get(address, "Unused custom-solenoid position; totanGameData declares custSol=0, so PinMAME serves no game-specific handler above public address 50.")
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"]
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			bulb = LAMP_BULBS.get(address, "#555")
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}. Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += (
					f" The printed lamp-locations parts list marks this insert \"({LAMP_QUANTITIES[address]})\" "
					"and the retained table binds two Light objects on opposite sides of the playfield "
					"(l28 right outlane, l28a left outlane), so it has two placements."
				)
			if address in {87, 88} == {88}:
				pass
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
			if address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["notes"] += (
					" Cabinet button lamp inside the illuminated start button assembly. A table object "
					"named l88 exists (raw (943.938, 2010.469), surface \"Apron\") but carries the "
					"unbound-default timer_interval of 100 and is not a member of the InsertLights "
					"collection Sub InitLights binds, so it is provably inert -- corroborating rather than "
					"contradicting the cabinet classification."
				)
			else:
				availability = "used"
				if address in LAMP_RENDER_DOUBLES:
					physical["notes"] += (
						" The retained table stacks a second co-located Light object purely for brightness "
						"(within 38 raw units, well under 4% of playfield width); the primary lNN object is "
						"used and the duplicate is documented render doubling, matching the manual's "
						"single-bulb parts entry."
					)
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


LAMP_POSITIONS = {
	11: [(0.298099, 0.777241)], 12: [(0.332257, 0.801695)], 13: [(0.38781, 0.819934)],
	14: [(0.454495, 0.826655)], 15: [(0.521619, 0.818968)], 16: [(0.574571, 0.801713)],
	17: [(0.607526, 0.776411)], 18: [(0.658295, 0.802659)],
	21: [(0.37888, 0.149919)], 22: [(0.318933, 0.190766)], 23: [(0.347019, 0.177926)],
	24: [(0.385382, 0.171503)], 25: [(0.426112, 0.172945)], 26: [(0.461485, 0.181822)],
	27: [(0.44645, 0.273669)], 28: [(0.852558, 0.767126), (0.054503, 0.768225)],
	31: [(0.311296, 0.427124)],
	32: [(0.286862, 0.3755)], 33: [(0.293509, 0.33181)], 34: [(0.242593, 0.336375)],
	35: [(0.407142, 0.747634)], 36: [(0.482399, 0.731123)], 37: [(0.554547, 0.720371)],
	38: [(0.441069, 0.696329)],
	41: [(0.42851, 0.59868)], 42: [(0.361966, 0.579817)], 43: [(0.430955, 0.566015)],
	44: [(0.512136, 0.568435)], 45: [(0.558774, 0.536935)], 46: [(0.496438, 0.514173)],
	47: [(0.434931, 0.496645)], 48: [(0.387209, 0.467452)],
	51: [(0.396777, 0.432721)], 52: [(0.397193, 0.408304)], 53: [(0.39225, 0.386821)],
	54: [(0.402431, 0.364959)], 55: [(0.613301, 0.683807)], 56: [(0.578837, 0.651808)],
	57: [(0.68197, 0.643371)], 58: [(0.224928, 0.643131)],
	61: [(0.685569, 0.444689)], 62: [(0.67394, 0.480838)], 63: [(0.65743, 0.508305)],
	64: [(0.641956, 0.535509)], 65: [(0.626558, 0.563268)], 66: [(0.610666, 0.590428)],
	67: [(0.595148, 0.617487)], 68: [(0.664319, 0.345143)],
	71: [(0.115649, 0.40537)], 72: [(0.130333, 0.440027)], 73: [(0.167967, 0.488741)],
	74: [(0.218092, 0.54296)], 75: [(0.182412, 0.570435)], 76: [(0.264725, 0.686886)],
	77: [(0.310694, 0.686849)], 78: [(0.357135, 0.687078)],
	81: [(0.827272, 0.390276)], 82: [(0.810027, 0.443123)], 83: [(0.77798, 0.495617)],
	84: [(0.738869, 0.535299)], 85: [(0.760309, 0.579378)], 86: [(0.510286, 0.272725)],
	87: [(0.287379, 0.478014)],
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
				"board": "WPC-95 power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in (0, 1, 2):
			notes += (
				" Backbox insert-panel illumination behind the translite: the manual's own wiring table "
				"shows no Playfield connector entry for this string (only Backbox J106-x)."
			)
			if address == 2:
				notes += (
					" The retained script's Sub UpdateGI implements ONLY this address (Case 2) and binds it "
					"to a broad playfield-wide dimming effect across dozens of playfield objects "
					"(FadingGIlights collection, tex1/tex2/tex3/ramp/sidewalls materials, the Genie figure "
					"material, slingshot and cage textures, ball tint) -- directly contradicting the "
					"manual's own physical wiring for this backbox-only string. See "
					"conflict.gi-string-3-playfield-binding. The manual's physical wiring is treated as "
					"authoritative for this device's location; the script's cross-wiring is not evidence of "
					"a playfield placement for a backbox bulb."
				)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			notes += (
				" Playfield general illumination per the manual's own wiring table (Playfield connector "
				"J105-x, #555 bulb), the string 5 also feeding a cabinet connection (J104). The retained "
				"script's Sub UpdateGI has no case for this address, so no VPX object is bound to it and "
				"no playfield coordinate can be validated from this source; the spatial field is omitted "
				"rather than fabricated."
			)
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
			"mechanism.knocker",
			"Cabinet knocker",
			"other",
			[output_id("Knocker")],
			[],
			"Solenoid 7 raps the cabinet knocker solenoid against the cabinet wall on scoring events "
			"(replay/match); it is a standard cabinet device with no playfield presence.",
			[],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="B-10686-1",
		),
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on trough optos 32-35, with Trough Ball 1 (32) at the eject end nearest the "
			"shooter lane and Trough Ball 4/Drain (35) at the drain entrance. Solenoid 9 (SolRelease) "
			"ejects the ball resting on 32 and pulses trough-eject opto 31 in the same event "
			"(vpmTimer.PulseSw 31). All five positions are printed optos that rest closed (column 3 of "
			"the inverted-switch mask), so a recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 / Drain entrance", ["switch.matrix-35"], "Drain entrance and fourth trough position; also fires the Drain handler."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.cages",
			"Left and right magnetic inlane cages",
			"other",
			[output_id("Left Cage"), output_id("Right Cage")],
			["switch.matrix-36", "switch.matrix-37"],
			"A raised cage wall traps a ball rolling through the left/right inlane opto (36/37) unless a "
			"second ball is simultaneously present in the trigger zone. The retained script's sw36_timer/"
			"sw37_timer handlers poll ball positions every 10 ms and only raise the cage (leftcage.z=0 / "
			"rightcage.z=0) once the lane is clear; solenoids 1/2 (SolSpikerLeft/SolSpikerRight) lower the "
			"cage back down (z=-69) on release. The cage optos rest closed and are normalized by "
			"PinMAME's inverted-switch mask column 3.",
			[
				("left", "Left cage raised over inlane opto 36", ["switch.matrix-36"], "Left inlane opto."),
				("right", "Right cage raised over inlane opto 37", ["switch.matrix-37"], "Right inlane opto."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20693",
		),
		mechanism(
			"mechanism.vanishing-ball",
			"Vanishing Magnet ball-teleport assembly",
			"other",
			[output_id("Vanish Drop"), output_id("Vanish Magnet")],
			["switch.matrix-12"],
			"The manual's \"Vanishing Magnet Assembly\" (TOC 2-25) makes a ball appear to disappear. "
			"Solenoid 3 (SolVanishDrop) opens a hidden trapdoor (HideVanish.Isdropped) beneath the Vanish "
			"Tunnel opto (switch 12, pulsed on entry) while solenoid 35 (SolVanishMagnet) energizes a "
			"magnet that holds the ball out of sight; releasing the magnet (HideVanish_Timer) launches the "
			"ball back into play in a random direction. All three retained table objects (VanishHole "
			"trigger, VanishMagnet trigger, HideVanish wall) cluster within one raw unit of each other, "
			"confirming a single physical assembly.",
			[("held", "Ball held vanished under the magnet", ["switch.matrix-12"], "Vanish Tunnel entry opto.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20644",
		),
		mechanism(
			"mechanism.lock",
			"Three-ball magnetic lock",
			"other",
			[output_id("Lock Eject"), output_id("Lock Magnet")],
			["switch.matrix-66", "switch.matrix-67", "switch.matrix-68"],
			"A single magnet (solenoid 6, mLockMagnet) captures and holds up to three locked balls at "
			"stacked positions Lock 1 (bottom, switch 66), Lock 2 (middle, switch 67), and Lock 3 (top, "
			"switch 68); the retained script's LockMagnet_hit/LockMagnet1_unhit handlers damp ball "
			"velocity while the magnet is energized. Solenoid 4 (SolLockRelease) kicks the stack loose "
			"(Lock1.kick) and opens two release walls (wall001/wall002) so the locked balls can return to "
			"play.",
			[
				("lock-1", "Lock 1 (bottom)", ["switch.matrix-66"], "Bottom locked-ball position."),
				("lock-2", "Lock 2 (middle)", ["switch.matrix-67"], "Middle locked-ball position."),
				("lock-3", "Lock 3 (top)", ["switch.matrix-68"], "Top locked-ball position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-L-3",
		),
		mechanism(
			"mechanism.bazaar-scoop",
			"Bazaar scoop",
			"kicker",
			[output_id("Bazaar Eject")],
			["switch.matrix-25"],
			"A ball resting on opto 25 (Bazaar Eject) is kicked back to the playfield by solenoid 5 "
			"(SolBazaarKick); the retained script raises a companion collision wall (sw25wall) while the "
			"ball is captured.",
			[("held", "Ball in the Bazaar scoop", ["switch.matrix-25"], "Bazaar scoop switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16434-2",
		),
		mechanism(
			"mechanism.ramp-magnet",
			"Ramp magnet",
			"other",
			[output_id("Ramp Magnet Coil")],
			[],
			"Solenoid 8 (SolRampMagnet) energizes a magnet (RMagnet) on the Magnet Ramp Assembly that "
			"catches and holds a ball mid-ramp; releasing it nudges the ball forward (VelX=5, VelY=2). No "
			"printed switch is dedicated to this device; the manual documents its own switch and diode "
			"assembly as part of the Magnet Ramp Assembly (item 1c, A-12238) but that assembly feeds the "
			"Ramp Made Left/Right matrix switches (41/47), not a magnet-specific position sensor.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20839",
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Swirl Ramp diverter",
			"gate",
			[output_id("Ramp Diverter")],
			[],
			"Solenoid 21 (RampDiverter) drives a physically rotating diverter post on the Swirl Ramp "
			"Assembly (manual item 2, printed 2-42) between two end stops over several animation steps "
			"(RampDiv_Timer, RampDivPos range -21 to 1), not a simple on/off flasher despite sitting in "
			"the flasher-numbered address range.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20626",
		),
		mechanism(
			"mechanism.playfield-diverter",
			"Left (playfield) diverter",
			"gate",
			[output_id("Left Diverter Power"), output_id("Left Diverter Hold")],
			[],
			"A two-stage power/hold coil pair (solenoids 33/34) on the Fliptronic upper-right circuit "
			"drives a playfield ball diverter gate (PlayFDiv) rather than an upper flipper -- this game has "
			"no upper flippers. The retained script scripts only the hold address (34, SolPlayFDiv via "
			"vpmSolDiverter); the power address (33) shares the same physical coil pair per the manual's "
			"J119-6 wiring bus.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20642",
		),
		mechanism(
			"mechanism.loop-post-diverter",
			"Loop post diverter",
			"gate",
			[output_id("Loop Post Diverter")],
			[],
			"Solenoid 36 (SolLoopDiv) raises a post (LoopPostDiverter wall) that diverts a ball at the "
			"right loop; it is wired on the same Fliptronic upper-left circuit bus (J119-8) as Vanish "
			"Magnet (solenoid 35) but is an independently scripted, unrelated device, not that circuit's "
			"power/hold partner.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17932-1",
		),
		mechanism(
			"mechanism.spinning-lamp-unit",
			"Spinning Lamp Unit (Magic Lamp disc)",
			"other",
			[],
			["switch.matrix-56", "switch.matrix-57"],
			"The manual's \"Spinning Lamp Unit Assembly\" (TOC 2-23) is a freely rotating disc (table "
			"radius 60 units, centered at normalized x=0.535714 y=0.388170) that two spinner-kick posts "
			"near the shooter lane (Kicker.SpinnerKick/SpinnerKick2) set spinning when struck by a ball. "
			"The retained script's SpinnerBallTimer_Timer integrates angular speed with friction and a "
			"spring-centered wobble every 10 ms, and pulses public switch 56 (Lamp Spin CCW) or 57 (Lamp "
			"Spin CW) each time the disc's rotation crosses a position threshold, depending on spin "
			"direction. There is no PinMAME mech table or ROM-side position counter for this motion; it is "
			"a pure VPX physical simulation with no coil -- the disc is ball-driven, not motorized.",
			[
				("ccw", "Rotating counter-clockwise past threshold", ["switch.matrix-56"], "Pulsed each time the disc crosses 30 or 210 degrees while spinning CCW."),
				("cw", "Rotating clockwise past threshold", ["switch.matrix-57"], "Pulsed each time the disc crosses 30 or 210 degrees while spinning CW."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="SW-1A-206",
		),
		mechanism(
			"mechanism.genie",
			"Genie figure and double target",
			"other",
			[],
			["switch.matrix-23", "switch.matrix-42"],
			"The manual's \"Genie Double Target Assembly\" (TOC 2-24) is a spring-loaded rocking figure "
			"(GenieP/GenieP1 primitives) struck by the ball at two collision zones (GenieTrig, GenieTrig1; "
			"a third object GenieTrig2 exists in the table but has no script handler and is inert). The "
			"retained script's UpdateGenie integrates a bounce/decay physics model on the figure's rock "
			"angle and asserts public switch 42 (Genie Target) whenever that angle exceeds 4.5 degrees -- "
			"there is no discrete trigger-hit event for the switch itself. The separate Genie Standup "
			"Target (switch 23, HitTarget sw23) is a distinct, single, ordinary standup target elsewhere "
			"on the playfield.",
			[
				("standup", "Genie Standup Target struck", ["switch.matrix-23"], "Single standup target."),
				("double-target", "Genie figure rocked past threshold", ["switch.matrix-42"], "SW-1A-207/208 double target read as one address via the figure's own rock-angle physics."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-18530-6",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot assembly carries a kick switch (A-17800) and a separate scored switch "
			"(A-17793, diode-attached) reported as one matrix address. The retained script's "
			"LeftSlingShot_Slingshot/RightSlingShot_Slingshot handlers pulse matrix addresses 51 and 52 "
			"and fire coils 10/11 in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-L-3",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Middle Jet Bumper")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-55"],
			"Three A-9415-2 jet bumpers with A-16443 skirt switches. The retained script's Bumper1_Hit, "
			"Bumper3_Hit, and Bumper2_Hit handlers pulse switches 53 (Left), 54 (Right), and 55 (Middle) "
			"and fire coils 12, 13, and 14 respectively, matching the printed Left/Right/Middle Jet Bumper "
			"labels (note the non-alphabetic table-object-to-address mapping: Bumper2 is the Middle jet "
			"and Bumper3 is the Right jet).",
			[
				("left", "Left jet bumper", ["switch.matrix-53"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-54"], "Right bumper of the nest."),
				("middle", "Middle jet bumper", ["switch.matrix-55"], "Bumper closest to the player."),
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
			"left) closes. Tales of the Arabian Nights runs Const UseSolenoids = 2 fast flips, so the ROM "
			"drives the coils directly. There are no upper flippers; the upper-flipper Fliptronic circuits "
			"(115, 116, 117, 118) are unfitted and the printed upper-flipper solenoid circuits (33-36) "
			"drive unrelated non-flipper devices.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14876-R-3 right with A-15849-L-2 left",
		),
		mechanism(
			"mechanism.left-kicker",
			"Left kicker hole",
			"kicker",
			[output_id("Left Kicker")],
			["switch.matrix-38"],
			"A ball resting on switch 38 (Left Eject) is kicked back to the playfield by solenoid 15 "
			"(SolLeftKicker).",
			[("held", "Ball in the left kicker hole", ["switch.matrix-38"], "Left eject switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-L-3",
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
	return [
		{
			"id": "conflict.gi-string-3-playfield-binding",
			"path": "outputs[binding.group=pinmame.output.gi,binding.device=2]",
			"description": (
				"The manual's own solenoid/flasher wiring table (printed 2-40) documents public GI "
				"address 2 (printed Illumination String 3) as backbox insert-panel only: its \"Voltage "
				"Connections\" and \"Drive Connections\" columns both carry only a Backbox entry (J106-3 / "
				"J106-9) with the Playfield column blank, and it uses the small #44 bulb shared with "
				"strings 1 and 2, while the genuinely playfield-wired strings are addresses 3 and 4 "
				"(printed Strings 4-5, Playfield connectors J105-5/J105-10 and J105-6/J105-11, #555 "
				"bulbs). The retained known-working script disagrees: its Sub UpdateGI(no, step) "
				"implements only `Case 2`, driving a playfield-wide dimming value (globalGI) applied to a "
				"large collection of playfield objects (the FadingGIlights collection plus tex1/tex2/tex3/"
				"ramp/sidewalls materials, the Genie figure's material, slingshot and cage textures, and "
				"ball tint), while addresses 0, 1, 3, and 4 fall through with no case and produce no "
				"visual effect at all. The manual is physical-construction ground truth and the retained "
				"script is runtime-semantics ground truth, and the two disagree on which public GI address "
				"actually lights the playfield. This curation follows the manual for the device's spatial "
				"classification (GI address 2 remains a backbox device with a not_applicable spatial "
				"record) rather than treating the script's cross-wiring as proof of a playfield location "
				"for a backbox bulb, and leaves GI addresses 3 and 4 (the manual's genuine playfield "
				"strings) without a validated placement because no VPX object binds specifically to them. "
				"Resolution path: a LibPinMAME gameplay-harness trace of a legal totan_14 ROM observing "
				"which GI address the ROM actually varies during attract-mode playfield dimming, cross-"
				"checked against a photograph or continuity trace of the physical J105/J106 harness. "
				"Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "williams.tales-of-the-arabian-nights.1996",
			"name": "Tales of the Arabian Nights",
			"manufacturer": "Williams",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 3824,
			"opdb_id": "G4llj-MQYb2",
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
				"spatial_placement": "conflicted",
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
		"knowledge": {"path": "knowledge/williams/tales-of-the-arabian-nights-1996.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Tales of the Arabian Nights device identifiers are not unique: {duplicates}")
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
		"status": "conflicted",
		"blockers": [
			"GI address 2 (printed Illumination String 3) is documented backbox-only by the manual's own "
			"wiring table, but the retained script's Sub UpdateGI binds only this address to a large "
			"playfield-wide dimming effect while leaving the manual's two genuine playfield strings "
			"(addresses 3 and 4) with no script binding at all. Recorded as unresolved "
			"conflict.gi-string-3-playfield-binding.",
			"GI addresses 3 and 4 (the manual's genuine playfield strings) have no validated spatial "
			"placement: no VPX object in the retained (non-VPW, 944-file) extraction is bound to either "
			"address, so their `spatial` key is omitted rather than fabricated with a projection.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2164; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/tales-of-the-arabian-nights-1996/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
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
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.tales-of-the-arabian-nights.1996/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"LightNN/f1/f16-style co-located brightness-doubling Light objects sharing an already-placed "
			"lamp address (max pairwise distance 38 raw units, well under 4% of playfield width, at every "
			"address except 28)",
			"FlasherFlash122b/122c and Flasherflash125b -- additional co-located render surfaces for "
			"single physical flasher bulbs at addresses 22 and 25",
			"GenieTrig2 -- present in the retained table with the unbound-default timer_interval, no "
			"script _Hit handler anywhere -- inert legacy collision object",
			"Light.l88 -- exists at Apron surface coordinates but carries the unbound-default "
			"timer_interval (100) and is not a member of the InsertLights collection the runtime lamp "
			"update binds, corroborating rather than contradicting lamp 88's cabinet classification",
		],
		"unresolved": [
			{"group": "pinmame.output.gi", "address": 3, "reason": "no VPX object bound to this playfield GI address in the retained extraction"},
			{"group": "pinmame.output.gi", "address": 4, "reason": "no VPX object bound to this playfield GI address in the retained extraction"},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Tales of the Arabian Nights (Williams, 1996) spatial review",
		"",
		f"Status: {report['status']}. Every switch, solenoid, and lamp address that the retained table "
		"can support is located and validated, but two GI addresses have no supporting VPX object and a "
		"third carries a genuine manual-versus-script wiring disagreement, so the physical machine record "
		"stays `partial` at `machines/partial/williams/tales-of-the-arabian-nights-1996.json`.",
		"",
		"The matching source is the retained known-working `Tales of the Arabian Nights (Williams 1996)."
		f"vpx` at SHA-256 `{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the "
		f"embedded script at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality "
		f"authority. Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 "
		"and y/2164 (not 2162) rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual PDF carries a genuine OCR text layer, but `pdftotext -layout` badly garbles "
		"the multi-column switch/solenoid/lamp tables. Every printed table used here was re-verified "
		"visually against the 300 dpi rendered pages and transcribed into "
		"`external:pinmame-review-artifacts/tales-of-the-arabian-nights-1996/manual-transcription.md`.",
		"- Two switches (31, 42) and two mechanism-driven switches (56, 57) have no dedicated playfield "
		"trigger object because the retained script sets their public state directly from another "
		"mechanism's continuous position (trough ball-release event, Genie figure rock angle, Spinning "
		"Lamp Unit disc rotation) rather than from a discrete Hit event. Those addresses are explicit "
		"documented projections onto the real table object that carries the underlying mechanism state.",
		"- This retained table is smaller and older than the VPW mods used for several other curated WPC "
		"games (944 files, no VPW authorship). Its object set does not support a validated playfield "
		"placement for GI addresses 3 and 4, so those two devices are left spatially unresolved rather "
		"than assigned a fabricated coordinate.",
		"- GI address 2 carries a first-class unresolved conflict: the manual documents it as backbox-only "
		"but the retained script binds only that address to a playfield-wide dimming effect. The manual's "
		"physical wiring controls this device's spatial classification (not_applicable/cabinet_or_service).",
		"- Solenoids 16 and 17 (Left Eject Flasher, Inlane Flashers) print two playfield bulbs each, but "
		"the retained table models only one Light object per address; one placement is recorded and the "
		"quantity gap is disclosed in `physical.notes` rather than fabricating a second coordinate.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with "
		"both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Unresolved (no fabricated placement)",
		"",
	]
	for entry in report["unresolved"]:
		lines.append(f"- {entry['group']} address {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved output bindings: {len(report['unresolved_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for switches, "
		"solenoids, lamps, or the flipper pair. GI address 2 carries a first-class, unresolved conflict "
		"between the manual's physical wiring and the retained script's runtime binding "
		"(`conflict.gi-string-3-playfield-binding`), and GI addresses 3 and 4 -- the manual's genuine "
		"playfield strings -- have no VPX object to validate a placement from in this retained "
		"(non-VPW) table. The definition therefore carries a non-empty `conflicts` array and "
		"`coverage.dimensions.physical_wiring = \"conflicted\"` / `coverage.dimensions.spatial_placement "
		"= \"conflicted\"`, so promotion to `author_ready` is refused; the record stays `partial` with "
		"`coverage.missing = [\"spatial_placement\", \"unresolved_conflicts\"]` until a LibPinMAME harness "
		"trace against a legal totan_14 ROM observes which GI address the ROM actually varies during "
		"attract-mode playfield dimming.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
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
		raise RuntimeError(f"Stale Tales of the Arabian Nights author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Tales of the Arabian Nights definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Tales of the Arabian Nights seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Tales of the Arabian Nights definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Tales of the Arabian Nights seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Tales of the Arabian Nights spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Tales of the Arabian Nights spatial review drifted from its deterministic curator: {markdown_path}")
	print("Tales of the Arabian Nights definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Tales of the Arabian Nights extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Tales of the Arabian Nights retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
