"""Curate the physical Bally Twilight Zone (1993) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label,
wiring detail, and normalized coordinate as a literal, so regeneration reproduces the
canonical artifact byte-for-byte without reading the external evidence roots.
``--check`` refuses drift, and ``--regenerate`` is the only path that writes the
canonical definition and its pinned seed.
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
PARTIAL_PATH = ROOT / "machines/partial/bally/twilight-zone-1993.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/twilight-zone-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/twilight-zone-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/twilight-zone-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/twilight-zone-1993.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-fliptronic"
MANUAL_SOURCE = "manual.bally.twilight-zone.1993"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.twilight-zone.1993"
VPX_TABLE_SOURCE = "vpx-table.tz-2-4-5"
VPX_SCRIPT_SOURCE = "vpx-script.tz-2-4-5"
VPX_EXTRACTION_SOURCE = "vpx-extraction.tz-2-4-5"
# The complete operations manual from IPDB (the Internet Archive scan above lacks every even page), its amendment,
# the 2020 ninuzzu table (the ancestor of the 2.4.5 lineage, so not an independent table), and the ROM clock test.
MANUAL_IPDB_SOURCE = "manual.bally.twilight-zone.1993.ipdb-2684"
MANUAL_AMENDMENT_SOURCE = "manual-amendment.bally.twilight-zone.1993"
VPX_2020_TABLE_SOURCE = "vpx-table.tz-ninuzzu-2020"
VPX_2020_SCRIPT_SOURCE = "vpx-script.tz-ninuzzu-2020"
VPX_2020_EXTRACTION_SOURCE = "vpx-extraction.tz-ninuzzu-2020"
RUNTIME_CLOCK_SOURCE = "runtime.twilight-zone.clock-test"
RUNTIME_CLOCK_PATH = "evidence/runtime/wpc-fliptronic/twilight-zone-clock-test.json"
RUNTIME_CLOCK_MECH_SOURCE = "runtime.twilight-zone.clock-test-mech"
RUNTIME_CLOCK_MECH_PATH = "evidence/runtime/wpc-fliptronic/twilight-zone-clock-test-mech.json"
RUNTIME_LIBRARY_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"

MANUAL_IPDB_SHA256 = "b026feca0fe20a709a7224b49cdb7330586b041798f1a02193c53a00738fa105"
MANUAL_AMENDMENT_SHA256 = "36b83c898727d4215ec9157f1236a2a074374187a39f665d82efa8f39e95a856"
TABLE_2020_SHA256 = "cd98f8a152065b1fdbd6c79d7d5f5301e165a37963991b1ee9104f7db3e435ca"
SCRIPT_2020_SHA256 = "40f8ed5cffe1184be2d3ee7079aa698a980ae6f8e9284bb006a6203f3a15d9a7"
EXTRACTION_2020_RELATIVE_PATH = Path("bally/twilight-zone-1993/ninuzzu-2020/extracted-vpxtool")
EXTRACTION_2020_MANIFEST_RELATIVE_PATH = Path("bally/twilight-zone-1993/ninuzzu-2020/extracted-vpxtool.manifest.json")
EXTRACTION_2020_MANIFEST_SHA256 = "c957f063d5d3ffdc015a5997ff4a1b6eeb682351985ad36abc7aa85043940aeb"
EXTRACTION_2020_FILE_COUNT = 1568
EXTRACTION_2020_TOTAL_BYTES = 124437697
TABLE_2020_BOUNDS = "left=0 top=0 right=1093 bottom=2162"
BOUNDS_2020_X = 1093.0
BOUNDS_2020_Y = 2162.0

TABLE_SHA256 = "4fcca01a076591384caec5b06d4f58547299cbeae9fac2a67faa29cc5af0d814"
SCRIPT_SHA256 = "122ef6811ff2e6912593a28a75078a467e6d58dd208c98e313c82712aee2bc4e"
MANUAL_SHA256 = "66b657fda3803ac65dbf0ca89f31825a1a3f95b989b96b99ecea02f42e32be34"
MANUAL_TRANSCRIPTION_SHA256 = "022e91ceaedb44fdaf410cca90bfa534aa11c89fcd832dd2a0f94166c24de39a"
VPX_GEOMETRY_SHA256 = "dc8a49f6b1d1568ba9027af7453157039da05a08d6ffd2ac0a60c54940cb2f3a"
# Objects first used by the 2026-09-25 spatial repair, kept in a separate versioned file so the
# original geometry dump above stays byte-identical.
VPX_GEOMETRY_SUPPLEMENT_SHA256 = "d0ba08f21084d370b3924f3ab8d3fb164f1a9fd14cb1f6df1c33ab747b3ff7c3"
# A second supplement added after the third review (the right ramp diverter blade and the callout-05 measurement);
# both earlier geometry files stay byte-identical.
VPX_GEOMETRY_SUPPLEMENT_2_SHA256 = "1cab0a1ff393a96e2fa43e49ac31039e05280d462293c258ab91df042d6b1aff"
# A third supplement for the 2026-09-26 pass: the 2020 table's objects (normalized by that table's own bounds), the
# frame comparison between the two tables, and the least-squares fits of the page 2-53 and 2-50 drawings with every
# measured callout pixel and offset. The three earlier files stay byte-identical.
VPX_GEOMETRY_SUPPLEMENT_3_SHA256 = "f5560fd3d0cc5b7f940955c9d20848ede4fe815dc4a89092dcb4aabea1b329c5"

EXTRACTION_RELATIVE_PATH = Path("bally/twilight-zone-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/twilight-zone-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "6188e966e86cafeece592dfecf0603f8b3a16b7bc188d3b9ed876a2425d506c8"
EXTRACTION_FILE_COUNT = 3176
EXTRACTION_TOTAL_BYTES = 546282740

TABLE_BOUNDS = "left=0 top=0 right=1082.353 bottom=2164.706"
BOUNDS_X = 1082.353
BOUNDS_Y = 2164.706

DRIVER_IDS = (
	"tz_92", "tz_93", "tz_94ch", "tz_94h", "tz_d1", "tz_d2", "tz_d3", "tz_d4",
	"tz_f10", "tz_f100", "tz_f19", "tz_f50", "tz_f86", "tz_f97", "tz_h7", "tz_h8",
	"tz_i7", "tz_i8", "tz_ifpa", "tz_ifpa2", "tz_l1", "tz_l2", "tz_l3", "tz_l4",
	"tz_l5", "tz_la9", "tz_p3", "tz_p3d", "tz_p4", "tz_p5", "tz_pa1", "tz_pa2",
)
# All 32 driver rows in catalog/pinmame.json trace tz_92 (root) and share tzGameData;
# they are firmware/prototype/tournament revisions of one physical machine.
DRIVER_COMPATIBILITY = {
	"tz_92": ("identical", "Bally production 9.2 game ROM, the catalog root."),
	"tz_93": ("identical", "9.3 revision; corrects an LED ghosting display artifact only."),
	"tz_94ch": ("identical", "9.4CH coin-play revision. The retained known-working VPX script binds cGameName = \"tz_94ch\" for the default (Romset=0) selection."),
	"tz_94h": ("identical", "9.4H revision. The retained known-working VPX script's alternate (Romset=1) selection binds cGameName = \"tz_94h\"."),
	"tz_d1": ("identical", "D-1 LED ghost-fix revision, paired with the L-1 game ROM's sound set."),
	"tz_d2": ("identical", "D-2 LED ghost-fix revision."),
	"tz_d3": ("identical", "D-3 LED ghost-fix revision."),
	"tz_d4": ("identical", "D-4 LED ghost-fix revision."),
	"tz_f10": ("compatible", "FreeWPC 0.10 community firmware for the same physical hardware."),
	"tz_f100": ("compatible", "FreeWPC 1.00 community firmware for the same physical hardware."),
	"tz_f19": ("compatible", "FreeWPC 0.19 community firmware for the same physical hardware."),
	"tz_f50": ("compatible", "FreeWPC 0.50 community firmware for the same physical hardware."),
	"tz_f86": ("compatible", "FreeWPC 0.86 community firmware for the same physical hardware."),
	"tz_f97": ("compatible", "FreeWPC 0.97 community firmware for the same physical hardware."),
	"tz_h7": ("identical", "H-7 revision."),
	"tz_h8": ("identical", "H-8 revision."),
	"tz_i7": ("identical", "I-7 LED ghost-fix revision, paired with H-7's sound set."),
	"tz_i8": ("identical", "I-8 LED ghost-fix revision, paired with H-8's sound set."),
	"tz_ifpa": ("identical", "IFPA tournament-rules revision."),
	"tz_ifpa2": ("identical", "IFPA tournament-rules LED ghost-fix revision."),
	"tz_l1": ("identical", "L-1 revision."),
	"tz_l2": ("identical", "L-2 revision. The retained vpxtable_scripts/vpx-standalone-scripts corpora both target this revision (Twilight Zone (Bally 1993) VPW Edition v1.0.2.vbs and Twilight Zone_VPX_2.1.vbs)."),
	"tz_l3": ("identical", "L-3 revision."),
	"tz_l4": ("identical", "L-4 revision."),
	"tz_l5": ("identical", "L-5 revision, the last standard production ROM."),
	"tz_la9": ("identical", "LA-9 PAPA tournament version 9.0, a specialised tournament revision of 9.2."),
	"tz_p3": ("identical", "P-3 prototype revision."),
	"tz_p3d": ("identical", "P-3 LED ghost-fix prototype revision."),
	"tz_p4": ("identical", "P-4 prototype revision."),
	"tz_p5": ("identical", "P-5 LED ghost-fix prototype revision."),
	"tz_pa1": ("identical", "PA-1 prototype revision, its own sound ROM set."),
	"tz_pa2": ("identical", "PA-2 LED ghost-fix prototype revision, sharing PA-1's sound ROM set."),
}

# --- Switch matrix (tz.c #defines; manual page 2-51 "Switch Locations (Continued)"
# confirms labels for 34-98; the first Switch Locations page, 2-50, covering items 1-33,
# is absent from the Internet Archive scan and is read from the complete IPDB copy).
SWITCH_LABELS = {
	11: "Right Inlane", 12: "Right Outlane", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Right Trough", 16: "Center Trough", 17: "Left Trough", 18: "Outhole",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In Button",
	25: "Far Left Trough", 26: "Trough Proximity (Powerball Detect)", 27: "Ball Shooter", 28: "Rocket Kicker",
	31: "Left Jet Bumper", 32: "Right Jet Bumper", 33: "Lower Jet Bumper",
	34: "Left Slingshot", 35: "Right Slingshot", 36: "Left Outlane", 37: "Left Inlane 1", 38: "Left Inlane 2",
	41: "Dead End", 42: "Mini-Playfield Top Hole", 43: "Player Piano", 44: "Mini-Playfield Enter",
	45: "Mini-Playfield Left", 46: "Mini-Playfield Right", 47: "Clock Millions", 48: "Lower Left 5 Million",
	51: "Gumball Popper Lane", 52: "Hitchhiker", 53: "Left Ramp Enter", 54: "Left Ramp",
	55: "Gumball Geneva", 56: "Gumball Exit", 57: "Slot Proximity", 58: "Slot Kickout",
	61: "Lower Skill Shot", 62: "Center Skill Shot", 63: "Upper Skill Shot",
	64: "Upper Right 5 Million", 65: "Power Payoff", 66: "Middle Right 5 Million 1", 67: "Middle Right 5 Million 2",
	68: "Lower Right 5 Million",
	72: "Auto-Fire Kicker", 73: "Right Ramp Enter", 74: "Gumball Popper",
	75: "Mini-Playfield Top", 76: "Mini-Playfield Exit", 77: "Middle Left 5 Million", 78: "Upper Left 5 Million",
	81: "Lower Right Magnet", 83: "Left Magnet", 84: "Lock Center",
	85: "Lock Upper", 87: "Gumball Enter", 88: "Lock Lower",
	91: "Clock 15 Minutes", 92: "Clock 0 Minutes", 93: "Clock 45 Minutes", 94: "Clock 30 Minutes",
	95: "Clock Hour 1", 96: "Clock Hour 2", 97: "Clock Hour 3", 98: "Clock Hour 4",
}
# Confirmed "Not Used" on the printed switch-locations page (2-51): no switch part
# number and no opto assembly at all, the strongest "not fitted" signature the manual
# uses.
UNUSED_MATRIX_ADDRESSES = {71, 82, 86}
# Page 2-50 of the complete IPDB manual prints matrix position 24 "Always Closed" in the
# switch matrix and in the switch list (part column "----"); pinned wpc.c closes the same
# position at machine init. tz.c has no #define for it, so it is not in SWITCH_LABELS.
ALWAYS_CLOSED_SWITCH = 24
ALWAYS_CLOSED_NOTE = (
	"Printed switch-matrix drive column 2, return row 4. Page 2-50 of the complete IPDB manual prints this position "
	"\"Always Closed\" both in the switch matrix and in the switch list, where its part column reads \"----\" "
	"instead of a part number: a permanently closed link, not a switch, that the WPC ROM reads as a closed reference "
	"contact to prove the matrix is connected. Pinned wpc.c closes the same position at machine init "
	"(coreGlobals.swMatrix[2] |= 0x08, \"Always closed switch\"), so a host never needs to drive it. tz.c defines "
	"no symbol for it. Column 2 is Green-Red J206-2 from driver U20-17; row 4 is White-Yellow J208-4 into receiver "
	"U18-7 (page 2-50 column and row headings)."
)
UNUSED_MATRIX_LABELS = {71: "Big Kick", 82: "Upper Right Magnet", 86: "Clock Lane"}
# Manual page 2-51: printed "A-14231 (LED) / A-14232 (Trans)" opto-pair construction.
OPTO_SWITCHES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87}
# tzGameData's inverted-switch mask, verbatim: {Coin=0,c1..c6=0,c7=0x3f,c8=0x7f,c9=0,c10=0,Cab=0,Cust=0xff}.
# Column 7 (71-78) bits 0-5 => 71-76 inverted; column 8 (81-88) bits 0-6 => 81-87
# inverted; Cust (internal column 12 = CORE_CUSTSWCOL, public 121-128) is fully inverted, while column 9
# (public 91-98) is 0x00. Columns 1-6 (11-68) are 0x00, so none of those addresses are emulator-normalized
# regardless of manual confirmation. The eight clock optos are handled separately (CLOCK_OPTO_PUBLIC below).
PINMAME_NORMALIZED_OPTO_SWITCHES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87}
PULSED_SWITCHES = {11, 12, 25, 27, 31, 32, 33, 36, 37, 38, 42, 43, 44, 45, 46, 51, 52, 53, 54, 56, 61, 62, 63, 73, 75, 76, 117}

# Manual page 2-51 part numbers, address -> (assembly_or_switch_part, note)
SWITCH_PARTS = {
	34: "SW-1A-114 (kicker) / SW-1A-120 (score)", 35: "SW-1A-114 (kicker) / SW-1A-120 (score)",
	36: "5647-12693-19", 37: "5647-12693-19", 38: "5647-12693-19",
	41: "5647-12693-13", 42: "5647-12693-13", 43: "5647-12693-13", 44: "5647-12693-19",
	45: "5647-12693-11", 46: "5647-12693-11", 47: "A-15658-2", 48: "A-14691-6",
	51: "5647-12693-13", 52: "5647-12693-19", 53: "5647-12693-11", 54: "5647-12693-21",
	55: "5647-12393-08", 56: "5647-12693-19", 57: "A-16535", 58: "5647-12693-25",
	61: "5647-12693-57", 62: "5647-12693-53", 63: "5647-12693-54",
	64: "A-14691-6", 65: "A-14691-4", 66: "A-14691-6", 67: "A-14691-6", 68: "A-15658-6",
	72: "A-14231 (LED) / A-14232 (Trans)", 73: "A-14231 (LED) / A-14232 (Trans)",
	74: "A-16908 (LED) / A-16909 (Trans)", 75: "A-14231 (LED) / A-14232 (Trans)",
	76: "A-14231 (LED) / A-14232 (Trans)", 77: "A-14691-6", 78: "A-14691-6",
	81: "A-14231 (LED) / A-14232 (Trans)", 83: "A-14231 (LED) / A-14232 (Trans)",
	84: "A-14231 (LED) / A-14232 (Trans)", 85: "A-14231 (LED) / A-14232 (Trans)",
	87: "A-14231 (LED) / A-14232 (Trans)", 88: "5647-12133-11",
	91: "A-16220", 92: "A-16220", 93: "A-16220", 94: "A-16220",
	95: "A-16219", 96: "A-16219", 97: "A-16219", 98: "A-16219",
}
# Page 2-50 of the complete IPDB copy: switch list items 11-33 ("Item", "Switch Part #", "Where Used"), as printed.
SWITCH_PARTS_2_50 = {
	11: ("5647-12693-19", "Right Inlane"), 12: ("5647-12693-19", "Right Outlane"),
	13: ("20-9663-1", "Start Button"), 14: ("A-15361", "*PlumbBob Tilt"), 15: ("5647-12693-08", "Right Trough"),
	16: ("5647-09957-00", "Center Trough"), 17: ("5647-09957-00", "Left Trough"), 18: ("5647-12133-12", "Outhole"),
	21: ("27-1066", "*Slam Tilt"), 22: ("5643-09288-00", "*Coin Door Closed"), 23: ("20-9663-9", "Buy-In Button"),
	25: ("5647-09957-00", "Far Left Trough"), 26: ("A-16528", "\u2020Trough Proximity"),
	27: ("5647-12693-04", "Ball Shooter"), 28: ("5647-12693-55", "Rocket Kicker"),
	31: ("SW-11A-37", "Left Jet Bumper"), 32: ("SW-11A-37", "Right Jet Bumper"), 33: ("SW-11A-37", "Lower Jet Bumper"),
}
# Page 2-50 switch-matrix headings: column -> (wire, CPU connector, column driver pin), row -> (wire, connector, receiver).
MATRIX_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"), 3: ("Green-Orange", "J206-3", "U20-16"),
	4: ("Green-Yellow", "J206-4", "U20-15"), 5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
MATRIX_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"), 3: ("White-Orange", "J208-3", "U18-5"),
	4: ("White-Yellow", "J208-4", "U18-7"), 5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
}
# Manual Amendment 16-50020-AMD-1 (page 3, entry for page 2-51) supersedes the printed part of switch 61.
AMENDED_SWITCH_PARTS = {61: "5647-12693-32", 74: "A-14231 (LED) / A-14232 (Trans)"}
AMENDMENT_NOTES = {
	61: (
		" Page 2-51 prints part 5647-12693-32; Manual Amendment 16-50020-AMD-1 changes it to 5647-12693-57 "
		"(\"Switch 61 changed to 5647-12693-57.\", its entry for page 2-51), the part recorded here."
	),
	74: (
		" Page 2-51 prints A-14231 (LED) / A-14232 (Trans), as does the Ball Popper Assembly A-16312 (page 2-25, "
		"items 15 and 14; its coil AE-23-800 is solenoid 4's, Gumball Popper). Manual Amendment 16-50020-AMD-1 "
		"changes that assembly's item 14 to \"A-16909 Opto Photo Transistor Assembly\" and item 15 to \"A-16908 Opto "
		"LED Assembly\" (its entry for page 2-25), the parts recorded here; it has no page 2-51 entry for switch 74."
	),
	57: (
		" Manual Amendment 16-50020-AMD-1 adds the part to the Lower Playfield Parts list (its entry for page 2-47, "
		"item 12a): \"A-16535 Ramp Prox Opto sensor Assembly\"."
	),
}
# Proximity-sensor assemblies (not a leaf switch, not an A-14231/A-14232 opto pair): switch_type "other", as on
# the Star Trek: The Next Generation record's return-lane proximity sensors.
PROXIMITY_SWITCHES = {57}
# Script-derived label kept as an alias where the printed name replaced it.
SWITCH_LABEL_ALIASES = {27: "Shooter Lane"}


def matrix_wiring(column: int, row: int) -> dict[str, str]:
	drive_wire, drive_connection, driver = MATRIX_COLUMN_WIRING[column]
	return_wire, return_connection, receiver = MATRIX_ROW_WIRING[row]
	return {
		"board": "WPC CPU board",
		"drive_connection": drive_connection,
		"drive_wire": drive_wire,
		"return_component": f"column driver {driver}; row receiver {receiver}",
		"return_connection": return_connection,
		"return_wire": return_wire,
	}


# Switch-list legend (page 2-51): a dagger marks the underside of the playfield, "*" a switch not shown on the
# diagram; page 2-50 marks 26 with the dagger and 14, 21, 22 with the asterisk.
UNDERSIDE_SWITCHES = {26, 55, 57, 58}
NOT_SHOWN_SWITCHES = {14, 21, 22}

# The eight clock optos. Pages 1-18 and 2-50 print them as a "9th column" numbered 91-98, but tz.c:175-182
# defines them as CORE_CUSTSWNO(1,1..8), and core.h:347 gives CORE_CUSTSWNO(c,r) = (CORE_CUSTSWCOL-1+c)*10+r with
# CORE_CUSTSWCOL = CORE_STDSWCOLS = 12, so PinMAME publishes them at 121-128 (the same rule the Indiana Jones and
# Star Trek: The Next Generation records follow). The curator's tables below stay keyed by the printed number;
# this map gives the public address each one is bound to.
CORE_CUSTSWCOL = 12


def core_custswno(column: int, row: int) -> int:
	return (CORE_CUSTSWCOL - 1 + column) * 10 + row


CLOCK_OPTO_PUBLIC = {90 + row: core_custswno(1, row) for row in range(1, 9)}
CLOCK_OPTO_BOARD = {
	"A-16220": "the Minute Opto P.C.B.; the Hour board is A-16219",
	"A-16219": "the Hour Opto P.C.B.; the Minute board is A-16220",
}
# Page 2-50 column 9 heading: Gray-White, "*J5-1" (footnote: "* Located on 8 Driver P.C.B., A-16100, in backbox"),
# no driver pin printed. Page 1-18: "This column is driven by Q1 and Q12 of the 8-Driver Board."
CLOCK_COLUMN_WIRING = ("Gray-White", "8-Driver PCB A-16100 J5-1", "8-Driver Board Q1 and Q12")

DEDICATED_SWITCH_LABELS = {
	1: ("Coin Chute 1", "cabinet.coin.1", "First coin chute."),
	2: ("Coin Chute 2", "cabinet.coin.2", "Second coin chute."),
	3: ("Coin Chute 3", "cabinet.coin.3", "Third coin chute."),
	4: ("Coin Chute 4", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}

FLIPPER_LABELS = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used"),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used"),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used"),
	115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "used"),
	116: ("Upper Right Flipper Button", "flipper.upper.right.button", "used"),
	117: ("Upper Left Flipper EOS", "internal.flipper.upper.left.eos", "used"),
	118: ("Upper Left Flipper Button", "flipper.upper.left.button", "used"),
}

# --- Retained-table objects used as spatial anchors. Raw table coordinates exactly as the
# retained extraction stores them (Light/Kicker/Trigger/Bumper/Flipper "center", HitTarget and
# Primitive "position", or the arithmetic mean of a Wall's own drag points); they are listed in
# review-artifacts/twilight-zone-1993/vpx-geometry.txt or its supplements vpx-geometry-2026-09-25.txt and
# vpx-geometry-2026-09-25-round3.txt
# and normalized by _norm() below.
TABLE_OBJECTS: dict[str, tuple[float, float]] = {
	"Kicker.sw15": (850.7996, 1896.9911),
	"Kicker.sw18": (505.2928, 2109.0137),
	"Kicker.sw58": (704.7905, 1123.8999),
	"Kicker.sw88": (817.7883, 371.15216),
	"Kicker.AutoPlungerKicker": (947.85394, 2113.5813),
	"Kicker.GumballPopper": (333.1182, 85.42504),
	"HitTarget.sw47": (525.56824, 469.4863),
	"Bumper.Bumper1": (81.207054, 1092.1573),
	"Bumper.Bumper2": (289.68414, 1082.9271),
	"Bumper.Bumper3": (177.10031, 1279.8246),
	"Flipper.LeftFlipper": (363.0102, 1809.9),
	"Flipper.RightFlipper": (687.8521, 1809.9),
	"Flipper.LeftFlipper1": (303.10974, 693.63904),
	"Flipper.RightFlipper1": (860.4233, 1152.7524),
	"Flipper.GumballDiverter": (631.3653, 117.31948),
	"Wall.LeftSlingShot": (320.879095, 1575.8101),
	"Wall.RightSlingShot": (731.9608916666666, 1574.7893666666666),
	"Wall.RampDivWall": (1035.77705, 639.40872875),
	"Primitive.BM_ClockLarge": (827.7844, 592.8787),
	"Primitive.BM_Gumballs": (201.49995, 231.02759),
	"Primitive.BM_RDiv": (302.25, 462.75),
	"Light.f17": (190.20378, 1138.8903),
	"Light.f17b": (26.05565, 1246.6298),
	"Light.f18": (935.20135, 872.79504),
	"Light.f19": (187.57002, 755.5025),
	"Light.f20": (437.96762, 81.31031),
	"Light.f41": (1025.6647, 112.99953),
	"Light.f28": (568.1295, 181.99942),
	"Light.f37": (907.95844, 1058.5209),
	"Light.f38": (56.394672, 100.31158),
	"Light.f39": (55.475533, 183.33089),
	"Light.f40": (55.97702, 291.95407),
}


def _norm(name: str) -> tuple[float, float]:
	x, y = TABLE_OBJECTS[name]
	return (round(x / BOUNDS_X, 6), round(y / BOUNDS_Y, 6))


# --- Objects of the 2020 ninuzzu table used as placements, raw as its extraction stores them (Light "center", or the
# arithmetic mean of a Wall's own drag points). That table is 1093 x 2162, so each is normalized by its own bounds
# (_norm2020); 60 same-named Trigger/Kicker/Bumper/Gate/Spinner objects of the two tables agree to a median 0.004
# normalized (53 within 0.01), so the two normalized frames can be mixed. Listed in
# review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-26.txt.
TABLE_2020_OBJECTS: dict[str, tuple[float, float]] = {
	"Light.f18c": (697.35803, 723.0047),
	"Light.f19a": (98.25, 631.25),
	"Light.f20c": (490.97662, 1251.9048),
	"Light.f41c": (566.0198, 1252.6528),
	"Wall.sw45": (58.503222, 869.03412),
	"Wall.sw45a": (85.86118925, 983.8593475),
	"Wall.sw46": (287.8799175, 866.305885),
	"Wall.sw46a": (280.2388025, 984.8149225),
}


def _norm2020(name: str) -> tuple[float, float]:
	x, y = TABLE_2020_OBJECTS[name]
	return (round(x / BOUNDS_2020_X, 6), round(y / BOUNDS_2020_Y, 6))


# The clock's rotation axis: the pivot of the minute-hand primitive that the retained script's
# UpdateClock rotates from Controller.GetMech(0). The hour-hand pivot (BM_ClockShort) sits within
# 0.009 of it; the clock face primitive's own pivot is not its axis, so it is not used.
CLOCK_AXIS = "Primitive.BM_ClockLarge"
# The gumball machine assembly (A-16132): the pivot of the gumball-globe primitive, which agrees
# with manual callouts 24 (page 2-53) and 55 (page 2-51), both printed inside the gumball-machine
# outline at the top left of the playfield.
GUMBALL_MACHINE = "Primitive.BM_Gumballs"

# --- Normalized playfield coordinates (x/1082.353, y/2164.706) from the retained
# extraction; see review-artifacts/twilight-zone-1993/vpx-geometry.txt.
SWITCH_POSITIONS = {
	11: [(0.75733, 0.733553)], 12: [(0.816857, 0.749645)],
	15: [(0.786065, 0.876327)], 16: [(0.717238, 0.897158)], 17: [(0.649107, 0.918002)], 18: [(0.466847, 0.974273)],
	25: [(0.586598, 0.938043)], 26: [_norm("Kicker.sw15")], 27: [(0.953552, 0.885472)], 28: [(0.816222, 0.633787)],
	31: [_norm("Bumper.Bumper1")], 32: [_norm("Bumper.Bumper2")], 33: [_norm("Bumper.Bumper3")],
	34: [(0.296464, 0.727956)], 35: [(0.676268, 0.727484)],
	36: [(0.049304, 0.746239)], 37: [(0.126765, 0.714541)], 38: [(0.212212, 0.713967)],
	41: [(0.085949, 0.216834)], 42: [(0.201272, 0.381543)], 43: [(0.663093, 0.297159)], 44: [(0.033737, 0.300647)],
	47: [_norm("HitTarget.sw47")],
	51: [(0.60814, 0.116087)], 52: [(0.143608, 0.216659)], 53: [(0.423152, 0.15106)], 54: [(0.871712, 0.078071)],
	55: [_norm(GUMBALL_MACHINE)],
	56: [(0.218257, 0.190395)], 57: [(0.528667, 0.472186)], 58: [(0.651165, 0.519193)],
	61: [(0.950867, 0.529593)], 62: [(0.950867, 0.491633)], 63: [(0.950797, 0.45433)],
	48: [(0.206766, 0.619195)],
	64: [(0.721088, 0.222436)], 65: [(0.759336, 0.32671), (0.759105, 0.30282)],
	66: [(0.646481, 0.383017)], 67: [(0.635675, 0.407582)], 68: [(0.628201, 0.432651)],
	72: [(0.875735, 0.976383)], 73: [(0.752093, 0.135059)], 74: [_norm("Kicker.GumballPopper")],
	75: [(0.184321, 0.296114)], 76: [(0.167764, 0.468382)], 77: [(0.298735, 0.531676)], 78: [(0.334772, 0.505688)],
	81: [(0.881833, 0.219272)], 83: [(0.313118, 0.156291)], 84: [(0.765208, 0.141901)],
	85: [(0.775234, 0.11319)], 87: [(0.174341, 0.060475)], 88: [(0.755565, 0.171456)],
	**{address: [_norm(CLOCK_AXIS)] for address in range(91, 99)},
	# Two contacts each ("(2)" on page 2-51), placed on the 2020 table's own switch walls.
	45: [_norm2020("Wall.sw45"), _norm2020("Wall.sw45a")],
	46: [_norm2020("Wall.sw46"), _norm2020("Wall.sw46a")],
}
# Switches placed from the 2020 ninuzzu table rather than the 2.4.5 table.
SWITCH_2020_PLACEMENTS = {
	45: (
		"Two placements, one per contact: manual page 2-51 prints \"Mini-playfield Left (2)\", and the page 2-50 drawing "
		"\"MINI-PLAYFIELD, TOP AND BOTTOM RAMP SWITCH LOCATIONS\" draws two numbered balloons for 45 on the left of the "
		"mini-playfield, one on its left side rail and one on its bottom rail (remote callout balloons whose pointer tails "
		"reach the switches). The coordinates are the drag-point centroids of the 2020 ninuzzu table's own switch walls "
		"Wall.sw45 (upper) and Wall.sw45a (lower), invisible collidable hit walls whose sw45_Hit and sw45a_Hit handlers "
		"both pulse switch 45 (its script.vbs lines 1718-1719); the retained 2.4.5 table keeps the handlers but has no "
		"such objects. The page 2-50 drawing is a perspective detail view with remote callout balloons, so it "
		"corroborates the count, the side and the order of the two contacts, while the coordinates come from the table: "
		"through an affine fit on six validated mini-playfield switches (leave-one-out RMS 0.066) its two balloons land "
		"0.034 (upper) and 0.024 (lower) from the two walls (see vpx-geometry-2026-09-26.txt)."
		" The pinned fit's pass rule is an offset no larger than the fit's largest leave-one-out error and under 0.07. That largest leave-one-out error (0.112) comes from one outlying control, balloon 53, so the 0.07 cap, the bar the Indianapolis 500 record also uses, is the one that decides."
	),
	46: (
		"Two placements, one per contact: manual page 2-51 prints \"Mini-playfield Right (2)\", and the page 2-50 drawing "
		"\"MINI-PLAYFIELD, TOP AND BOTTOM RAMP SWITCH LOCATIONS\" draws two numbered balloons for 46 on the right of the "
		"mini-playfield, one on its right side rail and one on its bottom rail (remote callout balloons whose pointer tails "
		"reach the switches). The coordinates are the drag-point centroids of the 2020 ninuzzu table's own switch walls "
		"Wall.sw46 (upper) and Wall.sw46a (lower), invisible collidable hit walls whose sw46_Hit and sw46a_Hit handlers "
		"both pulse switch 46 (its script.vbs lines 1720-1721); the retained 2.4.5 table keeps the handlers but has no "
		"such objects. The page 2-50 drawing is a perspective detail view with remote callout balloons, so it "
		"corroborates the count, the side and the order of the two contacts, while the coordinates come from the table: "
		"through an affine fit on six validated mini-playfield switches (leave-one-out RMS 0.066) its two balloons land "
		"0.047 (upper) and 0.035 (lower) from the two walls (see vpx-geometry-2026-09-26.txt)."
		" The pinned fit's pass rule is an offset no larger than the fit's largest leave-one-out error and under 0.07. That largest leave-one-out error (0.112) comes from one outlying control, balloon 53, so the 0.07 cap, the bar the Indianapolis 500 record also uses, is the one that decides."
	),
}
# Position 65 has two HitTarget objects (sw65, sw65a); Power Payoff is a two-target
# bank sharing one public switch, matching the manual's "(2)" quantity annotation.
SWITCH_PROJECTIONS = {
	26: (
		"Projected onto Kicker.sw15, the right-trough eject position: the retained script's sw15_hit/sw15_unhit "
		"handlers set and clear switch 26 from the ball resting in that kicker (script.vbs sw15_hit), and the "
		"manual's Main Playfield Switch Locations drawing (page 2-51) prints callout 26 beside callout 15 at the "
		"trough's eject end. The proximity sensor itself is not a separate table object."
	),
	31: (
		"Placed on Bumper.Bumper1, the object whose Bumper1_Hit handler pulses switch 31 in the retained script; "
		"it is the left bumper of the three, and the manual's Main Playfield Switch Locations drawing (page 2-51) "
		"prints callout 31 on the left jet bumper."
	),
	32: (
		"Placed on Bumper.Bumper2, the object whose Bumper2_Hit handler pulses switch 32 in the retained script; "
		"it is the upper-right bumper of the three, and the manual's drawing (page 2-51) prints callout 32 there."
	),
	33: (
		"Placed on Bumper.Bumper3, the object whose Bumper3_Hit handler pulses switch 33 in the retained script; "
		"it is the lower bumper of the three, and the manual's drawing (page 2-51) prints callout 33 there."
	),
	52: "Placed on Trigger.sw52, the table's own trigger for this switch: its sw52_Hit handler pulses switch 52 (script.vbs line 1709); the geometry file lists it under the Hitchhiker figure's lane.",
	55: (
		"Projected onto the gumball machine assembly (A-16132), represented by the pivot of the retained table's "
		"gumball-globe primitive (Primitive.BM_Gumballs). The geneva switch sits on the underside of the playfield "
		"beneath that assembly (manual dagger footnote) and the manual's drawing (page 2-51) prints callout 55 "
		"inside the gumball-machine outline. The table has no switch object of its own for it; its script pulses "
		"switch 55 from SolGumRelease, which SolGumballMotor schedules after solenoid 24 turns on."
	),
	**{
		address: (
			"Projected onto the clock's rotation axis (the pivot of Primitive.BM_ClockLarge, the minute hand the "
			"retained script's UpdateClock rotates from Controller.GetMech(0)). The Minute (A-16220) and Hour "
			"(A-16219) opto boards are inside the clock assembly, and the table models no individual opto object."
		)
		for address in range(91, 99)
	},
}
# Physical switches with no defensible coordinate: their spatial key is omitted entirely. None remain since the
# 2026-09-26 pass placed switches 45/46 from the 2020 table.
UNPLACED_SWITCHES: dict[int, str] = {}

_JET_LABEL_NOTE = (
	"tz.c names this address only swJet{n}; the printed label comes from the manual's Main Playfield Switch "
	"Locations drawing (page 2-51), which prints callout 31 on the left, 32 on the upper-right, and 33 on the lower "
	"jet bumper, and the retained script binds Bumper1/Bumper2/Bumper3 (left/upper-right/lower) to 31/32/33 in the "
	"same order. An earlier revision of this definition labelled 31-33 Lower/Left/Right by analogy with the "
	"jet-bumper coil order (12 Lower, 13 Left, 14 Right), which no source supports for the switches."
)
SWITCH_EXTRA_NOTES = {
	31: _JET_LABEL_NOTE.format(n=1),
	32: _JET_LABEL_NOTE.format(n=2),
	33: _JET_LABEL_NOTE.format(n=3),
	34: "The retained script's LeftSlingShot_Slingshot pulses switch 34 and also, erroneously, switch 42; the extra pulse is a defect in the consumed table, not a property of the machine.",
	35: "The retained script's RightSlingShot_Slingshot pulses switch 35 and also, erroneously, switch 41; the extra pulse is a defect in the consumed table, not a property of the machine.",
	41: "Besides its DeadEnd trigger, the retained script also pulses switch 41 from RightSlingShot_Slingshot, a defect in the consumed table rather than a machine behavior.",
	42: "Besides its sw42 trigger, the retained script also pulses switch 42 from LeftSlingShot_Slingshot, a defect in the consumed table rather than a machine behavior.",
}


def _switch_spatial(identifier: str, address: int, physical: dict[str, Any]) -> dict[str, Any]:
	refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
	if address in SWITCH_2020_PLACEMENTS:
		physical["notes"] += " " + SWITCH_2020_PLACEMENTS[address]
		refs = (VPX_2020_TABLE_SOURCE, VPX_2020_SCRIPT_SOURCE, MANUAL_IPDB_SOURCE, MANUAL_SOURCE)
		return located(identifier, "sensor", SWITCH_POSITIONS[address], *refs)
	if address in SWITCH_PROJECTIONS:
		physical["notes"] += " " + SWITCH_PROJECTIONS[address]
		refs = refs + (MANUAL_SOURCE,)
	return located(identifier, "sensor", SWITCH_POSITIONS[address], *refs)


# --- Solenoids (public PinMAME address -> label). Manual page 2-53 "Solenoid/Flasher
# Locations"; printed items 37-44 are the auxiliary board's own callout numbers, bridged
# to true public addresses 51-58 by the retained script's own comments (see
# manual-transcription.md).
SOLENOID_LABELS = {
	1: "Slot Kickout", 2: "Rocket Kicker", 3: "Auto-Fire Kicker", 4: "Gumball Popper",
	5: "Right Ramp Diverter", 6: "Gumball Diverter", 7: "Knocker", 8: "Outhole", 9: "Ball Release",
	10: "Right Slingshot", 11: "Left Slingshot",
	12: "Lower Jet Bumper", 13: "Left Jet Bumper", 14: "Right Jet Bumper",
	15: "Lock Release", 16: "Shooter Diverter",
	17: "Bumpers Flasher", 18: "Power Payoff Flasher", 19: "Mini-Playfield Flasher", 20: "Upper Left Ramp Flasher",
	21: "Left Magnet", 23: "Lower Right Magnet", 24: "Gumball Motor",
	25: "Left Mini-Playfield Magnet", 26: "Right Mini-Playfield Magnet", 27: "Left Ramp Diverter",
	28: "Inside Ramp Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold",
	35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	51: "Upper Right Flipper Flasher", 52: "Gumball Machine High Flasher",
	53: "Gumball Machine Middle Flasher", 54: "Gumball Machine Low Flasher",
	55: "Upper Right Ramp Flasher",
	56: "Clock Reverse", 57: "Clock Forward",
	58: "Clock Switch Strobe",
}
NOT_FITTED_SOLENOID_LABELS = {22: "Upper Right Magnet"}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Fliptronic Output 37", 38: "Unused WPC-Fliptronic Output 38",
	39: "Unused WPC-Fliptronic Output 39", 40: "Unused WPC-Fliptronic Output 40",
	41: "Unused WPC-Fliptronic Output 41", 42: "Unused WPC-Fliptronic Output 42",
	43: "Unused WPC-Fliptronic Output 43", 44: "Unused WPC-Fliptronic Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
	59: "Gumball Release (Software State)",
}
# Manual item numbers (printed on the auxiliary board diagram) that differ from the
# true public PinMAME address.
MANUAL_SOLENOID_ALIASES = {51: "37", 52: "38", 53: "39", 54: "40", 55: "41", 56: "42", 57: "43", 58: "44"}
SOLENOID_ASSEMBLIES = {
	1: "A-16434", 2: "A-16647", 3: "A-16647", 4: "A-16312", 5: "A-16361", 6: "A-16313",
	7: "B-10686-1", 8: "A-8039-3", 9: "A-16766", 10: "A-16645-R", 11: "A-16645-L",
	12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2", 15: "A-16307", 16: "A-16338",
	17: "A-12336-1", 18: "A-12336-1 / A-16060", 19: "A-12336-1", 20: "A-16330 / A-16060",
	21: None, 23: None, 24: "A-16132", 25: "A-16749", 26: "A-16749", 27: "A-16064",
	28: "A-16060", 51: "A-12336-1", 52: "A-16651-4", 53: "A-16651-4", 54: "A-16651-4",
	55: "A-16330 / A-16060", 56: "A-16120", 57: "A-16120", 58: "A-16100",
}
SOLENOID_COIL_PART = {
	1: "AE-24-900", 2: "AL-23-800", 3: "AL-23-800", 4: "AE-23-800", 5: "AE-26-1200", 6: "AE-26-1500",
	7: "AE-23-800", 8: "AE-27-1200", 9: "AE-26-1200", 10: "AE-27-1200", 11: "AE-27-1200",
	12: "AE-26-1200", 13: "AE-26-1200", 14: "AE-26-1200", 15: "AE-27-1200", 16: "SZ-33-3000",
	17: "24-8802", 18: "24-8802", 19: "24-8802", 20: "24-8802",
	21: "20-9247", 23: "20-9247", 24: "14-7984", 25: "20-9247", 26: "20-9247", 27: "AE-26-1500",
	28: "24-8802", 51: "24-8802", 52: "24-8802", 53: "24-8802", 54: "24-8802", 55: "24-8802",
}
SOLENOID_CALLBACKS = {
	1: "SlotMachineKickout", 2: "SolRocket", 3: "SolAutoKicker", 4: "SolGumballPopper",
	5: "SolRightRampDiverter", 6: "SolGumballDiverter", 7: "SolKnocker", 8: "SolOuthole", 9: "SolBallRelease",
	15: "LockKickout", 16: "SolShootDiverter",
	17: "SolModCallback UpdateF17", 18: "SolModCallback FlashPWM 18", 19: "SolModCallback FlashPWM 19",
	20: "SolModCallback FlashPWM 20",
	21: "SolLeftMagnet", 23: "SolLowerRightMagnet", 24: "SolGumballMotor",
	25: "SolMiniMagnet mLeftMini", 26: "SolMiniMagnet mRightMini", 27: "SolLeftRampDiverter",
	28: "SolModCallback FlashPWM 28",
	34: "SolURFlipper via SolCallback(sURFlipper) (upper right)",
	36: "SolULFlipper via SolCallback(sULFlipper) (upper left)",
	46: "SolRFlipper via SolCallback(sLRFlipper) (lower right)",
	48: "SolLFlipper via SolCallback(sLLFlipper) (lower left)",
	51: "SolModCallback FlashPWM 37", 52: "SolModCallback FlashPWM 38", 53: "SolModCallback FlashPWM 39",
	54: "SolModCallback FlashPWM 40", 55: "SolModCallback FlashPWM 41",
	59: "SolGumRelease (commented out; PinMAME hack, unreliable with SolModCallbacks)",
}
FLASHER_ADDRESSES = {17, 18, 19, 20, 28, 51, 52, 53, 54, 55}
# The clock switch strobe drives the clock opto boards' emitters through the auxiliary board; it is
# a logic-level line, not an actuator or an emitter, so it is typed control_signal.
CONTROL_SIGNAL_SOLENOIDS = {58}
# Printed quantities on the Solenoid/Flasher Locations table (page 2-53): items 17-20 print "(2)"; item 41 (public 55)
# prints no "(2)" but, like items 18 and 20, prints two 24-8802 bulb rows (on A-16330 and on A-16060), and the
# location drawing on the same page draws two callout-41 circles.
FLASHER_PRINTED_QUANTITY = {17: 2, 18: 2, 19: 2, 20: 2, 55: 2}

SOLENOID_POSITIONS = {
	1: [_norm("Kicker.sw58")], 2: [(0.816222, 0.633787)], 3: [_norm("Kicker.AutoPlungerKicker")],
	4: [(0.307772, 0.039463)], 5: [_norm("Primitive.BM_RDiv")], 6: [_norm("Flipper.GumballDiverter")],
	8: [_norm("Kicker.sw18")], 9: [(0.786065, 0.876327)],
	10: [_norm("Wall.RightSlingShot")], 11: [_norm("Wall.LeftSlingShot")],
	12: [_norm("Bumper.Bumper3")], 13: [_norm("Bumper.Bumper1")], 14: [_norm("Bumper.Bumper2")],
	15: [_norm("Kicker.sw88")], 16: [(0.907357, 0.888818)],
	17: [_norm("Light.f17"), _norm("Light.f17b")],
	21: [(0.313118, 0.156291)], 23: [(0.881833, 0.219272)], 24: [_norm(GUMBALL_MACHINE)],
	25: [(0.100956, 0.42269)], 26: [(0.237953, 0.42269)], 27: [_norm("Wall.RampDivWall")],
	28: [_norm("Light.f28")],
	33: [_norm("Flipper.RightFlipper1")], 34: [_norm("Flipper.RightFlipper1")],
	35: [_norm("Flipper.LeftFlipper1")], 36: [_norm("Flipper.LeftFlipper1")],
	45: [_norm("Flipper.RightFlipper")], 46: [_norm("Flipper.RightFlipper")],
	47: [_norm("Flipper.LeftFlipper")], 48: [_norm("Flipper.LeftFlipper")],
	51: [_norm("Light.f37")], 52: [_norm("Light.f38")], 53: [_norm("Light.f39")], 54: [_norm("Light.f40")],
	56: [_norm(CLOCK_AXIS)], 57: [_norm(CLOCK_AXIS)],
	# Two sockets each: the first on the retained 2.4.5 table's Light, the second on the 2020 table's Light for the
	# socket 2.4.5 dropped.
	18: [_norm("Light.f18"), _norm2020("Light.f18c")],
	19: [_norm("Light.f19"), _norm2020("Light.f19a")],
	20: [_norm("Light.f20"), _norm2020("Light.f20c")],
	55: [_norm("Light.f41"), _norm2020("Light.f41c")],
}
# Per-placement sources of the two-socket flashers: the first socket is the 2.4.5 table's script-bound Light, the
# second the 2020 table's; both are reconciled against the page 2-53 drawing.
_FLASHER_FIRST_SOCKET_REFS = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
_FLASHER_SECOND_SOCKET_REFS = (VPX_2020_TABLE_SOURCE, VPX_2020_SCRIPT_SOURCE, MANUAL_SOURCE, MANUAL_IPDB_SOURCE)
SOLENOID_PLACEMENT_REFS = {
	address: [_FLASHER_FIRST_SOCKET_REFS, _FLASHER_SECOND_SOCKET_REFS] for address in (18, 19, 20, 55)
}
_CLOCK_DRIVE_PLACEMENT_NOTE = (
	"Projected onto the clock's rotation axis (pivot of Primitive.BM_ClockLarge): this drive line runs the clock's DC "
	"gearmotor, which the manual's Clock Gear Train Assembly page (1-51) mounts on the clock's back panel, through the "
	"D.C. Motor Control Board A-16120; the clock test text on page 1-18 puts that board \"UNDER the playfield at "
	"approximately the same position as the clock\" and the drives 42 and 43 on the 8-Driver Board in the backbox. Page "
	"2-53 draws callouts 42/43 right of centre above the slot machine and page 2-47 (item 17, \"D.C. Motor Assembly\") "
	"puts A-16120 under the rear right of the playfield; the motor itself is on the clock."
)
# Why each placed output sits where it does. Every entry is either a script-bound object that is the
# device itself or a documented projection onto the device's own mechanism object.
SOLENOID_PLACEMENT_NOTES = {
	1: "Projected onto Kicker.sw58, the slot kickout hole the retained script's SlotMachineKickout kicks (with the overflow kicker beside it); manual page 2-53 prints callout 01 at the slot machine.",
	3: "Projected onto Kicker.AutoPlungerKicker, the shooter-lane kicker the retained script's SolAutoKicker fires; the same object carries switch 72.",
	5: (
		"Placed on Primitive.BM_RDiv, the diverter blade the retained script's diverterTimer rotates (through the BP_RDiv "
		"array) when SolRightRampDiverter fires; the position is the primitive's own pivot, the blade's hinge. The script's "
		"Trigger.DivTrig (an invisible trigger that catches the ball to kick it) and Wall.DivWall (an invisible collision "
		"wall whose collidability the coil toggles) are helpers and are not used. The table's invisible right-ramp physics "
		"ramp (Ramp.Ramp342, a two-wire ramp about 135 units above the playfield) runs from the right-ramp hairpin to the "
		"left side and passes about 0.02 in front of this pivot, over Wall.DivWall. Manual page 2-53 prints callout 05 "
		"left of centre with its arrow pointing left "
		"to a vertical rail; measured on the committed crop, the arrow tip normalizes to about (0.273, 0.199), 0.016 from "
		"the pivot (see vpx-geometry-2026-09-25-round3.txt)."
	),
	6: "Placed on Flipper.GumballDiverter, the diverter blade the retained script's SolGumballDiverter rotates; the manual's Lower Playfield Parts page (2-47) shows the A-16313 Rear Diverter Assembly (item 19) under this rear-centre region, while the leaderless callout 06 on page 2-53 is printed further left, in the same region but not on the blade.",
	8: "Projected onto Kicker.sw18, the outhole the retained script's SolOuthole kicks.",
	10: "Projected onto the retained table's Wall.RightSlingShot (drag-point mean), the slingshot assembly this coil fires; the table uses native slingshot physics, so no scripted coil object exists. Manual page 2-53 prints callout 10 at the right slingshot.",
	11: "Projected onto the retained table's Wall.LeftSlingShot (drag-point mean), the slingshot assembly this coil fires; the table uses native slingshot physics, so no scripted coil object exists. Manual page 2-53 prints callout 11 at the left slingshot.",
	12: "Projected onto Bumper.Bumper3, the lower jet bumper; manual page 2-53 prints callout 12 on the lower bumper. The table's bumpers are native physics, so the coil has no object of its own.",
	13: "Projected onto Bumper.Bumper1, the left jet bumper; manual page 2-53 prints callout 13 on the left bumper. The table's bumpers are native physics, so the coil has no object of its own.",
	14: "Projected onto Bumper.Bumper2, the upper-right jet bumper; manual page 2-53 prints callout 14 on the right bumper. The table's bumpers are native physics, so the coil has no object of its own.",
	15: "Projected onto Kicker.sw88, the lower lock position the retained script's LockKickout kicks; manual page 2-53 prints callout 15 at the lock.",
	17: "Two sockets, both driven by the retained script's UpdateF17: Light.f17 between the jet bumpers and Light.f17b at the left edge beside them, matching the two callout-17 circles on manual page 2-53 and its printed \"(2)\".",
	24: "Projected onto the gumball machine assembly (A-16132), represented by the pivot of Primitive.BM_Gumballs; manual page 2-53 prints callout 24 inside the gumball-machine outline. The retained script's SolGumballMotor turns the machine's knob animation.",
	27: "Projected onto Wall.RampDivWall (drag-point mean), the blocking wall the retained script's SolLeftRampDiverter drops; manual page 2-53 prints callout 27 at the same right-edge position. Flipper.RampDiverter, the visible blade animation, sits at y=1.000665, outside the playfield, and is not used.",
	28: "Placed on Light.f28, the flasher light the retained script's FlashPWM 28 drives; manual page 2-53 draws one callout-28 circle at the inside of the ramp.",
	33: "Projected onto Flipper.RightFlipper1, the upper right flipper the retained script's SolURFlipper moves.",
	34: "Projected onto Flipper.RightFlipper1, the upper right flipper the retained script's SolURFlipper moves.",
	35: "Projected onto Flipper.LeftFlipper1, the upper left flipper the retained script's SolULFlipper moves.",
	36: "Projected onto Flipper.LeftFlipper1, the upper left flipper the retained script's SolULFlipper moves.",
	45: "Projected onto Flipper.RightFlipper, the lower right flipper the retained script's SolRFlipper moves.",
	46: "Projected onto Flipper.RightFlipper, the lower right flipper the retained script's SolRFlipper moves.",
	47: "Projected onto Flipper.LeftFlipper, the lower left flipper the retained script's SolLFlipper moves.",
	48: "Projected onto Flipper.LeftFlipper, the lower left flipper the retained script's SolLFlipper moves.",
	51: "Placed on Light.f37, the flasher light the retained script's FlashPWM 37 drives; manual page 2-53 draws callout 37 beside the upper right flipper.",
	52: "Placed on Light.f38, the flasher light the retained script's FlashPWM 38 drives; manual page 2-53 draws callouts 38-40 stacked at the top-left corner by the gumball machine.",
	53: "Placed on Light.f39, the flasher light the retained script's FlashPWM 39 drives; manual page 2-53 draws callouts 38-40 stacked at the top-left corner by the gumball machine.",
	54: "Placed on Light.f40, the flasher light the retained script's FlashPWM 40 drives; manual page 2-53 draws callouts 38-40 stacked at the top-left corner by the gumball machine.",
	56: _CLOCK_DRIVE_PLACEMENT_NOTE,
	57: _CLOCK_DRIVE_PLACEMENT_NOTE,
	18: (
		"Two sockets, matching the \"(2)\" printed on page 2-52 and page 2-53 and the two callout-18 circles on the page "
		"2-53 drawings (one on the ramp overlay, one right of centre on a small insert of the main playfield). The first "
		"is the retained 2.4.5 table's Light.f18, the ramp-overlay bulb its FlashPWM 18 drives. The second is the 2020 "
		"ninuzzu table's Light.f18c, which that table's SolCallback(18) \"setlamp 118\" drives through NFadeLm 118 (its "
		"script.vbs line 2182); of the two co-located Lights there (f18c falloff 50, f18d falloff 110) the one with the "
		"smaller falloff is used. Reconciled against the page 2-53 main-playfield drawing by a least-squares affine fit on "
		"eight validated placements (RMS residual 0.010, leave-one-out RMS 0.019): the fitted callout lands 0.008 "
		"from Light.f18c."
	),
	19: (
		"Two sockets, matching the \"(2)\" printed on page 2-52 and page 2-53 and the two callout-19 circles the page 2-53 "
		"overlay drawing puts on the mini-playfield, one at its centre and one near its top. The first is the retained "
		"2.4.5 table's Light.f19, which its FlashPWM 19 drives; the second is the 2020 ninuzzu table's Light.f19a, which "
		"that table's SolCallback(19) \"setlamp 119\" drives through NFadeLm 119 (its script.vbs line 2188), the only "
		"Light at that spot. Reconciled against the overlay drawing by a least-squares affine fit on nine validated "
		"placements (RMS residual 0.020, leave-one-out RMS 0.034): the lower circle lands 0.014 from Light.f19 and the "
		"upper circle 0.040 from Light.f19a, more than that RMS, so the drawing corroborates the count, that both sockets "
		"are on the mini-playfield and their order (one at its centre, one near its top), while the coordinates come from "
		"the tables. The pinned fit's pass rule is an offset no larger than the fit's largest leave-one-out error and "
		"under 0.07; that largest leave-one-out error (0.067) comes from one outlying control, callout 18 on the "
		"overlay, so the 0.07 cap, the bar the Indianapolis 500 record also uses, is the one that decides."
	),
	20: (
		"Two sockets, matching the two 24-8802 bulb rows and the \"(2)\" printed on page 2-53 (page 2-52 prints this row "
		"without \"(2)\") and the two callout-20 circles on its drawings, at the top of the upper left ramp and on the "
		"door panel's Gum insert. The first is the retained 2.4.5 table's Light.f20, the ramp bulb its FlashPWM 20 drives. "
		"The second is the 2020 ninuzzu table's Light.f20c under the Gum insert, which that table's SolCallback(20) "
		"\"setlamp 120\" drives through NFadeLm 120 (its script.vbs line 2195); of the two co-located Lights there (f20c "
		"falloff 80, f20d falloff 95) the one with the smaller falloff is used. Reconciled against the page 2-53 "
		"main-playfield drawing by the same eight-point fit as flasher 18: the fitted callout lands 0.005 from Light.f20c. "
		"Both retained scripts comment the circuit \"x2 (**)\" with the footnote \"(**) - the additional GUM and BALL "
		"flashers were removed ro reduce cost\" [sic]; that is an unsourced claim about later production, and the manual, "
		"the physical authority, prints two sockets."
	),
	55: (
		"Two sockets, matching the two 24-8802 bulb rows page 2-53 prints for item 41 (without a \"(2)\"; page 2-52 prints "
		"one row) and the two callout-41 circles on its drawings, at the top of the upper right ramp and on the door "
		"panel's Ball insert. The first is the retained 2.4.5 table's Light.f41, the ramp bulb its FlashPWM 41 drives. "
		"The second is the 2020 ninuzzu table's Light.f41c under the Ball insert, which that table's SolCallback(55) "
		"\"setlamp 141\" drives through NFadeLm 141 (its script.vbs line 2232); of the two co-located Lights there (f41c "
		"falloff 80, f41d falloff 95) the one with the smaller falloff is used. Reconciled against the page 2-53 "
		"main-playfield drawing by the same eight-point fit as flasher 18: the fitted callout lands 0.008 from Light.f41c. "
		"Both retained scripts comment the circuit \"x2 (**)\" with the unsourced note that the door-panel bulb was removed "
		"to reduce cost; the manual prints two sockets."
	),
}
# Physical outputs with no defensible coordinate: their spatial key is omitted entirely. None remain since the
# 2026-09-26 pass: the knocker is backbox hardware and every flasher's sockets are placed.
UNPLACED_SOLENOIDS: dict[int, str] = {}
_CLOCK_DRIVE_COMMON = (
	"The clock test text on page 1-18 reads \"With only drive 43 turned ON, the clock moves forward. With only drive 42 "
	"turned ON, the clock moves in reverse. With both drives ON, or both drives OFF, the clock is stopped.\"; page 2-52 "
	"prints drive 42 \"Clock Reverse\" and 43 \"Clock Forward\" (both A-16120, from the D.C. Motor Control Assembly), "
	"page 2-53 prints items 42 Clock Reverse and 43 Clock Forward, and the retained script's commented cross-reference "
	"reads '(42) Clock Reverse' against SolCallback(56) and '(43) Clock Forward' against SolCallback(57). The ROM's own "
	"clock test (T.16 on the 9.2 ROM; runtime.twilight-zone.clock-test) agrees: while its display reads CLOCK FWD. SLOW "
	"or FWD. FAST, public 57 stays on and 56 drops in short bursts, so the intervals with only one drive on are 57-only; "
	"while it reads CLOCK REV. SLOW or REV. FAST they are 56-only; and while it reads CLOCK STOPPED both stay on. The run "
	"shows which public output the ROM holds for each named operation, not which physical wire turns the motor which "
	"way. Pinned PinMAME's src/wpc/sims/wpc/full/tz.c defines sClockFwd as CORE_CUSTSOLNO(6), public 56, and sClockRev "
	"as CORE_CUSTSOLNO(7), public 57 (tz.c:210-211), names that read backwards against the manual and the ROM. Only the "
	"names are swapped: tz.c:601-616 declares mechClock = {sClockRev, sClockFwd, MECH_TWODIRSOL|MECH_FAST, ...} with its "
	"own clock-opto table, outside the #if 0 block at tz.c:638-661 (an older, disabled tick model), and init_tz "
	"registers it with mech_add(0,&mechClock) (tz.c:624). mech.c:140-145 reads sol1 = sClockRev = public 57 and sol2 = "
	"sClockFwd = public 56 and sets dir = (sol==1)-(sol==2), so 57 alone runs PinMAME's live clock model forward and 56 "
	"alone runs it back, as the manual and the ROM say. With that model on (mechanics bit 0, the retained table's "
	"HandleMechanics = 1), a second run of the ROM's clock test (runtime.twilight-zone.clock-test-mech) shows the "
	"displayed time advance from 0:00 to 0:15 under CLOCK FWD. SLOW and on to 1:00 under CLOCK FWD. FAST, and fall back "
	"to 12:00 under CLOCK REV. FAST. The swapped #define names are a PinMAME naming defect, not a disagreement about "
	"the machine."
)
CLOCK_DRIVE_NOTES = {
	56: "Clock Reverse: drive 42 of the 8-Driver Board, the reverse input of the clock's D.C. motor control board. " + _CLOCK_DRIVE_COMMON,
	57: "Clock Forward: drive 43 of the 8-Driver Board, the forward input of the clock's D.C. motor control board. " + _CLOCK_DRIVE_COMMON,
}
KNOCKER_NOTE = (
	"Backbox hardware, so the spatial record is a controlled not_applicable: the Solenoid/Flasher Table (page 2-52 of "
	"the complete IPDB copy) prints the knocker's connections J130-8 and J107-3 and coil AE-23-800 "
	"under its Backbox columns, where the outhole row beside it uses the Playfield columns, and the Backbox Assembly "
	"page 2-4 lists item 2 \"B-10686-1 Knocker & Bracket Assy.\" and draws it inside the backbox, top left. Page "
	"2-52's column headings do not match its cells, on this row as on every coil row 01-28: each row prints its "
	"power driver board drive connection (a J130, J127, J125 or J124 pin, which the connector list on page 3-33 "
	"names as that solenoid's drive) under Voltage Connections and its J107 or J109 supply pin under Drive "
	"Connections, as the G.I. rows print return and feed the other way round. So J130-8 is the knocker's drive "
	"connection and J107-3 its supply. The power "
	"driver board's connector list (page 3-33) labels J130-8 \"Violet-Black, Sol 7 to playfield coil\", the same "
	"wording as every other J130 pin; that generic label does not outweigh the backbox columns and the backbox assembly "
	"drawing. The retained table's KnockerPosition primitive is an invisible sound-position helper parked off the "
	"playfield, not evidence."
)


# --- Lamps (full 8x8 matrix, manual page 2-55 "Lamp Locations").
LAMP_LABELS = {
	11: "Camera (Door)", 12: "Hitch-Hicker (Door)", 13: "Clock Chaos (Door)", 14: "Super Skill (Door)",
	15: "Fast Lock (Door)", 16: "Lite Gumball (Door)", 17: "Town Square Madness (Door)", 18: "Lite Extra Ball (Door)",
	21: 'Door Panel "Lock 2"', 22: "Greed (Door)", 23: "10 Million (Door)", 24: "Battle the Power (Door)",
	25: "The Spiral (Door)", 26: "Clock Million (Door)", 27: "Super Slot (Door)", 28: 'Door Panel "Ball"',
	31: "Left Extra Ball", 32: 'Door Panel "Lock 1"', 33: "Left Inlane 1", 34: "Door Handle",
	35: "Left Inlane 2", 36: 'Door Panel "Gum"', 37: "Lower Left 5 Million", 38: "Dead End",
	41: 'Spiral "2 Million"', 42: "Spiral Left Battle Power", 43: 'Spiral "4 Million"',
	44: "Spiral Right Battle Power", 45: 'Spiral "10 Million"', 46: 'Spiral "Extra Ball"',
	47: "Shoot Again", 48: "Right Inlane",
	51: "Left Ramp Bonus X", 52: "Left Ramp Multiball", 53: "Left Ramp Super Skill", 54: "Left Powerball",
	55: "The Camera", 56: "Right Ramp The Power", 57: "Lock Extra Ball", 58: "Lock Arrow",
	61: "Left Jet Bumper", 62: "Lower Jet Bumper", 63: "Right Jet Bumper", 64: "Middle Left 5 Million",
	65: "Upper Left 5 Million", 66: "Right Special", 67: "Right Powerball", 68: "Right Lane Spiral",
	71: "Lower Right 5 Million", 72: "Middle Right 5 Million 2", 73: "Middle Right 5 Million",
	74: "Power Payoff", 75: "Upper Right 5 Million", 76: "Mini-Playfield 500,000",
	77: "Mini-Playfield 1,000,000", 78: "Mini-Playfield 750,000",
	81: "Left Spiral", 82: "Clock Millions", 83: "Piano Yellow", 84: "Piano Red",
	85: "Slot Machine", 86: "Right Lane Gumball", 87: "Buy-In Button", 88: "Credit Button",
}
LAMP_ASSEMBLIES = {
	11: "A-16327", 12: "A-16327", 13: "A-16327", 14: "A-16327", 15: "A-16327", 16: "A-16327",
	17: "A-16327", 18: "A-16327",
	21: "A-16327", 22: "A-16327", 23: "A-16327", 24: "A-16327", 25: "A-16327", 26: "A-16327",
	27: "A-16327", 28: "A-16327",
	31: "A-16327", 32: "A-16516", 33: "A-16327", 34: "A-16516", 35: "A-16327", 36: "A-16516",
	37: "A-16517", 38: "A-16517",
	41: "A-16328", 42: "A-16328", 43: "A-16328", 44: "A-16328", 45: "A-16328", 46: "A-16328",
	47: "A-11754", 48: "A-11271",
	51: "A-16329", 52: "A-16329", 53: "A-16329", 54: "A-11271", 55: "A-11754", 56: "A-11271",
	57: "A-16515", 58: "A-16515",
	61: "B-9414-3", 62: "B-9414-3", 63: "B-9414-3", 64: "A-16517", 65: "A-11271", 66: "A-11271",
	67: "A-11754", 68: "A-11271",
	71: "A-16514", 72: "A-16514", 73: "A-16514", 74: "A-16514", 75: "A-16515", 76: "A-12887",
	77: "A-12887", 78: "A-12887",
	81: "A-12887", 82: "A-11271", 83: "A-12887", 84: "A-12887", 85: "A-11905", 86: "B-12224",
	87: "20-9663-9", 88: "20-9663-1",
}
LAMP_BULB = {
	address: ("#44" if code == "24-6549" else "#555")
	for address, code in {
		11: "24-8768", 12: "24-8768", 13: "24-8768", 14: "24-8768", 15: "24-8768", 16: "24-8768", 17: "24-8768", 18: "24-8768",
		21: "24-8768", 22: "24-8768", 23: "24-8768", 24: "24-8768", 25: "24-8768", 26: "24-8768", 27: "24-8768", 28: "24-8768",
		31: "24-8768", 32: "24-8768", 33: "24-8768", 34: "24-8768", 35: "24-8768", 36: "24-8768", 37: "24-8768", 38: "24-8768",
		41: "24-8768", 42: "24-8768", 43: "24-8768", 44: "24-8768", 45: "24-8768", 46: "24-8768", 47: "24-6549", 48: "24-6549",
		51: "24-8768", 52: "24-8768", 53: "24-8768", 54: "24-6549", 55: "24-6549", 56: "24-6549", 57: "24-8768", 58: "24-8768",
		61: "24-8768", 62: "24-8768", 63: "24-8768", 64: "24-8768", 65: "24-6549", 66: "24-6549", 67: "24-6549", 68: "24-6549",
		71: "24-8768", 72: "24-8768", 73: "24-8768", 74: "24-8768", 75: "24-8768", 76: "24-8768", 77: "24-8768", 78: "24-8768",
		81: "24-8768", 82: "24-6549", 83: "24-8768", 84: "24-8768", 85: "24-6549", 86: "24-8768",
	}.items()
}
LAMP_NOT_SHOWN = {76, 77, 78, 81, 83, 84, 85, 86}
LAMP_DOOR_INSERTS = {11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28}

LAMP_POSITIONS = {
	11: [(0.485033, 0.725309)], 12: [(0.407717, 0.724457)], 13: [(0.391142, 0.695878)], 14: [(0.390946, 0.655104)],
	15: [(0.391442, 0.617117)], 16: [(0.391005, 0.576266)], 17: [(0.406546, 0.539161)], 18: [(0.483602, 0.539219)],
	21: [(0.519007, 0.682909)], 22: [(0.561394, 0.723758)], 23: [(0.578152, 0.695283)], 24: [(0.577851, 0.656535)],
	25: [(0.575682, 0.616606)], 26: [(0.576326, 0.576487)], 27: [(0.560138, 0.539998)], 28: [(0.517527, 0.590167)],
	31: [(0.047299, 0.689935)], 32: [(0.445067, 0.682686)], 33: [(0.125581, 0.666423)], 34: [(0.441444, 0.637367)],
	35: [(0.212659, 0.666365)], 36: [(0.446808, 0.589079)], 37: [(0.238096, 0.639057)], 38: [(0.275385, 0.59232)],
	41: [(0.351168, 0.789469)], 42: [(0.406278, 0.778502)], 43: [(0.461657, 0.767818)], 44: [(0.517596, 0.767998)],
	45: [(0.571875, 0.778993)], 46: [(0.626699, 0.790051)], 47: [(0.489927, 0.86706)], 48: [(0.765058, 0.666869)],
	51: [(0.436739, 0.267084)], 52: [(0.446589, 0.304463)], 53: [(0.45534, 0.344007)], 54: [(0.330153, 0.279837)],
	55: [(0.402614, 0.415884)], 56: [(0.530783, 0.278281)], 57: [(0.654346, 0.216161)], 58: [(0.667387, 0.179159)],
	61: [(0.074018, 0.503123)], 62: [(0.165877, 0.588481)], 63: [(0.27162, 0.498675)], 64: [(0.320356, 0.558033)],
	65: [(0.392771, 0.511491)], 66: [(0.827084, 0.694934)], 67: [(0.809029, 0.429388)], 68: [(0.838774, 0.378112)],
	71: [(0.621373, 0.460741)], 72: [(0.589784, 0.409192)], 73: [(0.601763, 0.382925)], 74: [(0.644298, 0.333997)],
	75: [(0.682706, 0.238389)], 76: [(0.171099, 0.385177)], 77: [(0.112407, 0.337345)], 78: [(0.220667, 0.337737)],
	81: [(0.258442, 0.292657)], 82: [(0.490298, 0.266812)], 83: [(0.746993, 0.278478)], 84: [(0.737593, 0.265849)],
	85: [(0.738458, 0.42924)], 86: [(0.815733, 0.481498)],
}

GI_LABELS = {0: "Playfield Left", 1: "Mini-Playfield & Insert", 2: "Clock & Insert", 3: "Insert Main", 4: "Playfield Right"}
GI_COIL_NUMBER = {0: "24-6549", 1: "24-8768", 2: "24-8829, 24-8768", 3: "24-8768", 4: "24-6549"}
GI_POSITIONS = {
	0: [
		(0.035747, 0.46807), (0.036477, 0.451417), (0.152873, 0.420241), (0.391963, 0.126611),
		(0.420068, 0.110875), (0.330254, 0.085431), (0.287518, 0.76036), (0.170528, 0.706527),
		(0.118867, 0.761465), (0.189684, 0.786184), (0.261934, 0.810595),
	],
	4: [
		(0.725698, 0.392912), (0.926481, 0.360232), (0.806104, 0.307407), (0.939409, 0.189479),
		(0.940655, 0.168729), (0.930424, 0.0966), (0.930776, 0.079079), (0.861673, 0.024368),
		(0.822776, 0.024412), (0.683537, 0.759072), (0.746216, 0.409721), (0.695766, 0.814269),
		(0.74457, 0.796746),
	],
}
_GI_COLUMN_NOTE = (
	"Page 2-52 prints each G.I. string's return pin under Voltage Connections and its 6.8VAC pin under Drive "
	"Connections; the power driver board's connector list (page 3-33) names the J120/J121 pins 1-6 \"Return G.I.\" and "
	"pins 7-11 \"6.8VAC\", and the triac switches the return."
)
# Per-string wiring from the complete manual: page 2-52 (Solenoid/Flasher Table, General Illumination rows) and the
# power driver board's connector list on page 3-33, where J121 pins go "to playfield" and J120 pins "to insert".
GI_WIRING_NOTES = {
	0: "Page 2-52 wires it to the playfield only (J-121-1 and J-121-7, triac Q18, Wht-Brn, playfield bulb 24-6549); page 3-33 lists J121-1 \"Brown, Return G.I. to playfield\". " + _GI_COLUMN_NOTE,
	1: "Page 2-52 wires it to both the playfield (J-121-2, J-121-8) and the backbox (J-120-2, J-120-8) through triac Q10 (Wht-Org, bulb 24-8768 in both columns); page 3-33 lists J121-2 \"Orange, Return G.I. to playfield\" and J120-2 \"Orange, Return G.I. to insert\". " + _GI_COLUMN_NOTE,
	2: "Page 2-52 wires it to both the playfield (J-121-3, J-121-9) and the backbox (J-120-3, J-120-9) through triac Q14 (Wht-Yel, playfield bulb 24-8829, backbox bulb 24-8768); page 3-33 lists J121-3 \"Yellow, Return G.I. to playfield\" and J120-3 \"Yellow, Return G.I. to insert\". " + _GI_COLUMN_NOTE,
	3: "Page 2-52 wires it to the backbox only (J-120-5 and J-120-10, triac Q16, Wht-Grn, backbox bulb 24-8768); page 3-33 lists J120-5 \"Green, Return G.I. to insert\". " + _GI_COLUMN_NOTE,
	4: "Page 2-52 wires it to the playfield only (J-121-6 and J-121-11, triac Q12, Wht-Vio, playfield bulb 24-6549); page 3-33 lists J121-6 \"Violet, Return G.I. to playfield\". " + _GI_COLUMN_NOTE,
}
GI_MINI_PLAYFIELD_BLOCKER = (
	"No spatial placement: the playfield part of this mixed string has no bulb list. The Mini-Playfield Assembly A-16806 "
	"(parts list page 2-40, drawing page 2-41) shows item 10 \"A-12887 Socket Assembly, #555 Bulb\" with item 49 "
	"\"Sleeve, Yellow\" in the Street Light (item 2), and in its back view item 10's leader reaches a second socket; the "
	"page prints no quantity, and no page enumerates this string's bulbs. The retained 2.4.5 script binds the string to a "
	"single light (l101, x=0.118778 y=0.301331 on the mini-playfield). The 2020 ninuzzu table's GIMinipf collection, "
	"which its UpdateGI dims from G.I. string index 1, includes Light20 and Light43, which sit on main-playfield jet "
	"bumpers 1 and 2 (within about 0.01), so its membership is an author's choice, not a socket list. The backbox insert "
	"part (J-120-2) is cabinet hardware with no playfield coordinate. Resolution: a continuity or bulb survey of G.I. "
	"string 02 on a physical machine."
)
# The clock's two G.I. sockets, projected co-located onto the clock axis (the anchor of the clock motor outputs and
# optos); the FunHouse record's co-located clock placements are the precedent.
GI_CLOCK_POSITIONS = [_norm(CLOCK_AXIS), _norm(CLOCK_AXIS)]
GI_CLOCK_PLACEMENT_NOTE = (
	"Projected onto the clock's rotation axis (the pivot of Primitive.BM_ClockLarge, the anchor already used for clock "
	"outputs 56/57 and optos 121-128) as two co-located placements, quantity 2, recorded as observed because the axis is not a bulb object. The projection hides an offset: the "
	"page 2-33 drawing puts the two sockets side by side on bracket 24, about an inch apart, inside the clock "
	"housing's footprint, so each real socket lies within the housing, near but not on the axis. The Clock Assembly A-16124 (parts list "
	"page 2-32, drawing page 2-33; renumbered A-16124-1 by Manual Amendment 16-50020-AMD-1, which changes no socket item) "
	"carries item 25 \"A-12887 Socket & Bulb Assembly\", whose leader reaches two sockets on item 24 \"01-11337 Clock "
	"Mounting Bracket\", one bulb in item 27 \"Light Bulb Sleeve - Red\" and one in item 29 \"Light Bulb Sleeve - "
	"Yellow\". That these two sockets are string 03's playfield bulbs rests on the string's printed name \"Clock & "
	"Insert\" and its playfield connection; no page lists the string's sockets. The quantity counts only these two "
	"playfield sockets: the string's insert-board bulbs are backbox hardware with no playfield coordinate and no printed "
	"count. The 2020 ninuzzu table's GIClock collection, which its UpdateGI dims from G.I. string index 2, holds four "
	"Flasher glow sprites (image F_refl) at two positions beside the clock, about (0.715, 0.283) and (0.791, 0.287); "
	"they corroborate that the recreation models two emitters at the clock and are not socket positions. The retained "
	"2.4.5 script's single binding for the string, l102, only drives baked clock lightmaps from an off-playfield raw "
	"position (x=-230.57) and is not used."
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Twilight Zone retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Twilight Zone extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Twilight Zone retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Twilight Zone retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Twilight Zone retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def verify_2020_extraction_manifest(source_root: Path) -> dict[str, Any]:
	"""Verify the 2020 ninuzzu table's retained extraction against its pinned manifest identity."""
	extraction_root = source_root / EXTRACTION_2020_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_2020_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Twilight Zone 2020 table extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Twilight Zone 2020 table extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_2020_FILE_COUNT, EXTRACTION_2020_TOTAL_BYTES, EXTRACTION_2020_MANIFEST_SHA256):
		raise RuntimeError(f"Twilight Zone 2020 table extraction identity mismatch: files, bytes, manifest_sha256 = {identity}")
	return actual

