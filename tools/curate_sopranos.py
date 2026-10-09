"""Curate the physical Stern The Sopranos (2005) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads two committed seeds, the placements (the retained table's object coordinates, rebuilt by
tools/sopranos_spatial_seed.py) and the factory drawing callout check, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is
the only path that writes the definition, its knowledge note and its spatial report.
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

MACHINE_ID = "stern.the-sopranos.2005"
PARTIAL_PATH = ROOT / "machines/partial/stern/the-sopranos-2005.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-sopranos-2005.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/the-sopranos-2005.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/stern/the-sopranos-2005.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/stern/the-sopranos-2005-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/stern/the-sopranos-2005-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/the-sopranos-2005.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/the-sopranos-2005.md"
RUNTIME_EVIDENCE_PATH = "evidence/runtime/whitestar/the-sopranos-stacking-opto-and-gameplay.json"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.stern.the-sopranos.2005"
MANUAL_SOURCE = "manual.stern.the-sopranos.2005"
VPX_TABLE_SOURCE = "vpx-table.sopranos-freneticamnesic-32assassin-1-0-2"
VPX_SCRIPT_SOURCE = "vpx-script.sopranos-freneticamnesic-32assassin-1-0-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.sopranos-freneticamnesic-32assassin-1-0-2"
VPX_CORPUS_SOURCE = "vpx-script.sopranos-v1-22"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.the-sopranos.stacking-opto-and-gameplay"
ROM_SOURCE = "rom.stern.the-sopranos.5-00"
CALLOUT_SOURCE = "drawing-callouts.the-sopranos.2026-10-09"
RUNTIME_LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "4d32c78ad266b18aa9abb508c63f924b92bdd8e88f933ff4e93a0a70d686a401"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/sopranos_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"sopranos-stacking-opto": "de91a43d8bc616768c3652f5204c4e461d467198be86c98bc60d5e2dd0475b3f",
	"sopranos-stacking-opto-boot-active": "7e9ea152c884fed50d69b9bf663ce86222e65cd990cd753da1715dc8df8edd64",
	"sopranos-gameplay": "042fdd91dd534fd2f6c0e22119f2a859660a594def07993730daf483f27b9ec2",
}

TABLE_NAME = "Sopranos, The (Stern 2005).vpx"
TABLE_SHA256 = "9bbc98d47888c28843cf17aa7f8ce5d04671da86ee1e76ddb1f2cd330b30162c"
SCRIPT_SHA256 = "56262b8bb13d295504abe54f0f586a5e6d288cb4f4b55963889d13c7ba57de08"
CORPUS_SCRIPT_SHA256 = "ab44cf364d11bc420c2aa85605ba02a7e0695138e86d08001ddc34ce4b035a36"
VPX_CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
MANUAL_NAME = "Stern_2005_The_Sopranos_Service_Manual.pdf"
MANUAL_IPDB_NAME = "Stern_2005_The_Sopranos_Pinball_Game_Service_Manual_labeled_as_Pinball_Service_Game_Manual.pdf"
MANUAL_SHA256 = "4765c79a9fac44d14e4330477ffb4ab4d7af259499a3b5d1156adf83d75b0c88"
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2300.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2300"

EXTRACTION_FILE_COUNT = 1441
EXTRACTION_TOTAL_BYTES = 115101357
EXTRACTION_MANIFEST_SHA256 = "7e2a9c25d8f694b6f6cf24b375f9d95b6450f4a1463ba245a0487a93395dc091"
EXTRACTION_RELATIVE_PATH = Path("stern/the-sopranos-2005/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/the-sopranos-2005/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-archive"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=5053"
MANUAL_URL = "https://www.ipdb.org/files/5053/" + MANUAL_IPDB_NAME
EXCERPT_CREDIT = "curator, read from the rendered page"
TEXT_CREDIT = "curator, transcribed from the PDF text layer and checked against the rendered page"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = (
	"sopranos", "sopranof", "sopranog", "sopranoi", "sopranol",
	"sopr400", "sopr400f", "sopr400g", "sopr400i", "sopr400l",
	"sopr300", "sopr300f", "sopr300g", "sopr300i", "sopr300l", "soprano3",
	"sopr204", "sopr107f", "sopr107g", "sopr107i", "sopr107l",
)
LANGUAGE = {"f": "French", "g": "German", "i": "Italian", "l": "Spanish"}


def _driver_note(driver_id: str) -> str:
	base = (
		"segames.c builds every Sopranos driver from one init_sopranos (INITGAME(sopranos, GEN_WS, se_dmd128x32, "
		"SE_BOARDID_520_5068_01)), so the controller routing, lamp columns, display and auxiliary board are identical; "
	)
	if driver_id == "sopranos":
		return base + "CPU 5.00 (sopcpua.500) with display 5.00 and the English sound set, the pinned parent driver the retained tables load (cGameName = \"sopranos\") and every harness run booted."
	if driver_id == "soprano3":
		return base + "CPU 3.00 (the same sopcpua.300 as sopr300) with display 3.00 and an alternative sound set whose U7 differs (segames.c: 'alternative sound feat a unique U7'); a sound-ROM difference on unchanged hardware."
	if driver_id == "sopr204":
		return base + "CPU 2.04 (sopcpua.204) with display 2.00 and the earlier sopsnd1 sound set: an earlier production firmware of the same machine."
	match = re.fullmatch(r"sopr(\d)(\d\d)([fgil]?)", driver_id)
	if match:
		version = f"{match.group(1)}.{match.group(2)}"
		language = LANGUAGE.get(match.group(3), "English")
		return base + f"CPU {version} with the {language} display and sound set: a firmware or language revision of the same machine."
	language = LANGUAGE[driver_id[-1]]
	return base + f"CPU 5.00 with the {language} display and sound set: a language revision of the same machine."


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, printed name, mounting, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, str, tuple[str, ...], bool]] = {
	1: ("Left Cabinet Button (UK Only)", "LT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-left",), False),
	2: ("4th Coin Slot", "4TH COIN SLOT", "Coin Door", "180-5204-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot", "6TH COIN SLOT", "Coin Door", "Future Use", "other", "optional", ("cabinet.coin.sixth",), True),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "Coin Door", "180-5204-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "Coin Door", "Future Use", "other", "optional", ("cabinet.coin.fifth",), True),
	8: ("Right Cabinet Button (UK Only)", "RT BUTTON (UK ONLY)", "Cabinet Side", "180-5160-00", "button", "optional", ("cabinet.uk-button-right",), False),
	9: ("Left Ramp", "LEFT RAMP", "Above P/F", "180-5010-01", "microswitch", "used", ("ball.path",), True),
	10: ("Safe Limit", "SAFE LIMIT", "Below P/F", "180-5198-00", "microswitch", "used", ("position.limit",), False),
	11: ("4-Ball Trough 1 (Left)", "4-BALL TROUGH #1 (LEFT)", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	12: ("4-Ball Trough 2", "4-BALL TROUGH #2", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	13: ("4-Ball Trough 3", "4-BALL TROUGH #3", "Below P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	14: ("4-Ball Trough VUK Opto", "4-BALL TROUGH VUK OPTO", "Below P/F", "See Sw. 14 Note", "opto", "used", ("ball.position",), False),
	15: ("4-Ball Stacking Opto", "4-BALL STACKING OPTO", "Below P/F", "See Sw. 15 Note", "opto", "used", ("ball.path",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "Below P/F", "180-5157-00", "microswitch", "used", ("ball.position",), False),
	17: ("Left Eject", "LEFT EJECT", "Below P/F", "180-5186-01", "microswitch", "used", ("ball.position",), False),
	18: ("Left Orbit", "LEFT ORBIT", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	19: ("Bing 1", "BING 1", "Above P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	20: ("Bing 2", "BING 2", "Above P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	21: ("Safe Hit Left", "SAFE HIT LEFT", "Above P/F", "180-5119-02", "microswitch", "used", (), True),
	22: ("Center Lock 1", "CENTER LOCK 1", "Above P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	23: ("Center Lock 2", "CENTER LOCK 2", "Above P/F", "180-5119-02", "microswitch", "used", ("ball.position",), False),
	24: ("Safe Hit Right", "SAFE HIT RIGHT", "Above P/F", "180-5119-02", "microswitch", "used", (), True),
	25: ("Right Ramp", "RIGHT RAMP", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	26: ("Drop Target", "DROP TARGET", "Below P/F", "180-5158-00", "other", "used", (), False),
	27: ("Spinner", "SPINNER", "Above P/F", "180-5010-04", "microswitch", "used", (), True),
	28: ("Center Eject", "CENTER EJECT", "Below P/F", "180-5186-01", "microswitch", "used", ("ball.position",), False),
	29: ("Right Ramp Exit", "RIGHT RAMP EXIT", "Above P/F", "180-5010-01", "microswitch", "used", ("ball.path",), True),
	31: ("Boat Lock 1", "BOAT LOCK 1", "Above P/F", "180--5119-02", "microswitch", "used", ("ball.position",), False),
	32: ("Boat Lock 2", "BOAT LOCK 2", "Above P/F", "180--5119-02", "microswitch", "used", ("ball.position",), False),
	33: ("Right Orbit", "RIGHT ORBIT", "Above P/F", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	34: ("Left Standup", "LEFT STANDUP", "Below P/F", "180-5132-00", "leaf", "used", (), True),
	35: ("Center Standup", "CENTER STANDUP", "Below P/F", "180-5132-00", "leaf", "used", (), True),
	36: ("Right 2-Bank Top", "R. 2-BANK TOP", "Below P/F", "180-5133-00", "leaf", "used", (), True),
	37: ("Right 2-Bank Bottom", "R. 2-BANK BOTTOM", "Below P/F", "180-5133-00", "leaf", "used", (), True),
	38: ("Left Top Lane", "LEFT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	39: ("Middle Top Lane", "MIDDLE TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	40: ("Right Top Lane", "RIGHT TOP LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	49: ("Left Bumper", "LEFT BUMPER", "Below P/F", "180-5015-04", "leaf", "used", (), True),
	50: ("Right Bumper", "RIGHT BUMPER", "Below P/F", "180-5015-04", "leaf", "used", (), True),
	51: ("Bottom Bumper", "BOTTOM BUMPER", "Below P/F", "180-5015-04", "leaf", "used", (), True),
	53: ("Slam Tilt (Optional)", "SLAM TILT (OPT)", "In Cabinet", "180-", "tilt", "optional", ("cabinet.slam-tilt",), False),
	54: ("Start Button", "START BUTTON", "In Cabinet", "180-5174-00", "button", "used", ("cabinet.start",), False),
	55: ("Tournament Start", "TOURNA- MENT START", "In Cabinet", "180-5174-00", "button", "optional", ("cabinet.tournament-start",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "In Cabinet", "See Sw. 56 Note", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "Below P/F", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "Below P/F", "180-5054-00 (x2)", "leaf", "used", (), True),
}
UNUSED_SWITCHES = (30, 41, 42, 43, 44, 45, 46, 47, 48, 52, 63, 64)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# The parts page's item description for each matrix switch (PDF 83, printed 66); see mechanism-assemblies excerpt.
SWITCH_PART_DESCRIPTIONS = {
	**{n: "Roll-Over Switch (Right Mount Style) assembly 500-6227-02 (item A-#)" for n in (38, 39, 40, 57, 58, 60, 61)},
	36: "Switch & Target Asm. Rect. (White) 515-6027-08 with Stack Sw. Radius End 180-5133-00 (item B-#)",
	37: "Switch & Target Asm. Rect. (White) 515-6027-08 with Stack Sw. Radius End 180-5133-00 (item B-#)",
	34: "Switch & Target Asm. Narrow (Yellow) 515-5967-06 with Stack Sw. Square End 180-5132-00 (item C-#)",
	35: "Switch & Target Asm. Narrow (Yellow) 515-5967-06 with Stack Sw. Square End 180-5132-00 (item C-#)",
	16: "Switch (for Shooter Lane) 180-5157-00 (item D-16)",
	17: "Switch (for Ejects) 180-5186-01 (item E-#)",
	28: "Switch (for Ejects) 180-5186-01 (item E-#)",
	9: "Switch (15/8\" Actuator) (for Wire Gates) 180-5010-01 (item F-#)",
	29: "Switch (15/8\" Actuator) (for Wire Gates) 180-5010-01 (item F-#)",
	**{n: "Switch Asm., Stack (Blade) (for Pops) 515-6459-09 with switch 180-5015-04 (item G-#)" for n in (49, 50, 51)},
	**{n: "Switch (Roller Actuator, Lite-Force) 180-5119-02 (item H-#)" for n in (19, 20, 21, 22, 23, 24, 31, 32)},
	**{n: "Switch (Roller Actuator, Lite-Force) 180-5119-02 (item I-#)" for n in (11, 12, 13)},
	14: "Dual OPTO TRANS PC Board Asm. 515-0173-00 and Dual OPTO REC PCB Assembly 515-0174-00 (items J-# and K-#)",
	15: "Dual OPTO TRANS PC Board Asm. 515-0173-00 and Dual OPTO REC PCB Assembly 515-0174-00 (items J-# and K-#)",
	59: "Switch, Stack (Blade) (for Slings) 180-5054-00, two per slingshot (item M-#)",
	62: "Switch, Stack (Blade) (for Slings) 180-5054-00, two per slingshot (item M-#)",
	26: "Switch (for Drop Target) 180-5158-00 (item N-26)",
	10: "Sw. (Custom Actuator) Cherry DA3A-B1A 180-5198-00 (item O-10)",
	**{n: "Switch (for Wire Gates) 180-5087-00 (item P-#)" for n in (18, 25, 33)},
	27: "Switch (1-1/4\" Actuator) 180-5010-04 (item Q-27)",
}
# What the retained 1.0.2 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	9: "Gate sw9's Hit handler pulses 9 (line 366)",
	10: "PrisonT_Timer sets 10 when its door animation finishes opening and clears it when it finishes closing (lines 203-231); SolSafe opens the door only while Q8 is off and the Safe Latch has not set Latch (lines 175-186)",
	11: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 282-285): a cvpmBallStack holding 11 at 1 while a ball occupies that position",
	12: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 282-285)",
	13: "bsTrough.InitSw 0, 14, 13, 12, 11 with Balls = 4 (lines 282-285)",
	14: "bsTrough.InitSw 0, 14, 13, 12, 11 (lines 282-285): 14 is the exit position the trough up-kicker empties, held at 1 while a ball waits there",
	15: "never written: solTrough pulses switch 22 instead (line 86), a table defect that drops the stacking-opto edge and pulses Center Lock 1 on every trough kick",
	16: "the cvpmImpulseP plungerIM on trigger swplunger owns 16 (.Switch 16, lines 322-329). Its Start-key lines that write 16 (310, 316) are unreachable, because KeyDownHandler/KeyUpHandler (lines 308, 314) return True for the Start key after sega.vbs writes 54; the pinned v1.22 script writes 16 on the Start key before it calls the handler (lines 496, 554), a defect of that version only",
	17: "Kicker sw17 feeds the cvpmBallStack bsRScoop saucer on 17 (lines 292-295, 335)",
	18: "Gate sw18's Hit handler pulses 18 (line 367)",
	19: "Trigger sw19 holds 19 while the ball sits on it (lines 342-343)",
	20: "Trigger sw20 holds 20 while the ball sits on it (lines 344-345)",
	21: "Wall sw21's Hit handler pulses 21 (line 354); the wall drops while the safe door is open",
	22: "Trigger sw22 holds 22 while the ball sits on it (lines 360-361); solTrough also pulses 22 on every trough kick (line 86), a table defect",
	23: "Trigger sw23 holds 23 while the ball sits on it (lines 362-363)",
	24: "Wall sw24's Hit handler pulses 24 (line 356); the wall drops while the safe door is open",
	25: "Spinner sw25's Spin handler pulses 25 (line 372): the table models the right-ramp switch as a spinner; the pinned v1.22 script rebinds it to a Hit handler (line 617)",
	26: "dtSingle.InitDrop sw26, 26 (line 298); the cvpmDropTarget holds 26 while the target is down",
	27: "Spinner sw27's Spin handler pulses 27 (line 373)",
	28: "Kicker sw28 feeds the cvpmBallStack bsTEject saucer on 28 (lines 287-290, 336)",
	29: "Gate sw29's Hit handler pulses 29 (line 368)",
	31: "Trigger sw31 holds 31 while the ball sits on it (lines 348-349)",
	32: "Trigger sw32 holds 32 while the ball sits on it (lines 350-351)",
	33: "Gate sw33's Hit handler pulses 33 (line 369)",
	34: "HitTarget sw34's Hit handler pulses 34 (line 392)",
	35: "HitTarget sw35's Hit handler pulses 35 (line 393)",
	36: "HitTarget sw36's Hit handler pulses 36 (line 394)",
	37: "HitTarget sw37's Hit handler pulses 37 (line 395)",
	38: "Trigger sw38 holds 38 while the ball sits on it (lines 376-377)",
	39: "Trigger sw39 holds 39 while the ball sits on it (lines 378-379)",
	40: "Trigger sw40 holds 40 while the ball sits on it (lines 380-381)",
	49: "Bumper1's Hit handler pulses 49 (line 398)",
	50: "Bumper2's Hit handler pulses 50 (line 399)",
	51: "Bumper3's Hit handler pulses 51 (line 400)",
	57: "Trigger sw57 holds 57 while the ball sits on it (lines 382-383)",
	58: "Trigger sw58 holds 58 while the ball sits on it (lines 384-385)",
	59: "LeftSlingShot_Slingshot pulses 59 (line 746)",
	60: "Trigger sw60 holds 60 while the ball sits on it (lines 386-387)",
	61: "Trigger sw61 holds 61 while the ball sits on it (lines 388-389)",
	62: "RightSlingShot_Slingshot pulses 62 (line 728)",
}
# Matrix switches the gameplay harness run closed, with the coil the ROM fired in response (step labels in the evidence).
GAMEPLAY_RESPONSE = {
	9: "closing it once in a game fired the Bada Bing! motor relay (18), raised the Bing lock post (23 on) and lit the back flash (26)",
	25: "closing it once released the Bing lock post (23 off) and the back flash (26 off)",
	17: "holding it fired the left eject (21) repeatedly with the fish jaw (17) and the left-sling flasher (27)",
	21: "closing it once fired the safe coil (8) and the safe latch (30) and blinked the GI",
	24: "closing it once fired the safe coil (8) twice and the safe latch (30) and blinked the GI",
	28: "holding it fired the center eject (3) repeatedly with the bumper flashers (29)",
	49: "closing it once fired the left bumper (9) and the bumper flashers (29)",
	50: "closing it once fired the right bumper (10), the bumper flashers (29) and the fish jaw (17)",
	51: "closing it once fired the bottom bumper (11) and the bumper flashers (29)",
	59: "closing it once fired the left slingshot (12)",
	62: "closing it once fired the right slingshot (13)",
}
GAMEPLAY_QUIET = (18, 26, 27, 29, 33, 34, 35, 36, 37, 38, 39, 40, 57, 58, 60, 61)


def switch_id(address: int) -> str:
	if address in SWITCHES:
		return f"switch.{address}-{slug(SWITCHES[address][0])}"
	return f"switch.{address}-not-used"


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


def _callout_seed() -> dict[str, Any]:
	return load_json(CALLOUT_SEED_PATH)


def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Observed spatial record for one device from the committed placement seed, or None."""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
		})
	return {"status": "observed", "placements": placements}


