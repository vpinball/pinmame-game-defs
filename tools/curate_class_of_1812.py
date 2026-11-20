"""Curate the physical Gottlieb Class of 1812 (1991) machine definition.

The builder is side-effect free and deterministic: every reviewed label is a literal here, so regeneration reproduces
the canonical definition, its pinned seed and the spatial report byte for byte without reading the external evidence
roots, and copies the knowledge note from its pinned seed. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes them.

Class of 1812 is a Gottlieb System 3 alphanumeric machine (``GEN_GTS3``, ``mGTS3S``, alpha generation 1) with one
physical driver, ``clas1812``, declared as ``INITGAME(clas1812, ALPHA, FLIP67, 3/*?*/, SNDBRD_GTS3, 4)``: two 20-character
16-segment displays, the cabinet port on public 0-5 (three coin chutes, Start and the left and right advance buttons),
cabinet-wired flippers copied into switches 6 (left) and 7 (right) from PinMAME's flipper column (public 143 and 141),
and ``hw.lampCol = 4``, so no auxiliary driver board and no lamps 120-127. Its clone ``beav_butt`` is a VPX-only reskin
excluded in ``scope.py``. No service manual is retained: IPDB lists one without hosting it. The ROM's own service tests
name every switch, lamp and solenoid, and a harness run of each pairs the name with the public address it drives or reads
(``evidence/runtime/gts3/class-of-1812-clas1812-service-tests.json``). Playfield positions come from the retained
NZ&TT 1.0 table by tom tower & ninuzzu, whose embedded script binds every playfield address to the same object as the
pinned known-working script. Each placement is the object the script binds, except switch 44, which the ROM's trough
probes and the table's own 3.0.21 update move to the trough's second position; with one table lineage and no factory
drawing they stay ``observed``. The object
coordinates are literals here, and ``verify_retained_table`` re-derives each one from the retained extraction and OBJ
export.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.class-of-1812.1991"
PARTIAL_PATH = ROOT / "machines/partial/gottlieb/class-of-1812-1991.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/gottlieb/class-of-1812-1991.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/gottlieb/class-of-1812-1991.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/gottlieb/class-of-1812-1991.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/gottlieb/class-of-1812-1991.md"
KNOWLEDGE_PATH = "knowledge/gottlieb/class-of-1812-1991.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/gottlieb/class-of-1812-1991-knowledge.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/gts3/class-of-1812-clas1812-service-tests.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-gts3"
IDENTITY_SOURCE = "identity.gottlieb.class-of-1812.1991"
CARDS_SOURCE = "manual.gottlieb.class-of-1812.1991.instruction-cards"
TEETH_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.teeth"
HEART_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.heart"
RIGHT_RAMP_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.right-ramp"
BAT_O_METER_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.illuminated-whitewood"
TWO_SLOT_DOOR_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.cabinet-front-5"
ONE_SLOT_DOOR_PHOTO_SOURCE = "ipdb-photo.gottlieb.class-of-1812.1991.cabinet-front-24"
RUNTIME_SOURCE = "runtime.class-of-1812.clas1812-service-tests"
SCRIPT_SOURCE = "vpx-script.class-of-1812-nztt-1-0"
LATER_SCRIPT_SOURCE = "vpx-script.class-of-1812-3-0-21"
VPM_LIBRARY_SOURCE = "vpm-script-library.class1812-vbs"
VPM_LIBRARY_URI = "external:pinmame-review-artifacts/vpm-script-libs/Class1812.vbs"
VPM_LIBRARY_SHA256 = "61fd1d667b910cf003b7eef6f2aec5afefcbfd24dd46637242c7659c055e36e3"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

TABLE_SCRIPTS_REPOSITORY = "https://github.com/sverrewl/vpxtable_scripts"
TABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
SCRIPT_PATH = "Class of 1812  - NZ&TT 1.0.vbs"
LATER_SCRIPT_PATH = "special_audiopan_and_audiofade_patched/Class of 1812 (Gottlieb 1991) v3.0.21.vbs"
# The pinned Git blobs; each checkout materializes byte-identical files.
SCRIPT_SHA256 = "b045899dfc7356c5c6c7a3cb19f89cdead062b48c86ce3b66a71c452ae3e3e65"
LATER_SCRIPT_SHA256 = "214ee041c554a2aedb61e7699a57fabf1e7869948d494a3a9f48d93041c83cd3"

IPDB_PAGE_SHA256 = "bf4b7c64e9d8e9169d22cc392b63624d95be7731676d4bd0ca3ee475aab829d4"
IPDB_PAGE_CAPTURE = "20241211163504"
CARDS_ZIP_NAME = "Gottlieb_1991_Class_of_1812_Reproduction_Score_and_Instruction_Cards_Including_French.zip"
CARDS_ZIP_SHA256 = "9defdeb17247db5023d8afd87c02fd73126b49692ca988ac76e95af0d1560e49"
CARDS_ZIP_CAPTURE = "20180814233009"
CARDS_PDF_SHA256 = "af6e107d7b0e896555c9fc8b5b90a94c9b55086eb05ba3c74f41db5991d6404b"
# IPDB photo number: (Wayback capture, SHA-256 of the retained JPEG, IPDB caption).
# IPDB photo number: (Wayback capture, SHA-256, caption, size, photographer as the page credits them).
PHOTOS = {
	5: ("20180816012329", "004db446ee40e6c80477964eae76fb7129684402e13b9b587daedc9cb8879db9", "Cabinet - Front", "800x600", "Gregory Bousquet"),
	11: ("20180816012342", "d32d60dffb64bdf3e9ffa2512b86cb1695d14809ada1e6b5087665a8a9ec3f4a", "Right Ramp", "800x600", "Gregory Bousquet"),
	12: ("20180816012334", "44532a4e48027c976b1f4a1b4159372c4a516f5e9582be6897fc6fd166df9511", "Mechanical Chattering Teeth", "800x600", "Gregory Bousquet"),
	13: ("20180816012339", "aefe59867fe91b002da2d8f2cd68d4525145f8bc95af5e11c0f544d725f22445", "Mechanical Beating Heart", "800x600", "Gregory Bousquet"),
	19: ("20180816012336", "e90123b1910729ff6854f9a6eb35f196f1e9a4f3ad154e13f65db5c2eab16e61", "Illuminated Whitewood", "1200x1600", "Philippe Thibault"),
	24: ("20180816012341", "13a4f52c37db19370aa0568e04e813adf3fa19bc0b9e2f61c73e775145c63963", "Cabinet - Front", "1024x761", "Jean-Pierre Renault"),
}

# The retained table: tom tower & ninuzzu's NZ&TT 1.0, under the working root's vpx-sources.
VPX_TABLE_SOURCE = "vpx-table.class-of-1812-nztt-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.class-of-1812-nztt-1-0"
VPX_OBJ_SOURCE = "vpx-obj-export.class-of-1812-nztt-1-0"
VPX_DIRECTORY = Path("gottlieb/class-of-1812-1991/nztt-1.0")
TABLE_FILENAME = "Class of 1812  - NZ&TT 1.0.vpx"
TABLE_RELATIVE_PATH = VPX_DIRECTORY / "source" / TABLE_FILENAME
TABLE_SHA256 = "27e1842e63714b2507aa828c1f8751a0324f756259b453ddc8c8d95583cc1500"
TABLE_BYTES = 54398976
# The embedded script as vpxtool extracts it (36,614 bytes).
EMBEDDED_SCRIPT_SHA256 = "ff98cc7740b1b81cedf0322090034879fc66ce8906759f8d5e897c00e1ac1914"
EXTRACTION_RELATIVE_PATH = VPX_DIRECTORY / "extracted-vpxtool"
EXTRACTION_MANIFEST_RELATIVE_PATH = VPX_DIRECTORY / "extracted-vpxtool.manifest.json"
EXTRACTION_FILE_COUNT = 1320
EXTRACTION_TOTAL_BYTES = 68838044
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "66c1a607486f804c3cdd14bf8f8c0e240b3ad42978280e5a7e63f408fcaa3f0f"
OBJ_RELATIVE_PATH = VPX_DIRECTORY / "export-obj-vpu" / "Class of 1812  - NZ&TT 1.0.obj"
OBJ_SHA256 = "72f51ce7240f8f21ad4d397831b86777d5a196d26f455cf1f09b2eafdeabc35c"
VPXTOOL_VERSION = "vpxtool git:v0.33.3"

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0
TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"

# (left, right) in the driver's own FLIP_SWNO macro order (FLIP67).
FLIP_SWNO = (6, 7)

DRIVER_IDS = ("clas1812",)
DRIVER_COMPATIBILITY = {
	"clas1812": (
		"identical",
		"The only physical Class of 1812 driver (gprom.bin with the yrom1, drom1, arom1 and arom2 sound ROMs), declared "
		"INITGAME(clas1812, ALPHA, FLIP67, 3/*?*/, SNDBRD_GTS3, 4) in pinned src/wpc/gts3games.c lines 217-226 and catalogued "
		"with CORE_GAMEDEFNV(clas1812, \"Class of 1812\", 1991, \"Gottlieb\", mGTS3S, 0). Its power-up screen reads CLASS OF "
		"1812 / 730 88FB, and 730 is IPDB's model number for the machine. Every runtime probe here ran on it, and the "
		"known-working script loads it (cGameName = \"clas1812\"). Its only clone, beav_butt, is a VPX-only reskin that "
		"scope.py excludes.",
	),
}

# --- Switches. Public addresses are Gottlieb's own decimal numbers (gts3_sw2m): tens digit strobe, units digit return.
# ROM_SWITCH_NAMES is the name the Switch Matrix Test (self-test 6) displays while the host holds the address at 1.
ROM_SWITCH_NAMES = {
	0: "LEFT COIN CHUTE", 1: "RIGHT COIN CHUTE", 2: "CENTER COIN CHUTE", 4: "L WHITE BUTTON", 5: "R WHITE BUTTON",
	6: "LEFT FLIPPER", 7: "RIGHT FLIPPER", 10: "LEFT POP BUMPER", 11: "TOP POP BUMPER", 12: "BOTTOM POP BUMPER",
	13: "L KICKING RUBBER", 14: "R KICKING RUBBER", 15: "SPINNER", 16: "L DROP TARGET 1", 17: "R DROP TARGET 1",
	20: "L SPOT TARGET 1", 21: "C SPOT TARGET 1", 22: "R SPOT TARGET 1", 23: "LEFT RTN ROLLOVER", 24: "RIGHT RTN ROLLOVR",
	25: "TOP ROLLOVER 1", 26: "L DROP TARGET 2", 27: "R DROP TARGET 2", 30: "L SPOT TARGET 2", 31: "C SPOT TARGET 2",
	32: "R SPOT TARGET 2", 33: "LEFT OUT ROLLOVER", 34: "RIGHT OUT ROLLOVR", 35: "TOP ROLLOVER 2", 36: "L DROP TARGET 3",
	37: "R DROP TARGET 3", 40: "L SPOT TARGET 3", 41: "C SPOT TARGET 3", 42: "R SPOT TARGET 3", 43: "SHOOTER LANE",
	44: "TROUGH", 45: "TOP ROLLOVER 3", 46: "L DROP TARGET 4", 47: "R DROP TARGET 4", 50: "RIGHT RAMP", 51: "LEFT RAMP",
	52: "BOTTOM UPKICKER", 53: "TOP KICKER", 54: "OUTHOLE", 55: "TOP KICKER RO",
}
MATRIX_ADDRESSES = tuple(column * 10 + row for column in range(12) for row in range(8))
UNUSED_SWITCHES = frozenset(address for address in MATRIX_ADDRESSES if address not in ROM_SWITCH_NAMES and address != 3)
SWITCH_LABELS = {
	0: "Left Coin Chute", 1: "Right Coin Chute", 2: "Center Coin Chute", 3: "Credit Button (Start)",
	4: "Left White Button", 5: "Right White Button", 6: "Left Flipper (Matrix Copy)", 7: "Right Flipper (Matrix Copy)",
	10: "Left Pop Bumper", 11: "Top Pop Bumper", 12: "Bottom Pop Bumper", 13: "Left Kicking Rubber",
	14: "Right Kicking Rubber", 15: "Spinner",
	16: "Left Drop Target 1", 26: "Left Drop Target 2", 36: "Left Drop Target 3", 46: "Left Drop Target 4",
	17: "Right Drop Target 1", 27: "Right Drop Target 2", 37: "Right Drop Target 3", 47: "Right Drop Target 4",
	20: "Left Spot Target 1", 30: "Left Spot Target 2", 40: "Left Spot Target 3",
	21: "Center Spot Target 1", 31: "Center Spot Target 2", 41: "Center Spot Target 3",
	22: "Right Spot Target 1", 32: "Right Spot Target 2", 42: "Right Spot Target 3",
	23: "Left Return Rollover", 24: "Right Return Rollover", 33: "Left Outlane Rollover", 34: "Right Outlane Rollover",
	25: "Top Rollover 1", 35: "Top Rollover 2", 45: "Top Rollover 3", 43: "Shooter Lane", 44: "Trough",
	50: "Right Ramp", 51: "Left Ramp", 52: "Bottom Upkicker", 53: "Top Kicker", 54: "Outhole", 55: "Top Kicker Rollover",
}
CABINET_SWITCH_ROLES = {
	0: "cabinet.coin", 1: "cabinet.coin", 2: "cabinet.coin", 3: "cabinet.start", 4: "cabinet.service", 5: "cabinet.service",
	6: "cabinet.flipper", 7: "cabinet.flipper",
}
CABINET_SWITCH_TYPES = {3: "button", 4: "button", 5: "button"}
# What the ROM did with the address at 1 outside the Switch Matrix Test.
ROM_RUNTIME = {
	0: "the Front Door Test counted a coin on the left chute (L) for each of two pulses at 1 (run front-door)",
	1: "the Front Door Test counted a coin on the right chute (R) for the pulse at 1 (run front-door), and in attract mode the first pulse brought up INSERT ANOTHER COIN and the second gave one credit (run gameplay)",
	2: "the Front Door Test counted a coin on the center chute (C) for the pulse at 1 (run front-door)",
	3: "with one credit a pulse at 1 started a game: the ROM reset both drop-target banks (8, 9), energized the Q relay (32) and pulsed the ball release (28) (run gameplay)",
	10: "40 ms pulses at 1 during a game made the ROM fire 1, LEFT POP BUMPER (run gameplay)",
	11: "40 ms pulses at 1 during a game made the ROM fire 2, TOP POP BUMPER (run gameplay)",
	12: "40 ms pulses at 1 during a game made the ROM fire 3, BOTTOM POP BUMPER (run gameplay)",
	13: "40 ms pulses at 1 during a game made the ROM fire 4, L KICKING RUBBER (run gameplay)",
	14: "40 ms pulses at 1 during a game made the ROM fire 5, R KICKING RUBBER (run gameplay)",
	15: "each of two pulses at 1 during a game scored 5,000 (run gameplay)",
	46: "with 16, 26 and 36 already held at 1 during a game, raising it made the ROM fire 8, LEFT DROP T BANK, and the display began a COUNTDOWN (run gameplay)",
	47: "with 17, 27 and 37 already held at 1 during a game, raising it made the ROM fire 9, RIGHT DROP T BANK, seven times in about 2.7 s while the host kept all four at 1 (run gameplay)",
	45: "pulsed during a game after 25 and 35, it set off a display animation that by the next step read YOU ADVANCED MULTIPLIER (run gameplay); the instruction cards advance the multiplier by completing the top rollovers",
	44: (
		"held at 1 before Start, the ROM released a ball (28) at Start; after the drain, once the host had closed it again, "
		"the ROM fired 29, 8, 9 and 28 and energized 32, and ball 2 began (run gameplay). Two tilt probes differ only in "
		"this switch. Held at 1 for the whole game, the ROM took the second tilt-switch pulse as a tilt, raised the relays "
		"26 and 31 and moved the display straight on to ball 2; within the next step it reset both banks, energized 32 and "
		"released a ball (28) while the tilted ball was still out and the outhole switch 54 open, and the fifth and sixth "
		"pulses did the same for ball 3 (run tilt-trough-closed). Opened once the ball was released, the ROM tilted on the "
		"same pulse and showed TILT, released nothing while 44 stayed open, kicked the outhole (29) when 54 rose, and "
		"served ball 2 only after the host had closed 44 again (run tilt-trough-open). The ROM thus reads 44 at 1 as both "
		"balls home in the trough: the switch is closed only while both balls are there"
	),
	52: "held at 1 for 8 s during a game, the ROM fired 6, BOTTOM UPKICKER, six times at intervals of about 0.7 s (run gameplay)",
	53: "held at 1 for 8 s during a game, the ROM fired 7, TOP KICKER, eight times at intervals of about 0.9 s (run gameplay)",
	54: "when it rose to 1 during a game the ROM released the Q relay (32) and the display read YOU DUG UP 1 STIFF (run gameplay)",
}
ROM_RUNTIME[16] = ROM_RUNTIME[26] = ROM_RUNTIME[36] = "held at 1 one after another during a game, the fourth target of the bank (46) made the ROM fire its reset 8 (run gameplay)"
ROM_RUNTIME[17] = ROM_RUNTIME[27] = ROM_RUNTIME[37] = "held at 1 one after another during a game, the fourth target of the bank (47) made the ROM fire its reset 9 (run gameplay)"
ROM_RUNTIME[25] = ROM_RUNTIME[35] = "pulsed in turn with the other two top rollovers during a game, the third (45) set off a display animation that by the next step read YOU ADVANCED MULTIPLIER (run gameplay)"
# The known-working script's writer for each playfield switch.
SCRIPT_WRITERS = {
	10: "sw10_Hit pulses it (line 375)", 11: "sw11_Hit pulses it (line 376)", 12: "sw12_Hit pulses it (line 377)",
	13: "sw13_Slingshot pulses it (line 383)", 14: "sw14_Slingshot pulses it (line 402)",
	15: "sw15_Spin pulses it on each spinner turn (line 420)",
	**{address: "the dtBankL drop target object writes it, 1 while the target is down (lines 132-137 and 423-426)" for address in (16, 26, 36, 46)},
	**{address: "the dtBankR drop target object writes it, 1 while the target is down (lines 139-144 and 428-431)" for address in (17, 27, 37, 47)},
	20: "Sw20_Hit pulses it (line 434)", 30: "Sw30_Hit pulses it (line 435)", 40: "Sw40_Hit pulses it (line 436)",
	21: "Sw21_Hit pulses it (line 438)", 31: "Sw31_Hit pulses it (line 439)", 41: "Sw41_Hit pulses it (line 440)",
	22: "Sw22_Hit pulses it (line 442)", 32: "Sw32_Hit pulses it (line 443)", 42: "Sw42_Hit pulses it (line 444)",
	23: "Sw23_Hit writes 1 and Sw23_UnHit 0 (lines 447-448)", 24: "Sw24_Hit writes 1 and Sw24_UnHit 0 (lines 449-450)",
	25: "Sw25_Hit writes 1 and Sw25_UnHit 0 (lines 451-452)", 33: "Sw33_Hit writes 1 and Sw33_UnHit 0 (lines 454-455)",
	34: "Sw34_Hit writes 1 and Sw34_UnHit 0 (lines 456-457)", 35: "Sw35_Hit writes 1 and Sw35_UnHit 0 (lines 458-459)",
	43: "Sw43_Hit writes 1 and Sw43_UnHit 0 (lines 460-461)", 45: "Sw45_Hit writes 1 and Sw45_UnHit 0 (lines 462-463)",
	55: "Sw55_Hit writes 1 and Sw55_UnHit 0 (lines 464-465)",
	50: "Sw50_Hit pulses it (line 467)", 51: "Sw51_Hit pulses it (line 468)",
	52: "the bsScoop saucer holds it at 1 while a ball sits in Kicker sw52 (lines 116-122)",
	53: "the bsTK saucer holds it at 1 while a ball sits in Kicker sw53k (lines 124-130); the table's Trigger sw53 beside it has no handler",
	44: (
		"Slot1_Hit writes 1 and Slot1_UnHit 0, and InitTrough sets it to 1 with both balls in the trough (lines 226-236). "
		"Slot1 is the release, so this table keeps 44 at 1 while one ball waits there and the other is in play, which the "
		"probes above show the ROM reads as both balls home: a defect in that table. Its 3.0.21 update writes 44 from "
		"Slot2_Hit and Slot2_UnHit, the second position behind the release (lines 789-790), and its changelog reports too "
		"many balls on the table in tilt mode and says the original's Slot1 and Slot2 subroutines were reversed, which "
		"caused its trough, tilt and multiball faults (lines 4602-4611)"
	),
	54: "Drain_Hit writes 1 and Drain_UnHit 0 (lines 249-257)",
}

# --- Solenoids. ROM_COIL_NAMES[public] is the Relay+Solenoid Test's name for driver (public - 1).
ROM_COIL_NAMES = {
	1: "LEFT POP BUMPER", 2: "TOP POP BUMPER", 3: "BOTTOM POP BUMPER", 4: "L KICKING RUBBER", 5: "R KICKING RUBBER",
	6: "BOTTOM UPKICKER", 7: "TOP KICKER", 8: "LEFT DROP T BANK", 9: "RIGHT DROP T BANK", 10: "GATE", 11: "HEART",
	12: "TEETH", 13: "LIGHTNING 67 (3)", 14: "WILLY WOOF 67 (2)", 15: "LA GHOST 67 (2)", 16: "VAMP 67 (2)",
	17: "MUMSY 67 (2)", 18: "ZOM B 67 (2)", 19: "ZOM B KILT 67 (2)", 20: "CLEAVER 67 (2)", 21: "PIECEMEAL 67 (2)",
	22: "RAMP 1 67", 23: "RAMP 2 67", 24: "RAMP 3 67", 25: "HEART 67 (2)", 26: "\"A\" RELAY", 27: "COIN MET/TIX COIL",
	28: "BALL RELEASE", 29: "OUTHOLE", 30: "KNOCKER", 31: "\"T\" RELAY", 32: "\"Q\" RELAY",
}
SOLENOID_LABELS = {
	1: "Left Pop Bumper", 2: "Top Pop Bumper", 3: "Bottom Pop Bumper", 4: "Left Kicking Rubber Coil",
	5: "Right Kicking Rubber Coil", 6: "Bottom Upkicker Coil", 7: "Top Kicker Coil", 8: "Left Drop Target Bank Reset",
	9: "Right Drop Target Bank Reset", 10: "Gate", 11: "Heart", 12: "Teeth", 13: "Lightning Flasher",
	14: "Willy Woof Flasher", 15: "LA Ghost Flasher", 16: "Vamp Flasher", 17: "Mumsy Flasher", 18: "Zom B Flasher",
	19: "Zom B Kilt Flasher", 20: "Cleaver Flasher", 21: "Piecemeal Flasher", 22: "Ramp 1 Flasher", 23: "Ramp 2 Flasher",
	24: "Ramp 3 Flasher", 25: "Heart Flasher", 26: "A Relay (Lightbox)", 27: "Coin Meter/Ticket Coil", 28: "Ball Release",
	29: "Outhole Kicker", 30: "Knocker", 31: "T Relay (General Illumination)", 32: "Q Relay (Game On)",
}
FLASHER_SOLENOIDS = frozenset(range(13, 26))
# Flashers the known-working script leaves unbound as backbox flashers (line 180: "(**) Used in backbox (translite)").
BACKBOX_SCRIPT_FLASHERS = frozenset(range(13, 22))
SOLENOID_KIND = {26: "relay", 31: "relay", 32: "relay"}
SOLENOID_CALLBACKS = {
	6: "SolVUK (line 187), which kicks the ball out of the bsScoop saucer at Kicker sw52 and raises the sw52p primitive (lines 309-318)",
	7: "bsTK.SolOut (line 188), which kicks the ball out of the bsTK saucer at Kicker sw53k",
	8: "dtBankL.SolDropUp (line 189), which raises the left bank's four targets 16, 26, 36 and 46",
	9: "dtBankR.SolDropUp (line 190), which raises the right bank's four targets 17, 27, 37 and 47",
	10: "SolDiv (line 191), which turns the DiverterP primitive about its stored position and swaps which of the walls DiverterOn and DiverterOff is collidable: on while the output is on, off when it turns off (lines 323-344)",
	11: "SolHeart (line 192), which pumps the heart primitive once each time the output turns on (lines 346-360)",
	12: "SolTeeth (line 193), which holds the BottomTeeth jaw at RotX 0 while the output is on and at -25 while it is off (lines 362-368)",
	22: "SetLamp 152 (line 205), which LampTimer draws on the domes domeYB and domeW and the Lights F22 and F22a under them (lines 547-554)",
	23: "SetLamp 153 (line 206), which LampTimer draws on the domes domeYT and domeR and the Lights F22x and F23 under them (lines 555-561)",
	24: "SetLamp 154 (line 207), which LampTimer draws on Light F24 under the ramp and on the dome domeB with Light F24a under it (lines 562-566)",
	25: "SetLamp 155 (line 208), which LampTimer draws on the F25 flasher sprite and the heart primitive's texture (lines 567-568)",
	26: "GIRelay (line 210, commented 'LightBox Relay'), which turns the table's GI collection off while the relay is on (lines 474-486)",
	27: "an empty callback (line 211)",
	28: "ReleaseBall (line 212), which kicks the lead ball out of Kicker Slot1 (lines 268-274)",
	29: "SolOuthole (line 213), which kicks the ball out of the Drain kicker (lines 259-266)",
	30: "SolKnocker (line 214), a sound only",
	31: "TiltRelay (line 215), which turns the table's GI collection off while the relay is on (lines 488-500)",
	32: "vpmNudge.SolGameOn (line 216)",
}
SOLENOID_RUNTIME = {
	1: "fired on 40 ms pulses of its switch 10 during a game (run gameplay)",
	2: "fired on 40 ms pulses of its switch 11 during a game (run gameplay)",
	3: "fired on 40 ms pulses of its switch 12 during a game (run gameplay)",
	4: "fired on 40 ms pulses of its switch 13 during a game (run gameplay)",
	5: "fired on 40 ms pulses of its switch 14 during a game (run gameplay)",
	6: "fired six times, about every 0.7 s, while switch 52 was held at 1 for 8 s (run gameplay)",
	7: "fired eight times, about every 0.9 s, while switch 53 was held at 1 for 8 s (run gameplay)",
	8: "fired at Start, when the last left target (46) went down, once more when the host pulsed spot target 22, and again when the ROM served ball 2 (run gameplay)",
	9: "fired at Start, seven times while the four right targets were held down, and again when the ROM served ball 2 (run gameplay)",
	12: "fired in two bursts of pulses: sixteen from about 2.5 s to 8.2 s after Start, the first held about 1.1 s and the others 0.06-0.34 s, and thirteen of 0.06-0.07 s each over about 1.7 s, beginning within 0.1 s of the first of two spinner pulses 0.8 s apart (run gameplay)",
	26: "rose with the flashers when the left bank was completed, on the first five of the nine spot-target hits and at the top-rollover multiplier advance (run gameplay)",
	28: (
		"was energized for about 0.5 s at Start and again when the ROM served ball 2 (run gameplay). With the trough switch "
		"44 held at 1 throughout, it was also energized in the steps of tilt-switch pulses 3 and 6, each time with the "
		"tilted ball still out, and twice more, alternating with 29, once the outhole switch 54 rose (run "
		"tilt-trough-closed); with 44 opened after the release, it was energized after the drain only once 44 had closed "
		"again (run tilt-trough-open)"
	),
	29: (
		"fired once after the drain, when the host had opened the outhole switch 54 and closed the trough switch 44 again "
		"(run gameplay). After a tilt with 44 open it fired four times, about every 0.65 s, while the host held 54 at 1 for "
		"3 s (run tilt-trough-open); with 44 held at 1 it fired twice, alternating with 28, while 54 was at 1 (run "
		"tilt-trough-closed)"
	),
	31: "rose at Start, and with 26 when the left bank was completed and on the first five of the nine spot-target hits (run gameplay)",
	32: "rose at Start, fell when the outhole switch 54 rose, and rose again when the ROM served ball 2 (run gameplay)",
}
CABINET_SOLENOIDS = {
	26: "relay in the cabinet or backbox; the load it switches is the backbox lightbox illumination",
	27: "cabinet",
	30: "cabinet",
	32: "relay in the cabinet or backbox; it enables the flipper circuit",
}

# --- Lamps. ROM_LAMP_NAMES is the Lamp Matrix Test's name for each lamp =nn (A0-B7 = 100-117) it blinked.
ROM_LAMP_NAMES = {
	0: "SHOOT AGAIN", 2: "TEETH", 3: "L OUTLANE EX BALL", 4: "R OUTLANE EX BALL", 5: "TOP LEFT EX BALL", 6: "TOP SPECIAL",
	7: "TOP RIGHT EX BALL", 10: "BATOMETER 5,000", 11: "BATOMETER 10,000", 12: "BATOMETER 20,000", 13: "BATOMETER EX BALL",
	14: "BATOMETER SPECIAL", 15: "TOP LANE 1", 16: "TOP LANE 2", 17: "TOP LANE 3", 20: "2X", 21: "3X", 22: "4X", 23: "5X",
	25: "C SPOT TARGET 1", 26: "C SPOT TARGET 2", 27: "C SPOT TARGET 3", 30: "L RAMP 1", 31: "L RAMP 2", 32: "L RAMP 3",
	33: "R RAMP 1", 34: "R RAMP 2", 35: "R RAMP 3", 36: "L BB ADD LETTER", 37: "L BB MILLION", 40: "C", 41: "O", 42: "F",
	43: "F", 44: "I", 45: "N", 46: "R BB ADD LETTER", 47: "R BB LOCK", 50: "B UPKICKER GRAVE", 51: "R SPOT TARGET 1",
	52: "R SPOT TARGET 2", 53: "R SPOT TARGET 3", 54: "R DT MILLIONS", 55: "R DT DOOR PRIZE", 56: "R RETURN LANE",
	57: "R RAMP MILLION", 60: "UPKCKR DOOR PRIZE", 61: "L SPOT TARGET 1", 62: "L SPOT TARGET 2", 63: "L SPOT TARGET 3",
	64: "L DT ZOM B BONUS", 65: "L DT LIGHT LOCK", 66: "L RETURN LANE", 67: "CRYPT MILLION", 70: "ZOM B CIRCLE 1",
	71: "ZOM B CIRCLE 2", 72: "ZOM B CIRCLE 3", 73: "ZOM B CIRCLE 4", 74: "GROVER CIRCLE 1", 75: "GROVER CIRCLE 2",
	76: "GROVER CIRCLE 3", 77: "GROVER CIRCLE 4", 80: "W WOOF TOMBSTONE", 81: "BELLY TOMBSTONE", 82: "VAMP TOMBSTONE",
	83: "PETER P TOMBSTONE", 84: "MUMSY TOMBSTONE", 85: "SPECIAL", 86: "BONUS 13", 90: "BONUS 7", 91: "BONUS 8",
	92: "BONUS 9", 93: "BONUS 12", 94: "BONUS 14", 95: "BONUS 17", 96: "BONUS 18", 97: "BONUS 19", 100: "BONUS 1",
	101: "BONUS 2", 102: "BONUS 3", 103: "BONUS 4", 104: "BONUS 5", 105: "BONUS 6", 106: "BONUS 10", 107: "BONUS 11",
	110: "BONUS 15", 111: "BONUS 16", 112: "BONUS 20", 113: "BONUS 21", 114: "BONUS 22", 115: "BONUS 23", 116: "BONUS 24",
	117: "BONUS 25",
}
LAMP_ADDRESSES = MATRIX_ADDRESSES
LAMP_LABELS = {
	0: "Shoot Again", 2: "Teeth", 3: "Left Outlane Extra Ball", 4: "Right Outlane Extra Ball", 5: "Top Left Extra Ball",
	6: "Top Special", 7: "Top Right Extra Ball", 10: "Bat-O-Meter 5,000", 11: "Bat-O-Meter 10,000", 12: "Bat-O-Meter 20,000",
	13: "Bat-O-Meter Extra Ball", 14: "Bat-O-Meter Special", 15: "Top Lane 1", 16: "Top Lane 2", 17: "Top Lane 3",
	20: "Multiplier 2X", 21: "Multiplier 3X", 22: "Multiplier 4X", 23: "Multiplier 5X",
	25: "Center Spot Target 1", 26: "Center Spot Target 2", 27: "Center Spot Target 3",
	30: "Left Ramp 1", 31: "Left Ramp 2", 32: "Left Ramp 3", 33: "Right Ramp 1", 34: "Right Ramp 2", 35: "Right Ramp 3",
	36: "Left BB Add Letter", 37: "Left BB Million", 40: "Coffin Letter C", 41: "Coffin Letter O",
	42: "Coffin Letter F (First)", 43: "Coffin Letter F (Second)", 44: "Coffin Letter I", 45: "Coffin Letter N",
	46: "Right BB Add Letter", 47: "Right BB Lock", 50: "Bottom Upkicker Grave", 51: "Right Spot Target 1",
	52: "Right Spot Target 2", 53: "Right Spot Target 3", 54: "Right Drop Targets Millions",
	55: "Right Drop Targets Door Prize", 56: "Right Return Lane", 57: "Right Ramp Million", 60: "Upkicker Door Prize",
	61: "Left Spot Target 1", 62: "Left Spot Target 2", 63: "Left Spot Target 3", 64: "Left Drop Targets Zom B Bonus",
	65: "Left Drop Targets Light Lock", 66: "Left Return Lane", 67: "Crypt Million",
	70: "Zom B Circle 1", 71: "Zom B Circle 2", 72: "Zom B Circle 3", 73: "Zom B Circle 4",
	74: "Grover Circle 1", 75: "Grover Circle 2", 76: "Grover Circle 3", 77: "Grover Circle 4",
	80: "W Woof Tombstone", 81: "Belly Tombstone", 82: "Vamp Tombstone", 83: "Peter P Tombstone", 84: "Mumsy Tombstone",
	85: "Special",
	**{address: f"Bonus {ROM_LAMP_NAMES[address].split()[1]}" for address in (86, 90, 91, 92, 93, 94, 95, 96, 97, 100, 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 114, 115, 116, 117)},
}
# Lamps PinMAME's clas1812 block types as strobed LEDs (gts3.c line 552): the Bat-O-Meter.
LED_LAMPS = frozenset(range(10, 15))

# --- Placements. Retained-table objects as (item type, x, y) in VPX units: a Wall's drag-point mean, a HitTarget's or
# Primitive's stored position, otherwise the stored centre. verify_retained_table re-derives every value.
TABLE_POINTS: dict[str, tuple[str, float, float]] = {
	"sw10": ("Bumper", 431.34116, 426.20593), "sw11": ("Bumper", 635.9831, 350.3542), "sw12": ("Bumper", 597.2671, 568.4282),
	"sw13": ("Wall", 220.29066, 1325.7377999999999), "sw14": ("Wall", 641.5223025, 1322.159425),
	"sw15": ("Spinner", 132.31686, 653.5003),
	"sw16": ("HitTarget", 104.72444, 988.6161), "sw26": ("HitTarget", 108.99944, 933.6987),
	"sw36": ("HitTarget", 113.60331, 876.4794), "sw46": ("HitTarget", 119.1937, 816.6293),
	"sw17": ("HitTarget", 744.3315, 816.7936), "sw27": ("HitTarget", 749.2642, 874.25946),
	"sw37": ("HitTarget", 754.1969, 930.9856), "sw47": ("HitTarget", 758.883, 987.7117),
	"sw20": ("HitTarget", 83.70397, 951.2443), "sw30": ("HitTarget", 88.12606, 894.06934), "sw40": ("HitTarget", 91.71574, 842.3048),
	"sw21": ("HitTarget", 373.22195, 593.64136), "sw31": ("HitTarget", 386.1557, 562.2307), "sw41": ("HitTarget", 399.70538, 532.05206),
	"sw22": ("HitTarget", 773.78577, 840.2449), "sw32": ("HitTarget", 778.58075, 894.0025), "sw42": ("HitTarget", 784.057, 957.0473),
	"sw23": ("Trigger", 123.56657, 1352.0946), "sw24": ("Trigger", 738.4374, 1348.905), "sw25": ("Trigger", 431.4655, 201.02963),
	"sw33": ("Trigger", 57.548492, 1350.0902), "sw34": ("Trigger", 804.45544, 1350.9094), "sw35": ("Trigger", 506.73105, 201.02965),
	"sw43": ("Trigger", 891.02606, 1682.1818), "sw45": ("Trigger", 582.67847, 201.00935), "sw50": ("Trigger", 698.5091, 124.301994),
	"sw51": ("Trigger", 61.133293, 130.25858), "sw55": ("Trigger", 343.77905, 160.14267),
	"sw52": ("Kicker", 548.87244, 718.1749), "sw53k": ("Kicker", 308.4339, 461.5646), "Drain": ("Kicker", 440.50513, 1855.7125),
	"Slot1": ("Kicker", 724.0075, 1700.1406), "Slot2": ("Kicker", 665.3572, 1727.1392),
	"DiverterP": ("Primitive", 332.0, 272.0),
	"l0": ("Light", 432.62592, 1565.5332), "l3": ("Light", 56.288364, 1245.1945), "l4": ("Light", 806.70135, 1242.3851),
	"l5": ("Light", 435.05295, 63.098286), "l6": ("Light", 511.45892, 61.27548), "l7": ("Light", 592.11816, 59.604572),
	"l15": ("Light", 400.27554, 86.02734), "l16": ("Light", 479.73837, 85.77101), "l17": ("Light", 555.61273, 86.02734),
	"l20": ("Light", 434.20886, 1326.2797), "l21": ("Light", 392.3268, 1368.0624), "l22": ("Light", 478.21042, 1367.7208),
	"l23": ("Light", 435.46555, 1409.1626),
	"l25": ("Light", 448.60953, 676.3314), "l26": ("Light", 462.00897, 631.8858), "l27": ("Light", 478.87885, 588.08905),
	"l30": ("Light", 338.1512, 829.82556), "l31": ("Light", 321.9207, 776.8954), "l32": ("Light", 300.59225, 716.8945),
	"l33": ("Light", 706.9414, 637.94476), "l34": ("Light", 727.6915, 580.62555), "l35": ("Light", 746.42096, 521.9746),
	"L36": ("Light", 260.67282, 673.9188), "L37": ("Light", 314.89874, 654.9652),
	"l40": ("Light", 326.09283, 1382.1764), "l41": ("Light", 361.8379, 1444.1362), "l42": ("Light", 395.08524, 1505.1084),
	"l43": ("Light", 468.7622, 1503.7908), "l44": ("Light", 502.16522, 1441.2941), "l45": ("Light", 536.25995, 1383.1566),
	"L46": ("Light", 734.1385, 461.4291), "L47": ("Light", 790.86084, 480.39175),
	"l50": ("Light", 557.10394, 803.04395), "l51": ("Light", 674.4598, 848.84607), "l52": ("Light", 707.58215, 907.0681),
	"l53": ("Light", 684.50604, 965.1782), "l54": ("Light", 616.38403, 865.38556), "l55": ("Light", 624.19293, 967.2836),
	"l56": ("Light", 739.32916, 1242.4644), "l57": ("Light", 687.7615, 700.9407),
	"l60": ("Light", 474.97446, 774.0489), "l61": ("Light", 181.54128, 966.95764), "l62": ("Light", 162.11249, 906.2718),
	"l63": ("Light", 194.94383, 851.1078), "l64": ("Light", 250.57713, 869.1375), "l65": ("Light", 241.61302, 967.548),
	"l66": ("Light", 123.48255, 1245.0107), "L67": ("Light", 382.2024, 53.84225),
	"l70": ("Light", 153.21771, 1118.4634), "l71": ("Light", 199.56506, 1080.1902), "l72": ("Light", 241.97615, 1120.5436),
	"l73": ("Light", 203.85461, 1169.5598), "l74": ("Light", 618.6954, 1120.711), "l75": ("Light", 666.23865, 1072.1045),
	"l76": ("Light", 709.05817, 1113.912), "l77": ("Light", 664.185, 1160.5664),
	"l80": ("Light", 327.23633, 946.00433), "l81": ("Light", 370.71365, 901.4016), "l82": ("Light", 431.5557, 885.91223),
	"l83": ("Light", 492.33057, 900.7248), "l84": ("Light", 536.1028, 946.5046), "l85": ("Light", 433.08807, 949.9709),
	"l86": ("Light", 428.5661, 1126.1685),
	"l90": ("Light", 375.515, 1071.5498), "l91": ("Light", 435.2848, 1067.7041), "l92": ("Light", 490.88358, 1065.6566),
	"l93": ("Light", 373.29477, 1128.6385), "l94": ("Light", 488.40332, 1126.3512), "l95": ("Light", 371.91968, 1189.6052),
	"l96": ("Light", 430.2263, 1186.5515), "l97": ("Light", 490.19122, 1187.877),
	"l100": ("Light", 313.73447, 1006.4357), "l101": ("Light", 373.23828, 1006.6065), "l102": ("Light", 431.4203, 1007.33514),
	"l103": ("Light", 489.59927, 1005.33997), "l104": ("Light", 548.25543, 1007.5129), "l105": ("Light", 315.285, 1067.2394),
	"l106": ("Light", 547.7653, 1066.8965), "l107": ("Light", 315.89224, 1128.0178),
	"l110": ("Light", 546.45654, 1128.1582), "l111": ("Light", 314.8806, 1190.2338), "l112": ("Light", 546.3275, 1188.6406),
	"l113": ("Light", 315.5375, 1251.7742), "l114": ("Light", 374.35388, 1250.2395), "l115": ("Light", 432.41827, 1250.0884),
	"l116": ("Light", 490.15097, 1248.9454), "l117": ("Light", 548.9427, 1250.0431),
	"F22": ("Light", 251.58966, 194.5473), "F22a": ("Light", 826.3066, 80.932144), "F22x": ("Light", 299.58966, 154.5473),
	"F23": ("Light", 883.98517, 440.43835), "F24": ("Light", 190.12376, 502.51755), "F24a": ("Light", 674.6027, 259.50006),
	"light1": ("Light", 671.5541, 1518.3309), "light2": ("Light", 165.2394, 1326.3037), "light3": ("Light", 689.97845, 1329.0038),
	"light4": ("Light", 207.66902, 1404.5614), "light5": ("Light", 149.83705, 1495.7917), "light6": ("Light", 183.66376, 1515.6309),
	"light7": ("Light", 808.7288, 1097.3256), "light8": ("Light", 817.7317, 871.0421), "light9": ("Light", 838.4946, 616.6963),
	"light10": ("Light", 49.940567, 1100.1002), "light11": ("Light", 52.527462, 867.65497), "light12": ("Light", 52.36064, 614.4766),
	"Light13": ("Light", 596.94324, 568.45056), "Light14": ("Light", 432.59756, 427.41354), "light15": ("Light", 647.5488, 1407.2615),
	"Light16": ("Light", 635.2643, 351.1666), "light17": ("Light", 705.3808, 1498.4918), "light18": ("Light", 161.06955, 456.0633),
	"light19": ("Light", 353.53564, 319.95084), "light20": ("Light", 349.84024, 524.42706), "light21": ("Light", 737.85236, 263.2888),
	"light22": ("Light", 245.13869, 195.13016), "light23": ("Light", 160.1457, 313.79218),
}
# Primitives whose stored position is not the part's centre: the world bounding-box centre of each in the retained
# `export obj --units vpu` (OBJ x and y are playfield x and y), rounded to six decimals.
MESH_POINTS: dict[str, tuple[float, float]] = {
	"SLING1": (212.92339, 1324.87335), "SLING2": (647.80165, 1324.5705),
	"heart": (489.313325, -26.773487), "TopTeeth": (226.91764, -9.49342), "BottomTeeth": (227.10639, -23.8483),
	"bulb5": (70.070594, 247.49475), "bulb6": (72.138805, 251.076995), "bulb7": (74.134227, 254.53317),
	"bulb8": (76.205145, 258.12009), "bulb9": (78.718412, 260.80933),
	"bulb1": (260.565765, 674.27243), "bulb2": (314.663605, 654.91885), "bulb3": (734.5213, 461.706935),
	"bulb4": (789.61653, 481.392975), "bulb10": (380.47393, 57.895043),
}
# Toys whose mesh centre lies behind the playfield's rear edge (y < 0): the IPDB photos show both mounted against the
# back panel at the rear of the playfield, so each is clamped to y = 0 with its raw value disclosed.
CLAMPED_TO_REAR = frozenset({"heart", "TopTeeth", "BottomTeeth"})
# The centre of a drop-target bank: the mean of its targets' stored positions, rounded to six decimals.
BANKS = {"left drop-target bank": ("sw16", "sw26", "sw36", "sw46"), "right drop-target bank": ("sw17", "sw27", "sw37", "sw47")}
# The object the embedded script binds to each playfield switch.
SWITCH_OBJECTS = {
	10: "sw10", 11: "sw11", 12: "sw12", 13: "sw13", 14: "sw14", 15: "sw15", 16: "sw16", 26: "sw26", 36: "sw36", 46: "sw46",
	17: "sw17", 27: "sw27", 37: "sw37", 47: "sw47", 20: "sw20", 30: "sw30", 40: "sw40", 21: "sw21", 31: "sw31", 41: "sw41",
	22: "sw22", 32: "sw32", 42: "sw42", 23: "sw23", 24: "sw24", 25: "sw25", 33: "sw33", 34: "sw34", 35: "sw35", 43: "sw43",
	44: "Slot2", 45: "sw45", 50: "sw50", 51: "sw51", 52: "sw52", 53: "sw53k", 54: "Drain", 55: "sw55",
}
# Switches placed on another object than the one the known-working script binds: the trough switch sits at the trough's
# second position, where the 3.0.21 update binds it and the trough probes put it.
SWITCH_OBJECT_NOTES = {
	44: (
		"Kicker Slot2, the trough's second position behind the release Slot1. The known-working script binds 44 to Slot1, "
		"the release, which the trough probes rule out (above); the 3.0.21 update of the same table binds it to Slot2 "
		"(lines 789-790)"
	),
}
SOLENOID_OBJECTS = {
	1: "sw10", 2: "sw11", 3: "sw12", 4: "SLING1", 5: "SLING2", 6: "sw52", 7: "sw53k", 8: "left drop-target bank",
	9: "right drop-target bank", 10: "DiverterP", 11: "heart", 12: "BottomTeeth", 25: "heart", 28: "Slot1", 29: "Drain",
}
SOLENOID_PROJECTED = {
	4: "the left slingshot's kicker arm it drives (Primitive SLING1, which the script moves on the hit); the coil has no object of its own",
	5: "the right slingshot's kicker arm it drives (Primitive SLING2, which the script moves on the hit); the coil has no object of its own",
	6: "the bottom upkicker the script kicks from; the coil has no object of its own",
	7: "the top kicker the script kicks from; the coil has no object of its own",
	8: "the centre of the left drop-target bank it resets; the coil sits below the bank and has no object of its own",
	9: "the centre of the right drop-target bank it resets; the coil sits below the bank and has no object of its own",
	10: "the gate the script turns, at the primitive's stored position, the point it rotates about; the coil has no object of its own",
	11: "the heart toy it moves; the coil has no object of its own",
	12: "the lower jaw of the teeth toy it moves; the coil has no object of its own",
	25: "the heart toy whose bulbs it lights; the table draws the bulbs only as a flasher sprite and the heart's texture",
	28: "the trough exit the script releases balls from; the coil has no object of its own",
	29: "the outhole kicker the script receives drained balls on; the coil has no object of its own",
}
# Flashers placed on the Lights under the table's flasher domes.
FLASHER_LIGHTS = {
	22: (["F22", "F22a"], "Lights F22 under the yellow dome domeYB and F22a under the white dome domeW"),
	23: (["F22x", "F23"], "Lights F22x under the yellow dome domeYT and F23 under the red dome domeR"),
	24: (["F24a"], "Light F24a under the blue dome domeB"),
}
# Lamps placed on another object than a Light l<n>: the teeth toy, the Bat-O-Meter bulbs and the four billboard bulbs and
# the crypt-sign bulb, each a bulb primitive the script draws the lamp on and its L<n> light sits on.
LAMP_OBJECTS = {
	2: "TopTeeth", 10: "bulb9", 11: "bulb8", 12: "bulb7", 13: "bulb6", 14: "bulb5",
	36: "bulb1", 37: "bulb2", 46: "bulb3", 47: "bulb4", 67: "bulb10",
}
BULB_LAMPS = {36: ("bulb1", 541), 37: ("bulb2", 542), 46: ("bulb3", 543), 47: ("bulb4", 544), 67: ("bulb10", 545)}
UPPERCASE_LAMP_LIGHTS = frozenset({36, 37, 46, 47, 67})
# Lamps the ROM names NOT USED but publishes in play (rises outside the self-tests: scripted game, held-closed and open
# trough probes, and the bottom-upkicker hold within the scripted game).
UNEXPLAINED_LAMPS = {24: (25, 7, 3, 18), 87: (43, 8, 3, 19)}
# Playfield G.I.: the members of the table's GI collection, which the script's TiltRelay switches with relay 31. Four of
# them show no bulb mesh: render lights, not sockets, so they are not placed.
GI_COLLECTION = tuple(["light%d" % index for index in range(1, 13)] + ["Light13", "Light14", "light15", "Light16"] + ["light%d" % index for index in range(17, 24)])
GI_RENDER_ONLY = ("light18", "light21", "light22", "light23")
GI_BULBS = tuple(name for name in GI_COLLECTION if name not in GI_RENDER_ONLY)
# The light the script draws solenoid 24 on under the left ramp: no dome covers it and it shows no bulb mesh.
UNPLACED_FLASHER_LIGHT = "F24"
# Matrix lamps placed on the image-mode Light that draws their insert.
INSERT_IMAGE = "1812 PFhole"


def lamp_light(address: int) -> str:
	return f"{'L' if address in UPPERCASE_LAMP_LIGHTS else 'l'}{address}"


# Matrix lamps the ROM names with no bulb primitive of their own: each is projected onto its insert overlay.
INSERT_LAMPS = tuple(address for address in ROM_LAMP_NAMES if address not in LAMP_OBJECTS)
INSERT_PROJECTION = (
	"Projected onto the centre of the image-mode insert overlay Light l<n> that InitLamps binds to it; the table models no "
	"bulb under the insert."
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _uri_path(path: Path) -> str:
	return quote(path.as_posix(), safe="/")


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Class of 1812 retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def _table_object_point(extraction_root: Path, kind: str, name: str) -> tuple[float, float]:
	path = extraction_root / "gameitems" / f"{kind}.{name}.json"
	if not path.is_file():
		raise RuntimeError(f"Class of 1812 retained table has no {kind} {name}: {path}")
	item = load_json(path)[kind]
	if kind == "Wall":
		points = item["drag_points"]
		return (sum(point["x"] for point in points) / len(points), sum(point["y"] for point in points) / len(points))
	if kind in ("Primitive", "HitTarget"):
		return (item["position"]["x"], item["position"]["y"])
	return (item["center"]["x"], item["center"]["y"])


def _light_item(extraction_root: Path, name: str) -> dict[str, Any]:
	path = extraction_root / "gameitems" / f"Light.{name}.json"
	if not path.is_file():
		raise RuntimeError(f"Class of 1812 retained table has no Light {name}: {path}")
	return load_json(path)["Light"]


def _obj_mesh_centres(obj_path: Path, names: set[str]) -> dict[str, tuple[float, float]]:
	bounds: dict[str, list[float]] = {}
	current = None
	with obj_path.open("r", encoding="utf-8", errors="replace") as stream:
		for line in stream:
			if line.startswith(("o ", "g ")):
				current = line[2:].strip() if line[2:].strip() in names else None
			elif current and line.startswith("v "):
				x, y = map(float, line.split()[1:3])
				box = bounds.setdefault(current, [x, x, y, y])
				box[:] = [min(box[0], x), max(box[1], x), min(box[2], y), max(box[3], y)]
	return {name: (round((box[0] + box[1]) / 2, 6), round((box[2] + box[3]) / 2, 6)) for name, box in bounds.items()}


def verify_retained_table(source_root: Path) -> None:
	"""Re-derive every placement literal from the retained table; raise on any difference."""
	table = source_root / TABLE_RELATIVE_PATH
	if not table.is_file() or table.stat().st_size != TABLE_BYTES or _file_sha256(table) != TABLE_SHA256:
		raise RuntimeError(f"Class of 1812 retained table is missing or not the pinned one: {table}")
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file() or _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Class of 1812 retained extraction manifest is missing or not the pinned one: {manifest_path}")
	extraction = source_root / EXTRACTION_RELATIVE_PATH
	manifest = load_json(manifest_path)
	if canonical_bytes(manifest) != canonical_bytes(build_extraction_manifest(extraction)):
		raise RuntimeError("Class of 1812 retained extraction does not match its manifest")
	if len(manifest["files"]) != EXTRACTION_FILE_COUNT or sum(item["size"] for item in manifest["files"]) != EXTRACTION_TOTAL_BYTES:
		raise RuntimeError("Class of 1812 retained extraction file count or byte total is not the pinned one")
	if _file_sha256(extraction / "script.vbs") != EMBEDDED_SCRIPT_SHA256:
		raise RuntimeError("Class of 1812 retained table's embedded script is not the pinned one")
	gamedata = load_json(extraction / "gamedata.json")
	if (gamedata["left"], gamedata["top"], gamedata["right"], gamedata["bottom"]) != (0.0, 0.0, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT):
		raise RuntimeError("Class of 1812 retained table bounds do not match the normalization's playfield width and height")
	for name, (kind, x, y) in TABLE_POINTS.items():
		if _table_object_point(extraction, kind, name) != (x, y):
			raise RuntimeError(f"Class of 1812 table point {name} does not match the retained {kind}")
	for name in GI_BULBS:
		if not _light_item(extraction, name)["show_bulb_mesh"]:
			raise RuntimeError(f"Class of 1812 G.I. light {name} no longer shows a bulb mesh")
	for name in GI_RENDER_ONLY + (UNPLACED_FLASHER_LIGHT,):
		item = _light_item(extraction, name)
		if item["show_bulb_mesh"] or item["is_image_mode"]:
			raise RuntimeError(f"Class of 1812 render light {name} shows a bulb mesh or is an image-mode light")
	for address in ROM_LAMP_NAMES:
		if address in LAMP_OBJECTS:
			continue
		item = _light_item(extraction, lamp_light(address))
		if not item["is_image_mode"] or item["image"] != INSERT_IMAGE or item["show_bulb_mesh"]:
			raise RuntimeError(f"Class of 1812 lamp {address}'s light is not an image-mode {INSERT_IMAGE!r} insert overlay")
	for address, (bulb, _) in BULB_LAMPS.items():
		if _light_item(extraction, lamp_light(address))["show_bulb_mesh"] or not (extraction / "gameitems" / f"Primitive.{bulb}.json").is_file():
			raise RuntimeError(f"Class of 1812 lamp {address} is not a bulb-less light on Primitive {bulb}")
	obj = source_root / OBJ_RELATIVE_PATH
	if not obj.is_file() or _file_sha256(obj) != OBJ_SHA256:
		raise RuntimeError(f"Class of 1812 retained OBJ export is missing or not the pinned one: {obj}")
	if _obj_mesh_centres(obj, set(MESH_POINTS)) != MESH_POINTS:
		raise RuntimeError("Class of 1812 mesh points do not match the retained OBJ export")


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def shown(address: int) -> str:
	"""How the service tests print an address: 00-97, then A0-A7 and B0-B7 for 100-117."""
	return f"{address:02d}" if address < 100 else ("A" if address < 110 else "B") + str(address % 10)


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


TABLE_REFS = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, SCRIPT_SOURCE)
PHOTO_REFS = {"heart": (HEART_PHOTO_SOURCE,), "TopTeeth": (TEETH_PHOTO_SOURCE,), "BottomTeeth": (TEETH_PHOTO_SOURCE,)}
# Objects whose choice rests on more than the original script: the trough probes and the 3.0.21 update put switch 44 at
# Slot2, while the original script writes it from Slot1.
PLACEMENT_REFS = {"Slot2": (RUNTIME_SOURCE, LATER_SCRIPT_SOURCE)}


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


def object_point(name: str) -> tuple[float, float]:
	if name in BANKS:
		members = [TABLE_POINTS[member] for member in BANKS[name]]
		return (round(sum(point[1] for point in members) / len(members), 6), round(sum(point[2] for point in members) / len(members), 6))
	if name in MESH_POINTS:
		return MESH_POINTS[name]
	_, x, y = TABLE_POINTS[name]
	return (x, y)


def placed_point(name: str) -> tuple[float, float]:
	"""The normalized placement: the object's point, with a rear toy clamped onto the playfield's rear edge."""
	x, y = norm(*object_point(name))
	return (x, 0.0) if name in CLAMPED_TO_REAR else (x, y)


def object_label(name: str) -> str:
	if name in BANKS:
		members = BANKS[name]
		return f"the centre of the {name}, the mean of HitTargets {', '.join(members[:-1])} and {members[-1]}"
	if name in MESH_POINTS:
		label = f"Primitive {name} (world mesh centre)"
		if name in CLAMPED_TO_REAR:
			x, y = MESH_POINTS[name]
			label += f", whose raw centre ({x}, {y}) lies behind the rear edge and is clamped to y = 0: the IPDB photo shows the toy mounted against the back panel at the rear of the playfield"
		return label
	return f"{TABLE_POINTS[name][0]} {name}"


def object_refs(*names: str) -> tuple[str, ...]:
	refs = TABLE_REFS + ((VPX_OBJ_SOURCE,) if any(name in MESH_POINTS for name in names) else ())
	for name in names:
		refs += tuple(ref for ref in PHOTO_REFS.get(name, ()) + PLACEMENT_REFS.get(name, ()) if ref not in refs)
	return refs


def located(identifier: str, role: str, names: list[str]) -> dict[str, Any]:
	placements = []
	for index, name in enumerate(names, start=1):
		x, y = placed_point(name)
		placements.append({
			"id": f"{identifier}.{role}" + (f".{index}" if len(names) > 1 else ""), "role": role, "space": "playfield",
			"x": x, "y": y, "provenance": provenance(*object_refs(name), status="observed"),
		})
	return {"status": "observed", "placements": placements}


def _excerpt(identifier: str, locator: str, filename: str, method: str, transcribed_by: str, reviewed: bool = True) -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": reviewed,
	}


def _photo_record(identifier: str, number: int, shows: str, use: str = "Used only to place the toy at the playfield's rear edge") -> dict[str, Any]:
	capture, sha256, caption, size, photographer = PHOTOS[number]
	return {
		"id": identifier, "kind": "human_review",
		"uri": f"https://web.archive.org/web/{capture}id_/https://www.ipdb.org/images/528/image-{number}.jpg",
		"revision": f"Wayback capture {capture}", "sha256": sha256, "acquired_at": "2026-11-20T08:40:00Z",
		"original_filename": f"image-{number}.jpg",
		"locator": (
			f"IPDB machine 528 photo {number}, captioned '{caption}' ({photographer}), a {size} JPEG retained as "
			f"manuals/by-machine/{MACHINE_ID}/ipdb/photos/image-{number}.jpg. {shows} {use}; no coordinate is measured "
			"from the perspective photo."
		),
		"license": "NOASSERTION", "attribution": f"{photographer} / Internet Pinball Database",
		"rights": "The photographer retains copyright; the image is kept outside the repository",
		"excerpts": [
			_excerpt(f"excerpt.class-of-1812.ipdb-photo-{number}", f"IPDB image-{number}.jpg, described", f"ipdb-photo-{number}.md", "manual", "curator, described from the retained photo"),
		],
	}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog record for clas1812, a root driver whose one clone, beav_butt (Beavis and Butt-Head, a 2023 Class of 1812 MOD), scope.py excludes as a VPX-only reskin",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/gts3games.c lines 7 (ALPHA = GTS3_dispAlpha), 11 (FLIP67 = FLIP_SWNO(6,7)), 26-29 (GTS3_dispAlpha: two "
				"20-digit CORE_SEG16 rows starting at digits 0 and 20), 40-44 (INITGAME: core_tGameData {GEN_GTS3, disptype, "
				"{flippers, 4, lamps, 0, sb, 0}} and GTS3_INPUT_PORTS_START) and 217-226 (the Class of 1812 #730 block: "
				"INITGAME(clas1812, ALPHA, FLIP67, 3/*?*/, SNDBRD_GTS3, 4), its ROM set and CORE_GAMEDEFNV(clas1812) on mGTS3S), "
				"line 235 (the beav_butt clone); src/wpc/gts3.h lines 12-24 GTS3_COMPORTS (COIN2, COIN1, COIN3, START1, Left "
				"Advance and Right Advance on bits 0x0001-0x0020, so public 0-5), lines 101 (GTS3_SOLSMOOTH 4) and 108-111 "
				"(GTS3_SWDIAG -8, GTS3_SWTILT -7, GTS3_SWSLAM -6, GTS3_SWPRIN -5) and line 199 (mGTS3S = gts3_1as); src/wpc/gts3.c "
				"line 66 xvia_0_a_r (the matrix returns read as ~core_getSwCol), lines 71-88 alpha_u4_pb_r (alpha generation 1: "
				"slam on PB3 and tilt on PB4, not inverted), line 467 (core_updateSw with solenoid 32 as the flipper enable), "
				"lines 470-491 (SWITCH_UPDATE: alpha games rewrite only bits 0x3f of internal column 1 from the cabinet port, and "
				"on alpha generation 1 the test switch drives VIA U4 CA1), lines 493-504 (gts3_sw2m/gts3_m2sw), lines 507-533 "
				"(GTS3_alpha_common_init: nGI = 0 with the note that the two G.I. relays are low-power solenoid outputs, nLamps = "
				"64 + lampCol * 8, outputs 26/31/32 typed as the 'A' relay (lightbox insert, backbox), the 'T' relay (G.I.) and "
				"'Q' (GameOn)), lines 550-553 (the clas1812 block: outputs 13-25 typed as #89 'Playfield & Backbox flashers' and "
				"lamps 10-14 as the strobed-LED 'Battometer'), lines 608-611 (MACHINE_INIT(gts3) sets alpha generation 1) and "
				"lines 1035-1044 and 1077 (aux1_r, the printer status read from GTS3_SWPRIN); src/wpc/core.h line 159 "
				"FLIP_SWNO(l,r); src/wpc/core.c line 1796 (flipSwCol 15 for GEN_GTS3), core_updateSw (the FLIP_SWNO copy and "
				"synthetic 45-48) and core_getAllSol; src/wpc/gen.h GEN_GTS3 0x0020000000000. None of these files carries "
				"the '// license:BSD-3-Clause' first line, so under the pinned checkout's LICENSE they stay under the "
				"inherited old MAME licence"
			),
			"license": "LicenseRef-PinMAME-Old-MAME", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/gts3.json", "revision": "repository",
			"locator": "Gottlieb System 3 decimal switch and lamp numbering, cabinet test inputs -8 to -5, the cabinet port, the 140-147 flipper column, solenoids 1-32 and synthetic 45-48, and the auxiliary-board lamps 120-127",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review",
			"uri": f"https://web.archive.org/web/{IPDB_PAGE_CAPTURE}id_/https://www.ipdb.org/machine.cgi?id=528",
			"revision": f"Wayback capture {IPDB_PAGE_CAPTURE}", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-11-20T08:38:00Z",
			"locator": (
				f"IPDB machine 528 'Class of 1812' (Premier Technology, trade name Gottlieb, August 1991, model 730, Gottlieb "
				f"System 3, 1,668 units, Multiball (2), toys 'Beating heart and chattering teeth'), the live page "
				f"https://www.ipdb.org/machine.cgi?id=528 fetched from the Wayback Machine capture {IPDB_PAGE_CAPTURE} and "
				f"retained as manuals/by-machine/{MACHINE_ID}/ipdb/"
				f"ipdb-528-wayback-{IPDB_PAGE_CAPTURE}.html. It lists a 3 MB English manual as 'Availability limited by copyright' "
				"without a link; the live file is a 0-byte placeholder. The title, manufacturer, model number 730 (which the ROM's "
				"power-up screen prints) and the System 3 MPU match the machine being curated."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [
				_excerpt("excerpt.class-of-1812.ipdb-page", f"IPDB machine 528 page, Wayback capture {IPDB_PAGE_CAPTURE}", "ipdb-page.md", "manual", "curator, read from the retained HTML"),
			],
		},
		{
			"id": CARDS_SOURCE, "kind": "manual",
			"uri": f"https://web.archive.org/web/{CARDS_ZIP_CAPTURE}id_/https://www.ipdb.org/files/528/{CARDS_ZIP_NAME}",
			"revision": f"Wayback capture {CARDS_ZIP_CAPTURE}", "sha256": CARDS_ZIP_SHA256, "acquired_at": "2026-11-20T08:38:00Z",
			"original_filename": CARDS_ZIP_NAME,
			"locator": (
				"Inkochnito's reproduction score and instruction cards, the IPDB file archived on "
				f"{CARDS_ZIP_CAPTURE[:4]}-{CARDS_ZIP_CAPTURE[4:6]}-{CARDS_ZIP_CAPTURE[6:8]} and retained as manuals/by-machine/"
				f"{MACHINE_ID}/ipdb/. Its Gottlieb_Class_of_1812_instruction_cards.pdf (SHA-256 {CARDS_PDF_SHA256}), pages 1-3, "
				"carries instruction cards 28290 (English, 3 and 5 balls per game) and 28291 (French), of which page 3 calls the 5-ball cards confirmed: the Bat-O-Meter, multiplier, "
				"extra ball, special, bonus, multiball lock and C.O.F.F.I.N. rules and the initials entry with the front right "
				"cabinet buttons and the credit button. A reproduction of the cards, not a service document."
			),
			"license": "NOASSERTION", "attribution": "Inkochnito (reproduction cards); Internet Pinball Database",
			"excerpts": [
				_excerpt("excerpt.class-of-1812.instruction-cards", "Gottlieb_Class_of_1812_instruction_cards.pdf pages 1-2, cards 28290 and 28291", "instruction-cards.md", "manual", "curator, the English cards read from the PDF text layer and checked against the rendered page, the French card read from the rendered page"),
			],
		},
		_photo_record(TEETH_PHOTO_SOURCE, 12, "It shows the chattering teeth on a bracket at the back panel under the backbox, with the beating heart beside them on the right."),
		_photo_record(HEART_PHOTO_SOURCE, 13, "It shows the beating heart against the back panel, resting on a bracket above the rear of the playfield."),
		_photo_record(
			RIGHT_RAMP_PHOTO_SOURCE, 11,
			"It shows the sign at the right ramp with two bulbs on top, a red one on the left over 'Add Letter To COFFIN When "
			"Lit' and a blue one on the right over 'LOCK BALL When Lit', a blue flasher dome to its upper left and a red one "
			"above the TO CRYPT sign to its right.",
			"Used only to tell which billboard bulb carries which rule and to corroborate that a blue flasher dome stands to "
			"the sign's upper left, where the table puts solenoid 24's domeB, whose coordinate comes from the table",
		),
		_photo_record(
			BAT_O_METER_PHOTO_SOURCE, 19,
			"It shows the populated playfield from the front, and at the upper left, in front of the teeth, a "
			"blue-bordered sign with five yellow rows reading, top to bottom, Special, Extra Ball, 20000, 10000 and 5000, "
			"each with two dark round marks near its left end, unlit in the photo.",
			"Used only to describe the Bat-O-Meter's form and the order of its values",
		),
		_photo_record(
			TWO_SLOT_DOOR_PHOTO_SOURCE, 5,
			"It shows a cabinet front whose coin door has two coin slots with a reject button each and two coin returns, "
			"the start game button to its left and the two top five enter initials buttons to its right.",
			"Used only to show that coin doors differ in their number of chutes",
		),
		_photo_record(
			ONE_SLOT_DOOR_PHOTO_SOURCE, 24,
			"It shows a cabinet front whose coin door has a single coin slot marked 10 Fr, 5 Fr and 1 Fr with one push-to-reject "
			"button and one coin return, the start game button to its left and the two top five enter initials buttons to "
			"its right.",
			"Used only to show that coin doors differ in their number of chutes",
		),
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH),
			"locator": (
				"Pinned LibPinMAME runs of clas1812, each from a new state directory holding only the factory-settings NVRAM: "
				"the Lamp Matrix, Relay & Solenoid and Switch Matrix self-tests, each step paired with the public address it "
				"drove or the host held and with the text the two alphanumeric displays showed, plus the Front Door Test, one "
				"scripted game, and two trough probes that tilt a game with switch 44 held closed (tilt-trough-closed) and drain "
				"a ball with 44 opened after the release (tilt-trough-open). Raw runs, display frames, NVRAM and the manifest "
				"are retained outside the repository."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		},
		{
			"id": SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"{TABLE_SCRIPTS_REPOSITORY}/blob/{TABLE_SCRIPTS_REVISION}/{quote(SCRIPT_PATH, safe='/')}",
			"revision": TABLE_SCRIPTS_REVISION, "original_filename": SCRIPT_PATH, "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"tom tower & ninuzzu's VPX recreation of Class of 1812 (NZ&TT 1.0) as patched by Thalamus on 2018-07-23 (lines "
				"43-46), 35,513 bytes in the pinned known-working corpus. Runtime authority: cGameName = \"clas1812\" (line 66), "
				"LoadVPM Class1812.VBS (line 68), UseSolenoids = 2 (line 73), the trough, saucer and drop-bank objects (lines "
				"112-147 and 226-274), the key handlers (lines 155-170), the solenoid callbacks (lines 180-219 and 259-368), the "
				"switch writers (lines 375-468), the G.I. relays (lines 474-500), the lamp drawing (lines 509-568) and the ramp sounds (lines 769-788). The "
				"retained table embeds the 2017 script before that patch: it differs only by Thalamus's UseSolenoids = 2 and "
				"single-flipper constants and the flipper-key writes to 4 and 5 (lines 160-161 and 167-168), so it binds every "
				"playfield address to the same object."
			),
			"license": "NOASSERTION", "attribution": "tom tower & ninuzzu; patched by Thalamus; pinned copy in sverrewl/vpxtable_scripts", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.class-of-1812.nztt-script-bindings", "Class of 1812  - NZ&TT 1.0.vbs lines 36-568 and 769-788, controller bindings and ramp sounds", "nztt-script-bindings.md", "manual", "curator, read from the pinned script"),
			],
		},
		{
			"id": LATER_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"{TABLE_SCRIPTS_REPOSITORY}/blob/{TABLE_SCRIPTS_REVISION}/{quote(LATER_SCRIPT_PATH, safe='/')}",
			"revision": TABLE_SCRIPTS_REVISION, "original_filename": "Class of 1812 (Gottlieb 1991) v3.0.21.vbs", "sha256": LATER_SCRIPT_SHA256,
			"locator": (
				"UnclePaulie's version 3.0.21 of the same table (lines 12-20: updated from the original by Tom Tower & Ninuzzu, "
				"with Tomate's baking), 190,387 bytes in the same pinned corpus. Same lineage, so it corroborates and never "
				"independently confirms. Cited for its solenoid map (lines 706-741): BGGI, the backglass G.I., on 26 and PFGI, the "
				"playfield G.I., on 31; the ramp-dome pairs on 22-24; and 13-21 driven only in its 'Backglass Solenoid Controlled "
				"Flashers' section (lines 728-741), whose comment notes that the manual numbers the drivers from zero (line 732)."
			),
			"license": "NOASSERTION", "attribution": "UnclePaulie and Tomate, after tom tower & ninuzzu; pinned copy in sverrewl/vpxtable_scripts", "rights": "NOASSERTION",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(TABLE_RELATIVE_PATH)}",
			"original_filename": TABLE_FILENAME, "sha256": TABLE_SHA256, "acquired_at": "2026-11-20T08:35:00Z",
			"locator": (
				f"Retained NZ&TT 1.0 table by tom tower & ninuzzu ({TABLE_BYTES:,} bytes), copied on 2026-11-20 from the "
				"contributor's table collection, where the file is dated 2017-09-28. Its embedded script "
				f"(SHA-256 {EMBEDDED_SCRIPT_SHA256}) is the known-working script before Thalamus's 2018 patch, so it binds every "
				f"playfield address to the same objects; line numbers differ. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/952 and y/1974. Geometry authority for script-bound table objects."
			),
			"license": "NOASSERTION", "attribution": "tom tower & ninuzzu", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt(
					"excerpt.class-of-1812.vpx-table-objects", "gameitems/*.json and the OBJ export, placed objects and their bindings",
					"vpx-table-objects.md", "mixed", "curator, generated from the retained extraction and checked against the script's bindings",
				),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(EXTRACTION_MANIFEST_RELATIVE_PATH)}",
			"sha256": EXTRACTION_MANIFEST_SHA256, "acquired_at": "2026-11-20T08:47:00Z",
			"locator": (
				f"Retained {VPXTOOL_VERSION} extraction of the table, {EXTRACTION_FILE_COUNT} files and "
				f"{EXTRACTION_TOTAL_BYTES:,} bytes, with a full sorted path/size/SHA-256 manifest whose own SHA-256 is this "
				f"record's sha256. Bounds are {TABLE_BOUNDS}. A Wall is placed at the mean of its drag points, a HitTarget or "
				"Primitive at its stored position, every other object at its stored centre."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_OBJ_SOURCE, "kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/{_uri_path(OBJ_RELATIVE_PATH)}",
			"sha256": OBJ_SHA256, "acquired_at": "2026-11-20T08:38:00Z",
			"locator": (
				f"{VPXTOOL_VERSION} `export obj --units vpu` of the table, the world-space mesh of every object (OBJ x is "
				"playfield x, OBJ y is playfield y). Used only for primitives whose stored position is not the part's centre: "
				"the slingshot kicker arms SLING1 and SLING2, the heart, the teeth TopTeeth and BottomTeeth, the Bat-O-Meter "
				"bulbs bulb5-bulb9, the billboard bulbs bulb1-bulb4 and the bulb bulb10, each placed at its world bounding-box "
				"centre. Control: the same export's pop bumper body "
				"BBody1 centres at (431.34122, 426.205935), within 0.0001 units of Bumper sw10's centre (431.34116, 426.20593)."
			),
			"license": "NOASSERTION", "attribution": "vpxtool export of the retained table",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "Class1812.vbs", "sha256": VPM_LIBRARY_SHA256,
			"locator": (
				"The VPinMAME script library the known-working script loads (LoadVPM \"02800000\", \"Class1812.VBS\", 3.50), "
				f"retained with core.vbs (SHA-256 {VPM_CORE_SHA256}). Class1812.vbs defines GameOnSolenoid = 32, swCoin1-3 = "
				"00-02, swStartButton = 03, swLeftAdvance = 04, swRightAdvance = 05, swLRFlip = 141 and swLLFlip = 143 and the "
				"test, tilt and slam inputs -8, -7 and -6, and writes them from the keys in vpmKeyDown/vpmKeyUp; core.vbs defines "
				"sLRFlipper = 46 and sLLFlipper = 48 and the vpmNudge TiltSwitch pulse."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.class-of-1812.vpm-script-library", "Class1812.vbs lines 18-110 and core.vbs lines 1120-1130 and 2862-2863", "vpm-script-library.md", "manual", "curator, read from the library files"),
			],
		},
	]


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
		"aliases": [{"namespace": "pinmame.switch" if group == "pinmame.input.switch" else ("pinmame.lamp" if group == "pinmame.output.lamp" else "pinmame.coil"), "value": str(address)}],
	}
	device.update(extra)
	return device


READ_PATH_NOTE = (
	" Class of 1812's game data sets no inverted-switch mask and gts3.c's xvia_0_a_r hands the CPU the complement of the "
	"matrix column, so public 1 is the closed contact the CPU sees, and the Switch Matrix Test reads ALL SWITCHES OPEN "
	"with every address at 0: the matrix contact rests open and closes when the device is actuated."
)
MATRIX_TEST_NOTE = (
	" In the Switch Matrix Test, holding public {address} at 1 alone displayed the ROM's name \"{name}\" with ={shown} "
	"(run switch-matrix)."
)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	cabinet = {
		-8: ("Test (Diagnostic) Button", "service.test", "button", (
			"GTS3_SWDIAG on the cabinet port (internal column 0). On alpha generation 1, which MACHINE_INIT(gts3) sets for "
			"this driver, SWITCH_UPDATE drives VIA U4 CA1 with it. Every retained self-test run steps through the tests with "
			"it: the first press at 1 shows the self-test 1 prompt (bookkeeping and game adjustments) and each further press "
			"steps to the next self-test, up to 9, the Front Door Test (runs nvram-init, lamp-matrix, solenoids, switch-matrix, "
			"front-door). Class1812.vbs names it swDiagnostic = -8."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE)),
		-7: ("Tilt", "cabinet.tilt", "tilt", (
			"GTS3_SWTILT on the cabinet port, read through alpha_u4_pb_r on VIA U4 PB4 without inversion. Held at 1 inside the "
			"Switch Matrix Test it replaced the switch line with TILT (run switch-matrix), so the ROM reads it active at 1. "
			"Class1812.vbs names it swTilt = -7. The known-working script sets vpmNudge.TiltSwitch = 151 (line 112), which is "
			"not this address or any address System 3 publishes, so its nudge tilt pulses nothing the ROM reads: a defect in "
			"that table."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE, SCRIPT_SOURCE)),
		-6: ("Slam Tilt", "cabinet.slam-tilt", "tilt", (
			"GTS3_SWSLAM on the cabinet port, read on alpha generation 1 through alpha_u4_pb_r on VIA U4 PB3 without "
			"inversion. A pulse at 1 inside the Front Door Test ended the test and left the displays showing the score "
			"screen (run front-door), so the ROM reads it active at 1. Class1812.vbs names it swSlamTilt = -6."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE)),
	}
	for address, (label, role, switch_type, notes, refs) in cabinet.items():
		items.append(_device(
			f"switch.cabinet-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used", core + refs,
			roles=[role], normally_closed=False,
			physical={"location": "coin door and cabinet", "switch_type": switch_type, "notes": notes},
			spatial=not_applicable("cabinet_or_service", *core),
		))
	items.append(_device(
		"switch.cabinet-5", "Communications Adapter Present", "virtual", "pinmame.input.switch", -5, "optional", core + (RUNTIME_SOURCE,),
		physical={
			"location": "CPU board auxiliary connector (optional communications adapter)",
			"notes": (
				"GTS3_SWPRIN, which PinMAME reads back into the printer status that aux1_r returns for the optional "
				"communications adapter (printer) on the CPU board's auxiliary connector: at 1 the status reads ready, at 0 not "
				"connected. It is not a matrix switch, and held at 1 inside the Switch Matrix Test it put no line of its own on "
				"the display, which still showed the previous step's RIGHT FLIPPER =07 (run switch-matrix). A recreation without "
				"the adapter leaves it at 0."
			),
		},
		spatial=not_applicable("virtual", *core),
	))
	for address in MATRIX_ADDRESSES:
		identifier = f"switch.matrix-{address}"
		column, row = divmod(address, 10)
		if address in UNUSED_SWITCHES:
			items.append(_device(
				identifier, f"Not Used (Matrix Position {address})", "switch", "pinmame.input.switch", address, "unused",
				core + (RUNTIME_SOURCE,),
				physical={"notes": (
					f"Strobe {column}, return {row}." + MATRIX_TEST_NOTE.format(address=address, shown=shown(address), name="NOT USED")
					+ " The ROM scans the position and calls it unused; the known-working script never writes it."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		label = SWITCH_LABELS[address]
		notes = f"Strobe {column}, return {row}."
		if address in ROM_SWITCH_NAMES:
			if address in FLIP_SWNO:
				notes += (
					f" In the Switch Matrix Test, holding the flipper button {143 if address == 6 else 141} at 1 displayed the "
					f"ROM's name \"{ROM_SWITCH_NAMES[address]}\" with ={address:02d} (run switch-matrix)."
				)
			else:
				notes += MATRIX_TEST_NOTE.format(address=address, shown=shown(address), name=ROM_SWITCH_NAMES[address])
		refs: tuple[str, ...] = core + (RUNTIME_SOURCE,)
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in ROM_RUNTIME:
			notes += f" In play, {ROM_RUNTIME[address]}."
		if address in SCRIPT_WRITERS:
			notes += f" The known-working script treats it as actuated at 1: {SCRIPT_WRITERS[address]}."
			refs += (SCRIPT_SOURCE,)
		notes += READ_PATH_NOTE
		if address in CABINET_SWITCH_TYPES:
			physical["switch_type"] = CABINET_SWITCH_TYPES[address]
		if address == 3:
			notes += (
				" Held at 1 alone in the Switch Matrix Test it put no name of its own on the display, whose frame showed the "
				"start of ALL SWITCHES OPEN (run switch-matrix): in the self-tests the credit button is a control of its own, "
				"which fires the displayed driver in the Relay+Solenoid Test (run solenoids) and answers the factory-settings "
				"prompts (run nvram-init). GTS3_COMPORTS calls it START1, Class1812.vbs writes it from the start key "
				"(swStartButton = 03), and the instruction cards enter each initial with the credit button."
			)
			refs += (VPM_LIBRARY_SOURCE, CARDS_SOURCE)
		if address in (4, 5):
			side = "left" if address == 4 else "right"
			notes += (
				f" The {side} of the two white buttons on the front of the cabinet, right of the coin door: the instruction "
				"cards select each initial 'using front right cabinet buttons' (French card: 'les 2 boutons a droite de la porte "
				f"avant'). GTS3_COMPORTS calls it {'Left' if address == 4 else 'Right'} Advance. "
				+ ("At the self-test 1 prompt PUSH L, WHITE BUTTON / FOR GAME ADJUSTMENTS a press at 1 entered the adjustments "
				"(run nvram-init)" if address == 4 else "In the Lamp Matrix and Relay+Solenoid Tests each press at 1 stepped "
				"to the next lamp or driver, and in the adjustments to the next item (runs lamp-matrix, solenoids, nvram-init); "
				"the Display and Sound Tests prompt PUSH R, WHITE BUTTON (run front-door)")
				+ f". Class1812.vbs names it sw{'Left' if address == 4 else 'Right'}Advance = 0{address} and writes it from "
				f"VPinMAME's key{'Down' if address == 4 else 'Up'} key; the known-working script also writes it from the "
				f"{side} flipper key (lines {160 if address == 4 else 161} and {167 if address == 4 else 168}), a table "
				"convenience for entering initials: on the machine the flipper buttons do not close it."
			)
			refs += (VPM_LIBRARY_SOURCE, CARDS_SOURCE, SCRIPT_SOURCE)
		if address in (0, 1, 2):
			notes += (
				f" Class1812.vbs names it swCoin{address + 1} = 0{address} and its help text the "
				f"{('left', 'right', 'center')[address]} coin chute; GTS3_COMPORTS rewrites it from a coin key only with "
				"PinMAME keyboard handling on. The Front Door Test counts all three chutes, but doors differ: IPDB photo 5 "
				"shows a door with two coin slots and photo 24 a French door with one, and no source says which of the three "
				"inputs a given door wires, so how many chutes a machine has depends on its door."
			)
			refs += (VPM_LIBRARY_SOURCE, TWO_SLOT_DOOR_PHOTO_SOURCE, ONE_SLOT_DOOR_PHOTO_SOURCE)
		if address in FLIP_SWNO:
			button = 143 if address == 6 else 141
			notes += (
				f" The driver declares FLIP_SWNO(6,7) with no FLIP_SOL, so core_updateSw copies the {'left' if address == 6 else 'right'} "
				f"flipper button from PinMAME's flipper column (public {button}) into this switch on every update; it cannot be "
				f"driven directly, because a host write here is overwritten on the next update. Drive {button}. The alpha "
				"SWITCH_UPDATE keeps bits 6 and 7 of the cabinet column when it rewrites the cabinet port. Class1812.vbs comments "
				f"swLRFlip = 141 as '06 and swLLFlip = 143 as '07 (lines 31-32), the reverse of FLIP_SWNO(6,7) and of the ROM's "
				"own names: a comment defect with no effect, since the library writes 141 and 143."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		if address in (13, 14):
			notes += (
				" The ROM calls it a kicking rubber, Gottlieb's name for a slingshot, and fires its own coil from it; the "
				f"known-working script models it as the {'left' if address == 13 else 'right'} slingshot wall sw{address}."
			)
		if address in (52, 53):
			notes += f" The ROM's coil {6 if address == 52 else 7} kicks the ball out (run gameplay, above)."
		if address == 53:
			notes += " TOP KICKER RO (55) is a rollover beside it."
		if address in (44, 54):
			notes += (
				" The machine holds two balls (IPDB: Multiball (2); the script's InitTrough creates two, lines 226-230); the "
				"driver's INITGAME passes 3 with PinMAME's own '/*?*/' doubt."
			)
		if address in (50, 51):
			notes += (
				" The known-working script files both ramp switches under the comment 'Optos' (line 466); the ROM's name and "
				"no manual here state the construction, so no switch type is recorded."
			)
		if address == 44:
			refs += (LATER_SCRIPT_SOURCE,)
		if address in SWITCH_OBJECTS:
			name = SWITCH_OBJECTS[address]
			if address in SWITCH_OBJECT_NOTES:
				notes += f" Placed at the retained table's {SWITCH_OBJECT_NOTES[address]}."
			else:
				notes += f" Placed at the retained table's {object_label(name)}, which the script binds to this address."
			extra["spatial"] = located(identifier, "sensor", [name])
			refs += tuple(ref for ref in object_refs(name) if ref not in refs)
		physical["notes"] = notes
		if address in CABINET_SWITCH_ROLES:
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			if address in (0, 1, 2):
				physical["location"] = "coin door"
			elif address == 3:
				physical["location"] = "cabinet front (credit button)"
			elif address in (4, 5):
				physical["location"] = "cabinet front, right of the coin door"
			else:
				physical["location"] = "matrix copy of the cabinet flipper button"
			extra["spatial"] = not_applicable("cabinet_or_service", *core)
		extra["normally_closed"] = False
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, physical=physical, **extra))
	items += flipper_column_inputs()
	return items


FLIPPER_COLUMN = (
	(140, "CORE_SWLRFLIPEOSBIT", 0x01, "Lower Right", "right", "eos"),
	(141, "CORE_SWLRFLIPBUTBIT", 0x02, "Lower Right", "right", "button"),
	(142, "CORE_SWLLFLIPEOSBIT", 0x04, "Lower Left", "left", "eos"),
	(143, "CORE_SWLLFLIPBUTBIT", 0x08, "Lower Left", "left", "button"),
	(144, "CORE_SWURFLIPEOSBIT", 0x10, "Upper Right", "right", "eos"),
	(145, "CORE_SWURFLIPBUTBIT", 0x20, "Upper Right", "right", "button"),
	(146, "CORE_SWULFLIPEOSBIT", 0x40, "Upper Left", "left", "eos"),
	(147, "CORE_SWULFLIPBUTBIT", 0x80, "Upper Left", "left", "button"),
)


def flipper_column_inputs() -> list[dict[str, Any]]:
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	matrix = {"left": FLIP_SWNO[0], "right": FLIP_SWNO[1]}
	items: list[dict[str, Any]] = []
	for address, constant, bit, position, side, kind in FLIPPER_COLUMN:
		base = (
			f"PinMAME flipper switch column (internal column 15, which core_updateSw uses for GEN_GTS3), bit {constant} = "
			f"0x{bit:02X}, published at {address} through gts3_m2sw(15, row) = 140 + row."
		)
		if address in (141, 143):
			notes = (
				f"{base} This is the {side} cabinet flipper button as the ROM receives it. The driver declares FLIP_SWNO(6,7) "
				"with no FLIP_SOL, so with keyboard handling off (the LibPinMAME default) core_updateSw reads this bit as the host "
				f"wrote it, copies it into matrix switch {matrix[side]} on every update and fabricates the synthetic "
				f"{'45/46' if side == 'right' else '47/48'} flipper outputs from it while the Q relay (32) is energized. Drive "
				f"this address, not {matrix[side]}. Held at 1 in the Switch Matrix Test it displayed "
				f"{'RIGHT' if side == 'right' else 'LEFT'} FLIPPER ={matrix[side]:02d} (run switch-matrix), and pressed during "
				f"the scripted game it raised {'45 and 46' if side == 'right' else '47 and 48'} (run gameplay). Class1812.vbs "
				f"names it swL{'R' if side == 'right' else 'L'}Flip = {address} and writes it from the flipper key in "
				"vpmKeyDown/vpmKeyUp, which the known-working script calls."
			)
			items.append({
				"id": f"switch.flipper-column-{address}",
				"label": f"{position} Flipper Button (PinMAME Flipper Column)",
				"kind": "switch",
				"binding": {"group": "pinmame.input.switch", "device": address},
				"availability": "used",
				"provenance": provenance(*core, RUNTIME_SOURCE, VPM_LIBRARY_SOURCE),
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"roles": [f"flipper.lower.{side}.button"],
				"normally_closed": False,
				"physical": {"location": "cabinet flipper button", "switch_type": "button", "notes": notes},
				"spatial": not_applicable("cabinet_or_service", *core),
			})
			continue
		if kind == "eos":
			reason = (
				"locals.flipMask carries this end-of-stroke bit only when hw.flippers sets FLIP_EOS, and FLIP_SWNO(6,7) does "
				"not, so core_updateSw neither synthesizes it nor copies it anywhere: PinMAME models no end-of-stroke switch on "
				"this machine."
			)
		else:
			reason = (
				"core_updateSw copies only the two lower button bits into the matrix and the synthetic outputs; this upper-button "
				"bit would join locals.flipMask only if hw.flippers set the matching upper FLIP_SW bit, which FLIP_SWNO(6,7) does "
				"not. The machine has two flippers."
			)
		reason += (
			" A host write survives in the column, but the ROM cannot read it there: xvia_0_a_r reads the matrix only through "
			"core_getSwCol with the twelve-bit lamp/switch strobe, which reaches internal columns 1-12."
		)
		items.append({
			"id": f"switch.flipper-column-{address}",
			"label": f"Unused Flipper Column {position} {'End-of-Stroke' if kind == 'eos' else 'Button'} ({address})",
			"kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": address},
			"availability": "unused",
			"provenance": provenance(*core),
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {"location": "internal public address space", "switch_type": "other", "notes": f"{base} {reason}"},
			"spatial": not_applicable("unused", *core),
		})
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in range(1, 33):
		driver = address - 1
		name = ROM_COIL_NAMES[address]
		quoted = name if '"' in name else f'"{name}"'
		notes = (
			f"The Relay+Solenoid Test names driver {driver} {quoted}, and the credit button fired public {address} there "
			"(run solenoids; the displayed driver number is the public address minus one)."
		)
		refs = core + (RUNTIME_SOURCE,)
		if address in SOLENOID_RUNTIME:
			notes += f" In play it {SOLENOID_RUNTIME[address]}."
		if address in SOLENOID_CALLBACKS:
			notes += f" The known-working script binds SolCallback({address}) to {SOLENOID_CALLBACKS[address]}."
			refs += (SCRIPT_SOURCE,)
		if address in (1, 2, 3, 4, 5):
			notes += (
				" The CPU fires it from its switch: the ROM, not a separate special-solenoid circuit, closes the loop, so a "
				"consumer only drives the switch. The known-working script comments its callback out (lines 182-186) and kicks "
				"the ball with the table's own bumper and slingshot physics."
			)
			refs += (SCRIPT_SOURCE,)
		if address in FLASHER_SOLENOIDS:
			count = re.search(r"\((\d)\)", name)
			notes += (
				" The ROM's name carries 67, the #67 flasher bulb"
				+ (f", and ({count.group(1)}), the number of bulbs it drives" if count else ", and no bulb count")
				+ "; PinMAME's clas1812 block (gts3.c lines 550-553) models it as a #89 bulb among its 'Playfield & Backbox "
				"flashers'."
			)
		if address in BACKBOX_SCRIPT_FLASHERS:
			notes += (
				" That the load is fitted rests on the ROM's own Relay+Solenoid Test, the game's driver table, which names it "
				"with its bulb type and count. The known-working script leaves SolCallback("
				f"{address}) commented out under its note '(**) Used in backbox (translite)' (lines 180 and {182 + address}), and "
				"its later 3.0.21 version drives it only in its backglass section (lines 728-741). Both scripts agree, but they "
				"are one lineage and no manual confirms the location, so the output is not placed."
			)
			refs += (SCRIPT_SOURCE, LATER_SCRIPT_SOURCE)
		if address == 22:
			notes += (
				" The script draws it on two domes, the yellow domeYB and the white domeW, and the 3.0.21 version's comment "
				"reads 'Flasher:Ramps #1 (2) White dome and yellow dome bottom' (line 713), so the placements are the Lights F22 "
				"and F22a under the two domes, without a quantity."
			)
			refs += (LATER_SCRIPT_SOURCE,)
		if address == 23:
			notes += (
				" The script draws it on two domes, the yellow domeYT and the red domeR, and the 3.0.21 version's comment reads "
				"'Flasher:Ramps #2 (2) Red dome and yellow dome top' (line 714), so the placements are the Lights F22x and F23 "
				"under the two domes, without a quantity."
			)
			refs += (LATER_SCRIPT_SOURCE,)
		if address == 24:
			notes += (
				" The script draws it on one dome, the blue domeB, and on a light under the ramp, and the 3.0.21 version's "
				"comment reads 'Flasher:Ramps #3 (2) Blue dome and under ramp' (line 715). The placement is the Light F24a under "
				"the dome. The light under the ramp is the render light F24 on the table's RuinsFlash surface, which no dome "
				"covers and which shows no bulb mesh: a table effect, so whether a second bulb is fitted under the ramp is "
				"unknown, and it is not placed; no quantity is recorded. IPDB photo 11 shows a blue flasher dome to the upper left "
				"of the sign at the right ramp, where the table puts domeB."
			)
			refs += (LATER_SCRIPT_SOURCE, RIGHT_RAMP_PHOTO_SOURCE)
		if address == 10:
			notes += (
				" The ROM calls it a gate; the known-working script models it as a diverter flap near the top kicker, at "
				"Primitive DiverterP, without saying where it sends the ball."
			)
		if address in (11, 12, 25):
			notes += (
				" IPDB lists the toys as a beating heart and chattering teeth, and its photos 12 and 13 show both mounted against "
				"the back panel at the rear of the playfield, the teeth left of the heart."
			)
			refs += (IDENTITY_SOURCE,)
		if address == 26:
			notes += (
				" PinMAME's System 3 init types it as the 'A' relay: lightbox insert (backbox) illumination. The known-working "
				"script's GIRelay switches the playfield G.I. from it instead, a stand-in its own comment calls the lightbox "
				"relay; the 3.0.21 version drives the backglass G.I. from it (BGGI, line 718)."
			)
			refs += (LATER_SCRIPT_SOURCE,)
		if address == 27:
			notes += (
				" An optional cabinet accessory output: the known-working script assigns it an empty callback and no gameplay "
				"run published it."
			)
		if address == 30:
			notes += (
				" The ROM's Relay+Solenoid Test names the driver KNOCKER but, unlike its flasher entries, gives no part, bulb "
				"or count, and the known-working script only plays a sound from it. No retained source shows a knocker fitted, "
				"so its fitment stays unknown."
			)
		if address == 31:
			notes += (
				" PinMAME's System 3 init types it as the 'T' relay, general illumination, and the 3.0.21 script drives the "
				f"playfield G.I. from it (PFGI, line 722). The placements are the {len(GI_BULBS)} of the {len(GI_COLLECTION)} "
				"members of the retained table's GI collection, which the script's TiltRelay switches with this relay, that show "
				f"a bulb mesh; {', '.join(GI_RENDER_ONLY[:-1])} and {GI_RENDER_ONLY[-1]} show none and are render lights, so they "
				"are not placed. Without a manual no G.I. bulb count or layout is known, and a table's "
				"grouping is not the machine's wiring, so the placements stay observed without a quantity."
			)
			refs += (LATER_SCRIPT_SOURCE, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE)
		if address == 32:
			notes += (
				" PinMAME's System 3 init types it as the 'Q' relay, game on, and passes its state to core_updateSw as the "
				"flipper enable: the synthetic flipper outputs 45-48 follow the buttons only while it is on. Class1812.vbs names "
				"it GameOnSolenoid = 32."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		kind = "flasher" if address in FLASHER_SOLENOIDS else SOLENOID_KIND.get(address, "coil")
		availability = "optional" if address == 27 else ("unknown" if address == 30 else "used")
		identifier = f"device.{slug(SOLENOID_LABELS[address])}"
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in CABINET_SOLENOIDS:
			physical["location"] = CABINET_SOLENOIDS[address]
			extra["spatial"] = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
		elif address in FLASHER_LIGHTS:
			names, description = FLASHER_LIGHTS[address]
			notes += f" Placed at the retained table's {description}."
			extra["spatial"] = located(identifier, "emitter", names)
			refs += tuple(ref for ref in object_refs(*names) if ref not in refs)
		elif address in SOLENOID_OBJECTS:
			obj = SOLENOID_OBJECTS[address]
			if address in SOLENOID_PROJECTED:
				notes += f" Projected onto {SOLENOID_PROJECTED[address]} ({object_label(obj)})."
			else:
				notes += f" Placed at the retained table's {object_label(obj)}."
			extra["spatial"] = located(identifier, "emitter" if kind == "flasher" else "effect", [obj])
			refs += tuple(ref for ref in object_refs(*(BANKS.get(obj) or (obj,))) if ref not in refs)
		elif address == 31:
			physical["location"] = "relay in the cabinet or backbox; the placements are the playfield G.I. it switches"
			extra["spatial"] = located(identifier, "emitter", list(GI_BULBS))
		physical["notes"] = notes
		items.append(_device(
			identifier, SOLENOID_LABELS[address], kind, "pinmame.output.solenoid", address,
			availability, refs, physical=physical, **extra,
		))
	synthetic = {
		45: ("Synthetic Lower Right Flipper Power", 141), 46: ("Synthetic Lower Right Flipper Hold", 141),
		47: ("Synthetic Lower Left Flipper Power", 143), 48: ("Synthetic Lower Left Flipper Hold", 143),
	}
	for address, (label, button) in synthetic.items():
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, "used", core + (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE, SCRIPT_SOURCE),
			roles=["internal.synthetic-flipper"],
			physical={"notes": (
				f"PinMAME fabricates it from the flipper button at public {button} (core_updateSw, CORE_FIRSTLFLIPSOL = 45) while "
				"the Q relay 32 is energized, and core_getAllSol publishes the power and hold outputs of a pair together. Class "
				"of 1812's flippers are cabinet-wired (FLIP_SWNO(6,7), no FLIP_SOL), so no CPU driver stands behind it. Pressing "
				f"{button} during the scripted game raised the pair (run gameplay). core.vbs names the hold output "
				f"s{'LR' if button == 141 else 'LL'}Flipper = {46 if button == 141 else 48}, and the known-working script fires "
				f"its {'right' if button == 141 else 'left'} flipper from it (lines 218-219 and 288-306)."
			)},
			spatial=not_applicable("virtual", *core),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in LAMP_ADDRESSES:
		column, row = divmod(address, 10)
		identifier = f"lamp.matrix-{address}"
		if address in UNEXPLAINED_LAMPS:
			gameplay, closed, opened, upkicker = UNEXPLAINED_LAMPS[address]
			items.append(_device(
				identifier, f"Not Used (Lamp {address})", "lamp", "pinmame.output.lamp", address, "unknown", core + (RUNTIME_SOURCE, SCRIPT_SOURCE),
				physical={"notes": (
					f"Strobe {column}, row {row}. The Lamp Matrix Test steps through ={shown(address)} and names it NOT USED, and "
					"the retained table has no light for it. The ROM still drives it in play: it rose "
					f"{gameplay} times in the scripted game ({upkicker} of them while the bottom upkicker's switch was held), "
					f"{closed} times in the tilt-trough-closed run and {opened} in the tilt-trough-open run. No wiring source "
					"says whether a bulb is fitted there or what the state means, so its fitment stays unknown and it is not "
					"placed."
				)},
			))
			continue
		if address not in ROM_LAMP_NAMES:
			items.append(_device(
				identifier, f"Not Used (Lamp {address})", "lamp", "pinmame.output.lamp", address, "unused", core + (RUNTIME_SOURCE, SCRIPT_SOURCE),
				physical={"notes": (
					f"Strobe {column}, row {row}. The Lamp Matrix Test steps through ={shown(address)} and names it NOT USED; "
					"the retained table has no light for it. It rose only inside the self-test runs, never in the scripted game "
					"or the two tilt-trough runs, so in the retained runs the ROM published no state there outside its own tests."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		name = ROM_LAMP_NAMES[address]
		notes = (
			f"Strobe {column}, row {row}. In the Lamp Matrix Test ={shown(address)} blinks this public address while the "
			f"display names it {name} (run lamp-matrix)."
		)
		refs = core + (RUNTIME_SOURCE, SCRIPT_SOURCE)
		physical: dict[str, Any] = {}
		if address in LED_LAMPS:
			notes += (
				" PinMAME's clas1812 block types it as a strobed LED of the 'Battometer' (CORE_MODOUT_LED_STROBE_1_10MS, gts3.c "
				"line 552). The instruction cards advance the Bat-O-Meter from the white targets and collect its flashing value "
				"at the spinner. IPDB photo 19 shows the Bat-O-Meter as a separate sign at the upper left, in front of the "
				"teeth, with five rows reading, top to bottom, Special, Extra Ball, 20000, 10000 and 5000, each with two dark "
				"round marks near its left end. The known-working script draws it on a bulb primitive and a flasher sprite of "
				f"a vertical stack at the left rear (AddLamp {address}, bulb{19 - address} and Li{address}, lines "
				f"{519 + address} and {525 + address})."
			)
			refs += (CARDS_SOURCE, BAT_O_METER_PHOTO_SOURCE)
		if address in range(40, 46):
			notes += (
				" One of the six letters of C.O.F.F.I.N., which the instruction cards add one at a time from the lit ramp; the "
				"ROM names it by its letter alone, and the two F lamps in order."
			)
			refs += (CARDS_SOURCE,)
		if address == 2:
			notes += (
				" The light of the chattering-teeth toy: the known-working script swaps the textures of both teeth primitives "
				"and draws the flasher sprite Li2 from it (lines 526-528)."
			)
			refs += (IDENTITY_SOURCE,)
		obj = LAMP_OBJECTS.get(address, lamp_light(address))
		if address in BULB_LAMPS:
			bulb, line = BULB_LAMPS[address]
			notes += (
				f" The known-working script's InitLamps binds Light L{address} to it (Lights({address}), line 512) and draws "
				f"the bulb primitive {bulb} on it (AddLamp {address}, line {line}); the light sits on that bulb. Placed at the "
				f"retained table's {object_label(obj)}, the bulb itself."
			)
		elif address in LAMP_OBJECTS:
			notes += f" Placed at the retained table's {object_label(obj)}."
		else:
			notes += (
				f" The known-working script's InitLamps binds Light {obj} to it (Lights({address}), line 512), an image-mode "
				"overlay of the insert drawn with the table's '1812 PFhole' image. Placed at that light's centre, the insert "
				"the lamp lights, as a projection: the table models no bulb under the insert, so the point is the insert's "
				"centre, not a measured socket."
			)
		if address in (46, 47):
			notes += (
				" IPDB photo 11 shows the sign at the right ramp with two bulbs on top: a red one on the left over 'Add Letter "
				"To COFFIN When Lit' and a blue one on the right over 'LOCK BALL When Lit', which match the ROM's R BB ADD "
				"LETTER and R BB LOCK."
			)
			refs += (RIGHT_RAMP_PHOTO_SOURCE,)
		if address == 47:
			notes += (
				" The script's comment on that line, 'Right Ramp Million (Right)', is an annotation defect of the table: the "
				"ROM and the photo both name the lock."
			)
		extra = {"spatial": located(identifier, "emitter", [obj])}
		refs += tuple(ref for ref in object_refs(obj) if ref not in refs)
		physical["notes"] = notes
		items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, physical=physical, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	refs = (CORE_SOURCE, RUNTIME_SOURCE)
	return [
		{
			"id": f"display.alpha-{index + 1}", "label": f"{('Upper', 'Lower')[index]} 20-character 16-segment alphanumeric display",
			"kind": "segment", "controller_index": index, "segment_start": index * 20, "width": 20,
			"physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", *refs),
			"provenance": provenance(*refs),
		}
		for index in range(2)
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}

	def coil(address: int) -> str:
		return f"device.{slug(SOLENOID_LABELS[address])}"

	def switch(address: int) -> str:
		return f"switch.matrix-{address}"

	m = (RUNTIME_SOURCE, SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole, two-ball trough, ball release and shooter lane", "kicker",
			[coil(29), coil(28)], [switch(54), switch(44), switch(43)],
			"The machine holds two balls (IPDB: Multiball (2); the script creates two in its trough). A drained ball lands on "
			"the OUTHOLE switch (54); the OUTHOLE coil (29) kicks it into the trough, and BALL RELEASE (28) feeds the lead ball "
			"into the shooter lane, where SHOOTER LANE (43) sees it waiting at the plunger. The ROM reads TROUGH (44) at 1 as "
			"both balls home. With 44 held at 1 throughout, a tilt ended the ball at once and the ROM released the next ball "
			"with the tilted one still out; with 44 opened after the release, the ROM waited after the tilt, kicked the "
			"outhole when 54 rose and served the next ball only once 44 had closed again (runs tilt-trough-closed and "
			"tilt-trough-open). That places 44 at the trough's second position, behind the ball waiting at the release, "
			"covered only while both balls are home. At Start the ROM reset both banks, energized the Q relay (32) and "
			"energized 28 for about 0.5 s. When 54 rose it released 32 and the display read YOU DUG UP 1 STIFF; once the "
			"host had opened 54 and closed 44 again it fired 29, reset both banks, energized 32 and 28 and began ball 2 (run "
			"gameplay). The script models the trough as two kickers, Slot1 at the release and Slot2 behind it, and the "
			"outhole as the Drain kicker (writing 54). It writes 44 from Slot1, a table defect that lets a tilt put a second "
			"ball in play; its 3.0.21 update writes 44 from Slot2. The known-working script models no ball lock: it holds "
			"balls only in the trough, the outhole and the two kickers (lines 112-147 and 226-274), and plays wire-ramp "
			"sounds for both ramps' exits (lines 769-788).",
			*m, IDENTITY_SOURCE, LATER_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.left-drop-targets", "Left four-target drop bank", "drop_target_bank", [coil(8)],
			[switch(16), switch(26), switch(36), switch(46)],
			"Four drop targets, L DROP TARGET 1-4 (16, 26, 36, 46), reset together by LEFT DROP T BANK (8). The ROM fired the "
			"reset at Start, when the fourth target went down and when it served ball 2, and completing the bank began a "
			"COUNTDOWN on the display; with L DT LIGHT LOCK (65) lit, it also turned 65 off, and R BB LOCK (47) flashed twice "
			"at once and again from about 12 s later (run gameplay). The instruction cards light the right ramp lock by "
			"completing the left "
			"drop targets when lit. The script's dtBankL writes the switches and raises the bank on 8.",
			*m, CARDS_SOURCE,
		),
		mechanism(
			"mechanism.right-drop-targets", "Right four-target drop bank", "drop_target_bank", [coil(9)],
			[switch(17), switch(27), switch(37), switch(47)],
			"Four drop targets, R DROP TARGET 1-4 (17, 27, 37, 47), reset together by RIGHT DROP T BANK (9). The ROM fired the "
			"reset at Start and when it served ball 2, and with all four held down it fired 9 seven times in about 2.7 s, "
			"retrying while the targets stayed down (run gameplay). The script's dtBankR writes the switches and raises the "
			"bank on 9.",
			*m,
		),
		mechanism(
			"mechanism.kickers-and-gate", "Bottom upkicker, top kicker and gate", "kicker",
			[coil(6), coil(7), coil(10)], [switch(52), switch(53), switch(55)],
			"Two ball holds: the BOTTOM UPKICKER (switch 52, coil 6), a scoop in the middle of the playfield, and the TOP KICKER "
			"(switch 53, coil 7) at the upper left, with the TOP KICKER RO rollover (55) on the lane above it. Held at 1 for "
			"8 s during a game, 52 drew six pulses of 6 and 53 eight pulses of 7 (run gameplay): the ROM kicks again while its "
			"switch stays closed. The script models both as saucers and moves the scoop's sw52p primitive with 6. GATE (10) is "
			"a diverter flap the script turns about Primitive DiverterP above the top kicker. Unresolved: the instruction "
			"cards light the right ramp for a lock (complete the left drop targets when lit) and award an instant multiball "
			"from the door prize. In the scripted game, completing the left bank while L DT LIGHT LOCK (65) was lit turned "
			"65 off; R BB LOCK (47) flashed twice at once, stayed dark until about 12 s later and then flashed through one "
			"pulse of the right ramp switch (50), which fired no gate and left 47 flashing. The host never closed the top "
			"kicker (53) afterwards. 10 rose only in the coil test, "
			"and the known-working script models no lock device. The ROM's full lock sequence, which path the gate opens, "
			"whether the top kicker holds the locked ball, and how the lock releases for multiball are therefore not known. A gameplay run that lights the lock and then writes the "
			"right ramp (50) and the top kicker (53) would show the ROM's sequence on 10, 7 and the ball release 28, but "
			"there the host supplies the ball path; the gate's physical route and where the ball is held need the manual, a "
			"factory drawing or an observation of a real machine.",
			*m, CARDS_SOURCE,
		),
		mechanism(
			"mechanism.heart-and-teeth", "Beating heart and chattering teeth", "toy",
			[coil(11), coil(12), coil(25), "lamp.matrix-2"], [],
			"The two toys IPDB lists stand against the back panel at the rear of the playfield (IPDB photos 12 and 13), the "
			"chattering teeth on a bracket left of the beating heart. HEART (11) beats the heart and HEART 67 (2) (25) lights "
			"it from two bulbs; TEETH (12) works the jaw and lamp 2 (TEETH) lights the teeth. The ROM chattered the teeth "
			"in two bursts of pulses, sixteen from about 2.5 s to 8.2 s after Start, the first held about 1.1 s and the "
			"others 0.06-0.34 s, and thirteen of 0.06-0.07 s each over about 1.7 s, beginning within 0.1 s of the first of "
			"two spinner pulses 0.8 s apart (run gameplay). The script pumps the heart primitive once "
			"each time 11 turns on and holds the lower jaw at one angle while 12 is on and another while it is off.",
			*m, IDENTITY_SOURCE, TEETH_PHOTO_SOURCE, HEART_PHOTO_SOURCE,
		),
		mechanism(
			"mechanism.cpu-fired-coils", "Pop bumpers and kicking rubbers", "other",
			[coil(1), coil(2), coil(3), coil(4), coil(5)], [switch(10), switch(11), switch(12), switch(13), switch(14)],
			"Three pop bumpers (switches 10, 11 and 12, coils 1, 2 and 3) and two kicking rubbers, the slingshots (switches 13 "
			"and 14, coils 4 and 5). System 3 has no special-solenoid circuit: the CPU reads each switch and fires its coil "
			"(40 ms pulses of each switch during a game fired its coil, run gameplay), so a consumer drives only the switch. The "
			"script assigns no callbacks to these coils and kicks with its own physics.",
			*m,
		),
		mechanism(
			"mechanism.flippers", "Two flippers, cabinet-wired", "other", [coil(32)], [switch(6), switch(7)],
			"Two flippers. The cabinet buttons fire them through the flipper circuit while the Q relay (32) is energized, so "
			"no CPU driver appears for them in the solenoid test; PinMAME fabricates 45-48 from the buttons at 141 and 143 "
			"while 32 is on. The ROM reads the buttons as matrix switches 6 (LEFT FLIPPER) and 7 (RIGHT FLIPPER), which "
			"core_updateSw copies from 143 and 141.",
			*m, VPM_LIBRARY_SOURCE,
		),
		mechanism(
			"mechanism.relays-and-cabinet", "Relays, knocker and coin meter", "other",
			[coil(26), coil(31), coil(30), coil(27)], [],
			"The 'A' relay (26) switches the backbox lightbox illumination and the 'T' relay (31) the playfield G.I., which "
			"goes out while it is energized; PinMAME's System 3 init types them so, and the later 3.0.21 script drives the "
			"backglass and playfield G.I. from them. In the scripted game the ROM raised both with the flashers as the left bank and five spot targets scored (run gameplay). The KNOCKER "
			"(30) would be in the cabinet, but no retained source shows it fitted, and COIN MET/TIX COIL (27) drives an "
			"optional coin meter or ticket dispenser.",
			*m, LATER_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": f"relationship.flipper-column-{button}-to-matrix-{target}", "kind": "direct",
			"source": f"switch.flipper-column-{button}", "destination": f"switch.matrix-{target}",
			"provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE),
		}
		for button, target in ((141, FLIP_SWNO[1]), (143, FLIP_SWNO[0]))
	]


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


COVERAGE_MISSING = ["output_semantics", "mechanism_behavior", "spatial_placement"]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Class of 1812", "manufacturer": "Gottlieb", "year": 1991, "kind": "physical_pinball",
			"model_number": "730", "ipdb_id": 528, "opdb_id": "G5DYX-M0oVW",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE, status="observed")},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "unknown", "mechanisms": "observed", "variant_coverage": "validated",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.gts3", "hardware_generation": "0x20000000000", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "partial"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Class of 1812 device identifiers are not unique: {duplicates}")
	labels = [device["label"] for device in definition["outputs"] if device["binding"]["group"] == "pinmame.output.lamp"]
	repeated = sorted({label for label in labels if labels.count(label) > 1 and not label.startswith("Not Used")})
	if repeated:
		raise RuntimeError(f"Class of 1812 lamp labels are not unique: {repeated}")
	return definition


SPATIAL_BLOCKERS = [
	"No factory drawing is retained: IPDB lists the English manual without hosting it (the file is a 0-byte placeholder) "
	"and no other attributable copy was found, so no placement can be checked against the machine's own switch, lamp or "
	"coil location drawings.",
	"Only one table lineage is retained: the NZ&TT 1.0 table by tom tower & ninuzzu, whose pinned known-working script is "
	"the same table's, and the 3.0.21 script is a later update of it. No independently built geometry confirms a "
	"placement, so every placement stays observed.",
	"The heart (solenoids 11 and 25) and the teeth (solenoid 12 and lamp 2) are table meshes centred behind the "
	"playfield's rear edge; IPDB photos 12 and 13 show both toys against the back panel, so each is clamped to y = 0 with "
	"its raw value disclosed, without a drawing to measure from.",
	f"Solenoid 31 (T relay, playfield G.I.): the {len(GI_BULBS)} placements are the members of the table's GI collection "
	f"that show a bulb mesh; {', '.join(GI_RENDER_ONLY[:-1])} and {GI_RENDER_ONLY[-1]} show none and are not placed. A "
	"table's grouping is not the machine's wiring and the bulb count is unknown, so they stay observed without a quantity.",
	"Solenoids 13-21 are flashers that both scripts treat as backbox (translite) flashers, but no manual confirms it, so "
	"none of the nine is placed or classified. Solenoids 22 and 23 are placed at the lights under the two domes the "
	"script pairs with each, and 24 at the light under its blue dome. The scripts also draw 24 on a light under the "
	"ramp, a bulb-less render light and so a table effect; whether a second bulb is fitted there is unknown, and it is "
	"not placed. The ROM's coil test gives no bulb count for 22-24.",
	f"The {len(INSERT_LAMPS)} matrix lamps drawn on the table's image-mode insert overlays ('{INSERT_IMAGE}') are "
	"projected onto each overlay's centre: the table models no bulb under the inserts, so each point is the insert's "
	"centre, not a measured socket.",
	"The drop-bank resets 8 and 9 are projected onto the centre of their banks, and the Bat-O-Meter lamps 10-14 onto the "
	"bulb primitives of the table's vertical stack. IPDB photo 19 shows the Bat-O-Meter as a five-row sign at the upper "
	"left with its values in the same order, but a perspective photo gives no coordinates, so the points stay the "
	"table's.",
	f"Lamps {' and '.join(str(address) for address in UNEXPLAINED_LAMPS)}, which the ROM names NOT USED but drives in "
	"play, have no table object and are not placed; whether a bulb is fitted there is unknown.",
]


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted_inputs, omitted_outputs = [], [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for collection, located_list, omitted in (("inputs", located_inputs, omitted_inputs), ("outputs", located_outputs, omitted_outputs)):
		for device in definition[collection]:
			binding: Any = device["binding"]["device"] if collection == "inputs" else {"group": device["binding"]["group"], "address": device["binding"]["device"]}
			spatial = device.get("spatial")
			if spatial is None:
				omitted.append(binding)
			elif spatial["status"] == "not_applicable":
				(na_inputs if collection == "inputs" else na_outputs).setdefault(spatial["reason"], []).append(binding)
			else:
				located_list.append(binding)
				for item in spatial["placements"]:
					placement_count += 1
					statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1

	def output_key(item: dict[str, Any]) -> tuple[str, int]:
		return (item["group"], item["address"])

	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": EMBEDDED_SCRIPT_SHA256, "table_sha256": TABLE_SHA256, "obj_export_sha256": OBJ_SHA256},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=output_key),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=output_key) for reason, values in sorted(na_outputs.items())},
		"omitted_inputs": sorted(omitted_inputs),
		"omitted_outputs": sorted(omitted_outputs, key=output_key),
		"projections": [
			{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."}
			for address, reason in sorted(SOLENOID_PROJECTED.items())
		] + [
			{"group": "pinmame.output.lamp", "address": 2, "reason": "Placed at the teeth toy (Primitive TopTeeth, world mesh centre), clamped onto the rear edge."},
		] + [
			{"group": "pinmame.output.lamp", "address": address, "reason": INSERT_PROJECTION}
			for address in INSERT_LAMPS
		],
		"excluded_object_classes": [
			"Lights L36, L37, L46, L47, L67 and L67a, which InitLamps binds to lamps 36, 37, 46, 47 and 67 and which show no bulb mesh: the bulb primitives bulb1-bulb4 and bulb10 the script draws those lamps on are the placements, and L67a is a second light on lamp 67 (no other lamp has an L<n>a double)",
			f"G.I. Lights {', '.join(GI_RENDER_ONLY[:-1])} and {GI_RENDER_ONLY[-1]}, members of the GI collection that show no bulb mesh: render lights, not sockets",
			"Light F24, which the script draws solenoid 24 on under the ramp: no dome covers it and it shows no bulb mesh",
			"Flasher sprites Li2, Li10-Li14, F22r1-F22r4, F22r1x, F22r2x, F23r, F24r1, F24r2 and F25, which the script draws beside the lights, and pfsh, which nothing drives; a sprite is a render helper, not a socket",
			"The flasher domes domeYB, domeW, domeYT, domeR and domeB, whose Lights F22, F22a, F22x, F23 and F24a are the placements",
			"Trigger sw53, which no handler binds (the script's top kicker is Kicker sw53k), and Kicker CenterHole beside the scoop",
			"The ramp sound triggers LREnter, LRExit, LRHelp1, LRail, rrenter, RRExit, RRHelp1-RRHelp3 and RRail, which write no switch",
			"The 640 a<nn>, b<nn> and c<nn> Light objects the script's Digits arrays light as the alphanumeric display segments, and the cabinet and backbox objects",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Class of 1812 (Gottlieb, 1991) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/gottlieb/class-of-1812-1991.json`; "
		f"its spatial dimension stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained `{TABLE_FILENAME}` by tom tower & ninuzzu, SHA-256 `{TABLE_SHA256}`. Its "
		f"embedded script (SHA-256 `{EMBEDDED_SCRIPT_SHA256}`) is the pinned known-working script before a 2018 patch that "
		f"changed no playfield binding. Bounds are `{TABLE_BOUNDS}`; every coordinate is x/952 and y/1974, rounded to at most "
		"six places. `evidence/excerpts/gottlieb.class-of-1812.1991/vpx-table-objects.md` lists each placed object, its "
		"coordinate and the script lines that bind it, and the curator's `verify_retained_table` re-derives every coordinate "
		"from the retained extraction and OBJ export.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the table object the script binds to the address: a trigger, target, spinner, kicker, bumper or "
		"slingshot wall for a switch, the bulb primitive the script draws a lamp on, the light under each flasher dome, the "
		"object a coil moves or kicks from, and each member of the GI collection `TiltRelay` switches that shows a bulb "
		"mesh. A matrix lamp without a bulb primitive is projected onto the image-mode `l<n>` insert overlay `InitLamps` "
		"binds to it.",
		"- Switch 44 is placed at Kicker `Slot2`, the trough's second position, not at `Slot1` where the known-working "
		"script binds it: the ROM's trough probes show 44 closes only while both balls are home, and the table's 3.0.21 "
		"update binds it to `Slot2`.",
		"- Render lights that show no bulb mesh and sit under no flasher dome (four G.I. lights and `F24`) make no socket "
		"and are not placed.",
		"- Primitives whose stored position is not the part's centre (the slingshot arms, the heart, the teeth, the "
		"Bat-O-Meter bulbs and the billboard and crypt bulbs) are placed at the centre of their world-space mesh from "
		"`vpxtool export obj --units vpu`.",
		"- The heart and teeth meshes centre behind the rear edge; IPDB photos 12 and 13 show both toys against the back "
		"panel, so their placements are clamped to y = 0 and the raw centre is disclosed in each device note.",
		"- Coils with no table object of their own are documented projections onto their own mechanism's object; a bank "
		"reset lands on the mean of its four targets.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the A and Q relays, the knocker, the coin "
		"meter, the cabinet and flipper-button switches, the test inputs and the two displays.",
		"- No placement is validated: no factory drawing is retained to check it, and only one table lineage is.",
		"",
		"## Explicit projections",
		"",
	]
	grouped: dict[tuple[str, str], list[int]] = {}
	for entry in report["projections"]:
		grouped.setdefault((entry["group"], entry["reason"]), []).append(entry["address"])
	for (group, reason), addresses in grouped.items():
		short = {"pinmame.input.switch": "Switch", "pinmame.output.solenoid": "Solenoid", "pinmame.output.lamp": "Lamp"}[group]
		label = f"{short} {addresses[0]}" if len(addresses) == 1 else f"{short}s {', '.join(str(address) for address in addresses)}"
		lines.append(f"- {label}: {reason}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Inputs with an omitted spatial key: {len(report['omitted_inputs'])}",
		f"- Outputs with an omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Excluded table objects", ""] + [f"- {entry}" for entry in report["excluded_object_classes"]]
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the "
		"mechanisms are inventoried, and polarity is settled for every switch by the read path, the ROM's Switch Matrix Test "
		"and the known-working script. Promotion to `author_ready` is refused, and `coverage.missing` is "
		f"`{json.dumps(COVERAGE_MISSING)}`: lamps {' and '.join(str(address) for address in UNEXPLAINED_LAMPS)}, which the "
		"ROM names NOT USED, publish state in play that no source explains, and no source shows the knocker (30) fitted; "
		"the ball lock the instruction cards describe was lit in the scripted game but never made, so the gate's path and "
		"the lock's hold and release are unknown; and every playfield placement rests on one community table lineage's geometry with nothing "
		"independent to check it. The service manual's lamp chart and its switch, lamp and coil location drawings, or a "
		"second table built independently from the machine, would settle the outputs, the placements and the backbox "
		"flashers 13-21. A gameplay run through the lock would show the ROM's lock sequence; the gate's physical route and "
		"the hold point need the manual, a factory drawing or an observation of a real machine.",
		"",
	]
	return "\n".join(lines)


def knowledge_bytes(root: Path = ROOT) -> bytes:
	"""The pinned knowledge note: the seed's bytes, which must be UTF-8 with LF line endings."""
	payload = (root / KNOWLEDGE_SEED_PATH.relative_to(ROOT)).read_bytes()
	if b"\r" in payload:
		raise RuntimeError(f"Class of 1812 knowledge seed has a carriage return: {KNOWLEDGE_SEED_PATH}")
	payload.decode("utf-8")
	return payload


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Class of 1812 definition with a {STATUS} one: {stale}")
		stale.unlink()
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	write_bytes(root / KNOWLEDGE_PATH, knowledge_bytes(root))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Class of 1812 is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Class of 1812 definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Class of 1812 seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Class of 1812 spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_bytes() != render_spatial_report(report).encode("utf-8"):
		raise RuntimeError(f"Class of 1812 spatial review drifted from its deterministic curator: {markdown_path}")
	knowledge_path = root / KNOWLEDGE_PATH
	if not knowledge_path.is_file() or knowledge_path.read_bytes() != knowledge_bytes(root):
		raise RuntimeError(f"Class of 1812 knowledge note is not byte-identical to its seed: {knowledge_path}")
	print("Class of 1812 definition, seed, spatial report and knowledge note match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed, the spatial report and the knowledge note")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
