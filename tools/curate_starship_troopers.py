"""Curate the physical Sega Starship Troopers (1997) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads one committed seed, the placements (the retained table's object coordinates, rebuilt by
tools/starship_troopers_spatial_seed.py), so regeneration reproduces the canonical artifact byte-for-byte without
reading the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes the
definition, its knowledge note and its spatial report.
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


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "sega.starship-troopers.1997"
PARTIAL_PATH = ROOT / "machines/partial/sega/starship-troopers-1997.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/sega/starship-troopers-1997.json"
KNOWLEDGE_PATH = ROOT / "knowledge/sega/starship-troopers-1997.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/sega/starship-troopers-1997.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/sega/starship-troopers-1997-spatial.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/sega/starship-troopers-1997.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/sega/starship-troopers-1997.md"
RUNTIME_201_PATH = "evidence/runtime/whitestar/starship-troopers-startrp-gameplay.json"
RUNTIME_200_PATH = "evidence/runtime/whitestar/starship-troopers-startrp2-gameplay.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = "pinmame.catalog.46e1a01a0f73"
CORE_SOURCE = "pinmame.core.46e1a01a0f73"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
IDENTITY_SOURCE = "identity.sega.starship-troopers.1997"
MANUAL_SOURCE = "manual.sega.starship-troopers.1997"
VPX_TABLE_SOURCE = "vpx-table.starship-troopers-vpw-2-0"
VPX_SCRIPT_SOURCE = "vpx-script.starship-troopers-vpw-2-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.starship-troopers-vpw-2-0"
VPX_OBJ_SOURCE = "vpx-obj.starship-troopers-vpw-2-0"
VPX_CORPUS_SOURCE = "vpx-script.e97088ef82faf822"
VPM_LIBRARY_SOURCE = "vpm-script-library.sega-vbs"
RUNTIME_SOURCE = "runtime.starship-troopers.startrp"
RUNTIME_200_SOURCE = "runtime.starship-troopers.startrp2"
ROM_SOURCE = "rom.sega.starship-troopers.2-01"
ROM_200_SOURCE = "rom.sega.starship-troopers.2-00"
LEGACY_SOURCE = "legacy.game.sst"
RUNTIME_LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE_SHA256 = "128e61465d43dc6188ac8c0e358f1a97de9513e3170cc82e75cba46ffa98b648"
ROM_200_ARCHIVE_SHA256 = "13cf7c70ba7eeaa9211b860b031ea2ae3c0074e927fd7b63b61499189dab9a26"
# Retained harness run directory -> SHA-256 of its manifest.json (tools/starship_troopers_runtime_evidence.py pins the same values).
RUN_MANIFESTS = {
	"startrp-gameplay": "ca4dff02c54bbf4f10661d1832a2077174faa52530a7484d4e3f051041311fd6",
	"startrp2-gameplay": "f11b88f3bb849debe95b0a38279ff457e8f08ced02a9a9764dcfc2eab7cbc810",
}
BOTH_RUNS = (RUNTIME_SOURCE, RUNTIME_200_SOURCE)

TABLE_NAME = "Starship Troopers (Sega 1997) VPW Mod v2.0.vpx"
TABLE_SHA256 = "0d7020ac848dc66f12d5faf2a12961bde69a606d154511947755bd0ac9b4731a"
TABLE_BYTES = 178515968
SCRIPT_SHA256 = "e97088ef82faf82205fbb080dac0f8489370ec03364cedc7d5b3f26bd5b03c3a"
CORPUS_SCRIPT_SHA256 = SCRIPT_SHA256
CORPUS_BLOB_SHA256 = "afe0f41f73be055ae62f834e5c9552a8aa685f86d9acf0602d01057965d66d8d"
CORPUS_PATH = "Starship Troopers (Sega 1997) VPW Mod v2.0/Starship Troopers (Sega 1997) VPW Mod v2.0.vbs.original"
VPX_CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
MANUAL_NAME = "Sega_1997_Starship_Troopers_Manual.pdf"
MANUAL_SHA256 = "0b773570c3ddaa38f6d63f7a590d4a8986f34facf70064cf3446cfc44ae22d09"
IPDB_PAGE_SHA256 = "fde477fd7e966324edbecc4b2eace5bbdadabc5fed15a747cf2416a7c3817f71"
VPM_SEGA_SHA256 = "d6e508aac5163fc6d93155e630a1ef5e9c57c3ef3416ada8930dca046daf4924"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2133.17
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2133.17"

EXTRACTION_FILE_COUNT = 1294
EXTRACTION_TOTAL_BYTES = 203950490
EXTRACTION_MANIFEST_SHA256 = "8b75f4b4810f47bfdfc06598e46e89a7a6891494808e7a23a9bbc74e73739cde"
VPX_DIRECTORY = "sega/starship-troopers-1997/vpw-mod-v2-0"
EXTRACTION_RELATIVE_PATH = Path(f"{VPX_DIRECTORY}/Starship Troopers (Sega 1997) VPW Mod v2.0")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path(f"{VPX_DIRECTORY}/extracted-vpxtool.manifest.json")
OBJ_EXPORT_RELATIVE_PATH = Path(f"{VPX_DIRECTORY}/world-obj-vpu/Starship Troopers (Sega 1997) VPW Mod v2.0.obj")
OBJ_EXPORT_SHA256 = "cb0003b5b9f3636e279d1df332ae6a848dab965906c94e6a5895ae024d83406d"
# The Whitestar platform profile this record's controller facts were checked against. A change to the profile stops
# the curator until the record has been reviewed against it and this pin updated.
CONTROLLER_PROFILE_PATH = ROOT / "controllers/pinmame/whitestar.json"
CONTROLLER_PROFILE_SHA256 = "5b1684e64f6259cdfb5969b5543a2052b794524eba3ae0254e261257d06a6b12"

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=4341"
IPDB_WAYBACK_URL = "https://web.archive.org/web/20261016082552id_/https://www.ipdb.org/machine.cgi?id=4341"
MANUAL_URL = "https://www.ipdb.org/files/4341/" + MANUAL_NAME
MANUAL_WAYBACK_URL = "https://web.archive.org/web/20251205014627id_/" + MANUAL_URL
EXCERPT_CREDIT = "curator, read from the rendered page"
QUOTE_CREDIT = "curator, quoted from the source file"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


# --- Legacy aliases ----------------------------------------------------------------------------------
# Addresses the superseded legacy-migrated record (legacy.game.sst, a VBScript-parser import of the same VPW table
# lineage) carried, kept as numeric and zero-padded vpe-legacy aliases while legacy consumers still resolve them. That
# record also exposed the table's SetLamp channels 123 and 129-132 (the brain bug and F5-F8 flash lamps) and 200 (the
# G.I.) as lamps, and named the lower flipper coils; those names stay on the devices they denote.
LEGACY_SWITCHES = {9, 10} | set(range(12, 36)) | set(range(37, 44)) | set(range(45, 54)) | set(range(56, 63)) | {88}
LEGACY_COILS = {1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 17, 23, 25, 26, 27, 28, 29, 30, 31, 32, 46, 48}
LEGACY_LAMPS = set(range(1, 33)) | set(range(35, 81)) | {123, 129, 130, 131, 132, 200}
LEGACY_COIL_NAMES = {46: "c_flipper_lower_right", 48: "c_flipper_lower_left"}
# Public solenoid -> the legacy lamp channel the table drives from that solenoid's callback.
LEGACY_LAMP_ON_SOLENOID = {23: 123, 29: 129, 30: 130, 31: 131, 32: 132}


def legacy_aliases(namespace: str, address: int, addresses: set[int]) -> list[dict[str, str]]:
	if address not in addresses:
		return []
	values = list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))
	return [{"namespace": namespace, "value": value} for value in values]


# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("startrp", "startrp2")
BASE_DRIVER_NOTE = (
	"segames.c builds both Starship Troopers drivers from the same INITGAME(GEN_WS, se_dmd128x32, 0) record (lower flippers "
	"only, no auxiliary board), the same display and sound ROMs and the same de_mSES1 machine driver, and MACHINE_INIT(se)'s "
	"'startrp' prefix gives both the fast-flip byte at CPU RAM 0x00 and the same output types, so the controller routing is "
	"identical; "
)
DRIVER_NOTES = {
	"startrp": (
		"CPU 2.01 (sstcpu.201), the root set and the latest code. The gameplay harness run drew the same switch-to-coil "
		"responses as startrp2 except for which stepper phases a few events pulsed."
	),
	"startrp2": (
		"CPU 2.00 (sstcpu.200), a clone of startrp with the same display (sstdspa.200) and sound sets: the code the retained "
		"table loads (cGameName = \"startrp2\"). Its gameplay harness run repeated the startrp scenario step for step."
	),
}
DRIVER_COMPATIBILITY = {"startrp": "identical", "startrp2": "identical"}


# --- Switch data -------------------------------------------------------------------------------------
# address -> (label, grid name, part cell, switch type, availability, roles, pulse)
SWITCHES: dict[int, tuple[str, str, str, str, str, tuple[str, ...], bool]] = {
	2: ("4th Coin Slot", "4TH COIN SLOT", "180-5024-00", "other", "optional", ("cabinet.coin.fourth",), True),
	3: ("6th Coin Slot", "6TH COIN SLOT", "(Future Use)", "other", "optional", ("cabinet.coin.sixth",), True),
	4: ("Right Coin Slot", "RIGHT COIN SLOT", "180-5024-00", "other", "used", ("cabinet.coin.right",), True),
	5: ("Center Coin Slot / DBA", "CENTER COIN SLOT / DBA", "180-5024-00", "other", "used", ("cabinet.coin.center",), True),
	6: ("Left Coin Slot", "LEFT COIN SLOT", "180-5024-00", "other", "used", ("cabinet.coin.left",), True),
	7: ("5th Coin Slot", "5TH COIN SLOT", "(Future Use)", "other", "optional", ("cabinet.coin.fifth",), True),
	9: ("Under-Trough: Skill Shot", "U'TROUGH: SKILL SHOT", "180-5057-00", "microswitch", "used", ("ball.path",), False),
	10: ("Under-Trough: Bug Hole", "U'TROUGH: BUG HOLE", "180-5057-00", "microswitch", "used", ("ball.path",), True),
	12: ("4-Ball Trough 1 (Left)", "4-BALL TROUGH #1 (LEFT)", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	13: ("4-Ball Trough 2", "4-BALL TROUGH #2", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	14: ("4-Ball Trough 3", "4-BALL TROUGH #3", "180-5119-00", "microswitch", "used", ("ball.position",), False),
	15: ("4-Ball Trough VUK Opto", "4-BALL TROUGH VUK OPTO", "TRANS 520-5124-00 / REC 520-5125-00", "opto", "used", ("ball.position",), False),
	16: ("Shooter Lane", "SHOOTER LANE", "500-5096-00", "unknown", "used", ("ball.position",), False),
	17: ("Left Bottom Stand-Up (Green)", "LEFT BOTTOM S-U (GRN)", "500-6139-04", "leaf", "used", (), True),
	18: ("Left Middle Stand-Up (Yellow)", "LEFT MIDDLE S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	19: ("Left Middle Stand-Up (Red)", "LEFT MIDDLE S-U (RED)", "500-6075-02", "leaf", "used", (), True),
	20: ("Left Top Stand-Up (Yellow)", "LEFT TOP S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	21: ("Right Bottom Stand-Up (Red)", "RIGHT BOTTOM S-U (RED)", "500-6075-02", "leaf", "used", (), True),
	22: ("Right Middle Stand-Up (Yellow)", "RIGHT MIDDLE S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	23: ("Right Middle Stand-Up (Green)", "RIGHT MIDDLE S-U (GRN)", "500-6139-04", "leaf", "used", (), True),
	24: ("Right Top Stand-Up (Yellow)", "RIGHT TOP S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	25: ("Left Ramp Enter", "LEFT RAMP ENTER", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	26: ("Left Ramp Exit", "LEFT RAMP EXIT", "180-5093-00", "microswitch", "used", ("ball.path",), True),
	27: ("Left Ramp Stand-Up (Yellow)", "LEFT RAMP S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	28: ("Pop Stand-Up (Blue)", "POP S-U (BLU)", "500-6228-05", "leaf", "used", (), True),
	29: ("Pop Stand-Up (Green)", "POP. S-U (GRN)", "500-6139-04", "leaf", "used", (), True),
	30: ("VUK Stand-Up (Green)", "VUK S-U (GRN)", "500-6139-04", "leaf", "used", (), True),
	31: ("VUK Stand-Up (Blue)", "VUK S-U (BLU)", "500-6228-05", "leaf", "used", (), True),
	32: ("Right Ramp Stand-Up (Yellow)", "RIGHT RAMP S-U (YEL)", "500-6138-06", "leaf", "used", (), True),
	33: ("Stepper Motor Rear", "STEPPER MOTOR REAR", "180-5119-00", "microswitch", "used", ("position.rear",), False),
	34: ("Stepper Motor Front", "STEPPER MOTOR FRONT", "180-5119-00", "microswitch", "used", ("position.front",), False),
	35: ("Warrior Bug Target", "STEPPER MOTOR BUG", "180-5119-00", "leaf", "used", (), True),
	37: ("Brain Bug Up", "BRAIN BUG UP", "180-5165-00", "microswitch", "used", ("position.up",), False),
	38: ("Brain Bug Hit", "BRAIN BUG HIT", "180-5165-00", "microswitch", "used", (), True),
	39: ("Brain Bug Up", "BRAIN BUG UP", "180-5165-00", "microswitch", "used", ("position.up",), False),
	40: ("Under-Trough: Pop Exit Hole", "U'TROUGH POP EXIT HOLE", "180-5057-00", "microswitch", "used", ("ball.path",), False),
	41: ("Left Top Lane", "LEFT TOP LANE", "500-6227-02", "microswitch", "used", (), False),
	42: ("Middle Top Lane", "MIDDLE TOP LANE", "500-6227-02", "microswitch", "used", (), False),
	43: ("Right Top Lane", "RIGHT TOP LANE", "500-6227-02", "microswitch", "used", (), False),
	45: ("VUK", "VUK", "180-5116-01", "microswitch", "used", ("ball.position",), False),
	46: ("Super VUK", "SUPER VUK", "180-5052-00", "microswitch", "used", ("ball.position",), False),
	47: ("Left Orbit Opto", "LEFT ORBIT", "TRANS 520-5082-00 / REC 520-5083-01", "opto", "used", ("ball.path",), False),
	48: ("Right Orbit Opto", "RIGHT ORBIT", "TRANS 520-5082-00 / REC 520-5083-01", "opto", "used", ("ball.path",), False),
	49: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "180-5015-03", "leaf", "used", (), True),
	50: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "180-5015-03", "leaf", "used", (), True),
	51: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "180-5015-03", "leaf", "used", (), True),
	52: ("Right Ramp Enter", "RIGHT RAMP ENTER", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	53: ("Right Ramp Exit", "RIGHT RAMP EXIT", "180-5087-00", "microswitch", "used", ("ball.path",), True),
	54: ("Start Button", "START BUTTON", "500-6090-06", "button", "used", ("cabinet.start",), False),
	55: ("Slam Tilt", "SLAM TILT", "180-5022-00", "tilt", "used", ("cabinet.slam-tilt",), False),
	56: ("Plumb Bob Tilt", "PLUMB BOB TILT", "HANGER 535-5319-00 / CONTACT 535-7563-01", "tilt", "used", ("cabinet.tilt",), False),
	57: ("Left Outlane", "LEFT OUTLANE", "500-6227-02", "microswitch", "used", (), False),
	58: ("Left Return Lane", "LEFT RETURN LANE", "500-6227-02", "microswitch", "used", (), False),
	59: ("Left Slingshot", "LEFT SLINGSHOT", "180-5054-00", "leaf", "used", (), True),
	60: ("Right Outlane", "RIGHT OUTLANE", "500-6227-02", "microswitch", "used", (), False),
	61: ("Right Return Lane", "RIGHT RETURN LANE", "500-6227-02", "microswitch", "used", (), False),
	62: ("Right Slingshot", "RIGHT SLINGSHOT", "180-5054-00", "leaf", "used", (), True),
}
UNUSED_SWITCHES = (1, 8, 11, 36, 44, 63, 64)
DOTS_SWITCHES = (16, 26, 33, 34, 35, 38, 40, 45, 46)
# Cabinet switches page 21 lists as "located in the cabinet and ... not noted in the diagram": 2 4 5 6 55 56; 3 and 7 are
# the coin door's Future Use positions and 54 the Start button.
CABINET_SWITCHES = (2, 3, 4, 5, 6, 7, 54, 55, 56)
# DR. 5 boxes drawn white (mounted above the playfield); every other playfield switch is drawn in a black box.
ABOVE_PLAYFIELD = (25, 26, 33, 34, 35, 52, 53)
MATRIX_DRIVE = [("GRN-BRN", "CN5-P1"), ("GRN-RED", "CN5-P3"), ("GRN-ORG", "CN5-P4"), ("GRN-YEL", "CN5-P5"), ("GRN-BLK", "CN5-P6"), ("GRN-BLU", "CN5-P7"), ("GRN-VIO", "CN5-P8"), ("GRN-GRY", "CN5-P9")]
MATRIX_RETURN = [("WHT-BRN", "CN7-P9", "U400"), ("WHT-RED", "CN7-P8", "U400"), ("WHT-ORG", "CN7-P7", "U400"), ("WHT-YEL", "CN7-P6", "U400"), ("WHT-GRN", "CN7-P5", "U401"), ("WHT-BLU", "CN7-P3", "U401"), ("WHT-VIO", "CN7-P2", "U401"), ("WHT-GRY", "CN7-P1", "U401")]
# The printed page-21 table's description where it differs from the grid.
PAGE21_NAMES = {
	3: "6TH COIN SLOT (italic)", 7: "5TH COIN SLOT (italic)", 26: "LEFT RAMP EXIT (on Wire Ramp)", 29: "POP S-U (GRN)",
	40: "U'TROUGH: POP EXIT HOLE", 47: "LEFT ORBIT (OPTO)", 48: "RIGHT ORBIT (OPTO)", 49: "TOP TURBO BUMPER", 55: "SLAM TILT (On Coin Door)",
}
# What the retained VPW Mod v2.0 table's embedded script does with each address (line numbers of that script).
SWITCH_SCRIPT = {
	9: "Trigger sw9 holds 9 while the ball sits on it (lines 1052-1053)",
	10: "sw10_Hit pulses 10 and hands the ball to the super VUK 1.8 s later (line 813)",
	12: "bsTrough.InitSw 0, 15, 14, 13, 12 with Balls = 4 (lines 274-281): a cvpmBallStack holding 12 at 1 while a ball occupies that position",
	13: "bsTrough.InitSw 0, 15, 14, 13, 12 with Balls = 4 (lines 274-281)",
	14: "bsTrough.InitSw 0, 15, 14, 13, 12 with Balls = 4 (lines 274-281)",
	15: "bsTrough.InitSw 0, 15, 14, 13, 12 (lines 274-281): 15 is the exit position the trough up-kicker empties, held at 1 while a ball waits there",
	16: "Trigger sw16 holds 16 while the ball sits on it (lines 1017-1018)",
	17: "Wall T17's Hit handler pulses 17 (line 1066)", 18: "Wall T18's Hit handler pulses 18 (line 1069)",
	19: "Wall T19's Hit handler pulses 19 (line 1072)", 20: "Wall T20's Hit handler pulses 20 (line 1075)",
	21: "Wall T21's Hit handler pulses 21 (line 1078)", 22: "Wall T22's Hit handler pulses 22 (line 1081)",
	23: "Wall T23's Hit handler pulses 23 (line 1084)", 24: "Wall T24's Hit handler pulses 24 (line 1087)",
	25: "Trigger sw25's Hit handler pulses 25 (line 1109)",
	26: "Trigger sw26's Hit handler pulses 26 (line 1113)",
	27: "Wall T27's Hit handler pulses 27 (line 1090)", 28: "Wall T28's Hit handler pulses 28 (line 1093)",
	29: "Wall T29's Hit handler pulses 29 (line 1096)", 30: "Wall T30's Hit handler pulses 30 (line 1099)",
	31: "Wall T31's Hit handler pulses 31 (line 1102)", 32: "Wall T32's Hit handler pulses 32 (line 1105)",
	33: "the warrior bug mech cvpmMyMech mBug registers 33 at its last steps (AddSw 33, 221, 222, line 330) and holds it at 1 while the bug is at that end",
	34: "the warrior bug mech mBug registers 34 at its first steps (AddSw 34, 0, 1, line 329) and holds it at 1 while the bug is at that end",
	35: "BWalls_Hit pulses 35 when the ball hits whichever of the bug walls BWall1-BWall24 UpdateWarriorBug has raised for the bug's position (lines 775-791)",
	37: "SolBrainBug holds 37 at 1 while Q7 is on and at 0 when it drops (lines 695-720)",
	38: "sw38_Hit starts a timer whose handler pulses 38 (lines 726-727); the wall sw38 stands only while Q7 holds the brain bug up",
	39: "SolBrainBug holds 39 at 1 while Q7 is on and at 0 when it drops (lines 695-720)",
	40: "Trigger sw40 holds 40 while the ball sits on it (lines 1061-1062)",
	41: "Trigger sw41 holds 41 while the ball sits on it (lines 1020-1021)",
	42: "Trigger sw42 holds 42 while the ball sits on it (lines 1023-1024)",
	43: "Trigger sw43 holds 43 while the ball sits on it (lines 1026-1027)",
	45: "cvpmSaucer bsLeftVUK (InitKicker sw45, 45, line 297) holds 45 while a ball waits in the VUK",
	46: "cvpmBallStack bsSuperVUK (InitSw 0, 46; InitKick sw46, lines 284-292) holds 46 while a ball waits in the super VUK; sw46_Hit adds a ball to it (line 685)",
	47: "Trigger sw47 holds 47 while the ball passes (lines 1042-1043)",
	48: "Trigger sw48 holds 48 while the ball passes (lines 1045-1046)",
	49: "Bumper1's Hit handler pulses 49 (line 1010)",
	50: "Bumper3's Hit handler pulses 50 (line 1012)",
	51: "Bumper2's Hit handler pulses 51 (line 1011)",
	52: "Trigger sw52's Hit handler pulses 52 (line 1110)",
	53: "Trigger sw53's Hit handler pulses 53 (line 1111)",
	57: "Trigger sw57 holds 57 while the ball sits on it (lines 1029-1030)",
	58: "Trigger sw58 holds 58 while the ball sits on it (lines 1032-1033)",
	59: "the right slingshot wall's handler Rightslingshot_Slingshot (line 964) pulses 59 (line 972), so the table reports a right-slingshot hit as the left slingshot switch",
	60: "Trigger sw60 holds 60 while the ball sits on it (lines 1038-1039)",
	61: "Trigger sw61 holds 61 while the ball sits on it (lines 1035-1036)",
	62: "the left slingshot wall's handler Leftslingshot_Slingshot (line 983) pulses 62 (line 991), so the table reports a left-slingshot hit as the right slingshot switch",
}
# Matrix switches the gameplay harness runs closed, with the outputs the ROM drove in response (step labels in the evidence).
GAMEPLAY_RESPONSE = {
	10: "closing it once changed warrior-bug stepper phases (startrp 19; startrp2 17-20), flashed 26, 27 and 29 and blinked the G.I.",
	16: "a ball resting on it raised the game-on state 15 and energized the warrior-bug stepper phases (17-20)",
	17: "closing it once flashed F3 (27)", 18: "closing it once flashed F2 (26)", 20: "closing it once flashed F2 (26)",
	22: "closing it once flashed F2 (26)", 23: "closing it once flashed F3 (27)", 24: "closing it once flashed F2 (26)",
	27: "closing it once flashed F2 (26)", 29: "closing it once flashed F3 (27)",
	26: "closing it once drew no coil or flasher but blinked the G.I.",
	32: "closing it once flashed F1-F4 (25-28) and F8 (32)",
	35: "closing it once changed warrior-bug stepper phases (startrp 18 and 19; startrp2 18), flashed F5 (29) and blinked the G.I.",
	43: "closing it once flashed F8 (32) and blinked the G.I.",
	45: "a ball held on it drew VUK kicks (3), a super-VUK kick (4), flashes 27, 30 and 32 and G.I. blinks",
	46: "a ball held on it drew super-VUK kicks (4) and flashed F8 (32)",
	38: "closing it once with the brain bug down, since neither run raised it, fired no coil or flasher",
	40: "closing it once fired no coil or flasher, and the G.I. went off during the step",
	47: "closing it once fired the right magnet 6 twice: a hold of about 0.6-0.7 s that began while the input was still 1, and a short pulse about 2 s later",
	48: "closing it once fired the right magnet 6 twice, as 47 does, and changed warrior-bug stepper phases (startrp 19 and 20; startrp2 17-20)",
	49: "closing it once fired the left turbo bumper 9 and changed warrior-bug stepper phases (startrp 17-20; startrp2 18 and 19)",
	50: "closing it once fired the bottom turbo bumper 10",
	51: "closing it once fired the right turbo bumper 11",
	53: "closing it once drew no coil or flasher but blinked the G.I.",
	57: "closing it once flashed F6 (30) and blinked the G.I.",
	59: "closing it once fired the left slingshot 12",
	60: "closing it once flashed F7 (31) and blinked the G.I.",
	62: "closing it once fired the right slingshot 13",
}
GAMEPLAY_QUIET = (9, 19, 21, 25, 28, 30, 31, 41, 42, 52, 58, 61)
# Placed matrix switches the pinned gameplay scenarios never toggle: the trough positions and both warrior bug limits are
# only set at boot, and the scenarios write neither brain bug up switch.
UNTOGGLED_MATRIX_SWITCHES = (13, 14, 15, 33, 34, 37, 39)
HARNESS_COVERAGE = (
	"The scenario's notes say it closes each playfield switch once. Of the placed matrix switches it toggles all but 13-15 and 33, "
	"which it holds closed from boot (the balls in the trough and the warrior bug's rear limit), 34, which it holds open from boot, "
	"and 37 and 39, which it never writes; it leaves the end-of-stroke inputs 81 and 83 to PinMAME."
)


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


def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Observed spatial record for one device from the committed placement seed, or None."""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		# A projection, or a table-derived point checked against a drawing, rests on the manual; a Light on a modelled
		# bulb, dome or socket on the world-space mesh export that shows the part under it.
		refs = [VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE]
		if entry.get("mesh"):
			refs.append(VPX_OBJ_SOURCE)
		if entry.get("projection") or entry.get("drawing"):
			refs.append(MANUAL_SOURCE)
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			"provenance": provenance("observed", *refs),
		})
	return {"status": "observed", "placements": placements}