def measured_placements(identifier: str, role: str) -> dict[str, Any] | None:
	"""Candidate placements measured on a factory drawing through its control fit, or None."""
	seed = _callout_seed()
	ids = sorted(pid for pid, item in seed["measurements"].items() if item["device"] == identifier)
	if not ids:
		return None
	placements = []
	for pid in ids:
		x, y = drawing_callouts.measured(seed, pid)
		placements.append({"id": pid, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance("candidate", MANUAL_SOURCE, CALLOUT_SOURCE)})
	return {"status": "candidate", "placements": placements}


def _placement_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	parts = []
	for entry in entries:
		text = f"{entry['type']} {entry['object']}"
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		if entry.get("note"):
			text += f" ({entry['note']})"
		parts.append(text)
	return f" Placement from the retained table's {', '.join(parts)}." if parts else ""


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(status, *refs),
	}
	device.update({key: value for key, value in extra.items() if value is not None})
	return device


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	drive_wire, drive_connection = MATRIX_DRIVE[column]
	return_wire, return_connection, receiver = MATRIX_RETURN[row]
	return {
		"board": "Whitestar CPU/Sound board switch matrix", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "return_component": f"column drive Q{column + 1}; row receiver {receiver}",
	}


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) prints this cell NOT USED with no part number, the location drawing marks no switch "
			"with this number, and neither retained script writes it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, mounting, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}", part):
		physical["assembly_part_number" if part.startswith("500-") else "part_number"] = part
	notes += f' The grid prints "{printed}", mounting class "{mounting}", part cell "{part}".'
	if address in SWITCH_PART_DESCRIPTIONS:
		notes += f" The playfield switch parts page lists it as {SWITCH_PART_DESCRIPTIONS[address]}."
	if address in (17, 28):
		notes += " That page prints the eject item's matrix numbers as '17 & 18'; the grid and the same page's wire-gate item (18, 25 & 33) put 18 on the left orbit, so the eject pair is 17 and 28."
	if address in (59, 62):
		physical["quantity"] = 2
		notes += " Two parallel blade contacts share this matrix address."
	if address in (14, 15):
		notes += (
			" The grid's Sw. 14 & 15 note: 'Transmitter & Receiver OPTO PC Boards are used as Switches' (515-0173-00 transmitter, "
			"515-0174-00 receiver), mounted at the trough up-kicker. Whitestar's switch_r hands the CPU ~core_getSwCol and the driver's "
			"invSw is zero, so public 1 is the CPU's closed-contact reading. The Trough Up-Kicker Dual OPTO Boards theory of operation "
			"(PDF 132) states the construction: with light on the receiver its output transistor is off and acts as an open switch; when "
			"the beam is blocked it conducts and acts as a closed switch."
		)
		refs += (RUNTIME_SOURCE,)
	if address == 14:
		notes += " The retained script holds 14 at 1 while a ball waits at the up-kicker, so the receiver's matrix contact closes while a ball blocks the beam and rests open."
	if address == 15:
		notes += (
			" Neither retained script writes 15. The ROM settles its sense: with four balls held on 11-14, raising 15 to 1 in attract mode, "
			"or holding it at 1 from power-up, makes the ROM fire the trough up-kicker (1) six times and then the auto launch (2); 15 at 0 at "
			"boot and a fall back to 0 draw no coil. The ROM reads 1 as a ball in the stacking beam, so the contact rests open."
		)
	if address in (3, 7):
		notes += " The cell reads Future Use: the harness position is wired but no coin switch is fitted by default."
	if address == 2:
		notes += " The cabinet wiring diagram (PDF 131) labels this input '4th Coin Slot European Use'."
	if address in (1, 8):
		notes += (
			" UK only: the cabinet wiring diagram's note says the two extra cabinet buttons serve the Post Save feature (the left button "
			"raises the left outlane ball deflector, the right button the right one, both together the center up/down post); they sit "
			"under the flipper buttons."
		)
	if address == 53:
		notes += " The cell carries a KIT tag and the drawing says 'Optional Slam Tilt Kit Required'; its part cell is cut off after '180-'."
	if address == 55:
		notes += " The cell carries a KIT tag and the drawing says 'Optional Tournament Kit Required'."
	if address in (53, 55):
		notes += (
			" sega.vbs (swSlamTilt = 55) and PinMAME's Whitestar keyboard port both put the slam-tilt key on 55, generic Whitestar numbering "
			"that on this game lands on Tournament Start; the optional slam tilt is wired to 53, which no key writes."
		)
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 56:
		notes += " Sw. 56 note: hanger bracket 535-5319-00 and contact wire 535-7563-01 in the cabinet."
	if address == 54:
		notes += " sega.vbs's swStartButton = 54 is what the VPinMAME Start key writes."
	if address in (4, 5, 6):
		notes += f" sega.vbs maps its coin keys to {'swCoin3 = 4' if address == 4 else 'swCoin1 = 5' if address == 5 else 'swCoin2 = 6'}."
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
		if address in (16, 25):
			refs += (VPX_CORPUS_SOURCE, VPM_LIBRARY_SOURCE) if address == 16 else (VPX_CORPUS_SOURCE,)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the gameplay harness run, {GAMEPLAY_RESPONSE[address]}."
		refs += (RUNTIME_SOURCE,)
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay harness run closed it once in a game and the ROM fired no coil in response, which says nothing against its fitment."
		refs += (RUNTIME_SOURCE,)
	if address == 5:
		notes += " In the gameplay run each coin on 5 pulsed the optional coin-meter output 24 four times."
		refs += (RUNTIME_SOURCE,)
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": False, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (11, 12, 13, 14):
		extra["initial_active"] = True
	if any(role.startswith("cabinet.") for role in roles):
		physical["location"] = "coin door" if mounting == "Coin Door" else "cabinet"
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE,)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, physical=physical, **extra)


