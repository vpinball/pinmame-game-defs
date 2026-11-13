"""Curate the physical Capcom Breakshot (1996) machine definition.

The builder is deterministic: every reviewed label, wiring detail and normalized coordinate is a
literal here, and the only files it reads are committed ones (the pinned catalog, the callout seed,
the committed excerpts and the runtime evidence bundle), so regeneration reproduces the definition,
its seed, the knowledge note and the spatial report byte for byte. Table placements start as
``observed`` and the factory location-drawing callout check (``tools/drawing_callouts.py`` over
``tools/seeds/capcom/breakshot-1996-callouts.json``) promotes the ones its drawings confirm; the
build refuses to finish while any placement is not validated. The record stays ``partial`` while any
fixed G.I. socket the lamp drawing marks lacks a checked position, and the build stops once none does,
so a promotion is made deliberately rather than by regeneration.

``--check`` refuses drift and an author-ready copy of the record, ``--regenerate`` writes every
artifact over the earlier partial record, and the two extraction modes write or verify the retained
VPX extraction manifest (both need ``PINMAME_VPX_SOURCES_ROOT``).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
	sys.path.insert(0, str(TOOLS))

import drawing_callouts  # noqa: E402

MACHINE_ID = "capcom.breakshot.1996"
DEFINITION_PATH = ROOT / "machines/partial/capcom/breakshot-1996.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/capcom/breakshot-1996.json"
SEED_PATH = ROOT / "tools/seeds/capcom/breakshot-1996.json"
CALLOUT_PATH = ROOT / "tools/seeds/capcom/breakshot-1996-callouts.json"
KNOWLEDGE_PATH = ROOT / "knowledge/capcom/breakshot-1996.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/capcom/breakshot-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/capcom/breakshot-1996.md"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/capcom/breakshot-service-diagnostics.json"
EXCERPT_DIR = ROOT / "evidence/excerpts/capcom.breakshot.1996"

# Pool Player is Illinois Pin Ball's 2000 conversion of Breakshot machines. PinMAME routes its one driver,
# pp100, exactly as Breakshot, but its own sources describe cabinets that differ, so it is a record of its own.
POOL_PLAYER_ID = "illinois-pinball.pool-player.2000"
POOL_PLAYER_PATH = ROOT / "machines/partial/illinois-pinball/pool-player-2000.json"
POOL_PLAYER_KNOWLEDGE_PATH = ROOT / "knowledge/illinois-pinball/pool-player-2000.md"
POOL_PLAYER_EXCERPT_DIR = ROOT / "evidence/excerpts/illinois-pinball.pool-player.2000"
POOL_PLAYER_WEB_URI = "external:pinmame-manuals/by-machine/illinois-pinball.pool-player.2000/web"
POOL_PLAYER_IPDB_SOURCE = "ipdb.illinois-pinball.pool-player.2000"
POOL_PLAYER_PINSIDE_SOURCE = "pinside.illinois-pinball.pool-player.2000"
POOL_PLAYER_NEWS_SOURCE = "pinball-news.illinois-pinball.pool-player.2000"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "7ce04ac647167a5fb15e0391099e8d0a52b93f91be467906c8d52d2eccb389b8"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-capcom"
MANUAL_SOURCE = "manual.capcom.breakshot.1996"
IPDB_SOURCE = "ipdb.capcom.breakshot.1996"
VPX_TABLE_SOURCE = "vpx-table.breakshot-vpw-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.breakshot-vpw-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.breakshot-vpw-1-1"
VPM_LIBRARY_SOURCE = "vpm-script-library.capcom-vbs-3-61"
SERVICE_SOURCE = "service-diagnostic.breakshot.bsv103"
GAMEPLAY_SOURCE = "runtime.breakshot.bsv103-gameplay"
CALLOUT_SOURCE = "drawing-callouts.breakshot-1996"
LEGACY_SOURCE = "legacy.game.brkshot"

MANUAL_SHA256 = "270a8c5ed8b8093696c242082aad47060ddffed7d6636cab95fb9e4cd6398e6d"
IPDB_PAGE_SHA256 = "e55786f9d19cfbe6c4be29732fafc6d39f4467f01bff0158e6b673c39ff3596d"
TABLE_SHA256 = "5b038fc3411647d405e43b0f56802e61067479a2ace702a5b3aca97835961932"
TABLE_SIZE = 184528896
TABLE_ARCHIVE_SHA256 = "ea49fea1ad86eaba1d712f1231f9d2c76c4af80624efc2cad53f99c9da95ec09"
TABLE_ARCHIVE_SIZE = 172884816
SCRIPT_SHA256 = "4d231b5737073c4df944b495a7c9bfe3b175ff42420872edf437099f538a7178"
VPM_CAPCOM_LIBRARY_SHA256 = "03323ded224c5e67b0f7703978529889339e1fd7f73ebdd15002a4a6b794a95e"
VPM_CORE_LIBRARY_SHA256 = "d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72"

EXTRACTION_RELATIVE_PATH = Path("capcom/breakshot-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("capcom/breakshot-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "0315f2b749cf9446af5a88a649417dc7e8935820629147627286f0d988778318"
EXTRACTION_FILE_COUNT = 1586
EXTRACTION_TOTAL_BYTES = 436686215
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

DRIVER_IDS = ("bsv103", "bsv102", "bsb105", "bsv100r", "bsv102r")
DRIVER_COMPATIBILITY = {
	"bsv103": (
		"identical",
		"Breakshot 1.3, the catalog's root driver: INITGAMEFF(bsv103, 5, ..., 0xa7da) in src/wpc/capgames.c, so it "
		"publishes the ROM's game-on (Fast Flips) flag as solenoid 51. The retained known-working table runs it "
		"(cGameName \"bsv103\") and every harness run behind this record booted it.",
	),
	"bsv102": (
		"identical",
		"Breakshot 1.2: plain INITGAME(bsv102, 5, ...) with the same gameno, so the same capInvSw5/capFlip5 switch and "
		"flipper definitions and the same three sound ROMs; plain INITGAME publishes no solenoid 51.",
	),
	"bsb105": (
		"identical",
		"Breakshot Beta 1.5: plain INITGAME(bsb105, 8, ...); capInvSw8 and capFlip8 equal the gameno-5 values, so the "
		"address topology is bsv103's without solenoid 51. Its sound set loads bsu28_b1.2 in place of u28_v11.bin.",
	),
	"bsv100r": (
		"compatible",
		"Breakshot Redemption 1.0 (source comment 'Redemption Version 1.0I'): plain INITGAME(bsv100r, 6, ...) with "
		"capInvSw6/capFlip6 equal to the gameno-5 values and a fourth sound ROM, u30_v10i.bin. Redemption firmware for "
		"this machine: the manual's Redemption menu (PDF 55), which it says is not in every software version, sets the "
		"game up for an optional ticket or token dispenser, driven from the CPU's J3 interface board (PB-6 wiring, PDF "
		"145) on lines PinMAME does not publish. No ROM image of it was run here. No solenoid 51.",
	),
	"bsv102r": (
		"compatible",
		"Breakshot Redemption 1.2 (source comment 'Redemption Version 1.2I'): plain INITGAME(bsv102r, 7, ...) with "
		"capInvSw7/capFlip7 equal to the gameno-5 values and the fourth sound ROM u30_v10i.bin. Redemption firmware for "
		"this machine with the manual's optional ticket or token dispenser, like bsv100r; not run here. No solenoid 51.",
	),
}
POOL_PLAYER_DRIVER_COMPATIBILITY = {
	"pp100": (
		"unknown",
		"Pool Player 1.0, declared in src/wpc/capgames.c as a clone of Breakshot's bsv103: plain INITGAME(pp100, 13, "
		"...) with capInvSw13/capFlip13 equal to Breakshot's gameno-5 values and Breakshot's three 1.1 sound ROMs, so "
		"PinMAME routes it exactly as Breakshot. Pinball News's report of the flyer describes three Pool Player "
		"versions, two with automatic ball launchers and one with a manual launcher, and no source says which of them "
		"this firmware ran. The authorized ROM library holds no copy, so nothing here was observed on it. No solenoid 51.",
	),
}

# --- Switches ----------------------------------------------------------------------------------
# address: (label, manual part, switch_type or None, roles)
CABINET_SWITCHES = {
	1: ("Coin Chute 1", None, None, ["cabinet.coin.1"]),
	2: ("Coin Chute 2", None, None, ["cabinet.coin.2"]),
	3: ("Coin Chute 3", None, None, ["cabinet.coin.3"]),
	4: ("Coin Chute 4", None, None, ["cabinet.coin.4"]),
	5: ("Left Flipper Button", "SW00127", "button", ["flipper.lower.left.button"]),
	6: ("Right Flipper Button", "SW00127", "button", ["flipper.lower.right.button"]),
	7: ("Start Button", "SW00130", "button", ["cabinet.start"]),
	8: ("Coin Door Open (Mode)", "SW00132", None, ["cabinet.coin-door"]),
}
CABINET_MANUAL_TEXT = {
	1: "*1 COIN DOOR-CHUTE 1, part cell '**'", 2: "*2 COIN DOOR-CHUTE 2, part cell '**'",
	3: "*3 COIN DOOR-CHUTE 3, part cell '**'", 4: "*4 COIN DOOR-CHUTE 4, part cell '**'",
	5: "*5 LEFT FLIPPER SW00127", 6: "*6 RIGHT FLIPPER SW00127", 7: "*7 START BUTTON SW00130",
	8: "*8 COIN DOOR OPEN (MODE) SW00132",
}
# Matrix switches the ROM reads (public 17-80), from the manual's table with the ROM's Switch Test names.
MATRIX_SWITCHES = {
	21: ("Upper Right Flipper Button", "SW00127", "button", ["flipper.upper.right.button"]),
	29: ("Coin Door Slam Tilt", "SW00121", None, ["cabinet.slam-tilt"]),
	30: ("Tilt Bob", "A-00065-1", "tilt", ["cabinet.tilt"]),
	33: ("Left Flipper EOS", "SW00127", None, []),
	34: ("Right Flipper EOS", "SW00127", None, []),
	35: ("Outhole", "SW00113", None, []),
	36: ("Ball Trough 1", "A0015604-3R", "opto", []),
	37: ("Ball Trough 2", "A0015604-3R", "opto", []),
	38: ("Ball Trough 3", "A0015604-3R", "opto", []),
	41: ("Left Slingshot", "SW00138", None, []),
	42: ("Right Slingshot", "SW00138", None, []),
	43: ("Shooter Lane", "SW00112", None, []),
	44: ("Left Inlane", "SW00111", None, []),
	45: ("Right Inlane", "SW00111", None, []),
	46: ("Left Outlane", "SW00112", None, []),
	47: ("Right Outlane", "SW00111", None, []),
	49: ("Right Drop Target (Left)", "SW00106", None, []),
	50: ("Right Drop Target (Center)", "SW00106", None, []),
	51: ("Right Drop Target (Right)", "SW00106", None, []),
	52: ("Right Drop Bank Standup", "SW00141", None, []),
	53: ("Left Orbit Opto", "A0020800-S", "opto", []),
	54: ("Right Orbit Opto", "A0020800-S", "opto", []),
	55: ("Captive Ball Standup", "SW00141", None, []),
	57: ("Left Star Bumper", "SW00126", None, []),
	58: ("Center Star Bumper", "SW00126", None, []),
	59: ("Right Star Bumper", "SW00126", None, []),
	60: ("Left Top Lane", "SW00111", None, []),
	61: ("Center Top Lane", "SW00111", None, []),
	62: ("Right Top Lane", "SW00111", None, []),
	63: ("Bankshot Lane", "SW00111", None, []),
	65: ("Center Pocket Opto", "A0021300", "opto", []),
	66: ("Center Post", "SW00118", None, []),
	67: ("Bonus Saucer", "SW00118", None, []),
	68: ("Center Pocket Left", "SW00139", None, []),
	69: ("Center Pocket Center", "SW00139", None, []),
	70: ("Center Pocket Right", "SW00139", None, []),
	71: ("Upper Right Flipper EOS", "SW00127", None, []),
	73: ("Left Drop Target (Left)", "SW00106", None, []),
	74: ("Left Drop Target (Center)", "SW00106", None, []),
	75: ("Left Drop Target (Right)", "SW00106", None, []),
	76: ("Left Drop Bank Standup", "SW00141", None, []),
	77: ("Left Lite Super Cue", "SW00140", None, []),
	78: ("Right Lite Super Cue", "SW00140", None, []),
	79: ("Captive Rollover", "SW00111", None, []),
}
MANUAL_SWITCH_TEXT = {
	21: "*21 UPPER RIGHT FLIPPER SW00127", 29: "22-29 NOT USED (the range's part cell filled black)", 30: "*30 TILT BOB A-00065-1",
	33: "33 LEFT FLIPPER E.O.S. SW00127", 34: "34 RIGHT FLIPPER E.O.S. SW00127", 35: "35 OUTHOLE SW00113",
	36: "36 BALL TROUGH 1 (OPTO), receiver A0015604-3R, transmitter A0015702-3R",
	37: "37 BALL TROUGH 2 (OPTO), receiver A0015604-3R, transmitter A0015702-3R",
	38: "38 BALL TROUGH 3 (OPTO), receiver A0015604-3R, transmitter A0015702-3R",
	41: "41 LEFT SLINGSHOT SW00138", 42: "42 RIGHT SLINGSHOT SW00138", 43: "43 SHOOTER LANE SW00112",
	44: "44 LEFT INLANE SW00111", 45: "45 RIGHT INLANE SW00111", 46: "46 LEFT OUTLANE SW00112", 47: "47 RIGHT OUTLANE SW00111",
	49: "49 RIGHT DROP (LEFT) SW00106", 50: "50 RIGHT DROP (CENTER) SW00106", 51: "51 RIGHT DROP (RIGHT) SW00106",
	52: "52 RIGHT DROP (STANDUP) SW00141", 53: "53 LEFT ORBIT (OPTO), receiver A0020800-S, transmitter A0020901",
	54: "54 RIGHT ORBIT (OPTO), receiver A0020800-S, transmitter A0020901", 55: "55 CAPTIVE BALL (STANDUP) SW00141",
	57: "57 LEFT STAR BUMPER SW00126", 58: "58 CENTER STAR BUMPER SW00126", 59: "59 RIGHT STAR BUMPER SW00126",
	60: "60 LEFT TOP LANE SW00111", 61: "61 CENTER TOP LANE SW00111", 62: "62 RIGHT TOP LANE SW00111", 63: "63 BANKSHOT LANE SW00111",
	65: "65 CENTER POCKET (OPTO), receiver A0021300, transmitter A0022601", 66: "66 CENTER POST SW00118",
	67: "67 BONUS SAUCER SW00118", 68: "68 CENTER POCKET (LEFT) SW00139", 69: "69 CENTER POCKET (CENTER) SW00139",
	70: "70 CENTER POCKET (RIGHT) SW00139", 71: "71 UPPER FLIPPER E.O.S. SW00127", 73: "73 LEFT DROP (LEFT) SW00106",
	74: "74 LEFT DROP (CENTER) SW00106", 75: "75 LEFT DROP (RIGHT) SW00106", 76: "76 LEFT DROP (STANDUP) SW00141",
	77: "77 LEFT LITE SUPER QUE SW00140", 78: "78 RIGHT LITE SUPER QUE SW00140", 79: "79 CAPTIVE ROLLOVER SW00111",
}
OPTO_TRANSMITTERS = {36: "A0015702-3R", 37: "A0015702-3R", 38: "A0015702-3R", 53: "A0020901", 54: "A0020901", 65: "A0022601"}
OPTO_SWITCHES = set(OPTO_TRANSMITTERS)
# The ROM's Switch Test: public -> (name, wiring text), exactly as the service excerpt prints them.
ROM_SWITCH_TEST = {
	1: ("COIN 1", "01) GRN-BRN"), 2: ("COIN 2", "02) GRN-RED"), 3: ("COIN 3", "03) GRN-ORG"), 4: ("COIN 4", "04) GRN-YEL"),
	17: ("UNUSED", "17)ROW WHT-BRN COL RED-BRN"), 18: ("UNUSED", "18)ROW WHT-RED COL RED-BRN"),
	19: ("UNUSED", "19)ROW WHT-ORG COL RED-BRN"), 20: ("UNUSED", "20)ROW WHT-YEL COL RED-BRN"),
	23: ("UNUSED", "23)ROW WHT-VIO COL RED-BRN"),
	25: ("UNUSED", "25)ROW WHT-BRN COL RED-BLK"), 26: ("UNUSED", "26)ROW WHT-RED COL RED-BLK"),
	27: ("UNUSED", "27)ROW WHT-ORG COL RED-BLK"), 28: ("UNUSED", "28)ROW WHT-YEL COL RED-BLK"),
	29: ("SLAM TILT", "29)ROW WHT-GRN COL RED-BLK"), 30: ("TILT BOB", "30)ROW WHT-BLU COL RED-BLK"),
	31: ("OPTIONAL BUY IN", "31)ROW WHT-VIO COL RED-BLK"), 32: ("DISPENSER NOTCH", "16) WHT-GRY"),
	33: ("L. FLIPPER EOS", "33)ROW WHT-BRN COL RED-ORG"), 34: ("R. FLIPPER EOS", "34)ROW WHT-RED COL RED-ORG"),
	35: ("OUTHOLE", "35)ROW WHT-ORG COL RED-ORG"), 36: ("TROUGH OPTO 1", "36)ROW WHT-YEL COL RED-ORG"),
	37: ("TROUGH OPTO 2", "37)ROW WHT-GRN COL RED-ORG"), 38: ("TROUGH OPTO 3", "38)ROW WHT-BLU COL RED-ORG"),
	39: ("UNUSED", "39)ROW WHT-VIO COL RED-ORG"), 40: ("DISPENSER NOTCH", "16) WHT-GRY"),
	41: ("L. SLINGSHOT", "41)ROW WHT-BRN COL RED-YEL"), 42: ("R. SLINGSHOT", "42)ROW WHT-RED COL RED-YEL"),
	43: ("SHOOTER LANE", "43)ROW WHT-ORG COL RED-YEL"), 44: ("L. INLANE", "44)ROW WHT-YEL COL RED-YEL"),
	45: ("R. INLANE", "45)ROW WHT-GRN COL RED-YEL"), 46: ("L. OUTLANE", "46)ROW WHT-BLU COL RED-YEL"),
	47: ("R. OUTLANE", "47)ROW WHT-VIO COL RED-YEL"),
	49: ("R. DROP L.", "49)ROW WHT-BRN COL RED-GRN"), 50: ("R. DROP C.", "50)ROW WHT-RED COL RED-GRN"),
	51: ("R. DROP R.", "51)ROW WHT-ORG COL RED-GRN"), 52: ("R. DROP STANDUP", "52)ROW WHT-YEL COL RED-GRN"),
	53: ("L. ORBIT OPTO", "53)ROW WHT-GRN COL RED-GRN"), 54: ("R. ORBIT OPTO", "54)ROW WHT-BLU COL RED-GRN"),
	55: ("CAPTIVE STANDUP", "55)ROW WHT-VIO COL RED-GRN"),
	57: ("L. STAR BMPR", "57)ROW WHT-BRN COL RED-BLU"), 58: ("C. STAR BMPR", "58)ROW WHT-RED COL RED-BLU"),
	59: ("R. STAR BMPR", "59)ROW WHT-ORG COL RED-BLU"), 60: ("L. TOPLANE", "60)ROW WHT-YEL COL RED-BLU"),
	61: ("C. TOPLANE", "61)ROW WHT-GRN COL RED-BLU"), 62: ("R. TOPLANE", "62)ROW WHT-BLU COL RED-BLU"),
	63: ("BANKSHOT LANE", "63)ROW WHT-VIO COL RED-BLU"), 64: ("DISPENSER NOTCH", "16) WHT-GRY"),
	65: ("CNTR PKT OPTO", "65)ROW WHT-BRN COL RED-VIO"), 66: ("CENTER POST", "66)ROW WHT-RED COL RED-VIO"),
	67: ("BONUS SAUCER", "67)ROW WHT-ORG COL RED-VIO"), 68: ("CNTR PKT L", "68)ROW WHT-YEL COL RED-VIO"),
	69: ("CNTR PKT C", "69)ROW WHT-GRN COL RED-VIO"), 70: ("CNTR PKT R", "70)ROW WHT-BLU COL RED-VIO"),
	71: ("UR. FLIPPER EOS", "71)ROW WHT-VIO COL RED-VIO"), 72: ("DISPENSER NOTCH", "16) WHT-GRY"),
	73: ("L. DROP L.", "73)ROW WHT-BRN COL RED-GRY"), 74: ("L. DROP C.", "74)ROW WHT-RED COL RED-GRY"),
	75: ("L. DROP R.", "75)ROW WHT-ORG COL RED-GRY"), 76: ("L. DROP STANDUP", "76)ROW WHT-YEL COL RED-GRY"),
	77: ("L LITE SUPER Q.", "77)ROW WHT-GRN COL RED-GRY"), 78: ("R LITE SUPER Q.", "78)ROW WHT-BLU COL RED-GRY"),
	79: ("CAPTIVE ROLLOVR", "79)ROW WHT-VIO COL RED-GRY"),
}
# Switches the retained script reports with vpmTimer.PulseSw (the three bumpers, and Capcom.vbs's coin keys).
PULSED_SWITCHES = {1, 2, 3, 4, 57, 58, 59}
# Switch Test steps where only the switch grid changed; the other unnamed positions left the frame unchanged.
SWITCH_TEST_GRID_ONLY = {21, 22}
# Unused matrix positions: the manual prints NOT USED and the ROM names nothing on them.
UNUSED_MATRIX = (17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 31, 32, 39, 40, 48, 56, 64, 72, 80)
SWITCH_SCRIPT_NOTES = {
	41: (
		"The retained table reports its two slingshots crossed: Sub LeftSlingShotUpdate writes Controller.Switch(42) and "
		"Sub RightSlingShotUpdate writes 41, while the ROM's Switch Test, the manual's table and the switch drawing all put "
		"41 on the left slingshot. A defect of that table, not of the machine; the placement is the left slingshot."
	),
	42: (
		"The retained table reports its two slingshots crossed (Sub LeftSlingShotUpdate writes 42); the ROM's Switch Test, "
		"the manual's table and the switch drawing put 42 on the right slingshot, where this placement is."
	),
	49: (
		"The retained table numbers the right bank one lower than the machine: DT48/DT49/DT50 on walls sw48/sw49/sw50 and "
		"the standup ST51, and ResetDropsRight raises 48-50. The ROM's Switch Test names 49-51 the three drops and 52 the "
		"standup; in the harness 48 alone changed nothing, while dropping 49, 50 and 51 took the score from 0 to 9,000. The "
		"switch drawing P62500 also prints the bank's discs one lower (48-51) than its own table. This placement is the "
		"bank's left drop, wall sw48, checked against drawing disc 48."
	),
	50: "The right bank's centre drop: wall sw49 of the retained table, checked against drawing disc 49 (see switch 49).",
	51: "The right bank's right drop: wall sw50 of the retained table, checked against drawing disc 50 (see switch 49).",
	52: (
		"The standup behind the right bank: the retained table's HitTarget sw51, which it reports as 51; checked against "
		"drawing disc 51, which the drawing prints for this standup (see switch 49). The drawing prints no 52."
	),
	57: (
		"The retained table reports each star bumper as another one: Bumper2 (upper left) pulses 58, Bumper1 (lower centre) "
		"pulses 59 and Bumper3 (upper right) pulses 57. The ROM names 57 the left, 58 the centre and 59 the right star "
		"bumper, and the switch drawing prints 57 on the upper left, 58 on the lower centre and 59 on the upper right "
		"bumper, so this placement is the upper left bumper, Bumper2."
	),
	58: "The lower centre star bumper, Bumper1 of the retained table, which pulses 59 there (see switch 57).",
	59: "The upper right star bumper, Bumper3 of the retained table, which pulses 57 there (see switch 57).",
}
# Table object behind each switch placement: (VPX item type, name, (x, y)).
SWITCH_OBJECTS = {
	33: ("Flipper", "LeftFlipper", (0.290704, 0.853145)),
	34: ("Flipper", "RightFlipper", (0.617647, 0.853145)),
	35: ("Kicker", "sw35", (0.473173, 0.983458)),
	36: ("Kicker", "sw36", (0.822838, 0.886139)),
	37: ("Kicker", "sw37", (0.72043, 0.912315)),
	38: ("Kicker", "sw38", (0.618814, 0.938503)),
	41: ("Wall", "LeftSlingShot", (0.240931, 0.740162)),
	42: ("Wall", "RightSlingShot", (0.665642, 0.740338)),
	43: ("Trigger", "sw43", (0.944364, 0.890085)),
	44: ("Trigger", "sw44", (0.136861, 0.721506)),
	45: ("Trigger", "sw45", (0.771617, 0.72065)),
	46: ("Trigger", "sw46", (0.061369, 0.794347)),
	47: ("Trigger", "sw47", (0.848265, 0.742492)),
	49: ("Wall", "sw48", (0.758789, 0.182188)),
	50: ("Wall", "sw49", (0.792788, 0.204714)),
	51: ("Wall", "sw50", (0.827735, 0.227223)),
	52: ("HitTarget", "sw51", (0.803777, 0.185708)),
	53: ("Trigger", "sw53", (0.218877, 0.074505)),
	54: ("Trigger", "sw54", (0.716451, 0.054639)),
	55: ("HitTarget", "sw55", (0.18781, 0.168184)),
	57: ("Bumper", "Bumper2", (0.323502, 0.172067)),
	58: ("Bumper", "Bumper1", (0.453757, 0.233746)),
	59: ("Bumper", "Bumper3", (0.583646, 0.172576)),
	60: ("Trigger", "sw60", (0.342701, 0.106383)),
	61: ("Trigger", "sw61", (0.449766, 0.106383)),
	62: ("Trigger", "sw62", (0.557329, 0.106383)),
	63: ("Trigger", "sw63", (0.832773, 0.14651)),
	65: ("Trigger", "sw65", (0.391658, 0.383201)),
	66: ("Wall", "CenterPostWall001", (0.45357, 0.397578)),
	67: ("Trigger", "sw67", (0.857233, 0.488367)),
	68: ("Trigger", "sw68", (0.35573, 0.294635)),
	69: ("Trigger", "sw69", (0.455582, 0.294635)),
	70: ("Trigger", "sw70", (0.556723, 0.294635)),
	71: ("Flipper", "RightUpFlipper", (0.873614, 0.412999)),
	73: ("Wall", "sw73", (0.108193, 0.524532)),
	74: ("Wall", "sw74", (0.119516, 0.498053)),
	75: ("Wall", "sw75", (0.130838, 0.471129)),
	76: ("HitTarget", "sw76", (0.089295, 0.486775)),
	77: ("HitTarget", "sw77", (0.349244, 0.41335)),
	78: ("HitTarget", "sw78", (0.560877, 0.413151)),
	79: ("Trigger", "sw79", (0.188088, 0.216149)),
}
# The script never writes these; their placement is the mechanism the switch belongs to.
UNSCRIPTED_SWITCHES = {33, 34, 71}
# Trough positions under the apron: the drawings print their numbers without a part, so they are
# documented projections onto the script's trough objects rather than callout-checked placements.
TROUGH_PROJECTION = (
	"Under the apron, where the switch drawing prints 35 and the opto circles 36-38 without leaders in open space below "
	"the apron's edge (35 at the centre, then 38, 37 and 36 rising towards the shooter lane) and draws no part, so the "
	"drawing confirms the order but checks no coordinate. The placement is the known-working script's trough object "
	"for this position (it creates the three balls in sw38, sw37 and sw36, kicks the outhole ball from sw35 and serves "
	"from sw36), which spaces the trough about twice as widely as the drawing's circles; a documented projection."
)
TROUGH_SWITCHES = {35, 36, 37, 38}

# --- Solenoids -----------------------------------------------------------------------------------
# address: (label, kind, manual part, ROM name, control wire, control connection, power wire, volts)
SOLENOIDS = {
	1: ("Outhole", "coil", "CL00109", "OUTHOLE", "BRN-BLK", "J17/18.1", "VIO", 50),
	2: ("Trough", "coil", "CL00109", "TROUGH", "BRN-RED", "J17/18.2", "VIO", 50),
	3: ("Knocker", "coil", "CL00109", "KNOCKER", "BRN-ORG", "J17/18.3", "VIO", 50),
	4: ("Left Slingshot", "coil", "CL00109", "L. SLINGSHOT", "BRN-YEL", "J17/18.4", "VIO", 50),
	5: ("Right Slingshot", "coil", "CL00109", "R. SLINGSHOT", "BRN-GRN", "J17/18.5", "VIO", 50),
	6: ("Left Outlane Kicker", "coil", "CL00109", "KICKER", "BRN-BLU", "J17/18.6", "VIO", 50),
	7: ("Right Drop Reset", "coil", "CL00109", "R. DROP RESET", "BRN-VIO", "J17/18.7", "VIO", 50),
	8: ("Bonus Saucer", "coil", "CL00109", "BONUS SAUCER", "BRN-GRY", "J17/18.9", "VIO", 50),
	9: ("Left Flipper", "coil", "CL00111", "L. FLIPPER", "GRN-BRN", "J21/22.1", "VIO", 50),
	10: ("Right Flipper", "coil", "CL00111", "R. FLIPPER", "GRN-RED", "J21/22.2", "VIO", 50),
	11: ("Upper Right Flipper", "coil", "CL00111", "UR. FLIPPER", "GRN-ORG", "J21/22.3", "VIO", 50),
	12: ("Center Post Up", "coil", "CL00109", "CENTER POST UP", "GRN-YEL", "J21/22.4", "VIO", 50),
	13: ("Left Drop Reset", "coil", "CL00109", "L. DROP RESET", "GRN-BLK", "J21/22.5", "VIO", 50),
	14: ("Center Post Down", "coil", "CL00109", "CENTER POST DOWN", "GRN-BLU", "J21/22.7", "VIO", 50),
	15: ("Right Top Gate", "coil", "CL00112", "RIGHT TOPGATE", "GRN-VIO", "J21/22.8", "RED", 20),
	16: ("Left Top Gate", "coil", "CL00112", "LEFT TOPGATE", "GRN-GRY", "J21/22.9", "RED", 20),
	25: ("Center Pocket Left", "coil", "CL00109", "CNTR POCKET L", "GRY-BRN", "J26/27.1", "VIO", 50),
	26: ("Center Pocket Center", "coil", "CL00109", "CNTR POCKET C", "GRY-RED", "J26/27.2", "VIO", 50),
	28: ("Center Pocket Flash", "flasher", "LP00103", "CNTR POCKET FLASH", "GRY-YEL", "J26/27.5", "RED", 20),
	29: ("Right Star Bumper", "coil", "CL00109", "R STAR BUMPER", "GRY-GRN", "J26/27.6", "VIO", 50),
	30: ("Center Star Bumper", "coil", "CL00109", "C STAR BUMPER", "GRY-BLU", "J26/27.7", "VIO", 50),
	31: ("Left Star Bumper", "coil", "CL00109", "L STAR BUMPER", "GRY-VIO", "J26/27.8", "VIO", 50),
	32: ("Center Pocket Right", "coil", "CL00109", "CNTR POCKET R", "GRY-BLK", "J26/27.9", "VIO", 50),
}
MANUAL_SOLENOID_TEXT = {
	1: "S1 OUTHOLE", 2: "S2 TROUGH", 3: "S3 KNOCKER", 4: "S4 LEFT SLINGSHOT", 5: "S5 RIGHT SLINGSHOT", 6: "S6 KICKER",
	7: "S7 RIGHT DROP RESET", 8: "S8 BONUS SAUCER", 9: "S9 LEFT FLIPPER", 10: "S10 RIGHT FLIPPER",
	11: "S11 UPPER RIGHT FLIPPER", 12: "S12 CENTER POST UP", 13: "S13 LEFT DROP RESET", 14: "S14 CENTER POST DOWN",
	15: "S15 RIGHT TOPGATE", 16: "S16 LEFT TOP GATE", 25: "S25 CENTER POCKET LEFT", 26: "S26 CENTER POCKET CENTER",
	28: "S28 CENTER POCKET FLASH", 29: "S29 RIGHT STAR BUMPER", 30: "S30 CENTER STAR BUMPER", 31: "S31 LEFT STAR BUMPER",
	32: "S32 CENTER POCKET RIGHT",
}
SOLENOID_CALLBACKS = {
	1: "SolCallback(1) = \"SolTrough\" (sw35.kick 57, 20)",
	2: "SolCallback(2) = \"SolRelease\" (sw36.kick 60, 9)",
	3: "SolCallback(3) = \"vpmSolSound SoundFX(\"\"Knocker\"\",DOFKnocker),\" (sound only)",
	6: "SolCallback(6) = \"Kickback\" (PlungerKB.Fire while energized, PullBack on release)",
	7: "SolCallback(7) = \"ResetDropsRight\" (DTRaise 48, 49, 50: the table's numbering of the right bank, see switch 49)",
	8: "SolCallback(8) = \"RightSaucer\" (kicks the ball held in sw67 only while switch 67 is set)",
	9: "SolCallback(sLLFlipper) = \"SolLLFlipper\" (core.vbs sLLFlipper = 48, the hold mirror of this coil; moves LeftFlipper)",
	10: "SolCallback(sLRFlipper) = \"SolLRFlipper\" (core.vbs sLRFlipper = 46, the hold mirror of this coil; moves RightFlipper)",
	11: "SolCallback(sURFlipper) = \"SolURFlipper\" (core.vbs sURFlipper = 34, the hold mirror of this coil; moves RightUpFlipper)",
	12: "SolCallback(12) = \"PostUp\" (raises CenterPostWall001-003 and sets switch 66 when the post is up)",
	13: "SolCallback(13) = \"ResetDropsLeft\" (DTRaise 73, 74, 75)",
	14: "SolCallback(14) = \"PostRelease\" (drops CenterPostWall001-003 and clears switch 66 when the post is down)",
	15: "SolCallback(15) = \"SolRightGate\" (RightGate.Open while energized; the gate's own timer closes it after release)",
	16: "SolCallback(16) = \"SolLeftGate\" (LeftGate.Open while energized; the gate's own timer closes it after release)",
	25: "SolCallback(25) = \"CLeftPocket\" (kicks the ball held in sw68 only while switch 68 is set)",
	26: "SolCallback(26) = \"CenterPocket\" (kicks the ball held in sw69 only while switch 69 is set)",
	28: "SolModCallback(28) = \"FlashLight\" (sets s128a and s128b to the modulated level)",
	32: "SolCallback(32) = \"CRightPocket\" (kicks the ball held in sw70 only while switch 70 is set)",
}
SOLENOID_ROLES = {3: ["cabinet.knocker"]}
# Table object behind each solenoid placement.
SOLENOID_OBJECTS = {
	1: [("Kicker", "sw35", (0.473173, 0.983458))],
	2: [("Kicker", "sw36", (0.822838, 0.886139))],
	4: [("Wall", "LeftSlingShot", (0.240931, 0.740162))],
	5: [("Wall", "RightSlingShot", (0.665642, 0.740338))],
	6: [("Plunger", "PlungerKB", (0.060717, 0.845021))],
	7: [("Wall", "sw49", (0.792788, 0.204714))],
	8: [("Trigger", "sw67", (0.857233, 0.488367))],
	9: [("Flipper", "LeftFlipper", (0.290704, 0.853145))],
	10: [("Flipper", "RightFlipper", (0.617647, 0.853145))],
	11: [("Flipper", "RightUpFlipper", (0.873614, 0.412999))],
	12: [("Wall", "CenterPostWall001", (0.45357, 0.397578))],
	13: [("Wall", "sw74", (0.119516, 0.498053))],
	14: [("Wall", "CenterPostWall001", (0.45357, 0.397578))],
	15: [("Gate", "RightGate", (0.651893, 0.045613))],
	16: [("Gate", "LeftGate", (0.285781, 0.057124))],
	25: [("Trigger", "sw68", (0.35573, 0.294635))],
	26: [("Trigger", "sw69", (0.455582, 0.294635))],
	28: [("Light", "s128a", (0.349772, 0.264226)), ("Light", "s128b", (0.554865, 0.262926))],
	29: [("Bumper", "Bumper3", (0.583646, 0.172576))],
	30: [("Bumper", "Bumper1", (0.453757, 0.233746))],
	31: [("Bumper", "Bumper2", (0.323502, 0.172067))],
	32: [("Trigger", "sw70", (0.556723, 0.294635))],
}
SOLENOID_PLACEMENT_NOTES = {
	1: (
		"Under the apron: the solenoid drawing prints disc 1 below the flippers at the outhole, in open space below the "
		"apron's edge with no leader and no part drawn, so it checks no coordinate. The placement is the outhole kicker "
		"sw35 that the known-working script kicks on S1; a documented projection, like the trough switches."
	),
	2: (
		"Under the apron: the solenoid drawing prints disc 2 towards the lower right at the trough, in open space below "
		"the apron's edge with no leader and no part drawn, so it checks no coordinate. The placement is trough position "
		"1, kicker sw36, which the known-working script ejects into the shooter lane on S2; a documented projection, like "
		"the trough switches."
	),
	4: "The coil's effect anchor is the left slingshot wall the retained table kicks from (the table has no coil object).",
	5: "The coil's effect anchor is the right slingshot wall the retained table kicks from (the table has no coil object).",
	6: "The coil's effect anchor is the retained table's kickback plunger PlungerKB in the left outlane.",
	7: "The coil's effect anchor is the right bank's centre drop target, wall sw49 of the retained table.",
	8: "The coil's effect anchor is the bonus saucer, trigger sw67 of the retained table.",
	9: "The coil's effect anchor is the left flipper's pivot (the table's LeftFlipper).",
	10: "The coil's effect anchor is the right flipper's pivot (the table's RightFlipper).",
	11: "The coil's effect anchor is the upper right flipper's pivot (the table's RightUpFlipper).",
	12: "The coil's effect anchor is the centre post, wall CenterPostWall001 of the retained table.",
	13: "The coil's effect anchor is the left bank's centre drop target, wall sw74 of the retained table.",
	14: "The coil's effect anchor is the centre post, wall CenterPostWall001 of the retained table, shared with S12.",
	15: "The coil's effect anchor is the right top gate, gate RightGate of the retained table.",
	16: "The coil's effect anchor is the left top gate, gate LeftGate of the retained table.",
	25: "The coil's effect anchor is the left centre pocket, trigger sw68 of the retained table.",
	26: "The coil's effect anchor is the centre pocket, trigger sw69 of the retained table.",
	28: "The two bulbs are the retained table's lights s128a and s128b, which FlashLight drives together; the solenoid drawing prints two discs 28 above the pockets.",
	29: "The coil's effect anchor is the upper right star bumper, Bumper3 of the retained table.",
	30: "The coil's effect anchor is the lower centre star bumper, Bumper1 of the retained table.",
	31: "The coil's effect anchor is the upper left star bumper, Bumper2 of the retained table.",
	32: "The coil's effect anchor is the right centre pocket, trigger sw70 of the retained table.",
}
TROUGH_SOLENOIDS = {1, 2}
UNUSED_SOLENOIDS = (17, 18, 19, 20, 21, 22, 23, 24, 27)

# Virtual solenoids from src/wpc/capcom.c at the pinned revision.
VIRTUAL_SOLENOIDS = {
	33: ("Upper Right Flipper Power Mirror", "used", ["internal.duplicate.mirror"], "sURFlipPow (CORE_FIRSTUFLIPSOL + 0): io_w copies physical solenoid 11, the upper right flipper, here."),
	34: ("Upper Right Flipper Hold Mirror", "used", ["internal.duplicate.mirror"], "sURFlip (CORE_FIRSTUFLIPSOL + 1): io_w copies physical solenoid 11, the upper right flipper, here. core.vbs's sURFlipper constant is 34, so the retained table's SolURFlipper callback runs from this address."),
	35: ("Upper Left Flipper Power Mirror", "unused", ["internal.unused"], "sULFlipPow: the Breakshot drivers declare FLIP_L | FLIP_UR and no upper left flipper, so capcom.c clears this mirror instead of copying solenoid 12 here."),
	36: ("Upper Left Flipper Hold Mirror", "unused", ["internal.unused"], "sULFlip: cleared for the same reason as 35; Breakshot has no upper left flipper."),
	45: ("Right Flipper Power Mirror", "used", ["internal.duplicate.mirror"], "sLRFlipPow (CORE_FIRSTLFLIPSOL + 0): io_w copies physical solenoid 10, the right flipper, here."),
	46: ("Right Flipper Hold Mirror", "used", ["internal.duplicate.mirror"], "sLRFlip (CORE_FIRSTLFLIPSOL + 1): io_w copies physical solenoid 10, the right flipper, here. core.vbs's sLRFlipper constant is 46, so the retained table's SolLRFlipper callback runs from this address."),
	47: ("Left Flipper Power Mirror", "used", ["internal.duplicate.mirror"], "sLLFlipPow (CORE_FIRSTLFLIPSOL + 2): io_w copies physical solenoid 9, the left flipper, here."),
	48: ("Left Flipper Hold Mirror", "used", ["internal.duplicate.mirror"], "sLLFlip (CORE_FIRSTLFLIPSOL + 3): io_w copies physical solenoid 9, the left flipper, here. core.vbs's sLLFlipper constant is 48, so the retained table's SolLLFlipper callback runs from this address."),
	51: ("Game On (Fast Flips)", "used", ["internal.diagnostic"], "CORE_FIRSTCUSTSOL: bsv103 is declared with INITGAMEFF(..., 0xa7da), whose bsv103_getsol reports the ROM's flipper-enable byte at 0xa7da as this solenoid (Capcom.vbs GameOnSolenoid = 51, which the table's fast flips follow). bsv102, bsb105, bsv100r, bsv102r and pp100 use plain INITGAME and publish no address 51."),
}
for _address in range(37, 45):
	VIRTUAL_SOLENOIDS[_address] = (f"Unused Platform Solenoid {_address}", "unused", ["internal.unused"], "capcom.c never writes this address: Capcom has no WPC-style duplicate of 33-36.")
for _address in (49, 50):
	VIRTUAL_SOLENOIDS[_address] = (f"Unused Platform Solenoid {_address}", "unused", ["internal.unused"], "Below CORE_FIRSTCUSTSOL; capcom.c never writes it.")

# --- Lamps ---------------------------------------------------------------------------------------
# public: (label, manual text, bulb, part); ROM lamp-test names follow in ROM_LAMP_TEST.
LAMPS = {
	1: ("Start Button", "11B START BUTTON", "44", "LP00104"),
	3: ("Captive Ball 1", "13B CAPTIVE BALL 1", "555", "LP00100"),
	4: ("Captive Ball 2", "14B CAPTIVE BALL 2", "555", "LP00100"),
	5: ("Captive Ball 3", "15B CAPTIVE BALL 3", "555", "LP00100"),
	6: ("Shoot Again", "16B SHOOT AGAIN", "44", "LP00104"),
	7: ("Right Super Cue", "17B RIGHT  SUPER CUE", "44", "LP00104"),
	8: ("Captive Ball EB", "18B CAPTIVE BALL EB", "44", "LP00104"),
	9: ("1 Ball", "21B 1 BALL", "555", "LP00100"),
	10: ("2 Ball", "22B 2 BALL", "555", "LP00100"),
	11: ("Jackpot", "23B JACKPOT", "44", "LP00104"),
	12: ("Left Super Cue", "24B LEFT SUPER CUE", "44", "LP00104"),
	13: ("3 Ball", "25B 3 BALL", "555", "LP00100"),
	14: ("9 Ball", "26B 9 BALL", "555", "LP00100"),
	15: ("10 Ball", "27B 10 BALL", "555", "LP00100"),
	16: ("11 Ball", "28B 11 BALL", "555", "LP00100"),
	17: ("6 Ball", "31B 6 BALL", "555", "LP00100"),
	18: ("14 Ball", "32B 14 BALL", "555", "LP00100"),
	19: ("Left Drop Spot 9", "33B LEFT DROP SPOT 9", "555", "LP00100"),
	20: ("9 Ball Points", "34B 9 BALL POINTS", "555", "LP00100"),
	21: ("Rotation Option", "35B ROTATION OPTION", "44", "LP00104"),
	22: ("9 Ball Extra Ball", "36B 9 BALL XBALL", "555", "LP00100"),
	23: ("8 Ball Option", "37B 9 BALL OPTION", "44", "LP00104"),
	24: ("9 Ball Special", "38B 9 BALL SPECIAL", "555", "LP00100"),
	25: ("Left Center Pocket G.I.", "41B L. CENTER PKT. GI", "44", "LP00104"),
	26: ("Right Center Pocket G.I.", "42B R. CENTER PKT GI", "44", "LP00104"),
	27: ("Right Top Lane", "43B RIGHT TOPLANE", "44", "LP00104"),
	28: ("Kicker", "44B KICKER", "44", "LP00104"),
	29: ("4 Ball", "45B 4 BALL", "555", "LP00100"),
	30: ("Left Lite Super Cue", "46B LITE SUPER CUE", "555", "LP00100"),
	31: ("12 Ball", "47B 12 BALL", "555", "LP00100"),
	32: ("Center Top Lane", "48B CENTER TOPLANE", "44", "LP00104"),
	33: ("Orbit Spot 9", "51B ORBIT SPOT 9", "44", "LP00104"),
	34: ("Call Your Shot", "52B CALL YOUR SHOT", "555", "LP00100"),
	35: ("Collect Bonus", "53B COLLECT BONUS", "555", "LP00100"),
	36: ("8 Ball", "54B 8 BALL", "555", "LP00100"),
	37: ("13 Ball", "55B 13 BALL", "555", "LP00100"),
	38: ("Right Lite Super Cue", "56B LITE SUPER CUE R.", "555", "LP00100"),
	39: ("5 Ball", "57B 5 BALL", "555", "LP00100"),
	40: ("Ballorama", "58B BALLORAMA", "44", "LP00104"),
	41: ("9 Ball Option", "61B 9 BALL OPTION", "44", "LP00104"),
	42: ("Center Pocket Left", "62B CNTR. POCKET L.", "555", "LP00100"),
	43: ("Center Pocket Center", "63B CNTR. POCKET C.", "555", "LP00100"),
	44: ("Center Pocket Right", "64B CNTR POCKET R.", "555", "LP00100"),
	45: ("Left Top Lane", "65B LEFT TOPLANE", "44", "LP00104"),
	46: ("Right Drop Spot 9", "66B R. DROP SPOT 9", "555", "LP00100"),
	47: ("15 Ball", "67 15 BALL", "555", "LP00100"),
	48: ("7 Ball", "68B 7 BALL", "555", "LP00100"),
	49: ("Bank Shot", "71B BANK SHOT", "44", "LP00104"),
	**{50 + i: (f"Bonus Rack {i + 1}", f"{72 + i if i < 7 else 81 + i - 7}B BONUS RACK {i + 1}", "555", "LP00100") for i in range(15)},
}
ROM_LAMP_TEST = {
	1: "START BUTTON", 2: "OPTIONAL BUY IN", 3: "CAPTIVE BALL 1", 4: "CAPTIVE BALL 2", 5: "CAPTIVE BALL 3",
	6: "SHOOT AGAIN", 7: "R SUPER CUE", 8: "CAPTIVE BALL EB", 9: "1 BALL", 10: "2 BALL", 11: "JACKPOT",
	12: "L SUPER CUE", 13: "3 BALL", 14: "9 BALL", 15: "10 BALL", 16: "11 BALL", 17: "6 BALL", 18: "14 BALL",
	19: "L DROP SPOT BALL", 20: "9 BALL POINTS", 21: "ROTATION OPTION", 22: "9 BALL XBALL", 23: "8 BALL OPTION",
	24: "9 BALL SPCL", 25: "L CNTR PKT GI", 26: "R CNTR PKT GI", 27: "RIGHT TOPLANE", 28: "KICKER", 29: "4 BALL",
	30: "LITE SUPER CUE L", 31: "12 BALL", 32: "CENTER TOPLANE", 33: "ORBIT SPOT BALL", 34: "CALL YOUR SHOT",
	35: "COLLECT BONUS", 36: "8 BALL", 37: "13 BALL", 38: "LITE SUPER CUE R", 39: "5 BALL", 40: "BALLORAMA",
	41: "9 BALL OPTION", 42: "CNTR POCKET L", 43: "CNTR POCKET C", 44: "CNTR POCKET R", 45: "LEFT TOPLANE",
	46: "R DROP SPOT BALL", 47: "15 BALL", 48: "7 BALL", 49: "BANK SHOT",
	**{50 + i: f"BONUS RACK {i + 1}" for i in range(15)},
}
# The ROM's Lamp Test wiring: column and row lines (manual page 71 prints the column colours reversed).
LAMP_COLUMNS = {1: ("J5/6.1", "BLU-BRN"), 2: ("J5/6.2", "BLU-RED"), 3: ("J5/6.3", "BLU-ORG"), 4: ("J5/6.4", "BLU-YEL"),
                5: ("J5/6.5", "BLU-GRN"), 6: ("J5/6.6", "BLU-BLK"), 7: ("J5/6.8", "BLU-VIO"), 8: ("J5/6.9", "BLU-GRY")}
LAMP_ROWS = {1: ("J7/8.1", "ORG-BRN"), 2: ("J7/8.2", "ORG-RED"), 3: ("J7/8.4", "ORG-BLK"), 4: ("J7/8.5", "ORG-YEL"),
             5: ("J7/8.6", "ORG-GRN"), 6: ("J7/8.7", "ORG-BLU"), 7: ("J7/8.8", "ORG-VIO"), 8: ("J7/8.9", "ORG-GRY")}
# The manual's lamp matrix sheet (PDF page 147): the same colours, other connectors, and its own cell names.
SHEET_COLUMNS = {1: "J9/10.1", 2: "J9/10.2", 3: "J9/10.3", 4: "J9/10.4", 5: "J9/10.5", 6: "J9/10.7", 7: "J9/10.8", 8: "J9/10.9"}
SHEET_ROWS = {1: "J4/5.1", 2: "J4/5.2", 3: "J4/5.3", 4: "J4/5.5", 5: "J4/5.6", 6: "J4/5.7", 7: "J4/5.8", 8: "J4/5.9"}
SHEET_NAMES = {
	1: "Start Button (CABINET)", 3: "Captive Ball 1", 4: "Captive Ball 2", 5: "Captive Ball 3", 6: "Shoot Again",
	7: "Right Super Cue", 8: "Captive Ball Extra Ball", 9: "1 Ball", 10: "2 Ball", 11: "Jackpot (two)", 12: "Left Super Cue",
	13: "3 Ball", 14: "9 Ball", 15: "10 Ball", 16: "11 Ball", 17: "6 Ball", 18: "14 Ball", 19: "Left Drop Spot 9 Ball",
	20: "9 Ball Points", 21: "Rotation Option", 22: "9 Ball Extra Ball", 23: "8 Ball Option", 24: "9 Ball Special",
	25: "Left Center Pocket GI", 26: "Right Center Pocket GI", 27: "Right Toplane Diamond", 28: "Kickback", 29: "4 Ball",
	30: "Light Super Cue Left", 31: "12 Ball", 32: "Center Toplane Diamond", 33: "Orbit Spot 9 Ball", 34: "Call Your Shot",
	35: "Collect Bonus", 36: "8 Ball", 37: "13 Ball", 38: "Light Super Cue Right", 39: "5 Ball", 40: "Ball -O- Rama",
	41: "9 Ball Option", 42: "Center Pocket Left", 43: "Center Pocket Center", 44: "Center Pocket Right", 45: "Left Toplane Diamond",
	46: "Right Drop Spot 9 Ball", 47: "15 Ball", 48: "7 Ball", 49: "Bank Shot Lane",
	**{50 + i: f"Bonus Rack {i + 1}" for i in range(15)},
}
# The sheet's "(23) Jackpot (two)": two bulbs under one insert, the second projected onto the first.
JACKPOT_BULBS = (
	"The sheet's '(two)' gives this output two bulbs, the way Capcom's Kingpin ROM marks its two-bulb outputs '(2)'; "
	"neither the lamp table, which has no quantity column, nor the ROM's test, which prints no counts, says otherwise. The "
	"playfield has one Jackpot insert, a rectangle about twice as wide as it is tall below LIT POCKET AWARDS on the "
	"retained table's playfield image, which the lamp drawing marks with the single disc 11 and the retained table lights "
	"with one light, l11, at its centre. Both bulbs light that insert, but no source shows where they sit under it, so "
	"the first placement is l11's centre, which disc 11 checks, and the second is a documented projection onto the same point."
)
JACKPOT_PROJECTION = (
	"The second of the Jackpot's two bulbs (the lamp matrix sheet's '(23) Jackpot (two)'), placement "
	"lamp.matrix-11.emitter.2. Both bulbs sit under the one Jackpot insert, which the lamp drawing marks with a single "
	"disc 11 that checks the first placement, the centre of light l11; no source shows where the bulbs sit under the "
	"insert, so the second is projected onto the first and excluded from the callout check."
)
# Light lN of the retained table for every playfield lamp (vpmMapLights binds lamp N to lN).
LAMP_POSITIONS = {
	3: (0.270139, 0.245052), 4: (0.306193, 0.234651), 5: (0.343028, 0.224349), 6: (0.453341, 0.732579),
	7: (0.892869, 0.249811), 8: (0.246732, 0.291926), 9: (0.335721, 0.041926), 10: (0.433394, 0.04249),
	11: (0.454135, 0.337549), 12: (0.110535, 0.267247), 13: (0.533179, 0.04167), 14: (0.383201, 0.042379),
	15: (0.484492, 0.041652), 16: (0.58221, 0.041759), 17: (0.190513, 0.503521), 18: (0.201174, 0.477813),
	19: (0.17297, 0.531054), 20: (0.384387, 0.467712), 21: (0.697066, 0.65735), 22: (0.52246, 0.46746),
	23: (0.209152, 0.656859), 24: (0.453477, 0.467442), 25: (0.413567, 0.269494), 26: (0.49526, 0.269779),
	27: (0.567601, 0.060937), 28: (0.060464, 0.703839), 29: (0.307616, 0.472811), 30: (0.323035, 0.443434),
	31: (0.291693, 0.501881), 32: (0.459972, 0.061176), 33: (0.100654, 0.152969), 34: (0.745399, 0.591916),
	35: (0.774376, 0.563294), 36: (0.800136, 0.536122), 37: (0.601283, 0.473212), 38: (0.584029, 0.443354),
	39: (0.616698, 0.502086), 40: (0.722755, 0.615917), 41: (0.453581, 0.516438), 42: (0.386505, 0.370705),
	43: (0.455187, 0.370401), 44: (0.522168, 0.37035), 45: (0.353429, 0.060937), 46: (0.773148, 0.243924),
	47: (0.7373, 0.221531), 48: (0.702151, 0.198279), 49: (0.692105, 0.141449), 50: (0.453796, 0.683992),
	51: (0.411281, 0.659464), 52: (0.496943, 0.659622), 53: (0.372942, 0.636023), 54: (0.453763, 0.6363),
	55: (0.534226, 0.636351), 56: (0.329448, 0.615459), 57: (0.415205, 0.61701), 58: (0.490022, 0.617222),
	59: (0.564697, 0.615866), 60: (0.298907, 0.598793), 61: (0.372661, 0.598981), 62: (0.453274, 0.598933),
	63: (0.527149, 0.599245), 64: (0.601024, 0.599229),
}

# Legacy compatibility aliases from games/brkshot.json (numeric forms only; see solenoid 9-11 notes).
LEGACY_SWITCHES = (30, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63,
                   65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 77, 78, 79)
LEGACY_LAMPS = tuple(range(3, 65))
LEGACY_COILS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 25, 26, 28, 29, 30, 31, 32)
LEGACY_RETIRED_COIL_NAMES = {9: "c_flipper_lower_right", 10: "c_flipper_upper_right", 11: "c_flipper_lower_left"}

EXCERPT_IMAGES = {
	"switch-locations.webp": "Capcom_1996_Breakshot_Manual.pdf page 82, crop box 0.085,0.335,0.405,0.9, scanned page rendered at its native resolution (embedded image xref 243, 4880px across 12.21in), rendered at 311 dpi, capped to 860px wide, grayscale, 861x1925 WebP quality 65 (tools/render_excerpt_image.py, PyMuPDF 1.28.2, Pillow 12.3.0)",
	"solenoid-locations.webp": "Capcom_1996_Breakshot_Manual.pdf page 84, crop box 0.6,0.115,0.895,0.745, scanned page rendered at its native resolution (embedded image xref 249, 4880px across 12.21in), rendered at 333 dpi, capped to 860px wide, grayscale, 861x2298 WebP quality 70 (tools/render_excerpt_image.py, PyMuPDF 1.28.2, Pillow 12.3.0)",
	"lamp-locations.webp": "Capcom_1996_Breakshot_Manual.pdf page 74, crop box 0.31,0.125,0.71,0.925, scanned page rendered at its native resolution (embedded image xref 219, 1827px across 12.18in), rendered at 150 dpi, grayscale, 518x1313 WebP quality 80 (tools/render_excerpt_image.py, PyMuPDF 1.28.2, Pillow 12.3.0)",
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Breakshot retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Breakshot extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Breakshot retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError(f"Breakshot retained extraction manifest does not match the files under {source_root / EXTRACTION_RELATIVE_PATH}")
	identity = (len(actual["files"]), sum(int(item["size"]) for item in actual["files"]), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Breakshot retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], refs: tuple[str, ...], status: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)})
	return {"status": status, "placements": placements}


def object_phrase(item_type: str, name: str) -> str:
	if item_type == "Wall":
		return f"the centroid of the outline of wall '{name}'"
	return f"the centre of {item_type.lower()} '{name}'"


def numeric_aliases(namespace: str, address: int) -> list[dict[str, str]]:
	return [{"namespace": namespace, "value": value} for value in dict.fromkeys((str(address), f"{address:02d}", f"{address:03d}"))]


def aliases(group: str, address: int) -> list[dict[str, str]]:
	public = {"input": "pinmame.switch", "solenoid": "pinmame.solenoid", "lamp": "pinmame.lamp"}[group]
	result = [{"namespace": public, "value": str(address)}]
	legacy = {"input": ("vpe-legacy.switch", LEGACY_SWITCHES), "solenoid": ("vpe-legacy.coil", LEGACY_COILS), "lamp": ("vpe-legacy.lamp", LEGACY_LAMPS)}[group]
	if address in legacy[1]:
		result += numeric_aliases(legacy[0], address)
	return result


def excerpt(identifier: str, stem: str, locator: str, *, image: bool = False, method: str = "manual", transcribed_by: str = "curator, read from the rendered page", directory: Path = EXCERPT_DIR) -> dict[str, Any]:
	path = directory / f"{stem}.md"
	record: dict[str, Any] = {
		"id": identifier,
		"locator": locator,
		"path": path.relative_to(ROOT).as_posix(),
		"sha256": _file_sha256(path),
		"method": method,
		"transcribed_by": transcribed_by,
		"reviewed": True,
	}
	if image:
		image_path = EXCERPT_DIR / f"{stem}.webp"
		record["image"] = image_path.relative_to(ROOT).as_posix()
		record["image_sha256"] = _file_sha256(image_path)
		record["image_derivation"] = EXCERPT_IMAGES[image_path.name]
	return record


HARNESS_LOCATOR = (
	f"LibPinMAME pinmame64.dll SHA-256 {LIBRARY_SHA256} built from vpinball/pinmame {PINMAME_REVISION}; ROM archive "
	f"bsv103.zip SHA-256 {ROM_ARCHIVE_SHA256}; fresh isolated NVRAM per run; raw runs and every DMD frame retained under "
	"external:pinmame-review-artifacts/breakshot-1996/harness-runs"
)


def _runtime_runs() -> dict[str, dict[str, Any]]:
	return {run["name"]: run for run in load_json(RUNTIME_EVIDENCE_PATH)["runtime"]["raw_runs"]}


def _run_text(name: str) -> str:
	run = _runtime_runs()[name]
	return f"raw run {name} (SHA-256 {run['sha256']}) from scenario {run['scenario_path']} (SHA-256 {run['scenario_sha256']})"


def source_records(callout_sha256: str) -> list[dict[str, Any]]:
	runtime_uri = {"uri": "internal:" + RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix(), "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH)}
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"PinmameGetGames driver records bsv103 (root) and its clones bsv102, bsb105, bsv100r and bsv102r; the clone "
				"pp100 is Pool Player, curated as illinois-pinball.pool-player.2000"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/capgames.c (FLIP, capInvSw5-8, capFlip5-8, INITGAME/INITGAMEFF, the Breakshot drivers); "
				"src/wpc/capcom.c (HAS_SWITCH_BOARD, SWITCH_UPDATE(cc), cc_sw2m/cc_m2sw, the io_r switch read and its "
				"inversion, io_w with the 9/10/11 flipper mirrors, MACHINE_INIT(cc) nLamps and the bsv bulb typing, and the "
				"port A/B comments on the J3 Token/Coin Meter/Printer Interface Board lines, which no public address carries); "
				"src/wpc/capcom.h (CC_COMPORTS); src/wpc/core.h (CORE_FIRSTUFLIPSOL, CORE_FIRSTLFLIPSOL, CORE_FIRSTCUSTSOL and "
				"the flipper mirror names); src/wpc/core.c (core_updateSw's flipper column and the 5/6 button copy)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
			"excerpts": [
				excerpt("excerpt.breakshot.pinmame-source", "pinmame-source", "The quoted source lines at the pinned revision and what this record derives from them", transcribed_by="curator, quoted from the pinned source checkout"),
			],
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/capcom.json",
			"revision": "repository",
			"locator": (
				"Capcom switch (1-96), solenoid (1-51) and lamp address ranges and the cc_sw2m/cc_m2sw switch mapping. Its "
				"flipper-mirror table and bsv flasher range predate the pinned revision: at 46e1a01a capcom.c mirrors 9, 10 "
				"and 11 to 47/48, 45/46 and 33/34 and types only 28 as a bulb for bsv, which this record follows"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=3784",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-11-13T00:00:00Z",
			"locator": (
				"IPDB machine 3784 page, retained as external:pinmame-manuals/by-machine/capcom.breakshot.1996/ipdb/"
				"ipdb-machine-3784.html through an authenticated browser session (IPDB is Cloudflare-gated): identity, "
				"date, model number, MPU, production, features and the documentation list that links the manual"
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Machine Database",
			"excerpts": [
				excerpt("excerpt.breakshot.ipdb-identity", "identity", "IPDB machine 3784 factual fields, transcribed from the retained page", transcribed_by="curator, read from the retained page"),
			],
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/capcom.breakshot.1996/ipdb/Capcom_1996_Breakshot_Manual.pdf",
			"original_filename": "Capcom_1996_Breakshot_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-11-13T00:00:00Z",
			"locator": (
				"Capcom Coin-Op operator's manual PM00147, issue 05/02/96 (21,318,109 bytes), retrieved from IPDB machine 3784 "
				"(https://www.ipdb.org/files/3784/Capcom_1996_Breakshot_Manual.pdf). PDF page = printed page + 4. Printed 70-71 "
				"(PDF 74-75): lamp location drawing P62400 and the Cabinet, Backbox, & Playfield Lamps table; printed 78 (PDF "
				"82): switch table and drawing P62500; printed 80 (PDF 84): solenoid and flasher table and drawing P62600; "
				"PDF 147: the lamp matrix wiring sheet; printed 20, 25-26, 38-39, 51 and 53 (PDF 24, 29-30, 42-43, 55 and "
				"57): the redemption menu and the ticket and token dispenser adjustments and tests; PDF 145: the PB-6 "
				"printer interface wiring sheet"
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "Capcom Coin-Op, Inc.",
			"excerpts": [
				excerpt("excerpt.breakshot.switch-locations", "switch-locations", "PDF page 82, printed page 78, Playfield & Cabinet Switches & Optos, table and drawing P62500", image=True, transcribed_by="curator, read from a 400 dpi render of the page"),
				excerpt("excerpt.breakshot.solenoid-locations", "solenoid-locations", "PDF page 84, printed page 80, Playfield and Backbox: Solenoids, and Flashers, table and drawing P62600", image=True, transcribed_by="curator, read from a 400 dpi render of the page"),
				excerpt("excerpt.breakshot.lamp-table", "lamp-table", "PDF page 75, printed page 71, Cabinet, Backbox, & Playfield Lamps table (matrixed lamps 1-64, G.I. 65A-68Q, fluorescent 69), and the PDF page 147 lamp matrix sheet", transcribed_by="curator, read from a 600 dpi render of page 75 and a 220 dpi render of page 147"),
				excerpt("excerpt.breakshot.lamp-locations", "lamp-locations", "PDF page 74, printed page 70, lamp location drawing P62400", image=True, transcribed_by="curator, read on gridded 4x and 8x zooms of the crop"),
				excerpt(
					"excerpt.breakshot.redemption-and-dispensers",
					"redemption-and-dispensers",
					"PDF pages 24, 29-30, 42-43, 55 and 57 (redemption menu, dispenser adjustments B1-16/B1-17, tests C1-09/C1-10, "
					"F5) and PDF page 145 (PB-6 printer interface wiring)",
					transcribed_by="curator, read from the text layer checked against 300 dpi renders, and from a 300 dpi render of PDF page 145",
				),
			],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/capcom/breakshot-1996/source/Breakshot%20%28Capcom%201996%29%20VPW%20v1.1.vpx",
			"original_filename": "Breakshot (Capcom 1996) VPW v1.1.vpx",
			"sha256": TABLE_SHA256,
			"acquired_at": "2026-11-13T00:00:00Z",
			"locator": (
				f"VPW's Breakshot v1.1 ({TABLE_SIZE} bytes), downloaded from https://vpuniverse.com/files/file/20471-breakshot-capcom-1996/ "
				f"(archive 'Breakshot (Capcom 1996) VPW v1.1.vpx.zip', {TABLE_ARCHIVE_SIZE} bytes, SHA-256 {TABLE_ARCHIVE_SHA256}). "
				f"Playfield bounds {TABLE_BOUNDS} (gamedata.json); normalized coordinates are x/952 and y/2162. Geometry "
				"authority for named table objects only."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "VPW (Niwak, Sixtoe, Apophis, Tastywasps and the VPW testing team)",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/capcom/breakshot-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"The retained table's embedded script (169,448 bytes): cGameName \"bsv103\", UseSolenoids = 2, the SolCallback "
				"table, the switch handlers, the trough, drop-target, centre-post, gate, saucer and pocket subs, and "
				"vpmMapLights AllLamps, which binds lamp N to light lN. Runtime and mechanism-causality authority except where "
				"this record names a table defect that the ROM proves."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "VPW (Niwak, Sixtoe, Apophis, Tastywasps and the VPW testing team)",
			"excerpts": [
				excerpt("excerpt.breakshot.script-and-libraries", "script-and-libraries", "Quoted lines of script.vbs, Capcom.vbs and core.vbs that this record relies on", transcribed_by="curator, quoted from the retained files"),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/" + EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix(),
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, "
				f"extracted with vpxtool from the retained table. Bounds {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPM_LIBRARY_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/vpm-script-libs/capcom.vbs",
			"original_filename": "Capcom.vbs",
			"sha256": VPM_CAPCOM_LIBRARY_SHA256,
			"locator": (
				"The VPinMAME system script the table loads (LoadVPM \"03060000\", \"CAPCOM.VBS\", 3.61), 'Last Updated in VBS "
				"v3.61', retained from the contributor's installation with the core.vbs it runs (SHA-256 "
				f"{VPM_CORE_LIBRARY_SHA256}, same folder): the swCoin/swStartButton/swDiagnostic/swSlamTilt/swTilt/swBuyIn "
				"and swLRFlip 82/swLLFlip 84/swURFlip 81 constants, vpmKeyDown/vpmKeyUp, and core.vbs's sLRFlipper 46, "
				"sLLFlipper 48 and sURFlipper 34. Quoted in the script excerpt."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "VPinMAME / Visual Pinball script-library maintainers",
		},
		{
			"id": SERVICE_SOURCE,
			"kind": "service_diagnostic",
			**runtime_uri,
			"revision": PINMAME_REVISION,
			"locator": (
				"bsv103's own service menu: Switch Test with each public switch held alone, Solenoid Test S01-S32 fired one at a "
				f"time, and the single-lamp Lamp Test walk; {_run_text('bsv103-switch-test')}, {_run_text('bsv103-solenoid-test')} "
				f"and {_run_text('bsv103-lamp-test')}, summarized in evidence/runtime/capcom/breakshot-service-diagnostics.json; "
				f"{HARNESS_LOCATOR}"
			),
			"license": "NOASSERTION",
			"attribution": "Capcom Coin-Op bsv103 service menu, executed locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
			"excerpts": [
				excerpt(
					"excerpt.breakshot.service-tests", "service-tests",
					"The Switch, Solenoid and Lamp Test readings and the gameplay check, one row per cited DMD frame",
					method="mixed",
					transcribed_by="tools/build_breakshot_runtime_evidence.py rendering the curator's frame readings pinned in tools/seeds/capcom/breakshot-1996-service-readings.json",
				),
			],
		},
		{
			"id": GAMEPLAY_SOURCE,
			"kind": "runtime_scenario",
			**runtime_uri,
			"revision": PINMAME_REVISION,
			"locator": (
				"A short bsv103 game on fresh state (the service excerpt's Gameplay check): boot, coins, Start with a full "
				"trough, the shooter lane, the flipper host inputs 84 and 82 and public 21 and 81, both drop banks under the "
				"ROM's and the retained table's numbering, the tilt bob and the slam tilt, with the solenoids each step fired; "
				f"{_run_text('bsv103-gameplay')}; {HARNESS_LOCATOR}"
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally with LibPinMAME from the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:" + CALLOUT_PATH.relative_to(ROOT).as_posix(),
			"sha256": callout_sha256,
			"revision": "2026-11-13",
			"locator": (
				"Factory location-drawing callout check of P62500 (switches), P62600 (solenoids and flashers) and P62400 "
				"(lamps), the three committed crops: every disc transcribed by an independent reader without table data, the "
				"curator's corrections recorded with their reasons, per-page control fits on the bumper caps, flipper pivots "
				"and playfield-outline corners and per-page callout fits; a table placement whose own disc lands within 0.07 "
				"normalized under both fits is validated (tools/drawing_callouts.py). Reads and the seed generator are "
				"retained under external:pinmame-review-artifacts/breakshot-1996/callout-check with a pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": LEGACY_SOURCE,
			"kind": "legacy_json",
			"uri": "https://github.com/vpinball/pinmame-game-defs",
			"revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
			"locator": "games/brkshot.json; origin=vbscript-parser",
			"attribution": "pinmame-game-defs contributors",
		},
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"aliases": extra.pop("aliases"),
		"availability": availability,
		"provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _switch_wiring(address: int) -> dict[str, Any]:
	text = ROM_SWITCH_TEST[address][1]
	match = re.fullmatch(r"\d+\)ROW (\S+) COL (\S+)", text)
	if match:
		return {"drive_wire": match.group(2), "return_wire": match.group(1)}
	match = re.fullmatch(r"\d+\) (\S+)", text)
	if not match:
		raise RuntimeError(f"unexpected Breakshot switch wiring text for {address}: {text!r}")
	return {"drive_wire": match.group(1)}


FLIPPER_HOST = {5: (84, "left", "CORE_SWLLFLIPBUTBIT"), 6: (82, "right", "CORE_SWLRFLIPBUTBIT")}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, part, switch_type, roles = CABINET_SWITCHES[address]
		physical: dict[str, Any] = {"location": "cabinet"}
		if part:
			physical["part_number"] = part
		if switch_type:
			physical["switch_type"] = switch_type
		notes = f"Manual switch table: '{CABINET_MANUAL_TEXT[address]}', footnoted '*NOTE: Switch is located in cabinet.'"
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {}
		if address in ROM_SWITCH_TEST:
			name, wire = ROM_SWITCH_TEST[address]
			notes += f" The ROM's Switch Test shows '{name} / {wire}' while it is held."
			extra["wiring"] = _switch_wiring(address)
			refs += (SERVICE_SOURCE,)
		if address <= 4:
			notes += " The '**' part cell is footnoted '**NOTE: Not serviced separately.': the switch belongs to the coin mechanism. Capcom.vbs pulses it from the coin keys (vpmTimer.PulseSw swCoinN)."
			refs += (VPM_LIBRARY_SOURCE,)
		if address in FLIPPER_HOST:
			host, side, bit = FLIPPER_HOST[address]
			notes += (
				f" FLIP_SWNO(5,6) makes this the ROM's {side} flipper button, but under PinMAME a host presses it through public "
				f"{host}: with keyboard handling off, core_updateSw copies the flipper column's {bit} into this switch every "
				f"frame, so a direct write here lasts at most one frame. In the harness, {host} fired the {side} flipper "
				f"({'9, 47 and 48' if address == 5 else '10, 45 and 46'}). The switch drawing prints {address} at the "
				f"{'left' if address == 5 else 'right'} cabinet button."
			)
			refs += (GAMEPLAY_SOURCE,)
		if address == 7:
			notes += " Capcom.vbs writes swStartButton = 07 from the start key; in the harness Start with a credit and a full trough fired solenoids 2, 7 and 13."
			refs += (GAMEPLAY_SOURCE, VPM_LIBRARY_SOURCE)
		if address == 8:
			notes += " Capcom.vbs toggles swDiagnostic = 08 from the self-test key; the service-menu runs entered the tests with it."
			refs += (VPM_LIBRARY_SOURCE,)
		physical["notes"] = notes
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address, "used", refs,
				aliases=aliases("input", address), normally_closed=False, pulse=address in PULSED_SWITCHES, roles=roles,
				physical=physical, spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE), **extra,
			)
		)

	for address in range(9, 17):
		notes = (
			"Internal switch column 0. Breakshot has no switch board (hw.lampCol is 1), so SWITCH_UPDATE(cc) never writes "
			"this column and the ROM never reads it: the address is dead under PinMAME, and the harness's Switch Test frame "
			"did not change while it was held."
		)
		if address == 9:
			notes += (
				" The manual's switch table prints '*9 COIN DOOR-SLAM SW00121' here, but the slam switch the ROM reads is "
				"public 29: the ROM's Switch Test names 29 SLAM TILT and holding 29 in a game ended it (Credits 0). See "
				"switch.matrix-29."
			)
		else:
			notes += " The manual's switch table prints 10-20 as NOT USED."
		items.append(
			_device(
				f"switch.unread-column-0-{address}", f"Unread Cabinet Column 0 Position {address}", "virtual", "pinmame.input.switch", address, "unused",
				(CORE_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE), aliases=aliases("input", address), physical={"notes": notes},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)

	for address in range(17, 81):
		identifier = f"switch.matrix-{address}"
		if address in UNUSED_MATRIX:
			if address in ROM_SWITCH_TEST:
				name, wire = ROM_SWITCH_TEST[address]
				rom = f"the ROM's Switch Test shows '{name} / {wire}' while it is held"
			elif address in SWITCH_TEST_GRID_ONLY:
				rom = "the ROM's Switch Test names nothing while it is held (only its switch grid changes)"
			else:
				rom = "the ROM's Switch Test frame does not change while it is held"
			if address <= 31:
				manual = "the manual's switch table prints it within a NOT USED range" if address != 31 else "the manual's switch table prints 31 NOT USED"
			else:
				manual = f"the manual's switch table prints {address} NOT USED" if address not in (39, 40) else "the manual's switch table prints 39-40 NOT USED"
			notes = f"No switch is fitted: {manual}, and {rom}."
			if address == 31:
				notes += " Capcom's keyboard map puts Buy In here; Breakshot fits no buy-in button."
			if address == 32:
				notes += " Capcom's keyboard map puts its 'Unused #1' cabinet bit here."
			if address in (32, 40, 64, 72):
				notes += (
					" The ROM's test prints the same text for 32, 40, 64 and 72. The name is the notch switch of the optional "
					"ticket dispenser a redemption setup adds (the manual's adjustment B1-16 on PDF 29 and test C1-09 on PDF "
					"42), which the ROM "
					"numbers 16, a switch PinMAME never reads on Breakshot. The standard machine fits no dispenser and its "
					"switch table lists none, so nothing closes this position; which public address a fitted dispenser's "
					"notch would reach under PinMAME is not established."
				)
			if address == 48:
				notes += " The retained table reports its right bank's first drop here (see switch 49); in the harness 48 alone, or with 49 and 50, changed nothing."
			refs: tuple[str, ...] = (MANUAL_SOURCE, SERVICE_SOURCE, CORE_SOURCE)
			if address == 48:
				refs += (GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)
			items.append(
				_device(
					identifier, f"Unused Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", refs,
					aliases=aliases("input", address), physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		label, part, switch_type, roles = MATRIX_SWITCHES[address]
		physical = {"part_number": part}
		if switch_type:
			physical["switch_type"] = switch_type
		notes = f"Manual switch table: '{MANUAL_SWITCH_TEXT[address]}'."
		refs = (MANUAL_SOURCE, SERVICE_SOURCE, CORE_SOURCE)
		extra = {}
		if address in ROM_SWITCH_TEST:
			name, wire = ROM_SWITCH_TEST[address]
			notes += f" The ROM's Switch Test shows '{name} / {wire}' while it is held."
			extra["wiring"] = _switch_wiring(address)
		if address in OPTO_SWITCHES:
			notes += (
				f" Opto: the table prints receiver {part} and transmitter {OPTO_TRANSMITTERS[address]} with the switch cell "
				"filled, the drawing marks it with an open circle and the ROM's switch grid shows its opto icon. The receiver "
				"conducts while the beam is clear; capInvSw marks this address, so PinMAME publishes 1 while the beam is "
				"blocked, which is the state to write when a ball is present."
			)
		if address == 21:
			physical["location"] = "cabinet"
			notes += (
				" The second switch at the right cabinet button: the switch drawing prints 21 beside 6 there. The ROM's Switch "
				"Test names nothing while 21 is held (only its grid changes), but in a game holding 21 fired the upper right "
				"flipper, solenoid 11 with its mirrors 33 and 34. A host presses it here directly. Capcom.vbs writes swURFlip "
				"= 81 for a staged right flipper key instead; 81 is the flipper column's lower right end-of-stroke bit, which "
				"core_updateSw overwrites every frame, and holding 81 fired nothing in the harness."
			)
			refs = (MANUAL_SOURCE, GAMEPLAY_SOURCE, SERVICE_SOURCE, VPM_LIBRARY_SOURCE, CORE_SOURCE)
		if address == 29:
			physical["location"] = "cabinet (coin door)"
			notes += (
				" The manual's table prints '22-29 NOT USED' and lists the coin-door slam switch, SW00121, as '*9 COIN "
				"DOOR-SLAM', a number the ROM never reads (see switch 9). The ROM reads the slam switch here: its Switch Test "
				"names 29 SLAM TILT, and holding 29 in a game ended it (Credits 0). Capcom's keyboard map also writes Slam "
				"Tilt to 29 on this board. The part and location are the manual's '*9' row."
			)
			refs = (MANUAL_SOURCE, SERVICE_SOURCE, GAMEPLAY_SOURCE, CORE_SOURCE)
		if address == 30:
			physical["location"] = "cabinet"
			notes += " In the harness the third touch of 30 tilted the game. The retained table sets vpmNudge.TiltSwitch = 30."
			refs += (GAMEPLAY_SOURCE, VPX_SCRIPT_SOURCE)
		if address in (33, 34, 71):
			notes += " No sub of the retained table writes it; its placement is the flipper whose stroke it senses."
		if address in SWITCH_SCRIPT_NOTES:
			notes += " " + SWITCH_SCRIPT_NOTES[address]
		if address in (49, 50, 51):
			refs += (GAMEPLAY_SOURCE,)
		if address in PULSED_SWITCHES:
			notes += " The retained table reports it with vpmTimer.PulseSw (momentary)."
		if address not in (21, 29, 30):
			refs += (VPX_SCRIPT_SOURCE,)
			if address in TROUGH_SWITCHES:
				obj = SWITCH_OBJECTS[address]
				notes += f" Placement: {object_phrase(obj[0], obj[1])} of the retained table. {TROUGH_PROJECTION}"
				extra["spatial"] = located(identifier, "sensor", [obj[2]], (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE), "validated")
			else:
				obj = SWITCH_OBJECTS[address]
				notes += f" Placement: {object_phrase(obj[0], obj[1])} of the retained table."
				placement_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in UNSCRIPTED_SWITCHES else (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
				extra["spatial"] = located(identifier, "sensor", [obj[2]], placement_refs, "observed")
		else:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		device_extra: dict[str, Any] = {"aliases": aliases("input", address), "normally_closed": address in OPTO_SWITCHES, "pulse": address in PULSED_SWITCHES}
		if roles:
			device_extra["roles"] = roles
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, physical=physical, **device_extra, **extra))

	flipper_column = {
		81: ("Lower Right Flipper EOS Bit", "CORE_SWLREOSBIT: rewritten every frame by core_updateSw's end-of-stroke model (FLIP_SOL declares the lower right flipper). Capcom.vbs writes swURFlip = 81 for a staged right flipper key, so that key never reaches the ROM; holding 81 fired nothing in the harness."),
		83: ("Lower Left Flipper EOS Bit", "CORE_SWLLEOSBIT: rewritten every frame by core_updateSw's end-of-stroke model. Capcom.vbs's swULFlip = 83 lands here."),
		85: ("Upper Right Flipper EOS Bit", "CORE_SWUREOSBIT: rewritten every frame by core_updateSw's end-of-stroke model (FLIP_UR is declared)."),
		86: ("Upper Right Flipper Button Bit", "CORE_SWURFLIPBUTBIT: outside locals.flipMask because no Breakshot driver declares FLIP_SW(FLIP_U), so core_updateSw leaves a write here unchanged and nothing acts on it. The real upper right flipper button is public 21."),
		87: ("Upper Left Flipper EOS Bit", "CORE_SWULEOSBIT: Breakshot declares no upper left flipper; nothing writes or reads it."),
		88: ("Upper Left Flipper Button Bit", "CORE_SWULFLIPBUTBIT: Breakshot declares no upper left flipper; nothing writes or reads it."),
	}
	for address in range(81, 89):
		if address in (82, 84):
			rom_address = 6 if address == 82 else 5
			side = "right" if address == 82 else "left"
			items.append(
				_device(
					f"switch.flipper-column-{address}", f"{side.capitalize()} Flipper Button Host Input", "virtual", "pinmame.input.switch", address, "used",
					(CORE_SOURCE, GAMEPLAY_SOURCE, VPM_LIBRARY_SOURCE), aliases=aliases("input", address),
					physical={"notes": (
						f"The flipper column's {side} button bit ({'CORE_SWLRFLIPBUTBIT' if address == 82 else 'CORE_SWLLFLIPBUTBIT'}), public {address} "
						f"by cc_m2sw. With keyboard handling off, core_updateSw copies it into matrix switch {rom_address} every frame "
						f"(FLIP_SWNO(5,6)), so a host presses the physical {side} flipper button (switch.cabinet-{rom_address}) here. "
						f"Capcom.vbs writes sw{'LR' if address == 82 else 'LL'}Flip = {address} from the flipper key; in the harness holding "
						f"{address} fired solenoid {'10 with 45 and 46' if address == 82 else '9 with 47 and 48'}. No ROM reads the column itself."
					)},
					spatial=not_applicable("virtual", CORE_SOURCE),
				)
			)
			continue
		label, note = flipper_column[address]
		items.append(
			_device(
				f"switch.flipper-column-{address}", label, "virtual", "pinmame.input.switch", address, "unused",
				(CORE_SOURCE, GAMEPLAY_SOURCE, VPM_LIBRARY_SOURCE) if address in (81, 83) else (CORE_SOURCE,),
				aliases=aliases("input", address),
				physical={"notes": f"PinMAME's flipper column (internal column 11, public {address}). {note} No Capcom circuit is behind it and no ROM reads the column."},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	for address in range(89, 97):
		items.append(
			_device(
				f"switch.unused-column-10-{address}", f"Unused Platform Switch Column 10 Position {address}", "virtual", "pinmame.input.switch", address, "unused",
				(CORE_SOURCE,), aliases=aliases("input", address),
				physical={"notes": "Internal column 10 exists only because CORE_STDSWCOLS reserves 12 columns; no Capcom driver reads or writes it."},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def solenoid_id(address: int) -> str:
	if address in SOLENOIDS:
		return f"device.{slug(SOLENOIDS[address][0])}"
	if address in VIRTUAL_SOLENOIDS:
		return f"device.{slug(VIRTUAL_SOLENOIDS[address][0])}"
	return f"device.unused-driver-output-{address}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 33):
		identifier = solenoid_id(address)
		if address in UNUSED_SOLENOIDS:
			notes = "Manual solenoid table: 'NOT USED', part '----------'. The ROM's Solenoid Test names it 'UNUSED' and pulses it only as one step of that test."
			if address == 27:
				notes += (
					" The test prints the driver's wire, 'GRY-ORG J26/27.3', but no power line. MACHINE_INIT(cc) keeps a commented-out "
					"plunger-flasher typing for 27 that its comment says 'appears in doc but was not kept in production'."
				)
				refs: tuple[str, ...] = (MANUAL_SOURCE, SERVICE_SOURCE, CORE_SOURCE)
			else:
				refs = (MANUAL_SOURCE, SERVICE_SOURCE)
			notes += " Nothing in a game drives it."
			items.append(
				_device(
					identifier, f"Unused Driver Output {address}", "coil", "pinmame.output.solenoid", address, "unused", refs,
					aliases=aliases("solenoid", address), physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		label, kind, part, rom_name, wire, connection, power_wire, volts = SOLENOIDS[address]
		physical: dict[str, Any] = {"part_number": part}
		notes = (
			f"Manual solenoid table: '{MANUAL_SOLENOID_TEXT[address]}', part {part}. The ROM's Solenoid Test shows "
			f"'S{address:02d} - {rom_name} / {wire} {connection} / {power_wire} PWR {volts}V' and fired "
			f"{'it with its mirrors ' + {9: '47 and 48', 10: '45 and 46', 11: '33 and 34'}[address] if address in (9, 10, 11) else 'it'}."
		)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		elif address in (4, 5):
			notes += " The retained script binds no callback; its slingshot walls kick on their own."
		elif address in (29, 30, 31):
			notes += " The retained script binds no callback; its bumpers kick on their own."
		if address in (9, 10, 11):
			notes += (
				f" The legacy definition named this address '{LEGACY_RETIRED_COIL_NAMES[address]}', which the ROM's test contradicts, "
				"so only its numeric legacy aliases are kept."
			)
		if address == 28:
			physical["quantity"] = 2
			notes += " MACHINE_INIT(cc) types it as a #89 bulb output (CORE_MODOUT_BULB_89_20V_DC_WPC) for the bsv drivers."
		if address == 3:
			physical["location"] = "backbox"
			notes += " The solenoid drawing prints disc 3 in the backbox box's upper right corner."
		if address in (12, 14):
			notes += " The retained table holds its centre post up as walls CenterPostWall001-003 and moves its post primitive to (431, 894) when it is up."
		if address == 2:
			notes += (
				" In the harness Start with a credit and a full trough fired 2 together with the two bank resets, pulsing it five times "
				"while trough position 1 (36) stayed closed; it released 2 when the served ball left position 1 and did not fire it again."
			)
		if address in (7, 13):
			notes += (
				" In the harness Start with a credit fired 7 and 13 together with the trough eject, resetting both banks for the new "
				"ball. With a bank's three drops held down for 4 s the ROM fired neither reset, and the run served no further ball, "
				"so when the ROM resets a completed bank during play was not observed."
			)
		refs = (MANUAL_SOURCE, SERVICE_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs += (VPX_SCRIPT_SOURCE,)
		if address in (2, 7, 13, 9, 10, 11):
			refs += (GAMEPLAY_SOURCE,)
		extra: dict[str, Any] = {
			"aliases": aliases("solenoid", address),
			"wiring": {"control_wire": wire, "control_connection": connection, "power_wire": power_wire, "nominal_voltage_v": volts, "voltage_type": "dc"},
		}
		if address in SOLENOID_ROLES:
			extra["roles"] = SOLENOID_ROLES[address]
		if address == 3:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			objects = SOLENOID_OBJECTS[address]
			role = "emitter" if kind == "flasher" else "effect"
			phrase = "; ".join(object_phrase(t, n) for t, n, _ in objects)
			if address in TROUGH_SOLENOIDS:
				notes += f" Placement: {phrase}. {SOLENOID_PLACEMENT_NOTES[address]}"
				extra["spatial"] = located(identifier, role, [p for _, _, p in objects], (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE), "validated")
			else:
				notes += f" Placement: {phrase}. {SOLENOID_PLACEMENT_NOTES[address]}"
				placement_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_CALLBACKS else (VPX_TABLE_SOURCE, MANUAL_SOURCE)
				extra["spatial"] = located(identifier, role, [p for _, _, p in objects], placement_refs, "observed")
		physical["notes"] = notes
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, physical=physical, **extra))

	for address in range(33, 52):
		label, availability, roles, note = VIRTUAL_SOLENOIDS[address]
		refs = (CORE_SOURCE,)
		if address in (33, 34, 45, 46, 47, 48):
			refs = (CORE_SOURCE, SERVICE_SOURCE, GAMEPLAY_SOURCE)
		if address in (34, 46, 48, 51):
			refs += (VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE)
		items.append(
			_device(
				solenoid_id(address), label, "virtual", "pinmame.output.solenoid", address, availability, refs,
				aliases=aliases("solenoid", address), roles=roles, physical={"notes": note}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, row = (address - 1) // 8 + 1, (address - 1) % 8 + 1
		identifier = f"lamp.matrix-{address}"
		rom_text = f"{column}{row}B - {ROM_LAMP_TEST[address]}"
		if address == 2:
			items.append(
				_device(
					identifier, "Unused Matrix Position 2", "lamp", "pinmame.output.lamp", address, "unused", (MANUAL_SOURCE, SERVICE_SOURCE),
					aliases=aliases("lamp", address),
					physical={"notes": (
						"Manual lamp table: '12B NOT USED' with '-----' in every other cell. The ROM's Lamp Test calls it '12B - OPTIONAL "
						"BUY IN', the lamp of a buy-in button Breakshot does not fit (switch 31, its button position, is NOT USED as well). "
						"The manual's lamp matrix sheet prints 'Not Used', with no reference, in Row 2 of Column 1."
					)},
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		label, manual_text, bulb, part = LAMPS[address]
		col_pin, col_wire = LAMP_COLUMNS[column]
		row_pin, row_wire = LAMP_ROWS[row]
		physical = {"part_number": part}
		notes = (
			f"Manual lamp table: '{manual_text}', bulb #{bulb}, {part}. The ROM's Lamp Test lights it as '{rom_text} / COL-SM{column}B "
			f"{col_pin} {col_wire} / ROW-M{row}B {row_pin} {row_wire}'. The manual's lamp matrix sheet prints cell '({column}{row}) "
			f"{SHEET_NAMES[address]}' on the same colours but on Column {column} {SHEET_COLUMNS[column]} and Row {row} "
			f"{SHEET_ROWS[row]}; that connector-only disagreement leaves the address, the lamp and its wire colours settled, and "
			"the wiring above follows the ROM's own test."
		)
		if address == 23:
			notes += (
				" The manual's table prints '37B 9 BALL OPTION', the same text as lamp 41 (61B); the ROM's Lamp Test and the "
				"lamp matrix sheet name 37 '8 Ball Option', which this label follows."
			)
		if address == 11:
			physical["quantity"] = 2
			notes += f" {JACKPOT_BULBS}"
		if address in (25, 26):
			notes += " A matrix lamp, not a G.I. string: the ROM switches it like any insert."
		refs = (MANUAL_SOURCE, SERVICE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": aliases("lamp", address),
			"wiring": {"drive_wire": col_wire, "drive_connection": col_pin, "return_wire": row_wire, "return_connection": row_pin},
		}
		if address == 1:
			physical["location"] = "cabinet"
			notes += " The start button's lamp; the lamp drawing prints 1 at the cabinet front, outside the playfield."
			extra["roles"] = ["cabinet.start-lamp"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			refs += (VPX_SCRIPT_SOURCE,)
			notes += f" Placement: the centre of light 'l{address}' of the retained table, which vpmMapLights binds to lamp {address}."
			if address == 27:
				notes += " The lamp drawing prints no number for it; its right top-lane insert is the drawing's only unlabelled lamp insert, read as 27 in the callout check."
			if address == 11:
				# Two bulbs under one insert: the first is the table's light, checked by disc 11; the second is projected onto it.
				spatial = located(identifier, "emitter", [LAMP_POSITIONS[address]] * 2, (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE), "observed")
				spatial["placements"][1]["provenance"] = provenance(VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
				extra["spatial"] = spatial
			else:
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE), "observed")
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", refs, physical=physical, **extra))
	for address, label, role, board in ((65, "CPU Board Diagnostic LED", "service.cpu-diagnostic", "CPU board"), (66, "Sound Board Diagnostic LED", "service.sound-diagnostic", "sound board")):
		items.append(
			_device(
				f"lamp.diag-{address}", label, "lamp", "pinmame.output.lamp", address, "used", (CORE_SOURCE,), aliases=aliases("lamp", address),
				roles=[role],
				physical={"location": "backbox", "notes": f"MACHINE_INIT(cc) types this the {board}'s diagnostic LED (CORE_MODOUT_LED): nLamps is 64 + 8 for Breakshot's single lamp matrix, so the LED column follows lamp 64."},
				spatial=not_applicable("cabinet_or_service", CORE_SOURCE),
			)
		)
	for address in range(67, 73):
		items.append(
			_device(
				f"lamp.unused-{address}", f"Unused Diagnostic Column Position {address}", "virtual", "pinmame.output.lamp", address, "unused", (CORE_SOURCE,),
				aliases=aliases("lamp", address), physical={"notes": "MACHINE_INIT(cc) types the rest of the LED column CORE_MODOUT_NONE."},
				spatial=not_applicable("virtual", CORE_SOURCE),
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
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, IPDB_SOURCE),
			"provenance": provenance(CORE_SOURCE, IPDB_SOURCE, SERVICE_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[int], sensors: list[str], behavior: str, *refs: str) -> dict[str, Any]:
		return {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": [solenoid_id(address) for address in actuators],
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}

	def switches(*addresses: int) -> list[str]:
		return [f"switch.matrix-{address}" for address in addresses]

	return [
		mechanism(
			"mechanism.outhole-and-trough", "Outhole and Ball Trough", "kicker", [1, 2], switches(35, 36, 37, 38),
			(
				"A drained ball rolls into the outhole under the apron's centre (switch 35, SW00113). The outhole coil (S1) "
				"kicks it into a three-ball trough that runs up towards the shooter lane under the apron, sensed by the three "
				"trough optos 38, 37 and 36, position 1 (36) at the shooter end. The trough coil (S2) serves the ball at "
				"position 1 into the shooter lane (switch 43), where the player plunges it. The retained script creates the "
				"three balls in sw38, sw37 and sw36 with all three optos set, kicks sw35 on S1 and sw36 on S2, and rolls the "
				"remaining balls forward (sw37 to sw36, sw38 to sw37) when a position empties. In the harness, Start with a "
				"credit and a full trough fired S2 together with both drop-bank resets, pulsing S2 five times while position 1 "
				"(36) stayed closed, and released S2 when the ball left position 1."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mechanism.left-outlane-kickback", "Left Outlane Kickback", "kicker", [6], switches(46),
			(
				"A kicker in the left outlane (S6 KICKER) returns a ball rolling down the outlane past switch 46 to the "
				"playfield; the ROM fires it when the kickback is lit (lamp 28 KICKER, at the left outlane). The retained "
				"script holds its plunger PlungerKB pulled back and fires it while S6 is energized."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE,
		),
		mechanism(
			"mechanism.right-drop-bank", "Right Drop Target Bank", "drop_target_bank", [7], switches(49, 50, 51, 52),
			(
				"Three drop targets in a diagonal row on the upper right (switches 49 left, 50 centre, 51 right, SW00106) with "
				"a standup target behind them (52, SW00141) that a ball reaches once the drops are down. One reset coil (S7) "
				"raises all three. In the harness, dropping 49, 50 and 51 took the score from 0 to 9,000; the ROM fired S7 "
				"with the trough eject when Start began the game, but not while the dropped bank stayed down for 4 s, and the "
				"run served no further ball. The retained script numbers the bank 48-50 with the standup 51 (a "
				"table defect: the ROM never reacts to 48), and its ResetDropsRight raises its three drops on S7."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mechanism.left-drop-bank", "Left Drop Target Bank", "drop_target_bank", [13], switches(73, 74, 75, 76),
			(
				"Three drop targets in a diagonal row on the left side (switches 73 lowest, 74, 75 highest, SW00106) with a "
				"standup target behind them (76, SW00141). One reset coil (S13) raises all three (the script's "
				"ResetDropsLeft: DTRaise 73, 74, 75). In the harness, dropping 73 and 74 each played the ROM's drop-target "
				"animation and, with 75 down too, the display returned to the score; the ROM fired S13 with the trough eject "
				"when Start began the game, but not while the dropped bank stayed down for 4 s, and the run served no further "
				"ball."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, GAMEPLAY_SOURCE,
		),
		mechanism(
			"mechanism.bonus-saucer", "Bonus Saucer", "kicker", [8], switches(67),
			(
				"A saucer on the right side below the upper right flipper holds the ball on switch 67 (SW00118) until S8 "
				"(BONUS SAUCER) kicks it out. The retained script kicks only a ball that is sitting in sw67 and clears 67 when "
				"the ball leaves."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE,
		),
		mechanism(
			"mechanism.center-post", "Center Post", "other", [12, 14], switches(66),
			(
				"A post at the foot of the centre pocket assembly, between the Lite Super Cue targets 77 and 78, raised by S12 "
				"(CENTER POST UP) and released by S14 (CENTER POST DOWN); switch 66 (SW00118) closes while it is up. The "
				"retained script raises its walls CenterPostWall001-003 on S12 and sets 66 at the end of the rise, and on S14 "
				"drops them and clears 66 at the end of the fall (its comment: S14 also pulses while the post fires up). IPDB "
				"describes a large metal plug in front of the centre feature that rises after a captured ball and that the "
				"player hits."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, IPDB_SOURCE,
		),
		mechanism(
			"mechanism.center-pockets", "Center Pockets", "kicker", [25, 26, 32], switches(68, 69, 70, 65),
			(
				"Three pockets side by side behind the centre post, each with its own switch (68 left, 69 centre, 70 right, "
				"SW00139) and its own eject coil (S25, S26, S32), with the centre pocket opto 65 at the assembly's foot and the "
				"Center Pocket Flash (S28, two bulbs) above them. The retained script kicks a pocket's ball only while that "
				"pocket's switch is set. IPDB describes three scoops at the top of the centre feature that hold balls for "
				"multiball."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, IPDB_SOURCE,
		),
		mechanism(
			"mechanism.top-gates", "Top Gates", "gate", [15, 16], [],
			(
				"Two gates at the top of the playfield, one at each end of the top-lane arch (S15 right, S16 left, CL00112 on "
				"the 20 V line). Each stands open while its coil is energized: the retained script sets RightGate.Open or "
				"LeftGate.Open while the coil is on and lets the gate's own timer close it after release, filtering PWM the "
				"ROM does not hold steady."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE,
		),
		mechanism(
			"mechanism.captive-ball", "Captive Ball", "other", [], switches(79, 55),
			(
				"A captive ball lane on the upper left: a ball shot into the lane strikes a stationary Newton ball, which "
				"passes the hit to a captive ball above it; the captive ball rolls up over the captive rollover (79) to the "
				"captive standup (55) at the top. IPDB lists one captive ball and one Newton ball. The retained script creates "
				"the Newton ball in NBKicker and the captive ball in CBKicker and moves the captive ball when a playfield ball "
				"hits the Newton ball from below. No coil acts on it; lamps 3-5 and 8 (Captive Ball 1-3, EB) line the lane."
			),
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SERVICE_SOURCE, IPDB_SOURCE,
		),
	]


def drivers(driver_ids: tuple[str, ...] = DRIVER_IDS, compatibility: dict[str, tuple[str, str]] = DRIVER_COMPATIBILITY) -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
	for driver_id in driver_ids:
		record = by_id[driver_id]
		item = {key: record[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if record.get("clone_of"):
			item["clone_of"] = record["clone_of"]
		item["physical_compatibility"], item["variant_notes"] = compatibility[driver_id]
		items.append(item)
	return items


def _web_source(identifier: str, filename: str, sha256: str, uri: str, locator: str, attribution: str, *excerpts: dict[str, Any]) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier,
		"kind": "human_review",
		"uri": uri,
		"original_filename": filename,
		"sha256": sha256,
		"acquired_at": "2026-11-13T00:00:00Z",
		"locator": f"Retained as {POOL_PLAYER_WEB_URI}/{filename}. {locator}",
		"license": "NOASSERTION",
		"rights": "NOASSERTION",
		"attribution": attribution,
	}
	if excerpts:
		record["excerpts"] = list(excerpts)
	return record


def pool_player_sources() -> list[dict[str, Any]]:
	identity = excerpt(
		"excerpt.pool-player.identity",
		"identity",
		"IPDB machine 4495 and Pinside's pool-player fields, and Pinball News's report of the flyer",
		transcribed_by="curator, read from the retained pages",
		directory=POOL_PLAYER_EXCERPT_DIR,
	)
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames driver record pp100, Pool Player (1.0), Illinois Pinball 2000, clone of bsv103",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "src/wpc/capgames.c: FLIP, capInvSw5 and capInvSw13, capFlip5 and capFlip13, and the pp100 driver block",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
			"excerpts": [
				excerpt(
					"excerpt.pool-player.pinmame-source",
					"pinmame-source",
					"The quoted capgames.c lines at the pinned revision and what this record derives from them",
					transcribed_by="curator, quoted from the pinned source checkout",
					directory=POOL_PLAYER_EXCERPT_DIR,
				),
			],
		},
		_web_source(
			POOL_PLAYER_IPDB_SOURCE,
			"ipdb-machine-4495-20250711.html",
			"426bb0c7eb99b4c419c2fca8dea02cbdf8b705671ba959bf9f9268bd3b7dc143",
			"https://www.ipdb.org/machine.cgi?id=4495",
			"Internet Archive capture of 2025-07-11 of IPDB machine 4495 (IPDB is Cloudflare-gated): manufacturer, date, "
			"type, theme, notes on the Breakshot playfield and on sales, ROM version.",
			"Internet Pinball Machine Database; capture hosted by the Internet Archive",
			identity,
		),
		_web_source(
			POOL_PLAYER_PINSIDE_SOURCE,
			"pinside-pool-player-20240413.html",
			"c887392c14cd44cba05645e48d9a4070a629c0f6cf00a22cd5c4e6c76a918f6f",
			"https://pinside.com/pinball/machine/pool-player",
			"Internet Archive capture of 2024-04-13 of Pinside's machine page: manufacturer, release type, generation, "
			"display, player, flipper and multiball counts, IPDB link. A secondary database, used as a lead.",
			"Pinside; capture hosted by the Internet Archive",
		),
		_web_source(
			POOL_PLAYER_NEWS_SOURCE,
			"pinballnews-williams.html",
			"c765adb3f90fc8ba891d93a148cc35eba8b80d19097d58b03c2e8e69ee892ec6",
			"https://www.pinballnews.com/news/williams.html",
			"Pinball News story of 3 October 2000 (updated 16 October 2000) reporting Illinois Pinball's Pool Player flyer, "
			"with the flyer scan pinballnews-illinois.jpg (SHA-256 c9993b8f9f8f5ccbb09677f652d8186fc2e8fef97fa19f523d7ab795768570e5). "
			"A contemporary report, used as a lead.",
			"Pinball News; flyer scan courtesy of Duncan Brown",
		),
	]


def build_pool_player() -> dict[str, Any]:
	"""Pool Player: identity, its one driver and what its sources say, nothing more yet."""
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": POOL_PLAYER_ID,
			"name": "Pool Player",
			"manufacturer": "Illinois Pinball",
			"year": 2000,
			"kind": "physical_conversion",
			"ipdb_id": 4495,
		},
		"coverage": {
			"status": "partial",
			"missing": [
				"identity",
				"input_enumeration",
				"input_semantics",
				"output_enumeration",
				"output_semantics",
				"display_inventory",
				"mechanism_inventory",
				"mechanism_behavior",
				"polarity",
				"variant_differences",
				"recreation_notes",
				"provenance",
				"spatial_placement",
			],
			"dimensions": {
				"catalog_identity": "candidate",
				"address_enumeration": "unknown",
				"semantic_naming": "unknown",
				"physical_wiring": "unknown",
				"mechanisms": "unknown",
				"variant_coverage": "unknown",
				"recreation_knowledge": "candidate",
				"spatial_placement": "unknown",
			},
		},
		"controller": {"platform": "pinmame.capcom", "hardware_generation": "0x0", "inversion_applied_by_emulator": True},
		"drivers": drivers(tuple(POOL_PLAYER_DRIVER_COMPATIBILITY), POOL_PLAYER_DRIVER_COMPATIBILITY),
		"inputs": [],
		"outputs": [],
		"displays": [],
		"mechanisms": [],
		"relationships": [],
		"sources": pool_player_sources(),
		"knowledge": {"path": POOL_PLAYER_KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "partial"},
		"conflicts": [],
	}


def callout_seed() -> dict[str, Any]:
	seed = load_json(CALLOUT_PATH)
	if CALLOUT_PATH.read_bytes() != canonical_bytes(seed):
		raise RuntimeError(f"{CALLOUT_PATH} is not in canonical byte format")
	return seed


def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Breakshot",
			"manufacturer": "Capcom",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 3784,
			"opdb_id": "G43oE-M0ok5",
			"playfield": {"width": 952.0, "height": 2162.0, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {},
		"controller": {"platform": "pinmame.capcom", "hardware_generation": "0x0", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(_file_sha256(CALLOUT_PATH)),
		"knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Breakshot device identifiers are not unique: {duplicates}")
	drawing_callouts.apply_to_definition(definition, callout_seed(), CALLOUT_SOURCE)
	weak = sorted(
		placement["id"]
		for collection in ("inputs", "outputs")
		for device in definition[collection]
		for placement in (device.get("spatial") or {}).get("placements") or []
		if placement["provenance"]["status"] != "validated"
	)
	if weak:
		raise RuntimeError(f"Breakshot placements the callout check does not validate: {weak}")
	definition["coverage"] = coverage([entry["socket"] for entry in gi_sockets(definition)[0] if entry["status"] != "validated"])
	return definition


def coverage(unplaced_gi: list[str]) -> dict[str, Any]:
	"""The record's coverage: partial while any fixed G.I. socket has only the drawing's position.

	The sockets have no controller address, so no device placement check sees them; this ties the
	record's status to them instead. Once every socket has a checked position the build stops: promote
	the record deliberately (its path, an audit-format spatial report and its tests), not by regenerating.
	"""
	if not unplaced_gi:
		raise RuntimeError("every fixed G.I. socket has a checked position; promote Breakshot deliberately instead of regenerating it as partial")
	return {
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
			"spatial_placement": "observed",
		},
	}


def callout_check(definition: dict[str, Any]) -> dict[str, Any]:
	seed = callout_seed()
	decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))
	return drawing_callouts.summary(seed, decisions, CALLOUT_PATH.relative_to(ROOT).as_posix(), _file_sha256(CALLOUT_PATH))


def projections() -> list[dict[str, Any]]:
	result = [{"group": "pinmame.input.switch", "address": address, "reason": TROUGH_PROJECTION} for address in sorted(TROUGH_SWITCHES)]
	result += [{"group": "pinmame.output.solenoid", "address": address, "reason": SOLENOID_PLACEMENT_NOTES[address]} for address in sorted(TROUGH_SOLENOIDS)]
	result.append({"group": "pinmame.output.lamp", "address": 11, "reason": JACKPOT_PROJECTION})
	return result


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	na_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
	placements = [p for c in ("inputs", "outputs") for d in definition[c] for p in (d["spatial"].get("placements") or [])]
	if definition["coverage"]["status"] != "partial":
		raise RuntimeError("the Breakshot spatial report is a blocker report; a promoted record needs an audit")
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "partial",
		"blockers": [GI_BLOCKER],
		"promotion_decision": PROMOTION_DECISION,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2162.0},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/" + EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix(),
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
			"table_archive_sha256": TABLE_ARCHIVE_SHA256,
			"vpm_capcom_library_sha256": VPM_CAPCOM_LIBRARY_SHA256,
			"vpm_core_library_sha256": VPM_CORE_LIBRARY_SHA256,
		},
		"placement_count": len(placements),
		"validated_placements": sum(p["provenance"]["status"] == "validated" for p in placements),
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=lambda item: (item["group"], item["address"])) for reason, bindings in sorted(na_outputs.items())},
		"unresolved_inputs": [],
		"unresolved_outputs": [],
		"projections": projections(),
		"drawing_callout_check": callout_check(definition),
		"excluded_object_classes": [
			"Kicker.CBKicker, Kicker.NBKicker and Kicker.CenterPostKicker: script helpers that create the captive ball, the Newton ball and the centre-post proxy ball at start-up",
			"Plunger.Plunger: the shooter-lane plunger, a manual mechanism with no controller address",
			"Flasher.OptionDMDFlasher and the VR cabinet primitives: render objects with no controller address",
			"Walls sw48a-sw50a and sw73a-sw75a: the second wall of each drop target in the table's DropTarget class; the placement is the primary wall",
		],
		"unresolved": [],
		"uncontrolled_lighting": gi_inventory(definition),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["drawing_callout_check"]
	gi = report["uncontrolled_lighting"]
	lines = [
		"# Breakshot (Capcom, 1996) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `partial` at "
		"`machines/partial/capcom/breakshot-1996.json`, and `spatial_placement` is its only missing requirement: every "
		"address carries a validated placement or a controlled `not_applicable` record and the record has no conflicts, but "
		"seven fixed G.I. sockets have only the lamp drawing's position.",
		"",
		"## Blockers",
		"",
		*[f"- {blocker}" for blocker in report["blockers"]],
		"",
		f"Promotion decision: {report['promotion_decision']}",
		"",
		f"The coordinate source is the retained known-working `Breakshot (Capcom 1996) VPW v1.1.vpx` at SHA-256 `{TABLE_SHA256}`, "
		f"whose embedded script (SHA-256 `{SCRIPT_SHA256}`) binds each switch, coil and lamp to a table object. Playfield bounds "
		f"are `{TABLE_BOUNDS}`; every coordinate is x/952 and y/2162 at no more than six decimals.",
		"",
		"## Evidence decisions",
		"",
		"- The retained script decides which table object stands for an address, except where the ROM proves the table wrong: "
		"its slingshots (41/42), its three star bumpers (57-59) and its right drop bank (48-51 against the ROM's 49-52) report "
		"other addresses than the machine, so those placements follow the ROM's names and the manual's drawings, not the table's "
		"switch numbers.",
		f"- The factory location drawings P62500, P62600 and P62400 check the placements: {check['validated']} of the "
		f"{check['checked']} checked placements land within {check['limit']} normalized of their own disc under both the "
		"control fit and the leave-one-out callout fit (`tools/drawing_callouts.py`, seed "
		f"`{check['seed']}`). The drawings print every number in a disc without a leader, so each read is recorded as a label "
		"beside its part.",
		"- The switch drawing numbers the right drop bank one lower than its own table, the ROM and the harness, so the bank's "
		"placements are checked against discs 48-51.",
		"- The solenoid drawing's disc 16 sits beside the left top gate's coil bracket; its read takes the bracket.",
		"- The lamp drawing prints no 27: the right top-lane insert, its only unlabelled lamp insert, is read as 27.",
		"- The trough (35-38) and its two coils (S1, S2) lie under the apron, where the drawings print their numbers in open "
		"space without a part. They are documented projections onto the script's trough objects, excluded from the check.",
		"- Lamp 11 has two bulbs under one Jackpot insert (the lamp matrix sheet's `(23) Jackpot (two)`). Its first placement "
		"is checked against disc 11; the second is a documented projection onto the first, excluded from the check.",
		f"- The 54 fixed G.I. sockets (65A-68Q) have no PinMAME output, so the definition has no device to carry them; "
		f"`uncontrolled_lighting` places them. {gi['counts']['validated']} take the centre of the retained table's G.I. light "
		f"that their own disc on the lamp drawing checks, and {gi['counts']['observed']} that the table does not model keep the "
		"drawing's position, observed only, which is the record's blocker. See the fixed general illumination section below.",
		"- Cabinet and backbox devices (coin switches, flipper and start buttons, slam and tilt, the knocker, the start lamp, the "
		"diagnostic LEDs and the DMD) carry controlled `cabinet_or_service` records.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({report['validated_placements']} validated)",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += ["", "## Drawing callout check", ""]
	for key, page in sorted(check["pages"].items()):
		lines.append(
			f"- {key} ({page['locator']}): {page['controls']} controls, control RMS {page['control_rms']}, "
			f"{page['callout_pairs']} callout pairs, worst leave-one-out offset {page['callout_loo_max']}"
		)
	lines += [
		"",
		"## Fixed general illumination",
		"",
		f"{gi['inventory']} {gi['rule']} The table's GI collection has {gi['table_lights']} distinct lights "
		f"(render double: {', '.join(f'{a} = {b}' for a, b in gi['render_doubles'].items())}); every one is paired. The "
		f"backbox fluorescent {gi['backbox']['socket']} carries a `{gi['backbox']['reason']}` disposition.",
		"",
		"| Socket | Wire | x | y | Status | Coordinate source | Control offset | Callout offset |",
		"| --- | --- | ---: | ---: | --- | --- | ---: | ---: |",
	]
	for entry in gi["sockets"]:
		offsets = (f"{entry['control_offset']} | {entry['callout_offset']}" if entry["status"] == "validated" else "- | -")
		lines.append(f"| {entry['socket']} | {entry['wire']} | {entry['x']} | {entry['y']} | {entry['status']} | {entry['coordinate_source']} | {offsets} |")
	lines.append("")
	lines += [f"- {entry['socket']}: {entry['note']}" for entry in gi["sockets"] if "note" in entry]
	lines += [
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Table archive SHA-256 `{TABLE_ARCHIVE_SHA256}` from VPUniverse file 20471.",
		f"- Callout reads and the seed generator under `external:pinmame-review-artifacts/{check['retained_artifacts']['directory']}`, "
		f"manifest SHA-256 `{check['retained_artifacts']['manifest_sha256']}`.",
		"",
	]
	return "\n".join(lines)


def callout_sentence(check: dict[str, Any]) -> str:
	return (
		f"The factory location drawings check {check['checked']} table placements and validate {check['validated']}: each "
		"drawing was fitted on its bumper caps, flipper pivots and playfield-outline corners and on its other discs, and a "
		f"placement validates when its own disc lands within {check['limit']} normalized under both fits "
		f"(`{check['seed']}`)."
	)


KNOWLEDGE_NOTE = """# Breakshot (Capcom, 1996)