MESH_PART = {"KabeSockel": "socket", "WarriorBugAssembly006": "bulb", "bulbs_red": "bulb", "bulbs_yellow": "bulb", "bulbs_blue": "bulb"}


def seed_tool_inserts() -> list[int]:
	"""The lamps the placement seed projects onto their insert lights."""
	return sorted(
		int(address) for address, entries in _spatial_seed()["lamp"].items()
		if any(entry["type"] == "Light" and entry.get("projection") for entry in entries)
	)


def _mesh_note(entry: dict[str, Any]) -> str:
	anchor = next(mesh for mesh in entry["mesh"] if mesh["object"] == entry["anchor"])
	text = (
		f"the point is the centre of the {anchor['object']} {MESH_PART.get(anchor['object'], 'dome')} piece the Light sits on in the "
		f"world-space mesh export, {anchor['height'][0]:g}-{anchor['height'][1]:g} VPU above the playfield and {anchor['distance']:g} VPU "
		"from the Light"
	)
	for mesh in entry["mesh"]:
		if mesh is not anchor:
			text += (
				f"; the Light also sits on the {mesh['object']} {MESH_PART.get(mesh['object'], 'dome')} piece, "
				f"{mesh['height'][0]:g}-{mesh['height'][1]:g} VPU above the playfield, whose centre is {mesh['distance']:g} VPU from it"
			)
	return text


def _placement_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	parts = []
	for entry in entries:
		text = f"{entry['type']} {entry['object']}"
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		if entry.get("note"):
			text += f" ({entry['note']})"
		if entry.get("segment"):
			segment = entry["segment"]
			text += f" (the lit centroid of its segment texture {segment['image']}, at u {segment['u']:g} and v {segment['v']:g} of the Flasher's quad)"
		if entry.get("drawing"):
			text += f" ({entry['drawing']})"
		if entry.get("mesh"):
			text += f" ({_mesh_note(entry)})"
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