# address -> (label, printed name, wire, connector, mounting, part, roles, availability, normally_closed)
DEDICATED = {
	-3: ("Coin Door Memory Protect", "Memory Protect Switch", "BLK-RED", "CN6-P12", "coin door", None, ("cabinet.memory-protect",), "used", False),
	-2: ("Volume / Service Left (Red)", "#6 VOLUME (RED BUTTON) (In Test: LEFT)", "GRY-BLU", "CN6-P8", "coin door", "180-5192-02", ("service.left",), "used", False),
	-1: ("Service Credit / Service Right (Green)", "#7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT)", "GRY-VIO", "CN6-P9", "coin door", "180-5192-04", ("service.right",), "used", False),
	0: ("Begin Test / Service Enter (Black)", "#8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER)", "GRY-BLK", "CN6-P10", "coin door", "180-5192-00", ("service.enter",), "used", False),
	81: ("Right Flipper End-of-Stroke", "#4 RIGHT FLIPPER E.O.S. (End-of-Stroke)", "GRY-YEL", "CN6-P6", "playfield", "180-5149-00", ("flipper.lower.right.eos",), "used", True),
	82: ("Right Flipper Button", "#3 RIGHT FLIPPER BUTTON", "GRY-ORG", "CN6-P4", "cabinet", "180-5160-00", ("flipper.lower.right.button",), "used", False),
	83: ("Left Flipper End-of-Stroke", "#2 LEFT FLIPPER E.O.S (End-of-Stroke)", "GRY-RED", "CN6-P3", "playfield", "180-5149-00", ("flipper.lower.left.eos",), "used", True),
	84: ("Left Flipper Button", "#1 LEFT FLIPPER BUTTON", "GRY-BRN", "CN6-P2", "cabinet", "180-5160-00", ("flipper.lower.left.button",), "used", False),
}
DEDICATED_INPUT = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1"}


def _dedicated(address: int) -> dict[str, Any]:
	label, printed, wire, connector, location, part, roles, availability, normally_closed = DEDICATED[address]
	name = f"n{-address}" if address < 0 else str(address)
	identifier = f"switch.{name}-{slug(label)}"
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
	if address in DEDICATED_INPUT:
		aliases.append({"namespace": "manual.address", "value": DEDICATED_INPUT[address]})
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": "leaf" if address in (81, 83) else "button" if address != -3 else "microswitch", "location": location}
	if part:
		physical["part_number"] = part
	if address == -3:
		notes = (
			"The cabinet/coin door wiring diagram (PDF 131) draws the Memory Protect Switch as an N.O. switch from CPU/Sound board CN6 pin 12 (BLK-RED) to ground; the fuse chart page puts it inside the coin door as the bottom switch. se.c's ram_w "
			"refuses writes to 0x1E00-0x1FFF while public -3 is 1, and the manual's troubleshooting table says the memory protect switch "
			"is enabled while the coin door is closed, so a closed door is public -3 at 1 and an open door 0."
		)
		extra: dict[str, Any] = {"initial_active": True, "wiring": {"board": "Whitestar CPU/Sound board memory-protect input", "drive_wire": wire, "drive_connection": connector}}
	else:
		notes = (
			f"Printed dedicated switch {DEDICATED_INPUT[address]} ({printed}), wired {wire} to {connector} on IC U206's inputs and returned "
			"to ground (BLK, CN6-P1/-P11). se.c's dedswitch_r swaps PinMAME's flipper column into U206's order and returns the complement, "
			"so public 1 is a closed contact."
		)
		extra = {"wiring": {"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": wire, "drive_connection": connector, "return_wire": "BLK", "return_connection": "CN6-P1/-P11", "return_component": "U206"}}
	if address in (81, 83):
		notes += (
			" The 2-Flipper Circuit Wiring Diagram (PDF 129) prints the E.O.S. as an N.C. switch on the flipper assembly and explains "
			"that it opens about 1/16\" when the flipper is energized; the CPU re-pulses the coil (40 ms) when it sees the switch close "
			"again during a hold, because a shot forced the bat back. normally_closed is that construction: at rest the contact is closed "
			"(public 1) and it opens (public 0) at the end of the stroke. The driver declares FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L) without "
			"FLIP_EOS, so core_updateSw never writes this bit and the ROM reads whatever the host writes; a recreation that leaves it at 0 "
			"only loses the re-pulse. Neither retained script writes it; sega.vbs names this address swURFlip/swULFlip, an upper-flipper "
			"label it writes only when an upper flipper solenoid is registered, which this table does not do."
		)
		refs += (VPM_LIBRARY_SOURCE,)
		flipper_entries = _spatial_seed()["switch"].get(str(address))
		spatial = located("switch", address, identifier, "sensor") if flipper_entries else None
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	elif address in (82, 84):
		notes += (
			f" The flipper column bit PinMAME's core_updateSw copies into the lower-flipper outputs; sega.vbs writes it from the "
			f"{'right' if address == 82 else 'left'} flipper key (swLRFlip = 82, swLLFlip = 84). In the gameplay harness run, holding it "
			f"made the ROM pulse {'45 and 46' if address == 82 else '47 and 48'}."
		)
		refs += (VPM_LIBRARY_SOURCE, RUNTIME_SOURCE)
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, aliases=aliases, normally_closed=normally_closed,
		pulse=False, roles=list(roles), physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items = [_dedicated(address) for address in (-3, -2, -1, 0)]
	items.extend(_matrix_switch(address) for address in range(1, 65))
	items.extend(_dedicated(address) for address in (81, 82, 83, 84))
	for address in (85, 86, 87):
		items.append(_device(
			f"switch.{address}-flipper-column-hole", f"Unused Flipper-Column Input {address}", "switch", SWITCH_GROUP, address, "unused",
			(CORE_SOURCE, CONTROLLER_SOURCE), aliases=[{"namespace": "pinmame.switch", "value": str(address)}], normally_closed=False, pulse=False,
			physical={"notes": "dedswitch_r reads only the flipper column's four low bits and its top bit (public 81-84 and 88); this bit reaches no input of U206."},
			spatial=not_applicable("unused", CORE_SOURCE),
		))
	items.append(_device(
		"switch.88-not-used-ds-5", "Not Used Dedicated Input DS-5", "switch", SWITCH_GROUP, 88, "unused", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.switch", "value": "88"}, {"namespace": "manual.address", "value": "DS-5"}], normally_closed=False, pulse=False,
		physical={"notes": "dedswitch_r routes the flipper column's upper-flipper button bit to U206 input 5 (DS-5), which the dedicated-switch column prints NOT USED (GRY-GRN, CN6-P7). The driver declares no upper flipper."},
		wiring={"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": "GRY-GRN", "drive_connection": "CN6-P7", "return_component": "U206"},
		spatial=not_applicable("unused", MANUAL_SOURCE),
	))
	for number in range(1, 9):
		used = number <= 5
		items.append(_device(
			f"switch.dip-{number}", f"SW300 Country Selector Bit {number}" if used else f"Unused DIP Bit {number}", "dip_switch", DIP_GROUP, number,
			"used" if used else "unused", (CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(number)}],
			physical={"switch_type": "dip", "location": "Whitestar CPU/Sound board", "notes": (
				"se.c's dip_r returns the complement of PinMAME DIP bank 0; sega.vbs's DIP form sets the country code in mask 0x0f (USA 0x00, "
				"UK 0x05, Germany 0x07 and so on)." if used else "Above the bits the country selector uses; nothing reads it.")},
			spatial=not_applicable("dip_switch", CORE_SOURCE),
		))
	return items


