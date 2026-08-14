"""Curate the physical Williams Congo (1995) machine definition.

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
PARTIAL_PATH = ROOT / "machines/partial/williams/congo-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/congo-1995.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/congo-1995.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/congo-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/congo-1995.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.congo.1995"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.congo.1995"
VPX_TABLE_SOURCE = "vpx-table.congo-jpsalas-nfozzy"
VPX_SCRIPT_SOURCE = "vpx-script.congo-jpsalas-nfozzy"
VPX_EXTRACTION_SOURCE = "vpx-extraction.congo-jpsalas-nfozzy"

TABLE_SHA256 = "45a6448efb586475a6886962c5bace44789be1d7cd3dde2c507169fdf085432c"
SCRIPT_SHA256 = "19c19ea64bb120af66ef3ca309a2ec98c08b35ecf08e198bb26b3cd1611cd936"
MANUAL_SHA256 = "2770692875d10e7cc5bdd11a823ceb9ecfd2f374ed196207ca66631127b77f40"

EXTRACTION_RELATIVE_PATH = Path("williams/congo-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/congo-1995/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "c9b02744cbb2e1b0659c7032b0ef42d4e7cadf5c36ed33ac171a037b8be82b62"
EXTRACTION_FILE_COUNT = 925
EXTRACTION_TOTAL_BYTES = 47770557

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
TABLE_WIDTH = 964.0
TABLE_HEIGHT = 2162.0

DRIVER_IDS = ("congo_21", "congo_20", "congo_20s10k", "congo_13", "congo_11")
DRIVER_COMPATIBILITY = {
	"congo_21": (
		"identical",
		"Williams production 2.1 game ROM (DCS95 sound ROM S1.1) shipped with the physical machine; the "
		"retained known-working script binds this exact driver (cGameName = \"congo_21\"). Pinned PinMAME's "
		"own libpinmame.h comment names GEN_WPC95 \"Integrated boards, Congo 3/96 - Cactus Canyon 2/99\", "
		"i.e. Congo is the first physical machine PinMAME's own catalog anchors that hardware generation to.",
	),
	"congo_20": (
		"identical",
		"Williams 2.0 game ROM (DCS95 sound ROM S1.1); an earlier firmware revision of the same physical "
		"machine with no controller-address or playfield change.",
	),
	"congo_13": (
		"identical",
		"Williams 1.3 game ROM (DCS95 sound ROM S1.1); an earlier firmware revision of the same physical "
		"machine with no controller-address or playfield change.",
	),
	"congo_11": (
		"identical",
		"Williams 1.1 game ROM (DCS95 sound ROM S1.1); an earlier firmware revision of the same physical "
		"machine with no controller-address or playfield change.",
	),
	"congo_20s10k": (
		"compatible",
		"Williams 2.0 game ROM built for the WPC-S hardware and sound-ROM S1.0-kit combination, per the "
		"pinned driver's own comment \"intended to be used with the playfield conversion kit\". Pinned "
		"PinMAME binds this one driver to congoDCSGameData (GEN_WPC95DCS, libpinmame.h: \"Hybrid WPC95 "
		"driver + DCS sound, Who Dunnit\") instead of the parent's congoGameData (GEN_WPC95); "
		"GENWPC_HASWPC95 (= GEN_WPC95 | GEN_WPC95DCS) treats both identically for coin/DIP/switch-matrix/"
		"Fliptronic/solenoid/lamp/GI addressing throughout core.c and wpc.c, so no controller binding "
		"differs. Only the sound subsystem differs (src/wpc/wpc.c selects SNDBRD_DCS for GEN_WPC95DCS "
		"instead of SNDBRD_DCS95), and pinned PinMAME flags this driver GAME_IMPERFECT_SOUND (flags=1024). "
		"This is the first driver family in this project where one clone genuinely uses a different "
		"PINMAME_HARDWARE_GEN_* constant than its parent while remaining the same physical machine.",
	),
}

# --- Printed switch matrix (manual page 2-40 wiring, 2-41 parts list).
SWITCH_LABELS = {
	11: "Inner Left Loop", 12: "Upper Loop", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Jet Exit", 16: "Left Outlane", 17: "Right Return Lane", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed", 25: "Right Eject Rubber",
	26: "Left Return Lane", 27: "Right Outlane", 28: "You Standup Target",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Volcano Stack", 37: "Mystery Eject", 38: "Right Eject",
	41: "Lock Ball 1", 42: "Lock Ball 2", 43: "Lock Ball 3", 44: "Mine Shaft",
	45: "Left Loop", 46: "Left Bank Top", 47: "Left Bank Center", 48: "Left Bank Bottom",
	51: "Travi", 52: "Com", 53: "2-Way Popper", 54: "We Are Standup Target",
	55: "Watching Standup Target", 56: "Perimeter Defense", 57: "Left Ramp Enter", 58: "Left Ramp Exit",
	61: "Left Slingshot", 62: "Right Slingshot", 63: "Left Jet Bumper", 64: "Right Jet Bumper",
	65: "Bottom Jet Bumper", 67: "Right Ramp Enter", 68: "Right Ramp Exit",
	71: "AMY Rollover (A)", 72: "AMY Rollover (M)", 73: "AMY Rollover (Y)",
	74: "CONGO Target (C)", 75: "CONGO Target (O, first)", 76: "CONGO Target (N)",
	77: "CONGO Target (G)", 78: "CONGO Target (O, second)",
}
# Printed matrix positions marked "NOT USED" on both the Switch Locations parts list (2-41) and the
# Switch Matrix wiring page (2-40). Column 8 (81-88) is entirely unpopulated.
UNUSED_MATRIX_ADDRESSES = {23, 66, 81, 82, 83, 84, 85, 86, 87, 88}
# Every switch shaded "OPTO, TYPICALLY CLOSED" on the printed matrix page (2-40): the trough
# optos, the Volcano Stack entrance opto, and the three Volcano lock-ball optos. Every one of these
# nine addresses is also independently identified as opto by its own Switch Locations part number
# (A-18617-1/A-18618-1 LED+phototransistor pair for 31-35, A-16909 LED+phototransistor for 36/41-43),
# and PinMAME's congoGameData inverted-switch mask normalizes exactly the same nine addresses
# (column 3 = 0x3f, bits 0-5 = rows 1-6 = 31-36; column 4 = 0x07, bits 0-2 = rows 1-3 = 41-43) --
# a clean sweep with zero disagreement between the manual and the emulator.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 41, 42, 43}
# vpmTimer.PulseSw / TargetBouncer callers in the retained known-working script.
PULSED_SWITCHES = {28, 31, 46, 47, 48, 51, 52, 54, 55, 56, 61, 62, 63, 64, 65, 74, 75, 76, 77, 78}

SWITCH_TYPES = {
	11: "microswitch", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch",
	24: "other", 25: "leaf", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto",
	37: "microswitch", 38: "microswitch", 41: "opto", 42: "opto", 43: "opto",
	44: "microswitch", 45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "leaf", 62: "leaf", 63: "leaf", 64: "leaf", 65: "leaf",
	67: "microswitch", 68: "microswitch",
	71: "microswitch", 72: "microswitch", 73: "microswitch",
	74: "microswitch", 75: "microswitch", 76: "microswitch", 77: "microswitch", 78: "microswitch",
}

# address -> (assembly_part_number, part_number), transcribed verbatim from printed 2-41.
SWITCH_PARTS = {
	11: (None, "5647-12693-19"), 12: (None, "5647-12693-19"), 13: (None, "20-9663-1"),
	14: (None, "A-15361"), 15: (None, "5647-12693-19"), 16: (None, "5647-12693-19"),
	17: (None, "5647-12693-19"), 18: (None, "5647-12693-62"), 21: (None, "A-17238"),
	22: (None, "5643-09268-00"), 24: (None, "5643-09112-00"), 25: (None, "A-17794"),
	26: (None, "5647-12693-19"), 27: (None, "5647-12693-19"), 28: (None, "A-17778-15"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16909 LED with A-16909 photo transistor", None),
	37: (None, "5647-12693-43"), 38: (None, "5647-12693-43"),
	41: ("A-16909 LED with A-16909 photo transistor", None),
	42: ("A-16909 LED with A-16909 photo transistor", None),
	43: ("A-16909 LED with A-16909 photo transistor", None),
	44: (None, "5647-12693-11"), 45: (None, "5647-12393-19"),
	46: (None, "A-18605-6"), 47: (None, "A-18605-6"), 48: (None, "A-18605-6"),
	51: (None, "A-20678-6"), 52: (None, "A-20678-6"), 53: (None, "5647-12693-11"),
	54: (None, "A-17778-15"), 55: (None, "A-17778-15"), 56: (None, "A-18605-1"),
	57: (None, "5647-12693-11"), 58: (None, "5647-12693-21"),
	61: ("SW-1A-204 (Kick)", "SW-1A-205 (Score)"), 62: ("SW-1A-204 (Kick)", "SW-1A-205 (Score)"),
	63: (None, "SW-11A-37-1"), 64: (None, "SW-11A-37-1"), 65: (None, "SW-11A-37-1"),
	67: (None, "5647-12693-11"), 68: (None, "5647-12693-21"),
	71: (None, "5647-12693-19"), 72: (None, "5647-12693-19"), 73: (None, "5647-12693-19"),
	74: (None, "SW-1A-203-6"), 75: (None, "SW-1A-203-6"), 76: (None, "SW-1A-203-6"),
	77: (None, "SW-1A-203-6"), 78: (None, "SW-1A-203-6"),
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
# Fliptronic F1-F8 wiring, printed 2-40. F5/F6 (upper right) print Not Used on both this page and
# the Switch Locations page; the manual's own Solenoid/Flasher Table has no "Upper Right Flipper"
# row either (only "Upper Left Post" and "Mystery Eject" occupy the printed Upr. Rt. slot), and
# congoGameData's FLIP_SOL(FLIP_L | FLIP_UL) omits FLIP_UR entirely -- three independent sources
# agree Congo fits exactly one upper flipper (left).
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed Solenoid/Flasher Table (manual page 2-42) and Solenoid/Flashlamp Locations (2-43).
SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Kickback", 3: "2-Way Popper Up", 4: "2-Way Popper Down",
	5: "Ramp Diverter", 6: "Volcano Popper", 7: "Knocker", 8: "Top Loop Post",
	9: "Trough Eject", 10: "Left Slingshot", 11: "Right Slingshot",
	12: "Left Jet Bumper", 13: "Right Jet Bumper", 14: "Bottom Jet Bumper",
	# Resolved Gorilla Left/Right naming: see conflicting-printed-copies note in
	# evidence/excerpts/williams.congo.1995/solenoid-flasher-table.md.
	15: "Gorilla Left", 16: "Gorilla Right",
	17: "Amy Flasher", 18: "Left Ramp Flasher", 19: "2-Way Popper Flasher",
	20: "Skill Shot Flasher", 21: "Gray Gorilla Flasher", 22: "Map Eject",
	23: "Left Gate", 24: "Right Gate", 25: "Lower Right Flasher", 26: "Right Ramp Flasher",
	27: "Volcano Flasher", 28: "Perimeter Defense Flasher",
	33: "Upper Left Post", 34: "Mystery Eject",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-95 LPDC Output 37",
	38: "Unused WPC-95 LPDC Output 38",
	39: "Unused WPC-95 LPDC Output 39",
	40: "Unused WPC-95 LPDC Output 40",
	41: "Unused WPC-95 LPDC Mirror 41",
	42: "Unused WPC-95 LPDC Mirror 42",
	43: "Unused WPC-95 LPDC Mirror 43",
	44: "Unused WPC-95 LPDC Mirror 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# Manual solenoid/flasher table addresses that differ from the PinMAME public address: printed
# circuits 29-32 (Lwr Rt Power/Hold, Lwr Lt Power/Hold) map to public 45-48 (CORE_FIRSTLFLIPSOL=45).
# Printed 33-36 (Upr Rt/Lt Power/Hold) equal their own public addresses unchanged
# (CORE_FIRSTUFLIPSOL=33), because congoGameData's FLIP_SOL never routes 33/34 through any flipper
# path (no FLIP_UR bit) and the upper-left pair (35/36, FLIP_UL) already starts at 33+2=35.
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}

# address -> {control_connection (unique Drive Connections column), driver_transistor,
# power_connection (shared Voltage Connections bus), part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(power_connection="J133-2", driver_transistor="Q72", control_connection="J116-1", part_number="AE-23-800", printed_type="High Power"),
	2: dict(power_connection="J133-2", driver_transistor="Q68", control_connection="J116-2", part_number="AE-23-800", printed_type="High Power"),
	3: dict(power_connection="J133-2", driver_transistor="Q71", control_connection="J116-4", part_number="AE-23-800", printed_type="High Power"),
	4: dict(power_connection="J133-2", driver_transistor="Q67", control_connection="J116-5", part_number="AE-23-800", printed_type="High Power"),
	5: dict(power_connection="J133-2", driver_transistor="Q70", control_connection="J116-6", part_number="AE-26-1500", printed_type="High Power"),
	6: dict(power_connection="J133-2", driver_transistor="Q66", control_connection="J116-7", part_number="AE-23-800", printed_type="High Power"),
	7: dict(power_connection="J133-2", driver_transistor="Q69", control_connection="J116-8", part_number="AE-23-800", printed_type="High Power"),
	8: dict(power_connection="J133-2", driver_transistor="Q65", control_connection="J116-9", part_number="AE-26-1500", printed_type="High Power"),
	9: dict(power_connection="J133-3", driver_transistor="Q44", control_connection="J113-1", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(power_connection="J133-3", driver_transistor="Q48", control_connection="J113-3", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(power_connection="J133-3", driver_transistor="Q43", control_connection="J113-4", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(power_connection="J133-3", driver_transistor="Q47", control_connection="J113-5", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(power_connection="J133-3", driver_transistor="Q42", control_connection="J113-6", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(power_connection="J133-3", driver_transistor="Q46", control_connection="J113-7", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(power_connection="J133-3", driver_transistor="Q41", control_connection="J113-8", part_number="AE-25-1000", printed_type="Low Power"),
	16: dict(power_connection="J133-3", driver_transistor="Q45", control_connection="J113-9", part_number="AE-25-1000", printed_type="Low Power"),
	17: dict(power_connection="J133-6 / J134-5", driver_transistor="Q28", control_connection="J111-1 / J112-1", printed_type="Flasher"),
	18: dict(power_connection="J133-6", driver_transistor="Q32", control_connection="J111-2", printed_type="Flasher"),
	19: dict(power_connection="J133-6", driver_transistor="Q27", control_connection="J111-3", printed_type="Flasher"),
	20: dict(power_connection="J133-6 / J134-5", driver_transistor="Q31", control_connection="J111-4 / J112-5", printed_type="Flasher"),
	21: dict(power_connection="J133-6 / J134-5", driver_transistor="Q26", control_connection="J111-5 / J112-6", printed_type="Flasher"),
	22: dict(power_connection="J133-1", driver_transistor="Q30", control_connection="J111-6", part_number="AE-26-1200", printed_type="Flasher"),
	23: dict(power_connection="J133-1", driver_transistor="Q25", control_connection="J111-7", part_number="A-14406", printed_type="Flasher"),
	24: dict(power_connection="J133-1", driver_transistor="Q29", control_connection="J111-8", part_number="A-14406", printed_type="Flasher"),
	25: dict(power_connection="J133-6", driver_transistor="Q16", control_connection="J109-1", printed_type="Gen. Purpose"),
	26: dict(power_connection="J133-6", driver_transistor="Q15", control_connection="J109-2", printed_type="Gen. Purpose"),
	27: dict(power_connection="J133-6 / J134-5", driver_transistor="Q14", control_connection="J109-3 / J107-4", printed_type="Gen. Purpose"),
	28: dict(power_connection="J133-6 / J134-5", driver_transistor="Q13", control_connection="J109-4 / J107-5", printed_type="Gen. Purpose"),
	33: dict(power_connection="J119-6 (Red-Vio)", driver_transistor="Q84", control_connection="J120-6", part_number="AE-27-1200", printed_type="Fliptronic power"),
	34: dict(power_connection="J119-6 (Red-Vio)", driver_transistor="Q86", control_connection="J120-4", part_number="AE-26-1200", printed_type="Fliptronic hold"),
	35: dict(power_connection="J119-8 (Red-Gry)", driver_transistor="Q81", control_connection="J120-3", printed_type="Fliptronic power"),
	36: dict(power_connection="J119-8 (Red-Gry)", driver_transistor="Q83", control_connection="J120-1", part_number="FL-11630", printed_type="Fliptronic hold"),
	45: dict(power_connection="J119-1 (Red-Grn)", driver_transistor="Q90", control_connection="J120-13", printed_type="Fliptronic power"),
	46: dict(power_connection="J119-1 (Red-Grn)", driver_transistor="Q92", control_connection="J120-11", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(power_connection="J119-4 (Red-Blu)", driver_transistor="Q87", control_connection="J120-9", printed_type="Fliptronic power"),
	48: dict(power_connection="J119-4 (Red-Blu)", driver_transistor="Q89", control_connection="J120-7", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {
	45: "Yel-Grn", 46: "Org-Grn", 47: "Yel-Blu", 48: "Org-Blu",
	33: "Yel-Vio", 34: "Org-Vio", 35: "Yel-Gry", 36: "Org-Gry",
}

SOLENOID_ASSEMBLIES = {
	1: "A-20439", 2: "B-11873", 3: "A-20625", 4: "A-20625", 5: "A-20655", 6: "A-20680",
	7: "B-10686-1", 8: "A-20654", 9: "A-19963-1", 10: "B-9362-L-2", 11: "B-9362-R-3",
	12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2", 15: "A-20614", 16: "A-20614",
	17: "04-10321-2", 18: "A-17983", 19: "A-17983", 20: "A-17983", 21: "04-10094-1",
	22: "A-20453-1", 23: "A-20665", 24: "A-20665", 25: "A-17983", 26: "A-17983",
	27: "A-17983 / 04-10321-2", 28: "A-17803",
	33: "A-17932-1", 34: "A-20453-1", 35: "A-20738", 36: "A-20738",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
# Retained VPW-derived script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "Auto_Plunger (AutoPlunger.Fire)", 2: "Kick_Back (KickBack.Fire)",
	3: "SolPopUp (bsAmyVuk.SolOutAlt 0)", 4: "SolPopDown (bsAmyVuk.SolOutAlt 1)",
	5: "RampDiverter (Diverter.RotateToEnd, DiverterSwoop.IsDropped)",
	6: "bsVolcano.SolOut (exit via sw36a kicker)",
	7: 'vpmSolSound SoundFX("Knocker",DOFKnocker)',
	8: "SolTopPost (TopPost.IsDropped)", 9: "SolRelease (bsTrough.ExitSol_On, vpmTimer.PulseSw 31)",
	15: "GorillaRight sub (rotates GoFlipperLeft; see the resolved Left/Right naming note)",
	16: "GorillaLeft sub (rotates GoFlipperRight; see the resolved Left/Right naming note)",
	17: "SolModCallback 17 -> AdvFlash (F1L, F1L2)", 18: "SolModCallback 18 -> AdvFlash (F2L)",
	19: "SolModCallback 19 -> AdvFlash (F3L)", 20: "SolModCallback 20 -> AdvFlash (F4L)",
	21: "SolModCallback 21 -> AdvFlash (F5L, F5L2)", 22: "MapKick (bsMap.ExitSol_On)",
	23: "LeftGateOn (gate2.open)", 24: "RightGateOn (gate4.open)",
	25: "SolModCallback 25 -> AdvFlash (F6L)", 26: "SolModCallback 26 -> AdvFlash (F7L)",
	27: "SolModCallback 27 -> AdvFlash (F8L, F8L1, F8L2, F8L3)", 28: "SolModCallback 28 -> AdvFlash (F9L, F9L2)",
	33: "SolLeftpost (LeftPost.IsDropped)", 34: "MysteryKick (bsMystery.ExitSol_On)",
	36: "SolULFlipper (sULFlipper, ULeftFlipper)",
	46: "SolRFlipper (sLRFlipper)", 48: "SolLFlipper (sLLFlipper)",
}

FLASHER_BULBS = {
	17: ("#906 (1) on the playfield and #906 (1) on the backbox", 2, 2),
	18: ("#89 (1) on the playfield", 1, 1),
	19: ("#89 (1) on the playfield", 1, 1),
	20: ("#89 (1) on the playfield and #906 (1) on the backbox", 2, 1),
	21: ("#906 (1) on the playfield and #906 (1) on the backbox", 2, 2),
	25: ("#89 (1) on the playfield", 1, 1),
	26: ("#89 (1) on the playfield", 1, 1),
	27: ("#89 (2) and #906 (1) on the playfield, #906 (1) on the backbox", 4, 3),
	28: ("#89 (1) on the playfield and #906 (1) on the backbox", 2, 2),
}

# --- Printed lamp matrix (manual page 2-38 wiring, 2-39 locations). First digit is the column.
LAMP_LABELS = {
	11: "(C)ongo", 12: "C(o)ngo", 13: "Co(n)go", 14: "Con(g)o", 15: "Cong(o)",
	16: "(A)my", 17: "A(m)y", 18: "Am(y)",
	21: "Zi(n)j", 22: "Zin(j)", 23: "Jet Extra Collect", 24: "Jungle Jackpot",
	25: "Skill Fire", 26: "You", 27: "Map", 28: "Diamond Right Eject",
	31: "Autofire", 32: "Right Ramp Extra Ball", 33: "Right Ramp Collect",
	34: "Diamond Right Ramp", 35: "Left Eject Eye", 36: "Diamond Left Eject",
	37: "Mystery", 38: "Right Ramp Jackpot",
	41: "Diamond Left Loop", 42: "We Are", 43: "Left Loop Extra Ball", 44: "Left Loop Lock",
	45: "Left Bank Bottom", 46: "Skill Shot", 47: "Left Bank Center", 48: "Left Bank Top",
	51: "Left Ramp 1", 52: "Left Ramp 2", 53: "Left Ramp 3", 54: "Diamond Left Ramp",
	55: "Left Ramp Jackpot", 56: "(Z)inj", 57: "Z(i)nj", 58: "Kickback",
	61: "Diamond Inner Loop", 62: "(G)ray", 63: "G(r)ay", 64: "Gr(a)y", 65: "Gra(y)",
	66: "Watching", 67: "Satellite Left", 68: "Super Score",
	71: "Travi", 72: "Com", 73: "Mine Shaft", 74: "Upper Loop Lock", 75: "Diamond Upper Loop",
	76: "Satellite Right", 77: "Satellite Center", 78: "Perimeter Defense",
	81: "(H)ippo", 82: "H(i)ppo", 83: "Hi(p)po", 84: "Hip(p)o", 85: "Hipp(o)",
	86: "Shoot Again", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-20603", "#555"), 12: ("A-20603", "#555"), 13: ("A-20603", "#555"),
	14: ("A-20603", "#555"), 15: ("A-20603", "#555"),
	16: ("A-20601", "#555"), 17: ("A-20601", "#555"), 18: ("A-20601", "#555"),
	21: ("A-20605", "#555"), 22: ("A-20605", "#555"), 23: ("A-20605", "#555"),
	24: ("A-20605", "#555"), 25: ("A-20605", "#555"), 26: ("A-20605", "#555"),
	27: ("A-20605", "#555"), 28: ("A-20605", "#555"),
	31: ("A-20605", "#555"), 32: ("A-20697", "#555"), 33: ("A-20697", "#555"),
	34: ("A-20697", "#555"), 35: ("A-20697", "#555"), 36: ("A-20697", "#555"),
	37: ("A-20697", "#555"), 38: ("A-17835", "#44"),
	41: ("A-20606", "#555"), 42: ("A-20606", "#555"), 43: ("A-20606", "#555"), 44: ("A-20606", "#555"),
	45: ("A-20602", "#555"), 46: ("A-20602", "#555"), 47: ("A-20602", "#555"), 48: ("A-20602", "#555"),
	51: ("A-20620", "#555"), 52: ("A-20620", "#555"), 53: ("A-20620", "#555"),
	54: ("A-20620", "#555"), 55: ("A-20620", "#555"),
	56: ("A-17835", "#44"), 57: ("A-17835", "#44"), 58: ("A-17835", "#44"),
	61: ("A-20607", "#555"), 62: ("A-20607", "#555"), 63: ("A-20607", "#555"),
	64: ("A-20607", "#555"), 65: ("A-20607", "#555"), 66: ("A-20607", "#555"),
	67: ("A-20607", "#555"), 68: ("A-17807", "#44"),
	71: ("A-20607", "#555"), 72: ("A-20607", "#555"), 73: ("A-20607", "#555"),
	74: ("A-20607", "#555"), 75: ("A-20607", "#555"), 76: ("A-20607", "#555"),
	77: ("A-20607", "#555"), 78: ("A-17835", "#44"),
	81: ("A-20600", "#555"), 82: ("A-20600", "#555"), 83: ("A-20600", "#555"),
	84: ("A-20600", "#555"), 85: ("A-20600", "#555"), 86: ("A-17807", "#44"),
	88: ("20-9663-1", None),
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
# Co-located Light objects stacked purely for brightness (l32l/l33l/l38l/l81l style pairs); the
# retained table has no printed multi-bulb quantity for any lamp address, so the primary object is
# used and the duplicate is documented render doubling.
LAMP_RENDER_DOUBLES = {32, 33, 38, 81}
# Item 72 prints "Corn" on the Lamp Locations page (2-39) but "COM" on the Lamp Matrix page (2-38)
# and the co-located switch 52 prints "Com" on both of its own pages; items 51/52 ("Travi"/"Com")
# spell "TRAVICOM", Karen Ross's company in the 1995 Congo film. Three of four printed mentions
# agree, so "Com" is used and "Corn" is treated as the typographic slip.
LAMP_MATRIX_PAGE_TYPOS = {72: "Corn"}

GI_STRINGS = {
	0: ("Playfield Gorilla", "J105-1 / J106-1", "Q5", "J105-7 / J106-7", "#555"),
	1: ("Playfield Top", "J105-2", "Q4", "J105-8", "#44"),
	2: ("Playfield Bottom", "J105-3 / J106-3", "Q3", "J105-9 / J106-9", "#44"),
	3: ("Backbox String 1", "J106-5", "Q2", "J106-10", "#555"),
	4: ("Backbox String 2", "J106-6 / J104-3", "Q1", "J106-11 / J104-1", "#555"),
}

# --- Normalized playfield coordinates derived from the retained JPSalas/nFozzy VP10 extraction
# (x/964, y/2162; review-artifacts/congo/vpx-geometry.txt, gameitems/*.json).
SWITCH_POSITIONS = {
	11: [(0.160887, 0.127649)], 12: [(0.921779, 0.144532)], 15: [(0.923854, 0.591225)],
	16: [(0.058869, 0.820537)], 17: [(0.765140, 0.748602)], 18: [(0.944860, 0.892986)],
	26: [(0.130026, 0.749171)], 27: [(0.856426, 0.746289)], 28: [(0.723613, 0.531134)],
	# 31-35: projected onto the trough's own release kicker (Kicker BallRelease); see SWITCH_PROJECTIONS.
	31: [(0.887545, 0.883389)], 32: [(0.887545, 0.883389)], 33: [(0.887545, 0.883389)],
	34: [(0.887545, 0.883389)], 35: [(0.887545, 0.883389)],
	36: [(0.715768, 0.067068)],
	# 41-43: projected onto the Volcano lock's own exit kicker (Kicker sw36a); see SWITCH_PROJECTIONS.
	41: [(0.776193, 0.087997)], 42: [(0.776193, 0.087997)], 43: [(0.776193, 0.087997)],
	37: [(0.617894, 0.424607)], 38: [(0.809582, 0.510754)],
	44: [(0.656380, 0.135870)], 45: [(0.060005, 0.233570)],
	46: [(0.111450, 0.531366)], 47: [(0.111450, 0.554955)], 48: [(0.111968, 0.577388)],
	51: [(0.427256, 0.202070)], 52: [(0.498833, 0.210164)], 53: [(0.524896, 0.160615)],
	54: [(0.138421, 0.328660)], 55: [(0.283908, 0.278937)], 56: [(0.557248, 0.396941)],
	57: [(0.194375, 0.267196)], 58: [(0.304875, 0.118939)],
	61: [(0.216599, 0.745131)], 62: [(0.679742, 0.744409)],
	63: [(0.671371, 0.361483)], 64: [(0.910371, 0.348552)], 65: [(0.833121, 0.442076)],
	67: [(0.893749, 0.209999)], 68: [(0.657158, 0.070537)],
	71: [(0.395488, 0.081522)], 72: [(0.492998, 0.081984)], 73: [(0.588434, 0.081984)],
	74: [(0.302732, 0.670127)], 75: [(0.365568, 0.692603)], 76: [(0.451629, 0.701100)],
	77: [(0.530861, 0.692329)], 78: [(0.593697, 0.669854)],
}
SWITCH_PROJECTIONS = {
	31: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center): the retained cvpmTrough helper (bsTrough) models switches 32-35 purely as an internal switch array with no separate playfield trigger object, and the trough-eject opto is pulsed in the same SolRelease handler that fires the BallRelease kicker.",
	32: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31. The retained cvpmTrough helper has no separate visible object per ball position.",
	33: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	34: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	35: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	41: "Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center): the retained cvpmTrough helper (bsVolcano) models switches 41-43 purely as an internal switch array with no separate playfield trigger object, and the volcano ejects a locked ball through the same sw36a kicker (.Initexit sw36a).",
	42: "Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.",
	43: "Projected onto the Volcano lock's own exit kicker (Kicker sw36a, table object center); see switch 41.",
}

SOLENOID_POSITIONS = {
	1: [(0.943724, 0.950009)], 2: [(0.060945, 0.887141)],
	3: [(0.524896, 0.160615)], 4: [(0.524896, 0.160615)],
	5: [(0.837075, 0.594063)], 6: [(0.776193, 0.087997)],
	8: [(0.707168, 0.015879)], 9: [(0.887545, 0.883389)],
	10: [(0.216599, 0.745131)], 11: [(0.679742, 0.744409)],
	12: [(0.671371, 0.361483)], 13: [(0.910371, 0.348552)], 14: [(0.833121, 0.442076)],
	15: [(0.416494, 0.494269)], 16: [(0.478734, 0.494032)],
	17: [(0.139523, 0.012257), (0.114627, 0.016883)],
	18: [(0.174793, 0.198196)],
	19: [(0.459025, 0.205905)],
	20: [(0.056017, 0.546254)],
	21: [(0.452801, 0.472671), (0.450726, 0.508094)],
	22: [(0.809582, 0.510754)],
	23: [(0.339147, 0.030537)],
	24: [(0.642246, 0.029981)],
	25: [(0.946577, 0.642789)],
	26: [(0.891021, 0.223310)],
	27: [(0.787863, 0.096438), (0.787863, 0.096438), (0.789938, 0.069714)],
	28: [(0.529888, 0.396002), (0.503112, 0.413506)],
	33: [(0.081925, 0.244521)],
	34: [(0.617894, 0.424607)],
	35: [(0.046680, 0.438945)], 36: [(0.046680, 0.438945)],
	45: [(0.618750, 0.861001)], 46: [(0.618750, 0.861001)],
	47: [(0.278750, 0.861001)], 48: [(0.278750, 0.861001)],
}

GI_POSITIONS = {
	0: [
		(0.598128, 0.623034), (0.604512, 0.642692), (0.297718, 0.644542),
		(0.302386, 0.621878), (0.456718, 0.656388),
	],
	1: [
		(0.149896, 0.024283), (0.391598, 0.136679), (0.444502, 0.077475),
		(0.538900, 0.078862), (0.720436, 0.203747), (0.265041, 0.193571),
		(0.110477, 0.214847), (0.590768, 0.380435), (0.071058, 0.061286),
		(0.669573, 0.360718), (0.904013, 0.346988), (0.829324, 0.443657),
		(0.491766, 0.229128),
	],
	2: [
		(0.028518, 0.515337), (0.046691, 0.568475), (0.749382, 0.497194),
		(0.861505, 0.521045), (0.830385, 0.567299), (0.922709, 0.620028),
		(0.911298, 0.648705), (0.209607, 0.779100), (0.175363, 0.829299),
		(0.718124, 0.827089), (0.877066, 0.717623), (0.874991, 0.790703),
		(0.468426, 0.745779), (0.685183, 0.777839), (0.210986, 0.782493),
		(0.687471, 0.781878),
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
		raise RuntimeError(f"Congo retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Congo extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Congo retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Congo retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Congo retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the congo_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/congo.c congoGameData GEN_WPC95 with wpc_dispDMD, "
				"FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_UL), the inverted-switch mask "
				"{0x00,0x00,0x00,0x3f,0x07,...}, swStart/swTilt/swSlamTilt/swCoinDoor/swLaunch defines, "
				"congoDCSGameData (GEN_WPC95DCS) bound only to driver congo_20s10k by init_congo's "
				"strncasecmp check, and init_congo's wpc_set_fastflip_addr(0x80); src/wpc/gen.h "
				"GEN_WPC95/GEN_WPC95DCS definitions; src/wpc/core.h CORE_FIRSTUFLIPSOL=33, "
				"CORE_FIRSTLFLIPSOL=45, and the sURFlip/sURFlipPow/sULFlip/sULFlipPow/sLRFlip/sLRFlipPow/"
				"sLLFlip/sLLFlipPow offsets; src/wpc/wpc.c GENWPC_HASWPC95=(GEN_WPC95|GEN_WPC95DCS) and "
				"GENWPC_HASFLIPTRON; src/wpc/core.c core_getSol WPC-95 37..40 to 41..44 duplication; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95=0x80 (\"Integrated boards, Congo "
				"3/96 - Cactus Canyon 2/99\") and PINMAME_HARDWARE_GEN_WPC95DCS=0x40 (\"Hybrid WPC95 "
				"driver + DCS sound, Who Dunnit\")"
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
			"uri": "external:pinmame-manuals/by-machine/williams.congo.1995/archive-arcademanual_Congo_OPS/Congo_OPS.pdf",
			"original_filename": "Congo_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"143-page Williams Congo Operations Manual (16-50050-101, November 1995, FINAL), a Paper "
				"Capture OCR scan with a usable but imperfect text layer. Printed pages 2-38 through 2-43 "
				"carry the lamp/switch/solenoid matrix wiring and locations tables and the general "
				"illumination and flipper-circuit tables; PDF page 2 (front matter, unnumbered) carries a "
				"duplicate DIP switch chart and a duplicate Solenoid/Flasher Table; PDF page 118 (printed "
				"3-5) carries a third copy of the Solenoid/Flasher Table beside the Section 3 schematics."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.congo.switch-locations",
					"locator": "PDF page 110, printed 2-41, Switch Locations parts list",
					"path": "evidence/excerpts/williams.congo.1995/switch-locations.md",
					"sha256": "a239ecfc3ca259d997ab447bae310877ac20a14f8fd43128a8cf92d0fb709788",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.switch-matrix",
					"locator": "PDF page 109, printed 2-40, SWITCH MATRIX table",
					"path": "evidence/excerpts/williams.congo.1995/switch-matrix.md",
					"sha256": "dfbc20f355661c0591c0a0903ae52716f1fa7a5d95ffac162b8e0cbd3de69974",
					"image": "evidence/excerpts/williams.congo.1995/switch-matrix.webp",
					"image_sha256": "2fc9c7842935e9e0b68f7b412395af9c50a9a285730353935aaffffe39858a55",
					"image_derivation": "Congo_OPS.pdf page 109, crop box 0.06,0.08,0.98,0.62 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 78 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.lamp-locations",
					"locator": "PDF page 108, printed 2-39, Lamp Locations parts list",
					"path": "evidence/excerpts/williams.congo.1995/lamp-locations.md",
					"sha256": "0490f2fe67deaba27451640045371936695f4f7a97b701c1ce6dd92e6e5ad838",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.lamp-matrix",
					"locator": "PDF page 107, printed 2-38, LAMP MATRIX table",
					"path": "evidence/excerpts/williams.congo.1995/lamp-matrix.md",
					"sha256": "67263bbc4ad51f56f381dd30053ba1a8363b44928c3972cce0f5552db15ab33c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.solenoid-flasher-table",
					"locator": "PDF page 111, printed 2-42, SOLENOID/FLASHER TABLE, General Illumination, and Flipper Circuits",
					"path": "evidence/excerpts/williams.congo.1995/solenoid-flasher-table.md",
					"sha256": "086b0949f1b5515672907f266e01d9dbb4383161eaf19ed4e62597e808672328",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.solenoid-flashlamp-locations",
					"locator": "PDF page 112, printed 2-43, Solenoid/Flashlamp Locations, Flippers, and General Illumination",
					"path": "evidence/excerpts/williams.congo.1995/solenoid-flashlamp-locations.md",
					"sha256": "9d995116ed35c57fc75c80bc95e1349a4671dabdb6a0974a9e88f481ebaeb7d5",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.congo.dip-switch-chart",
					"locator": "PDF page 2 (front matter, unnumbered), DIP Switch Chart and duplicate Solenoid/Flasher Table",
					"path": "evidence/excerpts/williams.congo.1995/dip-switch-chart.md",
					"sha256": "76311d6972ea3bd3e9dffa169d71c792867b9b2557d0b1d66aa1c2d759b90a93",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/congo/manual-transcription.md",
			"revision": "2026-08-07",
			"locator": (
				"Retained human transcription summary of every rendered manual table used by this "
				"definition, cross-referencing the individual excerpts above, together with the rendered "
				"PNG page cache under external:pinmame-manuals/rendered/williams.congo.1995/."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/congo-1995/source/Congo%20%28Williams%201995%29%201.1.vpx",
			"original_filename": "Congo (Williams 1995) 1.1.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working recreation of the physical machine (original VP9 table by JPSalas, "
				"VP10 conversion by nFozzy, spotlight primitive by Dark, flasher images by LoadedWeapon), "
				f"binding driver \"congo_21\". Exact playfield bounds are {TABLE_BOUNDS}; normalized "
				"coordinates are x/964 and y/2162. Geometry authority only for named table objects. This is "
				"a thin table (925 extracted files, far fewer than richer WPC-95 recreations in this "
				"project), so several mechanism-internal sensors have no dedicated playfield object and are "
				"documented projections rather than validated coordinates."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, nFozzy, Dark, LoadedWeapon",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/congo-1995/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (72,923 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "congo_21", Const UseSolenoids = 1, Const UseVPMModSol = 1 (PWM-modulated '
				"flashers via SolModCallback/AdvFlash), the SolCallback table for solenoids 1-9, 15-16, "
				"22-24, 33 plus core.vbs sLRFlipper/sLLFlipper/sULFlipper, the Controller.Switch and "
				"vpmTimer.PulseSw switch semantics for the trough/volcano/two-way-popper/mystery/map/gray-"
				"gorilla state machines, GICallback2 UpdateGi mapping GI 0/1/2 to the GiGorilla/GiTop/"
				"GIBottom playfield emitter collections, and the GorillaRight/GorillaLeft mechanism subs "
				"that swing the GoFlipperLeft/GoFlipperRight primitives and rock the gorilla figure "
				"(Gorilla.objRotZ)."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas, nFozzy",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/congo-1995/extracted-vpxtool.manifest.json",
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
			unused = address in UNUSED_MATRIX_ADDRESSES
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
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the Switch Locations parts list both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					" Printed on the switch-locations parts list with an LED/photo-transistor opto pair and "
					"no separate switch part number, and shaded \"OPTO, TYPICALLY CLOSED\" on the printed "
					"switch matrix. PinMAME's congoGameData inverted-switch mask ({0x00,0x00,0x00,0x3f,0x07,"
					"...}, column 3 bits 0-5 and column 4 bits 0-2) covers this exact address, so the public "
					"switch state is already normalized and must not be inverted again -- a clean sweep with "
					"zero disagreement between the manual and the emulator across all nine opto addresses "
					"(31-36, 41-43)."
				)
			if address == 24:
				notes += " Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 45:
				notes += ' Printed part number transcribed verbatim as "5647-12393-19" (every other rollover switch on this machine prints the "5647-12693-" prefix); the manual print is preserved rather than silently corrected.'
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if address == 25:
				notes += (
					" No VPX object supplies a reliable coordinate for this switch: the retained extraction's "
					"only candidate, a Primitive literally named \"sw25\", sits at local-space (684.0966, "
					"1112.3384) -- the exact same coordinate as an unrelated Primitive named \"sw1\" (not a "
					"valid Congo switch address), indicating both are copies of a reusable decorative mesh "
					"whose position field was never updated to the object's real placement. Left unresolved "
					"rather than invented; see coverage.missing."
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
				label = f"Not Used Matrix Position {address}"
				refs = (MANUAL_SOURCE, CONTROLLER_SOURCE)
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
					physical["location"] = "cabinet interior" if address != 13 else "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address == 25:
					pass  # spatial intentionally omitted -- see notes above and coverage.missing.
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None, True, [(0.618750, 0.861001)]),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316", True, [(0.618750, 0.861001)]),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None, True, [(0.278750, 0.861001)]),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316", True, [(0.278750, 0.861001)]),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, False, None),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, "A-17316", True, None),
		117: ("Upper Left Flipper EOS", "internal.flipper.upper.left.eos", "used", False, "leaf", "SW-1A-194", None, True, [(0.046680, 0.438945)]),
		118: ("Upper Left Flipper Button", "flipper.upper.left.button", "used", True, "opto", None, "A-17316", True, [(0.046680, 0.438945)]),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly, keep_wiring, position) in flipper_inputs.items():
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
				" Congo has no upper-right flipper: the Switch Locations page marks this position Not Used "
				"(both the assembly and switch part columns print NOT USED), the manual's Solenoid/Flasher "
				"Table has no \"Upper Right Flipper\" row at all (the printed Upr. Rt. slot instead drives "
				"Upper Left Post and Mystery Eject, ordinary non-flipper coils), and congoGameData's "
				"FLIP_SOL(FLIP_L | FLIP_UL) omits the FLIP_UR bit entirely -- three independent sources agree."
			)
			physical["location"] = "not installed"
			if keep_wiring:
				notes += (
					" The switch-matrix wiring page nonetheless shades this position as an opto on the reused "
					"Flipper Opto assembly template (A-17316, same construction as the fitted flipper button "
					"optos 112/114/118), so its printed construction is recorded even though no physical "
					"switch is installed."
				)
			else:
				notes += " The matrix-page wiring for this position is drawn as a plain (non-opto) end-of-stroke leaf, matching the fitted flipper EOS template."
		elif switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed. WPC-95 reads the flipper column through "
				"WPC_FLIPPERSW95 with a hardware inversion, so the public switch state is already normalized."
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
			extra["spatial"] = (
				not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if role.endswith(".button")
				else located(f"switch.generic-{address}", "sensor", position, VPX_TABLE_SOURCE)
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
					"location": "WPC-95 CPU board U27",
					"switch_type": "dip",
					"notes": (
						"WPC-95 CPU-board country/option configuration DIP bank. The retained manual's own DIP "
						"Switch Chart (front matter, PDF page 2) documents five country combinations (America, "
						"European, French, German, Spain) across SW1-SW8; the DIP Switch Test (T.15) description "
						"states only that it \"shows the positions of the DIP switches on the CPU board (U27)\" "
						"with no further per-bit function documented."
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
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			if 17 <= address <= 21 or 25 <= address <= 28:
				kind = "flasher"
			elif address in {35, 36, 45, 46, 47, 48}:
				kind = "coil"
			else:
				kind = "coil"
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
						" Only the playfield-visible bulb(s) have a playfield placement; the backbox bulb has "
						"no coordinate in the retained thin table."
					)
			if address in {22, 23, 24}:
				notes += (
					" The printed \"Solenoid Type\" column names this the \"Flasher\" driver-board circuit "
					"bank (shared with the five genuine light flashers 17-21), not a literal flashlamp: this "
					"is an ordinary kicker/gate coil wired through that bank's transistor section."
				)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {15, 16}:
				notes += (
					" Left/Right naming resolved from a manual self-contradiction: the printed Solenoid/"
					"Flasher Table at 2-42 (PDF page 111) reads 15 \"Gorilla Right\"/16 \"Gorilla Left\", but "
					"two other printed copies of the same table (front-matter PDF page 2 and the Section 3 "
					"copy at PDF page 118) both read the opposite, and the retained script's own object "
					"manipulation (which of the two GoFlipperLeft/GoFlipperRight primitives actually rotates) "
					"agrees with the front-matter/Section-3 reading rather than page 111's. See "
					"evidence/excerpts/williams.congo.1995/solenoid-flasher-table.md."
				)
			if address in {33, 34}:
				notes += (
					" This address sits in the Fliptronic \"Upr. Rt.\" driver-board slot (CORE_FIRSTUFLIPSOL=33) "
					"but Congo has no upper-right flipper; congoGameData's FLIP_SOL(FLIP_L | FLIP_UL) never "
					"routes 33/34 through any flipper-coil path, so they pass straight through as ordinary "
					"public solenoids with no address translation."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the "
					"same circuits 29-32; the manual address is preserved as an alias."
				)
			if address in {35, 36}:
				notes += (
					" Genuine upper-left flipper circuit (CORE_FIRSTUFLIPSOL+2/+3); the printed circuit number "
					"already equals the public address, so no alias is needed."
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
			availability = "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in SOLENOID_POSITIONS:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			else:
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Congo playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Congo playfield device.",
			31: "PinMAME's synthetic game-on state. Congo sets wpc_set_fastflip_addr(0x80), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			37: "Unused WPC-95 LPDC general-purpose output; Congo has no DC-motor mechanism and populates no LPDC output.",
			38: "Unused WPC-95 LPDC general-purpose output; Congo has no DC-motor mechanism and populates no LPDC output.",
			39: "Unused WPC-95 LPDC general-purpose output; Congo has no DC-motor mechanism and populates no LPDC output.",
			40: "Unused WPC-95 LPDC general-purpose output; Congo has no DC-motor mechanism and populates no LPDC output.",
			41: "Unused WPC-95 LPDC mirror of output 37; both the real output and its mirror are unpopulated.",
			42: "Unused WPC-95 LPDC mirror of output 38; both the real output and its mirror are unpopulated.",
			43: "Unused WPC-95 LPDC mirror of output 39; both the real output and its mirror are unpopulated.",
			44: "Unused WPC-95 LPDC mirror of output 40; both the real output and its mirror are unpopulated.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. congoGameData declares no custSol.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
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
			if address in LAMP_MATRIX_PAGE_TYPOS:
				notes += (
					f' The Lamp Locations page (2-39) prints this insert as "{LAMP_MATRIX_PAGE_TYPOS[address]}"; '
					"the Lamp Matrix page (2-38) and the co-located switch 52 (printed on both its own pages) "
					'agree on "Com", and lamps 71/72 together spell "TRAVICOM" (Karen Ross\'s company in the '
					"1995 Congo film), so \"Com\" is used here."
				)
			if address == 88:
				notes += " Cabinet button lamp inside the illuminated start button assembly, sharing its assembly part number with switch 13."
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
				label = "Not Used Lamp Position 87"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The Lamp Locations page marks this position Not Used."
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				if address in LAMP_RENDER_DOUBLES:
					physical["notes"] += (
						f" The retained table stacks a second co-located Light object (l{address}l) purely for "
						"brightness; the primary object is used and the duplicate is documented render "
						"doubling, matching the manual's single-bulb entry."
					)
				position = LAMP_POSITIONS[address]
				extra["spatial"] = located(identifier, "emitter", position, VPX_TABLE_SOURCE)
				if address == 62:
					physical["notes"] += (
						" The retained table names this object \"L62\" (uppercase) rather than the lowercase "
						"\"lNN\" convention every other lamp address uses; the position is otherwise ordinary."
					)
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
	11: [(0.335416, 0.622917)], 12: [(0.384763, 0.603653)], 13: [(0.446058, 0.601469)],
	14: [(0.512610, 0.602625)], 15: [(0.559356, 0.622890)],
	16: [(0.423042, 0.032233)], 17: [(0.493063, 0.032695)], 18: [(0.561463, 0.032377)],
	21: [(0.765041, 0.685361)], 22: [(0.858402, 0.684783)], 23: [(0.813084, 0.628035)],
	24: [(0.690482, 0.637142)], 25: [(0.717388, 0.610170)], 26: [(0.695475, 0.556458)],
	27: [(0.742933, 0.583285)], 28: [(0.766792, 0.557672)],
	31: [(0.795124, 0.658360)], 32: [(0.714471, 0.446519)], 33: [(0.745980, 0.408418)],
	34: [(0.686268, 0.475225)], 35: [(0.618192, 0.486095)], 36: [(0.568270, 0.508875)],
	37: [(0.549469, 0.475457)], 38: [(0.797070, 0.348173)],
	41: [(0.110996, 0.395698)], 42: [(0.153138, 0.356383)], 43: [(0.087785, 0.341640)],
	44: [(0.071706, 0.306256)], 45: [(0.156999, 0.579646)], 46: [(0.248071, 0.572716)],
	47: [(0.156402, 0.555154)], 48: [(0.156428, 0.530380)],
	51: [(0.300592, 0.471731)], 52: [(0.284613, 0.440965)], 53: [(0.267808, 0.410178)],
	54: [(0.254538, 0.381129)], 55: [(0.238200, 0.350775)], 56: [(0.060947, 0.684768)],
	57: [(0.129149, 0.684771)], 58: [(0.061333, 0.750737)],
	61: [(0.335840, 0.159921)], 62: [(0.323587, 0.185592)], 63: [(0.326180, 0.211494)],
	64: [(0.329162, 0.237454)], 65: [(0.331691, 0.263356)], 66: [(0.300603, 0.306632)],
	67: [(0.396979, 0.258962)], 68: [(0.634531, 0.202966)],
	71: [(0.403527, 0.225139)], 72: [(0.488784, 0.233927)], 73: [(0.577736, 0.229099)],
	74: [(0.607235, 0.292438)], 75: [(0.556924, 0.314870)], 76: [(0.488330, 0.289142)],
	77: [(0.441909, 0.275382)], 78: [(0.496693, 0.400396)],
	81: [(0.915451, 0.407402)], 82: [(0.938032, 0.436682)], 83: [(0.950480, 0.466677)],
	84: [(0.950602, 0.497751)], 85: [(0.949520, 0.527901)], 86: [(0.449818, 0.914720)],
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		if address == 2:
			notes += (
				' The Solenoid/Flashlamp Locations page (2-43) prints this string\'s own bulb number as '
				'"24-8549", which matches none of that page\'s own four legend codes; the Solenoid/Flasher '
				'Table page (2-42) states the bulb type directly as "#44" for this same string, which is used '
				"here as the more legible source."
			)
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
				"coordinate come from the retained table's GI emitter collection for this string "
				"(UpdateGi/UpdateGiOn in the retained script). GI address 0 drives collection GiGorilla; GI "
				"address 1 drives GiTop; GI address 2 drives GIBottom."
			)
			if address == 1:
				notes += (
					" GiTop contains 14 members; one (GI10_Deactivated) is excluded here as a table modeling "
					"anomaly (its own name marks it disabled) rather than a distinct active physical bulb, "
					"leaving 13 placements."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite; the retained script's UpdateGi/"
				"UpdateGiOn handle only GI addresses 0-2, so this string has no playfield coordinate."
			)
			if address == 4:
				notes += " This string additionally feeds a cabinet bulb through J104, the only cabinet connection on the printed general-illumination wiring."
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
			"Four balls rest on trough optos 32-35; the retained script's cvpmTrough helper (bsTrough) reads "
			"them as a plain switch array [32,33,34,35] with the ball nearest the shooter lane at 32 and the "
			"drain entrance at 35, and ejects the ball resting on 32 through solenoid 9 (Trough Eject), pulsing "
			"trough-eject opto 31 in the same SolRelease event. All five positions are printed optos that rest "
			"closed, normalized by PinMAME's column-3 inverted-switch mask bits.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"Congo has no manual plunger. The ball ejected from the trough rests on shooter-lane switch 18 and "
			"auto-plunger coil 1 launches it when the cabinet Launch key is pressed.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20439",
		),
		mechanism(
			"mechanism.kickback",
			"Left outlane kickback",
			"kicker",
			[output_id("Kickback")],
			["switch.matrix-16"],
			"Solenoid 2 (Kickback) returns a ball that has drained down the left outlane (switch 16) back to "
			"the playfield. The manual's own rule card states the feature is re-lit by completing the Left "
			"Bank three-target bank (switches 46/47/48).",
			[("outlane", "Ball in left outlane", ["switch.matrix-16"], "Left outlane switch.")],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="B-11873",
		),
		mechanism(
			"mechanism.two-way-popper",
			"Two-way popper (Amy VUK)",
			"kicker",
			[output_id("2-Way Popper Up"), output_id("2-Way Popper Down")],
			["switch.matrix-53"],
			"A single saucer (the retained script's bsAmyVuk, a cvpmSaucer) at switch 53 can eject a captured "
			"ball in either of two directions: solenoid 3 fires the primary (up/forward) kick and solenoid 4 "
			"fires the alternate (down) kick. Adjustment A.2 20 (\"Amy Feed Disabled\") lets an operator force "
			"every ball to the down direction only, described in the manual as a workaround \"for use when the "
			"Amy ramp or Two-way popper are broken\", indicating this popper normally feeds the Amy ramp/Gray "
			"Gorilla complex.",
			[("held", "Ball captured in the two-way popper", ["switch.matrix-53"], "2-Way Popper switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20625",
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Ramp diverter",
			"diverter",
			[output_id("Ramp Diverter")],
			[],
			"Solenoid 5 rotates a diverter flap (Diverter) between two ramp paths and toggles a companion "
			"drop-away guide (DiverterSwoop) in the same motion; the manual documents no dedicated switch for "
			"this device, only the coil.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20655",
		),
		mechanism(
			"mechanism.volcano",
			"Volcano three-ball lock and popper",
			"kicker",
			[output_id("Volcano Popper")],
			["switch.matrix-36", "switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
			"A ball entering the Volcano is sensed by the Volcano Stack entrance opto (switch 36, which also "
			"feeds it into the retained script's second cvpmTrough helper bsVolcano) and then rests on one of "
			"three lock optos (41-43, read as a plain switch array with no separate playfield object). Solenoid "
			"6 (Volcano Popper) ejects a locked ball back to the playfield through the same kicker object "
			"(sw36a) that models the entrance.",
			[
				("entry", "Ball entering the Volcano", ["switch.matrix-36"], "Volcano Stack entrance opto."),
				("lock-1", "Volcano Lock Ball 1", ["switch.matrix-41"], "First lock position."),
				("lock-2", "Volcano Lock Ball 2", ["switch.matrix-42"], "Second lock position."),
				("lock-3", "Volcano Lock Ball 3", ["switch.matrix-43"], "Third lock position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20680",
		),
		mechanism(
			"mechanism.top-loop-post",
			"Top loop post",
			"gate",
			[output_id("Top Loop Post")],
			["switch.matrix-12"],
			"Solenoid 8 raises and lowers a post (TopPost) that blocks or admits the Upper Loop shot (switch "
			"12); the retained script initializes the post raised (blocking) at power-on.",
			[("loop", "Ball completing the Upper Loop", ["switch.matrix-12"], "Upper Loop switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20654",
		),
		mechanism(
			"mechanism.mystery-saucer",
			"Mystery saucer",
			"kicker",
			[output_id("Mystery Eject")],
			["switch.matrix-37"],
			"A ball captured at switch 37 (Mystery Eject) is held and then kicked back to the playfield by "
			"solenoid 34 through the same saucer object (the retained script's bsMystery, a cvpmSaucer).",
			[("held", "Ball captured in the Mystery saucer", ["switch.matrix-37"], "Mystery Eject switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="5647-12693-43",
		),
		mechanism(
			"mechanism.map-saucer",
			"Map saucer",
			"kicker",
			[output_id("Map Eject")],
			["switch.matrix-38"],
			"A ball captured at switch 38 (Right Eject) is held and then kicked back to the playfield by "
			"solenoid 22 (Map Eject) through the same saucer object (the retained script's bsMap, a "
			"cvpmSaucer).",
			[("held", "Ball captured in the Map saucer", ["switch.matrix-38"], "Right Eject switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20453-1",
		),
		mechanism(
			"mechanism.gates",
			"Left and right one-way gates",
			"gate",
			[output_id("Left Gate"), output_id("Right Gate")],
			[],
			"Two solenoid-operated one-way gates (gate2 solenoid 23, gate4 solenoid 24) admit a ball into a "
			"loop or lane while blocking return travel; the retained script's LeftGateOn/RightGateOn handlers "
			"toggle each gate's own .open property directly. The manual documents no dedicated switch for "
			"either gate.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20665",
		),
		mechanism(
			"mechanism.upper-left-post",
			"Upper left post",
			"gate",
			[output_id("Upper Left Post")],
			[],
			"Solenoid 33 raises and lowers a post (LeftPost, with a companion invisible collision proxy "
			"LeftPost_invis) despite sitting in the Fliptronic driver board's printed \"Upr. Rt.\" circuit "
			"slot; Congo has no upper-right flipper, so this address is an ordinary post coil rather than "
			"flipper hardware.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17932-1",
		),
		mechanism(
			"mechanism.gray-gorilla",
			"Underground Gray Gorilla mini-playfield",
			"motorized",
			[output_id("Gorilla Left"), output_id("Gorilla Right")],
			["switch.matrix-74", "switch.matrix-75", "switch.matrix-76", "switch.matrix-77", "switch.matrix-78"],
			"A hidden lower-level mini-playfield reached by completing the G-R-A-Y lamp sequence (lamps "
			"62-65); the manual's own instruction card reads \"COMPLETE G-R-A-Y SEQUENCE TO ACTIVATE LOWER "
			"LEVEL GRAY GORILLA FEATURE\" and a second card reads \"USE FLIPPER BUTTONS TO SWING GORILLA LEFT "
			"AND RIGHT AND HIT PINBALL INTO C-O-N-G-O TARGETS. COMPLETE CONGO TO DEFEAT GRAY GORILLA AND AWARD "
			"BONUS.\" The manual's Gorilla Mechanism Test (T.16) confirms the physical layout: \"the operator "
			"[can] enable the underground mini-playfield and test its operation... the left and right flipper "
			"buttons will operate the gorilla mechanism and [display] the state of the gorilla stand-up "
			"switches\" (the five CONGO standup targets 74-78). Solenoids 15 (Gorilla Left) and 16 (Gorilla "
			"Right) each swing one of two small captive flipper-arm primitives (GoFlipperLeft, GoFlipperRight) "
			"inside the compartment while a separate timer gently rocks the gorilla figure itself "
			"(Gorilla.objRotZ) between three fixed angles; a dedicated persistent \"lower playfield\" ball prop "
			"(created by CreateLPFball/kickerLPF at power-on) represents the ball visually while it is in the "
			"hidden compartment. This machine has no magnet of any kind; the ball is captured and flung purely "
			"by the two small mechanical flipper arms.",
			[
				("target-c", "CONGO Target (C)", ["switch.matrix-74"], "First standup in the five-target C-O-N-G-O bank."),
				("target-o1", "CONGO Target (O, first)", ["switch.matrix-75"], "Second standup."),
				("target-n", "CONGO Target (N)", ["switch.matrix-76"], "Third standup."),
				("target-g", "CONGO Target (G)", ["switch.matrix-77"], "Fourth standup."),
				("target-o2", "CONGO Target (O, second)", ["switch.matrix-78"], "Fifth standup."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20614",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-61", "switch.matrix-62"],
			"Each slingshot assembly carries a combined kick/score switch (SW-1A-204 kick contact with "
			"SW-1A-205 score contact, diode-equipped). The retained script's LeftSlingShot_Slingshot and "
			"RightSlingShot_Slingshot handlers pulse matrix addresses 61 and 62 and fire coils 10/11 in the "
			"same event.",
			[
				("left", "Left slingshot", ["switch.matrix-61"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-L-2 left with B-9362-R-3 right",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-65"],
			"Three A-9415-2 jet bumpers with SW-11A-37-1 skirt switches. The retained script's Bumper1_Hit, "
			"Bumper2_Hit, and Bumper3_Hit handlers pulse switches 63, 64, and 65 and fire coils 12, 13, and 14 "
			"respectively, matching printed Left/Right/Bottom Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-63"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-64"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-65"], "Bumper closest to the player."),
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
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: "
			"the ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops "
			"to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. Printed "
			"circuits 29/30 (Lwr Rt Power/Hold) and 31/32 (Lwr Lt Power/Hold) map to public addresses 45-48.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15849-R-2 right with A-15849-L-2 left",
		),
		mechanism(
			"mechanism.upper-left-flipper",
			"Upper left flipper",
			"other",
			[output_id("Upper Left Flipper Power"), output_id("Upper Left Flipper Hold")],
			["switch.generic-117", "switch.generic-118"],
			"Congo's single upper flipper (FL-11630). The ROM energizes the power winding on the cabinet "
			"button opto (118), then drops to the hold winding once the end-of-stroke leaf switch (117) "
			"closes, exactly mirroring the lower-flipper pattern. There is no upper-right counterpart.",
			[("left", "Upper left flipper", ["switch.generic-117", "switch.generic-118"], "Button opto 118 and end-of-stroke switch 117.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20738",
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
			"id": "williams.congo.1995",
			"name": "Congo",
			"manufacturer": "Williams",
			"year": 1995,
			"kind": "physical_pinball",
			"ipdb_id": 3780,
			"model_number": "16-50050-101",
			"playfield": {
				"width": TABLE_WIDTH,
				"height": TABLE_HEIGHT,
				"units": "vpx",
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
			"opdb_id": "GrNd0-MJNW1",
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
		"knowledge": {"path": "knowledge/williams/congo-1995.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Congo device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
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
		spatial = device.get("spatial")
		if spatial is not None and spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"Switch 25 (Right Eject Rubber) has no reliable playfield coordinate. The retained "
			"extraction's only candidate object, a Primitive literally named \"sw25\", sits at local-"
			"space (684.0966, 1112.3384) -- the identical coordinate to an unrelated Primitive named "
			"\"sw1\" (not a valid Congo switch address) -- indicating both are copies of a reusable "
			"decorative mesh whose transform was never updated to the object's real placement. This is "
			"the sole reason coverage.status stays partial; every other dimension is validated.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": TABLE_WIDTH, "bottom": TABLE_HEIGHT},
			"x": f"x/{TABLE_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{TABLE_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/congo-1995/extracted-vpxtool.manifest.json",
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
		"unresolved_input_addresses": sorted(unresolved_inputs),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.congo.1995/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/congo/manual-transcription.md",
			},
		},
		"excluded_object_classes": [
			"GiTop member GI10_Deactivated -- its own name marks it disabled; not a distinct active physical bulb",
			"Flasher F8L3 (Volcano Flasher backbox bulb, normalized x=1.022303, outside the 0..1 playfield bounds) -- table modeling anomaly, backbox bulb parked off-table",
			"l32l, l33l, l38l, l81l co-located brightness-doubling Light objects",
			"lNNf-style Flasher companion objects (l11f, l12f, l14f, ... f9l2) -- insert glow-overlay effects layered on the lamp's own Light object, not separate physical bulbs",
		],
		"unresolved": [
			{"group": "pinmame.input.switch", "address": 25, "reason": "no reliable VPX object; see blockers"},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Congo (Williams, 1995) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete except for one "
		"switch, but the physical machine record itself remains `partial` at "
		"`machines/partial/williams/congo-1995.json` because that one address has no reliable coordinate; "
		"see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Congo (Williams 1995) 1.1.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to at "
		"most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual PDF has a usable but imperfect OCR text layer (Paper Capture scan); every "
		"printed table used here was still read from 300/600/1200 dpi renders and transcribed by hand into "
		"`evidence/excerpts/williams.congo.1995/`.",
		"- Several switches have no dedicated playfield trigger object because the retained script's "
		"cvpmTrough helpers (bsTrough, bsVolcano) model multi-position ball sensing purely as an internal "
		"switch array. Those addresses are explicit documented projections onto the real kicker object that "
		"carries the mechanism's exit/entry point.",
		"- GiTop member `GI10_Deactivated` is excluded as a table modeling anomaly (its own name marks it "
		"disabled); GI address 1's physical quantity is 13, not the collection's raw 14 members.",
		"- Flasher `F8L3` (part of solenoid 27, Volcano Flasher) sits at normalized x=1.022303, outside the "
		"retained table's 0..1 playfield bounds, and is excluded as the modeled stand-in for the printed "
		"table's backbox bulb; the other three Volcano Flasher bulbs (2 playfield #89, 1 playfield #906) are "
		"placed normally.",
		"- GI strings 0-2 use the retained table's GiGorilla/GiTop/GIBottom emitter collections, matching the "
		"retained script's `UpdateGi`/`UpdateGiOn` dispatch exactly. GI strings 3 and 4 are backbox insert-"
		"panel circuits and take a controlled `cabinet_or_service` record.",
		"- Solenoids 41-44 are PinMAME's unused WPC-95 LPDC mirrors; Congo populates no LPDC output at all "
		"(37-40 are also unused), unlike WPC-95 games with a DC-motor mechanism.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with "
		"both PinMAME core and manual provenance.",
		"- Switch 25 (Right Eject Rubber) is the sole unresolved spatial gap; its `spatial` key is omitted "
		"entirely rather than a coordinate or an undefined status being invented, matching the precedent set "
		"by other partial records in this project for a genuinely unlocatable address.",
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
		f"- Unresolved input addresses: {report['unresolved_input_addresses']}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical semantic, wiring, or mechanism question remains unresolved, and the "
		"deterministic curator reproduces the canonical artifact and its pinned seed byte-for-byte. Switch "
		"25 (Right Eject Rubber) is a genuinely used, printed switch with no reliable coordinate anywhere in "
		"the retained thin table -- its only candidate VPX object shares an identical, evidently-unmoved "
		"local-space coordinate with an unrelated object -- so it is left without a `spatial` key rather "
		"than being invented. The definition therefore carries `coverage.missing = [\"spatial_placement\"]` "
		"and stays `partial` until a richer retained table, a manual playfield diagram calibration, or "
		"another source resolves this one address.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Human-readable manual transcriptions under `evidence/excerpts/williams.congo.1995/` (six tables "
		"plus the DIP switch chart), each hashed and cited from the definition's manual source record.",
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
		raise RuntimeError(f"Stale Congo author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Congo definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Congo seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Congo definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Congo seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Congo spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Congo spatial review drifted from its deterministic curator: {markdown_path}")
	print("Congo definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Congo extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Congo retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
