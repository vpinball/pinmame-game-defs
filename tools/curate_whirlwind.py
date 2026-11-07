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
import drawing_callouts
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
DEFINITION_PATH = ROOT / "machines/author-ready/williams/whirlwind-1990.json"
SEED_PATH = ROOT / "tools/seeds/williams/whirlwind-1990.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/whirlwind-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/whirlwind-1990.md"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/whirlwind-1990.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.whirlwind.1990"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.whirlwind.1990"
VPX_TABLE_SOURCE = "vpx-table.whirlwind-1990"
VPX_SCRIPT_SOURCE = "vpx-script.whirlwind-1990"
VPX_EXTRACTION_SOURCE = "vpx-extraction.whirlwind-1990"
DROP_LEVELS_SOURCE = "runtime.whirlwind.drop-target-levels"
SERVICE_SOURCE = "runtime.whirlwind.service-tests"
BIGUS_SOURCE = "vpx-table.whirlwind-bigus-supplement"
FLASHER_TABLE_SOURCE = "vpx-table.whirlwind-4k-flasher-geometry"
FLASHER_DRAWING_SOURCE = "manual-measurement.whirlwind-flashers"
GI_PHOTO_SOURCE = "physical-photo.whirlwind-gi"
GI_BLINKER_SOURCE = "physical-photo.whirlwind-backbox-blinkers"
GI_STOCK_SOURCE = "physical-photo.whirlwind-stock-bank-sockets"
GI_BANK_SOURCE = "manual-measurement.whirlwind-three-bank-gi"
GI_CURVE_SOURCE = "physical-photo.whirlwind-left-curve"
GI_CORNER_SOURCE = "physical-photo.whirlwind-right-rear-bulbs"
GI_WIRE_SOURCE = "physical-photo.whirlwind-left-points-wire-passage"
GI_INVENTORY_SOURCE = "physical-review.whirlwind-playfield-gi-inventory"
REAR_ASSEMBLY_SOURCE = "manual.williams.whirlwind-d13356"
REAR_PHOTO_SOURCE = "physical-photo.whirlwind-d13356"
REAR_GI_BRANCH_SOURCE = "physical-repair.whirlwind-rear-gi-branch"
REAR_PLACEMENT_SOURCE = "physical-projection.whirlwind-rear-panel"
MATRIX_BULB_SOURCE = "physical-review.whirlwind-matrix-bulbs"
HIDDEN_BULB_SOURCE = "physical-projection.whirlwind-million-bulbs"
HANDBOOK_SOURCE = "manual.williams.whirlwind-operators-handbook"
RAMP_DOME_SOURCE = "manual.williams.whirlwind-r13190-lamps"
FLASHER_SEED_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-flasher-callouts.json"
FLASHER_SEED_SHA256 = "fbdeb5dbbe409c3031df947d4755ee11425079e45efda46dc73964ed6877a218"
GI_BANK_SEED_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-gi-bank-callouts.json"
GI_BANK_SEED_SHA256 = "8e8d4a9b51e8667e57cae5ac8c8c70ded49d092aad3af8dd94daff50274db03b"
GI_INVENTORY_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-gi-inventory.json"
GI_INVENTORY_SHA256 = "2d9c98894d3d7c63c404cf78e6d44353de6088c7430046bde3b3ae681e763b31"
REAR_PLACEMENT_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-rear-panel-projection.json"
REAR_PLACEMENT_SHA256 = "61ef011370e3c0a23caa8a976b9bb0145353d7d0654681493999788c05516391"
MATRIX_BULB_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-matrix-bulbs.json"
MATRIX_BULB_SHA256 = "92547887b8ee3675356af0feff4dca6b74c38670d22cf99fa1659d7ce87944a5"
HIDDEN_BULB_PATH = ROOT / "tools/seeds/williams/whirlwind-1990-hidden-bulbs.json"
HIDDEN_BULB_SHA256 = "4c5e47b2fd2e6aab49973b06583de57f360ea71384f41872dcfab2abd1232778"
SERVICE_RUN_SHA256 = "8ebba45898c3b38a1ce90a9ad38cbab1bf4cc93b572bb24c8614a2da1a71495e"
COIL_RUN_SHA256 = "168021c8e573436e4c750805775dc99489749c5d79ae471d963362c7dddf2d39"
VPM_EXCERPT_SHA256 = "4264fb8055edb5553560743a73ef9460cbae9ca93ce832cfc87ff833c12112dd"
# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (58, 57)

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
EXTRACTION_TOTAL_BYTES = 129468345
EXTRACTION_MANIFEST_SHA256 = "4b3b7045c243787f381a42be2479aa53325783618820689468b6b0bce8dc7b49"

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
	30: "Ramp Bottom Flasher (Left Playfield)", 31: "3-Bank Target/Middle Target Flashers", 32: "Million+/Compass Flashers",
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
	20: "Right Kicker (Slingshot)", 21: "Bottom Upper Jet Bumper", 22: "Right Ramp Down",
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
# The handbook's 2/1/2 is corroborated by the complete D13356 drawing and
# actual ten-position PCB. Keep the operations table's 3bp literal above.
REAR_FLASHER_QUANTITIES = {37: 2, 39: 1, 40: 2}

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
	33: "Platform generic upper-flipper-coil address (CORE_FIRSTUFLIPSOL). Whirlwind's hw.flippers declares no FLIP_U* bit, and core_getSol only serves 33-36 for GEN_ALLWPC/GEN_SAM, so this reads as always-zero. The physical upper-right flipper has its own coil, wired to the same cabinet button as the lower-right coil; it has no independent public output.",
	34: "Platform generic upper-flipper-coil address; unused, see address 33.",
	35: "Platform generic upper-flipper-coil address; unused, see address 33.",
	36: "Platform generic upper-flipper-coil address; unused, see address 33.",
	42: "Outer bound of the platform's 'Sound overlay board' address range (core_getSol's GEN_ALLS11 branch serves 37-44); Whirlwind's own Sound Overlay Board populates only 37-41 (5 devices, matching the 5 manual items 23-27), confirmed by the retained script's own SolCallback registrations stopping at 41. No device is wired at 42.",
	43: "Outer bound of the platform's Sound Overlay Board address range; unused, see address 42.",
	44: "Outer bound of the platform's Sound Overlay Board address range; unused, see address 42.",
	45: "PinMAME's synthetic lower-right-flipper power output (CORE_FIRSTLFLIPSOL). Whirlwind's hw.flippers is FLIP_SWNO(58,57) with no FLIP_SOL bit, so core_updateSw fabricates this address (with 46) from PinMAME's flipper column, public 82, the right cabinet button that it also copies into matrix switch 57, while the switched-solenoid enable (23) is on; on real hardware the lower-right flipper button fires its coil directly through a relay/fuse circuit with no independent CPU coil drive, confirmed by the Solenoid Table's own flipper rows carrying no Sol. No. and by note 2 ('Flipper connections shown in braces are from flipper switch to flipper coil'). The CPU senses lower-coil activation through the lane-change optocoupler at matrix switch 57.",
	46: "PinMAME's synthetic lower-right-flipper hold output; see address 45.",
	47: "PinMAME's synthetic lower-left-flipper power output; see address 45. Fabricated (with 48) from public 84, the left cabinet button that core_updateSw also copies into matrix switch 58.",
	48: "PinMAME's synthetic lower-left-flipper hold output; see address 47. Whirlwind's upper-right flipper has a separate coil and EOS switch, sharing the right cabinet button with the lower-right coil (manual Power Wiring Diagram, printed 96). The script rotates both RightFlipper and RightFlipper1 from SolRFlipper; no separate synthetic output models the upper-right coil.",
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
	48: "Skill Shot Left", 56: "Right Standup", 64: "Right Spinner",
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
	identity = (len(files), sum(item["size"] for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Whirlwind retained extraction identity mismatch: files, bytes, manifest_sha256 = {identity}")
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
	# Labels may be corrected without renaming existing public semantic IDs.
	legacy = {
		"Bottom Upper Jet Bumper": "device.top-upper-jet-bumper",
		"Ramp Bottom Flasher (Left Playfield)": "device.right-ramp-bottom-flasher",
	}
	if label in legacy:
		return legacy[label]
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
	gi_inventory()
	rear_panel_seed()
	gi_bank_seed()
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
				"core_updateSw flipper-column copy into FLIP_SWL/FLIP_SWR and synthetic-flipper-solenoid fallback, "
				"locals.flipMask construction; src/wpc/core.h CORE_FLIPPERSWCOL=11, CORE_SWLRFLIPEOSBIT..CORE_SWULFLIPBUTBIT, "
				"FLIP_SWNO/FLIP_SW/FLIP_EOS/FLIP_SOL, CORE_LRFLIPSOLBITS/CORE_LLFLIPSOLBITS; src/wpc/gen.h "
				"GEN_S11B==GEN_S11X==GEN_S11A; src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_S11B=0x100"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json",
			"revision": "repository",
			"locator": "System 11 public switch/lamp sequential-matrix numbering, dedicated diagnostic addresses, the 81-88 flipper column, and the solenoid A/C-mux/special/sound-overlay/GI address rules",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.whirlwind.1990/archive-arcademanual_Whirlwind_OPS/Whirlwind_OPS.pdf",
			"original_filename": "Whirlwind_OPS.pdf", "sha256": MANUAL_SHA256,
			"locator": (
				"Acquired 2026-08-07 from https://archive.org/download/arcademanual_Whirlwind_OPS/Whirlwind_OPS.pdf; "
				"item https://archive.org/details/arcademanual_Whirlwind_OPS, uploaded by manuallibrary@textfiles.com. "
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
					"image": "evidence/excerpts/williams.whirlwind.1990/switch-locations.webp",
					"image_sha256": "b9791a4a4c4922fa9b02039437e7edfd4b75bf1b67e0753cc74a770df8e39a80",
					"image_derivation": "Whirlwind_OPS.pdf page 84, crop box 0.04,0.04,0.96,0.9, scanned page rendered at its native resolution (embedded image xref 361, 2472px across 8.24in), rendered at 79 dpi, capped to 600px wide, 601x744 WebP quality 65",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.power-wiring",
					"locator": "PDF page 106 printed 96: four GI branches and separate left/right flipper circuits; PDF 62 printed 52 lamp-board parts; PDF 52 printed 42 board location",
					"path": "evidence/excerpts/williams.whirlwind.1990/power-wiring.md",
					"sha256": "9fefc2089c8718c66ac45f3601eccfd4d4ac7d72698c26de8e6aa32577b4e29a",
					"image": "evidence/excerpts/williams.whirlwind.1990/power-wiring.webp",
					"image_sha256": "7956dd02d87fefeb26046d12b8b8d46d4372c60c00e48be0f33f02c15f7fade4",
					"image_derivation": "Whirlwind_OPS.pdf page 106, crop box 0.06,0.56,0.91,0.87, scanned page rendered at its native resolution (embedded image xref 466, 3307px across 16.54in), rendered at 100 dpi, capped to 1400px wide, grayscale, 1401x362 WebP quality 80",
					"method": "manual", "transcribed_by": "repository curator, visually checked against factory schematic and parts tables", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.switch-matrix", "locator": "PDF page 85, printed page 75, Switch-Matrix Table",
					"path": "evidence/excerpts/williams.whirlwind.1990/switch-matrix.md",
					"sha256": "bc3dcd1628892ae3eb3633a6e91994abc1b19ad28205f57ac4b629123aaf2b94",
					"image": "evidence/excerpts/williams.whirlwind.1990/switch-matrix.webp",
					"image_sha256": "ccf6b0613104043484667358ced655e583684f5f63c539301f3ae3ff458227d2",
					"image_derivation": "Whirlwind_OPS.pdf page 85, crop box 0.05,0.04,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 366, 2472px across 8.24in), rendered at 92 dpi, capped to 700px wide, 1001x867 WebP quality 70",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.lamp-matrix", "locator": "PDF page 86, printed page 76, Lamp-Matrix Table",
					"path": "evidence/excerpts/williams.whirlwind.1990/lamp-matrix.md",
					"sha256": "d4c62161c161d4675b88869f72b3513dd3b31876372c433e5173b36e1eef64ae",
					"image": "evidence/excerpts/williams.whirlwind.1990/lamp-matrix.webp",
					"image_sha256": "84c7728abd97a7bddc14d5bb9691e84d90831bbdb720bbd84050e3d8070d7619",
					"image_derivation": "Whirlwind_OPS.pdf page 86, crop box 0.05,0.04,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 370, 2484px across 8.28in), rendered at 92 dpi, capped to 700px wide, 1001x867 WebP quality 70",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.lamp-locations", "locator": "PDF page 87, printed page 77, Lamps locations",
					"path": "evidence/excerpts/williams.whirlwind.1990/lamp-locations.md",
					"sha256": "5fffaa4a4ade7fc732d3df3693243c7468050337bcd4f5a803568464cf9e8d04",
					"image": "evidence/excerpts/williams.whirlwind.1990/lamp-locations.webp",
					"image_sha256": "a0c3abdc92d7c3cb0c2254c9aa7ff3ee4205e1d850ac9f4fe9c49164c61990dc",
					"image_derivation": "Whirlwind_OPS.pdf page 87, crop box 0.05,0.04,0.96,0.9, scanned page rendered at its native resolution (embedded image xref 374, 2484px across 8.28in), rendered at 93 dpi, capped to 700px wide, 1001x877 WebP quality 70",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.solenoid-flasher-locations",
					"locator": "PDF page 8 quick-reference Solenoid Table, page 42 printed 32 duplicate, page 83 printed 73 separate Solenoids/Flashers location list and drawing",
					"path": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-locations.md",
					"sha256": "57ea848bdc56e8afc15e34a7e0d5d59b598f55595ea68a3886583d8fadd7de21",
					"image": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-locations.webp",
					"image_sha256": "63f9415fda1162c65ff7e6bf2c2fe6954983134e8d68034d2b3aa49aaefdcc91",
					"image_derivation": "Whirlwind_OPS.pdf page 8, crop box 0.04,0.04,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 30, 2497px across 8.32in), rendered at 78 dpi, capped to 600px wide, 601x735 WebP quality 65",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.solenoid-flasher-wiring",
					"locator": "PDF pages 43 and 105, printed pages 33 and 95, special/controlled solenoid theory and schematic",
					"path": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-wiring.md",
					"sha256": "2db57788e02ec38544a6b2b1d32655a2fc8a8a40d9bfe77db03b4f9e72206a90",
					"image": "evidence/excerpts/williams.whirlwind.1990/solenoid-flasher-wiring.webp",
					"image_sha256": "97c1c0b9ef67771621ecbec29d7c4eb8580d1f4602225411bd13b8f8559ae6ee",
					"image_derivation": "Whirlwind_OPS.pdf page 105, crop box 0.03,0.04,0.98,0.88, scanned page rendered at its native resolution (embedded image xref 461, 3307px across 16.54in), rendered at 45 dpi, capped to 700px wide, 1001x439 WebP quality 70",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.general-illumination", "locator": "PDF page 63, printed page 53, GI relay boards",
					"path": "evidence/excerpts/williams.whirlwind.1990/general-illumination.md",
					"sha256": "0e96cc2b83f8fb4bb41f5f7653a7d327885519bddf067401c3b6fc72f0454914",
					"image": "evidence/excerpts/williams.whirlwind.1990/general-illumination.webp",
					"image_sha256": "5d8b1e4e7e01184b1f1032462ae58f2881295720811b97b0266b1aa4e5c24f0f",
					"image_derivation": "Whirlwind_OPS.pdf page 63, crop box 0.05,0.05,0.96,0.85, scanned page rendered at its native resolution (embedded image xref 272, 2497px across 8.32in), rendered at 93 dpi, capped to 700px wide, 1001x816 WebP quality 70",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.whirlwind.boards-and-assemblies",
					"locator": "PDF pages 76 and 88, printed pages 66 and 78, Wheels Drive Assembly and flipper assembly parts",
					"path": "evidence/excerpts/williams.whirlwind.1990/boards-and-assemblies.md",
					"sha256": "975410acc7f0b9b54538794c6217d7e56dc5420efb89a0c1b6319cdba362415d",
					"image": "evidence/excerpts/williams.whirlwind.1990/boards-and-assemblies.webp",
					"image_sha256": "241080c57a8b50776a335da164f0aeada9212e25d467ee50a46c9c6d954c27ff",
					"image_derivation": "Whirlwind_OPS.pdf page 88, crop box 0.05,0.04,0.96,0.9, scanned page rendered at its native resolution (embedded image xref 378, 2484px across 8.28in), rendered at 80 dpi, capped to 600px wide, 601x752 WebP quality 65",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind/manual-transcription.md", "revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": "Historical 2026-08-07 transcription retained unchanged for audit. Corrected and expanded repository excerpts on MANUAL_SOURCE supersede its mislabeled flasher mounting, incomplete tables and other corrected readings; do not treat this historical summary as current physical authority.",
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
			"excerpts": [{
				"id": "excerpt.whirlwind.script-lighting", "locator": "SolCallback table, Sol25-Sol40, SolUpperGI/SolLowerGI and UpdateLamps",
				"path": "evidence/excerpts/williams.whirlwind.1990/script-lighting.md",
				"sha256": "e517a1af6039656f49d57a4ff94359c273252d1cc2f8fbde3b8bbf5c27217f4b",
				"method": "manual", "transcribed_by": "repository curator, checked against retained embedded script and object flags", "reviewed": True,
			}],
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
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script",
			"uri": VPM_LIBRARY_URI,
			"original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads at runtime (script.vbs line 799 LoadVPM "
				"\"01560000\", \"S11.VBS\", 3.26; S11.VBS executes core.vbs), retained from the contributor's working "
				f"installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and "
				"swLLFlip = 84 and sets them from the flipper keys in vpmKeyDown/vpmKeyUp; core.vbs routes "
				"KeyDownHandler/KeyUpHandler to them."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.whirlwind.vpm-script-library-flippers",
					"locator": "s11.vbs lines 37-40, 69-86 and 104-121; core.vbs lines 2061-2062, 2090 and 2854-2855; script.vbs lines 799, 1149 and 1606-1635",
					"path": "evidence/excerpts/williams.whirlwind.1990/vpm-script-library-flippers.md",
					"sha256": VPM_EXCERPT_SHA256,
					"method": "manual", "transcribed_by": "curator, read from the library and script files", "reviewed": True,
				},
			],
		},
		{
			"id": BIGUS_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/supplemental-20261106/primary-bigus/table.vpx",
			"sha256": "7b321c04e92954a2cb119900ba8707c49c90e5b49c0e60ee783ef837e39feb0a",
			"locator": "Supplemental retained Bigus table, same ancestral layout. Lamp 9 binds NfadeL 9,l9 at script.vbs:455; Light.l9 center 133.09065,1546.9991 on 964x2162 bounds agrees with original geometry within 0.002 normalized. Script SHA-256 0ebd3bf51240e632fa9b2d716b9c56ef992a6151392490b77b314101f1af7cb7. vpxtool git:v0.33.3 full sorted extraction manifest: 1259 files, 80205398 bytes, canonical SHA-256 e0b36d739b79021cfde21c81ecf1db0ff9015d0844d9608fd699f56a25ea33f7. GI collections are render groupings and supply no physical counts.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "walamab, Siggi and Bigus, retained community recreation",
		},
		{
			"id": SERVICE_SOURCE, "kind": "runtime_scenario",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/harness-all-levels.json",
			"sha256": SERVICE_RUN_SHA256,
			"locator": f"whirl_l3 Switch Levels, every fitted matrix input except overwritten relay feedback 2; drive 82/84 for 57/58. Companion harness-coils.json SHA-256 {COIL_RUN_SHA256} corroborates sound-overlay public 37-41/manual 23-27. Pinned library and initial NVRAM identities in the excerpt.",
			"excerpts": [{
				"id": "excerpt.whirlwind.rom-service-tests", "locator": "Switch Levels high intervals and Coil Test sound-overlay cycle",
				"path": "evidence/excerpts/williams.whirlwind.1990/rom-service-tests.md",
				"sha256": "823afeeff0ba79d40dbe3c54dc4e81ef6139e3859bf11e9ddd607da40af7a4d3",
				"method": "manual", "transcribed_by": "repository curator, checked against retained raw ROM display and callback events", "reviewed": True,
			}],
		},
		{
			"id": DROP_LEVELS_SOURCE, "kind": "runtime_scenario",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/harness-levels-repeat.json",
			"sha256": "cbf0f2f6ddd0160abbe39902e66444c9fad1362231d9ea284798242a1d66054e",
			"locator": "whirl_l3 Switch Levels: target 26/27/28/29 high and low snapshots, with mechanical control 15 before and after. Pinned native revision 46e1a01a0f73dc5ce163d98db1ae435883ecc450; keyboard and mechanics disabled; fresh factory-initialized NVRAM.",
			"excerpts": [{
				"id": "excerpt.whirlwind.drop-target-levels",
				"locator": "ROM diagnostic snapshots and s11.c pia4a_r, s11games.c INITGAME, working script dtT/dtL and core.vbs cvpmDropTarget",
				"path": "evidence/excerpts/williams.whirlwind.1990/drop-target-levels.md",
				"sha256": "671348ab3c1ac090a61bbd59a5adca58152d9fd7ab082314da33c12e134be196",
				"method": "manual", "transcribed_by": "repository curator, checked against retained code and raw diagnostic displays", "reviewed": True,
			}],
		},
		{
			"id": FLASHER_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/supplemental-20261106/primary-4k-1113/table.vpx",
			"sha256": "4ef5614e92109aa8c9362957e0b8390c56bcf04b098aaacad7cabb8482ffbd54",
			"locator": "Whirlwind 4K1.113, five script-bound Flupper dome bases, bounds 0..952 by 0..2164. Embedded script SHA-256 704319827005cfaa196b4415cd9e42db3ff8b4d55192b711d08884456d7f2501. vpxtool git:v0.33.3 extraction: 3016 files, 351873613 bytes; sorted POSIX path/size/SHA-256 canonical manifest 018991497f6b90ca112c4dc1ca1f582fd6f8bf05d2aec5a38daf40c4d50905a6. Geometry supplement; original known-working script retains runtime authority. See the portable flasher-placement excerpt for exact code paths and raw centers.",
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Flupper, Rothbauerw, Fleep, Blackmoor and the table's credited contributors",
		},
		{
			"id": FLASHER_DRAWING_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-flasher-callouts.json",
			"revision": "2026-11-06", "sha256": FLASHER_SEED_SHA256,
			"locator": "Factory PDF 83/printed 73: nine independent mechanism controls, six round flashlamp-symbol measurements, five dome callout checks; two insert-feature endpoints excluded. Native full-render pixels and object identities in seed; measured coordinates rounded to three decimals.",
			"license": "NOASSERTION", "attribution": "Williams drawing; repository curator visual measurement and geometry review",
			"excerpts": [{
				"id": "excerpt.whirlwind.flasher-placement", "locator": "Factory PDF 83/printed 73 right-hand location drawing and supplemental 4K1.113 script-bound dome bases",
				"path": "evidence/excerpts/williams.whirlwind.1990/flasher-placement.md",
				"sha256": "6c2a1ad854a84b8ee5970f5e851a1d25199fd8d0038947fb072a411b374f10d0",
				"image": "evidence/excerpts/williams.whirlwind.1990/flasher-placement.webp",
				"image_sha256": "4fdde68e8fdc02e736500cd7bc58bf977ccf084f2502a0b6a4f0eec444e479d3",
				"image_derivation": "Whirlwind_OPS.pdf page 83, crop box 0.52,0.1,0.94,0.7, scanned page rendered at its native resolution (embedded image xref 357, 2472px across 8.24in), rendered at 159 dpi, capped to 550px wide, grayscale, 551x1041 WebP quality 65",
				"method": "manual", "transcribed_by": "repository curator, read and checked at native resolution", "reviewed": True,
			}],
		},
		{
			"id": REAR_ASSEMBLY_SOURCE, "kind": "manual",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/primary-red-parts/page0473_i2.jpg",
			"sha256": "9b6351d58ed5405a776d9f585ea1c5852cde6aa1b9ee4b08d5ada840836b8338",
			"acquired_at": "2026-11-06T23:48:17.811073Z", "revision": "Williams Red Parts Catalog 16-9190-B",
			"locator": "Printed 5-37, complete D13356 / PCB 5768-12583-00 front and side elevations and seven-row parts table. Publisher image https://www.planetarypinball.com/reference/partsmanuals/WMS_Parts_Red_16-9190-B/files/assets/mobile/page0473_i2.jpg. Drawing has five #906 and five #555 sockets; literal GI table quantities (4), repeated bulb/socket part number and printed 1-11 nine-lamp index are discrepant. Actual LMP1-LMP10 pattern independently corroborated by the original-board repair photo.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; catalog hosted by Planetary Pinball Supply",
			"excerpts": [{
				"id": "excerpt.whirlwind.rear-panel-lamp-assembly", "locator": "Printed 5-37 D13356 complete parts table and front/side elevations",
				"path": "evidence/excerpts/williams.whirlwind.1990/rear-panel-lamp-assembly.md",
				"sha256": "874c1378687b0697f68706073d8c818aa5c5481231cc7e30cb4423dec2975321",
				"image": "evidence/excerpts/williams.whirlwind.1990/rear-panel-lamp-assembly.webp",
				"image_sha256": "370ce8cbfc0a58728c9edc51336e150cb5fd2ded9095cc58e13f85fbc7bf8878",
				"image_derivation": "page0473_i2-wrapper.pdf page 1, crop box 0.219,0.075,0.486,0.858, scanned page rendered at its native resolution (embedded image xref 3, 1050px across 10.94in), rendered at 96 dpi, grayscale, rotated 270 degrees counter-clockwise, 1065x282 WebP quality 65",
				"method": "manual", "transcribed_by": "repository curator, complete native catalog raster visually checked", "reviewed": True,
			}],
		},
		{
			"id": RAMP_DOME_SOURCE, "kind": "manual",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/primary-red-ramp/page0272_i2.jpg",
			"sha256": "4a96646a047c8c10c1083b82010f123277db9de857eb10b7d20e83580d840998",
			"acquired_at": "2026-11-07T02:05:13.737818Z", "revision": "Williams Red Parts Catalog 16-9190-B, printed 3-24",
			"locator": "R13190 complete right-ramp exploded assembly; https://www.planetarypinball.com/reference/partsmanuals/WMS_Parts_Red_16-9190-B/files/assets/mobile/page0272_i2.jpg. Four mini-domes with separate receptacles, bulbs and sockets. This is the ramp fixture count, not the full C-bank count.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; Planetary Pinball publisher scan",
			"excerpts": [{
				"id": "excerpt.whirlwind.ramp-dome-parts", "locator": "Printed 3-24 complete lamp-fixture labels and quantities on R13190",
				"path": "evidence/excerpts/williams.whirlwind.1990/ramp-dome-parts.md",
				"sha256": "9b005a89744880fe834a1cae08d4fe66534fa0e31379cb41500020e1a841cb7d",
				"image": "evidence/excerpts/williams.whirlwind.1990/ramp-dome-parts.webp",
				"image_sha256": "8d4294c35a8524d478653ea68f0c84ae9ff9a34f436fc94fe028e56e40a8bd80",
				"image_derivation": "page0272_i2-wrapper.pdf page 1, crop box 0.545,0.455,0.9,0.714, scanned page rendered at its native resolution (embedded image xref 3, 1050px across 10.94in), rendered at 96 dpi, grayscale, 373x353 WebP quality 65",
				"method": "manual", "transcribed_by": "repository curator, complete native exploded drawing visually checked", "reviewed": True,
			}],
		},
		{
			"id": REAR_PHOTO_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/primary-red-parts/physical-board-original.jpg",
			"sha256": "e6892411527eb8a56c0b8b747ccb00113bf80eb4ee9ee44146ca20f64fd895ea",
			"acquired_at": "2026-11-07T00:01:46.584758Z", "revision": "2017 repair photograph",
			"locator": "Andrew Burch, Whirlwind Repair & Service Log 1, https://www.enteryourinitials.com/2017/03/07/whirlwind-repair-service-log-1/; exact 600x450 image http://www.enteryourinitials.com/images/whirlwind/whirlwind_rear_storm_lamp_board_dirty.jpg. All ten LMP designators match the factory diagram, including partly clipped LMP10 GI at the left edge and the missing LMP8 GI twist socket.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Andrew Burch / EnterYourInitials",
			"excerpts": [{
				"id": "excerpt.whirlwind.rear-panel-physical-labels", "locator": "Native photo LMP1-LMP10 label/size correspondence table",
				"path": "evidence/excerpts/williams.whirlwind.1990/rear-panel-lamp-assembly.md",
				"sha256": "874c1378687b0697f68706073d8c818aa5c5481231cc7e30cb4423dec2975321",
				"method": "manual", "transcribed_by": "repository curator, native photograph visually checked against factory elevation", "reviewed": True,
			}],
		},
		{
			"id": REAR_PLACEMENT_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-rear-panel-projection.json",
			"revision": "2026-11-07", "sha256": REAR_PLACEMENT_SHA256,
			"locator": "D13356 ten physical sockets projected onto their own front plastic plane: registered factory elevation, actual four PCB mounts, independently masked plastic artwork, full-board edge/header registration, second assembled PCB/plastic elevation with five withheld flasher bases, and separately mounted stock panel-plane check. Raw pixels, transforms, model world bounds, all holdouts, uncertainty and immutable external reproduction snapshots in seed and portable excerpt. Does not assert PCB depth or emitter Z.",
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams factory drawing; Andrew Burch/EnterYourInitials and PantherCityPins/Pinside photographs; Bigus table contributors; repository curator physical inspection and projection review",
			"excerpts": [{
				"id": "excerpt.whirlwind.rear-panel-placement", "locator": "Complete ten-socket projected inventory, exact photographs/hashes, four-post registration and independent assembled/mounted checks",
				"path": "evidence/excerpts/williams.whirlwind.1990/rear-panel-placement.md",
				"sha256": "5296ca37ecb0adab9967dcc69711acc2f9d5a1686ca85f1974a750215eefb5ca",
				"method": "manual", "transcribed_by": "repository curator, physical originals and independent registration checks inspected; projection limitations explicitly retained", "reviewed": True,
			}],
		},
		{
			"id": MATRIX_BULB_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-matrix-bulbs.json",
			"revision": "2026-11-07", "sha256": MATRIX_BULB_SHA256,
			"locator": "Complete 57 playfield matrix-bulb inventory: exact original bulb-configured objects, six actual Bigus jet bulbs, two separately script-bound 4K cellar glass meshes and physical stock socket correspondence. Twelve withheld PCB axes check model location with disclosed height parallax; occluded sites are not claimed as directly measured. Original colored cellar covers and 4K insert/glow helpers are not bulb authorities.",
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams factory construction; original/Bigus/Flupper table contributors; jef4130 original stock photographs; repository curator physical inspection and exact geometry review",
			"excerpts": [{
				"id": "excerpt.whirlwind.matrix-bulbs", "locator": "57 physical lamp inventory, exact own-bulb bounds and bindings, photo URLs/hashes and physical socket checks",
				"path": "evidence/excerpts/williams.whirlwind.1990/matrix-bulbs.md",
				"sha256": "3637e486af83aec290f48d713b467890c2ae6009bd7e3a21f41a2de5655cbaca",
				"method": "manual", "transcribed_by": "repository curator, actual lamp/mesh objects, script bindings and physical originals inspected", "reviewed": True,
			}],
		},
		{
			"id": HIDDEN_BULB_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-hidden-bulbs.json",
			"revision": "2026-11-07", "sha256": HIDDEN_BULB_SHA256,
			"locator": "Actual Million/Million Plus glass bodies, public 28/32 second emitters: two independently inspected native views per bulb, physical holder/insert identity, separate stock 08C BLK-GRY wiring, and reproduced constrained two-camera normal projections. Added forward/outer wood controls enclose both targets; positive convex-combination certificates reproduce no-extrapolation. All native URLs/hashes, reads, camera assumptions, rejected variants and conservative 0.015 normalized uncertainty retained. Not insert-art centers or exact filaments/Z.",
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "Williams factory construction; jef4130 Google Photos stock photographs; SimplePin/Pinside exposed replacement-playfield photographs; repository curator physical inspection and projection review",
			"excerpts": [{
				"id": "excerpt.whirlwind.hidden-flasher-placement", "locator": "Two physical single-globe measurements, full bounded control sets, camera sensitivity, identity and exact native-photo URLs/hashes/regions",
				"path": "evidence/excerpts/williams.whirlwind.1990/hidden-flasher-placement.md",
				"sha256": "12b254bd19424ab01375024f31ed1342549605eafbd2e5c634915a717c722d98",
				"method": "manual", "transcribed_by": "repository curator, native glass/holders and matched wood openings inspected; both bounded calculations reproduced", "reviewed": True,
			}],
		},
		{
			"id": REAR_GI_BRANCH_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/web/backplastic-gi.page.json",
			"sha256": "8852f682a1595c33507a40da69c8a8db67d670b28edd725c11d3514bcf7d1de5",
			"acquired_at": "2026-11-06T20:58:02.771703Z", "revision": "Pinside actual circuit trace and successful repair, posts 41/44",
			"locator": "https://pinside.com/pinball/forum/topic/whirlwind-backplastic-gi-not-turning-on posts 41 jhanley and 44 Pmaino. Traced panel GI parallel with rear playfield GI; repaired disconnected purple/white-purple inline pair restored panel. Factory power wiring independently identifies this as output 11; owner four-bayonet prose does not establish a complete inventory.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "jhanley and Pmaino, Pinside; repository curator factual synthesis with factory power wiring",
			"excerpts": [{
				"id": "excerpt.whirlwind.rear-panel-gi-branch", "locator": "Posts 41/44 physical trace and repair, qualified by the factory VIO/WHT-VIO branch",
				"path": "evidence/excerpts/williams.whirlwind.1990/rear-panel-gi-branch.md",
				"sha256": "db3ed5fa98f47dbcfd51c7d774dab7ef02d808d11bbd3ca15c6af626a02b5196",
				"method": "manual", "transcribed_by": "repository curator, complete retained thread read and factual observations checked", "reviewed": True,
			}],
		},
		{
			"id": HANDBOOK_SOURCE, "kind": "manual",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-handbook/Whirlwind_Operators_Handbook.pdf",
			"sha256": "b1934cd063d7593a7d912f7100a41b43451d4fae8e51890f6850760f794f6905",
			"acquired_at": "2026-11-07T00:10:40.801860Z", "revision": "16-574-103, December 1989",
			"locator": "Operator's Handbook PDF 8/printed 8 complete Solenoids/Flashers Table; https://arcarc.xmission.com/Pinball/PDF%20Pinball%20Williams%20%281979-2000%29/Whirlwind/Whirlwind%20Operators%20Handbook.pdf. Rows 23/25/26 explicitly specify 2/1/2 #906 rear-panel bulbs. Native 600 dpi table visually read, rotated 270CCW. Other early table differences preserved, not substituted for operations/construction authority.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.; Arcade Archive scan",
			"excerpts": [{
				"id": "excerpt.whirlwind.handbook-solenoids", "locator": "PDF 8/printed 8 complete table and all five numbered notes",
				"path": "evidence/excerpts/williams.whirlwind.1990/handbook-solenoids.md",
				"sha256": "33631a74d17dc94083658c8f75a5398e1124c4c43f81c0fdc98f5a8315b6b6da",
				"method": "manual", "transcribed_by": "repository curator, complete native table visually checked independently of the earlier count", "reviewed": True,
			}],
		},
		{
			"id": GI_PHOTO_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-gi-ocd/official-install.html",
			"sha256": "9e2fc33553abb79326e468172120c5b3a88165f14a0aa8fe7e0636de8a2d2510",
			"acquired_at": "2026-11-06T21:50:02Z", "revision": "2017 installation; 2026-11-06 visual census",
			"locator": "Harold Toler's official GI OCD Whirlwind installation, https://ledocd.com/install_sys11_gi_r2.html, steps 2-12; before-modification 2048x1152 backbox photo, native socket centers in portable excerpt. Socket counts observed; 17 constant /18 controlled split synthesized with factory relay routing. Playfield inventory is established separately by GI_INVENTORY_SOURCE.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Harold Toler / LED OCD; native photograph by herg; repository curator visual census",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-physical-evidence", "locator": "Before-modification backbox original and install steps 3/10/11; factory PDF 106 power wiring",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-physical-evidence.md",
				"sha256": "4513e8c5a7350c4508c32bb71b8f0bb1364a90865ca3f6cff29cd873fd9d278e",
				"method": "manual", "transcribed_by": "repository curator, original photo and bare-wire paths visually checked", "reviewed": True,
			}],
		},
		{
			"id": GI_BLINKER_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-blinkers/owner-backbox.jpg",
			"sha256": "e7a264dac3bb7ea7b7a6c980c472a30cf53b85f547f0b1c1034ef96711311bf8",
			"acquired_at": "2026-11-06T22:47:27Z", "revision": "Pinside owner photograph, post 3; 2026-11-07 visual correspondence review",
			"locator": "EEE, https://pinside.com/pinball/forum/topic/need-help-with-location-of-whirlwind-flashers-in-backbox post 3; post 4 identifies #455 bulbs. Original https://o.pinside.com/b/a7/20/ba72059ed81e316c2495754241ac842667cab0a7.jpg, 2560x1536. Six large globes independently matched to the installer photo's controlled lower strings using nine ordinary socket controls and six withheld checks; exact reads and transform retained in parent-blinkers/front-to-back-registration.json. Portable excerpt records matches and limits.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "EEE, Pinside; repository curator visual correspondence and bare-wire review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-blinkers", "locator": "Six autonomous blinkers subsection, owner front photo matched to installer rear photo",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-physical-evidence.md",
				"sha256": "4513e8c5a7350c4508c32bb71b8f0bb1364a90865ca3f6cff29cd873fd9d278e",
				"method": "manual", "transcribed_by": "repository curator, both originals and wire strings visually checked", "reviewed": True,
			}],
		},
		{
			"id": GI_STOCK_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/primary-recent-club/post6085-lamps.jpeg",
			"sha256": "4df426424368b1c7ef15e57ea7c73707cda1f0d1ecd7f75eed145e582bf8b1f7",
			"acquired_at": "2026-11-07T01:21:47.3867821Z", "revision": "Pinside Whirlwind Club post 6085; 2026-11-07 physical inspection",
			"locator": "LWB250, https://pinside.com/pinball/forum/topic/whirlwind-club-members-only/page/122#post-9282237. Original https://o.pinside.com/4/d0/0a/4d00ac3c693443ae773123ee835e14adcfd6c260.jpeg, 1536x2048. Native box 450,900,900,1350 shows two distinct #47 bulbs in the three-bank island. Original worn playfield and adjacent hardware establish region. Stock post 064-05 independently corroborates two socket barrels. Existence evidence only; no numbered branch, coordinates or complete GI quantity inferred.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "LWB250 / Pinside; repository curator physical socket review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-stock-sockets", "locator": "Post 6085 original photograph, adjacent three-bank sockets; stock teardown corroboration",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-stock-sockets.md",
				"sha256": "59a8d43565f5ce809303a0b62d3fe0b47a2197fafb868ba0c33f36602ead8d61",
				"method": "manual", "transcribed_by": "repository curator, independently inspected the original photo and native crop", "reviewed": True,
			}],
		},
		{
			"id": GI_INVENTORY_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-gi-inventory.json",
			"sha256": GI_INVENTORY_SHA256, "revision": "2026-11-07",
			"locator": "Twenty-one original-stock playfield bayonets: exact Bigus bulb meshes reconciled with independent 4K UV socket-mouth reads, eighteen non-GI controls and twenty-one withheld stock-wood apertures. Both bank coordinates use the separate factory measurement. Original jef4130 photographs and exact source URLs/hashes/regions in the portable excerpt; VIO/WHT-VIO feeds, factory routing and regional switched states establish upper 10/lower 11. Rear-panel five and backbox controlled 18 are counted separately.",
			"license": "NOASSERTION", "rights": "NOASSERTION",
			"attribution": "jef4130 physical photographs; Bigus and Flupper table contributors; Williams factory wiring; repository curator independent physical and geometry review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-playfield-inventory", "locator": "Complete physical inventory, original-photo URLs/hashes/native regions, twenty-one coordinate authorities and disclosed renderer defects",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-playfield-inventory.md",
				"sha256": "47bfdaae3023ba0b0138027ba9d4115f7e7fa31e7d396062b2a81292c39c9591",
				"method": "manual", "transcribed_by": "repository curator, native photographs, exact bulb objects and independent socket checks visually inspected", "reviewed": True,
			}],
		},
		{
			"id": GI_BANK_SOURCE, "kind": "human_review",
			"uri": "tools/seeds/williams/whirlwind-1990-gi-bank-callouts.json",
			"revision": "2026-11-07", "sha256": GI_BANK_SEED_SHA256,
			"locator": "Factory PDF 83/printed 73, native 2473x3273 hi-083.png: two stock-confirmed three-bank GI socket apertures at 1712,1033 and 1725,1052. Nine independently read mechanism controls reconcile the drawing to exact retained VPX objects. Regional measurement only; GI_INVENTORY_SOURCE separately establishes lower 16 membership and full quantities.",
			"license": "NOASSERTION", "attribution": "Williams factory drawing; repository curator native measurement and physical-photo reconciliation",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-bank-placement", "locator": "Two apertures, native source pixels, nine-control affine fit and regional normalized positions",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-bank-placement.md",
				"sha256": "8bad97cf0a845b38756cffeedf1cc4175e5a8a0deb623808911a55cf6336d904",
				"image": "evidence/excerpts/williams.whirlwind.1990/gi-bank-placement.webp",
				"image_sha256": "34df6f5c3236c95553d2f7431bcf71a7fc3e0179442f6f1fcbe3f7fb0b30406d",
				"image_derivation": "Native hi-083.png SHA256 74d2e9fd5823471dc42a45efca2cc83aa1ff9306b7de1e1465940c8fb2cec70a, box (1630,925,1800,1120), no resize, grayscale WebP quality 70, 170x195, 6950 bytes",
				"method": "manual", "transcribed_by": "repository curator, independently read and visually checked against native drawing and stock photographs", "reviewed": True,
			}],
		},
		{
			"id": GI_CURVE_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-aussie7512/selected-originals/Whirlwind 116.JPG",
			"sha256": "af58c1ad57dae8dc98e6020fc82da1d963eb213cfc2ea196c24c23895c2d72bd",
			"acquired_at": "2026-11-07T01:55:31.696559Z", "revision": "2011 original-playfield restoration photograph; 2026-11-07 physical inspection",
			"locator": "Strangeways, https://aussiepinball.com.au/index.php?topic=7512.0; published original http://www.aussiepinball.com/strangeways/restores/Whirlwind/Whirlwind%20116.JPG. Native 979x734 box 135,40,355,175 shows three separate fitted glass bulbs and a wire-gate leg entering the fourth round opening. Bare 234 corroborates the four wood mouths; no branch or normalized coordinate inferred.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Strangeways / Aussie Pinball; repository curator independent physical review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-left-curve", "locator": "Original 116 three glass bulbs and fourth wire opening, cross-checked against stripped 234",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-left-curve.md",
				"sha256": "dac7916935b2fb008e305dcce3412b649a3dee216dba58a89c8c9edb0b3ddeb6",
				"method": "manual", "transcribed_by": "repository curator, native original and tight crop visually checked", "reviewed": True,
			}],
		},
		{
			"id": GI_CORNER_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-gi-voltage-and-rescue/rescue-selected-2.jpeg",
			"sha256": "820b37686b040ecd691b22c021ebf53e3d9b3bd0b5c8b4092e5894c8403a8a2f",
			"acquired_at": "2026-11-07T02:56:58.281317Z", "revision": "Original-playfield rescue, post 4 third photograph; 2026-11-07 physical inspection",
			"locator": "PantherCityPins, https://pinside.com/pinball/forum/topic/rescuing-a-whirlwind post 4. Original https://o.pinside.com/9/ff/41/9ff419bb0709e4b77b2e29359f382a39b9b72af7.jpeg, 1536x2048. Native box 410,730,1180,1740 shows three separate fitted glass bulbs outside the rear-right curved guide, distinct from threaded posts and elongated switch slots. Regional physical inventory only; no numbered branch or normalized coordinate inferred.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "PantherCityPins / Pinside; repository curator independent physical review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-right-rear", "locator": "Post 4 third original, three glass bulbs and separate threaded posts",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-right-rear.md",
				"sha256": "fc166ee0ef65e9ec9c403822db11008fc97c87665ff8eef03220fb4b79ecd746",
				"method": "manual", "transcribed_by": "repository curator, complete original and native crop visually checked", "reviewed": True,
			}],
		},
		{
			"id": GI_WIRE_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/whirlwind-20261106/parent-recent-club/stock-and-stage-originals/post6083-04.jpg",
			"sha256": "f9e6a5ecc0bc5bd6764157f334b4a1c7322a37a040baf2d75462a07b7f4625fc",
			"acquired_at": "2026-11-07T01:26:07.429655Z", "revision": "Stock playfield, Whirlwind Club post 6083; 2026-11-07 construction inspection",
			"locator": "LWB250, https://pinside.com/pinball/forum/topic/whirlwind-club-members-only/page/122 post 6083 fifth original. Original https://o.pinside.com/6/54/ab/654abd3ba92e78e54583060a0218b97f4d60bb38.jpeg, 1536x2048. Native box 250,940,480,1190 positively shows switch leads entering an open round wood passage between two slots. Stripped IPDB 2765 photo 25889 independently shows the same bore/slot pattern. Bigus Light67 is a rendering candidate here, not an additional physical GI bulb. No coordinate derived from the correspondence fit.",
			"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "LWB250 / Pinside; Allen Shope / IPDB stripped view; repository curator independent physical review",
			"excerpts": [{
				"id": "excerpt.whirlwind.gi-wire-passage", "locator": "Stock 6083 native wire passage and stripped IPDB 25889 bore/slot correspondence",
				"path": "evidence/excerpts/williams.whirlwind.1990/gi-wire-passage.md",
				"sha256": "776dfd744c6a2312d4d81a9743093a984e03d8ae924a223009afd1011b0c7efb",
				"method": "manual", "transcribed_by": "repository curator, native construction crop visually checked against the stripped playfield", "reviewed": True,
			}],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/whirlwind-1990/extracted-vpxtool/",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": f"Retained vpxtool git:v0.33.3 extraction, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, from table SHA-256 {TABLE_SHA256}. Full sorted POSIX path/size/SHA-256 manifest at {EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}; canonical JSON SHA-256 {EXTRACTION_MANIFEST_SHA256}. Bounds {TABLE_BOUNDS}. verify_extraction_manifest recomputes every file and pins count, total bytes and canonical digest.",
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
				roles=[role], normally_closed=False,
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
					"Board), confirming opto interrupter construction. The retained script initializes dtT/dtL with "
					"switches 26/27-29; core.vbs cvpmDropTarget.Hit writes True when a target drops and SolDropUp "
					"writes False on reset. System 11 pia4a_r reads core_getSwCol without complementing it, and "
					"whirlGameData has no inversion mask. Thus the active public level 1 is a matrix closure and "
					"the inactive matrix contact rests open (normally_closed=false). This derives the matrix "
					"contact from the read path and working runtime semantics, not from beam condition."
				)
			else:
				notes += (
					" The switch-locations parts list marks this position with an unnumbered Sol./Switch entry and the "
					"** footnote 'Optotransistor on Backbox Interconnect Bd'; the physical cabinet flipper button "
					"(SW-10A-48 left / SW-1010A-13 right) has no matrix address of its own and switches coil power "
					"directly through the hardware relay/fuse circuit, with no independent CPU coil drive. The factory "
					"Power Wiring Diagram (PDF 106/printed 96) shows the input LED of "
					f"{'2U2' if address == 58 else '2U3'} on a resistor-fed sensing branch between the flipper supply "
					f"and the switched lower-coil return ({'BLU-GRY left' if address == 58 else 'BLU-VIO right'}), "
					"in parallel with the coil load. Its output transistor is optically isolated on the matrix side, "
					"allowing the CPU to sense lower-flipper activation here. The lower-coil return runs directly "
					"via 2P8/2J8 to the cabinet button; the linked upper-right BLK-YEL return is not monitored by 2U3. "
					"The normally-open button removes the return path at rest, so the opto is off and the matrix "
					"contact rests open. Pinned PinMAME declares FLIP_SWNO(58,57) (58=left, 57=right). "
					"A consumer cannot drive this address: with keyboard handling off (the LibPinMAME default, and "
					"the retained script sets HandleKeyboard=0) core_updateSw rewrites it on every update from "
					f"PinMAME's flipper column, public {84 if address == 58 else 82} (the "
					f"{'left' if address == 58 else 'right'} cabinet button, "
					f"{'CORE_SWLLFLIPBUTBIT' if address == 58 else 'CORE_SWLRFLIPBUTBIT'}). The ROM therefore reads "
					"the button state exactly as the host writes it there, 1 while the button is pressed, which is "
					"what the retained script's S11.VBS flipper keys produce. The retained script also writes "
					f"Controller.Switch({address}) directly from the flipper key (script.vbs lines "
					f"{'1612/1616 and 1628/1632' if address == 58 else '1613/1615 and 1629/1631'}); those writes are "
					"overwritten on the next update and have no effect, a defect of the table rather than a fact "
					"about the machine."
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
		if not unused:
			extra["normally_closed"] = False
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
		if address in {26, 27, 28, 29}:
			refs += (VPM_LIBRARY_SOURCE, DROP_LEVELS_SOURCE)
		if not unused and address != 2:
			refs += (SERVICE_SOURCE,)
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	items.extend(flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(58,57)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE),
		button_normally_closed=False,
		button_notes={
			side: (
				f"The retained known-working script drives it: Table1_KeyDown/Table1_KeyUp hand the {side} flipper key to "
				f"KeyDownHandler/KeyUpHandler, which core.vbs routes to S11.VBS vpmKeyDown/vpmKeyUp, and those set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). "
				f"The physical counterpart is the {side} cabinet flipper button, which directly switches coil power "
				"through the hardware circuit with no independent CPU coil drive. Lower-flipper activation is sensed "
				f"at matrix {58 if side == 'left' else 57} by the optically isolated output transistor of "
				f"{'2U2' if side == 'left' else '2U3'}; its input LED is on a resistor-fed branch between the flipper "
				f"supply and switched lower-coil return ({'BLU-GRY' if side == 'left' else 'BLU-VIO'}), in parallel "
				"with the coil load. The lower-coil return runs directly via 2P8/2J8 to the button. "
				"The linked upper-right BLK-YEL return is not monitored by 2U3. "
				"The factory Power Wiring Diagram (PDF 106/printed 96) draws each cabinet button return contact "
				"open at rest, removing the return path and leaving the opto off, establishing normally_closed=false "
				"independently of public host-input levels."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(),
		unused_note_refs=(VPM_LIBRARY_SOURCE,),
	))

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
# Physical C-bank bulbs are drawn on printed 73; sound-overlay bulbs are on the
# rear playfield back panel (printed 42/52). BGArr is an additional renderer proxy.
FLASHER_ADDRESSES = {25, 26, 27, 28, 29, 30, 31, 32, 37, 39, 40}

# Five physical dome-base centers from the supplemental table, normalized by
# its own 952x2164 bounds. Factory-symbol measurements supply the other six.
FLASHER_DOME_OBJECTS = {25: "Flasherbase9", 27: "Flasherbase4", 28: "Flasherbase3", 29: "Flasherbase2", 30: "Flasherbase1"}
FLASHER_DOME_POSITIONS = {
	25: (0.881314, 0.619084), 27: (0.636002, 0.122058),
	28: (0.297845, 0.177921), 29: (0.103789, 0.321688), 30: (0.158411, 0.565065),
}


def flasher_seed() -> dict[str, Any]:
	if _file_sha256(FLASHER_SEED_PATH) != FLASHER_SEED_SHA256:
		raise RuntimeError("Whirlwind factory flasher measurement seed changed")
	return load_json(FLASHER_SEED_PATH)


def gi_bank_seed() -> dict[str, Any]:
	if _file_sha256(GI_BANK_SEED_PATH) != GI_BANK_SEED_SHA256:
		raise RuntimeError("Whirlwind GI bank measurement seed changed")
	seed = load_json(GI_BANK_SEED_PATH)
	for identifier in seed["measurements"]:
		drawing_callouts.measured(seed, identifier)
	return seed


def gi_inventory() -> dict[str, Any]:
	if _file_sha256(GI_INVENTORY_PATH) != GI_INVENTORY_SHA256:
		raise RuntimeError("Whirlwind physical GI inventory changed")
	return load_json(GI_INVENTORY_PATH)


def rear_panel_seed() -> dict[str, Any]:
	if _file_sha256(REAR_PLACEMENT_PATH) != REAR_PLACEMENT_SHA256:
		raise RuntimeError("Whirlwind rear panel projection seed changed")
	seed = load_json(REAR_PLACEMENT_PATH)
	xs = [p[0] for p in seed["factory_mount_reads"]]
	ys = seed["mount_world_x"]
	xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
	slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / sum((x - xbar) ** 2 for x in xs)
	intercept = ybar - slope * xbar
	for actual, expected in zip((slope, intercept), seed["fit_world_x"]):
		if abs(actual - expected) > 1e-9:
			raise RuntimeError("Whirlwind rear panel mount fit does not reproduce")
	for row in seed["sockets"]:
		x = round((slope * row["factory_upright_pixels"][0] + intercept) / seed["bounds"][0], 3)
		y = round(seed["panel_front_y_vpu"] / seed["bounds"][1], 6)
		if [x, y] != row["normalized_xy"]:
			raise RuntimeError("Whirlwind rear panel socket projection does not reproduce")
	return seed


def rear_panel_spatial(identifier: str, address: int) -> dict[str, Any]:
	placements = []
	for row in rear_panel_seed()["sockets"]:
		if row["address"] == address:
			x, y = row["normalized_xy"]
			placements.append({"id": f"{identifier}.{row['id']}", "role": "emitter", "space": "playfield", "x": x, "y": y,
				"provenance": provenance(REAR_PLACEMENT_SOURCE, REAR_ASSEMBLY_SOURCE, REAR_PHOTO_SOURCE, BIGUS_SOURCE)})
	return {"status": "validated", "placements": placements}


def matrix_bulbs() -> dict[str, Any]:
	if _file_sha256(MATRIX_BULB_PATH) != MATRIX_BULB_SHA256:
		raise RuntimeError("Whirlwind matrix bulb inventory changed")
	seed = load_json(MATRIX_BULB_PATH)
	for row in seed["cellar_bulbs"]:
		xy = [round((row["bounds_min"][i] + row["bounds_max"][i]) / 2 / seed["cellar_bounds"][i], 6) for i in (0, 1)]
		if xy != row["normalized_xy"]:
			raise RuntimeError("Whirlwind cellar bulb mesh center does not reproduce")
	return seed


def hidden_bulbs() -> dict[str, Any]:
	if _file_sha256(HIDDEN_BULB_PATH) != HIDDEN_BULB_SHA256:
		raise RuntimeError("Whirlwind hidden bulb projection seed changed")
	seed = load_json(HIDDEN_BULB_PATH)
	for row in seed["placements"]:
		certificate = row["hull_certificate"]
		weights = certificate["weights"]
		if min(weights) < 0 or abs(sum(weights) - 1) > 1e-9:
			raise RuntimeError("Whirlwind hidden bulb control-hull certificate is invalid")
		for axis in (0, 1):
			world = sum(weight * row["controls_world_xy"][index][axis] for weight, index in zip(weights, certificate["indices"]))
			if abs(world / row["bounds"][axis] - row["normalized_xy"][axis]) > 1e-9:
				raise RuntimeError("Whirlwind hidden bulb control-hull certificate does not reproduce")
	return seed


def gi_spatial(identifier: str, branch: str) -> dict[str, Any]:
	placements = []
	for row in gi_inventory()["placements"]:
		if row["branch"] != branch:
			continue
		x, y = row["normalized_xy"]
		refs = [GI_INVENTORY_SOURCE, MANUAL_SOURCE]
		if "measurement" in row:
			x, y = drawing_callouts.measured(gi_bank_seed(), row["measurement"])
			refs.append(GI_BANK_SOURCE)
		else:
			refs.append(BIGUS_SOURCE)
		placements.append({"id": f"{identifier}.{row['id']}", "role": "emitter", "space": "playfield", "x": x, "y": y,
			"provenance": provenance(*refs)})
	if branch == "upper":
		placements.extend(rear_panel_spatial(identifier, 11)["placements"])
	return {"status": "validated", "placements": placements}


def flasher_spatials() -> dict[int, dict[str, Any]]:
	seed = flasher_seed()
	hidden = {row["address"]: row for row in hidden_bulbs()["placements"]}
	result = {}
	for address, label in SOLENOID_C_LABELS.items():
		identifier = output_id(label)
		positions = [FLASHER_DOME_POSITIONS[address]] if address in FLASHER_DOME_POSITIONS else []
		for pid, measurement in seed["measurements"].items():
			if measurement["device"] == identifier:
				positions.append(drawing_callouts.measured(seed, pid))
		if address in hidden:
			positions.append(tuple(hidden[address]["normalized_xy"]))
		spatial = located(identifier, "emitter", positions, MANUAL_SOURCE, FLASHER_DRAWING_SOURCE, FLASHER_TABLE_SOURCE)
		if address in hidden:
			spatial["placements"][-1]["provenance"] = provenance(HIDDEN_BULB_SOURCE, MANUAL_SOURCE, FLASHER_TABLE_SOURCE)
		result[address] = spatial
	return result


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
	flasher_geometry = flasher_spatials()

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
			refs += (GI_PHOTO_SOURCE, GI_STOCK_SOURCE, GI_BANK_SOURCE, GI_CURVE_SOURCE, GI_CORNER_SOURCE, GI_INVENTORY_SOURCE, BIGUS_SOURCE, FLASHER_TABLE_SOURCE, REAR_ASSEMBLY_SOURCE, REAR_PHOTO_SOURCE, REAR_GI_BRANCH_SOURCE, REAR_PLACEMENT_SOURCE)
			physical["notes"] += (
				" Pinned PinMAME's whirl_ MACHINE_INIT block names this address 'Upper Playfield GI output' "
				"(CORE_MODOUT_BULB_44_6_3V_AC_REV), confirmed by the manual's own GI relay board page (printed 53) and "
				"the retained script's SolUpperGI handler. The retained script's UpperGI light collection is empty "
				"(zero bound playfield objects) -- a completeness gap in this retained table, not evidence the "
				"physical machine lacks an upper-playfield GI bank. The power schematic (printed 96) routes "
				"VIO / WHT-VIO via 2J9-5/1 to this relay. The factory D13356 elevation and original silkscreened "
				"board corroborate five rear-panel GI positions, LMP6-LMP10; an actual traced purple/white-purple "
				"inline connection and successful repair establish their parallel membership in this branch. "
				"Original-stock photographs expose ten upper-playfield bayonets: two deep left, three left-curve, "
				"three rear-right and two inner-right. Actual VIO/WHT-VIO feeds, local links, factory routing, regional "
				"voltage observations and independently authored 4K switched socket depictions reconcile this inventory. "
				"Quantity 15 includes those ten and five D13356 GI lamps. The ten playfield positions use exact Bigus "
				"bulb meshes cross-checked against 4K socket mouths and independently read stock wood apertures. "
				"The five upright rear-panel GI bulbs are separately projected onto their own corroborated front "
				"plastic plane, with factory/physical PCB registration and independent assembled/mounted checks; "
				"this does not assert actual PCB depth or filament height. "
				"Both three-bank bayonets belong to lower 16: Bigus Light81's upper membership is a renderer defect. "
				"The left white curve's fourth opening carries a wire-gate leg and is not another lamp."
			)
			physical["quantity"] = 15
			physical["notes"] += " Value 1 on this public address commands GI darkness and 0 commands light in SolUpperGI; this is a relay command, not direct lamp intensity."
			extra["roles"] = ["gi.upper-playfield"]
			kind = "gi"
			extra["spatial"] = gi_spatial(identifier, "upper")
		elif address == 12:
			physical["notes"] += " A/C Select Relay (mounted on the Aux Power Driver Board, D-12247, in the backbox); multiplexes 16 controlled/switched solenoids between circuit A and circuit C. See controllers/pinmame/system-11.json for the full mux mechanism."
			extra["roles"] = ["internal.ac-select-relay"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
			kind = "relay"
		elif address == 16:
			refs += (GI_PHOTO_SOURCE, GI_BLINKER_SOURCE, GI_STOCK_SOURCE, GI_BANK_SOURCE, GI_WIRE_SOURCE, GI_INVENTORY_SOURCE, BIGUS_SOURCE, FLASHER_TABLE_SOURCE)
			physical["notes"] += (
				" Pinned PinMAME's whirl_ MACHINE_INIT block names this address 'Backbox and Lower playfield GI "
				"output'. The manual's own GI relay board page (printed 53) confirms this single address energizes "
				"TWO physically separate relays simultaneously: the playfield-side C-11902-1 board (lower playfield "
				"GI) and the separate backbox C-11998-1 board (backbox/backglass GI). The retained script's "
				"SolLowerGI handler drives both the LowerGI light collection (one member, Light1) and the near-"
				"full-table Flasher4 overlay together. That single light and overlay simplify the actual inventory. The power schematic "
				"(printed 96) routes YEL / WHT-YEL via 2J9-6/7 to the lower-playfield relay; the separate "
				"2J10-10/9 coin-door branch is outside it. Backbox GI also includes an always-on portion. "
				"The before-modification installer photograph contains 35 backbox sockets in three traced portions: "
				"17 upper sockets remain powered, while 6 left and 12 right sockets are relay controlled, so only 18 "
				"backbox sockets belong to this output. An independent owner photo's six large-globe #455 blinkers "
				"match sockets within those controlled 18 (two left, four right); the other 12 are ordinary lamps. "
				"The blinkers operate autonomously while supplied and are not six extra CPU-controlled flashers. "
				"Eleven original-stock playfield bayonets belong to lower 16: both three-bank, one left-points, two "
				"right-points, one per sling and two per return island. Physical bodies, local wiring, factory routing "
				"and 4K lower-only socket depictions reconcile the inventory; renderer collection size is not the count. "
				"Quantity 29 includes eleven playfield plus eighteen backbox bulbs. Spatial places only the eleven "
				"playfield emitters; the eighteen backbox emitters are cabinet/service locations and need no invented "
				"playfield points. Both bank positions use the independent factory measurement; the other nine use "
				"actual Bigus bulb meshes checked against 4K and stock wood. Light66 duplicates the sole left-sling "
				"bulb, and Light81 incorrectly groups the rear bank bulb as upper."
				" The supplemental Bigus LowerGI member Light67 lies at a round switch-wire passage. A stock native "
				"photograph positively shows green and pale leads entering that open bore; its bulb flag does not "
				"establish another physical socket."
			)
			physical["quantity"] = 29
			physical["notes"] += " Value 1 on this public address commands GI darkness and 0 commands light in SolLowerGI; this is a relay command, not direct lamp intensity."
			extra["roles"] = ["gi.lower-playfield-and-backbox"]
			extra["spatial"] = gi_spatial(identifier, "lower")
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
				"verbatim, to solenoid 10's row. The manual's separate Solenoids/Flashers location list and drawing "
				"(printed 73) resolve item 21 as 'Lower Top Jet Bumper', the bottom bumper of the upper cluster, "
				"matching switch 51 / Bumper3. The canonical label follows that location list; both printed readings "
				"are preserved in "
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
				"flasher with f125-f132 playfield Light effects in UpdateLamps as well as a FlSol backglass/VR "
				"proxy in BGArr. The manual's location drawing (printed 73) establishes playfield bulbs, and "
				"the Solenoid Table's 1p/2p entries establish quantity. These effect-light centers are not socket "
				"coordinates: show_bulb_mesh is false. Physical placements use separately reviewed dome bases "
				"or round factory flashlamp symbols, rather than those render effects."
			)
		if address == 30:
			notes += " The wiring table calls 06C 'R Ramp Bottom Flasher'; the separate location list prints 'Ramp Bottom (L P'fld) Flasher' and draws it on the left, consistent with the retained table. The canonical label follows the construction/location evidence."
		if address in {27, 28, 29, 30}:
			refs += (RAMP_DOME_SOURCE,)
			notes += (
				" This circuit's raised ramp fixture is one of four on R-13190. The factory exploded assembly "
				"specifies 03-8171-9 transparent-red mini-dome, 03-8172-13 clear dome receptacle, "
				"24-8802 #906 bulb and 24-8812 light socket, four of each. That assembly quantity does not "
				"include this circuit's separate below-playfield bulb where fitted."
			)
		extra = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{a_address:02d}C"}],
			"physical": {"quantity": quantity, "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "driver_transistor": SOLENOID_A_DRIVER[a_address],
				"power_connection": SOLENOID_C_PLAYFIELD[address],
			},
			"spatial": flasher_geometry[address],
		}
		if address in {28, 32}:
			refs += (HIDDEN_BULB_SOURCE,)
			extra["physical"]["notes"] += " The separate under-insert Million/Million Plus glass body is placed from two native physical photographs with enclosing, independently matched wood controls and a reproduced two-camera normal projection. Position is rounded to three decimals with conservative 0.015 normalized uncertainty; no exact filament or height is asserted. The factory insert-feature leader alone is excluded as a socket coordinate."
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
			identifier, label, "virtual", address, "used" if address in {23, 45, 46, 47, 48} else "unused",
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
				"drive_wire": SOLENOID_OVERLAY_WIRE[address], "control_connection": SOLENOID_OVERLAY_SOL_J4[address],
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
			refs += (REAR_ASSEMBLY_SOURCE, REAR_PHOTO_SOURCE, HANDBOOK_SOURCE, REAR_PLACEMENT_SOURCE, BIGUS_SOURCE)
			extra["physical"] = {"quantity": REAR_FLASHER_QUANTITIES[address], "notes": notes}
			notes += (
				" The table drives f137/f139/f140 playfield Light effects as well as FlSol backglass proxies. "
				"The manual legend defines bp as Back Panel; printed 42 locates D-13356 at the rear of the "
				"playfield, and printed 52 lists its #906 flashlamps and #555 GI bulbs. The physical flashers "
				"are on that upright rear playfield panel. Renderer backglass proxies are not extra bulbs. "
				"The CPU's 1P21 ribbon is shared upstream; the structured control connection identifies the "
				"individual board output at SOL J4. The Red Parts Catalog printed 5-37 draws five #906 "
				"positions LMP1-LMP5 and five GI positions LMP6-LMP10; the actual original board shows "
				"that complete labelled pattern. This settles the physical rear-panel total at five flashers, "
				"rather than the operations solenoid table's six. The independent operator's handbook "
				"printed 8 explicitly specifies two left, one middle and two right, agreeing with the complete "
				"drawing and physical pattern. Each actual socket is projected onto its own front plastic plane: "
				"factory/PCB/mount registration supplies X, exact Bigus world-mesh front face supplies Y, with "
				"independent header/edge, assembled-board and mounted-stock checks. The projection does not "
				"assert actual socket PCB depth or emitter Z; measured X is rounded to three decimals."
			)
			if address == 37:
				notes += " The operations table's three-left-bulb entry is a quantity erratum; physical quantity 2 follows the corroborated handbook count."
			extra["physical"]["notes"] = notes
			extra["spatial"] = rear_panel_spatial(identifier, address)
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
	37: (0.572691, 0.102691), 38: (0.532656, 0.190552),
	41: (0.713324, 0.374736), 42: (0.735881, 0.335705), 43: (0.612977, 0.345704), 44: (0.513142, 0.321156),
	45: (0.417101, 0.297672), 46: (0.882212, 0.457146), 47: (0.757600, 0.405426), 48: (0.598432, 0.387459),
	49: (0.261348, 0.659187), 50: (0.228056, 0.433808), 51: (0.422232, 0.477915), 52: (0.418910, 0.234930),
	53: (0.679651, 0.308830), 54: (0.804060, 0.350782), 55: (0.874534, 0.341587), 56: (0.842636, 0.538893),
	57: (0.507094, 0.874461), 58: (0.363891, 0.785374), 59: (0.420767, 0.793690), 60: (0.477756, 0.801414),
	61: (0.534746, 0.801142), 62: (0.592707, 0.793401), 63: (0.647747, 0.785388), 64: (0.900559, 0.290056),
}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	cellar_positions = {p["address"]: tuple(p["normalized_xy"]) for p in matrix_bulbs()["cellar_bulbs"]}
	for address in range(2, 9):
		label = BACKGLASS_REEL_LAMPS[address]
		identifier = f"lamp.backglass-reel-{address}"
		items.append(
			_device(
				identifier, label, "lamp", "pinmame.output.lamp", address, "used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
				physical={"quantity": 1, "notes": f"Printed lamp-matrix drive column 1, return row {address}. This is a physical backbox award-indicator bulb. UpdateLamps represents it with FadeRm against the L{address} Reel object; that renderer class does not make the real lamp a mechanical score reel."},
				wiring={"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[1][0], "drive_connection": LAMP_COLUMN_WIRING[1][1], "return_wire": LAMP_ROW_WIRING[address][0], "return_connection": LAMP_ROW_WIRING[address][1], "driver_transistor": f"column driver {LAMP_COLUMN_WIRING[1][2]}; row driver Q{79 + address}"},
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
		if address == 53:
			notes += " The matrix table repeats 'L Return Lane' here (also printed for 49); the separate location list and script-bound l53 identify the left standup at the right ramp. The literal matrix misprint remains in the excerpt."
		if address == 9:
			notes += " The original script omits the lamp 9 binding even though Light.l9 exists. The supplemental Bigus script explicitly binds NfadeL 9,l9, and its center agrees within 0.002 normalized with the original l9 at the factory left-outlane insert. This is an original-table omission, not an absent physical lamp."
		position = cellar_positions[address] if address in cellar_positions else LAMP_POSITIONS[address]
		spatial_refs = (MATRIX_BULB_SOURCE, MANUAL_SOURCE, FLASHER_TABLE_SOURCE) if address in cellar_positions else (MATRIX_BULB_SOURCE, MANUAL_SOURCE, VPX_TABLE_SOURCE)
		if address == 9 or 33 <= address <= 38:
			spatial_refs += (BIGUS_SOURCE,)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
			"physical": {"quantity": 1, "notes": notes},
			"wiring": {
				"board": "System 11B CPU board", "drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
				"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
				"driver_transistor": f"column driver {LAMP_COLUMN_WIRING[column][2]}; row driver Q{79 + row}",
			},
			"spatial": located(identifier, "emitter", [position], *spatial_refs),
		}
		if address in {39, 40}:
			extra["physical"]["notes"] += " Original runtime binding uses image-swap colored cover Primitive.l39/l40 (bulbcover1_red/yellow), whose center is not the bulb. Placement instead uses this lamp's separate 4K BulbLeft/Right glass mesh world-bounds midpoint, bound through CellarLeft/RightNew for 39/40. Its baked primitive origin is not used. The original cover approximation is a consumed-table artifact, not a second physical bulb."
		elif 33 <= address <= 38:
			extra["physical"]["notes"] += " Original center agrees exactly with the corresponding Bigus l33-l38 actual own bulb (show_bulb_mesh=true). Larger bumper glow companions do not add bulbs or displace this center."
		else:
			extra["physical"]["notes"] += " Single physical socket location from the original bulb-configured object, reconciled with factory lamp construction and stock socket/PCB correspondence. Its suppressed mesh does not establish quantity; insert/light-map/bloom helpers are excluded."
		refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, MATRIX_BULB_SOURCE) + ((BIGUS_SOURCE,) if address == 9 or 33 <= address <= 38 else ())
		if address in cellar_positions:
			refs += (FLASHER_TABLE_SOURCE,)
		items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
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
				output_id("Left Upper Jet Bumper"), output_id("Right Upper Jet Bumper"), output_id("Bottom Upper Jet Bumper"),
			],
			["switch.matrix-49", "switch.matrix-50", "switch.matrix-51", "switch.matrix-52", "switch.matrix-53", "switch.matrix-54"],
			"Two clusters of three jet bumpers each: an upper cluster near the top of the playfield (switches 49-51, "
			"solenoids 17/19/21) and a lower cluster nearer the cellar (switches 52-54, solenoids 9/15/10). Each "
			"bumper's coil and switch belong to one assembly. The Playfield Parts table identifies red B-9414-3 "
			"and yellow B-9414-2 jet assemblies, both with B-9415-1 coil/bracket assemblies.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9414-2 / B-9414-3",
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
			"a relay/fuse circuit with no independent CPU coil drive (no public solenoid address corresponds to a real "
			"driver-board output). Backbox Interconnect Board optocouplers 2U2/2U3 sense lower-flipper activation: "
			"their input LEDs are on resistor-fed branches from the flipper supply to the switched lower-coil "
			"returns (BLU-GRY left, BLU-VIO right), in parallel with the coil loads; their optically isolated output "
			"transistors report to the CPU at matrix 58 (left) and 57 (right) for 'Flipper Lane Change'. The lower-coil "
			"returns run directly via 2P8/2J8 to the cabinet buttons; the linked upper-right BLK-YEL return is not "
			"monitored by 2U3. The normally-open buttons remove the return paths at rest, leaving the optos off. "
			"In PinMAME the button state enters at public 82 (right) and "
			"84 (left), which core_updateSw copies into 57/58 and into the synthetic outputs 45-48; a consumer drives "
			"82/84, never 57/58. The retained script's SolRFlipper handler rotates both "
				"RightFlipper (lower) and RightFlipper1 (upper) together. The Power Wiring Diagram (printed 96) "
				"shows two separate right coils and EOS switches wired to the same right cabinet button.",
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
		*flipper_column_relationships(
			flip_swno=FLIP_SWNO, matrix_ids={57: "switch.matrix-57", 58: "switch.matrix-58"}, refs=(CORE_SOURCE,),
		),
	]


