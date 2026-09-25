"""Curate the physical Sega GoldenEye (1996) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal below, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: the retained manual scan lost every callout number from its playfield location
# drawings, so no placement can be checked against a factory drawing and every coordinate comes
# from one community table (observed); several flasher sockets have no table object; and public
# solenoid 36 carries an undocumented magnet-board latch bit in LibPinMAME's default output mode.
PARTIAL_PATH = ROOT / "machines/partial/sega/goldeneye-1996.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/sega/goldeneye-1996.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/sega/goldeneye-1996.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/sega/goldeneye-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/sega/goldeneye-1996.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts/sega.goldeneye.1996"
EXCERPT_PREFIX = "evidence/excerpts/sega.goldeneye.1996"
RUNTIME_PATH = "evidence/runtime/whitestar/goldeneye-satellite-and-ball-serve.json"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
MANUAL_SOURCE = "manual.sega.goldeneye.1996.operations-manual"
VPX_TABLE_SOURCE = "vpx-table.goldeneye-vpw-1-2-1"
VPX_SCRIPT_SOURCE = "vpx-script.goldeneye-vpw-1-2-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.goldeneye-vpw-1-2-1"
VPW_CORPUS_SCRIPT_SOURCE = "vpx-script.goldeneye-vpw-1-2"
DOZER_SCRIPT_SOURCE = "vpx-script.goldeneye-dozer-2"
VPM_LIBRARY_SOURCE = "vpx-script.vpinmame-sega2-library"
RUNTIME_SOURCE = "runtime.goldeneye.satellite-and-ball-serve"

MANUAL_SHA256 = "0203f37a1342e9ecb0205a37a5d45fa695591904e1355d43291565605214470f"
MANUAL_OCR_SHA256 = "52c190a3949710bcc470facf80ba67f943464fec2f1d8bbe9b703a084794a707"
TABLE_SHA256 = "4438e8e271d4593abc8b9faa5ef1a586b6b004692010fc8eaafbbf1ce0ef9310"
SCRIPT_SHA256 = "b0f1e0d13ee5ca2729e01000d9205a4de75473e082be9338e429a01438f04a84"
VPW_CORPUS_SCRIPT_SHA256 = "9836e0d43739c39d887672a9ad9b640fb368ab95e0a06f4fda1be005e58dd871"
DOZER_SCRIPT_SHA256 = "99b7378c66729a6fbf541de0c77a2897536458dc780121e4bc75c76661cb03c5"
SEGA2_VBS_SHA256 = "786524789eccb014ca104fc501ee9cbf8e0bad71fcc4ec95496b109886cb17dd"
CORE_VBS_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

EXTRACTION_RELATIVE_PATH = Path("sega/goldeneye-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("sega/goldeneye-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "d4d2fd649ab9a3b5b1ae9b9e8ad5c2ed720b7a1d1b637db5bb1edc3cff34ab69"
EXTRACTION_FILE_COUNT = 4144
EXTRACTION_TOTAL_BYTES = 483050999

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

DRIVER_IDS = ("gldneye",)
DRIVER_COMPATIBILITY = {
	"gldneye": (
		"identical",
		"Sega GoldenEye, the only PinMAME driver for the machine: game ROM bondcpu.404, display ROM bondispa.400 "
		"and sound ROMs bondu7/bondu17/bondu21, declared with the de_mSES1 Whitestar machine driver. Both retained "
		"scripts and the retained table run this driver.",
	),
}

# --- Printed switch matrix (manual printed 20 grid and printed 21 description list). -----------------
# (label, switch type, part, location class, roles, printed description)
SWITCHES: dict[int, tuple[str, str, str | None, str, list[str]]] = {
	1: ("Plumb Bob Tilt", "tilt", None, "cabinet", ["cabinet.tilt"]),
	2: ("4th Coin Slot", "button", None, "cabinet", ["cabinet.coin.fourth"]),
	3: ("Start Button", "button", "500-5026-07", "cabinet", ["cabinet.start"]),
	4: ("Right Coin Slot", "button", "180-5024-00", "cabinet", ["cabinet.coin.right"]),
	5: ("Center Coin Slot / DBA", "button", "180-5024-00", "cabinet", ["cabinet.coin.center"]),
	6: ("Left Coin Slot", "button", "180-5024-00", "cabinet", ["cabinet.coin.left"]),
	7: ("Slam Tilt", "tilt", "180-5022-00", "cabinet", ["cabinet.slam-tilt"]),
	9: ("Fire Button", "button", "180-5111-00", "cabinet", ["cabinet.fire"]),
	10: ("5-Ball Trough #1 (Left)", "microswitch", "180-5119-00", "playfield", ["internal.trough"]),
	11: ("5-Ball Trough #2", "microswitch", "180-5119-00", "playfield", ["internal.trough"]),
	12: ("5-Ball Trough #3", "microswitch", "180-5119-00", "playfield", ["internal.trough"]),
	13: ("5-Ball Trough #4", "microswitch", "180-5119-00", "playfield", ["internal.trough"]),
	14: ("5-Ball Trough #5 (Right)", "microswitch", "180-5119-00", "playfield", ["internal.trough"]),
	15: ("5-Ball Trough VUK Opto", "opto", "520-5124-00 transmitter with 520-5125-00 receiver", "playfield", ["internal.trough"]),
	16: ("Shooter Lane", "microswitch", "500-570X-00", "playfield", []),
	17: ("Right Ramp Exit", "microswitch", "180-5087-00", "playfield", []),
	18: ("Center Ramp Exit", "microswitch", "180-5087-00", "playfield", []),
	19: ("Right Ramp Enter", "microswitch", "180-5087-00", "playfield", []),
	20: ("Satellite Home", "microswitch", "180-5052-00", "playfield", []),
	23: ("Satellite Magnet Board", "other", None, "playfield", []),
	24: ("Flipper Magnet Board", "other", None, "playfield", []),
	25: ("Left 5-Bank Bottom", "leaf", "515-5162-00", "playfield", []),
	26: ("Left 5-Bank Middle-Bottom", "leaf", "515-5162-00", "playfield", []),
	27: ("Left 5-Bank Middle", "leaf", "515-5967-00", "playfield", []),
	28: ("Left 5-Bank Middle Top", "leaf", "515-5162-00", "playfield", []),
	30: ("Left Stand-Up", "leaf", "515-5967-00", "playfield", []),
	31: ("Right Stand-Up", "leaf", "515-5967-00", "playfield", []),
	32: ("Left Ramp Made", "microswitch", "180-5087-00", "playfield", []),
	33: ("2-Bank Bottom", "leaf", "515-5162-00", "playfield", []),
	34: ("2-Bank Top", "leaf", "515-5162-00", "playfield", []),
	39: ("Eject Stand-Up", "leaf", "515-5967-00", "playfield", []),
	40: ("Left Ramp Enter", "microswitch", "180-5087-00", "playfield", []),
	41: ("Left Turbo Bumper", "leaf", "180-5015-03", "playfield", []),
	42: ("Bottom Turbo Bumper", "leaf", "180-5015-03", "playfield", []),
	43: ("Right Turbo Bumper", "leaf", "180-5015-03", "playfield", []),
	44: ("Right 5-Bank Top", "leaf", "515-5162-00", "playfield", []),
	45: ("Right 5-Bank Middle Top", "leaf", "515-5162-00", "playfield", []),
	46: ("Right 5-Bank Middle", "leaf", "515-5162-00", "playfield", []),
	47: ("Right 5-Bank Middle Bottom", "leaf", "515-5967-00", "playfield", []),
	48: ("Right 5-Bank Bottom", "leaf", "515-5162-00", "playfield", []),
	50: ("Scoop", "microswitch", "180-5057-00", "playfield", []),
	51: ("Right Top Lane", "microswitch", "500-570X-00", "playfield", []),
	52: ("Middle Top Lane", "microswitch", "500-570X-00", "playfield", []),
	53: ("Left Top Lane", "microswitch", "500-570X-00", "playfield", []),
	54: ("Center Ramp Enter", "microswitch", "180-5087-00", "playfield", []),
	55: ("Top Lane Enter", "unknown", None, "playfield", []),
	56: ("Tank Trap Door", "unknown", None, "playfield", []),
	57: ("Left Outlane", "microswitch", "500-570X-00", "playfield", []),
	58: ("Right Outlane", "microswitch", "500-570X-00", "playfield", []),
	59: ("Left Return Lane", "microswitch", "500-570X-00", "playfield", []),
	60: ("Right Return Lane", "microswitch", "500-570X-00", "playfield", []),
	61: ("Left Slingshot", "leaf", "180-5054-00", "playfield", []),
	62: ("Right Slingshot", "leaf", "180-5054-00", "playfield", []),
	63: ("Left Flipper Button", "button", "180-5122-00", "cabinet", ["flipper.lower.left.button"]),
	64: ("Right Flipper Button", "button", "180-5122-00", "cabinet", ["flipper.lower.right.button"]),
}
UNUSED_MATRIX_ADDRESSES = {8, 21, 22, 29, 35, 36, 37, 38, 49}
# vpmTimer.PulseSw callers in the retained script: ramp gates, targets, bumpers, slingshots, the flipper
# magnet release and SolLockOut's pulse of the VUK opto.
PULSED_SWITCHES = {15, 17, 18, 19, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 54, 61, 62}
SWITCH_COLUMN_WIRING = {
	1: ("Q1", "GRN-BRN", "CN5-1"), 2: ("Q2", "GRN-RED", "CN5-3"), 3: ("Q3", "GRN-ORG", "CN5-4"),
	4: ("Q4", "GRN-YEL", "CN5-5"), 5: ("Q5", "GRN-BLK", "CN5-6"), 6: ("Q6", "GRN-BLU", "CN5-7"),
	7: ("Q7", "GRN-VIO", "CN5-8"), 8: ("Q8", "GRN-GRY", "CN5-9"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "CN7-9"), 2: ("WHT-RED", "CN7-8"), 3: ("WHT-ORG", "CN7-7"), 4: ("WHT-YEL", "CN7-6"),
	5: ("WHT-GRN", "CN7-5"), 6: ("WHT-BLU", "CN7-3"), 7: ("WHT-VIO", "CN7-2"), 8: ("WHT-GRY", "CN7-1"),
}
# Public -> (printed dedicated switch, wire, connector, label, role, note)
DEDICATED_SWITCHES = {
	-2: ("DS-6", "GRY-BLU", "CN6-8", "Volume / Left (Red Button)", "service.button", "Normal: Volume. In Test: Left."),
	-1: ("DS-7", "GRY-VIO", "CN6-9", "Service Credits / Right (Green Button)", "service.button", "Normal: Service Credits. In Test: Right."),
	0: ("DS-8", "GRY-BLK", "CN6-10", "Begin Test / Enter (Black Button)", "service.test", "Normal: Begin Test. In Test: Enter."),
}
# Whitestar's flipper column is read as dedicated inputs DS-1..DS-5 (se.c dedswitch_r); GoldenEye prints
# all five NOT USED and takes its flipper buttons through the matrix instead.
UNUSED_DEDICATED = {
	81: ("DS-4", "GRY-YEL", "CN6-6", "right flipper end-of-stroke"),
	82: ("DS-3", "GRY-ORG", "CN6-4", "right flipper button"),
	83: ("DS-2", "GRY-RED", "CN6-3", "left flipper end-of-stroke"),
	84: ("DS-1", "GRY-BRN", "CN6-2", "left flipper button"),
	88: ("DS-5", "GRY-GRN", "CN6-7", "upper flipper button"),
}

# Flipper-column end-of-stroke bits core_updateSw rewrites every frame: address -> (side, public winding).
SYNTHETIC_EOS_INPUTS = {81: ("Right", 46), 83: ("Left", 48)}

# Retained table objects (normalized x/952, y/2162). "center" is the object's own center; walls use the
# bounding-box center of their drag points.
SWITCH_POSITIONS = {
	10: (0.859077, 0.875321), 11: (0.859077, 0.875321), 12: (0.859077, 0.875321), 13: (0.859077, 0.875321),
	14: (0.859077, 0.875321), 15: (0.859077, 0.875321), 16: (0.944731, 0.891371),
	17: (0.050705, 0.52556), 18: (0.827013, 0.053942), 19: (0.853814, 0.34681), 20: (0.669427, 0.354595),
	23: (0.669118, 0.355227), 24: (0.4511, 0.914716),
	25: (0.084562, 0.560729), 26: (0.110691, 0.538931), 27: (0.13225, 0.520869), 28: (0.154844, 0.502087),
	30: (0.214201, 0.366465), 31: (0.340631, 0.348608), 32: (0.334554, 0.20696), 33: (0.805208, 0.608594),
	34: (0.783536, 0.583495), 39: (0.44082, 0.27745), 40: (0.117644, 0.299756),
	41: (0.57351, 0.192903), 42: (0.673382, 0.272063), 43: (0.779023, 0.189343),
	44: (0.574252, 0.372744), 45: (0.611528, 0.389015), 46: (0.648162, 0.404849), 47: (0.679001, 0.417763),
	48: (0.709583, 0.430758), 50: (0.384451, 0.132164), 51: (0.701475, 0.097128), 52: (0.606616, 0.097494),
	53: (0.512652, 0.097556), 54: (0.223658, 0.237028), 55: (0.826298, 0.062286), 56: (0.042158, 0.353158),
	57: (0.046648, 0.734893), 58: (0.854961, 0.73381), 59: (0.12883, 0.734986), 60: (0.774826, 0.733443),
	61: (0.227133, 0.730066), 62: (0.67492, 0.729382),
}
SWITCH_OBJECTS = {
	16: "Trigger SW16", 17: "Gate GateSw17", 18: "Gate GateSw18", 19: "Gate GateSw19", 32: "Gate GateSw32",
	40: "Gate GateSw40", 54: "Gate GateSw54", 25: "Wall SS25", 26: "Wall SS26", 27: "Wall SS27", 28: "Wall SS28",
	30: "Wall SS30", 31: "Wall SS31", 33: "Wall SS33", 34: "Wall SS34", 39: "Wall SS39", 44: "Wall SS44",
	45: "Wall SS45", 46: "Wall SS46", 47: "Wall SS47", 48: "Wall SS48", 41: "Bumper LeftTurboBumper",
	42: "Bumper BottomTurboBumper", 43: "Bumper RightTurboBumper", 50: "Kicker Scoop", 51: "Trigger SW51",
	52: "Trigger SW52", 53: "Trigger SW53", 55: "Trigger SW55", 57: "Trigger SW57", 58: "Trigger SW58",
	59: "Trigger SW59", 60: "Trigger SW60", 61: "Wall LeftSlingShot", 62: "Wall RightSlingShot",
}
SWITCH_PROJECTIONS = {
	10: "Trough switch projected onto the retained BallRelease kicker, where the table's bsTrough holds balls on 10-14 and ejects them; the table models no per-ball trough object.",
	11: "Trough switch projected onto the retained BallRelease kicker (see switch 10).",
	12: "Trough switch projected onto the retained BallRelease kicker (see switch 10).",
	13: "Trough switch projected onto the retained BallRelease kicker (see switch 10).",
	14: "Trough switch projected onto the retained BallRelease kicker (see switch 10).",
	15: "VUK opto projected onto the retained BallRelease kicker, the table's stand-in for the trough up-kicker it sits on.",
	20: "Satellite home cam switch projected onto the satellite dish primitive RadarA; the switch sits on the motor base under it.",
	23: "Magnet-board ball detection projected onto the RadarKicker the table uses to hold a ball on the satellite magnet.",
	24: "Magnet-board ball detection projected onto the FlipperMagnet trigger between the flippers.",
	56: "Tank switch projected onto the TankKickBig kicker where the table's bsTank (switch 56) holds balls.",
}

# --- Coils detailed chart (manual printed 24 and page v). -------------------------------------------
# public -> (label, kind, D.T., control wire, control connect, power color, power connection, voltage, coil)
SOLENOIDS: dict[int, tuple[str, str, str, str, str, str, str, str, str | None]] = {
	1: ("Trough Up-Kicker", "coil", "Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-4/5", "50v", "23-800 090-5000-01"),
	2: ("Auto Launch", "coil", "Q2", "BRN-RED", "J8-P3", "YEL-VIO", "J10-4/5", "50v", "24-940 090-5036-01"),
	4: ("Power Scoop", "coil", "Q4", "BRN-YEL", "J8-P5", "YEL-VIO", "J10-4/5", "50v", "23-800 090-5000-01"),
	8: ("Replay Knocker Drive Line", "coil", "Q8", "BRN-GRY", "J8-P9", "YEL-VIO", "J10-4/5", "50v", None),
	9: ("Left Turbo Bumper", "coil", "Q9", "BLU-BRN", "J9-P1", "YEL-VIO", "J10-4/5", "50v", "26-1200 090-5044-00"),
	10: ("Bottom Turbo Bumper", "coil", "Q10", "BLU-RED", "J9-P2", "YEL-VIO", "J10-4/5", "50v", "26-1200 090-5044-00"),
	11: ("Right Turbo Bumper", "coil", "Q11", "BLU-ORG", "J9-P4", "YEL-VIO", "J10-4/5", "50v", "26-1200 090-5044-00"),
	12: ("Left Slingshot", "coil", "Q12", "BLU-YEL", "J9-P5", "YEL-VIO", "J10-4/5", "50v", "26-1200 090-5044-00"),
	13: ("Right Slingshot", "coil", "Q13", "BLU-GRN", "J9-P6", "YEL-VIO", "J10-4/5", "50v", "26-1200 090-5044-00"),
	14: ("Tank Kicker", "coil", "Q14", "BLU-BLK", "J9-P7", "YEL-VIO", "J10-4/5", "50v", "23-800 090-5000-01"),
	17: ("Trough Lock Ball", "coil", "Q17", "VIO-BRN", "J7-P2", "BRN", "J7-1", "20v", "25-1240 090-5034-00"),
	18: ("Up-Down Ramp Plunger", "coil", "Q18", "VIO-RED", "J7-P3", "BRN", "J7-1", "20v", "27-1500 090-5004-00"),
	20: ("Satellite Launch Ramp", "coil", "Q20", "VIO-YEL", "J7-P6", "BRN", "J7-1", "20v", "27-1500 090-5004-00"),
	21: ("Satellite Motor Relay", "relay", "Q21", "VIO-GRN", "J7-P7", "BRN", "J7-1", "20v", None),
	22: ("Tank Trap Door", "coil", "Q22", "VIO-BLU", "J7-P8", "BRN", "J7-1", "20v", "27-1500 090-5004-00"),
	24: ("Coin Meter", "coil", "Q24", "VIO-GRY", "J7-P10", "BRN", "J16-7", "5v", None),
}
UNUSED_SOLENOIDS = {
	3: ("Q3", "BRN-ORG", "J8-P4", "YEL-VIO"),
	5: ("Q5", "BRN-GRN", "J8-P6", "YEL-VIO"),
	6: ("Q6", "BRN-BLU", "J8-P7", "BRN"),
	7: ("Q7", "BRN-VIO", "J8-P8", "YEL-VIO"),
	19: ("Q19", "VIO-ORG", "J7-P4", "BRN"),
	23: ("Q23", "VIO-BLK", "J7-P9", "BRN"),
}
# Flash lamps: public -> (label, D.T., control wire, control connect, playfield/back-panel quantity,
# printed locations, printed bulbs)
FLASHERS = {
	25: ("Flasher Bottom Left and Right", "Q25", "BLK-BRN", "J6-P1", 2, "Bottom L&R X2, Backbox Insert X1", "2X #906, 1X #89"),
	26: ("Flasher Lower Flipper Magnet", "Q26", "BLK-RED", "J6-P2", 1, "Lower Flipper Magnet X1, Backbox Insert X2", "1X #906, 2X #89"),
	27: ("Flasher Lower Left", "Q27", "BLK-ORG", "J6-P3", 2, "Lower Left X2, Backbox Insert X1", "2X #906, 1X #89"),
	28: ("Flasher Satellite", "Q28", "BLK-YEL", "J6-P4", 2, "Satellite X2, Backbox Insert X2", "4X #89"),
	29: ("Flasher Lower Right Playfield", "Q29", "BLK-GRN", "J6-P5", 2, "Lower Right Playfield X2, Backbox Insert X2", "4X #89"),
	30: ("Flasher Helicopter", "Q30", "BLK-BLU", "J6-P6", 1, "Helicopter X1, Backbox Insert X1", "2X #89"),
	31: ("Flasher Upper Left and Back Panel", "Q31", "BLK-VIO", "J6-P7", 3, "Upper Left X1, Backpanel X2, Backbox Insert X1", "4X #89"),
	32: ("Flasher Upper Right and Back Panel", "Q32", "BLK-GRY", "J6-P8", 3, "Upper Right X2, Backpanel X1, Backbox Insert X1", "4X #89"),
}
# Retained script flasher objects that stand for a printed playfield/back-panel socket.
FLASHER_POSITIONS = {
	25: [(0.75962, 0.803119), (0.148214, 0.804297)],
	27: [(0.050275, 0.587681), (0.100935, 0.483525)],
	28: [(0.718536, 0.38814)],
	29: [(0.853193, 0.568084)],
	31: [(0.336258, 0.000081), (0.09477, 0.000421)],
	32: [(0.877586, 0.000058)],
}
FLASHER_NOTES = {
	25: "Placed at the retained Sol25 lights Flash001 (right) and Flash002 (left), one per printed Bottom L&R socket.",
	26: (
		"Not placed: the retained Sol26 lights Flasher26 (an off-table helper at x < 0) and LL15F, which sits on "
		"the GOLDENEYE insert (lamp 15) at mid-playfield, not at the flipper magnet between the flippers that the "
		"printed location names, so no retained object stands for this socket."
	),
	27: "Placed at the retained Sol27 lights Flash003A and Flash003B, one per printed Lower Left socket.",
	28: "One of the two printed Satellite sockets is placed, at the retained Sol28 light Flash004 beside the satellite; the table models no second socket.",
	29: "One of the two printed Lower Right Playfield sockets is placed, at the Flupper dome Flasherbase1 the retained Sol29 drives; the table models no second socket.",
	30: (
		"Not placed: the retained Sol30 drives two lights (Flash003 below the helicopter and rampflash4 beside the "
		"scoop) for a printed single Helicopter socket, and neither is a bulb object at the helicopter."
	),
	31: (
		"The two printed Backpanel sockets are placed at the Flupper domes Flasherbase2 and Flasherbase3 the retained "
		"Sol31 drives, on the back panel at the rear edge of the playfield (the Back Panel Assembly lists three #89 "
		"stand-up short sockets: these two plus flasher 32's); the printed Upper Left playfield socket has no table object."
	),
	32: (
		"The printed Backpanel socket is placed at the Flupper dome Flasherbase4 the retained Sol32 drives; the two "
		"printed Upper Right playfield sockets have no table object."
	),
}
SOLENOID_POSITIONS = {
	1: [(0.859077, 0.875321)], 2: [(0.946062, 0.894757)], 4: [(0.384451, 0.132164)],
	9: [(0.57351, 0.192903)], 10: [(0.673382, 0.272063)], 11: [(0.779023, 0.189343)],
	12: [(0.227133, 0.730066)], 13: [(0.67492, 0.729382)], 14: [(0.042158, 0.353158)],
	17: [(0.859077, 0.875321)], 18: [(0.949645, 0.188682)], 20: [(0.554708, 0.528289)],
	21: [(0.669427, 0.354595)], 22: [(0.042779, 0.403357)],
	33: [(0.669118, 0.355227)], 34: [(0.4511, 0.914716)],
}
SOLENOID_OBJECTS = {
	1: "Kicker BallRelease (projection: the table's trough exit stands in for the up-kicker)",
	2: "Kicker Plunger (the auto-launch kicker at the foot of the shooter lane)",
	4: "Kicker Scoop",
	9: "Bumper LeftTurboBumper", 10: "Bumper BottomTurboBumper", 11: "Bumper RightTurboBumper",
	12: "Wall LeftSlingShot (bounding-box center)", 13: "Wall RightSlingShot (bounding-box center)",
	14: "Kicker TankKickBig",
	17: "Kicker BallRelease (projection: the lock-ball coil sits on the trough beside the up-kicker)",
	18: "Primitive MrampA (projection: the plunger sits under the up-down ramp the script moves)",
	20: "Primitive RampSat3D (the satellite launch ramp the script raises)",
	21: "Primitive RadarA (projection: the relay drives the satellite motor under the dish)",
	22: "Kicker DropRamp1 (the trap door on the wire ramp the script opens)",
	33: "Kicker RadarKicker (the ball-hold position on the satellite magnet)",
	34: "Trigger FlipperMagnet (the magnet under the playfield between the flippers)",
}
SOLENOID_CALLBACKS = {
	1: 'SolCallback(1) = "bsTrough.SolOut"', 2: 'SolCallback(2) = "bsPlunger.SolOut"', 4: 'SolCallback(4) = "bsScoop.SolOut"',
	8: "SolCallback(8) plays the knocker sound", 14: 'SolCallback(14) = "bsTank.SolOut"', 17: 'SolCallback(17) = "SolLockOut", which pulses switch 15',
	18: 'SolCallback(18) = "SolUpDownRamp"', 20: 'SolCallback(20) = "SolSatLaunchRamp"', 21: 'SolCallback(21) = "SolSatMotorRelay"',
	22: 'SolCallback(22) = "DropRamp1.Enabled="', 25: 'SolModCallback(25) = "Sol25"', 26: 'SolModCallback(26) = "Sol26"',
	27: 'SolModCallback(27) = "Sol27"', 28: 'SolModCallback(28) = "Sol28"', 29: 'SolModCallback(29) = "Sol29"',
	30: 'SolModCallback(30) = "sol30"', 31: 'SolModCallback(31) = "Sol31"', 32: 'SolModCallback(32) = "Sol32"',
	33: 'SolCallback(33) = "SolRadarMagnet"', 34: 'SolCallback(34) = "SolFlipperMagnet"',
	45: 'SolCallback(45) = "TiltMod", a no-op in that script', 46: 'SolCallback(sLRFlipper) = "SolRFlipper" (sLRFlipper = 46 in core.vbs)',
	48: 'SolCallback(sLLFlipper) = "SolLFlipper" (sLLFlipper = 48 in core.vbs; sega2.vbs also sets GameOnSolenoid = 48)',
}

# --- Lamp matrix grid (manual page iii). Lamp = (row - 1) x 8 + column. -----------------------------
LAMP_LABELS = {
	1: "Military Intelligence HQ", 2: "Eject Hurry-Up", 3: "Electro Magnetic Pulse", 4: "Severnaya Station",
	5: "Tank Chase", 6: "Petya Station", 7: "Cat and Mouse", 8: "Nerve Gas",
	10: "Right Outlane", 11: "Right Return Lane", 12: "Left Return Lane", 13: "Shoot Again", 14: "Jump Ramp",
	15: "GoldenEye", 16: "Mischa Satellite", 17: "Scoop Bottom", 18: "Scoop Top", 19: "Left Turbo Bumper",
	20: "Right Ramp Arrow", 21: "Right Ramp Top", 22: "Right Ramp Bottom", 23: "2-Bank Bottom", 24: "2-Bank Top",
	25: "Left Stand-Up Left", 26: "Left Stand-Up Right", 27: "Bottom Turbo Bumper", 28: "Eject Bottom", 29: "Eject Top",
	30: "Left Top Lane", 31: "Middle Top Lane", 32: "Right Top Lane", 33: "Left Outlane", 34: "Right Ramp Enter",
	35: "Left Ramp", 36: "Left Ramp Top", 37: "Middle Ramp Bottom", 38: "Middle Ramp Top", 39: "Under Ramp Top",
	40: "Under Ramp Bottom", 41: "Right Turbo Bumper", 42: "Scoop Arrow", 43: "Left Ramp Arrow", 44: "Narrow Escape",
	45: "Left 5-Bank Middle Top", 46: "Left 5-Bank Middle", 47: "Left 5-Bank Middle Bottom", 48: "Left 5-Bank Bottom",
	49: "Helicopter", 50: "Center Ramp Enter Left", 51: "Center Ramp Enter Right", 52: "Right 5-Bank Bottom",
	53: "Right 5-Bank Middle Bottom", 54: "Right 5-Bank Middle", 55: "Right 5-Bank Middle Top", 56: "Right 5-Bank Top",
	57: "Start Button", 58: "Behind Eject Stand-Up", 59: "Above Eject Stand-Up", 60: "Lock 1", 61: "Lock 2",
	62: "Right Fire Missile", 63: "Left Fire Missile", 65: "100 Million", 66: "75 Million", 67: "50 Million",
	68: "25 Million", 69: "Helicopter Spotlight", 72: "GoldenEye Letter E (Last)", 73: "GoldenEye Letter G",
	74: "GoldenEye Letter O", 75: "GoldenEye Letter L", 76: "GoldenEye Letter D", 77: "GoldenEye Letter E (First)",
	78: "GoldenEye Letter N", 79: "GoldenEye Letter E (Second)", 80: "GoldenEye Letter Y",
}
PRINTED_LAMP_TEXT = {
	1: "MILITARY INTEL-LIGENCE HQ", 3: "ELECTRO MAG-NETIC PULSE", 11: "RIGHT RE-TURN LANE", 12: "LEFT RE-TURN LANE",
	19: "LEF TURBO BUMPER", 27: "BOT. TURBO BUMPER", 37: "MID. RAMP BOTTOM", 38: "MID. RAMP TOP",
	40: "UNDER RAMP BOT.", 45: "LT. 5-BANK MID-TOP", 46: "LT. 5-BANK MIDDLE", 47: "LT. 5-BANK MID-BOT",
	48: "LT. 5-BANK BOTTOM", 52: "RT. 5-BANK BOTTOM", 53: "RT. 5-BANK MID-BOT", 54: "RT. 5-BANK MIDDLE",
	55: "RT. 5-BANK MID-TOP", 56: "RT. 5-BANK TOP", 58: "BEHIND EJECT S-U", 59: "ABOVE EJECT S-U",
	69: "HELICOPTER SPOTLITE", 72: "GOLDEN-EY( E )", 73: "( G )OLDEN-EYE", 74: "G( O )LDEN-EYE", 75: "GO( L )DEN-EYE",
	76: "GOL( D )EN-EYE", 77: "GOLD( E )N-EYE", 78: "GOLDE( N )-EYE", 79: "GOLDEN-( E )YE", 80: "GOLDEN-E( Y )E",
}
UNUSED_LAMPS = {9, 64, 70, 71}
SPEAKER_PANEL_LAMPS = set(range(72, 81))
LAMP_COLUMN_WIRING = {
	1: ("U10", "YEL-BRN", "J13-1"), 2: ("U11", "YEL-RED", "J13-3"), 3: ("U12", "YEL-ORG", "J13-4"), 4: ("U13", "YEL-BLK", "J13-5"),
	5: ("U14", "YEL-GRN", "J13-6"), 6: ("U15", "YEL-BLU", "J13-7"), 7: ("U16", "YEL-VIO", "J13-8"), 8: ("U17", "YEL-GRY", "J13-9"),
}
LAMP_ROW_WIRING = {
	1: ("Q33", "RED-BRN", "J12-1"), 2: ("Q34", "RED-BLK", "J12-2"), 3: ("Q35", "RED-ORG", "J12-3"), 4: ("Q36", "RED-YEL", "J12-4"),
	5: ("Q37", "RED-GRN", "J12-5"), 6: ("Q38", "RED-BLU", "J12-6"), 7: ("Q39", "RED-VIO", "J12-8"), 8: ("Q40", "RED-GRY", "J12-9"),
	9: ("Q41", "RED-WHT", "J12-10"), 10: ("Q42", "RED", "J12-11"),
}
LAMP_POSITIONS = {
	1: (0.411336, 0.703542), 2: (0.543275, 0.730791), 3: (0.454384, 0.730187), 4: (0.360206, 0.729553),
	5: (0.58231, 0.759737), 6: (0.494536, 0.759368), 7: (0.409546, 0.759336), 8: (0.321939, 0.759222),
	10: (0.859482, 0.778505), 11: (0.75264, 0.665909), 12: (0.144621, 0.667519), 13: (0.449279, 0.861075),
	14: (0.542474, 0.564918), 15: (0.461093, 0.621125), 16: (0.494963, 0.704246), 17: (0.369633, 0.275628),
	18: (0.360387, 0.25134), 19: (0.571914, 0.192824), 20: (0.751493, 0.519726), 21: (0.725137, 0.550884),
	22: (0.706553, 0.568561), 23: (0.757839, 0.632066), 24: (0.732062, 0.607041), 25: (0.2196, 0.384226),
	26: (0.353337, 0.369928), 27: (0.673382, 0.272063), 28: (0.444984, 0.32685), 29: (0.441293, 0.301811),
	30: (0.513906, 0.050682), 31: (0.607826, 0.052308), 32: (0.704941, 0.051555), 33: (0.042533, 0.777038),
	34: (0.850927, 0.355072), 35: (0.205237, 0.461665), 36: (0.197289, 0.439011), 37: (0.326376, 0.448438),
	38: (0.316071, 0.427939), 39: (0.260921, 0.314152), 41: (0.778041, 0.188931),
	42: (0.338315, 0.221477), 43: (0.179522, 0.406448), 44: (0.866124, 0.649943), 45: (0.209462, 0.518249),
	46: (0.193035, 0.534238), 47: (0.162074, 0.553061), 48: (0.132405, 0.580335), 49: (0.198968, 0.146886),
	50: (0.2067, 0.242225), 51: (0.246607, 0.240959), 52: (0.676626, 0.451335), 53: (0.649747, 0.43774),
	54: (0.62129, 0.424488), 55: (0.571143, 0.413991), 56: (0.538857, 0.390435), 59: (0.42615, 0.258586),
	60: (0.280484, 0.40339), 61: (0.318379, 0.39879), 62: (0.852456, 0.671388), 63: (0.054425, 0.672567),
	65: (0.471888, 0.508414), 66: (0.494355, 0.481241), 67: (0.508614, 0.455635), 68: (0.530778, 0.43391),
	69: (0.349051, 0.074538),
}

# One bulb-mesh light per distinct position of the retained GI collection (each position also carries a
# second glow light without a mesh, which is not counted).
GI_POSITIONS = [
	(0.795662, 0.017562), (0.100723, 0.047076), (0.233263, 0.07284), (0.05029, 0.076888), (0.40824, 0.084919),
	(0.748115, 0.096502), (0.654372, 0.097358), (0.561123, 0.097463), (0.467036, 0.097731), (0.776563, 0.129688),
	(0.874419, 0.16161), (0.264841, 0.183585), (0.120159, 0.194464), (0.845869, 0.240306), (0.175252, 0.255638),
	(0.862271, 0.293027), (0.192964, 0.322873), (0.63507, 0.332974), (0.84909, 0.353637), (0.617687, 0.366668),
	(0.654821, 0.379869), (0.889964, 0.408134), (0.112602, 0.445919), (0.875197, 0.471587), (0.104207, 0.505734),
	(0.054263, 0.543626), (0.830017, 0.590748), (0.066698, 0.603774), (0.884012, 0.606084), (0.72428, 0.719937),
	(0.181562, 0.721), (0.694467, 0.761375), (0.210189, 0.762663), (0.808619, 0.780007), (0.097063, 0.781616),
	(0.690637, 0.82444), (0.21412, 0.824628),
]

# Addresses the superseded legacy-migrated record (legacy.game.goldeneye, a VBScript-parser import) carried,
# kept as numeric and zero-padded vpe-legacy aliases while legacy consumers still resolve them. The legacy
# record exposed the G.I. relay as lamp 0.
LEGACY_SWITCHES = {
	1, 3, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 39, 40,
	41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
}
LEGACY_LAMPS = {
	0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
	32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61,
	62, 63, 65, 66, 67, 68, 69,
}
LEGACY_COILS = {1, 2, 4, 8, 14, 17, 18, 20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 48}


def legacy_aliases(namespace: str, address: int, addresses: set[int]) -> list[dict[str, str]]:
	if address not in addresses:
		return []
	values = list(dict.fromkeys([str(address), "%02d" % address, "%03d" % address]))
	return [{"namespace": namespace, "value": value} for value in values]


# Lamps the turbo pop bumper sockets carry; the bulb page restricts those sockets to #555 bulbs.
TURBO_BUMPER_LAMPS = {19, 27, 41}
BULB_CONFLICT = "conflict.bulb-types"
# Flash lamps FLAMP 1-3, whose playfield sockets the flash lamp chart prints as #906.
FLASHER_906_ADDRESSES = {25, 26, 27}
PLAYFIELD_LAMP_BULB_NOTE = (
	" The lamp grid prints '#44 Bulb' in this cell, as it does in every populated cell. The playfield bulb pages "
	"list both 94 #44 bayonet bulbs and 54 #555 wedge bulbs, and the playfield boards page says the eight light "
	"boards (L1-L8) use #555 bulbs without saying which lamps sit on them, so this lamp's bulb type is disputed "
	"(see conflict.bulb-types)."
)
# Lamps whose printed name matches a ramp assembly that lists a #555 bulb. The name match is an inference: the
# assembly pages name the part, not the lamp address.
RAMP_ASSEMBLY_555_LAMPS = {
	49: "the Right Plastic Ramp's Helicopter Assembly 500-6074-00 (printed 83), which lists a #555 wedge bulb in a laydown wedge base L/R black socket",
	60: "the Center Plastic Ramp's 'Lock Ball' sign (item 6G, printed 84), which lists two #555 wedge bulbs",
	61: "the Center Plastic Ramp's 'Lock Ball' sign (item 6G, printed 84), which lists two #555 wedge bulbs",
	69: "the Center Plastic Ramp's Spot Light Assembly 500-5818-02 (printed 84), which lists a #555 wedge bulb behind a reflector",
}

def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _text_sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"GoldenEye retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained GoldenEye extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"GoldenEye retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"GoldenEye retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"GoldenEye retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "observed") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": provenance(*source_refs, status=status),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# (excerpt id suffix, transcription file, locator, image derivation)
MANUAL_EXCERPTS = (
	("fuse-chart", "fuse-chart.md", "PDF page 3, Find-It-In-Front page i, QUICK REFERENCE FUSE CHART", "Sega_1996_Goldeneye_Manual.pdf page 3, crop box 0.095,0.525,0.53,0.908, scanned page rendered at its native resolution (embedded image xref 10, 2496px across 8.32in), rendered at 180 dpi, capped to 650px wide, grayscale, 651x808 WebP quality 80"),
	("dip-switch-settings", "dip-switch-settings.md", "PDF page 4, Find-It-In-Front page ii, CPU DIP SWITCH SETTINGS, LOC. SW300", "Sega_1996_Goldeneye_Manual.pdf page 4, crop box 0.09,0.448,0.96,0.722, scanned page rendered at its native resolution (embedded image xref 15, 2496px across 8.32in), rendered at 152 dpi, capped to 1100px wide, grayscale, 1101x490 WebP quality 80"),
	("lamp-matrix-grid-1", "lamp-matrix-grid.md", "PDF page 5, Find-It-In-Front page iii, LAMP MATRIX GRID rows 1-5", "Sega_1996_Goldeneye_Manual.pdf page 5, crop box 0.1,0.528,0.965,0.752, scanned page rendered at its native resolution (embedded image xref 20, 2496px across 8.32in), rendered at 139 dpi, capped to 1000px wide, grayscale, 1001x367 WebP quality 80"),
	("lamp-matrix-grid-2", "lamp-matrix-grid.md", "PDF page 5, Find-It-In-Front page iii, LAMP MATRIX GRID rows 5-10", "Sega_1996_Goldeneye_Manual.pdf page 5, crop box 0.1,0.748,0.965,0.938, scanned page rendered at its native resolution (embedded image xref 20, 2496px across 8.32in), rendered at 167 dpi, capped to 1200px wide, grayscale, 1201x373 WebP quality 80"),
	("flash-lamps-chart", "flash-lamps-chart.md", "PDF page 7, Find-It-In-Front page v, Flash Lamps (FLAMP) and Aux. Data Line", "Sega_1996_Goldeneye_Manual.pdf page 7, crop box 0.09,0.135,0.955,0.595, scanned page rendered at its native resolution (embedded image xref 30, 2496px across 8.32in), rendered at 125 dpi, capped to 900px wide, grayscale, 901x676 WebP quality 80"),
	("switch-matrix-grid", "switch-matrix-grid.md", "PDF page 32, printed page 20, SWITCH MATRIX GRID and Dedicated Switches", "Sega_1996_Goldeneye_Manual.pdf page 32, crop box 0.11,0.585,0.985,0.9, scanned page rendered at its native resolution (embedded image xref 155, 2496px across 8.32in), rendered at 124 dpi, capped to 900px wide, grayscale, 901x458 WebP quality 80"),
	("switch-matrix-descriptions-1", "switch-matrix-descriptions.md", "PDF page 33, printed page 21, Switch Matrix Descriptions rows 1-22", "Sega_1996_Goldeneye_Manual.pdf page 33, crop box 0.515,0.118,0.97,0.39, scanned page rendered at its native resolution (embedded image xref 160, 2496px across 8.32in), rendered at 198 dpi, capped to 750px wide, grayscale, 751x633 WebP quality 80"),
	("switch-matrix-descriptions-2", "switch-matrix-descriptions.md", "PDF page 33, printed page 21, Switch Matrix Descriptions rows 22-44", "Sega_1996_Goldeneye_Manual.pdf page 33, crop box 0.515,0.385,0.97,0.63, scanned page rendered at its native resolution (embedded image xref 160, 2496px across 8.32in), rendered at 211 dpi, capped to 800px wide, grayscale, 801x609 WebP quality 80"),
	("switch-matrix-descriptions-3", "switch-matrix-descriptions.md", "PDF page 33, printed page 21, Switch Matrix Descriptions rows 44-64", "Sega_1996_Goldeneye_Manual.pdf page 33, crop box 0.515,0.625,0.97,0.878, scanned page rendered at its native resolution (embedded image xref 160, 2496px across 8.32in), rendered at 225 dpi, capped to 850px wide, grayscale, 851x668 WebP quality 80"),
	("backbox-insert-flash-lamp-locations", "backbox-insert-flash-lamp-locations.md", "PDF page 34, printed page 22, Backbox Insert Flash Lamp Locations", "Sega_1996_Goldeneye_Manual.pdf page 34, crop box 0.1,0.44,0.985,0.9, scanned page rendered at its native resolution (embedded image xref 165, 2496px across 8.32in), rendered at 122 dpi, capped to 900px wide, grayscale, 901x660 WebP quality 80"),
	("playfield-coil-and-flash-lamp-tables", "playfield-coil-and-flash-lamp-tables.md", "PDF page 35, printed page 23, Playfield Coil and Flash Lamp Locations tables", "Sega_1996_Goldeneye_Manual.pdf page 35, crop box 0.1,0.58,0.97,0.91, scanned page rendered at its native resolution (embedded image xref 170, 2496px across 8.32in), rendered at 124 dpi, capped to 900px wide, grayscale, 901x482 WebP quality 80"),
	("coils-detailed-chart-1", "coils-detailed-chart.md", "PDF page 36, printed page 24, COILS DETAILED CHART TABLE, High Current Coils Group 1", "Sega_1996_Goldeneye_Manual.pdf page 36, crop box 0.085,0.084,0.985,0.268, scanned page rendered at its native resolution (embedded image xref 175, 2496px across 8.32in), rendered at 160 dpi, capped to 1200px wide, grayscale, 1201x347 WebP quality 80"),
	("coils-detailed-chart-2", "coils-detailed-chart.md", "PDF page 36, printed page 24, COILS DETAILED CHART TABLE, High Current Coils Group 2", "Sega_1996_Goldeneye_Manual.pdf page 36, crop box 0.085,0.283,0.985,0.464, scanned page rendered at its native resolution (embedded image xref 175, 2496px across 8.32in), rendered at 174 dpi, capped to 1300px wide, grayscale, 1301x370 WebP quality 80"),
	("coils-detailed-chart-3", "coils-detailed-chart.md", "PDF page 36, printed page 24, COILS DETAILED CHART TABLE, Low Current Coils Group 1", "Sega_1996_Goldeneye_Manual.pdf page 36, crop box 0.085,0.478,0.985,0.67, scanned page rendered at its native resolution (embedded image xref 175, 2496px across 8.32in), rendered at 174 dpi, capped to 1300px wide, grayscale, 1301x392 WebP quality 80"),
	("flipper-coils", "flipper-coils.md", "PDF page 36, printed page 24, FLIPPER COILS", "Sega_1996_Goldeneye_Manual.pdf page 36, crop box 0.1,0.8,0.99,0.9, scanned page rendered at its native resolution (embedded image xref 175, 2496px across 8.32in), rendered at 300 dpi, grayscale, 2223x352 WebP quality 80"),
	("backbox-speaker-panel-1", "backbox-speaker-panel.md", "PDF page 48, printed page 54, Backbox - General Parts items 1-17", "Sega_1996_Goldeneye_Manual.pdf page 48, crop box 0.11,0.6,0.545,0.905, scanned page rendered at its native resolution (embedded image xref 235, 2496px across 8.32in), rendered at 193 dpi, capped to 700px wide, grayscale, 701x693 WebP quality 80"),
	("backbox-speaker-panel-2", "backbox-speaker-panel.md", "PDF page 48, printed page 54, Backbox - General Parts items 18-22 (Speaker Panel Assembly)", "Sega_1996_Goldeneye_Manual.pdf page 48, crop box 0.545,0.6,0.985,0.905, scanned page rendered at its native resolution (embedded image xref 235, 2496px across 8.32in), rendered at 178 dpi, capped to 650px wide, grayscale, 651x636 WebP quality 80"),
	("playfield-boards", "playfield-boards.md", "PDF page 58, printed page 64, Playfield - Boards: Light, Magnet Processor / Driver and Auxiliary Relay", "Sega_1996_Goldeneye_Manual.pdf page 58, crop box 0.1,0.78,0.98,0.905, scanned page rendered at its native resolution (embedded image xref 285, 2496px across 8.32in), rendered at 246 dpi, capped to 1800px wide, grayscale, 1801x361 WebP quality 80"),
	("playfield-bulbs-and-sockets-1", "playfield-bulbs-and-sockets.md", "PDF page 59, printed page 65, Playfield - Wedge Base Type Bulbs and Sockets (socket captions)", "Sega_1996_Goldeneye_Manual.pdf page 59, crop box 0.1,0.09,0.97,0.26, scanned page rendered at its native resolution (embedded image xref 290, 2496px across 8.32in), rendered at 300 dpi, grayscale, 2173x600 WebP quality 80"),
	("playfield-bulbs-and-sockets-2", "playfield-bulbs-and-sockets.md", "PDF page 59, printed page 65, Playfield - Wedge Base Type Bulbs and Sockets parts table", "Sega_1996_Goldeneye_Manual.pdf page 59, crop box 0.1,0.775,0.965,0.895, scanned page rendered at its native resolution (embedded image xref 290, 2496px across 8.32in), rendered at 208 dpi, capped to 1500px wide, grayscale, 1501x294 WebP quality 80"),
	("playfield-bulbs-and-sockets-3", "playfield-bulbs-and-sockets.md", "PDF page 60, printed page 66, Playfield - Bayonet Type Bulbs and Sockets parts table", "Sega_1996_Goldeneye_Manual.pdf page 60, crop box 0.1,0.8,0.965,0.9, scanned page rendered at its native resolution (embedded image xref 295, 2496px across 8.32in), rendered at 208 dpi, capped to 1500px wide, grayscale, 1501x245 WebP quality 80"),
	("playfield-bulbs-and-sockets-4", "playfield-bulbs-and-sockets.md", "PDF page 61, printed page 67, Playfield - Large Bayonet Type Bulbs and Sockets parts table", "Sega_1996_Goldeneye_Manual.pdf page 61, crop box 0.09,0.825,0.96,0.892, scanned page rendered at its native resolution (embedded image xref 300, 2496px across 8.32in), rendered at 300 dpi, grayscale, 2173x236 WebP quality 80"),
	("playfield-bulbs-and-sockets-5", "playfield-bulbs-and-sockets.md", "PDF page 59, printed page 65, Playfield - Wedge Base Type Bulbs and Sockets captions of B, 7, 8 and C", "Sega_1996_Goldeneye_Manual.pdf page 59, crop box 0.1,0.535,0.97,0.6, scanned page rendered at its native resolution (embedded image xref 290, 2496px across 8.32in), rendered at 300 dpi, grayscale, 2173x229 WebP quality 80"),
	("playfield-bulbs-and-sockets-6", "playfield-bulbs-and-sockets.md", "PDF page 60, printed page 66, Playfield - Bayonet Type Bulbs and Sockets caption of bulb B (#455)", "Sega_1996_Goldeneye_Manual.pdf page 60, crop box 0.57,0.585,0.97,0.775, scanned page rendered at its native resolution (embedded image xref 295, 2496px across 8.32in), rendered at 270 dpi, capped to 900px wide, grayscale, 901x604 WebP quality 80"),
	("playfield-bulbs-and-sockets-7", "playfield-bulbs-and-sockets.md", "PDF page 59, printed page 65, Playfield - Wedge Base Type Bulbs and Sockets captions of sockets 4-6", "Sega_1996_Goldeneye_Manual.pdf page 59, crop box 0.1,0.315,0.97,0.43, scanned page rendered at its native resolution (embedded image xref 290, 2496px across 8.32in), rendered at 207 dpi, capped to 1500px wide, grayscale, 1501x281 WebP quality 80"),
	("ramp-assembly-bulbs-1", "ramp-assembly-bulbs.md", "PDF page 76, printed page 82, Right Plastic Ramp Assembly item 9 (Entrance Gate & Sign, 'Tank Multiball')", "Sega_1996_Goldeneye_Manual.pdf page 76, crop box 0.55,0.722,1,0.89, scanned page rendered at its native resolution (embedded image xref 375, 2496px across 8.32in), rendered at 300 dpi, grayscale, 1124x592 WebP quality 80"),
	("ramp-assembly-bulbs-2", "ramp-assembly-bulbs.md", "PDF page 77, printed page 83, Right Plastic Ramp Assembly item 23 (Helicopter Assembly)", "Sega_1996_Goldeneye_Manual.pdf page 77, crop box 0.09,0.703,0.535,0.814, scanned page rendered at its native resolution (embedded image xref 380, 2496px across 8.32in), rendered at 300 dpi, grayscale, 1112x392 WebP quality 80"),
	("ramp-assembly-bulbs-3", "ramp-assembly-bulbs.md", "PDF page 78, printed page 84, Center Plastic Ramp Assembly item 6 (Entrance Gate & Sign, 'Lock Ball')", "Sega_1996_Goldeneye_Manual.pdf page 78, crop box 0.545,0.572,0.99,0.742, scanned page rendered at its native resolution (embedded image xref 385, 2496px across 8.32in), rendered at 284 dpi, capped to 1050px wide, grayscale, 1051x567 WebP quality 80"),
	("ramp-assembly-bulbs-4", "ramp-assembly-bulbs.md", "PDF page 78, printed page 84, Center Plastic Ramp Assembly item 12 (Spot Light Assembly)", "Sega_1996_Goldeneye_Manual.pdf page 78, crop box 0.545,0.805,0.99,0.91, scanned page rendered at its native resolution (embedded image xref 385, 2496px across 8.32in), rendered at 300 dpi, grayscale, 1112x371 WebP quality 80"),
	("gun-and-auto-launch-assemblies", "gun-and-auto-launch-assemblies.md", "PDF page 64, printed page 70, \"007\" Gun Assembly and Auto Ball Launch (Shooter Lane) Assembly", "Sega_1996_Goldeneye_Manual.pdf page 64, crop box 0.09,0.05,0.97,0.905, scanned page rendered at its native resolution (embedded image xref 315, 2496px across 8.32in), rendered at 116 dpi, capped to 850px wide, grayscale, 851x1165 WebP quality 80"),
	("trough-assembly-1", "trough-assembly.md", "PDF page 65, printed page 71, 5-Ball Trough Assembly parts items 1-11", "Sega_1996_Goldeneye_Manual.pdf page 65, crop box 0.1,0.51,0.53,0.705, scanned page rendered at its native resolution (embedded image xref 320, 2496px across 8.32in), rendered at 280 dpi, capped to 1000px wide, grayscale, 1001x641 WebP quality 80"),
	("trough-assembly-2", "trough-assembly.md", "PDF page 65, printed page 71, 5-Ball Trough Assembly parts items 11-25", "Sega_1996_Goldeneye_Manual.pdf page 65, crop box 0.1,0.7,0.53,0.9, scanned page rendered at its native resolution (embedded image xref 320, 2496px across 8.32in), rendered at 252 dpi, capped to 900px wide, grayscale, 901x591 WebP quality 80"),
	("trough-assembly-3", "trough-assembly.md", "PDF page 65, printed page 71, Lock Ball Assembly parts items 26-40", "Sega_1996_Goldeneye_Manual.pdf page 65, crop box 0.53,0.68,0.965,0.9, scanned page rendered at its native resolution (embedded image xref 320, 2496px across 8.32in), rendered at 249 dpi, capped to 900px wide, grayscale, 901x642 WebP quality 80"),
	("power-scoop-and-kick-big", "power-scoop-and-kick-big.md", "PDF page 70, printed page 76, Power Scoop Assembly and Kick Big Assembly", "Sega_1996_Goldeneye_Manual.pdf page 70, crop box 0.1,0.06,0.97,0.905, scanned page rendered at its native resolution (embedded image xref 345, 2496px across 8.32in), rendered at 124 dpi, capped to 900px wide, grayscale, 901x1234 WebP quality 80"),
	("tank-trap-door-and-satellite-launch-ramp", "tank-trap-door-and-satellite-launch-ramp.md", "PDF page 71, printed page 77, Tank Trap Door Plunger Assembly and Satellite Launch Ramp Assembly", "Sega_1996_Goldeneye_Manual.pdf page 71, crop box 0.52,0.27,0.97,0.89, scanned page rendered at its native resolution (embedded image xref 350, 2496px across 8.32in), rendered at 147 dpi, capped to 550px wide, grayscale, 551x1070 WebP quality 80"),
	("satellite-assemblies", "satellite-assemblies.md", "PDF pages 72-73, printed pages 78-79, Satellite Assembly and Satellite Motor Base Assembly", "Sega_1996_Goldeneye_Manual.pdf page 73, crop box 0.1,0.74,0.97,0.89, scanned page rendered at its native resolution (embedded image xref 360, 2496px across 8.32in), rendered at 180 dpi, capped to 1300px wide, grayscale, 1301x317 WebP quality 80"),
	("up-down-ramp-assemblies", "up-down-ramp-assemblies.md", "PDF page 74, printed page 80, Up-Down Metal Ramp Plunger and Ramp & Flat Rail Assemblies", "Sega_1996_Goldeneye_Manual.pdf page 74, crop box 0.1,0.25,0.54,0.46, scanned page rendered at its native resolution (embedded image xref 365, 2496px across 8.32in), rendered at 300 dpi, grayscale, 1099x740 WebP quality 80"),
	("back-panel-and-flipper-magnet", "back-panel-and-flipper-magnet.md", "PDF page 79, printed page 85, Back Panel Assembly and Between Flipper Magnet Individual Parts", "Sega_1996_Goldeneye_Manual.pdf page 79, crop box 0.1,0.36,0.98,0.9, scanned page rendered at its native resolution (embedded image xref 390, 2496px across 8.32in), rendered at 205 dpi, capped to 1500px wide, grayscale, 1501x1299 WebP quality 80"),
	("trough-opto-theory", "trough-opto-theory.md", "PDF page 88, printed page 94, Trough Up-Kicker OPTO Theory of Operation & Schematic", "Sega_1996_Goldeneye_Manual.pdf page 88, crop box 0.07,0.11,0.95,0.87, scanned page rendered at its native resolution (embedded image xref 435, 2496px across 8.32in), rendered at 137 dpi, capped to 1000px wide, grayscale, 1001x1219 WebP quality 80"),
)


def _excerpts() -> list[dict[str, Any]]:
	records = []
	for suffix, transcription, locator, derivation in MANUAL_EXCERPTS:
		records.append(
			{
				"id": f"excerpt.goldeneye.{suffix}",
				"locator": locator,
				"path": f"{EXCERPT_PREFIX}/{transcription}",
				"sha256": _text_sha256(EXCERPT_DIRECTORY / transcription),
				"image": f"{EXCERPT_PREFIX}/{suffix}.webp",
				"image_sha256": _file_sha256(EXCERPT_DIRECTORY / f"{suffix}.webp"),
				"image_derivation": derivation,
				"method": "manual",
				"transcribed_by": "curator, read from the native-resolution render",
				"reviewed": True,
			}
		)
	return records


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames record for gldneye",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/segames.c: INITGAME(gldneye,GEN_WS,se_dmd128x32,SE_BOARDID_520_5143_00) expanding to "
				"{FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L), swCol 0, lampCol 2, custSol 0, soundBoard 0, display "
				"SE_BOARDID_520_5143_00} with a zero wpc.invSw mask, and CORE_GAMEDEFNV(gldneye,\"GoldenEye\",1996,\"Sega\","
				"de_mSES1,0); src/wpc/se.h SE_BOARDID_520_5143_00 'GoldenEye & Twister double magnets processor'; src/wpc/se.c "
				"se_solenoid_w (physical Q15/Q16 moved to flipper bits: Q16 -> public 45, Q15 -> public 47), no fast-flip "
				"address for gldneye (public 15 written 0), the 520-5143-00 aux handler (solenoids2 |= auxdata << 4; "
				"physical outputs 33/34 = magnet 1/2 enable, 35 = ASTB processor reset), switch_r returning ~core_getSwCol, "
				"dedswitch_r (dedicated DS-1..DS-5 from the flipper column, DS-6..DS-8 from the coin-door buttons), "
				"coreGlobals.nLamps = 64 + lampCol * 8 = 80, nSolenoids = 50, nGI = 1, and the gldneye output typing of "
				"25-32 as #89 bulbs. src/wpc/core.c core_getAllSol (33-36 from solenoids2 bits 4-7 on Whitestar; 45-48 "
				"lower flippers with the hold state set whenever either winding is) and core_getAllPhysicSols (33-36 from "
				"the physical outputs on Whitestar)."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/whitestar.json",
			"revision": "repository",
			"locator": "Whitestar public switch, DIP, solenoid, lamp and aggregate G.I. address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/sega.goldeneye.1996/Sega_1996_Goldeneye_Manual.pdf",
			"original_filename": "Sega_1996_Goldeneye_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T14:07:06Z",
			"locator": (
				"132-page image-only scan of the Sega Pinball GoldenEye operations manual (Acrobat 5.0 Scan Plug-in, "
				"2003), supplied by the contributor; owner-password protected against copying but not against viewing. "
				"The untouched file is retained under this hash. A decrypted copy with a contributor-made Acrobat OCR text "
				"layer (Sega_1996_Goldeneye_Manual.ocr.pdf, SHA-256 " + MANUAL_OCR_SHA256 + ") is retained beside it "
				"for text search only. Find-It-In-Front pages i-v (fuse chart, DIP settings, switch and lamp grids, coil "
				"and flash-lamp charts); Section 3 printed 20-24 (switch grid and descriptions, backbox and playfield "
				"flash-lamp locations, coils detailed chart, flipper coils); Section 4 printed 54, 64-67, 70-71, 76-80 and 82-85 "
				"(parts, bulbs and sockets, and assemblies); Section 5 printed 94 (trough up-kicker opto). The playfield location drawings "
				"survive only as outlines: none of their callout numbers is legible in this scan."
			),
			"license": "NOASSERTION",
			"attribution": "Sega Pinball, Inc.; scan supplied by the contributor",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/sega/goldeneye-1996/source/Goldeneye%20(Sega%201996)%20VPW%201.2.1.vpx",
			"original_filename": "Goldeneye (Sega 1996) VPW 1.2.1.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW GoldenEye 1.2.1 (project lead Astronasty; based on the JPJ/32Assassin/Pingod/"
				f"UncleReamus/Destruk/The Trout tables), VPX 10.8, table version 1.2. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/952 and y/2162. Geometry for named table objects only."
			),
			"license": "NOASSERTION",
			"attribution": "VPW (Astronasty, Fluffhead35, Apophis, Oqqsan and team); JPJ, 32Assassin, Pingod, UncleReamus, Destruk, The Trout",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/sega/goldeneye-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script of the retained table (141,075 bytes): cGameName = "gldneye", UseVPMModSol = 2, UseLamps = 1, '
				'HandleMechanics = 0, LoadVPM "03060000","SEGA2.VBS"; bsTrough on switches 14-10 ejecting through solenoid 1; '
				"bsPlunger on 16 (solenoid 2), bsScoop on 50 (solenoid 4), bsTank on 56 (solenoid 14, trap door solenoid 22); "
				"SolLockOut (17) pulses 15; SolCallback 18/20/21/33/34 drive the up-down ramp, satellite launch ramp, satellite "
				"motor, satellite magnet and flipper magnet; SolModCallback 25-32 flashers; RotRadar raises switch 20 near the "
				"dish's home angle; RadarKicker holds 23 closed while a ball sits on the satellite magnet; the flipper magnet "
				"pulses 24 when it releases a ball; SolLFlipper/SolRFlipper on 48/46 fire the flippers only while enabled and "
				"write 63/64; vpmMapLights AllLamps; GIUpdates2 drives the whole GI collection from G.I. channel 0."
			),
			"license": "NOASSERTION",
			"attribution": "VPW GoldenEye team; JPJ, 32Assassin and earlier authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/sega/goldeneye-1996/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPW_CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/Goldeneye%20%28Sega%201996%29%20VPW%201.2.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": VPW_CORPUS_SCRIPT_SHA256,
			"locator": (
				"Goldeneye (Sega 1996) VPW 1.2.vbs (141,010 bytes), the released VPW 1.2 script of the same table: the same "
				"SolCallback, switch and lamp bindings as the retained 1.2.1 script. Ignoring whitespace, 1.2.1 differs only in "
				"flipper activation (it fires a flipper only while its key is held), in dropping 1.2's LockBarKey as a second "
				"key for the Fire Button switch 9, in commenting out the bsScoop/bsTank/bsPlunger InitExitSnd lines, in a debug "
				"print, and in the corpus copy's Thalamus AudioFade/AudioPan patch. Script only."
			),
			"license": "NOASSERTION",
			"attribution": "VPW GoldenEye team; corpus by sverrewl",
			"rights": "NOASSERTION",
		},
		{
			"id": DOZER_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/Goldeneye%20VPX%20%28Sega%201996%29_Dozer_2.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": DOZER_SCRIPT_SHA256,
			"locator": (
				"Goldeneye VPX (Sega 1996)_Dozer_2.vbs (25,404 bytes), an independent table lineage by Dozer: the same "
				"SolCallback table for 1, 2, 4, 8, 14, 17, 18, 20-22, 25-34 (22 = Tank_Trapdoor, 33 = SatMag_Sol, 34 = "
				"FlipMag_Sol); switch 23 held closed while a ball is held on the satellite magnet and pulsed when one "
				"passes it unpowered, switch 24 closed while a ball sits on the flipper magnet, switch 20 closed at the "
				"dish's home angle; bsTrough on 14-10 and SolLockOut pulsing 15. Script only."
			),
			"license": "NOASSERTION",
			"attribution": "Dozer; corpus by sverrewl",
			"rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/goldeneye/vpm-script-libs/sega2.vbs",
			"original_filename": "sega2.vbs",
			"sha256": SEGA2_VBS_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads (last updated in VBS v3.56): 'GoldenEye and Apollo13 "
				"use different flipper techinques and switch locations than other Sega games'; swLRFlip = 64, swLLFlip = 63 "
				"(the flipper keys write these matrix switches), GameOnSolenoid = 48 with UseSolenoids = 2, and cabinet "
				"constants swStartButton = 3, swTilt = 1, swSlamTilt = 8, swCoin1/2/3 = 5/6/4, swRed/swGreen/swBlack = -2/-1/0, "
				"swMemoryProtect = -3. The companion core.vbs (SHA-256 " + CORE_VBS_SHA256 + ", retained beside it) defines "
				"sLRFlipper = 46 and sLLFlipper = 48."
			),
			"license": "NOASSERTION",
			"attribution": "Visual PinMAME script library contributors",
			"rights": "NOASSERTION",
		},
		{
			"id": RUNTIME_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_PATH}",
			"revision": PINMAME_REVISION,
			"locator": (
				"Seven hash-pinned LibPinMAME harness runs of gldneye from empty NVRAM with five balls on trough switches "
				"10-14 (scenarios tools/harness-scenarios/whitestar/gldneye-*.json). With Satellite Home 20 at 0 the ROM "
				"runs the satellite motor relay (21) for about 13.8 s after power-up and gives up; with 20 at 1 from boot "
				"it never runs it; raising 20 while it runs releases 21 about 0.11 s later. After coins and Start the ROM "
				"fires the lock-ball coil (17); raising only the VUK opto 15 draws the trough up-kicker (1) about 0.25 s "
				"later and releasing only trough switch 14 about 0.81 s later, while changing neither shows only the ROM's "
				"retry cycle (17 five times, then the auto launch 2 and up-kicker 1, repeated); about 14.8 s after the shooter lane 16 closes the ROM raises the "
				"flipper enables 45-48 together and holds them; the Fire Button 9 draws the auto launch (2) and the flipper "
				"magnet (34); each coin pulses the coin meter (24)."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
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


def _matrix_position(address: int) -> tuple[int, int]:
	column, row = divmod(address - 1, 8)
	return column + 1, row + 1


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = _matrix_position(address)
	transistor, drive_wire, drive_connection = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "CPU/Sound Board",
		"driver_transistor": transistor,
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
	}


def _switch_notes(address: int) -> str:
	column, row = _matrix_position(address)
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	if address in {1, 2, 4, 5, 6, 7, 63, 64}:
		notes += " The switch list marks it with the asterisk for switches located in the cabinet."
	if address == 1:
		notes += " The part cell refers to Section 4, Chapter 1."
	if address == 2:
		notes += " The part cell is printed as dashes; the fourth coin slot is an optional coin-door position."
	if address == 3:
		notes += " Printed 'START BUTTON (Left of Coin Door) RED'; lamp 57 lights it."
	if address == 5:
		notes += " Printed 'CENTER COIN SLOT / DBA', the dollar bill acceptor position."
	if address == 7:
		notes += (
			" The retained table writes this address from the slam key itself; its sega2.vbs library also writes "
			"swSlamTilt = 8, a matrix position the manual prints Not Used."
		)
	if address == 9:
		notes += (
			" The trigger microswitch of the cabinet \"007\" Gun Assembly 500-5698-01 (item 5, 180-5111-00). The "
			"retained script writes it from the plunger key; the harness shows the ROM firing the auto launch (2) "
			"about 0.08 s after it closes with a ball in the shooter lane."
		)
	if 10 <= address <= 14:
		notes += (
			" One of five subminiature roller switches (item 3, 180-5119-00, with a 1N4001 switch diode) along the "
			"5-Ball Trough (OPTO) Assembly 500-5989-05-42; #1 is at the left, #5 at the right beside the up-kicker. "
			"A plain contact, closed while a ball rests on it."
		)
	if address == 15:
		notes += (
			" The 520-5124-00 transmitter / 520-5125-00 receiver opto pair on the trough up-kicker. The manual's "
			"theory of operation (printed 94) says the receiver acts as an open switch while light reaches it and a "
			"closed switch when the beam is blocked, so the matrix contact rests open and closes with a ball on the "
			"up-kicker. Whitestar's switch_r returns ~core_getSwCol, so public 1 is that closed reading; pinned "
			"PinMAME applies no inversion (the gldneye invSw mask is zero). The harness is consistent with it. As the "
			"ROM fires the lock-ball coil (17), raising only 15 to 1, with trough switch 14 still closed, draws the "
			"up-kicker (1) about 0.25 s later. Releasing only 14 also draws the up-kicker, but about 0.81 s later, and "
			"leaving both alone draws it only in the ROM's retry cycle, about 3.45 s after the first lock-ball pulse. In "
			"both isolation runs the ROM then kicks four more times, whether or not 15 stays at 1, and afterwards "
			"returns to its lock-ball retry cycle if 14 never opened and stops if it did. The retained script pulses 15 from its SolLockOut callback."
		)
	if address == 16:
		notes += " Rollover switch assembly 500-570X-00 in the shooter lane beside the auto-launch kicker."
	if address in {17, 18, 19, 32, 40, 54}:
		notes += " Ramp gate microswitch (180-5087-00); the retained script pulses it from its gate object's Hit event."
	if address == 20:
		notes += (
			" Item 7 'Switch (Motor Cam)' 180-5052-00 of the Satellite Motor Base Assembly 500-5982-00-42, cabled as "
			"item 15 'Switch Cable (Sw. 20 Home)'. The harness shows public 1 is home: with 20 at 0 the ROM runs the "
			"satellite motor relay (21) at power-up for about 13.8 s and gives up, with 20 held at 1 it never runs it, "
			"and raising 20 while the motor runs releases the relay about 0.11 s later. Both retained scripts close it "
			"near the dish's home angle."
		)
	if address == 23:
		notes += (
			" Not a mechanical switch: printed 'SATELLITE MAGNET BOARD' with the part cell 'See Magnet Board Layout'. "
			"The M1 Magnet Processor / Driver Board 520-5143-00 senses a ball on the satellite magnet and reports it "
			"here (pinned PinMAME: 'drive magnet but also perform ball detection and report it on the switch matrix'). "
			"Both retained scripts hold it at 1 while a ball is held on the satellite magnet; the Dozer script also "
			"pulses it when a ball passes the unpowered magnet."
		)
	if address == 24:
		notes += (
			" Not a mechanical switch: printed 'FLIPPER MAGNET BOARD'; the M1 Magnet Processor / Driver Board "
			"520-5143-00 reports a ball on the magnet between the flippers. The Dozer script holds it at 1 while a "
			"ball sits on the flipper magnet; the VPW script only pulses it when the magnet releases a ball."
		)
	if address in {25, 26, 27, 28, 30, 31, 33, 34, 39, 44, 45, 46, 47, 48}:
		notes += " Stand-up target assembly (515-5162-00 or 515-5967-00); the retained script pulses it from the target's Hit event."
	if address in {25, 26, 27, 28}:
		notes += " The manual names this bank the left 5-bank, but it prints only four switches for it (25-28) and the table models four targets."
	if address in {41, 42, 43}:
		notes += " Turbo bumper skirt switch (180-5015-03); the retained script pulses it from the bumper's Hit event."
	if address == 50:
		notes += " Micro switch (180-5057-00) on the Power Scoop Weld Assembly 500-5809-00-42."
	if address in {51, 52, 53, 57, 58, 59, 60}:
		notes += " Rollover switch assembly (500-570X-00); the retained script holds it while its trigger is covered."
	if address == 55:
		notes += " The part cell reads 'Verify'; the retained script holds it while its SW55 trigger is covered."
	if address == 56:
		notes += (
			" The part cell reads 'Verify'. The retained script uses 56 as its tank lock switch (bsTank), closed while a "
			"ball waits in the tank for the tank kicker (14)."
		)
	if address in {61, 62}:
		notes += " Slingshot kicker switch (180-5054-00); the retained script pulses it from the slingshot wall's Slingshot event."
	if address in {63, 64}:
		side, transistor = ("left", "Q7") if address == 63 else ("right", "Q5")
		notes += (
			f" Printed '* {side.upper()} FLIPPER POWER SWITCH BUTTON VIA {transistor} ON THE SSFB' (180-5122-00). The "
			f"cabinet {side} flipper button is wired to the 2-Flipper Solid State Flipper Board (520-5080-00), which "
			"fires the flipper coil itself and reports the button to the CPU through this matrix position (the "
			"flipper coil table prints the switch drive GRN-GRY and the returns WHT-VIO/WHT-GRY through the SSFB). "
			"The retained sega2.vbs library writes it from the flipper key (swLLFlip = 63, swLRFlip = 64). Unlike other "
			"Whitestar games, GoldenEye's flipper buttons are not on the dedicated DS inputs (public 81-84)."
		)
	if address in SWITCH_PROJECTIONS:
		notes += " " + SWITCH_PROJECTIONS[address]
	elif address in SWITCH_OBJECTS:
		notes += f" Placement: retained table object {SWITCH_OBJECTS[address]}."
	return notes


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	items.append(
		_device(
			"switch.memory-protect", "Memory Protect", "switch", "pinmame.input.switch", -3, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": "-3"}],
			normally_closed=False,
			roles=["service.memory-protect"],
			physical={
				"location": "coin door",
				"switch_type": "button",
				"notes": (
					"PinMAME public -3. The manual's cabinet drawing (page i) labels the 'Memory Protect & Coil Power "
					"Interlock Switches' on the coin door, and its diagnostic aids say opening the coin door opens the "
					"memory protect switch. The retained sega2.vbs library binds it to the coin-door key."
				),
			},
			spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE, CONTROLLER_SOURCE),
		)
	)
	for address, (printed, wire, connection, label, role, note) in DEDICATED_SWITCHES.items():
		items.append(
			_device(
				f"switch.dedicated-{printed.lower()}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
				normally_closed=False,
				roles=[role],
				physical={
					"location": "coin door",
					"switch_type": "button",
					"notes": f"Printed dedicated switch {printed} ({wire}, {connection}, into IC U206; ground BLK CN6-1). {note}",
				},
				wiring={"board": "CPU/Sound Board", "drive_wire": wire, "drive_connection": connection, "return_component": "U206"},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for address in range(1, 65):
		column, row = _matrix_position(address)
		identifier = f"switch.matrix-{address}"
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
			+ legacy_aliases("vpe-legacy.switch", address, LEGACY_SWITCHES),
			"wiring": _switch_wiring(address),
		}
		if address in UNUSED_MATRIX_ADDRESSES:
			notes = f"Printed switch-matrix drive column {column}, return row {row}. The printed grid and the switch list both mark this position Not Used."
			if address == 8:
				notes += " The retained sega2.vbs library's swSlamTilt constant points here; the manual puts the slam tilt at 7."
			if address == 49:
				notes += (
					" The retained table nevertheless binds a rollover trigger SW49 beside the left slingshot to this "
					"address; the manual prints no switch there."
				)
			extra["physical"] = {"notes": notes}
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE), **extra))
			continue
		label, switch_type, part, location, roles = SWITCHES[address]
		physical: dict[str, Any] = {"switch_type": switch_type, "notes": _switch_notes(address)}
		if part:
			physical["part_number"] = part
		if address in {23, 24}:
			physical["assembly_part_number"] = "520-5143-00"
		if address == 9:
			physical["assembly_part_number"] = "500-5698-01"
		if 10 <= address <= 15:
			physical["assembly_part_number"] = "500-5989-05-42"
		if address == 20:
			physical["assembly_part_number"] = "500-5982-00-42"
		if address == 50:
			physical["assembly_part_number"] = "500-5809-00-42"
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		if address in {15, 20}:
			refs = refs + (RUNTIME_SOURCE,)
		if address in {9, 16}:
			refs = refs + (RUNTIME_SOURCE,)
		if address in {23, 24, 20}:
			refs = refs + (DOZER_SCRIPT_SOURCE,)
		if address in {7, 63, 64}:
			refs = refs + (VPM_LIBRARY_SOURCE,)
		extra["normally_closed"] = False
		extra["physical"] = physical
		if address in PULSED_SWITCHES:
			extra["pulse"] = True
		if roles:
			extra["roles"] = roles
		availability = "optional" if address == 2 else "used"
		if location == "cabinet":
			physical["location"] = "coin door" if address in {2, 4, 5, 6} else "cabinet"
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			physical["location"] = "below playfield" if address in {10, 11, 12, 13, 14, 15, 20, 23, 24} else "playfield"
			coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address]], *coordinate_refs)
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	for address, (printed, wire, connection, meaning) in UNUSED_DEDICATED.items():
		if address in SYNTHETIC_EOS_INPUTS:
			side, winding = SYNTHETIC_EOS_INPUTS[address]
			items.append(
				_device(
					f"switch.flipper-column-{address}", f"Synthetic {side} Flipper End-of-Stroke", "virtual", "pinmame.input.switch", address, "used",
					(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
					aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
					roles=["internal.synthetic-flipper"],
					physical={
						"notes": (
							f"Written by PinMAME, not by a host. gldneye declares FLIP_SOL(FLIP_L), and FLIP_SOL implies FLIP_EOS, so "
							f"core.c's core_updateSw rewrites this {meaning} bit every frame: it reads 1 once public {winding} has "
							"been on for CORE_FLIPSTROKETIME frames and 0 otherwise. Because GoldenEye's 45-48 are flipper enables "
							"that the ROM holds for the whole of play, this input reads 1 throughout play. se.c's dedswitch_r "
							f"passes it to the ROM as dedicated input {printed} ({wire}, {connection}), which GoldenEye's dedicated "
							"switch table prints NOT USED: the flippers' physical end-of-stroke switches are wired to the Solid State "
							"Flipper Board (BRN-VIO to CN1-1 on the right, BRN-GRY to CN1-9 on the left), not to the CPU, and the "
							"flipper buttons reach the CPU through matrix switches 63 and 64. Any value a host writes here is overwritten on the next "
							"frame, so a recreation must not drive it."
						)
					},
					wiring={"board": "CPU/Sound Board", "drive_wire": wire, "drive_connection": connection, "return_component": "U206"},
					spatial=not_applicable("virtual", CORE_SOURCE, MANUAL_SOURCE),
				)
			)
			continue
		items.append(
			_device(
				f"switch.flipper-column-{address}", f"Not Used Dedicated Input {printed}", "switch", "pinmame.input.switch", address, "unused",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
				physical={
					"notes": (
						f"PinMAME's generic {meaning} position, which se.c's dedswitch_r reads as dedicated input {printed} "
						f"({wire}, {connection}). GoldenEye's dedicated switch table prints {printed} NOT USED: its flipper "
						"buttons reach the CPU through matrix switches 63 and 64 instead. Under LibPinMAME, core_updateSw "
						"leaves whatever a host writes here unchanged, and nothing else writes it."
					)
				},
				wiring={"board": "CPU/Sound Board", "drive_wire": wire, "drive_connection": connection, "return_component": "U206"},
				spatial=not_applicable("unused", MANUAL_SOURCE),
			)
		)
	for address in (85, 86, 87):
		items.append(
			_device(
				f"switch.flipper-column-{address}", f"Unused Flipper-Column Input {address}", "switch", "pinmame.input.switch", address, "unused",
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				physical={"notes": "Generic flipper-column hole on Whitestar; no dedicated input reads it."},
				spatial=not_applicable("unused", CONTROLLER_SOURCE),
			)
		)

	used_dips = {1, 2, 3, 4}
	for address in range(1, 9):
		note = (
			f"CPU DIP switch bank SW300 on the CPU/Sound Board, position {address}. "
			+ (
				"The printed country chart (page ii) sets positions 1-4 to select the USA (all off), Austria, Belgium, "
				"Canada, England, France, Germany, Holland, Italy, Japan, Norway, Sweden or Switzerland; every other "
				"country uses the USA setting."
				if address in used_dips
				else "No printed country setting turns positions 5-8 on; PinMAME publishes the full eight-address bank regardless."
			)
		)
		items.append(
			_device(
				f"dip.sw300-{address}", f"SW300 Position {address}", "dip_switch", "pinmame.input.dip", address,
				"used" if address in used_dips else "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={"location": "CPU/Sound Board", "switch_type": "dip", "notes": note},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE, CONTROLLER_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return "device." + "".join(character if character.isalnum() else "-" for character in label.lower()).replace("--", "-").strip("-")


def _solenoid_notes(address: int) -> str:
	notes = f"Printed coils detailed chart entry #{address}."
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
	if address in {9, 10, 11, 12, 13}:
		notes += " The retained script binds no callback; the table's own bumper/slingshot physics fire on contact and pulse the switch."
	if address == 1:
		notes += (
			" The up-kicker (VUK) coil of the 5-Ball Trough (OPTO) Assembly 500-5989-05-42 (item 8, 23-800), under the "
			"opto 15. In the harness the ROM fires it about 0.25 s after only the VUK opto reports a ball, about 0.81 "
			"s after only trough switch 14 opens, and, with neither, only in its retry cycle about 3.45 s after the "
			"first lock-ball pulse. The retained table ejects the trough ball through it."
		)
	if address == 2:
		notes += (
			" The Auto Ball Launch (Shooter Lane) Assembly 500-5477-01-42 (24-940) at the foot of the shooter lane. The "
			"harness shows the ROM firing it when the cabinet Fire Button (9) closes with a ball on the shooter lane "
			"switch (16), and retrying while 16 stays closed."
		)
	if address == 4:
		notes += (
			" Printed 'POWER SCOOP'; the coil is the 23-800 of the Kick Big Assembly 500-5862-00-42, which the manual "
			"says works in conjunction with the Power Scoop Assembly (switch 50). The Kick Big parts list prints the "
			"coil as 090-5001-01; this chart prints 090-5000-01, which is recorded."
		)
	if address == 8:
		notes += (
			" Printed '(OPTIONAL REPLAY KNOCKER DRIVE LINE)' (page 23: EXTERNAL REPLAY KNOCKER DRIVE LINE) with no coil "
			"(N/A) and listed among the coils not used: the driver drives an external replay knocker only when one is "
			"fitted."
		)
	if address == 14:
		notes += " Kicks balls out of the tank lock (switch 56); the retained script's bsTank ejects them through TankKickBig."
	if address == 17:
		notes += (
			" The 25-1240 coil of the Lock Ball Assembly 500-5684-01 mounted on the 5-ball trough (items 23-39): it "
			"releases one ball from the trough onto the up-kicker. The harness shows the ROM pulsing it after Start. In "
			"the negative-control run, where the VUK opto 15 never reports a ball, the ROM pulses it five times about "
			"0.7 s apart, fires the auto launch (2) and up-kicker (1), and repeats that cycle for as long as the run "
			"lasts."
		)
	if address == 18:
		notes += (
			" The 27-1500 coil of the Up-Down Metal Ramp Plunger Assembly 500-6058-00-42 with its lift-ramp plunger and "
			"link, moving the Up-Down Metal Ramp & Flat Rail Assembly 500-6052-00-42. The retained script lowers the ramp "
			"(and switches the ball path to its lowered surfaces) while the coil is energized and restores it when "
			"released."
		)
	if address == 20:
		notes += (
			" The coil of the Satellite Launch Ramp Assembly 500-6004-00-42 (Lift Ramp Plunger Assembly, item 2, coil "
			"printed 'xx-xxxx' there and 27-1500 in this chart) raising the Up-Down Ramp Sub-Assembly with its Skill "
			"Shot Flap. The retained script raises the ramp toward the satellite while the coil is energized and lowers "
			"it when released."
		)
	if address == 21:
		notes += (
			" Printed 'SATELLITE MOTOR RELAY' with the part cell '24V DC 10A DPDT': a relay switching the 24v AC 6 RPM "
			"motor of the Satellite Motor Base Assembly 500-5982-00-42, whose crank arm and cam link swing the dish; fuse "
			"F28 protects the 24v AC special relay/motor supply. The playfield board list names an A1 Auxiliary Relay "
			"Board 520-5010-00 without saying which output it serves. The harness shows the ROM running it until the "
			"home switch 20 closes."
		)
	if address == 22:
		notes += (
			" The 27-1500 coil of the Tank Trap Door Plunger Assembly 500-5940-01-42, whose Trap Door (Diverter) Wire "
			"opens a trap door in the wire ramp. The retained script enables its DropRamp1 kicker while the coil is on, "
			"sending a ball on that ramp into the tank lock (switch 56)."
		)
	if address == 24:
		notes += " Printed '(OPTIONAL COIN METER)', a 5v meter 'If required' fed from J16-7. The harness shows the ROM pulsing it with every coin."
	return notes


def _flasher_notes(address: int) -> str:
	label, transistor, wire, connect, quantity, locations, bulbs = FLASHERS[address]
	notes = (
		f"Printed flash lamp FLAMP {address - 24} (coil test #{address}): '{locations}', bulbs {bulbs}; the playfield "
		f"table on printed page 23 lists the same quantities. The quantity counts the {quantity} playfield/back-panel "
		"bulbs; the backbox insert bulbs (drawn on printed page 22) are not placed."
	)
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
	notes += " " + FLASHER_NOTES[address]
	if address == 26:
		notes += " The harness shows the ROM flashing it with every coin."
	if address == 32:
		notes += (
			" In the harness run the ROM started flashing it together with the flipper enables while the ball sat in the "
			"shooter lane, and stopped once the Fire Button launched the ball."
		)
	if address in FLASHER_906_ADDRESSES:
		notes += (
			" The flash lamp chart prints #906 wedge bulbs for this flash lamp's playfield sockets, but the wedge-base bulb "
			"page lists the #906 bulb, the 906 wedge base socket and the 555/906 IDC socket all at quantity 0 ('Items with "
			"0 Qty. are not used in this game'), so which bulb these sockets carry is disputed (see conflict.bulb-types)."
		)
	return notes


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}] + legacy_aliases("vpe-legacy.coil", address, LEGACY_COILS)
		if address in UNUSED_SOLENOIDS:
			transistor, wire, connect, power = UNUSED_SOLENOIDS[address]
			items.append(
				_device(
					f"device.not-used-solenoid-{address}", f"Not Used Solenoid {address}", "coil", "pinmame.output.solenoid", address, "unused",
					(MANUAL_SOURCE, CORE_SOURCE),
					aliases=aliases + [{"namespace": "manual.address", "value": f"#{address}"}],
					physical={"notes": f"Printed #{address} NOT USED in the coils detailed chart (drive transistor {transistor} populated, no coil) and in the page 23 not-used list."},
					wiring={"board": "I/O Power Driver Board", "driver_transistor": transistor, "control_wire": wire, "control_connection": connect},
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		if address in SOLENOIDS:
			label, kind, transistor, wire, connect, power_color, power_connection, voltage, coil = SOLENOIDS[address]
			identifier = output_id(label)
			physical: dict[str, Any] = {"notes": _solenoid_notes(address)}
			if coil and kind == "coil":
				physical["part_number"] = coil
			if address == 1 or address == 17:
				physical["assembly_part_number"] = "500-5989-05-42" if address == 1 else "500-5684-01"
			assemblies = {2: "500-5477-01-42", 4: "500-5862-00-42", 18: "500-6058-00-42", 20: "500-6004-00-42", 21: "500-5982-00-42", 22: "500-5940-01-42"}
			if address in assemblies:
				physical["assembly_part_number"] = assemblies[address]
			wiring = {
				"board": "I/O Power Driver Board",
				"driver_transistor": transistor,
				"control_wire": wire,
				"control_connection": connect,
				"power_wire": power_color,
				"power_connection": f"{power_connection} ({voltage})",
			}
			extra: dict[str, Any] = {"aliases": aliases + [{"namespace": "manual.address", "value": f"#{address}"}], "physical": physical, "wiring": wiring}
			availability = "used"
			if address == 8:
				availability = "optional"
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 24:
				availability = "optional"
				extra["roles"] = ["cabinet.coin-meter"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
				physical["notes"] += f" Placement: retained table object {SOLENOID_OBJECTS[address]}."
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {1, 2, 17, 21, 24}:
				refs = refs + (RUNTIME_SOURCE,)
			if address in {14, 22}:
				refs = refs + (DOZER_SCRIPT_SOURCE,)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue
		if address in FLASHERS:
			label, transistor, wire, connect, quantity, locations, bulbs = FLASHERS[address]
			identifier = output_id(label)
			extra = {
				"aliases": aliases + [{"namespace": "manual.address", "value": f"FLAMP {address - 24}"}],
				"physical": {"quantity": quantity, "notes": _flasher_notes(address)},
				"wiring": {"board": "I/O Power Driver Board", "driver_transistor": transistor, "control_wire": wire, "control_connection": connect, "power_wire": "ORG", "power_connection": "J6-P10 (20v)"},
			}
			if address in FLASHER_POSITIONS:
				extra["spatial"] = located(identifier, "emitter", FLASHER_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE) + ((RUNTIME_SOURCE,) if address in {26, 32} else ())
			device = _device(identifier, label, "flasher", "pinmame.output.solenoid", address, "used", refs, **extra)
			if address in FLASHER_906_ADDRESSES:
				device["provenance"]["status"] = "conflicted"
			items.append(device)
			continue
		items.append(_special_solenoid(address, aliases))
	return items


def _special_solenoid(address: int, aliases: list[dict[str, str]]) -> dict[str, Any]:
	if address in {15, 16}:
		notes = {
			15: (
				"PinMAME's synthetic fast-flip slot. se_solenoid_w removes physical Q15 (Left Flipper Enable) from this "
				"address and publishes it at 47, and se.c configures no fast-flip address for gldneye, so the slot is "
				"written constant zero."
			),
			16: (
				"PinMAME's companion slot to 15. se_solenoid_w masks physical Q16 (Right Flipper Enable) off this address "
				"in every write (sols &= 0xffff3fff) and publishes it at 45; unlike 15, no fast-flip path ever sets it, so "
				"it is constant zero on every Whitestar game."
			),
		}[address]
		return _device(
			f"device.solenoid-{address}-reserved", f"Reserved Solenoid Slot {address}", "virtual", "pinmame.output.solenoid", address, "unused",
			(CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases, roles=["internal.unused-platform-slot"],
			physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
		)
	if address in {33, 34}:
		label = "Satellite Magnet" if address == 33 else "Flipper Magnet"
		identifier = output_id(label)
		board_row = "#1 'Magnet Grab Satellite ???'" if address == 33 else "#2 'Magnet Hold Flippers ???'"
		notes = (
			f"Aux. data line {board_row} on the Magnet Driver (M1 Magnet Processor / Driver Board 520-5143-00, located "
			"under the playfield; control BLUE P4, power YEL-VIO P3 50v, printed with question marks). Pinned PinMAME "
			f"publishes magnet {address - 32} enable here from the magnet board's aux data latch (bit {address - 33}) in "
			"both output modes. "
		)
		if address == 33:
			notes += (
				"The magnet is the 22-600 of the Satellite Assembly 500-6000-00-42 in the satellite dish, fused by a 3A "
				"50v DC Satellite Magnet fuse under the playfield. Both retained scripts hold a ball on the dish while it "
				"is on and release it when it drops."
			)
		else:
			notes += (
				"The magnet is the 22-600 of the Between Flipper Magnet parts, located under the playfield between the "
				"flippers, fused by a 3A 50v DC Flipper Magnet fuse. The harness shows the ROM energizing it for about 5.8 "
				"s when the Fire Button launches a ball; both retained scripts catch and hold a ball over the gap between "
				"the flippers while it is on."
			)
		notes += f" Placement: retained table object {SOLENOID_OBJECTS[address]}."
		refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, DOZER_SCRIPT_SOURCE) + ((RUNTIME_SOURCE,) if address == 34 else ())
		return _device(
			identifier, label, "magnet", "pinmame.output.solenoid", address, "used", refs,
			aliases=aliases + [{"namespace": "manual.address", "value": f"Aux. Data Line #{address - 32}"}],
			physical={"assembly_part_number": "500-6000-00-42" if address == 33 else "515-6141-00", "part_number": "090-5042-01" if address == 33 else "090-5042-00", "notes": notes},
			wiring={"board": "Magnet Processor / Driver Board 520-5143-00", "control_wire": "BLUE", "control_connection": "P4", "power_wire": "YEL-VIO", "power_connection": "P3 (50v)"},
			spatial=located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
		)
	if address == 35:
		return _device(
			"device.magnet-board-latch-bit-2", "Magnet Board Aux Latch Bit 2", "control_signal", "pinmame.output.solenoid", 35, "unknown",
			(CORE_SOURCE, CONTROLLER_SOURCE), aliases=aliases, roles=["internal.magnet-processor"],
			physical={
				"notes": (
					"What this address carries depends on the output mode. In LibPinMAME's default binary mode core_getAllSol "
					"publishes bit 2 of the 520-5143-00 magnet board's aux data latch here (solenoids2 bit 6), and no source "
					"says what the ROM puts in that bit: the manual's aux data line table prints only the two magnets, and no "
					"harness run so far has seen it change. With physical outputs enabled (PWM/modulated solenoid mode, which "
					"the retained table uses) core_getAllPhysicSols instead publishes the board's ASTB strobe ('reset "
					"processor') here. No source ties either reading to a playfield device and no retained script binds it; "
					"its binary-mode meaning is as unknown as 36's."
				)
			},
			spatial=not_applicable("internal_nonvisual", CORE_SOURCE),
		)
	if address == 36:
		return _device(
			"device.magnet-board-latch-bit-3", "Magnet Board Aux Latch Bit 3", "control_signal", "pinmame.output.solenoid", 36, "unknown",
			(CORE_SOURCE, CONTROLLER_SOURCE), aliases=aliases, roles=["internal.magnet-processor"],
			physical={
				"notes": (
					"In LibPinMAME's default binary mode core_getAllSol publishes bit 3 of the 520-5143-00 magnet board's aux "
					"data latch here (solenoids2 bit 7); in physical-output mode nothing writes it. No source says what the "
					"ROM puts in that bit, the manual's aux data line table prints only the two magnets, and no harness run "
					"so far has seen it change, so its meaning is unknown."
				)
			},
			spatial=not_applicable("internal_nonvisual", CORE_SOURCE),
		)
	if 37 <= address <= 44:
		return _device(
			f"device.solenoid-{address}-reserved", f"Reserved Solenoid Slot {address}", "virtual", "pinmame.output.solenoid", address, "unused",
			(CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases, roles=["internal.unused-platform-slot"],
			physical={"notes": "Reserved compatibility hole in the Whitestar public solenoid range; core_getAllSol writes nothing here on Whitestar."},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	if address in {45, 46, 47, 48}:
		side = "Right" if address in {45, 46} else "Left"
		transistor = "Q16" if side == "Right" else "Q15"
		hold = address in {46, 48}
		label = f"{side} Flipper Enable" + (" (Hold View)" if hold else "")
		notes = (
			f"Printed coils detailed chart #{16 if side == 'Right' else 15} '{side.upper()} FLIPPER ENABLE' ({transistor}, "
			f"{'ORG-VIO J9-P9, power BLU-YEL' if side == 'Right' else 'ORG-GRY J9-P8, power GRY-YEL'} J10-4/5 50v, coil "
			"22-1080 090-5032-00). se_solenoid_w moves physical "
			f"{transistor} from public {16 if side == 'Right' else 15} to {45 if side == 'Right' else 47}; core_getAllSol "
			f"reports {46 if side == 'Right' else 48} as set whenever {45 if side == 'Right' else 47} is. "
		)
		notes += (
			"On GoldenEye this is a flipper enable, not a per-flip pulse: the 2-Flipper Solid State Flipper Board fires the "
			"flipper coil from the cabinet button itself (its coil output is printed '50v Q2, Q3' and '8vAC SR1' for the "
			"right flipper, '50v Q2, Q10' and 'SR2' for the left) while the CPU holds the enable. In the harness run the "
			"ROM raised 45, 46, 47 and 48 together and held them; that was the next output change about 14.8 s after the "
			"shooter-lane switch 16 closed, and the run does not show what the ROM waited for in between. The retained "
			"script fires its flipper only while this enable is on and the key is held"
		)
		if address == 45:
			notes += "; it also binds SolCallback(45) to a no-op TiltMod routine."
		elif address == 46:
			notes += " (SolCallback(sLRFlipper), sLRFlipper = 46)."
		elif address == 48:
			notes += " (SolCallback(sLLFlipper), sLLFlipper = 48; sega2.vbs also makes 48 its GameOnSolenoid)."
		else:
			notes += "."
		refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE) + ((VPM_LIBRARY_SOURCE,) if address in {46, 48} else ())
		return _device(
			output_id(label), label, "control_signal", "pinmame.output.solenoid", address, "used", refs,
			aliases=aliases + [{"namespace": "manual.address", "value": f"#{16 if side == 'Right' else 15}"}],
			roles=[f"flipper.lower.{side.lower()}"],
			physical={"notes": notes},
			wiring={"board": "I/O Power Driver Board", "driver_transistor": transistor, "control_wire": "ORG-VIO" if side == "Right" else "ORG-GRY", "control_connection": "J9-P9" if side == "Right" else "J9-P8"},
			spatial=not_applicable("internal_nonvisual", CORE_SOURCE, MANUAL_SOURCE),
		)
	notes = {
		49: "PinMAME's simulator-only ball-shooter channel; GoldenEye has no simulator and launches with solenoid 2.",
		50: "Reserved slot at the top of the Whitestar public solenoid range; gldneye declares no custom solenoids.",
	}[address]
	return _device(
		f"device.solenoid-{address}-reserved", f"Reserved Solenoid Slot {address}", "virtual", "pinmame.output.solenoid", address, "unused",
		(CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases, roles=["internal.unused-platform-slot"],
		physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
	)


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 81):
		row, column = divmod(address - 1, 8)
		row += 1
		column += 1
		column_driver, column_wire, column_connection = LAMP_COLUMN_WIRING[column]
		row_driver, row_wire, row_connection = LAMP_ROW_WIRING[row]
		wiring = {
			"board": "I/O Power Driver Board",
			"drive_wire": column_wire,
			"drive_connection": column_connection,
			"return_wire": row_wire,
			"return_connection": row_connection,
			"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
		}
		identifier = f"lamp.matrix-{address}"
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		aliases += legacy_aliases("vpe-legacy.lamp", address, LEGACY_LAMPS)
		prefix = f"Printed lamp-matrix row {row}, column {column}."
		if address in UNUSED_LAMPS:
			notes = f"{prefix} Printed NOT USED with no bulb."
			if address in {9, 64, 70}:
				notes += (
					" The attract-mode harness runs show the ROM toggling this matrix bit: its attract animation drives "
					"matrix positions whether or not a bulb is fitted, and PinMAME reports matrix bits, not bulbs. The "
					"lamp grid shades the cell and prints no bulb there, so the toggling lights nothing and the address "
					"stays unused for a recreation."
				)
			items.append(
				_device(
					identifier, f"Not Used Lamp {address}", "lamp", "pinmame.output.lamp", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE),
					aliases=aliases, wiring=wiring, physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		notes = prefix + " Printed #44 bulb."
		if address in PRINTED_LAMP_TEXT:
			notes += f" Printed '{PRINTED_LAMP_TEXT[address]}'."
		physical: dict[str, Any] = {"quantity": 1}
		extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring, "physical": physical}
		refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		status = "validated"
		if address == 57:
			notes += " The lamp in the cabinet start button (switch 3)."
			extra["roles"] = ["cabinet.start"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
		elif address in SPEAKER_PANEL_LAMPS:
			notes += (
				" One of the nine lettered GOLDENEYE lamps in the backbox speaker panel: the Goldeneye Speaker Panel "
				"Assembly 500-5995-00-42 lists nine 3-lug stand-up long sockets and nine #44 bulbs under square light "
				"covers. Rows 9 and 10 exist because gldneye declares lampCol 2. The retained table renders them as "
				"backglass lights (L72-L80)."
			)
			extra["roles"] = ["cabinet.backbox"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			# A playfield lamp: the lamp grid's #44 disagrees with the bulb pages (conflict.bulb-types).
			status = "conflicted"
			notes += PLAYFIELD_LAMP_BULB_NOTE
			if address in TURBO_BUMPER_LAMPS:
				notes += (
					" This lamp sits in a turbo bumper cap, and the wedge-base bulb page lists three Turbo Pop Bumper "
					"Sockets (077-5206-00) printed 'Use #555 Bulbs only'."
				)
			if address in RAMP_ASSEMBLY_555_LAMPS:
				notes += (
					f" Its printed name suggests it is {RAMP_ASSEMBLY_555_LAMPS[address]}; that is an inference from the "
					"name, since the assembly pages do not print lamp numbers."
				)
			if address == 58:
				notes += " The retained table models no light for this address, so it is not placed."
			elif address == 40:
				notes += (
					" Not placed: the retained table's LL40 has no bulb light or insert primitive beside it (every other "
					"placed lamp has one), its falloff radius of 130 is wider than any insert light's, and the script "
					"switches it on and off from its satellite launch ramp animation, so it stands for a ramp effect rather "
					"than a socket."
				)
			else:
				notes += f" Placement: retained table Light LL{address}."
				if address in TURBO_BUMPER_LAMPS:
					notes += " The light sits in its turbo bumper cap."
				if address == 69:
					notes += " The helicopter spotlight; the retained table models it as a wide spotlight light above the helicopter."
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		physical["notes"] = notes
		device = _device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra)
		device["provenance"]["status"] = status
		items.append(device)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	identifier = "gi.relay"
	notes = (
		"PinMAME publishes Whitestar's general-illumination relay (the G.I. Relay on the I/O Power Driver Board) as one "
		"aggregate channel. Behind it the fuse chart prints four separately fused 6.3v AC strings: F24 'G.I. Lamp Insert "
		"Left', F25 'G.I. Lamp Lower Half Playfield', F26 'G.I. Lamp Insert Right & Coin Door' and F27 'G.I. Lamp Upper "
		"Half Playfield'; the backbox insert drawing shows the insert GI on two runs (WHT/BRN-BRN and GRN-WHT/GRN). No "
		"source enumerates the playfield sockets, so the placements are the retained table's GI collection, which its "
		"GIUpdates2 routine drives from this channel, reduced to one bulb-mesh light per position; they stay observed. "
		"The quantity counts those playfield emitters only; the backbox insert and coin door bulbs are not placed. The "
		"superseded legacy record exposed this channel as lamp 0, which its vpe-legacy.lamp aliases keep resolvable."
	)
	return [
		_device(
			identifier, "General Illumination Relay", "gi", "pinmame.output.gi", 0, "used", (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=[{"namespace": "pinmame.gi", "value": "0"}] + legacy_aliases("vpe-legacy.lamp", 0, LEGACY_LAMPS),
			physical={"quantity": len(GI_POSITIONS), "notes": notes},
			spatial=located(identifier, "emitter", GI_POSITIONS, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
		)
	]


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.dmd",
			"label": "128x32 dot-matrix display",
			"kind": "dmd",
			"controller_index": 0,
			"width": 128,
			"height": 32,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": pdesc} for pid, plabel, psensors, pdesc in positions]
		return record

	return [
		mechanism(
			"mechanism.trough", "Five-ball trough with lock ball and up-kicker", "kicker",
			[output_id("Trough Lock Ball"), output_id("Trough Up-Kicker")],
			["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-14", "switch.matrix-15"],
			"GoldenEye is a five-ball game (the manual's front page: 'INSTALL 5 BALLS!'). Drained balls roll into the 5-Ball "
			"Trough (OPTO) Assembly 500-5989-05-42 and rest on five subminiature roller switches, #1 (10) at the left to #5 "
			"(14) at the right. The Lock Ball Assembly 500-5684-01 on the trough (a 25-1240 coil, link and cam: solenoid 17) "
			"releases one ball at a time onto the up-kicker at the right end, where the opto pair 15 sees it; the 23-800 "
			"up-kicker (VUK, solenoid 1) then kicks it up into the shooter lane. Four harness runs show the sequence. "
			"After Start the ROM pulses 17. Raising only 15 draws 1 about 0.25 s later; releasing only trough switch 14 "
			"draws it about 0.81 s later; changing neither leaves the ROM pulsing 17 five times about 0.7 s apart, then "
			"firing the auto launch (2) and the up-kicker (1), and repeating that cycle for the whole run. The retained table models "
			"the trough with one ball stack on 10-14 ejected through solenoid 1 and pulses 15 whenever 17 fires.",
			[
				("trough-1", "Trough #1 (left)", ["switch.matrix-10"], "Leftmost trough position."),
				("trough-2", "Trough #2", ["switch.matrix-11"], "Second trough position."),
				("trough-3", "Trough #3", ["switch.matrix-12"], "Third trough position."),
				("trough-4", "Trough #4", ["switch.matrix-13"], "Fourth trough position."),
				("trough-5", "Trough #5 (right)", ["switch.matrix-14"], "Rightmost trough position, next to the lock ball."),
				("up-kicker", "Ball on the up-kicker", ["switch.matrix-15"], "VUK opto; closes while a ball blocks its beam."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly_part_number="500-5989-05-42",
		),
		mechanism(
			"mechanism.auto-launch", "Shooter lane, gun trigger and auto launch", "kicker",
			[output_id("Auto Launch")], ["switch.matrix-16", "switch.matrix-9"],
			"A served ball rests on the shooter-lane rollover (16). There is no plunger: the player pulls the trigger of "
			"the cabinet \"007\" Gun Assembly (Fire Button, 9) and the ROM fires the Auto Ball Launch Assembly "
			"500-5477-01-42 (24-940 coil, solenoid 2). The harness shows the launch about 0.08 s after 9 closes, a retry "
			"while 16 stays closed, and the flipper magnet (34) energized for about 5.8 s after the launch; flasher 32 "
			"flashes while the ball waits in the lane. The manual's operator alert text names the auto launch among the "
			"switch-activated coils the CPU fires ten times before reporting a stuck ball.",
			[("shooter", "Ball in the shooter lane", ["switch.matrix-16"], "Shooter lane rollover.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly_part_number="500-5477-01-42",
		),
		mechanism(
			"mechanism.power-scoop", "Power scoop", "kicker", [output_id("Power Scoop")], ["switch.matrix-50"],
			"A ball entering the scoop at the top left of the playfield closes the micro switch (50) of the Power Scoop "
			"Assembly 500-5809-00-42; the separate Kick Big Assembly 500-5862-00-42 (23-800 coil, solenoid 4) kicks it back "
			"out. The manual says the two assemblies work in conjunction with each other.",
			[("ball", "Ball in the scoop", ["switch.matrix-50"], "Scoop micro switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="500-5809-00-42",
		),
		mechanism(
			"mechanism.tank", "Tank trap door and tank lock", "kicker",
			[output_id("Tank Trap Door"), output_id("Tank Kicker")], ["switch.matrix-56"],
			"The Tank Trap Door Plunger Assembly 500-5940-01-42 (27-1500 coil, solenoid 22) swings a trap door (diverter) "
			"wire in the wire ramp on the left of the playfield; while it is open a ball on that ramp drops into the tank "
			"at the upper left, where switch 56 ('Tank Trap Door') reports it, and the 23-800 tank kicker (solenoid 14) "
			"kicks it back out. The retained table enables its DropRamp1 kicker while 22 is on and ejects up to two "
			"balls at a time through TankKickBig; the Dozer script also binds 22 as the trap door.",
			[("ball", "Ball in the tank", ["switch.matrix-56"], "Tank switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, DOZER_SCRIPT_SOURCE, assembly_part_number="500-5940-01-42",
		),
		mechanism(
			"mechanism.satellite", "Satellite dish with magnet", "motorized",
			[output_id("Satellite Motor Relay"), output_id("Satellite Magnet")], ["switch.matrix-20", "switch.matrix-23"],
			"The satellite dish (Satellite Assembly 500-6000-00-42) carries a 22-600 magnet. It is swung by the 24v AC 6 RPM "
			"motor of the Satellite Motor Base Assembly 500-5982-00-42 through a crank arm and cam link, switched by the "
			"satellite motor relay (solenoid 21, a 24V DC 10A DPDT relay); a motor-cam microswitch reports home (20). The "
			"M1 Magnet Processor / Driver Board 520-5143-00 powers the magnet (public 33) and reports a ball held on it "
			"(23). The harness shows the ROM running the motor at power-up until 20 closes, releasing the relay about "
			"0.11 s after it does, and giving up after about 13.8 s if it never does. The retained VPW table swings the "
			"dish back and forth (30 x sin(theta) - 10 degrees) and closes 20 near theta = 0; it grabs a ball arriving "
			"on the raised launch ramp while 33 is on and holds 23 closed until 33 drops. The printed Satellite flasher "
			"(28) lights it.",
			[
				("home", "Satellite at home", ["switch.matrix-20"], "Motor cam switch; public 1 at home."),
				("ball", "Ball held on the satellite magnet", ["switch.matrix-23"], "Magnet board ball detection."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, DOZER_SCRIPT_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, assembly_part_number="500-5982-00-42",
		),
		mechanism(
			"mechanism.satellite-launch-ramp", "Satellite launch ramp", "diverter", [output_id("Satellite Launch Ramp")], [],
			"The Satellite Launch Ramp Assembly 500-6004-00-42: a lift ramp plunger assembly (solenoid 20) raises the "
			"Up-Down Ramp Sub-Assembly with its Skill Shot Flap in the centre of the playfield so a ball can run up it "
			"onto the satellite. No switch reports its position. The retained script raises the ramp while 20 is on and "
			"lowers it when released.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="500-6004-00-42",
		),
		mechanism(
			"mechanism.up-down-ramp", "Up-down metal ramp", "diverter", [output_id("Up-Down Ramp Plunger")], [],
			"The Up-Down Metal Ramp Plunger Assembly 500-6058-00-42 (27-1500 coil, solenoid 18) moves the Up-Down Metal "
			"Ramp & Flat Rail Assembly 500-6052-00-42 at the upper right through a plunger and link. No switch reports "
			"its position. The retained script lowers the ramp and switches the ball path to its lowered surfaces while "
			"18 is on and restores the raised path when released.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="500-6058-00-42",
		),
		mechanism(
			"mechanism.flipper-magnet", "Flipper magnet", "other", [output_id("Flipper Magnet")], ["switch.matrix-24"],
			"A 22-600 magnet under the playfield between the flippers (Between Flipper Magnet parts), powered by the M1 "
			"Magnet Processor / Driver Board (public 34), which also reports a ball on it (24). It catches a ball heading "
			"down the centre drain. The harness shows the ROM energizing it for about 5.8 s after a launch; the Dozer "
			"script holds 24 closed while a ball sits on it and kicks the ball back up when the magnet drops, and the VPW "
			"script releases the ball and pulses 24 when it drops.",
			[("ball", "Ball on the flipper magnet", ["switch.matrix-24"], "Magnet board ball detection.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, DOZER_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly_part_number="515-6141-00",
		),
		mechanism(
			"mechanism.turbo-bumpers", "Three turbo bumpers", "other",
			[output_id("Left Turbo Bumper"), output_id("Bottom Turbo Bumper"), output_id("Right Turbo Bumper")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
			"Three turbo (pop) bumpers at the top right, printed left (9/41), bottom (10/42) and right (11/43), each lit "
			"by a lamp in its cap (19, 27, 41). The retained table's LeftTurboBumper, BottomTurboBumper and "
			"RightTurboBumper pulse 41, 42 and 43, matching the printed names to the objects' positions.",
			[
				("left", "Left turbo bumper", ["switch.matrix-41"], "Table object LeftTurboBumper."),
				("bottom", "Bottom turbo bumper", ["switch.matrix-42"], "Table object BottomTurboBumper, below the other two."),
				("right", "Right turbo bumper", ["switch.matrix-43"], "Table object RightTurboBumper."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-61", "switch.matrix-62"],
			"Slingshot assemblies with 26-1200 coils (12 left, 13 right) and 180-5054-00 kicker switches (61 left, 62 right).",
			[("left", "Left slingshot", ["switch.matrix-61"], "Left slingshot."), ("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Two flippers on the solid state flipper board", "other",
			[output_id("Right Flipper Enable"), output_id("Right Flipper Enable (Hold View)"), output_id("Left Flipper Enable"), output_id("Left Flipper Enable (Hold View)")],
			["switch.matrix-63", "switch.matrix-64"],
			"Two lower flippers (22-1080 coils) driven by the 2-Flipper Solid State Flipper Board 520-5080-00 in the "
			"backbox. The cabinet buttons are wired to the SSFB, which fires each coil from its button (50v through its "
			"output transistors, then an 8v AC hold), uses the flipper's own end-of-stroke switch, and reports each "
			"button to the CPU as matrix switch 63 (left) or 64 (right). The CPU only enables the flippers, through "
			"Q15/Q16 (public 47/45, with 48/46 set alongside); in the harness run all four went high together and "
			"stayed high, as the next output change about 14.8 s after the shooter-lane switch closed. A recreation fires a flipper while its button is held and the matching enable is on.",
			[
				("left", "Left flipper", ["switch.matrix-63"], "Button 63, enable 47/48."),
				("right", "Right flipper", ["switch.matrix-64"], "Button 64, enable 45/46."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE, assembly_part_number="520-5080-00",
		),
		mechanism(
			"mechanism.stand-up-targets", "Stand-up target banks", "other", [],
			["switch.matrix-25", "switch.matrix-26", "switch.matrix-27", "switch.matrix-28", "switch.matrix-30", "switch.matrix-31", "switch.matrix-33", "switch.matrix-34", "switch.matrix-39", "switch.matrix-44", "switch.matrix-45", "switch.matrix-46", "switch.matrix-47", "switch.matrix-48"],
			"Stationary targets only; no target bank has a drop or reset coil. The left bank on the left side of the "
			"playfield (25-28, printed 'left 5-bank' although four switches are printed), the right 5-bank in the "
			"centre-right (44-48), the 2-bank at the right (33, 34), the left and right stand-ups (30, 31) and the eject "
			"stand-up (39). Each lights its own lamps (left bank 45-48, right bank 52-56, 2-bank 23-24, stand-ups 25-26, "
			"eject 58-59).",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


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


COVERAGE_MISSING = ("output_semantics", "spatial_placement", "unresolved_conflicts")


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": BULB_CONFLICT,
			"path": (
				"outputs[pinmame.output.lamp:1-8|10-56|58-63|65-69]; outputs[pinmame.output.solenoid:25|26|27]"
			),
			"description": (
				"The manual disagrees with itself about bulb types. The lamp matrix grid (Find-It-In-Front page iii) prints "
				"'#44 Bulb' in every populated cell, and the flash lamp chart (page v) prints #906 wedge bulbs for the "
				"playfield sockets of FLAMP 1-3 (solenoids 25-27, five bulbs). The playfield bulb and socket pages (printed "
				"65-67) list 94 #44 bayonet bulbs, so #44 bulbs are on the playfield, but also 54 #555 wedge bulbs, 42 "
				"lamp-board wedge sockets and three Turbo Pop Bumper Sockets printed 'Use #555 Bulbs only', 29 #89 bulbs, "
				"and the #906 bulb, the 906 socket and the 555/906 IDC socket all at quantity 0, which the pages define as "
				"not used in this game. The playfield boards page (printed 64) adds that '#555 Bulbs are used on the Light "
				"Boards' L1-L8, and the ramp assembly pages (printed 82-84) list #555 bulbs in the 'Tank Multiball' and "
				"two-bulb 'Lock Ball' signs, the Helicopter Assembly and the Spot Light Assembly, the last two in a "
				"laydown wedge base L/R black socket (077-5026-01) that the wedge-base page lists at quantity 0. So at "
				"least the turbo bumper lamps 19, 27 and 41, every lamp on the eight light boards, and the ramp sign and "
				"helicopter lamps (by name most likely 49, 60, 61 and 69, an inference) take a #555 wedge bulb instead "
				"of the printed #44, and flashers 25-27 either take no #906 or the bulb pages are wrong. No page says "
				"which lamps sit on the light boards, so every playfield lamp is affected. The start button (57) and "
				"the nine speaker-panel letters (72-80), whose own parts list prints #44, are not. Pinned PinMAME's "
				"Whitestar output typing models every lamp as a #44 bulb on 18v DC and, for gldneye, all eight flash "
				"lamps 25-32 as #89 bulbs; for 25-27 that matches the bulb pages rather than the flash lamp chart. "
				"Resolution path: photographs of the underside "
				"of an unrestored GoldenEye playfield showing which inserts sit on light boards L1-L8 and which bulb the "
				"FLAMP 1-3 sockets carry, which any GoldenEye owner could take, or a later revision of these parts pages."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		}
	]


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "sega.goldeneye.1996",
			"name": "GoldenEye",
			"manufacturer": "Sega",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 3792,
			"opdb_id": "G43wE-MQV5K",
		},
		"coverage": {
			"status": "partial",
			"missing": list(COVERAGE_MISSING),
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {
			"platform": "pinmame.whitestar",
			"hardware_generation": "0x4000000000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/sega/goldeneye-1996.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"GoldenEye device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	observed_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
			continue
		placement_count += len(spatial["placements"])
		(observed_inputs if spatial["status"] == "observed" else located_inputs).append(address)
	located_outputs: list[dict[str, Any]] = []
	observed_outputs: list[dict[str, Any]] = []
	unplaced_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unplaced_outputs.append(binding)
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
			continue
		placement_count += len(spatial["placements"])
		(observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
	order = lambda item: (item["group"], item["address"])  # noqa: E731
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "observed",
		"blockers": [
			"The retained manual scan keeps the outlines of its playfield switch, coil and flash-lamp location drawings "
			"but none of their callout numbers, so no placement can be checked against a factory drawing. Every "
			"coordinate comes from one community table (the VPW GoldenEye 1.2.1, itself built on the JPJ/32Assassin "
			"table) and stays observed. Promotion needs a scan with legible callouts, a second independent geometry "
			"source, or a survey of a real machine.",
			"Flasher sockets without a table object: 26 (Lower Flipper Magnet), 30 (Helicopter), the second socket of "
			"28 (Satellite) and 29 (Lower Right Playfield), the Upper Left socket of 31 and both Upper Right sockets of "
			"32 are not placed.",
			"Lamp 58 (Behind Eject Stand-Up) has no table light and is not placed.",
			"Lamp 40 (Under Ramp Bottom) is not placed: its only table object, LL40, has no bulb light or insert "
			"primitive, a wider falloff than any insert light, and is switched by the satellite launch ramp animation, "
			"so it stands for a ramp effect rather than a socket.",
			"Playfield general illumination has no factory socket list; its 37 emitters come from the retained table's GI collection.",
		],
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
			"manifest_uri": "external:pinmame-vpx-sources/sega/goldeneye-1996/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"observed_input_addresses": sorted(observed_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=order),
		"observed_output_bindings": sorted(observed_outputs, key=order),
		"unplaced_output_bindings": sorted(unplaced_outputs, key=order),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": SOLENOID_OBJECTS[address]}
			for address in (1, 17, 18, 21)
		],
		"coordinate_origins": {
			"bounding_box_centers": [
				"Walls SS25-SS28, SS30, SS31, SS33, SS34, SS39 and SS44-SS48 (stand-up targets)",
				"Walls LeftSlingShot and RightSlingShot (switches 61/62, solenoids 12/13)",
			],
			"object_centers": "every other placement uses its retained object's own center",
		},
		"excluded_object_classes": [
			"LLb-prefixed bloom lights bound to the same lamp as an LL light, and the A/B halo copies of the bumper lamps.",
			"The glow light without a bulb mesh at each GI position.",
			"L72-L80, backglass lights standing for the speaker-panel GOLDENEYE letters (lamps 72-80).",
			"Flasher25-Flasher32, invisible helper lights outside the playfield (x < 0).",
			"LL15F and rampflash4/Flash003, lights the script drives for flashers 26 and 30 that do not stand at a printed socket.",
			"The retained table's SW49 trigger, bound to a matrix position the manual prints Not Used.",
			"FlashMagnet, the optional 'fantasy magnet' effect of the flipper magnet.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# GoldenEye (Sega, 1996) spatial review",
		"",
		f"Status: {report['status']}. Every playfield switch, coil, magnet, flasher socket the table models and lamp is "
		"placed from the retained table or carries a controlled `not_applicable` record, but every coordinate is "
		"`observed`: the retained manual scan lost the callout numbers of its location drawings, so nothing can be "
		"checked against a factory drawing. The record stays at `machines/partial/sega/goldeneye-1996.json`.",
		"",
		f"The geometry source is the retained known-working `Goldeneye (Sega 1996) VPW 1.2.1.vpx` (SHA-256 "
		f"`{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding authority. Exact "
		f"playfield bounds are `{TABLE_BOUNDS}`; every coordinate is x/952 and y/2162 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime authority, cross-checked against the pinned VPW 1.2 script and the "
		"independent Dozer script; the operations manual is the physical inventory, construction and wiring authority; "
		"pinned PinMAME owns controller topology; hash-pinned harness runs settle the satellite home and VUK opto "
		"polarity and the ball-serve sequence; the retained table supplies geometry.",
		"- Trough switches 10-15 are projected onto the table's trough exit kicker, switch 20 onto the satellite dish, "
		"switches 23/24 onto the magnet positions and switch 56 onto the tank kicker.",
		"- The lock-ball coil, up-down ramp plunger and satellite motor relay are projected onto the mechanism each moves.",
		"- The speaker-panel GOLDENEYE lamps (72-80), the start button lamp (57), the knocker and coin meter drive lines "
		"and the backbox insert flash lamps are cabinet or backbox devices and are not placed.",
		"",
		"## Blockers",
		"",
	]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Explicit projections", ""]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
		f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
		f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
		f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
		f"- Output bindings without a placement: {len(report['unplaced_output_bindings'])}",
	]
	lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
	lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Refused. `coverage.missing` is `" + json.dumps(list(COVERAGE_MISSING)) + "`: every coordinate rests on one "
		"community table with no legible factory drawing to check it against, several flasher sockets and lamps 40 "
		"and 58 have no socket object, public solenoids 35 and 36 carry magnet-board latch bits whose meaning no "
		"source states, and the manual's lamp grid and bulb pages disagree about bulb types (conflict.bulb-types).",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Operations manual SHA-256 `{MANUAL_SHA256}`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("Stale GoldenEye author-ready definition is still present")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"GoldenEye artifact is missing: {path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"GoldenEye definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"GoldenEye seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"GoldenEye spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"GoldenEye spatial review drifted from its deterministic curator: {markdown_path}")
	print("GoldenEye definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, seed and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		print(f"GoldenEye extraction manifest written: {write_extraction_manifest(root)}")
	elif args.verify_extraction:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		verify_extraction_manifest(root)
		print("GoldenEye retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