# --- Solenoid data -------------------------------------------------------------------------------------
# Q number -> (label, printed name, kind, availability, part/bulb cell, power wire, power connection, voltage, control wire, control connection)
Q_OUTPUTS: dict[int, tuple[str, str, str, str, str, str, str, int, str, str]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00T", "YEL-VIO", "J10-P4/5", 50, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "23-800 / 090-5001-00B", "YEL-VIO", "J10-P4/5", 50, "BRN-RED", "J8-P3"),
	3: ("Center Eject", "CENTER EJECT", "coil", "used", "26-1200 / 090-5044-00B", "YEL-VIO", "J10-P4/5", 50, "BRN-ORG", "J8-P4"),
	4: ("Center Lock Post", "CENTER LOCK POST", "coil", "used", "27-1500 / 090-5004-00T", "YEL-VIO", "J10-P4/5", 50, "BRN-YEL", "J8-P5"),
	5: ("Left Control Gate", "LEFT CONTROL GATE", "coil", "used", "32-1800 / 515-6543-00", "YEL-VIO", "J10-P4/5", 50, "BRN-GRN", "J8-P6"),
	6: ("Right Control Gate", "RIGHT CONTROL GATE", "coil", "used", "32-1800 / (090-5031-00)", "YEL-VIO", "J10-P4/5", 50, "BRN-BLU", "J8-P7"),
	7: ("1-Bank Trip", "1 BANK TRIP", "coil", "used", "32-1250 / 515-6916-01", "YEL-VIO", "J10-P4/5", 50, "BRN-VIO", "J8-P8"),
	8: ("Safe", "SAFE", "coil", "used", "22-1080 / 090-5032-00T", "VIO-YEL", "J10-P3", 50, "BRN-GRY", "J8-P9"),
	9: ("Left Bumper", "LEFT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", "YEL-VIO", "J10-P4/5", 50, "BLU-BRN", "J9-P1"),
	10: ("Right Bumper", "RIGHT BUMPER", "coil", "used", "26-1200 / 090-5044-00T", "YEL-VIO", "J10-P4/5", 50, "BLU-RED", "J9-P2"),
	11: ("Bottom Bumper", "BOTTOM BUMPER", "coil", "used", "26-1200 / 090-5044-00B", "YEL-VIO", "J10-P4/5", 50, "BLU-ORG", "J9-P4"),
	12: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "26-1200 / 090-5044-00T", "YEL-VIO", "J10-P4/5", 50, "BLU-YEL", "J9-P5"),
	13: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "26-1200 / 090-5044-00T", "YEL-VIO", "J10-P4/5", 50, "BLU-GRN", "J9-P6"),
	14: ("1-Bank Reset", "1 BANK RESET", "coil", "used", "27-1500 / 090-5004-00B", "YEL-VIO", "J10-P1/2", 50, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "22-1080 / 090-5032-00T", "GRY-YEL~3A Fuse~RED-YEL", "J10-P1/2", 50, "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "22-1080 / 090-5032-00T", "BLU-YEL~3A Fuse~RED-YEL", "J10-P1/2", 50, "ORG-VIO", "J9-P9"),
	17: ("Fish Jaw", "FISH JAW", "coil", "used", "27-1500 / 090-5004-00B", "BROWN", "J7-P1", 20, "VIO-BRN", "J7-P2"),
	18: ("Bada Bing! Motor Relay", "BING MOTOR (RELAY)", "relay", "used", "Relay Asm / 500-6700-00", "BROWN", "J7-P1", 20, "VIO-RED", "J7-P3"),
	19: ("Super Jackpot Flasher", "FLASH: SUPER JP", "flasher", "used", "#89 Bulb / 165-5000-89-HF", "ORANGE", "J6-P10", 20, "VIO-ORG", "J7-P4"),
	20: ("Safe Flasher", "FLASH: SAFE", "flasher", "used", "#89 Bulb / 165-5000-89-HF", "ORANGE", "J6-P10", 20, "VIO-YEL", "J7-P6"),
	21: ("Left Eject", "LEFT EJECT", "coil", "used", "26-1200 / 090-5044-00B", "BROWN", "J7-P1", 20, "VIO-GRN", "J7-P7"),
	22: ("Boat Lock Post", "BOAT LOCK POST", "coil", "used", "26-1200 / 090-5044-00T", "BROWN", "J7-P1", 20, "VIO-BLU", "J7-P8"),
	23: ("Bing Lock Post", "BING LOCK POST", "coil", "used", "26-1200 / 090-5044-00T", "BROWN", "J7-P1", 20, "VIO-BLK", "J7-P9"),
	24: ("Optional Coil (Coin Meter)", "OPTIONAL COIL", "coil", "optional", "Opt. 5v", "RED", "J16-P7", 5, "VIO-GRY", "J7-P10"),
	25: ("Fish Flasher", "FLASH: FISH", "flasher", "used", "#44 LED / 112-5023-08", "ORANGE", "J6-P10", 20, "BLK-BRN", "J6-P1"),
	26: ("Back Flashers (X3)", "FLASH: BACK X3", "flasher", "used", "#89 #906 / X2 & X1", "ORANGE", "J6-P10", 20, "BLK-RED", "J6-P2"),
	27: ("Left Sling Flasher", "FLASH: LEFT SLING", "flasher", "used", "#906 Bulb / 165-5004-00", "ORANGE", "J6-P10", 20, "BLK-ORG", "J6-P3"),
	28: ("Right Sling Flasher", "FLASH: RIGHT SLING", "flasher", "used", "#906 Bulb / 165-5004-00", "ORANGE", "J6-P10", 20, "BLK-YEL", "J6-P4"),
	29: ("Bumper Flashers (X2)", "FLASH: BUMPERS X2", "flasher", "used", "#906 Bulb / 165-5004-00", "ORANGE", "J6-P10", 20, "BLK-GRN", "J6-P5"),
	30: ("Safe Latch", "SAFE LATCH", "coil", "used", "27-1500 / 090-5004-00B", "BROWN", "J7-P1", 20, "BLK-BLU", "J6-P6"),
	31: ("Playfield Left and Right Flashers (X2)", "FLASH: PF LT & RT X2", "flasher", "used", "#89 Bulb / 165-5000-89-HF", "ORANGE", "J6-P10", 20, "BLK-VIO", "J6-P7"),
	32: ("Truck Flashers (X2)", "FLASH: TRUCK X2", "flasher", "used", "#89 Bulb / 165-5000-89-HF", "ORANGE", "J6-P10", 20, "BLK-GRY", "J6-P8"),
}
PUBLIC_BINDING = {15: 48, 16: 46}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"solTrough\": bsTrough.ExitSol_On (lines 34, 83-88)",
	2: "SolCallback(2) = \"solAutofire\": PlungerIM.AutoFire on the shooter-lane impulse plunger (lines 35, 90-94)",
	3: "SolCallback(3) = \"bsTEject.SolOut\": ejects the center-eject saucer on 28 (line 36)",
	4: "SolCallback(4) = \"SolCenterLock\": drops wall CenterPost and lowers primitive CenterPin while energized (lines 37, 96-105)",
	5: "SolCallBack(5) = \"SolGateL\": opens gate sol5 while energized (lines 38, 107-114)",
	6: "SolCallBack(6) = \"SolGateR\": opens gate sol6 while energized (lines 39, 116-123)",
	7: "SolCallback(7) = \"dtSingle.SolHit 1,\": knocks the drop target down (line 40)",
	8: "SolCallback(8) = \"SolSafe\": with Q8 energized it starts the door animation closing (walls sw21/sw24 restored, switch 10 cleared at the end); with Q8 released it starts it opening (primitives sw21p/sw24p raised, walls dropped, switch 10 set at the end). While the Safe Latch has set Latch, any Q8 change only selects the closing state and exits without starting the animation, so an idle door does not move (lines 41, 175-231)",
	9: "Bumper1 is a VPX bumper that fires itself; no callback",
	10: "Bumper2 is a VPX bumper that fires itself; no callback",
	11: "Bumper3 is a VPX bumper that fires itself; no callback",
	12: "LeftSlingShot is a VPX slingshot wall that fires itself; no callback",
	13: "RightSlingShot is a VPX slingshot wall that fires itself; no callback",
	14: "SolCallback(14) = \"dtSingle.SolDropUp\": raises the drop target (line 42)",
	17: "SolCallback(17) = \"SolFish\": rotates the invisible helper flipper fishf (the fishmouth jaw primitive follows it) to its end while energized (lines 43, 125-132)",
	18: "SolCallback(18) = \"Strippers\": runs strippert_Timer, spinning primitives stripper1/stripper2, while energized (lines 44, 156-169)",
	19: "SolCallback(19) = \"SetLamp 119,\": light L119 (lines 50, 534)",
	20: "SolCallback(20) = \"SetLamp 120,\": light L120 (lines 51, 536)",
	21: "SolCallBack(21) = \"bsRScoop.SolOut\": ejects the left-eject saucer on 17 (line 45)",
	22: "SolCallback(22) = \"SolBoatLock\": drops wall BoatPost and moves primitive BoatPin while energized (lines 46, 134-143)",
	23: "SolCallback(23) = \"SolBingLock\": drops wall BingPost while energized (lines 47, 145-152)",
	25: "SolCallback(25) = \"SetLamp 125,\": Flasher sprites f125a/f125b at the fish eyes (lines 52, 538-539)",
	26: "SolCallback(26) = \"SetLamp 126,\": dome primitive P126 and light L126 (lines 53, 541-542)",
	27: "SolCallback(27) = \"SetLamp 127,\": dome primitive P127 and light f127 (lines 54, 544-545)",
	28: "SolCallback(28) = \"SetLamp 128,\": dome primitive P128 and light f128 (lines 55, 547-548)",
	29: "SolCallback(29) = \"SetLamp 129,\": dome primitives P129a/P129b and lights l29a/l29b (lines 56, 550-553)",
	30: "SolCallback(30) = \"SolSafeLatch\": only sets or clears Latch (lines 48, 190-196); while it is set, SolSafe turns a Q8 change into the closing state without starting the door animation",
	31: "SolCallback(31) = \"SetLamp 131,\": one light L131 (lines 57, 555)",
	32: "SolCallback(32) = \"SetLamp 132,\": lights L32a/L32b (lines 58, 557-558)",
}
# What the gameplay harness run showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: "the ROM fired it on Start and at the drain",
	2: "the stacking-opto runs fired it once after each burst of trough kicks",
	3: "a ball held in the center eject (28) made the ROM fire it repeatedly",
	7: "it fired at the drain, with the 1-bank reset (14)",
	8: "it fired at power-up and from each safe hit (21, 24), each time with the safe latch (30)",
	9: "it answered the left bumper switch (49)",
	10: "it answered the right bumper switch (50)",
	11: "it answered the bottom bumper switch (51)",
	12: "it answered the left slingshot switch (59)",
	13: "it answered the right slingshot switch (62)",
	14: "it fired at power-up, on Start and at the drain",
	17: "it fired from the right bumper (50) and while a ball sat in the left eject (17)",
	18: "it pulsed on Start and from the left ramp switch (9)",
	21: "a ball held in the left eject (17) made the ROM fire it repeatedly",
	23: "the left ramp switch (9) raised it and the right ramp switch (25) released it",
	24: "each coin on the center slot (5) pulsed it four times, the coin-meter count",
	25: "it switched on at Start and off at the drain",
	26: "it pulsed on Start and switched on from the left ramp (9) and off from the right ramp (25)",
	27: "it flashed while a ball sat in the left eject (17)",
	29: "it flashed with every bumper and the center eject",
	30: "it fired at power-up and with each safe hit, with the safe coil (8)",
}
FLASHER_LOCATIONS = {
	19: "super jackpot", 20: "safe", 25: "inside the fish head (fish eyes)", 26: "two #89 on the back panel and one #906 yellow dome at the stage",
	27: "yellow dome over the left slingshot", 28: "yellow dome over the right slingshot", 29: "two red domes at the bumpers",
	31: "one at each side of the playfield", 32: "two at the truck",
}
FLASHER_QUANTITY = {26: 3, 29: 2, 31: 2, 32: 2}