Breakshot is Capcom Coin-Op's billiards-themed pinball of May 1996 (IPDB 3784, model BRK3002, 1,000 built),
designed by Greg Kmiec. It is a single-level playfield with no ramps, three flippers, three star bumpers, two drop-target
banks, a captive ball with a Newton ball, and a centre feature: a post that rises in front of three pockets. This note
collects what a table author needs beyond the structured definition `machines/partial/capcom/breakshot-1996.json`,
which is partial only because seven fixed G.I. sockets have no checked position (see General illumination).

## Identity and drivers

The physical machine is the one IPDB 3784 and the Capcom operator's manual PM00147 (issue 05/02/96) describe. PinMAME runs
it with five drivers: `bsv103` (1.3, the root and the only one built with `INITGAMEFF`), `bsv102` (1.2), `bsb105` (Beta
1.5) and the two redemption builds `bsv100r` and `bsv102r`. All five use the same switch inversion mask and flipper
declaration, so they share one address map; only `bsv103` publishes solenoid 51, the ROM's game-on (Fast Flips) state.
The redemption builds were not run for this record.

PinMAME also declares `pp100`, Illinois Pinball's Pool Player of 2000, as a clone of `bsv103` with the same routing. Pool
Player was built from Breakshot machines, but its own sources describe a modified playfield and versions with an
automatic ball launcher, so it is a partial record of its own, `illinois-pinball.pool-player.2000`.

