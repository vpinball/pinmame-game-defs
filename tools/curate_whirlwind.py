"""Curate the physical Williams Whirlwind (1990) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail,
and normalized coordinate as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.

Whirlwind is the first System 11 machine curated in this project. It reuses no WPC conventions:
switches and lamps share one sequential column-major 1-64 address space (address = (column-1)*8 +
row, not column-times-ten), there is no dedicated-switch namespace separate from matrix column 1,
and general illumination is simply two ordinary solenoid addresses (11, 16) rather than a distinct
GI channel. See ``controllers/pinmame/system-11.json`` for the full platform derivation.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines/partial/williams/whirlwind-1990.json"
SEED_PATH = ROOT / "tools/seeds/williams/whirlwind-1990.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/whirlwind-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/whirlwind-1990.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.whirlwind.1990"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.whirlwind.1990"
VPX_TABLE_SOURCE = "vpx-table.whirlwind-1990"
VPX_SCRIPT_SOURCE = "vpx-script.whirlwind-1990"
VPX_EXTRACTION_SOURCE = "vpx-extraction.whirlwind-1990"

TABLE_SHA256 = "105477078e68547c24167fc9ba99baeff24ec48ce16c46ec2530184a67f92e23"
SCRIPT_SHA256 = "e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2"
MANUAL_SHA256 = "365421ffdc059180ef5457fec2aa7567981954c383ab26d6b1e92223b790c649"
MANUAL_TRANSCRIPTION_SHA256 = "af6d1a70eea94ac46baa6858fa220766eaf0dddaf90684179fc5687e51c0fbe6"
VPX_GEOMETRY_SHA256 = "dfe62e82674ca6ce91cc20fad8f1a648add5e3d278e677dfb34128f312f8020b"

EXTRACTION_RELATIVE_PATH = Path("williams/whirlwind-1990/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/whirlwind-1990/extracted-vpxtool.manifest.json")

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

DRIVER_IDS = ("whirl_l3", "whirl_l2", "whirl_g1", "whirl_g2", "whirl_g3")
DRIVER_COMPATIBILITY = {
	"whirl_l3": ("identical", "Williams production LA-3 US/Canadian ROM shipped with the physical machine; the clone-tree parent."),
	"whirl_l2": ("identical", "Williams LU-2 firmware revision for the same physical machine; whirlGameData/init_whirl are shared with the parent, so the switch matrix, lamp matrix, solenoid table, and playfield hardware are unchanged."),
	"whirl_g1": ("identical", "Williams LG-1 German-localized firmware; shares whirlGameData/init_whirl with the parent (input_ports_whirl aliases the shared input_ports_s11 table), no controller-address or playfield difference."),
	"whirl_g2": ("identical", "Williams LG-2 German-localized firmware revision; same hardware as LG-1."),
	"whirl_g3": ("identical", "Williams LG-3 German-localized firmware revision; same hardware as LG-1/LG-2."),
}

EXTRACTION_FILE_COUNT = 1881

# --- Switch matrix (public address = (column-1)*8+row). Primary labels from the authoritative
# Switches parts list (printed page 74); matrix-table (printed page 75/76) wording is used where it
# is more specific or where the two pages disagree only in synonymous phrasing.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "C Side Power A/C Relay", 3: "Game Start (Credit) Button",
	4: "Right Coin Chute (USA)", 5: "Center Coin Chute", 6: "Left Coin Chute (USA)",
	7: "Slam Tilt", 8: "High Score Reset",
	10: "Outhole", 11: "Ball Trough #1 (Left)", 12: "Ball Trough #2 (Middle)", 13: "Ball Trough #3 (Right)",
	15: "Right Return Lane", 16: "Right Outlane", 17: "Left Outlane", 18: "Left Return Lane",
	19: "Right Cellar", 20: "Left Cellar",
	21: "Left Standup", 22: "Left Lock 1 (Lower)", 23: "Left Lock 2 (Middle)", 24: "Left Lock 3 (Upper)",
	25: "Right Standup", 26: "1-Bank Drop Target", 27: "3-Bank Drop Target (Lower)",
	28: "3-Bank Drop Target (Middle)", 29: "3-Bank Drop Target (Top)", 30: "Middle Standup",
	33: "Enter Left Ramp", 34: "Left Ramp Score (Top)", 35: "Left Ramp Score (Bottom)",
	36: "Left Loop (Top)", 37: "Left Loop (Bottom)", 38: "Right Loop (Top)", 39: "Right Loop (Bottom)",
	40: "Inner Loop", 41: "Spinner", 42: "Right Ramp Down", 43: "Top Right Eject",
	44: "Right Ramp Score (Top)", 45: "Right Ramp Score (Bottom)",
	47: "Left Standup (Right Ramp)", 48: "Right Standup (Right Ramp)",
	49: "Left Top Jet Bumper", 50: "Right Top Jet Bumper", 51: "Lower Top Jet Bumper",
	52: "Left Bottom Jet Bumper", 53: "Right Bottom Jet Bumper", 54: "Upper Bottom Jet Bumper",
	55: "Bottom-Left Kicker (Slingshot)", 56: "Bottom-Right Kicker (Slingshot)",
	57: "Right Flipper Lane Change", 58: "Left Flipper Lane Change",
	59: "Ball Shooter Lane", 60: "Left 110 Point", 61: "Right 110 Point",
}
# Printed matrix positions marked "Not Used" on both the parts list (page 74) and the matrix table
# (page 75).
UNUSED_MATRIX_ADDRESSES = {9, 14, 31, 32, 46, 62, 63, 64}
# Every switch confirmed opto construction by the switches parts list (page 74): drop-target optos
# (p/o C-13311, p/o C-13205-1, blank switch part number) and the flipper-lane-change opto pair
# (optotransistor on the Backbox Interconnect board, per its ** footnote).
OPTO_SWITCHES = {26, 27, 28, 29, 57, 58}
SWITCH_TYPES = {
	1: "tilt", 2: "other", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button",
	10: "microswitch", 11: "microswitch", 12: "microswitch", 13: "microswitch",
	15: "microswitch", 16: "microswitch", 17: "microswitch", 18: "microswitch",
	19: "microswitch", 20: "microswitch",
	21: "microswitch", 22: "microswitch", 23: "microswitch", 24: "microswitch",
	25: "microswitch", 26: "opto", 27: "opto", 28: "opto", 29: "opto", 30: "microswitch",
	33: "microswitch", 34: "microswitch", 35: "microswitch", 36: "microswitch", 37: "microswitch",
	38: "microswitch", 39: "microswitch", 40: "microswitch", 41: "microswitch", 42: "microswitch",
	43: "microswitch", 44: "microswitch", 45: "microswitch",
	47: "microswitch", 48: "microswitch",
	49: "leaf", 50: "leaf", 51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf",
	55: "leaf", 56: "leaf", 57: "opto", 58: "opto",
	59: "microswitch", 60: "microswitch", 61: "microswitch",
}
# address -> (assembly/opto part, switch part), transcribed verbatim from printed page 74.
SWITCH_PARTS = {
	1: (None, None), 2: (None, "5580-09555-01"), 3: (None, "SW-1A-126"),
	4: (None, "27-1092"), 5: (None, None), 6: (None, "27-1092"), 7: (None, "27-1066"), 8: (None, "27-1008"),
	10: (None, "5647-12133-12"), 11: (None, "5647-09957-00"), 12: (None, "5647-09957-00"), 13: (None, "5647-12073-08"),
	15: (None, "5647-12073-19"), 16: (None, "5647-12073-19"), 17: (None, "5647-12073-19"), 18: (None, "5647-12073-19"),
	19: (None, "5647-12073-25"), 20: (None, "5647-12073-25"),
	21: (None, "B-12583-6"), 22: (None, "5647-12073-32"), 23: (None, "5647-12073-33"), 24: (None, "5647-12073-34"),
	25: (None, "B-11696-15"), 26: ("p/o C-13311", None), 27: ("p/o C-13205-1", None), 28: ("p/o C-13205-1", None),
	29: ("p/o C-13205-1", None), 30: (None, "B-11696-5"),
	33: (None, "5647-12073-11"), 34: (None, "5647-12133-04"), 35: (None, "5647-12073-21"),
	36: (None, "5647-12073-19"), 37: (None, "5647-12073-19"), 38: (None, "5647-12073-19"), 39: (None, "5647-12073-19"),
	40: (None, "5647-12133-08"), 41: (None, "5647-12133-08"), 42: (None, "5647-12001-00"), 43: (None, "5647-12133-11"),
	44: (None, "5647-12073-21"), 45: (None, "5647-12073-21"),
	47: (None, "B-12583-6"), 48: (None, "B-12583-4"),
	49: (None, "B-12030-2"), 50: (None, "B-12030-2"), 51: (None, "B-12030-2"),
	52: (None, "B-12030-2"), 53: (None, "B-12030-2"), 54: (None, "B-12030-2"),
	55: (None, None), 56: (None, None), 57: (None, None), 58: (None, None),
	59: (None, "5647-12073-04"), 60: (None, "5647-12133-13"), 61: (None, "5647-12133-13"),
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
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Up/Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic", "service.cpu-diag"), -4: ("Sound Diagnostic", "service.sound-diag"),
}

# --- Solenoid table (public address). "A/C" pairs share one driver transistor multiplexed by
# solenoid 12; "C"-side addresses are (A-side address + 24) per updsol()'s mux copy.
SOLENOID_A_LABELS = {
	1: "Outhole Kicker", 2: "Shooter Lane Feeder", 3: "Right Ramp Lifter", 4: "Left Locking Kickback",
	5: "Top Eject", 6: "Knocker", 7: "3-Bank Drop Target Reset", 8: "1-Bank Drop Target Reset",
}
SOLENOID_C_LABELS = {
	25: "Bottom Right Flasher", 26: "Spinner Flasher", 27: "Right Ramp Top/Upper Jets Flashers",
	28: "Right Ramp Upper Middle/Million Flashers", 29: "Ramp Lower Middle/Lower Jets Flashers",
	30: "Right Ramp Bottom Flasher", 31: "3-Bank Target/Middle Target Flashers", 32: "Million+/Compass Flashers",
}
SOLENOID_A_DRIVER = {1: "Q33", 2: "Q25", 3: "Q32", 4: "Q24", 5: "Q31", 6: "Q23", 7: "Q30", 8: "Q22"}
SOLENOID_A_WIRE = {1: "Vio-Brn", 2: "Vio-Red", 3: "Vio-Orn", 4: "Vio-Yel", 5: "Vio-Grn", 6: "Vio-Blu", 7: "Vio-Blk", 8: "Vio-Gry"}
SOLENOID_A_CONTROL = {1: "1P11-1", 2: "1P11-3", 3: "1P11-4", 4: "1P11-5", 5: "1P11-6", 6: "1P11-7", 7: "1P11-8", 8: "1P11-9"}
SOLENOID_A_PLAYFIELD = {1: "5J1-9", 2: "5J1-7", 3: "5J1-6", 4: "5J1-5", 5: "5J1-4", 6: "5J1-3", 7: "5J1-2", 8: "5J1-1"}
SOLENOID_C_PLAYFIELD = {25: "5J5-9", 26: "5J5-8", 27: "5J5-7", 28: "5J5-5", 29: "5J5-4", 30: "5J5-3", 31: "5J5-2", 32: "5J5-1"}
SOLENOID_A_PART = {
	1: "AE-23-800", 2: "AE-23-800", 3: "AE-24-900", 4: "AE-23-800", 5: "AE-23-800",
	6: "AE-23-800", 7: "AE-26-1200", 8: "AE-23-800",
}
SOLENOID_C_FLASHLAMPS = {
	25: ("#906 flashlamp", 1), 26: ("#906 flashlamp", 1), 27: ("#906 flashlamps", 2), 28: ("#906 flashlamps", 2),
	29: ("#906 flashlamps", 2), 30: ("#906 flashlamp", 1), 31: ("#906 flashlamps", 2), 32: ("#906 flashlamps", 2),
}

SOLENOID_STANDARD_LABELS = {
	9: "Left Lower Jet Bumper", 10: "Top Lower Jet Bumper", 11: "Upper Playfield GI Relay",
	12: "A/C Select Relay", 13: "Diverter", 14: "Cellar Kickback", 15: "Right Lower Jet Bumper",
	16: "Lower Playfield / Backbox GI Relay",
}
SOLENOID_STANDARD_DRIVER = {9: "Q17", 10: "Q9", 11: "Q16", 12: "Q8", 13: "Q15", 14: "Q7", 15: "Q14", 16: "Q6"}
SOLENOID_STANDARD_WIRE = {9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio", 16: "Brn-Gry"}
SOLENOID_STANDARD_CONTROL = {9: "1P12-1", 10: "1P12-2", 11: "1P12-4", 12: "1P12-5", 13: "1P12-6", 14: "1P12-7", 15: "1P12-8", 16: "1P12-9"}
SOLENOID_STANDARD_PLAYFIELD = {
	9: "5J2-9: 5J6-9: 2J4-3", 10: "5J2-8: 5J6-8: 2J4-5", 11: "5J2-6: 5J6-7: 2J4-6", 12: "5J2-5",
	13: "5J2-4: 5J6-5", 14: "5J2-3: 5J6-3", 15: "5J2-2: 5J6-2", 16: "5J2-1: 5J6-1",
}
SOLENOID_STANDARD_PART = {9: "AE-23-800", 10: "AE-23-800", 13: "AE-26-1200", 14: "AE-26-1500", 15: "AE-23-800"}

SOLENOID_SPECIAL_LABELS = {
	17: "Left Upper Jet Bumper", 18: "Left Kicker (Slingshot)", 19: "Right Upper Jet Bumper",
	20: "Right Kicker (Slingshot)", 21: "Top Upper Jet Bumper", 22: "Right Ramp Down",
}
SOLENOID_SPECIAL_NUM = {17: 1, 18: 2, 19: 3, 20: 4, 21: 5, 22: 6}
SOLENOID_SPECIAL_DRIVER = {17: "Q75", 18: "Q71", 19: "Q73", 20: "Q69", 21: "Q77", 22: "Q79"}
SOLENOID_SPECIAL_WIRE = {17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk"}
SOLENOID_SPECIAL_CONTROL = {17: "1P19-7", 18: "1P19-4", 19: "1P19-3", 20: "1P19-6", 21: "1P19-8", 22: "1P19-9"}
SOLENOID_SPECIAL_PLAYFIELD = {17: "5J3-7: 5J7-7", 18: "5J3-6: 5J7-6", 19: "5J3-3: 5J7-3", 20: "5J3-4: 5J7-5", 21: "5J3-2: 5J7-2", 22: "5J3-1: 5J7-1"}
SOLENOID_SPECIAL_PART = {17: "AE-23-800", 18: "AE-26-1500", 19: "AE-23-800", 20: "AE-26-1500", 21: "AE-23-800", 22: "SM-26-600-DC"}

# Sound Overlay Board (public address = manual item number + 14; see manual-transcription.md).
SOLENOID_OVERLAY_LABELS = {
	37: "BP Lightning (Left) Flashers", 38: "Blower Motor (Fan)", 39: "BP Thunder (Middle) Flasher",
	40: "BP Thunder (Right) Flashers", 41: "Spin Wheels Motor",
}
SOLENOID_OVERLAY_MANUAL_ITEM = {37: 23, 38: 24, 39: 25, 40: 26, 41: 27}
SOLENOID_OVERLAY_DRIVER = {37: "Q1", 38: "Q4", 39: "Q7", 40: "Q10", 41: "Q13"}
SOLENOID_OVERLAY_WIRE = {37: "Gry-Brn", 38: "Gry-Red", 39: "Gry-Org", 40: "Gry-Org", 41: "Gry-Org"}
SOLENOID_OVERLAY_SOL_J4 = {37: "SOL J4-6", 38: "SOL J4-5", 39: "SOL J4-4", 40: "SOL J4-2", 41: "SOL J4-1"}
SOLENOID_OVERLAY_PART = {37: "#906 flashlamps, 3bp", 38: "14-7956 via Triac Bd", 39: "#906 flashlamps, 1bp", 40: "#906 flashlamps, 2bp", 41: "14-7955"}

# Retained VPW-derived VPX script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn", 2: "bsTrough.SolOut (BallRelease kicker)", 3: "SolRightRampEntryLifter",
	4: "SolLeftLockingKickback", 5: "bsSaucer.SolOut", 6: 'vpmSolSound (Knocker)',
	7: "dtL.SolDropUp", 8: "dtT.SolDropUp", 11: "SolUpperGI", 13: "SolRampDiverter", 14: "trCellar.SolOut",
	16: "SolLowerGI", 22: "SolRightRampEntryDown",
	25: "Sol25", 26: "Sol26", 27: "Sol27", 28: "Sol28", 29: "Sol29", 30: "Sol30", 31: "Sol31", 32: "Sol32",
	37: "Sol37", 38: "SolBackwallFan", 39: "Sol39", 40: "Sol40", 41: "SolSpinWheelsMotor",
}

VIRTUAL_SOLENOID_NOTES = {
	23: "PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL: an emulator/ROM-internal 'flipper and switched-solenoid enable' pulse with no physical driver-board output of its own. Not a manual device; the manual's own item 23 (BP Lightning (L) Flashers) is a different, unrelated device at public address 37 (see the Sound Overlay Board offset note on address 37).",
	24: "Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay-multiplexed 'C'-side alias bank (25-32). No known driver populates this address.",
	33: "Platform generic upper-flipper-coil address (CORE_FIRSTUFLIPSOL). Whirlwind's hw.flippers declares no FLIP_U* bit, and core_getSol only serves 33-36 for GEN_ALLWPC/GEN_SAM, so this reads as always-zero; Whirlwind has no upper-flipper coil.",
	34: "Platform generic upper-flipper-coil address; unused, see address 33.",
	35: "Platform generic upper-flipper-coil address; unused, see address 33.",
	36: "Platform generic upper-flipper-coil address; unused, see address 33.",
	42: "Outer bound of the platform's 'Sound overlay board' address range (core_getSol's GEN_ALLS11 branch serves 37-44); Whirlwind's own Sound Overlay Board populates only 37-41 (5 devices, matching the 5 manual items 23-27), confirmed by the retained script's own SolCallback registrations stopping at 41. No device is wired at 42.",
	43: "Outer bound of the platform's Sound Overlay Board address range; unused, see address 42.",
	44: "Outer bound of the platform's Sound Overlay Board address range; unused, see address 42.",
	45: "PinMAME's synthetic lower-right-flipper power output (CORE_FIRSTLFLIPSOL). Whirlwind's hw.flippers is FLIP_SWNO(58,57) with no FLIP_SOL bit, so core_updateSw fabricates this address purely from live switch-57 state for ball-physics purposes; on real hardware the lower-right flipper button fires its coil directly through a relay/fuse circuit with no CPU involvement, confirmed by the Solenoid Table's own flipper rows carrying no Sol. No. and by note 2 ('Flipper connections shown in braces are from flipper switch to flipper coil').",
	46: "PinMAME's synthetic lower-right-flipper hold output; see address 45.",
	47: "PinMAME's synthetic lower-left-flipper power output; see address 45 (switch 58).",
	48: "PinMAME's synthetic lower-left-flipper hold output; see address 45 (switch 58). Whirlwind's upper-right flipper shares the lower-right coil/button in the retained script (RightFlipper and RightFlipper1 both rotate from SolRFlipper) and has no separate synthetic address of its own.",
	49: "Platform-wide simulator-only fake solenoid for the ball shooter (CORE_FIRSTSIMSOL); not System-11-specific and not a Whirlwind hardware output.",
	50: "Unassigned platform gap between the simulator slot (49) and the custom-solenoid base (51). whirlGameData declares no custSol, so PinMAME models exactly 50 solenoid address slots for this game (CORE_FIRSTCUSTSOL-1+0); addresses 51 and above are not modeled at all.",
}

# --- Lamp matrix (public address = (column-1)*8+row). Primary labels from the authoritative
# Lamp-Matrix Table (printed page 76); backglass score-reel lamps (2-8) are not part of the
# playfield matrix devices below (see BACKGLASS_REEL_LAMPS).
LAMP_LABELS = {
	1: "Middle Standup", 9: "Left Outlane", 17: "S Compass Arrow", 25: "Toll 1", 33: "Bottom Jets Left",
	41: "Right Ramp Lock", 49: "Left Return Lane", 57: "Shoot Again",
	10: "Right Outlane", 18: "SW Compass Arrow", 26: "Toll 2", 34: "Bottom Jets Top",
	42: "Right Ramp Double", 50: "Left Loop", 58: "2X",
	11: "Top Drop 50K", 19: "W Compass Arrow", 27: "Toll 3", 35: "Bottom Jets Right",
	43: "Left Ramp Million Plus", 51: "Left Standup", 59: "3X",
	12: "Top Drop 75K", 20: "NW Compass Arrow", 28: "Toll 4", 36: "Top Jets Left",
	44: "Left Ramp Million", 52: "Inner Loop Arrow", 60: "4X",
	13: "Top Drop 100K", 21: "N Compass Arrow", 29: "Toll 5", 37: "Top Jets Right",
	45: "Left Ramp Release", 53: "Right Ramp Left Standup", 61: "5X",
	14: "Top Drop 150K", 22: "NE Compass Arrow", 30: "Toll 30", 38: "Top Jets Bottom",
	46: "Skill Shot Right", 54: "Right Ramp Right Standup", 62: "6X Lites Extra Ball",
	15: "Top Drop Quick", 23: "E Compass Arrow", 31: "Toll 20", 39: "Left Cellar Arrow",
	47: "Skill Shot Middle", 55: "Right Loop", 63: "6X Lites Special",
	16: "Top Drop Extra Ball", 24: "SE Compass Arrow", 32: "Toll 10", 40: "Right Cellar Arrow",
	48: "Skill Shot Left", 56: "Right Standup", 64: "Spinner",
}
# Backglass "score reel" lamps 2-8: driven by FadeRm/Flash in UpdateLamps against Reel objects
# (L2-L8), not Light objects; backbox/cabinet devices with no playfield coordinate.
BACKGLASS_REEL_LAMPS = {
	2: "Upper Jets On", 3: "250K", 4: "Extra Ball On", 5: "3-Bank 100K", 6: "500K",
	7: "Lite Million", 8: "Lower Jets On",
}
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"),
	4: ("YEL-BLK", "1J7-4", "Q60"), 5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"),
	7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1"), 2: ("RED-BLK", "1J6-2"), 3: ("RED-ORN", "1J6-3"), 4: ("RED-YEL", "1J6-5"),
	5: ("RED-GRN", "1J6-6"), 6: ("RED-BLU", "1J6-7"), 7: ("RED-VIO", "1J6-8"), 8: ("RED-GRY", "1J6-9"),
}
# Lamp-locations page (printed 77) prints "Sign" for 39/40 against the matrix table's (printed 76)
# "Arrow"; page 76 (the wiring table of record) is used as the working label.
LAMP_LOCATIONS_PAGE_WORDING = {39: "Left Cellar Sign", 40: "Right Cellar Sign"}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Whirlwind retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Whirlwind extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Whirlwind retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Whirlwind retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	if len(files) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Whirlwind retained extraction file count mismatch: files={len(files)}, expected={EXTRACTION_FILE_COUNT}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield",
			"x": round(x, 6), "y": round(y, 6), "provenance": provenance(*source_refs),
		})
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned catalog driver records for the whirl_* clone tree",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c whirlGameData INITGAME(whirl,GEN_S11B,s11_dispS11b2,12,FLIP_SWNO(58,57),"
				"S11_LOWALPHA|S11_DISPINV,S11_MUXSW2|S11_SNDOVERLAY), CORE_GAMEDEF/CORE_CLONEDEF for whirl_l3/l2/g1/g2/g3, "
				"input_ports_whirl=input_ports_s11; src/wpc/s11.c SWITCH_UPDATE(s11) dedicated-switch/mux-feedback logic, "
				"setSSSol special-solenoid PIA-to-address map, updsol A/C-relay mux copy, pia0b_w/pia1a_w/pia1b_w/"
				"pia2a_r/pia4a_r/pia4b_w/pia5cb2_w, s11_readmem/s11_writemem, MACHINE_INIT(s11) whirl_ GI/bulb-type block "
				"(addresses 11, 16, 25, 40, 42); src/wpc/s11.h S11_SWADVANCE/S11_SWUPDN/S11_SWCPUDIAG/S11_SWSOUNDDIAG, "
				"S11_COMINPORT/S11_COMPORTS, S11_MUXSW2/S11_SNDOVERLAY, COREPORT_DIPNAME Country jumper; src/wpc/core.h "
				"core_tGameData sxx.muxSol/sxx.ssSw, CORE_FIRSTSSSOL=17, CORE_SSFLIPENSOL=23, CORE_FIRSTEXTSOL=37, "
				"CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, CORE_FIRSTSIMSOL=49, CORE_FIRSTCUSTSOL=51, CORE_MAXSOL=64; "
				"src/wpc/core.c core_swSeq2m/core_m2swSeq/core_getSw/core_setSw, core_getSol GEN_ALLS11 branch, "
				"core_updateSw synthetic-flipper-solenoid fallback; src/wpc/gen.h GEN_S11B==GEN_S11X==GEN_S11A; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_S11B=0x100"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json",
			"revision": "repository",
			"locator": "System 11 public switch/lamp sequential-matrix numbering, dedicated diagnostic addresses, and the solenoid A/C-mux/special/sound-overlay/GI address rules",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.whirlwind.1990/archive-arcademanual_Whirlwind_OPS/Whirlwind_OPS.pdf",
			"original_filename": "Whirlwind_OPS.pdf", "sha256": MANUAL_SHA256,
			"locator": (
				"110-page scan with an OCR text layer of the Williams Whirlwind operations manual (Internet Archive item "
				"arcademanual_Whirlwind_OPS). PDF page = printed page + 10 throughout Sections 1-3. Printed page 74 carries "
				"the switch-locations parts list; 75 the switch-matrix wiring table; 76 the lamp-matrix wiring table; 77 the "
				"lamp-locations parts list; 66 the Wheels Drive Assembly parts list; 53 the GI relay board parts lists; 33 and "
				"95 the special/controlled solenoid circuit theory and schematic; 73/32 (plus the unpaginated front insert) the "
				"solenoid table and locations; 78 the playfield parts list (flipper assemblies)."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; scanned by Heinz-Peter Bader, hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.whirlwind.switch-locations", "locator": "PDF page 84, printed page 74, Switches parts list",
					"path": "evidence/excerpts/williams.whirlwind.1990/switch-locations.md",
					"sha256": "4d4c0ece88d0c8ee8376d08cd677407d54cb6ccfd50d6dd9ea399b4067aee7f8",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.switch-matrix", "locator": "PDF page 85, printed page 75, Switch-Matrix Table",
					"path": "evidence/excerpts/williams.whirlwind.1990/switch-matrix.md",
					"sha256": "51f68602137365ca91a08ab7993248f9e6e95697a99c767a6b51497dc87b12da",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.lamp-matrix", "locator": "PDF page 86, printed page 76, Lamp-Matrix Table",
					"path": "evidence/excerpts/williams.whirlwind.1990/lamp-matrix.md",
					"sha256": "47cfc2d08dd2a9f1c3260e4ff8a7c3d4f091c5ae88f67aba297f75246bbf3027",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.lamp-locations", "locator": "PDF page 87, printed page 77, Lamps locations",
					"path": "evidence/excerpts/williams.whirlwind.1990/lamp-locations.md",
					"sha256": "5fffaa4a4ade7fc732d3df3693243c7468050337bcd4f5a803568464cf9e8d04",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.solenoid-flasher-locations",
					"locator": "PDF pages 8/43/93, printed pages 32/33/73, Solenoid Table",
					"path": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-locations.md",
					"sha256": "3dac1cf98c591f0995b444800c43cfe4a12eeccf15952cb1f291b98db19e35cd",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.solenoid-flasher-wiring",
					"locator": "PDF pages 43 and 105, printed pages 33 and 95, special/controlled solenoid theory and schematic",
					"path": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-wiring.md",
					"sha256": "5b718c57b2ba59ad8f404749ec8f52b505bd63389642d02880a857404dabaf22",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.general-illumination", "locator": "PDF page 63, printed page 53, GI relay boards",
					"path": "evidence/excerpts/williams.whirlwind.1990/general-illumination.md",
					"sha256": "0e96cc2b83f8fb4bb41f5f7653a7d327885519bddf067401c3b6fc72f0454914",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.boards-and-assemblies",
					"locator": "PDF pages 76 and 88, printed pages 66 and 78, Wheels Drive Assembly and flipper assembly parts",
					"path": "evidence/excerpts/williams.whirlwind.1990/boards-and-assemblies.md",
					"sha256": "73e4a9a82a38b615e47a0504f6f75412b94d84e12bbdcc6d287bb3fd7428c572",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind/manual-transcription.md", "revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": "Retained human transcription of every rendered manual table used by this definition, cross-referencing the excerpts above.",
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/source/Whirlwind%20%28Williams%201990%29.vpx",
			"original_filename": "Whirlwind (Williams 1990).vpx", "sha256": TABLE_SHA256,
			"locator": f"Retained known-working VPX recreation of the physical machine. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for named table objects.",
			"license": "NOASSERTION", "attribution": "unattributed VPX table author", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				'Retained embedded script (89,549 bytes). Runtime and mechanism-causality authority: cGameName = "whirl_l3", '
				"UseLamps=0 with an explicit UpdateLamps routine (so lamp bindings come from that routine, not name-pattern "
				"matching), UseGI=0 with explicit SolUpperGI/SolLowerGI routines, the SolCallback table for solenoids 1-8, 11, "
				"13, 14, 16, 22, 25-32, 37-41, and sLRFlipper/sLLFlipper, the Controller.Switch/vpmTimer.PulseSw switch "
				"semantics for the trough/cellar/lock/target/gate/bumper/slingshot state machines, SolSpinWheelsMotor driving "
				"the three-disc turntable mechanism, and SolBackwallFan driving the cabinet fan sound/glow cue. Full "
				"cross-reference in external:pinmame-review-artifacts/whirlwind/vpx-geometry.txt."
			),
			"license": "NOASSERTION", "attribution": "unattributed VPX table author", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/extracted-vpxtool/",
			"locator": f"Retained vpxtool extraction, {EXTRACTION_FILE_COUNT} files, produced from the retained table. Bounds are {TABLE_BOUNDS}.",
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	]


# --- Normalized playfield coordinates derived from the retained VPX extraction (x/964, y/2162);
# see review-artifacts/whirlwind/vpx-geometry.txt for the full gameitems cross-reference.
SWITCH_POSITIONS = {
	10: [(0.534836, 0.957920)], 11: [(0.869973, 0.874758)], 12: [(0.869973, 0.874758)], 13: [(0.869973, 0.874758)],
	15: [(0.805644, 0.739048)], 16: [(0.875218, 0.766501)], 17: [(0.138108, 0.772051)], 18: [(0.206928, 0.741718)],
	19: [(0.354692, 0.449995)], 20: [(0.151451, 0.495450)],
	21: [(0.411431, 0.455707)], 22: [(0.058280, 0.828065)], 23: [(0.058763, 0.798926)], 24: [(0.058427, 0.770579)],
	25: [(0.865944, 0.518753)], 26: [(0.672731, 0.137875)], 27: [(0.455815, 0.377291)], 28: [(0.445716, 0.403585)],
	29: [(0.435380, 0.430022)], 30: [(0.535038, 0.227511)],
	33: [(0.211420, 0.233719)], 34: [(0.871517, 0.069775)], 35: [(0.916804, 0.452409)], 36: [(0.057490, 0.119546)],
	37: [(0.060369, 0.170905)], 38: [(0.866656, 0.074157)], 39: [(0.920560, 0.114878)], 40: [(0.276464, 0.165024)],
	41: [(0.902531, 0.283572)], 42: [(0.751948, 0.308094)],
	43: [(0.808501, 0.157239)], 44: [(0.464495, 0.137223)], 45: [(0.145112, 0.344083)],
	47: [(0.687199, 0.292210)], 48: [(0.814741, 0.328618)],
	49: [(0.370103, 0.120103)], 50: [(0.574201, 0.102232)], 51: [(0.535288, 0.190128)],
	52: [(0.081349, 0.381487)], 53: [(0.302674, 0.400981)], 54: [(0.230891, 0.314034)],
	55: [(0.286784, 0.740424)], 56: [(0.723445, 0.738622)],
	59: [(0.938722, 0.889459)], 60: [(0.162086, 0.580157)], 61: [(0.849482, 0.602081)],
}
# Switches 10-13 (Outhole, Ball Trough #1-#3) have no dedicated VPX trigger objects; the retained
# script's cvpmBallStack helper (bsTrough.InitSw 10,11,12,13) manages them abstractly against the
# BallRelease exit kicker. Projected onto the two real anchor objects that bound the mechanism.
SWITCH_PROJECTIONS = {
	10: "Projected onto the Drain kicker (Kicker.Drain, table object center): switch 10 (Outhole) has no dedicated VPX trigger object -- the retained script's cvpmBallStack helper (bsTrough.InitSw 10,11,12,13) manages it abstractly, and Drain is the physical object nearest the outhole funnel (Drain_Hit feeds the trough via bsTrough.addball).",
	11: "Projected onto the BallRelease kicker (Kicker.BallRelease, table object center): switches 11-13 (Ball Trough #1-#3) have no individual VPX trigger objects -- the retained script's cvpmBallStack helper manages all three abstractly against the single BallRelease exit kicker (bsTrough.InitKick BallRelease,75,4), the trough mechanism's own retained object.",
	12: "Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.",
	13: "Projected onto the BallRelease kicker (Kicker.BallRelease, table object center); see switch 11.",
	42: "Projected onto the Right Ramp's own retained geometry (the RightRampUp/RightRampDown shared entry endpoint, table object center): switch 42 (Right Ramp Down) has a real printed switch part (5647-12001-00) but no dedicated VPX trigger object -- the retained script instead sets Controller.Switch(42) directly from the same SolRightRampEntryLifter/SolRightRampEntryDown handlers that swap the ramp's up/down geometry, because the physical switch is mechanically slaved to the same ramp position those solenoids control.",
}

def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append(
			_device(
				f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				roles=[role],
				physical={"location": "coin door / cabinet diagnostic switch cluster", "switch_type": "button", "notes": "System 11 diagnostic input, upper nibble of the shared S11_COMINPORT keyboard port (core_swSeq2m maps public n to matrix column 0)."},
				spatial=not_applicable("cabinet_or_service", CORE_SOURCE),
			)
		)

	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		label = SWITCH_LABELS.get(address)
		unused = address in UNUSED_MATRIX_ADDRESSES
		identifier = f"switch.matrix-{address}"
		assembly, part_number = SWITCH_PARTS.get(address, (None, None))
		physical: dict[str, Any] = {}
		if assembly:
			physical["assembly_part_number"] = assembly
		if part_number:
			physical["part_number"] = part_number
		if address in SWITCH_TYPES:
			physical["switch_type"] = SWITCH_TYPES[address]
		notes = f"Printed switch-matrix drive column {column}, return row {row}."
		if unused:
			notes += " The printed switch-locations parts list and the switch-matrix table both mark this position Not Used."
			label = f"Not Used (Matrix Position {address})"
		if address in OPTO_SWITCHES:
			if address in {26, 27, 28, 29}:
				notes += (
					" Printed on the switch-locations parts list with a blank Switch Part Number and an opto/photo-board "
					"part number instead ('p/o C-13311' for the 1-Bank Opto Board, 'p/o C-13205-1' for the 3-Bank Opto "
					"Board), confirming opto interrupter construction. Pinned PinMAME's whirlGameData declares no "
					"inverted-switch mask at all (wpc.invSw is entirely unset for this driver), so the public state is "
					"not emulator-normalized and the rest-state polarity (normally open vs normally closed) is not "
					"stated by this manual; see coverage.missing polarity."
				)
			else:
				notes += (
					" The switch-locations parts list marks this position with an unnumbered Sol./Switch entry and the "
					"** footnote 'Optotransistor on Backbox Interconnect Bd'; the physical cabinet flipper button "
					"(SW-10A-48 left / SW-1010A-13 right) is a separate, unnumbered, direct-wired circuit with no "
					"matrix address at all (it fires the flipper coil straight through a relay/fuse circuit with no "
					"CPU path), matching pinned PinMAME's FLIP_SWNO(58,57) declaration exactly (58=left, 57=right). "
					"Whirlwind's own inverted-switch mask is entirely unset, so rest-state polarity is unconfirmed "
					"here too; see coverage.missing polarity."
				)
		if address == 2:
			notes += (
				" Pinned PinMAME sets hw.gameSpecific1's S11_MUXSW2 flag for whirl_l3, which makes SWITCH_UPDATE(s11) "
				"unconditionally overwrite public switch 2 with the live state of the A/C Select Relay (solenoid 12) "
				"rather than any nominal 'ball tilt' meaning the shared S11_COMPORTS keyboard convention might "
				"otherwise suggest; the manual's own label ('C Power-A/C Relay') independently confirms this identity."
			)
		if address in {15, 16, 17, 18}:
			manual_wording = {15: None, 16: "Right Drain Lane", 17: "Left Drain Lane", 18: None}[address]
			if manual_wording:
				notes += f" The switch-locations parts list (page 74) prints this position \"{manual_wording}\"; \"Outlane\" (matrix table wording, printed page 75) is used as the working label -- the two terms describe the same physical feature."
		if address in SWITCH_PROJECTIONS:
			notes += " " + SWITCH_PROJECTIONS[address]
		physical["notes"] = notes

		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
			"physical": physical,
			"wiring": _switch_wiring(column, row),
		}
		if unused:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif address in {1, 3, 4, 5, 6, 7, 8}:
			availability = "optional" if address == 5 else "used"
			extra["roles"] = ["cabinet.tilt" if address in {1, 7} else "cabinet.coin" if address in {4, 5, 6} else "cabinet.service"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 2:
			availability = "used"
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in {57, 58}:
			availability = "used"
			extra["roles"] = ["cabinet.flipper-lane-change"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in SWITCH_PROJECTIONS:
			availability = "used"
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
		else:
			availability = "used"
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61}:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	dip_labels = {0: "Country Jumper (USA/Germany)"}
	for address, label in dip_labels.items():
		items.append(
			_device(
				f"switch.dip-{address}", label, "dip_switch", "pinmame.input.dip", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={"location": "System 11B CPU board", "switch_type": "dip", "notes": "Single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7. This retained manual's German/European preset-adjustments tables (printed pages 23, 13) confirm the jumper selects between US/Canadian and German/European default pricing and rules, not a per-switch DIP bank."},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


SOLENOID_POSITIONS = {
	1: [(0.534836, 0.957920)], 2: [(0.869973, 0.874758)], 3: [(0.751948, 0.308094)],
	4: [(0.059086, 0.826030)], 5: [(0.808501, 0.157239)],
	7: [(0.445716, 0.403585)], 8: [(0.672731, 0.137875)],
	9: [(0.081349, 0.381487)], 10: [(0.230891, 0.314034)],
	13: [(0.106958, 0.642185)], 14: [(0.151451, 0.495450)], 15: [(0.302674, 0.400981)],
	16: [(0.267403, 0.750777)],
	17: [(0.370103, 0.120103)], 18: [(0.286784, 0.740424)], 19: [(0.574201, 0.102232)],
	20: [(0.723445, 0.738622)], 21: [(0.535288, 0.190128)], 22: [(0.751948, 0.308094)],
}
# Confirmed backglass-only per the retained script (FlSol25-32/37/39/40, BGArr repositioning
# array, negative raw pos_y outside the 0-2162 playfield bounds); no playfield coordinate can be
# derived from this evidence even though the manual names these as ramp/target-mounted flashers.
SOLENOID_BACKGLASS_ONLY = {25, 26, 27, 28, 29, 30, 31, 32, 37, 39, 40}


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11B CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection,
		"return_component": f"column driver {drive_component}",
	}


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	def emit(identifier: str, label: str, kind: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> None:
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))

	# 1-8: switched "A"-side solenoids.
	for address, label in SOLENOID_A_LABELS.items():
		identifier = output_id(label)
		notes = f"Printed Solenoid Table entry {address:02d}A (Switched). Circuit A is pulsed while solenoid 12 (A/C Select Relay) is de-energized."
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}A"}],
			"physical": {"part_number": SOLENOID_A_PART[address], "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "driver_transistor": SOLENOID_A_DRIVER[address],
				"drive_wire": SOLENOID_A_WIRE[address], "control_connection": SOLENOID_A_CONTROL[address],
				"power_connection": SOLENOID_A_PLAYFIELD[address],
			},
		}
		if address == 6:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			if address == 7:
				extra["physical"]["notes"] += " Projected onto the middle target of the 3-bank drop target it resets (HitTarget.sw28, table object center); the reset mechanism has no separate actuator object in the retained table."
			if address == 8:
				extra["physical"]["notes"] += " Projected onto the single drop target it resets (HitTarget.sw26, table object center)."
		emit(identifier, label, "coil", address, "used", refs, **extra)

	# 9-16: controlled solenoids (jet bumpers, GI relays, diverter, cellar kickback, A/C relay).
	for address, label in SOLENOID_STANDARD_LABELS.items():
		identifier = output_id(label)
		notes = f"Printed Solenoid Table entry {address:02d} (Controlled)."
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		wiring: dict[str, Any] = {
			"board": "System 11B CPU board", "driver_transistor": SOLENOID_STANDARD_DRIVER[address],
			"drive_wire": SOLENOID_STANDARD_WIRE[address], "control_connection": SOLENOID_STANDARD_CONTROL[address],
			"power_connection": SOLENOID_STANDARD_PLAYFIELD[address],
		}
		physical: dict[str, Any] = {"notes": notes}
		if address in SOLENOID_STANDARD_PART:
			physical["part_number"] = SOLENOID_STANDARD_PART[address]
		extra = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"physical": physical, "wiring": wiring,
		}
		if address == 11:
			physical["notes"] += (
				" Pinned PinMAME's whirl_ MACHINE_INIT block names this address 'Upper Playfield GI output' "
				"(CORE_MODOUT_BULB_44_6_3V_AC_REV), confirmed by the manual's own GI relay board page (printed 53) and "
				"the retained script's SolUpperGI handler. The retained script's UpperGI light collection is empty "
				"(zero bound playfield objects) -- a completeness gap in this retained table, not evidence the "
				"physical machine lacks an upper-playfield GI bank. No coordinate is invented; see coverage.missing "
				"spatial_placement."
			)
			extra["roles"] = ["gi.upper-playfield"]
			kind = "gi"
			# spatial intentionally omitted (schema allows an output with no spatial key)
		elif address == 12:
			physical["notes"] += " A/C Select Relay (mounted on the Aux Power Driver Board, D-12247, in the backbox); multiplexes 16 controlled/switched solenoids between circuit A and circuit C. See controllers/pinmame/system-11.json for the full mux mechanism."
			extra["roles"] = ["internal.ac-select-relay"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
			kind = "relay"
		elif address == 16:
			physical["notes"] += (
				" Pinned PinMAME's whirl_ MACHINE_INIT block names this address 'Backbox and Lower playfield GI "
				"output'. The manual's own GI relay board page (printed 53) confirms this single address energizes "
				"TWO physically separate relays simultaneously: the playfield-side C-11902-1 board (lower playfield "
				"GI) and the separate backbox C-11998-1 board (backbox/backglass GI). The retained script's "
				"SolLowerGI handler drives both the LowerGI light collection (one member, Light1) and the near-"
				"full-table Flasher4 overlay together."
			)
			extra["roles"] = ["gi.lower-playfield-and-backbox"]
			extra["spatial"] = located(identifier, "emitter", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			kind = "gi"
		else:
			kind = "coil"
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		emit(identifier, label, kind, address, "used", refs, **extra)

	# 17-22: special solenoids (jet bumpers, slingshot kickers, right ramp down).
	for address, label in SOLENOID_SPECIAL_LABELS.items():
		identifier = output_id(label)
		printed_num = SOLENOID_SPECIAL_NUM[address]
		notes = f"Printed Solenoid Table entry Special #{printed_num} (public address {address}, resolved via setSSSol's ssSolNo[0]={{5,4,1,2,0,3}} PIA-to-address table)."
		if address == 21:
			notes += (
				" The Solenoid Table prints this row's Function column as \"Top Lower Jet Bumper\" -- identical text, "
				"verbatim, to solenoid 10's row. This is very likely a proofing duplication rather than the intended "
				"label: solenoids 17/19/21 share the Special #1/#3/#5 wiring bank (Left/Right Upper Jet Bumper plus "
				"a third position), the same structure as solenoids 9/15/10 (Left/Right Lower Jet Bumper plus a "
				"third position). Switch labels for the two matching jet-bumper clusters use the same Left/Right/"
				"third-position pattern ('Top Jets left/right/bot' for switches 49-51, matching Bumper1/2/3; 'Btm "
				"Jets left/right/top' for 52-54, matching Bumper4/5/6). By that structure, solenoid 10 (\"Top Lower "
				"Jet Bumper\") is the 'top' position of the LOWER cluster (matching switch 54 / Bumper6), and "
				"solenoid 21 is resolved as the 'bottom' position of the UPPER cluster (matching switch 51 / "
				"Bumper3), i.e. the same physical bumper as switch 51. Labeled 'Top Upper Jet Bumper' here for "
				"clarity; the manual's own printed text is preserved verbatim in "
				"evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-locations.md."
			)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		extra = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"Special #{printed_num}"}],
			"physical": {"part_number": SOLENOID_SPECIAL_PART[address], "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "driver_transistor": SOLENOID_SPECIAL_DRIVER[address],
				"drive_wire": SOLENOID_SPECIAL_WIRE[address], "control_connection": SOLENOID_SPECIAL_CONTROL[address],
				"power_connection": SOLENOID_SPECIAL_PLAYFIELD[address],
			},
		}
		if address == 22:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			extra["physical"]["notes"] += f" Retained script callback: {SOLENOID_CALLBACKS[22]}."
		extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		emit(identifier, label, "coil", address, "used", refs, **extra)

	# 25-32: A/C-relay-multiplexed "C"-side flashers, same driver transistors as 1-8.
	for address, label in SOLENOID_C_LABELS.items():
		identifier = output_id(label)
		a_address = address - 24
		flashlamp, quantity = SOLENOID_C_FLASHLAMPS[address]
		notes = (
			f"Printed Solenoid Table entry {a_address:02d}C (Switched). Circuit C is pulsed while solenoid 12 (A/C "
			f"Select Relay) is energized, using the same driver transistor ({SOLENOID_A_DRIVER[a_address]}) as "
			f"solenoid {a_address:02d}A ({SOLENOID_A_LABELS[a_address]}); the two are the same physical driver "
			"circuit routed to a different device by relay contacts, not independent coils."
		)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			notes += (
				f" Retained script callback: {SOLENOID_CALLBACKS[address]}. The retained table implements this "
				"flasher purely as a backglass glow effect (FlSol member of the BGArr backglass-repositioning array, "
				"raw pos_y far outside the 0-2162 playfield bounds), even though the manual's own name for this "
				"device implies a playfield-mounted bulb near the feature it lights. No playfield coordinate can be "
				"derived from this table; see conflict.flasher-backglass-vs-playfield-mounting."
			)
		extra = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{a_address:02d}C"}],
			"physical": {"quantity": quantity, "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "driver_transistor": SOLENOID_A_DRIVER[a_address],
				"power_connection": SOLENOID_C_PLAYFIELD[address],
			},
			# spatial intentionally omitted; see SOLENOID_BACKGLASS_ONLY note above.
		}
		emit(identifier, label, "flasher", address, "used", refs, **extra)

	# 33-36, 42-44, 45-48, 49, 50, 23, 24: platform address-space slots Whirlwind does not fit a
	# real device to.
	for address, notes in VIRTUAL_SOLENOID_NOTES.items():
		label = {
			23: "PinMAME Flipper/Switched-Solenoid Enable State", 24: "Unassigned Solenoid Slot 24",
			33: "Unused Upper Flipper Coil 33", 34: "Unused Upper Flipper Coil 34",
			35: "Unused Upper Flipper Coil 35", 36: "Unused Upper Flipper Coil 36",
			42: "Unused Sound Overlay Board Slot 42", 43: "Unused Sound Overlay Board Slot 43",
			44: "Unused Sound Overlay Board Slot 44",
			45: "Synthetic Lower Right Flipper Power", 46: "Synthetic Lower Right Flipper Hold",
			47: "Synthetic Lower Left Flipper Power", 48: "Synthetic Lower Left Flipper Hold",
			49: "PinMAME Simulator Ball-Shooter Channel", 50: "Unassigned Solenoid Slot 50",
		}[address]
		identifier = output_id(label)
		roles = ["internal.game-on-enable"] if address == 23 else ["internal.synthetic-flipper"] if address in {45, 46, 47, 48} else ["internal.unused-platform-slot"]
		emit(
			identifier, label, "virtual", address, "unused" if address not in {23} else "used",
			(CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
		)

	# 37-41: Sound Overlay Board (public address = manual item number + 14).
	for address, label in SOLENOID_OVERLAY_LABELS.items():
		identifier = output_id(label)
		manual_item = SOLENOID_OVERLAY_MANUAL_ITEM[address]
		notes = (
			f"Printed Solenoid Table item {manual_item} (\"Snd O/L {manual_item - 22}\"), routed over a ribbon cable "
			f"to the Sound Overlay Solenoid Board. The manual's own board-local item number ({manual_item}) is not "
			f"the PinMAME public address; the offset (public = manual item + 14) is resolved by cross-referencing "
			"pinned PinMAME's own doc comment ('37-41 Sound overlay board', core.h) against the retained script's "
			f"SolCallback registrations."
		)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		kind = "motor" if address in {38, 41} else "flasher"
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": str(manual_item)}],
			"wiring": {
				"board": "Sound Overlay Solenoid Board", "driver_transistor": SOLENOID_OVERLAY_DRIVER[address],
				"drive_wire": SOLENOID_OVERLAY_WIRE[address], "control_connection": "1P21 (ribbon cable to SOL Bd)",
				"power_connection": SOLENOID_OVERLAY_SOL_J4[address],
			},
		}
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}, confirming this address directly."
		if address == 38:
			notes += (
				" No fan mesh or primitive exists anywhere in the retained table's extraction; SolBackwallFan only "
				"toggles a backglass flasher (FlSol38, BGArr member) and starts/stops a 'Topper_Fan' sound cue. "
				"The manual confirms cabinet placement ('Blower Motor atop B'box') and no switch. Cabinet-mounted, "
				"no playfield coordinate."
			)
			extra["roles"] = ["cabinet.fan"]
			extra["physical"] = {"part_number": SOLENOID_OVERLAY_PART[address], "notes": notes}
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 41:
			notes += (
				" Drives the three-disc turntable mechanism (ttLeftSpinner/ttMiddleSpinner/ttRightSpinner MotorOn+"
				"Speed); see mechanism.spinning-discs. The manual's own Wheels Drive Assembly parts list (printed "
				"page 66) confirms a single motor (14-7955) drives all three discs through a shared gear train, "
				"with no per-disc coil."
			)
			extra["physical"] = {"part_number": SOLENOID_OVERLAY_PART[address], "notes": notes}
			# The Wheels Drive Assembly (D-13199) is a shared central mechanism; its own mounting bracket has no
			# single meaningful playfield (x, y) distinct from the three disc primitives it turns. Documented as a
			# projection onto the middle disc, the assembly's rotational center.
			extra["physical"]["notes"] += " Projected onto the middle disc (Primitive.MiddleWheel, table object center), the visual center of the shared drive assembly."
			extra["spatial"] = located(identifier, "effect", [(0.565785, 0.551479)], VPX_TABLE_SOURCE)
		else:
			flashlamp = SOLENOID_OVERLAY_PART[address]
			extra["physical"] = {"quantity": int(flashlamp.split("bp")[0][-1]) if "bp" in flashlamp else 1, "notes": notes}
			notes += (
				" The retained table implements this flasher purely as a backglass glow effect (FlSol member of the "
				"BGArr backglass-repositioning array, raw pos_y far outside the 0-2162 playfield bounds), even "
				"though the manual's own name implies a playfield-mounted bulb. No playfield coordinate can be "
				"derived from this table; see conflict.flasher-backglass-vs-playfield-mounting."
			)
			extra["physical"]["notes"] = notes
			# spatial intentionally omitted; see SOLENOID_BACKGLASS_ONLY note above.
		emit(identifier, label, kind, address, "used", refs, **extra)

	return items


LAMP_POSITIONS = {
	1: (0.534823, 0.260046), 9: (0.138743, 0.714020), 10: (0.875743, 0.710625),
	11: (0.612769, 0.308283), 12: (0.620860, 0.286312), 13: (0.627678, 0.262782), 14: (0.634208, 0.241153),
	15: (0.643219, 0.216197), 16: (0.651721, 0.188950),
	17: (0.507761, 0.751709), 18: (0.423153, 0.738282), 19: (0.384995, 0.699959), 20: (0.423700, 0.663644),
	21: (0.509290, 0.646519), 22: (0.592801, 0.663556), 23: (0.631085, 0.700504), 24: (0.591473, 0.737660),
	25: (0.605515, 0.440562), 26: (0.636922, 0.420963), 27: (0.690518, 0.418071), 28: (0.731089, 0.431244),
	29: (0.740017, 0.455841), 30: (0.708962, 0.474984), 31: (0.656202, 0.478552), 32: (0.613182, 0.464332),
	33: (0.081654, 0.381758), 34: (0.230675, 0.314318), 35: (0.302685, 0.401167), 36: (0.365677, 0.119520),
	37: (0.572691, 0.102691), 38: (0.532656, 0.190552), 39: (0.143808, 0.470758), 40: (0.345436, 0.440059),
	41: (0.713324, 0.374736), 42: (0.735881, 0.335705), 43: (0.612977, 0.345704), 44: (0.513142, 0.321156),
	45: (0.417101, 0.297672), 46: (0.882212, 0.457146), 47: (0.757600, 0.405426), 48: (0.598432, 0.387459),
	49: (0.261348, 0.659187), 50: (0.228056, 0.433808), 51: (0.422232, 0.477915), 52: (0.418910, 0.234930),
	53: (0.679651, 0.308830), 54: (0.804060, 0.350782), 55: (0.874534, 0.341587), 56: (0.842636, 0.538893),
	57: (0.507094, 0.874461), 58: (0.363891, 0.785374), 59: (0.420767, 0.793690), 60: (0.477756, 0.801414),
	61: (0.534746, 0.801142), 62: (0.592707, 0.793401), 63: (0.647747, 0.785388), 64: (0.900559, 0.290056),
}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(2, 9):
		label = BACKGLASS_REEL_LAMPS[address]
		identifier = f"lamp.backglass-reel-{address}"
		items.append(
			_device(
				identifier, label, "lamp", "pinmame.output.lamp", address, "used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
				physical={"notes": f"Printed lamp-matrix drive column 1, return row {address}. UpdateLamps drives this address with FadeRm against a Reel object (L{address}), a backglass scoring-feature indicator reel, not a Light bulb."},
				wiring={"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[1][0], "drive_connection": LAMP_COLUMN_WIRING[1][1], "return_wire": LAMP_ROW_WIRING[address][0], "return_connection": LAMP_ROW_WIRING[address][1]},
				roles=["cabinet.backglass-reel"],
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
			)
		)

	for address in range(1, 65):
		if address in BACKGLASS_REEL_LAMPS:
			continue
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		label = LAMP_LABELS[address]
		identifier = f"lamp.matrix-{address}"
		notes = f"Printed lamp-matrix drive column {column}, return row {row}."
		if address in LAMP_LOCATIONS_PAGE_WORDING:
			notes += f" The lamp-locations parts list (page 77) prints this insert \"{LAMP_LOCATIONS_PAGE_WORDING[address]}\"; the lamp-matrix wiring table (page 76, used here) prints \"Arrow\" for the same address."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
			"physical": {"quantity": 1, "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
				"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
				"driver_transistor": f"column driver {LAMP_COLUMN_WIRING[column][2]}",
			},
			"spatial": located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE),
		}
		if address in {39, 40}:
			extra["physical"]["notes"] += " Bound to Primitive.l39/l40 in the retained table (an image-swap indicator, not a simple Light bulb): NFadeObjm toggles between 'bulbcover1_redOn'/'bulbcover1_red' (39) and 'bulbcover1_yellowOn'/'bulbcover1_yellow' (40)."
		items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
	return items


def displays() -> list[dict[str, Any]]:
	return [
		{
			"id": "display.alphanumeric",
			"label": "16-character x 2-line alphanumeric display",
			"kind": "segment",
			"controller_index": 0,
			"segment_start": 0,
			"width": 16,
			"height": 2,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		return record

	return [
		mechanism(
			"mechanism.spinning-discs", "Three motorized spinning discs", "motorized",
			[output_id("Spin Wheels Motor")], [],
			"A single motor (Wheels Drive Assembly, p/n D-13199) drives a shaft/pinion/gear train (72T/84T/115T "
			"gears) turning three playfield discs (LeftWheel, MiddleWheel, RightWheel) simultaneously through "
			"solenoid 41. The retained script spins the middle disc opposite sense (+50) from the two outer discs "
			"(-50) and coasts the assembly down (SpinnerStep decays by 0.05/tick) rather than stopping instantly "
			"when the solenoid de-energizes. The Wheels Drive Assembly parts list lists no switch, opto, or sensor "
			"part of any kind, and no Controller.Switch call anywhere in the retained script is associated with any "
			"of the three discs or their cvpmTurntable collision helpers -- both independent sources agree this is "
			"a pure motor-driven obstacle with no position or ball-pass feedback.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="D-13199",
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other",
			[output_id("Knocker")], [],
			"Solenoid 6 raps a knocker coil mounted in the backbox to give an audible award/replay signal; no "
			"switch is associated with it.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.fan", "Cabinet blower fan", "motorized",
			[output_id("Blower Motor (Fan)")], [],
			"A blower motor mounted atop the backbox (driven via the Sound Overlay Solenoid Board and a Triac "
			"board, p/n 14-7956) with no associated switch. The retained script only toggles a backglass glow cue "
			"(FlSol38) and starts/stops a 'Topper_Fan' sound effect; no fan mesh exists anywhere in the retained "
			"table's extraction.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.trough", "Four-position ball trough and outhole", "kicker",
			[output_id("Outhole Kicker"), output_id("Shooter Lane Feeder")],
			["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13"],
			"A ball draining from the playfield lands in the outhole (switch 10) and is kicked into the trough "
			"proper (solenoid 1, Outhole Kicker); up to three balls queue at trough positions 1-3 (switches 11-13); "
			"solenoid 2 (Shooter Lane Feeder) ejects the lead ball into the shooter lane through the BallRelease "
			"kicker. The retained script manages all four switches through its cvpmBallStack helper "
			"(bsTrough.InitSw 10,11,12,13) with no individual per-position trigger objects.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.cellar", "Left/right cellar subway", "kicker",
			[output_id("Cellar Kickback")], ["switch.matrix-19", "switch.matrix-20"],
			"A ball entering the right cellar opening (switch 19, kCellarRight) or left cellar opening (switch 20, "
			"kCellarLeft) travels through a below-playfield subway; solenoid 14 (Cellar Kickback) ejects it back to "
			"the playfield through the left cellar exit (kCellarLeft, exit speed/angle 157/16 per the retained "
			"script's cvpmTrough helper).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-13225",
		),
		mechanism(
			"mechanism.ball-lock", "Three-position left ball lock", "kicker",
			[output_id("Left Locking Kickback")],
			["switch.matrix-22", "switch.matrix-23", "switch.matrix-24"],
			"A locking kickback assembly (p/n B-13269) holds up to three balls in a row along the left playfield "
			"edge, sensed by switches 22 (lower), 23 (middle), and 24 (upper). Solenoid 4 (Left Locking Kickback) "
			"releases the chain by firing Kicker3, then (on Kicker3's own hit event) Kicker2, then Kicker1 in "
			"sequence, walking a ball down from the top position to the exit.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-13269",
		),
		mechanism(
			"mechanism.top-saucer", "Top-right saucer/eject hole", "kicker",
			[output_id("Top Eject")], ["switch.matrix-43"],
			"A ball resting on switch 43 (Top Right Eject, the saucer's own named kicker object) is kicked back to "
			"the playfield by solenoid 5 (Top Eject) through the retained script's cvpmBallStack saucer helper.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.right-ramp", "Right ramp lifter/diverter", "diverter",
			[output_id("Right Ramp Lifter"), output_id("Right Ramp Down"), output_id("Diverter")],
			["switch.matrix-42"],
			"Solenoid 3 (Right Ramp Lifter) raises the right ramp entry into its 'up' geometry (RightRampUp visible "
			"and collidable, RightRampDown hidden) and solenoid 22 (Right Ramp Down, a 'special' solenoid) reverses "
			"it; the retained script tracks which geometry is active directly via Controller.Switch(42), matching "
			"switch 42's real printed part (5647-12001-00) even though no separate VPX trigger object senses it. "
			"Solenoid 13 (Diverter) independently rotates a playfield diverter (25deg/0deg) that steers ball flow "
			"near the ramp entrance.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.drop-targets", "Single and 3-bank opto drop targets", "drop_target_bank",
			[output_id("1-Bank Drop Target Reset"), output_id("3-Bank Drop Target Reset")],
			["switch.matrix-26", "switch.matrix-27", "switch.matrix-28", "switch.matrix-29"],
			"A single drop target (switch 26, opto-sensed via the 1-Bank Opto Board C-13311) and a 3-bank drop "
			"target group (switches 27-29, opto-sensed via the 3-Bank Opto Board C-13205-1) are reset by solenoids "
			"8 and 7 respectively. The retained script's dtT/dtL drop-target helper objects fire Hit(1)/Hit(2)/"
			"Hit(3) as each bank target falls.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers", "Six-bumper jet nest (two triangular clusters)", "other",
			[
				output_id("Left Lower Jet Bumper"), output_id("Right Lower Jet Bumper"), output_id("Top Lower Jet Bumper"),
				output_id("Left Upper Jet Bumper"), output_id("Right Upper Jet Bumper"), output_id("Top Upper Jet Bumper"),
			],
			["switch.matrix-49", "switch.matrix-50", "switch.matrix-51", "switch.matrix-52", "switch.matrix-53", "switch.matrix-54"],
			"Two clusters of three jet bumpers each: an upper cluster near the top of the playfield (switches 49-51, "
			"solenoids 17/19/21) and a lower cluster nearer the cellar (switches 52-54, solenoids 9/15/10). Each "
			"bumper's coil and switch are the same physical assembly (B-12030-2).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-12030-2",
		),
		mechanism(
			"mechanism.slingshots", "Bottom-left and bottom-right slingshot kickers", "other",
			[output_id("Left Kicker (Slingshot)"), output_id("Right Kicker (Slingshot)")],
			["switch.matrix-55", "switch.matrix-56"],
			"Two slingshot kickers (BL/BR Kicker, each a paired kicker-actuating switch assembly per the "
			"switch-locations *** footnote) sensed at switches 55/56 and fired by solenoids 18/20. The retained "
			"script's LeftSlingShot_Slingshot/RightSlingShot_Slingshot handlers play a multi-frame flip-book "
			"animation on each kick.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Three cabinet-fired flippers (lower-left, lower-right, upper-right)", "other",
			[],
			["switch.matrix-57", "switch.matrix-58"],
			"Three physical flipper assemblies (Lower Left C-11626-L-3, Lower Right C-11626-R-3, Upper Right "
			"C-11626-R-3; no upper-left flipper exists). Pinned PinMAME declares FLIP_SWNO(58,57) with no FLIP_SOL "
			"bit: the cabinet flipper buttons (SW-10A-48 left, SW-1010A-13 right) fire their coils directly through "
			"a relay/fuse circuit with zero CPU involvement (no public solenoid address corresponds to a real "
			"driver-board output), while a separate Backbox Interconnect Board optotransistor pair independently "
			"watches the same buttons and reports their state to the CPU at matrix addresses 57 (right) and 58 "
			"(left) for the 'Flipper Lane Change' feature. The retained script's SolRFlipper handler rotates both "
			"RightFlipper (lower) and RightFlipper1 (upper) together, confirming the upper-right flipper shares the "
			"lower-right flipper's coil/button rather than having an independent one.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="C-11626-L-3 left with C-11626-R-3 right (x2)",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ball-lock-chain",
			"kind": "pulse",
			"source": output_id("Left Locking Kickback"),
			"destination": "switch.matrix-24",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.right-ramp-lifter-switch",
			"kind": "direct",
			"source": output_id("Right Ramp Lifter"),
			"destination": "switch.matrix-42",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.flasher-backglass-vs-playfield-mounting",
			"path": "outputs[binding.device=25,26,27,28,29,30,31,32,37,39,40]",
			"description": (
				"The Solenoid Table names all eleven of these addresses after playfield features they light -- "
				"e.g. 'R Ramp Top/Upr Jets Flashers' (28), 'BP Lightning (L) Flashers' (37) -- implying bulbs "
				"mounted on or near the playfield feature itself, and the manual's Solenoid Table 'p'/'bp' bulb-"
				"quantity footnotes ('#906 flashlamps... p' for playfield bulbs elsewhere in the same table) draw "
				"exactly that playfield/backbox distinction. The retained known-working VPX script implements every "
				"one of these eleven addresses purely as a backglass effect: each SolNN(enabled) handler toggles "
				"the visibility of an FlSolNN Flasher object, and all eleven FlSol25-FlSol32/FlSol37/FlSol39/"
				"FlSol40 objects are confirmed members of the script's BGArr backglass-repositioning array with raw "
				"pos_y values far outside the 0-2162 playfield bounds (e.g. FlSol25.pos_y=-902.14825). No playfield "
				"coordinate can be derived from this table for any of the eleven addresses. Resolution path: a "
				"second retained table, a photograph of an unrestored machine's lower playfield, or the manual's "
				"Section 3 wiring diagrams (not transcribed here) showing a distinct playfield connector run for "
				"one of these circuits, would settle whether real playfield-mounted bulbs exist alongside (or "
				"instead of) the backglass effect this table models. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
		},
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


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "williams.whirlwind.1990",
			"name": "Whirlwind",
			"manufacturer": "Williams",
			"year": 1990,
			"kind": "physical_pinball",
			"playfield": {"width": 964.0, "height": 2162.0, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.system-11",
			"hardware_generation": "0x100",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/whirlwind-1990.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Whirlwind device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	omitted_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			omitted_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	for device in definition["inputs"]:
		if device["spatial"]["status"] != "not_applicable":
			placement_count += len(device["spatial"]["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"GI address 11 (Upper Playfield GI) has no bound playfield light object in the retained VPX table "
			"(the UpperGI light collection is empty); pinned PinMAME and the manual both confirm the address is a "
			"real physical GI relay, but no coordinate can be derived from this evidence, so its spatial key is "
			"omitted rather than invented.",
			"Eleven flasher solenoid addresses (25-32, 37, 39, 40) are implemented purely as backglass effects in "
			"the retained table (BGArr member Flasher objects with negative pos_y) even though the manual names "
			"them after playfield features; recorded as conflict.flasher-backglass-vs-playfield-mounting and left "
			"unresolved rather than guessed. Their spatial keys are omitted.",
			"Four opto-constructed switches (26-29, drop targets) and the flipper-lane-change opto pair (57, 58) "
			"have confirmed construction but no confirmed rest-state polarity: this manual states no shading/"
			"typically-closed legend, and pinned PinMAME declares no inverted-switch mask at all for whirl_l3 "
			"(wpc.invSw is entirely unset), so the public state is never emulator-normalized for this driver.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"omitted_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.whirlwind.1990/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/whirlwind/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"vpx_geometry": {
				"path": "external:pinmame-review-artifacts/whirlwind/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"l33a-l38a, l39a, l40a bloom/halo companion Light objects (BloomLights array)",
			"L2-L8 backglass score-reel Reel objects (BG collection) -- see lamp.backglass-reel-* not_applicable records",
			"f125-f132/f137/f139/f140 solenoid-controlled flasher-lamp companions in UpdateLamps -- backglass-repositioned, not distinct playfield devices",
		],
		"unresolved": ["conflict.flasher-backglass-vs-playfield-mounting"],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Whirlwind (Williams, 1990) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record itself remains `partial` at "
		"`machines/partial/williams/whirlwind-1990.json` because of the unresolved backglass-vs-playfield flasher "
		"mounting conflict and the unconfirmed opto polarity noted below; see the promotion decision.",
		"",
		"The matching source is the retained known-working `Whirlwind (Williams 1990).vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained vpxtool extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Williams operations manual "
		"is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology and the System 11 address-space rules; the retained table supplies geometry.",
		"- System 11 has no separate GI address space: GI is simply two ordinary solenoid addresses (11, 16) whose "
		"per-game bulb-type metadata happens to be continuous AC GI bulbs, resolved from pinned PinMAME's own "
		"per-game MACHINE_INIT block rather than any fixed platform range.",
		"- Switches 10-13 (outhole/trough) and 42 (right ramp down) have no dedicated VPX trigger object in the "
		"retained table; they are documented projections onto the nearest real mechanism object (the Drain/"
		"BallRelease kickers, and the Right Ramp's own up/down geometry) rather than invented coordinates.",
		"- Eleven flasher addresses are implemented purely as backglass effects in the retained table even though "
		"the manual names them after playfield features; this is recorded as an unresolved first-class conflict "
		"and their spatial keys are omitted rather than guessed either way.",
		"- GI address 11 has an empty light collection in the retained table; its spatial key is omitted rather "
		"than invented, matching the precedent set for Star Trek: The Next Generation's unresolved lamps.",
		"- The three spinning discs are a pure motor mechanism (solenoid 41) with no position sensor, confirmed "
		"independently by both the retained script (no Controller.Switch call for any disc object) and the "
		"manual's own Wheels Drive Assembly parts list (no switch/opto part).",
		"- The alphanumeric display is cabinet/backbox hardware, so its spatial record is a controlled "
		"`not_applicable` with both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with an intentionally omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this "
		"audit locates. However, eleven flasher solenoid addresses (25-32, 37, 39, 40) are implemented purely as "
		"backglass effects in the retained table while the manual names them after playfield features -- an "
		"unresolved conflict recorded as `conflict.flasher-backglass-vs-playfield-mounting` -- and four opto "
		"switches (26-29) plus the flipper-lane-change opto pair (57, 58) have confirmed construction but no "
		"confirmed rest-state polarity, since pinned PinMAME declares no inverted-switch mask at all for this "
		"driver. The definition therefore carries a non-empty `conflicts` array and "
		"`coverage.missing = [\"polarity\", \"spatial_placement\", \"unresolved_conflicts\"]`, so promotion to "
		"`author_ready` is refused; the record stays `partial` until a second independent table, a photograph of "
		"an unrestored machine's playfield, or a manual wiring diagram settles the flasher-mounting question, and "
		"a LibPinMAME harness trace or a manual opto-polarity legend settles the rest-state question.",
		"",
		"## Retained evidence",
		"",
		f"- Retained vpxtool extraction, {EXTRACTION_FILE_COUNT} files.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- VPX script/geometry cross-reference, SHA-256 `{VPX_GEOMETRY_SHA256}`.",
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
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if not definition_path.is_file():
		raise RuntimeError(f"Whirlwind definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Whirlwind seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Whirlwind definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Whirlwind seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Whirlwind spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Whirlwind spatial review drifted from its deterministic curator: {markdown_path}")
	print("Whirlwind definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition and pinned seed")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Whirlwind extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Whirlwind retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
