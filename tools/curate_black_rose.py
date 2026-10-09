"""Curate the physical Bally Black Rose (1992) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and
runtime-derived fact as a literal and reads three committed seeds (the table-derived placements, the
factory-drawing callout check and the legacy aliases), so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots.  ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the definition, its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "bally.black-rose.1992"
PARTIAL_PATH = ROOT / "machines/partial/bally/black-rose-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/black-rose-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/black-rose-1992.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/bally/black-rose-1992.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/bally/black-rose-1992-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/black-rose-1992-callouts.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/bally/black-rose-1992-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/black-rose-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/black-rose-1992.md"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
IDENTITY_SOURCE = "identity.bally.black-rose.1992"
MANUAL_SOURCE = "manual.bally.black-rose.1992"
VPX_TABLE_SOURCE = "vpx-table.br-vpw-1-4"
VPX_SCRIPT_SOURCE = "vpx-script.br-vpw-1-4"
VPX_EXTRACTION_SOURCE = "vpx-extraction.br-vpw-1-4"
EDGES_SOURCE = "runtime.black-rose.switch-edges"
UPPER_LEFT_SOURCE = "runtime.black-rose.switch-edges-upper-left"
SOLENOID_TEST_SOURCE = "runtime.black-rose.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.black-rose.br-l4.flasher-test"
FLASHER_NAMES_SOURCE = "runtime.black-rose.flasher-test-names"
GI_TEST_SOURCE = "runtime.black-rose.gi-test"
LAMP_TEST_SOURCE = "runtime.black-rose.single-lamps"
FLIPPER_TEST_SOURCE = "runtime.black-rose.flipper-coil-test"
CANNON_TEST_SOURCE = "runtime.black-rose.cannon-test"
CALLOUT_SOURCE = "drawing-callouts.black-rose.2026-10-09"
PHOTO_SOURCE = "photos.bally.black-rose.1992.ipdb"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-fliptronic"
RUNTIME_LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"

TABLE_SHA256 = "41f965d27c1615841d39f0b83922e09e37e2fe6bad54318fd6bf18b08c1b1a8e"
SCRIPT_SHA256 = "c860e49c2b8be296ce73a64b5e9715245e290b3c2a799f24640234534f799f25"
MANUAL_SHA256 = "63c80f33ae9570c6c9575b198f7b2d73634750f0395c7280782bf7e91437cc90"
IPDB_PAGE_SHA256 = "cdafa8c6962cedc720e60d2b6427bd384dabf5aecc7829ae11ec4aae1396ea78"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

EXTRACTION_FILE_COUNT = 1715
EXTRACTION_TOTAL_BYTES = 201701385
EXTRACTION_MANIFEST_SHA256 = "6bcef73e07d14a8452b900476d320e0c26fff5d81395166afb283e17c4956a94"
EXTRACTION_RELATIVE_PATH = Path("bally/black-rose-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/black-rose-1992/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / "evidence/excerpts/bally.black-rose.1992"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("br_l4", "br_d4", "br_l3", "br_d3", "br_l1", "br_d1", "br_p17", "br_p18")
DRIVER_COMPATIBILITY = {
	"br_l4": (
		"identical",
		"Production L-4 game ROM, the latest production firmware of the physical machine and PinMAME's parent driver (the catalog "
		"year 1993 is the firmware's, the machine shipped in July 1992). The retained known-working VPW v1.4 table binds it directly "
		'(Const cGameName = "br_l4"), and every runtime run behind this definition booted it. Its test menu adds T.12 FLIPPER COIL '
		"TEST and T.13 ORDERED LAMP ahead of the cannon test, which the manual's list (written for earlier firmware) numbers T.12.",
	),
	"br_d4": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-4 ROM for the same physical machine; pinned driver.c describes the fix as a "
		"lamp-matrix driver timing correction against LED ghosting, and it changes no controller address or playfield device.",
	),
	"br_l3": (
		"identical",
		"Production L-3 game ROM of the same physical machine, on the same wpc_mFliptronS hardware with the same brGameData I/O.",
	),
	"br_d3": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-3 ROM, with no hardware or address change.",
	),
	"br_l1": (
		"identical",
		"Production L-1 game ROM, the first production firmware revision of the same physical machine; it runs on the same "
		"wpc_mFliptronS hardware with the same brGameData I/O.",
	),
	"br_d1": (
		"identical",
		"Community 'LED Ghost Fix' revision of the L-1 ROM, with no hardware or address change.",
	),
	"br_p17": (
		"unknown",
		"P-17 prototype game ROM (a 2-megabit U6 image, half the size of the production ROMs) paired in pinned br.c with the "
		"prototype U18 sound ROM u18-sp1.rom, for pre-production machines. It shares brGameData and the WPC-Fliptronic controller "
		"generation, which proves its routing, but no retained source describes the prototype machines' hardware, so whether it runs "
		"this production machine's devices unchanged is unknown: it may drive devices this definition does not declare or name them "
		"differently.",
	),
	"br_p18": (
		"unknown",
		"P-18 'LED Ghost Fix' prototype game ROM with the same prototype SP-1 sound ROM as br_p17; as for br_p17, no retained source "
		"describes the prototype hardware, so its physical compatibility is unknown.",
	),
}

# --- Switch data (switch-locations.md, switch-matrix.md) ----------------------------------------------
# address -> (switch number cell, assembly cell, description), as printed on the Switch Locations page.
SWITCH_LOCATIONS = {
	13: ("---", "20-9663-7", "Start Button"),
	14: ("---", "20-6502-A", "*Plumb Bob"),
	15: ("5647-12133-12", "A-10417", "Outhole"),
	16: ("5647-12693-08", "A-11680", "Right Trough"),
	17: ("5647-09957-00", "B-8925", "Center Trough"),
	18: ("5647-09957-00", "B-8925", "Left Trough"),
	21: ("---", "27-1066", "*Slam Tilt"),
	22: ("---", "A-8630", "*Coin Door Closed"),
	24: ("---", "A-8630", "*Always Closed"),
	25: ("5647-12693-04", "A-11619", "Shooter"),
	26: ("5647-12693-19", "A-12688-1", "Left Outlane"),
	27: ("5647-12693-19", "A-12688-1", "Left Flipper Lane"),
	28: ("SW-A1-120", "B-11700-1", "Left Sling"),
	31: ("---", "A-15118-6", "Bottom Standups Bottom"),
	32: ("---", "A-15118-6", "Bottom Standups Middle"),
	33: ("---", "A-15118-6", "Bottom Standups Top"),
	34: ("5641-12673-00", "---", "Fire Button"),
	35: ("5647-12133-12", "A-14640", "Cannon Kicker"),
	36: ("5647-12693-19", "A-12688", "Right Outlane"),
	37: ("5647-12693-19", "A-12688", "Right Return"),
	38: ("SW-1A-120", "B-11700-1", "Right Slingshot"),
	41: ("---", "A-15118-2", "Middle Standups Top"),
	42: ("---", "A-15118-2", "Middle Standups Middle"),
	43: ("---", "A-15118-2", "Middle Standups Bottom"),
	44: ("5647-12693-36", "A-14042", "Left Ramp Enter"),
	45: ("5647-12693-19", "A-12688-1", "Top Left Loop"),
	46: ("SW-1A-187", "B-13267", "Left Jet"),
	47: ("SW-1A-187", "B-13267", "Bottom Jet"),
	48: ("SW-1A-187", "B-13267", "Right Jet"),
	51: ("---", "A-15118-4", "Top Standups Bottom"),
	52: ("---", "A-15118-4", "Top Standups Middle"),
	53: ("---", "A-15118-4", "Top Standups Top"),
	54: ("5647-12693-49", "A-14821", "Up/Down Ramp"),
	55: ("SW-1A-167", "A-11657", "Ball Popper"),
	56: ("5647-12693-21", "A-14827", "Right Ramp Made"),
	57: ("5647-12693-19", "A-12688", "Exit Jet Bumpers"),
	58: ("5647-12693-19", "A-12688", "Enter Jet Bumper"),
	61: ("5647-12693-21", "A-14824", "Subway Top"),
	62: ("5647-12693-21", "A-14825", "Backboard Ramp"),
	63: ("5647-12693-50", "A-14820", "Lockup 1"),
	64: ("5647-12693-51", "A-14820", "Lockup 2"),
	65: ("---", "A-15118-5", "Right Single Standup"),
	66: ("5647-12693-21", "A-14824", "Subway Bottom"),
	71: ("5647-12693-36", "A-15132", "Lockup Enter"),
	72: ("5647-12693-11", "A-15133", "Middle Ramp"),
	76: ("5647-12693-11", "A-15131", "Right Ramp Enter"),
}
# The Switch Matrix page's own cell name where it differs in wording from the locations list.
MATRIX_NAMES = {
	14: "Plumb Bob Tilt", 25: "Shooter", 27: "Left Return Lane", 28: "Left Sling", 31: "Bottom Standup Bottom",
	32: "Bottom Standup Middle", 33: "Bottom Standup Top", 37: "Right Return Lane", 41: "Middle Standup Top",
	42: "Middle Standup Middle", 43: "Middle Standup Bottom", 47: "Right Jet", 48: "Bottom Jet", 51: "Top Standup Bottom",
	52: "Top Standup Middle", 53: "Top Standup Top", 54: "Ramp Down", 57: "Jet Bumpers Exit", 58: "Jet Bumper Enter",
}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 67, 68, 73, 74, 75, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "Outhole", 16: "Right Trough", 17: "Center Trough", 18: "Left Trough",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed", 25: "Shooter Lane", 26: "Left Outlane", 27: "Left Return Lane",
	28: "Left Slingshot", 31: "Bottom Standup Bottom", 32: "Bottom Standup Middle", 33: "Bottom Standup Top", 34: "Fire Button",
	35: "Cannon Kicker", 36: "Right Outlane", 37: "Right Return Lane", 38: "Right Slingshot", 41: "Middle Standup Top",
	42: "Middle Standup Middle", 43: "Middle Standup Bottom", 44: "Left Ramp Enter", 45: "Top Left Loop", 46: "Left Jet Bumper",
	47: "Right Jet Bumper", 48: "Bottom Jet Bumper", 51: "Top Standup Bottom", 52: "Top Standup Middle", 53: "Top Standup Top",
	54: "Ramp Down", 55: "Ball Popper (Broadside)", 56: "Right Ramp Made", 57: "Jet Bumpers Exit", 58: "Jet Bumper Enter",
	61: "Subway Top", 62: "Backboard Ramp", 63: "Lockup 1", 64: "Lockup 2", 65: "Right Single Standup", 66: "Subway Bottom",
	71: "Lockup Enter", 72: "Middle Ramp", 76: "Right Ramp Enter",
}
SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "tilt",
	22: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "leaf", 31: "unknown",
	32: "unknown", 33: "unknown", 34: "button", 35: "microswitch", 36: "microswitch", 37: "microswitch", 38: "leaf",
	41: "unknown", 42: "unknown", 43: "unknown", 44: "microswitch", 45: "microswitch", 46: "leaf", 47: "leaf", 48: "leaf",
	51: "unknown", 52: "unknown", 53: "unknown", 54: "microswitch", 55: "leaf", 56: "microswitch", 57: "microswitch",
	58: "microswitch", 61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "unknown",
	66: "microswitch", 71: "microswitch", 72: "microswitch", 76: "microswitch",
}
SWITCH_ROLES = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 34: "cabinet.fire-button"}
# The ROM's own names from the T.1 SWITCH EDGES run (the top display line while the switch is active). 37's frame clips the
# first letter at the display edge.
ROM_SWITCH_NAMES = {
	14: "PLUMB BOB TILT", 15: "OUTHOLE", 16: "RIGHT TROUGH", 17: "CENTER TROUGH", 18: "LEFT TROUGH", 25: "SHOOTER",
	26: "LEFT OUTLANE", 27: "LEFT RETURN LANE", 28: "LEFT SLINGSHOT", 31: "BOT. STANDUPS BOT", 32: "BOT. STANDUPS MID",
	33: "BOT. STANDUPS TOP", 34: "FIRE BUTTON", 35: "CANNON KICKER", 36: "RIGHT OUTLANE", 37: "(R)IGHT RETURN LANE",
	38: "RIGHT SLINGSHOT", 41: "MID. STANDUPS TOP", 42: "MID. STANDUPS MID", 43: "MID. STANDUPS BOT", 44: "L. RAMP ENTER",
	45: "TOP LEFT LOOP", 46: "LEFT JET", 47: "RIGHT JET", 48: "BOTTOM JET", 51: "TOP STANDUPS BOT", 52: "TOP STANDUPS MID",
	53: "TOP STANDUPS TOP", 54: "RAMP DOWN", 55: "BALL POPPER", 56: "R. RAMP MADE", 57: "JETS EXIT", 58: "JETS ENTER",
	61: "SUBWAY TOP", 62: "BACKBOARD RAMP", 63: "LOCKUP 1", 64: "LOCKUP 2", 65: "R. SINGLE STANDUP", 66: "SUBWAY BOTTOM",
	71: "LOCKUP ENTER", 72: "MIDDLE RAMP", 76: "R. RAMP ENTER",
}
# Switches whose closure the ROM answers with their coil even inside T.1.
EDGE_COILS = {28: 6, 38: 5, 46: 13, 47: 14, 48: 15}
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
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"), 3: ("Orange-Black", "J205-3", "U17-11"),
	4: ("Orange-Yellow", "J205-4", "U17-9"), 5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
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
# Fliptronic grounded switches (switch-matrix.md, fliptronic-and-flipper-wiring.md): public -> (label, wire, connector, IC,
# type, role, printed number). None marks a position with nothing fitted.
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "Black-Green", "J906-1", "U4A-5", "leaf", "internal.flipper.lower.right.eos", "F1"),
	112: ("Lower Right Flipper Button", "Blue-Violet", "J905-1", "U4B-7", "opto", "flipper.lower.right.button", "F2"),
	113: ("Lower Left Flipper EOS", "Black-Blue", "J906-3", "U4C-9", "leaf", "internal.flipper.lower.left.eos", "F3"),
	114: ("Lower Left Flipper Button", "Blue-Gray", "J905-2", "U4D-11", "opto", "flipper.lower.left.button", "F4"),
	115: ("Upper Right Flipper EOS", "Black-Violet", "J906-4", "U6A-5", "leaf", "internal.flipper.upper.right.eos", "F5"),
	116: ("Upper Right Flipper Button", "Black-Yellow", "J905-3", "U6B-7", "opto", "flipper.upper.right.button", "F6"),
	117: ("Not Fitted Upper Left Flipper EOS", None, None, "U6C-9", None, "internal.unused.flipper", "F7"),
	118: ("Left Flipper Button Second Opto (Upper Left Channel)", "Black-Blue", "J905-5", "U6D-11", "opto", "internal.flipper.upper.left.button", "F8"),
}

# --- Solenoid data (solenoid-flasher-table.md, solenoid-flasher-locations.md, power-driver-board-connectors.md) ---
SOLENOID_LABELS = {
	1: "Ball Popper", 2: "Outhole", 3: "Cannon Motor", 4: "Ball Release", 5: "Right Slingshot", 6: "Left Slingshot",
	7: "Knocker", 8: "Cannon Kicker", 9: "Left Ball Lockup", 10: "Ramp Up", 11: "Ramp Down", 13: "Left Jet Bumper",
	14: "Right Jet Bumper", 15: "Bottom Jet Bumper", 17: "Left Bottom Flasher", 18: "Left Top Flasher", 19: "Right Bottom Flasher",
	20: "Right Top Flasher", 21: "Right Ramp Flasher", 22: "Left Ramp Flasher", 23: "Locker Open Flasher", 24: "Left Sword Flasher",
	25: "Top Popper Flasher", 26: "Cannon Flasher", 27: "Fire Button Flasher", 28: "Right Sword Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_USED_SOLENOID_LABELS = {
	12: "Not Used Solenoid Position 12",
	16: "Not Used Solenoid Position 16",
	35: "Not Fitted Upper Left Flipper Power",
	36: "Not Fitted Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC State Bit 29 (GILAMPS bit 5)",
	30: "WPC State Bit 30 (GILAMPS bit 6)",
	31: "WPC State Bit 31 (GILAMPS bit 7)",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38",
	39: "Unused WPC-Fliptronic Output 39", 40: "Unused WPC-Fliptronic Output 40",
	41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> (printed type, wire colour, printed connection, driver transistor, part / flashlamp), solenoid-flasher-table.md.
SOLENOID_TABLE = {
	1: ("High Power", "Vio-Brn", "J130-1", "Q82", "AE-24-900"),
	2: ("High Power", "Vio-Red", "J130-2", "Q80", "AE-27-1200"),
	3: ("High Power", "Vio-Orn", "J130-4", "Q78", "14-7965 20V"),
	4: ("High Power", "Vio-Yel", "J130-5", "Q76", "AE-26-1200"),
	5: ("High Power", "Vio-Grn", "J130-6", "Q64", "AE-26-1500"),
	6: ("High Power", "Vio-Blu", "J130-7", "Q66", "AE-26-1500"),
	7: ("High Power", "Vio-Blk", "J130-8", "Q68", "AE-23-800"),
	8: ("Low Power", "Vio-Gry", "J130-9", "Q70", "A-15016"),
	9: ("Low Power", "Brn-Blk", "J127-1", "Q58", "AE-26-1500"),
	10: ("Low Power", "Brn-Red", "J127-3", "Q56", "AE-26-1200"),
	11: ("Low Power", "Brn-Org", "J127-4", "Q54", "SM1-29-1000-DC"),
	12: ("Low Power", "Brn-Yel", "J127-5", "Q52", None),
	13: ("Low Power", "Brn-Grn", "J127-6", "Q50", "AE-26-1200"),
	14: ("Low Power", "Brn-Blu", "J127-7", "Q48", "AE-26-1200"),
	15: ("Low Power", "Brn-Vio", "J127-8", "Q46", "AE-26-1200"),
	16: ("Low Power", "Brn-Gry", "J127-9", "Q44", None),
	17: ("Flasher", "Blk-Brn", "J125-1, J126-1", "Q42", "#906,#89"),
	18: ("Flasher", "Blk-Red", "J125-2, J126-2", "Q40", "#906,#89"),
	19: ("Flasher", "Blk-Org", "J125-3, J126-3", "Q38", "#906,#89"),
	20: ("Flasher", "Blk-Yel", "J125-5, J126-4", "Q36", "#906,#89"),
	21: ("Flasher", "Blu-Grn", "J125-6, J126-5", "Q28", "#906,#89"),
	22: ("Flasher", "Blu-Blk", "J125-7, J126-6", "Q30", "#906,#89"),
	23: ("Low Power", "Blu-Vio", "J125-8, J126-7", "Q34", "#906"),
	24: ("Low Power", "Blu-Gry", "J125-9, J126-8", "Q32", "#906"),
	25: ("Flasher", "Blu-Brn", "J123-1", "Q26", "#906"),
	26: ("Flasher", "Blu-Red", "J123-2", "Q24", "#906"),
	27: ("Flasher", "Blu-Org", "J123-3", "Q22", "#906"),
	28: ("Flasher", "Blu-Yel", "J123-4", "Q20", "#906"),
}
# The control connection followed in structured data: the connector list (power-driver-board-connectors.md) where it and the
# solenoid wiring page agree against the table's J123 pins; 27 and 28 also feed an insert flasher on J132.
SOLENOID_CONNECTIONS = {
	25: "J123-1", 26: "J123-3", 27: "J123-4, J132-3", 28: "J123-5, J132-5",
}
# Locations-list assembly and coil/flashlamp part for each coil/flasher (solenoid-flasher-locations.md).
SOLENOID_ASSEMBLIES = {
	1: "D-11335-1", 2: "A-8039-3", 3: "A-14635", 4: "B-9362-L-2", 5: "B-11203-R-1", 6: "B-11203-L-1", 7: "B-10686-1",
	8: "A-14640", 9: "B-11203-R-1", 10: "B-9362-R-3", 11: "A-14918", 13: "A-12872-1", 14: "A-12872-1", 15: "A-12842-3",
	18: "A-8798", 20: "A-8798", 21: "A-8798", 22: "A-8798", 23: "A-12336-1", 24: "A-12336-1", 25: "C-13337",
	26: "A-12336-1", 27: "A-12336-1", 28: "A-12336-1",
}
FLASHER_LAMPS = {
	17: "24-8802 Left Bottom Flasher #906", 18: "24-8704 Left Top Flasher #89", 19: "24-8802 Right Bottom Flasher #906",
	20: "24-8704 Right Top Flasher #89", 21: "24-8704 Right Ramp Flasher #89", 22: "24-8704 Left Ramp Flasher #89",
	23: "24-8704 Locker Open Flasher #906", 24: "24-8802 Left Sword Flasher #906", 25: "24-8802 Top Popper Flasher #906 (2)",
	26: "24-8802 Cannon Flasher (2) #906", 27: "24-8802 Fire Button Flasher #906", 28: "24-8802 Right Sword Flasher #906",
}
FLASHER_SOLENOIDS = frozenset(range(17, 29))
BACKBOX_INSERT_FLASHERS = frozenset({17, 18, 19, 20, 21, 22, 23, 24, 27, 28})
# Printed flasher counts on the Locations list: 25 "#906 (2)", 26 "(2) #906".
FLASHER_COUNTS = {25: 2, 26: 2}
# The ROM's T.4 SOLENOID TEST and T.5 FLASHER TEST names and wires per public address (read from the retained frames).
T4_NAMES = {
	1: "BALL POPPER", 2: "OUTHOLE", 3: "CANNON MOTOR", 4: "BALL RELEASE", 5: "RIGHT SLINGSHOT", 6: "LEFT SLINGSHOT", 7: "KNOCKER",
	8: "CANNON KICKER", 9: "BALL LOCKUP", 10: "RAMP UP", 11: "RAMP DOWN", 13: "LEFT JET", 14: "RIGHT JET", 15: "BOTTOM JET",
}
T4_WIRES = {
	1: "VIO-BRN VIO-YEL", 2: "VIO-RED VIO-YEL", 3: "VIO-ORN VIO-YEL", 4: "VIO-YEL VIO-YEL", 5: "VIO-GRN VIO-YEL", 6: "VIO-BLU VIO-YEL",
	7: "VIO-BLK VIO-YEL", 8: "VIO-GRY VIO-YEL", 9: "BRN-BLK VIO-ORN", 10: "BRN-RED VIO-ORN", 11: "BRN-ORN VIO-ORN",
	13: "BRN-GRN VIO-ORN", 14: "BRN-BLU VIO-ORN", 15: "BRN-VIO VIO-ORN",
}
T5_NAMES = {
	17: "LEFT BOTTOM", 18: "LEFT TOP", 19: "RIGHT BOTTOM", 20: "RIGHT TOP", 21: "RIGHT RAMP", 22: "LEFT RAMP", 23: "LOCKER OPEN",
	24: "LEFT SWORD", 25: "TOP POPPER", 26: "CANNON", 27: "FIRE BUTTON", 28: "RIGHT SWORD",
}
SOLENOID_CALLBACKS = {
	1: "RampSwordKicker", 2: "bsTroughSolIn", 3: "CannonMotor", 4: "bsTroughSolOut", 7: "SolKnocker", 8: "FireCannon",
	9: "PiratesCoveKick", 10: "RampUp", 11: "RampDown", 17: "Sol17 (SolModCallback)", 18: "Sol18 (SolModCallback)",
	19: "Sol19 (SolModCallback)", 20: "Sol20 (SolModCallback)", 21: "Sol21 (SolModCallback)", 22: "Sol22 (SolModCallback)",
	23: "Sol23 (SolModCallback)", 24: "Sol24 (SolModCallback)", 25: "SetLamp 125 (SolModCallback)", 26: "SetLamp 126 (SolModCallback)",
	27: "Sol27 (SolModCallback)", 28: "Sol28 (SolModCallback)", 34: "SolURFlipper (sURFlipper)", 46: "SolRFlipper (sLRFlipper)",
	48: "SolLFlipper (sLLFlipper)",
}
# Fliptronic circuits (solenoid-flasher-table.md, fliptronic-and-flipper-wiring.md, the T.12 FLIPPER COIL TEST):
# public -> (stage, voltage connector, J902 control pin, printed transistor pair, supply wire, control wire, ROM name, ROM wires).
FLIPPER_COILS = {
	45: ("power", "J907-8,9", "J902-13", "Q4, Q11", "Blue-Yellow", "Blue-Violet", "R. FLIP. POWER", "BLU-VIO BLU-YEL"),
	46: ("hold", "J907-8,9", "J902-11", "Q4, Q11", "Blue-Yellow", "Orange-Green", "R. FLIP. HOLD", "ORN-GRN BLU-YEL"),
	47: ("power", "J907-6,7", "J902-9", "Q3, Q9", "Gray-Yellow", "Blue-Gray", "L. FLIP. POWER", "BLU-GRY GRY-YEL"),
	48: ("hold", "J907-6,7", "J902-7", "Q3, Q9", "Gray-Yellow", "Orange-Blue", "L. FLIP. HOLD", "ORN-BLU GRY-YEL"),
	33: ("power", "J907-4,5", "J902-6", "Q2, Q7", "Blue-Yellow", "Black-Yellow", "U.R. FLIP. POWER", "BLK-YEL BLU-YEL"),
	34: ("hold", "J907-4,5", "J902-4", "Q2, Q7", "Blue-Yellow", "Orange-Violet", "U.R. FLIP. HOLD", "ORN-VIO BLU-YEL"),
}
FLIPPER_SIDES = {45: "Lower Right", 46: "Lower Right", 47: "Lower Left", 48: "Lower Left", 33: "Upper Right", 34: "Upper Right"}
FLIPPER_PARTS = {45: ("FL-11629", "A-14876-R-3"), 46: ("FL-11629", "A-14876-R-3"), 47: ("FL-11629", "A-14876-L-3"),
	48: ("FL-11629", "A-14876-L-3"), 33: ("FL-11630", "A-15205-R-3"), 34: ("FL-11630", "A-15205-R-3")}

# --- Lamp data (lamp-locations.md, lamp-matrix.md, power-driver-board-connectors.md) -----------------------------
# address -> (bulb, assembly, description as printed); second bulbs listed separately.
LAMP_LOCATIONS = {
	11: ("24-6549", "A-11754", "Special #44"), 12: ("24-8768", "C-12982", "Jet Enter 8K #555"),
	13: ("24-8768", "C-12982", "Jet Enter 4K #555"), 14: ("24-8768", "C-13028", "Jet Enter 2K #555"),
	15: ("24-8768", "C-13028", "Jet Enter 1K #555"), 16: ("24-8768", "C-13028", "Jet Enter Jewel #555"),
	17: ("24-8768", "C-13028", "Sequence Shot 2 #555"), 18: ("24-6549", "A-11271", "Single Standup #44"),
	21: ("24-8768", "C-13361", "Letter (S) I N K #555"), 22: ("24-8768", "C-13361", "Letter S (I) N K #555"),
	23: ("24-8768", "C-13361", "Letter S I (N) K #555"), 24: ("24-6549", "A-11754", "Letter S I N (K) #44"),
	25: ("24-6549", "A-11754", "Letter (S) H I P #44"), 26: ("24-8768", "C-13361", "Letter S (H) I P #555"),
	27: ("24-8768", "C-13361", "Letter S H (I) P #555"), 28: ("24-8768", "C-13361", "Letter S H I (P) #555"),
	31: ("24-8768", "A-15141", "Bottom Standups Bottom #555"), 32: ("24-8768", "A-15141", "Bottom Standups Middle #555"),
	33: ("24-8768", "A-15141", "Bottom Standups Top #555"), 34: ("24-8768", "A-15140", "Ramp 100K #555"),
	35: ("24-8768", "A-15140", "Right Ramp 200K #555"), 36: ("24-8768", "A-15140", "Right Ramp 300K #555"),
	37: ("24-8768", "A-15140", "Right Ramp 400K #555"), 38: ("24-8768", "A-15140", "Right Ramp Million #555"),
	41: ("24-8768", "C-13361", "Middle Standups Top #555"), 42: ("24-8768", "C-13361", "Middle Standups Middle #555"),
	43: ("24-8768", "C-13361", "Middle Standups Bottom #555"), 44: ("24-6549", "A-11271", "Left Drain #44"),
	45: ("24-6549", "A-11271", "Left Return #44"), 46: ("24-6549", "A-11271", "Right Return #44"),
	47: ("24-6549", "A-11271", "Right Drain #44"), 48: ("24-6549", "A-11754", "Shoot Again #44"),
	51: ("24-8768", "A-15142", "Top Standups Bottom #555"), 52: ("24-8768", "A-15142", "Top Standups Middle #555"),
	53: ("24-8768", "A-15142", "Top Standups Top #555"), 54: ("24-6549", "A-11754", "Lock 1 #44"),
	55: ("24-6549", "A-11754", "Lock 2 #44"), 56: ("24-6549", "A-11754", "Lockup Jewel #44"),
	57: ("24-6549", "A-11271", "Left Ramp Coins #44"), 58: ("24-6549", "A-11271", "Bottom Standup Jewel #44"),
	61: ("24-8768", "A-15141", "Middle Ramp Jewel #555"), 62: ("24-8768", "A-15142", "Top Loop Jewel #555"),
	63: ("24-8768", "A-15142", "Top Standup Jewel #555"), 64: ("24-6549", "A-11271", "Broadside Jewel #44"),
	65: ("24-8768", "A-15140", "Bottom Standup Jewel #555"), 66: ("24-6549", "A-11271", "Right Ramp Jewel #44"),
	67: ("24-8768", "A-15142", "Sequence Shot 1 #555"), 68: ("24-6549", "A-11754", "Multiball Release #44"),
	71: ("24-8768", "A-15142", "Millions #555"), 72: ("24-8768", "A-15142", "Rigging Swing #555"),
	73: ("24-8768", "A-15141", "Treasure Chest #555"), 74: ("24-8768", "A-15141", "Walk the Plank #555"),
	75: ("24-8768", "A-15141", "Instant Multiball #555"), 76: ("24-6549", "A-11271", "Knife Throw #44"),
	77: ("24-6549", "A-11754", "Polly #44"), 78: ("24-8768", "---", "Insert Left #555"),
	81: ("24-8768", "A-15140", "Skill Shot 1 #555"), 82: ("24-6549", "A-11271", "Skill Shot 2 #44"),
	83: ("24-8768", "A-15141", "Middle Ramp Left #555"), 84: ("24-8768", "A-15140", "Middle Ramp Middle #555"),
	85: ("24-6549", "A-11271", "Middle Ramp Right #44"), 86: ("24-6549", "A-11271", "Jackpot #44"),
	87: ("24-8768", "---", "Insert Right #555"), 88: ("---", "20-9663-7", "Credit Button"),
}
# The lamp matrix page's own cell names (lamp-matrix.md) and the ROM's T.8 SINGLE LAMPS names (read from the frames).
LAMP_MATRIX_NAMES = {
	11: "Special", 12: "Jet Enter 8K", 13: "Jet Enter 4K", 14: "Jet Enter 2K", 15: "Jet Enter 1K", 16: "Jet Enter Jewel",
	17: "Combo Shot Right", 18: "Right Single Standup", 21: "Letter (S) INK", 22: "Letter S (I) NK", 23: "Letter SI (N) K",
	24: "Letter SIN (K)", 25: "Letter (S) HIP", 26: "Letter S (H) IP", 27: "Letter SH (I) P", 28: "Letter SHI (P)",
	31: "Bottom Standup Bottom", 32: "Bottom Standup Middle", 33: "Bottom Standup Top", 34: "Right Ramp 100K",
	35: "Right Ramp 200K", 36: "Right Ramp 300K", 37: "Right Ramp 400K", 38: "Right Ramp Million", 41: "Middle Standup Top",
	42: "Middle Standup Middle", 43: "Middle Standup Bottom", 44: "Left Outlane", 45: "Left Return Lane", 46: "Right Return Lane",
	47: "Right Outlane", 48: "Shoot Again", 51: "Top Standup Bottom", 52: "Top Standup Middle", 53: "Top Standup Top",
	54: "Lockup 1", 55: "Lockup 2", 56: "Lockup Jewel", 57: "Left Ramp Coins", 58: "Bottom Standup Jewel", 61: "Middle Ramp Jewel",
	62: "Top Loop Jewel", 63: "Top Standup Jewel", 64: "Broadside Jewel", 65: "Bottom Standup Jewel", 66: "Right Ramp Coins",
	67: "Sequence Shot 1", 68: "Multi-ball Ready", 71: "Millions", 72: "Rigging Swing", 73: "Treasure Chest", 74: "Walk The Plank",
	75: "Instant Multi-ball", 76: "Knife Throw", 77: "Polly", 78: "Insert Left", 81: "Skill (Open)", 82: "Skill (Locker)",
	83: "Middle Ramp 200K", 84: "Middle Ramp 300K", 85: "Middle Ramp 400K", 86: "Jackpot", 87: "Insert Right", 88: "Credit Button",
}
ROM_LAMP_NAMES = {
	11: "SPECIAL", 12: "JET ENTER 8K", 13: "JET ENTER 4K", 14: "JET ENTER 2K", 15: "JET ENTER 1K", 16: "JET ENTER JEWEL",
	17: "COMBO SHOT RIGHT", 18: "R. SINGLE STANDUP", 21: "LETTER (S)INK", 22: "LETTER S(I)NK", 23: "LETTER SI(N)K",
	24: "LETTER SIN(K)", 25: "LETTER (S)HIP", 26: "LETTER S(H)IP", 27: "LETTER SH(I)P", 28: "LETTER SHI(P)",
	31: "BOT. STANDUPS BOT.", 32: "BOT. STANDUPS MID.", 33: "BOT. STANDUPS TOP", 34: "RGT RAMP 100K", 35: "RGT RAMP 200K",
	36: "RGT RAMP 300K", 37: "RGT RAMP 400K", 38: "RGT RAMP MILL.", 41: "MID. STANDUPS TOP", 42: "MID. STANDUPS MID.",
	43: "MID. STANDUPS BOT.", 44: "LEFT OUTLANE", 45: "LEFT RETURN LANE", 46: "(R)IGHT RETURN LANE", 47: "RIGHT OUTLANE",
	48: "SHOOT AGAIN", 51: "TOP STANDUPS BOT.", 52: "TOP STANDUPS MID.", 53: "TOP STANDUPS TOP", 54: "LOCKUP 1", 55: "LOCKUP 2",
	56: "LOCKUP JEWEL", 57: "LEFT RAMP COINS", 58: "BOT. STNDUP JEWEL", 61: "MID. RAMP JEWEL", 62: "TOP LOOP JEWEL",
	63: "TOP STNDUP JEWEL", 64: "BROADSIDE JEWEL", 65: "BOT. STNDUP JEWEL", 66: "R. RAMP COINS", 67: "COMBO SHOT LEFT",
	68: "MULTIBALL READY", 71: "MILLIONS", 72: "RIGGING SWING", 73: "TREASURE CHEST", 74: "WALK THE PLANK", 75: "INSTANT MULTI",
	76: "KNIFE THROW", 77: "POLLY", 78: "INSERT LEFT", 81: "SKILL (OPEN)", 82: "SKILL (LOCKER)", 83: "MID. RAMP 200K",
	84: "MID. RAMP 300K", 85: "MID. RAMP 400K", 86: "JACKPOT", 87: "INSERT RIGHT", 88: "CREDIT BUTTON",
}
LAMP_LABELS = {
	11: "Special", 12: "Jet Enter 8K", 13: "Jet Enter 4K", 14: "Jet Enter 2K", 15: "Jet Enter 1K", 16: "Jet Enter Jewel",
	17: "Combo Shot Right (Sequence Shot 2)", 18: "Right Single Standup", 21: "SINK Letter S", 22: "SINK Letter I",
	23: "SINK Letter N", 24: "SINK Letter K", 25: "SHIP Letter S", 26: "SHIP Letter H", 27: "SHIP Letter I", 28: "SHIP Letter P",
	31: "Bottom Standup Bottom", 32: "Bottom Standup Middle", 33: "Bottom Standup Top", 34: "Right Ramp 100K",
	35: "Right Ramp 200K", 36: "Right Ramp 300K", 37: "Right Ramp 400K", 38: "Right Ramp Million", 41: "Middle Standup Top",
	42: "Middle Standup Middle", 43: "Middle Standup Bottom", 44: "Left Outlane", 45: "Left Return Lane", 46: "Right Return Lane",
	47: "Right Outlane", 48: "Shoot Again", 51: "Top Standup Bottom", 52: "Top Standup Middle", 53: "Top Standup Top",
	54: "Lockup 1", 55: "Lockup 2", 56: "Lockup Jewel", 57: "Left Ramp Coins", 58: "Bottom Standup Jewel (58)",
	61: "Middle Ramp Jewel", 62: "Top Loop Jewel", 63: "Top Standup Jewel", 64: "Broadside Jewel", 65: "Bottom Standup Jewel (65)",
	66: "Right Ramp Coins (Jewel)", 67: "Combo Shot Left (Sequence Shot 1)", 68: "Multiball Ready (Release)", 71: "Millions",
	72: "Rigging Swing", 73: "Treasure Chest", 74: "Walk the Plank", 75: "Instant Multiball", 76: "Knife Throw", 77: "Polly",
	78: "Insert Left (Backbox)", 81: "Skill Shot 1 (Open)", 82: "Skill Shot 2 (Locker)", 83: "Middle Ramp 200K (Left)",
	84: "Middle Ramp 300K (Middle)", 85: "Middle Ramp 400K (Right)", 86: "Jackpot", 87: "Insert Right (Backbox)", 88: "Credit Button",
}
ROM_LAMP_ROW_WIRES = {1: "BRN", 2: "BLK", 3: "ORN", 4: "YEL", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
ROM_LAMP_COLUMN_WIRES = {1: "BRN", 2: "RED", 3: "ORN", 4: "BLK", 5: "GRN", 6: "BLU", 7: "VIO", 8: "GRY"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# Two bulbs: 11 has a #44 and a #555 row and two balloons; 86 has one row but one balloon with two wedges (JACK and POT).
DUAL_BULB_LAMPS = {11: "a second row (24-8768, C-12982, 'Special #555') and two balloons, one at the right and one at the left rail", 86: "one row but a balloon with two wedges ending on two inserts, which the retained table models as l86 ('Jack') and l86a ('Pot')"}
SWORD_LAMPS = frozenset({14, 15, 16, 17})
BACKBOX_LAMPS = {78: ("J138-7", "J135-9"), 87: ("J138-9", "J135-8")}
CABINET_LAMPS = {88}

# --- General illumination (solenoid-flasher-table.md, power-driver-board-connectors.md, the T.6 run) ----------------
# address -> (printed name, wire, return connection, feed, transistor, bulbs, ROM name, ROM wires)
GI_STRINGS = {
	0: ("Jet & Back Ramp String", "Brown", "J120-1", "J120-7 White-Brown", "Q18", "#44, #555", "JETS & BACK RAMP", "WHT-BRN BRN"),
	1: ("Top Playfield String", "Orange", "J120-2", "J120-8 White-Orange", "Q10", "#44, #555", "TOP PLAYFIELD", "WHT-ORN ORN"),
	2: ("Bottom Playfield String", "Yellow", "J120-3", "J120-9 White-Yellow", "Q14", "#44, #555", "BOT. PLAYFIELD", "WHT-YEL YEL"),
	3: ("Left Insert String", "Green", "J121-5", "J121-10 White-Green", "Q16", "#555", "LEFT/TOP INSERT", "WHT-GRN GRN"),
	4: ("Right Insert String", "Violet", "J121-6", "J121-11 White-Violet", "Q12", "#555", "RIGHT INSERT", "WHT-VIO VIO"),
}
GI_LABELS = {0: "Jets & Back Ramp", 1: "Top Playfield", 2: "Bottom Playfield", 3: "Left Insert (Backbox)", 4: "Right Insert (Backbox)"}


# --- Shared helpers ------------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _excerpt_digests() -> dict[str, str]:
	return {path.name: _file_sha256(path) for path in sorted(EXCERPT_ROOT.glob("*")) if path.is_file()}


EXCERPT_FILE_HASHES = _excerpt_digests()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Black Rose retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Black Rose extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Black Rose retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Black Rose retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Black Rose retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


_LEGACY_ALIASES: dict[str, Any] = {}


def _legacy_aliases() -> dict[str, Any]:
	"""The legacy import's numeric and zero-padded aliases by binding group and address, kept while compatibility needs them."""
	if not _LEGACY_ALIASES:
		_LEGACY_ALIASES.update(load_json(LEGACY_ALIAS_SEED_PATH)["aliases"])
	return _LEGACY_ALIASES


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