## Controller and addresses

Breakshot runs on modified Capcom hardware without a switch board: it drives a single lamp matrix and strobes its
switches with the second lamp matrix's hardware (PinMAME's `hw.lampCol` is 1). That shapes its switch map:

- Public 1-8 are the coin door and cabinet inputs: coins 1-4, the two flipper buttons (5 left, 6 right), Start (7) and the
  coin-door switch (8).
- Public 9-16 are dead under PinMAME: nothing writes or reads internal column 0 on this board. The manual's "*9 COIN
  DOOR-SLAM" is read by the ROM at public 29.
- Public 17-80 are the strobed matrix. The ROM reads the slam switch at 29, the tilt bob at 30 and the upper right
  flipper button at 21.
- 81-88 are PinMAME's flipper column. 82 and 84 are the host inputs for the right and left flipper buttons (core copies
  them into 6 and 5 every frame); the end-of-stroke bits 81, 83 and 85 are rewritten every frame, and nothing acts on 86-88.

Every switch read is inverted by the board, and PinMAME's `capInvSw` mask normalizes the six optos (36-38, 53, 54, 65), so
a public 1 is a closed contact or a blocked beam: write 1 when a ball is present. `normally_closed` is false for every
contact switch and true for the six optos, whose receivers conduct while the beam is clear.

