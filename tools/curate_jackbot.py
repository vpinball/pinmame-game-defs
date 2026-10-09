"""Curate the physical Williams Jack*Bot (1995) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and
runtime-derived fact as a literal and reads two committed seeds (the table-derived placements and the
factory-drawing callout check), so regeneration reproduces the canonical artifact byte-for-byte without
reading the external evidence roots.  ``--check`` refuses drift, and ``--regenerate`` is the only path that
writes the definition, its knowledge note and its spatial report.
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

MACHINE_ID = "williams.jackbot.1995"
PARTIAL_PATH = ROOT / "machines/partial/williams/jackbot-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/jackbot-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/jackbot-1995.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/williams/jackbot-1995.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/williams/jackbot-1995-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/williams/jackbot-1995-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/jackbot-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/jackbot-1995.md"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
IDENTITY_SOURCE = "identity.williams.jackbot.1995"
MANUAL_SOURCE = "manual.williams.jackbot.1995"
BULLETIN_SOURCE = "service-bulletin-86.williams.jackbot.1995"
VPX_TABLE_SOURCE = "vpx-table.jackbot-bord-1-1-2a"
VPX_SCRIPT_SOURCE = "vpx-script.jackbot-bord-1-1-2a"
VPX_EXTRACTION_SOURCE = "vpx-extraction.jackbot-bord-1-1-2a"
EDGES_SOURCE = "runtime.jackbot.switch-edges-sweep"
SOLENOID_TEST_SOURCE = "runtime.jackbot.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.jackbot.flasher-test"
FLIPPER_TEST_SOURCE = "runtime.jackbot.flipper-coil-test"
GI_TEST_SOURCE = "runtime.jackbot.gi-test"
LAMP_TEST_SOURCE = "runtime.jackbot.single-lamps"
RAMP_TEST_SOURCE = "runtime.jackbot.ramp-test"
VISOR_TEST_SOURCE = "runtime.jackbot.visor-test"
CALLOUT_SOURCE = "drawing-callouts.jackbot.2026-10-09"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-95"

TABLE_NAME = "Jack-Bot (Williams 1995).vpx"
TABLE_SHA256 = "31b827ba75dc7bc9fab1b3df5c9ff0708b235eb46e64666a781d4721fce4260f"
SCRIPT_SHA256 = "8edd32cea57460f1d76b864e39b742bb3bc77c0c201816a72094e4476c516c8b"
MANUAL_NAME = "Williams_1995_Jack_Bot_English_Manual.pdf"
MANUAL_SHA256 = "8295268601bbd4379917de2003b44ab56abc260b334f83c345d75ed50fe2ff94"
BULLETIN_NAME = "Williams_1995_Jack_Bot_Service_Bulletin_86.pdf"
BULLETIN_SHA256 = "9fe7a8314e8de55585893743b80087b351c4cc80e62aa8431676d517512381e0"
IPDB_PAGE_SHA256 = "86566b440d59ad72ba4d5a65e1117e769e21bdb0c19a32392034a19660f411f5"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/williams.jackbot.1995/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=3619"
IPDB_WAYBACK = "https://web.archive.org/web/2024id_/https://www.ipdb.org/machine.cgi?id=3619"
WAYBACK_FILES = {
	MANUAL_NAME: "https://web.archive.org/web/20211017122025id_/https://www.ipdb.org/files/3619/" + MANUAL_NAME,
	BULLETIN_NAME: "https://web.archive.org/web/20211017122021id_/https://www.ipdb.org/files/3619/" + BULLETIN_NAME,
}
ACQUIRED_AT = "2026-10-09T19:56:00Z"
RIGHTS_NOTE = "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Machine Database"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

EXTRACTION_FILE_COUNT = 1603
EXTRACTION_TOTAL_BYTES = 289318015
EXTRACTION_MANIFEST_SHA256 = "8c76313b82c0c5850c94c5e1eab0f3f478091422a8f2fe7a4c1dcdb9b75bbea7"
EXTRACTION_RELATIVE_PATH = Path("williams/jackbot-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/jackbot-1995/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# Every wiring field below cites the retained May 1995 preliminary manual, which documents the WPC Security
# five-board set: CPU A-17651-50051 (J205, J207, J209), Power Driver A-12697-3 (J1xx), Fliptronic II A-15472-1
# (J9xx), Dot Matrix Controller A-14039.1 and the separate DCS sound board.  IPDB names the MPU WPC Security and
# says some production games were built with WPC-95 board sets, whose connectors this manual does not document.
CPU_BOARD = "WPC Security CPU board A-17651-50051"
DRIVER_BOARD = "WPC power driver board A-12697-3"
FLIPTRONIC_BOARD = "Fliptronic II board A-15472-1"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("jb_10r", "jb_101r", "jb_10b", "jb_101b", "jb_04a")
DRIVER_COMPATIBILITY = {
	"jb_10r": (
		"identical",
		"Production game ROM 1.0R (jack1_0r.rom) with the DCS sound ROMs S2-S6, the parent driver. The retained known-working table "
		'binds it (Const cGameName="jb_10r"), and every service-test run behind this definition booted it.',
	),
	"jb_101r": (
		"identical",
		"Game ROM 1.01R, which pinned jb.c describes as the LED Ghost Fix revision of 1.0R; the same sound ROMs, jbGameData and "
		"wpc_m95DCSS machine driver, so the public controller contract is the parent's. A firmware revision on the same hardware.",
	),
	"jb_10b": (
		"identical",
		"Game ROM 1.0B, the Belgian/Canadian release of 1.0; the same sound ROMs, jbGameData and machine driver. The manual's "
		"ROM summary lists a foreign game ROM (-1X) beside the domestic one (-1A); the difference is firmware, not hardware.",
	),
	"jb_101b": (
		"identical",
		"Game ROM 1.01B, the Belgian/Canadian LED Ghost Fix revision; the same sound ROMs, jbGameData and machine driver.",
	),
	"jb_04a": (
		"unknown",
		"Sample/prototype game ROM 0.4A with its own speech ROM jbsnd_04a.u2 (the other four sound ROMs equal production's), the "
		"ROM IPDB hosts as 'Sample/Prototype ROM 0.4A'. Pinned jb.c comments it 'WPC-S 5-Board' and gives it the parent's "
		"jbGameData and wpc_m95DCSS driver, so the public controller contract is the same. No retained source documents the "
		"sample cabinet beyond Service Bulletin 86, which concerns sample games' CPU boards without naming their game code. Shared "
		"game data proves the routing, not the cabinet, so its physical compatibility stays unknown until a source describes the "
		"sample machine.",
	),
}

# --- Switch data (switch-matrix.md, switch-locations.md, section-3-boards.md) ---------------------------
# address -> (switch part number cell, printed Switch Locations description).
SWITCH_LOCATIONS = {
	11: ("SW-1A-120", "Lower Left 10 Point"), 12: ("SW-1A-120", "Upper Left 10 Point"), 13: ("20-9663-1", "Start Button"),
	14: ("A-15361", "Plumb Bob Tilt*"), 15: ("5647-12001-00", "Ramp Is Down"), 16: ("A-13609", "High Drop Target"),
	17: ("A-13609", "Center Drop Target"), 18: ("A-13609", "Low Drop Target"), 21: ("A-17238", "Slam Tilt*"),
	22: ("5643-09268-00", "Coin Door Closed*"), 23: ("20-9663-18", "Buy Extra Ball"), 24: ("5643-09112-00", "Always Closed*"),
	25: ("5647-12693-19", "Left Outlane"), 26: ("5647-12693-19", "Left Flipper Lane"), 27: ("5647-12693-19", "Right Flipper Lane"),
	28: ("5647-12693-19", "Right Outlane"),
	31: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough Jam"), 32: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 1 (Right)"),
	33: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 2"), 34: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 3"),
	35: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 4"), 36: ("5647-12693-11", "Ramp Exit"), 37: ("5647-12693-11", "Ramp Entrance"),
	38: ("A-18605-4", "Target Under Ramp"), 41: ("SW-1A-161", "Visor 1 (Left)"), 42: ("SW-1A-163-1", "Visor 2"),
	43: ("SW-1A-163-4", "Visor 3"), 44: ("SW-1A-163-2", "Visor 4"), 45: ("SW-1A-163-3", "Visor 5 (Right)"),
	46: ("5647-12693-43", "Far Left Eject"), 47: ("5647-12693-43", "Left Eject Hole (Visor)"), 48: ("5647-12693-43", "Right Eject Hole (Visor)"),
	51: ("A-18605-6", "5-Bank Target 1 (Upper)"), 52: ("A-18605-1", "5-Bank Target 2"), 53: ("A-18605-15", "5-Bank Target 3"),
	54: ("A-18605-2", "5-Bank Target 4"), 55: ("A-18605-4", "5-Bank Target 5 (Lower)"), 56: ("5647-12133-08", "Vortex Upper"),
	57: ("5647-12133-08", "Vortex Center"), 58: ("5647-12693-19", "Vortex Lower"), 61: ("A-12030-3", "Upper Jet Bumper"),
	62: ("A-12030-3", "Left Jet Bumper"), 63: ("A-12030-3", "Lower Jet Bumper"),
	64: ("SW-1A-120 (score) / SW-1A-114 (kick)", "Right Slingshot"), 65: ("SW-1A-120 (score) / SW-1A-114 (kick)", "Left Slingshot"),
	66: ("SW-1A-120", "Right 10 Point"), 67: ("A-18605-2", "Hit Me Target"), 68: ("5647-12693-32", "Ball Shooter"),
}
SWITCH_LABELS = {
	11: "Lower Left 10 Point", 12: "Upper Left 10 Point", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Ramp Is Down",
	16: "High Drop Target", 17: "Center Drop Target", 18: "Low Drop Target", 21: "Slam Tilt", 22: "Coin Door Closed",
	23: "Buy Extra Ball", 24: "Always Closed", 25: "Left Outlane", 26: "Left Flipper Lane", 27: "Right Flipper Lane",
	28: "Right Outlane", 31: "Trough Jam", 32: "Trough 1 (Right)", 33: "Trough 2", 34: "Trough 3", 35: "Trough 4 (Left)",
	36: "Ramp Exit", 37: "Ramp Entrance", 38: "Target Under Ramp", 41: "Visor Target 1 (Left)", 42: "Visor Target 2",
	43: "Visor Target 3", 44: "Visor Target 4", 45: "Visor Target 5 (Right)", 46: "Game Saucer (Far Left Eject)",
	47: "Left Eye Eject Hole (Visor)", 48: "Right Eye Eject Hole (Visor)", 51: "5-Bank Target 1 (Upper)", 52: "5-Bank Target 2",
	53: "5-Bank Target 3", 54: "5-Bank Target 4", 55: "5-Bank Target 5 (Lower)", 56: "Vortex Upper", 57: "Vortex Center",
	58: "Vortex Lower", 61: "Upper Jet Bumper", 62: "Left Jet Bumper", 63: "Lower Jet Bumper", 64: "Right Slingshot",
	65: "Left Slingshot", 66: "Right 10 Point", 67: "Hit Me Target", 68: "Ball Shooter",
}
SWITCH_TYPES = {
	11: "leaf", 12: "leaf", 13: "button", 14: "tilt", 15: "microswitch", 16: "opto", 17: "opto", 18: "opto", 21: "tilt",
	22: "microswitch", 23: "button", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "microswitch", 37: "microswitch", 38: "other",
	41: "leaf", 42: "leaf", 43: "leaf", 44: "leaf", 45: "leaf", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "other", 52: "other", 53: "other", 54: "other", 55: "other", 56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "leaf", 62: "leaf", 63: "leaf", 64: "leaf", 65: "leaf", 66: "leaf", 67: "other", 68: "microswitch",
}
SWITCH_ROLES = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}
UNUSED_MATRIX_ADDRESSES = frozenset(range(71, 79)) | frozenset(range(81, 89))
# PinMAME's jbGameData invSw {0x00,0xe0,0x00,0x1f,0x00,...} inverts these public addresses through wpc_sw2m (column 1
# rows 6-8 and column 3 rows 1-5); the test recomputes the set from the mask.
MASKED_SWITCHES = frozenset({16, 17, 18, 31, 32, 33, 34, 35})
# Cells the matrix page shades "OPTO, TYPICALLY CLOSED" (measured in switch-matrix.md; identical on all three printings).
SHADED_SWITCHES = frozenset({16, 17, 18, 41, 42, 43, 44, 45, 112, 114, 116, 118})
OPTO_SWITCHES = frozenset({16, 17, 18, 31, 32, 33, 34, 35})
# The ROM's own T.1 names (switch-edges sweep), read while the host held the public address at 1.
ROM_SWITCH_NAMES = {
	11: "L. LEFT 10 POINT", 12: "U. LEFT 10 POINT", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "RAMP IS DOWN",
	16: "HIGH DROP TARGET", 17: "CENT. DROP TARGET", 18: "LOW DROP TARGET", 21: "SLAM TILT", 22: "COIN DOOR CLOSED",
	23: "BUY EXTRA BALL", 25: "LEFT OUTLANE", 26: "L. FLIPPER LANE", 27: "R. FLIPPER LANE", 28: "RIGHT OUTLANE", 31: "TROUGH JAM",
	32: "TROUGH 1 (RIGHT)", 33: "TROUGH 2", 34: "TROUGH 3", 35: "TROUGH 4 (LEFT)", 36: "RAMP EXIT", 37: "RAMP ENTRANCE",
	38: "TARG. UNDER RAMP", 41: "VISOR 1 (LEFT)", 42: "VISOR 2", 43: "VISOR 3", 44: "VISOR 4", 45: "VISOR 5 (RIGHT)",
	46: "GAME SAUCER", 47: "LEFT EJECT HOLE", 48: "RIGHT EJECT HOLE", 51: "5-BANK 1 (UPPER)", 52: "5-BANK TARGET 2",
	53: "5-BANK TARGET 3", 54: "5-BANK TARGET 4", 55: "5-BANK 5 (LOWER)", 56: "VORTEX UPPER", 57: "VORTEX CENTER",
	58: "VORTEX LOWER", 61: "UPPER JET BUMPER", 62: "LEFT JET BUMPER", 63: "LOWER JET BUMPER", 64: "RIGHT SLINGSHOT",
	65: "LEFT SLINGSHOT", 66: "RIGHT 10 POINT", 67: "HIT ME TARGET", 68: "BALL SHOOTER",
}
# Switches whose closure makes the ROM fire their own coil even inside T.1 (switch-edges sweep).
SWITCH_FIRES = {61: 13, 62: 12, 63: 11, 64: 10, 65: 9}
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"), 3: ("Green-Orange", "J207-3", "U20-16"),
	4: ("Green-Yellow", "J207-4", "U20-15"), 5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"), 3: ("White-Orange", "J209-3", "U18-5"),
	4: ("White-Yellow", "J209-4", "U18-7"), 5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"), 4: ("Orange-Yellow", "J205-4"),
	5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"), 7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Printed Normal 'Service Credit', Test 'Escape'."),
	6: ("Volume Down / Down", "service.down", "Printed Normal 'Volume Down', Test 'Down'."),
	7: ("Volume Up / Up", "service.up", "Printed Normal 'Volume Up', Test 'Up'."),
	8: ("Begin Test / Enter", "service.enter", "Printed Normal 'Begin Test', Test 'Enter'."),
}
# The ROM's T.1 names for the coin switches (switch-edges sweep).
ROM_COIN_NAMES = {1: "LEFT COIN SLOT", 2: "CENTER COIN SLOT", 3: "RIGHT COIN SLOT", 4: "4TH COIN OPTION"}
# Fliptronic column (switch-matrix.md; section-3-boards.md, printed 3-11 to 3-14 and 3-20):
# public -> (label, printed position, wire, connector, type, role or None).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J906-1", "leaf", "internal.flipper.lower.right.eos"),
	112: ("Right Flipper Button Lower Opto", "F2", "Blue-Violet", "J905-1", "opto", "flipper.lower.right.button"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J906-3", "leaf", "internal.flipper.lower.left.eos"),
	114: ("Left Flipper Button Lower Opto", "F4", "Blue-Gray", "J905-2", "opto", "flipper.lower.left.button"),
	115: ("Visor Closed", "F5", "Black-Violet", "J906-4", "microswitch", None),
	116: ("Right Flipper Button Upper Opto", "F6", "Black-Yellow", "J905-3", "opto", "flipper.lower.right.button"),
	117: ("Visor Open", "F7", "Black-Gray", "J906-5", "microswitch", None),
	118: ("Left Flipper Button Upper Opto", "F8", "Black-Blue", "J905-5", "opto", "flipper.lower.left.button"),
}
# T.1's printed position and wires for the Fliptronic column (switch-edges sweep).
FLIPPER_ROM_TEXT = {112: "R. FLIPPER EOS. / LAST SW F1 / BLK-GRN ORN", 114: "L. FLIPPER EOS. / LAST SW F3 / BLK-BLU ORN", 115: "VISOR IS CLOSED / LAST SW F5 / BLK-VIO ORN", 116: "R. FLIPPER EOS. / LAST SW F1 / BLK-GRN ORN", 117: "VISOR IS OPEN / LAST SW F7 / BLK-GRY ORN", 118: "L. FLIPPER EOS. / LAST SW F3 / BLK-BLU ORN"}
FLIPPER_FIRES = {112: frozenset({45, 46}), 114: frozenset({47, 48}), 116: frozenset({45, 46}), 118: frozenset({47, 48})}

# --- Solenoid data (solenoid-flasher-table.md, solenoid-flashlamp-locations.md, section-3-boards.md) -----
SOLENOID_LABELS = {
	1: "Ball Release", 3: "Game Saucer Eject", 4: "Drop Target Reset", 5: "Right Eye Eject", 6: "Raise Ramp", 7: "Knocker",
	8: "Left Eye Eject", 9: "Left Slingshot", 10: "Right Slingshot", 11: "Lower Jet Bumper", 12: "Left Jet Bumper",
	13: "Upper Jet Bumper", 14: "Drop Ramp", 15: "Right Visor Flasher", 16: "Left Visor Flasher", 17: "Center Visor Flasher",
	18: "Pinbot Face Flasher", 19: "Jet Bumpers Flasher", 20: "Lower Left Flasher", 21: "Middle Left Flasher",
	22: "Lower Right Flasher", 23: "Back Panel Flasher 1 (Left)", 24: "Back Panel Flasher 2", 25: "Back Panel Flasher 3",
	26: "Back Panel Flasher 4", 27: "Back Panel Flasher 5 (Right)", 28: "Visor Motor",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_USED_SOLENOID_LABELS = {
	2: "Not Used Solenoid Position 2", 33: "Not Used Upper Right Flipper Power", 34: "Not Used Upper Right Flipper Hold",
	35: "Not Used Upper Left Flipper Power", 36: "Not Used Upper Left Flipper Hold",
	**{address: f"Not Used Solenoid Position {address}" for address in range(37, 41)},
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B", 31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32", 41: "LPDC Mirror Position 41", 42: "LPDC Mirror Position 42", 43: "LPDC Mirror Position 43",
	44: "LPDC Mirror Position 44", 49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> printed (function, type, voltage connector(s), transistor, drive connector(s), wire, part or flashlamp), 2-38.
SOLENOID_TABLE = {
	1: ("BALL RELEASE", "High Power", "J107-2", "Q82", "J130-1", "VIO-BRN", "AE-26-1500"),
	2: ("NOT USED", "High Power", "J107-2", "Q80", "J130-2", "VIO-RED", None),
	3: ("FAR LEFT EJECT", "High Power", "J107-2", "Q78", "J130-4", "VIO-ORG", "AE-26-1200"),
	4: ("DROP TARGETS", "High Power", "J107-2", "Q76", "J130-5", "VIO-YEL", "AE-26-1200"),
	5: ("RIGHT EJECT HOLE", "High Power", "J107-2", "Q64", "J130-6", "VIO-GRN", "AE-26-1200"),
	6: ("RAISE RAMP", "High Power", "J107-2", "Q66", "J130-7", "VIO-BLU", "AE-26-1200"),
	7: ("KNOCKER", "High Power", "J107-2 (backbox)", "Q68", "J130-8 (backbox)", "VIO-BLK", "AE-23-800"),
	8: ("LEFT EJECT HOLE", "High Power", "J107-2", "Q70", "J130-9", "VIO-GRY", "AE-26-1200"),
	9: ("LEFT SLINGSHOT", "Low Power", "J107-3", "Q58", "J127-1", "BRN-BLK", "AE-26-1200"),
	10: ("RIGHT SLINGSHOT", "Low Power", "J107-3", "Q56", "J127-3", "BRN-RED", "AE-26-1200"),
	11: ("LOWER JET BUMPER", "Low Power", "J107-3", "Q54", "J127-4", "BRN-ORG", "AE-26-1200"),
	12: ("LEFT JET BUMPER", "Low Power", "J107-3", "Q52", "J127-5", "BRN-YEL", "AE-26-1200"),
	13: ("UPPER JET BUMPER", "Low Power", "J107-3", "Q50", "J127-6", "BRN-GRN", "AE-26-1200"),
	14: ("DROP RAMP", "Low Power", "J107-3", "Q48", "J127-7", "BRN-BLU", "SM1-26-600"),
	15: ("RIGHT VISOR FLSHR(2)", "Low Power", "J107-6", "Q46", "J127-8", "BRN-VIO", "#906"),
	16: ("LEFT VISOR FLSHR(2)", "Low Power", "J107-6", "Q44", "J127-9", "BRN-GRY", "#906"),
	17: ("CENTER VISOR FLSHR", "Flashlamp", "J107-6", "Q42", "J126-1", "BLK-BRN", "#906"),
	18: ("PINBOT FACE FLSHR", "Flashlamp", "J107-6", "Q40", "J126-2", "BLK-RED", "#906"),
	19: ("JET BUMPERS FLSHR", "Flashlamp", "J107-6", "Q38", "J126-3", "BLK-ORG", "#906"),
	20: ("LOWER LEFT FLSHR", "Flashlamp", "J107-6", "Q36", "J126-4", "BLK-YEL", "#906"),
	21: ("MIDDLE LEFT FLSHR", "Flashlamp", "J107-6", "Q28", "J126-5", "BLU-GRN", "#906"),
	22: ("LOWER RIGHT FLSHR", "Flashlamp", "J107-6", "Q30", "J126-6", "BLU-BLK", "#906"),
	23: ("BACK PNL FLSHR 1 (LT)", "Flashlamp", "J107-6", "Q34", "J126-7", "BLU-VIO", "#906"),
	24: ("BACK PANEL FLSHR 2", "Flashlamp", "J107-6", "Q32", "J126-8", "BLU-GRY", "#906"),
	25: ("BACK PANEL FLSHR 3", "Gen. Purpose", "J107-6", "Q26", "J122-1", "BLU-BRN", "#906"),
	26: ("BACK PANEL FLSHR 4", "Gen. Purpose", "J107-6", "Q24", "J122-2", "BLU-RED", "#906"),
	27: ("BACK PNL FLSHR 5 (RT)", "Gen. Purpose", "J107-6", "Q22", "J122-3", "BLU-ORG", "#906"),
	28: ("VISOR MOTOR", "Gen. Purpose", "J118-2", "Q20", "J122-4", "BLU-YEL", "14-8023"),
	37: ("NOT USED", "Low Power", None, "Q16", None, "BRN-WHT", None),
	38: ("NOT USED", "Low Power", None, "Q15", None, "BLK-WHT", None),
	39: ("NOT USED", "Low Power", None, "Q14", None, "ORG-WHT", None),
	40: ("NOT USED", "Low Power", None, "Q13", None, "YEL-WHT", None),
	41: ("NOT USED", "Low Power", None, "Q9", None, "GRN-WHT", None),
	42: ("NOT USED", "Low Power", None, "Q10", None, "BLU-WHT", None),
	43: ("NOT USED", "Low Power", None, "Q11", None, "VIO-WHT", None),
	44: ("NOT USED", "Low Power", None, "Q12", None, "GRY-WHT", None),
}
# Solenoid/Flashlamp Locations list (2-39): address -> (coil or flasher number, assembly number).
SOLENOID_ASSEMBLIES = {
	1: ("AE-26-1500", "A-19963"), 3: ("AE-26-1200", "A-20453"), 4: ("AE-26-1200", "A-20415"), 5: ("AE-26-1200", "A-20453"),
	6: ("AE-26-1200", "B-9362-L-2"), 7: ("AE-23-800", "B-10686-1"), 8: ("AE-26-1200", "A-20453"), 9: ("AE-26-1200", "B-9362-L-2"),
	10: ("AE-26-1200", "B-9362-L-2"), 11: ("AE-26-1200", "A-9415-2"), 12: ("AE-26-1200", "A-9415-2"), 13: ("AE-26-1200", "A-9415-2"),
	14: ("SM1-26-600", "B-11304"), 15: ("24-8802", "A-20158"), 16: ("24-8802", "A-20158"), 17: ("24-8802", "A-20158"),
	18: ("24-8802", "A-17802"), 19: ("24-8802", "A-17802"), 20: ("24-8802", "04-10091.1"), 21: ("24-8802", "04-10091.1"),
	22: ("24-8802", "04-10091.1"), 23: ("24-8802", "A-20158"), 24: ("24-8802", "A-20158"), 25: ("24-8802", "A-20158"),
	26: ("24-8802", "A-20158"), 27: ("24-8802", "A-20158"), 28: ("14-8023", "A-20100"),
}
FLASHER_SOLENOIDS = frozenset(range(15, 28))
BACK_PANEL_FLASHERS = frozenset(range(23, 28))
# "FLSHR(2)": the table prints two lamps on each eye-flasher line.
FLASHER_COUNTS = {15: 2, 16: 2}
# The ROM's own T.4 and T.5 names and wires (solenoid-test and flasher-test runs).
ROM_SOLENOID_NAMES = {
	1: ("BALL RELEASE", "VIO-BRN RED-BRN"), 3: ("GAME SAUCER", "VIO-ORN RED-BRN"), 4: ("DROP TARGETS", "VIO-YEL RED-BRN"),
	5: ("RIGHT EJECT HOLE", "VIO-GRN RED-BRN"), 6: ("RAISE RAMP", "VIO-BLU RED-BRN"), 7: ("KNOCKER", "VIO-BLK RED-BRN"),
	8: ("LEFT EJECT HOLE", "VIO-GRY RED-BRN"), 9: ("LEFT SLINGSHOT", "BRN-BLK RED-BLK"), 10: ("RIGHT SLINGSHOT", "BRN-RED RED-BLK"),
	11: ("LOWER JET BUMPER", "BRN-ORN RED-BLK"), 12: ("LEFT JET BUMPER", "BRN-YEL RED-BLK"), 13: ("UPPER JET BUMPER", "BRN-GRN RED-BLK"),
	14: ("DROP RAMP", "BRN-BLU RED-BLK"),
	15: ("RIGHT VISOR", "BRN-VIO RED-WHT"), 16: ("LEFT VISOR", "BRN-GRY RED-WHT"), 17: ("CENTER VISOR", "BLK-BRN RED-WHT"),
	18: ("PINBOT FACE", "BLK-RED RED-WHT"), 19: ("JET BUMPERS", "BLK-ORN RED-WHT"), 20: ("LOWER LEFT", "BLK-YEL RED-WHT"),
	21: ("MID LEFT", "BLU-GRN RED-WHT"), 22: ("LOWER RIGHT", "BLU-BLK RED-WHT"), 23: ("BACK PANEL 1 (L)", "BLU-VIO RED-WHT"),
	24: ("BACK PANEL 2", "BLU-GRY RED-WHT"), 25: ("BACK PANEL 3", "BLU-BRN RED-WHT"), 26: ("BACK PANEL 4", "BLU-RED RED-WHT"),
	27: ("BACK PANEL 5 (R)", "BLU-ORN RED-WHT"),
	45: ("R. FLIP. POWER", "YEL-GRN RED-GRN"), 46: ("R. FLIP. HOLD", "ORN-GRN RED-GRN"), 47: ("L. FLIP. POWER", "YEL-BLU RED-BLU"),
	48: ("L. FLIP. HOLD", "ORN-BLU RED-BLU"),
}
T4_ADDRESSES = frozenset({1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14})
T5_ADDRESSES = frozenset(range(15, 28))
T12_ADDRESSES = frozenset({45, 46, 47, 48})
# Fliptronic flipper windings (solenoid-flasher-table.md flipper block; the manual numbers them 29-32).
FLIPPER_COILS = {
	45: ("power", "29", "Q4", "J902-13", "YEL-GRN", "J907-1 (RED-GRN)", "A-15849-R"),
	46: ("hold", "30", "Q11", "J902-11", "ORG-GRN", "J907-1 (RED-GRN)", "A-15849-R"),
	47: ("power", "31", "Q3", "J902-9", "YEL-BLU", "J907-4 (RED-BLU)", "A-15849-L"),
	48: ("hold", "32", "Q9", "J902-7", "ORG-BLU", "J907-4 (RED-BLU)", "A-15849-L"),
}
UPPER_FLIPPER_CIRCUITS = {
	33: ("power", "Q2", "J902-6", "YEL-VIO", "J907-6 (RED-VIO)", "upper right"),
	34: ("hold", "Q7", "J902-4", "ORG-VIO", "J907-6 (RED-VIO)", "upper right"),
	35: ("power", "Q1", "J902-3", "YEL-GRY", "J907-8 (RED-GRY)", "upper left"),
	36: ("hold", "Q5", "J902-1", "ORG-GRY", "J907-8 (RED-GRY)", "upper left"),
}

# --- Lamp data (lamp-locations.md, lamp-matrix.md) -------------------------------------------------------
# address -> (bulb part number, lamp assembly, printed Lamp Locations description).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-20079", "Yellow Arrow"), 12: ("24-8768", "A-20079", "Yellow 1 (High)"), 13: ("24-8768", "A-20079", "Yellow 2"),
	14: ("24-8768", "A-20079", "Yellow 3"), 15: ("24-8768", "A-20079", "Yellow 4"), 16: ("24-8768", "A-20079", "Yellow 5 (Low)"),
	17: ("24-6549", "A-17835", "Left Outlane"), 18: ("24-6549", "A-17835", "Left Flipper Lane"),
	21: ("24-8768", "A-20079", "Blue Arrow"), 22: ("24-8768", "A-20079", "Blue 1 (High)"), 23: ("24-8768", "A-20079", "Blue 2"),
	24: ("24-8768", "A-20079", "Blue 3"), 25: ("24-8768", "A-20079", "Blue 4"), 26: ("24-8768", "A-20079", "Blue 5 (Low)"),
	27: ("24-6549", "A-17835", "Bonus 2X"), 28: ("24-6549", "A-17835", "Bonus 3X"),
	31: ("24-8768", "A-20079", "Amber Arrow"), 32: ("24-8768", "A-20079", "Amber 1 (High)"), 33: ("24-8768", "A-20079", "Amber 2"),
	34: ("24-8768", "A-20079", "Amber 3"), 35: ("24-8768", "A-20079", "Amber 4"), 36: ("24-8768", "A-20079", "Amber 5 (Low)"),
	37: ("24-6549", "A-17807", "Shoot Again"), 38: ("24-6549", "A-17835", "Bonus 4X"),
	41: ("24-8768", "A-20079", "Green Arrow"), 42: ("24-8768", "A-20079", "Green 1 (High)"), 43: ("24-8768", "A-20079", "Green 2"),
	44: ("24-8768", "A-20079", "Green 3"), 45: ("24-8768", "A-20079", "Green 4"), 46: ("24-8768", "A-20079", "Green 5 (Low)"),
	47: ("24-6549", "A-17835", "Bonus 5X"), 48: ("24-6549", "A-17835", "Jack•Bot (Target)"),
	51: ("24-8768", "A-20079", "Red Arrow"), 52: ("24-8768", "A-20079", "Red 1 (High)"), 53: ("24-8768", "A-20079", "Red 2"),
	54: ("24-8768", "A-20079", "Red 3"), 55: ("24-8768", "A-20079", "Red 4"), 56: ("24-8768", "A-20079", "Red 5 (Low)"),
	57: ("24-6549", "A-17835", "Right Flipper Lane"), 58: ("24-6549", "A-17835", "Right Outlane"),
	61: ("24-8768", "A-20125", "Card 1 (Left)"), 62: ("24-8768", "A-20125", "Card 2"), 63: ("24-8768", "A-20125", "Card 3"),
	64: ("24-8768", "A-20125", "Card 4"), 65: ("24-8768", "A-20125", "Card 5 (Right)"), 66: ("24-6549", "A-17835", "Casino Run"),
	67: ("24-6549", "A-17835", "Hit Me"), 68: ("24-6549", "A-17807", "Low Drop Target"),
	71: ("24-8768", "A-19035", "Light Ex. Ball (Mini Plfd)"), 72: ("24-8768", "A-19035", "Mega Ramp (Mini Plfd)"),
	73: ("24-8768", "A-19035", "Cashier (Mini Plfd)"), 74: ("24-8768", "A-19035", "25 Million (Mini Plfd)"),
	75: ("24-8768", "A-17272", "Game Saucer"), 76: ("24-8768", "A-17272", "Mega Ramp"), 77: ("24-6549", "A-17807", "High Drop Target"),
	78: ("24-6549", "A-17807", "Center Drop Target"),
	81: ("24-8768", "A-20174", "Pinbot Poker"), 82: ("24-8768", "A-20174", "Slot Machine"), 83: ("24-8768", "A-20174", "Roll The Dice"),
	84: ("24-8768", "A-20174", "Keno"), 85: ("24-6549", "A-17807", "Cashier (Under Ramp)"), 86: ("24-6549", "A-17835", "Jack•Bot (Ramp)"),
	87: (None, "20-9663-18", "Buy-In Button"), 88: (None, "20-9663-1", "Start Button"),
}
# Lamp Matrix cell text where it differs from the Lamp Locations description (lamp-matrix.md).
LAMP_MATRIX_TEXT = {71: "CASHIER MINI-PLFD", 73: "LIGHT EX. BALL MINI-PLFD", 74: "JACK•BOT MINI-PLFD"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J134-1", "Q90"), 2: ("Red-Black", "J134-2", "Q89"), 3: ("Red-Orange", "J134-4", "Q88"),
	4: ("Red-Yellow", "J134-5", "Q87"), 5: ("Red-Green", "J134-6", "Q87"), 6: ("Red-Blue", "J134-7", "Q86"),
	7: ("Red-Violet", "J134-8", "Q84"), 8: ("Red-Gray", "J134-9", "Q83"),
}
CABINET_LAMPS = {87: "cabinet.buy-in", 88: "cabinet.start"}
# The ROM's T.8 SINGLE LAMPS names (single-lamps run, read on each step's lit frame).
ROM_LAMP_NAMES = {
	11: "YELLOW ARROW", 12: "YELLOW 1 (HI)", 13: "YELLOW 2", 14: "YELLOW 3", 15: "YELLOW 4", 16: "YELLOW 5 (LOW)",
	17: "LEFT OUTLANE", 18: "L. FLIPPER LANE", 21: "BLUE ARROW", 22: "BLUE 1 (HI)", 23: "BLUE 2", 24: "BLUE 3", 25: "BLUE 4",
	26: "BLUE 5 (LOW)", 27: "BONUS 2X", 28: "BONUS 4X", 31: "AMBER ARROW", 32: "AMBER 1 (HI)", 33: "AMBER 2", 34: "AMBER 3",
	35: "AMBER 4", 36: "AMBER 5 (LOW)", 37: "SHOOT AGAIN", 38: "BONUS 5X", 41: "GREEN ARROW", 42: "GREEN 1 (HI)", 43: "GREEN 2",
	44: "GREEN 3", 45: "GREEN 4", 46: "GREEN 5 (LOW)", 47: "BONUS 3X", 48: "JACK*BOT TARGET", 51: "RED ARROW", 52: "RED 1 (HI)",
	53: "RED 2", 54: "RED 3", 55: "RED 4", 56: "RED 5 (LOW)", 57: "R. FLIPPER LANE", 58: "RIGHT OUTLANE", 61: "CARD 1 (L)",
	62: "CARD 2", 63: "CARD 3", 64: "CARD 4", 65: "CARD 5 (R)", 66: "CASINO RUN", 67: "HIT ME", 68: "LOW DROP TARGET",
	71: "CASHIER MINI-P.F.", 72: "MEG. RAMP MINI-P.F.", 73: "LITE EXTRA BALL", 74: "JACK*BOT MINI-P.F.", 75: "GAME SAUCER",
	76: "MEGA RAMP", 77: "HIGH DROP TARGET", 78: "CENT. DROP TARGET", 81: "PINBOT POKER", 82: "SLOT MACHINE", 83: "ROLL THE DICE",
	84: "KENO", 85: "CASHIER", 86: "JACK*BOT (RAMP)", 87: "BUY IN BUTTON", 88: "START BUTTON",
}
# Where the ROM and the retained table's insert art agree against the manual's printed cells (the manual is the May 1995
# preliminary edition): address -> (printed Lamp Matrix cell, printed Lamp Locations description).
LAMP_MANUAL_MISPRINTS = {
	28: ("BONUS 3X", "Bonus 3X"), 38: ("BONUS 4X", "Bonus 4X"), 47: ("BONUS 5X", "Bonus 5X"),
}
# Where the ROM agrees with the Lamp Matrix against the Lamp Locations list.
LAMP_LIST_MISPRINTS = {71: "Light Ex. Ball (Mini Plfd)", 73: "Cashier (Mini Plfd)", 74: "25 Million (Mini Plfd)"}
LAMP_LABELS = {
	27: "Bonus 2X", 28: "Bonus 4X", 38: "Bonus 5X", 47: "Bonus 3X", 48: "Jack•Bot (Target)", 71: "Cashier (Mini-Playfield)",
	72: "Mega Ramp (Mini-Playfield)", 73: "Light Extra Ball (Mini-Playfield)", 74: "Jack•Bot (Mini-Playfield)",
	85: "Cashier (Under Ramp)", 86: "Jack•Bot (Ramp)", 87: "Buy-In Button", 88: "Start Button",
}

# --- General illumination (solenoid-flasher-table.md G.I. block; gi-test run) -----------------------------
# public -> (string, printed function, voltage connections, triac, drive connections, wire, bulb, ROM T.6 name, ROM wires)
GI_STRINGS = {
	0: (1, "PLAYFIELD LOWER", "J120-1, J121-1", "Q18", "J120-7, J121-7", "WHT-BRN", "#44 playfield", "PLAYFIELD LOWER", "WHT-BRN BRN"),
	1: (2, "PLAYFIELD LEFT", "J120-2, J121-2", "Q10", "J120-8, J121-8", "WHT-ORG", "#44 playfield", "PLAYFIELD LEFT", "WHT-ORN ORN"),
	2: (3, "PLAYFIELD UPPER", "J120-3, J121-3", "Q14", "J120-9, J121-9", "WHT-YEL", "#44 playfield", "PLAYFIELD UPPER", "WHT-YEL YEL"),
	3: (4, "PLAYFIELD RIGHT", "J120-5, J121-5", "Q16", "J120-10, J121-10", "WHT-GRN", "#44 playfield", "PLAYFIELD RIGHT", "WHT-GRN GRN"),
	4: (5, "INSERT", "J120-6, J119-3 (cabinet)", "Q12", "J120-11, J119-1 (cabinet)", "WHT-VIO", "#555 backbox", "INSERT", "WHT-VIO VIO"),
}


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
		raise RuntimeError(f"Jack*Bot retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Jack*Bot extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Jack*Bot retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Jack*Bot retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Jack*Bot retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


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
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")


# --- Placements ----------------------------------------------------------------------------------------
def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Located spatial record for one device from the committed placement seed, or None.

	Table-derived placements start as ``observed``; ``drawing_callouts.apply_to_definition`` promotes the ones the factory
	location drawings confirm. A placement measured on a drawing stays observed and cites the manual and the callout record.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		refs = (MANUAL_SOURCE, CALLOUT_SOURCE) if entry.get("measured") else (VPX_TABLE_SOURCE,)
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": entry["x"],
				"y": entry["y"],
				"provenance": provenance("observed", *refs),
			}
		)
	return {"status": "observed", "placements": placements}


def _spatial_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	notes = [entry["note"] for entry in entries if entry.get("note")]
	return (" " + " ".join(dict.fromkeys(notes))) if notes else ""


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": CPU_BOARD,
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


# What the retained known-working script does for each matrix switch (vpx-analysis script facts).
SWITCH_SCRIPT = {
	14: "vpmNudge.TiltSwitch = 14",
	15: "RampTimer_Timer sets it at 1 once the modelled ramp reaches the down end (RampLvl >= 0.8) and clears it near the up end (RampLvl < 0.33); no table object",
	16: "the drop target sw16 sets it when the target has dropped and clears it while the bank resets", 17: "the drop target sw17 sets it when the target has dropped",
	18: "the drop target sw18 sets it when the target has dropped",
	22: "Table1_Init sets Controller.Switch(22) = 1 (coin door closed)", 23: "the right MagnaSave key sets Controller.Switch(23) while held (the Extra Ball buy-in button)",
	24: "Table1_Init sets Controller.Switch(24) = 1",
	25: "trigger sw25 follows the ball", 26: "trigger sw26 follows the ball", 27: "trigger sw27 follows the ball", 28: "trigger sw28 follows the ball",
	36: "trigger rampout follows the ball", 37: "trigger rampin follows the ball", 38: "the sw38 target pulses it",
	41: "the sw41 visor target pulses it (the between-target sw4142 pulses 41 and 42)", 42: "the sw42 visor target pulses it",
	43: "the sw43 visor target pulses it", 44: "the sw44 visor target pulses it", 45: "the sw45 visor target pulses it",
	46: "the sw46 saucer (bsSaucer) holds the ball on it", 47: "the sw47 saucer (bsLEye) holds the ball on it", 48: "the sw48 saucer (bsREye) holds the ball on it",
	51: "the sw51 target pulses it", 52: "the sw52 target pulses it", 53: "the sw53 target pulses it", 54: "the sw54 target pulses it", 55: "the sw55 target pulses it",
	56: "trigger sw56 pulses it 100 ms after the ball enters", 57: "trigger sw57 pulses it", 58: "trigger sw58 follows the ball",
	61: "the sw61_bumper1 bumper pulses it", 62: "the sw62_bumper2 bumper pulses it", 63: "the sw63_bumper3 bumper pulses it",
	64: "RightSlingShot_Slingshot pulses it", 65: "LeftSlingShot_Slingshot pulses it", 67: "the sw67 target pulses it",
	68: "trigger sw68 follows the ball",
	11: "its only handler (WallLAa_Hit) names an object the table does not have, so the table never sets it",
	12: "its only handlers (Walllcc_Hit, Walllccc_Hit) name objects the table does not have, so the table never sets it",
	66: "its only handler (Wallrb_Hit) names an object the table does not have, so the table never sets it",
}
for _address, _slot in ((32, 1), (33, 2), (34, 3), (35, 4)):
	SWITCH_SCRIPT[_address] = f"the cvpmBallStack bsTrough derives it from its slot {_slot} ball count (no table object)"
SWITCH_SCRIPT[31] = "the table never writes it: bsTrough declares no jam or entry switch"
VISOR_TARGETS = {41: 1, 42: 2, 43: 3, 44: 4, 45: 5}
FIVE_BANK = {51: 1, 52: 2, 53: 3, 54: 4, 55: 5}


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += (
			" The Switch Matrix prints NOT USED in every cell of columns 7 and 8 and the Switch Locations list ends '71 THROUGH 88 ARE "
			"NOT USED'. In the ROM's T.1 SWITCH EDGES sweep a host write of 1 or 0 at this address drew no name."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, EDGES_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra,
		)
	part, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address], "part_number": part}
	notes += f' Switch Locations description "{description}".'
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address == 24:
		notes += (
			" PinMAME holds public 24 at 1 from power-up. In T.1 SWITCH EDGES the redundant write of 1 drew nothing new and the 1 -> 0 "
			"edge drew 'ALWAYS CLOSED', so the ROM reports this position when it opens."
		)
	else:
		notes += f" The ROM names it \"{ROM_SWITCH_NAMES[address]}\" in T.1 SWITCH EDGES while the host holds public {address} at 1, and clears the name at 0."
	if address in SWITCH_FIRES:
		notes += f" Closing it made the ROM fire its own coil, public solenoid {SWITCH_FIRES[address]}, even inside T.1."
	if address in MASKED_SWITCHES:
		notes += (
			" PinMAME's jbGameData inverted-switch mask inverts this address, so public 1 is an open matrix contact; the ROM reads the "
			"switch as active at public 1 (it names it there), so its matrix contact rests closed and normally_closed is true."
		)
	if address in {16, 17, 18}:
		notes += (
			" One of the three optos of the 3-Bank Opto Drop Target Board A-13609 (printed 3-21: OPTO 3, 2 and 1 read switch rows 6, 7 "
			"and 8 of column 1 through J1-1 to J1-3), which see the target drop. The matrix page shades the cell 'OPTO, TYPICALLY CLOSED'."
		)
	if address in {31, 32, 33, 34, 35}:
		board = {31: "LED 1 (Jam Ball)", 32: "LED 2 (Ball 1)", 33: "LED 3 (Ball 2)", 34: "LED 4 (Ball 3)", 35: "LED 5 (Ball 4)"}[address]
		notes += (
			f" Ball trough opto pair on the Trough IR LED Board A-18617-1 ({board}) and the Trough IR Photo Transistor Board A-18618-1, "
			"read through the 7-Opto Switch Board A-15595 (printed 3-15 to 3-19). The matrix page leaves the cell unshaded although the "
			"switch list, the trough pages and PinMAME's mask all make it an opto: the construction comes from those pages, the unshaded "
			"cell stays literal in the excerpt."
		)
		if address == 31:
			notes += " The jam position over the trough's ball-release coil; the switch list prints 'Trough Jam'."
		else:
			notes += f" It reports the trough holding at least {address - 31} ball{'s' if address > 32 else ''} (four balls are installed)."
	if address in VISOR_TARGETS:
		notes += (
			f" Visor target {VISOR_TARGETS[address]} of the five on the front of Pinbot's motorized visor (left to right); hitting the visor "
			"targets lights the chest matrix lamps. The switch list prints a leaf switch part (SW-1A-161 or SW-1A-163-n) while the matrix page "
			"shades the cell 'OPTO, TYPICALLY CLOSED'; PinMAME's mask leaves it alone and the ROM names it at public 1, an unmasked closed "
			"contact, so whatever the construction the matrix contact rests open and normally_closed is false. The parts list's leaf switch is "
			"recorded as the switch type."
		)
	if address in FIVE_BANK:
		notes += f" Stationary target {FIVE_BANK[address]} (top to bottom) of the 5-bank standup beside the visor; hits light the chest matrix like the visor targets."
	if address in {46, 47, 48}:
		notes += {
			46: " The Game Saucer: the eject hole at the upper left (the 'eject hole on the far left' of the rules) where Pinbot Poker, Slot Machine, Roll The Dice, Keno and Casino Run are played; its eject coil is solenoid 3, which the ROM's T.4 names GAME SAUCER.",
			47: " The left eye lock behind the visor: revealed when the visor opens, it holds a ball for multiball; its eject coil is solenoid 8.",
			48: " The right eye lock behind the visor: revealed when the visor opens, it holds a ball for multiball; its eject coil is solenoid 5.",
		}[address]
	if address in {56, 57, 58}:
		notes += " One of the three Vortex holes (upper, center, lower) the skill shot plunges into; the center hole scores three times the Vortex Millions value."
	if address in {11, 12, 66}:
		notes += " A 10-point rubber switch (SW-1A-120 leaf switch behind a rubber)."
	if address == 15:
		notes += (
			" The micro-switch 5647-12001-00 of the Ramp Lifting Mechanism Assembly B-11304 (item 16): closed while the lifting ramp is down. "
			"The ROM's T.16 RAMP TEST shows 'RAMP DOWN SW.' while it reads the switch closed."
		)
	if address in {36, 37}:
		notes += " A ramp switch of the lifting ramp to the mini-playfield: entering the ramp and leaving it at the top."
	if address == 38:
		notes += " The standup target under the lifting ramp (the Cashier shot under the ramp)."
	if address == 67:
		notes += " The lower-right Hit Me target that deals the Blackjack hand."
	if address == 68:
		notes += " The shooter lane switch where the ball rests before the plunger."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = {13: "cabinet front", 23: "cabinet front"}.get(address, "cabinet interior")
	elif address == 24:
		extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _spatial_note("switch", address)
	kind = "constant" if address == 24 else "switch"
	if address == 24:
		extra["constant_active"] = True
		extra["initial_active"] = True
	else:
		extra["normally_closed"] = address in MASKED_SWITCHES
	if address == 22:
		extra["initial_active"] = True
		notes += " The retained script sets it closed at table start; it is closed while the coin door is closed, and the service buttons need the door open."
	if address == 23:
		notes += " The Buy Extra Ball (buy-in) button on the cabinet front, lit by lamp 87; pressed repeatedly on a game title it makes Pin•Bot 'cheat' (rules)."
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		if address in ROM_COIN_NAMES:
			note += f" T.1 SWITCH EDGES names public {address} '{ROM_COIN_NAMES[address]}'."
			refs += (EDGES_SOURCE,)
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", refs,
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note} The dedicated switches reach the CPU through the Coin Door Interface Board A-17051-1."},
				wiring={"board": CPU_BOARD, "drive_wire": wire, "drive_connection": connection, "return_component": "U17-5 (printed after every dedicated wire on 3-3)"},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, switch_type, role) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} on the {FLIPTRONIC_BOARD}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": FLIPTRONIC_BOARD, "drive_wire": wire, "drive_connection": connection},
		}
		if role:
			extra["roles"] = [role]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		physical: dict[str, Any] = {"switch_type": switch_type}
		if address in {111, 113}:
			physical["part_number"] = "SW-1A-194"
			physical["location"] = "flipper assembly"
			notes += (
				f" End-of-stroke switch SW-1A-194 on the lower {'right' if address == 111 else 'left'} flipper assembly "
				f"({'A-15849-R' if address == 111 else 'A-15849-L'}). jbGameData declares FLIP_SOL(FLIP_L), so PinMAME rewrites this "
				"bit from the flipper coil state on every update: in the T.1 sweep a host write of 1 read back 0 and drew no name. Its "
				"public level is not a measurement of the contact; normally_closed records the grounded switch's open rest state."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address in {112, 114, 116, 118}:
			side = "right" if address in {112, 116} else "left"
			physical["location"] = "cabinet flipper button"
			physical["assembly_part_number"] = "A-17316"
			notes += (
				f" One of the two optos of the {side} Flipper Opto Board A-17316 at the {side} cabinet button. WPC-95 reads the flipper "
				"column complemented (WPC_FLIPPERSW95 returns ~swMatrix), so public 1 is the pressed button and the contact the matrix sees "
				"is open at rest: normally_closed is false. The matrix page shades the cell as an opto."
			)
			if side == "right":
				notes += (
					" Page 3-14's pin list for the right Flipper Opto Board prints Black-Yellow from J905-1 and Blue-Violet from J905-3, the "
					"reverse of the switch matrix and pages 3-11 and 3-13, which agree on Blue-Violet J905-1 (F2) and Black-Yellow J905-3 (F6); "
					"the wiring follows the agreeing pages, and both readings stay in the excerpts."
				)
			if address in FLIPPER_FIRES:
				notes += f" In the T.1 sweep a host write of 1 made the ROM fire the lower {side} flipper (power and hold) and show '{FLIPPER_ROM_TEXT[address]}'."
			if address in {116, 118}:
				notes += (
					f" The Switch Locations list prints '{printed} NOT USED', but the matrix page prints the cell '{'Upper Right' if side == 'right' else 'Upper Left'} "
					f"Opto' with its wire and pin, and the wiring pages (3-11 cabinet switch lines, 3-13 cabinet switch circuits, 3-14 Flipper "
					f"Opto Board pin list) wire {printed} to the second opto of the same {side} button's board. Jack•Bot has no upper flipper, "
					f"so the role is the {side} flipper button's, the same as {address - 4}'s: a consumer drives both from that button. The "
					"retained VPinMAME library writes only 112 and 114."
				)
				refs += (VPX_SCRIPT_SOURCE,)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			physical["part_number"] = "5647-12693-06"
			opened = address == 117
			notes += (
				f" The visor {'open' if opened else 'closed'} micro-switch (Switch Locations '{'Visor Is Open' if opened else 'Visor Is Closed'}', "
				f"part 5647-12693-06; the bracket's parts list 2-23 prints its two Mini Micro Switches as 5647-12694-06) on the Visor Motor "
				"Bracket Assembly A-20100. The Flipper Circuit Diagram's note says: 'IN JACK•BOT, THE UPPER "
				"RIGHT E.O.S. SWITCH, (F5), IS USED AS THE VISOR CLOSED SWITCH, AND THE UPPER LEFT E.O.S. SWITCH, (F7), IS USED AS THE VISOR OPEN "
				"SWITCH. THE UPPER RIGHT AND UPPER LEFT FLIPPERS ARE NOT USED.' jbGameData declares FLIP_SOL(FLIP_L) only, so PinMAME never "
				"synthesizes this upper end-of-stroke position and a host write reaches the ROM. PinMAME's mask leaves it alone, so WPC-95's "
				"complemented flipper-column read hands the ROM the complement of the public level: public 1 is the grounded, closed contact. "
				+ VISOR_SWITCH_EVIDENCE[address]
			)
			extra["normally_closed"] = False
			refs += (VPX_SCRIPT_SOURCE, VISOR_TEST_SOURCE)
			notes += (
				f" Retained script: the visor cvpmMech closes it at mech position {'58, the end the visor opens to' if opened else '0, where the visor starts'}."
			)
			spatial = located("switch", address, f"switch.generic-{address}", "sensor")
			if spatial:
				extra["spatial"] = spatial
				notes += _spatial_note("switch", address)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, "used", refs, **extra))
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country configuration bit)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC Security CPU board", "switch_type": "dip",
					"notes": "CPU-board country DIP bank; the manual's DIP Switch Chart (inside cover) sets the country: America Off Off On On On On On On, European Off Off On On On Off On On, French Off Off On On On On Off Off, German Off Off On On On On On Off, Spain Off Off On On Off On On On (SW1-SW8).",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# The ROM's T.17 VISOR TEST behaviour with each position switch (visor-test run).
VISOR_SWITCH_EVIDENCE = {
	115: (
		"The ROM names it 'VISOR IS CLOSED' (F5 BLK-VIO ORN) in T.1 SWITCH EDGES while the host holds public 115 at 1, and in T.17 VISOR "
		"TEST it fills the CLOSED box while 115 is 1; running CLOSE, the ROM stops the visor motor (28) the moment 115 reads 1 and starts it "
		"again when 115 returns to 0, while running OPEN it ignores 115. So public 1 is the closed contact at the visor-closed end: the "
		"switch rests open and normally_closed is false."
	),
	117: (
		"The ROM names it 'VISOR IS OPEN' (F7 BLK-GRY ORN) in T.1 SWITCH EDGES while the host holds public 117 at 1, and in T.17 VISOR "
		"TEST it fills the OPEN box while 117 is 1; running OPEN, the ROM stops the visor motor (28) the moment 117 reads 1 and starts it "
		"again when 117 returns to 0, while running CLOSE it ignores 117. So public 1 is the closed contact at the visor-open end: the "
		"switch rests open and normally_closed is false."
	),
}


# --- Outputs -------------------------------------------------------------------------------------------
SOLENOID_NOTES = {
	1: "Ball release coil of the Outhole Ball Trough Assembly A-19963 (parts page 2-17 and the factory parts list; the Solenoid/Flashlamp Locations list 2-39 prints A-19663): kicks the lowest trough ball over the jam opto (31) into the shooter lane (switch 68).",
	3: "Eject coil (assembly A-20453) under the Game Saucer, the eject hole at the far upper left (switch 46), where the casino games are played.",
	4: "Reset coil of the drop target assembly A-20415 (2-39), whose 3-Bank Drop Target Assembly A-16032-1 (parts page 2-20, item 4 coil AE-26-1200) carries the 3-Bank Opto Assembly A-13609: raises the three drop targets (optos 16, 17, 18).",
	5: "Eject coil (assembly A-20453) under the right eye lock behind the visor (switch 48).",
	6: "Lift coil (AE-26-1200, coil and bracket B-9362-L-2) of the Ramp Lifting Mechanism Assembly B-11304 (RAISE RAMP): raises the left ramp.",
	7: "Knocker Assembly B-10686-1 (coil AE-23-800), wired to the backbox voltage and drive columns.",
	8: "Eject coil (assembly A-20453) under the left eye lock behind the visor (switch 47).",
	9: "Left slingshot kicker (coil and bracket B-9362-L-2) behind kick switch 65.",
	10: "Right slingshot kicker (coil and bracket B-9362-L-2) behind kick switch 64.",
	11: "Jet bumper coil (A-9415-2) of the lower jet bumper, switch 63.",
	12: "Jet bumper coil (A-9415-2) of the left jet bumper, switch 62.",
	13: "Jet bumper coil (A-9415-2) of the upper jet bumper, switch 61.",
	14: "The smaller coil SM1-26-600 of the Ramp Lifting Mechanism Assembly B-11304 (DROP RAMP): lets the raised left ramp drop; the mechanism's micro-switch (15) reports the ramp down.",
	15: "Right visor (eye) flasher: the table prints 'RIGHT VISOR FLSHR(2)', two #906 lamps on one Low Power driver.",
	16: "Left visor (eye) flasher: the table prints 'LEFT VISOR FLSHR(2)', two #906 lamps on one Low Power driver.",
	17: "Center visor flasher, one #906 at the middle of the visor.",
	18: "Pinbot face flasher, one #906 under the large Pinbot face insert in the middle of the playfield.",
	19: "Jet bumpers flasher, one #906 beside the jet bumpers.",
	20: "Lower left flasher, one #906 (assembly 04-10091.1) on the lower left playfield.",
	21: "Middle left flasher, one #906 (assembly 04-10091.1) on the left side.",
	22: "Lower right flasher, one #906 (assembly 04-10091.1) on the lower right playfield.",
	23: "Back panel flasher 1, the leftmost of five #906 domes on the playfield back panel.",
	24: "Back panel flasher 2 on the playfield back panel.",
	25: "Back panel flasher 3, the middle of the five back panel flashers.",
	26: "Back panel flasher 4 on the playfield back panel.",
	27: "Back panel flasher 5, the rightmost back panel flasher.",
	28: (
		"Visor motor 14-8023 on the Visor Motor Bracket Assembly A-20100, driven through the Motor EMI w/Brake PCB Assembly A-15340 "
		"(3-20: +12V on J1-3 from J118-2, drive on J1-1, motor leads J2-1 red and J2-2 black). One output and one motor direction: the "
		"motor turns the Motor Cam Assembly 04-10080, which works the visor through its lever arm and link (Visor Assembly C-11159, "
		"2-23), and the ROM stops it on the visor open (117) or closed (115) switch."
	),
}
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"bsTrough.SolOut\" releases a ball from the trough's BallRelease kicker",
	3: "SolCallback(3) = \"bsSaucer.SolOut\" kicks the ball out of the sw46 saucer",
	4: "SolCallback(4) = \"ResetDrops\" raises the three drop targets",
	5: "SolCallback(5) = \"bsREye.SolOut\" kicks the ball out of the sw48 saucer",
	6: "SolCallback(6) = \"solRampUp\" raises the modelled left ramp",
	7: "SolCallback(7) = \"SolKnocker\" plays the knocker sound",
	8: "SolCallback(8) = \"bsLEye.SolOut\" kicks the ball out of the sw47 saucer",
	14: "SolCallback(14) = \"solRampDwn\" lowers the modelled left ramp",
	28: "the visor cvpmMech mVisor takes .Sol1 = 28 (one solenoid, reversing, linear, 58 steps) with switches 115 at position 0 and 117 at 58",
	46: "SolCallback(sLRFlipper) = \"SolRFlipper\" (sLRFlipper = 46)",
	48: "SolCallback(sLLFlipper) = \"SolLFlipper\" (sLLFlipper = 48)",
}
SOLENOID_SCRIPT.update({address: "the callback is commented out; the table fires the coil from the switch's physics event, so the address has no binding" for address in (9, 10, 11, 12, 13)})
SOLENOID_SCRIPT.update({address: f"SolModCallback({address}) = \"Flasherset{address}\" fades the table's flasher objects for it" for address in range(15, 28)})
SOLENOID_ROLES = {7: "cabinet.knocker"}


def _rom_note(address: int) -> str:
	if address not in ROM_SOLENOID_NAMES:
		return ""
	name, wires = ROM_SOLENOID_NAMES[address]
	test = "T.5 FLASHER TEST" if address in T5_ADDRESSES else ("T.12 FLIPPER COIL TEST" if address in T12_ADDRESSES else "T.4 SOLENOID TEST")
	return f" {test}: the ROM pulses public {address} and prints \"{name}\" with the wires {wires}."


def _solenoid_wiring(address: int) -> dict[str, Any]:
	function, printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
	wiring: dict[str, Any] = {"board": DRIVER_BOARD, "control_wire": wire, "driver_transistor": transistor}
	if drive:
		wiring["control_connection"] = drive
	if voltage:
		wiring["power_connection"] = voltage
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in FLIPPER_COILS:
			stage, printed, transistor, control, wire, voltage, assembly = FLIPPER_COILS[address]
			side = "right" if address in {45, 46} else "left"
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			notes = (
				f"Lower {side} flipper {stage} winding (coil FL-11630, printed coil colour RED), printed Fliptronic circuit {printed} "
				f"(driver {transistor}, {control}, {wire}, supply {voltage}) on the {FLIPTRONIC_BOARD}. PinMAME publishes the lower flipper "
				f"windings at 45-48; the ROM's T.12 FLIPPER COIL TEST drives {'45 and 46' if side == 'right' else '47 and 48'} for "
				f"{side[0].upper()}. FLIP. POWER and only {'46' if side == 'right' else '48'} for {side[0].upper()}. FLIP. HOLD."
			) + _rom_note(address)
			if address in {45, 46}:
				notes += RIGHT_FLIPPER_PIN_NOTE
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE)
			if address in SOLENOID_SCRIPT:
				notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
				refs += (VPX_SCRIPT_SOURCE,)
			extra: dict[str, Any] = {
				"aliases": aliases + [{"namespace": "manual.address", "value": printed}],
				"physical": {"part_number": "FL-11630", "assembly_part_number": assembly, "notes": notes},
				"wiring": {"board": FLIPTRONIC_BOARD, "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage},
			}
			spatial = located("solenoid", address, identifier, "effect")
			if spatial:
				extra["spatial"] = spatial
				extra["physical"]["notes"] += _spatial_note("solenoid", address)
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		if address in UPPER_FLIPPER_CIRCUITS:
			stage, transistor, control, wire, voltage, side = UPPER_FLIPPER_CIRCUITS[address]
			label = NOT_USED_SOLENOID_LABELS[address]
			notes = (
				f"Fliptronic {side} flipper {stage} circuit (driver {transistor}, {control}, {wire}, supply {voltage}). The flipper block prints "
				f"'NOT USED' and no coil part for it, and the Flipper Circuit Diagram's note says the upper right and upper left flippers are "
				"not used; Jack•Bot has no upper flipper. jbGameData declares FLIP_SOL(FLIP_L) only, so PinMAME publishes here whatever the "
				"ROM writes to this Fliptronic drive bit, which its T.12 FLIPPER COIL TEST does not offer and no service-test run changed."
			) + (RIGHT_FLIPPER_PIN_NOTE if side == "upper right" else "")
			items.append(
				_device(
					output_id(label), label, "coil", SOLENOID_GROUP, address, "unused", (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE),
					aliases=aliases + [{"namespace": "manual.address", "value": str(address)}],
					physical={"notes": notes},
					wiring={"board": FLIPTRONIC_BOARD, "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage},
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		if address in VIRTUAL_SOLENOID_LABELS:
			label = VIRTUAL_SOLENOID_LABELS[address]
			used = address in {29, 30, 31, 49}
			notes = {
				29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here (wpc.c core_write_pwm_output of WPC_GILAMPS >> 5 at 29-30); it is not a Jack•Bot playfield device. The service-test runs saw it toggle in the menus.",
				30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Jack•Bot playfield device.",
				31: "PinMAME's synthetic game-on state: init_jb calls wpc_set_fastflip_addr(0x7b), so this channel reflects the ROM's fast-flip RAM flag, not a relay. The manual's printed flipper circuits 29-32 are the lower flippers at public 45-48.",
				32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
				49: "PinMAME's simulator ball-shooter channel (sim.h sShooterRel, CORE_FIRSTSIMSOL): jbSimData enables the manual-shooter simulation, so while PinMAME's simulator runs, sim.c pulses this channel on the shooter key's release and core_getSol publishes it. No physical circuit; the physical machine's ball enters play from the manual plunger.",
				50: "Reserved PinMAME output position before the first custom-output boundary; jbGameData declares no custom solenoids.",
			}.get(address)
			if notes is None:
				function, printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
				notes = (
					f"PinMAME's WPC-95 backward-compatibility mirror of LPDC output {address - 4} (core_getSol serves 41-44 from the 37-40 bits "
					f"for GEN_WPC95DCS as for GEN_WPC95); it can only repeat {address - 4}, which nothing drives on this machine, and no service-test "
					f"run changed it. The manual's table separately prints a row {address} 'NOT USED' ({printed_type}, {transistor}, {wire}) with no "
					"connection or part."
				)
			roles = ["internal.wpc-state"] if address in {29, 30, 31} else (["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else (["internal.simulator-ball-shooter"] if address == 49 else ["internal.unused.wpc-output"]))
			items.append(
				_device(
					output_id(label), label, "virtual", SOLENOID_GROUP, address, "used" if used else "unused", (CONTROLLER_SOURCE, CORE_SOURCE),
					aliases=aliases, roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
				)
			)
			continue
		if address in NOT_USED_SOLENOID_LABELS:
			label = NOT_USED_SOLENOID_LABELS[address]
			function, printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
			if address == 2:
				notes = (
					"Printed solenoid table entry 02 'NOT USED' (High Power, Q80, VIO-RED). The table still prints a voltage (J107-2) and drive "
					"(J130-2) connection for it, but the Power Driver Board connector list prints J130-2 'N/C', the locations list prints NOT USED "
					"with no coil or assembly, the drawing has no balloon 2, and the ROM's T.4 SOLENOID TEST skips it."
				)
			else:
				notes = (
					f"Printed solenoid table entry {address} 'NOT USED' ({printed_type}, {transistor}, {wire}) with no voltage or drive connection "
					"or part. PinMAME publishes the WPC-95 LPDC bit here for this hybrid generation; nothing on this machine drives it, the ROM's "
					"T.4 SOLENOID TEST does not offer it, and no service-test run changed it."
				)
			items.append(
				_device(
					output_id(label), label, "coil", SOLENOID_GROUP, address, "unused", (MANUAL_SOURCE, CORE_SOURCE, SOLENOID_TEST_SOURCE),
					aliases=aliases + [{"namespace": "manual.address", "value": f"{address:02d}"}],
					physical={"notes": notes}, wiring=_solenoid_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		function, printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
		notes = f"Printed solenoid table entry {address:02d} '{function}' ({printed_type}, driver {transistor}, wire {wire}). " + SOLENOID_NOTES[address]
		notes += _rom_note(address)
		if address in T5_ADDRESSES or address in T4_ADDRESSES:
			pass
		if address in SOLENOID_SCRIPT:
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
		kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address == 28 else "coil")
		coil, assembly = SOLENOID_ASSEMBLIES[address]
		physical: dict[str, Any] = {"assembly_part_number": assembly}
		if kind == "flasher":
			notes += " Printed flashlamp #906 (24-8802)."
			if address in FLASHER_COUNTS:
				physical["quantity"] = FLASHER_COUNTS[address]
		else:
			physical["part_number"] = coil
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_SCRIPT:
			refs += (VPX_SCRIPT_SOURCE,)
		if address in T4_ADDRESSES:
			refs += (SOLENOID_TEST_SOURCE,)
		if address in T5_ADDRESSES:
			refs += (FLASHER_TEST_SOURCE,)
		if address in {6, 14}:
			refs += (RAMP_TEST_SOURCE,)
			notes += RAMP_COIL_EVIDENCE[address]
		if address == 28:
			refs += (VISOR_TEST_SOURCE,)
			notes += VISOR_MOTOR_EVIDENCE
		if address in {9, 10, 11, 12, 13}:
			refs += (EDGES_SOURCE,)
		extra: dict[str, Any] = {"aliases": aliases + [{"namespace": "manual.address", "value": f"{address:02d}"}], "wiring": _solenoid_wiring(address)}
		if address in SOLENOID_ROLES:
			extra["roles"] = [SOLENOID_ROLES[address]]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			physical["location"] = "backbox"
		else:
			role = "emitter" if kind == "flasher" else "effect"
			spatial = located("solenoid", address, identifier, role)
			if spatial:
				extra["spatial"] = spatial
				notes += _spatial_note("solenoid", address)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, "used", refs, **extra))
	return items


RIGHT_FLIPPER_PIN_NOTE = (
	" Page 3-12's right flipper circuit prints the J902 pins of the left circuit (9, 7, 3, 1); the Flipper Circuit Diagram (3-11) "
	"and the Solenoid/Flashlamp Table print the right-side drives at J902-13 and J902-11 (lower right) and J902-6 and J902-4 (upper "
	"right), and the wire colours agree on every page, so the wiring follows 3-11 and the table and both readings stay in the excerpt."
)


RAMP_COIL_EVIDENCE = {
	6: (
		" T.16 RAMP TEST names it item 01 'RAMP UP': running, the test alternates 01 and 02 and pulses public 6 for each RAMP UP step "
		"(about 0.4 s), and in repeat mode RAMP UP pulses 6 alone. After the power-up the ROM pulsed 6 and 14 alternately while it looked "
		"for the ramp-down switch, which no mechanism answered in these runs."
	),
	14: (
		" T.16 RAMP TEST names it item 02 'RAMP DOWN': running, it pulses public 14 (about 0.06 s) for each RAMP DOWN step, and in repeat "
		"mode RAMP DOWN pulses 14 alone; the test shows 'RAMP DOWN SW.' while the ROM reads switch 15 closed."
	),
}
VISOR_MOTOR_EVIDENCE = (
	" The ROM's T.17 VISOR TEST drives public 28 for both OPEN and CLOSE and drops it when the selected end switch reads closed "
	"(117 for OPEN, 115 for CLOSE); T.4 and T.5 do not offer it. After the power-up the ROM held 28 for about 8 s while it looked for a "
	"visor switch, which no mechanism answered in these runs."
)


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"assembly_part_number": assembly}
			notes = (
				f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description "
				f'"{description}".'
			)
			if bulb:
				physical["quantity"] = 1
				notes += f" Printed bulb {bulb} ({'#555' if bulb == '24-8768' else '#44'})."
			rom_row = ("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")[row - 1]
			rom_column = ("BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY")[column - 1]
			notes += (
				f" The ROM's T.8 SINGLE LAMPS test lights public lamp {address} alone and prints \"{ROM_LAMP_NAMES[address]}\" with the wires "
				f"RED-{rom_row} YEL-{rom_column}."
			)
			if row in {4, 5}:
				notes += " The matrix prints the row driver of both rows 4 and 5 as Q87 and no row as Q85; the duplicated designator is kept as printed."
			if address in LAMP_MANUAL_MISPRINTS:
				matrix, listed = LAMP_MANUAL_MISPRINTS[address]
				notes += (
					f" The manual's Lamp Matrix prints this cell '{matrix}' and the Lamp Locations list '{listed}', but the ROM names it "
					f"'{ROM_LAMP_NAMES[address]}' and the retained table's light for it sits on the {ROM_LAMP_NAMES[address][-2:]} insert of its "
					"playfield art (2X upper left, 3X upper right, 4X lower left, 5X lower right around Shoot Again); the manual's own Lamp "
					f"Locations drawing points callout {address} at that same insert (the callout check validates the placement). The ROM and "
					"the table agree against the preliminary manual's printed cells, so the label follows them and the printed cells stay in "
					"the excerpts."
				)
			if address in LAMP_LIST_MISPRINTS:
				notes += (
					f" The Lamp Locations list prints '{LAMP_LIST_MISPRINTS[address]}', but the Lamp Matrix prints '{LAMP_MATRIX_TEXT[address]}' "
					f"and the ROM names it '{ROM_LAMP_NAMES[address]}'; the label follows the matrix and the ROM."
				)
			if column in {1, 2, 3, 4, 5} and row in {2, 3, 4, 5, 6}:
				notes += " One of the 25 chest matrix lamps (five colours in columns, five rows from 1 HIGH to 5 LOW) in Pinbot's chest, lit by the visor and 5-bank targets and used by Keno."
			if column in {1, 2, 3, 4, 5} and row == 1:
				notes += " One of the five coloured arrows below the visor."
			physical["notes"] = notes
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"physical": physical,
				"wiring": {
					"board": DRIVER_BOARD, "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in CABINET_LAMPS:
				extra["roles"] = [CABINET_LAMPS[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet button"
				physical["notes"] += " Lamp inside the lit " + ("Buy Extra Ball (buy-in) button, switch 23." if address == 87 else "Start button.")
			else:
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
					physical["notes"] += _spatial_note("lamp", address)
			label = LAMP_LABELS.get(address, description)
			items.append(
				_device(identifier, label, "lamp", LAMP_GROUP, address, "used", (MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE, VPX_SCRIPT_SOURCE), **extra)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (string, function, voltage, triac, drive, wire, bulb, rom_name, rom_wires) in GI_STRINGS.items():
		identifier = f"gi.string-{string}"
		notes = (
			f"Printed general-illumination string {string:02d} '{function}': triac {triac}, wire {wire}, voltage {voltage}, drive {drive}; "
			f"bulbs {bulb}. The ROM's T.6 GENERAL ILLUMINATION TEST names it '{rom_name}' ({rom_wires}) and steps the brightness of public "
			f"GI {address} alone."
		)
		notes += (
			" The Solenoid/Flashlamp Table prints the J120 pins under its PLAYFIELD connection columns and the J121 pins under BACKBOX, while "
			"the Power Driver Board connector list labels the J120 pins 'G.I. to insert panel' and the J121 pins 'G.I. to playfield'. For "
			"string 5 the table's own bulb column (#555 under BACKBOX, J120 its only non-cabinet connection) agrees with the connector list, so "
			"the table's column placement of the two connectors is the doubtful reading; which connector feeds which panel is a wiring detail "
			"that changes no address, and the wiring fields name both connectors without a location."
		)
		if address == 4:
			notes += (
				" The INSERT string lights the backbox insert panel (#555, 24-8768 on the locations list); its cabinet branch J119 goes to the "
				"Coin Door Interface Board (J119-1 'G.I. to Coin Door Brd J2-5')."
			)
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, GI_TEST_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{string:02d}"}],
			"wiring": {"board": DRIVER_BOARD, "driver_transistor": triac, "control_connection": drive, "control_wire": wire, "power_connection": voltage},
		}
		if address == 4:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			extra["physical"] = {"location": "backbox", "notes": notes}
		else:
			spatial = located("gi", address, identifier, "emitter")
			if spatial:
				refs += (VPX_SCRIPT_SOURCE,)
				extra["spatial"] = spatial
				notes += (
					f" The retained table's UpdateGi drives its {GI_TABLE_COLLECTIONS[address]} light collection for string number {address}; "
					"the placements are those lights with stacked render doubles collapsed, kept observed and without a quantity because the "
					"manual prints no per-string bulb count and no drawing locates G.I. bulbs, and the table's grouping is the author's."
				)
			extra["physical"] = {"notes": notes}
		items.append(_device(identifier, f"General Illumination String {string} ({function.title()})", "gi", GI_GROUP, address, "used", refs, **extra))
	return items


GI_TABLE_COLLECTIONS = {0: "GI_Bottom", 1: "GI_Left", 2: "GI_Upper", 3: "GI_Right"}


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		}
	]


# --- Mechanisms, drivers and conflicts -------------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _mechanism(
	suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...],
	positions: list[tuple[str, str, list[str], str]] | None = None, assembly: str | None = None, status: str = "observed",
) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		"behavior": behavior, "provenance": provenance(status, *refs),
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


VISOR_BEHAVIOR = (
	"Pinbot's visor (Visor Assembly C-11159 with the Moving Target Assembly C-11157 and the Visor Motor Bracket Assembly A-20100) covers "
	"his eyes, the two eye locks. Five visor targets (41-45, left to right) on its front face the playfield. One motor (14-8023, "
	"solenoid 28, driven through the Motor EMI w/Brake board A-15340) turns in one direction only and moves the visor through a cam "
	"(Motor Cam Assembly 04-10080) and the visor's lever arm and link, so each run of the motor carries the visor from one end to the other; two micro-switches on the motor bracket report the ends, "
	"Visor Closed (F5, public 115) and Visor Open (F7, public 117), which are the Fliptronic upper-flipper end-of-stroke inputs reused "
	"because Jack•Bot has no upper flippers. The ROM runs the motor until the wanted end switch closes: T.17 VISOR TEST stops 28 on "
	"117 when opening and on 115 when closing and ignores the other switch. Rules: visor-target and 5-bank hits light the 5x5 chest "
	"matrix; completing it opens the visor and reveals the eye locks (47, 48), whose balls start multiball; Mega Visor raises it again "
	"after 15 Jack•Bots. Three flashers light it: right and left visor (15, 16, two lamps each) and center visor (17). The retained "
	"table models the visor as a one-solenoid reversing linear mech of 58 steps with 115 at the closed end and 117 at the open end; that "
	"is a synthetic model, and no source gives the physical travel time."
)
RAMP_BEHAVIOR = (
	"The left ramp to the upper mini-playfield lifts. The Ramp Lifting Mechanism Assembly B-11304 carries a lift coil (AE-26-1200 on a "
	"B-9362-L-2 bracket, solenoid 6, RAISE RAMP), a smaller coil with an armature (SM1-26-600, solenoid 14, DROP RAMP) and a micro-switch "
	"(5647-12001-00, public 15, RAMP IS DOWN) that is made while the ramp is down. Down, the ramp is a shot: the ball rolls past the ramp "
	"entrance (37) to the mini-playfield and leaves past the ramp exit (36); raised, it opens the way to the Cashier target under it (38), the rules' shot 'under the ramp'. Pulsing 6 raises "
	"the ramp and pulsing 14 lets it drop again. T.16 RAMP TEST cycles RAMP UP "
	"(6) and RAMP DOWN (14) and reports RAMP DOWN SW. while 15 is closed. Lamps 75 (Game Saucer) and 76 (Mega Ramp) light the sign over "
	"the ramp entrance, and 71-74 the mini-playfield awards. The retained table models the ramp angle with a timer and writes 15 from it."
)


def mechanisms() -> list[dict[str, Any]]:
	flipper_refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE)
	return [
		_mechanism(
			"visor", "Pinbot's visor", "motorized",
			[_coil(28), _coil(15), _coil(16), _coil(17)],
			["switch.generic-115", "switch.generic-117"] + _matrix(41, 42, 43, 44, 45, 47, 48),
			VISOR_BEHAVIOR,
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, VISOR_TEST_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE),
			[
				("closed", "Closed", ["switch.generic-115"], "Visor down over the eyes; its five targets face the playfield; the Visor Closed switch (F5, 115) is made."),
				("open", "Open", ["switch.generic-117"], "Visor raised, revealing the left and right eye locks (47, 48); the Visor Open switch (F7, 117) is made."),
			],
			"A-20100",
		),
		_mechanism(
			"lifting-ramp", "Lifting left ramp to the mini-playfield", "diverter", [_coil(6), _coil(14)], _matrix(15, 37, 36, 38),
			RAMP_BEHAVIOR,
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, RAMP_TEST_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("down", "Down", _matrix(15), "Ramp lowered onto the playfield so a shot can travel up it; the Ramp Is Down micro-switch (15) is made."),
				("up", "Up", [], "Ramp lifted and latched, opening the Cashier shot under it (target 38); switch 15 is open."),
			],
			"B-11304",
		),
		_mechanism(
			"drop-targets", "3-bank drop targets", "kicker", [_coil(4)], _matrix(16, 17, 18),
			"Three drop targets on the left side (high 16, center 17, low 18) read by the optos of the 3-Bank Opto Drop Target Board A-13609, "
			"and one reset coil (solenoid 4, DROP TARGETS) that raises all three. Rules: with all three up a single target lamp (77, 78, 68) "
			"moves back and forth, and hitting that target first advances the bonus multiplier; once a target is down a timer runs on the "
			"other two, and completing the bank before it expires awards a card. The retained table models each target's drop and sets its "
			"switch once the target is down.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			None, "A-20415",
		),
		_mechanism(
			"ball-trough", "Outhole ball trough", "kicker", [_coil(1)], _matrix(31, 32, 33, 34, 35),
			"Outhole Ball Trough Assembly A-19963 with four balls: drained balls roll onto the Trough 1-4 optos (32 at the right, 35 at the "
			"left) and the ball release coil (1) kicks the rightmost ball over the jam opto (31) into the shooter lane (68). The optos are IR "
			"pairs on the Trough IR LED Board A-18617-1 and Photo Transistor Board A-18618-1, read through the 7-Opto Switch Board A-15595; "
			"the board's ball 5 and 6 positions are not wired.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("jam", "Jam", _matrix(31), "A ball over the release coil."),
				("trough-1", "Trough 1", _matrix(32), "At least one ball in the trough."),
				("trough-2", "Trough 2", _matrix(33), "At least two balls."),
				("trough-3", "Trough 3", _matrix(34), "At least three balls."),
				("trough-4", "Trough 4", _matrix(35), "All four balls."),
			],
			"A-19963",
		),
		_mechanism(
			"game-saucer", "Game Saucer", "kicker", [_coil(3)], _matrix(46),
			"The eject hole at the far upper left (switch 46, eject coil 3, which the ROM's T.4 names GAME SAUCER). Shooting the ramp lights it; "
			"the jet bumpers or the left flipper button move the flashing game lamp among Pinbot Poker, Slot Machine, Roll The Dice and Keno "
			"(lamps 81-84), and after all four Casino Run (66). Shooting it then plays the selected game.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "A-20453",
		),
		_mechanism(
			"eye-locks", "Eye locks", "kicker", [_coil(8), _coil(5)], _matrix(47, 48),
			"Two eject holes behind the visor, Pinbot's eyes: the left eye lock (switch 47, eject coil 8) and the right eye lock (switch 48, "
			"eject coil 5). They are reachable only while the visor is open; balls locked there start multiball, and during multiball both "
			"eyes are Jack•Bot shots (hitting two holes at once awards a Super Jack•Bot). Either eye also spins the Casino Run slot machine.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			[
				("left-eye", "Left eye", _matrix(47), "Left eye lock, eject coil 8."),
				("right-eye", "Right eye", _matrix(48), "Right eye lock, eject coil 5."),
			],
			"A-20453",
		),
		_mechanism(
			"vortex", "Vortex skill shot", "other", [], _matrix(56, 57, 58),
			"The plunger shoots the ball around the top into the Vortex, three holes (upper 56, center 57, lower 58). The upper and lower "
			"holes award the Vortex Millions value and the center hole three times it (operator multipliers 1X, 3X, 1X by default); the "
			"display shows each hole's value during the skill shot. With less than ten seconds of Casino Run left and the ball at the "
			"shooter, the center hole collects the Bank. No coil serves the Vortex; the holes return the ball to the playfield.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE),
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)],
			["switch.generic-111", "switch.generic-112", "switch.generic-116"],
			"Flipper assembly A-15849-R with an FL-11630 coil (power 45, hold 46, printed circuits 29-30) and an SW-1A-194 end-of-stroke "
			"switch (F1, 111) that PinMAME synthesizes. The cabinet button interrupts both optos of the right Flipper Opto Board A-17316 "
			"(F2, 112 and F6, 116).",
			flipper_refs, None, "A-15849-R",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)],
			["switch.generic-113", "switch.generic-114", "switch.generic-118"],
			"Flipper assembly A-15849-L with an FL-11630 coil (power 47, hold 48, printed circuits 31-32) and an SW-1A-194 end-of-stroke "
			"switch (F3, 113) that PinMAME synthesizes. The cabinet button interrupts both optos of the left Flipper Opto Board A-17316 "
			"(F4, 114 and F8, 118); the left button also moves the flashing Game Saucer lamp.",
			flipper_refs, None, "A-15849-L",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(9), _coil(10)], _matrix(65, 64),
			"Two slingshots (coil and bracket B-9362-L-2): left kicker 9 behind kick switch 65, right kicker 10 behind kick switch 64; each "
			"address carries the kick switch SW-1A-114 and the score switch SW-1A-120.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "B-9362-L-2",
		),
		_mechanism(
			"jet-bumpers", "Jet bumpers", "other", [_coil(13), _coil(12), _coil(11)], _matrix(61, 62, 63),
			"Three jet bumpers (A-9415-2 coils) on the right: upper 61 with coil 13, left 62 with coil 12, lower 63 with coil 11. Jet hits "
			"raise the Dice Wager and move the Game Saucer's flashing game lamp; a ball that falls from the mini-playfield into the jets "
			"builds Solar Jets. Flasher 19 lights them.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "A-9415-2",
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
TRANSCRIBED = "curator, read from the rendered page"
DRAWING_DERIVATIONS = {
	"switch-locations": "page 115, crop box 0.42,0.09,0.93,0.88, scanned page rendered at its native resolution (embedded image xref 570, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1301x2607 WebP quality 80",
	"lamp-locations": "page 113, crop box 0.42,0.07,0.95,0.9, scanned page rendered at its native resolution (embedded image xref 560, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1352x2739 WebP quality 80",
	"solenoid-flashlamp-locations": "page 117, crop box 0.44,0.09,0.99,0.79, scanned page rendered at its native resolution (embedded image xref 580, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1403x2310 WebP quality 80",
}


def _excerpt(name: str, locator: str, *, image: bool = False, method: str = "manual", reviewed: bool = True, credit: str = TRANSCRIBED) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.jackbot.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = f"{MANUAL_NAME} {DRAWING_DERIVATIONS[name]}"
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("switch-matrix", "PDF page 114, printed 2-36, Switch Matrix with the dedicated and flipper grounded-switch blocks and the measured opto shading; reprints PDF 120 (3-2) and PDF 149 compared; PDF 121 (3-3) dedicated switches"),
		_excerpt("lamp-matrix", "PDF page 112, printed 2-34, Lamp Matrix; reprints PDF 122 (3-4) and PDF 149 compared"),
		_excerpt("solenoid-flasher-table", "PDF page 116, printed 2-38, Solenoid/Flashlamp Table with the general-illumination and flipper-circuit blocks; reprints PDF 123 (3-5) and the inside-cover sheet (PDF 2) compared"),
		_excerpt("switch-locations", "PDF page 115, printed 2-37 (Switch Locations parts list and playfield drawing; image)", image=True),
		_excerpt("lamp-locations", "PDF page 113, printed 2-35 (Lamp Locations parts list and playfield drawing with the chest inset; image)", image=True),
		_excerpt("solenoid-flashlamp-locations", "PDF page 117, printed 2-39 (Solenoid/Flashlamp Locations lists and playfield drawing; image)", image=True),
		_excerpt("power-driver-board", "PDF pages 146-148, printed 3-28 to 3-30, Power Driver Board connector list"),
		_excerpt("section-3-boards", "PDF pages 121-141, printed 3-3 to 3-23: dedicated switches, coil and flashlamp wiring, G.I. and flipper circuits, flipper opto boards, trough and 7-opto boards, Motor EMI board and visor motor circuit, 3-bank opto drop target board, coin door interface"),
		_excerpt("mechanism-assemblies", "PDF pages 95, 98, 99 and 101, printed 2-17, 2-20, 2-21 and 2-23: the outhole ball trough, 3-bank drop target, ramp lifting mechanism, visor, moving target and visor motor bracket assembly parts lists"),
		_excerpt("service-tests", "PDF pages 37 and 45-49, printed 1-8 and 1-16 to 1-20, the menu system and the Test menu T.1-T.18", reviewed=False),
		_excerpt("game-rules", "PDF pages 12-28, printed A-Q, rules and shot maps", reviewed=False),
		_excerpt("game-operation", "PDF pages 35-36 (1-6, 1-7), game control locations and game operation; PDF 2 DIP switch chart and EPROM jumpers; PDF 30 (1-1) ROM summary", reviewed=False),
	]


RUNTIME_SOURCES = (
	(EDGES_SOURCE, "switch-edges-sweep", "One hash-pinned LibPinMAME harness run of jb_10r from empty NVRAM with built-in mechanisms disabled (tools/harness-scenarios/wpc-95/jb-switch-edges-sweep.json): inside T.1 SWITCH EDGES the coin switches 1-4, every public matrix address 11-88 and every Fliptronic address 111-118 are set to 1 and back to 0 for 2 s each. The ROM names each fitted switch at public 1 (24 on its 1 -> 0 edge; the end-of-stroke bits 111 and 113, which PinMAME rewrites from the flipper coils, are never named), names nothing for 71-88, fires the jet and sling coils for their switches and the lower flippers for 112/116 and 114/118."),
	(SOLENOID_TEST_SOURCE, "solenoid-test", "One hash-pinned run of jb_10r (jb-solenoid-test.json) stepping T.4 SOLENOID TEST: it walks 1 and 3-14, naming each driver and its wires and pulsing that public address, and wraps."),
	(FLASHER_TEST_SOURCE, "flasher-test", "One hash-pinned run of jb_10r (jb-flasher-test.json) stepping T.5 FLASHER TEST through 15-27, each named with its wires and pulsed alone, and wrapping to 15."),
	(FLIPPER_TEST_SOURCE, "flipper-coil-test", "One hash-pinned run of jb_10r (jb-flipper-coil-test.json) stepping T.12 FLIPPER COIL TEST: R. FLIP. POWER drives 45 and 46, R. FLIP. HOLD 46, L. FLIP. POWER 47 and 48, L. FLIP. HOLD 48; nothing offers or publishes 33-36."),
	(GI_TEST_SOURCE, "gi-test", "One hash-pinned run of jb_10r (jb-gi-test.json) stepping T.6 GENERAL ILLUMINATION TEST: PLAYFIELD LOWER, LEFT, UPPER, RIGHT and INSERT each dim public GI 0-4 alone."),
	(LAMP_TEST_SOURCE, "single-lamps", "One hash-pinned run of jb_10r (jb-single-lamps.json) stepping T.8 SINGLE LAMPS through public lamps 11-88 in matrix order, each lit alone with its name, test number and row and column wires printed."),
	(RAMP_TEST_SOURCE, "ramp-test", "One hash-pinned run of jb_10r (jb-ramp-test.json): T.16 RAMP TEST alternates 01 RAMP UP (public 6) and 02 RAMP DOWN (public 14), shows RAMP DOWN SW. while the host holds public 15 at 1, and in repeat mode pulses only the selected coil."),
	(VISOR_TEST_SOURCE, "visor-test", "One hash-pinned run of jb_10r (jb-visor-test.json): T.17 VISOR TEST drives the visor motor 28 for OPEN and CLOSE, stops it when public 117 (OPEN) or 115 (CLOSE) reads 1, ignores the other switch, and marks the OPEN and CLOSED boxes from 117 and 115."),
)


def source_records() -> list[dict[str, Any]]:
	def pdf(source_id: str, kind: str, name: str, locator: str, sha: str, excerpts: list[dict[str, Any]]) -> dict[str, Any]:
		return {
			"id": source_id,
			"kind": kind,
			"uri": f"external:{MANUALS_DIRECTORY}/{name}",
			"original_filename": name,
			"sha256": sha,
			"acquired_at": ACQUIRED_AT,
			"locator": locator + f" Direct resource: {WAYBACK_FILES[name]}.",
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
			"excerpts": excerpts,
		}

	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the jb_* clone tree (jb_10r parent; jb_101r, jb_10b, jb_101b, jb_04a)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/jb.c (a preliminary simulator whose switch and solenoid symbols are not this machine's wiring) "
				"jbGameData: GEN_WPC95DCS, wpc_dispDMD, FLIP_SW(FLIP_L|FLIP_U) | FLIP_SOL(FLIP_L), no custom switch columns, lamp columns or "
				"solenoids, no mechanism, the inverted-switch mask {0x00,0xe0,0x00,0x1f,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00} (column 1 "
				"rows 6-8 and column 3 rows 1-5, public 16-18 and 31-35 under wpc_sw2m), init_jb calling wpc_set_fastflip_addr(0x7b), and the "
				"five drivers with wpc_m95DCSS (jb_04a commented 'WPC-S 5-Board'); src/wpc/wpc.c WPC_FLIPPERSW95 returning "
				"~swMatrix[CORE_FLIPPERSWCOL], the 29-31 state mirror and the jb_ PWM typing of solenoids 15-24 as #89 bulbs (a brightness "
				"model); src/wpc/core.c core_getSol (37-40 mirrored at 41-44 for the WPC-95 generations) and core_updateSw (lower-flipper "
				"end-of-stroke synthesis). The runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-95.json", "revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "revision": "Wayback capture, 2024",
			"sha256": IPDB_PAGE_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"IPDB machine 3619 'Jack·Bot' (Williams Electronics Games, October 10, 1995, model 50051, MPU Williams WPC Security, "
				f"2,428 units, four players). IPDB is Cloudflare-gated, so the page was read from the Wayback capture {IPDB_WAYBACK} "
				"(retained as ipdb-3619.html). Its title, date and model number match the manual cover (16-50051-101) and the machine "
				"being curated; its notes say some production games were built with WPC-95 board sets and describe two playfield versions "
				"(white or coloured arrow inserts below the visor targets) and two ramp plastics."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine 3619 page, title line to file and image lists", reviewed=False, credit="curator, from the retained HTML")],
		},
		pdf(
			MANUAL_SOURCE, "manual", MANUAL_NAME,
			"Williams Jack•Bot operations manual, May 1995 PRELIMINARY, document 16-50051-101: a 150-page image-only scan (300 dpi, "
			"1-bit) with Section 1 (game operation and tests), Section 2 (parts, PDF 79-118, printed 2-N at PDF 78+N) and Section 3 "
			"(wiring, PDF 119-149, printed 3-N at PDF 118+N). It documents the WPC Security five-board set.",
			MANUAL_SHA256, _manual_excerpts(),
		),
		pdf(
			BULLETIN_SOURCE, "service_bulletin", BULLETIN_NAME,
			"Service Bulletin 86 (January 11, 1996): premature loss of battery voltage on the WPC-95 CPU board (bare board 5764-14533-08) "
			"of Jack•Bot and Congo sample games manufactured before 12-15-95, with the D28 diode and R129 resistor modification. It "
			"changes no switch, lamp or solenoid and shows that sample games carried WPC-95 CPU boards.",
			BULLETIN_SHA256,
			[_excerpt("service-bulletin-86", "Single page", method="ocr", reviewed=False, credit="curator; the PDF text layer")],
		),
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/williams/jackbot-1995/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine (VPU file 7953, version 1.1.2a of February 22, 2022; info "
				f"table_version 1.1.2). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and "
				f"y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION", "attribution": "bord, with the update by leojreimroc", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/jackbot-1995/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				'Retained embedded script (4,720 lines). Runtime and mechanism-causality authority: Const cGameName="jb_10r", '
				"UseSolenoids=2, UseLamps=0, UseVPMModSol=1, HandleMechanics=0, the SolCallback table, SolModCallback 15-27 for the "
				"flashers, the cvpmBallStack trough and three saucers, the visor cvpmMech on solenoid 28 with switches 115 and 117, the "
				"RampTimer ramp model writing switch 15, the ChangedLamps/SetLamp lamp loop and UpdateGi for G.I. strings 0-3. The pinned "
				"script corpora (vpxtable_scripts and vpx-standalone-scripts) carry the same binding statements."
			),
			"license": "NOASSERTION", "attribution": "bord and leojreimroc", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/jackbot-1995/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	] + [
		{
			"id": source_id, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/jackbot-jb_10r-{name}.json",
			"revision": PINMAME_REVISION, "locator": locator, "license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		}
		for source_id, name, locator in RUNTIME_SOURCES
	] + [
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/williams/jackbot-1995-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of the manual's drawings 2-35, 2-37 and 2-39 (the committed 300 dpi "
				"excerpt crops): every callout transcribed by an independent reader working only from the page, per-page control fits from "
				"the jet bumper caps and flipper pivots, and the callout fit; a table placement whose own callout lands within 0.07 "
				"normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and generators are retained under "
				"review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION", "attribution": "PinMAME game definitions contributors",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Jack•Bot",
			"manufacturer": "Williams",
			"year": 1995,
			"kind": "physical_pinball",
			"ipdb_id": 3619,
			"opdb_id": "GRKOX-MLyrW",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["variant_differences", "spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "observed",
				"variant_coverage": "candidate",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.wpc-95", "hardware_generation": "0x40", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/jackbot-1995.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Jack*Bot device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Jack*Bot mechanism {mechanism['id']} names unknown devices: {unknown}")
	seed = load_json(CALLOUT_SEED_PATH)
	measured = {placement_id: drawing_callouts.measured(seed, placement_id) for placement_id in seed.get("measurements", {})}
	placed = drawing_callouts.placements_of(definition)
	for placement_id, value in measured.items():
		if placed.get(placement_id) != value:
			raise RuntimeError(f"Jack*Bot measured placement {placement_id} is {placed.get(placement_id)}, but its drawing read reproduces {value}")
	drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
UNRESOLVED_GEOMETRY = [
	"The G.I. placements of strings 1-4 rest on the retained table's own grouping; no factory drawing or bulb count locates G.I. bulbs, so they stay observed.",
	"Placements the drawings do not confirm keep their observed status; each such device's note says what the drawing showed.",
]
PROJECTION_CLASSES = {
	"switch": "The retained table's collision object for the switch (trigger, target, drop-target wall, saucer kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are projected onto the trough's BallRelease kicker because the script derives them from a ball count. Switches with no live table object (the rubber switches 11, 12 and 66, the ramp-down switch 15 and the visor switches 115 and 117) are measured on the switch drawing.",
	"lamp": "The script-driven Light's own centre (the smaller-falloff member of each render double), validated where the lamp drawing marks the same insert; the drawing's chest-matrix inset is not at playfield scale and checks nothing. The mini-playfield lamps 71-74 and the lamps 75 and 76, which the table draws without a Light, take the bulb or sign object the script drives.",
	"solenoid": "The object the solenoid callback moves (saucer kicker, drop-target wall, flipper, bumper, slingshot), the flasher dome primitive or the Light the script fades, validated where the solenoid drawing's callout agrees. The ramp coils 6 and 14, the visor motor 28 and the visor flashers 15-17, for which the table has no usable object, are measured on the solenoid drawing; the back-panel flashers 23-27 sit on the table's back-panel domes and the drawing's back-panel strip is not at playfield scale.",
	"gi": "Per-string collections of the table's UpdateGi lights for strings 1-4, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates G.I. bulbs. String 5 lights the backbox insert panel and is not placed.",
}


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"] + definition["displays"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device.get("availability", "used") in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	seed = load_json(CALLOUT_SEED_PATH)
	check = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
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
			"manifest_uri": "external:pinmame-vpx-sources/williams/jackbot-1995/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/williams/jackbot-1995-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": PROJECTION_CLASSES,
		"unresolved_geometry": UNRESOLVED_GEOMETRY,
		"promotion_decision": "partial: every fitted device has an observed or validated placement or a controlled not-applicable record, but no general-illumination placement can be validated from any retained drawing or count.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Jack•Bot (Williams, 1995) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places "
		"(factory-drawing measurements to three).",
		"",
		"## Placement status",
		"",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(report['without_placements'])}" + (f" ({', '.join(f'`{item}`' for item in report['without_placements'])})" if report["without_placements"] else ""),
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
		raise RuntimeError(f"Refusing to overwrite an author-ready Jack*Bot artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Jack*Bot author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Jack*Bot deterministic artifact drift: {path}")
	print("Jack*Bot definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Jack*Bot extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Jack*Bot retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