# --- ROM clock test (T.16 on the 9.2 ROM): integrate public 56/57 per named operation of the retained run.
CLOCK_TEST_OPERATIONS = {
	# operation named on the DMD top line: (label of the start-press step, label of the stop-press step)
	"CLOCK FWD. SLOW": ("service Enter: start the selected operation (expected CLOCK FWD SLOW)", "service Enter: stop the first operation"),
	"CLOCK FWD. FAST": ("service Enter: start operation after Up press 1", "service Enter: stop operation after Up press 1"),
	"CLOCK REV. SLOW": ("service Enter: start operation after Up press 2", "service Enter: stop operation after Up press 2"),
	"CLOCK REV. FAST": ("service Enter: start operation after Up press 3", "service Enter: stop operation after Up press 3"),
}
CLOCK_TEST_STOPPED = {
	# stopped windows: (label of the step before the first sample, label of the last sample)
	"after service Enter opened T.16": ("service Enter: open T.16 CLOCK TEST", "T.16 idle sample 004"),
	"after the first stop": ("service Enter: stop the first operation", "T.16 stopped sample 004"),
	"after the second stop": ("service Enter: stop operation after Up press 1", "T.16 operation 2 stopped sample 004"),
	"after the third stop": ("service Enter: stop operation after Up press 2", "T.16 operation 3 stopped sample 004"),
	"after the fourth stop": ("service Enter: stop operation after Up press 3", "T.16 operation 4 stopped sample 004"),
}


