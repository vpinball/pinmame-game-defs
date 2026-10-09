"""Curate the physical Williams Diner (1990) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and table
coordinate is a literal here, and the factory-drawing callout check is recomputed from its committed
seed, so regeneration reproduces the canonical definition, its pinned seed and the spatial report byte
for byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes them.

Diner is a System 11C machine (``GEN_S11C``) whose A/C select relay is solenoid 12:
``dinerGameData`` sets ``sxx.muxSol = 12``, so pinned PinMAME publishes the eight switched "A" loads
at 1-8 while the relay is released and their "C" partners at 25-32 while it is energized. It sets
``S11_MUXSW2``, which copies the relay's state into switch 2 (the relay's C-side contact), declares
no switch-driven special solenoids (plain ``INITGAME``, so ``sxx.ssSw`` is empty) and wires its
flippers through the cabinet with ``FLIP_SWNO(58,57)`` copying the buttons into the two lane-change
optos. The backbox DINE-TIME clock is a stepper motor on controlled solenoids 15 and 16 with a home
opto at switch 59.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import drawing_callouts
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_flipper_column import (
	VPM_CORE_SHA256,
	VPM_LIBRARY_SOURCE,
	VPM_LIBRARY_URI,
	VPM_S11_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.diner.1990"
PARTIAL_PATH = ROOT / "machines/partial/williams/diner-1990.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/diner-1990.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/diner-1990.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/williams/diner-1990-callouts.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/williams/diner-1990-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/diner-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/diner-1990.md"
KNOWLEDGE_PATH = "knowledge/williams/diner-1990.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/diner-l4-service-and-mechanisms.json"
VARIANT_GAMES = ("diner_l3", "diner_l2", "diner_l1", "diner_l4fr")


def variant_evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/system-11/diner-{game.split('_', 1)[1]}-service-tests.json"


def variant_source(game: str) -> str:
	return f"runtime.diner.{game.replace('_', '-')}-service-tests"

GAME_ON_EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/diner-diner_l4-game-on-23.json"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.diner.1990"
AMENDMENT_SOURCE = "service-bulletin.williams.diner.1990.amendment-1"
RUNTIME_SOURCE = "runtime.diner.l4-service-and-mechanisms"
GAME_ON_SOURCE = "runtime.diner.diner-l4.game-on-23"
VPX_TABLE_SOURCE = "vpx-table.diner-flupper-1-2"
VPX_SCRIPT_SOURCE = "vpx-script.diner-flupper-1-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.diner-flupper-1-2"
VPX_OBJ_SOURCE = "vpx-obj-export.diner-flupper-1-2"
CALLOUT_SOURCE = "drawing-callouts.diner.2026-10-09"

# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (58, 57)
AC_RELAY = 12

MANUAL_SHA256 = "da75ffb79e6d6b8d1b332ce65f93ee1486a5a7ff8d9060878f07a91438b573aa"
AMENDMENT_SHA256 = "6ffa18e1a4bb861b26dad22ec32e8c7a90305f24aecc2e0d98185ecccd7fedef"
TABLE_SHA256 = "f59be95f63e485415b36ff4a46ce07c3b4060d20f512dbe3e36a64b0bbde69b1"
SCRIPT_SHA256 = "df18744ca1550d20c2eba5e940b8723dd0fc0498d98f6a252d417bd5429e6162"
OBJ_EXPORT_SHA256 = "98f650fbce16de01af48ea0d7b7fd32266db5475d402e79873d82e6dedf60478"

EXTRACTION_RELATIVE_PATH = Path("williams/diner-1990/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/diner-1990/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 906
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "7685fc6099d42e9f0eb7762a75e4e9b53c0bfab2f24d216fef297ad5a614551d"

TABLE_BOUNDS = "left=0 top=0 right=1000 bottom=2000"
PLAYFIELD_WIDTH = 1000.0
PLAYFIELD_HEIGHT = 2000.0


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


DRIVER_IDS = ("diner_l4", "diner_l3", "diner_l2", "diner_l1", "diner_f2", "diner_g2", "diner_p0", "diner_l4fr")
_SHARED = (
	"Shares dinerGameData/init_diner with the parent through CORE_CLONEDEF (pinned src/wpc/s11games.c lines 1460 and "
	"1518-1525), and so the same GEN_S11C generation, s11_dispS11c display layout, A/C select relay 12, S11_MUXSW2 "
	"switch-2 copy and FLIP_SWNO(58,57) flipper wiring, and it plays on the same L-1 sound ROMs."
)
DRIVER_COMPATIBILITY = {
	"diner_l4": (
		"identical",
		"Williams LA-4 production game ROMs (dinr_u26.l4, dinr_u27.l4), the pinned clone-tree parent and the driver the "
		"retained known-working table binds (cGameName = \"diner_l4\"). The runtime evidence was recorded on it.",
	),
	"diner_l3": (
		"identical",
		"Williams LA-3 production game ROM (U27 u27-la3.rom with the U26 dinr_u26.l2). " + _SHARED + " Its Coil, Single "
		"Lamps and Switch Levels tests name every address exactly as LA-4 does (run diner_l3 in the variant evidence).",
	),
	"diner_l2": (
		"identical",
		"Williams LU-2 European game ROM (U27 dinr_u27.lu2 with the U26 dinr_u26.l2). " + _SHARED + " Its Coil, Single "
		"Lamps and Switch Levels tests name every address exactly as LA-4 does (run diner_l2 in the variant evidence).",
	),
	"diner_l1": (
		"identical",
		"Williams LU-1 European game ROMs (u26-lu1.rom, u27-lu1.rom), the European revision IPDB also hosts. " + _SHARED +
		" Its Coil, Single Lamps and Switch Levels tests name every address exactly as LA-4 does (run diner_l1 in the "
		"variant evidence).",
	),
	"diner_f2": (
		"identical",
		"Williams LF-2 French-language game ROM (U27 dinr_u27.lf2 with the U26 dinr_u26.l2). " + _SHARED + " A language "
		"revision of the production game; its archive is not in the local ROM corpus, so its service tests were not run.",
	),
	"diner_g2": (
		"identical",
		"Williams LG-2 German-language game ROM (U27 Diner_Nova_Apparate_U27_REV2.bin, which the pinned source calls "
		"\"presumably version LG-2\", with the U26 dinr_u26.l2). " + _SHARED + " A language revision of the production "
		"game; its archive is not in the local ROM corpus, so its service tests were not run.",
	),
	"diner_p0": (
		"unknown",
		"Williams PA-0 prototype game ROMs (dinr_u26.pa0, dinr_u27.pa0), catalogued 1989. " + _SHARED + " Shared game "
		"data proves PinMAME routes it like the production machine, not that the prototype it ran on had the production "
		"playfield; its archive is not in the local ROM corpus, so its service tests, which name every address the ROM "
		"drives, could not be compared, and no source describes the prototype.",
	),
	"diner_l4fr": (
		"identical",
		"2025 community modification of the LA-4 game ROMs (U26 dinr_u26.l4fr with the LA-4 U27), \"Fixed Right Ramp MOD\", "
		"which per the pinned source keeps the right ramp at 100k while the R is lit. " + _SHARED + " Its Coil, Single "
		"Lamps and Switch Levels tests name every address exactly as LA-4 does (run diner_l4fr in the variant evidence).",
	),
}

# --- Switch matrix (public address = (column-1)*8+row; System 11 sequential column-major).
# Labels of record follow the Switch-Matrix Table (printed page 75) with detail from the Switches
# parts list (printed page 74); the ROM's own Switch Levels names are kept per address.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "A/C Relay C-Side", 3: "Game Start (Credit)", 4: "Right Coin Chute", 5: "Center Coin Chute",
	6: "Left Coin Chute", 7: "Slam Tilt", 8: "High Score Reset",
	9: "Outhole", 10: "Up/Down (Left Ramp)", 11: "Ball Trough #1 (Right)", 12: "Ball Trough #2 (Middle)",
	13: "Ball Trough #3 (Left)", 14: "Shooter Lane", 15: "Sub-Playfield Shooter 1", 16: "Sub-Playfield Shooter 2",
	17: "Cup", 18: "Grill Bonus (Standup)", 19: "E (Top Lane)", 20: "A (Top Lane)", 21: "T (Top Lane)",
	22: "Hot Dog (Center 3-Bank Drop Target)", 23: "Burger (Center 3-Bank Drop Target)",
	24: "Chili (Center 3-Bank Drop Target)", 27: "Right Ramp Entry", 28: "Right Ramp Exit", 29: "Cup Entry (Right Ramp)",
	30: "Root Beer (Left 3-Bank Drop Target)", 31: "Fries (Left 3-Bank Drop Target)", 32: "Iced Tea (Left 3-Bank Drop Target)",
	36: "Left Ramp Exit", 37: "Left Outlane", 38: "Left Return Lane", 39: "Right Return Lane", 40: "Right Outlane",
	49: "Upper Left Eject", 50: "Lower Left Eject", 51: "Left Jet Bumper", 52: "Right Jet Bumper", 53: "Lower Jet Bumper",
	54: "Right Slingshot", 55: "Left Slingshot", 56: "Spinner", 57: "Right Flipper (Lane Change Opto)",
	58: "Left Flipper (Lane Change Opto)", 59: "Clock Wheel Opto",
}
UNUSED_SWITCHES = frozenset({25, 26, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 60, 61, 62, 63, 64})
# Switch-Matrix Table cell wording, kept where it differs from the label of record.
MATRIX_WORDING = {
	2: "C Side Power A/C Relay", 3: "Game Start", 10: "Up/Down (L Ramp)", 11: "Ball Trough #1 (right)",
	12: "Ball Trough #2 (mid)", 13: "Ball Trough #3 (left)", 15: "Sub-P'fld Shooter 1", 16: "Sub-P'fld Shooter 2",
	18: "Grill Bonus", 22: "Hot Dog (C 3-Bk Dr Tgt)", 23: "Burger (C 3-Bk Dr Tgt)", 24: "Chili (C 3-Bk Dr Tgt)",
	27: "R Ramp Entry", 28: "R Ramp Exit", 29: "Cup Entry R Ramp", 30: "Root Beer (L 3-Bk Dr Tgt)",
	31: "Fries (L 3-Bk Dr Tgt)", 32: "Iced Tea (L 3-Bk Dr Tgt)", 36: "L Ramp Exit", 54: "BR Kicker (\"sling\")",
	55: "BL Kicker (\"sling\")", 57: "Flipper Right", 58: "Flipper Left", 59: "Clock Wheel",
}
# Switches parts list (printed page 74) description, kept where it differs from the label of record.
PARTS_LIST_WORDING = {
	2: "A/C Relay, C-Side", 3: "Game START (Credit)", 4: "R Coin Chute (USA)", 6: "L Coin Chute (USA)",
	10: "Up/Down (L Ramp)", 11: "Ball Trough #1 (left)", 12: "Ball Trough #2 (mdl)", 13: "Ball Trough #3 (right)",
	15: "Sub-P'fld Shooter 1", 16: "Sub-P'fld Shooter 2", 22: "3-Bank Dr Tgt Opto Bd", 23: "3-Bank Dr Tgt Opto Bd",
	24: "3-Bank Dr Tgt Opto Bd", 29: "Cup Entry (R Ramp)", 30: "3-Bank Dr Tgt Opto Bd", 31: "3-Bank Dr Tgt Opto Bd",
	32: "3-Bank Dr Tgt Opto Bd", 36: "L Ramp Exit", 37: "L Outlane", 38: "L Return Lane", 39: "R Return Lane",
	40: "R Outlane", 54: "Lwr R Kicker***", 55: "Lwr L Kicker***", 57: "R Flpr Lane Change**", 58: "L Flpr Lane Change**",
	59: "Clock Wheel Opto Bd",
}
ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 2: "A/C SELECT", 3: "CREDIT BUTTON", 4: "RT. COIN SWITCH", 5: "CNTR. COIN SWITCH",
	6: "LEFT COIN SWITCH", 7: "SLAM TILT", 8: "HIGH SCORE RESET", 9: "OUTHOLE", 10: "RAMP UP/DOWN", 11: "TROUGH 1 BALL",
	12: "TROUGH 2 BALLS", 13: "TROUGH 3 BALLS", 14: "SHOOTER LANE", 15: "RT. SUB. PFLD. 1", 16: "RT. SUB. PFLD. 2",
	17: "CUP", 18: "GRILL BONUS", 19: "EAT - E", 20: "EAT - A", 21: "EAT - T", 22: "HOT DOG", 23: "BURGER", 24: "CHILI",
	25: "NOT USED", 26: "NOT USED", 27: "RIGHT RAMP ENTRY", 28: "RIGHT RAMP EXIT", 29: "CUP ENTRY", 30: "ROOT BEER",
	31: "FRIES", 32: "ICED TEA", 33: "NOT USED", 34: "NOT USED", 35: "NOT USED", 36: "LEFT RAMP EXIT",
	37: "LEFT OUTLANE", 38: "LEFT RET. LANE", 39: "RIGHT RET. LANE", 40: "RIGHT OUTLANE", 41: "NOT USED", 42: "NOT USED",
	43: "NOT USED", 44: "NOT USED", 45: "NOT USED", 46: "NOT USED", 47: "NOT USED", 48: "NOT USED",
	49: "UPPER LEFT EJECT", 50: "LOWER LEFT EJECT", 51: "LEFT JET", 52: "RIGHT JET", 53: "BOTTOM JET", 54: "RIGHT SLING",
	55: "LEFT SLING", 56: "SPINNER", 57: "RIGHT FLIPPER", 58: "LEFT FLIPPER", 59: "WHEEL",
}
SWITCH_PARTS = {
	2: "5580-09555-01", 3: "SW-1A-126", 4: "27-1092", 6: "27-1092", 7: "27-1066", 8: "27-1008", 9: "5647-12133-12",
	10: "5647-12001-00", 11: "5647-09957-00", 12: "5647-09957-00", 13: "5647-12073-08", 14: "5647-12073-04",
	15: "5647-12073-32", 16: "5647-12073-33", 17: "5647-12073-17", 18: "B-12912-4", 19: "5647-12073-19",
	20: "5647-12073-19", 21: "5647-12073-19", 22: "p/o C-13205", 23: "p/o C-13205", 24: "p/o C-13205",
	27: "5647-12073-07", 28: "5647-12073-21", 29: "5647-12073-11", 30: "p/o C-13205", 31: "p/o C-13205",
	32: "p/o C-13205", 36: "5647-12073-21", 37: "5647-12073-19", 38: "5647-12073-19", 39: "5647-12073-19",
	40: "5647-12073-19", 49: "5647-12133-11", 50: "5647-12133-11", 51: "B-12030-2", 52: "B-12030-2", 53: "B-12030-2",
	56: "5647-12133-08", 57: "p/o D-12313", 58: "p/o D-12313", 59: "p/o D-12046",
}
# Construction is asserted only where a part number, footnote or assembly page identifies it.
SWITCH_TYPES = {
	1: "tilt", 2: "other", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button",
	22: "opto", 23: "opto", 24: "opto", 30: "opto", 31: "opto", 32: "opto", 57: "opto", 58: "opto", 59: "opto",
}
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"),
	4: ("GRN-YEL", "1J8-4", "Q48"), 5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"),
	7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_LABELS = {
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Auto-Up/Manual-Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic (SW2)", "service.cpu-diag"), -4: ("Sound Diagnostic (SW1)", "service.sound-diag"),
}
CABINET_SWITCH_ROLES = {
	1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin",
	7: "cabinet.slam-tilt", 8: "cabinet.service", 57: "cabinet.flipper", 58: "cabinet.flipper", 59: "cabinet.backbox",
}

# --- Switch placements: retained-table object centres in VPX units, the object the script binds to each address.
SWITCH_OBJECTS = {
	9: ("Kicker Outhole", (448.32117, 1953.4423)),
	14: ("Trigger ShooterLane", (939.25, 1804.25)),
	17: ("Trigger Cup", (594.4753, 83.080246)),
	18: ("Primitive grillbonus (object position)", (249.05551, 347.26065)),
	19: ("Trigger E", (364.4198, 271.95645)), 20: ("Trigger A", (467.2099, 260.61725)),
	21: ("Trigger T", (568.3951, 247.24702)),
	22: ("HitTarget hotdog", (423.2391, 771.33136)), 23: ("HitTarget burger", (472.3559, 795.3541)),
	24: ("HitTarget chili", (522.07776, 819.9066)),
	27: ("Trigger RightRampEntry", (798.0, 730.0)), 28: ("Trigger RightRampExit", (523.5, 390.5)),
	29: ("Trigger CupEntry", (638.5, 116.5)),
	30: ("HitTarget rootbeer", (134.51485, 1024.7632)), 31: ("HitTarget fries", (148.21034, 971.56146)),
	32: ("HitTarget icedtea", (160.58899, 919.6768)),
	36: ("Trigger LeftRampExit", (390.5, 366.0)),
	37: ("Trigger LeftOutlane", (78.27468, 1481.6018)), 38: ("Trigger LeftReturnlane", (156.06482, 1456.932)),
	39: ("Trigger RightReturnLane", (775.3549, 1455.6172)), 40: ("Trigger RightOutlane", (848.3549, 1475.6172)),
	49: ("Kicker UpperEject", (236.61113, 97.740746)), 50: ("Kicker Lowkicker", (222.5, 241.5)),
	51: ("Bumper LeftJetBumper", (402.63742, 484.75214)), 52: ("Bumper RightJetBumper", (618.5554, 461.3021)),
	53: ("Bumper LowerJetBumper", (525.975, 654.3496)),
	54: ("Wall RSling (drag-point mean)", (681.108805, 1435.7498)),
	55: ("Wall LSling (drag-point mean)", (249.6972033, 1439.6479)),
	56: ("Spinner Spinner", (769.82306, 373.2726)),
}
BALL_RELEASE = (871.40625, 1677.1719)
OUTHOLE = (448.32117, 1953.4423)
LOCK_RAMP = (130.44453, 423.889)
SUBWAY_POPPER = (943.25964, 982.63446)
# Documented projections: a sensor with no table object of its own, placed on its own mechanism's object.
SWITCH_PROJECTIONS = {
	10: (LOCK_RAMP, (
		"Projected onto the table's lock (Cash Register) ramp (Primitive lockramp, object position), the moving part of the "
		"B-11304-2 Ramp Elevator Assembly whose switch this is (5647-12001-00). The retained script has no switch object: it "
		"writes this address from SolRampUp/SolRampDown and its lockramptimer when the ramp reaches either end of travel "
		"(script lines 662-686)."
	)),
	11: (BALL_RELEASE, (
		"Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the "
		"trough as one three-ball cvpmTrough (bsTrough.initSwitches Array(11,12,13) with Initexit BallRelease, script lines "
		"462-471) and has no object per trough position. The switch drawing places 11 at the right end of the trough, under "
		"the shooter lane."
	)),
	12: (BALL_RELEASE, "Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11. The switch drawing places 12 left of 11 along the same trough."),
	13: (BALL_RELEASE, "Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 11. The switch drawing places 13 left of 12, next to the outhole (9)."),
	15: (SUBWAY_POPPER, (
		"Projected onto the table's sub-playfield popper (Kicker SubWaypopper, object centre), where the script's two-ball "
		"cvpmTrough bsSubWay holds the balls this switch counts (initSwitches Array(15,16), Initexit SubWaypopper, script "
		"lines 505-515); the switch sits in the B-13652 Sub-Playfield Shooter below the playfield and has no object of its own."
	)),
	16: (SUBWAY_POPPER, "Projected onto the table's sub-playfield popper (Kicker SubWaypopper); see switch 15."),
}
SWITCH_OBJECT_NOTES = {
	18: (
		"The table models the standup as a primitive whose own Hit event pulses this address (grillbonus_Hit, script line "
		"610); its object position agrees with the centre of its mesh within 3 units."
	),
	22: "The script's cvpmDropTarget dtright binds the three centre targets hotdog, burger and chili to 22-24 (script lines 482-487).",
	30: "The script's cvpmDropTarget dtleft binds the three left targets rootbeer, fries and icedtea to 30-32 (script lines 474-479).",
	49: "The script's cvpmSaucer bsUpperEject binds this kicker to 49 and kicks it with solenoid 5 (script lines 497-502, 628).",
	50: (
		"The script's cvpmSaucer bsLowKicker (commented \"lock ramp saucer\") binds this kicker to 50 and kicks it with "
		"solenoid 8 (script lines 490-494, 629)."
	),
}

# --- Solenoid Table (inside front cover, PDF 2; reprinted on printed page 32) and Solenoids/Flashers list (printed page 73).
# Switched A/C pairs: (A-side public, C-side public, CPU connection, A-side power, C-side power, driver, C-side CPU wire).
AC_PAIRS = {
	1: (1, 25, "1P11-1", "5J1-9: 5J4-9 (A)", "5J5-9 (C)", "Q33", "Gry-Brn"),
	2: (2, 26, "1P11-3", "5J1-7: 5J4-8 (A)", "5J5-8 (C)", "Q25", "Gry-Red"),
	3: (3, 27, "1P11-4", "5J1-6: 5J4-7 (A)", "5J5-7(C)", "Q32", "Gry-Orn"),
	4: (4, 28, "1P11-5", "5J1-5:  5J4-6 (A)", "5J5-5 (C)", "Q24", "Gry-Yel"),
	5: (5, 29, "1P11-6", "5J1-4: 5J4-5 (A)", "5J5-4 (C)", "Q31", "Gry-Grn"),
	6: (6, 30, "1P11-7", "5J1-3: 5J4-4 (A)", "5J5-3 (C)", "Q23", "Gry-Blu"),
	7: (7, 31, "1P11-8", "5J1-2: 5J4-2 (A)", "5J5-2 (C)", "Q30", "Gry-Vio"),
	8: (8, 32, "1P11-9", "5J1-1: 5J4-1 (A)", "5J5-1 (C)", "Q22", "Gry-Blk"),
}
SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Ramp Down", 3: "Center 3-Bank Drop Target Reset", 4: "Ramp Up", 5: "Upper Left Eject",
	6: "Sub-Playfield Shooter", 7: "Knocker", 8: "Lower Left Eject",
	9: "Right Ramp Flashers", 10: "Backbox and Playfield G.I. Relay", 11: "Left Ramp Flashers", 12: "A/C Select Relay",
	13: "Left 3-Bank Drop Target Reset", 14: "Diverter", 15: "Clock Wheel Motor (B)", 16: "Clock Wheel Motor (A)",
	17: "Left Jet Bumper", 18: "Left Slingshot", 19: "Right Jet Bumper", 20: "Right Slingshot", 21: "Lower Jet Bumper",
	22: "Shooter Lane Feeder",
	25: "Haji Flash", 26: "Babs Flash", 27: "Boris Flash", 28: "Pepe Flash", 29: "Buck Flash", 30: "Cup Flashers",
	31: "Clock Flashers", 32: "DINE-TIME Flashers",
}
SOLENOID_MANUAL_NUMBER = {address: f"{address:02d}A" for address in range(1, 9)}
SOLENOID_MANUAL_NUMBER.update({address: f"{address - 24:02d}C" for address in range(25, 33)})
SOLENOID_MANUAL_NUMBER.update({address: f"{address:02d}" for address in range(9, 23)})
SOLENOID_TABLE_WORDING = {
	1: "Outhole Kicker", 2: "Ramp Down", 3: "Center 3-Bk Dr Tgt Reset", 4: "Ramp Up", 5: "Upper Left Eject",
	6: "Sub-P'fld Shooter", 7: "Knocker (in Backbox)", 8: "Lower Left Eject", 9: "Right Ramp Flashers",
	10: "Backbox/Pl'fld  Illum Relay", 11: "Left Ramp Flashers", 12: "A/C Select Relay", 13: "Left 3-Bk Dr Tgt Reset",
	14: "Diverter", 15: "Clock Wheel (B)", 16: "Clock Wheel (A)", 17: "Left Jet Bumper", 18: "Left Kicker (\"sling\")",
	19: "Right  Jet Bumper", 20: "Right Kicker (\"sling\")", 21: "Lower Jet Bumper", 22: "Shooter Lane Feeder",
	25: "Haji Flash", 26: "Babs Flash", 27: "Boris Flash", 28: "Pepe Flash", 29: "Buck Flash", 30: "Cup Flashers",
	31: "Clock Flashers", 32: "DINE - TIME Flashers",
}
LIST_WORDING = {
	1: "Outhole Kicker", 2: "Ramp Down", 3: "Cen 3-Bk Dr Tgt Reset", 4: "Ramp Up", 5: "Upper Left Eject",
	6: "Sub-Playfield Shooter", 7: "Knocker (Backbox)", 8: "Lower Left Eject", 9: "Right Ramp Flash",
	10: "B'box/P'fld G I Relays*", 11: "Left Ramp Flash", 12: "A/C Select Relay**", 13: "Left 3-Bk Dr Tgt Reset",
	14: "Diverter", 15: "Clock Wheel Motor (B)", 16: "Clock Wheel Motor (A)", 17: "Left Jet Bumper",
	18: "Left Kicker (\"sling\")", 19: "Right Jet Bumper", 20: "Right Kicker (\"sling\")", 21: "Lower Jet Bumper",
	22: "Shooter Lane Feeder", 25: "Haji Flash", 26: "Babs Flash", 27: "Boris Flash", 28: "Pepe Flash", 29: "Buck Flash",
	30: "Cup Flash", 31: "Clock Flash", 32: "DINE-TIME Flash",
}
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "HAJI", 2: "RAMP DOWN", 26: "BABS", 3: "CENTER DROP BANK", 27: "BORIS", 4: "RAMP UP", 28: "PEPE",
	5: "UPPER LEFT EJECT", 29: "BUCK", 6: "SUB-PFLD SHOOTER", 30: "CUP FLASHERS", 7: "KNOCKER", 31: "CLOCK FLASHERS",
	8: "LOWER LEFT EJECT", 32: "DINE TIME FLSHRS", 9: "RT. RAMP FLASHERS", 10: "GEN. ILLUMINATION",
	11: "LT. RAMP FLASHERS", 12: "A/C SELECT", 13: "LEFT DROP BANK", 14: "DIVERTER", 15: "WHEEL B", 16: "WHEEL A",
	17: "LEFT JET", 18: "LEFT SLING", 19: "RIGHT JET", 20: "RIGHT SLING", 21: "BOTTOM JET", 22: "BALL RELEASE",
}
COIL_TEST_ORDER = (1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
SOLENOID_WIRE = {
	1: "Vio-Brn", 25: "Blk-Brn", 2: "Vio-Red", 26: "Blk-Red", 3: "Vio-Orn", 27: "Blk-Orn", 4: "Vio- Yel", 28: "Blk-Yel",
	5: "Vio-Grn", 29: "Blk-Grn", 6: "Vio-Blu", 30: "Blk-Blu", 7: "Vio-Blk", 31: "Blk-Vio", 8: "Vio-Gry", 32: "Blk-Gry",
	9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio",
	16: "Brn-Gry", 17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
}
CONTROLLED = {
	9: ("1P12-1", "5J2-9:5J6-9:2J4-10", "Q17"), 10: ("1P12-2", "5J2-8:5J6-8:2J4-11", "Q9"),
	11: ("1P12-4", "5J2-6:5J6-7:2J4-12", "Q16"), 12: ("1P12-5", "5J2-5", "Q8"),
	13: ("1P12-6", "5J2-4:5J6-5:2J4-13", "Q15"), 14: ("1P12-7", "5J2-3:5J6-3:2J4-14", "Q7"),
	15: ("1P12-8", "2J4-15: 2J11-2", "Q14"), 16: ("1P12-9", "2J4-16: 2J11-1", "Q6"),
	17: ("1P19-7", "5J3-7: 5J7-7", "Q75"), 18: ("1P19-4", "5J3-6: 5J7-6", "Q71"), 19: ("1P19-3", "5J3-3: 5J7-3", "Q73"),
	20: ("1P19-6", "5J3-4: 5J7-5", "Q69"), 21: ("1P19-8", "5J3-2: 5J7-2", "Q77"), 22: ("1P19-9", "5J3-1: 5J7-1", "Q79"),
}
SOLENOID_PART = {
	1: "AE-23-800", 25: "#89/906 flashlamps", 2: "SM-1-26-600", 26: "#89/906 flashlamps", 3: "AE-26-1200",
	27: "#89/906 flashlamps", 4: "AE-23-800", 28: "#89/906 flashlamps", 5: "AE-23-800", 29: "#89/906 flashlamps",
	6: "AE-23-800", 30: "#89/906 flashlamps", 7: "AE-23-800", 31: "#89 flashlamps", 8: "AE-23-800", 32: "#89 flashlamps",
	9: "#89/906 flashlamps", 10: "5580-09555-01", 11: "#906 flashlamps", 12: "5580-09555-01", 13: "AE-26-1200",
	14: "AE-26-1500", 15: "14-7948", 16: "14-7948", 17: "AE-23-800", 18: "AE-26-1200", 19: "AE-23-800",
	20: "AE-26-1200", 21: "AE-23-800", 22: "AE-23-800",
}
# The table's quantity suffix (p = playfield, g = backglass) per flasher circuit.
FLASHLAMP_QUANTITY = {
	25: (1, 1), 26: (1, 1), 27: (1, 1), 28: (1, 1), 29: (1, 1), 30: (4, 0), 31: (0, 2), 32: (1, 2), 9: (2, 1), 11: (2, 0),
}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "coil", 9: "flasher", 10: "gi",
	11: "flasher", 12: "relay", 13: "coil", 14: "coil", 15: "motor", 16: "motor", 17: "coil", 18: "coil", 19: "coil",
	20: "coil", 21: "coil", 22: "coil", 25: "flasher", 26: "flasher", 27: "flasher", 28: "flasher", 29: "flasher",
	30: "flasher", 31: "flasher", 32: "flasher",
}
# What the retained known-working script does with each address (script.vbs).
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn (line 339), which kicks a drained ball from the Outhole kicker into the trough",
	2: "SolRampDown (line 362), which lowers the table's lock ramp and closes switch 10 when it is down (lines 662-686)",
	3: "dtright.SolDropUp (line 359), raising the centre drop targets 22-24",
	4: "SolRampUp (line 361), which raises the lock ramp and opens switch 10 when it is up (lines 670-686)",
	5: "SolUpperEject (line 346), bsUpperEject.SolOut on Kicker UpperEject",
	6: "SolSubPlfdShooter (line 349), which fires bsSubWay out of Kicker SubWaypopper when it holds a ball",
	7: "vpmSolSound Knocker (lines 341 and 358)",
	8: "SolLowKicker (line 345), bsLowKicker.SolOut on Kicker Lowkicker",
	9: "SolFlash9 (line 347), lighting the two right flasher domes Flasher1 and Flasher2",
	10: "SolGIRelay (line 356), which turns every Light of its lightsGI collection off while the solenoid is on",
	11: "SolFlash11 (line 348), lighting the two left flasher domes Flasher3 and Flasher4",
	12: "SolACSelect (line 357), a relay sound only",
	13: "dtleft.SolDropUp (line 360), raising the left drop targets 30-32",
	14: "Sol14Diverter (line 363), which swings the right-ramp diverter divider179to201 and drops its blocking wall Sol14Closed",
	15: "the cvpmMech WheelMech (.Sol1 = 15, line 455), a stepper-solenoid mechanism driving the backglass clock hand",
	16: "the cvpmMech WheelMech (.Sol2 = 16, line 455)",
	17: "vpmSolSound bumperleft (line 342)", 19: "vpmSolSound bumperright (line 343)", 21: "vpmSolSound bumpermiddle (line 344)",
	22: "bsTrough.SolOut (line 340), kicking the next trough ball from Kicker BallRelease",
	23: "TiltSol (line 338), which enables the flipper keys while it is on",
	25: "SolHajiF (line 350), FlashCutout 33", 26: "SolBabsF (line 351), FlashCutout 34", 27: "SolBorisF (line 352), FlashCutout 35",
	28: "SolPepeF (line 353), FlashCutout 36", 29: "SolBuckF (line 354), FlashCutout 37",
	30: "SolCupF (line 355), lighting Flasher5light and Flasher5lightsec in the cup",
}
# Placements: (object, coordinate in VPX units) per bulb or effect location.
SOLENOID_OBJECTS = {
	1: [("Kicker Outhole", OUTHOLE)], 2: [("Primitive lockramp (object position)", LOCK_RAMP)],
	3: [("HitTarget burger, the bank's middle target", (472.3559, 795.3541))],
	4: [("Primitive lockramp (object position)", LOCK_RAMP)],
	5: [("Kicker UpperEject", (236.61113, 97.740746))], 6: [("Kicker SubWaypopper", SUBWAY_POPPER)],
	8: [("Kicker Lowkicker", (222.5, 241.5))],
	9: [("Primitive Flasher1 (dome, object position)", (644.8061, 399.972)), ("Primitive Flasher2 (dome, object position)", (752.65753, 545.7495))],
	11: [("Primitive Flasher3 (dome, object position)", (183.1762, 241.55226)), ("Primitive Flasher4 (dome, object position)", (112.328415, 20.932192))],
	13: [("HitTarget fries, the bank's middle target", (148.21034, 971.56146))],
	14: [("Primitive divider179to201 (pivot, object position)", (628.5605, 193.66422))],
	17: [("Bumper LeftJetBumper", (402.63742, 484.75214))], 19: [("Bumper RightJetBumper", (618.5554, 461.3021))],
	21: [("Bumper LowerJetBumper", (525.975, 654.3496))],
	18: [("Wall LSling (drag-point mean)", (249.6972033, 1439.6479))], 20: [("Wall RSling (drag-point mean)", (681.108805, 1435.7498))],
	22: [("Kicker BallRelease", BALL_RELEASE)],
	25: [("Light Light33 (Haji cutout insert)", (285.34735, 1297.0762))], 26: [("Light Light34 (Babs cutout insert)", (374.3602, 1274.6891))],
	27: [("Light Light35 (Boris cutout insert)", (462.02512, 1257.2661))], 28: [("Light Light36 (Pepe cutout insert)", (559.54913, 1262.027))],
	29: [("Light Light37 (Buck cutout insert)", (644.36096, 1285.3145))],
	30: [("Light Flasher5light (in the cup)", (462.8092, 96.50552))],
}
# Placements that are documented projections rather than the device's own table object.
SOLENOID_PROJECTED = {
	1: "the drain kicker the script's cvpmTrough receives balls on; the outhole kicker coil has no object of its own",
	2: "the lock ramp, the moving part the B-11304-2 Ramp Elevator's SM-1-26-600 armature coil lowers",
	3: "the bank's middle drop target; the reset coil sits below the bank and has no object of its own",
	4: "the lock ramp, which the B-11304-2 Ramp Elevator's AE-23-800 coil and lift crank raise",
	6: "the popper the script fires the sub-playfield ball from; the B-13652 shooter coil has no object of its own",
	13: "the bank's middle drop target; the reset coil sits below the bank and has no object of its own",
	14: "the diverter's pivot; the B-13346 Ramp Diverter coil sits under the right ramp and has no object of its own",
	22: "the ball-release kicker the script kicks from; the C-9638 feeder coil has no object of its own",
}
FLASHER_NOTES = {
	9: (
		"The Solenoid Table prints 2p,1g: two playfield bulbs and one backglass bulb. The playfield bulbs are the two right "
		"flasher domes the script lights for this address (Flasher1 at the right ramp's top and Flasher2 further down "
		"it), which are the placements; the backglass bulb has no playfield position."
	),
	11: (
		"The Solenoid Table prints 2p, both on the playfield. They are the two left flasher domes the script lights for this "
		"address (Flasher3 beside the upper left loop and Flasher4 in the top left corner), which are the placements; the "
		"solenoid drawing marks callout 11 twice at the same two places."
	),
	25: "",
	30: (
		"The Solenoid Table prints 4p, four playfield bulbs. The solenoid drawing draws callout 6C twice, each with two "
		"leaders: two at the cup and two on the right side of the playfield. The retained table models only the cup's light "
		"(Flasher5light and its companion Flasher5lightsec at the same point), which is the one placement; the other three "
		"bulbs have no table object."
	),
}
CUTOUT_FLASH_NOTE = (
	"The Solenoid Table prints 1p,1g: one playfield bulb in the customer's playfield cutout and one in the backglass. "
	"The retained script lights the cutout's insert light {light} for this address (FlashCutout {lamp}), the same Light "
	"object that carries the cutout's #555 lamp {lamp}, so the flashlamp and that lamp share the cutout; the placement is "
	"that light and the backglass bulb has no playfield position."
)

VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", "internal.game-on-enable", (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (pinned src/wpc/s11.h S11_GAMEONSOL 23), set from PIA0 CB2 in "
		"pia0cb2_w and used to gate the six special solenoids and the synthetic flipper outputs 45-48. It has no driver "
		"transistor and no Sol. No. of its own. In the retained gameplay runs it is 0 in attract mode, rises when a game "
		"starts, falls at the third plumb-bob tilt, rises again for the next ball and falls at game over (runs gameplay "
		"and game-on-23). The retained script binds SolCallback(23) = \"TiltSol\", which enables its flipper keys."
	)),
	24: ("Unassigned Solenoid Slot 24", "unused", "internal.unused-platform-slot", (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay C-side bank (25-32); no "
		"System 11 driver populates it and no Diner run published it."
	)),
	45: ("Synthetic Lower Right Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-right flipper power output (CORE_FIRSTLFLIPSOL = 45). dinerGameData declares "
		"FLIP_SWNO(58,57) with no FLIP_SOL, so core_updateSw fabricates 45/46 from the right button bit at public 82 and "
		"47/48 from the left bit at public 84 while the enable (23) is on. The manual confirms there is no driver behind "
		"them: the two flipper rows of the Solenoid Table carry no Sol. No. and no transistor, and note 1 says the CPU-board "
		"wire runs to the flipper switch on the cabinet. The retained script comments out SolCallback(sLRFlipper) and "
		"moves its flippers from the keys directly (lines 365-367 and 874-900)."
	)),
	46: ("Synthetic Lower Right Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-right flipper hold output; see address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper power output; see address 45."),
	48: ("Synthetic Lower Left Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper hold output; see address 47."),
	49: ("PinMAME Simulator Ball-Shooter Channel", "unused", "internal.unused-platform-slot", (
		"Platform-wide simulator-only output (CORE_FIRSTSIMSOL = 49); dinerGameData declares no simulator."
	)),
	50: ("Unassigned Solenoid Slot 50", "unused", "internal.unused-platform-slot", (
		"Unassigned gap below the custom-solenoid base (51). dinerGameData declares no custSol, so MACHINE_INIT(s11) sizes "
		"coreGlobals.nSolenoids as CORE_FIRSTCUSTSOL-1+0 = 50 and nothing above 50 is modelled."
	)),
}
UPPER_FLIPPER_NOTE = (
	"Platform generic upper-flipper address (CORE_FIRSTUFLIPSOL = 33). dinerGameData's FLIP_SWNO(58,57) sets no upper "
	"FLIP_SW or FLIP_SOL bit and core_getSol serves 33-36 only for WPC and SAM generations, so it reads as always zero. "
	"Diner has two flippers only: the Solenoid Table and the Solenoids/Flashers list name a lower right and a lower left "
	"flipper and nothing else."
)
OVERLAY_NOTE = (
	"Platform sound-overlay range (37-44). dinerGameData's hw.gameSpecific1 is S11_MUXSW2 only, so S11_SNDOVERLAY is unset "
	"and pia5cb2_w never diverts the sound byte to a solenoid pattern. Unpopulated on this machine."
)

# --- Lamp matrix (public address = (column-1)*8+row). Labels from the Lamp-Matrix Table (printed page 76).
LAMP_LABELS = {
	1: "Cash Register 20K", 2: "Cash Register 40K", 3: "Cash Register 60K", 4: "Cash Register 80K",
	5: "Cash Register 100K", 6: "Advance DINE TIME (Left Return Lane)", 7: "Advance DINE TIME (Right Return Lane)",
	8: "Extra Ball (Right Outlane)", 9: "Serve Again", 10: "Ramp Scores 500K (Left Ramp)",
	11: "Ramp Scores 500K (Right Ramp)", 12: "Lock (Left Ramp)", 13: "Release (Upper Right)", 14: "Rush 1 (Upper Right)",
	15: "Rush 2 (Lower Right)", 16: "Spinner", 17: "D (in DINER)", 18: "I (in DINER)", 19: "N (in DINER)",
	20: "E (in DINER)", 21: "R (in DINER)", 22: "E (Top Lane)", 23: "A (Top Lane)", 24: "T (Top Lane)",
	25: "Jukebox 1", 26: "Jukebox 2", 27: "Jukebox 3", 28: "Jukebox 4", 29: "Jukebox 5",
	30: "Hot Dog (Center Drop Target)", 31: "Burger (Center Drop Target)", 32: "Chili (Center Drop Target)",
	33: "Haji", 34: "Babs", 35: "Boris", 36: "Pepe", 37: "Buck",
	38: "Root Beer (Left Drop Target)", 39: "Fries (Left Drop Target)", 40: "Iced Tea (Left Drop Target)",
	41: "Grill Bonus 100K", 42: "Grill Bonus 150K", 43: "Grill Bonus 250K", 44: "Grill Bonus 1 Million",
	45: "Grill Bonus Extra Ball", 46: "Spot Food (Left)", 47: "Cup Scores 10X DINER Letter",
	48: "Extra Ball (Left Outlane)",
	61: "Top 5 Hits with Lit", 62: "Today's Special", 63: "DINE TIME Collect", 64: "Spot Food (Right)",
}
CLOCK_LAMPS = {49 + hour - 1: hour for hour in range(1, 13)}
for _address, _hour in CLOCK_LAMPS.items():
	LAMP_LABELS[_address] = f"{_hour} O'Clock DINE TIME (Backglass)"
LAMP_MATRIX_WORDING = {
	1: "20K (C Regstr)", 2: "40K (C Regstr)", 3: "60K (C Regstr)", 4: "80K (C Regstr)", 5: "100K (C Regstr)",
	6: "Adv DINE TIME (L Return Lane)", 7: "Adv DINE TIME (R Return Lane)", 8: "Extra Ball (Right Outlane)",
	10: "Ramp Scores 500K (L Ramp)", 11: "Ramp Scores 500K (R Ramp)", 12: "LOCK (L Ramp)", 13: "Release (Upr Right)",
	14: "RUSH 1 (Upr Right)", 15: "RUSH 2 (Lwr Right)", 17: "D (in DINER)", 18: "I (in DINER)", 19: "N (in DINER)",
	20: "E (in DINER)", 21: "R (in DINER)", 22: "E (2) (Top Lane)", 23: "A (2) (Top Lane)", 24: "T (2) (Top Lane)",
	30: "Hot Dog (C Dr Tgt)", 31: "Burger (C Dr Tgt)", 32: "Chili (C Dr Tgt)", 38: "Root Beer (L Dr Tgt)",
	39: "Fries (L Dr Tgt)", 40: "Iced Tea (L Dr Tgt)", 41: "100K Grill BONUS", 42: "250K Grill BONUS",
	43: "500K Grill BONUS", 44: "1 Million Grill BONUS", 45: "Extra Ball Grill BONUS", 46: "Spot Food (L)",
	47: "Cup Scores 10X Diner Letter", 48: "Extra Ball (Left Outlane)", 61: "Top 5 Hits w/Lit", 63: "Dine Time Collect",
	64: "Spot Food (R)",
}
for _address, _hour in CLOCK_LAMPS.items():
	LAMP_MATRIX_WORDING[_address] = f"{_hour} o'clock Dine Time"
ROM_LAMP_NAMES = {
	1: "CASH REG. 20K", 2: "CASH REG. 40K", 3: "CASH REG. 60K", 4: "CASH REG. 80K", 5: "CASH REG. 100K",
	6: "LEFT RETURN LANE", 7: "RT. RETURN LANE", 8: "RIGHT OUTLANE", 9: "SERVE AGAIN", 10: "LEFT RAMP 500K",
	11: "RIGHT RAMP 500K", 12: "LOCK", 13: "RELEASE", 14: "EJECT RUSH", 15: "HOLE RUSH", 16: "SPINNER",
	17: "DINER - D", 18: "DINER - I", 19: "DINER - N", 20: "DINER - E", 21: "DINER - R", 22: "EAT - E", 23: "EAT - A",
	24: "EAT - T", 25: "JUKEBOX NO. 1", 26: "JUKEBOX NO. 2", 27: "JUKEBOX NO. 3", 28: "JUKEBOX NO. 4",
	29: "JUKEBOX NO. 5", 30: "HOT DOG", 31: "BURGER", 32: "CHILI", 33: "HAJI", 34: "BABS", 35: "BORIS", 36: "PEPE",
	37: "BUCK", 38: "ROOT BEER", 39: "FRIES", 40: "ICED TEA", 41: "GRILL BONUS 100K", 42: "GRILL BONUS 150K",
	43: "GRILL BONUS 250K", 44: "GRILL BONUS 1MIL", 45: "EXTRA BALL", 46: "LEFT SPOT FOOD", 47: "CUP SCORES 10X",
	48: "LEFT OUTLANE", 61: "TOP 5 HITS W/LIT", 62: "TODAY'S SPECIAL", 63: "COLL. DINE TIME", 64: "RIGHT SPOT FOOD",
}
for _address, _hour in CLOCK_LAMPS.items():
	ROM_LAMP_NAMES[_address] = f"WHEEL {_hour} O'CLOCK"
# Bulb type from the Lamps list (printed page 77): 555 except where it prints 44.
LAMP_BULB_44 = frozenset({9, 16, 61})
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"),
	4: ("YEL-BLK", "1J7-4", "Q60"), 5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"),
	7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"),
	4: ("RED-YEL", "1J6-5", "Q83"), 5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"),
	7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
# Script-bound insert lights: the LightN member (LightObjectSecond) of each lamp, in VPX units.
LAMP_LIGHTS = {
	6: (153.38222, 1338.4987), 7: (776.66516, 1338.7933), 8: (848.60016, 1360.8556), 9: (466.5, 1659.333),
	10: (382.44446, 1472.5552), 11: (548.8439, 1473.4277), 12: (200.43881, 824.6326), 13: (702.7166, 603.82733),
	14: (672.9051, 700.96716), 15: (733.09283, 1221.4242), 16: (750.2885, 445.4172), 17: (336.6908, 1057.8464),
	18: (398.808, 1058.1588), 19: (462.64218, 1058.6272), 20: (525.0718, 1057.3784), 21: (589.68604, 1056.7539),
	22: (364.15192, 367.74054), 23: (467.42096, 355.93036), 24: (567.0, 345.0), 30: (379.4403, 831.30194),
	31: (421.5803, 891.4684), 32: (497.43216, 889.59546), 33: (285.34735, 1297.0762), 34: (374.3602, 1274.6891),
	35: (462.02512, 1257.2661), 36: (559.54913, 1262.027), 37: (644.36096, 1285.3145), 38: (204.55972, 1050.547),
	39: (255.82993, 993.30646), 40: (235.69643, 921.9028), 41: (322.4944, 606.91327), 42: (302.28705, 542.1591),
	43: (286.44614, 482.51346), 44: (268.5487, 423.28903), 45: (340.27844, 710.7685), 46: (246.2828, 811.04785),
	47: (671.4827, 1113.8818), 48: (79.72386, 1361.0599), 61: (937.8782, 393.79358), 62: (809.29553, 1073.0299),
	63: (621.5878, 867.3614), 64: (708.54193, 999.7828),
}
# Lamps 1-5: the lit windows of the cash register toy, world-space mesh bounding-box centres of the baked primitives.
REGISTER_WINDOWS = {
	1: ("Primitive register20k", (107.814, 532.237)), 2: ("Primitive register40k", (150.181, 521.2125)),
	3: ("Primitive register60k", (191.996, 512.606)), 4: ("Primitive register80k", (135.917, 555.1625)),
	5: ("Primitive register100k", (178.691, 543.4305)),
}
# Lamps 22-24: the second bulb of each E-A-T lamp, the raised sign at the back of the playfield (baked primitives).
EAT_SIGN = {
	22: ("Primitive circleE", (363.878, 51.064)), 23: ("Primitive circleA", (469.66, 51.064)),
	24: ("Primitive circleT", (574.607, 51.064)),
}
JUKEBOX = (851.420755, 126.625989)
# Playfield G.I.: every GIn Light of the retained lightsGI collection plus the bulb-mesh light in each jet bumper cap.
GI_LIGHTS = (
	("GI1", (864.426, 1125.218)), ("GI2", (682.78076, 1501.1036)), ("GI3", (718.6481, 1383.6631)),
	("GI4", (313.38687, 289.79865)), ("GI5", (517.5942, 263.54684)), ("GI6", (748.55865, 1589.9927)),
	("GI7", (524.3116, 772.31366)), ("GI8", (453.79318, 740.4125)), ("GI9", (52.410526, 1082.7336)),
	("GI10", (417.97952, 276.16907)), ("GI11", (84.410515, 839.2768)), ("GI12", (78.63272, 747.32605)),
	("GI13", (98.23769, 972.2149)), ("GI14", (179.2018, 1594.6748)), ("GI15", (242.65277, 1499.2307)),
	("GI16", (212.87035, 1380.1075)), ("GI17", (26.652746, 1149.8981)), ("GI18", (850.0386, 849.3246)),
	("GI19", (54.652752, 1007.67535)), ("GI20", (103.98608, 865.89764)), ("GI21", (856.28235, 1187.8239)),
	("GI22", (524.43066, 749.3055)), ("GI23", (474.65292, 720.86115)), ("GI24", (738.6528, 1696.8612)),
	("GI25", (200.87514, 1691.5272)), ("bumper2light2", (399.80164, 485.43845)),
	("bumper1light1", (616.82214, 465.77316)), ("bumper3light2", (526.92365, 655.4027)),
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Diner retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Diner extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Diner retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Diner retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Diner retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Diner retained extraction file count mismatch: {len(actual['files'])} != {EXTRACTION_FILE_COUNT}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def placement(identifier: str, role: str, xy: tuple[float, float], status: str, *refs: str) -> dict[str, Any]:
	x, y = norm(*xy)
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, points: list[tuple[float, float]], status: str | list[str], *refs: str) -> dict[str, Any]:
	statuses = status if isinstance(status, list) else [status] * len(points)
	placements = [
		placement(f"{identifier}.{role}" + (f".{index}" if len(points) > 1 else ""), role, xy, item_status, *refs)
		for index, (xy, item_status) in enumerate(zip(points, statuses), start=1)
	]
	order = {"candidate": 0, "observed": 1, "validated": 2}
	return {"status": min((p["provenance"]["status"] for p in placements), key=order.__getitem__), "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(address: int) -> str:
	if address in SOLENOID_LABELS:
		return f"device.{slug(SOLENOID_LABELS[address])}"
	return f"device.{slug(VIRTUAL_SOLENOIDS[address][0]) if address in VIRTUAL_SOLENOIDS else slug(solenoid_platform_label(address))}"


def solenoid_platform_label(address: int) -> str:
	if 33 <= address <= 36:
		return f"Unused Upper Flipper Slot {address}"
	if 37 <= address <= 44:
		return f"Unused Sound Overlay Slot {address}"
	raise KeyError(address)


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _excerpt(identifier: str, locator: str, filename: str, method: str = "manual", transcribed_by: str = "curator, read from the rendered pages") -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": True,
	}


def source_records() -> list[dict[str, Any]]:
	callout_seed_sha = _file_sha256(CALLOUT_SEED_PATH)
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog records for the eight-driver diner_* clone tree rooted at diner_l4",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c lines 33-36 INITGAME macro and line 1460 INITGAME(diner,GEN_S11C,s11_dispS11c,12,"
				"FLIP_SWNO(58,57),S11_LOWALPHA|S11_DISPINV,S11_MUXSW2): sxx.muxSol = 12, no sxx.ssSw entries, hw.display "
				"S11_LOWALPHA|S11_DISPINV and gameSpecific1 S11_MUXSW2; lines 1461-1516 the diner_* ROM sets and lines 1518-1525 "
				"CORE_GAMEDEF(diner,l4) and the seven CORE_CLONEDEFs; src/wpc/s11.h line 110 s11_dispS11c = s11_dispS11b2, "
				"S11_GAMEONSOL 23, the diagnostic switch numbers and the S11_MUXSW2/S11_SNDOVERLAY flags; src/wpc/s11.c line 70 "
				"s11_dispS11b2 (two DISP_SEG_16 rows of sixteen CORE_SEG16 characters, starts 0 and 20), lines 191-200 the "
				"switch-driven special-solenoid loop (empty for this game), setSSSol (line 537) and its WMS ssSolNo table, updsol "
				"(line 558, the muxSol copy of the low solenoid byte to 25-32 while 12 is pulsed), pia0cb2_w (line 611, "
				"S11_GAMEONSOL), pia4a_r (line 644) returning core_getSwCol without inversion, SWITCH_UPDATE(s11) line 796 "
				"(S11_MUXSW2: core_setSw(2, core_getSol(muxSol))), MACHINE_INIT(s11) output sizing and the diner_ output-type block "
				"(9 and 11 as #89 bulbs, 10 as a reverse #44 \"Playfield GI output\", 25-32 as #89 bulbs, commented \"Mux relay is "
				"solenoid #12\"); src/wpc/core.h CORE_FIRSTSSSOL 17, CORE_SSFLIPENSOL 23, CORE_FIRSTLFLIPSOL 45, CORE_FIRSTSIMSOL 49, "
				"CORE_FIRSTCUSTSOL 51, CORE_FLIPPERSWCOL 11 and DISP_SEG_16; src/wpc/core.c core_updateSw's FLIP_SWNO copy and "
				"synthetic 45-48; src/wpc/gen.h GEN_S11C (0x400, \"No CPU board sound\")"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, the Country jumper, the A/C mux alias bank, the S11_MUXSW2 switch-2 copy, special solenoids, the sound-overlay range, synthetic flipper outputs and the 81-88 flipper column",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "https://web.archive.org/web/20260207074232id_/https://www.ipdb.org/files/681/Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf",
			"original_filename": "Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf",
			"sha256": MANUAL_SHA256, "acquired_at": "2026-10-09T13:12:00Z", "source_id": "ipdb.681",
			"locator": (
				"IPDB machine 681 (Williams Diner, model 571, manufactured June 11, 1990; machine page "
				"https://www.ipdb.org/machine.cgi?id=681, read through https://web.archive.org/web/20250108053619id_/https://www.ipdb.org/machine.cgi?id=681, "
				"resource https://www.ipdb.org/files/681/Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf) "
				"downloaded through the Wayback Machine: the 106-page Williams DINER Operations Manual 16-571-101 (June 1990) with "
				"Section 3 schematics, 150 dpi grayscale scans with an OCR text layer that was used only to find pages. For "
				"Sections 1 and 2 the printed folio \"DINER n\" is PDF page n + 4. PDF 2 ROM and Jumper Table and Solenoid Table "
				"(reprinted on PDF 36); PDF 5-13 game operation and status displays; PDF 23-25 feature adjustments; PDF 34-43 "
				"Test/Diagnostic Procedures (Lamp-Matrix Table reprinted on PDF 35, Switch-Matrix Table on PDF 38); PDF 46-76 "
				"board and mechanism assembly parts lists; PDF 77-81 the Solenoids/Flashers and Switches lists with their numbered "
				"location drawings, the Switch-Matrix and Lamp-Matrix Tables with their wiring drawings and the Lamps list; PDF 83 "
				"Playfield Parts; PDF 105 a third copy of both matrix tables."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.diner.switch-matrix", "PDF page 79 (printed 75), with the copies on PDF 38 and 105, DINER Switch-Matrix Table and wiring drawing", "switch-matrix.md"),
				_excerpt("excerpt.diner.lamp-matrix", "PDF page 80 (printed 76), with the copies on PDF 35 and 105, DINER Lamp-Matrix Table and wiring drawing", "lamp-matrix.md"),
				_excerpt("excerpt.diner.solenoid-table", "PDF page 2 (inside front cover), with the copy on PDF 36 (printed 32), DINER ROM and Jumper Table and Solenoid Table", "solenoid-table.md"),
				_excerpt("excerpt.diner.switch-locations", "PDF page 78 (printed 74), Switches parts list and drawing callouts", "switch-locations.md"),
				_excerpt("excerpt.diner.lamp-locations", "PDF page 81 (printed 77), Lamps list and drawing callouts", "lamp-locations.md"),
				_excerpt("excerpt.diner.solenoid-flasher-locations", "PDF page 77 (printed 73), Solenoids/Flashers and Playfield Rubber Parts lists and drawing callouts", "solenoid-flasher-locations.md"),
				_excerpt("excerpt.diner.playfield-parts", "PDF pages 75, 82 and 83 (printed 71, 78 and 79), Posts, Playfield Rubber Locations and Playfield Parts", "playfield-parts.md"),
				_excerpt("excerpt.diner.mechanism-assemblies", "PDF pages 6-8, 44, 46-76 (printed 2-4, 40, 42-72), board and mechanism assembly parts lists", "mechanism-assemblies.md"),
				_excerpt("excerpt.diner.diagnostics-and-operation", "PDF pages 5, 8, 10-13, 23-25 and 34-43 (printed 1, 4, 6-9, 19-21 and 30-39), ROM summary, game operation, audits, feature adjustments and Test/Diagnostic Procedures", "diagnostics-and-operation.md"),
			],
		},
		{
			"id": AMENDMENT_SOURCE, "kind": "service_bulletin",
			"uri": "https://web.archive.org/web/20260209042301id_/https://www.ipdb.org/files/681/Williams_1990_Diner_Operations_Manual_Amendment_1_pp_15_16_from_1990_Service_Bulletin_Book.pdf",
			"original_filename": "Williams_1990_Diner_Operations_Manual_Amendment_1_pp_15_16_from_1990_Service_Bulletin_Book.pdf",
			"sha256": AMENDMENT_SHA256, "acquired_at": "2026-10-09T13:12:00Z", "source_id": "ipdb.681",
			"locator": (
				"IPDB machine 681 resource https://www.ipdb.org/files/681/Williams_1990_Diner_Operations_Manual_Amendment_1_pp_15_16_from_1990_Service_Bulletin_Book.pdf "
				"through the Wayback Machine: Operations Manual (16-571-101) Amendment #1, page 15 of the 1990 service bulletin "
				"book, which corrects the Diverter coil (Sol. 14) from AE-26-1200 to AE-26-1500 and the Aux Power Driver Board part "
				"number and fuse F1 in the Fuse Listing; page 16 is a general insert-board lamp-socket notice."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.diner.amendment-1", "Amendment #1, page 15, corrections 1 and 2", "amendment-1.md"),
			],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH),
			"locator": (
				"Pinned LibPinMAME runs of diner_l4, each from a new state directory inheriting only the retained initialization "
				"run's NVRAM: the Coil Test paired step by step with the name the ROM displays, the Single Lamps test stepped "
				"through designators 01-64 with the Start button, the Switch Levels test over public 1-64 and 81-88, the C-Side "
				"test, two Wheel Test runs, twelve power-up probes with switches held from start and a gameplay run. Raw runs, "
				"manifest and hashes are retained outside the repository."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		},
	] + [
		{
			"id": variant_source(game), "kind": "runtime_scenario", "uri": f"internal:{variant_evidence_path(game).relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(variant_evidence_path(game)),
			"locator": (
				f"Pinned LibPinMAME Coil, Single Lamps and Switch Levels runs of {game}, from its own initialized NVRAM, each "
				"compared name by name and address by address with the diner_l4 run of the same test."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		}
		for game in VARIANT_GAMES
	] + [
		{
			"id": GAME_ON_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{GAME_ON_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": "8371478a7640f1896dcdf565aed340dc5df989ba", "sha256": _file_sha256(GAME_ON_EVIDENCE_PATH),
			"locator": (
				"Two hash-pinned LibPinMAME harness runs of diner_l4 recorded on an earlier pinned PinMAME revision: a "
				"factory-settings initialization from empty NVRAM (tools/harness-scenarios/system-11/diner-nvram-init.json), then a "
				"three-ball game from a fresh state holding only its .nv file (tools/harness-scenarios/system-11/diner-game-on-23.json). "
				"Public 23 is 0 in attract mode, rises during the start press, drops at the third plumb-bob tilt, rises again for "
				"ball 2, stays 1 through balls 2 and 3, and drops when ball 3 ends the game."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/diner-1990/source/Diner%20VPX%201.2.vpx",
			"original_filename": "Diner VPX 1.2.vpx", "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPX recreation of the physical machine by Flupper (version 1.2, based on Tamoore's VP9 "
				f"table, playfield redraw by Bodydump, per the script header), copied from the contributor's table collection. Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/1000 and y/2000. Geometry authority for "
				"script-bound table objects, checked against the manual's numbered locations drawings."
			),
			"license": "NOASSERTION", "attribution": "Flupper and the contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/diner-1990/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded script (1,170 lines). Runtime authority: cGameName = \"diner_l4\" (line 210), UseLamps = 0 "
				"with a LampTimer/ChangedLamps loop (lines 1004-1035) over its LightType/LightObjectFirst/LightObjectSecond tables "
				"(lines 245-317); switch constants (lines 229-238); SolCallback 1-11, 12, 13, 14, 22, 23 and 25-30 (lines 338-363); "
				"cvpmTrough trough (11, 12, 13, entry 10 noted, exit BallRelease) and sub-playfield trough (15, 16, SubWaypopper); "
				"cvpmSaucer ejects (49, 50); cvpmDropTarget banks 22-24 and 30-32; the cvpmMech clock (solenoids 15 and 16, switch "
				"59); the lock-ramp timer writing switch 10; the flipper keys driving the flippers while 23 is on."
			),
			"license": "NOASSERTION", "attribution": "Flupper and the contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads (script.vbs line 329 LoadVPM \"01560000\", \"S11.VBS\", "
				f"3.26), retained with core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and swLLFlip = 84 and "
				"sets them from the flipper keys in vpmKeyDown/vpmKeyUp, which the table's key handlers call directly."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.diner.vpm-script-library-flippers", "s11.vbs lines 37-40, 69-80 and 104; script.vbs lines 329, 365-367, 407, 411 and 874-903", "vpm-script-library-flippers.md", transcribed_by="curator, read from the library and script files"),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/diner-1990/extracted-vpxtool.manifest.json",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": (
				f"Retained vpxtool git:v0.33.3 extraction of the retained table, {EXTRACTION_FILE_COUNT} files, with a full sorted "
				f"path/size/SHA-256 manifest whose own SHA-256 is this record's sha256. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_OBJ_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/diner-1990/export-obj-vpu/Diner%20VPX%201.2.obj",
			"sha256": OBJ_EXPORT_SHA256,
			"locator": (
				"vpxtool git:v0.33.3 `export obj --units vpu` of the retained table, the world-space mesh of every object (OBJ x is "
				"playfield x, OBJ y is playfield y and OBJ z is minus the height). Used only for the baked-mesh primitives whose "
				"stored position is a local origin: the cash-register windows register20k-register100k and the E-A-T sign circles "
				"circleE, circleA and circleT, each placed at its world bounding-box centre. Control: the same export's Flasher1 dome "
				"centre (644.9, 400.1) lies within 0.2 units of that primitive's stored position."
			),
			"license": "NOASSERTION", "attribution": "vpxtool export of the retained table",
		},
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/williams/diner-1990-callouts.json", "sha256": callout_seed_sha,
			"locator": (
				"2026-10-09 factory location-drawing callout check of the solenoid (PDF 77), switch (PDF 78) and lamp (PDF 81) "
				"drawings: every callout read independently on gridded tiles of the retained renders without table data, verifier "
				"corrections recorded with their reasons, per-page control and callout fits; a table placement whose own callout "
				"lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py)."
			),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		},
	]


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11C CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


RUNTIME_SWITCH_NOTE = (
	" In the ROM's Switch Levels test (run switch-levels) holding public {address} at 1 makes the upper display show the "
	"ROM's name for it and the lower display its number, so the ROM reads it active at 1. dinerGameData has no "
	"inverted-switch mask and pia4a_r returns core_getSwCol raw, so the contact the matrix sees is open at rest and "
	"closed when actuated."
)
OPTO_NOTE = (
	" The manual identifies it as an optotransistor ({where}) and prints no rest state for it; the matrix contact rests "
	"open by the read-path rule stated below, whatever the beam does."
)
DROP_TARGET_NOTE = (
	" Apart from the reset it fires at Start with every target up, in the gameplay run the ROM fired this bank's reset coil "
	"({coil}) only once all three of the bank's switches were held at 1 (four pulses 0.5-0.6 s apart while they stayed there) "
	"and never for one or two, so public 1 is a dropped target."
)
MICROSWITCH_PARTS = ("5647-12073-", "5647-09957-", "5647-12001-")
MICROSWITCH_NOTE = (
	" Its 5647-series part is a microswitch: the assembly pages print that family as \"Microswitch\" or \"Sub-Mini "
	"Microswitch\" (Ball Trough Switches, Right Plastic Ramp, Sub-Playfield Shooter and Ramp Elevator assemblies)."
)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], roles=[role], normally_closed=False,
			physical={
				"location": "coin door and CPU board diagnostic switches", "switch_type": "button",
				"notes": (
					"System 11 diagnostic input on the S11_COMINPORT keyboard port. The manual's Game Control Locations and "
					"Test/Diagnostic Procedures drive every test from the coin-door ADVANCE button and AUTO-UP/MANUAL-DOWN "
					"switch (part of the 27-1008 Game Adjustment/Diagnostic Switches) and name the CPU board's SW 2 the CPU "
					"Diagnostic switch and its SW1 the sound diagnostic. The retained runs enter and step the tests with -6 and -7."
				),
			},
			spatial=not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		))
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		physical: dict[str, Any] = {}
		notes = f"Printed switch-matrix column {column} ({SWITCH_COLUMN_WIRING[column][0]}), row {row} ({SWITCH_ROW_WIRING[row][0]})."
		if address in ROM_SWITCH_NAMES:
			notes += f" The ROM's Switch Levels test names it \"{ROM_SWITCH_NAMES[address]}\"."
		if unused:
			notes += " The Switch-Matrix Table prints an empty cell here and the Switches parts list prints \"Not Used\"."
			if address >= 60:
				notes += " The Switch Levels test showed nothing while this address was held, so the ROM does not report it."
			else:
				notes += (
					" The Switch Levels test still reports a closure here as \"NOT USED\", so the ROM scans the position; no "
					"switch is fitted."
				)
		else:
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			elif address in SWITCH_PARTS and SWITCH_PARTS[address].startswith(MICROSWITCH_PARTS):
				physical["switch_type"] = "microswitch"
				notes += MICROSWITCH_NOTE
			elif address == 18:
				physical["switch_type"] = "leaf"
				notes += " The Standup Target assembly (B-12912-4) carries the SW-1A-184-4 Sta. Target Switch, a leaf switch."
			if address in MATRIX_WORDING and MATRIX_WORDING[address] != label:
				notes += f" The Switch-Matrix Table prints \"{MATRIX_WORDING[address]}\"."
			if address in PARTS_LIST_WORDING and PARTS_LIST_WORDING[address] != label:
				notes += f" The Switches parts list prints \"{PARTS_LIST_WORDING[address]}\"."
			if address == 11:
				notes += (
					" The parts list's \"(left)\" for #1 and \"(right)\" for #3 is reversed against two other pages: the "
					"Switch-Matrix Table prints #1 (right) and #3 (left), and the switch drawing places callouts 9, 13, 12 and "
					"11 left to right along the trough, 11 under the shooter-lane end where the feeder kicks. The label follows "
					"the matrix and the drawing; the ROM calls it \"TROUGH 1 BALL\", the switch closed with one ball home."
				)
			if address == 13:
				notes += " See switch 11 for the parts list's reversed left/right."
			if address in (11, 12, 13):
				notes += (
					" The manual says Diner \"normally uses three balls; however, it will operate with two balls\", and its "
					"assembly instructions say to install three balls of which only two are used in play at once (2-ball "
					"Multi-Ball)."
				)
			if address in (22, 23, 24, 30, 31, 32):
				notes += OPTO_NOTE.format(where="part of the C-13205 3-Bank Drop Target Opto Board, Opto Interruptor 5490-10159-00")
				notes += DROP_TARGET_NOTE.format(coil=3 if address < 30 else 13)
			if address in (57, 58):
				side = "right" if address == 57 else "left"
				button = 82 if address == 57 else 84
				notes += OPTO_NOTE.format(where="footnote **: \"Optotransistor on Backbox Interconnect Bd.\" (D-12313, opto isolators U1-U3)")
				notes += (
					f" It senses the {side} cabinet flipper button's circuit; the cabinet switch itself (SW-10A-48) fires the "
					"flipper coil directly. dinerGameData's FLIP_SWNO(58,57) without FLIP_SOL makes core_updateSw rewrite this "
					f"address from PinMAME's flipper column, public {button}, on every update, so a consumer cannot drive it "
					f"directly: it drives {button}, and the Switch Levels test shows \"{ROM_SWITCH_NAMES[address]}\" while "
					f"{button} is held. The Wheel Test uses the two flipper buttons to step the backbox clock by hand."
				)
			if address == 59:
				notes += OPTO_NOTE.format(where="\"p/o D-12046\", the opto of the clock's Motor Control Board, whose own parts list prints p/n D-12045 and an OPTO 1 Opto Interruptor Module")
				notes += (
					" It is the home sensor of the backbox DINE-TIME clock (C-12036-3): the retained script's clock cvpmMech "
					"reports it at position 0 of 60 (.AddSw 59, 0, 0, script line 457)."
				)
			if address == 2:
				notes += (
					" It is the C-side contact of the A/C Select Relay (5580-09555-01, K1 on the D-12247-566 Aux Power Driver "
					"Board in the backbox). dinerGameData sets S11_MUXSW2, so pinned SWITCH_UPDATE(s11) overwrites public switch "
					"2 with the live state of solenoid 12 on every update: a recreation reads it and never drives it. In the "
					"C-Side test (run c-side-test) the ROM alternates 12 and shows \"C-SIDE\" while 12 is energized and nothing "
					"while it is released. The Switch Levels name appeared only because the harness's held pulse rewrote the "
					"address on every poll."
				)
			if address == 5:
				notes += (
					" The Switches parts list prints item 5 \"Not Used\" with this description because the USA door has two "
					"chutes; the Coin Door Assembly lists both a 2-chute (09-17002-x) and a 3-chute (09-17003-x) door, so the "
					"center chute switch is fitted only with the 3-chute door. The ROM names and reads it."
				)
			if address in (54, 55):
				notes += (
					" The Switches list prints no part number for the scoring switch and the footnote \"*** - Paired Kicker "
					"Actuating Switch: A-4834-H + B-8734-1\". In the gameplay run each closure of this address made the ROM fire "
					f"its slingshot coil ({20 if address == 54 else 18}) within one poll."
				)
			if address in (51, 52, 53):
				notes += (
					f" In the gameplay run each closure of this address made the ROM fire its jet bumper coil "
					f"({ {51: 17, 52: 19, 53: 21}[address] }) within one poll."
				)
			if address == 10:
				notes += (
					" It is the B-11304-2 Ramp Elevator's microswitch (5647-12001-00). In the gameplay run the ROM pulsed Ramp "
					"Down (2) six times about 0.8 s apart after Start while this switch stayed at 0, then stopped; the retained "
					"script closes it when its ramp is down and opens it when the ramp is up."
				)
			notes += RUNTIME_SWITCH_NOTE.format(address=address)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": _switch_wiring(column, row),
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if unused:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, RUNTIME_SOURCE)
		elif address == 2:
			availability = "used"
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in CABINET_SWITCH_ROLES:
			availability = "optional" if address == 5 else "used"
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address in (57, 58, 59):
				refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE) if address != 59 else (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		else:
			availability = "used"
			extra["normally_closed"] = False
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in SWITCH_PROJECTIONS:
				xy, reason = SWITCH_PROJECTIONS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "validated", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += " " + reason
			else:
				obj, xy = SWITCH_OBJECTS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += f" Placed at the retained table's {obj}, which the script binds to this address."
				if address in SWITCH_OBJECT_NOTES:
					notes += " " + SWITCH_OBJECT_NOTES[address]
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	column = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(58,57)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: Diner_KeyDown and Diner_KeyUp pass the {side} flipper key to "
				"S11.VBS vpmKeyDown/vpmKeyUp (script lines 895 and 902), which set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). In the Switch "
				f"Levels run holding this address showed \"{'LEFT FLIPPER' if side == 'left' else 'RIGHT FLIPPER'}\". The "
				f"physical counterpart is the {side} cabinet flipper button (SW-10A-48), which fires the flipper coil through "
				"the flipper circuit and is sensed by its lane-change optotransistor on the Backbox Interconnect Board."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(VPM_LIBRARY_SOURCE,),
	)
	for item in column:
		if item["availability"] == "used":
			item["normally_closed"] = False
	items.extend(column)
	items.append(_device(
		"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used",
		(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={
			"location": "System 11C CPU board", "switch_type": "dip",
			"notes": (
				"System 11's single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7 (pinned s11.c labels it \"Jumper "
				"W7\"). The manual's ROM and Jumper Table lists the CPU board's installed jumpers (W1, 2, 4, 5, 7, 8, 11, 14, 16, "
				"17, and 19) and its Special Preset Adjustments (Install German 1-6 and others) are the operator-facing "
				"counterpart of a country setup."
			),
		},
		spatial=not_applicable("dip_switch", MANUAL_SOURCE),
	))
	return items


# Behaviour each output showed in the runs, appended to its note.
SOLENOID_RUNTIME = {
	1: "In the gameplay run the ROM fired it once the drained ball closed the outhole switch (9); with 9 held from power-up it retried 11 times in 14 s (power-up probe).",
	2: "In the gameplay run the ROM pulsed it at Start and five more times about 0.8 s apart while the Up/Down switch (10) stayed open, then stopped.",
	3: "In the gameplay run the ROM pulsed it at Start and, once all three centre targets (22-24) were held down, four times 0.6 s apart.",
	4: "At power-up, with no ball in the trough, the ROM pulses it twice in its ball search (power-up probes).",
	5: "In the gameplay run the ROM pulsed it three times about 1.5 s apart while switch 49 was held closed; with 49 and 50 held from power-up it retried 7 times (power-up probe).",
	6: "With 15 (or 15 and 16) held from power-up the ROM pulsed it 7-8 times in 12 s (power-up probes); in the gameplay run it fired once, about 6.9 s after 15 closed.",
	8: "In the gameplay run the ROM pulsed it three times about 1.5 s apart while switch 50 was held closed.",
	10: "In the gameplay run the ROM energized it from the third plumb-bob tilt until the next ball started, the only span it was held in play.",
	12: "The ROM energizes it ahead of every C-side step of the Coil Test and releases it for every A-side step, and alternates it about every 2 s in the C-Side test.",
	13: "In the gameplay run the ROM pulsed it at Start and, once all three left targets (30-32) were held down, four times 0.5 s apart.",
	14: "In the gameplay run the ROM energized it as the ball passed Right Ramp Exit (28) and held it 3.75 s, until the ball closed the Cup switch (17).",
	15: "At power-up the ROM drives 15 and 16 for about 7.7 s whether the clock opto (59) is held open or closed (power-up probes), and the Wheel Test steps them continuously; PinMAME's smoothed solenoid state shows the stepper's phases as long on-spans, not as individual steps.",
	16: "See solenoid 15.",
	17: "In the gameplay run the ROM fired it within one poll of switch 51 closing.",
	18: "In the gameplay run the ROM fired it within one poll of switch 55 closing.",
	19: "In the gameplay run the ROM fired it within one poll of switch 52 closing.",
	20: "In the gameplay run the ROM fired it within one poll of switch 54 closing.",
	21: "In the gameplay run the ROM fired it within one poll of switch 53 closing.",
	22: "In the gameplay run the ROM fired it at Start and again 2 s later until the host opened trough switch 11; the game-on run shows it at every ball's serve.",
}


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	pair_of = {a: pair for pair, (a, c, *_rest) in AC_PAIRS.items() for a in (a, c)}
	for address in list(range(1, 23)) + list(range(25, 33)):
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		kind = SOLENOID_KIND[address]
		number = SOLENOID_MANUAL_NUMBER[address]
		step = COIL_TEST_ORDER.index(address) + 1
		notes = f"Solenoid Table entry {number} (\"{SOLENOID_TABLE_WORDING[address]}\")"
		if LIST_WORDING[address] != SOLENOID_TABLE_WORDING[address]:
			notes += f"; the Solenoids/Flashers list prints \"{LIST_WORDING[address]}\""
		notes += "."
		if address in pair_of:
			pair = pair_of[address]
			a_side, c_side, cpu, power_a, power_c, driver, cpu_wire = AC_PAIRS[pair]
			notes += (
				f" Switched pair {pair:02d}A/{pair:02d}C on driver {driver}: the \"A\" load is pulsed with the A/C Select Relay "
				f"(12) de-energized and the \"C\" load with it energized (the table's note 3). Pinned updsol publishes the A load "
				f"at {a_side} and the C load at {c_side}."
			)
			wiring = {
				"board": "System 11C CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu if address == a_side else f"{cpu} (C side, through the A/C Select Relay)",
				"power_connection": power_a if address == a_side else power_c,
			}
			if address == c_side:
				wiring["control_wire"] = cpu_wire
		else:
			cpu, power, driver = CONTROLLED[address]
			kind_word = "Controlled" if address <= 16 else f"Special #{address - 16}"
			notes += f" Solenoid Type \"{kind_word}\"."
			wiring = {
				"board": "System 11C CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu, "power_connection": power,
			}
		notes += (
			f" The ROM's Coil Test (run coil-test) pulses this address at step {step} of {len(COIL_TEST_ORDER)} while the upper "
			f"display shows \"{ROM_COIL_NAMES[address]}\"."
		)
		if 17 <= address <= 22:
			notes += (
				" dinerGameData is a plain INITGAME with no sxx.ssSw entries, so PinMAME publishes this special solenoid only "
				"when the ROM drives its PIA line itself (setSSSol, WMS ssSolNo order); the Coil Test shows the printed Special "
				"numbers 1-6 at public 17-22."
			)
		if address in SOLENOID_RUNTIME:
			notes += " " + SOLENOID_RUNTIME[address]
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		else:
			notes += " The retained script has no callback for this address."
		physical: dict[str, Any] = {"part_number": SOLENOID_PART[address]}
		if address in FLASHLAMP_QUANTITY:
			playfield, backglass = FLASHLAMP_QUANTITY[address]
			physical["quantity"] = playfield + backglass
		extra_roles: list[str] = []
		spatial: dict[str, Any] | None = None
		handled = True
		refs: tuple[str, ...] = (MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address == 14:
			refs = (MANUAL_SOURCE, AMENDMENT_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			notes += (
				" Amendment #1 corrects the Solenoid Table's AE-26-1200 to AE-26-1500 for this coil (and item 6 of the B-13346 "
				"Ramp Diverter Assembly), so the part number follows the amendment. The diverter sits on the right ramp: "
				"energized, it turns right-ramp shots into the cup (adjustment 43 \"DINER RAMP\" sets how easily it \"opens\" the "
				"cup)."
			)
		if address == 7:
			notes += " The manual puts it in the backbox (\"Knocker (in Backbox)\"; Knocker Assembly B-10686-1)."
			extra_roles = ["cabinet.knocker"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 31:
			notes += (
				" The Solenoid Table prints 2g: both bulbs are in the backglass, lighting the DINE-TIME clock. The retained "
				"script has no callback for it."
			)
			extra_roles = ["cabinet.backbox-flasher"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 12:
			notes += (
				" The A/C select relay (5580-09555-01, note 5: \"mounted on Aux Power Driver Bd, D-12247, in the backbox\"). "
				"Pinned PinMAME publishes its own state here and, while it is pulsed, moves the low solenoid byte to 25-32; it "
				"also copies this state into switch 2 (S11_MUXSW2), the relay's C-side contact the ROM reads."
			)
			extra_roles = ["internal.ac-select-relay"]
			spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in (15, 16):
			notes += (
				" One of the two windings (phases A and B) of the 14-7948 stepper motor of the backbox DINE-TIME clock (C-12036-3, "
				"Motor & Connector Assy B-12088 on the D-12045 Motor Control Board); the drive connections 2J4-15/16 and 2J11 "
				"stay in the backbox. The clock's single hand steps round the dial, homing on the Clock Wheel opto (59); see the "
				"clock mechanism."
			)
			extra_roles = ["cabinet.backbox"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 10:
			notes += (
				" This output drives two relays (5580-09555-01, K1 on each of two C-11998-1 General Illumination Relay Boards, the "
				"table's note 4a), one under the playfield and one on the backbox insert board, which switch the playfield and the "
				"backbox general illumination (the Solenoids/Flashers list prints \"B'box/P'fld G I Relays\" with the footnote "
				"\"for both Playfield and Backbox General Illumination\"). The Locations Diagram lists the relay board under both "
				"and labels the insert-board one \"Rly Bd Sol. 10\" while its parts list prints \"Relay Board (Sol. 11 Gen. Illum)\"; the Solenoid Table, the Solenoids/Flashers list and "
				"the ROM's \"GEN. ILLUMINATION\" all put it at 10. Energized means G.I. off: the ROM holds it through a tilt, the "
				"retained script turns its lightsGI collection off while it is on, and pinned PinMAME types it as a reverse-acting "
				"#44 \"Playfield GI output\". The manual prints no G.I. bulb count or layout; the placements are the 28 bulb "
				"lights of the retained table's lightsGI collection (each GIn Light and the bulb-mesh light in each jet bumper "
				"cap). A table's G.I. grouping is not the machine's wiring, so these placements stay observed and no quantity is "
				"asserted."
			)
			extra_roles = ["gi.playfield", "gi.backbox"]
			spatial = located(identifier, "emitter", [xy for _, xy in GI_LIGHTS], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
		elif address == 32:
			notes += (
				" The Solenoid Table prints 1p,2g: one playfield bulb and two in the backglass DINE-TIME sign. The solenoid "
				"drawing marks the playfield bulb with callout 8C beside the right ramp, but the retained table has no object "
				"for it and its script no callback, so the spatial key is omitted."
			)
			spatial = None
		else:
			handled = False
		if not handled:
			if address not in SOLENOID_OBJECTS:
				raise RuntimeError(f"no spatial disposition for solenoid {address}")
			objects = SOLENOID_OBJECTS[address]
			role = "emitter" if kind in ("flasher", "gi", "lamp") else "effect"
			status = "validated" if address in SOLENOID_PROJECTED else "observed"
			spatial = located(identifier, role, [xy for _, xy in objects], status, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
			if address in SOLENOID_PROJECTED:
				notes += f" Placed at the retained table's {objects[0][0]}, a documented projection onto {SOLENOID_PROJECTED[address]}."
			elif 25 <= address <= 29:
				notes += " " + CUTOUT_FLASH_NOTE.format(light=f"Light{address + 8}", lamp=address + 8)
			elif kind == "flasher":
				notes += " " + FLASHER_NOTES[address]
			else:
				notes += f" Placed at the retained table's {objects[0][0]}."
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": number}]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if extra_roles:
			extra["roles"] = extra_roles
		if spatial is not None:
			extra["spatial"] = spatial
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	for address in (23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
		if address in VIRTUAL_SOLENOIDS:
			label, availability, role, notes = VIRTUAL_SOLENOIDS[address]
		elif address <= 36:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", UPPER_FLIPPER_NOTE
		else:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", OVERLAY_NOTE
		refs = (CONTROLLER_SOURCE, CORE_SOURCE)
		if availability == "used":
			refs = (CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, GAME_ON_SOURCE, VPX_SCRIPT_SOURCE) if address == 23 else (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE)
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=[role], physical={"notes": notes},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"lamp.matrix-{address}"
		wiring = {
			"board": "System 11C CPU board",
			"drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
			"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
			"driver_transistor": f"column {LAMP_COLUMN_WIRING[column][2]}, row {LAMP_ROW_WIRING[row][2]}",
		}
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		label = LAMP_LABELS[address]
		notes = (
			f"Printed lamp-matrix column {column}, row {row}. In the Single Lamps test (run single-lamps) designator "
			f"{address:02d} blinks this address while the upper display shows \"{ROM_LAMP_NAMES[address]}\"."
		)
		if address in LAMP_MATRIX_WORDING and LAMP_MATRIX_WORDING[address] != label:
			notes += f" The Lamp-Matrix Table prints \"{LAMP_MATRIX_WORDING[address]}\"."
		if address in (42, 43):
			notes += (
				" The Lamp-Matrix Table and the Lamps list print "
				+ ("250K" if address == 42 else "500K")
				+ ", but the ROM's lamp name and the insert artwork of the retained table's redrawn playfield both read "
				+ ("150K" if address == 42 else "250K")
				+ " (the four Grill Bonus inserts read 100K, 150K, 250K and 1 MIL), so the label follows them and the printed "
				"value is kept here."
			)
		bulb = "#44" if address in LAMP_BULB_44 else "#555"
		physical: dict[str, Any] = {"part_number": bulb, "quantity": 2 if address in EAT_SIGN else 1}
		refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address in CLOCK_LAMPS:
			notes += (
				" One of the twelve hour lamps of the backbox DINE-TIME clock: the Lamps list prints \"(Backglass)\" for 49-60 and "
				"the lamp drawing draws none of them. The retained script leaves 49-60 unconnected (LightType 4)."
			)
			extra = {"roles": ["cabinet.backglass-indicator"], "spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE)}
		elif address in REGISTER_WINDOWS:
			obj, xy = REGISTER_WINDOWS[address]
			notes += (
				" A lamp inside the Cash Register toy (B-13656, lamp assembly C-13434) on the left side of the playfield; the lamp "
				f"drawing points its \"1 - 5\" callout there. Placed at the retained table's {obj}, the lit window the script "
				"shows for this lamp (LightType 1), at its world-space mesh bounding-box centre: the primitive's stored position "
				"is a local origin with the geometry baked into the mesh. The window is the part the bulb lights, not a modelled "
				"socket, so the placement stays observed."
			)
			extra = {"spatial": located(identifier, "emitter", [xy], "observed", VPX_TABLE_SOURCE, VPX_OBJ_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)}
			refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPX_OBJ_SOURCE)
		elif 25 <= address <= 29:
			notes += (
				" A lamp in the Jukebox (C-13661) at the top right; the lamp drawing points its \"25 - 29\" callout there. The "
				"retained table shows a decal Flasher for each of the five (juke25k ... juke150k, LightType 1) and all five share "
				"one drag-point centre on the jukebox, so the placement is that shared centre, a projection onto the jukebox with "
				"no per-bulb position."
			)
			extra = {"spatial": located(identifier, "emitter", [JUKEBOX], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)}
		else:
			xy = LAMP_LIGHTS[address]
			points = [xy]
			light = f"Light{address}"
			notes += f" Placed at the retained table's Light {light}, the insert light the script drives for this lamp."
			if address in EAT_SIGN:
				obj, sign = EAT_SIGN[address]
				points.append(sign)
				notes += (
					" The Lamp-Matrix Table marks it with the circled 2 of \"Multiple Lamps\" and the lamp drawing draws the number "
					"twice, at the top lane and at the round sign at the top of the playfield. The second placement is that sign, "
					f"the retained table's {obj} (world-space mesh bounding-box centre), which the script shows with this lamp "
					"(LightType 2); it stands on the back panel above the playfield surface."
				)
				refs = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPX_OBJ_SOURCE)
			if 33 <= address <= 37:
				notes += (
					f" The customer cutout at the front of the playfield also holds the #89/906 flashlamp of solenoid {address - 8}, "
					"which the script lights through the same Light."
				)
			sources = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_OBJ_SOURCE, MANUAL_SOURCE) if address in EAT_SIGN else (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
			extra = {"spatial": located(identifier, "emitter", points, "observed", *sources)}
		physical["notes"] = notes
		items.append(_device(
			identifier, label, "lamp", "pinmame.output.lamp", address, "used", refs,
			aliases=aliases, wiring=wiring, physical=physical, **extra,
		))
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start,
			"width": 16, "height": 1, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		}

	return [
		display("display.upper-alphanumeric", "Upper sixteen-character alphanumeric display (D-12232-1 Master Display Board)", 0, 0),
		display("display.lower-alphanumeric", "Lower sixteen-character alphanumeric display (D-12232-1 Master Display Board)", 1, 20),
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	m = (MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker", [output_id(1), output_id(22)],
			["switch.matrix-9", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13"],
			"A drained ball rests on the outhole switch (9) at the left end of the trough, and the Outhole Kicker (1, B-8039-2) "
			"kicks it into the trough, where up to three balls queue on Ball Trough #3 (13, left), #2 (12) and #1 (11, right, "
			"nearest the shooter lane; the ROM calls 11-13 TROUGH 1-3 BALL(S)). The Shooter Lane Feeder (22, Special #6, the "
			"C-9638 assembly) kicks the lead ball into the shooter lane (14). Three balls are installed but at most two are in "
			"play (2-ball Multi-Ball); the manual's Pinball Missing message reports a lost ball and the game runs on two. In the "
			"gameplay run the ROM fed the first ball at Start and repeated the feed 2 s later until trough #1 opened, and after "
			"the drain it kicked the outhole once. With no ball in the trough at power-up the ROM runs a ball search through "
			"4, 1, 2, 5, 8 and 6. The retained script models the trough as one three-ball cvpmTrough.",
			*m, assembly="C-9638 with B-8039-2",
		),
		mechanism(
			"mechanism.lock-ramp", "Cash Register (left) elevator ramp and lock", "diverter", [output_id(4), output_id(2)],
			["switch.matrix-10", "switch.matrix-50", "switch.matrix-36"],
			"The left ramp's end is lifted and lowered by the B-11304-2 Ramp Elevator (\"Ramp Mover\"): Ramp Up (4, an AE-23-800 "
			"coil on the B-13655 bracket driving the A-11137 lift crank through a plunger) raises it and Ramp Down (2, the "
			"SM-1-26-600 coil working the A-11139 armature and lift-crank lock) releases it to drop; the assembly's microswitch "
			"(10, 5647-12001-00) reports the ramp's position. Shots up the left (Cash Register) ramp pass Left Ramp Exit (36) "
			"and advance the cash register value (lamps 1-5, adjustment 42). Spelling D-I-N-E-R raises the ramp so that a ball "
			"can be locked (lamp 12 LOCK; adjustments 34 and 43), and a locked ball leads to 2-ball Multi-Ball; the retained "
			"script calls the Lower Left Eject (50, kicked by 8) its \"lock ramp saucer\". "
			"In the gameplay run the ROM pulsed Ramp Down at Start and five more times about 0.8 s apart while 10 stayed open; "
			"the retained script closes 10 when its ramp is down and opens it when the ramp is up.",
			*m, assembly="B-11304-2 with B-13662",
		),
		mechanism(
			"mechanism.ejects", "Upper and lower left eject holes", "kicker", [output_id(5), output_id(8)],
			["switch.matrix-49", "switch.matrix-50"],
			"Two saucers on the left (B-9361-R-1 Eject Hole Arm assemblies): the Upper Left Eject (49, kicked by 5) at the top "
			"left, whose awards (adjustment 46) can also be reached from the sub-playfield shooter, and the Lower Left Eject (50, "
			"kicked by 8) under the Cash Register ramp, which holds the locked ball. In the gameplay run the ROM kicked each "
			"three times about 1.5 s apart while its switch stayed closed.",
			*m, assembly="B-9361-R-1",
		),
		mechanism(
			"mechanism.right-ramp-and-cup", "Right ramp, diverter and coffee cup", "diverter", [output_id(14)],
			["switch.matrix-27", "switch.matrix-28", "switch.matrix-29", "switch.matrix-17"],
			"The right plastic ramp (D-13663) carries Right Ramp Entry (27) and Right Ramp Exit (28) micro switches. The Ramp "
			"Diverter (14, B-13346, coil AE-26-1500 per Amendment #1) on the ramp, when energized, sends the ball into the "
			"Coffee Cup (D-13660) at the top of the playfield: the ball passes Cup Entry (29) on the ramp and closes the Cup "
			"switch (17) in the cup. Spelling D-I-N-E-R \"opens\" the cup for the Cup Bonus (adjustment 43); "
			"the Cup Flashers (30) light it. In the gameplay run the ROM energized 14 as the ball passed 28 and released it when "
			"17 closed 3.75 s later. The retained script swings its diverter primitive and drops a blocking wall while 14 is on.",
			*m, assembly="D-13663 with B-13346 and D-13660",
		),
		mechanism(
			"mechanism.sub-playfield-shooter", "Today's Special sub-playfield shooter", "kicker", [output_id(6)],
			["switch.matrix-15", "switch.matrix-16"],
			"A shot into Today's Special drops the ball below the playfield into the B-13652 Sub-Playfield Shooter, a bell-"
			"armature kicker (AE-23-800, solenoid 6) with a three-position switch bracket carrying Sub-Playfield Shooter 1 (15) "
			"and 2 (16), which count the balls waiting there. The shooter fires the ball up the 12-6904 wireform (\"Sub-p'fld "
			"Shooter Ramp\"), from which it can reach the Upper Left Eject (adjustment 46). Today's Special awards a random "
			"feature (adjustment 39), and with adjustment 34 it can start Multi-Ball while a ball is locked. With 15 held from "
			"power-up the ROM fired 6 repeatedly; in play it fired once about 6.9 s after 15 closed.",
			*m, assembly="B-13652",
		),
		mechanism(
			"mechanism.center-drop-bank", "Center 3-bank drop targets (Hot Dog, Burger, Chili)", "drop_target_bank", [output_id(3)],
			["switch.matrix-22", "switch.matrix-23", "switch.matrix-24"],
			"Three drop targets (C-11223-1) in the centre: Hot Dog (22), Burger (23) and Chili (24), sensed by the optos of a "
			"C-13205 board and reset together by the AE-26-1200 coil (3). Lamps 30-32 sit in front of them. Completing a bank "
			"serves a customer (lamps 33-37, adjustment 37). In the gameplay run the ROM reset the bank at Start and, once all "
			"three were held down, retried the reset about every 0.6 s.",
			*m, assembly="C-11223-1 with C-13205",
		),
		mechanism(
			"mechanism.left-drop-bank", "Left 3-bank drop targets (Root Beer, Fries, Iced Tea)", "drop_target_bank", [output_id(13)],
			["switch.matrix-30", "switch.matrix-31", "switch.matrix-32"],
			"Three drop targets (C-11223-1) on the left: Root Beer (30, lower), Fries (31) and Iced Tea (32, upper), sensed by the "
			"optos of a second C-13205 board and reset together by the AE-26-1200 coil (13). Lamps 38-40 sit in front of them. "
			"In the gameplay run the ROM reset the bank at Start and, once all three were held down, retried about every 0.5 s.",
			*m, assembly="C-11223-1 with C-13205",
		),
		mechanism(
			"mechanism.dine-time-clock", "Backbox DINE-TIME clock", "motorized", [output_id(15), output_id(16)], ["switch.matrix-59"],
			"The backbox clock (C-12036-3) turns one hand (decal 31-1559-571-2) on a wheel (03-8161) round a twelve-hour dial lit "
			"by lamps 49-60 (one per hour) and the Clock Flashers (31). A 14-7948 stepper motor (Motor & Connector Assy B-12088) "
			"is driven through the D-12045 Motor Control Board from Clock Wheel (A) (16) and (B) (15), and the board's opto "
			"(59) marks the home position. The manual's Wheel Test moves the hand to 12 o'clock (position 001), steps it "
			"clockwise to 11:59 (191), runs a \"pendulum\" sweep 001-191, 021-181 ... down to 111, and in Manual-Down mode lets "
			"the flipper buttons step it one position (a tenth of a step) either way. The ROM's Single Lamps test names 49-60 "
			"\"WHEEL n O'CLOCK\". At power-up the ROM drives 15 and 16 for about 7.7 s with the opto held either way, and in the "
			"Wheel Test the display counts the positions while 15 and 16 run; PinMAME's smoothed solenoid state does not resolve "
			"the individual steps. The retained script models a 60-step stepper cvpmMech on 15 and 16 with the opto at position "
			"0 (vpmMechStepSol + vpmMechCircle), which is what a recreation needs to answer the ROM.",
			*m, assembly="C-12036-3 with D-12045",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [output_id(17), output_id(19), output_id(21)],
			["switch.matrix-51", "switch.matrix-52", "switch.matrix-53"],
			"Three B-9414-1 jet bumpers with B-9415-1 coils in the upper centre: Left (17, switch 51), Right (19, switch 52) and "
			"Lower (21, switch 53). They are special solenoids, but dinerGameData maps no switch to them in PinMAME: the ROM "
			"fires each through its PIA line within one poll of its switch closing (gameplay run), so a consumer drives only the "
			"switch. The #44 bulbs in the caps are playfield G.I.",
			*m, assembly="B-9414-1 with B-9415-1",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other", [output_id(18), output_id(20)], ["switch.matrix-55", "switch.matrix-54"],
			"Two B-12665 slingshot kickers above the flippers (AE-26-1200 coils): Left (18) with its scoring switch 55 (\"BL "
			"Kicker\") and Right (20) with 54 (\"BR Kicker\"). Each also has a paired kicker actuating switch (A-4834-H + "
			"B-8734-1) that the Switches list prints without a matrix address. In PinMAME the ROM fires each special solenoid "
			"within one poll of its scoring switch closing (gameplay run).",
			*m, assembly="B-12665",
		),
		mechanism(
			"mechanism.flippers", "Two flippers, cabinet-wired", "other", [], ["switch.matrix-58", "switch.matrix-57"],
			"Two flippers (C-13174-R and -L, FL-11630/50VDC coils). The cabinet buttons (SW-10A-48) fire the coils through the "
			"flipper circuit, so no Sol. No. or driver is printed for them and PinMAME fabricates 45-48 from the buttons at public "
			"82 and 84. A Flipper Lane Change optotransistor on the Backbox Interconnect Board senses each button for the CPU (58 "
			"left, 57 right), which core_updateSw copies from 84 and 82; the end-of-stroke switches in the coil circuit have no "
			"matrix address.",
			*m, assembly="C-13174-R with C-13174-L",
		),
		mechanism(
			"mechanism.top-lanes-and-standup", "E-A-T top lanes, Grill Bonus standup and spinner", "other", [],
			["switch.matrix-19", "switch.matrix-20", "switch.matrix-21", "switch.matrix-18", "switch.matrix-56"],
			"Three top rollover lanes E (19), A (20) and T (21) light the E-A-T lamps 22-24, each of which also lights the "
			"matching letter of the raised sign at the back of the playfield; the Grill Bonus standup (18, B-12912-4) advances "
			"the Grill Bonus ladder (lamps 41-45); the spinner (56) is lit by lamp 16.",
			*m,
		),
		mechanism(
			"mechanism.toys", "Cash register, jukebox and backbox people", "toy", [], [],
			"Static toys lit by the lamp matrix: the Cash Register (B-13656) at the left shows the 20K-100K values (lamps 1-5), and "
			"the Jukebox (C-13661) at the top right shows lamps 25-29. The left and right DINER People assemblies "
			"(B-13764-1 and -2: Haji, Babs, Cook and Boris, Buck, Pepe decals on wood spacers), printed on the clock's page, "
			"carry no lamp, coil or switch.",
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.ac-select", "A/C solenoid select relay", "other", [output_id(12)], ["switch.matrix-2"],
			"The A/C Select Relay (12) on the Aux Power Driver Board switches the solenoid supply between the \"A\" and \"C\" "
			"terminals so that each of the eight switched drivers (Q22-Q25, Q30-Q33) serves an \"A\" coil while it is released "
			"and a \"C\" flasher while it is energized. Pinned PinMAME publishes the C loads separately at 25-32 and copies the "
			"relay's state into switch 2, the relay's C-side contact the ROM checks in its C-Side test.",
			MANUAL_SOURCE, RUNTIME_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [output_id(7)], [],
			"The A-side load of pair 07 (7, AE-23-800) raps the B-10686-1 Knocker Assembly in the backbox for replays and specials.",
			MANUAL_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ac-relay-switch-2", "kind": "direct", "source": output_id(AC_RELAY), "destination": "switch.matrix-2",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	] + flipper_column_relationships(flip_swno=FLIP_SWNO, matrix_ids={57: "switch.matrix-57", 58: "switch.matrix-58"}, refs=(CORE_SOURCE, RUNTIME_SOURCE))


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
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


COVERAGE_MISSING = ["variant_differences", "spatial_placement"]


def build_base() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Diner", "manufacturer": "Williams", "year": 1990, "kind": "physical_pinball",
			"model_number": "571", "ipdb_id": 681, "opdb_id": "GRWBd-MLy5p",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "candidate",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x400", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	apply_legacy_aliases(definition)
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Diner device identifiers are not unique: {duplicates}")
	return definition


def apply_legacy_aliases(definition: dict[str, Any]) -> None:
	"""Carry the legacy import's numeric, zero-padded and named aliases by binding, while compatibility needs them."""
	legacy = load_json(LEGACY_ALIAS_SEED_PATH)["aliases"]
	devices = {(device["binding"]["group"], str(device["binding"]["device"])): device for device in definition["inputs"] + definition["outputs"]}
	for group, addresses in legacy.items():
		for address, aliases in addresses.items():
			device = devices.get((group, address))
			if device is None:
				raise RuntimeError(f"legacy alias target {group} {address} is not in the Diner definition")
			device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in aliases]


