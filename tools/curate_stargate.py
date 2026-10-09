"""Curate the physical Gottlieb Stargate (1995) machine definition.

The builder is side-effect free and deterministic: every reviewed label and table coordinate is a literal here, so
regeneration reproduces the canonical definition, its pinned seed and the spatial report byte for byte without reading
the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes them.

Stargate is a Gottlieb System 3 DMD machine (``GEN_GTS3``, ``mGTS3DMDS``). Every one of its six drivers declares
``INITGAME2(<set>, DMD, FLIP8182, 4, SNDBRD_GTS3, 5)``: the cabinet port flagged ``0x8000`` (coins, Start, Tournament and
Coin Door on public 0-6), cabinet-wired flippers copied into matrix switches 81 and 82 from PinMAME's flipper column
(public 143 and 141), and ``hw.lampCol = 5``, which adds the auxiliary driver board's eight outputs at lamps 120-127.
No service manual is retained: IPDB lists one but does not host it. The ROM's own service tests name every switch,
lamp, solenoid and auxiliary driver, and a harness run of each pairs the name with the public address it drives or
reads (``evidence/runtime/gts3/stargate-<set>-service-tests.json``).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "gottlieb.stargate.1995"
PARTIAL_PATH = ROOT / "machines/partial/gottlieb/stargate-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/gottlieb/stargate-1995.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/gottlieb/stargate-1995.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/gottlieb/stargate-1995-legacy-aliases.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/gottlieb/stargate-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/gottlieb/stargate-1995.md"
KNOWLEDGE_PATH = "knowledge/gottlieb/stargate-1995.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID

PRIMARY_SET = "stargat5"
VARIANT_SETS = ("stargate", "stargat4", "stargat3", "stargat2", "stargat1")


def runtime_evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/gts3/stargate-{game}-service-tests.json"


def runtime_source(game: str) -> str:
	return f"runtime.stargate.{game}-service-tests"


PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-gts3"
IDENTITY_SOURCE = "identity.gottlieb.stargate.1995"
RUNTIME_SOURCE = runtime_source(PRIMARY_SET)
VPX_TABLE_SOURCE = "vpx-table.stargate-vpw-2-0"
VPX_SCRIPT_SOURCE = "vpx-script.stargate-vpw-2-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.stargate-vpw-2-0"
VPX_OBJ_SOURCE = "vpx-obj-export.stargate-vpw-2-0"
MORTTIS_SCRIPT_SOURCE = "vpx-script.stargate-morttis-1-3-0"
VPM_LIBRARY_SOURCE = "vpm-script-library.gts3-vbs"
VPM_LIBRARY_URI = "external:pinmame-review-artifacts/vpm-script-libs/gts3.vbs"
VPM_GTS3_SHA256 = "66c329fa86e97d2f10a8036a9a6527be6a67ce59bb3591962aa1c8a9da101314"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

IPDB_PAGE_SHA256 = "40bae4cc334d154348995d86cd6fb9f2b427465cff199352e95a546d462cafa0"
TABLE_SHA256 = "581ffc6fc4f5f1cb2b835d8e341272215ce41f4c5e25064cdfc30fe61848904b"
SCRIPT_SHA256 = "eda1f035a56672f83411efe228ff98291a2bdaf9b85114d1da7dc4ab337974a1"
OBJ_EXPORT_SHA256 = "28651ac96e06abc549f45ebcc96608454dbd751e01a89afd9e572340e180b850"
MORTTIS_TABLE_SHA256 = "344f0454b9fbdb9603dd7ff896f0f665169870b4c902aabcb9d3ad2da07ce256"
MORTTIS_SCRIPT_SHA256 = "113a65ebceab8ad9912eb122390302e14991cc340f1e8c49dae46bd7a931ecba"

EXTRACTION_RELATIVE_PATH = Path("gottlieb/stargate-1995/v2.0/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("gottlieb/stargate-1995/v2.0/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 2354
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "887813c8c8879ef20647843062dea57884fd17263ac802e66be9998c018a6c73"

PLAYFIELD_WIDTH = 952.941
PLAYFIELD_HEIGHT = 2164.706
TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=2164.706"

# (left, right) in the driver's own FLIP_SWNO macro order (FLIP8182).
FLIP_SWNO = (81, 82)


def norm(x: float, y: float) -> tuple[float, float]:
	"""Normalize a retained-table coordinate (VPX units) into the canonical playfield space."""
	return (round(x / PLAYFIELD_WIDTH, 6), round(y / PLAYFIELD_HEIGHT, 6))


DRIVER_IDS = ("stargate", "stargat1", "stargat2", "stargat3", "stargat4", "stargat5")
_SHARED = (
	"Declared with the same INITGAME2(<set>, DMD, FLIP8182, 4, SNDBRD_GTS3, 5) line as every other Stargate driver "
	"(pinned src/wpc/gts3games.c lines 613-665), so it shares GEN_GTS3, the 128x32 DMD layout, the cabinet port, the "
	"FLIP_SWNO(81,82) flipper wiring, hw.lampCol = 5 and the mGTS3DMDS machine driver, and it plays the same sound ROMs."
)
_COMPARED = (
	" Its Lamp Matrix, Relay & Solenoid, Aux Driver and Switch Edges tests name every address exactly as stargat5's do "
	"(run comparison in its runtime evidence)."
)
DRIVER_COMPATIBILITY = {
	"stargat5": (
		"identical",
		"Revision 5 game ROM (stgtcpu5.512) with the rev. 3 display ROM (dsprom3.bin); its boot screen reads Game #742/5. "
		"The driver both retained tables load (cGameName = \"stargat5\") and the one every runtime probe here ran on. " + _SHARED,
	),
	"stargat4": (
		"identical",
		"Revision 4 game ROM (gprom4.bin, which the pinned source says \"fixes at least the 'Beeping and Garbled DMD' issue\") "
		"with the rev. 3 display ROM (dsprom3.bin); its boot screen reads Game #742/4. " + _SHARED + _COMPARED,
	),
	"stargat3": ("identical", "Revision 3 game and display ROMs (gprom3.bin, dsprom3.bin); its boot screen reads Game #742/3. " + _SHARED + _COMPARED),
	"stargat2": ("identical", "Revision 2 game and display ROMs (gprom2.bin, dsprom2.bin); its boot screen reads Game #742/2. " + _SHARED + _COMPARED),
	"stargat1": ("identical", "Revision 1 game and display ROMs (gprom1.bin, dsprom1.bin); its boot screen reads Game #742/1. " + _SHARED + _COMPARED),
	"stargate": (
		"identical",
		"The clone tree's root, catalogued without a revision number (gprom.bin, dsprom.bin); its boot screen reads Game #742 "
		"with no revision suffix. " + _SHARED + _COMPARED,
	),
}

# --- Switches. Public addresses are Gottlieb's own decimal numbers (gts3_sw2m): tens digit strobe, units digit return.
# ROM_SWITCH_NAMES is the name the Switch Edges Test (self-test 6) displays while the host holds the address at 1.
ROM_SWITCH_NAMES = {
	0: "COIN CHUTE #1 -LEFT", 1: "COIN CHUTE #2 -RIGHT", 2: "COIN CHUTE #3 -CENTER", 3: "COIN CHUTE #4",
	5: "TOURNAMENT", 6: "FRONT DOOR (SERVICE)", 7: "(NOT USED)",
	10: "BOTTOM POP BUMPER", 11: "TOP POP BUMPER", 12: "LEFT KICKING RUBBER", 13: "RIGHT KICKING RUBBER",
	14: "LEFT KICKING TARGET", 15: "CENTER KICKING TARGET", 16: "RIGHT KICKING TARGET", 17: "LEFT DROP TARGET #1",
	20: "GLIDER LEFT (MOTOR)", 21: "GLIDER MOTOR STOP", 22: "BULLSEYE TAR (INNER)", 23: "TOP CENTER UPKICKER",
	24: "OUTHOLE", 25: "LOWER LEFT KICKER", 26: "CENTER DROP TARGET #1", 27: "LEFT DROP TARGET #2",
	30: "GLIDER RIGHT (MOTOR)", 31: "SHOOTER LANE ROLLOVER", 32: "BULLSEYE TAR (OUTER)", 33: "TOP RIGHT UPKICKER",
	34: "TROUGH", 35: "ROLLOVER DROP TARGET", 36: "CENTER DROP TARGET #2", 37: "LEFT DROP TARGET #3",
	80: "TOP L. UPKICKER -OPTO", 81: "LEFT FLIPPER", 82: "RIGHT FLIPPER",
	90: "LOWER LEFT RAMP -OPTO", 91: "TOP PYRAMID -OPTO",
	100: "TOP LEFT RAMP -OPTO", 101: "BALL GATE -SENSOR", 102: "TOP PYRAMID -SENSOR",
	110: "TOP RIGHT RAMP -OPTO", 111: "LEFT OUTLANE", 112: "LEFT RETURN ROLLOVER", 113: "RIGHT RETURN ROLLOVER",
	114: "RIGHT OUTLANE", 115: "LEFT SIDE ROLLOVER", 116: "LEFT PIVOT TARGET", 117: "RIGHT PIVOT TARGET",
}
MATRIX_ADDRESSES = tuple(column * 10 + row for column in range(12) for row in range(8))
UNUSED_SWITCHES = frozenset(address for address in MATRIX_ADDRESSES if ROM_SWITCH_NAMES.get(address) == "(NOT USED)" or (address not in ROM_SWITCH_NAMES and address != 4))
SWITCH_LABELS = {
	0: "Coin Chute #1 (Left)", 1: "Coin Chute #2 (Right)", 2: "Coin Chute #3 (Center)", 3: "Coin Chute #4",
	4: "Credit Button (Start)", 5: "Tournament Button", 6: "Front Door (Coin Door Closed)",
	10: "Bottom Pop Bumper", 11: "Top Pop Bumper", 12: "Left Kicking Rubber (Slingshot)", 13: "Right Kicking Rubber (Slingshot)",
	14: "Left Kicking Target", 15: "Center Kicking Target", 16: "Right Kicking Target", 17: "Left Drop Target #1",
	20: "Glider Left (Motor)", 21: "Glider Motor Stop", 22: "Bullseye Target (Inner)", 23: "Top Center Upkicker",
	24: "Outhole", 25: "Lower Left Kicker", 26: "Center Drop Target #1", 27: "Left Drop Target #2",
	30: "Glider Right (Motor)", 31: "Shooter Lane Rollover", 32: "Bullseye Target (Outer)", 33: "Top Right Upkicker",
	34: "Trough", 35: "Rollover Drop Target", 36: "Center Drop Target #2", 37: "Left Drop Target #3",
	80: "Top Left Upkicker Opto", 81: "Left Flipper (Matrix Copy)", 82: "Right Flipper (Matrix Copy)",
	90: "Lower Left Ramp Opto", 91: "Top Pyramid Opto",
	100: "Top Left Ramp Opto", 101: "Ball Gate Sensor", 102: "Top Pyramid Sensor",
	110: "Top Right Ramp Opto", 111: "Left Outlane", 112: "Left Return Rollover", 113: "Right Return Rollover",
	114: "Right Outlane", 115: "Left Side Rollover", 116: "Left Pivot (Horus) Target", 117: "Right Pivot (Horus) Target",
}
OPTO_SWITCHES = frozenset({80, 90, 91, 100, 110})
# Used switches no retained source shows the active level of.
POLARITY_UNKNOWN = frozenset({20})
CABINET_SWITCH_ROLES = {
	0: "cabinet.coin", 1: "cabinet.coin", 2: "cabinet.coin", 3: "cabinet.coin", 4: "cabinet.start", 5: "cabinet.service",
	6: "cabinet.coin-door", 81: "cabinet.flipper", 82: "cabinet.flipper",
}
CABINET_SWITCH_TYPES = {4: "button", 5: "button"}
# Runtime proof that the ROM treats public 1 as the actuated state (gameplay, tournament-door and front-door runs).
ROM_ACTIVE_AT_1 = {
	0: "the Front Door Test counted one coin on chute 1 per pulse at 1 (run front-door), and two pulses gave one credit (run gameplay)",
	1: "the Front Door Test counted one coin on chute 2 for the pulse at 1 (run front-door)",
	2: "the Front Door Test counted one coin on chute 3 for the pulse at 1 (run front-door)",
	3: "the Front Door Test counted one coin on chute 4 for the pulse at 1 (run front-door)",
	4: "a pulse at 1 with one credit started a game (run gameplay)",
	5: "closing it at 1 in attract mode brought up the TOURNAMENT MODE settings screen (FREE PLAY = OFF, GAME FEATURES = NORMAL, ...) (run tournament-door)",
	6: "coins inserted while it was held at 1 gave a credit, and with it back at 0 the tournament screen read CLOSE DOOR TO BEGIN PLAY (run tournament-door)",
	10: "of three 100 ms pulses at 1 during a game, one made the ROM fire 1, BOTTOM POP BUMPER (run gameplay)",
	13: "of three 100 ms pulses at 1 during a game, two made the ROM fire 4, RIGHT KICKING RUBBER (run gameplay)",
	14: "of three 100 ms pulses at 1 during a game, two made the ROM fire 5, LEFT KICKING TARGET (run gameplay)",
	15: "of three 100 ms pulses at 1 during a game, one made the ROM fire 6, CENTER KICKING TARGET (run gameplay)",
	16: "of three 100 ms pulses at 1 during a game, two made the ROM fire 7, RIGHT KICKING TARGET (run gameplay)",
	23: "held at 1 for 1.2 s during a game, the ROM fired 11, TOP CENTER UPKICKER, twice (run gameplay)",
	24: "held at 1 for 2 s, the ROM fired 29, OUTHOLE, three times about 0.7 s apart (run gameplay)",
	25: "held at 1 for 1.2 s during a game, the ROM opened the ball gate (13) and then fired 8, LOWER LEFT KICKER (run gameplay)",
	34: "about 2.6 s after it rose to 1 following the second outhole kick, the ROM fired 28, BALL RELEASE (run gameplay)",
	81: "with the left flipper button (143), which core_updateSw copies into it, at 1, the menu stepped to the next item (run nvram-init)",
	82: "with the right flipper button (141), which core_updateSw copies into it, at 1, the menu selected SELF-TEST and each test stepped to its next item (runs lamp-matrix, solenoids, aux-drivers)",
}
# Script authority for a level the runs do not exercise: what the known-working table writes when the device is actuated.
SCRIPT_ACTIVE_AT_1 = {
	17: "DTHit 17 and the DropTarget class write 1 when the target has dropped and 0 when it is raised (lines 1531, 3342, 3398)",
	27: "DTHit 27 and the DropTarget class write 1 when the target has dropped and 0 when it is raised (lines 1532, 3342, 3398)",
	37: "DTHit 37 and the DropTarget class write 1 when the target has dropped and 0 when it is raised (lines 1533, 3342, 3398)",
	26: "DTHit 26 and the DropTarget class write 1 when the target has dropped and 0 when it is raised (lines 1536, 3342, 3398)",
	36: "DTHit 36 and the DropTarget class write 1 when the target has dropped and 0 when it is raised (lines 1537, 3342, 3398)",
	35: "DTHit 35 and the DropTarget class write 1 when the target is down and 0 when it is raised (lines 1539, 3342, 3398)",
	21: "GliderTimer_Timer writes 1 while the glider is retracted to its home position (lines 1406-1410)",
	11: "Bumper2_Hit pulses it (lines 1049-1050)", 12: "LeftSlingShot_Slingshot pulses it (lines 1895-1897)",
	33: "sw33_Hit writes 1 while the ball sits in the kicker and sw33_UnHit 0 (lines 928-939)",
	80: "sw80_Hit writes 1 while the ball sits in the kicker and sw80_UnHit 0 (lines 978-989)",
	30: "GliderTimer_Timer writes 1 while the left-right swing is at its right end (lines 1412-1416)",
	22: "sw22_Hit pulses it (line 1115)", 32: "STHit 32 pulses it (lines 1541, 3033)",
	31: "SW31_Hit writes 1 while the ball is on the rollover (line 1118)",
	90: "sw90_Hit pulses it (line 1189)", 100: "sw100_Hit pulses it (line 1190)", 110: "sw110_Hit pulses it (line 1191)",
	91: "sw91_Hit pulses it (lines 1256-1257)",
	101: "SolDiv writes 1 while the ball gate coil (13) is on and 0 when it is off (lines 782-792)",
	102: "SolPyramid writes 1 half a second after the pyramid coil (16) turns on and 0 half a second after it turns off (line 1339)",
	111: "SW111_Hit writes 1 while the ball is on the wire (line 1120)", 112: "SW112_Hit writes 1 (line 1122)",
	113: "SW113_Hit writes 1 (line 1124)", 114: "SW114_Hit writes 1 (line 1126)", 115: "SW115_Hit writes 1 (line 1128)",
	116: "the v1.3.0 script's sw116_Hit pulses it on a hit (line 970); the VPW table's binding is defective, below", 117: "the v1.3.0 script's sw117_Hit pulses it on a hit (line 988); the VPW table's binding is defective, below",
}

# --- Switch placements: retained-table (VPW v2.0) object centres in VPX units, the object the script binds.
SWITCH_OBJECTS = {
	10: ("Bumper Bumper1", (177.58493, 1093.712)), 11: ("Bumper Bumper2", (112.81917, 884.93317)),
	12: ("Wall LeftSlingShot (drag-point mean)", (227.011128, 1509.372417)),
	13: ("Wall RightSlingShot (drag-point mean)", (640.506338, 1510.241483)),
	14: ("HitTarget sw14", (298.5, 855.87)), 15: ("HitTarget sw15", (356.86, 508.4)), 16: ("HitTarget sw16", (736.78, 1233.1)),
	17: ("Primitive BM_DT_sw17 (world mesh centre)", (179.9361, 1261.3621)),
	22: ("Trigger sw22", (537.18, 496.38)), 23: ("Trigger sw23", (672.02, 91.73)), 24: ("Kicker Drain", (454.35745, 2028.6724)),
	25: ("Kicker sw25", (51.970787, 1883.4116)),
	26: ("Primitive BM_DT_sw26 (world mesh centre)", (358.182, 939.484)),
	27: ("Primitive BM_DT_sw27 (world mesh centre)", (215.549, 1225.5177)),
	31: ("Trigger sw31", (896.78, 1890.65)), 32: ("HitTarget sw32", (540.03, 488.13)), 33: ("Trigger sw33", (860.55, 92.35)),
	34: ("Kicker swTrough3", (684.6303, 1888.7783)),
	35: ("Primitive BM_DT_sw35 (world mesh centre)", (871.4435, 721.8806)),
	36: ("Primitive BM_DT_sw36 (world mesh centre)", (382.8493, 898.2439)),
	37: ("Primitive BM_DT_sw37 (world mesh centre)", (251.8556, 1189.4425)),
	80: ("Trigger sw80", (205.24, 121.04)), 90: ("Trigger sw90", (124.83, 1267.2)), 91: ("Trigger sw91", (435.35, 120.8)),
	100: ("Trigger sw100", (222.8, 308.34)), 110: ("Trigger sw110", (666.85, 304.83)),
	111: ("Trigger sw111", (56.17, 1579.56)), 112: ("Trigger sw112", (136.17, 1560.0)), 113: ("Trigger sw113", (721.94, 1535.65)),
	114: ("Trigger sw114", (813.31, 1580.61)), 115: ("Trigger sw115", (57.53, 1253.96)),
	116: ("HitTarget sw116", (174.8, 760.48)), 117: ("HitTarget sw117", (653.21, 504.24)),
}
GLIDER = (423.5749, 331.9704)
PYRAMID = (434.7423, 342.2717)
BALL_GATE = (121.41875, 1763.2825)
SWITCH_PROJECTIONS = {
	20: (GLIDER, (
		"Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the switch senses the Glidercraft's left-right "
		"drive and has no table object; the retained script never writes it."
	)),
	21: (GLIDER, (
		"Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the script writes it from its GliderTimer when "
		"the glider is retracted (lines 1406-1410) and has no object for the switch."
	)),
	30: (GLIDER, (
		"Projected onto the glider (Primitive BM_Glider_1, world mesh centre): the script writes it from its GliderTimer at "
		"the right end of the swing (lines 1412-1416) and has no object for the switch."
	)),
	101: (BALL_GATE, (
		"Projected onto the lower left ball gate (Flipper Flipper1, object centre), the moving part whose position the "
		"script reports here from SolDiv (lines 782-792); the sensor has no object of its own."
	)),
	102: (PYRAMID, (
		"Projected onto the pyramid top (Primitive BM_Pyramid1, world mesh centre), whose open state the script reports here "
		"from SolPyramid (line 1339); the sensor has no object of its own."
	)),
}

# --- Solenoids. ROM_COIL_NAMES[public] is the Relay & Solenoid Test's name for driver (public - 1).
ROM_COIL_NAMES = {
	1: "BOTTOM POP BUMPER", 2: "TOP POP BUMPER", 3: "LEFT KICKING RUBBER", 4: "RIGHT KICKING RUBBER",
	5: "LEFT KICKING TARGET", 6: "CENTER KICKING TARGET", 7: "RIGHT KICKING TARGET", 8: "LOWER LEFT KICKER",
	9: "SHOOTER LANE KICKER", 10: "TOP LEFT UPKICKER", 11: "TOP CENTER UPKICKER", 12: "TOP RIGHT UPKICKER",
	13: "LOWER LEFT BALL GATE", 14: "LEFT PIVOT TARGET", 15: "RIGHT PIVOT TARGET", 16: "TOP PYRAMID",
	17: "3-BANK DROP TAR RESET", 18: "2-BANK DROP TAR RESET", 19: "ROLLOVER TARGET RESET", 20: "ROLLOVER TARGET TRIP",
	21: "NOT USED", 22: "ROPE LIGHTS (18)", 23: "GLIDER MOTOR (L & R)", 24: "GLIDER MOTOR -FORWARD", 25: "NOT USED",
	26: "LIGHTBOX RELAY (A)", 27: "TICKET/COIN METER", 28: "BALL RELEASE", 29: "OUTHOLE", 30: "KNOCKER",
	31: "TILT RELAY (T)", 32: "GAME OVER RELAY (Q)",
}
SOLENOID_LABELS = {
	1: "Bottom Pop Bumper", 2: "Top Pop Bumper", 3: "Left Kicking Rubber (Slingshot)", 4: "Right Kicking Rubber (Slingshot)",
	5: "Left Kicking Target", 6: "Center Kicking Target", 7: "Right Kicking Target", 8: "Lower Left Kicker",
	9: "Shooter Lane Kicker", 10: "Top Left Upkicker", 11: "Top Center Upkicker", 12: "Top Right Upkicker",
	13: "Lower Left Ball Gate", 14: "Left Pivot (Horus) Target", 15: "Right Pivot (Horus) Target", 16: "Top Pyramid",
	17: "3-Bank Drop Target Reset", 18: "2-Bank Drop Target Reset", 19: "Rollover Target Reset", 20: "Rollover Target Trip",
	22: "Rope Lights", 23: "Glider Motor (Left and Right)", 24: "Glider Motor (Forward)", 26: "Lightbox Relay (A)",
	27: "Ticket/Coin Meter", 28: "Ball Release", 29: "Outhole", 30: "Knocker", 31: "Tilt Relay (T)", 32: "Game Over Relay (Q)",
}
UNUSED_SOLENOIDS = frozenset({21, 25})
SOLENOID_KIND = {22: "lamp", 23: "motor", 24: "motor", 26: "relay", 31: "relay", 32: "relay"}
SOLENOID_CALLBACKS = {
	8: "SolLeftPlunge (line 747), which kicks the ball held at Kicker sw25 (lines 895-900)",
	9: "SolAutoFire (line 748), which fires the impulse plunger in the shooter lane (lines 1003-1010)",
	10: "LeftPop (line 749), which kicks the ball held at Trigger sw80 straight up (lines 991-999)",
	11: "BotPop (line 750), which kicks the ball held at Trigger sw23 straight up (lines 966-974)",
	12: "VukTopPop (line 751), which kicks the ball held at Trigger sw33 straight up (lines 941-949)",
	13: "SolDiv (line 752), which swings the ball gate Flipper1 and writes switch 101 (lines 782-792)",
	14: "SolPivL (line 753, 'Left Pivot Target'), which raises the left guardian out of the way and stops sw116 colliding while on (lines 1269-1283)",
	15: "SolPivR (line 754, 'Right Pivot Target'), which raises the right guardian and stops sw117 colliding while on (lines 1299-1313)",
	16: "SolPyramid (line 755, 'Pyramid Unit'), which opens the pyramid while on and reports it at 102 (lines 1329-1343)",
	17: "LeftDropUp (line 756), raising drop targets 17, 27 and 37 (lines 1551-1559)",
	18: "TopDropUp (line 757), raising drop targets 26 and 36 (lines 1561-1568)",
	19: "RightDropUp (line 758), raising drop target 35 (lines 1570-1576)",
	20: "RightDropTrip (line 759), dropping target 35 (lines 1578-1584)",
	22: "SolBGRopeLights (line 761, 'Rope Lights Backglass'), lighting the VR backglass tube BGTube",
	23: "SolGlid1 (line 762, 'Left and Right Glide Motor'), which swings the glider left and right while on (lines 1515-1518)",
	24: "SolGlid2 (line 763, 'Forward Glide motor'), which moves the glider out and back while on (lines 1520-1523)",
	26: "SolBBGI (line 765, 'BackBox GI used as PF GI'), whose two branches are commented out (lines 837-843)",
	28: "SolRelease (line 767), which kicks the ball from Kicker swTrough1 into the shooter lane (lines 887-893)",
	29: "SolTrough (line 768), which kicks the ball from Kicker Drain into the trough (lines 879-885)",
	30: "SolKnocker (line 769), a sound only",
	31: "GIState (line 770, 'Tilt Relay and PF GI'), which turns every light of its GI collection off while the relay is on (lines 815-824)",
}
SOLENOID_OBJECTS = {
	1: [("Bumper Bumper1", (177.58493, 1093.712))], 2: [("Bumper Bumper2", (112.81917, 884.93317))],
	3: [("Wall LeftSlingShot (drag-point mean)", (227.011128, 1509.372417))],
	4: [("Wall RightSlingShot (drag-point mean)", (640.506338, 1510.241483))],
	5: [("HitTarget sw14", (298.5, 855.87))], 6: [("HitTarget sw15", (356.86, 508.4))], 7: [("HitTarget sw16", (736.78, 1233.1))],
	8: [("Kicker sw25", (51.970787, 1883.4116))],
	9: [("Primitive BM_Autoplunger (world mesh centre)", (900.1113, 1933.9005))],
	10: [("Trigger sw80", (205.24, 121.04))], 11: [("Trigger sw23", (672.02, 91.73))], 12: [("Trigger sw33", (860.55, 92.35))],
	13: [("Flipper Flipper1 (ball gate)", BALL_GATE)],
	14: [("Primitive BM_GuardianL (world mesh centre)", (159.0688, 731.1572))],
	15: [("Primitive BM_GuardianR (world mesh centre)", (666.4908, 479.5917))],
	16: [("Primitive BM_Pyramid1 (world mesh centre)", PYRAMID)],
	17: [("Primitive BM_DT_sw27, the bank's middle target (world mesh centre)", (215.549, 1225.5177))],
	18: [("Primitive BM_DT_sw26 (world mesh centre)", (358.182, 939.484))],
	19: [("Primitive BM_DT_sw35 (world mesh centre)", (871.4435, 721.8806))],
	20: [("Primitive BM_DT_sw35 (world mesh centre)", (871.4435, 721.8806))],
	23: [("Primitive BM_Glider_1 (world mesh centre)", GLIDER)], 24: [("Primitive BM_Glider_1 (world mesh centre)", GLIDER)],
	28: [("Kicker swTrough1", (817.9233, 1810.345))], 29: [("Kicker Drain", (454.35745, 2028.6724))],
}
SOLENOID_PROJECTED = {
	5: "the kicking target it drives; the coil sits behind it and has no object of its own",
	6: "the kicking target it drives; the coil sits behind it and has no object of its own",
	7: "the kicking target it drives; the coil sits behind it and has no object of its own",
	8: "the kicker hole the script ejects from; the coil has no object of its own",
	10: "the upkicker the script lifts the ball from; the coil has no object of its own",
	11: "the upkicker the script lifts the ball from; the coil has no object of its own",
	12: "the upkicker the script lifts the ball from; the coil has no object of its own",
	13: "the ball gate it swings; the coil has no object of its own",
	14: "the left Horus guardian it raises; the coil sits below the playfield and has no object of its own",
	15: "the right Horus guardian it raises; the coil sits below the playfield and has no object of its own",
	16: "the pyramid top it opens; the drive has no object of its own",
	17: "the bank's middle drop target; the reset coil sits below the bank and has no object of its own",
	18: "the bank's first drop target; the reset coil sits below the bank and has no object of its own",
	19: "the single drop target it raises; the coil has no object of its own",
	20: "the single drop target it knocks down; the coil has no object of its own",
	23: "the glider it swings; the motor has no object of its own",
	24: "the glider it moves out and back; the motor has no object of its own",
	28: "the trough kicker the script releases balls from; the coil has no object of its own",
	29: "the outhole kicker the script receives drained balls on; the coil has no object of its own",
}
GAMEPLAY_GAPS = {
	2: "Three 100 ms pulses of its switch (11) during the gameplay run published nothing here. PinMAME smooths System 3 solenoids over four frames (GTS3_SOLSMOOTH), which can swallow a short coil pulse, so that is a possible explanation, not a proven one. The Relay & Solenoid Test fired it.",
	3: "Three 100 ms pulses of its switch (12) during the gameplay run published nothing here. PinMAME smooths System 3 solenoids over four frames (GTS3_SOLSMOOTH), which can swallow a short coil pulse, so that is a possible explanation, not a proven one. The Relay & Solenoid Test fired it.",
	10: "In the gameplay run it fired 1.24 s after switch 80 closed, just as the host's 1.2 s hold ended.",
	12: "In the gameplay run it stayed off while switch 33 was held at 1 for 1.2 s; the ROM had not yet served the game's first ball and had seen balls in three other kickers, and the run does not show why it held this one. The Relay & Solenoid Test fired it.",
}
# Outputs that sit in the backbox or cabinet, or drive no playfield device.
CABINET_SOLENOIDS = {22, 26, 27, 30, 31, 32}

# --- Lamps. ROM_LAMP_NAMES is the Lamp Matrix Test's name for each LAMP:nn (A0-B7 = 100-117) it blinked.
ROM_LAMP_NAMES = {
	0: "\"SHOOT AGAIN\"", 1: "CREDIT BUTTON", 5: "PYRAMID", 6: "\"DOUBLE\"", 7: "BRACELET",
	11: "\"SAVE\"", 12: "\"OPEN\"", 13: "\"OPEN\"", 14: "\"SPECIAL\"", 15: "PYRAMID", 16: "\"COMBO\"", 17: "TRANSPORTER",
	21: "\"QUARTZ\"", 22: "\"5M\"", 23: "\"10M\"", 24: "\"20M\"", 25: "PYRAMID", 26: "\"HURRY-UP\"", 27: "\"SARCOPHAGUS\"",
	32: "\"DOUBLE\"", 33: "\"40M\"", 34: "\"80M\"", 35: "PYRAMID", 36: "\"COMBO\"", 37: "\"SPELL STARGATE\"",
	41: "BOTTOM POP BUMPER", 42: "TOP POP BUMPER", 43: "\"EXTRA BALL\"", 44: "\"HORUS\" GUARD", 45: "PYRAMID",
	46: "\"BEGIN COMBO\"", 47: "\"LIGHT DOUBLE\"",
	55: "PYRAMID", 56: "\"COMBO\"", 57: "EYE OF RA (PYRAMID)",
	65: "PYRAMID", 66: "\"COMBO\"", 67: "\"QUARTZ TRADE\"",
	71: "EYE OF RA", 72: "\"GLIDERCRAFT\"", 73: "\"REBELLION\"", 74: "\"RA'S TEMPLE\"", 75: "\"QUARTZ\"", 76: "\"BATTLE\"",
	77: "\"SAVE SARI\"",
	81: "\"TRANSPORTER\"", 82: "\"HURRY-UP\"", 83: "\"PYRAMID\"", 84: "\"QUARTZ\"", 85: "\"SPELL STARGATE\"", 86: "\"COMBO\"",
	87: "\"SARCOPHAGUS\"",
	90: "LIGHTBOX #1", 91: "LIGHTBOX #2", 92: "LIGHTBOX #3", 100: "LIGHTBOX #4", 101: "LIGHTBOX #5", 102: "LIGHTBOX #6",
	110: "LIGHTBOX #7", 111: "LIGHTBOX #8", 112: "LIGHTBOX #9",
}
LAMP_ADDRESSES = MATRIX_ADDRESSES
LIGHTBOX_LAMPS = frozenset({90, 91, 92, 100, 101, 102, 110, 111, 112})
# Retained-table Light object per playfield lamp: VPW's L<n> light, which vpmMapLights binds by TimerInterval = n.
LAMP_LIGHTS = {
	0: (430.375, 1810.5538), 5: (540.56, 1441.91), 6: (588.17, 1385.38), 7: (636.85, 1325.36),
	11: (53.08, 1461.82), 12: (117.5, 1420.25), 13: (746.5, 1422.0), 14: (811.21, 1463.98), 15: (321.39, 1113.47),
	16: (295.31, 1050.76), 17: (263.53, 978.96),
	21: (402.72, 1415.0), 22: (316.5, 1411.5), 23: (351.0, 1361.0), 24: (406.0, 1332.5), 25: (700.14, 1024.37),
	26: (735.99, 959.59), 27: (779.32, 894.38),
	32: (528.36, 1073.48), 33: (455.5, 1044.75), 34: (480.5, 990.5), 35: (628.5, 963.38), 36: (660.65, 892.88), 37: (685.8, 818.88),
	41: (173.34, 1097.86), 42: (109.36, 876.4), 43: (74.24, 1133.46), 44: (182.85, 784.8), 45: (555.18, 891.74),
	46: (491.65, 849.63), 47: (431.36, 801.46),
	55: (432.51, 725.08), 56: (433.43, 650.87), 57: (430.9, 572.67),
	65: (611.24, 681.1), 66: (632.65, 605.27), 67: (654.87, 533.25),
	71: (533.0, 1231.31), 72: (526.92, 1168.55), 73: (475.0, 1209.31), 74: (485.31, 1272.41), 75: (548.52, 1294.33),
	76: (597.97, 1252.89), 77: (587.34, 1190.59),
	81: (350.39, 1556.2), 82: (327.91, 1645.82), 83: (387.15, 1717.82), 84: (478.0, 1717.98), 85: (535.11, 1646.73),
	86: (515.66, 1557.11), 87: (433.64, 1514.27),
}
# Lightbox lamps the retained table models in its VR backbox (Light L<n> at y = -76, above the playfield).
LIGHTBOX_MODELLED = frozenset({90, 92, 101, 110, 112})

# --- Auxiliary driver board (hw.lampCol = 5): lamps 120-127. Aux Driver Test names, driver n = lamp 120 + n.
ROM_AUX_NAMES = {
	120: "REBELLION -#67", 121: "TOP LEFT -#67", 122: "LEFT STARGATE -#67", 123: "RIGHT STARGATE -#67",
	124: "TOP RIGHT -#67", 125: "BOTTOM RIGHT -#67", 126: "RA'S EYES -#67 (LB)", 127: "WHITE RAILS -#67 (LB)",
}
AUX_LABELS = {
	120: "Rebellion Flasher", 121: "Top Left Flasher", 122: "Left Stargate Flasher", 123: "Right Stargate Flasher",
	124: "Top Right Flasher", 125: "Bottom Right Flasher", 126: "Ra's Eyes Flasher (Lightbox)", 127: "White Rails Flasher (Lightbox)",
}
AUX_LIGHTS = {
	120: (81.57, 995.18), 121: (350.19, 433.11), 122: (313.76, 177.68), 123: (617.72, 170.67), 124: (525.6, 418.89),
	125: (822.42, 1295.11),
}
# Playfield G.I.: every light of the retained GI collection, which GIState switches with relay 31.
GI_LIGHTS = (
	("GI_001", (680.33, 1706.39)), ("GI_002", (151.25, 1675.87)), ("GI_003", (666.83, 1552.53)), ("GI_004", (218.2, 1598.96)),
	("GI_006", (801.05, 1256.03)), ("GI_007", (142.39, 1239.23)), ("GI_008", (884.07, 908.48)), ("GI_009", (266.0, 769.08)),
	("GI_010", (65.61, 748.48)), ("GI_011", (159.84, 472.28)), ("GI_012", (836.47, 527.33)), ("GI_013", (583.87, 437.87)),
	("GI_014", (370.43, 361.45)), ("GI_015", (500.44, 361.55)), ("GI_016", (307.21, 448.37)), ("GI_017", (160.09, 341.56)),
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Stargate retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Stargate extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Stargate retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Stargate retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Stargate retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Stargate retained extraction file count mismatch: {len(actual['files'])} != {EXTRACTION_FILE_COUNT}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def placement(identifier: str, role: str, xy: tuple[float, float], status: str, *refs: str) -> dict[str, Any]:
	x, y = norm(*xy)
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, points: list[tuple[float, float]], status: str, *refs: str) -> dict[str, Any]:
	placements = [
		placement(f"{identifier}.{role}" + (f".{index}" if len(points) > 1 else ""), role, xy, status, *refs)
		for index, xy in enumerate(points, start=1)
	]
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def _excerpt(identifier: str, locator: str, filename: str, method: str, transcribed_by: str, reviewed: bool = True) -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": reviewed,
	}


def source_records() -> list[dict[str, Any]]:
	runtime_records = [
		{
			"id": runtime_source(game), "kind": "runtime_scenario", "uri": f"internal:{runtime_evidence_path(game).relative_to(ROOT).as_posix()}",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(runtime_evidence_path(game)),
			"locator": (
				f"Pinned LibPinMAME runs of {game}, each from a new state directory holding only that set's factory-settings "
				"NVRAM: the Lamp Matrix, Relay & Solenoid, Aux Driver and Switch Edges self-tests, each step paired with the "
				"public address it drove or the host held and with the text the DMD showed, read glyph by glyph by "
				"tools/gts3_dmd_text.py"
				+ (
					", plus the Front Door Test, a tournament and coin-door probe, one scripted game and a mechanism-sensor run"
					if game == PRIMARY_SET else
					", compared name by name with stargat5's"
				)
				+ ". Raw runs, DMD frames, NVRAM and the manifest are retained outside the repository."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes, NVRAM and DMD frames remain external",
		}
		for game in (PRIMARY_SET,) + VARIANT_SETS
	]
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog records for the six-driver stargat* clone tree rooted at stargate",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/gts3games.c lines 9 (DMD = GTS3_dispDMD), 16 (FLIP8182 = FLIP_SWNO(81,82)), 21-23 (GTS3_dispDMD, one "
				"32x128 CORE_DMD), 56-61 (INITGAME2: core_tGameData {GEN_GTS3, disptype, {flippers, 4, lamps, 0, sb, 0}} and "
				"GTS32_INPUT_PORTS_START) and 610-665 (the Stargate #742 block: INITGAME2(<set>, DMD, FLIP8182, 4, SNDBRD_GTS3, 5), "
				"the six ROM sets and CORE_GAMEDEFNV(stargate)/CORE_CLONEDEFNV(stargat1-5) on mGTS3DMDS); src/wpc/gts3.h "
				"GTS32_COMPORTS (coins 0-3, Start 4, Tournament 5 and Coin Door 6 toggles, flag 0x8000), GTS3_SWDIAG -8, "
				"GTS3_SWTILT -7, GTS3_SWSLAM -6, GTS3_SWPRIN -5 and GTS3_SOLSMOOTH 4; src/wpc/gts3.c xvia_0_a_r (the matrix "
				"returns read as ~core_getSwCol), dmd_u4_pb_r (test and tilt, not inverted), xvia_0_b_w (twelve-column lamp "
				"and switch strobe), xvia_1_b_w (hw.lampCol > 4: auxiliary board outputs into lampMatrix[12]), "
				"GTS3_interface_update (solenoid smoothing and core_updateSw with solenoid 32 as the flipper enable), "
				"SWITCH_UPDATE(GTS3), gts3_sw2m/gts3_m2sw, gts3dmd_init (nLamps = 64 + lampCol * 8, nGI = 0, outputs 26/31/32 "
				"typed as the A and T relays and Q game-on, and the stargate block typing 22 as an LED 'Rope Lights, circle of "
				"leds around Ra in backbox' and lamps 120-127 as 'Flashers from aux board'), solenoid_w, lds_w and "
				"MACHINE_DRIVER_START(gts3) MDRV_SWITCH_CONV/MDRV_LAMP_CONV; src/wpc/core.c core_updateSw (flipSwCol 15 for "
				"GEN_GTS3, the FLIP_SWNO copy and synthetic 45-48) and core_getAllSol; src/wpc/vpintf.c vp_getChangedLamps; "
				"src/wpc/gen.h GEN_GTS3 0x0020000000000"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/gts3.json", "revision": "repository",
			"locator": "Gottlieb System 3 decimal switch and lamp numbering, cabinet test inputs -8 to -5, the cabinet port on 0-6, the 140-147 flipper column, solenoids 1-32 and synthetic 45-48, and the auxiliary-board lamps 120-127",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2847",
			"revision": "Wayback capture 2025-04-24T12:35:42Z", "sha256": IPDB_PAGE_SHA256, "acquired_at": "2026-10-09T16:22:00Z",
			"locator": (
				"IPDB machine 2847 'Stargate' (Premier Technology, trade name Gottlieb, March 1995, model 742, Gottlieb System 3, "
				"3,600 units). IPDB is Cloudflare-gated, so the page was read from the raw Wayback capture "
				"https://web.archive.org/web/20250424123542id_/https://ipdb.org/machine.cgi?id=2847 (retained as "
				"manuals/by-machine/gottlieb.stargate.1995/ipdb/ipdb-2847-page-wayback.html); the live page, opened in a browser, "
				"lists the same English and Spanish manuals as 'Availability limited by copyright' without a link. The title, "
				"manufacturer, model number 742 (which the ROM's boot screen prints as Game #742/5) and the System 3 MPU match "
				"the machine being curated."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [
				_excerpt("excerpt.stargate.ipdb-page", "IPDB machine 2847 page, Wayback capture 2025-04-24", "ipdb-page.md", "manual", "curator, read from the retained HTML"),
			],
		},
		*runtime_records,
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/gottlieb/stargate-1995/v2.0/source/Stargate%20(Gottlieb%201995)%20v2.0.vpx",
			"original_filename": "Stargate (Gottlieb 1995) v2.0.vpx", "sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPX recreation of the physical machine by VPin Workshop (table version 2.0, saved "
				"2025-09-24, \"Table originally created by 32Assassin and JLouLoulou, Completely rebuilt by VPW\"), copied from "
				f"the contributor's table collection. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are "
				"x/952.941 and y/2164.706. Geometry authority for script-bound table objects."
			),
			"license": "NOASSERTION", "attribution": "VPin Workshop and the contributors credited in the table", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/gottlieb/stargate-1995/v2.0/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded script of the VPW v2.0 table; the pinned sverrewl/vpxtable_scripts corpus holds the same "
				"script as 'Stargate (Gottlieb 1995) v2.0.vbs' apart from whitespace and an appended Table1_exit sub. Runtime "
				"authority: cGameName = \"stargat5\" (line 60), UseSolenoids = 2 (line 75), LoadVPM GTS3.VBS (line 109), "
				"vpmMapLights AllLamps (line 228), the solenoid callbacks (lines 740-774, 1767-1769), the trough, kicker, target, "
				"glider and pyramid handlers and the tournament/free-play timer."
			),
			"license": "NOASSERTION", "attribution": "VPin Workshop and the contributors credited in the table", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.stargate.vpw-script-bindings", "script.vbs lines 60-3729, controller bindings", "vpw-script-bindings.md", "manual", "curator, read from the extracted script"),
			],
		},
		{
			"id": MORTTIS_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/gottlieb/stargate-1995/morttis-led-v1.3.0/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": MORTTIS_SCRIPT_SHA256,
			"locator": (
				"Embedded script of the retained 'Stargate ( Gottlieb 1995 ) - v.1.3.0 - Led Lights - rev.1.1 [D&N][CC][FSS]"
				f"[DMD][10.6+][Morttis].vpx' (table SHA-256 {MORTTIS_TABLE_SHA256}), the 32Assassin and JLouLoulou release the VPW "
				"table was rebuilt from, so it corroborates rather than independently confirms. Used for its switch writers, "
				"which pulse the Horus targets as 116 and 117 (lines 970 and 988)."
			),
			"license": "NOASSERTION", "attribution": "32Assassin, JLouLoulou and the contributors credited in the script", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.stargate.morttis-script-bindings", "script.vbs lines 32-988, controller bindings", "morttis-script-bindings.md", "manual", "curator, read from the extracted script"),
			],
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "gts3.vbs", "sha256": VPM_GTS3_SHA256,
			"locator": (
				"The VPinMAME script library both retained tables load (LoadVPM ..., \"GTS3.VBS\", ...), retained with core.vbs "
				f"(SHA-256 {VPM_CORE_SHA256}). GTS3.VBS defines swLRFlip = 141 and swLLFlip = 143 and writes them from the flipper "
				"keys in vpmKeyDown/vpmKeyUp, which the tables' key handlers call."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.stargate.vpm-script-library", "gts3.vbs lines 21-123", "vpm-script-library.md", "manual", "curator, read from the library file"),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/gottlieb/stargate-1995/v2.0/extracted-vpxtool.manifest.json",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": (
				f"Retained vpxtool git:v0.33.3 extraction of the VPW v2.0 table, {EXTRACTION_FILE_COUNT} files, with a full sorted "
				f"path/size/SHA-256 manifest whose own SHA-256 is this record's sha256. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": VPX_OBJ_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/gottlieb/stargate-1995/v2.0/export-obj-vpu/Stargate%20(Gottlieb%201995)%20v2.0.obj",
			"sha256": OBJ_EXPORT_SHA256,
			"locator": (
				"vpxtool git:v0.33.3 `export obj --units vpu` of the VPW v2.0 table, the world-space mesh of every object (OBJ x "
				"is playfield x, OBJ y is playfield y). Used only for baked-mesh primitives whose stored position is a local "
				"origin: the drop targets BM_DT_sw17/26/27/35/36/37, the Horus guardians BM_GuardianL/R, the pyramid top "
				"BM_Pyramid1, the glider BM_Glider_1 and the auto-plunger arm BM_Autoplunger, each placed at its world "
				"bounding-box centre. Control: the same export's BM_KT_sw14 kicking target centre (298.4, 856.2) lies within "
				"1.4 units of HitTarget sw14's stored position (298.5, 855.9)."
			),
			"license": "NOASSERTION", "attribution": "vpxtool export of the retained table",
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
	" Stargate's game data sets no inverted-switch mask and gts3.c's xvia_0_a_r hands the CPU the complement of the "
	"matrix column, so public 1 is the closed contact the CPU sees: the matrix contact rests open and closes when the "
	"device is actuated."
)
EDGES_NOTE = " The ROM's Switch Edges Test names it \"{name}\" while the host holds public {address} at 1 (run switch-edges)."


def _switch_spatial(address: int) -> dict[str, Any]:
	if address in SWITCH_OBJECTS:
		_, xy = SWITCH_OBJECTS[address]
		refs = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
		if "world mesh centre" in SWITCH_OBJECTS[address][0]:
			refs += (VPX_OBJ_SOURCE,)
		return located(f"switch.matrix-{address}", "sensor", [xy], "observed", *refs)
	xy, _ = SWITCH_PROJECTIONS[address]
	refs = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
	if xy in (GLIDER, PYRAMID):
		refs += (VPX_OBJ_SOURCE,)
	return located(f"switch.matrix-{address}", "sensor", [xy], "observed", *refs)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	cabinet = {
		-8: ("Test (Diagnostic) Button", "service.test", "button", (
			"GTS3_SWDIAG on the cabinet port (internal column 0), read through dmd_u4_pb_r on VIA U4 PB3 without inversion. "
			"Every retained run enters and steps the self-tests with it: two presses at 1 bring up TEST MODE and the menu, and "
			"each further press steps to the next self-test (runs lamp-matrix, solenoids, aux-drivers, switch-edges, front-door)."
		), (RUNTIME_SOURCE,)),
		-7: ("Tilt", "cabinet.tilt", "tilt", (
			"GTS3_SWTILT on the cabinet port, read through dmd_u4_pb_r on VIA U4 PB4 without inversion. Held at 1 inside the "
			"Switch Edges Test it replaced the test screen with TILT (run switch-edges), so the ROM reads it active at 1. "
			"GTS3.VBS names it swTilt = -7."
		), (RUNTIME_SOURCE, VPM_LIBRARY_SOURCE)),
		-6: ("Slam Tilt", "cabinet.slam-tilt", "tilt", (
			"GTS3_SWSLAM on the cabinet port, read through VIA U4 CA1 on the DMD generation. A pulse at 1 inside the Front "
			"Door Test reset the game to attract mode (GAME OVER, run front-door), so the ROM reads it active at 1. GTS3.VBS "
			"names it swSlamTilt = -6."
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
				"communications adapter (printer) on the CPU board's auxiliary connector: at 1 the status reads ready, at 0 "
				"not connected. It is not a matrix switch, and held at 1 inside the Switch Edges Test it changed nothing on "
				"the display (run switch-edges). A recreation without the adapter leaves it at 0."
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
					f"Strobe {column}, return {row}." + EDGES_NOTE.format(name="(NOT USED)", address=address)
					+ " The ROM scans the position and calls it unused; neither retained table writes it."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		label = SWITCH_LABELS[address]
		notes = f"Strobe {column}, return {row}."
		if address in ROM_SWITCH_NAMES:
			if address in (81, 82):
				notes += (
					f" The ROM's Switch Edges Test names it \"{ROM_SWITCH_NAMES[address]}\" while the host holds the flipper button "
					f"{143 if address == 81 else 141} at 1 (run switch-edges)."
				)
			else:
				notes += EDGES_NOTE.format(name=ROM_SWITCH_NAMES[address], address=address)
		refs: tuple[str, ...] = core + (RUNTIME_SOURCE,)
		physical: dict[str, Any] = {}
		extra: dict[str, Any] = {}
		if address in ROM_ACTIVE_AT_1:
			notes += f" Polarity: {ROM_ACTIVE_AT_1[address]}." + READ_PATH_NOTE
		elif address in SCRIPT_ACTIVE_AT_1:
			who = "the retained tables treat it" if address in (116, 117) else "the known-working script treats it"
			notes += f" Polarity: {who} as actuated at 1 ({SCRIPT_ACTIVE_AT_1[address]})." + READ_PATH_NOTE
			refs += (VPX_SCRIPT_SOURCE,) if address not in (116, 117) else (MORTTIS_SCRIPT_SOURCE,)
		if address in OPTO_SWITCHES:
			physical["switch_type"] = "opto"
			notes += " The ROM's own name marks it as an opto; the matrix contact rests open by the read-path rule above, whatever the beam does."
		if address in CABINET_SWITCH_TYPES:
			physical["switch_type"] = CABINET_SWITCH_TYPES[address]
		if address == 4:
			notes += (
				" The Switch Edges Test shows nothing for it: Start is one of the test's own controls. Lamp 1 is the button's "
				"lamp, which the Lamp Matrix Test names CREDIT BUTTON. GTS32_COMPORTS calls it START1, and GTS3.VBS writes it "
				"from the start key (swStartButtonX = 4)."
			)
		if address == 5:
			notes += (
				" It is a service button inside the coin door. The VPW table holds it at 1 from three seconds after start, "
				"together with 6, under its banner 'JLouLou SYS3 Freeplay & Tournament MOD' (lines 127-129 and 3726-3729), and "
				"also writes it from the right magna-save key (lines 673 and 707); that is a table customization, not the "
				"machine's rest state. The retained v1.3.0 script leaves its toggle commented out (line 773)."
			)
			refs += (VPX_SCRIPT_SOURCE, MORTTIS_SCRIPT_SOURCE)
		if address == 6:
			notes += (
				" It reads 1 while the coin door is shut, like the WPC Coin Door Closed switch: the contact is closed by the "
				"closed door and open while the door is open, and the game plays with it at either level (run gameplay was "
				"started with it at 0). The VPW table holds it at 1 from three seconds after start (lines 3726-3729) and the "
				"v1.3.0 table toggles it from the End key (line 774)."
			)
			refs += (VPX_SCRIPT_SOURCE, MORTTIS_SCRIPT_SOURCE)
		if address in (0, 1, 2, 3):
			notes += (
				f" The Front Door Test counts it as coin chute {address + 1}. GTS3.VBS names it swCoin{address + 1} = {address:02d}, "
				"and GTS32_COMPORTS rewrites it from a coin key only with PinMAME keyboard handling on."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		if address in (81, 82):
			button = 143 if address == 81 else 141
			notes += (
				f" The driver declares FLIP_SWNO(81,82) with no FLIP_SOL, so core_updateSw copies the {'left' if address == 81 else 'right'} "
				f"flipper button from PinMAME's flipper column (public {button}) into this switch on every update; it cannot be "
				f"driven directly, because a host write here is overwritten on the next update. Drive {button}. Both retained "
				f"scripts also write {address} from the flipper key before calling vpmKeyDown/vpmKeyUp, which writes {button} "
				"(VPW lines 653-661 and 688-697; v1.3.0 lines 771-782): a defect with no effect, since the copy overwrites it."
			)
			refs += (VPX_SCRIPT_SOURCE, MORTTIS_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE)
		if address in (116, 117):
			notes += (
				f" The VPW table binds this Horus target through its StandupTarget class (line {2946 if address == 116 else 2947}), "
				f"whose STAnimate pulses 'switch mod 100' (line 3033), so a hit pulses {address - 100} instead of {address}: a "
				f"defect in that table. The retained v1.3.0 script pulses {address} itself."
			)
		if address in (22, 32):
			notes += (
				" The bullseye target has two contacts at one spot: 22 (inner) and 32 (outer); both retained tables place them "
				"on one target."
			)
		if address == 34:
			notes += (
				" The machine holds four balls: the trough plus one resting in the outhole (24). The VPW table creates three "
				"balls in its trough kickers and one in the drain at start and writes 34 from the trough position nearest the "
				"drain (lines 261-266 and 856-861); the v1.3.0 table models one four-ball stack whose positions 1-4 all report "
				"34 (line 562)."
			)
			refs += (VPX_SCRIPT_SOURCE, MORTTIS_SCRIPT_SOURCE)
		if address == 20:
			notes += (
				" Polarity unknown: neither retained table writes it and no retained run exercised it, so no source shows which "
				"level the ROM treats as actuated; the Switch Edges Test proves only that the ROM scans it."
			)
		physical["notes"] = notes
		if address in CABINET_SWITCH_ROLES:
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			physical["location"] = "coin door and cabinet" if address in (0, 1, 2, 3, 4, 5, 6) else "matrix copy of the cabinet flipper button"
			spatial = not_applicable("cabinet_or_service", *core)
		else:
			spatial = _switch_spatial(address)
			placement_note = (
				f" Placed at the retained table's {SWITCH_OBJECTS[address][0]}, which the script binds to this address."
				if address in SWITCH_OBJECTS else f" {SWITCH_PROJECTIONS[address][1]}"
			)
			physical["notes"] += placement_note
		if address not in POLARITY_UNKNOWN:
			extra["normally_closed"] = False
		items.append(_device(
			identifier, label, "switch", "pinmame.input.switch", address, "used", refs,
			physical=physical, spatial=spatial, **extra,
		))
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
				f"{base} This is the {position.lower()} cabinet flipper button as the ROM receives it. The driver declares "
				"FLIP_SWNO(81,82) with no FLIP_SOL, so with keyboard handling off (the LibPinMAME default) core_updateSw reads "
				f"this bit as the host wrote it, copies it into matrix switch {matrix[side]} on every update and fabricates the "
				f"synthetic {'45/46' if side == 'right' else '47/48'} flipper outputs from it while the game-over relay (32) is "
				f"energized. Drive this address, not {matrix[side]}. In the self-tests it is the menu's "
				f"{'select' if side == 'right' else 'step'} control (TEST MODE screen: L FLIPPER TO STEP, R FLIPPER TO SELECT); "
				+ ("every retained self-test run pressed it there (runs nvram-init, lamp-matrix, solenoids, aux-drivers, "
				"switch-edges, front-door)" if side == "right" else "the nvram-init run pressed it there to reach GAME ADJUSTMENTS")
				+ f". In the gameplay run a press with the game-over relay on raised {'45 and 46' if side == 'right' else '47 and 48'}. GTS3.VBS names "
				f"it swL{'R' if side == 'right' else 'L'}Flip = {address} and writes it from the flipper key in "
				"vpmKeyDown/vpmKeyUp, which both retained tables call."
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
				"locals.flipMask carries this end-of-stroke bit only when hw.flippers sets FLIP_EOS, and FLIP_SWNO(81,82) does "
				"not, so core_updateSw neither synthesizes it nor copies it anywhere: PinMAME models no end-of-stroke switch on "
				"this machine."
			)
		else:
			reason = (
				"core_updateSw copies only the two lower button bits into the matrix and the synthetic outputs; this upper-button "
				"bit would join locals.flipMask only if hw.flippers set the matching upper FLIP_SW bit, which FLIP_SWNO(81,82) "
				"does not."
			)
		reason += (
			" A host write survives in the column, but the ROM cannot read it there: xvia_0_a_r reads the matrix only through "
			"core_getSwCol with the twelve-bit lamp/switch strobe, which reaches internal columns 1-12."
		)
		if address in (145, 147):
			reason += (
				f" GTS3.VBS names it sw{'UR' if address == 145 else 'UL'}Flip = {address} and writes it from a staged flipper key "
				f"while vpmFlips.FlipperSolNumber({'3' if address == 145 else '2'}) is non-zero; the write reaches nothing the ROM reads."
			)
		items.append({
			"id": f"switch.flipper-column-{address}",
			"label": f"Unused Flipper Column {position} {'End-of-Stroke' if kind == 'eos' else 'Button'} ({address})",
			"kind": "switch",
			"binding": {"group": "pinmame.input.switch", "device": address},
			"availability": "unused",
			"provenance": provenance(*core, *((VPM_LIBRARY_SOURCE,) if address in (145, 147) else ())),
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
			"physical": {"location": "internal public address space", "switch_type": "other", "notes": f"{base} {reason}"},
			"spatial": not_applicable("unused", *core),
		})
	return items


SOLENOID_RUNTIME = {
	1: "fired when bottom pop bumper switch 10 was pulsed during a game (run gameplay)",
	4: "fired twice when right kicking rubber switch 13 was pulsed three times during a game (run gameplay)",
	5: "fired twice when kicking target switch 14 was pulsed three times during a game (run gameplay)",
	6: "fired once when kicking target switch 15 was pulsed three times during a game (run gameplay)",
	7: "fired twice when kicking target switch 16 was pulsed three times during a game (run gameplay)",
	8: "fired once, 1.0 s after switch 25 closed and after the ball gate (13) opened (run gameplay)",
	11: "fired twice while switch 23 was held at 1 for 1.2 s (run gameplay)",
	13: "opened about 0.5 s after switch 25 closed, before the kicker (8) fired, and closed again about 0.5 s after it (run gameplay)",
	17: "fired, with 18, the rollover-target trip (20) and the ball release (28), when the ROM served a ball after the second outhole kick (run gameplay)",
	18: "fired, with 17, 20 and 28, when the ROM served a ball after the second outhole kick (run gameplay)",
	20: "fired at game start and again when the ROM served a ball after the second outhole kick (run gameplay)",
	28: "fired about 2.6 s after the trough switch 34 rose following the second outhole kick (run gameplay)",
	29: "fired repeatedly while the outhole switch 24 was held at 1 (run gameplay)",
	32: "rose at game start and again when the next ball was served (run gameplay)",
}


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in range(1, 33):
		driver = address - 1
		name = ROM_COIL_NAMES[address]
		notes = (
			f"The Relay & Solenoid Test names driver {driver} \"{name}\", and the credit button fired public {address} there "
			"(run solenoids; the displayed driver number is the public address minus one)."
		)
		refs = core + (RUNTIME_SOURCE,)
		if address in UNUSED_SOLENOIDS:
			notes += (
				" The ROM's own test table calls the driver NOT USED, and both retained scripts leave its callback commented "
				"'Not Used' (VPW line {line}, v1.3.0 line {mline}). The test sweep fires it; no gameplay run published it."
			).format(line=760 if address == 21 else 764, mline=345 if address == 21 else 351)
			items.append(_device(
				f"device.not-used-{address}", f"Not Used (Driver {driver})", "coil", "pinmame.output.solenoid", address, "unused",
				refs + (VPX_SCRIPT_SOURCE, MORTTIS_SCRIPT_SOURCE),
				physical={"notes": notes}, spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		if address in SOLENOID_RUNTIME:
			notes += f" In play it {SOLENOID_RUNTIME[address]}."
		if address in SOLENOID_CALLBACKS:
			notes += f" The VPW script binds SolCallback({address}) to {SOLENOID_CALLBACKS[address]}."
			refs += (VPX_SCRIPT_SOURCE,)
		if address in (1, 2, 3, 4, 5, 6, 7):
			notes += (
				" The CPU fires it from its switch: the ROM, not a separate special-solenoid circuit, closes the loop, so a "
				"consumer only drives the switch. Both retained tables leave the callback commented out and kick the ball "
				"with the table's own bumper, slingshot or kicking-target physics (VPW lines 740-746)."
			)
			refs += (VPX_SCRIPT_SOURCE,)
		if address in GAMEPLAY_GAPS:
			notes += " " + GAMEPLAY_GAPS[address]
		if address == 9:
			notes += (
				" The shooter lane is fed by the ball release (28) and has a plunger; this kicker is its auto-launch: the VPW "
				"script fires its impulse plunger on it."
			)
		if address == 22:
			notes += (
				" PinMAME's stargate output block types it as an LED output: 'Rope Lights', the circle of LEDs around Ra in the "
				"backbox. The ROM's name carries (18)."
			)
		if address in (23, 24):
			notes += (
				" In the Relay & Solenoid Test the ROM energized the pyramid (16) about 0.2-0.3 s before this motor and released it "
				"about 0.25 s after (run solenoids): the Glidercraft extends from the pyramid when it is open (IPDB)."
			)
			refs += (IDENTITY_SOURCE,)
		if address == 26:
			notes += (
				" PinMAME's System 3 init types it as the 'A' relay: lightbox insert (backbox) illumination. The VPW comment calls "
				"it 'BackBox GI used as PF GI' but its handler does nothing."
			)
		if address == 27:
			notes += (
				" An optional cabinet accessory output: neither retained table binds it (VPW line 766 'Ticket dispenser', "
				"commented out), and no gameplay run published it."
			)
			refs += (VPX_SCRIPT_SOURCE,)
		if address == 31:
			notes += (
				" PinMAME's System 3 init types it as the 'T' relay, general illumination. The ROM calls it the tilt relay: it "
				"switches the playfield G.I. off when energized, which the VPW script reproduces."
			)
		if address == 32:
			notes += (
				" PinMAME's System 3 init types it as the 'Q' relay, game on, and passes its state to core_updateSw as the "
				"flipper enable: the synthetic flipper outputs 45-48 follow the buttons only while it is on. GTS3.VBS names it "
				"GameOnSolenoid = 32."
			)
			refs += (VPM_LIBRARY_SOURCE,)
		kind = SOLENOID_KIND.get(address, "coil")
		availability = "optional" if address == 27 else "used"
		physical: dict[str, Any] = {"notes": notes}
		if address in CABINET_SOLENOIDS:
			spatial = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
			physical["location"] = "backbox" if address in (22, 26) else "cabinet"
		else:
			placements = SOLENOID_OBJECTS[address]
			obj_refs: tuple[str, ...] = (VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
			if any("world mesh centre" in label for label, _ in placements):
				obj_refs += (VPX_OBJ_SOURCE,)
			role = "effect"
			spatial = located(f"device.{slug(SOLENOID_LABELS[address])}", role, [xy for _, xy in placements], "observed", *obj_refs)
			placed = ", ".join(label for label, _ in placements)
			physical["notes"] += (
				f" Projected onto {SOLENOID_PROJECTED[address]} ({placed})." if address in SOLENOID_PROJECTED
				else f" Placed at the retained table's {placed}."
			)
		items.append(_device(
			f"device.{slug(SOLENOID_LABELS[address])}", SOLENOID_LABELS[address], kind, "pinmame.output.solenoid", address,
			availability, refs, physical=physical, spatial=spatial,
		))
	synthetic = {
		45: ("Synthetic Lower Right Flipper Power", 141), 46: ("Synthetic Lower Right Flipper Hold", 141),
		47: ("Synthetic Lower Left Flipper Power", 143), 48: ("Synthetic Lower Left Flipper Hold", 143),
	}
	for address, (label, button) in synthetic.items():
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, "used", core + (RUNTIME_SOURCE,),
			roles=["internal.synthetic-flipper"],
			physical={"notes": (
				f"PinMAME fabricates it from the flipper button at public {button} (core_updateSw, CORE_FIRSTLFLIPSOL = 45) while "
				"the game-over relay 32 is energized, and core_getAllSol publishes the power and hold outputs of a pair together. "
				f"Stargate's flippers are cabinet-wired (FLIP_SWNO(81,82), no FLIP_SOL), so no CPU driver stands behind it. In "
				f"the gameplay run, with 32 energized, a press of {button} raised the pair for the press"
				+ (", and so did each press in the Relay & Solenoid Test, which energizes 32; the other self-tests leave 32 off "
				"and the presses there raised nothing." if button == 141 else "; the self-tests that pressed it leave 32 off and "
				"raised nothing.")
			)},
			spatial=not_applicable("virtual", *core),
		))
	return items


def _lamp_label(address: int) -> str:
	name = ROM_LAMP_NAMES[address].replace('"', "")
	words = " ".join(word.capitalize() if not re.fullmatch(r"\d+M", word) else word for word in name.split())
	duplicates = [other for other, value in ROM_LAMP_NAMES.items() if value.replace('"', "") == name]
	return f"{words} (Lamp {address})" if len(duplicates) > 1 else words


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	core = (CORE_SOURCE, CONTROLLER_SOURCE)
	for address in LAMP_ADDRESSES:
		column, row = divmod(address, 10)
		shown = f"{address:02d}" if address < 100 else ("A" if address < 110 else "B") + str(address % 10)
		identifier = f"lamp.matrix-{address}"
		if address not in ROM_LAMP_NAMES:
			items.append(_device(
				identifier, f"Not Used (Lamp {address})", "lamp", "pinmame.output.lamp", address, "unused", core + (RUNTIME_SOURCE,),
				physical={"notes": (
					f"Strobe {column}, row {row}. The Lamp Matrix Test steps through LAMP:{shown} and names it (NOT USED); "
					"neither retained table binds it."
				)},
				spatial=not_applicable("unused", CORE_SOURCE, RUNTIME_SOURCE),
			))
			continue
		name = ROM_LAMP_NAMES[address]
		notes = (
			f"Strobe {column}, row {row}. In the Lamp Matrix Test LAMP:{shown} blinks this public address while the display "
			f"names it {name} (run lamp-matrix); a quoted name is the insert's printed text."
		)
		refs = core + (RUNTIME_SOURCE,)
		physical: dict[str, Any] = {}
		if address == 1:
			notes += " The lamp in the cabinet's credit (Start) button."
			physical["location"] = "cabinet"
			spatial = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
		elif address in LIGHTBOX_LAMPS:
			notes += (
				" One of nine lightbox lamps behind the backglass. "
				+ (
					"The VPW table models it as Light L{0} in its VR backbox, above the playfield, which vpmMapLights binds through "
					"the AllLamps collection.".format(address)
					if address in LIGHTBOX_MODELLED else "Neither retained table models it."
				)
			)
			physical["location"] = "backbox"
			spatial = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
			if address in LIGHTBOX_MODELLED:
				refs += (VPX_SCRIPT_SOURCE,)
		else:
			notes += (
				f" Placed at the retained table's Light L{address}, which vpmMapLights binds to this address through its "
				"TimerInterval in the AllLamps collection (script line 228); the table's insert lights are invisible bulb "
				"lights under the playfield art."
			)
			refs += (VPX_SCRIPT_SOURCE,)
			spatial = located(identifier, "emitter", [LAMP_LIGHTS[address]], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
		physical["notes"] = notes
		items.append(_device(identifier, _lamp_label(address), "lamp", "pinmame.output.lamp", address, "used", refs, physical=physical, spatial=spatial))
	for address in range(120, 128):
		name = ROM_AUX_NAMES[address]
		notes = (
			f"Auxiliary driver board output {address - 120}: Stargate declares hw.lampCol = 5, so gts3.c's xvia_1_b_w writes VIA "
			f"U5 port B into lampMatrix[12], published at 120-127, and PinMAME's stargate block calls them 'Flashers from aux "
			f"board' and models their brightness as #89 bulbs, where the ROM's names give #67. The Aux Driver Test names driver {address - 120} \"{name}\" and the credit button blinked "
			f"public {address} there (run aux-drivers); the Lamp Check self-test flashes 120-127 with the lamps."
		)
		refs = core + (RUNTIME_SOURCE,)
		physical = {"notes": notes}
		if address in AUX_LIGHTS:
			notes_extra = (
				f" Placed at the retained table's Light L{address}, which vpmMapLights binds to this address (script line 228)."
			)
			physical["notes"] += notes_extra
			refs += (VPX_SCRIPT_SOURCE,)
			spatial = located(f"lamp.aux-{address}", "emitter", [AUX_LIGHTS[address]], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			physical["notes"] += " The ROM's name marks it (LB), lightbox: it lights the backglass, not the playfield."
			physical["location"] = "backbox"
			spatial = not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE)
		items.append(_device(f"lamp.aux-{address}", AUX_LABELS[address], "flasher", "pinmame.output.lamp", address, "used", refs, physical=physical, spatial=spatial))
	return items


def gi_spatial_note() -> str:
	return ", ".join(name for name, _ in GI_LIGHTS)


def displays() -> list[dict[str, Any]]:
	return [{
		"id": "display.dmd", "label": "128x32 dot-matrix display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32,
		"physical_location": "cabinet_or_service",
		"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, RUNTIME_SOURCE),
		"provenance": provenance(CORE_SOURCE, RUNTIME_SOURCE),
	}]


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

	m = (RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole, trough, ball release and shooter lane", "kicker", [coil(29), coil(28), coil(9)],
			[switch(24), switch(34), switch(31)],
			"The machine holds four balls (the boot screen reads Install 4 Balls). A drained ball rests on the outhole switch "
			"(24) and the Outhole coil (29) kicks it into the trough, whose switch (34, TROUGH) the ROM watches before it serves "
			"a ball; the Ball Release coil (28) then kicks the lead ball into the shooter lane, where the Shooter Lane Rollover "
			"(31) sees it, and the player plunges it. The Shooter Lane Kicker (9) is the lane's auto-launch. At rest one ball sits "
			"in the outhole: the VPW table starts with three balls in its trough and one on the drain, with 24 and 34 at 1 "
			"(lines 261-266). In the gameplay run, started with 34 closed and 24 open, the ROM kicked the outhole three times "
			"about 0.7 s apart while the host held 24 closed for 2 s, then showed WARNING! Ball missing or stuck / Place 1 ball in "
			"outhole and did not serve while 34 was held for 6 s; after a second ball reached the outhole it reset the drop "
			"targets (17, 18) and tripped the rollover target (20) about 1.4 s after 34 rose and fired the Ball Release (28) "
			"about 2.6 s after it.",
			*m,
		),
		mechanism(
			"mechanism.pyramid", "Top pyramid and Glidercraft", "motorized", [coil(16), coil(23), coil(24)],
			[switch(102), switch(91), switch(21), switch(30), switch(20)],
			"The pyramid at the top of the playfield is the main toy (IPDB). Its top opens by raising and lowering under the "
			"TOP PYRAMID output (16), which the ROM holds on while the pyramid is open; the TOP PYRAMID -SENSOR (102) reports the "
			"top's position (the VPW table writes it 1 half a second after 16 turns on and 0 half a second after it turns off), "
			"and the TOP PYRAMID -OPTO (91) sees a ball enter the pyramid, which the tables pass into a subway (VPW line 1256). "
			"The Glidercraft extends from the open pyramid and zig-zags left and right in front of it with about 90 degrees of "
			"travel (IPDB). Two motors drive it: GLIDER MOTOR -FORWARD (24) moves it out and back, GLIDER MOTOR (L & R) (23) "
			"swings it. The ROM names three glider switches: GLIDER MOTOR STOP (21), GLIDER RIGHT (MOTOR) (30) and GLIDER LEFT "
			"(MOTOR) (20). The VPW table closes 21 while the glider is fully retracted and 30 at the right end of the swing "
			"(lines 1406-1416) and never writes 20, and it plays; neither table models 20. When the ROM's Relay & Solenoid Test "
			"fires either glider motor it energizes the pyramid (16) about 0.2-0.3 s first and releases it about 0.25 s after "
			"the motor stops (run solenoids), and in attract mode it ran 16 and 23 together for about 7 s (run "
			"mechanism-sensors). Holding 102, 21, 20 or 30 at 1 in attract mode drew no response.",
			*m, IDENTITY_SOURCE,
		),
		mechanism(
			"mechanism.horus-guardians", "Left and right Horus pivot targets", "toy", [coil(14), coil(15)], [switch(116), switch(117)],
			"Two large Horus guardians on pivots block two key shots. Each carries a target (116 left, 117 right) that rises "
			"into the air with its guardian, the reverse of a drop target; the game occasionally raises them to open the shots "
			"(IPDB). The LEFT and RIGHT PIVOT TARGET outputs (14, 15) are held on while a guardian is raised: the VPW script "
			"lifts the guardian out of the shot and stops its target colliding while the output is on (lines 1269-1313), and "
			"the v1.3.0 script drops the target object while it is on (line 974). In the gameplay run the ROM raised and lowered "
			"both together, roughly every two seconds, from the start of the game.",
			*m, MORTTIS_SCRIPT_SOURCE, IDENTITY_SOURCE,
		),
		mechanism(
			"mechanism.left-drop-bank", "Left 3-bank drop targets", "drop_target_bank", [coil(17)], [switch(17), switch(27), switch(37)],
			"Three drop targets on the left, LEFT DROP TARGET #1-#3 (17, 27, 37), reset together by the 3-BANK DROP TAR RESET "
			"coil (17). When the ROM served a ball it reset the bank (run gameplay). Holding all three down for six seconds in "
			"the same run drew no reset, but the game's first ball had not been served yet, so that run does not show when "
			"the ROM resets a completed bank during play.",
			*m,
		),
		mechanism(
			"mechanism.center-drop-bank", "Center 2-bank drop targets", "drop_target_bank", [coil(18)], [switch(26), switch(36)],
			"Two drop targets in the centre, CENTER DROP TARGET #1 and #2 (26, 36), reset together by the 2-BANK DROP TAR RESET "
			"coil (18). When the ROM served a ball it reset them (run gameplay); holding both down for six seconds before the "
			"game's first ball had been served drew no reset.",
			*m,
		),
		mechanism(
			"mechanism.rollover-drop-target", "Right rollover drop target", "drop_target_bank", [coil(19), coil(20)], [switch(35)],
			"A single drop target on the right, the ROLLOVER DROP TARGET (35), with its own reset coil (19, ROLLOVER TARGET RESET) "
			"and a trip coil (20, ROLLOVER TARGET TRIP) that knocks it down so the ball can roll over it. The ROM fired the trip "
			"at game start and again when it served a ball (run gameplay); the VPW script raises the target on 19 and drops it "
			"on 20 (lines 1570-1584).",
			*m,
		),
		mechanism(
			"mechanism.upkickers", "Top left, centre and right upkickers", "kicker", [coil(10), coil(11), coil(12)],
			[switch(80), switch(23), switch(33)],
			"Three vertical up-kickers at the top of the playfield: TOP LEFT (switch 80, an opto by the ROM's name; coil 10), TOP "
			"CENTER (switch 23; coil 11) and TOP RIGHT (switch 33; coil 12). In the gameplay run, each switch held for 1.2 s, the "
			"ROM fired 11 twice for 23 and 10 once for 80, and left 33 unkicked while the game's first ball was still unserved. "
			"The tables lift the ball straight up out of the hole (VPW lines 941-999).",
			*m,
		),
		mechanism(
			"mechanism.lower-left-kicker-and-gate", "Lower left kicker and ball gate", "kicker", [coil(8), coil(13)],
			[switch(25), switch(101)],
			"A kicker hole at the lower left (switch 25) ejects the ball with the LOWER LEFT KICKER coil (8), and the LOWER LEFT "
			"BALL GATE (13) swings a gate whose position the BALL GATE -SENSOR (101) reports. With 25 held closed the ROM opened "
			"the gate (13) about 0.5 s later, fired the kicker (8) about 0.5 s after that, and closed the gate again (run "
			"gameplay). The VPW script swings its gate flipper Flipper1 and writes "
			"101 from the gate coil's state (lines 782-792).",
			*m,
		),
		mechanism(
			"mechanism.cpu-fired-coils", "Pop bumpers, kicking rubbers and kicking targets", "other",
			[coil(1), coil(2), coil(3), coil(4), coil(5), coil(6), coil(7)],
			[switch(10), switch(11), switch(12), switch(13), switch(14), switch(15), switch(16)],
			"Two pop bumpers (switches 10 bottom and 11 top, coils 1 and 2), two kicking rubbers (slingshots; switches 12 and "
			"13, coils 3 and 4) and three kicking targets (switches 14, 15 and 16, coils 5, 6 and 7): stand-up targets that kick "
			"the ball back. System 3 has no special-solenoid circuit: the CPU reads each switch and fires its coil (in the "
			"gameplay run pulses of 10, 13, 14, 15 and 16 fired 1, 4, 5, 6 and 7; 2 and 3 were not observed, which PinMAME's "
			"four-frame solenoid smoothing could explain), so a consumer drives only the switch. The tables leave these callbacks commented out and kick with "
			"their own physics.",
			*m,
		),
		mechanism(
			"mechanism.flippers", "Three flippers, cabinet-wired", "other", [coil(32)], [switch(81), switch(82)],
			"Three flippers (IPDB): lower left and right, and an upper right flipper on the right side of the playfield. The "
			"cabinet buttons fire them through the flipper circuit while the GAME OVER RELAY (Q, 32) is energized, so no driver "
			"of their own appears in the solenoid test; PinMAME fabricates 45-48 from the buttons at 141 and 143 while 32 is on. "
			"The ROM reads the buttons as matrix switches 81 and 82, which core_updateSw copies from 143 and 141. The VPW table "
			"fires its upper right flipper from the staged right flipper key, which VPX maps to the right flipper key unless a "
			"separate staged key is set.",
			*m, VPM_LIBRARY_SOURCE, IDENTITY_SOURCE,
		),
		mechanism(
			"mechanism.relays-and-backbox", "Relays, rope lights, knocker and coin meter", "other",
			[coil(26), coil(31), coil(22), coil(30), coil(27)], [],
			"The LIGHTBOX RELAY (A, 26) switches the backbox lightbox illumination and the TILT RELAY (T, 31) the playfield G.I., "
			"which goes out while it is energized (PinMAME's System 3 init types them as the A and T relays; the VPW script turns "
			"its G.I. lights off while 31 is on). ROPE LIGHTS (22) is the ring of LEDs around Ra in the backbox (PinMAME's "
			"stargate block), which the ROM flashes in attract mode. The KNOCKER (30) is in the cabinet, and TICKET/COIN METER "
			"(27) drives an optional ticket dispenser or coin meter.",
			*m,
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


COVERAGE_MISSING = ["polarity", "spatial_placement"]


def gi_relay_spatial() -> dict[str, Any]:
	return located("device.tilt-relay-t", "emitter", [xy for _, xy in GI_LIGHTS], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)


def build_base() -> dict[str, Any]:
	outputs = solenoid_outputs() + lamp_outputs()
	for output in outputs:
		if output["binding"] == {"group": "pinmame.output.solenoid", "device": 31}:
			output["spatial"] = gi_relay_spatial()
			output["physical"]["notes"] += (
				" The placements are the bulb lights of the VPW table's GI collection (" + gi_spatial_note() + "), which GIState "
				"switches with this relay; without a manual no G.I. bulb count or layout is known, and a table's grouping is not "
				"the machine's wiring, so they stay observed without a quantity."
			)
			output["physical"]["location"] = "relay in the cabinet or backbox; the placements are the playfield G.I. it switches"
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Stargate", "manufacturer": "Gottlieb", "year": 1995, "kind": "physical_pinball",
			"model_number": "742", "ipdb_id": 2847, "opdb_id": "G50pv-MdE6R",
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
		"outputs": outputs,
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
		raise RuntimeError(f"Stargate device identifiers are not unique: {duplicates}")
	return definition


def apply_legacy_aliases(definition: dict[str, Any]) -> None:
	"""Carry the legacy import's numeric and zero-padded aliases by binding, while compatibility needs them."""
	legacy = load_json(LEGACY_ALIAS_SEED_PATH)["aliases"]
	devices = {(device["binding"]["group"], str(device["binding"]["device"])): device for device in definition["inputs"] + definition["outputs"]}
	for group, addresses in legacy.items():
		for address, aliases in addresses.items():
			device = devices.get((group, address))
			if device is None:
				raise RuntimeError(f"legacy alias target {group} {address} is not in the Stargate definition")
			device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in aliases]