def _switch_aliases(address: int) -> list[dict[str, str]]:
	return [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}] + legacy_aliases("vpe-legacy.switch", address, LEGACY_SWITCHES)


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	identifier = switch_id(address)
	aliases = _switch_aliases(address)
	notes = f"Printed switch-matrix drive column {column + 1}, return row {row + 1}."
	if address in UNUSED_SWITCHES:
		notes += (
			" The Switch Matrix Grid (DR. 4) and the printed page-21 table print this cell NOT USED, shaded, with no part number; "
			"page 21 lists it under 'The following switches are not used: 1 8 11 36 44 63 64', the location drawing (DR. 5) marks no "
			"switch with this number, and the retained script never writes it."
		)
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=aliases, normally_closed=False, pulse=False, physical={"notes": notes}, wiring=_switch_wiring(address),
			spatial=not_applicable("unused", MANUAL_SOURCE),
		)
	label, printed, part, switch_type, availability, roles, pulse = SWITCHES[address]
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": switch_type}
	if address == 35:
		physical["part_number"] = "180-5133-00"
	elif re.fullmatch(r"\d{3}-\d{4}-\d{2}", part):
		physical["assembly_part_number" if part.startswith("500-") else "part_number"] = part
	notes += f' The grid prints "{printed}"; the page-21 table gives part "{part}"'
	notes += f' and describes it as "{PAGE21_NAMES[address]}".' if address in PAGE21_NAMES else "."
	if address in DOTS_SWITCHES:
		notes += " Both tables tag the switch DOTS (diode on terminal strip)."
	if address in CABINET_SWITCHES:
		notes += " The page-21 note lists 2, 4, 5, 6, 55 and 56 as switches located in the cabinet, not drawn on the playfield diagram."
	elif address in ABOVE_PLAYFIELD:
		notes += " The location drawing (DR. 5) draws it in a white box: mounted above the playfield."
	else:
		notes += " The location drawing (DR. 5) draws it in a black box: mounted below the playfield."
	if address in (12, 13, 14):
		notes += (
			" One of the three Submini-Switch Roller Actuators (180-5119-00) of the 4-Ball Trough (OPTO) Assembly 500-6119-24 (printed "
			"page 71), whose Take Note 1 reads: 'Ball Position (1) is determined by the OPTO Switch; therefore, a 4-Ball Trough, requires "
			"only 3 Submini-Switch Roller Actuators.'"
		)
	if address == 15:
		notes += (
			" The trough's ball position 1, at the up-kicker, on the Trough Up-Kicker OPTO boards (transmitter 520-5124-00, receiver "
			"520-5125-00). Whitestar's switch_r hands the CPU ~core_getSwCol and the driver's invSw is zero, so public 1 is the CPU's "
			"closed-contact reading. The opto boards' theory of operation (printed page 95) states the construction: with light on the "
			"receiver its output transistor is off and 'acts as an OPEN SWITCH'; when the light is blocked it conducts and 'acts as a "
			"CLOSED SWITCH', so the contact rests open and a ball at the up-kicker reads 1."
		)
	if address in (47, 48):
		side = "left" if address == 47 else "right"
		notes += (
			f" One pair of the Playfield Sw. OPTO 'Long-Hop' boards (transmitter 520-5082-00, receiver 520-5083-01), whose page (printed page "
			f"97) notes: '1 Pair are used for Switch {address}, {side.capitalize()} Orbit (GRN-BLU, {'WHT-VIO' if address == 47 else 'WHT-GRY'})'. "
			"Its theory text says the receiver's comparator drives Q1 'and makes the switch' while light falls on the receiver LED, which read "
			"alone would make the contact rest closed. The board page prints no matrix rest state, so the record derives it as the Whitestar "
			"rule in docs/PLATFORMS.md requires, from the read path and a runtime proof: se.c's switch_r hands the CPU ~core_getSwCol with a "
			"zero invSw, so public 1 is the CPU's closed-contact reading; the known-working script holds this address at 1 while the ball "
			"passes; and in both gameplay runs the ROM answered a 100 ms 1 pulse while the input was still 1, the right magnet Q6 rising "
			"46-100 ms after the write. An input the script and the ROM treat as active at 1 has a matrix contact that rests open, so "
			"normally_closed is false."
		)
	if address in (9, 10, 40):
		notes += (
			" A Micro Switch (High Form) 180-5057-00 under the playfield. The ball-path callouts (printed pages 7 and 9) send the ball from the "
			"top exit hole and the warrior bug's exit hole into the Under-Trough, and from the pop exit hole into the Mini-Under-Trough, both "
			"leading to the super VUK; the bottom view (printed page 10) lists the 'Plastic Trough' and the 'Metal Mini-Trough' among the "
			"bottom-mounted assemblies and labels the long Plastic Trough and the short Mini-Trough beside it. The "
			"Plastic Under-Trough Assembly 500-6244-00-59 (printed page 83) lists two of these switches (item 4, Qty. 2) with two 1N4001 "
			"diodes; the Metal Under-Trough (Small VUK) Assembly 500-6243-00-59 (printed page 82) lists one (item 4, Qty. 1), its diode on a "
			"terminal strip. "
			+ ("This is one of the plastic under-trough's two switches." if address in (9, 10) else "This is the metal mini-under-trough's single switch.")
		)
	if address == 16:
		notes += (
			" The page-21 part cell names the switch assembly 500-5096-00, and no assembly page in the manual lists its contact, so the "
			"switch type is not recorded."
		)
	if address in (33, 34):
		notes += (
			" One of the two Micro Switches (Roller Actuator) 180-5119-00 of the Warrior Bug Assembly 500-6239-00-59 (printed pages 78-79), "
			f"which sense the bug carriage at the {'rear' if address == 33 else 'front'} end of its stepper-driven travel. The warrior bug "
			"page's Note 2: 'The Switch Diode, 1N4001, (Qty. 3), 2-Micro Switches & 1-S-U Target are not located on this assembly (nor "
			"included); all 3 are located on a terminal strip under the playfield.'"
		)
	if address == 35:
		notes += (
			" The page-21 part cell prints 180-5119-00 once beside 33, 34 and 35, but the Warrior Bug Assembly's Warrior Bug Target "
			"Sub-Assembly 515-6776-08-59 carries 'Sw. & Target 1\"×1-1/2\" Rect. Wht 515-6027-08' with '(a) Stack Switch (Radius End) "
			"180-5133-00': the target rides the moving bug carriage. The shared cell is repeated beside a stand-up target, and the record "
			"follows the assembly page's own part."
		)
	if address in (37, 38, 39):
		notes += (
			" One of the three Limit Switches (Cherry #E33-90N) 180-5165-00 of the Brain Bug Assembly 500-6256-00-59 (printed pages 76-77), "
			"which lists two switch diodes for the three switches."
		)
	if address in (37, 39):
		notes += (
			" The grid prints BRAIN BUG UP for both 37 and 39; no source gives the two a different name, and both report the brain bug raised."
		)
	if address == 45:
		notes += " The VUK Assembly 500-5839-04 (printed page 75) carries this Micro Switch (Heavy Duty \"Y\" Actuator) 180-5116-01."
	if address == 46:
		notes += (
			" The Super VUK Assembly 500-6245-02-59 (printed page 76) carries this Micro Switch 180-5052-00 on its SVUK Switch Bracket; "
			"its note: 'The Switch Diode, 1N4001, is not located on this assembly (nor included); it's located on a terminal strip under "
			"the playfield.'"
		)
	if address == 26:
		notes += " The Wire Ramp Assembly 500-6248-00-59 (printed page 82) carries this Micro Switch 180-5093-00 on the left ramp's wire exit."
	if address == 49:
		notes += (
			" The page-21 table describes this row as TOP TURBO BUMPER and prints its row cell as '4' (the grid places it in row 1), and the "
			"location drawing puts 49 at the top bumper of the three. The grid's LEFT and the coil chart's LEFT TURBO BUMPER (Q9) name the same "
			"top bumper; the record keeps the grid's name."
		)
	if address in (3, 7):
		notes += " The part cell reads (Future Use): the coin-door harness position is wired but no coin switch is fitted by default."
	if address == 2:
		notes += " The cabinet wiring diagram (printed page 94) labels this input '4th Coin Slot European Use'."
	if address == 5:
		notes += " The cabinet wiring diagram labels it 'U.S. Bill Acceptor Center Coin Slot'."
	if address == 55:
		notes += " sega.vbs's swSlamTilt = 55 is the key the VPinMAME Slam Tilt key writes; the cabinet wiring diagram draws it on drive 7, return 7."
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 56:
		notes += " sega.vbs's swTilt = 56; the retained script sets vpmNudge.TiltSwitch = 56 (line 269)."
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
	if address == 54:
		notes += (
			" sega.vbs's swStartButton = 54 is what the VPinMAME Start key writes. In the gameplay runs a press after four coins started a "
			"game: the ROM kicked the trough up-kicker (1) and flashed F8 (32)."
		)
		refs += (VPM_LIBRARY_SOURCE,) + BOTH_RUNS
	if address in (4, 5, 6):
		notes += f" sega.vbs maps its coin keys to {'swCoin3 = 4' if address == 4 else 'swCoin1 = 5' if address == 5 else 'swCoin2 = 6'}."
		refs += (VPM_LIBRARY_SOURCE,)
	if address == 5:
		notes += " In the gameplay runs each of four coins on 5 pulsed the optional coin-meter output 24, flashed F1-F4 (25-28) and blinked the G.I."
		refs += BOTH_RUNS
	if address in SWITCH_SCRIPT:
		notes += f" Retained table script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in (59, 62):
		notes += (
			" The crossing is a defect of the retained table, not of the machine: the location drawing draws 59 at the left slingshot and 62 "
			"at the right, the coil chart pairs them with Q12 (left) and Q13 (right), and in the gameplay runs each switch fired its own side's "
			"coil. The table's slingshot walls kick on their own, so play looks right while the ROM scores the wrong side. The record follows "
			"the manual and the ROM, and the placement follows the manual."
		)
	if address in GAMEPLAY_RESPONSE:
		notes += f" In the gameplay harness runs, {GAMEPLAY_RESPONSE[address]}."
		refs += BOTH_RUNS
	elif address in GAMEPLAY_QUIET:
		notes += " The gameplay harness runs closed it once in a game and the ROM fired no coil or flasher in response, which says nothing against its fitment."
		refs += BOTH_RUNS
	extra: dict[str, Any] = {"aliases": aliases, "normally_closed": False, "pulse": pulse, "wiring": _switch_wiring(address)}
	if roles:
		extra["roles"] = list(roles)
	if address in (12, 13, 14, 15):
		extra["initial_active"] = True
	if address in CABINET_SWITCHES:
		physical["location"] = "cabinet" if address in (54, 56) else "coin door"
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	if address in LEGACY_SWITCHES:
		refs += (LEGACY_SOURCE,)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, availability, refs, physical=physical, **extra)


# address -> (label, printed, wire, connector, location, part, roles, normally_closed)
DEDICATED = {
	-3: ("Coin Door Memory Protect", "Memory Protect Switch", "BLK-RED", "CN6-P12", "coin door", None, ("cabinet.memory-protect",), False),
	-2: ("Volume / Service Left (Red)", "#6 VOLUME (RED BUTTON) (Normal) (In Test: LEFT)", "GRY-BLU", "CN6-P8", "coin door", None, ("service.left",), False),
	-1: ("Service Credit / Service Right (Green)", "#7 SERV. CRED. (GREEN BUTTON) (In Test: RIGHT)", "GRY-VIO", "CN6-P9", "coin door", None, ("service.right",), False),
	0: ("Begin Test / Service Enter (Black)", "#8 BEGIN TEST (BLACK BUTTON) (In Test: ENTER)", "GRY-BLK", "CN6-P10", "coin door", None, ("service.enter",), False),
	81: ("Right Flipper End-of-Stroke", "#4 RIGHT FLIPPER E.O.S.", "GRY-YEL", "CN6-P6", "playfield", "180-5149-00", ("flipper.lower.right.eos",), True),
	82: ("Right Flipper Button", "#3 RIGHT FLIPPER BUTTON", "GRY-ORG", "CN6-P4", "cabinet", None, ("flipper.lower.right.button",), False),
	83: ("Left Flipper End-of-Stroke", "#2 LEFT FLIPPER E.O.S (End-of-Stroke)", "GRY-RED", "CN6-P3", "playfield", "180-5149-00", ("flipper.lower.left.eos",), True),
	84: ("Left Flipper Button", "#1 LEFT FLIPPER BUTTON", "GRY-BRN", "CN6-P2", "cabinet", None, ("flipper.lower.left.button",), False),
	88: ("Mini Flipper Button", "#5 MINI FLIPPER BUTTON", "GRY-GRN", "CN6-P7", "cabinet", None, ("flipper.mini.right.button",), False),
}
DEDICATED_INPUT = {-2: "DS-6", -1: "DS-7", 0: "DS-8", 81: "DS-4", 82: "DS-3", 83: "DS-2", 84: "DS-1", 88: "DS-5"}