def _clock_step_end_times(run: dict[str, Any]) -> dict[str, float]:
	"""Time of the last snapshot of each scenario step, keyed by step label (a pulse has a held and a released one)."""
	ends: dict[str, float] = {}
	for snapshot in run["snapshots"]:
		label = snapshot["label"]
		if label.endswith(" (held)"):
			continue
		ends[label] = snapshot["time_s"]
	return ends


def _clock_integrate(run: dict[str, Any], start: float, end: float) -> tuple[dict[str, float], dict[int, int]]:
	events = sorted((e["time_s"], e["number"], e["state"]) for e in run["events"] if e["event"] == "solenoid" and e["number"] in (56, 57))
	state = {56: 0, 57: 0}
	for time, number, value in events:
		if time <= start:
			state[number] = value
	totals = {"56 only": 0.0, "57 only": 0.0, "both": 0.0, "neither": 0.0}
	drops = {56: 0, 57: 0}

	def key() -> str:
		if state[56] and state[57]:
			return "both"
		return "56 only" if state[56] else "57 only" if state[57] else "neither"

	cursor = start
	for time, number, value in events:
		if start < time <= end:
			totals[key()] += time - cursor
			cursor = time
			if state[number] and not value:
				drops[number] += 1
			state[number] = value
	totals[key()] += end - cursor
	return {name: round(seconds, 3) for name, seconds in totals.items()}, drops