def build() -> dict[str, Any]:
	return build_base()


SPATIAL_BLOCKERS = [
	"No factory drawing is retained: IPDB lists the operations manual without hosting it, and no other attributable copy "
	"was found, so no placement can be checked against the machine's own switch, lamp or coil location drawings.",
	"The two retained tables are not independent: the VPW v2.0 table credits the 32Assassin and JLouLoulou v1.3.0 release as "
	"the table it rebuilt, so their agreement could only supplement a placement, never validate it. Every placement here "
	"comes from the VPW table and stays observed.",
	"Solenoid 31 (Tilt Relay, playfield G.I.): the 16 placements are the bulb lights of the VPW table's GI collection; a "
	"table's grouping is not the machine's wiring and the bulb count is unknown, so they stay observed without a quantity.",
	"Glider switches 20, 21 and 30, ball gate sensor 101 and pyramid sensor 102 have no table object of their own and are "
	"projected onto the glider, the ball gate and the pyramid top.",
]


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
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
		"status": "observed",
		"blockers": SPATIAL_BLOCKERS,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952.941; 0=left, 1=right",
			"y": "y/2164.706; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "table_sha256": TABLE_SHA256, "obj_export_sha256": OBJ_EXPORT_SHA256},
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
		"excluded_object_classes": [
			"BM_ and LM_ baked render primitives other than the drop targets, guardians, pyramid top, glider and auto-plunger arm, which are placed at their world mesh centres",
			"f0-f5 Light objects: flasher companions the script copies from L120-L125 (lines 189-210); L120-L125 are the placements",
			"Flipper helpers APFlipper, LeftFlipper1, LeftFlipper2 and RightFlipper2, parked off the playfield to drive animations",
			"Triggers RampTrigger001-011, LWiresCorner3/5, TrapTriggerL/R, TriggerLF/RF and swPlunger: sound, physics and trap helpers with no switch binding",
			"HitTargets sw14col, sw15col and sw16col: the kicking targets' collision helpers; sw14, sw15 and sw16 carry the switches",
			"VR room, cabinet and backbox objects (VRCab, VRMin, VRMega collections and the lights at y = -76 or below)",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Stargate (Gottlieb, 1995) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/gottlieb/stargate-1995.json`; "
		f"its spatial dimension stays open because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained known-working `Stargate (Gottlieb 1995) v2.0.vpx` by VPin Workshop, SHA-256 "
		f"`{TABLE_SHA256}`, whose embedded script (SHA-256 `{SCRIPT_SHA256}`) is the binding authority. Bounds are "
		f"`{TABLE_BOUNDS}`; every coordinate is x/952.941 and y/2164.706, rounded to at most six places.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker or bumper "
		"for a switch, the `L<n>` bulb light `vpmMapLights` binds to each lamp and auxiliary flasher, the object a coil moves "
		"or kicks from, and each G.I. bulb light of the `GI` collection.",
		"- Baked-mesh primitives (the drop targets, the Horus guardians, the pyramid top, the glider and the auto-plunger arm) "
		"are placed at the centre of their world-space mesh from `vpxtool export obj --units vpu`. Control: `BM_KT_sw14` lies "
		"within 1.4 units of `HitTarget sw14`'s stored position.",
		"- Sensors and coils with no table object of their own are documented projections onto their own mechanism's object.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: the nine lightbox lamps and the two lightbox "
		"flashers (126, 127), the credit-button lamp, the rope lights, the lightbox and game-over relays, the knocker, the coin "
		"meter, the cabinet and flipper-button switches, the test inputs and the DMD.",
		"- No placement is validated: no factory drawing is retained to check it, and the two retained tables share ancestry.",
		"",
		"## Explicit projections",
		"",
	]
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
		"Every controller address is enumerated with a semantic disposition taken from the ROM's own service tests, the "
		"mechanisms are covered, polarity is settled by the read path with the ROM's or the known-working script's active "
		"level for every switch except GLIDER LEFT (MOTOR) (20), and all six drivers name every address alike. Promotion to "
		"`author_ready` is refused because every playfield placement rests on one community table's geometry with nothing "
		"independent to check it and switch 20's active level is unknown, so `coverage.missing` is "
		"`[\"polarity\", \"spatial_placement\"]`. The Stargate operations manual's switch, lamp and coil location "
		"drawings, or a second table built independently from the machine, would close the spatial gap.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		if STATUS != "author_ready":
			raise RuntimeError(f"refusing to replace the author-ready Stargate definition with a {STATUS} one: {stale}")
		stale.unlink()
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Stargate is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Stargate definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Stargate seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Stargate spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Stargate spatial review drifted from its deterministic curator: {markdown_path}")
	print("Stargate definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Stargate extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Stargate retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
