"""Curate the physical Williams Fish Tales (1992) machine definition.

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
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# The task brief that seeded this curation named tools/seeds/bally/... and
# machines/<state>/bally/...; Fish Tales is a Williams machine (confirmed from
# ft.c CORE_GAMEDEF(ft,l5,...,"Williams",...) and every retained manual page),
# and the pre-existing legacy stub this replaces already lived under
# machines/partial/williams/, so this curator uses williams/ throughout,
# matching every other curated game and the Simpsons Pinball Party /
# Whirlwind precedents for the same class of brief/template mismatch.
DEFINITION_PATH = ROOT / "machines/partial/williams/fish-tales-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/fish-tales-1992.json"
SEED_PATH = ROOT / "tools/seeds/williams/fish-tales-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/fish-tales-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/fish-tales-1992.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.williams.fish-tales.1992"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.fish-tales.1992"
VPX_TABLE_SOURCE = "vpx-table.ft-vpw-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.ft-vpw-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ft-vpw-1-1"

TABLE_SHA256 = "1f82c0237831b50c514e53c8938636f59ee584fc4346c143a3216b9f5d8a1029"
SCRIPT_SHA256 = "b6289a7087f11bd1902d8b059fe663723a6319c6490d1a2fa124d3dd7089e1f5"
MANUAL_SHA256 = "3bcd72631e2276eddf3b77a95ad693a1c16aaa30dea529acaf69cb3a259561c6"
MANUAL_TRANSCRIPTION_SHA256 = "4d45217f9b63775a5d1f969365a6333a8fd2e55417c84bbad15d81407664df3a"

EXTRACTION_RELATIVE_PATH = Path("williams/fish-tales-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/fish-tales-1992/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "946a74ffd92d949fd3d1dfac2c8c8c4207eacc9da3e090174f204fdbb28008c5"
EXTRACTION_FILE_COUNT = 3176
EXTRACTION_TOTAL_BYTES = 1099189711

TABLE_BOUNDS = "left=0 top=0 right=952.9412 bottom=2164.7058"
PLAYFIELD_WIDTH = 952.9412
PLAYFIELD_HEIGHT = 2164.7058

DRIVER_IDS = ("ft_l5", "ft_l5p", "ft_d5", "ft_d6", "ft_l3", "ft_l4", "ft_p2", "ft_p4", "ft_p5")
DRIVER_COMPATIBILITY = {
	"ft_l5": (
		"identical",
		"Williams production L-5 game ROM shipped with the physical machine; the retained known-working "
		'VPW 1.1 table binds this driver directly (Const cGameName = "ft_l5"), so no driver substitution '
		"is needed.",
	),
	"ft_l5p": (
		"identical",
		"Williams L-5 'Text size patch' revision for the same physical machine. The driver's own comment "
		'records the fix: with "Add a ball" enabled, attract mode read "xtra balle" and this ROM corrects '
		'it to "extra ball". No controller-address or playfield change.',
	),
	"ft_d5": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-5 ROM for the same physical machine, correcting DMD "
		"LED matrix ghosting artifacts with no hardware or address change.",
	),
	"ft_d6": (
		"identical",
		"2015 Inkochnito/Williams 'D-6' revision combining the L-5P text-size patch and the D-5 LED Ghost "
		"Fix for the same physical machine.",
	),
	"ft_l3": (
		"identical",
		"Williams L-3 game ROM, an earlier production firmware revision of the same physical machine.",
	),
	"ft_l4": (
		"identical",
		"Williams L-4 game ROM, an earlier production firmware revision of the same physical machine.",
	),
	"ft_p2": (
		"identical",
		"Williams P-2 prototype game ROM for the same physical machine.",
	),
	"ft_p4": (
		"identical",
		"Williams P-4 prototype game ROM for the same physical machine.",
	),
	"ft_p5": (
		"identical",
		"Williams P-5 prototype game ROM with the LED Ghost Fix applied, for the same physical machine.",
	),
}

# --- Printed switch matrix (manual printed 2-43 Switch Locations parts list; printed 3-4 Switch
# Matrix wiring page carries no shading/opto legend at all, unlike several other WPC manuals in this
# project). address -> (switch_no_field, switch_assy_field, description).
SWITCH_LOCATIONS = {
	13: ("-----", "20-9663-1", "Start Button"),
	14: ("-----", "20-6502-A", "Plumb Bob Tilt"),
	15: ("5647-12133-12", "A-10417", "Outhole"),
	16: ("5647-12693-08", "A-11680", "Trough 1"),
	17: ("5647-09957-00", "B-8925", "Trough 2"),
	18: ("5647-09957-00", "B-8925", "Trough 3"),
	21: ("SW-1A-117", "A-15487", "Slam Tilt"),
	22: ("-----", "A-8630", "Coin Door Closed"),
	24: ("-----", "A-8630", "Always Closed"),
	25: ("5647-12693-19", "A-12688", "Left Outlane"),
	26: ("5647-12693-19", "A-12688", "Left Return Lane"),
	27: ("-----", "A-15741", "Left Standup Tgt 1"),
	28: ("-----", "A-15741", "Left Standup Tgt 2"),
	31: ("20-9713-07", "A-15130", "Cast"),
	32: ("5647-12693-21", "A-15055", "Left Boat Exit"),
	33: ("5647-12693-21", "A-15055", "Right Boat Exit"),
	34: ("5647-12133-00", "A-12010", "Spinner"),
	35: ("5647-12693-17", "A-15404", "Reel Entry"),
	36: ("5647-12693-12", "A-14947", "Catapult"),
	37: ("A-14315 (LED) / A-14316 (Trans)", "-----", "Reel 1"),
	38: ("A-14315 (LED) / A-14316 (Trans)", "-----", "Reel 2"),
	41: ("A-14691-5", "-----", "Captive Ball"),
	42: ("5647-12693-18", "A-12687", "Right Boat Entry"),
	43: ("5647-12693-19", "A-12688-1", "Left Boat Entry"),
	44: ("5647-12693-19", "A-12688-1", "Letter (L)IE"),
	45: ("5647-12693-19", "A-12688", "Letter L(I)E"),
	46: ("5647-12693-19", "A-12688", "Letter Ll(E)"),
	47: ("SW-1A-167-1", "A-11658-1", "Ball Popper"),
	48: ("5647-12693-31", "A-15211", "Drop Target"),
	51: ("SW-11A-37", "B-12029-2", "Left Jet Bumper"),
	52: ("SW-11A-37", "B-12029-2", "Center Jet Bumper"),
	53: ("SW-11A-37", "B-12029-2", "Right Jet Bumper"),
	54: ("-----", "A-15741", "Right Standup Tgt 1"),
	55: ("-----", "A-15741", "Right Standup Tgt 2"),
	56: ("5647-12693-19", "A-12688", "Ball Shooter"),
	57: ("SW-1A-114 (Kick) / SW-1A-120-1 (Score)*", "A-8284-2", "Left Slingshot"),
	58: ("SW-1A-114 (Kick) / SW-1A-120-1 (Score)*", "A-8284-2", "Right Slingshot"),
	61: ("-----", "A-15658-6", "Extra Ball"),
	62: ("5647-12693-18", "A-12687", "Top Right Loop"),
	63: ("5647-12133-11", "A-0381-R", "Top Eject Hole"),
	64: ("5647-12693-19", "A-12688", "Top Left Loop"),
	65: ("5647-12693-19", "A-12688", "Right Return"),
	66: ("5647-12693-19", "A-12688", "Right Outlane"),
}
# Printed matrix positions marked "Not Used" on both the Switch Locations parts list (no row printed
# at all for these addresses) and the Switch Matrix legend (printed 3-4). Address 23 ("Ticket Opto")
# has a blank Switch No. and an explicit "Not Used" Switch Assy No. -- a vestigial scaffolding label,
# not a fitted device; ft.c declares #define swTicket 23 but never references it anywhere in the file.
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# The only two addresses this manual documents as opto construction anywhere (Switch Locations'
# "(LED)"/"(Trans)" notation, corroborated by the Fish Reel Unit Assembly page's discrete A-14315/
# A-14316 opto parts). Pinned PinMAME's ftGameData inverted-switch mask does NOT cover them --
# see conflict.reel-opto-switches-not-normalized.
MANUAL_OPTO_SWITCHES = {37, 38}
# ftGameData's inverted-switch mask ({0x00,0x00,0x00,0xc0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}):
# column 4 = 0xc0 = bits 6/7 -> rows 7/8 -> public switches 47 (Ball Popper) and 48 (Drop Target).
# Verified in code: (0xc0 >> 6) & 1 and (0xc0 >> 7) & 1 are the only set bits, and every other column
# is 0x00. Both addresses are documented on this manual as ordinary microswitches with no opto or
# proximity marking -- see conflict.ball-popper-drop-target-normalized-non-opto.
PINMAME_NORMALIZED_SWITCHES = {47, 48}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch", 18: "microswitch",
	21: "tilt", 22: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch",
	27: "microswitch", 28: "microswitch", 31: "button", 32: "microswitch", 33: "microswitch",
	34: "other", 35: "microswitch", 36: "microswitch", 37: "opto", 38: "opto",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch", 45: "microswitch",
	46: "microswitch", 47: "microswitch", 48: "microswitch", 51: "leaf", 52: "leaf", 53: "leaf",
	54: "microswitch", 55: "microswitch", 56: "microswitch", 57: "leaf", 58: "leaf",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch",
	66: "microswitch",
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209", "18-11"), 2: ("White-Red", "J209", "U18-9"),
	3: ("White-Orange", "J209", "U18-5"), 4: ("White-Yellow", "J209", "U18-7"),
	5: ("White-Green", "J209", "U19-11"), 6: ("White-Blue", "J209", "U19-9"),
	7: ("White-Violet", "J209", "U19-5"), 8: ("White-Gray", "J209", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "14", "4"), 2: ("Orange-Red", "J205-2", "13", "5"),
	3: ("Orange-Black", "J205-3", "12", "6"), 4: ("Orange-Yellow", "J205-4", "17", None),
	5: ("Orange-Green", "J205-6", "11", "7"), 6: ("Orange-Blue", "J205-7", "10", "8"),
	7: ("Orange-Violet", "J205-8", "9", "9"), 8: ("Orange-Gray", "J205-9", "8", "11"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", 'Fourth coin chute; the manual prints this label "Forth Coin Chute" (a spelling slip, transcribed verbatim in the excerpt).'),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
# Board-internal Fliptronic II wiring (generic circuit-theory pages 3-15/3-17, PDF 109/111): these
# wires are board properties shared by every Fliptronic II board regardless of which positions a given
# game's harness populates, so they may be cited for the two fitted lower positions even though this
# manual's own game-specific Switch Locations page (2-43/printed) does not itself print wire colors.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906"), 112: ("Blue-Violet", "J905"),
	113: ("Black-Blue", "J906"), 114: ("Blue-Gray", "J905"),
}

# --- Printed solenoid table (manual printed 3-8; identical duplicate at unnumbered PDF page 2).
SOLENOID_LABELS = {
	1: "Ball Shooter", 2: "Catapult", 3: "Ball Popper", 4: "Left Sling", 5: "Right Sling",
	6: "Left Gate", 7: "Knocker", 8: "Backbox Fish", 9: "Outhole", 10: "Ball Release",
	11: "Eject Hole", 12: "Drop Target Up", 13: "Drop Target Down", 14: "Left Jet Bumper",
	15: "Center Jet Bumper", 16: "Right Jet Bumper", 17: "Jackpot Flasher",
	18: "Super Jackpot Flasher", 19: "Instant Multi-ball Flasher", 20: "Light Extra Ball Flasher",
	21: "Rock the Boat Flasher", 22: "Video Mode Flasher", 23: "Hold Bonus Flasher",
	25: "Reel Flasher", 26: "Top Left Flasher", 27: "Casters Club Flasher", 28: "Reel Motor",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {
	24: "Not Used Solenoid Position 24",
	33: "Not Fitted Upper Right Flipper Power",
	34: "Not Fitted Upper Right Flipper Hold",
	35: "Not Fitted Upper Left Flipper Power",
	36: "Not Fitted Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37",
	38: "Unused WPC-Fliptronic Output 38",
	39: "Unused WPC-Fliptronic Output 39",
	40: "Unused WPC-Fliptronic Output 40",
	41: "Unused WPC-Fliptronic Output 41",
	42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43",
	44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
	51: "PinMAME Internal Reel Ball-1 Position Flag",
	52: "PinMAME Internal Reel Ball-2 Position Flag",
	53: "PinMAME Internal Reel Ball-3 Position Flag",
}

# address -> {control_connection, driver_transistor, power_connection?, part_number?, printed_type, wire}
SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", part_number="AE-23-800", printed_type="High Power", wire="Vio-Brn"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", part_number="AL-23-800", printed_type="High Power", wire="Vio-Red"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", part_number="AE-24-900", printed_type="High Power", wire="Vio-Org"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", part_number="AE-27-1200", printed_type="High Power", wire="Vio-Yel"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", part_number="AE-27-1200", printed_type="High Power", wire="Vio-Grn"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", part_number="A-14406", printed_type="High Power", wire="Vio-Blu"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", part_number="AE-23-800", printed_type="High Power", wire="Vio-Blk"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", part_number="AE-23-800", printed_type="High Power", wire="Vio-Gry"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", part_number="AE-27-1200", printed_type="Low Power", wire="Brn-Blk"),
	10: dict(control_connection="J127-3", driver_transistor="Q56", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Red"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Org"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Yel"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", part_number="SM1-26-600", printed_type="Low Power", wire="Brn-Grn"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Blu"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Vio"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", part_number="AE-26-1200", printed_type="Low Power", wire="Brn-Gry"),
	17: dict(control_connection="J126-1", driver_transistor="Q42", printed_type="Flasher", wire="Blk-Brn"),
	18: dict(control_connection="J126-2", driver_transistor="Q40", printed_type="Flasher", wire="Blk-Red"),
	19: dict(control_connection="J126-3, J125-3", driver_transistor="Q38", printed_type="Flasher", wire="Blk-Org"),
	20: dict(control_connection="J126-4, J125-5", driver_transistor="Q36", printed_type="Flasher", wire="Blk-Yel"),
	21: dict(control_connection="J126-5, J125-6", driver_transistor="Q28", printed_type="Flasher", wire="Blu-Grn"),
	22: dict(control_connection="J126-6, J125-7", driver_transistor="Q30", printed_type="Flasher", wire="Blu-Blk"),
	23: dict(control_connection="J126-7, J125-8", driver_transistor="Q34", printed_type="Flasher", wire="Blu-Vio"),
	24: dict(driver_transistor="Q32", printed_type="Flasher", wire="Blu-Gry"),
	25: dict(control_connection="J122-1, J124-1, J124-1", driver_transistor="Q26", printed_type="Flasher", wire="Blu-Brn"),
	26: dict(control_connection="J122-2", driver_transistor="Q24", printed_type="Flasher", wire="Blu-Red"),
	27: dict(control_connection="J122-3, J124-3", driver_transistor="Q22", printed_type="Flasher", wire="Blu-Org"),
	28: dict(control_connection="J122-4", driver_transistor="Q20", part_number="14-7967", printed_type="Low Power", wire="Blu-Yel"),
	45: dict(power_connection="J907-8, 9", control_connection="J902-13", driver_transistor="Q4", part_number="FL-11629", printed_type="Fliptronic power", power_wire="Blu-Yel", control_wire="Blu-Vio"),
	46: dict(power_connection="J907-8, 9", control_connection="J902-11", driver_transistor="Q11", part_number="FL-11629", printed_type="Fliptronic hold", power_wire="Blu-Yel", control_wire="Org-Grn"),
	47: dict(power_connection="J907-6, 7", control_connection="J902-9", driver_transistor="Q3", part_number="FL-11629", printed_type="Fliptronic power", power_wire="Gry-Yel", control_wire="Blu-Gry"),
	48: dict(power_connection="J907-6, 7", control_connection="J902-7", driver_transistor="Q9", part_number="FL-11629", printed_type="Fliptronic hold", power_wire="Gry-Yel", control_wire="Org-Blu"),
}

SOLENOID_ASSEMBLIES = {
	28: "A-14945",
}
# Retained VPW 1.1 script callbacks (SolCallback/SolModCallBack table).
SOLENOID_CALLBACKS = {
	1: "AutoPlunger", 2: "SolCatapult", 3: "SolVUK", 6: "SolGate", 7: "SolKnocker",
	8: "TopperFish", 9: "SolDrain", 10: "SolRelease", 11: "SolFF", 12: "SolDTUp", 13: "SolDTDown",
	17: "Flash17 (f17, f17b)", 18: "Flash18 (f18, f18b)", 19: "Flash19", 20: "Flash20",
	21: "Flash21", 22: "Flash22", 23: "Flash23", 25: "Flash25", 26: "Flash26", 27: "Flash27",
	28: "ReelMotor",
	45: "SolRFlipper (sLRFlipper)", 46: "SolRFlipper (sLRFlipper)",
	47: "SolLFlipper (sLLFlipper)", 48: "SolLFlipper (sLLFlipper)",
}

FLASHER_BULBS = {
	17: "1PL #906", 18: "1PL #906", 19: "1PL #906 / 2 IB #906", 20: "1PL #906 / 2 IB #906",
	21: "1PL #906 / 2 IB #906", 22: "1PL #906 / 2 IB #906", 23: "1PL #906 / 1 IB #906",
	25: "1PL #89 / 1HD #906 / 2 IB #906", 26: "1PL #89 / 1PL #906", 27: "1PL #89 / 1 IB #906",
}

# --- Printed lamp matrix (manual printed 2-42 Lamp Locations parts list; printed 3-2 Lamp Matrix
# wiring). address -> (bulb_part, assembly_part, description).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-15338", "Hold Bonus"), 12: ("24-8768", "A-15338", "Video Mode"),
	13: ("24-8768", "A-15338", "Rock the Boat"), 14: ("24-8768", "A-15338", "Light Ex. Ball"),
	15: ("24-8768", "A-15338", "Instant Multi-Ball"),
	16: ("24-8768", "A-15339", "Letter (L) IE"), 17: ("24-8768", "A-15339", "Letter L(I)E"),
	18: ("24-8768", "A-15339", "Letter Ll(E)"),
	21: ("24-8768", "A-15337", "Stringer 1 Body"), 22: ("24-8768", "A-15337", "Stringer 2 Body"),
	23: ("24-8768", "A-15337", "Stringer 3 Body"), 24: ("24-8768", "A-15337", "Stringer 4 Body"),
	25: ("24-8768", "A-15334", "Left Feed Frenzy"), 26: ("24-8768", "A-15334", "Monster Bonus"),
	27: ("24-8768", "A-15334", "Fish Finder"), 28: ("24-8768", "A-15334", "Jackpot"),
	31: ("24-8768", "A-15337", "Stringer 1 Tail"), 32: ("24-8768", "A-15337", "Stringer 2 Tail"),
	33: ("24-8768", "A-15337", "Stringer 3 Tail"), 34: ("24-8768", "A-15337", "Stringer 4 Tail"),
	35: ("24-6549", "A-11271", "Right Boat Entry"), 36: ("24-6549", "A-11271", "Rt. Boat Feed Frenzy"),
	37: ("24-6549", "A-11271", "Fish Finder"), 38: ("24-6549", "A-11271", "Lt. Boat Feed Frenzy"),
	41: ("24-8768", "A-15337", "Tropical"), 42: ("24-8768", "A-15337", "Freshwater"),
	43: ("24-6549", "A-11754", "Cast Again"), 44: ("24-8768", "A-15337", "Deep Sea"),
	45: ("24-8768", "A-15470", "Left Fish Head"), 46: ("24-8768", "A-15470", "Left Fish Body"),
	47: ("24-8768", "A-15470", "Left Fish Tail"), 48: ("24-8768", "B-12224", "Specials"),
	51: ("24-8768", "A-15337", "Bonus 1X"), 52: ("24-8768", "A-15337", "Bonus 2X"),
	53: ("24-8768", "A-15337", "Auto Cast"), 54: ("24-8768", "A-15337", "Bonus 4X"),
	55: ("24-8768", "A-15470", "Right Fish Head"), 56: ("24-8768", "A-15470", "Right Fish Body"),
	57: ("24-8768", "A-15470", "Right Fish Tail"), 58: ("24-8768", "B-12224", "Light Long Cast"),
	61: ("24-8768", "A-15336", "School Fish 1"), 62: ("24-8768", "A-15336", "School Fish 2"),
	63: ("24-8768", "A-15336", "School Fish 3"), 64: ("24-8768", "A-15336", "School Fish 4"),
	65: ("24-8768", "A-15336", "School Fish 5"), 66: ("24-8768", "A-15336", "School Fish 6"),
	67: ("24-6549", "A-11271", "Super Jackpot"), 68: ("24-8768", "B-12224", "Light Fish Finder"),
	71: ("24-6549", "A-11271", "Casters Club"), 72: ("24-8768", "A-15335", "Doubles Jackpot"),
	73: ("24-8768", "A-15335", "Lock 3"), 74: ("24-8768", "A-15335", "Lock 2"),
	75: ("24-6549", "A-11754", "Lock 1"), 76: ("24-8768", "A-15335", "Rt. Feed Frenzy"),
	77: ("24-8768", "A-15335", "Long Cast"), 78: ("24-6549", "A-11754", "Extra Ball"),
	81: ("24-8768", "A-15415", "Stretch Truth 5X Actual"), 82: ("24-8768", "A-15415", "Stretch Truth 3X Actual"),
	83: ("24-8768", "A-15415", "Stretch Truth 2X Actual"), 84: ("24-8768", "A-15415", "Stretch Truth Actual Size"),
	85: ("24-8768", "A-15415", "Stretch Truth Total Lie"), 86: ("24-6549", "A-8882", "Video Mode"),
	87: (None, "20-9713-07", "Cast"), 88: (None, "20-9663-1", "Start Button"),
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137", "Q98"), 2: ("Yellow-Red", "J137", "Q97"),
	3: ("Yellow-Orange", "J137", "Q96"), 4: ("Yellow-Black", "J137", "Q95"),
	5: ("Yellow-Green", "J137", "Q94"), 6: ("Yellow-Blue", "J137", "Q93"),
	7: ("Yellow-Violet", "J137", "Q92"), 8: ("Yellow-Gray", "J137", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133", "Q90"), 2: ("Red-Black", "J133", "Q89"),
	3: ("Red-Orange", "J133", "Q88"), 4: ("Red-Yellow", "J133", "Q87"),
	5: ("Red-Green", "J133", "Q86"), 6: ("Red-Blue", "J133", "Q85"),
	7: ("Red-Violet", "J133", "Q84"), 8: ("Red-Gray", "J133", "Q83"),
}
# Lamp-matrix page (3-2/PDF 96) wording differs from the Lamp Locations parts list (2-42/PDF 90) on
# these addresses; the parts list is authoritative for the label per this project's standing
# convention, and the disagreement is preserved verbatim in physical.notes rather than silently
# dropped.
LAMP_MATRIX_PAGE_TYPOS = {
	16: "Lie (L)", 17: "Lie (I)", 18: "Lie (E)",
	47: "Left Fish Body (repeats 46's label; the parts list distinguishes 46 Left Fish Body from 47 Left Fish Tail)",
}
# Lamps 16/17/18 ("Letter (L)IE"/"Letter L(I)E"/"Letter Ll(E)") share their assembly A-15339 with the
# manual's own "3-Lamp Board Assembly" (Back Panel Assembly page, printed 2-30/PDF 79 per
# boards-and-assemblies.md) -- a BACKBOX insert-panel board, not a playfield insert, even though the
# retained script models two Light objects per address (base + an "f" suffix pair sitting near the
# playfield's own y=0 rear edge) for visual effect. The genuinely playfield-mounted "LIE" collection
# devices are the boat-mounted rollover switches at 44/45/46, a different physical location entirely.
BACKBOX_LAMP_ADDRESSES = {16, 17, 18}
# Two mirrored playfield inserts (left outlane cluster near l58, right outlane cluster near l68) both
# parse to public address 48 under vpmMapLights' trailing-digit convention (l48 and l48a); this is
# inferred from the retained table's own two genuinely distinct, symmetric Light objects rather than
# an explicit manual "(2)" quantity marker, and is disclosed as such.
LAMP_QUANTITIES = {48: 2}

GI_STRINGS = {
	0: ("Backbox G.I.", "Wht-Brn", "J121-7", "Q18", "#555"),
	1: ("Backbox G.I. / Hood", "Wht-Org", "J121-8, J120-8", "Q10", "#555"),
	2: ("Playfield G.I.", "Wht-Yel", "J120-9", "Q14", "#44"),
	3: ("Backbox G.I.", "Wht-Grn", "J121-10", "Q16", "#555"),
	4: ("Playfield G.I. / Coin Door", "Wht-Vio", "J120-11, J119-1", "Q12", "#44"),
}

# --- Normalized playfield coordinates derived from the retained VPW 1.1 extraction
# (x/952.9412, y/2164.7058; review-artifacts/fish-tales/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.530576, 0.953656)], 16: [(0.846184, 0.875277)], 17: [(0.789529, 0.88998)],
	18: [(0.734042, 0.904441)], 25: [(0.055146, 0.735594)], 26: [(0.126438, 0.735794)],
	27: [(0.158997, 0.594)], 28: [(0.19051, 0.561138)], 32: [(0.251915, 0.283536)],
	33: [(0.683563, 0.29077)], 34: [(0.145631, 0.191227)], 35: [(0.235023, 0.430236)],
	36: [(0.046806, 0.573699)], 41: [(0.4531, 0.262514)], 42: [(0.507351, 0.239177)],
	43: [(0.393517, 0.238325)], 44: [(0.733933, 0.096724)], 45: [(0.628883, 0.091105)],
	46: [(0.523582, 0.097249)], 47: [(0.850533, 0.230701)], 48: [(0.835802, 0.268799)],
	51: [(0.45542, 0.145222)], 52: [(0.642618, 0.192021)], 53: [(0.824782, 0.146017)],
	54: [(0.816145, 0.550312)], 55: [(0.826524, 0.584891)], 56: [(0.937684, 0.885247)],
	57: [(0.225084, 0.732844)], 58: [(0.674183, 0.732644)], 61: [(0.755792, 0.270171)],
	62: [(0.829421, 0.068019)], 63: [(0.822721, 0.033925)], 64: [(0.140219, 0.105573)],
	65: [(0.775286, 0.736108)], 66: [(0.847248, 0.736042)],
}
# Reel-position optos 37/38 have no VPX Trigger/opto object at all -- Controller.Switch(37)/(38) is
# written directly from a 23-branch Select Case on the internal software ReelPosition angle counter
# (script.vbs lines 1610-1637), so both are projected onto the visible Reel drum Primitive that the
# same counter drives (Reel.Rotx = ReelPosition + 46, line 1641).
SWITCH_PROJECTIONS = {
	37: "Projected onto the Reel drum (Primitive Reel, table object center): switches 37/38 have no dedicated sensor object; the retained script derives both directly from the internal ReelPosition angle counter that also drives the visible Reel primitive's own rotation (Reel.Rotx = ReelPosition + 46).",
	38: "Projected onto the Reel drum (Primitive Reel, table object center); see switch 37.",
}
REEL_POSITION = (0.122796, 0.457965)

SOLENOID_POSITIONS = {
	1: [(0.93913, 0.959779)],
	2: [(0.047335, 0.520806)],
	3: [(0.850533, 0.230701)],
	4: [(0.225084, 0.732844)],
	5: [(0.674183, 0.732644)],
	6: [(0.373394, 0.038621)],
	9: [(0.530576, 0.953656)],
	10: [(0.846184, 0.875277)],
	11: [(0.822721, 0.033925)],
	12: [(0.835802, 0.268799)],
	13: [(0.835802, 0.268799)],
	14: [(0.45542, 0.145222)],
	15: [(0.642618, 0.192021)],
	16: [(0.824782, 0.146017)],
	17: [(0.171506, 0.255911)],
	18: [(0.452444, 0.497925)],
	19: [(0.452096, 0.296879)],
	20: [(0.45216, 0.319219)],
	21: [(0.451968, 0.338693)],
	22: [(0.452031, 0.363252)],
	23: [(0.452015, 0.387832)],
	25: [(0.095483, 0.370329)],
	26: [(0.186274, 0.191296)],
	27: [(0.832626, 0.286716)],
	28: [(0.122796, 0.457965)],
	45: [(0.617562, 0.848152)],
	46: [(0.617562, 0.848152)],
	47: [(0.284645, 0.848152)],
	48: [(0.284645, 0.848152)],
}

LAMP_POSITIONS = {
	11: [(0.452966, 0.394089)], 12: [(0.452621, 0.368681)], 13: [(0.452966, 0.342475)],
	14: [(0.452966, 0.3247)], 15: [(0.452966, 0.302065)],
	21: [(0.322877, 0.655764)], 22: [(0.407279, 0.665336)], 23: [(0.494163, 0.671949)],
	24: [(0.582732, 0.656495)], 25: [(0.232254, 0.42997)], 26: [(0.213619, 0.36933)],
	27: [(0.192928, 0.315827)], 28: [(0.175074, 0.260317)],
	31: [(0.322123, 0.701165)], 32: [(0.409691, 0.712119)], 33: [(0.49515, 0.710905)],
	34: [(0.582997, 0.700104)], 35: [(0.557933, 0.392536)], 36: [(0.568197, 0.311814)],
	37: [(0.345296, 0.392404)], 38: [(0.333838, 0.311315)],
	41: [(0.363663, 0.754587)], 42: [(0.452029, 0.752482)], 43: [(0.453244, 0.869468)],
	44: [(0.536248, 0.751671)], 45: [(0.278946, 0.56718)], 46: [(0.239348, 0.590195)],
	47: [(0.223117, 0.620065)], 48: [(0.056722, 0.6873), (0.849622, 0.68605)],
	51: [(0.397871, 0.812632)], 52: [(0.452222, 0.830748)], 53: [(0.454686, 0.790977)],
	54: [(0.509438, 0.813104)], 55: [(0.765429, 0.594749)], 56: [(0.753707, 0.564061)],
	57: [(0.735462, 0.535111)], 58: [(0.125977, 0.687305)],
	61: [(0.297412, 0.516205)], 62: [(0.359386, 0.526383)], 63: [(0.422064, 0.537491)],
	64: [(0.481757, 0.538312)], 65: [(0.545544, 0.528807)], 66: [(0.608007, 0.518028)],
	67: [(0.453479, 0.495369)], 68: [(0.77777, 0.686549)],
	71: [(0.82469, 0.285227)], 72: [(0.755967, 0.393419)], 73: [(0.787752, 0.349092)],
	74: [(0.805626, 0.323395)], 75: [(0.823674, 0.297369)], 76: [(0.844113, 0.428352)],
	77: [(0.881551, 0.378089)], 78: [(0.741201, 0.306591)],
	81: [(0.105153, 0.14746)], 82: [(0.113014, 0.163226)], 83: [(0.119128, 0.178607)],
	84: [(0.124369, 0.192066)], 85: [(0.125242, 0.205909)], 86: [(0.831904, 0.014028)],
}

GI_POSITIONS = {
	2: [
		(0.259554, 0.08758), (0.220229, 0.122071), (0.360719, 0.119155), (0.295473, 0.186403),
		(0.39497, 0.187498), (0.099066, 0.22816), (0.141046, 0.384156), (0.269285, 0.300742),
		(0.279697, 0.366889), (0.922911, 0.057397), (0.453533, 0.257703), (0.788716, 0.241982),
		(0.638844, 0.18958), (0.454677, 0.144719), (0.824354, 0.140727), (0.389828, 0.300457),
		(0.517246, 0.301654), (0.476096, 0.100239), (0.566058, 0.089654), (0.685869, 0.089289),
		(0.77666, 0.100239),
	],
	4: [
		(0.18229, 0.70139), (0.212438, 0.758575), (0.150001, 0.800366), (0.216767, 0.820603),
		(0.724755, 0.704462), (0.694608, 0.760651), (0.757869, 0.802869), (0.689982, 0.823355),
		(0.148483, 0.567598), (0.881389, 0.532594), (0.873857, 0.580573),
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
		raise RuntimeError(f"Fish Tales retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Fish Tales extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Fish Tales retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Fish Tales retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Fish Tales retained extraction identity mismatch: "
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
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the ft_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/ft.c ftGameData GEN_WPCFLIPTRON with wpc_dispDMD, the inverted-switch "
				"mask {0x00,0x00,0x00,0xc0,0x00,...} (column 4 bits 6/7 -> public 47/48 only), "
				"FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR), hw.custSol=3 (sFakeReel1..3, PinMAME's own "
				"internal reel ball-position bookkeeping for its built-in ball simulator, never referenced by "
				"the retained known-working VPX script), swStart/swTilt/swSlamTilt/swCoinDoor/swCast dedicated-"
				"switch defines with wpc.comSw.shooter=swCast, ft_handleMech's drop-target and reel-motor state "
				"handling, and init_ft's wpc_set_fastflip_addr(0x7b); the file's own header comment discloses "
				'"I don\'t have access to this game, I guessed most of it from a Playfield picture and the '
				'rulesheet!" and "I\'m guessing on the reel optos"; src/wpc/core.h CORE_FIRSTCUSTSOL=51/'
				"CORE_CUSTSOLNO/CORE_FIRSTUFLIPSOL=33/CORE_FIRSTLFLIPSOL=45/FLIP_UR=0x4/FLIP_L=(FLIP_LL|FLIP_LR); "
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
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules, including the no-LPDC 37-44 unused range and the Fliptronic flipper block",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.fish-tales.1992/archive-arcademanual_Fish_Tales_OPS/Fish_Tales_OPS.pdf",
			"original_filename": "Fish_Tales_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"149-page OCR'd (Adobe Acrobat Paper Capture) scan of the Williams Fish Tales operations manual "
				"(16-50005-101, August 1992). Printed pages 2-40 through 2-43 carry the playfield-parts, lamp-"
				"locations, and switch-locations parts lists; printed pages 3-2, 3-4, 3-6, 3-8, and 3-9 carry the "
				"lamp matrix, switch matrix, dedicated-switch, solenoid table, and solenoid wiring pages; printed "
				"pages 2-12 through 2-31 and 2-34/2-35 carry mechanism assembly pages that fix device construction "
				"(Flipper Opto Board, Fish Reel Unit Assembly, Boat Unit Assembly, Fliptronic II Board and its "
				"generic 3-15 to 3-19 circuit-theory pages). Internet Archive item id inferred only from the local "
				"folder-naming convention (archive-arcademanual_Fish_Tales_OPS); no archive credit or uploader "
				"stamp appears anywhere in the 149 rendered pages, so it is not independently confirmed."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.fish-tales.switch-locations",
					"locator": "PDF page 91, printed page 2-43, Switch Locations parts list",
					"path": "evidence/excerpts/williams.fish-tales.1992/switch-locations.md",
					"sha256": "ab9f84d395990f1001ae0513b48e95febd663925becabefa27a8b15386026c43",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.switch-matrix",
					"locator": "PDF page 98, printed page 3-4, Switch Matrix table",
					"path": "evidence/excerpts/williams.fish-tales.1992/switch-matrix.md",
					"sha256": "5e23f9bf28a1992938960057257a3db77ffcb4726381fa6305e23cd6135ff74e",
					"image": "evidence/excerpts/williams.fish-tales.1992/switch-matrix.webp",
					"image_sha256": "38cc01df3dc66649925727a5376d363652174f8e6493cbe7ca71812b633ad296",
					"image_derivation": "Fish_Tales_OPS.pdf page 98, rendered at 300 dpi with pdftoppm, cropped to the SWITCH MATRIX block, grayscale WebP, documenting that the page carries no shading/opto legend at all",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.lamp-locations",
					"locator": "PDF page 90, printed page 2-42, Lamp Locations parts list",
					"path": "evidence/excerpts/williams.fish-tales.1992/lamp-locations.md",
					"sha256": "b84fdff8105cd94992f56073849e4eca5a4ebd484839d854b612e729181f12a0",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.lamp-matrix",
					"locator": "PDF page 96, printed page 3-2, Lamp Matrix wiring table",
					"path": "evidence/excerpts/williams.fish-tales.1992/lamp-matrix.md",
					"sha256": "0310672b30d51602bd625b8e10db9be8c1f2fe0c65cc4055c35da1a3f9e5505f",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.solenoid-flasher-locations",
					"locator": "PDF pages 88-89, printed pages 2-40/2-41, Playfield Parts (flipper assembly line items)",
					"path": "evidence/excerpts/williams.fish-tales.1992/solenoid-flasher-locations.md",
					"sha256": "babc0267301790497b89a7151e406be05331b9248c39ad95456fc0457e705584",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.solenoid-flasher-wiring",
					"locator": "PDF pages 102-103 and 128, printed pages 3-8/3-9 and 3-34, Solenoid Table, General Illumination, Flipper Circuits, Solenoid Wiring, and Fliptronic II interboard wiring",
					"path": "evidence/excerpts/williams.fish-tales.1992/solenoid-flasher-wiring.md",
					"sha256": "c47774f19c004ad902766f79ed3d64b659a1cae181a5c7213b5bc6c181a31671",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.general-illumination",
					"locator": "PDF page 102, printed page 3-8, General Illumination table (same page as the Solenoid Table)",
					"path": "evidence/excerpts/williams.fish-tales.1992/general-illumination.md",
					"sha256": "9fb5812444a9c496e8b130b546f68203704f59ed340df3c674e9f474ca9763c3",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.fish-tales.boards-and-assemblies",
					"locator": "PDF pages 60-79, 82-84, 109-113, printed pages 2-12 through 2-31, 2-34/2-35, and 3-15 through 3-19, mechanism and Fliptronic II board assembly pages",
					"path": "evidence/excerpts/williams.fish-tales.1992/boards-and-assemblies.md",
					"sha256": "6add7f33840a6da574ab8b378974fa21564b527cfa64b44d3b34780c4e1f5343",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/fish-tales/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition. This "
				"manual's pdftotext OCR text layer exists but is not authoritative for any mapping; every table "
				"used here was read from a rendered page, not OCR text."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/fish-tales-1992/source/Fish%20Tales%20%28Williams%201992%29%20VPW%201.1.vpx",
			"original_filename": "Fish Tales (Williams 1992) VPW 1.1.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW 1.1 recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. "
				"Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/fish-tales-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (251,489 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "ft_l5" (the production parent driver, no substitution needed), Const '
				"UseSolenoids = 2 (fast flips), Const UseLamps = 1 (vpmMapLights AllLamps bulk binding, no "
				"table-authored UpdateLamps routine), Const UseGI = 1 with UpdateGI2 driving GI addresses 2 "
				"(TopGI, 21 playfield bulbs) and 4 (BottomGI, 11 playfield bulbs) only, the SolCallback/"
				"SolModCallBack table for solenoids 1-3, 6-13, 17-23, 25-28 and the lower-flipper pair, the "
				"self-contained ReelPosition software angle-counter reel simulation (independent of PinMAME's "
				"own fake-solenoid reel bookkeeping) deriving switches 37/38 directly, the DropTarget class "
				"instance DT48 and its DTAnimate state machine, and the unconditional NoUpperLeftFlipper/"
				"NoUpperRightFlipper calls at load with zero references anywhere to switches 111-118 or "
				"solenoids 33-36."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/fish-tales-1992/extracted-vpxtool.manifest.json",
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
		"board": "WPC CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver at {return_connection}-{return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, cdi_j1, cdi_j3 = DEDICATED_SWITCH_WIRING[address]
		wiring: dict[str, Any] = {"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": f"Coin Door Interface J1-{cdi_j1}"}
		if cdi_j3:
			wiring["return_component"] += f", J3-{cdi_j3}"
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
				wiring=wiring,
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			unused = address in UNUSED_MATRIX_ADDRESSES
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			physical: dict[str, Any] = {}
			label = "Not Used Matrix Position " + str(address)
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if not unused:
				switch_no, assy_no, description = SWITCH_LOCATIONS[address]
				label = description
				if switch_no and switch_no != "-----":
					physical["part_number"] = switch_no
				if assy_no and assy_no not in ("-----", "Not Used"):
					physical["assembly_part_number"] = assy_no
				if address in SWITCH_TYPES:
					physical["switch_type"] = SWITCH_TYPES[address]
				notes += f' Manual description "{description}".'
			else:
				notes += (
					" Both the Switch Locations parts list (no row printed) and the Switch Matrix legend "
					'(printed "Not Used") agree this position is unfitted.'
				)
				if address == 23:
					notes += (
						' ft.c declares #define swTicket 23 but never references it anywhere in the driver '
						'body; the manual prints "Ticket Opto" as the description with a blank Switch No. and '
						'an explicit "Not Used" Switch Assy No., confirming a vestigial scaffolding label '
						"rather than a fitted device."
					)
			if address in MANUAL_OPTO_SWITCHES:
				notes += (
					" Documented opto construction (LED part A-14315 / photo-transistor part A-14316, "
					"corroborated by the Fish Reel Unit Assembly page which lists the identical two part "
					"numbers as the reel's top and bottom opto brackets). Pinned PinMAME's ftGameData "
					"inverted-switch mask does not cover this column, so the public switch state is not "
					"emulator-normalized despite the confirmed opto construction; see "
					"conflict.reel-opto-switches-not-normalized."
				)
			elif address in PINMAME_NORMALIZED_SWITCHES:
				notes += (
					" Pinned PinMAME's ftGameData inverted-switch mask (column 4 = 0xc0, bits 6/7) normalizes "
					"this address, but the manual documents it as an ordinary microswitch with no opto or "
					"proximity marking; see conflict.ball-popper-drop-target-normalized-non-opto."
				)
			if address == 24:
				notes += " Physical part A-8630 (the same generic part also used for Coin Door Closed, address 22) is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 31:
				notes += (
					" This is the cabinet-front 'Fishing Reel handle' pushbutton (A-15130 assembly), installed "
					"in the position a spring plunger rod normally occupies (assembly instructions step 9, "
					"printed 1-3): Fish Tales has no manual plunger, the ball is auto-launched by solenoid 1 "
					"(Ball Shooter), and this button is used for Video Mode control. ftGameData's own "
					"wpc.comSw.shooter field is set to swCast (this address), so PinMAME's platform-level "
					"'shooter' common-switch role is assigned to this cabinet pushbutton rather than to the "
					"shooter-lane ball sensor at address 56."
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
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				if address not in MANUAL_OPTO_SWITCHES:
					extra["normally_closed"] = address in PINMAME_NORMALIZED_SWITCHES
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22, 31}:
					role = {
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
						31: "cabinet.shooter",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {13, 31} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				elif address in SWITCH_PROJECTIONS:
					extra["spatial"] = located(identifier, "sensor", [REEL_POSITION], VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE)
				else:
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf"),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf"),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto"),
		115: ("Not Fitted Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None),
		116: ("Not Fitted Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None),
		117: ("Not Fitted Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None),
		118: ("Not Fitted Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type) in flipper_inputs.items():
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
		}
		if availability == "unused":
			notes += (
				" Four independent, game-specific manual sources agree Fish Tales has exactly two flippers, "
				"both lower, with no upper-flipper hardware at all: the Switch Locations parts list prints no "
				"F5-F8 row whatsoever (not even a 'NOT USED' placeholder, unlike some other WPC-Fliptronic "
				"manuals in this project); the Fliptronic II Flipper Assembly parts list names only two "
				"assemblies (A-15205-R-2, A-15205-L-2), both lower positions; the full Playfield Parts list "
				"names only two flipper-assembly line items; and the Solenoid Table prints only two flipper-"
				"circuit rows (Lower Right, Lower Left), again with no placeholder row for an upper pair. The "
				"retained known-working VPX script independently confirms this: it calls both "
				"NoUpperLeftFlipper and NoUpperRightFlipper unconditionally at load and references no switch "
				"address in 111-118 anywhere. Pinned PinMAME's ftGameData nonetheless declares "
				"FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR), naming an upper-RIGHT flipper as real "
				'driver-modeled hardware; the driver file\'s own header comment discloses its author "guessed '
				'most of it from a Playfield picture and the rulesheet" without access to the real machine. '
				"Given the overwhelming, mutually-corroborating game-specific evidence against a single, "
				"self-disclaimed driver field, this position is recorded as not fitted. The generic "
				"Fliptronic II circuit-theory pages (3-15 to 3-19) do print wiring for all four possible "
				"flipper positions, but the manual's own text there documents this as board-level capability "
				"present regardless of which positions a given game's harness populates, not evidence of "
				"actual fitment."
			)
			physical["location"] = "not installed"
		elif switch_type == "opto":
			notes += (
				" Board A-15894 (Flipper Opto Board) carries exactly two opto interrupters and is the "
				"cabinet-front flipper-button opto board. This generation's WPC_FLIPPERS register read "
				"unconditionally complements the flipper switch column regardless of hardware generation, "
				"so the public switch state is already normalized."
			)
		physical["notes"] = notes
		extra["physical"] = physical
		if availability != "unused":
			wire, connection = FLIPPER_SWITCH_WIRING[address]
			extra["wiring"] = {"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection}
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
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
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
						"this manual does not include the per-country switch-combination chart, so no specific "
						"ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	import re

	slug = re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed"
	return f"device.{slug}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 54):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING.get(address, {})
			kind = "flasher" if 17 <= address <= 27 else "motor" if address == 28 else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid table entry {address:02d} ({printed_type})." if wiring_data else f"Printed solenoid table entry {address:02d}."
			if kind == "flasher" and address in FLASHER_BULBS:
				physical["quantity"] = FLASHER_BULBS[address].count("#") if False else None
				notes += f" Printed flashlamp complement: {FLASHER_BULBS[address]}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if address == 24:
				notes += (
					" The printed table shows a populated driver transistor (Q32) with wire color Blu-Gry "
					"assigned but a blank Connections cell ('—'), so no flasher or other device is fitted here."
				)
			if address in {33, 34, 35, 36}:
				side = "Right" if address in {33, 34} else "Left"
				stage = "Power" if address in {33, 35} else "Hold"
				notes += (
					f" Fliptronic upper-{side.lower()} flipper {stage.lower()} circuit. Four independent "
					"game-specific manual sources (Switch Locations, Fliptronic II Flipper Assembly parts "
					"list, full Playfield Parts list, and this Solenoid Table itself, which prints only two "
					"flipper-circuit rows with no placeholder for an upper pair) plus the retained known-"
					"working script (no SolCallback for 33-36, explicit NoUpperLeftFlipper/NoUpperRightFlipper "
					"calls) agree Fish Tales has no upper flippers; see switch.generic-115's notes for the full "
					"citation trail. Pinned PinMAME's ftGameData nonetheless declares FLIP_SOL(FLIP_UR), naming "
					"public 33/34 as a real driver-modeled coil; this position is recorded as not fitted."
				)
			if address in {45, 46, 47, 48}:
				notes += " Fed from the retained script's SolRFlipper/SolLFlipper handlers (named constants sLRFlipper/sLLFlipper, conventionally the lower-flipper pair)."
			physical["notes"] = notes
			if physical.get("quantity") is None:
				physical.pop("quantity", None)

			wiring: dict[str, Any] = {}
			if "driver_transistor" in wiring_data:
				wiring["board"] = "Fliptronic II controller board (J901-J907)" if address in {45, 46, 47, 48} else "WPC power driver board"
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
				if "control_connection" in wiring_data:
					wiring["control_connection"] = wiring_data["control_connection"]
				if "wire" in wiring_data:
					wiring["control_wire"] = wiring_data["wire"]
				if "control_wire" in wiring_data:
					wiring["control_wire"] = wiring_data["control_wire"]
				if "power_connection" in wiring_data:
					wiring["power_connection"] = wiring_data["power_connection"]
				if "power_wire" in wiring_data:
					wiring["power_wire"] = wiring_data["power_wire"]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if wiring_data:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
			if wiring:
				extra["wiring"] = wiring
			if not fitted:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			elif address == 7:
				availability = "used"
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 8:
				availability = "used"
				extra["roles"] = ["cabinet.backbox"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Fish Tales playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Fish Tales playfield device.",
			31: "PinMAME's synthetic game-on state. Fish Tales sets wpc_set_fastflip_addr(0x7b), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			37: "This WPC-Fliptronic generation has no integrated LPDC board (unlike WPC-95), so pinned PinMAME's core_getSol dispatch serves the 37-44 range only for GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11; this address is simply unused space here.",
			38: "Unused WPC-Fliptronic address space; see 37.",
			39: "Unused WPC-Fliptronic address space; see 37.",
			40: "Unused WPC-Fliptronic address space; see 37.",
			41: "Unused WPC-Fliptronic address space; see 37.",
			42: "Unused WPC-Fliptronic address space; see 37.",
			43: "Unused WPC-Fliptronic address space; see 37.",
			44: "Unused WPC-Fliptronic address space; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-Fliptronic hardware output. Fish Tales' real ball shooter is public solenoid 1.",
			50: "Reserved PinMAME output position before the first custom-output boundary (CORE_FIRSTCUSTSOL=51).",
			51: (
				"PinMAME's own internal reel ball-1 position bookkeeping for its built-in ball simulator "
				"(sFakeReel1 = CORE_CUSTSOLNO(1)). ft.c's own inline comment labels this address '(33)', which "
				"is stale under the pinned revision: CORE_FIRSTCUSTSOL=51, so CORE_CUSTSOLNO(1) resolves to "
				"public 51, verified directly from core.h. The retained known-working VPX script never "
				"references this address anywhere -- it implements its own independent, self-contained "
				"reel-position physics (an internal ReelPosition angle counter) with no dependency on this "
				"channel. There is no real driver-board transistor or coil behind this address."
			),
			52: (
				"PinMAME's own internal reel ball-2 position bookkeeping (sFakeReel2 = CORE_CUSTSOLNO(2), "
				"public 52; ft.c's own stale inline comment reads '(34)'); see 51 for the full explanation."
			),
			53: (
				"PinMAME's own internal reel ball-3 position bookkeeping (sFakeReel3 = CORE_CUSTSOLNO(3), "
				"public 53; ft.c's own stale inline comment reads '(35)'); see 51 for the full explanation."
			),
		}[address]
		roles = ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
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
			bulb, assembly, label = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_MATRIX_PAGE_TYPOS:
				notes += (
					f' The lamp-matrix page (3-2) labels this insert "{LAMP_MATRIX_PAGE_TYPOS[address]}"; the '
					"lamp-locations parts list (2-42) label used here is taken as authoritative per this "
					"project's standing convention."
				)
			if address in BACKBOX_LAMP_ADDRESSES:
				notes += (
					" This lamp is mounted on the A-15339 '3-Lamp Board Assembly', a BACKBOX insert-panel "
					"board on the Back Panel Assembly (printed 2-30), not a playfield insert -- confirmed "
					"independently of the same-numbered playfield rollover switches at 44/45/46, which use the "
					"same LIE-letter theme but sit on the boat-unit assembly instead. The retained script "
					"models two co-located Light objects for this address purely for visual effect near the "
					"playfield's own rear edge; neither is treated as a playfield coordinate."
				)
			if address == 48:
				notes += (
					" The retained table models two genuinely distinct, mirrored Light objects for this "
					"address (left and right outlane clusters, alongside the single-address lamps 58 and 68 "
					"respectively) that both parse to public address 48 under vpmMapLights' trailing-digit "
					"convention. The manual's Lamp Locations page prints no explicit '(2)' quantity marker for "
					"this address; the two-placement quantity here is inferred from the retained table's own "
					"geometry rather than an explicit manual count, and is disclosed as such."
				)
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated Cast/Start Button assembly, sharing its assembly part number with the matching switch."
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
			availability = "used"
			if address in BACKBOX_LAMP_ADDRESSES or address in {87, 88}:
				extra["roles"] = ["cabinet.insert-panel" if address in BACKBOX_LAMP_ADDRESSES else ("cabinet.shooter" if address == 87 else "cabinet.start")]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
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
	for address, (label, wire, connections, transistor, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}, wire {wire}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC power driver board",
				"control_connection": connections,
				"driver_transistor": transistor,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter "
				"coordinate come from the retained table's own GI emitter collection for this string "
				"(UpdateGI2 in the retained script): GI address 2 drives collection TopGI (21 members) and GI "
				"address 4 drives collection BottomGI (11 members), matching this manual's own 'Playfield "
				"G.I.' classification for printed strings 03 and 05 exactly."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox illumination behind the translite/insert panel, matching this manual's own "
				"'Backbox G.I.' classification. The retained script's UpdateGI2 handles only GI addresses 2 "
				"and 4 with real playfield bulb collections; addresses 0, 1, and 3 have no playfield "
				"representation at all in the retained table, consistent with all three being backbox "
				"circuits rather than an unmodeled gap."
			)
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
			"Ball trough and outhole",
			"kicker",
			[output_id("Outhole"), output_id("Ball Release")],
			["switch.matrix-15", "switch.matrix-16", "switch.matrix-17", "switch.matrix-18"],
			"A drained ball lands on the outhole switch (15) and solenoid 9 kicks it into the three-"
			"position trough (16/17/18). Solenoid 10 (Ball Release) releases the ball nearest the exit "
			"onto the shooter lane. The retained script's sw16_Hit/sw17_Hit/sw18_Hit handlers call a "
			"shared UpdateTrough routine to track ball count.",
			[
				("outhole", "Outhole", ["switch.matrix-15"], "Drained-ball catch position."),
				("trough-1", "Trough 1", ["switch.matrix-16"], "Trough position nearest the release exit."),
				("trough-2", "Trough 2", ["switch.matrix-17"], "Middle trough position."),
				("trough-3", "Trough 3", ["switch.matrix-18"], "Trough position nearest the outhole."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-10417",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Ball Shooter")],
			["switch.matrix-56"],
			"Fish Tales has no manual plunger: the cabinet-front reel-handle button (switch 31, Cast) "
			"occupies the position a spring plunger rod normally uses, and the ball resting on shooter-"
			"lane switch 56 is launched by auto-plunger coil 1 (SolCallback(1)=\"AutoPlunger\") under ROM "
			"control (Const UseSolenoids = 2, fast flips).",
			[("shooter", "Ball in shooter lane", ["switch.matrix-56"], "Shooter-lane switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14945",
		),
		mechanism(
			"mechanism.reel",
			"Motorized fishing reel and multiball lock",
			"reel",
			[output_id("Reel Motor")],
			["switch.matrix-35", "switch.matrix-37", "switch.matrix-38"],
			"The headline mechanism: a 50V gear motor (part 14-7967, solenoid 28) drives a belt/pulley "
			"that rotates a physical fishing-reel drum (A-14945 Fish Reel Unit Assembly). A ball enters "
			"the reel via reel-entry switch 35 after leaving the Habit Trail from the Caster's Club VUK. "
			"Two discrete opto pairs (A-14315 LED / A-14316 photo-transistor, one top bracket and one "
			"bottom bracket) report rotational position back to the CPU as switches 37 (Reel 1) and 38 "
			"(Reel 2). Pinned PinMAME's own ft_handleMech models this with a 0-149 position counter and "
			"three symmetric ball-lock zones (Ball1Up=0, Ball2Up=50, Ball3Up=100, each mirrored at "
			"+75/+75/-75 for the corresponding 'Down' release zone, ERROR_RANGE=10) plus three internal "
			"'fake' solenoids (public 51/52/53) that only PinMAME's own built-in ball simulator consumes. "
			"The retained known-working VPX script implements its own independent, richer 0-360 degree "
			"ReelPosition angle counter with six named zones (10-30 Lock1, 70-90 Ball3Out, 130-150 Lock3, "
			"190-210 Ball1Out, 250-270 Lock2, 310-330 Ball2Out), derives switches 37/38 directly from that "
			"counter, drives the visible Reel primitive's own rotation from it (Reel.Rotx = ReelPosition + "
			"46), and models three ball-catch positions as Kicker objects that release balls into the "
			"Catapult mechanism as the reel rotates -- this is the machine's multiball lock: up to three "
			"balls ride the reel simultaneously before dropping one at a time into the catapult.",
			[
				("entry", "Reel entry", ["switch.matrix-35"], "Ball enters the reel from the Habit Trail."),
				("opto-1", "Reel opto 1", ["switch.matrix-37"], "Closed during every ball lock/release position."),
				("opto-2", "Reel opto 2", ["switch.matrix-38"], "Closed only at the Ball 1 Up position."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14945",
		),
		mechanism(
			"mechanism.catapult",
			"Ball catapult",
			"kicker",
			[output_id("Catapult")],
			["switch.matrix-36"],
			"A ball dropped from the reel lands in the catapult cup (switch 36) and solenoid 2 (part "
			"AL-23-800) launches it back onto the playfield. The retained script animates a separate "
			"rotating-arm visual (CatPrim) alongside the ball-catch Kicker.",
			[("caught", "Ball in catapult", ["switch.matrix-36"], "Catapult cup switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14947",
		),
		mechanism(
			"mechanism.casters-club",
			"Caster's Club ball popper (multiball lock entry)",
			"kicker",
			[output_id("Ball Popper")],
			["switch.matrix-47"],
			"A ball captured on switch 47 (Ball Popper) is kicked by solenoid 3 (SolVUK) up the Habit "
			"Trail toward the reel-entry switch (35), which is this machine's entry point into the reel "
			"multiball-lock feature.",
			[("caught", "Ball in Caster's Club", ["switch.matrix-47"], "Ball Popper switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-11658-1",
		),
		mechanism(
			"mechanism.fish-finder",
			"Fish Finder saucer",
			"kicker",
			[output_id("Eject Hole")],
			["switch.matrix-63"],
			"A ball captured on switch 63 (Top Eject Hole) is kicked back to the playfield by solenoid 11 "
			"(SolFF, Eject Hole).",
			[("caught", "Ball in Fish Finder saucer", ["switch.matrix-63"], "Top Eject Hole switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-0381-R",
		),
		mechanism(
			"mechanism.gate",
			"Left gate",
			"gate",
			[output_id("Left Gate")],
			[],
			"Solenoid 6 (SolGate, part A-14406) opens and closes a one-way gate; the retained script "
			"toggles the Gate object's .Open/.Collidable state and drives a companion visual rotation. No "
			"printed switch is dedicated to this gate.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14406",
		),
		mechanism(
			"mechanism.drop-target-ramp",
			"1-bank drop target / ramp",
			"drop_target_bank",
			[output_id("Drop Target Up"), output_id("Drop Target Down")],
			["switch.matrix-48"],
			"The A-15211 1-Bank Drop Target Assembly is driven by two separate coils: solenoid 12 (Up) "
			"raises it and solenoid 13 (Down) knocks it down; switch 48 senses the dropped state. The "
			"retained script models a single DropTarget class instance (DT48) whose DTAnimate state "
			"machine drives a visible Primitive through hit-bend, drop, hold-down, raise-hold, and reset "
			"phases; the public switch state is a side effect of that animation reaching its fully-dropped "
			"or fully-reset threshold, not a direct collision-to-switch binding.",
			[
				("up", "Target up / ramp raised", [], "Rest position."),
				("down", "Target down / ramp lowered", ["switch.matrix-48"], "Dropped/lowered position."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15211",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Center Jet Bumper"), output_id("Right Jet Bumper")],
			["switch.matrix-51", "switch.matrix-52", "switch.matrix-53"],
			"Three SW-11A-37 jet bumpers, wired to solenoids 14/15/16 and switches 51/52/53 respectively.",
			[
				("left", "Left jet bumper", ["switch.matrix-51"], "Left bumper of the nest."),
				("center", "Center jet bumper", ["switch.matrix-52"], "Center bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-53"], "Right bumper of the nest."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="SW-11A-37",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Sling"), output_id("Right Sling")],
			["switch.matrix-57", "switch.matrix-58"],
			"Each slingshot assembly (A-8284-2) carries a kick switch (SW-1A-114) and a separate scored "
			"switch (SW-1A-120-1, with a diode attached, per the manual's footnote) at addresses 57/58. "
			"Solenoids 4/5 fire the kickers.",
			[
				("left", "Left slingshot", ["switch.matrix-57"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-58"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-8284-2",
		),
		mechanism(
			"mechanism.knocker",
			"Cabinet knocker",
			"other",
			[output_id("Knocker")],
			[],
			"Standard WPC cabinet knocker, solenoid 7, raps to signal a Special or replay award. No "
			"printed switch is dedicated to it.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.backbox-fish",
			"Backbox fish toy",
			"toy",
			[output_id("Backbox Fish")],
			[],
			"Solenoid 8 (script name TopperFish) actuates a bell-armature toy on the large backglass "
			"'Fish & Plastic Insert' (A-15713 panel with A-15304 Coil Unit Assembly and A-6306-2 Bell "
			"Armature Assembly). No printed switch is dedicated to it; this is a backbox device with no "
			"playfield coordinate.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15304",
		),
		mechanism(
			"mechanism.boat",
			"Boat unit (rollover lanes and captive-ball target)",
			"other",
			[],
			["switch.matrix-32", "switch.matrix-33", "switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
			"The A-15109 Boat Unit Assembly carries two rollover switches (A-12688-1, matching printed "
			"'Rollover Switch Assembly') for the port/starboard boat-exit lanes (32/33) and boat-entry "
			"lanes (42/43), plus the captive-ball standup target (A-14691-5, switch 41) and two lamp "
			"boards (A-15338 five-lamp PCB for 11-15, A-11271 four-bulb array for 35-38). No page read "
			"describes a motor, tilt actuator, or moving axis for the boat prop itself -- unlike the reel, "
			"which is explicitly motor-driven, the assembly page shows only switches, lamps, and flashers. "
			"On the evidence gathered here the boat is a stationary playfield structure the ball rolls "
			"through/over, not a mechanically animated rocking mechanism; 'Rock the Boat' (lamp 13, "
			"flasher 21) is a scoring-mode name on the rules pages, not evidence of physical motion, and "
			"this should be re-checked if stronger contrary evidence (a motor line item, a schematic "
			"showing a drive coil) surfaces later.",
			[
				("boat-exit-left", "Left boat exit", ["switch.matrix-32"], "Port boat-exit rollover."),
				("boat-exit-right", "Right boat exit", ["switch.matrix-33"], "Starboard boat-exit rollover."),
				("boat-entry-right", "Right boat entry", ["switch.matrix-42"], "Starboard boat-entry rollover."),
				("boat-entry-left", "Left boat entry", ["switch.matrix-43"], "Port boat-entry rollover."),
				("captive-ball", "Captive ball target", ["switch.matrix-41"], "Standup target mounted on the boat."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15109",
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
			"left) closes. Fish Tales runs Const UseSolenoids = 2 fast flips, so the ROM drives the coils "
			"directly. There are no upper flippers; the upper-flipper Fliptronic circuits (33-36, "
			"115-118) are unfitted despite pinned PinMAME's ftGameData declaring an upper-right flipper "
			"-- see switch.generic-115's notes for the full evidence trail.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="FL-11629",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.reel-opto-switches-not-normalized",
			"path": "inputs[binding.device=37,38]",
			"description": (
				"The manual documents public switches 37/38 (Reel 1, Reel 2) as opto construction: the Switch "
				"Locations parts list (printed 2-43) lists discrete parts A-14315 (LED) / A-14316 (Trans) with "
				"a blank Switch Assy No., and the Fish Reel Unit Assembly page (printed 2-26/2-27) independently "
				"confirms the identical two part numbers as the reel's top-bracket and bottom-bracket opto "
				"pairs. Pinned PinMAME's ftGameData inverted-switch mask ({0x00,0x00,0x00,0xc0,0x00,0x00,0x00,"
				"0x00,0x00,0x00,0x00,0x00}) covers only column 4 (public 47/48); column 3, which carries 37/38, "
				"is 0x00, so unlike 47/48 the public state of 37/38 is not emulator-normalized despite the "
				"confirmed opto construction. The manual is physical-construction ground truth and pinned "
				"PinMAME is public-address and emulator-normalization ground truth, and the two disagree on "
				"whether a recreation must invert these two addresses. Resolution path: run the implemented "
				"LibPinMAME gameplay harness against a legal ft_l5 ROM, drive the reel motor through its full "
				"rotation, and observe the idle public state of 37/38 and their transitions as the reel passes "
				"each documented position. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.ball-popper-drop-target-normalized-non-opto",
			"path": "inputs[binding.device=47,48]",
			"description": (
				"Pinned PinMAME's ftGameData inverted-switch mask normalizes public switches 47 (Ball Popper) "
				"and 48 (Drop Target) -- column 4 = 0xc0, bits 6 and 7 -- verified in code: (0xc0 >> 6) & 1 and "
				"(0xc0 >> 7) & 1 are the only set bits in the entire twelve-column mask. The manual documents "
				"both as ordinary microswitches with no opto or proximity marking: 47 is SW-1A-167-1/A-11658-1 "
				"and 48 is 5647-12693-31/A-15211, the latter cross-checking exactly against the 1-Bank Drop "
				"Target Assembly's own microswitch item (printed 2-29). This manual's Switch Matrix wiring page "
				"(printed 3-4) carries no shading or opto legend at all, so it cannot independently corroborate "
				"either reading. A physically normally-closed mechanical switch (not only an opto) can "
				"legitimately need the same software inversion, so this is not necessarily a defect, but the "
				"manual gives no independent confirmation either way, and it is the opposite disagreement "
				"direction from conflict.reel-opto-switches-not-normalized (there, confirmed optos are NOT "
				"normalized; here, non-opto-marked switches ARE normalized). Resolution path: the same "
				"LibPinMAME harness trace that resolves the reel-opto conflict can also observe the idle public "
				"state of 47/48 against known ball presence at the Ball Popper saucer and the Drop Target's "
				"raised/lowered state. Unresolved."
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
			"id": "williams.fish-tales.1992",
			"name": "Fish Tales",
			"manufacturer": "Williams",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 861,
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
			"opdb_id": "G5Wxd-MLxl3",
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
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
		"knowledge": {"path": "knowledge/williams/fish-tales-1992.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Fish Tales device identifiers are not unique: {duplicates}")
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
			"Public switches 37/38 (Reel 1/Reel 2) are documented opto construction that pinned PinMAME's "
			"ftGameData inverted-switch mask does not normalize (column 3 is 0x00), while public switches "
			"47/48 (Ball Popper, Drop Target) are normalized by the mask (column 4 = 0xc0) despite the "
			"manual documenting both as ordinary microswitches with no opto marking. Neither is a spatial "
			"gap -- every dimension this report audits is complete and validated -- but both are recorded "
			"as conflict.reel-opto-switches-not-normalized and "
			"conflict.ball-popper-drop-target-normalized-non-opto. The record stays partial until those "
			"polarity conflicts are resolved.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/fish-tales-1992/extracted-vpxtool.manifest.json",
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
			"root": "external:pinmame-manuals/rendered/williams.fish-tales.1992/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/fish-tales/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"l16f/l17f/l18f (address 16/17/18 backbox insert-panel lamp objects) -- backbox device, not a playfield coordinate",
			"GI0/GI1/GI3 backbox strings -- no playfield emitter collection in the retained script",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Fish Tales (Williams, 1992) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete, but the physical "
		"machine record itself remains `partial` at `machines/partial/williams/fish-tales-1992.json` "
		"because of two unresolved switch-polarity conflicts outside this audit's scope; see the "
		"promotion decision below.",
		"",
		"The matching source is the retained known-working `Fish Tales (Williams 1992) VPW 1.1.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/{PLAYFIELD_WIDTH} and "
		f"y/{PLAYFIELD_HEIGHT} rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual PDF is OCR'd, but its multi-column tables are not reliable from OCR text "
		"alone; every printed table used here was read from rendered pages and transcribed into "
		"`external:pinmame-review-artifacts/fish-tales/manual-transcription.md`.",
		"- Switches 37/38 (Reel 1/Reel 2) have no dedicated playfield sensor object; the retained script "
		"derives them from the reel's own internal ReelPosition angle counter, so both are documented "
		"projections onto the visible Reel drum Primitive that the same counter drives.",
		"- Lamps 16/17/18 are a backbox insert-panel device (A-15339 3-Lamp Board Assembly) despite the "
		"retained table modeling two co-located Light objects per address near the playfield's own rear "
		"edge for visual effect; neither is treated as a playfield coordinate. GI strings 0, 1, and 3 are "
		"likewise backbox circuits with no playfield representation in the retained script, matching this "
		"manual's own 'Backbox G.I.' classification for the same three printed addresses.",
		"- GI strings 2 and 4 use the retained table's TopGI/BottomGI emitter collections (21 and 11 "
		"members respectively), matching this manual's own 'Playfield G.I.' classification for printed "
		"strings 03 and 05 exactly.",
		"- Public solenoids 51/52/53 are PinMAME's own internal reel-position bookkeeping for its built-in "
		"ball simulator, never referenced by the retained known-working script, and have no real driver-"
		"board transistor behind them; they are declared virtual with a `virtual` spatial record.",
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
		"No authoring-critical placement, quantity, or semantic question remains unresolved for the "
		"addresses this audit covers, and the deterministic curator reproduces the canonical artifact and "
		"its pinned seed byte-for-byte. However, two switch-polarity conflicts remain unresolved "
		"(`conflict.reel-opto-switches-not-normalized` and "
		"`conflict.ball-popper-drop-target-normalized-non-opto`). The definition therefore carries a "
		"non-empty `conflicts` array and `coverage.dimensions.physical_wiring = \"conflicted\"`, so promotion "
		"to `author_ready` is refused; the record stays `partial` with `coverage.missing = [\"polarity\", "
		"\"unresolved_conflicts\"]` until a LibPinMAME harness trace against a legal ft_l5 ROM resolves the "
		"polarity conflicts.",
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
		raise RuntimeError(f"Stale Fish Tales author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Fish Tales definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Fish Tales seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Fish Tales definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Fish Tales seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Fish Tales spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Fish Tales spatial review drifted from its deterministic curator: {markdown_path}")
	print("Fish Tales definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Fish Tales extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Fish Tales retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
