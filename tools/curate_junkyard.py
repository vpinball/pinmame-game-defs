"""Curate the physical Williams Junk Yard (1996) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed
label, wiring detail, and normalized coordinate as a literal, so regeneration
reproduces the canonical artifact byte-for-byte without reading the external
evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only
path that writes the canonical definition and its pinned seed.
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
PARTIAL_PATH = ROOT / "machines/partial/williams/junkyard-1996.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/junkyard-1996.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/junkyard-1996.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/junkyard-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/junkyard-1996.md"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.junkyard.1996"
VPX_TABLE_SOURCE = "vpx-table.junkyard-mfuegemann"
VPX_SCRIPT_SOURCE = "vpx-script.junkyard-mfuegemann"
VPX_EXTRACTION_SOURCE = "vpx-extraction.junkyard-mfuegemann"

TABLE_SHA256 = "8ff2c1c8ae3457a4b88ff2207bc506d07435b049343301ded4dbf8e855bef07f"
SCRIPT_SHA256 = "b583aed396fea3cf6e2f862fdb51989aa01a99e624bbae8b30e8aeba7eeb4033"
MANUAL_SHA256 = "08819a08990c61070c4a3a99a4d5f00d9d082b6d00477ffaf9b0a58fddce3fe1"

EXTRACTION_RELATIVE_PATH = Path("williams/junkyard-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/junkyard-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "bb9b127b90d2e892f18707933288e15a080819e7d27cefaf787ee04379adbdbc"
EXTRACTION_FILE_COUNT = 1008
EXTRACTION_TOTAL_BYTES = 299118752

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"
TABLE_WIDTH = 952.0
TABLE_HEIGHT = 2162.0


DRIVER_IDS = ("jy_12", "jy_12c", "jy_11", "jy_03")
DRIVER_COMPATIBILITY = {
	"jy_12": (
		"identical",
		"Williams production 1.2 game ROM (DCS sound) shipped with the physical machine; the retained "
		"known-working script binds this exact driver (cGameName = \"jy_12\"). Pinned PinMAME's own "
		"libpinmame.h comment names GEN_WPC95 \"Integrated boards, Congo 3/96 - Cactus Canyon 2/99\", i.e. "
		"Junk Yard is part of the same integrated-board WPC-95 hardware generation as the other machines in "
		"that era.",
	),
	"jy_12c": (
		"compatible",
		"Williams 1.2C Competition MOD (2019), a community ruleset built on the 1.2 game ROM that runs on "
		"the identical physical hardware and addresses; a later firmware revision of the same physical "
		"machine with no controller-address or playfield change.",
	),
	"jy_11": (
		"identical",
		"Williams 1.1 game ROM; an earlier firmware revision of the same physical machine with no "
		"controller-address or playfield change.",
	),
	"jy_03": (
		"identical",
		"Williams 0.3 Prototype game ROM; a prototype firmware revision of the same physical machine with "
		"no controller-address or playfield change.",
	),
}

# --- Printed switch matrix (manual page 2-34 wiring, 2-35 parts list).
SWITCH_LABELS = {
	11: "Toaster Gun", 12: "Rebound Switch", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Top Left Crane", 16: "Left Outlane", 17: "Left Return Lane", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Not Used", 24: "Always Closed",
	25: "Not Used", 26: "Right Return Lane", 27: "Right Outlane", 28: "Crane Down",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Lock Up 2", 37: "Lock Up 1", 38: "Top Right Crane",
	41: "Past Spinner", 42: "In The Sewer", 43: "Lock Jam", 44: "Past Crane",
	45: "Ramp Exit", 46: "Car Target 1 (Left)", 47: "Car Target 2", 48: "Car Target 3",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Car Target 4", 54: "Car Target 5 (Right)",
	55: "Not Used", 56: "Lower Left 3-Bank Bottom", 57: "Lower Left 3-Bank Middle", 58: "Lower Left 3-Bank Top",
	61: "Upper Right 3-Bank Bottom", 62: "Upper Right 3-Bank Middle", 63: "Upper Right 3-Bank Top",
	64: "Upper Left 3-Bank Bottom", 65: "Upper Left 3-Bank Middle", 66: "Upper Left 3-Bank Top",
	67: "Bowl Entry", 68: "Bowl Exit",
	71: "Ramp Entry", 72: "Scoop Down", 73: "Scoop Made", 74: "Dog Entry", 75: "Not Used",
	76: "Right 3-Bank Bottom", 77: "Right 3-Bank Middle", 78: "Right 3-Bank Top",
	81: "Not Used", 82: "Not Used", 83: "Not Used", 84: "Not Used",
	85: "Not Used", 86: "Not Used", 87: "Not Used", 88: "Not Used",
}

UNUSED_MATRIX_ADDRESSES = {23, 25, 55, 75, 81, 82, 83, 84, 85, 86, 87, 88}

# Opto construction per the Switch Locations parts list (2-35). Column 3 rows 1-7 (31-37) carry the
# trough and lock-up optos (A-18617-1/A-18618-1 for 31-35, A-16908/A-16909 for 36-37); column 4 rows 1-4
# (41-44) carry the A-16908/A-16909 opto pair for Past Spinner, In The Sewer, Lock Jam, and Past Crane.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44}
# The subset of opto addresses that PinMAME's jyGameData inverted-switch mask actually normalizes
# (column 3 = 0x7f covers rows 1-7 = 31-37; column 4 = 0x07 covers rows 1-3 = 41-43). Switch 44
# (Past Crane) is opto-constructed but NOT in this set -- the one polarity conflict.
NORMALIZED_OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 41, 42, 43}

# Pulsed switches from the retained known-working script (vpmTimer.PulseSw / Controller.Switch setters).
PULSED_SWITCHES = {12, 16, 17, 18, 26, 27, 28, 41, 42, 44, 45, 46, 47, 48, 51, 52, 61, 62, 63, 64, 65, 66, 72, 73, 76, 77, 78}

SWITCH_TYPES = {
	11: "microswitch", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "microswitch", 17: "microswitch", 18: "microswitch",
	21: "leaf", 22: "microswitch", 24: "other", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 38: "microswitch",
	41: "opto", 42: "opto", 43: "opto", 44: "opto",
	45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "leaf", 52: "leaf", 53: "microswitch", 54: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch", 66: "microswitch",
	67: "microswitch", 68: "microswitch",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "microswitch",
	76: "microswitch", 77: "microswitch", 78: "microswitch",
}
SWITCH_PARTS = {
	11: "A-18530-6", 12: "A-17794", 13: "20-9663-16", 14: "04-10346", 15: "A-18530-4",
	16: "5647-12693-19", 17: "5647-12693-19", 18: "5647-12693-65",
	21: "A-17238", 22: "5643-09268-00", 24: "5643-15190-00", 26: "5647-12693-19",
	27: "5647-12693-19", 28: "5647-12693-31",
	31: "A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", 32: "A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)",
	33: "A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)", 34: "A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)",
	35: "A-18617-1 (LED) / A-18618-1 (PHOTO TRANS)",
	36: "A-16908 (LED) / A-16909 (PHOTO TRANS)", 37: "A-16908 (LED) / A-16909 (PHOTO TRANS)",
	38: "A-18530-4",
	41: "A-16908 (LED) / A-16909 (PHOTO TRANS)", 42: "A-16908 (LED) / A-16909 (PHOTO TRANS)",
	43: "A-16908 (LED) / A-16909 (PHOTO TRANS)", 44: "A-16908 (LED) / A-16909 (PHOTO TRANS)",
	45: "A-12556", 46: "SW-1A-210-1", 47: "SW-1A-210-2", 48: "SW-1A-210-3",
	51: "A-17800 (KICK) / A-17794 (SCORE)", 52: "A-17800 (KICK) / A-17794 (SCORE)",
	53: "SW-1A-210-4", 54: "SW-1A-210-5",
	56: "A-21349-1", 57: "A-21349-1", 58: "A-21349-1",
	61: "A-21351-1", 62: "A-21351-2", 63: "A-21351-3", 64: "A-21351-4", 65: "A-21351-5", 66: "A-21351-6",
	67: "5647-12693-36", 68: "5647-12693-21",
	71: "5647-12693-21", 72: "5647-12693-36", 73: "5647-12693-21", 74: "5647-12693-19",
	76: "A-21349-1", 77: "A-21349-1", 78: "A-21349-1",
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
# Fliptronic F1-F8 wiring, printed 2-34. F6/F7/F8 are Not Used (Junk Yard fits no upper flippers).
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed Solenoid/Flasher Table (manual page 2-38) and Solenoid/Flashlamp Locations (2-39).
SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Refrigerator Popper", 3: "Power Crane",
	4: "Not Used Solenoid 4", 5: "Scoop Down", 6: "Bus Diverter", 7: "Knocker",
	8: "Not Used Solenoid 8", 9: "Trough", 10: "Left Slingshot", 11: "Right Slingshot",
	12: "Not Used Solenoid 12", 13: "Not Used Solenoid 13", 14: "Not Used Solenoid 14",
	15: "Hold Crane", 16: "Move Dog",
	17: "Dog Face Flasher", 18: "Window Shop Flasher", 19: "Autofire Flashers",
	20: "Left Side Flashers", 21: "Scoop Up", 22: "Under Crane Flasher",
	23: "Back Left Flashers", 24: "Back Right Flashers", 25: "Shooter Flasher",
	26: "Scoop Flashers", 27: "Dog House Flasher", 28: "Cars Flashers",
	33: "Unused Upper Right Power", 34: "Unused Upper Right Hold",
	35: "Unused Upper Left Power", 36: "Unused Upper Left Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}

MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}

# address -> driver_transistor, control_connection(s), power_connection(s), part_number, printed_type
SOLENOID_WIRING = {
	1: dict(power_connection="J133-2", driver_transistor="Q72", control_connection="J116-1", part_number="AE-23-800", printed_type="High Power"),
	2: dict(power_connection="J133-2", driver_transistor="Q68", control_connection="J116-2", part_number="AE-23-800", printed_type="High Power"),
	3: dict(power_connection="J133-2", driver_transistor="Q71", control_connection="J116-4", part_number="A-20099", printed_type="High Power"),
	4: dict(power_connection="J133-2", driver_transistor="Q67", part_number="AE-23-800", printed_type="High Power"),
	5: dict(power_connection="J133-2", driver_transistor="Q70", control_connection="J116-6", part_number="SM1-28-900", printed_type="High Power"),
	6: dict(power_connection="J133-2", driver_transistor="Q66", control_connection="J116-7", part_number="AE-27-1200", printed_type="High Power"),
	7: dict(power_connection="J133-2", driver_transistor="Q69", control_connection="J116-8", part_number="AE-23-800", printed_type="High Power"),
	8: dict(power_connection="J133-2", driver_transistor="Q65", part_number="AE-23-800", printed_type="High Power"),
	9: dict(power_connection="J133-3", driver_transistor="Q44", control_connection="J113-1", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(power_connection="J133-3", driver_transistor="Q48", control_connection="J113-3", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(power_connection="J133-3", driver_transistor="Q43", control_connection="J113-4", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(power_connection="J133-3", driver_transistor="Q47", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(power_connection="J133-3", driver_transistor="Q42", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(power_connection="J133-3", driver_transistor="Q46", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(power_connection="J133-2", driver_transistor="Q41", control_connection="J113-8", part_number="A-20099", printed_type="Low Power"),
	16: dict(power_connection="J133-3", driver_transistor="Q45", control_connection="J113-9", part_number="AE-26-1200", printed_type="Low Power"),
	17: dict(power_connection="J133-6", driver_transistor="Q28", control_connection="J111-1", part_number="#906 (1)", printed_type="Flasher"),
	18: dict(power_connection="J133-6", driver_transistor="Q32", control_connection="J112-2", part_number="#906 (1)", printed_type="Flasher"),
	19: dict(power_connection="J133-6", driver_transistor="Q27", control_connection="J111-3", part_number="#89 (2)", printed_type="Flasher"),
	20: dict(power_connection="J133-6", driver_transistor="Q31", control_connection="J111-4 / J112-5", part_number="#906 (1) playfield / #906 (1) insert", printed_type="Flasher"),
	21: dict(power_connection="J133-3", driver_transistor="Q26", control_connection="J111-5", part_number="AE-26-1200", printed_type="Low Power"),
	22: dict(power_connection="J133-6", driver_transistor="Q30", control_connection="J111-6", part_number="#906 (1)", printed_type="Flasher"),
	23: dict(power_connection="J133-6", driver_transistor="Q25", control_connection="J111-7 / J112-8", part_number="#906 (1) playfield / #906 (1) insert", printed_type="Flasher"),
	24: dict(power_connection="J133-6", driver_transistor="Q29", control_connection="J111-8 / J112-9", part_number="#906 (1) playfield / #906 (1) insert", printed_type="Flasher"),
	25: dict(power_connection="J133-6", driver_transistor="Q16", control_connection="J109-1", part_number="#906 (1)", printed_type="Gen. Purpose"),
	26: dict(power_connection="J133-6", driver_transistor="Q15", control_connection="J109-2 / J108-3", part_number="#906 (1) playfield / #906 (1) insert", printed_type="Gen. Purpose"),
	27: dict(power_connection="J133-6", driver_transistor="Q14", control_connection="J109-3", part_number="#89 (1)", printed_type="Gen. Purpose"),
	28: dict(power_connection="J133-6", driver_transistor="Q13", control_connection="J109-4", part_number="#89 (2)", printed_type="Gen. Purpose"),
	33: dict(power_connection="J119-6 (RED-VIO)", driver_transistor="Q84", control_connection="J120-6", printed_type="Fliptronic power"),
	34: dict(power_connection="J119-6 (RED-VIO)", driver_transistor="Q86", control_connection="J120-4", printed_type="Fliptronic hold"),
	35: dict(power_connection="J119-8 (RED-GRY)", driver_transistor="Q81", control_connection="J120-3", printed_type="Fliptronic power"),
	36: dict(power_connection="J119-8 (RED-GRY)", driver_transistor="Q83", control_connection="J120-1", printed_type="Fliptronic hold"),
	45: dict(power_connection="J119-1 (RED-GRN)", driver_transistor="Q90", control_connection="J120-13", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(power_connection="J119-1 (RED-GRN)", driver_transistor="Q92", control_connection="J120-11", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(power_connection="J119-4 (RED-BLU)", driver_transistor="Q87", control_connection="J120-9", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(power_connection="J119-4 (RED-BLU)", driver_transistor="Q89", control_connection="J120-7", part_number="FL-11629", printed_type="Fliptronic hold"),
}

SOLENOID_ASSEMBLIES = {
	1: "A-21022", 2: "A-21216", 3: "A-21523", 5: "A-21220", 6: "A-21409-1", 7: "B-10686-1",
	9: "A-19963-1", 10: "B-9362-R-3", 11: "B-9362-R-3", 15: "A-21523", 16: "A-21383",
	17: "A-21395", 19: "A-17984", 21: "A-21220", 22: "A-21525", 23: "A-20158", 24: "A-20158",
	25: "A-17802", 26: "A-21355", 27: "A-17983", 28: "04-10509",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}

SOLENOID_CALLBACKS = {
	1: "Autoplunger (Auto_Plunger.Pullback/.Fire when switch 18)", 2: "bsFridgePopper.SolOut",
	3: "SolPowerCrane (Wrecker ball chain/crane drive)",
	5: "ScoopDown (Controller.Switch(72)=True, fork arms down)", 6: "BusDiverter (Sol6.IsDropped)",
	7: 'vpmSolSound SoundFX("Knocker",DOFKnocker)', 9: "SolTrough (bsTrough.ExitSol_On, PulseSw 31)",
	10: "vpmSolSound SoundFX(\"Slingshot\") left, PulseSwitch 51", 11: "vpmSolSound SoundFX(\"Slingshot\") right, PulseSwitch 52",
	15: "SolHoldCrane (Wrecker ball hold)", 16: "SpikeBark (SpikeTimer, dog spike)",
	17: "SolFlash17 (dog face flasher)", 19: "vpmFlasher Sol19 (autofire flasher)", 20: "SolFlash20 (fridge flasher)",
	21: "ScoopUp (Controller.Switch(72)=False, forks up)", 22: "SolFlash22 (under-crane flasher)",
	23: "SolFlash23 (back-left flasher)", 24: "SolFlash24 (back-right flasher)",
	25: "SolFlash25 (shooter flasher)", 26: "SolFlash26 (scoop flasher)",
	27: "SolFlash27 (dog-house flasher)", 28: "SolFlash28 (car flashers, two)",
	46: "SolRFlipper (RightFlipper)", 48: "SolLFlipper (LeftFlipper)",
}

FLASHER_QTY = {
	17: ("#906 (1) on the playfield", 1, 1), 18: ("#906 (1) on the backbox", 1, 0),
	19: ("#89 (2) on the playfield", 2, 2), 20: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	22: ("#906 (1) on the playfield", 1, 1), 23: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	24: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	25: ("#906 (1) on the playfield", 1, 1), 26: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	27: ("#89 (1) on the playfield", 1, 1), 28: ("#89 (2) on the playfield", 2, 2),
}

# --- Printed lamp matrix (manual page 2-36 wiring, 2-37 locations).
LAMP_LABELS = {
	11: "Top Left Bank Bottom", 12: "Top Left Bank Middle", 13: "Top Left Bank Top",
	14: "Top Right Bank Top", 15: "Top Right Bank Middle", 16: "Top Right Bank Bottom",
	17: "Right Recycle", 18: "Right Crane H.U.",
	21: "Right 3-Bank Top", 22: "Right 3-Bank Middle", 23: "Right 3-Bank Bottom",
	24: "Left Bank Bottom", 25: "Left Bank Middle", 26: "Left Bank Top",
	27: "Fan", 28: "Bath Tub",
	31: "Jackpot", 32: "Super Jackpot", 33: "Multiball", 34: "Wrecking Ball",
	35: "Radar Adventure", 36: "Jalopy Race", 37: "Toilet Adventure", 38: "A.T.C. Adventure",
	41: "Gen. Bus", 42: "Toast", 43: "Magic Bus", 44: "Collect Junk",
	45: "Coo Coo Clock", 46: "Television", 47: "Weather Vane", 48: "Fish Bowl",
	51: "Gen. Toilet", 52: "Window Shopping", 53: "Left Recycle", 54: "Left Crane H.U.",
	55: "Shoot Again", 56: "Not Used", 57: "Toaster", 58: "Hair Dryer",
	61: "Propeller", 62: "Outer Space", 63: "DO(G)", 64: "(D)OG", 65: "D(O)G",
	66: "Choose Junk", 67: "Angel Slingshot", 68: "Bicycles",
	71: "Time Machine", 72: "Start Adventure", 73: "Extra Ball", 74: "Toast",
	75: "Gen. Sewer", 76: "Toaster Gun", 77: "Gen. Alley", 78: "Devil Slingshot",
	81: "Fireworks", 82: "Toxic Waste", 83: "Light Extra Ball", 84: "Free Game",
	85: "Light Jackpot", 86: "Gen. Crane", 87: "Not Used", 88: "Start Button",
}

LAMP_BULB = {
	11: "#555", 12: "#555", 13: "#555", 14: "#555", 15: "#555", 16: "#555",
	17: "#44", 18: "#44",
	21: "#555", 22: "#555", 23: "#555", 24: "#555", 25: "#555", 26: "#555",
	27: "#44", 28: "#44",
	31: "#555", 32: "#555", 33: "#555", 34: "#555", 35: "#555", 36: "#555", 37: "#555", 38: "#555",
	41: "#555", 42: "#555", 43: "#555", 44: "#44",
	45: "#555", 46: "#555", 47: "#555", 48: "#555",
	51: "#555", 52: "#555", 53: "#44", 54: "#44", 55: "#44",
	57: "#44", 58: "#44",
	61: "#555", 62: "#555", 63: "#555", 64: "#555", 65: "#555", 66: "#555",
	67: "#44 (2 bulbs)", 68: "#44",
	71: "#555", 72: "#555", 73: "#555", 74: "#555", 75: "#555",
	76: "#44", 77: "#44", 78: "#44 (2 bulbs)",
	81: "#555", 82: "#555", 83: "#555", 84: "#555", 85: "#555", 86: "#44",
}

LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
	3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Black", "J121-4", "Q99"),
	5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
	3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
	5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}
# Items 81-86 are annotated "located on the insert panel" on the Lamp Locations page.
INSERT_PANEL_LAMPS = {81, 82, 83, 84, 85, 86}

GI_STRINGS = {
	0: ("Playfield String 1", "J105-1 / J105-7", "Q5", "#44"),
	1: ("Playfield String 2", "J105-2 / J105-8", "Q4", "#44"),
	2: ("Logo String 3", "J106-3 / J106-9", "Q3", "#555"),
	3: ("Illumination String 4 (always on)", "J106-5 / J106-10", "Q2", "#555"),
	4: ("Illumination String 5 (always on)", "J106-6 / J104-3 / J106-11 / J104-1", "Q1", "#555"),
}

# --- Normalized playfield coordinates (x/952, y/2162) from the retained VPX extraction.
SWITCH_POSITIONS = {
	11: [(0.640537, 0.323614)], 15: [(0.370113, 0.113269)],
	12: [(0.103504, 0.422329)],
	28: [(0.865764, 1.350081)],
	31: [(0.869354, 0.866385)],
	32: [(0.869354, 0.866385)],
	33: [(0.869354, 0.866385)],
	34: [(0.869354, 0.866385)],
	35: [(0.869354, 0.866385)],
	36: [(0.798582, 0.421369)],
	37: [(0.798582, 0.421369)],
	42: [(0.798582, 0.421369)],
	43: [(0.080396, 0.466650)],
	16: [(0.061396, 0.734114)], 17: [(0.136199, 0.737552)], 18: [(0.947154, 0.880379)],
	26: [(0.789611, 0.738814)], 27: [(0.865246, 0.734808)],
	38: [(0.559668, 0.113615)], 41: [(0.940543, 0.475824)],
	42: [(0.711827, 1.391472)], 44: [(0.247794, 0.041003)], 45: [(0.807913, 0.109658)],
	46: [(0.280217, 0.150392)], 47: [(0.363981, 0.117515)], 48: [(0.470102, 0.104233)],
	51: [(0.226610, 0.725648)], 52: [(0.686888, 0.728451)],
	53: [(0.581586, 0.120938)], 54: [(0.658672, 0.155413)],
	56: [(0.133647, 0.561311)], 57: [(0.135694, 0.531456)], 58: [(0.137639, 0.501187)],
	61: [(0.674824, 0.175079)], 62: [(0.640212, 0.152867)], 63: [(0.604523, 0.129689)],
	64: [(0.261952, 0.178108)], 65: [(0.294782, 0.155378)], 66: [(0.328613, 0.131666)],
	67: [(0.094363, 0.313984)], 68: [(0.188671, 0.053608)],
	71: [(0.214811, 0.30535)], 72: [(0.734508, 0.282871)], 73: [(0.734508, 0.282871)], 74: [(0.839130, 0.286291)],
	76: [(0.806296, 0.553691)], 77: [(0.807320, 0.524401)], 78: [(0.808225, 0.494915)],
	115: [(0.933303, 0.505121)],
}
SWITCH_PROJECTIONS = {
	12: "Projected onto the movable Rebound Switch wall object (Wall.Switch12a, drag-point centroid): "
	    "the retained script pulses switch 12 from the Switch12 and Switch12a wall hit handlers and there is "
	    "no separate trigger object.",
	31: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center): the retained "
	    "cvpmTrough helper (bsTrough) models switches 32-35 purely as an internal switch array with no separate "
	    "playfield trigger object, and the trough-eject opto is pulsed in the same SolTrough handler that fires "
	    "the BallRelease kicker.",
	32: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	33: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	34: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	35: "Projected onto the trough's own release kicker (Kicker BallRelease, table object center); see switch 31.",
	36: "Projected onto the sewer kicker (Kicker Sewer, table object center): the lock-up two-slot bank sits "
	    "beside the sewer/scoop complex and the retained script models the two lock-up optos (36, 37) as part of "
	    "the same ball stack helper as the sewer entries.",
	37: "Projected onto the sewer kicker (Kicker Sewer, table object center); see switch 36.",
	43: "Projected onto the refrigerator popper kicker (Kicker Sol2, table object center): switch 43 "
	    "(Lock Jam) is the popper's internal position reported by the retained script's bsFridgePopper ball "
	    "stack handling, and the fridge unit has no separate switch-43 trigger object.",
}

# Switches whose only retained VPX object sits below the playfield apron (y > 1) and cannot be
# promoted to a validated playfield coordinate; their spatial key is omitted entirely. Switch 28
# (Crane Down) has no separate playfield object (its only candidate is off-apron), and switch 42
# (In The Sewer) likewise reports through the hidden sewer sink rather than a playfield trigger.
UNRESOLVED_SWITCHES = {28, 42}

SOLENOID_POSITIONS = {
	1: [(0.955817, 0.956156)], 2: [(0.080396, 0.466650)],
	3: [(0.100972, 0.068166)], 5: [(0.247794, 0.041003)],
	6: [(0.784861, 0.124993)], 9: [(0.869354, 0.866385)],
	10: [(0.226610, 0.725648)], 11: [(0.686888, 0.728451)],
	16: [(0.927521, 0.277521)],
	17: [(0.941736, 0.333218)], 22: [(0.463120, 0.203393)],
}
SOLENOID_PROJECTIONS = {
	3: "Projected onto the crane mechanism's top-left hole (Kicker CraneHole, table object center); the crane "
	    "arm itself (PCraneArm) is a render primitive without a switch/solenoid collision object.",
	16: "Projected onto the dog-house spike object (Primitive Spike, table object center): solenoid 16 (Move "
	    "Dog) drives the spike arm that the retained script's SpikeTimer animates.",
}

# GI address 0 is the retained script's GIString1 collection plus the six bloom lights (GI22-GI27);
# GI address 1 is GIString2. GI addresses 2-4 are backbox strings with no playfield coordinate.
GI_POSITIONS = {
	0: [
		(0.814732, 0.774690), (0.703388, 0.816898), (0.704438, 0.756135), (0.767332, 0.798797),
		(0.724265, 0.709066), (0.217371, 0.756652), (0.151326, 0.799750), (0.103926, 0.775643),
		(0.219013, 0.817761), (0.197545, 0.709583), (0.084559, 0.423219), (0.850315, 0.529140),
		(0.067752, 0.584644), (0.855567, 0.598520), (0.860819, 0.354764), (0.695252, 0.763266),
		(0.760611, 0.805614), (0.691517, 0.824116), (0.225597, 0.762444), (0.160238, 0.804792),
		(0.229332, 0.823294), (0.464810, 0.939524), (0.033789, 0.111505), (0.275307, 0.067376),
		(0.658750, 0.067376), (0.738426, 0.205793), (0.924337, 0.307026), (0.828062, 0.030738),
	],
	1: [(0.257878, 0.137373), (0.670693, 0.139223), (0.163340, 0.253006), (0.746324, 0.216235)],
}

LAMP_POSITIONS = {
	11: [(0.310346, 0.190316)], 12: [(0.363392, 0.170080)], 13: [(0.382300, 0.144641)],
	14: [(0.537499, 0.144756)], 15: [(0.567961, 0.168692)], 16: [(0.600787, 0.192050)],
	17: [(0.866592, 0.680168)], 18: [(0.790174, 0.672282)],
	21: [(0.777390, 0.504262)], 22: [(0.777873, 0.532842)], 23: [(0.775468, 0.559949)],
	24: [(0.177642, 0.559586)], 25: [(0.179659, 0.532219)], 26: [(0.179134, 0.503888)],
	27: [(0.741641, 0.637150)], 28: [(0.681226, 0.679178)],
	31: [(0.464543, 0.423198)], 32: [(0.467169, 0.376133)], 33: [(0.464281, 0.320788)],
	34: [(0.463206, 0.267443)], 35: [(0.277128, 0.523908)], 36: [(0.344312, 0.514979)],
	37: [(0.419197, 0.512368)], 38: [(0.491151, 0.514842)],
	41: [(0.257679, 0.359881)], 42: [(0.292096, 0.406843)], 43: [(0.316431, 0.441948)],
	44: [(0.338191, 0.473491)], 45: [(0.241812, 0.677948)], 46: [(0.193535, 0.636394)],
	47: [(0.194538, 0.604101)], 48: [(0.288115, 0.573656)],
	51: [(0.149665, 0.387251)], 52: [(0.185297, 0.427775)], 53: [(0.060174, 0.680701)],
	54: [(0.137248, 0.671051)], 55: [(0.464239, 0.870375)], 57: [(0.308598, 0.761723)],
	58: [(0.309862, 0.788714)],
	61: [(0.532905, 0.588506)], 62: [(0.542054, 0.535797)], 63: [(0.598319, 0.493097)],
	64: [(0.635694, 0.431067)], 65: [(0.615833, 0.462640)], 66: [(0.213663, 0.458859)],
	67: [(0.218045, 0.748307)], 68: [(0.560870, 0.735777)],
	71: [(0.608493, 0.602832)], 72: [(0.630247, 0.580573)], 73: [(0.667579, 0.547601)],
	74: [(0.702285, 0.514389)], 75: [(0.753409, 0.471492)], 76: [(0.588535, 0.394694)],
	77: [(0.660846, 0.390995)], 78: [(0.701554, 0.749743)],
	86: [(0.465988, 0.139605)],
}
# Lamps without a playfield placement in the retained table: 56 and 87 are printed Not Used; 81-85 are
# insert-panel lamps with no playfield Light object; 88 is the cabinet start button.
LAMP_POSITIONS_UNUSED_OR_BACKBOX = {56, 81, 82, 83, 84, 85, 87, 88}

GI_STRING1_OBJECTS = {1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 18, 21}
GI_STRING2_OBJECTS = {16, 17, 19, 20}

def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Junk Yard retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{
				"path": path.relative_to(extraction_root).as_posix(),
				"size": path.stat().st_size,
				"sha256": _file_sha256(path),
			}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Junk Yard extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Junk Yard retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Junk Yard retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Junk Yard retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
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
				"provenance": provenance(*source_refs),
			}
		)
	return {"status": "validated", "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}

def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the jy_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/jy.c jyGameData GEN_WPC95 with wpc_dispDMD, "
				"FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), the inverted-switch mask "
				"{0x00,0x00,0x00,0x7f,0x07,0x00,...} (column 3 bits 0-6 = rows 1-7 = switches 31-37, column 4 "
				"bits 0-2 = rows 1-3 = 41-43), swStart/swTilt/swSlamTilt/swCoinDoor/swTicket defines, and "
				"init_jy's wpc_set_fastflip_addr(0x80); src/wpc/wpc.c wpc_dispDMD 128x32 DMD layout; "
				"src/wpc/core.h CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, and the sLRFlip/sLRFlipPow/"
				"sLLFlip/sLLFlipPow/sURFlip/sURFlipPow/sULFlip/sULFlipPow offsets; src/wpc/gen.h GEN_WPC95; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-95.json",
			"revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.junkyard.1996/Junk_Yard_Operations_Manual.pdf",
			"original_filename": "Williams_Junk_Yard.PDF",
			"sha256": MANUAL_SHA256,
			"locator": (
				"146-page Williams Junk Yard Operations Manual (16-50052-101, JANUARY 1997 FINAL), a scanned "
				"document with a usable OCR text layer. Printed pages 2-34 through 2-39 carry the switch matrix, "
				"switch locations, lamp matrix, lamp locations, solenoid/flasher table, and solenoid/flashlamp "
				"locations pages; the loose front-matter page (PDF page 2) duplicates the Solenoid/Flasher Table "
				"with the DIP switch chart and EPROM jumper settings; Section 3 repeats the tables at 3-2 through "
				"3-5. Section 2-40 through 2-43 carry the general illumination and flipper circuit tables."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt-junkyard.switch-matrix",
					"locator": "PDF page 110, printed 2-34, SWITCH MATRIX table",
					"path": "evidence/excerpts/williams.junkyard.1996/switch-matrix.md",
					"sha256": "ec89129e4b28e82ddcee93024b53d7d0969956ff616f5ae1c96f31039ec5d0f0",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page; cross-checked against two repeated copies",
					"reviewed": False,
				},
				{
					"id": "excerpt-junkyard.switch-locations",
					"locator": "PDF page 111, printed 2-35, Switch Locations parts list",
					"path": "evidence/excerpts/williams.junkyard.1996/switch-locations.md",
					"sha256": "14669b28fa11a9f840a3e932de914fb4fb7f6aae6c1e4400402a18c1eebcbf59",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page",
					"reviewed": False,
				},
				{
					"id": "excerpt-junkyard.lamp-matrix",
					"locator": "PDF page 112, printed 2-36, LAMP MATRIX table",
					"path": "evidence/excerpts/williams.junkyard.1996/lamp-matrix.md",
					"sha256": "3ffc96bfbbbdaa6eef8ed918678010fb3259fcca68700dd32d8837c293b469bf",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page; cross-checked against repeated copies",
					"reviewed": False,
				},
				{
					"id": "excerpt-junkyard.lamp-locations",
					"locator": "PDF page 113, printed 2-37, Lamp Locations LOCATION",
					"path": "evidence/excerpts/williams.junkyard.1996/lamp-locations.md",
					"sha256": "70815d934c020da7f47a47d47096ee673ca2fdec6b97d326eaee05311fbbefc6",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page",
					"reviewed": False,
				},
				{
					"id": "excerpt-junkyard.solenoid-flasher-table",
					"locator": "PDF page 114, printed 2-38, SOLENOID/FLASHER TABLE, GENERAL ILLUMINATION, and FLIPPER CIRCUITS",
					"path": "evidence/excerpts/williams.junkyard.1996/solenoid-flasher-table.md",
					"sha256": "ce85a949fb9f252721966d672bbf12caf90c51b7711ae024dc705564196939ec",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page; cross-checked against the front-matter and Section-3 copies",
					"reviewed": False,
				},
				{
					"id": "excerpt-junkyard.solenoid-locations",
					"locator": "PDF page 115, printed 2-39, Solenoid/Flashlamp LOCATION",
					"path": "evidence/excerpts/williams.junkyard.1996/solenoid-locations.md",
					"sha256": "8216b87751a54358b91014bba29dc70b2404c4700aaa359a74ec5379ebf36f1e",
					"method": "model",
					"transcribed_by": "vision worker (sonnet) transcribed from the rendered page",
					"reviewed": False,
				},
			],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/junkyard-1996/source/Junk%20Yard%20(Williams%201996).vpx",
			"original_filename": "Junk Yard (Williams 1996).vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working recreation of the physical machine (VPX v1.3, author mfuegemann; "
				"primitives/textures by Fuzzel and Dark, lighting by Hauntfreaks), binding driver \"jy_12\". "
				f"Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/952 and y/2162. "
				"Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "mfuegemann, Fuzzel, Dark, Hauntfreaks",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/junkyard-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (74,162 bytes). Runtime and mechanism-causality authority: cGameName = '
				'"jy_12", Const UseSolenoids = 1 / UseLamps = 1 / UseGI = True, the SolCallBack table for '
				"solenoids 1-28 plus sLLFlipper/sLRFlipper, the cvpmBallStack trough and refrigerator-popper "
				"helpers (bsTrough with switches 32-35, bsFridgePopper with 37/36/43), the WreckerBall/Crane "
				"power-and-hold chain driven by solenoids 3 and 15, the Spike dog-bark mechanism on solenoid 16, "
				"the UpdateGI string collections GIString1/GIString2, and the Switch115 spinner plus the "
				"switch11/12/15/16/17/18/26/27/28/41/42/44/45/51/52/56/61/62/63/64/65/66/67/68/71/72/73/74/"
				"76/77/78 callbacks."
			),
			"license": "NOASSERTION",
			"attribution": "mfuegemann",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/junkyard-1996/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} "
				f"files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
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


def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_component = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC-95 CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, component = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door" if address <= 4 else "cabinet", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			part_number = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the Switch Locations parts list both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				shaded = "shaded \"OPTO, TYPICALLY CLOSED\" on the printed switch matrix (column 3 rows 1-7)" if column == 3 else (
					f"printed in column {column}, which the switch matrix does not shade (only column 3 is shaded)"
				)
				normalized = (
					"PinMAME's jyGameData inverted-switch mask normalizes this address, so the public "
					"switch state is already normalized and must not be inverted again."
				) if address in NORMALIZED_OPTO_SWITCHES else (
					"PinMAME's jyGameData inverted-switch mask does NOT normalize this address, so the "
					"printed A-16908/A-16909 opto pair is not inverted by the emulator."
				)
				notes += (
					" Printed on the switch-locations parts list with an LED/photo-transistor opto pair and "
					"no separate switch part number, " + shaded + ". " + normalized
				)
			if address == 24:
				notes += " Physical part 5643-15190-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Matrix Position {address}"
				refs = (MANUAL_SOURCE, CONTROLLER_SOURCE)
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				if address in PULSED_SWITCHES:
					extra["pulse"] = True
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet interior" if address != 13 else "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address in UNRESOLVED_SWITCHES:
					pass  # spatial intentionally omitted; raw VPX object sits below the playfield apron
				elif address in SWITCH_PROJECTIONS:
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
				else:
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", True, [(0.628838, 0.837541)]),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", "A-17316", True, None),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", True, [(0.297535, 0.837518)]),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", "A-17316", True, None),
		115: ("Spinner", "playfield.spinner", "used", False, "leaf", "5647-12693-24", True, [(0.933303, 0.505121)]),
		116: ("Not Fitted Upper Right Flipper Button", "internal.unfitted.flipper-button", "unused", True, "opto", None, True, None),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, "leaf", None, True, None),
		118: ("Not Fitted Upper Left Flipper Button", "internal.unfitted.flipper-button", "unused", True, "opto", None, True, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, keep_wiring, position) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") or role == "internal.unfitted.flipper-button" else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if address in {111, 113}:
			notes += (
				" PinMAME forces this end-of-stroke address every VBLANK: jyGameData's FLIP_SOL(FLIP_L) "
				"sets the lower-flipper FLIP_EOS bit, so core_updateSw recomputes it from core_getSol "
				"(the flipper hold coil state) plus CORE_FLIPSTROKETIME and writes it back into the "
				"matrix. A recreation must not drive it. Its normalized coordinate is the retained "
				"table's own flipper pivot center: the retained extraction contains no separate EOS "
				"contact object, so this is a documented projection onto the flipper assembly rather "
				"than a surveyed sensor position."
			)
		elif address in {116, 118}:
			notes += (
				" Junk Yard fits no upper flippers, so no physical upper-flipper button is installed (the "
				"Switch Locations page prints this position Not Used). jyGameData's FLIP_SW(FLIP_L | "
				"FLIP_U) includes the FLIP_U bit, so PinMAME's flipMask carries the upper-flipper button "
				"bit, but under LibPinMAME (g_fHandleKeyboard=0) the button bits are read straight from "
				"and written back to the matrix unchanged, so PinMAME publishes no meaningful runtime "
				"state at this address. Recorded unused."
			)
		elif availability == "unused":
			notes += (
				" Junk Yard fits no upper flippers: the Switch Locations page marks this position Not Used "
				"(both the assembly and switch part columns print NOT USED). jyGameData's FLIP_SOL(FLIP_L) "
				"sets no FLIP_EOS bit for the upper flippers, so this EOS address is dead and PinMAME never "
				"publishes state at it."
			)
		elif switch_type == "opto":
			notes += (
				" The switch matrix's Fliptronic block shades this position as an opto that is typically "
				"closed. WPC-95 reads the flipper column through WPC_FLIPPERSW95 with a hardware "
				"inversion, so the public switch state is already normalized."
			)
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
		}
		if keep_wiring:
			extra["wiring"] = {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			if normally_closed is not None:
				extra["normally_closed"] = bool(normally_closed)
		else:
			extra["normally_closed"] = bool(normally_closed)
			extra["spatial"] = (
				not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if role.endswith(".button")
				else located(f"switch.generic-{address}", "sensor", position, VPX_TABLE_SOURCE)
		)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				**extra,
			)
		)

	dip_labels = {n: f"CPU DIP {n} (country/option configuration bit)" for n in range(1, 9)}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				dip_labels[address],
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.dip", "value": str(address)},
					{"namespace": "manual.address", "value": f"SW{address}"},
				],
				physical={
					"location": "WPC-95 CPU board U27",
					"switch_type": "dip",
					"notes": (
						"WPC-95 CPU-board country/option configuration DIP bank. The retained manual's own "
						"front-matter DIP Switch Chart documents five country combinations (America, European, "
						"French, German, Spain) across SW1-SW8."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"

def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			if 17 <= address <= 20 or 22 <= address <= 28:
				kind = "flasher"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if address in {4, 8, 12, 13, 14}:
				notes = (
					f"Printed solenoid {address:02d} is NOT USED: the Solenoid/Flasher Table lists the row "
					"with a driver transistor and a drive wire color but a blank Voltage Connections, Drive "
					"Connections, and Part Number column, and the Solenoid/Flashlamp Locations page prints "
					f"item {address:02d} Not Used with a blank assembly number. Enumerated-but-unfitted; "
					"no physical device is created."
				)
			if kind == "flasher" and address in FLASHER_QTY:
				bulbs, quantity, playfield_emitters = FLASHER_QTY[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += " Only the playfield-visible bulb(s) have a playfield placement; the insert-panel/backbox bulb(s) have no coordinate."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the "
					"same circuits 29-32; the manual address is preserved as an alias."
				)
			if address in {33, 34, 35, 36}:
				notes += (
					" Printed upper-flipper circuit that is not fitted: the switch locations and flipper "
					"circuit rows both print NOT USED for the upper flipper positions, and jyGameData's "
					"FLIP_SOL(FLIP_L) never routes these four addresses through any flipper-coil path."
				)
			if address in SOLENOID_PROJECTIONS:
				notes += " " + SOLENOID_PROJECTIONS[address]
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-95 power driver board", "driver_transistor": wiring_data["driver_transistor"]}
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if address in {4, 8, 12, 13, 14} or address in {33, 34, 35, 36}:
				availability = "unused"
				extra["roles"] = ["internal.unused.wpc-output" if address >= 33 else "internal.unfitted"]
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				availability = "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 18:
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address == 15:
				pass  # hold-crane projection anchor sits below the playfield apron; spatial omitted
			elif address in SOLENOID_POSITIONS:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			elif address in SOLENOID_PROJECTIONS:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			elif availability != "unused":
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		record = {
			29: ("WPC State Channel 29", "used"),
			30: ("WPC State Channel 30", "used"),
			31: ("PinMAME Fast-Flip Game-On State", "used"),
			32: ("Unused WPC State Channel 32", "unused"),
			37: ("Unused WPC-95 LPDC Output 37", "unused"),
			38: ("Unused WPC-95 LPDC Output 38", "unused"),
			39: ("Unused WPC-95 LPDC Output 39", "unused"),
			40: ("Unused WPC-95 LPDC Output 40", "unused"),
			41: ("Unused WPC-95 LPDC Mirror 41", "unused"),
			42: ("Unused WPC-95 LPDC Mirror 42", "unused"),
			43: ("Unused WPC-95 LPDC Mirror 43", "unused"),
			44: ("Unused WPC-95 LPDC Mirror 44", "unused"),
			49: ("PinMAME Simulator Ball-Shooter Channel", "used"),
			50: ("Reserved WPC Output 50", "unused"),
		}[address]
		label, availability = record
		identifier = output_id(label)
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is a meaningful runtime state channel, not a Junk Yard playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is a meaningful runtime state channel, not a Junk Yard playfield device.",
			31: "PinMAME's synthetic game-on state. Junk Yard sets wpc_set_fastflip_addr(0x80), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero.",
			37: "Unused WPC-95 LPDC general-purpose output; Junk Yard has no DC-motor LPDC output.",
			38: "Unused WPC-95 LPDC general-purpose output; Junk Yard has no DC-motor LPDC output.",
			39: "Unused WPC-95 LPDC general-purpose output; Junk Yard has no DC-motor LPDC output.",
			40: "Unused WPC-95 LPDC general-purpose output; Junk Yard has no DC-motor LPDC output.",
			41: "Unused WPC-95 LPDC mirror of output 37; both the real output and its mirror are unpopulated.",
			42: "Unused WPC-95 LPDC mirror of output 38; both the real output and its mirror are unpopulated.",
			43: "Unused WPC-95 LPDC mirror of output 39; both the real output and its mirror are unpopulated.",
			44: "Unused WPC-95 LPDC mirror of output 40; both the real output and its mirror are unpopulated.",
			49: "PinMAME's simulator-only ball-shooter channel (sShooterRel), consumed by the built-in ball simulator; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary; jyGameData declares no custSol.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=virtual_aliases,
				roles=roles,
				physical={"notes": notes},
				spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS.get(address)
			unused = address in {56, 87}
			identifier = f"lamp.matrix-{address}"
			physical: dict[str, Any] = {"quantity": 2 if address in {67, 78} else 1}
			bulb = LAMP_BULB.get(address)
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address == 88:
				notes += " Cabinet button lamp inside the illuminated start button assembly, sharing its assembly part number with switch 13."
			if address in INSERT_PANEL_LAMPS:
				notes += " The Lamp Locations page footnotes this lamp as located on the insert panel; lamp 86 is also drawn on the playfield crane mechanism."
			if address not in LAMP_POSITIONS and not unused and address not in {81, 82, 83, 84, 85, 86, 87, 88}:
				notes += " No playfield Light object exists in the retained table for this address."
			physical["notes"] = notes

			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": {
					"board": "WPC-95 power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in INSERT_PANEL_LAMPS:
				availability = "used"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				position = LAMP_POSITIONS[address]
				extra["spatial"] = located(identifier, "emitter", position, VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					availability,
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items

def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, connections, transistor, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label})."
		extra: dict[str, Any] = {}
		if address in GI_POSITIONS:
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter "
				"coordinate come from the retained table's GI emitter collection for this string as bound by "
				"the retained script's UpdateGI dispatch (GI address 0 drives collection GIString1 plus the "
				"six bloom lights GI22-GI27; GI address 1 drives GIString2)."
			)
			if address == 0:
				notes += " GIString1 contains 22 named members (including the Light1-Light5/Light41 apron lights); all are included."
			extra["spatial"] = located(identifier, "emitter", GI_POSITIONS[address], VPX_TABLE_SOURCE)
			extra["physical"] = {"notes": notes, "quantity": len(GI_POSITIONS[address])}
		else:
			if address == 2:
				notes += (
					" Backbox insert-panel illumination behind the translite. The retained script's UpdateGI "
					"has a case 2 for this string, but its whole body is two commented-out VBScript lines "
					"('BackGlass Junk Yard logo On/Off'), so no address 0-4 outside 0/1 produces any visual "
					"effect; this string has no playfield coordinate."
				)
			elif address == 4:
				notes += (
					" Backbox insert-panel illumination that additionally feeds a cabinet bulb through J104. "
					"The retained script's UpdateGI handles only GI addresses 0-2, so this string has no "
					"playfield coordinate."
				)
			else:
				notes += (
					" Backbox insert-panel illumination behind the translite. The retained script's UpdateGI "
					"handles only GI addresses 0-2, so this string has no playfield coordinate."
				)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			extra["physical"] = {"notes": notes}
		extra["wiring"] = {
			"board": "WPC-95 power driver board",
			"control_connection": connections,
			"driver_transistor": transistor,
		}
		items.append(
			_device(
				identifier,
				label,
				"gi",
				"pinmame.output.gi",
				address,
				"used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.gi", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address + 1:02d}"},
				],
				**extra,
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
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier, label, kind, actuators, sensors, behavior, positions, *refs, assembly_part_number=None):
		record = {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [
				{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
				for position_id, position_label, position_sensors, description in positions
			]
		return record

	sw = lambda n: f"switch.matrix-{n}"
	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough")],
			[sw(31), sw(32), sw(33), sw(34), sw(35)],
			"Four balls rest on trough optos 32-35; the retained script's cvpmTrough helper (bsTrough) reads "
			"them as a plain switch array [32,33,34,35] and ejects the ball nearest the shooter lane through "
			"solenoid 9 (Trough), pulsing trough-eject opto 31 in the same SolTrough event. All five positions "
			"are printed optos that rest closed, normalized by PinMAME's column-3 inverted-switch mask bits.",
			[
				("ball-1", "Trough Ball 1 (eject position)", [sw(32)], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", [sw(33)], "Second trough position."),
				("ball-3", "Trough Ball 3", [sw(34)], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", [sw(35)], "Drain entrance."),
				("eject", "Trough eject", [sw(31)], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			[sw(18)],
			"The ball ejected from the trough rests on shooter-lane switch 18 and auto-plunger coil 1 launches "
			"it; the retained script's Autoplunger handler pulls back and fires the Auto_Plunger only when "
			"switch 18 is active.",
			[("shooter", "Ball in shooter lane", [sw(18)], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21022",
		),
		mechanism(
			"mechanism.crane",
			"Crane mechanism with wrecking ball",
			"motorized",
			[output_id("Power Crane"), output_id("Hold Crane")],
			[sw(15), sw(28), sw(44)],
			"Solenoid 3 (Power Crane) drives the crane arm that raises and swings the wrecking-ball head across "
			"the top of the playfield; solenoid 15 (Hold Crane) holds the mechanism against gravity. The "
			"retained script's SolPowerCrane/SolHoldCrane handlers steer the Wrecker ball along the crane track "
			"while switch 15 (Top Left Crane) and 44 (Past Crane) report the arm's positional limits and switch "
			"28 (Crane Down) reports the lowered position.",
			[
				("left", "Top Left Crane position", [sw(15)], "Crane head at the left stop."),
				("right", "Past Crane position", [sw(44)], "Crane head past the right stop."),
				("down", "Crane Down position", [sw(28)], "Crane head lowered."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21523",
		),
		mechanism(
			"mechanism.refrigerator-popper",
			"Refrigerator popper",
			"kicker",
			[output_id("Refrigerator Popper")],
			[sw(37), sw(36), sw(43)],
			"The retained script's second cvpmBallStack helper (bsFridgePopper) uses switch 37 as its entry "
			"ball-position switch and switches 36/43 as the Fridge ball-stack array; solenoid 2 fires the "
			"popper to eject a captured ball back to the playfield.",
			[
				("entry", "Ball in refrigerator popper", [sw(37)], "Popper entry position."),
				("stack-1", "Lock Up 2", [sw(36)], "Shared lock/scoop position."),
				("stack-2", "Lock Jam", [sw(43)], "Popper internal position."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21216",
		),
		mechanism(
			"mechanism.bus-diverter",
			"Bus ramp diverter",
			"diverter",
			[output_id("Bus Diverter")],
			[],
			"Solenoid 6 rotates a diverter flap (Sol6, a stopping wall/diverter object) that selects whether a "
			"ball entering the bus ramp lane continues to the top of the playfield or drops back; the retained "
			"script's BusDiverter handler sets Sol6.IsDropped accordingly. The manual documents no dedicated "
			"switch for this device.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-21409-1",
		),
		mechanism(
			"mechanism.dog",
			"Spike the dog mechanism",
			"motorized",
			[output_id("Move Dog")],
			[sw(74)],
			"Solenoid 16 (Move Dog) drives the dog-house spike arm; the retained script's SpikeBark/SpikeTimer "
			"handlers pulse the spike spike.transy up and down while switch 74 (Dog Entry) reports a ball in the "
			"dog-house entry scoop.",
			[("entry", "Ball in dog-house entry", [sw(74)], "Dog Entry switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21383",
		),
		mechanism(
			"mechanism.scoop",
			"Fork-lift scoop (up/down)",
			"kicker",
			[output_id("Scoop Down"), output_id("Scoop Up")],
			[sw(72), sw(73)],
			"The two-way fork-lift scoop at the center-right of the playfield lowers (solenoid 5, Scoop Down) "
			"and raises (solenoid 21, Scoop Up) to fling a ball from switch 73 (Scoop Made); the retained "
			"script's ScoopDown/ScoopUp handlers drive the fork-arm primitives and toggle switch 72 to report "
			"the scoop's own state.",
			[
				("made", "Ball in the scoop", [sw(73)], "Scoop Made switch."),
				("down", "Scoop lowered", [sw(72)], "State switch toggled by the ScoopDown handler."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-21220",
		),
		mechanism(
			"mechanism.toaster-gun",
			"Toaster gun and rebound",
			"other",
			[],
			[sw(11), sw(12)],
			"Toaster Gun (switch 11) and Rebound Switch (switch 12, part A-17794) form the left-side upper "
			"features; the retained script pulses switch 12 from both the Switch12 and Switch12a wall hit "
			"handlers.",
			[
				("gun", "Toaster Gun switch", [sw(11)], "Toaster-gun target."),
				("rebound", "Rebound Switch", [sw(12)], "Rebound switch (two positions, A-17794)."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-18530-6",
		),
		mechanism(
			"mechanism.car-targets",
			"Car drop-target bank",
			"other",
			[],
			[sw(46), sw(47), sw(48), sw(53), sw(54)],
			"Five standup targets (Car Target 1-5) sit at the top of the playfield above the crane track "
			"(SW-1A-210-1 through -5); they are hit targets, not a resettable drop bank.",
			[
				("car-1", "Car Target 1 (Left)", [sw(46)], "First car target."),
				("car-2", "Car Target 2", [sw(47)], "Second car target."),
				("car-3", "Car Target 3", [sw(48)], "Third car target."),
				("car-4", "Car Target 4", [sw(53)], "Fourth car target."),
				("car-5", "Car Target 5 (Right)", [sw(54)], "Fifth car target."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="SW-1A-210",
		),
		mechanism(
			"mechanism.three-banks",
			"Upper and lower three-bank target clusters",
			"other",
			[],
			[sw(56), sw(57), sw(58), sw(61), sw(62), sw(63), sw(64), sw(65), sw(66), sw(76), sw(77), sw(78)],
			"Four clusters of three standup targets each: Upper Right 3-Bank (61-63), Upper Left 3-Bank "
			"(64-66), Lower Left 3-Bank (56-58) and Right 3-Bank (76-78). All use part A-21349-1 (lower/right "
			"clusters) or A-21351-1..-6 (upper clusters).",
			[
				("ur-top", "Upper Right 3-Bank Top", [sw(63)], "Upper-right cluster top."),
				("ur-mid", "Upper Right 3-Bank Middle", [sw(62)], "Upper-right cluster middle."),
				("ur-bot", "Upper Right 3-Bank Bottom", [sw(61)], "Upper-right cluster bottom."),
				("ul-top", "Upper Left 3-Bank Top", [sw(66)], "Upper-left cluster top."),
				("ul-mid", "Upper Left 3-Bank Middle", [sw(65)], "Upper-left cluster middle."),
				("ul-bot", "Upper Left 3-Bank Bottom", [sw(64)], "Upper-left cluster bottom."),
				("ll-top", "Lower Left 3-Bank Top", [sw(58)], "Lower-left cluster top."),
				("ll-mid", "Lower Left 3-Bank Middle", [sw(57)], "Lower-left cluster middle."),
				("ll-bot", "Lower Left 3-Bank Bottom", [sw(56)], "Lower-left cluster bottom."),
				("r-top", "Right 3-Bank Top", [sw(78)], "Right cluster top."),
				("r-mid", "Right 3-Bank Middle", [sw(77)], "Right cluster middle."),
				("r-bot", "Right 3-Bank Bottom", [sw(76)], "Right cluster bottom."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-21349-1 / A-21351",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			[sw(51), sw(52)],
			"Each slingshot assembly has a combined kick/score switch (SW-1A-204 kick with SW-1A-205 score); "
			"the retained script's LeftSlingShot_Slingshot/RightSlingShot_Slingshot handlers pulse switches 51 "
			"and 52 while coils 10/11 articulate the arms.",
			[
				("left", "Left slingshot", [sw(51)], "Left slingshot score switch."),
				("right", "Right slingshot", [sw(52)], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9362-R-3",
		),
		mechanism(
			"mechanism.spinner",
			"Spinner",
			"other",
			[],
			["switch.generic-115"],
			"The Fliptronic F5 position is a playfield spinner (part 5647-12693-24), not a flipper contact; the "
			"retained script's Switch115_Spin handler pulses switch 115 on each revolution.",
			[("spinner", "Spinner", ["switch.generic-115"], "Spinner switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="5647-12693-24",
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"), output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold")],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: "
			"the ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops "
			"to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. Printed "
			"circuits 29/30 (Lwr Rt Power/Hold) and 31/32 (Lwr Lt Power/Hold) map to public addresses 45-48.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15849-R-2 right with A-15849-L-2 left",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough"),
			"destination": "switch.matrix-31",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.scoop-down-sets-scoop-down-switch",
			"kind": "direct",
			"source": output_id("Scoop Down"),
			"destination": "switch.matrix-72",
			"provenance": provenance(VPX_SCRIPT_SOURCE),
		},
		{
			"id": "relationship.scoop-up-clears-scoop-down-switch",
			"kind": "direct",
			"source": output_id("Scoop Up"),
			"destination": "switch.matrix-72",
			"provenance": provenance(VPX_SCRIPT_SOURCE),
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
			"id": "williams.junkyard.1996",
			"name": "Junk Yard",
			"manufacturer": "Williams",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 4014,
			"model_number": "16-50052-101",
			"playfield": {
				"width": TABLE_WIDTH,
				"height": TABLE_HEIGHT,
				"units": "vpx",
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
			"opdb_id": "GRLlj-MQZN8",
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-95",
			"hardware_generation": "0x80",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/junkyard-1996.md", "status": "complete"},
		"conflicts": [
			{
				"id": "conflict.junkyard.past-crane-opto-not-normalized",
				"status": "unresolved",
				"description": (
					"Switch 44 (Past Crane) is opto-constructed per the manual's Switch Locations parts list "
					"(2-35), which prints an A-16908 (LED) / A-16909 (PHOTO TRANS) opto pair for item 44 as it "
					"does for items 41-43 -- but pinned PinMAME's jyGameData inverted-switch mask "
					"({0x00,0x00,0x00,0x7f,0x07,0x00,0x00,...}) covers column 4 rows 1-3 (0x07, switches 41-43) "
					"and leaves row 4 (switch 44) uninverted. The other ten opto addresses (31-37, 41-43) all "
					"agree between the manual and the emulator; this is the sole polarity disagreement, of the "
					"same family as Monster Bash's Dracula-position optos and Indiana Jones's captive-ball opto. "
					"Resolution path: a LibPinMAME gameplay-harness trace of a legal jy_11/jy_12 ROM observing "
					"the public idle state of switch 44 and its transitions as the crane passes, or a later "
					"corrected upstream mask."
				),
				"path": "evidence/excerpts/williams.junkyard.1996/switch-locations.md",
				"source_refs": ["manual.williams.junkyard.1996", "pinmame.core.8371478a7640"],
			},
		],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Junk Yard device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	for device in definition["inputs"]:
		spatial = device.get("spatial")
		if spatial is not None and spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"Switch 44 (Past Crane) polarity remains unresolved and the crane-related sensors carry "
			"documented projections rather than surveyed coordinates; several GI and flasher devices sit on "
			"backbox/insert-panel circuits with no playfield placement. See the promotion decision.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": TABLE_WIDTH, "bottom": TABLE_HEIGHT},
			"x": f"x/{TABLE_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{TABLE_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/junkyard-1996/extracted-vpxtool.manifest.json",
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
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"unresolved_input_addresses": sorted(unresolved_inputs),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		] + [
			{"group": "pinmame.input.switch", "address": 111, "reason": "Lower Right Flipper EOS projected onto the retained table's own flipper pivot center; no separate EOS contact object exists in the extraction."},
			{"group": "pinmame.input.switch", "address": 113, "reason": "Lower Left Flipper EOS projected onto the retained table's own flipper pivot center; no separate EOS contact object exists in the extraction."},
		] + [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.junkyard.1996/",
		},
		"excluded_object_classes": [
			"Switch 42's only retained trigger object sits below the playfield apron (y > 1) and is a modelling artifact of the hidden sewer sink; it is left unresolved rather than promoted to a playfield coordinate.",
			"Flasher 18 (Window Shop) and flashers 20/23/24/26 second inset bulbs are backbox/insert-panel circuits with no playfield placement.",
		],
		"unresolved": [
			{"group": "pinmame.input.switch", "address": 44, "reason": "opto polarity not normalized by PinMAME; see conflict.junkyard.past-crane-opto-not-normalized"},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Junk Yard (Williams, 1996) spatial review",
		"",
		f"Status: {report['status']} spatial-report format; spatial coverage itself is `candidate`. The "
		"definition remains `partial` at "
		"`machines/partial/williams/junkyard-1996.json` because the past-crane opto polarity conflict is "
		"unresolved and several mechanism-internal sensors carry documented projections.",
		"",
		"The matching source is the retained known-working `Junk Yard (Williams 1996).vpx` (v1.3 by "
		f"mfuegemann) at SHA-256 `{TABLE_SHA256}`. The retained `vpxtool` extraction produced the embedded "
		f"script at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. "
		f"Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and y/2162 "
		"rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual (146 pages, 16-50052-101 FINAL) carries a usable OCR text layer but every "
		"printed table used here was read from 200 dpi renders and transcribed (by a vision-capable model "
		"worker) into `evidence/excerpts/williams.junkyard.1996/`, cross-checked across the repeated copies.",
		"- The trough and lock/scoop multi-position sensors have no dedicated playfield trigger objects "
		"because the retained script's cvpmBallStack helpers model ball sensing purely as an internal switch "
		"array. Those addresses are explicit documented projections onto the real kicker object that carries "
		"the mechanism's exit/entry point.",
		"- Switch 44 (Past Crane) is the single polarity disagreement: opto-constructed per the manual but "
		"not normalized by jyGameData's mask. Recorded as a first-class unresolved conflict.",
		"- GI addresses 2-4 and flasher/insert-panel bulbs are backbox/cabinet circuits with controlled "
		"`not_applicable` spatial records.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable`.",
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved input addresses: {report['unresolved_input_addresses']}",
		"",
		"## Promotion decision",
		"",
		"Junk Yard is a deterministic partial. The past-crane opto polarity question and the trough/crane "
		"projections must be resolved before promotion; a LibPinMAME harness trace of the public idle state "
		"of switch 44 on a legal jy_11/jy_12 ROM is the concrete next step.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Six manual transcriptions (switch matrix, switch locations, lamp matrix, lamp locations, "
		"solenoid/flasher table, solenoid locations) under `evidence/excerpts/williams.junkyard.1996/`.",
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
	stale_author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready.exists():
		stale_author_ready.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	stale_author_ready_path = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale_author_ready_path.exists():
		raise RuntimeError(f"Stale Junk Yard author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Junk Yard definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Junk Yard seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Junk Yard definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Junk Yard seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Junk Yard spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Junk Yard spatial review drifted from its deterministic curator: {markdown_path}")
	print("Junk Yard definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Junk Yard extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Junk Yard retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
