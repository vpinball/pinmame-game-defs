"""Curate the physical Williams Star Trek: The Next Generation (1993) machine definition.

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
# Stays partial: three playfield lamps (53 "Advance in Rank", 85 "Borg Lock", 86 "Borg Jackpot") have
# no world-space light object in the retained extraction (only local-origin Primitive meshes
# parented to an unresolved transform), so their spatial placement cannot be derived without
# inventing a coordinate. See coverage.missing below.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/star-trek-the-next-generation-1993.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/star-trek-the-next-generation-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/star-trek-the-next-generation-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/star-trek-the-next-generation-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/star-trek-the-next-generation-1993.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-dcs"
MANUAL_SOURCE = "manual.williams.star-trek-the-next-generation.1993"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.star-trek-the-next-generation.1993"
VPX_TABLE_SOURCE = "vpx-table.sttng-vpw-mod-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.sttng-vpw-mod-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.sttng-vpw-mod-1-0"

TABLE_SHA256 = "bd00efe46f3ab2392f8c471e65177b348da8e9fcb5829e9f073ab23f69714d8c"
SCRIPT_SHA256 = "073d9971157e822a246b2baf1e8f8033304d1b5272ffb2e9bd9581caf448cd24"
MANUAL_SHA256 = "7f626bce89556b2af4c80bf9eb1a5f74c72cbffe83a85b5142f17140bc820d86"
MANUAL_TRANSCRIPTION_SHA256 = "07f57792c7f405a5e59607a73ac73bb00f9b7daa91ede63477337d4a9ce8f948"

EXTRACTION_RELATIVE_PATH = Path("williams/star-trek-the-next-generation-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/star-trek-the-next-generation-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "c913342c6421558eead345703d08105db5b2779e936f898e56ec1fd177249542"
EXTRACTION_FILE_COUNT = 1585
EXTRACTION_TOTAL_BYTES = 247600334

# Wide-body "Superpin" table, like Williams Indiana Jones: bounds differ from the 952-wide
# divisor every other curated WPC game uses.
TABLE_BOUNDS = "left=0 top=0 right=1093 bottom=2162"

DRIVER_IDS = (
	"sttng_l7", "sttng_d1", "sttng_d2", "sttng_d7", "sttng_dx", "sttng_g7", "sttng_h7",
	"sttng_l1", "sttng_l2", "sttng_l3", "sttng_l5", "sttng_l7c", "sttng_p4", "sttng_p5",
	"sttng_p6", "sttng_p8", "sttng_x7", "sttng_x8", "sttng_x9",
)
DRIVER_COMPATIBILITY = {
	"sttng_l7": ("identical", "Williams production LX-7 game ROM (Sound L-1), the parent driver, shipped with the physical machine."),
	"sttng_d1": ("identical", "DX-1 LED Ghost Fix revision of LX-1; same physical machine and I/O map, a display-defect fix."),
	"sttng_d2": ("identical", "DX-2 LED Ghost Fix revision of LX-2; same physical machine and I/O map."),
	"sttng_d7": ("identical", "DX-7 LED Ghost Fix revision of LX-7, Sound L-1; same physical machine and I/O map."),
	"sttng_dx": ("identical", "DX-7 LED Ghost Fix revision, Special Sound L-1; same physical machine and I/O map."),
	"sttng_g7": ("identical", "LG-7 German-language revision of LX-7; same physical machine and I/O map."),
	"sttng_h7": ("identical", "HG-7 LED Ghost Fix German-language revision; same physical machine and I/O map."),
	"sttng_l1": ("identical", "LX-1 earlier production game ROM for the same physical machine."),
	"sttng_l2": ("identical", "LX-2 earlier production game ROM for the same physical machine."),
	"sttng_l3": ("identical", "LX-3 earlier production game ROM for the same physical machine."),
	"sttng_l5": ("identical", "LX-5 earlier production game ROM for the same physical machine."),
	"sttng_l7c": ("identical", "LX-7C Competition MOD (2017 community patch, rev. L-7X patch b804); a firmware modification of LX-7 for competition play on the same physical machine, not a new game."),
	"sttng_p4": ("identical", "P-4 prototype/pre-production game ROM for the same physical machine."),
	"sttng_p5": ("identical", "P-5 prototype/pre-production game ROM for the same physical machine."),
	"sttng_p6": ("identical", "P-6 LED Ghost Fix prototype/pre-production game ROM for the same physical machine."),
	"sttng_p8": ("identical", "P-8 prototype/pre-production game ROM for the same physical machine."),
	"sttng_x7": ("identical", "LX-7 Special Sound revision, Sound L-1; same physical machine and I/O map."),
	"sttng_x8": ("identical", "LX-8 MOD (2023 community firmware modification, Special Sound L-1); a firmware modification for the same physical machine, not a new game."),
	"sttng_x9": ("identical", "LX-9 MOD (2026 community firmware modification, Special Sound L-1); a firmware modification for the same physical machine, not a new game."),
}

# --- Printed switch matrix (manual page 2-42 wiring, 2-43 parts list). Column*10+Row addressing.
SWITCH_LABELS = {
	11: "Buy-in Button", 12: "Right Fire Button", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Outlane", 16: "Left Return Lane", 17: "Right Return Lane", 18: "Right Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Made Middle Ramp", 24: "Always Closed",
	25: "Enter Right Ramp", 26: "Left 45° Target", 27: "Center 45° Target", 28: "Right 45° Target",
	31: "Borg Lock", 32: "Under Left Gun Sw. 2", 33: "Under Right Gun Sw. 2", 34: "Right Gun Shooter",
	35: "Under Left Lock Sw. 2", 36: "Under Left Gun Sw. 1", 37: "Under Right Gun Sw. 1", 38: "Left Gun Shooter",
	41: "Under Left Lock Sw. 1", 42: "Under Left Lock Sw. 3", 43: "Under Left Lock Sw. 4", 44: "Left Outer Loop",
	45: "Under Top Hole", 46: "Under Left Hole", 47: "Under Borg Hole", 48: "Borg Entry",
	51: "Left Bank Top", 52: "Left Bank Middle", 53: "Left Bank Bottom",
	54: "Right Bank Top", 55: "Right Bank Middle", 56: "Right Bank Bottom",
	57: "Top Drop Target", 58: "Right Outer Loop",
	61: "Trough L.R. 1", 62: "Trough L.R. 2", 63: "Trough L.R. 3", 64: "Trough L.R. 4",
	65: "Trough L.R. 5", 66: "Trough L.R. 6", 67: "Trough Up", 68: "Shooter",
	71: "Left Jet", 72: "Right Jet", 73: "Bottom Jet", 74: "Right Sling", 75: "Left Sling",
	76: "Top Lane Left", 77: "Top Lane Center", 78: "Top Lane Right",
	81: "Time", 82: "Rift", 83: "Made Left Ramp", 84: "Q", 85: "Left 2X Shuttle", 86: "Right 2X Shuttle",
	87: "Made Right Ramp", 88: "Enter Left Ramp",
}
# Every switch shaded "OPTO, TYPICALLY CLOSED" on the printed switch matrix (2-42): columns 3
# (31-38) and 4 (41-48) in full, plus column 6 (61-67, excluding 68 Shooter).
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 61, 62, 63, 64, 65, 66, 67}
# sttngGameData inverted-switch mask, column by column: {0}, {0x00,0x00,0x00,0xff,0xff,0x00,0x7f,
# 0x00,0x00,0x00,0x00,0x00}. Column 3 = 0xff (all 8 inverted), column 4 = 0xff (all 8), column 6 =
# 0x7f (rows 1-7 inverted, row 8/Shooter=68 not inverted). This matches the printed shading
# exactly, column for column and row for row -- zero disagreement, unlike Monster Bash/Indiana
# Jones. The custom column (12, public 121-128) has no printed opto shading and PinMAME's array
# leaves it at its zero-filled default (not inverted); the Gun Circuit Diagram (3-23) independently
# confirms plain switch-contact symbols with no LED/phototransistor pair, so this also agrees.
PINMAME_NORMALIZED_OPTO_SWITCHES = set(OPTO_SWITCHES)
SWITCH_TYPES = {
	11: "button", 12: "button", 13: "button", 14: "tilt", 15: "microswitch",
	16: "other", 17: "other", 18: "microswitch",
	21: "leaf", 22: "microswitch", 23: "microswitch", 24: "other", 25: "microswitch",
	26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 38: "opto",
	41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto", 46: "opto", 47: "opto", 48: "opto",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch", 55: "microswitch", 56: "microswitch",
	57: "microswitch", 58: "microswitch",
	61: "opto", 62: "opto", 63: "opto", 64: "opto", 65: "opto", 66: "opto", 67: "opto", 68: "microswitch",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "leaf", 75: "leaf",
	76: "microswitch", 77: "microswitch", 78: "microswitch",
	81: "microswitch", 82: "microswitch", 83: "microswitch", 84: "microswitch",
	85: "microswitch", 86: "microswitch", 87: "microswitch", 88: "microswitch",
}
# address -> (assembly/opto-assembly part number, switch part number), transcribed from 2-43.
SWITCH_PARTS = {
	11: (None, "20-9663-17"), 12: (None, "5647-12693-03"), 13: (None, "20-9663-16"),
	14: (None, "20-6502-A"), 15: (None, "A-12688"), 16: ("A-16922 Proximity Sensor II PCB with A-17064 Eddy Sensor", None),
	17: ("A-16922 Proximity Sensor II PCB with A-17064 Eddy Sensor", None), 18: (None, "A-12688"),
	21: (None, "A-17238"), 22: (None, "5643-09268-00"), 23: (None, "5647-12693-21"),
	24: (None, "5643-09112-00"), 25: (None, "5647-12693-11"), 26: (None, "A-14690-6"),
	27: (None, "A-16759"), 28: (None, "A-14690-6"),
	31: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	32: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	33: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	34: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	35: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	36: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	37: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	38: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	41: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	42: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	43: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	44: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	45: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	46: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	47: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	48: ("A-16908 (LED) / A-16909 (Photo Transistor)", None),
	51: (None, "A-14691-6"), 52: (None, "A-14691-6"), 53: (None, "A-14691-6"),
	54: (None, "A-14691-6"), 55: (None, "A-14691-6"), 56: (None, "A-14691-6"),
	57: (None, "5647-12693-31"), 58: (None, "A-12688-1"),
	61: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	62: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	63: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	64: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	65: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	66: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	67: ("A-16927 (LED) / A-16926 (Photo Transistor)", None),
	68: (None, "5467-12133-12"),
	71: (None, "A-12030-2"), 72: (None, "A-12030-2"), 73: (None, "A-12030-2"),
	74: (None, "A-17418"), 75: (None, "A-17418"),
	76: (None, "A-12688-1"), 77: (None, "A-12688-1"), 78: (None, "A-12688-1"),
	81: (None, "A-14691-4"), 82: (None, "A-14691-4"), 83: (None, "5647-12693-21"),
	84: (None, "A-14691-4"), 85: (None, "A-15658-4"), 86: (None, "A-15658-4"),
	87: (None, "5647-12693-11"), 88: (None, "5647-12693-11"),
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
	1: ("Orange-Brown", "J205-1", "U18-11"), 2: ("Orange-Red", "J205-2", "U18-9"),
	3: ("Orange-Black", "J205-3", "U18-5"), 4: ("Orange-Yellow", "J205-4", "U18-7"),
	5: ("Orange-Green", "J205-6", "U19-11"), 6: ("Orange-Blue", "J205-7", "U19-9"),
	7: ("Orange-Violet", "J205-8", "U19-5"), 8: ("Orange-Gray", "J205-9", "U19-7"),
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
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J906-5"),
}

# Custom switch column (public 121-128, PinMAME's CORE_CUSTSWCOL=12 arithmetic). Printed matrix
# labels this "column 9" (91-98); sttng.c's own CORE_CUSTSWNO() comments are stale (//92 etc, from
# an older core.h). The retained known-working script's own Controller.Switch(122/125/126/127)
# assignments in CannonLTimer_Timer/CannonRTimer_Timer are the runtime proof of the true addresses.
CUSTOM_SWITCH_LABELS = {122: "Left Gun Mark", 125: "Right Gun Home", 126: "Right Gun Mark", 127: "Left Gun Home"}
CUSTOM_SWITCH_UNUSED = {121, 123, 124, 128}
CUSTOM_SWITCH_MANUAL_ALIAS = {121: "91", 122: "92", 123: "93", 124: "94", 125: "95", 126: "96", 127: "97", 128: "98"}
CUSTOM_SWITCH_PARTS = {122: "5647-12693-58", 125: "5647-12693-08", 126: "5647-12693-58", 127: "5647-12693-08"}

# --- Printed solenoid/flasher table (manual pages 2-44 wiring, 2-45 parts/location).
SOLENOID_LABELS = {
	1: "Left Gun Kicker", 2: "Right Gun Kicker", 3: "Left Gun Popper", 4: "Right Gun Popper",
	5: "Left Popper", 6: "Plunger", 7: "Knocker", 8: "Kickback",
	9: "Left Slingshot", 10: "Right Slingshot", 11: "Trough",
	12: "Left Jet Bumper", 13: "Right Jet Bumper", 14: "Bottom Jet Bumper",
	15: "Top Divertor", 16: "Borg Kicker", 17: "Left Gun Motor", 18: "Right Gun Motor",
	20: "Jets Flasher", 21: "Right Popper Flasher", 22: "Middle Ramp Flasher",
	23: "Shields Flasher", 24: "Autofire Flasher", 25: "Exit Underground Flasher",
	26: "Right Borg Flasher", 27: "Left Borg Flasher", 28: "Center Borg Flasher",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
}
NOT_FITTED_SOLENOID_LABELS = {
	19: "Not Used Solenoid Position 19",
	35: "Not Used Upper Left Flipper Power",
	36: "Not Used Upper Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-DCS Output 37", 38: "Unused WPC-DCS Output 38",
	39: "Unused WPC-DCS Output 39", 40: "Unused WPC-DCS Output 40",
	41: "Unused WPC-DCS Output 41", 42: "Unused WPC-DCS Output 42",
	43: "Unused WPC-DCS Output 43", 44: "Unused WPC-DCS Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}
# The custom board's own silkscreen prints 37-42; PinMAME's public address is CORE_CUSTSOLNO(n) =
# CORE_FIRSTCUSTSOL - 1 + n = 50 + n, i.e. 51-56. The retained known-working script's own
# SolCallBack(51..54) and SolModCallBack(55/56) registrations confirm this directly.
CUSTOM_SOLENOID_LABELS = {
	51: "Under Divertor Top", 52: "Under Divertor Bottom",
	53: "Top Drop Up", 54: "Top Drop Down",
	55: "Romulan Flashers", 56: "Right Ramp Flashers",
}
CUSTOM_SOLENOID_MANUAL_ALIAS = {51: "37", 52: "38", 53: "39", 54: "40", 55: "41", 56: "42"}
CUSTOM_SOLENOID_KIND = {51: "motor", 52: "motor", 53: "motor", 54: "motor", 55: "flasher", 56: "flasher"}

SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power (backbox)"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", power_connection="J107-3", part_number="AE-23-800", printed_type="High Power"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(control_connection="J127-3", driver_transistor="Q56", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", power_connection="J107-2", part_number="AE-26-1500", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", power_connection="J107-2", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", power_connection="J107-2", part_number="AE-25-1000", printed_type="Low Power"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", power_connection="J107-2", part_number="AL-23-800", printed_type="Low Power"),
	17: dict(control_connection="J126-1", driver_transistor="Q42", power_connection="J118-2", part_number="A-17562", printed_type="Low Power motor"),
	18: dict(control_connection="J126-2", driver_transistor="Q40", power_connection="J118-2", part_number="A-17562", printed_type="Low Power motor"),
	19: dict(driver_transistor="Q38", printed_type="Not Used"),
	20: dict(control_connection="J126-4", driver_transistor="Q36", power_connection="J107-6", printed_type="Flasher"),
	21: dict(control_connection="J126-5", driver_transistor="Q28", power_connection="J107-6", secondary_connection="J125-6", secondary_power="J106-5", printed_type="Flasher"),
	22: dict(control_connection="J126-6", driver_transistor="Q30", power_connection="J107-6", printed_type="Flasher"),
	23: dict(control_connection="J126-7", driver_transistor="Q34", power_connection="J107-6", secondary_connection="J125-8", secondary_power="J106-5", printed_type="Flasher"),
	24: dict(control_connection="J126-8", driver_transistor="Q32", power_connection="J107-6", printed_type="Flasher"),
	25: dict(control_connection="J122-1", driver_transistor="Q26", power_connection="J107-6", secondary_connection="J124-1", secondary_power="J106-5", printed_type="Gen. Purpose"),
	26: dict(control_connection="J122-2", driver_transistor="Q24", power_connection="J107-6", secondary_connection="J124-2", secondary_power="J106-5", printed_type="Gen. Purpose"),
	27: dict(control_connection="J122-3", driver_transistor="Q22", power_connection="J107-6", secondary_connection="J124-3", secondary_power="J106-5", printed_type="Gen. Purpose"),
	28: dict(control_connection="J122-4", driver_transistor="Q20", power_connection="J107-6", secondary_connection="J124-5", secondary_power="J106-5", printed_type="Gen. Purpose"),
	33: dict(control_connection="J902-6", driver_transistor="Q2", power_connection="J907-1", part_number="FL-11629", printed_type="Fliptronic power"),
	34: dict(control_connection="J902-4", driver_transistor="Q7", power_connection="J907-1", part_number="FL-11629", printed_type="Fliptronic hold"),
	35: dict(control_connection="J902-3", driver_transistor="Q1", power_connection="J907-4", printed_type="Fliptronic power (not fitted)"),
	36: dict(control_connection="J902-1", driver_transistor="Q5", power_connection="J907-4", printed_type="Fliptronic hold (not fitted)"),
	45: dict(control_connection="J902-13", driver_transistor="Q4", power_connection="J907-7", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(control_connection="J902-11", driver_transistor="Q11", power_connection="J907-7", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(control_connection="J902-9", driver_transistor="Q3", power_connection="J907-9", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(control_connection="J902-7", driver_transistor="Q9", power_connection="J907-9", part_number="FL-11629", printed_type="Fliptronic hold"),
	51: dict(control_connection="J4-2", driver_transistor="Q16", power_connection="J107-1", part_number="AE-25-1000", printed_type="Low Power (8-Driver Board)"),
	52: dict(control_connection="J4-4", driver_transistor="Q15", power_connection="J107-1", part_number="AE-25-1000", printed_type="Low Power (8-Driver Board)"),
	53: dict(control_connection="J4-5", driver_transistor="Q14", power_connection="J107-1", part_number="AE-26-1200", printed_type="Low Power (8-Driver Board)"),
	54: dict(control_connection="J4-6", driver_transistor="Q13", power_connection="J107-1", part_number="SM1-26-600", printed_type="Low Power (8-Driver Board)"),
	55: dict(control_connection="J3-2", driver_transistor="Q9", power_connection="J107-6", secondary_connection="J3-2", secondary_power="J106-5", printed_type="Flasher (8-Driver Board)"),
	56: dict(control_connection="J3-3", driver_transistor="Q10", power_connection="J107-6", secondary_connection="J3-3", secondary_power="J106-5", printed_type="Flasher (8-Driver Board)"),
}
FLIPPER_DRIVE_WIRE = {45: "Blu-Yel", 46: "Org-Grn", 47: "Gry-Yel", 48: "Org-Blu", 33: "Blu-Yel", 34: "Org-Vio", 35: "Gry-Yel", 36: "Org-Gry"}

SOLENOID_ASSEMBLIES = {
	1: "A-17081-L", 2: "A-17081-R", 3: "A-17049-1", 4: "A-17049-1", 5: "A-17049",
	6: "A-16757", 7: "B-10686-1", 8: "A-17234", 9: "B-9362-L-2", 10: "B-9362-R-2",
	11: "A-16765", 12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2", 15: "A-16763",
	16: "A-17219", 17: "A-17220-L", 18: "A-17220-R",
	45: "A-15205-R-2", 46: "A-15205-R-2", 47: "A-15205-L-2", 48: "A-15205-L-2",
	33: "A-15205-R-2", 34: "A-15205-R-2",
	51: "A-17124", 52: "A-17124", 53: "A-14615", 54: "A-14615",
}
# Retained VPW-mod script callbacks/animation drivers, per public solenoid address.
SOLENOID_CALLBACKS = {
	1: "LeftCannonKicker (Kicker1.kick)", 2: "RightCannonKicker (Kicker2.kick)",
	3: "UnderLeftGun (sw36.kick)", 4: "UnderRightGun (sw37.kick)",
	5: "LeftLock (sw41.kick)", 6: "AutoPlunge (AutoPlunger.Kick)",
	7: 'vpmSolSound SoundFX("Knocker",DOFKnocker)', 8: "KickBack (KickBackPlunger.Fire)",
	11: "SolRelease (bsTrough.ExitSol_On)", 15: "TopDiverter (diverter.RotateToEnd)",
	16: "BorgLock.SolOut", 17: "LeftCannonMotor (CannonLTimer.Enabled)",
	18: "RightCannonMotor (CannonRTimer.Enabled)",
	20: "Flash120 (l120/l83 intensity)", 21: "Flash121 (f121.opacity)",
	22: "Flash122 (f122.opacity)", 23: "Flash123 (f123.opacity)",
	24: "SetLamp 124 (l124)", 25: "Flash125 (f125.opacity)",
	26: "Flash126 (f126.opacity)", 27: "Flash127 (f127.opacity)", 28: "Flash128 (f128.opacity)",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
	51: "UnderDiverterTop (DiverterFRG.isDropped)", 52: "UnderDiverterBottom (DiverterFLG.isDropped)",
	53: "TopDrop.SolDropUp (sw57)", 54: "TopDrop.SolDropDown (sw57)",
	55: "Flash141 (f141.opacity)", 56: "Flash142 (f142.opacity)",
}

# (bulb description, total printed quantity, playfield-emitter count)
FLASHER_BULBS = {
	20: ("#89 (1) on the playfield", 1, 1),
	21: ("#89 (1) on the playfield and #906 (1) on the backbox", 2, 1),
	22: ("#89 (1) on the playfield", 1, 1),
	23: ("#906 (3) on the playfield and #906 (1) on the backbox", 4, 3),
	24: ("#906 (1) on the playfield", 1, 1),
	25: ("#89 (1) on the playfield and #906 (1) on the backbox", 2, 1),
	26: ("#906 (2) on the playfield and #906 (1) on the backbox", 3, 2),
	27: ("#906 (2) on the playfield and #906 (1) on the backbox", 3, 2),
	28: ("#906 (2) on the playfield and #906 (1) on the backbox", 3, 2),
	55: ("#906 (1) on the playfield and #906 (1) on the backbox", 2, 1),
	56: ("#89 (1) on the playfield and #906 (1) on the backbox", 2, 1),
}

# --- Printed lamp matrix (manual page 2-40 wiring, 2-41 parts list). First digit is the column.
LAMP_LABELS = {
	11: "Left Bank Top", 12: "Left Bank Middle", 13: "Ship Mode 1", 14: "Ship Mode 2",
	15: "Left Bank Bottom", 16: "Final Frontier", 17: "Shoot Again", 18: "Ship Mode 7",
	21: "Ship Mode 3", 22: "Ship Mode 4", 23: "Ship Mode 5", 24: "Right Bank Top",
	25: "Right Bank Middle", 26: "Command Decision", 27: "Ship Mode 6", 28: "Right Bank Bottom",
	31: "Top Lane Left", 32: "Top Lane Center", 33: "Top Lane Right", 34: "Bonus 2X",
	35: "Bonus 4X", 36: "Multipliers Held", 37: "Bonus 8X", 38: "Bonus 10X",
	41: "Q", 42: "Generic 1", 43: "Right Lock", 44: "Holodeck",
	45: "Right 2X Shuttle", 46: "Generic 4", 47: "Right Millions", 48: "Left 2X Shuttle",
	51: "Left Return Lane", 52: "Left Launcher", 53: "Advance in Rank", 54: "Generic 6",
	55: "Super", 56: "Jackpot", 57: "Extra Ball", 58: "Start Mission",
	61: "Generic 3", 62: "Increase Warp", 63: "Spinner", 64: "Generic 7",
	65: "Left Millions", 66: "Jackpot X", 67: "Rift", 68: "Time",
	71: "Generic 2", 72: "Top 3-bank Left", 73: "Top 3-bank Center", 74: "Top 3-bank Right",
	75: "Left Lock", 76: "Generic 5", 77: "Worm Hole", 78: "Borg Ship",
	81: "Right Return Lanes", 82: "Right Launcher", 83: "Million Jets", 84: "Kickback",
	85: "Borg Lock", 86: "Borg Jackpot", 87: "Buy-in", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-17356", "#555"), 12: ("A-17356", "#555"), 13: ("A-17356", "#555"), 14: ("A-17356", "#555"),
	15: ("A-17356", "#555"), 16: ("A-17356", "#555"), 17: ("A-11754", "#44"), 18: ("A-17356", "#555"),
	21: ("A-17356", "#555"), 22: ("A-17356", "#555"), 23: ("A-17356", "#555"), 24: ("A-17356", "#555"),
	25: ("A-17356", "#555"), 26: ("A-17356", "#555"), 27: ("A-17356", "#555"), 28: ("A-17356", "#555"),
	31: ("A-17014", "#555"), 32: ("A-17014", "#555"), 33: ("A-17014", "#555"), 34: ("A-16920", "#555"),
	35: ("A-16920", "#555"), 36: ("A-16920", "#555"), 37: ("A-16920", "#555"), 38: ("A-16920", "#555"),
	41: ("A-11905", "#44"), 42: ("A-11905", "#44"), 43: ("A-11754", "#44"), 44: ("A-17013", "#555"),
	45: ("A-17013", "#555"), 46: ("A-17013", "#555"), 47: ("A-17013", "#555"), 48: ("A-17013", "#555"),
	51: ("A-11754", "#44"), 52: ("A-12887", "#555"), 53: ("A-17330", "#555"), 54: ("A-17012", "#555"),
	55: ("A-17012", "#555"), 56: ("A-17012", "#555"), 57: ("A-11905", "#44"), 58: ("A-11905", "#44"),
	61: ("A-11905", "#44"), 62: ("A-11905", "#44"), 63: ("A-11905", "#44"), 64: ("A-17012", "#555"),
	65: ("A-17012", "#555"), 66: ("A-17012", "#555"), 67: ("A-11905", "#44"), 68: ("A-11905", "#44"),
	71: ("A-11905", "#44"), 72: ("A-11905", "#44"), 73: ("A-11905", "#44"), 74: ("A-11905", "#44"),
	75: ("A-11905", "#44"), 76: ("A-11905", "#44"), 77: ("A-11905", "#44"), 78: ("A-17158", "#555"),
	81: ("A-11754", "#44"), 82: ("A-12887", "#555"), 83: ("A-11754", "#44"), 84: ("A-11905", "#44"),
	85: ("A-17272", "#555"), 86: ("A-11905", "#44"), 87: ("20-9663-17", None), 88: ("20-9663-16", None),
}
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
# Co-located Light objects stacked purely for brightness (l<nn>/l<nn>b pairs); the primary object
# is used and the duplicate is documented render doubling.
LAMP_RENDER_DOUBLE_ADDRESSES = tuple(sorted(set(range(11, 89)) - {c * 10 + r for c in (9,) for r in range(1, 9)}))

# --- Normalized playfield coordinates derived from the retained VPWmod v1.0 extraction
# (x/1093, y/2162; review-artifacts/star-trek-the-next-generation-1993/vpx-geometry.txt).
SWITCH_POSITIONS = {
	15: [(0.047772, 0.755208)], 16: [(0.121602, 0.729143)], 17: [(0.877509, 0.729143)],
	18: [(0.953799, 0.75455)], 23: [(0.124006, 0.076768)], 25: [(0.803822, 0.293039)],
	26: [(0.25397, 0.122602)], 27: [(0.315383, 0.134855)], 28: [(0.370806, 0.107798)],
	31: [(0.588037, 0.096601)], 32: [(0.169705, 0.518748)], 33: [(0.823115, 0.516963)],
	34: [(0.828697, 0.66684)], 35: [(0.17694, 0.46744)], 36: [(0.120591, 0.524254)],
	37: [(0.877592, 0.524768)], 38: [(0.171778, 0.666695)],
	41: [(0.126267, 0.474172)], 42: [(0.222411, 0.461494)], 43: [(0.27282, 0.455053)],
	44: [(0.459426, 0.06991)], 45: [(0.521437, 0.028485)], 46: [(0.200142, 0.201556)],
	47: [(0.600536, 0.189068)], 48: [(0.462455, 0.049251)],
	51: [(0.184259, 0.550113)], 52: [(0.152518, 0.569506)], 53: [(0.120475, 0.589279)],
	54: [(0.83435, 0.552343)], 55: [(0.864224, 0.5714)], 56: [(0.894997, 0.590296)],
	57: [(0.577522, 0.027112)], 58: [(0.952065, 0.115248)], 68: [(0.948991, 0.914339)],
	61: [(0.868281, 0.878273)], 62: [(0.868281, 0.878273)], 63: [(0.868281, 0.878273)],
	64: [(0.868281, 0.878273)], 65: [(0.868281, 0.878273)], 66: [(0.868281, 0.878273)],
	67: [(0.868281, 0.878273)],
	71: [(0.690471, 0.186714)], 72: [(0.869249, 0.161881)], 73: [(0.821842, 0.251134)],
	74: [(0.703284, 0.728689)], 75: [(0.300038, 0.727762)],
	76: [(0.660737, 0.10299)], 77: [(0.742394, 0.091092)], 78: [(0.824764, 0.080636)],
	81: [(0.268423, 0.419949)], 82: [(0.310949, 0.411307)], 83: [(0.206778, 0.077864)],
	84: [(0.675711, 0.229665)], 85: [(0.705453, 0.334566)], 86: [(0.823546, 0.362106)],
	87: [(0.921732, 0.08056)], 88: [(0.134398, 0.2674)],
}
SWITCH_PROJECTIONS = {
	31: "Projected onto the Borg Lock kicker (Kicker BorgKicker, table object center): the retained script's BorgLock ball-stack class (cvpmBallStack.InitSw 0,31,0,0,0,0,0,0) has no separate playfield trigger object for this position; the single lock ball rests directly at the kicker used to eject it.",
	34: "Projected onto the right gun kicker (Kicker Kicker2, table object center): the retained script's Kicker2_Hit handler sets Controller.Switch(34)=1 when a ball reaches the right gun barrel and RightCannonKicker clears it on launch (Controller.Switch(34)=0) -- there is no separate playfield sensor object beyond the kicker itself.",
	38: "Projected onto the left gun kicker (Kicker Kicker1, table object center); see switch 34's right-side counterpart -- Kicker1_Hit sets Controller.Switch(38)=1 and LeftCannonKicker clears it.",
	61: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center): the retained script models the six-position trough purely as a cvpmBallStack ball counter (bsTrough.InitSw 0,66,65,64,63,62,61,0) with no discrete playfield trigger per position.",
	62: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.",
	63: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.",
	64: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.",
	65: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.",
	66: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center); see switch 61.",
	67: "Projected onto the trough ball-release kicker (Kicker BallRelease, table object center): the retained script's SolRelease handler pulses this switch (vpmTimer.PulseSw 67) in the same event that fires bsTrough.ExitSol_On, with no separate playfield sensor object.",
	68: "Projected onto the auto plunger (Kicker AutoPlunger, table object center): the retained script's AutoPlunger_Hit handler sets Controller.Switch(68)=1 directly on the plunger kicker object, with no separate playfield sensor.",
}
CUSTOM_SWITCH_POSITIONS = {
	122: [(0.207336, 0.719294)], 125: [(0.792664, 0.719294)],
	126: [(0.792664, 0.719294)], 127: [(0.207336, 0.719294)],
}
CUSTOM_SWITCH_PROJECTIONS = {
	122: "Projected onto the left gun's own rotating base (Primitive CannonBaseL, table object center): the retained script's CannonLTimer_Timer sets Controller.Switch(122)=1 while CannonBaseL.ObjRotZ sits in -20..9 degrees, directly from the gun's continuous rotation angle, not from a discrete cam-actuated sensor object. The motor (solenoid 17) drives the rotation continuously; it does not itself actuate this switch -- the switch senses the resulting mechanical position.",
	125: "Projected onto the right gun's own rotating base (Primitive CannonBaseR, table object center); see switch 122's left-side counterpart -- CannonRTimer_Timer sets Controller.Switch(125)=1 for -20..-17 degrees (Right Gun Home).",
	126: "Projected onto the right gun's own rotating base (Primitive CannonBaseR, table object center); see switch 125 -- CannonRTimer_Timer sets Controller.Switch(126)=1 for -20..9 degrees (Right Gun Mark).",
	127: "Projected onto the left gun's own rotating base (Primitive CannonBaseL, table object center); see switch 122 -- CannonLTimer_Timer sets Controller.Switch(127)=1 for -20..-17 degrees (Left Gun Home).",
}

SOLENOID_POSITIONS = {
	1: [(0.171778, 0.666695)], 2: [(0.828697, 0.66684)],
	3: [(0.120591, 0.524254)], 4: [(0.877592, 0.524768)],
	5: [(0.126267, 0.474172)], 6: [(0.948991, 0.914339)],
	8: [(0.048195, 0.844989)], 9: [(0.235884, 0.719923)], 10: [(0.767871, 0.719847)],
	11: [(0.868281, 0.878273)],
	12: [(0.690471, 0.186714)], 13: [(0.869249, 0.161881)], 14: [(0.821842, 0.251134)],
	15: [(0.152852, 0.0)], 16: [(0.588037, 0.096601)],
	17: [(0.207336, 0.719294)], 18: [(0.792664, 0.719294)],
	20: [(0.795011, 0.200739)], 21: [(0.998909, 0.553857)], 22: [(0.379666, 0.09429)],
	23: [(0.2011, 0.53323)], 24: [(0.501047, 0.82363)], 25: [(0.001161, 0.610071)],
	26: [(0.808326, 0.068918)], 27: [(0.34538, 0.197502)], 28: [(0.530916, 0.213812)],
	33: [(0.887466, 0.440796)], 34: [(0.887466, 0.440796)],
	45: [(0.650785, 0.843663)], 46: [(0.650785, 0.843663)],
	47: [(0.352242, 0.843663)], 48: [(0.352242, 0.843663)],
	51: [(0.450192, 0.395118)], 52: [(0.450256, 0.444442)],
	53: [(0.577522, 0.027112)], 54: [(0.577522, 0.027112)],
	55: [(0.315933, 0.239165)], 56: [(0.939904, 0.0412)],
}
SOLENOID_PROJECTIONS = {
	15: "Y clamped from -0.008688 (raw local coordinate -18.784, essentially at the rear playfield edge) to the schema-valid boundary 0.0; the retained table's Flipper-typed \"Diverter\" primitive sits fractionally above y=0, matching the manual's Top Divertor location near the very top of the playfield.",
}

# GI address 0 (Shields G.I.): St1Shields collection, 6 ShieldGiBig1-6 Light objects; the 6
# ShieldGiFlasherS1-6 Flasher objects sit within 0.002 normalized units of their ShieldGiBig
# counterpart (co-located glow-dome render doubles) and are excluded.
GI_POSITIONS = {
	0: [
		(0.685488, 0.565824), (0.625916, 0.541167), (0.461632, 0.525631),
		(0.371954, 0.541418), (0.315344, 0.5667), (0.538863, 0.52524),
	],
	# GI address 3 (Playfield G.I.): St4PFGI collection deduplicated by nearest-neighbor pairing
	# (each physical bulb models a "Gis*"+"Gi*" co-located Light pair); Flasher1-5/GiBig excluded
	# as duplicates of already-counted flasher devices / a synthetic ambient-wash helper; l1/l2/
	# l1b/l2b excluded as unidentified cosmetic lights with no manual bulb to match.
	3: [
		(0.826675, 0.782192), (0.178388, 0.782245), (0.265608, 0.757125), (0.731792, 0.7569),
		(0.956547, 0.396425), (0.960218, 0.580045), (0.054244, 0.303007), (0.048059, 0.427956),
		(0.048676, 0.521722), (0.05598, 0.612978), (0.185532, 0.292324), (0.282919, 0.392152),
		(0.094564, 0.114219), (0.271267, 0.037158), (0.864568, 0.075676), (0.701067, 0.097463),
		(0.917412, 0.018927), (0.870647, 0.162114),
	],
	# GI address 4 (Return Lane/Coin): St5ReLa collection, same dedup rule. Two raw members
	# (Gi9, Gi11) sit at coordinates identical to two St4PFGI members and are excluded here to
	# avoid a double placement of the same physical bulb under two GI addresses -- their paired
	# "Gis*" sibling belongs to St4PFGI, so that is their recorded home circuit.
	4: [
		(0.282962, 0.81815), (0.72246, 0.818346), (0.897515, 0.121828), (0.894051, 0.10044),
		(0.782373, 0.086457), (0.619316, 0.107571), (0.139406, 0.199628), (0.163235, 0.253351),
		(0.081393, 0.379928), (0.046748, 0.475593), (0.047182, 0.567444), (0.960267, 0.490414),
		(0.777489, 0.680136), (0.220963, 0.678023), (0.689325, 0.187262), (0.819299, 0.252159),
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
		raise RuntimeError(f"Star Trek: The Next Generation retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Star Trek: The Next Generation extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Star Trek: The Next Generation retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Star Trek: The Next Generation retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Star Trek: The Next Generation retained extraction identity mismatch: "
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


# Committed crops are binary, so unlike the transcriptions they are hashed from
# the file on disk rather than from a literal in this curator.
EXCERPT_IMAGE_HASHES = {
	path.name: hashlib.sha256(path.read_bytes()).hexdigest()
	for path in sorted((Path(__file__).resolve().parents[1] / "evidence/excerpts/williams.star-trek-the-next-generation.1993").glob("*.webp"))
}


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the sttng_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/sttng.c sttngGameData GEN_WPCDCS with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0xff,0xff,0x00,0x7f,0x00,0x00,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_U)|"
				"FLIP_SOL(FLIP_L|FLIP_UR), hw.swCol=1/hw.custSol=6, sw*/s* defines, sttng_stateDef ball-tracking "
				"simulator (GUN_HOME=8*2=16, GUN_MARK=8*7=56, GUN_END=8*20=160 step constants), sttng_handleMech "
				"(diverter position counters and gun rotation buffering), sttng_getSol (reads WPC_EXTBOARD1 bits "
				"0-5 for the six custom solenoids), sttng_swRowRead (9th switch column read-back); src/wpc/core.h "
				"CORE_CUSTSWCOL=CORE_STDSWCOLS=12, CORE_CUSTSWNO(c,r)=(CORE_CUSTSWCOL-1+c)*10+r, "
				"CORE_FIRSTCUSTSOL=51, CORE_CUSTSOLNO(n)=CORE_FIRSTCUSTSOL-1+n, CORE_FIRSTUFLIPSOL=33, "
				"CORE_FIRSTLFLIPSOL=45; src/wpc/core.c core_getSol dispatch (the solNo<=44 branch returns 0 for "
				"GEN_WPCDCS before ever reaching hw.getSol, proving the six custom solenoids must be numbered "
				"above 50 for sttng_getSol to be reachable at all); src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WPCDCS=0x10"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-dcs.json",
			"revision": "repository",
			"locator": "WPC-DCS public switch, DIP, solenoid, lamp, and five-GI address rules, including the custom switch/solenoid column arithmetic and the no-LPDC 37-44 unused range, reused unchanged from Williams Indiana Jones: The Pinball Adventure",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.star-trek-the-next-generation.1993/archive-arcademanual_Star_Trek_TNG_OPS/Star_Trek_TNG_OPS.pdf",
			"original_filename": "Star_Trek_TNG_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"136-page scan of the Williams Star Trek: The Next Generation operations manual (Internet Archive "
				"item arcademanual_Star_Trek_TNG_OPS, textfiles.com manual library). Printed pages 2-40 through "
				"2-45 carry the lamp/switch/solenoid location parts lists and their matrix and solenoid/flasher "
				"wiring tables; printed pages 3-14 through 3-28 carry the Flipper Opto, LED/Photo Transistor, 7 "
				"Ball Trough, Proximity Sensor II, Eddy Sensor, Motor EMI, Gun Circuit Diagram, 8-Driver PCB, and "
				"16-Opto PCB assembly/schematic pages that fix device construction and the true custom-column/"
				"custom-solenoid public addressing; printed page 1-41 documents the gun/cannon assembly's physical "
				"topology."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive (textfiles.com manual library)",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.sttng.switch-matrix",
					"locator": "PDF page 94, printed 2-42, Switch Matrix",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/switch-matrix.md",
					"sha256": "5acc795d6f5a8dc2286af376cd0a11645ac0a6d2e9bd4690306b5ec039b7ae56",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/switch-matrix.webp",
					"image_sha256": "9de182e94db2db6cfbaf2903b902918d0b21608a4a7d777d8ee4cbc1f85d314b",
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 94, crop box 0.10,0.135,0.975,0.63 of the page, rendered at 300 dpi with pdftoppm, reduced to 700px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.switch-locations",
					"locator": "PDF page 95, printed 2-43, Switch Locations parts list",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/switch-locations.md",
					"sha256": "f7d48e1f0142ca868b9ad95523153647c7d61b862bd39e5205fc9db0c338fb22",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/switch-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-locations.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 95, crop box 0.02,0.05,0.99,0.94, scanned page rendered at its native resolution (embedded image xref 403, 2567px across 8.33in), rendered at 308 dpi, 2471x3206 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.gun-assembly",
					"locator": "PDF page 121 (printed 3-23, Gun Circuit Diagram) and PDF page 51 (printed 1-41, Removing the Gun Assembly)",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/gun-assembly.md",
					"sha256": "357928d58c3934b62f28643c744a9c8aaad486bfeee5bcf11c6764ad9d46267d",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/gun-assembly.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["gun-assembly.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 121, crop box 0.03,0.06,0.98,0.94, scanned page rendered at its native resolution (embedded image xref 521, 2588px across 8.40in), rendered at 308 dpi, 2420x3170 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.opto-and-sensor-boards",
					"locator": "PDF pages 112-113 (3-14/3-15), 118-120 (3-20/3-21/3-22), 124-125 (3-26/3-27), opto and proximity-sensor board assemblies",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/opto-and-sensor-boards.md",
					"sha256": "614c5c18f18f73ef5fbbc8b7a93059ba9d3d065406035dc3e570ca4715e49ae4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.lamp-matrix-and-locations",
					"locator": "PDF pages 92-93, printed 2-40/2-41, Lamp Matrix and Lamp Locations",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/lamp-matrix-and-locations.md",
					"sha256": "8f7c6f3627d2dd964598d9566266b5588d7d399926a90090eab543664a809dfe",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/lamp-matrix-and-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-matrix-and-locations.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 92, crop box 0.03,0.03,0.98,0.56, scanned page rendered at its native resolution (embedded image xref 389, 2574px across 8.36in), rendered at 308 dpi, 2420x1910 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.solenoid-flasher-wiring",
					"locator": "PDF page 96, printed 2-44, Solenoid/Flasher Table and Flipper Circuits",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/solenoid-flasher-wiring.md",
					"sha256": "52a786aec5587e96ce97eea8b6a3dd5882c112837c669236c36c32eb5df581f2",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/solenoid-flasher-wiring.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-flasher-wiring.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 96, crop box 0.02,0.03,0.99,0.79, scanned page rendered at its native resolution (embedded image xref 408, 2546px across 8.27in), rendered at 308 dpi, 2471x2738 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.solenoid-flasher-locations",
					"locator": "PDF page 97, printed 2-45, Solenoid/Flasher Location parts list",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/solenoid-flasher-locations.md",
					"sha256": "82442dac2dea28f11827bc1c6815b7e3f33ed8becb6af4e6491e80d3bdae9648",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/solenoid-flasher-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-flasher-locations.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 97, crop box 0.02,0.06,0.58,0.97, scanned page rendered at its native resolution (embedded image xref 412, 2567px across 8.33in), rendered at 308 dpi, 1427x3278 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.sttng.general-illumination",
					"locator": "PDF page 96, printed 2-44, General Illumination wiring",
					"path": "evidence/excerpts/williams.star-trek-the-next-generation.1993/general-illumination.md",
					"sha256": "2a260ba559a63d0272d21f68365e3ea83dfd1848f797f6672ea06feeb385c549",
					"image": "evidence/excerpts/williams.star-trek-the-next-generation.1993/general-illumination.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["general-illumination.webp"],
					"image_derivation": "Star_Trek_TNG_OPS.pdf page 96, crop box 0.02,0.518,0.99,0.605, scanned page rendered at its native resolution (embedded image xref 408, 2546px across 8.27in), rendered at 308 dpi, 2471x315 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/star-trek-the-next-generation-1993/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with "
				"the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/williams.star-trek-the-next-generation.1993/. The retained PDF "
				"carries an OCR text layer, but every printed table used here was visually confirmed against the "
				"rendered page rather than trusted from OCR text alone."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/source/Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx",
			"original_filename": "Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW Mod v1.0 recreation of the physical machine. Exact playfield bounds are "
				f"{TABLE_BOUNDS} (a wide-body \"Superpin\" table, matching Williams Indiana Jones); normalized "
				"coordinates are x/1093 and y/2162. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (149,787 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "sttng_l7", Const UseSolenoids = 2 (fast flips), the SolCallback/SolModCallback '
				"table for solenoids 1-28 and 51-56 (public addresses, confirming the custom-solenoid arithmetic "
				"against the manual's stale 37-42 silkscreen numbers), the CannonLTimer_Timer/CannonRTimer_Timer "
				"handlers that set Controller.Switch(122/125/126/127) directly from CannonBaseL/CannonBaseR.ObjRotZ "
				"(confirming the custom-switch-column arithmetic against the manual's stale 91-98 silkscreen "
				"numbers and the driver's own stale //92 etc. comments), the bsTrough/BorgLock cvpmBallStack "
				"instances (proving switches 31 and 61-67 have no discrete playfield trigger object), and "
				"UpdateGI mapping GI addresses 0/3/4 to the St1Shields/St4PFGI/St5ReLa playfield emitter "
				"collections (GI 1/2 drive only VR-backglass-room helper objects, confirming they are backbox-only)."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/extracted-vpxtool.manifest.json",
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
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
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
				notes += " Both the printed matrix and the switch-locations parts list mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					" Printed shaded \"OPTO, TYPICALLY CLOSED\" on the switch matrix (2-42) and listed with a "
					"dual LED/photo-transistor part pair and no switch part number on the switch-locations parts "
					"list (2-43) -- an opto interrupter that rests closed. PinMAME's sttngGameData inverted-switch "
					"mask covers this exact column and row set ({0x00,0x00,0x00,0xff,0xff,0x00,0x7f,...}), so the "
					"public switch state is already normalized and must not be inverted again; the manual shading "
					"and the emulator mask agree address for address here, unlike Monster Bash's Dracula-position "
					"optos or Indiana Jones's wheel-position optos."
				)
			elif address == 16 or address == 17:
				notes += (
					" Printed with no LED/photo-transistor part pair; the switch-locations parts list assigns "
					"assembly A-16922 (Proximity Sensor II PCB, TDA0161 eddy-current IC) and A-17064 (Eddy Sensor "
					"Assembly) rather than a leaf switch or an opto pair. Section 3's own Proximity Sensor II PCB "
					"schematic (3-20) independently wires this exact switch column/row pair, and PinMAME's inverted-"
					"switch mask leaves this column (column 1) at 0x00 -- construction, wiring, and normalization "
					"all agree this is an eddy-current sensor, not an opto, and is not inverted."
				)
			if address == 24:
				notes += " Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
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
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {11, 13, 14, 21, 22}:
					role = {
						11: "cabinet.buy-in",
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
				elif address == 12:
					extra["roles"] = ["cabinet.fire-button"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet (control grip trigger)"
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316"),
		115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "used", False, "leaf", "SW-1A-194", None),
		116: ("Upper Right Flipper Button", "flipper.upper.right.button", "used", True, "opto", None, "A-17316"),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly) in flipper_inputs.items():
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
				" This game has no upper-left flipper solenoid and the switch-locations parts list on manual page "
				"2-43 marks this position Not Used (blank part number)."
			)
			physical["location"] = "not installed"
		elif switch_type == "opto":
			notes += (
				" Printed A-17316 Flipper Opto PCB Assembly (an opto that is typically closed). WPC-DCS reads the "
				"flipper column through an unconditional bitwise complement (src/wpc/wpc.c WPC_FLIPPERS, gated on "
				"(gen & GENWPC_HASWPC95)==0) regardless of the physical switch's construction, so the public switch "
				"state is already normalized."
			)
		else:
			notes += " Printed plain (non-opto) end-of-stroke leaf switch (SW-1A-194)."
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"wiring": {"board": "WPC-DCS CPU board (Fliptronic II)", "drive_wire": wire, "drive_connection": connection},
		}
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

	# Fliptronic F7 (public 117) is repurposed as a plain playfield Spinner, confirmed by the
	# retained script's sw117spinner_Spin handler (vpmTimer.PulseSw 117).
	items.append(
		_device(
			"switch.generic-117",
			"Spinner",
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
				"part_number": "5647-12693-11",
				"switch_type": "leaf",
				"notes": (
					"Printed Fliptronic grounded switch F7. The switch-locations parts list on page 2-43 names it "
					"Spinner (a plain leaf part, 5647-12693-11) rather than an upper-left flipper position, and the "
					"footnote on the switch matrix page marks it \"used as switches other than flipper switches in "
					"this game.\" The retained script's sw117spinner_Spin handler independently confirms it: "
					"vpmTimer.PulseSw 117."
				),
			},
			wiring={"board": "WPC-DCS CPU board (Fliptronic II)", "drive_wire": "Black-Gray", "drive_connection": "J906-5"},
			spatial=located("switch.generic-117", "sensor", [(0.174289, 0.382255)], VPX_TABLE_SOURCE),
		)
	)

	for address in sorted(CUSTOM_SWITCH_LABELS.keys() | CUSTOM_SWITCH_UNUSED):
		unused = address in CUSTOM_SWITCH_UNUSED
		label = CUSTOM_SWITCH_LABELS.get(address) or f"Not Used Custom Position {address}"
		identifier = f"switch.custom-{address}"
		manual_alias = CUSTOM_SWITCH_MANUAL_ALIAS[address]
		notes = (
			f"Printed switch-matrix \"column 9\" position, silkscreened and printed as address {manual_alias}. "
			"PinMAME's CORE_CUSTSWCOL=CORE_STDSWCOLS=12 places sttngGameData's one declared custom switch column "
			f"(hw.swCol=1) at internal column 12, so CORE_CUSTSWNO(1,r) = 120+r publishes at public {address}, not "
			f"the printed {manual_alias}. sttng.c's own macro comment for this position is stale (from an older "
			"core.h numbering)."
		)
		physical: dict[str, Any] = {"notes": notes}
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": manual_alias},
			],
		}
		if unused:
			extra["physical"] = physical
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CORE_SOURCE), **extra))
			continue
		part_number = CUSTOM_SWITCH_PARTS[address]
		physical["part_number"] = part_number
		physical["switch_type"] = "microswitch"
		physical["notes"] += (
			" Printed with a single leaf-switch part number and no LED/photo-transistor pair on the switch-"
			"locations parts list, not shaded on the switch matrix, and the Gun Circuit Diagram (3-23) draws it as "
			"a plain switch-contact symbol -- an ordinary leaf switch, not an opto. PinMAME's inverted-switch mask "
			"array leaves this column (internal index 12) at its zero-filled default, agreeing with the physical "
			"construction: no polarity conflict."
		)
		extra["normally_closed"] = False
		extra["physical"] = physical
		extra["spatial"] = located(identifier, "sensor", CUSTOM_SWITCH_POSITIONS[address], VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE)
		extra["physical"]["notes"] += " " + CUSTOM_SWITCH_PROJECTIONS[address]
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra))

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
					"location": "WPC CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC CPU-board country/option configuration DIP bank. The retained transcription of this "
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
	for address in range(1, 57):
		fitted = address in SOLENOID_LABELS
		if not fitted and address not in NOT_FITTED_SOLENOID_LABELS and address not in CUSTOM_SOLENOID_LABELS:
			continue
		is_custom = address in CUSTOM_SOLENOID_LABELS
		label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS.get(address) or CUSTOM_SOLENOID_LABELS.get(address)
		identifier = output_id(label)
		wiring_data = SOLENOID_WIRING[address]
		if is_custom:
			kind = CUSTOM_SOLENOID_KIND[address]
		else:
			kind = "flasher" if 20 <= address <= 28 else "motor" if address in {17, 18} else "coil"
		physical: dict[str, Any] = {}
		part_number = wiring_data.get("part_number")
		if part_number and kind != "flasher":
			physical["part_number"] = part_number
		if address in SOLENOID_ASSEMBLIES:
			physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
		printed_type = wiring_data.get("printed_type", "")
		if is_custom:
			manual_addr = CUSTOM_SOLENOID_MANUAL_ALIAS[address]
			notes = (
				f"Printed 8-Driver Board item {manual_addr} ({printed_type}). PinMAME's hw.custSol=6 publishes at "
				f"CORE_CUSTSOLNO(n) = CORE_FIRSTCUSTSOL-1+n = 50+n, i.e. public {address}, not the printed "
				f"{manual_addr}; sttng.c's own macro comment for this position is stale. core_getSol's solNo<=44 "
				"branch returns constant 0 for GEN_WPCDCS before ever reaching hw.getSol, so sttng_getSol (which "
				"implements this output by reading WPC_EXTBOARD1) could only ever be invoked above public address "
				"50, structurally proving the arithmetic."
			)
		else:
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
		if kind == "flasher" and address in FLASHER_BULBS:
			bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
			physical["quantity"] = quantity
			notes += f" Printed flashlamp complement: {bulbs}."
			if playfield_emitters < quantity:
				notes += (
					" Only the playfield bulb(s) have a playfield placement; backbox bulbs are behind the "
					"translite and are deliberately not given a playfield coordinate."
				)
			if playfield_emitters > 1:
				notes += (
					f" The manual prints {playfield_emitters} playfield bulbs on this circuit, but the retained "
					"table represents them with a single combined Flasher render object, so this device carries "
					"one placement rather than one per printed bulb."
				)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
		if address == 7:
			notes += " Backbox-mounted knocker; voltage and drive connections are both on the backbox side of the harness (J130-8), unlike every other solenoid 1-18."
		if address in {33, 34}:
			notes += " Fliptronic upper-right flipper circuit; this game fits an upper-right flipper (FLIP_SOL(FLIP_UR))."
		if address in {35, 36}:
			notes += " Fliptronic upper-left flipper circuit with no coil printed; this game has no upper-left flipper."
		if address in {45, 46, 47, 48}:
			notes += " Printed table numbers these circuits 29-32; PinMAME's public lower-flipper addresses are 45-48, preserved as a manual.address alias."
		physical["notes"] = notes

		wiring: dict[str, Any] = {"board": "8-Driver Board" if is_custom else "WPC power driver board", "driver_transistor": wiring_data["driver_transistor"]}
		if "control_connection" in wiring_data:
			wiring["control_connection"] = wiring_data["control_connection"]
		if "power_connection" in wiring_data:
			wiring["power_connection"] = wiring_data["power_connection"]
		if "secondary_connection" in wiring_data:
			physical["notes"] += (
				f" Backbox flashlamp connections: {wiring_data['secondary_connection']} "
				f"(power {wiring_data.get('secondary_power', '')})."
			)
		if address in FLIPPER_DRIVE_WIRE:
			wiring["control_wire"] = FLIPPER_DRIVE_WIRE[address]
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if is_custom:
			aliases.append({"namespace": "manual.address", "value": CUSTOM_SOLENOID_MANUAL_ALIAS[address]})
		else:
			aliases.append({"namespace": "manual.address", "value": f"{address:02d}" if address <= 28 else str(address)})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if not fitted:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			availability = "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 7:
				extra["roles"] = ["cabinet.backbox"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in SOLENOID_PROJECTIONS:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
				physical["notes"] += " " + SOLENOID_PROJECTIONS[address]
			else:
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		refs = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS or is_custom:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))

	for address in sorted(VIRTUAL_SOLENOID_LABELS.keys()):
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Star Trek: The Next Generation playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Star Trek: The Next Generation playfield device.",
			31: "PinMAME's synthetic game-on state (GEN_ALLWPC J111/GameOn remap); this driver does not call wpc_set_fastflip_addr, so this channel is present only as PinMAME's generic WPC state bit.",
			32: "PinMAME reports this WPC state channel as always zero; this driver does not use it.",
			37: "Unused WPC-DCS address space; this generation has no integrated LPDC board, so core_getSol's 37-44 branch returns constant 0 here regardless of driver.",
			38: "Unused WPC-DCS address space; see 37.",
			39: "Unused WPC-DCS address space; see 37.",
			40: "Unused WPC-DCS address space; see 37.",
			41: "Unused WPC-DCS address space; see 37.",
			42: "Unused WPC-DCS address space; see 37.",
			43: "Unused WPC-DCS address space; see 37.",
			44: "Unused WPC-DCS address space; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-DCS hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary (CORE_FIRSTCUSTSOL=51).",
		}[address]
		roles = ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
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
	unresolved_addresses = {53, 85, 86}
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated buy-in/start button assembly, sharing its assembly part number with switch 11 or 13."
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"wiring": {
					"board": "WPC power driver board",
					"drive_wire": LAMP_COLUMN_WIRING[column][0],
					"drive_connection": LAMP_COLUMN_WIRING[column][1],
					"return_wire": LAMP_ROW_WIRING[row][0],
					"return_connection": LAMP_ROW_WIRING[row][1],
					"driver_transistor": f"{LAMP_COLUMN_WIRING[column][2]} column driver with {LAMP_ROW_WIRING[row][2]} row driver",
				},
			}
			if address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in unresolved_addresses:
				availability = "used"
				notes += (
					" No world-space Light object exists for this bulb in the retained extraction: the table "
					"models it as a colored Primitive mesh at local origin (0,0), parented to a transform this "
					"curator does not resolve, rather than a placeable Light object. Fabricating a coordinate "
					"would violate the never-invent-a-coordinate rule, so no spatial assertion is made for this "
					"device rather than guessing one; see reports/spatial for the named gap."
				)
				# No "spatial" key: the schema offers only "located" or "not_applicable", and neither is
				# honest here -- this is a real playfield device whose position is simply unresolved.
			elif address == 78:
				notes += (
					" The retained table renders this single manual-documented bulb as a five-waypoint animated "
					"\"Borg ship flying across the top of the playfield\" effect (Light objects l78a-e plus "
					"per-letter \"borg\" sub-segments) at (0.531972,0.12796), (0.353346,0.148471), "
					"(0.410071,0.147901), (0.665519,0.051425), and (0.797217,0.052922); those five points are the "
					"same physical device's own animation path, not five separate bulbs, so this device carries "
					"one placement at their centroid rather than five."
				)
				extra["spatial"] = located(identifier, "emitter", [(0.5316, 0.10935)], VPX_TABLE_SOURCE)
			else:
				availability = "used"
				if address in LAMP_RENDER_DOUBLE_ADDRESSES:
					notes += (
						f" The retained table stacks a second co-located Light object purely for brightness "
						f"(l{address}/l{address}b style pair, offset under one bulb diameter); the primary object "
						"is used and the duplicate is documented render doubling, matching the manual's single-"
						"bulb parts entry."
					)
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			physical["notes"] = notes
			extra["physical"] = physical
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
	11: [(0.247699, 0.569505)], 12: [(0.244714, 0.592099)], 13: [(0.396539, 0.6691)],
	14: [(0.338957, 0.621082)], 15: [(0.246018, 0.614935)], 16: [(0.501854, 0.683261)],
	17: [(0.500554, 0.873917)], 18: [(0.606092, 0.6691)],
	21: [(0.396539, 0.573064)], 22: [(0.501612, 0.558359)], 23: [(0.606686, 0.573665)],
	24: [(0.75816, 0.574017)], 25: [(0.758306, 0.596888)], 26: [(0.50133, 0.621345)],
	27: [(0.662487, 0.621983)], 28: [(0.756577, 0.617357)],
	31: [(0.663492, 0.065965)], 32: [(0.744909, 0.054504)], 33: [(0.827762, 0.043367)],
	34: [(0.398203, 0.789785)], 35: [(0.448749, 0.775031)], 36: [(0.500799, 0.760885)], 37: [(0.552848, 0.775791)],
	38: [(0.604297, 0.790545)],
	41: [(0.666816, 0.264865)], 42: [(0.908061, 0.312614)], 43: [(0.828054, 0.422359)],
	44: [(0.867009, 0.369329)], 45: [(0.804378, 0.386381)], 46: [(0.734315, 0.389384)],
	47: [(0.702991, 0.428804)], 48: [(0.687215, 0.358364)],
	51: [(0.207867, 0.760148)], 52: [(0.212486, 0.727145)],
	54: [(0.582213, 0.231767)], 55: [(0.573398, 0.292642)], 56: [(0.568018, 0.348724)],
	57: [(0.561251, 0.404122)], 58: [(0.555287, 0.454203)],
	61: [(0.192783, 0.418756)], 62: [(0.23173, 0.474199)], 63: [(0.269349, 0.525846)],
	64: [(0.495513, 0.218104)], 65: [(0.49971, 0.261439)], 66: [(0.505592, 0.291027)],
	67: [(0.3392, 0.445458)], 68: [(0.293577, 0.454244)],
	71: [(0.253317, 0.242783)], 72: [(0.327043, 0.267262)], 73: [(0.372902, 0.252606)],
	74: [(0.420511, 0.239404)], 75: [(0.391471, 0.30612)], 76: [(0.414045, 0.363809)],
	77: [(0.490826, 0.382953)],
	81: [(0.79729, 0.761175)], 82: [(0.787831, 0.727025)], 83: [(0.795653, 0.200381)],
	84: [(0.105653, 0.634123)],
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	definitions = {
		0: ("Shields G.I.", "J121-1", "Q18", "J121-7", "#44"),
		1: ("Insert G.I.", "J120-2", "Q10", "J120-8", "#555"),
		2: ("Insert G.I.", "J120-3", "Q14", "J120-9", "#555"),
		3: ("Playfield G.I.", "J121-5", "Q16", "J121-10", "#44"),
		4: ("Return Lane/Coin", "J121-6", "Q12", "J121-11", "#44"),
	}
	for address, (label, drive_connection, transistor, power_connection, bulb) in definitions.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination circuit {address + 1:02d} ({label}); printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC power driver board",
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
				" The manual prints no per-string bulb count and no dedicated General Illumination Location "
				"diagram exists in this manual, so the physical quantity and every emitter coordinate come from "
				"the retained table's GI emitter collection for this circuit (UpdateGI in the retained script). "
				"GI address 0 drives collection St1Shields; GI address 3 drives St4PFGI; GI address 4 drives "
				"St5ReLa."
			)
			if address == 0:
				notes += (
					" St1Shields contains 12 members: 6 ShieldGiBig Light objects (the physical bulbs) plus 6 "
					"ShieldGiFlasherS Flasher objects co-located within 0.002 normalized units of their ShieldGiBig "
					"counterpart -- excluded here as render-doubling glow-dome helpers, leaving 6 placements."
				)
			if address == 3:
				notes += (
					" St4PFGI contains 42 raw members. Most physical bulbs are modeled as a co-located \"Gis*\"+"
					"\"Gi*\" Light pair (nearest-neighbor deduplicated to 17 bulb positions), plus 2 \"lbumperr\" "
					"jet-bumper-cap Light objects sharing this circuit (18 placements total). Excluded: \"Flasher1"
					"-5\" (Flasher-typed objects at coordinates identical to already-counted solenoid-driven "
					"flasher devices, e.g. Flasher4 exactly matches solenoid 21's f121 position -- the same "
					"physical flasher bulb re-included in the GI dimming collection, not a distinct GI bulb), "
					"\"GiBig\" (a large ambient-wash Flasher helper with no corresponding manual bulb), and "
					"\"l1\"/\"l2\"/\"l1b\"/\"l2b\" (unidentified cosmetic lights matching no lamp-matrix or GI "
					"parts-list entry)."
				)
			if address == 4:
				notes += (
					" St5ReLa contains 31 raw members, nearest-neighbor deduplicated the same way to 16 bulb "
					"positions (14 Gis/Gi pairs plus 2 lbumperr jet-bumper-cap positions). Two further raw members "
					"(Gi9, Gi11) sit at coordinates identical to two St4PFGI members and are excluded here as a "
					"shared-object anomaly -- their paired \"Gis*\" sibling exists only in St4PFGI, so that "
					"circuit is recorded as their physical home rather than double-placing the same bulb under "
					"both GI addresses."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite: the retained script's UpdateGI Case 1/2 "
				"handlers only fade opacity on VR-backglass-room helper collections (St2GI1/St3GI2, named "
				"\"VRBGGI*\"/\"VRBGGIarea*\"), never a playfield emitter collection, confirming this circuit has "
				"no playfield bulb."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
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
			"mechanism.left-gun",
			"Left rotating gun/cannon",
			"motorized",
			[output_id("Left Gun Kicker"), output_id("Left Gun Popper"), output_id("Left Gun Motor")],
			["switch.matrix-32", "switch.matrix-36", "switch.matrix-38", "switch.custom-122", "switch.custom-127"],
			"A ball entering the left underplayfield subway trips opto 32 (Under Left Gun Sw. 2), advances to opto "
			"36 (Under Left Gun Sw. 1) where solenoid 3 (Left Gun Popper) kicks it up into the gun barrel, and it "
			"comes to rest on opto 38 (Left Gun Shooter, \"ball loaded\") inside the barrel. Solenoid 17 (Left Gun "
			"Motor) continuously rotates the entire kicker/barrel/dome assembly (retained script primitive "
			"CannonBaseL) back and forth through roughly -19 to +64 degrees around a pivot; the motor does not "
			"itself actuate a discrete switch -- the two position switches sense the assembly's resulting "
			"mechanical angle. Custom switch 127 (Left Gun Home) is asserted only near the home end of the sweep "
			"(-20 to -17 degrees) and custom switch 122 (Left Gun Mark) is asserted over a wider band (-20 to +9 "
			"degrees) that the retained script also uses to pick a lower launch force; PinMAME's own internal "
			"ball-tracking simulator (sttng.c, used only for its built-in keyboard-driven playfield visualization, "
			"not by a VPX table) models the same two-sensor homing scheme with step constants GUN_HOME=8*2=16, "
			"GUN_MARK=8*7=56 out of a GUN_END=8*20=160-step full sweep before reversing direction -- a different "
			"unit system (steps vs. degrees) describing the same physical homing behavior. When solenoid 1 (Left "
			"Gun Kicker) fires, the ball loaded in the barrel launches along the gun's current aim angle and opto "
			"38 clears.",
			[
				("entry", "Ball entering the left subway", ["switch.matrix-32"], "First opto in the underplayfield path."),
				("popper", "Ball at the left gun popper", ["switch.matrix-36"], "Opto that gates solenoid 3's kick into the barrel."),
				("loaded", "Ball loaded in the left gun barrel", ["switch.matrix-38"], "Opto cleared when solenoid 1 launches the ball."),
				("home", "Left gun at home position", ["switch.custom-127"], "Motor rotation -20 to -17 degrees."),
				("mark", "Left gun within the mark band", ["switch.custom-122"], "Motor rotation -20 to +9 degrees; also gates launch force."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17081-L",
		),
		mechanism(
			"mechanism.right-gun",
			"Right rotating gun/cannon",
			"motorized",
			[output_id("Right Gun Kicker"), output_id("Right Gun Popper"), output_id("Right Gun Motor")],
			["switch.matrix-33", "switch.matrix-37", "switch.matrix-34", "switch.custom-125", "switch.custom-126"],
			"Mirror of the left gun (mechanism.left-gun): opto 33 (Under Right Gun Sw. 2) then opto 37 (Under Right "
			"Gun Sw. 1, gates solenoid 4's kick), ball rests on opto 34 (Right Gun Shooter) in the barrel, solenoid "
			"18 (Right Gun Motor) rotates the assembly (retained script primitive CannonBaseR) and solenoid 2 "
			"(Right Gun Kicker) launches it. Custom switch 125 (Right Gun Home) and custom switch 126 (Right Gun "
			"Mark) sense the assembly's rotation exactly as 127/122 do on the left side; the motor never directly "
			"actuates either switch.",
			[
				("entry", "Ball entering the right subway", ["switch.matrix-33"], "First opto in the underplayfield path."),
				("popper", "Ball at the right gun popper", ["switch.matrix-37"], "Opto that gates solenoid 4's kick into the barrel."),
				("loaded", "Ball loaded in the right gun barrel", ["switch.matrix-34"], "Opto cleared when solenoid 2 launches the ball."),
				("home", "Right gun at home position", ["switch.custom-125"], "Motor rotation -20 to -17 degrees."),
				("mark", "Right gun within the mark band", ["switch.custom-126"], "Motor rotation -20 to +9 degrees; also gates launch force."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17081-R",
		),
		mechanism(
			"mechanism.left-lock-queue",
			"Left lock four-ball queue and popper",
			"kicker",
			[output_id("Left Popper")],
			["switch.matrix-43", "switch.matrix-42", "switch.matrix-35", "switch.matrix-41"],
			"A separate underplayfield path from the left gun subway: balls queue through four opto positions in "
			"order (43 Under Left Lock Sw. 4, farthest from the popper, then 42 Sw. 3, then 35 Sw. 2, then 41 Sw. "
			"1, nearest the popper). Solenoid 5 (Left Popper) kicks the ball resting on opto 41 back out to the "
			"right inlane. This is a straight ball-holding queue, not the Borg ball lock (mechanism.borg-lock).",
			[
				("queue-4", "Fourth queue position", ["switch.matrix-43"], "Farthest from the popper."),
				("queue-3", "Third queue position", ["switch.matrix-42"], "Middle of the four-ball queue."),
				("queue-2", "Second queue position", ["switch.matrix-35"], "Second-nearest the popper."),
				("queue-1", "Popper position", ["switch.matrix-41"], "Kicked out by solenoid 5."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17049",
		),
		mechanism(
			"mechanism.borg-lock",
			"Borg multiball lock",
			"kicker",
			[output_id("Borg Kicker")],
			["switch.matrix-48", "switch.matrix-31"],
			"A ball entering the Borg hole passes opto 48 (Borg Entry) and comes to rest at opto 31 (Borg Lock), "
			"an opto interrupter mounted on the Borg Bracket Assembly (A-17219) rather than a discrete playfield "
			"trigger object -- the retained script models this position purely as a one-ball cvpmBallStack "
			"(BorgLock.InitSw 0,31,0,0,0,0,0,0). Solenoid 16 (Borg Kicker) ejects the locked ball back to play, "
			"typically as part of Borg multiball.",
			[
				("entry", "Ball entering the Borg hole", ["switch.matrix-48"], "Opto at the hole mouth."),
				("locked", "Ball held at the Borg lock", ["switch.matrix-31"], "Opto at the kicker; ejected by solenoid 16."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17219",
		),
		mechanism(
			"mechanism.underplayfield-diverters",
			"Underplayfield hole diverters",
			"gate",
			[output_id("Top Divertor"), output_id("Under Divertor Top"), output_id("Under Divertor Bottom")],
			["switch.matrix-45", "switch.matrix-46", "switch.matrix-47"],
			"Three balls entering Top Hole (opto 45), Left Hole (opto 46), or Center/Borg Hole (opto 47) share an "
			"underplayfield routing maze. Solenoid 15 (Top Divertor) raises a flap (retained script object "
			"\"diverter\") that routes a completed left-ramp shot either onward or into the Borg Entry path. The "
			"two custom-board diverters -- solenoid 51 (Under Divertor Top, retained script object "
			"\"DiverterFRG\") and solenoid 52 (Under Divertor Bottom, \"DiverterFLG\") -- gate whether a ball from "
			"these holes is routed to the right gun subway, the left gun subway, or the left popper queue. PinMAME's "
			"own sttng_handleMech buffers each diverter's real position from solenoid on/off transitions with a "
			"debounce counter (CHECK_SOL=50 checks) rather than a discrete return switch, because none of these "
			"three diverters has its own position sensor -- only the coil state is known.",
			[
				("top-hole", "Ball in the top hole", ["switch.matrix-45"], "Feeds the diverter maze."),
				("left-hole", "Ball in the left hole", ["switch.matrix-46"], "Feeds the diverter maze."),
				("center-hole", "Ball in the center/Borg hole", ["switch.matrix-47"], "Feeds the diverter maze."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16763",
		),
		mechanism(
			"mechanism.top-drop-target",
			"Top drop target",
			"drop_target_bank",
			[output_id("Top Drop Up"), output_id("Top Drop Down")],
			["switch.matrix-57"],
			"A single drop target (retained script class TopDrop, cvpmDropTarget bound to sw57) is raised by "
			"solenoid 53 (Top Drop Up) and lowered by solenoid 54 (Top Drop Down), both on the 8-Driver Board. When "
			"raised, a ball striking it scores and it drops; when down, a ball rolls over it into the Top Hole "
			"instead. PinMAME's own internal simulator independently confirms the switch asserts only while the "
			"target is down (core_setSw(swTDropTarget, locals.TdroptargetPos==DT_DOWN)).",
			[("target", "Top drop target", ["switch.matrix-57"], "Asserted while the target is in its down/dropped position.")],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14615",
		),
		mechanism(
			"mechanism.bank-standups",
			"Left and right 3-bank standup targets",
			"other",
			[],
			["switch.matrix-51", "switch.matrix-52", "switch.matrix-53", "switch.matrix-54", "switch.matrix-55", "switch.matrix-56"],
			"Despite the printed \"Bank\" naming, these six positions (51-53 left, 54-56 right) are fixed standup "
			"targets (retained table HitTarget objects, not a drop-target Wall with isDropped state) with no reset "
			"solenoid printed on the solenoid/flasher table or registered in the retained script's SolCallback "
			"table -- there is no dropping/resetting mechanism, only score switches.",
			[
				("left-top", "Left bank top", ["switch.matrix-51"], "Topmost standup of the left 3-bank."),
				("left-middle", "Left bank middle", ["switch.matrix-52"], "Middle standup of the left 3-bank."),
				("left-bottom", "Left bank bottom", ["switch.matrix-53"], "Bottommost standup of the left 3-bank."),
				("right-top", "Right bank top", ["switch.matrix-54"], "Topmost standup of the right 3-bank."),
				("right-middle", "Right bank middle", ["switch.matrix-55"], "Middle standup of the right 3-bank."),
				("right-bottom", "Right bank bottom", ["switch.matrix-56"], "Bottommost standup of the right 3-bank."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14691-6",
		),
		mechanism(
			"mechanism.trough",
			"Six-ball trough and ball release",
			"kicker",
			[output_id("Trough")],
			["switch.matrix-61", "switch.matrix-62", "switch.matrix-63", "switch.matrix-64", "switch.matrix-65", "switch.matrix-66", "switch.matrix-67"],
			"The retained script models the trough purely as a cvpmBallStack ball counter (bsTrough.InitSw 0,66,"
			"65,64,63,62,61,0), with no discrete playfield trigger object per position -- switches 61-66 (Trough "
			"L.R. 1-6, all opto) and 67 (Trough Up, opto) exist only as PinMAME public addresses the class asserts "
			"from its own internal ball count. The manual's \"7 Ball Trough Photo Transistor/LED PCB Assembly\" "
			"board name reflects seven physical opto stations (six ball rest positions plus the eject/up sensor); "
			"solenoid 11 (Trough) ejects the ball at position 1 toward the shooter lane, pulsing opto 67 in the "
			"same event (retained script SolRelease). The game carries six balls total: three start in the trough "
			"and three more start pre-placed in the gun subways/lock queue at boot.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-61"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-62"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-63"], "Third trough position."),
				("ball-4", "Trough Ball 4", ["switch.matrix-64"], "Fourth trough position."),
				("ball-5", "Trough Ball 5", ["switch.matrix-65"], "Fifth trough position."),
				("ball-6", "Trough Ball 6 (drain entrance)", ["switch.matrix-66"], "Drain entrance and sixth trough position."),
				("up", "Trough eject/up sensor", ["switch.matrix-67"], "Pulsed as the ejected ball leaves toward the shooter lane."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16765",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Plunger")],
			["switch.matrix-68"],
			"Star Trek: The Next Generation has no manual plunger. The ball ejected from the trough rests on "
			"shooter-lane switch 68 (a plain leaf switch, the sole non-opto position in switch column 6) and "
			"solenoid 6 (Plunger, A-16757 Catapult Assembly) auto-launches it.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-68"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16757",
		),
		mechanism(
			"mechanism.kickback",
			"Left outlane kickback",
			"kicker",
			[output_id("Kickback")],
			["switch.matrix-15"],
			"When lit, a ball draining down the left outlane (switch 15) conditionally fires solenoid 8 (Kickback) "
			"to return it to the playfield instead of draining; PinMAME's own internal simulator independently "
			"models this exact conditional (the Left Outlane state's altstate is sKickBack -> stFree). There is no "
			"separate kickback-position switch.",
			[("outlane", "Ball in the left outlane", ["switch.matrix-15"], "Fires solenoid 8 conditionally.")],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17234",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-71", "switch.matrix-72", "switch.matrix-73"],
			"Three A-9415-2 jet bumpers. The retained script's LeftJetBumper_hit, RightJetBumper_hit, and "
			"BottomJetBumper_hit handlers pulse switches 71, 72, and 73 and fire solenoids 12, 13, and 14 "
			"respectively. Each bumper's cap is GI-lit rather than lamp-matrix-lit (see gi.string-4/gi.string-5 "
			"lbumperr placements) -- there is no lamp-matrix address for any jet bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-71"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-72"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-73"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-74", "switch.matrix-75"],
			"Two A-17418 slingshot switches (leaf, not opto). Solenoid 9 (Left Slingshot) fires from switch 75 "
			"(Left Sling) and solenoid 10 (Right Slingshot) fires from switch 74 (Right Sling) -- the printed "
			"Left/Right function names and the printed switch addresses cross to opposite sides of the matrix row, "
			"confirmed by the retained table's SlingShotLeft/SlingShotRight wall objects sitting on their "
			"named side (x=0.300 left, x=0.703 right).",
			[
				("left", "Left slingshot", ["switch.matrix-75"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-74"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_TABLE_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17418",
		),
		mechanism(
			"mechanism.flippers",
			"Flipper set (lower pair plus upper right)",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
				output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114", "switch.generic-115", "switch.generic-116"],
			"Three FL-11629 flippers on Fliptronic circuits: two lower (A-15205-L-2 left, A-15205-R-2 right) and "
			"one upper right (A-15205-R-2). Each has a separate power and hold winding; the ROM energizes the power "
			"winding on the cabinet button opto, then drops to the hold winding once the end-of-stroke leaf switch "
			"closes. Const UseSolenoids=2 (fast flips) is set in the retained script, so the ROM drives the coils "
			"directly. There is no upper-left flipper: printed solenoid circuits 35/36 and Fliptronic positions "
			"117 (repurposed as a Spinner) and 118 (not fitted) confirm it.",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
				("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button opto 116 and end-of-stroke switch 115."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 (lower right, upper right) with A-15205-L-2 (lower left)",
		),
		mechanism(
			"mechanism.eddy-return-lanes",
			"Left and right return-lane eddy sensors",
			"other",
			[],
			["switch.matrix-16", "switch.matrix-17"],
			"Two A-16922 Proximity Sensor II PCB assemblies (TDA0161 eddy-current IC) with A-17064 Eddy Sensor "
			"coils detect a ball passing the left/right return lane without a mechanical contact switch. The "
			"Section 3 schematic (3-20/3-21) wires each board's eddy coil directly and feeds the switch matrix at "
			"column 1, rows 6/7 -- public switches 16 and 17.",
			[],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16922",
		),
		mechanism(
			"mechanism.spinner",
			"Spinner",
			"other",
			[],
			["switch.generic-117"],
			"A free-spinning target wired on the Fliptronic F7 position rather than the switch matrix. The "
			"retained script's sw117spinner_Spin handler pulses switch 117 on every rotation.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="5647-12693-11",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough"),
			"destination": "switch.matrix-67",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
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
			"id": "williams.star-trek-the-next-generation.1993",
			"name": "Star Trek: The Next Generation",
			"manufacturer": "Williams",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 2357,
			"playfield": {"width": 1093, "height": 2162, "units": "vpx"},
			"opdb_id": "GR6d8-M1rZd",
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
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
			"platform": "pinmame.wpc-dcs",
			"hardware_generation": "0x10",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/star-trek-the-next-generation-1993.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Star Trek: The Next Generation device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
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
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	projections = []
	for address, reason in sorted(SWITCH_PROJECTIONS.items()):
		projections.append({"group": "pinmame.input.switch", "address": address, "reason": reason})
	for address, reason in sorted(CUSTOM_SWITCH_PROJECTIONS.items()):
		projections.append({"group": "pinmame.input.switch", "address": address, "reason": reason})
	for address, reason in sorted(SOLENOID_PROJECTIONS.items()):
		projections.append({"group": "pinmame.output.solenoid", "address": address, "reason": reason})
	projections.append({"group": "pinmame.output.lamp", "address": 78, "reason": "Centroid of the five l78a-e \"Borg Ship\" flight-path animation waypoints (same single physical bulb's own multi-primitive render effect, not a centroid of other devices)."})
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"Lamps 53 (Advance in Rank), 85 (Borg Lock), and 86 (Borg Jackpot) have no world-space Light "
			"object in the retained extraction -- only a colored Primitive mesh at local origin "
			"(0,0,0), parented to a transform this curator does not resolve. No coordinate is "
			"asserted for these three positions rather than inventing one from an unrelated anchor.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 1093.0, "bottom": 2162.0},
			"x": "x/1093; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/star-trek-the-next-generation-1993/extracted-vpxtool.manifest.json",
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
		"unresolved_output_bindings": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": projections,
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.star-trek-the-next-generation.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/star-trek-the-next-generation-1993/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"ShieldGiFlasherS1-6 (co-located Flasher render doubles of ShieldGiBig1-6, GI address 0)",
			"Flasher1-5 and GiBig within St4PFGI/St5ReLa (already-counted flasher devices and a synthetic ambient-wash helper swept into the GI dimming collection)",
			"l1, l2, l1b, l2b within St4PFGI (unidentified cosmetic lights matching no lamp-matrix or GI parts-list entry)",
			"ShieldGiFlasherS/f123a-style co-located Flasher duplicates of already-placed solenoid-driven flashers",
			"VRBGGI*/VRBGGIarea* VR-backglass-room helper objects (GI addresses 1/2; confirm those circuits are backbox-only)",
		],
		"unresolved": [
			{"group": "pinmame.output.lamp", "address": 53, "reason": "No world-space Light object; only a local-origin Primitive with an unresolved parent transform."},
			{"group": "pinmame.output.lamp", "address": 85, "reason": "No world-space Light object; only a local-origin Primitive with an unresolved parent transform."},
			{"group": "pinmame.output.lamp", "address": 86, "reason": "No world-space Light object; only a local-origin Primitive with an unresolved parent transform."},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Star Trek: The Next Generation (Williams, 1993) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete except three "
		"lamp positions with no resolvable world-space coordinate; the physical machine record stays "
		"`partial` at `machines/partial/williams/star-trek-the-next-generation-1993.json` for exactly "
		"that reason. See the promotion decision below.",
		"",
		"The matching source is the retained known-working "
		"`Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script "
		f"at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. "
		f"Exact playfield bounds are `{TABLE_BOUNDS}` (a wide-body \"Superpin\" table like Indiana "
		"Jones), and every canonical coordinate is x/1093 and y/2162 rounded to at most six fractional "
		"places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations manual is "
		"the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller topology; "
		"the retained table supplies geometry.",
		"- The manual's own switch-matrix and custom-column silkscreen prints \"column 9\" as addresses 91-98, and "
		"the custom-solenoid board prints items 37-42; neither is the PinMAME public address. "
		"CORE_CUSTSWCOL/CORE_FIRSTCUSTSOL arithmetic places them at public 121-128 and 51-56 respectively, and the "
		"retained known-working script's own Controller.Switch(122/125/126/127) assignments and "
		"SolCallBack(51-54)/SolModCallBack(55/56) registrations confirm the arithmetic directly at runtime.",
		"- The switch-matrix opto shading (2-42) and PinMAME's sttngGameData inverted-switch mask agree on every "
		"single opto address (columns 3, 4, and 6 rows 1-7) -- zero polarity conflicts, unlike Monster Bash or "
		"Indiana Jones.",
		"- Several switches have no dedicated playfield trigger object because the retained script sets their "
		"public state directly from a ball-stack class's internal counter (trough, Borg lock) or from a gun "
		"assembly's continuous rotation angle (gun Home/Mark) rather than from a Hit/Trigger event. Those "
		"addresses are explicit documented projections onto the real table object that carries the underlying "
		"mechanism state; the projection notes are explicit that a motor's continuous rotation, not a solenoid "
		"pulse, drives the sensed position.",
		"- GI addresses 1 and 2 (\"Insert G.I.\") drive only VR-backglass-room helper objects "
		"(VRBGGI*/VRBGGIarea*) in the retained table's own UpdateGI dispatch, confirming they are backbox-only "
		"circuits with no playfield bulb, matching the manual's own \"Insert\" (non-playfield) wording.",
		"- GI addresses 0, 3, and 4 use the retained table's St1Shields/St4PFGI/St5ReLa emitter collections, "
		"nearest-neighbor deduplicated to exclude co-located Light/Flasher render-double pairs and already-counted "
		"solenoid-driven flasher devices incidentally swept into the ambient-dimming collection.",
		"- Solenoid 7 (Knocker) is a backbox device (voltage and drive connections both on the backbox side of the "
		"harness) and takes a controlled `cabinet_or_service` record.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group'].rsplit('.', 1)[-1].capitalize()} {entry['address']}: {entry['reason']}")
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
	lines.append(f"- Unresolved output placements: {len(report['unresolved_output_bindings'])}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No unresolved semantic question, address-enumeration gap, or polarity conflict remains anywhere in this "
		"definition, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. `conflicts` is empty and `coverage.dimensions.physical_wiring = \"validated\"`. However, "
		"three playfield lamps (53 Advance in Rank, 85 Borg Lock, 86 Borg Jackpot) have no resolvable world-space "
		"coordinate in the retained extraction -- only a colored Primitive mesh at local origin, parented to a "
		"transform this curator does not resolve. Inventing a coordinate for them would violate the project's "
		"never-invent-a-coordinate rule, so the record stays `partial` with "
		"`coverage.missing = [\"spatial_placement\"]` until a further extraction pass resolves those three "
		"primitives' world transforms (or a photograph/service note independently fixes their playfield location).",
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
		raise RuntimeError(f"Stale Star Trek: The Next Generation author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Star Trek: The Next Generation definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Star Trek: The Next Generation seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Star Trek: The Next Generation definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Star Trek: The Next Generation seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Star Trek: The Next Generation spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Star Trek: The Next Generation spatial review drifted from its deterministic curator: {markdown_path}")
	print("Star Trek: The Next Generation definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Star Trek: The Next Generation extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Star Trek: The Next Generation retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
