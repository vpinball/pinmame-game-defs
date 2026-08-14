"""Curate the physical Bally Creature from the Black Lagoon (1992) machine definition.

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
PARTIAL_PATH = ROOT / "machines/partial/bally/creature-from-the-black-lagoon-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/creature-from-the-black-lagoon-1992.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/creature-from-the-black-lagoon-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/creature-from-the-black-lagoon-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/creature-from-the-black-lagoon-1992.md"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/creature-from-the-black-lagoon-1992.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.bally.creature-from-the-black-lagoon.1992"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.creature-from-the-black-lagoon.1992"
VPX_TABLE_SOURCE = "vpx-table.cftbl-source"
VPX_SCRIPT_SOURCE = "vpx-script.cftbl-source"
VPX_EXTRACTION_SOURCE = "vpx-extraction.cftbl-source"

TABLE_SHA256 = "0527ebf5d66a6fa45d40a1ce2bdf1f395af7a3d77aed9bd4eb437399ee0bbb34"
SCRIPT_SHA256 = "e6393a87a33c1e53e3b32c3cff2af19dc14b2b4c8764f71dbb57736cadb98df8"
MANUAL_SHA256 = "d84d28a807505339f57676e0222adc6cc6fe7bef7371d31f9a9076ec33021d97"
MANUAL_TRANSCRIPTION_SHA256 = "5c30e18c830a9f2192d250bdc9ed178a4d7216a47cf637429776e098b5d5ec72"

EXTRACTION_RELATIVE_PATH = Path("bally/creature-from-the-black-lagoon-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/creature-from-the-black-lagoon-1992/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "bd9d362125af6225a95d10a2192230dac0d285b52da5e50e438e74536ff9b11c"
EXTRACTION_FILE_COUNT = 856
EXTRACTION_TOTAL_BYTES = 125041427

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

DRIVER_IDS = ("cftbl_l4", "cftbl_l4c", "cftbl_d4", "cftbl_l3", "cftbl_d3", "cftbl_l2", "cftbl_d2", "cftbl_p3")
DRIVER_COMPATIBILITY = {
	"cftbl_l4": (
		"identical",
		"Bally production L-4 game ROM shipped with the physical machine; the retained known-working "
		"table binds this exact driver (cGameName = \"cftbl_l4\").",
	),
	"cftbl_l4c": (
		"identical",
		"2020 community L-4C \"Competition + LED Ghost MOD\" ROM patch; a later firmware revision of the "
		"same physical machine with no controller-address or playfield change (LED-ghosting display fix "
		"plus a competition ruleset tweak).",
	),
	"cftbl_d4": (
		"identical",
		"D-4 LED Ghost Fix game ROM; a display-timing revision of the L-4 firmware with no I/O change.",
	),
	"cftbl_l3": (
		"identical",
		"L-3 game ROM; an earlier firmware revision of the same physical machine.",
	),
	"cftbl_d3": (
		"identical",
		"D-3 LED Ghost Fix game ROM; a display-timing revision of the L-3 firmware with no I/O change.",
	),
	"cftbl_l2": (
		"identical",
		"L-2 game ROM; an earlier firmware revision of the same physical machine.",
	),
	"cftbl_d2": (
		"identical",
		"D-2 LED Ghost Fix game ROM; a display-timing revision of the L-2 firmware with no I/O change.",
	),
	"cftbl_p3": (
		"identical",
		"P-3 Prototype (SP-1) game ROM, 1992; an earlier prototype sound ROM (u18-sp1.rom) paired with the "
		"same game ROM structure. Pinned driver.c clones it under cftbl_l4 with no separate hardware "
		"generation, so it is treated as an early-production firmware revision of the same physical "
		"machine rather than a distinct board revision.",
	),
}

# --- Printed switch matrix + locations (evidence/excerpts/.../switch-locations.md, switch-matrix.md);
# cross-validated cell-for-cell between the two pages with zero disagreement.
SWITCH_LABELS = {
	13: "Credit/Start Button", 14: "Plumb Bob Tilt", 15: "Top Left Rollover", 16: "Left Subway",
	17: "Center Subway", 18: "Center Shot",
	21: "Slam Tilt", 22: "Coin Door",
	25: "P of P-A-I-D", 26: "A of P-A-I-D", 27: "I of P-A-I-D", 28: "D of P-A-I-D",
	33: "Bottom Jet", 34: "Right Popper", 35: "Right Ramp Enter", 36: "Left Ramp Enter",
	37: "Lower Right Popper", 38: "Ramp Up/Down",
	41: "Cola", 42: "Hot Dog", 43: "Popcorn", 44: "Ice Cream",
	45: "Left Jet", 46: "Right Jet", 47: "Left Slingshot", 48: "Right Slingshot",
	51: "Left Out Lane", 52: "Left Return Lane", 53: "Start Combo", 54: "Right Out Lane",
	55: "Outhole", 56: "Right Trough", 57: "Center Trough", 58: "Left Trough",
	61: "Right Ramp Exit", 62: "Left Ramp Exit", 63: "Center Lane Exit", 64: "Upper Ramp",
	65: "Bowl", 66: "Shooter",
}
UNUSED_MATRIX_ADDRESSES = {
	11, 12, 23, 24, 31, 32, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88,
}
# The Switch Locations page's LED-plus-phototransistor construction pair (the only opto-construction
# marker in this manual; the switch-matrix wiring page carries no shaded-cell legend at all).
OPTO_SWITCHES = {34, 37}
# Pinned cftblGameData inverted-switch mask: index1 (column1) = 0x10 (bit4 -> row5 -> addr15); index3
# (column3) = 0xc8 (bits3,6,7 -> rows4,7,8 -> addr34,37,38). Confirmed both by manual construction (34,
# 37 are printed opto pairs) and, for the two non-opto addresses, by independent runtime/mechanism
# evidence: switch 15's retained script handlers explicitly invert hit/unhit (`sw15_Hit` clears the
# switch, `sw15_Unhit` sets it -- the opposite of every other rollover in the file), and switch 38 is a
# ramp-position microswitch driven purely from `cftbl_handleMech`'s motor-position state, not from a
# Hit event.
PINMAME_NORMALIZED_OPTO_SWITCHES = {15, 34, 37, 38}

SWITCH_PARTS = {
	13: ("20-9663-1", None), 14: ("20-6502-A", None), 15: ("5647-12693-19", None),
	16: ("5647-12693-21", None), 17: ("5647-12693-21", None), 18: ("5647-12693-36", None),
	21: ("27-1066", None), 22: ("5643-09288-00", None),
	25: ("5647-12693-19", None), 26: ("5647-12693-19", None), 27: ("5647-12693-19", None), 28: ("5647-12693-19", None),
	33: ("SW-11A-37", None), 34: ("A-14231 (LED) with A-14232 (Trans.)", None), 35: ("5647-12693-26", None),
	36: ("5647-12693-21", None), 37: ("A-14231 (LED) with A-14232 (Trans.)", None), 38: ("5647-12693-11", None),
	41: ("A-16206-2", None), 42: ("A-16206-2", None), 43: ("A-16206-2", None), 44: ("A-16206-2", None),
	45: ("SW-11A-37", None), 46: ("SW-11A-37", None), 47: ("SW-1A-114", None), 48: ("SW-1A-114", None),
	51: ("5647-12693-19", None), 52: ("5647-12693-19", None), 53: ("5647-12693-19", None), 54: ("5647-12693-19", None),
	55: ("5647-12133-12", None), 56: ("5647-12693-08", None), 57: ("5647-09957-00", None), 58: ("5647-09957-00", None),
	61: ("5647-12693-36", None), 62: ("5647-12693-21", None), 63: ("5647-12693-19", None), 64: ("5647-12693-21", None),
	65: ("5647-12693-21", None), 66: ("5647-12693-04", None),
}
SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "leaf", 16: "leaf", 17: "leaf", 18: "leaf",
	21: "tilt", 22: "microswitch",
	25: "leaf", 26: "leaf", 27: "leaf", 28: "leaf",
	33: "leaf", 34: "opto", 35: "leaf", 36: "leaf", 37: "opto", 38: "leaf",
	41: "leaf", 42: "leaf", 43: "leaf", 44: "leaf",
	45: "leaf", 46: "leaf", 47: "leaf", 48: "leaf",
	51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf",
	55: "leaf", 56: "leaf", 57: "leaf", 58: "leaf",
	61: "leaf", 62: "leaf", 63: "leaf", 64: "leaf", 65: "leaf", 66: "leaf",
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
	1: ("Orange-Brown", "J205-1", "U18-11"), 2: ("Orange-Red", "J205-2", "U18-9"),
	3: ("Orange-Black", "J205-3", "U18-5"), 4: ("Orange-Yellow", "J205-4", "U18-7"),
	5: ("Orange-Green", "J205-6", "U19-11"), 6: ("Orange-Blue", "J205-7", "U19-9"),
	7: ("Orange-Violet", "J205-8", "U19-5"), 8: ("Orange-Gray", "J205-9", "U19-7"),
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
# Fliptronic F1-F8, printed switch-matrix page 3-2 wiring block. F1-F4 are also confirmed by the
# Switch Locations parts list (SW-1A-193 EOS leaf + A-15894 opto board); F5-F8 appear ONLY on this
# wiring page -- see conflict.upper-flipper-switches-unconfirmed-fitment.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Blue-Black", "J905-5"),
}

# --- Printed solenoid/flasher table (evidence/excerpts/.../solenoid-flasher-locations.md,
# solenoid-flasher-wiring.md). Canonical labels follow the wiring page (3-5), which agrees with the
# switch-side naming; the Locations page (2-43) prints "Bottom Right Popper" for solenoid 3 and "Right
# Popper Flasher" for solenoid 16 where the wiring page and this curator use "Lower Right Popper" (which
# matches switch 37's own name on both switch pages) and "Right Popper Slide Flasher" (the Locations
# page's own fuller name) respectively; both are the same manual disagreeing with itself in small ways,
# not evidence disagreements, and are noted in physical.notes rather than raised as first-class conflicts.
SOLENOID_LABELS = {
	1: "Top Right Popper", 2: "Left Subway Enter Flasher", 3: "Lower Right Popper", 4: "Trough (Ball Release)",
	5: "Right Slingshot", 6: "Left Slingshot", 7: "Knocker", 8: "Bottom Right Flasher",
	9: "Back Flashers", 10: "Bowl Flasher", 11: "Creature Flasher (Insert)", 12: "Outhole",
	13: "Left Jet", 14: "Right Jet", 15: "Bottom Jet", 16: "Right Popper Slide Flasher",
	17: "Bottom Left Flasher", 18: "Right Ramp Flasher", 19: "Left Ramp Flasher",
	20: "Sequential G.I. #1 Select", 21: "Hologram Push Motor", 22: "Center Hole Flasher",
	23: "Up/Down Ramp (Up)", 24: "Sequential G.I. #2 Select", 25: "Start Movie Flashers",
	26: "Up/Down Ramp (Down)", 27: "Creature Mirror Motor", 28: "Hologram Lamp",
}
SOLENOID_ASSEMBLIES = {
	1: "A-15769", 2: "A-8798", 3: "A-15842", 4: "B-9362-L-2", 5: "A-14369-R", 6: "A-14369-L",
	7: "B-10686-1", 8: "A-8798", 9: "A-8798", 10: "A-9359", 11: None, 12: "A-8039-3",
	13: "A-9415-2", 14: "A-9415-2", 15: "A-9415-2", 16: "A-8798", 17: "A-8798", 18: "A-8798",
	19: "A-8798", 20: "A-15541", 21: "A-15988", 22: "A-8798", 23: "A-16042", 24: "A-15541",
	25: "A-9302", 26: "A-16042", 27: "A-15988", 28: "A-15857",
}
# kind classification per the manual's own "Solenoid Type" column, except 20/24 which this curation
# overrides to control_signal (see the note on SOLENOID_LABELS above and the mechanism writeup):
# despite the manual printing "Flasher" for 20 and "Low Power" for 24 -- an internal inconsistency for
# what is functionally the identical 2-bit decoder address-select role -- neither drives a playfield
# bulb of its own.
SOLENOID_KINDS = {
	1: "coil", 2: "flasher", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "flasher",
	9: "flasher", 10: "flasher", 11: "flasher", 12: "coil", 13: "coil", 14: "coil", 15: "coil",
	16: "flasher", 17: "flasher", 18: "flasher", 19: "flasher", 20: "control_signal",
	21: "motor", 22: "flasher", 23: "motor", 24: "control_signal", 25: "flasher", 26: "motor",
	27: "motor", 28: "flasher",
}
SOLENOID_PRINTED_TYPE = {
	1: "High Power", 2: "High Power", 3: "High Power", 4: "High Power", 5: "High Power", 6: "High Power",
	7: "High Power", 8: "High Power", 9: "Low Power", 10: "Low Power", 11: "Low Power", 12: "Low Power",
	13: "Low Power", 14: "Low Power", 15: "Low Power", 16: "Low Power", 17: "Flasher", 18: "Flasher",
	19: "Flasher", 20: "Flasher", 21: "Flasher", 22: "Flasher", 23: "Low Power", 24: "Low Power",
	25: "Flasher", 26: "Flasher", 27: "Flasher", 28: "Flasher",
}
SOLENOID_WIRING = {
	1: dict(driver_transistor="Q82", control_connection="J130-1", power_connection="J107-3", control_wire="Vio-Brn"),
	2: dict(driver_transistor="Q80", control_connection="J130-2", power_connection="J107-5", control_wire="Vio-Red"),
	3: dict(driver_transistor="Q78", control_connection="J130-4", power_connection="J107-3", control_wire="Vio-Org"),
	4: dict(driver_transistor="Q76", control_connection="J130-5", power_connection="J107-3", control_wire="Vio-Yel"),
	5: dict(driver_transistor="Q64", control_connection="J130-6", power_connection="J107-3", control_wire="Vio-Grn"),
	6: dict(driver_transistor="Q66", control_connection="J130-7", power_connection="J107-3", control_wire="Vio-Blu"),
	7: dict(driver_transistor="Q68", control_connection="J130-8", power_connection="J107-3", control_wire="Vio-Blk"),
	8: dict(driver_transistor="Q70", control_connection="J130-9", power_connection="J107-5", control_wire="Vio-Gry"),
	9: dict(driver_transistor="Q58", control_connection="J127-1", power_connection="J107-6", control_wire="Brn-Blk"),
	10: dict(driver_transistor="Q56", control_connection="J127-3", power_connection="J107-6", control_wire="Brn-Red"),
	11: dict(driver_transistor="Q54", control_connection="J129-4", power_connection="J106-5", control_wire="Brn-Org"),
	12: dict(driver_transistor="Q52", control_connection="J127-5", power_connection="J107-2", control_wire="Brn-Yel"),
	13: dict(driver_transistor="Q50", control_connection="J127-6", power_connection="J107-2", control_wire="Brn-Grn"),
	14: dict(driver_transistor="Q48", control_connection="J127-7", power_connection="J107-2", control_wire="Brn-Blu"),
	15: dict(driver_transistor="Q46", control_connection="J127-8", power_connection="J107-2", control_wire="Brn-Vio"),
	16: dict(driver_transistor="Q44", control_connection="J127-9", power_connection="J107-5", control_wire="Brn-Gry"),
	17: dict(driver_transistor="Q42", control_connection="J126-1", power_connection="J107-5", control_wire="Blk-Brn"),
	18: dict(driver_transistor="Q40", control_connection="J126-2", power_connection="J107-5", control_wire="Blk-Red"),
	19: dict(driver_transistor="Q38", control_connection="J126-3", power_connection="J107-5", control_wire="Blk-Org"),
	20: dict(driver_transistor="Q36", control_connection="J126-4", power_connection="J118-2", control_wire="Blk-Yel"),
	21: dict(driver_transistor="Q28", control_connection="J126-5", power_connection="J104-1,2", control_wire="Blu-Grn"),
	22: dict(driver_transistor="Q30", control_connection="J126-6", power_connection="J107-6", control_wire="Blu-Blk"),
	23: dict(driver_transistor="Q34", control_connection="J126-7", power_connection="J107-1", control_wire="Blu-Vio"),
	24: dict(driver_transistor="Q32", control_connection="J126-8", power_connection="J118-2", control_wire="Blu-Gry"),
	25: dict(driver_transistor="Q26", control_connection="J122-1", power_connection="J107-6", control_wire="Blu-Brn"),
	26: dict(driver_transistor="Q24", control_connection="J122-2", power_connection="J107-1", control_wire="Blu-Red"),
	27: dict(driver_transistor="Q22", control_connection="J123-4", power_connection="J104-1,2", control_wire="Blu-Org"),
	28: dict(driver_transistor="Q20", control_connection="J123-5", power_connection="J118-2", control_wire="Blu-Yel"),
}
# Retained script callbacks/bindings, per solenoid address (only the ACTIVE, uncommented assignments;
# the script carries an earlier commented-out block for 1-28 that a later block partly re-enables).
SOLENOID_CALLBACKS = {
	1: "RightUpperKicker (kicks sw34)", 3: "RightLowerKicker (kicks sw37)", 4: "ReleaseBall (kicks sw56)",
	7: 'vpmSolSound SoundFX("Knocker",DOFKnocker)', 8: "Sol08 (FlSol08.visible)", 10: "Sol10 (FlSol10.visible)",
	11: "Sol11 (FlSol11.visible)", 12: "SolOuthole (kicks sw55)", 17: "Sol17 (FlSol17.visible)",
	22: "Sol22 (FlSol22.visible)", 23: "SolRampUp", 26: "SolRampDown", 27: "CreatureMotorMirror (creature.visible)",
	28: "HoloLamp (creature.visible)",
}
# Addresses with no SolCallback assignment at all in the retained script (dead/unscripted in this
# specific fan recreation, even though the manual documents them as real fitted circuits): 2, 5, 6, 9,
# 13, 14, 15, 16, 18, 19, 20, 21, 24, 25. 5/6/13/14/15 are handled natively by the VPX slingshot/bumper
# physics objects instead of a SolCallback; 20/24 are explicitly commented "does not work properly with
# rom !!! so I did not use this, but for reference".
SOLENOID_UNSCRIPTED_NOTE = (
	"The retained script assigns no SolCallback for this address, so pulsing it produces no visible "
	"effect in this specific fan recreation; the manual's own fitment evidence is authoritative regardless."
)

FLASHER_BULBS = {
	2: ("#89 playfield, #906 (2) insert", "Left Subway Enter Flasher"),
	8: ("#89 playfield, #906 (2) insert", "Bottom Right Flasher"),
	9: ("#89 (2) playfield only", "Back Flashers"),
	10: ("#89 playfield, #906 (2) insert", "Bowl Flasher"),
	11: ("#906 (2) insert only, no playfield bulb", "Creature Flasher"),
	16: ("#89 playfield, #906 (2) insert", "Right Popper Slide Flasher"),
	17: ("#89 playfield, #906 (1) insert", "Bottom Left Flasher"),
	18: ("#89 playfield, #906 (2) insert", "Right Ramp Flasher"),
	19: ("#89 playfield, #906 (2) insert", "Left Ramp Flasher"),
	22: ("#89 playfield, #906 (2) insert", "Center Hole Flasher"),
	25: ("#89 (2) playfield only", "Start Movie Flashers"),
	28: ("#1156", "Hologram Lamp"),
}

GI_STRINGS = {
	0: ("Sequential G.I. #1", "J120-1", "Q18", "J120-7", "#86"),
	1: ("Insert/Playfield Middle", "J120-2 / J121-2", "Q10", "J120-8 / J121-8", "#44 / #555"),
	2: ("Insert/Playfield Upper", "J120-3 / J121-3", "Q14", "J120-9 / J121-9", "#44 / #555"),
	3: ("Sequential G.I. #2", "J120-5", "Q15", "J120-10", "#86"),
	4: ("Insert/Playfield Lower", "J120-6 / J121-6", "Q12", "J120-11 / J121-11", "#44 / #555"),
}

# --- Printed lamp matrix (evidence/excerpts/.../lamp-locations.md, lamp-matrix.md). All 64 matrix
# positions are populated; there is no "Not Used" lamp address on this machine.
LAMP_LABELS = {
	11: "(P)-A-I-D", 12: "P-(A)-I-D", 13: "P-A-(I)-D", 14: "P-A-I-(D)",
	15: "Left Jet", 16: "Right Jet", 17: "Bottom Jet", 18: "Admit One",
	21: "(K)-I-S-S", 22: "K-(I)-S-S", 23: "K-I-(S)-S", 24: "K-I-S-(S)",
	25: "10 Million", 26: "20 Million", 27: "30 Million", 28: "Specials",
	31: "Start Mega Menu", 32: "Playground Award", 33: "Lite Big Millions", 34: "Slide",
	35: "Right Search", 36: "Right Video", 37: "Right Start Movie", 38: "Mega Menu",
	41: "Lips", 42: "Left Search", 43: "Left Video", 44: "Left Start Movie",
	45: "Combo Award", 46: "Parking O.K.", 47: "Move Your Car", 48: "Extra Ball",
	51: "Snack Bar", 52: "Center Search", 53: "Cola", 54: "Hotdog",
	55: "Super Jackpot", 56: "Jackpot", 57: "Rescue", 58: "Multiball Restart",
	61: "Free Pass", 62: "Build Combo", 63: "Unlimited Millions", 64: "Creature Feature",
	65: "Extra Ball Countdown", 66: "Big Millions", 67: "Movie Madness", 68: "Snack Attack",
	71: "C (Creature)", 72: "R (Creature)", 73: "E (Creature)", 74: "A (Creature)",
	75: "T (Creature)", 76: "U (Creature)", 77: "R (Creature)", 78: "E (Creature)",
	81: "(F)-I-L-M", 82: "F-(I)-L-M", 83: "F-I-(L)-M", 84: "F-I-L-(M)",
	85: "Start Combo", 86: "Popcorn", 87: "Ice Cream", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: "A-15731", 12: "A-15731", 13: "A-15731", 14: "A-15731",
	15: "A-15727", 16: "A-15727", 17: "A-15727", 18: "A-11754",
	21: "A-15734", 22: "A-15734", 23: "A-15734", 24: "A-15734",
	25: "A-15734", 26: "A-15734", 27: "A-11271", 28: "A-11271",
	31: "A-11754", 32: "A-8882", 33: "A-11754", 34: "A-8882",
	35: "A-15728", 36: "A-15728", 37: "A-15728", 38: "A-8882",
	41: "A-15730", 42: "A-15730", 43: "A-15730", 44: "A-15730",
	45: "A-15733", 46: "A-15733", 47: "A-15733", 48: "A-15733",
	51: "A-11733", 52: "A-11754", 53: "A-11754", 54: "A-11754",
	55: "A-14305", 56: "A-14305", 57: "A-14305", 58: "A-14305",
	61: "A-11754", 62: "A-11271", 63: "C-12709", 64: "C-12709",
	65: "C-12709", 66: "C-12709", 67: "C-12709", 68: "C-12709",
	71: None, 72: None, 73: None, 74: None, 75: None, 76: None, 77: None, 78: None,
	81: "A-15732", 82: "A-15732", 83: "A-15732", 84: "A-15732",
	85: "A-11271", 86: "A-11754", 87: "A-11754", 88: None,
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J138-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# Column-9 chase-light addresses (see the mechanism writeup): cftblGameData declares lampCol = 1, and
# pinned wpc.c's WPC_CFTBL handling writes the same 2-bit-decoder chase pattern directly into
# coreGlobals.lampMatrix[8] -- the public lamp-matrix's 9th row/column, i.e. addresses 91-98 -- rather
# than through the normal lamp-strobe scan. This is a real, emulator-computed public address group with
# no printed manual line item of its own (the manual only names the assembly "Sequential G.I. #1/#2").
CHASE_LAMP_LABELS = {90 + n: f"Curly Ramp Chase Light {n}" for n in range(1, 9)}

# --- Normalized playfield coordinates from the retained extraction (x/964, y/2162;
# review-artifacts/creature/vpx-geometry.txt has the full raw dump).
SWITCH_POSITIONS = {
	15: [(0.049111, 0.19029)], 16: [(0.195943, 0.405437)], 17: [(0.462425, 0.382413)],
	25: [(0.529659, 0.094217)], 26: [(0.626339, 0.090824)], 27: [(0.720405, 0.08805)], 28: [(0.815199, 0.084961)],
	34: [(0.859834, 0.352609)], 35: [(0.666824, 0.501653)], 36: [(0.215317, 0.322391)],
	37: [(0.84146, 0.592598)], 51: [(0.052052, 0.738465)], 52: [(0.127819, 0.738682)],
	53: [(0.786979, 0.739935)], 54: [(0.861669, 0.74024)], 55: [(0.469214, 0.967569)],
	56: [(0.813787, 0.878631)], 57: [(0.756061, 0.89311)], 58: [(0.699852, 0.908373)],
	61: [(0.3203, 0.228185)], 62: [(0.373618, 0.090791)], 63: [(0.422203, 0.071702)],
	64: [(0.267433, 0.12773)], 65: [(0.828343, 0.778473)], 66: [(0.937859, 0.884605)],
	# Projected positions (see SWITCH_PROJECTIONS below): 33/45/46 onto their own jet-bumper object,
	# 38 onto the moveRamp mechanism primitive.
	33: [(0.628203, 0.262458)], 38: [(0.108224, 0.078951)],
	45: [(0.515321, 0.177189)], 46: [(0.738429, 0.178966)],
}
# Devices with no separate playfield trigger object: their public switch state is set directly by
# another mechanism's own state (bumper hit event, ramp motor position counter, target-bank hit
# event), so they are documented projections onto that mechanism's own retained table object rather
# than an invented sensor position.
SWITCH_PROJECTIONS = {
	33: "Projected onto the Bumper3 jet-bumper object (table object center): the retained script's Bumper3_Hit handler pulses switch 33 directly from the bumper ring's own collision event, matching Bottom Jet.",
	38: "Projected onto the moveRamp Primitive (table object center), the mechanism's own moving ramp section: the retained script sets Controller.Switch(38) directly from the ramp motor's up/down state inside the SolRampUp/SolRampDown handlers, not from a Hit event on a fixed object, and pinned cftbl_handleMech does the same via core_setSw(swRampUpDown, locals.creaturerampPos).",
	45: "Projected onto the Bumper1 jet-bumper object (table object center): Bumper1_Hit pulses switch 45 (Left Jet) directly from the bumper ring's own collision event.",
	46: "Projected onto the Bumper2 jet-bumper object (table object center): Bumper2_Hit pulses switch 46 (Right Jet) directly from the bumper ring's own collision event.",
}
SOLENOID_POSITIONS = {
	1: [(0.859834, 0.352609)], 3: [(0.84146, 0.592598)], 4: [(0.813787, 0.878631)], 12: [(0.469214, 0.967569)],
	13: [(0.515321, 0.177189)], 14: [(0.738429, 0.178966)], 15: [(0.628203, 0.262458)],
}
SOLENOID_PROJECTIONS = {
	1: "Projected onto the sw34 Kicker object: solenoid 1 (RightUpperKicker) fires the same Top Right Popper kicker that switch 34 (Right Popper) senses -- the same physical hole.",
	3: "Projected onto the sw37 Kicker object: solenoid 3 (RightLowerKicker) fires the same Lower Right Popper kicker that switch 37 senses -- the same physical hole.",
	4: "Projected onto the sw56 Kicker object: solenoid 4 (ReleaseBall) fires the trough-release kicker at the Right Trough position (switch 56).",
	12: "Projected onto the sw55 Kicker object: solenoid 12 (SolOuthole) fires the Outhole kicker at the same position switch 55 senses.",
	13: "Projected onto the Bumper1 jet-bumper object: solenoid 13 (Left Jet) is the coil inside the same bumper ring switch 45 senses.",
	14: "Projected onto the Bumper2 jet-bumper object: solenoid 14 (Right Jet) is the coil inside the same bumper ring switch 46 senses.",
	15: "Projected onto the Bumper3 jet-bumper object: solenoid 15 (Bottom Jet) is the coil inside the same bumper ring switch 33 senses.",
}

GI_POSITIONS = {
	0: [
		(0.183755, 0.091886), (0.220911, 0.163841), (0.205328, 0.206614), (0.157365, 0.248872),
		(0.081079, 0.287584), (0.011615, 0.33001), (0.025754, 0.429979), (0.094603, 0.477579),
		(0.187835, 0.511567), (0.323689, 0.528014), (0.448888, 0.522349), (0.534334, 0.499599),
		(0.577968, 0.467805), (0.611572, 0.430345), (0.640578, 0.392017), (0.674593, 0.34339),
		(0.681242, 0.29389), (0.64322, 0.263983), (0.580426, 0.241486), (0.489492, 0.227132),
		(0.387585, 0.243435), (0.314683, 0.266053), (0.283333, 0.316629), (0.300203, 0.364992),
		(0.699773, 0.742086), (0.650959, 0.759628), (0.645131, 0.796338), (0.689573, 0.81453),
		(0.7821, 0.814854), (0.821442, 0.797637), (0.830913, 0.762552), (0.8025, 0.74436),
	],
	1: [
		(0.605118, 0.423425), (0.546104, 0.360383), (0.793223, 0.434389), (0.107177, 0.340792),
		(0.14652, 0.464317), (0.793492, 0.433566), (0.606001, 0.423425), (0.103773, 0.339535),
		(0.264215, 0.27293), (0.548832, 0.357625), (0.858153, 0.286669), (0.885815, 0.259259),
	],
	2: [
		(0.381075, 0.15941), (0.397103, 0.195469), (0.389817, 0.129848), (0.224434, 0.116854),
		(0.21642, 0.133747), (0.573737, 0.096958), (0.674278, 0.094684), (0.767534, 0.087971),
	],
	4: [
		(0.500757, 0.5), (0.860842, 0.616388), (0.205958, 0.746421), (0.18653, 0.718701),
		(0.701014, 0.757272), (0.73139, 0.724131), (0.058422, 0.61463), (0.056785, 0.5824),
		(0.051867, 0.549508), (0.866989, 0.527033), (0.86357, 0.53827), (0.049562, 0.613989),
		(0.202628, 0.75597), (0.168818, 0.726094), (0.70136, 0.756107), (0.740088, 0.72486),
		(0.861111, 0.619433),
	],
}
LAMP_POSITIONS = {
	11: [(0.527505, 0.047551)], 12: [(0.621579, 0.044546)], 13: [(0.717385, 0.040973)], 14: [(0.812189, 0.037805)],
	15: [(0.561382, 0.223093)], 16: [(0.696166, 0.223479)], 17: [(0.634739, 0.172173)], 18: [(0.817167, 0.016436)],
	21: [(0.220096, 0.615919)], 22: [(0.229454, 0.589393)], 23: [(0.251652, 0.564237)], 24: [(0.290858, 0.54301)],
	25: [(0.14587, 0.643574)], 26: [(0.126842, 0.668406)], 27: [(0.156825, 0.777953)], 28: [(0.051381, 0.786788)],
	31: [(0.661802, 0.687891)], 32: [(0.690469, 0.653253)], 33: [(0.721232, 0.615295)], 34: [(0.755789, 0.574247)],
	35: [(0.786798, 0.535143)], 36: [(0.804189, 0.510145)], 37: [(0.864052, 0.463422)], 38: [(0.383209, 0.503996)],
	41: [(0.169184, 0.565173)], 42: [(0.122812, 0.536938)], 43: [(0.108776, 0.510224)], 44: [(0.048416, 0.461106)],
	45: [(0.360118, 0.412692)], 46: [(0.360583, 0.377025)], 47: [(0.365939, 0.344585)], 48: [(0.362217, 0.307315)],
	51: [(0.551608, 0.408665)], 52: [(0.446687, 0.405201)], 53: [(0.219555, 0.485881)], 54: [(0.217409, 0.447854)],
	55: [(0.516692, 0.311817)], 56: [(0.51314, 0.32578)], 57: [(0.515155, 0.320335)], 58: [(0.50397, 0.328367)],
	61: [(0.456315, 0.866525)], 62: [(0.237629, 0.358773)], 63: [(0.091487, 0.207829)], 64: [(0.091303, 0.210767)],
	65: [(0.090872, 0.21214)], 66: [(0.729889, 0.467168)], 67: [(0.729983, 0.471401)], 68: [(0.733535, 0.475665)],
	81: [(0.354357, 0.808002)], 82: [(0.422113, 0.802429)], 83: [(0.492533, 0.803251)], 84: [(0.559264, 0.808824)],
	85: [(0.788731, 0.669898)], 86: [(0.513915, 0.440853)], 87: [(0.537567, 0.47898)],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Creature retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Creature extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Creature retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Creature retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Creature retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


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
			"locator": "Pinned catalog driver records for the cftbl_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/cftbl.c cftblGameData GEN_WPCFLIPTRON with wpc_dispDMD, hw = "
				"{FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), swCol=0, lampCol=1, custSol=0, soundBoard=0, "
				"display=0, gameSpecific1=WPC_CFTBL, gameSpecific2=0}, the inverted-switch mask "
				"{0x00,0x10,0x00,0xc8,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}, swStart/swTilt/swSlamTilt/"
				"swCoinDoor defines, and cftbl_handleMech (core_setSw(swRampUpDown, locals.creaturerampPos) "
				"driven by core_getSol(sRampUp)/core_getSol(sRampDown)); src/wpc/wpc.h WPC_CFTBL=0x01 "
				"\"chase light 2 bit decoder from solenoid #3 output, wired through triacs to 2 GI outputs, "
				"leading to 8 additional PWM controlled GI\"; src/wpc/wpc.c WPC_SOLENOID3/WPC_GILAMPS cases "
				"computing chase_2b from (pulsedSolState>>22 & 2)|(pulsedSolState>>19 & 1) (solenoids 24 and "
				"20 respectively) and chase_gi from conductingGITriacs bits 0 and 3 (GI addresses 0 and 3), "
				"then writing coreGlobals.lampMatrix[8] = 0x11 << chase_2b -- the public lamp-matrix's 9th "
				"row, i.e. addresses 91-98; src/wpc/core.h CORE_FIRSTUFLIPSOL=33/CORE_FIRSTLFLIPSOL=45/"
				"CORE_FLIPPERSWCOL=11/CORE_STDSWCOLS=12; src/wpc/wpc.h WPC_swF1..WPC_swF8; "
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
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic-block and no-LPDC notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.creature-from-the-black-lagoon.1992/arcade-museum/Creature_From_The_Black_Lagoon_OPS.pdf",
			"original_filename": "Creature_From_The_Black_Lagoon_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"134-page Adobe Paper Capture OCR scan of the Bally Creature from the Black Lagoon operations "
				"manual, retrieved from arcade-museum.com because the Internet Archive item of the same name "
				"carries only a .zip. Printed pages 2-40 through 2-43 carry the lamp/switch/solenoid location "
				"parts lists; printed pages 3-2 through 3-8 carry the switch matrix, lamp matrix, solenoid/"
				"flasher table, and general-illumination/flipper wiring."
			),
			"license": "NOASSERTION",
			"attribution": "Bally Manufacturing Corporation; scan hosted by arcade-museum.com",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.creature.switch-locations",
					"locator": "PDF page 101, printed 2-41, Switch Locations parts list",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/switch-locations.md",
					"sha256": "d5cd1b235ba8d3aff865eae2bc99ea86de1e17f42d635cebb996349e313c620e",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.creature.switch-matrix",
					"locator": "PDF page 106, printed 3-2, SWITCHES / SWITCH MATRIX CIRCUIT",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/switch-matrix.md",
					"sha256": "fdbf44392fa79e772ff862b9c2ff0958e6d9246093affef89da02b2649ae2593",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.creature.lamp-locations",
					"locator": "PDF page 100, printed 2-40, Lamp Locations parts list",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/lamp-locations.md",
					"sha256": "6f49583d8e4a5a8424e797f5bf0ee908c25dd6e886a5224423dc2f1cbe857e33",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.creature.lamp-matrix",
					"locator": "PDF page 108, printed 3-4, LAMPS / LAMP MATRIX CIRCUIT",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/lamp-matrix.md",
					"sha256": "ea62438e5b62c1dbed84c0cfe1fbd5fc975922a68a82e4f2ed771acdcc5ef4e3",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.creature.solenoid-flasher-locations",
					"locator": "PDF page 103, printed 2-43, Solenoid/Flasher Locations + General Illumination + Flipper Coils",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/solenoid-flasher-locations.md",
					"sha256": "9bbfff44447cace0efe06b32dddf99c9c1a4593ac8a6629b5e18dda6c655361c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.creature.solenoid-flasher-wiring",
					"locator": "PDF page 109, printed 3-5, SOLENOID/FLASHER TABLE + General Illumination + Flipper Circuits",
					"path": "evidence/excerpts/bally.creature-from-the-black-lagoon.1992/solenoid-flasher-wiring.md",
					"sha256": "e018865c87050161a1ee21e0e85ac0c5866fdb1d76efab2f2ae4898f70e522e7",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/creature/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription index tying every rendered manual table used by this "
				"definition to its excerpt, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/bally.creature-from-the-black-lagoon.1992/."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/source/Creature%20From%20The%20Black%20Lagoon%20%28Bally%201992%29.vpx",
			"original_filename": "Creature From The Black Lagoon (Bally 1992).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for "
				"named table objects. This is the smallest retained extraction in the project to date (856 "
				"files), and several documented devices have no matching table object; those are left "
				"spatially unresolved rather than projected onto an unrelated object."
			),
			"license": "NOASSERTION",
			"attribution": "unknown VPX table author",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (104,439 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "cftbl_l4", the SolCallback table for solenoids 1,3,4,7,8,10,11,12,17,22,23,26,'
				"27,28,31 (fast-flip tilt), the sw15_Hit/sw15_Unhit inverted-polarity handlers, the "
				"SolRampUp/SolRampDown ramp-motor handlers driving Controller.Switch(38) directly, the "
				"Bumper1_Hit/2_Hit/3_Hit handlers pulsing switches 45/46/33, the RightUpperKicker/"
				"RightLowerKicker/SolOuthole/ReleaseBall handlers kicking sw34/sw37/sw55/sw56, the "
				"UpdateGIstuff/UpdateGIObjects dispatch binding GI address 0 to the chaselights collection "
				"(32 swirlramplight Light objects), GI 1/2/4 to the GI_Middle/GI_Upper/GI_Lower collections, "
				"and the commented-out 'does not work properly with rom !!!' SeqGI1/SeqGI2 handlers for "
				"solenoids 20/24 confirming this recreation drives the chase lights from GI0 on/off alone "
				"rather than the true 2-bit decoder state."
			),
			"license": "NOASSERTION",
			"attribution": "unknown VPX table author",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; {EXTRACTION_FILE_COUNT} files, produced with vpxtool from the retained "
				f"table. Bounds are {TABLE_BOUNDS}."
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
				wiring={"board": "WPC Fliptronic CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
			identifier = f"switch.matrix-{address}"
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
				notes += " The Switch Locations parts list and the Switch Matrix wiring page both mark this position Not Used."
				label = f"Not Used Matrix Position {address}"
			elif address in OPTO_SWITCHES:
				notes += (
					" Printed on the Switch Locations parts list with a two-row LED-plus-phototransistor "
					"construction pair (A-14231 LED over A-14232 Trans.), the manual's only opto-construction "
					"marker for this machine; PinMAME's cftblGameData inverted-switch mask normalizes it."
				)
			elif address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				extra_reason = (
					"the retained script's own sw15_Hit/sw15_Unhit handlers invert the usual hit/unhit polarity "
					"(clearing the switch on Hit, setting it on UnHit -- the opposite of every other rollover in "
					"the file)"
					if address == 15
					else "pinned cftbl_handleMech sets its public state purely from the ramp motor's own position "
					"(core_setSw(swRampUpDown, locals.creaturerampPos)) rather than from a Hit event"
				)
				notes += (
					" PinMAME's cftblGameData inverted-switch mask normalizes this address as well, even though "
					f"its printed part ({part_number}) is an ordinary leaf switch with no LED/Trans opto pair; "
					f"{extra_reason}, which independently corroborates a normally-closed physical construction."
				)
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 53:
				notes += (
					' The manual\'s "Where Used" column names this address by its rule function ("Start Combo") '
					"rather than a physical location, unlike its symmetric partner 52 (\"Left Return Lane\"); its "
					"retained-table position sits on the opposite (right) side of the playfield from 52, and it "
					"is wired on the same matrix row/column pattern as the other return-lane switches, so it is "
					"treated as the physical right return lane whose sole printed game function is starting the "
					"Combo feature."
				)
			if address == 3:
				pass
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
			else:
				availability = "used"
				extra["normally_closed"] = address in PINMAME_NORMALIZED_OPTO_SWITCHES
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address == 18:
					extra["roles"] = ["feature.move-your-car"]
					notes += (
						" The retained script defines Sub sw18_Hit(), but no object literally named 'sw18' exists "
						"anywhere in the extraction (Trigger, Kicker, Gate, or otherwise), so the handler is "
						"unreachable in this specific recreation and no VPX geometry is available for this address."
					)
					physical["notes"] = notes
				elif address in SWITCH_POSITIONS:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
				# else: no spatial key at all -- unresolved (address 18 above, and no other case reaches here).
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Right Flipper End of Stroke", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-193"),
		112: ("Right Flipper Opto", "flipper.lower.right.button", "used", True, "opto", "A-15894"),
		113: ("Left Flipper End of Stroke", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-193"),
		114: ("Left Flipper Opto", "flipper.lower.left.button", "used", True, "opto", "A-15894"),
		115: ("Upper Right Flipper End of Stroke", "internal.unresolved.flipper", "unknown", None, None, None),
		116: ("Upper Right Flipper Opto", "internal.unresolved.flipper", "unknown", None, "opto", None),
		117: ("Upper Left Flipper End of Stroke", "internal.unresolved.flipper", "unknown", None, None, None),
		118: ("Upper Left Flipper Opto", "internal.unresolved.flipper", "unknown", None, "opto", None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		notes = f"Printed Fliptronic grounded switch F{address - 110}, connector {connection}."
		if availability == "unknown":
			notes += (
				" cftblGameData declares FLIP_SW(FLIP_L | FLIP_U), and the switch-matrix wiring page (3-2) "
				"prints real wire colors and Fliptronic-II-board connector pins for this position labeled "
				'"Upper Right/Left Flipper End of Stroke/Opto" with no "Not Used" marking anywhere on that '
				"page. But the Switch Locations parts list (2-41), a different page of the same manual, lists "
				"only F1-F4 and omits F5-F8 entirely -- not even as a Not Used row -- and no upper-flipper "
				"coil circuit is printed anywhere in the Solenoid/Flasher Locations table (cftblGameData's "
				"FLIP_SOL(FLIP_L) only enables the lower coils). Fitment is unconfirmed; see "
				"conflict.upper-flipper-switches-unconfirmed-fitment."
			)
		elif switch_type == "opto":
			notes += (
				" Printed opto board position. This generation's WPC_FLIPPERS register read unconditionally "
				"complements the flipper switch column regardless of hardware generation, so the public "
				"switch state is already normalized here exactly as on WPC-95."
			)
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "WPC Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
		}
		if normally_closed is not None:
			extra["normally_closed"] = bool(normally_closed)
		if availability == "unknown":
			pass  # no spatial key at all: fitment itself is unresolved, so neither located nor not_applicable is honest.
		else:
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
					"location": "WPC Fliptronic CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC CPU-board country/option configuration DIP bank. The retained transcription of this "
						"manual does not include a per-country switch-combination chart, so no specific ON/OFF "
						"combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	import re as _re

	return "device." + _re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		kind = SOLENOID_KINDS[address]
		wiring_data = SOLENOID_WIRING[address]
		physical: dict[str, Any] = {}
		if SOLENOID_ASSEMBLIES.get(address):
			physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
		printed_type = SOLENOID_PRINTED_TYPE[address]
		notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
		if address in FLASHER_BULBS:
			bulbs, wiring_label = FLASHER_BULBS[address]
			notes += f" Printed flashlamp complement: {bulbs}."
		if address == 3:
			notes += ' The Solenoid/Flasher Locations page (2-43) instead prints "Bottom Right Popper" for this address; the wiring page (3-5) and both switch-side pages (which name switch 37 "Lower Right Popper") agree on the name used here.'
		if address == 16:
			notes += ' The Solenoid/Flasher Table (3-5) abbreviates this to "Right Popper Flasher"; the fuller Locations-page name is used here.'
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		else:
			notes += " " + SOLENOID_UNSCRIPTED_NOTE
		if address in {20, 24}:
			other = 24 if address == 20 else 20
			notes += (
				" This is the Sequential G.I. board's 2-bit decoder address-select line (assembly A-15541), "
				"not a coil or a bulb of its own: pinned wpc.c's WPC_CFTBL handling reads bits from this "
				f"solenoid together with address {other} to select which of four chase-light groups the GI "
				"triacs feed, and writes the result into the public lamp matrix's 9th row (addresses 91-98). "
				'The manual\'s own "Solenoid Type" column is internally inconsistent for this identical role '
				f'(printing "{printed_type}" here); it is overridden with kind="control_signal" and no '
				"assembly-driven playfield placement, since neither line drives a visible bulb by itself."
			)
		if address in {27, 28}:
			notes += (
				' Printed with a "Δ" marker, "Located in cabinet bottom", on the Solenoid/Flasher Locations '
				"page: genuinely cabinet-mounted hardware for the hologram effect, not playfield hardware, "
				"even though the resulting hologram image appears to float above the playfield."
			)
		if address == 11:
			notes += (
				" This is the only dual-mount-style flasher item on the Locations page that prints an Insert "
				"connection with no Playfield connection at all -- a genuine backbox-insert-only device."
			)
		if address == 7:
			notes += (
				" Marked \"*Not shown\" on the Solenoid/Flasher Locations page, consistent with the standard "
				"WPC cabinet-mounted knocker (mounted to the cabinet wall near the coin door, not on the "
				"playfield)."
			)
		physical["notes"] = notes

		wiring: dict[str, Any] = {"board": "WPC Fliptronic power driver board", "driver_transistor": wiring_data["driver_transistor"]}
		wiring["control_connection"] = wiring_data["control_connection"]
		wiring["power_connection"] = wiring_data["power_connection"]
		wiring["control_wire"] = wiring_data["control_wire"]
		aliases = [
			{"namespace": "pinmame.solenoid", "value": str(address)},
			{"namespace": "manual.address", "value": f"{address:02d}"},
		]
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if address == 7:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in {27, 28}:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in {20, 24}:
			extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE, MANUAL_SOURCE)
		elif address in SOLENOID_POSITIONS:
			role = "effect" if kind in {"coil", "motor"} else "emitter"
			coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *coordinate_refs)
			if address in SOLENOID_PROJECTIONS:
				physical["notes"] += " " + SOLENOID_PROJECTIONS[address]
		elif address == 21:
			extra["spatial"] = located(identifier, "effect", [(0.461806, 0.678542)], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			physical["notes"] += (
				" No distinct VPX object represents the push motor itself; projected onto the Flasher "
				"'creature' object's position, the hologram image's own on-table location, since the push "
				"motor is part of the same under-playfield hologram apparatus and no separate mechanism "
				"primitive exists in the retained extraction."
			)
		# else: unresolved, no spatial key (addresses with a real fitted flasher but no matching table object).
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if address in {87 + n for n in range(1, 9)} and address != 88:
				pass
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": {
					"board": "WPC Fliptronic power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if 71 <= address <= 78:
				notes += (
					' Printed "*Located on backbox insert"; this address spells one letter of the backbox '
					'"CREATURE" header. The retained table\'s matching Light object sits at normalized x '
					"outside [0,1] (behind the rear/backglass edge), independently confirming it is not "
					"playfield hardware."
				)
				extra["roles"] = ["cabinet.header-display"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 88:
				notes += " Illuminated Start Button lamp inside the cabinet pushbutton assembly, sharing its function with switch 13."
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in LAMP_POSITIONS:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			physical["notes"] = notes
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					"used",
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)

	for address, label in CHASE_LAMP_LABELS.items():
		identifier = f"lamp.chase-{address}"
		items.append(
			_device(
				identifier,
				label,
				"lamp",
				"pinmame.output.lamp",
				address,
				"used",
				(CORE_SOURCE, MANUAL_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={
					"notes": (
						"Not a printed manual line item: cftblGameData declares lampCol = 1, and pinned wpc.c's "
						"WPC_CFTBL handling writes the 2-bit-decoder chase-light pattern directly into the public "
						"lamp matrix's 9th row (coreGlobals.lampMatrix[8]) rather than through the normal lamp-"
						"strobe scan, so addresses 91-98 are a real, emulator-computed public lamp group for the "
						'"8 ramp lights \'Chase Light\'" the driver\'s own comment describes. The retained VPX '
						"table does not read Controller.Lamp for any of these eight addresses; it instead drives "
						"its own 32-bulb swirlramplight collection from GI address 0's on/off state alone (see "
						"the Sequential G.I. mechanism), so no VPX object represents any individual address in "
						"this group and none is given a coordinate."
					)
				},
				# no spatial key: genuinely unresolved, not merely absent from the manual.
			)
		)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address}"
		notes = f"Printed general-illumination string {address:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address:02d}"},
			],
			"wiring": {
				"board": "WPC Fliptronic power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			if address == 0:
				notes += (
					" This is the true power bus for the 8 physical curly-ramp chase bulbs (see solenoids 20/24 "
					"and lamps 91-98), but the manual prints no per-string bulb count for it. The retained "
					"table's own 'chaselights' emitter collection (32 swirlramplight Light objects, the table "
					"author's own stylized chase animation rather than a faithful 8-bulb model) supplies the "
					"quantity and every coordinate here."
				)
			else:
				notes += (
					" The manual prints no per-string bulb count, so the physical quantity and every emitter "
					"coordinate come from the retained table's own GI emitter collection for this string "
					"(UpdateGIstuff/UpdateGIObjects in the retained script)."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" This is the address-select-line partner of solenoid 24 (see the mechanism writeup); the "
				"retained script's UpdateGIstuff calls FadeGI 203 ('Chaselights #2') but never calls "
				"UpdateGIObjects for it, so no playfield emitter collection is bound to this string in this "
				"recreation."
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
			"Three-position trough and ball release",
			"kicker",
			[output_id("Trough (Ball Release)")],
			["switch.matrix-56", "switch.matrix-57", "switch.matrix-58"],
			"Three balls rest on plain leaf switches 56 (Right Trough, nearest the release), 57 (Center "
			"Trough), and 58 (Left Trough, drain entrance). The retained script's UpdateTroughTimer kicks the "
			"ball resting on 57 onto 56's position and the ball on 58 onto 57's, cascading balls toward the "
			"release end whenever a downstream position empties; solenoid 4 (ReleaseBall) then kicks the ball "
			"resting on switch 56 out to the shooter lane. This is a simpler, three-ball trough with no "
			"dedicated eject-opto stage, unlike the four/five-position optical troughs on later WPC-Fliptronic "
			"machines.",
			[
				("ball-1", "Trough Ball 1 (release position)", ["switch.matrix-56"], "Ball nearest the release coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-57"], "Second trough position."),
				("ball-3", "Trough Ball 3 (drain entrance)", ["switch.matrix-58"], "Drain entrance and third trough position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.outhole",
			"Outhole",
			"kicker",
			[output_id("Outhole")],
			["switch.matrix-55"],
			"A drained ball rests on outhole switch 55 (SolOuthole/RandomSoundBallRelease-style handling in "
			"the retained script pulses solenoid 12 to kick it into the trough).",
			[("held", "Ball in the outhole", ["switch.matrix-55"], "Outhole switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-8039-3",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Manual plunger shooter lane",
			"other",
			[],
			["switch.matrix-66"],
			"No solenoid in the printed table drives the shooter lane; the retained extraction includes a "
			"single Plunger primitive (a manual pull-plunger, not an auto-launcher). Switch 66 (Shooter) "
			"senses the ball resting in the lane before the player plunges it.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-66"], "Shooter-lane switch.")],
			MANUAL_SOURCE, VPX_TABLE_SOURCE,
		),
		mechanism(
			"mechanism.subway-tunnel",
			"KISS and Snackbar subway tunnel to the Lower Right Popper",
			"other",
			[output_id("Lower Right Popper")],
			["switch.matrix-16", "switch.matrix-17", "switch.matrix-37"],
			'Pinned cftbl_stateDef routes both "Left Subway" (switch 16, the K-I-S-S hole, per the driver\'s '
			'own key-help comment "L = Left Subway Hole (K-I-S-S)") and "Center Subway" (switch 17, the '
			'Snackbar hole, "H = Center Subway Hole (Snackbar)") to the same stLowRPopper ball state, meaning '
			"both entry holes feed an internal tunnel that exits through the Lower Right Popper (switch 37, "
			"solenoid 3). The Right Subway state (the F-I-L-M hole) is separate and exits through the Top "
			"Right Popper (switch 34, solenoid 1) instead -- see mechanism.right-popper.",
			[
				("kiss-entry", "K-I-S-S hole entry", ["switch.matrix-16"], "Left subway entry."),
				("snackbar-entry", "Snackbar hole entry", ["switch.matrix-17"], "Center subway entry."),
				("exit", "Tunnel exit at the Lower Right Popper", ["switch.matrix-37"], "Shared exit for both entries."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.right-popper",
			"Top Right Popper (F-I-L-M hole)",
			"kicker",
			[output_id("Top Right Popper")],
			["switch.matrix-34"],
			'A ball resting on opto 34 (Right Popper, the "f-i-l-M" hole per the driver\'s key-help comment '
			'"Z = Right Subway (f-i-l-M)") is kicked back to the playfield by solenoid 1 (RightUpperKicker).',
			[("held", "Ball in the top right popper", ["switch.matrix-34"], "Right popper opto.")],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15769",
		),
		mechanism(
			"mechanism.creature-ramp",
			"Motorized up/down curly ramp",
			"motorized",
			[output_id("Up/Down Ramp (Up)"), output_id("Up/Down Ramp (Down)")],
			["switch.matrix-38", "switch.matrix-35", "switch.matrix-36", "switch.matrix-61", "switch.matrix-62", "switch.matrix-64"],
			"A DC gearmotor (A-16042 assembly) raises and lowers the curly ramp between an Up position (the "
			"ball climbs the Creature Ramp) and a Down position (the ball instead travels the ordinary Left "
			"Ramp). Solenoid 23 drives it up and solenoid 26 drives it down; the retained script's "
			"SolRampUp/SolRampDown handlers set Controller.Switch(38) directly from the motor's own commanded "
			"direction rather than from a Hit event, matching pinned cftbl_handleMech's "
			"core_setSw(swRampUpDown, locals.creaturerampPos). Switches 35 (Right Ramp Enter) and 36 (Left "
			"Ramp Enter) sense balls entering either ramp mouth; 61 (Right Ramp Exit), 62 (Left Ramp Exit), "
			"and 64 (Upper Ramp) sense the ball on its way back to the playfield. Pinned cftbl_stateDef's "
			"stLRamp hook state reads core_getSw(swRampUpDown) to decide whether a ball entering the left "
			"ramp mouth climbs the Creature Ramp or takes the ordinary left-ramp path.",
			[
				("up", "Ramp up (Creature Ramp active)", ["switch.matrix-38"], "Motor commanded up."),
				("down", "Ramp down (ordinary left ramp active)", ["switch.matrix-38"], "Motor commanded down."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16042",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet"), output_id("Right Jet"), output_id("Bottom Jet")],
			["switch.matrix-45", "switch.matrix-46", "switch.matrix-33"],
			"Three jet bumpers (SW-11A-37 skirt switches, A-9415-2 coil assemblies). The retained script's "
			"Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit handlers pulse switches 45, 46, and 33 and fire coils "
			"13, 14, and 15 respectively, matching printed Left/Right/Bottom Jet.",
			[
				("left", "Left jet bumper", ["switch.matrix-45"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-46"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-33"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-47", "switch.matrix-48"],
			"Two kicking slingshots (SW-1A-114 switches, A-14369-L/R coil assemblies) driven natively by the "
			"retained table's Wall.LeftSlingShot/Wall.RightSlingShot slingshot objects, firing coils 6 (left) "
			"and 5 (right).",
			[
				("left", "Left slingshot", ["switch.matrix-47"], "Left slingshot switch."),
				("right", "Right slingshot", ["switch.matrix-48"], "Right slingshot switch."),
			],
			MANUAL_SOURCE, VPX_TABLE_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14369-R",
		),
		mechanism(
			"mechanism.paid-lane",
			"P-A-I-D rollover lane",
			"other",
			[],
			["switch.matrix-25", "switch.matrix-26", "switch.matrix-27", "switch.matrix-28"],
			'Four sequential rollovers spelling "P-A-I-D", each independently lit; pinned cftbl_stateDef awards '
			"all four in sequence via the Paid states, and the driver's own #define names encode which letter "
			"is lit at each address (swPaid=25 P, swpAid=26 A, swpaId=27 I, swpaiD=28 D).",
			[
				("p", "P lit", ["switch.matrix-25"], "First rollover."),
				("a", "A lit", ["switch.matrix-26"], "Second rollover."),
				("i", "I lit", ["switch.matrix-27"], "Third rollover."),
				("d", "D lit", ["switch.matrix-28"], "Fourth rollover."),
			],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.snackbar-targets",
			"Snackbar standup target bank",
			"drop_target_bank",
			[],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44"],
			"Four standup targets (Cola, Hot Dog, Popcorn, Ice Cream) feeding the Snackbar/Snack Bar award "
			"chain; the retained table models each as a HitTarget object (sw41-sw44) and the script pulses "
			"the matching switch address with vpmTimer.PulseSw on each hit.",
			[
				("cola", "Cola target", ["switch.matrix-41"], "Snackbar target."),
				("hot-dog", "Hot Dog target", ["switch.matrix-42"], "Snackbar target."),
				("popcorn", "Popcorn target", ["switch.matrix-43"], "Snackbar target."),
				("ice-cream", "Ice Cream target", ["switch.matrix-44"], "Snackbar target."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16206-2",
		),
		mechanism(
			"mechanism.bowl-loop",
			"Creature Bowl orbit loop",
			"other",
			[],
			["switch.matrix-65"],
			'A single opto/leaf switch (Bowl, 65) is passed up to four times as a ball circles the orbit loop; '
			'pinned cftbl_stateDef chains "In Bowl Loop 1" through "In Bowl Loop 4" and a final "Creature Bowl" '
			"state, all keyed on the same swBowl=65 switch, counting passes rather than sensing four distinct "
			"physical positions.",
			[("pass", "Ball passing the bowl-loop switch", ["switch.matrix-65"], "Counted up to four times per orbit.")],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.sequential-gi-chase",
			"Sequential G.I. curly-ramp chase lights",
			"other",
			[output_id("Sequential G.I. #1 Select"), output_id("Sequential G.I. #2 Select")],
			[],
			"WPC_CFTBL custom hardware unique to this machine (pinned wpc.h: \"chase light 2 bit decoder from "
			"solenoid #3 output, wired through triacs to 2 GI outputs, leading to 8 additional PWM controlled "
			"GI\"). Solenoids 20 and 24 are not coils; they are the two address-select bits of a 2-bit decoder "
			"on the A-15541 Sequential G.I. board. GI addresses 0 and 3 (public GI outputs 1 and 4, 1-based, "
			"matching the driver comment) are the power buses the decoder gates: pinned wpc.c reads "
			"chase_2b from (solenoid 24 state << 1) | (solenoid 20 state), reads chase_gi from whether GI "
			"triacs 0 and 3 are conducting, and writes the selected 8-bit pattern into "
			"coreGlobals.lampMatrix[8] -- the public lamp matrix's 9th row, addresses 91-98 (see lamp outputs "
			"91-98). This produces a moving chase pattern across the 8 physical curly-ramp bulbs as the "
			"decoder cycles through its four selectable groups. The retained VPX table does not read "
			"addresses 91-98 at all; it instead drives its own 32-object 'chaselights' Light collection from "
			"a self-contained internal timer (swirlramplight1_Timer) keyed only to GI address 0's on/off "
			"state, approximating rather than reproducing the true decoder-selected pattern -- confirmed by "
			"its own commented-out SeqGI1/SeqGI2 handlers noting 'does not work properly with rom !!!'.",
			[],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15541",
		),
		mechanism(
			"mechanism.hologram",
			"Creature hologram effect",
			"other",
			[output_id("Hologram Push Motor"), output_id("Hologram Lamp"), output_id("Creature Mirror Motor")],
			[],
			"A three-part cabinet-mounted illusion: a 48VAC push motor (solenoid 21) positions a mechanism "
			"under the playfield, a #1156 hologram lamp (solenoid 28) illuminates a hidden image, and a "
			"48VAC spinning mirror motor (solenoid 27, printed 'Δ Located in cabinet bottom' alongside "
			"solenoid 28) reflects that image up through the playfield glass so the Creature figure appears "
			"to float above the play surface -- the machine's signature feature. The retained script's "
			"HoloLamp handler (bound to solenoid 28) sets a holoState flag and makes the 'creature' Flasher "
			"object visible, and a separate reflectionTrigger disables ball reflection rendering while the "
			"hologram is active so the illusion is not broken by a mirrored ball image. There is also a "
			"backbox-insert-only 'Hologram Creature Flasher' (solenoid 11) that lights a companion insert "
			"graphic, distinct from the hologram projection itself.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15988",
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two flippers (FL-11629 right, FL-15411 left) on Fliptronic circuits. Each flipper has an "
			"end-of-stroke leaf switch (111 right, 113 left) and an opto button/position sensor (112 right, "
			"114 left). Fitment of any corresponding upper-flipper hardware at 115-118 is unresolved; see "
			"conflict.upper-flipper-switches-unconfirmed-fitment.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "End-of-stroke switch 111 and opto 112."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "End-of-stroke switch 113 and opto 114."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 right with A-15205-L-4 left",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.subway-tunnel-to-lower-right-popper",
			"kind": "direct",
			"source": "switch.matrix-16",
			"destination": output_id("Lower Right Popper"),
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE),
		},
		{
			"id": "relationship.snackbar-tunnel-to-lower-right-popper",
			"kind": "direct",
			"source": "switch.matrix-17",
			"destination": output_id("Lower Right Popper"),
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.upper-flipper-switches-unconfirmed-fitment",
			"path": "inputs[binding.device=115,116,117,118]",
			"description": (
				"Pinned cftblGameData declares FLIP_SW(FLIP_L | FLIP_U), and the Switch Matrix wiring page "
				'(printed 3-2) prints real, distinct wire colors and Fliptronic-II-board connector pins for '
				'all eight F1-F8 positions, labeling F5-F8 "Upper Right/Left Flipper End of Stroke/Opto" with '
				'no "Not Used" marking anywhere on that page -- the same treatment as the fitted F1-F4 '
				"positions. But the Switch Locations parts list (printed 2-41), a different page of the same "
				"manual, lists only F1-F4 with real part numbers and omits F5-F8 entirely, not even as a "
				'"Not Used" row (unlike matrix positions 11-12, 23-24, 31-32, and 67-88, which the same page '
				"marks Not Used explicitly). No upper-flipper coil circuit is printed anywhere in the "
				"Solenoid/Flasher Locations or Solenoid/Flasher Table pages, consistent with cftblGameData's "
				"FLIP_SOL(FLIP_L) enabling only the lower coils -- but that is evidence about the coils, not "
				"about whether the EOS/opto switches for a physically absent upper flipper pair were also left "
				"unpopulated on this specific machine. The retained known-working script assigns no "
				"Controller.Switch call anywhere for addresses 111-118, so it provides no runtime evidence "
				"either way. Two pages of the same primary source disagree on whether this hardware is fitted, "
				"and no VPX geometry, script behavior, or PinMAME structural declaration settles it. "
				"Resolution path: a clear photograph of an unrestored machine's Fliptronic II board, a parts "
				"listing that itemizes F5-F8 by part number the way F1-F4 are itemized, or a LibPinMAME "
				"gameplay-harness trace observing whether legal ROM ever reads a nonzero idle state at "
				"111-118 that is inconsistent with permanently-open unpopulated switches. Unresolved."
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
			"id": "bally.creature-from-the-black-lagoon.1992",
			"name": "Creature from the Black Lagoon",
			"manufacturer": "Bally",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 588,
			"playfield": {"width": 964.0, "height": 2162.0, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
			"opdb_id": "GrNWn-MQdqZ",
		},
		"coverage": {
			"status": "partial",
			"missing": ["output_enumeration", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "candidate",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "conflicted",
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
		"knowledge": {"path": "knowledge/bally/creature-from-the-black-lagoon-1992.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Creature device identifiers are not unique: {duplicates}")
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
		spatial = device.get("spatial")
		if spatial is not None and spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
		"blockers": [
			"Switch 18 (Center Shot / Move Your Car feature) has a script handler (Sub sw18_Hit) but no "
			"matching table object anywhere in the retained extraction, so its spatial placement is "
			"unresolved.",
			"Fliptronic switches 115-118 (upper flipper block) have unconfirmed fitment "
			"(conflict.upper-flipper-switches-unconfirmed-fitment) and therefore carry neither a location "
			"nor a not_applicable record.",
			"GI address 3 ('Sequential G.I. #2') is a real printed GI string with no bound emitter "
			"collection in the retained table, so it has no placement.",
			"Lamp addresses 91-98 (the true Sequential G.I. chase-light bulbs, computed by PinMAME's "
			"WPC_CFTBL hardware model) are not read by the retained script at all, so none has a placement.",
			"Solenoids 2, 9, 16, 18, 19, and 25 are real fitted flashers per the manual with no matching "
			"playfield-facing VPX object: the retained table's only bound object for the related addresses "
			"8, 10, 11, 17, and 22 (FlSol08/10/11/17/22) sits at normalized y well outside [0,1], reading as "
			"a backbox/insert-panel companion bulb rather than the playfield dome the manual documents, so "
			"those five addresses are left unresolved rather than placed at an out-of-bounds coordinate.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/creature-from-the-black-lagoon-1992/extracted-vpxtool.manifest.json",
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
		"unresolved_inputs": sorted(unresolved_inputs),
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		]
		+ [{"group": "pinmame.output.solenoid", "address": 21, "reason": "Projected onto the Flasher 'creature' object (the hologram's own on-table position); see mechanism.hologram."}],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.creature-from-the-black-lagoon.1992/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/creature/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [],
		"unresolved": [
			f"switch address {address}" for address in (18, 115, 116, 117, 118)
		]
		+ ["gi address 3", "lamp addresses 91-98"]
		+ [f"solenoid address {address}" for address in (2, 9, 16, 18, 19, 25)],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Creature from the Black Lagoon (Bally, 1992) spatial review",
		"",
		f"Status: {report['status']}. This audit itself finds several genuinely unresolved gaps -- this is "
		"the smallest retained VPX extraction curated in this project to date (856 files), and its "
		"fidelity does not stretch to cover every documented device -- so the physical machine record at "
		"`machines/partial/bally/creature-from-the-black-lagoon-1992.json` stays `partial` for reasons "
		"that include, but are not limited to, this audit's own findings.",
		"",
		"The matching source is the retained known-working "
		f"`Creature From The Black Lagoon (Bally 1992).vpx` at SHA-256 `{TABLE_SHA256}`. The retained "
		f"`vpxtool` extraction produced the embedded script at SHA-256 `{SCRIPT_SHA256}`; that embedded "
		f"stream is the runtime and causality authority. Exact playfield bounds are `{TABLE_BOUNDS}`, and "
		"every canonical coordinate is x/964 and y/2162 rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW-style script is the runtime address and causality authority; the Bally "
		"operations manual is the physical inventory, quantity, polarity, and wiring authority; pinned "
		"PinMAME owns controller topology; the retained table supplies geometry.",
		"- The retained manual PDF carries a real (Adobe Paper Capture) OCR text layer, but it garbles "
		"every multi-column table used here. Every printed table used in this definition was read from "
		"300 dpi renders and transcribed into `evidence/excerpts/bally.creature-from-the-black-lagoon.1992/`, "
		"indexed by `external:pinmame-review-artifacts/creature/manual-transcription.md`.",
		"- Several switches have no dedicated playfield trigger object because the retained script sets "
		"their public state directly from another mechanism's own event (a jet-bumper Hit, the ramp "
		"motor's own up/down command) rather than from a Hit/Trigger event on a fixed object. Those "
		"addresses are documented projections onto the real table object that carries the underlying "
		"mechanism state.",
		"- Switch 18 has a script handler with no matching object anywhere in the extraction (not even "
		"under a different type), so it is left genuinely unresolved rather than projected onto anything.",
		"- Fliptronic switches 115-118 have unconfirmed fitment (two pages of the same manual disagree) "
		"and are recorded with neither a location nor a not_applicable spatial record, since either would "
		"assert something not yet established.",
		"- Solenoids 20 and 24 are the Sequential G.I. board's own 2-bit decoder address-select lines, not "
		"coils or bulbs, and take a controlled `internal_nonvisual` record. Solenoids 27 and 28 are printed "
		"cabinet-bottom hardware and take `cabinet_or_service`. Solenoid 7 (Knocker) is the standard "
		"WPC cabinet-mounted knocker and also takes `cabinet_or_service`.",
		"- Lamp addresses 91-98 are a real, PinMAME-computed public address group (the true Sequential G.I. "
		"chase-light bulbs, per pinned wpc.c's WPC_CFTBL handling) that the retained table's script never "
		"reads, so none has a coordinate.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with "
		"both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group'].split('.')[-1].title()} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved input addresses: {len(report['unresolved_inputs'])}",
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
		"This record cannot be promoted to `author_ready`. Beyond the unresolved spatial gaps this audit "
		"itself reports (switch 18, switches 115-118, GI address 3, lamp addresses 91-98, and five "
		"unbound flasher solenoids), the record carries a non-empty `conflicts` array "
		"(`conflict.upper-flipper-switches-unconfirmed-fitment`) and "
		"`coverage.dimensions.physical_wiring = \"conflicted\"`. The definition stays `partial` with "
		"`coverage.missing = [\"output_enumeration\", \"spatial_placement\", \"unresolved_conflicts\"]`: "
		"the current solenoid inventory stops at the printed 1-28 table and does not yet enumerate the full "
		"WPC state/Fliptronic public range. A clearer photograph "
		"or parts listing of an unrestored machine's Fliptronic II board settles the upper-flipper "
		"question and a LibPinMAME gameplay-harness trace against a legal cftbl ROM (or a richer retained "
		"VPX recreation) resolves the remaining spatial gaps.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, {EXTRACTION_FILE_COUNT} files.",
		"- Human transcription index of every printed table read from the rendered manual pages at "
		"`external:pinmame-review-artifacts/creature/manual-transcription.md`, plus the underlying VPX "
		"geometry dump at `external:pinmame-review-artifacts/creature/vpx-geometry.txt`.",
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
		raise RuntimeError(f"Stale Creature author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Creature definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Creature seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Creature definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Creature seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Creature spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Creature spatial review drifted from its deterministic curator: {markdown_path}")
	print("Creature definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Creature extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Creature retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
