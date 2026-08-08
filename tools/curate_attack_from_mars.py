"""Curate the physical Bally Attack From Mars (1995) machine definition.

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
DEFINITION_PATH = ROOT / "machines/author-ready/bally/attack-from-mars-1995.json"
PARTIAL_PATH = ROOT / "machines/partial/bally/attack-from-mars-1995.json"
SEED_PATH = ROOT / "tools/seeds/bally/attack-from-mars-1995.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/attack-from-mars-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/attack-from-mars-1995.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.bally.attack-from-mars.1995"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.attack-from-mars.1995"
VPX_TABLE_SOURCE = "vpx-table.afm-jpsalas-3-0-2"
VPX_SCRIPT_SOURCE = "vpx-script.afm-jpsalas-3-0-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.afm-jpsalas-3-0-2"
ROM_SOURCE = "rom.afm-authorized-corpus"
RUNTIME_SOURCE = "runtime.attack-from-mars.boot-attract-and-ball-start"

TABLE_SHA256 = "f4bd2ae0e456030d14ea2f6f8fcd45e0e4f72ff22235a908d17424f1e9441cbd"
SCRIPT_SHA256 = "46992cf7854853bac592ab9b2b5f65d641727accec8405b7aff84fbc8e2aa139"
MANUAL_SHA256 = "5900c779f3bfb14251ada18d25a4dde84dd608b6ddd988ece8c92ea20fd0114b"
ROM_SHA256 = "378102edfd80d650bf6810d5e521fd08cfd972f8732f3c2204f5929d2266358d"
MANUAL_TRANSCRIPTION_SHA256 = "eecef9b72e309e581c07fd5ecc8c5b4f9d3808f5bf4a4a3fdf53891e10296733"

# Rendered manual pages that a human actually read to decide a canonical value. Recording their
# hashes makes an empty or substituted render cache an audit failure rather than an assumed source.
VISUAL_REVIEW_CACHE = (
	("p-03.png", "2c8a09af5708d06158d0530fce2454e7c75adfd27406d827a97af19ef563e46d", "Printed page 1: menu operation and the T.1-T.20 test list, including the four game-specific tests T.16 Loop/Gate, T.17 Saucer LED, T.18 Drop Target and T.19 Motor Bank"),
	("p-04.png", "d09f4ac1d5cf34bc7d021dd842beeb37cd88aa218d49f061c044db5e5c0b64ed", "Printed page 2: complete lamp matrix with column/row wiring, plus lamp locations 11-58"),
	("p-05.png", "61cf5eeed7da2476e35e3672f702f08ac7b82080c146dda7b3fe895b861b9f3b", "Printed page 3: lamp-locations playfield map and lamp locations 61-88"),
	("p-06.png", "24c01a1f467f7d3e3100cff7e87b190ae167892db5d250e445eebb2c5a7b4f14", "Printed page 4: complete switch matrix with dedicated, row, column and Fliptronic wiring, plus switch locations F1-F8 and 11-48"),
	("p-07.png", "12b0fb9c4f5894361160744a38076c2a9752f31d351298a4ee42f5b8b9080736", "Printed page 5: switch-locations playfield map and switch locations 51-78"),
	("p-08.png", "d8d4dbb5d9581ad13822be36aa9e4d151fe64846db7cd9ecc40c4bc0626767fe", "Printed page 6: solenoid/flasher table and solenoid locations 01-16"),
	("p-09.png", "36f4dd0fa71f0aabf007111486a27ab9a1e038337410add0d72a8e94a097679b", "Printed page 7: solenoid-locations playfield map, solenoid locations 17-39, the five general-illumination circuits and the flipper coils"),
	("p-10.png", "bd358939faa738fcb45c3ca4bdeb53d5a8218585326ebcbd913e786d689b2d10", "Printed page 8: upper playfield parts list naming the four alien mech assemblies, the ball-gate assemblies, the ramp diverter, the 3-bank motor and the ramp assemblies"),
	("p-11.png", "24ddfebc9bf1d457ee248df326f361fb10b32708f7eec5f3cfe5432d510ae794", "Printed page 9: upper playfield parts map"),
	("swparts-06.png", "2165d7ff0fd927e5f1134fb29b6ab848df899799cc99848718dc536596de70ea", "400 dpi crop of printed page 4 switch locations re-read to fix a transcription error in the 5647-12693 part-number groupings and to confirm F5-F8 print no part number"),
	("solhi-08.png", "bb837326cab0c27a307d11dd1cb648c2e87156ec4ed0f2277f6f1384e18b9004", "400 dpi crop of the solenoid/flasher table used to read every wire colour, connector, driver transistor and part number, including 33 RIGHT GATE High Power and 34 LEFT GATE Low Power on J119-6,7"),
	("swmap-07.png", "4a9b4ae57d8fa255fcf34e4ec33e970eefcdde0c69af79bfc0dfa0875c997e93", "300 dpi crop of the switch-locations playfield map; F6 and F8 are drawn outside the playfield with no leader line, matching their Not Used parts entries"),
	("solmap-09.png", "b210941d97fb9dcde79c1261ea7919fdefe4786a9e579c12053a10c5c7e55a8c", "300 dpi crop of the solenoid-locations playfield map used to reconcile every flasher against the retained table, in particular placing solenoid 19 on the right side and solenoid 27 on the left"),
	("upperpf-10.png", "29bce9dbf1f0f4ab5ccc27c7e3f6bc787ba02e95a41b01ff3a86ce3001ddefe0", "300 dpi crop of the upper playfield parts list showing four A-20579/A-20479 alien mech assemblies with distinct figurine support brackets, A-17797-2 Right Ball Gate with A-17797-1 Left Ball Gate, and the wire/plastic ramp assemblies that carry the ramp flashers"),
)

EXTRACTION_RELATIVE_PATH = Path("bally/attack-from-mars-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/attack-from-mars-1995/extraction-manifest.json")
EXTRACTION_MANIFEST_SHA256 = "f2d555ebcf2b9dc563178400d741350006f8627f197eea47e2f2379045dbeb5e"
EXTRACTION_FILE_COUNT = 745
EXTRACTION_TOTAL_BYTES = 17831547

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

DRIVER_IDS = (
	"afm_03", "afm_10", "afm_11", "afm_113", "afm_113b",
	"afm_11pfx", "afm_11u", "afm_f10", "afm_f20", "afm_f32",
)
DRIVER_COMPATIBILITY = {
	"afm_03": (
		"identical",
		"Bally 0.3 prototype game ROM with S0.6 sound for the same physical Attack From Mars machine; "
		"the switch matrix, lamp matrix, solenoid/flasher table and playfield hardware are unchanged.",
	),
	"afm_10": (
		"identical",
		"Bally production 1.0 game ROM with S1.0 sound shipped with the physical machine.",
	),
	"afm_11": (
		"identical",
		"Bally 1.1 game ROM with S1.0 sound; a later firmware revision of the same physical machine "
		"with no controller-address or playfield change.",
	),
	"afm_113": (
		"identical",
		"Bally 1.13 game ROM with S1.1 sound, the clone-tree parent in the pinned catalog and the last "
		"factory revision. Its 1999 catalog year is the firmware release year, not a second physical game.",
	),
	"afm_113b": (
		"identical",
		"Bally 1.13b game ROM with S1.1 sound. This is the driver the retained known-working JPSalas "
		"table binds to and the driver the pinned harness booted; it drives the identical I/O inventory "
		"as 1.0.",
	),
	"afm_11pfx": (
		"compatible",
		"1.1 game ROM re-released by Zen Studios for Pinball FX with modified display text only. It is a "
		"WPC-95 game ROM image for the same physical machine, not a separate product; the physical "
		"playfield, controller generation and every controller address are unchanged.",
	),
	"afm_11u": (
		"compatible",
		"1.1 game ROM re-released by Global VR for the Ultrapin cabinet with modified display text only. "
		"It is a WPC-95 game ROM image for the same physical machine; the physical playfield, controller "
		"generation and every controller address are unchanged.",
	),
	"afm_f10": (
		"compatible",
		"FreeWPC 0.10 community firmware. It is an independently written game program that runs on the "
		"unmodified physical WPC-95 machine and drives the same switch, lamp and solenoid hardware; its "
		"rules and display content differ entirely from the factory ROM.",
	),
	"afm_f20": (
		"compatible",
		"FreeWPC 0.20 community firmware for the unmodified physical machine; same hardware inventory and "
		"addresses as the factory ROM, different rules and display content.",
	),
	"afm_f32": (
		"compatible",
		"FreeWPC 0.32 community firmware for the unmodified physical machine; same hardware inventory and "
		"addresses as the factory ROM, different rules and display content.",
	),
}

# --- Printed switch matrix (manual printed page 4). First digit is the drive column,
# --- second digit is the return row.
SWITCH_LABELS = {
	11: "Launch Button", 13: "Start Button", 14: "Plumb Bob Tilt",
	16: "Left Outlane", 17: "Right Return", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 24: "Always Closed",
	26: "Left Return", 27: "Right Outlane",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2",
	34: "Trough Ball 3", 35: "Trough Ball 4",
	36: "Left Popper", 37: "Right Popper", 38: "Left Top Lane",
	41: 'MARTI"A"N Target', 42: 'MARTIA"N" Target',
	43: 'MAR"T"IAN Target', 44: 'MART"I"AN Target',
	45: "Left Motor Bank", 46: "Center Motor Bank", 47: "Right Motor Bank",
	48: "Right Top Lane",
	51: "Left Slingshot", 52: "Right Slingshot",
	53: "Left Jet", 54: "Bottom Jet", 55: "Right Jet",
	56: '"M"ARTIAN Target', 57: 'M"A"RTIAN Target', 58: 'MA"R"TIAN Target',
	61: "Left Ramp Enter", 62: "Center Ramp Enter", 63: "Right Ramp Enter",
	64: "Left Ramp Exit", 65: "Right Ramp Exit",
	66: "Motor Bank Down", 67: "Motor Bank Up",
	71: "Right Loop High", 72: "Right Loop Low",
	73: "Left Loop High", 74: "Left Loop Low",
	75: "Left Saucer Target", 76: "Right Saucer Target",
	77: "Drop Target", 78: "Center Trough",
}

# Printed opto set: column 3 rows 1-7. afmGameData's inverted-switch mask is 0x7f on column 3,
# which covers exactly 31-37. Switch 38 sits in column 3 row 8 and is not an opto.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37}

# Momentary switches the retained script drives with vpmTimer.PulseSw rather than a held state.
PULSED_SWITCHES = {31, 41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56, 57, 58, 75, 76}

# address -> (schema switch_type, the physical form the manual actually describes). The schema
# vocabulary is deliberately small, so the printed form is preserved in the device notes instead of
# being forced into an invented enum value.
SWITCH_TYPES = {
	11: ("button", "cabinet launch button"), 13: ("button", "cabinet start button"),
	14: ("tilt", "plumb bob tilt"), 18: ("leaf", "shooter-lane rollover"),
	21: ("tilt", "slam tilt leaf"), 22: ("leaf", "coin door interlock leaf"),
	16: ("leaf", "lane rollover"), 17: ("leaf", "lane rollover"),
	26: ("leaf", "lane rollover"), 27: ("leaf", "lane rollover"),
	38: ("leaf", "top-lane rollover"), 48: ("leaf", "top-lane rollover"),
	41: ("leaf", "standup target"), 42: ("leaf", "standup target"),
	43: ("leaf", "standup target"), 44: ("leaf", "standup target"),
	45: ("leaf", "moving target on the 3-bank"), 46: ("leaf", "moving target on the 3-bank"),
	47: ("leaf", "moving target on the 3-bank"),
	51: ("leaf", "slingshot kicker and score leaf pair"),
	52: ("leaf", "slingshot kicker and score leaf pair"),
	53: ("leaf", "jet bumper wafer"), 54: ("leaf", "jet bumper wafer"), 55: ("leaf", "jet bumper wafer"),
	56: ("leaf", "standup target"), 57: ("leaf", "standup target"), 58: ("leaf", "standup target"),
	61: ("leaf", "ramp wireform rollover"), 62: ("leaf", "ramp wireform rollover"),
	63: ("leaf", "ramp wireform rollover"), 64: ("leaf", "ramp wireform rollover"),
	65: ("leaf", "ramp wireform rollover"),
	66: ("leaf", "motor bank position leaf"), 67: ("leaf", "motor bank position leaf"),
	71: ("leaf", "loop rollover"), 72: ("leaf", "loop rollover"),
	73: ("leaf", "loop rollover"), 74: ("leaf", "loop rollover"),
	75: ("leaf", "saucer target"), 76: ("leaf", "saucer target"),
	77: ("leaf", "drop target"), 78: ("leaf", "centre trough rollover"),
}

# (assembly_part_number, part_number) exactly as the switch-locations parts list prints them.
SWITCH_PARTS = {
	11: (None, "20-9663-B-4"), 13: (None, "20-9663-2"), 14: (None, "04-10346"),
	16: (None, "5647-12693-19"), 17: (None, "5647-12693-19"), 18: (None, "5647-12693-32"),
	22: (None, "5643-09288-00"), 24: (None, "5643-09112-00"),
	26: (None, "5647-12693-19"), 27: (None, "5647-12693-19"),
	31: ("A-18617-1", "A-18618-1"), 32: ("A-18617-1", "A-18618-1"), 33: ("A-18617-1", "A-18618-1"),
	34: ("A-18617-1", "A-18618-1"), 35: ("A-18617-1", "A-18618-1"),
	36: ("A-16908", "A-16909"), 37: ("A-16908", "A-16909"),
	38: (None, "5647-12693-19"),
	41: (None, "A-18018-21"), 42: (None, "A-18018-21"), 43: (None, "A-18018-21"), 44: (None, "A-18018-21"),
	45: ("A-20683", "SW-1A-201-4"), 46: ("A-20683", "SW-1A-200-4"), 47: ("A-20683", "SW-1A-200-4"),
	48: (None, "5647-12693-19"),
	51: ("A-17801", "SW-1A-114"), 52: ("A-17801", "SW-1A-114"),
	53: ("A-12030-3", "SW-11A-37-1"), 54: ("A-12030-3", "SW-11A-37-1"), 55: ("A-12030-3", "SW-11A-37-1"),
	56: (None, "A-18018-21"), 57: (None, "A-18018-21"), 58: (None, "A-18018-21"),
	61: (None, "5647-12693-11"), 62: (None, "5647-12693-11"), 63: (None, "5647-12693-11"),
	64: (None, "5647-12693-21"), 65: (None, "5647-12693-13"),
	66: ("A-20572", "5647-12693-06"), 67: ("A-20572", "5647-12693-06"),
	71: (None, "5647-12693-19"), 72: (None, "5647-12693-19"),
	73: (None, "5647-12693-19"), 74: (None, "5647-12693-19"),
	75: (None, "A-20784-4"), 76: (None, "A-20784-4"),
	77: ("A-20657", "5647-12693-31"), 78: ("A-20658", "5647-12693-26"),
}

# Printed switch-matrix wiring. Drive is White-*, return is Green-*.
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
	1: ("Orange-Brown", "J205-1", "U17-5"), 2: ("Orange-Red", "J205-2", "U17-11"),
	3: ("Orange-Black", "J205-3", "U17-11"), 4: ("Orange-Yellow", "J205-4", "U17-9"),
	5: ("Orange-Green", "J205-6", "U16-9"), 6: ("Orange-Blue", "J205-7", "U16-11"),
	7: ("Orange-Violet", "J205-8", "U16-7"), 8: ("Orange-Gray", "J205-9", "U16-5"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin", "Printed Left Coin Chute."),
	2: ("Center Coin Chute", "cabinet.coin", "Printed Center Coin Chute."),
	3: ("Right Coin Chute", "cabinet.coin", "Printed Right Coin Chute."),
	4: ("Fourth Coin Chute", "cabinet.coin", "Printed 4th Coin Chute; fitted only on cabinets with a fourth chute."),
	5: ("Service Credits / Escape", "cabinet.service", "Printed Service Credits in normal play and Escape in test mode."),
	6: ("Volume Down / Down", "cabinet.service", "Printed Volume Down in normal play and Down in test mode."),
	7: ("Volume Up / Up", "cabinet.service", "Printed Volume Up in normal play and Up in test mode."),
	8: ("Begin Test / Enter", "cabinet.service", "Printed Begin Test in normal play and Enter in test mode."),
}
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Trough Eject", 3: "Left Popper", 4: "Right Popper",
	5: "Left Alien Low", 6: "Left Alien High", 7: "Knocker", 8: "Right Alien High",
	9: "Left Slingshot", 10: "Right Slingshot", 11: "Left Jet", 12: "Bottom Jet",
	13: "Right Jet", 14: "Right Alien Low", 15: "Saucer Shake", 16: "Drop Target",
	17: "Right Ramp High Flasher", 18: "Right Ramp Low Flasher",
	19: "Right Side High Flasher", 20: "Right Side Low Flasher",
	21: "Center Arrow Flasher", 22: "Jets Flasher", 23: "Saucer Dome Flasher",
	24: "Motor Bank Motor",
	25: "Left Ramp Left Flasher", 26: "Left Ramp Right Flasher",
	27: "Left Side High Flasher", 28: "Left Side Low Flasher",
	33: "Right Gate", 34: "Left Gate", 35: "Diverter Power", 36: "Diverter Hold",
	37: "Saucer L.E.D. Clock", 38: "Saucer L.E.D. Data", 39: "Strobe Light",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}

VIRTUAL_SOLENOID_LABELS = {
	29: "WPC State Channel 29", 30: "WPC State Channel 30",
	31: "WPC Fast-Flip Game-On State", 32: "WPC State Channel 32",
	40: "Unused LPDC Output 40",
	41: "LPDC Mirror Of Saucer L.E.D. Clock", 42: "LPDC Mirror Of Saucer L.E.D. Data",
	43: "LPDC Mirror Of Strobe Light", 44: "Unused LPDC Mirror 44",
	49: "PinMAME Simulator Ball Shooter", 50: "Reserved Output Position 50",
	51: "Custom Duplicate Of Right Gate", 52: "Custom Duplicate Of Left Gate",
	53: "Custom Duplicate Of Diverter",
}

# (control_wire, control_connection, driver_transistor, power_connection, part_number, printed_type)
SOLENOID_WIRING = {
	1: ("Violet-Brown", "J116-1", "Q72", "J133-2", "AE-23-800", "High Power"),
	2: ("Violet-Red", "J116-2", "Q68", "J133-2", "AE-26-1500", "High Power"),
	3: ("Violet-Orange", "J116-4", "Q71", "J133-2", "AE-26-800", "High Power"),
	4: ("Violet-Yellow", "J116-5", "Q67", "J133-2", "AE-25-1000", "High Power"),
	5: ("Violet-Green", "J116-6", "Q70", "J133-2", "AE-26-1500", "High Power"),
	6: ("Violet-Blue", "J116-7", "Q66", "J133-2", "AE-26-1500", "High Power"),
	7: ("Violet-Black", "J116-8", "Q69", "J133-2", "AE-23-800", "High Power"),
	8: ("Violet-Gray", "J116-9", "Q65", "J133-2", "AE-26-1500", "High Power"),
	9: ("Brown-Black", "J113-1", "Q44", "J133-3", "AE-26-1200", "Low Power"),
	10: ("Brown-Red", "J113-3", "Q48", "J133-3", "AE-26-1200", "Low Power"),
	11: ("Brown-Orange", "J113-4", "Q43", "J133-3", "AE-26-1200", "Low Power"),
	12: ("Brown-Yellow", "J113-5", "Q47", "J133-3", "AE-26-1200", "Low Power"),
	13: ("Brown-Green", "J113-6", "Q42", "J133-3", "AE-26-1200", "Low Power"),
	14: ("Brown-Blue", "J113-7", "Q46", "J133-3", "AE-26-1500", "Low Power"),
	15: ("Brown-Violet", "J113-8", "Q41", "J133-3", "AE-26-1500", "Low Power"),
	16: ("Brown-Gray", "J113-9", "Q45", "J133-3", "AE-26-1200", "Low Power"),
	17: ("Black-Brown", "J111-1", "Q28", "J133-6", None, "Flasher"),
	18: ("Black-Red", "J111-2", "Q32", "J133-6", None, "Flasher"),
	19: ("Black-Orange", "J111-3", "Q27", "J133-6", None, "Flasher"),
	20: ("Black-Yellow", "J111-4", "Q31", "J133-6", None, "Flasher"),
	21: ("Blue-Green", "J111-5", "Q26", "J133-6", None, "Flasher"),
	22: ("Blue-Black", "J111-6", "Q30", "J133-6", None, "Flasher"),
	23: ("Blue-Violet", "J111-7", "Q25", "J133-6", None, "Flasher"),
	24: ("Blue-Gray", "J111-8", "Q29", "J140-2", "14-8023", "Flasher"),
	25: ("Blue-Brown", "J109-1", "Q16", "J133-6", None, "Gen. Purpose"),
	26: ("Blue-Red", "J109-2", "Q15", "J133-6", None, "Gen. Purpose"),
	27: ("Blue-Orange", "J109-3", "Q14", "J133-6", None, "Gen. Purpose"),
	28: ("Blue-Yellow", "J109-4", "Q13", "J133-6", None, "Gen. Purpose"),
	33: ("Yellow-Violet", "J120-6", "Q84", "J119-6,7", "A-14406", "High Power"),
	34: ("Orange-Violet", "J120-4", "Q86", "J119-6,7", "A-14406", "Low Power"),
	35: ("Yellow-Gray", "J120-3", "Q81", "J119-8,9", "A-20099", "High Power"),
	36: ("Orange-Gray", "J120-1", "Q83", "J119-8,9", "A-20099", "Low Power"),
	37: ("Brown-White", "J110-1", None, "J140-2", None, "Flasher"),
	38: ("Violet-White", "J110-3", None, "J140-2", None, "Flasher"),
	39: ("Orange-White", "J110-4", None, "J140-2", None, "Flasher"),
	45: ("Yellow-Green", "J120-13", "Q90", "J119-1", "FL-11629", "Flipper Power"),
	46: ("Orange-Green", "J120-11", "Q92", "J119-1", "FL-11629", "Flipper Hold"),
	47: ("Yellow-Blue", "J120-9", "Q87", "J119-4", "FL-11629", "Flipper Power"),
	48: ("Orange-Blue", "J120-7", "Q89", "J119-4", "FL-11629", "Flipper Hold"),
}

SOLENOID_ASSEMBLIES = {
	1: "A-14525", 2: "A-19963-1", 3: "A-20633", 4: "A-20573", 5: "A-20579-1", 6: "A-20579-2",
	7: "B-10686-1", 8: "A-20579-1", 9: "B-9362-L-2", 10: "B-9362-R-3", 11: "A-9415-2",
	12: "A-9415-2", 13: "A-9415-2", 14: "A-20579-1", 15: "A-20608", 16: "A-20657",
	17: "A-20621", 18: "A-20621", 19: "A-20549", 20: "A-17983", 21: "A-20624", 22: "A-17803",
	23: "A-20670", 24: "A-20572", 25: "A-20553", 26: "A-20553", 27: "A-20546", 28: "A-17983",
	33: "A-17796", 34: "A-17796", 35: "A-17241", 36: "A-17241",
	37: "A-20670", 38: "A-20670", 39: "A-20718",
	45: "A-15849-R-2", 46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}

SOLENOID_CALLBACKS = {
	1: 'SolCallback(1) = "Auto_Plunger"',
	2: 'SolCallback(2) = "SolRelease"',
	3: 'SolCallback(3) = "bsL.SolOut"',
	4: 'SolCallback(4) = "Sol4"',
	5: 'SolCallback(5) = "SolAlien5"',
	6: 'SolCallback(6) = "SolAlien6"',
	7: 'SolCallback(7) = "vpmSolSound SoundFX(""fx_Knocker"",DOFKnocker),"',
	8: 'SolCallback(8) = "SolAlien8"',
	14: 'SolCallback(14) = "SolAlien14"',
	16: 'SolCallback(16) = "SolDropTargetUp"',
	17: 'SolModCallback(17) = "SetModLamp 117," binding f17a with the f17b and f17c wall glows',
	18: 'SolModCallback(18) = "SetModLamp 118," binding f18a with the f18b and f18c wall glows',
	19: 'SolModCallback(19) = "SetModLamp 119," binding f19a with the f19b wall glow',
	20: 'SolModCallback(20) = "SetModLamp 120," binding f20 with the f20b wall glow',
	21: 'SolModCallback(21) = "SetModLamp 121," binding f21 and f21a',
	22: 'SolModCallback(22) = "SetModLamp 122," binding f22',
	23: 'SolCallback(23) = "SetLamp 123," binding f23 and f23a',
	24: "the retained script drives the motor through cvpmMech Mech3Bank with .Sol1 = 24, not a direct callback",
	25: 'SolModCallback(25) = "SetModLamp 125," binding f25a with the f25b and f25c wall glows',
	26: 'SolModCallback(26) = "SetModLamp 126," binding f26a with the f26b wall glow',
	27: 'SolModCallback(27) = "SetModLamp 127," binding f27a with the f27b wall glow',
	28: 'SolModCallback(28) = "SetModLamp 128," binding f28 with the f28b wall glow',
	33: 'SolCallback(33) = "vpmSolGate RGate,false,"',
	34: 'SolCallback(34) = "vpmSolGate LGate,false,"',
	36: 'SolCallback(36) = "SolDiv"',
	45: "SolCallback(sLRFlipper) = \"SolRFlipper\" through core.vbs",
	47: "SolCallback(sLLFlipper) = \"SolLFlipper\" through core.vbs",
}

# PinMAME's public lower-flipper addresses are 45-48; the printed table numbers the same circuits
# 29-32. Every other printed number matches its public address on this machine.
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}

# (printed flashlamp complement, physical bulb quantity, bulbs given a playfield coordinate)
FLASHER_BULBS = {
	17: ("#906 playfield with a second #906 in the backbox", 2, 1),
	18: ("#906 playfield with a second #906 in the backbox", 2, 1),
	19: ("#906 playfield with a second #906 in the backbox", 2, 1),
	20: ("#89", 1, 1),
	21: ("#906", 1, 1),
	22: ("#89", 1, 1),
	23: ("#906", 1, 1),
	25: ("#906 playfield with a second #906 in the backbox", 2, 1),
	26: ("#906 playfield with a second #906 in the backbox", 2, 1),
	27: ("#906 playfield with a second #906 in the backbox", 2, 1),
	28: ("#89", 1, 1),
}

LAMP_LABELS = {
	11: "Super Jets", 12: "Super Jackpot", 13: "Martian Attack Multiball", 14: "Annihilation",
	15: "Return To Battle", 16: "Conquer Mars", 17: "5-Way Combo", 18: "Drop Target",
	21: "Big-O-Beam 1", 22: "Big-O-Beam 2", 23: "Big-O-Beam 3", 24: "Left Ramp Jackpot",
	25: "Left Ramp Arrow", 26: "Lock 2", 27: "Lock 3", 28: "Center Ramp Jackpot",
	31: "Tractor Beam 1", 32: "Tractor Beam 2", 33: "Tractor Beam 3", 34: "Right Ramp Jackpot",
	35: "Right Ramp Arrow", 36: "Martian Attack", 37: "Rule Universe", 38: "Stroke Of Luck",
	41: "Right Loop Arrow", 42: "Center Ramp Arrow", 43: "Left Top Lane", 44: "Right Top Lane",
	45: "Left Motor Bank", 46: "Center Motor Bank", 47: "Right Motor Bank", 48: 'MAR"T"IAN Target',
	51: "Attack Mars", 52: "D.C. U.S.A.", 53: "London England", 54: "Light Lock",
	55: "Lock 1", 56: "Pisa Italy", 57: "Berlin Germany", 58: "Paris France",
	61: 'MARTIA"N" Target', 62: 'MARTI"A"N Target', 63: "Atomic Blaster 1", 64: "Atomic Blaster 2",
	65: "Atomic Blaster 3", 66: "Right Loop Jackpot", 67: "Extra Ball", 68: 'MART"I"AN Target',
	71: "Capture 1", 72: "Capture 2", 73: "Capture 3", 74: "Left Loop Jackpot",
	75: "Left Loop Arrow", 76: '"M"ARTIAN Target', 77: 'M"A"RTIAN Target', 78: 'MA"R"TIAN Target',
	81: "Shoot Again", 82: "Left Outlane", 83: "Left Return", 84: "Right Return",
	85: "Right Outlane", 86: "Launch Button", 88: "Start Button",
}

# (assembly_part_number, printed bulb type) from the lamp-locations parts list.
LAMP_ASSEMBLIES = {
	11: ("A-20622", "#555"), 12: ("A-20622", "#555"), 13: ("A-20622", "#555"), 14: ("A-20622", "#555"),
	15: ("A-20622", "#555"), 16: ("A-20622", "#555"), 17: ("A-20622", "#555"), 18: ("A-17807", "#555"),
	21: ("A-20624", "#555"), 22: ("A-20624", "#555"), 23: ("A-20624", "#555"), 24: ("A-20624", "#555"),
	25: ("A-20624", "#555"), 26: ("A-20624", "#555"), 27: ("A-20624", "#555"), 28: ("A-20624", "#555"),
	31: ("A-20624", "#555"), 32: ("A-20624", "#555"), 33: ("A-20624", "#555"), 34: ("A-20624", "#555"),
	35: ("A-20624", "#555"), 36: ("A-20624", "#555"), 37: ("A-20624", "#555"), 38: ("A-20624", "#555"),
	41: ("A-17835", "#555"), 42: ("A-20624", "#555"), 43: ("A-17835", "#555"), 44: ("A-17835", "#555"),
	45: ("A-20624", "#555"), 46: ("A-20624", "#555"), 47: ("A-20624", "#555"), 48: ("A-20624", "#555"),
	51: ("A-20624", "#555"), 52: ("A-20624", "#555"), 53: ("A-20624", "#555"), 54: ("A-20624", "#555"),
	55: ("A-20624", "#555"), 56: ("A-20624", "#555"), 57: ("A-20624", "#555"), 58: ("A-20624", "#555"),
	61: ("A-20624", "#555"), 62: ("A-20624", "#555"), 63: ("A-20624", "#555"), 64: ("A-20624", "#555"),
	65: ("A-20624", "#555"), 66: ("A-20624", "#555"), 67: ("A-20624", "#555"), 68: ("A-20624", "#555"),
	71: ("A-20623", "#555"), 72: ("A-20623", "#555"), 73: ("A-20623", "#555"), 74: ("A-20623", "#555"),
	75: ("A-20623", "#555"), 76: ("A-20629", "#555"), 77: ("A-20629", "#555"), 78: ("A-20629", "#555"),
	81: ("A-17807", "#555"), 82: ("A-17835", "#555"), 83: ("A-17835", "#555"), 84: ("A-17835", "#555"),
	85: ("A-17835", "#555"), 86: ("20-9663-B-4", "#555"), 87: (None, None), 88: ("20-9663-2", "#555"),
}

LAMP_QUANTITIES = {15: 2}

LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
	3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Yellow", "J121-4", "Q99"),
	5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
	3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
	5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}

# The saucer LED ring on board A-20670, shifted in serially by public solenoids 37 and 38 and
# reported at PinMAME's two auxiliary lamp columns.
SAUCER_LED_ADDRESSES = (91, 92, 93, 94, 95, 96, 97, 98, 101, 102, 103, 104, 105, 106, 107, 108)

# (label, control_wire, control_connection, driver_transistor, power_connection, bulb)
GI_STRINGS = {
	0: ("Bottom Playfield General Illumination", "White-Brown", "J105-7", "Q5", "J105-1", "#44 playfield with #555 in the backbox"),
	1: ("Middle Playfield General Illumination", "White-Orange", "J105-8", "Q4", "J105-2", "#44, #555"),
	2: ("Top Playfield General Illumination", "White-Yellow", "J105-9", "Q3", "J105-3", "#44, #555"),
	3: ("Top Insert Panel General Illumination", "White-Green", "J106-10", "Q2", "J106-5", "#555"),
	4: ("Bottom Insert Panel General Illumination", "White-Violet", "J106-11", "Q1", "J106-6", "#555"),
}

SWITCH_POSITIONS = {
	16: [(0.036480, 0.731410)], 17: [(0.785609, 0.731729)], 18: [(0.940674, 0.902435)],
	26: [(0.104641, 0.731158)], 27: [(0.855326, 0.731519)],
	31: [(0.871687, 0.866808)], 32: [(0.871687, 0.866808)], 33: [(0.871687, 0.866808)],
	34: [(0.871687, 0.866808)], 35: [(0.871687, 0.866808)],
	36: [(0.251465, 0.101238)], 37: [(0.673171, 0.292502)], 38: [(0.627343, 0.068706)],
	41: [(0.794865, 0.542192)], 42: [(0.801349, 0.567169)],
	43: [(0.367998, 0.276870)], 44: [(0.615923, 0.277102)],
	45: [(0.432832, 0.260753)], 46: [(0.489627, 0.260753)], 47: [(0.546681, 0.260753)],
	48: [(0.724144, 0.066869)],
	51: [(0.207504, 0.722160)], 52: [(0.678207, 0.724389)],
	53: [(0.631674, 0.148081)], 54: [(0.791166, 0.205840)], 55: [(0.816840, 0.114547)],
	56: [(0.099455, 0.595036)], 57: [(0.111515, 0.568730)], 58: [(0.122407, 0.542597)],
	61: [(0.141023, 0.194046)], 62: [(0.402588, 0.082351)], 63: [(0.804870, 0.258838)],
	64: [(0.263916, 0.063628)], 65: [(0.946533, 0.246727)],
	66: [(0.490145, 0.254403)], 67: [(0.490145, 0.254403)],
	71: [(0.931943, 0.110734)], 72: [(0.905637, 0.278514)],
	73: [(0.083371, 0.116313)], 74: [(0.054929, 0.221688)],
	75: [(0.419346, 0.194886)], 76: [(0.560166, 0.194424)],
	77: [(0.490405, 0.163434)], 78: [(0.489807, 0.130739)],
}

# Switch addresses whose coordinate is an explicit projection onto a documented assembly anchor
# rather than a directly named table object for that switch.
SWITCH_PROJECTIONS = {
	31: "Projected onto the retained trough-exit kicker BallRelease. The retained table models the trough as an abstract four-ball cvpmTrough with no per-position objects, so no per-ball coordinate is observable from it; the manual switch-location map places the whole trough under the apron with the eject opto outboard of Trough Ball 1.",
	32: "Projected onto the retained trough-exit kicker BallRelease; see switch 31. Trough Ball 1 is the position nearest the eject.",
	33: "Projected onto the retained trough-exit kicker BallRelease; see switch 31.",
	34: "Projected onto the retained trough-exit kicker BallRelease; see switch 31.",
	35: "Projected onto the retained trough-exit kicker BallRelease; see switch 31. Trough Ball 4 is the position furthest from the eject.",
	66: "Projected onto the retained backbank moving-target assembly. The position switch is under the playfield inside 3-bank motor assembly A-20572 and has no separate table object.",
	67: "Projected onto the retained backbank moving-target assembly. The position switch is under the playfield inside 3-bank motor assembly A-20572 and has no separate table object.",
}

SOLENOID_POSITIONS = {
	1: [(0.940674, 0.902435)],
	2: [(0.871687, 0.866808)],
	3: [(0.251465, 0.101238)],
	4: [(0.673171, 0.292502)],
	5: [(0.137141, 0.534795)],
	6: [(0.369295, 0.271277)],
	8: [(0.622407, 0.270352)],
	9: [(0.207504, 0.722160)],
	10: [(0.678207, 0.724389)],
	11: [(0.631674, 0.148081)],
	12: [(0.791166, 0.205840)],
	13: [(0.816840, 0.114547)],
	14: [(0.826357, 0.541471)],
	15: [(0.494813, 0.209528)],
	16: [(0.490405, 0.163434)],
	17: [(0.897303, 0.089732)],
	18: [(0.779046, 0.191489)],
	19: [(0.904798, 0.462754)],
	20: [(0.857884, 0.537003)],
	21: [(0.490664, 0.347826)],
	22: [(0.743776, 0.152005)],
	23: [(0.495851, 0.210715)],
	24: [(0.490145, 0.254403)],
	25: [(0.089014, 0.054028)],
	26: [(0.341286, 0.052266)],
	27: [(0.098482, 0.286742)],
	28: [(0.056017, 0.531452)],
	33: [(0.770325, 0.020942)],
	34: [(0.564880, 0.019853)],
	35: [(0.384336, 0.102451)],
	36: [(0.384336, 0.102451)],
	39: [(0.494813, 0.209066)],
	45: [(0.614088, 0.847287)],
	46: [(0.614088, 0.847287)],
	47: [(0.281796, 0.847287)],
	48: [(0.281796, 0.847287)],
}

# Solenoid addresses whose coordinate is an explicit projection rather than a directly named
# table object for that device.
SOLENOID_PROJECTIONS = {
	1: "Projected onto the retained shooter-lane trigger swPlunger. The retained table drives the auto plunger through cvpmImpulseP bound to that trigger and models no separate kicker object; the manual solenoid-location map places kicker bracket A-14525 at the back of the same shooter lane.",
	17: "Taken from the origin of the retained flasher object f17a. Solenoids 17, 18, 19, 25, 26 and 27 have no separate emitter object in the retained table: the author draws each as a raised flare quad at the bulb position plus one or two wall-glow quads projected onto the cabinet walls. The flare origin is the bulb position and is used as the anchor; the wall glows are excluded because they are light spill, not sockets.",
	18: "Taken from the origin of the retained flasher object f18a; see solenoid 17.",
	19: "Taken from the drag-point centroid of the retained flasher object f19a rather than its stored pos_x/pos_y, which the table author left at a stale (71, 800) on the left. This is the one flasher whose stored origin is wrong. The centroid, the matching f19b right-wall glow at the same y, the manual solenoid-location map, and the printed assembly A-20549 Right Wire Ramp all place Right Side High on the right of the playfield.",
	25: "Taken from the origin of the retained flasher object f25a; see solenoid 17.",
	26: "Taken from the origin of the retained flasher object f26a; see solenoid 17.",
	27: "Taken from the origin of the retained flasher object f27a; see solenoid 17.",
	35: "Projected onto the retained diverter blade primitive DivP. The retained table actuates the diverter through an invisible flipper object parked off the playfield at (0.843508, 0.984320), which is a physics helper and not the physical blade location.",
	36: "Projected onto the retained diverter blade primitive DivP; see solenoid 35. The hold winding acts on the same blade as the power winding.",
	45: "Projected onto the retained RightFlipper object; the power and hold windings are the two windings of the same FL-11629 coil on assembly A-15849-R-2.",
	46: "Projected onto the retained RightFlipper object; see solenoid 45.",
	47: "Projected onto the retained LeftFlipper object; the power and hold windings are the two windings of the same FL-11629 coil on assembly A-15849-L-2.",
	48: "Projected onto the retained LeftFlipper object; see solenoid 47.",
}

LAMP_POSITIONS = {
	11: [(0.350098, 0.727802)], 12: [(0.296143, 0.746417)], 13: [(0.405762, 0.709405)],
	14: [(0.489258, 0.709731)], 15: [(0.399047, 0.761093), (0.488366, 0.761418)],
	16: [(0.544434, 0.728237)], 17: [(0.598389, 0.747235)], 18: [(0.490097, 0.197727)],
	21: [(0.301204, 0.546161)], 22: [(0.281267, 0.505299)], 23: [(0.260729, 0.465688)],
	24: [(0.241140, 0.426375)], 25: [(0.215973, 0.382283)], 26: [(0.347443, 0.420845)],
	27: [(0.334957, 0.389266)], 28: [(0.319675, 0.350168)],
	31: [(0.626918, 0.564467)], 32: [(0.648133, 0.524403)], 33: [(0.673702, 0.485051)],
	34: [(0.700256, 0.446531)], 35: [(0.720459, 0.403143)], 36: [(0.618264, 0.404576)],
	37: [(0.602447, 0.432689)], 38: [(0.633859, 0.374174)],
	41: [(0.868743, 0.348605)], 42: [(0.299973, 0.305831)], 43: [(0.621368, 0.027212)],
	44: [(0.717315, 0.024938)], 45: [(0.437243, 0.296893)], 46: [(0.490766, 0.297039)],
	47: [(0.542877, 0.297442)], 48: [(0.379756, 0.319632)],
	51: [(0.492432, 0.591381)], 52: [(0.492706, 0.553568)], 53: [(0.492218, 0.515304)],
	54: [(0.374756, 0.484943)], 55: [(0.361725, 0.453932)], 56: [(0.493683, 0.476712)],
	57: [(0.492218, 0.438176)], 58: [(0.492706, 0.400076)],
	61: [(0.750473, 0.572345)], 62: [(0.745895, 0.544226)], 63: [(0.767975, 0.496206)],
	64: [(0.788832, 0.462841)], 65: [(0.810678, 0.430345)], 66: [(0.835803, 0.391917)],
	67: [(0.647003, 0.344197)], 68: [(0.601562, 0.319572)],
	71: [(0.152008, 0.467579)], 72: [(0.132934, 0.433894)], 73: [(0.112915, 0.400679)],
	74: [(0.086685, 0.361752)], 75: [(0.065400, 0.312758)], 76: [(0.152353, 0.600991)],
	77: [(0.164346, 0.573017)], 78: [(0.174362, 0.547321)],
	81: [(0.447021, 0.877424)], 82: [(0.036621, 0.695063)], 83: [(0.111587, 0.679088)],
	84: [(0.781967, 0.679986)], 85: [(0.857422, 0.696593)],
}

# The saucer LED ring is a single physical board; the retained table models no individual LED
# objects, so every address is projected onto the saucer assembly anchor.
SAUCER_LED_POSITION = (0.494813, 0.209528)

GI_POSITIONS = {
	0: [
		(0.158900, 0.714057), (0.734601, 0.715115), (0.196413, 0.759786),
		(0.695262, 0.760521), (0.132615, 0.800555), (0.760148, 0.802321),
		(0.199642, 0.822212), (0.696034, 0.823545),
	],
	1: [
		(0.031154, 0.389652), (0.873861, 0.435822), (0.860045, 0.497424),
		(0.038013, 0.501017), (0.051829, 0.559026), (0.878514, 0.593452),
		(0.048423, 0.598585),
	],
	2: [
		(0.925669, 0.039720), (0.200347, 0.042940), (0.767635, 0.059667),
		(0.672199, 0.065217), (0.578838, 0.067993), (0.057585, 0.080243),
		(0.233925, 0.099924), (0.178856, 0.162037), (0.354622, 0.198998),
		(0.613282, 0.201393), (0.130705, 0.248844), (0.767635, 0.277983),
		(0.204357, 0.296485), (0.790456, 0.308511),
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
		raise RuntimeError(f"Attack From Mars retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Attack From Mars extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Attack From Mars retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Attack From Mars retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Attack From Mars retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the afm_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/afm.c switch and solenoid defines, afmGameData GEN_WPC95 with wpc_dispDMD, "
				"FLIP_SW(FLIP_L|FLIP_U) with FLIP_SOL(FLIP_L), lampCol=2 and custSol=3, the inverted-switch mask "
				"0x7f on column 3, the sRGate/sLGate/sDiverter custom-solenoid definitions whose afm_getSol bit "
				"reads are transposed relative to their own /* 33 */ and /* 34 */ comments and to the printed "
				"table, afm_handleMech bank stepping with swMBankDn/swMBankUp, and afm_wpc_w shifting a 16-bit "
				"word into tmpLampMatrix[8] and [9]; src/wpc/core.h WPC solenoid numbering and WPC_swF1..WPC_swF8; "
				"src/wpc/core.c core_getSol WPC95 37..40 to 41..44 duplication; src/wpc/wpc.c WPC_FLIPPERCOIL95 "
				"writing bits 0-3 to public solenoids 45-48 and bits 4-7 to public solenoids 33-36, WPC_SOLENOID1 "
				"bits 4-7 documented as the J122/J123/J124 GPIO that appear as LPDC outputs 37..40 in manuals, "
				"WPC_FLIPPERSW95 inversion and the J111/fast-flip game-on state; src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WPC95=0x80"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-95.json",
			"revision": "repository",
			"locator": (
				"WPC-95 public switch, DIP, solenoid, lamp and five-GI address rules with the Fliptronic, LPDC "
				"mirror and auxiliary lamp-column notes"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": (
				"external:pinmame-manuals/by-machine/bally.attack-from-mars.1995/"
				"archive-arcademanual_Attack_From_Mars_OPS/Attack_From_Mars_OPS.pdf"
			),
			"original_filename": "Attack_From_Mars_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"Manifest ID archive.arcademanual_Attack_From_Mars_OPS.bally.attack-from-mars.1995.5900c779f3bf; "
				"16-page image-only scan of Bally/Midway Operators Handbook 16-10206. Printed page 1 carries the "
				"test-menu list, printed page 2 the lamp matrix and lamp locations 11-58, printed page 3 the "
				"lamp-locations map and lamp locations 61-88, printed page 4 the switch matrix and switch "
				"locations F1-F8 and 11-48, printed page 5 the switch-locations map and switch locations 51-78, "
				"printed page 6 the solenoid/flasher table and solenoid locations 01-16, printed page 7 the "
				"solenoid-locations map with locations 17-39, the five general-illumination circuits and the "
				"flipper coils, and printed pages 8-9 the upper playfield parts list and map."
			),
			"license": "NOASSERTION",
			"attribution": "Bally/Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/attack-from-mars-1995/manual-transcription.md",
			"revision": "2026-08-05",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every printed table used by this definition, together with the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/bally.attack-from-mars.1995/. "
				"The retained PDF is image-only, so every table was read from rendered pages rather than OCR."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": (
				"external:pinmame-vpx-sources/bally/attack-from-mars-1995/source/"
				"Attack%20from%20Mars%203.02.vpx"
			),
			"original_filename": "Attack from Mars 3.02.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working JPSalas recreation of the physical machine, table version 3.0.2. Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry "
				"authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": (
				"external:pinmame-vpx-sources/bally/attack-from-mars-1995/extracted-vpxtool/script.vbs"
			),
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				"Retained embedded JPSalas script (38,230 bytes). Runtime and mechanism-causality authority: "
				'cGameName = "afm_113b", the SolCallback/SolModCallback table for solenoids 1-43, the '
				"Controller.Switch and vpmTimer.PulseSw switch semantics, the cvpmTrough four-ball stack on "
				"switches 32-35 with BallRelease, the cvpmBallStack right popper on switch 37, the cvpmDropTarget "
				"on switch 77, the cvpmMech Mech3Bank motor bank with .Sol1 = 24 and AddSw 67/66 at steps 0 and "
				"55, and the UpdateGI mapping of GI 0/1/2 to the aGiLLights/aGiMLights/aGiTLights emitter arrays."
			),
			"license": "NOASSERTION",
			"attribution": "JPSalas",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": (
				"external:pinmame-vpx-sources/bally/attack-from-mars-1995/extraction-manifest.json"
			),
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} "
				f"files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. Bounds "
				f"are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": ROM_SOURCE,
			"kind": "rom_static_analysis",
			"uri": "external:pinmame-roms/afm_113b.zip",
			"sha256": ROM_SHA256,
			"locator": (
				"Pre-existing authorized local ROM archive used only to boot the pinned harness; ROM bytes are "
				"never copied into this repository"
			),
			"license": "NOASSERTION",
			"attribution": "Authorized local evidence",
		},
		{
			"id": RUNTIME_SOURCE,
			"kind": "runtime_scenario",
			"uri": "internal:evidence/runtime/wpc-95/attack-from-mars-boot-attract-and-ball-start.json",
			"revision": PINMAME_REVISION,
			"locator": (
				"Pinned LibPinMAME harness runs that boot afm_113b from empty NVRAM, reach attract mode, add "
				"credits and start a ball. They observe all five GI strings, sixty matrix lamps, every one of the "
				"sixteen auxiliary saucer-LED addresses 91-98 and 101-108 across four attract phases, and "
				"solenoids 29, 31, 37, 38, 41 and 42."
			),
			"license": "NOASSERTION",
			"attribution": (
				"Generated locally from PinMAME and the user-authorized ROM corpus; ROM bytes remain external"
			),
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
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE)
		notes = f"Printed dedicated grounded switch D{address}. {note}"
		if address in {5, 6, 7, 8}:
			notes += (
				" PinMAME's MAME-only keyboard port (WPC_COMPORTS) labels these four service bits in the opposite "
				"order; that is a MAME key binding, not public address semantics, and the printed matrix governs."
			)
		items.append(
			_device(
				f"switch.cabinet-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"optional" if address == 4 else "used",
				refs,
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": notes},
				wiring={
					"board": "WPC-95 CPU board",
					"drive_wire": wire,
					"drive_connection": connection,
					"return_component": component,
				},
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
			printed_form: str | None = None
			if address in SWITCH_TYPES:
				physical["switch_type"], printed_form = SWITCH_TYPES[address]
			if address in OPTO_SWITCHES:
				physical["switch_type"] = "opto"
				printed_form = "infrared opto pair"
			notes = (
				f"Printed switch-matrix drive column {column}, return row {row}. The printed matrix is drawn "
				"column-first, so the left digit is the drive column and the right digit is the return row."
			)
			if printed_form:
				notes += f" Physical form: {printed_form}."
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			if address in OPTO_SWITCHES:
				notes += (
					" Printed as a shaded opto that rests closed. afmGameData's inverted-switch mask 0x7f covers "
					"exactly column 3 rows 1-7, so the public switch state is already normalized and must not be "
					"inverted again. Switch 38 shares column 3 but is row 8 and is an ordinary rollover."
				)
			if address == 24:
				notes += (
					" Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is "
					"connected, and afmGameData names it in the always-closed slot."
				)
			if address == 22:
				notes += " Closed while the coin door is closed; opening the door removes solenoid power."
			if address in {45, 46, 47}:
				notes += (
					" Mounted on moving target assembly A-20683, which the 3-bank motor raises and lowers, so the "
					"target is only reachable while the bank is up."
				)
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
				refs = (MANUAL_SOURCE, CORE_SOURCE)
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
					coordinate_refs = (
						(VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316"),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {
			"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"
		}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" Attack From Mars has no upper flippers. The printed switch matrix annotates F5 through F8 "
				"'(NOT USED)' and the switch-locations parts list prints '---' and 'Not Used' for all four, so "
				"these positions are unused even though afmGameData declares FLIP_SW(FLIP_L|FLIP_U). The upper "
				"Fliptronic outputs are still in use: they drive the two ball gates and the ramp diverter."
			)
			physical["location"] = "not installed"
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
			"wiring": {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection},
		}
		if availability == "unused":
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			extra.pop("wiring")
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
				f"CPU DIP {address} (country code bit)",
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
					"location": "WPC-95 CPU board U27",
					"switch_type": "dip",
					"notes": (
						"WPC-95 country-code DIP bank on the CPU board. The retained handbook lists T.15 Dip "
						"Switch Test but prints no country-setting chart, so no per-country pattern is asserted "
						"here."
					),
				},
				spatial=not_applicable("dip_switch", CONTROLLER_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 54):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			drive_wire, drive_connection, transistor, power_connection, part_number, printed_type = SOLENOID_WIRING[address]
			if address == 24:
				kind = "motor"
			elif address in {37, 38}:
				# Serial clock and data lines into the saucer shift register. The printed table lists
				# them under the flasher driver group, but they emit no light of their own: the light
				# they produce is the sixteen saucer L.E.D.s at lamp addresses 91-98 and 101-108.
				# They are not relays either - no relay exists on this circuit - so they use the
				# control_signal kind added for logic-level outputs that drive another board.
				kind = "control_signal"
			elif 17 <= address <= 28 or address == 39:
				kind = "flasher"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			if part_number and address != 24:
				physical["part_number"] = part_number
			if address == 24:
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if address in FLASHER_BULBS:
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" The printed table gives this address a playfield drive on J111 or J109 and a separate "
						"backbox drive on J112 or J107, so only the playfield bulb receives a coordinate while the "
						"physical quantity stays two."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script binding: {SOLENOID_CALLBACKS[address]}."
			if address == 7:
				notes += " Backbox knocker; the printed table routes both its voltage and drive connections through the backbox."
			if address in {17, 18}:
				notes += " Mounted on middle plastic ramp assembly A-20621."
			if address == 19:
				notes += " Mounted on right wire ramp assembly A-20549, which is why this flasher sits on the right side of the playfield."
			if address in {25, 26}:
				notes += " Mounted on left plastic ramp assembly A-20553."
			if address == 27:
				notes += " Mounted on left wire ramp assembly A-20546, which is why this flasher sits on the left side of the playfield."
			if address == 24:
				notes += (
					" The printed table lists this output under the flasher driver group with transistor Q29, but "
					"its load is motor 14-8023 in 3-bank motor assembly A-20572, not a flashlamp."
				)
			if address in {33, 34}:
				notes += (
					" Physically a one-way loop gate wired to the Fliptronic upper-right flipper circuit: 33 is the "
					"power winding and 34 the hold winding of that circuit, which the printed flipper-circuit block "
					"on the same page confirms. afmGameData declares FLIP_SOL(FLIP_L), so the emulator never drives "
					"these as flippers. The left/right naming rests on the physical sources, which agree: the "
					"printed solenoid/flasher table gives 33 RIGHT GATE and 34 LEFT GATE, the upper-playfield parts "
					"list pairs actuator coil A-17796 with A-17797-2 Right Ball Gate Assembly on item 24 and "
					"A-17797-1 Left Ball Gate Assembly on item 25, and both retained known-working scripts bind "
					"SolCallback(33) to the right gate and SolCallback(34) to the left. Pinned PinMAME disagrees "
					"and is also inconsistent with itself, so the disagreement is recorded rather than averaged: "
					"wpc.c writes WPC_FLIPPERCOIL95 bits 4-7 to public solenoids 33-36, making bit 0x10 public 33 "
					"and bit 0x20 public 34, while afm.c reads bit 0x10 for sLGate and bit 0x20 for sRGate - the "
					"opposite naming - even though its own comments annotate sRGate as /* 33 */ and sLGate as "
					"/* 34 */. The manual and the proven scripts govern here because the manual owns physical "
					"identity and the known-working script owns runtime binding."
				)
			if address in {35, 36}:
				notes += (
					" Physically the ramp diverter (A-17241 with shaft and blade A-20556) wired to the Fliptronic "
					"upper-left flipper circuit; 35 is the power winding and 36 the hold winding. PinMAME's afm.c "
					"reads both together as sDiverter from WPC_FLIPPERCOIL95 bits 0xc0."
				)
			if address in {37, 38}:
				notes += (
					" This output emits no light itself and therefore has no playfield placement; it is one of the "
					"two serial control lines into shift-register board A-20670, and the light it ultimately "
					"produces is the sixteen saucer L.E.D.s enumerated at lamp addresses 91-98 and 101-108. The "
					"printed table lists it under the flasher driver group because of the driver circuit it shares, "
					"not because it drives a flashlamp. "
					"WPC-95 auxiliary output on power-driver connector J110 with no drive transistor of its own. "
					"PinMAME duplicates it at public address "
					f"{address + 4}, so a recreation must treat {address} and {address + 4} as one physical signal. "
					"afm_wpc_w shifts a sixteen-bit word into PinMAME's two auxiliary lamp columns using this pair, "
					"and wpc.c documents WPC_SOLENOID1 bits 4-7 as the J122/J123/J124 GPIO that appear as LPDC "
					"outputs 37-40 in manuals. The pinned harness saw 37, 38, 41 and 42 active together with the "
					"saucer LED ring in attract mode and all four go quiet together at ball start."
				)
			if address == 39:
				notes += (
					" WPC-95 auxiliary output on J110-4 driving strobe assembly A-20718 through strobe cable "
					"H-20705. PinMAME duplicates it at public address 43, and the retained JPSalas script binds the "
					"strobe on the mirror address with SolCallback(43) = \"SetLamp 130,\", so a recreation must "
					"treat 39 and 43 as one physical strobe."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias. The power and hold windings share "
					"one FL-11629 blue coil."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {
				"board": "WPC-95 power driver board",
				"control_wire": drive_wire,
				"control_connection": drive_connection,
			}
			if transistor:
				wiring["driver_transistor"] = transistor
			if power_connection:
				wiring["power_connection"] = power_connection
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in {37, 38}:
				extra["roles"] = ["internal.serial-control"]
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
			else:
				role = "emitter" if kind == "flasher" else "effect"
				coordinate_refs = (
					(VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
				)
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *coordinate_refs)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {37, 38, 39}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue

		if address not in VIRTUAL_SOLENOID_LABELS:
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41, 42, 43, 51, 52, 53} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here. The pinned harness observed it active throughout attract mode; it is not an Attack From Mars playfield device.",
			30: "PinMAME publishes the second meaningful WPC J111 general-purpose state bit here; it is not an Attack From Mars playfield device. Failure to observe a transition in the retained harness trace does not make the public channel unused.",
			31: "PinMAME's synthetic game-on state. The pinned harness observed it inactive on a cold boot, active from the moment the service Enter button had been used, and active throughout ball play, so it reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME reports this WPC state channel as always zero on this generation.",
			40: "Unused WPC-95 auxiliary output; Attack From Mars populates LPDC outputs 37, 38 and 39 only.",
			41: "PinMAME's backward-compatibility mirror of auxiliary output 37. It reports the same physical saucer L.E.D. clock signal and is not an additional device; the pinned harness saw 37 and 41 change together.",
			42: "PinMAME's backward-compatibility mirror of auxiliary output 38. It reports the same physical saucer L.E.D. data signal and is not an additional device; the pinned harness saw 38 and 42 change together.",
			43: "PinMAME's backward-compatibility mirror of auxiliary output 39. It reports the same physical strobe light and is not an additional device, but it is the address the retained JPSalas script actually binds, so a recreation must accept the strobe on either 39 or 43.",
			44: "Unused WPC-95 LPDC mirror of output 40.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary.",
			51: "PinMAME custom solenoid CORE_CUSTSOLNO(1), defined in afm.c as sRGate and reading WPC_FLIPPERCOIL95 bit 0x20. wpc.c writes that bit to public solenoid 34, so this is a second view of public solenoid 34 and not an additional device. Note that afm.c\'s own comment annotates this definition /* 33 */ and calls it the right gate, which contradicts both its bit read and the printed table; the definition follows the manual, under which public 34 is the left gate.",
			52: "PinMAME custom solenoid CORE_CUSTSOLNO(2), defined in afm.c as sLGate and reading WPC_FLIPPERCOIL95 bit 0x10. wpc.c writes that bit to public solenoid 33, so this is a second view of public solenoid 33 and not an additional device. Note that afm.c\'s own comment annotates this definition /* 34 */ and calls it the left gate, which contradicts both its bit read and the printed table; the definition follows the manual, under which public 33 is the right gate.",
			53: "PinMAME custom solenoid CORE_CUSTSOLNO(3), defined in afm.c as sDiverter and reading WPC_FLIPPERCOIL95 bits 0xc0. It is a combined view of public solenoids 35 and 36, the ramp diverter power and hold windings, and not an additional device.",
		}[address]
		if address in {41, 42, 43}:
			roles = ["internal.duplicate.lpdc-mirror"]
		elif address in {51, 52, 53}:
			roles = ["internal.duplicate.custom-solenoid"]
		elif address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		else:
			roles = ["internal.unused.wpc-output"]
		refs = (CONTROLLER_SOURCE, CORE_SOURCE)
		if address in {29, 31, 41, 42}:
			refs = (CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE)
		if address == 43:
			refs = (CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				refs,
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
			unused = label is None
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = (
				f"Printed lamp-matrix drive column {column}, return row {row}. The printed matrix is drawn "
				"column-first, so the left digit is the drive column and the right digit is the return row."
			)
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if unused:
				notes += " The printed lamp matrix and the lamp-locations parts list both mark this address Not Used."
				physical.pop("quantity")
			if address in LAMP_QUANTITIES:
				notes += (
					f" The printed lamp matrix marks this address as driving {LAMP_QUANTITIES[address]} bulbs, and "
					"the retained table binds a separate emitter to each (l15 and l15a), so both are placed."
				)
			if address in {86, 88}:
				notes += " Cabinet button lamp inside the illuminated launch or start button assembly."
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
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(
					_device(
						identifier,
						f"Not Used Lamp Position {address}",
						"lamp",
						"pinmame.output.lamp",
						address,
						"unused",
						(MANUAL_SOURCE, CONTROLLER_SOURCE),
						**extra,
					)
				)
				continue
			if address in {86, 88}:
				extra["roles"] = ["cabinet.launch" if address == 86 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(
				_device(
					identifier,
					label,
					"lamp",
					"pinmame.output.lamp",
					address,
					"used",
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
					**extra,
				)
			)

	for index, address in enumerate(SAUCER_LED_ADDRESSES, start=1):
		identifier = f"lamp.saucer-led-{index:02d}"
		items.append(
			_device(
				identifier,
				f"Saucer L.E.D. {index:02d}",
				"lamp",
				"pinmame.output.lamp",
				address,
				"used",
				(CORE_SOURCE, RUNTIME_SOURCE, MANUAL_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={
					"assembly_part_number": "A-20670",
					"quantity": 1,
					"location": "saucer assembly A-20608",
					"notes": (
						"One of the sixteen L.E.D. positions on saucer board A-20670. These are not in the printed "
						"lamp matrix: the ROM shifts a sixteen-bit word into the board through public solenoids 37 "
						"(L.E.D. Clock) and 38 (L.E.D. Data), and PinMAME's afm_wpc_w publishes the result in its "
						"two auxiliary lamp columns, which appear at public lamp addresses 91-98 and 101-108. The "
						"pinned harness observed every one of the sixteen addresses lit across four attract phases, "
						"eight at a time, and dark during ball play. The printed parts list names the board and the "
						"T.17 Saucer LED test but does not number the individual L.E.D.s, so these are numbered "
						"positionally by controller address and carry no printed insert legend."
					),
				},
				wiring={
					"board": "WPC-95 power driver board",
					"control_connection": "J110-1 clock and J110-3 data through strobe cable H-20705",
					"driver_transistor": "serial shift register on saucer board A-20670",
				},
				spatial=located(identifier, "emitter", [SAUCER_LED_POSITION], VPX_TABLE_SOURCE, MANUAL_SOURCE),
			)
		)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_wire, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		physical: dict[str, Any] = {}
		notes = f"Printed general-illumination string {address + 1:02d}; printed bulb type {bulb}."
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-95 power driver board",
				"control_wire": drive_wire,
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			# String 03 has an unresolved socket question (see below), so no count is asserted for it.
			if address != 2:
				physical["quantity"] = len(positions)
			if address == 2:
				notes += (
					" The manual prints no per-string bulb count. Every emitter coordinate below comes from the "
					"retained table's GI emitter array for this string, which pairs each bulb with a co-located "
					"halo light so that only one placement per physical socket is recorded."
				)
			else:
				notes += (
					" The manual prints no per-string bulb count, so the physical quantity and every emitter "
					"coordinate come from the retained table's GI emitter array for this string. The table pairs "
					"each bulb with a co-located halo light, and only one placement per physical socket is recorded."
				)
			if address == 0:
				notes += (
					" The printed table gives this string a playfield harness on J105-1/J105-7 with #44 bulbs and a "
					"separate backbox harness on J106-1/J106-7 with #555 bulbs; only the playfield sockets are "
					"placed and the backbox component has no coordinate or asserted count."
				)
			if address == 2:
				notes += (
					" No physical socket count is asserted for this string, and unlike strings 01 and 02 the "
					"placement set is explicitly not claimed to be exhaustive. The retained script's comment marks "
					"this string as also covering the jet bumpers, and the table carries three further bulb lights "
					"gi31, gi32 and gi33 sitting exactly at the three jet-bumper centres. They are absent from the "
					"aGiTLights collection, which proves only that this table does not modulate them through that "
					"collection; it does not prove the physical sockets are missing. The manual does not itemize "
					"the string, so whether those three are additional string-03 sockets or pure decoration is "
					"unresolved, and the fourteen placements below are the emitters this string is observed to "
					"drive rather than a complete socket inventory."
				)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite. The printed table marks strings 04 and 05 "
				"with a double asterisk and the footnote that they do not brighten and dim but are always on, and "
				"the retained script's UpdateGI handles only the three playfield strings, so this string has no "
				"playfield coordinate. No parts page itemizes the insert-panel sockets, so the physical bulb count "
				"is deliberately not asserted and has to be read from the machine."
			)
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
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
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
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
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

	def alien(identifier: str, label: str, address: int, targets: list[int], where: str, assembly: str) -> dict[str, Any]:
		sensors = [f"switch.matrix-{target}" for target in targets]
		names = ", ".join(SWITCH_LABELS[target] for target in targets)
		return mechanism(
			identifier,
			label,
			"toy",
			[output_id(SOLENOID_LABELS[address])],
			sensors,
			f"One of the four Martian alien figurines (figurine 23-6768 on its own support bracket). The mech sits "
			f"{where} and covers the {names} target group. Coil {address:02d} drives the figurine up and down; the "
			"retained script models the visible motion by translating the alien primitive on the Z axis while the "
			"targets themselves report through the switch matrix. The manual prints four alien mech assemblies, one "
			"per target group, and each carries a distinct figurine support bracket, so a recreation needs four "
			"independent actuators rather than one shared Martian mechanism.",
			[],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number=assembly,
		)

	return [
		mechanism(
			"mechanism.trough",
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on opto pairs 32-35 under the apron, with Trough Ball 1 (32) at the eject end nearest "
			"the shooter lane and Trough Ball 4 (35) furthest from it. Solenoid 02 ejects the ball resting at the "
			"eject end into the shooter lane and the same event asserts trough-eject opto 31. All five positions are "
			"printed as shaded optos that rest closed, built from A-18617-1 LED and A-18618-1 photo-transistor "
			"pairs, and afmGameData's 0x7f column-3 mask normalizes them, so a recreation asserts the public switch "
			"when a ball is present. The retained script models the trough as a four-ball cvpmTrough on switches "
			"32-35 exiting through BallRelease at 80 degrees.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4", ["switch.matrix-35"], "Fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto at the trough exit, asserted as the ball leaves."),
			],
			VPX_SCRIPT_SOURCE,
			MANUAL_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"Attack From Mars has no manual plunger. The ball ejected from the trough rests on shooter-lane switch "
			"18 (A-18973) and auto-plunger coil 01 on kicker bracket A-14525 launches it when the cabinet Launch "
			"Button (switch 11) is pressed. The retained script drives it through cvpmImpulseP bound to the "
			"shooter-lane trigger with switch 18 and a 0.6 second full-plunge time.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			VPX_SCRIPT_SOURCE,
			MANUAL_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.motor-bank",
			"Motorized three-bank moving target",
			"motorized",
			[output_id("Motor Bank Motor")],
			[
				"switch.matrix-45", "switch.matrix-46", "switch.matrix-47",
				"switch.matrix-66", "switch.matrix-67",
			],
			"A motor (14-8023 in 3-bank motor assembly A-20572) raises and lowers moving target assembly A-20683, "
			"which carries the Left, Center and Right Motor Bank targets 45, 46 and 47. Two leaf switches sense the "
			"end positions: 67 Motor Bank Up and 66 Motor Bank Down, both 5647-12693-06. The bank gates access to "
			"the shots behind it, and pinned PinMAME encodes that causality explicitly: its keyboard conditions make "
			"the three moving targets reachable only while 67 Motor Bank Up is closed, and the left and right saucer "
			"targets, the drop target and the centre trough reachable only while 66 Motor Bank Down is closed. "
			"Solenoid 24 is wired through the flasher driver group with transistor Q29 but its load is the motor. "
			"The two retained models number the travel differently and neither is a physical measurement: the "
			"retained script's cvpmMech is linear, reversed and single-solenoid over 55 steps with 67 at one end and "
			"66 at the other, while PinMAME's afm_handleMech steps an internal bankPos counter and asserts 66 near "
			"the start of the cycle and 67 near its midpoint. Both agree the two switches mark opposite ends of one "
			"continuous motor travel.",
			[
				("up", "Bank up", ["switch.matrix-67"], "Moving targets 45-47 presented; the shots behind the bank are blocked."),
				("down", "Bank down", ["switch.matrix-66"], "Bank lowered; the saucer targets, drop target and centre trough behind it become reachable."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-20572",
		),
		mechanism(
			"mechanism.drop-target",
			"Single drop target",
			"drop_target_bank",
			[output_id("Drop Target")],
			["switch.matrix-77"],
			"A one-bank drop target assembly A-20657 behind the motor bank. Switch 77 (5647-12693-31) closes when "
			"the target is knocked down, and coil 16 raises it again: pinned PinMAME clears swDrop whenever the drop "
			"solenoid fires, and the retained script drives the same reset through cvpmDropTarget bound to switch "
			"77. The target is only reachable while the motor bank is down.",
			[
				("up", "Target raised", [], "Target standing; switch 77 open."),
				("down", "Target dropped", ["switch.matrix-77"], "Target knocked down; switch 77 closed until coil 16 resets it."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-20657",
		),
		mechanism(
			"mechanism.left-popper",
			"Left popper",
			"kicker",
			[output_id("Left Popper")],
			["switch.matrix-36"],
			"A single-ball popper (assembly A-20633 with scoop 04-10296) at the top left of the playfield. Opto 36, "
			"built from an A-16908 LED and an A-16909 photo transistor, holds the ball and coil 03 ejects it. The "
			"retained script models it as a one-ball cvpmTrough on switch 36 exiting at 180 degrees. It is also the "
			"destination the ramp diverter selects.",
			[("held", "Ball held in popper", ["switch.matrix-36"], "Opto broken by the resting ball.")],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-20633",
		),
		mechanism(
			"mechanism.right-popper",
			"Right popper",
			"kicker",
			[output_id("Right Popper")],
			["switch.matrix-37"],
			"A single-ball popper (assembly A-20573) on the right of the playfield. Opto 37, again an A-16908 LED "
			"with an A-16909 photo transistor, holds the ball and coil 04 ejects it. The retained script models it "
			"as a cvpmBallStack kicking at 210 degrees with a 65 degree upward component, which is why the ejected "
			"ball arcs rather than rolling out.",
			[("held", "Ball held in popper", ["switch.matrix-37"], "Opto broken by the resting ball.")],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-20573",
		),
		mechanism(
			"mechanism.saucer",
			"Flying saucer with shaker, dome flasher and L.E.D. ring",
			"toy",
			[
				output_id("Saucer Shake"),
				output_id("Saucer Dome Flasher"),
				output_id("Saucer L.E.D. Clock"),
				output_id("Saucer L.E.D. Data"),
				output_id("Strobe Light"),
			],
			["switch.matrix-75", "switch.matrix-76"],
			"The centrepiece flying saucer (assembly A-20608) sits above the playfield centre behind the motor "
			"bank. Coil 15 shakes the saucer body. Flasher 23 lights the dome. Board A-20670 inside the saucer "
			"carries a sixteen-L.E.D. ring that the ROM writes serially: public solenoid 37 is the clock and 38 the "
			"data, and the shifted word appears at public lamp addresses 91-98 and 101-108. Strobe assembly A-20718 "
			"on public solenoid 39, cabled through H-20705, fires the white strobe inside the dome. The left and "
			"right saucer targets 75 and 76 (A-20784-4) are the shots that attack it, and both are only reachable "
			"while the motor bank is down. The pinned harness observed the L.E.D. ring rotating through four "
			"eight-L.E.D. phases in attract mode with solenoids 37, 38 and their mirrors 41 and 42 active, and the "
			"whole ring dark during ball play.",
			[
				("target-left", "Left saucer target", ["switch.matrix-75"], "Left attack target on the saucer."),
				("target-right", "Right saucer target", ["switch.matrix-76"], "Right attack target on the saucer."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			RUNTIME_SOURCE,
			assembly_part_number="A-20608",
		),
		mechanism(
			"mechanism.loop-gates",
			"Left and right one-way loop gates",
			"gate",
			[output_id("Right Gate"), output_id("Left Gate")],
			["switch.matrix-71", "switch.matrix-72", "switch.matrix-73", "switch.matrix-74"],
			"Two ball gates at the top of the playfield control the orbit loops. Each is an A-17796 actuator coil "
			"driving a gate assembly: A-17797-2 on the right (public solenoid 33) and A-17797-1 on the left (public "
			"solenoid 34). Both ride the Fliptronic upper-right flipper circuit, 33 on its power winding and 34 on "
			"its hold winding, which is how a machine with no upper flippers still uses those outputs. Loop travel "
			"is sensed by the high and low switch pairs 71/72 on the right and 73/74 on the left; pinned PinMAME's "
			"simulator uses one gate to turn a right-loop shot into a left-loop return and the other to do the "
			"mirror, which is the physical purpose of a one-way gate. PinMAME's sLGate and sRGate names are "
			"transposed relative to the printed table and to both retained scripts, so the address-to-side "
			"assignment here follows the manual and the proven scripts.",
			[
				("right-loop", "Right loop", ["switch.matrix-71", "switch.matrix-72"], "Right orbit, high then low."),
				("left-loop", "Left loop", ["switch.matrix-73", "switch.matrix-74"], "Left orbit, high then low."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Centre ramp diverter",
			"diverter",
			[output_id("Diverter Power"), output_id("Diverter Hold")],
			["switch.matrix-62", "switch.matrix-65", "switch.matrix-36"],
			"Ramp diverter assembly A-17241 with shaft and blade A-20556 sits at the top of the ramp system and "
			"selects where a centre-ramp shot is delivered. It rides the Fliptronic upper-left flipper circuit: "
			"public solenoid 35 is the power winding and 36 the hold winding, and pinned PinMAME reads both together "
			"as its sDiverter custom solenoid. With the blade at rest a centre-ramp shot entering at switch 62 "
			"continues to the right ramp exit at switch 65; with the diverter energized the same shot is delivered "
			"into the left popper at opto 36. The retained script drives the blade with SolDiv, which rotates the "
			"actuator and swaps which of the two ramp walls is dropped.",
			[
				("rest", "Diverter at rest", ["switch.matrix-65"], "Centre ramp feeds the right ramp exit."),
				("diverted", "Diverter energized", ["switch.matrix-36"], "Centre ramp feeds the left popper."),
			],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-17241",
		),
		alien("mechanism.alien-left-low", "Left low Martian alien", 5, [56, 57, 58], "at the left of the playfield", "A-20579-1"),
		alien("mechanism.alien-left-high", "Left high Martian alien", 6, [43], "above and inboard of the left target bank", "A-20579-2"),
		alien("mechanism.alien-right-high", "Right high Martian alien", 8, [44], "above and inboard of the right target bank", "A-20579-1"),
		alien("mechanism.alien-right-low", "Right low Martian alien", 14, [41, 42], "at the right of the playfield", "A-20579-1"),
		mechanism(
			"mechanism.jet-bumpers",
			"Three jet bumpers",
			"other",
			[output_id("Left Jet"), output_id("Bottom Jet"), output_id("Right Jet")],
			["switch.matrix-53", "switch.matrix-54", "switch.matrix-55"],
			"Three jet bumpers in the upper right of the playfield, each an A-9415-2 coil assembly with an "
			"A-12030-3 switch assembly, a B-9414-3 red wafer and a 03-9007-9 red cap. Wafer switches 53, 54 and 55 "
			"fire coils 11, 12 and 13 respectively; the printed names are Left Jet, Bottom Jet and Right Jet. "
			"Flasher 22 lights the whole nest and the jets sit inside general-illumination string 03.",
			[],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Two slingshots above the lower flippers. Each uses an A-17811 kicker assembly with an A-17801 kicker "
			"count switch assembly and a B-9362 coil bracket, left-handed B-9362-L-2 and right-handed B-9362-R-3. "
			"The printed parts list gives each position two switch part numbers, SW-1A-114 for the kicker leaf and "
			"SW-1A-120 for the score leaf, both reporting on the one public address.",
			[],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
			assembly_part_number="A-17811",
		),
		mechanism(
			"mechanism.flippers",
			"Two lower flippers",
			"other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Attack From Mars has exactly two flippers, both at the bottom. Each is an FL-11629 blue coil on "
			"assembly A-15849-R-2 or A-15849-L-2 with a power and a hold winding, driven from the Fliptronic board "
			"and numbered 29-32 in the manual but 45-48 by PinMAME. Cabinet button optos A-17316 report on F2 and "
			"F4 and SW-1A-194 end-of-stroke leaves on F1 and F3. The four upper Fliptronic switch positions F5-F8 "
			"are printed Not Used because there are no upper flippers, while the matching upper Fliptronic outputs "
			"drive the two loop gates and the ramp diverter instead.",
			[],
			MANUAL_SOURCE,
			VPX_SCRIPT_SOURCE,
			CORE_SOURCE,
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
		{
			"id": "relationship.drop-target-reset",
			"kind": "inverted",
			"source": output_id("Drop Target"),
			"destination": "switch.matrix-77",
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE),
		},
		{
			"id": "relationship.motor-bank-up",
			"kind": "direct",
			"source": output_id("Motor Bank Motor"),
			"destination": "switch.matrix-67",
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "relationship.motor-bank-down",
			"kind": "direct",
			"source": output_id("Motor Bank Motor"),
			"destination": "switch.matrix-66",
			"provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
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
			"id": "bally.attack-from-mars.1995",
			"name": "Attack From Mars",
			"manufacturer": "Bally",
			"year": 1995,
			"kind": "physical_pinball",
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
		"knowledge": {"path": "knowledge/bally/attack-from-mars-1995.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Attack From Mars device identifiers are not unique: {duplicates}")
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
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
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
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/attack-from-mars-1995/extraction-manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool 0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"manual_transcription_sha256": MANUAL_TRANSCRIPTION_SHA256,
			"rom_sha256": ROM_SHA256,
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
		"projections": (
			[
				{"group": "pinmame.input.switch", "address": address, "reason": reason}
				for address, reason in sorted(SWITCH_PROJECTIONS.items())
			]
			+ [
				{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
				for address, reason in sorted(SOLENOID_PROJECTIONS.items())
			]
			+ [
				{
					"group": "pinmame.output.lamp",
					"address": address,
					"reason": (
						"Projected onto the retained saucer primitive ufo1. The sixteen L.E.D.s of board A-20670 "
						"share one assembly and the retained table models no individual L.E.D. objects, so every "
						"address takes the saucer assembly anchor."
					),
				}
				for address in SAUCER_LED_ADDRESSES
			]
		),
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.attack-from-mars.1995/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/attack-from-mars-1995/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"pages": [{"path": path, "sha256": digest, "note": note} for path, digest, note in VISUAL_REVIEW_CACHE],
		},
		"excluded_object_classes": [
			"flw wall-glow quads on the left rail at pos_x -2.5, the right rail at pos_x 947.5, and the rear wall at pos_y 10, which are light spill projected onto the cabinet rather than bulb sockets",
			"BallShadow* render helpers stacked at one apron coordinate",
			"DivF invisible diverter actuator parked off the playfield",
			"sw36a, sw37a and swp45-swp47 popper-exit and target render primitives",
			"peg*, rpeg*, screw*, metal* and Primitive* decorative playfield hardware",
		],
		"unresolved": [
			{
				"scope": "pinmame.output.gi 2",
				"question": (
					"Whether the retained table's gi31, gi32 and gi33 bulb lights, which sit exactly at the three "
					"jet-bumper centres and are absent from the aGiTLights collection, are additional physical "
					"sockets on general-illumination string 03 or pure decoration."
				),
				"why_not_blocking": (
					"The manual itemizes no general-illumination string, so no printed count exists to contradict "
					"or confirm either reading. The definition therefore asserts no physical quantity for string "
					"03 and states that its fourteen placements are the emitters the string is observed to drive "
					"rather than a complete socket inventory. An author gets fourteen correct emitter positions "
					"plus an explicit note; nothing authoring-critical is presented as settled. The same class of "
					"unknown is already accepted in the promoted Williams Medieval Madness definition, whose "
					"insert-panel strings assert no bulb count at all."
				),
				"independent_review_dissent": (
					"The independent gpt-5.6-sol review of contribution HEAD 7faacbb held that this unknown "
					"should block promotion and that the machine ought to stay partial until the three bulbs are "
					"resolved. The maintainer decided to promote, on the grounds that every other dimension is "
					"complete and validated and that the identical class of unknown was already accepted for "
					"Medieval Madness. The dissent is recorded here rather than dropped so a later reviewer can "
					"revisit the call."
				),
			}
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Attack From Mars (Bally, 1995) spatial review",
		"",
		f"Status: {report['status']} and promoted to `machines/author-ready/bally/attack-from-mars-1995.json`.",
		"",
		"The matching source is the retained known-working `Attack from Mars 3.02.vpx` by JPSalas at SHA-256 "
		f"`{TABLE_SHA256}`. A fresh `vpxtool` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. `vpxtool` established "
		f"exact playfield bounds `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to "
		"at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded JPSalas script is the runtime address and causality authority; the Bally operators "
		"handbook is the physical inventory, quantity, polarity and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry; and the pinned LibPinMAME harness supplies "
		"runtime observation.",
		"- The retained manual PDF is an image-only scan. Every printed table used here was read from rendered "
		"pages and transcribed into "
		"`external:pinmame-review-artifacts/attack-from-mars-1995/manual-transcription.md`; no OCR text was "
		"treated as authority.",
		"- Flasher representation in the retained table needs care. Solenoids 20, 21, 22, 23 and 28 have an "
		"ordinary `Light` object at the bulb. Solenoids 17, 18, 19, 25, 26 and 27 do not: the author draws each "
		"as a raised `flare_red` glare quad sitting at the bulb position plus one or two `flw` wall-glow quads "
		"pinned to the left rail at `pos_x -2.5`, the right rail at `pos_x 947.5` or the rear wall at "
		"`pos_y 10`. For those six the flare origin is the only coordinate the table offers for the bulb and is "
		"used as the anchor, which the projection list records device by device. The wall glows are light spill "
		"projected onto the cabinet, never sockets, and are excluded from both placement and multiplicity.",
		"- Solenoid 19 Right Side High is the one flasher whose stored `pos_x`/`pos_y` is stale in the retained "
		"table, pointing at (71, 800) on the left. Its drag-point centroid, its own right-rail wall glow at the "
		"same y, the manual solenoid-location map and the fact that its printed assembly A-20549 is the right wire "
		"ramp all place it on the right, and the centroid is used.",
		"- GI strings 0-2 use the table's `aGiLLights`, `aGiMLights` and `aGiTLights` arrays. The table pairs each "
		"bulb with a co-located halo light, so those 50 light objects reduce to 29 distinct emitter positions. The "
		"manual prints no per-string bulb count, so strings 01 and 02 take their asserted physical quantity from "
		"those deduplicated arrays. String 03 asserts no quantity at all: three further bulb lights sit at the jet-"
		"bumper centres outside the modulated collection and the evidence does not settle whether they are "
		"additional sockets on that string, so its fourteen placements are the emitters the string is observed to "
		"drive rather than a claimed socket inventory. GI strings 3 and 4 are backbox insert-panel circuits and "
		"take a controlled `cabinet_or_service` record with no asserted count.",
		"- The sixteen saucer L.E.D.s at public lamp addresses 91-98 and 101-108 are not in the printed lamp "
		"matrix. They are shifted into board A-20670 by public solenoids 37 and 38, and the pinned harness "
		"observed every one of the sixteen lit across four attract phases, eight at a time, with solenoids 37, 38, "
		"41 and 42 active alongside them.",
		"- Solenoids 41, 42 and 43 are PinMAME's mirrors of auxiliary outputs 37, 38 and 39, and custom solenoids "
		"51, 52 and 53 are second views of 33, 34 and 35/36. All six are declared virtual with a `virtual` spatial "
		"record so no duplicate device is ever placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		group = entry["group"].rsplit(".", 1)[-1]
		lines.append(f"- {group.capitalize()} {entry['address']}: {entry['reason']}")
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
		"No authoring-critical placement, polarity, quantity, or semantic question remains unresolved, the "
		"definition carries no conflict records, and the deterministic curator reproduces the canonical artifact "
		"and its pinned seed byte-for-byte. Promotion to `author_ready` is therefore justified.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Candidate geometry `external:pinmame-review-artifacts/attack-from-mars-1995/vpx-spatial-candidates.json`.",
		"- Rendered manual pages `external:pinmame-manuals/rendered/bally.attack-from-mars.1995/`; the "
		f"{len(VISUAL_REVIEW_CACHE)} pages that decided a canonical value are listed with their SHA-256 in the "
		"companion JSON report, so an empty or substituted render cache is an audit failure rather than an "
		"assumed source.",
		f"- Human transcription of every printed table read from those pages, SHA-256 `{MANUAL_TRANSCRIPTION_SHA256}`.",
		"- Harness runs and DMD captures `external:pinmame-review-artifacts/attack-from-mars-1995/harness/`.",
		"",
	]
	return "\n".join(lines)


# The rest of the promoted bundle is hand-authored prose and machine-generated evidence rather than
# curator output, so it is pinned by content hash instead of regenerated. That keeps a stale knowledge
# note or a substituted evidence file an audit failure rather than an unnoticed drift.
KNOWLEDGE_RELATIVE_PATH = Path("knowledge/bally/attack-from-mars-1995.md")
KNOWLEDGE_SHA256 = "f35a3dee6a266072731f25b8c40ff014476ad7f5a5851160cb2281db4a753291"
EVIDENCE_RELATIVE_PATH = Path("evidence/runtime/wpc-95/attack-from-mars-boot-attract-and-ball-start.json")
EVIDENCE_SHA256 = "026ddd92e4eab3d44d76cf933c79d3f87c1c483c01d67af44796dab42047a883"


def verify_promoted_bundle(root: Path = ROOT) -> None:
	"""Refuse drift in the promoted artifacts the curator does not itself generate."""
	for relative, expected in (
		(KNOWLEDGE_RELATIVE_PATH, KNOWLEDGE_SHA256),
		(EVIDENCE_RELATIVE_PATH, EVIDENCE_SHA256),
	):
		path = root / relative
		if not path.is_file():
			raise RuntimeError(f"Attack From Mars promoted artifact is missing: {path}")
		actual = _file_sha256(path)
		if actual != expected:
			raise RuntimeError(
				f"Attack From Mars promoted artifact drifted from its pinned hash: {path} is {actual}, "
				f"expected {expected}"
			)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	partial = root / PARTIAL_PATH.relative_to(ROOT)
	if partial.exists():
		partial.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	partial_path = root / PARTIAL_PATH.relative_to(ROOT)
	if partial_path.exists():
		raise RuntimeError(f"Stale Attack From Mars partial definition is still present: {partial_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Attack From Mars definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Attack From Mars seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Attack From Mars definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Attack From Mars seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Attack From Mars spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Attack From Mars spatial review drifted from its deterministic curator: {markdown_path}")
	verify_promoted_bundle(root)
	print("Attack From Mars definition, seed, spatial audit, knowledge note, and evidence match the deterministic curator.")


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
		print(f"Attack From Mars extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Attack From Mars retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
