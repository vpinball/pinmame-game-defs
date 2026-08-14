"""Curate the physical Bally Theatre of Magic (1995) machine definition.

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
# The retained known-working script binds tom_14hb (a 2005 "1.4 Home version Coin
# Play" driver variant), but pinned PinMAME's own driver.c dates tom_13 "08/95 B"
# as the final arcade production ROM (the parent/root of the clone tree). The
# machine's primary firmware binding is tom_13; tom_14hb remains a driver variant.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/theatre-of-magic-1995.json"
PARTIAL_PATH = ROOT / "machines/partial/bally/theatre-of-magic-1995.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/theatre-of-magic-1995.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/theatre-of-magic-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/theatre-of-magic-1995.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
MANUAL_SOURCE = "manual.bally.theatre-of-magic.1995"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.theatre-of-magic.1995"
VPX_TABLE_SOURCE = "vpx-table.tom-2-4"
VPX_SCRIPT_SOURCE = "vpx-script.tom-2-4"
VPX_EXTRACTION_SOURCE = "vpx-extraction.tom-2-4"

TABLE_SHA256 = "5f8bb3e0493c408484e475516e2f2c3d84b3487dcfb63eb231bca2c40b531253"
SCRIPT_SHA256 = "596c926f27c1782819a0184566f083a161be362fec7a3bbc634a9138d97b47c3"
MANUAL_SHA256 = "ef9348415031e5d851b3c46454a0df0178f7a2066223d54a42db0d6708e56d92"
MANUAL_TRANSCRIPTION_SHA256 = "c7a4dd783f33e63413bc33b9dcdf99c7381f80e82eb84017cf0b2a1354d6b9fb"
VPX_GEOMETRY_SHA256 = "df048e59d6638d8d5fc91e9c2d857de6f3437fc70cf858c265439289d809fa2a"

EXTRACTION_RELATIVE_PATH = Path("bally/theatre-of-magic-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/theatre-of-magic-1995/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "2db2ef0933b9738ff48e79e3ca6f2332e97e5457321f711d4b8430d4f0c6cc45"
EXTRACTION_FILE_COUNT = 1994
EXTRACTION_TOTAL_BYTES = 151153328

# Hazard #2: this table's playfield is unusually tall. Normalizing with the more
# common 2162 bottom bound (used by every other curated WPC game so far) would
# compress every y coordinate by about 20%; the correct divisor is 2594.1.
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2594.1"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2594.1

# Hazard #1: the pinned catalog's tom clone tree. tom_13 (parent, no clone_of) is
# the final arcade production ROM per pinned driver.c's own dated comment
# ("08/95 B Theatre of Magic (1.3X)"); tom_14h/tom_14hb are dated "10/96" and
# commented "Theatre of Magic (1.4 Home version)" / "(1.4 Home version Coin
# Play)" -- i.e. a later non-arcade "Home version" ROM, not the shipped
# production firmware. Every tom_* clone is registered through the identical
# CORE_CLONEDEF(tom, <ver>, 13, ...) macro sharing one init_tom/tomGameData
# struct (src/wpc/sims/wpc/full/tom.c), so PinMAME's own driver registration
# proves there is no controller-address or polarity difference between any two
# tom_* drivers -- the difference is ROM-internal game rules only.
DRIVER_IDS = (
	"tom_13", "tom_06", "tom_061", "tom_10f", "tom_101f", "tom_12", "tom_12a",
	"tom_121", "tom_13c", "tom_13f", "tom_14h", "tom_14hb",
)
DRIVER_COMPATIBILITY = {
	"tom_13": (
		"identical",
		"Bally production 1.3X game ROM shipped with the physical machine (pinned driver.c dates it "
		"\"08/95 B\", the newest of the six 1995-dated revisions and the parent of the clone tree). "
		"This is the primary firmware binding for this definition.",
	),
	"tom_06": (
		"identical",
		"Bally 0.6A prototype game ROM (driver.c \"03/95 B\"), the earliest cataloged revision. Same "
		"physical machine, switch matrix, lamp matrix, and solenoid/flasher table as production.",
	),
	"tom_061": (
		"identical",
		"Bally 0.61A prototype game ROM with an LED ghost-image fix; no controller-address change.",
	),
	"tom_10f": (
		"identical",
		"Bally 1.0 French-localized game ROM (driver.c \"04/95 B\"); no controller-address change.",
	),
	"tom_101f": (
		"identical",
		"Bally 1.01 French-localized game ROM with an LED ghost-image fix; no controller-address change.",
	),
	"tom_12": (
		"identical",
		"Bally 1.2X game ROM (driver.c \"04/95 B\"); no controller-address change.",
	),
	"tom_12a": (
		"identical",
		"Bally 1.2A game ROM; no controller-address change.",
	),
	"tom_121": (
		"identical",
		"Bally 1.21X game ROM with an LED ghost-image fix; no controller-address change.",
	),
	"tom_13c": (
		"identical",
		"2019 \"1.3XC Competition MOD\" community ruleset patch built from the 1.3X production ROM "
		"(pinned tom.c comment: \"based on 1.3X, NOT the Tiger saw rev. 1.4H, but it includes Tiger "
		"saw support\"). Same physical hardware and addresses as tom_13.",
	),
	"tom_13f": (
		"identical",
		"2005 French-localized rebuild of the 1.3 production ROM; no controller-address change.",
	),
	"tom_14h": (
		"identical",
		"2005 \"1.4 Home version\" game ROM (driver.c \"10/96 B\", i.e. a post-arcade-run software "
		"revision; NOT the shipped arcade firmware). Registered through the identical "
		"CORE_CLONEDEF/init_tom path as tom_13, so the controller-address map is unchanged; only "
		"ROM-internal rules differ.",
	),
	"tom_14hb": (
		"identical",
		"2005 \"1.4 Home version Coin Play\" game ROM, a coin-mechanism variant of tom_14h. This is "
		"the driver the retained script binds (cGameName = \"tom_14hb\", commented \"1.3x arcade rom "
		"- with credits\" by the table author), but it is not the machine's production firmware -- see "
		"the hazard note above. It shares the identical controller-address map with every other tom_* "
		"driver; no conflicts entry is required for switch, coil, or lamp semantics because PinMAME's "
		"own driver registration (one tomGameData struct, one init_tom, for every clone) structurally "
		"rules out an address-level difference between the bound driver and the production ROM.",
	),
}

# --- Printed switch matrix (manual pages 2-42 wiring, 2-43 parts list; page 2 for
# identity cross-check). address = column*10 + row.
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In", 24: "Always Closed",
	25: "Left Outlane", 26: "Left Return Lane", 27: "Right Return Lane", 28: "Right Outlane",
	31: "Trough Jam", 32: "Trough 1", 33: "Trough 2", 34: "Trough 3", 35: "Trough 4",
	36: "Subway Opto", 37: "Spinner", 38: "Right Lower Target",
	41: "Lock 1", 42: "Lock 2", 43: "Lock 3", 44: "Popper",
	45: "Left Drain Eddy", 47: "Subway Micro", 48: "Right Drain Eddy",
	51: "Left Bank Target", 52: "Captive Ball Rest", 53: "Right Lane Enter", 54: "Left Lane Enter",
	55: "Cube Position 4", 56: "Cube Position 1", 57: "Cube Position 2", 58: "Cube Position 3",
	61: "Left Sling", 62: "Right Sling", 63: "Bottom Jet", 64: "Middle Jet", 65: "Top Jet",
	66: "Top Lane 1", 67: "Top Lane 2",
	71: "Center Ramp Exit", 73: "Right Ramp Exit", 74: "Right Ramp Exit 2",
	75: "Center Ramp Enter", 76: "Right Ramp Enter", 77: "Captive Ball Top", 78: "Loop Left",
	81: "Loop Right", 82: "Center Ramp Targets", 83: "Vanish Lock 1", 84: "Vanish Lock 2",
	85: "Trunk Hit", 86: "Right Lane Exit", 87: "Left Lane Exit",
}
UNUSED_MATRIX_ADDRESSES = {11, 12, 16, 17, 18, 46, 68, 72, 88}
# Shaded "OPTO, TYPICALLY CLOSED" on the printed switch matrix (2-42): trough
# optos (31-36) and Cube Position optos (55-58). Column 3 rows 7-8 (37 Spinner,
# 38 Right Lower Target) and column 4 (41-48, Lock/Popper/Eddy) are NOT shaded.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 55, 56, 57, 58}
# PinMAME's tomGameData inverted-switch mask: column 3 (index 3) = 0x3f (bits 0-5
# = rows 1-6 = 31-36), column 5 (index 5) = 0xF0 (bits 4-7 = rows 5-8 = 55-58).
# Every printed opto is normalized -- zero disagreement, unlike Monster Bash.
PINMAME_NORMALIZED_OPTO_SWITCHES = set(OPTO_SWITCHES)
# Eddy-current proximity sensors (manual page 1-45 "Eddy Sensor Calibration"):
# construction described but not classifiable as opto or leaf; switch_type "other".
EDDY_SWITCHES = {45, 48, 85}
# vpmTimer.PulseSw / momentary callers in the retained script.
PULSED_SWITCHES = {25, 41}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 21: "leaf", 22: "microswitch",
	23: "button", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	28: "microswitch", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto",
	36: "opto", 37: "other", 38: "microswitch", 41: "microswitch", 42: "microswitch",
	43: "microswitch", 44: "microswitch", 45: "other", 47: "microswitch", 48: "other",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch",
	55: "opto", 56: "opto", 57: "opto", 58: "opto",
	61: "microswitch", 62: "microswitch", 63: "leaf", 64: "leaf", 65: "leaf",
	66: "microswitch", 67: "microswitch", 71: "microswitch", 73: "microswitch",
	74: "microswitch", 75: "microswitch", 76: "microswitch", 77: "microswitch",
	78: "microswitch", 81: "microswitch", 82: "microswitch", 83: "microswitch",
	84: "microswitch", 85: "other", 86: "microswitch", 87: "microswitch",
}

# address -> (assembly/opto part number(s), plain switch part number)
SWITCH_PARTS = {
	13: (None, "20-9663-1"), 14: (None, "A-15361"), 15: (None, "5647-12693-32"),
	21: (None, "A-17238"), 22: (None, "5643-09288-00"), 23: (None, "20-9663-18"),
	24: (None, "5643-09112-00"),
	25: (None, "5647-12693-19"), 26: (None, "5647-12693-19"), 27: (None, "5647-12693-19"),
	28: (None, "5647-12693-19"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16908 LED with A-16909 photo transistor", None),
	37: (None, "5647-12693-24"), 38: (None, "A-17799-6"),
	41: (None, "5647-12693-34"), 42: (None, "5647-12693-33"), 43: (None, "5647-12693-32"),
	44: (None, "5647-12693-11"),
	45: (None, "A-18543-1"), 47: (None, "5647-12693-13"), 48: (None, "A-18543-1"),
	51: (None, "A-18059-15"), 52: (None, "5647-12693-19"), 53: (None, "5647-12693-19"),
	54: (None, "5647-12693-19"),
	55: (None, "A-19749"), 56: (None, "A-19749"), 57: (None, "A-19749"), 58: (None, "A-19749"),
	61: (None, "SW-1A-114 kicker with SW-1A-120 score"), 62: (None, "SW-1A-114 kicker with SW-1A-120 score"),
	63: (None, "SW-11A-37"), 64: (None, "SW-11A-37"), 65: (None, "SW-11A-37"),
	66: (None, "5647-12693-19"), 67: (None, "5647-12693-19"),
	71: (None, "5647-12693-13"), 73: (None, "5647-12693-13"), 74: (None, "5647-12693-13"),
	75: (None, "5647-12693-11"), 76: (None, "5647-12693-11"), 77: (None, "5647-12693-19"),
	78: (None, "5647-12693-19"), 81: (None, "5647-12693-19"), 82: (None, "A-20014-5"),
	83: (None, "5647-12133-11"), 84: (None, "5647-12133-12"), 85: (None, "A-18543-2"),
	86: (None, "5647-12693-13"), 87: (None, "5647-12693-13"),
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
# Fliptronic F1-F8 wiring, printed 2-42.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Black-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Black-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J905-5"),
}

# --- Printed solenoid/flasher table (manual page 2 clean render; duplicated 2-46/2-47
# in Section 2 Locations and 3-5 in Section 3 Wiring).
SOLENOID_LABELS = {
	1: "Ball Trough", 2: "Magnet Diverter", 3: "Trap Door Up", 4: "Subway Popper",
	5: "Right Drain Magnet", 6: "Center Loop Post", 7: "Knocker", 8: "Top Diverter Post",
	9: "Left Sling", 10: "Right Sling", 11: "Bottom Jet", 12: "Middle Jet", 13: "Top Jet",
	14: "Trap Door Hold", 15: "Left Up/Down Gate", 16: "Right Up/Down Gate",
	17: "Box Clockwise", 18: "Box Counter Clockwise",
	20: "Return Lane Flasher", 21: "Top Kickout", 24: "Trap Door Flasher",
	25: "Spirit Ring Flasher", 26: "Saw Flasher", 27: "Jet Flasher", 28: "Box Flasher",
	33: "Cube Magnet", 34: "Sub Ball Release", 35: "Left Drain Magnet",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {
	19: "Not Used Solenoid Position 19",
	22: "Not Used Solenoid Position 22",
	23: "Not Used Solenoid Position 23",
	36: "Not Used Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC Output 37", 38: "Unused WPC Output 38", 39: "Unused WPC Output 39",
	40: "Unused WPC Output 40", 41: "Unused WPC Output 41", 42: "Unused WPC Output 42",
	43: "Unused WPC Output 43", 44: "Unused WPC Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# Manual solenoid/flasher table addresses that differ from the PinMAME public address.
MANUAL_SOLENOID_ALIASES = {33: "Upr. Rt. Power", 34: "Upr. Rt. Hold", 35: "Upr. Lt. Power", 45: "29", 46: "30", 47: "31", 48: "32"}

# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(driver_transistor="Q82", control_connection="J107-2", power_connection="J130-1", part_number="AE-26-1500", printed_type="High Power"),
	2: dict(driver_transistor="Q80", control_connection="J107-2", power_connection="J130-2", part_number="20-10179", printed_type="High Power"),
	3: dict(driver_transistor="Q78", control_connection="J107-2", power_connection="J130-4", part_number="A-20099", printed_type="High Power"),
	4: dict(driver_transistor="Q76", control_connection="J107-2", power_connection="J130-5", part_number="AE-26-1200", printed_type="High Power"),
	5: dict(driver_transistor="Q64", control_connection="J107-2", power_connection="J130-6", part_number="20-10197", printed_type="High Power"),
	6: dict(driver_transistor="Q66", control_connection="J107-2", power_connection="J130-7", part_number="AE-27-1200", printed_type="High Power"),
	7: dict(driver_transistor="Q68", power_connection="J130-8", part_number="AE-23-800", printed_type="High Power"),
	8: dict(driver_transistor="Q70", control_connection="J107-2", power_connection="J130-9", part_number="AE-27-1200", printed_type="High Power"),
	9: dict(driver_transistor="Q58", control_connection="J107-3", power_connection="J127-1", part_number="AE-27-1200", printed_type="Low Power"),
	10: dict(driver_transistor="Q56", control_connection="J107-3", power_connection="J127-3", part_number="AE-27-1200", printed_type="Low Power"),
	11: dict(driver_transistor="Q54", control_connection="J107-3", power_connection="J127-4", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(driver_transistor="Q52", control_connection="J107-3", power_connection="J127-5", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(driver_transistor="Q50", control_connection="J107-3", power_connection="J127-6", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(driver_transistor="Q48", control_connection="J107-2", power_connection="J127-7", part_number="A-20099", printed_type="Low Power"),
	15: dict(driver_transistor="Q46", control_connection="J107-3", power_connection="J127-8", part_number="A-14406", printed_type="Low Power"),
	16: dict(driver_transistor="Q44", control_connection="J107-3", power_connection="J127-9", part_number="A-14406", printed_type="Low Power"),
	17: dict(driver_transistor="Q42", control_connection="J116-2", power_connection="J126-1", part_number="14-8018", printed_type="Flasher-bank driver"),
	18: dict(driver_transistor="Q40", control_connection="J116-2", power_connection="J126-2", part_number="14-8018", printed_type="Flasher-bank driver"),
	19: dict(driver_transistor="Q38", control_connection="J116-2", power_connection="J126-3", printed_type="Flasher-bank driver"),
	20: dict(driver_transistor="Q36", control_connection="J107-6", power_connection="J126-4", printed_type="Flasher"),
	21: dict(driver_transistor="Q28", control_connection="J107-1", power_connection="*J126-5", part_number="AE-27-1200", printed_type="Flasher-bank driver"),
	22: dict(driver_transistor="Q30", control_connection="J107-6", power_connection="J126-6", printed_type="Flasher-bank driver"),
	23: dict(driver_transistor="Q34", control_connection="J107-6", power_connection="J126-7", printed_type="Flasher-bank driver"),
	24: dict(driver_transistor="Q32", control_connection="J107-6", power_connection="J126-8", printed_type="Flasher-bank driver"),
	25: dict(driver_transistor="Q26", control_connection="J107-6/J106-5", power_connection="J122-1/J124-1", printed_type="Gen. Purpose"),
	26: dict(driver_transistor="Q24", control_connection="J107-6/J106-5", power_connection="J122-2/J124-2", printed_type="Gen. Purpose"),
	27: dict(driver_transistor="Q22", control_connection="J107-6/J106-5", power_connection="J122-3/J124-3", printed_type="Gen. Purpose"),
	28: dict(driver_transistor="Q20", control_connection="J107-6/J106-5", power_connection="J122-4/J124-5", printed_type="Gen. Purpose"),
	33: dict(driver_transistor="Q2", control_connection="J907-6,7", power_connection="J902-6", part_number="20-10197", printed_type="High Power (repurposed Upr. Rt. Power)"),
	34: dict(driver_transistor="Q7", control_connection="J907-6,7", power_connection="J902-4", part_number="AE-27-1200", printed_type="Low Power (repurposed Upr. Rt. Hold)"),
	35: dict(driver_transistor="Q1", control_connection="J907-8,9", power_connection="J902-3", part_number="20-10197", printed_type="High Power (repurposed Upr. Lt. Power)"),
	36: dict(driver_transistor="Q5", control_connection="J907-8,9", power_connection="J902-1", printed_type="Fliptronic hold (Upr. Lt. Hold)"),
	45: dict(driver_transistor="Q4", control_connection="J907-1", power_connection="J902-13", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(driver_transistor="Q11", control_connection="J907-1", power_connection="J902-11", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(driver_transistor="Q3", control_connection="J907-4", power_connection="J902-9", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(driver_transistor="Q9", control_connection="J907-4", power_connection="J902-7", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "Yel-Grn", 46: "Org-Grn", 47: "Yel-Blu", 48: "Org-Blu", 33: "Yel-Vio", 35: "Yel-Gry"}

SOLENOID_ASSEMBLIES = {
	1: "A-19963", 2: "A-19778", 3: "A-19939", 4: "A-19939", 6: "A-17932", 7: "B-10686-1",
	8: "A-17932", 9: "B-9362-L-3", 10: "B-9362-R-4", 11: "A-9415-2", 12: "A-9415-2",
	13: "A-9415-2", 14: "A-19939", 15: "A-17796", 16: "A-17796", 17: "A-19782", 18: "A-19782",
	20: "A-17983", 21: "A-20003", 24: "A-17983 with A-17803", 25: "A-17983", 26: "A-17903",
	27: "A-17803", 28: "A-17983 with A-17803",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
# Retained VPW-style script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "SolRelease (kicks sw32)", 2: "SolSpiritRing", 3: "SolTrapDoorUp", 4: "SolSubwayPopper",
	5: "SolRightMagnet", 6: "SolLoopPost", 7: "SolKnocker", 8: "SolDivPost",
	14: "SolTrapDoorHold", 15: "SolGate3", 16: "SolGate1",
	17: "solTrunkMotorCW", 18: "solTrunkMotorCCW", 21: "SolTopKickout (kicks sw83)",
	20: "SetLamp 120, (FlasherMod=0) / SetModLamp 120, (FlasherMod=1)",
	24: "SetLamp 124, / SetModLamp 124,", 25: "SetLamp 125, / SetModLamp 125,",
	26: "SetLamp 126, / SetModLamp 126,", 27: "SetLamp 127, / SetModLamp 127,",
	28: "SetLamp 128, / SetModLamp 128,",
	33: "SolTrunkMagnet", 34: "SolSubBallRelease (kicks sw41)", 35: "SolLeftMagnet",
	46: "SolRFlipper (public sLRFlip = 46)", 48: "SolLFlipper (public sLLFlip = 48)",
}

FLASHER_BULBS = {
	20: ("#89 (2), playfield", 2),
	24: ("#89 (2) playfield (assemblies A-17983 and A-17803) plus #906 backbox", 2),
	25: ("#906 + #89 playfield (assembly A-17983) plus #906 backbox", 1),
	26: ("#906 + #89 (2) playfield (assembly A-17903) plus #906 backbox", 1),
	27: ("#906 + #89 (2) playfield (assembly A-17803) plus #906 backbox", 1),
	28: ("#906 (2) + #89 playfield (assemblies A-17983 and A-17803) plus #906 backbox", 1),
}

# --- Printed lamp matrix (manual page 2-40 locations, 2-41 parts list).
LAMP_LABELS = {
	11: "(T)heatre", 12: "T(H)eatre", 13: "Th(e)atre", 14: "The(a)tre", 15: "Thea(t)re",
	16: "Theat(r)e", 17: "Theatr(e)", 18: "(M)agic",
	21: "Haunted Basement", 22: "Metamorphosis Award", 23: "Right Spell Magic",
	24: "Spirit Ring", 25: "Advance Clock", 26: "Jacket Award", 27: "M(a)gic",
	28: "Trunk Hit 3",
	31: "MA(G)IC", 32: "MAGI(C)", 33: "Lift Trapdoor", 34: "Center Spell Magic",
	35: "Levitate Award", 36: "MAG(I)C", 37: "Top Rollover 1", 38: "Top Rollover 2",
	41: "Extra Ball", 42: "Vanish", 43: "Spell Theatre", 44: "Jackpot",
	45: "Safe Award", 46: "Tiger Saw Award", 47: "Start Finale", 48: "Trunk Hit 1",
	51: "Trunk Hit 2", 52: "Hurry Up", 53: "Trunk Escape", 54: "Lock Ball",
	55: "Hat Trick Award", 56: "Start Illusion", 57: "Start Multi-Ball", 58: "Lite Vanish",
	61: "Tiger Saw", 62: "Levitate Woman", 63: "Grand Finale", 64: "Trunk Escape",
	65: "Spirit Cards", 66: "Safe Escape", 67: "Meta-Morphisis", 68: "Strait Jacket",
	71: "Hat Magic", 72: "Spirit Award", 73: "Theatre", 74: "Multi-Ball", 75: "Midnight",
	76: "Illusions", 77: "Saw Multi-Ball", 78: "Hocus Pocus",
	81: "Special", 82: "Not Used", 83: "Not Used", 84: "Not Used", 85: "Lamp In Cube",
	86: "Shoot Again", 87: "Buy-In", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-19982", "#555"), 12: ("A-19982", "#555"), 13: ("A-19982", "#555"),
	14: ("A-19982", "#555"), 15: ("A-19982", "#555"), 16: ("A-19982", "#555"),
	17: ("A-19982", "#555"), 18: ("A-19982", "#555"),
	21: ("A-19982", "#555"), 22: ("A-19982", "#555"), 23: ("A-19982", "#555"),
	24: ("A-19982", "#555"), 25: ("A-19982", "#555"),
	26: ("A-19983 and A-19982", "#555"), 27: ("A-19982", "#555"), 28: ("A-17836", "#44"),
	31: ("A-19982", "#555"), 32: ("A-19982", "#555"), 33: ("A-19984", "#555"),
	34: ("A-19984", "#555"), 35: ("A-19984", "#555"), 36: ("A-19982", "#555"),
	37: ("A-17835", "#44"), 38: ("A-17835", "#44"),
	41: ("A-19983", "#555"), 42: ("A-19983", "#555"), 43: ("A-19983", "#555"),
	44: ("A-19983", "#555"), 45: ("A-19983 and A-19984", "#555"), 46: ("A-19983", "#555"),
	47: ("A-19983", "#555"), 48: ("A-19983", "#555"),
	51: ("A-19983", "#555"), 52: ("A-19983", "#555"), 53: ("A-19983", "#555"),
	54: ("A-19983 and A-19984", "#555"), 55: ("A-19983", "#555"), 56: ("A-19983", "#555"),
	57: ("A-19983", "#555"), 58: ("A-19983", "#555"),
	61: ("A-19981", "#555"), 62: ("A-19981", "#555"), 63: ("A-19981", "#555"),
	64: ("A-19981", "#555"), 65: ("A-19981", "#555"), 66: ("A-19981", "#555"),
	67: ("A-19981", "#555"), 68: ("A-19981", "#555"),
	71: ("A-19981", "#555"), 72: ("A-19984", "#555"), 73: ("A-19981", "#555"),
	74: ("A-19981", "#555"), 75: ("A-19981", "#555"), 76: ("A-19981", "#555"),
	77: ("A-17807", "#44"), 78: ("A-17835", "#44"),
	81: ("A-17835", "#44"), 82: (None, None), 83: (None, None), 84: (None, None),
	85: ("A-17826", "#555"), 86: ("A-17807", "#44"),
	87: ("20-9663-18", None), 88: ("20-9663-1", None),
}
LAMP_QUANTITIES = {26: 2, 45: 2, 54: 2, 63: 2, 81: 2}

GI_STRINGS = {
	0: ("String 1", "Backbox J120-1", "Q18", "Backbox J120-7", "#555 (backbox)"),
	1: ("String 2", "Backbox J120-2", "Q10", "Backbox J120-8", "#555 (backbox)"),
	2: ("String 3", "Playfield J121-3", "Q14", "Playfield J121-9", "#44 (playfield)"),
	3: ("String 4", "Playfield J121-5", "Q16", "Playfield J121-10", "#44 (playfield)"),
	4: ("String 5", "Playfield J121-6", "Q12", "Playfield J121-11", "#44 (playfield)"),
}

# --- Normalized playfield coordinates derived from the retained VPX extraction
# (x/952, y/2594.1; review-artifacts/theatre-of-magic-1995/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.944816, 0.912629)], 25: [(0.053653, 0.80606)], 26: [(0.130727, 0.784713)],
	27: [(0.776867, 0.784762)], 28: [(0.854992, 0.807313)],
	31: [(0.876872, 0.889652)], 32: [(0.800507, 0.906649)], 33: [(0.726369, 0.921146)],
	34: [(0.653525, 0.935375)], 35: [(0.581464, 0.949315)], 36: [(0.301778, 0.363896)],
	37: [(0.649549, 0.42143)], 38: [(0.828791, 0.64886)],
	41: [(0.469898, 0.517236)], 42: [(0.446254, 0.495308)], 43: [(0.42984, 0.470845)],
	44: [(0.711155, 0.564702)], 45: [(0.077156, 0.732624)], 47: [(0.39908, 0.42081)],
	48: [(0.838448, 0.734407)],
	51: [(0.097031, 0.643884), (0.105917, 0.618638)], 52: [(0.152655, 0.467546)],
	53: [(0.919855, 0.268301)], 54: [(0.062975, 0.395898)],
	55: [(0.335084, 0.357928)], 56: [(0.335084, 0.357928)], 57: [(0.335084, 0.357928)],
	58: [(0.335084, 0.357928)],
	61: [(0.222815, 0.776297)], 62: [(0.683079, 0.776154)], 63: [(0.75706, 0.390839)],
	64: [(0.880103, 0.322842)], 65: [(0.659227, 0.305299)], 66: [(0.617681, 0.239293)],
	67: [(0.711472, 0.24824)],
	71: [(0.115152, 0.32398)], 73: [(0.101459, 0.243577)], 74: [(0.102552, 0.391505)],
	75: [(0.516089, 0.33209)], 76: [(0.756068, 0.386433)], 77: [(0.126263, 0.279842)],
	78: [(0.18036, 0.341255)],
	81: [(0.525423, 0.305115)], 82: [(0.448022, 0.426313), (0.585437, 0.44043)],
	83: [(0.36689, 0.238442)], 84: [(0.406398, 0.225076)], 85: [(0.368803, 0.387906)],
	86: [(0.232224, 0.20219)], 87: [(0.859186, 0.356635)],
}
SWITCH_PROJECTIONS = {
	55: "Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center): the four Cube Position optos are printed on the trunk's own \"Opto Board\" (manual page 1-50 teardown diagram) and the retained script's TrunkTimer_Timer sets all four from one TrunkAngle counter (0-360 degrees) rather than from four fixed playfield objects.",
	56: "Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.",
	57: "Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.",
	58: "Projected onto the rotating trunk (Primitive Trunk/Trunk1/Trunk2, table object center); see switch 55.",
}

SOLENOID_POSITIONS = {
	1: [(0.800507, 0.906649)], 2: [(0.120404, 0.444085)], 3: [(0.722836, 0.549031)],
	4: [(0.711155, 0.564702)], 5: [(0.773731, 0.714452)], 6: [(0.317357, 0.271829)],
	8: [(0.439531, 0.186026)], 9: [(0.222815, 0.776297)], 10: [(0.683079, 0.776154)],
	11: [(0.75706, 0.390839)], 12: [(0.880103, 0.322842)], 13: [(0.659227, 0.305299)],
	14: [(0.722836, 0.549031)], 15: [(0.501038, 0.199139)], 16: [(0.778747, 0.195558)],
	17: [(0.335084, 0.357928)], 18: [(0.335084, 0.357928)],
	20: [(0.101258, 0.81371), (0.806239, 0.814077)],
	21: [(0.36689, 0.238442)],
	24: [(0.709645, 0.470098), (0.914519, 0.62309)],
	25: [(0.270985, 0.446123)], 26: [(0.353641, 0.26259)], 27: [(0.234742, 0.003406)],
	28: [(0.786287, 0.366017)],
	33: [(0.335084, 0.357928)], 34: [(0.469898, 0.517236)], 35: [(0.129892, 0.716256)],
	# Public 45/46 = sLRFlipPow/sLRFlip (Lower RIGHT flipper, CORE_FIRSTLFLIPSOL+0/1) -> the
	# retained table's RightFlipper object (larger x); 47/48 = sLLFlipPow/sLLFlip (Lower LEFT,
	# +2/+3) -> LeftFlipper (smaller x). Matches the manual's own "Lwr. Rt."/"Lwr. Lt." naming.
	45: [(0.621639, 0.868509)], 46: [(0.621639, 0.868509)],
	47: [(0.285504, 0.868509)], 48: [(0.285504, 0.868509)],
}

LAMP_POSITIONS = {
	11: [(0.247672, 0.684448)], 12: [(0.316391, 0.678823)], 13: [(0.385267, 0.67542)],
	14: [(0.452882, 0.674524)], 15: [(0.520734, 0.675707)], 16: [(0.587665, 0.679117)],
	17: [(0.656645, 0.685499)], 18: [(0.347261, 0.642663)],
	21: [(0.670803, 0.604867)], 22: [(0.648946, 0.624255)], 23: [(0.633556, 0.640805)],
	24: [(0.616606, 0.657759)], 25: [(0.747828, 0.630441)],
	26: [(0.702372, 0.667561), (0.1751, 0.602612)], 27: [(0.376654, 0.616103)],
	28: [(0.407498, 0.44301)],
	31: [(0.452255, 0.608522)], 32: [(0.557233, 0.642722)], 33: [(0.506622, 0.46313)],
	34: [(0.507563, 0.48609)], 35: [(0.504315, 0.507706)], 36: [(0.527815, 0.616319)],
	37: [(0.618028, 0.206275)], 38: [(0.711082, 0.215489)],
	41: [(0.083002, 0.491816)], 42: [(0.121503, 0.532684)], 43: [(0.149441, 0.56462)],
	44: [(0.378751, 0.578314)], 45: [(0.640226, 0.459789), (0.2093, 0.431889)],
	46: [(0.18675, 0.526785)], 47: [(0.232214, 0.470682)], 48: [(0.307368, 0.445742)],
	51: [(0.354582, 0.434554)], 52: [(0.373209, 0.551827)], 53: [(0.370375, 0.528616)],
	54: [(0.250757, 0.508959), (0.625654, 0.504575)], 55: [(0.366471, 0.504606)],
	56: [(0.357917, 0.459295)], 57: [(0.362982, 0.483012)], 58: [(0.213135, 0.570178)],
	61: [(0.403144, 0.726234)], 62: [(0.403144, 0.754038)],
	63: [(0.410419, 0.702216), (0.482902, 0.702408)], 64: [(0.403144, 0.782103)],
	65: [(0.403961, 0.809581)], 66: [(0.504957, 0.726234)], 67: [(0.504479, 0.754189)],
	68: [(0.504, 0.78243)],
	71: [(0.501927, 0.809581)], 72: [(0.645396, 0.420923)], 73: [(0.376041, 0.849324)],
	74: [(0.42136, 0.857613)], 75: [(0.480302, 0.857895)], 76: [(0.527993, 0.84993)],
	77: [(0.82705, 0.572433)], 78: [(0.159116, 0.652125)],
	81: [(0.071705, 0.848768), (0.833377, 0.849053)],
	85: [(0.335084, 0.357928)], 86: [(0.451615, 0.897952)],
}

GI_POSITIONS = {
	2: [
		(0.995273, 0.492656), (0.999988, 0.285263), (0.691563, 0.851512),
		(0.728555, 0.766966), (0.694819, 0.802543), (0.757473, 0.834586),
		(0.691404, 0.85138), (0.728294, 0.767383), (0.694513, 0.803522),
		(0.757219, 0.834624), (0.942868, 0.581523), (0.968225, 0.491789),
		(0.933561, 0.539497), (0.86896, 0.646178), (0.834512, 0.686722),
	],
	3: [
		(0.845059, 0.487403), (0.877997, 0.447893), (0.845163, 0.486508),
		(0.881697, 0.44798), (0.713543, 0.486778), (0.699778, 0.488234),
		(0.757649, 0.455052), (0.740872, 0.455244), (0.715855, 0.420775),
		(0.742423, 0.422329),
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
		raise RuntimeError(f"Theatre of Magic retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Theatre of Magic extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Theatre of Magic retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Theatre of Magic retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Theatre of Magic retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the tom_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/tom.c tomGameData GEN_WPCSECURITY with wpc_dispDMD, the inverted-switch "
				"mask {0x00,0x00,0x00,0x3f,0x00,0xF0,0x00,0x00,0x00,0x00,0x00,0x00}, FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L) "
				"(no upper-flipper bit), swStart/swTilt/swSlamTilt/swCoinDoor defines, sBallTrough..sLeftDrainMagnet "
				"solenoid defines (33-35 in the driver-specific 33-36 range, no FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) "
				"so no flipper remap applies), tom_handleMech/tom_getMech (TrunkPos 0-359 in TOM_TRUNKTICKS=2 degree "
				"steps, TOM_SWCLOSEDDEGREE=20 degree windows at 0/90/180/270, magnetTicks countdown from "
				"TOM_MAGNETTICKSINIT=30), CORE_GAMEDEF(tom,13,...)/CORE_CLONEDEF(tom,<ver>,13,...) for every clone "
				"sharing one init_tom/tomGameData struct; src/wpc/gen.h GEN_WPCSECURITY=U64(0x20); src/wpc/wpc.c "
				"GENWPC_HASFLIPTRON/GENWPC_HASWPC95/GENWPC_HASPIC masks and the WPC_FLIPPERS/WPC_SWROWREAD dispatch; "
				"src/wpc/core.h WPC solenoid/switch numbering; src/wpc/core.c core_getSol/core_getSw dispatch; "
				"src/wpc/driver.c dated driver comments (tom_13 \"08/95 B\", tom_14h/tom_14hb \"10/96 B ... Home "
				"version\"); src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCSECURITY=0x20"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-security.json",
			"revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp, and five-GI address rules (identical addressing to WPC-DCS/WPC-Fliptronic; the security PIC only changes the internal matrix-scan handshake, not the public address space)",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.theatre-of-magic.1995/archive-arcademanual_Theatre_of_Magic_OPS/Theatre_of_Magic_OPS.pdf",
			"original_filename": "Theatre_of_Magic_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"158-page Bally Theatre of Magic operations manual (part number 16-50039-101, FINAL, March 1995, "
				"Midway Manufacturing Company). Printed page 2 carries a clean duplicate of the DIP switch chart and "
				"the full Solenoid/Flasher Table; printed pages 2-40 through 2-45 carry the lamp/switch/solenoid "
				"location parts lists and matrix/wiring tables a second time; printed page 1-45 carries Eddy Sensor "
				"Calibration; printed page 1-50 carries the Magic Trunk teardown diagram; Section 3 (3-1 onward) "
				"carries Game Wiring and Schematics a third time with component-level circuit detail. The PDF carries "
				"an OCR text layer (Adobe Acrobat Paper Capture) that was verified against 300 dpi page renders "
				"rather than trusted directly."
			),
			"license": "NOASSERTION",
			"attribution": "Bally Pinball / Midway Manufacturing Company",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.theatre-of-magic.dip-switch-country-chart",
					"locator": "PDF page 2, DIP switch country chart",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/dip-switch-country-chart.md",
					"sha256": "376b7b3af50393253445796c65278a89c2fa5ddae73e6a027ae1a3521a8f93dc",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.solenoid-flasher-wiring",
					"locator": "PDF page 2, Solenoid/Flasher Table and Flipper Circuits",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/solenoid-flasher-wiring.md",
					"sha256": "1e754fc43b950969b6ef5e2163344e725829ef7f0207256019bcadda303be1ca",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.general-illumination",
					"locator": "PDF page 2, General Illumination",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/general-illumination.md",
					"sha256": "8d16c9820c2a23483b462148ddb3d3fd4a36794ea8dd5e526004b43e500b9fe9",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.lamp-matrix",
					"locator": "PDF page 116, printed 2-40, Lamp Matrix",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/lamp-matrix.md",
					"sha256": "28c4adb6749471f686344e631d6aff7adf7a95062145d2345a3e604f6d487f7d",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.lamp-locations",
					"locator": "PDF page 117, printed 2-41, Lamp Locations parts list",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/lamp-locations.md",
					"sha256": "ab00109255b88ed8cbf5a55358fe70205105af8f4effc5c96fe1a1248d381c6d",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.switch-matrix",
					"locator": "PDF page 118, printed 2-42, Switch Matrix",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/switch-matrix.md",
					"sha256": "2764b1d577ce7a4f629e38f5221623553d0b091cb96efb52c4a09b808c9e86df",
					"image": "evidence/excerpts/bally.theatre-of-magic.1995/switch-matrix.webp",
					"image_sha256": "d1031fc66ac11c53903b37e2b40c61e9cf75d5fda55bccbe5c9d6dea14ea589d",
					"image_derivation": "Theatre_of_Magic_OPS.pdf page 118, crop box 0.10,0.073,0.98,0.567 of the page, rendered at 300 dpi with pdftoppm, reduced to 700px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.switch-locations",
					"locator": "PDF page 119, printed 2-43, Switch Locations parts list",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/switch-locations.md",
					"sha256": "5ec316e8c8874073e48235d2c8ac70e64951b01b427a6256356cf3edb63337af",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.solenoid-flashlamp-locations",
					"locator": "PDF pages 120-121, printed 2-44/2-45, Solenoid/Flashlamp Locations parts list",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/solenoid-flashlamp-locations.md",
					"sha256": "8d3df2db58e0a26caf0e16d8362027bfd73bf9c9d200381f88c706683683af25",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.theatre-of-magic.eddy-and-trunk-teardown",
					"locator": "PDF page 45 (printed 1-45, Eddy Sensor Calibration) and PDF page 50 (printed 1-50, Magic Trunk teardown)",
					"path": "evidence/excerpts/bally.theatre-of-magic.1995/eddy-and-trunk-teardown.md",
					"sha256": "73ee6efa9327b9fdc098cc0bfcb56aed94a88ac3ea06580db3d839810487abf6",
					"method": "manual",
					"transcribed_by": "curator, verified against the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/theatre-of-magic-1995/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, verified "
				"against 300 dpi page renders regardless of the retained PDF's OCR text layer, together with the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/bally.theatre-of-magic.1995/."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/theatre-of-magic-1995/source/Theatre%20of%20Magic%20%28Bally%201995%29%202.4.vpx",
			"original_filename": "Theatre of Magic (Bally 1995) 2.4.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working table, version 2.4. Exact playfield bounds are "
				f"{TABLE_BOUNDS} -- unusually tall, so normalized coordinates are x/952 and y/2594.1, not the "
				"y/2162 divisor used by every standard-height WPC table curated so far. Geometry authority only "
				"for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/theatre-of-magic-1995/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (207,444 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "tom_14hb" (see the ROM-binding hazard note in the curator), the SolCallback table for '
				"solenoids 1-28 and 33-35 plus core.vbs sLLFlipper/sLRFlipper, the TrunkTimer_Timer trunk-rotation "
				"state machine, the trough/subway/lock/vanish-lock switch handlers, UpdateLamps' lamp-object bindings, "
				"and UpdateGI's GI-collection bindings."
			),
			"license": "NOASSERTION",
			"attribution": "table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/theatre-of-magic-1995/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
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
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			elif address in EDDY_SWITCHES:
				notes += (
					" Manual page 1-45 (\"Eddy Sensor Calibration\"): an eddy-current proximity sensor that detects "
					"the ball without a mechanical switch, not an opto or leaf contact. PinMAME's tomGameData "
					"inverted-switch mask does not cover this column position, matching the eddy construction "
					"(no opto normalization applies)."
				)
			elif address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed as an opto that is typically closed; PinMAME's tomGameData inverted-switch mask "
					"({0x00,0x00,0x00,0x3f,0x00,0xF0,...}, column 3 bits 0-5 and column 5 bits 4-7) covers it, so "
					"the public switch state is already normalized and must not be inverted again."
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
				if address in {13, 14, 21, 22, 23}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {13, 23} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316"),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly) in flipper_inputs.items():
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
				" Theatre of Magic has no upper flippers (tomGameData.hw.flippers declares FLIP_SW(FLIP_L) only) "
				"and the switch-locations parts list on manual page 2-43 marks this position Not Used (blank part "
				"number). The switch-matrix wiring page (2-42) nonetheless prints a stale generic Fliptronic-II-"
				"board template description here (\"Upper Right/Left Flipper EOS/Opto\") rather than \"NOT USED\"; "
				"the parts list is preferred per project policy and this printed matrix-page label is disclosed "
				"but not modeled as fitted hardware."
			)
			physical["location"] = "not installed"
		physical["notes"] = notes
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"F{address - 110}"},
				],
				roles=[role],
				physical=physical,
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable(
					"unused" if availability == "unused" else ("cabinet_or_service" if role.endswith(".button") else "internal_nonvisual"),
					MANUAL_SOURCE,
				),
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
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-Security CPU board U6 region",
					"switch_type": "dip",
					"notes": (
						"Country/option configuration DIP bank; the retained manual's country chart (page 2) "
						"documents America/European/French/German/Spain combinations for reference, but no "
						"specific ON/OFF combination is asserted for this definition."
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
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING.get(address, {})
			kind = "motor" if address in {17, 18} else "flasher" if address in {20, 24, 25, 26, 27, 28} else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})." if wiring_data else f"Printed solenoid/flasher table entry {address:02d}."
			if kind == "flasher" and address in FLASHER_BULBS:
				bulbs, playfield_emitters = FLASHER_BULBS[address]
				notes += f" Printed flashlamp complement: {bulbs}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {19, 22, 23, 36}:
				if address == 19:
					notes += (
						" Printed NOT USED (blank part number; voltage/drive connections through Q38/J126-3 remain "
						"populated, a wired-but-unpopulated flasher-bank position). The retained script implements "
						"a callback (SolTigerSaw) driving a rotating 'Saw' prop only when a table-author toggle "
						"TigerSaw is enabled -- TigerSaw = 1 (on) by default in this retained table -- but the "
						"assignment is commented \"'****** VPM controlled (only in prototypes)\" by the script's "
						"own author. Pinned driver.c independently lists 0.6A/0.61A prototype clones (tom_06, "
						"tom_061); this definition treats the motorized captive-ball 'Tiger Saw' disc as "
						"prototype-only and unfitted on the production 1.3X machine this definition binds."
					)
				elif address == 23:
					notes += (
						" The Solenoid/Flasher Table prints NOT USED (blank part number; connections through "
						"Q34/J126-7 remain populated), but the Solenoid/Flashlamp Locations page assigns this "
						"position a real #89 bulb and A-17803 assembly, 'Save Post Flasher'. The retained script "
						"resolves the disagreement: SolCallback(23) is implemented only when a table-author toggle "
						"CenterPost is enabled, commented 'Magic Post Flasher (***)', and CenterPost = 0 (off) by "
						"default in this retained table -- matching the Solenoid/Flasher Table's NOT USED. Treated "
						"as unfitted on the production machine; see conflict.optional-magic-post-solenoids-23-36."
					)
				elif address == 36:
					notes += (
						" Repurposed Fliptronic Upper Left Flipper Hold circuit (Q5); NOT USED coil part and color "
						"on the printed Flipper Circuits sub-table. The retained script implements a callback "
						"(SolMagicPost) only when the same CenterPost toggle used for solenoid 23 is enabled "
						"(default off); see conflict.optional-magic-post-solenoids-23-36."
					)
				else:
					notes += " Printed NOT USED; connections through Q30/J126-6 remain populated but no bulb or coil part is printed."
			if address in {33, 34, 35}:
				notes += (
					" Printed twice: once in the main Solenoid/Flasher Table under its own function name, and "
					"again in the Flipper Circuits sub-table as an 'Upr. Rt./Lt. Power/Hold' row sharing the "
					"identical drive transistor number -- confirming this Fliptronic-II-board upper-flipper "
					"position is repurposed for a non-flipper coil with no address translation, because "
					"tomGameData.hw.flippers declares no FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) bit."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-Security power driver board"}
			if wiring_data.get("driver_transistor"):
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
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
				if address == 7:
					extra["roles"] = ["cabinet.backbox"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				else:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {19, 23, 36}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Theatre of Magic playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Theatre of Magic playfield device.",
			31: "PinMAME's synthetic game-on state. tom.c does not call wpc_set_fastflip_addr, so this channel is not driven by a dedicated ROM RAM flag on this game.",
			32: "PinMAME reports this WPC state channel as always zero.",
			37: "Unused WPC output; this generation has no integrated LPDC board (GENWPC_HASWPC95 excludes GEN_WPCSECURITY), so 37-44 are simply unused address space.",
			38: "Unused WPC output; see 37.", 39: "Unused WPC output; see 37.", 40: "Unused WPC output; see 37.",
			41: "Unused WPC output; see 37.", 42: "Unused WPC output; see 37.", 43: "Unused WPC output; see 37.",
			44: "Unused WPC output; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-Security hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. tomGameData declares no custSol.",
		}[address]
		roles = ["internal.unused.wpc-output"]
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			unused = address in {82, 83, 84}
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += f" The printed lamp-locations parts list marks this insert with a bulb quantity of {LAMP_QUANTITIES[address]} and the retained table binds both bulbs, so it has two placements."
			if address in {87, 88}:
				notes += " Illuminated cabinet pushbutton assembly, no separate lamp assembly number."
			if address == 85:
				notes += " Rides inside the rotating trunk; the retained script repositions this light every tick to follow Trunk.RotZ, so it is a documented projection onto the trunk's own table-object center rather than a fixed playfield coordinate."
			physical["notes"] = notes

			LAMP_COLUMN_WIRING = {
				1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
				3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
				5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
				7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
			}
			LAMP_ROW_WIRING = {
				1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
				3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
				5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
				7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
			}
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
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The lamp-locations parts list marks this position Not Used."
			elif address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address == 85 else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], *coordinate_refs)
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
				"board": "WPC-Security power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in {0, 1}:
			notes += (
				" Wired exclusively through Backbox-column connectors on the printed Solenoid/Flasher Table, unlike "
				"strings 3-5 which are wired through Playfield-column connectors. The retained script's UpdateGI "
				"nonetheless drives a genuine playfield Light collection for this address as a stylized mood-"
				"lighting/color-grade effect (see conflict.gi-strings-1-2-backbox-vs-script-playfield-binding); this "
				"definition follows the manual for spatial classification and keeps this address a backbox device "
				"with no playfield coordinate."
			)
			extra["roles"] = ["cabinet.backbox"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's GI emitter collection for this string (UpdateGI in the retained "
				f"script): {'GIRight' if address == 2 else 'GIMiddle'}."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Wired through a Playfield-column connector per the manual, but the retained script's UpdateGI "
				"implements no case for this address, so no VPX object binds a coordinate to it; left with no "
				"spatial record rather than a fabricated one."
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
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Ball Trough")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Balls drain into the OutHole and are kicked down the chain toward Trough 4 (35, drain end) through "
			"Trough 3/2 to Trough 1 (32, eject end nearest the shooter). Solenoid 1 (SolRelease) kicks the ball "
			"resting on switch 32 toward the shooter lane. All five positions (Trough Jam 31 plus Trough 1-4 "
			"32-35) are printed optos that rest closed (column 3 of the inverted-switch mask), so a recreation "
			"asserts the public switch when a ball is present.",
			[
				("jam", "Trough Jam", ["switch.matrix-31"], "Jam-detection opto ahead of the eject position."),
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Manual shooter lane",
			"other",
			[],
			["switch.matrix-15"],
			"Theatre of Magic has a player-pulled spring plunger (a single retained Plunger table object; the "
			"manual's Solenoid/Flasher Table has no auto-plunger entry and swShooter=15 is the only shooter-lane "
			"switch). The ball ejected from the trough rests on shooter-lane switch 15 until the player pulls the "
			"plunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-15"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.trunk",
			"Motorized rotating Magic Trunk with internal ball lock and cube magnet",
			"motorized",
			[output_id("Box Clockwise"), output_id("Box Counter Clockwise"), output_id("Cube Magnet")],
			["switch.matrix-55", "switch.matrix-56", "switch.matrix-57", "switch.matrix-58", "switch.matrix-85"],
			"The headline mechanism: a single DC gearmotor (A-19782 Magic Trunk Motor Assembly, manual page 1-50 "
			"teardown diagram) rotates the trunk box through solenoids 17 (clockwise) and 18 (counter-clockwise). "
			"The retained script's TrunkTimer_Timer tracks one continuous TrunkAngle counter (TrunkSpeed = 0.12 "
			"degrees per millisecond, clamped 0-270) and asserts the corresponding Cube Position opto only while "
			"the trunk is within +/-15 degrees of that face's rotational home: switch 56 (Cube Position 1) near 0 "
			"degrees, switch 55 (Cube Position 4) near 90, switch 58 (Cube Position 3) near 180, switch 57 (Cube "
			"Position 2) near 270 -- all four assert together while the trunk is in transit between any two "
			"detents. A mechanical stop collar (manual Fig. 1) limits physical travel. Cube Magnet (solenoid 33, "
			"a repurposed Fliptronic Upper-Right-Power circuit) holds a ball inside the rotating box; while held, "
			"the retained script repositions the ball every tick to follow the trunk's own rotation (the "
			"'vanishing ball' effect), and the eddy-current Trunk Hit sensor (switch 85, in front of the trunk) "
			"is only reachable/droppable while the trunk sits at the 270-degree (Cube Position 2 / switch 57) "
			"face (sw85.IsDropped = NOT Controller.Switch(57)).",
			[
				("position-1", "Cube Position 1", ["switch.matrix-56"], "Trunk near 0 degrees."),
				("position-4", "Cube Position 4", ["switch.matrix-55"], "Trunk near 90 degrees."),
				("position-3", "Cube Position 3", ["switch.matrix-58"], "Trunk near 180 degrees."),
				("position-2", "Cube Position 2", ["switch.matrix-57"], "Trunk near 270 degrees; Trunk Hit target droppable here."),
				("hit", "Trunk Hit", ["switch.matrix-85"], "Eddy-current sensor in front of the trunk."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-19782",
		),
		mechanism(
			"mechanism.subway-lock",
			"Rear subway, ball lock, and trap door",
			"kicker",
			[output_id("Trap Door Up"), output_id("Trap Door Hold"), output_id("Subway Popper"), output_id("Sub Ball Release")],
			["switch.matrix-36", "switch.matrix-47", "switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44"],
			"A ball shot into the rear trunk entrance travels the subway (opto 36, microswitch 47) and is released "
			"onto Lock 1 (solenoid 34, Sub Ball Release, a repurposed Fliptronic Upper-Right-Hold circuit) where it "
			"progresses through Lock 1/2/3 (switches 41/42/43) toward the Trap Door assembly. Solenoid 3/14 "
			"(Trap Door Up/Hold) raises the trap door to admit a ball to the right ramp; Solenoid 4 (Subway Popper) "
			"kicks the ball resting on the Popper switch (44) back onto the playfield.",
			[
				("subway", "Ball in subway", ["switch.matrix-36", "switch.matrix-47"], "Subway opto then microswitch."),
				("lock-1", "Lock 1", ["switch.matrix-41"], "First lock position."),
				("lock-2", "Lock 2", ["switch.matrix-42"], "Second lock position."),
				("lock-3", "Lock 3", ["switch.matrix-43"], "Third lock position."),
				("popper", "Popper", ["switch.matrix-44"], "Ball ejected back to the playfield."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19939",
		),
		mechanism(
			"mechanism.vanish-lock",
			"Vanish Lock captive-ball kickout",
			"kicker",
			[output_id("Top Kickout")],
			["switch.matrix-83", "switch.matrix-84"],
			"Switches 83/84 (Vanish Lock 1/2) count up to two balls held at a captive lock. Solenoid 21 (Top "
			"Kickout) kicks the held ball(s) back to the playfield; the retained script's SolTopKickout reads "
			"sw83.ballcntover/sw84.ballcntover to choose a one-ball or two-ball kickout sound and releases the "
			"trunk's cube magnet (TrunkMagnets 0) in the same event.",
			[
				("lock-1", "Vanish Lock 1", ["switch.matrix-83"], "First captive position."),
				("lock-2", "Vanish Lock 2", ["switch.matrix-84"], "Second captive position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20003",
		),
		mechanism(
			"mechanism.captive-ball",
			"Static captive ball (Left Bank Target / Captive Ball Rest)",
			"other",
			[],
			["switch.matrix-51", "switch.matrix-52", "switch.matrix-77"],
			"A ball rests captive behind the Left Bank Target (2) standups (switch 51) and can be struck to rock "
			"against Captive Ball Rest (52) and Captive Ball Top (77). This production assembly is static -- it "
			"has no drive motor. It is distinct from the prototype-only motorized 'Tiger Saw' spinning-disc prop "
			"(solenoid 19), which the retained script's own comment marks 'VPM controlled (only in prototypes)' "
			"and this definition leaves unfitted for the production machine (see the unused-solenoid note on "
			"device 19).",
			[
				("rest", "Captive ball at rest", ["switch.matrix-52"], "Default resting position."),
				("top", "Captive ball at top", ["switch.matrix-77"], "Ball knocked to the top sensor."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-18059-15",
		),
		mechanism(
			"mechanism.magnetic-outlanes",
			"Left and right drain magnets with eddy sensors",
			"other",
			[output_id("Right Drain Magnet"), output_id("Left Drain Magnet")],
			["switch.matrix-45", "switch.matrix-48"],
			"Two eddy-current sensors (manual page 1-45, 'Auto Magna-Save Eddy (Hocus Pocus)') detect the ball in "
			"each outlane without a mechanical switch; solenoids 5 and 35 (Right/Left Drain Magnet, the latter a "
			"repurposed Fliptronic Upper-Left-Power circuit) energize to hold or redirect the ball, giving an "
			"automatic outlane save.",
			[
				("left", "Left drain eddy", ["switch.matrix-45"], "Left outlane eddy sensor."),
				("right", "Right drain eddy", ["switch.matrix-48"], "Right outlane eddy sensor."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-18543-1",
		),
		mechanism(
			"mechanism.diverters-and-gates",
			"Magnet diverter, loop post, top diverter post, and up/down gates",
			"gate",
			[
				output_id("Magnet Diverter"), output_id("Center Loop Post"), output_id("Top Diverter Post"),
				output_id("Left Up/Down Gate"), output_id("Right Up/Down Gate"),
			],
			[],
			"Solenoid 2 (Magnet Diverter, script callback SolSpiritRing) diverts a ball at the ramp/loop junction; "
			"solenoid 6 (Center Loop Post) and solenoid 8 (Top Diverter Post) raise/lower posts that route a ball "
			"between the inner and outer loops; solenoids 15/16 (Left/Right Up/Down Gate) admit a ball into a loop "
			"or lane while blocking return travel, driven through the retained script's SolGate3/SolGate1 "
			"handlers.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.knocker",
			"Cabinet knocker",
			"other",
			[output_id("Knocker")],
			[],
			"Solenoid 7 (Knocker) is a fitted cabinet/backbox coil (assembly B-10686-1) that raps the cabinet on "
			"replay/match awards, per the retained script's SolKnocker callback. Unlike Williams Monster Bash, "
			"this machine ships with a real knocker coil on this circuit.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="B-10686-1",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Sling"), output_id("Right Sling")],
			["switch.matrix-61", "switch.matrix-62"],
			"Standard slingshot kickers; the retained script's LeftSlingshot_Slingshot and RightSlingshot_"
			"Slingshot handlers pulse matrix addresses 61 and 62 and fire coils 9/10 in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-61"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Bottom Jet"), output_id("Middle Jet"), output_id("Top Jet")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-65"],
			"Three SW-11A-37 jet bumpers. The retained script's Bumper3_Hit/Bumper2_Hit/Bumper1_Hit handlers pulse "
			"switches 63, 64, and 65 and fire coils 11, 12, and 13 respectively, matching printed Bottom/Middle/Top "
			"Jet.",
			[
				("bottom", "Bottom jet bumper", ["switch.matrix-63"], "Bumper closest to the player."),
				("middle", "Middle jet bumper", ["switch.matrix-64"], "Middle bumper of the nest."),
				("top", "Top jet bumper", ["switch.matrix-65"], "Topmost bumper of the nest."),
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
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: the "
			"ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops to the "
			"hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. There are no upper "
			"flippers; the upper-flipper Fliptronic circuits (33-36, 115-118) are unfitted or repurposed for "
			"non-flipper coils.",
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
			"id": "relationship.ball-trough-release-eject",
			"kind": "pulse",
			"source": output_id("Ball Trough"),
			"destination": "switch.matrix-32",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.subway-ball-release-lock1",
			"kind": "pulse",
			"source": output_id("Sub Ball Release"),
			"destination": "switch.matrix-41",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.top-kickout-vanish-lock",
			"kind": "pulse",
			"source": output_id("Top Kickout"),
			"destination": "switch.matrix-83",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.gi-strings-1-2-backbox-vs-script-playfield-binding",
			"path": "outputs[binding.group=pinmame.output.gi,binding.device=0,1]",
			"description": (
				"The manual's own Solenoid/Flasher Table wires GI strings 1 and 2 (public PinMAME addresses 0 and "
				"1) exclusively through Backbox-column connectors (J120) with #555 bulbs, while strings 3-5 "
				"(addresses 2-4) are wired exclusively through Playfield-column connectors (J121) with #44 bulbs -- "
				"a clean, internally consistent split on a single printed table. The retained known-working "
				"script's UpdateGI(no, step) nonetheless implements cases 0 ('top') and 1 ('bottom left') by "
				"driving genuine playfield Light collections (GITop+GIBumpers, GILeft respectively) with dozens of "
				"members each, alongside a Table1.ColorGradeImage LUT swap -- i.e. the routine reads as a stylized "
				"playfield mood-lighting/color-grade effect keyed off which GI relay is active, not a literal "
				"per-bulb wiring replica; genuine backbox/insert-panel illumination would not plausibly drive "
				"dozens of scattered playfield bulbs. This is the same class of disagreement Williams Tales of the "
				"Arabian Nights already established for its own GI address 2 (a retained script visually "
				"contradicting its own manual's backbox wiring for a different address). The manual is physical-"
				"construction ground truth for a device's spatial classification, so this definition keeps GI "
				"addresses 0 and 1 controlled not_applicable/cabinet_or_service devices despite the script's "
				"visual behavior. Unresolved: whether any production unit's backbox strings genuinely double as a "
				"visual dimming relay for playfield GI would require a LibPinMAME harness trace or a second "
				"independent manual copy; this curation defaults to the manual's own wiring table. "
				"Resolution path: run the machine's own general-illumination test on an unrestored "
				"production unit and photograph what actually lights at the two steps for strings 1 and 2, "
				"or continuity-check the printed Wht-Brn J120-7/Q18 and Wht-Org J120-8/Q10 drives into the "
				"backbox insert panel against the playfield harness; a second printed copy of manual "
				"16-50039-101 would independently confirm the Backbox/Playfield split of the wiring table. "
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
			"id": "bally.theatre-of-magic.1995",
			"name": "Theatre of Magic",
			"manufacturer": "Bally",
			"year": 1995,
			"kind": "physical_pinball",
			"ipdb_id": 2845,
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
			"opdb_id": "G5BLE-MQ75Y",
		},
		"coverage": {
			"status": "partial",
			"missing": ["unresolved_conflicts", "spatial_placement"],
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
		"knowledge": {"path": "knowledge/bally/theatre-of-magic-1995.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Theatre of Magic device identifiers are not unique: {duplicates}")
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
	missing_spatial_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			missing_spatial_outputs.append(binding)
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
		"status": "partial",
		"blockers": [
			"GI address 4 (String 5) is wired playfield per the manual's own Solenoid/Flasher Table, but the "
			"retained script's UpdateGI implements no case for it, so no VPX object binds a coordinate to it. It "
			"is left with no spatial record rather than a fabricated one, keeping spatial_placement partial.",
			"conflict.gi-strings-1-2-backbox-vs-script-playfield-binding is unresolved: the manual documents GI "
			"addresses 0 and 1 as backbox-only, but the retained script visually drives genuine playfield Light "
			"collections for both. This keeps physical_wiring conflicted and unresolved_conflicts in coverage.missing.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/theatre-of-magic-1995/extracted-vpxtool.manifest.json",
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
		"missing_spatial_outputs": sorted(missing_spatial_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [{"group": "pinmame.output.lamp", "address": 85, "reason": "Lamp In Cube rides inside the rotating trunk; projected onto the trunk's own table-object center (Primitive Trunk)."}]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in (
				(17, "Box Clockwise: no separate motor-drive object; projected onto the trunk's own table-object center."),
				(18, "Box Counter Clockwise: same projection as 17."),
				(33, "Cube Magnet: fires inside the rotating trunk; projected onto the trunk's own table-object center."),
			)
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.theatre-of-magic.1995/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/theatre-of-magic-1995/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"geometry_dump": {
				"path": "external:pinmame-review-artifacts/theatre-of-magic-1995/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"lNhalo / lNaHalo / lNa3-style co-located brightness-doubling Light/Flasher objects (e.g. l18halo, l25halo, l37a, l38a, l85a3) -- one physical bulb each, matching the manual's single-bulb parts entries",
			"Bumper001-004 -- unreferenced decorative jet-bumper caps with no script callback",
		],
		"unresolved": [
			"gi.string-5 (GI address 4): playfield per the manual, no VPX object binding available.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Theatre of Magic (Bally, 1995) spatial review",
		"",
		f"Status: {report['status']}. Every switch, coil, and lamp address is enumerated and the trunk mechanism "
		"is fully mapped, but GI address 4 has no VPX-bound coordinate and GI addresses 0/1 carry an unresolved "
		"manual-vs-script wiring conflict; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Theatre of Magic (Bally 1995) 2.4.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}` -- unusually tall -- and every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and "
		f"y/{PLAYFIELD_HEIGHT:g} rounded to at most six fractional places. Using the more common y/2162 divisor "
		"used by every standard-height WPC game curated so far would have compressed every y coordinate by "
		"roughly 20% and silently corrupted the whole spatial set; front devices (flippers, trough, outhole) were "
		"sanity-checked to land near y=1.0 and top-lane devices near the low end of the range before this report "
		"was accepted.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the Bally operations manual is the "
		"physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; "
		"the retained table supplies geometry.",
		"- The retained manual PDF carries an OCR text layer, but every printed table used here was independently "
		"verified against a 300 dpi render of the same page and transcribed into "
		"`external:pinmame-review-artifacts/theatre-of-magic-1995/manual-transcription.md`; the OCR text was "
		"never treated as authoritative on its own.",
		"- The four Cube Position switches (55-58) have no fixed playfield sensor object; the retained script sets "
		"all four from one continuous TrunkAngle counter, so they are documented projections onto the rotating "
		"trunk's own table-object center (Primitive Trunk/Trunk1/Trunk2), matching the precedent established for "
		"Williams Monster Bash's Dracula-position optos and Williams Star Trek: TNG's idol-wheel optos.",
		"- Solenoids 17/18 (trunk motor) and 33 (cube magnet, fires inside the rotating box) are likewise projected "
		"onto the trunk's own table-object center rather than invented as separate fixed coordinates.",
		"- Lamp 85 (Lamp In Cube) rides inside the rotating trunk and is projected onto the same trunk object "
		"center for the same reason.",
		"- GI strings 3 and 4 (public addresses 2 and 3) use the retained table's GIRight/GIMiddle emitter "
		"collections, matching the retained script's UpdateGI dispatch. GI string 5 (address 4) is playfield-wired "
		"per the manual but has no UpdateGI case and therefore no VPX object binding; it is left with no spatial "
		"record at all rather than a fabricated one, and the corresponding definition entry omits its `spatial` "
		"key -- the same honest-omission pattern Williams Star Trek: TNG established for three lamps with no "
		"resolvable coordinate.",
		"- GI strings 1 and 2 (addresses 0 and 1) are backbox devices per the manual's own wiring table despite the "
		"retained script visually driving playfield light collections for both; see "
		"`conflict.gi-strings-1-2-backbox-vs-script-playfield-binding`.",
		"- Solenoids 19 (prototype-only 'Tiger Saw' captive-ball motor) and 23/36 (optional 'Magic Post' flasher "
		"and up/down coil, gated behind a table-author toggle that defaults off) are recorded `unused` on the "
		"production machine this definition binds, each with the disagreement fully disclosed in `physical.notes`.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
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
		f"- Outputs with no spatial record (missing evidence): {len(report['missing_spatial_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every switch, coil, and lamp address is enumerated with an honest disposition, the trunk/subway/lock/"
		"vanish-lock mechanism chain is fully documented with real causality from the retained script, and the "
		"opto-polarity sweep found zero disagreement between the manual's shading and PinMAME's inverted-switch "
		"mask. However, GI address 4 has no resolvable playfield coordinate and GI addresses 0/1 carry an "
		"unresolved conflict between the manual's backbox wiring and the retained script's playfield-collection "
		"binding. `coverage.dimensions.physical_wiring = \"conflicted\"` and "
		"`coverage.dimensions.spatial_placement = \"partial\"`, so promotion to `author_ready` is refused; the "
		"record stays `partial` with `coverage.missing = [\"unresolved_conflicts\", \"spatial_placement\"]` until "
		"a LibPinMAME harness trace or a second independent manual copy resolves the GI wiring disagreement and "
		"a VPX object binding is found for GI string 5.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- Curated VPX geometry reference, SHA-256 `{VPX_GEOMETRY_SHA256}`.",
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
		raise RuntimeError(f"Stale Theatre of Magic author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Theatre of Magic definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Theatre of Magic seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Theatre of Magic definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Theatre of Magic seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Theatre of Magic spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Theatre of Magic spatial review drifted from its deterministic curator: {markdown_path}")
	print("Theatre of Magic definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Theatre of Magic extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Theatre of Magic retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
