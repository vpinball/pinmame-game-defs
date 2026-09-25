"""Curate the physical Williams Earthshaker (1989) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail, runtime
observation, and normalized coordinate is a literal here, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed, and the
spatial report.

Earthshaker runs on Williams System 11B. Switches and lamps share one sequential column-major
1-64 address space, general illumination is three ordinary solenoid addresses (10, 11, 15), and
the eight switched solenoids 1-8 are multiplexed onto 25-32 by the A/C select relay (12). See
``controllers/pinmame/system-11.json`` for the platform derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.earthshaker.1989"
PARTIAL_PATH = ROOT / "machines/partial/williams/earthshaker-1989.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/earthshaker-1989.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/earthshaker-1989.json"
KNOWLEDGE_PATH = "knowledge/williams/earthshaker-1989.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/earthshaker-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/earthshaker-1989.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
LA3_RUNTIME_PATH = "evidence/runtime/system-11/earthshaker-la3-service-and-mechanisms.json"
PA1_RUNTIME_PATH = "evidence/runtime/system-11/earthshaker-pa1-prototype-service.json"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.earthshaker.1989"
ROM_SOURCE = "rom.earthshaker.name-tables"
RUNTIME_SOURCE = "runtime.earthshaker.la3-service-and-mechanisms"
PA1_RUNTIME_SOURCE = "runtime.earthshaker.pa1-prototype-service"
VPX_TABLE_SOURCE = "vpx-table.earthshaker-vpw-lite-v006"
VPX_SCRIPT_SOURCE = "vpx-script.earthshaker-vpw-lite-v006"
VPX_EXTRACTION_SOURCE = "vpx-extraction.earthshaker-vpw-lite-v006"

MANUAL_SHA256 = "94ad82c16f1ae72fd7b71cdadf4616c8166fd545a2740efe5cda2cc9b1a8db3b"
TABLE_SHA256 = "7df82a9ab3196214bc03df98a0b2669bf49b27cee91814f341bb4bc1c27d9522"
SCRIPT_SHA256 = "0c2bb47c3469e9b04d28a44f94469c3935050aa4975d31ee12e6fb344392eb72"
EXTRACTION_RELATIVE_PATH = Path("williams/earthshaker-1989/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/earthshaker-1989/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "cc52978345233ac0650ea8e54173b18494e19d1e75d57a88c95941c295159f76"
EXTRACTION_FILE_COUNT = 2447
EXTRACTION_TOTAL_BYTES = 258155460
TABLE_WIDTH = 964.0
TABLE_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

# --- Driver tree -----------------------------------------------------------------------------
DRIVER_IDS = ("esha_la3", "esha_l4c", "esha_ma3", "esha_pr4", "esha_lg1", "esha_lg2", "esha_la1", "esha_pa4", "esha_pa1")
_SHARED = (
	"Declared with CORE_CLONEDEF against esha_la3 on the same s11_mS11BS machine driver, so it runs the one static "
	"eshaGameData (GEN_S11B, s11_dispS11b2, A/C mux relay 12, FLIP_SWNO(58,57), S11_MUXSW2) and init_esha; no "
	"controller-address change."
)
DRIVER_COMPATIBILITY = {
	"esha_la3": ("identical", "Williams LA-3 production game ROMs (eshk_u26.l3/eshk_u27.l3), the clone-tree parent and the driver the retained known-working script binds (cGameName = \"esha_la3\"). Its coil test names solenoid 9 UNUSED and 22 QUAKE MOTOR, and its switch table names 25/26 BLDNG. 1 UNUSED and BLDNG. 2 UNUSED, yet it still energizes solenoid 9 for about 5.9 s on entering Game-Over mode (see the building note on solenoid 9)."),
	"esha_l4c": ("identical", f"LA-4C Competition MOD (2016) of the production ROM for the unchanged machine. {_SHARED} Its ROM archive is not in the local corpus, so its name tables were not read."),
	"esha_ma3": ("identical", f"LA-3 Metallica MOD: a text re-theme of LA-3 for the unchanged machine. {_SHARED} Its ROM renames the Fault to FIGHT FIRE (coil FIGHT FIRE FIGHT, switch 42 FIGHT FIRE), the on-ramp switches to LGTNING, the building-height switches 25/26 to AMP 1/2 UNUSED, and the Quake motor to CROWD MOTOR; addresses are unchanged."),
	"esha_pr4": ("identical", f"PR-4 \"Family version\". Pinned PinMAME comments it \"Prototype ?? also known as F-1\" and notes that its ROM (eshk_u26.f1) \"says PR 4, not F-1\", so whether it is a prototype is unsettled. {_SHARED} Its switch and coil name tables match LA-3 exactly, so no hardware difference is known."),
	"esha_lg1": ("identical", f"LG-1 German ROM. {_SHARED} Its switch and coil name tables match LA-3 exactly (the service text stays English)."),
	"esha_lg2": ("identical", f"LG-2 German ROM. {_SHARED} Its switch and coil name tables match LA-3 exactly."),
	"esha_la1": ("identical", f"LA-1 production ROM. {_SHARED} Its tables match LA-3 except switch 8, spelled HI.  SCORE RESET."),
	"esha_pa4": ("compatible", f"PA-4 prototype, commented in pinned s11games.c as supporting the collapsible building (\"aka Phil Dixons version\"). {_SHARED} The prototype building mechanism is not fitted to production machines; see the solenoid 9 and switch 25/26 notes. Its ROM archive is not in the local corpus."),
	"esha_pa1": ("compatible", f"PA-1 prototype. {_SHARED} Its ROM names solenoid 9 BUILDING MOTOR and switches 25/26 BLDNG HEIGHT 1/2 where production ROMs print UNUSED, so it expects the motor-driven sinking building that production machines do not fit; see the solenoid 9 and switch 25/26 notes."),
}

# --- Switches (manual printed 66 locations list, 68 matrix; ROM switch name table) ---------------
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "A/C Relay C-Side Power", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute",
	6: "Left Coin Chute", 7: "Slam Tilt", 8: "High Score Reset", 9: "Playfield Tilt", 10: "Outhole",
	11: "Ball Trough 1 (Right)", 12: "Ball Trough 2 (Middle)", 13: "Ball Trough 3 (Left)",
	14: "Right Inner Return Lane (Zone 7)", 15: "Right Outer Return Lane", 16: "Right Outlane", 17: "Left Outlane",
	18: "Left Return Lane (Zone 8)", 19: "Left Standup (Zone 1)", 20: "Eject Hole (Zone 5)",
	21: "Right Standup High (Zone 2)", 22: "Right Standup Low (Zone 3)", 23: "Captive Ball Standup (Zone 9)",
	24: "Right 50K Standup", 25: "Building Height 1", 26: "Building Height 2",
	27: "3-Bank Drop Target Left", 28: "3-Bank Drop Target Center", 29: "3-Bank Drop Target Right",
	30: "Center Standup (Zone 4)", 31: "Right Loop (Zone 6)", 32: "Left Loop (Zone 6)",
	33: "On-Ramp 50K", 34: "On-Ramp 25K", 35: "On-Ramp 100K", 36: "On-Ramp Bypass",
	37: "Top Ball Popper", 38: "Drop Hole 1", 39: "Drop Hole 2", 40: "Bottom Ball Popper", 41: "Spinner",
	42: "Fault Open", 43: "Right Ramp Entry", 44: "Center Ramp Entry", 45: "Center Ramp Middle", 46: "Center Ramp End",
	50: "Ball Shooter Lane", 52: "Left Jet Bumper", 53: "Right Jet Bumper", 54: "Top Jet Bumper",
	55: "Left Slingshot", 56: "Right Slingshot", 57: "Right Flipper Button", 58: "Left Flipper Button",
}
UNUSED_SWITCHES = {47, 48, 49, 51, 59, 60, 61, 62, 63, 64}
PROTOTYPE_SWITCHES = {25, 26}
# ROM switch-table text (esha_la3, U26 offset 0x12ec), decoded by tools/s11_rom_name_tables.py.
ROM_SWITCH_NAMES = {
	1: "PLUMB  TILT", 2: "A/C RELAY", 3: "CREDIT BUTTON", 4: "RIGHT COIN", 5: "CENTER COIN", 6: "LEFT COIN",
	7: "SLAM  TILT", 8: "HIGH SCORE RESET", 9: "PLAYFIELD TILT", 10: "OUTHOLE", 11: "TROUGH   1", 12: "TROUGH   2",
	13: "TROUGH   3", 14: "R. INNER RETLANE", 15: "R. OUTER RETLANE", 16: "RIGHT OUTLANE", 17: "LEFT OUTLANE",
	18: "LEFT RETURN LANE", 19: "LEFT STANDUP", 20: "EJECT HOLE", 21: "RIGHT STANDUP 1", 22: "RIGHT STANDUP 2",
	23: "CAPTIVE BALL", 24: "BOTM. RT. STANDUP", 25: "BLDNG. 1 UNUSED", 26: "BLDNG. 2 UNUSED", 27: "LEFT DROP TARGET",
	28: "CENTER DROP TARG.", 29: "RIGHT DROP TARGT.", 30: "CENTER STANDUP", 31: "RIGHT LOOP", 32: "LEFT LOOP",
	33: "ON-RAMP 50K", 34: "ON-RAMP 25K", 35: "ON-RAMP 100K", 36: "ON-RAMP BYPASS", 37: "TOP BALL POPPER",
	38: "DROP HOLE 1", 39: "DROP HOLE 2", 40: "BOTM. BALL POPPER", 41: "SPINNER", 42: "FAULT OPEN",
	43: "RIGHT RAMP ENTRY", 44: "CENTR. RAMP ENTRY", 45: "CNTR. RAMP MIDDLE", 46: "CENTER RAMP END", 47: "UNUSED",
	48: "UNUSED", 49: "UNUSED", 50: "SHOOTER LANE", 51: "UNUSED", 52: "LEFT JET BUMPER", 53: "RIGHT JET BUMPER",
	54: "TOP JET BUMPER", 55: "LEFT SLINGSHOT", 56: "RIGHT SLINGSHOT", 57: "RIGHT FLIPPER", 58: "LEFT FLIPPER",
}
# Printed matrix wording (printed page 68) where it differs from the working label.
MATRIX_WORDING = {
	2: "C Side Power A/C Relay", 4: "Left Coin Chute", 6: "Right Coin Chute", 11: "Ball Trough #1 (R)", 12: "Ball Trough #2 (Mid)",
	13: "Ball Trough #3 (L)", 14: "Right Inside Return Lane", 15: "Right Outside Return Lane", 21: "Right Standup (high)",
	22: "Right Standup (low)", 23: "Captive Ball", 24: "Right Standup (50K)", 27: "3-Bank DT (left)", 28: "3-Bank DT (mid)",
	29: "3-Bank DT (right)", 37: "Ball Popper (top)", 38: "Under Playfield Drop Hole 1", 39: "Under Playfield Drop Hole 2",
	40: "Ball Popper (bottom)", 50: "Ball Shooter", 55: "BL Kicker (\"sling\")", 56: "BR Kicker (\"sling\")",
	57: "Flipper Right", 58: "Flipper Left",
}
# Locations-list wording (printed page 66) where it differs from the working label.
LIST_WORDING = {
	2: "Not Used", 4: "R Coin Chute (USA)", 5: "Center Coin Chute (Not Used (USA))", 6: "L Coin Chute (USA)",
	11: "Ball Trough 1 (right)", 12: "Ball Trough 2 (left)", 13: "Ball Trough 3 (left)", 14: "R Inner Return Lane (Zone 7)",
	16: "Right Outlane (drain)", 17: "Left Outlane (drain)", 21: "R ight Standup Tgt (Zone 2)", 22: "R ight Standup Tgt (Zone 3)",
	23: "Cptv Ball Standup Tgt (Zone 9)", 24: "50K (R Wh Standup Tgt)", 38: "Drop Hole 1 (under p'fld)", 39: "Drop Hole 2 (under p'fld)",
	55: "Left Kicker***", 56: "Right Kicker***", 57: "R Flipper Lane Change**1", 58: "L Flipper Lane Change**1",
}
SWITCH_PARTS = {
	3: "SW-1A-126", 4: "27-1092", 6: "27-1092", 7: "27-1066", 8: "27-1008", 9: "B-8306-1", 10: "5647-12133-12",
	11: "5647-12073-08", 12: "5647-09957-00", 13: "5647-09957-00", 14: "5647-12073-19", 15: "5647-12073-19",
	16: "5647-12073-19", 17: "5647-12073-19", 18: "5647-12073-19", 19: "B-11696-1", 20: "5647-12133-11",
	21: "B-11696-1", 22: "B-11696-1", 23: "B-11696-5", 24: "B-11696-5", 25: "p/o C-12406", 26: "p/o C-12406",
	27: "p/o C-12559", 28: "p/o C-12559", 29: "p/o C-12559", 30: "B-12583-6", 31: "5647-12133-08", 32: "5647-12133-08",
	33: "5647-12073-19", 34: "5647-12073-19", 35: "5647-12073-19", 36: "5647-12073-19", 37: "A-11658",
	38: "5647-12073-13", 39: "5647-12073-21", 40: "A-11658", 41: "5647-12133-08", 42: "5647-12073-06",
	43: "5647-12073-11", 44: "5647-12073-11", 45: "5647-12073-13", 46: "5647-12073-13", 50: "5647-12073-04",
	52: "B-12030-2", 53: "B-12030-2", 54: "B-12030-2",
}
SWITCH_TYPES = {1: "tilt", 2: "other", 3: "button", 7: "tilt", 8: "button", 9: "tilt", 25: "opto", 26: "opto", 27: "opto", 28: "opto", 29: "opto", 57: "opto", 58: "opto"}
# The manual itself names part 5647-12073-06 a "Mini Misro-Switch w/Roller" (Zone Opener Assembly, printed 58).
MICROSWITCH_PART_PREFIX = "5647-12073-"
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"), 4: ("GRN-YEL", "1J8-4", "Q48"),
	5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"), 7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_SWITCHES = {
	-7: ("Advance", "service.advance", "S11_SWADVANCE: the ADVANCE button on the coin-door diagnostic switch assembly; it steps the Game Status, audit, adjustment, and diagnostic displays."),
	-6: ("Auto-Up/Manual-Down", "service.updown", "S11_SWUPDN: the AUTO-UP/MANUAL-DOWN toggle. In PinMAME's public state 1 is Auto-Up and 0 is Manual-Down; the harness runs step forward through the audits at 1 and backward from Game ID to Ad 70 at 0."),
	-5: ("CPU Diagnostic", "service.diagnostic", "S11_SWCPUDIAG: pinned s11.c wires it to the CPU's NMI line (the CPU board's diagnostic button)."),
	-4: ("Sound Diagnostic", "service.diagnostic", "S11_SWSOUNDDIAG: pinned s11.c passes it to the sound board's diagnostic input."),
}
CABINET_SWITCH_ROLES = {1: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin", 7: "cabinet.slam-tilt", 8: "cabinet.service", 9: "cabinet.tilt", 57: "cabinet.flipper", 58: "cabinet.flipper"}

# Normalized coordinates from the retained table (x/964, y/2162), object centres unless noted.
SWITCH_POSITIONS = {
	10: ("Kicker.sw10", 0.500721, 0.960313), 11: ("Kicker.sw11", 0.863791, 0.866782), 12: ("Kicker.sw12", 0.810403, 0.880249),
	13: ("Kicker.sw13", 0.752210, 0.895964), 14: ("Trigger.sw14", 0.733766, 0.743347), 15: ("Trigger.sw15", 0.799258, 0.733697),
	16: ("Trigger.sw16", 0.864471, 0.756760), 17: ("Trigger.sw17", 0.065087, 0.773929), 18: ("Trigger.sw18", 0.164803, 0.743295),
	19: ("HitTarget.sw19", 0.247154, 0.464013), 20: ("Kicker.sw20", 0.290258, 0.383899), 21: ("HitTarget.sw21", 0.687716, 0.483721),
	22: ("HitTarget.sw22", 0.711075, 0.508207), 23: ("HitTarget.sw23", 0.851253, 0.445030), 24: ("HitTarget.sw24", 0.816853, 0.552503),
	25: ("Primitive.InstituteBackWall", 0.456950, 0.202086), 26: ("Primitive.InstituteBackWall", 0.456950, 0.202086),
	27: ("HitTarget.sw27", 0.380338, 0.255708), 28: ("HitTarget.sw28", 0.416755, 0.276056), 29: ("HitTarget.sw29", 0.453891, 0.296541),
	30: ("HitTarget.sw30", 0.637013, 0.325423), 31: ("Gate.sw31", 0.699440, 0.118079), 32: ("Gate.sw32", 0.478443, 0.114819),
	33: ("Trigger.sw33", 0.141615, 0.146127), 34: ("Trigger.sw34", 0.246195, 0.112401), 35: ("Trigger.sw35", 0.141034, 0.084950),
	36: ("Trigger.sw36", 0.373181, 0.091002), 37: ("Kicker.TopVUK", 0.909149, 0.039435), 38: ("Trigger.sw38", 0.738383, 0.279892),
	39: ("Trigger.sw39", 0.827577, 0.560223), 40: ("Kicker.BottomVuk", 0.843250, 0.600117), 41: ("Spinner.sw41", 0.289613, 0.212762),
	42: ("Primitive.CalPrim", 0.456432, 0.121521), 43: ("Gate.sw43", 0.811780, 0.386610), 44: ("Gate.sw44", 0.602797, 0.260811),
	45: ("Trigger.sw45", 0.054716, 0.446063), 46: ("Trigger.sw46", 0.053552, 0.583204), 50: ("Trigger.sw50", 0.927014, 0.881886),
	52: ("Bumper.Bumper3", 0.091884, 0.325858), 53: ("Bumper.Bumper2", 0.297461, 0.315178), 54: ("Bumper.Bumper1", 0.172121, 0.241741),
	55: ("Wall.LeftSlingShot drag-point centroid", 0.248059, 0.741320), 56: ("Wall.RightSlingShot drag-point centroid", 0.654428, 0.740398),
}
SWITCH_PROJECTIONS = {
	25: "Building Height 1 is an optotransistor on the prototype Bldg Positioner Bd (p/o C-12406), which no retained source draws; it is anchored at the Institute building it senses. The anchor is the InstituteBackWall primitive's origin, which the building's baked meshes share, not a sensor position, so the placement is observed only.",
	26: "Building Height 2 shares switch 25's anchor for the same reason.",
	37: "The Top Ball Popper switch (A-11658) sits in the popper assembly under its cap; anchored at the retained TopVUK kicker, which the script closes 37 from.",
	40: "The Bottom Ball Popper switch (A-11658) sits in the popper assembly; anchored at the retained BottomVuk kicker, which the script closes 40 from.",
	42: "Fault Open is the roller micro-switch (item 12, 5647-12073-06) inside the Zone Opener Assembly (C-12429) under the California/Nevada fault; no retained object models it, so it is anchored at the California map primitive (CalPrim) the fault coil slides.",
	55: "The slingshot switch pair (A-4834-H; B-8734-1) is inside the slingshot; anchored at the drag-point centroid of the retained LeftSlingShot wall.",
	56: "Anchored at the drag-point centroid of the retained RightSlingShot wall.",
}
# Script pulses that disagree with the manual's physical ordering (table defect, not machine doubt).
BUMPER_SCRIPT_PULSE = {52: "Bumper1_Hit pulses 52 from the uppermost bumper", 53: "Bumper2_Hit pulses 53 from the right bumper", 54: "Bumper3_Hit pulses 54 from the leftmost bumper"}

# --- Solenoids (Solenoid Table printed 30; locations list printed 65; ROM coil test) ---------------
SOLENOID_A = {
	1: ("Outhole Kicker", "coil", "Vio-Brn", "1P11-1", "5J1-9: 5J4-9 (A)", "Q33", "AE-23-800"),
	2: ("Ball Release (Shooter Lane Feeder)", "coil", "Vio-Red", "1P11-3", "5J1-7: 5J4-8 (A)", "Q25", "AE-23-800"),
	3: ("3-Bank Drop Target Reset", "coil", "Vio-Orn", "1P11-4", "5J1-6: 5J4-7 (A)", "Q32", "AE-26-1200"),
	4: ("California Fault", "coil", "Vio- Yel", "1P11-5", "5J1-5: 5J4-6 (A)", "Q24", "AE-23-800"),
	5: ("Eject Hole", "coil", "Vio-Grn", "1P11-6", "5J1-4: 5J4-5 (A)", "Q31", "AE-26-1500"),
	6: ("Bottom Ball Popper", "coil", "Vio-Blu", "1P11-7", "5J1-3: 5J4-4 (A)", "Q23", "AE-23-800"),
	7: ("Knocker", "coil", "Vio-Blk", "1P11-8", "5J1-2: 5J4-2 (A)", "Q30", "AE-23-800"),
	8: ("Not Used Switched Solenoid 08A", "coil", "Vio-Gry", "1P11-9", "5J1-1: 5J4-1 (A)", "Q22", None),
}
SOLENOID_C = {
	25: ("Captive Ball Flasher", "Blk-Brn", "(Gry-Brn)", "5J5-9 (C)", "#89 flashlamp", 1),
	26: ("Center Ramp 1 and Building Flashers", "Blk-Red", "(Gry-Red)", "5J5-8 (C)", "#906/#89 flashlamps", 2),
	27: ("Center Ramp 2 and Spinner Flashers", "Blk-Orn", "(Gry-Orn)", "5J5-7(C)", "#906/#89 flashlamps", 2),
	28: ("Center Ramp 3 Flasher", "Blk-Yel", "(Gry-Yel)", "5J5-5 (C)", "#906 flashlamp", 1),
	29: ("Center Ramp 4 Flasher", "Blk-Grn", "(Gry-Grn)", "5J5-4 (C)", "#906 flashlamp", 1),
	30: ("Right Ramp 1 Flasher", "Blk-Blu", "(Gry-Blu)", "5J5-3 (C)", "#906 flashlamp", 1),
	31: ("Right Ramp 2 Flasher", "Blk-Vio", "(Gry-Vio)", "5J5-2 (C)", "#906 flashlamp", 1),
	32: ("Right Ramp 3 Flashers", "Blk-Gry", "(Gry-Blk)", "5J5-1 (C)", "#906/#89 flashlamps", 2),
}
SOLENOID_CONTROLLED = {
	9: ("Building Motor Relay (Prototype Sinking Building)", "relay", "Brn-Blk", "1P12-1", "5J2-9: 5J6-9: 2J4-3", "Q17", "5580-12145-01"),
	10: ("Upper Playfield G.I. Relay", "gi", "Brn-Red", "1P12-2", "5J2-8: 5J6-8: 2J4-5", "Q9", "5580-12145-01"),
	11: ("Insert Board G.I. Relay", "gi", "Brn-Orn", "1P12-4", "5J2-6: 5J6-7: 2J4-6", "Q16", "5580-09555-01"),
	12: ("A/C Select Relay", "relay", "Brn-Yel", "1P12-5", "5J2-5", "Q8", "5580-09555-01"),
	13: ("Top Ball Popper", "coil", "Brn-Grn", "1P12-6", "5J2-4: 5J6-5", "Q15", "AE-23-800"),
	14: ("Jackpot and Sun Flashers", "flasher", "Brn-Blu", "1P12-7", "5J2-4: 5J6-3", "Q7", None),
	15: ("Lower Playfield G.I. Relay", "gi", "Brn-Vio", "1P12-8", "5J2-2: 5J6-2", "Q14", "5580-12145-01"),
	16: ("On-Ramp and Jet Bumper Flashers", "flasher", "Brn-Gry", "1P12-9", "5J2-1: 5J6-1", "Q6", None),
}
SOLENOID_SPECIAL = {
	17: ("Left Jet Bumper", "Blu-Brn", "1P19-7", "5J3-7: 5J7-7", "Q75", "AE-23-800", 1),
	18: ("Left Slingshot", "Blu-Red", "1P19-4", "5J3-6: 5J7-6", "Q71", "AE-26-1500", 2),
	19: ("Right Jet Bumper", "Blu-Orn", "1P19-3", "5J3-3: 5J7-3", "Q73", "AE-23-800", 3),
	20: ("Right Slingshot", "Blu-Yel", "1P19-6", "5J3-4: 5J7-5", "Q69", "AE-26-1500", 4),
	21: ("Top Jet Bumper", "Blu-Grn", "1P19-8", "5J3-2:5J7-2", "Q77", "AE-23-800", 5),
	22: ("Quake Shaker Motor", "Blu-Blk", "1P19-9", "5J3-1: 5J7-1", "Q79", "14-7951", 6),
}
# ROM coil-test names by public address (esha_la3 Auto Burn-in coil test paired with the ROM coil table).
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "CAPTV. BALL FLASH", 2: "BALL RELEASE", 26: "CNTR. RMP. FLASH 1", 3: "DROP TARGT. RESET",
	27: "CNTR. RMP. FLASH 2", 4: "CALIFORNIA FAULT", 28: "CNTR. RMP. FLASH 3", 5: "EJECT HOLE", 29: "CNTR. RMP. FLASH 4",
	6: "BOTM. BALL POPPER", 30: "RGHT. RMP. FLASH 1", 7: "KNOCKER", 31: "RGHT. RMP. FLASH 2", 8: "UNUSED",
	32: "RGHT. RMP. FLASH 3", 9: "UNUSED", 10: "UPPER PLAYFLD. G.I.", 11: "INSERT G.I.", 12: "A/C   SELECT",
	13: "TOP BALL POPPER", 14: "JACKPT/SUN FLASH", 15: "LOWER PLAYFLD. G.I.", 16: "JET BUMPER FLASH", 17: "LEFT JET BUMPER",
	18: "LEFT SLINGSHOT", 19: "RIGHT JET BUMPER", 20: "RIGHT SLINGSHOT", 21: "TOP JET BUMPER", 22: "QUAKE MOTOR",
}
SOLENOID_CALLBACKS = {
	1: "SolOuthole (kicks sw10)", 2: "ReleaseBall (kicks sw11)", 3: "SolDropReset", 4: "SolFault (toggles the California/Nevada fault)",
	5: "bsLSaucer.SolOut (sw20 saucer)", 6: "BotPop (raises the ball from BottomVuk)", 7: "vpmSolSound Knocker", 9: "InstituteDrop (moves the modelled building)",
	10: "PFGI2 (upper G.I. collection GIU off while energized)", 12: "Flash112 (VR backglass flashers only)", 13: "VukTopPop (raises the ball from TopVUK)",
	14: "SetLamp 114 (f114/f114a)", 15: "PFGI (lower G.I. collection GI off while energized)", 16: "Flash116 (Flupper dome 10)",
	22: "ShakerMotor (nudges the table while energized)", 25: "Flash125 (dome 6)", 26: "Flash126 (dome 4)", 27: "Flash127 (dome 3)",
	28: "Flash128 (dome 2)", 29: "Flash129 (dome 1)", 30: "Flash130 (dome 7)", 31: "Flash131 (dome 8)", 32: "Flash132 (domes 5 and 9)",
}
SOLENOID_POSITIONS = {
	1: ("Kicker.sw10", [(0.500721, 0.960313)]), 2: ("Kicker.sw11", [(0.863791, 0.866782)]),
	3: ("HitTarget.sw28 (middle target of the bank it resets)", [(0.416755, 0.276056)]),
	4: ("Primitive.CalPrim (the California map the fault slides)", [(0.456432, 0.121521)]),
	5: ("Kicker.sw20", [(0.290258, 0.383899)]), 6: ("Kicker.BottomVuk", [(0.843250, 0.600117)]),
	13: ("Kicker.TopVUK", [(0.909149, 0.039435)]),
	14: ("Light.f114", [(0.486255, 0.468923)]),
	16: ("Primitive.Flasherbase10", [(0.057899, 0.147656)]),
	17: ("Bumper.Bumper3", [(0.091884, 0.325858)]), 18: ("Wall.LeftSlingShot drag-point centroid", [(0.248059, 0.741320)]),
	19: ("Bumper.Bumper2", [(0.297461, 0.315178)]), 20: ("Wall.RightSlingShot drag-point centroid", [(0.654428, 0.740398)]),
	21: ("Bumper.Bumper1", [(0.172121, 0.241741)]),
	25: ("Primitive.Flasherbase6", [(0.847805, 0.529321)]), 26: ("Primitive.Flasherbase4", [(0.636852, 0.132233)]),
	27: ("Primitive.Flasherbase3", [(0.149029, 0.241426)]), 28: ("Primitive.Flasherbase2", [(0.142067, 0.393604)]),
	29: ("Primitive.Flasherbase1", [(0.059215, 0.671183)]), 30: ("Primitive.Flasherbase7", [(0.845948, 0.300005)]),
	31: ("Primitive.Flasherbase8", [(0.845182, 0.241093)]),
	32: ("Primitive.Flasherbase5 and Primitive.Flasherbase9", [(0.798441, 0.033921), (0.845182, 0.180132)]),
}
# What the building-model runs show about how the ROM stops solenoid 9.
BUILDING_RULE = (
	'In nine esha_la3 runs with a modelled building the ROM ignored the first change of 25/26 after energizing 9, whatever it was, then released 9 within about 0.1 s of the next fall of 25 or rise of 26, and never on a rise of 25 or a fall of 26. Two of the runs rule out a run-time threshold: a fall of 25 stopped the motor 0.73 s after it started when a rise of 25 had come first, and a fall of 25 at 2.50 s did not stop it when it was the first change. In the second of those runs 9 stayed on for 10.08 s, longer than the static 5.9 s, with changes 2.5 and 5.0 s apart, so the timeout may run from the last change; the runs do not settle that. Which physical height those edges mark is not documented.'
)
# Flasher circuits whose second printed bulb no retained source places.
PARTLY_PLACED_FLASHERS = {
	14: "the location drawing gives two callout-14 leaders; the first ends on the center arrow insert where the table's f114 light sits, and the second on lamp 45's own insert (the lamp drawing's lamp-45 leader reaches the same insert), where the table models no flasher. The table's second bound light, f114a, sits on an unlabelled round insert that neither drawing gives a callout, so it is not used",
	16: "the table models one dome (the on-ramp flasher at the upper left, where the manual's callout 16 leads); the jet-bumper bulb has no drawn or modelled location",
	26: "the table models one dome (the center-ramp flasher where callout 02C leads); the building bulb has no drawn or modelled location",
	27: "the table models one dome (beside the top jet bumper and spinner, where callout 03C leads); the second bulb has no drawn or modelled location",
}
GI_UPPER = [
	("GI_3", 0.787533, 0.438798), ("GI_32", 0.669476, 0.253583), ("GI_27", 0.698848, 0.085279), ("GI_26", 0.814336, 0.043501),
	("GI_25", 0.195889, 0.098076), ("GI_22", 0.512071, 0.266658), ("GI_12", 0.324028, 0.078103), ("GI_19", 0.940243, 0.130995),
	("GI_4", 0.823316, 0.338276), ("GI_24", 0.488128, 0.251857), ("GI_23", 0.711806, 0.173408), ("GI_18", 0.680843, 0.022201),
	("GI_11", 0.051866, 0.130145),
]
GI_LOWER = [
	("GI_31", 0.732861, 0.492107), ("GI_30", 0.863965, 0.653396), ("GI_29", 0.776508, 0.795694), ("GI_20", 0.155251, 0.803882),
	("GI_10", 0.089682, 0.634357), ("GI_17", 0.246056, 0.769966), ("GI_16", 0.668256, 0.769254), ("GI_15", 0.092857, 0.575005),
	("GI_14", 0.108710, 0.621530), ("GI_13", 0.839114, 0.642194), ("GI_7", 0.842481, 0.502406), ("GI_5", 0.757146, 0.461955),
	("GI_2", 0.697448, 0.820815), ("GI_1", 0.220784, 0.823946), ("GI_33", 0.220852, 0.448738), ("GI_8", 0.063362, 0.407909),
	("GI_6", 0.225522, 0.426410), ("GI_9", 0.062701, 0.460853),
]
VIRTUAL_SOLENOIDS = {
	23: ("Game-On / Special-Solenoid Enable", "used", ["internal.game-on-enable"], "CORE_SSFLIPENSOL / S11_GAMEONSOL: the ROM's flipper and special-solenoid enable. It has no driver-board output of its own. In the esha_la3 harness runs it is already on at the first sample while the ROM sits at FACTORY SETTING, goes off just after the Advance that enters Game-Over mode, and comes back on when a game starts."),
	24: ("Unassigned Solenoid Slot 24", "unused", ["internal.unused-platform-slot"], "Reserved gap between the enable (23) and the C-side aliases (25-32); no System 11 driver populates it."),
	33: ("Unused Upper Flipper Slot 33", "unused", ["internal.unused-platform-slot"], "Generic upper-flipper-coil address (CORE_FIRSTUFLIPSOL). eshaGameData declares FLIP_SWNO(58,57) with no FLIP_SOL bit, so nothing drives 33-36; the upper-left flipper is wired to the left flipper button and has no CPU output."),
	34: ("Unused Upper Flipper Slot 34", "unused", ["internal.unused-platform-slot"], "See address 33."),
	35: ("Unused Upper Flipper Slot 35", "unused", ["internal.unused-platform-slot"], "See address 33."),
	36: ("Unused Upper Flipper Slot 36", "unused", ["internal.unused-platform-slot"], "See address 33."),
	37: ("Unused Sound Overlay Slot 37", "unused", ["internal.unused-platform-slot"], "System 11 sound-overlay board range 37-44. eshaGameData sets gameSpecific1 = S11_MUXSW2 only, without S11_SNDOVERLAY, and the manual lists no sound overlay board, so 37-44 stay zero."),
	38: ("Unused Sound Overlay Slot 38", "unused", ["internal.unused-platform-slot"], "See address 37."),
	39: ("Unused Sound Overlay Slot 39", "unused", ["internal.unused-platform-slot"], "See address 37."),
	40: ("Unused Sound Overlay Slot 40", "unused", ["internal.unused-platform-slot"], "See address 37."),
	41: ("Unused Sound Overlay Slot 41", "unused", ["internal.unused-platform-slot"], "See address 37."),
	42: ("Unused Sound Overlay Slot 42", "unused", ["internal.unused-platform-slot"], "See address 37."),
	43: ("Unused Sound Overlay Slot 43", "unused", ["internal.unused-platform-slot"], "See address 37."),
	44: ("Unused Sound Overlay Slot 44", "unused", ["internal.unused-platform-slot"], "See address 37."),
	45: ("Synthetic Lower Right Flipper Power", "used", ["internal.synthetic-flipper"], "PinMAME fabricates 45/46 from right flipper button 57 because eshaGameData declares FLIP_SWNO(58,57) with no FLIP_SOL bit. The lower right flipper (FL-11630) is wired straight from its cabinet switch through the Orn-Vio circuit (1P19-1) with no CPU output; this address is the emulator's view of that button, not a driver."),
	46: ("Synthetic Lower Right Flipper Hold", "used", ["internal.synthetic-flipper"], "See address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", ["internal.synthetic-flipper"], "PinMAME fabricates 47/48 from left flipper button 58. The left cabinet switch (Orn-Gry circuit, 1P19-2) fires both the lower left flipper (FL-11630) and the upper left flipper (FL-11722) directly; neither has a CPU output."),
	48: ("Synthetic Lower Left Flipper Hold", "used", ["internal.synthetic-flipper"], "See address 47."),
	49: ("Simulator Ball-Shooter Slot", "unused", ["internal.unused-platform-slot"], "CORE_FIRSTSIMSOL: the PinMAME simulator's fake ball-shooter solenoid, not System 11 hardware."),
	50: ("Unassigned Solenoid Slot 50", "unused", ["internal.unused-platform-slot"], "Gap before the custom-solenoid base; eshaGameData declares no custom solenoids, so PinMAME models 50 solenoid slots for this game."),
}

# --- Lamps (Lamp-Matrix Table printed 67; locations list printed 69) -----------------------------
LAMP_LABELS = {
	1: "Captive Ball 25K", 2: "Captive Ball 50K", 3: "Captive Ball 100K", 4: "Captive Ball 150K", 5: "Captive Ball 250K",
	6: "Captive Ball Arrow (Zone 9)", 7: "Spinner 3000 When Lit", 8: "Jet Bumper Center 5000 When Lit", 9: "Bonus 2X", 10: "Bonus 3X",
	11: "Bonus 4X", 12: "Bonus 5X", 13: "Bonus 6X / Lites Extra Ball", 14: "Bonus 6X / Lites Special", 15: "Left Return Lane (Zone 8)",
	16: "Left Outlane Special", 17: "Building Window 7", 18: "Building Window 8", 19: "Building Window 9", 20: "Building Window 4",
	21: "Building Window 5", 22: "Building Window 6", 23: "Building Window 1", 24: "Building Window 2", 25: "Building Window 3",
	26: "Right Standup High (Zone 2)", 27: "Right Standup Low (Zone 3)", 28: "Right Standup 50K",
	29: "Right Inside Return Lane (Zone 7)", 30: "Right Outside Return Lane / Light Spinner", 31: "Right Outlane Special",
	32: "Shoot Again", 33: "Ramp Miles 1", 34: "Ramp Miles 2", 35: "Ramp Miles 3", 36: "Ramp Miles 4", 37: "Ramp Miles 5",
	38: "Ramp Miles 10", 39: "Ramp Miles 20", 40: "Ramp Miles 30", 41: "Top Jet Bumper", 42: "Left Jet Bumper",
	43: "Right Jet Bumper", 44: "Right Ramp Jackpot Arrow", 45: "Right Ramp Lock Arrow", 46: "Right Ramp 3 Miles / Million Arrow",
	47: "Center Ramp 100K / 50000 Arrow", 48: "Center Ramp 2 Miles Arrow", 49: "Left Road Sign", 50: "Left Standup (Zone 1)",
	51: "Eject Hole Lock Arrow", 52: "Eject Hole (Zone 5)", 53: "Center Standup (Zone 4)", 54: "Drop Hole Extra Ball Arrow",
	55: "Drop Hole Lock Arrow", 56: "Under Fault Loop (Zone 6)", 57: "Right Road Sign",
	58: "Jackpot 500K + Special", 59: "Jackpot 1 Million", 60: "Jackpot 1.25 Million", 61: "Jackpot 1.5 Million",
	62: "Jackpot 1.5 Million + Extra Ball", 63: "Jackpot 2 Million", 64: "Jackpot 2.5 Million",
}
LAMP_MATRIX_WORDING = {
	1: "Captive Ball 1 (low)", 2: "Captive Ball 2", 3: "Captive Ball 3", 4: "Captive Ball 4", 5: "Captive Ball 5 (high)",
	7: "Spinner", 8: "Jet Bumper Center", 13: "BONUS 6X/Lites Ex. Ball", 14: "BONUS 6X/Lites Special", 15: "L Return Lane",
	16: "Left Outlane", 26: "Right Standup (High)", 27: "Right Standup (Low)", 28: "Right Standup 50K", 29: "R Inside Return Lane",
	30: "R Outside Return Lane", 31: "Right Outlane", 33: "Miles 1", 34: "Miles 2", 35: "Miles 3", 36: "Miles 4", 37: "Miles 5",
	38: "Miles 10", 39: "Miles 20", 40: "Miles 30", 44: "Right Ramp Jackpot", 45: "Right Ramp Lock", 46: "Right Ramp 3 Miles",
	47: "Center Ramp 100K", 48: "Center Ramp 2 Miles", 51: "Eject Lock", 52: "Eject Top", 54: "Drop Hole Extra Ball", 55: "Drop Hole Lock",
	56: "Under Fault Loop", 58: "Jackpot (SP) 1", 59: "Jackpot (SP) 2", 60: "Jackpot (SP) 3", 61: "Jackpot (SP) 4", 62: "Jackpot (SP) 5",
	63: "Jackpot (SP) 6", 64: "Jackpot (SP) 7",
}
LAMP_LIST_WORDING = {
	1: "25K (Captive Ball, lowest)", 2: "50K (Captive Ball, lower)", 3: "100K (Captive Ball, mid)", 4: "150K (Captive Ball, higher)",
	5: "250K (Captive Ball, highest)", 6: "Zone 9 (Captive Ball arrow)", 7: "3000 W/LIT (Spinner)", 8: "5000 W/LIT (J Bumper Center)",
	16: "SPECIAL (Left Outlane)", 28: "50000 (R Standup)", 29: "Zone 7 (R Inner Return Lane)", 30: "Light Spinner (R Out. Ret Lane)",
	31: "SPECIAL (Right Outlane)", 44: "JACKPOT arrow (R Ramp)", 45: "LOCK arrow (R Ramp)", 46: "MILLION arrow (R Ramp)",
	47: "50000 arrow (Cntr Ramp)", 48: "2 Miles arrow (Cntr Ramp)", 51: "LOCK arrow (Eject Hole)", 52: "Zone 5 (Eject Hole)",
	53: "Zone 4 (Eject Hole)", 54: "Extra Ball arrow (Drop Hole)", 55: "LOCK arrow (Drop Hole)", 56: "Zone 6 (under Fault Loop)",
	58: "500K + SPECIAL (Jackpot Value, spkr panel)", 59: "1 Million (Jackpot Value, spkr panel)", 60: "1.25 Million (Jackpot Value, spkr panel)",
	61: "1.5 Million (Jackpot Value, spkr panel)", 62: "1.5 Million + Ex. Ball (Jackpot Value, spkr panel)", 63: "2 Million (Jackpot Value, spkr panel)",
	64: "2.5 Million (Jackpot Value, spkr panel)",
}
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"), 4: ("YEL-BLK", "1J7-4", "Q60"),
	5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"), 7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"), 4: ("RED-YEL", "1J6-5", "Q83"),
	5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"), 7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
SPEAKER_PANEL_LAMPS = set(range(58, 65))
BUILDING_LAMPS = set(range(17, 26))
# Window centres per column, from the retained InstituteWindow1-9 meshes: the centre of each mesh's local
# bounding box, scaled by 100, rotated by ObjRotZ 22 degrees (VPX: x' = x cos - y sin, y' = x sin + y cos),
# and moved to the primitives' shared position (440.5, 438.0). Rows differ only in height.
BUILDING_WINDOW_COLUMNS = {"left": (0.396848, 0.207947), "centre": (0.448657, 0.217280), "right": (0.496020, 0.225813)}
LAMP_POSITIONS = {
	1: ("L1", 0.539700, 0.733793), 2: ("L2", 0.570928, 0.703300), 3: ("L3", 0.601749, 0.673183), 4: ("L4", 0.636383, 0.644811),
	5: ("L5", 0.666472, 0.614831), 6: ("L6", 0.703434, 0.578904), 7: ("L7", 0.291151, 0.225212), 8: ("l8", 0.189558, 0.298524),
	9: ("L9", 0.317032, 0.791021), 10: ("L10", 0.384103, 0.807329), 11: ("L11", 0.455520, 0.813886), 12: ("L12", 0.528847, 0.807816),
	13: ("L13", 0.592750, 0.790171), 14: ("L14", 0.455644, 0.779938), 15: ("L15", 0.202539, 0.673182), 16: ("L16", 0.063987, 0.690598),
	26: ("L26", 0.649742, 0.517262), 27: ("L27", 0.672759, 0.540862), 28: ("L28", 0.771198, 0.586677), 29: ("L29", 0.692786, 0.673709),
	30: ("L30", 0.798917, 0.678016), 31: ("L31", 0.865368, 0.706958), 32: ("L32", 0.455587, 0.882375), 33: ("L33", 0.384346, 0.733129),
	34: ("L34", 0.358807, 0.705464), 35: ("L35", 0.335677, 0.679108), 36: ("L36", 0.308400, 0.651290), 37: ("L37", 0.285017, 0.624753),
	38: ("L38", 0.219623, 0.623048), 39: ("L39", 0.258091, 0.595490), 40: ("L40", 0.326928, 0.602444), 41: ("l41", 0.172409, 0.241360),
	42: ("l42", 0.091791, 0.327879), 43: ("l43", 0.295941, 0.316903), 44: ("L44", 0.486515, 0.469155), 45: ("L45", 0.579186, 0.442136),
	46: ("L46", 0.668811, 0.421178), 47: ("L47", 0.544602, 0.404348), 48: ("L48", 0.563533, 0.354548), 49: ("Primitive.L49 bulb-cover mesh", 0.563561, 0.335039),
	50: ("L50", 0.288565, 0.524341), 51: ("L51", 0.343882, 0.490956), 52: ("L52", 0.320496, 0.441057), 53: ("L53", 0.621556, 0.355379),
	54: ("L54", 0.692010, 0.324149), 55: ("L55", 0.716906, 0.280953), 56: ("L56", 0.670713, 0.362838), 57: ("Primitive.L57 bulb-cover mesh", 0.774870, 0.398662),
}
BUILDING_WINDOW_ROWS = {23: "bottom left", 24: "bottom centre", 25: "bottom right", 20: "middle left", 21: "middle centre", 22: "middle right", 17: "top left", 18: "top centre", 19: "top right"}

# --- Helpers ---------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Earthshaker retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Earthshaker extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Earthshaker retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(extraction_root)):
		raise RuntimeError(f"Earthshaker retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Earthshaker retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": {"status": status, "source_refs": list(source_refs)}})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(label: str) -> str:
	return "device." + "-".join("".join(character if character.isalnum() else " " for character in label.casefold()).split())


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address}, "availability": availability, "provenance": provenance(*refs)}
	device.update(extra)
	return device


EXCERPTS = (
	("solenoid-table", "PDF page 34, printed 30, EARTHSHAKER Solenoid Table and notes", "earthshaker.pdf page 34, crop box 0.11,0.3,0.88,0.77, scanned page rendered at its native resolution (embedded image xref 234, 2550px across 8.50in), rendered at 122 dpi, capped to 800px wide, grayscale, 801x633 WebP quality 50"),
	("solenoid-locations", "PDF page 69, printed 65, Solenoids/Flashers list and location drawing", "earthshaker.pdf page 69, crop box 0.09,0.06,0.56,0.66, scanned page rendered at its native resolution (embedded image xref 339, 2550px across 8.50in), rendered at 130 dpi, capped to 520px wide, grayscale, 521x860 WebP quality 65"),
	("switch-matrix", "PDF pages 71 (printed 67, wiring diagram) and 72 (printed 68, EARTHSHAKER Switch-Matrix Table)", "earthshaker.pdf page 72, crop box 0.09,0.63,0.89,0.945, scanned page rendered at its native resolution (embedded image xref 348, 2550px across 8.50in), rendered at 147 dpi, capped to 1000px wide, grayscale, 1001x510 WebP quality 80"),
	("switch-locations", "PDF page 70, printed 66, Switches list and location drawing", "earthshaker.pdf page 70, crop box 0.08,0.06,0.93,0.93, scanned page rendered at its native resolution (embedded image xref 342, 2550px across 8.50in), rendered at 83 dpi, capped to 600px wide, grayscale, 601x796 WebP quality 55"),
	("lamp-matrix", "PDF pages 71 (printed 67, EARTHSHAKER Lamp-Matrix Table) and 72 (printed 68, wiring diagram)", "earthshaker.pdf page 71, crop box 0.11,0.645,0.91,0.95, scanned page rendered at its native resolution (embedded image xref 345, 2550px across 8.50in), rendered at 147 dpi, capped to 1000px wide, grayscale, 1001x494 WebP quality 80"),
	("lamp-locations", "PDF page 73, printed 69, Lamps list and location drawing", "earthshaker.pdf page 73, crop box 0.2,0.05,0.9,0.92, scanned page rendered at its native resolution (embedded image xref 351, 2550px across 8.50in), rendered at 101 dpi, capped to 600px wide, grayscale, 601x966 WebP quality 55"),
	("mechanism-assemblies", "PDF pages 56, 57, 61-64, printed 52, 53, 57-60: 3-bank drop target and opto board, ball poppers, zone opener, building, shaker, and state assemblies (image: printed 59, Building Assembly)", "earthshaker.pdf page 63, crop box 0.2,0.04,0.8,0.83, scanned page rendered at its native resolution (embedded image xref 321, 2550px across 8.50in), rendered at 118 dpi, capped to 600px wide, grayscale, 600x1024 WebP quality 80"),
	("game-play", "PDF page 12, printed 8, EARTHSHAKER GAME PLAY (rules)", None),
	("flippers-and-boards", "PDF pages 51-52, printed 47-48: lamp boards, G.I. relay boards, and flipper assemblies (image: printed 47)", "earthshaker.pdf page 51, crop box 0.1,0.02,0.95,0.94, scanned page rendered at its native resolution (embedded image xref 285, 2550px across 8.50in), rendered at 97 dpi, capped to 700px wide, grayscale, 701x981 WebP quality 80"),
)


def _excerpt(name: str, locator: str, derivation: str | None, *, method: str = "manual", transcribed_by: str = "curator, read from the rendered page") -> dict[str, Any]:
	text_path = EXCERPT_DIRECTORY / f"{name}.md"
	record: dict[str, Any] = {
		"id": f"excerpt.earthshaker.{name}",
		"locator": locator,
		"path": text_path.relative_to(ROOT).as_posix(),
		"sha256": hashlib.sha256(text_path.read_bytes()).hexdigest(),
	}
	if derivation is not None:
		image_path = EXCERPT_DIRECTORY / f"{name}.webp"
		record["image"] = image_path.relative_to(ROOT).as_posix()
		record["image_sha256"] = hashlib.sha256(image_path.read_bytes()).hexdigest()
		record["image_derivation"] = derivation
	record.update({"method": method, "transcribed_by": transcribed_by, "reviewed": True})
	return record


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned PinmameGetGames catalog records for the nine-driver esha_* clone tree rooted at esha_la3",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c: INITGAME(esha,GEN_S11B,s11_dispS11b2,12,FLIP_SWNO(58,57),S11_LOWALPHA|S11_DISPINV,S11_MUXSW2) (no "
				"sxx.ssSw map, no custom solenoids, no sound overlay), the esha_* ROM sets, CORE_GAMEDEF(esha,la3) and the eight "
				"CORE_CLONEDEFs with their comments (pa4 'supports collapsable building, aka Phil Dixons version'), input_ports_esha = "
				"input_ports_s11; src/wpc/s11.c: s11_dispS11b2 (two 16-character sixteen-segment rows), MACHINE_INIT(s11)'s esha_ block "
				"typing 10 'Upper Playfield GI', 11 'Backbox GI', and 15 'Lower Playfield GI' as reverse-acting #44 G.I. and 14, 16, and "
				"the 25-32 mux bank as #89 flashers, SWITCH_UPDATE(s11) copying the mux relay's state into switch 2 under S11_MUXSW2, "
				"setSSSol's WMS ssSolNo {5,4,1,2,0,3} special-solenoid map, updsol's A/C mux copy, and the switch read returning "
				"core_getSwCol without inversion; src/wpc/s11.h S11_COMPORTS and S11_SWADVANCE/-UPDN/-CPUDIAG/-SOUNDDIAG; src/wpc/core.c "
				"core_updateSw's FLIP_SWNO flipper copy and synthetic 45-48 states; src/wpc/core.h CORE_SSFLIPENSOL, CORE_FIRSTLFLIPSOL, "
				"CORE_FIRSTSIMSOL."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, A/C mux, special-solenoid, and per-game G.I. address rules",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://archive.org/details/williams-earthshaker-pinball-manual",
			"source_id": "williams-earthshaker-pinball-manual", "original_filename": "earthshaker.pdf", "sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T13:35:00Z",
			"locator": (
				"Williams Earthshaker! operations manual (game number 568), 114-page scan with an OCR text layer (Internet Archive item "
				"williams-earthshaker-pinball-manual, file https://archive.org/download/williams-earthshaker-pinball-manual/earthshaker.pdf, "
				"uploader kay@barkbark.zone, public date 2026-07-12, Internet Archive SHA-1 cec2ab145ff4509a96f1e28a26cff35a2e136ecb). PDF page = "
				"printed page + 4. Tables were read from renders of the native 300 ppi page images because the OCR layer interleaves "
				"columns. Retained locally under external:pinmame-manuals/by-machine/williams.earthshaker.1989/."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive", "rights": "NOASSERTION",
			"excerpts": [_excerpt(name, locator, derivation) for name, locator, derivation in EXCERPTS],
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:pinmame-review-artifacts/earthshaker/rom-name-tables/",
			"revision": "eshk_u26.l3",
			"locator": (
				"Switch and coil name tables of the U26 program ROM of every esha_* set in the local corpus (la3, la1, lg1, lg2, ma3, pa1, pr4), "
				"decoded by tools/s11_rom_name_tables.py: 58 switch entries in public-address order and 30 coil entries in coil-test order. "
				"The decoded JSON per set is retained beside the ROM member SHA-256s listed in the excerpt."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games program ROMs, user-authorized local copies; ROM bytes are not redistributed",
			"excerpts": [_excerpt("rom-name-tables", "U26 switch tables at the listed offsets (entries 1-58) and coil tables (entries 1-30) for seven esha_* sets", None, method="mixed", transcribed_by="tools/s11_rom_name_tables.py, reviewed by curator")],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{LA3_RUNTIME_PATH}", "revision": PINMAME_REVISION,
			"locator": (
				"Pinned LibPinMAME runs of esha_la3 from empty NVRAM: the Auto Burn-in coil test paired step by step with the ROM coil table; "
				"Game-Over entry and game start with drop-target switches 27-29 held at 1 and at 0; Game-Over entry with building switches "
				"25/26 held at 01, 10, and 11; and seven runs in which the host moves a modelled building while solenoid 9 is on."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": PA1_RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{PA1_RUNTIME_PATH}", "revision": PINMAME_REVISION,
			"locator": "Pinned LibPinMAME runs of the esha_pa1 prototype from empty NVRAM: the Auto Burn-in coil test (step 17, public 9, BUILDING MOTOR) and Game-Over entry with 25/26 at 0.",
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/earthshaker-1989/source/Earthshaker%20%28Williams%201989%29_VPW-Lite_v006.vpx",
			"original_filename": "Earthshaker (Williams 1989)_VPW-Lite_v006.vpx", "sha256": TABLE_SHA256, "acquired_at": "2026-09-25T13:34:00Z",
			"locator": (
				f"Retained VPW-Lite v006 recreation (table version 0.9a) from the contributor's existing table collection. Exact playfield "
				f"bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority for named table objects only."
			),
			"license": "NOASSERTION", "attribution": "32assassin; VPin Workshop mod by Bord, benji, oqqsan, Sixtoe, and Uncle_Paulie", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/earthshaker-1989/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True, "acquired_at": "2026-09-25T13:34:00Z",
			"locator": (
				"Retained embedded script (84,666 bytes). Runtime authority: cGameName = \"esha_la3\"; SolCallback 1-7, 9, 10, 12-16, 22, 25-32 "
				"and sLRFlipper/sLLFlipper; UpdateLamps' NFadeL bindings of lamps 1-16 and 26-64 and its FadeObj bindings of building lamps "
				"17-25 to InstituteWindow1-9; the three-ball trough (sw11-13), drain (sw10), eject saucer (sw20), 3-bank cvpmDropTarget "
				"(27-29, reset by 3), top and bottom VUK poppers (37/13 and 40/6), California/Nevada fault (4, switch 42 on the open "
				"stroke), building motor model (9, switches 25/26), shaker (22), and G.I. relays 10 and 15 (lights off while energized)."
			),
			"license": "NOASSERTION", "attribution": "32assassin; VPin Workshop mod by Bord, benji, oqqsan, Sixtoe, and Uncle_Paulie", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/earthshaker-1989/extracted-vpxtool.manifest.json", "acquired_at": "2026-09-25T13:34:00Z",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, "
				f"produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	]


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address - 1, 8)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column + 1]
	return_wire, return_connection = SWITCH_ROW_WIRING[row + 1]
	return {
		"board": "System 11B CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role, note) in DEDICATED_SWITCHES.items():
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], normally_closed=False, roles=[role],
			physical={"location": "coin door diagnostic switch assembly / CPU board", "switch_type": "button" if address != -6 else "other", "notes": note + " Read from System 11's dedicated column, not the playfield matrix."},
			spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
		))
	for address in range(1, 65):
		column, row = divmod(address - 1, 8)
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		notes = [f"Printed switch-matrix column {column + 1} ({SWITCH_COLUMN_WIRING[column + 1][0]}), row {row + 1} ({SWITCH_ROW_WIRING[row + 1][0]})."]
		if address in ROM_SWITCH_NAMES:
			notes.append(f"The esha_la3 switch table names it \"{ROM_SWITCH_NAMES[address]}\".")
		else:
			notes.append("The esha_la3 switch table ends at entry 58, so this address has no ROM name.")
		if address in MATRIX_WORDING:
			notes.append(f"The matrix table (printed 68) prints \"{MATRIX_WORDING[address]}\".")
		if address in LIST_WORDING:
			notes.append(f"The switches list (printed 66) prints \"{LIST_WORDING[address]}\".")
		physical: dict[str, Any] = {}
		if address in SWITCH_PARTS:
			physical["part_number"] = SWITCH_PARTS[address]
		if address in SWITCH_TYPES:
			physical["switch_type"] = SWITCH_TYPES[address]
		elif SWITCH_PARTS.get(address, "").startswith(MICROSWITCH_PART_PREFIX):
			physical["switch_type"] = "microswitch"
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]}
		availability = "used"
		if unused:
			availability = "unused"
			notes.append("Both the matrix table and the switches list leave this position empty (\"Not Used\").")
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
		elif address == 2:
			notes.append(
				"The switches list prints item 2 \"Not Used\" because no playfield switch sits here; the matrix table's \"C Side Power A/C Relay\" "
				"names what the position reads instead: the C-side power contact of the A/C select relay (12). eshaGameData sets S11_MUXSW2, so "
				"pinned SWITCH_UPDATE(s11) overwrites public switch 2 with the live state of solenoid 12 every update; a recreation reads it and never drives it."
			)
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
			refs = (MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
		elif address in CABINET_SWITCH_ROLES:
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address == 5:
				availability = "optional"
				notes.append("The switches list prints \"Not Used (USA)\" as its part number: US machines ship a two-chute door, so the center chute is fitted only on other doors (09-17003-x three-chute door).")
			if address in (4, 6):
				notes.append("The switches list and the ROM put the right chute on 4 and the left on 6; the matrix table prints them the other way round. The list and ROM are followed.")
			if address == 9:
				notes.append("The retained script uses it as the nudge tilt (vpmNudge.TiltSwitch = 9).")
				refs = refs + (VPX_SCRIPT_SOURCE,)
			if address in (57, 58):
				side = "right" if address == 57 else "left"
				notes.append(
					f"The switches list names it \"{side.capitalize()} Flipper Lane Change\" with footnote **1, \"Optotransistor on Backbox "
					f"Interconnect Bd\"; the manual does not say more about how it senses the {side} flipper button. The cabinet switch itself "
					"(SW-10A-48 right, SW-1010-13 left) fires the flipper coil directly. eshaGameData declares FLIP_SWNO(58,57) without FLIP_SOL, "
					f"so pinned core_updateSw rewrites this address from the {side} flipper button bit on every update: public 1 means the button "
					f"is pressed, a host write here is overwritten, and a consumer presses the {side} flipper through public {82 if address == 57 else 84}. "
					"The retained script writes Controller.Switch(57/58) directly from its flipper keys; that is consumed-table behaviour, not "
					"a path a recreation should copy."
				)
				refs = refs + (VPX_SCRIPT_SOURCE,)
		elif address in PROTOTYPE_SWITCHES:
			availability = "optional"
			notes.append(
				"The switches list prints it as p/o C-12406 with footnote **2, an optotransistor on the Bldg Positioner board, but the matrix table "
				"leaves the cell empty and the production Building Assembly (B-12728) has no motor, slide, or opto. Every production ROM in the corpus "
				"names it BLDNG. 1/2 UNUSED; only the esha_pa1 prototype names it BLDNG HEIGHT 1/2. It is fitted only with the prototype sinking "
				"building (and owner retrofits of it). Which physical height each opto marks is not documented; see solenoid 9."
			)
			notes.append(SWITCH_PROJECTIONS[address])
			refs = (MANUAL_SOURCE, ROM_SOURCE, PA1_RUNTIME_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address][1:]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status="observed")
		else:
			object_name = SWITCH_POSITIONS[address][0]
			if address in SWITCH_PROJECTIONS:
				notes.append(SWITCH_PROJECTIONS[address])
			else:
				notes.append(f"Placed at the retained table object {object_name}.")
			if address in BUMPER_SCRIPT_PULSE:
				notes.append(
					"The manual's switch drawing puts 54 on the uppermost bumper, 53 on the right one, and 52 on the leftmost, matching the ROM's "
					f"names and the lamp and coil drawings; the retained script's {BUMPER_SCRIPT_PULSE[address]}, which swaps 52 and 54. "
					"The placement follows the manual; the swap is a defect of the retained table."
				)
			if address in (27, 28, 29):
				notes.append(
					"One of three opto interrupters on the 3-Bank Drop Target Opto Board (C-12559), whose LM339 comparators drive the matrix rows. "
					"s11.c reads the matrix without inversion, and the ROM treats 1 as a dropped target: with 27-29 held at 1 it fired the reset "
					"coil (3) seven times after Game-Over entry and seven more after Start, against once each with them at 0. The matrix contact "
					"therefore rests open while the target stands."
				)
				refs = refs + (RUNTIME_SOURCE,)
			refs = refs + (VPX_SCRIPT_SOURCE,)
			extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address][1:]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		physical["notes"] = " ".join(notes)
		extra["physical"] = physical
		extra["wiring"] = _switch_wiring(address)
		if availability in ("used", "optional") and address not in PROTOTYPE_SWITCHES:
			# No source or run says which level the ROM treats as the prototype optos' rest state.
			extra["normally_closed"] = False
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))
	items.append(_device(
		"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used", (CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={"location": "System 11B CPU board", "switch_type": "dip", "notes": "S11 input port 1 'Country' jumper (0 = USA, 1 = Germany), read by the ROM through PIA2."},
		spatial=not_applicable("dip_switch", CORE_SOURCE),
	))
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	def emit(identifier: str, label: str, kind: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> None:
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))

	def rom_note(address: int) -> str:
		return f" The esha_la3 coil test names it \"{ROM_COIL_NAMES[address]}\"." if address in ROM_COIL_NAMES else ""

	def callback_note(address: int) -> str:
		return f" Retained script: {SOLENOID_CALLBACKS[address]}." if address in SOLENOID_CALLBACKS else ""

	for address, (label, kind, wire, control, power, driver, part) in SOLENOID_A.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address:02d}A (Switched): pulsed while the A/C select relay (12) is released." + rom_note(address) + callback_note(address)
		wiring = {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power}
		refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = refs + (VPX_SCRIPT_SOURCE,)
		physical: dict[str, Any] = {}
		if part:
			physical["part_number"] = part
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}A"}], "wiring": wiring}
		availability = "used"
		if address == 8:
			availability = "unused"
			notes += " The table prints 08A \"Not Used\" with no part; its driver Q22 and harness pin exist only for the C side (32). The coil test still steps through it."
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
			identifier = "device.not-used-switched-solenoid-08a"
		elif address == 7:
			notes += " The Solenoids/Flashers list prints \"Knocker/Ticket Dispenser (b)\": the same drive serves a ticket dispenser where one is fitted. A cabinet device."
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			object_name, positions = SOLENOID_POSITIONS[address]
			notes += f" Placed at {object_name}."
			if address == 6:
				notes += " The Solenoids/Flashers list prints AE-24-900 for 06A; the Solenoid Table and the Bottom Ball Popper Assembly (D-12642, whose D-11335-2 popper lists coil AE-23-800) agree on AE-23-800."
			if address == 4:
				notes += " The coil drives the Zone Opener Assembly (C-12429): a threaded plunger turns a flat cam on the zone-opener shaft, so each pulse toggles the fault between closed and open, and a roller micro-switch (42) reports open."
			extra["spatial"] = located(identifier, "effect", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		emit(identifier, label, kind, address, availability, refs, **extra)

	for address, (label, kind, wire, control, power, driver, part) in SOLENOID_CONTROLLED.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address:02d} (Controlled)." + rom_note(address) + callback_note(address)
		wiring = {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power}
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = refs + (VPX_SCRIPT_SOURCE,)
		physical: dict[str, Any] = {}
		if part:
			physical["part_number"] = part
		extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}], "wiring": wiring}
		availability = "used"
		if address == 9:
			availability = "optional"
			refs = refs + (PA1_RUNTIME_SOURCE,)
			notes += (
				" The Solenoid Table prints 09 \"Not Used\" with no part and the production Building Assembly (B-12728) has no motor, but the "
				"Solenoids/Flashers list prints \"Building Motor Relay\" (5580-12145-01) and, as a separate item, \"Building Motor\" (14-7941-1), "
				"and the esha_pa1 prototype's coil test names this step BUILDING MOTOR. Q17 therefore drives the coil of a relay that switches "
				"the building motor. The location drawing's callout 9 leads down into the Institute building, but no page shows the relay's "
				"board or the motor's supply. Both are fitted only with the prototype sinking building. The two ROMs run here still drive it: "
				"esha_la3 and esha_pa1 both energize 9 on entering Game-Over mode and, when switches 25/26 never change, release it after about "
				"5.9 s. " + BUILDING_RULE
			)
			extra["physical"] = dict(physical, notes=notes)
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			emit(identifier, label, kind, address, availability, refs, **extra)
			continue
		if address in (10, 11, 15):
			board = "C-11902-1" if address in (10, 15) else "C-11998-1"
			notes += (
				f" A 24 V relay on the {board} relay board per the board's own parts page (manual printed 47, which prints the relay as "
				+ ("5580-12145-00" if address in (10, 15) else "5580-09555-01") + "). The Solenoid Table's note 4 prints the board letters the other "
				"way round, and the Solenoids/Flashers list's footnote puts all three G.I. relays on C-11998-1"
				+ (" and prints this relay as 5580-12145-01" if address == 11 else "") + ". "
				"G.I. is lit while the relay is released and dark while it is energized: pinned s11.c types the address as reverse-acting #44 "
				"G.I., and the retained script turns its lights off when the callback is enabled."
			)
		if address == 10:
			extra["roles"] = ["gi.upper-playfield"]
			notes += f" The retained table's GIU collection holds {len(GI_UPPER)} bulbs for it; the manual prints no G.I. bulb count."
			extra["spatial"] = located(identifier, "emitter", [(x, y) for _, x, y in GI_UPPER], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
			physical["quantity"] = len(GI_UPPER)
		elif address == 15:
			extra["roles"] = ["gi.lower-playfield"]
			notes += f" The retained table's GI collection holds {len(GI_LOWER)} bulbs for it; the manual prints no G.I. bulb count."
			extra["spatial"] = located(identifier, "emitter", [(x, y) for _, x, y in GI_LOWER], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE)
			physical["quantity"] = len(GI_LOWER)
		elif address == 11:
			extra["roles"] = ["cabinet.backbox"]
			notes += " The insert board is the backbox lamp insert behind the backglass; pinned s11.c calls it 'Backbox GI'. The retained table does not model it."
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 12:
			extra["roles"] = ["internal.ac-select-relay"]
			notes += " Mounted on the Aux Power Driver board (D-12247) in the backbox. Released, drives 1-8 reach their A-side loads; energized, the same drives reach the C-side loads published as 25-32. Its C-side power contact is read back as switch 2."
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in (14, 16):
			quantity = 2
			physical["quantity"] = quantity
			if address == 14:
				notes += " Two #906 flashlamps (2p). Only the first is placed: " + PARTLY_PLACED_FLASHERS[14] + "."
			else:
				notes += " Two #906/#89 flashlamps (2p). " + PARTLY_PLACED_FLASHERS[16][0].upper() + PARTLY_PLACED_FLASHERS[16][1:] + "."
			extra["spatial"] = located(identifier, "emitter", SOLENOID_POSITIONS[address][1], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		else:
			notes += f" Placed at {SOLENOID_POSITIONS[address][0]}."
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address][1], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		emit(identifier, label, kind, address, availability, refs, **extra)

	for address, (label, wire, control, power, driver, part, special) in SOLENOID_SPECIAL.items():
		identifier = output_id(label)
		notes = f"Solenoid Table entry {address} (Special #{special}); pinned setSSSol maps the special-solenoid PIA outputs onto 17-22 in Special #1-#6 order." + rom_note(address) + callback_note(address)
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Special #{special}"}],
			"wiring": {"board": "System 11B CPU board", "driver_transistor": driver, "drive_wire": wire, "control_connection": control, "power_connection": power},
		}
		if address == 22:
			kind = "motor"
			notes += (
				" The Shaker Assembly (B-12388): an 11 RPM motor (14-7951) turning an eccentric weight, the machine's earthquake shaker. The "
				"Solenoids/Flashers list prints 22 \"Not Used\", but the Solenoid Table and both ROM coil tests name it (QUAKE MOTOR) and the "
				"location drawing gives callout 22 a dashed under-playfield leader. The ROM text also carries a QUAKE INTENSITY adjustment."
			)
			extra["roles"] = ["cabinet.shaker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, ROM_SOURCE)
			refs = refs + (VPX_SCRIPT_SOURCE,)
		else:
			kind = "coil"
			if address == 21:
				notes += " The Solenoids/Flashers list prints \"Lower Jet Bumper\"; the Solenoid Table and the ROM print Top Jet Bumper, and the coil drawing's callout 21 leads to the uppermost bumper."
			notes += f" Placed at {SOLENOID_POSITIONS[address][0]} (manual coil drawing: 21 top, 19 right, 17 left bumper)." if address in (17, 19, 21) else f" Placed at {SOLENOID_POSITIONS[address][0]}."
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address][1], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		extra["physical"] = {"part_number": part, "notes": notes}
		emit(identifier, label, kind, address, "used", refs, **extra)

	for address, (label, availability, roles, note) in VIRTUAL_SOLENOIDS.items():
		refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((RUNTIME_SOURCE,) if address == 23 else ())
		emit(
			output_id(label), label, "virtual", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=roles, physical={"notes": note},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)

	for address, (label, wire, cpu, power, lamp_type, quantity) in SOLENOID_C.items():
		identifier = output_id(label)
		a_address = address - 24
		notes = (
			f"Solenoid Table entry {a_address:02d}C (Switched): driver {SOLENOID_A[a_address][5]} of {a_address:02d}A routed to this load while the "
			f"A/C select relay (12) is energized; pinned updsol publishes it as {address}. {lamp_type}, {quantity}p."
			+ rom_note(address) + callback_note(address)
		)
		refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		object_name, positions = SOLENOID_POSITIONS[address]
		if address in PARTLY_PLACED_FLASHERS:
			notes += " " + PARTLY_PLACED_FLASHERS[address][0].upper() + PARTLY_PLACED_FLASHERS[address][1:] + "."
		else:
			notes += f" Placed at {object_name}."
		if address == 31:
			notes += " The Solenoids/Flashers list prints \"#89/906 Flashlamps\"; the Solenoid Table prints one #906 (1p) and the drawing gives one leader."
		if address == 32:
			notes += " The Solenoids/Flashers list prints one \"#906 Flashlamp\"; the Solenoid Table prints 2p and the drawing gives two 08C leaders."
		emit(
			identifier, label, "flasher", address, "used", refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{a_address:02d}C"}],
			physical={"quantity": quantity, "notes": notes},
			wiring={"board": "System 11B CPU board", "driver_transistor": SOLENOID_A[a_address][5], "drive_wire": wire, "power_connection": f"{power}, CPU {cpu}"},
			spatial=located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE),
		)
	return sorted(items, key=lambda item: item["binding"]["device"])


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, row = divmod(address - 1, 8)
		identifier = f"lamp.matrix-{address}"
		notes = [f"Printed lamp-matrix column {column + 1}, row {row + 1}."]
		if address in LAMP_MATRIX_WORDING:
			notes.append(f"The matrix table (printed 67) prints \"{LAMP_MATRIX_WORDING[address]}\".")
		if address in LAMP_LIST_WORDING:
			notes.append(f"The lamps list (printed 69) prints \"{LAMP_LIST_WORDING[address]}\".")
		if address == 16:
			notes.append("The matrix prints the circled zone-8 marker in this cell, but the lamps list, switch 18, and the rules put zone 8 on the left return lane (lamp 15); the marker's cell is a printing slip.")
		if address == 53:
			notes.append("The list's \"(Eject Hole)\" is wrong: the matrix names the Center Standup (zone 4), switch 30 is the zone-4 target, and the eject hole is zone 5 (lamp 52). The label follows the matrix.")
		refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": {
				"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[column + 1][0], "drive_connection": LAMP_COLUMN_WIRING[column + 1][1],
				"driver_transistor": f"column {LAMP_COLUMN_WIRING[column + 1][2]}, row {LAMP_ROW_WIRING[row + 1][2]}",
				"return_wire": LAMP_ROW_WIRING[row + 1][0], "return_connection": LAMP_ROW_WIRING[row + 1][1],
			},
		}
		if address in SPEAKER_PANEL_LAMPS:
			notes.append("A jackpot-value lamp in the speaker panel under the score displays (\"SP = Speaker Panel\"); the retained table shows it on its backglass.")
			extra["roles"] = ["cabinet.speaker-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in BUILDING_LAMPS:
			notes.append(
				f"One of the nine #555 window lamps on the Building Lamp Board (C-12427) in the Earthquake Institute building ({BUILDING_WINDOW_ROWS[address]} "
				"window as seen from the front; the decal numbers the rows 7 8 9 / 4 5 6 / 1 2 3). The retained script fades InstituteWindow"
				f"{LAMP_LABELS[address].rsplit(' ', 1)[1]} from it. It is placed at the centre of that window's mesh, derived from the retained "
				"primitive's local bounding box, scale, 22-degree rotation, and position; the three windows of a column share x and y and "
				"differ only in height. The bulb socket on C-12427 behind the window is not surveyed, so the placement is observed, not validated."
			)
			extra["physical"] = {"part_number": "C-12427", "quantity": 1}
			column = BUILDING_WINDOW_ROWS[address].split()[1]
			extra["spatial"] = located(identifier, "emitter", [BUILDING_WINDOW_COLUMNS[column]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE, status="observed")
		else:
			object_name = LAMP_POSITIONS[address][0]
			if address in (49, 57):
				notes.append(
					"A red road-sign bulb at a ramp entrance (the drawing's callout 49 leads to the center-ramp entrance and 57 to the "
					f"right-ramp entrance). The retained script fades the l{address} bulb-cover primitive from it (NFadeObjm {address}); that mesh "
					"is baked in table coordinates, so the placement is the centre of its bounding box. The table's glow light "
					f"L{address}a (falloff 150, no bulb mesh) sits within 0.001 of it and is not used."
				)
			else:
				notes.append(f"Placed at the retained light {object_name}.")
			extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address][1:]], VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
		physical = extra.get("physical", {"quantity": 1})
		physical["notes"] = " ".join(notes)
		extra["physical"] = physical
		items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.upper-alphanumeric", "label": "Upper sixteen-character alphanumeric display", "kind": "segment",
			"controller_index": 0, "segment_start": 0, "width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
		{
			"id": "display.lower-alphanumeric", "label": "Lower sixteen-character alphanumeric display", "kind": "segment",
			"controller_index": 1, "segment_start": 20, "width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE), "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		},
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	return [
		mechanism(
			"mechanism.trough", "Outhole and three-ball trough", "kicker",
			[output_id("Outhole Kicker"), output_id("Ball Release (Shooter Lane Feeder)")], ["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-50"],
			"A drained ball rests on the outhole switch (10); the Outhole Kicker (1) kicks it into the trough, which holds three balls on "
			"Trough 3 (13, left), Trough 2 (12), and Trough 1 (11, right). The Ball Release / Shooter Lane Feeder (2) feeds the ball at 11 into "
			"the shooter lane (50), and the stack rolls down. The retained script creates its three balls on 11-13.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.eject-hole", "Eject hole (Zone 5)", "kicker", [output_id("Eject Hole")], ["switch.matrix-20"],
			"A ball in the eject hole closes 20; the Eject Hole coil (5, AE-26-1500) kicks it back out. During Quick Multi-Ball the ROM holds "
			"it there as a temporary lock (rules, printed 8).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.drop-hole-subway", "Drop hole subway and bottom ball popper", "kicker",
			[output_id("Bottom Ball Popper")], ["switch.matrix-38", "switch.matrix-39", "switch.matrix-40"],
			"A ball shot into the drop hole falls under the playfield across Drop Hole 1 (38) and Drop Hole 2 (39) into the Bottom Ball "
			"Popper (D-12642), where it closes 40; the popper coil (6, AE-23-800) lifts it back up to the right return lane (rules, printed "
			"8: 'Before the ball in the Drop Hole pops up to the right return lane, a Match-up award cycle occurs'). The drop hole is one of "
			"the two lock routes.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="D-12642",
		),
		mechanism(
			"mechanism.top-ball-popper", "Top ball popper", "kicker", [output_id("Top Ball Popper")], ["switch.matrix-37"],
			"The right ramp (entry switch 43) climbs the right side to the Top Ball Popper (D-11335-2), where the ball closes 37; the popper "
			"coil (13, AE-23-800) lifts it onto the wire ramp that crosses the top of the playfield to the California/Nevada fault. The "
			"retained script holds the ball until 13 fires.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="D-11335-2",
		),
		mechanism(
			"mechanism.drop-targets", "3-bank drop targets", "drop_target_bank", [output_id("3-Bank Drop Target Reset")], ["switch.matrix-27", "switch.matrix-28", "switch.matrix-29"],
			"Three drop targets (C-11223-1) sensed by the opto interrupters of the C-12559 board; a dropped target reads 1. The reset coil (3, "
			"AE-26-1200) raises all three through one reset plate. Held down in the harness, the ROM retried the reset about every 0.6 s.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_SOURCE, assembly="C-11223-1",
		),
		mechanism(
			"mechanism.california-fault", "California/Nevada fault (zone opener)", "diverter", [output_id("California Fault")], ["switch.matrix-42"],
			"The Zone Opener Assembly (C-12429) under the California and Nevada state maps: each pulse of the California Fault coil (4) turns "
			"a flat cam on the zone-opener shaft one step, so successive pulses open and close the fault; the State Assembly (C-12433) slide "
			"shifts the California map. The roller micro-switch (42, 5647-12073-06) beside the cam reports the open position. The top "
			"popper's wire ramp ends at the fault; the retained table routes that ball down its left exit ramp while the fault is closed and "
			"its right exit ramp while it is open. The retained script toggles an open/closed state on each pulse, slides both map "
			"primitives, swaps the two exit ramps, and sets 42 at the end of the opening stroke. The loop that passes under the fault is "
			"Zone 6 (31 right, 32 left).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE, assembly="C-12429",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Top Jet Bumper")], ["switch.matrix-52", "switch.matrix-53", "switch.matrix-54"],
			"Special solenoids 17 (left), 19 (right), and 21 (top) fire the jet bumpers; their skirt switches are 52, 53, and 54. The manual's "
			"drawings put the top bumper uppermost, the right one to its lower right, and the left one nearest the left wall. Pinned "
			"eshaGameData has no sxx.ssSw map, so the ROM, not a switch-to-coil wire, fires each bumper.",
			MANUAL_SOURCE, ROM_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.slingshots", "Slingshots", "other", [output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-55", "switch.matrix-56"],
			"Special solenoids 18 (left) and 20 (right), AE-26-1500, kick from the slingshots; each has a paired actuating switch (A-4834-H; "
			"B-8734-1) read as 55 and 56.",
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.shaker", "Quake shaker motor", "motorized", [output_id("Quake Shaker Motor")], [],
			"The Shaker Assembly (B-12388) under the playfield: an 11 RPM motor (14-7951) turning an eccentric weight (20-9588). The ROM runs "
			"it for earthquakes (its text includes a QUAKE INTENSITY adjustment); the retained script nudges the table while 22 is on.",
			MANUAL_SOURCE, ROM_SOURCE, VPX_SCRIPT_SOURCE, assembly="B-12388",
		),
		mechanism(
			"mechanism.captive-ball", "Captive ball", "other", [], ["switch.matrix-23"],
			"A captive ball in a lane at the right strikes the Captive Ball standup (23, zone 9); the five lamps 1-5 along the lane show its "
			"25K-250K value and lamp 6 the zone-9 arrow. It has no coil and no flasher of its own beyond 25.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, ROM_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Three flippers", "other", [], ["switch.matrix-57", "switch.matrix-58"],
			"Lower right and lower left flippers (C-11626-R-3 / C-11626-L-3, FL-11630 coils) and an upper left flipper (C-11626-L-6, FL-11722). "
			"Each cabinet button fires its coils directly; the left button fires both left flippers. Each assembly has an end-of-stroke switch "
			"(03-7811) that opens the power winding and is not in the switch matrix. The CPU sees only the lane-change optos 57/58 (and "
			"PinMAME's synthetic 45-48). In PinMAME a consumer presses the flippers through public 82 (right) and 84 (left); core_updateSw "
			"copies them to 57/58 every update and overwrites any direct write there.",
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ac-relay-switch-2", "kind": "direct", "source": output_id("A/C Select Relay"), "destination": "switch.matrix-2",
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
	]


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
			"id": MACHINE_ID, "name": "Earthshaker", "manufacturer": "Williams", "year": 1989, "kind": "physical_pinball",
			"ipdb_id": 753, "opdb_id": "GRw0r-Mp42p",
			"playfield": {"width": TABLE_WIDTH, "height": TABLE_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": STATUS,
			"missing": ["spatial_placement", "variant_differences"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "observed",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
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
		raise RuntimeError(f"Earthshaker device identifiers are not unique: {duplicates}")
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
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/earthshaker-1989/extracted-vpxtool.manifest.json",
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
		"observed_only": [
			{"group": "pinmame.input.switch", "addresses": [25, 26], "reason": "Prototype building-height optos anchored at the building primitives' shared origin; no source draws the positioner board."},
			{"group": "pinmame.output.lamp", "addresses": sorted(BUILDING_LAMPS), "reason": "Building windows placed at their window meshes' centres, one point per column; the lamp-board sockets behind them are not surveyed."},
		],
		"partly_placed": [
			{"group": "pinmame.output.solenoid", "address": address, "printed_quantity": 2, "placed": 1, "reason": reason}
			for address, reason in sorted(PARTLY_PLACED_FLASHERS.items())
		],
		"projections": [
			{"group": "pinmame.input.switch", "address": 25, "reason": SWITCH_PROJECTIONS[25]},
			{"group": "pinmame.input.switch", "address": 26, "reason": SWITCH_PROJECTIONS[26]},
			{"group": "pinmame.input.switch", "address": 37, "reason": SWITCH_PROJECTIONS[37]},
			{"group": "pinmame.input.switch", "address": 40, "reason": SWITCH_PROJECTIONS[40]},
			{"group": "pinmame.input.switch", "address": 42, "reason": SWITCH_PROJECTIONS[42]},
			{"group": "pinmame.input.switch", "address": 55, "reason": SWITCH_PROJECTIONS[55]},
			{"group": "pinmame.input.switch", "address": 56, "reason": SWITCH_PROJECTIONS[56]},
			{"group": "pinmame.output.solenoid", "address": 3, "reason": "Drop Target Reset placed on the middle target (sw28) of the bank it resets."},
			{"group": "pinmame.output.solenoid", "address": 4, "reason": "California Fault placed on the California map primitive the zone opener slides."},
			{"group": "pinmame.output.lamp", "address": 17, "reason": "Building windows 17-25 are placed at their window meshes' centres (one point per column, rows differ only in height); the derivation is in each lamp's note."},
		],
		"ordering_decisions": [
			"Jet-bumper switches follow the manual's drawing (54 top, 53 right, 52 left), the ROM's names, and the lamp and coil drawings, not the retained script, whose Bumper1/Bumper3 handlers swap 52 and 54.",
			"Coin chutes follow the switches list and the ROM (4 right, 6 left) over the matrix table's reversed pair.",
			"Right-ramp flashers follow the coil drawing (08C twice at the top, then 07C, then 06C down the right side), which agrees with the retained script's dome bindings.",
		],
		"visual_review_cache": {"root": "external:pinmame-manuals/by-machine/williams.earthshaker.1989/rendered/"},
		"excluded_object_classes": [
			"Flasherflash/Flasherlit render layers co-located with each Flasherbase dome",
			"l41a/l42a/l43a bumper glow layers co-located with l41/l42/l43",
			"FlBG*/FlBGL* VR backglass flashers and L58-L64 backglass jackpot lights",
			"Light.L49a/L57a glow lights (falloff 150, no bulb mesh), within 0.001 of the Primitive.L49/L57 bulb-cover meshes that carry the positions",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Earthshaker (Williams, 1989) spatial review",
		"",
		f"Status: {report['status']}.",
		"",
		f"Geometry comes from the retained known-working VPW-Lite v006 table (SHA-256 `{TABLE_SHA256}`), whose embedded script (SHA-256 "
		f"`{SCRIPT_SHA256}`) is the runtime authority. Exact bounds are `{TABLE_BOUNDS}`; every coordinate is x/964 and y/2162. The Williams "
		"operations manual is the physical authority; its location drawings were used to check sides and order, not to measure positions.",
		"",
		"## Evidence decisions",
		"",
	]
	lines += [f"- {decision}" for decision in report["ordering_decisions"]]
	lines += [
		"- Speaker-panel jackpot lamps 58-64, the insert-board G.I. (11), the knocker (7), and the quake shaker (22) take controlled `cabinet_or_service` records.",
		"- G.I. strings 10 and 15 are placed at the retained GIU and GI collections' bulbs; the manual prints no G.I. bulb count.",
		"",
		"## Blocking gaps",
		"",
	]
	lines += [f"- Solenoid {entry['address']}: {entry['printed_quantity']} bulbs printed, {entry['placed']} placed; {entry['reason']}." for entry in report["partly_placed"]]
	lines += [f"- {entry['group']} {', '.join(str(address) for address in entry['addresses'])}: observed only. {entry['reason']}" for entry in report["observed_only"]]
	lines += [
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
		f"- Runtime evidence `{LA3_RUNTIME_PATH}` and `{PA1_RUNTIME_PATH}`.",
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
		raise RuntimeError(f"Stale Earthshaker definition is still present: {stale}")
	expected = canonical_bytes(build())
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Earthshaker definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Earthshaker seed is not byte-identical to the canonical definition: {seed_path}")
	report = build_spatial_report(build())
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Earthshaker spatial report drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Earthshaker spatial review drifted from its deterministic curator: {markdown_path}")
	print("Earthshaker definition, seed, and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Earthshaker extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Earthshaker retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