def q_output_id(number: int) -> str:
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def _q_wiring(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire,
		"control_connection": control_connection, "power_wire": power_wire, "power_connection": power_connection,
		"nominal_voltage_v": voltage, "voltage_type": "dc",
	}


def _q_output(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	address = PUBLIC_BINDING.get(number, number)
	identifier = q_output_id(number)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {}
	coil_part = part.split(" / ")[-1]
	if re.fullmatch(r"\d{3}-\d{4}-\d{2}[A-Z-]*", coil_part):
		physical["part_number" if not coil_part.startswith("500-") else "assembly_part_number"] = coil_part
	notes = f'Coils Detailed Chart Table (DR. 6) row #{number} "{printed}": drive transistor Q{number}, cell "{part}".'
	if number in FLASHER_LOCATIONS:
		physical["location"] = FLASHER_LOCATIONS[number]
	if number in FLASHER_QUANTITY:
		physical["quantity"] = FLASHER_QUANTITY[number]
	if number == 26:
		notes += " The location drawing (DR. 7) marks two 26 bulbs on the back panel's front view and one yellow-domed 26 at the stage on the playfield; only the playfield bulb is placed."
	if number == 31:
		notes += " The location drawing marks one 31 on each side of the playfield; the retained table models only the right one (L131, its 'right spotlight')."
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} flipper "
			f"power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public {address}, the retained "
			f"table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase state, not a second coil. The "
			"2-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, then 1 ms every 12 ms while held."
		)
		refs += (VPX_SCRIPT_SOURCE, RUNTIME_SOURCE)
	if number == 18:
		notes += (
			" The relay switches the Bada Bing! motor (Bada Bing! parts page, PDF 115: Motor Assembly 500-6887-00, 24v AC 4W 45.7/54.9 RPM "
			"bi-directional, turning two pole-dancer dolls through pulleys and a belt; the motor's 2-pin connector goes 'to Relay')."
		)
	if number == 24:
		notes += (
			" The location drawing's note: 'Coil Q24 is Optional. If either a Coin Meter, Token Dispenser or Knocker (all optional "
			"equipment) is required, call Technical Support'. The cabinet wiring diagram routes Q24 (J7-10 VIO-GRY, +5V DC J16-7 RED) 'TO COIN "
			"METER'. No stock playfield device is fitted and neither retained script registers a callback."
		)
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
		refs += (RUNTIME_SOURCE,)
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}], "wiring": _q_wiring(number)}
	role = "emitter" if kind == "flasher" else "effect"
	if number == 24:
		extra["roles"] = ["cabinet.coin-meter"]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = "cabinet (coin meter, when fitted)"
	else:
		spatial = located("solenoid", address, identifier, role)
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("solenoid", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	physical["notes"] = notes
	return _device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, physical=physical, **extra)


AUX_OUTPUTS = {
	33: ("UK Left Up/Down Post (Left Outlane Ball Deflector)", "AUX 1: LEFT UP/DOWN POST", "26-1200 / 090-5044-00T", "WHITE", "J2-P3"),
	34: ("UK Center Up/Down Post", "AUX 2: CENTER UP/DOWN POST", "23-1100 / 090-5030-00T", "RED", "J2-P4"),
	35: ("UK Right Up/Down Post (Right Outlane Ball Deflector)", "AUX 3: RIGHT UP/DOWN POST", "26-1200 / 090-5044-00T", "ORANGE", "J2-P7"),
}