Solenoids 1-32 are the driver board's outputs, 17-24 and 27 unfitted. At the pinned revision PinMAME mirrors each flipper
coil to a power and a hold address: S9 (left) to 47/48, S10 (right) to 45/46 and S11 (upper right) to 33/34. The
repository's Capcom controller profile still describes an older mirror table (9 to 45 only, 10 to 47), and its bsv
flasher range (28-32) is also older than the pinned source, which types only 28 as a bulb; this record follows the pinned
source.

Lamps 1-64 are one 8x8 matrix; 65 and 66 are the CPU and sound board LEDs. General illumination has no PinMAME output.
The ROM's Lamp Test and the manual's lamp matrix sheet agree on every lamp's column, row and wire colours but print
different connectors (the ROM J5/6 and J7/8, the sheet J9/10 and J4/5); the record's wiring follows the ROM. The sheet
calls lamp 11 "Jackpot (two)": two bulbs, both under the one Jackpot insert below LIT POCKET AWARDS. No source shows where
they sit under it, so the record places the second bulb on the first, the centre of the table's light l11.

## Flippers

Three flippers: left (S9), right (S10) and upper right (S11, beside the bonus saucer). The right cabinet button carries two
switches, 6 for the right flipper and 21 for the upper right one; the drawing prints them side by side. In the harness,
holding 21 fired S11. The VPinMAME system script maps a staged right flipper key to 81 instead, which the ROM never sees, so
a recreation that wants the upper flipper on its own key must drive 21. Each flipper has an end-of-stroke switch the ROM
reads (33 left, 34 right, 71 upper right); the retained table never writes them.

