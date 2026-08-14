"""Curate the physical Williams The Getaway: High Speed II (1992) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift,
and ``--regenerate`` is the only path that writes the canonical definition and its pinned seed.
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
PARTIAL_PATH = ROOT / "machines/partial/williams/the-getaway-high-speed-ii-1992.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/the-getaway-high-speed-ii-1992.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/the-getaway-high-speed-ii-1992.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/the-getaway-high-speed-ii-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/the-getaway-high-speed-ii-1992.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.williams.the-getaway-high-speed-ii.1992"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.the-getaway-high-speed-ii.1992"
VPX_TABLE_SOURCE = "vpx-table.gw-v1.2"
VPX_SCRIPT_SOURCE = "vpx-script.gw-v1.2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.gw-v1.2"

TABLE_SHA256 = "22e7257316dcb3c414f62a0543f6a68063e8f50524ad9559f1ff98bd38184efc"
SCRIPT_SHA256 = "4f91dbf71bf134b1113939a517900c27d87fa1a142109e79ad64306a40aeb78e"
MANUAL_SHA256 = "9d59b0d38fff9cf8b87cbee5defb205700ae42b79f00cdd509a1137a7ce96558"
MANUAL_TRANSCRIPTION_SHA256 = "a450922126d99280fb9accedbe3c40cf00a70fde102ad541fb322b0521f0743f"

EXTRACTION_RELATIVE_PATH = Path("williams/the-getaway-high-speed-ii-1992/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/the-getaway-high-speed-ii-1992/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 875

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

DRIVER_IDS = (
	"gw_l5", "gw_d5", "gw_l5c", "gw_pb", "gw_pc", "gw_pd", "gw_p7", "gw_p8",
	"gw_l1", "gw_d1", "gw_l2", "gw_d2", "gw_l3", "gw_d3",
)
DRIVER_COMPATIBILITY = {
	"gw_l5": ("identical", "Williams production L-5 game ROM shipped with the physical machine; the retained known-working table binds this driver."),
	"gw_d5": ("identical", "Williams D-5 LED Ghost Fix game ROM; a display-timing firmware revision of the identical physical machine."),
	"gw_l5c": ("identical", "2017 community L-5C \"Competition MOD\" patch (rev. L-5 patch bc43) for the identical physical hardware, in scope as a driver/ROM variant of the same physical machine."),
	"gw_pb": ("identical", "P-B prototype game ROM; a pre-production firmware revision of the identical physical machine."),
	"gw_pc": ("identical", "P-C prototype game ROM; a pre-production firmware revision of the identical physical machine."),
	"gw_pd": ("identical", "P-D LED Ghost Fix prototype game ROM; a pre-production firmware revision of the identical physical machine."),
	"gw_p7": ("identical", "P-7 prototype game ROM; a pre-production firmware revision of the identical physical machine."),
	"gw_p8": ("identical", "P-8 LED Ghost Fix prototype game ROM; a pre-production firmware revision of the identical physical machine."),
	"gw_l1": ("identical", "Williams L-1 game ROM; an earlier production firmware revision of the identical physical machine."),
	"gw_d1": ("identical", "Williams D-1 LED Ghost Fix game ROM; a display-timing firmware revision of the identical physical machine."),
	"gw_l2": ("identical", "Williams L-2 game ROM; an earlier production firmware revision of the identical physical machine."),
	"gw_d2": ("identical", "Williams D-2 LED Ghost Fix game ROM; a display-timing firmware revision of the identical physical machine."),
	"gw_l3": ("identical", "Williams L-3 game ROM; an earlier production firmware revision of the identical physical machine."),
	"gw_d3": ("identical", "Williams D-3 LED Ghost Fix game ROM; a display-timing firmware revision of the identical physical machine."),
}

# --- Printed switch matrix (manual page 2-40 Switch Locations parts list; page 3-4 SWITCH MATRIX wiring).
SWITCH_LABELS = {
	13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Freeway Bottom", 16: "Left Freeway Top", 17: "Right Freeway Bottom", 18: "Right Freeway Top",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Dispenser", 24: "Always Closed",
	25: "Left Outlane", 26: "Left Return Lane", 27: "Right Return Lane", 28: "Right Outlane",
	31: "Left Slingshot", 32: "Right Slingshot", 33: "Gear Shifter Low", 34: "Gear Shifter High",
	36: "Top Red Target", 37: "Middle Red Target", 38: "Bottom Red Target",
	41: "Top Yellow Target", 42: "Middle Yellow Target", 43: "Bottom Yellow Target",
	44: "Right Bank Bottom Target", 45: "Right Bank Middle Target", 46: "Right Bank Top Target",
	51: "Top Green Target", 52: "Middle Green Target", 53: "Bottom Green Target",
	54: "Ramp Down", 55: "Outhole", 56: "Left Trough", 57: "Center Trough", 58: "Right Trough",
	61: "Top Jet Bumper", 62: "Left Jet Bumper", 63: "Bottom Jet Bumper",
	65: "Made Up/Down Ramp", 67: "Made Left Ramp",
	71: "Top Loop", 72: "Middle Loop", 73: "Bottom Loop",
	74: "Top Lock", 75: "Middle Lock", 76: "Bottom Lock", 77: "Eject Hole", 78: "Shooter Lane",
	81: "Opto 1", 82: "Opto 2", 83: "Opto 3", 84: "Opto Made Loop", 85: "Enter Left Ramp",
	86: "Left Bank Bottom Target", 87: "Left Bank Middle Target", 88: "Left Bank Top Target",
}
# Printed "Not Used" on both the Switch Locations parts list and the SWITCH MATRIX wiring page.
UNUSED_MATRIX_ADDRESSES = {11, 12, 35, 47, 48, 64, 66, 68}
# The five switches whose Switch Locations row prints a paired opto LED/phototransistor part
# (A-14316 Trans / A-14315 LED) -- swept exhaustively across the entire 11-88 address range.
# Independently confirmed by the two dedicated opto driver boards (A-15189 Accelerator Board for
# 81-83; A-13901-1 Opto Ramp Switch Board for 84-85), each of which names the LED/Transistor pins
# per address explicitly.
OPTO_SWITCHES = {81, 82, 83, 84, 85}
# gwGameData's inverted-switch mask ({0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1f,0x00,0x00,0x00})
# sets column 8 bits 0-4 (rows 1-5), i.e. exactly addresses 81-85. Zero disagreement with the sweep.
PINMAME_NORMALIZED_OPTO_SWITCHES = {81, 82, 83, 84, 85}

SWITCH_TYPES = {
	13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch", 18: "microswitch",
	21: "leaf", 22: "microswitch", 23: "other", 24: "other", 25: "microswitch", 26: "microswitch",
	27: "microswitch", 28: "microswitch", 31: "leaf", 32: "leaf", 33: "microswitch", 34: "microswitch",
	36: "microswitch", 37: "microswitch", 38: "microswitch", 41: "microswitch", 42: "microswitch",
	43: "microswitch", 44: "microswitch", 45: "microswitch", 46: "microswitch",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 65: "microswitch", 67: "microswitch",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "microswitch", 75: "microswitch",
	76: "microswitch", 77: "microswitch", 78: "microswitch",
	81: "opto", 82: "opto", 83: "opto", 84: "opto", 85: "opto",
	86: "microswitch", 87: "microswitch", 88: "microswitch",
}

# address -> (switch part, switch assy part), transcribed verbatim from the Switch Locations page
# (2-40); a leading "opto" tuple marks the paired LED/Trans opto part instead.
SWITCH_PARTS: dict[int, tuple[str | None, str | None]] = {
	13: (None, "20-9663-1"), 14: (None, "20-6502-A"),
	15: ("5647-12693-19", "A-12688L"), 16: ("5647-12693-19", "A-12688L"),
	17: ("5647-12693-19", "A-12688R"), 18: ("5647-12693-19", "A-12688R"),
	21: (None, "20-1066"), 22: (None, "A-8630"), 24: (None, "A-8630"),
	25: ("5647-12693-19", "A-12688"), 26: ("5647-12693-19", "A-12688"),
	27: ("5467-12693-19", "A-12688"), 28: ("5647-12693-19", "A-12688"),
	31: ("A-4834-H", "A-8284-2"), 32: ("A-4834-H", "A-8284-2"),
	33: (None, "A-15419"), 34: (None, "A-15419"),
	36: (None, "A-14691-4"), 37: (None, "A-14691-4"), 38: (None, "A-14691-4"),
	41: (None, "A-14691-6"), 42: (None, "A-14691-6"), 43: (None, "A-14691-6"),
	44: (None, "A-14691-5"), 45: (None, "A-14691-5"), 46: (None, "A-14691-5"),
	51: (None, "A-14691-2"), 52: (None, "A-14691-2"), 53: (None, "A-14691-2"),
	54: ("5647-12001-00", "B-12576"), 55: ("5647-12133-12", "A-10417"),
	56: ("5647-09557-00", "A-8925"), 57: ("5647-09557-00", "A-8925"), 58: ("5647-12693-08", "A-11680"),
	61: (None, "B-12030-2"), 62: (None, "B-12030-2"), 63: (None, "B-12030-2"),
	65: ("5647-12693-21", "A-15103"), 67: ("5647-12693-21", "A-15102"),
	71: ("5647-12693-19", "A-12688"), 72: ("5647-12693-19", "A-12688"), 73: ("5647-12693-19", "A-12688"),
	74: ("5647-12693-21", "A-15103"), 75: ("5647-12693-21", "A-15103"), 76: ("5447-12693-21", "A-15103"),
	77: (None, "A-9381-R"), 78: ("5647-12693-19", "A-12688"),
	86: (None, "A-14691-5"), 87: (None, "A-14691-5"), 88: (None, "A-14691-5"),
}
OPTO_SWITCH_PARTS = {n: ("A-14316 (Trans)", "A-14315 (LED)") for n in OPTO_SWITCHES}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
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
# Fliptronic F1-F8 wiring, printed 3-4 and again on the late-manual duplicate matrix page.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J905-5"),
}

# --- Printed solenoid tables (manual page 2-42 Locations; page 3-6 Solenoid Table wiring).
SOLENOID_LABELS = {
	1: "Diverter High", 2: "Up Ramp", 3: "Down Ramp", 4: "Locker (Disappearing Post)",
	5: "Left Slingshot", 6: "Right Slingshot", 7: "Knocker", 8: "Kickback",
	9: "Eject Hole", 10: "Diverter Low", 11: "Ball Release (Trough)", 12: "Plunger Kicker",
	13: "Top Jet Bumper", 14: "Left Jet Bumper", 15: "Bottom Jet Bumper", 16: "Outhole",
	17: "Right Bank Flasher", 18: "Supercharger Flasher", 19: "Left Slingshot Flasher",
	20: "Free Ride Flasher", 21: "Left Ramp Flasher", 22: "Left Bank Flasher",
	23: "Flipper Flasher", 24: "Right Slingshot Flasher",
	25: "Enable 1", 26: "Enable 2", 27: "Revolving Lamp", 28: "Enable 3",
}
# Manual solenoid-table naming inconsistency: item 27 is "Mars Lamp" on the Solenoid/Flasher
# Locations page (2-42) and "Revolving Lamp" on the Solenoid Table wiring page (3-6) -- both name
# the identical device (same part 14-7971, the A-15311 Revolving Flash Lamp Assembly motor).
SOLENOID_ALTERNATE_LABELS = {27: "Mars Lamp"}
# Manual page 3-20 Solenoid Circuits gives the printed solenoid-table numbers verbatim; every
# address here equals the public PinMAME address directly (no custSol range is declared).
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "coil",
	9: "coil", 10: "coil", 11: "coil", 12: "coil", 13: "coil", 14: "coil", 15: "coil", 16: "coil",
	17: "flasher", 18: "flasher", 19: "flasher", 20: "flasher", 21: "flasher", 22: "flasher",
	23: "flasher", 24: "flasher",
	25: "motor", 26: "motor", 27: "motor", 28: "motor",
}
# address -> {control_connection, driver_transistor, power_connection, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", part_number="A-14701", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", part_number="AE-26-1200", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", part_number="SM1-28-900-DC", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", part_number="AE-26-1200", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", part_number="AE-26-1500", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", part_number="AE-26-1500", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", part_number="AE-23-800", printed_type="High Power"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", part_number="AE-23-800", printed_type="High Power"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(control_connection="J127-3", driver_transistor="Q56", part_number="A-14701", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", part_number="A-14789", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", part_number="AE-26-1200", printed_type="Low Power"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", part_number="AE-27-1200", printed_type="Low Power"),
	17: dict(control_connection="J126-1", driver_transistor="Q42", printed_type="Flasher"),
	18: dict(control_connection="J126-2", power_connection="J125-2", driver_transistor="Q40", printed_type="Flasher"),
	19: dict(control_connection="J126-3", power_connection="J125-3", driver_transistor="Q38", printed_type="Flasher"),
	20: dict(control_connection="J126-4", driver_transistor="Q36", printed_type="Flasher"),
	21: dict(control_connection="J126-5", power_connection="J125-6", driver_transistor="Q28", printed_type="Special"),
	22: dict(control_connection="J126-6", driver_transistor="Q30", printed_type="Special"),
	23: dict(control_connection="J126-7", power_connection="J125-8", driver_transistor="Q34", printed_type="Special"),
	24: dict(control_connection="J126-8", power_connection="J125-9", driver_transistor="Q32", printed_type="Special"),
	25: dict(control_connection="J122-1", driver_transistor="Q26", part_number="A-15685", printed_type="Special"),
	26: dict(control_connection="J122-2", driver_transistor="Q24", part_number="A-15685", printed_type="Special"),
	27: dict(power_connection="J123-4", driver_transistor="Q22", part_number="14-7971", printed_type="Special"),
	28: dict(control_connection="J122-4", driver_transistor="Q20", part_number="A-15685", printed_type="Special"),
}
SOLENOID_ASSEMBLIES = {
	1: "A-15297", 2: "B-9362-L-2", 3: "B-12576", 4: "A-15127", 5: "B-11203-L-1", 6: "B-13935",
	7: "B-10686-1", 8: "B-11873", 9: "B-9362-L-2", 10: "A-15297", 11: "C-9638", 12: "A-15675",
	13: "A-9415-2", 14: "A-9415-2", 15: "A-9415-2", 16: "A-8039-3",
	17: "A-8789", 18: "C-13337", 19: "A-8789", 20: "A-12336-1", 21: "A-8789", 22: "A-8789",
	23: "A-8789", 24: "A-8789", 25: "A-15300", 26: "A-15300", 27: "B-10934-1", 28: "A-15300",
}
# Retained VPW-style script callbacks, per solenoid address (SolCallback table in script.vbs).
SOLENOID_CALLBACKS = {
	2: "SolRampUp", 3: "SolRampDown", 4: "LockPost", 7: 'vpmSolSound SoundFX("Knocker",DOFKnocker),',
	8: "SolKickback", 9: "bsEjectHole.SolOut", 10: "SuperchargerDiverter", 11: "bsTrough.SolOut",
	12: "SolPlunger (plungerIM.AutoFire)", 16: "bsTrough.SolIn",
	17: "SetLamp 117,", 18: "SetLamp 118,", 19: "SetLamp 119,", 20: "SetLamp 120,",
	21: "SetLamp 121,", 22: "SetLamp 122,", 23: "SetLamp 123,", 24: "SetLamp 124,",
	27: "Siren (no-op in this recreation)",
}
# Fliptronic flipper coil solenoids. CORE_FIRSTUFLIPSOL=33 (sURFlipPow=33/sURFlip=34,
# sULFlipPow=35/sULFlip=36); CORE_FIRSTLFLIPSOL=45 (sLRFlipPow=45/sLRFlip=46, sLLFlipPow=47/
# sLLFlip=48). gwGameData sets FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR): the lower pair and
# upper-right are fitted; upper-left (35/36) is not, matching the unfitted switch positions
# 117/118. Wiring transcribed from the Flipper Circuits page (printed 3-21).
FLIPPER_SOLENOID_LABELS = {
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
FLIPPER_SOLENOID_FITTED = {33, 34, 45, 46, 47, 48}
FLIPPER_SOLENOID_ASSEMBLY = {
	33: "A-15205-R", 34: "A-15205-R", 35: "A-15205-L", 36: "A-15205-L",
	45: "A-15205-R-2", 46: "A-15205-R-2", 47: "A-15205-L-2", 48: "A-15205-L-2",
}
FLIPPER_SOLENOID_PART = {
	33: "FL-11630", 34: "FL-11630", 35: None, 36: None,
	45: "FL-11629", 46: "FL-11629", 47: "FL-11629", 48: "FL-11629",
}
# (power connection, holding connection) from the Flipper Circuits wire table (printed 3-21);
# unfitted 35/36 have no printed connector at all.
FLIPPER_SOLENOID_WIRING = {
	33: ("Black-Yellow, J902-6", "Blue-Yellow, J907-4,5 (power feed)"),
	34: ("Orange-Violet, J902-4", None),
	45: ("Blue-Violet, J902-13", "Blue-Yellow, J907-8,9 (power feed)"),
	46: ("Orange-Green, J902-11", None),
	47: ("Blue-Gray, J902-9", "Gray-Yellow, J907-6,7 (power feed)"),
	48: ("Orange-Blue, J902-7", None),
}

# (bulb description, total quantity per manual, playfield-count) transcribed from the Solenoid
# Table's Flashlamp Type column (PL=playfield, BB=back-box).
FLASHER_BULBS = {
	17: ("#89 (1) on the playfield", 1, 1),
	18: ("#906 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	19: ("#89 (1) on the playfield and #906 (1) on the insert panel", 2, 1),
	20: ("#906 (1) on the playfield", 1, 1),
	21: ("#89 (2) and #906 (1), all on the playfield, plus #906 (1) on the insert panel", 4, 3),
	22: ("#89 (2), both on the playfield", 2, 2),
	23: ("#89 (1) and #906 (1) on the playfield, plus #906 (1) on the insert panel", 3, 2),
	24: ("#89 (1) on the playfield, plus #906 (1) on the insert panel", 2, 1),
}

# --- Printed lamp matrix (manual page 2-41 Lamp Locations; page 3-2 LAMP MATRIX wiring).
LAMP_LABELS = {
	11: "Freeway 1", 12: "Freeway 2", 13: "Freeway 3", 14: "Freeway 4", 15: "Freeway 5",
	16: "Speed", 17: "Left Freeway", 18: "Lock",
	21: "2X", 22: "4X", 23: "Hold Bonus", 24: "6X", 25: "8X", 26: "Getaway", 27: "Speed Millions", 28: "Super Jackpot",
	31: "Top Red", 32: "Top Yellow", 33: "Top Green", 34: "Right Freeway", 35: "Special",
	36: "Video Mode", 37: "Random Lamp", 38: "Extra Ball",
	41: "Tach 1", 42: "Tach 2", 43: "Tach 3", 44: "Tach 4", 45: "Tach 5",
	46: "Bottom Red", 47: "Bottom Yellow", 48: "Bottom Green",
	51: "Shoot Again", 52: "Kickback", 53: "Tach 11", 54: "Tach 12", 55: "Tach 13", 56: "Tach 14",
	57: "Tach 15", 58: "Shift",
	61: "Right Return Lane", 62: "Left Return Lane", 63: "Six Bank Bottom", 64: "Six Bank Middle",
	65: "Six Bank Top", 66: "Supercharger", 67: "Red Line Mania", 68: "Start Button",
	71: "4th Gear", 72: "5th Gear", 73: "Stop Light Red", 74: "Stop Light Yellow", 75: "Stop Light Green",
	76: "1st Gear", 77: "2nd Gear", 78: "3rd Gear",
	81: "Tach 9", 82: "Tach 10", 83: "Middle Red", 84: "Middle Yellow", 85: "Middle Green",
	86: "Tach 6", 87: "Tach 7", 88: "Tach 8",
}
LAMP_ASSEMBLIES = {
	11: ("A-15144", "#555"), 12: ("A-15144", "#555"), 13: ("A-15144", "#555"), 14: ("A-15144", "#555"),
	15: ("A-15144", "#555"), 16: ("A-15147/B-12224", "#555"), 17: ("A-15147", "#555"), 18: ("A-15147/B-12224", "#555"),
	21: ("A-11754", "#44"), 22: ("A-15144", "#555"), 23: ("A-15144", "#555"), 24: ("A-15144", "#555"),
	25: ("A-11754", "#44"), 26: ("B-12224", "#555"), 27: ("B-12224", "#555"), 28: ("A-11754", "#44"),
	31: ("C-13361", "#555"), 32: ("C-13361", "#555"), 33: ("C-13361", "#555"), 34: ("B-12224", "#555"),
	35: ("B-12224", "#555"), 36: ("A-15147", "#555"), 37: ("A-15147", "#555"), 38: ("A-15147", "#555"),
	41: ("A-11754", "#44"), 42: ("A-15143", "#555"), 43: ("A-15143", "#555"), 44: ("A-15143", "#555"),
	45: ("A-15143", "#555"), 46: ("C-13361", "#555"), 47: ("C-13361", "#555"), 48: ("C-13361", "#555"),
	51: ("A-11754", "#44"), 52: ("B-12224", "#555"), 53: ("A-15145", "#555"), 54: ("A-15145", "#555"),
	55: ("A-15145", "#555"), 56: ("A-15145", "#555"), 57: ("A-11754", "#44"), 58: ("A-11754", "#44"),
	61: ("A-15145", "#555"), 62: ("A-15143", "#555"), 63: ("A-15143/A-15145", "#555"), 64: ("A-15143/A-15145", "#555"),
	65: ("A-15143/A-15145", "#555"), 66: ("A-15456-6", "#555"), 67: ("A-15456-6", "#555"), 68: ("20-9663-3", "#44"),
	71: ("A-15146", "#555"), 72: ("A-15146", "#555"), 73: ("B-15283", "#555"), 74: ("B-15283", "#555"),
	75: ("B-15283", "#555"), 76: ("A-15146", "#555"), 77: ("A-15146", "#555"), 78: ("A-15146", "#555"),
	81: ("A-15146", "#555"), 82: ("A-15146", "#555"), 83: ("C-13361", "#555"), 84: ("C-13361", "#555"),
	85: ("C-13361", "#555"), 86: ("A-15146", "#555"), 87: ("A-15146", "#555"), 88: ("A-15146", "#555"),
}
# Printed "(2)" bulb-count addresses on the Lamp Locations page; independently confirmed by
# gw_lampPos in the pinned driver source, which splits these same six matrix addresses (and no
# others) into two drawn bulb positions.
LAMP_QUANTITIES = {16: 2, 18: 2, 35: 2, 63: 2, 64: 2, 65: 2}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
# Addresses whose retained VPX extraction carries only one of the two script-referenced Light
# objects in-bounds (the second is a co-located brightness/render double or simply absent); see
# knowledge doc. 66/67 keep only their "a"-suffixed object (l66a/l67a); 73/74/75 have no VPX Light
# object at all (Stop Light Assembly appears to be implemented as a non-Light primitive not
# resolved by this pass).
LAMPS_WITHOUT_SPATIAL = {73, 74, 75}

GI_STRINGS = {
	0: ("Illumination String 1", "J120-1", "Q18", "J120-7", "#44", "playfield"),
	1: ("Illumination String 2", "J120-2", "Q10", "J120-8", "#44", "playfield"),
	2: ("Illumination String 3", "J121-3", "Q14", "J121-9", "#555", "insert"),
	3: ("Illumination String 4", "J121-5", "Q16", "J121-10", "#555", "insert"),
	4: ("Illumination String 5", "J121-6 and J-119-3", "Q12", "J121-11 and J119-1", "#555", "insert+cabinet"),
}

# --- Normalized playfield coordinates (x/964, y/2162) from the retained vpxtool extraction;
# see review-artifacts/getaway/vpx-geometry.txt for every raw value and field path.
SWITCH_POSITIONS = {
	15: [(0.054547, 0.155697)], 16: [(0.107077, 0.075094)], 17: [(0.943159, 0.15348)], 18: [(0.887603, 0.076629)],
	25: [(0.055248, 0.789403)], 26: [(0.125893, 0.73539)], 27: [(0.780487, 0.73477)], 28: [(0.849427, 0.757932)],
	31: [(0.207383, 0.732069)], 32: [(0.697878, 0.726677)],
	36: [(0.684474, 0.156797)], 37: [(0.410603, 0.310205)], 38: [(0.341101, 0.384879)],
	41: [(0.690698, 0.181362)], 42: [(0.465298, 0.31941)], 43: [(0.359699, 0.408544)],
	44: [(0.819014, 0.61169)], 45: [(0.799966, 0.587513)], 46: [(0.780022, 0.562427)],
	51: [(0.69797, 0.205045)], 52: [(0.518007, 0.327602)], 53: [(0.377434, 0.431496)],
	54: [(0.784924, 0.050262)], 55: [(0.440943, 0.958516)],
	61: [(0.523803, 0.182334)], 62: [(0.339658, 0.225013)], 63: [(0.513489, 0.273686)],
	65: [(0.912589, 0.1893)], 67: [(0.045124, 0.308858)],
	71: [(0.238926, 0.126799)], 72: [(0.148409, 0.177198)], 73: [(0.158552, 0.234861)],
	74: [(0.909664, 0.473449)], 75: [(0.909664, 0.499351)], 76: [(0.909664, 0.524906)],
	77: [(0.789379, 0.162012)], 78: [(0.93664, 0.897516)],
	81: [(0.223615, 0.108331)], 82: [(0.419006, 0.078937)], 83: [(0.615362, 0.054731)],
	84: [(0.275242, 0.418388)], 85: [(0.819328, 0.164328)],
	86: [(0.110346, 0.594496)], 87: [(0.128896, 0.571803)], 88: [(0.147195, 0.548912)],
}
SWITCH_PROJECTIONS = {
	31: "Projected onto the Wall.LeftSlingshot collision wall's centroid: the retained script's LeftSlingShot_Slingshot handler pulses switch 31 on collision with this wall (vpmTimer.pulseSw 31), and no separate switch-31 trigger object exists.",
	32: "Projected onto the Wall.RightSlingshot collision wall's centroid; see switch 31.",
	54: "Projected onto the div_ramp Primitive (the ramp-lift flap object the retained script rotates in the same handler): SolRampUp/SolRampDown set Controller.Switch(54) directly in code (RampaMovil.Collidable / div_ramp.ObjRotY are toggled together in the same Sub), matching the manual's own finding that the physical sensor is the B-12576 Ramp Lifting Mechanism's own microswitch (part 5647-12001-00, identical to the part this manual prints for switch 54) rather than a separate playfield object.",
	55: "Projected onto the Kicker.Drain object (the retained table's drain/outhole entry kicker): the cvpmBallStack class (bsTrough.InitSw 55,58,57,56) manages switches 55-58 internally with no individually named trigger object per address; Kicker.Drain is the one physically-modeled object at the outhole/drain position.",
}
# Switches with no VPX geometry at all in this thin retained table (keyboard-virtual, hardcoded,
# or abstracted inside a ball-stack helper class with no per-address object). No spatial key is
# recorded for these addresses; see coverage.missing and the spatial report's blockers.
SWITCHES_WITHOUT_SPATIAL = {33, 34, 56, 57, 58}

SOLENOID_POSITIONS = {
	2: [(0.668544, 0.0646)], 3: [(0.668544, 0.0646)],
	4: [(0.910327, 0.541782)],
	5: [(0.207383, 0.732069)], 6: [(0.697878, 0.726677)],
	8: [(0.055546, 0.881569)], 9: [(0.789379, 0.162012)], 10: [(0.164951, 0.098571)],
	11: [(0.858425, 0.872563)], 12: [(0.93664, 0.897516)],
	13: [(0.523803, 0.182334)], 14: [(0.339658, 0.225013)], 15: [(0.513489, 0.273686)],
	16: [(0.440943, 0.958516)],
	17: [(0.954168, 0.363287)], 18: [(0.49585, 0.199558)], 19: [(0.153401, 0.804517)], 20: [(0.451094, 0.835026)],
	21: [(0.177303, 0.186311), (0.346473, 0.21107)],
	22: [(0.204748, 0.350468), (0.504149, 0.460685)],
	23: [(0.961835, 0.199201), (0.623098, 0.190513)],
	24: [(0.757835, 0.801419)],
}
SOLENOID_PROJECTIONS = {
	2: "Projected onto the RampaMovil moving-ramp object's centroid: SolRampUp/SolRampDown directly toggle RampaMovil.Collidable and rotate the div_ramp flap in the same handler; there is no separate coil-plunger object modeled.",
	3: "Projected onto the RampaMovil moving-ramp object's centroid; see solenoid 2.",
	4: "Projected onto the postlock Primitive (the retained script's LockPost sub raises/lowers PosteArriba and repositions postlock.z in the same event).",
	5: "Projected onto the Wall.LeftSlingshot collision wall's centroid, the object the retained script's LeftSlingShot_Slingshot handler animates on the same event that pulses switch 31.",
	6: "Projected onto the Wall.RightSlingshot collision wall's centroid; see solenoid 5.",
	8: "Projected onto the retained table's literal Plunger1 object (near the left outlane, raw x=53.5 next to switch 25's raw x=53.3): the retained script's SolKickback handler calls Plunger1.Fire/Plunger1.PullBack directly, confirming this VPX Plunger-type object -- not the shooter-lane plunger -- is the kickback mechanism.",
	9: "Projected onto the Kicker.sw77 object, the same physical captive-ball saucer switch 77 senses.",
	10: "Projected onto the sc_div Primitive (the visible Supercharger loop diverter flap the retained script's SuperchargerDiverter handler rotates); the companion Wall29 collision wall shares the same mechanism.",
	12: "Projected onto the Trigger.ShooterLane position: the retained script's cvpmImpulseP plunger instance (plungerIM) is initialized against the ShooterLane object at the same physical shooter-lane location as switch 78.",
}

LAMP_POSITIONS = {
	11: [(0.295605, 0.785495)], 12: [(0.374434, 0.798643)], 13: [(0.451849, 0.802916)],
	14: [(0.535242, 0.797763)], 15: [(0.61327, 0.783782)],
	16: [(0.864454, 0.301771), (0.129975, 0.364001)],
	17: [(0.159194, 0.415226)],
	18: [(0.693151, 0.478712), (0.190207, 0.466126)],
	21: [(0.304875, 0.733535)], 22: [(0.373577, 0.749605)], 23: [(0.451395, 0.754736)],
	24: [(0.53171, 0.749946)], 25: [(0.600166, 0.733253)],
	26: [(0.524988, 0.406874)], 27: [(0.610417, 0.443446)], 28: [(0.778103, 0.514581)],
	31: [(0.635351, 0.169188)], 32: [(0.642127, 0.193944)], 33: [(0.648753, 0.218003)],
	34: [(0.831066, 0.352367)], 35: [(0.848736, 0.708738), (0.054443, 0.708311)],
	36: [(0.746624, 0.283742)], 37: [(0.711249, 0.335884)], 38: [(0.678062, 0.386331)],
	41: [(0.247624, 0.708965)], 42: [(0.213119, 0.677723)], 43: [(0.20176, 0.643829)],
	44: [(0.210597, 0.610004)], 45: [(0.246084, 0.578866)],
	46: [(0.392915, 0.385084)], 47: [(0.411518, 0.408472)], 48: [(0.427851, 0.43248)],
	51: [(0.452756, 0.88393)], 52: [(0.054508, 0.763842)],
	53: [(0.654999, 0.578859)], 54: [(0.691459, 0.609319)], 55: [(0.701443, 0.644792)], 56: [(0.690295, 0.677774)],
	57: [(0.653754, 0.708844)], 58: [(0.450422, 0.614439)],
	61: [(0.779231, 0.676555)], 62: [(0.124856, 0.676143)],
	63: [(0.756857, 0.643224), (0.168063, 0.627848)],
	64: [(0.741426, 0.622448), (0.185179, 0.60659)],
	65: [(0.728575, 0.59986), (0.197696, 0.583832)],
	66: [(0.251575, 0.438209)], 67: [(0.312586, 0.43396)],
	71: [(0.547348, 0.510309)], 72: [(0.636629, 0.529938)],
	76: [(0.263626, 0.531178)], 77: [(0.35043, 0.511399)], 78: [(0.450394, 0.504948)],
	81: [(0.529939, 0.538977)], 82: [(0.598618, 0.554764)],
	83: [(0.391876, 0.338578)], 84: [(0.444265, 0.345794)], 85: [(0.496127, 0.355325)],
	86: [(0.305818, 0.554813)], 87: [(0.376362, 0.538717)], 88: [(0.451006, 0.532657)],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"The Getaway retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Getaway extraction")
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
		raise RuntimeError(f"The Getaway retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"The Getaway retained extraction manifest does not match all files under {extraction_root}")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"The Getaway retained extraction identity mismatch: files={len(actual['files'])}")
	return actual


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
			"locator": "Pinned catalog driver records for the gw_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/gw.c gwGameData GEN_WPCFLIPTRON with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1f,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_UR)|"
				"FLIP_SOL(FLIP_L|FLIP_UR), swStart/swTilt/swSlamTilt/swCoinDoor/swGearLo comSw defines, no swCol/"
				"lampCol/custSol declared, gw_handleMech (sets/clears swRampDown from sRampUp/sRampDown), and the "
				"gw_lampPos table splitting matrix addresses 16/18/35/63/64/65 into two drawn bulb positions each. "
				"The driver's own header comment states the author had no access to the physical machine and guessed "
				"most switch/solenoid semantic labels from a playfield photo and the rulesheet -- its numeric public "
				"addresses (WPC column*10+row convention) are still real hardware, but its #define comment labels "
				"are not treated as authoritative device identity ground truth by themselves. src/wpc/core.h "
				"CORE_FIRSTUFLIPSOL=33/CORE_FIRSTLFLIPSOL=45; src/wpc/wpc.c WPC_FLIPPERS unconditional complement for "
				"non-WPC95 generations; src/wpc/wpc.c lines ~507-527 core_gameon fallback (wpc_fastflip_addr==0 mirrors "
				"WPC_GILAMPS bits 5-7 across public solenoids 29-31 when a driver never calls wpc_set_fastflip_addr, "
				"which gw.c never does); src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCFLIPTRON=0x8"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-fliptronic.json",
			"revision": "repository",
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules, including the no-LPDC 37-44 unused range and Fliptronic F1-F8 switch ordering",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.the-getaway-high-speed-ii.1992/archive-arcademanual_Getaway_HSII_OPS/Getaway_HSII_OPS.pdf",
			"original_filename": "Getaway_HSII_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"131-page Williams The Getaway: High Speed II operations manual scan (Internet Archive item "
				"arcademanual_Getaway_HSII_OPS) with an Adobe Acrobat Pro Paper Capture OCR text layer that is present "
				"but garbled for the multi-column wiring tables and never trusted alone. Printed pages 2-40 through "
				"2-44 carry the switch/lamp/solenoid/ramp location parts lists; printed pages 3-2, 3-4, 3-6, 3-12, "
				"3-14, 3-20, 3-21, and 3-22 carry the lamp/switch/solenoid matrix wiring and the two opto driver board "
				"assembly pages; printed pages 2-24, 2-25, 2-28, 2-29, 2-30, 2-33, 2-38, and 2-39 carry the mechanism "
				"and playfield-parts assemblies."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.getaway.switch-locations",
					"locator": "PDF page 101, printed 2-40, Switch Locations parts list",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/switch-locations.md",
					"sha256": "695e37c7e904a278880d07fd6cf4c0292d824a54e9e7c7fcd0ca10c6d2a02683",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.switch-matrix",
					"locator": "PDF page 109, printed 3-4, SWITCH MATRIX table",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/switch-matrix.md",
					"sha256": "7141f023a5e2a57490bff3b862c48573cd07bf115adda8b222aaed737cd6e933",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.lamp-locations",
					"locator": "PDF page 102, printed 2-41, Lamp Locations parts list",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/lamp-locations.md",
					"sha256": "156f3011a2599a0b35c8cd8401d7f5477596ee48f2ab2eb80c0aefcae3d97ba2",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.lamp-matrix",
					"locator": "PDF page 107, printed 3-2, LAMP MATRIX wiring table",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/lamp-matrix.md",
					"sha256": "8ce2e6e20e060bc72c759f60a56fc3602998f0eaa50731e384d30a7a3c42df10",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.solenoid-flasher-locations",
					"locator": "PDF page 103, printed 2-42, Solenoid/Flasher Locations parts list",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/solenoid-flasher-locations.md",
					"sha256": "72138a5d7486743284374c050fc33c65d0ff9e0142a3db21796a12b4e2926d26",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.solenoid-table",
					"locator": "PDF page 111, printed 3-6, Solenoid Table wiring page",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/solenoid-table.md",
					"sha256": "2c7fac053b24e3dbbb014e6ce6c4ef8b2e0eeddaedd89ef00ab40958faa38c7e",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.general-illumination",
					"locator": "PDF page 127, printed 3-22, General Illumination Circuits wiring page",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/general-illumination.md",
					"sha256": "87762a83994057ee72247b162fc7546db6eb9104b4fd41ca38fe495f0a77ca0c",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.accelerator-and-opto-ramp-boards",
					"locator": "PDF pages 117 and 119, printed 3-12 and 3-14, opto driver board assembly pages",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/accelerator-and-opto-ramp-boards.md",
					"sha256": "158b88ba0d1aa368b6ecc6d2680b8cdecbe3c8905463de506d686694f74090d6",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.getaway.ramp-locations",
					"locator": "PDF page 105, printed 2-44, Ramp Locations parts list",
					"path": "evidence/excerpts/williams.the-getaway-high-speed-ii.1992/ramp-locations.md",
					"sha256": "f850e859f4f7e2e3e904b00bfa6013bd1cdbaa0b6ae40a68d9f3f284abd4ea73",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/getaway/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription cache indexing every rendered manual table used by this definition, "
				"the mechanism/assembly page transcriptions (external:pinmame-review-artifacts/getaway/"
				"mechanism-pages.md), and the raw VPX geometry dump (external:pinmame-review-artifacts/getaway/"
				"vpx-geometry.txt), together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/williams.the-getaway-high-speed-ii.1992/. The retained PDF's OCR "
				"text layer is present but garbled for the wiring tables, so this transcription is the source of "
				"record for every table cited by this definition."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-getaway-high-speed-ii-1992/source/Getaway%2C%20The%20-%20High%20Speed%20II%20v1.2.vpx",
			"original_filename": "Getaway, The - High Speed II v1.2.vpx",
			"sha256": TABLE_SHA256,
			"known_working": True,
			"locator": (
				f"Retained known-working recreation, VPX version 10.4, credited flupper1/32assassin/ganjafarmer/"
				f"nFozzy/bassgeige. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and "
				"y/2162. This is a comparatively thin table (875 extracted files, 39,497-byte script) and does not "
				"model every physical device with a distinct table object; several addresses have no VPX geometry at "
				"all (see coverage.missing and the spatial report)."
			),
			"license": "NOASSERTION",
			"attribution": "flupper1, 32assassin, ganjafarmer, nFozzy, bassgeige",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/the-getaway-high-speed-ii-1992/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (39,497 bytes). Runtime and mechanism-causality authority: cGameName = '
				'"gw_l5", Const UseSolenoids=1, the SolCallback table for solenoids 2-4, 7-12, 16-24, 27, and the '
				"Fliptronic flipper addresses, the SW15/16/17/18/25-28/65/67/71-73/81-85 Controller.Switch wire-"
				"trigger handlers, the cvpmBallStack/cvpmVLock/cvpmImpulseP mechanism-class initializations for the "
				"trough, ball lock, and shooter lane, and GiCallback2's UpdateGI routine (which ignores its own `no` "
				"GI-address parameter and drives one shared 25-member GI collection for every GI address)."
			),
			"license": "NOASSERTION",
			"attribution": "flupper1, 32assassin, ganjafarmer, nFozzy, bassgeige",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/the-getaway-high-speed-ii-1992/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; {EXTRACTION_FILE_COUNT} files, produced with vpxtool from the retained table. "
				f"Bounds are {TABLE_BOUNDS}. Raw per-object coordinates and field paths for every switch, lamp, "
				"solenoid-driven toy, GI collection member, and mechanism reference object are retained verbatim in "
				"external:pinmame-review-artifacts/getaway/vpx-geometry.txt."
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
		"board": "Fliptronic II CPU board",
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
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address,
				"optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "Fliptronic II CPU board", "drive_wire": wire, "drive_connection": connection},
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
			if unused:
				parts = (None, None)
			elif address in OPTO_SWITCHES:
				parts = OPTO_SWITCH_PARTS[address]
			else:
				parts = SWITCH_PARTS.get(address, (None, None))
			switch_part, assembly_part = parts
			physical: dict[str, Any] = {}
			if assembly_part:
				physical["assembly_part_number"] = assembly_part
			if switch_part and address not in OPTO_SWITCHES:
				physical["part_number"] = switch_part
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The Switch Locations parts list and the SWITCH MATRIX wiring page both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					" The Switch Locations page prints a paired opto LED/phototransistor part (A-14316 Trans / "
					"A-14315 LED) for this address, independently confirmed by the dedicated opto driver board pages "
					"(A-15189 Accelerator Board Assembly for 81-83; A-13901-1 Opto Ramp Switch Board Assembly for "
					"84-85), each naming this address's own LED/Transistor connector pins. PinMAME's gwGameData "
					"inverted-switch mask (column 8 bits 0-4, i.e. exactly 81-85) normalizes it, so the public "
					"switch state is already normalized and must not be inverted again."
				)
			elif address == 23:
				notes += (
					' The SWITCH MATRIX page\'s grid cell names this address "Ticket Opto.", but the Switch '
					'Locations page prints no switch or assembly part number at all for it -- only "(optional)" -- '
					"and PinMAME's inverted-switch mask does not normalize it. The ticket dispenser is optional "
					"cabinet-adjacent equipment on this machine; its construction is recorded as unconfirmed rather "
					"than asserted opto."
				)
			if address == 24:
				notes += " Permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed; the retained script hardcodes Controller.Switch(22)=True at table init."
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
			}
			if not unused:
				extra["wiring"] = _switch_wiring(address)
			if unused:
				availability = "used" if False else "unused"
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
				availability = "optional" if address == 23 else "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet"
					if address == 22:
						extra["initial_active"] = True
					if address == 14:
						physical["notes"] += " The retained script drives this purely via vpmNudge.TiltSwitch=14, not a table trigger object."
				elif address == 23:
					extra["roles"] = ["cabinet.coin-door"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "coin door area (optional ticket dispenser)"
				elif address in SWITCHES_WITHOUT_SPATIAL:
					if address in {33, 34}:
						physical["notes"] += (
							" No VPX object models the physical Up-Down Shifter mechanism (20-9710) in this "
							"recreation; the retained script drives this address purely from an unrelated keyboard "
							"key (LeftMagnaSave for 33, PlungerKey for 34)."
						)
					else:
						physical["notes"] += (
							" The retained script's cvpmBallStack class manages this trough position internally "
							"with no individually named table object for this specific address."
						)
					# No spatial key: no VPX geometry exists for this address in the retained thin table.
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label or f"Not Used Matrix Position {address}", kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True),
		115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "used", False),
		116: ("Upper Right Flipper Button", "flipper.upper.right.button", "used", True),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None),
	}
	for address, (label, role, availability, normally_closed) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" The Getaway has no upper-left flipper. Three independent sources confirm it: the Switch "
				"Locations parts list has no A-15205-L (upper-left leaf switch) row at all; the Left Flipper "
				"Circuit diagram (printed 3-10) labels this position \"UPPER LEFT (NOT USED)\"; and the Flipper "
				"Circuits wire table (printed 3-21) prints the Upper Left Flipper Button Switch wire as "
				'"Black/Blue(NU)". gwGameData independently agrees: FLIP_SW(FLIP_L|FLIP_UR) sets no FLIP_UL bit. '
				"A later duplicate Switch Matrix page near the end of the manual lists F7/F8 without any Not Used "
				"annotation of its own -- the same generic Fliptronic silkscreen template every WPC-Fliptronic "
				"game's manual reuses regardless of that game's actual flipper count -- but the three game-specific "
				"sources above settle fitment decisively."
			)
			physical["location"] = "not installed"
		else:
			notes += " Fitted; gwGameData sets FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR)."
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "Fliptronic II CPU board", "drive_wire": wire, "drive_connection": connection},
		}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			extra["normally_closed"] = bool(normally_closed) if normally_closed is not None else False
			extra["spatial"] = not_applicable("cabinet_or_service" if role.endswith(".button") else "internal_nonvisual", MANUAL_SOURCE)
		items.append(
			_device(
				f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE), **extra,
			)
		)

	dip_labels = {n: f"CPU DIP {n} (country/option configuration bit)" for n in range(1, 9)}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", dip_labels[address], "dip_switch", "pinmame.input.dip", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={
					"location": "Fliptronic II CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-Fliptronic CPU-board country/option configuration DIP bank. The retained transcription "
						"of this manual does not include the per-country switch-combination chart, so no specific "
						"ON/OFF combination is asserted here."
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
	for address in range(1, 29):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		wiring_data = SOLENOID_WIRING[address]
		kind = SOLENOID_KIND[address]
		physical: dict[str, Any] = {}
		part_number = wiring_data.get("part_number")
		if part_number:
			physical["part_number"] = part_number
		if address in SOLENOID_ASSEMBLIES:
			physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
		printed_type = wiring_data.get("printed_type", "")
		notes = f"Printed solenoid-table entry {address:02d} ({printed_type})."
		if address in SOLENOID_ALTERNATE_LABELS:
			notes += (
				f' Printed "{SOLENOID_ALTERNATE_LABELS[address]}" on the Solenoid/Flasher Locations page (2-42) and '
				f'"{label}" on the Solenoid Table wiring page (3-6); same part {part_number}, same physical device -- '
				"an internal manual naming inconsistency, not two devices."
			)
		if kind == "flasher":
			bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
			physical["quantity"] = quantity
			notes += f" Printed flashlamp complement: {bulbs}."
			if address not in SOLENOID_POSITIONS or len(SOLENOID_POSITIONS.get(address, [])) < playfield_emitters:
				placed = len(SOLENOID_POSITIONS.get(address, []))
				notes += (
					f" The retained table's script (SetLamp {100 + address}, dispatched from UpdateLamps) drives "
					f"{placed} confidently-attributable playfield object(s) at the position(s) recorded below; the "
					f"remaining printed playfield/insert-panel bulb(s) have no VPX object this pass could confirm "
					"belongs to this address."
				)
		if address == 5:
			notes += (
				' gw.c\'s own #define labels this address sRSling ("Right Slingshot"), but the Solenoid/Flasher '
				"Locations page and the Solenoid Table wiring page both independently print item 5 as \"Left "
				'Slingshot" (assembly B-11203-L-1, the left-hand kicker-arm assembly per the Lower Playfield Parts '
				"list). The driver's own header comment admits its author guessed most labels without access to the "
				"physical machine; the two agreeing manual pages are treated as the correction."
			)
		if address == 6:
			notes += (
				' gw.c\'s own #define labels this address sLSling ("Left Slingshot"), but the Solenoid/Flasher '
				"Locations and Solenoid Table pages both independently print item 6 as \"Right Slingshot\" "
				"(assembly B-13935); see solenoid 5's note for the same correction."
			)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		if address == 1:
			notes += (
				" The retained script's SolCallback table has no entry for solenoid 1 at all -- this recreation does "
				"not visually implement the Diverter High coil, unlike Diverter Low (solenoid 10), which the script "
				"drives via the SuperchargerDiverter sub."
			)
		if address in {25, 26, 28}:
			notes += (
				" Wired to the A-15189 Accelerator Board Assembly (same board carrying the switch 81-83 opto "
				"circuits) and routed \"To Playfield\" on the Solenoid Circuits interboard wiring page (printed "
				"3-20), engaging the motorized accelerator wheels; the retained script has no SolCallback entry for "
				"this address and models the Supercharger loop's ball acceleration purely through the SW81/82/83 "
				"Hit handlers instead, so no VPX object could be confirmed as this relay's own position."
			)
		if address == 27:
			notes += (
				" The Solenoid Circuits interboard wiring page (printed 3-20) is the only row on that page with a "
				"blank \"To Playfield\" entry -- only a backbox connector (J123-4) -- and the A-15311 Revolving "
				"Flash Lamp Assembly is a self-contained motorized reflector/beacon unit; this is backbox hardware, "
				"not a playfield device."
			)
		if address == 7:
			notes += " Knocker coil, mounted in the cabinet behind the coin door (B-10686-1 Knocker Assembly); standard cabinet-mounted hardware, not a playfield device."
		physical["notes"] = notes

		wiring: dict[str, Any] = {"board": "Fliptronic II power driver board", "driver_transistor": wiring_data["driver_transistor"]}
		if "control_connection" in wiring_data:
			wiring["control_connection"] = wiring_data["control_connection"]
		if "power_connection" in wiring_data:
			wiring["power_connection"] = wiring_data["power_connection"]
		aliases = [
			{"namespace": "pinmame.solenoid", "value": str(address)},
			{"namespace": "manual.address", "value": f"{address:02d}"},
		]
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if address == 27:
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 7:
			extra["roles"] = ["cabinet.interior"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in {1, 25, 26, 28}:
			pass  # No spatial key: no VPX geometry could be confirmed for this address.
		else:
			role = "emitter" if kind == "flasher" else "effect"
			positions = SOLENOID_POSITIONS[address]
			coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
			extra["spatial"] = located(identifier, role, positions, *coordinate_refs)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS or address in {5, 6}:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))

	for address, label in FLIPPER_SOLENOID_LABELS.items():
		identifier = output_id(label)
		fitted = address in FLIPPER_SOLENOID_FITTED
		physical: dict[str, Any] = {}
		part = FLIPPER_SOLENOID_PART[address]
		if part:
			physical["part_number"] = part
		physical["assembly_part_number"] = FLIPPER_SOLENOID_ASSEMBLY[address]
		notes = f"Fliptronic flipper {'power' if address % 2 == 1 else 'hold'} winding, public address {address}."
		if fitted:
			notes += " Printed on the Flipper Circuits wire table (3-21) and the Solenoid/Flasher Locations Flippers block (2-42)."
		else:
			notes += (
				" The Getaway has no upper-left flipper; see switch.generic-117/118 for the three independent "
				"manual confirmations. This circuit position has no coil, and the Flipper Circuits wire table "
				"prints no connector for it."
			)
		physical["notes"] = notes
		extra = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
			"physical": physical,
		}
		if fitted:
			control, power = FLIPPER_SOLENOID_WIRING[address]
			wiring = {"board": "Fliptronic II controller board", "control_connection": control}
			if power:
				wiring["power_connection"] = power
			extra["wiring"] = wiring
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		else:
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		items.append(
			_device(
				identifier, label, "coil", "pinmame.output.solenoid", address, "used" if fitted else "unused",
				(MANUAL_SOURCE, CORE_SOURCE), **extra,
			)
		)

	virtual_labels = {
		29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
		31: "PinMAME Fast-Flip Game-On State (undeclared for this driver)",
		32: "Unused WPC State Channel 32",
		37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38",
		39: "Unused WPC-Fliptronic Output 39", 40: "Unused WPC-Fliptronic Output 40",
		41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
		43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
		49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
	}
	for address, label in virtual_labels.items():
		identifier = output_id(label)
		notes = {
			29: (
				"PinMAME mirrors bit 5 of the WPC_GILAMPS register here when no fast-flip address is declared "
				"(src/wpc/wpc.c core_gameon fallback), which is the case for gw.c; it is not a Getaway playfield "
				"device."
			),
			30: "PinMAME mirrors bit 6 of the WPC_GILAMPS register here under the same fallback as 29.",
			31: (
				"Under a normally-configured WPC-Fliptronic driver this channel is PinMAME's synthetic fast-flip "
				"game-on state, taken from the driver's own fast-flip RAM flag once wpc_set_fastflip_addr is called. "
				"gw.c never calls wpc_set_fastflip_addr, so per src/wpc/wpc.c's core_gameon fallback (lines ~514-518) "
				"PinMAME instead mirrors bit 7 of the WPC_GILAMPS register here -- a GI-lamp-related state bit, not a "
				"flipper-enable signal. The retained known-working script nonetheless binds "
				'SolCallback(31) = "FastFlips.TiltSol", the standard nFozzy cFastFlips convention that treats this '
				"address as the flipper-enable gate. See conflict.solenoid-31-fastflip-address-not-declared."
			),
			32: "PinMAME reports this WPC state channel as always zero.",
			37: "Unused WPC-Fliptronic address space; this generation has no integrated LPDC board (GENWPC_HASWPC95 is not set), so 37-44 are simply unused rather than a duplicated general-purpose range.",
			38: "Unused WPC-Fliptronic address space; see 37.",
			39: "Unused WPC-Fliptronic address space; see 37.",
			40: "Unused WPC-Fliptronic address space; see 37.",
			41: "Unused WPC-Fliptronic address space; see 37.",
			42: "Unused WPC-Fliptronic address space; see 37.",
			43: "Unused WPC-Fliptronic address space; see 37.",
			44: "Unused WPC-Fliptronic address space; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-Fliptronic hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. gwGameData declares no custSol.",
		}[address]
		roles = ["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"]
		items.append(
			_device(
				identifier, label, "virtual", "pinmame.output.solenoid", address,
				"used" if address in {29, 30, 31} else "unused",
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}. Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += (
					f" The Lamp Locations page marks this insert with a bulb quantity of {LAMP_QUANTITIES[address]}, "
					f"independently confirmed by gw_lampPos in the pinned driver source, which splits this exact "
					"address into two drawn bulb positions; the retained table binds both bulbs."
				)
			if address in {66, 67}:
				notes += (
					" The retained table's UpdateLamps sub only references the \"a\"-suffixed Light object for this "
					"address (l66a / l67a); no non-suffixed object exists for it in this recreation."
				)
			if address in LAMPS_WITHOUT_SPATIAL:
				notes += (
					" This address is part of the A-15283 Stop Light Assembly (a 3-lamp PC board behind red/orange/"
					"green starburst inserts). No Light object named for this address exists in the retained "
					"extraction; the mechanism appears to be implemented, if at all, through an object this pass "
					"could not confidently attribute to a specific address, so no coordinate is recorded."
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
					"board": "Fliptronic II power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address == 68:
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in LAMPS_WITHOUT_SPATIAL:
				pass  # No spatial key: no VPX object could be confirmed for this address.
			else:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, return_connection, bulb, placement) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "Fliptronic II power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"return_connection": return_connection,
			},
		}
		physical: dict[str, Any] = {}
		if placement == "playfield":
			notes += (
				" Routed exclusively to the playfield (General Illumination Circuits page, printed 3-22). The "
				"retained script's UpdateGI sub ignores its own GI-address parameter and drives one shared 25-member "
				"\"GI\" object collection for every GI address uniformly, so this recreation cannot distinguish "
				"which specific playfield bulb(s) belong to this string versus the other playfield string (GI "
				"address 0 or 1); no per-address coordinate is recorded for either."
			)
			extra["roles"] = ["playfield.gi"]
		else:
			notes += " Backbox insert-panel illumination behind the translite; the retained script's monolithic UpdateGI has no distinguishable geometry for it either way."
			if address == 4:
				notes += " This string additionally feeds a cabinet connector (J-119-3), the only cabinet connection on the printed general-illumination wiring page."
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))
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
		identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str,
		positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None,
	) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
			"behavior": behavior, "provenance": provenance(*refs),
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
			"mechanism.supercharger-loop", "Motorized Supercharger accelerator loop", "motorized",
			[output_id("Enable 1"), output_id("Enable 2"), output_id("Enable 3")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-83"],
			"Three motorized wheels (A-15300 Accelerator Tray Assembly, driven from the A-15189 Accelerator Board "
			"Assembly) sit in sequence along the Accelerator Ramp Assembly (A-15297/A-15301) at the upper-left of "
			"the playfield, forcibly accelerating a ball around a fixed loop track. Each wheel has its own opto "
			"position sensor (switches 81, 82, 83, Opto 1/2/3) wired through the same board that also carries the "
			"three wheel-drive Enable relays (solenoids 25, 26, 28). The retained known-working script's SW81_Hit/"
			"SW82_Hit/SW83_Hit handlers each add ball velocity in sequence (velX += 11, +15, +19) as the ball "
			"passes each wheel, modeling the physical acceleration purely through scripted velocity boosts rather "
			"than true wheel-drive physics. No VPX object could be confidently attributed to the Enable relays' own "
			"positions; the loop's physical location is anchored by the three opto switch positions instead.",
			[
				("wheel-1", "Accelerator wheel 1", ["switch.matrix-81"], "First wheel opto position."),
				("wheel-2", "Accelerator wheel 2", ["switch.matrix-82"], "Second wheel opto position."),
				("wheel-3", "Accelerator wheel 3", ["switch.matrix-83"], "Third wheel opto position."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15300",
		),
		mechanism(
			"mechanism.supercharger-diverter", "Supercharger loop entrance/return diverter", "gate",
			[output_id("Diverter High"), output_id("Diverter Low")],
			["switch.matrix-84", "switch.matrix-85"],
			"A diverter flap (retained table objects Wall29/sc_div) at the base of the Accelerator Return Assembly "
			"(A-15293) either sends a ball around the Supercharger loop again or lets it continue toward the left "
			"ramp; solenoid 10 (Diverter Low) drives the retained script's SuperchargerDiverter handler, which "
			"rotates sc_div and toggles Wall29's collidability. Solenoid 1 (Diverter High) has no SolCallback entry "
			"in the retained script at all and is not visually implemented by this recreation. Switches 84 and 85 "
			"sit on the dedicated A-13901-1 Opto Ramp Switch Board (one each) at this same mechanism, but which "
			"physical position (ramp entrance versus loop-completion point) corresponds to which address is a "
			"genuine, unresolved disagreement between the manual's own Switch Locations labels and the retained "
			"script's runtime behavior; see conflict.switch-84-85-manual-vs-script-semantics. This recreation's "
			"SW81_Hit-style velocity boost does not extend to switch 84 or 85; 85 only plays a distinct \"sc_loop2\" "
			"sound and 84 only plays a generic \"rollover\" sound.",
			[],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15293",
		),
		mechanism(
			"mechanism.ramp-lift", "Motorized right ramp lift", "motorized",
			[output_id("Up Ramp"), output_id("Down Ramp")],
			["switch.matrix-54"],
			"The B-12576 Ramp Lifting Mechanism Assembly raises and lowers the right ramp surface (RampaMovil) "
			"between a lowered position (ball routes onto the Supercharger loop's return path) and a raised "
			"position (ball routes along the right ramp instead), driven by solenoids 2 (Up Ramp) and 3 (Down "
			"Ramp). The mechanism's own microswitch (part 5647-12001-00, identical to the part the Switch Locations "
			"page prints for switch 54) senses the lowered position; the retained script's SolRampUp/SolRampDown "
			"handlers set Controller.Switch(54) directly in the same code that toggles RampaMovil.Collidable and "
			"rotates the div_ramp flap object, with no separate trigger object for switch 54 in this recreation. "
			"gw_handleMech in the pinned driver source independently confirms the same causal pairing "
			"(core_setSw(swRampDown,...) keyed off core_getSol(sRampUp)/core_getSol(sRampDown)).",
			[("down", "Ramp lowered", ["switch.matrix-54"], "Ball routes onto the Supercharger loop's return path.")],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="B-12576",
		),
		mechanism(
			"mechanism.ball-lock", "Three-ball visible lock", "kicker",
			[output_id("Locker (Disappearing Post)")],
			["switch.matrix-74", "switch.matrix-75", "switch.matrix-76"],
			"Three balls can be held on the Wire Right Ramp (A-15103) at Top/Middle/Bottom Lock (switches 74/75/"
			"76). The retained script's cvpmVLock class (visibleLock.InitVLock Array(sw76,sw75,sw74), "
			"Array(k76,k75,k74), Array(76,75,74)) manages the visible three-ball lock; solenoid 4 (Locker/"
			"Disappearing Post, A-15127 Disappear Post Assembly) raises/lowers a post (PosteArriba/postlock) that "
			"releases the locked balls when fired, per the retained LockPost sub.",
			[
				("top", "Top lock", ["switch.matrix-74"], "Ball held nearest the ramp entrance."),
				("middle", "Middle lock", ["switch.matrix-75"], "Second locked ball."),
				("bottom", "Bottom lock", ["switch.matrix-76"], "Third locked ball, nearest the disappearing post."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15127",
		),
		mechanism(
			"mechanism.kickback", "Left outlane kickback", "kicker",
			[output_id("Kickback")],
			["switch.matrix-25"],
			"The B-11873 Kickback Assembly fires a ball resting in the left outlane back onto the playfield. The "
			"retained script's SolKickback handler fires a literal VPX Plunger-type object (Plunger1, positioned "
			"immediately below switch 25/Left Outlane in the retained geometry) rather than the shooter-lane "
			"plunger, which is a separate cvpmImpulseP instance bound to solenoid 12.",
			[("held", "Ball in the left outlane", ["switch.matrix-25"], "Left outlane switch, upstream of the kickback plunger.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="B-11873",
		),
		mechanism(
			"mechanism.trough", "Three-ball trough and ball release", "kicker",
			[output_id("Ball Release (Trough)"), output_id("Outhole")],
			["switch.matrix-55", "switch.matrix-56", "switch.matrix-57", "switch.matrix-58"],
			"The retained script's cvpmBallStack class (bsTrough.InitSw 55,58,57,56) manages the outhole/trough "
			"ball stack as an abstract queue rather than four individually named table objects. The two physically "
			"modeled endpoints are Kicker.Drain (the drain/outhole entry point, solenoid 16 per bsTrough.InitKick "
			"BallRelease,85,7 -- note the class also references public switch 85 and solenoid 7 as additional "
			"trough-adjacent parameters) and Kicker.BallRelease (the ball-release exit point, solenoid 11). "
			"Switches 56/57/58 (Left/Center/Right Trough) have no individual sensor geometry in this recreation.",
			[("outhole", "Ball at the outhole", ["switch.matrix-55"], "Drain entry, modeled by Kicker.Drain.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="C-9638",
		),
		mechanism(
			"mechanism.shooter-lane", "Shooter lane and auto plunger", "kicker",
			[output_id("Plunger Kicker")],
			["switch.matrix-78"],
			"The retained script's cvpmImpulseP instance (plungerIM.InitImpulseP ShooterLane, 46, 0.1) models the "
			"manual plunger/shooter lane, bound to switch 78 (Shooter, Trigger.ShooterLane) and solenoid 12 "
			"(Plunger Kicker, A-15675 Kicker Assembly).",
			[("shooter", "Ball in shooter lane", ["switch.matrix-78"], "Shooter-lane switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-15675",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-31", "switch.matrix-32"],
			"Each slingshot assembly (A-14875-2 right / A-14875-1 left kicker arms, with B-13935 / B-11203-L-1 "
			"coil-and-bracket assemblies and A-8284-2 kicker switch assemblies) carries its own switch. The "
			"retained script's LeftSlingShot_Slingshot/RightSlingShot_Slingshot handlers pulse matrix addresses 31 "
			"and 32 directly from a collision with the Wall.LeftSlingshot/Wall.RightSlingshot objects; solenoids 5 "
			"and 6 fire the physical kickers (the pinned driver's own #define comments reverse these two solenoid "
			"labels against the manual; see the device notes on solenoid 5/6).",
			[
				("left", "Left slingshot", ["switch.matrix-31"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-32"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14875-2",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three-bumper jet nest", "other",
			[output_id("Top Jet Bumper"), output_id("Left Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-61", "switch.matrix-62", "switch.matrix-63"],
			"Three A-9415-2 jet bumpers with B-12030-2 switch-and-diode skirt assemblies. The retained script's "
			"Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit handlers pulse switches 61, 62, and 63 (matching printed "
			"Top/Left/Bottom Jet Bumper), and solenoids 13/14/15 fire the corresponding coils.",
			[
				("top", "Top jet bumper", ["switch.matrix-61"], "Uppermost bumper of the nest."),
				("left", "Left jet bumper", ["switch.matrix-62"], "Left bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-63"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.eject-hole", "Captive-ball eject hole", "kicker",
			[output_id("Eject Hole")],
			["switch.matrix-77"],
			"A ball resting in the eject-hole saucer (A-9381-R, switch 77) is kicked back to the playfield by "
			"solenoid 9; the retained script's cvpmBallStack instance (bsEjectHole.InitSaucer sw77,77,100,10) "
			"manages the saucer and Kicker.sw77 is the single physical object serving both the switch and solenoid.",
			[("held", "Ball in the eject hole", ["switch.matrix-77"], "Eject-hole saucer switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-9381-R",
		),
		mechanism(
			"mechanism.gear-shifter", "Up-Down Shifter gear lever", "other",
			[],
			["switch.matrix-33", "switch.matrix-34"],
			"The 20-9710 Up-Down Shifter is a cabinet-mounted gear-shift lever (Gear Shift Assembly, A-15419) with "
			"an internal microswitch mechanism and its own bayonet-base bulb; its own manual page (printed 2-33) "
			"carries no item-number balloons or parts table at all, only a \"Cabinet shown for reference\" "
			"illustration caption. No object anywhere in the retained VPX extraction has \"gear\" or \"shift\" in "
			"its name -- this recreation does not model the lever's physical geometry at all, and instead drives "
			"switches 33 (Gear Shifter Low) and 34 (Gear Shifter High) purely from two unrelated keyboard keys "
			"(LeftMagnaSave and PlungerKey respectively) in Table1_KeyDown/KeyUp. No spatial placement is recorded "
			"for either switch as a result.",
			[
				("low", "Gear shifted low", ["switch.matrix-33"], "Low-gear detent."),
				("high", "Gear shifted high", ["switch.matrix-34"], "High-gear detent."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15419",
		),
		mechanism(
			"mechanism.lower-flippers", "Lower flipper pair", "other",
			[],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Two FL-11629 flippers on Fliptronic circuits. Each flipper has a separate power and hold winding: the "
			"ROM energizes the power winding on the cabinet button opto (112 right, 114 left), then drops to the "
			"hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes.",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 right with A-15205-L-2 left",
		),
		mechanism(
			"mechanism.upper-right-flipper", "Upper right flipper", "other",
			[],
			["switch.generic-115", "switch.generic-116"],
			"One FL-11630 flipper on the upper-right Fliptronic circuit, feeding the Supercharger loop's entrance "
			"path. There is no upper-left counterpart; see the switch.generic-117/118 device notes for the three "
			"independent manual confirmations that position is unfitted.",
			[("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button 116 and end-of-stroke switch 115.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ramp-down-switch",
			"kind": "direct",
			"source": output_id("Down Ramp"),
			"destination": "switch.matrix-54",
			"provenance": provenance(VPX_SCRIPT_SOURCE, CORE_SOURCE),
		},
		{
			"id": "relationship.kickback-outlane",
			"kind": "direct",
			"source": output_id("Kickback"),
			"destination": "switch.matrix-25",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.switch-84-85-manual-vs-script-semantics",
			"path": "inputs[binding.device=84,85]",
			"description": (
				"The Switch Locations parts list (printed 2-40) labels public switch 84 \"Opto Made Loop\" and "
				"switch 85 \"Enter Left Ramp\". The pinned driver's own (self-admittedly guessed -- gw.c's header "
				"comment states its author had no access to the physical machine) #define comments assign the "
				"opposite semantic pairing (swLRampEnt=84, swOptoLoopMade=85). The retained known-working script's "
				"own runtime grouping and audio design independently point the same direction as the driver's "
				"guess rather than the manual: SW85_Hit is grouped under the script's own 'supercharger comment "
				"header alongside SW81_Hit/SW82_Hit/SW83_Hit (the three motorized accelerator-wheel optos that each "
				"add ball velocity) and plays a distinct \"sc_loop2\" sound, while SW84_Hit sits in a separate "
				"'Ramp Triggers comment block alongside ordinary lane switches 65/67 and plays only a generic "
				"\"rollover\" sound. Per this project's evidence-authority order the known-working script is "
				"authoritative for runtime semantics and would normally settle this outright, but the script's own "
				"organizational comments are informal authorial judgment, not a documented independent source, and "
				"it is unclear whether the table's author derived this grouping from genuine knowledge of the "
				"physical machine or simply inherited the same guessed driver semantics this manual disagrees "
				"with -- the two agreeing sources (driver guess, script grouping) are not demonstrably independent "
				"of each other. Neither the A-13901-1 Opto Ramp Switch Board Assembly page (which wires switches 84 "
				"and 85 to identical-looking connectors J2/J3 with no location callout) nor the Ramp Locations page "
				"resolves which physical position -- the Accelerator Entrance Ramp Assembly (item 1, upper ramp "
				"entry) or the Accelerator Return Assembly (item 3, lower return path near the diverter) -- "
				"corresponds to which address. Resolution path: a LibPinMAME gameplay harness trace against a legal "
				"gw_l5 ROM, driving a ball through the Supercharger loop and observing which address transitions "
				"first as the ball enters versus which transitions as it completes the loop. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE],
		},
		{
			"id": "conflict.solenoid-31-fastflip-address-not-declared",
			"path": "outputs[binding.device=31]",
			"description": (
				"The retained known-working script binds SolCallback(31) = \"FastFlips.TiltSol\", the standard "
				"nFozzy cFastFlips convention that treats public solenoid 31 as PinMAME's synthetic fast-flip "
				"flipper-enable gate. Pinned gw.c never calls wpc_set_fastflip_addr anywhere in init_gw or "
				"elsewhere (confirmed by an exhaustive case-insensitive source grep). Per src/wpc/wpc.c's "
				"core_gameon function (lines approximately 507-527), when wpc_fastflip_addr is zero (i.e. never "
				"configured) PinMAME instead publishes public solenoids 29-31 as a mirror of bits 5-7 of the "
				"WPC_GILAMPS register -- a general-illumination-lamp state register, unrelated to flipper enable or "
				"game-on -- rather than reading any fast-flip RAM flag. This is a direct contradiction between what "
				"the pinned driver source says public solenoid 31 actually carries and what the retained "
				"known-working table's script assumes it carries. Because this table is nonetheless credited and "
				"described as a working, playable recreation, either this analysis of core.c/wpc.c is missing a "
				"secondary path, or WPC_GILAMPS bit 7 happens to correlate with genuine flipper-enable state for "
				"unrelated reasons in this ROM's own logic, or the recreation's flipper timing is subtly wrong in a "
				"way that has not been reported. Resolution path: a LibPinMAME gameplay harness trace against a "
				"legal gw_l5 ROM, comparing the observed public state of solenoid 31 against the ROM's actual "
				"flipper-enable behavior during play. Unresolved."
			),
			"source_refs": [CORE_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "williams.the-getaway-high-speed-ii.1992",
			"name": "The Getaway: High Speed II",
			"manufacturer": "Williams",
			"year": 1992,
			"kind": "physical_pinball",
			"ipdb_id": 1000,
			"opdb_id": "Grx8Y-MKNe9",
		},
		"coverage": {
			"status": "partial",
			"missing": ["output_semantics", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "conflicted",
				"physical_wiring": "validated",
				"output_semantics": "conflicted",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "candidate",
				"spatial_placement": "conflicted",
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
		"knowledge": {"path": "knowledge/williams/the-getaway-high-speed-ii-1992.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"The Getaway device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	no_spatial_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			no_spatial_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	no_spatial_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			no_spatial_outputs.append(binding)
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
		"status": "partial",
		"blockers": [
			"Switches 33/34 (Gear Shifter Low/High), 56/57/58 (Left/Center/Right Trough), and solenoids 1 "
			"(Diverter High) and 25/26/28 (Enable 1/2/3) have no VPX object anywhere in the retained "
			"extraction; this thin table (875 files, 39,497-byte script) does not model a physical position for "
			"any of them. Lamps 73/74/75 (the A-15283 Stop Light Assembly) are similarly unplaced.",
			"conflict.switch-84-85-manual-vs-script-semantics is unresolved: the manual's own printed labels for "
			"switches 84/85 disagree with the retained known-working script's runtime grouping and audio design, "
			"and the two agreeing 'driver guess' and 'script grouping' sources are not demonstrably independent.",
			"conflict.solenoid-31-fastflip-address-not-declared is unresolved: gw.c never declares a fast-flip "
			"address, so pinned PinMAME publishes public solenoid 31 as a WPC_GILAMPS mirror bit rather than a "
			"genuine flipper-enable signal, yet the retained script's cFastFlips binding assumes the latter.",
			"GI addresses 0 and 1 (both playfield-wired per the manual) share one monolithic 25-member VPX "
			"collection with no way to attribute specific bulbs to one address versus the other, so neither "
			"carries a validated placement.",
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
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_uri": "external:pinmame-vpx-sources/williams/the-getaway-high-speed-ii-1992/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"vpxtool_version": "vpxtool",
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
		"unresolved_input_addresses": sorted(no_spatial_inputs),
		"unresolved_output_bindings": sorted(no_spatial_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		] + [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.the-getaway-high-speed-ii.1992/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/getaway/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"dome118/dome121/dome123, supercharger_p, superramp_p Primitives -- all five sit at raw local-mesh "
			"origin (0,0) with a 90/180-degree rotation and ~1000-unit size, the same 'local-origin Primitive mesh "
			"is not a coordinate' pattern documented elsewhere in this project; excluded rather than promoted.",
			"f118a, f121a, f123a, f121c, f123c Flasher objects -- raw pos_x/pos_y values thousands of units "
			"outside the 0-964/0-2162 playfield bounds; excluded as unusable rather than clamped or guessed.",
			"f120a Light object -- co-located brightness-doubling duplicate of f120 (Free Ride Flasher), matching "
			"the render-doubling pattern documented on other curated titles.",
		],
		"unresolved": [
			"switch.matrix-33", "switch.matrix-34", "switch.matrix-56", "switch.matrix-57", "switch.matrix-58",
			output_id("Diverter High"), output_id("Enable 1"), output_id("Enable 2"), output_id("Enable 3"),
			"lamp.matrix-73", "lamp.matrix-74", "lamp.matrix-75",
			"gi.string-1", "gi.string-2",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Getaway: High Speed II (Williams, 1992) spatial review",
		"",
		f"Status: {report['status']}. This is a comparatively thin retained table (875 extracted files, a "
		"39,497-byte script) and several authoring-relevant addresses have no VPX geometry at all; see Blockers "
		"below.",
		"",
		"The matching source is the retained known-working `Getaway, The - High Speed II v1.2.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW-style script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry. The pinned driver source's own #define "
		"comment labels are treated with reduced authority for semantic device identity specifically, because "
		"the driver's own header comment states its author had no access to the physical machine and guessed "
		"most switch/solenoid labels from a photo and the rulesheet; its numeric public addresses remain real "
		"hardware regardless.",
		"- The retained manual PDF carries an Adobe Acrobat Pro Paper Capture OCR text layer that is present but "
		"garbled for the multi-column wiring tables. Every printed table used here was read from rendered pages "
		"and transcribed into `external:pinmame-review-artifacts/getaway/manual-transcription.md`.",
		"- Several addresses have no VPX geometry at all in this recreation: the gear-shifter switches (33/34) "
		"are driven purely from unrelated keyboard keys with no modeled lever object; the individual trough "
		"positions (56/57/58) are abstracted inside a ball-stack helper class; the Enable relay solenoids "
		"(25/26/28) and Diverter High (1) have no SolCallback-bound visual object. These are recorded as named "
		"gaps rather than projected or invented.",
		"- Switches 31/32 (slingshots) and solenoid 54's causing pair (2/3, the ramp lift) are documented "
		"projections onto the mechanism object the retained script actually manipulates in the same event that "
		"sets the switch/solenoid state, not onto an unrelated placeholder.",
		"- GI addresses 0 and 1 are both playfield-wired per the manual, but the retained script's UpdateGI "
		"ignores its own GI-address parameter and drives one shared 25-member object collection for any GI "
		"address; neither address carries a validated per-address placement as a result.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved (no spatial key) input addresses: {len(report['unresolved_input_addresses'])}",
		f"- Unresolved (no spatial key) output bindings: {len(report['unresolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"This record stays `partial`. Two first-class conflicts remain unresolved "
		"(`conflict.switch-84-85-manual-vs-script-semantics`, `conflict.solenoid-31-fastflip-address-not-"
		"declared`), several authoring-relevant addresses have no spatial placement at all in this thin retained "
		"table, and recreation knowledge remains candidate until those semantic and spatial gaps are documented. "
		"`coverage.missing = [\"output_semantics\", \"recreation_notes\", \"spatial_placement\", "
		"\"unresolved_conflicts\"]` names each gap explicitly.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, {EXTRACTION_FILE_COUNT} files.",
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
		raise RuntimeError(f"Stale The Getaway author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"The Getaway definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"The Getaway seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"The Getaway definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"The Getaway seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"The Getaway spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"The Getaway spatial review drifted from its deterministic curator: {markdown_path}")
	print("The Getaway definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"The Getaway extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("The Getaway retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
