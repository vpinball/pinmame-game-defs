"""Curate the physical Williams The Machine: Bride of Pinbot (1991) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail, runtime
observation, and normalized coordinate is a literal here, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed, and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.the-machine-bride-of-pinbot.1991"
PARTIAL_PATH = ROOT / "machines/partial/williams/the-machine-bride-of-pinbot-1991.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/the-machine-bride-of-pinbot-1991.json"
STATUS = "author_ready"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/the-machine-bride-of-pinbot-1991.json"
KNOWLEDGE_PATH = "knowledge/williams/the-machine-bride-of-pinbot-1991.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/the-machine-bride-of-pinbot-1991.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/the-machine-bride-of-pinbot-1991.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = "evidence/runtime/wpc-alpha/bride-of-pinbot-head-helmet-and-service-names.json"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-alpha"
MANUAL_SOURCE = "manual.williams.the-machine-bride-of-pinbot.1991"
RUNTIME_SOURCE = "runtime.bride-of-pinbot.head-helmet-and-service-names"
VPX_TABLE_SOURCE = "vpx-table.bop-vpw-1-0-3"
VPX_SCRIPT_SOURCE = "vpx-script.bop-vpw-1-0-3"
VPX_EXTRACTION_SOURCE = "vpx-extraction.bop-vpw-1-0-3"
VPX_ALT_TABLE_SOURCE = "vpx-table.bop-vp10-rev-2-0"

MANUAL_SHA256 = "28b580b38af835cc8efa100d0b44f504684dce756ea7079ca9a042f34aa5c3b9"
TABLE_SHA256 = "041c49cff7ff206f570fbac4cfad01d075c8f2c6d8a09f27cdf78c68b3a60270"
SCRIPT_SHA256 = "b7624ad6d6f7cc807d55c2d83748239d7847a31f52d2314ebc1f318b55a4a3a7"
EXTRACTION_RELATIVE_PATH = Path("williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "4090ee6bb9a55da0dc8aff6c6fecf92150e9aa0187ffe51b16f0a7e728749fd2"
EXTRACTION_FILE_COUNT = 4084
EXTRACTION_TOTAL_BYTES = 300991426
TABLE_WIDTH = 952.0
TABLE_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

# --- Driver tree -----------------------------------------------------------------------------
DRIVER_IDS = (
	"bop_l7", "bop_d7", "bop_l8", "bop_d8", "bop_l6", "bop_d6", "bop_l5", "bop_d5",
	"bop_l4", "bop_d4", "bop_l3", "bop_d3", "bop_l2", "bop_d2",
)
_SHARED = (
	"Declared with CORE_CLONEDEF against bop_l7 on the same wpc_mAlpha2S machine driver, so it runs the one "
	"static bopGameData (GEN_WPCALPHA_2, wpc_dispAlpha, FLIP_SWNO(12,11), two extra lamp columns) and "
	"init_bop; no controller-address or playfield change."
)
DRIVER_COMPATIBILITY = {
	"bop_l7": ("identical", "Williams L-7 production game ROM (tmbopl_7.rom, 0x40000 bytes), the clone-tree parent and the driver the retained known-working script binds (cGameName = \"bop_l7\"). Pinned bop_handleMech special-cases this exact driver name: when a host sets HandleMechanics to -1 or -2 it writes 0x01 to wpc_ram[0x1fc9], the game's stored head-face byte, so the ROM's remembered face agrees with a table whose head starts on face 1. No other bop driver receives that reset."),
	"bop_d7": ("identical", f"D-7 game ROM, an LED ghost-fix build of L-7 (0x40000 bytes). {_SHARED} The wpc_ram[0x1fc9] head-face reset in bop_handleMech is keyed to the driver name bop_l7 and does not run for this clone."),
	"bop_l8": ("identical", f"L-8 game ROM, described by pinned PinMAME as a billionaire multiplayer patch of L-7 (0x40000 bytes); it runs on the unchanged physical machine. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d8": ("identical", f"D-8 game ROM, the LED ghost-fix build of the L-8 patch (0x40000 bytes). {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_l6": ("identical", f"L-6 game ROM (0x20000 bytes). {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d6": ("identical", f"D-6 LED ghost-fix build of L-6. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_l5": ("identical", f"L-5 game ROM. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d5": ("identical", f"D-5 LED ghost-fix build of L-5. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_l4": ("identical", f"L-4 game ROM. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d4": ("identical", f"D-4 LED ghost-fix build of L-4. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_l3": ("identical", f"L-3 game ROM (bop_l3.u6). {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d3": ("identical", f"D-3 LED ghost-fix build of L-3. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_l2": ("identical", f"L-2 game ROM (bop_l2.u6), the earliest revision retained by PinMAME. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
	"bop_d2": ("identical", f"D-2 LED ghost-fix build of L-2. {_SHARED} The bop_l7-only head-face reset does not run for this clone."),
}

# --- Switches (manual printed 2-40 matrix, 2-41 locations; ROM T.1 switch-edge names) ------------
SWITCH_LABELS = {
	11: "Right Flipper", 12: "Left Flipper", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Outlane", 16: "Left Flipper Lane", 17: "Right Flipper Lane", 18: "Right Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed",
	25: "Right Trough", 26: "Center Trough", 27: "Left Trough", 28: "Left Standup",
	31: "Skill Shot 50K", 32: "Skill Shot 75K", 33: "Skill Shot 100K", 34: "Skill Shot 200K",
	35: "Skill Shot 25K", 36: "Right Top Standup", 37: "Right Bottom Standup", 38: "Outhole",
	41: "Right Ramp Made", 43: "Left Loop", 44: "Right Loop Top", 45: "Right Loop Bottom",
	46: "Under Playfield Kicker", 47: "Enter Head",
	51: "Spinner", 52: "Shooter Lane Feeder", 53: "Upper Right Jet Bumper", 54: "Upper Left Jet Bumper",
	55: "Lower Jet Bumper", 56: "Jet Bumper Sling", 57: "Left Slingshot", 58: "Right Slingshot",
	63: "Head Left Eye", 64: "Head Right Eye", 65: "Head Mouth", 67: "Face Position",
	71: "Wireform Top", 72: "Wireform Bottom", 73: "Enter Mini Playfield", 74: "Mini Exit Left",
	75: "Mini Exit Right", 76: "Left Ramp Enter", 77: "Right Ramp Enter",
}
# Printed "Not Used" on both switch pages (and named NOT USED by the ROM's switch-edge test).
PRINTED_NOT_USED = {42, 48, 61, 62, 66, 68, 78}
# Column 8 cells carry an address number but no description; the locations list stops at 78.
BLANK_COLUMN_8 = set(range(81, 89))
SWITCH_PARTS = {
	11: "A-9990-1", 12: "A-9990-1", 13: "SW-1A-126", 14: "20-6502-A",
	15: "5647-12693-19", 16: "5647-12693-19", 17: "5647-12693-19", 18: "5647-12693-19",
	21: "27-1066", 22: "A-8630", 24: "A-8630",
	25: "5647-12693-08", 26: "5647-09957-00", 27: "5647-09957-00", 28: "B-11854-4",
	31: "5647-12693-46", 32: "5647-12693-19", 33: "5647-12693-19", 34: "5647-12693-19", 35: "5647-12693-19",
	36: "B-11854-4", 37: "B-11854-4", 38: "5647-12133-12",
	41: "5647-12693-21", 43: "5647-12693-19", 44: "5647-12693-18", 45: "5647-12693-18",
	46: "5647-12693-25", 47: "5647-12693-36",
	51: "5647-12133-08", 52: "5647-12693-04", 53: "SW-11A-37", 54: "SW-11A-37", 55: "SW-11A-37",
	56: "SW-1A-114", 57: "SW-1A-114", 58: "SW-1A-114",
	63: "5647-12693-47", 64: "5647-12693-48", 65: "5647-12693-39", 67: "5647-12693-06",
	71: "5647-12693-21", 72: "5647-12693-21", 73: "5647-12693-36", 74: "5647-12693-36",
	75: "5647-12693-21", 76: "5647-12693-36", 77: "5647-12693-21",
}
# ROM T.1 switch-edge names (bop_l7), recorded verbatim from the alphanumeric display.
ROM_SWITCH_NAMES = {
	13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "LEFT OUTLANE", 16: "L. FLIPPER LANE",
	17: "R. FLIPPER LANE", 18: "RIGHT OUTLANE", 21: "SLAM TILT", 23: "TICKET OPTO", 25: "RIGHT TROUGH",
	26: "CENTER TROUGH", 27: "LEFT TROUGH", 28: "LEFT STANDUP", 31: "SKILL SHOT 50K", 32: "SKILL SHOT 75K",
	33: "SKILL SHOT 100K", 34: "SKILL SHOT 200K", 35: "SKILL SHOT 25K", 36: "RGHT TOP STANDUP",
	37: "RGHT BOT STANDUP", 38: "OUTHOLE", 41: "RIGHT RAMP MADE", 43: "LEFT LOOP", 44: "RIGHT LOOP TOP",
	45: "RIGHT LOOP BOT", 46: "UNDER PLAY KICK", 47: "ENTER HEAD", 51: "SPINNER", 52: "SHOOTER",
	53: "U.R. JET BUMPER", 54: "U.L. JET BUMPER", 55: "LOWER JET BUMPER", 56: "JET BUMPER SLING",
	57: "LEFT SLINGSHOT", 58: "RIGHT SLINGSHOT", 63: "HEAD LEFT EYE", 64: "HEAD RIGHT EYE", 65: "HEAD MOUTH",
	71: "WIREFORM TOP", 72: "WIREFORM BOTTOM", 73: "ENTER MINI PLYFD", 74: "MINI EXIT LEFT",
	75: "MINI EXIT RIGHT", 76: "LEFT RAMP ENTER", 77: "RGT RAMP ENTER",
}
MICROSWITCH_PART_PREFIX = "5647-12693-"
SWITCH_COLUMN_WIRES = {1: "Green-Brown", 2: "Green-Red", 3: "Green-Orange", 4: "Green-Yellow", 5: "Green-Black", 6: "Green-Blue", 7: "Green-Violet", 8: "Green-Gray"}
SWITCH_ROW_WIRES = {1: "White-Brown", 2: "White-Red", 3: "White-Orange", 4: "White-Yellow", 5: "White-Green", 6: "White-Blue", 7: "White-Violet", 8: "White-Gray"}
DEDICATED_SWITCHES = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Orange-Brown", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Orange-Red", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Orange-Black", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Orange-Yellow", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Orange-Green", "Normal function Service Credits; test function Escape."),
	6: ("Volume Down / Down", "service.down", "Orange-Blue", "Normal function Volume Down; test function Down."),
	7: ("Volume Up / Up", "service.up", "Orange-Violet", "Normal function Volume Up; test function Up."),
	8: ("Begin Test / Enter", "service.enter", "Orange-Gray", "Normal function Begin Test; test function Enter."),
}

# --- Solenoids (manual printed 2-42 table and front-matter copy, 2-43 locations) ----------------
SOLENOID_LABELS = {
	1: "Outhole", 2: "Ball Release", 3: "Under Playfield Kicker", 4: "Controlled Gate",
	5: "Skill Shot Kicker", 6: "Wire Ball Holder", 7: "Knocker", 8: "Head Mouth Kicker",
	9: "Upper Left Jet Bumper", 10: "Left Slingshot", 11: "Upper Right Jet Bumper", 12: "Right Slingshot",
	13: "Lower Jet Bumper", 14: "Jets Sling", 15: "Head Left Eye Kicker", 16: "Head Right Eye Kicker",
	17: "Billion Flasher", 18: "Left Ramp Flasher", 19: "Jackpot Flasher", 20: "Skill Shot Flasher",
	21: "Left Helmet Flasher", 22: "Right Helmet Flasher", 23: "Jets Enter Flasher", 24: "Left Loop Flasher",
	25: "Helmet Lights Data", 26: "Helmet Lights Clock", 27: "Head Motor Relay", 28: "Head Motor",
}
SOLENOID_PRINTED = {
	1: "Outhole", 2: "Ball Realease", 3: "Under Playfield Kicker", 4: "Controlled Gate", 5: "Skill Shot Kicker",
	6: "Wire Ball Holder", 7: "Knocker", 8: "Head Mouth", 9: "Upper Left Jet Bumper", 10: "Left (sling) Kicker",
	11: "Upper Right Jet Bumper", 12: "Right (sling) Kicker", 13: "Lower Jet Bumper", 14: "Jets Sling",
	15: "Head - Left Eye", 16: "Head - Right Eye", 17: "Billion Flasher", 18: "Left Ramp Flash",
	19: "Jackpot Flasher", 20: "Skill Shot Flasher", 21: "Left Helmet Flasher", 22: "Right Helmet Flasher",
	23: "Jets Enter Flash", 24: "Left Loop Flash", 25: "Helmet Lights Data Port", 26: "Helmet Light Clock Port",
	27: "Motor Relay", 28: "Head Motor",
}
SOLENOID_WIRING = {
	1: ("High Power", "Vio-Brn", "J130-1", "Q82", "AE-27-1200"),
	2: ("High Power", "Vio-Red", "J130-2", "Q80", "AE-26-1200"),
	3: ("High Power", "Vio-Orn", "J130-4", "Q78", "AE-23-800"),
	4: ("High Power", "Vio-Yel", "J130-5", "Q76", "A-14406"),
	5: ("High Power", "Vio-Grn", "J130-6", "Q64", "AE-24-900"),
	6: ("High Power", "Vio-Blu", "J130-7", "Q66", "AE-26-1200"),
	7: ("High Power", "Vio-Blk", "J130-8", "Q68", "AE-23-800"),
	8: ("High Power", "Vio-Gry", "J130-9", "Q70", "AE-30-2000"),
	9: ("Low Power", "Brn-Blk", "J127-1", "Q58", "AE-26-1200"),
	10: ("Low Power", "Brn-Red", "J127-3", "Q56", "AE-26-1500"),
	11: ("Low Power", "Brn-Orn", "J127-4", "Q54", "AE-26-1200"),
	12: ("Low Power", "Brn-Yel", "J127-5", "Q52", "AE-26-1500"),
	13: ("Low Power", "Brn-Grn", "J127-6", "Q50", "AE-26-1200"),
	14: ("Low Power", "Brn-Blu", "J127-7", "Q48", "AE-26-1500"),
	15: ("Low Power", "Brn-Vio", "J127-8", "Q46", "AE-30-2000"),
	16: ("Low Power", "Brn-Gry", "J127-9", "Q44", "AE-30-2000"),
	17: ("Flasher", "Blk-Brn", "J125-1", "Q42", None),
	18: ("Flasher", "Blk-Red", "J126-2 / J125-2", "Q40", None),
	19: ("Flasher", "Blk-Orn", "J126-3 / J125-3", "Q38", None),
	20: ("Flasher", "Blk-Yel", "J126-4", "Q36", None),
	21: ("Flasher", "Blu-Grn", "J126-6 / J125-6", "Q28", None),
	22: ("Flasher", "Blu-Blk", "J126-7 / J125-7", "Q30", None),
	23: ("Flasher", "Blu-Vio", "J126-8 / J125-8", "Q34", None),
	24: ("Flasher", "Blu-Gry", "J126-9 / J125-9", "Q32", None),
	25: ("Special", "Blu-Brn", "J122-1", "Q26", None),
	26: ("Special", "Blu-Red", "J122-2", "Q24", None),
	27: ("Special", "Blu-Orn", "J122-3", "Q22", "A-14423-1"),
	28: ("Special", "Blu-Yel", "J122-4", "Q20", "A-14119"),
}
# Flashlamp complement: playfield bulb plus, where printed, one #906 insert bulb in the backbox.
FLASHERS_WITH_INSERT = {18, 19, 21, 22, 23, 24}
FLASHERS_PLAYFIELD_ONLY = {17, 20}
SOLENOID_CALLBACKS = {
	1: "kisort (Drain.Kick, clears switch 38)", 2: "KickBallToLane (ballrelease.Kick)", 3: "SolKickout (sw46k.kick)",
	4: "SolGate3 (vpmSolGate Gate3)", 5: "Solss (plungerIM.AutoFire, SSkick arm)", 6: "solBallLockPost (drops and raises the BL post wall)",
	7: "KnockerSolenoid", 8: "KickMouth (clears switch 65)", 15: "KickLeftEye (clears switch 63)", 16: "KickRightEye (clears switch 64)",
	17: "SolModCallBack ModLampz.SetModLamp 17 (f117, LB117)", 18: "SolModCallBack ModFlashLR (f118 and the F118 side flashers)",
	19: "SolModCallBack ModFlashJP (f119, LB119)", 20: "SolModCallBack ModFlashSK (f120)",
	21: "SolModCallBack SetRedDome1 (Flasherbase1 dome)", 22: "SolModCallBack SetRedDome2 (Flasherbase2 dome)",
	23: "SolModCallBack SetRedDome4 (Flasherbase4 dome)", 24: "SolModCallBack SetRedDome3 (Flasherbase3 dome)",
	27: "cvpmMyMech Sol2 (direction) of the head mech", 28: "cvpmMyMech Sol1 (drive) of the head mech",
}
ROM_SOLENOID_NAMES = {
	1: "OUTHOLE", 2: "BALL RELEASE", 3: "UNDERPLAY KICKER", 4: "CONTROLLED GATE", 5: "SKILL SHOT KICKR",
	6: "WIRE BALL HOLDER", 7: "KNOCKER", 9: "U.L. JET BUMPER", 10: "LEFT SLINGSHOT", 11: "U.R. JET BUMPER",
	12: "RIGHT SLINGSHOT", 13: "LOWER JET BUMPER", 14: "JET BUMPER SLING", 27: "MOTOR RELAY",
	17: "BILLION", 18: "LEFT RAMP", 19: "JACKPOT", 20: "SKILL SHOT", 21: "LEFT HELMET", 22: "RIGHT HELMET",
	23: "JETS ENTRANCE", 24: "LEFT LOOP",
	8: "HEAD MOUTH", 15: "HEAD LEFT EYE", 16: "HEAD RIGHT EYE",
}

# --- Lamps (manual printed 2-38 matrix, 2-39 locations; ROM T.8 single-lamp names) --------------
LAMP_LABELS = {
	11: "Left Outlane", 12: "Left Return Lane", 13: "Right Return Lane", 14: "Right Outlane",
	15: "Left Standup", 16: "Right Top Standup", 17: "Right Bottom Standup", 18: "Shoot Again",
	21: "Circle Lite Jackpot", 22: "Circle Lite Billion", 23: "Circle Extra Ball", 24: "Circle Lite Extra Ball",
	25: "Circle 50K", 26: "Circle 100K", 27: "Values Doubled", 28: "Spin Small Wheel",
	31: "Circle 250K", 32: "Circle 10 Million", 33: "Circle 50 Million", 34: "Circle Special",
	35: "Circle 5 Million", 36: "Circle 1 Million", 37: "Space Shuttle", 38: "Launch Pad",
	41: "Skill Shot 50K", 42: "Skill Shot 75K", 43: "Skill Shot 100K", 44: "Skill Shot 200K",
	45: "Skill Shot 25K", 46: "Head Left Eye", 47: "Head Right Eye", 48: "Head Mouth",
	51: "Left Loop 500K", 52: "Left Loop 100K", 53: "Left Loop 50K", 54: "Left Loop 25K",
	55: "Right Loop 500K", 56: "Right Loop 100K", 57: "Right Loop 50K", 58: "Right Loop 25K",
	61: "Right Ramp Million", 62: "Right Ramp 500K", 63: "Right Ramp 100K", 64: "Wire Ball Lock",
	65: "Jets Enter 500K", 66: "Jets Enter 100K", 67: "Jets Enter 50K", 68: "Jets Enter 25K",
	71: "Jackpot 8 Million", 72: "Jackpot 7 Million", 73: "Jackpot 6 Million", 74: "Jackpot 5 Million",
	75: "Jackpot 4 Million", 76: "Jackpot 3 Million", 77: "Jackpot 2 Million", 78: "Jackpot 1 Million",
	81: "Backglass Hip", 82: "Backglass Middle Leg", 83: "Backglass Knee", 84: "Backglass Foot",
	85: "Backglass Shoulder", 86: "Mini Playfield 100K", 87: "Mini Playfield 200K", 88: "Mini Playfield 300K",
}
LAMP_BULB_44 = {18, 37, 38, 64}
BACKBOX_INSERT_LAMPS = set(range(71, 79)) | set(range(81, 86))
LAMP_COLUMN_WIRES = {1: ("Yellow-Brown", "J137-1"), 2: ("Yellow-Red", "J137-2"), 3: ("Yellow-Orange", "J137-3"), 4: ("Yellow-Black", "J137-4"), 5: ("Yellow-Green", "J137-5"), 6: ("Yellow-Blue", "J137-6"), 7: ("Yellow-Violet", "J137-7"), 8: ("Yellow-Gray", "J137-8")}
LAMP_ROW_WIRES = {1: ("Red-Brown", "J133-1"), 2: ("Red-Black", "J133-2"), 3: ("Red-Orange", "J133-3"), 4: ("Red-Yellow", "J133-5"), 5: ("Red-Green", "J133-6"), 6: ("Red-Blue", "J133-7"), 7: ("Red-Violet", "J133-8"), 8: ("Red-Gray", "J133-9")}
ROM_LAMP_NAMES = {
	11: "LEFT OUTLANE", 12: "LEFT RETURN LANE", 13: "RGHT RETURN LANE", 14: "RIGHT OUTLANE", 15: "LEFT STANDUP",
	16: "RGHT TOP STANDUP", 17: "RGHT BOT STANDUP", 18: "SHOOT AGAIN", 25: "CIRCLE 50K", 26: "CIRCLE 100K",
	27: "VALUES DOUBLED", 28: "SPIN SMALL WHEEL", 31: "CIRCLE 250K", 37: "SPACE SHUTTLE", 38: "LAUNCH PAD",
	61: "RIGHT RAMP MILL", 62: "RIGHT RAMP 500K", 63: "RIGHT RAMP 100K", 64: "WIRE BALL LOCK", 81: "BACKGLS HIP", 85: "BACKGLS SHOULDER", 86: "MINI PLYFLD 100K",
	87: "MINI PLYFLD 200K", 88: "MINI PLYFLD 300K",
}
# Helmet chase lamps: public address in the ROM's T.17 single-lamp order. The manual says the first
# lamp is the lower-left one and Up moves clockwise; the ROM starts on 108 and Up steps 107...101,
# 98...91 and back to 108.
HELMET_CLOCKWISE_FROM_LOWER_LEFT = (108, 107, 106, 105, 104, 103, 102, 101, 98, 97, 96, 95, 94, 93, 92, 91)
# The retained table's sixteen helmet bulb objects in clockwise order from the lower-left socket
# (its own names l91 ... l98, l101 ... l108 run the opposite way round from the ROM's order).
HELMET_SOCKETS_CLOCKWISE = (
	("l91", (0.25897, 0.294062)), ("l92", (0.258824, 0.269612)), ("l93", (0.259158, 0.246326)),
	("l94", (0.259037, 0.221928)), ("l95", (0.259888, 0.200382)), ("l96", (0.263594, 0.178929)),
	("l97", (0.285042, 0.159913)), ("l98", (0.336704, 0.149807)), ("l101", (0.507389, 0.150123)),
	("l102", (0.558527, 0.160006)), ("l103", (0.578951, 0.179023)), ("l104", (0.582691, 0.20064)),
	("l105", (0.583542, 0.22228)), ("l106", (0.58333, 0.246356)), ("l107", (0.583755, 0.269682)),
	("l108", (0.583688, 0.293945)),
)

# --- Normalized playfield coordinates from the retained VPX extraction (x/952, y/2162) --------
SWITCH_POSITIONS = {
	15: ("sw15", (0.060991, 0.754505)), 16: ("sw16", (0.131847, 0.740759)),
	17: ("sw17", (0.77915, 0.741833)), 18: ("sw18", (0.851045, 0.75551)),
	25: ("ballrelease", (0.864531, 0.872343)), 26: ("sw26", (0.8092, 0.886962)), 27: ("sw27", (0.748336, 0.902555)),
	28: ("pSW28", (0.123084, 0.609972)),
	31: ("sw31", (0.94102, 0.560298)), 32: ("sw32", (0.940185, 0.499434)), 33: ("sw33", (0.940439, 0.44559)),
	34: ("sw34", (0.939766, 0.390977)), 35: ("sw35", (0.939548, 0.336677)),
	36: ("pSW36", (0.744232, 0.580398)), 37: ("pSW37", (0.757272, 0.601084)), 38: ("Drain", (0.49872, 0.963105)),
	41: ("sw41", (0.764505, 0.360576)), 43: ("sw43", (0.14596, 0.334433)), 44: ("sw44", (0.847824, 0.375557)),
	45: ("sw45", (0.849938, 0.590612)), 46: ("sw46k", (0.076635, 0.309209)), 47: ("sw47", (0.419172, 0.138132)),
	51: ("sw51", (0.63645, 0.395256)), 52: ("sw52", (0.943289, 0.892104)),
	53: ("Bumper2", (0.895641, 0.125361)), 54: ("Bumper1", (0.690334, 0.141046)), 55: ("Bumper3", (0.824944, 0.211535)),
	56: ("SLINGU", (0.806002, 0.294809)), 57: ("SLING2", (0.210763, 0.735063)), 58: ("SLING1", (0.700447, 0.735897)),
	63: ("sw63x", (0.373736, 0.193591)), 64: ("sw64x", (0.469571, 0.193679)), 65: ("sw65x", (0.421941, 0.242163)),
	67: ("Face", (0.421729, 0.207557)),
	71: ("sw71", (0.41121, 0.359301)), 72: ("sw72", (0.411592, 0.384382)), 73: ("sw73", (0.682707, 0.074153)),
	74: ("sw74", (0.761337, 0.292994)), 75: ("sw75", (0.854406, 0.342235)), 76: ("sw76", (0.154378, 0.390067)),
	77: ("sw77", (0.463356, 0.382468)),
}
SOLENOID_POSITIONS = {
	1: ("Drain", [(0.49872, 0.963105)]), 2: ("ballrelease", [(0.864531, 0.872343)]),
	3: ("sw46k", [(0.076635, 0.309209)]), 4: ("Gate3", [(0.545882, 0.063605)]),
	5: ("SSkick", [(0.946403, 0.585773)]), 6: ("BL", [(0.411475, 0.398834)]),
	8: ("TWKicker1", [(0.42161, 0.241885)]), 9: ("Bumper1", [(0.690334, 0.141046)]),
	10: ("SLING2", [(0.210763, 0.735063)]), 11: ("Bumper2", [(0.895641, 0.125361)]),
	12: ("SLING1", [(0.700447, 0.735897)]), 13: ("Bumper3", [(0.824944, 0.211535)]),
	14: ("SLINGU", [(0.806002, 0.294809)]), 15: ("TWKicker2", [(0.374089, 0.193892)]),
	16: ("TWKicker3", [(0.470358, 0.193617)]),
	17: ("f117", [(0.461921, 0.542295)]), 18: ("f118", [(0.182658, 0.397893)]),
	19: ("f119", [(0.087959, 0.484336)]), 20: ("f120", [(0.941459, 0.625228)]),
	21: ("Flasherbase1", [(0.194517, 0.235942)]), 22: ("Flasherbase2", [(0.647048, 0.237336)]),
	23: ("Flasherbase4", [(0.539124, 0.425744)]), 24: ("Flasherbase3", [(0.282305, 0.423305)]),
	28: ("Face", [(0.421729, 0.207557)]),
}
LAMP_POSITIONS = {
	11: (0.061461, 0.696932), 12: (0.132982, 0.682848), 13: (0.777076, 0.684685), 14: (0.849128, 0.698395),
	15: (0.165091, 0.611405), 16: (0.706859, 0.58387), 17: (0.721151, 0.607332), 18: (0.458692, 0.85806),
	21: (0.45685, 0.620761), 22: (0.45723, 0.589734), 23: (0.526003, 0.672375), 24: (0.45586, 0.690381),
	25: (0.388107, 0.67362), 26: (0.38721, 0.636751), 27: (0.456301, 0.65535), 28: (0.125521, 0.529758),
	31: (0.525093, 0.636578), 32: (0.583286, 0.622275), 33: (0.584245, 0.688098), 34: (0.45649, 0.721128),
	35: (0.329658, 0.688063), 36: (0.326198, 0.622579), 37: (0.246901, 0.546074), 38: (0.267819, 0.580495),
	41: (0.886883, 0.53334), 42: (0.887509, 0.476156), 43: (0.886122, 0.42281), 44: (0.886274, 0.368117),
	45: (0.887187, 0.314801), 46: (0.374055, 0.177294), 47: (0.469863, 0.177207), 48: (0.421526, 0.226769),
	51: (0.352337, 0.455117), 52: (0.353009, 0.482594), 53: (0.356702, 0.507574), 54: (0.359877, 0.532017),
	55: (0.72789, 0.462681), 56: (0.708454, 0.498376), 57: (0.696542, 0.521802), 58: (0.686074, 0.545565),
	61: (0.465105, 0.495074), 62: (0.465591, 0.461362), 63: (0.466604, 0.436274), 64: (0.349988, 0.372951),
	65: (0.604814, 0.459626), 66: (0.595056, 0.48654), 67: (0.586435, 0.510969), 68: (0.575113, 0.534438),
	86: (0.739664, 0.048231), 87: (0.836236, 0.048468), 88: (0.935665, 0.048674),
}
LAMP_POSITION_OBJECTS = {address: f"l{address}" for address in LAMP_POSITIONS}
LAMP_POSITION_OBJECTS.update({86: "F86", 87: "F87", 88: "F88"})
# G.I. strings: smallest-radius named light in each co-located cluster of the retained collections.
GI_REAR_POSITIONS = [
	("GI026", (0.236417, 0.351897)), ("GI028", (0.393108, 0.336208)), ("GI030", (0.556594, 0.352737)),
	("GI034", (0.79465, 0.381178)), ("GI032", (0.702302, 0.416205)), ("GI024", (0.795027, 0.469036)),
	("l001", (0.690097, 0.140883)), ("l002", (0.895167, 0.125294)), ("l003", (0.824916, 0.211775)),
]
GI_FRONT_POSITIONS = [
	("GI022", (0.795028, 0.558478)), ("GI016", (0.725825, 0.704517)), ("GI014", (0.694736, 0.762315)),
	("GI012", (0.759439, 0.804327)), ("GI006", (0.151231, 0.803923)), ("GI002", (0.215873, 0.76187)),
	("GI004", (0.184117, 0.70427)), ("GI018", (0.063566, 0.624548)), ("GI020", (0.061625, 0.552954)),
]


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Bride of Pinbot retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Bride of Pinbot extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Bride of Pinbot retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Bride of Pinbot retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Bride of Pinbot retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*source_refs)})
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


EXCERPTS = (
	("switch-matrix", "PDF page 108, printed 2-40, THE MACHINE Switch Matrix", "the_machine_operations_manual.pdf page 108, crop box 0.098,0.455,0.961,0.955, scanned page rendered at its native resolution (embedded image xref 512, 2550px across 8.50in), rendered at 164 dpi, capped to 1200px wide, grayscale, 1201x901 WebP quality 80"),
	("switch-locations", "PDF page 109, printed 2-41, THE MACHINE SWITCH LOCATIONS list and drawing", "the_machine_operations_manual.pdf page 109, crop box 0.11,0.127,0.482,0.833, scanned page rendered at its native resolution (embedded image xref 515, 2550px across 8.50in), rendered at 158 dpi, capped to 500px wide, grayscale, 501x1229 WebP quality 80"),
	("lamp-matrix", "PDF page 106, printed 2-38, THE MACHINE Lamp Matrix", "the_machine_operations_manual.pdf page 106, crop box 0.149,0.46,0.863,0.91, scanned page rendered at its native resolution (embedded image xref 506, 2550px across 8.50in), rendered at 165 dpi, capped to 1000px wide, grayscale, 1001x817 WebP quality 80"),
	("lamp-locations", "PDF page 107, printed 2-39, THE MACHINE LAMP LOCATIONS list and drawing", "the_machine_operations_manual.pdf page 107, crop box 0.059,0.07,0.392,0.927, scanned page rendered at its native resolution (embedded image xref 509, 2550px across 8.50in), rendered at 148 dpi, capped to 420px wide, grayscale, 421x1400 WebP quality 80"),
	("solenoid-table", "PDF pages 110 (printed 2-42) and 2 (front matter), THE MACHINE Solenoid Table and Jumper Chart", "the_machine_operations_manual.pdf page 110, crop box 0.102,0.152,0.875,0.697, scanned page rendered at its native resolution (embedded image xref 518, 2550px across 8.50in), rendered at 107 dpi, capped to 700px wide, grayscale, 701x639 WebP quality 80"),
	("solenoid-locations", "PDF page 111, printed 2-43, THE MACHINE SOLENOID LOCATIONS list and drawing", "the_machine_operations_manual.pdf page 111, crop box 0.1,0.135,0.47,0.5, scanned page rendered at its native resolution (embedded image xref 521, 2550px across 8.50in), rendered at 207 dpi, capped to 650px wide, grayscale, 651x831 WebP quality 80"),
	("head-assemblies", "PDF pages 91-93 and 117, printed 2-23 to 2-25 and 3-3, head coil, face, relay, and motor-regulator assemblies", "the_machine_operations_manual.pdf page 91, crop box 0.1,0.06,0.95,0.8, scanned page rendered at its native resolution (embedded image xref 461, 2550px across 8.50in), rendered at 125 dpi, capped to 900px wide, grayscale, 901x1015 WebP quality 80"),
	("helmet-and-chase-light", "PDF pages 95, 100, 120, and 55, printed 2-27, 2-32, 3-6, and 1-35, chase light board, helmet assembly, and helmet light test", "the_machine_operations_manual.pdf page 100, crop box 0.1,0.08,0.95,0.86, scanned page rendered at its native resolution (embedded image xref 488, 2550px across 8.50in), rendered at 166 dpi, capped to 1200px wide, grayscale, 1201x1426 WebP quality 80"),
)


def _excerpt_records() -> list[dict[str, Any]]:
	records = []
	for name, locator, derivation in EXCERPTS:
		text_path = EXCERPT_DIRECTORY / f"{name}.md"
		image_path = EXCERPT_DIRECTORY / f"{name}.webp"
		records.append({
			"id": f"excerpt.bride-of-pinbot.{name}",
			"locator": locator,
			"path": text_path.relative_to(ROOT).as_posix(),
			"sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
			"image": image_path.relative_to(ROOT).as_posix(),
			"image_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
			"image_derivation": derivation,
			"method": "manual",
			"transcribed_by": "curator, read from the rendered page",
			"reviewed": True,
		})
	return records


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog records for the fourteen-driver bop_* clone tree rooted at bop_l7",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/bop.c: bopGameData (GEN_WPCALPHA_2, wpc_dispAlpha, FLIP_SWNO(12,11) with no FLIP_SOL, "
				"lampCol = 2 commented 'extra lamp columns for the helmet lights', an all-zero inverted-switch mask, and "
				"swStart/swTilt/swSlamTilt/swCoinDoor dedicated switches), every swXX/sXX #define, the CORE_GAMEDEF/CORE_CLONEDEF "
				"driver list and ROM sizes, bop_wpc_w (WPC_SOLENOID1 bit 1 clocks and bit 0 shifts a 16-bit helmet register "
				"published as lamp columns 9 and 10, i.e. public lamps 91-98 and 101-108), the P-ROC handler comments naming C25 "
				"data and C26 clock, bop_handleMech's four-face tick model of switch 67 and its bop_l7-only wpc_ram[0x1fc9] "
				"face reset, and bop_getMech; src/wpc/wpc.c wpc_init's per-game output typing (17-24 #89 flashers, helmet "
				"lamps typed as underpowered #44 with a FIXME saying the helmet wiring is unknown), the WPC_GILAMPS J111/"
				"Game-On mapping, the 64 + lampCol*8 public lamp count, and the wpc_dispAlpha layout; src/wpc/core.c "
				"core_getSol's 1-50 public dispatch, core_updateSw's generic flipper column and matrix copies 112->11 and "
				"114->12, and the synthetic lower-flipper states; src/wpc/core.h CORE_FIRSTSIMSOL."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-alpha.json",
			"revision": "repository",
			"locator": "WPC-Alpha public switch, DIP, solenoid, lamp (including the lampCol auxiliary columns 91-98 and 101-108), and five-GI address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "https://archive.org/details/williams-the-machine-bride-of-pinbot-manual",
			"source_id": "williams-the-machine-bride-of-pinbot-manual",
			"original_filename": "the_machine_operations_manual.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T10:58:00Z",
			"locator": (
				"Williams operations manual for The Machine (Bride of Pin*Bot), part number 16-50002-101, March 1991, 170-page "
				"scan with an OCR text layer (Internet Archive item williams-the-machine-bride-of-pinbot-manual, file "
				"https://archive.org/download/williams-the-machine-bride-of-pinbot-manual/the_machine_operations_manual.pdf, "
				"uploader kay@barkbark.zone, public date 2026-07-17, Internet Archive SHA-1 af114883fa7ec24a1f1211642a5534c6b281c628). "
				"PDF page = printed Section-2 page + 68. Tables were read from the native 300 dpi page images because the "
				"OCR layer doubles glyphs. Retained locally under external:pinmame-manuals/by-machine/"
				"williams.the-machine-bride-of-pinbot.1991/."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": _excerpt_records(),
		},
		{
			"id": RUNTIME_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_EVIDENCE_PATH}",
			"revision": PINMAME_REVISION,
			"locator": (
				"Pinned LibPinMAME runs of bop_l7 from empty NVRAM driven by tools/bop_head_mech_experiment.py: the head "
				"cycle test under three synthetic switch-67 models, the head coil test from four head start angles, the "
				"helmet single-lamp test, and the switch-edge, single-lamp, solenoid, and flasher service tests whose "
				"display names were recorded. Display names quoted in device notes are read with digits restored from context: the WPC alphanumeric font draws 5 like S and 0 like O."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/source/The%20Machine-Bride%20Of%20Pinbot%20%28Williams%201991%29_VPW_1.0.3.vpx",
			"original_filename": "The Machine-Bride Of Pinbot (Williams 1991)_VPW_1.0.3.vpx",
			"sha256": TABLE_SHA256,
			"acquired_at": "2026-09-25T11:00:00Z",
			"locator": (
				f"Retained VPW 1.0.3 recreation from the contributor's existing table collection. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/2162. Geometry authority for named table objects only."
			),
			"license": "NOASSERTION",
			"attribution": "VPW (Visual Pinball Workshop) table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"acquired_at": "2026-09-25T11:00:00Z",
			"locator": (
				"Retained embedded script (306,089 bytes). Runtime authority: cGameName = \"bop_l7\"; SolCallback 1-8, 15, 16 "
				"and the SolModCallBack 17-24 flasher table; the Lampz.MassAssign bindings for 11-68, 71-85 (backglass flasher "
				"objects), 86-88, and the sixteen helmet lights 91-98/101-108; ModLampz G.I. strings 2 (GiRear) and 4 (GiFront) "
				"with 0 and 3 used only for the VR backglass; the cvpmMyMech head model (Sol1 = 28 drive, Sol2 = 27 direction, "
				"HeadMechCallback closing switch 67 only while faces 1-3 are up) with Controller.HandleMechanics = -1; the "
				"trough, eye/mouth kickers, and wire ball lock post handlers."
			),
			"license": "NOASSERTION",
			"attribution": "VPW (Visual Pinball Workshop) table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_ALT_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/source-alt/The%20Machine%20-%20Bride%20Of%20Pinbot%20%28Williams%201991%29.vpx",
			"original_filename": "The Machine - Bride Of Pinbot (Williams 1991).vpx",
			"sha256": "606f9991dd4c21b113a38d7b8d25b653a0a6c999ff9892b368b6f07127246349",
			"acquired_at": "2026-09-25T11:00:00Z",
			"locator": (
				"Older VP10 Rev 2.0 recreation retained from the contributor's table archive (embedded script SHA-256 "
				"0a569c9732d4ed90ad03e2c010ce23d98acf4bb12e1c8e1f5a2cb8929e377c89, extracted beside it as extracted-alt-vpxtool). "
				"Cited only for its Bumper1_Hit/Bumper2_Hit/Bumper3_Hit handlers (script lines 1950, 1964, 1978), which pulse "
				"switches 53, 55, and 54: the same permutation as the VPW 1.0.3 table. Not a geometry or runtime source."
			),
			"license": "NOASSERTION",
			"attribution": "VP10 table authors (unclewilly, wrd1972 and contributors)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool.manifest.json",
			"acquired_at": "2026-09-25T11:00:00Z",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, "
				f"produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
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
	return {
		"board": "WPC CPU board",
		"drive_wire": SWITCH_COLUMN_WIRES[column],
		"drive_connection": f"J206-{column} (printed label 'J20' with a detached '6' beside pin 8)",
		"return_wire": SWITCH_ROW_WIRES[row],
		"return_connection": f"J208-{row}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, wire, note = DEDICATED_SWITCHES[address]
		items.append(_device(
			f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
			normally_closed=False,
			roles=[role],
			physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address} ({wire} wire). {note}"},
			wiring={"board": "WPC CPU board", "drive_wire": wire},
			spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
		))

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"switch.matrix-{address}"
			label = SWITCH_LABELS.get(address)
			physical: dict[str, Any] = {}
			part = SWITCH_PARTS.get(address)
			if part:
				physical["part_number"] = part
				if part.startswith(MICROSWITCH_PART_PREFIX):
					physical["switch_type"] = "microswitch"
			notes = f"Printed switch-matrix column {column} ({SWITCH_COLUMN_WIRES[column]}), row {row} ({SWITCH_ROW_WIRES[row]})."
			if address in ROM_SWITCH_NAMES:
				notes += f" The bop_l7 switch-edge test names this address \"{ROM_SWITCH_NAMES[address]}\"."
			extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
			kind = "switch"
			availability = "used"
			if address in PRINTED_NOT_USED:
				label = f"Not Used Matrix Position {address}"
				availability = "unused"
				notes += " Printed \"Not Used\" on both the switch matrix (2-40) and the switch-locations list (2-41), and named NOT USED by the ROM's switch-edge test."
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
				refs = (MANUAL_SOURCE, RUNTIME_SOURCE)
			elif address in BLANK_COLUMN_8:
				label = f"Unpopulated Matrix Position {address}"
				availability = "unused"
				notes += " The printed matrix cell carries only the address number, with no description and no part; the switch-locations list stops at 78. Closing this address in the switch-edge test produced no display response."
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
				refs = (MANUAL_SOURCE, RUNTIME_SOURCE)
			elif address == 23:
				label = "Ticket Opto (Not Fitted)"
				availability = "unused"
				notes += (
					" The matrix page prints \"Ticket Opto\" but the switch-locations list prints \"Not Used\" in its part-number "
					"column: the ROM supports an optional ticket dispenser, which this machine does not ship with. Pinned bop.c "
					"declares a vestigial #define swTicket 23 that nothing else references. Recorded unused as fitted."
				)
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			elif address == 24:
				kind = "constant"
				notes += " Physical part A-8630, the same part as switch 22; a permanently closed link proving the matrix is connected. Toggling it in the switch-edge test produced no display response."
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
			elif address in {11, 12}:
				right = address == 11
				notes += (
					f" A-9990-1 cabinet flipper-button switch. bopGameData declares FLIP_SWNO(12,11) with no FLIP_SOL, so "
					f"core_updateSw copies PinMAME's generic cabinet input {112 if right else 114} into this matrix address; the "
					"retained script sets it directly from the flipper keys."
				)
				extra["roles"] = ["flipper.lower.right.button" if right else "flipper.lower.left.button"]
				extra["normally_closed"] = False
				physical["location"] = "cabinet flipper button"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
			elif address in {13, 14, 21, 22}:
				extra["roles"] = [{13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]]
				extra["normally_closed"] = False
				physical["location"] = "cabinet"
				if address == 13:
					physical["switch_type"] = "button"
				if address == 14:
					physical["switch_type"] = "tilt"
				if address == 22:
					notes += " Closed while the coin door is closed."
					extra["initial_active"] = True
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["normally_closed"] = False
				object_name, position = SWITCH_POSITIONS[address]
				if address != 67:
					notes += f" Retained table object {object_name}."
				spatial_refs: tuple[str, ...] = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
				if address in {53, 54, 55}:
					notes += (
						" The manual prints 53 Upper Right, 54 Upper Left, 55 Lower on both switch pages, draws 54 in the "
						"upper-left bumper, 53 in the upper-right bumper and 55 in the lower bumper, pinned bop.c names them "
						"swRightJet/swLeftJet/swBottomJet, and the ROM's switch test names 53 \"U.R.\" and 54 \"U.L.\"; "
						"the placement follows that agreement. The retained script instead pulses 53 from Bumper1 (upper left), "
						"55 from Bumper2 (upper right), and 54 from Bumper3 (lower); the older VP10 Rev 2.0 table retained beside it "
						"carries the same permutation. That is a defect in the consumed table, not a disagreement about the machine: "
						"the three bumpers score alike, so it is invisible in play."
					)
					spatial_refs = (MANUAL_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
					refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, VPX_ALT_TABLE_SOURCE)
				if address in {63, 64, 65}:
					notes += " A mini microswitch mounted on the head's eye/mouth coil bracket (A-14124/A-14123/A-14125 item 8); it closes while a ball rests in the opening and is cleared when the kicker coil fires. Located at the opening's trigger in the retained table."
				if address == 67:
					notes += (
						" Mini microswitch 5647-12693-06 riding the head drive; the head's only position feedback. The manual's "
						"head tests say it must be open on an indentation and closed off one. Runtime contract observed on bop_l7: "
						"the ROM stops the head motor just after this switch closes when it moves to faces 1, 2 and 3, and just "
						"after it opens when it moves to face 4; it homes by running to the next opening edge of 67, which it treats as face 4, and then stepping one face; from four start angles under the same pattern it homed onto three different physical positions, so homing does not find an absolute mark in these synthetic patterns. Pinned bop.c's header comment, its wpc_ram[0x1fc9] face reset, and the retained script's advice to delete the .nv file when the head desynchronizes all indicate that the ROM keeps the current face in NVRAM. The manual's head-test introduction (printed 1-32/1-33) says the head homes to face 1 when a head test starts, re-times every face position (calibrates) if it cannot home, and shows ERROR UNABLE TO CALIBRATE HEAD if that fails, so the real cam gives the ROM a reference these synthetic patterns, whose switch-closed windows are identical, do not reproduce; no run showed the calibration error. The switch-locations drawing (2-41) prints 67 above and "
						"behind the head box; no retained table object models it, so it is anchored at the centre of the head assembly it senses."
					)
					spatial_refs = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				if address == 25:
					notes += " The retained ballrelease kicker holds the third trough ball and asserts 25 while occupied; ball release (2) ejects from it."
				if address == 46:
					notes += " Located on the retained sw46k kicker, which the under-playfield kicker coil (3) fires."
				if address == 38:
					notes += " Located on the retained Drain kicker that the outhole coil (1) kicks."
				if address in {28, 36, 37}:
					notes += " B-11854-4 red standup target assembly; located at the target primitive's centre."
				extra["spatial"] = located(identifier, "sensor", [position], *spatial_refs)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	for address in range(111, 119):
		used = address in {112, 114}
		right = address == 112
		label = "Generic Right Flipper Button State" if right else "Generic Left Flipper Button State" if used else f"Unused Generic Flipper Input {address}"
		notes = (
			f"Live generic cabinet-flipper input from PinMAME's switch column 11; core_updateSw copies it to matrix switch {11 if right else 12}."
			if used else
			"Public generic-flipper-column position. The Machine has no upper flippers and declares no EOS input here, so it is explicitly unused."
		)
		extra = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {"location": "cabinet flipper button" if used else "internal public address space", "switch_type": "button" if used else "other", "notes": notes},
			"normally_closed": False,
			"spatial": not_applicable("cabinet_or_service" if used else "unused", CORE_SOURCE, CONTROLLER_SOURCE),
		}
		if used:
			extra["roles"] = ["flipper.lower.right.button" if right else "flipper.lower.left.button"]
		items.append(_device(f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "used" if used else "unused", (CORE_SOURCE, CONTROLLER_SOURCE), **extra))

	for address in range(1, 9):
		items.append(_device(
			f"switch.dip-{address}", f"CPU Configuration Bit {address}", "dip_switch", "pinmame.input.dip", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
			physical={
				"location": "WPC CPU board",
				"switch_type": "dip",
				"notes": (
					"One of the eight CPU-board configuration bits PinMAME exposes as DIP inputs. The manual's front-matter "
					"Jumper Chart sets country with jumpers W14-W18 (all In for American; W17 Out for French; W18 Out for "
					"German); it does not tie those jumpers to individual PinMAME DIP positions, so no mapping is asserted here."
				),
			},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		))
	return items


def output_id(label: str) -> str:
	return "device." + label.lower().replace("/", "-").replace("(", "").replace(")", "").replace(",", "").replace(".", "").replace(" ", "-")


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		printed_type, wire, connection, transistor, part = SOLENOID_WIRING[address]
		is_flasher = 17 <= address <= 24
		kind = "flasher" if is_flasher else "control_signal" if address in {25, 26} else "relay" if address == 27 else "motor" if address == 28 else "coil"
		physical: dict[str, Any] = {}
		if part and not is_flasher:
			physical["part_number"] = part
		notes = f"Printed solenoid table entry {address:02d} \"{SOLENOID_PRINTED[address]}\" ({printed_type})."
		if address in ROM_SOLENOID_NAMES:
			notes += f" The bop_l7 service tests name it \"{ROM_SOLENOID_NAMES[address]}\"."
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": {"board": "WPC power driver board", "control_wire": wire, "control_connection": connection, "driver_transistor": transistor},
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
		if is_flasher:
			object_name, positions = SOLENOID_POSITIONS[address]
			if address in FLASHERS_WITH_INSERT:
				physical["quantity"] = 2
				notes += (
					" Printed flashlamp types: a playfield bulb and a #906 insert-panel bulb in the backbox. The table prints types, not "
					"counts; one bulb of each is assumed for the quantity. The front-matter "
					"copy of the solenoid table gives each such flasher a second, J125 connection (page 2-42 prints that column one row "
					"lower). Only the playfield bulb has a playfield placement."
				)
			else:
				physical["quantity"] = 1
				notes += " Printed flashlamp complement: one #89 playfield bulb only."
			if address in {21, 22, 23, 24}:
				notes += (
					" Both copies of the solenoid table print the playfield bulb as #555, the solenoid-locations page prints #89PL, "
					"and pinned wpc.c types all of 17-24 as #89 flashers; the helmet parts list calls the dome's bulb a Single "
					"Flashlamp Assy (C-13337)."
				)
			if address in {21, 22}:
				notes += " A red mini dome mounted on the helmet."
			notes += f" Retained table object {object_name}."
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		elif address in {25, 26}:
			notes += (
				" Logic-level line into the A-14007 Chase Light board's J1 "
				+ ("DATA input" if address == 25 else "CLOCK input")
				+ ": two cascaded 74LS164 shift registers drive sixteen 2N6427 lamp transistors for the helmet lights, whose "
				"B+ comes from G.I. string 02. Pinned bop.c shifts one bit per clock edge and publishes the sixteen register "
				"outputs as public lamps 91-98 and 101-108. It drives no load of its own."
			)
			extra["roles"] = ["internal.helmet-shift-register"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 27:
			notes += (
				" A-14423-1 double-pole change-over relay (printed 3-3): with the relay released the head motor's BLU lead is on "
				"+12 V and its BLK lead on the head-motor driver (28); energized, the leads swap and the motor reverses. On bop_l7 "
				"the ROM holds it released for forward (clockwise) moves and energized for reverse moves."
			)
			extra["roles"] = ["internal.head-motor-direction"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, RUNTIME_SOURCE)
		elif address == 28:
			notes += (
				" A-14119 +12 V DC head motor, powered from the A-13892-2 Motor Regulator Board and switched on its low side through "
				"the relay (27). Placed at the head assembly it rotates."
			)
			object_name, positions = SOLENOID_POSITIONS[address]
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		elif address == 7:
			notes += " Cabinet knocker; not drawn on the playfield."
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			object_name, positions = SOLENOID_POSITIONS[address]
			if address == 12:
				notes += " The solenoid-locations list prints item 12 as \"Left (\"Sling\") Kicker\", a typo: both copies of the table print Right, and that page's own drawing places 12 at the right slingshot."
			if address in {8, 15, 16}:
				notes += " AE-30-2000 coil on its own head coil assembly inside the rotating head; it kicks a ball back out of the face opening. The ROM's normal solenoid test skips it; the head-coil test fires it only with its face up."
			if address == 6:
				notes += " Drives the post (AE-26-1200 coil, the A-14046 Disappear Post Assembly in the playfield parts list) that holds balls on the wireform; the retained script drops the BL post wall while energized."
			notes += f" Retained table object {object_name}."
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))

	state_outputs = {
		29: ("device.wpc-j111-state-29", "WPC J111 State 29", "virtual", "used", ["internal.wpc-state"], "PinMAME mirrors WPC_GILAMPS bit 5, one of the CPU board's J111 GPIO state bits, to public address 29; a live controller state channel, not a playfield device."),
		30: ("device.wpc-j111-state-30", "WPC J111 State 30", "virtual", "used", ["internal.wpc-state"], "PinMAME mirrors WPC_GILAMPS bit 6, one of the CPU board's J111 GPIO state bits, to public address 30; a live controller state channel, not a playfield device."),
		31: ("device.game-on-solenoid-relay", "Game-On Solenoid Relay", "relay", "used", ["internal.wpc-state", "cabinet.game-on-relay"], "The real pre-Fliptronic Game-On relay controlled by WPC_GILAMPS bit 7, which enables the direct-wired flippers; pinned core.c also gates the synthetic flipper states on it. A cabinet/flipper-enable relay, not a playfield coil."),
		32: ("device.unused-wpc-state-output-32", "Unused WPC State Output 32", "virtual", "unused", ["internal.unused.wpc-output"], "PinMAME's WPC state remap has no fourth bit at public address 32, so this position is constant zero."),
	}
	for address in range(33, 45):
		state_outputs[address] = (
			f"device.unused-wpc-output-{address}", f"Unused WPC Output {address}", "virtual", "unused", ["internal.unused-platform-slot"],
			"Generic upper-flipper-shaped public position; The Machine has no upper flippers and bopGameData declares no FLIP_SOL, so nothing drives it." if address <= 36 else
			"Platform public-output position not served by the WPC-Alpha generation; PinMAME returns zero.",
		)
	state_outputs.update({
		45: ("device.synthetic-lower-right-flipper-power", "Synthetic Lower Right Flipper Power", "virtual", "used", ["internal.synthetic-flipper"], "Fabricated by core_updateSw from the live right flipper button while the Game-On relay is on; the physical FL-11630 flipper is direct-wired (Blu-Yel, J109-7) and has no driver-board output."),
		46: ("device.synthetic-lower-right-flipper", "Synthetic Lower Right Flipper", "virtual", "used", ["internal.synthetic-flipper", "flipper.lower.right"], "PinMAME's combined lower-right flipper state (sLRFlipper) that the retained script's SolRFlipper consumes; not an additional coil."),
		47: ("device.synthetic-lower-left-flipper-power", "Synthetic Lower Left Flipper Power", "virtual", "used", ["internal.synthetic-flipper"], "Fabricated from the live left flipper button under the same conditions as 45; the physical FL-11630 flipper is direct-wired (Gry-Yel, J109-5)."),
		48: ("device.synthetic-lower-left-flipper", "Synthetic Lower Left Flipper", "virtual", "used", ["internal.synthetic-flipper", "flipper.lower.left"], "PinMAME's combined lower-left flipper state (sLLFlipper) that the retained script's SolLFlipper consumes; not an additional coil."),
		49: ("device.pinmame-simulator-ball-shooter", "PinMAME Simulator Ball-Shooter Channel", "virtual", "used", ["internal.simulator-ball-shooter"], "Platform simulator-only fake ball-shooter solenoid (sShooterRel, CORE_FIRSTSIMSOL); bop.c's Shooter state uses it. No physical circuit."),
		50: ("device.unassigned-solenoid-slot-50", "Unassigned Solenoid Slot 50", "virtual", "unused", ["internal.unused-platform-slot"], "Reserved platform gap before custom outputs; bopGameData declares no custom solenoids."),
	})
	for address in range(29, 51):
		identifier, label, kind, availability, roles, notes = state_outputs[address]
		items.append(_device(
			identifier, label, kind, "pinmame.output.solenoid", address, availability, (CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			roles=roles,
			physical={"notes": notes},
			spatial=not_applicable("cabinet_or_service" if address == 31 else "virtual", CORE_SOURCE, CONTROLLER_SOURCE),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"lamp.matrix-{address}"
			bulb = "#44" if address in LAMP_BULB_44 else "#555"
			drive_wire, drive_connection = LAMP_COLUMN_WIRES[column]
			return_wire, return_connection = LAMP_ROW_WIRES[row]
			notes = f"Printed lamp-matrix column {column}, row {row}; bulb {bulb}."
			if address in ROM_LAMP_NAMES:
				notes += f" The bop_l7 single-lamp test names it \"{ROM_LAMP_NAMES[address]}\"."
			if address in {61, 63}:
				notes += (
					" The lamp-matrix page (2-38) prints 61 \"Right Ramp 100K\" and 63 \"Right Ramp Million\", swapped against the "
					"lamp-locations page (2-39: 61 Million, 63 100K), whose drawing puts 61 on the large lowest insert of the stack. The "
					"ROM's single-lamp test shows RIGHT RAMP MILL at lamp 61 and RIGHT RAMP 100K at lamp 63, so the matrix cells are swapped."
				)
			if address == 25:
				notes += (
					" The lamp-matrix page prints \"Circle 500K\" while the lamp-locations page prints \"Circle - 50K\". The ROM's "
					"single-lamp test displays CIRCLE SOK here (one zero glyph; the 500K lamps display SOOK, and this font draws 5 like S "
					"and 0 like O), i.e. 50K, so the matrix cell is the typo."
				)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": {"board": "WPC power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection, "return_wire": return_wire, "return_connection": return_connection},
			}
			if address in BACKBOX_INSERT_LAMPS:
				notes += " Marked \"(on insert)\" on the lamp-locations page and not drawn on the playfield: a backbox insert-panel lamp. The retained script binds it to a backglass flasher object."
				extra["roles"] = ["cabinet.backglass"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				object_name = LAMP_POSITION_OBJECTS[address]
				notes += f" Retained table object {object_name}."
				if address in {86, 87, 88}:
					notes += " One of the three bulbs on the bracket at the rear of the mini-playfield, drawn left to right as 86, 87, 88 on the lamp-locations page; the retained table models them as upright flashers whose drag-point centres give the coordinate."
				if address in {46, 47, 48}:
					notes += " On the head face (A-14025 Face Lamp Assy)."
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
			extra["physical"] = {"quantity": 1, "notes": notes}
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE), **extra))

	vpx_by_position = {name: position for name, position in HELMET_SOCKETS_CLOCKWISE}
	for index, address in enumerate(HELMET_CLOCKWISE_FROM_LOWER_LEFT, start=1):
		socket_name, position = HELMET_SOCKETS_CLOCKWISE[index - 1]
		vpx_name = f"l{address}"
		vpx_position = vpx_by_position[vpx_name]
		column = 9 if address < 100 else 10
		notes = (
			f"Helmet chase light {index} of 16, counted clockwise from the lower-left socket. The sixteen #555 helmet bulbs sit on "
			"two A-14410/A-14412 8-lamp boards, are switched by the A-14007 Chase Light board from the data/clock lines "
			"(solenoids 25 and 26), and take their B+ from G.I. string 02; they are not matrix lamps, but pinned bop.c publishes "
			f"the shift register as lamp column {column}. The manual's helmet test says the first single lamp is the lower-left "
			"one and Up moves clockwise; on bop_l7 the test starts on public 108 and Up steps 107 ... 101, 98 ... 91, so this "
			f"address is socket {index} in that order. The coordinate is the retained table's {socket_name} socket. The retained "
			f"script binds this address to its own {vpx_name} object at x={vpx_position[0]}, y={vpx_position[1]}; its l91-l108 "
			"naming runs the other way round the helmet (mirrored left to right), a consumed-table defect that only reverses "
			"the direction of the chase."
		)
		items.append(_device(
			f"lamp.helmet-{address}", f"Helmet Light {index}", "lamp", "pinmame.output.lamp", address, "used",
			(MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
			physical={"quantity": 1, "location": "helmet", "notes": notes},
			spatial=located(f"lamp.helmet-{address}", "emitter", [position], MANUAL_SOURCE, RUNTIME_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE),
		))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	gi = {
		0: ("Backglass Body G.I.", "01", "Backglass Body", "Wht-Brn", "J121-7", "Q18"),
		1: ("Helmet Lights G.I. Supply", "02", "Used In Helmet", "Wht-Org", "J120-8", "Q10"),
		2: ("Rear Playfield G.I.", "03", "Rear Playfield", "Wht-Yel", "J120-9", "Q14"),
		3: ("Backglass No-Body G.I.", "04", "Backglass - No Body", "Wht-Grn", "J121-11", "Q16"),
		4: ("Front Playfield G.I.", "05", "Front Playfield", "Wht-Vio", "J120-11", "Q12"),
	}
	items: list[dict[str, Any]] = []
	for address, (label, printed, printed_label, wire, connection, transistor) in gi.items():
		identifier = f"gi.string-{address}"
		notes = f"Printed general-illumination circuit {printed} \"{printed_label}\" (#555 bulbs)."
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": printed}, {"namespace": "manual.label", "value": printed_label}],
			"wiring": {"board": "WPC power driver board", "return_wire": wire, "return_connection": connection, "driver_transistor": transistor},
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address in {0, 3}:
			notes += " A backbox string; the retained script drives it only for its VR backglass."
			extra["roles"] = ["cabinet.backglass"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 1:
			notes += (
				" The helmet test states that the helmet lights' power is obtained through G.I. string #2: this string is the B+ "
				"the Chase Light board switches, so its emitters are the sixteen helmet bulbs (public lamps 91-108), which share "
				"these placements: each helmet bulb lights only while this string is on and its own shift-register bit is set. The "
				"relationship vocabulary has no supply-gating kind, so that two-condition rule is stated here and on each helmet "
				"lamp rather than as a structured relationship. Pinned wpc.c's FIXME guessing the helmet supply comes from G.I. "
				"line 2 is confirmed. The retained script does not drive it."
			)
			physical["quantity"] = 16
			positions = [position for _name, position in HELMET_SOCKETS_CLOCKWISE]
			extra["spatial"] = located(identifier, "emitter", positions, MANUAL_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_TABLE_SOURCE)
		else:
			members = GI_REAR_POSITIONS if address == 2 else GI_FRONT_POSITIONS
			collection = "GiRear" if address == 2 else "GiFront"
			notes += (
				f" The retained script's ModLampz string {address} drives the {collection} collection. Its lights reduce to "
				f"{len(members)} co-located emitter clusters; the smallest-radius named light in each supplies the coordinate "
				f"({', '.join(name for name, _position in members)})."
			)
			notes += " The manual prints no per-string bulb count, so the quantity and grouping are the retained table's emitter count."
			if address == 2:
				notes += " Three of the nine are the jet-bumper cap lights, which the table puts on this string."
			physical["quantity"] = len(members)
			extra["spatial"] = located(identifier, "emitter", [position for _name, position in members], VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", refs, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.player-1-alphanumeric",
			"label": "Upper sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 0,
			"segment_start": 0,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "display.player-2-alphanumeric",
			"label": "Lower sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 1,
			"segment_start": 20,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly:
			record["assembly_part_number"] = assembly
		if positions:
			record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": description} for pid, plabel, psensors, description in positions]
		return record

	return [
		mechanism(
			"mechanism.head", "Rotating four-face head", "rotary",
			[output_id("Head Motor"), output_id("Head Motor Relay")], ["switch.matrix-67"],
			"A +12 V DC motor (A-14119, fed by the A-13892-2 Motor Regulator Board) turns the head box carrying four face plates "
			"(A-14121). Head Motor (28) runs it; the Motor Relay (27, A-14423-1) swaps the motor leads, released for forward "
			"(clockwise) and energized for reverse. Face Position switch 67 is the only feedback. On bop_l7 the ROM stops the motor "
			"shortly after 67 closes when it moves to faces 1, 2 or 3, and shortly after 67 opens when it moves to face 4; "
			"it homes by running to the next opening edge of 67, which it treats as face 4, and then stepping one face; from four start angles under the same pattern it homed onto three different physical positions, so homing does not find an absolute mark in these synthetic patterns. Pinned bop.c's header comment, its wpc_ram[0x1fc9] face reset, and the retained script's advice to delete the .nv file when the head desynchronizes all indicate that the ROM keeps the current face in NVRAM. The manual's head-test introduction (printed 1-32/1-33) says the head homes to face 1 when a head test starts, re-times every face position (calibrates) if it cannot home, and shows ERROR UNABLE TO CALIBRATE HEAD if that fails, so the real cam gives the ROM a reference these synthetic patterns, whose switch-closed windows are identical, do not reproduce; no run showed the calibration error. A recreation must therefore keep the modelled head and the stored face (wpc_ram 0x1fc9) in step (the retained script sets HandleMechanics = -1, "
			"which writes face 1 for bop_l7, and starts its head on face 1). The known-working model closes 67 only while faces "
			"1-3 dwell, so the opening edge the ROM treats as reaching face 4 arrives as the head leaves face 3: the table's "
			"standard path stops just past the face the head left (face 3 moving forward, face 1 moving in reverse) while the ROM "
			"believes face 4, and only its P-ROC path "
			"keeps turning to the next face window and snaps (delayHeadStop, script.vbs lines 1115-1170). Faces 3 and 4 both carry "
			"blank guide plates, so play is unaffected; a recreation that must show face 4 correctly needs that coast-to-next-face "
			"behaviour, which the harness's instant-stop probe models do not include. Faces: 1 mouth, 2 eyes with a Y lane-select diverter, 3 and 4 plain guide faces. Balls arrive from the "
			"Shuttle (left) ramp over Enter Head (47) when the Controlled Gate is closed.",
			[
				("face-1", "Face 1 (mouth)", ["switch.matrix-65"], "Face Plate 1 (A-14130): one central opening; a ball entering it closes Head Mouth (65) and Head Mouth Kicker (8) ejects it."),
				("face-2", "Face 2 (eyes)", ["switch.matrix-63", "switch.matrix-64"], "Face Plate 2 (A-14131): two openings behind the Y lane-select diverter; Head Left/Right Eye (63/64) and kickers 15/16."),
				("face-3", "Face 3", [], "Face Plate 3 (A-14132): no opening; ball guides return the ball."),
				("face-4", "Face 4", [], "Face Plate 4 (A-14133): no opening; ball guides return the ball. Reached when 67 opens."),
			],
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly="A-14121",
		),
		mechanism(
			"mechanism.head-mouth-kicker", "Head mouth kicker", "kicker",
			[output_id("Head Mouth Kicker")], ["switch.matrix-65"],
			"AE-30-2000 coil assembly A-14125 behind the face-1 opening with its own microswitch (65). A ball resting in the mouth "
			"closes 65; firing 8 kicks it back out and 65 opens. The ROM's head-coil test fires 8 only with face 1 up.",
			[], MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, assembly="A-14125",
		),
		mechanism(
			"mechanism.head-eye-kickers", "Head eye kickers", "kicker",
			[output_id("Head Left Eye Kicker"), output_id("Head Right Eye Kicker")], ["switch.matrix-63", "switch.matrix-64"],
			"Two AE-30-2000 coil assemblies (A-14124 left, A-14123 right) behind the face-2 openings, each with its own microswitch "
			"(63 left, 64 right). A passive Y lane-select (01-10164) on Face Plate 2 splits balls between the eyes. Firing 15 or 16 "
			"kicks the ball out and opens its switch; the ROM's head-coil test fires 15 and then 16 at the same head stop (face 2).",
			[], MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker",
			[output_id("Outhole"), output_id("Ball Release")], ["switch.matrix-38", "switch.matrix-27", "switch.matrix-26", "switch.matrix-25", "switch.matrix-52"],
			"Drained balls land in the outhole (38); Outhole (1) kicks them into the trough, which fills Left (27), Center (26), and "
			"Right (25) Trough. Ball Release (2) feeds the ball at 25 to the shooter lane feeder (52). The retained script creates "
			"its three balls at 27, 26, and 25.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.skill-shot", "Shuttle skill shot and kicker", "kicker",
			[output_id("Skill Shot Kicker")], ["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"The plunged ball climbs the right-side skill-shot lane between rubber cylinders and falls back past five rollovers "
			"stacked 35 (25K, top), 34 (200K), 33 (100K), 32 (75K), 31 (50K, bottom); the Skill Shot Kicker (5, AE-24-900, B-11395-1) "
			"then fires it into play from the bottom of the lane. The retained script's impulse plunger uses 31 as its ball-present "
			"switch.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.controlled-gate", "Shuttle ramp controlled gate", "diverter",
			[output_id("Controlled Gate")], ["switch.matrix-76", "switch.matrix-73", "switch.matrix-47"],
			"A-14406 gate assembly at the top of the Shuttle (left) ramp. Energized, it routes the ramp ball into the mini-playfield "
			"(Enter Mini Playfield 73); de-energized, the ball continues to the head (Enter Head 47). Left Ramp Enter (76) sees every "
			"ramp shot.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.wire-ball-holder", "Wireform ball lock post", "gate",
			[output_id("Wire Ball Holder")], ["switch.matrix-71", "switch.matrix-72"],
			"Balls returning from the head run down the wireform past Wireform Top (71) to a post that holds them at Wireform Bottom "
			"(72). Energizing the Wire Ball Holder (6) retracts the post and releases the held ball to the left inlane; the retained "
			"script drops its BL post while 6 is on.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.under-playfield-kicker", "Small wheel under-playfield kicker", "kicker",
			[output_id("Under Playfield Kicker")], ["switch.matrix-46"],
			"The far-left shot drops through the small-wheel entrance to a kicker under the playfield (46); Under Playfield Kicker (3) "
			"fires it back up at the far left.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.mini-playfield-jets", "Mini-playfield jet bumpers and jets sling", "other",
			[output_id("Upper Left Jet Bumper"), output_id("Upper Right Jet Bumper"), output_id("Lower Jet Bumper"), output_id("Jets Sling")],
			["switch.matrix-54", "switch.matrix-53", "switch.matrix-55", "switch.matrix-56", "switch.matrix-73", "switch.matrix-74", "switch.matrix-75"],
			"The upper-right mini-playfield (A-14358) carries three jet bumpers, Upper Left (switch 54, coil 9), Upper Right (switch 53, "
			"coil 11) and Lower (switch 55, coil 13), and the jets sling kicker (switch 56, coil 14). Balls enter at 73 and leave at "
			"Mini Exit Left (74, toward the playfield) or Mini Exit Right (75, back toward the shooter).",
			[], MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.slingshots", "Lower slingshots", "kicker",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-57", "switch.matrix-58"],
			"Left (switch 57, coil 10) and right (switch 58, coil 12) slingshot kickers above the flippers.",
			[], MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.helmet-chase-lights", "Helmet chase lights", "other",
			[output_id("Helmet Lights Data"), output_id("Helmet Lights Clock")], [],
			"The ROM shifts a 16-bit pattern into the A-14007 Chase Light board (two 74LS164 registers) through the data (25) and "
			"clock (26) lines; each output switches one of the sixteen helmet bulbs, which draw power from G.I. string 02. PinMAME "
			"publishes the register as lamps 91-98 and 101-108. Clockwise from the lower-left socket the bulbs are 108, 107, 106, "
			"105, 104, 103, 102, 101, 98, 97, 96, 95, 94, 93, 92, 91 (manual helmet test plus the ROM's single-lamp order).",
			[], MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Direct-wired flippers", "other",
			[output_id("Synthetic Lower Right Flipper"), output_id("Synthetic Lower Left Flipper")],
			["switch.generic-112", "switch.generic-114", "switch.matrix-11", "switch.matrix-12"],
			"Two FL-11630 flippers wired straight to the cabinet buttons through the Game-On relay (31); there is no CPU flipper "
			"drive. PinMAME fabricates public states 45-48 from the buttons for animation; the matrix copies 11/12 tell the ROM a "
			"button is held.",
			[
				("lower-right", "Lower-right flipper", ["switch.generic-112", "switch.matrix-11"], "Animate from synthetic state 46."),
				("lower-left", "Lower-left flipper", ["switch.generic-114", "switch.matrix-12"], "Animate from synthetic state 48."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	# The motor relay only reverses the head motor; it never decides whether the motor can run, so it is
	# not a relay_gated relationship. Both outputs are the head mechanism's actuators instead.
	return []


def conflicts() -> list[dict[str, Any]]:
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
			"id": MACHINE_ID,
			"name": "The Machine: Bride of Pinbot",
			"manufacturer": "Williams",
			"year": 1991,
			"kind": "physical_pinball",
			"ipdb_id": 1502,
			"opdb_id": "GRpee-MePdR",
			"playfield": {"width": TABLE_WIDTH, "height": TABLE_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": STATUS,
			"missing": [],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "validated",
			},
		},
		"controller": {"platform": "pinmame.wpc-alpha", "hardware_generation": "0x2", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Bride of Pinbot device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	placement_count = 0
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved_outputs: list[dict[str, Any]] = []
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			placement_count += len(spatial["placements"])
	key = lambda item: (item["group"], item["address"])
	return {
		"format": "pinmame-spatial-audit" if STATUS == "author_ready" else "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": STATUS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": TABLE_WIDTH, "bottom": TABLE_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/the-machine-bride-of-pinbot-1991/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=key),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=key) for reason, bindings in sorted(not_applicable_outputs.items())},
		"unresolved": [{"group": "pinmame.input.switch", "address": address} for address in sorted(unresolved_inputs)] + sorted(unresolved_outputs, key=key),
		"projections": [
			{"group": "pinmame.input.switch", "address": 67, "reason": "Face Position rides the head drive; the switch-locations drawing (2-41) prints it in the dashed drive housing about 0.1 further toward the rear, but no retained table object models it, so it is anchored at the head assembly's centre (Face primitive), which the head motor (28) shares."},
			{"group": "pinmame.output.solenoid", "address": 28, "reason": "Head Motor placed at the centre of the head it rotates (Face primitive)."},
			{"group": "pinmame.output.solenoid", "address": 8, "reason": "Head Mouth Kicker placed on the retained TWKicker1 kicker-arm primitive behind the mouth opening."},
			{"group": "pinmame.output.solenoid", "address": 15, "reason": "Head Left Eye Kicker placed on the retained TWKicker2 kicker-arm primitive behind the left eye opening."},
			{"group": "pinmame.output.solenoid", "address": 16, "reason": "Head Right Eye Kicker placed on the retained TWKicker3 kicker-arm primitive behind the right eye opening."},
			{"group": "pinmame.output.gi", "address": 1, "reason": "The helmet-light supply string is placed at the sixteen helmet bulb sockets it powers, shared with lamps 91-108."},
		],
		"ordering_decisions": [
			"Jet-bumper switches follow the manual (both switch pages and the drawing), pinned bop.c names, and the ROM's switch-test names, not the retained script's permuted Bumper1/2/3 pulses.",
			"Helmet lamps follow the manual's helmet test (first lamp lower left, Up moves clockwise) combined with the ROM's single-lamp order (108 first, then 107 ... 101, 98 ... 91); the retained table's l91-l108 naming runs the opposite way round.",
			"Flasher domes 21-24 follow the manual's solenoid-locations drawing (21 left of the head, 22 right, 24 lower left, 23 lower right) and the retained script's SetRedDome1/2/4/3 bindings.",
		],
		"visual_review_cache": {"root": "external:pinmame-manuals/by-machine/williams.the-machine-bride-of-pinbot.1991/rendered/"},
		"excluded_object_classes": [
			"lbNN and LBNN co-located bloom Light objects paired with each lNN lamp object",
			"Larger-radius GiRear/GiFront render layers co-located with the smallest-radius emitter used for each G.I. cluster",
			"l91_refl-style HelmetLightRefl reflection helpers and the Flasherlit/Flasherflash dome render layers",
			"VR-room backglass objects (BG1M-BG8M, VRBGFL*, VRGiBody, VRGiNoBody) bound to backbox lamps 71-85 and G.I. strings 0 and 3",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Machine: Bride of Pinbot (Williams, 1991) spatial review",
		"",
		f"Status: {report['status']}.",
		"",
		f"Geometry comes from the retained known-working VPW 1.0.3 table (SHA-256 `{TABLE_SHA256}`), whose embedded script "
		f"(SHA-256 `{SCRIPT_SHA256}`) is the runtime authority. Exact bounds are `{TABLE_BOUNDS}`; every coordinate is x/952 and "
		"y/2162 at six fractional places. The Williams operations manual (16-50002-101, March 1991) is the physical authority.",
		"",
		"## Evidence decisions",
		"",
	]
	lines += [f"- {decision}" for decision in report["ordering_decisions"]]
	lines += [
		"- Backbox insert lamps 71-85 and G.I. strings 0 and 3 take controlled `cabinet_or_service` records; the insert bulbs of flashers 18, 19, and 21-24 are counted in each flasher's quantity without a playfield placement.",
		"- The helmet data and clock lines (25, 26) and the head motor relay (27) are `internal_nonvisual`.",
		"",
		"## Explicit projections",
		"",
	]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved records: {len(report['unresolved'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Manual SHA-256 `{MANUAL_SHA256}`; committed excerpts under `evidence/excerpts/{MACHINE_ID}/`.",
		f"- Runtime evidence `{RUNTIME_EVIDENCE_PATH}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	write_json(definition_path, definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return definition_path


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		raise RuntimeError(f"Stale Bride of Pinbot definition is still present: {stale}")
	expected = canonical_bytes(build())
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Bride of Pinbot definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Bride of Pinbot seed is not byte-identical to the canonical definition: {seed_path}")
	report = build_spatial_report(build())
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Bride of Pinbot spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Bride of Pinbot spatial review drifted from its deterministic curator: {markdown_path}")
	print("Bride of Pinbot definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Bride of Pinbot extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Bride of Pinbot retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