def conflicts() -> list[dict[str, Any]]:
	# The former backglass-versus-playfield conflict was a misreading of renderer
	# proxies. Factory construction and the script's playfield bindings settle it.
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


KNOWLEDGE_TEXT = """# Whirlwind (Williams, 1990)

Coverage: **author_ready**. Controller enumeration, target polarity, physical flasher fitment and complete controlled-GI quantities/membership are settled. All 21 playfield bayonets and thirteen C-bank flashlamps are placed. All ten rear-panel bulbs have documented projections onto their own corroborated plastic plane. Matrix bulbs use physical socket correspondence and actual bulb geometry; renderer effects never supply quantities or substitute for physical bulbs.

## Identity and source roles

The five physical-machine drivers are whirl_l3 (LA-3 US/Canadian parent), whirl_l2 (LU-2), and German-localized whirl_g1/g2/g3 (LG-1/2/3). All share whirlGameData/init_whirl and the same physical System 11B hardware. There is no separate physical edition for a language revision.

The retained known-working original VPX script controls runtime bindings and modeled mechanism causality. The Williams operations manual controls physical parts, wiring, quantities and mounting. PinMAME controls emulator topology. Supplemental 4K1.113 geometry supplies five actual Flupper dome bases, checked against the factory drawing; its effects and GI collections do not supply physical quantities. Portable excerpts carry the actual tables and factual observations, not just source hashes. The older external manual-transcription.md is retained unchanged as historical evidence; corrected repository excerpts supersede its errors and omissions.

## System 11 addresses and runtime levels

Switches and lamps use sequential column-major 1-64 addresses: (column-1)*8+row. Column 1 is ordinary matrix wiring, with no separate WPC dedicated-switch namespace. Diagnostics are -7/-6/-5/-4; country selection is DIP 0. Every matrix address is enumerated, including unused positions and the optional center coin chute.

GI uses ordinary solenoid outputs 11 and 16, not a separate GI channel. Output 12 multiplexes the eight physical A/C driver transistors: de-energized selects A-side 1-8; energized selects C-side 25-32. Special coils occupy 17-22. Public 23 is the flipper/switched-solenoid enable state, separate from the manual's board-local item 23. Manual sound-overlay items 23-27 map to public 37-41. The retained whirl_l3 Coil Test displays those item numbers while publishing 37-41, corroborating the offset. Per-game PWM-type comments in the historical PinMAME source are secondary to the actual read/callback paths and the physical table.

Switch 2 is A/C relay feedback, overwritten by the driver's S11_MUXSW2 behavior. It is not a user-controlled ball-tilt input. With keyboard handling off, drive public 82 for the right flipper button and 84 for the left. PinMAME copies those to 57/58; direct writes to 57/58 are overwritten. Public 45-48 are synthetic power/hold indications, not physical CPU-controlled flipper coils. Other flipper-column positions are enumerated as unused for this game's flags.

## Switch construction and target polarity

The switch parts list identifies drop-target optos 26-29 and the separate backbox-interconnect lane-change optos 57/58. Beam condition alone does not establish matrix contact polarity. Pinned operational PinMAME 46e1a01a reads the selected S11 switch column without complement; whirlGameData supplies a zero inversion mask. The known-working cvpmDropTarget Hit path asserts 1 for a dropped target and reset clears 0. Fresh-state ROM Switch Levels traces independently show 26,27,28,29 active at 1 and cleared at 0, with mechanical control 15 before and after. This combined read-path, working-library and ROM evidence establishes normally-open matrix behavior. Portable drop-target-levels and rom-service-tests excerpts identify all raw inputs and hashes. A full scan corroborates 55 distinct host inputs, using 82/84 for 57/58; host readback is not treated as ROM evidence.

## Flashers and physical quantities

The factory solenoid table and printed 73 location drawing specify thirteen C-bank playfield bulbs: quantities 1,1,2,2,2,1,2,2 at 25-32. Sound-overlay outputs 37/39/40 serve D-13356, the upright rear playfield lightning panel (printed 42/52), separate from the insert panel behind the backglass. The operations table prints 3/1/2 bulbs, but the complete Red Parts Catalog elevation printed 5-37 draws only five #906 sockets LMP1-LMP5 plus five GI sockets LMP6-LMP10. The original board repair photo independently shows all ten designators and the same sizes, including the partly clipped LMP10 GI bulb. The independent December 1989 operator's handbook printed 8 explicitly specifies 2/1/2, agreeing with that complete five-flasher pattern and resolving the operations table's left quantity 3 as an erratum. Both complete literal tables are retained portably, including the catalog's erroneous GI(4) quantities, repeated 24-8768 socket/bulb part and nine-lamp index description. Other early handbook differences are not silently substituted for later construction evidence.

The original script drives f125-f132/f137/f139/f140 playfield effects as well as FlSol backglass/VR proxies in BGArr. Those proxies neither relocate physical bulbs nor add bulbs. The earlier supposed mounting conflict came from overlooking the playfield effects and misreading BP as backglass; the manual establishes Back Panel. No physical-source conflict remains on mounting.

Five script-bound Flupper domes use Flasherbase9/4/3/2/1 for 25/27/28/29/30, normalized by the supplemental table's own 952x2164 bounds. Six round factory flashlamp symbols supply six more locations, measured with nine independently read mechanism controls and rounded to three decimals. The seed retains full native pixels, object hashes and the transform. Five dome checks plus six printed bumper labels pass the .07 callout limit, worst leave-one-out .0538. Million/Million+ insert-feature leaders do not locate their sockets and remain excluded from that drawing check.

The two separate under-insert flashlamps are physically visible in retained stock and exposed replacement-playfield photographs. Million 28's second bulb is projected at approximately (.527,.331), Million Plus 32's at (.616,.352), each rounded to three decimals with conservative 0.015 normalized uncertainty. Two-camera fits remove perspective from each actual single glass body using 12/10 enclosing absolute wood controls and independent same-wood matches; added forward/outer openings prevent extrapolation. Positive convex-combination certificates reproduce the control-hull check. Stock black/grey wiring independently identifies 08C. Native URLs/hashes, glass reads, rejected bad T-nut/wide-lens/depth variants, old unbounded comparisons and all camera assumptions are retained in the hidden-bulbs seed/excerpt. These are approximate bulb-body XY projections, not insert centers, exact filaments or asserted Z.

The Red Parts Catalog printed 3-24 independently draws four mini-dome fixtures on R-13190, one each on 27/28/29/30. Each uses a 03-8171-9 red mini-dome, 03-8172-13 clear receptacle, 24-8802 #906 bulb and 24-8812 socket. The portable ramp-dome-parts excerpt retains every lamp-fixture label and quantity. These four ramp bulbs are part of the thirteen C-bank bulbs; they do not replace the separate insert flashers or identify 25's different fixture.

The wiring table calls 30 Right Ramp Bottom; the separate location list says Ramp Bottom (L P'fld) and draws it on the left. Its corrected label follows construction evidence. The wiring table duplicates Top Lower for 21, while the location list identifies Lower Top, the bottom bumper of the upper cluster. The existing semantic IDs device.right-ramp-bottom-flasher and device.top-upper-jet-bumper remain stable despite corrected display labels. Literal source readings remain in the excerpts.

## GI routing, physical inventory and constant loads

Three physical relays serve two public outputs. Output 11 switches the upper-playfield relay on C-11902-1. Output 16 switches a second playfield relay plus the separate C-11998-1 backbox relay. Factory PDF 106 routes VIO/WHT-VIO at 2J9-5/1 through 11, YEL/WHT-YEL at 2J9-6/7 through 16, and the coin-door 2J10-10/9 branch outside them. The relay command 1 darkens GI and 0 restores it in both original script handlers; it is not direct light intensity.

Harold Toler's official GI OCD installation and original backbox photograph show 35 physical sockets in three bare-wire portions: 17 upper, 6 lower-left, 12 lower-right. The upper portion remains powered; the latter 18 pass through the backbox relay. These are counted sockets in a physical example, with operating split supplied by the installer and factory routing. A separate owner photograph identifies six large-globe #455 blinkers; front/back socket correspondence places all six within the controlled 18, two on the left string and four on the right. These bulbs blink autonomously while powered. Thus the controlled portion includes 12 ordinary lamps and six blinkers; the constant upper portion has 17 ordinary lamps. No additional blinker sockets are added to 35. The portable gi-physical-evidence excerpt retains URLs, hashes, every native socket center and the six withheld correspondence checks.

The five D13356 GI positions are on output 11. An owner traced that light-bar branch parallel with rear playfield GI; a second owner repaired its disconnected purple/white-purple inline pair and restored the panel. The factory power schematic independently identifies those colours with output 11. The portable rear-panel-gi-branch excerpt distinguishes that demonstrated repair from an unregistered owner count of four upper bayonets.

The original UpperGI collection is empty; LowerGI has one light and a broad overlay. The completed stock census establishes 21 playfield bayonets: ten upper (two deep-left, three left-curve, three rear-right, two inner-right) and eleven lower (two three-bank, one left-points, two right-points, one per sling, two per return island). Original photographs expose actual bayonet bodies, violet feeds and local links. The separate eighteen-control wood registration checks all 21 apertures without using them as fit controls; maximum withheld difference from independent 4K socket reads is 0.008534 normalized. Extrapolated corner/return photo points are corroboration only. Twenty exact Bigus bulb meshes agree with the independently authored 4K sites within 0.019435 normalized, under 0.025. The portable gi-playfield-inventory excerpt and pinned seed retain every object hash, raw center, physical read, source URL, fit and limitation.

Output 11 quantity 15 comprises ten playfield bayonets and five D13356 GI lamps, all placed. The ten rear-panel bulbs (five GI, five flashers) use documented projections onto their own front plastic plane. The complete factory socket pattern, actual four mounts, independently registered PCB edges/headers, second assembled elevation and separately mounted stock panel corroborate their X layout and chosen Y plane. Three-decimal measured X and exact model-plane Y do not assert actual PCB depth or emitter Z. The portable rear-panel-placement excerpt and pinned seed retain every read, transform, outside-control position, independent check and camera assumption. Output 16 quantity 29 comprises eleven playfield bayonets and eighteen controlled backbox lamps. Its eleven playfield positions are complete; the eighteen backbox emitters are cabinet/service locations rather than invented playfield points. The 17 constant backbox and two coin-door lamps are outside these switched quantities. Regional voltage observations, actual wiring and 4K switched socket states corroborate the branch split; renderer collections do not provide counts.

The physical census corrects three Bigus artifacts. Light66 duplicates the sole left-sling lamp. Light67's bore actually carries switch leads. Light81 correctly locates one three-bank bulb but puts it in UpperGI; both bank bulbs belong to lower 16. Their published coordinates come from the independent factory drawing: rear (.381,.364), front (.397,.375), native pixels 1712,1033 and 1725,1052, both within the nine mechanism controls. The bank's second bulb is not omitted because the renderer models only one. The left-curve fourth opening carries a wire-gate leg; a black bracket can obscure the third actual bulb. The regional stock excerpts remain useful observations and the new inventory supplies their complete circuit reconciliation.

## Ball transport and ramp mechanisms

A drain closes outhole 10; coil 1 moves the ball into the three-ball trough, sensed by 11-13. Coil 2 feeds the shooter lane. The original cvpmBallStack manages all four sensors through bsTrough.InitSw 10,11,12,13. With no individual sensor geometry, their retained projections are explicitly anchored to Drain and BallRelease, not fabricated separate coordinates.

Either cellar opening,19 right or 20 left, feeds a subway returned through the left exit by 14, assembly B-13225. The solenoid table literally abbreviates 14 as Under P'fld Kickbig; the location list and schematic identify Cellar Kickback. Script exit angle/speed 157/16 are recreation tuning, not factory measurements.

The B-13269 left lock holds up to three balls sensed at 22 lower,23 middle,24 upper. Coil 4 releases the chain. The original script implements that transport with successive Kicker3/Kicker2/Kicker1 events. It does not imply three physical eject coils. Top-right saucer 43 is ejected by 5 through the script's saucer helper.

Coil 3 raises the right ramp entry and 22 lowers it;42 reports ramp position. In the original script, these callbacks switch visible/collidable up/down geometry and update 42 directly. Coil 13 independently moves the diverter. A single 26 drop target resets through 8; the 27-29 bank resets through 7. C-13311 and C-13205-1 are their opto boards. Dropped targets assert through dtT/dtL, and the reset path clears them.

## Jets, slings, flippers, discs and fan

The upper jet cluster uses switches 49-51 and coils 17/19/21; the lower cluster uses 52-54 and 9/15/10. Factory parts are red B-9414-3 and yellow B-9414-2 with B-9415-1 coil/bracket assemblies. B-12030-2 is the switch part, not the whole bumper. Two slings use paired actuating switches at 55/56 and coils 18/20; script flip-book animation is recreation detail.

Three separate physical flipper assemblies each have their own coil and EOS switch: lower-left C-11626-L-3, lower-right and upper-right C-11626-R-3. Both right coils share the right cabinet button, not one physical coil. The original script rotates RightFlipper and RightFlipper1 together; the factory power diagram establishes the separate coils/EOS construction. There is no upper-left flipper. Buttons directly switch the physical power/hold circuits; synthetic outputs 45-48 do not model an independent upper-right CPU driver.

One 14-7955 motor drives all three discs through D-13199's shaft/pinion and 72T/84T/115T gear train. The complete parts list has no sensor, and the script associates no Controller.Switch call with the discs or their collision helpers. This is an unsensed motorized obstacle. The script turns the middle disc opposite the outer pair and coasts SpinnerStep down by .05 per tick; those speeds and decay are table tuning, not factory timing.

Public 38 drives the atop-backbox 14-7956 blower through the sound-overlay and triac boards; it has no sensor. The original table provides sound and a FlSol38 cue rather than a physical fan mesh. Knocker 6 is also backbox mounted. Neither receives an invented playfield coordinate.

## Lamp-table and renderer corrections

All 64 lamp addresses are represented. Addresses 2-8 are physical backbox award lamps even though the original script renders them with Reel objects; the class does not make mechanical score reels. Lamp 64 is Right Spinner. The matrix repeats L Return Lane at 53, while the location list and script identify the left standup at the right ramp. Both printed readings remain literal; row transistors Q80-Q87 are retained with column wiring. Cellar-sign names and arrows are reconciled with the location list.

The original script omits lamp 9 despite retaining l9 geometry. The supplemental Bigus script explicitly binds NfadeL 9,l9 and agrees within .002 normalized at the physical left-outlane insert. This is a consumed-table omission, not a missing physical bulb. Bloom companions and glow helpers do not add lamp quantities.

The 57 playfield matrix bulbs have a separate pinned physical/geometry audit. Factory lamp construction and actual stock bayonet/PCB holders reconcile ordinary bulb-configured objects, with twelve held-out PCB axes checking model/socket correspondence. The photographs are not an exhaustive optical calibration; some sites are occluded and PCB-height parallax is disclosed. Six actual Bigus jet bulb meshes agree exactly with the original centers. Cellar 39/40 instead use the 4K table's separate script-bound BulbLeft/Right glass meshes at (.167547,.462153)/(.338248,.446100): original l39/l40 image-swap objects are colored covers, whose centers cannot stand for the bulbs. All world bounds, raw objects, hashes and physical-photo locators are in the matrix-bulbs seed and portable excerpt. Differently centered 4K insert/glow helpers are effects rather than competing physical sockets.
"""


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
			"ipdb_id": 2765,
			"playfield": {"width": 964.0, "height": 2162.0, "units": "vpx"},
			"opdb_id": "GrE7e-MQ9N1",
		},
		"coverage": {
			"status": "author_ready",
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
	drawing_callouts.apply_to_definition(definition, flasher_seed(), FLASHER_DRAWING_SOURCE)
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
	incomplete_outputs: list[dict[str, Any]] = []
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
			if spatial["status"] != "validated":
				incomplete_outputs.append({
					**binding, "placed": len(spatial["placements"]),
					"quantity": device.get("physical", {}).get("quantity"),
					"status": spatial["status"],
				})
	for device in definition["inputs"]:
		if device["spatial"]["status"] != "not_applicable":
			placement_count += len(device["spatial"]["placements"])
	return {
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": definition["coverage"]["status"],
		"blockers": [],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
			"rear_assembly_raster_sha256": "9b6351d58ed5405a776d9f585ea1c5852cde6aa1b9ee4b08d5ada840836b8338",
			"rear_board_photo_sha256": "e6892411527eb8a56c0b8b747ccb00113bf80eb4ee9ee44146ca20f64fd895ea",
			"operators_handbook_sha256": "b1934cd063d7593a7d912f7100a41b43451d4fae8e51890f6850760f794f6905",
		},
		"flasher_drawing": drawing_callouts.summary(
			flasher_seed(), drawing_callouts.evaluate(flasher_seed(), drawing_callouts.placements_of(definition)),
			FLASHER_SEED_PATH.relative_to(ROOT).as_posix(), FLASHER_SEED_SHA256,
		),
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"omitted_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
		"incomplete_outputs": sorted(incomplete_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/by-machine/williams.whirlwind.1990/archive-arcademanual_Whirlwind_OPS/render/",
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
			"f125-f132/f137/f139/f140 playfield glow helpers in UpdateLamps; these are not modeled bulb sockets",
			"FlSol25-32/37/39/40 BGArr backglass/VR proxies; these do not determine physical fitment",
		],
		"rear_panel_projection": {
			"source_ref": REAR_PLACEMENT_SOURCE,
			"seed": REAR_PLACEMENT_PATH.relative_to(ROOT).as_posix(), "sha256": REAR_PLACEMENT_SHA256,
			"emitter_count": 10, "plane_y": .112843,
			"method": "Registered physical socket X projected onto the assembly's corroborated front plastic plane; not actual PCB depth or emitter Z.",
			"outside_first_mount_span": [p["id"] for p in rear_panel_seed()["sockets"] if p["outside_four_post_x_span"]],
			"independent_checks": "Full PCB edges/header pitch, second assembled elevation with five withheld flasher bases, and mounted stock front-plane camera checks; all raw reads and limits in seed/excerpt.",
		},
		"hidden_bulb_projections": {
			"source_ref": HIDDEN_BULB_SOURCE, "seed": HIDDEN_BULB_PATH.relative_to(ROOT).as_posix(), "sha256": HIDDEN_BULB_SHA256,
			"points": [{"address": p["address"], "xy": p["normalized_xy"], "controls": p["control_count"], "uncertainty_norm": p["conservative_uncertainty_norm"]} for p in hidden_bulbs()["placements"]],
			"method": "Own single glass-body perpendicular XY projection from two physical views; both targets enclosed by independently matched absolute wood controls. Camera assumptions, residuals and rejected variants retained; no exact filament/Z claim.",
		},
		"matrix_bulb_audit": {"source_ref": MATRIX_BULB_SOURCE, "seed": MATRIX_BULB_PATH.relative_to(ROOT).as_posix(), "sha256": MATRIX_BULB_SHA256, "playfield_bulbs": 57, "cellar_geometry": "Own script-bound 4K glass meshes replace original colored cover centers."},
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Whirlwind (Williams, 1990) spatial review", "",
		f"Status: {report['status']}. Complete physical inventories, bulb placements and documented projections are reconciled with the factory construction and retained runtime source.", "",
		"Coordinates use x/964 and y/2162: left=0, right=1; rear=0, front=1. A renderer glow does not supply a socket coordinate.", "",
		"## Evidence decisions", "",
		"- Factory construction identifies 13 C-bank playfield flashlamps. The complete D13356 catalog elevation and actual LMP1-LMP10 pattern prove five rear-playfield flashlamps plus five GI positions; the independent handbook specifies 2/1/2 on 37/39/40, correcting the operations table's three-left-bulb erratum. The original script drives playfield glow helpers and additional backglass/VR proxies; the former mounting conflict was a source-reading error.",
		"- GI 11 has 15 controlled bulbs: 10 playfield plus 5 rear-panel. GI 16 has 29: 11 playfield plus 18 controlled backbox. Seventeen constant backbox and two coin-door bulbs are excluded. Each playfield emitter has a pinned physical inventory and reviewed coordinate; rear sockets project onto their own panel plane.",
		"- All 13 C-bank flashlamps are placed: 5 actual dome bases, 6 measured factory symbols and 2 physically photographed under-insert glass bodies. The latter use bounded two-camera projections at approximately (.527,.331)/(.616,.352), with 0.015 normalized uncertainty; no exact filament/Z claim.",
		"- All 57 playfield matrix bulbs reconcile factory construction with actual socket/PCB correspondence. Six own jet meshes agree exactly; two own cellar glass meshes replace colored cover centers. Insert/glow helpers never add quantities or displace physical bulbs.",
		"- ROM Switch Levels proves targets 26-29 active at public 1 and inactive at 0, with control 15 before and after. The uninverted S11 read path and zero mask establish normally-open matrix contacts. See the portable drop-target-levels excerpt.",
		"- Both right flippers have their own coils and EOS switches, sharing one cabinet button. The two physical right coils do not have independent CPU outputs.",
		"- Jet 21 follows the location list's Lower Top Jet Bumper, resolving the duplicated Top Lower wording in the wiring table.", "",
		"## Promotion decision", "",
	]
	lines += ["- No authoring-critical spatial or semantic blocker remains. Approximate photo measurements, rear-panel projections and renderer limitations are explicitly disclosed."]
	lines += ["", "## Explicit mechanism projections", ""]
	lines += [f"- Switch {item['address']}: {item['reason']}" for item in report["projections"]]
	lines += [
		"", "## Counts", "",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with no spatial record: {len(report['omitted_outputs'])}",
		f"- Outputs with incomplete spatial records: {len(report['incomplete_outputs'])}",
		"", "## Retained evidence", "",
		f"- Original table SHA-256: `{TABLE_SHA256}`; script: `{SCRIPT_SHA256}`.",
		f"- Manual SHA-256: `{MANUAL_SHA256}`; source record carries acquisition URLs and per-page excerpts.",
		f"- Extraction: {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, canonical sorted manifest SHA-256 `{EXTRACTION_MANIFEST_SHA256}`.",
		"- Research, supplemental tables, raw runtime traces and geometry checks: `external:pinmame-review-artifacts/whirlwind-20261106/` and `external:pinmame-vpx-sources/williams/whirlwind-1990/supplemental-20261106/`.", "",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	target = root / DEFINITION_PATH.relative_to(ROOT)
	author_ready = root / "machines/author-ready/williams/whirlwind-1990.json"
	if author_ready.is_file() and author_ready.read_bytes() != canonical_bytes(definition):
		raise RuntimeError("Refusing to overwrite an existing author-ready Whirlwind definition with changed curator output")
	write_json(target, definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	write_text(root / KNOWLEDGE_PATH.relative_to(ROOT), KNOWLEDGE_TEXT.rstrip() + "\n")
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
	knowledge_path = root / KNOWLEDGE_PATH.relative_to(ROOT)
	if not knowledge_path.is_file() or knowledge_path.read_text(encoding="utf-8").rstrip() != KNOWLEDGE_TEXT.rstrip():
		raise RuntimeError(f"Whirlwind recreation knowledge drifted from its deterministic curator: {knowledge_path}")
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