def _dedicated(address: int) -> dict[str, Any]:
	label, printed, wire, connector, location, part, roles, normally_closed = DEDICATED[address]
	name = f"n{-address}" if address < 0 else str(address)
	identifier = f"switch.{name}-{slug(label)}"
	aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
	if address in DEDICATED_INPUT:
		aliases.append({"namespace": "manual.address", "value": DEDICATED_INPUT[address]})
	aliases += legacy_aliases("vpe-legacy.switch", address, LEGACY_SWITCHES)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {"switch_type": "leaf" if address in (81, 83) else "button" if address != -3 else "microswitch", "location": location}
	if part:
		physical["part_number"] = part
	if address == -3:
		notes = (
			"The cabinet/coin door wiring diagram (printed page 94) draws the Memory Protect Switch from CPU board CN6 pin 12 (BLK-RED) "
			"to ground. se.c's ram_w refuses writes to the protected RAM while public -3 is 1, and sega.vbs names the address "
			"swMemoryProtect; a closed coin door is public -3 at 1 and an open door 0."
		)
		refs += (VPM_LIBRARY_SOURCE,)
		extra: dict[str, Any] = {"initial_active": True, "wiring": {"board": "Whitestar CPU/Sound board memory-protect input", "drive_wire": wire, "drive_connection": connector}}
	else:
		notes = (
			f"Printed dedicated switch {DEDICATED_INPUT[address]} ({printed}), wired {wire} to {connector} on IC U206's inputs and returned "
			"to ground (BLK, CN6-P1/-P11). se.c's dedswitch_r swaps PinMAME's flipper column into U206's order and returns the complement, "
			"so public 1 is a closed contact."
		)
		extra = {"wiring": {"board": "Whitestar CPU/Sound board dedicated-switch input", "drive_wire": wire, "drive_connection": connector, "return_wire": "BLK", "return_connection": "CN6-P1/-P11", "return_component": "U206"}}
	if address in (-2, -1, 0):
		notes += " The cabinet wiring diagram draws it among the PORTALS™ SERVICE BUTTONS on the coin door."
	if address in (81, 83):
		notes += (
			" The 3-Flipper Circuit Wiring Diagram (printed page 92) prints the E.O.S. as an N.C. switch on the flipper assembly (Power (End of "
			"Stroke) Switch 180-5149-00 on Flipper Assemblies 500-5944-14 left and 500-5944-04 right) and explains that it opens about 1/16\" "
			"when the flipper is energized; the CPU re-pulses the coil (40 ms) when it sees the switch close again during a hold, because a "
			"shot forced the bat back. normally_closed is that construction: at rest the contact is closed (public 1) and it opens (public 0) "
			"at the end of the stroke. PinMAME does not take this input from the host: the driver declares FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), "
			"and core.h's FLIP_SOL includes FLIP_EOS, so core_updateSw puts both lower EOS bits in its flipper-column mask and rewrites this "
			f"one on every update from the {'right' if address == 81 else 'left'} flipper output: it publishes 1 once core_getSol({46 if address == 81 else 48}) "
			"has been on for CORE_FLIPSTROKETIME (two updates) and 0 otherwise (core.c lines 1848-1870). A host write is overwritten, so a "
			"recreation does not drive it, and the published level is PinMAME's stroke model, not the contact: dedswitch_r hands the ROM a "
			"closed contact while the coil is held, where the real N.C. contact is open. The retained script never writes it, which is right; "
			"sega.vbs names this address swURFlip/swULFlip, an upper-flipper label it writes only when an upper flipper "
			"solenoid is registered, which this table does not do."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE,)
	elif address in (82, 84):
		notes += (
			f" The ROM reads it through se.c's dedswitch_r and drives the {'right' if address == 82 else 'left'} flipper itself: "
			f"se_solenoid_w moves {'Q16' if address == 82 else 'Q15'} to the power address {45 if address == 82 else 47}, and core_getSol "
			f"reports the canonical {46 if address == 82 else 48} whenever that power bit is set. Because the driver declares FLIP_SOL(FLIP_L), "
			"core_updateSw fakes no flipper output from this button. sega.vbs writes it from the "
			f"{'right' if address == 82 else 'left'} flipper key (swLRFlip = 82, swLLFlip = 84). In the gameplay harness runs, holding it "
			f"made the ROM pulse {'45 and 46' if address == 82 else '47 and 48'}."
		)
		if address == 82:
			notes += (
				" During that step the ROM also fired 2, 7, 14, 9, 6, 10, 3, 11, 5, 12, 13 and 4 one at a time, about a quarter second "
				"apart, and went on after the button was released: a ball search for the ball last seen leaving the super VUK, not a "
				"response to the button."
			)
		refs += (VPM_LIBRARY_SOURCE,) + BOTH_RUNS
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	elif address == 88:
		notes += (
			" se.c's dedswitch_r carries the flipper column's top bit, PinMAME's upper-flipper button, to U206 input 5 (D4, commented 'Not "
			"Used (Upper Flipper on some games!)'), so public 88 is DS-5. The cabinet and 3-flipper wiring diagrams draw it as the N.O. MINI "
			"FLIPPER CABINET SWITCH, a cabinet button of its own beside the right flipper button. The driver declares lower flippers only "
			"(FLIP_SW(FLIP_L)), so core_updateSw never drives a coil from it: the ROM reads it and fires the mini flipper Q14 itself, and "
			"the 3-flipper page draws no end-of-stroke switch for the mini flipper. sega.vbs has no constant for 88; the retained script "
			"writes it from its own RightMagnaSave/LockbarKey handler (lines 474-480 and 517-519). In the gameplay harness runs holding it "
			"made the ROM pulse 14."
		)
		refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE) + BOTH_RUNS
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	if address in LEGACY_SWITCHES:
		refs += (LEGACY_SOURCE,)
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, "used", refs, aliases=aliases, normally_closed=normally_closed,
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
	items.append(_dedicated(88))
	for number in range(1, 9):
		used = number <= 5
		items.append(_device(
			f"switch.dip-{number}", f"SW300 Country Selector Bit {number}" if used else f"Unused DIP Bit {number}", "dip_switch", DIP_GROUP, number,
			"used" if used else "unused", (CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": str(number)}],
			physical={"switch_type": "dip", "location": "Whitestar CPU/Sound board", "notes": (
				"se.c's dip_r ('Dip Switch SW300 - Country Settings') returns the complement of PinMAME DIP bank 0, and se.h's SE_COMPORTS "
				"declares 'Dip SW300' as a five-bit country selector (COREPORT_DIPNAME 0x001f, USA 0x0000, Austria 0x0001 and so on); sega.vbs's "
				"DIP form sets the older country codes in mask 0x0f." if used else
				"se.h's SE_COMPORTS declares the country selector in bits 1-5 only (mask 0x001f); this bit is padding in the eight-address public "
				"DIP bank that nothing in PinMAME or the VPinMAME library sets."
			)},
			spatial=not_applicable("dip_switch", CORE_SOURCE),
		))
	return items


# --- Solenoid data -------------------------------------------------------------------------------------
# Q number -> (label, printed name, kind, availability, coil/bulb cell, power wire, power connection, voltage, control wire, control connection)
YV = ("YEL-VIO", "J10-P4/5", 50)
VY = ("VIO-YEL", "J10-P3", 50)
OR = ("ORG", "J6-P10", 20)
ST = ("GRY-RED", "J16-P3", 12)
Q_OUTPUTS: dict[int, tuple[str, str, str, str, str, str, str, int, str, str]] = {
	1: ("Trough Up-Kicker", "TROUGH UP-KICKER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-BLK", "J8-P1"),
	2: ("Auto Launch", "AUTO LAUNCH", "coil", "used", "24-940 / 090-5036-00T", *YV, "BRN-RED", "J8-P3"),
	3: ("VUK", "VUK", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-ORG", "J8-P4"),
	4: ("Super VUK", "SUPER VUK", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BRN-YEL", "J8-P5"),
	5: ("Left Magnet", "LEFT MAGNET", "magnet", "used", "22-650 / 090-5042-01", *VY, "BRN-GRN", "J8-P6"),
	6: ("Right Magnet", "RIGHT MAGNET", "magnet", "used", "22-650 / 090-5042-01", *VY, "BRN-BLU", "J8-P7"),
	7: ("Brain Bug", "BRAIN BUG", "coil", "used", "22-1080 / 090-5032-00T", "VIO-YEL / RED-WHT", "J10-P3", 50, "BRN-VIO", "J8-P8"),
	8: ("European Token Dispenser", "EUROPEAN TOKEN DISPENSER", "coil", "optional", "N/A", *YV, "BRN-GRY", "J8-P9"),
	9: ("Left Turbo Bumper", "LEFT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-BRN", "J9-P1"),
	10: ("Bottom Turbo Bumper", "BOTTOM TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-RED", "J9-P2"),
	11: ("Right Turbo Bumper", "RIGHT TURBO BUMPER", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-ORG", "J9-P4"),
	12: ("Left Slingshot", "LEFT SLINGSHOT", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-YEL", "J9-P5"),
	13: ("Right Slingshot", "RIGHT SLINGSHOT", "coil", "used", "26-1200 / 090-5044-00T", *YV, "BLU-GRN", "J9-P6"),
	14: ("Mini Flipper", "MINI FLIPPER", "coil", "used", "22-1080 / 090-5032-00T", "RED-YEL / BLU-YEL", "J10-P1/2", 50, "BLU-BLK", "J9-P7"),
	15: ("Left Flipper", "LEFT FLIPPER (50v RED/YEL)", "coil", "used", "23-1100 / 090-5030-00T", "RED-YEL / GRY-YEL", "J10-P1/2", 50, "ORG-GRY", "J9-P8"),
	16: ("Right Flipper", "RIGHT FLIPPER (50v RED/YEL)", "coil", "used", "23-1100 / 090-5030-00T", "RED-YEL / BLU-YEL", "J10-P1/2", 50, "ORG-VIO", "J9-P9"),
	17: ("Stepper Motor Phase 1", "STEPPER MOTOR #1", "motor", "used", "Step.Motor / 041-5062-00", *ST, "VIO-BRN", "J7-P2"),
	18: ("Stepper Motor Phase 2", "STEPPER MOTOR #2", "motor", "used", "Step.Motor / 041-5062-00", *ST, "VIO-RED", "J7-P3"),
	19: ("Stepper Motor Phase 3", "STEPPER MOTOR #3", "motor", "used", "Step.Motor / 041-5062-00", *ST, "VIO-ORG", "J7-P4"),
	20: ("Stepper Motor Phase 4", "STEPPER MOTOR #4", "motor", "used", "Step.Motor / 041-5062-00", *ST, "VIO-YEL", "J7-P6"),
	23: ("Brain Bug Flashers (X2)", "FLASH BRAIN BUG ✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "VIO-BLK", "J7-P9"),
	24: ("Optional Coin Meter", "OPTIONAL COIN METER", "coil", "optional", "5v Meter / (If Required)", "RED", "J16-P7", 5, "VIO-GRY", "J7-P10"),
	25: ("F1 Red Flashers (X4)", "#F1 FLASH RED✻4", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-BRN", "J6-P1"),
	26: ("F2 Yellow Flashers (X4)", "#F2 FLASH YELLOW✻4", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-RED", "J6-P2"),
	27: ("F3 Green Flashers (X4)", "#F3 FLASH GREEN✻4", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-ORG", "J6-P3"),
	28: ("F4 Blue Flashers (X4)", "#F4 FLASH BLUE✻4", "flasher", "used", "#906 Bulb / 165-5004-00", *OR, "BLK-YEL", "J6-P4"),
	29: ("F5 Multiball Flashers (X4)", "#F5 FLASH MULTIBALL✻4", "flasher", "used", "#906 Bulb† / 165-5004-00", *OR, "BLK-GRN", "J6-P5"),
	30: ("F6 Left Ramp Flashers (X4)", "#F6 FLASH LT RAMP✻4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-BLU", "J6-P6"),
	31: ("F7 Right Ramp Flashers (X4)", "#F7 FLASH RT RAMP✻4", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-VIO", "J6-P7"),
	32: ("F8 Pop Flashers (X2)", "#F8 FLASH POPS✻2", "flasher", "used", "#89 Bulb / 165-5000-89", *OR, "BLK-GRY", "J6-P8"),
}
# The two NOT USED rows: Q number -> control wire, control connection.
UNUSED_Q = {21: ("VIO-GRN", "J7-P7"), 22: ("VIO-BLU", "J7-P8")}
PUBLIC_BINDING = {15: 48, 16: 46}
# What the retained table does with each callback (embedded script line numbers).
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"SolRelease\": bsTrough.ExitSol_On while balls remain (lines 606, 641-643)",
	2: "SolCallback(2) = \"SolAutolaunch\": fires the table's Plunger with Autoplunger set (lines 607, 648-654)",
	3: "SolCallback(3) = \"SolLeftVuk\": ejects the VUK saucer bsLeftVUK on 45 and animates the vuk_kicker primitive (lines 609, 665-668)",
	4: "SolCallback(4) = \"bsSupervuk.SolOut\": ejects the super-VUK ball stack on 46 (line 610)",
	5: "SolCallback(5) = \"SolLeftMagnet\" only plays a sound (lines 611, 889); the cvpmMagnet mLeftMagnet on the trigger LeftMagnet takes .Solenoid = 5 and holds the ball itself (lines 303-309)",
	6: "SolCallback(6) = \"SolRightMagnet\" only plays a sound (lines 612, 890); the cvpmMagnet mRightMagnet on the trigger RightMagnet takes .Solenoid = 6 (lines 311-317)",
	7: "SolCallBack(7) = \"SolBrainBug\": rotates BrainBugFlipper up, raises the walls sw38 and sw38a and sets 37 and 39 while energized, and lowers them all when it drops, after kicking any ball inside its region away (lines 613, 695-720)",
	8: "SolCallBack(8) = \"SolKnocker\" plays the table's knocker sound (lines 614, 633, 3421)",
	9: "Bumper1 is a VPX bumper that fires itself; no callback",
	10: "Bumper3 is a VPX bumper that fires itself; no callback",
	11: "Bumper2 is a VPX bumper that fires itself; no callback",
	12: "the slingshot walls fire themselves; no callback",
	13: "the slingshot walls fire themselves; no callback",
	14: "SolCallback(14) is commented out; the table fires its RightFlipperS through SolRFlipperS (line 947) from its own mini-flipper key handler, gated by the game-on state 15, instead of from Q14",
	17: "the cvpmMyMech mBug takes .Sol1 = 17 with vpmMechStepSol + vpmMechTwoDirSol, 222 steps, and moves the WarriorBugGroup primitives and the BWalls through UpdateWarriorBug (lines 320-331, 775-788)",
	23: "SolCallBack(23) = \"SetLamp 123,\" lights l123a and l123b (lines 616, 1711-1712)",
	25: "SolCallBack(25) = \"Sol25\" blinks the red dome lights of StrobeFlashersLRed (l125a-l125d) and their overlays (lines 617, 627)",
	26: "SolCallBack(26) = \"Sol26\" blinks StrobeFlashersLYellow (l126a-l126d) (lines 618, 628)",
	27: "SolCallBack(27) = \"Sol27\" blinks StrobeFlashersLGreen (l127a-l127d) (lines 619, 629)",
	28: "SolCallBack(28) = \"Sol28\" blinks StrobeFlashersLBlue (l128a-l128d) (lines 620, 630)",
	29: "SolCallBack(29) = \"SetLamp 129,\" ('F5 WarBugSled Flasher X4') lights l129, l129a, l129b and the flasher lf129 and its overlays (lines 621, 1715-1720)",
	30: "SolCallBack(30) = \"SetLamp 130,\" ('F6 Left Ramp Flasher X4') lights l130b-l130e and the flashers f130a-f130d (lines 622, 1724-1731)",
	31: "SolCallBack(31) = \"SetLamp 131,\" ('F7 Right Ramp Flasher X4') lights l131b-l131e and f131a-f131d (lines 623, 1734-1741)",
	32: "SolCallBack(32) = \"SetLamp 132,\" ('F8 Pop Bumpers Flasher X2') lights l132 and lf132 (lines 624, 1743-1744)",
}
# What the harness runs showed for each output (evidence step labels).
SOLENOID_RUNTIME = {
	1: "the ROM fired it on Start and again at the drain",
	3: "a ball held on the VUK (45) drew its kicks",
	4: "a ball held on the super VUK (46) drew its kicks, and a ball held on the VUK drew one more",
	6: "each orbit opto, 47 and 48, fired it twice: a hold of 0.60-0.67 s rising 46-100 ms after the 0-to-1 write, while the input was still 1, and a 66-133 ms pulse about 2.1 s after the write",
	9: "it answered the left turbo bumper switch (49)",
	10: "it answered the bottom turbo bumper switch (50)",
	11: "it answered the right turbo bumper switch (51)",
	12: "it answered the left slingshot switch (59)",
	13: "it answered the right slingshot switch (62)",
	14: "holding the mini flipper button (88) pulsed it",
	24: "each coin on the center slot (5) pulsed it",
	25: "it flashed with each coin, from the right ramp stand-up (32) and at the drain",
	26: "it flashed with each coin, from the yellow stand-ups (18, 20, 22, 24, 27), the right ramp stand-up (32), the bug hole (10) and at the drain",
	27: "it flashed with each coin, from the green stand-ups (17, 23, 29), the right ramp stand-up (32), the bug hole (10), the VUK (45) and at the drain",
	28: "it flashed with each coin, from the right ramp stand-up (32) and at the drain",
	29: "it flashed from the warrior bug target (35) and the bug hole (10)",
	30: "it flashed from the left outlane (57) and the VUK (45)",
	31: "it flashed from the right outlane (60)",
	32: "it flashed on Start, from the right top lane (43), the right ramp stand-up (32), the VUK and the super VUK, and at the drain",
}
SEARCH_ONLY = (2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14)
SOLENOID_NOT_SEEN = {
	2: "No harness run provoked an auto launch outside the ball search.",
	5: "No harness run fired the left magnet outside the ball search.",
	7: "No harness run raised the brain bug outside the ball search, so 37 and 39 were never exercised.",
	8: "No harness run fired it.",
	23: "No harness run fired it.",
}
FLASHER_LOCATIONS = {
	23: "two bulbs either side of the brain bug picture at the centre",
	25: "one #906 under each of the four flash domes of colour red, in the four dome groups at the top left, top right, left side and right side",
	26: "one #906 under each yellow dome of the four dome groups", 27: "one #906 under each green dome of the four dome groups",
	28: "one #906 under each blue dome of the four dome groups",
	29: "three #906 on the warrior bug track and one #89 at its head",
	30: "three down the left ramp and one at the lower left of the centre inserts",
	31: "three down the right side of the upper playfield and one at the lower right of the centre inserts",
	32: "two at the pop bumpers",
}
FLASHER_QUANTITY = {23: 2, 25: 4, 26: 4, 27: 4, 28: 4, 29: 4, 30: 4, 31: 4, 32: 2}


def q_output_id(number: int) -> str:
	if number in UNUSED_Q:
		return f"device.q{number}-not-used"
	return f"device.q{number}-{slug(Q_OUTPUTS[number][0])}"


def _q_wiring(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	return {
		"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire,
		"control_connection": control_connection, "power_wire": power_wire, "power_connection": power_connection,
		"nominal_voltage_v": voltage, "voltage_type": "dc",
	}


def _solenoid_aliases(address: int, number: int) -> list[dict[str, str]]:
	aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Q{number}"}]
	aliases += legacy_aliases("vpe-legacy.coil", address, LEGACY_COILS)
	if address in LEGACY_COIL_NAMES:
		aliases.append({"namespace": "vpe-legacy.coil", "value": LEGACY_COIL_NAMES[address]})
	if address in LEGACY_LAMP_ON_SOLENOID:
		aliases += legacy_aliases("vpe-legacy.lamp", LEGACY_LAMP_ON_SOLENOID[address], LEGACY_LAMPS)
	return aliases


def _q_output(number: int) -> dict[str, Any]:
	label, printed, kind, availability, part, power_wire, power_connection, voltage, control_wire, control_connection = Q_OUTPUTS[number]
	address = PUBLIC_BINDING.get(number, number)
	identifier = q_output_id(number)
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	physical: dict[str, Any] = {}
	coil_part = part.split(" / ")[-1].split(" ")[0]
	if number != 29 and re.fullmatch(r"\d{3}-\d{4}-\d{2}[A-Z]?(-\d{2})?", coil_part):
		physical["part_number"] = coil_part
	notes = f'Coils Detailed Chart Table (DR. 6) row #{f"{number:02d}" if number <= 24 else f"F{number - 24}"} "{printed}": drive transistor Q{number}, cell "{part}".'
	if number in FLASHER_LOCATIONS:
		physical["location"] = FLASHER_LOCATIONS[number]
	if number in FLASHER_QUANTITY:
		physical["quantity"] = FLASHER_QUANTITY[number]
	if number == 4:
		notes += (
			" The chart prints the control colour BRY-YEL; every other high-current row of the J8 group uses BRN-, the pin sequence puts BRN-YEL "
			"here, and the Backbox I/O Power Driver Board Detailed Wiring Diagram (printed page 88) prints BRN/YEL on J8-5, so the record "
			"follows BRN-YEL."
		)
	if number == 7:
		notes += (
			" The power-colour cell prints VIO-YEL and RED-WHT over each other. The Backbox I/O Power Driver Board Detailed Wiring Diagram "
			"(printed page 88) separates them: the VIO/YEL 50V DC supply from J10-P3 feeds a 3A slow-blow fuse, and RED/WHT runs from that "
			"fuse to the coil, so the record keeps both segments, supply side first, as it does for the fused flipper branches. The diagram's "
			"note places the fuses of 5, 6 and 7 under the playfield by their assemblies. The Brain Bug Assembly 500-6256-00-59 (printed "
			"pages 76-77) carries this 22-1080 coil."
		)
	if number in (5, 6):
		notes += (
			" The associated parts of the Threaded Bushing Core Assembly 515-6142-00 (Qty. 2, printed page 84) list the Magnet Coil (22-650) "
			"090-5042-01 (Qty. 2); the coil location drawing (DR. 7) draws 5 and 6 side by side at the rear edge of the playfield, below it. "
			"The Backbox I/O Power Driver Board Detailed Wiring Diagram (printed page 88) feeds each magnet coil from the VIO/YEL 50V DC "
			"J10-P3 supply through its own 3A slow-blow fuse 'located under playfield by assembly'; on the board, bridge 1's 50V DC reaches "
			"that 'Magnet' J10-P3 output through the 3A slow-blow F20. "
			"The ball-path callouts (printed pages 6-7): a hard orbit shot with the magnet on deflects the ball down into the top exit hole "
			"(left) or the top lanes (right); with the magnet off it completes the orbit."
		)
	if number in (25, 26, 27, 28):
		notes += (
			" The flash lamp location drawing (DR. 7) draws four domes in each of four groups (top left, top right, left side and right "
			"side) and orders each group F1, F3, F2, F4. The Plastic Ramp Assembly's item 21, the 4X Light & Clear Plastic Assembly "
			"515-6778-01-59 (Qty. 3, printed page 81), carries four WB Offset (w/Step-Bracket) Sockets, four #906 Wedge Base Bulbs "
			"165-5004-00, one Mini-Mars Light Cover Snap-in each in blue, yellow, green and red, and the 'Fl. Lamp F1-F4 Cable Wiring "
			"Harness'; its note places a fourth such assembly over the wire ramp by the Hopper Bug. Each colour's four bulbs are therefore "
			"one under each of the four assemblies' domes. The Backbox I/O Power Driver Board Detailed Wiring Diagram (printed page 88) "
			"labels each F1-F4 group '#555 Bulb ✻4'; DR. 6 and the assembly's own parts list both give the #906 165-5004-00, and the record "
			"follows them."
		)
	if number == 29:
		notes += (
			" The chart's note reads 'F5 = 3✻ #906 Bulb + 1✻ #89 Bulb.', and the Backbox I/O Power Driver Board Detailed Wiring Diagram "
			"(printed page 88) labels the group '#89 + #906 Bulbs ✻1+✻3'. The four bulbs are three #906 (165-5004-00) and one #89 "
			"(165-5000-89), so the record gives the quantity and no single part number. The flash lamp location drawing draws F5 three times "
			"in white boxes on the warrior bug track and once in a black box with a bulb symbol at its head, and the Warrior Bug Assembly "
			"lists two #906 bulbs plus a screened plastic carrying one #906 and the #555 of lamp 34."
		)
	if number in (30, 31):
		notes += (
			f" The flash lamp location drawing draws {'F6' if number == 30 else 'F7'} three times in circles with bulb symbols down the "
			f"{'left ramp' if number == 30 else 'right side of the upper playfield'} and once more at the lower "
			f"{'left' if number == 30 else 'right'} of the centre inserts."
		)
	if number in (15, 16):
		side = "left" if number == 15 else "right"
		power = 47 if number == 15 else 45
		notes += (
			f" Physical Q{number} is removed from public {number}: se.c's se_solenoid_w masks it off and publishes it as the lower-{side} flipper "
			f"power bit {power}, and core.c synthesizes canonical callback {address} from it. Bind this one coil to public {address}, the retained "
			f"table's SolCallback(sL{'L' if number == 15 else 'R'}Flipper); public {power} is its power-phase state, not a second coil. The "
			"3-Flipper Circuit Wiring Diagram describes the drive: a 40 ms pulse on a button closure, then 1 ms every 12 ms while held, from one "
			f"50v supply through a 3A slow-blow fuse under the playfield ({'GRY-YEL' if number == 15 else 'BLU-YEL'}). Flipper "
			f"{'(Left) Assembly 500-5944-14' if number == 15 else '(Right) Assy. 500-5944-04'} (printed page {72 if number == 15 else 73})."
		)
		refs += (VPX_SCRIPT_SOURCE,) + BOTH_RUNS
	if number == 14:
		notes += (
			" The 3-Flipper Circuit Wiring Diagram draws it as the MINI FLIPPER COIL (22-1080) on the third 3A slow-blow fused BLU-YEL branch "
			"of the same 50v J10 supply, returning on BLU-BLK to Q14, with no wired end-of-stroke input; the Flipper (Mini-Right) Assy. "
			"500-5944-02 (printed page 73) carries the coil, and its heading's item range (Items 1-15 + 17) takes in item 9, the Power (End of "
			"Stroke) Switch 180-5149-00, which the circuit connects to no switch input. The driver declares lower flippers only, so PinMAME publishes Q14 at public 14 as the ROM "
			"drives it from the mini flipper button (88); there is no power-phase pair."
		)
		refs += BOTH_RUNS
	if number in (17, 18, 19, 20):
		notes += (
			f" Phase {number - 16} of the warrior bug's unipolar stepper: Appendix F (printed page 127) lists the Haydon Switch & Instrument "
			"Series 36000 HSI #36864-12, 15° per step, .004\" travel per step, 12v DC, 4.6W, on the HSI Stepper Motor Sub-Assembly "
			"515-6794-00-59 of the Warrior Bug Assembly. The chart prints a DOTS tag beside each phase's name and the power colour GRY/RED."
		)
	if number == 23:
		notes += " The flash lamp location drawing draws 23 twice, in circles with bulb symbols, either side of the brain bug picture."
	if number == 8:
		notes += (
			" The row is printed on a grey band and its coil cell reads N/A: the European token dispenser is optional equipment, not on a "
			"standard machine. The cabinet wiring diagram draws no knocker and the chart lists none. The retained script binds this callback "
			"to a knocker sound, a table defect that touches no physical device."
		)
		physical["location"] = "cabinet (token dispenser, when fitted)"
	if number == 24:
		notes += (
			" The row is printed on a grey band. The cabinet wiring diagram's TO COIN METER box routes Q24 (J7-10, 78 VIO/GRY) and +5VDC "
			"(J16-7, 22 RED) to the meter. No stock playfield device is fitted."
		)
		physical["location"] = "cabinet (coin meter, when fitted)"
	if number in SOLENOID_SCRIPT:
		notes += f" Retained table script: {SOLENOID_SCRIPT[number]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if number in SOLENOID_RUNTIME:
		notes += f" In the harness runs {SOLENOID_RUNTIME[number]}."
		refs += BOTH_RUNS
	if number in SEARCH_ONLY:
		notes += " The ball search both runs drew while the right flipper button was held fired it once in turn."
		refs += BOTH_RUNS
	if number in SOLENOID_NOT_SEEN:
		notes += f" {SOLENOID_NOT_SEEN[number]}"
		refs += BOTH_RUNS
	extra: dict[str, Any] = {"aliases": _solenoid_aliases(address, number), "wiring": _q_wiring(number)}
	role = "emitter" if kind == "flasher" else "effect"
	if number in (8, 24):
		extra["roles"] = ["cabinet.coin-meter"] if number == 24 else ["cabinet.token-dispenser"]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("solenoid", address, identifier, role)
		unplaced = _spatial_seed()["unplaced_solenoid_lights"].get(str(address))
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("solenoid", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif unplaced:
			notes += (
				f" No placement: the retained table's script drives the Light{'s' if len(unplaced) > 1 else ''} {', '.join(unplaced)} for this "
				"output, but the world-space mesh export shows no bulb, dome or socket under any of them, so they are render lights rather "
				"than sockets, and the flash lamp location drawing (DR. 7) has not been measured."
			)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, VPX_OBJ_SOURCE)
	if address in LEGACY_COILS or address in LEGACY_LAMP_ON_SOLENOID:
		refs += (LEGACY_SOURCE,)
	physical["notes"] = notes
	return _device(identifier, label, kind, SOLENOID_GROUP, address, availability, refs, physical=physical, **extra)


def _unused_q(number: int) -> dict[str, Any]:
	control_wire, control_connection = UNUSED_Q[number]
	return _device(
		q_output_id(number), f"Not Used Driver Q{number}", "coil", SOLENOID_GROUP, number, "unused", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE) + BOTH_RUNS,
		aliases=[{"namespace": "pinmame.solenoid", "value": str(number)}, {"namespace": "manual.address", "value": f"Q{number}"}],
		physical={"notes": (
			f"Coils Detailed Chart Table (DR. 6) row #{number} prints NOT USED on a grey band: drive transistor Q{number}, control "
			f"{control_wire} {control_connection}, power BRN with its connection and voltage cells N / C and the coil cell NOT USED. The coil "
			"location drawing draws no coil with this number, the retained script registers no callback for it, and neither harness run saw "
			"the address change."
		)},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01", "driver_transistor": f"Q{number}", "control_wire": control_wire, "control_connection": control_connection},
		spatial=not_applicable("unused", MANUAL_SOURCE),
	)


def solenoid_outputs() -> list[dict[str, Any]]:
	items = [_q_output(number) for number in Q_OUTPUTS]
	items.extend(_unused_q(number) for number in UNUSED_Q)
	items.append(_device(
		"virtual.15-fast-flip-game-on", "Whitestar Fast-Flip / Game-On State", "virtual", SOLENOID_GROUP, 15, "used",
		(CORE_SOURCE, CONTROLLER_SOURCE, VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE, LEGACY_SOURCE) + BOTH_RUNS,
		aliases=[{"namespace": "pinmame.solenoid", "value": "15"}] + legacy_aliases("vpe-legacy.coil", 15, LEGACY_COILS),
		physical={"notes": (
			"se.c sets public 15 while the ROM's fast-flip byte is non-zero, i.e. while the flippers are enabled in a game; MACHINE_INIT(se) "
			"places that byte at CPU RAM 0x00 for every driver whose name starts 'startrp', so both drivers publish it. sega.vbs declares "
			"GameOnSolenoid = 15, the retained table sets UseSolenoids = 15 (line 213) and SolCallBack(15) = \"FlippersEnabled=\" (line 615), "
			"which also gates its mini flipper. In both gameplay runs it rose when the served ball reached the shooter lane and fell at the "
			"drain. Physical Q15 is the left flipper at public 48; never wire this state to a transistor."
		)},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	items.append(_device(
		"virtual.16-remapped-flipper-hole", "Unused Remapped-Flipper Address 16", "virtual", SOLENOID_GROUP, 16, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
		aliases=[{"namespace": "pinmame.solenoid", "value": "16"}],
		physical={"notes": "se_solenoid_w masks physical Q16 off public 16 and publishes it at 45/46; nothing else drives 16."},
		spatial=not_applicable("virtual", CORE_SOURCE),
	))
	for address in range(33, 45):
		items.append(_device(
			f"virtual.{address}-reserved", f"Reserved Address {address}", "virtual", SOLENOID_GROUP, address, "unused", (CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": "A Whitestar compatibility hole: the driver declares no auxiliary board (INITGAME hw 0), and nothing in se.c drives it for this driver."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	for address, side, canonical, number in ((45, "right", 46, 16), (47, "left", 48, 15)):
		items.append(_device(
			f"virtual.{address}-{side}-flipper-power-phase", f"{side.capitalize()} Flipper Power-Phase State", "virtual", SOLENOID_GROUP, address, "used",
			(CORE_SOURCE, CONTROLLER_SOURCE) + BOTH_RUNS, aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			physical={"notes": (
				f"se_solenoid_w publishes physical Q{number}'s drive here and core.c synthesizes canonical {canonical} from it; one {side} flipper coil "
				f"is bound at {canonical}. In the gameplay runs, holding the {side} flipper button pulsed {address} and {canonical} together."
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
# address -> (label, grid name, bulb cell)
LAMPS: dict[int, tuple[str, str, str]] = {
	1: ("Antilles", "ANTILLES", "#555 Bulb"), 2: ("Zegema Beach", "ZEGEMA BEACH", "#555 Bulb"), 3: ("Dantana", "DANTANA", "#555 Bulb"),
	4: ("Tango Urilla", "TANGO URILLA", "#555 Bulb"), 5: ("Planet B", "PLANET B", "#555 Bulb"), 6: ("Klendathu", "KLENDATHU", "#555 Bulb"),
	7: ("Ball Saver", "BALL SAVER", "#555 Bulb"), 8: ("Starship (Hotdog)", "STARSHIP (HOTDOG)", "#555 Bulb"),
	9: ("Left Bottom Stand-Up (Green)", "LEFT BOTTOM S-U (GRN)", "#555 Bulb"), 10: ("Left Middle Stand-Up (Yellow)", "LEFT MIDDLE S-U (YEL)", "#555 Bulb"),
	11: ("Left Middle Stand-Up (Red)", "LEFT MIDDLE S-U (RED)", "#555 Bulb"), 12: ("Left Top Stand-Up (Yellow)", "LEFT TOP S-U (YEL)", "#555 Bulb"),
	13: ("Right Bottom Stand-Up (Red)", "RIGHT BOTTOM S-U (RED)", "#555 Bulb"), 14: ("Right Middle Stand-Up (Yellow)", "RIGHT MIDDLE S-U (YEL)", "#555 Bulb"),
	15: ("Right Middle Stand-Up (Green)", "RIGHT MIDDLE S-U (GRN)", "#555 Bulb"), 16: ("Right Top Stand-Up (Yellow)", "RIGHT TOP S-U (YEL)", "#555 Bulb"),
	17: ("Left Orbit \"Orbit\"", "LEFT ORBIT \"ORBIT\"", "#555 Bulb"), 18: ("Left Orbit Nuke", "LEFT ORBIT NUKE", "#555 Bulb"),
	19: ("Right Orbit \"Orbit\"", "RIGHT ORBIT \"ORBIT\"", "#555 Bulb"), 20: ("Right Orbit Nuke", "RIGHT ORBIT NUKE", "#555 Bulb"),
	21: ("Left Ramp Jackpot", "LEFT RAMP JACKPOT", "#555 Bulb"), 22: ("Left Ramp Starship", "LEFT RAMP STARSHIP", "#555 Bulb"),
	23: ("Right Ramp Jackpot", "RIGHT RAMP JACKPOT", "#555 Bulb"), 24: ("Right Ramp Trooper", "RIGHT RAMP TROOPER", "#555 Bulb"),
	25: ("(B)UG", "( B ) UG", "#555 Bulb"), 26: ("B(U)G", "B ( U ) G", "#555 Bulb"), 27: ("BU(G)", "BU ( G )", "#555 Bulb"),
	28: ("Left Turbo Bumper", "LEFT TUR- BO BUMPER", "#555 Bulb"), 29: ("Bottom Turbo Bumper", "BOTTOM TUR- BO BUMPER", "#555 Bulb"),
	30: ("Right Turbo Bumper", "RIGHT TUR- BO BUMPER", "#555 Bulb"), 31: ("Multi Ball", "MULTI BALL", "#44 Bulb"), 32: ("Super Nuke", "SUPER NUKE", "#44 Bulb"),
	34: ("Warrior Bug", "WARRIOR BUG", "#555 Bulb"), 35: ("2X Nuke", "2X NUKE", "#555 Bulb"), 36: ("Recon", "RECON", "#555 Bulb"),
	37: ("Left Outlane", "LEFT OUTLANE", "#555 Bulb"), 38: ("Right Outlane", "RIGHT OUTLANE", "#555 Bulb"),
	39: ("Advance Planet", "ADVANCE PLANET", "#555 Bulb"), 40: ("Left/Right Return Lanes", "LT/RT RE- TURN LANES", "#555 Bulb"),
	41: ("Left Ramp Stand-Up (Yellow)", "LEFT RAMP S-U (YEL)", "#555 Bulb"), 42: ("Pops Stand-Up (Blue)", "POPS S-U (BLU)", "#555 Bulb"),
	43: ("Pops Stand-Up (Green)", "POPS S-U (GRN)", "#555 Bulb"), 44: ("VUK Stand-Up (Green)", "VUK S-U (GRN)", "#44 Bulb"),
	45: ("VUK Stand-Up (Blue)", "VUK S-U (BLU)", "#44 Bulb"), 46: ("Right Ramp Stand-Up (Yellow)", "RIGHT RAMP S-U (YEL)", "#555 Bulb"),
	47: ("Left Ramp Nuke", "LEFT RAMP NUKE", "#555 Bulb"), 48: ("Right Ramp Nuke", "RIGHT RAMP NUKE", "#555 Bulb"),
	56: ("Arm Nukes", "ARM NUKES", "#44 Bulb"), 64: ("Extra Ball", "EXTRA BALL", "#44 Bulb"),
	72: ("Troopers (Hotdog)", "TROOPERS (HOTDOG)", "#555 Bulb"), 80: ("Shoot Again", "SHOOT AGAIN", "#555 Bulb"),
}
# The four 7-segment displays: lamp row -> (name, DR. 5 position, board display, row line).
LED_DISPLAYS = {7: ("Warrior", "top left", "DISP1", "Lamp Row 7 (Q39)"), 8: ("Hopper", "top right", "DISP2", "Lamp Row 8 (Q40)"), 9: ("Plasmabug", "bottom left", "DISP3", "Lamp Row 9 (Q41)"), 10: ("Tanker", "bottom right", "DISP4", "Lamp Row 10 (Q42)")}
SEGMENT_PINS = {"A": "Pin-1", "B": "Pin-13", "C": "Pin-10", "D": "Pin-8", "E": "Pin-7", "F": "Pin-2", "G": "Pin-11"}
for _row, (_name, _place, _disp, _line) in LED_DISPLAYS.items():
	for _index, _segment in enumerate("ABCDEFG"):
		LAMPS[(_row - 1) * 8 + _index + 1] = (f"{_name} 7-Segment {_segment}", f"{_name.upper()} 7- SEGMENT \"{_segment}\"", "Red LED")
LAMPS = dict(sorted(LAMPS.items()))
UNUSED_LAMPS = (33,)
DOTS_LAMPS = (28, 29, 30, 34, 35, 36, 39, 47, 48)
LAMP_DRIVE = [("YEL-BRN", "J13-P9", "U17"), ("YEL-RED", "J13-P8", "U16"), ("YEL-ORG", "J13-P7", "U15"), ("YEL-BLK", "J13-P6", "U14"), ("YEL-GRN", "J13-P5", "U13"), ("YEL-BLU", "J13-P4", "U12"), ("YEL-VIO", "J13-P3", "U11"), ("YEL-GRY", "J13-P1", "U10")]
LAMP_RETURN = [("RED-BRN", "J12-P1"), ("RED-BLK", "J12-P2"), ("RED-ORG", "J12-P3"), ("RED-YEL", "J12-P4"), ("RED-GRN", "J12-P5"), ("RED-BLU", "J12-P6"), ("RED-VIO", "J12-P8"), ("RED-GRY", "J12-P9"), ("RED-WHT", "J12-P10"), ("RED", "J12-P11")]
# 4X 7-Segment Display Board CN1 pin for each lamp column (columns 1-7) and display row (rows 7-10).
LED_COLUMN_PINS = {1: "CN1-P8", 2: "CN1-P9", 3: "CN1-P4", 4: "CN1-P10", 5: "CN1-P11", 6: "CN1-P6", 7: "CN1-P7"}
LED_ROW_PINS = {7: "CN1-P15", 8: "CN1-P12", 9: "CN1-P14", 10: "CN1-P13"}


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
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}] + legacy_aliases("vpe-legacy.lamp", address, LEGACY_LAMPS)
		notes = f"Printed lamp-matrix row {row + 1}, column {column + 1}."
		if address in UNUSED_LAMPS:
			notes += (
				" The Lamp Matrix Grid (DR. 4) prints this cell NOT USED and shaded with no bulb line, the lamp location drawing (DR. 5) marks "
				"no lamp with this number, and the retained script assigns no light to it. The ROM's lamp shows still write the bit with the rest "
				"of row 5: both harness runs saw it change 100 times, as often as its row neighbour 35. PinMAME publishes the lamp-matrix data "
				"the ROM writes whether or not a bulb sits in the cell, so that traffic is the light show, not a socket."
			)
			items.append(_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE) + BOTH_RUNS,
				aliases=aliases, physical={"notes": notes}, wiring=_lamp_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE)))
			continue
		label, printed, bulb = LAMPS[address]
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE) + BOTH_RUNS
		physical: dict[str, Any] = {"location": label}
		wiring = _lamp_wiring(address)
		notes += f' The grid prints "{printed}" with the lamp cell "{bulb}".'
		if bulb == "#555 Bulb":
			physical["part_number"] = "165-5002-00"
		if address in DOTS_LAMPS:
			notes += " The cell carries the grid's DOTS (diode on terminal strip) tag."
		if bulb == "Red LED":
			name, place, display, line = LED_DISPLAYS[row + 1]
			segment = "ABCDEFG"[column]
			physical["location"] = f"{name} 7-segment display, segment {segment}"
			physical["part_number"] = "165-5040-00"
			wiring = {
				"board": "4X 7-Segment Display Board 520-5166-00 on the lamp matrix", "drive_wire": LAMP_DRIVE[column][0],
				"drive_connection": f"{LED_COLUMN_PINS[column + 1]} (lamp column {column + 1}, {LAMP_DRIVE[column][1]})",
				"return_wire": LAMP_RETURN[row][0], "return_connection": f"{LED_ROW_PINS[row + 1]} ({line}, {LAMP_RETURN[row][1]})",
				"return_component": f"{display} cathode Pin-14; segment {segment} anode {SEGMENT_PINS[segment]} through diode D{column + 1} and resistor R{column + 1}",
			}
			notes += (
				f" Segment {segment} of {display} on the 4X 7-Segment Display Board 520-5166-00 (printed page 116): a 1\" red 7-segment display "
				f"MTN4126-CHR (165-5040-00), cathode on {line}, segment anode {SEGMENT_PINS[segment]} fed from lamp column {column + 1} through a "
				f"1N914 diode and a 220 Ω resistor. DR. 5 draws the {name.upper()} display {place} of the four over the flippers, segment A at the "
				"top, B upper right, C lower right, D bottom, E lower left, F upper left, G middle. se.c types the lamp as an LED strobe "
				"(CORE_MODOUT_LED_STROBE_1_10MS) for every 'startrp' driver. The board's solder-side note pairs CN1 pins 12-15 with DISP1-DISP4 "
				"'respectively', which read literally would put pin 12 on DISP1; its own schematic and the segment lamp numbers put Lamp Row 7 "
				"(pin 15) on DISP1, and the record follows them."
			)
			refs += (CORE_SOURCE,)
		elif bulb == "#44 Bulb":
			notes += " The grid prints a #44 bulb here, where most inserts carry #555."
		if address == 34:
			notes += (
				" The Warrior Bug Assembly's Screened Plastic -21 Assy 515-6777-21-59 carries one #555 bulb beside an F5 #906, and DR. 5 draws "
				"lamp 34 at the head of the warrior bug track. The retained table binds no light to 34."
			)
		if address == 40:
			physical["quantity"] = 2
			notes += " DR. 5 draws 40 twice, at the left and the right return lane: one address lights both."
		if address in (28, 29, 30):
			notes += " The Turbo Bumper Top Assy. 515-6459-01 carries one #555 wedge base bulb."
		notes += " The harness runs saw the ROM drive it."
		extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring}
		spatial = located("lamp", address, identifier, "emitter")
		if spatial:
			extra["spatial"] = spatial
			if address != 34:
				notes += " Retained table script: UpdateLamps drives it from Controller.ChangedLamps (UseLamps = 0, lines 214, 1505-1707)."
			notes += _placement_note("lamp", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		if address in LEGACY_LAMPS:
			refs += (LEGACY_SOURCE,)
		physical["notes"] = notes
		items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, "used", refs, physical=physical, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	entries = _spatial_seed()["gi"]["0"]
	placements = [{
		"id": f"gi.relay.emitter.{index}", "role": "emitter", "space": "playfield", "x": entry["x"], "y": entry["y"],
		"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
	} for index, entry in enumerate(entries, start=1)]
	notes = (
		"One G.I. relay on the I/O Power Driver board 520-5137-01 (U206 74HCT273 data latch D0 through R254 1K to Q200 2N3904, coil on "
		"20v DC with D229 across it) switches the 6.3v AC G.I. supply from J14 to four separately fused circuits on J15 (General "
		"Illumination Circuit Detailed Wiring Diagram, printed page 89): circuit 1, F24, BRN/WHT to WHT/BRN, under the upper left "
		"playfield, 10 #44; circuit 2, F25, YEL to WHT/YEL, under the lower left playfield, 7 #44, plus 2 #555 above the left mid "
		"playfield and the left return lane; circuit 3, F26, GRN to WHT/GRN, under the upper right playfield, 7 #44, plus 2 #555 in the "
		"coin door; circuit 4, F27, VIO to WHT/VIO, under the lower right playfield, 6 #44, plus 2 #555 above the right ramp and the "
		"right return lane. The page warns that G.I. bulb quantities may change during production. The quantity 36 is those 34 "
		"playfield bulbs plus the two coin-door bulbs. se.c publishes the relay as GI 0; the harness runs saw it switch on in attract "
		"mode and blink with the coins, the ramp exits, the right top lane, the outlanes, the warrior bug target, the bug hole, the VUKs and the drain. The retained "
		"table binds it: GICallback = UpdateGI (line 237) calls SetLamp 200 (lines 1155-1159), and UpdateLamps drives the GILamps "
		"collection Light001-Light028 and the glow flashers GIFL1 and lfgi001-lfgi004 from channel 200 (lines 1747-1779). Each of the "
		f"{len(entries)} GILamps lights draws its bulb (show_bulb_mesh) and none sits within 0.010 of another, so each is placed as one "
		"socket, observed only; the page's string drawing numbers the bulbs per circuit, but the placements have not been matched to it, "
		f"so no placement carries a circuit. That leaves {len(entries)} placed sockets against the 34 playfield bulbs the page prints; the "
		"two coin-door bulbs are counted but not placed."
	)
	return [_device(
		"gi.relay", "General Illumination Relay", "gi", GI_GROUP, 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, LEGACY_SOURCE) + BOTH_RUNS,
		aliases=[{"namespace": "pinmame.gi", "value": "0"}] + legacy_aliases("vpe-legacy.lamp", 200, LEGACY_LAMPS),
		physical={"location": "playfield and coin door", "quantity": 36, "notes": notes},
		wiring={"board": "Whitestar I/O Power Driver board 520-5137-01 G.I. relay", "power_wire": "YEL / YEL-WHT 6.3v AC through F24-F27", "power_connection": "J14/J15", "nominal_voltage_v": 6.3, "voltage_type": "ac"},
		spatial={"status": "observed", "placements": placements},
	)]


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "Dot Matrix Display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, *BOTH_RUNS),
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
	}]


# --- Mechanisms ----------------------------------------------------------------------------------------
def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], assembly: str | None = None, positions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
	result: dict[str, Any] = {"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior}
	if assembly:
		result["assembly_part_number"] = assembly
	if positions:
		result["positions"] = positions
	result["provenance"] = provenance("validated", *refs)
	return result


def mechanisms() -> list[dict[str, Any]]:
	common = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	run = common + BOTH_RUNS
	s = switch_id
	q = q_output_id
	return [
		_mechanism("trough", "4-ball trough with up-kicker opto", "kicker", [q(1)], [s(12), s(13), s(14), s(15)],
			"Four balls rest in the 4-Ball Trough (OPTO) Assembly 500-6119-24 on the roller micro switches 12 (left), 13 and 14 and on "
			"the up-kicker opto 15, which is ball position 1 (the trough page: 'Ball Position (1) is determined by the OPTO Switch'). Q1 "
			"(26-1200) kicks the ball on 15 up into the shooter lane and the rest roll one place toward the up-kicker; hold each "
			"occupied position at 1. In the gameplay runs the ROM fired Q1 on Start and again after the "
			"drain. The retained table's bsTrough holds the same four positions.", run, assembly="500-6119-24"),
		_mechanism("shooter", "Ball shooter and auto launch", "kicker", [q(2)], [s(16)],
			"A served ball rests on shooter-lane switch 16, which in the gameplay runs made the ROM raise the game-on state 15. The player "
			"plunges it, or Q2 (24-940) fires the autoplunger arm; the ball-path callout (printed page 6) sends a shooter-lane shot into the "
			"right orbit. IPDB notes that the right outlane also serves as part of the shooter lane. The retained table fires its Plunger "
			"object with Autoplunger set.", common + (IDENTITY_SOURCE,) + BOTH_RUNS),
		_mechanism("vuk", "VUK on the left side", "kicker", [q(3)], [s(45)],
			"The VUK Assembly 500-5839-04 (printed page 75, coil 26-1200, Micro Switch 180-5116-01) at the left side of the playfield: a "
			"ball that enters rests on 45 until Q3 kicks it up. In the gameplay runs a ball held on 45 drew Q3 kicks, and also a Q4 kick and "
			"the flashers 27, 30 and 32. The retained table holds it in the cvpmSaucer bsLeftVUK and kicks it with SolLeftVuk.", run, assembly="500-5839-04"),
		_mechanism("super-vuk", "Super VUK and under-troughs", "kicker", [q(4)], [s(46), s(9), s(10), s(40)],
			"The Super VUK Assembly 500-6245-02-59 (printed page 76, coil 26-1200, Micro Switch 180-5052-00, enter/exit scoop 'located "
			"above the Super VUK'). The Plastic Under-Trough Assembly 500-6244-00-59 (printed page 83) collects balls from the top exit hole "
			"(9, the soft left-orbit or soft left-ramp shot) and the warrior bug's exit hole (10) and lists two Micro Switches (High Form) "
			"180-5057-00 for them; the Metal Under-Trough (Small VUK) Assembly 500-6243-00-59 (printed page 82), the Mini-Under-Trough, "
			"collects balls from the pop exit hole and lists one, switch 40. Both lead to the super VUK, which shoots the ball 'out towards "
			"the right flippers' (ball-path callouts, printed pages 7 and 9). A ball rests on 46 until Q4 kicks it. In the gameplay runs a "
			"ball held on 46 drew Q4 kicks; one closure of 10 changed warrior-bug stepper phases and flashed F2, F3 and F5; one closure of 9 "
			"drew nothing, and one of 40 drew no coil or flasher while the G.I. went off. The retained table pulses 10 from a kicker and "
			"hands the ball to its bsSuperVUK stack 1.8 s later, and holds 9 and 40 on triggers.", run, assembly="500-6245-02-59"),
		_mechanism("magnets", "Orbit magnets", "other", [q(5), q(6)], [s(47), s(48)],
			"Two magnets (22-650, 090-5042-01, on Threaded Bushing Core Assemblies 515-6142-00) under the rear of the playfield, where the "
			"two orbits meet at the top. A hard orbit shot with the left magnet on deflects the ball down into the top exit hole and the "
			"under-trough to the super VUK; a hard right orbit shot with the right magnet on deflects it into the top lanes; with a magnet "
			"off the ball completes the orbit (ball-path callouts, printed pages 6-7). The orbit optos 47 and 48 see the ball enter; in the "
			"gameplay runs each made the ROM fire the right magnet Q6 twice, a hold of 0.60-0.67 s that began while the input was still 1 "
			"and a short pulse about 2.1 s after it. The retained table holds the ball with cvpmMagnet objects on "
			"the triggers LeftMagnet and RightMagnet.", run),
		_mechanism("warrior-bug", "Warrior bug on a stepper-driven track", "motorized", [q(17), q(18), q(19), q(20), q(29), lamp_id(34)], [s(33), s(34), s(35)],
			"Warrior Bug Assembly 500-6239-00-59 (printed pages 78-79): a bug carriage on a track at the upper left, moved forward and back "
			"by a unipolar HSI #36864-12 stepper motor (15° and .004\" per step, 12v DC, 4.6W; Appendix F) whose four phases are Q17-Q20. "
			"Roller micro switches 33 (rear) and 34 (front) sense the carriage at each end of its travel, and the target 35 (stack switch "
			"180-5133-00) rides the carriage. F5 (Q29) lights three #906 on the track and one #89 at its head, and lamp 34 (#555) sits on the "
			"screened plastic at the head. The callout (printed page 7): 'Each hit to the Warrior Bug will push it back until the ball can "
			"enter the Bug Exit Hole to the Undertrough', which is switch 10. The Backbox I/O Power Driver Board Detailed Wiring Diagram "
			"(printed page 88) wires the motor's two centre-tapped windings: Q17 to RED and Q19 to BLK on one, Q18 to GRN and Q20 to BLU on "
			"the other, both WHT taps to the +12V DC GRY/RED supply (J16-P3), with each phase's 1N4004 on a terminal strip below the "
			"playfield; energizing 17, 18, 19, 20 in turn therefore alternates the windings one full step at a time. The direction comes "
			"from the known-working script: its cvpmMyMech mBug hands PinMAME's mech.c Sol1 = 17 with vpmMechStepSol + vpmMechTwoDirSol, "
			"the four-step-solenoid mode, in which phases following in the order 20, 19, 18, 17 count the position up toward the rear "
			"switch 33 (steps 221-222 in the script) and phases in the order 17, 18, 19, 20 count it down toward the front switch 34 (steps "
			"0-1). The travel length is the table's own: the script models 222 positions over a mech length of 600 (.Length, its trip-time setting), and the manual gives the .004\" "
			"step but no length. In the gameplay runs the ROM changed the phases at power-up, when a ball reached the shooter lane, and "
			"from the bumper 49, the target 35, the bug hole 10 and the right orbit 48, and flashed F5 from 35 and 10; the harness samples "
			"outputs about every 67 ms, too slowly to resolve the step order, and drove no mechanism, so the end switches never changed. The "
			"retained table moves the bug through UpdateWarriorBug and raises one of 24 hit walls for the bug's position.",
			run + (VPX_TABLE_SOURCE,), assembly="500-6239-00-59",
			positions=[
				{"id": "mechanism.warrior-bug.rear", "label": "Rear limit", "sensors": [s(33)], "description": "Carriage at the rear end of the track, the stepper motor rear switch closed."},
				{"id": "mechanism.warrior-bug.front", "label": "Front limit", "sensors": [s(34)], "description": "Carriage at the front end of the track, the stepper motor front switch closed."},
			]),
		_mechanism("brain-bug", "Brain bug pop-up", "toy", [q(7), q(23)], [s(37), s(38), s(39)],
			"Brain Bug Assembly 500-6256-00-59 (printed pages 76-77): the brain bug figure (880-5004-00) on a slide plate under the centre of "
			"the playfield, raised by the 22-1080 coil Q7 through a window flap, with three Cherry limit switches 180-5165-00: 37 and 39 "
			"('BRAIN BUG UP') and 38 ('BRAIN BUG HIT'). Q23 lights two #89 either side of the brain bug picture. The callout (printed page 9): "
			"'If that Brain Bug Pops up from under the playfield, hit it with the ball!' The assembly carries a ball-trap prevention wire "
			"form (535-8245-00). No harness run raised the brain bug outside the ball search, so its up switches 37 and 39 were never "
			"exercised; 38, closed once in each run while Q7 was off and the bug down, drew no coil, flasher or G.I. change. The retained table rotates BrainBugFlipper up, raises the walls sw38/sw38a and sets 37 and 39 while Q7 is on, and "
			"pulses 38 from a hit on the wall sw38.", run, assembly="500-6256-00-59"),
		_mechanism("lower-flippers", "Lower flippers", "other", [q(15), q(16)], ["switch.84-left-flipper-button", "switch.83-left-flipper-end-of-stroke", "switch.82-right-flipper-button", "switch.81-right-flipper-end-of-stroke"],
			"Left (500-5944-14) and right (500-5944-04) flipper assemblies with 23-1100 coils on one 50v supply. The CPU applies a 40 ms pulse "
			"on a button closure and then 1 ms every 12 ms while the button is held; each N.C. end-of-stroke switch opens at full stroke, and a "
			"closure during a hold earns another 40 ms pulse. PinMAME publishes Q15 at 47/48 and Q16 at 45/46. The ROM reads the buttons "
			"82 and 84 and drives both coils itself; PinMAME does not take the end-of-stroke inputs from the host, but rewrites 81 and 83 "
			"from 46 and 48 (FLIP_SOL includes FLIP_EOS), publishing 1 once a coil has been held two updates, the reverse of the N.C. "
			"contact.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) + BOTH_RUNS),
		_mechanism("mini-flipper", "Mini flipper", "other", [q(14)], ["switch.88-mini-flipper-button"],
			"The Flipper (Mini-Right) Assy. 500-5944-02 (printed page 73) with a 22-1080 coil (Q14) and a fluorescent orange mini bat, "
			"right of centre above the trough (coil location drawing). Its own N.O. cabinet button (88, DS-5) is read by the CPU, which "
			"drives Q14 itself; no end-of-stroke input is wired (the 3-Flipper Circuit draws none, although the assembly heading's item "
			"range takes in the EOS switch 180-5149-00) and PinMAME runs no flipper simulation for it. In the gameplay runs holding 88 pulsed "
			"Q14. The retained table fires its RightFlipperS from its mini-flipper key handler while the game-on state 15 is set.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) + BOTH_RUNS, assembly="500-5944-02"),
		_mechanism("bumpers", "Three turbo bumpers", "other", [q(9), q(10), q(11)], [s(49), s(50), s(51)],
			"Left (top of the triangle; Q9/49), bottom (Q10/50) and right (Q11/51) turbo bumpers (515-6459-01, -04, -03) with stack-blade "
			"spoon switches 180-5015-03; each switch fired its own coil in the gameplay runs. F8 (Q32) lights two #89 at the pops.", run),
		_mechanism("slingshots", "Slingshots", "other", [q(12), q(13)], [s(59), s(62)],
			"Left (Q12/59) and right (Q13/62) slingshots (500-5849-01, coil 26-1200, switch 180-5054-00); each switch fired its own coil in "
			"the gameplay runs. The retained table's handlers cross the two switch numbers.", run, assembly="500-5849-01"),
	]


# --- Drivers -------------------------------------------------------------------------------------------
def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {driver["id"]: driver for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
	if set(by_id) != set(DRIVER_IDS):
		raise RuntimeError(f"Starship Troopers driver family differs from the catalog: {sorted(set(DRIVER_IDS) ^ set(by_id))}")
	records = []
	for driver_id in sorted(DRIVER_IDS):
		source = by_id[driver_id]
		record = {key: source[key] for key in ("id", "description", "year", "manufacturer", "flags")}
		if source.get("clone_of"):
			record["clone_of"] = source["clone_of"]
		record["physical_compatibility"] = DRIVER_COMPATIBILITY[driver_id]
		record["variant_notes"] = BASE_DRIVER_NOTE + DRIVER_NOTES[driver_id]
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

RENDERER = "; rendered by tools/render_excerpt_image.py with PyMuPDF 1.26.3 and Pillow 12.3.0"
IMAGE_DERIVATIONS = {
	"switch-lamp-locations": f"{MANUAL_NAME} page 7, crop box 0.12,0.02,0.97,0.68, scanned page rendered at its native resolution (embedded image xref 42, 1912px across 6.37in), rendered at 222 dpi, capped to 1200px wide, grayscale, 1201x1207 WebP quality 70" + RENDERER,
	"coil-flash-locations": f"{MANUAL_NAME} page 9, crop box 0.12,0.02,0.98,0.7, scanned page rendered at its native resolution (embedded image xref 52, 1912px across 6.37in), rendered at 219 dpi, capped to 1200px wide, grayscale, 1201x1229 WebP quality 70" + RENDERER,
	"gi-wiring": f"{MANUAL_NAME} page 103, full page, scanned page rendered at its native resolution (embedded image xref 549, 1912px across 6.37in), rendered at 235 dpi, capped to 1500px wide, grayscale, 1500x1942 WebP quality 80" + RENDERER,
	"flipper-circuit": f"{MANUAL_NAME} page 106, full page, scanned page rendered at its native resolution (embedded image xref 564, 1912px across 6.37in), rendered at 235 dpi, capped to 1500px wide, grayscale, 1500x1942 WebP quality 80" + RENDERER,
}


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {"id": f"excerpt.starship-troopers.{name}", "locator": locator, "path": f"evidence/excerpts/{MACHINE_ID}/{name}.md", "sha256": EXCERPT_FILE_HASHES[f"{name}.md"]}
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
		_excerpt("switch-matrix", "PDF page 6, printed DR. 4, Switch Matrix Grid and dedicated switches; PDF page 35, printed page 21, Switch Matrix Grid Descriptions with Part Numbers and Locations"),
		_excerpt("lamp-matrix", "PDF page 6 (lower half), printed DR. 4, Lamp Matrix Grid"),
		_excerpt("switch-lamp-locations", "PDF page 7, printed DR. 5, switch and lamp location drawings"),
		_excerpt("coil-table", "PDF page 8, printed DR. 6, Coils Detailed Chart Table"),
		_excerpt("coil-flash-locations", "PDF page 9, printed DR. 7, coil and flash lamp location drawings"),
		_excerpt("backbox-display", "PDF pages 64 and 69, printed pages 50 and 55, Backbox Layout Locations and Backbox (Front Side) Assembly items 1-8"),
		_excerpt("power-driver-wiring", "PDF page 102, printed page 88, Backbox I/O Power Driver Board Detailed Wiring Diagram"),
		_excerpt("gi-wiring", "PDF page 103, printed page 89, General Illumination Circuit Detailed Wiring Diagram"),
		_excerpt("flipper-circuit", "PDF page 106, printed page 92, 3-Flipper Circuit Wiring Diagram"),
		_excerpt("cabinet-wiring", "PDF page 108, printed page 94, Cabinet / Coin Door Wiring Diagram"),
		_excerpt("led-display-board", "PDF page 130, printed page 116, 4X 7-Segment Display Board schematic, layout and parts"),
		_excerpt("mechanism-assemblies", "PDF pages 20-24, 73, 75, 83-98, 109, 111 and 143, printed pages 6-10, 59, 61, 71-84, 95, 97 and 127, playfield overview, Tanker Bug parts, major assemblies, opto boards and Appendix F (selected items)", reviewed=False),
	]


def source_records() -> list[dict[str, Any]]:
	runs_201 = load_json(ROOT / RUNTIME_201_PATH)["runtime"]["raw_runs"]
	runs_200 = load_json(ROOT / RUNTIME_200_PATH)["runtime"]["raw_runs"]

	def describe(raw_runs: list[dict[str, Any]]) -> str:
		return ", ".join(f"{raw['name']} (run.json SHA-256 {raw['sha256'][:12]}..., directory manifest {RUN_MANIFESTS[raw['name']][:12]}...)" for raw in raw_runs)

	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the startrp clone tree (" + ", ".join(DRIVER_IDS) + "); src/wpc/driver.c lines 1391-1392",
			"license": "LicenseRef-PinMAME-Old-MAME", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/segames.c INITGAME macro (lines 12-15: FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), swCol 0, lampCol 2, custSol 0) and "
				"INITGAME(startrp, GEN_WS, se_dmd128x32, 0) / INITGAME(startrp2, ...) with the sstcpu.201 and sstcpu.200 ROM sets on de_mSES1 "
				"(lines 323-343); src/wpc/se.h SE_COMPORTS 'Dip SW300' (line 23, mask 0x001f); src/wpc/se.c fast-flip block publishing public 15 "
				"(lines 183-191), MACHINE_INIT(se) (line 357; the 'startrp' prefix sets the fast-flip byte at CPU RAM 0x00, lines 408-409), the "
				"'startrp' output types (lines 522-529: solenoid 23 and 25-32 #89 bulbs, lamps 49-55, 57-63, 65-71 and 73-79 LED strobes), "
				"ram_w's memory-protect gate on -3 (lines 593-596), switch_r (~core_getSwCol, line 641), dedswitch_r (flipper column swapped "
				"into U206 order with the upper-flipper bit on D4, complemented, lines 645-661), dip_r (line 664), se_solenoid_w (Q15/Q16 masked "
				"off and published at 47/45, lines 668-680) and the G.I. relay at gi[0] (line 829); src/wpc/core.c core_updateSw (FLIP_SOL "
				"includes FLIP_EOS, core.h lines 160-161, so lines 1839-1870 fake no flipper output and rewrite the lower EOS bits 81/83 from "
				"core_getSol(46/48) after CORE_FLIPSTROKETIME); src/wpc/mech.c mech_update (lines 117-136: MECH_FOURSTEPSOL reads Sol1..Sol1+3 as one four-bit pattern "
				"and counts the position up when the previous pattern is the current one rotated right, down when rotated left). None of these "
				"files carries the BSD-3-Clause marker, so the pinned LICENSE leaves them under the older MAME terms."
			),
			"license": "LicenseRef-PinMAME-Old-MAME", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/whitestar.json", "revision": "repository",
			"sha256": CONTROLLER_PROFILE_SHA256,
			"locator": (
				"Whitestar public switch (-3..0, 1-64, 81-88), DIP 1-8, solenoid 1-50, lamp and GI 0 address rules and their notes; sha256 is "
				"the profile file this record was checked against, and the curator refuses to run when the file no longer matches it"
			),
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-11-20T08:27:49Z",
			"locator": (
				"IPDB machine 4341 'Starship Troopers' (Sega Pinball, December 1997, model 59, Sega/Stern Whitestar, 6 players), read from the "
				f"Wayback Machine capture {IPDB_WAYBACK_URL} because the live site is Cloudflare-gated; the capture is retained gzip-compressed "
				f"under {MANUALS_DIRECTORY}. Its documentation list carries the 16 MB English manual whose bytes match the retained copy."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", f"IPDB machine 4341 page, {IPDB_WAYBACK_URL}", reviewed=False)],
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}", "original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256, "acquired_at": "2026-11-20T08:28:22Z",
			"locator": (
				"Sega Starship Troopers operations manual (150 scanned pages, no text layer; printed page = PDF page - 14 in Sections 2-5). PDF "
				"6-9 are the front-matter Dr. Pinball sheets (DR. 4 switch and lamp matrix grids, DR. 5 switch and lamp locations, DR. 6 coil "
				"chart, DR. 7 coil and flash locations); PDF 20-24 the playfield overview and ball paths; PDF 35 the printed page-21 switch "
				"table; PDF 64 and 69 the backbox layout and the Backbox (Front Side) Assembly with the dot matrix display; PDF 83-98 the major assemblies; PDF 102 the I/O power driver board wiring; PDF 103-111 the G.I., flipper, cabinet and opto pages; PDF 130 the 7-segment display "
				f"board; PDF 143 Appendix F. IPDB's direct resource {MANUAL_URL} was fetched through the Wayback Machine ({MANUAL_WAYBACK_URL})."
			),
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Sega Pinball, Inc.; hosted by the Internet Pinball Machine Database",
			"excerpts": _manual_excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "known_working": True,
			"uri": f"external:pinmame-vpx-sources/{VPX_DIRECTORY}/" + quote(TABLE_NAME),
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256, "acquired_at": "2026-11-20T08:31:13Z",
			"locator": (
				f"Retained VPW Starship Troopers Mod v2.0 recreation ({TABLE_BYTES} bytes). Exact playfield bounds are {TABLE_BOUNDS}; "
				f"normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for the objects its "
				"embedded script binds; the placement seed tools/seeds/sega/starship-troopers-1997-spatial.json lists them."
			),
			"license": "NOASSERTION", "attribution": "VPW (table authors)", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "known_working": True,
			"uri": f"external:pinmame-vpx-sources/{VPX_DIRECTORY}/" + quote("Starship Troopers (Sega 1997) VPW Mod v2.0/script.vbs"),
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256,
			"locator": (
				"The retained table's embedded script as vpxtool extracts it. Runtime authority for controller callbacks: Const cGameName = "
				"\"startrp2\", LoadVPM \"01560000\", \"sega.vbs\", 3.57, UseSolenoids = 15, UseLamps = 0, HandleMechanics = 0, the bsTrough and "
				"bsSuperVUK ball stacks, the bsLeftVUK saucer, the two cvpmMagnet objects, the warrior bug cvpmMyMech, the SolCallback table, "
				"UpdateLamps, the G.I. callback and the switch handlers. Known table defects: the slingshot handlers pulse each other's switch "
				"(59/62), SolCallBack(8) plays a knocker on the token-dispenser driver, and lamp 34 is not bound. It never writes the EOS inputs "
				"81/83, which PinMAME rewrites from the flipper outputs."
			),
			"license": "NOASSERTION", "attribution": "VPW (table authors)", "rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment line of the embedded script that binds the controller, with its line number", credit=QUOTE_CREDIT)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}", "sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under the vpxtool extraction "
				f"'{EXTRACTION_RELATIVE_PATH.as_posix()}'; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_OBJ_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{VPX_DIRECTORY}/" + quote(OBJ_EXPORT_RELATIVE_PATH.relative_to(VPX_DIRECTORY).as_posix()),
			"sha256": OBJ_EXPORT_SHA256,
			"locator": (
				"vpxtool git:v0.33.3 `export obj --units vpu` of the retained table, the world-space mesh of every object (OBJ x is "
				"playfield x, OBJ y is playfield y and OBJ z is minus the height). Used to find the modelled part under each flasher and bulb "
				"lamp Light and to place it: each object is split into connected pieces after welding vertices that agree at 0.1 VPU, the "
				"placement seed records the piece of the Caps<Color> domes, the KabeSockel sockets, the WarriorBugAssembly006 bulbs or the "
				"bulbs_red, bulbs_yellow and bulbs_blue lamp bulbs whose bounds contain each placed flasher Light and bulb lamp Light, and "
				"each of those 18 flasher and 8 lamp placements is the centre of its socket or bulb piece. The seed also checks that no "
				"such piece lies under the brain bug, ramp and pop flasher Lights and that each bulbs_* piece belongs to exactly one lamp. "
				"Control: the "
				"largest Bumper1Base piece centres 0.29 VPU from the bumper Bumper1's stored centre."
			),
			"license": "NOASSERTION", "attribution": "vpxtool export of the retained table",
		},
		{
			"id": VPX_CORPUS_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/jsm174/vpx-standalone-scripts/blob/{VPX_CORPUS_REVISION}/" + quote(CORPUS_PATH, safe="/"),
			"revision": VPX_CORPUS_REVISION, "sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				"Pinned corpus copy of the same VPW Mod v2.0 table script, byte-identical to the retained embedded script; it corroborates the "
				"bindings, not independently, because both are one table's script. The retained SHA-256 is the repository checkout's CRLF "
				f"materialization; the linked Git blob is the identical LF-normalized text (SHA-256 {CORPUS_BLOB_SHA256})."
			),
			"license": "NOASSERTION", "attribution": "Authors credited in " + CORPUS_PATH + " and repository contributors",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-review-artifacts/vpm-script-libs/sega.vbs",
			"original_filename": "sega.vbs", "sha256": VPM_SEGA_SHA256,
			"locator": (
				"VPinMAME Sega/Stern Whitestar script library the retained table loads, copied from the contributor's Visual Pinball Scripts "
				f"folder beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). It defines GameOnSolenoid = 15, swBlack 0 / swGreen -1 / "
				"swRed -2 / swMemoryProtect -3, swStartButton 54, swTilt 56, swSlamTilt 55, swCoin3 4 / swCoin1 5 / swCoin2 6, swLRFlip 82, "
				"swLLFlip 84, swURFlip 81 and swULFlip 83, and the country DIP form; it has no constant for the mini flipper button 88."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library", "sega.vbs constants (lines 20-39), DIP form (lines 52-69) and key handlers (lines 71-139); core.vbs fast-flip solenoid (lines 2121-2133 and 2479)", credit=QUOTE_CREDIT)],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/startrp.zip", "revision": "2.01", "sha256": ROM_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned startrp ROM set (sstcpu.201 CRC 549699fe, sstdspa.200 CRC 76a0e09e); used to identify the ROM the harness booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Sega Pinball game code; ROM bytes remain external",
		},
		{
			"id": ROM_200_SOURCE, "kind": "rom_static_analysis", "uri": "external:vpinmame-roms/startrp2.zip", "revision": "2.00", "sha256": ROM_200_ARCHIVE_SHA256,
			"locator": "User-authorized read-only archive whose members match the pinned startrp2 ROM set (sstcpu.200 CRC 1bd865a5); used to identify the ROM the second harness run booted. ROM bytes stay external.",
			"license": "NOASSERTION", "attribution": "Sega Pinball game code; ROM bytes remain external",
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_201_PATH}", "revision": PINMAME_REVISION,
			"sha256": _file_sha256(ROOT / RUNTIME_201_PATH),
			"locator": (
				f"A hash-pinned LibPinMAME harness run of startrp (library SHA-256 {RUNTIME_LIBRARY_SHA256[:12]}..., built from "
				f"{PINMAME_REVISION[:8]}) from empty NVRAM with built-in mechanisms off: {describe(runs_201)}. Scenario under "
				"tools/harness-scenarios/whitestar; tools/starship_troopers_runtime_evidence.py derives the committed per-step transitions from the retained run. "
				f"{HARNESS_COVERAGE}"
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": RUNTIME_200_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_200_PATH}", "revision": PINMAME_REVISION,
			"sha256": _file_sha256(ROOT / RUNTIME_200_PATH),
			"locator": (
				f"A hash-pinned LibPinMAME harness run of startrp2 on the same library from empty NVRAM with built-in mechanisms off: "
				f"{describe(runs_200)}. Its scenario repeats the startrp gameplay scenario step for step. {HARNESS_COVERAGE}"
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": LEGACY_SOURCE, "kind": "legacy_json", "uri": "https://github.com/vpinball/pinmame-game-defs", "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
			"locator": "games/sst.json; origin=vbscript-parser. The superseded migration record; only its alias values are kept, on the devices they denote.",
			"attribution": "pinmame-game-defs contributors",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
def _check_controller_profile() -> None:
	if _file_sha256(CONTROLLER_PROFILE_PATH) != CONTROLLER_PROFILE_SHA256:
		raise RuntimeError(
			"controllers/pinmame/whitestar.json changed since this record was checked against it; review the Starship Troopers "
			"controller facts against the new profile, then update CONTROLLER_PROFILE_SHA256"
		)


def build() -> dict[str, Any]:
	_check_controller_profile()
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Starship Troopers", "manufacturer": "Sega", "year": 1997, "kind": "physical_pinball", "model_number": "59",
			"ipdb_id": 4341, "opdb_id": "G5we0-MDx6b",
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
		"knowledge": {"path": "knowledge/sega/starship-troopers-1997.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Starship Troopers device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Starship Troopers mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Extraction manifest -------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Starship Troopers retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest", "version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Starship Troopers extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Starship Troopers retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Starship Troopers retained extraction manifest does not match the files under the extraction")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Starship Troopers retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
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
	return {
		"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield", "source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right", "y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256, "embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH), "obj_export_sha256": OBJ_EXPORT_SHA256,
		},
		"extraction": {
			"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "total_bytes": EXTRACTION_TOTAL_BYTES, "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}", "source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The centre of the VPX object the embedded script binds to each switch (trigger, target wall, kicker, bumper). The trough "
				"switches, which the table does not model, are projected onto the release kicker BallRelease; the under-trough switches onto "
				"the hole objects that pulse them; the stepper end switches onto the end walls the warrior bug mech raises and the bug target "
				"onto their midpoint; the brain bug switches 37 and 39 onto the wall sw38a; each end-of-stroke contact onto its flipper; and "
				"the slingshot switches onto the slingshot wall on the manual's side, across the table's crossed handlers."
			),
			"lamp": (
				f"The {len(seed_tool_inserts())} lamps DR. 5 draws below the playfield are projected onto the bulb light UpdateLamps drives for each, "
				"at the insert it lights: the table models no bulb or socket under the playfield, so each point is the insert's position, "
				"not a measured socket. The lamps whose Lights sit on a bulb the table models (the turbo "
				"bumpers 28-30, the ramp nukes 47 and 48 and the Tanker Bug sign's 35, 36 and 39) are placed at the centre of that bulb's "
				"piece of the world-space mesh export, which they cite with its height; the sign stands upright, so its lamp 39 is the bulb below 35 and 36, as the Tanker Bug Assembly "
				"(printed pages 59 and 61) and DR. 5 draw it. Each 7-segment LED segment is the lit centroid of its segment texture on the "
				"Flasher quad UpdateLamps drives, checked against the A-G key and the two-by-two layout on DR. 5. Lamp 34, which the table "
				"does not bind, is projected onto the rearmost bug wall at the head of the warrior bug track."
			),
			"solenoid": (
				"The kicker, bumper, slingshot wall or flipper the script fires, the magnet triggers, and for a flasher each script-driven "
				"Light that sits on a part the table models. No flasher Light draws a bulb mesh of its own, so the world-space mesh export "
				"decides: each of the sixteen F1-F4 Lights sits on one Caps<Color> Mini-Mars dome and one KabeSockel socket piece (0.3-7.7 VPU "
				"from their centres), and F5's l129 and l129a each sit on one of the two bulbs modelled on WarriorBugAssembly006 (5.1 and "
				"7.4 VPU); each is placed at the centre of that socket or bulb piece, not at its render Light. The brain bug, ramp and pop flasher Lights (l123a, l123b, l130b-l130d, l131b-l131d, l132) sit on no modelled bulb, "
				"dome or socket and place nothing, and neither do the table's VPX Flasher glow sprites (lf129, f130a-f130d, f131a-f131d, lf132 "
				"and the strobe overlays) or the wide-falloff ambient lights l129b, l130e and l131e. The auto launch is placed on the table's "
				"Plunger, the brain bug coil on the wall sw38a and the four stepper phases on the rear wall BWall24, where the Warrior Bug "
				"Assembly drawing mounts the motor, each projection citing the manual drawing that locates the part."
			),
			"gi": "The 28 Light members of the table's GILamps collection, each drawing its bulb; observed only, without per-circuit assignment.",
		},
		"unresolved_geometry": [
			"The trough switches 12-15 and the under-trough switches 9, 10 and 40 are not modelled as switches by the table; their placements are projections onto mechanism and hole objects.",
			"The warrior bug's stepper motor and end switches, its target, the brain bug coil and its two up switches are projections onto the walls the script moves, not the parts under or on the playfield.",
			"Lamp 34 is unbound in the table and projected onto the bug track's rear wall from the lamp location drawing.",
			f"The {len(seed_tool_inserts())} insert lamps DR. 5 draws below the playfield ({sum(len(_spatial_seed()['lamp'][str(address)]) for address in seed_tool_inserts())} "
			"bulbs) are projected onto the bulb lights the table drives at their inserts; the table models no bulb or socket under the "
			"playfield, so their sockets are not measured.",
			"Each 7-segment LED segment is placed at the lit centre of the table's segment texture, which agrees with the manual's A-G key but was not measured on a real display; the four one-inch displays sit over the flippers.",
			"Flasher bulbs without a placement: " + "; ".join(
				f"{'the brain bug flasher' if number == 23 else f'F{number - 24}'} (Q{number}) {len(_spatial_seed()['solenoid'].get(str(number), []))} of {quantity} placed"
				for number, quantity in FLASHER_QUANTITY.items() if len(_spatial_seed()["solenoid"].get(str(number), [])) < quantity
			) + ". The table models none of these bulbs, only render lights and glow sprites near some of them, and the flash lamp location drawing (DR. 7) has not been measured for them.",
			"No placement has been checked against the factory location drawings by a callout fit, so every placement stays observed.",
			"The table models 28 G.I. sockets against the 34 playfield bulbs the G.I. page prints. That page gives each bulb's circuit and a broad region (upper or lower, left or right), not a socket position, so the six sockets the table lacks need a factory G.I. socket drawing or photographs of a real playfield.",
		],
		"promotion_decision": "partial: the brain bug, ramp and pop flashers have no placement, and projections and placements the drawings do not yet confirm keep spatial_placement in coverage.missing.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Starship Troopers (Sega, 1997) spatial blockers", "",
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
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Starship Troopers artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Starship Troopers author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"Starship Troopers deterministic artifact drift: {path}")
	print("Starship Troopers definition, knowledge note and spatial report match the deterministic curator.")


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
		print(f"Starship Troopers extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Starship Troopers retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
