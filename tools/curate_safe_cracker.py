"""Curate the physical Bally Safe Cracker (1996) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived fact
as a literal and reads two committed seeds (the table-derived placements and the factory-drawing callout check), so
regeneration reproduces the canonical artifact byte-for-byte without reading the external evidence roots. ``--check``
refuses drift, and ``--regenerate`` is the only path that writes the definition, its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "bally.safe-cracker.1996"
PARTIAL_PATH = ROOT / "machines/partial/bally/safe-cracker-1996.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/safe-cracker-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge/bally/safe-cracker-1996.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/bally/safe-cracker-1996.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/bally/safe-cracker-1996-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/bally/safe-cracker-1996-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/safe-cracker-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/safe-cracker-1996.md"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
IDENTITY_SOURCE = "identity.bally.safe-cracker.1996"
MANUAL_SOURCE = "manual.bally.safe-cracker.1996"
BULLETIN_SOURCE = "service-bulletin-90.bally.safe-cracker.1996"
VPX_TABLE_SOURCE = "vpx-table.safe-cracker-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.safe-cracker-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.safe-cracker-1-0"
VPX_SCRIPT_V2_SOURCE = "vpx-script.safe-cracker-2-0-0"
EDGES_SOURCE = "runtime.safe-cracker.switch-edges-sweep"
SOLENOID_TEST_SOURCE = "runtime.safe-cracker.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.safe-cracker.flasher-test"
FLIPPER_TEST_SOURCE = "runtime.safe-cracker.flipper-coil-test"
GI_TEST_SOURCE = "runtime.safe-cracker.gi-test"
LAMP_TEST_SOURCE = "runtime.safe-cracker.single-lamps"
MOVING_TARGET_SOURCE = "runtime.safe-cracker.moving-target-test"
MOVING_TARGET_CODES_SOURCE = "runtime.safe-cracker.moving-target-codes"
TOKEN_TEST_SOURCE = "runtime.safe-cracker.token-test"
LIGHT_ROPE_SOURCE = "runtime.safe-cracker.light-rope-test"
DROP_TARGET_SOURCE = "runtime.safe-cracker.drop-target-test"
TOP_TROUGH_SOURCE = "runtime.safe-cracker.top-trough-test"
CALLOUT_SOURCE = "drawing-callouts.safe-cracker.2026-10-09"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-95"

TABLE_NAME = "Safe Cracker (Bally 1996) v1.0.vpx"
TABLE_SHA256 = "3f1e77be9e64dc202576dec9c07681e40b19c3e666824b0d3b85267358ac645b"
MODIFIED_TABLE_NAME = "Safe Cracker (Bally 1996).vpx"
MODIFIED_TABLE_SHA256 = "7583e22934590814ac58c95a3aff4a8373f0c4b4d4e4f10cd713990a828db265"
SCRIPT_SHA256 = "e224e815280ce8e74ec1d2dfe1562dee9e5675b3f379cb5031ff69c39007fa0a"
SCRIPT_V2_PATH = "special_audiopan_and_audiofade_patched/Safe Cracker (Bally 1996) v2.0.0.vbs"
SCRIPT_V2_SHA256 = "cdfcc3981c4ad305d015b067e3c6b1e69b5d654d3622611760bb16d0a3bdf192"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
MANUAL_NAME = "Bally_1996_Safe_Cracker_Manual.pdf"
MANUAL_SHA256 = "a51dd1611ff135878d082f124aafa215907ff0f13b4dd105f9e6c4864de01c04"
BULLETIN_NAME = "Bally_1996_Safe_Cracker_Service_Bulletin_90.pdf"
BULLETIN_SHA256 = "d4ca5fe924c5f2531b5d31c8a74c8b6f782036e2b79ba5a296c069fb3a9f3579"
IPDB_PAGE_SHA256 = "008770dc357150706973db1bfa6489b05bd6069d46afb9e9ec855b793c5c8155"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/bally.safe-cracker.1996/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=3782"
IPDB_WAYBACK = "https://web.archive.org/web/2024id_/https://www.ipdb.org/machine.cgi?id=3782"
WAYBACK_FILES = {
	MANUAL_NAME: "https://web.archive.org/web/20241127050553id_/https://www.ipdb.org/files/3782/" + MANUAL_NAME,
	BULLETIN_NAME: "https://web.archive.org/web/20241126224955id_/https://www.ipdb.org/files/3782/" + BULLETIN_NAME,
}
ACQUIRED_AT = "2026-10-09T19:54:00Z"
RIGHTS_NOTE = "Midway Manufacturing Company (trade name Bally); scan hosted by the Internet Pinball Machine Database"
PLAYFIELD_WIDTH = 862.0
PLAYFIELD_HEIGHT = 1875.0
TABLE_BOUNDS = "left=0 top=0 right=862 bottom=1875"

EXTRACTION_FILE_COUNT = 825
EXTRACTION_TOTAL_BYTES = 98720715
EXTRACTION_MANIFEST_SHA256 = "1746e58c6a386940c6692454ecbadc149c694bd64a25b8bac07a1b93d5a007a3"
EXTRACTION_RELATIVE_PATH = Path("bally/safe-cracker-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/safe-cracker-1996/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("sc_18s11", "sc_18n11", "sc_18s2", "sc_18ns2", "sc_17", "sc_17n", "sc_14", "sc_10", "sc_091", "sc_18pfx")
NO_PERCENTAGING = (
	" Pinned sc.c notes that the percentaging firmware limits the number of tokens the game issues by its earnings, so a game "
	"on free play issues very few; the No Percentaging build removes that limit. Token dispensing is firmware policy on the same "
	"token tubes, so the physical machine is unchanged."
)
DRIVER_COMPATIBILITY = {
	"sc_18s11": (
		"identical",
		"Production game ROM 1.8 (safe_18g.rom) with sound ROM S1.1 (su2-11.rom), the parent driver. Every service-test run behind this "
		"definition booted it; the retained v1.0 table names the older sc_18 set with the same game ROM image.",
	),
	"sc_18n11": ("identical", "Game ROM 1.8 No Percentaging (safe_18n.rom) with sound ROM S1.1; same wpc_m95S hardware and I/O." + NO_PERCENTAGING),
	"sc_18s2": ("identical", "Game ROM 1.8 with the German-speech sound ROM S2.4 (su2-24g.rom); same hardware and I/O."),
	"sc_18ns2": ("identical", "Game ROM 1.8 No Percentaging with the German-speech sound ROM S2.4; same hardware and I/O." + NO_PERCENTAGING),
	"sc_17": ("identical", "Game ROM 1.7 (g11-17g.rom) with sound ROM S1.0; pinned sc.c gives it the same scGameData I/O map."),
	"sc_17n": ("identical", "Game ROM 1.7 No Percentaging (g11-17n.rom) with sound ROM S1.0; same I/O map." + NO_PERCENTAGING),
	"sc_14": ("identical", "Game ROM 1.4 (g11-14.rom) with sound ROM S1.0; same I/O map."),
	"sc_10": ("identical", "Game ROM 1.0 (g11-10.rom) with sound ROM S1.0, the first production release; same I/O map."),
	"sc_091": (
		"identical",
		"Prototype game ROM 0.91 (sc_091.bin) with sound ROM S1.0; pinned sc.c gives it the same scGameData I/O map. An exploratory "
		"harness boot (review-artifacts safe-cracker-1996/harness/explore-091-menu) identifies it as 90003 REV. 0.91 and offers the same "
		"test menu as 1.8 through T.17 TOKEN TEST, including T.16 MOVING TGT.; no hardware difference is documented.",
	),
	"sc_18pfx": (
		"identical",
		"Zen Studios' 2019 Pinball FX image of game ROM 1.8 (safepfx_18g.rom), which pinned sc.c says differs from safe_18g.rom in four "
		"bytes and was packaged with the S1.0 sound ROMs. It runs on the same wpc_m95S board model, scGameData I/O map and init_sc "
		"auxiliary-lamp routing as the factory ROM and declares no separate physical edition; firmware provenance alone does not make it compatible.",
	),
}

# --- Switch data (switch-matrix.md, switch-locations.md, section-3-boards.md) ---------------------------
# address -> (switch part cell, printed description) from the Switch Locations list (2-42, 2-43).
SWITCH_LOCATIONS = {
	11: ("5647-12693-26", "Tp Trough (Roof)"), 12: ("5647-12693-26", "Tp Trough (Vari)"), 13: ("20-9663-16", "Start Button"),
	14: ("04-10346", "*Plumb Bob Tilt"), 15: ("5647-12693-19", "Right Orbit"), 16: ("5647-12693-19", "Left Outlane"),
	17: ("5647-12693-19", "Right Outlane"), 18: ("5647-12693-65", "Ball Shooter"), 21: ("A-17195-1", "*Slam Tilt"),
	22: ("5643-09288-00", "*Coin Door Closed"), 24: ("5643-09112-00", "*Always Closed"), 25: ("5647-12693-19", "Upper Right Flip Rollover"),
	26: ("5647-12693-19", "Left Return"), 27: ("5647-12693-19", "Right Return"), 28: ("20-10293", "Left Orbit"),
	31: ("A-18617-1 / A-18618-1", "Trough Eject (LED) / (Trans.)"), 32: ("A-18617-1 / A-18618-1", "Trough Ball 1 (LED) / (Trans.)"),
	33: ("A-18617-1 / A-18618-1", "Trough Ball 2 (LED) / (Trans.)"), 34: ("A-18617-1 / A-18618-1", "Trough Ball 3 (LED) / (Trans.)"),
	35: ("A-18617-1 / A-18618-1", "Trough Ball 4 (LED) / (Trans.)"), 36: ("A-16908 / A-16909", "Lockup 1 Front (LED) / (Trans.)"),
	37: ("A-16908 / A-16909", "Lockup 2 Rear (LED) / (Trans.)"), 41: ("A-16908 / A-16909", "Kick Back (LED) / (Trans.)"),
	42: ("A-16908 / A-16909", "Left Big Kick (LED) / (Trans.)"), 43: ("A-16908 / A-16909", "*Token Chute Jam (LED) / (Trans.)"),
	44: ("SW-11A-37-1", "Left Jet"), 45: ("SW-11A-37-1", "Right Jet"), 46: ("SW-11A-37-1", "Top Jet"),
	47: ("SW-1A-114 / SW-1A-120", "Left Slingshot (kicker) / (score)"), 48: ("SW-1A-114 / SW-1A-120", "Right Slingshot (kicker) / (score)"),
	51: ("A-18530-6", "(A)LARM Standup"), 52: ("A-18530-6", "A(L)ARM Standup"), 53: ("A-20976-6", "AL(A)RM Standup"),
	54: ("A-17799-6", "ALA(R)M Standup"), 55: ("A-17799-6", "ALAR(M) Standup"), 56: ("A-20906", "Vari Target C"),
	57: ("A-20906", "Vari Target B"), 58: ("A-20906", "Vari Target A"), 61: ("A-13609", "Top Left 3-Bank Top"),
	62: ("A-13609", "Top Left 3-Bank Middle"), 63: ("A-13609", "Top Left 3-Bank Bottom"), 64: ("A-13609", "Top Right 3-Bank Bottom"),
	65: ("A-13609", "Top Right 3-Bank Middle"), 66: ("A-13609", "Top Right 3-Bank Top"), 67: ("20-10293", "Top Left Lane"),
	68: ("5647-12693-15", "Top Popper"), 71: ("A-13609", "Bottom Left 3-Bank Top"), 72: ("A-13609", "Bottom Left 3-Bank Middle"),
	73: ("A-13609", "Bottom Left 3-Bank Bottom"), 74: ("A-13609", "Bottom Right 3-Bank Bottom"), 75: ("A-13609", "Bottom Right 3-Bank Middle"),
	76: ("A-13609", "Bottom Right 3-Bank Top"), 77: ("5647-12693-26", "Bank Kickout"), 78: ("20-10293", "Top Right Lane"),
	81: ("20-10301", "*Left Token Level"), 82: ("20-10301", "*Right Token Level"), 83: ("5647-12693-21", "Ramp Entrance"),
	84: ("5647-12693-11", "Ramp Made"), 85: ("A-20952", "Wheel Channel A"), 86: ("A-20952", "Wheel Channel B"),
}
SWITCH_LABELS = {
	11: "Top Trough (Roof)", 12: "Top Trough (Vari)", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Right Orbit", 16: "Left Outlane",
	17: "Right Outlane", 18: "Ball Shooter", 21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed", 25: "Upper Right Flip Rollover",
	26: "Left Return", 27: "Right Return", 28: "Left Orbit", 31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2",
	34: "Trough Ball 3", 35: "Trough Ball 4", 36: "Lockup 1 Front", 37: "Lockup 2 Rear", 41: "Kickback", 42: "Left Big Kick",
	43: "Token Chute Jam", 44: "Left Jet", 45: "Right Jet", 46: "Top Jet", 47: "Left Slingshot", 48: "Right Slingshot",
	51: "(A)LARM Standup", 52: "A(L)ARM Standup", 53: "AL(A)RM Standup", 54: "ALA(R)M Standup", 55: "ALAR(M) Standup",
	56: "Vari Target C", 57: "Vari Target B", 58: "Vari Target A", 61: "Top Left 3-Bank Top", 62: "Top Left 3-Bank Middle",
	63: "Top Left 3-Bank Bottom", 64: "Top Right 3-Bank Bottom", 65: "Top Right 3-Bank Middle", 66: "Top Right 3-Bank Top",
	67: "Top Left Lane", 68: "Top Popper", 71: "Bottom Left 3-Bank Top", 72: "Bottom Left 3-Bank Middle", 73: "Bottom Left 3-Bank Bottom",
	74: "Bottom Right 3-Bank Bottom", 75: "Bottom Right 3-Bank Middle", 76: "Bottom Right 3-Bank Top", 77: "Bank Kickout",
	78: "Top Right Lane", 81: "Left Token Level", 82: "Right Token Level", 83: "Ramp Entrance", 84: "Ramp Made",
	85: "Wheel Channel A", 86: "Wheel Channel B",
}
SWITCH_TYPES = {
	11: "microswitch", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "tilt", 22: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	28: "unknown", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 41: "opto", 42: "opto",
	43: "opto", 44: "leaf", 45: "leaf", 46: "leaf", 47: "leaf", 48: "leaf", 51: "other", 52: "other", 53: "other", 54: "other",
	55: "other", 56: "opto", 57: "opto", 58: "opto", 61: "opto", 62: "opto", 63: "opto", 64: "opto", 65: "opto", 66: "opto",
	67: "unknown", 68: "microswitch", 71: "opto", 72: "opto", 73: "opto", 74: "opto", 75: "opto", 76: "opto", 77: "microswitch",
	78: "unknown", 81: "unknown", 82: "unknown", 83: "microswitch", 84: "microswitch", 85: "opto", 86: "opto",
}
SWITCH_ROLES = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 43: "cabinet.backbox", 81: "cabinet.backbox", 82: "cabinet.backbox"}
SWITCH_LOCATIONS_TEXT = {13: "cabinet front", 14: "cabinet interior", 21: "coin door", 22: "coin door", 43: "backbox token mechanism", 81: "backbox token mechanism", 82: "backbox token mechanism"}
UNUSED_MATRIX_ADDRESSES = frozenset({23, 38, 87, 88})
# PinMAME's scGameData invSw {0x00,0x00,0x00,0x7f,0x06,0xe0,0x3f,0x3f,0x00,...} inverts these public addresses through wpc_sw2m
# (core_setSw indexes invSw by wpc_sw2m(no)/8); the test recomputes the set from the mask.
MASKED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 42, 43, 56, 57, 58, 61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76})
# Cells the matrix page shades "Opto, Typically Closed" (switch-matrix.md).
SHADED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 56, 57, 58, 61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76, 85, 86, 112, 114, 116, 118})
OPTO_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 56, 57, 58, 61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76, 85, 86})
# The 10-opto board (A-18159) positions the Section 3 pages tie to switch numbers.
TEN_OPTO_POSITIONS = {31: 1, 32: 2, 33: 3, 34: 4, 35: 5, 36: 6, 37: 7, 41: 8, 42: 9, 43: 10}
# The ROM's own T.1 names (switch-edges sweep).
ROM_SWITCH_NAMES = {
	11: "TP TROUGH (ROOF)", 12: "TP TROUGH (MOVE)", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "RIGHT ORBIT", 16: "LEFT OUTLANE",
	17: "RIGHT OUTLANE", 18: "BALLSHOOTER", 21: "SLAM TILT", 22: "COIN DOOR CLOSED", 24: "ALWAYS CLOSED", 25: "UR FLIP ROLLOVER",
	26: "LEFT RETURN", 27: "RIGHT RETURN", 28: "LEFT ORBIT", 31: "TROUGH EJECT *", 32: "TROUGH BALL 1 *", 33: "TROUGH BALL 2 *",
	34: "TROUGH BALL 3 *", 35: "TROUGH BALL 4 *", 36: "LOCKUP 1 FRONT *", 37: "LOCKUP 2 REAR *", 41: "KICKBACK *", 42: "LEFT BIG KICK *",
	43: "TOKN CHUTE EXIT*", 44: "LEFT JET", 45: "RIGHT JET", 46: "TOP JET", 47: "LEFT SLINGSHOT", 48: "RIGHT SLINGSHOT",
	51: "(A)LARM STANDUP", 52: "A(L)ARM STANDUP", 53: "AL(A)RM STANDUP", 54: "ALA(R)M STANDUP", 55: "ALAR(M) STANDUP",
	56: "MOVNG TARGET C", 57: "MOVNG TARGET B", 58: "MOVNG TARGET A", 61: "TL 3BANK TOP", 62: "TL 3BANK MIDDLE", 63: "TL 3BANK BOTTOM",
	64: "TR 3BANK BOTTOM", 65: "TR 3BANK MIDDLE", 66: "TR 3BANK TOP", 67: "TOP LEFT LANE", 68: "TOP POPPER", 71: "BL 3BANK TOP",
	72: "BL 3BANK MIDDLE", 73: "BL 3BANK BOTTOM", 74: "BR 3BANK BOTTOM", 75: "BR 3BANK MIDDLE", 76: "BR 3BANK TOP", 77: "BANK KICKOUT",
	78: "TOP RIGHT LANE", 81: "LEFT TOKEN LVL.", 82: "RIGHT TOKEN LVL.", 83: "RAMP ENTRANCE", 84: "RAMP MADE", 85: "WHEEL CHANNEL A",
	86: "WHEEL CHANNEL B",
}
# Switches whose closure makes the ROM fire their own coil even inside T.1 (switch-edges sweep).
SWITCH_FIRES = {44: 12, 45: 13, 46: 14, 47: 10, 48: 11}
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"), 3: ("Green-Orange", "J206-3", "U20-16"),
	4: ("Green-Yellow", "J206-4", "U20-15"), 5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
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
# Fliptronic column (switch-matrix.md; section-3-boards.md; cpu-board.md):
# public -> (label, printed position, wire, connector, comparator pin, type, role or None, availability).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J208-13", "U26A-1", "leaf", "internal.flipper.lower.right.eos", "used"),
	112: ("Right Flipper Button Lower Opto", "F2", "Blue-Violet", "J212-12", "U25A-1", "opto", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J208-12", "U26B-2", "leaf", "internal.flipper.lower.left.eos", "used"),
	114: ("Left Flipper Button Opto", "F4", "Blue-Gray", "J212-11", "U25B-2", "opto", "flipper.lower.left.button", "used"),
	115: ("Upper Right Flipper EOS", "F5", "Black-Violet", "J208-11", "U26C-14", "leaf", "internal.flipper.upper.right.eos", "used"),
	116: ("Right Flipper Button Upper Opto", "F6", "Black-Yellow", "J212-10", "U25C-14", "opto", "flipper.upper.right.button", "used"),
	117: ("Not Used Fliptronic Position F7", "F7", "Black-Gray", "J208-10", "U26D-13", "leaf", None, "unused"),
	118: ("Token Coin Slot", "F8", "Black-Blue", "J212-9", "U25D-13", "other", "cabinet.coin.token", "used"),
}
FLIPPER_ROM_TEXT = {111: None, 112: ("R FLIPPER EOS", "F1 BLK-GRN ORN"), 113: None, 114: ("L FLIPPER EOS", "F3 BLK-BLU ORN"), 115: None, 116: ("UR FLIPPER EOS", "F5 BLK-VIO ORN"), 117: None, 118: ("TOKEN COIN SLOT", "F8 BLK-BLU ORN")}


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
		raise RuntimeError(f"Safe Cracker retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Safe Cracker extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Safe Cracker retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Safe Cracker retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Safe Cracker retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
	location drawings confirm.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": entry["x"],
				"y": entry["y"],
				"provenance": provenance("observed", VPX_TABLE_SOURCE),
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


# What the retained known-working v1.0 script does for each matrix switch (vpx-analysis script facts).
SWITCH_SCRIPT = {
	11: "RoofTrigger_Hit pulses it (vpmTimer.PulseSw 11), a hidden subway trigger at the roof entrance",
	12: "variTrigger_Hit pulses it, a hidden subway trigger behind the moving target",
	14: "vpmNudge.TiltSwitch = 14", 15: "sw15_Hit pulses it", 16: "sw16_Hit pulses it", 17: "sw17_Hit pulses it",
	18: "sw18_hit sets it and sw18_unhit clears it while the ball sits in the shooter lane", 25: "sw25_Hit pulses it",
	26: "sw26_Hit pulses it", 27: "sw27_Hit pulses it", 28: "sw28_Hit pulses it",
	31: "ReleaseBall (solenoid 9) kicks the ball out of trough slot sw32 and pulses 31",
	32: "Table1_Init sets it to 1 with a ball in kicker sw32; sw32_Hit sets it and sw32_UnHit clears it",
	33: "Table1_Init sets it to 1 with a ball in kicker sw33; sw33_Hit sets it and sw33_UnHit clears it",
	34: "Table1_Init sets it to 1 with a ball in kicker sw34; sw34_Hit sets it and sw34_UnHit clears it",
	35: "Table1_Init sets it to 1 with a ball in kicker sw35; sw35_Hit (the drain) sets it and sw35_UnHit clears it",
	36: "lockTrigger_Hit sets it for the first locked ball; the lock pin's release clears it",
	37: "lockTrigger_Hit sets it for the second locked ball; the lock pin's release clears it",
	41: "Table1_Init sets it to 1 ('switch mapped backwards'); sw41_Hit writes 0 and sw41_Unhit writes 1",
	42: "VariTargetTimer_Timer sets it while a ball lies in the left kickback rectangle around the LeftKickBack kicker and clears it otherwise",
	43: "SolTokenRelease pulses it whenever solenoid 2 or 4 turns on (with a token animation; no table object)",
	44: "Bumper1_Hit pulses it", 45: "Bumper3_Hit pulses it", 46: "Bumper2_Hit pulses it",
	47: "LeftSlingShot_Slingshot pulses it", 48: "RightSlingShot_Slingshot pulses it",
	51: "the t51 target pulses it", 52: "the t52 target pulses it", 53: "the t53 target pulses it", 54: "the t54 target pulses it", 55: "the t55 target pulses it",
	67: "sw67_Hit pulses it", 68: "sw68_Hit sets it when the ball enters the top popper; the popper coils' handlers clear it",
	77: "sw77_Hit sets it; the bank kick (solenoid 5) clears it",
	78: "sw78_Hit pulses it", 81: "SolTokenRelease from solenoid 4 holds it at the solenoid's level (no table object)",
	82: "SolTokenRelease from solenoid 2 holds it at the solenoid's level (no table object)",
	83: "sw83_Hit sets it and sw83_Unhit clears it", 84: "sw84_Hit sets it and sw84_Unhit clears it",
	85: "SpinDiscSwitches_Timer writes it from the spin disc's rotation (quadrature with 86, one switch per 3.75 degrees)",
	86: "SpinDiscSwitches_Timer writes it from the spin disc's rotation (quadrature with 85)",
}
for _address in (56, 57, 58):
	SWITCH_SCRIPT[_address] = "VariTargetTimer_Timer computes 56/57/58 from the moving target's travel (pVari.TransY) with its own code table"
for _address, _bank in ((61, "SolUpperLeftTargetsUp"), (62, "SolUpperLeftTargetsUp"), (63, "SolUpperLeftTargetsUp"), (64, "SolUpperRightTargetsUp"), (65, "SolUpperRightTargetsUp"), (66, "SolUpperRightTargetsUp"), (71, "SolLowerLeftTargetsUp"), (72, "SolLowerLeftTargetsUp"), (73, "SolLowerLeftTargetsUp"), (74, "SolLowerRightTargetsUp"), (75, "SolLowerRightTargetsUp"), (76, "SolLowerRightTargetsUp")):
	SWITCH_SCRIPT[_address] = f"t{_address}_dropped sets it to 1 and {_bank} clears it when the bank resets"


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += (
			" The Switch Matrix prints NOT USED in this cell"
			+ (" and the Switch Locations list prints 'Not Used'." if address in (23, 38) else "; the Switch Locations list ends at 86.")
			+ " The ROM still scans the position: in its T.1 SWITCH EDGES sweep a host write of 1 drew the name 'UNUSED', and 0 cleared it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, EDGES_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE), **extra,
		)
	part, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if " / " in part:
		physical["assembly_part_number"] = part
	else:
		physical["part_number"] = part
	notes += f" Switch Locations description \"{description}\"."
	if description.startswith("*"):
		notes += " The list's '*' footnote reads 'Not Shown': the location drawing carries no balloon for it."
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address == 24:
		notes += (
			" PinMAME holds public 24 at 1 from power-up. In T.1 SWITCH EDGES the redundant write of 1 drew nothing new and the 1 -> 0 "
			"edge drew 'ALWAYS CLOSED / T.1 LAST SW 24', so the ROM reports this position when it opens."
		)
	elif address == 43:
		notes += (
			" T.1 SWITCH EDGES draws nothing new when the host sets public 43 to 1 and names it 'TOKN CHUTE EXIT*' on the 1 -> 0 edge, "
			"where every other masked opto is named at 1: PinMAME's scGameData mask inverts 43, so public 0 is a closed matrix contact, "
			"and the ROM treats the closed contact as active. Under the platform rule (a masked switch the ROM treats as active at public 0 "
			"has a contact that is closed when active) normally_closed is false. Read physically, the 10-opto board's optos rest closed "
			"with the beam clear (the matrix shades them 'Opto, Typically Closed'), so the ROM's active state here is the clear chute and "
			"a token breaking the beam drops the ROM's reading: the retained scripts leave public 43 at 0 and pulse it to 1 as a token is "
			"dispensed, which is that event. A recreation leaves 43 at 0 and writes 1 while a token passes."
		)
	else:
		notes += f" The ROM names it \"{ROM_SWITCH_NAMES[address]}\" in T.1 SWITCH EDGES while the host holds public {address} at 1, and clears the name at 0."
	if address in SWITCH_FIRES:
		notes += f" Closing it made the ROM fire its own coil, public solenoid {SWITCH_FIRES[address]}, even inside T.1."
	if address in MASKED_SWITCHES and address != 43:
		notes += (
			" PinMAME's scGameData inverted-switch mask inverts this address, so public 1 is an open matrix contact; the ROM reads the "
			"switch as active at public 1, so its matrix contact rests closed and normally_closed is true. The matrix page shades the cell "
			"'Opto, Typically Closed'."
		)
	elif address in OPTO_SWITCHES and address != 43:
		notes += (
			" The matrix page shades the cell 'Opto, Typically Closed', but PinMAME's mask does not invert it and the ROM names it at "
			"public 1, an unmasked closed contact, so under the platform rule the matrix contact rests open and normally_closed is false. "
			"The printed legend marks opto construction, not the rest state the ROM reads."
		)
	if address in TEN_OPTO_POSITIONS:
		notes += f" It is opto {TEN_OPTO_POSITIONS[address]} of the 10 Opto P.C.B. A-18159 (Section 3 pin lists 3-18, 3-19)"
		if address <= 35:
			board = {31: "JAM BALL", 32: "BALL 1", 33: "BALL 2", 34: "BALL 3", 35: "BALL 4"}[address]
			notes += f", read through the trough's IR LED board A-18617-1 and photo-transistor board A-18618-1 position {board}."
		else:
			notes += ", with an LED Board A-16908 transmitter and a Photo Transistor Board A-16909 receiver."
	if address in {31, 32, 33, 34, 35}:
		if address == 31:
			notes += " It sees the ball at the trough's eject position, over the trough eject coil (solenoid 9)."
		else:
			notes += f" It reports the trough holding at least {address - 31} ball{'s' if address > 32 else ''} (Safe Cracker is a four-ball game)."
	if address == 41:
		notes += (
			" The ROM names it 'KICKBACK *' at public 1 (unmasked, so a closed matrix contact), and both retained scripts hold public 41 at 1 "
			"while no ball is in the right ramp kickback lane and write 0 while the ball passes ('switch mapped backwards'). The two agree "
			"if this opto, like the other nine on its board, rests closed with the beam clear: the ROM's active state is then the clear "
			"lane, and initial_active records that rest state. Under the platform rule (the ROM's active level on an unmasked contact) "
			"normally_closed is false. A gameplay probe that presented each edge with a ball in play drew no kickback coil either way "
			"(review-artifacts safe-cracker-1996/harness/kickback-probe, inconclusive), so the coil's trigger edge is not settled here."
		)
		extra["initial_active"] = True
	if address == 42:
		notes += " The left big kick opto at the left kickback, whose coil is BIG KICK (solenoid 1); the retained script arms the LeftKickBack kicker from solenoid 1 and derives 42 from the ball lying in front of it."
	if address in {56, 57, 58}:
		letter = {56: "C", 57: "B", 58: "A"}[address]
		notes += (
			f" Opto {letter} of the 3 Opto Vari Target P.C.B. A-20906 on the moving target (Vari-Target Assembly A-20851). The ROM's "
			f"T.16 MOVING TARGET TEST shows SWITCH \"{letter}\" (#{address}) CLOSED while the host holds it at 0 and OPEN at 1. The Section 3 "
			"reprint of the matrix (3-2) labels 56-58 VARI TARGET A, B, C, reversed; the primary matrix, the Switch Locations list and the "
			"ROM (T.1 and T.16) all give 56 = C and 58 = A. The board's pin list (3-20) prints its common line as Green-Blue from J206-6 "
			"(column 6) where the matrix wires column 5 (Green-Black, J206-5); the ROM's own T.1 and T.16 place the three at 56-58, so the "
			"wiring record follows the matrix."
		)
		board_opto, pin = {56: (1, "J1-5 White-Blue from J208-7"), 57: (2, "J1-6 White-Violet from J208-8"), 58: (3, "J1-7 White-Gray from J208-9")}[address]
		notes += f" The board's schematic and pin list run OPTO{board_opto}'s collector to {pin}, the matrix's row {address % 10}."
		if address == 58:
			notes += (
				" This is the Opto 3 of the manual's Adjust Moving Target Assembly procedure (1-52, 1-53): its beam is clear with the target "
				"rear-most and completely broken with the target forward-most, at home, so a recreation holds public 58 at 1 (OPEN) while "
				"the target is home."
			)
		refs += (MOVING_TARGET_SOURCE, MOVING_TARGET_CODES_SOURCE)
	if address in {61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76}:
		bank = {6: ("top", 15 if address <= 63 else 16), 7: ("bottom", 27 if address <= 73 else 28)}[column]
		side = "left" if address in (61, 62, 63, 71, 72, 73) else "right"
		notes += (
			f" A target of the {bank[0]} {side} 3-bank drop target set (switch assembly A-13609), reset by solenoid {bank[1]}. The ROM's T.19 "
			"DROP TARGET TEST marks it while the host holds it at 1, i.e. while the target is down."
		)
	if address in {85, 86}:
		notes += (
			" One of the two optos of the Spin Disc Opto P.C.B. A-20952 under the spinning disc (Spin Target Assembly A-20911) that the "
			"manual's rules call the wheel: the two channels read the disc's rotation in quadrature (both retained scripts write 85/86 as "
			"a two-bit Gray sequence from the disc angle). The Section 3 circuit boxes print 'Sw #85' (White-Green) with 'Sw #86' "
			"(White-Blue) on 3-20 and 'Sw #57' (White-Violet) on 3-23, whose own pin list prints White-Blue from J208-7; the matrix and "
			"the ROM place the channels at 85 and 86."
		)
	if address in {36, 37}:
		notes += " A lock-up opto of the Multi-Ball Assembly A-20935 on the ramp; the lock-up release coil (solenoid 36) lets the locked balls go."
	if address in {11, 12, 77}:
		notes += {
			11: " The ROM's T.20 TOP TROUGH TEST shows it as TR1-11, the first switch of the underground (top) trough that a ball dropping through the roof entrance reaches.",
			12: " The ROM's T.20 TOP TROUGH TEST shows it as TR2-12, the underground trough switch a ball reaches through the moving target's opening when the target is pushed fully back.",
			77: " The ROM's T.20 TOP TROUGH TEST shows it as TR3-77, the end of the underground trough at the bank: while the host held 77 at 1 the ROM showed KICKING BALL FROM EJECT and pulsed the bank kick coil (solenoid 5).",
		}[address]
	if address == 68:
		notes += " The ROM's T.20 TOP TROUGH TEST shows it as TOP BALL POPPER-68: while the host held it at 1 the ROM showed KICKING BALL FROM POPPER and pulsed the top popper up coil (solenoid 6)."
	if address in {81, 82}:
		side = "left" if address == 81 else "right"
		notes += (
			f" A level switch (20-10301) of the {side} token tube in the backbox token mechanism, not shown on the playfield drawing. The "
			f"retained script ties it to the {'left' if address == 81 else 'right'} token tube coil (solenoid {4 if address == 81 else 2}) and "
			"the Section 3 lists carry no further detail of its level sense."
		)
	if address == 43:
		notes += " The token chute opto (LED Board A-16908, Photo Transistor Board A-16909) on the chute the backbox token tubes dispense into; the manual's list prints it '*Token Chute Jam', not shown on the playfield drawing, and the ROM calls it TOKN CHUTE EXIT."
	if address in {47, 48}:
		notes += " The slingshot kick switch SW-1A-114 and the score switch SW-1A-120 share this address."
	if address in {51, 52, 53, 54, 55}:
		notes += " One of the five ALARM standup targets; making them spells ALARM (lamps 35, 37, 46, 47, 48 light the letters)."
	if address == 18:
		notes += " The shooter-lane switch: the ball rests on it before the plunger or the auto plunger (solenoid 35) launches it."
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = SWITCH_LOCATIONS_TEXT[address]
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
		extra["normally_closed"] = address in MASKED_SWITCHES and address != 43
	if address == 22:
		extra["initial_active"] = True
		notes += " It is closed while the coin door is closed; the service buttons need the door open."
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		if address == 4:
			note += " The Dedicated Switches drawing (3-3) runs the D4 line to the coin door connector with no pin number and no switch symbol."
		if address == 5:
			note += " The matrix prints 'Ser Credits'; the Dedicated Switches drawing spells it 'Service Credits'."
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", refs,
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note} The dedicated switches reach the CPU through the Coin Door Interface Board A-20949."},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, component, switch_type, role, availability) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": f"comparator {component}"},
		}
		if role:
			extra["roles"] = [role]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		physical: dict[str, Any] = {"switch_type": switch_type}
		if address in {111, 113, 115}:
			physical["part_number"] = "SW-1A-194"
			physical["location"] = "flipper assembly"
			flipper = {111: ("lower right", "A-14876-R-6"), 113: ("lower left", "A-15849-L-7"), 115: ("upper right", "A-15849-R-1")}[address]
			notes += (
				f" End-of-stroke switch SW-1A-194 on the {flipper[0]} flipper assembly ({flipper[1]}). scGameData declares "
				"FLIP_SOL(FLIP_L | FLIP_UR), so PinMAME rewrites this bit from the flipper coil state on every update: in the T.1 sweep a host "
				"write of 1 read back 0 and drew no name. Its public level is not a measurement of the contact; normally_closed records the "
				"grounded switch's open rest state."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address in {112, 114, 116}:
			side = "right" if address in {112, 116} else "left"
			board_pin = "J1-1" if address == 116 else "J1-2"
			physical["location"] = "cabinet flipper button"
			physical["assembly_part_number"] = "A-17316"
			rom_name, rom_text = FLIPPER_ROM_TEXT[address]
			notes += (
				f" An opto of the {side} Flipper Opto Board A-17316 at the {side} cabinet button ({board_pin}); WPC-95 reads the flipper "
				"column complemented (WPC_FLIPPERSW95 returns ~swMatrix), so public 1 is the pressed button and the contact the matrix sees "
				"is open at rest: normally_closed is false. The matrix page shades the cell as an opto and the Switch Locations list calls "
				f"it '*... Flipper Cabinet'. In the T.1 sweep a host write of 1 named '{rom_name}' ({rom_text})"
			)
			if address == 112:
				notes += " and fired the lower right flipper (public 45 and 46)."
			elif address == 114:
				notes += " and fired the lower left flipper (public 47 and 48)."
			else:
				notes += (
					" and fired both the upper right flipper (public 33 and 34) and the lower right flipper (45 and 46). The right button's "
					"board carries both optos (F2 on J1-2, F6 on J1-1), so one press interrupts 112 and 116 together and a consumer writes "
					"both from the right flipper button. The retained VPinMAME library writes 116 only for its staged right flipper key."
				)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 117:
			notes += (
				" The matrix prints F7 'Upper Left Flipper EOS', but the Switch Locations list prints F7 Not Used, the CPU board list prints "
				"J208-10 Not Used, Safe Cracker has no upper left flipper, and in the T.1 sweep a host write of 1 round-tripped and drew no name."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			physical["location"] = "coin door"
			notes += (
				" The matrix prints F8 'Upper Left Flipper Opto' and the Switch Locations list prints F8 Not Used, but this game's CPU board "
				"list wires J212-9 (Black-Blue, F8) to the Coin Door Interface Board J13-2, the Left Flipper Opto Board's own pin list prints "
				"its J1-1 Not Used, and the ROM consumes the position: in the T.1 sweep a host write of 1 at public 118 named 'TOKEN COIN SLOT' "
				"(F8 BLK-BLU ORN) and 0 cleared it. A wiring page and the ROM rebut the 'Not Used' row, so the position is recorded as the "
				"token slot switch: a magic token inserted at the coin door closes it (the rules' hint: 'Replay MAGIC TOKENS for surprising "
				"results!'). WPC-95's complemented flipper-column read makes public 1 the closed contact, so normally_closed is false. Both "
				"retained scripts pulse 118 when a token is dispensed or added with a test key."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			refs += (VPX_SCRIPT_SOURCE,)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, availability, refs, **extra))
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country configuration bit)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC-95 CPU board", "switch_type": "dip",
					"notes": "WPC-95 CPU-board country DIP bank; the manual's Dip Switch Chart sets the country (America, European, French, German, Spain). No ON/OFF combination is asserted here; the ROM's T.15 DIPSW. TEST shows the positions.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Solenoid data (solenoid-flasher-table.md, solenoid-flasher-locations.md, power-driver-board.md) ------
SOLENOID_LABELS = {
	1: "Big Kick", 2: "Right Token Tube", 3: "Vari Target Reset", 4: "Left Token Tube", 5: "Bank Kick", 6: "Top Popper Up",
	7: "Ramp Diverter", 8: "Kickback (Ramp)", 9: "Trough Eject", 10: "Left Slingshot", 11: "Right Slingshot", 12: "Left Jet",
	13: "Right Jet", 14: "Top Jet", 15: "Top Left 3-Bank Reset", 16: "Top Right 3-Bank Reset", 17: "Back Left Flasher",
	18: "Jets & Back Right Flashers", 19: "Right Middle Flasher", 20: "Right Bottom Flasher", 21: "Left Middle Flasher",
	22: "Left Bottom Flasher", 23: "Light Rope 1", 24: "Light Rope 2", 25: "Top Popper Eject", 26: "Top Light & Motor",
	27: "Bottom Left 3-Bank Reset", 28: "Bottom Right 3-Bank Reset", 33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Auto Plunger", 36: "Lock Up Release", 37: "Aux. Lamp Enable", 38: "Aux. Lamp Clock", 39: "Aux. Lamp Data 1",
	40: "Aux. Lamp Data 2", 45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power",
	48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B", 31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32", 41: "Aux. Lamp Enable LPDC Mirror", 42: "Aux. Lamp Clock LPDC Mirror",
	43: "Aux. Lamp Data 1 LPDC Mirror", 44: "Aux. Lamp Data 2 LPDC Mirror", 49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# address -> printed (type, voltage connection, transistor, drive connection, wire, part or flashlamp), Solenoid/Flasher Table (2-44).
SOLENOID_TABLE = {
	1: ("High Power", "J133-2", "Q72", "J116-1", "Vio-Brn", "AE-24-900"), 2: ("High Power", "J135-2 (backbox)", "Q68", "J118-2 (backbox)", "Vio-Red", "04-10424"),
	3: ("High Power", "J133-2", "Q71", "J116-4", "Vio-Org", "SM1-26-600"), 4: ("High Power", "J135-2 (backbox)", "Q67", "J118-5 (backbox)", "Vio-Yel", "04-10424"),
	5: ("High Power", "J133-2", "Q70", "J116-6", "Vio-Grn", "AE-23-800"), 6: ("High Power", "J133-2", "Q66", "J116-7", "Vio-Blu", "AE-24-900"),
	7: ("High Power", "J133-2", "Q69", "J116-8", "Vio-Blk", "AE-26-1500"), 8: ("High Power", "J133-2", "Q65", "J116-9", "Vio-Gry", "AE-23-800"),
	9: ("Low Power", "J133-3", "Q44", "J113-1", "Brn-Blk", "AE-26-1500"), 10: ("Low Power", "J133-3", "Q48", "J113-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J133-3", "Q43", "J113-4", "Brn-Org", "AE-26-1200"), 12: ("Low Power", "J133-3", "Q47", "J113-5", "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J133-3", "Q42", "J113-6", "Brn-Grn", "AE-26-1200"), 14: ("Low Power", "J133-3", "Q46", "J113-7", "Brn-Blu", "AE-26-1200"),
	15: ("Low Power", "J133-3", "Q41", "J113-8", "Brn-Vio", "AE-26-1200"), 16: ("Low Power", "J133-3", "Q45", "J113-9", "Brn-Gry", "AE-26-1200"),
	17: ("Flasher", "J133-6", "Q28", "J111-1", "Blk-Brn", "#906"), 18: ("Flasher", "J133-6", "Q32", "J111-2", "Blk-Red", "#89, #906"),
	19: ("Flasher", "J133-6", "Q27", "J111-3", "Blk-Org", "#906"), 20: ("Flasher", "J133-6", "Q31", "J111-4", "Blk-Yel", "#906"),
	21: ("Flasher", "J133-6", "Q26", "J111-5", "Blu-Brn", "#906"), 22: ("Flasher", "J133-6", "Q30", "J111-6", "Blu-Red", "#906"),
	23: ("Flasher", "J134-5 (backbox)", "Q25", "J112-8 (backbox)", "Blu-Org", "04-10440"), 24: ("Flasher", "J134-5 (backbox)", "Q29", "J112-9 (backbox)", "Blu-Yel", "04-10440"),
	25: ("Gen. Purpose", "J133-1", "Q16", "J109-1", "Blu-Grn", "AE-27-1200"), 26: ("Gen. Purpose", "J140-2 (backbox)", "Q15", "J109-2 (backbox)", "Blu-Blk", "20-10307"),
	27: ("Gen. Purpose", "J133-1", "Q14", "J109-3", "Blu-Vio", "AE-26-1200"), 28: ("Gen. Purpose", "J133-1", "Q13", "J109-4", "Blu-Gry", "AE-26-1200"),
	35: ("High Power", "J119-8,9", "Q81", "J120-3", "Yel-Gry", "AE-23-800"), 36: ("Low Power", "J119-8,9", "Q83", "J120-1", "Org-Gry", "AE-26-1200"),
	37: ("L.P.D.C.", "J138-2 (backbox)", None, "J110-1 (backbox)", "Brn-Wht", "A-20909"), 38: ("L.P.D.C.", "J138-2 (backbox)", None, "J110-3 (backbox)", "Org-Wht", "A-20909"),
	39: ("L.P.D.C.", "J138-2 (backbox)", None, "J110-4 (backbox)", "Yel-Wht", "A-20909"), 40: ("L.P.D.C.", "J138-2 (backbox)", None, "J110-5 (backbox)", "Grn-Wht", "A-20909"),
}
# Locations-list assembly for each coil/flasher (solenoid-flasher-locations.md, 2-44 and 2-45).
SOLENOID_ASSEMBLIES = {
	1: "A-21034", 2: "A-20925", 3: "A-20916", 4: "A-20925", 5: "A-20923", 6: "A-20919", 7: "A-20882", 8: "A-20959", 9: "A-19963-3",
	10: "B-9362-L-2", 11: "B-9362-R-3", 12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2", 15: "A-20892", 16: "A-20895", 17: "A-20958",
	18: "A-20944", 19: "A-20944", 20: "A-20944", 21: "A-20958", 22: "A-20958", 23: "90003-BB", 24: "90003-BB", 25: "A-20920",
	26: "90003-BB", 27: "A-20896", 28: "A-20892", 33: "A-15849-R-1", 34: "A-15849-R-1", 35: "A-21022", 36: "A-20935", 37: "A-20909",
	38: "A-20909", 39: "A-20909", 40: "A-20909", 45: "A-14876-R-6", 46: "A-14876-R-6", 47: "A-15849-L-7", 48: "A-15849-L-7",
}
FLASHER_SOLENOIDS = frozenset({17, 18, 19, 20, 21, 22, 23, 24})
BACKBOX_SOLENOIDS = frozenset({2, 4, 23, 24, 26})
# The ROM's own T.4 and T.5 names and wires (solenoid-test and flasher-test runs).
ROM_SOLENOID_NAMES = {
	1: ("BIG KICK", "VIO-BRN RED-BRN"), 2: ("RIGHT TOKEN TUBE", "VIO-RED RED-BRN"), 3: ("MOVE TGT. RESET", "VIO-ORN RED-BRN"),
	4: ("LEFT TOKEN TUBE", "VIO-YEL RED-BRN"), 5: ("BANK KICK", "VIO-GRN RED-BRN"), 6: ("TOP POPPER UP", "VIO-BLU RED-BRN"),
	7: ("RAMP DIVERTOR", "VIO-BLK RED-BRN"), 8: ("KICKBACK (RAMP)", "VIO-GRY RED-BRN"), 9: ("TROUGH EJECT", "BRN-BLK RED-BLK"),
	10: ("LEFT SLINGSHOT", "BRN-RED RED-BLK"), 11: ("RIGHT SLINGSHOT", "BRN-ORN RED-BLK"), 12: ("LEFT JET", "BRN-YEL RED-BLK"),
	13: ("RIGHT JET", "BRN-GRN RED-BLK"), 14: ("TOP JET", "BRN-BLU RED-BLK"), 15: ("TOP. L. 3 BANK", "BRN-VIO RED-BLK"),
	16: ("TOP. R. 3 BANK", "BRN-GRY RED-BLK"), 17: ("BACK LEFT", "BLK-BRN RED-WHT"), 18: ("JETS + BK RT. (2)", "BLK-RED RED-WHT"),
	19: ("RIGHT MIDDLE", "BLK-ORN RED-WHT"), 20: ("RIGHT BOTTOM", "BLK-YEL RED-WHT"), 21: ("LEFT MIDDLE", "BLU-GRN RED-WHT"),
	22: ("LEFT BOTTOM", "BLU-BLK RED-WHT"), 23: ("LIGHT ROPE 1", "BLU-VIO RED-WHT"), 24: ("LIGHT ROPE 2", "BLU-GRY RED-WHT"),
	25: ("TOP POPPER EJECT", "BLU-BRN RED-ORN"), 26: ("TOP LIGHT+MOTOR", "BLU-RED RED-ORN"), 27: ("BOT. L. 3 BANK", "BLU-ORN RED-ORN"),
	28: ("BOT. R. 3 BANK", "BLU-YEL RED-ORN"), 33: ("U.R. FLIP. POWER", "YEL-VIO RED-VIO"), 34: ("U.R. FLIP. HOLD", "ORN-VIO RED-VIO"),
	35: ("AUTO PLUNGER", "YEL-GRY RED-GRY"), 36: ("LOCKUP RELEASE", "ORN-GRY RED-GRY"), 45: ("R. FLIP. POWER", "YEL-GRN RED-GRN"),
	46: ("R. FLIP. HOLD", "ORN-GRN RED-GRN"), 47: ("L. FLIP. POWER", "YEL-BLU RED-BLU"), 48: ("L. FLIP. HOLD", "ORN-BLU RED-BLU"),
}
T5_ADDRESSES = frozenset({17, 18, 19, 20, 21, 22, 23, 24})
T12_ADDRESSES = frozenset({33, 34, 45, 46, 47, 48})
# The retained v1.0 script's handling of each solenoid (vpx-analysis script facts).
SOLENOID_SCRIPT = {
	1: "SolCallBack(1) = \"SolLeftKickBack\" arms the hidden LeftKickBack kicker, which kicks the next ball that enters it",
	2: "SolCallBack(2) = \"SolTokenRelease \"\"L\"\", 82, \" holds switch 82 at the solenoid's level and pulses 43 and 118 with a token animation",
	3: "SolCallback(3) = \"SolResetVariTarget\" drives the moving target (pVari) back home",
	4: "SolCallBack(4) = \"SolTokenRelease \"\"R\"\", 81, \" holds switch 81 at the solenoid's level and pulses 43 and 118 with a token animation",
	5: "SolCallback(5) = \"SolBankKick\" kicks the ball out of the bank kickout kicker sw77",
	6: "SolCallback(6) = \"SolPopperKickUp\" lifts the ball out of the top popper sw68 and drops it onto the habitrail",
	7: "SolCallback(7) = \"SolRampDiverter\" rotates the diverter (pDiverter) and drops diverterWall",
	8: "SolCallBack(8) = \"SolRightKickBack\" arms the hidden RightKickBack kicker",
	9: "SolCallback(9) = \"ReleaseBall\" kicks the ball out of trough slot sw32 and pulses switch 31",
	15: "SolCallback(15) = \"SolUpperLeftTargetsUp\" raises targets t61-t63 and clears 61-63",
	16: "SolCallback(16) = \"SolUpperRightTargetsUp\" raises targets t64-t66 and clears 64-66",
	23: "SolCallback(23) = \"SolFlasherStripSeq1\" toggles the backglass strip sprites", 24: "SolCallback(24) = \"SolFlasherStripSeq2\" toggles the backglass strip sprites",
	25: "SolCallback(25) = \"SolPopperEject\" kicks the ball out of the top popper sw68 onto the playfield",
	27: "SolCallback(27) = \"SolLowerLeftTargetsUp\" raises targets t71-t73 and clears 71-73",
	28: "SolCallback(28) = \"SolLowerRightTargetsUp\" raises targets t74-t76 and clears 74-76",
	35: "SolCallback(35) = \"SolPlunger\" fires the AutoPlunger", 36: "SolCallback(36) = \"SolLockupRelease\" drops lockPinWall and rotates the lock pin, clearing 36 and 37",
	46: "SolCallback(sLRFlipper) = \"SolRFlipper\" (sLRFlipper = 46) rotates RightFlipper and RightUpperFlipper together",
	48: "SolCallback(sLLFlipper) = \"SolLFlipper\" (sLLFlipper = 48)",
}
for _address in (17, 18, 19, 20, 21, 22):
	SOLENOID_SCRIPT[_address] = f"SolModCallBack({_address}) = \"Flasherset{_address}\" lights Flupper dome {_address}" + (" and the light lF18 among the jet bumpers" if _address == 18 else "")
SOLENOID_SCRIPT.update({address: "no callback; the table fires the coil from the switch's physics event" for address in (10, 11, 12, 13, 14)})
FLIPPER_COILS = {
	45: ("power", "29", "Lwr. Rt. Power", "J119-1 (Red-Grn)", "Q90", "J120-13", "Yel-Grn", "FL-20867", "WHITE"),
	46: ("hold", "30", "Lwr. Rt. Hold", "J119-1 (Red-Grn)", "Q92", "J120-11", "Org-Grn", "FL-20867", "WHITE"),
	47: ("power", "31", "Lwr. Lt. Power", "J119-4 (Red-Blu)", "Q87", "J120-9", "Yel-Blu", "FL-20867", "WHITE"),
	48: ("hold", "32", "Lwr. Lt. Hold", "J119-4 (Red-Blu)", "Q89", "J120-7", "Org-Blu", "FL-20867", "WHITE"),
	33: ("power", "33", "Upr. Rt. Power", "J119-6 (Red-Vio)", "Q84", "J120-6", "Yel-Vio", "FL-11753", "YELLOW"),
	34: ("hold", "34", "Upr. Rt. Hold", "J119-6 (Red-Vio)", "Q86", "J120-4", "Org-Vio", "FL-11753", "YELLOW"),
}
SOLENOID_NOTES = {
	1: "The BIG KICK coil (AE-24-900, assembly A-21034) of the left kickback beside the left big kick opto (switch 42), which kicks a ball back up the left side.",
	2: "The right token tube's coil (04-10424, Token tube assembly A-20925) in the backbox token mechanism: it releases a token from the right tube, whose level switch is 82. The ROM's T.17 TOKEN TEST pulses it with 4 for every dispense. Service Bulletin 90 replaces the stop brackets (04-10506) of both token-tube shuttle plungers on games built between 5/2/96 and 5/20/96 that dispensed intermittently.",
	3: "The moving (vari) target's reset coil (SM1-26-600, A-20916): its armature bracket engages the pivot arm's teeth and holds the target back, and the manual's adjustment procedure (1-53) frees the target to snap to its forward-most, home position by dislodging that bracket from the teeth. The ROM's T.16 MOVING TARGET TEST pulses it on Enter ('RESETTING MOVING TARGET').",
	4: "The left token tube's coil (04-10424, A-20925) in the backbox token mechanism, whose level switch is 81. The ROM's T.17 TOKEN TEST pulses it with 2 for every dispense; Service Bulletin 90 applies to it as to 2.",
	5: "The BANK KICK coil (AE-23-800) of the Center Loop Kick-Back Assembly A-20923 under the bank kickout (switch 77, TR3 of the underground trough): it kicks the ball out of the bank. The ROM's T.20 TOP TROUGH TEST pulses it while 77 is held ('KICKING BALL FROM EJECT').",
	6: "The TOP POPPER UP coil (AE-24-900, Popper Mounting Bracket Assembly A-20919) under the top popper (switch 68): it pops the ball up into the underground (top) trough. The ROM's T.20 TOP TROUGH TEST pulses it while 68 is held ('KICKING BALL FROM POPPER').",
	7: "The ramp diverter coil (AE-26-1500, Diverter Assembly A-20882) at the ramp; the retained script rotates its diverter and drops a wall that changes the ramp's ball path. The rules light the LOCK shot on the ramp once the flashing drop targets are made, and the lock-up (switches 36, 37) sits at the ramp's far end.",
	8: "The ramp kickback coil (AE-23-800, A-20959) at the right ramp kickback lane (switch 41).",
	9: "Ball Trough Assembly A-19963-3 (coil AE-26-1500): kicks the ball over the trough eject opto (31) into the shooter lane.",
	10: "Slingshot coil (B-9362-L-2) behind the left slingshot's kick switch 47; the ROM fired it when the T.1 sweep closed 47.",
	11: "Slingshot coil (B-9362-R-3) behind the right slingshot's kick switch 48; the ROM fired it when the T.1 sweep closed 48.",
	12: "Jet bumper coil (A-9415-2) of the left jet bumper, switch 44; the ROM fired it when the T.1 sweep closed 44.",
	13: "Jet bumper coil (A-9415-2) of the right jet bumper, switch 45; the ROM fired it when the T.1 sweep closed 45.",
	14: "Jet bumper coil (A-9415-2) of the top jet bumper, switch 46; the ROM fired it when the T.1 sweep closed 46. Pinned sc.c's simulator defines sTopJet as 16, which the ROM's T.4 and T.1 contradict (16 is TOP. R. 3 BANK); the simulator constant is a naming defect, not a second jet coil.",
	15: "The reset coil (AE-26-1200) of the top left 3-bank drop targets (switches 61-63, 3-Bank Drop Target Assembly A-20892). The ROM's T.19 DROP TARGET TEST fires it for the UPPER LEFT BANK.",
	16: "The reset coil (AE-26-1200) of the top right 3-bank drop targets (switches 64-66, 3-Bank Target Assembly A-20895). The ROM's T.19 DROP TARGET TEST fires it for the UPPER RIGHT BANK.",
	17: "The BACK LEFT flasher: a #906 (24-8802) playfield flashlamp (A-20958).",
	18: "The JETS & BACK RIGHT (2) flasher: two bulbs on one circuit, a #906 (24-8802, A-20944) at the back right and a #89 (24-8704, A-17984) among the jet bumpers.",
	19: "The RIGHT MIDDLE flasher: a #906 (24-8802, A-20944).",
	20: "The RIGHT BOTTOM flasher: a #906 (24-8802, A-20944).",
	21: "The LEFT MIDDLE flasher: a #906 (24-8802, A-20958).",
	22: "The LEFT BOTTOM flasher: a #906 (24-8802, A-20958).",
	23: "Light rope 1 (04-10440) in the backbox, part of the backbox assembly 90003-BB. The ROM's T.18 LIGHT ROPE TEST flashes it as LIGHT ROPE 1 (and with 24 as BOTH).",
	24: "Light rope 2 (04-10440) in the backbox, part of the backbox assembly 90003-BB. The ROM's T.18 LIGHT ROPE TEST flashes it as LIGHT ROPE 2.",
	25: "The TOP POPPER EJECT coil (AE-27-1200, A-20920) of the top popper (switch 68): it ejects the ball from the popper back onto the playfield.",
	26: "The top light and motor (20-10307) of the backbox, a motor-driven rotating light on the 90003-BB backbox assembly powered from J140-2 (+12V to Backbox Motor). The ROM's T.4 holds it on while it is selected. The retained v1.0 script binds no callback; the later v2.0.0 script turns it into rotating beacons.",
	27: "The reset coil (AE-26-1200) of the bottom left 3-bank drop targets (switches 71-73, 3-Bank Target Assembly A-20896). The ROM's T.19 DROP TARGET TEST fires it for the LOWER LEFT BANK.",
	28: "The reset coil (AE-26-1200) of the bottom right 3-bank drop targets (switches 74-76, A-20892). The ROM's T.19 DROP TARGET TEST fires it for the LOWER RIGHT BANK.",
	35: "The AUTO PLUNGER coil (AE-23-800, Shooter Lane Kicker Assembly A-21022) in the shooter lane, on the upper-left Fliptronic power circuit (printed 'Upr. Lt. Power', Q81, J120-3): it launches the ball from the shooter-lane switch 18. The game also has a manual ball shooter (B-12445).",
	36: "The LOCK UP RELEASE coil (AE-26-1200, Multi-Ball Assembly A-20935) of the ramp lock-up (switches 36, 37), on the upper-left Fliptronic hold circuit (printed 'Upr. Lt. Hold', Q83, J120-1).",
	37: "The AUX. LAMP ENABLE line: a WPC-95 low-power device control output (J110-1, Brown-White) into the 48 Lamp & Driver P.C.B. A-20909 in the backbox, which latches its six 4094 shift registers onto the 48 backbox lamps. Pinned sc.c strobes all six registers from this bit.",
	38: "The AUX. LAMP CLOCK line (J110-3, Orange-White) into the 48 Lamp & Driver P.C.B. A-20909: it shifts both data strings one position. Pinned sc.c clocks all six registers from this bit.",
	39: "The AUX. LAMP DATA 1 line (J110-4, Yellow-White) into the 48 Lamp & Driver P.C.B. A-20909: the serial data of its first string (lamps L1-L24), which PinMAME publishes as public lamps 91-118.",
	40: "The AUX. LAMP DATA 2 line (J110-5, Green-White) into the 48 Lamp & Driver P.C.B. A-20909: the serial data of its second string (lamps L25-L48), which PinMAME publishes as public lamps 121-148.",
}
WIRE_COLOUR_NOTES = {
	21: "The ROM's T.5 prints its wires as BLU-GRN RED-WHT where this game's solenoid table and power driver list print Blu-Brn (J111-5).",
	22: "The ROM's T.5 prints its wires as BLU-BLK RED-WHT where this game's solenoid table and power driver list print Blu-Red (J111-6).",
	23: "The ROM's T.5 prints its wires as BLU-VIO RED-WHT where this game's solenoid table and power driver list print Blu-Org (J112-8).",
	24: "The ROM's T.5 prints its wires as BLU-GRY RED-WHT where this game's solenoid table and power driver list print Blu-Yel (J112-9).",
	25: "The ROM's T.4 prints its wires as BLU-BRN RED-ORN where this game's solenoid table and power driver list print Blu-Grn (J109-1).",
	26: "The ROM's T.4 prints its wires as BLU-RED RED-ORN where this game's solenoid table and power driver list print Blu-Blk (J109-2).",
	27: "The ROM's T.4 prints its wires as BLU-ORN RED-ORN where this game's solenoid table and power driver list print Blu-Vio (J109-3).",
	28: "The ROM's T.4 prints its wires as BLU-YEL RED-ORN where this game's solenoid table and power driver list print Blu-Gry (J109-4).",
}
for _address in WIRE_COLOUR_NOTES:
	WIRE_COLOUR_NOTES[_address] += " The device and the public address agree, so the colour is a wiring detail; the wiring record follows the game's own two pages."


def _solenoid_wiring(address: int) -> dict[str, Any]:
	printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
	wiring: dict[str, Any] = {"board": "WPC-95 power driver board", "control_wire": wire}
	if transistor:
		wiring["driver_transistor"] = transistor
	elif address in {37, 38, 39, 40}:
		wiring["driver_transistor"] = "low-power device control driver (no transistor printed)"
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
			stage, printed, printed_type, voltage, transistor, control, wire, coil, colour = FLIPPER_COILS[address]
			flipper = "upper right" if address in {33, 34} else ("lower right" if address in {45, 46} else "lower left")
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			notes = (
				f"The {flipper} flipper's {stage} winding (coil {coil}, printed coil colour {colour}), printed Fliptronic circuit {printed} "
				f"('{printed_type}', driver {transistor}, {control}, {wire}, supply {voltage})."
			)
			if address in {45, 46, 47, 48}:
				notes += " PinMAME publishes the lower flipper windings at 45-48, where the manual numbers them 29-32."
			else:
				notes += " scGameData declares FLIP_SOL(FLIP_UR), so PinMAME publishes the upper right flipper's ROM drive at 33-34."
			notes += _rom_note(address)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE, EDGES_SOURCE)
			script_address = 46 if address in {33, 34, 45, 46} else 48
			notes += f" Retained script: {SOLENOID_SCRIPT[script_address]}."
			refs += (VPX_SCRIPT_SOURCE,)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
				"physical": {"part_number": coil, "assembly_part_number": SOLENOID_ASSEMBLIES[address], "notes": notes},
				"wiring": {"board": "WPC-95 power driver board", "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage},
			}
			spatial = located("solenoid", address, identifier, "effect")
			if spatial:
				extra["spatial"] = spatial
				extra["physical"]["notes"] += _spatial_note("solenoid", address)
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
			notes = f"Printed solenoid table entry {address:02d} ({printed_type}" + (f", driver {transistor}" if transistor else "") + f", wire {wire}). " + SOLENOID_NOTES[address]
			notes += _rom_note(address)
			if address in WIRE_COLOUR_NOTES:
				notes += " " + WIRE_COLOUR_NOTES[address]
			if address in SOLENOID_SCRIPT:
				notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			elif address not in {37, 38, 39, 40}:
				notes += " The retained v1.0 script registers no callback for it."
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address == 26 else ("control_signal" if address in {37, 38, 39, 40} else "coil"))
			physical: dict[str, Any] = {"assembly_part_number": SOLENOID_ASSEMBLIES[address]}
			if kind in {"coil", "motor"}:
				physical["part_number"] = part
			if address in FLASHER_SOLENOIDS and address not in {23, 24}:
				physical["part_number"] = "24-8802 (#906)" if address != 18 else "24-8802 (#906), 24-8704 (#89)"
				if address == 18:
					physical["quantity"] = 2
			if address in {23, 24}:
				physical["part_number"] = part
			extra = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]}
			extra["wiring"] = _solenoid_wiring(address)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_SCRIPT:
				refs += (VPX_SCRIPT_SOURCE,)
			if address in ROM_SOLENOID_NAMES and address not in T5_ADDRESSES:
				refs += (SOLENOID_TEST_SOURCE,)
			if address in T5_ADDRESSES:
				refs += (FLASHER_TEST_SOURCE,)
			if address in {10, 11, 12, 13, 14}:
				refs += (EDGES_SOURCE,)
			if address in {2, 4}:
				refs += (TOKEN_TEST_SOURCE, BULLETIN_SOURCE)
			if address == 3:
				refs += (MOVING_TARGET_SOURCE,)
			if address in {15, 16, 27, 28}:
				refs += (DROP_TARGET_SOURCE,)
			if address in {5, 6}:
				refs += (TOP_TROUGH_SOURCE,)
			if address in {23, 24}:
				refs += (LIGHT_ROPE_SOURCE,)
			if address in {37, 38, 39, 40}:
				refs += (LAMP_TEST_SOURCE,)
			if address in BACKBOX_SOLENOIDS:
				extra["roles"] = ["cabinet.backbox"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "backbox"
			elif address in {37, 38, 39, 40}:
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
				physical["location"] = "backbox auxiliary lamp board"
			else:
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, identifier, role)
				if spatial:
					extra["spatial"] = spatial
					notes += _spatial_note("solenoid", address)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		used = address in {29, 30, 31, 41, 42, 43, 44}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Safe Cracker playfield device. The service-test runs saw it toggle in the menus.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Safe Cracker playfield device.",
			31: "PinMAME's synthetic game-on state: init_sc calls wpc_set_fastflip_addr(0x86), so this channel reflects the ROM's fast-flip RAM flag, not a relay. No WPC generation has a game-on relay here.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
			41: "PinMAME's WPC-95 backward-compatibility mirror of LPDC output 37 (core_getSol serves 41-44 from the 37-40 bits); it reports the same auxiliary-lamp enable line and is not an additional device. Every run saw it change with 37.",
			42: "PinMAME's mirror of LPDC output 38 (auxiliary-lamp clock); not an additional device.",
			43: "PinMAME's mirror of LPDC output 39 (auxiliary-lamp data 1); not an additional device.",
			44: "PinMAME's mirror of LPDC output 40 (auxiliary-lamp data 2); not an additional device.",
			49: "PinMAME's simulator-only ball-shooter channel; Safe Cracker's real launcher is public solenoid 35.",
			50: "Reserved PinMAME output position before the first custom-output boundary; scGameData declares no custom solenoids.",
		}[address]
		roles = ["internal.wpc-state"] if address in {29, 30, 31} else (["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"])
		refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((SOLENOID_TEST_SOURCE,) if address in {41, 42, 43, 44} else ())
		items.append(
			_device(
				identifier, label, "virtual", SOLENOID_GROUP, address, "used" if used else "unused", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


# --- Lamp data (lamp-matrix.md, lamp-locations.md, aux-lamp-board.md) ------------------------------------
# address -> (bulb part number, lamp assembly, printed description), Lamp Locations lists (2-46, 2-47).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-20887", "Lite Deposit"), 12: ("24-8768", "A-20887", 'Center Timer "10"'), 13: ("24-8768", "A-20887", "Disable Computer"),
	14: ("24-8768", "A-20887", 'Center Timer "5"'), 15: ("24-8768", "A-20887", 'Center Timer "0"'), 16: ("24-8768", "A-20887", "Lite Lock"),
	17: ("24-8768", "A-20887", 'Center Timer "55"'), 18: ("24-8768", "A-20887", 'Center Timer "50"'), 21: ("24-8768", "A-20887", 'Center Timer "15"'),
	22: ("24-8768", "A-20887", 'Center Timer "20"'), 23: ("24-8768", "A-20887", 'Center Timer "25"'), 24: ("24-8768", "A-20887", 'Center Timer "30"'),
	25: ("24-8768", "A-20887", 'Center Timer "35"'), 26: ("24-8768", "A-20887", "Call Guard"), 27: ("24-8768", "A-20887", 'Center Timer "45"'),
	28: ("24-8768", "A-20887", 'Center Timer "40"'), 31: ("24-8768", "A-20886", "Armor Car-Cellar"), 32: ("24-8768", "A-20886", "Armor Car-Roof"),
	33: ("24-8768", "A-20886", "Armor Car-Main"), 34: ("24-8768", "A-20886", "Bonus 2X"), 35: ("24-8768", "A-20888", "(A)LARM Standup"),
	36: ("24-8768", "A-20888", "ATM Card"), 37: ("24-8768", "A-20888", "A(L)ARM Standup"), 38: ("24-8768", "A-20888", "Ramp Jackpot"),
	41: ("24-8768", "A-20886", "Bonus 5X + Outlane"), 42: ("24-8768", "A-20886", "Bonus 5X"), 43: ("24-8768", "A-20886", "Bonus 4X"),
	44: ("24-8768", "A-20886", "Bonus 3X"), 45: ("24-6549", "A-17807", "Ramp Lock"), 46: ("24-6549", "A-17835", "AL(A)RM Standup"),
	47: ("24-6549", "A-17835", "ALA(R)M Standup"), 48: ("24-6549", "A-17835", "ALAR(M) Standup"), 51: ("24-8768", "A-20888", "Wheel Arrow"),
	52: ("24-8768", "A-20888", "Lite Outlanes"), 53: ("24-8768", "A-20888", "Invisible Code"), 54: ("24-8768", "A-20888", "Explosives"),
	55: ("24-8768", "A-20888", "Note to Teller"), 56: ("24-6549", "A-17835", "Top Left Lane"), 57: ("24-6549", "A-17807", "Top Middle Lane"),
	58: ("24-6549", "A-17835", "Top Right Lane"), 61: ("24-6549", "A-17835", "Top Right 3-Bank Top"), 62: ("24-6549", "A-17807", "Top Right 3-Bank Middle"),
	63: ("24-6549", "A-17835", "Top Right 3-Bank Bottom"), 64: ("24-6549", "A-17835", "Top Left 3-Bank Top"), 65: ("24-6549", "A-17807", "Top Left 3-Bank Middle"),
	66: ("24-6549", "A-17835", "Top Left 3-Bank Bottom"), 67: ("24-6549", "A-17835", 'Right "Extra Time"'), 68: ("24-6549", "A-17835", "Right Return"),
	71: ("24-6549", "A-17835", "Bottom Right 3-Bank Top"), 72: ("24-6549", "A-17807", "Bottom Right 3-Bank Middle"), 73: ("24-6549", "A-17835", "Bottom Right 3-Bank Bottom"),
	74: ("24-6549", "A-17835", "Bottom Left 3-Bank Top"), 75: ("24-6549", "A-17807", "Bottom Left 3-Bank Middle"), 76: ("24-6549", "A-17835", "Bottom Left 3-Bank Bottom"),
	77: ("24-6549", "A-17835", "Left Return"), 78: ("24-6549", "A-17835", 'Left "Extra Time"'), 81: ("24-8768", "B-9414-3", "Top Jet (Yellow)"),
	82: ("24-8768", "B-9414-3", "Left Jet (Clear)"), 83: ("24-8768", "B-9414-3", "Right Jet (Red)"), 84: ("24-6549", "04-10083", "Bank Left"),
	85: ("24-6549", "04-10083", "Bank Right"), 86: ("24-6549", "A-16041", "Vari Break In"), 87: ("24-6549", "A-16041", "Roof Break In"),
	88: ("---", "20-9663-16", "Start Button"),
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
# The ROM's T.8 SINGLE LAMPS names (single-lamps run).
ROM_LAMP_NAMES = {
	11: "LITE DEPOSIT", 12: 'CTR. TIMER "10"', 13: "DISABLE COMPUTER", 14: 'CTR. TIMER "5"', 15: 'CTR. TIMER "0"', 16: "LITE LOCK",
	17: 'CTR. TIMER "55"', 18: 'CTR. TIMER "50"', 21: 'CTR. TIMER "15"', 22: 'CTR. TIMER "20"', 23: 'CTR. TIMER "25"', 24: 'CTR. TIMER "30"',
	25: 'CTR. TIMER "35"', 26: "CALL GUARD", 27: 'CTR. TIMER "45"', 28: 'CTR. TIMER "40"', 31: "ARMOR CAR-CELLAR", 32: "ARMOR CAR-ROOF",
	33: "ARMOR CAR-MAIN", 34: "BONUS 2X", 35: "(A)LARM STANDUP", 36: "ATM CARD", 37: "A(L)ARM STANDUP", 38: "RAMP JACKPOT",
	41: "BONUS 5X+OUTLANE", 42: "BONUS 5X", 43: "BONUS 4X", 44: "BONUS 3X", 45: "RAMP LOCK", 46: "AL(A)RM STANDUP", 47: "ALA(R)M STANDUP",
	48: "ALAR(M) STANDUP", 51: "WHEEL ARROW", 52: "LITE OUTLANES", 53: "VAULT LETTER", 54: "EXPLOSIVES", 55: "NOTE TO TELLER",
	56: "TOP LEFT LANE", 57: "TOP MIDDLE LANE", 58: "TOP RIGHT LANE", 61: "TR. 3BANK TOP", 62: "TR. 3BANK MIDDLE", 63: "TR. 3BANK BOTTOM",
	64: "TL. 3BANK TOP", 65: "TL. 3BANK MIDDLE", 66: "TL. 3BANK BOTTOM", 67: 'RT. "EXTRA TIME"', 68: "RIGHT RETURN", 71: "BR. 3BANK TOP",
	72: "BR. 3BANK MIDDLE", 73: "BR. 3BANK BOTTOM", 74: "BL. 3BANK TOP", 75: "BL. 3BANK MIDDLE", 76: "BL. 3BANK BOTTOM", 77: "LEFT RETURN",
	78: 'LT. "EXTRA TIME"', 81: "TOP JET (YELLOW)", 82: "LEFT JET (CLEAR)", 83: "RIGHT JET (RED)", 84: "BANK LEFT", 85: "BANK RIGHT",
	86: "MOVNG BREAK IN", 87: "ROOF BREAK IN", 88: "START BUTTON",
}
LAMP_LABELS = {
	12: 'Center Timer "10"', 14: 'Center Timer "5"', 15: 'Center Timer "0"', 17: 'Center Timer "55"', 18: 'Center Timer "50"',
	21: 'Center Timer "15"', 22: 'Center Timer "20"', 23: 'Center Timer "25"', 24: 'Center Timer "30"', 25: 'Center Timer "35"',
	27: 'Center Timer "45"', 28: 'Center Timer "40"', 35: "(A)LARM Standup", 37: "A(L)ARM Standup", 46: "AL(A)RM Standup",
	47: "ALA(R)M Standup", 48: "ALAR(M) Standup", 36: "ATM Card", 67: 'Right "Extra Time"', 78: 'Left "Extra Time"',
	41: "Bonus 5X + Outlane", 31: "Armor Car-Cellar", 32: "Armor Car-Roof", 33: "Armor Car-Main",
}
# Backbox board-game lamps of the 48 Lamp & Driver P.C.B. A-20909: public -> (L number, ROM name, the ROM's lamp-power wire).
AUX_LAMPS = {
	91: (24, "!", "WHT-VIO"), 92: (23, "TELLER", "WHT-VIO"), 93: (22, "DOG", "WHT-VIO"), 94: (21, "?", "WHT-VIO"), 95: (20, "ALARM 3", "WHT-VIO"),
	96: (19, "$", "WHT-VIO"), 97: (18, "DOG", "WHT-VIO"), 98: (17, "CANDY", "WHT-VIO"), 101: (16, "$", "WHT-VIO"), 102: (15, "?", "WHT-VIO"),
	103: (14, "ALARM 2", "WHT-VIO"), 104: (13, "#", "WHT-VIO"), 105: (12, "<-->", "WHT-VIO"), 106: (11, "TELLER", "WHT-VIO"),
	107: (10, "BRIBE", "WHT-VIO"), 108: (9, "?", "WHT-VIO"), 111: (8, "ALARM 1", "WHT-GRN"), 112: (7, "$", "WHT-GRN"), 113: (6, "DOG", "WHT-GRN"),
	114: (5, "CANDY", "WHT-GRN"), 115: (4, "$", "WHT-GRN"), 116: (3, "?", "WHT-GRN"), 117: (2, "ALARM 4", "WHT-GRN"), 118: (1, "$", "WHT-GRN"),
	121: (48, "BRIBE", "WHT-GRN"), 122: (47, "?", "WHT-GRN"), 123: (46, "$", "WHT-GRN"), 124: (45, "?", "WHT-GRN"), 125: (44, "CELLAR", "WHT-GRN"),
	126: (43, "$", "WHT-GRN"), 127: (42, "?", "WHT-GRN"), 128: (41, "?", "WHT-GRN"), 131: (40, "VAULT", "WHT-ORN"), 132: (39, "GATE 1", "WHT-ORN"),
	133: (38, "?", "WHT-ORN"), 134: (37, "GATE 2", "WHT-ORN"), 135: (36, "?", "WHT-ORN"), 136: (35, "GATE 3", "WHT-ORN"), 137: (34, "GATE 4", "WHT-ORN"),
	138: (33, "?", "WHT-ORN"), 141: (32, "?", "WHT-ORN"), 142: (31, "BRIBE", "WHT-ORN"), 143: (30, "ROOF", "WHT-ORN"), 144: (29, "BRIBE", "WHT-ORN"),
	145: (28, "$", "WHT-ORN"), 146: (27, "?", "WHT-ORN"), 147: (26, "$", "WHT-ORN"), 148: (25, "MAIN", "WHT-ORN"),
}
AUX_POWER = {"WHT-VIO": (4, "AUX. LAMP 3 POWER", "J106-11"), "WHT-GRN": (3, "AUX. LAMP 2 POWER", "J106-10"), "WHT-ORN": (1, "AUX. LAMP 1 POWER", "J106-8")}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description = LAMP_LOCATIONS[address]
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {"quantity": 1, "assembly_part_number": assembly}
			if bulb != "---":
				physical["part_number"] = bulb
			notes = (
				f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description "
				f"\"{description}\"" + (f", bulb {bulb} ({'#555' if bulb == '24-8768' else '#44'})." if bulb != "---" else ", no bulb printed.")
			)
			notes += (
				f" The ROM's T.8 SINGLE LAMPS TEST lights public lamp {address} alone and names it \"{ROM_LAMP_NAMES[address]}\" "
				f"(RED-{('BRN', 'BLK', 'ORN', 'YEL', 'GRN', 'BLU', 'VIO', 'GRY')[row - 1]} YEL-{('BRN', 'RED', 'ORN', 'BLK', 'GRN', 'BLU', 'VIO', 'GRY')[column - 1]})."
			)
			if address == 53:
				notes += " The manual's matrix and list print INVISIBLE CODE where the 1.8 ROM names it VAULT LETTER."
			if address == 86:
				notes += " The manual prints VARI BREAK IN where the 1.8 ROM names it MOVNG BREAK IN (the vari target is the moving target)."
			if address in {75, 76}:
				notes += (
					f" The matrix prints this cell BOTTOM R. 3-BANK {'MIDDLE' if address == 75 else 'BOTTOM'}, but the Lamp Locations list "
					"prints Bottom Left, the ROM names it BL. 3BANK and its T.19 DROP TARGET TEST flashes 74-76 for the LOWER LEFT BANK: the "
					"matrix cell is a misprint and the label follows the list."
				)
			if address in {61, 62, 63, 64, 65, 66, 71, 72, 73, 74, 75, 76}:
				bank = {6: ("UPPER RIGHT", "64-66") if address <= 63 else ("UPPER LEFT", "61-63"), 7: ("LOWER RIGHT", "74-76") if address <= 73 else ("LOWER LEFT", "71-73")}[column]
				notes += f" The ROM's T.19 DROP TARGET TEST flashes it for the {bank[0]} BANK, whose target switches are {bank[1]}."
			if address in {27, 28}:
				notes += (
					f" The retained v1.0 script binds lamp {address} to the light named l{55 - address} (NFadeL 27, l28 and NFadeL 28, l27); "
					"the later v2.0.0 script's change log says the manual picture had the inserts for 27 and 28 reversed while the written "
					"numbers were correct."
				)
			if address in {81, 82, 83}:
				notes += f" The jet bumper cap lamp (B-9414-3) of the {('top', 'left', 'right')[address - 81]} jet bumper (switch {(46, 44, 45)[address - 81]}, coil {(14, 12, 13)[address - 81]})."
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
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE)
			if address == 88:
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet button"
				physical["notes"] += " The lamp inside the lit Start button; the retained v1.0 script does not handle lamp 88."
			else:
				refs += (VPX_SCRIPT_SOURCE,)
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
					physical["notes"] += _spatial_note("lamp", address)
			label = LAMP_LABELS.get(address, description.title().replace("'S", "'s"))
			items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, "used", refs, **extra))
	for address, (lamp, name, wire) in AUX_LAMPS.items():
		gi, power_name, power_pin = AUX_POWER[wire]
		string = "first (DATA 1, lamps L1-L24)" if lamp <= 24 else "second (DATA 2, lamps L25-L48)"
		notes = (
			f"Backbox board-game lamp L{lamp} of the 48 Lamp & Driver P.C.B. A-20909 (bulb 24-8768, #555; the Lamp Locations backbox "
			f"list prints every L1-L48 row as 'Backbox Lamp'). The ROM's T.8 SINGLE LAMPS TEST lights public lamp {address} alone and "
			f"prints it as L{lamp} \"{name}\" on the AUX P.C.B. with the lamp-power wire {wire}, which is G.I. string {gi + 1} "
			f"({power_name}, {power_pin}). PinMAME's init_sc shifts the LPDC lines 37-40 into six 4094 registers and publishes them "
			f"as lamp columns 9-14; this lamp sits on the board's {string} serial string. The lamps light the board game drawn on "
			"the backglass, behind the backbox doors."
		)
		if lamp == 40:
			notes += " The backbox lamp drawing (2-48) prints no balloon for L40; its list row and the ROM's test name it."
		items.append(
			_device(
				f"lamp.backbox-l{lamp}", f"Backbox Lamp L{lamp}", "lamp", LAMP_GROUP, address, "used",
				(MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE, VPX_SCRIPT_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"L{lamp}"}],
				roles=["cabinet.backbox"],
				physical={"location": "backbox", "quantity": 1, "part_number": "24-8768", "assembly_part_number": "A-20909", "notes": notes + " Retained script: FlashC drives the backglass sprite l" + str(address) + "."},
				wiring={"board": "48 Lamp & Driver P.C.B. A-20909", "power_connection": f"{power_pin} ({power_name})", "power_wire": {"WHT-VIO": "White-Violet", "WHT-GRN": "White-Green", "WHT-ORN": "White-Orange"}[wire]},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	return items


# --- General illumination (solenoid-flasher-table.md G.I. block; power-driver-board.md; gi-test run) -----
# public -> (string, printed function, triac, voltage, drive, wire, playfield bulb, backbox bulb, ROM T.6 name, ROM wires, dimmable in T.6)
GI_STRINGS = {
	0: (1, "ILLUMINATION STRING 1", "Q5", "J105-1, J106-1", "J105-7, J106-7", "Wht-Brn", "#44", "#555", "ILLUM. STRING 1", "WHT-BRN BRN", True),
	1: (2, "**AUX. LAMP 1 POWER", "Q4", None, "J106-8", "Wht-Org", None, "#555", "AUX. LAMP 1 POWER", "WHT-ORN ORN", True),
	2: (3, "ILLUMINATION STRING 3", "Q3", "J105-3, J106-3", "J105-9, J106-9", "Wht-Yel", "#44", "#555", "ILLUM. STRING 3", "WHT-YEL YEL", True),
	3: (4, "**AUX. LAMP 2 POWER", "Q2", None, "J106-10", "Wht-Grn", None, "#555", "AUX. LAMP 2 POWER", "WHT-GRN GRN", False),
	4: (5, "**AUX. LAMP 3 POWER", "Q1", None, "J106-11", "Wht-Vio", None, "#555", "AUX. LAMP 3 POWER", "WHT-VIO VIO", False),
}
AUX_STRING_LAMPS = {1: "L25-L40 (public 131-148)", 3: "L1-L8 and L41-L48 (public 111-128)", 4: "L9-L24 (public 91-108)"}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (string, printed, triac, voltage, drive, wire, playfield_bulb, backbox_bulb, rom_name, rom_wires, dimmable) in GI_STRINGS.items():
		notes = (
			f"Printed general-illumination row {string:02d} '{printed}': triac {triac}, wire {wire}, drive {drive}"
			+ (f", voltage {voltage}" if voltage else ", no voltage connection printed")
			+ (f"; playfield bulbs {playfield_bulb}, backbox bulbs {backbox_bulb}." if playfield_bulb else f"; backbox bulbs {backbox_bulb} only.")
		)
		if dimmable:
			notes += f" The ROM's T.6 GENERAL ILLUMINATION TEST names it '{rom_name}' ({rom_wires}) and steps its brightness on public GI {address} alone."
		else:
			notes += f" The ROM's T.6 names it '{rom_name}' 'ON ONLY' ({rom_wires}), and public GI {address} stayed on in every snapshot of every service-test run."
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, GI_TEST_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{string:02d}"}],
			"wiring": {"board": "WPC-95 power driver board", "driver_transistor": triac, "control_connection": drive, "control_wire": wire},
		}
		if voltage:
			extra["wiring"]["power_connection"] = voltage
		if string in (2, 4, 5):
			notes += (
				f" The table's footnote marks it '**These G.I. strings do not brighten and dim, they are always ON.' It powers the backbox "
				f"board-game lamps {AUX_STRING_LAMPS[address]} of the 48 Lamp & Driver P.C.B. A-20909 through the board's J2, which is how "
				"the ROM's T.8 prints their lamp-power wire."
			)
			if address == 1:
				notes += " The ROM nevertheless dims this string in T.6 (ALL ILLUMINATION and its own item step BRIGHT=1-8 on public GI 1), so its runtime level is not constant."
			extra["roles"] = ["cabinet.backbox"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			extra["physical"] = {"location": "backbox", "notes": notes}
		else:
			if address == 0:
				notes += (
					" The power driver board's list routes J105-1 and J105-7 to the Coin Door Interface Board (J2-5, J2-3) where the solenoid "
					"table files them under Playfield; J106-1/J106-7 feed the insert panel."
				)
			else:
				notes += " The power driver board's list routes J105-3 and J105-9 to the playfield and J106-3/J106-9 to the insert panel."
			notes += (
				" The retained v1.0 table drives every GI bulb it models from public GI 0 alone (UpdateGIObjects on the GIs collection) and "
				"has no consumer for strings 2-5, so it cannot say which modelled bulb belongs to string 1 or string 3; no retained drawing "
				"or count locates GI bulbs either, so the string has no placement."
			)
			extra["physical"] = {"notes": notes}
			refs += (VPX_SCRIPT_SOURCE,)
		items.append(_device(f"gi.string-{string}", f"General Illumination String {string}" + (f" ({printed.strip('*').title()})" if string in (2, 4, 5) else ""), "gi", GI_GROUP, address, "used", refs, **extra))
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
			"physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		},
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
	banks = []
	for suffix, label, coil, switches, lamps, rom, assembly in (
		("top-left-drop-bank", "Top left 3-bank drop targets", 15, (61, 62, 63), (64, 65, 66), "UPPER LEFT BANK (LOW-63 MID-62 UPR-61)", "A-20892"),
		("top-right-drop-bank", "Top right 3-bank drop targets", 16, (66, 65, 64), (61, 62, 63), "UPPER RIGHT BANK (UPR-66 MID-65 LOW-64)", "A-20895"),
		("bottom-left-drop-bank", "Bottom left 3-bank drop targets", 27, (71, 72, 73), (74, 75, 76), "LOWER LEFT BANK (LOW-73 MID-72 UPR-71)", "A-20896"),
		("bottom-right-drop-bank", "Bottom right 3-bank drop targets", 28, (76, 75, 74), (71, 72, 73), "LOWER RIGHT BANK (UPR-76 MID-75 LOW-74)", "A-20892"),
	):
		banks.append(_mechanism(
			suffix, label, "drop_target_bank", [_coil(coil)], _matrix(*switches),
			f"Three drop targets (switch assembly A-13609, optos the matrix shades) with one reset coil, solenoid {coil}. A target's "
			f"switch reads 1 while it is down. The ROM's T.19 DROP TARGET TEST shows the bank as {rom}, marks each target while it is "
			f"held down, flashes the bank's three lamps {', '.join(map(str, lamps))} and fires {coil} on Enter. The rules' break-ins "
			"start from the flashing drop targets; completing them lights the LOCK on the ramp.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, DROP_TARGET_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, assembly,
		))
	return banks + [
		_mechanism(
			"moving-target", "Moving (vari) target", "other", [_coil(3)], _matrix(56, 57, 58, 12),
			"The Vari-Target Assembly A-20851 (the ROM calls it the moving target): a target the ball pushes back along a track, read "
			"by the three optos of the 3 Opto Vari Target P.C.B. A-20906 (switches 56, 57, 58, the ROM's C, B and A), whose interrupter "
			"fingers set the depth reading. The reset coil's armature bracket engages the pivot arm's teeth and holds the target back; "
			"dislodged from the teeth, the target snaps to its forward-most position, which is home. The manual's adjustment procedure "
			"(1-52, 1-53) leaves Opto 3's beam clear with the target rear-most and has it completely broken with the target forward-most; "
			"the board's schematic and pin list wire OPTO3 to row 8, switch 58 (A), so at home 58 reads OPEN (public 1). The procedure "
			"does not give the other two optos' home levels. In the ROM's T.16 MOVING TARGET TEST each switch reads CLOSED at public 0 "
			"and OPEN at 1, and the number the test shows reads 0 with all closed, 1 with A (58) open, 3 with B (57), 2 with B and A, 7 "
			"with C (56), 6 with C and A, 4 with C and B and 5 with all three: the ROM decodes the three optos as the reflected binary "
			"(Gray) code of a position 0-7 with A as the least significant bit. Home with A open and the rear-most position with A clear "
			"are consistent with that code but do not fix which positions they are. Enter fires the reset coil (solenoid 3) and the test "
			"shows RESETTING MOVING TARGET. Pushed fully back, the target lets the ball through to the underground trough switch 12 (TP "
			"TROUGH (MOVE), T.20's TR2). The retained v1.0 script models the travel with its own code table for 56-58 and holds 56 alone "
			"at 1 at home; the later v2.0.0 script uses a one-hot code and holds all three at 0 at home. Neither is the factory encoder: "
			"take the code from the ROM's decoding and the home level of 58 from the manual.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_SCRIPT_V2_SOURCE, MOVING_TARGET_SOURCE, MOVING_TARGET_CODES_SOURCE, EDGES_SOURCE, TOP_TROUGH_SOURCE),
			None, "A-20851",
		),
		_mechanism(
			"top-popper-and-underground-trough", "Top popper, underground trough and bank kickout", "kicker",
			[_coil(6), _coil(25), _coil(5)], _matrix(68, 11, 12, 77),
			"A ball in the top popper (switch 68) is either popped up into the underground (top) trough by TOP POPPER UP (solenoid 6) or "
			"ejected back onto the playfield by TOP POPPER EJECT (25). The underground trough also takes balls from the roof entrance "
			"(TR1, switch 11) and from behind the moving target (TR2, 12) and delivers them to TR3 at the bank (77), where BANK KICK (5, "
			"Center Loop Kick-Back Assembly A-20923) kicks them out. The ROM's T.20 TOP TROUGH TEST shows TOP BALL POPPER-68 and TR1-11, "
			"TR2-12, TR3-77; it pulsed 6 while 68 was held ('KICKING BALL FROM POPPER') and 5 while 77 was held ('KICKING BALL FROM "
			"EJECT'); the manual says balls arriving at the bank are kicked back out after a slight pause.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, TOP_TROUGH_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("popper", "Top popper", _matrix(68), "Ball in the top popper; 6 pops it up into the underground trough, 25 ejects it to the playfield."),
				("tr1", "TR1 (roof)", _matrix(11), "Underground trough switch reached from the roof entrance."),
				("tr2", "TR2 (moving target)", _matrix(12), "Underground trough switch reached past the moving target."),
				("tr3", "TR3 (bank)", _matrix(77), "Ball at the bank kickout; 5 kicks it out."),
			],
			"A-20923",
		),
		_mechanism(
			"spin-disc", "Spinning disc (the wheel)", "rotary", [], _matrix(85, 86),
			"The Spin Target Assembly A-20911: a free-spinning disc the ball sets turning, read by the two optos of the Spin Disc Opto "
			"P.C.B. A-20952 (WHEEL CHANNEL A and B, switches 85 and 86) in quadrature, so the ROM sees both speed and direction. It has "
			"no coil. The manual's T.16 Wheel Test (a test the 1.8 ROM no longer offers) showed whether both optos were seen and which way "
			"the wheel turned; the rules' 'wheel' value is shown on the display. The retained scripts write 85/86 as a two-bit Gray "
			"sequence from the disc angle, one step per 3.75 degrees.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE), None, "A-20911",
		),
		_mechanism(
			"token-dispenser", "Token dispenser and token slot", "toy", [_coil(4), _coil(2)], _matrix(81, 82, 43) + ["switch.generic-118"],
			"The backbox token mechanism: two token tubes, each with a shuttle-plunger coil (04-10424; left tube solenoid 4, right tube "
			"solenoid 2) and a level switch (81 left, 82 right), dispense magic tokens past the token chute opto (43, TOKN CHUTE EXIT) to "
			"the player when the vault is cracked. The ROM's T.17 TOKEN TEST pulses 4 and 2 one after the other for each dispense. A token "
			"put back into the token slot at the coin door closes the F8 input (118, TOKEN COIN SLOT); the rules' hint is 'Replay MAGIC "
			"TOKENS for surprising results!'. IPDB: twenty different tokens (19 gold, 1 silver). Service Bulletin 90 replaces the stop "
			"brackets of both shuttle plungers on early games that dispensed intermittently. Pinned sc.c: the percentaging firmware limits "
			"tokens by earnings; the No Percentaging builds do not.",
			(MANUAL_SOURCE, BULLETIN_SOURCE, IDENTITY_SOURCE, CORE_SOURCE, TOKEN_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			None, "A-20925",
		),
		_mechanism(
			"backbox-board-game", "Backbox board game lamps", "other", [_coil(37), _coil(38), _coil(39), _coil(40)], [],
			"The backglass shows a board game the player moves around to reach the vault, lit from behind by the 48 lamps L1-L48 of the "
			"48 Lamp & Driver P.C.B. A-20909 (six 4094 shift registers, 2N6426 Darlington drivers, an LM339 input buffer). The ROM shifts "
			"the lamp states out on the WPC-95 low-power device control lines 37 (enable), 38 (clock), 39 (data 1, L1-L24) and 40 (data 2, "
			"L25-L48); PinMAME's init_sc decodes the stream into lamp columns 9-14 (public 91-148), which the ROM's T.8 walks as L24-L1 "
			"and L48-L25. G.I. strings 2, 4 and 5 power the lamps. The backbox doors swing open to reveal the backglass (IPDB).",
			(MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE, IDENTITY_SOURCE, VPX_SCRIPT_SOURCE), None, "A-20909",
		),
		_mechanism(
			"ramp-lock", "Ramp lock-up", "kicker", [_coil(36), _coil(7)], _matrix(36, 37, 83, 84),
			"The Multi-Ball Assembly A-20935 holds up to two locked balls on the ramp, seen by the Lockup 1 Front (36) and Lockup 2 Rear "
			"(37) optos and released by LOCK UP RELEASE (solenoid 36, on the upper-left Fliptronic hold circuit). The ramp diverter (7) "
			"sits on the ramp, which has an entrance switch (83) and a made switch (84). The rules light LOCK on the ramp once the "
			"flashing drop targets are made; locked balls light the bank entrances for a break-in, and multi-ball follows a break-in. The "
			"retained script releases both locked balls with one pin and clears 36 and 37 together.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE), None, "A-20935",
		),
		_mechanism(
			"kickbacks", "Left big kick and ramp kickback", "kicker", [_coil(1), _coil(8)], _matrix(42, 41),
			"Two kickbacks, each with an opto from the 10-opto board: BIG KICK (solenoid 1, A-21034) at the left with the left big kick opto "
			"(42), and KICKBACK (RAMP) (solenoid 8, A-20959) at the right with the kickback opto (41). Opto 42 reads 1 while the ball is "
			"in front of the left kicker; opto 41 rests at public 1 and drops to 0 while the ball passes (see the switch notes).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE), None, "A-21034",
		),
		_mechanism(
			"ball-trough", "Ball trough", "kicker", [_coil(9)], _matrix(31, 32, 33, 34, 35),
			"Ball Trough Assembly A-19963-3 with four balls: drained balls collect over the Trough Ball 1-4 optos (32-35) and the trough "
			"eject coil (9) kicks the lowest ball past the Trough Eject opto (31) into the shooter lane. The optos read a ball at public 1.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("trough-eject", "Trough eject", _matrix(31), "Ball at the eject position, over the trough eject coil."),
				("trough-1", "Trough, 1 ball", _matrix(32), "At least one ball in the trough."),
				("trough-2", "Trough, 2 balls", _matrix(33), "At least two balls."),
				("trough-3", "Trough, 3 balls", _matrix(34), "At least three balls."),
				("trough-4", "Trough, 4 balls", _matrix(35), "All four balls."),
			],
			"A-19963-3",
		),
		_mechanism(
			"shooter-lane", "Shooter lane and auto plunger", "kicker", [_coil(35)], _matrix(18),
			"A manual ball shooter (B-12445) and an AUTO PLUNGER coil (solenoid 35, Shooter Lane Kicker Assembly A-21022) both launch the "
			"ball resting on the shooter-lane switch 18. The auto plunger sits on the upper-left Fliptronic power circuit.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE), None, "A-21022",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(10), _coil(11)], _matrix(47, 48),
			"Two slingshots with kick switches SW-1A-114 and score switches SW-1A-120 on 47 and 48; the ROM fired 10 for 47 and 11 for 48 "
			"even inside the T.1 test.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE),
		),
		_mechanism(
			"jet-bumpers", "Jet bumpers", "other", [_coil(12), _coil(13), _coil(14)], _matrix(44, 45, 46),
			"Three jet bumpers (Jet Bumper Assembly B-9414-3, coil assemblies A-9415-2): left (switch 44, coil 12, clear cap lamp 82), right "
			"(45, 13, red cap lamp 83) and top (46, 14, yellow cap lamp 81). The ROM fired each coil for its own switch even inside T.1. "
			"The retained v1.0 script pairs the switches with its bumper objects the same way; the later v2.0.0 script swaps 44 and 46.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_SCRIPT_V2_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE, LAMP_TEST_SOURCE), None, "B-9414-3",
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)], ["switch.generic-111", "switch.generic-112"],
			"Flipper assembly A-14876-R-6 with an FL-20867 coil (power 45, hold 46, printed circuits 29-30) and an SW-1A-194 end-of-stroke "
			"switch (F1, 111) that PinMAME synthesizes. The right cabinet button breaks the right Flipper Opto Board's F2 opto (112); its F6 "
			"opto (116) fires this flipper too.",
			flipper_refs, None, "A-14876-R-6",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)], ["switch.generic-113", "switch.generic-114"],
			"Flipper assembly A-15849-L-7 with an FL-20867 coil (power 47, hold 48, printed circuits 31-32) and an SW-1A-194 end-of-stroke "
			"switch (F3, 113) that PinMAME synthesizes. The left cabinet button breaks the left Flipper Opto Board's F4 opto (114).",
			flipper_refs, None, "A-15849-L-7",
		),
		_mechanism(
			"upper-right-flipper", "Upper right flipper", "other", [_coil(33), _coil(34)], ["switch.generic-115", "switch.generic-116"],
			"Flipper assembly A-15849-R-1 with an FL-11753 coil (power 33, hold 34) and an SW-1A-194 end-of-stroke switch (F5, 115) that "
			"PinMAME synthesizes. It is worked by the right cabinet button's second opto (F6, 116), which the ROM also uses to fire the "
			"lower right flipper; the rules light the wheel from the right upper mini-flipper lane, whose rollover is switch 25.",
			flipper_refs, None, "A-15849-R-1",
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
	"switch-locations": "Bally_1996_Safe_Cracker_Manual.pdf page 115, crop box 0.25,0.09,0.76,0.685, scanned page rendered at its native resolution (embedded image xref 570, 2480px across 8.27in), rendered at 300 dpi, grayscale, 1265x1951 WebP quality 80",
	"solenoid-flasher-locations": "Bally_1996_Safe_Cracker_Manual.pdf page 117, crop box 0.25,0.06,0.755,0.665, scanned page rendered at its native resolution (embedded image xref 580, 2480px across 8.27in), rendered at 300 dpi, grayscale, 1253x1984 WebP quality 80",
	"lamp-locations": "Bally_1996_Safe_Cracker_Manual.pdf page 119, crop box 0.31,0.05,0.69,0.735, scanned page rendered at its native resolution (embedded image xref 590, 2477px across 8.26in), rendered at 300 dpi, grayscale, 943x2235 WebP quality 80",
}


def _excerpt(name: str, locator: str, *, image: bool = False, method: str = "manual", reviewed: bool = True, credit: str = TRANSCRIBED) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.safe-cracker.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = DRAWING_DERIVATIONS[name]
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("switch-matrix", "PDF page 114, printed 2-42, Switch Matrix with the dedicated and flipper grounded-switch blocks and the opto shading; Section 3 reprint PDF 126 (3-2) compared; Dedicated Switches drawing PDF 127 (3-3)"),
		_excerpt("switch-locations", "PDF pages 114-115, printed 2-42 and 2-43, Switch Locations list and playfield drawing (image)", image=True),
		_excerpt("lamp-matrix", "PDF page 118, printed 2-46, Lamp Matrix; reprints PDF 128 (3-4) and PDF 157 compared"),
		_excerpt("lamp-locations", "PDF pages 118-120, printed 2-46 to 2-48, Lamp Locations lists, playfield lamp drawing (image) and backbox lamp drawing", image=True),
		_excerpt("solenoid-flasher-table", "PDF page 116, printed 2-44, Solenoid/Flasher Table with the general-illumination and flipper-circuit blocks; reprint PDF 129 (3-5) compared"),
		_excerpt("solenoid-flasher-locations", "PDF pages 116-117, printed 2-44 and 2-45, Solenoid/Flasher Locations list, G.I. and flipper-coil lists and playfield drawing (image)", image=True),
		_excerpt("solenoid-wiring-pages", "PDF pages 130-134, printed 3-6 to 3-10, solenoid, flasher, high-power, special-solenoid and G.I. circuit drawings"),
		_excerpt("power-driver-board", "PDF pages 148-151, printed 3-24 to 3-27, Power Driver Board A-20028 drawing and connector list"),
		_excerpt("cpu-board", "PDF pages 152-153, printed 3-28 and 3-29, Security CPU Board A-20119-90003 drawing and connector list"),
		_excerpt("aux-lamp-board", "PDF pages 86, 145 and 146, printed 2-14, 3-21 and 3-22, 48 Lamp & Driver P.C.B. A-20909 parts list, board drawing and schematic"),
		_excerpt("section-3-boards", "PDF pages 135-144 and 147, printed 3-11 to 3-20 and 3-23, flipper circuits, cabinet switch circuits, opto boards, 10 Opto P.C.B., 3 Opto Vari Target P.C.B. and Spin Disc Opto P.C.B."),
		_excerpt("game-rules", "PDF page 16, printed B, Game Rules"),
		_excerpt("moving-target-adjustment", "PDF pages 68-69, printed 1-52 and 1-53, Adjust Moving Target Assembly procedure and its two drawings"),
		_excerpt("service-tests", "PDF pages 32-36, printed 1-16 to 1-20, the Test menu and T.1-T.22 descriptions", method="ocr", reviewed=False, credit="curator; Windows OCR of the renders, unedited"),
	]


RUNTIME_SOURCES = (
	(EDGES_SOURCE, "switch-edges-sweep", "One hash-pinned LibPinMAME harness run of sc_18s11 from empty NVRAM with built-in mechanisms disabled (tools/harness-scenarios/wpc-95/sc-switch-edges-sweep.json): inside T.1 SWITCH EDGES every public matrix address 11-88 and every Fliptronic address 111-118 is set to 1 and back to 0 for 2 s each. The ROM names each fitted switch at public 1 (24 and 43 on their 1 -> 0 edge; 23, 38, 87 and 88 as UNUSED; the synthesized end-of-stroke bits 111, 113 and 115 never), fires the jet and sling coils for their switches, the lower right flipper for 112, the lower left for 114 and both right flippers for 116, and names 118 TOKEN COIN SLOT."),
	(SOLENOID_TEST_SOURCE, "solenoid-test", "One hash-pinned run of sc_18s11 (sc-solenoid-test.json) stepping T.4 SOLENOID TEST: it walks 1-16, 25-28, 35 and 36, naming each driver and its wires and pulsing that public address, and wraps."),
	(FLASHER_TEST_SOURCE, "flasher-test", "One hash-pinned run of sc_18s11 (sc-flasher-test.json) stepping T.5 FLASHER TEST through 17-24, each named and pulsed."),
	(FLIPPER_TEST_SOURCE, "flipper-coil-test", "One hash-pinned run of sc_18s11 (sc-flipper-coil-test.json) stepping T.12 FLIPPER COIL TEST: R. FLIP. POWER drives 45 and 46, R. FLIP. HOLD 46, L. FLIP. POWER 47 and 48, L. FLIP. HOLD 48, U.R. FLIP. POWER 33 and 34, U.R. FLIP. HOLD 34."),
	(GI_TEST_SOURCE, "gi-test", "One hash-pinned run of sc_18s11 (sc-gi-test.json) stepping T.6 GENERAL ILLUMINATION: ALL ILLUMINATION dims public GI 0-2, ILLUM. STRING 1, AUX. LAMP 1 POWER and ILLUM. STRING 3 dim GI 0, 1 and 2 alone, and AUX. LAMP 2 and 3 POWER are ON ONLY; GI 3 and 4 stay on throughout."),
	(LAMP_TEST_SOURCE, "single-lamps", "One hash-pinned run of sc_18s11 (sc-single-lamps.json) stepping T.8 SINGLE LAMPS TEST through public lamps 11-88 and then 91-148, each lit alone and named; the auxiliary ones as the AUX P.C.B. lamps L24-L1 and L48-L25 with their lamp-power wire."),
	(MOVING_TARGET_SOURCE, "moving-target-test", "One hash-pinned run of sc_18s11 (sc-moving-target-test.json): T.16 MOVING TARGET TEST shows switches C (#56), B (#57) and A (#58) CLOSED at public 0 and OPEN at 1 with a decoded number, and Enter pulses solenoid 3."),
	(MOVING_TARGET_CODES_SOURCE, "moving-target-codes", "One hash-pinned run of sc_18s11 (sc-moving-target-codes.json): T.16 MOVING TARGET TEST reads 4 with public 56 and 57 at 1, 2 with 57 and 58, 6 with 56 and 58 and 5 with all three, completing the ROM's Gray-code decoding of the three optos."),
	(TOKEN_TEST_SOURCE, "token-test", "One hash-pinned run of sc_18s11 (sc-token-test.json): T.17 TOKEN TEST pulses 4 and 2 for each dispense."),
	(LIGHT_ROPE_SOURCE, "light-rope-test", "One hash-pinned run of sc_18s11 (sc-light-rope-test.json): T.18 LIGHT ROPE TEST flashes 23 for LIGHT ROPE 1, 24 for LIGHT ROPE 2 and both for BOTH."),
	(DROP_TARGET_SOURCE, "drop-target-test", "One hash-pinned run of sc_18s11 (sc-drop-target-test.json): T.19 DROP TARGET TEST names each bank's switches by position, flashes its lamps and fires its reset coil (LOWER LEFT 27, UPPER LEFT 15, UPPER RIGHT 16, LOWER RIGHT 28)."),
	(TOP_TROUGH_SOURCE, "top-trough-test", "One hash-pinned run of sc_18s11 (sc-top-trough-test.json): T.20 TOP TROUGH TEST shows the top popper 68 and TR1-11, TR2-12, TR3-77, pulses 6 while 68 is held and 5 while 77 is held."),
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
			"locator": "Pinned catalog driver records for the sc_* clone tree (sc_18s11 parent; sc_18n11, sc_18s2, sc_18ns2, sc_17, sc_17n, sc_14, sc_10, sc_091, sc_18pfx)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/sc.c (a preliminary simulator) scGameData: GEN_WPC95, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_UR) | "
				"FLIP_SOL(FLIP_L | FLIP_UR), lampCol 6, the inverted-switch mask {0x00,0x00,0x00,0x7f,0x06,0xe0,0x3f,0x3f,0x00,0x00,0x00,0x00} "
				"(public 31-37, 42, 43, 56-58, 61-66 and 71-76 under wpc_sw2m), sc_wpc_w driving six HC4094 registers from WPC_SOLENOID1 bits 4-7 "
				"(strobe, clock, data of chip 0, data of chip 3) into lamp columns 8-13, init_sc's wpc_set_fastflip_addr(0x86), the ROM set "
				"definitions and the percentaging note; src/wpc/wpc.c WPC_FLIPPERSW95 returning ~swMatrix[CORE_FLIPPERSWCOL] and the 29-31 "
				"state mirror; src/wpc/core.c core_getSol (37-40 mirrored at 41-44 on WPC-95) and core_updateSw (end-of-stroke synthesis). The "
				"runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-95.json", "revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp (including the six auxiliary columns 91-148) and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "revision": "Wayback capture, 2024",
			"sha256": IPDB_PAGE_SHA256, "acquired_at": ACQUIRED_AT,
			"locator": (
				"IPDB machine 3782 'Safe Cracker' (Midway Manufacturing Company, trade name Bally, March 1996, model 90003, Williams WPC-95, "
				f"1,148 units, payout machine). IPDB is Cloudflare-gated, so the page was read from the Wayback capture {IPDB_WAYBACK} "
				"(retained as ipdb3782.html). Its title, date and model number match the manual and the ROM's own identification (90003); its "
				"notes describe the backbox doors, the backglass board game and the token launcher with twenty tokens."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine 3782 page, title line to image list", reviewed=False, credit="curator, from the retained HTML")],
		},
		pdf(
			MANUAL_SOURCE, "manual", MANUAL_NAME,
			"Midway/Bally Safe Cracker operations manual: a 158-page scan without a text layer (Windows OCR used only to find pages). "
			"PDF 114-120 carry the matrices, the location lists and drawings (2-42 to 2-48), PDF 126-157 Section 3 wiring. Its test menu "
			"(T.16 Wheel Test, T.17 Vari Target Test) describes an earlier ROM than the 1.8 build the runs used.",
			MANUAL_SHA256, _manual_excerpts(),
		),
		pdf(
			BULLETIN_SOURCE, "service_bulletin", BULLETIN_NAME,
			"Service Bulletin 90 (May 24, 1996): intermittent token dispensing on games built between 5/2/96 and 5/20/96, fixed by "
			"replacing the stop brackets (04-10506) of both token-tube shuttle plunger assemblies. It changes no switch, lamp or solenoid.",
			BULLETIN_SHA256,
			[_excerpt("service-bulletin-90", "Whole document", method="ocr", reviewed=False, credit="curator; the PDF text layer, unedited")],
		),
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/bally/safe-cracker-1996/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine (fuzzel, flupper1, rothbauerw; table_version 1.0). Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry "
				f"authority only for named table objects. A second retained file, {MODIFIED_TABLE_NAME} (SHA-256 {MODIFIED_TABLE_SHA256}), "
				"is a modified copy of the same table with blanked credits and the same binding statements apart from a solenoid 26 "
				"callback; it is derived and not an independent table."
			),
			"license": "NOASSERTION", "attribution": "fuzzel, flupper1, rothbauerw (VP9 authors ICPjuggla, OldSkoolGamer and Herweh)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/safe-cracker-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded v1.0 script (2,763 lines). Runtime and mechanism-causality authority: cGameName = \"sc_18\" (the older set "
				"name of the same 1.8 game ROM), HandleMechanics = 0, the SolCallBack and SolModCallBack tables, the trough kickers, the "
				"vari-target and spin-disc switch code, the ChangedLamps/UpdateLamps lamp loop (including the board-game lamps 91-148) and "
				"the single consumed GI channel."
			),
			"license": "NOASSERTION", "attribution": "fuzzel, flupper1, rothbauerw", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_V2_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/{quote(SCRIPT_V2_PATH, safe='/')}",
			"revision": VPXTABLE_SCRIPTS_REVISION, "original_filename": SCRIPT_V2_PATH.rsplit('/', 1)[1], "sha256": SCRIPT_V2_SHA256, "known_working": True,
			"locator": (
				"The pinned script corpus's copy of UnclePaulie's v2.0.0 update of the same table (219,234 bytes; no table geometry retained). "
				"Used to compare bindings: cGameName = \"sc_18n11\", SolCallback(26) = \"SolRotateBeacons\", held rather than pulsed rollover "
				"levels, a one-hot vari-target code, switch 41 still 'mapped backwards', and bumper switches 44 and 46 swapped against v1.0."
			),
			"license": "NOASSERTION", "attribution": "UnclePaulie (update of the table by fuzzel, flupper1, rothbauerw)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/safe-cracker-1996/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained v1.0 table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	] + [
		{
			"id": source_id, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/safe-cracker-sc_18s11-{name}.json",
			"revision": PINMAME_REVISION, "locator": locator, "license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		}
		for source_id, name, locator in RUNTIME_SOURCES
	] + [
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/bally/safe-cracker-1996-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of the manual's switch drawing 2-43 and solenoid/flasher drawing 2-45 (the "
				"committed 300 dpi excerpt crops): every callout transcribed by an independent reader working only from the page, per-page "
				"control fits from the jet bumper caps and flipper pivots, and the callout fit; a table placement whose own callout lands "
				"within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and generators are retained "
				"under review-artifacts with a pinned manifest."
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
			"name": "Safe Cracker",
			"manufacturer": "Bally",
			"year": 1996,
			"kind": "physical_pinball",
			"model_number": "90003",
			"ipdb_id": 3782,
			"opdb_id": "GRBxq-MJpOP",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["mechanism_behavior", "spatial_placement"],
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
		"knowledge": {"path": "knowledge/bally/safe-cracker-1996.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Safe Cracker device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Safe Cracker mechanism {mechanism['id']} names unknown devices: {unknown}")
	seed = load_json(CALLOUT_SEED_PATH)
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
			"manifest_uri": "external:pinmame-vpx-sources/bally/safe-cracker-1996/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/bally/safe-cracker-1996-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "The retained table's object for the switch (trigger, target, kicker, bumper or slingshot wall), chosen by what the script binds, observed and validated where the switch drawing's own callout agrees. The trough optos 31-35 are the trough slot kickers; the lock optos 36/37 are projected onto the hidden lock trigger that writes them; the moving-target optos 56-58 onto the target's pivot and the spin-disc optos 85/86 onto the disc centre, because the table derives those switches from the mechanism's motion.",
			"lamp": "The script-bound Light's own centre (for 27 and 28 the crossed lights the script binds), the bumper-cap lights for 81-83 and the world-space mesh centres of the baked lamp primitives for 84-87; observed only, because the lamp drawing is a symbol diagram with no flipper or other mechanism feature a control fit can use. The 48 backbox lamps are not applicable (backbox).",
			"solenoid": "The object the solenoid callback moves (kicker, flipper, plunger, lock pin, diverter pivot, moving target) or, for the slingshots and jet bumpers, the object that fires the coil, the middle target of each drop bank for its reset coil, and the Flupper dome base each flasher callback lights (two bulbs for 18); validated where the solenoid drawing's callout agrees.",
			"gi": "None: the retained table drives all its GI bulbs from public GI 0 and has no consumer for the other strings, so it cannot tell string 1's bulbs from string 3's, and no retained drawing or count locates GI bulbs. Strings 2, 4 and 5 power the backbox lamps only and are not applicable.",
		},
		"unresolved_geometry": [
			"General illumination strings 1 and 3 (public GI 0 and 2) light #44 playfield bulbs, but neither the retained table nor any retained drawing or count says which bulb belongs to which string, so they have no placement.",
			"The left big kick opto (switch 42) has no table object: the v1.0 script's VariTargetTimer_Timer derives it from a ball-position rectangle (raw 50,1005 to 100,1055; the v2.0.0 script uses 50,990 to 110,1055) around the LeftKickBack kicker, a script surrogate rather than the opto, so it has no placement. The switch drawing's callout 42 marks it at the left kickback lane; placing it from the drawing needs a reproducible measurement under the spatial measurement rule.",
			"The lamp drawing (2-47) cannot validate lamp placements: it shows lamp symbols in an outline with no flippers or other mechanism feature for an independent control fit, so every lamp placement stays observed.",
			"Placements the switch and solenoid drawings do not confirm keep their observed status; the drawing callout check lists them with the distance or reason.",
		],
		"promotion_decision": "partial: every fitted playfield device has an observed or validated placement or a controlled not-applicable record except the general-illumination strings 1 and 3, whose bulbs no retained source assigns to a string, and the left big kick opto (switch 42), which the retained table only synthesises from a ball-position rectangle.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	lines = [
		"# Safe Cracker (Bally, 1996) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places.",
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
		raise RuntimeError(f"Refusing to overwrite an author-ready Safe Cracker artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Safe Cracker author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Safe Cracker deterministic artifact drift: {path}")
	print("Safe Cracker definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Safe Cracker extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Safe Cracker retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