## Trough, outhole and shooter lane

A drained ball rolls into the outhole under the apron (35). S1 kicks it into a three-ball trough under the apron that rises
towards the shooter lane, sensed by optos 38, 37 and 36, position 1 (36) at the shooter end. S2 serves the ball from
position 1 into the shooter lane (43), and the player plunges it by hand. At start-up the trough holds all three balls, so
36-38 read 1. Pressing Start with a credit fires S2 together with both drop-bank resets (S7 and S13); in the harness the
ROM pulsed S2 five times while 36 stayed closed and released it once the ball left position 1.

## Drop-target banks

Both banks have three drops and a standup behind them. The right bank on the upper right is 49 (left), 50 (centre) and 51
(right) with the standup 52, reset by S7; the left bank is 73 (lowest), 74 and 75 (highest) with the standup 76, reset by
S13. In the harness, dropping 49, 50 and 51 took the score from 0 to 9,000, and dropping 73 and 74 each played the ROM's
drop-target animation. The ROM resets both banks with the trough eject when Start begins a game. With a bank's three drops
held down for four seconds it fired neither reset, and the run served no further ball, so when it resets a completed bank
during play was not observed.

Two sources number the right bank one lower: the manual's switch drawing (discs 48-51) and the retained table (drops 48-50,
standup 51). The manual's own table, the ROM's Switch Test and the harness agree on 49-52: 48 alone changes nothing.

