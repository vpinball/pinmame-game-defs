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

TABLE_SHA256 = "4fcca01a076591384caec5b06d4f58547299cbeae9fac2a67faa29cc5af0d814"
SCRIPT_SHA256 = "122ef6811ff2e6912593a28a75078a467e6d58dd208c98e313c82712aee2bc4e"
MANUAL_SHA256 = "a1df4b4aac2c14ced066adde3d743d06f1a95220b32747fcae6754a6834ebba5"
MANUAL_TRANSCRIPTION_SHA256 = "022e91ceaedb44fdaf410cca90bfa534aa11c89fcd832dd2a0f94166c24de39a"
VPX_GEOMETRY_SHA256 = "dc8a49f6b1d1568ba9027af7453157039da05a08d6ffd2ac0a60c54940cb2f3a"

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
# confirms labels for 34-98; the manual's first Switch Locations page, 2-50, covering
# items 1-33, is absent from this retained scan -- see manual-transcription.md).
SWITCH_LABELS = {
	11: "Right Inlane", 12: "Right Outlane", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Right Trough", 16: "Center Trough", 17: "Left Trough", 18: "Outhole",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In Button",
	25: "Far Left Trough", 26: "Trough Proximity (Powerball Detect)", 27: "Shooter Lane", 28: "Rocket Kicker",
	31: "Lower Jet Bumper", 32: "Left Jet Bumper", 33: "Right Jet Bumper",
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
# uses. 24 has no #define anywhere in tz.c's switch list (column 2 jumps 23 -> 25) and
# is treated the same way for lack of any contrary evidence.
UNUSED_MATRIX_ADDRESSES = {24, 71, 82, 86}
UNUSED_MATRIX_LABELS = {71: "Big Kick", 82: "Upper Right Magnet", 86: "Clock Lane"}
# Manual page 2-51: printed "A-14231 (LED) / A-14232 (Trans)" opto-pair construction.
OPTO_SWITCHES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87, 91, 92, 93, 94, 95, 96, 97, 98}
# tzGameData's inverted-switch mask, verbatim: {Coin=0,c1..c6=0,c7=0x3f,c8=0x7f,c9=0,c10=0,Cab=0,Cust=0xff}.
# Column 7 (71-78) bits 0-5 => 71-76 inverted; column 8 (81-88) bits 0-6 => 81-87
# inverted; the custom column (91-98) is fully inverted. Columns 1-6 (11-68) are 0x00,
# so none of those addresses are emulator-normalized regardless of manual confirmation.
PINMAME_NORMALIZED_OPTO_SWITCHES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87, 91, 92, 93, 94, 95, 96, 97, 98}
PULSED_SWITCHES = {11, 12, 25, 27, 31, 32, 33, 36, 37, 38, 42, 43, 44, 45, 46, 51, 52, 53, 54, 56, 61, 62, 63, 73, 75, 76, 117}

# Manual page 2-51 part numbers, address -> (assembly_or_switch_part, note)
SWITCH_PARTS = {
	34: "SW-1A-114 (kicker) / SW-1A-120 (score)", 35: "SW-1A-114 (kicker) / SW-1A-120 (score)",
	36: "5647-12693-19", 37: "5647-12693-19", 38: "5647-12693-19",
	41: "5647-12693-13", 42: "5647-12693-13", 43: "5647-12693-13", 44: "5647-12693-19",
	45: "5647-12693-11", 46: "5647-12693-11", 47: "A-15658-2", 48: "A-14691-6",
	51: "5647-12693-13", 52: "5647-12693-19", 53: "5647-12693-11", 54: "5647-12693-21",
	55: "5647-12393-08", 56: "5647-12693-19", 57: "A-16535", 58: "5647-12693-25",
	61: "5647-12693-32", 62: "5647-12693-53", 63: "5647-12693-54",
	64: "A-14691-6", 65: "A-14691-4", 66: "A-14691-6", 67: "A-14691-6", 68: "A-15658-6",
	72: "A-14231 (LED) / A-14232 (Trans)", 73: "A-14231 (LED) / A-14232 (Trans)",
	74: "A-14231 (LED) / A-14232 (Trans)", 75: "A-14231 (LED) / A-14232 (Trans)",
	76: "A-14231 (LED) / A-14232 (Trans)", 77: "A-14691-6", 78: "A-14691-6",
	81: "A-14231 (LED) / A-14232 (Trans)", 83: "A-14231 (LED) / A-14232 (Trans)",
	84: "A-14231 (LED) / A-14232 (Trans)", 85: "A-14231 (LED) / A-14232 (Trans)",
	87: "A-14231 (LED) / A-14232 (Trans)", 88: "5647-12133-11",
	91: "A-16220", 92: "A-16220", 93: "A-16220", 94: "A-16220",
	95: "A-16219", 96: "A-16219", 97: "A-16219", 98: "A-16219",
}
UNDERSIDE_SWITCHES = {55, 57, 58}
NOT_SHOWN_SWITCHES = {91, 92, 93, 94, 95, 96, 97, 98}

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