def solenoid_outputs() -> list[dict[str, Any]]:
	items = [_q_output(number) for number in Q_OUTPUTS]
	items.append(_device(
		"virtual.15-fast-flip-game-on", "Whitestar Fast-Flip / Game-On State", "virtual", SOLENOID_GROUP, 15, "used", (CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}],
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; MACHINE_INIT(se3), "
			"which every sopranos set's de_mSES3 machine driver uses, places that byte at CPU address 0x04. sega.vbs declares GameOnSolenoid = 15. In the gameplay run it rose on Start "
			"and fell at the drain. Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
		)},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.16-remapped-flipper-hole", "Unused Remapped-Flipper Address 16", "virtual", SOLENOID_GROUP, 16, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "16"}],
		physical={"notes": "se_solenoid_w masks physical Q16 off public 16 and publishes it at 45/46; nothing else drives 16."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	for index, (address, (label, printed, part, control_wire, control_connection)) in enumerate(AUX_OUTPUTS.items(), start=1):
		identifier = f"device.aux{index}-{slug(label)}"
		notes = (
			f'Coils Detailed Chart Table row "{printed}" under "Auxiliary (UK ONLY)": UK 3X Trans. Driver Board transistor Q{index}, cell "{part}". '
			"segames.c gives the driver SE_BOARDID_520_5068_01, whose ESTB strobe se.c latches into public 33-35. The cabinet wiring "
			"diagram's UK note: the left and right extra cabinet buttons (matrix 1 and 8) raise the left and right outlane ball deflectors and "
			"both together the center up/down post (the Post Save feature); the UK-only parts pages list Ball Deflector Assemblies 500-5788-02 "
			"(Qty. 2) and Up/Down Post Assembly 500-6293-00. A standard machine fits none of the three, and the retained US table models none."
		)
		spatial = measured_placements(identifier, "effect")
		if spatial:
			notes += " Placement measured on the coil location drawing (DR. 7), which draws the AUX boxes on the playfield; a drawing measurement is a candidate."
		items.append(_device(
			identifier, label, "coil", SOLENOID_GROUP, address, "optional", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE) + ((CALLOUT_SOURCE,) if spatial else ()),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"AUX {index}"}],
			physical={"part_number": part.split(" / ")[-1], "location": label, "notes": notes},
			wiring={"board": "UK 3X Trans. Driver Board", "driver_transistor": f"Q{index}", "power_wire": "BROWN", "power_connection": "J7-P1", "control_wire": control_wire, "control_connection": control_connection, "nominal_voltage_v": 20, "voltage_type": "dc"},
			spatial=spatial,
		))
	items.append(_device(
		"virtual.36-aux-hole", "Unused Auxiliary Address 36", "virtual", SOLENOID_GROUP, 36, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "36"}],
		physical={"notes": "Board 520-5068-01 latches three outputs (33-35); se.c never writes 36 for this driver."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	for address in range(37, 45):
		items.append(_device(
			f"virtual.{address}-reserved", f"Reserved Address {address}", "virtual", SOLENOID_GROUP, address, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": "A Whitestar compatibility hole: nothing in se.c drives it for this driver."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE, RUNTIME_SOURCE), aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": (
				f"se_solenoid_w publishes physical Q{number}'s drive here and core.c synthesizes canonical {canonical} from it; one {side} flipper coil "
				f"is bound at {canonical}. In the gameplay run, holding the {side} flipper button pulsed {address} and {canonical} together."
			)},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	items.append(_device(
		"virtual.49-simulated-shooter", "Unused Simulated Ball Shooter", "virtual", SOLENOID_GROUP, 49, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "49"}],
		physical={"notes": "PinMAME's reserved simulation output; the machine's auto launch is Q2 at public 2."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.50-reserved", "Reserved Address 50", "virtual", SOLENOID_GROUP, 50, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "50"}],
		physical={"notes": "The last address below PinMAME's custom-solenoid boundary (custSol is 0 for this driver); nothing drives it."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	return sorted(items, key=lambda item: item["binding"]["device"])


# --- Lamps ---------------------------------------------------------------------------------------------
# address -> (label, bulb cell)
LAMPS: dict[int, tuple[str, str]] = {
	1: ("Ranks: Associate", "#555 Clear Bulb"), 2: ("Ranks: Soldier", "#555 Clear Bulb"), 3: ("Ranks: Good Earner", "#555 Clear Bulb"),
	4: ("Ranks: Acting Capo", "#555 Clear Bulb"), 5: ("Ranks: Capo", "#555 Clear Bulb"), 6: ("Ranks: Consigliere", "#555 Clear Bulb"),
	7: ("Ranks: Under Boss", "#555 Clear Bulb"), 8: ("Ranks: Boss", "#44 Clear Bulb"),
	9: ("Boss: Food", "#44 Clear Bulb"), 10: ("Boss: Truck Heist", "#44 Clear Bulb"), 11: ("Boss: Bada Bing", "#44 Clear Bulb"),
	12: ("Boss: Episodes", "#44 Clear Bulb"), 13: ("Boss: Safe", "#44 Clear Bulb"), 14: ("Boss: RIP", "#44 Clear Bulb"),
	15: ("Boss: Super Jackpot", "#44 Clear Bulb"), 16: ("Boss: Meadowlands", "#44 Clear Bulb"),
	17: ("FISH 'F' (Left Outlane)", "#555 Clear Bulb"), 18: ("FISH 'I' (Left Return Lane)", "#555 Clear Bulb"),
	19: ("FISH 'S' (Right Return Lane)", "#555 Clear Bulb"), 20: ("FISH 'H' (Right Outlane)", "#555 Clear Bulb"),
	21: ("Pork Store Standup", "#555 Clear Bulb"), 22: ("Light Standup", "#555 Clear Bulb"), 23: ("Fish", "#555 Clear Bulb"),
	24: ("The Stugots", "#44 LED Bulb"),
	25: ("Left Truck Heist 1 (Bottom)", "#555 Clear Bulb"), 26: ("Left Truck Heist 2", "#555 Clear Bulb"), 27: ("Left Truck Heist 3", "#555 Clear Bulb"),
	28: ("Left Orbit Food", "#555 Clear Bulb"), 29: ("Left Orbit Envelope", "#555 Clear Bulb"), 30: ("Left Orbit Arrow", "#555 Clear Bulb"),
	31: ("Bada Bing 1 (Bottom)", "#555 Clear Bulb"), 32: ("Bada Bing 2", "#555 Clear Bulb"), 33: ("Bada Bing 3", "#555 Clear Bulb"),
	34: ("Left Ramp Food", "#555 Clear Bulb"), 35: ("Left Ramp Envelope", "#555 Clear Bulb"), 36: ("Left Ramp Arrow", "#555 Clear Bulb"),
	37: ("Start Episode", "#555 Clear Bulb"), 38: ("Pork Store", "#555 Clear Bulb"), 39: ("Special", "#555 Clear Bulb"), 40: ("Extra Ball", "#555 Clear Bulb"),
	41: ("Advance Rank", "#555 Clear Bulb"), 42: ("Center Arrow", "#555 Clear Bulb"), 43: ("Light Lock", "#555 Clear Bulb"), 44: ("Lock 1", "#555 Clear Bulb"),
	45: ("Lock 2", "#555 Clear Bulb"), 46: ("Jackpot", "#555 Clear Bulb"), 47: ("Meadowlands 1", "#555 Clear Bulb"), 48: ("Meadowlands 2", "#555 Clear Bulb"),
	49: ("Meadowlands 3", "#555 Clear Bulb"), 50: ("Right Ramp Food", "#555 Clear Bulb"), 51: ("Right Ramp Envelope", "#555 Clear Bulb"),
	52: ("Right Ramp Arrow", "#555 Clear Bulb"), 53: ("Right Truck Heist 1 (Bottom)", "#555 Clear Bulb"), 54: ("Right Truck Heist 2", "#555 Clear Bulb"),
	55: ("Right Truck Heist 3", "#555 Clear Bulb"), 56: ("Right Orbit Food", "#555 Clear Bulb"), 57: ("Right Orbit Envelope", "#555 Clear Bulb"),
	58: ("Right Orbit Arrow", "#555 Clear Bulb"), 59: ("R.I.P. 'R' (Left Top Lane)", "#555 Clear Bulb"), 60: ("R.I.P. 'I' (Middle Top Lane)", "#555 Clear Bulb"),
	61: ("R.I.P. 'P' (Right Top Lane)", "#555 Clear Bulb"),
	65: ("RIP 1 (Top Left)", "#44 Clear Bulb"), 66: ("RIP 2", "#44 Clear Bulb"), 67: ("RIP 3", "#44 Clear Bulb"), 68: ("RIP 4", "#44 Clear Bulb"),
	69: ("RIP 5 (Bottom Left)", "#44 Clear Bulb"), 70: ("RIP 6", "#44 Clear Bulb"), 71: ("RIP 7", "#44 Clear Bulb"), 72: ("RIP 8", "#44 Clear Bulb"),
	73: ("Episodes: Arson", "#555 Yel. Bulb"), 74: ("Episodes: Exterminate", "#555 Yel. Bulb"), 75: ("Episodes: Horse Race", "#555 Yel. Bulb"),
	76: ("Episodes: Exec. Game", "#555 Yel. Bulb"), 77: ("Episodes: Satisfaction", "#555 Yel. Bulb"), 78: ("Shoot Again", "#555 Clear Bulb"),
	79: ("Tournament Button (Optional)", "OPTIONAL"), 80: ("Start Button", "#555 Clear Bulb"),
}
UNUSED_LAMPS = (62, 63, 64)
BULB_PART = {"#555 Clear Bulb": "165-5002-00", "#555 Yel. Bulb": "165-5054-06", "#44 Clear Bulb": "165-5000-44"}
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
LAMPS_SEEN = frozenset(list(range(1, 62)) + list(range(65, 79)) + [80])


def lamp_id(address: int) -> str:
	if address in LAMPS:
		return f"lamp.{address}-{slug(LAMPS[address][0])}"
	return f"lamp.{address}-not-used"


def _lamp_wiring(address: int) -> dict[str, Any]:
	row, column = divmod(address - 1, 8)
	drive_wire, drive_connection, driver = LAMP_DRIVE[column]
	return_wire, return_connection = LAMP_RETURN[row]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01 lamp matrix", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "return_component": f"column driver {driver}; row transistor Q{33 + row}",
	}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		identifier = lamp_id(address)
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		notes = f"Printed lamp-matrix row {row + 1}, column {column + 1}."
		if address in UNUSED_LAMPS:
			notes += " The Lamp Matrix Grid (DR. 5) prints this cell NOT USED, the location drawing marks no lamp with this number, and no harness run lit it."
			items.append(_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", (MANUAL_SOURCE, RUNTIME_SOURCE, CONTROLLER_SOURCE),
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE)))
			continue
		label, bulb = LAMPS[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
		physical: dict[str, Any] = {"location": label}
		if bulb in BULB_PART:
			physical["part_number"] = BULB_PART[bulb]
		notes += f' Bulb cell "{bulb}".'
		if address == 24:
			notes += " The grid prints a #44 LED bulb; the lamp-part notes give no LED part number."
		if address in LAMPS_SEEN:
			notes += " The harness runs saw the ROM drive it."
			refs += (RUNTIME_SOURCE,)
		extra: dict[str, Any] = {"aliases": aliases, "wiring": _lamp_wiring(address)}
		availability = "used"
		if 65 <= address <= 72:
			notes += (
				" The grid's note says lamps 65 thru 72 are located on the rear of the Back Panel, and the drawing's back-panel inset puts 65-68 "
				"left to right in its top row and 69-72 in its bottom row, behind the RIP portraits. The back panel stands at the rear of the "
				"playfield, outside normalized playfield space; the retained table renders them only as Flasher sprites off the playfield plane."
			)
			extra["roles"] = ["cabinet.rear-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			physical["location"] = f"back panel ({label})"
		elif address in (79, 80):
			notes += (
				" The cabinet/coin door wiring diagram wires the Start button lamp (80) and the Tournie button lamp (79) to the I/O board's J12/J13 lamp matrix."
			)
			if address == 79:
				notes += " Cell 79 reads OPTIONAL and is shaded as not on the playfield: the lamp exists only with the optional tournament kit, and no run lit it."
				availability = "optional"
				extra["roles"] = ["cabinet.tournament-start"]
			else:
				extra["roles"] = ["cabinet.start"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			physical["location"] = "cabinet (front molding button)"
		elif 73 <= address <= 77:
			notes += (
				" The location drawing ends five separate leaders for 73-77 in the art area left of the bumpers, while the retained table "
				"stacks primitives l73-l77 at one x/y and five heights (its NFadeObjm/Flash calls, lines 516-525), so no table object "
				"gives this lamp's own position."
			)
			refs += (VPX_SCRIPT_SOURCE,)
			spatial = measured_placements(identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
				refs += (CALLOUT_SOURCE,)
				notes += " Placement measured where its leader ends on the lamp location drawing (DR. 5), through that page's control fit; a candidate."
		else:
			spatial = located("lamp", address, identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
				notes += _placement_note("lamp", address)
				refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, availability, refs, physical=physical, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	entries = _spatial_seed()["gi"]["0"]
	placements = [{
		"id": f"gi.relay.emitter.{index}", "role": "emitter", "space": "playfield", "x": entry["x"], "y": entry["y"],
		"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
	} for index, entry in enumerate(entries, start=1)]
	notes = (
		"One G.I. relay on the I/O Power Driver board (driven from U206 data latch through Q200) switches the 5.7v AC G.I. supply to four "
		"separately fused circuits (General Illumination Circuit Detailed Wiring Diagram, PDF 126): Circuit 1, F24, BRN-WHT to WHT-BRN, "
		"Back Panel X12, 12 #44; Circuit 2, F25, YELLOW to WHT-YEL, Mid./Lwr. Rt. P/F X13, 11 + 1 #44 + #555; Circuit 3, F26, GREEN to "
		"WHT-GRN, Upr. Rt. Playfield X8 + US Coin Door X2 (Euro X3), 8 #44 plus 2 #555 on the coin door; Circuit 4, F27, VIOLET to WHT-VIO, "
		"Middle / Lower Left Playfield X12, 10 + 2 #44 + #555. The page warns that G.I. bulb quantities may change during production. "
		"The quantity 47 counts circuit 2 by its X13 location count, which the drawing's 13 Y circles match, not by its 11 + 1 bulb line. "
		"se.c publishes the relay as GI 0 (on while the latch bit is low); the retained table's UpdateGI switches every light of its GI "
		f"collection from GICallback. The {len(entries)} distinct GI collection lights match the drawing's 33 playfield G.I. circles (12 V, "
		"8 G, 13 Y, read independently) one for one in count; they are placed as the playfield bulbs, observed only, because the "
		"drawing is a mirrored bottom view without reliable controls. The 12 back-panel and two coin-door bulbs are counted but not placed."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, RUNTIME_SOURCE),
		aliases=[{"namespace": "pinmame.gi", "value": "0"}],
		physical={"location": "playfield, back panel and coin door", "quantity": 47, "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT 5.7v AC through F24-F27", "power_connection": "J14/J15", "nominal_voltage_v": 5.7, "voltage_type": "ac"},
		spatial={"status": "observed", "placements": placements},
	)]


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "Dot Matrix Display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		"spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
	}]


# --- Mechanisms ----------------------------------------------------------------------------------------
def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], positions: list[dict[str, Any]] | None = None, assembly: str | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
	if assembly:
		result["assembly_part_number"] = assembly
	if positions is not None:
		result["positions"] = positions
	result["provenance"] = provenance("validated", *refs)
	return result


def mechanisms() -> list[dict[str, Any]]:
	common = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	run = common + (RUNTIME_SOURCE,)
	s = switch_id
	q = q_output_id
	return [
		_mechanism("trough", "4-ball trough with up-kicker and stacking opto", "kicker", [q(1)], [s(11), s(12), s(13), s(14), s(15)],
			"Four balls rest in the trough on roller switches 11 (left), 12 and 13 and on the VUK opto 14 at the up-kicker. Q1 kicks the ball on 14 up "
			"past the stacking opto 15 into the shooter lane, and the rest roll one place toward the up-kicker. Hold each occupied position at 1 and "
			"pass the kicked ball through 15 as a short 1 pulse: the ROM reads 15 at 1 as a ball in the beam and, with balls still on 11-14, keeps "
			"kicking (six tries, then the auto launch) until 15 falls. The retained table's bsTrough omits 15 and pulses 22 instead, a defect.",
			run, assembly="500-6318-14"),
		_mechanism("shooter", "Ball shooter and auto launch", "kicker", [q(2)], [s(16)],
			"A served ball rests on shooter-lane switch 16. The player plunges it with the ball shooter (500-6146-00-04), or Q2 fires the "
			"autoplunger arm (500-6091-00 with coil 500-6092-03B and shooter-lane switch assembly 500-6096-00). The retained table uses a "
			"cvpmImpulseP (power 50, 0.6 s, randomization 0.3) on trigger swplunger.", common),
		_mechanism("left-eject", "Left eject under the fish", "kicker", [q(21)], [s(17)],
			"A 30-degree eject (500-6511-01) under the fish: the ball settles on 17 and Q21 kicks it out. In the gameplay run a ball held on 17 "
			"drew repeated Q21 kicks with the fish jaw (Q17) and the left-sling flasher (Q27).", run, assembly="500-6511-01"),
		_mechanism("center-eject", "Center eject under the safe", "kicker", [q(3)], [s(28)],
			"The second 30-degree eject (500-6511-01), under the safe: the ball settles on 28 and Q3 kicks it out; a ball held on 28 drew "
			"repeated Q3 kicks.", run, assembly="500-6511-01"),
		_mechanism("center-lock", "Center lock with up/down post", "gate", [q(4)], [s(22), s(23)],
			"The up/down post assembly 500-5867-02 (labelled SPINNER LANE BALL LOCK on its drawing) holds balls on Center Lock 1 (22) and 2 (23). "
			"Q4 (27-1500) pulls the post down while energized; the spring returns it. The retained table drops wall CenterPost while Q4 is on.",
			common, assembly="500-5867-02"),
		_mechanism("boat-lock", "Boat (right ramp) lock with up/down post", "gate", [q(22)], [s(31), s(32)],
			"Up/down post assembly 500-5867-09 on the right steel (boat) ramp holds balls on Boat Lock 1 (31) and 2 (32); Q22 lowers it while "
			"energized. The retained table drops wall BoatPost while Q22 is on.", common, assembly="500-5867-09"),
		_mechanism("bing-lock", "Bada Bing! lock with up/down post", "gate", [q(23)], [s(19), s(20)],
			"The second 500-5867-09 post, behind the left wire ramp, holds balls on Bing 1 (19) and 2 (20) at the Bada Bing!; Q23 lowers it while "
			"energized. In the gameplay run the left ramp switch (9) raised Q23 and the right ramp switch (25) released it, so the ROM holds the "
			"post energized for long stretches. The retained table drops wall BingPost while Q23 is on.", run, assembly="500-5867-09"),
		_mechanism("control-gates", "Left and right 2-way control gates", "diverter", [q(5), q(6)], [],
			"Two 2-way ball gates (ball gate coil assembly 515-6544-01, mini-coil 32-1800, one bracket mounted mirrored for each side) at the "
			"top of the playfield. Each flap swings while its coil is energized and returns on release. The retained table opens gates sol5 and "
			"sol6 while Q5/Q6 are on. Neither gate has a position switch.", common, assembly="515-6544-01"),
		_mechanism("drop-target", "1-bank drop target", "drop_target_bank", [q(7), q(14)], [s(26)],
			"Assembly 500-6893-01: one drop target with switch 26 (closed while down), a 27-1500 reset coil (Q14) and a 32-1250 mini trip coil "
			"(Q7, assembly 515-6916-01) that knocks the target down under ROM control. In the gameplay run the ROM reset it at power-up and on "
			"Start and tripped and reset it at the drain.", run, assembly="500-6893-01"),
		_mechanism("safe", "Safe door with latch", "toy", [q(8), q(30)], [s(10), s(21), s(24)],
			"The safe (front assembly 515-7493-00 above the playfield, bottom 500-6865-00 below) has a door struck by the ball on Safe Hit Left (21) "
			"and Right (24). A dual coil mounting bracket carries the Safe coil (Q8, 22-1080) and the Safe Latch coil (Q30, 27-1500); the Cherry "
			"limit switch 10 (180-5198-00) senses the door's travel. In the harness runs Q8 and Q30 fired together at power-up and on every safe "
			"hit (Q8 on, Q30 on, Q8 off, Q30 off). The retained table models the door from those two outputs: Q8 energized starts it closing and Q8 "
			"released starts it opening, while Q30's latch, if set when Q8 changes, only selects the closing state without moving an idle "
			"door; it writes 10 at the end of each travel (1 open, 0 closed). Neither the manual nor any run settles the physical door's sequence or the limit switch's sense, so treat the table's "
			"model as a working recreation, not as the factory mechanism.", run, assembly="500-6865-00"),
		_mechanism("fish", "Talking fish head", "toy", [q(17), q(25)], [],
			"The fish head and body (515-7455-00, with clear lite-hat eyes) has a molded jaw on a lever bracket driven by the fish-jaw coil Q17 "
			"(27-1500); the Q25 flash lamp (#44 LED) inside the head lights the eyes. The ROM works the jaw in time with speech; in the gameplay "
			"run it opened and closed with a bumper hit and while a ball sat in the left eject below the fish.", run),
		_mechanism("bada-bing", "Bada Bing! pole dancers", "motorized", [q(18)], [],
			"Q18 energizes a relay (500-6700-00) that runs the Bada Bing! motor (500-6887-00, 24v AC, bi-directional, about 46-55 RPM), which turns "
			"two pole-dancer dolls on shafts through 1\" and 1-1/2\" pulleys and a clear belt. There is no position switch: the dancers simply spin "
			"while Q18 is on. The retained table spins primitives stripper1/stripper2 while Q18 is on.", run, assembly="500-6887-00"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], ["switch.84-left-flipper-button", "switch.83-left-flipper-end-of-stroke", "switch.82-right-flipper-button", "switch.81-right-flipper-end-of-stroke"],
			"Left (500-6543-12) and right (500-6543-02) flipper assemblies with 22-1080 coils on one 50v supply. The CPU applies a 40 ms pulse on a "
			"button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke switch opens at full stroke, and a closure "
			"during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and Q16 at 45/46.", (MANUAL_SOURCE, CORE_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE)),
		_mechanism("bumpers", "Three pop bumpers", "other", [q(9), q(10), q(11)], [s(49), s(50), s(51)],
			"Left (Q9/49), right (Q10/50) and bottom (Q11/51) pop bumpers with stack-blade spoon switches; each switch fired its own coil in the "
			"gameplay run, with the two red bumper domes (Q29).", run),
		_mechanism("slingshots", "Slingshots", "other", [q(12), q(13)], [s(59), s(62)],
			"Left (Q12/59) and right (Q13/62) slingshots (500-5849-01), two parallel blade contacts per side; each switch fired its own coil in the "
			"gameplay run.", run, assembly="500-5849-01"),
		_mechanism("uk-post-save", "UK Post Save ball deflectors and center post", "other",
			["device.aux1-uk-left-up-down-post-left-outlane-ball-deflector", "device.aux2-uk-center-up-down-post", "device.aux3-uk-right-up-down-post-right-outlane-ball-deflector"],
			[s(1), s(8)],
			"UK only: board 520-5068-01 (UK 3X Trans. Driver Board) drives the left and right outlane ball deflectors (AUX 1/AUX 3, 500-5788-02) and "
			"the center up/down post (AUX 2, 500-6293-00) at public 33-35. The cabinet buttons on 1 and 8 ask the ROM for the Post Save; the ROM, "
			"not a wire, raises the deflectors. A standard machine fits none of it.", (MANUAL_SOURCE, CORE_SOURCE)),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"The Sopranos driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = "identical"
		record["variant_notes"] = _driver_note(driver_id)
		records.append(record)
	return records


# --- Sources -------------------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _excerpt_digests() -> dict[str, str]:
	return {path.name: _file_sha256(path) for path in sorted(EXCERPT_ROOT.glob("*")) if path.is_file()}


EXCERPT_FILE_HASHES = _excerpt_digests()

IMAGE_DERIVATIONS = {
	"switch-locations": f"{MANUAL_NAME} page 6, crop box 0.04,0.49,0.885,0.785, scanned page rendered at its native resolution (embedded image xref 228, 2698px across 7.10in), rendered at 380 dpi, grayscale, 2730x1234 WebP quality 80",
	"lamp-locations": f"{MANUAL_NAME} page 7, crop box 0.1,0.49,0.915,0.775, scanned page rendered at its native resolution (embedded image xref 304, 2698px across 7.10in), rendered at 380 dpi, grayscale, 2633x1192 WebP quality 80",
	"coil-flash-locations": f"{MANUAL_NAME} page 9, crop box 0.11,0.035,0.53,0.925, scanned page rendered at its native resolution (embedded image xref 5450, 1311px across 3.79in), rendered at 346 dpi, grayscale, 1236x3387 WebP quality 80",
	"gi-wiring": f"{MANUAL_NAME} page 126, crop box 0.12,0.09,0.95,0.92, born-digital page rendered for legibility (smallest type in region 4.0pt, targeting 11px glyphs), rendered at 198 dpi, grayscale, 1398x1808 WebP quality 80",
	"flipper-circuit": f"{MANUAL_NAME} page 129, crop box 0.05,0.04,0.97,0.93, born-digital page rendered for legibility (smallest type in region 5.0pt, targeting 11px glyphs), rendered at 158 dpi, grayscale, 1240x1552 WebP quality 50",
}


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {"id": f"excerpt.the-sopranos.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md", "sha256": EXCERPT_FILE_HASHES[f"{name}.md"]}
	if name in IMAGE_DERIVATIONS:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = IMAGE_DERIVATIONS[name]
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("switch-matrix", "PDF page 6, printed DR. 4, Switch Matrix Grid and dedicated-switch column", method="mixed", credit=TEXT_CREDIT),
		_excerpt("switch-locations", "PDF page 6, printed DR. 4, switch location drawing (lower half)"),
		_excerpt("lamp-matrix", "PDF page 7, printed DR. 5, Lamp Matrix Grid", method="mixed", credit=TEXT_CREDIT),
		_excerpt("lamp-locations", "PDF page 7, printed DR. 5, lamp location drawing and back-panel inset (lower half)"),
		_excerpt("coil-table", "PDF page 8, printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 9, printed DR. 7, Coil & Flash Lamp Locations drawing and its notes"),
		_excerpt("gi-wiring", "PDF page 126, printed Section 5 page 109, General Illumination Circuit Detailed Wiring Diagram; with the PDF page 3 fuse list"),
		_excerpt("flipper-circuit", "PDF page 129, printed Section 5 page 112, 2-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 131, printed Section 5 page 114, Cabinet / Coin Door Wiring Diagram", method="mixed", credit=TEXT_CREDIT),
		_excerpt("mechanism-assemblies", "PDF pages 83 and 100-121, printed 66 and 83-104, playfield switch parts and the major-assembly pages", method="mixed", credit=TEXT_CREDIT),
		_excerpt("game-operation", "PDF pages 13-14, 19, 27-28 and 132, contents, game operation, switch-test text and trough opto boards", method="mixed", credit=TEXT_CREDIT, reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	harness = load_json(ROOT / RUNTIME_EVIDENCE_PATH)
	runs = ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in harness["runtime"]["raw_runs"])
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the sopranos clone tree (" + ", ".join(sorted(DRIVER_IDS)) + ")",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/segames.c INITGAME macro (FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, custSol 0) and INITGAME(sopranos, GEN_WS, "
				"se_dmd128x32, SE_BOARDID_520_5068_01) with the 21 sopranos ROM sets; src/wpc/se.c switch_r (~core_getSwCol), dedswitch_r (flipper "
				"column swapped into U206 order, complemented), dip_r, se_solenoid_w (Q15/Q16 masked off and published at 47/45), the fast-flip "
				"byte at 0x04 driving public 15, the G.I. relay at gi[0], the 520-5068-01 ESTB latch at 33-35, ram_w's memory-protect gate on -3, "
				"nLamps = 64 + lampCol * 8; src/wpc/core.c core_updateSw (no FLIP_EOS: EOS bits untouched); src/wpc/core.h CORE_FIRSTCUSTSOL 51."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"locator": "Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes",
			"license": "BSD-3-Clause", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "acquired_at": "2026-10-09T18:15:00Z",
			"locator": (
				"IPDB machine 5053 'The Sopranos' (Stern Pinball, February 2005, model I-0085, Stern Whitestar (modified), 4 players), read live in "
				"an interactive browser session. Its documentation list carries the service manual whose bytes match the retained copy, and its note "
				"that a few S.A.M.-board games were shipped overseas for testing and converted to Whitestar before sale."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", f"IPDB machine 5053 page, {IPDB_URL}", reviewed=False, credit="curator, read from the rendered page")],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}", "original_filename": MANUAL_IPDB_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-08-31T07:20:24Z",
			"locator": (
				"Stern The Sopranos Pinball Game Service Manual (214 pages, born-digital with scanned location drawings). PDF 6-9 are the front-matter "
				"Dr. Pinball sheets (DR. 4 switch matrix and locations, DR. 5 lamp matrix and locations, DR. 6 coil chart, DR. 7 coil and flash "
				"locations); PDF 83 the playfield switch parts; PDF 100-121 the major assemblies; PDF 123-131 the Section 5 coil chart copy, I/O "
				f"board, G.I., flipper and cabinet wiring. Direct resource {MANUAL_URL}, re-downloaded on 2026-10-09 with the same SHA-256 as the copy "
				"retained on 2026-08-31 under a shortened name."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Stern Pinball, Inc.; hosted by the Internet Pinball Machine Database",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/the-sopranos-2005/Sopranos,%20The%20(Stern%202005).vpx",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				"Retained freneticamnesic/32assassin 1.0.2 recreation (table info: 'Beta table by freneticamnesic, strip and rebuild on VP 10.5 by "
				f"32assassin'). Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. "
				"Geometry authority only for the objects its embedded script binds; the placement seed tools/seeds/stern/the-sopranos-2005-spatial.json "
				"lists them."
			),
			"license": "NOASSERTION", "attribution": "freneticamnesic and 32assassin (table authors)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": "external:pinmame-vpx-sources/stern/the-sopranos-2005/Sopranos,%20The%20(Stern%202005).vbs",
			"original_filename": "Sopranos, The (Stern 2005).vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script (identical to extracted-vpxtool/script.vbs). Runtime authority for controller callbacks: "
				"Const cGameName = \"sopranos\", LoadVPM \"01560000\", \"sega.VBS\", 3.10, HandleMechanics = 0, the bsTrough/bsTEject/bsRScoop "
				"ball stacks, dtSingle, plungerIM, the SolCallback table and the NFadeL lamp calls. Known table defects: solTrough pulses 22 instead "
				"of the stacking opto 15, and the right-ramp switch 25 is a spinner; its Start-key writes to 16 are unreachable behind the VPinMAME key handler."
			),
			"license": "NOASSERTION", "attribution": "freneticamnesic and 32assassin (table authors)", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit="curator, quoted from the script file")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/the-sopranos-2005/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest SHA-256 "
				f"{EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, extracted with vpxtool from the "
				f"retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_CORPUS_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPX_CORPUS_REVISION}/" + quote("special_audiopan_and_audiofade_patched/The Sopranos (Stern 2005) v1.22.vbs", safe="/"),
			"revision": VPX_CORPUS_REVISION, "sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				"Pinned corpus script of the 2024 'Modern Upgrade' v1.22 of the same table lineage (credited to JPSalas, freneticamnesic, 32assassin "
				"and others). Its SolCallback table (lines 110-137), ball stacks (lines 429-451) and switch handlers (lines 582-652) repeat the 1.0.2 "
				"bindings, including solTrough's PulseSw 22 (line 225), and writes 16 on the Start key before calling the VPinMAME key handler (lines 496, 554); it rebinds 25 from a spinner to a "
				"Hit handler (line 617). It corroborates the bindings, not independently: both descend from one table."
			),
			"license": "NOASSERTION", "attribution": "Table authors credited in the script; vpxtable_scripts contributors",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sega.vbs",
			"original_filename": "sega.vbs", "sha256": VPM_SEGA_SHA256,
			"locator": (
				"VPinMAME Sega/Stern Whitestar script library the retained table loads, copied from the contributor's Visual Pinball Scripts "
				f"folder beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). It defines GameOnSolenoid = 15, swBlack 0 / swGreen -1 / "
				"swRed -2 / swMemoryProtect -3, swStartButton 54, swTilt 56, swSlamTilt 55, swCoin3 4 / swCoin1 5 / swCoin2 6, swLRFlip 82, "
				"swLLFlip 84, swURFlip 81 and swULFlip 83, and the country DIP form."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library", "sega.vbs constants (lines 20-39), DIP form (lines 52-69) and key handlers (lines 71-139)", credit="curator, quoted from the library file")],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/sopranos.zip", "revision": "5.00", "sha256": ROM_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned sopranos ROM set (sopcpua.500 CRC e3430f28, sopdspa.500 CRC 170bd8d1); used to identify the ROM the harness booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Stern Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				f"Three hash-pinned LibPinMAME harness runs of sopranos (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM with built-in mechanisms off: {runs}. Scenarios under tools/harness-scenarios/whitestar; "
				"tools/sopranos_runtime_evidence.py derives the committed per-step transitions from the retained runs."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/stern/the-sopranos-2005-callouts.json", "sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of PDF 6, 7 and 9 (DR. 4, DR. 5 and DR. 7): every callout transcribed independently "
				"on the committed excerpt crops, per-page control and callout fits; a table placement whose own callout lands within 0.07 normalized "
				"under both fits is validated (tools/drawing_callouts.py). Reads, overlays and the generator are retained under review-artifacts with a "
				"pinned manifest."
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
			"id": MACHINE_ID, "name": "The Sopranos", "manufacturer": "Stern", "year": 2005, "kind": "physical_pinball", "model_number": "I-0085",
			"ipdb_id": 5053, "opdb_id": "G5WoB-MDyNZ",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "validated",
				"mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.whitestar", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/stern/the-sopranos-2005.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"The Sopranos device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"The Sopranos mechanism {mechanism['id']} names unknown devices: {unknown}")
	drawing_callouts.apply_to_definition(definition, _callout_seed(), CALLOUT_SOURCE)
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"The Sopranos retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained The Sopranos extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"The Sopranos retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("The Sopranos retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"The Sopranos retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


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
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield", "source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right", "y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256, "embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH), "callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "total_bytes": EXTRACTION_TOTAL_BYTES, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/the-sopranos-2005/extracted-vpxtool.manifest.json", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/stern/the-sopranos-2005-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "The centre of the VPX object the embedded script binds to each switch (trigger, gate, spinner, hit target, kicker, slingshot wall, bumper). The trough switches and the stacking opto, which the table does not model, are projected onto the release kicker BallRelease; the safe limit onto the midpoint of the two safe-door walls; each end-of-stroke contact onto its flipper.",
			"lamp": "The centre of the insert Light each lamp's NFadeL call drives. The five Episodes lamps 73-77, which the table stacks at one point, are drawing-measured candidates.",
			"solenoid": "The kicker, slingshot wall, bumper, flipper, post wall or gate the script fires, and for flashers the script-driven Light. The auto launch is placed on the shooter-lane trigger its impulse plunger uses; the drop-target coils on the target; the safe and safe-latch coils on the safe door; the fish jaw and fish flasher on the jaw primitive; the Bada Bing! relay on the dancers' midpoint. The UK AUX posts are drawing-measured candidates.",
			"gi": "The 33 Light members of the table's GI collection; observed only, without per-string assignment.",
		},
		"unresolved_geometry": [
			"The trough switches 11-15 and the safe limit 10 are not modelled by the table; their placements are projections onto mechanism objects and stay observed.",
			"The five Episodes lamps 73-77 share one table point; their drawing-measured placements are candidates.",
			"The UK AUX posts 33-35 are not in the US table; their drawing-measured placements are candidates.",
			"The flipper and slingshot coils, the Q31 left flasher, the second Q29 dome and other placements listed below fail the callout limit or have no callout, and stay observed.",
			"The G.I. drawing is a mirrored bottom view without reliable controls, so the 33 G.I. placements stay observed although their count matches.",
		],
		"promotion_decision": "partial: every used device has a placement or a controlled not-applicable record, but projections, candidates and placements the drawings do not confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Sopranos (Stern, 2005) spatial blockers", "",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest `{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.", "",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places.", "",
		"## Placement status", "",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [f"- controlled `not_applicable` records: {report['not_applicable_device_count']}", f"- used devices with no placement record: {len(report['without_placements'])}", ""]
	lines += [f"  - `{item}`" for item in report["without_placements"]]
	lines += ["", "## Projection classes", ""]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	check = report["drawing_callout_check"]
	lines += ["", "## Drawing callout check", "", f"{check['rule']} It validates {check['validated']} of the {check['checked']} table placements it checks ([seed](../../../{check['seed']})); the rest keep their observed status:", ""]
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
		raise RuntimeError(f"Refusing to overwrite an author-ready The Sopranos artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale The Sopranos author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"The Sopranos deterministic artifact drift: {path}")
	print("The Sopranos definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"The Sopranos extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("The Sopranos retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