## Centre feature

At the centre, two Lite Super Cue targets (77, 78) flank a post (S12 up, S14 down; switch 66 closed while it is up) at the
foot of the centre pocket assembly, and an opto (65) sits at the assembly's foot. Behind the post are three pockets side by
side, each with a switch (68, 69, 70) and an eject coil (S25, S26, S32), lit by inserts 42-44 and by the matrix lamps 25 and
26 (Center Pocket G.I.). The Center Pocket Flash, S28 (part LP00103), lights two bulbs above the pockets, one on
each shoulder of the assembly; PinMAME models it as a #89 bulb. IPDB describes the feature as a
large metal plug that rises after each captured ball and that the player hits, with three scoops behind it that hold balls
for multiball. The retained table raises three walls for the post and sets 66 once it is up.

## Other playfield features

- Star bumpers: 57 and S31 on the upper left, 58 and S30 at the lower centre, 59 and S29 on the upper right.
- Captive ball lane, upper left: the Newton ball passes a hit to the captive ball, which rolls over the captive rollover
  (79) to the captive standup (55). Lamps 3-5 and 8 line it.
- Top lanes 60, 61 and 62 under inserts 45, 32 and 27; the orbit optos 53 and 54 at the left and right orbit entrances;
  the bankshot lane 63 on the upper right (lamp 49).