def _callout_seed() -> dict[str, Any]:
	return load_json(CALLOUT_SEED_PATH)


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(status, *refs),
	}
	device.update({key: value for key, value in extra.items() if value is not None})
	legacy = _legacy_aliases().get(group, {}).get(str(address))
	if legacy:
		device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in legacy]
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")


# --- Placements ----------------------------------------------------------------------------------------
def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Located spatial record for one device from the committed placement seed, or None.

	Table-derived placements start as ``observed``; ``drawing_callouts.apply_to_definition`` promotes the
	ones the factory location drawings confirm. A placement measured on a drawing takes its coordinate from
	the callout seed's measurement, stays observed and cites the manual and the callout record.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placement_id = f"{identifier}.{role}{suffix}"
		if entry.get("measured"):
			x, y = drawing_callouts.measured(_callout_seed(), placement_id)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CALLOUT_SOURCE)
		else:
			x, y = entry["x"], entry["y"]
			refs = (VPX_TABLE_SOURCE,)
		placements.append({"id": placement_id, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance("observed", *refs)})
	return {"status": "observed", "placements": placements}


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


# What the retained known-working script does for each matrix switch.
SWITCH_SCRIPT = {
	15: "the cvpmTrough's EntrySw is 15; Drain_Hit hands a drained ball to the trough, which sets it", 16: "cvpmTrough initSwitches Array(16, 17, 18) sets it from the trough's ball count (no table object)",
	17: "cvpmTrough initSwitches sets it from the trough's ball count (no table object)", 18: "cvpmTrough initSwitches sets it from the trough's ball count (no table object)",
	25: "ShooterLane_Hit/_UnHit follow the ball (Controller.Switch 1/0)", 26: "Sw26_Hit/_UnHit follow the ball", 27: "Sw27_Hit/_UnHit follow the ball",
	28: "LeftSlingShot_Slingshot pulses it (vpmTimer.PulseSw)", 34: "the plunger key writes Controller.Switch(34) while it is held, together with the table's Plunger object",
	35: "sw66_Sub_Hit sets it when the subway delivers a ball into the cannon, and FireCannon (solenoid 8) clears it as it launches the ball",
	36: "Sw36_Hit/_UnHit follow the ball", 37: "Sw37_Hit/_UnHit follow the ball", 38: "RightSlingShot_Slingshot pulses it (vpmTimer.PulseSw)",
	44: "GateSw44_Hit pulses it", 45: "Sw45_Hit/_UnHit follow the ball", 46: "Bumper1_Hit pulses it", 47: "Bumper2_Hit pulses it", 48: "BumperSw48_Hit pulses it",
	54: "the RampDown callback (solenoid 11) sets it and the RampUp callback (solenoid 10) clears it, with no table object",
	55: "KickerSW55_Hit sets it and the RampSwordKicker callback (solenoid 1) clears it as it kicks the ball up", 56: "Sw56_Hit/_UnHit follow the ball",
	57: "Sw57_Hit/_UnHit follow the ball", 58: "Sw58_Hit/_UnHit follow the ball", 61: "sw61_Sub_Hit pulses it as the ball drops into the subway",
	62: "Sw62_Hit/_UnHit follow the ball", 63: "KickerSw63_Hit sets it and PiratesCoveKick (solenoid 9) clears it", 64: "KickerSw64_Hit sets it and PiratesCoveKick (solenoid 9) clears it",
	65: "Sw65_Hit pulses it", 66: "sw66_Sub_Hit pulses it and loads the cannon (sets 35)", 71: "GateSw71_Hit pulses it", 72: "GateSw72_Hit pulses it", 76: "GateSw76_Hit pulses it",
}
for _address in (31, 32, 33, 41, 42, 43, 51, 52, 53):
	SWITCH_SCRIPT[_address] = f"Sw{_address}_Hit pulses it (stand-up target)"