# --- Normalized playfield coordinates (x/1082.353, y/2164.706) from the retained
# extraction; see review-artifacts/twilight-zone-1993/vpx-geometry.txt.
SWITCH_POSITIONS = {
	11: [(0.75733, 0.733553)], 12: [(0.816857, 0.749645)],
	15: [(0.786065, 0.876327)], 16: [(0.717238, 0.897158)], 17: [(0.649107, 0.918002)], 18: [(0.466847, 0.974273)],
	25: [(0.586598, 0.938043)], 27: [(0.953552, 0.885472)], 28: [(0.816222, 0.633787)],
	34: [(0.296464, 0.727956)], 35: [(0.676268, 0.727484)],
	36: [(0.049304, 0.746239)], 37: [(0.126765, 0.714541)], 38: [(0.212212, 0.713967)],
	41: [(0.085949, 0.216834)], 42: [(0.201272, 0.381543)], 43: [(0.663093, 0.297159)], 44: [(0.033737, 0.300647)],
	47: [(0.143608, 0.216659)],
	51: [(0.60814, 0.116087)], 52: [(0.143608, 0.216659)], 53: [(0.423152, 0.15106)], 54: [(0.871712, 0.078071)],
	56: [(0.218257, 0.190395)], 57: [(0.528667, 0.472186)], 58: [(0.651165, 0.519193)],
	61: [(0.950867, 0.529593)], 62: [(0.950867, 0.491633)], 63: [(0.950797, 0.45433)],
	48: [(0.206766, 0.619195)],
	64: [(0.721088, 0.222436)], 65: [(0.759336, 0.32671), (0.759105, 0.30282)],
	66: [(0.646481, 0.383017)], 67: [(0.635675, 0.407582)], 68: [(0.628201, 0.432651)],
	72: [(0.875735, 0.976383)], 73: [(0.752093, 0.135059)], 74: [(0.60814, 0.116087)],
	75: [(0.184321, 0.296114)], 76: [(0.167764, 0.468382)], 77: [(0.298735, 0.531676)], 78: [(0.334772, 0.505688)],
	81: [(0.881833, 0.219272)], 83: [(0.313118, 0.156291)], 84: [(0.765208, 0.141901)],
	85: [(0.775234, 0.11319)], 87: [(0.174341, 0.060475)], 88: [(0.755565, 0.171456)],
}
# Position 65 has two HitTarget objects (sw65, sw65a); Power Payoff is a two-target
# bank sharing one public switch, matching the manual's "(2)" quantity annotation.
SWITCH_PROJECTIONS = {
	52: "Projected onto the Trigger.sw52 object, the only VPX trigger the retained script binds to switch 52; the geometry file lists it under the Hitchhiker figure's lane.",
}
UNRESOLVED_SWITCH_SPATIAL = {
	26: "No VPX object binds switch 26 (Trough Proximity / powerball detect); the retained script sets it from tz_handleBallState's ball-type detection rather than a Hit event.",
	31: "Bumper1/Bumper2/Bumper3 are three generically-named VPX Bumper objects with no per-object binding to a specific public switch address in the retained script or extraction; a left/right/lower assignment could only be guessed from relative position, so no placement is asserted.",
	32: "See switch 31: no explicit per-object address binding exists for the three generic Bumper objects.",
	33: "See switch 31: no explicit per-object address binding exists for the three generic Bumper objects.",
	45: "No gameitem, collection, or object event binding named sw45/sw45a was found anywhere in the retained extraction, despite the retained script defining Sub sw45_Hit and Sub sw45a_Hit.",
	46: "No gameitem, collection, or object event binding named sw46/sw46a was found anywhere in the retained extraction, despite the retained script defining Sub sw46_Hit and Sub sw46a_Hit.",
	55: "No VPX object binds switch 55 (Gumball Geneva); pinned PinMAME's tz_handleMech sets it synthetically from the internal gumball-motor position counter rather than from a table Hit event, and the manual documents it only as \"located on the underside of the playfield\".",
}

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
	56: "Clock Motor Drive A", 57: "Clock Motor Drive B",
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
# true public PinMAME address; see conflict.clock-motor-direction-naming for 56/57.
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
	45: "SolLFlipper (lower left)", 46: "SolRFlipper (lower right)",
	47: "SolULFlipper (upper left)", 48: "SolURFlipper (upper right)",
	51: "SolModCallback FlashPWM 37", 52: "SolModCallback FlashPWM 38", 53: "SolModCallback FlashPWM 39",
	54: "SolModCallback FlashPWM 40", 55: "SolModCallback FlashPWM 41",
	59: "SolGumRelease (commented out; PinMAME hack, unreliable with SolModCallbacks)",
}
FLASHER_ADDRESSES = {17, 18, 19, 20, 28, 51, 52, 53, 54, 55}