- Top gates S16 (left) and S15 (right) on the 20 V line: each gate stands open while its coil is energized.
- Left outlane kickback S6, lit by lamp 28 KICKER; bonus saucer 67 with S8 below the upper right flipper.
- The bonus rack: lamps 50-64 in a triangle pointing down above the flippers, 60-64 across its top.

## Redemption and the optional dispensers

The manual documents a redemption setup the standard machine does not ship with
(`evidence/excerpts/capcom.breakshot.1996/redemption-and-dispensers.md`). Its Redemption menu (F, PDF 55), which it says
is not in every software version, pays tickets, tokens, credits or extra balls at up to five score levels within a time
limit, through an optional ticket dispenser (adjustment B1-16: Deltronics model 1275 or Coin Controls CTD10) or token
dispenser (B1-17: a Bally Wulff or Coin Controls dispenser, or a Coin Controls Compact Hopper). The ticket dispenser has a
motor, a notch switch and a meter (test C1-09); a token dispenser is fired by a solenoid and usually has no feedback
switch (test C1-10). Both hang off the RS232/Coin Meter PCB on the CPU's J3, which carries a ticket meter, a coin meter
and a motor drive line; in the German configuration a Token Driver PCB switches 50 V to the token dispenser (PB-6
wiring, PDF 145). `bsv100r` and `bsv102r` are the redemption builds.

None of this reaches a PinMAME address. Pinned `capcom.c` leaves the J3 lines unmapped, so no dispenser motor, solenoid
or meter is published. The ROM numbers the ticket dispenser's notch switch 16 (WHT-GRY), in the cabinet column PinMAME
never reads on Breakshot, and its Switch Test shows that name while public 32, 40, 64 or 72 is held, positions the
standard machine leaves empty. The structured definition records the standard machine; a recreation of a redemption
Breakshot has to model the dispenser outside the emulator.

## General illumination

The lamp table lists 54 #44 G.I. bulbs (LP00104) on four strings, 65A-65P (ORG/WHT, 14 bulbs), 66A-66N (BLU/WHT, 13),
67A-67M (GRN/WHT, 12) and 68A-68Q (BLK/WHT, 15), lettered without I and O, and the backbox fluorescent 69. The ROM does
not switch them and PinMAME has no output for them, so the structured definition has no device to carry them.