SWITCH_NOTES = {
	15: "The outhole kicker (solenoid 2) kicks a drained ball from here into the trough.",
	16: "The trough end next to the ball release (solenoid 4), which feeds the shooter lane.",
	17: "The middle of the three trough positions.",
	18: "The trough position nearest the outhole.",
	25: "Shooter-lane rollover under the ball waiting at the manual plunger.",
	34: "The Fire button on the lockdown bar fires the cannon; the manual's Game Control Locations page names only the Start button, the coin-door buttons, the flipper buttons and the ball shooter, and IPDB places the Fire button on the lockdown bar.",
	35: "The cannon kicker switch on the A-14640 Catapult Assembly (item 10, 5647-12133-12) under the cannon: it closes while a ball sits in the catapult. The ROM's T.14 CANNON TEST prints SW.35 CANNON = CLOSED at public 1 and OPEN at public 0, and fires the cannon kicker (solenoid 8) on the closure.",
	44: "Entrance switch of the left ramp.",
	45: "Rollover in the top left loop.",
	54: "Closes when the up/down (Davy Jones' Locker) ramp is down: the manual's error messages say 'Check to make sure switch 54, ramp down, is definitely closed when the ramp is down, and positively open when the ramp is up', and report a ramp that fails to open or close after three tries. The Switch Locations list prints 'Up/Down Ramp' (5647-12693-49, A-14821).",
	55: "The Broadside popper's switch (SW-1A-167, A-11657): a ball resting in the popper at the top of the playfield, kicked up by solenoid 1.",
	61: "Top of the subway that carries a ball from the locker under the playfield to the cannon.",
	62: "Ramp switch on the backboard ramp.",
	63: "Lockup position 1 of Pirates' Cove (5647-12693-50, A-14820).",
	64: "Lockup position 2 of Pirates' Cove (5647-12693-51, A-14820).",
	65: "The single standup target on the right (A-15118-5), the Doubloon target of the game rules.",
	66: "Bottom of the subway, where the ball drops into the cannon's catapult.",
	71: "Entrance switch of Pirates' Cove (the lockup).",
	72: "Middle ramp switch (A-15133), the locker ramp of the game rules.",
	76: "Entrance switch of the right ramp.",
}


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += "" if address == 23 else " The Switch Matrix prints this cell 'Not Used'"
		if address in {11, 12}:
			notes += (
				". The Switch Locations parts list numbers its first two rows 11 'Right Flipper' (SW-1A-192, A-15060) and 12 'Left Flipper' "
				"(SW-1A-191, A-15058) and draws their balloons beside the cabinet's front corners: those are the cabinet flipper buttons, which "
				"reach the Fliptronic II board (F2 and F4, public 112 and 114), not matrix positions 11 and 12."
			)
		elif address == 23:
			notes += (
				" The Switch Matrix prints this cell only with the name 'Ticket Opto', and the Switch Locations list prints '*Ticket Opto.' "
				"with 'Not Used' in its assembly column. No ticket dispenser is part of the machine, so the position is a vestigial ticket-opto "
				"label with nothing fitted."
			)
		elif address == 77:
			notes += (
				", and the Switch Locations list's '77-88 Not Used' row covers it. Pinned br.c defines swCannonDir as 77 and marks it "
				"'FAKE!, Not used in the Pin': its simulator writes the cannon's sweep direction there, which no physical switch supplies."
			)
		else:
			notes += ", and the Switch Locations list's Not Used range row covers it."
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE) + ((CORE_SOURCE,) if address == 77 else ()),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra,
		)
	switch_no, assembly, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if switch_no != "---":
		physical["part_number"] = switch_no
	if assembly != "---":
		physical["assembly_part_number"] = assembly
	notes += f' Switch Locations description "{description}".'
	if address in MATRIX_NAMES:
		notes += f' The Switch Matrix names it "{MATRIX_NAMES[address]}".'
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in ROM_SWITCH_NAMES:
		refs += (EDGES_SOURCE,)
		notes += (
			f' The ROM\'s T.1 SWITCH EDGES run names it "{ROM_SWITCH_NAMES[address]}" while public {address} is 1, with the wires '
			"of its matrix row and column, and clears the name at 0; brGameData's inverted-switch mask is all zero, so the CPU reads the "
			"public level directly and the contact rests open."
		)
		if "(R)" in ROM_SWITCH_NAMES[address]:
			notes += " The frame clips the leading R at the display edge; (R) marks the letter it cuts off."
	if address in EDGE_COILS:
		notes += f" In the same run the ROM fires solenoid {EDGE_COILS[address]} on the closure."
	if address in SWITCH_NOTES:
		notes += " " + SWITCH_NOTES[address]
	if address in {47, 48}:
		notes += (
			" The Switch Locations list prints 47 'Bottom Jet' and 48 'Right Jet', the other way round from the Switch Matrix (47 Right Jet, "
			"48 Bottom Jet). The matrix is followed: the ROM names 47 RIGHT JET and 48 BOTTOM JET and fires the Right and Bottom Jet Bumper "
			"coils (14 and 15) from them, the same list's drawing puts balloon 47 on the right bumper and 48 on the lower one, and the retained "
			"script pulses 47 from the right bumper and 48 from the lower one."
		)
	if address in {31, 32, 33, 41, 42, 43, 51, 52, 53, 65}:
		notes += " The list prints no switch part number for this stand-up target, so its contact construction is not recorded."
	if address in {16, 17, 18}:
		notes += " The three trough microswitches sit under the playfield (the Ball Trough Switches page views them from below)."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = {13: "cabinet front", 34: "lockdown bar", 14: "cabinet interior", 21: "coin door", 22: "coin door"}[address]
	elif address == 24:
		extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
	kind = "constant" if address == 24 else "switch"
	if address == 24:
		notes += " The same part A-8630 as the Coin Door Closed switch; pinned wpc.c sets this matrix position closed at start-up (swMatrix[2] |= 0x08, 'Always closed switch'), so it is permanently active."
		extra["constant_active"] = True
		extra["initial_active"] = True
	else:
		extra["normally_closed"] = False
	if address == 22:
		extra["initial_active"] = True
		notes += " The retained script sets it closed at table start; it is closed while the coin door is closed."
	if address == 13:
		notes += " The lit Start button (lamp 88, Credit Button)."
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, ic = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address} ({ic}). {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, wire, connection, ic, switch_type, role, printed) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} ({ic})."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"roles": [role],
		}
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		physical: dict[str, Any] = {}
		if address == 117:
			notes += (
				" Not fitted: the Switch Matrix's Flipper Switches block prints F7 'Upper Left Flipper End of Stroke' (Blk-Gry J906-5), but the "
				"Fliptronic II board's connector list prints J906-5 'Not Used' and the flipper-circuit drawing heads that circuit 'UPPER LEFT (NOT "
				"USED)'. pinned br.c declares FLIP_SW(FLIP_L | FLIP_UR), so PinMAME never synthesizes it. The T.1 run drove it to 1: the "
				"switch grid marked it closed, but the ROM named no switch and drove no output."
			)
			physical["location"] = "not installed"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			refs += (UPPER_LEFT_SOURCE,)
			items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, "unused", refs, physical={**physical, "notes": notes}, **extra))
			continue
		physical["switch_type"] = switch_type
		extra["wiring"] = {"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection}
		extra["normally_closed"] = False
		if address == 118:
			notes += (
				" The left cabinet opto board's second opto: the Fliptronic II connector list prints J905-5 'Black-Blue, to left flipper button "
				"opto', and the Flipper Opto Switch Board page wires the left board's J1-2 'Black-Blue (upper flipper)' to J905-5, so the left "
				"flipper button breaks both of that board's beams. No upper left flipper is fitted (the flipper-circuit drawing heads it 'UPPER "
				"LEFT (NOT USED)', J902 and J907 carry no upper-left lines), and brGameData does not declare one. The T.1 run drove public 118 "
				"to 1: the switch grid marked it closed but the ROM named no switch and fired nothing, so the ROM gives the channel no function. "
				"A recreation may mirror the left button here; nothing requires it."
			)
			physical["location"] = "cabinet flipper button"
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			refs += (UPPER_LEFT_SOURCE,)
			physical["notes"] = notes
			items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, "optional", refs, physical=physical, **extra))
			continue
		if role.endswith(".button"):
			physical["location"] = "cabinet flipper button"
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			refs += (EDGES_SOURCE, VPX_SCRIPT_SOURCE)
			side = {112: "right", 114: "left", 116: "right"}[address]
			coils = {112: "45/46", 114: "47/48", 116: "33/34"}[address]
			notes += (
				f" One opto of the {side} cabinet Flipper Opto Switch Board A-15894 (two LED/photo-transistor pairs per board; the Fliptronic II "
				f"connector list prints {connection} '{wire}, to {side} flipper button opto'). This generation's WPC_FLIPPERS read returns the "
				"complement of the flipper switch column, so the public state is already normalized: public 1 is the pressed button and the "
				"contact the CPU sees is open at rest, so normally_closed is false whatever the beam does. The Switch Locations list's rows 11 "
				"and 12 print leaf-switch parts (SW-1A-192 / SW-1A-191) for the right and left flipper buttons; the board pages and the "
				"connector list, which describe this machine's Fliptronic wiring, are followed for the construction."
			)
			notes += f" The T.1 run set it to 1 and the ROM fired the flipper ({coils}) and named its synthesized end-of-stroke switch."
			if address == 116:
				notes += " It is the right board's second opto: the right cabinet button operates the lower right and the upper right flipper together."
		else:
			physical["location"] = "flipper assembly"
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			refs += (EDGES_SOURCE,)
			notes += (
				f" End-of-stroke switch of its flipper assembly ({wire} on {connection}). PinMAME synthesizes this address from the flipper "
				"coil state after the flip stroke time (brGameData declares FLIP_SOL for this flipper), so its public level is not a measurement of "
				"the physical contact and normally_closed records the Fliptronic grounded-switch convention (closed to ground only at end of stroke). "
				"The ROM's T.1 names it when the flipper fires."
			)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, "used", refs, **extra))
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country/option configuration bit)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC CPU board", "switch_type": "dip",
					"notes": "WPC CPU-board country/option DIP bank. The manual's front-matter jumper chart covers the EPROM and country jumpers, and no ON/OFF combination of this bank is asserted here.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Outputs -------------------------------------------------------------------------------------------
