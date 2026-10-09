"""Curate the physical Bally NBA Fastbreak (1997) machine definition.

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

MACHINE_ID = "bally.nba-fastbreak.1997"
PARTIAL_PATH = ROOT / "machines/partial/bally/nba-fastbreak-1997.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/nba-fastbreak-1997.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/nba-fastbreak-1997.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/bally/nba-fastbreak-1997.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/bally/nba-fastbreak-1997-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/nba-fastbreak-1997-callouts.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/bally/nba-fastbreak-1997-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/nba-fastbreak-1997.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/nba-fastbreak-1997.md"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
IDENTITY_SOURCE = "identity.bally.nba-fastbreak.1997"
MANUAL_SOURCE = "manual.bally.nba-fastbreak.1997"
MANUAL_MARCH_SOURCE = "manual-march.bally.nba-fastbreak.1997"
BULLETIN_SOURCE = "service-bulletin-99.bally.nba-fastbreak.1997"
VPX_TABLE_SOURCE = "vpx-table.nbaf-vpw-1-3"
VPX_SCRIPT_SOURCE = "vpx-script.nbaf-vpw-1-3"
VPX_EXTRACTION_SOURCE = "vpx-extraction.nbaf-vpw-1-3"
EDGES_SOURCE = "runtime.nba-fastbreak.switch-edges-sweep"
SOLENOID_TEST_SOURCE = "runtime.nba-fastbreak.solenoid-test"
BLINKED_SOURCE = "runtime.nba-fastbreak.blinked-names"
FLASHER_TEST_SOURCE = "runtime.nba-fastbreak.flasher-test-sweep"
FLIPPER_TEST_SOURCE = "runtime.nba-fastbreak.flipper-coil-test"
GI_TEST_SOURCE = "runtime.nba-fastbreak.gi-test"
LAMP_TEST_SOURCE = "runtime.nba-fastbreak.single-lamps"
MOTOR_TEST_SOURCE = "runtime.nba-fastbreak.motor-test"
BACKBOX_TEST_SOURCE = "runtime.nba-fastbreak.backbox-test"
EARLIER_EDGES_SOURCE = "runtime.nba-fastbreak.nbaf-31.switch-edges"
EARLIER_FLASHER_SOURCE = "runtime.nba-fastbreak.nbaf-31.flasher-test"
CALLOUT_SOURCE = "drawing-callouts.nba-fastbreak.2026-10-09"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-95"

TABLE_NAME = "NBA Fastbreak (Bally 1997)_VPWmod_v1.3.vpx"
ANCESTOR_TABLE_NAME = "NBA Fastbreak (Bally 1997)_VPWmod_v1.17.0.vpx"
TABLE_SHA256 = "d4d242abc77c106d195310d6d8a66cd2d8c1ffadf9ec8ac8aacc588cc87cb912"
ANCESTOR_TABLE_SHA256 = "9553e3c6aa0ed991a43a6b10ebb308b3c2acde3e10310a18bb8ff40d5b54ae8d"
SCRIPT_SHA256 = "69537260b7bc976a136a8ea1a4bd63ce7e0c09f81c766eafcbb765e9cb0b1a31"
MANUAL_NAME = "Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf"
MANUAL_SHA256 = "c901d3301766fec9c55dea8d8be22e08cbdf1edfd1dee5c67716fa3f728ad551"
MANUAL_MARCH_NAME = "Bally_1997_NBA_Fastbreak_Operations_Manual_Final_no_schematics.pdf"
MANUAL_MARCH_SHA256 = "49919913e84821cd849b665f9dd7477d6bdeb2957615efad9d7e29e482dae8d7"
BULLETIN_NAME = "Bally_1997_NBA_Fastbreak_Service_Bulletin_99.pdf"
BULLETIN_SHA256 = "90feb58ec3b55a9bdcf12281b1fe1c3f08936848a8b50de382bdb4bf47c7c370"
IPDB_PAGE_SHA256 = "4cc3480cc89151e02bf730ab20ff21df074b1f6d8d6736d56c3fa855b568d0a8"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/bally.nba-fastbreak.1997/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4023"
IPDB_WAYBACK = "https://web.archive.org/web/2025/https://www.ipdb.org/machine.cgi?id=4023"
WAYBACK_FILES = {
	MANUAL_NAME: "https://web.archive.org/web/20251122120230id_/https://www.ipdb.org/files/4023/" + MANUAL_NAME,
	MANUAL_MARCH_NAME: "https://web.archive.org/web/20251127000829id_/https://www.ipdb.org/files/4023/" + MANUAL_MARCH_NAME,
	BULLETIN_NAME: "https://web.archive.org/web/20251122092136id_/https://www.ipdb.org/files/4023/" + BULLETIN_NAME,
}
ACQUIRED_AT = "2026-10-09T15:41:00Z"
RIGHTS_NOTE = "Midway Manufacturing Company (trade name Bally); scan hosted by the Internet Pinball Machine Database"
PLAYFIELD_WIDTH = 964.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

EXTRACTION_FILE_COUNT = 2237
EXTRACTION_TOTAL_BYTES = 232890841
EXTRACTION_MANIFEST_SHA256 = "37bb4b83816dfdbd700b116035f026d71346292dda861b37bdb6057bab906ac1"
EXTRACTION_RELATIVE_PATH = Path("bally/nba-fastbreak-1997/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/nba-fastbreak-1997/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("nbaf_31", "nbaf_11", "nbaf_11a", "nbaf_11s", "nbaf_115", "nbaf_21", "nbaf_22", "nbaf_23")
LINKED_NOTE = (
	" From game ROM 2.1 the firmware supports linked head-to-head play with a second machine, which needs the NBA Fastbreak "
	"Linking Kit 58030 (an exchanged G11 game ROM and S2 sound ROM, a max239 line driver and a 16C450 UART added to the "
	"Audio/Visual board, and a cable on J607); the manual says a linked game can also be played alone, and PinMAME emulates no "
	"link port, so the standalone machine's I/O is unchanged."
)
DRIVER_COMPATIBILITY = {
	"nbaf_31": (
		"identical",
		"Production game ROM 3.1 with sound ROM S2 3.0 (English and German speech), the parent driver. The retained known-working VPW "
		'table binds it directly (Const cGameName = "nbaf_31"), and every service-test run behind this definition booted it.' + LINKED_NOTE,
	),
	"nbaf_11": ("identical", "Production game ROM 1.1, the first production release, with sound ROM S2 1.0; same wpc_m95S hardware and I/O."),
	"nbaf_11a": (
		"identical",
		"Game ROM 1.1 with the German-speech sound ROM S2 2.0; pinned nbaf.c calls it basically S1.0 with German speech. Same hardware and I/O.",
	),
	"nbaf_11s": (
		"identical",
		"Game ROM 1.1 paired with the prototype sound ROM S0.4; pinned nbaf.c notes that S0.4 is only parked here and belongs with "
		"prototype game code. The sound ROM is firmware on the same DCS sound hardware, so the physical machine is unchanged.",
	),
	"nbaf_115": ("identical", "Game ROM 1.15 with sound ROM S2 1.0; same hardware and I/O."),
	"nbaf_21": ("identical", "Game ROM 2.1 with sound ROM S2 3.0." + LINKED_NOTE),
	"nbaf_22": ("identical", "Game ROM 2.2 with sound ROM S2 3.0." + LINKED_NOTE),
	"nbaf_23": ("identical", "Game ROM 2.3 with sound ROM S2 3.0." + LINKED_NOTE),
}

# --- Switch data (switch-locations.md, switch-matrix.md, section-3-boards.md) ---------------------------
# address -> (assembly or opto assembly cell, switch part number cell, printed description), Switch Locations list (2-42).
SWITCH_LOCATIONS = {
	11: ("20-10327-4", "-----", "BALL LAUNCH"), 12: ("A-21710", "5647-12693-19", "BACKBOX BASKET"),
	13: ("20-9663-16", "-----", "START BUTTON"), 14: ("-----", "04-10346", "PLUMB BOB TILT"),
	15: ("A-17791", "5647-12693-32", "SHOOTER LANE"), 16: ("A-17813", "5647-12693-19", "LEFT RETURN LANE"),
	17: ("A-17813", "5647-12693-19", "RIGHT RETURN LANE"), 18: ("A-18019-6", "-----", "LOWER RIGHT STANDUP TARGET"),
	21: ("A-17238", "-----", "SLAM TILT"), 22: ("-----", "5643-09268-00", "COIN DOOR CLOSED"),
	23: ("A-16443-1", "SW-11A-37-1", "RIGHT JET BUMPER"), 24: ("-----", "5643-15190-00", "ALWAYS CLOSED"),
	25: ("-----", "5647-12693-66", "EJECT HOLE"), 26: ("A-17813", "5647-12693-19", "LEFT OUTLANE"),
	27: ("A-17813", "5647-12693-19", "RIGHT OUTLANE"), 28: ("A-18019-6", "-----", "UPPER RIGHT STANDUP TARGET"),
	31: ("A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", "-----", "TROUGH ELECT"),
	32: ("A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", "-----", "TROUGH BALL 1"),
	33: ("A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", "-----", "TROUGH BALL 2"),
	34: ("A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", "-----", "TROUGH BALL 3"),
	35: ("A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", "-----", "TROUGH BALL 4"),
	36: ("A-16908 (LED) / A-16909 (PHOTO TRANS)", "-----", "CENTER RAMP OPTO"),
	37: ("A-16908 (LED) / A-16909 (PHOTO TRANS)", "-----", "RIGHT LOOP ENTER OPTO"),
	38: ("A-17813", "5647-12693-19", "RIGHT LOOP EXIT"), 41: ("A-17799-3", "-----", "STANDUP TARGET '3'"),
	42: ("A-18530-3", "-----", "STANDUP TARGET 'P'"), 43: ("A-18530-3", "-----", "STANDUP TARGET 'T'"),
	44: ("-----", "20-10293", "RIGHT RAMP ENTER"), 45: ("-----", "20-10448", "LEFT RAMP ENTER"),
	46: ("A-21729", "5647-12693-21", "LEFT RAMP MADE"), 47: ("-----", "20-10293", "LEFT LOOP ENTER"),
	48: ("A-17813", "5647-12693-19", "LEFT LOOP MADE"),
	51: ("A-21402", "-----", "DEFENDER POSITION 4"), 52: ("A-21402", "-----", "DEFENDER POSITION 3"),
	53: ("A-21402", "-----", "DEFENDER LOCK POSITION"), 54: ("A-21402", "-----", "DEFENDER POSITION 2"),
	55: ("A-21402", "-----", "DEFENDER POSITION 1"), 56: ("A-19289", "5647-12693-33", "JET BALL DRAIN"),
	57: ("A-17800 (KICK) / A-17794 (**SCORE)", "SW-1A-114 / SW-1A-120", "LEFT SLINGSHOT"),
	58: ("A-17800 (KICK) / A-17794 (**SCORE)", "SW-1A-114 / SW-1A-120", "RIGHT SLINGSHOT"),
	61: ("A-16443-1", "SW-11A-37-1", "LEFT JET BUMPER"), 62: ("A-16443-1", "SW-11A-37-1", "MIDDLE JET BUMPER"),
	63: ("-----", "20-10293", "LEFT LOOP RAMP EXIT"), 64: ("-----", "20-10293", "RIGHT RAMP MADE"),
	65: ("-----", "5467-12693-66", "IN THE PAINT 4"), 66: ("-----", "5467-12693-66", "IN THE PAINT 3"),
	67: ("-----", "5467-12693-66", "IN THE PAINT 2"), 68: ("-----", "5467-12693-66", "IN THE PAINT 1"),
}
SWITCH_LABELS = {
	11: "Ball Launch (Shoot) Button", 12: "Backbox Basket", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Shooter Lane",
	16: "Left Return Lane", 17: "Right Return Lane", 18: "Lower Right Standup Target", 21: "Slam Tilt", 22: "Coin Door Closed",
	23: "Right Jet Bumper", 24: "Always Closed", 25: "Eject Hole (Crazy Bob's)", 26: "Left Outlane", 27: "Right Outlane",
	28: "Upper Right Standup Target", 31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Center Ramp Opto", 37: "Right Loop Enter Opto", 38: "Right Loop Exit", 41: "Standup Target '3'",
	42: "Standup Target 'P'", 43: "Standup Target 'T'", 44: "Right Ramp Enter", 45: "Left Ramp Enter", 46: "Left Ramp Made",
	47: "Left Loop Enter", 48: "Left Loop Made", 51: "Defender Position 4", 52: "Defender Position 3",
	53: "Defender Lock Position", 54: "Defender Position 2", 55: "Defender Position 1", 56: "Jets Ball Drain",
	57: "Left Slingshot", 58: "Right Slingshot", 61: "Left Jet Bumper", 62: "Middle Jet Bumper", 63: "Left Loop Ramp Exit",
	64: "Right Ramp Made", 65: "In The Paint 4", 66: "In The Paint 3", 67: "In The Paint 2", 68: "In The Paint 1",
}
SWITCH_TYPES = {
	11: "button", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "other", 21: "tilt", 22: "microswitch", 23: "leaf", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	28: "other", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 38: "microswitch",
	41: "other", 42: "other", 43: "other", 44: "unknown", 45: "unknown", 46: "microswitch", 47: "unknown", 48: "microswitch",
	51: "opto", 52: "opto", 53: "opto", 54: "opto", 55: "opto", 56: "microswitch", 57: "leaf", 58: "leaf", 61: "leaf", 62: "leaf",
	63: "unknown", 64: "unknown", 65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "microswitch",
}
SWITCH_ROLES = {
	11: "cabinet.launch", 12: "cabinet.backbox", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door",
}
UNUSED_MATRIX_ADDRESSES = frozenset(range(71, 79)) | frozenset(range(81, 89))
# PinMAME's nbafGameData invSw {0x00,0x00,0x00,0x7f,0x00,...,0x10} inverts these public addresses through wpc_sw2m
# (core_setSw indexes invSw by wpc_sw2m(no)/8); the test recomputes the set from the mask.
MASKED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 115})
# Cells the matrix page shades "OPTO, TYPICALLY CLOSED" (measured in switch-matrix.md; identical in both editions).
SHADED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 51, 52, 53, 54, 55, 112, 114, 115, 116, 118})
OPTO_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 51, 52, 53, 54, 55, 115})
# The ROM's own T.1 names (switch-edges sweep), read while the host held the public address at 1.
ROM_SWITCH_NAMES = {
	11: "BALL LAUNCH", 12: "BACKBOX BASKET", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "SHOOTER LANE", 16: "LT. RETURN LANE",
	17: "RT. RETURN LANE", 18: "L. R. STANDUP", 21: "SLAM TILT", 22: "COIN DOOR CLOSED", 23: "RIGHT JET", 24: "ALWAYS CLOSED",
	25: "EJECT HOLE", 26: "LEFT OUT LANE", 27: "RIGHT OUTLANE", 28: "U. R. STANDUP", 31: "TROUGH EJECT", 32: "TROUGH BALL 1",
	33: "TROUGH BALL 2", 34: "TROUGH BALL 3", 35: "TROUGH BALL 4", 36: "CENTER RAMP OPTO", 37: "R. LOOP ENT. OPTO",
	38: "RIGHT LOOP EXIT", 41: "STANDUP '3'", 42: "STANDUP 'P'", 43: "STANDUP 'T'", 44: "RIGHT RAMP ENTER", 45: "LEFT RAMP ENTER",
	46: "LEFT RAMP MADE", 47: "LEFT LOOP ENTER", 48: "LEFT LOOP MADE", 51: "DEFENDER POS. 4", 52: "DEFENDER POS. 3",
	53: "DEFEND. LOCK POS", 54: "DEFENDER POS. 2", 55: "DEFENDER POS. 1", 56: "JETS BALL DRAIN", 57: "L. SLINGSHOT",
	58: "R. SLINGSHOT", 61: "LEFT JET", 62: "MIDDLE JET", 63: "L. LOOP RAMP EXIT", 64: "RIGHT RAMP MADE", 65: '"IN THE PAINT" 4',
	66: '"IN THE PAINT" 3', 67: '"IN THE PAINT" 2', 68: '"IN THE PAINT" 1', 115: "BASKET MADE", 117: "BASKET HOLD",
}
# Switches whose closure makes the ROM fire their own coil even inside T.1 (switch-edges sweep).
SWITCH_FIRES = {23: 14, 57: 10, 58: 11, 61: 12, 62: 13}
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"), 3: ("Green-Orange", "J206-3", "U20-16"),
	4: ("Green-Yellow", "J206-4", "U20-15"), 5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
# Row 6 prints its connector as "U208-7" in both editions; the opto board pages and the CPU connector list print J208-7.
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"), 3: ("White-Orange", "J208-3", "U18-5"),
	4: ("White-Yellow", "J208-4", "U18-7"), 5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
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
# Fliptronic column (switch-matrix.md; section-3-boards.md, printed 3-11 and 3-13):
# public -> (label, printed position, wire, connector, comparator pin, type, role or None).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J208-13", "U26A-1", "leaf", "internal.flipper.lower.right.eos"),
	112: ("Right Flipper Button Lower Opto", "F2", "Blue-Violet", "J212-12", "U25A-1", "opto", "flipper.lower.right.button"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J208-12", "U26B-2", "leaf", "internal.flipper.lower.left.eos"),
	114: ("Left Flipper Button Lower Opto", "F4", "Blue-Gray", "J212-11", "U25B-2", "opto", "flipper.lower.left.button"),
	115: ("Basket Made Opto", "F5", "Black-Violet", "J208-11", "U26C-14", "opto", None),
	116: ("Right Flipper Button Upper Opto", "F6", "Black-Yellow", "J212-10", "U25C-14", "opto", "flipper.lower.right.button"),
	117: ("Basket Hold", "F7", "Black-Gray", "J208-10", "U26D-13", "microswitch", None),
	118: ("Left Flipper Button Upper Opto", "F8", "Black-Blue", "J212-9", "U25D-13", "opto", "flipper.lower.left.button"),
}
# T.1's printed position and wires for the Fliptronic column (switch-edges sweep).
FLIPPER_ROM_TEXT = {111: "F1 BLK-GRN", 112: "F1 BLK-GRN", 113: "F3 BLK-BLU", 114: "F3 BLK-BLU", 115: "F5 BLK-VIO", 116: "F1 BLK-GRN", 117: "F7 BLK-GRY", 118: "F3 BLK-BLU"}

# --- Solenoid data (solenoid-flasher-table.md, solenoid-flashlamp-locations.md, section-3-boards.md) -----
SOLENOID_LABELS = {
	1: "Auto Plunger", 3: "Left Ramp Diverter", 4: "Right Loop Diverter", 5: "Eject (Crazy Bob's)", 6: "Loop Gate",
	7: "Backbox Flipper", 8: "Ball Catch Magnet", 9: "Trough Eject", 10: "Left Slingshot", 11: "Right Slingshot",
	12: "Left Jet Bumper", 13: "Middle Jet Bumper", 14: "Right Jet Bumper", 15: "Pass Right 2", 16: "Pass Left 2",
	17: "Eject Kickout Flasher", 18: "Left Jet Bumper Flasher", 19: "Upper Left Flasher", 20: "Upper Right Flasher",
	22: "Trophy Insert Flasher", 24: "Lower Right/Left Flashers", 25: "Pass Right 1", 26: "Pass Left 3", 27: "Pass Right 3",
	28: "Pass Left 4", 33: "Shoot 1", 34: "Shoot 2", 35: "Shoot 3", 36: "Shoot 4", 37: "Defender Motor Enable",
	38: "Defender Motor Direction", 39: "Shot Clock Enable", 40: "Shot Clock Count",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_USED_SOLENOID_LABELS = {2: "Not Used Solenoid Position 2", 21: "Not Used Flasher Position 21", 23: "Not Used Flasher Position 23"}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B", 31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32", 41: "Defender Motor Enable LPDC Mirror", 42: "Defender Motor Direction LPDC Mirror",
	43: "Shot Clock Enable LPDC Mirror", 44: "Shot Clock Count LPDC Mirror", 49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# address -> printed (type, voltage connector(s), transistor or gates, drive connector(s), wire, part or flashlamp), Solenoid/Flasher Table (2-50).
SOLENOID_TABLE = {
	1: ("High Power", "J133-2", "Q72", "J116-1", "VIO-BRN", "AE-24-900"), 2: ("High Power", None, "Q68", None, "VIO-RED", None),
	3: ("High Power", "J133-2", "Q71", "J116-4", "VIO-ORG", "AE-26-1500"), 4: ("High Power", "J133-2", "Q67", "J116-5", "VIO-YEL", "AE-26-1500"),
	5: ("High Power", "J133-2", "Q70", "J116-6", "VIO-GRN", "AE-30-2000"), 6: ("High Power", "J133-2", "Q66", "J116-7", "VIO-BLU", "A-14406"),
	7: ("High Power", "J133-2 (backbox)", "Q69", "J117-3 (backbox)", "VIO-BLK", "FL-11753"),
	8: ("High Power", "J133-2", "Q65", "J116-9", "VIO-GRY", "B-13522"),
	9: ("Low Power", "J133-3", "Q44", "J113-1", "BRN-BLK", "AE-28-1500"), 10: ("Low Power", "J133-3", "Q48", "J113-3", "BRN-RED", "AE-26-1200"),
	11: ("Low Power", "J133-3", "Q43", "J113-4", "BRN-ORG", "AE-26-1200"), 12: ("Low Power", "J133-3", "Q47", "J113-5", "BRN-YEL", "AE-26-1200"),
	13: ("Low Power", "J133-3", "Q42", "J113-6", "BRN-GRN", "AE-26-1200"), 14: ("Low Power", "J133-3", "Q46", "J113-7", "BRN-BLU", "AE-26-1200"),
	15: ("Low Power", "J133-3", "Q41", "J113-8", "BRN-VIO", "AE-29-2000"), 16: ("Low Power", "J133-3", "Q45", "J113-9", "BRN-GRY", "AE-29-2000"),
	17: ("Flasher", "J133-6", "Q28", "J111-1", "BLK-BRN", "#906 (1)"), 18: ("Flasher", "J133-6", "Q32", "J111-2", "BLK-RED", "#906 (1)"),
	19: ("Flasher", "J133-6, J134-5 (backbox)", "Q27", "J111-3, J112-3 (backbox)", "BLK-ORG", "#906 (1) playfield, #906 (1) backbox"),
	20: ("Flasher", "J133-6, J134-5 (backbox)", "Q31", "J111-4, J112-5 (backbox)", "BLK-YEL", "#906 (1) playfield, #906 (1) backbox"),
	21: ("Flasher", None, "Q26", None, "BLU-GRN", None), 22: ("Flasher", "J133-6", "Q30", "J111-6", "BLU-BLK", "#906 (1)"),
	23: ("Flasher", None, "Q25", None, "BLU-VIO", None), 24: ("Flasher", "J133-6", "Q29", "J111-8", "BLU-GRY", "#906 (2)"),
	25: ("Gen. Purpose", "J133-1", "Q16", "J109-1", "BLU-BRN", "AE-29-2000"), 26: ("Gen. Purpose", "J133-1", "Q15", "J109-2", "BLU-RED", "AE-29-2000"),
	27: ("Gen. Purpose", "J133-1", "Q14", "J109-3", "BLU-ORG", "AE-29-2000"), 28: ("Gen. Purpose", "J133-1", "Q13", "J109-4", "BLU-YEL", "AE-29-2000"),
	33: ("Upr. Rt. Power", "J119-6 (RED-VIO)", "Q84", "J120-6", "YEL-VIO", "AE-23-800"), 34: ("Upr. Rt. Hold", "J119-6 (RED-VIO)", "Q86", "J120-4", "ORG-VIO", "AE-23-800"),
	35: ("Upr. Lt. Power", "J119-8 (RED-GRY)", "Q81", "J120-3", "YEL-GRY", "AE-23-800"), 36: ("Upr. Lt. Hold", "J119-8 (RED-GRY)", "Q83", "J120-1", "ORG-GRY", "AE-23-800"),
	37: ("Low Power", "J139-2", "U3A, U3B", "J110-1", "BRN-WHT", "14-8034"), 38: ("Low Power", "J139-2", "U3C, U3D", "J110-3", "ORG-WHT", "14-8034"),
	39: ("Low Power", "J139-2", "U3G, U3H", "J110-4", "YEL-WHT", "A-21380"), 40: ("Low Power", "J139-2", "U3E, U3F", "J110-5", "BLU-WHT", "A-21380"),
}
# Locations-list assembly for each coil/flasher (solenoid-flashlamp-locations.md, 2-40).
SOLENOID_ASSEMBLIES = {
	1: "A-21553", 3: "A-21531", 4: "A-21530", 5: "A-21405-1", 6: "A-17796", 7: "A-21717", 8: "A-21520", 9: "A-19963-1",
	10: "B-9362-R-3", 11: "B-9362-R-3", 12: "A-9415-3", 13: "A-9415-2", 14: "A-9415-2", 15: "A-21411-2", 16: "A-21411-2",
	22: "C-13375", 25: "A-21411-1", 26: "A-21411-3", 27: "A-21411-3", 28: "A-21411-4", 33: "A-21411-1", 34: "A-21411-2",
	35: "A-21411-3", 36: "A-21411-4", 37: "A-21413", 38: "A-21413", 39: "A-21393", 40: "A-21393", 45: "A-14876-R", 46: "A-14876-R",
	47: "A-15849-L", 48: "A-15849-L",
}
FLASHER_SOLENOIDS = frozenset({17, 18, 19, 20, 22, 24})
FLASHER_COUNTS = {19: 2, 20: 2, 24: 2}
# The ROM's own T.4 and T.5 names and wires (solenoid-test, flasher-test-sweep and blinked-names runs).
ROM_SOLENOID_NAMES = {
	1: ("AUTOPLUNGER", "VIO-BRN RED-BRN"), 3: ("L. RAMP DIVERTER", "VIO-ORN RED-BRN"), 4: ("R. LOOP DIVERTER", "VIO-YEL RED-BRN"),
	5: ("EJECT", "VIO-GRN RED-BRN"), 6: ("LOOP GATE", "VIO-BLU RED-BRN"), 7: ("BACKBOX FLIPPER", "VIO-BLK RED-BRN"),
	8: ("BALL CATCH MAG.", "VIO-GRY RED-BRN"), 9: ("TROUGH EJECT", "BRN-BLK RED-BLK"), 10: ("LEFT SLING", "BRN-RED RED-BLK"),
	11: ("RIGHT SLING", "BRN-ORN RED-BLK"), 12: ("LEFT JET", "BRN-YEL RED-BLK"), 13: ("MIDDLE JET", "BRN-GRN RED-BLK"),
	14: ("RIGHT JET", "BRN-BLU RED-BLK"), 15: ("PASS RIGHT 2", "BRN-VIO RED-BLK"), 16: ("PASS LEFT 2", "BRN-GRY RED-BLK"),
	17: ("EJECT KICKOUT", "BLK-BRN RED-WHT"), 18: ("LEFT JET BUMPER", "BLK-RED RED-WHT"), 19: ("UPPER LEFT", "BLK-ORN RED-WHT"),
	20: ("UPPER RIGHT", "BLK-YEL RED-WHT"), 22: ("TROPHY INSERT", "BLU-BLK RED-WHT"), 24: ("LOWER LEFT/RIGHT", "BLU-GRY RED-WHT"),
	25: ("PASS RIGHT 1", "BLU-BRN RED-ORN"), 26: ("PASS LEFT 3", "BLU-RED RED-ORN"), 27: ("PASS RIGHT 3", "BLU-ORN RED-ORN"),
	28: ("PASS LEFT 4", "BLU-YEL RED-ORN"), 33: ("SHOOT 1", "YEL-VIO RED-VIO"), 34: ("SHOOT 2", "ORN-VIO RED-VIO"),
	35: ("SHOOT 3", "YEL-GRY RED-GRY"), 36: ("SHOOT 4", "ORN-GRY RED-GRY"), 37: ("MOTOR ENABLE", "BRN-WHT GRY-YEL"),
	38: ("MOTOR DIRECTION", "ORN-WHT GRY-YEL"), 39: ("SHOT CLK ENABLE", "YEL-WHT GRY-YEL"), 40: ("SHOT CLK COUNT", "GRN-WHT GRY-YEL"),
	45: ("R. FLIP. POWER", "YEL-GRN RED-GRN"), 46: ("R. FLIP. HOLD", "ORN-GRN RED-GRN"), 47: ("L. FLIP. POWER", "YEL-BLU RED-BLU"),
	48: ("L. FLIP. HOLD", "ORN-BLU RED-BLU"),
}
T5_ADDRESSES = frozenset({17, 18, 19, 20, 22, 24})
T12_ADDRESSES = frozenset({45, 46, 47, 48})
# The retained table's own handling of each solenoid (vpx-analysis script facts).
SOLENOID_SCRIPT = {
	1: "SolCallBack(1) = \"Auto_Plunger\" fires the cvpmImpulseP plunger at swPlunger",
	3: "SolCallBack(3) = \"SolDiverter2\" drops the Diverter2 wall and animates DiverterP2",
	4: "SolCallBack(4) = \"vpmSolWall Diverter1,True,\"",
	5: "SolCallBack(5) = \"bsEject.SolOut\" kicks the ball out of the sw25 saucer",
	6: "SolCallBack(6) = \"RightGate.Open =\"",
	7: "SolCallBack(7) = \"SolBasket\" kicks the backbox ball (BackBall) and rotates BasketFlipper in the table's backbox model",
	8: "a cvpmMagnet (MagnetCatch, BCMagnet trigger) follows Controller.Solenoid(8); no SolCallBack",
	9: "SolCallBack(9) = \"bsTrough.SolOut\" releases a ball from the trough's BallRelease kicker",
	15: "SolCallBack(15) = \"PassRight2\" alt-kicks the ball held in the In The Paint 2 saucer (sw67) to the right",
	16: "SolCallBack(16) = \"PassLeft2\" alt-kicks the ball held in the In The Paint 2 saucer (sw67) to the left",
	17: "SolCallBack(17) = \"FlashSol17\" lights Flupper dome 3", 18: "SolCallBack(18) = \"FlashSol18\" lights Flupper dome 10, on the left jet bumper",
	19: "SolCallBack(19) = \"FlashSol19\" lights Flupper dome 4 (commented 'upper left / BG Left')",
	20: "SolCallBack(20) = \"FlashSol20\" lights Flupper dome 5 (commented 'upper right / BG Right')",
	22: "SolCallBack(22) = \"SetLamp 122,\" writes a lamp state nothing reads (commented 'trophy insert TODO')",
	24: "SolCallBack(24) = \"FlashSol24\" lights Flupper domes 1 and 2 on opposite sides of the lower playfield",
	25: "SolCallBack(25) = \"PassRight1\" alt-kicks the ball held in the In The Paint 1 saucer (sw68) to the right",
	26: "SolCallBack(26) = \"PassLeft3\" alt-kicks the ball held in the In The Paint 3 saucer (sw66) to the left",
	27: "SolCallBack(27) = \"PassRight3\" alt-kicks the ball held in the In The Paint 3 saucer (sw66) to the right",
	28: "SolCallBack(28) = \"PassLeft4\" alt-kicks the ball held in the In The Paint 4 saucer (sw65) to the left",
	33: "SolCallBack(33) = \"bsSaucer1.SolOut\" shoots the ball from the In The Paint 1 saucer (sw68) toward the basket",
	34: "SolCallBack(34) = \"bsSaucer2.SolOut\" shoots from In The Paint 2 (sw67)",
	35: "SolCallBack(35) = \"bsSaucer3.SolOut\" shoots from In The Paint 3 (sw66)",
	36: "SolCallBack(36) = \"bsSaucer4.SolOut\" shoots from In The Paint 4 (sw65)",
	37: "the cvpmMech mDefender takes .Sol1 = 37 (Enable)", 38: "the cvpmMech mDefender takes .Sol2 = 38 (Direction)",
	39: "SolCallBack(39) = \"ClockEnable\" is commented out; the table draws the shot clock from Controller.ChangedLEDs instead",
	40: "SolCallBack(40) = \"ClockCount\" is commented out; the table draws the shot clock from Controller.ChangedLEDs instead",
	46: "SolCallback(sLRFlipper) = \"SolRFlipper\" (sLRFlipper = 46)", 48: "SolCallback(sLLFlipper) = \"SolLFlipper\" (sLLFlipper = 48)",
}
SOLENOID_SCRIPT.update({address: "the vpmSolSound callback is commented out; the table fires the coil from the switch's physics event, so the address has no binding" for address in (10, 11, 12, 13, 14)})
# Fliptronic flipper windings (solenoid-flasher-table.md flipper block; manual numbers them 29-32).
FLIPPER_COILS = {
	45: ("power", "29", "Lwr. Rt. Power", "J119-1 (RED-GRN)", "Q90", "J120-13", "YEL-GRN"),
	46: ("hold", "30", "Lwr. Rt. Hold", "J119-1 (RED-GRN)", "Q92", "J120-11", "ORG-GRN"),
	47: ("power", "31", "Lwr. Lt. Power", "J119-4 (RED-BLU)", "Q87", "J120-9", "YEL-BLU"),
	48: ("hold", "32", "Lwr. Lt. Hold", "J119-4 (RED-BLU)", "Q89", "J120-7", "ORG-BLU"),
}

# --- Lamp data (lamp-locations.md, lamp-matrix.md) -------------------------------------------------------
# address -> (lamp assembly, bulb part number, socket, printed description), Lamp Locations list (2-44).
LAMP_LOCATIONS = {
	11: ("A-21547", "24-8768", "24-8767", "20 POINTS"), 12: ("A-21547", "24-8768", "24-8767", "FREE THROW"),
	13: ("A-21547", "24-8768", "24-8767", "3 POINTS"), 14: ("A-21547", "24-8768", "24-8767", "2 POINTS"),
	15: ("A-21547", "24-8768", "24-8767", "FIELD GOALS"), 16: ("A-21547", "24-8768", "24-8767", "MULTIBALLS"),
	17: ("A-21547", "24-8768", "24-8767", "SHOOT AROUND"), 18: ("A-21547", "24-8768", "24-8767", "AROUND THE WORLD"),
	21: ("A-21547", "24-8768", "24-8767", "POWER HOOPS"), 22: ("A-21547", "24-8768", "24-8767", "FASTBREAK COMBO"),
	23: ("A-21547", "24-8768", "24-8767", "ALLEY OOP COMBO"), 24: ("A-21547", "24-8768", "24-8767", "SLAM DUNK COMBO"),
	25: ("A-21547", "24-8768", "24-8767", "COMBOS"), 26: ("A-21547", "24-8768", "24-8767", "TROPHY"),
	27: ("A-21547", "24-8768", "24-8767", "TIP-OFF COMBO"), 28: ("A-21547", "24-8768", "24-8767", "STADIUM GOODIES"),
	31: ("A-21548", "24-8768", "24-8767", "MULTIBALL HOOPS"), 32: ("A-21548", "24-8768", "24-8767", "RUN & SHOOT HOOPS"),
	33: ("A-21548", "24-8768", "24-8767", "HOOK SHOT HOOPS"), 34: ("A-21548", "24-8768", "24-8767", "HALF COURT HOOPS"),
	35: ("A-21548", "24-8768", "24-8767", "LIGHT TIP-OFF"), 36: ("A-21548", "24-8768", "24-8767", 'RIGHT "IN THE PAINT"'),
	37: ("A-21548", "24-8768", "24-8767", "SHOO(T)"), 38: ("A-17835*", "24-6549", "-----", "LEFT RETURN LANE"),
	41: ("A-21548", "24-8768", "24-8767", "CHAMPION RING 1"), 42: ("A-21548", "24-8768", "24-8767", "CHAMPION RING 2"),
	43: ("A-21548", "24-8768", "24-8767", "RIGHT RETURN LANE"), 44: ("A-21548", "24-8768", "24-8767", "CHAMPION RING 4"),
	45: ("A-21548", "24-8768", "24-8767", "CHAMPION RING 3"), 46: ("A-21548", "24-8768", "24-8767", "LOWER RIGHT STANDUP"),
	47: ("A-21548", "24-8768", "24-8767", "UPPER RIGHT STANDUP"), 48: ("A-17835*", "24-6549", "-----", "LEFT OUTLANE"),
	51: ("A-21549", "24-8768", "24-8767", "SODA"), 52: ("A-21549", "24-8768", "24-8767", "QUESTION"),
	53: ("A-21549", "24-8768", "24-8767", "HOT DOG"), 54: ("A-21549", "24-8768", "24-8767", "PIZZA"),
	55: ("A-21549", "24-8768", "24-8767", "CRAZY BOB'S"), 56: ("A-21549", "24-8768", "24-8767", "EXTRA BALL"),
	57: ("A-17807", "24-6549", "A-17806", "RIGHT OUTLANE"), 58: ("A-17807", "24-6549", "A-17806", "SHOOT AGAIN"),
	61: ("A-21551 / A-21549", "24-8768", "24-8767", "RAMPS: 3 POINTS"), 62: ("A-21549", "24-8768", "24-8767", "TIP-OFF"),
	63: ("A-21549", "24-8768", "24-8767", "FASTBREAK"), 64: ("A-21549", "24-8768", "24-8767", "ALLEY OOP"),
	65: ("A-21549", "24-8768", "24-8767", "FREE THROW"), 66: ("A-21549", "24-8768", "24-8767", "SH(O)OT"),
	67: ("A-21582*", "24-8768", "-----", "IN THE PAINT 4"), 68: ("A-21581*", "24-8768", "-----", "IN THE PAINT 3"),
	71: ("A-21551", "24-8768", "24-8767", "LEFT LIGHT FASTBREAK"), 72: ("A-21551", "24-8768", "24-8767", "SLAM DUNK"),
	73: ("A-21551", "24-8768", "24-8767", "S(H)OOT"), 74: ("A-21322", "24-8768", "24-8767", "RIGHT LIGHT FASTBREAK"),
	75: ("A-21322", "24-8768", "24-8767", "LIGHT SLAM DUNK"), 76: ("A-21322", "24-8768", "24-8767", "SHO(O)T"),
	77: ("A-21579*", "24-8768", "-----", "IN THE PAINT 1"), 78: ("A-21580*", "24-8768", "-----", "IN THE PAINT 2"),
	81: ("A-21322", "24-8768", "24-8767", "LIGHT ALLEY OOP"), 82: ("A-21322", "24-8768", "24-8767", 'LEFT "IN THE PAINT"'),
	83: ("A-21322", "24-8768", "24-8767", "(S)HOOT"), 84: ("A-17835*", "24-6768", "-----", "(3) PT."),
	85: ("A-17835*", "24-8768", "-----", "3 (P)T."), 86: ("A-17835*", "24-8768", "-----", "3 P(T)"),
	87: ("20-10327-4", None, None, "BALL LAUNCH"), 88: ("20-9663-16", None, None, "START BUTTON"),
}
LAMP_LABELS = {
	36: 'Right "In The Paint"', 82: 'Left "In The Paint"', 84: "(3) PT.", 85: "3 (P)T.", 86: "3 P(T)", 61: "Ramps: 3 Points",
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"), 3: ("Yellow-Orange", "J121-3", "Q95"),
	4: ("Yellow-Black", "J121-4", "Q99"), 5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"), 3: ("Red-Orange", "J125-4", "Q103"),
	4: ("Red-Yellow", "J125-5", "Q107"), 5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}
CABINET_LAMPS = {87: "cabinet.launch", 88: "cabinet.start"}
IN_THE_PAINT_LAMPS = {77: 1, 78: 2, 68: 3, 67: 4}

# --- General illumination (solenoid-flasher-table.md G.I. block; gi-test run) -----------------------------
# public -> (string, voltage connectors, triac, drive connectors, wire, playfield bulb, backbox bulb, ROM T.6 wires)
GI_STRINGS = {
	0: (1, "J106-1, J105-1", "Q5", "J106-7, J105-7", "WHT-BRN", "#44", "#555", "WHT-BRN BRN"),
	1: (2, "J106-2, J105-2", "Q4", "J106-8, J105-8", "WHT-ORG", "#44", "#555", "WHT-ORN ORN"),
	2: (3, "J106-3, J105-3", "Q3", "J106-9, J105-9", "WHT-YEL", "#44", "#555", "WHT-YEL YEL"),
	3: (4, "J106-5", "Q2", "J106-10", "WHT-GRN", "#44", None, "WHT-GRN GRN"),
	4: (5, "J106-6, J105-6, J104-3 (cabinet)", "Q1", "J106-11, J105-11, J104-1 (cabinet)", "WHT-VIO", "#44", "#555", "WHT-VIO VIO"),
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
		raise RuntimeError(f"NBA Fastbreak retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained NBA Fastbreak extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"NBA Fastbreak retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"NBA Fastbreak retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"NBA Fastbreak retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
		"board": "WPC-95 CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


# What the retained known-working script does for each matrix switch (vpx-analysis script facts).
SWITCH_SCRIPT = {
	11: "the plunger key writes Controller.Switch(11) (the table has no manual plunger)",
	12: "trigger sw12 in the table's hidden backbox-basketball model sets and clears it",
	14: "vpmNudge.TiltSwitch = 14", 15: "the cvpmImpulseP auto-plunger's swPlunger trigger reports it",
	16: "trigger sw16 follows the ball", 17: "trigger sw17 follows the ball", 18: "the sw18 target wall pulses it (vpmTimer.PulseSw)",
	22: "table1_Init sets Controller.Switch(22) = 1 (coin door closed)", 23: "Bumper2_Hit pulses it",
	24: "table1_Init sets Controller.Switch(24) = 1", 25: "the sw25 saucer (bsEject) holds the ball on it",
	26: "trigger sw26 follows the ball", 27: "trigger sw27 follows the ball", 28: "the sw28 target wall pulses it",
	36: "trigger sw36 follows the ball", 37: "trigger sw37 follows the ball", 38: "trigger sw38 follows the ball",
	41: "the sw41 target pulses it", 42: "the sw42 target pulses it", 43: "the sw43 target pulses it",
	44: "trigger sw44 follows the ball", 45: "trigger sw45 follows the ball", 46: "trigger sw46 follows the ball",
	47: "trigger sw47 follows the ball", 48: "trigger sw48 follows the ball", 56: "trigger sw56 follows the ball",
	57: "LeftSlingShot_Slingshot pulses it", 58: "RightSlingShot_Slingshot pulses it", 61: "Bumper1_Hit pulses it",
	62: "Bumper3_Hit pulses it", 63: "trigger sw63 follows the ball", 64: "trigger sw64 follows the ball",
	65: "the sw65 saucer (bsSaucer4) holds the ball on it", 66: "the sw66 saucer (bsSaucer3) holds the ball on it",
	67: "the sw67 saucer (bsSaucer2) holds the ball on it", 68: "the sw68 saucer (bsSaucer1) holds the ball on it",
}
for _address, _slot in ((31, 5), (32, 1), (33, 2), (34, 3), (35, 4)):
	SWITCH_SCRIPT[_address] = f"the cvpmBallStack bsTrough derives it from its slot {_slot} ball count (no table object)"
for _address, _window in ((51, "0-1"), (52, "17-18"), (53, "31-32"), (54, "44-45"), (55, "64-65")):
	SWITCH_SCRIPT[_address] = f"the cvpmMech mDefender sets it in its position window {_window} of 65 steps (no table object)"


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if row == 6:
		extra["wiring"]["return_connection"] = "J208-7"
		notes += " The matrix page prints row 6's connector as 'U208-7' in both editions; the opto-board pages route Switch Row 6 to CPU board J208-7, which the wiring record follows."
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += (
			" The Switch Matrix prints NOT USED in every cell of columns 7 and 8 and the Switch Locations list ends '71 to 88 NOT USED'. "
			"In the ROM's T.1 SWITCH EDGES sweep a host write of 1 or 0 at this address drew no name: the test kept showing the last "
			"named switch, 68."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, EDGES_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra,
		)
	assembly, part, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if part != "-----":
		physical["part_number"] = part
	if assembly != "-----":
		physical["assembly_part_number"] = assembly
	notes += f' Switch Locations description "{description}".'
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address == 24:
		notes += (
			" PinMAME holds public 24 at 1 from power-up. In T.1 SWITCH EDGES the redundant write of 1 drew nothing new and the 1 -> 0 "
			"edge drew 'ALWAYS CLOSED / T.1 LAST SW 24', so the ROM reports this position when it opens: an open Always Closed "
			"switch is the fault the test exists to show."
		)
	else:
		notes += f" The ROM names it \"{ROM_SWITCH_NAMES[address]}\" in T.1 SWITCH EDGES while the host holds public {address} at 1, and clears the name at 0."
	if column == 4:
		notes += " The ROM's T.1 text prints this column's wire as GRN-WHT where the manual's matrix prints Green-Yellow (J206-4); the wiring record follows the manual."
	if address in SWITCH_FIRES:
		notes += f" Closing it made the ROM fire its own coil, public solenoid {SWITCH_FIRES[address]}, even inside T.1."
	if address in MASKED_SWITCHES:
		notes += (
			" PinMAME's nbafGameData inverted-switch mask inverts this address, so public 1 is an open matrix contact; the ROM reads "
			"the switch as active at public 1 (it names it there), so its matrix contact rests closed and normally_closed is true. "
			"The matrix page shades the cell 'OPTO, TYPICALLY CLOSED', and the trough and ramp opto wiring page says that when the beam "
			"is broken the switch is made."
		)
	elif address in OPTO_SWITCHES:
		notes += (
			" The matrix page shades the cell 'OPTO, TYPICALLY CLOSED' and the Defender Switch Board A-21402 carries its opto, but "
			"PinMAME's mask does not invert it and the ROM names it at public 1, an unmasked closed contact, so the matrix contact "
			"rests open and normally_closed is false: the board's comparator closes the matrix line when the defender's flag "
			"reaches the opto. The printed legend marks opto construction, not the rest state the ROM reads."
		)
	if address in {31, 32, 33, 34, 35}:
		board = {31: ("LED 1 (Jam Ball)", "GRY-BRN", "ORG-BRN"), 32: ("LED 2 (Ball 1)", "GRY-RED", "ORG-RED"), 33: ("LED 3 (Ball 2)", "GRY-ORG", "ORG-BLK"),
			34: ("LED 4 (Ball 3)", "GRY-BLK", "ORG-YEL"), 35: ("LED 5 (Ball 4)", "GRY-GRN", "ORG-GRN")}[address]
		notes += (
			f" Ball trough opto pair on the Trough IR LED Board A-18617-1 ({board[0]}, {board[1]}) and the Trough IR Photo Transistor "
			f"Board A-18618-1 ({board[2]}), read through the 7-Opto Switch Board A-15576.1."
		)
		if address == 31:
			notes += " The Switch Locations list prints its description 'TROUGH ELECT'; the matrix, the wiring pages and the ROM print TROUGH EJECT, the position over the trough's eject coil."
		else:
			notes += f" It reports the trough holding at least {address - 31} ball{'s' if address > 32 else ''} (four balls are installed)."
	if address in {36, 37}:
		notes += " LED Board A-16908 (transmitter) and Photo Transistor Board A-16909 (receiver), read through the 7-Opto Switch Board A-15576.1; the manual's receiver reads 0.1-0.7 V unblocked and 11-13 V blocked."
	if address in {51, 52, 53, 54, 55}:
		notes += (
			" One of the five optos of the Defender Switch Board A-21402 (rows 1-5 of column 5) that report the defender arm's position. "
			"The ROM's T.16 MOTOR TEST shows them as POS 1, POS 2, LOCK, POS 3 and POS 4 from left to right."
		)
	if address in {65, 66, 67, 68}:
		notes += f" The ball rests on this saucer switch at In The Paint shooter position {69 - address}; see the In The Paint mechanism."
	if address in {41, 42, 43}:
		notes += " One of the three 3-PT standup targets in front of the center of the playfield; completing the three lights 3 POINTS on the left and center ramps (game rules)."
	if address in {18, 28}:
		notes += " A right-side standup target; completing the right standups lights the left outlane's INBOUND PASS (game rules)."
	if address in {57, 58}:
		notes += " The slingshot kick switch A-17800 (SW-1A-114) and the score switch A-17794 (SW-1A-120, with a diode attached) share this address."
	if address == 12:
		notes += (
			" A microswitch on the backbox basketball goal (assembly A-21710), not a playfield device: the backbox flipper (solenoid 7) "
			"flips the backbox ball at the basket, and this switch scores the basket. T.17 BACKBOX TEST marks BACKBOX while the host "
			"holds it at 1."
		)
	if address == 11:
		notes += (
			" The SHOOT button on the cabinet's front molding (20-10327-4, lit by lamp 87). It launches the ball through the auto plunger, "
			"locks in the team at game start, fires the backbox flipper during the backbox game and ends the trivia quiz. T.17 BACKBOX TEST "
			"marks SHOOT while it is held and fires solenoid 7 on each press."
		)
	if address == 56:
		notes += " The Switch Locations list prints 'JET BALL DRAIN'; the matrix prints 'JETS BALL DRAIN'. It sees the ball leave the jet bumpers."
	if address in {65, 66, 67, 68}:
		notes += " The Switch Locations list prints the part number 5467-12693-66 here, where the eject hole (25) prints 5647-12693-66."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = {11: "cabinet front molding", 12: "backbox", 13: "cabinet front"}.get(address, "cabinet interior")
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
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		if address <= 4:
			note += (
				f" An earlier T.1 run at the previous PinMAME pin names public {address} "
				f"'{('LEFT COIN SLOT', 'CENTER COIN SLOT', 'RIGHT COIN SLOT', '4TH COIN OPTION')[address - 1]}' and reports it as LAST SW D{address}."
			)
			refs += (EARLIER_EDGES_SOURCE,)
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", refs,
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note} The dedicated switches reach the CPU through the Coin Door Interface Board A-20580."},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, component, switch_type, role) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": f"comparator {component}"},
		}
		if role:
			extra["roles"] = [role]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		physical: dict[str, Any] = {"switch_type": switch_type}
		rom = FLIPPER_ROM_TEXT[address]
		if address in {111, 113}:
			physical["part_number"] = "SW-1A-194"
			physical["location"] = "flipper assembly"
			notes += (
				f" End-of-stroke switch SW-1A-194 on the lower {'right' if address == 111 else 'left'} flipper assembly "
				f"({'A-14876-R' if address == 111 else 'A-15849-L'}). nbafGameData declares FLIP_SOL(FLIP_L), so PinMAME rewrites this "
				"bit from the flipper coil state on every update: in the T.1 sweep a host write of 1 read back 0 and drew no name. Its "
				"public level is not a measurement of the contact; normally_closed records the grounded switch's open rest state."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address in {112, 114, 116, 118}:
			side = "right" if address in {112, 116} else "left"
			board_pin = "J1-2" if address in {112, 114} else "J1-1"
			physical["location"] = "cabinet flipper button"
			physical["assembly_part_number"] = "A-17316"
			notes += (
				f" One of the two optos (OPTO1/OPTO2) of the {side} Flipper Opto Board A-17316 at the {side} cabinet button ({board_pin}); "
				"WPC-95 reads the flipper column complemented (WPC_FLIPPERSW95 returns ~swMatrix), so public 1 is the pressed button and "
				"the contact the matrix sees is open at rest: normally_closed is false. The matrix page shades the cell as an opto."
			)
			if address in {112, 114}:
				notes += f" In the T.1 sweep a host write of 1 made the ROM fire the lower {side} flipper (power and hold) and name '{side[0].upper()}. FLIPPER EOS.' ({rom})."
			else:
				notes += (
					f" The Switch Locations list prints '{printed} NOT USED ... UPPER {side.upper()} FLIPPER CABINET', but this game's own wiring "
					f"pages (3-11 cabinet opto table, 3-13 cabinet switch circuits, 3-14 Flipper Opto Board pin list, which name the "
					f"basket switches F5 and F7 and so are not a reused template) wire {printed} to the second opto of the same {side} "
					f"button's board, and the ROM consumes it: in the T.1 sweep a host write of 1 at public {address} fired the lower {side} "
					f"flipper (power and hold) exactly as {address - 4} did and named '{side[0].upper()}. FLIPPER EOS.'. A game-specific "
					"wiring page rebuts a 'NOT USED' row, so the position is recorded as fitted: the second opto of the "
					f"{side} flipper button, which a press interrupts together with {address - 4}. NBA Fastbreak has no upper flipper, so "
					f"the role is the {side} flipper button's, the same as {address - 4}'s: a consumer drives both from that button. The "
					"retained VPinMAME library writes only 112 and 114, which the ROM accepts on their own."
				)
				refs += (VPX_SCRIPT_SOURCE,)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 115:
			physical["assembly_part_number"] = "A-16908 (LED) / A-16909 (PHOTO TRANS)"
			notes += (
				" The basket-made opto under the playfield basket, read through the 24-Opto Switch Board A-15646 ('FOR BASKET MADE OPTO "
				"SWITCH'); the Flipper Circuit Diagram marks F5 '*BASKET MADE OPTO' with the footnote 'A FLIPPER CIRCUIT USED FOR ANOTHER "
				"PURPOSE'. PinMAME's nbafGameData mask inverts this position (Cust byte 0x10), and WPC-95 also complements the flipper "
				"column on read, so the ROM sees the public level directly: the T.1 sweep named 'BASKET MADE' (F5 BLK-VIO) while the host "
				"held public 115 at 1. Public 1 is therefore a raw open grounded contact, the beam-broken state, and the contact rests "
				"closed: normally_closed is true, as the shaded 'OPTO, TYPICALLY CLOSED' cell says. IPDB notes that later playfields route "
				"this opto's wire through an oval hole below the aerial hoop, where earlier ones ran it behind the scoreboard."
			)
			extra["normally_closed"] = True
			refs += (VPX_SCRIPT_SOURCE, IDENTITY_SOURCE)
			notes += " Retained script: trigger sw115 follows the ball."
		else:
			physical["part_number"] = "5647-12693-04"
			notes += (
				" The basket-hold microswitch where a made basket's ball is held (Switch Locations F7, part 5647-12693-04); the Flipper "
				"Circuit Diagram marks F7 '*BASKET HOLD', a flipper circuit used for another purpose. Not inverted by PinMAME's mask; the "
				"complemented flipper-column read gives the ROM the public level, and the T.1 sweep named 'BASKET HOLD' (F7 BLK-GRY) at "
				"public 1, a closed contact: normally_closed is false."
			)
			extra["normally_closed"] = False
			refs += (VPX_SCRIPT_SOURCE,)
			notes += " Retained script: trigger sw117 follows the ball."
		if address in {115, 117}:
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
					"location": "WPC-95 CPU board", "switch_type": "dip",
					"notes": "WPC-95 CPU-board country DIP bank; the manual's DIP Switch Chart sets the country. No ON/OFF combination is asserted here; the ROM's T.15 DIP SWITCH TEST shows the positions.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Outputs -------------------------------------------------------------------------------------------
SOLENOID_NOTES = {
	1: "Auto Plunger Assembly A-21553 (coil AE-24-900) at the bottom of the shooter lane: the ROM fires it to launch the ball from the shooter lane (switch 15) when the SHOOT button (switch 11) is pressed or a ball is served automatically; there is no manual plunger.",
	3: "Left Ramp Diverter Assembly A-21531: diverts the left ramp so a ball entering it (switch 45) is sent to the basket instead of the left ramp's exit (pinned nbaf.c's simulation routes a left-ramp entry to Basket Made while it is on).",
	4: "Right Loop Diverter Assembly A-21530: diverts a ball in the right loop (switch 37) into the jet bumpers instead of letting it complete the loop toward In The Paint position 4 (pinned nbaf.c's simulation follows the same routing).",
	5: "Eject Assembly A-21405-1 under the Crazy Bob's vendor hole (switch 25), the left eject that collects Stadium Goodies.",
	6: "Loop Gate Assembly A-17796 (coil A-14406): on the left loop, with the gate up the ball completes the loop onto the left-loop ramp exit (63) instead of feeding In The Paint (pinned nbaf.c's simulation).",
	7: "Backbox Flipper Assembly A-21717 (coil FL-11753) in the backbox: flips the small backbox basketball at the backbox basket (switch 12). The table and the Locations list mark it IN BACKBOX; it is the IPDB 'mechanical backbox animation'.",
	8: "NBA Magnet Assembly A-21520 (coil B-13522), which the solenoid drawing points out at the middle of the In The Paint ring under the basket. The manual does not describe its use; in pinned nbaf.c's simulation it catches a ball passed between positions 2 and 3 and the ball leaving Basket Hold, and releases it toward the jets when it turns off.",
	9: "Ball Trough Assembly A-19963-1 (coil AE-28-1500): kicks the ball over the trough eject opto (31) into the shooter lane.",
	10: "Slingshot (Coil & Bracket B-9362-R-3) behind the left slingshot's kick switch 57; the ROM fired it when the T.1 sweep closed 57.",
	11: "Slingshot (Coil & Bracket B-9362-R-3) behind the right slingshot's kick switch 58; the ROM fired it when the T.1 sweep closed 58.",
	12: "Jet bumper coil (A-9415-3) of the left jet bumper, switch 61; the ROM fired it when the T.1 sweep closed 61.",
	13: "Jet bumper coil (A-9415-2) of the middle jet bumper, switch 62; the ROM fired it when the T.1 sweep closed 62.",
	14: "Jet bumper coil (A-9415-2) of the right jet bumper, switch 23 (the matrix places that bumper in column 2); the ROM fired it when the T.1 sweep closed 23.",
	15: "Pass Assembly No. 2 (A-21411-2): passes the ball held at In The Paint position 2 (switch 67) to the right, toward position 3.",
	16: "Pass Assembly No. 2 (A-21411-2): passes the ball held at In The Paint position 2 (switch 67) to the left, toward position 1.",
	17: "Flasher at the eject (Crazy Bob's) kickout; #906 playfield flashlamp.",
	18: "Flasher on the left jet bumper; #906 playfield flashlamp.",
	19: "Upper left flasher: one #906 on the playfield (J111-3) and one #906 on the insert panel (J112-3, the Locations list's 'Insert Panel Flasher*'), so the quantity counts both bulbs and only the playfield one is placed.",
	20: "Upper right flasher: one #906 on the playfield (J111-4) and one #906 on the insert panel (J112-5), so the quantity counts both bulbs and only the playfield one is placed.",
	22: "Trophy insert flasher (C-13375, a #906 under the TROPHY insert). The retained table has no object for it (its callback writes a lamp state nothing reads, commented 'trophy insert TODO').",
	24: "Lower right and left flashers: two #906 playfield flashlamps in parallel on one line (J111-8, printed '#906 (2)'), one on each side of the lower playfield.",
	25: "Pass Assembly No. 1 (A-21411-1): passes the ball held at In The Paint position 1 (switch 68) to the right, toward position 2. The solenoid table marks 25-28 with tieback diodes at J109-5, -6, -8 and -9.",
	26: "Pass Assembly No. 3 (A-21411-3): passes the ball held at In The Paint position 3 (switch 66) to the left, toward position 2.",
	27: "Pass Assembly No. 3 (A-21411-3): passes the ball held at In The Paint position 3 (switch 66) to the right, toward position 4.",
	28: "Pass Assembly No. 4 (A-21411-4): passes the ball held at In The Paint position 4 (switch 65) to the left, toward position 3.",
	33: "Shoot coil (AE-23-800) of Pass Assembly No. 1: shoots the ball from In The Paint position 1 (switch 68) at the basket. It is the upper-right flipper power circuit (printed 'Upr. Rt. Power', Q84, J120-6).",
	34: "Shoot coil (AE-23-800) of Pass Assembly No. 2, In The Paint position 2 (switch 67); the upper-right flipper hold circuit (Q86). The solenoid table and the 3-6 coil drawing print its drive on J120-4, the Power Driver Board connector list on J120-5 with J120-4 N/C; the device and address agree, so the pin is a wiring detail and the table is followed.",
	35: "Shoot coil (AE-23-800) of Pass Assembly No. 3, In The Paint position 3 (switch 66); the upper-left flipper power circuit (Q81).",
	36: "Shoot coil (AE-23-800) of Pass Assembly No. 4, In The Paint position 4 (switch 65); the upper-left flipper hold circuit (Q83). The Locations list prints its description 'Shoot 3' (a repeat of 35); the solenoid table, the wiring pages and the ROM print SHOOT 4.",
	37: "Enable line of the defender motor: a WPC-95 low-power driver output (gates U3A/U3B, J110-1) into the High Current Driver Board C-13963-1, which runs the 14-8034 motor of the Defender Arm Assembly A-21413. The ROM's T.16 MOTOR TEST drives 37 alone to MOVE LEFT and 37 with 38 to MOVE RIGHT.",
	38: "Direction line of the defender motor (J110-3, into the High Current Driver Board C-13963-1); on, the motor runs the defender right, toward POS 4 (T.16 MOVE RIGHT). The Locations list prints the device part 14-8043 here where the solenoid table prints 14-8034 for both lines.",
	39: "Enable (blanking) line of the shot clock: J110-4 into the 2 LED Driver Board A-21399 (4029B counters and 4511 decoders) on the Backboard Assembly A-21393, whose 2 LED Display Board A-21380 shows the two digits. The ROM's T.4 prints its wire as YEL-WHT, as the manual does.",
	40: "Count line of the shot clock: J110-5 into the 2 LED Driver Board A-21399; each pulse counts the display down, which T.16 shows counting from 24. The ROM's T.4 prints its wire as GRN-WHT where the solenoid table and the shot clock wiring print BLU-WHT; the device and address agree, so the colour is a wiring detail.",
}
SOLENOID_ROLES = {7: "cabinet.backbox"}


def _solenoid_wiring(address: int) -> dict[str, Any]:
	printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
	board = "WPC-95 power driver board"
	wiring: dict[str, Any] = {"board": board, "control_wire": wire}
	if transistor:
		wiring["driver_transistor"] = transistor if transistor.startswith("Q") else f"logic gates {transistor}"
	if drive:
		wiring["control_connection"] = drive
	if voltage:
		wiring["power_connection"] = voltage
	return wiring


def _rom_note(address: int) -> str:
	if address not in ROM_SOLENOID_NAMES:
		return ""
	name, wires = ROM_SOLENOID_NAMES[address]
	test = "T.5 FLASHER TEST" if address in T5_ADDRESSES else ("T.12 FLIPPER COIL TEST" if address in T12_ADDRESSES else "T.4 SOLENOID TEST")
	return f" {test}: the ROM pulses public {address} and prints \"{name}\" with the wires {wires}."


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in FLIPPER_COILS:
			stage, printed, printed_type, voltage, transistor, control, wire = FLIPPER_COILS[address]
			side = "right" if address in {45, 46} else "left"
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			notes = (
				f"Lower {side} flipper {stage} winding (coil FL-11630, printed coil colour RED), printed Fliptronic circuit {printed} "
				f"('{printed_type}', driver {transistor}, {control}, {wire}, supply {voltage}). PinMAME publishes the lower flipper "
				f"windings at 45-48; the ROM's T.12 FLIPPER COIL TEST drives {'45 and 46' if side == 'right' else '47 and 48'} for "
				f"{side[0].upper()}. FLIP. POWER and only {'46' if side == 'right' else '48'} for {side[0].upper()}. FLIP. HOLD."
			) + _rom_note(address)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE)
			if address in SOLENOID_SCRIPT:
				notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
				refs += (VPX_SCRIPT_SOURCE,)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
				"physical": {"part_number": "FL-11630", "assembly_part_number": SOLENOID_ASSEMBLIES[address], "notes": notes},
				"wiring": {"board": "WPC-95 power driver board", "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage},
			}
			spatial = located("solenoid", address, identifier, "effect")
			if spatial:
				extra["spatial"] = spatial
				extra["physical"]["notes"] += _spatial_note("solenoid", address)
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		if address in SOLENOID_LABELS or address in NOT_USED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_USED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
			notes = f"Printed solenoid table entry {address:02d} ({printed_type}, {'driver ' + transistor if transistor.startswith('Q') else 'gates ' + transistor}, wire {wire})."
			if fitted:
				notes += " " + SOLENOID_NOTES[address]
			if address in {33, 34, 35, 36}:
				notes += (
					" The Flipper Circuit Diagram marks the four SHOOT drives '*', a flipper circuit used for another purpose; nbafGameData "
					"declares FLIP_SOL(FLIP_L) only, so PinMAME publishes the ROM's drive here and never fabricates a flipper state."
				)
			else:
				notes += " The solenoid table and the Locations list print NOT USED with no connection or part."
				if address == 2:
					notes += " The ROM's T.4 SOLENOID TEST skips 2."
				else:
					notes += f" The ROM's T.5 FLASHER TEST skips {address}. The Solenoid/Flashlamp Locations drawing nonetheless prints a balloon 21; see the trophy insert flasher (22)."
			notes += _rom_note(address)
			if address in SOLENOID_SCRIPT:
				notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			elif fitted:
				notes += " The retained script registers no callback for it."
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("magnet" if address == 8 else ("control_signal" if address in {37, 38, 39, 40} else "coil"))
			physical: dict[str, Any] = {}
			if part and kind not in {"flasher"} and address not in {37, 38, 39, 40} and fitted:
				physical["part_number"] = part
			if address in {37, 38}:
				physical["part_number"] = "14-8034"
			if address in {39, 40}:
				physical["part_number"] = "A-21380"
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if address in FLASHER_SOLENOIDS:
				notes += f" Printed flashlamp {part} (#906 is 24-8802)."
				if address in FLASHER_COUNTS:
					physical["quantity"] = FLASHER_COUNTS[address]
			extra = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]}
			extra["wiring"] = _solenoid_wiring(address)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_SCRIPT:
				refs += (VPX_SCRIPT_SOURCE,)
			if address in ROM_SOLENOID_NAMES and address not in T5_ADDRESSES:
				refs += (SOLENOID_TEST_SOURCE,)
			if address in T5_ADDRESSES:
				refs += (FLASHER_TEST_SOURCE,)
			if address in {24, 25}:
				refs += (BLINKED_SOURCE,)
			if address == 19:
				refs += (EARLIER_FLASHER_SOURCE,)
				notes += " An earlier T.5 run at the previous PinMAME pin printed the same name and wires at this address."
			if address in {10, 11, 12, 13, 14}:
				refs += (EDGES_SOURCE,)
			if address in {37, 38, 39, 40}:
				refs += (MOTOR_TEST_SOURCE,)
			if address == 7:
				refs += (BACKBOX_TEST_SOURCE,)
				notes += " T.17 BACKBOX TEST fires it on every press of the SHOOT button (switch 11), with the coin door open or closed."
			if not fitted:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				availability = "unused"
			elif address in SOLENOID_ROLES:
				extra["roles"] = [SOLENOID_ROLES[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "backbox"
				availability = "used"
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, identifier, role)
				if spatial:
					extra["spatial"] = spatial
					notes += _spatial_note("solenoid", address)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		used = address in {29, 30, 31, 41, 42, 43, 44}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here (wpc.c core_write_pwm_output of WPC_GILAMPS >> 5 at 29-30); it is not an NBA Fastbreak playfield device. The service-test runs saw it toggle in the menus.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not an NBA Fastbreak playfield device.",
			31: "PinMAME's synthetic game-on state: init_nbaf calls wpc_set_fastflip_addr(0x7b), so this channel reflects the ROM's fast-flip RAM flag, not a relay. No WPC generation has a game-on relay here.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
			41: "PinMAME's WPC-95 backward-compatibility mirror of LPDC output 37 (core_getSol serves 41-44 from the 37-40 bits); it reports the same defender motor enable and is not an additional device. The T.4 and T.16 runs saw it change with 37 every time. The ROM's T.4 offers a further item, '41 COIN METER' (BLK-WHT GRY-YEL), for which PinMAME publishes nothing at 41 or anywhere else: the coin meter has no public address.",
			42: "PinMAME's mirror of LPDC output 38 (defender motor direction); not an additional device.",
			43: "PinMAME's mirror of LPDC output 39 (shot clock enable); not an additional device.",
			44: "PinMAME's mirror of LPDC output 40 (shot clock count); not an additional device.",
			49: "PinMAME's simulator-only ball-shooter channel; NBA Fastbreak's real launcher is public solenoid 1.",
			50: "Reserved PinMAME output position before the first custom-output boundary; nbafGameData declares no custom solenoids (nbaf_getSol answers only 33-40 internally).",
		}[address]
		roles = ["internal.wpc-state"] if address in {29, 30, 31} else (["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"])
		refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((SOLENOID_TEST_SOURCE, MOTOR_TEST_SOURCE) if address in {41, 42, 43, 44} else ())
		items.append(
			_device(
				identifier, label, "virtual", SOLENOID_GROUP, address, "used" if used else "unused", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


LAMP_SCRIPT_EXCEPTIONS = {
	67: "the table has no Light for it and draws it as Flupper dome 9", 68: "the table draws it as Flupper dome 8",
	77: "the table draws it as Flupper dome 6", 78: "the table draws it as Flupper dome 7",
}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			assembly, bulb, socket, description = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"quantity": 2 if address == 61 else 1, "assembly_part_number": assembly}
			notes = (
				f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description "
				f'"{description}".'
			)
			if bulb:
				notes += f" Printed bulb {bulb}" + (f", socket {socket}." if socket and socket != "-----" else ".")
			notes += (
				f" The ROM's T.8 SINGLE LAMPS TEST lights public lamp {address} alone and prints its wires as RED-{('BRN', 'BLK', 'ORN', 'YEL', 'GRN', 'BLU', 'VIO', 'GRY')[row - 1]} "
				f"YEL-{('BRN', 'RED', 'ORN', 'BLK', 'GRN', 'BLU', 'VIO', 'GRY')[column - 1]}."
			)
			if address == 61:
				notes += " Item 61 is printed twice ('1 OF 2' on A-21551 and '2 OF 2' on A-21549): the footnote says it lights two bulbs on separate lamp boards, the two RAMPS: 3 POINTS inserts in front of the left and center ramps."
			if address == 84:
				notes += " The Lamp Locations list prints its bulb part number 24-6768, a number its legend does not define; the other two lamps of the (3)PT group print 24-8768 (#555)."
			if address in IN_THE_PAINT_LAMPS:
				notes += f" Lamp for In The Paint shooter position {IN_THE_PAINT_LAMPS[address]}: a lamp assembly whose socket is not sold separately; making a basket from that position lights it, and lighting all four starts Around The World multiball."
			if address == 43:
				notes += " The matrix and the Lamp Locations list both name this cell RIGHT RETURN LANE on an A-21548 insert assembly, where the left return lane (38) uses an A-17835 lane lamp."
			if address in LAMP_SCRIPT_EXCEPTIONS:
				notes += f" Retained script: {LAMP_SCRIPT_EXCEPTIONS[address]}."
			physical["notes"] = notes
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"physical": physical,
				"wiring": {
					"board": "WPC-95 power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in CABINET_LAMPS:
				extra["roles"] = [CABINET_LAMPS[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet button"
				physical["notes"] += " Lamp inside the lit " + ("SHOOT (Ball Launch) button on the front molding." if address == 87 else "Start button.")
				physical.pop("quantity", None) if False else None
			else:
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
					physical["notes"] += _spatial_note("lamp", address)
			label = LAMP_LABELS.get(address, description.title().replace("'S", "'s"))
			items.append(
				_device(identifier, label, "lamp", LAMP_GROUP, address, "used", (MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE, VPX_SCRIPT_SOURCE), **extra)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (string, voltage, triac, drive, wire, playfield_bulb, backbox_bulb, rom_wires) in GI_STRINGS.items():
		identifier = f"gi.string-{string}"
		dimmable = address <= 2
		notes = (
			f"Printed general-illumination string {string:02d}: triac {triac}, wire {wire}, voltage {voltage}, drive {drive}; playfield bulbs {playfield_bulb}"
			+ (f", backbox bulbs {backbox_bulb}." if backbox_bulb else ", no backbox connection.")
		)
		if dimmable:
			notes += (
				f" The ROM's T.6 GENERAL ILLUMINATION TEST names it 'STRING {string}' ({rom_wires}) and steps its brightness on public GI {address} alone."
			)
		else:
			notes += (
				f" The table's footnote says strings 4 and 5 do not brighten and dim, they are always on; the ROM's T.6 names it 'STRING {string}' "
				f"'ON ONLY' ({rom_wires}), and public GI {address} stayed on in every snapshot of every service-test run."
			)
		if address == 4:
			notes += " Its third branch is the cabinet connection J104 (coin door), which lights the coin-door lamps."
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, GI_TEST_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{string:02d}"}],
			"wiring": {"board": "WPC-95 power driver board", "driver_transistor": triac, "control_connection": drive, "control_wire": wire, "power_connection": voltage},
		}
		spatial = located("gi", address, identifier, "emitter")
		if spatial:
			refs += (VPX_SCRIPT_SOURCE,)
			extra["spatial"] = spatial
			notes += (
				f" The retained table's UpdateGI drives its GI{address} light collection for this string; the placements are those lights "
				"with stacked render doubles collapsed, kept observed and without a quantity because the manual prints no per-string bulb "
				"count and no drawing locates GI bulbs, and the table's grouping is the author's."
			)
		else:
			notes += (
				" The retained table drives no light collection for this string (its UpdateGI handles strings 0-2 only), and no retained "
				"drawing or list locates its playfield bulbs, so it has no placement."
			)
		extra["physical"] = {"notes": notes}
		items.append(_device(identifier, f"General Illumination String {string}", "gi", GI_GROUP, address, "used", refs, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	shot_clock = located("display", 1, "display.shot-clock", "display")
	record: dict[str, Any] = {
		"id": "display.shot-clock",
		"label": "Shot clock two-digit seven-segment display",
		"kind": "segment",
		"controller_index": 1,
		"segment_start": 0,
		"width": 2,
		"physical_location": "playfield",
		"provenance": provenance("observed", CORE_SOURCE, MANUAL_SOURCE, MOTOR_TEST_SOURCE, VPX_SCRIPT_SOURCE),
	}
	if shot_clock:
		for placement in shot_clock["placements"]:
			placement["provenance"] = provenance("observed", MANUAL_SOURCE, CORE_SOURCE, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		record["spatial"] = shot_clock
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
		},
		record,
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


def mechanisms() -> list[dict[str, Any]]:
	flipper_refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE)
	return [
		_mechanism(
			"in-the-paint", "In The Paint shooters", "kicker",
			[_coil(25), _coil(15), _coil(16), _coil(26), _coil(27), _coil(28), _coil(33), _coil(34), _coil(35), _coil(36)],
			_matrix(68, 67, 66, 65),
			"Four ball-holding saucers on a ring below the top lanes, around the playfield basket: In The Paint positions 1-4 from "
			"left to right, each a Pass Assembly (A-21411-1 to -4) with a saucer switch (68, 67, 66, 65) and a shoot coil on a "
			"Fliptronic upper-flipper circuit (33-36, AE-23-800) that shoots the ball at the basket. Pass coils move the ball "
			"along the ring: Pass Right 1 (25) from 1 to 2, Pass Left 2 (16) from 2 to 1, Pass Right 2 (15) from 2 to 3, "
			"Pass Left 3 (26) from 3 to 2, Pass Right 3 (27) from 3 to 4, Pass Left 4 (28) from 4 to 3. When IN THE PAINT is lit, a "
			"left or right loop shot feeds the ring (the left loop through the loop gate, 6; the right loop's exit 38 to "
			"position 4) and the shot clock starts at 24; the shot map says to use the flippers to pass, and a shot must be taken "
			"from a position the defender does not block; a basket from a position lights that position's lamp (77, "
			"78, 68, 67 for positions 1-4). A blocked shot drops into the jet bumpers. Completing all four starts Around The World "
			"multiball. The ROM's T.4 names and pulses every pass and shoot coil.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("position-1", "Position 1 (left)", _matrix(68), "Pass Right 1 (25) passes right; Shoot 1 (33) shoots."),
				("position-2", "Position 2", _matrix(67), "Pass Left 2 (16) and Pass Right 2 (15); Shoot 2 (34)."),
				("position-3", "Position 3", _matrix(66), "Pass Left 3 (26) and Pass Right 3 (27); Shoot 3 (35)."),
				("position-4", "Position 4 (right)", _matrix(65), "Pass Left 4 (28) passes left; Shoot 4 (36)."),
			],
			"A-21411",
		),
		_mechanism(
			"defender", "Defender", "motorized", [_coil(37), _coil(38)], _matrix(55, 54, 53, 52, 51),
			"The Defender Arm Assembly A-21413 swings a defender figure between the In The Paint positions and the basket to block "
			"shots. A 14-8034 motor runs on the High Current Driver Board C-13963-1 from two WPC-95 low-power lines: 37 enables the "
			"motor and 38 sets the direction. The Defender Switch Board A-21402 carries five optos that report the arm at Position 1, "
			"Position 2, the Lock position, Position 3 and Position 4 (switches 55, 54, 53, 52, 51), which the ROM's T.16 MOTOR TEST "
			"draws left to right as POS 1, POS 2, LOCK, POS 3, POS 4. In T.16, run with PinMAME's own defender model answering the "
			"motor, the self-test homed the arm to POS 4, MOVE LEFT drove 37 alone and stopped at POS 3, and MOVE RIGHT drove 37 with "
			"38 and returned to POS 4; AUTO RUN cycled it. That model (pinned nbaf.c, 80 steps, POS 4 at one end, POS 1 at the other "
			"and LOCK midway, starting at LOCK) and the retained table's cvpmMech (65 steps, the same order, its walls indexed so POS 4 "
			"is at the right) are synthetic: the run proves the ROM's contract with such a model, not the physical arm's travel, "
			"speed or opto spacing. The manual does not describe what the lock position is used for.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, MOTOR_TEST_SOURCE, EDGES_SOURCE),
			[
				("position-1", "Position 1", _matrix(55), "Defender in front of In The Paint position 1 (left)."),
				("position-2", "Position 2", _matrix(54), "Defender in front of position 2."),
				("lock", "Lock position", _matrix(53), "Defender at the lock position, midway."),
				("position-3", "Position 3", _matrix(52), "Defender in front of position 3."),
				("position-4", "Position 4", _matrix(51), "Defender in front of position 4 (right); the T.16 self-test homes here."),
			],
			"A-21413",
		),
		_mechanism(
			"playfield-basket", "Playfield basket and ball catch", "other", [_coil(8)], ["switch.generic-115", "switch.generic-117"],
			"The aerial hoop over In The Paint: a made basket breaks the Basket Made opto (F5, public 115, on the 24-Opto Switch "
			"Board A-15646), and the ball comes to rest on the Basket Hold microswitch (F7, public 117) before the game returns it. "
			"The NBA Magnet Assembly A-21520 (Ball Catch Magnet, solenoid 8) sits at the middle of the ring under the basket; in "
			"pinned nbaf.c's simulation it catches a ball passed between positions 2 and 3 and the ball leaving Basket Hold. "
			"The left ramp diverter (3) can also send a left-ramp shot to the basket. F5 and F7 are Fliptronic positions used for "
			"another purpose (the Flipper Circuit Diagram's '*'). IPDB notes two playfield versions that differ only in how this "
			"opto's wire is routed.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, IDENTITY_SOURCE),
			None, "A-21520",
		),
		_mechanism(
			"backbox-basketball", "Backbox basketball game", "toy", [_coil(7)], _matrix(12),
			"In the backbox a small flipper (Backbox Flipper Assembly A-21717, coil FL-11753, solenoid 7) at the lower right flips a "
			"captive ball at a basket on the far left whose switch (12, A-21710) scores it. The ROM fires it after jet-bumper hit "
			"counts (Power Points), during Hot Dog Mania, Egyptian Soda and multiballs, and lets the player time it with the "
			"flipper buttons or SHOOT button in Pizza Power Shots, where a basket scores the 1, 2 or 3 points shown. T.17 BACKBOX "
			"TEST fires 7 on each SHOOT press and marks BACKBOX while 12 is closed.",
			(MANUAL_SOURCE, IDENTITY_SOURCE, BACKBOX_TEST_SOURCE, VPX_SCRIPT_SOURCE),
			None, "A-21717",
		),
		_mechanism(
			"shot-clock", "Shot clock", "other", [_coil(39), _coil(40)], [],
			"A two-digit LED display on the playfield Backboard Assembly A-21393: the 2 LED Driver Board A-21399 (two 4029B counters "
			"and two 4511 decoders) counts down on each pulse of the count line (40) and the enable line (39) blanks or shows it; the "
			"2 LED Display Board A-21380 holds the digits. The ROM sets it to 24 for timed modes and In The Paint, and T.16 runs it "
			"from 24 down to 0. PinMAME's nbaf.c models the same counter from the two lines and publishes it as display 1, which "
			"counted 23, 22, ... in the T.16 run. The retained table draws it from that display (Controller.ChangedLEDs), not from "
			"solenoid callbacks.",
			(MANUAL_SOURCE, CORE_SOURCE, MOTOR_TEST_SOURCE, VPX_SCRIPT_SOURCE),
			None, "A-21393",
		),
		_mechanism(
			"ball-trough", "Ball trough", "kicker", [_coil(9)], _matrix(31, 32, 33, 34, 35),
			"Ball Trough Assembly A-19963-1 with four balls: drained balls collect over the Trough Ball 1-4 optos (32-35, IR pairs "
			"on the A-18617-1 LED and A-18618-1 photo-transistor boards) and the trough eject coil (9) kicks the lowest ball past "
			"the Trough Eject opto (31) into the shooter lane. The optos read a ball when it breaks the beam.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("trough-eject", "Trough eject", _matrix(31), "Ball at the eject position, over the trough eject coil."),
				("trough-1", "Trough, 1 ball", _matrix(32), "At least one ball in the trough."),
				("trough-2", "Trough, 2 balls", _matrix(33), "At least two balls."),
				("trough-3", "Trough, 3 balls", _matrix(34), "At least three balls."),
				("trough-4", "Trough, 4 balls", _matrix(35), "All four balls."),
			],
			"A-19963-1",
		),
		_mechanism(
			"auto-plunger", "Auto plunger and shooter lane", "kicker", [_coil(1)], _matrix(15, 11),
			"No manual plunger: the Auto Plunger (A-21553, solenoid 1) launches the ball resting on the shooter-lane switch (15) when "
			"the SHOOT button (11) is pressed or a ball is served (Inbound Pass, ball saves). Service Bulletin 99 fixes a ball trap "
			"at the plunger-lane entrance to the right ramp (replace a plastic pin with a 6-32 ESNA nut, kit A-22014).",
			(MANUAL_SOURCE, BULLETIN_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "A-21553",
		),
		_mechanism(
			"eject-hole", "Crazy Bob's eject", "kicker", [_coil(5)], _matrix(25),
			"The left eject hole (Crazy Bob's vendor stand, switch 25) holds the ball and the Eject Assembly A-21405-1 (solenoid 5) "
			"kicks it out; visiting it collects the Stadium Goodies modes. Flasher 17 lights the kickout.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "A-21405-1",
		),
		_mechanism(
			"diverters-and-gate", "Left ramp diverter, right loop diverter and loop gate", "diverter", [_coil(3), _coil(4), _coil(6)],
			_matrix(45, 46, 37, 38, 47, 48, 63),
			"Three routing devices: the Left Ramp Diverter (A-21531, solenoid 3) sends a left-ramp shot (entry 45) to the basket "
			"instead of the left ramp exit (made 46); the Right Loop Diverter (A-21530, solenoid 4) sends a right-loop ball (entry 37) "
			"into the jet bumpers instead of around the loop (exit 38) toward In The Paint position 4; the Loop Gate (A-17796, "
			"solenoid 6) on the left loop (enter 47, made 48) sends the ball onto the left loop ramp exit (63) instead of into In The "
			"Paint. The routing follows pinned nbaf.c's simulation, which matches the shot map's description of the feeds.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)],
			["switch.generic-111", "switch.generic-112", "switch.generic-116"],
			"Flipper assembly A-14876-R with an FL-11630 coil (power 45, hold 46, printed circuits 29-30) and an SW-1A-194 "
			"end-of-stroke switch (F1, 111) that PinMAME synthesizes. The cabinet button breaks both optos of the right Flipper Opto "
			"Board A-17316 (F2, 112 and F6, 116); the ROM fires the flipper from either. During In The Paint the flipper buttons pass "
			"the ball.",
			flipper_refs, None, "A-14876-R",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)],
			["switch.generic-113", "switch.generic-114", "switch.generic-118"],
			"Flipper assembly A-15849-L with an FL-11630 coil (power 47, hold 48, printed circuits 31-32) and an SW-1A-194 "
			"end-of-stroke switch (F3, 113) that PinMAME synthesizes. The cabinet button breaks both optos of the left Flipper Opto "
			"Board A-17316 (F4, 114 and F8, 118); the ROM fires the flipper from either.",
			flipper_refs, None, "A-15849-L",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(10), _coil(11)], _matrix(57, 58),
			"Two slingshots (coil and bracket B-9362-R-3) with kick switches A-17800 and score switches A-17794 on 57 and 58; the ROM "
			"fired 10 for 57 and 11 for 58 even inside the T.1 test.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "B-9362-R-3",
		),
		_mechanism(
			"jet-bumpers", "Jet bumpers", "other", [_coil(12), _coil(13), _coil(14)], _matrix(61, 62, 23, 56),
			"Three jet bumpers (A-9415 coils) with switches 61 (left), 62 (middle) and 23 (right, in matrix column 2); the ROM fired "
			"12, 13 and 14 for them even inside T.1. Balls leave the jets past the Jets Ball Drain switch (56). Jet hits build the "
			"Power Hoops levels and trigger backbox Power Points baskets.",
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
	"switch-locations": (64, 403, 4956, "16.54", 300, "1684x2885"),
	"lamp-locations": (65, 409, 4952, "16.51", 300, "1685x2889"),
	"solenoid-flashlamp-locations": (63, 396, 4956, "16.58", 299, "1679x2878"),
}


def _excerpt(name: str, locator: str, *, image: bool = False, method: str = "manual", reviewed: bool = True, credit: str = TRANSCRIBED) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.nba-fastbreak.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image:
		page, xref, mask, inches, dpi, size = DRAWING_DERIVATIONS[name]
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = (
			f"{MANUAL_NAME} page {page}, crop box 0.57,0.07,0.91,0.95, scanned page rendered at its native resolution (embedded image "
			f"xref {xref} through its {mask}px /Mask over a 1652px background, {mask}px across {inches}in), rendered at {dpi} dpi, grayscale, "
			f"{size} WebP quality 80"
		) if name != "lamp-locations" else (
			f"{MANUAL_NAME} page {page}, crop box 0.57,0.07,0.91,0.95, scanned page rendered at its native resolution (embedded image "
			f"xref {xref} through its {mask}px /Mask over a 1651px background, {mask}px across {inches}in), rendered at {dpi} dpi, grayscale, "
			f"{size} WebP quality 80"
		)
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("switch-matrix", "PDF page 67 left half, printed 2-48, Switch Matrix with the dedicated and flipper grounded-switch blocks and the measured opto shading; Section 3 reprint PDF 70 (3-2, 3-3) compared"),
		_excerpt("lamp-matrix", "PDF page 67 right half, printed 2-49, Lamp Matrix; Section 3 reprint PDF 71 (3-4) compared"),
		_excerpt("solenoid-flasher-table", "PDF page 68, printed 2-50, Solenoid/Flasher Table with the general-illumination, flipper-circuit and motor and shot clock blocks"),
		_excerpt("switch-locations", "PDF page 64, printed 2-42 (Switch Locations parts list) and 2-43 (playfield drawing; image)", image=True),
		_excerpt("lamp-locations", "PDF page 65, printed 2-44 (Lamp Locations parts list) and 2-45 (playfield drawing; image)", image=True),
		_excerpt("solenoid-flashlamp-locations", "PDF page 63, printed 2-40 (Solenoid/Flashlamp Locations list) and 2-41 (playfield drawing; image)", image=True),
		_excerpt("power-driver-board", "PDF pages 83-84, printed 3-29 to 3-31, Power Driver Board connector list"),
		_excerpt("section-3-boards", "PDF pages 72-85, printed 3-6 to 3-33, solenoid and flashlamp wiring, flipper and GI circuits, opto boards, Defender Switch Board, shot clock boards, High Current Driver Board and coin door interface"),
		_excerpt("differences-march-vs-may", "Every table above compared with the March 1997 edition (PDF 118-131); the differences found"),
	]


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
			"locator": "Pinned catalog driver records for the nbaf_* clone tree (nbaf_31 parent; nbaf_11, nbaf_11a, nbaf_11s, nbaf_115, nbaf_21, nbaf_22, nbaf_23)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/nbaf.c nbafGameData: GEN_WPC95, nbaf_dispDMD (a 128x32 DMD plus a two-digit CORE_SEG7|CORE_NODISP "
				"display at layout index 1), FLIP_SW(FLIP_L|FLIP_U) | FLIP_SOL(FLIP_L), no custom switch columns, lamp columns or solenoids, "
				"the inverted-switch mask {0x00,0x00,0x00,0x7f,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x10} (column 3 rows 1-7 and Cust bit 4, "
				"public 31-37 and 115 under wpc_sw2m), nbaf_wpc_w counting the shot clock from solenoid 40 rising edges while 39 enables "
				"it, the defender mech_add (37 enable, 38 direction, MECH_LINEAR|MECH_STOPEND|MECH_ONEDIRSOL, 80 positions, switches "
				"51/52/53/54/55 at 0, 1/3, 1/2, 2/3 and the far end, starting at the lock), wpc_set_fastflip_addr(0x7b), nbaf_getSol "
				"answering 33-40 from the flipper-coil register, and the simulator's ball routing; src/wpc/wpc.c WPC_FLIPPERSW95 "
				"returning ~swMatrix[CORE_FLIPPERSWCOL], the 29-31 state mirror; src/wpc/core.c core_getSol (37-40 mirrored at 41-44 on "
				"WPC-95) and core_updateSw (end-of-stroke synthesis). The runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-95.json", "revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "revision": "Wayback capture, 2025",
			"sha256": IPDB_PAGE_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"IPDB machine 4023 'NBA Fastbreak' (Midway Manufacturing Company, trade name Bally, March 1997, model 50053, Williams "
				f"WPC-95, 4,414 units, four balls). IPDB is Cloudflare-gated, so the page was read from the Wayback capture {IPDB_WAYBACK} "
				"(retained as ipdb-4023.html). Its title, date and model number match the manual cover (16-50053.1-101) and the machine "
				"being curated; its notes describe the backbox flipper and basket and two playfield versions that differ in the "
				"basket-made opto's wire routing."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine 4023 page, title line to image list", reviewed=False, credit="curator, from the retained HTML")],
		},
		pdf(
			MANUAL_SOURCE, "manual", MANUAL_NAME,
			"Midway/Bally NBA Fastbreak operations manual, May 1997 FINAL, document 16-50053.1-101, with schematics: an 87-page scan of "
			"two-page spreads (mixed raster, 300 dpi line art over a 100 dpi background, with an Acrobat Paper Capture text layer used "
			"only to find pages). PDF 63-65 carry the location lists and drawings (2-40 to 2-45), PDF 67-68 the switch and lamp "
			"matrices and the solenoid/flasher table (2-48 to 2-50), PDF 69-86 Section 3 wiring, PDF 15-16 the Linking Kit "
			"instructions (1-10, 1-11). It is the later edition; its tables agree with the March edition except where "
			"differences-march-vs-may.md says.",
			MANUAL_SHA256, _manual_excerpts(),
		),
		pdf(
			MANUAL_MARCH_SOURCE, "manual", MANUAL_MARCH_NAME,
			"The March 1997 edition of the same operations manual (164 single pages, ABBYY FineReader text layer), used for the test "
			"menu and game rules text and as the comparison copy of every table; a copy of one table is not a second source.",
			MANUAL_MARCH_SHA256,
			[
				_excerpt("service-tests", "PDF pages 40-44, printed 1-18 to 1-22, the Test menu and T.1-T.18", method="ocr", reviewed=False, credit="curator; the ABBYY text layer, unedited"),
				_excerpt("game-rules", "PDF pages 14-19, printed II-VII, playfield shots and game rules", method="ocr", reviewed=False, credit="curator; the ABBYY text layer, unedited"),
			],
		),
		pdf(
			BULLETIN_SOURCE, "service_bulletin", BULLETIN_NAME,
			"Service Bulletin 99 (May 14, 1997): a ball trap at the plunger-lane entrance to the right ramp, fixed with a 6-32 ESNA nut "
			"in place of a plastic pin (kit A-22014). It changes no switch, lamp or solenoid.",
			BULLETIN_SHA256,
			[_excerpt("service-bulletin-99", "Single page", method="ocr", reviewed=False, credit="curator; the PDF text layer, unedited")],
		),
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/nba-fastbreak-1997/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPW mod recreation of the physical machine (file v1.3, info table_version 1.1). Exact playfield bounds "
				f"are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for "
				f"named table objects. The ancestral VPW mod v1.17.0 ({ANCESTOR_TABLE_NAME}, SHA-256 {ANCESTOR_TABLE_SHA256}) carries the same "
				"226 binding statements and is not an independent second table."
			),
			"license": "NOASSERTION", "attribution": "VPW (based on the tables by jpsalas, Aurich and bmiki75)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/nba-fastbreak-1997/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				'Retained embedded VPW script (157,269 bytes). Runtime and mechanism-causality authority: Const cGameName = "nbaf_31", '
				"UseSolenoids = 2, HandleMechanics = 0, the SolCallBack table, the cvpmBallStack trough and saucers, the cvpmMagnet ball "
				"catch, the cvpmMech defender (37/38, switches 51-55), the ChangedLamps/UpdateLamps lamp loop, UpdateGI for GI strings "
				"0-2 and the ChangedLEDs shot clock."
			),
			"license": "NOASSERTION", "attribution": "VPW table authors", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/nba-fastbreak-1997/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	] + [
		{
			"id": source_id, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/nba-fastbreak-nbaf_31-{name}.json",
			"revision": PINMAME_REVISION, "locator": locator, "license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		}
		for source_id, name, locator in RUNTIME_SOURCES
	] + [
		{
			"id": EARLIER_EDGES_SOURCE, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/wpc-95/nba-fastbreak-nbaf_31-switch-edges.json",
			"revision": "8371478a7640f1896dcdf565aed340dc5df989ba",
			"locator": "An earlier run of nbaf_31 at the previous pin that held public 12, 1-4 and 12 inside T.1 SWITCH EDGES: the ROM names public 1-3 LEFT, CENTER and RIGHT COIN SLOT, public 4 4TH COIN OPTION and public 12 BACKBOX BASKET.",
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": EARLIER_FLASHER_SOURCE, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/wpc-95/nba-fastbreak-nbaf_31-flasher-test.json",
			"revision": "8371478a7640f1896dcdf565aed340dc5df989ba",
			"locator": "An earlier run of nbaf_31 at the previous pin that stepped T.5 FLASHER TEST through 17, 18, 19, 20, 22 and 24; at step 19 the ROM prints UPPER LEFT with BLK-ORN RED-WHT.",
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/bally/nba-fastbreak-1997-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of the May manual's drawings 2-41, 2-43 and 2-45 (the committed "
				"300 dpi excerpt crops): every callout transcribed by an independent reader working only from the page, per-page control "
				"fits from the jet bumper caps and flipper pivots, and the callout fit; a table placement whose own callout lands within "
				"0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and generators are retained "
				"under review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION", "attribution": "PinMAME game definitions contributors",
		},
	]


RUNTIME_SOURCES = (
	(EDGES_SOURCE, "switch-edges-sweep", "One hash-pinned LibPinMAME harness run of nbaf_31 from empty NVRAM with built-in mechanisms disabled (tools/harness-scenarios/wpc-95/nbaf-switch-edges-sweep.json): inside T.1 SWITCH EDGES every public matrix address 11-88 and every Fliptronic address 111-118 is set to 1 and back to 0 for 2 s each. The ROM names each fitted switch at public 1 (24 on its 1 -> 0 edge), names nothing for 71-88, fires the jet and sling coils for their switches and the lower flippers for 112/116 and 114/118."),
	(SOLENOID_TEST_SOURCE, "solenoid-test", "One hash-pinned run of nbaf_31 (nbaf-solenoid-test.json) stepping T.4 SOLENOID TEST: it walks 1, 3-16, 25-28 and 33-41, naming each driver and its wires and pulsing that public address (37-40 also at 41-44); its 41 COIN METER publishes nothing."),
	(BLINKED_SOURCE, "blinked-names", "One hash-pinned run of nbaf_31 (nbaf-blinked-names.json) taking eight frames at T.4 item 25 (PASS RIGHT 1) and T.5 item 24 (LOWER LEFT/RIGHT), whose names the other runs caught dark."),
	(FLASHER_TEST_SOURCE, "flasher-test-sweep", "One hash-pinned run of nbaf_31 (nbaf-flasher-test-sweep.json) stepping T.5 FLASHER TEST through 17, 18, 19, 20, 22 and 24, each named and pulsed."),
	(FLIPPER_TEST_SOURCE, "flipper-coil-test", "One hash-pinned run of nbaf_31 (nbaf-flipper-coil-test.json) stepping T.12 FLIPPER COIL TEST: R. FLIP. POWER drives 45 and 46, R. FLIP. HOLD 46, L. FLIP. POWER 47 and 48, L. FLIP. HOLD 48."),
	(GI_TEST_SOURCE, "gi-test", "One hash-pinned run of nbaf_31 (nbaf-gi-test.json) stepping T.6 GENERAL ILLUMINATION TEST: STRING 1-3 dim public GI 0-2 alone; STRING 4 and 5 are ON ONLY and public GI 3 and 4 stay on throughout."),
	(LAMP_TEST_SOURCE, "single-lamps", "One hash-pinned run of nbaf_31 (nbaf-single-lamps.json) stepping T.8 SINGLE LAMPS TEST through public lamps 11-88 in matrix order, each lit alone with its row and column wires printed."),
	(MOTOR_TEST_SOURCE, "motor-test", "One hash-pinned run of nbaf_31 with PinMAME's built-in defender mechanism enabled (nbaf-motor-test.json): T.16 MOTOR TEST homes to POS 4, MOVE LEFT drives 37 alone to POS 3, MOVE RIGHT 37 with 38 back to POS 4, and the shot clock display 1 counts down from 24."),
	(BACKBOX_TEST_SOURCE, "backbox-test", "One hash-pinned run of nbaf_31 (nbaf-backbox-test.json): T.17 BACKBOX TEST fires solenoid 7 on each press of public 11 (SHOOT), marks BACKBOX while public 12 is 1, and fires nothing for 112-118."),
)


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "NBA Fastbreak",
			"manufacturer": "Bally",
			"year": 1997,
			"kind": "physical_pinball",
			"ipdb_id": 4023,
			"opdb_id": "GrO0D-MQolo",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
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
		"controller": {"platform": "pinmame.wpc-95", "hardware_generation": "0x80", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/nba-fastbreak-1997.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"NBA Fastbreak device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"NBA Fastbreak mechanism {mechanism['id']} names unknown devices: {unknown}")
	seed = load_json(CALLOUT_SEED_PATH)
	for placement_id in seed.get("measurements", {}):
		drawing_callouts.measured(seed, placement_id)
	drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
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
			"manifest_uri": "external:pinmame-vpx-sources/bally/nba-fastbreak-1997/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/nba-fastbreak-1997-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "The retained table's collision object for the switch (trigger, target, kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are projected onto the trough's BallRelease kicker because the script derives them from a ball count; the five defender optos 51-55, which the table derives from its cvpmMech, are measured on the switch drawing, where each has its own leader.",
			"lamp": "The script-driven Light's own centre (render doubles collapsed by the smallest falloff), validated where the lamp drawing marks the same insert; the In The Paint lamps 67, 68, 77 and 78, which the table draws only as Flupper domes, take the dome base. Lamp 61's two bulbs are both placed.",
			"solenoid": "The object the solenoid callback moves (wall, gate, saucer kicker, magnet trigger, flipper, bumper, slingshot) or the Flupper dome base it lights, validated where the solenoid drawing's callout agrees. The defender motor lines 37/38, the shot clock lines 39/40 and the trophy insert flasher 22 have no table object and are measured on the drawing.",
			"gi": "Per-string collections of the table's UpdateGI lights for strings 1-3, collapsed where bulbs are stacked, observed only: the manual prints no per-string bulb count and no drawing locates GI bulbs. Strings 4 and 5 have no table collection and no placement.",
			"display": "The shot clock display at the midpoint of the table's two digit sprites on the backboard, observed.",
		},
		"unresolved_geometry": [
			"General illumination strings 4 and 5 (public GI 3 and 4) are wired to playfield #44 bulbs, but neither the retained table nor any retained drawing or count locates them, so they have no placement.",
			"The GI placements of strings 1-3 rest on the retained table's own grouping; no factory drawing or bulb count locates GI bulbs, so they stay observed.",
			"Placements the drawings do not confirm keep their observed status; each such device's note says what the drawing showed.",
		],
		"promotion_decision": "partial: every fitted device has an observed or validated placement or a controlled not-applicable record except the always-on GI strings 4 and 5, and no general-illumination placement can be validated from any retained drawing or count.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# NBA Fastbreak (Bally, 1997) spatial blockers",
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
		f"- used devices with no placement record: {len(report['without_placements'])} ({', '.join(f'`{item}`' for item in report['without_placements'])})",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready NBA Fastbreak artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale NBA Fastbreak author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"NBA Fastbreak deterministic artifact drift: {path}")
	print("NBA Fastbreak definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"NBA Fastbreak extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("NBA Fastbreak retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
