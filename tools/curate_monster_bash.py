"""Curate the physical Williams Monster Bash (1998) machine definition.

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
# Demoted 2026-08-06: switches 74-78 are physically normally-closed optos that pinned PinMAME does
# not normalize (conflict.dracula-position-opto-not-normalized, unresolved), so the record lives
# under machines/partial until a harness trace settles their idle public state.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/monster-bash-1998.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/monster-bash-1998.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/monster-bash-1998.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/monster-bash-1998.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/monster-bash-1998.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.williams.monster-bash.1998"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.monster-bash.1998"
VPX_TABLE_SOURCE = "vpx-table.mb-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.mb-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.mb-vpw-1-0"

TABLE_SHA256 = "bef48b75b072c3fc8b4803639cc65f54144db6ff7e9476f6ea6b1fc23bc68c8d"
SCRIPT_SHA256 = "b043d07c74693ce5c713a9edc1529413f3c2ec4420b63488085cd45e4fe413e8"
MANUAL_SHA256 = "b0c1027e557c7f5a1b3efa7954a88c6b7aa5d993a172c28a08f9445f2a111fc3"
MANUAL_TRANSCRIPTION_SHA256 = "a5d8d4a1936fe379ed855227a1d73d3a26d95438f75e0c60f3b11e1080d84bfc"

EXTRACTION_RELATIVE_PATH = Path("williams/monster-bash-1998/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/monster-bash-1998/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "1361d166539823e12aedc983e95c0d1b0789dab291de4fd9a23f9aa830ec57ea"
EXTRACTION_FILE_COUNT = 2153
EXTRACTION_TOTAL_BYTES = 199010658

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

DRIVER_IDS = ("mb_05", "mb_10", "mb_106", "mb_106b")
DRIVER_COMPATIBILITY = {
	"mb_05": (
		"identical",
		"Williams 0.5 prototype game ROM for the same physical Monster Bash machine; the switch "
		"matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged.",
	),
	"mb_10": (
		"identical",
		"Williams production 1.0 game ROM shipped with the physical machine.",
	),
	"mb_106": (
		"identical",
		"Williams 1.06 game ROM; a later firmware revision of the same physical machine with no "
		"controller-address or playfield change.",
	),
	"mb_106b": (
		"identical",
		"Williams 1.06B game ROM. This is the driver the retained known-working VPW table binds to "
		"(cGameName = \"mb_106b\"), and it drives the identical I/O inventory as 1.0.",
	),
}

# --- Printed switch matrix (manual page 2-48/2-49 parts list, 2-51 wiring).
SWITCH_LABELS = {
	11: "Launch Button", 12: "Dracula Standup Top", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Dracula Standup Bottom", 16: "Left Outlane", 17: "Right Return", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Tomb Treasure", 24: "Always Closed",
	25: "Dracula Target", 26: "Left Return", 27: "Right Outlane", 28: "Left Eject",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Right Popper",
	42: "Left Flipper Opto", 43: "Right Flipper Opto", 44: "Left Blue Target",
	45: "Center Blue Target", 46: "Right Blue Target", 47: "Left Flipper Proximity Sensor",
	48: "Right Flipper Proximity Sensor",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Left Jet Bumper", 54: "Right Jet Bumper",
	55: "Bottom Jet Bumper", 56: "Left Top Lane", 57: "Center Top Lane", 58: "Right Top Lane",
	61: "Left Loop Low", 62: "Left Loop High", 63: "Right Loop Low", 64: "Right Loop High",
	65: "Center Loop", 66: "Left Ramp Enter", 67: "Left Ramp Exit", 68: "Center Ramp Enter",
	71: "Right Ramp Enter", 72: "Right Ramp Exit", 73: "Right Ramp Lock",
	74: "Dracula Position 5", 75: "Dracula Position 4", 76: "Dracula Position 3",
	77: "Dracula Position 2", 78: "Dracula Position 1",
	81: "Up/Down Bank Up", 82: "Up/Down Bank Down", 83: "Frank Table Down", 84: "Frank Table Up",
	85: "Left Up/Down Bank Target", 86: "Right Up/Down Bank Target", 87: "Frank Hit",
}
# Printed matrix positions marked "NOT USED" on both the parts list (2-48/49) and the shaded
# wiring page (2-51).
UNUSED_MATRIX_ADDRESSES = {37, 38, 41, 88}
# Every switch shaded "OPTO, TYPICALLY CLOSED" on the printed matrix page (2-51): trough/popper
# optos, flipper optos, and Dracula position optos 74-78 (printed on the A-21402 Defender Switch
# Board Assembly with a blank switch part number). All thirteen are physically normally-closed.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 42, 43, 74, 75, 76, 77, 78}
# PinMAME's mbGameData inverted-switch mask covers only these eight (column 3 = 0x3f bits 0-5,
# column 4 = 0x06 bits 1-2); column 7, which carries 74-78, is 0x00. Those five optos are printed
# normally-closed but PinMAME does not normalize them -- see conflict.dracula-position-opto-not-normalized.
PINMAME_NORMALIZED_OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 42, 43}
# vpmTimer.PulseSw / momentary-target callers in the retained VPW script.
PULSED_SWITCHES = {25, 31, 51, 52, 53, 54, 55, 68, 71, 117}

SWITCH_TYPES = {
	11: "button", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch",
	23: "microswitch", 24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	28: "microswitch", 44: "microswitch", 45: "microswitch", 46: "microswitch",
	47: "other", 48: "other", 51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf", 55: "leaf",
	56: "microswitch", 57: "microswitch", 58: "microswitch", 61: "microswitch",
	62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch",
	66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "microswitch",
	72: "microswitch", 73: "microswitch", 74: "opto", 75: "opto",
	76: "opto", 77: "opto", 78: "opto", 81: "microswitch",
	82: "microswitch", 83: "microswitch", 84: "microswitch", 85: "microswitch",
	86: "microswitch", 87: "microswitch",
}

# address -> (assembly_part_number, part_number), transcribed verbatim from printed 2-48/49.
SWITCH_PARTS = {
	11: ("20-9663-B-4", None), 12: ("A-20499-9", None), 13: ("20-9663-16", None),
	14: (None, "04-10346"), 15: ("A-20499-9", None),
	16: ("A-17813", "5647-12693-19"), 17: ("A-17813", "5647-12693-19"),
	18: ("A-17791", "5467-12693-32"), 21: ("A-17238", None), 22: (None, "5643-09268-00"),
	23: ("A-18019-15", None), 24: (None, "5643-15190-00"), 25: ("A-22411", None),
	26: ("A-17813", "5647-12693-19"), 27: ("A-17813", "5647-12693-19"),
	28: (None, "5647-12693-66"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16908 LED with A-16909 photo transistor", None),
	42: ("A-16908 LED with A-16909 photo transistor", None),
	43: ("A-16908 LED with A-16909 photo transistor", None),
	44: ("A-18530-1", None), 45: ("A-18530-1", None), 46: ("A-22414-1", None),
	47: ("A-17064", None), 48: ("A-17064", None),
	51: ("A-17801", "A-17800 kick with A-17794 score"),
	52: ("A-17801", "A-17800 kick with A-17794 score"),
	53: ("A-12030-3", "A-16443-1"), 54: ("A-12030-3", "A-16443-1"), 55: ("A-12030-3", "A-16443-1"),
	56: ("A-17813", "5647-12693-19"), 57: ("A-17813", "5647-12693-19"), 58: ("A-17813", "5647-12693-19"),
	61: ("A-17813", "5647-12693-19"), 62: ("A-17813", "5647-12693-19"),
	63: ("A-22481", "5647-12693-36"), 64: ("A-17813", "5647-12693-19"), 65: ("A-17813", "5647-12693-19"),
	66: ("A-17813", "5647-12693-19"), 67: (None, "5647-12693-13"),
	68: ("A-22437", "5647-12693-24"), 71: ("A-22437", "5647-12693-24"),
	72: (None, "5647-12693-24"), 73: (None, "5647-12693-21"),
	74: ("A-21402", None), 75: ("A-21402", None), 76: ("A-21402", None), 77: ("A-21402", None),
	78: ("A-21402", None),
	81: (None, "5647-12693-36"), 82: (None, "5647-12693-36"),
	83: (None, "5647-12693-11"), 84: (None, "5647-12693-11"),
	85: (None, "SW-1A-217-4"), 86: (None, "SW-1A-217-4"),
	87: (None, "5647-12693-69"),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-White", "J206-4", "U20-15"),
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
# Fliptronic F1-F8 wiring, printed 2-51. Identical column/connector layout to the other retained
# WPC-95 CPU board.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed solenoid/flasher table (manual pages 2-46 locations, 2-53 wiring).
SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Bride Post", 3: "Mummy Coffin", 5: "Left Gate", 6: "Right Gate",
	8: "Ramp Lock Post", 9: "Trough Eject", 10: "Left Slingshot", 11: "Right Slingshot",
	12: "Left Jet Bumper", 13: "Right Jet Bumper", 14: "Bottom Jet Bumper", 15: "Left Eject",
	16: "Right Popper", 17: "Wolfman Flashers", 18: "Bride Flasher",
	19: "Frankenstein Flashers", 20: "Dracula Coffin Flasher", 21: "Creature Flashers",
	22: "Jets/Mummy Flashers", 23: "Right Popper Flasher", 24: "Frank Arrow Flasher",
	25: "Monsters of Rock Flasher", 26: "Wolfman Loop Flasher", 27: "Frank Motor",
	28: "Up/Down Bank Motor", 37: "Dracula Motor Forward", 38: "Dracula Motor Backward",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {
	4: "Not Used Solenoid Position 4",
	7: "Not Used Solenoid Position 7",
	33: "Not Used Upper Right Flipper Power",
	34: "Not Used Upper Right Flipper Hold",
	35: "Not Used Upper Left Flipper Power",
	36: "Not Used Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	39: "Unused WPC-95 LPDC Output 39",
	40: "Unused WPC-95 LPDC Output 40",
	41: "Dracula Motor Forward LPDC Mirror",
	42: "Dracula Motor Backward LPDC Mirror",
	43: "Unused WPC-95 LPDC Mirror 43",
	44: "Unused WPC-95 LPDC Mirror 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# Manual solenoid/flasher table addresses that differ from the PinMAME public address.
MANUAL_SOLENOID_ALIASES = {41: "37", 42: "38", 45: "29", 46: "30", 47: "31", 48: "32"}

# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(control_connection="J116-1", driver_transistor="Q72", power_connection="J133-2", part_number="AE-24-900", printed_type="High Power"),
	2: dict(control_connection="J116-2", driver_transistor="Q68", power_connection="J133-2", part_number="AE-26-1500", printed_type="High Power"),
	3: dict(control_connection="J116-4", driver_transistor="Q71", power_connection="J133-2", part_number="AE-27-1200", printed_type="High Power"),
	4: dict(driver_transistor="Q67", printed_type="High Power"),
	5: dict(control_connection="J116-6", driver_transistor="Q70", power_connection="J133-2", part_number="A-14406", printed_type="High Power"),
	6: dict(control_connection="J116-7", driver_transistor="Q66", power_connection="J133-2", part_number="A-14406", printed_type="High Power"),
	7: dict(driver_transistor="Q69", printed_type="High Power"),
	8: dict(control_connection="J116-9", driver_transistor="Q65", power_connection="J133-2", part_number="AE-27-1200", printed_type="High Power"),
	9: dict(control_connection="J113-1", driver_transistor="Q44", power_connection="J133-3", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(control_connection="J113-3", driver_transistor="Q48", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(control_connection="J113-4", driver_transistor="Q43", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(control_connection="J113-5", driver_transistor="Q47", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J113-6", driver_transistor="Q42", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J113-7", driver_transistor="Q46", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J113-8", driver_transistor="Q41", power_connection="J133-3", part_number="AE-30-2000", printed_type="Low Power"),
	16: dict(control_connection="J113-9", driver_transistor="Q45", power_connection="J133-3", part_number="AE-25-1000", printed_type="Low Power"),
	17: dict(control_connection="J111-1", driver_transistor="Q28", power_connection="J133-6", printed_type="Flasher"),
	18: dict(control_connection="J111-2", driver_transistor="Q32", power_connection="J133-6", printed_type="Flasher"),
	19: dict(control_connection="J111-3", driver_transistor="Q27", power_connection="J133-6", printed_type="Flasher"),
	20: dict(control_connection="J111-4", driver_transistor="Q31", power_connection="J133-6", printed_type="Flasher"),
	21: dict(control_connection="J111-5", driver_transistor="Q26", power_connection="J133-6", printed_type="Flasher"),
	22: dict(control_connection="J111-6", driver_transistor="Q30", power_connection="J133-6", printed_type="Flasher"),
	23: dict(control_connection="J111-7", driver_transistor="Q25", power_connection="J133-6", printed_type="Flasher"),
	24: dict(control_connection="J111-8", driver_transistor="Q29", power_connection="J133-6", printed_type="Flasher"),
	25: dict(control_connection="J109-1", driver_transistor="Q16", power_connection="J133-6", printed_type="Gen. Purpose"),
	26: dict(control_connection="J109-2", driver_transistor="Q15", power_connection="J133-6", printed_type="Gen. Purpose"),
	27: dict(control_connection="J109-3", driver_transistor="Q14", power_connection="J140-2", part_number="14-8015", printed_type="Gen. Purpose"),
	28: dict(control_connection="J109-4", driver_transistor="Q13", power_connection="J140-2", part_number="14-8015", printed_type="Gen. Purpose"),
	33: dict(control_connection="J120-6", driver_transistor="Q84", power_connection="J119-6", printed_type="Fliptronic power"),
	34: dict(control_connection="J120-4", driver_transistor="Q86", power_connection="J119-6", printed_type="Fliptronic hold"),
	35: dict(control_connection="J120-3", driver_transistor="Q81", power_connection="J119-8", printed_type="Fliptronic power"),
	36: dict(control_connection="J120-1", driver_transistor="Q83", power_connection="J119-8", printed_type="Fliptronic hold"),
	37: dict(control_connection="J110-1", driver_transistor="U3A and U3B", power_connection="J141-2", part_number="14-8034", printed_type="Low Power motor"),
	38: dict(control_connection="J110-3", driver_transistor="U3C and U3D", power_connection="J141-2", part_number="14-8034", printed_type="Low Power motor"),
	45: dict(control_connection="J120-13", driver_transistor="Q90", power_connection="J119-1", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(control_connection="J120-11", driver_transistor="Q92", power_connection="J119-1", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(control_connection="J120-9", driver_transistor="Q87", power_connection="J119-4", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(control_connection="J120-7", driver_transistor="Q89", power_connection="J119-4", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "YEL-GRN", 46: "ORG-GRN", 47: "YEL-BLU", 48: "ORG-BLU", 33: "YEL-VIO", 34: "ORG-VIO", 35: "YEL-GRY", 36: "ORG-GRY"}

SOLENOID_ASSEMBLIES = {
	1: "A-22429-1", 2: "A-22425", 3: "A-22302", 5: "A-17796", 6: "A-17796",
	8: "A-22293", 9: "A-19963", 10: "A-22207-2", 11: "A-22206-2", 12: "A-22205-2",
	13: "A-22205-2", 14: "A-22205-2", 15: "A-22449", 16: "A-22266",
	17: "A-17802", 18: "A-17983", 19: "04-10091.1", 20: "A-17983", 21: "A-17802",
	22: "A-17802", 25: "A-17802", 26: "A-17802", 27: "A-22404", 28: "A-22404",
	37: "A-22292", 38: "A-22292", 45: "A-22603-R", 46: "A-22603-R",
	47: "A-15849-L-2", 48: "A-15849-L-2",
}
# Retained VPW script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "AutoPlunger (Plunger.Fire)", 2: "SolBride", 3: "SolMummy",
	5: 'vpmSolGate LGate,false,', 6: 'vpmSolGate Rgate,false,', 8: "SolLockPost",
	9: "RandomSoundBallRelease sw32 with vpmTimer.PulseSw 31", 10: "LeftSlingShot_Slingshot",
	11: "RightSlingShot_Slingshot", 12: "Bumper1_Hit", 13: "Bumper2_Hit", 14: "Bumper3_Hit",
	15: "SolCallback(15)", 16: "SolCallback(16)",
	17: "SolMod17", 18: "SolMod18", 19: "SolMod19", 20: "SolMod20", 21: "SolMod21",
	22: "SolMod22", 23: "SolMod23", 24: "SolMod24", 25: "SolMod25", 26: "SolMod26",
	27: "FrankMove timer", 28: "BankMove timer",
	37: "Drac forward drive (mirrored at public 41)", 38: "Drac backward drive (mirrored at public 42)",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
}

FLASHER_BULBS = {
	17: ("#906 (2) on the back panel and #906 (1) on the insert panel", 3, 0),
	18: ("#89 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	19: ("#906 (2) on the playfield and #906 (1) on the insert panel", 3, 2),
	20: ("#89 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	21: ("#906 (2), both on the playfield", 2, 2),
	22: ("#906 (2) on the playfield and #906 (1) on the insert panel", 3, 2),
	23: ("#906 (1) on the playfield", 1, 1),
	24: ("#906 (1) on the playfield", 1, 1),
	25: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	26: ("#906 (2), both on the playfield", 2, 2),
}

# --- Printed lamp matrix (manual page 2-44 locations, 2-52 wiring). First digit is the column.
LAMP_LABELS = {
	11: "Monster Mosh Pit", 12: "Half Moon", 13: "Frankenstein Arrow", 14: "Drac-Attack",
	15: "Extra Ball", 16: "Monsters of Rock", 17: "Monster Bash", 18: "Mummy Mayhem",
	21: "Right Ramp Arrow", 22: "Rock C.D.", 23: "Right Return", 24: "Full Moon Fever",
	25: "Right Gargle", 26: "Right Warm Up", 27: "Right Primp", 28: "Right Loop Arrow",
	31: "Quarter Moon", 32: "Left Blue Target", 33: "Tomb Treasure", 34: "Dracula Standup Top",
	35: "Right Top Lane", 36: "Middle Top Lane", 37: "Left Top Lane", 38: "Dracula Standup Bottom",
	41: "Left Return", 42: "Left Outlane", 43: "Three-Quarter Moon", 44: "Right Blue Target",
	45: "Left Ramp Arrow", 46: "Left Primp", 47: "Left Warm Up", 48: "Left Gargle",
	51: "Guitar", 52: "Drums", 53: "Bass Guitar", 54: "Keyboard", 55: "Microphone",
	56: "Saxophone", 57: "Center Loop Arrow 3", 58: "Center Blue Target",
	61: "Creature", 62: "Bride", 63: "Frankenstein", 64: "Mummy", 65: "Wolfman", 66: "Dracula",
	67: "Right Outlane", 68: "Shoot Again",
	71: "Left Frankenstein Arm", 72: "Left Frankenstein Leg", 73: "Frankenstein Torso",
	74: "Frankenstein Head", 75: "Right Frankenstein Leg", 76: "Right Frankenstein Arm",
	77: "Left Loop Arrow",
	78: "Not Used",
	81: "Muck", 82: "Seaweed", 83: "Algae", 84: "Pond Scum",
	85: "Center Loop Arrow 2", 86: "Center Loop Arrow 1", 87: "Launch Button", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("04-12334", "#555"), 12: ("04-12334", "#555"), 13: ("04-12334", "#555"),
	14: ("04-12334", "#555"), 15: ("04-12334", "#555"), 16: ("04-12334", "#555"),
	17: ("04-12334", "#555"), 18: ("04-12334", "#555"),
	21: ("04-12334", "#555"), 22: ("A-17807", "#44"), 23: ("A-17835", "#44"),
	24: ("04-12334", "#555"), 25: ("04-12334", "#555"), 26: ("04-12334", "#555"),
	27: ("04-12334", "#555"), 28: ("A-17835", "#44"),
	31: ("04-12334", "#555"), 32: ("A-17835", "#44"), 33: ("A-17835", "#44"),
	34: ("04-12334", "#555"), 35: ("04-12332", "#555"), 36: ("04-12332", "#555"),
	37: ("04-12332", "#555"), 38: ("04-12334", "#555"),
	41: ("A-17835", "#44"), 42: ("A-17807", "#44"), 43: ("04-12334", "#555"),
	44: ("A-17835", "#44"), 45: ("04-12338", "#555"), 46: ("04-12338", "#555"),
	47: ("04-12338", "#555"), 48: ("04-12338", "#555"),
	51: ("04-12336", "#555"), 52: ("04-12336", "#555"), 53: ("04-12336", "#555"),
	54: ("04-12336", "#555"), 55: ("04-12336", "#555"), 56: ("04-12336", "#555"),
	57: ("A-17807", "#44"), 58: ("A-17807", "#44"),
	61: ("04-12335", "#555"), 62: ("04-12335", "#555"), 63: ("04-12335", "#555"),
	64: ("04-12335", "#555"), 65: ("04-12335", "#555"), 66: ("04-12335", "#555"),
	67: ("A-17807", "#44"), 68: ("A-17807", "#44"),
	71: ("04-12337", "#555"), 72: ("04-12337", "#555"), 73: ("04-12337", "#555"),
	74: ("04-12337", "#555"), 75: ("04-12337", "#555"), 76: ("04-12337", "#555"),
	77: ("A-17807", "#44"), 78: (None, None),
	81: ("04-12339", "#555"), 82: ("04-12339", "#555"), 83: ("04-12339", "#555"),
	84: ("04-12339", "#555"), 85: ("A-17835", "#44"), 86: ("A-17835", "#44"),
	87: ("20-9663-B-4", None), 88: ("20-9663-16", None),
}
LAMP_QUANTITIES = {12: 2, 24: 2, 31: 2, 43: 2}
# Typographic slips on the lamp-matrix page (2-52) against the authoritative parts list (2-44).
LAMP_MATRIX_PAGE_TYPOS = {
	14: "DRAC-ATTTACK", 31: "QUARTER MOOM (2)", 43: "THREE-QUARTERS MOON (2)", 48: "LEFT GARGOYLE",
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
# Two co-located Light objects stacked purely for brightness; the primary object is used and the
# duplicate is documented render doubling (l<nn>a / l<nn>2 style pairs).
LAMP_RENDER_DOUBLES = {11, 57, 61, 62, 63, 64, 65, 66, 81, 82, 83, 84, 85, 86}

GI_STRINGS = {
	0: ("Bottom Playfield", "J105-1", "Q5", "J105-7", "#44"),
	1: ("Top Right Playfield", "J105-2", "Q4", "J105-8", "#44"),
	2: ("Top Left Playfield", "J105-3", "Q3", "J105-9", "#44"),
	3: ("Top Insert Panel", "J106-5", "Q2", "J106-10", "#555"),
	4: ("Bottom Insert Panel", "J106-6 and J104-3", "Q1", "J106-11 and J104-1", "#555"),
}

# --- Normalized playfield coordinates derived from the retained VPWmod v1.0 extraction
# (x/952, y/2162; vpx-geometry.txt and the GIbot/GITopRight/GITopLeft/GIbumpers collections).
SWITCH_POSITIONS = {
	12: [(0.79339, 0.546718)], 15: [(0.80176, 0.577485)], 16: [(0.056163, 0.792569)],
	17: [(0.781825, 0.734693)], 18: [(0.940212, 0.888177)], 23: [(0.568145, 0.219875)],
	25: [(0.563025, 0.498711)], 26: [(0.130588, 0.735344)], 27: [(0.854191, 0.791607)],
	28: [(0.055721, 0.438299)],
	31: [(0.824045, 0.878631)], 32: [(0.824045, 0.878631)], 33: [(0.765591, 0.89311)],
	34: [(0.708674, 0.908373)], 35: [(0.47697, 0.965135)], 36: [(0.615801, 0.327809)],
	42: [(0.198164, 0.785796)], 43: [(0.717155, 0.785218)],
	44: [(0.191493, 0.382958)], 45: [(0.275835, 0.281448)], 46: [(0.440766, 0.30976)],
	47: [(0.336426, 0.834122)], 48: [(0.573876, 0.834396)],
	51: [(0.231092, 0.732499)], 52: [(0.680999, 0.732088)],
	53: [(0.59731, 0.185911)], 54: [(0.806414, 0.194469)], 55: [(0.653701, 0.270982)],
	56: [(0.589688, 0.102685)], 57: [(0.683217, 0.11114)], 58: [(0.777298, 0.11892)],
	61: [(0.07216, 0.262182)], 62: [(0.090386, 0.085131)], 63: [(0.817496, 0.379136)],
	64: [(0.938473, 0.135431)], 65: [(0.464097, 0.099835)], 66: [(0.117182, 0.13618)],
	67: [(0.144047, 0.340962)], 68: [(0.335628, 0.193648)],
	71: [(0.769069, 0.301429)], 72: [(0.683029, 0.215406)], 73: [(0.92034, 0.559596)],
	74: [(0.563025, 0.498711)], 75: [(0.563025, 0.498711)], 76: [(0.563025, 0.498711)],
	77: [(0.563025, 0.498711)], 78: [(0.563025, 0.498711)],
	81: [(0.35637, 0.310761)], 82: [(0.35637, 0.310761)], 83: [(0.41725, 0.340541)],
	84: [(0.41725, 0.340541)],
	85: [(0.323708, 0.308058)], 86: [(0.387755, 0.303073)], 87: [(0.364792, 0.324425)],
}
SWITCH_PROJECTIONS = {
	25: "Projected onto the rotating Dracula figure (Primitive Drac, table object center): DracTargets_Hit fires public switch 25 from a 47-segment target-wall ring that surrounds Drac and only one segment is active at a time (indexed from Drac.RotZ), so there is no single fixed target object.",
	31: "Projected onto the trough Ball 1 kicker position (sw32): the retained script's ball-release handler kicks the ball resting on switch 32 and pulses switch 31 (RandomSoundBallRelease sw32: vpmTimer.PulseSw 31) in the same event, and the manual switch-location map places the trough-eject opto immediately outboard of Trough Ball 1.",
	74: "Projected onto the rotating Dracula figure (Primitive Drac, table object center): the five position optos 74-78 are printed on the A-21402 Defender Switch Board Assembly inside the Dracula mechanism and PinMAME's mb_mech reads them from a single 90-step motor-position counter, not five separate playfield objects.",
	75: "Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.",
	76: "Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.",
	77: "Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.",
	78: "Projected onto the rotating Dracula figure (Primitive Drac, table object center); see switch 74.",
	81: "Projected onto the Up/Down Bank target assembly (Primitive frankytargets, table object center): the retained script sets public switches 81/82 directly from frankytargets.z threshold crossings rather than from a separate playfield sensor object.",
	82: "Projected onto the Up/Down Bank target assembly (Primitive frankytargets, table object center); see switch 81.",
	83: "Projected onto the Frankenstein figure (Primitive franky, table object center): the retained script sets public switches 83/84 directly from franky.rotx threshold crossings rather than from a separate playfield sensor object.",
	84: "Projected onto the Frankenstein figure (Primitive franky, table object center); see switch 83.",
	87: "Projected onto the centroid of the retained table's fhitwall collision wall, the hit surface raised while the Frankenstein figure is in striking position (public switch 87 is set from franky.rotx thresholds in the same handlers as switches 83/84, not from a Hit event on a fixed object).",
}

SOLENOID_POSITIONS = {
	1: [(0.940964, 0.940452)], 2: [(0.292819, 0.087459)], 3: [(0.788657, 0.096)],
	5: [(0.52882, 0.042622)], 6: [(0.853242, 0.083662)], 8: [(0.880777, 0.59052)],
	9: [(0.824045, 0.878631)], 10: [(0.231092, 0.732499)], 11: [(0.680999, 0.732088)],
	12: [(0.59731, 0.185911)], 13: [(0.806414, 0.194469)], 14: [(0.653701, 0.270982)],
	15: [(0.055721, 0.438299)], 16: [(0.615801, 0.327809)],
	18: [(0.256934, 0.158159)],
	19: [(0.493552, 0.212122), (0.228629, 0.277338)],
	20: [(0.882318, 0.419467)],
	21: [(0.16245, 0.516318), (0.171424, 0.579018)],
	22: [(0.675323, 0.171262), (0.682877, 0.214865)],
	23: [(0.620798, 0.316841)],
	24: [(0.405227, 0.534545)],
	25: [(0.454553, 0.727723)],
	26: [(0.865167, 0.31883), (0.097053, 0.32042)],
	27: [(0.41725, 0.340541)], 28: [(0.35637, 0.310761)],
	37: [(0.563025, 0.498711)], 38: [(0.563025, 0.498711)],
	45: [(0.622584, 0.842831)], 46: [(0.622584, 0.842831)],
	47: [(0.28813, 0.842831)], 48: [(0.28813, 0.842831)],
}

GI_POSITIONS = {
	0: [
		(0.1299, 0.835814), (0.126577, 0.827555), (0.767103, 0.838585),
		(0.191916, 0.72116), (0.724195, 0.72039), (0.050051, 0.614144),
		(0.063808, 0.584358), (0.043709, 0.551138), (0.861658, 0.612235),
		(0.837731, 0.559556), (0.765928, 0.838193), (0.894207, 0.671444),
		(0.894058, 0.716994), (0.892986, 0.762912), (0.894315, 0.80735),
		(0.204068, 0.732796), (0.713039, 0.731279), (0.83899, 0.580915),
		(0.050421, 0.613812), (0.896565, 0.714763), (0.896921, 0.668763),
		(0.896986, 0.760838), (0.896986, 0.805683), (0.722341, 0.721568),
		(0.044675, 0.550567), (0.860641, 0.611454), (0.190289, 0.721396),
		(0.896803, 0.805157), (0.898293, 0.759757), (0.897882, 0.714728),
		(0.899366, 0.668884), (0.836172, 0.559655), (0.049929, 0.613812),
		(0.061253, 0.584811),
	],
	1: [
		(0.88138, 0.450526), (0.785764, 0.294217), (0.790638, 0.312809),
		(0.880939, 0.165578), (0.731931, 0.114243), (0.635559, 0.106024),
		(0.636412, 0.105715), (0.73046, 0.114087), (0.82559, 0.121643),
		(0.824223, 0.121752), (0.542681, 0.098378), (0.542835, 0.09868),
		(0.806837, 0.196578), (0.597053, 0.188737), (0.653386, 0.274218),
		(0.807018, 0.191713), (0.597234, 0.183872), (0.653328, 0.269352),
		(0.806788, 0.196354), (0.597003, 0.188513), (0.653337, 0.273993),
		(0.881848, 0.449488), (0.813012, 0.193484), (0.602617, 0.18581),
		(0.661959, 0.269317), (0.640974, 0.023737), (0.810812, 0.042427),
		(0.946018, 0.062306), (0.675758, 0.216111), (0.77798, 0.302304),
		(0.640974, 0.023737), (0.946018, 0.06255), (0.809706, 0.040965),
		(0.946018, 0.06249), (0.881435, 0.165635), (0.785232, 0.294001),
		(0.791143, 0.312835), (0.640974, 0.023737), (0.809617, 0.042427),
	],
	2: [
		(0.065107, 0.060667), (0.157855, 0.024838), (0.063879, 0.061019),
		(0.157855, 0.024838), (0.275594, 0.100972), (0.209958, 0.121384),
		(0.422123, 0.119935), (0.426709, 0.191344), (0.287952, 0.179428),
		(0.194658, 0.173398), (0.249468, 0.237365), (0.209597, 0.121076),
		(0.27488, 0.101121), (0.157855, 0.024838), (0.065107, 0.061019),
	],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Monster Bash retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Monster Bash extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Monster Bash retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Monster Bash retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Monster Bash retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the mb_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/mb.c mbGameData GEN_WPC95 with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x3f,0x06,...}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), swStart/swTilt/swSlamTilt/"
				"swCoinDoor/swTicket/swLaunch defines, sKnocker=7 (preliminary ball-simulator scaffolding only), "
				"mb_mech[] mechanism table (mech 0 solenoid 28 with switches 81/82, mech 1 solenoid 27 with switches "
				"83/84, mech 2 solenoids 41/42 MECH_TWODIRSOL with switches 78/77/76/75/74 over a 90-step counter), "
				"and init_mb's wpc_set_fastflip_addr(0x87); src/wpc/core.h WPC solenoid numbering and WPC_swF1..WPC_swF8; "
				"src/wpc/core.c core_getSol WPC95 37..40 to 41..44 duplication; src/wpc/wpc.c WPC_FLIPPERSW95 inversion; "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95=0x80"
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
			"uri": "external:pinmame-manuals/by-machine/williams.monster-bash.1998/archive-Williams_Monster_Bash_Operations_Manual/Williams_1998_Monster_Bash_English_Manual.pdf",
			"original_filename": "Williams_1998_Monster_Bash_English_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"158-page image-only scan of the Williams Monster Bash operations manual (Internet Archive item "
				"Williams_Monster_Bash_Operations_Manual). Printed pages 2-44 through 2-53 carry the lamp/switch/"
				"solenoid location parts lists and their matrix and solenoid/flasher wiring tables; printed pages "
				"2-10 through 2-16 and 2-38 through 2-40 carry the board and assembly parts that fix device "
				"construction (trough opto boards, flipper opto PCB, eddy proximity sensor PCB, Dracula defender "
				"switch board, DC motor control assembly); Section 3 carries Game Wiring and Schematics."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.monster-bash.switch-locations",
					"locator": "PDF pages 116-117, printed 2-48/2-49, switch-locations parts list",
					"path": "evidence/excerpts/williams.monster-bash.1998/switch-locations.md",
					"sha256": "4dd414f43ae88a2d3e64f40ad85ec3cb1c9767aa59eafbc837370d47a9f6a8f2",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.switch-matrix",
					"locator": "PDF page 119, printed page 2-51, SWITCH MATRIX table",
					"path": "evidence/excerpts/williams.monster-bash.1998/switch-matrix.md",
					"sha256": "3095812b39f76d1ab1d26a7232e0f8581ed4b83f11260391dcadd25e628fa294",
					"image": "evidence/excerpts/williams.monster-bash.1998/switch-matrix.webp",
					"image_sha256": "5054d0ad3d70ca17e24dbdeb861f54ffc26235a5c8e0ed94cb33bb05551776ca",
					"image_derivation": "Williams_1998_Monster_Bash_English_Manual.pdf page 119, crop box 0.08,0.06,0.98,0.58 of the page, rendered at 300 dpi with pdftoppm, reduced to 750px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.lamp-locations",
					"locator": "PDF page 112, printed 2-44, lamp-locations parts list",
					"path": "evidence/excerpts/williams.monster-bash.1998/lamp-locations.md",
					"sha256": "bd375fb9ec32550387cd1d7ebe69779d8ccd28240129d8a08ad0e9a299c2712c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.lamp-matrix",
					"locator": "PDF page 120, printed 2-52, lamp matrix wiring table",
					"path": "evidence/excerpts/williams.monster-bash.1998/lamp-matrix.md",
					"sha256": "69fd8340c0324e0ca991e14652fdaca5a9aa1b67cf449a91d748bdb10f689205",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.solenoid-flasher-locations",
					"locator": "PDF page 114, printed 2-46, solenoid/flasher locations parts list",
					"path": "evidence/excerpts/williams.monster-bash.1998/solenoid-flasher-locations.md",
					"sha256": "335515d2c806ed3e14fd04cdf77845872af0fc79958f514ac6d4606ff6c214f1",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.solenoid-flasher-wiring",
					"locator": "PDF page 121, printed 2-53, solenoid/flasher wiring table",
					"path": "evidence/excerpts/williams.monster-bash.1998/solenoid-flasher-wiring.md",
					"sha256": "66b0b99fbede03f85298dabddae8f8354d133edae3a5d53addaf1ff6ebd7d14c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.general-illumination",
					"locator": "PDF pages 114 and 121, printed 2-46 and 2-53, general illumination location and wiring",
					"path": "evidence/excerpts/williams.monster-bash.1998/general-illumination.md",
					"sha256": "745bae316909842d9b7853c2f2672e1da49532177dd349bb460ed0d64b322970",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.monster-bash.boards-and-assemblies",
					"locator": "PDF pages 78-84, printed 2-10 through 2-16, board/assembly pages fixing device construction",
					"path": "evidence/excerpts/williams.monster-bash.1998/boards-and-assemblies.md",
					"sha256": "9f7836b0ffb632401f0985286e6d439051243ff8a992d62f3e06bbc4137314f6",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/monster-bash-1998/manual-transcription.md",
			"revision": "2026-08-06",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with "
				"the rendered PNG page cache under external:pinmame-manuals/rendered/williams.monster-bash.1998/. "
				"The retained PDF is image-only (pdftotext yields 158 bytes of form feeds only), so this transcription "
				"is the source of record and the OCR text is never an authority."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/monster-bash-1998/source/Monster%20Bash%20%28Williams%201998%29%20VPWmod%20v1.0.vpx",
			"original_filename": "Monster Bash (Williams 1998) VPWmod v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW Mod v1.0 recreation of the physical machine, VPX version 10.6, released "
				f"February 2022. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/952 and "
				"y/2162. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/monster-bash-1998/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (163,861 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "mb_106b", Const UseSolenoids = 2 (fast flips), Const UseLamps = 0 with an explicit '
				"UpdateLamps routine, Const UseSync = 1, the SolCallback table for solenoids 1-28 and 41 plus "
				"core.vbs sLRFlipper/sLLFlipper, the Controller.Switch and vpmTimer.PulseSw switch semantics for the "
				"trough/Dracula/Frankenstein/Up-Down-Bank state machines, and GiCallBack2 UpdateGi mapping GI 0/1/2 to "
				"the GIBot/GITopRight+GIBumpers/GITopLeft playfield emitter collections."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/monster-bash-1998/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
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
				"optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			assembly, part_number = SWITCH_PARTS.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed as an opto that is typically closed; PinMAME's mbGameData inverted-switch mask "
					"({0x00,0x00,0x00,0x3f,0x06,...}, column 3 bits 0-5 and column 4 bits 1-2) covers it, so the "
					"public switch state is already normalized and must not be inverted again."
				)
			elif address in OPTO_SWITCHES:
				notes += (
					" Printed on the A-21402 Defender Switch Board Assembly (page 2-11/2-12, \"IC Opto Inter w/Switch "
					"10mA\") as an opto interrupter that rests closed: it is listed under the manual's Opto Assembly "
					"Part Number column with no switch part number, and shaded \"OPTO, TYPICALLY CLOSED\" on the "
					"printed switch matrix (2-51), the same halftone used for 31-36 and 42/43. Unlike those eight, "
					"column 7 of PinMAME's mbGameData inverted-switch mask is 0x00, so the public switch state is "
					"not normalized by the emulator even though the hardware is physically normally closed; see "
					"conflict.dracula-position-opto-not-normalized."
				)
			if address == 24:
				notes += (
					" Physical part 5643-15190-00 is a permanently closed link used to prove the matrix is connected."
				)
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 18:
				notes += ' Printed part number transcribed verbatim as "5467-12693-32" (all sibling rollover parts use the 5647- prefix; the manual print is preserved rather than silently corrected).'
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CONTROLLER_SOURCE)
				label = f"Not Used Matrix Position {address}"
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
				if address in {11, 13, 14, 21, 22}:
					role = {
						11: "cabinet.launch",
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {11, 13} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None, True),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316", True),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None, True),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316", True),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None, False),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, "A-17316", True),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", True, "opto", None, "A-17316", True),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly, keep_wiring) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" Monster Bash has no upper flippers and the switch-locations parts list on manual page 2-48 marks "
				"this position Not Used (assembly and switch part both print NOT USED)."
			)
			physical["location"] = "not installed"
			if keep_wiring:
				notes += (
					" The switch-matrix wiring page (2-51) nonetheless shades this position as an opto on the reused "
					"Flipper Opto PCB Assembly template (assembly A-17316, same construction as the fitted lower-"
					"flipper button optos 112/114), so its printed construction is recorded even though no physical "
					"switch is installed."
				)
			else:
				notes += " The matrix-page wiring for this position is drawn as a plain (non-opto) end-of-stroke leaf, matching the fitted lower-flipper EOS template."
		elif switch_type == "opto":
			notes += (
				" Printed as an opto that is typically closed. WPC-95 reads the flipper column through "
				"WPC_FLIPPERSW95 with a hardware inversion, so the public switch state is already normalized."
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
			extra["spatial"] = not_applicable(
				"cabinet_or_service" if role.endswith(".button") else "internal_nonvisual",
				MANUAL_SOURCE,
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

	# Fliptronic 117 (F7) is repurposed as the Center Spinner, confirmed by the retained script's
	# Spinner1_spin handler (vpmTimer.PulseSw 117).
	items.append(
		_device(
			"switch.generic-117",
			"Center Spinner",
			"switch",
			"pinmame.input.switch",
			117,
			"used",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
			aliases=[
				{"namespace": "pinmame.switch", "value": "117"},
				{"namespace": "manual.address", "value": "F7"},
			],
			normally_closed=False,
			physical={
				"assembly_part_number": "A-22268",
				"part_number": "5647-12693-24",
				"switch_type": "leaf",
				"notes": (
					"Printed Fliptronic grounded switch F7. The switch-locations parts list on page 2-48 names it "
					"CENTER SPINNER rather than an upper-left flipper position, and the wiring page (2-51) matrix-"
					"page description agrees. The retained script's Spinner1_spin handler independently confirms it: "
					"vpmTimer.PulseSw 117."
				),
			},
			wiring={"board": "WPC-95 CPU board", "drive_wire": "Black-Gray", "drive_connection": "J208-10"},
			spatial=located("switch.generic-117", "sensor", [(0.493432, 0.212976)], VPX_TABLE_SOURCE),
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
						"WPC-95 CPU-board country/option configuration DIP bank. The retained transcription of this "
						"manual does not include the per-country switch-combination chart, so no specific ON/OFF "
						"combination is asserted here."
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
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			kind = "flasher" if 17 <= address <= 26 else "motor" if address in {27, 28, 37, 38} else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher":
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" Only the playfield bulb(s) have a playfield placement; back-panel and insert-panel bulbs "
						"are backbox hardware behind the translite and are deliberately not given a playfield "
						"coordinate."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {4, 7}:
				notes += (
					" The printed table shows a populated power-driver transistor with no voltage connection and no "
					"drive connection in any playfield, insert, or cabinet column, so no solenoid, flasher, flipper, "
					"or motor is fitted here."
				)
				if address == 7:
					notes += (
						" Pinned PinMAME's *** PRELIMINARY *** mb.c defines #define sKnocker 7, consumed only by its "
						"preliminary ball simulator, and the retained known-working VPW script sets "
						'SolCallback(7) = "solKnocker" and plays a knocker sound. These are reconcilable rather than '
						"contradictory: the WPC-95 operating system uses driver 7 as its standard knocker output and "
						"the ROM pulses it, but this physical machine ships with no knocker coil on that circuit. All "
						"three sources are cited and no physical knocker device is claimed."
					)
			if address in {33, 34, 35, 36}:
				notes += (
					" Fliptronic upper-flipper circuit with no coil or switch part printed; Monster Bash has no upper "
					"flippers and no other device is wired through this circuit."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias."
				)
			if address in {37, 38}:
				notes += (
					" WPC-95 LPDC output; PinMAME duplicates it at public address "
					f"{41 if address == 37 else 42}, so a recreation must treat {address} and "
					f"{41 if address == 37 else 42} as one physical DC-motor drive line, not an additional device. "
					"The A-16120 DC Motor Control Assembly drives the Dracula motor as an H-bridge, which is why 37/38 "
					"are forward/backward drive lines rather than two independent coils."
				)
			if address in {45, 46, 47, 48}:
				notes += " Manual page 3-style flipper circuits are fed from the +50 V supply."
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-95 power driver board", "driver_transistor": wiring_data["driver_transistor"]}
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			if address in FLIPPER_DRIVE_WIRE:
				wiring["control_wire"] = FLIPPER_DRIVE_WIRE[address]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if not fitted:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				if address == 17:
					extra["roles"] = ["cabinet.insert-panel"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				else:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address == 7:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41, 42} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Monster Bash playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Monster Bash playfield device.",
			31: "PinMAME's synthetic game-on state. Monster Bash sets wpc_set_fastflip_addr(0x87), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			39: "Unused WPC-95 LPDC general-purpose output; Monster Bash populates only LPDC outputs 37 and 38.",
			40: "Unused WPC-95 LPDC general-purpose output; Monster Bash populates only LPDC outputs 37 and 38.",
			41: "PinMAME's backward-compatibility mirror of LPDC output 37 (Dracula Motor Forward). It reports the same physical H-bridge drive line and is not an additional device; PinMAME's own mb_mech[2] table (MECH_TWODIRSOL) reads the Dracula mechanism through 41/42 rather than 37/38.",
			42: "PinMAME's backward-compatibility mirror of LPDC output 38 (Dracula Motor Backward); see 41.",
			43: "Unused WPC-95 LPDC mirror of output 39.",
			44: "Unused WPC-95 LPDC mirror of output 40.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. mbGameData declares no custSol.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42} else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if address in MANUAL_SOLENOID_ALIASES:
			virtual_aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			if address == 78:
				# Only lamp 78 is unused; handled after this loop body via the fitted branch below.
				pass
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += f" The printed lamp-locations map marks this insert with a bulb quantity of {LAMP_QUANTITIES[address]} and the retained table binds both bulbs, so it has two placements."
			if address in LAMP_MATRIX_PAGE_TYPOS:
				notes += (
					f' The lamp-matrix page (2-52) prints this insert as "{LAMP_MATRIX_PAGE_TYPOS[address]}"; the '
					"lamp-locations parts list (2-44) label used here is taken as authoritative."
				)
			if address == 48:
				notes += (
					" The paired right-hand insert at 25 reads RIGHT GARGLE on both pages, and the Bride of "
					"Frankenstein insert trio is PRIMP / WARM UP / GARGLE (46/47/48 left, 27/26/25 right), so "
					'"GARGOYLE" on the matrix page is the typographic slip.'
				)
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated launch/start button assembly, sharing its assembly part number with switch 11 or 13."
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
			if address == 78:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = "Not Used Lamp Position 78"
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The lamp-locations parts list marks this position Not Used."
			elif address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.launch" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				if address in LAMP_RENDER_DOUBLES:
					suffix = {11: "l11/l11a", 57: "l57/l57a"}.get(address, f"l{address}/l{address}a duplicates")
					physical["notes"] += (
						f" The retained table stacks a second co-located Light object purely for brightness ({suffix} "
						"style pair, offset under one bulb diameter); the primary object is used and the duplicate is "
						"documented render doubling, matching the manual's single-bulb parts entry."
					)
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
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


LAMP_POSITIONS = {
	11: [(0.518277, 0.509543)], 12: [(0.199804, 0.49876), (0.710372, 0.502353)],
	13: [(0.405943, 0.533151)], 14: [(0.50634, 0.537244)], 15: [(0.574517, 0.41598)],
	16: [(0.551512, 0.451824)], 17: [(0.53859, 0.479014)], 18: [(0.481972, 0.573016)],
	21: [(0.671491, 0.427018)], 22: [(0.454597, 0.73012)], 23: [(0.779019, 0.680592)],
	24: [(0.158099, 0.435465), (0.765244, 0.441418)], 25: [(0.599521, 0.512225)],
	26: [(0.62114, 0.483876)], 27: [(0.644151, 0.457066)], 28: [(0.809852, 0.400382)],
	31: [(0.21877, 0.531547), (0.684767, 0.534045)], 32: [(0.205052, 0.404896)],
	33: [(0.562259, 0.255792)], 34: [(0.729677, 0.56667)], 35: [(0.782401, 0.09427)],
	36: [(0.688094, 0.086437)], 37: [(0.593039, 0.078379)], 38: [(0.738957, 0.595469)],
	41: [(0.130041, 0.67901)], 42: [(0.052464, 0.710041)],
	43: [(0.178016, 0.467174), (0.737886, 0.472255)], 44: [(0.449184, 0.33161)],
	45: [(0.262057, 0.418111)], 46: [(0.280541, 0.449214)], 47: [(0.297417, 0.476591)],
	48: [(0.314342, 0.505653)], 51: [(0.603303, 0.783676)], 52: [(0.554294, 0.789335)],
	53: [(0.503492, 0.807494)], 54: [(0.41922, 0.815784)], 55: [(0.357062, 0.796703)],
	56: [(0.299984, 0.781439)], 57: [(0.501164, 0.253295)], 58: [(0.265512, 0.301478)],
	61: [(0.28784, 0.675863)], 62: [(0.346238, 0.658298)], 63: [(0.416445, 0.648462)],
	64: [(0.495905, 0.649024)], 65: [(0.565473, 0.661109)], 66: [(0.62834, 0.677409)],
	67: [(0.855933, 0.708944)], 68: [(0.453033, 0.875112)],
	71: [(0.310768, 0.372746)], 72: [(0.35508, 0.411708)], 73: [(0.372835, 0.379081)],
	74: [(0.366614, 0.345176)], 75: [(0.40987, 0.410668)], 76: [(0.434169, 0.368818)],
	77: [(0.123032, 0.386948)],
	81: [(0.09814, 0.421767)], 82: [(0.09912, 0.417134)], 83: [(0.099927, 0.412752)],
	84: [(0.101703, 0.407718)], 85: [(0.499801, 0.301312)], 86: [(0.501563, 0.348812)],
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-95 power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's GI emitter collection for this string (UpdateGi in the retained "
				"script). GI address 0 drives collection GIBot; GI address 1 drives GITopRight plus GIBumpers; GI "
				"address 2 drives GITopLeft."
			)
			if address == 0:
				notes += (
					" GIBot contains 35 members; one (light11, at normalized x=1.087804) sits outside the retained "
					"table's playfield bounds and is excluded here as a table modeling anomaly rather than a "
					"distinct physical bulb, leaving 34 placements."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite; the retained script's UpdateGi handles "
				"only GI addresses 0-2, so this string has no playfield coordinate."
			)
			if address == 4:
				notes += " This string additionally feeds cabinet bulbs through J104, the only cabinet connection on the printed general-illumination wiring page."
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(
			_device(
				identifier,
				label,
				"gi",
				"pinmame.output.gi",
				address,
				"used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
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
	def mechanism(
		identifier: str,
		label: str,
		kind: str,
		actuators: list[str],
		sensors: list[str],
		behavior: str,
		positions: list[tuple[str, str, list[str], str]],
		*refs: str,
		assembly_part_number: str | None = None,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
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

	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on trough optos 32-35, with Trough Ball 1 (32) at the eject end nearest the shooter lane "
			"and Trough Ball 4 (35) at the drain entrance. Solenoid 9 ejects the ball resting on 32; the retained "
			"script's ball-release handler (RandomSoundBallRelease sw32) pulses trough-eject opto 31 in the same "
			"event. All five positions are printed optos that rest closed (column 3 of the inverted-switch mask), "
			"so a recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"Monster Bash has no manual plunger. The ball ejected from the trough rests on shooter-lane switch 18 and "
			"auto-plunger coil 1 launches it when the cabinet Launch Ball button (switch 11) is pressed.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22429-1",
		),
		mechanism(
			"mechanism.dracula",
			"Rotating Dracula figure and coffin",
			"motorized",
			[output_id("Dracula Motor Forward"), output_id("Dracula Motor Backward")],
			["switch.matrix-74", "switch.matrix-75", "switch.matrix-76", "switch.matrix-77", "switch.matrix-78", "switch.matrix-25"],
			"A DC gearmotor drives the rotating Dracula figure through an H-bridge (A-16120 DC Motor Control "
			"Assembly) on public LPDC outputs 37 (forward) and 38 (backward); PinMAME publishes the same two "
			"physical drive lines a second time at mirror addresses 41/42, and its own mb_mech[2] table "
			"(MECH_TWODIRSOL) reads the mechanism through 41/42 over a 90-step position counter with switch 78 "
			"asserting at steps 0-5, 77 at 18-23, 76 at 36-51, 75 at 64-69, and 74 at 85-89 -- i.e. printed Dracula "
			"Position 1 through Position 5 in ascending step order. The five position optos are printed on the "
			"A-21402 Defender Switch Board Assembly mounted inside the mechanism, not as five separate playfield "
			"objects. Dracula Target switch 25 is a 47-segment target-wall ring (collection DracTargets) that "
			"surrounds the figure; only one segment is active at a time, selected by the figure's own rotation "
			"(DracTargets_Hit indexes on Drac.RotZ).",
			[
				("position-1", "Dracula Position 1", ["switch.matrix-78"], "Motor step 0-5."),
				("position-2", "Dracula Position 2", ["switch.matrix-77"], "Motor step 18-23."),
				("position-3", "Dracula Position 3", ["switch.matrix-76"], "Motor step 36-51."),
				("position-4", "Dracula Position 4", ["switch.matrix-75"], "Motor step 64-69."),
				("position-5", "Dracula Position 5", ["switch.matrix-74"], "Motor step 85-89."),
				("target-ring", "Dracula target ring struck", ["switch.matrix-25"], "One of 47 target-wall segments surrounding the figure."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22292",
		),
		mechanism(
			"mechanism.frankenstein-table",
			"Motorized Frankenstein table and hit target",
			"motorized",
			[output_id("Frank Motor")],
			["switch.matrix-83", "switch.matrix-84", "switch.matrix-87"],
			"Motor 27 rotates the Frankenstein figure (franky) between a lowered rest position and a raised "
			"striking position. PinMAME's own mb_mech[1] table reads switches 83 (table down, position steps 0-10) "
			"and 84 (table up, steps FRANKTIME-10..FRANKTIME-1, FRANKTIME=120) from the same motor-position counter "
			"used by the WPC-95 mechanism API. The retained script instead drives 83/84 directly from the figure's "
			"own rotation angle (franky.rotx) and raises Frank Hit switch 87 whenever franky.rotx sits in the "
			"striking band (above -80 to -76 degrees depending on direction), toggling a hit-wall collision object "
			"(fhitwall) in step so a ball can only score the hit while the figure is in range.",
			[
				("down", "Frank table down", ["switch.matrix-83"], "Lowered/rest position."),
				("up", "Frank table up", ["switch.matrix-84"], "Raised/striking position."),
				("hit", "Frank hit", ["switch.matrix-87"], "Ball strikes the raised figure's hit wall."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22422",
		),
		mechanism(
			"mechanism.up-down-bank",
			"Motorized up/down target bank",
			"motorized",
			[output_id("Up/Down Bank Motor")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-85", "switch.matrix-86"],
			"Motor 28 raises and lowers the two-target bank (frankytargets) between an up (targets exposed) and a "
			"down (targets retracted) position. PinMAME's own mb_mech[0] table reads switches 81 (bank up, steps "
			"0-10) and 82 (bank down, steps BANKTIME-10..BANKTIME-1) from the WPC-95 mechanism API's own position "
			"counter. The retained script instead drives 81/82 directly from frankytargets.z threshold crossings in "
			"the same timer that animates the bank, and toggles the drop-target visuals (sw85b/sw86b) in step. Left "
			"and right standup targets 85/86 sit on the bank and are reachable only while it is up.",
			[
				("up", "Bank up", ["switch.matrix-81"], "Targets exposed."),
				("down", "Bank down", ["switch.matrix-82"], "Targets retracted."),
				("left-target", "Left up/down bank target", ["switch.matrix-85"], "Left standup on the bank."),
				("right-target", "Right up/down bank target", ["switch.matrix-86"], "Right standup on the bank."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22276",
		),
		mechanism(
			"mechanism.mummy-coffin",
			"Mummy coffin toy",
			"toy",
			[output_id("Mummy Coffin")],
			[],
			"Solenoid 3 (SolMummy) opens and closes the mummy coffin lid (Mumcoffin); the retained script animates "
			"the lid rotation and drives a shake timer while the coffin is open. There is no printed switch dedicated "
			"to this toy; it is driven purely as a scored callback.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22302",
		),
		mechanism(
			"mechanism.bride-post",
			"Bride post toy",
			"toy",
			[output_id("Bride Post")],
			[],
			"Solenoid 2 (SolBride) raises and lowers a post (BrideH) near the top lanes; the retained script animates "
			"the post's Z height on activation and release. There is no printed switch dedicated to this toy.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22425",
		),
		mechanism(
			"mechanism.ramp-lock-post",
			"Right ramp lock post",
			"gate",
			[output_id("Ramp Lock Post")],
			["switch.matrix-73"],
			"Solenoid 8 (SolLockPost) raises a post (LockP) that locks a ball on the right ramp; right-ramp-lock "
			"switch 73 senses the ball held at the lock. The retained script raises the post and enables a "
			"companion diverter (RRPost) together.",
			[("locked", "Ball locked at the right ramp post", ["switch.matrix-73"], "Right ramp lock switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-22293",
		),
		mechanism(
			"mechanism.ball-gates",
			"Left and right ball gates",
			"gate",
			[output_id("Left Gate"), output_id("Right Gate")],
			[],
			"Two solenoid-operated one-way gates (LGate solenoid 5, RGate solenoid 6) admit a ball into a loop or "
			"lane while blocking return travel; the retained script drives both through the shared vpmSolGate helper "
			"and animates companion playfield flap objects (sw68p/sw71p/sw63p rotation) tied to the same gate angle.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.left-eject",
			"Left eject hole",
			"kicker",
			[output_id("Left Eject")],
			["switch.matrix-28"],
			"A ball resting on switch 28 (Left Eject) is kicked back to the playfield by solenoid 15.",
			[("held", "Ball in the left eject hole", ["switch.matrix-28"], "Left eject switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22449",
		),
		mechanism(
			"mechanism.right-popper",
			"Right popper",
			"kicker",
			[output_id("Right Popper")],
			["switch.matrix-36"],
			"A ball resting on opto 36 (Right Popper) is kicked back to the playfield by solenoid 16.",
			[("held", "Ball in the right popper", ["switch.matrix-36"], "Right popper opto.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22266",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot assembly (A-17801) carries a kick switch (A-17800/SW-1A-114) and a separate scored "
			"switch (A-17794/SW-1A-120) with a diode attached. The retained script's LeftSlingShot_Slingshot and "
			"RightSlingShot_Slingshot handlers pulse matrix addresses 51 and 52 and fire coils 10/11 in the same "
			"event.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17801",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-55"],
			"Three A-12030-3 jet bumpers with A-16443-1 skirt switches. The retained script's Bumper1_Hit, "
			"Bumper2_Hit, and Bumper3_Hit handlers pulse switches 53, 54, and 55 and fire coils 12, 13, and 14 "
			"respectively, matching printed Left/Right/Bottom Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-53"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-54"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-55"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-12030-3",
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: the "
			"ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops to the "
			"hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. Monster Bash runs "
			"Const UseSolenoids = 2 fast flips, so the ROM drives the coils directly. There are no upper flippers; "
			"the upper-flipper Fliptronic circuits (33-36, 115, 116, 118) are unfitted.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-22603-R right with A-15849-L-2 left",
		),
		mechanism(
			"mechanism.center-spinner",
			"Center spinner",
			"other",
			[],
			["switch.generic-117"],
			"A free-spinning target (Spinner1) wired on the Fliptronic F7 position rather than the switch matrix. "
			"The retained script's Spinner1_spin handler pulses switch 117 and plays the spinner sound effect on "
			"every rotation.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22268",
		),
		mechanism(
			"mechanism.flipper-proximity-sensors",
			"Flipper eddy-current proximity sensors",
			"other",
			[],
			["switch.matrix-47", "switch.matrix-48"],
			"Two A-22149-1 Auto Adjust Eddy Sensor PCB assemblies detect flipper-blade position without a mechanical "
			"contact switch (TDA0161 proximity sensor IC with an auto-adjusting eddy controller and dual digital "
			"potentiometer). The retained script's own comment marks 42, 43, 47, and 48 as 'Opto & proximity "
			"switches', separating these eddy sensors (47/48) from the flipper-opto pair (42/43).",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22149-1",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough Eject"),
			"destination": "switch.matrix-31",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.dracula-position-opto-not-normalized",
			"path": "inputs[binding.device=74,75,76,77,78]",
			"description": (
				"The manual documents public switches 74-78 (Dracula Position 5 through 1) as opto interrupters "
				"that rest closed: printed switch-locations page 2-48/49 lists assembly A-21402 under the "
				"\"Switch Assembly Part Number OR Opto Assembly Part Number\" column with the Switch Part Number "
				"column blank -- the same signature as the trough optos (31-35) and the right-popper opto (36) -- "
				"printed 2-11/2-12 names A-21402 the \"Defender Switch Board Assembly\" with \"IC Opto Inter "
				"w/Switch 10mA\", and the printed switch matrix (2-51) shades all five cells \"OPTO, TYPICALLY "
				"CLOSED\", the identical halftone used for 31-36 and 42/43. Pinned PinMAME's mbGameData does not "
				"treat them the same way: its inverted-switch mask "
				"({0x00,0x00,0x00,0x3f,0x06,0x00,0x00,0x00,0x00,0x00,0x00,0x00}) covers only columns 3 and 4 "
				"(31-36 and 42/43); column 7, which carries 74-78, is 0x00, so unlike those eight addresses the "
				"public state of 74-78 is not emulator-normalized. Compounding this, PinMAME's own mb_mech[2] "
				"table (MECH_TWODIRSOL, switches 78/77/76/75/74 asserted at ascending 90-step motor-position "
				"ranges) asserts each of these switches ON while the figure occupies its position, which is the "
				"sense a normally-open sensor would report, i.e. the opposite of a printed normally-closed opto. "
				"The manual is physical-construction ground truth and pinned PinMAME is public-address and "
				"emulator-normalization ground truth, and the two disagree on whether a recreation must invert "
				"these five addresses. Resolution path: run the implemented LibPinMAME gameplay harness against a "
				"legal mb_10 or mb_106b ROM, drive the Dracula motor through its 90-step range, and observe the "
				"idle public state of 74-78 and their transitions at the mb_mech[2] boundaries. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
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
			"id": "williams.monster-bash.1998",
			"name": "Monster Bash",
			"manufacturer": "Williams",
			"year": 1998,
			"kind": "physical_pinball",
			"ipdb_id": 4441,
			"opdb_id": "Gr3EW-MD3Nj",
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "validated",
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
		"knowledge": {"path": "knowledge/williams/monster-bash-1998.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Monster Bash device identifiers are not unique: {duplicates}")
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
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
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
			"Public switches 74-78 (Dracula Position 5-1) are printed normally-closed opto interrupters "
			"that pinned PinMAME's mbGameData inverted-switch mask does not normalize (column 7 is 0x00, "
			"unlike columns 3 and 4), while PinMAME's own mb_mech[2] table asserts them at their step "
			"ranges in what reads as the opposite sense. This is a polarity conflict, not a spatial gap "
			"-- every dimension this report audits is complete and validated -- but it is recorded as "
			"conflict.dracula-position-opto-not-normalized and keeps the machine record partial until a "
			"LibPinMAME harness trace against a legal mb_10 or mb_106b ROM observes the true idle public "
			"state of 74-78.",
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
			"manifest_uri": "external:pinmame-vpx-sources/williams/monster-bash-1998/extracted-vpxtool.manifest.json",
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
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.monster-bash.1998/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/monster-bash-1998/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"GIbot member light11 (normalized x=1.087804, outside the 0..1 playfield bounds) -- table modeling anomaly, not a distinct physical bulb",
			"f20a, f22c, f21c flasher render-doubling/centroid helper Light objects",
			"l11a, l57a, l6na, l8npp2-style co-located brightness-doubling Light objects",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Monster Bash (Williams, 1998) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete, but the physical "
		"machine record itself remains `partial` at `machines/partial/williams/monster-bash-1998.json` "
		"because of an unresolved switch-polarity conflict outside this audit's scope; see the promotion "
		"decision below.",
		"",
		"The matching source is the retained known-working `Monster Bash (Williams 1998) VPWmod v1.0.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at "
		f"SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and y/2162 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is "
		"the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; "
		"the retained table supplies geometry.",
		"- The retained manual PDF is an image-only scan (`pdftotext` yields 158 bytes of form feeds only). Every "
		"printed table used here was read from rendered pages and transcribed into "
		"`external:pinmame-review-artifacts/monster-bash-1998/manual-transcription.md`.",
		"- Several switches have no dedicated playfield trigger object because the retained script sets their public "
		"state directly from another mechanism's continuous position (Dracula motor step counter, Frankenstein "
		"figure rotation, Up/Down Bank target Z height) rather than from a Hit/Trigger event. Those addresses are "
		"explicit documented projections onto the real table object that carries the underlying mechanism state.",
		"- GIbot member `light11` sits at normalized x=1.087804, outside the retained table's 0..1 playfield bounds, "
		"and is excluded as a table modeling anomaly; GI address 0's physical quantity is 34, not the collection's "
		"raw 35 members.",
		"- Flasher addresses 18-26 (excluding 17) each drive at least one playfield bulb; only the playfield bulb "
		"receives a coordinate. Address 17 (Wolfman Flashers) has zero playfield bulbs -- both fitted lamps are on "
		"the back panel and insert panel -- so it takes a `cabinet_or_service` record with role `cabinet.insert-"
		"panel`.",
		"- GI strings 0-2 use the retained table's GIBot/GITopRight+GIBumpers/GITopLeft emitter collections, matching "
		"the retained script's `UpdateGi` dispatch exactly. GI strings 3 and 4 are backbox insert-panel circuits "
		"and take a controlled `cabinet_or_service` record.",
		"- Solenoids 41/42 are PinMAME's LPDC mirror of physical Dracula-motor drive lines 37/38 and are declared "
		"virtual with a `virtual` spatial record so no duplicate motor is ever placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
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
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses "
		"this audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. However, public switches 74-78 (Dracula Position 5 through 1) are printed normally-closed "
		"opto interrupters on the A-21402 Defender Switch Board Assembly that pinned PinMAME's mbGameData "
		"inverted-switch mask does not normalize (column 7 is 0x00, unlike columns 3 and 4), while PinMAME's own "
		"mb_mech[2] table asserts them at their step ranges in what reads as the opposite sense -- an unresolved "
		"polarity conflict recorded as `conflict.dracula-position-opto-not-normalized`. The definition therefore "
		"carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = \"conflicted\"`, so "
		"promotion to `author_ready` is refused; the record stays `partial` with "
		"`coverage.missing = [\"polarity\", \"unresolved_conflicts\"]` until a LibPinMAME harness trace against a "
		"legal mb_10 or mb_106b ROM observes the true idle public state of 74-78.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
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
		raise RuntimeError(f"Stale Monster Bash author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Monster Bash definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Monster Bash seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Monster Bash definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Monster Bash seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Monster Bash spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Monster Bash spatial review drifted from its deterministic curator: {markdown_path}")
	print("Monster Bash definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Monster Bash extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Monster Bash retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