def build() -> tuple[dict[str, Any], dict[str, Any]]:
	definition = build_base()
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	return definition, decisions


def build_spatial_report(definition: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted = [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(device["binding"]["device"])
		else:
			located_inputs.append(device["binding"]["device"])
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": device["binding"]["device"]}
		spatial = device.get("spatial")
		if spatial is None:
			omitted.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	unvalidated = sorted(
		item["id"] for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "validated",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/1000; 0=left, 1=right",
			"y": "y/2000; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"unvalidated_placements": unvalidated,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=lambda item: (item["group"], item["address"])) for reason, values in sorted(na_outputs.items())},
		"omitted_outputs": sorted(omitted, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, (_, reason) in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."} for address, reason in sorted(SOLENOID_PROJECTED.items())]
		),
		"callout_check": drawing_callouts.summary(
			json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8")), decisions,
			CALLOUT_SEED_PATH.relative_to(ROOT).as_posix(), _file_sha256(CALLOUT_SEED_PATH),
		),
		"excluded_object_classes": [
			"LightNb Light objects: glow companions of each script-bound insert light LightN (LightObjectFirst)",
			"GInb and GI10b*/GI2b*/GI3b* Light objects: glow helpers of the lightsGI collection; the GIn lights and the three bulb-mesh bumper lights are the placements",
			"Flasher1lightsec-Flasher5lightsec and Flasher1light-Flasher4light: glow lights beside the modelled flasher domes",
			"Primitives baked at a local origin other than the cash-register windows and the E-A-T sign circles (sidewalls, ramps, apron, backwall)",
			"Triggers LRentrysound, RRentrysound, LeftRampEntry, LeftRampDrop, RightRampDrop, Cup2, CupExit and trigger1: sound and physics helpers with no switch binding",
			"Kicker subwayenter: the sub-playfield drop hole, which plays a sound only; the balls are counted at Kicker SubWaypopper",
			"Glowball1-3, GlowBatLightLeft/Right and the clock primitives clock and clockwijzer: ball, flipper and backglass decorations",
		],
		"unresolved": [],
	}


SPATIAL_BLOCKERS = [
	"Solenoid 10 (Backbox and Playfield G.I. Relay): the 28 placements are the bulb lights of the retained table's lightsGI "
	"collection. The manual prints no G.I. bulb count or layout and a table's grouping is not the machine's wiring, so they "
	"stay observed without a quantity.",
	"Solenoid 32 (DINE-TIME Flashers): the solenoid drawing marks its one playfield bulb (callout 8C) beside the right ramp, "
	"but the retained table has no object for it, so its spatial key is omitted.",
	"Solenoid 30 (Cup Flashers): the manual prints four playfield bulbs and the drawing two pairs of leaders (at the cup and on "
	"the right side), but the table models only the cup's light, so the one placement stays observed.",
	"Eleven checked table placements land beyond the 0.07 callout limit and stay observed: the cup flasher, the left and "
	"right jet bumpers, the upper left eject, lamp 12 and switches 17, 27, 28, 29, 36 and 49 (see the callout check). "
	"Most sit at the top of the playfield, above the drawings' bumper and flipper controls.",
	"Lamps 1-5 and 25-29: the cash register's windows and the jukebox decals are the parts the bulbs light, not modelled "
	"sockets (the five jukebox lamps share one point), so these placements stay observed.",
]


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["callout_check"]
	lines = [
		"# Diner (Williams, 1990) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/williams/diner-1990.json`; "
		f"its spatial dimension stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained known-working `Diner VPX 1.2.vpx` by Flupper, SHA-256 `{TABLE_SHA256}`, whose "
		f"embedded script (SHA-256 `{SCRIPT_SHA256}`) is the binding authority. Bounds are `{TABLE_BOUNDS}`; every coordinate "
		"is x/1000 and y/2000, rounded to at most six places.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker, bumper, "
		"spinner or primitive for a switch, the `LightN` insert light of each lamp, the modelled flasher dome or script-driven "
		"Light for a flasher, and each G.I. bulb light.",
		f"- {check['validated']} of the {check['checked']} table placements the manual's numbered drawings check land within 0.07 "
		"normalized of their own callout under both fits (rule below) and are validated; the others keep the table's `observed` "
		"status.",
		"- Sensors and coils with no table object of their own (the ramp, trough and sub-playfield switches, and the outhole, ramp, "
		"drop-reset, sub-playfield, diverter and feeder drives) are documented projections onto their own mechanism's object and "
		"are not checked against the drawings.",
		"- Baked-mesh primitives (the cash-register windows and the E-A-T sign circles) are placed at the centre of their "
		"world-space mesh from `vpxtool export obj --units vpu`.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the clock lamps 49-60, the clock flashers (31), "
		"the clock stepper (15, 16) and its opto (59), the knocker, the A/C relay and its contact, the cabinet, flipper-opto and "
		"diagnostic switches, the Country jumper and both displays.",
		"",
		"## Callout check",
		"",
		f"Rule: {check['rule']}",
		"",
	]
	for key, page in check["pages"].items():
		lines.append(
			f"- {key} ({page['locator']}): {page['controls']} controls, control RMS {page['control_rms']}, control leave-one-out max "
			f"{page['control_loo_max']}; {page['callout_pairs']} callout pairs, {page['callout_fit_pairs']} in the callout fit, "
			f"leave-one-out max {page['callout_loo_max']}."
		)
	lines += ["", f"Checked {check['checked']}, validated {check['validated']}."]
	if check["not_validated"]:
		lines += ["", "Not validated by the check:", ""]
		for pid, item in check["not_validated"].items():
			lines.append(f"- `{pid}`: " + ", ".join(f"{k} {v}" for k, v in item.items()))
	lines += ["", "## Explicit projections", ""]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with an omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the "
		"mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is "
		"refused: the G.I. placements come only from the table's grouping, the DINE-TIME playfield flasher has no placement, "
		"three cup flashers have no table object, and the PA-0 prototype driver's hardware is unknown, so `coverage.missing` is "
		"`[\"variant_differences\", \"spatial_placement\"]`. A G.I. lamp layout from the machine, a photograph or measurement of "
		"the DINE-TIME and cup flasher sockets, and the prototype's ROM (whose service tests name every address it drives) would "
		"close them.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Diner definition with a {STATUS} one: {stale}")
		stale.unlink()
	definition, decisions = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition, decisions)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Diner is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition, decisions = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Diner definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Diner seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition, decisions)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Diner spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Diner spatial review drifted from its deterministic curator: {markdown_path}")
	print("Diner definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed and the spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Diner extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Diner retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