SOLENOID_NOTES = {
	1: "The Broadside popper: the D-11335-1 Ball Popper Assembly (AE-24-900 coil) at the top centre of the playfield kicks a ball resting on switch 55 up to the center habitrail, which returns it towards the flippers (IPDB calls it the Broadside VUK).",
	2: "Outhole Kicker Assembly A-8039-3: kicks a drained ball from the outhole (switch 15) into the trough.",
	3: "The cannon's 20 V motor (14-7965, item 13 of the A-14635 Cannon Assembly): while it runs the cannon sweeps from side to side, and the player fires when it points at the wanted target. The ROM's T.14 CANNON TEST toggles it: MOTOR = ON drives public 3. The manual prints no cannon position sensor and the switch matrix has no free cannon switch.",
	4: "Trough ball-release coil (B-9362-L-2 Coil & Bracket Assembly): releases a ball from the trough into the shooter lane.",
	5: "Right slingshot kicker arm (B-11203-R-1 coil and bracket); kick switch 38.",
	6: "Left slingshot kicker arm (B-11203-L-1 coil and bracket); kick switch 28.",
	7: "Knocker Assembly B-10686-1; the Locations list marks it '(Not Shown)'.",
	8: "The catapult coil (A-15016) of the A-14640 Catapult Assembly under the cannon: it fires the ball resting on switch 35 out through the cannon. The ROM's T.14 CANNON TEST fires it when public 35 closes.",
	9: "Kicks the locked balls out of Pirates' Cove (the lockup, switches 63 and 64); the manual's T.12 Cannon Test text says the test also activates 'the cannon kicker and left lockup coils'. The Locations list prints the same coil and bracket B-11203-R-1 as the right slingshot.",
	10: "Ramp Up coil (AE-26-1200 in B-9362-R-3) of the A-14918 Ramp Lifting Mechanism under the up/down ramp: it raises the ramp, opening Davy Jones' Locker so the next shot drops into the subway that loads the cannon.",
	11: "Ramp Down solenoid (SM1-29-1000-DC) of the A-14918 Ramp Lifting Mechanism: it lowers the up/down ramp again, closing switch 54.",
	12: "Printed 'Not Used' (driver Q52 with a wire colour but no part); the Locations list prints it Not Used and the ROM's T.4 walk skips it.",
	13: "Left jet bumper coil (A-12872-1 assembly); scoring switch 46. The retained script registers no callback: the table's Bumper object fires itself.",
	14: "Right jet bumper coil (A-12872-1 assembly); scoring switch 47. The retained script registers no callback.",
	15: "Bottom jet bumper coil (A-12842-3 assembly); scoring switch 48. The retained script registers no callback.",
	16: "Printed 'Not Used' (driver Q44 with a wire colour but no part); the Locations list prints it Not Used and the ROM's T.4 walk skips it.",
	17: "Left bottom flasher (24-8802 #906, no assembly number) with a backbox insert #906 on its second connection.",
	18: "Left top flasher (24-8704 #89 in A-8798) with a backbox insert #906.",
	19: "Right bottom flasher (24-8802 #906) with a backbox insert #906. The retained table's f19c, a Light with no bulb on the cannon toy that the script comments 'Cannon', is a glow helper and is not placed.",
	20: "Right top flasher (24-8704 #89 in A-8798) with a backbox insert #906.",
	21: "Right ramp flasher (24-8704 #89 in A-8798) with a backbox insert #906.",
	22: "Left ramp flasher (24-8704 #89 in A-8798) with a backbox insert #906. The retained table's f22c (a wide, raised glow) and f22e (a glow on the cannon toy) are helpers and are not placed.",
	23: "Locker Open flasher (A-12336-1 socket; the Locations list prints part 24-8704, the #89 number, beside a '#906' description) with a backbox insert #906. The table prints its type 'Low Power' where the other flasher rows print 'Flasher'.",
	24: "Left sword flasher (24-8802 #906 in A-12336-1) with a backbox insert #906. The table prints its type 'Low Power'.",
	25: "Top Popper flashers: the Locations list prints a count of (2) (24-8802 #906, C-13337), the table connects them to J123 only, and the drawing prints two balloons 25 without leaders above the playfield's top edge, either side of the Broadside popper, so the two bulbs are on the back panel behind the popper. The retained table models them only as six raised glow lights and its script drives them through SetLamp 125, so no table object is a bulb and no drawing leader ends on one: the device carries no placement.",
	26: "Cannon flashers: the Locations list prints a count of (2) (24-8802 #906, A-12336-1), and the drawing's two balloons 26 end at the lower left and lower right of the cannon's circle. The retained script drives them through SetLamp 126; its f26e is a glow on the cannon toy and is not placed.",
	27: "Fire Button flasher (24-8802 #906, A-12336-1) with a backbox insert #906: the bulb lights the Fire button on the lockdown bar, where the retained table puts its f27a/f27b lights (y about 1.03, below the playfield), and the drawing's balloon 27 sits at the playfield's front edge. Its f27c is a glow on the cannon toy.",
	28: "Right sword flasher (24-8802 #906 in A-12336-1) with a backbox insert #906.",
}
SOLENOID_ROLES = {7: "cabinet.knocker", 27: "cabinet.fire-button"}