SOLENOID_POSITIONS = {
	2: [(0.816222, 0.633787)], 4: [(0.307772, 0.039463)], 9: [(0.786065, 0.876327)],
	15: [(0.815733, 0.481498)], 16: [(0.907357, 0.888818)], 21: [(0.313118, 0.156291)],
	23: [(0.881833, 0.219272)], 24: [(0.583327, 0.054196)], 25: [(0.100956, 0.42269)],
	26: [(0.237953, 0.42269)],
	45: [(0.33539, 0.836095)], 46: [(0.635515, 0.836095)], 47: [(0.33539, 0.836095)], 48: [(0.635515, 0.836095)],
	56: [(0.765208, 0.141901)], 57: [(0.765208, 0.141901)], 58: [(0.815733, 0.481498)],
}
# Flasher bulbs are diffuse fixtures without their own single named playfield trigger
# object in this retained extraction; their approximate location is documented in
# physical.notes from the manual's "Where Used" text instead of a coordinate.
UNRESOLVED_SOLENOID_SPATIAL = {
	27: "The only candidate VPX object (Flipper.RampDiverter) sits at normalized y=1.000665, just outside the 0..1 playfield bounds -- a table-modeling anomaly (the diverter blade pivots below the visible apron edge) -- so no coordinate is asserted.",
	1: "Slot Kickout coil location coincides with the slot machine assembly (Trigger.slotMachine, Kicker.SlotKickerOverflow); no single coil-body object is separately named in the retained extraction.",
	3: "Auto-Fire Kicker coil is inside the Kicker.AutoPlungerKicker assembly; the shooter-lane kicker object itself is used for switch 72's placement instead of a duplicate coil coordinate.",
	5: "Right Ramp Diverter coil has no separately named coil-body object; Flipper.RampDiverter documents the diverter blade only.",
	6: "Gumball Diverter coil has no separately named coil-body object; Flipper.GumballDiverter documents the diverter blade only.",
	10: "Right Slingshot coil is native VPX slingshot physics (Wall.RightSlingShot); no scripted coil object exists.",
	11: "Left Slingshot coil is native VPX slingshot physics (Wall.LeftSlingShot); no scripted coil object exists.",
	12: "Lower Jet Bumper coil has no separately named coil-body object distinct from Bumper.Bumper3.",
	13: "Left Jet Bumper coil has no separately named coil-body object distinct from Bumper.Bumper1.",
	14: "Right Jet Bumper coil has no separately named coil-body object distinct from Bumper.Bumper2.",
}


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
	1: [(0.118778, 0.301331)],
	4: [
		(0.725698, 0.392912), (0.926481, 0.360232), (0.806104, 0.307407), (0.939409, 0.189479),
		(0.940655, 0.168729), (0.930424, 0.0966), (0.930776, 0.079079), (0.861673, 0.024368),
		(0.822776, 0.024412), (0.683537, 0.759072), (0.746216, 0.409721), (0.695766, 0.814269),
		(0.74457, 0.796746),
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


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": round(x, 6),
				"y": round(y, 6),
				"provenance": provenance(*source_refs),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


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
				"CORE_CUSTSOLNO(9) fake gumball-release state, tz_handleMech's synthetic swGeneva/clock-opto derivation, "
				"and mechClock's MECH_TWODIRSOL clock mechanism table; src/wpc/core.h CORE_FIRSTUFLIPSOL=33/"
				"CORE_FIRSTLFLIPSOL=45/CORE_FIRSTCUSTSOL=51/CORE_CUSTSWCOL/CORE_CUSTSWNO/CORE_CUSTSOLNO; src/wpc/core.c "
				"core_getSol's 37-44 branch gated on GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11 only; src/wpc/wpc.c WPC_FLIPPERS "
				"register read (unconditional swMatrix complement for non-WPC95 generations); "
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
				"page 2-55 (\"Lamp Locations\") carries the full 64-position lamp matrix. This retained scan is missing "
				"every even printed page from 2-48 through 2-54 inclusive, so the Switch Matrix wiring page (2-50, "
				"which also carries switch items 1-33), the Solenoid/Flasher Table wiring page (2-52), and the Lamp "
				"Matrix wiring page (2-54) are unavailable; see manual-transcription.md."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
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
				f"SHA-256 {VPX_GEOMETRY_SHA256}."
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
			label = SWITCH_LABELS.get(address) or UNUSED_MATRIX_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES or label is None
			identifier = f"switch.matrix-{address}"
			part = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part:
				if "(" in part and "/" in part:
					physical["assembly_part_number"] = part
				else:
					physical["part_number"] = part
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
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
					" Printed with LED/phototransistor opto construction (A-14231/A-14232); pinned PinMAME's tzGameData "
					"inverted-switch mask covers this address, so the public switch state is already normalized and "
					"must not be inverted again."
				)
			elif address in OPTO_SWITCHES:
				notes += " Printed with LED/phototransistor opto construction (A-14231/A-14232)."
			elif address in SWITCH_PARTS:
				notes += " Printed as a plain mechanical switch/target part; PinMAME's inverted-switch mask leaves this column at 0x00 (not normalized)."
			else:
				notes += (
					" This address is below the range covered by the retained switch-locations page (2-51); the "
					"manual's first Switch Locations page (2-50, covering items 1-33) is missing from this scan (see "
					"manual-transcription.md), so label and polarity here are sourced from tz.c's #define and its "
					"inverted-switch mask alone, not cross-checked against a printed part number."
				)
			if address in UNDERSIDE_SWITCHES:
				notes += " Located on the underside of the playfield (manual dagger footnote)."
			if address in NOT_SHOWN_SWITCHES:
				notes += " Not shown on the printed switch-locations diagram (manual asterisk footnote)."
			if address == 65:
				notes += " Power Payoff is a two-target bank sharing one public switch (manual \"(2)\")."
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
			}
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
				elif address in UNRESOLVED_SWITCH_SPATIAL:
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE)
					physical["notes"] += " " + UNRESOLVED_SWITCH_SPATIAL[address]
				elif address in SWITCH_POSITIONS:
					coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
					if address in SWITCH_PROJECTIONS:
						physical["notes"] += " " + SWITCH_PROJECTIONS[address]
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
				else:
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE)
					physical["notes"] += " No VPX geometry evidence located for this address."
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	# Custom switch column (CORE_CUSTSWCOL), public addresses 91-98: the eight clock-
	# position optos on the Minute (91-94) and Hour (95-98) opto PC boards.
	for address in range(91, 99):
		label = SWITCH_LABELS[address]
		identifier = f"switch.matrix-{address}"
		part = SWITCH_PARTS[address]
		physical = {
			"switch_type": "opto",
			"part_number": part,
			"notes": (
				f"Printed custom switch column position {address}. Printed with opto-board construction ({part}, "
				"Minute Opto P.C.B. for 91-94 or Hour Opto P.C.B. for 95-98). Not shown on the printed "
				"switch-locations diagram (manual asterisk footnote). Pinned PinMAME's inverted-switch mask marks the "
				"entire custom column 0xff, so the public switch state is already normalized and must not be "
				"inverted again."
			),
		}
		items.append(
			_device(
				identifier,
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				normally_closed=True,
				physical=physical,
				spatial=not_applicable("internal_nonvisual", CORE_SOURCE),
			)
		)

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
				spatial=not_applicable("cabinet_or_service" if is_button else "internal_nonvisual", MANUAL_SOURCE),
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
			kind = "flasher" if address in FLASHER_ADDRESSES else "motor" if address in {56, 57, 58, 24} else "coil"
			if address in {33, 34, 35, 36, 45, 46, 47, 48}:
				kind = "coil"
			physical: dict[str, Any] = {}
			coil_part = SOLENOID_COIL_PART.get(address)
			if coil_part and kind != "flasher":
				physical["part_number"] = coil_part
			assembly = SOLENOID_ASSEMBLIES.get(address)
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed solenoid/flasher-locations item {address}."
			if address in MANUAL_SOLENOID_ALIASES:
				notes += f" Printed auxiliary-board callout number {MANUAL_SOLENOID_ALIASES[address]}."
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
			if address in {56, 57}:
				notes += (
					" Drives the analog clock hand through the A-16120 D.C. Motor Control Assembly as one of a "
					"forward/reverse drive pair; see conflict.clock-motor-direction-naming for the Forward/Reverse "
					"label disagreement between tz.c's #define names and the manual/script cross-reference."
				)
			if address == 58:
				notes += " Strobes the eight custom clock-position optos (91-98); not driven by the retained VPX script (handled entirely by PinMAME's own mechClock simulation)."
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
				if address in SOLENOID_POSITIONS:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
				elif address in UNRESOLVED_SOLENOID_SPATIAL:
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE)
					physical["notes"] += " " + UNRESOLVED_SOLENOID_SPATIAL[address]
				elif kind == "flasher":
					extra["roles"] = ["cabinet.insert-panel"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["notes"] += " Flasher bulb location is not separately named in the retained extraction; treated as a controlled backbox/insert circuit rather than an invented playfield coordinate."
				else:
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE)
					physical["notes"] += " No VPX geometry evidence located for this address."
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 32} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a Twilight Zone playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Twilight Zone playfield device.",
			31: "PinMAME's synthetic game-on state, reflecting the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME reports this WPC state channel as always zero.",
			49: "PinMAME's simulator-only ball-shooter channel; no WPC-Fliptronic hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary (CORE_FIRSTCUSTSOL=51).",
			59: "PinMAME's fake gumball-release solenoid, driven from software state rather than a real coil; the retained script comments it out as \"unreliable with SolModCallbacks\".",
		}.get(address, (
			"Unlike WPC-95, this WPC-Fliptronic generation has no integrated LPDC board: pinned PinMAME's core_getSol "
			"dispatch only serves 37-44 for GEN_WPC95/GEN_WPC95DCS/GEN_ALLS11, and Twilight Zone's own tz_getSol hook "
			"does not claim this address either, so it is simply unused address space on this machine."
		))
		roles = ["internal.wpc-state"] if address in {29, 30, 31, 32} else ["internal.unused.wpc-output"]
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
				notes += ' Printed suffix "(Door)": mounted on the cabinet coin door insert panel rather than the playfield.'
			if address in LAMP_NOT_SHOWN:
				notes += " Not shown on the printed lamp-locations diagram (manual asterisk footnote)."
			if address in {87, 88}:
				notes += " Cabinet button lamp inside the illuminated buy-in/credit button assembly."
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
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				if address in LAMP_POSITIONS:
					extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
				else:
					extra["spatial"] = not_applicable("internal_nonvisual", CORE_SOURCE)
					physical["notes"] += " No VPX geometry evidence located for this address."
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
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's GI emitter collection for this string (UpdateGI in the retained "
				"script)."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 2:
			notes += (
				" The retained script's UpdateGI binds this string to a single light object (l102), but that object's "
				"raw table coordinate (x=-230.57, before normalization) falls outside the 0..1 playfield bounds -- a "
				"table-modeling anomaly, the same class of issue documented for Monster Bash's GIbot light11. No "
				"validated playfield placement is asserted for this address; see reports/spatial/bally/"
				"twilight-zone-1993.json unresolved list."
			)
			extra["spatial"] = not_applicable("internal_nonvisual", VPX_SCRIPT_SOURCE)
		else:
			notes += (
				" The retained script's UpdateGI case for this address binds no light collection at all (case 3 has "
				"an empty body), so this string has no playfield-visible emitter evidence from the retained table."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", VPX_SCRIPT_SOURCE)
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
			"Geneva) senses the motor's geneva-gear position but is driven synthetically by pinned PinMAME's "
			"tz_handleMech from an internal position counter rather than a table Hit event, and has no bound VPX "
			"trigger object in the retained extraction. PinMAME's tz_getSol also exposes a fake CORE_CUSTSOLNO(9) "
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
			[output_id("Clock Motor Drive A"), output_id("Clock Motor Drive B")],
			[
				"switch.matrix-91", "switch.matrix-92", "switch.matrix-93", "switch.matrix-94",
				"switch.matrix-95", "switch.matrix-96", "switch.matrix-97", "switch.matrix-98",
			],
			"A bidirectional DC gearmotor (A-16120 D.C. Motor Control Assembly) drives a physical analog clock hand "
			"through solenoids 56/57 as a forward/reverse pair, strobed by solenoid 58 (Clock Switch Strobe, A-16100). "
			"Eight opto sensors on Minute (A-16220, addresses 91-94) and Hour (A-16219, addresses 95-98) opto PC "
			"boards report clock-hand position; all eight are in PinMAME's fully-inverted custom switch column. "
			"Pinned PinMAME does not expose this to the table script at all: init_tz's mech_add(0, &mechClock) drives "
			"an internal MECH_TWODIRSOL simulation (mechClock's own switch/step-range table, disabled by an #if 0 "
			"block in tz_handleMech in this pinned revision) and Controller.GetMech(0) reports the resulting position "
			"directly; the retained script reads that mechanism position rather than driving the clock switches "
			"itself. Twilight Zone's own tz.c #define names solenoid 56 \"sClockFwd\" (Forward) and 57 \"sClockRev\" "
			"(Reverse); the printed manual and the retained script's own cross-reference comments read the opposite "
			"way -- see conflict.clock-motor-direction-naming, unresolved.",
			[
				("minute-15", "Clock 15 minutes", ["switch.matrix-91"], "Minute-hand opto."),
				("minute-0", "Clock 0 minutes", ["switch.matrix-92"], "Minute-hand opto."),
				("minute-45", "Clock 45 minutes", ["switch.matrix-93"], "Minute-hand opto."),
				("minute-30", "Clock 30 minutes", ["switch.matrix-94"], "Minute-hand opto."),
				("hour-1", "Clock hour 1", ["switch.matrix-95"], "Hour-hand opto bit 1."),
				("hour-2", "Clock hour 2", ["switch.matrix-96"], "Hour-hand opto bit 2."),
				("hour-3", "Clock hour 3", ["switch.matrix-97"], "Hour-hand opto bit 3."),
				("hour-4", "Clock hour 4", ["switch.matrix-98"], "Hour-hand opto bit 4."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
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
			"Left/Right) have named _Hit subs in the retained script (sw45_Hit/sw45a_Hit/sw46_Hit/sw46a_Hit) but no "
			"gameitem, collection, or object binding for those names exists anywhere in the retained extraction, so "
			"their causal role beyond the manual's plain \"Mini-Playfield Left/Right\" label is unconfirmed.",
			[
				("enter", "Mini-playfield enter", ["switch.matrix-44"], "Ball leaves the main playfield for the mini-playfield."),
				("camera", "Camera / mini-playfield top hole", ["switch.matrix-42"], "Also called the Camera switch in the retained script's own comment."),
				("piano", "Player piano", ["switch.matrix-43"], "Piano keys standup target."),
				("top", "Mini-playfield top", ["switch.matrix-75"], "Upper mini-playfield opto."),
				("exit", "Mini-playfield exit", ["switch.matrix-76"], "Ball returns to the main playfield."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
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
			"Three A-9415-2 jet bumpers. Solenoid 12 fires the Lower Jet Bumper (switch 31), solenoid 13 the Left "
			"Jet Bumper (switch 32), and solenoid 14 the Right Jet Bumper (switch 33); the retained script leaves "
			"these three SolCallback entries commented out because the table's native VPX bumper physics handles "
			"them directly.",
			[
				("lower", "Lower jet bumper", ["switch.matrix-31"], "Closest to the player."),
				("left", "Left jet bumper", ["switch.matrix-32"], "Left of the nest."),
				("right", "Right jet bumper", ["switch.matrix-33"], "Right of the nest."),
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
	return [
		{
			"id": "conflict.clock-motor-direction-naming",
			"path": "binding:pinmame.output.solenoid/56,57/None",
			"description": (
				"Pinned PinMAME's src/wpc/sims/wpc/full/tz.c names public solenoid 56 \"sClockFwd\" "
				"(#define sClockFwd CORE_CUSTSOLNO(6)) and public solenoid 57 \"sClockRev\" "
				"(#define sClockRev CORE_CUSTSOLNO(7)) -- i.e. 56 = Forward, 57 = Reverse. The printed manual's "
				'Solenoid/Flasher Locations page (2-53) prints the opposite direction for the equivalent auxiliary-'
				'board callout numbers: item 42 = "Clock Reverse" and item 43 = "Clock Forward". The retained '
				"known-working VPX script's own commented-out SolCallback lines bridge the two numbering schemes "
				"directly and independently corroborate the manual: `'SolCallback(56) = \"\"  '(42) Clock Reverse "
				"(***)` and `'SolCallback(57) = \"\"  '(43) Clock Forward (***)`. Two independent sources (the "
				"printed manual and the retained script author's own cross-reference comment) agree with each other "
				"and disagree with pinned PinMAME's internal #define name for which physical drive line is Forward "
				"versus Reverse. Neither solenoid is exercised at runtime by the retained script (the clock motor is "
				"driven entirely by PinMAME's own mechClock simulation, disabled by an #if 0 block in this pinned "
				"revision's tz_handleMech), so there is no runtime observation available to break the tie. "
				"Resolution path: a LibPinMAME gameplay-harness trace driving solenoids 56/57 individually against a "
				"legal tz_92 or later ROM while observing which direction the physical/simulated clock hand moves, "
				"or inspection of the A-16120 D.C. Motor Control Assembly schematic on a missing manual page. "
				"Unresolved."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "bally.twilight-zone.1993",
			"name": "Twilight Zone",
			"manufacturer": "Bally",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 2358,
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "conflicted",
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


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
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
		"status": "partial",
		"blockers": [
			"conflict.clock-motor-direction-naming is unresolved: pinned PinMAME's tz.c #define names contradict "
			"both the printed manual and the retained script's own cross-reference comment for which of solenoids "
			"56/57 is the clock's forward drive line.",
			"Switches 26 (Trough Proximity), 45/46 (Mini-Playfield Left/Right), and 55 (Gumball Geneva) have no "
			"bound VPX playfield object in the retained extraction, so they carry no validated spatial placement.",
			"GI address 2 (Clock & Insert) is bound in the retained script to a single light object whose raw "
			"coordinate falls outside the 0..1 playfield bounds; excluded as a table-modeling anomaly rather than "
			"promoted to a placement.",
			"The manual's Switch Matrix (2-50), Solenoid/Flasher Table (2-52), and Lamp Matrix (2-54) wiring pages "
			"are absent from this retained scan, so exact wire colors and connector/pin assignments are not "
			"asserted for any device.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": BOUNDS_X, "bottom": BOUNDS_Y},
			"x": f"x/{BOUNDS_X}; 0=left, 1=right",
			"y": f"y/{BOUNDS_Y}; 0=rear/backglass, 1=apron/player",
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
			"root": "external:pinmame-manuals/rendered/bally.twilight-zone.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"geometry": {
				"path": "external:pinmame-review-artifacts/twilight-zone-1993/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"Light.l102/l105-l111 (GI/backbox helper lights parented off-table, raw x=-230.57 outside 0..1 bounds after normalization) -- table modeling anomaly, not a distinct physical GI emitter",
			"Trigger.sw81_help/sw82_help/sw83_help debug/label marker duplicates of the magnet position triggers",
		],
		"unresolved": [
			{"group": "pinmame.input.switch", "address": 26, "reason": UNRESOLVED_SWITCH_SPATIAL[26]},
			{"group": "pinmame.input.switch", "address": 45, "reason": UNRESOLVED_SWITCH_SPATIAL[45]},
			{"group": "pinmame.input.switch", "address": 46, "reason": UNRESOLVED_SWITCH_SPATIAL[46]},
			{"group": "pinmame.input.switch", "address": 55, "reason": UNRESOLVED_SWITCH_SPATIAL[55]},
			{"group": "pinmame.output.gi", "address": 2, "reason": "Bound light object l102 sits outside the playfield bounds; excluded as an anomaly rather than promoted."},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Twilight Zone (Bally, 1993) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `partial` at "
		"`machines/partial/bally/twilight-zone-1993.json`, driven by one unresolved semantic conflict "
		"(`conflict.clock-motor-direction-naming`) and a small number of switches/one GI string with no validated "
		"playfield placement; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Twilight Zone (Bally 1993) 2.4.5.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 `{SCRIPT_SHA256}`; that "
		f"embedded stream is the runtime and causality authority. Exact playfield bounds are `{TABLE_BOUNDS}`, wider "
		"than the standard VPW WPC table divisor used elsewhere in this repository; every canonical coordinate here "
		f"is x/{BOUNDS_X} and y/{BOUNDS_Y} rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime and address/causality authority; the Bally operations manual is "
		"the physical inventory, quantity, polarity, and label authority; pinned PinMAME owns controller topology "
		"and the emulator-normalization mask; the retained table supplies geometry.",
		"- The retained manual PDF is an image-only scan. Every printed table used here was read from rendered pages "
		"and transcribed into `external:pinmame-review-artifacts/twilight-zone-1993/manual-transcription.md`.",
		"- This retained scan is missing every even printed page from 2-48 through 2-54 inclusive, removing the "
		"Switch Matrix (2-50, which also carries the first Switch Locations table for items 1-33), Solenoid/Flasher "
		"Table (2-52), and Lamp Matrix (2-54) wiring pages. Wire colors and connector/pin assignments are therefore "
		"not asserted for any device in this definition, and switches below address 34 rely on pinned PinMAME's own "
		"#defines and inverted-switch mask rather than a printed part-number cross-check.",
		"- The manual's printed auxiliary-board item numbers 37-44 for the custom solenoid board are not the same "
		"as PinMAME's public solenoid addresses for the same physical outputs; the retained script's own comments "
		"bridge the two numbering schemes explicitly (see manual-transcription.md), resolving what would otherwise "
		"look like a large unexplained address gap.",
		"- Switches 71 (Big Kick), 82 (Upper Right Magnet), and 86 (Clock Lane), and solenoid 22 (Upper Right "
		"Magnet), are printed \"Not Used\" with no part number at all. PinMAME's own simulator-only input-port "
		"toggles of the same names belong to its internal text-mode ball tracker (sim.c), not a documented physical "
		"factory option, so no fitted variant is claimed.",
		"- GI address 2 (Clock & Insert) is bound in the retained script to a single light object (l102) whose raw "
		"coordinate sits outside the playfield bounds; excluded as a table-modeling anomaly rather than promoted to "
		"a false placement, the same treatment Monster Bash's curation gave its GIbot light11 anomaly.",
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
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
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
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Identity, controller platform, address enumeration, mechanism inventory/behavior, variant coverage, and "
		"recreation knowledge are all complete and validated. Promotion to `author_ready` is refused for two "
		"reasons: `conflict.clock-motor-direction-naming` is a genuine, unresolved disagreement between pinned "
		"PinMAME's internal #define names and two independent sources (the printed manual and the retained script "
		"author's own cross-reference comment) about which of solenoids 56/57 is the clock's forward drive line, "
		"and a small number of addresses (switches 26/45/46/55 and GI address 2) have no validated playfield "
		"placement because no bound VPX object exists for them in the retained extraction. The definition therefore "
		"carries a non-empty `conflicts` array, `coverage.dimensions.semantic_naming = \"conflicted\"`, and "
		"`coverage.missing = [\"spatial_placement\", \"unresolved_conflicts\"]`. Resolving the clock-direction "
		"conflict needs a LibPinMAME harness trace or the missing D.C. Motor Control Assembly schematic; resolving "
		"the remaining spatial gaps needs either a corrected retained table build or the missing 2-50 manual page.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table read from the rendered manual pages, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- Raw retained-table object geometry, SHA-256 `{VPX_GEOMETRY_SHA256}`.",
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
		print("Twilight Zone retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
