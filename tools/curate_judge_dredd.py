"""Curate the physical Bally Judge Dredd (1993) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed
label, wiring detail, and normalized coordinate as a literal, so regeneration
reproduces the canonical artifact byte-for-byte without reading the external
evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only
path that writes the canonical definition and its pinned seed.

Judge Dredd is a wide-body "Superpin": the retained table's own playfield bounds
are ``left=0 top=0 right=1093 bottom=2162``, so every normalized coordinate here
is ``x/1093`` and ``y/2162``. Using the 952 divisor that standard-width WPC games
take would stretch every x by about 15 percent.
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
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/judge-dredd-1993.json"
PARTIAL_PATH = ROOT / "machines/partial/bally/judge-dredd-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/judge-dredd-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/judge-dredd-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/judge-dredd-1993.md"
KNOWLEDGE_PATH = "knowledge/bally/judge-dredd-1993.md"

MACHINE_ID = "bally.judge-dredd.1993"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-dcs"
MANUAL_SOURCE = "manual.bally.judge-dredd.1993"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.judge-dredd.1993"
VPX_TABLE_SOURCE = "vpx-table.jd-vpw-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.jd-vpw-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.jd-vpw-1-1"

TABLE_SHA256 = "61f6844d947cc788f81a9ed91e108bd800bd3172abd125ad2ecfb51f6d55be06"
SCRIPT_SHA256 = "817427aed72dc68a5e96a6a50614e8ab822d9d6d98c6033757ef245eda5b6d32"
SCRIPT_BYTES = 191673
MANUAL_SHA256 = "0883aa81befaed928d6761e32b937a1c61417ba834d8f47ae6bc5541b2424fec"
MANUAL_TRANSCRIPTION_SHA256 = "78b62d0f8a3a2b1b4a2b1e29bdcbd0aa2e3b6c76eb5a2c19e6a1cd9a4dfd8e01"

EXTRACTION_RELATIVE_PATH = Path("bally/judge-dredd-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/judge-dredd-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "8eaa44e94e08384f9fd0f77b1d237539d73f2c79bb716fa51eb78197268d81d2"
EXTRACTION_FILE_COUNT = 1840
EXTRACTION_TOTAL_BYTES = 419225172

PLAYFIELD_WIDTH = 1093.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=1093 bottom=2162"

# --- Driver inventory (catalog/pinmame.json, the twelve-driver jd_l7 clone tree).
DRIVER_IDS = (
	"jd_l1", "jd_d1", "jd_l1at", "jd_l1d", "jd_l4", "jd_d4",
	"jd_l5", "jd_d5", "jd_l6", "jd_d6", "jd_l7", "jd_d7",
)
DRIVER_COMPATIBILITY = {
	"jd_l1": (
		"identical",
		"Bally L-1 game ROM. This is the driver the retained known-working VPW table binds to "
		"(cGameName = \"jd_l1\"), and its own script comment records why: L-1 still runs the Deadworld "
		"ball lock as originally designed, physically diverting balls onto the rotating globe, while "
		"later production code virtualises the lock. Same physical machine and the same I/O inventory.",
	),
	"jd_d1": ("identical", "L-1 with the LED ghost fix; a display-driver change only."),
	"jd_l1at": (
		"identical",
		"Community MOD of L-1 for the aftermarket Deadworld hardware modification, per pinned "
		"driver.c's own comment. It runs on the physical machine and changes no controller address.",
	),
	"jd_l1d": ("identical", "Community MOD of jd_l1at by KoP, per pinned driver.c's own comment."),
	"jd_l4": ("identical", "Bally L-4 game ROM; a later firmware revision of the same physical machine."),
	"jd_d4": ("identical", "L-4 with the LED ghost fix; a display-driver change only."),
	"jd_l5": ("identical", "Bally L-5 game ROM; a later firmware revision of the same physical machine."),
	"jd_d5": ("identical", "L-5 with the LED ghost fix; a display-driver change only."),
	"jd_l6": ("identical", "Bally L-6 game ROM; a later firmware revision of the same physical machine."),
	"jd_d6": ("identical", "L-6 with the LED ghost fix; a display-driver change only."),
	"jd_l7": (
		"identical",
		"Bally L-7 game ROM, the pinned catalog's clone-tree parent and the last factory revision. "
		"Judge Dredd's Deadworld ball lock was deactivated for production, so L-7 locks balls "
		"virtually rather than diverting them onto the globe; the playfield hardware is unchanged.",
	),
	"jd_d7": ("identical", "L-7 with the LED ghost fix; a display-driver change only."),
}

# --- Printed switch matrix (manual printed 2-42) and switch locations (2-42 lower, 2-43).
# Labels are taken from the Switch Locations parts list, which is the authoritative label source;
# where the Switch Matrix page prints something different it is recorded in the device notes.
SWITCH_LABELS = {
	11: "Left Fire Button", 12: "Right Fire Button", 13: "Credit (Start)", 14: "Plumb Bob Tilt",
	15: "Left Shoot Lane", 16: "Left Outlane", 17: "Left Return Lane", 18: "3-Bank Targets",
	21: "Slam Tilt", 22: "Front Door Closed", 23: "Ticket Dispenser", 24: "Always Closed",
	25: "Top Right Post", 26: "Captive Ball 1", 27: "Mystery",
	31: "Buy-In (Extra Ball)", 33: "Left Rollover", 34: "Inside Right Return",
	35: "Top Center Rollover", 36: "Left Score Target", 37: "Subway Enter 1", 38: "Subway Enter 2",
	41: "Right Ball Shooter", 42: "Right Outlane", 43: "Outside Right Return", 44: "Super Game",
	51: "Left Sling", 52: "Right Sling", 53: "Captive Ball 2",
	54: "Drop Target \"J\"", 55: "Drop Target \"U\"", 56: "Drop Target \"D\"",
	57: "Drop Target \"G\"", 58: "Drop Target \"E\"",
	61: "Globe Position #1", 62: "Crane Exit", 63: "Left Ramp To Lock", 64: "Left Ramp Exit",
	66: "Center Ramp Exit", 67: "Left Ramp Enter", 68: "Captive Ball 3",
	71: "Magnet Over Ring", 72: "Top Right Opto", 73: "Left Popper", 74: "Right Popper",
	75: "Top Ramp Exit", 76: "Right Ramp Exit", 77: "Globe Position #2",
	81: "Trough 1", 82: "Trough 2", 83: "Trough 3", 84: "Trough 4", 85: "Trough 5",
	86: "Trough 6", 87: "Top Trough",
}
# Printed "Not Used" on both the switch matrix (2-42) and the switch-locations parts list (2-43),
# with a blank switch part number, and with no callout in the location diagram either.
UNUSED_MATRIX_ADDRESSES = (45, 46, 47, 48, 78, 88)
# Printed "Not Used" with a blank part number, but still drawn as a callout in this manual's own
# playfield location diagram AND driven by the retained known-working script. See
# conflict.l1-era-switch-fitment.
UNRESOLVED_MATRIX_ADDRESSES = {
	28: (
		"Crane Assembly Switch Position 28 (Fitment Unresolved)",
		"The location diagram on printed 2-43 draws a 28 callout on the crane / Magnet Over Ring "
		"assembly beside switch 71, and the retained known-working script asserts public switch 28 "
		"for as long as the Globe Magnet holds a ball (Sub CraneMag), but the parts list on the same "
		"page prints item 28 with a blank part number and \"Not Used\".",
	),
	32: (
		"Left Ramp Entrance Opto Position 32 (Fitment Unresolved)",
		"The location diagram on printed 2-43 draws a 32 callout on the plastic orbit ramp where it "
		"passes the globe, pinned PinMAME's jdGameData inverted-switch mask normalizes this address "
		"(column 3 bit 1) as though an opto were fitted, and the retained known-working script fires "
		"public 32 from its own ramp-entrance trigger, but the parts list prints item 32 with a blank "
		"part number and \"Not Used\".",
	),
	65: (
		"Right Ramp Entrance Position 65 (Fitment Unresolved)",
		"The location diagram on printed 2-43 draws a 65 callout on the right-hand ramp and the "
		"retained known-working script pulses public 65 from a trigger there, its own comment reading "
		"'Opto Right Ramp Entrace (Not used?)', but the parts list prints item 65 with a blank part "
		"number and \"Not Used\".",
	),
}
# Every cell the printed switch matrix (2-42) fills with the "Opto, Typically Closed" halftone,
# swept mechanically over all 64 cells at 600 dpi; see evidence/excerpts/.../switch-matrix.md.
MATRIX_SHADED_OPTO_SWITCHES = (61, 62, 63, 64, 66, 67, 71, 72, 73, 74, 75, 76, 77)
# Every address whose Switch Locations row (2-43) discloses a two-part LED + phototransistor
# construction, swept over the whole list.
PARTS_LIST_OPTO_SWITCHES = (62, 63, 64, 66, 67, 71, 72, 73, 74, 75, 76, 81, 82, 83, 84, 85, 86, 87)
# Union of the two cues: the addresses this definition records as physically opto-constructed.
OPTO_SWITCHES = tuple(sorted(set(MATRIX_SHADED_OPTO_SWITCHES) | set(PARTS_LIST_OPTO_SWITCHES)))
# jdGameData's inverted-switch mask {0x00,0x00,0x00,0x02,0x00,0xf8,0x6e,0x3e,0x7f,0x00,0x00,0x00},
# indexed by matrix column with bit = row - 1, recomputed in code rather than read off by hand.
PINMAME_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x02, 0x00, 0xf8, 0x6e, 0x3e, 0x7f, 0x00, 0x00, 0x00)


def pinmame_normalized_switches() -> tuple[int, ...]:
	"""Public matrix addresses PinMAME already inverts, derived from the mask rather than listed."""
	return tuple(
		column * 10 + row
		for column, value in enumerate(PINMAME_INVERTED_SWITCH_MASK)
		if column >= 1
		for row in range(1, 9)
		if (value >> (row - 1)) & 1
	)


PINMAME_NORMALIZED_SWITCHES = pinmame_normalized_switches()

SWITCH_TYPES = {
	11: "button", 12: "button", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch",
	17: "microswitch", 18: "microswitch", 21: "leaf", 22: "microswitch", 23: "other",
	24: "other", 25: "microswitch", 26: "microswitch", 27: "microswitch",
	31: "button", 33: "microswitch", 34: "microswitch", 35: "microswitch", 36: "microswitch",
	37: "microswitch", 38: "microswitch", 41: "microswitch", 42: "microswitch",
	43: "microswitch", 44: "button", 51: "leaf", 52: "leaf", 53: "microswitch",
	54: "unknown", 55: "unknown", 56: "unknown", 57: "unknown", 58: "unknown",
	68: "microswitch",
}

SWITCH_PARTS = {
	11: "20-9846-1", 12: "20-9846-1", 13: "20-9663-1", 14: "A-15361",
	15: "5647-12693-19", 16: "5647-12693-19", 17: "5647-12693-19", 18: "A-14227-15",
	21: "SW-1A-117", 22: "5643-09288-00", 24: "5643-09288-00",
	25: "A-16910-15", 26: "5647-12693-19", 27: "A-14227-15",
	31: "20-9663-9", 33: "5647-12693-19", 34: "5647-12693-19", 35: "5647-12693-19",
	36: "A-16910-15", 37: "5647-12693-13", 38: "5647-12693-13",
	41: "5647-12693-19", 42: "5647-12693-19", 43: "5647-12693-19", 44: "20-9663-13",
	51: "SW-1A-114 kick with SW-1A-120 score", 52: "SW-1A-114 kick with SW-1A-120 score",
	53: "5647-12693-19",
	54: "A-16486", 55: "A-16486", 56: "A-16486", 57: "A-16486", 58: "A-16486",
	61: "A-16598", 77: "A-16598", 68: "A-14227-15",
	62: "A-14231 LED with A-14232 phototransistor", 63: "A-14231 LED with A-14232 phototransistor",
	64: "A-14231 LED with A-14232 phototransistor", 66: "A-14231 LED with A-14232 phototransistor",
	67: "A-14231 LED with A-14232 phototransistor", 71: "A-14231 LED with A-14232 phototransistor",
	72: "A-14231 LED with A-14232 phototransistor", 73: "A-14231 LED with A-14232 phototransistor",
	74: "A-14231 LED with A-14232 phototransistor", 75: "A-14231 LED with A-14232 phototransistor",
	76: "A-14231 LED with A-14232 phototransistor",
	81: "A-16926 phototransistor with A-16927 LED", 82: "A-16926 phototransistor with A-16927 LED",
	83: "A-16926 phototransistor with A-16927 LED", 84: "A-16926 phototransistor with A-16927 LED",
	85: "A-16926 phototransistor with A-16927 LED", 86: "A-16926 phototransistor with A-16927 LED",
	87: "A-16926 phototransistor with A-16927 LED",
}
# Rows the Switch Locations parts list marks *Not Shown or †Located Under Playfield.
SWITCH_NOT_SHOWN = (14, 21, 22, 23, 24, 61, 77)
SWITCH_UNDER_PLAYFIELD = (37, 38, 71)
# Labels this machine's Switch Matrix page prints differently from the parts list.
SWITCH_MATRIX_PAGE_LABELS = {
	24: "Always Closed", 36: "Left Score Post", 51: "Left Sling (2)", 52: "Right Sling (2)",
	62: "Crane Exit",
}
# Retained script handlers that pulse rather than hold the public switch.
PULSED_SWITCHES = (16, 17, 32, 33, 34, 35, 37, 38, 42, 43, 51, 52, 63, 64, 65, 66, 72, 75, 76, 87)

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
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-7"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute; the manual prints \"Forth Coin Chute\"."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
# Fliptronic F1-F8, printed in the right-hand block of the switch matrix page (2-42) and in the
# Switch Locations parts list (2-43). All eight are genuine flipper hardware on this machine.
FLIPPER_SWITCH_LABELS = {
	111: ("Lower Right Flipper EOS", "F1", "SW-1A-194", "Black-Green", "J906-1", "eos"),
	112: ("Lower Right Flipper Button", "F2", "A-16384-1", "Blue-Violet", "J905-1", "button"),
	113: ("Lower Left Flipper EOS", "F3", "SW-1A-194", "Black-Blue", "J906-3", "eos"),
	114: ("Lower Left Flipper Button", "F4", "A-15894", "Blue-Gray", "J905-2", "button"),
	115: ("Upper Right Flipper EOS", "F5", "SW-1A-194", "Black-Violet", "J906-4", "eos"),
	116: ("Upper Right Flipper Button", "F6", "A-16384-1", "Black-Yellow", "J905-3", "button"),
	117: ("Upper Left Flipper EOS", "F7", "SW-1A-194", "Black-Gray", "J906-5", "eos"),
	118: ("Upper Left Flipper Button", "F8", "A-15894", "Black-Blue", "J905-5", "button"),
}

# --- Printed solenoid/flasher table (2-44) and solenoid/flasher locations (2-45).
SOLENOID_LABELS = {
	1: "Globe Magnet", 2: "Left Popper", 3: "Right Popper", 4: "Globe Arm",
	5: "Reset Drop Targets", 6: "Globe Motor", 7: "Knocker", 8: "Right Shooter",
	9: "Left Shooter", 10: "Trip Drop Target", 11: "Diverter", 13: "Trough",
	15: "Left Slingshot", 16: "Right Slingshot",
	17: "Judge Fire Flashers", 18: "Judge Fear Flashers", 19: "Judge Death Flashers",
	20: "Judge Mortis Flashers", 21: "Pursuit Left Flashers", 22: "Pursuit Right Flashers",
	23: "Blackout Flashers", 24: "Cursed Earth Flashers", 25: "Lower Left Flashers",
	26: "Globe Flashers", 27: "Right Ramp Flashers", 28: "Insert Flashers",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
SOLENOID_KINDS = {
	1: "magnet", 2: "coil", 3: "coil", 4: "motor", 5: "coil", 6: "motor", 7: "coil",
	8: "coil", 9: "coil", 10: "coil", 11: "coil", 13: "coil", 15: "coil", 16: "coil",
	17: "flasher", 18: "flasher", 19: "flasher", 20: "flasher", 21: "flasher", 22: "flasher",
	23: "flasher", 24: "flasher", 25: "flasher", 26: "flasher", 27: "flasher", 28: "flasher",
	33: "coil", 34: "coil", 35: "coil", 36: "coil", 45: "coil", 46: "coil", 47: "coil", 48: "coil",
}
NOT_FITTED_SOLENOID_LABELS = {
	12: "Not Used Solenoid Position 12",
	14: "Not Used Solenoid Position 14",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "WPC GameOn State Bit",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-DCS Address 37", 38: "Unused WPC-DCS Address 38",
	39: "Unused WPC-DCS Address 39", 40: "Unused WPC-DCS Address 40",
	41: "Unused WPC-DCS Address 41", 42: "Unused WPC-DCS Address 42",
	43: "Unused WPC-DCS Address 43", 44: "Unused WPC-DCS Address 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
	51: "PinMAME Claw-Release Diagnostic State",
}
USED_VIRTUAL_SOLENOIDS = {29, 30, 31, 51}
# address -> (printed type, playfield voltage conn., drive transistor, playfield drive conn.,
#             backbox voltage conn., backbox drive conn., drive wire, part number)
SOLENOID_WIRING = {
	1: ("High Power", "J130-1", "Q82", "J107-3", None, None, "Vio-Brn", "A-12158-1"),
	2: ("High Power", "J130-2", "Q80", "J107-3", None, None, "Vio-Red", "AE-26-1200"),
	3: ("High Power", "J130-4", "Q78", "J107-3", None, None, "Vio-Org", "AE-23-800"),
	4: ("High Power", "J130-5", "Q76", "J118-2", None, None, "Vio-Yel", "14-7989"),
	5: ("High Power", "J130-6", "Q64", "J107-3", None, None, "Vio-Grn", "AE-24-900"),
	6: ("High Power", "J130-7", "Q66", "J118-2", None, None, "Vio-Blu", "14-7985"),
	7: ("High Power", "J130-8", "Q68", "J107-3", None, None, "Vio-Blk", "AE-23-800"),
	8: ("High Power", "J130-9", "Q70", "J107-3", None, None, "Vio-Gry", "AE-23-800"),
	9: ("Low Power", "J127-1", "Q58", "J107-2", None, None, "Brn-Blk", "AE-23-800"),
	10: ("Low Power", "J127-3", "Q56", "J107-2", None, None, "Brn-Red", "AE-27-1200"),
	11: ("Low Power", "J127-4", "Q54", "J107-2", None, None, "Brn-Org", "AE-25-1000"),
	12: ("Low Power", None, "Q52", None, None, None, "Brn-Yel", None),
	13: ("Low Power", "J127-6", "Q50", "J107-2", None, None, "Brn-Grn", "AE-26-1500"),
	14: ("Low Power", None, "Q48", None, None, None, "Brn-Blu", None),
	15: ("Low Power", "J127-8", "Q46", "J107-2", None, None, "Brn-Vio", "AE-27-1200"),
	16: ("Low Power", "J127-9", "Q44", "J107-2", None, None, "Brn-Gry", "AE-27-1200"),
	17: ("Flasher", "J126-1", "Q42", "J107-6", "J125-1", "J106-5", "Blk-Brn", None),
	18: ("Flasher", "J126-2", "Q40", "J107-6", "J125-2", "J106-5", "Blk-Red", None),
	19: ("Flasher", "J126-3", "Q38", "J107-6", "J125-3", "J106-5", "Blk-Org", None),
	20: ("Flasher", "J126-4", "Q36", "J107-6", "J125-5", "J106-5", "Blk-Yel", None),
	21: ("Flasher", "J126-5", "Q28", "J107-6", "J125-6", "J106-5", "Blu-Grn", None),
	22: ("Flasher", "J126-6", "Q30", "J107-6", "J125-7", "J106-5", "Blu-Blk", None),
	23: ("Flasher", "J126-7", "Q34", "J107-6", "J125-8", "J106-5", "Blu-Vio", None),
	24: ("Flasher", "J126-8", "Q32", "J107-6", None, None, "Blu-Gry", None),
	25: ("Gen. Purpose", "J122-1", "Q26", "J107-6", "J124-1", "J106-5", "Blu-Brn", None),
	26: ("Gen. Purpose", "J122-2", "Q24", "J107-6", "J124-2", "J106-5", "Blu-Red", None),
	27: ("Gen. Purpose", "J122-3", "Q22", "J107-6", "J124-3", "J106-5", "Blu-Org", None),
	28: ("Gen. Purpose", None, "Q20", None, "J124-5", "J106-5", "Blu-Yel", None),
	33: ("Fliptronic power", "J907-4 (Blu-Yel)", "Q2", "J902-6", None, None, "Blk-Yel", "FL-11630"),
	34: ("Fliptronic hold", "J907-4 (Blu-Yel)", "Q7", "J902-4", None, None, "Org-Vio", "FL-11630"),
	35: ("Fliptronic power", "J907-1 (Gry-Yel)", "Q1", "J902-3", None, None, "Blk-Blu", "FL-11629"),
	36: ("Fliptronic hold", "J907-1 (Gry-Yel)", "Q5", "J902-1", None, None, "Org-Gry", "FL-11629"),
	45: ("Fliptronic power", "J907-9 (Blu-Yel)", "Q4", "J902-13", None, None, "Blu-Vio", "FL-11629"),
	46: ("Fliptronic hold", "J907-9 (Blu-Yel)", "Q11", "J902-11", None, None, "Org-Grn", "FL-11629"),
	47: ("Fliptronic power", "J907-7 (Gry-Yel)", "Q3", "J902-9", None, None, "Blu-Gry", "FL-11629"),
	48: ("Fliptronic hold", "J907-7 (Gry-Yel)", "Q9", "J902-7", None, None, "Org-Blu", "FL-11629"),
}
SOLENOID_ASSEMBLIES = {
	1: "A-16769", 2: "A-16580", 3: "A-15769", 4: "A-16678", 5: "A-16947", 6: "A-16478",
	7: "B-16086-1", 8: "A-14525", 9: "A-16936", 10: "A-16445", 11: "A-16802", 13: "A-16765",
	15: "A-14369-L", 16: "A-14369-R",
	17: "A-16844", 18: "A-16844", 19: "A-16844", 20: "A-16844",
	21: "A-12336-1", 22: "A-12336-1", 23: "A-16929", 24: "A-16891",
	25: "A-8798", 26: "A-16475", 27: "A-8798",
	33: "A-15205-R", 34: "A-15205-R", 35: "A-16976-L", 36: "A-16976-L",
	45: "A-15205-R-2", 46: "A-15205-R-2", 47: "A-15205-L-2", 48: "A-15205-L-2",
}
SOLENOID_NOT_SHOWN = (7, 28)
SOLENOID_UNDER_PLAYFIELD = (5, 6, 10, 11, 24, 26)
# address -> (printed bulb description, total bulbs, playfield bulbs, backbox bulbs)
FLASHER_BULBS = {
	17: ("#906 (1) on the playfield and #906 (1) in the backbox", 2, 1, 1),
	18: ("#906 (1) on the playfield and #906 (1) in the backbox", 2, 1, 1),
	19: ("#906 (1) on the playfield and #906 (1) in the backbox", 2, 1, 1),
	20: ("#906 (1) on the playfield and #906 (1) in the backbox", 2, 1, 1),
	21: ("#906 (2) on the playfield and #906 (1) in the backbox", 3, 2, 1),
	22: ("#906 (2) on the playfield and #906 (1) in the backbox", 3, 2, 1),
	23: ("#906 (1) on the playfield and #906 (2) in the backbox", 3, 1, 2),
	24: ("#906 (2), both on the playfield", 2, 2, 0),
	25: ("#89 (2) on the playfield and #906 (2) in the backbox", 4, 2, 2),
	26: ("#906 (1) on the playfield and #906 (2) in the backbox", 3, 1, 2),
	27: ("#89 (2) on the playfield and #906 (1) in the backbox", 3, 2, 1),
	28: ("#906 (3), all in the backbox", 3, 0, 3),
}
# Retained VPW script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "CraneMag", 2: "bsBotVUK.SolOut", 3: "bsTopVUK.SolOut", 4: "CraneArm",
	5: "ResetDrops", 6: "SolWheelDrive", 7: "SolKnocker", 8: "JDPlunger", 9: "KickBack",
	10: "TripDrop", 11: "Diverter", 13: "JDTrough",
	17: "SetLamp 117,", 18: "SetLamp 118,", 19: "SetLamp 119,", 20: "SetLamp 120,",
	21: "FlashSol21", 22: "FlashSol22", 23: "SetLamp 123,", 24: "SetLamp 124,",
	25: "SetLamp 125,", 26: "FlashSol26", 27: "SetLamp 127,", 28: "SetLamp 128,",
	33: "SolURFlipper (core.vbs sURFlipper)", 35: "SolULFlipper (core.vbs sULFlipper)",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
}

# --- Printed lamp matrix (2-40) and lamp locations (2-41). Labels come from the parts list.
LAMP_LABELS = {
	11: "Perp 1 (White)", 12: "Perp 1 (Red)", 13: "Perp 1 (Yellow)", 14: "Perp 1 (Green)",
	15: "Perp 2 (White)", 16: "Perp 2 (Red)", 17: "Perp 2 (Yellow)", 18: "Perp 2 (Green)",
	21: "Perp 4 (White)", 22: "Perp 4 (Red)", 23: "Perp 4 (Yellow)", 24: "Perp 4 (Green)",
	25: "Perp 5 (White)", 26: "Perp 5 (Red)", 27: "Perp 5 (Yellow)", 28: "Perp 5 (Green)",
	31: "Perp 3 (White)", 32: "Perp 3 (Red)", 33: "Perp 3 (Yellow)", 34: "Perp 3 (Green)",
	35: "Lock 1", 36: "Lock 2", 37: "Lock 3", 38: "Buy-In",
	41: "Crime Level 4 (White)", 42: "Crime Level 3 (Red)", 43: "Crime Level 2 (Yellow)",
	44: "Crime Level 1 (Green)", 45: "Meltdown", 46: "Impersonator", 47: "Battle Tank",
	48: "Stop Meltdown",
	51: "Stakeout", 52: "Safecracker", 53: "Pursuit", 54: "Ultimate Challenge", 55: "Manhunt",
	56: "Blackout", 57: "Sniper", 58: "Pick A Prize",
	61: "Extra Ball", 62: "Right Start Feature", 63: "Tank Center", 64: "Award Sniper",
	65: "Air Raid", 66: "Left Center Feature", 67: "Tank Left", 68: "Mystery",
	71: "Drop Target \"J\"", 72: "Drop Target \"U\"", 73: "Drop Target \"D\"",
	74: "Drop Target \"G\"", 75: "Drop Target \"E\"", 76: "Award Safecracker",
	77: "Multi-ball Jackpot", 78: "Award Bad Impersonator",
	81: "Award Stakeout", 82: "Blackout Jackpot", 83: "Drain Shield", 84: "Judge Again",
	85: "Advance Crime Level", 86: "Tank Right", 87: "Super Game", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-16843", "#555"), 12: ("A-16843", "#555"), 13: ("A-16843", "#555"), 14: ("A-16843", "#555"),
	15: ("A-16843", "#555"), 16: ("A-16843", "#555"), 17: ("A-16843", "#555"), 18: ("A-16843", "#555"),
	21: ("A-16843", "#555"), 22: ("A-16843", "#555"), 23: ("A-16843", "#555"), 24: ("A-16843", "#555"),
	25: ("A-16843", "#555"), 26: ("A-16843", "#555"), 27: ("A-16843", "#555"), 28: ("A-16843", "#555"),
	31: ("A-16843", "#555"), 32: ("A-16843", "#555"), 33: ("A-16843", "#555"), 34: ("A-16843", "#555"),
	35: ("A-11754", "#44"), 36: ("A-11271", "#44"), 37: ("A-11754", "#44"), 38: ("20-9663-13", None),
	41: ("A-16839", "#555"), 42: ("A-16839", "#555"), 43: ("A-16839", "#555"), 44: ("A-16839", "#555"),
	45: ("A-16839", "#555"), 46: ("A-16839", "#555"), 47: ("A-16839", "#555"), 48: ("B-12224", "#555"),
	51: ("A-16839", "#555"), 52: ("A-16839", "#555"), 53: ("A-16839", "#555"), 54: ("A-16839", "#555"),
	55: ("A-16839", "#555"), 56: ("A-16839", "#555"), 57: ("A-16839", "#555"), 58: ("A-8882", "#44"),
	61: ("A-16841", "#555"), 62: ("A-16841", "#555"), 63: ("A-16841", "#555"), 64: ("A-16841", "#555"),
	65: ("A-16841", "#555"), 66: ("A-11754", "#44"), 67: ("A-11754", "#44"), 68: ("A-11271", "#44"),
	71: ("A-16840", "#555"), 72: ("A-16840", "#555"), 73: ("A-16840", "#555"), 74: ("A-16840", "#555"),
	75: ("A-16840", "#555"), 76: ("A-16840", "#555"), 77: ("A-16840", "#555"), 78: ("A-16840", "#555"),
	81: ("A-8882", "#44"), 82: ("A-11754", "#44"), 83: ("A-16929", "#555"), 84: ("A-16929", "#555"),
	85: ("A-16340", "#555"), 86: ("A-16340", "#555"), 87: ("20-9663-10", None), 88: ("20-9663-1", None),
}
LAMP_QUANTITIES = {61: 2, 83: 2}
LAMP_CABINET_ADDRESSES = (38, 87, 88)
LAMP_MATRIX_PAGE_LABELS = {61: "Right Extra Ball"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"),
	3: ("Yellow-Orange", "J137-3", "Q96"), 4: ("Yellow-Black", "J137-4", "Q95"),
	5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-4", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

# --- Printed general illumination (2-44 and 2-45). Public address N is printed string N + 1.
GI_STRINGS = {
	0: ("String 1", "J-120-1", "Q18", "J-120-7", "J-121-1", "J-121-6", "Wht-Brn", "#44", "#555"),
	1: ("String 2", "J-120-2", "Q10", "J-120-8", "J-121-2", "J-121-8", "Wht-Org", "#555", "#555"),
	2: ("String 3", "J-120-3", "Q14", "J-120-9", "J-121-3", "J-121-7", "Wht-Yel", "#44", "#555"),
	3: ("String 4", "J-120-5", "Q16", "J-120-10", "J-121-5", "J-121-10", "Wht-Grn", "#555", "#555"),
	4: ("String 5", "J-121-6", "Q12", "J-120-11", None, None, "Wht-Vio", "#555", None),
}
# The retained script's own collection comment for each public GI address, verbatim.
GI_SCRIPT_COMMENTS = {
	0: "wht/vio  Left/Right Middle GI, Backbox Bottom / Coin Door Maybe?",
	1: "wht/grn  Top & Under Deadworld GI, Backbox Middle",
	2: "wht/yel  Low Left, Slingshots & Upper Left JD Backbox",
	3: "wht/org  Deadworld Planet GI",
	4: "wht/brn  Backbox Top Right, Front Buttons",
}

# --- Normalized playfield coordinates from the retained VPW v1.1 extraction (x/1093, y/2162).
SWITCH_POSITIONS = {
	15: [(0.050677, 0.892147)],
	16: [(0.147583, 0.752392)],
	17: [(0.203593, 0.752572)],
	18: [(0.653681, 0.460209), (0.653647, 0.437641), (0.653685, 0.415084)],
	25: [(0.767428, 0.247378)],
	26: [(0.834849, 0.494568)],
	27: [(0.117843, 0.566472)],
	33: [(0.419259, 0.081865)],
	34: [(0.775587, 0.752577)],
	35: [(0.466934, 0.112817)],
	36: [(0.153259, 0.391626)],
	37: [(0.31473, 0.3284)],
	38: [(0.271729, 0.438483)],
	41: [(0.942654, 0.891454)],
	42: [(0.888342, 0.736885)],
	43: [(0.83227, 0.737031)],
	51: [(0.289021, 0.74675)],
	52: [(0.689489, 0.747789)],
	53: [(0.867845, 0.422924)],
	54: [(0.336559, 0.36104)],
	55: [(0.382313, 0.34781)],
	56: [(0.430454, 0.333973)],
	57: [(0.478838, 0.319978)],
	58: [(0.52344, 0.307221)],
	61: [(0.325711, 0.220814)],
	62: [(0.05581, 0.226642)],
	63: [(0.492223, 0.113321)],
	64: [(0.922232, 0.051341)],
	66: [(0.371455, 0.038853)],
	67: [(0.167429, 0.110546)],
	68: [(0.872264, 0.322924)],
	71: [(0.107114, 0.102134)],
	72: [(0.860018, 0.234505)],
	73: [(0.053586, 0.539086)],
	74: [(0.786835, 0.132744)],
	75: [(0.668474, 0.133324)],
	76: [(0.667801, 0.134591)],
	77: [(0.325711, 0.220814)],
	81: [(0.367357, 0.974698)],
	82: [(0.429977, 0.977613)],
	83: [(0.488625, 0.980719)],
	84: [(0.546611, 0.983513)],
	85: [(0.604174, 0.986005)],
	86: [(0.668684, 0.986977)],
	87: [(0.668684, 0.986977)],
}
SWITCH_PROJECTIONS = {
	18: (
		"Three physical standup targets share the one matrix address. The manual's own location "
		"diagram draws the 18 callout three times against a single `A-14227-15` part number, and the "
		"retained script instantiates three separate hit targets (sw18, sw18a, sw18b) that all report "
		"the same public switch. Each of the three retained objects supplies one placement rather "
		"than one being chosen or the three being averaged."
	),
	61: (
		"Projected onto the rotating Deadworld disc (Primitive DW_Disc, table object center). The "
		"manual marks item 61 `*Not Shown` in the parts list yet draws its callout inside the disc "
		"outline at the hub, and pinned PinMAME reads it as the ball-resting-on-the-globe state in "
		"jd_stateDef's \"Planet\" step rather than from a fixed playfield sensor."
	),
	71: (
		"Projected onto the crane assembly (Primitive Crane, table object center). The manual marks "
		"item 71 `†Located Under Playfield`, and the retained script asserts public switch 71 from "
		"the crane arm's own rotation angle inside Crane_X_Timer rather than from a playfield trigger."
	),
	77: (
		"Projected onto the rotating Deadworld disc (Primitive DW_Disc, table object center). The "
		"manual marks item 77 `*Not Shown` and draws its callout at the disc hub beside 61; the "
		"retained script asserts public switch 77 when the disc's own rotation angle brings a loaded "
		"slot under the crane (FWTimer_Timer), and pinned PinMAME's jd_handleMech does the same from "
		"a 0-100 globe-position counter. It is an angular position sensor, not a playfield location."
	),
	87: (
		"Projected onto the trough eject position (Kicker sw86). The retained script's trough handler "
		"kicks the ball resting at Trough 6 and pulses public switch 87 in the same event "
		"(Sub JDTrough: sw86.kick 37,30 then vpmTimer.PulseSw 87), and the manual's location diagram "
		"draws 87 immediately outboard of 86 at the eject end of the trough."
	),
}

SOLENOID_POSITIONS = {
	1: [(0.107114, 0.102134)],
	2: [(0.053586, 0.539086)],
	3: [(0.786835, 0.132744)],
	4: [(0.107114, 0.102134)],
	5: [(0.335881, 0.360424)],
	6: [(0.325673, 0.220822)],
	8: [(0.95253, 0.943079)],
	9: [(0.05032, 0.93515)],
	10: [(0.429672, 0.333303)],
	11: [(0.466606, 0.006938)],
	13: [(0.668684, 0.986977)],
	15: [(0.289021, 0.74675)],
	16: [(0.689489, 0.747789)],
	17: [(0.627209, 0.609621)],
	18: [(0.315645, 0.609621)],
	19: [(0.503453, 0.609621)],
	20: [(0.407336, 0.609621)],
	21: [(0.185009, 0.39554), (0.304347, 0.380802)],
	22: [(0.661423, 0.483842), (0.778941, 0.505036)],
	23: [(0.488315, 0.797686)],
	24: [(0.15704, 0.24277), (0.331432, 0.117367)],
	25: [(0.096344, 0.791254), (0.057088, 0.588707)],
	26: [(0.3253, 0.220701)],
	27: [(0.869126, 0.110577), (0.820478, 0.313288)],
	33: [(0.731673, 0.353217)],
	34: [(0.731673, 0.353217)],
	35: [(0.093245, 0.484046)],
	36: [(0.093245, 0.484046)],
	45: [(0.643951, 0.862627)],
	46: [(0.643951, 0.862627)],
	47: [(0.339351, 0.862627)],
	48: [(0.339351, 0.862627)],
}
SOLENOID_PROJECTIONS = {
	1: (
		"Projected onto the crane assembly (Primitive Crane, table object center). The Globe Magnet "
		"is carried on the end of the crane arm and has no fixed playfield position; the manual draws "
		"its callout on the crane assembly at the left of the globe."
	),
	4: (
		"Projected onto the crane assembly (Primitive Crane, table object center); the Globe Arm motor "
		"drives that assembly and the manual draws its callout on it. Same anchor as solenoid 1, which "
		"is mounted on the same arm."
	),
	5: (
		"Projected onto the \"J\" drop target (Primitive sw54prim), the left-hand end of the five-target "
		"JUDGE bank that this coil resets. The manual marks item 05 `†Located Under Playfield` and draws "
		"its callout at that end of the bank. The coil is part of the bank's own mechanism; it is not "
		"placed at a centroid of the five targets."
	),
	10: (
		"Projected onto the \"D\" drop target (Primitive sw56prim), the single target this coil pulls "
		"down. The manual marks item 10 `†Located Under Playfield` and the retained script's TripDrop "
		"handler drops exactly that target."
	),
	13: (
		"Projected onto the trough eject position (Kicker sw86), the ball position this coil ejects "
		"from; the manual draws item 13 at the eject end of the trough."
	),
}

LAMP_POSITIONS = {
	11: [(0.158234, 0.459997)], 12: [(0.151223, 0.450577)], 13: [(0.143283, 0.441211)],
	14: [(0.136003, 0.431982)], 15: [(0.489258, 0.229368)], 16: [(0.479737, 0.221347)],
	17: [(0.468746, 0.212188)], 18: [(0.459817, 0.204429)],
	21: [(0.762866, 0.283732)], 22: [(0.751461, 0.289846)], 23: [(0.737595, 0.296819)],
	24: [(0.725458, 0.303751)], 25: [(0.700738, 0.526174)], 26: [(0.694125, 0.535162)],
	27: [(0.687532, 0.544501)], 28: [(0.681131, 0.553601)],
	31: [(0.682225, 0.143044)], 32: [(0.67999, 0.153088)], 33: [(0.677457, 0.163441)],
	34: [(0.673968, 0.173708)], 35: [(0.280255, 0.46509)], 36: [(0.262529, 0.442205)],
	37: [(0.245598, 0.418636)],
	41: [(0.589145, 0.741906)], 42: [(0.524432, 0.741906)], 43: [(0.459361, 0.741906)],
	44: [(0.393404, 0.741906)], 45: [(0.575929, 0.695271)], 46: [(0.49094, 0.698196)],
	47: [(0.403894, 0.69557)], 48: [(0.768748, 0.584743)],
	51: [(0.738824, 0.663668)], 52: [(0.605452, 0.666084)], 53: [(0.242512, 0.662396)],
	54: [(0.490778, 0.653456)], 55: [(0.665711, 0.683558)], 56: [(0.319454, 0.68233)],
	57: [(0.376746, 0.666493)], 58: [(0.355465, 0.272403)],
	61: [(0.163058, 0.407578), (0.742862, 0.259969)],
	62: [(0.654288, 0.258018)], 63: [(0.574632, 0.237131)], 64: [(0.664788, 0.213708)],
	65: [(0.718751, 0.238292)], 66: [(0.307856, 0.503192)], 67: [(0.197125, 0.512181)],
	68: [(0.165334, 0.579442)],
	71: [(0.361444, 0.382237)], 72: [(0.408451, 0.36832)], 73: [(0.45559, 0.355698)],
	74: [(0.503055, 0.342378)], 75: [(0.550412, 0.3292)], 76: [(0.565924, 0.374211)],
	77: [(0.488308, 0.38777)], 78: [(0.438795, 0.409011)],
	81: [(0.791611, 0.383111)], 82: [(0.538413, 0.148233)],
	84: [(0.491486, 0.874109)], 85: [(0.611827, 0.441613)], 86: [(0.527184, 0.438556)],
}

GI_POSITIONS = {
	0: [
		(0.0348, 0.589919), (0.031275, 0.483548), (0.886171, 0.543361),
		(0.701686, 0.396457), (0.039723, 0.393736),
	],
	1: [
		(0.885067, 0.074438), (0.7386, 0.166706), (0.600667, 0.140489),
		(0.470409, 0.158599), (0.461001, 0.259776),
	],
	2: [
		(0.704398, 0.780364), (0.737399, 0.73876), (0.277688, 0.780415),
		(0.243627, 0.739277), (0.098126, 0.769499),
	],
	3: [(0.280882, 0.222896), (0.368146, 0.218938)],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Judge Dredd retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Judge Dredd extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Judge Dredd retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Judge Dredd retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Judge Dredd retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
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
			"locator": "Pinned catalog driver records for the twelve-driver jd_l7 clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/jd.c jdGameData GEN_WPCDCS with wpc_dispDMD; hw fields "
				"flippers=FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U), swCol=0, lampCol=0, custSol=1, "
				"soundBoard=0, display=0; inverted-switch mask "
				"{0x00,0x00,0x00,0x02,0x00,0xf8,0x6e,0x3e,0x7f,0x00,0x00,0x00}; comSw "
				"{swStart=13, swTilt=14, swSlamTilt=21, swCoinDoor=22, shooter=swRFire=12}; the switch and "
				"solenoid #define block; sFakeSol1 = CORE_CUSTSOLNO(1) with its stale /* 33 */ comment; "
				"jd_getSol returning core_getSol(sArmMagnet)==0 for that address; jd_handleMech's 0-100 "
				"globePos and armPos counters driving swGlobe2 (77) and swArmFR (71) and its five-target "
				"drop-target block; jd_stateDef's Planet/In Claw/Dropped and Subway ball paths; init_jd, "
				"which does not call wpc_set_fastflip_addr. src/wpc/core.h CORE_FIRSTUFLIPSOL=33, "
				"CORE_FIRSTLFLIPSOL=45, CORE_FIRSTCUSTSOL=51, CORE_CUSTSOLNO(n), FLIP_L/FLIP_U bit "
				"definitions; src/wpc/core.c core_getSol dispatch (the 37-44 branch is gated on "
				"GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11 and returns 0 for GEN_WPCDCS); src/wpc/wpc.c the "
				"wpc_fastflip_addr == 0 branch mirroring WPC_GILAMPS bits 5-7 into public solenoids "
				"29-31, the WPC_FLIPPERS complement for (gen & GENWPC_HASWPC95) == 0, and the five-bit "
				"WPC_GILAMPS to coreGlobals.gi[0..4] loop; src/libpinmame/libpinmame.h "
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
			"locator": (
				"WPC-DCS public switch, DIP, solenoid, lamp, and five-GI address rules, including the "
				"Fliptronic 111-118 order, the absence of an LPDC board (37-44 unused on this "
				"generation), and CORE_FIRSTCUSTSOL = 51"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.judge-dredd.1993/ipdb/Bally_1993_Judge_Dredd_Manual.pdf",
			"original_filename": "Bally_1993_Judge_Dredd_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"148-page scan of the Bally Judge Dredd operations manual with an Adobe Paper Capture OCR "
				"layer. Printed pages 2-40 through 2-45 carry the lamp matrix, lamp locations, switch "
				"matrix, switch locations, solenoid/flasher table and solenoid/flasher locations; "
				"printed 3-3 carries the dedicated-switch wiring and circuit; printed 3-10 carries the "
				"general-illumination circuit. The OCR text layer scrambles every multi-column table on "
				"those pages and was never used for a value."
			),
			"license": "NOASSERTION",
			"attribution": "Bally / Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.judge-dredd.switch-matrix",
					"locator": "PDF page 110, printed 2-42, SWITCH MATRIX grid, opto legend, dedicated and Fliptronic blocks",
					"path": "evidence/excerpts/bally.judge-dredd.1993/switch-matrix.md",
					"sha256": "4cfb0c5c481ce23c41973bb8d8ee5dd4bcf355625319fdf176d66ea58c19b1ab",
					"image": "evidence/excerpts/bally.judge-dredd.1993/switch-matrix.webp",
					"image_sha256": "c1dd472e2920da0ac2115f091dc3c4bd218bdf90d1936f6831db0f93bcd535c8",
					"image_derivation": (
						"Bally_1993_Judge_Dredd_Manual.pdf page 110, crop box 0.255,0.055,0.735,0.465 of the "
						"page, rendered at 300 dpi with pdftoppm, reduced to 820px wide grayscale, quality 66 WebP"
					),
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page and swept mechanically for the opto halftone",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.switch-locations",
					"locator": "PDF pages 110-111, printed 2-42 lower half and 2-43, SWITCH LOCATIONS parts list and playfield diagram",
					"path": "evidence/excerpts/bally.judge-dredd.1993/switch-locations.md",
					"sha256": "90fbcd6aae797a2f541f6a4dcfa5adae2977d673e6d51ce8a9d63d360f9b379d",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.lamp-matrix",
					"locator": "PDF page 108, printed 2-40, LAMP MATRIX table",
					"path": "evidence/excerpts/bally.judge-dredd.1993/lamp-matrix.md",
					"sha256": "8dad6dc5fa21ec2048949d533e82d692796c34841a8fa61fde6e3bf762964e36",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.lamp-locations",
					"locator": "PDF page 109, printed 2-41, LAMP LOCATIONS parts list and playfield diagram",
					"path": "evidence/excerpts/bally.judge-dredd.1993/lamp-locations.md",
					"sha256": "ea8f9f041403f4e96e9a836fb83a0c741305d9770b2fdf5c2c81e1a22f354773",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.solenoid-flasher-table",
					"locator": "PDF page 112, printed 2-44, SOLENOID/FLASHER TABLE with its General Illumination and Flipper Circuits blocks",
					"path": "evidence/excerpts/bally.judge-dredd.1993/solenoid-flasher-table.md",
					"sha256": "2a860ded19875d4e81172e7e0dd99517dda788c43e5cc2b16da1886a827f6f2e",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.solenoid-flasher-locations",
					"locator": "PDF page 113, printed 2-45, SOLENOID/FLASHER LOCATIONS parts list, GI circuits, flipper coils and playfield diagram",
					"path": "evidence/excerpts/bally.judge-dredd.1993/solenoid-flasher-locations.md",
					"sha256": "1fdab88c604ae4dfabcd77a6263ac354df10c0bd5702c0ad7d6184ac7c81be87",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.general-illumination",
					"locator": "PDF page 124, printed 3-10, General Illumination Circuit and block diagram",
					"path": "evidence/excerpts/bally.judge-dredd.1993/general-illumination.md",
					"sha256": "2fcf2c302de342386b044febec280058e63f8fde7f4caf23e137f247f9c1c33f",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.judge-dredd.dedicated-switches",
					"locator": "PDF page 117, printed 3-3, DEDICATED SWITCHES wiring and DEDICATED SWITCH CIRCUIT",
					"path": "evidence/excerpts/bally.judge-dredd.1993/dedicated-switches.md",
					"sha256": "229bf6c17ac2334e19830a38c90a14fdbb28d2f4713099d0ae54fdff7ab9c9bd",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/judge-dredd-1993/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained record of how the printed tables were read: the rendered page cache under "
				"external:pinmame-manuals/rendered/bally.judge-dredd.1993/, the identity check against "
				"the same-titled Judge Dredd video-game manuals, the reason the PDF's own OCR layer was "
				"never trusted, and the mechanical connected-component sweep that established which "
				"switch-matrix cells carry the opto halftone."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/judge-dredd-1993/source/Judge%20Dredd%20%28Bally%201993%29%20VPW%20v1.1.vpx",
			"original_filename": "Judge Dredd (Bally 1993) VPW v1.1.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working V-Pin Workshop v1.1 recreation of the physical machine, VPX file "
				f"version 10.6. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are "
				"x/1093 and y/2162, the wide-body Superpin divisor. Geometry authority only for named "
				"table objects."
			),
			"license": "NOASSERTION",
			"attribution": "V-Pin Workshop",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/judge-dredd-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				f"Retained embedded VPW script ({SCRIPT_BYTES:,} bytes). Runtime and mechanism-causality "
				"authority: cGameName = \"jd_l1\" carrying the author's own '***DO NOT CHANGE***' note and "
				"the explanation that L-1 keeps the physical Deadworld ball lock that production code "
				"deactivated; Const UseSolenoids = 2, UseLamps = 0, UseGI = 0, UseSync = 0, HandleMech = 0; "
				"the SolCallBack table for solenoids 1-28 plus core.vbs sLRFlipper/sLLFlipper/sURFlipper/"
				"sULFlipper; Lampz.MassAssign for lamp addresses 11-86 and flasher pseudo-lamps 117-128; "
				"ModLampz.MassAssign binding public GI 0-4 to the GIstring1-GIstring5 collections with "
				"their own wire-colour comments; the Controller.Switch and vpmTimer.PulseSw semantics for "
				"the Deadworld globe, crane, trough, subway and JUDGE drop-target state machines; and the "
				"commented-out SW32/SW67 block recording that the ramp-entrance opto address changed "
				"between the L-1 and L-7 ROM revisions."
			),
			"license": "NOASSERTION",
			"attribution": "V-Pin Workshop table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/judge-dredd-1993/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 "
				f"under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
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
				"optional" if address == 4 else "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={
					"location": "coin door",
					"switch_type": "button",
					"notes": (
						f"Printed dedicated grounded switch D{address}. {note} The dedicated-switch "
						"circuit ties the column side permanently to ground, so a closed contact pulls "
						"the dedicated input low and the board reports the switch closed; these are "
						"ordinary normally-open contacts."
					),
				},
				wiring={
					"board": "WPC CPU board",
					"drive_wire": wire,
					"drive_connection": connection,
					"return_component": component,
				},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	normalized = set(PINMAME_NORMALIZED_SWITCHES)
	shaded = set(MATRIX_SHADED_OPTO_SWITCHES)
	parts_opto = set(PARTS_LIST_OPTO_SWITCHES)
	pulsed = set(PULSED_SWITCHES)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"switch.matrix-{address}"
			label = SWITCH_LABELS.get(address)
			unresolved = address in UNRESOLVED_MATRIX_ADDRESSES
			unused = label is None and not unresolved
			if unresolved:
				label, unresolved_note = UNRESOLVED_MATRIX_ADDRESSES[address]
			elif unused:
				label = f"Not Used Switch Position {address}"

			physical: dict[str, Any] = {}
			part = SWITCH_PARTS.get(address)
			if part:
				physical["part_number"] = part
			if address in shaded or address in parts_opto:
				physical["switch_type"] = "opto"
			elif address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in SWITCH_UNDER_PLAYFIELD:
				physical["location"] = "under playfield"
			elif address in (11, 12, 13, 31, 44):
				physical["location"] = "cabinet"
			elif address in (14, 21, 22, 23, 24):
				physical["location"] = "coin door / cabinet"
			if address == 18:
				physical["quantity"] = 3

			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if address in SWITCH_MATRIX_PAGE_LABELS and SWITCH_MATRIX_PAGE_LABELS[address] != label:
				notes += (
					f" The switch-matrix page prints this cell \"{SWITCH_MATRIX_PAGE_LABELS[address]}\"; "
					"the switch-locations parts list is preferred as the label source."
				)
			if address == 62:
				notes += (
					" The switch-locations parts list prints item 62 \"Left Ramp Enter\", the same label "
					"it already prints on item 67. The switch-matrix page prints \"Crane Exit\", the "
					"location diagram draws the 62 callout at the extreme left playfield edge beside the "
					"crane, pinned PinMAME defines swGlobeExit 62 with the comment \"Fires when ball is "
					"dropped from Magnet!\", and the retained script's handler is commented \"Crane Exit "
					"Opto, *critical* to keeping track of balls.\" The duplicated parts-list row is a "
					"copy-paste slip."
				)
			if address == 18:
				notes += (
					" Three physical standup targets are wired to this one matrix address: the manual's "
					"location diagram draws the 18 callout three times against a single A-14227-15 part "
					"number, and the retained script instantiates three hit targets (sw18, sw18a, sw18b) "
					"that all report public switch 18."
				)
			if address in (51, 52):
				notes += (
					" The printed cell carries \"(2)\": each slingshot assembly has a kick switch "
					"(SW-1A-114) and a separate score switch (SW-1A-120), both wired to this one address."
				)
			if address in shaded and address in parts_opto:
				notes += (
					" Printed as an opto both ways: the switch-matrix cell carries the \"Opto, Typically "
					"Closed\" halftone and the switch-locations row discloses a two-part LED and "
					"phototransistor construction."
				)
			elif address in shaded:
				notes += (
					" The switch-matrix cell carries the \"Opto, Typically Closed\" halftone, but the "
					"switch-locations row gives a single A-16598 Globe Position part number with no "
					"LED/phototransistor breakout."
				)
			elif address in parts_opto:
				notes += (
					" The switch-locations row discloses a two-part LED and phototransistor construction, "
					"but the switch-matrix page leaves the whole of column 8 unshaded, so the printed "
					"opto marker is absent for this address."
				)
			if address in normalized:
				notes += (
					" Pinned PinMAME's jdGameData inverted-switch mask covers this address, so the public "
					"switch state is already normalized and must not be inverted again."
				)
			elif address in shaded or address in parts_opto:
				notes += (
					" Pinned PinMAME's jdGameData inverted-switch mask does not cover this address, so "
					"the public state is not emulator-normalized even though the hardware is a "
					"normally-closed opto; see conflict.column-6-7-optos-not-all-normalized."
				)
			if address in (54, 55, 56, 57, 58):
				notes += (
					" The mask does cover this address even though no source discloses opto construction "
					"for the A-16486 drop target; see conflict.judge-drop-targets-normalized-without-opto-evidence."
				)
			if address == 24:
				notes += (
					" Part 5643-09288-00 is a permanently closed link used to prove the matrix is connected."
				)
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 23:
				notes += " Optional ticket-dispenser input; the parts list gives no part number for it."
			if unused:
				notes += (
					" The switch matrix, the switch-locations parts list and the location diagram all agree "
					"nothing is fitted here: the cell reads \"Not Used\", the parts-list row has a blank "
					"part number, and the diagram draws no callout."
				)
			if unresolved:
				notes += " " + unresolved_note
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if address in SWITCH_NOT_SHOWN:
				notes += " The parts list marks this item \"*Not Shown\"."
			physical["notes"] = notes

			aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
			if address in SWITCH_MATRIX_PAGE_LABELS and SWITCH_MATRIX_PAGE_LABELS[address] != label:
				aliases.append({"namespace": "manual.switch-matrix-label", "value": SWITCH_MATRIX_PAGE_LABELS[address]})

			extra: dict[str, Any] = {
				"aliases": aliases,
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if address in shaded or address in parts_opto:
				extra["normally_closed"] = True
			elif not unused and not unresolved:
				extra["normally_closed"] = False
			if address in pulsed:
				extra["pulse"] = True
			if address == 24:
				extra["constant_active"] = True
			if address in (11, 12, 13, 31, 44):
				extra["roles"] = ["cabinet.button"]
			elif address in (14, 21, 22):
				extra["roles"] = ["cabinet.service"]
			elif address == 23:
				extra["roles"] = ["cabinet.ticket"]

			if address in SWITCH_POSITIONS:
				extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			elif unused:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			elif address in (11, 12, 13, 31, 44):
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in (14, 21, 22, 23):
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 24:
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
			# 28, 32 and 65 deliberately carry no spatial key: whether anything is fitted at all is
			# unresolved, so there is no honest placement and no honest not_applicable reason either.

			kind = "constant" if address == 24 else "switch"
			availability = "used"
			if unused:
				availability = "unused"
			elif unresolved:
				availability = "unknown"
			elif address == 23:
				availability = "optional"

			items.append(
				_device(
					identifier,
					label,
					kind,
					"pinmame.input.switch",
					address,
					availability,
					(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
					**extra,
				)
			)

	for address, (label, printed, part, wire, connection, role) in FLIPPER_SWITCH_LABELS.items():
		identifier = f"switch.flipper-{address}"
		is_button = role == "button"
		notes = (
			f"Printed Fliptronic grounded switch {printed} ({part}). "
			+ (
				"Cabinet flipper button, printed \"Opto\" on the switch-matrix page and "
				"\"Flipper Cabinet\" in the switch-locations parts list."
				if is_button
				else "End-of-stroke leaf switch on the flipper assembly under the playfield."
			)
			+ " Judge Dredd fits four flippers, so unlike several other WPC games of this generation "
			"none of the eight Fliptronic positions is repurposed for non-flipper hardware; the "
			"manual's flipper-coil list, its Fliptronic switch block and pinned PinMAME's "
			"FLIP_SW(FLIP_L|FLIP_U) all agree."
		)
		items.append(
			_device(
				identifier,
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": printed},
				],
				normally_closed=False,
				physical={
					"part_number": part,
					"switch_type": "opto" if is_button else "leaf",
					"location": "cabinet" if is_button else "under playfield",
					"notes": notes,
				},
				wiring={"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable(
					"cabinet_or_service" if is_button else "internal_nonvisual", MANUAL_SOURCE
				),
			)
		)

	return items


def solenoid_output_id(address: int) -> str:
	label = SOLENOID_LABELS.get(address)
	if label:
		prefix = "flasher" if SOLENOID_KINDS[address] == "flasher" else "coil"
		return f"{prefix}.{slug(label)}"
	if address in NOT_FITTED_SOLENOID_LABELS:
		return f"solenoid.unused-{address}"
	return f"solenoid.virtual-{address}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in sorted(set(SOLENOID_LABELS) | set(NOT_FITTED_SOLENOID_LABELS) | set(VIRTUAL_SOLENOID_LABELS)):
		identifier = solenoid_output_id(address)
		fitted = address in SOLENOID_LABELS
		not_fitted = address in NOT_FITTED_SOLENOID_LABELS
		label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS.get(address) or VIRTUAL_SOLENOID_LABELS[address]
		kind = SOLENOID_KINDS.get(address, "virtual")

		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if fitted or not_fitted:
			if address <= 28:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})

		physical: dict[str, Any] = {}
		wiring: dict[str, Any] = {}
		extra: dict[str, Any] = {"aliases": aliases}

		if address in SOLENOID_WIRING:
			printed_type, pf_voltage, transistor, pf_drive, bb_voltage, bb_drive, wire, part = SOLENOID_WIRING[address]
			wiring["board"] = "Fliptronic II board" if address in (33, 34, 35, 36, 45, 46, 47, 48) else "WPC power driver board"
			wiring["driver_transistor"] = transistor
			if pf_voltage:
				wiring["power_connection"] = pf_voltage
			if pf_drive:
				wiring["control_connection"] = pf_drive
			elif bb_drive:
				wiring["control_connection"] = bb_drive
			wiring["control_wire"] = wire
			if part:
				physical["part_number"] = part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
		notes_parts: list[str] = []
		if address in SOLENOID_WIRING:
			printed_type = SOLENOID_WIRING[address][0]
			notes_parts.append(f"Printed solenoid/flasher table type \"{printed_type}\".")
		if address in FLASHER_BULBS:
			description, total, playfield_bulbs, backbox_bulbs = FLASHER_BULBS[address]
			physical["quantity"] = total
			notes_parts.append(
				f"Printed flashlamp complement {description}; the locations page prints the same total "
				f"as \"({total})\". {playfield_bulbs} playfield and {backbox_bulbs} backbox bulbs."
			)
		if address in SOLENOID_UNDER_PLAYFIELD:
			physical["location"] = "under playfield"
			notes_parts.append("The locations parts list marks this item \"†Located Under Playfield\".")
		if address in SOLENOID_NOT_SHOWN:
			notes_parts.append("The locations parts list marks this item \"*Not Shown\".")
		if not_fitted:
			notes_parts.append(
				"Printed \"Not Used\" with blank voltage and drive connections and a blank part number "
				f"on the solenoid/flasher table, and absent from the locations parts list. The drive "
				f"transistor {SOLENOID_WIRING[address][1] or ''}{SOLENOID_WIRING[address][2]} is still "
				"populated on the power driver board; the blank connection columns, not the transistor, "
				"are what prove nothing is fitted."
			)
		if address in SOLENOID_CALLBACKS:
			notes_parts.append(f"Retained script callback: {SOLENOID_CALLBACKS[address]}.")
		if address in (33, 34, 35, 36):
			notes_parts.append(
				"Public address from CORE_FIRSTUFLIPSOL = 33; the manual's flipper-circuit table numbers "
				"no flipper circuit at all, so there is no printed number to mistake for this one. "
				"Judge Dredd genuinely fits both upper flippers, and pinned PinMAME's "
				"FLIP_SOL(FLIP_L|FLIP_U) routes 33-36 through the upper-flipper coil path accordingly."
			)
		if address in (45, 46, 47, 48):
			notes_parts.append("Public address from CORE_FIRSTLFLIPSOL = 45.")
		if address in (29, 30):
			notes_parts.append(
				"Not a physical driver output. Pinned PinMAME mirrors two of the three WPC J111 "
				"general-purpose GPIO bits here (src/wpc/wpc.c, the wpc_fastflip_addr == 0 branch "
				"shifting WPC_GILAMPS bits 5-7 into solenoids2)."
			)
		if address == 31:
			notes_parts.append(
				"Not a physical driver output. init_jd never calls wpc_set_fastflip_addr, so this "
				"address carries WPC_GILAMPS bit 7 — the pre-Fliptronic GameOn bit — rather than "
				"PinMAME's synthetic fast-flip state that a driver with a fast-flip address publishes here."
			)
		if address == 32:
			notes_parts.append("Not a physical driver output; a WPC state channel that stays zero on this generation.")
			extra["roles"] = ["internal.unused.wpc-output"]
		if 37 <= address <= 44:
			notes_parts.append(
				"Unused address space on this hardware generation. WPC-DCS has no LPDC board, and pinned "
				"PinMAME's core_getSol serves the 37-44 branch only for GEN_WPC95, GEN_WPC95DCS and "
				"GEN_ALLS11, returning a constant 0 here."
			)
		if address == 49:
			notes_parts.append("PinMAME's simulator-only ball-shooter channel; no physical driver output.")
		if address == 50:
			notes_parts.append("Reserved WPC output below the first custom-solenoid address; no physical driver output.")
		if address == 51:
			notes_parts.append(
				"jdGameData declares hw.custSol = 1, so PinMAME publishes one game-specific custom "
				"solenoid at CORE_FIRSTCUSTSOL = 51. jd.c's own #define carries a stale \"/* 33 */\" "
				"comment from an older core.h and is wrong about the address under the pinned revision. "
				"The value is not a control line: jd_getSol answers it with core_getSol(sArmMagnet) == 0, "
				"a derived \"the claw magnet has let go\" flag that the driver's own ball simulator uses "
				"to move a ball out of the claw. Nothing on the playfield is driven by it."
			)
		if notes_parts:
			physical["notes"] = " ".join(notes_parts)
		if physical:
			extra["physical"] = physical
		if wiring:
			extra["wiring"] = wiring

		if address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
		elif address == 7:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 28:
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif not_fitted:
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			extra["spatial"] = not_applicable("virtual", CORE_SOURCE)
			if address in {29, 30, 31}:
				extra["roles"] = ["internal.wpc-state"]
			else:
				extra["roles"] = ["internal.unused.wpc-output"] if address != 51 else ["internal.derived-state"]

		availability = "used" if fitted or address in USED_VIRTUAL_SOLENOIDS else "unused"
		refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if fitted else (
			(MANUAL_SOURCE, CORE_SOURCE) if not_fitted else (CORE_SOURCE, CONTROLLER_SOURCE)
		)
		items.append(
			_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"lamp.matrix-{address}"
			label = LAMP_LABELS[address]
			assembly, bulb = LAMP_ASSEMBLIES[address]
			cabinet = address in LAMP_CABINET_ADDRESSES
			quantity = LAMP_QUANTITIES.get(address, 1)

			physical: dict[str, Any] = {"assembly_part_number": assembly, "quantity": quantity}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if cabinet:
				notes += (
					" Cabinet button lamp: the lamp-locations parts list gives it a blank bulb number and "
					"a 20-9663 button assembly, and draws it outside the playfield outline."
				)
			if quantity > 1:
				notes += (
					f" The lamp-locations parts list prints a quantity of {quantity} for this address, and "
					"its location diagram draws the callout twice."
				)
			if address in LAMP_MATRIX_PAGE_LABELS:
				notes += (
					f" The lamp-matrix page prints this cell \"{LAMP_MATRIX_PAGE_LABELS[address]}\"; the "
					"parts list is preferred as the label source."
				)
			if address == 58:
				notes += (
					" The retained script annotates this address \"Cursed Earth / Subway Entrance Lamp\", "
					"which describes where the insert sits rather than what it awards; the manual's "
					"functional name is used."
				)
			if address == 83:
				notes += (
					" The retained table models a single Light object for this address, sitting almost "
					"exactly midway between the two printed Drain Shield positions, so neither physical "
					"bulb has a usable coordinate and no placement is recorded."
				)
			physical["notes"] = notes

			aliases = [{"namespace": "pinmame.lamp", "value": str(address)}]
			if address in LAMP_MATRIX_PAGE_LABELS:
				aliases.append({"namespace": "manual.lamp-matrix-label", "value": LAMP_MATRIX_PAGE_LABELS[address]})

			drive_wire, drive_connection, drive_component = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, return_component = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": aliases,
				"physical": physical,
				"wiring": {
					"board": "WPC power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"return_component": f"column driver {drive_component}; row driver {return_component}",
				},
			}
			if cabinet:
				extra["roles"] = ["cabinet.button"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in LAMP_POSITIONS:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			# Lamp 83 deliberately carries no spatial key.

			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					"used",
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, pf_voltage, transistor, pf_drive, bb_voltage, bb_drive, wire, pf_bulb, bb_bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination {label} ({wire}). Printed playfield bulb type {pf_bulb}"
			+ (f" and backbox bulb type {bb_bulb}." if bb_bulb else ", with no backbox column entry.")
		)
		notes += (
			" Public GI address is zero-based and corresponds to the manual's printed string number: "
			"pinned PinMAME fills coreGlobals.gi[0..4] from the five low bits of WPC_GILAMPS in order "
			"(src/wpc/wpc.c)."
		)
		if address == 4:
			notes += (
				" This row prints its playfield voltage connection as J-121-6, a backbox connector pin, "
				"and that same pin is already printed as String 1's backbox drive connection; the print "
				"is preserved rather than corrected."
			)
		notes += (
			f" The retained script binds this public address to its GIstring{address + 1} collection and "
			f"comments it \"{GI_SCRIPT_COMMENTS[address]}\", a wire colour that does not match this "
			"printed string; see conflict.gi-string-order-script-vs-manual."
		)

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC power driver board",
				"driver_transistor": transistor,
				"power_connection": pf_voltage,
				"control_connection": pf_drive,
				"control_wire": wire,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the emitter coordinates and the "
				"physical quantity come from the retained table's own collection for this address."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" The retained table's collection for this address contains backglass objects only, so "
				"no playfield emitter coordinate is available even though the printed table gives this "
				"string a playfield drive connection."
			)
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
			"mechanism.deadworld-globe",
			"Deadworld rotating globe",
			"motorized",
			[solenoid_output_id(6)],
			["switch.matrix-61", "switch.matrix-77"],
			"A gearmotor (14-7985, assembly A-16478, mounted under the playfield) rotates the Deadworld "
			"globe above the playfield. The globe carries three ball slots. Pinned PinMAME models it as a "
			"free-running 0-100 position counter that advances one step per mech tick while solenoid 6 is "
			"energised and wraps at 100, asserting Globe Position #2 (switch 77) over steps 0-10 — the "
			"window in which a captured ball sits under the crane and can be lifted, which is what jd.c's "
			"own comment on swGlobe2 says. Globe Position #1 (switch 61) is the ball-present state at the "
			"globe: jd_stateDef's \"Planet\" step holds a ball on switch 61 with the Arm Magnet as its "
			"release solenoid. The retained script implements the same shape differently, rotating the "
			"disc by a fixed angular step per timer tick and asserting switch 77 when the angle brings a "
			"loaded slot to one of three drop positions. Neither position sensor is a point on the "
			"playfield surface; both are angular sensors on the globe assembly.",
			[
				("loaded", "Ball resting in a globe slot", ["switch.matrix-61"], "A ball diverted up the left ramp has come to rest on the globe."),
				("liftable", "Slot under the crane", ["switch.matrix-77"], "Globe position counter 0-10: a loaded slot is under the crane and the ball can be lifted."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16478",
		),
		mechanism(
			"mechanism.deadworld-crane",
			"Deadworld crane arm and magnet",
			"motorized",
			[solenoid_output_id(4), solenoid_output_id(1)],
			["switch.matrix-71", "switch.matrix-62"],
			"A second gearmotor (14-7989, assembly A-16678) swings a crane arm out over the globe, and an "
			"electromagnet on the end of the arm (A-12158-1, assembly A-16769) picks a ball off a globe "
			"slot and carries it back to the playfield. Pinned PinMAME models the arm as its own 0-100 "
			"position counter advancing while solenoid 4 is energised and asserts Magnet Over Ring "
			"(switch 71) over steps 0-10, the window in which the magnet is above the ring and a ball can "
			"be picked up or released. Releasing the magnet drops the ball, which then breaks the Crane "
			"Exit opto (switch 62) on its way back into play — the driver's ball simulator sequences "
			"exactly that as Planet, In Claw, Dropped. Switch 62 is the only reliable way to know a ball "
			"has left the mechanism, which is why the retained script's own handler for it is commented "
			"\"*critical* to keeping track of balls\". Whether a further switch reports that the magnet "
			"is holding a ball is unresolved; see conflict.l1-era-switch-fitment for matrix position 28.",
			[
				("over-ring", "Magnet over the ring", ["switch.matrix-71"], "Arm position counter 0-10: the magnet is above the globe and can grab or drop a ball."),
				("released", "Ball dropped from the claw", ["switch.matrix-62"], "The Crane Exit opto breaks as the released ball falls back to the playfield."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16678",
		),
		mechanism(
			"mechanism.judge-drop-targets",
			"Five-target JUDGE drop-target bank",
			"drop_target_bank",
			[solenoid_output_id(5), solenoid_output_id(10)],
			["switch.matrix-54", "switch.matrix-55", "switch.matrix-56", "switch.matrix-57", "switch.matrix-58"],
			"Five drop targets spelling J-U-D-G-E sit in a single left-to-right bank across the middle of "
			"the playfield. Solenoid 5 (Reset Drop Targets, A-16947, under the playfield) raises all five "
			"at once; solenoid 10 (Trip Drop Target, A-16445, under the playfield) pulls only the centre "
			"\"D\" target down, which is what opens the subway beneath it. Pinned PinMAME's jd_handleMech "
			"keeps a per-target up/down flag and asserts each switch while its target is DOWN, so a "
			"recreation reports the switch closed for a dropped target rather than for a struck one. The "
			"retained script drives the same five targets through its own DropTarget helper objects "
			"(DT54-DT58) and implements ResetDrops and TripDrop to match. The physical construction of the "
			"A-16486 target switch is not disclosed by any source read here, and PinMAME normalizes all "
			"five addresses; see conflict.judge-drop-targets-normalized-without-opto-evidence.",
			[
				("j", "Drop Target \"J\"", ["switch.matrix-54"], "Leftmost target of the bank."),
				("u", "Drop Target \"U\"", ["switch.matrix-55"], "Second target from the left."),
				("d", "Drop Target \"D\"", ["switch.matrix-56"], "Centre target; the only one solenoid 10 can drop on its own, opening the subway."),
				("g", "Drop Target \"G\"", ["switch.matrix-57"], "Fourth target from the left."),
				("e", "Drop Target \"E\"", ["switch.matrix-58"], "Rightmost target of the bank."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16947",
		),
		mechanism(
			"mechanism.subway",
			"Subway under the D drop target",
			"other",
			[solenoid_output_id(2)],
			["switch.matrix-37", "switch.matrix-38", "switch.matrix-73"],
			"With the centre \"D\" drop target down, a ball shot at the bank enters a subway under the "
			"playfield. Two rollovers track it on the way through — Subway Enter 1 (switch 37) at the "
			"start and Subway Enter 2 (switch 38) part way along, both marked †Located Under Playfield — "
			"and it comes to rest in the Left Popper, an opto-sensed vertical up-kicker (switch 73, "
			"solenoid 2, assembly A-16580) that fires it onto a habitrail. Pinned PinMAME's own ball "
			"simulator sequences Subway, Subway, Subway Popper, Subway Habitrail in exactly that order, "
			"and gates entry on the \"D\" target being down through its custom key condition.",
			[
				("enter", "Subway entered", ["switch.matrix-37"], "First under-playfield rollover after the D target."),
				("midway", "Subway midway", ["switch.matrix-38"], "Second under-playfield rollover."),
				("held", "Ball in the left popper", ["switch.matrix-73"], "Ball resting on the subway popper opto, waiting for solenoid 2."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16580",
		),
		mechanism(
			"mechanism.right-popper",
			"Sniper Tower right popper",
			"kicker",
			[solenoid_output_id(3)],
			["switch.matrix-74"],
			"A ball resting on the Right Popper opto (switch 74) at the top right of the playfield is "
			"kicked back into play by solenoid 3 (A-15769) onto a wire ramp. Pinned PinMAME's ball "
			"simulator names this shot the Sniper Tower and routes its exit to the left inlane.",
			[("held", "Ball in the right popper", ["switch.matrix-74"], "Right popper opto.")],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15769",
		),
		mechanism(
			"mechanism.left-ramp-diverter",
			"Left ramp diverter to the Deadworld globe",
			"diverter",
			[solenoid_output_id(11)],
			["switch.matrix-67", "switch.matrix-63", "switch.matrix-64"],
			"The plastic orbit ramp that runs up the left side and round past the globe has a "
			"solenoid-operated diverter at the top (solenoid 11, A-16802, under the playfield). With the "
			"diverter at rest the ball carries on through Left Ramp Exit (switch 64); with the diverter "
			"energised it is sent through Left Ramp To Lock (switch 63) and onto the Deadworld globe. "
			"Pinned PinMAME's ball simulator encodes exactly that branch, with sDiverter selecting the "
			"\"Towards Planet\" alternative from the Left Ramp state. Which opto reports the ramp "
			"entrance differs between ROM revisions; see conflict.l1-era-switch-fitment.",
			[
				("entered", "Ramp entered", ["switch.matrix-67"], "Ramp-entrance opto on the production machine."),
				("to-lock", "Diverted to the globe", ["switch.matrix-63"], "Diverter energised: the ball is on its way to the Deadworld globe."),
				("exit", "Ramp exit", ["switch.matrix-64"], "Diverter at rest: the ball completes the orbit."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16802",
		),
		mechanism(
			"mechanism.trough",
			"Six-ball trough and ball release",
			"kicker",
			[solenoid_output_id(13)],
			[
				"switch.matrix-81", "switch.matrix-82", "switch.matrix-83", "switch.matrix-84",
				"switch.matrix-85", "switch.matrix-86", "switch.matrix-87",
			],
			"Six balls rest on trough optos 81-86, with Trough 6 (86) at the eject end nearest the right "
			"shooter lane and Trough 1 (81) at the drain entrance. Solenoid 13 (AE-26-1500, assembly "
			"A-16765) ejects the ball resting on 86, and Top Trough (87) reports the ball leaving; the "
			"retained script's handler kicks from 86 and pulses 87 in the same event. All seven positions "
			"carry an A-16926 phototransistor and A-16927 LED per the switch-locations parts list, so a "
			"recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough 1 (drain entrance)", ["switch.matrix-81"], "Ball furthest from the eject coil."),
				("ball-2", "Trough 2", ["switch.matrix-82"], "Second trough position."),
				("ball-3", "Trough 3", ["switch.matrix-83"], "Third trough position."),
				("ball-4", "Trough 4", ["switch.matrix-84"], "Fourth trough position."),
				("ball-5", "Trough 5", ["switch.matrix-85"], "Fifth trough position."),
				("ball-6", "Trough 6 (eject position)", ["switch.matrix-86"], "Ball nearest the eject coil."),
				("eject", "Top trough", ["switch.matrix-87"], "Opto pulsed as the ejected ball leaves the trough."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16765",
		),
		mechanism(
			"mechanism.shooter-lanes",
			"Right and left shooter lanes",
			"kicker",
			[solenoid_output_id(8), solenoid_output_id(9)],
			["switch.matrix-41", "switch.matrix-15"],
			"Judge Dredd has two ball-launch lanes. The right shooter lane is the normal one: a ball "
			"ejected from the trough rests on switch 41 and solenoid 8 (A-14525) launches it. The left "
			"shoot lane is a second, mode-specific launcher — the retained script calls solenoid 9 "
			"(A-16936) the KickBack and the manual calls it Left Shooter — fed from the Air Raid ramp "
			"habitrail and resting on switch 15.",
			[
				("right", "Ball in the right shooter lane", ["switch.matrix-41"], "Normal launch position."),
				("left", "Ball in the left shoot lane", ["switch.matrix-15"], "Second launcher fed from the Air Raid habitrail."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[solenoid_output_id(15), solenoid_output_id(16)],
			["switch.matrix-51", "switch.matrix-52"],
			"Each slingshot assembly (A-14369-L and A-14369-R) carries a kick switch (SW-1A-114) and a "
			"separate score switch (SW-1A-120), which is what the \"(2)\" printed in matrix cells 51 and "
			"52 records; both switches feed the one matrix address. The retained script's slingshot "
			"handlers pulse 51 and 52 and fire coils 15 and 16 in the same event.",
			[
				("left", "Left slingshot", ["switch.matrix-51"], "Left slingshot, kick and score switches."),
				("right", "Right slingshot", ["switch.matrix-52"], "Right slingshot, kick and score switches."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14369-L",
		),
		mechanism(
			"mechanism.captive-balls",
			"Three-switch captive ball",
			"other",
			[],
			["switch.matrix-26", "switch.matrix-53", "switch.matrix-68"],
			"A captive-ball lane on the right side of the playfield is instrumented at three depths: "
			"Captive Ball 1 (switch 26) nearest the player, Captive Ball 2 (switch 53) and Captive Ball 3 "
			"(switch 68) furthest in. Harder shots push the captive ball deeper and register more of the "
			"three in sequence, which is exactly how pinned PinMAME's ball simulator chains them "
			"(Captive Ball -, Captive Ball /, Captive Ball |). Switches 26 and 53 are 5647-12693-19 "
			"rollovers and 68 is an A-14227-15 target switch; none of the three is an opto.",
			[
				("shallow", "Captive ball 1", ["switch.matrix-26"], "Nearest switch, registered by the weakest scoring shot."),
				("middle", "Captive ball 2", ["switch.matrix-53"], "Middle switch."),
				("deep", "Captive ball 3", ["switch.matrix-68"], "Deepest switch, registered only by a full-strength shot."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.three-bank-targets",
			"Advance Crime three-bank standup targets",
			"other",
			[],
			["switch.matrix-18"],
			"Three standup targets stacked vertically on the right of the playfield share the single "
			"matrix address 18. The manual's own switch-location diagram draws the 18 callout three times "
			"against one A-14227-15 part number, and the retained script instantiates three separate hit "
			"targets that all report public switch 18. A recreation therefore needs three physical "
			"targets but only one controller input.",
			[("hit", "Any of the three targets struck", ["switch.matrix-18"], "All three targets report the same address.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-14227-15",
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[solenoid_output_id(45), solenoid_output_id(46), solenoid_output_id(47), solenoid_output_id(48)],
			["switch.flipper-111", "switch.flipper-112", "switch.flipper-113", "switch.flipper-114"],
			"Two FL-11629 flippers on Fliptronic circuits (A-15205-R-2 right, A-15205-L-2 left). Each has "
			"a separate power and hold winding: the ROM energises the power winding on the cabinet button "
			"opto (112 right, 114 left), then drops to the hold winding once the end-of-stroke leaf switch "
			"(111 right, 113 left) closes. The retained table runs Const UseSolenoids = 2, so the ROM "
			"drives the coils directly rather than the table simulating them.",
			[
				("right", "Lower right flipper", ["switch.flipper-111", "switch.flipper-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.flipper-113", "switch.flipper-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 right with A-15205-L-2 left",
		),
		mechanism(
			"mechanism.upper-flippers",
			"Upper flipper pair",
			"other",
			[solenoid_output_id(33), solenoid_output_id(34), solenoid_output_id(35), solenoid_output_id(36)],
			["switch.flipper-115", "switch.flipper-116", "switch.flipper-117", "switch.flipper-118"],
			"Judge Dredd is a four-flipper wide-body: an upper right flipper (A-15205-R) sits below the "
			"Sniper Tower shot and an upper left flipper (A-16976-L) beside the Deadworld globe. Both are "
			"fitted, so all four upper Fliptronic switch positions and all four upper flipper solenoid "
			"addresses carry real hardware and none is repurposed. The upper right flipper is the one "
			"circuit that uses a different coil, FL-11630 (Red) rather than FL-11629 (Blue). Pinned "
			"PinMAME agrees: jdGameData declares FLIP_SW(FLIP_L|FLIP_U) and FLIP_SOL(FLIP_L|FLIP_U), so "
			"core_getSol routes public 33/34 through the upper-right coil path and 35/36 through the "
			"upper-left path, and the retained script binds sURFlipper to its right-hand upper flipper "
			"object and sULFlipper to its left-hand one.",
			[
				("right", "Upper right flipper", ["switch.flipper-115", "switch.flipper-116"], "Button opto 116 and end-of-stroke switch 115."),
				("left", "Upper left flipper", ["switch.flipper-117", "switch.flipper-118"], "Button opto 118 and end-of-stroke switch 117."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R upper right with A-16976-L upper left",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-top-trough",
			"kind": "pulse",
			"source": solenoid_output_id(13),
			"destination": "switch.matrix-87",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.trip-drop-target-d",
			"kind": "direct",
			"source": solenoid_output_id(10),
			"destination": "switch.matrix-56",
			"provenance": provenance(VPX_SCRIPT_SOURCE, CORE_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.column-6-7-optos-not-all-normalized",
			"path": "inputs[binding.device=61,71,77]",
			"description": (
				"The printed switch matrix (2-42) fills the cells for 61 Globe Position #1, 71 Magnet "
				"Over Ring and 77 Globe Position #2 with the same \"Opto, Typically Closed\" halftone it "
				"uses for the ten ramp and popper optos beside them, and a mechanical connected-component "
				"sweep of all 64 cells at 600 dpi confirms the shading is present on exactly those "
				"thirteen cells and absent everywhere else. For 71 the switch-locations parts list agrees "
				"independently, giving an A-14231 LED and A-14232 phototransistor pair. Pinned PinMAME "
				"treats them differently: recomputing jdGameData's inverted-switch mask "
				"{0x00,0x00,0x00,0x02,0x00,0xf8,0x6e,0x3e,0x7f,0x00,0x00,0x00} bit by bit gives normalized "
				"addresses 32, 54-58, 62, 63, 64, 66, 67, 72, 73, 74, 75, 76 and 81-87, which covers ten of "
				"the thirteen shaded cells but leaves 61, 71 and 77 uninverted. The manual is "
				"physical-construction ground truth and pinned PinMAME is emulator-normalization ground "
				"truth, and the two disagree about whether a recreation must invert the state it reports "
				"for these three. 61 and 77 carry an A-16598 part number that discloses no construction "
				"either way, which weakens the manual side for those two but not for 71. Resolving it needs "
				"a LibPinMAME harness trace against a legal jd_l1 or jd_l7 ROM observing the idle public "
				"state of 61, 71 and 77 with no ball on the globe and the crane parked. "
				"Resolution path: run the repository's LibPinMAME gameplay harness against a legal jd_l1 "
				"or jd_l7 ROM with 61, 71 and 77 watched, reading their idle state with no ball on the "
				"globe and the crane parked and their transitions as each is made; independently, a "
				"photograph or parts breakdown of the A-16598 assembly would fix construction for 61 and "
				"77, which the printed part number alone does not disclose. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE, MANUAL_SUPPORT_SOURCE],
		},
		{
			"id": "conflict.judge-drop-targets-normalized-without-opto-evidence",
			"path": "inputs[binding.device=54,55,56,57,58]",
			"description": (
				"Pinned PinMAME's jdGameData inverted-switch mask normalizes the five JUDGE drop-target "
				"switches 54-58 (column 5 = 0xf8, bits 3-7), which is the treatment it gives optos "
				"elsewhere on this machine. No source read here discloses opto construction for them: the "
				"switch-locations parts list gives a single assembly number A-16486 with no LED or "
				"phototransistor breakout, unlike every genuine opto row on the same page, and the printed "
				"switch matrix leaves all five cells unshaded. Pinned PinMAME's own jd_handleMech asserts "
				"each of these switches while its target is DOWN, which is the sense a normally-open "
				"target switch would report and therefore the opposite of what a normally-closed opto plus "
				"emulator inversion would produce. Either the A-16486 target really is an opto assembly "
				"whose construction this manual does not spell out, or the mask's column 5 is wrong. "
				"Resolving it needs a LibPinMAME harness trace observing the idle public state of 54-58 "
				"with the bank reset, or a photograph of an A-16486 target assembly. "
				"Resolution path: run the repository's LibPinMAME gameplay harness against a legal jd_l1 "
				"or jd_l7 ROM with 54-58 watched, reading them with the JUDGE bank reset and again with "
				"each target knocked down, or obtain a photograph of an A-16486 target assembly showing "
				"whether it carries a discrete LED and phototransistor pair. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.l1-era-switch-fitment",
			"path": "inputs[binding.device=28,32,65]",
			"description": (
				"Three matrix addresses are printed \"Not Used\" with a blank part number on both the "
				"switch matrix (2-42) and the switch-locations parts list (2-43), yet the location diagram "
				"printed on that same parts-list page still draws a callout for each of them: 28 on the "
				"crane / Magnet Over Ring assembly, 32 on the plastic orbit ramp beside the globe, and 65 "
				"on the right-hand ramp. The other six \"Not Used\" addresses (45, 46, 47, 48, 78, 88) have "
				"no callout, so this is not a habit of the drawing. Conversely item 67, a fitted opto with "
				"a full A-14231/A-14232 part pair, has no callout anywhere in the diagram. The retained "
				"known-working table binds the L-1 ROM and drives all three: it asserts 28 while the Globe "
				"Magnet holds a ball, pulses 65 from a right-ramp trigger whose own comment reads \"Opto "
				"Right Ramp Entrace (Not used?)\", and pulses 32 from its ramp-entrance trigger under a "
				"commented block recording that the ramp opto's address \"Position changed between L1 and "
				"L7 ROM Revisions\" — SW32 at the ramp entrance for L-1, SW67 near the top of the ramp for "
				"L-7. Pinned PinMAME corroborates 32 twice over: jdGameData's inverted-switch mask "
				"normalizes address 32 as though an opto were fitted there, while jd.c's own #define block "
				"marks 32 unused and names 67 swLRampEnt. The coherent reading is that the location "
				"drawing and the L-1 firmware come from an earlier design revision in which 28, 32 and 65 "
				"were fitted and 67 was not, and that production deleted them and updated the parts list "
				"but not the drawing. That reading is not proved, and it matters to an author: a "
				"recreation bound to jd_l1 must decide whether to wire three addresses the production "
				"manual says do not exist. Resolving it needs a photograph of an unrestored production "
				"playfield at those three positions, or a LibPinMAME trace comparing what jd_l1 and jd_l7 "
				"actually read. "
				"Resolution path: a photograph of an unrestored production playfield at the crane / Magnet "
				"Over Ring, orbit-ramp and right-ramp positions showing whether a switch body is fitted at "
				"each, together with a LibPinMAME gameplay-harness trace run twice — once on a legal jd_l1 "
				"ROM and once on jd_l7 — watching 28, 32, 65 and 67 under the same driven inputs so the "
				"revision difference is observed rather than inferred. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.gi-string-order-script-vs-manual",
			"path": "outputs[binding.group=pinmame.output.gi]",
			"description": (
				"Pinned PinMAME publishes the five general-illumination strings as zero-based addresses "
				"0-4 taken from the five low bits of WPC_GILAMPS in order (src/wpc/wpc.c), and the "
				"repository's WPC-DCS controller profile records that public address N is the manual's "
				"printed string N+1. The manual identifies its five printed strings by wire colour: "
				"String 1 Wht-Brn, String 2 Wht-Org, String 3 Wht-Yel, String 4 Wht-Grn, String 5 Wht-Vio. "
				"The retained known-working table binds public GI 0 through 4 to collections it names "
				"GIstring1 through GIstring5 and annotates them, in that order, wht/vio, wht/grn, wht/yel, "
				"wht/org and wht/brn — the printed order reversed, agreeing only on the self-symmetric "
				"middle string. The two claims cannot both be right. Emitter coordinates in this "
				"definition follow the script's runtime binding, because a known-working table is the "
				"runtime authority for what each public address actually lights, while the bulb types, "
				"connector pins and wire colours follow the manual under the profile's printed-order rule; "
				"if the script's annotation is correct then those two halves are attached to each other "
				"wrongly. Two further details fit neither reading cleanly: the table's collection for "
				"public GI 4 contains backglass objects only, while the manual gives printed String 5 a "
				"playfield drive connection and no backbox column, and the table's collection for public "
				"GI 3 contains two playfield objects and no backglass, while the manual gives both "
				"candidate strings entries in both columns. Resolving it needs a LibPinMAME harness trace "
				"driving each GI address in turn against a legal ROM, or a photograph of the J120/J121 "
				"harness on a real machine. "
				"Resolution path: run the machine's own general-illumination test on an unrestored unit and "
				"record which of the five printed wire colours (Wht-Brn J-120-7, Wht-Org J-120-8, Wht-Yel "
				"J-120-9, Wht-Grn J-120-10, Wht-Vio J-120-11 on printed 2-44) lights at each step, since "
				"printed 3-10 draws one unnumbered representative string and cannot say which triac serves "
				"which string; pairing that against a LibPinMAME harness trace driving public GI 0-4 in "
				"turn on a legal jd_l1 or jd_l7 ROM closes the mapping from both ends. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE],
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
			"id": MACHINE_ID,
			"name": "Judge Dredd",
			"manufacturer": "Bally",
			"year": 1993,
			"kind": "physical_pinball",
			"playfield": {
				"width": PLAYFIELD_WIDTH,
				"height": PLAYFIELD_HEIGHT,
				"units": "vpx",
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
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
				"spatial_placement": "conflicted",
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
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Judge Dredd device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	omitted_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			omitted_inputs.append(address)
		elif spatial["status"] == "not_applicable":
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
		spatial = device.get("spatial")
		if spatial is not None and spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])

	projections = [
		{"group": "pinmame.input.switch", "address": address, "reason": reason}
		for address, reason in sorted(SWITCH_PROJECTIONS.items())
	] + [
		{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
		for address, reason in sorted(SOLENOID_PROJECTIONS.items())
	]

	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "partial",
		"blockers": [
			"Lamp 83 (Drain Shield) is printed with a quantity of two and drawn twice in the manual's "
			"own lamp-location diagram, once each side of the drain. The retained table models a single "
			"Light object for the address, sitting almost exactly midway between the two printed "
			"positions, so it is the arithmetic midpoint of the two real bulbs rather than either of "
			"them. Neither bulb has a usable coordinate and the address carries no placement.",
			"Public GI address 4 has no playfield emitter coordinate: the retained table's collection "
			"for that address contains backglass objects only, while the manual gives its printed "
			"string a playfield drive connection. This is entangled with "
			"conflict.gi-string-order-script-vs-manual, which is unresolved.",
			"Matrix positions 28, 32 and 65 carry no spatial record at all because whether anything is "
			"fitted at those addresses is itself unresolved; see conflict.l1-era-switch-fitment.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/1093; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/judge-dredd-1993/extracted-vpxtool.manifest.json",
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
		"projections": projections,
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.judge-dredd.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/judge-dredd-1993/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"L<nn>g / l<nn>g co-located glow doubles and L<nn>f / l<nn>f co-located flare Flashers stacked on each matrix lamp",
			"l48r, l61r, l61ar, l68r, L71r-L75r reflection Flashers offset from their own lamp",
			"f17g-f20g, F18g-F24a-style flasher glow doubles",
			"f21bloom, f22bloom, f25bloom, f26bloom, f27bloom screen-space bloom Flashers, all five sharing one centre-of-playfield coordinate",
			"F25Bulb, F25aBulb, F27Bulb, F27aBulb bulb-mesh Primitives at raw coordinates outside the playfield bounds",
			"bg_b_*, bg_o_*, bg_y_*, bg_g_*, bg_s* backglass Flashers at negative raw y",
			"GI_Bulbs Bulb1-Bulb15 bulb-mesh Primitives",
			"sw<nn>o / sw<nn>p / sw<nn>p_off / sw<nn>prim / sw<nn>prim_off target-visual Primitives",
			"L83, the single retained Light for lamp 83, which is the arithmetic midpoint of the two printed Drain Shield bulbs",
		],
		"unresolved": [
			{"group": "pinmame.output.lamp", "address": 83, "reason": "Two printed bulbs, and the only retained object is their midpoint."},
			{"group": "pinmame.output.gi", "address": 4, "reason": "No playfield emitter in the retained table's collection for this address."},
			{"group": "pinmame.input.switch", "address": 28, "reason": "Fitment unresolved; see conflict.l1-era-switch-fitment."},
			{"group": "pinmame.input.switch", "address": 32, "reason": "Fitment unresolved; see conflict.l1-era-switch-fitment."},
			{"group": "pinmame.input.switch", "address": 65, "reason": "Fitment unresolved; see conflict.l1-era-switch-fitment."},
		],
		"omitted_spatial_inputs": sorted(omitted_inputs),
		"omitted_spatial_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Judge Dredd (Bally, 1993) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record lives at "
		"`machines/partial/bally/judge-dredd-1993.json` and stays `partial`: five addresses have no "
		"placement and four unresolved conflicts remain. See the promotion decision below.",
		"",
		"The matching source is the retained known-working `Judge Dredd (Bally 1993) VPW v1.1.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded "
		f"script at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality "
		f"authority. Exact playfield bounds are `{TABLE_BOUNDS}` — this is a wide-body Superpin, so every "
		"canonical coordinate is x/1093 and y/2162, rounded to at most six fractional places, and the "
		"952 divisor that standard-width WPC games use would stretch every x by about 15 percent.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Bally operations "
		"manual is the physical inventory, quantity, polarity and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- The retained manual PDF carries an Adobe Paper Capture OCR layer, but its output for every "
		"multi-column table in Sections 2 and 3 is scrambled. Every printed table used here was read "
		"from 300-600 dpi renders and transcribed by hand into "
		"`evidence/excerpts/bally.judge-dredd.1993/`.",
		"- Which switch-matrix cells carry the \"Opto, Typically Closed\" halftone was settled by a "
		"mechanical connected-component sweep of all 64 cells at 600 dpi, not by eye, and the result was "
		"cross-checked against the switch-locations parts list's independent LED/phototransistor "
		"disclosure. The two agree cell for cell.",
		"- Lamp bindings come from the retained script's `Lampz.MassAssign` table, which assigns the "
		"primary `L<nn>` Light plus co-located glow and flare doubles per address. Only the primary "
		"object supplies a coordinate. Addresses 38, 87 and 88 have no assignment at all, matching the "
		"manual, which prints them as cabinet button lamps with a blank bulb number.",
		"- Lamp 61 is printed `Extra Ball (2)` and drawn twice in the manual's location diagram; the "
		"retained table models it as two Lights far apart on the playfield, so it takes two placements. "
		"Lamp 83 is also printed with a quantity of two, but its single retained Light is the midpoint of "
		"the two printed positions and is therefore excluded rather than used.",
		"- Flasher placements match the manual's own playfield bulb counts address by address: one each "
		"for 17-20, two each for 21, 22, 24, 25 and 27, one each for 23 and 26, and none for 28, which "
		"the printed table gives blank Playfield columns and three backbox bulbs.",
		"- Several switches have no dedicated playfield object because the retained script and pinned "
		"PinMAME both derive their public state from a mechanism's own continuous position (the globe "
		"rotation counter, the crane arm counter) or from another device's event (the trough eject). "
		"Those are explicit documented projections onto the real table object that carries the "
		"underlying mechanism, never a centroid of other devices.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` "
		"with both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group'].rsplit('.', 1)[-1].title()} {entry['address']}: {entry['reason']}")
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
	lines.append(f"- Inputs with no spatial record at all: {len(report['omitted_spatial_inputs'])}")
	lines.append(f"- Outputs with no spatial record at all: {len(report['omitted_spatial_outputs'])}")
	lines += [
		"",
		"## Unresolved",
		"",
	]
	for entry in report["unresolved"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Promotion to `author_ready` is refused. Five addresses have no placement — lamp 83, GI 4 and "
		"switch positions 28, 32 and 65 — and the definition carries four unresolved conflicts: three "
		"printed opto cells that pinned PinMAME does not normalize, five drop-target switches that it "
		"does normalize with no opto evidence behind them, three switch addresses whose fitment the "
		"manual contradicts itself about, and a general-illumination string order on which the manual "
		"and the retained known-working script disagree outright. `coverage.status` stays `partial` "
		"with `coverage.missing = [\"polarity\", \"spatial_placement\", \"unresolved_conflicts\"]`. The "
		"cheapest route to closing three of the four is a LibPinMAME gameplay-harness trace against a "
		"legal jd_l1 and jd_l7 ROM: the idle public state of 61/71/77 and 54-58 settles the two polarity "
		"conflicts, driving each GI address in turn settles the string order, and comparing what the two "
		"ROMs read at 28, 32 and 65 settles the fitment question.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Manual reading record, SHA-256 `{MANUAL_TRANSCRIPTION_SHA256}`, with the rendered page cache "
		"at `external:pinmame-manuals/rendered/bally.judge-dredd.1993/`.",
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
		raise RuntimeError(f"Stale Judge Dredd author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Judge Dredd definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Judge Dredd seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Judge Dredd definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Judge Dredd seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Judge Dredd spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Judge Dredd spatial review drifted from its deterministic curator: {markdown_path}")
	print("Judge Dredd definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Judge Dredd extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Judge Dredd retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
