"""Curate the physical Bally Cirqus Voltaire (1997) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail,
and normalized coordinate as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/bally/cirqus-voltaire-1997.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/cirqus-voltaire-1997.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/cirqus-voltaire-1997.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/cirqus-voltaire-1997.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/cirqus-voltaire-1997.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.bally.cirqus-voltaire.1997"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.cirqus-voltaire.1997"
VPX_TABLE_SOURCE = "vpx-table.cv-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.cv-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.cv-vpw-1-0"

TABLE_SHA256 = "7aab0f175816f7bdee4114d5859cbfc70760aead8ef39ebf6481609b649207e5"
SCRIPT_SHA256 = "2abdca0fb8870c995314c52d5e3931530f6c850b1c8ac5f11176aca58b87bfa4"
MANUAL_SHA256 = "14cb9a4a225a7f5e6b9ea8b3f81b8626f3307cf299c4420d34612d42367a0eec"
SB101_SHA256 = "ebf2bf28d58b27f6f39203b05ffb3b5ca797bc8adf79e289c27e467e058ff0ac"
SB102_SHA256 = "d7721bdd95a741720cfd49904ebd53f43b6d6ca4ff827129692ad0b406c916bf"
SB104_SHA256 = "af63fd98cc858a756751fdac787b3e239d469fcc3cf7a1ecd6dd880ec9af8594"

EXTRACTION_RELATIVE_PATH = Path("bally/cirqus-voltaire-1997/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/cirqus-voltaire-1997/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "156520b390cbd3e9314d498ff3c6787e3511031093ca21597a82327d66d01660"
EXTRACTION_FILE_COUNT = 1522
EXTRACTION_TOTAL_BYTES = 297184998

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
TABLE_WIDTH = 964.0
TABLE_HEIGHT = 2162.0

DRIVER_IDS = ("cv_10", "cv_11", "cv_13", "cv_14", "cv_20h", "cv_20hc", "cv_d52")
DRIVER_COMPATIBILITY = {
	"cv_10": ("identical", "Bally production 1.0 game ROM, an early firmware revision of the same physical machine."),
	"cv_11": ("identical", "Bally 1.1 game ROM; a later firmware revision with no controller-address or playfield change."),
	"cv_13": ("identical", "Bally 1.3 game ROM; a later firmware revision with no controller-address or playfield change."),
	"cv_14": ("identical", "Bally 1.4 game ROM, the pinned catalog's clone-tree parent."),
	"cv_20h": (
		"identical",
		"Bally 2.0H \"Home\" ROM. This is the driver the retained known-working VPW table binds to "
		'(cGameName = "cv_20h"), a post-arcade-run home/free-play revision of the same physical machine '
		"with the identical switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware.",
	),
	"cv_20hc": ("identical", "Bally 2.0H \"Home, Coin Play\" ROM; the coin-mechanism-enabled sibling of cv_20h."),
	"cv_d52": ("identical", "Bally D.52 prototype game ROM for the same physical machine; pre-release firmware with no dumped sound ROMs."),
}

# --- Printed switch matrix (manual page 155/printed 2-49; excerpt switch-matrix.md).
SWITCH_LABELS = {
	11: "Backbox Luck", 12: "Wire Ramp Enter", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Loop Upper", 16: "Top Eddy", 17: "Right Inlane", 18: "Shooter Lane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Right Loop Upper", 24: "Always Closed",
	25: "Inner Loop Left", 26: "Left Inlane", 27: "Left Outlane", 28: "Inner Loop Right",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3",
	35: "Trough Ball 4", 36: "Popper Opto", 37: "\"WOW\" Targets", 38: "Top Targets",
	41: "Left Lane", 42: "Ringmaster Up", 43: "Ringmaster Middle", 44: "Ringmaster Down",
	45: "Left Ramp Made", 46: "Trough Upper", 47: "Trough Middle", 48: "Left Loop Enter",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Upper Jet Bumper", 54: "Middle Jet Bumper",
	55: "Lower Jet Bumper", 56: "Skill Shot", 57: "Right Outlane", 58: "Ring \"N\", \"G\"",
	61: "\"Light\" Standup Target", 62: "\"Lock\" Standup Target", 63: "Ramp Enter", 64: "Ramp Magnet",
	65: "Ramp Made", 66: "Ramp Lock Low", 67: "Ramp Lock Middle", 68: "Ramp Lock High",
	71: "Left Saucer", 72: "Right Saucer", 74: "Big Ball Rebound", 75: "\"Volt\" Right",
	76: "\"Volt\" Left",
}
# Printed matrix positions marked "Not Used" on both the switch-locations list and switch matrix.
UNUSED_MATRIX_ADDRESSES = {73, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# Every switch shaded "OPTO, TYPICALLY CLOSED" on the printed switch matrix (2-49): column 3 in
# full, all eight rows -- trough optos, popper opto, and the two target-bank optos.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 37, 38}
# PinMAME's cvGameData inverted-switch mask covers only these six (index 3 = 0x3f, bits 0-5 = rows
# 1-6); rows 7-8 (37, 38) are shaded on the printed matrix but the mask's bits 6-7 are clear. See
# conflict.wow-top-targets-opto-not-normalized.
PINMAME_NORMALIZED_OPTO_SWITCHES = {31, 32, 33, 34, 35, 36}
# vpmTimer.PulseSw / momentary-target callers in the retained VPW script.
PULSED_SWITCHES = {11, 31, 53, 54, 55, 74, 115, 117}

SWITCH_TYPES = {
	11: "other", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch",
	16: "other", 17: "other", 18: "microswitch", 21: "leaf", 22: "microswitch",
	23: "microswitch", 24: "other", 25: "microswitch", 26: "other", 27: "microswitch",
	28: "microswitch", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto",
	37: "opto", 38: "opto", 41: "other", 42: "other", 43: "other", 44: "other",
	45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "leaf", 52: "leaf", 53: "microswitch", 54: "leaf", 55: "microswitch",
	56: "other", 57: "microswitch", 58: "other", 61: "other", 62: "other",
	63: "microswitch", 64: "microswitch", 65: "microswitch", 66: "microswitch",
	67: "microswitch", 68: "microswitch", 71: "leaf", 72: "leaf",
	74: "other", 75: "other", 76: "other",
}

# address -> (assembly_part_number, part_number), transcribed verbatim from switch-locations.md.
SWITCH_PARTS = {
	11: (None, "5647-12693-19"), 12: (None, "5647-12693-13"), 13: ("20-9663-16", None),
	14: (None, "04-10346"), 15: ("A-17813", "5647-12693-19"), 16: ("A-20036", None),
	17: ("A-18008-1", "A-16443"), 18: (None, "5647-12693-68"), 21: ("A-17238", None),
	22: (None, "5643-09268-00"), 23: ("A-17813-1", "5647-12693-19"), 24: (None, "5643-15190-00"),
	25: ("A-17813", "5647-12693-19"), 26: ("A-18008-1", "A-16443"), 27: ("A-17813-1", "5647-12693-19"),
	28: ("A-17813-1", "5647-12693-19"),
	31: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	32: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	33: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	34: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	35: ("A-18617-1 LED with A-18618-1 photo transistor", None),
	36: ("A-16908 LED with A-16909 photo transistor", None),
	37: ("A-21960-6", None), 38: ("A-18530-6", None),
	42: (None, "5647-12693-01"), 43: (None, "5647-12693-01"), 44: (None, "5647-12693-01"),
	45: (None, "5647-12693-21"), 46: (None, "5647-12693-13"), 47: (None, "5647-12693-13"),
	48: ("A-17813-1", "5647-12693-19"),
	53: ("B-12030-2", "A-16443"), 54: (None, "SW-1A-213"), 55: ("B-12030-2", "A-16443"),
	56: ("A-20846-9", None), 57: ("A-17813", None), 58: ("A-20846-9", "5647-12693-19"),
	61: ("A-18530-6", None), 62: ("A-18530-6", None),
	63: (None, "20-10293"), 64: (None, "5647-12693-13"), 65: (None, "5647-12693-13"),
	66: (None, "5647-12693-66"), 67: (None, "5647-12693-66"), 68: (None, "5647-12693-66"),
	74: ("A-17794", "A-17793"), 75: ("A-18008-1", "A-16443"), 76: ("A-18008-1", "A-16443"),
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
# Fliptronic F1-F8 wiring, printed switch matrix page.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed solenoid/flasher table (manual page 156, printed 2-50; excerpt solenoid-flasher-table.md).
SOLENOID_LABELS = {
	1: "Plunger", 2: "Backbox Kick", 3: "Left Loop Magnet", 4: "Middle Jet Bumper",
	5: "Ramp Magnet", 6: "Diverter Power", 7: "Jet Up", 8: "Jet Release", 9: "Trough Eject",
	10: "Left Slingshot", 11: "Right Slingshot", 12: "Upper Jet Bumper", 13: "Lower Jet Bumper",
	14: "Left Saucer", 15: "Right Saucer", 16: "Lock Post",
	17: "Join Flashers", 18: "Ring #1 Flashers", 19: "Ring #2 Flashers", 20: "Ring #3 Flashers",
	21: "Right Playfield Flasher", 22: "Motor Enable", 23: "Jet Flasher", 24: "Left Playfield Flasher",
	25: "Upper Left Flasher", 26: "Up. Right Playfield Flasher", 27: "Ringmaster Flashers",
	28: "Bear Playfield Flasher",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	33: "Popper", 34: "Diverter Hold", 35: "Ringmaster Magnet", 36: "Upper Post",
	37: "Neon", 39: "Motor Direction", 40: "Eddy Board",
}
NOT_FITTED_SOLENOID_LABELS = {38: "Not Used Motor Circuit Position 38"}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	41: "Motor Direction LPDC Mirror",
	42: "Unused WPC-95 LPDC Mirror 42",
	43: "Unused WPC-95 LPDC Mirror 43",
	44: "Unused WPC-95 LPDC Mirror 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
	51: "PinMAME Decaying Fire State for Solenoid 35",
	52: "PinMAME Decaying Fire State for Solenoid 36",
}
# Manual printed items that differ from the PinMAME public address (lower-flipper power/hold pairs).
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32"}

SOLENOID_WIRING = {
	1: dict(control_connection="J116-1", driver_transistor="Q72", power_connection="J133-2", part_number="AE-23-800", printed_type="High Power"),
	2: dict(control_connection="J118-2", driver_transistor="Q68", power_connection="J134-3", part_number="AE-23-800", printed_type="High Power"),
	3: dict(control_connection="J116-4", driver_transistor="Q71", power_connection="J133-2", part_number="20-10197", printed_type="High Power"),
	4: dict(control_connection="J116-5", driver_transistor="Q67", power_connection="J133-2", part_number="AE-23-800", printed_type="High Power"),
	5: dict(control_connection="J116-6", driver_transistor="Q70", power_connection="J133-2", part_number="20-10197", printed_type="High Power"),
	6: dict(control_connection="J116-7", driver_transistor="Q66", power_connection="J133-2", part_number="FL-11753", printed_type="High Power"),
	7: dict(control_connection="J116-8", driver_transistor="Q69", power_connection="J133-2", part_number="FL-11630", printed_type="High Power"),
	8: dict(control_connection="J116-9", driver_transistor="Q65", power_connection="J133-2", part_number="SM1-26-600", printed_type="High Power"),
	9: dict(control_connection="J114-1", driver_transistor="Q44", power_connection="J133-3", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(control_connection="J114-3", driver_transistor="Q48", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(control_connection="J114-4", driver_transistor="Q43", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(control_connection="J114-5", driver_transistor="Q47", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(control_connection="J114-6", driver_transistor="Q42", power_connection="J133-3", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(control_connection="J114-7", driver_transistor="Q46", power_connection="J133-3", part_number="AE-27-1200", printed_type="Low Power"),
	15: dict(control_connection="J114-8", driver_transistor="Q41", power_connection="J133-3", part_number="AE-27-1200", printed_type="Low Power"),
	16: dict(control_connection="J114-9", driver_transistor="Q45", power_connection="J133-3", part_number="AE-26-1500", printed_type="Low Power"),
	17: dict(control_connection="J111-1", driver_transistor="Q28", power_connection="J133-6", printed_type="Flasher"),
	18: dict(control_connection="J111-2", driver_transistor="Q32", power_connection="J133-6", printed_type="Flasher"),
	19: dict(control_connection="J111-3", driver_transistor="Q27", power_connection="J133-6", printed_type="Flasher"),
	20: dict(control_connection="J111-4", driver_transistor="Q31", power_connection="J133-6", printed_type="Flasher"),
	21: dict(control_connection="J111-5", driver_transistor="Q26", power_connection="J133-6", printed_type="Flasher"),
	22: dict(control_connection="J111-6", driver_transistor="Q30", power_connection="J133-6", part_number="A-15680", printed_type="Flasher"),
	23: dict(control_connection="J111-7", driver_transistor="Q25", power_connection="J133-6", printed_type="Flasher"),
	24: dict(control_connection="J111-8", driver_transistor="Q29", power_connection="J133-6", printed_type="Flasher"),
	25: dict(control_connection="J109-1", driver_transistor="Q16", power_connection="J133-6", printed_type="Gen. Purpose"),
	26: dict(control_connection="J109-2", driver_transistor="Q15", power_connection="J133-6", printed_type="Gen. Purpose"),
	27: dict(control_connection="J109-3", driver_transistor="Q14", power_connection="J133-6", printed_type="Gen. Purpose"),
	28: dict(control_connection="J109-4", driver_transistor="Q13", power_connection="J133-6", printed_type="Gen. Purpose"),
	33: dict(control_connection="J120-6", driver_transistor="Q84", power_connection="J119-6", part_number="AL-25-1000", printed_type="Fliptronic power"),
	34: dict(control_connection="J120-4", driver_transistor="Q86", power_connection="J119-6", part_number="FL-11730", printed_type="Fliptronic hold"),
	35: dict(control_connection="J120-3", driver_transistor="Q81", power_connection="J119-8", part_number="20-10197", printed_type="Fliptronic power"),
	36: dict(control_connection="J120-1", driver_transistor="Q83", power_connection="J119-8", part_number="AE-27-1200", printed_type="Fliptronic hold"),
	37: dict(control_connection="J110-1", driver_transistor="U3A and U3B", power_connection="J139-2", part_number="A-21577", printed_type="Low Power motor"),
	39: dict(control_connection="J110-4", driver_transistor="U3G and U3H", power_connection="J133-6", part_number="A-15680", printed_type="Low Power motor"),
	40: dict(control_connection="J110-5", driver_transistor="U3E and U3F", power_connection="J139-2", part_number="A-22151-2", printed_type="Low Power motor"),
	45: dict(control_connection="J120-13", driver_transistor="Q90", power_connection="J119-1", part_number="FL-11630", printed_type="Fliptronic power"),
	46: dict(control_connection="J120-11", driver_transistor="Q92", power_connection="J119-1", part_number="FL-11630", printed_type="Fliptronic hold"),
	47: dict(control_connection="J120-9", driver_transistor="Q87", power_connection="J119-4", part_number="FL-11630", printed_type="Fliptronic power"),
	48: dict(control_connection="J120-7", driver_transistor="Q89", power_connection="J119-4", part_number="FL-11630", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "YEL-GRN", 46: "ORG-GRN", 47: "YEL-BLU", 48: "ORG-BLU", 33: "YEL-VIO", 34: "ORG-VIO", 35: "YEL-GRY", 36: "ORG-GRY"}

SOLENOID_ASSEMBLIES = {
	1: "A-21022", 2: "B-11873", 4: "A-21564", 5: "A-21959", 6: "A-22035", 7: "A-21564", 8: "A-21564",
	9: "A-19963-1", 10: "A-21527", 11: "A-21527", 12: "A-9415-2", 13: "A-9415-2", 14: "A-21829",
	15: "A-21829", 16: "A-21825", 22: "A-21953", 33: "A-21824", 34: "A-22035", 35: "A-21953",
	36: "A-17932", 37: "A-21577", 39: "A-21953", 45: "A-14876-R", 46: "A-14876-R",
	47: "A-15849-L", 48: "A-15849-L",
}
# Retained VPW script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "AutoPlunger (Plunger1.Fire)", 2: "BackBoxKick (Plunger2.Fire, backbox wheel/bell sequence)",
	9: "SolRelease (vpmTimer.PulseSw 31, bsTrough.ExitSol_On)",
	14: "LeftSaucer.SolOut", 15: "RightSaucer.SolOut", 16: "LockPost (vlLock.SolExit)",
	17: "Flash117", 18: "Flash118", 19: "Flash119", 20: "Flash120", 21: "Flash121",
	22: "MotorEnable (motor sound only)", 23: "Flash123", 24: "Flash124", 25: "Flash125",
	26: "Flash126", 27: "Flash127", 28: "Flash128",
	33: "SolPopper (Popper.ExitSol_On)", 34: "DiverterHold (diverter.RotateToEnd/Start)",
	35: "SolRingmasterMagnet", 36: "UpperPost (UpperPostWall.IsDropped)",
	37: "Flash137 (Neon)",
	46: "SolRFlipper (core.vbs sLRFlipper = 46)", 48: "SolLFlipper (core.vbs sLLFlipper = 48)",
	3: "LoopMagnet.Solenoid = 3 (cvpmMagnet class, no SolCallback line)",
	5: "LockMagnet.Solenoid = 5 (cvpmMagnet class, no SolCallback line)",
	22: "MotorEnable / mechRM.Sol1 = 22 (cvpmMech class)",
	39: "mechRM.Sol2 = 39 (cvpmMech class)",
}

FLASHER_BULBS = {
	17: ("#906 on the playfield and #906 on the insert panel", 2, 1),
	18: ("#906 on the playfield only", 1, 1),
	19: ("#906 on the playfield only", 1, 1),
	20: ("#906 on the playfield only", 1, 1),
	21: ("#906 on the playfield and #906 on the backbox insert panel", 2, 1),
	23: ("#906 on the playfield only", 1, 1),
	24: ("#906 on the playfield and #906 on the backbox insert panel", 2, 1),
	25: ("#906 on the playfield only", 1, 1),
	26: ("#906 on the playfield and #906 on the backbox insert panel", 2, 1),
	27: ("#906 (2) on the playfield", 2, 2),
	28: ("#906 on the playfield and #906 on the backbox insert panel", 2, 1),
}

# --- Printed lamp matrix (manual page 154, printed 2-48; excerpt lamp-matrix.md).
LAMP_LABELS = {
	11: "Cirqus \"R\"", 12: "Grid Top", 13: "Cirqus \"Q\"", 14: "Cirqus \"U\"",
	15: "Grid Top/Right", 16: "Cirqus \"S\"", 17: "Grid Middle/Right", 18: "Left Jackpot",
	21: "Cirqus \"I\"", 22: "Cirqus \"C\"", 23: "Grid Middle/Left", 24: "Grid Bottom/Left",
	25: "Grid Bottom", 26: "Grid Middle", 27: "Grid Bottom/Right", 28: "Grid Top/Left",
	31: "Side Show", 32: "Left Loop Top", 33: "Left Loop 3", 34: "Left Loop 2",
	35: "Left Loop 1", 36: "Multiball", 37: "Lock", 38: "Spot Marvel",
	41: "Ringmaster Left", 42: "Ringmaster 2", 43: "Ringmaster 3", 44: "Ringmaster 4",
	45: "Ringmaster Right", 46: "Special", 47: "Razz", 48: "Frenzy",
	51: "Crank Top", 52: "Crank 2", 53: "Crank 3", 54: "Crank Bottom",
	55: "Right Loop Top", 56: "Right Loop 3", 57: "Right Loop 2", 58: "Right Loop 1",
	61: "Middle Jackpot", 62: "Right Jackpot", 63: "Light Standup Target", 64: "Lock Standup Target",
	65: "Ring \"R\"", 66: "Ring \"I\"", 67: "Shoot Again", 68: "Left Outlane",
	71: "Wow Right \"W\" Target", 72: "Wow \"O\" Target", 73: "Wow Left \"W\" Target",
	74: "Ring \"N\"", 75: "Ring \"G\"", 76: "Right Outlane", 77: "Left In-Lane", 78: "Skill Ring",
	81: "Extra Ball", 82: "Top Jet Bumper", 83: "Middle Jet Bumper", 84: "Lower Jet Bumper",
	85: "Right In-Lane", 86: "Volt Left", 87: "Volt Right", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: ("A-21809", "#555"), 12: ("A-21809", "#555"), 13: ("A-21809", "#555"), 14: ("A-21809", "#555"),
	15: ("A-21809", "#555"), 16: ("A-21809", "#555"), 17: ("A-21809", "#555"), 18: ("A-17807", "#44"),
	21: ("A-21809", "#555"), 22: ("A-21809", "#555"), 23: ("A-21809", "#555"), 24: ("A-21809", "#555"),
	25: ("A-21809", "#555"), 26: ("A-21809", "#555"), 27: ("A-21809", "#555"), 28: ("A-21809", "#555"),
	31: ("A-21818", "#555"), 32: ("A-21818", "#555"), 33: ("A-21818", "#555"), 34: ("A-21818", "#555"),
	35: ("A-21818", "#555"), 36: ("A-21290", "#555"), 37: ("A-21290", "#555"), 38: ("A-21290", "#555"),
	41: ("A-20890", "#555"), 42: ("A-20890", "#555"), 43: ("A-20890", "#555"), 44: ("A-20890", "#555"),
	45: ("A-20890", "#555"), 46: ("A-21290", "#555"), 47: ("A-21290", "#555"), 48: ("A-21290", "#555"),
	51: ("A-21813", "#555"), 52: ("A-21813", "#555"), 53: ("A-21813", "#555"), 54: ("A-21813", "#555"),
	55: ("A-21813", "#555"), 56: ("A-21813", "#555"), 57: ("A-21813", "#555"), 58: ("A-21813", "#555"),
	61: ("A-17807", "#44"), 62: ("A-17807", "#44"), 63: ("A-17807", "#44"), 64: ("A-17807", "#44"),
	65: ("A-17835", "#44"), 66: ("A-17835", "#44"), 67: ("A-17807", "#44"), 68: ("A-17835", "#44"),
	71: ("A-21808", "#555"), 72: ("A-21808", "#555"), 73: ("A-21808", "#555"),
	74: ("A-17835", "#44"), 75: ("A-17835", "#44"), 76: ("A-17835", "#44"), 77: ("A-17807", "#44"),
	78: ("A-17807", "#44"), 81: ("A-17807", "#44"), 82: ("A-21554", "#555"), 83: ("A-21554", "#555"),
	84: (None, "#44"), 85: ("A-17807", "#44"), 86: ("A-17807", "#44"), 87: ("A-17807", "#44"),
	88: ("20-9663-16", None),
}
# Two co-located Light objects stacked purely for brightness (l##/l##b style pairs); the primary
# object is used and the duplicate is documented render doubling.
LAMP_RENDER_DOUBLES = set(range(11, 19)) | set(range(21, 29)) | set(range(31, 39)) | \
	set(range(41, 49)) | set(range(51, 59)) | set(range(61, 69)) | set(range(71, 78)) | \
	set(range(81, 88))

GI_STRINGS = {
	0: ("Playfield Right", "J105-1", "Q5", "J105-7", "#44"),
	1: ("Playfield Middle", "J105-2", "Q4", "J105-8", "#44"),
	2: ("Playfield Left", "J105-3", "Q3", "J105-9", "#44"),
	3: ("Backbox 2", "J106-5", "Q2", "J106-10", "#555"),
	4: ("Backbox 1", "J106-6 and J104-3", "Q1", "J106-11 and J104-1", "#555"),
}

# --- Normalized playfield coordinates derived from the retained VPWmod v1.0 extraction
# (x/964, y/2162; vpx-geometry.txt in the review artifacts).
SWITCH_POSITIONS = {
	12: [(0.564021, 0.098164)], 15: [(0.238185, 0.021515)], 16: [(0.619582, 0.307607)],
	17: [(0.762342, 0.755774)], 18: [(0.939823, 0.894084)], 23: [(0.747359, 0.013202)],
	25: [(0.521248, 0.162843)], 26: [(0.147113, 0.754619)], 27: [(0.057155, 0.770779)],
	28: [(0.83565, 0.192079)],
	31: [(0.86355, 0.87162)], 32: [(0.86355, 0.87162)], 33: [(0.86355, 0.87162)],
	34: [(0.86355, 0.87162)], 35: [(0.86355, 0.87162)],
	36: [(0.905118, 0.403491)],
	37: [(0.601181, 0.174182), (0.677953, 0.172111), (0.746256, 0.186486)],
	38: [(0.518211, 0.274752), (0.743706, 0.304476)],
	41: [(0.070735, 0.464461)], 42: [(0.645703, 0.25084)], 43: [(0.646697, 0.251088)],
	44: [(0.645703, 0.25084)],
	45: [(0.105604, 0.363037)], 46: [(0.75331, 0.124248)], 47: [(0.737409, 0.336614)],
	48: [(0.062477, 0.107855)],
	56: [(0.379969, 0.32457)], 57: [(0.851956, 0.770779)], 58: [(0.768859, 0.622889)],
	61: [(0.231825, 0.422018)], 62: [(0.359188, 0.39834)],
	63: [(0.258943, 0.353034)], 64: [(0.735329, 0.110577)], 65: [(0.904528, 0.268494)],
	66: [(0.341253, 0.33464)], 67: [(0.341859, 0.310043)], 68: [(0.352548, 0.286127)],
	71: [(0.176216, 0.172499)], 72: [(0.299934, 0.138666)],
	75: [(0.671677, 0.409987)], 76: [(0.485489, 0.448247)],
}
SWITCH_PROJECTIONS = {
	31: "Projected onto the ball-release kicker (BallRelease, table object center): the retained script's cvpmBallStack class (bsTrough) tracks trough switches 31-35 from internal ball-count state rather than five separate playfield trigger objects, and BallRelease is the trough's own exit kicker.",
	32: "Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.",
	33: "Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.",
	34: "Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.",
	35: "Projected onto the ball-release kicker (BallRelease, table object center); see switch 31.",
	42: "Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center): the retained script's cvpmMech class (mechRM) reads switches 42/43/44 from a single 0-118 motor-position counter (AddSw 44,0,1 / AddSw 43,88,89 / AddSw 42,117,118), not three separate playfield sensor objects.",
	43: "Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center); see switch 42.",
	44: "Projected onto the rotating/rising Ringmaster figure (Primitive Ringmaster, table object center); see switch 42.",
}

SOLENOID_POSITIONS = {
	1: [(0.93962, 0.982168)], 3: [(0.128644, 0.0479)], 4: [(0.672565, 0.520006)],
	5: [(0.888035, 0.122114)],
	6: [(1.0, 0.140435)], 7: [(1.0, 0.530928)], 8: [(1.0, 0.530928)],
	9: [(0.86355, 0.87162)], 10: [(0.235632, 0.727262)], 11: [(0.674285, 0.726706)],
	12: [(0.912931, 0.491617)], 13: [(0.834583, 0.601722)],
	14: [(0.176216, 0.172499)], 15: [(0.299934, 0.138666)], 16: [(0.345415, 0.349834)],
	17: [(0.457851, 0.587504)], 18: [(0.378923, 0.790764)], 19: [(0.678564, 0.601894)],
	20: [(0.454313, 0.38938)], 21: [(0.965631, 0.332974)], 22: [(0.645703, 0.25084)],
	23: [(0.672001, 0.520404)], 24: [(0.062584, 0.415905)], 25: [(0.060641, 0.021317)],
	26: [(0.777544, 0.08932)], 27: [(0.533514, 0.2579)], 28: [(0.106665, 0.506626)],
	33: [(0.915682, 0.40701)], 34: [(1.0, 0.140435)], 35: [(0.646697, 0.251088)], 36: [(0.535892, 0.019241)],
	37: [(1.0, 0.657313)], 39: [(0.645703, 0.25084)],
	45: [(0.619971, 0.844358)], 46: [(0.619971, 0.844358)],
	47: [(0.291079, 0.844369)], 48: [(0.291079, 0.844369)],
}
# Objects placed at/near normalized x=1.0 whose raw geometry sits just past the retained table's own
# declared right edge; clamped to the schema-valid boundary with the raw overshoot disclosed here
# rather than fabricating a different coordinate (matching the precedent already established for
# Williams Monster Bash's GIbot light11 exclusion and Bally The Addams Family's y-clamp).
CLAMPED_X_RAW = {
	6: 1.062556, 7: 1.067884, 8: 1.067884, 34: 1.062556, 37: 1.080000,
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Cirqus Voltaire retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Cirqus Voltaire extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Cirqus Voltaire retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Cirqus Voltaire retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Cirqus Voltaire retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the cv_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/cv.c cvGameData GEN_WPC95 with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x00,0x00,0x3f,0x00,...}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), swStart/swTilt/swSlamTilt/"
				"swCoinDoor/swTicket defines, hw.custSol=2 (CORE_CUSTSOLNO(1)=51, CORE_CUSTSOLNO(2)=52, a decaying "
				"fire-state counter for solenoids 35/36 read back by the driver's own preliminary getSol handler), "
				"cv_ringMech mechanism table (MECH_LINEAR|MECH_REVERSE|MECH_ONEDIRSOL, sol1=22, sol2=43, switches "
				"42/43/44), and init_cv's wpc_set_fastflip_addr(0x80); src/wpc/core.h WPC solenoid numbering, "
				"CORE_FIRSTLFLIPSOL=45, CORE_FIRSTUFLIPSOL=33, CORE_FIRSTCUSTSOL=51; src/wpc/core.c core_getSol "
				"WPC95 37..40 to 41..44 duplication (solNo 41-44 read back at solNo-4, so public 43 mirrors public "
				"39); src/wpc/wpc.c WPC_FLIPPERSW95 inversion; src/libpinmame/libpinmame.h "
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
			"locator": "WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.cirqus-voltaire.1997/ipdb/Bally_1997_Cirqus_Voltaire_Manual.pdf",
			"original_filename": "Bally_1997_Cirqus_Voltaire_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"194-page Bally Cirqus Voltaire operations manual. Printed pages 2-42 through 2-50 carry the "
				"lamp/switch/solenoid location parts lists and their matrix and combined solenoid/flasher/GI/"
				"flipper/motor wiring tables; the parts lists (2-10 through 2-16 and similar) name assemblies that "
				"fix device construction (trough opto boards, popper opto, eddy-current sensor boards, ball "
				"guides). Service Bulletins 101, 102, and 104 (separate PDFs) record post-production field fixes "
				"for the disappearing jet bumper, an upgrade kit, and an adjustment sheet."
			),
			"license": "NOASSERTION",
			"attribution": "Bally/Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.cirqus-voltaire.switch-matrix",
					"locator": "PDF page 155, printed page 2-49, SWITCH MATRIX table",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/switch-matrix.md",
					"sha256": "e5c95baf8f6ce2b62b9eb7de76a3af12406e14bf245c0e2406f89b8f7f242dfd",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/switch-matrix.webp",
					"image_sha256": "ed5bba5c151d579d1f145a3d9815f1bcdb837443844001d406e88362bf9c1664",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 155, crop box 0.06,0.05,0.99,0.60 of the page, rendered at 300 dpi with pdftoppm, reduced to 780px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.switch-locations",
					"locator": "PDF pages 150-151, printed pages 2-44/2-45, Switch Locations parts list",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/switch-locations.md",
					"sha256": "8ddd10a3b60eedffbf5885b043cd312890726349cd44a2a1af37524706dba3ef",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/switch-locations.webp",
					"image_sha256": "67621a3706cb91a16ba0818c8bcff4f8d9dd2f2d7116b1d6d16f69e9e3eafb3f",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 150, crop box 0.03,0.03,0.97,0.98, scanned page rendered at its native resolution (embedded image xref 627, 4950px across 8.25in), rendered at 335 dpi, capped to 2600px wide, 2601x3718 WebP quality 80; the parts list table (items F1-73) is complete on this page, with only items 74-88 continuing onto page 151 alongside an unrelated full-page playfield location diagram, so this crops page 150 where the table itself is",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.lamp-matrix",
					"locator": "PDF page 154, printed page 2-48, LAMP MATRIX table",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/lamp-matrix.md",
					"sha256": "01ebb38fa7828aecde224135d7c2aff9709c5bf8d45734499ef2cc346269316d",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/lamp-matrix.webp",
					"image_sha256": "87c0a472837b4dd34d9957011331748e605e4581e0ec384d3b53d25b9a07e6d4",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 154, crop box 0.05,0.03,0.98,0.52, scanned page rendered at its native resolution (embedded image xref 647, 4963px across 8.27in), rendered at 130 dpi, capped to 1000px wide, 1001x746 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.lamp-locations",
					"locator": "PDF page 148, printed page 2-42, Lamp Locations parts list",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/lamp-locations.md",
					"sha256": "a73a59ccfa470cb99086b002ffc9fb5fee8a6727328cbf783a0ec46bf7f9f3ad",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/lamp-locations.webp",
					"image_sha256": "401f9154603d7487318622d04cd60ce70ec6f71f430e1da5a28f647651f4ed0f",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 148, crop box 0.03,0.03,0.98,0.93, scanned page rendered at its native resolution (embedded image xref 619, 4950px across 8.25in), rendered at 332 dpi, capped to 2600px wide, 2601x3485 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.solenoid-flasher-table",
					"locator": "PDF page 156, printed page 2-50, combined Solenoid/Flasher/G.I./Flipper Circuits/Motor Circuit table",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/solenoid-flasher-table.md",
					"sha256": "7be25313455dd16750ed3bc41b07d51d6d4b5397ff001510e588b45f6c3aa3e8",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/solenoid-flasher-table.webp",
					"image_sha256": "35c564a0421a265378daad7fd3124bcc5a75ac195d20e69bd3cca95463aea596",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 156, crop box 0.03,0.02,0.985,0.71, scanned page rendered at its native resolution (embedded image xref 655, 4950px across 8.25in), rendered at 76 dpi, capped to 600px wide, 601x614 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.solenoid-flashlamp-locations",
					"locator": "PDF page 152, printed page 2-46, Solenoid/Flashlamp Locations parts list",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/solenoid-flashlamp-locations.md",
					"sha256": "bbd412e37d8f6d3f75a459ec1686a3ac596320f17c33f02e64c5ff8d224c0ad4",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/solenoid-flashlamp-locations.webp",
					"image_sha256": "7e4725a870d4d452bc528296362af2433e61fb0d6b9959287e2707d40851cd9e",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 152, crop box 0.03,0.02,0.985,0.83, scanned page rendered at its native resolution (embedded image xref 637, 4991px across 8.32in), rendered at 330 dpi, capped to 2600px wide, 2601x3120 WebP quality 80",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.cirqus-voltaire.general-illumination",
					"locator": "PDF page 156, printed page 2-50, General Illumination block (see solenoid-flasher-table.md)",
					"path": "evidence/excerpts/bally.cirqus-voltaire.1997/general-illumination.md",
					"sha256": "3dcdfbb4ea379918c836440b8bf729d65881c4f059c75eff2463c9be8d3d50b4",
					"image": "evidence/excerpts/bally.cirqus-voltaire.1997/general-illumination.webp",
					"image_sha256": "2a67d7f5f47ff4eac6e2348186e80af5fa116141eb7c22f8a449e18987ed1e7b",
					"image_derivation": "Bally_1997_Cirqus_Voltaire_Manual.pdf page 156, crop box 0.03,0.412,0.985,0.49, scanned page rendered at its native resolution (embedded image xref 655, 4950px across 8.25in), rendered at 330 dpi, capped to 2600px wide, 2601x302 WebP quality 80; a tight crop of only the General Illumination sub-block near the bottom of page 156, distinct from and excluding the Solenoid/Flasher rows above and the Flipper Circuits/Motor Circuit rows below that excerpt.cirqus-voltaire.solenoid-flasher-table crops from the same page",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/cirqus-voltaire/manual-transcription.md",
			"revision": "2026-08-07",
			"locator": (
				"Retained human transcription summary of every rendered manual table used by this definition, "
				"together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/bally.cirqus-voltaire.1997/ and the three retained Service "
				"Bulletin PDFs (SB101 disappearing-jet-bumper fix, SB102 upgrade kit, SB104 adjustment sheet)."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": "manual.bally.cirqus-voltaire.1997.service-bulletin-101",
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.cirqus-voltaire.1997/ipdb/Bally_1997_Cirqus_Voltaire_Service_Bulletin_101.pdf",
			"original_filename": "Bally_1997_Cirqus_Voltaire_Service_Bulletin_101.pdf",
			"sha256": SB101_SHA256,
			"locator": "Service Bulletin SB101 (1997-12-09): disappearing jet bumper release-latch and coil-frame-bending field fix for the first 200 samples.",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
		},
		{
			"id": "manual.bally.cirqus-voltaire.1997.service-bulletin-102",
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.cirqus-voltaire.1997/ipdb/Bally_1997_Cirqus_Voltaire_Service_Bulletin_102.pdf",
			"original_filename": "Bally_1997_Cirqus_Voltaire_Service_Bulletin_102.pdf",
			"sha256": SB102_SHA256,
			"locator": "Service Bulletin SB102 (1997-12-09): upgrade kit A-22270 (display panel bracket, Ringmaster cam lubrication, ramp switch-tension post, neon ramp switch bracket).",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
		},
		{
			"id": "manual.bally.cirqus-voltaire.1997.service-bulletin-104",
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.cirqus-voltaire.1997/ipdb/Bally_1997_Cirqus_Voltaire_Service_Bulletin_104.pdf",
			"original_filename": "Bally_1997_Cirqus_Voltaire_Service_Bulletin_104.pdf",
			"sha256": SB104_SHA256,
			"locator": "Service Bulletin SB104 (1998-04-02): adjustment sheet covering ball traps near the display, the left wire ramp switch, and the three center lock switch pivots (p/n 5647-12693-66).",
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/cirqus-voltaire-1997/source/Cirqus%20Voltaire%20%28Bally%201997%29%20VPW%20Mod%20v1.0.vpx",
			"original_filename": "Cirqus Voltaire (Bally 1997) VPW Mod v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPW Mod v1.0 recreation of the physical machine. Exact playfield bounds "
				f"are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for "
				"named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/cirqus-voltaire-1997/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (148,250 bytes). Runtime and mechanism-causality authority: '
				'cGameName = "cv_20h", Const UseSolenoids = 2, the SolCallback/SolModCallback table for solenoids '
				"1-2, 7-9, 14-28, 33-36 plus core.vbs sLRFlipper/sLLFlipper, the cvpmMech class configuring the "
				"Ringmaster motor (Sol1=22, Sol2=39, AddSw 42/43/44), the cvpmMagnet class instances for the Left "
				"Loop Magnet (Solenoid=3), Ramp/Lock Magnet (Solenoid=5), and Ringmaster Magnet (SolRingmasterMagnet "
				"callback for solenoid 35), the cvpmVLock class for the three-position ramp lock (switches 66/67/68, "
				"solenoid 16), the cvpmBallStack classes for the trough (switches 31-35, solenoid 9) and popper "
				"(switch 36, solenoid 33), and UpdateGI mapping GI 0/1/2 to the Gi_Pf_Right_01/Gi_Pf_Middle_02/"
				"Gi_Pf_Left_03 playfield emitter collections."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/cirqus-voltaire-1997/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 under "
				f"extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, "
				f"{EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool from the retained table. Bounds are "
				f"{TABLE_BOUNDS}."
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
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			if address in OPTO_SWITCHES:
				if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
					notes += (
						" Printed as an opto that is typically closed; PinMAME's cvGameData inverted-switch mask "
						"(mask index 3 = 0x3f, rows 1-6) covers it, so the public switch state is already "
						"normalized and must not be inverted again."
					)
				else:
					notes += (
						" Printed on the same shaded 'OPTO, TYPICALLY CLOSED' column as 31-36 (assembly A-21960-6 "
						"for the WOW target bank, A-18530-6 for the top target bank), but PinMAME's cvGameData "
						"inverted-switch mask covers only rows 1-6 of this column (mask index 3 = 0x3f); rows 7-8 "
						"(this address) are not covered, so the public switch state is not normalized by the "
						"emulator even though the printed hardware is normally closed; see "
						"conflict.wow-top-targets-opto-not-normalized."
					)
			if address == 24:
				notes += " Physical part 5643-15190-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 16:
				notes += (
					" A-20036 \"Magic Eddy Coil PCB Assembly\" mounted near the Ringmaster mechanism; the retained "
					"script only enables this switch's playfield collision while the Ringmaster mechanism is out "
					"of its home position (sw16.enabled = RMCurrPos > 4 and RMCurrPos < 100 in Sub UpdateRM)."
				)
			if address in {17, 26, 75, 76}:
				notes += (
					" A-18008-1 eddy-current proximity sensor construction (part A-16443, the same construction "
					"as switches 75/76/17/26), not an optical opto interrupter; PinMAME's inverted-switch mask "
					"does not cover it, consistent with an eddy board that outputs an already-normalized signal. "
					"The retained script ties this switch to one of four 'volt1'..'volt4' table objects also "
					"driven by lamps 85-87 and 77; see physical spatial notes."
				)
			if address == 74:
				notes += (
					" The retained script comments this switch 'MENAGERIE' immediately above its handler "
					"(Sub sw74_Hit: vpmTimer.PulseSw 74), tying it to the machine's menagerie-ball feature."
				)
			if address == 41:
				notes += " Modeled in the retained table as a HitTarget (T41) despite the printed 'Left Lane' name; no further construction detail is documented."
			if address in {37, 38}:
				quantity = 3 if address == 37 else 2
				notes += f" Printed target-bank quantity ({quantity}) shares this one electrical address across {quantity} standup targets."
				if address == 38:
					notes += (
						" The retained script's RMHit_Hit handler (the Ringmaster's own raised-position hit "
						"wall, collidable while RMCurrPos > 17) also pulses this same address, so it registers "
						"hits from the Ringmaster figure as well as the two printed standup targets."
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
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				if address in PULSED_SWITCHES:
					extra["pulse"] = True
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22, 11}:
					role = {
						11: "cabinet.backbox-toy",
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "backbox" if address == 11 else ("cabinet" if address in {13} else "cabinet interior")
					if address == 22:
						extra["initial_active"] = True
					if address == 11:
						notes = physical["notes"] + (
							" The retained table's own sw11 trigger object sits at a large negative x, in the "
							"VR backbox visual area, not on the physical playfield: this is the Backbox Prize "
							"Wheel/Bell mechanism (public solenoid 2, Backbox Kick), a backbox toy with no "
							"playfield location."
						)
						physical["notes"] = notes
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS or address in {37, 38, 16, 17, 26, 75, 76, 74, 41} else (VPX_TABLE_SOURCE,)
					if address in SWITCH_POSITIONS:
						extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
					else:
						extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper E.O.S.", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None, True),
		112: ("Lower Right Flipper Opto", "flipper.lower.right.button", "used", True, "opto", None, "A-17316", True),
		113: ("Lower Left Flipper E.O.S.", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None, True),
		114: ("Lower Left Flipper Opto", "flipper.lower.left.button", "used", True, "opto", None, "A-17316", True),
		116: ("Not Used Upper Right Flipper Opto", "internal.unused.flipper", "unused", True, "opto", None, None, True),
		118: ("Not Used Upper Left Flipper Opto", "internal.unused.flipper", "unused", True, "opto", None, None, True),
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
				" Cirqus Voltaire has no upper flippers and the switch-locations parts list marks this position "
				"Not Used (both assembly and switch part blank/NOT USED)."
			)
			physical["location"] = "not installed"
			notes += (
				" The switch-matrix wiring page nonetheless shades this position as an opto with a real printed "
				"wire color and J212 connector pin, matching the fitted lower-flipper button optos 112/114's "
				"template -- the WPC-95 CPU board's own generic Fliptronic circuit, present on the board hardware "
				"whether or not this machine populates it."
			)
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

	# Fliptronic F5 (115) and F7 (117) are repurposed as free-spinning targets, confirmed by the
	# retained script's own spinner handlers and by the retained table's own left/right geometry
	# (a prior legacy-migrated record had these reversed).
	spinner_inputs = {
		115: ("Right Spinner", [(0.823849, 0.276523)]),
		117: ("Left Spinner", [(0.089923, 0.295271)]),
	}
	for address, (label, positions) in spinner_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				"used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"F{address - 110}"},
				],
				normally_closed=False,
				pulse=True,
				physical={
					"part_number": "5647-12693-24",
					"switch_type": "other",
					"notes": (
						f"Printed Fliptronic grounded switch F{address - 110}, repurposed as a free-spinning "
						f"target ({'Right' if address == 115 else 'Left'} Spinner). The retained script's "
						f"sw{address}spinner_Spin handler pulses switch {address} on every rotation. The retained "
						f"table's own {'sw115spinner' if address == 115 else 'sw117spinner'} object sits at "
						f"normalized x={positions[0][0]}, confirming which physical side the printed F-position "
						"serves; a prior legacy-migrated record had the left/right spinner labels reversed."
					),
				},
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=located(f"switch.generic-{address}", "sensor", positions, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
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
						"WPC-95 CPU-board country/option configuration DIP bank. The retained transcription of "
						"this manual does not include the per-country switch-combination chart, so no specific "
						"ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def _slug(label: str) -> str:
	import re

	return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed"


def output_id(label: str) -> str:
	return f"device.{_slug(label)}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 53):
		if address in SOLENOID_LABELS or address in NOT_FITTED_SOLENOID_LABELS:
			fitted = address in SOLENOID_LABELS
			label = SOLENOID_LABELS.get(address) or NOT_FITTED_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING.get(address, {})
			if address in {22, 37, 39, 40}:
				kind = "motor"
			elif 17 <= address <= 28:
				kind = "flasher"
			elif address in {3, 5, 35}:
				kind = "magnet"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher/motor table entry {address:02d} ({printed_type})." if fitted else "Printed motor-circuit table entry 38 (Not Used)."
			if kind == "flasher":
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
				if playfield_emitters < quantity:
					notes += (
						" Only the playfield bulb(s) have a playfield placement; backbox insert-panel bulbs are "
						"behind the translite and are deliberately not given a playfield coordinate."
					)
				if address == 27:
					notes += (
						" This game's own printed \"(2)\" quantity is two physical bulbs, but the retained table "
						"models both with a single large polygon Flasher shape (f127, light-mapped to l127) "
						"draped over the Ringmaster area rather than as two separately placed bulb objects; the "
						"one recorded placement is that shape's own drag-point centroid, not two distinct bulbs. "
						"The shape's light-map object (l127) itself sits at an anomalous stray coordinate far "
						"from the shape and was excluded as a table-modeling anomaly rather than used."
					)
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/binding: {SOLENOID_CALLBACKS[address]}."
			if address == 38:
				notes += " No voltage, drive gate, or drive connection is printed in the Motor Circuit block; no device is fitted."
			if address in {33, 34, 35, 36}:
				notes += (
					" Fliptronic upper-flipper-slot circuit with no upper flippers on this machine; repurposed for "
					"a non-flipper device (Cirqus Voltaire has no upper flippers, matching cvGameData's "
					"FLIP_SOL(FLIP_L))."
				)
			if address in {45, 46, 47, 48}:
				notes += (
					" PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same "
					"circuits 29-32; the manual address is preserved as an alias."
				)
			if address == 22:
				notes += (
					" Printed inside the Flasher address block (17-28) and wired through a driver transistor the "
					"same way a flasher is, but part number A-15680 is a DC gearmotor part (reused at solenoid 39, "
					"Motor Direction) and the retained script's MotorEnable sub only starts/stops a motor sound; "
					"this is the Ringmaster motor's continuous enable line, not a flashlamp."
				)
			if address == 39:
				notes += (
					" WPC-95 LPDC output; PinMAME duplicates it at public address 43 (solNo 41-44 read back at "
					"solNo-4), so a recreation must treat 39 and 43 as one physical drive line, not an additional "
					"device. Pinned PinMAME's own preliminary cv_ringMech table (src/wpc/sims/wpc/prelim/cv.c) "
					"independently names this same drive line by its mirror address 43 rather than 39; the "
					"retained known-working script's own cvpmMech configuration (Sol2 = 39) and this manual's "
					"'MOTOR DIRECTION' printed function agree with each other and are treated as the runtime "
					"authority over the preliminary source's choice of alias."
				)
			if address == 40:
				notes += (
					" Device part A-22151-2 is a control-board circuit closely related to (but numbered "
					"differently from) the A-22149-2 \"Auto Adjust Eddy Sensor PCB\" construction printed for "
					"switches 17/26/75/76; it is not itself a moving playfield device, so it is recorded with no "
					"playfield placement."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-95 power driver board"}
			if wiring_data.get("driver_transistor"):
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
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
				if address == 2:
					extra["roles"] = ["cabinet.backbox-toy"]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				elif address == 40:
					extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
				elif address in CLAMPED_X_RAW:
					raw_x, y = SOLENOID_POSITIONS[address][0]
					placement = located(identifier, role, [(raw_x, y)], VPX_TABLE_SOURCE)
					placement["placements"][0]["provenance"]["status"] = "validated"
					notes += (
						f" The retained table's own object sits at raw normalized x={CLAMPED_X_RAW[address]:.6f}, "
						"just past the declared playfield right edge; the coordinate is clamped to the schema-"
						"valid boundary x=1.000000 with the raw offset disclosed here rather than fabricating a "
						"different position."
					)
					physical["notes"] = notes
					extra["spatial"] = placement
				else:
					extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {22, 39}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41, 51, 52} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Cirqus Voltaire playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Cirqus Voltaire playfield device.",
			31: "PinMAME's synthetic game-on state. Cirqus Voltaire sets wpc_set_fastflip_addr(0x80), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME's WPC remap has no fourth state bit; public address 32 is constant zero in both the WPC_GILAMPS and configured fast-flip branches.",
			41: "PinMAME's backward-compatibility mirror of LPDC output 39 (Motor Direction). It reports the same physical Ringmaster-motor direction line and is not an additional device; pinned PinMAME's own preliminary cv_ringMech table reads the mechanism through this mirror address rather than 39.",
			42: "Unused WPC-95 LPDC mirror of output 38 (which the motor circuit table itself marks Not Used).",
			43: "Unused WPC-95 LPDC mirror of output 39's sibling slot; the motor circuit table declares no third motor-circuit device.",
			44: "Unused WPC-95 LPDC mirror of output 40 (Eddy Board); Eddy Board is a Low Power motor-circuit entry, not an LPDC output, so PinMAME still reserves this mirror slot but nothing drives it.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. cvGameData declares custSol=2.",
			51: "cvGameData declares hw.custSol=2, publishing this address (CORE_CUSTSOLNO(1)) through the driver's own preliminary cv_getSol handler: a synthetic 10-VBLANK decaying counter that mirrors recent public-solenoid-35 (Ringmaster Magnet) activity for the *** PRELIMINARY *** ball simulator's own attract-mode animation. It is not a distinct physical device; solenoid 35 is the real control line.",
			52: "cvGameData's second custom solenoid (CORE_CUSTSOLNO(2)): the same kind of decaying counter, mirroring recent public-solenoid-36 (Upper Post) activity. Not a distinct physical device; solenoid 36 is the real control line.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address == 41 else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		if address in {51, 52}:
			roles = ["internal.duplicate.decaying-fire-state"]
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
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address == 88:
				notes += (
					" Assembly 20-9663-16 is the identical illuminated-button assembly printed for switch 13 "
					"(Start Button), confirming this is a real cabinet button lamp. The retained VPX table's own "
					"UpdateLamps routine has both 'Lampm 88, l88' calls commented out, so no Light object models "
					"it in this extraction."
				)
			if address in {87, 86, 85, 77}:
				volt = {87: "volt2", 86: "volt1", 85: "volt3", 77: "volt4"}[address]
				notes += (
					f" The retained script's UpdateLamps ties this lamp to table object '{volt}' "
					"(DisableLightingm/imgswapm), the same object switches 75/76/17/26 respectively toggle by "
					"z-position on hit -- lamp and switch share one physical 'Volt' insert."
				)
			physical["notes"] = notes

			drive_wire, drive_connection, column_driver = (
				{1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
				 3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Black", "J121-4", "Q99"),
				 5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
				 7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97")}[column]
			)
			return_wire, return_connection, row_driver = (
				{1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
				 3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
				 5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
				 7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105")}[row]
			)
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
			if address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				if address in LAMP_RENDER_DOUBLES:
					physical["notes"] += (
						f" The retained table stacks a second co-located Light object purely for brightness "
						f"(l{address}/l{address}b pair); the primary object is used and the duplicate is "
						"documented render doubling, matching the manual's single-bulb parts entry."
					)
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE)
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
	11: (0.411673, 0.63698), 12: (0.456913, 0.673254), 13: (0.499661, 0.637134), 14: (0.57327, 0.659519),
	15: (0.510579, 0.698732), 16: (0.619615, 0.691686), 17: (0.569915, 0.723714), 18: (0.093814, 0.295056),
	21: (0.339977, 0.659042), 22: (0.293408, 0.692562), 23: (0.344068, 0.722821), 24: (0.397347, 0.749496),
	25: (0.456575, 0.774479), 26: (0.455924, 0.724704), 27: (0.511071, 0.747899), 28: (0.397975, 0.698038),
	31: (0.138453, 0.388734), 32: (0.173552, 0.441376), 33: (0.196702, 0.4753), 34: (0.216071, 0.507017),
	35: (0.236537, 0.53809), 36: (0.316854, 0.453219), 37: (0.345683, 0.499854), 38: (0.36937, 0.543855),
	41: (0.521616, 0.32196), 42: (0.567497, 0.33018), 43: (0.617201, 0.33506), 44: (0.666152, 0.336686),
	45: (0.716259, 0.336681), 46: (0.597563, 0.382306), 47: (0.580927, 0.428164), 48: (0.565263, 0.473373),
	51: (0.802808, 0.308516), 52: (0.787552, 0.329457), 53: (0.770501, 0.349732), 54: (0.751655, 0.370006),
	55: (0.864685, 0.360902), 56: (0.841552, 0.39554), 57: (0.816533, 0.426273), 58: (0.793628, 0.457526),
	61: (0.457225, 0.242557), 62: (0.903334, 0.292259), 63: (0.263854, 0.472843), 64: (0.379911, 0.443291),
	65: (0.248711, 0.636248), 66: (0.27601, 0.619201), 67: (0.458709, 0.890189), 68: (0.0667, 0.808598),
	71: (0.731918, 0.205996), 72: (0.664834, 0.192417), 73: (0.596792, 0.19669), 74: (0.690314, 0.634156),
	75: (0.695571, 0.658321), 76: (0.844464, 0.809164), 77: (0.146421, 0.754513), 78: (0.422106, 0.342253),
	81: (0.064265, 0.173879), 82: (0.9133, 0.492204), 83: (0.672001, 0.520404), 84: (0.834754, 0.601865),
	85: (0.761675, 0.755795), 86: (0.485194, 0.448347), 87: (0.67207, 0.410103),
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	gi_playfield_positions = {
		0: [
			(0.699388, 0.821372), (0.746655, 0.808139), (0.682828, 0.752538), (0.721525, 0.70916),
			(0.911298, 0.700262), (0.956199, 0.666013), (0.939889, 0.447581), (0.930424, 0.370156),
			(0.92441, 0.012142), (0.880404, 0.119466), (0.719989, 0.080451),
		],
		1: [
			(0.322917, 0.284251), (0.235929, 0.26366), (0.272515, 0.225615), (0.533478, 0.200233),
			(0.785869, 0.242099), (0.722803, 0.166637), (0.636584, 0.158252), (0.441885, 0.0772),
			(0.335965, 0.064481),
		],
		2: [
			(0.212354, 0.820182), (0.164928, 0.805245), (0.225888, 0.751661), (0.19044, 0.708034),
			(0.051407, 0.632656), (0.040651, 0.509955), (0.090234, 0.437869), (0.064828, 0.388346),
			(0.134199, 0.215164), (0.155296, 0.005028), (0.196377, 0.094879),
		],
	}
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
		if address in gi_playfield_positions:
			positions = gi_playfield_positions[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter "
				"coordinate come from the retained table's GI emitter collection for this string (UpdateGI in "
				"the retained script). GI address 0 drives collection Gi_Pf_Right_01; GI address 1 drives "
				"Gi_Pf_Middle_02; GI address 2 drives Gi_Pf_Left_03. Each collection's own large overlay-shape "
				"helper Light (GIRight/GiCenter/GILeft, a Flasher-type object with no discrete center) is "
				"excluded as a table-modeling render helper, not a distinct physical bulb."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox illumination behind the translite; the retained script's UpdateGI handles only GI "
				"addresses 0-2, so this string has no playfield coordinate. Marked '**' on the printed page: "
				"these strings do not brighten/dim, they are always on."
			)
			if address == 4:
				notes += " This string additionally feeds cabinet bulbs through J104, the only cabinet connection on the printed general-illumination wiring."
			notes += (
				" The Solenoid/Flashlamp Locations list (printed 2-46) prints this same address's function name "
				"the opposite way round ('Backbox 1'/'Backbox 2' swapped) from the primary wiring table (printed "
				"2-50, which carries the connector numbers); see conflict.gi-backbox-string-numbering."
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
		return record

	return [
		mechanism(
			"mechanism.ringmaster",
			"Rising/rotating Ringmaster head",
			"motorized",
			[output_id("Motor Enable"), output_id("Motor Direction")],
			["switch.matrix-42", "switch.matrix-43", "switch.matrix-44", "switch.matrix-16"],
			"A DC gearmotor (A-21953 Ring Master Assembly, part A-15680) drives the Ringmaster figure through "
			"a 0-118 position counter tracked by the retained script's cvpmMech class (mechRM: Sol1=22 pulses "
			"the motor, Sol2=39 sets direction, Length=960, Steps=118). Position 0-1 asserts switch 44 "
			"(Ringmaster Down, retracted below the playfield, Ringmaster.z = -310), position 88-89 asserts "
			"switch 43 (Ringmaster Middle), and position 117-118 asserts switch 42 (Ringmaster Up, raised near "
			"the playfield surface, Ringmaster.z = -56). UpdateRM steps a chain of 22 collision-wall objects "
			"(RMWall0..RMWall255) as the head rises so a ball can only strike it while it protrudes, and enables "
			"switch 16 (Top Eddy, the A-20036 Magic Eddy Coil PCB) only while the head is out of its home "
			"position (RMCurrPos between 4 and 100). Service Bulletin 102 documents a factory lubrication "
			"procedure for the mechanism's own cam-and-switch assembly (\"Locate the Ringmaster Cam & Switch "
			"Assembly on the back of the Ringmaster bracket\"). Pinned PinMAME's own preliminary cv_ringMech "
			"table (src/wpc/sims/wpc/prelim/cv.c) models the same three switches over a shorter 0-127 range with "
			"a different position-to-switch ordering and names its second solenoid by public address 43 (the "
			"WPC-95 LPDC mirror of 39) rather than 39 directly; the retained known-working script is treated as "
			"authoritative for runtime position-to-switch mapping and this manual for the printed Up/Middle/Down "
			"labels, both of which agree with each other.",
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-21953",
		),
		mechanism(
			"mechanism.ringmaster-magnet",
			"Ringmaster magnet ball catcher",
			"other",
			[output_id("Ringmaster Magnet")],
			[],
			"Solenoid 35 energizes a magnet (mRingmasterMagnet, InitMagnet RingmasterMagnet) at the Ringmaster "
			"head that catches a ball in flight (RMMagnetkicker_Hit). On release the retained script's "
			"SolRingmasterMagnet sub computes a randomized kick angle (125-235 degrees from a coin-flip base) "
			"and velocity, then fires the ball off the magnet after a 400 ms delay -- a scripted trick-shot "
			"release rather than a plain drop. There is no dedicated switch; ball presence is tracked purely in "
			"script state (RMBallInMagnet).",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-21953",
		),
		mechanism(
			"mechanism.loop-and-ramp-magnets",
			"Left loop and ramp ball-catch magnets",
			"other",
			[output_id("Left Loop Magnet"), output_id("Ramp Magnet")],
			["switch.matrix-64"],
			"Two independent grab-and-release magnets: solenoid 3 (Left Loop Magnet, cvpmMagnet LoopMagnet at "
			"the LeftMagnet object) catches a ball on the left orbit, and solenoid 5 (Ramp Magnet, cvpmMagnet "
			"LockMagnet at the RampMagnet object) catches a ball on the upper ramp at the same location switch "
			"64 (Ramp Magnet) senses. Both magnets are configured through the retained script's cvpmMagnet class "
			"(.Solenoid = 3 / .Solenoid = 5) rather than through an explicit SolCallback line; two commented-out "
			"SolCallback(3)/SolCallback(5) lines earlier in the script are vestigial from an older authoring "
			"approach superseded by the class-based binding.",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.diverter",
			"Right-orbit diverter",
			"gate",
			[output_id("Diverter Power"), output_id("Diverter Hold")],
			[],
			"Solenoid 6 (Diverter Power) and solenoid 34 (Diverter Hold) drive one diverter flap (Diverter) that "
			"routes a ball into or past the right orbit. The retained script's DiverterHold sub rotates the flap "
			"and swaps a pair of wall objects (diverter_rightorbit_On/Off) together; there is no dedicated switch "
			"and no script callback is registered for solenoid 6 alone, consistent with 6 being the brief power "
			"pulse that moves the flap and 34 being the continuous hold that keeps it there.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-22035",
		),
		mechanism(
			"mechanism.upper-post",
			"Upper post (subway/lock exit)",
			"gate",
			[output_id("Upper Post")],
			[],
			"Solenoid 36 raises and lowers a single post (UpperPostWall) near the top of the playfield; the "
			"retained script's UpperPost sub toggles UpperPostWall.IsDropped and plays a sound positioned at the "
			"subwaykicker1 object. No dedicated switch is printed.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-17932",
		),
		mechanism(
			"mechanism.disappearing-jet-bumper",
			"Disappearing (raising/lowering) middle jet bumper",
			"motorized",
			[output_id("Jet Up"), output_id("Jet Release"), output_id("Middle Jet Bumper")],
			["switch.matrix-54"],
			"Assembly A-21564 (\"Disappear Jet Bump Assembly\", Lower Playfield Parts item 8) raises the middle "
			"jet bumper into play (solenoid 7, Jet Up) and releases/lowers it (solenoid 8, Jet Release); solenoid "
			"4 (Middle Jet Bumper) is the same assembly's own thump/kick coil, sharing its assembly part number, "
			"and switch 54 senses a hit. The retained script's JetUp/JetRelease subs toggle the "
			"boombumperflipper Flipper object's collidability and a companion rubber/skirt animation. Service "
			"Bulletin 101 (1997-12-09) documents a factory quality-assurance fix for the first 200 production "
			"samples: a brass release latch installed backwards and a release-coil frame that could bend, both "
			"correctable with an added bracket (p/n 01-14803).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE,
			assembly_part_number="A-21564",
		),
		mechanism(
			"mechanism.ramp-lock",
			"Three-position ramp ball lock",
			"other",
			[output_id("Lock Post")],
			["switch.matrix-66", "switch.matrix-67", "switch.matrix-68"],
			"A vertical three-position lock on the Center Wire ramp (A-21851) holds up to three balls at switches "
			"66 (Ramp Lock Low), 67 (Ramp Lock Middle), and 68 (Ramp Lock High); the retained script's cvpmVLock "
			"class (vlLock) tracks the three positions and solenoid 16 (Lock Post) releases them "
			"(vlLock.SolExit). Service Bulletin 104 (1998-04-02) documents a factory adjustment for these same "
			"three switches: \"we recommend that you further adjust the switch tension on the three center LOCK "
			"switches (p/n 5647-12693-66)... move the switchblades over to the other pivot position\", "
			"independently confirming both the part number and the three-switch construction transcribed from "
			"the switch-locations list.",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.ball-trough",
			"Four-ball trough and eject",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"The retained script's cvpmBallStack class (bsTrough.InitSw 0, 32, 33, 34, 35) tracks four balls "
			"resting on trough optos 32-35 and ejects the ball at the head of the trough through solenoid 9 "
			"(Trough Eject), which pulses trough-eject opto 31 in the same event (SolRelease: vpmTimer.PulseSw "
			"31). All five positions are printed optos that rest closed (switch-matrix column 3), and the class "
			"exposes no individually named playfield trigger objects for the four ball positions, only the "
			"exit kicker (BallRelease).",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Plunger")],
			["switch.matrix-18"],
			"An auto-plunger (solenoid 1, Plunger1.Fire) launches a ball resting on shooter-lane switch 18.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-21022",
		),
		mechanism(
			"mechanism.saucers",
			"Left and right saucers",
			"kicker",
			[output_id("Left Saucer"), output_id("Right Saucer")],
			["switch.matrix-71", "switch.matrix-72"],
			"Two ball-catching saucers (cvpmBallStack .InitSaucer sw71/sw72, each object serving as both the "
			"switch trigger and the kicker) are cleared by solenoid 14 (Left Saucer) and solenoid 15 (Right "
			"Saucer).",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-21829",
		),
		mechanism(
			"mechanism.popper",
			"Popper (subway kickout)",
			"kicker",
			[output_id("Popper")],
			["switch.matrix-36"],
			"A ball resting on opto 36 (Popper Opto) is kicked back to the playfield by solenoid 33 (Popper), "
			"printed on the upper-flipper Fliptronic slot rather than the standard 1-16 solenoid range.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-21824",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-51", "switch.matrix-52"],
			"Standard slingshot assemblies (A-21527) at switches 51/52, fired by solenoids 10/11.",
			MANUAL_SOURCE, VPX_TABLE_SOURCE,
			assembly_part_number="A-21527",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Fixed upper and lower jet bumpers",
			"other",
			[output_id("Upper Jet Bumper"), output_id("Lower Jet Bumper")],
			["switch.matrix-53", "switch.matrix-55"],
			"Two standard fixed jet bumpers (A-9415-2) at switches 53 (Upper) and 55 (Lower), fired by solenoids "
			"12/13; distinct from the disappearing middle jet bumper (switch 54, mechanism.disappearing-jet-"
			"bumper).",
			MANUAL_SOURCE, VPX_TABLE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.wow-target-bank",
			"\"WOW\" three-target bank",
			"other",
			[],
			["switch.matrix-37"],
			"Three standup targets (assembly A-21960-6, retained table objects T37a/T37b/T37c) share the single "
			"printed switch address 37; any one target hit registers on that one electrical address. Manual "
			"prints the printed quantity as \"WOW\" Targets (3).",
			MANUAL_SOURCE, VPX_TABLE_SOURCE,
			assembly_part_number="A-21960-6",
		),
		mechanism(
			"mechanism.top-target-bank",
			"Top two-target bank",
			"other",
			[],
			["switch.matrix-38"],
			"Two standup targets (assembly A-18530-6, retained table objects T38a/T38b) share the single printed "
			"switch address 38. Manual prints the printed quantity as Top Targets (2). The retained script's "
			"RMHit_Hit handler -- the Ringmaster figure's own raised-position hit wall (RMHitWallSMall, "
			"collidable while RMCurrPos > 17) -- also pulses switch 38, so this one address additionally "
			"registers hits on the raised Ringmaster figure, not only the two standup targets.",
			MANUAL_SOURCE, VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-18530-6",
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
			"Two Fliptronic flippers (right A-14876-R, left A-15849-L). Each flipper has a separate power and "
			"hold winding: the ROM energizes the power winding on the cabinet button opto (112 right, 114 left), "
			"then drops to the hold winding once the end-of-stroke leaf switch (111 right, 113 left) closes. "
			"There are no upper flippers; the upper-flipper Fliptronic circuits (33-36 repurposed, 115/117 "
			"repurposed as spinners, 116/118 unfitted) carry no flipper hardware.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-14876-R right with A-15849-L left",
		),
		mechanism(
			"mechanism.spinners",
			"Left and right spinners",
			"other",
			[],
			["switch.generic-115", "switch.generic-117"],
			"Two free-spinning targets wired on the Fliptronic F5 (public 115, Right Spinner) and F7 (public 117, "
			"Left Spinner) positions rather than the switch matrix. The retained script's sw115spinner_Spin and "
			"sw117spinner_Spin handlers each pulse their own switch and play the spinner sound effect on every "
			"rotation.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE,
			assembly_part_number="5647-12693-24",
		),
		mechanism(
			"mechanism.backbox-prize-wheel",
			"Backbox prize wheel and bell",
			"other",
			[output_id("Backbox Kick")],
			["switch.matrix-11"],
			"Solenoid 2 (Backbox Kick) launches a ball (Plunger2) into a backbox spinning-wheel/bell assembly; "
			"the retained script's BackBoxKick sub randomly selects one of four wheel-spin cases, each ending "
			"with an EndCannon timer that pulses switch 11 (Backbox Luck) and plays a bell sound. This is a "
			"backbox toy with no playfield location; both the trigger switch and the kicker object sit in the "
			"retained table's separate backbox visual coordinate space, not on the physical playfield.",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="B-11873",
		),
		mechanism(
			"mechanism.menagerie-ball-rebound",
			"Menagerie ball rebound",
			"other",
			[],
			["switch.matrix-74"],
			"Switch 74 (printed Big Ball Rebound) is commented 'MENAGERIE' directly above its handler in the "
			"retained script (Sub sw74_Hit: vpmTimer.PulseSw 74), tying it to the machine's menagerie-ball "
			"feature; no dedicated actuator is printed for this switch.",
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17794",
		),
		mechanism(
			"mechanism.neon-ramp",
			"Neon ramp lighting",
			"other",
			[output_id("Neon")],
			[],
			"Solenoid 37 (Neon, Low Power) drives the A-21577 Neon Ramp Assembly. Service Bulletin 102's Upgrade "
			"D documents a factory bracket retrofit for the ramp's own switch mounting (\"the bracket should be "
			"to the right of the Spinner Assembly\"), independently confirming the assembly's playfield location "
			"near a spinner. There is no dedicated switch for the neon tube itself.",
			MANUAL_SOURCE,
			assembly_part_number="A-21577",
		),
		mechanism(
			"mechanism.eddy-sensors",
			"Eddy-current proximity sensor bank",
			"other",
			[],
			["switch.matrix-17", "switch.matrix-26", "switch.matrix-75", "switch.matrix-76"],
			"Four A-18008-1 eddy-current proximity sensors (part A-16443) at switches 17 (Right Inlane), 26 (Left "
			"Inlane), 75 (\"Volt\" Right), and 76 (\"Volt\" Left) detect a ball without a mechanical contact "
			"switch, driven by the A-22151-2/A-22149-2 eddy control-board circuitry (solenoid 40, Eddy Board). "
			"The retained script ties each of the four switches to one of four 'volt1'..'volt4' table objects "
			"also driven by lamps 85-87 and 77 (see lamp-matrix.md), confirming the four sensors and four "
			"matching inserts form one 'Volt' effect around the two inlanes and two Volt targets.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-18008-1",
		),
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.wow-top-targets-opto-not-normalized",
			"path": "inputs[binding.device=37,38]",
			"description": (
				"The printed switch matrix (page 2-49) shades column 3 -- addresses 31 through 38 -- entirely "
				"'OPTO, TYPICALLY CLOSED', and the switch-locations parts list confirms addresses 37 (\"WOW\" "
				"Targets, assembly A-21960-6) and 38 (Top Targets, assembly A-18530-6) with no separate switch "
				"part number, the same signature pattern as the trough optos. Pinned PinMAME's cvGameData "
				"inverted-switch mask ({0x00,0x00,0x00,0x3f,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}) covers only "
				"bits 0-5 of column 3 (addresses 31-36); bits 6-7 (37, 38) are clear, so unlike 31-36 the public "
				"state of 37 and 38 is not emulator-normalized even though the manual documents them as normally "
				"closed hardware. The manual is physical-construction ground truth and pinned PinMAME is "
				"public-address and emulator-normalization ground truth, and the two disagree on whether a "
				"recreation must invert these two addresses. Resolution path: run the implemented LibPinMAME "
				"gameplay harness against a legal cv_20h or cv_14 ROM, and observe the idle public state of 37 "
				"and 38 and their transitions when a target is hit. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.gi-backbox-string-numbering",
			"path": "outputs[binding.group=pinmame.output.gi,device=3,4]",
			"description": (
				"The primary Solenoid/Flasher/G.I. wiring table (printed page 2-50) prints GI item 04 as "
				"\"Backbox 2\" (connector J106-5/J106-10) and item 05 as \"Backbox 1\" (connector J106-6+J104-3/"
				"J106-11+J104-1, the only GI row with a cabinet leg). The separate Solenoid/Flashlamp Locations "
				"list (printed page 2-46) prints the same two items the other way round -- item 04 \"Backbox 1\", "
				"item 05 \"Backbox 2\" -- with no connector data to arbitrate. Both are the manual's own printed "
				"text; this record uses the primary wiring table's connector-carrying labels (public GI address "
				"3 = \"Backbox 2\", address 4 = \"Backbox 1\") as authoritative, but the disagreement itself is "
				"unresolved rather than silently normalized away. Neither address has a playfield coordinate "
				"regardless of which label is used, since both are backbox insert-panel strings the retained "
				"script's UpdateGI never dispatches. "
				"Resolution path: a photograph or continuity check of the backbox insert-panel harness on an "
				"unrestored machine, establishing which physical string plugs J106-5/J106-10 and which plugs "
				"J106-6/J106-11 with the cabinet leg on J104-1/J104-3, or a second printed revision of the "
				"Bally manual whose pages 2-46 and 2-50 agree with each other; no emulator trace can settle "
				"it, because only the printed name attached to each already-identified drive is in dispute. "
				"Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "bally.cirqus-voltaire.1997",
			"name": "Cirqus Voltaire",
			"manufacturer": "Bally",
			"year": 1997,
			"kind": "physical_pinball",
			"ipdb_id": 4059,
			"playfield": {"width": TABLE_WIDTH, "height": TABLE_HEIGHT, "units": "vpx"},
			"opdb_id": "GRVjJ-MLq7W",
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
		"relationships": [
			{
				"id": "relationship.trough-eject-opto",
				"kind": "pulse",
				"source": output_id("Trough Eject"),
				"destination": "switch.matrix-31",
				"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
			},
		],
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/cirqus-voltaire-1997.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Cirqus Voltaire device identifiers are not unique: {duplicates}")
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
			"Public switches 37 and 38 ('WOW' Targets, Top Targets) are printed normally-closed opto "
			"interrupters that pinned PinMAME's cvGameData inverted-switch mask does not normalize "
			"(bits 6-7 of the mask's column-3 entry are clear, unlike bits 0-5 for 31-36). This is a "
			"polarity conflict, not a spatial gap -- every dimension this report audits is complete "
			"and validated -- but it is recorded as conflict.wow-top-targets-opto-not-normalized and "
			"keeps the machine record partial until a LibPinMAME harness trace against a legal cv_20h "
			"or cv_14 ROM observes the true idle public state of 37/38.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": TABLE_WIDTH, "bottom": TABLE_HEIGHT},
			"x": "x/964; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/cirqus-voltaire-1997/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
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
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.cirqus-voltaire.1997/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/cirqus-voltaire/manual-transcription.md",
			},
		},
		"excluded_object_classes": [
			"GIRight, GiCenter, GILeft flasher-type large overlay shapes with no discrete center -- render helpers, not distinct physical bulbs",
			"l127 (Ringmaster Flashers light-map object) at an anomalous stray coordinate far from its own Flasher shape f127 -- table modeling anomaly, not used",
			"l##b-style co-located brightness-doubling Light objects for every lamp address",
		],
		"clamped_coordinates": [
			{"group": "pinmame.output.solenoid", "address": address, "raw_x": raw_x, "clamped_x": 1.0}
			for address, raw_x in sorted(CLAMPED_X_RAW.items())
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Cirqus Voltaire (Bally, 1997) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete, but the physical "
		"machine record itself remains `partial` at `machines/partial/bally/cirqus-voltaire-1997.json` "
		"because of an unresolved switch-polarity conflict outside this audit's scope; see the promotion "
		"decision below.",
		"",
		"The matching source is the retained known-working `Cirqus Voltaire (Bally 1997) VPW Mod v1.0.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 rounded to at most six "
		"fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Bally operations manual "
		"is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- The retained manual has a present but column-shifted `pdftotext -layout` text layer. Every printed "
		"table used here was read from 300-600 dpi renders, not the OCR text layer alone.",
		"- Trough switches 31-35 have no dedicated playfield trigger object because the retained script's "
		"cvpmBallStack class tracks them from internal ball-count state; they are documented projections onto "
		"the trough's own exit kicker (BallRelease). Ringmaster switches 42-44 are likewise projected onto the "
		"Ringmaster figure itself, since the retained script's cvpmMech class reads them from one continuous "
		"motor-position counter rather than three discrete sensor objects.",
		"- Two solenoid-driven mechanisms (Diverter Power/Hold at 1.06-1.07 normalized x, Neon at 1.08) sit "
		"just past the retained table's own declared right edge; each is clamped to x=1.000000 with the raw "
		"offset disclosed rather than fabricating a different coordinate.",
		"- GI strings 0-2 use the retained table's Gi_Pf_Right_01/Gi_Pf_Middle_02/Gi_Pf_Left_03 emitter "
		"collections, matching the retained script's `UpdateGI` dispatch exactly. GI strings 3 and 4 are backbox "
		"insert-panel circuits and take a controlled `cabinet_or_service` record; the manual disagrees with "
		"itself about which is 'Backbox 1' and which is 'Backbox 2' (conflict.gi-backbox-string-numbering), "
		"which does not affect either string's spatial disposition.",
		"- Solenoids 41 and 51/52 are PinMAME's mirror/decaying-state duplicates of physical solenoids 39, 35, "
		"and 36 respectively and are declared `virtual` with a `virtual` spatial record so no duplicate device "
		"is ever placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"- A prior legacy-migrated record had the Left/Right Spinner labels (switches 115/117) reversed; the "
		"manual's own printed F5/F7 labels and the retained table's own left/right geometry both independently "
		"agree and correct it.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Clamped coordinates",
		"",
	]
	for entry in report["clamped_coordinates"]:
		lines.append(f"- Solenoid {entry['address']}: raw x={entry['raw_x']:.6f}, clamped to {entry['clamped_x']:.6f}")
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
		"byte-for-byte. However, public switches 37 and 38 ('WOW' Targets, Top Targets) are printed "
		"normally-closed opto interrupters that pinned PinMAME's cvGameData inverted-switch mask does not "
		"normalize -- an unresolved polarity conflict recorded as "
		"`conflict.wow-top-targets-opto-not-normalized` -- and a second, independent manual self-contradiction "
		"about the two backbox GI strings' own numbering is recorded as "
		"`conflict.gi-backbox-string-numbering`. The definition therefore carries a non-empty `conflicts` array "
		"and `coverage.dimensions.physical_wiring = \"conflicted\"`, so promotion to `author_ready` is refused; "
		"the record stays `partial` with `coverage.missing = [\"polarity\", \"unresolved_conflicts\"]` until a "
		"LibPinMAME harness trace against a legal cv_20h or cv_14 ROM observes the true idle public state of "
		"37/38.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Human transcription of every printed table read from the rendered manual pages under "
		"`external:pinmame-review-artifacts/cirqus-voltaire/`.",
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
		raise RuntimeError(f"Stale Cirqus Voltaire author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Cirqus Voltaire definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Cirqus Voltaire seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Cirqus Voltaire definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Cirqus Voltaire seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Cirqus Voltaire spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Cirqus Voltaire spatial review drifted from its deterministic curator: {markdown_path}")
	print("Cirqus Voltaire definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Cirqus Voltaire extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Cirqus Voltaire retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