def clock_test_windows(run: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
	"""Per named clock-test operation, the seconds each 56/57 combination was on and the number of drops of each output.

	An operation window runs from the snapshot before its start press to the snapshot after its stop press; a
	stopped window covers the four 0.25 s samples that follow the open or stop press.
	"""
	labels = [step["label"] for step in run["steps"]]
	ends = _clock_step_end_times(run)

	def previous_end(label: str) -> float:
		index = labels.index(label)
		return ends[labels[index - 1]]

	operations = {}
	for name, (start_label, stop_label) in CLOCK_TEST_OPERATIONS.items():
		start, end = previous_end(start_label), ends[stop_label]
		totals, drops = _clock_integrate(run, start, end)
		operations[name] = {"start_label": start_label, "seconds": round(end - start, 3), "window": totals, "drops": drops}
	stopped = {}
	for name, (before_label, last_label) in CLOCK_TEST_STOPPED.items():
		start, end = ends[before_label], ends[last_label]
		totals, drops = _clock_integrate(run, start, end)
		stopped[name] = {"end_label": last_label, "seconds": round(end - start, 3), "window": totals, "drops": drops}
	return operations, stopped


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(
	identifier: str,
	role: str,
	positions: list[tuple[float, float]],
	*source_refs: str,
	status: str = "validated",
	placement_refs: list[tuple[str, ...]] | None = None,
) -> dict[str, Any]:
	"""Placements for one device; placement_refs, when given, names the sources of each placement separately."""
	if placement_refs is not None and len(placement_refs) != len(positions):
		raise RuntimeError(f"{identifier}: {len(placement_refs)} placement source lists for {len(positions)} placements")
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		refs = placement_refs[index - 1] if placement_refs is not None else source_refs
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": round(x, 6),
				"y": round(y, 6),
				"provenance": provenance(*refs, status=status),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# Committed crops are binary, so unlike the transcriptions they are hashed from
# the file on disk rather than from a literal in this curator.
EXCERPT_IMAGE_HASHES = {
	path.name: hashlib.sha256(path.read_bytes()).hexdigest()
	for path in sorted((ROOT / "evidence/excerpts/bally.twilight-zone.1993").glob("*.webp"))
}
# Transcriptions added by the 2026-09-26 pass, read from the complete IPDB manual and its amendment.
EXCERPT_TEXT_HASHES = {
	"solenoid-flasher-table.md": "f9bb7c526a04da60952826b1f1b09deb0b74d65db724250d87af9a35b28f836e",
	"clock-test.md": "c4347bdf983e47c2c2f0b0bee5f78cc043cce318c0167baf8a5453c51c7fabe3",
	"backbox-assembly.md": "8c885fb616793087de72215046cea70da95c4c83465d995c395116c9911405f0",
	"clock-assembly.md": "c5d2a1dd0b7a5debeaf9f0eef35ccc23889aae55e2d990805b35b62529ea55a9",
	"mini-playfield-assembly.md": "bf7b8d3c3969e133d9cc369074e9c23c99e02deab535730c4cb19ed48eae24ad",
	"power-driver-connectors.md": "20601e8157af11c2ddd710c399165dff25fae90169e34a70d3074d2bc9d1f572",
	"mini-playfield-switch-drawing.md": "0718b567ff484cd944acee8daab695c8036676c2b376c6ceb9b6538d3139afb2",
	"manual-amendment-clock-assembly.md": "12b29e9d296a2922afe3116701fecb176ca0cf29299e844e12932f29321aa6d1",
	"switch-matrix.md": "7c9737f72045c4325f3d9651f521cd55157de64abd2304cbb2b2cd4746d9af87",
}
_IPDB_EXCERPT_ROOT = "evidence/excerpts/bally.twilight-zone.1993"
_IPDB_READ = "curator, read from the 300 dpi render of the complete IPDB copy; the PDF's OCR layer only located the page"


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the tz_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/tz.c tzGameData GEN_WPCFLIPTRON with wpc_dispDMD, the inverted-switch mask "
				"{0x00 x7, 0x3f, 0x7f, 0x00, 0x00, 0x00, 0xff}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U), the "
				"complete swXxx/sXxx #define block, tz_getSol's CORE_CUSTSOLNO(1..8) external-board dispatch and "
				"CORE_CUSTSOLNO(9) fake gumball-release state, tz_swRowRead (tz.c:586-589, the 9th switch column read from "
				"internal column CORE_CUSTSWCOL), the clock-opto defines CORE_CUSTSWNO(1,1..8) (tz.c:175-182), mechClock's "
				"MECH_TWODIRSOL clock mechanism registered with mech_add (tz.c:601-624), and tz_handleMech, whose gumball-machine "
				"swGeneva derivation (mechanics bit 1) runs while its clock block (tz.c:638-661, an older tick model) is "
				"disabled by #if 0; src/wpc/mech.c:140-145 (the "
				"MECH_TWODIRSOL direction, dir = (sol==1)-(sol==2)); src/wpc/core.h CORE_FIRSTUFLIPSOL=33/"
				"CORE_FIRSTLFLIPSOL=45/CORE_FIRSTCUSTSOL=51/CORE_CUSTSWCOL/CORE_CUSTSWNO/CORE_CUSTSOLNO; src/wpc/core.c "
				"core_getSol's 37-44 branch gated on GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11 only; src/wpc/wpc.c WPC_FLIPPERS "
				"register read (unconditional swMatrix complement for non-WPC95 generations) and wpc.c:1545 (the always-closed "
				"switch 24 set at machine init); "
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
			"locator": "WPC-Fliptronic public switch, DIP, solenoid, lamp, and five-GI address rules, contrasted against WPC-95",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.twilight-zone.1993/archive-arcademanual_Twilight_Zone_OPS/Twilight_Zone_OPS.pdf",
			"original_filename": "Twilight_Zone_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"166-page image-only scan of the Bally Twilight Zone operations manual (16-50020-101, April 1993; "
				"Internet Archive item arcademanual_Twilight_Zone_OPS). Printed page 2-51 (\"Switch Locations "
				"(Continued)\") carries switch items 34-98; page 2-53 (\"Solenoid/Flasher Locations\") carries the "
				"complete solenoid/flasher table, the Flipper Coils list, and the General Illumination Circuits table; "
				"page 2-55 (\"Lamp Locations\") carries the full 64-position lamp matrix. This retained scan carries "
				"only odd-numbered printed pages (for example PDF 40 = 2-9, 58 = 2-45, 64 = 2-57), so every even page "
				"is absent, including the Switch Matrix wiring page (2-50, which also carries switch items 1-33), the "
				"Solenoid/Flasher Table wiring page (2-52), and the Lamp Matrix wiring page (2-54). The retained "
				"manual-transcription.md header states only the narrower 2-48 to 2-54 gap and is stale on that point. "
				f"The complete document is the IPDB copy ({MANUAL_IPDB_SOURCE}); this scan stays cited for the pages "
				"and excerpts already read from it."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.twilight-zone.switch-locations-continued",
					"locator": "PDF page 61, printed 2-51, Switch Locations (Continued), items 34-98",
					"path": "evidence/excerpts/bally.twilight-zone.1993/switch-locations-continued.md",
					"sha256": "efabefdc70c7dbac727ccff4a7f4b7a48c4fa42cceef79d402a1afd3b2d0b80d",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/switch-locations-continued.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-locations-continued.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 61, crop box 0.02,0.085,0.45,0.925, scanned page rendered at its native resolution (embedded image xref 259, 2556px across 8.52in), rendered at 300 dpi, 1097x2773 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.solenoid-flasher-locations",
					"locator": "PDF page 62, printed 2-53, Solenoid/Flasher Locations and Flipper Coils",
					"path": "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-locations.md",
					"sha256": "aa5dad42d4247374b901614d4a007f8d835e4b6c28149374d393a26590773ad1",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-flasher-locations.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 62, crop box 0.02,0.085,0.58,0.885, scanned page rendered at its native resolution (embedded image xref 264, 2562px across 8.54in), rendered at 300 dpi, 1428x2641 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.general-illumination",
					"locator": "PDF page 62, printed 2-53, General Illumination Circuits",
					"path": "evidence/excerpts/bally.twilight-zone.1993/general-illumination.md",
					"sha256": "b0c1ce13a73927da9a1af17af19100ddf9da409cae3e209febe2731d6059020d",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/general-illumination.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["general-illumination.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 62, crop box 0.02,0.665,0.45,0.785, scanned page rendered at its native resolution (embedded image xref 264, 2562px across 8.54in), rendered at 300 dpi, 1097x397 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.lamp-locations",
					"locator": "PDF page 63, printed 2-55, Lamp Locations, full 64-position matrix",
					"path": "evidence/excerpts/bally.twilight-zone.1993/lamp-locations.md",
					"sha256": "9e925d39687cbaf85483d062f4a6f468ad049b944e6c62e581485c56e15ba2eb",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/lamp-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-locations.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 63, crop box 0.02,0.085,0.45,0.87, scanned page rendered at its native resolution (embedded image xref 269, 2550px across 8.50in), rendered at 300 dpi, 1097x2591 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.switch-locations-drawing",
					"locator": "PDF page 61, printed 2-51, Main Playfield Switch Locations drawing",
					"path": "evidence/excerpts/bally.twilight-zone.1993/switch-locations-drawing.md",
					"sha256": "be99f74c549abd99e6a34c06252b290d471d7b3c509b4aabe084a8b8724644c3",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/switch-locations-drawing.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-locations-drawing.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 61, crop box 0.44,0.12,0.9,0.85, scanned page rendered at its native resolution (embedded image xref 259, 2556px across 8.52in), rendered at 300 dpi, grayscale, 1173x2409 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.solenoid-flasher-locations-drawing",
					"locator": "PDF page 62, printed 2-53, Solenoid/Flasher Locations drawings (ramp overlay and main playfield)",
					"path": "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-locations-drawing.md",
					"sha256": "448093daa0058f6f5a2d703ed5bcf523c8b0c7d32f3bb3b0dc1a944a13a6afcf",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-locations-drawing.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-flasher-locations-drawing.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 62, crop box 0.59,0.09,0.97,0.93, scanned page rendered at its native resolution (embedded image xref 264, 2562px across 8.54in), rendered at 300 dpi, grayscale, 970x2772 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.lamp-locations-drawing",
					"locator": "PDF page 63, printed 2-55, Lamp Locations drawing (door panel and cabinet buttons)",
					"path": "evidence/excerpts/bally.twilight-zone.1993/lamp-locations-drawing.md",
					"sha256": "d5444d68fde1c0f56e717d6bf64172330636cb9e897e9b6f8c6a974459617374",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/bally.twilight-zone.1993/lamp-locations-drawing.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-locations-drawing.webp"],
					"image_derivation": "Twilight_Zone_OPS.pdf page 63, crop box 0.45,0.12,0.93,0.87, scanned page rendered at its native resolution (embedded image xref 269, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1225x2475 WebP quality 80",
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with "
				"the rendered PNG page cache under external:pinmame-manuals/rendered/bally.twilight-zone.1993/. The "
				"retained PDF is image-only, so this transcription is the source of record and OCR is never authoritative."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": MANUAL_IPDB_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/2684/Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf",
			"original_filename": "Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf",
			"sha256": MANUAL_IPDB_SHA256,
			"acquired_at": "2026-09-25T22:26:32Z",
			"locator": (
				"Complete 164-page copy of the Bally Twilight Zone operations manual 16-50020-101 (April 1993), 1-bit "
				"300 dpi page scans with an Acrobat Paper Capture OCR layer, from IPDB machine 2684 "
				"(https://www.ipdb.org/machine.cgi?id=2684: Bally 'Twilight Zone', 1993), retained at "
				"external:pinmame-manuals/by-machine/bally.twilight-zone.1993/ipdb-2684/. It carries every page the "
				"Internet Archive scan lacks. PDF page = printed page for the pages used: PDF 26 = 1-18, 72 = 2-4, "
				"100/101 = 2-32/2-33, 108/109 = 2-40/2-41, 118 = 2-50, 120 = 2-52, 121 = 2-53, 159 = 3-33. Every cited "
				"cell was read from native 300 dpi renders (render-ops/); the PDF's OCR layer and a local Windows OCR "
				"pass (ocr-windows-ops/) were used only to find pages."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by IPDB",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.twilight-zone.solenoid-flasher-table",
					"locator": "PDF page 120, printed 2-52, Solenoid/Flasher Table with its General Illumination and Flipper Circuits rows",
					"path": f"{_IPDB_EXCERPT_ROOT}/solenoid-flasher-table.md",
					"sha256": EXCERPT_TEXT_HASHES["solenoid-flasher-table.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
				},
				{
					"id": "excerpt.twilight-zone.clock-test",
					"locator": "PDF page 26, printed 1-18, T.14 Clock Test",
					"path": f"{_IPDB_EXCERPT_ROOT}/clock-test.md",
					"sha256": EXCERPT_TEXT_HASHES["clock-test.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
				},
				{
					"id": "excerpt.twilight-zone.backbox-assembly",
					"locator": "PDF page 72, printed 2-4, Backbox Assembly item list",
					"path": f"{_IPDB_EXCERPT_ROOT}/backbox-assembly.md",
					"sha256": EXCERPT_TEXT_HASHES["backbox-assembly.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
				},
				{
					"id": "excerpt.twilight-zone.clock-assembly",
					"locator": "PDF pages 100-101, printed 2-32 (A-16124 Clock Assembly parts list) and 2-33 (socket detail of the drawing)",
					"path": f"{_IPDB_EXCERPT_ROOT}/clock-assembly.md",
					"sha256": EXCERPT_TEXT_HASHES["clock-assembly.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
					"image": f"{_IPDB_EXCERPT_ROOT}/clock-assembly.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["clock-assembly.webp"],
					"image_derivation": "Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf page 101, crop box 0.385,0.615,0.615,0.85, scanned page rendered at its native resolution (embedded image xref 347, 2562px across 8.54in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 776x588 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.mini-playfield-assembly",
					"locator": "PDF pages 108-109, printed 2-40 (A-16806 Mini-Playfield Assembly parts list) and 2-41 (Street Light socket detail of the front and back views)",
					"path": f"{_IPDB_EXCERPT_ROOT}/mini-playfield-assembly.md",
					"sha256": EXCERPT_TEXT_HASHES["mini-playfield-assembly.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
					"image": f"{_IPDB_EXCERPT_ROOT}/mini-playfield-assembly.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["mini-playfield-assembly.webp"],
					"image_derivation": "Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf page 109, crop box 0.14,0.33,0.62,0.7, scanned page rendered at its native resolution (embedded image xref 376, 2582px across 8.61in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 1221x1224 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.power-driver-connectors",
					"locator": "PDF page 159, printed 3-33, Power Driver Board connector list (continued), J115-J132",
					"path": f"{_IPDB_EXCERPT_ROOT}/power-driver-connectors.md",
					"sha256": EXCERPT_TEXT_HASHES["power-driver-connectors.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
				},
				{
					"id": "excerpt.twilight-zone.mini-playfield-switch-drawing",
					"locator": "PDF page 118, printed 2-50, drawing \"MINI-PLAYFIELD, TOP AND BOTTOM RAMP SWITCH LOCATIONS\"",
					"path": f"{_IPDB_EXCERPT_ROOT}/mini-playfield-switch-drawing.md",
					"sha256": EXCERPT_TEXT_HASHES["mini-playfield-switch-drawing.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
					"image": f"{_IPDB_EXCERPT_ROOT}/mini-playfield-switch-drawing.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["mini-playfield-switch-drawing.webp"],
					"image_derivation": "Bally_1993_Twilight_Zone_Operations_Manual_OCR_searchable.pdf page 118, crop box 0.455,0.54,0.896,0.905, scanned page rendered at its native resolution (embedded image xref 409, 2588px across 8.63in), rendered at 300 dpi, grayscale, 1125x1205 WebP quality 80",
				},
				{
					"id": "excerpt.twilight-zone.switch-matrix",
					"locator": "PDF page 118, printed 2-50, Switch Matrix table and the switch list items F1-F8 and 11-33",
					"path": f"{_IPDB_EXCERPT_ROOT}/switch-matrix.md",
					"sha256": EXCERPT_TEXT_HASHES["switch-matrix.md"],
					"method": "manual",
					"transcribed_by": _IPDB_READ,
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_AMENDMENT_SOURCE,
			"kind": "manual",
			"uri": "https://www.ipdb.org/files/2684/Bally_1993_Twilight_Zone_Manual_Amendment_16_50020_AMD_1.pdf",
			"original_filename": "Bally_1993_Twilight_Zone_Manual_Amendment_16_50020_AMD_1.pdf",
			"sha256": MANUAL_AMENDMENT_SHA256,
			"acquired_at": "2026-09-25T22:26:34Z",
			"locator": (
				"Four-page Twilight Zone Manual Amendment 16-50020-AMD-1 from IPDB machine 2684, retained at "
				"external:pinmame-manuals/by-machine/bally.twilight-zone.1993/ipdb-2684/. Page 3 renumbers the clock "
				"assembly (manual pages 2-32/2-33) to A-16124-1 and its item 13 to A-17047, and changes switch 61's part "
				"(page 2-51) to 5647-12693-57, and page 4 changes the ball popper's opto parts (page 2-25) to A-16909/A-16908 "
				"and adds A-16535 Ramp Prox Opto sensor Assembly to the Lower Playfield Parts list (page 2-47, item 12a); "
				"switches 61, 74 and 57 record these. Its page 2 entry changes the Fliptronic II flipper assembly's "
				"end-of-stroke switch (page 2-20, item 2) to SW-1A-194, a part this definition does not record."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by IPDB",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.twilight-zone.manual-amendment-clock-assembly",
					"locator": "PDF pages 2-4, entries for manual pages 2-20 (flipper switch), 2-25 (Ball Popper optos), 2-32/2-33 (Clock Assembly), 2-47 (item 12a) and 2-51 (switch 61)",
					"path": f"{_IPDB_EXCERPT_ROOT}/manual-amendment-clock-assembly.md",
					"sha256": EXCERPT_TEXT_HASHES["manual-amendment-clock-assembly.md"],
					"method": "manual",
					"transcribed_by": "curator, read from the 300 dpi render; a local OCR pass only located the entry",
					"reviewed": True,
				},
			],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/source/Twilight%20Zone%20%28Bally%201993%29%202.4.5.vpx",
			"original_filename": "Twilight Zone (Bally 1993) 2.4.5.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working recreation \"Skitso Detail mod 2.0\" by Skitso, based on Ninuzzu's original, "
				f"VPX 10.8, save revision 475, released 2018-10-03. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/1082.353 and y/2164.706. This table is wider than the standard VPW WPC "
				"bounds used by other titles in this repository; do not reuse another game's divisor. Geometry "
				"authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "Skitso, based on Ninuzzu's original",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Retained embedded VPX script (4726 lines). Runtime and mechanism-causality authority: cGameName "
				'selects "tz_94ch" (Romset=0, default) or "tz_94h" (Romset=1); Const UseLamps = 1, Const UseSolenoids '
				"= 2; the SolCallback/SolModCallback table for solenoids 1-28, 45-48, and 51-58 with the explicit "
				"printed-item-number cross-reference comments for the auxiliary board (37-44) and clock outputs "
				"(42-44); GiCallback2 UpdateGI mapping GI 0-4 to the l100/l101/l102/(no binding)/l104 playfield "
				"emitter collections; and the per-switch _Hit/_UnHit handlers used to bind public switch addresses "
				"to named playfield trigger/kicker/target objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. Bounds are "
				f"{TABLE_BOUNDS}. Raw per-object coordinates are retained in "
				"external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry.txt, "
				f"SHA-256 {VPX_GEOMETRY_SHA256}, and its supplements "
				"external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-25.txt, "
				f"SHA-256 {VPX_GEOMETRY_SUPPLEMENT_SHA256}, and "
				"external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-25-round3.txt, "
				f"SHA-256 {VPX_GEOMETRY_SUPPLEMENT_2_SHA256}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPX_2020_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/ninuzzu-2020/Twilight%20Zone%20%28Bally%201993%29.vpx",
			"original_filename": "Twilight Zone (Bally 1993).vpx",
			"sha256": TABLE_2020_SHA256,
			"locator": (
				"The contributor's archived copy of ninuzzu's VPX recreation (script header \"VPX recreation by ninuzzu\", "
				"file dated 2020-01-20), copied from the contributor's table archive into the working root. It is the "
				"ancestor of the retained 2.4.5 lineage, so it is not an independent table; it is cited for the objects "
				"the 2.4.5 table dropped (the second sockets of flashers 18, 19, 20 and 41 and the switch walls of 45/46) "
				f"and as corroboration. Exact playfield bounds are {TABLE_2020_BOUNDS}; its objects are normalized by "
				f"x/{BOUNDS_2020_X} and y/{BOUNDS_2020_Y}. 60 same-named Trigger/Kicker/Bumper/Gate/Spinner objects of the "
				"two tables agree to a median 0.004 normalized, 53 of them within 0.01."
			),
			"license": "NOASSERTION",
			"attribution": "ninuzzu, with coindropper, Clark Kent, Flupper and Tom Tower (script credits)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_2020_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/ninuzzu-2020/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_2020_SHA256,
			"locator": (
				"Embedded script of the 2020 ninuzzu table (2899 lines; cGameName tz_94ch or tz_94h). Cited lines: "
				"SolCallback(18/19/20) \"setlamp 118/119/120\" and SolCallback(55) \"setlamp 141\" (lines 1273-1291), "
				"whose NFadeLm 118/119/120/141 lines (2179-2236) drive Light.f18c, f19a, f20c and f41c; sw45_Hit/sw45a_Hit "
				"pulsing 45 and sw46_Hit/sw46a_Hit pulsing 46 (lines 1718-1721); and UpdateGI, which dims the GIMinipf "
				"collection from G.I. string index 1 and GIClock from index 2 (lines 2350-2360)."
			),
			"license": "NOASSERTION",
			"attribution": "ninuzzu and the credited contributors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_2020_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/ninuzzu-2020/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under the 2020 "
				f"table's extracted-vpxtool; manifest SHA-256 {EXTRACTION_2020_MANIFEST_SHA256}; "
				f"{EXTRACTION_2020_FILE_COUNT} files, {EXTRACTION_2020_TOTAL_BYTES} bytes, produced with vpxtool "
				"git:v0.33.3 from a copy of the table in the working root. Raw per-object coordinates are retained in "
				"external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-26.txt, "
				f"SHA-256 {VPX_GEOMETRY_SUPPLEMENT_3_SHA256}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": RUNTIME_CLOCK_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_CLOCK_PATH}",
			"revision": RUNTIME_LIBRARY_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of tz_92 from empty NVRAM (scenario "
				"tools/harness-scenarios/wpc-fliptronic/tz-clock-test.json, --handle-mechanics 0) that opens the ROM's "
				"own clock test (T.16 on this ROM) and starts and stops each of its four operations. While the DMD's top "
				"line reads CLOCK FWD. SLOW or FWD. FAST, public 57 stays on and 56 drops in short bursts; while it reads "
				"CLOCK REV. SLOW or REV. FAST, 56 stays on and 57 drops; while it reads CLOCK STOPPED both stay on. The "
				"evidence file records the seconds each combination was on per operation. With the clock model off the "
				"optos never change, so the run shows which public output the ROM drives for each named operation, not "
				"which way a physical motor turns."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": RUNTIME_CLOCK_MECH_SOURCE,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_CLOCK_MECH_PATH}",
			"revision": RUNTIME_LIBRARY_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of tz_92 from empty NVRAM with PinMAME's own clock model on "
				"(scenario tools/harness-scenarios/wpc-fliptronic/tz-clock-test-mech.json, --handle-mechanics 1, the "
				"retained table's setting), through the same four operations of the ROM's clock test. The ROM holds the "
				"same outputs as in the model-off run (57 on and 56 dropping for CLOCK FWD., 56 on and 57 dropping for "
				"CLOCK REV., both on for CLOCK STOPPED), and its display shows the modelled clock's reading: 0:00 at 12 "
				"HOUR on opening, 0:15 after CLOCK FWD. SLOW, 1:00 after CLOCK FWD. FAST, still 1:00 after CLOCK REV. SLOW, "
				"and 12:00 after CLOCK REV. FAST, with the minute and hour opto boxes changing with it. It shows that "
				"PinMAME's model moves the way the ROM's operation names say for the outputs the ROM holds; the frames show "
				"a model, not a physical clock."
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


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
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
				physical={"location": "coin door", "switch_type": "button", "notes": f"Standard WPC dedicated grounded switch D{address}. {note}"},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			if address == ALWAYS_CLOSED_SWITCH:
				items.append(
					_device(
						f"switch.matrix-{address}",
						"Always Closed",
						"constant",
						"pinmame.input.switch",
						address,
						"used",
						(MANUAL_IPDB_SOURCE, CORE_SOURCE),
						aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
						constant_active=True,
						initial_active=True,
						physical={"switch_type": "other", "notes": ALWAYS_CLOSED_NOTE},
						spatial=not_applicable("constant", MANUAL_IPDB_SOURCE),
						wiring={
							"board": "WPC CPU board",
							"drive_connection": "J206-2",
							"drive_wire": "Green-Red",
							"return_component": "column driver U20-17; row receiver U18-7",
							"return_connection": "J208-4",
							"return_wire": "White-Yellow",
						},
					)
				)
				continue
			label = SWITCH_LABELS.get(address) or UNUSED_MATRIX_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES or label is None
			identifier = f"switch.matrix-{address}"
			part = SWITCH_PARTS.get(address) or SWITCH_PARTS_2_50.get(address, (None, None))[0]
			physical: dict[str, Any] = {}
			if part:
				if "(" in part and "/" in part:
					physical["assembly_part_number"] = part
				else:
					physical["part_number"] = part
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
			elif address in PROXIMITY_SWITCHES:
				physical["switch_type"] = "other"
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += (
					' The switch-locations table (manual page 2-51) marks this position "Not Used" with no switch '
					"or opto assembly part at all; PinMAME's tz_inportData/tz_initSim expose a same-named toggle "
					"(\"Third Magnet\"/\"Big Kick\"/\"Clock Lane\") only for its own internal text-mode ball-tracking "
					"simulator (sim.c), not a real CPU-board DIP switch or documented factory option."
					if address in UNUSED_MATRIX_LABELS
					else " No #define exists for this position anywhere in tz.c's switch list; no other evidence of a fitted device was found."
				)
			elif address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				notes += (
					" Printed with LED/phototransistor opto construction; pinned PinMAME's tzGameData "
					"inverted-switch mask covers this address, so the public switch state is already normalized and "
					"must not be inverted again."
				)
			elif address in OPTO_SWITCHES:
				notes += " Printed with LED/phototransistor opto construction (A-14231/A-14232)."
			elif address in PROXIMITY_SWITCHES:
				notes += (
					f" Printed as part {SWITCH_PARTS[address]} on the switch list (page 2-51), a proximity sensor assembly "
					"under the playfield rather than a leaf switch or an A-14231/A-14232 opto pair, so switch_type is other; "
					"PinMAME's inverted-switch mask leaves this column at 0x00 (not normalized)."
				)
			elif address in SWITCH_PARTS:
				notes += " Printed as a plain mechanical switch/target part; PinMAME's inverted-switch mask leaves this column at 0x00 (not normalized)."
			elif address in SWITCH_PARTS_2_50:
				printed_part, printed_name = SWITCH_PARTS_2_50[address]
				notes += (
					f" Page 2-50 of the complete IPDB copy lists item {address} as part {printed_part}, \"{printed_name}\" "
					"(the Internet Archive scan lacks that page); PinMAME's inverted-switch mask leaves this column at "
					"0x00 (not normalized)."
				)
			else:
				raise RuntimeError(f"Twilight Zone switch {address} has no printed part or disposition")
			if address in UNDERSIDE_SWITCHES:
				notes += " Located on the underside of the playfield (manual dagger footnote)."
			if address in NOT_SHOWN_SWITCHES:
				notes += " Not shown on the printed switch-locations diagram (manual asterisk footnote)."
			if address in AMENDMENT_NOTES:
				notes += AMENDMENT_NOTES[address]
			if address == 65:
				notes += " Power Payoff is a two-target bank sharing one public switch (manual \"(2)\")."
			if address in SWITCH_LABEL_ALIASES:
				notes += (
					" Labelled with page 2-50's printed name; earlier revisions of this definition used the retained "
					f"script's \"{SWITCH_LABEL_ALIASES[address]}\", kept as an alias."
				)
			if not unused:
				notes += (
					f" Matrix wiring from the page 2-50 headings: column {column} {MATRIX_COLUMN_WIRING[column][0]} "
					f"{MATRIX_COLUMN_WIRING[column][1]} (driver {MATRIX_COLUMN_WIRING[column][2]}), row {row} "
					f"{MATRIX_ROW_WIRING[row][0]} {MATRIX_ROW_WIRING[row][1]} (receiver {MATRIX_ROW_WIRING[row][2]})."
				)
			physical["notes"] = notes

			aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
			if address in SWITCH_LABEL_ALIASES:
				aliases.append({"namespace": "vpx-script.label", "value": SWITCH_LABEL_ALIASES[address]})
			extra: dict[str, Any] = {
				"aliases": aliases,
				"physical": physical,
			}
			if not unused:
				extra["wiring"] = matrix_wiring(column, row)
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE if address in UNUSED_MATRIX_LABELS else CORE_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE) if address in UNUSED_MATRIX_LABELS else (CORE_SOURCE,)
				label = f"Not Used Matrix Position {address}" if label is None else f"{label} (Not Used)"
			else:
				availability = "used"
				extra["normally_closed"] = address in PINMAME_NORMALIZED_OPTO_SWITCHES
				if address in PULSED_SWITCHES:
					extra["pulse"] = True
				refs = (CORE_SOURCE, VPX_SCRIPT_SOURCE) if address in SWITCH_PARTS or address in SWITCH_POSITIONS else (CORE_SOURCE,)
				if address in SWITCH_PARTS:
					refs = (MANUAL_SOURCE,) + refs
				if address in {13, 14, 21, 22, 23}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", CORE_SOURCE)
					physical["location"] = "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address in UNPLACED_SWITCHES:
					physical["notes"] += " " + UNPLACED_SWITCHES[address]
				elif address in SWITCH_POSITIONS:
					extra["spatial"] = _switch_spatial(identifier, address, physical)
					if address in SWITCH_2020_PLACEMENTS:
						refs = refs + (VPX_2020_SCRIPT_SOURCE, MANUAL_IPDB_SOURCE)
				else:
					raise RuntimeError(f"Twilight Zone switch {address} has neither a placement nor an explicit unplaced reason")
				if address in SWITCH_EXTRA_NOTES:
					physical["notes"] += " " + SWITCH_EXTRA_NOTES[address]
				# The page 2-50 part numbers (11-33) and matrix wiring (every used matrix switch) come from the IPDB copy.
				if MANUAL_IPDB_SOURCE not in refs:
					refs = refs + (MANUAL_IPDB_SOURCE,)
				if address in AMENDMENT_NOTES:
					refs = refs + (MANUAL_AMENDMENT_SOURCE,)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	for address, (label, role, availability) in FLIPPER_LABELS.items():
		is_button = role.endswith(".button")
		physical = {
			"location": "cabinet flipper button" if is_button else "flipper assembly",
			"switch_type": "opto" if is_button else "leaf",
			"notes": (
				f"Printed Fliptronic grounded switch F{address - 110}. WPC_FLIPPERS unconditionally complements the "
				"flipper switch column for this hardware generation (no WPC-95-specific register is required), so "
				"the public state is already normalized."
			),
		}
		if is_button:
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			# The repository-wide convention for end-of-stroke contacts (The Addams Family, Monster Bash,
			# Medieval Madness, Attack From Mars): an internal part of the flipper assembly, paired with its
			# internal.* role. The flipper's position is carried by its coils.
			physical["notes"] += (
				" The end-of-stroke contact is internal to the flipper assembly; the flipper's playfield position "
				"is carried by its power/hold coil placements."
			)
			spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"F{address - 110}"},
				],
				roles=[role],
				normally_closed=False,
				physical=physical,
				spatial=spatial,
			)
		)

	# Custom switch column (CORE_CUSTSWCOL, internal column 12), public addresses 121-128: the eight clock-position
	# optos on the Minute (printed 91-94) and Hour (printed 95-98) opto PC boards.
	for printed, address in CLOCK_OPTO_PUBLIC.items():
		row = printed - 90
		label = SWITCH_LABELS[printed]
		identifier = f"switch.custom-{address}"
		part = SWITCH_PARTS[printed]
		drive_wire, drive_connection, driver = CLOCK_COLUMN_WIRING
		return_wire, return_connection, receiver = MATRIX_ROW_WIRING[row]
		physical = {
			"switch_type": "opto",
			"part_number": part,
			"notes": (
				f"Clock opto, printed as switch {printed} in the \"9th column\" of the switch matrix (pages 1-18 and "
				f"2-50; kept as a manual.address alias). tz.c:175-182 defines it as CORE_CUSTSWNO(1,{row}), and "
				f"core.h:347 makes that public {address}: CORE_CUSTSWCOL = CORE_STDSWCOLS = 12, so the first custom "
				"column is 121-128 and the printed column number is not the PinMAME address. tz_swRowRead "
				"(tz.c:586-589) returns coreGlobals.swMatrix[CORE_CUSTSWCOL] whenever bit 7 of the WPC_EXTBOARD1 "
				"register enables the 9th column, so a host write to the printed number would land in internal column 9, "
				f"which the ROM never reads. Printed with opto-board construction ({part}, {CLOCK_OPTO_BOARD[part]}). Not shown on the printed switch-locations diagram (manual asterisk "
				"footnote). tzGameData's inverted-switch mask sets the Cust entry, internal column 12, to 0xff, so "
				"121-128 are inverted (column 9's entry is 0x00), and the public switch state is already normalized "
				"and must not be inverted again. Matrix wiring from the page 2-50 headings and the page 1-18 clock "
				f"test: column 9 {drive_wire} from J5-1 of the 8-Driver Board A-16100 (page 2-50 footnote \"* Located "
				"on 8 Driver P.C.B., A-16100, in backbox\"; page 2-50 prints no driver pin, page 1-18 says the column "
				"is driven by Q1 and Q12 of that board, and page 2-52 prints the same Gry-Wht *J5-1 on item 44, Clock "
				f"Switch Strobe, public solenoid 58), row {row} {return_wire} {return_connection} (receiver {receiver})."
			),
		}
		spatial = _switch_spatial(identifier, printed, physical)
		items.append(
			_device(
				identifier,
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, MANUAL_IPDB_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": str(printed)},
				],
				normally_closed=True,
				physical=physical,
				spatial=spatial,
				wiring={
					"board": "Minute/Hour Opto P.C.B. via 8-Driver PCB A-16100 (column) and WPC CPU board (row)",
					"drive_connection": drive_connection,
					"drive_wire": drive_wire,
					"return_component": f"column driver {driver}; row receiver {receiver}",
					"return_connection": return_connection,
					"return_wire": return_wire,
				},
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
				(CONTROLLER_SOURCE, CORE_SOURCE),
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
				spatial=not_applicable("dip_switch", CORE_SOURCE),
			)
		)
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 60):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label if fitted else f"{label} (Not Fitted)")
			kind = "flasher" if address in FLASHER_ADDRESSES else "motor" if address in {56, 57, 24} else "coil"
			if address in CONTROL_SIGNAL_SOLENOIDS:
				kind = "control_signal"
			if address in {33, 34, 35, 36, 45, 46, 47, 48}:
				kind = "coil"
			physical: dict[str, Any] = {}
			coil_part = SOLENOID_COIL_PART.get(address)
			if coil_part and kind != "flasher":
				physical["part_number"] = coil_part
			assembly = SOLENOID_ASSEMBLIES.get(address)
			if assembly:
				physical["assembly_part_number"] = assembly
			if address in MANUAL_SOLENOID_ALIASES:
				notes = (
					f"Printed solenoid/flasher-locations item {MANUAL_SOLENOID_ALIASES[address]}, the auxiliary board's "
					f"callout number for public solenoid {address}."
				)
			elif address in {33, 34, 35, 36, 45, 46, 47, 48}:
				notes = (
					"Not an item of the page 2-53 solenoid/flasher-locations table; the flipper coil is listed in the "
					"Flipper Coils table on the same page."
				)
			else:
				notes = f"Printed solenoid/flasher-locations item {address:02d}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if address == 22:
				notes += (
					' The manual prints no coil number and no assembly number at all ("----"/"----"), the strongest '
					"\"not fitted\" signature in its convention. The retained script's own comment marks its "
					'SolCallback "(22) Upper Right Magnet (*)" with a footnote reading "only in prototype, supported '
					'by rom 9.4" -- i.e. the ROM can drive this coil, but this physical machine does not have it '
					"installed. Matches switch 82 (also Not Used)."
				)
			if address in CLOCK_DRIVE_NOTES:
				notes += " " + CLOCK_DRIVE_NOTES[address]
			if address == 58:
				notes += (
					" Strobes the eight custom clock-position optos (public 121-128, printed 91-98): page 2-52 prints this item's "
					"connection as Gry-Wht *J5-1, the same wire and 8-Driver pin page 2-50 prints as the switch matrix's "
					"9th-column drive. Not driven by the retained VPX script (handled "
					"entirely by PinMAME's own mechClock simulation). It is a logic-level strobe line into the clock opto "
					"boards rather than an actuator or an emitter, so it is typed control_signal and, like every "
					"control_signal output, carries an internal_nonvisual spatial record: there is no device of its own "
					"to place. The optos it strobes are placed on switches 121-128."
				)
			if address == 59:
				notes += " Software-only state, not a real coil; PinMAME's tz_getSol special-cases it and the retained script comment calls it \"unreliable with SolModCallbacks\"."
			physical["notes"] = notes

			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
			if not fitted:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				availability = "used"
				role = "emitter" if kind == "flasher" else "effect"
				if kind == "flasher" and address in FLASHER_PRINTED_QUANTITY:
					physical["quantity"] = FLASHER_PRINTED_QUANTITY[address]
				if address in SOLENOID_POSITIONS:
					positions = SOLENOID_POSITIONS[address]
					if kind == "flasher":
						printed = physical.setdefault("quantity", len(positions))
						if printed != len(positions):
							raise RuntimeError(f"Twilight Zone flasher {address} quantity {printed} does not match {len(positions)} placements")
					refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
					if address in SOLENOID_PLACEMENT_NOTES:
						physical["notes"] += " " + SOLENOID_PLACEMENT_NOTES[address]
						refs = refs + (MANUAL_SOURCE,)
					if address in {56, 57}:
						refs = refs + (MANUAL_IPDB_SOURCE,)
					extra["spatial"] = located(
						identifier, role, positions, *refs, placement_refs=SOLENOID_PLACEMENT_REFS.get(address)
					)
				elif address == 7:
					physical["notes"] += " " + KNOCKER_NOTE
					extra["roles"] = ["cabinet.knocker"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_IPDB_SOURCE, MANUAL_SOURCE)
				elif address in UNPLACED_SOLENOIDS:
					physical["notes"] += " " + UNPLACED_SOLENOIDS[address]
				elif kind == "control_signal":
					extra["roles"] = ["internal.clock-opto-strobe"]
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE, MANUAL_SOURCE)
				else:
					raise RuntimeError(f"Twilight Zone solenoid {address} has neither a placement nor an explicit unplaced reason")
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {7, 18, 19, 20, 55}:
				refs = refs + (MANUAL_IPDB_SOURCE,)
			if address in {18, 19, 20, 55}:
				refs = refs + (VPX_2020_SCRIPT_SOURCE,)
			if address in CLOCK_DRIVE_NOTES:
				refs = (MANUAL_SOURCE, MANUAL_IPDB_SOURCE, RUNTIME_CLOCK_SOURCE, RUNTIME_CLOCK_MECH_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a Twilight Zone playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Twilight Zone playfield device.",
			31: "tz.c does not configure wpc_set_fastflip_addr, so PinMAME publishes WPC_GILAMPS bit 7 here. It is meaningful WPC state but not a physical Game-On relay on this Fliptronic generation.",
			32: "PinMAME reports this WPC state channel as always zero.",
			49: "PinMAME's simulator-only ball-shooter channel; no WPC-Fliptronic hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary (CORE_FIRSTCUSTSOL=51).",
			59: "PinMAME's fake gumball-release solenoid, driven from software state rather than a real coil; the retained script comments it out as \"unreliable with SolModCallbacks\".",
		}.get(address, (
			"Unlike WPC-95, this WPC-Fliptronic generation has no integrated LPDC board: pinned PinMAME's core_getSol "
			"dispatch only serves 37-44 for GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11, and Twilight Zone's own tz_getSol hook "
			"does not claim this address either, so it is simply unused address space on this machine."
		))
		roles = ["internal.wpc-state"] if address in {29, 30, 31} else ["internal.unused.wpc-output"]
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
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly = LAMP_ASSEMBLIES[address]
			bulb = LAMP_BULB.get(address)
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			else:
				notes += " Manual prints no separate bulb number (cabinet button lamp, integral to the illuminated button assembly)."
			if address in LAMP_DOOR_INSERTS:
				notes += (
					" Printed suffix \"(Door)\" names the playfield's central door-panel insert group, not the cabinet coin "
					"door: the manual's Lamp Locations drawing (page 2-55) prints callouts 11-18 and 21-28 on the inserts "
					"around the door panel in the middle of the playfield, and the retained script maps the matching "
					"Light objects l11-l28 by TimerInterval through vpmMapLights AllLamps."
				)
			if address in LAMP_NOT_SHOWN:
				notes += " Not shown on the printed lamp-locations diagram (manual asterisk footnote)."
			if address in {87, 88}:
				notes += (
					" Cabinet button lamp inside the illuminated buy-in/credit button assembly; the manual's Lamp "
					"Locations drawing (page 2-55) prints callouts 87 and 88 below the playfield outline, at the cabinet "
					"front."
				)
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": f"{address:02d}"},
				],
				"physical": physical,
			}
			if address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.credit"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in LAMP_DOOR_INSERTS:
				availability = "used"
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
			else:
				availability = "used"
				if address not in LAMP_POSITIONS:
					raise RuntimeError(f"Twilight Zone lamp {address} has no placement")
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


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, label in GI_LABELS.items():
		identifier = f"gi.string-{address + 1}"
		coil_number = GI_COIL_NUMBER[address]
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed coil/flasher number {coil_number}."
		notes += " " + GI_WIRING_NOTES[address]
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
		}
		physical: dict[str, Any] = {}
		refs = (MANUAL_SOURCE, MANUAL_IPDB_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's GI emitter collection for this string (UpdateGI in the retained "
				"script)."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 1:
			notes += " " + GI_MINI_PLAYFIELD_BLOCKER
		elif address == 2:
			physical["quantity"] = len(GI_CLOCK_POSITIONS)
			notes += " " + GI_CLOCK_PLACEMENT_NOTE
			extra["spatial"] = located(
				identifier, "emitter", GI_CLOCK_POSITIONS, VPX_TABLE_SOURCE, MANUAL_IPDB_SOURCE, MANUAL_AMENDMENT_SOURCE, MANUAL_SOURCE,
				status="observed",
			)
			refs = refs + (MANUAL_AMENDMENT_SOURCE, VPX_2020_SCRIPT_SOURCE)
		else:
			notes += (
				" The printed description \"Insert Main\" names the backbox insert board, the lamp board behind the "
				"translite, and the wiring agrees: this is the only string whose page 2-52 row fills the Backbox columns "
				"alone (J-120-5 and J-120-10, no Playfield connection), and the power driver board's connector list "
				"(page 3-33) sends its Green return J120-5 \"Return G.I. to insert\". The retained script's UpdateGI "
				"case 3 has an empty body, so the table models no playfield emitter for it either."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_IPDB_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
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
				refs,
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
			"Four-position ball trough and release",
			"kicker",
			[output_id("Ball Release"), output_id("Outhole")],
			["switch.matrix-15", "switch.matrix-16", "switch.matrix-17", "switch.matrix-25", "switch.matrix-18"],
			"A ball drains through the Outhole (18) into the trough, which the retained script's UpdateTrough logic "
			"walks through Far Left Trough (25), Left Trough (17), Center Trough (16), and Right Trough (15) at the "
			"eject end. Solenoid 9 (Ball Release) ejects the ball resting on switch 15 into the shooter lane; "
			"solenoid 8 (Outhole) kicks a drained ball from 18 into the trough chain.",
			[
				("outhole", "Outhole", ["switch.matrix-18"], "Ball drains here before entering the trough."),
				("far-left", "Far Left Trough", ["switch.matrix-25"], "Fourth/entry trough position."),
				("left", "Left Trough", ["switch.matrix-17"], "Third trough position."),
				("center", "Center Trough", ["switch.matrix-16"], "Second trough position."),
				("right", "Right Trough (eject)", ["switch.matrix-15"], "Ball nearest the release coil."),
			],
			VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16313",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto-fire kicker",
			"kicker",
			[output_id("Auto-Fire Kicker")],
			["switch.matrix-72"],
			"The ball released from the trough rests on shooter-lane opto 72 (Auto-Fire Kicker) and solenoid 3 fires "
			"it onto the playfield; there is no manual plunger. The retained script's AutoPlungerKicker_Hit/"
			"SolAutoKicker handlers pulse switch 72 and drive the kicker.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-72"], "Auto-fire kicker opto.")],
			VPX_SCRIPT_SOURCE, CORE_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16647",
		),
		mechanism(
			"mechanism.gumball-machine",
			"Gumball machine",
			"toy",
			[output_id("Gumball Popper"), output_id("Gumball Diverter"), output_id("Gumball Motor")],
			["switch.matrix-51", "switch.matrix-55", "switch.matrix-56", "switch.matrix-74", "switch.matrix-87"],
			"A ball diverted by solenoid 6 (Gumball Diverter) enters the gumball lane (switch 51), is caught by the "
			"Gumball Popper opto (switch 74) and kicked by solenoid 4 into the gumball wheel; a real gumball then "
			"enters the machine (switch 87, Gumball Enter opto) and travels to the exit (switch 56, Gumball Exit) "
			"where it is released to the player. Solenoid 24 turns the internal gumball motor; switch 55 (Gumball "
			"Geneva, on the underside beneath the gumball machine) senses the motor's geneva-gear position. Pinned "
			"PinMAME's tz_handleMech drives it synthetically from an internal position counter, and the retained table "
			"also pulses it itself: SolGumballMotor schedules SolGumRelease 1.7 s after solenoid 24 turns on, and "
			"SolGumRelease calls vpmtimer.PulseSw 55 (script.vbs line 2401) -- a behaviour of the table, not a Hit "
			"event from a switch object. Its spatial record is a projection onto the gumball machine assembly. PinMAME's "
			"tz_getSol also exposes a fake CORE_CUSTSOLNO(9) "
			"\"gumball release\" state used only to simplify emulator-side sequencing, not a real coil.",
			[
				("lane", "Gumball popper lane", ["switch.matrix-51"], "Ball enters the lane leading to the popper."),
				("popper", "Gumball popper", ["switch.matrix-74"], "Ball caught and kicked into the gumball wheel."),
				("enter", "Gumball enter", ["switch.matrix-87"], "A dispensed gumball enters the delivery chute."),
				("exit", "Gumball exit", ["switch.matrix-56"], "Gumball reaches the player-accessible exit."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16132",
		),
		mechanism(
			"mechanism.clock",
			"Motorized analog clock",
			"motorized",
			[output_id("Clock Reverse"), output_id("Clock Forward")],
			[
				"switch.custom-121", "switch.custom-122", "switch.custom-123", "switch.custom-124",
				"switch.custom-125", "switch.custom-126", "switch.custom-127", "switch.custom-128",
			],
			"A bidirectional DC gearmotor drives a physical analog clock hand through the D.C. Motor Control Board "
			"A-16120, which the clock test text on page 1-18 places under the playfield at about the clock's position. Two "
			"drives of the 8-Driver Board control it: with only drive 43 (public 57, Clock Forward) on the clock moves "
			"forward, with only drive 42 (public 56, Clock Reverse) on it moves in reverse, and with both on or both off it "
			"stops (page 1-18). The ROM's own clock test holds both on while it reports CLOCK STOPPED and, while it runs "
			"an operation, keeps one on and drops the other in short bursts: 57 stays on for CLOCK FWD. SLOW/FAST and 56 "
			"for CLOCK REV. SLOW/FAST, with more bursts and more time on one drive alone in the fast modes (runtime.twilight-zone.clock-test). "
			"The position optos are strobed by solenoid 58 (Clock Switch Strobe, A-16100). "
			"Eight opto sensors on Minute (A-16220, public 121-124) and Hour (A-16219, public 125-128) opto PC "
			"boards report clock-hand position. The manual prints them as a 9th switch column numbered 91-98; PinMAME "
			"publishes them in its first custom column, internal column 12, whose inversion mask is 0xff. "
			"Pinned PinMAME models this clock itself when mechanics handling bit 0 is on, which the retained table sets "
			"(Controller.HandleMechanics = 1): init_tz registers mechClock with mech_add(0, &mechClock) (tz.c:601-624), "
			"a MECH_TWODIRSOL|MECH_FAST model whose own step-range table drives the eight clock optos, and "
			"Controller.GetMech(0) reports its position, which the retained script's UpdateClock reads to turn the "
			"hands; the script does not drive the clock switches itself. The #if 0 block in tz_handleMech "
			"(tz.c:638-661) is an older, disabled tick model. mech.c:140-145 takes sol1 = sClockRev = public 57 and "
			"sol2 = sClockFwd = public 56 and sets dir = (sol==1)-(sol==2), so the model runs forward on 57 alone and "
			"back on 56 alone; only tz.c's #define names (sClockFwd = 56, sClockRev = 57) read backwards, a PinMAME "
			"naming defect rather than a disagreement about the machine. With the model on, the ROM's clock test shows "
			"the time and the minute and hour opto boxes advancing under CLOCK FWD. and falling back under CLOCK REV. "
			"FAST (runtime.twilight-zone.clock-test-mech).",
			[
				("minute-15", "Clock 15 minutes", ["switch.custom-121"], "Minute-hand opto."),
				("minute-0", "Clock 0 minutes", ["switch.custom-122"], "Minute-hand opto."),
				("minute-45", "Clock 45 minutes", ["switch.custom-123"], "Minute-hand opto."),
				("minute-30", "Clock 30 minutes", ["switch.custom-124"], "Minute-hand opto."),
				("hour-1", "Clock hour 1", ["switch.custom-125"], "Hour-hand opto bit 1."),
				("hour-2", "Clock hour 2", ["switch.custom-126"], "Hour-hand opto bit 2."),
				("hour-3", "Clock hour 3", ["switch.custom-127"], "Hour-hand opto bit 3."),
				("hour-4", "Clock hour 4", ["switch.custom-128"], "Hour-hand opto bit 4."),
			],
			CORE_SOURCE, MANUAL_SOURCE, MANUAL_IPDB_SOURCE, RUNTIME_CLOCK_SOURCE, RUNTIME_CLOCK_MECH_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16120",
		),
		mechanism(
			"mechanism.magnets",
			"Left, lower-right, and upper-right playfield magnets",
			"other",
			[output_id("Left Magnet"), output_id("Lower Right Magnet"), output_id("Upper Right Magnet (Not Fitted)")],
			["switch.matrix-83", "switch.matrix-81"],
			"Three eddy-current magnets guide the ball for the Spiral/Battle the Power shots and Powerball detection. "
			"Solenoid 21 (Left Magnet, switch 83) and solenoid 23 (Lower Right Magnet, switch 81) are fitted on this "
			"machine. Solenoid 22 and switch 82 (Upper Right Magnet) are both printed \"Not Used\" with no part "
			"number at all; the retained script's own comment marks the ROM callback \"(*) only in prototype, "
			"supported by rom 9.4\", i.e. the ROM can drive a third magnet, but this physical machine does not carry "
			"it. No manual/schematic evidence of a fitted production variant was found.",
			[
				("left", "Left magnet", ["switch.matrix-83"], "Left magnet position opto."),
				("lower-right", "Lower right magnet", ["switch.matrix-81"], "Lower right magnet position opto."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="20-9247",
		),
		mechanism(
			"mechanism.mini-playfield",
			"Upper mini-playfield",
			"other",
			[output_id("Left Mini-Playfield Magnet"), output_id("Right Mini-Playfield Magnet")],
			[
				"switch.matrix-44", "switch.matrix-42", "switch.matrix-75", "switch.matrix-76",
				"switch.matrix-43", "switch.matrix-45", "switch.matrix-46",
			],
			"A raised second playfield reached through the Mini-Playfield Enter opto (44). Two eddy-current magnets "
			"(solenoid 25 Left, solenoid 26 Right) manipulate the ball around the mini-playfield's own Camera/"
			"Mini-Playfield Top Hole (42, also colloquially \"the camera\" per the retained script's own comment), "
			"Player Piano target (43), and Mini-Playfield Top/Exit optos (75/76). Switches 45/46 (Mini-Playfield "
			"Left/Right) are two contacts each (page 2-51 \"(2)\"): the page 2-50 mini-playfield switch drawing puts one "
			"balloon of each on the side rail and one on the bottom rail of its own side, and the 2020 ninuzzu table "
			"models them as invisible hit walls sw45/sw45a and sw46/sw46a whose handlers pulse 45 and 46. The retained "
			"2.4.5 script keeps the same sw45_Hit/sw45a_Hit/sw46_Hit/sw46a_Hit handlers but its extraction has no such "
			"objects, so that table never asserts either switch.",
			[
				("enter", "Mini-playfield enter", ["switch.matrix-44"], "Ball leaves the main playfield for the mini-playfield."),
				("camera", "Camera / mini-playfield top hole", ["switch.matrix-42"], "Also called the Camera switch in the retained script's own comment."),
				("piano", "Player piano", ["switch.matrix-43"], "Piano keys standup target."),
				("top", "Mini-playfield top", ["switch.matrix-75"], "Upper mini-playfield opto."),
				("exit", "Mini-playfield exit", ["switch.matrix-76"], "Ball returns to the main playfield."),
			],
			MANUAL_SOURCE, MANUAL_IPDB_SOURCE, VPX_SCRIPT_SOURCE, VPX_2020_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16749",
		),
		mechanism(
			"mechanism.ball-lock",
			"Three-position ball lock",
			"kicker",
			[output_id("Lock Release")],
			["switch.matrix-88", "switch.matrix-84", "switch.matrix-85"],
			"A three-ball lock with Lower (88), Center (84), and Upper (85) position optos; solenoid 15 (Lock "
			"Release) kicks locked balls back into play. Center and Upper positions use opto construction "
			"(A-14231/A-14232); Lower uses a plain switch part (5647-12133-11).",
			[
				("lower", "Lock lower", ["switch.matrix-88"], "Entry/lowest lock position."),
				("center", "Lock center", ["switch.matrix-84"], "Middle lock position."),
				("upper", "Lock upper", ["switch.matrix-85"], "Furthest/highest lock position."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16307",
		),
		mechanism(
			"mechanism.slot-machine",
			"Slot machine",
			"toy",
			[output_id("Slot Kickout")],
			["switch.matrix-57", "switch.matrix-58"],
			"A ball entering the slot machine crosses proximity switch 57 (underside of the playfield) and rests on "
			"kickout opto 58; solenoid 1 (Slot Kickout) returns it to the playfield. The retained script's "
			"SlotMachine_Hit/SlotMachineKickout handlers drive the slot-reel animation and kickout together.",
			[
				("proximity", "Slot proximity", ["switch.matrix-57"], "Underside-of-playfield entry sensor."),
				("kickout", "Slot kickout", ["switch.matrix-58"], "Ball held for kickout."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16434",
		),
		mechanism(
			"mechanism.ramp-diverters",
			"Left and right ramp diverters",
			"diverter",
			[output_id("Left Ramp Diverter"), output_id("Right Ramp Diverter")],
			["switch.matrix-53", "switch.matrix-73"],
			"Solenoid 27 (Left Ramp Diverter) and solenoid 5 (Right Ramp Diverter) route balls entering the left "
			"ramp (switch 53) and right ramp (switch 73) between alternate paths, including the Spiral loop and the "
			"mini-playfield entrance.",
			[
				("left", "Left ramp diverter", ["switch.matrix-53"], "Left ramp entry."),
				("right", "Right ramp diverter", ["switch.matrix-73"], "Right ramp entry."),
			],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16361",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Lower Jet Bumper"), output_id("Left Jet Bumper"), output_id("Right Jet Bumper")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33"],
			"Three A-9415-2 jet bumpers. By the manual's location drawings, the left bumper carries switch 31 "
			"(page 2-51) and coil 13 (page 2-53), the upper-right bumper switch 32 and coil 14, and the lower bumper "
			"switch 33 and coil 12; the retained script binds Bumper1/Bumper2/Bumper3 to switches 31/32/33 in the "
			"same left/upper-right/lower order. Which coil the ROM fires for each switch is not asserted beyond this "
			"co-location. The retained script leaves the three coil SolCallback entries commented out because the "
			"table's native VPX bumper physics handles them directly.",
			[
				("left", "Left jet bumper", ["switch.matrix-31"], "Left of the nest; coil 13 by location."),
				("right", "Right jet bumper", ["switch.matrix-32"], "Upper right of the nest; coil 14 by location."),
				("lower", "Lower jet bumper", ["switch.matrix-33"], "Closest to the player; coil 12 by location."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-34", "switch.matrix-35"],
			"Each slingshot assembly carries a kick switch (SW-1A-114) and a separate scored switch (SW-1A-120). "
			"Solenoid 11 fires the Left Slingshot (switch 34) and solenoid 10 the Right Slingshot (switch 35); the "
			"retained script leaves both SolCallback entries commented out because native VPX slingshot physics "
			"handles them directly (Wall.LeftSlingShot / Wall.RightSlingShot).",
			[
				("left", "Left slingshot", ["switch.matrix-34"], "Left slingshot."),
				("right", "Right slingshot", ["switch.matrix-35"], "Right slingshot."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-16645-L",
		),
		mechanism(
			"mechanism.flippers",
			"Two lower and two upper Fliptronic flippers",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
				output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold"),
				output_id("Upper Left Flipper Power"), output_id("Upper Left Flipper Hold"),
			],
			[
				"switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114",
				"switch.generic-115", "switch.generic-116", "switch.generic-117", "switch.generic-118",
			],
			"Four Fliptronic flippers: two lower (FL-15411 orange, A-15205-L-4/R-4) and two upper (FL-11753 yellow "
			"upper-left A-15205-L-1, FL-11722 green upper-right A-15205-R-3), confirmed by the manual's printed "
			"\"Flipper Coils\" list and by tzGameData's FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L|FLIP_U). Each flipper "
			"has a separate power and hold winding: the ROM energizes the power winding on the cabinet button opto, "
			"then drops to the hold winding once the end-of-stroke leaf switch closes. Const UseSolenoids = 2 in the "
			"retained script means the ROM drives the coils directly (fast flips).",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "EOS 111, button 112."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "EOS 113, button 114."),
				("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "EOS 115, button 116."),
				("upper-left", "Upper left flipper", ["switch.generic-117", "switch.generic-118"], "EOS 117, button 118."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-15205-L-4",
		),
		mechanism(
			"mechanism.rocket-kicker",
			"Rocket kicker",
			"kicker",
			[output_id("Rocket Kicker")],
			["switch.matrix-28"],
			"A ball resting on switch 28 (Rocket Kicker) is fired by solenoid 2 up the right orbit toward the "
			"Hitchhiker lane.",
			[("held", "Ball in the rocket kicker", ["switch.matrix-28"], "Rocket kicker switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16647",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	# conflict.clock-motor-direction-naming was withdrawn on 2026-09-26: the manual's clock test text (page 1-18), its
	# solenoid table (pages 2-52/2-53), the retained script's cross-reference and the ROM's own clock test agree that
	# public 56 is Clock Reverse and 57 Clock Forward. Only pinned PinMAME's unused tz.c #define names read the other
	# way, which is a PinMAME naming defect, not a disagreement about the machine (runbook "What is not a conflict").
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
			"id": "bally.twilight-zone.1993",
			"name": "Twilight Zone",
			"manufacturer": "Bally",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 2684,
			"opdb_id": "GrXzD-MjBPX",
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "observed",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
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
		"knowledge": {"path": "knowledge/bally/twilight-zone-1993.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Twilight Zone device identifiers are not unique: {duplicates}")
	return definition


def _unplaced_reason(device: dict[str, Any]) -> str:
	group = device["binding"]["group"]
	address = int(device["binding"]["device"])
	if group == "pinmame.input.switch" and address in UNPLACED_SWITCHES:
		return UNPLACED_SWITCHES[address]
	if group == "pinmame.output.solenoid" and address in UNPLACED_SOLENOIDS:
		return UNPLACED_SOLENOIDS[address]
	if group == "pinmame.output.gi" and address == 1:
		return (
			"Mixed mini-playfield + backbox insert string with no bulb list: the Mini-Playfield Assembly A-16806 (pages "
			"2-40/2-41) shows a #555 socket (item 10, yellow sleeve item 49) in the Street Light and item 10's leader to a "
			"second socket in its back view, with no printed quantity; the 2020 table's GIMinipf collection includes "
			"Light20/Light43 on main-playfield jet bumpers 1 and 2, so its membership is an author's choice, and the 2.4.5 "
			"table binds a single light (l101). Resolution: a continuity or bulb survey of G.I. string 02 on a physical "
			"machine."
		)
	raise RuntimeError(f"Twilight Zone device {device['id']} has no spatial record and no documented reason")


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved: list[dict[str, Any]] = []
	placement_count = 0
	for collection in ("inputs", "outputs"):
		for device in definition[collection]:
			group = device["binding"]["group"]
			address = int(device["binding"]["device"])
			spatial = device.get("spatial")
			if spatial is None:
				unresolved.append({"group": group, "address": address, "reason": _unplaced_reason(device)})
				continue
			if spatial["status"] == "not_applicable":
				if collection == "inputs":
					not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
				else:
					not_applicable_outputs.setdefault(spatial["reason"], []).append({"group": group, "address": address})
				continue
			placement_count += len(spatial["placements"])
			if collection == "inputs":
				located_inputs.append(address)
			else:
				located_outputs.append({"group": group, "address": address})
	placement_notes = [
		{"group": "pinmame.input.switch", "address": CLOCK_OPTO_PUBLIC.get(address, address), "reason": reason}
		for address, reason in sorted(
			{**SWITCH_PROJECTIONS, **SWITCH_2020_PLACEMENTS}.items(), key=lambda item: CLOCK_OPTO_PUBLIC.get(item[0], item[0])
		)
	] + [
		{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
		for address, reason in sorted(SOLENOID_PLACEMENT_NOTES.items())
	] + [
		{"group": "pinmame.output.gi", "address": 2, "reason": GI_CLOCK_PLACEMENT_NOTE},
	]
	# A projection places a device on another object of its own mechanism; the other notes place a device on the
	# retained table's own object for it and only explain the choice.
	projections = [entry for entry in placement_notes if entry["reason"].startswith("Projected onto")]
	direct_placements = [entry for entry in placement_notes if not entry["reason"].startswith("Projected onto")]
	unresolved_labels = ", ".join(f"{entry['group'].rsplit('.', 1)[-1]} {entry['address']}" for entry in unresolved)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
		"blockers": [
			f"{len(unresolved)} physical device carries no spatial record because no defensible coordinate exists "
			f"({unresolved_labels}); it is listed with its reason under `unresolved`.",
		],
		"notes": [
			"The complete operations manual from IPDB (machine 2684) carries the Switch Matrix (2-50), Solenoid/Flasher "
			"Table (2-52) and Lamp Matrix (2-54) wiring pages that the retained Internet Archive scan lacks. This pass "
			"uses them for the clock drives, the knocker's backbox wiring, the G.I. strings' playfield/backbox split, the "
			"flasher socket counts, the mini-playfield switch drawing and the switch matrix wiring (every used matrix "
			"switch, including column 9, the clock optos at public 121-128); the lamp matrix and the other outputs' wire "
			"colours and connector/pin assignments have not been transferred yet.",
			"Two placements are observed rather than validated: G.I. string 03's two clock sockets, projected onto "
			"the clock axis, which is not a bulb object (page 2-33 draws the sockets about an inch apart inside the "
			"clock housing). With G.I. string 02, which has no placement, they are the spatial records that are not "
			"validated.",
			"conflict.clock-motor-direction-naming was withdrawn: the manual's clock test text (page 1-18), its "
			"solenoid table (pages 2-52/2-53), the retained script's cross-reference and the ROM's own clock test agree "
			"that public 56 is Clock Reverse and 57 Clock Forward; only pinned PinMAME's tz.c #define names read the other "
			"way, while its live clock model (tz.c:601-624, mech.c:140-145) runs forward on 57.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": BOUNDS_X, "bottom": BOUNDS_Y},
			"x": f"x/{BOUNDS_X}; 0=left, 1=right",
			"y": f"y/{BOUNDS_Y}; 0=rear/backglass, 1=apron/player",
			"second_table": (
				f"Objects of the 2020 ninuzzu table are normalized by that table's own bounds ({TABLE_2020_BOUNDS}): "
				f"x/{BOUNDS_2020_X}, y/{BOUNDS_2020_Y}. 60 same-named Trigger/Kicker/Bumper/Gate/Spinner objects of the "
				"two tables agree to a median 0.004 normalized, 53 of them within 0.01."
			),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool (current PATH build)",
		},
		"extraction_2020": {
			"fail_closed": True,
			"file_count": EXTRACTION_2020_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_2020_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/twilight-zone-1993/ninuzzu-2020/extracted-vpxtool.manifest.json",
			"source_ref": VPX_2020_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_2020_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"manual_ipdb_sha256": MANUAL_IPDB_SHA256,
			"manual_amendment_sha256": MANUAL_AMENDMENT_SHA256,
			"table_sha256": TABLE_SHA256,
			"table_2020_sha256": TABLE_2020_SHA256,
			"embedded_script_2020_sha256": SCRIPT_2020_SHA256,
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
		"direct_placements": direct_placements,
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.twilight-zone.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"geometry": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
			"geometry_supplement": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-25.txt",
				"sha256": VPX_GEOMETRY_SUPPLEMENT_SHA256,
			},
			"geometry_supplement_2": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-25-round3.txt",
				"sha256": VPX_GEOMETRY_SUPPLEMENT_2_SHA256,
			},
			"geometry_supplement_3": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry-2026-09-26.txt",
				"sha256": VPX_GEOMETRY_SUPPLEMENT_3_SHA256,
			},
		},
		"excluded_object_classes": [
			"Light.l102/l105-l111 (GI/backbox helper lights parented off-table, raw x=-230.57 outside 0..1 bounds after normalization) -- render controllers for baked lightmaps, not physical GI emitters",
			"Trigger.sw81_help/sw82_help/sw83_help debug/label marker duplicates of the magnet position triggers",
			"Flipper.RampDiverter and Flipper.LRampSw (invisible animation helpers stored at y=1.000665/1.003437, outside the playfield)",
			"Primitive.KnockerPosition (invisible sound-position helper parked off the playfield at y=-0.023220)",
			"Trigger.DivTrig and Wall.DivWall (invisible ball-catch trigger and collision wall of the right ramp diverter; solenoid 5 is placed on the blade primitive BM_RDiv instead)",
			"2020 table Light.f18d/f20d/f41d (each co-located with the smaller-falloff Light f18c/f20c/f41c that is used) and 2020 Light.f18/f18a/f18b, f19, f20/f20a/f20b, f41/f41a/f41b (the sockets the 2.4.5 table already models; its Lights are used for those)",
			"2020 table Flasher objects (f18e, f18flash, f19b, f20e, f20flash, f20r, f41e, f41flash, f41r, and the GIClock glow sprites Flasher1-Flasher4) -- glow, reflection or backglass sprites, not sockets",
			"2020 table GIMinipf collection -- an author's grouping that includes Light20/Light43 on the main-playfield jet bumpers, not a socket list for G.I. string 02",
		],
		"unresolved": sorted(unresolved, key=lambda item: (item["group"], item["address"])),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Twilight Zone (Bally, 1993) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `partial` at "
		"`machines/partial/bally/twilight-zone-1993.json`; it has no conflicts, and the one physical device listed under "
		"Unresolved spatial evidence has no defensible coordinate; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Twilight Zone (Bally 1993) 2.4.5.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 `{SCRIPT_SHA256}`; that "
		f"embedded stream is the runtime and causality authority. Exact playfield bounds are `{TABLE_BOUNDS}`, wider "
		"than the standard VPW WPC table divisor used elsewhere in this repository; every canonical coordinate here "
		f"is x/{BOUNDS_X} and y/{BOUNDS_Y} rounded to at most six fractional places, except the placements taken from "
		f"the 2020 ninuzzu table (SHA-256 `{TABLE_2020_SHA256}`), which are normalized by that table's own bounds "
		f"`{TABLE_2020_BOUNDS}`. That table is the ancestor of the 2.4.5 lineage, not an independent recreation; 60 "
		"same-named Trigger/Kicker/Bumper/Gate/Spinner objects of the two tables agree to a median 0.004 normalized, so "
		"the two frames can be mixed.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime and address/causality authority; the Bally operations manual is "
		"the physical inventory, quantity, polarity, label, and playfield-versus-cabinet authority; pinned PinMAME "
		"owns controller topology and the emulator-normalization mask; the retained table supplies geometry.",
		"- Two scans of the April 1993 operations manual 16-50020-101 are cited. The Internet Archive scan "
		"(`Twilight_Zone_OPS.pdf`) carries only odd printed pages; its tables were transcribed into "
		"`external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md`, and its three location "
		"drawings (pages 2-51, 2-53, 2-55) are committed as page-scale excerpts. The complete 164-page copy from IPDB "
		f"(SHA-256 `{MANUAL_IPDB_SHA256}`) supplies the pages that scan lacks; the regions used are committed as excerpts "
		"(the whole Solenoid/Flasher Table on page 2-52, the clock test text on page 1-18, the backbox, clock and "
		"mini-playfield assembly pages, the power driver board's connector list on page 3-33, and the switch matrix, the "
		"switch list items F1-F8 and 11-33 and the mini-playfield switch drawing on page 2-50). Manual Amendment "
		"16-50020-AMD-1 renumbers the clock assembly to A-16124-1, which changes no socket item, and changes switch "
		"61's part to 5647-12693-57, which the definition records.",
		"- Switches 45 and 46 each have two contacts (page 2-51 \"(2)\"). They are placed on the 2020 table's own switch "
		"walls (sw45/sw45a, sw46/sw46a); the page 2-50 drawing, a perspective detail with remote callout balloons, "
		"corroborates the count, the side and the order.",
		"- Flasher circuits 18, 19, 20 and public 55 (item 41) each have two sockets. The first socket keeps the 2.4.5 "
		"table's Light; the second is the 2020 table's Light for the socket the 2.4.5 table dropped (the smaller-falloff "
		"Light of each co-located pair). Each new socket was compared with its callout on the page 2-53 drawings through "
		"least-squares affine fits on validated placements (`vpx-geometry-2026-09-26.txt`). A placement passes at an offset no "
		"larger than the fit's largest leave-one-out error and under 0.07; outlying controls (callout 18 at 0.067 on the "
		"overlay fit, balloon 53 at 0.112 on the 2-50 fit) inflate the first bound, so the 0.07 cap decides (flasher "
		"19's upper socket at 0.040, switch 46's upper contact at 0.047). The drawings corroborate the "
		"count and where each socket sits, and the coordinates come from the table.",
		"- The knocker is backbox hardware: page 2-52 prints its connections under the Backbox columns and page 2-4 lists "
		"the B-10686-1 Knocker & Bracket Assy. in the backbox assembly.",
		"- G.I. string 03 (\"Clock & Insert\", public G.I. 2) is placed as the clock assembly's two sockets (A-16124 item "
		"25), projected co-located onto the clock axis although page 2-33 draws them side by side on bracket 24 about an "
		"inch apart inside the clock housing's footprint, so both placements are observed, not validated; its "
		"insert-board bulbs are backbox hardware. G.I. string 04 "
		"(\"Insert Main\", public G.I. 3) is wired to the backbox only.",
		"- A `not_applicable` spatial record is used only for a device that genuinely has no playfield position: "
		"coin-door, cabinet-button, and backbox devices the manual places off the playfield, unused addresses, "
		"PinMAME-internal state channels, DIP switches, the clock strobe control line, and the four flipper "
		"end-of-stroke contacts, which follow the repository-wide convention of an internal_nonvisual record paired "
		"with an internal.* role because they sit inside the flipper assembly whose position the flipper coils "
		"already carry. A physical playfield "
		"device without a defensible coordinate carries no spatial key at all and is listed under Unresolved "
		"spatial evidence.",
		"- Lamps 11-18 and 21-28 carry the printed suffix \"(Door)\". That names the playfield's central door-panel "
		"insert group, not the cabinet coin door: the Lamp Locations drawing prints those callouts on the door "
		"panel in the middle of the playfield, and the retained script maps Light objects l11-l28 to them through "
		"vpmMapLights. An earlier revision treated them as coin-door lamps.",
		"- Switches 31-33 are labelled Left/Right/Lower from the Main Playfield Switch Locations drawing and the "
		"script's Bumper1/Bumper2/Bumper3 binding, which agree; the earlier Lower/Left/Right labels had no source.",
		"- Several earlier placements were wrong and are corrected here: switch 47 carried switch 52's trigger "
		"coordinate, switch 74 carried the gumball popper lane hole instead of the popper kicker, solenoid 15 "
		"carried lamp 86's coordinate instead of the lock kicker, solenoid 24 carried the gumball diverter blade, "
		"solenoids 45 and 48 were placed on the opposite flipper, and solenoids 56-58 carried the lock kicker and "
		"lamp 86 coordinates.",
		"- The flasher Light objects (f17, f17b, f18, f19, f20, f28, f37-f41) are the lights the retained script's "
		"FlashPWM/UpdateF17 callbacks drive; each coincides with a callout circle on the manual's Solenoid/Flasher "
		"Locations drawing.",
		"- Solenoids 37-44 do not carry the WPC-95 LPDC duplication: this is a WPC-Fliptronic (pre-95, pre-integrated "
		"board) generation, and pinned PinMAME's core_getSol only serves that address range for WPC-95/S11 "
		"generations; Twilight Zone's own driver hook does not claim it either, so 37-44 are simply unused here.",
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
		"## Direct placements with a recorded reason",
		"",
		"These devices sit on a retained table's own object for them; the note records why that object was chosen.",
		"",
	]
	for entry in report["direct_placements"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Unresolved spatial evidence",
		"",
	]
	for entry in report["unresolved"]:
		lines.append(f"- {entry['group']} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Physical devices without a spatial record: {len(report['unresolved'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Identity, controller platform, address enumeration, semantic naming, mechanism inventory/behavior, variant "
		"coverage, and recreation knowledge are complete and validated, and the definition carries no conflicts. "
		"Promotion to `author_ready` is refused because G.I. string 02 (\"Mini-playfield & Insert\", public G.I. 1) "
		"has no defensible playfield placement: no page enumerates its bulbs, the mini-playfield assembly shows a #555 "
		"socket in the Street Light and a second socket in its back view without a quantity, and the recreations' "
		"groupings are authors' choices. `coverage.missing` is therefore `[\"spatial_placement\"]`. Resolving it needs a "
		"continuity or bulb survey of G.I. string 02 on a physical machine. G.I. string 03's two clock sockets are "
		"placed but only observed (projected onto the clock axis); measuring the page 2-33 bracket offset, or a "
		"survey of the clock housing, would validate them.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- 2020 table extraction manifest `{report['extraction_2020']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_2020_MANIFEST_SHA256}`, {EXTRACTION_2020_FILE_COUNT} files, {EXTRACTION_2020_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- Raw retained-table object geometry, SHA-256 `{VPX_GEOMETRY_SHA256}`, and its two 2026-09-25 supplements, "
		f"SHA-256 `{VPX_GEOMETRY_SUPPLEMENT_SHA256}` and `{VPX_GEOMETRY_SUPPLEMENT_2_SHA256}` (the second also records "
		"the callout-05 measurement on the page 2-53 drawing).",
		f"- The 2026-09-26 supplement `vpx-geometry-2026-09-26.txt`, SHA-256 `{VPX_GEOMETRY_SUPPLEMENT_3_SHA256}`: the "
		"2020 table's objects, the frame comparison, and the page 2-53 and 2-50 drawing fits with every measured callout "
		"pixel, residual, leave-one-out error and offset.",
		f"- The ROM clock-test runs summarized in `{RUNTIME_CLOCK_PATH}` (clock model off) and "
		f"`{RUNTIME_CLOCK_MECH_PATH}` (clock model on).",
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
		raise RuntimeError(f"Stale Twilight Zone author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Twilight Zone definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Twilight Zone seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Twilight Zone definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Twilight Zone seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Twilight Zone spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Twilight Zone spatial review drifted from its deterministic curator: {markdown_path}")
	print("Twilight Zone definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Twilight Zone extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		verify_2020_extraction_manifest(source_root)
		print("Twilight Zone retained extractions (2.4.5 and the 2020 table) match their pinned manifest identities.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
