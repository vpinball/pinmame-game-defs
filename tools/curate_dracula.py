"""Curate the physical Williams Bram Stoker's Dracula (1993) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses
drift, and ``--regenerate`` is the only path that writes the canonical definition and its
pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/williams/bram-stoker-s-dracula-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/bram-stoker-s-dracula-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/bram-stoker-s-dracula-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/bram-stoker-s-dracula-1993.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.williams.bram-stoker-s-dracula.1993"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.bram-stoker-s-dracula.1993"
VPX_TABLE_SOURCE = "vpx-table.drac-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.drac-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.drac-vpw-1-0"
IPDB_SOURCE = "ipdb.williams.bram-stoker-s-dracula.1993"

TABLE_SHA256 = "e291eb0ab61eb8940aba6f54d16efd512d4565cbb6af29fcae5530035de7575e"
SCRIPT_SHA256 = "32f4f0ed85702cc015563eb262ea6c5b7cb7c90f6d30fa6b73c36f3c37c42c5f"
MANUAL_SHA256 = "de6840bb83a98333ef96a2781e3170103e5856380e9c46aad237974fc028498a"
MANUAL_TRANSCRIPTION_SHA256 = "46fae8a9e5b625634576dd280d0cf8ce78106ecd71aafdee0f921784f5105548"

EXTRACTION_RELATIVE_PATH = Path("williams/bram-stokers-dracula-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/bram-stokers-dracula-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "ea69203a05b34f6eeb7572e17d1185e2d42be87b8ebd5593bf9efe44baa28da0"
EXTRACTION_FILE_COUNT = 2484
EXTRACTION_TOTAL_BYTES = 597253321

TABLE_BOUNDS = "left=0 top=0 right=952.941 bottom=2117.647"

DRIVER_IDS = ("drac_l1", "drac_d1", "drac_l2c", "drac_p11", "drac_p12")
DRIVER_COMPATIBILITY = {
	"drac_l1": (
		"identical",
		"Williams production L-1 game ROM shipped with the physical machine; the retained known-working "
		'VPW script binds this driver directly (Const cGameName = "drac_l1").',
	),
	"drac_d1": (
		"identical",
		"Williams D-1 LED Ghost Fix revision; a later firmware revision of the same physical machine with "
		"no controller-address or playfield change.",
	),
	"drac_l2c": (
		"identical",
		"L-2C Competition MOD, a 2016 community ruleset revision that runs on the identical physical "
		"hardware and addresses as the production L-1 ROM.",
	),
	"drac_p11": (
		"identical",
		"P-11 prototype game ROM for the same physical machine; PinMAME clones it directly from drac_l1 "
		"with no separate core_tGameData.",
	),
	"drac_p12": (
		"identical",
		"P-12 LED Ghost Fix prototype revision; a further prototype firmware revision of the same physical "
		"machine.",
	),
}

# --- Printed switch matrix (manual page 116, printed 3-4). Opto label taken verbatim from
# the printed cell text (this manual writes "Opto ___" directly rather than shading).
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt", 15: "L. Drop Target", 16: "L. Drop Score",
	17: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed",
	25: "Top 3-lane Left", 26: "Top 3-Lane Middle", 27: "Top 3-lane Right", 28: "R. Ramp Score",
	31: "Under Shooter Ramp", 34: "Launch Ball", 35: "Left Drain", 36: "Left Return",
	37: "Right Return", 38: "Right Drain",
	41: "Trough 1 Ball", 42: "Trough 2 Balls", 43: "Trough 3 Balls", 44: "Trough 4 Balls",
	48: "Outhole",
	51: "T.R. Lane", 52: "Magnet Left Pocket", 53: "Castle Lock 1", 54: "Castle Lock 2",
	55: "Wire Ramp Popper", 56: "Crypt Popper", 57: "Castle Lock 3", 58: "Mystery Hole",
	61: "Left Jet Bumper", 62: "Right Jet Bumper", 63: "Bottom Jet Bumper",
	64: "Left Slingshot", 65: "Right Slingshot",
	66: "Left 3-bank Top", 67: "Left 3-bank Middle", 68: "Left 3-Bank Bottom",
	71: "Castle Popper", 72: "Coffin Popper", 73: "Left Ramp Entry", 77: "Right Ramp Up",
	81: "Magnet Left", 82: "Ball On Magnet", 83: "Magnet Right",
	84: "Left Ramp Made", 85: "Left Ramp Diverted",
	86: "Middle 3-bank Left", 87: "Middle 3-bank Middle", 88: "Middle 3-bank Right",
}
# Printed "Not Used" on the switch matrix, plus 23 ("Ticket Opto." on the matrix page but a
# blank Switch No. -- physical-fitment ground truth -- on the Switch Locations parts list).
UNUSED_MATRIX_ADDRESSES = {11, 12, 18, 23, 32, 33, 45, 46, 47, 74, 75, 76, 78}
# Switches labelled "Opto ___" on the printed matrix (columns 5 and 7 rows 1-3) plus switch 82,
# which the Switch Locations parts list alone proves is the only genuine opto in column 8
# (A-14315/A-14316); 81 and 83 use the plain leaf part 5647-12693-14.
OPTO_SWITCHES = {51, 52, 53, 54, 55, 56, 57, 71, 72, 73, 82}
PULSED_SWITCHES = {31}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	21: "leaf", 22: "microswitch", 24: "other",
	25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "microswitch", 34: "microswitch", 35: "microswitch", 36: "microswitch",
	37: "microswitch", 38: "microswitch",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch", 48: "microswitch",
	51: "opto", 52: "opto", 53: "opto", 54: "opto", 55: "opto", 56: "opto", 57: "opto",
	58: "microswitch",
	61: "leaf", 62: "leaf", 63: "leaf", 64: "leaf", 65: "leaf",
	66: "microswitch", 67: "microswitch", 68: "microswitch",
	71: "opto", 72: "opto", 73: "opto", 77: "microswitch",
	81: "microswitch", 82: "opto", 83: "microswitch",
	84: "microswitch", 85: "microswitch",
	86: "microswitch", 87: "microswitch", 88: "microswitch",
}

# address -> (assembly_part_number, part_number), transcribed verbatim from the Switch
# Locations page (109, printed 2-46).
SWITCH_PARTS = {
	13: (None, "20-9663-1"), 14: (None, "A-6502-A"),
	15: (None, "5647-12693-31"), 16: (None, "5647-12693-19"), 17: (None, "5647-12693-04"),
	21: (None, "SW-1A-117"), 22: (None, "5643-09288-00"), 24: (None, "5643-09288-00"),
	25: (None, "5647-12693-19"), 26: (None, "5647-12693-19"), 27: (None, "5647-12693-19"),
	28: (None, "5647-12693-21"), 31: (None, "5647-12693-19"), 34: (None, "A-15896-1"),
	35: (None, "5647-12693-19"), 36: (None, "5647-12693-19"), 37: (None, "5647-12693-19"),
	38: (None, "5647-12693-19"),
	41: (None, "5647-12693-08"), 42: (None, "5647-09957-00"), 43: (None, "5647-09957-00"),
	44: (None, "5647-09957-00"), 48: (None, "5647-12133-12"),
	51: ("A-14315 (LED) with A-14316 (Trans)", None),
	52: ("A-14315 (LED) with A-14316 (Trans)", None),
	53: ("A-14315 (LED) with A-14316 (Trans)", None),
	54: ("A-14315 (LED) with A-14316 (Trans)", None),
	55: ("A-14315 (LED) with A-14316 (Trans)", None),
	56: ("A-14315 (LED) with A-14316 (Trans)", None),
	57: ("A-14315 (LED) with A-14316 (Trans)", None),
	58: (None, "5647-12693-13"),
	61: (None, "SW-11A-37"), 62: (None, "SW-11A-37"), 63: (None, "SW-11A-37"),
	64: ("SW-1A-114 (Kick) with SW-1A-120 (Score)", None),
	65: ("SW-1A-114 (Kick) with SW-1A-120 (Score)", None),
	66: (None, "A-14691-2"), 67: (None, "A-14691-4"), 68: (None, "A-14691-2"),
	71: ("A-14315 (LED) with A-14316 (Trans)", None),
	72: ("A-14315 (LED) with A-14316 (Trans)", None),
	73: ("A-14315 (LED) with A-14316 (Trans)", None),
	77: (None, "5647-12693-36"),
	81: (None, "5647-12693-14"),
	82: ("A-14315 (LED) with A-14316 (Trans)", None),
	83: (None, "5647-12693-14"),
	84: (None, "5647-12693-21"), 85: (None, "5647-12693-21"),
	86: (None, "A-14691-2"), 87: (None, "A-14691-4"), 88: (None, "A-14691-2"),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"),
	3: ("Green-Orange", "J207-3", "U20-16"), 4: ("Green-Yellow", "J207-4", "U20-15"),
	5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"),
	3: ("White-Orange", "J209-3", "U18-5"), 4: ("White-Yellow", "J209-4", "U18-7"),
	5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"),
	3: ("Orange-Black", "J205-3"), 4: ("Orange-Yellow", "J205-4"),
	5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
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
# Fliptronic II F1-F8 wiring, printed on the Switch Matrix page (116). F1-F4 are populated
# per the Switch Locations parts list; F5-F8 print this same generic board wiring but have no
# printed part number anywhere and no upper-flipper coil row on the Solenoid/Flasher Table.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J905-5"),
}

# --- Printed solenoid/flasher table (manual page 120, printed 3-8).
SOLENOID_LABELS = {
	1: "Shooter", 2: "Coffin Popper", 3: "Castle Popper", 4: "Right Ramp Down",
	5: "Crypt Popper", 6: "Wire Ramp Ball Popper", 7: "Knocker", 8: "Shooter Ramp Entry",
	9: "Left Sling", 10: "Right Sling", 11: "Left Jet", 12: "Right Jet", 13: "Bottom Jet",
	14: "Right Ramp Up", 15: "Outhole", 16: "Trough",
	17: "T.R. Corner / Dracula Flasher", 18: "Jackpot / Stoker Flasher",
	19: "3-bank / House Flasher", 20: "T.L. Corner / Mina Flasher",
	21: "Castle / Helsing Flasher", 22: "L. Ramp / L. Logo Flasher",
	23: "R. Ramp / R. Logo Flasher", 24: "Asylum / Renfield Flasher",
	25: "L. Drop Target Reset", 26: "Speaker Panel Flasher",
	27: "Magnet", 28: "Magnet's Motor",
	33: "Up/Down Post Diverter", 34: "Right Gate",
	35: "Castle Release Post", 36: "Left Gate Actuator",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38",
	39: "Unused WPC-Fliptronic Output 39", 40: "Unused WPC-Fliptronic Output 40",
	41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}

# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", power_connection="J107-3", part_number="AE-24-900", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", power_connection="J107-3", part_number="AE-26-1500", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", power_connection="J107-3", part_number="AE-26-1200", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", power_connection="J107-3", part_number="AE-26-1500", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", power_connection="J107-3", part_number="AE-26-1500", printed_type="High Power"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(control_connection="J127-3", driver_transistor="Q56", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", power_connection="J107-2", part_number="SM1-28-900", printed_type="Low Power"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", power_connection="J107-2", part_number="AE-27-1200", printed_type="Low Power"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	17: dict(control_connection="J126-1 (pf), J125-1 (bb)", driver_transistor="Q42", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	18: dict(control_connection="J126-2 (pf), J125-2 (bb)", driver_transistor="Q40", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	19: dict(control_connection="J126-3 (pf), J125-3 (bb)", driver_transistor="Q38", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	20: dict(control_connection="J126-4 (pf), J125-5 (bb)", driver_transistor="Q36", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	21: dict(control_connection="J126-5 (pf), J125-6 (bb)", driver_transistor="Q28", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	22: dict(control_connection="J126-6 (pf), J125-7 (bb)", driver_transistor="Q30", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	23: dict(control_connection="J126-7 (pf), J125-8 (bb)", driver_transistor="Q34", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	24: dict(control_connection="J126-8 (pf), J125-9 (bb)", driver_transistor="Q32", power_connection="J107-6 (pf), J106-5 (bb)", printed_type="Flasher"),
	25: dict(control_connection="*J122-1", driver_transistor="Q26", power_connection="J107-1", part_number="AE-26-1200", printed_type="Low Power"),
	26: dict(control_connection="J128-2 (bb)", driver_transistor="Q24", power_connection="J106-5 (bb)", printed_type="Flasher (Low Power)"),
	27: dict(control_connection="*J122-3", driver_transistor="Q22", power_connection="J107-1", part_number="20-9831", printed_type="Low Power"),
	28: dict(control_connection="J122-4", driver_transistor="Q20", power_connection="J107-6", part_number="14-7981", printed_type="Low Power"),
	33: dict(control_connection="J902-3", driver_transistor="Q1", power_connection="J907-2", part_number="AE-26-1500", printed_type="Up Lt. F. Power"),
	34: dict(control_connection="J902-1", driver_transistor="Q5", power_connection="J907-1", part_number="AE-26-1500", printed_type="Up Lt. F. Hold"),
	35: dict(control_connection="J902-6", driver_transistor="Q2", power_connection="J907-5", part_number="AE-26-1500", printed_type="Up Rt. F. Power"),
	36: dict(control_connection="J902-4", driver_transistor="Q7", power_connection="J907-4", part_number="A-14406", printed_type="Up Rt. F. Hold"),
	45: dict(control_connection="J902-11,13", driver_transistor="Q4", power_connection="J907-8,9", part_number="FL-15411", printed_type="Fliptronic power"),
	46: dict(control_connection="J902-11,13", driver_transistor="Q11", power_connection="J907-8,9", part_number="FL-15411", printed_type="Fliptronic hold"),
	47: dict(control_connection="J902-7,9", driver_transistor="Q3", power_connection="J907-6,7", part_number="FL-15411", printed_type="Fliptronic power"),
	48: dict(control_connection="J902-7,9", driver_transistor="Q9", power_connection="J907-6,7", part_number="FL-15411", printed_type="Fliptronic hold"),
}
SOLENOID_ASSEMBLIES = {
	1: "A-14525", 2: "A-16261", 3: "A-16263", 4: "A-16264", 5: "A-16262", 6: "A-16256",
	7: "B-10686-1", 8: "A-16245", 9: "B-9362-L-2", 10: "B-9362-R-3", 11: "A-9415-2",
	12: "A-9415-2", 13: "A-9415-2", 14: "A-16264", 15: "A-8039-3", 16: "B-9362-R-3",
	17: "A-12336-1", 18: "A-12336-1", 19: "A-8798", 20: "A-12336-1, A-8798", 21: "A-8798",
	22: "A-12336-1", 23: "A-12336-1", 24: "A-8798", 25: "A-16267", 27: "A-16266",
	28: "A-16050", 33: "A-16265", 34: "B-13935", 35: "A-16268", 36: "A-16246",
	45: "A-15205-R-4", 46: "A-15205-R-4", 47: "A-15205-L-4", 48: "A-15205-L-4",
}
# Retained VPW script callbacks and driven light objects, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "AutoPlunger (Plunger.Fire)", 2: "CoffinPopper (VUK)", 3: "CastlePopper (VUK)",
	4: "SolRRampDown (RightRamp.Collidable=True, Controller.Switch(77)=False)",
	5: "CryptPopper (VUK)", 6: "WirerampPopper (VUK)", 7: "SolKnocker",
	8: "SolShooterRamp (sramp2.Collidable, FLRamp.rotate)",
	14: "SolRRampUp (RightRamp.Collidable=False, Controller.Switch(77)=True)",
	16: "SolRelease (trough)", 25: "SolDTUp (drop-target reset)",
	27: "SolMistMagnet (MagnetOn flag consumed by MistTimer)",
	28: "MotorTimer_Timer reads Controller.Solenoid(28) directly -- no SolCallback",
	33: "SolTopDiverter (wDivert.isdropped, FDivert.rotate)",
	34: "SolRGate (RGate.open, RGateWall.IsDropped)",
	35: "CastleLockPost (clpost.isdropped)",
	36: "SolLGate (LGate.open, Wall_LO.isdropped)",
	46: "SolRFlipper (core.vbs sLRFlipper)", 48: "SolLFlipper (core.vbs sLLFlipper)",
}
# address -> (VPX light object(s), playfield placement count, backbox-only)
FLASHER_OBJECTS = {
	17: (["F17_Dome"], "(3) #906 on the playfield and (1) #906 on the back panel; the retained script's Flasher17 sub drives one light object (F17_Dome) for both the printed 'T.R Corner' and 'Dracula' functions."),
	18: (["F18"], "(1) #906 on the playfield and (1) #906 on the back panel; the retained script drives one light object (F18) for both the printed 'Jackpot' and 'Stoker' functions."),
	19: (["F19", "F19a"], "(1) #89 on the playfield and (1) #906 on the back panel; the retained script drives two distinct playfield light objects (F19 near the left 3-bank, F19a near center), matching the printed '3-bank' and 'House' functions."),
	20: (["F20", "F20_Dome"], "(1) #89 and (1) #906 on the playfield plus (1) #906 on the back panel; the retained script drives two distinct playfield light objects (F20, F20_Dome), matching the printed 'T.L. Corner' and 'Mina' functions."),
	21: (["F21", "F21a"], "(2) #89 on the playfield and (1) #906 on the back panel; the retained script drives two distinct playfield light objects (F21, F21a) near the castle lock lane, matching the printed 'Castle' and 'Helsing' functions."),
	22: (["F22"], "(1) #906 on the playfield and (1) #906 on the back panel; the retained script drives one light object (F22) for both the printed 'L. Ramp' and 'L. Logo' functions."),
	23: (["F23"], "(1) #906 on the playfield and (1) #906 on the back panel; the retained script drives one light object (F23) for both the printed 'R. Ramp' and 'R. Logo' functions."),
	24: (["F24"], "(1) #89 on the playfield and (1) #906 on the back panel; the retained script drives one light object (F24) for both the printed 'Asylum' and 'Renfield' functions."),
	26: (["F26"], "(3) #906, all on the back panel (speaker panel); the retained table's F26 light object normalizes to a negative y (outside playfield bounds), independently corroborating the manual's backbox-only wiring."),
}

# --- Printed lamp matrix (manual page 114, printed 3-2; Lamp Locations page 107, printed 2-44).
LAMP_LABELS = {
	16: "R. Ramp Lock", 17: "Dracula Face", 18: "R. Ramp 2 Million",
	21: "Coffin Lock 1", 22: "Coffin Lock 2", 23: "Dracula A",
	24: "R. Ramp 0.5 Million", 25: "R. Ramp 1 Million", 26: "R. Ramp 2.5 Million",
	27: "R. Ramp Double", 28: "R. Ramp 1.5 Million",
	31: "R. Lane Video V", 32: "R. Lane Video I", 33: "R. Lane Video D",
	34: "R. Lane Video E", 35: "R. Lane Video O",
	36: "Dracula R", 37: "Left Drain", 38: "Left Return",
	41: "Right Return", 42: "Right Drain", 43: "Coffin Multiball",
	44: "Playfield 2X", 45: "Castle Multiball", 46: "Playfield 3X",
	47: "Mist Multiball", 48: "Dracula D",
	51: "Coffin Lamp 1", 52: "Coffin Lamp 2", 53: "Magnet",
	54: "Shoot Again", 55: "Love Never Dies", 56: "Coffin Lamp 3", 57: "L. Ramp Lock",
	58: "L. Ramp Diverted",
	61: "L. Skill 100K", 62: "M. Skill 1 Million", 63: "R. Skill 100K",
	64: "T. 3-lane Left", 65: "T. 3-lane Middle", 66: "T. 3-lane Right",
	67: "Dracula U", 68: "Jet Insert",
	71: "Dracula C", 72: "Dracula L", 73: "Left 3-bank Top", 74: "Left 3-bank Middle",
	75: "Left 3-bank Bottom", 76: "Middle 3-bank Left", 77: "Middle 3-bank Middle",
	78: "Middle 3-bank Right",
	81: "Rats Mode", 82: "Dracula A", 83: "T.L. Hole Mystery", 84: "T.L. Hole Carriage",
	85: "T.L. Hole Ex-ball", 86: "T.L. Hole Jackpot", 87: "Launch Ball", 88: "Game Start",
}
LAMP_UNUSED = {11, 12, 13, 14, 15}
LAMP_ASSEMBLIES = {
	16: ("A-11754", "#44"), 17: ("A-11754", "#44"), 18: ("A-16108", "#555"),
	21: ("A-16366-1", "#44"), 22: ("A-16366-1", "#44"), 23: ("A-16110", "#555"),
	24: ("A-16108", "#555"), 25: ("A-16108", "#555"), 26: ("A-16108", "#555"),
	27: ("A-16108", "#555"), 28: ("A-16108", "#555"),
	31: ("A-16109", "#555"), 32: ("A-16109", "#555"), 33: ("A-16109", "#555"),
	34: ("A-16109", "#555"), 35: ("A-16109", "#555"),
	36: ("A-16110", "#555"), 37: ("B-12224", "#555"), 38: ("B-12224", "#555"),
	41: ("B-12224", "#555"), 42: ("B-12224", "#555"), 43: ("A-16111", "#555"),
	44: ("A-16111", "#555"), 45: ("A-16111", "#555"), 46: ("A-16111", "#555"),
	47: ("A-16111", "#555"), 48: ("A-16110", "#555"),
	51: ("A-16523", "#555"), 52: ("A-16523", "#555"), 53: ("A-11905", "#44"),
	54: ("A-11754", "#44"), 55: ("A-11754", "#44"), 56: ("A-16523", "#555"),
	57: ("A-16511", "#555"), 58: ("B-12224", "#555"),
	61: ("A-16337", "#555"), 62: ("A-16337", "#555"), 63: ("A-16337", "#555"),
	64: ("A-16106", "#555"), 65: ("A-16106", "#555"), 66: ("A-16106", "#555"),
	67: ("A-16110", "#555"), 68: ("A-11754", "#44"),
	71: ("A-16110", "#555"), 72: ("A-16110", "#555"), 73: ("A-16511", "#555"),
	74: ("A-16511", "#555"), 75: ("A-16511", "#555"), 76: ("A-16337", "#555"),
	77: ("A-16337", "#555"), 78: ("A-16337", "#555"),
	81: ("A-11754", "#44"), 82: ("A-16110", "#555"), 83: ("A-16107", "#555"),
	84: ("A-16107", "#555"), 85: ("A-16107", "#555"), 86: ("A-16107", "#555"),
	87: ("A-15896-1", None), 88: ("20-9663-1", None),
}
# Lamps drawn only inside the manual's "A-16399 Back Panel Assy." box, never on the main
# playfield diagram; the retained table independently corroborates this (all four normalize
# to y < 0.011, sitting right at the playfield's rear edge rather than mid-playfield).
BACKBOX_LAMPS = {58, 61, 62, 63}
# Dracula name-chase inserts (letters D-R-A-C-U-L-A) and the R. Lane VIDEO chase inserts.
LAMP_DRACULA_CHASE = {48: "D", 36: "R", 23: "A", 71: "C", 67: "U", 72: "L", 82: "A"}
LAMP_VIDEO_CHASE = {31: "V", 32: "I", 33: "D", 34: "E", 35: "O"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

GI_STRINGS = {
	0: ("Lower Playfield / Insert", "J121-1", "J120-1", "Q18", "J121-7", "J120-7", "#555"),
	1: ("Upper Playfield / Insert", "J121-2", "J120-2", "Q10", "J121-8", "J120-8", "#555"),
	2: ("Center Playfield / Insert", "J121-3", "J120-3", "Q14", "J121-9", "J120-9", "#555"),
	3: ("Insert", None, "J120-5", "Q16", None, "J120-10", "#555"),
	4: ("Insert", None, "J120-6", "Q12", None, "J120-11", "#555"),
}

# --- Normalized playfield coordinates derived from the retained VPWmod v1.0 extraction
# (x/952.941, y/2117.647; see review-artifacts/dracula/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.279762, 0.040054)], 16: [(0.183657, 0.062736)], 17: [(0.943364, 0.888014)],
	25: [(0.378121, 0.141314)], 26: [(0.473133, 0.141826)], 27: [(0.569755, 0.141183)],
	28: [(0.248180, 0.226698)], 31: [(0.942700, 0.616447)],
	34: [(0.943714, 0.961670)],
	35: [(0.053912, 0.733048)], 36: [(0.129065, 0.735966)], 37: [(0.776394, 0.735917)],
	38: [(0.851310, 0.733792)],
	41: [(0.871152, 0.865797)], 42: [(0.789770, 0.887669)], 43: [(0.703057, 0.910312)],
	44: [(0.609170, 0.934625)], 48: [(0.495477, 0.964765)],
	51: [(0.832097, 0.078876)], 52: [(0.109398, 0.567897)], 53: [(0.850897, 0.549701)],
	54: [(0.812986, 0.535093)], 55: [(0.070880, 0.506130)], 56: [(0.098516, 0.412027)],
	57: [(0.773145, 0.521054)], 58: [(0.269449, 0.148727)],
	61: [(0.419036, 0.232456)], 62: [(0.628895, 0.233128)], 63: [(0.522324, 0.314927)],
	64: [(0.234533, 0.732635)], 65: [(0.681483, 0.725867)],
	66: [(0.147015, 0.454212)], 67: [(0.144622, 0.482631)], 68: [(0.142623, 0.510655)],
	71: [(0.792129, 0.532952)], 72: [(0.678707, 0.166887)], 73: [(0.130348, 0.233751)],
	77: [(0.776315, 0.192236)],
	81: [(0.409565, 0.472090)], 82: [(0.409565, 0.472090)], 83: [(0.409565, 0.472090)],
	84: [(0.895362, 0.117461)], 85: [(0.522557, 0.123063)],
	86: [(0.468406, 0.380144)], 87: [(0.530592, 0.375149)], 88: [(0.590912, 0.370173)],
}
SWITCH_PROJECTIONS = {
	34: "Projected onto the retained Plunger object (Plunger.Plunger): the Launch Ball switch is a mechanical switch on the plunger assembly itself, not a separate playfield sensor.",
	61: "Projected onto the retained Bumper2 object, which the retained script's Bumper2_Hit handler pulses as switch 61 (Left Jet).",
	62: "Projected onto the retained Bumper3 object, which the retained script's Bumper3_Hit handler pulses as switch 62 (Right Jet).",
	63: "Projected onto the retained Bumper1 object, which the retained script's Bumper1_Hit handler pulses as switch 63 (Bottom Jet).",
	64: "Projected onto the retained LeftSlingShot wall, which the retained script's LeftSlingShot_Slingshot handler pulses as switch 64.",
	65: "Projected onto the retained RightSlingShot wall, which the retained script's RightSlingShot_Slingshot handler pulses as switch 65.",
	77: "Projected onto the Right Ramp mechanism (Ramp.RightRamp): the retained script sets public switch 77 directly from the SolRRampUp/SolRRampDown solenoid commands (Controller.Switch(77) = True/False) rather than from a discrete sensor object, even though the Switch Locations parts list prints a real part number (5647-12693-36) for it.",
	81: "Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): the motorized magnet carriage has no single resting position (see the Mist Magnet mechanism), and switch 81 is set from the carriage's software-tracked position (MagnetPos > 490) rather than a discrete sensor object at a fixed location.",
	82: "Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): the retained script's MistTimer_Timer sets switch 82 from a ball-crossing line test against this same zone rather than a Hit event on a separate object; see switch 81.",
	83: "Projected onto the fixed Mist Magnet detection-zone trigger (Trigger.Magnet): switch 83 is set from the carriage's software-tracked position (MagnetPos < 10); see switch 81.",
}

SOLENOID_POSITIONS = {
	1: [(0.943714, 0.961670)],
	2: [(0.678707, 0.166887)], 3: [(0.792129, 0.532952)],
	4: [(0.776315, 0.192236)], 5: [(0.098516, 0.412027)], 6: [(0.070880, 0.506130)],
	8: [(0.940694, 0.740838)],
	9: [(0.234533, 0.732635)], 10: [(0.681483, 0.725867)],
	11: [(0.419036, 0.232456)], 12: [(0.628895, 0.233128)], 13: [(0.522324, 0.314927)],
	14: [(0.776315, 0.192236)],
	15: [(0.495477, 0.964765)],
	16: [(0.871152, 0.865797)],
	17: [(0.928339, 0.006092)],
	18: [(0.357234, 0.370633)],
	19: [(0.060191, 0.446545), (0.522646, 0.355495)],
	20: [(0.178430, 0.119540), (0.080379, 0.005735)],
	21: [(0.881604, 0.518690), (0.845181, 0.606649)],
	22: [(0.213148, 0.403852)],
	23: [(0.759221, 0.309357)],
	24: [(0.083059, 0.369293)],
	25: [(0.279762, 0.040054)],
	27: [(0.409565, 0.472090)], 28: [(0.409565, 0.472090)],
	33: [(0.740491, 0.051904)], 34: [(0.840463, 0.415911)],
	35: [(0.878573, 0.559420)], 36: [(0.163790, 0.560275)],
	45: [(0.620992, 0.841783)], 46: [(0.620992, 0.841783)],
	47: [(0.287666, 0.841783)], 48: [(0.287666, 0.841783)],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Bram Stoker's Dracula retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Dracula extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Dracula retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Dracula retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Dracula retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


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
			"locator": "Pinned catalog driver records for the drac_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/drac.c dracGameData GEN_WPCFLIPTRON with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x00,0x00,0x7f,0x00,0x07,0x02,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), "
				"swStart/swTilt/swSlamTilt/swCoinDoor/swLaunch defines, the full switch/solenoid #define block, "
				"drac_handleMech (coffin ramp, drop target, mist magnet position counter, top diverter timing), and "
				"init_drac; src/wpc/core.h CORE_FIRSTUFLIPSOL=33 (sURFlipPow/sURFlip=33/34, sULFlipPow/sULFlip=35/36) "
				"and CORE_FIRSTLFLIPSOL=45 (sLRFlipPow/sLRFlip=45/46, sLLFlipPow/sLLFlip=47/48); "
				"src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCFLIPTRON=0x8"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-fliptronic.json",
			"revision": "repository",
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules, including the 111-118 Fliptronic ordering and the 33-36/45-48 solenoid ranges",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.bram-stoker-s-dracula.1993/archive-arcademanual_Dracula_Bram_Stoker_OPS/Dracula_Bram_Stoker_OPS.pdf",
			"original_filename": "Dracula_Bram_Stoker_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"152-page scan of the Williams Bram Stoker's Dracula operations manual. Printed pages 2-44 through "
				"2-46 carry the lamp/solenoid/switch location parts lists; printed pages 3-2 through 3-21 carry the "
				"lamp matrix, switch matrix, dedicated switches, solenoid/flasher table, general illumination "
				"circuit, and Fliptronic II flipper circuit diagrams."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.dracula.switch-matrix",
					"locator": "PDF page 116, printed page 3-4, SWITCH MATRIX table",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/switch-matrix.md",
					"sha256": "79bbed0a5505932a768bad9953ec6f0073a7952e4576bffdf22f6420f97fa2ac",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.dracula.switch-locations",
					"locator": "PDF page 109, printed page 2-46, SWITCH LOCATIONS parts list",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/switch-locations.md",
					"sha256": "77beb5087c6ef86f1a2be178fce9a8ebf9bb7452df01b8839a4f9f35aeb2364d",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.dracula.lamp-matrix-and-locations",
					"locator": "PDF page 114 (printed 3-2, Lamp Matrix) and PDF page 107 (printed 2-44, Lamp Locations)",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/lamp-matrix-and-locations.md",
					"sha256": "689739d03e65c1a8c4e11d4f2c2b283f7e0613dbec51a353b56e182ac12cc958",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.dracula.solenoid-flasher-locations",
					"locator": "PDF page 108, printed page 2-45, SOLENOID/FLASHER LOCATION parts list",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/solenoid-flasher-locations.md",
					"sha256": "922af198d7e0d07ceec89fa162fcdb6bf4eebe211f4f1afed862d583c74a3c33",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.dracula.solenoid-flasher-wiring",
					"locator": "PDF page 120, printed page 3-8, SOLENOID/FLASHER TABLE",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/solenoid-flasher-wiring.md",
					"sha256": "68a9465bd5a0981182055b0be1f9a1cd30202b1d81c6c46821b26d5abdecbab6",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.dracula.general-illumination",
					"locator": "PDF page 120 (printed 3-8, GI rows) and PDF page 128 (printed 3-16, GI circuit theory)",
					"path": "evidence/excerpts/williams.bram-stoker-s-dracula.1993/general-illumination.md",
					"sha256": "35c8c78bc4dcbf77b6b97539cad8bf6080794ae7891172a98884be07dba13dcb",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/dracula/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with "
				"the rendered PNG page cache under external:pinmame-manuals/rendered/williams.bram-stoker-s-dracula.1993/ "
				"and the raw VPX geometry dump external:pinmame-review-artifacts/dracula/vpx-geometry.txt."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/source/Bram%20Stokers%20Dracula%20%28Williams%201993%29%20VPW%201.0.vpx",
			"original_filename": "Bram Stokers Dracula (Williams 1993) VPW 1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPW recreation of the physical machine, VPX version 10.6. Exact playfield "
				f"bounds are {TABLE_BOUNDS}; normalized coordinates are x/952.941 and y/2117.647. Geometry authority "
				"only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (236,233 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "drac_l1", the SolCallback/SolModCallback table for solenoids 1-8, 14, 16, 25, 27, '
				"33-36, and core.vbs sLRFlipper/sLLFlipper, the Controller.Switch semantics for the trough/castle-"
				"lock/mist-magnet state machines, GIUpdate2 mapping GI 0/1/2 to the GIBOT/GITOP/GIMID playfield "
				"emitter collections and GI 3/4 to single backbox bulbs gibg4/gibg5, and the Flasher17-Flasher26 "
				"callbacks naming their driven Light objects directly."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": IPDB_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?gid=3072",
			"revision": "2026-08-07",
			"locator": (
				"IPDB machine number 3072 for Williams' Bram Stoker's Dracula (1993), model number 50001. The IPDB "
				"page itself returns HTTP 403 to unauthenticated fetches (Cloudflare-gated); this identity is "
				"corroborated by the search engine's own crawled page title (\"Internet Pinball Machine Database: "
				"Williams 'Bram Stoker's Dracula'\" at this exact gid) together with independently consistent "
				"Wikipedia and Pinside entries for the same title/manufacturer/year, rather than a rendered fetch of "
				"the gated page."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database",
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
		"board": "WPC CPU board",
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
		wire, connection = DEDICATED_SWITCH_WIRING[address]
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
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
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
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed switch matrix marks this position Not Used."
				if address == 23:
					notes += (
						' The matrix page itself prints "Ticket Opto." at this address, but the Switch Locations '
						"parts list (page 109, printed 2-46) prints a blank Switch No. with \"Not Used\" -- the blank "
						"parts-list entry is physical-fitment ground truth (same resolution as Williams Indiana "
						"Jones's switch 23)."
					)
			elif address in OPTO_SWITCHES:
				notes += (
					' Printed "Opto ___" on the switch matrix (columns 5 and 7 rows 1-3) or, for switch 82 alone, '
					"proven opto by the Switch Locations parts list (A-14315 LED with A-14316 phototransistor) "
					"while its column-8 neighbors 81 and 83 use the plain leaf part 5647-12693-14. Pinned PinMAME's "
					"dracGameData inverted-switch mask "
					"({0x00,0x00,0x00,0x00,0x00,0x7f,0x00,0x07,0x02,0x00,0x00,0x00}, column 5 = 0x7f rows 1-7, "
					"column 7 = 0x07 rows 1-3, column 8 = 0x02 row 2) normalizes every one of these addresses "
					"exactly, with zero disagreement anywhere in the matrix."
				)
			if address == 24:
				notes += " Physical part 5643-09288-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 84:
				notes += ' Printed "L. Ramp Score" on the Lamp/Switch pages and driver symbol swLRampMade ("L Ramp Made"); both describe the same rollover.'
			if address == 85:
				notes += ' Printed "L. Ramp Diverted" and driver symbol swLRampDivMade; both describe the ramp diverter rollover.'
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
				if address in {13, 14, 21, 22}:
					role = {
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address == 13 else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-193", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, None, None, "5490-12451-00"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-193", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, None, None, "5490-12451-00"),
		115: ("Not Fitted Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		116: ("Not Fitted Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
		117: ("Not Fitted Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		118: ("Not Fitted Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, assembly, part_number) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if assembly:
			physical["assembly_part_number"] = assembly
		if part_number:
			physical["part_number"] = part_number
		notes = f"Printed Fliptronic II grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" This machine has no physical upper flippers: the Switch Locations parts list (page 109, printed "
				"2-46) has no row at all for F5-F8 (unlike the fitted F1-F4, each of which carries a real part "
				"number), the Solenoid/Flasher Table has only two flipper-coil rows (Lower Left, Lower Right, no "
				"Upper row), and the retained known-working script never references public switches 115-118 "
				"anywhere. The Switch Matrix page and the generic Fliptronic II Flipper Cabinet Switch / "
				"End-of-Stroke circuit-diagram pages (3-17 through 3-21) still print all eight F1-F8 positions "
				"descriptively, matching pinned PinMAME's own dracGameData FLIP_SW(FLIP_L|FLIP_U) bit, which reads "
				"the upper positions' button state regardless of physical fitment; this is a known WPC-Fliptronic "
				"driver characteristic, not evidence of real hardware."
			)
			physical["location"] = "not installed"
		physical["notes"] = notes
		extra = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
		}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
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

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				f"CPU DIP {address} (country/option configuration bit)",
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
					"location": "WPC CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC CPU-board country/option configuration DIP bank. The retained transcription of this "
						"manual does not include a per-country switch-combination chart, so no specific ON/OFF "
						"combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	import re

	return f"device.{re.sub(r'[^a-z0-9]+', '-', label.casefold()).strip('-')}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			kind = "flasher" if (17 <= address <= 24 or address == 26) else "motor" if address == 28 else "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher":
				objects, bulb_note = FLASHER_OBJECTS[address]
				physical["quantity"] = len(objects)
				notes += f" {bulb_note}"
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {33, 34, 35, 36}:
				notes += (
					" Wired through the otherwise-unpopulated upper-flipper power/hold driver-transistor pair "
					"(this machine has no upper flippers); see conflict.upper-flipper-circuit-side-naming for the "
					"disagreement between pinned PinMAME's own macro naming and this manual's printed circuit-side "
					"label."
				)
			if address in {45, 46, 47, 48}:
				notes += " PinMAME's public lower-flipper addresses 45-48 are identically numbered on the printed table (no alias needed)."
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": wiring_data["driver_transistor"]}
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.solenoid", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
				"wiring": wiring,
			}
			availability = "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 26:
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 7:
				extra["roles"] = ["cabinet.knocker"]
				physical["notes"] += " The Knocker is a cabinet-mounted device (behind the coin door / under the playfield front), not a playfield-visible effect."
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 32} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Dracula playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Dracula playfield device.",
			31: "PinMAME's synthetic game-on state, taken from the driver's fast-flip RAM flag.",
			32: "PinMAME reports this WPC state channel as always zero.",
			37: "Unused WPC-Fliptronic output; this generation has no LPDC board, so 37-44 are simply unused address space (pinned core_getSol only serves that range for GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11).",
			38: "Unused WPC-Fliptronic output; see 37.",
			39: "Unused WPC-Fliptronic output; see 37.",
			40: "Unused WPC-Fliptronic output; see 37.",
			41: "Unused WPC-Fliptronic output; see 37.",
			42: "Unused WPC-Fliptronic output; see 37.",
			43: "Unused WPC-Fliptronic output; see 37.",
			44: "Unused WPC-Fliptronic output; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-Fliptronic hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. dracGameData declares no custSol.",
		}[address]
		roles = ["internal.wpc-state"] if address in {29, 30, 31, 32} else ["internal.unused.wpc-output"]
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
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
			unused = address in LAMP_UNUSED
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES.get(address, (None, None))
			physical: dict[str, Any] = {}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_DRACULA_CHASE:
				notes += (
					f' Dracula name-chase insert, letter "{LAMP_DRACULA_CHASE[address]}"; the seven name-chase '
					"lamps (23, 36, 48, 67, 71, 72, 82) spell D-R-A-C-U-L-A in address order "
					"48-36-23-71-67-72-82."
				)
			if address in LAMP_VIDEO_CHASE:
				notes += (
					f' R. Lane VIDEO-chase insert, letter "{LAMP_VIDEO_CHASE[address]}"; addresses 31-35 spell '
					"VIDEO in already-ascending order."
				)
			if address == 63:
				notes += (
					' Internal manual disagreement: the Lamp Matrix wiring page (114, printed 3-2) prints this '
					'address "R. Skill 100K", while the Lamp Locations parts list (page 107, printed 2-44) prints '
					'the same address "R Skill 500K". Both are transcribed; neither is preferred, since this is a '
					"backbox scoring-legend value with no bearing on wiring, polarity, or placement."
				)
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
					"board": "WPC power driver board",
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
				physical["notes"] = f"Printed lamp-matrix drive column {column}, return row {row}. The lamp-locations parts list marks this position Not Used."
			elif address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.launch" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in BACKBOX_LAMPS:
				availability = "used"
				extra["roles"] = ["cabinet.insert-panel"]
				physical["notes"] += (
					' Drawn only inside the manual\'s "A-16399 Back Panel Assy." box, above the main playfield '
					"diagram; the retained table's own Light object normalizes to y < 0.011, sitting right at the "
					"playfield's rear edge rather than a genuine mid-playfield position, independently corroborating "
					"backbox mounting."
				)
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_TABLE_SOURCE)
			elif address == 53:
				availability = "used"
				physical["notes"] += (
					" No matching Light object exists anywhere in the retained extraction and script.vbs never "
					"references it; the spatial key is omitted rather than a coordinate being invented."
				)
				# spatial intentionally omitted -- see coverage.missing.
			else:
				availability = "used"
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label if label else f"Not Used Lamp Position {address}",
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
	16: [(0.806771, 0.182557)], 17: [(0.657766, 0.542287)], 18: [(0.783927, 0.384343)],
	21: [(0.644187, 0.179645)], 22: [(0.708200, 0.179645)], 23: [(0.597604, 0.658152)],
	24: [(0.718173, 0.403631)], 25: [(0.674973, 0.373897)], 26: [(0.728976, 0.378636)],
	27: [(0.773223, 0.316364)], 28: [(0.740043, 0.353911)],
	31: [(0.916319, 0.236954)], 32: [(0.897539, 0.267921)], 33: [(0.878011, 0.295898)],
	34: [(0.859247, 0.324080)], 35: [(0.840900, 0.352221)],
	36: [(0.354714, 0.647211)], 37: [(0.054949, 0.681319)], 38: [(0.130941, 0.665085)],
	41: [(0.776015, 0.664585)], 42: [(0.853306, 0.680600)], 43: [(0.375085, 0.794122)],
	44: [(0.419649, 0.821083)], 45: [(0.455193, 0.789716)], 46: [(0.488526, 0.821365)],
	47: [(0.533150, 0.793726)], 48: [(0.309165, 0.658715)],
	51: [(0.678239, 0.187378)], 52: [(0.678239, 0.222383)],
	54: [(0.455013, 0.856410)], 55: [(0.456247, 0.897615)], 56: [(0.678063, 0.258980)],
	57: [(0.212604, 0.402881)],
	64: [(0.364312, 0.080868)], 65: [(0.474418, 0.081069)], 66: [(0.582991, 0.081697)],
	67: [(0.504051, 0.640521)], 68: [(0.518253, 0.252618)],
	71: [(0.453926, 0.637547)], 72: [(0.552275, 0.647014)], 73: [(0.222481, 0.452599)],
	74: [(0.221242, 0.482700)], 75: [(0.217277, 0.514325)], 76: [(0.472313, 0.412116)],
	77: [(0.539079, 0.406169)], 78: [(0.607354, 0.400899)],
	81: [(0.765908, 0.558615)], 82: [(0.402371, 0.640375)], 83: [(0.297337, 0.214954)],
	84: [(0.318386, 0.268034)], 85: [(0.337834, 0.318435)], 86: [(0.356830, 0.370687)],
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, pf_conn, bb_conn, transistor, pf_drive, bb_drive, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		power_connection = f"{pf_conn} (pf), {bb_conn} (bb)" if pf_conn else f"{bb_conn} (bb)"
		control_connection = f"{pf_drive} (pf), {bb_drive} (bb)" if pf_drive else f"{bb_drive} (bb)"
		wiring: dict[str, Any] = {
			"board": "WPC power driver board",
			"driver_transistor": transistor,
			"power_connection": power_connection,
			"control_connection": control_connection,
		}
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": wiring,
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's GI emitter collection for this string (GIUpdate2 in the retained "
				"script). GI address 0 drives collection GIBOT; GI address 1 drives GITOP; GI address 2 drives GIMID."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox-only circuit with no playfield voltage or drive connection printed; the retained script's "
				"GIUpdate2 drives a single non-playfield bulb (gibg4 for address 3, gibg5 for address 4) rather than "
				"a playfield collection."
			)
			if address == 4:
				notes += " This string additionally feeds a cabinet bulb through J119, the only cabinet connection on the printed general-illumination wiring."
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


GI_POSITIONS = {
	0: [
		(0.181349, 0.697785), (0.209961, 0.758311), (0.152710, 0.799887), (0.218758, 0.820662),
		(0.727456, 0.697270), (0.698084, 0.757507), (0.751802, 0.799142), (0.689026, 0.819948),
	],
	1: [
		(0.091266, 0.345141), (0.071111, 0.284643), (0.180203, 0.170039), (0.199053, 0.134944),
		(0.156562, 0.042262), (0.231922, 0.083680), (0.277033, 0.104577), (0.329195, 0.144606),
		(0.423693, 0.144060), (0.520742, 0.145104), (0.615678, 0.144714), (0.661355, 0.116748),
		(0.682169, 0.097181), (0.726476, 0.074712), (0.925264, 0.058214), (0.932671, 0.093777),
		(0.858865, 0.180843), (0.713580, 0.221754), (0.929464, 0.319585), (0.915525, 0.337482),
	],
	2: [
		(0.039222, 0.556640), (0.112906, 0.465945), (0.113991, 0.446151), (0.491500, 0.367420),
		(0.567701, 0.348021), (0.838075, 0.481935), (0.863311, 0.534023), (0.824171, 0.586837),
		(0.861532, 0.625491), (0.528729, 0.561740),
	],
}


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
		*refs: str,
	) -> dict[str, Any]:
		return {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}

	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough",
			"kicker",
			[output_id("Trough"), output_id("Outhole")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44", "switch.matrix-48"],
			"Four balls rest on trough switches 41-44 (Trough 1-4 Ball), Trough 1 (41) nearest the eject end. "
			"Solenoid 16 (Trough) ejects the ball resting on 41 to the shooter lane; the outhole (switch 48) feeds "
			"drained balls into the trough via solenoid 15 (Outhole). The retained script's SolRelease callback "
			"drives this directly; none of these five switches is a printed opto (column 4's inverted-switch mask "
			"row is 0x00).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.castle-lock",
			"Castle Lock lane and release post",
			"gate",
			[output_id("Castle Release Post")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-57"],
			"A three-position lock lane behind the Left Ramp diverter queues balls on opto switches 57 (Castle "
			"Lock 3, entry), 54 (Castle Lock 2), and 53 (Castle Lock 1, exit, nearest the release post). Solenoid "
			"35 (Castle Release Post, printed 'Dis. Castle Release Pst', wired through the otherwise-unused "
			"upper-flipper power driver transistor) retracts the post (clpost.isdropped=0) to release the queued "
			"ball at position 53 toward the shooter lane; the retained script's clpost_Timer sub restores the post "
			"280 ms later. All three lock switches are genuine opto interrupters (A-14315/A-14316) that pinned "
			"PinMAME's inverted-switch mask normalizes (column 5 = 0x7f, rows 3/4/7).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.mist-magnet",
			"Mist Magnet ball-levitation carriage",
			"other",
			[output_id("Magnet"), output_id("Magnet's Motor")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-83"],
			"A single magnet is mounted on a motor-driven carriage (solenoid 28, 'Magnet's Motor') that travels "
			"diagonally beneath the playfield between a right-side entry near the Right Gate and a left-side exit "
			"near the Left Gate. The retained script tracks the carriage's position purely in software as a 0-500 "
			"counter (MagnetPos), incremented or decremented while solenoid 28 is energized and reversing direction "
			"at each endpoint; it has no single resting coordinate. Two plain leaf limit switches confirm the "
			"carriage has reached an end of travel: switch 81 (Magnet Left, part 5647-12693-14) asserts near "
			"MagnetPos=500 (the left/exit end, feeding the Left Gate) and switch 83 (Magnet Right, same part) "
			"asserts near MagnetPos=0 (the right/entry end, feeding the Right Gate) -- neither is a printed opto. "
			"Switch 82 (Ball On Magnet) is the only genuine opto of the three (A-14315/A-14316): the retained "
			"script's MistTimer_Timer tests every ball's position against a fixed diagonal line equation "
			"representing the physical beam, independent of carriage position, and PinMAME's inverted-switch mask "
			"normalizes only this one address in column 8 (0x02). Solenoid 27 (Magnet) is the electromagnet coil "
			"itself, energized by SolMistMagnet to hold a captive ball on the carriage while it travels; the "
			"driver's own stMagnet ball-state case requires the magnet to be both energized and at the correct "
			"switch/position combination before releasing the ball toward the matching gate.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.mist-gates",
			"Left and Right Mist Magnet entry gates",
			"gate",
			[output_id("Left Gate Actuator"), output_id("Right Gate")],
			["switch.matrix-52"],
			"One-way gates admit a ball onto the Mist Magnet carriage from either side. Solenoid 34 (Right Gate, "
			"printed 'Right Gate', wired through the otherwise-unused upper-flipper power driver transistor) opens "
			"a gate near the top-right loop (RGate.open, plus dropping RGateWall) so a ball can fall onto the "
			"carriage from the right; solenoid 36 (Left Gate Actuator, printed 'Left Ball Gate Actuator') opens a "
			"gate near the Magnet Left Pocket opto (switch 52, LGate.open, plus dropping Wall_LO) admitting a ball "
			"from the left. The driver's own ball-state chain confirms both paths lead to stMagnet.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.right-ramp",
			"Moving Right Ramp / Coffin Ramp section",
			"diverter",
			[output_id("Right Ramp Down"), output_id("Right Ramp Up")],
			["switch.matrix-77"],
			"A section of the Right Ramp raises and lowers to route the ball either up the ramp or over a hump "
			"toward the Coffin Popper. Solenoid 14 (Right Ramp Up) raises it and sets the retained script's "
			"Controller.Switch(77) True; solenoid 4 (Right Ramp Down) lowers it and clears the same public switch. "
			"The Switch Locations parts list prints a real part number for switch 77 (5647-12693-36), but the "
			"retained script sets its public state directly from the solenoid commands rather than reading a "
			"discrete sensor -- an implementation simplification, not a source disagreement.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.shooter-ramp",
			"Shooter Ramp entry diverter",
			"diverter",
			[output_id("Shooter Ramp Entry")],
			[],
			"A small flap near the auto-plunger lane diverts the auto-launched ball either up a habitrail loop "
			"(solenoid 8 energized) or lets it fall through toward the Left Loop (solenoid 8 off), per the driver's "
			"stBallLane ball-state case. No discrete switch reports this flap's position.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.top-diverter",
			"Up/Down Post Diverter",
			"diverter",
			[output_id("Up/Down Post Diverter")],
			["switch.matrix-73"],
			"A spring-loaded post near the top of the playfield (printed 'Up/Dn Post Diverter', solenoid 33, wired "
			"through the otherwise-unused upper-flipper power driver transistor) toggles the ball between two "
			"orbit/ramp paths. Left Ramp Entry (opto switch 73) senses a ball entering the diverted path.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.drop-target",
			"Single Left Drop Target",
			"drop_target_bank",
			[output_id("L. Drop Target Reset")],
			["switch.matrix-15", "switch.matrix-16"],
			"A single drop target (not a bank) near the top-left lanes. Hitting it drops the target (switch 15, "
			"L. Drop Target) and reveals a rollover behind it (switch 16, L. Drop Score) that scores the ball's "
			"passage. Solenoid 25 (L. Drop Target Reset) raises it again after a delay via the retained script's "
			"SolDTUp callback. This corrects an earlier candidate note that described a '3-bank drop target' at "
			"this address; the retained script instantiates exactly one DropTarget object (`DT15`) for switch 15, "
			"and the genuine 3-bank standup-target arrays are the unrelated Left 3-bank (66/67/68) and Middle "
			"3-bank (86/87/88) banks.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject",
			"kind": "pulse",
			"source": output_id("Trough"),
			"destination": "switch.matrix-41",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.upper-flipper-circuit-side-naming",
			"path": "outputs[binding.device=33,34,35,36]",
			"description": (
				"Solenoids 33-36 are wired through the Fliptronic board's otherwise-unused upper-flipper power/hold "
				"driver-transistor pairs (this machine has no physical upper flippers). Pinned PinMAME's own "
				"src/wpc/core.h macros name CORE_FIRSTUFLIPSOL(33)/34 as sURFlipPow/sURFlip -- the upper-RIGHT "
				"circuit -- and 35/36 as sULFlipPow/sULFlip -- the upper-LEFT circuit. This manual's own printed "
				"Solenoid/Flasher Table (page 120, printed 3-8) labels the identical two circuits the opposite way "
				"round: 'Up Lt. F. Power/Hold' at 33/34 and 'Up Rt. F. Power/Hold' at 35/36. Neither the device "
				"functions (Up/Down Post Diverter, Right Gate, Castle Release Post, Left Gate Actuator) nor their "
				"public addresses are in doubt on either source; only which now-repurposed flipper-side driver "
				"transistor pair physically underlies each address disagrees. Unresolved; recorded for provenance "
				"completeness rather than blocking the device labels, which are taken directly from the manual's "
				"function column."
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
			"id": "williams.bram-stoker-s-dracula.1993",
			"name": "Bram Stoker's Dracula",
			"manufacturer": "Williams",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 3072,
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
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
			"platform": "pinmame.wpc-fliptronic",
			"hardware_generation": "0x8",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/dracula.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Dracula device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
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
		elif spatial["status"] == "not_applicable":
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
			"Lamp 53 (Magnet, #44) is a genuine bulb per the Lamp Locations parts list but has no matching Light "
			"object anywhere in the retained extraction and is never referenced in script.vbs, so it has no "
			"resolvable spatial evidence. Its `spatial` key is omitted rather than a coordinate being invented; "
			"every other dimension this report audits is complete.",
			"Solenoids 33-36 are wired through the Fliptronic upper-flipper driver-transistor pairs, and pinned "
			"PinMAME's own macro naming disagrees with this manual's printed circuit-side label about which pair "
			"is which (conflict.upper-flipper-circuit-side-naming). This does not affect any device's address or "
			"function, which are taken from the manual directly, but it is an unresolved disagreement between "
			"equal-authority sources and keeps physical_wiring conflicted.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.941, "bottom": 2117.647},
			"x": "x/952.941; 0=left, 1=right",
			"y": "y/2117.647; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/bram-stokers-dracula-1993/extracted-vpxtool.manifest.json",
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
		"unresolved_inputs": sorted(unresolved_inputs),
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.bram-stoker-s-dracula.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/dracula/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [],
		"unresolved": ["lamp.matrix-53"],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Bram Stoker's Dracula (Williams, 1993) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete except one lamp with no "
		"retained geometry, but the physical machine record itself remains `partial` at "
		"`machines/partial/williams/bram-stoker-s-dracula-1993.json` because of that gap plus an unresolved "
		"wiring-provenance conflict outside this audit's scope; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Bram Stokers Dracula (Williams 1993) VPW 1.0.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at "
		f"SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952.941 and y/2117.647 rounded to at "
		"most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations manual "
		"is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- This manual marks opto-construction switches by writing \"Opto\" directly into the printed switch-"
		"matrix label rather than by shading. Columns 5 and 7 match pinned PinMAME's inverted-switch mask exactly; "
		"column 8's single opto (switch 82) is resolvable only from the Switch Locations parts list, where 81 and "
		"83 use the plain leaf part 5647-12693-14 -- zero polarity disagreement across the whole matrix.",
		"- Switches 61-65 (jets and slingshots) and 77 (Right Ramp Up) have no dedicated playfield trigger object; "
		"the retained script pulses their public state directly from the Bumper/Wall objects' Hit events or from "
		"solenoid commands, so they are documented projections onto the real mechanism object.",
		"- Switches 81/82/83 (Mist Magnet) have no fixed sensor object: the motorized carriage's position is "
		"tracked purely in software, so all three are projected onto the fixed Trigger.Magnet detection zone.",
		"- Flasher addresses with two manual-printed functions per circuit (19, 20, 21) drive two distinct "
		"retained Light objects and get two placements; addresses with one manual-printed function pair sharing a "
		"single retained Light object (17, 18, 22, 23, 24) get one placement, disclosed in physical.notes.",
		"- GI strings 0-2 use the retained table's GIBOT/GITOP/GIMID emitter collections, matching the retained "
		"script's GIUpdate2 dispatch exactly with zero script-vs-manual disagreement. GI strings 3 and 4 are "
		"backbox-only circuits and take a controlled `cabinet_or_service` record.",
		"- Four lamps (58, 61, 62, 63) are drawn only inside the manual's separate \"Back Panel Assy.\" box; the "
		"retained table corroborates this independently (all four normalize to y < 0.011). They take a controlled "
		"`cabinet_or_service` record.",
		"- Lamp 53 (Magnet) has no retained Light object and no script reference; its `spatial` key is omitted "
		"entirely rather than a coordinate being invented, and it is the sole entry in `coverage.missing`'s "
		"spatial gap.",
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
		f"- Unresolved inputs (no spatial key): {report['unresolved_inputs']}",
		f"- Unresolved outputs (no spatial key): {report['unresolved_outputs']}",
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
		"this audit covers except lamp 53, and the deterministic curator reproduces the canonical artifact and "
		"its pinned seed byte-for-byte. Lamp 53 (Magnet, #44) is a genuine bulb per the manual with no resolvable "
		"geometry in the retained extraction, and solenoids 33-36 carry an unresolved disagreement between pinned "
		"PinMAME's own macro naming and this manual's printed circuit-side label about which upper-flipper driver "
		"pair underlies each address (`conflict.upper-flipper-circuit-side-naming`). The definition therefore "
		"carries a non-empty `conflicts` array and `coverage.dimensions.physical_wiring = \"conflicted\"`, so "
		"promotion to `author_ready` is refused; the record stays `partial` with `coverage.missing = "
		"[\"spatial_placement\", \"unresolved_conflicts\"]`.",
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
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if not definition_path.is_file():
		raise RuntimeError(f"Dracula definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Dracula seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Dracula definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Dracula seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Dracula spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Dracula spatial review drifted from its deterministic curator: {markdown_path}")
	print("Dracula definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Dracula extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Dracula retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