def _solenoid_wiring(address: int) -> dict[str, Any]:
	printed_type, wire, connection, transistor, part = SOLENOID_TABLE[address]
	wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": transistor, "control_wire": wire}
	wiring["control_connection"] = SOLENOID_CONNECTIONS.get(address, connection)
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in FLIPPER_COILS:
			stage, voltage, control, transistors, supply_wire, control_wire, rom_name, rom_wires = FLIPPER_COILS[address]
			side = FLIPPER_SIDES[address]
			part, assembly = FLIPPER_PARTS[address]
			label = SOLENOID_LABELS[address]
			notes = (
				f"{side} flipper {stage} winding on the Fliptronic II board ({control}, {control_wire}; supply {voltage}, {supply_wire}). The "
				f"Solenoid/Flasher Table prints the flipper row's transistors as one pair, {transistors}, so which transistor drives which winding "
				f"is not printed. Coil {part} in assembly {assembly}. The ROM's T.12 FLIPPER COIL TEST names it \"{rom_name}\" with the wires "
				f"{rom_wires}"
			)
			notes += " and publishes the hold winding together with the power winding in that step." if stage == "power" else " and publishes it alone."
			callback = SOLENOID_CALLBACKS.get(address)
			notes += f" Retained script callback: {callback}." if callback else " The retained script registers no callback for it (UseSolenoids = 2 fast flips drive the flipper from the hold address)."
			wiring = {
				"board": "Fliptronic II controller board",
				"driver_transistor": transistors,
				"control_connection": control,
				"control_wire": control_wire,
				"power_connection": voltage,
				"power_wire": supply_wire,
			}
			identifier = output_id(label)
			spatial = located("solenoid", address, identifier, "effect")
			extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}], "physical": {"part_number": part, "assembly_part_number": assembly, "notes": notes}, "wiring": wiring}
			if spatial:
				extra["spatial"] = spatial
			refs = (MANUAL_SOURCE, FLIPPER_TEST_SOURCE, CORE_SOURCE) + ((VPX_SCRIPT_SOURCE,) if callback else ())
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		if address in SOLENOID_LABELS or address in NOT_USED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_USED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			if address in SOLENOID_TABLE:
				printed_type, wire, connection, transistor, part = SOLENOID_TABLE[address]
				notes = f"Printed solenoid table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire}, connection {connection})."
			else:
				notes = (
					"Upper left flipper position, not fitted: the flipper-circuit drawing heads the circuit 'UPPER LEFT (NOT USED)', the Fliptronic II "
					"connector list carries no upper-left J902 line and prints J907-1/2 'Not Used', and the Solenoid/Flasher Table and Locations list "
					"name only the lower left, lower right and upper right flippers. pinned br.c declares FLIP_SOL(FLIP_L | FLIP_UR), so PinMAME never "
					"publishes it, and the ROM's T.12 walk drives only 45-48, 33 and 34."
				)
				printed_type = part = None
			if address in SOLENOID_NOTES:
				notes += " " + SOLENOID_NOTES[address]
			if address in SOLENOID_CONNECTIONS:
				notes += (
					f" The Solenoid/Flasher Table prints connection {connection}; the Power Driver Board connector list prints J123-1 Sol 25, J123-2 "
					"Key, J123-3 Sol 26, J123-4 Sol 27 and J123-5 Sol 28, the solenoid wiring page draws the same pins and the table's Cannon Block "
					f"Diagram puts the cannon flasher on J123 pin 3, so the structured connection follows those ({SOLENOID_CONNECTIONS[address]}); "
					"the device and its address are not in doubt."
				)
			if address in BACKBOX_INSERT_FLASHERS and address <= 24:
				notes += (
					" The connector list brings it out to the playfield flashlamp on J126 and to the insert board flashlamp on J125, with the pins the "
					"table prints; the solenoid wiring page draws the J126 pins one higher from solenoid 18 on (it skips pin 2), a drawing quirk the "
					"connector list does not share."
				)
			if address in T4_NAMES:
				notes += f" T.4 SOLENOID TEST: the ROM pulses public {address} and prints \"{T4_NAMES[address]}\" with the wires {T4_WIRES[address]}."
			if address in T5_NAMES:
				notes += f" T.5 FLASHER TEST: the ROM pulses public {address} and prints \"{T5_NAMES[address]}\" with the wires {wire.upper().replace('ORG', 'ORN')} RED-WHT."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			elif fitted and address not in {5, 6, 13, 14, 15}:
				notes += " The retained script registers no callback for it."
			elif fitted:
				notes += " The retained script registers an empty callback: the table's own slingshot or bumper object fires it."
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address == 3 else "coil")
			physical: dict[str, Any] = {}
			if part and kind == "coil":
				physical["part_number"] = part
			if address == 3:
				physical["part_number"] = "14-7965"
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if address in FLASHER_SOLENOIDS:
				notes += f" Printed flashlamp type {part}; the Locations list prints '{FLASHER_LAMPS[address]}'."
				if address in FLASHER_COUNTS:
					physical["quantity"] = FLASHER_COUNTS[address]
				if address in BACKBOX_INSERT_FLASHERS:
					notes += " Only the playfield (or, for 27, lockdown-bar) bulb is this device's location; its backbox insert bulb is behind the translite."
			physical["notes"] = notes
			extra = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}], "physical": physical}
			if address in SOLENOID_TABLE:
				extra["wiring"] = _solenoid_wiring(address)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or (fitted and address in {5, 6, 13, 14, 15}):
				refs += (VPX_SCRIPT_SOURCE,)
			if address in T4_NAMES or address in {12, 16}:
				refs += (SOLENOID_TEST_SOURCE,)
			if address in T5_NAMES:
				refs += (FLASHER_NAMES_SOURCE,) + ((FLASHER_TEST_SOURCE,) if address == 19 else ())
			if address in {3, 8}:
				refs += (CANNON_TEST_SOURCE,)
			if address in {35, 36}:
				refs += (FLIPPER_TEST_SOURCE,)
			if address in {5, 6, 13, 14, 15}:
				refs += (EDGES_SOURCE,)
				notes = physical["notes"] + f" The T.1 run also saw the ROM fire it when its switch closed ({ {5: 38, 6: 28, 13: 46, 14: 47, 15: 48}[address] })."
				physical["notes"] = notes
			if not fitted:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				availability = "unused"
			elif address in SOLENOID_ROLES:
				extra["roles"] = [SOLENOID_ROLES[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				availability = "used"
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, identifier, role)
				if spatial:
					extra["spatial"] = spatial
			items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors WPC_GILAMPS bit 5 here when the driver sets no fast-flip RAM address; init_br calls no wpc_set_fastflip_addr (wpc.c: core_write_pwm_output of WPC_GILAMPS >> 5 at outputs 29-31). It is not a Black Rose playfield device.",
			30: "PinMAME mirrors WPC_GILAMPS bit 6 here under the same rule as 29; not a playfield device.",
			31: "PinMAME mirrors WPC_GILAMPS bit 7 here under the same rule as 29, the bit that drove the game-on relay before Fliptronics; no relay exists on this machine, and the harness runs found it active in the service menu. Not a playfield device.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
		}.get(address, "This WPC-Fliptronic generation has no integrated LPDC board, so pinned PinMAME's core_getSol serves the 37-44 range only for WPC-95 and System 11; this address is unused space." if 37 <= address <= 44 else (
			"PinMAME's simulator-only ball-shooter channel; Black Rose has a manual plunger and no ball-shooter coil." if address == 49 else "Reserved PinMAME output position before the first custom-output boundary; brGameData declares no custom solenoids."))
		items.append(
			_device(
				identifier, label, "virtual", SOLENOID_GROUP, address, availability, (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"],
				physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"quantity": 2 if address in DUAL_BULB_LAMPS else 1}
			if assembly != "---":
				physical["assembly_part_number"] = assembly
			notes = (
				f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description "
				f"\"{description}\"; the Lamp Matrix names it \"{LAMP_MATRIX_NAMES[address]}\"."
			)
			if bulb != "---":
				notes += f" Printed bulb {bulb}."
			notes += (
				f" The ROM's T.8 SINGLE LAMPS test lights public lamp {address} alone and names it \"{ROM_LAMP_NAMES[address]}\" with the wires "
				f"RED-{ROM_LAMP_ROW_WIRES[row]} YEL-{ROM_LAMP_COLUMN_WIRES[column]}."
			)
			if "(R)" in ROM_LAMP_NAMES[address]:
				notes += " The frame clips the leading R at the display edge; (R) marks the letter it cuts off."
			if address in DUAL_BULB_LAMPS:
				notes += f" Two bulbs: the Lamp Locations list prints {DUAL_BULB_LAMPS[address]}."
			if address in {58, 65}:
				notes += " Both 58 and 65 are printed 'Bottom Standup Jewel' on both lamp pages and named BOT. STNDUP JEWEL by the ROM; they are two inserts, told apart here by address."
			if address in BACKBOX_LAMPS:
				column_pin, row_pin = BACKBOX_LAMPS[address]
				notes += (
					f" A backbox insert lamp: the Lamp Locations list prints no assembly for it, the lamp drawing prints no balloon for it, and the "
					f"Power Driver Board connector list brings its column and row out to the insert lamps ({column_pin}, {row_pin}) rather than only to "
					"the playfield. The retained script leaves it unassigned (commented 'Insert Left??' / 'Insert Right??')."
				)
			if address in CABINET_LAMPS:
				notes += " The lamp in the lit Start (Credit) button, assembly 20-9663-7: the connector list brings column 8 and row 8 out to the cabinet lamp (J136-3, J134-9). The retained script leaves it unassigned."
			if address == 17:
				notes += " The retained table's light for it is named L17 (capital L)."
			if address in SWORD_LAMPS:
				notes += (
					" One of the jet-lane sword's inserts (12-17 from the top). The factory lamp drawing numbers the sword's four lower inserts 17, "
					"16, 15, 14 from the top, the reverse of the retained table's lights; IPDB playfield photos show the legends 8K at the top, 1K "
					"just above the guard, then the red jewel and a triangle printed COMBO at the bottom, which with the lamp names (12 Jet Enter 8K "
					"... 15 Jet Enter 1K, 16 Jet Enter Jewel, 17 Combo Shot Right) puts the lamps in the table's order. The placement follows the "
					"table and is not checked against the drawing's reversed numbers, so it stays observed."
				)
			physical["notes"] = notes
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"physical": physical,
				"wiring": {
					"board": "WPC power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			refs: tuple[str, ...] = (MANUAL_SOURCE, LAMP_TEST_SOURCE, CORE_SOURCE)
			if address in BACKBOX_LAMPS:
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in CABINET_LAMPS:
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				refs += (VPX_SCRIPT_SOURCE,) + ((PHOTO_SOURCE,) if address in SWORD_LAMPS else ())
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", LAMP_GROUP, address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (printed, wire, connection, feed, transistor, bulbs, rom_name, rom_wires) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination circuit {address + 1:02d} '{printed}'; printed bulbs {bulbs}, return wire {wire} on {connection}, "
			f"driver {transistor}. The ROM's T.6 GENERAL ILLUMINATION test lights public GI {address} alone and names it \"{rom_name}\" "
			f"({rom_wires})."
		)
		wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": transistor, "control_connection": connection, "control_wire": wire}
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}], "wiring": wiring}
		refs: tuple[str, ...] = (MANUAL_SOURCE, GI_TEST_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		if address <= 2:
			notes += (
				f" The Power Driver Board connector list prints its return {connection} and feed {feed} as going 'to insert board', while the "
				"Solenoid/Flasher Table and Locations list name it a playfield string, print #44 and #555 bulbs for it where the two insert "
				"strings print #555 only, and the ROM names it a playfield circuit; the connector list alone disagrees, so the table's playfield "
				"classification is followed. The retained table's GIUpdates drives a per-string collection of playfield Light objects for it, whose "
				"grouping is the table author's: the placements are those lights with co-located render doubles collapsed and the jet-bumper glow "
				"helpers left out, kept observed and without a quantity because the manual prints no per-string bulb count and no drawing locates GI bulbs."
			)
			spatial = located("gi", address, identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
		else:
			notes += (
				f" Backbox illumination behind the translite, matching the table's 'Insert' name and the connector list's 'to insert' lines "
				f"(return {connection}, {feed}). The retained script drives only backglass bulbs for it."
			)
			if address == 4:
				notes += " The connector list also brings the 6.8 VAC G.I. to the coin door on J119 (J119-1 White-Violet, return J119-3 Violet), the colour of this string."
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		extra["physical"] = {"notes": notes}
		items.append(_device(identifier, GI_LABELS[address], "gi", GI_GROUP, address, "used", refs, **extra))
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
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		}
	]