The lamp drawing marks every socket with its string and letter, so the strings' membership is the machine's own. The
retained table models 47 of the sockets as always-on lights of its `GI` collection, the bake sources of its G.I.
lightmaps (gi014 repeats gi011 exactly). Each socket's disc was paired one-to-one, nearest first, with a table light
and checked like the lamp placements: under the page's control fit and its callout fit on {GI_FIT_PAIRS} lamp discs,
all 47 pairs land within the 0.07 callout limit, most within 0.01, and those sockets take the light's centre. 66L and
66N are the loosest, about 0.057 from gi044 and gi045: the drawing prints their discs below 66K and 66M, while the
table puts the two lights above. Seven sockets have no table light and keep their disc's position through the control
fit, observed only: 67A, 67B and 67F across the top, 68B at the top right, 68K on the right, and 65A and 65B, printed
just inside the outline's front edge beside disc 1 where the drawing shows no part. A disc is printed on or beside its
socket and is about 0.05 of the playfield width across, so a drawing-only position is good to a few hundredths. The
spatial report carries the same inventory with every offset (`uncontrolled_lighting` in
`reports/spatial/capcom/breakshot-1996.json`).

Those seven sockets are why the record is `partial`, with `spatial_placement` its only missing requirement: a position
read off a drawing alone is not a checked one, and the two at the front edge may not even light the playfield. A
recreation that models them, or a drawing that locates them, checked against a photograph of a Breakshot playfield
showing them (with the apron removed for 65A and 65B), would settle it.

{GI_SOCKETS}

## Defects in the retained table

The VPW v1.1 table plays correctly on bsv103 but reports several switches as other addresses than the machine. Each is a
defect of the table, recorded on the device it affects:

- Its slingshots are crossed (the left reports 42, the right 41).
- Its star bumpers are rotated (upper left reports 58, lower centre 59, upper right 57).
- Its right bank is numbered one lower (48-50 and the standup 51), so the ROM never sees its first drop.
- The comments beside its three flipper callbacks name the wrong flippers; the bindings themselves are right.

## Spatial placements

Every playfield placement is the centre of the retained table's object that the script binds to the address, or the
mechanism the switch or coil belongs to. {CALLOUT_CHECK} The trough and its two coils lie under the apron, where the
drawings print only numbers in open space, so they are documented projections onto the script's trough objects. Lamp 11's
second bulb is a documented projection onto its first, under the same Jackpot insert.

## Sources

- Capcom operator's manual PM00147, 05/02/96, from IPDB: switch, solenoid and lamp tables and location drawings, the
  redemption menu, dispenser adjustments and tests, and the PB-6 interface wiring (excerpts under
  `evidence/excerpts/capcom.breakshot.1996/`).
- The ROM's own Switch, Solenoid and Lamp Tests and a short game, run on LibPinMAME from the pinned source
  (`evidence/runtime/capcom/breakshot-service-diagnostics.json`).
- PinMAME `src/wpc/capgames.c`, `capcom.c`, `capcom.h`, `core.h` and `core.c` at the pinned revision.
- VPW's Breakshot v1.1 table and its script, with the VPinMAME `Capcom.vbs` and `core.vbs` it loads.
"""


# The lamp table's G.I. strings: wire colour and socket count, lettered without I and O.
GI_STRINGS = {"65": ("ORG/WHT", 14), "66": ("BLU/WHT", 13), "67": ("GRN/WHT", 12), "68": ("BLK/WHT", 15)}
GI_LETTERS = "ABCDEFGHJKLMNPQ"
GI_PAGE = "pdf-74"
# Centre of every light in the retained table's GI collection (Light.gi*), x/952 and y/2162. The script switches none of
# them: they are the bake sources of the table's G.I. lightmaps (LM_GI_*), always on.
GI_LIGHTS = {
	"gi001": (0.045357, 0.640573), "gi002": (0.046325, 0.606177), "gi003": (0.045034, 0.578318),
	"gi004": (0.042129, 0.549037), "gi005": (0.045679, 0.457784), "gi006": (0.072795, 0.426514),
	"gi007": (0.062788, 0.389273), "gi008": (0.076345, 0.353739), "gi009": (0.039869, 0.272008),
	"gi01": (0.68459, 0.83202), "gi010": (0.04116, 0.134987), "gi011": (0.050844, 0.102863),
	"gi012": (0.085384, 0.079979), "gi013": (0.211139, 0.136301), "gi015": (0.254243, 0.131809),
	"gi02": (0.749976, 0.811944), "gi020": (0.634013, 0.141093), "gi021": (0.656835, 0.080996),
	"gi022": (0.361001, 0.016396), "gi023": (0.471435, 0.017461), "gi024": (0.558492, 0.017816),
	"gi025": (0.801125, 0.026689), "gi026": (0.88197, 0.05177), "gi028": (0.939216, 0.367124),
	"gi029": (0.9315, 0.39401), "gi03": (0.681409, 0.775839), "gi030": (0.880506, 0.456449),
	"gi031": (0.791936, 0.460388), "gi032": (0.850088, 0.576601), "gi033": (0.831301, 0.602208),
	"gi034": (0.867981, 0.619936), "gi04": (0.719227, 0.731173), "gi043": (0.337517, 0.373536),
	"gi044": (0.307068, 0.345846), "gi045": (0.599293, 0.346424), "gi046": (0.569371, 0.373206),
	"gi047": (0.253064, 0.205888), "gi048": (0.151773, 0.03267), "gi05": (0.222659, 0.832005),
	"gi06": (0.156754, 0.811838), "gi07": (0.225452, 0.776547), "gi08": (0.18831, 0.731663),
	"gi09": (0.613609, 0.099964), "gi10": (0.506602, 0.100163), "gi11": (0.398687, 0.100163),
	"gi12": (0.291225, 0.100363), "gi13": (0.778516, 0.147564),
}
# gi014 repeats gi011 exactly (centre, height, falloff radius 57 and intensity 5): a render double of one light.
GI_RENDER_DOUBLES = {"gi014": "gi011"}
# The sockets no table light stands for, which keep the drawing's own position; gi_sockets refuses any other outcome.
GI_DRAWING_ONLY = ("65A", "65B", "67A", "67B", "67F", "68B", "68K")
GI_NOTES = {
	"65A": "Printed just inside the outline's front edge beside disc 1 (the start button), where the drawing shows no part and the table models no light, so what the bulb lights there, such as the apron, is not established.",
	"65B": "Printed just inside the outline's front edge beside disc 1 (the start button), where the drawing shows no part and the table models no light, so what the bulb lights there, such as the apron, is not established.",
}
GI_BLOCKER = (
	"Seven of the 54 fixed G.I. sockets the lamp location drawing P62400 (PDF 74) marks have no checked position: 67A, 67B "
	"and 67F across the top arch, 68B at the top right and 68K on the right side, for which the retained table models no "
	"light, and 65A and 65B, printed just inside the playfield outline's front edge beside the start button on no drawn "
	"part, so what they light, the apron perhaps, is not established. Each keeps its disc's position through the drawing's "
	"control fit, observed only, so the uncontrolled lighting of the playfield is not fully placed. Resolution path: a "
	"recreation that models these sockets, or a drawing that locates them, checked against a photograph of a Breakshot "
	"playfield showing them, with the apron removed for 65A and 65B, which any owner can take."
)
PROMOTION_DECISION = (
	"partial: seven fixed G.I. sockets have only the lamp drawing's position. Otherwise every switch, coil, lamp and "
	"display address carries a validated placement or a controlled not-applicable record, every placement the factory "
	"drawings mark agrees with its callout, the other 47 G.I. sockets sit on the table light their own disc checks, and the "
	"definition carries no conflict."
)
GI_BACKBOX = {
	"socket": "69",
	"label": "FLUORESCENT IN BACKBOX",
	"wire": "WHT/BLK",
	"bulb": "T815W",
	"part_number": "LP00102",
	"reason": "cabinet_or_service",
	"note": "The backbox fluorescent tube, printed at the left of the drawing's backbox box; no playfield position.",
}


def gi_sockets(definition: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
	"""Every fixed G.I. socket the lamp drawing marks, on the table light its own disc checks or measured on the drawing.

	Sockets and table lights pair one-to-one, nearest first under the page's control fit, the way
	drawing_callouts pairs callouts with placements; a pair validates when the disc lands within the callout
	limit of the light under both the control fit and the callout fit, and the socket then takes the light's
	centre. A socket without such a light keeps its disc's position through the control fit, rounded to the
	three decimals `drawing_callouts.measured` uses, and stays observed.
	"""
	seed = callout_seed()
	page = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition))["pages"][GI_PAGE]
	reads = {read["label"]: read for read in seed["pages"][GI_PAGE]["reads"] if read["label"][:2] in GI_STRINGS and not read["label"].isdigit()}
	expected = [string + letter for string, (_, count) in GI_STRINGS.items() for letter in GI_LETTERS[:count]]
	if sorted(reads) != expected:
		raise RuntimeError(f"the lamp drawing's G.I. reads are not the lamp table's 54 sockets: {sorted(set(reads) ^ set(expected))}")
	drawn = {label: (drawing_callouts.apply(page["control_fit"], reads[label]["pixel"]), drawing_callouts.apply(page["callout_fit"], reads[label]["pixel"]))
	         for label in expected}
	options = sorted((drawing_callouts.distance(drawn[label][0], xy), label, name) for label in expected for name, xy in GI_LIGHTS.items())
	paired: dict[str, str] = {}
	for _, label, name in options:
		if label not in paired and name not in paired.values():
			paired[label] = name
	sockets: list[dict[str, Any]] = []
	for label in expected:
		by_controls, by_callouts = drawn[label]
		entry: dict[str, Any] = {
			"socket": label,
			"wire": GI_STRINGS[label[:2]][0],
			"bulb": "#44",
			"part_number": "LP00104",
			"drawing_read": list(reads[label]["pixel"]),
			"drawing_point": [round(by_controls[0], 3), round(by_controls[1], 3)],
		}
		name = paired.get(label)
		offsets = (drawing_callouts.distance(by_controls, GI_LIGHTS[name]), drawing_callouts.distance(by_callouts, GI_LIGHTS[name])) if name else None
		if offsets and max(offsets) <= drawing_callouts.LIMIT:
			x, y = GI_LIGHTS[name]
			entry.update(x=x, y=y, status="validated", coordinate_source=f"Light.{name}",
			             control_offset=round(offsets[0], 4), callout_offset=round(offsets[1], 4))
		else:
			x, y = entry["drawing_point"]
			entry.update(x=x, y=y, status="observed", coordinate_source=f"lamp drawing {GI_PAGE}, control fit")
		if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
			raise RuntimeError(f"G.I. socket {label} falls outside the playfield: ({x}, {y})")
		if label in GI_NOTES:
			entry["note"] = GI_NOTES[label]
		sockets.append(entry)
	claimed = {entry["coordinate_source"].removeprefix("Light.") for entry in sockets if entry["status"] == "validated"}
	if claimed != set(GI_LIGHTS):
		raise RuntimeError(f"table G.I. lights no drawn socket checks: {sorted(set(GI_LIGHTS) - claimed)}")
	drawing_only = tuple(entry["socket"] for entry in sockets if entry["status"] == "observed")
	if drawing_only != GI_DRAWING_ONLY:
		raise RuntimeError(f"the G.I. sockets without a table light changed: {drawing_only}")
	return sockets, page


def gi_inventory(definition: dict[str, Any]) -> dict[str, Any]:
	sockets, page = gi_sockets(definition)
	return {
		"binding": "none: the ROM does not switch the G.I. and PinMAME publishes no output for it, so the definition has no device to carry these sockets",
		"inventory": "The lamp table (PDF 75): 54 #44 G.I. bulbs (LP00104) on strings 65 (ORG/WHT, 14), 66 (BLU/WHT, 13), 67 (GRN/WHT, 12) and 68 (BLK/WHT, 15), lettered without I and O, and the backbox fluorescent 69. The lamp drawing (PDF 74) marks each socket with its string and letter, so string membership is the machine's own, not the table's grouping.",
		"rule": (
			f"Each socket's disc on {GI_PAGE} pairs one-to-one, nearest first under the control fit, with a light of the retained table's GI "
			f"collection. The socket takes the light's centre (status validated) when the disc lands within {drawing_callouts.LIMIT} normalized "
			"of it under both the control fit and the callout fit; otherwise it keeps the disc's position through the control fit at three "
			"decimals (status observed). A disc is printed on or beside its socket and is about 0.05 of the playfield width across."
		),
		"source_refs": [MANUAL_SOURCE, VPX_EXTRACTION_SOURCE, CALLOUT_SOURCE],
		"drawing_page": GI_PAGE,
		"control_fit_controls": page["controls"],
		"callout_fit_pairs": page["callout_fit_pairs"],
		"limit": drawing_callouts.LIMIT,
		"table_lights": len(GI_LIGHTS),
		"render_doubles": GI_RENDER_DOUBLES,
		"sockets": sockets,
		"counts": {
			"sockets": len(sockets),
			"validated": sum(entry["status"] == "validated" for entry in sockets),
			"observed": sum(entry["status"] == "observed" for entry in sockets),
		},
		"backbox": GI_BACKBOX,
	}


def gi_socket_table(definition: dict[str, Any]) -> str:
	sockets, _ = gi_sockets(definition)
	lines = ["| Socket | String wire | x | y | Position from |", "| --- | --- | ---: | ---: | --- |"]
	for entry in sockets:
		if entry["status"] == "validated":
			basis = f"table light {entry['coordinate_source'].removeprefix('Light.')}, disc within {max(entry['control_offset'], entry['callout_offset']):.3f}"
		else:
			basis = "drawing only (observed)"
		lines.append(f"| {entry['socket']} | {entry['wire']} | {entry['x']:.3f} | {entry['y']:.3f} | {basis} |")
	return "\n".join(lines)


def knowledge_text(definition: dict[str, Any]) -> str:
	_, page = gi_sockets(definition)
	return (
		KNOWLEDGE_NOTE.replace("{CALLOUT_CHECK}", callout_sentence(callout_check(definition)))
		.replace("{GI_FIT_PAIRS}", str(page["callout_fit_pairs"]))
		.replace("{GI_SOCKETS}", gi_socket_table(definition))
	)


POOL_PLAYER_KNOWLEDGE_NOTE = """# Pool Player (Illinois Pinball, 2000)

Coverage: **partial - identity, driver and Capcom platform only. No input, output, display or mechanism inventory is
recorded yet.**

This record holds PinMAME's one Pool Player driver, `pp100` (Pool Player (1.0)). It was split from
`capcom.breakshot.1996`, whose curator `tools/curate_breakshot.py` writes and checks it.

## What is known

- IPDB 4495 lists Pool Player as Illinois Pin Ball Incorporated's game of 2000 (trade name IPB), a solid-state
  four-player game with an acrylic backglass. Its notes say the playfield is Breakshot's, reportedly slightly modified,
  and that none was ever sold to the public. Pinside lists it as a conversion kit with a dot-matrix display, three
  flippers and no ramps.
- Pinball News reported in October 2000 that Illinois Pinball's founder, Gene Cunningham, had bought Capcom's remaining
  stock, and that the company's Pool Player flyer shows three games that look like rebranded Breakshots with differences
  between them: two with automatic ball launchers and one with a manual launcher, and silver, black and gold legs with
  matching trim.
- PinMAME declares `pp100` a clone of Breakshot's `bsv103` with Breakshot's switch inversion mask, flipper set and sound
  ROMs, so it routes exactly as Breakshot does. Shared routing does not show that the cabinet matches.

The sources are excerpted under `evidence/excerpts/illinois-pinball.pool-player.2000/`.

## Why it is not part of the Breakshot record

`capcom.breakshot.1996` describes the machine Capcom's manual documents, whose ball is plunged by hand. Pool Player's
own sources describe a modified playfield and versions with an automatic ball launcher, hardware Breakshot does not have,
and none says which version `pp100` ran on. Until that is known the firmware cannot be called compatible with Breakshot,
so its driver is `unknown` here.

## What a curator must establish next

- The OPDB identity: the pinned snapshot has no Pool Player record.
- How the playfield differs from Breakshot's, and how each version's automatic launcher is fitted and driven, including
  which solenoid and switch addresses it uses under `pp100`. Photographs, an owner or the ROM itself could settle it;
  the authorized ROM library holds no copy.
- The full input, output and display inventory. Breakshot's record is a starting point only: every address has to be
  confirmed against this firmware.
- Wiring, polarity, mechanism behaviour and normalized placements.
"""


def artifacts() -> dict[Path, bytes]:
	definition = build()
	report = build_spatial_report(definition)
	return {
		DEFINITION_PATH: canonical_bytes(definition),
		SEED_PATH: canonical_bytes(definition),
		KNOWLEDGE_PATH: knowledge_text(definition).encode("utf-8"),
		SPATIAL_REPORT_PATH: canonical_bytes(report),
		SPATIAL_REPORT_MARKDOWN_PATH: render_spatial_report(report).encode("utf-8"),
		POOL_PLAYER_PATH: canonical_bytes(build_pool_player()),
		POOL_PLAYER_KNOWLEDGE_PATH: POOL_PLAYER_KNOWLEDGE_NOTE.encode("utf-8"),
	}


def generate() -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"refusing to write a partial record beside the author-ready one: {AUTHOR_READY_PATH.relative_to(ROOT).as_posix()}")
	for path, data in artifacts().items():
		write_text(path, data.decode("utf-8"))
	return DEFINITION_PATH


def check() -> None:
	for path, data in artifacts().items():
		if not path.is_file() or path.read_bytes() != data:
			raise RuntimeError(f"Breakshot artifact drifted from its deterministic curator: {path.relative_to(ROOT).as_posix()}")
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"an author-ready copy of the partial record exists: {AUTHOR_READY_PATH.relative_to(ROOT).as_posix()}")
	print("Breakshot definition, seed, knowledge note and spatial review, and the Pool Player record, match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and every artifact it writes")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, its seed, the knowledge note and the spatial review")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Breakshot extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Breakshot retained extraction matches its pinned manifest identity.")
	elif args.check:
		check()
	else:
		print(f"Wrote {generate().relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
	main()