# --- Mechanisms, drivers and conflicts -------------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _mechanism(
	suffix: str,
	label: str,
	kind: str,
	actuators: list[str],
	sensors: list[str],
	behavior: str,
	refs: tuple[str, ...],
	positions: list[tuple[str, str, list[str], str]] | None = None,
	assembly: str | None = None,
	status: str = "observed",
) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}",
		"label": label,
		"kind": kind,
		"actuators": actuators,
		"sensors": sensors,
		"behavior": behavior,
		"provenance": provenance(status, *refs),
	}
	if assembly:
		record["assembly_part_number"] = assembly
	if positions:
		record["positions"] = [
			{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
			for position_id, position_label, position_sensors, description in positions
		]
	return record


def _matrix(*addresses: int) -> list[str]:
	return [f"switch.matrix-{address}" for address in addresses]


def mechanisms() -> list[dict[str, Any]]:
	flipper_refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE)
	return [
		_mechanism(
			"cannon",
			"Ball cannon",
			"motorized",
			[_coil(3), _coil(8)],
			_matrix(35, 66),
			"The A-14635 Cannon Assembly sits in the lower centre of the playfield, between the slingshots. A ball shot into the opened "
			"Davy Jones' Locker drops into a subway under the playfield (switch 61 at its top, 66 at its bottom) and rolls into the cannon's "
			"catapult (the A-14640 Catapult Assembly), where it closes the cannon kicker switch 35. With a ball loaded the 20 V cannon motor "
			"(solenoid 3, 14-7965) sweeps the cannon from side to side, the Fire button on the lockdown bar (switch 34) flashes, and pressing "
			"it fires the catapult coil (solenoid 8, A-15016), which shoots the ball out of the cannon at whatever the cannon points at: the "
			"jewel and treasure targets for awards and SINK SHIP letters (game rules). The manual's T.12 Cannon Test text (T.14 on the L-4 ROM) "
			"says the cannon should reach from the far left shot (the lockup) to the far right shot (the jets), and the ROM's T.14 shows SW.35 "
			"CANNON = CLOSED at public 1 and fires 8 on the closure; MOTOR = ON drives 3. The manual prints no cannon position sensor and the "
			"switch matrix has no free cannon switch: the motor sweeps the cannon and the player times the shot (the rules say to press Fire "
			"when the cannon is aimed at the desired target); how the ROM tracks the cannon's aim, if at all, is not documented. Pinned br.c's simulator writes a direction "
			"bit to the unused matrix position 77 and marks it 'FAKE!, Not used in the Pin'. The retained script models the sweep as a disc "
			"rotating between -45 and +45 degrees while solenoid 3 is on, creates the ball at its CannonKicker and kicks it along the disc "
			"angle when 8 fires with 35 set. The Cannon Flashers (solenoid 26, two bulbs) light the cannon and the Fire Button flasher (27) "
			"lights the button. The manual's maintenance pages give a cannon level adjustment and the reinforcing clips of its mounting ring.",
			(MANUAL_SOURCE, IDENTITY_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, CANNON_TEST_SOURCE, SOLENOID_TEST_SOURCE),
			[
				("loaded", "Ball loaded", _matrix(35), "A ball rests in the catapult and holds switch 35 closed; the ROM may fire solenoid 8."),
				("subway", "Subway feed", _matrix(61, 66), "A ball dropped into the locker passes subway switches 61 and 66 on its way to the catapult."),
			],
			"A-14635",
		),
		_mechanism(
			"davy-jones-locker-ramp",
			"Up/down ramp (Davy Jones' Locker)",
			"diverter",
			[_coil(10), _coil(11)],
			_matrix(54),
			"The A-14918 Ramp Lifting Mechanism moves the up/down ramp (the A-14831 Lift Ramp Assembly on the Ramp Locations page) between two "
			"positions: the Ramp Up coil (solenoid 10, AE-26-1200 in B-9362-R-3) raises it and the Ramp Down solenoid (11, SM1-29-1000-DC) "
			"lowers it again, through the A-14870 lift crank. The only feedback is switch 54, which the manual's error messages say must be "
			"'definitely closed when the ramp is down, and positively open when the ramp is up'; the ROM reports 'Warning Ramp Open/Closed Not "
			"Reliable' and, after three failed tries in a row, 'Error-Ramp not opening/closing-check sw./CL.'. IPDB describes it as a left ramp "
			"'raised at certain times to load the ball cannon': raised, it opens Davy Jones' Locker so the next shot drops into the subway "
			"(61, 66) that loads the cannon; lowered, the shot rides the ramp. The game opens the locker on the skill shot, on completing the "
			"three 3-banks, on consecutive ramp shots from the side flipper or on the 3-bank rebound (game rules). The ROM's T.4 names 10 RAMP "
			"UP and 11 RAMP DOWN and T.1 names 54 RAMP DOWN. The retained script sets 54 from the solenoid callbacks and swaps two ramp "
			"surfaces, so its timing is the table author's.",
			(MANUAL_SOURCE, IDENTITY_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("down", "Ramp down (locker closed)", _matrix(54), "Switch 54 is closed; the ramp shot rides the ramp."),
				("up", "Ramp up (locker open)", [], "Switch 54 is open; the next ramp shot drops into the locker and the subway to the cannon."),
			],
			"A-14918",
		),
		_mechanism(
			"pirates-cove-lockup",
			"Pirates' Cove lockup",
			"kicker",
			[_coil(9)],
			_matrix(71, 63, 64),
			"A two-ball lock: a ball enters past the Lockup Enter switch (71) and stops at Lockup 1 (63) or, with one ball already held, at "
			"Lockup 2 (64); the Left Ball Lockup coil (solenoid 9, B-11203-R-1 coil and bracket) kicks the held balls back out. Locking a ball "
			"while LOCK 1 flashes starts 2-ball multiball, and locking both during 2-ball multiball starts 3-ball multiball (game rules). The "
			"ROM's T.4 names 9 BALL LOCKUP and T.1 names 71 LOCKUP ENTER, 63 LOCKUP 1 and 64 LOCKUP 2; pinned br.c's simulator moves a ball "
			"past 71 and 64 to rest on 63, where 9 kicks it. The retained script kicks both kickers from the one callback and animates a hammer.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("lock-1", "Lockup 1", _matrix(63), "First held ball."),
				("lock-2", "Lockup 2", _matrix(64), "Second held ball."),
			],
			"B-11203-R-1",
		),
		_mechanism(
			"broadside-popper",
			"Broadside popper",
			"kicker",
			[_coil(1)],
			_matrix(55),
			"The D-11335-1 Ball Popper Assembly (AE-24-900 coil, A-11336 armature, 03-8053 cap) at the top centre of the playfield: a ball "
			"shot into the Broadside hole rests on switch 55 and solenoid 1 kicks it straight up onto the center habitrail, which returns it "
			"towards the flippers (IPDB: 'The Broadside VUK kicks the ball to the center habitrail'). The two Top Popper flashers (solenoid 25) "
			"sit behind it. The ROM's T.4 names 1 BALL POPPER and T.1 names 55 BALL POPPER.",
			(MANUAL_SOURCE, IDENTITY_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			None,
			"D-11335-1",
		),
		_mechanism(
			"ball-trough",
			"Outhole and ball trough",
			"kicker",
			[_coil(2), _coil(4)],
			_matrix(15, 18, 17, 16),
			"A drained ball rolls into the outhole (switch 15), where the Outhole Kicker Assembly A-8039-3 (solenoid 2) kicks it into the "
			"ball trough under the apron; three trough microswitches count the balls held (18 Left nearest the outhole, 17 Center, 16 Right "
			"at the release end), and the ball-release coil (solenoid 4) releases one into the shooter lane. The machine plays with three balls. "
			"The retained script models it as a cvpmTrough of three with entry switch 15 and solenoids 2 (in) and 4 (out).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("outhole", "Outhole", _matrix(15), "Drained-ball catch position."),
				("trough-left", "Trough, left", _matrix(18), "Trough position nearest the outhole."),
				("trough-center", "Trough, center", _matrix(17), "Middle trough position."),
				("trough-right", "Trough, right", _matrix(16), "Release end of the trough, next to the shooter lane."),
			],
			"A-8039-3",
		),
		_mechanism(
			"shooter-lane",
			"Shooter lane and manual plunger",
			"other",
			[],
			_matrix(25),
			"A manual ball shooter (the manual's Game Control Locations drawing labels the 'Ball Shooter Assy.'): the ball released by "
			"solenoid 4 waits on the shooter-lane switch 25 and the player plunges it; plunging the lower 3-bank targets at the start of a ball "
			"is the skill shot that opens Davy Jones' Locker. The retained script's plunger key also writes the Fire button (34).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE),
			None,
		),
		_mechanism(
			"lower-right-flipper",
			"Lower right flipper",
			"other",
			[_coil(45), _coil(46)],
			["switch.generic-111", "switch.generic-112"],
			"Fliptronic II flipper assembly A-14876-R-3 with an FL-11629 (blue) coil whose power and hold windings are public 45 and 46, and an "
			"end-of-stroke switch (F1, public 111). The cabinet button is the right Flipper Opto Switch Board's first opto (F2, public 112). "
			"PinMAME synthesizes the end-of-stroke bit; the T.1 run showed the ROM firing the flipper when 112 was set to 1.",
			flipper_refs,
			None,
			"A-14876-R-3",
		),
		_mechanism(
			"lower-left-flipper",
			"Lower left flipper",
			"other",
			[_coil(47), _coil(48)],
			["switch.generic-113", "switch.generic-114"],
			"Fliptronic II flipper assembly A-14876-L-3 with an FL-11629 (blue) coil (public 47 power, 48 hold) and an end-of-stroke switch "
			"(F3, public 113). The cabinet button is the left Flipper Opto Switch Board's first opto (F4, public 114).",
			flipper_refs,
			None,
			"A-14876-L-3",
		),
		_mechanism(
			"upper-right-flipper",
			"Upper right (side) flipper",
			"other",
			[_coil(33), _coil(34)],
			["switch.generic-115", "switch.generic-116"],
			"The side flipper on the right of the playfield: Fliptronic II flipper assembly A-15205-R-3 with an FL-11630 (red) coil (public 33 "
			"power, 34 hold) and an end-of-stroke switch (F5, public 115). Its cabinet input is the right opto board's second opto (F6, public "
			"116), so the right flipper button works both right flippers. The game rules build combination shots from it ('Side Flipper/Left "
			"Flipper Combination') and use it to load the cannon. There is no upper left flipper: F7, F8 and 35/36 have nothing fitted, though "
			"the left opto board's second opto is still wired to F8.",
			flipper_refs,
			None,
			"A-15205-R-3",
		),
		_mechanism(
			"slingshots",
			"Slingshots",
			"kicker",
			[_coil(6), _coil(5)],
			_matrix(28, 38),
			"Two kicker-arm slingshots, each with a leaf kick switch (28 left, 38 right; SW-A1-120 / SW-1A-120 printed) and a coil (solenoids 6 "
			"and 5, B-11203-L-1 / B-11203-R-1). Even in T.1 the ROM fires the matching coil when a kick switch closes.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			None,
			"B-11700-1",
		),
		_mechanism(
			"jet-bumpers",
			"Jet bumpers",
			"other",
			[_coil(13), _coil(14), _coil(15)],
			_matrix(46, 47, 48),
			"Three jet bumpers in the upper right, two above (left, switch 46 / coil 13, and right, 47 / 14; A-12872-1 assemblies) and one "
			"below them (bottom, 48 / 15; A-12842-3), entered past switch 58 and left past 57. Even in T.1 the ROM fires each bumper's coil "
			"when its switch closes. The jet bumper lane (12-16) and the right rollover to the jets advance the jet values (game rules).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			None,
			"A-12872-1",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return []


def drivers() -> list[dict[str, Any]]:
	by_id = {item["id"]: item for item in load_json(ROOT / "catalog/pinmame.json")["drivers"]}
	result = []
	for driver_id in DRIVER_IDS:
		item = {key: value for key, value in by_id[driver_id].items() if key in {"id", "clone_of", "description", "year", "manufacturer", "flags"}}
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		result.append(item)
	return result


# --- Sources -------------------------------------------------------------------------------------------
MANUAL_NAME = "Bally_1992_Black_Rose_Manual.pdf"
TABLE_NAME = "Black Rose (Bally 1992) VPW v1.4.vpx"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/bally.black-rose.1992/ipdb-313"
IPDB_WAYBACK = "https://web.archive.org/web/20251221222245id_/https://www.ipdb.org/machine.cgi?id=313"
MANUAL_WAYBACK = "https://web.archive.org/web/20250907095912id_/https://www.ipdb.org/files/313/" + MANUAL_NAME
RIGHTS_NOTE = "Bally/Midway; scan hosted by the Internet Pinball Machine Database"
EXCERPT_CREDIT = "curator, read from the rendered page"
DERIVATIONS = {
	"switch-locations": ("100", "0.05,0.05,0.97,0.93", 495, 300, None, "2347x2901"),
	"lamp-locations": ("99", "0.05,0.05,0.97,0.93", 490, 300, None, "2347x2901"),
	"solenoid-flasher-locations": ("101", "0.05,0.05,0.97,0.93", 500, 300, None, "2347x2901"),
	"lamp-matrix": ("106", "0.03,0.04,0.93,0.5", 525, 131, 1000, "1001x661"),
	"switch-matrix": ("107", "0.03,0.08,0.97,0.5", 530, 131, 1050, "1051x607"),
	"solenoid-flasher-table": ("109", "0.07,0.04,0.93,0.68", 540, 97, 710, "711x684"),
	"solenoid-wiring": ("112", "0.03,0.04,0.97,0.93", 555, 163, 1300, "1301x1591"),
	"fliptronic-and-flipper-wiring": ("116", "0.05,0.06,0.97,0.96", 575, 156, 1220, "1221x1543"),
	"power-driver-board-connectors": ("118", "0.05,0.06,0.55,0.93", 585, 160, 680, "680x1530"),
}


def _derivation(name: str) -> str:
	page, box, xref, dpi, capped, size = DERIVATIONS[name]
	cap = f", capped to {capped}px wide" if capped else ""
	return (
		f"{MANUAL_NAME} page {page}, crop box {box}, scanned page rendered at its native resolution (embedded image xref {xref}, "
		f"2550px across 8.50in), rendered at {dpi} dpi{cap}, grayscale, {size} WebP quality 80"
	)


def _excerpt(name: str, locator: str, *, image: bool = False, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.black-rose.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = _derivation(name)
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	partial = "transcribed from the rendered page; the curator checked the lines this definition uses against the render"
	ocr = "Windows OCR with obvious character errors corrected against the rendered pages"
	return [
		_excerpt("switch-locations", "PDF page 100, printed 2-42, Switch Locations parts list and playfield drawing", image=True),
		_excerpt("lamp-locations", "PDF page 99, printed 2-41, Lamp Locations parts list and playfield drawing", image=True),
		_excerpt("solenoid-flasher-locations", "PDF page 101, printed 2-43, Solenoid/Flasher Locations parts list and playfield drawing", image=True),
		_excerpt("switch-matrix", "PDF page 107, printed 3-3, Switch Matrix with the dedicated and flipper grounded-switch blocks", image=True),
		_excerpt("lamp-matrix", "PDF page 106, printed 3-2, Lamp Matrix wiring table (reprinted on PDF page 141)", image=True),
		_excerpt("solenoid-flasher-table", "PDF page 109, printed 3-5, Solenoid/Flasher Table with the general-illumination and flipper rows and the Cannon Block Diagram (reprinted on PDF page 2)", image=True),
		_excerpt("solenoid-wiring", "PDF page 112, printed 3-8, Solenoid Wiring drawing", image=True, reviewed=False, credit=partial),
		_excerpt("power-driver-board-connectors", "PDF pages 117-119, printed 3-13 to 3-15, Power Driver Board A-12697-1 connector list (image: page 118, the G.I., flasher and lamp connectors)", image=True, reviewed=False, credit=partial),
		_excerpt("fliptronic-and-flipper-wiring", "PDF pages 113, 116 and 123, printed 3-9, 3-12 and 3-19, flipper circuits, Flipper Opto Switch Board A-15894 and the Fliptronic II board connector list (image: page 116)", image=True, reviewed=False, credit=partial),
		_excerpt("cpu-and-coin-door-connectors", "PDF pages 120 and 124, printed 3-16 and 3-20, CPU board and coin door interface board connector lists", reviewed=False, credit=partial),
		_excerpt("mechanism-assemblies", "PDF pages 3-4, 19, 74-90, 98 and 103, contents, ROM summary and mechanism parts pages", method="mixed", reviewed=False, credit=ocr),
		_excerpt("game-rules", "PDF pages 5-17, the rules and playfield shot maps", method="mixed", reviewed=False, credit=ocr),
		_excerpt("service-tests", "PDF pages 22, 30-32 and 52-57, game control locations, test menu, error messages and maintenance", method="mixed", reviewed=False, credit=ocr),
	]


def _runtime(source_id: str, filename: str, scenario: str, locator: str, revision: str = PINMAME_REVISION) -> dict[str, Any]:
	return {
		"id": source_id,
		"kind": "runtime_scenario",
		"uri": f"internal:{EVIDENCE_DIRECTORY}/{filename}",
		"revision": revision,
		"locator": f"One hash-pinned LibPinMAME harness run of br_l4 from empty NVRAM with built-in mechanisms disabled (scenario tools/harness-scenarios/wpc-fliptronic/{scenario}.json). {locator}",
		"license": "NOASSERTION",
		"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the br_* clone tree (br_l4, br_d4, br_l3, br_d3, br_l1, br_d1, br_p17, br_p18)",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/br.c brGameData with GEN_WPCFLIPTRON, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_UR) | FLIP_SOL(FLIP_L | FLIP_UR) "
				"(lower flippers and the upper right one), an all-zero inverted-switch mask, no custom solenoids and no wpc_set_fastflip_addr call "
				"in init_br, so wpc.c mirrors WPC_GILAMPS bits 5-7 at solenoids 29-31; br.c's simulator #defines (swCannonDir 77 marked 'FAKE!, "
				"Not used in the Pin') and its br_handleMech, which only the built-in simulator uses; src/wpc/wpc.c sets the always-closed switch "
				"24 at start-up (swMatrix[2] |= 0x08); src/wpc/core.h CORE_FIRSTCUSTSOL=51 and CORE_FIRSTUFLIPSOL=33; src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WPCFLIPTRON=0x8. The runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-fliptronic.json",
			"revision": "repository",
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp and five-GI address rules, including the no-LPDC 37-44 unused range and the Fliptronic flipper block",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=313",
			"revision": "Wayback capture 2025-12-21T22:22:45Z",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-09T19:54:00Z",
			"locator": (
				"IPDB machine 313 'Black Rose' (Midway/Bally, July 1992, model 20013, Williams WPC Fliptronics 2, 4 players, 3,746 units). IPDB "
				f"is Cloudflare-gated, so the page was read from the raw Wayback capture {IPDB_WAYBACK} (retained as ipdb-313-page-wayback.html). "
				"The title, manufacturer, date and model number match the manual's cover (August 1992, 16-20013-101) and the machine being curated."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors",
			"excerpts": [
				_excerpt("ipdb-page", f"IPDB machine 313 page, Wayback capture {IPDB_WAYBACK}", reviewed=False, credit="curator, read from the retained HTML"),
			],
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}",
			"original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-09T19:55:00Z",
			"locator": (
				"Image-only 300 dpi scan of the Bally Black Rose operations manual 16-20013-101 (August 1992), 142 pages. The PDF has no text layer; "
				"every table was read from a rendered page and a Windows OCR pass was used only to find pages. PDF 99-101 (printed 2-41 to 2-43) carry "
				"the lamp, switch and solenoid/flasher location lists, PDF 106-109 (3-2 to 3-5) the lamp matrix, switch matrix and solenoid/flasher "
				"table, PDF 112-116 (3-8 to 3-12) the solenoid wiring, flipper circuits and flipper opto board, PDF 117-124 (3-13 to 3-20) the board "
				"connector lists, PDF 30-32 the test menu and PDF 52-57 the error messages and maintenance. PDF 2 and 141 reprint the solenoid table "
				f"and the matrices. Direct resource: {MANUAL_WAYBACK}."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/black-rose-1992/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME,
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW v1.4 recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT}. Geometry authority only for named "
				"table objects the script binds; the trough, the ramp-lift coils and the Ramp Down switch have no table object."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/black-rose-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW v1.4 script (150,060 bytes). Runtime and mechanism-causality authority: Const cGameName = "br_l4", Const '
				"UseSolenoids = 2 (fast flips), HandleMechanics = 0, the cvpmTrough (switches 16-18, entry 15, solenoids 2 and 4), the "
				"SolCallback/SolModCallback table, the cannon (CannonMotor, FireCannon, sw66_Sub_Hit), the up/down ramp (RampUp, RampDown, switch "
				"54), the Pirates' Cove kickers and the Lampz light assignments."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment script line that binds the controller, with its line number", credit="curator, quoted from the script file")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/black-rose-1992/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		_runtime(EDGES_SOURCE, "black-rose-br_l4-switch-edges.json", "br-switch-edges",
			"It opens T.1 SWITCH EDGES and drives every fitted playfield and cabinet switch except 13, 21, 22 and 24, and the Fliptronic buttons "
			"112, 114 and 116, to 1 and back to 0. The ROM names each switch with its wires while its public level is 1 and clears the name at 0, "
			"fires the sling and jet coils from their switches and the flippers from their buttons."),
		_runtime(UPPER_LEFT_SOURCE, "black-rose-br_l4-switch-edges-upper-left.json", "br-switch-edges-upper-left",
			"It drives public 118 and 117, the Fliptronic positions of the unfitted upper left flipper, to 1 and back in T.1: the switch grid "
			"marks each closed, but the ROM names no switch and drives no output."),
		_runtime(SOLENOID_TEST_SOURCE, "black-rose-br_l4-solenoid-test.json", "br-solenoid-test",
			"It steps T.4 SOLENOID TEST in repeat mode: the ROM names and pulses 1-11, 13, 14 and 15 in turn with their wires, skips 12 and 16, "
			"and wraps."),
		_runtime(FLASHER_NAMES_SOURCE, "black-rose-br_l4-flasher-test-names.json", "br-flasher-test-names",
			"It steps T.5 FLASHER TEST in repeat mode: the ROM names and pulses 17-28 in turn with their wires and wraps."),
		_runtime(FLASHER_TEST_SOURCE, "black-rose-br_l4-flasher-test.json", "br-flasher-test",
			"An earlier run on a library built from 8371478a that steps T.5 FLASHER TEST through flashers 17-28 with output checkpoints; at step 19 "
			"the ROM pulses public solenoid 19 and prints RIGHT BOTTOM with the wires BLK-ORN RED-WHT.", revision="8371478a7640f1896dcdf565aed340dc5df989ba"),
		_runtime(GI_TEST_SOURCE, "black-rose-br_l4-gi-test.json", "br-gi-test",
			"It steps T.6 GENERAL ILLUMINATION: after ALL ILLUMINATION the ROM lights public GI 0-4 alone in turn and names each circuit with its wires."),
		_runtime(LAMP_TEST_SOURCE, "black-rose-br_l4-single-lamps.json", "br-single-lamps",
			"It steps T.8 SINGLE LAMPS through all 64 lamps: the ROM lights each public lamp 11-88 alone in matrix order and names it with its wires."),
		_runtime(FLIPPER_TEST_SOURCE, "black-rose-br_l4-flipper-coil-test.json", "br-flipper-coil-test",
			"It steps the L-4 ROM's T.12 FLIPPER COIL TEST: the ROM names and drives the right, left and upper right flipper windings (45/46, 47/48, "
			"33/34) with their wires, never 35/36, and wraps."),
		_runtime(CANNON_TEST_SOURCE, "black-rose-br_l4-cannon-test.json", "br-cannon-test",
			"It opens the L-4 ROM's T.14 CANNON TEST: SW.35 CANNON reads CLOSED at public 1 and OPEN at 0 and the ROM fires the cannon kicker (8) on "
			"the closure; toggling the motor drives public 3."),
		{
			"id": PHOTO_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=313",
			"revision": "IPDB gallery images 14298 and 23355, Wayback raw captures",
			"acquired_at": "2026-10-09T21:40:00Z",
			"locator": (
				"Two IPDB playfield photos (images/313/image-19.jpg 'Playfield' and image-8.jpg 'Upper Playfield'), retained under the manuals "
				"root's ipdb-313/photos with their SHA-256 and not committed. Read only for the legends of the jet-lane sword's inserts, which "
				"settle the order of lamps 12-17 against the factory lamp drawing's reversed balloon numbers."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors and the photographers credited on IPDB",
			"excerpts": [
				_excerpt("ipdb-playfield-photos", "IPDB machine 313 images 14298 and 23355, the jet-lane sword inserts", reviewed=True, credit="curator, read from the retained photos"),
			],
		},
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:tools/seeds/bally/black-rose-1992-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of PDF 99, 100 and 101 (printed 2-41 to 2-43): every callout transcribed "
				"independently on the committed 300 dpi crops, per-page control and callout fits; a table placement whose own callout lands within "
				"0.07 normalized under both fits is validated (tools/drawing_callouts.py), and six placements with no usable table object are "
				"measured on the drawings. Reads, overlays and generator are retained under review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "PinMAME game definitions contributors",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Black Rose",
			"manufacturer": "Bally",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 313,
			"opdb_id": "G5vZd-MQpWZ",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "variant_differences"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "observed",
				"variant_coverage": "observed",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
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
		"knowledge": {"path": "knowledge/bally/black-rose-1992.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Black Rose device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Black Rose mechanism {mechanism['id']} names unknown devices: {unknown}")
	drawing_callouts.apply_to_definition(definition, _callout_seed(), CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device["availability"] in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	seed = _callout_seed()
	check = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/black-rose-1992/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/black-rose-1992-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "Exact VPX collision object the retained script binds to the matrix switch (trigger, target, kicker, gate, bumper or slingshot wall), observed, and validated where the factory drawing's own callout agrees within the limit. The trough switches 16-18 and the Ramp Down switch 54 have no table object and are measured on the switch drawing; the cannon kicker switch 35 uses the cannon's CannonKicker kicker.",
			"lamp": "Exact VPX Light centre for each lamp's playfield bulb, observed, validated where the lamp drawing's callout agrees; 11 and 86 place both of their bulbs. The backbox insert lamps 78 and 87 and the Credit button lamp 88 are controlled not-applicable records.",
			"solenoid": "Named VPX mechanism anchor or visible effect object for each coil, and the script-driven bulb Light for each flasher with render doubles collapsed, observed, validated where the solenoid/flasher drawing's own callout agrees; the ramp-lift coils 10 and 11 have no table object and are measured on the drawing. Flipper windings print no callout and keep their table placements observed. The cannon motor (3) and the lockup coil (9) project onto the cannon disc and the first lockup kicker.",
			"gi": "Per-string collections of table GI lights for the three playfield strings, collapsed where bulbs are stacked and without the jet-bumper glow helpers, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs.",
		},
		"unresolved_geometry": [
			"The general-illumination bulb coordinates of the three playfield strings rest on the retained table's own grouping; no factory drawing or bulb count locates them, so their placements stay observed and spatial_placement stays in coverage.missing.",
			"The two Top Popper flashers (solenoid 25) sit on the back panel behind the Broadside popper; the drawing prints their balloons without leaders above the playfield's top edge and the table models them only as glow lights, so solenoid 25 has no placement.",
			"Hidden mechanism parts (the trough switches, the ramp-lift coils and the Ramp Down switch, the cannon motor and its catapult) are placed at the mechanism they belong to, not at a measured contact centre.",
		],
		"promotion_decision": "partial: every used device has a placement or a controlled not-applicable record except the Top Popper flashers, and the factory drawings validate most table placements, but the general-illumination bulbs cannot be validated from any retained drawing or count.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Black Rose (Bally, 1992) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT} rounded to at most six places "
		"(factory-drawing measurements to three).",
		"",
		"## Placement status",
		"",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(report['without_placements'])}",
		"",
		"## Projection classes",
		"",
	]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	lines += [
		"",
		"## Drawing callout check",
		"",
		f"{check['rule']} It validates {check['validated']} of the {check['checked']} table placements it checks "
		f"([seed](../../../{check['seed']})); the rest keep their observed status:",
		"",
	]
	for placement_id, item in check["not_validated"].items():
		if "control_offset" in item:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {max(item['control_offset'], item['callout_offset']):.3f} normalized away.")
		else:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {item['reason']}.")
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Black Rose artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Black Rose author-ready artifact: {AUTHOR_READY_PATH}")
	definition = build()
	report = build_spatial_report(definition)
	expected = (
		(PARTIAL_PATH, canonical_bytes(definition)),
		(SPATIAL_REPORT_PATH, canonical_bytes(report)),
		(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report).encode("utf-8")),
		(KNOWLEDGE_PATH, KNOWLEDGE_SEED_PATH.read_bytes()),
	)
	for path, content in expected:
		if not path.is_file() or path.read_bytes() != content:
			raise RuntimeError(f"Black Rose deterministic artifact drift: {path}")
	print("Black Rose definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Black Rose extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Black Rose retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
