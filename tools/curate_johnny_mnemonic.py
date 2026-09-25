"""Curate the physical Williams Johnny Mnemonic (1995) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal below, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: the flasher sockets are measured only from the manual's location drawing (the
# retained table parks its flasher lights at the cabinet edge), G.I. string 4 has no coordinate at
# all, and the playfield G.I. sockets come only from the retained table's G.I. collections.
PARTIAL_PATH = ROOT / "machines/partial/williams/johnny-mnemonic-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/johnny-mnemonic-1995.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/johnny-mnemonic-1995.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/johnny-mnemonic-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/johnny-mnemonic-1995.md"
KNOWLEDGE_PATH = "knowledge/williams/johnny-mnemonic-1995.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts/williams.johnny-mnemonic.1995"
EXCERPT_PREFIX = "evidence/excerpts/williams.johnny-mnemonic.1995"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
MANUAL_SOURCE = "manual.williams.johnny-mnemonic.1995.operations-manual"
SB85_SOURCE = "service-bulletin.williams.johnny-mnemonic.sb85"
SB87_SOURCE = "service-bulletin.williams.johnny-mnemonic.sb87"
ADDENDUM1_SOURCE = "service-bulletin.williams.johnny-mnemonic.addendum-1"
ADDENDUM2_SOURCE = "service-bulletin.williams.johnny-mnemonic.addendum-2"
VPX_TABLE_SOURCE = "vpx-table.johnny-mnemonic-vpw-1-2-2"
VPX_SCRIPT_SOURCE = "vpx-script.johnny-mnemonic-vpw-1-2-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.johnny-mnemonic-vpw-1-2-2"
CORPUS_SCRIPT_SOURCE = "vpx-script.johnny-mnemonic-1-3"
DRAWING_FIT_SOURCE = "human-review.johnny-mnemonic.solenoid-drawing-fit"
ARCHIVE_TABLE_SOURCE = "vpx-table.johnny-mnemonic-alessio-2020"

MANUAL_SHA256 = "5dfa8c788011a3e1177668eb0815ed081dbd2c96ca4859f3525bf040b9f01519"
ADDENDUM1_SHA256 = "a6469fb01b1dc9c78e9fecea3a9dbb1deea6e286f6ae05d3df9579ecbf85f4c8"
ADDENDUM2_SHA256 = "1e6e3b63122fa36c36f89aa6ac9d231188a7668ab8b53d27dcc53ccfef7dd314"
SB85_SHA256 = "3af7d09c1f02cf9dc93995ef2931aeab82f322c08a327e0283a4feda7b928662"
SB87_SHA256 = "00aefd0da623f9789ae3f2ddc1b9ddc190041fcc3a21d4f229d6851499814ee2"
TABLE_SHA256 = "234c81299f3bff614fee39f9fa5594f060dbc06f49d96f8e68673fb07c03acf8"
SCRIPT_SHA256 = "1a70a6128f293072261657597b4b62c404d16d5e88e50080a3bc163b2fe1d5ef"
CORPUS_SCRIPT_SHA256 = "38e1e83bd2b6ca8b4720c49591a36d30cb7d0f3863a52668c41fc4d8b1617d08"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
DRAWING_FIT_SHA256 = "b7b8d812e2072bbb7190836b9956123a7191d41ca2c76a63c03390dbdf86ea4d"
DRAWING_FIT_OUTPUT_SHA256 = "5be04b8cdc5643c829b793cec16b27efa4cedb2852c2fd637cee7084e8e58cf0"
ARCHIVE_TABLE_SHA256 = "45ca049ef65852c5eb01076c4b19cdc3e92e5a7beb98fee8e2d77b87334485e6"
ARCHIVE_SCRIPT_SHA256 = "c66790ffbc7a1b91799563797d4eeef56652df986fa6cb22c134d87c0bc6edaf"
ARCHIVE_MANIFEST_SHA256 = "e94fce3afda18382b04e010d45cb58585ab5b36131cd7316b836c14d88c6670f"
ARCHIVE_FILE_COUNT = 814
ARCHIVE_TOTAL_BYTES = 78611022

EXTRACTION_RELATIVE_PATH = Path("williams/johnny-mnemonic-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/johnny-mnemonic-1995/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "4cd4fe13f56c9400a0bc7aef22ea70256af35bae8d8ec41937a23b459ef40809"
EXTRACTION_FILE_COUNT = 3281
EXTRACTION_TOTAL_BYTES = 729809766

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
WAYBACK_PREFIX = "https://web.archive.org/web/"
IPDB_FILES = "https://www.ipdb.org/files/3683/"
ACQUIRED_AT = "2026-09-25T19:41:51Z"

DRIVER_IDS = ("jm_12r", "jm_12b", "jm_05r")
DRIVER_COMPATIBILITY = {
	"jm_12r": ("identical", "Williams 1.2R game ROM, the parent of the jm clone tree and the firmware both retained scripts run."),
	"jm_12b": ("identical", "Williams 1.2 Belgian game ROM for the same physical machine. It is declared with the same wpc_mSecurityS machine driver and shares the parent's jmGameData, so every public address is the same."),
	"jm_05r": (
		"compatible",
		"Williams 0.5R prototype game ROM (pinned jm.c asks whether it is the 0.4 named in the version history). It shares the parent's "
		"jmGameData and wpc_mSecurityS machine driver, so the public controller contract is the same; no retained source documents the "
		"prototype cabinet, so its physical build is not asserted identical. Manual Addendum 1 records that the first 100 sample games ran "
		"game code 1.0 or 1.1, which must be paired with sound code 1.0.",
	),
}

# --- Printed switch matrix (manual printed 2-34; the quick-reference sheet PDF 141 repeats it).
SWITCH_LABELS = {
	11: "Ball Launch", 12: "X Hand Home", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Left Outlane",
	16: "Left Return Lane", 17: "Right Return Lane", 18: "Right Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In Button", 24: "Always Closed", 25: "Left Slingshot",
	26: "Right Slingshot", 27: "Left Standup Target", 28: "Right Standup Target",
	31: "Trough Jam", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3", 35: "Trough Ball 4",
	36: "Ball Popper", 37: "Y Hand Home", 38: "Right Rubber",
	41: "Left Ramp Enter", 42: "Left Ramp Made", 43: "Drop Target", 44: "Left Jet Bumper", 45: "Bottom Jet Bumper",
	46: "Right Jet Bumper", 47: "Crazy Bob's", 48: "Spinner",
	51: "Cyber Matrix 11", 52: "Cyber Matrix 21", 53: "Cyber Matrix 31", 54: "Right Ramp Enter", 55: "Right Ramp Made",
	56: "Left Loop", 57: "Right Loop", 58: "Inner Loop Entry",
	61: "Cyber Matrix 12", 62: "Cyber Matrix 22", 63: "Cyber Matrix 32", 64: "Left Jet Lane", 65: "Middle Jet Lane",
	66: "Right Jet Lane", 67: "Right Hand Control", 68: "Left Hand Control",
	71: "Cyber Matrix 13", 72: "Cyber Matrix 23", 73: "Cyber Matrix 33", 74: "X Hand Encoder A", 75: "X Hand Encoder B",
	76: "Y Hand Encoder B", 77: "Y Hand Encoder A", 78: "Shooter Lane",
}
UNUSED_MATRIX_ADDRESSES = {81, 82, 83, 84, 85, 86, 87, 88}
# Shaded "Opto, Typically Closed" on the printed matrix.
OPTO_SWITCHES = {31, 32, 33, 34, 35, 36, 74, 75, 76, 77}
# jmGameData's inverted-switch mask {0x00,0x00,0x00,0x3f,0x00,0x00,0x00,0x78,0x00,...} is indexed by
# matrix column: 0x3f normalizes 31-36 and 0x78 normalizes 74-77.
PINMAME_INVERTED_MASK = (0x00, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00)
# vpmTimer.PulseSw callers in the retained script: slingshots, jets, the right rubber and the spinner,
# the launch button key, and Trough Jam, which SolRelease pulses on every trough eject.
PULSED_SWITCHES = {11, 25, 26, 31, 38, 44, 45, 46, 48}
CYBER_MATRIX_SWITCHES = {51, 52, 53, 61, 62, 63, 71, 72, 73}
HAND_SENSOR_SWITCHES = {12, 37, 74, 75, 76, 77}

SWITCH_TYPES = {
	11: "button", 12: "microswitch", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "tilt", 22: "microswitch", 23: "button", 24: "other", 25: "leaf", 26: "leaf", 27: "leaf",
	28: "leaf", 31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "microswitch", 38: "leaf",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "leaf", 45: "leaf", 46: "leaf", 47: "microswitch",
	48: "microswitch", 51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch", 61: "microswitch", 62: "microswitch", 63: "microswitch",
	64: "microswitch", 65: "microswitch", 66: "microswitch", 67: "button", 68: "button", 71: "microswitch",
	72: "microswitch", 73: "microswitch", 74: "opto", 75: "opto", 76: "opto", 77: "opto", 78: "microswitch",
}
SWITCH_PARTS = {
	11: "20-9663-B-4", 12: "5647-12693-06", 13: "20-9663-2", 14: "A-15361", 15: "5647-12693-19", 16: "5647-12693-19",
	17: "5647-12693-19", 18: "5647-12693-19", 21: "A-17238", 22: "5643-09268-00", 23: "20-9663-21", 24: "5643-09112-00",
	25: "A-17800 (kick) with A-17794 (score)", 26: "A-17800 (kick) with A-17794 (score)", 27: "A-20499-9", 28: "A-20499-9",
	31: "A-18617-1 LED with A-18618-1 transistor", 32: "A-18617-1 LED with A-18618-1 transistor",
	33: "A-18617-1 LED with A-18618-1 transistor", 34: "A-18617-1 LED with A-18618-1 transistor",
	35: "A-18617-1 LED with A-18618-1 transistor", 36: "A-16908 LED with A-16909 photo transistor", 37: "5647-12693-06",
	38: "A-17794", 41: "5647-12693-24", 42: "5647-12693-21", 43: "5647-12693-31", 44: "A-16443", 45: "A-16443",
	46: "A-16443", 47: "5647-12693-43", 48: "5647-12693-24", 51: "5647-14712-01", 52: "5647-14712-01",
	53: "5647-14712-01", 54: "5647-12693-24", 55: "5647-12693-21", 56: "5647-12693-24", 57: "5647-12693-19",
	58: "5647-12693-19", 61: "5647-14712-01", 62: "5647-14712-01", 63: "5647-14712-01", 64: "5647-12693-19",
	65: "5647-12693-19", 66: "5647-12693-19", 67: "A-18602-1", 68: "A-18602", 71: "5647-14712-01", 72: "5647-14712-01",
	73: "5647-14712-01", 74: "A-20533.1", 75: "A-20533.1", 76: "A-20533.1", 77: "A-20533.1", 78: "5647-12693-32",
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
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"),
	4: ("Orange-Yellow", "J205-4"), 5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"),
	7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credits / Escape", "service.escape", "Printed Normal Function Srv Crdts, Test Function Escape."),
	6: ("Volume Down / Down", "service.down", "Printed Normal Function Volume Dn, Test Function Down."),
	7: ("Volume Up / Up", "service.up", "Printed Normal Function Volume Up, Test Function Up."),
	8: ("Begin Test / Enter", "service.enter", "Printed Normal Function Begin Test, Test Function Enter."),
}
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "leaf", "SW-1A-194", "Black-Green", "J906-1"),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", "opto", "A-17316", "Blue-Violet", "J905-1"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "leaf", "SW-1A-194", "Black-Blue", "J906-3"),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", "opto", "A-17316", "Blue-Gray", "J905-2"),
}
UNUSED_FLIPPER_SWITCHES = {
	116: ("Black-Yellow", "J905-3", "Upper Right Flipper Opto", "Upper Right Flipper Cbnt"),
	117: ("Black-Gray", "J906-5", "Upper Left Flipper E.O.S.", "Upper Left Flipper E.O.S."),
	118: ("Black-Blue", "J905-5", "Upper Left Flipper Opto", "Upper Left Flipper Cbnt"),
}

# --- Normalized playfield coordinates from the retained VPW v1.2.2 extraction, x/964 and y/2162
# (external:pinmame-review-artifacts/johnny-mnemonic/vpx-geometry-raw.tsv). Walls use the mean of
# their drag points.
SWITCH_POSITIONS = {
	15: (0.053456, 0.792896), 16: (0.125042, 0.74053), 17: (0.779078, 0.740194), 18: (0.851359, 0.762921),
	25: (0.22369, 0.73513), 26: (0.679548, 0.735172), 27: (0.099402, 0.536998), 28: (0.858487, 0.516792),
	31: (0.847395, 0.870418), 32: (0.847395, 0.870418), 33: (0.781005, 0.889331), 34: (0.710927, 0.910299),
	35: (0.638082, 0.930486), 36: (0.373924, 0.100777), 38: (0.850915, 0.588529),
	41: (0.291436, 0.450092), 42: (0.128559, 0.341198), 43: (0.443696, 0.112586),
	44: (0.176482, 0.240365), 45: (0.223952, 0.317187), 46: (0.385499, 0.268581), 47: (0.420812, 0.32717),
	48: (0.64467, 0.215595),
	51: (0.639004, 0.063367), 52: (0.713174, 0.063367), 53: (0.787344, 0.063367),
	54: (0.78304, 0.296945), 55: (0.93468, 0.316034), 56: (0.150341, 0.449108), 57: (0.938563, 0.209803),
	58: (0.600101, 0.093345),
	61: (0.639004, 0.096901), 62: (0.713174, 0.096901), 63: (0.787344, 0.096901),
	64: (0.205753, 0.164457), 65: (0.299279, 0.171771), 66: (0.391233, 0.181187),
	71: (0.639004, 0.130435), 72: (0.713174, 0.130435), 73: (0.787344, 0.130435),
	78: (0.939177, 0.893043),
}
SWITCH_OBJECTS = {
	15: "Trigger sw15", 16: "Trigger sw16", 17: "Trigger sw17", 18: "Trigger sw18",
	25: "Wall Leftslingshot (mean of its drag points)", 26: "Wall Rightslingshot (mean of its drag points)",
	27: "HitTarget sw27", 28: "HitTarget sw28", 32: "Kicker sw32", 33: "Kicker sw33", 34: "Kicker sw34", 35: "Kicker sw35",
	36: "Kicker KickToGlove", 38: "Wall sw38 (mean of its drag points)", 41: "Trigger sw41", 42: "Trigger sw42",
	43: "Wall sw43 (mean of its drag points)", 44: "Bumper Bumper1", 45: "Bumper Bumper2", 46: "Bumper Bumper3",
	47: "Trigger sw47", 48: "Spinner sw48", 51: "Kicker Matrix11", 52: "Kicker Matrix21", 53: "Kicker Matrix31",
	54: "Trigger sw54", 55: "Trigger sw55", 56: "Trigger sw56", 57: "Trigger sw57", 58: "Trigger sw58",
	61: "Kicker Matrix12", 62: "Kicker Matrix22", 63: "Kicker Matrix32", 64: "Trigger sw64", 65: "Trigger sw65",
	66: "Trigger sw66", 71: "Kicker Matrix13", 72: "Kicker Matrix23", 73: "Kicker Matrix33", 78: "Trigger sw78",
}
SWITCH_PROJECTIONS = {
	31: (
		"Projected onto the trough eject kicker (Kicker sw32, the Trough Ball 1 position): the retained table models no Trough Jam "
		"object and its SolRelease pulses 31 on every eject, while the manual's switch drawing puts callout 31 at the shooter end of "
		"the trough beyond callout 32."
	),
}
OBSERVED_SWITCHES = {31}

SOLENOID_LABELS = {
	1: "Trough Eject", 2: "Autoplunger", 3: "Popper", 5: "Clear Matrix", 6: "Hand Magnet", 7: "Knocker",
	9: "Left Slingshot", 10: "Right Slingshot", 11: "Left Jet Bumper", 12: "Bottom Jet Bumper", 13: "Right Jet Bumper",
	14: "Crazy Bob's Eject", 15: "Drop Target Up", 16: "Drop Target Down", 17: "Jets Flasher",
	18: "Crazy Bob's Flasher", 19: "Left Slingshot Flasher", 20: "Right Slingshot Flasher",
	21: "X Motor Direction", 22: "X Motor Enable", 23: "Y Motor Direction", 24: "Y Motor Enable",
	25: "Left Ramp Flasher", 26: "Right Ramp Flasher", 27: "Hand Popper Flasher", 28: "Right Back Panel Flasher",
	33: "Left Diverter Power", 34: "Left Diverter Hold", 35: "Right Diverter Power", 36: "Right Diverter Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
UNUSED_SOLENOIDS = {4: ("Q76", "Vio-Yel"), 8: ("Q70", "Vio-Gry")}
FLASHERS = {17, 18, 19, 20, 25, 26, 27, 28}
MOTOR_CONTROLS = {21, 22, 23, 24}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "WPC Game-On State", 32: "Unused WPC State Channel 32",
	37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40",
	41: "Unused WPC-Security Output 41", 42: "Unused WPC-Security Output 42",
	43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# address -> (printed type, voltage connection, transistor, drive connection, drive wire, part/lamp)
SOLENOID_WIRING = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "Vio-Brn", "AE-26-1500"),
	2: ("High Power", "J107-2", "Q80", "J130-2", "Vio-Red", "AE-23-800"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "Vio-Org", "AE-24-900"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "Vio-Grn", "AE-25-1000"),
	6: ("High Power", "J107-2", "Q66", "J130-7", "Vio-Blu", "20-10201"),
	7: ("High Power", "J107-2 (Backbox)", "Q68", "J130-8 (Backbox)", "Vio-Blk", "AE-23-800"),
	9: ("Low Power", "J107-3", "Q58", "J127-1", "Brn-Blk", "AE-26-1200"),
	10: ("Low Power", "J107-3", "Q56", "J127-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "Brn-Org", "AE-26-1200"),
	12: ("Low Power", "J107-3", "Q52", "J127-5", "Brn-Yel", "AE-26-1200"),
	13: ("Low Power", "J107-3", "Q50", "J127-6", "Brn-Grn", "AE-26-1200"),
	14: ("Low Power", "J107-3", "Q48", "J127-7", "Brn-Blu", "AE-26-1500"),
	15: ("Low Power", "J107-3", "Q46", "J127-8", "Brn-Vio", "AE-26-1200"),
	16: ("Low Power", "J107-3", "Q44", "J127-9", "Brn-Gry", "SM1-26-600"),
	17: ("Flasher", "J107-6", "Q42", "J126-1", "Blk-Brn", "#89"),
	18: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q40", "J126-2 (Playfield) / J125-2 (Backbox)", "Blk-Red", "#906"),
	19: ("Flasher", "J107-6", "Q38", "J126-3", "Blk-Org", "#906"),
	20: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q36", "J126-4 (Playfield) / J125-5 (Backbox)", "Blk-Yel", "#906"),
	21: ("Flasher", "J107-6", "Q28", "J126-5", "Blu-Grn", "A-20532"),
	22: ("Flasher", "J107-6", "Q30", "J126-6", "Blu-Blk", "A-20532"),
	23: ("Flasher", "J107-6", "Q34", "J126-7", "Blu-Vio", "A-20532"),
	24: ("Flasher", "J107-6", "Q32", "J126-8", "Blu-Gry", "A-20532"),
	25: ("Gen. Purpose", "J107-6 (Playfield) / J106-5 (Backbox)", "Q26", "J122-1 (Playfield) / J124-1 (Backbox)", "Blu-Brn", "#906"),
	26: ("Gen. Purpose", "J107-6", "Q24", "J122-2", "Blu-Red", "#906"),
	27: ("Gen. Purpose", "J107-6", "Q22", "J122-3", "Blu-Org", "#89"),
	28: ("Gen. Purpose", "J107-6 (Playfield) / J106-5 (Backbox)", "Q20", "J122-4 (Playfield) / J124-5 (Backbox)", "Blu-Yel", "#906"),
	33: ("Fliptronic power", "J907-6 (Red-Vio)", "Q2", "J902-6", "Yel-Vio", "FL-11753"),
	34: ("Fliptronic hold", "J907-6 (Red-Vio)", "Q7", "J902-4", "Org-Vio", "FL-11753"),
	35: ("Fliptronic power", "J907-8 (Red-Gry)", "Q1", "J902-3", "Yel-Gry", "FL-11753"),
	36: ("Fliptronic hold", "J907-8 (Red-Gry)", "Q5", "J902-1", "Org-Gry", "FL-11753"),
	45: ("Fliptronic power", "J907-1 (Red-Grn)", "Q4", "J902-13", "Yel-Grn", "FL-11629"),
	46: ("Fliptronic hold", "J907-1 (Red-Grn)", "Q11", "J902-11", "Org-Grn", "FL-11629"),
	47: ("Fliptronic power", "J907-4 (Red-Blu)", "Q3", "J902-9", "Yel-Blu", "FL-11629"),
	48: ("Fliptronic hold", "J907-4 (Red-Blu)", "Q9", "J902-7", "Org-Blu", "FL-11629"),
}
# Printed flipper-circuit numbers (manual.address aliases) for the public Fliptronic addresses.
PRINTED_FLIPPER_CIRCUITS = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
SOLENOID_ASSEMBLIES = {
	1: "A-19963", 2: "A-14525", 3: "A-20498", 5: "A-20446", 6: "A-20500", 7: "A-10686-1", 9: "B-9362-L-2",
	10: "B-9362-R-3", 11: "A-9415-2", 12: "A-9415-2", 13: "A-9415-2", 14: "A-20496", 15: "A-20587", 16: "A-20587",
	17: "A-17803", 18: "A-17802", 21: "A-20532", 22: "A-20532", 23: "A-20532", 24: "A-20532", 27: "04-10280",
	33: "A-20497", 34: "A-20497", 35: "A-20497", 36: "A-20497", 45: "A-19223-R", 46: "A-19223-R",
	47: "A-15849-L-2", 48: "A-15849-L-2",
}
SOLENOID_CALLBACKS = {
	1: "SolRelease (kicks the ball on Kicker sw32 into the shooter lane and pulses switch 31)",
	2: "SolAutofire (fires the impulse plunger PlungerIM on Trigger swplunger)",
	3: "SolKickToGlove (kicks the ball on KickToGlove straight up to the hand)",
	5: "DoClearMatrix (kicks every ball held in the nine Matrix kickers out of the matrix)",
	6: "DoHandMagnet (holds the ball under the hand and picks up a matrix ball below it)",
	7: "vpmSolSound Knocker",
	14: "CrazyBobKick (kicks the ball on sw47 up out of the eject)",
	15: "ResetDrop (raises drop target 43)",
	16: "DropTargetDown (drops target 43)",
	17: "Flash117 (SolModCallBack)", 18: "Flash118 (SolModCallBack)", 19: "Flash119 (SolModCallBack)",
	20: "Flash120 (SolModCallBack)", 25: "Flash125 (SolModCallBack)", 26: "Flash126 (SolModCallBack)",
	27: "Flash127 (SolModCallBack)", 28: "Flash128 (SolModCallBack)",
	21: "the cvpmMech MoveGloveX (Sol2 = -21, the direction)", 22: "the cvpmMech MoveGloveX (Sol1 = 22, the enable)",
	23: "the cvpmMech MoveGloveY (Sol2 = -23, the direction)", 24: "the cvpmMech MoveGloveY (Sol1 = 24, the enable)",
	34: "SolLeftDiverterHold (swaps the LeftDiverterOpen/LeftDiverterClosed walls and swings diverter01)",
	36: "SolRightDiverterHold (swaps the RightDiverterOpen/RightDiverterClosed walls and swings diverter02)",
	46: "SolRFlipper through SolCallback(sLRFlipper)",
	48: "SolLFlipper through SolCallback(sLLFlipper)",
}
SOLENOID_POSITIONS = {
	1: [(0.847395, 0.870418)], 2: [(0.937757, 0.897982)], 3: [(0.373924, 0.100777)],
	6: [(0.369153, 0.09882)], 9: [(0.22369, 0.73513)], 10: [(0.679548, 0.735172)], 11: [(0.176482, 0.240365)],
	12: [(0.223952, 0.317187)], 13: [(0.385499, 0.268581)], 14: [(0.420812, 0.32717)], 15: [(0.443696, 0.112586)],
	16: [(0.443696, 0.112586)], 33: [(0.189408, 0.073588)], 34: [(0.189408, 0.073588)],
	35: [(0.400812, 0.061334)], 36: [(0.400812, 0.061334)],
	45: [(0.621899, 0.84515)], 46: [(0.621899, 0.84515)], 47: [(0.283577, 0.845095)], 48: [(0.283577, 0.845095)],
}
SOLENOID_OBJECTS = {
	1: "Kicker sw32 (Trough Ball 1, the eject position)", 2: "Trigger swplunger (the impulse plunger's trigger)",
	3: "Kicker KickToGlove", 6: "Kicker GloveMag (where the retained table's hand catches the popper ball, beside Kicker KickToGlove)",
	9: "Wall Leftslingshot (mean of its drag points)", 10: "Wall Rightslingshot (mean of its drag points)",
	11: "Bumper Bumper1", 12: "Bumper Bumper2", 13: "Bumper Bumper3", 14: "Trigger sw47", 15: "Wall sw43 (mean of its drag points)",
	16: "Wall sw43 (mean of its drag points)", 33: "Wall LeftDiverterOpen (mean of its drag points; the wall the table raises with the coil off)",
	34: "Wall LeftDiverterOpen (mean of its drag points; the wall the table raises with the coil off)",
	35: "Wall RightDiverterOpen (mean of its drag points; the wall the table raises with the coil off)",
	36: "Wall RightDiverterOpen (mean of its drag points; the wall the table raises with the coil off)",
	45: "Flipper RightFlipper", 46: "Flipper RightFlipper", 47: "Flipper LeftFlipper", 48: "Flipper LeftFlipper",
}
SOLENOID_PROJECTIONS = {
	6: (
		"Hand Magnet projected onto Kicker GloveMag, where the retained table's hand catches the ball the popper (Kicker "
		"KickToGlove) shoots up: the magnet rides the moving hand. Service Bulletin SB 85's troubleshooting asks the "
		"technician to verify that the magnet is positioned approximately over the ball popper when it fails to catch."
	),
}
# Coil callouts measured on the solenoid/flashlamp location drawing through the same affine fit as
# the flashers.
DRAWING_COIL_POSITIONS = {
	5: ((0.828, 0.038), "the end of callout 05's leader, on the coil drawn at the right rear corner of the matrix"),
}
# Flasher sockets measured on the solenoid/flashlamp location drawing (printed 2-37) through the
# least-squares affine fit in external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py.
DRAWING_FLASHER_POSITIONS = {
	17: ((0.282, 0.259), "the plain dome circle drawn between the two upper jet bumpers"),
	18: ((0.471, 0.312), "the end of callout 18's leader at the upper right corner of the Crazy Bob's eject box"),
	19: ((0.197, 0.75), "the dome circle drawn inside the left slingshot"),
	20: ((0.705, 0.755), "the dome circle drawn inside the right slingshot"),
	26: ((0.936, 0.201), "the dome circle drawn at the right of the upper playfield, beside the right loop"),
	27: ((0.237, 0.078), "the end of callout 27's leader in the popper mechanism at the rear left"),
	28: ((0.941, 0.049), "the end of callout 28's leader at the right end of the back panel"),
	25: ((0.061, 0.287), "the centre of the unlabelled plain dome circle drawn at the far left beside the jet bumpers"),
}
# Distance from each drawing measurement to the glow sprite F1nn that the 2020 archive table (Alessio)
# drives from the same solenoid, both normalized in their own table frames (the fit output lists them).
ARCHIVE_GLOW_DISTANCES = {17: 0.005, 18: 0.076, 19: 0.021, 20: 0.008, 25: 0.021, 26: 0.044, 27: 0.096, 28: 0.009}
EXTRAPOLATED_FLASHERS = {25, 26, 28}

# --- Lamp matrix (manual printed 2-32).
LAMP_LABELS = {
	11: "Mode Ready", 12: "Download", 13: "Access Code 2", 14: "Access Code 1", 15: "Upload", 16: "Left Jet Lane",
	17: "Middle Jet Lane", 18: "Right Jet Lane",
	21: "Power Down", 22: "N.A.S. Cure", 23: "Right Ramp Block 4", 24: "Sector 6", 25: "Right Ramp Block 2",
	26: "Hold Bonus", 27: "Right Standup Right Block", 28: "Right Standup Left Block",
	31: "Left Ramp Block 4", 32: "Extra Ball", 33: "Sector 2", 34: "Left Ramp Block 2", 35: "Left Ramp Block 1",
	36: "Sector 1", 38: "Shoot Again",
	41: "Left Loop Top Arrow", 42: "Left Standup Arrow", 43: "Right Ramp Block 1", 44: "Light Spinner",
	45: "Big Points", 46: "Gigabytes", 47: "Light Extra Ball", 48: "Quick Multiball",
	51: "Cyber Matrix 13", 52: "Cyber Matrix 23", 53: "Cyber Matrix 33", 54: "Right Outlane", 55: "Bonus Held",
	56: "Bonus 4X", 57: "Bonus 3X", 58: "Bonus 2X",
	61: "Cyber Matrix 12", 62: "Cyber Matrix 22", 63: "Cyber Matrix 32", 64: "Right Return Lane", 65: "Sector 5",
	66: "Spinner Millions", 67: "Cyber Lock 2", 68: "Inner Loop Top",
	71: "Cyber Matrix 11", 72: "Cyber Matrix 21", 73: "Cyber Matrix 31", 74: "Popper Top Arrow", 75: "Sector 3",
	76: "Crazy Bob's", 77: "Mode Start", 78: "Cyber Lock 1",
	81: "Right Loop Top Arrow", 82: "Cyber Lock 3", 83: "Sector 7", 84: "Left Outlane", 85: "Left Return Lane",
	86: "Ball Launch", 87: "Buy-In Button", 88: "Start Button",
}
UNUSED_LAMPS = {37}
LAMP_BULBS = {address: "#44" for address in (38, 54, 64, 84, 85)}
LAMP_ASSEMBLIES = {
	**{address: "A-20454" for address in (11, 12, 13, 14, 15, 21, 22)},
	**{address: "A-20108" for address in (16, 17, 18)},
	**{address: "A-20456" for address in (23, 24, 25, 26, 27, 28, 43, 44, 45, 46, 47, 48)},
	**{address: "A-20455" for address in (31, 32, 33, 34, 35, 36, 41, 42)},
	**{address: "A-17835" for address in (38, 54, 64, 84, 85)},
	**{address: "04-10277" for address in (51, 52, 53, 61, 62, 63, 71, 72, 73)},
	**{address: "A-20174" for address in (55, 56, 57, 58)},
	**{address: "A-20457" for address in (65, 66, 67, 68, 74, 75, 76, 77, 78)},
	**{address: "A-20458" for address in (81, 82, 83)},
	86: "20-9663-B-4", 87: "20-663-21", 88: "20-9663-2",
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
LAMP_POSITIONS = {
	11: (0.451106, 0.746463), 12: (0.520791, 0.764947), 13: (0.452677, 0.786257), 14: (0.38091, 0.764884),
	15: (0.3337, 0.753692), 16: (0.207079, 0.124687), 17: (0.302235, 0.13215), 18: (0.393566, 0.141105),
	21: (0.45073, 0.711672), 22: (0.572833, 0.753691), 23: (0.675795, 0.415223), 24: (0.652951, 0.438693),
	25: (0.687355, 0.459681), 26: (0.705246, 0.492199), 27: (0.853627, 0.539403), 28: (0.809663, 0.52424),
	31: (0.349014, 0.52944), 32: (0.238618, 0.5721), 33: (0.36878, 0.555759), 34: (0.426156, 0.559918),
	35: (0.329887, 0.57328), 36: (0.267344, 0.615032), 38: (0.451871, 0.873683),
	41: (0.206452, 0.521068), 42: (0.137631, 0.558198), 43: (0.594875, 0.442607), 44: (0.586801, 0.514688),
	45: (0.623637, 0.541222), 46: (0.691078, 0.542737), 47: (0.732449, 0.522269), 48: (0.634972, 0.48942),
	51: (0.639004, 0.129972), 52: (0.71473, 0.129972), 53: (0.786307, 0.129972), 54: (0.851472, 0.728329),
	55: (0.661632, 0.592583), 56: (0.635848, 0.622695), 57: (0.610641, 0.651946), 58: (0.58728, 0.680805),
	61: (0.639004, 0.097132), 62: (0.71473, 0.097132), 63: (0.786307, 0.097132), 64: (0.775468, 0.688782),
	65: (0.57371, 0.405821), 66: (0.589227, 0.361093), 67: (0.61337, 0.301983), 68: (0.633832, 0.249505),
	71: (0.639004, 0.06383), 72: (0.71473, 0.06383), 73: (0.786307, 0.06383), 74: (0.518967, 0.203041),
	75: (0.463041, 0.412373), 76: (0.444884, 0.360898), 77: (0.516768, 0.303193), 78: (0.517295, 0.252197),
	81: (0.871391, 0.354005), 82: (0.82802, 0.403468), 83: (0.788027, 0.446913), 84: (0.05117, 0.755168),
	85: (0.126002, 0.689079),
}
LAMP_CONNECTOR_NOTE = (
	" Connectors follow the lamp matrix page; the power driver board connector list (printed 3-30/3-31) instead puts the "
	"playfield rows on J134 and the columns on J138 and marks J133 and J137 Not Used, with the same wire colours."
)
# Nine matrix lamps: which matrix hole kicker each sits under (the label, not the number, pairs them).
MATRIX_LAMP_HOLES = {51: 71, 52: 72, 53: 73, 61: 61, 62: 62, 63: 63, 71: 51, 72: 52, 73: 53}

# (label, 6.8Vac feed, feed wire, triac, switched return, return wire, printed lamps). The connector
# list (printed 3-30) and the G.I. circuit (printed 3-10) show the triac switching the return pin; the
# solenoid table prints the returns under "Voltage Connections" and the feeds under the drive columns.
GI_STRINGS = {
	0: ("String 1", "J121-7 (Playfield) / J120-7 (Backbox)", "White-Brown", "Q18", "J121-1 (Playfield) / J120-1 (Backbox)", "Brown", "#44 playfield, #555 backbox"),
	1: ("String 2", "J121-8 (Playfield) / J120-8 (Backbox)", "White-Orange", "Q10", "J121-2 (Playfield) / J120-2 (Backbox)", "Orange", "#44 playfield, #555 backbox"),
	2: ("String 3", "J121-9 (Playfield) / J120-9 (Backbox)", "White-Yellow", "Q14", "J121-3 (Playfield) / J120-3 (Backbox)", "Yellow", "#44 playfield, #555 backbox"),
	3: ("String 4", "J121-10 (Playfield)", "White-Green", "Q16", "J121-5 (Playfield)", "Green", "#44 playfield"),
	4: ("String 5", "J120-11 (Backbox) / J119-1 (Cabinet)", "White-Violet", "Q12", "J120-6 (Backbox) / J119-3 (Cabinet)", "Violet", "#555 backbox"),
}
GI_COLLECTIONS = {0: "GIString1", 1: "GIString2", 2: "GIString3"}
GI_POSITIONS = {
	0: [
		(0.691818, 0.824338), (0.691413, 0.765101), (0.860572, 0.466277), (0.761617, 0.325188), (0.077028, 0.512886),
		(0.2318, 0.373803), (0.426855, 0.219043), (0.439021, 0.188615), (0.121911, 0.194193), (0.924476, 0.101077),
	],
	1: [
		(0.213867, 0.824701), (0.146994, 0.804855), (0.756134, 0.803203), (0.720391, 0.724885), (0.875926, 0.491633),
		(0.04641, 0.410373), (0.172193, 0.289508), (0.346276, 0.180434), (0.58369, 0.142526), (0.059183, 0.06013),
		(0.386983, 0.269666),
	],
	2: [
		(0.212305, 0.765404), (0.183037, 0.72481), (0.88887, 0.611733), (0.043127, 0.572262), (0.070844, 0.47258),
		(0.262922, 0.418641), (0.69612, 0.311818), (0.709041, 0.283673), (0.253676, 0.171655), (0.514509, 0.096093),
		(0.223895, 0.317724), (0.175678, 0.240579),
	],
}
GI_MEMBERS = {
	0: "l140a-l140j",
	1: "l141a-l141k (l141k sits in the right jet bumper)",
	2: "l142a-l142l (l142k and l142l sit in the bottom and left jet bumpers)",
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _text_sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Johnny Mnemonic retained extraction is missing: {extraction_root}")
	paths = sorted(
		(path for path in extraction_root.rglob("*") if path.is_file()),
		key=lambda path: path.relative_to(extraction_root).as_posix(),
	)
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [
			{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)}
			for path in paths
		],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Johnny Mnemonic extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Johnny Mnemonic retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Johnny Mnemonic retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Johnny Mnemonic retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


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
				"x": x,
				"y": y,
				"provenance": provenance(*source_refs, status=status),
			}
		)
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# (excerpt id suffix, locator, image derivation or None); the transcription defaults to <suffix>.md.
MANUAL_EXCERPTS = (
	("dip-switch-chart", "PDF page 2, quick-reference sheet DIP SWITCH SETTINGS AND JUMPERS", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 2, crop box 0.11,0.05,0.9,0.29, scanned page rendered at its native resolution (embedded image xref 5, 2550px across 8.50in), rendered at 134 dpi, capped to 900px wide, grayscale, 901x355 WebP quality 80"),
	("lamp-matrix", "PDF page 100, printed page 2-32, Lamp Matrix", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 100, crop box 0.12,0.015,0.85,0.53, scanned page rendered at its native resolution (embedded image xref 495, 2550px across 8.50in), rendered at 148 dpi, capped to 920px wide, grayscale, 921x841 WebP quality 80"),
	("lamp-locations", "PDF page 101, printed page 2-33, Lamp Locations parts list", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 101, crop box 0.11,0.06,0.5,0.77, scanned page rendered at its native resolution (embedded image xref 500, 2550px across 8.50in), rendered at 139 dpi, capped to 460px wide, grayscale, 461x1085 WebP quality 80"),
	("switch-matrix", "PDF page 102, printed page 2-34, Switch Matrix", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 102, crop box 0.09,0.025,0.89,0.545, scanned page rendered at its native resolution (embedded image xref 505, 2550px across 8.50in), rendered at 112 dpi, capped to 760px wide, grayscale, 761x641 WebP quality 80"),
	("switch-locations", "PDF page 103, printed page 2-35, Switch Locations parts list", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 103, crop box 0.13,0.075,0.47,0.755, scanned page rendered at its native resolution (embedded image xref 510, 2550px across 8.50in), rendered at 159 dpi, capped to 460px wide, grayscale, 461x1191 WebP quality 80"),
	("switch-locations-drawing", "PDF page 103, printed page 2-35, Switch Locations drawing with the Cyber Space Assy. inset", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 103, crop box 0.48,0.07,0.99,0.66, scanned page rendered at its native resolution (embedded image xref 510, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1301x1947 WebP quality 80"),
	("solenoid-flasher-table", "PDF page 104, printed page 2-36, Solenoid/Flasher Table rows 01-28", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 104, crop box 0.09,0.03,0.89,0.418, scanned page rendered at its native resolution (embedded image xref 515, 2550px across 8.50in), rendered at 115 dpi, capped to 780px wide, grayscale, 781x491 WebP quality 80"),
	("gi-and-flipper-circuits", "PDF page 104, printed page 2-36, Solenoid/Flasher Table General Illumination and Flipper Circuits blocks and footnotes", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 104, crop box 0.09,0.415,0.89,0.67, scanned page rendered at its native resolution (embedded image xref 515, 2550px across 8.50in), rendered at 162 dpi, capped to 1100px wide, grayscale, 1101x455 WebP quality 80"),
	("solenoid-flasher-locations", "PDF page 105, printed page 2-37, Solenoid/Flashlamp Locations parts list", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 105, crop box 0.09,0.06,0.55,0.73, scanned page rendered at its native resolution (embedded image xref 520, 2550px across 8.50in), rendered at 174 dpi, capped to 680px wide, grayscale, 681x1283 WebP quality 80"),
	("solenoid-flasher-locations-drawing", "PDF page 105, printed page 2-37, Solenoid/Flashlamp Locations drawing", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 105, crop box 0.52,0.1,0.995,0.71, scanned page rendered at its native resolution (embedded image xref 520, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1212x2013 WebP quality 80"),
	("diverter-assembly", "PDF page 90, printed page 2-22, A-20497 Diverter Assembly", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 90, crop box 0.1,0.08,0.95,0.88, scanned page rendered at its native resolution (embedded image xref 445, 2550px across 8.50in), rendered at 300 dpi, grayscale, 2168x2640 WebP quality 80"),
	("hand-popper-assembly", "PDF page 91, printed page 2-23, A-20498 Hand Popper Assembly", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 91, crop box 0.12,0.08,0.95,0.84, scanned page rendered at its native resolution (embedded image xref 450, 2550px across 8.50in), rendered at 300 dpi, grayscale, 2117x2508 WebP quality 80"),
	("cyber-space-assembly", "PDF page 93, printed page 2-25, A-20447 Cyber Space Assembly", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 93, crop box 0.14,0.08,0.98,0.9, scanned page rendered at its native resolution (embedded image xref 460, 2550px across 8.50in), rendered at 300 dpi, grayscale, 2142x2706 WebP quality 80"),
	("crazy-bobs-eject-assembly", "PDF page 89, printed page 2-21, A-20496 Crazy Bob's Eject Assembly", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 89, crop box 0.12,0.04,0.97,0.9, scanned page rendered at its native resolution (embedded image xref 440, 2550px across 8.50in), rendered at 125 dpi, capped to 900px wide, grayscale, 901x1180 WebP quality 80"),
	("drop-target-assembly", "PDF page 92, printed page 2-24, A-20587 Drop Target Assembly", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 92, crop box 0.04,0.575,0.97,0.89, scanned page rendered at its native resolution (embedded image xref 455, 2550px across 8.50in), rendered at 127 dpi, capped to 1000px wide, grayscale, 1001x439 WebP quality 80"),
	("hand-assembly", "PDF page 94, printed page 2-26, A-20500 Hand Assembly parts list", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 94, crop box 0.12,0.1,0.96,0.64, scanned page rendered at its native resolution (embedded image xref 465, 2550px across 8.50in), rendered at 109 dpi, capped to 780px wide, grayscale, 781x650 WebP quality 80"),
	("dual-relay-motor-driver", "PDF page 128, printed page 3-20, A-20532 Dual Relay Motor Driver Assembly connector list", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 128, crop box 0.12,0.06,0.98,0.25, scanned page rendered at its native resolution (embedded image xref 635, 2550px across 8.50in), rendered at 150 dpi, capped to 1100px wide, grayscale, 1101x315 WebP quality 80"),
	("hand-motors-circuit", "PDF page 129, printed page 3-21, A-20533 Position Encoder Board Assembly and Hand Motors Circuit", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 129, crop box 0.12,0.08,0.99,0.88, scanned page rendered at its native resolution (embedded image xref 640, 2550px across 8.50in), rendered at 300 dpi, grayscale, 2219x2640 WebP quality 80"),
	("power-driver-connectors-3-29", "PDF page 137, printed page 3-29, power driver board connectors J106 and J107", None),
	("power-driver-connectors-3-30-left", "PDF page 138, printed page 3-30, power driver board connectors J119-J123", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 138, crop box 0.09,0.395,0.52,0.78, scanned page rendered at its native resolution (embedded image xref 685, 2550px across 8.50in), rendered at 192 dpi, capped to 700px wide, grayscale, 701x812 WebP quality 80"),
	("power-driver-connectors-3-30-right", "PDF page 138, printed page 3-30, power driver board connectors J124-J126", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 138, crop box 0.49,0.045,0.97,0.395, scanned page rendered at its native resolution (embedded image xref 685, 2550px across 8.50in), rendered at 172 dpi, capped to 700px wide, grayscale, 701x662 WebP quality 80"),
	("power-driver-connectors-3-30-lamp-rows", "PDF page 138, printed page 3-30, power driver board connectors J133-J134", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 138, crop box 0.49,0.72,0.97,0.855, scanned page rendered at its native resolution (embedded image xref 685, 2550px across 8.50in), rendered at 172 dpi, capped to 700px wide, grayscale, 701x256 WebP quality 80"),
	("power-driver-connectors-3-31", "PDF page 139, printed page 3-31, power driver board connectors J135-J138", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 139, crop box 0.12,0.07,0.56,0.39, scanned page rendered at its native resolution (embedded image xref 690, 2550px across 8.50in), rendered at 187 dpi, capped to 700px wide, grayscale, 701x659 WebP quality 80"),
	("gi-circuit", "PDF page 118, printed page 3-10, General Illumination Circuit and its block diagram", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 118, crop box 0.14,0.07,0.9,0.8, scanned page rendered at its native resolution (embedded image xref 585, 2550px across 8.50in), rendered at 139 dpi, capped to 900px wide, grayscale, 901x1120 WebP quality 80"),
	("flashlamp-wiring", "PDF page 115, printed page 3-7, Playfield Flashlamps and Backbox Flashlamps wiring", "Williams_1995_Johnny_Mnemonic_English_Manual.pdf page 115, crop box 0.12,0.07,0.9,0.9, scanned page rendered at its native resolution (embedded image xref 570, 2550px across 8.50in), rendered at 136 dpi, capped to 900px wide, grayscale, 901x1240 WebP quality 80"),
	("game-rules", "PDF pages 13-18, rules section: Cyberspace Matrix Shots, Skill Shot, Mnemonic Recovery, Access Jet Bumpers, Video Mode, Cyberspace Multiball and Powerdown Multiball paragraphs", None),
)
# Several crops share one transcription.
EXCERPT_TRANSCRIPTIONS = {
	"switch-locations-drawing": "switch-locations.md",
	"gi-and-flipper-circuits": "solenoid-flasher-table.md",
	"solenoid-flasher-locations-drawing": "solenoid-flasher-locations.md",
	"diverter-assembly": "diverter-and-popper-assemblies.md",
	"hand-popper-assembly": "diverter-and-popper-assemblies.md",
	"dual-relay-motor-driver": "hand-motor-circuits.md",
	"hand-motors-circuit": "hand-motor-circuits.md",
	"power-driver-connectors-3-29": "power-driver-connectors.md",
	"power-driver-connectors-3-30-left": "power-driver-connectors.md",
	"power-driver-connectors-3-30-right": "power-driver-connectors.md",
	"power-driver-connectors-3-30-lamp-rows": "power-driver-connectors.md",
	"power-driver-connectors-3-31": "power-driver-connectors.md",
}


def _excerpts(entries: tuple[tuple[str, str, str | None], ...]) -> list[dict[str, Any]]:
	records = []
	for suffix, locator, derivation in entries:
		transcription = EXCERPT_TRANSCRIPTIONS.get(suffix, f"{suffix}.md")
		record: dict[str, Any] = {
			"id": f"excerpt.johnny-mnemonic.{suffix}",
			"locator": locator,
			"path": f"{EXCERPT_PREFIX}/{transcription}",
			"sha256": _text_sha256(EXCERPT_DIRECTORY / transcription),
		}
		if derivation is not None:
			record["image"] = f"{EXCERPT_PREFIX}/{suffix}.webp"
			record["image_sha256"] = _file_sha256(EXCERPT_DIRECTORY / f"{suffix}.webp")
			record["image_derivation"] = derivation
		record.update({"method": "manual", "transcribed_by": "curator, read from the native-resolution render", "reviewed": True})
		records.append(record)
	return records


def _bulletin_excerpt(suffix: str = "service-bulletins") -> list[dict[str, Any]]:
	return [
		{
			"id": f"excerpt.johnny-mnemonic.{suffix}",
			"locator": "Quoted statements from Service Bulletins SB 85 and SB 87 and Manual Addenda 1 and 2",
			"path": f"{EXCERPT_PREFIX}/service-bulletins.md",
			"sha256": _text_sha256(EXCERPT_DIRECTORY / "service-bulletins.md"),
			"method": "manual",
			"transcribed_by": "curator, quoted from the text layer read with Poppler pdftotext",
			"reviewed": True,
		}
	]


def _bulletin(identifier: str, filename: str, capture: str, sha256: str, locator: str, excerpts: bool) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier,
		"kind": "service_bulletin",
		"uri": f"{WAYBACK_PREFIX}{capture}id_/{IPDB_FILES}{filename}",
		"original_filename": filename,
		"sha256": sha256,
		"acquired_at": ACQUIRED_AT,
		"locator": locator,
		"license": "NOASSERTION",
		"attribution": "WMS Games Parts & Service Inc.; hosted by the Internet Pinball Machine Database, retrieved from the Internet Archive's Wayback Machine",
		"rights": "NOASSERTION",
	}
	if excerpts:
		record["excerpts"] = _bulletin_excerpt("service-bulletins" if identifier == SB85_SOURCE else "service-bulletin-87")
	return record


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames records for jm_12r, jm_12b and jm_05r",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/jm.c: CORE_GAMEDEF(jm,12r) and CORE_CLONEDEF(jm,12b/05r) all with wpc_mSecurityS; "
				"jmGameData GEN_WPCSECURITY with wpc_dispDMD, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L)|FLIP_BUT(FLIP_L|FLIP_U), the "
				"inverted-switch mask {0x00,0x00,0x00,0x3f,0x00,0x00,0x00,0x78,0x00,0x00,0x00,0x00}, no custom solenoids, no "
				"wpc_set_fastflip_addr call; jm_handleMech (called by core.c only while mechanics handling is non-zero) copies public "
				"116 to 67 and 118 to 68, reads the hand motor lines from WPC_SOLENOID3 >> 4 (bit 0 = 21 X direction, bit 1 = 22 X "
				"enable, bit 2 = 23 Y direction, bit 3 = 24 Y enable), and with mechanics bits 0 and 1 steps a hand position and "
				"drives the home switches 12 and 37 (position < 1) and quadrature encoders 74/75 and 77/76; init_jm starts the hand "
				"at -64/-300. The *** PRELIMINARY *** simulator's #define block and jm_stateDef are cross-reference only. "
				"src/wpc/wpc.c: the jm_ output typing marks 17-20 and 25-28 as #89 20V DC bulbs. src/wpc/core.h/core.c: "
				"CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, core_getSol (29-31 J111/game-on remap, 33-36 raw bits because "
				"FLIP_SOL covers only the lower flippers, 37-44 zero outside WPC-95/System 11, 45-48 lower flippers), and "
				"core_updateSw's flipper mask (the lower EOS bits 111/113 recomputed from the coils, the four button bits carried "
				"through when keyboard handling is off). src/libpinmame/libpinmame.cpp: g_fHandleMechanics defaults to 0."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-security.json",
			"revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp and five-string G.I. address rules",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": f"{WAYBACK_PREFIX}20241009041944id_/{IPDB_FILES}Williams_1995_Johnny_Mnemonic_English_Manual.pdf",
			"original_filename": "Williams_1995_Johnny_Mnemonic_English_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": ACQUIRED_AT,
			"locator": (
				"142-page image-only Williams Johnny Mnemonic operations manual (September 1995; cover part numbers 50042), IPDB machine "
				"3683 (https://www.ipdb.org/machine.cgi?id=3683: Williams 'Johnny Mnemonic', August 08, 1995, model 50042, MPU Williams "
				"WPC Security (WPC-S), 2,756 units; page retained from Wayback capture 20241009040904). The PDF is IPDB's 'English Manual' "
				"file, retrieved from its Wayback Machine capture because IPDB is Cloudflare-gated. Scan at 300 dpi; PDF page = printed "
				"1-N + 20, 2-N + 68, 3-N + 108. Used: quick-reference DIP chart (PDF 2), rules (PDF 13-18), Section 2 printed 2-21 to "
				"2-26 (Crazy Bob's eject, diverter, hand popper, drop target, cyber space and hand assemblies) and 2-32 to 2-37 (lamp matrix/locations, switch "
				"matrix/locations, solenoid table and locations), Section 3 printed 3-20/3-21 (dual relay motor driver, position "
				"encoder, hand motors circuit), 3-7 (flashlamp wiring), 3-10 (G.I. circuit) and 3-29 to 3-31 (power driver board connector list). A local Windows.Media.Ocr text layer (external:pinmame-manuals/by-machine/"
				"williams.johnny-mnemonic.1995/ocr-windows) was used only to find pages; every cited cell was read from the render."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Machine Database, retrieved from the Internet Archive's Wayback Machine",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(MANUAL_EXCERPTS),
		},
		_bulletin(
			SB85_SOURCE, "Williams_1995_Johnny_Mnemonic_Service_Bulletin_85.pdf", "20241009065237", SB85_SHA256,
			"Service Bulletin SB 85, November 9, 1995, 'Manual Amendment', three pages: LED 2/3 unused, and the Data Glove "
			"troubleshooting text (ball catcher magnet, Ball in Hand switch, X/Y drives with home switches and encoders).",
			True,
		),
		_bulletin(
			SB87_SOURCE, "Williams_1995_Johnny_Mnemonic_Service_Bulletin_87.pdf", "20241009043310", SB87_SHA256,
			"Service Bulletin SB 87, March 19, 1996, two pages: moving the hand electromagnet supply from fuse F104 to F103, through the "
			"6-pin connector that comes off the back panel assembly at the back of the playfield.",
			True,
		),
		_bulletin(
			ADDENDUM1_SOURCE, "Williams_1995_Johnny_Mnemonic_Manual_Addendum_1.pdf", "20241009093924", ADDENDUM1_SHA256,
			"Manual Addendum 1, October 13, 1995, two pages: production modifications for the first 100 sample games (sound code "
			"pairing, back-panel flash lamp terminal insulation, magnet wire clip).",
			False,
		),
		_bulletin(
			ADDENDUM2_SOURCE, "Williams_1995_Johnny_Mnemonic_Manual_Addendum_2.pdf", "20241009052346", ADDENDUM2_SHA256,
			"Manual Addendum 2, December 1995, one page: dressing the data glove wires to stop fuses 104/105 blowing.",
			False,
		),
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/Johnny Mnemonic (Williams 1995) VPW v1.2.2.vpx",
			"original_filename": "Johnny Mnemonic (Williams 1995) VPW v1.2.2.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW Johnny Mnemonic v1.2.2 (VPX 10.8, dated 16 Sep 2024 in the contributor's collection), a "
				f"Blender-baked table whose lamp and G.I. Light objects sit at their inserts and bulbs. Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority for named table objects only: its eight "
				"flasher lights l117-l128 are lightmap drivers parked in a row at the cabinet edge (y 2129), not sockets."
			),
			"license": "NOASSERTION",
			"attribution": "Virtual Pinball Workshop (VPW)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script of the retained table (219,146 bytes): cGameName = "jm_12r", UseSolenoids = 2, UseLamps = 1, '
				"HandleMechanics = 0; vpmMapLights AllLamps; SolCallback for 1-3, 5-7, 14-16, 34 and 36 and SolModCallBack for 17-20 "
				"and 25-28; cvpmMech MoveGloveX (Sol1 22, Sol2 -21, switch 12, pulses 74/75) and MoveGloveY (Sol1 24, Sol2 -23, switch "
				"37, pulses 76/77) with vpmMechLengthSw; magna-save keys write 67 (right) and 68 (left); Ball in Hand written to 115; "
				"GiCallBack2 UpdateGI Case 0-2 to the GIString1-3 collections and Case 3 to l143a."
			),
			"license": "NOASSERTION",
			"attribution": "Virtual Pinball Workshop (VPW)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/Johnny_Mnemonic_1.3.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION,
			"sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				'Johnny_Mnemonic_1.3.vbs (32,237 bytes), the earlier table the VPW release descends from: cGameName = "jm_12r", '
				"HandleMechanics = 0, the same solenoid map (bsKickToGlove on 3, bsCrazyBobs on 14, dtDrop on 15/16, setLamp 117-128 "
				"for the flashers, SolLeftDiverterHold/SolRightDiverterHold on 34/36), the same cvpmMech glove setup and the same 67/68 "
				"and 115 writes. Same lineage, so it corroborates the bindings but is not independent evidence. Script only; its "
				"table is not retained."
			),
			"license": "NOASSERTION",
			"attribution": "Johnny Mnemonic VPX table authors; corpus by sverrewl",
			"rights": "NOASSERTION",
		},
		{
			"id": ARCHIVE_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/archive-2020/Johnny Mnemonic (Williams 1995).vpx",
			"original_filename": "Johnny Mnemonic (Williams 1995).vpx",
			"sha256": ARCHIVE_TABLE_SHA256,
			"locator": (
				"The contributor's archived 2020 Johnny Mnemonic table by Alessio (VPX 10.4; its info block still carries another "
				f"table's title), whose script (SHA-256 {ARCHIVE_SCRIPT_SHA256}) runs jm_12r and binds SolCallback 17-20 and 25-28 to "
				"setLamp 117-128, which AddLamp maps onto the glow sprites F117-F128. Bounds 952x1974. Used only to corroborate the "
				"drawing-measured flasher placements by the centres of those sprites (external:pinmame-review-artifacts/"
				"johnny-mnemonic/vpx-geometry-archive2020.tsv and the drawing-fit output); no placement takes its coordinates. "
				f"Extraction manifest SHA-256 {ARCHIVE_MANIFEST_SHA256}, {ARCHIVE_FILE_COUNT} files, {ARCHIVE_TOTAL_BYTES} bytes, "
				"vpxtool git:v0.33.3."
			),
			"license": "NOASSERTION",
			"attribution": "Alessio",
			"rights": "NOASSERTION",
		},
		{
			"id": DRAWING_FIT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py",
			"sha256": DRAWING_FIT_SHA256,
			"locator": (
				"Least-squares affine fit of the solenoid/flashlamp location drawing (printed 2-37, PDF page 105 rendered at 300 dpi, "
				"2550x3300) onto the retained table's coordinates through nine shared features: the four corner matrix holes, the two "
				"upper jet bumper centres, both flipper pivots and the Crazy Bob's eject box. Pixel readings were taken on 25px gridded "
				"2x zooms. Worst control residual 0.013 normalized. Output retained beside it as fit_solenoid_drawing.out.txt "
				f"(SHA-256 {DRAWING_FIT_OUTPUT_SHA256})."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curator",
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
		"board": "WPC-Security CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_component}; row receiver {return_component}",
	}


def _switch_notes(address: int, column: int, row: int) -> str:
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	if row == 6:
		notes += " The printed row-6 header reads 'U209-7'; every other row prints J209-n, so the connector is recorded as J209-7."
	if address in OPTO_SWITCHES:
		notes += (
			' Printed shaded "Opto, Typically Closed" on the switch matrix. Pinned PinMAME\'s jmGameData inverted-switch mask '
			"normalizes this address, so the public state is already normalized and must not be inverted again."
		)
	if address in {31, 32, 33, 34, 35}:
		notes += " A-18617-1 LED with an A-18618-1 phototransistor across the outhole ball trough (A-19963)."
		if address == 31:
			notes += (
				" Trough Jam sits at the shooter end of the trough past Trough Ball 1. The retained script's SolRelease pulses 31 on "
				"every trough eject, a table stand-in for a ball passing the jam opto rather than a jam."
			)
	if address == 36:
		notes += (
			" The switch-locations list prints A-16909 for both the LED and the transistor; the A-20498 Hand Popper Assembly parts "
			"list gives A-16908 LED Assembly and A-16909 Photo Transistor Assembly, which is recorded. The matrix prints 'Ball "
			"Popper 1' and the locations list 'Popper Ball 1'; the popper holds one ball."
		)
	if address in {74, 75, 76, 77}:
		axis = "X (left/right)" if address in {74, 75} else "Y (in/out)"
		notes += (
			f" One of the two Sharp GP1A52HR slotted interrupters on an A-20533 Position Encoder Board of the {axis} hand drive, "
			"reading the drive's opto wheel (04-10255); the two outputs of one board form a quadrature pair (manual printed 3-21). "
			"The matrix prints the Y pair as 76 'Encoder B' and 77 'Encoder A'. A quadrature channel has no resting state, so "
			"normally_closed records only the platform rule for masked WPC matrix inputs: PinMAME inverts this address, so the raw "
			"matrix contact is closed whenever the public state is 0. The hand motors circuit (printed 3-21) draws the encoder "
			"rows 4-7 on J209-5/6/7/8, while the switch matrix prints rows 4-7 on J209-4/5/7/8; the matrix is recorded."
		)
	if address in {12, 37}:
		axis = "X (left/right)" if address == 12 else "Y (in/out)"
		notes += (
			f" Home switch of the {axis} hand drive: one of the two 5647-12693-06 mini micro switches of the A-20500 Hand Assembly. "
			"Service Bulletin SB 85 lists a home switch in each drive."
		)
	if address in HAND_SENSOR_SWITCHES:
		notes += (
			" With LibPinMAME's default of mechanics handling off, the host supplies this switch; with mechanics bits 0 (X) and 1 (Y) "
			"enabled, pinned jm_handleMech drives it from its own hand position every update. No playfield coordinate is recorded: "
			"the sensor rides the hand drive at the rear left."
		)
	if address in CYBER_MATRIX_SWITCHES:
		notes += (
			" One of the nine ball positions of the A-20447 Cyber Space Assembly: a red rollover button (03-9103.1-9) on a spring "
			"over the switch. The matrix and the drawing's Cyber Space Assy. inset name each hole column-then-row: 51/52/53 across "
			"the rear row, 61/62/63 across the middle and 71/72/73 across the front."
		)
	if address in {67, 68}:
		side = "right" if address == 67 else "left"
		notes += (
			f" Cabinet {side} hand-control button (A-18602{'-1' if address == 67 else ''}) on the matrix, which steers the Data Glove "
			"and is one of the four cabinet buttons Video Mode uses. With mechanics handling on, pinned jm_handleMech copies public "
			f"{116 if address == 67 else 118} into this address on every update, so a host must then drive "
			f"{116 if address == 67 else 118} instead (recorded as an optional virtual input); with it off (LibPinMAME's default) "
			f"the host drives {address} directly, as the "
			"retained script does from its magna-save keys."
		)
	if address in {25, 26}:
		notes += " The slingshot kicker switch (A-17800) and the separate score switch (A-17794) share this address."
	if address in {27, 28}:
		notes += " A-20499-9 standup target on the side rail."
		if address == 27:
			notes += " Per the rules, it opens the diverter that channels spinner and right loop shots into the jet bumpers."
	if address == 43:
		notes += " The single drop target's mini micro switch (item 19 of the A-20587 Drop Target Assembly)."
	if address == 47:
		notes += " Crazy Bob's eject hole; the retained script models it as a vertical up-kicker."
	if address == 24:
		notes += (
			" Physical part 5643-09112-00 is a permanently closed link that proves the matrix is connected; pinned PinMAME sets it "
			"closed at machine reset and the retained script also writes Controller.Switch(24) = 1."
		)
	if address == 22:
		notes += " Closed while the coin door is closed; the retained script writes it closed at start."
	if address == 11:
		notes += " Cabinet Ball Launch button (lamp 86 lights it) that fires the autoplunger."
	if address in SWITCH_PROJECTIONS:
		notes += " " + SWITCH_PROJECTIONS[address]
	elif address in SWITCH_OBJECTS:
		notes += f" Placement: retained table object {SWITCH_OBJECTS[address]}."
	return notes


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	cabinet_roles = {
		11: "cabinet.launch", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door",
		23: "cabinet.buy-in", 67: "cabinet.hand-control.right", 68: "cabinet.hand-control.left",
	}
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			identifier = f"switch.matrix-{address}"
			physical: dict[str, Any] = {}
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if address in UNUSED_MATRIX_ADDRESSES:
				physical["notes"] = f"Printed switch-matrix drive column {column}, return row {row}. The printed matrix marks this position NOT USED and the switch-locations list prints '81 to 88 ARE NOT USED.'"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			label = SWITCH_LABELS[address]
			physical["notes"] = _switch_notes(address, column, row)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address in HAND_SENSOR_SWITCHES:
				refs = (MANUAL_SOURCE, SB85_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address == 24:
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE, CORE_SOURCE)
				items.append(_device(identifier, label, "constant", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, CORE_SOURCE), **extra))
				continue
			# On the WPC matrix row read the CPU sees swMatrix directly, so a switch inside the inversion
			# mask that the ROM treats as active at public 1 has a matrix contact that rests closed.
			extra["normally_closed"] = address in OPTO_SWITCHES
			if address in PULSED_SWITCHES:
				extra["pulse"] = True
			if address in cabinet_roles:
				extra["roles"] = [cabinet_roles[address]]
				physical["location"] = "cabinet" if address in {11, 13, 23, 67, 68} else "cabinet interior"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if address == 22:
					extra["initial_active"] = True
			elif address in HAND_SENSOR_SWITCHES:
				physical["location"] = "hand assembly (A-20500)"
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			else:
				status = "observed" if address in OBSERVED_SWITCHES else "validated"
				coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
				if address in CYBER_MATRIX_SWITCHES:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE)
				extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address]], *coordinate_refs, status=status)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, **extra))

	for address, (label, role, switch_type, part, wire, connection) in FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		notes = f"Printed Fliptronic grounded switch {position} ({wire}, {connection}); switch-locations part {part}."
		if switch_type == "opto":
			notes += (
				" Printed shaded as an opto (A-17316 flipper opto board, cabinet mounted). On this generation PinMAME's WPC_FLIPPERS "
				"register read returns the complement of the whole Fliptronic column, so the public state is already normalized "
				"(1 = button pressed) and must not be inverted again. With keyboard handling off (LibPinMAME) the host's value is "
				"carried through unchanged."
			)
		else:
			notes += (
				" Plain end-of-stroke leaf switch (SW-1A-194) on the flipper assembly. jmGameData declares FLIP_SOL(FLIP_L), so "
				"core_updateSw recomputes this bit from the flipper coil every update; a host must not drive it."
			)
		items.append(
			_device(
				f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				roles=[role],
				normally_closed=False,
				physical={
					"location": "cabinet flipper button" if switch_type == "opto" else "flipper assembly",
					"switch_type": switch_type,
					"part_number": part,
					"notes": notes,
				},
				wiring={"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service" if switch_type == "opto" else "internal_nonvisual", MANUAL_SOURCE),
			)
		)
	items.append(
		_device(
			"switch.generic-115", "Ball In Hand", "switch", "pinmame.input.switch", 115, "used",
			(MANUAL_SOURCE, SB85_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
			aliases=[
				{"namespace": "pinmame.switch", "value": "115"},
				{"namespace": "manual.address", "value": "F5"},
			],
			normally_closed=False,
			physical={
				"location": "hand assembly (A-20500), inside the magnet can",
				"switch_type": "leaf",
				"part_number": "A-20612",
				"notes": (
					"Printed Fliptronic grounded switch F5 'BALL IN HAND' (Black-Violet, J906-4); the switch-locations list leaves the "
					"part cell blank and the A-20500 Hand Assembly lists the A-20612 Hand Switch Assembly. Service Bulletin SB 85: a leaf "
					"switch in the magnet can that the ball closes by its own weight; once it closes the ROM duty-cycles the magnet. "
					"PinMAME's Fliptronic column read is complemented as a whole on this generation, so 1 = ball in the hand; the F5 bit "
					"is outside jmGameData's flipper mask, so the host's value is never overwritten. The retained script writes 115 while "
					"it holds a ball under the hand. No playfield coordinate is recorded: the switch rides the moving hand."
				),
			},
			wiring={"board": "Fliptronic II board", "drive_wire": "Black-Violet", "drive_connection": "J906-4"},
			spatial=not_applicable("internal_nonvisual", MANUAL_SOURCE),
		)
	)
	for address, (wire, connection, matrix_label, list_label) in UNUSED_FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		alias_of = {116: 67, 118: 68}.get(address)
		note = (
			f"Printed Fliptronic grounded switch {position} ({wire}, {connection}) labelled '{matrix_label}' on the matrix; the "
			f"switch-locations list prints {position} 'Not Used' ('{list_label}'). Johnny Mnemonic has no upper flippers."
		)
		if alias_of:
			note += (
				f" No physical switch is fitted, but pinned jm_handleMech copies this bit into matrix switch {alias_of} on every update "
				f"while mechanics handling is on, so a host that enables mechanics must press the {'right' if alias_of == 67 else 'left'} "
				"hand control here; FLIP_BUT(FLIP_U) also maps PinMAME's upper-flipper keys here when keyboard handling is on. With "
				"mechanics handling off (LibPinMAME's default) nothing reads it."
			)
		label = f"Hand Control {'Right' if alias_of == 67 else 'Left'} (Mechanics-Handling Alias of {alias_of})" if alias_of else f"Not Used Fliptronic Position {position}"
		items.append(
			_device(
				f"switch.generic-{address}", label, "virtual" if alias_of else "switch",
				"pinmame.input.switch", address, "optional" if alias_of else "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				physical={"location": "not installed", "notes": note},
				spatial=not_applicable("virtual" if alias_of else "unused", CORE_SOURCE if alias_of else MANUAL_SOURCE),
			)
		)

	chart = "AMERICA Off/Off/On/On/On/On/On/On, EUROPEAN Off/Off/On/On/On/Off/On/On, FRENCH Off/Off/On/On/On/On/Off/Off, GERMAN Off/Off/On/On/On/On/On/Off, SPAIN Off/Off/On/On/Off/On/On/On"
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country configuration bit)", "dip_switch",
				"pinmame.input.dip", address, "used", (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC-Security CPU board",
					"switch_type": "dip",
					"notes": f"CPU-board country DIP SW{address}. The manual's quick-reference DIP Switch Chart (PDF page 2) prints SW1-SW8 per country: {chart}.",
				},
				spatial=not_applicable("dip_switch", CORE_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace(chr(39), '')}"


def _solenoid_notes(address: int, printed_type: str) -> str:
	printed_number = PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")
	notes = f"Printed solenoid/flasher table entry {printed_number} ({printed_type})."
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
	if address in {9, 10, 11, 12, 13}:
		notes += " The retained script binds no callback; the table's own bumper/slingshot physics fire on contact and pulse the switch."
	if address == 1:
		notes += " Kicks the ball from the Trough Ball 1 position into the shooter lane."
	if address == 2:
		notes += (
			" A-14525 kicker bracket at the foot of the shooter lane, fired from the cabinet Ball Launch button (11) or automatically; "
			"the rules call it the AUTOFIRE and use it for the Mnemonic Recovery 'virtual kickback' and Powerdown Multiball."
		)
	if address == 3:
		notes += (
			" A-20498 Hand Popper under the rear left of the playfield; Service Bulletin SB 85 says it is designed to shoot the ball "
			"straight up to the hand."
		)
	if address == 5:
		notes += (
			" AE-25-1000 coil of the A-20446 coil bracket under the A-20447 Cyber Space Assembly; its plunger and link drive the "
			"assembly's pivot arm (04-10213) on the Cyber Space base (04-10215), which rides two nylined bearings. The retained script "
			"models the stroke as kicking every held ball out of the matrix. Placement: measured on the solenoid/flashlamp location "
			"drawing (printed 2-37) at the end of callout 05's leader, on the coil drawn at the right rear corner of the matrix, "
			"through the least-squares affine fit of that drawing onto the retained table; observed only, rounded to three places. "
			"The matrix's centre hole is about 0.13 away. The point lies outside the fit's control-point extent (x 0.18-0.79, y "
			"0.06-0.85), so it is extrapolated and the residual does not bound its error."
		)
	if address == 6:
		notes += (
			" Electromagnet (coil 20-10201) in the magnet can of the A-20500 Hand Assembly. Service Bulletin SB 85: turned on at full "
			"power to catch the ball shot up to the magnet assembly, then duty-cycled once the Ball In Hand switch (115) closes. Service "
			"Bulletin SB 87 moves its supply from fuse F104 to F103."
		)
	if address == 7:
		notes += " Printed with backbox voltage (J107-2) and drive (J130-8) connections; the locations list marks the knocker **NOT SHOWN on the playfield drawing."
	if address == 14:
		notes += " A-20496 Crazy Bob's Eject Assembly with a bell armature; the retained script kicks the ball straight up out of the hole."
	if address in {15, 16}:
		notes += (
			" A-20587 single drop target: 15 (AE-26-1200) raises it through the reset plate, 16 (SM1-26-600, the A-14908 Target "
			"K/Down Assembly) knocks it down."
		)
	if address in {21, 22, 23, 24}:
		axis, motion = ("X", "left & right") if address in {21, 22} else ("Y", "in & out")
		role = "direction" if address in {21, 23} else "enable"
		notes += (
			f" Not a lamp: a control line into the A-20532 Dual Relay Motor Driver board (footnote ** of the table), whose {role} input "
			f"{'switches a 12V DPDT relay that reverses' if role == 'direction' else 'turns on a TIP102 Darlington that powers'} the "
			f"{axis} motor (14-8025, footnote *), which 'moves hand {motion}' (manual printed 3-20/3-21). Pinned jm_handleMech reads "
			"these four lines from the raw WPC_SOLENOID3 register because the smoothed solenoid state is too slow for the motor. "
			"The board's connector list (printed 3-20) takes its J1-10 ground from J118-3, while the hand motors circuit (printed "
			"3-21) draws it from J118-2."
		)
	if address in {33, 34, 35, 36}:
		side = "Left" if address in {33, 34} else "Right"
		circuit = "Upper Right" if address in {33, 34} else "Upper Left"
		notes += (
			f" The {side} Diverter (A-20497, FL-11753 coil) is printed on the Fliptronic {circuit} flipper circuit. jmGameData sets "
			"FLIP_SOL for the lower flippers only, so core_getSol publishes the raw power (odd) and hold (even) bits here. The "
			"plunger turns a drive arm (A-19293) on the diverter blade shaft; the spring returns it when the coil is off."
		)
		if address in {33, 34}:
			notes += (
				" The solenoid drawing's callout 33 ends about 0.06 normalized from the retained table's left diverter walls, which the "
				"script's SolLeftDiverterHold swings on 34."
			)
	if address in {45, 46, 47, 48}:
		notes += (
			f" Printed flipper circuit {printed_number}; PinMAME publishes the lower flippers at 45-48, odd addresses the power winding "
			"alone and even addresses power OR hold."
		)
	if address in SOLENOID_PROJECTIONS:
		notes += " " + SOLENOID_PROJECTIONS[address]
	elif address in SOLENOID_OBJECTS and address not in DRAWING_COIL_POSITIONS:
		notes += f" Placement: retained table object {SOLENOID_OBJECTS[address]}."
	return notes


def _flasher_notes(address: int, printed_type: str, part: str) -> str:
	notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type}), flashlamp type {part}."
	backbox = {18: "J125-2", 20: "J125-5", 25: "J124-1", 28: "J124-5"}
	if address in backbox:
		notes += (
			f" The same output also lights a #906 backbox insert-panel bulb (backbox drive {backbox[address]}; the locations list prints "
			"the second row 'Insert Panel', or 'Inset Panel' for 18). Only the playfield bulb is counted and placed."
		)
	if address in {19, 20, 25, 26}:
		notes += " The locations list marks it '*USED WITH A-14266-13, RECEPTACLE AND SKIRT.'"
	if address == 17:
		notes += " A-17803 jet flasher assembly; the jet bumpers are 11-13."
	if address == 18:
		notes += " A-17802 flasher assembly at Crazy Bob's eject."
	if address == 27:
		notes += " Hand Popper Flasher, assembly 04-10280, at the popper mechanism at the rear left, below where the hand catches the ball."
	if address == 20:
		notes += (
			" The connector list (printed 3-30) prints its backbox drive J125-5 as 'solenoid 21' with solenoid 20's Black-Yellow wire, "
			"and the flashlamp wiring page (printed 3-7) prints that backbox wire BLK-ORG; the solenoid table's Blk-Yel is recorded."
		)
	if address == 28:
		notes += (
			" Right end of the back panel. The A-20500 Hand Assembly, which carries the screened back panel, lists a #906 bulb in a "
			"red mini dome with a socket; Manual Addendum 1 adds insulation to the back-panel flash lamp terminals, which can short "
			"and blow fuse 111; and Service Bulletin SB 87's connector 'off the back panel assembly' carries a blue/yellow wire "
			"(solenoid 28's drive colour) with the red/white +20V flasher feed. The second bulb is counted as a backbox insert-panel "
			"bulb: the solenoid table gives it backbox connections (J106-5 supply, J124-5 drive), the locations list prints its row "
			"'Insert Panel', the flashlamp wiring page draws it under BACKBOX FLASHLAMPS, and the connector list gives its J106-5 "
			"supply as '+20V to insert panel flashers'. The same list calls J124-5 'solenoid 28 drive to back panel flasher', which "
			"is read as the device's name, not a second back-panel socket."
		)
	notes += (
		" Pinned wpc.c types the jm_ outputs 17-20 and 25-28 as #89 20V DC bulbs for its brightness model; the printed table gives "
		"#89 for 17 and 27 and #906 for the others, which is recorded."
	)
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained script: {SOLENOID_CALLBACKS[address]}; its light l1{address} is a lightmap driver parked at the cabinet edge, not a socket."
	if address in DRAWING_FLASHER_POSITIONS:
		(_, _), feature = DRAWING_FLASHER_POSITIONS[address]
		notes += (
			f" Placement: measured on the solenoid/flashlamp location drawing (printed 2-37) at {feature}, mapped through the "
			"least-squares affine fit of that drawing onto the retained table (worst control residual 0.013); observed only, rounded "
			"to three places."
		)
		if address in EXTRAPOLATED_FLASHERS:
			notes += (
				" The fit's control points span x 0.18-0.79 and y 0.06-0.85, so this point is extrapolated and the residual does not "
				"bound its error."
			)
		if address == 25:
			notes += (
				" The drawing gives this dome no callout and draws no callout 25 anywhere; the dome is taken to be the Left Ramp "
				"Flasher because the 2020 archive table (Alessio) drives its glow sprite F125 from solenoid 25 at the same spot, "
				f"{ARCHIVE_GLOW_DISTANCES[address]} away. Neither source is a socket record, so the placement stays observed."
			)
		else:
			notes += (
				f" The 2020 archive table (Alessio) drives a glow sprite F1{address} from this solenoid; its centre lies "
				f"{ARCHIVE_GLOW_DISTANCES[address]} from this measurement in that table's own normalized frame, whose rear area "
				"differs from the retained VPW table by up to about 0.06. A glow sprite shows where the table paints light, not a "
				"socket, so it only corroborates."
			)
	return notes


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in UNUSED_SOLENOIDS:
			transistor, wire = UNUSED_SOLENOIDS[address]
			items.append(
				_device(
					f"device.not-used-solenoid-{address}", f"Not Used Solenoid {address}", "coil", "pinmame.output.solenoid", address, "unused",
					(MANUAL_SOURCE, CORE_SOURCE),
					aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
					physical={"notes": f"Printed '{address:02d} NOT USED', High Power, with transistor {transistor} and drive wire {wire} printed but no voltage connection, drive connection or coil; the locations list prints item {address:02d} Not Used and draws no callout."},
					wiring={"board": "WPC-Security power driver board", "driver_transistor": transistor, "control_wire": wire},
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_WIRING[address]
			if address in FLASHERS:
				kind = "flasher"
			elif address in MOTOR_CONTROLS:
				kind = "control_signal"
			elif address == 6:
				kind = "magnet"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			if not part.startswith("#") and part != "A-20532":
				physical["part_number"] = part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if kind == "flasher":
				physical["quantity"] = 1
				physical["notes"] = _flasher_notes(address, printed_type, part)
			else:
				physical["notes"] = _solenoid_notes(address, printed_type)
			wiring: dict[str, Any] = {"board": "Fliptronic II board" if address in PRINTED_FLIPPER_CIRCUITS else "WPC-Security power driver board", "driver_transistor": transistor}
			if voltage:
				wiring["power_connection"] = voltage
			if drive:
				wiring["control_connection"] = drive
			if wire:
				wiring["control_wire"] = wire
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")}]
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {3, 6}:
				refs = refs + (SB85_SOURCE,)
			if address == 6:
				refs = refs + (SB87_SOURCE,)
			if address == 28:
				refs = refs + (ADDENDUM1_SOURCE, SB87_SOURCE)
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif kind == "control_signal":
				extra["roles"] = ["mechanism.hand.motor-control"]
				extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			elif kind == "flasher":
				if address in DRAWING_FLASHER_POSITIONS:
					(x, y), _ = DRAWING_FLASHER_POSITIONS[address]
					extra["spatial"] = located(identifier, "emitter", [(x, y)], MANUAL_SOURCE, DRAWING_FIT_SOURCE, VPX_TABLE_SOURCE, ARCHIVE_TABLE_SOURCE, status="observed")
			elif address in DRAWING_COIL_POSITIONS:
				(x, y), _ = DRAWING_COIL_POSITIONS[address]
				extra["spatial"] = located(identifier, "effect", [(x, y)], MANUAL_SOURCE, DRAWING_FIT_SOURCE, VPX_TABLE_SOURCE, status="observed")
			else:
				coordinate_refs: tuple[str, ...] = (VPX_TABLE_SOURCE,)
				if address in SOLENOID_PROJECTIONS or address in {33, 34}:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE)
				if address == 6:
					coordinate_refs = (VPX_TABLE_SOURCE, SB85_SOURCE)
				extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a Johnny Mnemonic playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Johnny Mnemonic playfield device.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the Game-On / flipper-enable state because jm.c configures no fast-flip address.",
			32: "PinMAME reports this WPC state channel as always zero; jmGameData declares no use for it.",
			49: "PinMAME's simulator-only ball-shooter channel; Johnny Mnemonic's autoplunger is solenoid 2 and has no output here.",
			50: "Reserved PinMAME output position before the first custom-output boundary; jmGameData declares no custom solenoids.",
		}.get(address, "Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and System 11.")
		roles = ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
		items.append(
			_device(
				output_id(label), label, "virtual", "pinmame.output.solenoid", address, "used" if used else "unused",
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
			identifier = f"lamp.matrix-{address}"
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			wiring = {
				"board": "WPC-Security power driver board",
				"drive_wire": drive_wire,
				"drive_connection": drive_connection,
				"return_wire": return_wire,
				"return_connection": return_connection,
				"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
			}
			aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
			if address in UNUSED_LAMPS:
				items.append(
					_device(
						identifier, f"Not Used Lamp {address}", "lamp", "pinmame.output.lamp", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE),
						aliases=aliases, wiring=wiring,
						physical={"notes": f"Printed lamp-matrix column {column}, row {row}: NOT USED on the matrix and 'Not Used' with no bulb or assembly in the lamp-locations list."},
						spatial=not_applicable("unused", MANUAL_SOURCE),
					)
				)
				continue
			physical: dict[str, Any] = {"assembly_part_number": LAMP_ASSEMBLIES[address]}
			if address not in {86, 87, 88}:
				physical["quantity"] = 1
			notes = f"Printed lamp-matrix drive column {column}, return row {row}." + LAMP_CONNECTOR_NOTE
			refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring, "physical": physical}
			if address in {86, 87, 88}:
				notes += (
					" Lamp inside the illuminated cabinet button assembly; the lamp-locations list prints its bulb number '-----' and the "
					"drawing puts its callout below the cabinet outline. The connector list routes rows 6-8 and column 8 to the cabinet "
					"on J135-7/8/9 and J136-3."
				)
				if address == 87:
					notes += " The locations list prints its assembly '20-663-21'; the switch-locations list prints the Buy-in Button as 20-9663-21."
				extra["roles"] = ["cabinet.launch" if address == 86 else "cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE)
			else:
				bulb = LAMP_BULBS.get(address, "#555")
				notes += f" Printed bulb {'24-6549' if bulb == '#44' else '24-8768'} ({bulb})."
				coordinate_refs: tuple[str, ...] = (VPX_TABLE_SOURCE,)
				if address in MATRIX_LAMP_HOLES:
					hole_switch = MATRIX_LAMP_HOLES[address]
					notes += (
						f" Under the matrix hole whose switch is {hole_switch} ('{SWITCH_LABELS[hole_switch]}'), on the 04-10277 PC board of "
						"the A-20447 Cyber Space Assembly. The lamp and switch matrices number the nine holes in opposite orders; the "
						"printed labels, the lamp-locations drawing and the retained table all pair them by label."
					)
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE)
				notes += f" Placement: retained table Light l{address} (vpmMapLights timer interval {address})."
				extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], *coordinate_refs)
			physical["notes"] = notes
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, feed, feed_wire, transistor, switched_return, return_wire, bulbs) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination string {address + 1:02d} '{label.upper()}'; printed lamps {bulbs}. The triac switches the "
			"return pin (G.I. circuit, printed 3-10; connector list, printed 3-30), so the 6.8Vac feed is recorded as the power "
			"connection and the return as the control connection. The solenoid table prints the return pins under its "
			"'Voltage Connections' columns and the feed pins and their White-colour wires under the drive columns."
		)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}],
			"wiring": {"board": "WPC-Security power driver board", "power_connection": feed, "power_wire": feed_wire, "driver_transistor": transistor, "control_connection": switched_return, "control_wire": return_wire},
		}
		physical: dict[str, Any] = {}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if address in {0, 1, 2}:
			notes += (
				" The power driver board connector list (printed 3-30) confirms the split: J121 pins go 'G.I. to playfield' and J120 "
				"pins 'G.I. to insert panel' (J121-1 is printed 'G.I. to' with no destination)."
			)
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				f" The manual prints no per-string bulb list or count, so the quantity counts playfield sockets only and every coordinate "
				f"comes from the retained table's {GI_COLLECTIONS[address]} collection ({GI_MEMBERS[address]}), which the retained script's "
				"UpdateGI dispatches for this string. These placements are observed, not validated: no factory source lists the sockets. "
				"The string's #555 backbox bulbs are not placed."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE, status="observed")
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		elif address == 3:
			notes += (
				" Recorded as a playfield string: the solenoid table gives it only playfield connections and a #44 playfield lamp type, "
				"and its J121-10 feed is 'White-Green, 6.8Vac, G.I. to playfield'. The connector list prints its J121-5 return "
				"'Green, return, G.I. to insert panel', which is read as a misprint because every other J121 pin runs to the playfield "
				"and every insert-panel G.I. pin is on J120. The retained script dispatches it to the single light l143a, a lightmap "
				"driver parked at the cabinet edge whose baked lightmaps cover the hand, its rail, the right diverter, other parts and "
				"an upper-left region of the playfield (LM_GI4_Playfield spans x 0-585 and y 0-760 table units), a lead for where the "
				"string lights but not socket positions; no factory "
				"source lists its sockets, so no coordinate is recorded."
			)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		else:
			notes += (
				" Backbox and cabinet string (printed backbox J120-6/J120-11 and cabinet J119-3/J119-1 connections, no playfield "
				"connection); the retained script's UpdateGI implements no case for it."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "gi", "pinmame.output.gi", address, "used", refs, **extra))
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
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior, "provenance": provenance(*refs)}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		if positions:
			record["positions"] = [{"id": pid, "label": plabel, "sensors": psensors, "description": pdesc} for pid, plabel, psensors, pdesc in positions]
		return record

	matrix_positions = [
		(f"hole-{SWITCH_LABELS[address][-2:]}", SWITCH_LABELS[address], [f"switch.matrix-{address}"],
		 f"{'Rear' if address < 60 else 'Middle' if address < 70 else 'Front'} row, {('left', 'centre', 'right')[address % 10 - 1]} column.")
		for address in (51, 52, 53, 61, 62, 63, 71, 72, 73)
	]
	return [
		mechanism(
			"mechanism.trough", "Four-ball trough", "kicker", [output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on the trough optos 32 (Trough Ball 1, at the shooter end) to 35 (Trough Ball 4, at the drain end) of the "
			"A-19963 outhole ball trough under the apron; 31 (Trough Jam) is a fifth LED/phototransistor pair at the shooter end past "
			"ball 1. All five are normalized by PinMAME. Solenoid 1 (Trough Eject, AE-26-1500) kicks the ball on 32 into the shooter "
			"lane. The retained script keeps real balls on kickers sw32-sw35, rolls them forward as the front ball leaves and pulses 31 "
			"with every eject.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4", ["switch.matrix-35"], "Fourth trough position, at the drain end."),
				("jam", "Trough Jam", ["switch.matrix-31"], "Jam opto at the shooter end of the trough."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-19963",
		),
		mechanism(
			"mechanism.autoplunger", "Shooter lane and autoplunger", "kicker", [output_id("Autoplunger")],
			["switch.matrix-78", "switch.matrix-11"],
			"A ball served from the trough rests on Shooter Lane (78). The ROM fires solenoid 2 (A-14525 kicker bracket, AE-23-800) to "
			"launch it, when the player presses the cabinet Ball Launch button (11, lit by lamp 86) or automatically; the rules use the "
			"same AUTOFIRE to return a ball for Mnemonic Recovery and to relaunch every ball during Powerdown Multiball. There is no "
			"manual plunger; the retained script's impulse plunger PlungerIM stands in for the kicker.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-78"], "Shooter lane rollover.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.data-glove", "Data Glove (moving hand)", "motorized",
			[output_id("X Motor Direction"), output_id("X Motor Enable"), output_id("Y Motor Direction"), output_id("Y Motor Enable"), output_id("Hand Magnet")],
			["switch.matrix-12", "switch.matrix-37", "switch.matrix-74", "switch.matrix-75", "switch.matrix-76", "switch.matrix-77", "switch.generic-115", "switch.matrix-67", "switch.matrix-68"],
			"A-20500 Hand Assembly: a molded left hand on a magnet carriage in front of the screened back panel at the rear left. Two "
			"14-8025 DC gear motors turn an X screw (left & right) and a Y screw (in & out) through couplers; each drive has a home "
			"switch (12 for X, 37 for Y) and an A-20533 position encoder board whose two Sharp GP1A52HR optos read an opto wheel as a "
			"quadrature pair (74/75 for X, 76/77 for Y). The A-20532 Dual Relay Motor Driver board takes the enable (22 X, 24 Y) on a "
			"TIP102 Darlington and the direction (21 X, 23 Y) on a 12V DPDT reversing relay. The magnet (solenoid 6, coil 20-10201) "
			"sits in the magnet can; Service Bulletin SB 85 says it is turned on at full power when the ball is shot up to it (the "
			"popper is designed to shoot the ball straight up to the hand) and duty-cycled once the Ball In Hand leaf switch (115) "
			"closes under the ball's weight, and asks the technician to verify that it sits approximately over the popper when it "
			"fails to catch. The ROM then carries the ball over the Cyberspace Matrix and releases it into a hole, and can pick a ball back up "
			"out of a hole. The player steers the hand with the cabinet Right/Left Hand Control buttons (67/68). Travel limits, speeds "
			"and encoder pitch are not printed. Pinned PinMAME models each axis (mechanics bits 0 and 1) as a counter stepped while its "
			"enable is on, home closed while the counter is below 1 and a quadrature pattern from its two low bits; it starts both "
			"axes at home. The retained script instead runs two cvpmMech objects with its own ranges and PinMAME mechanics handling "
			"off.",
			[
				("home", "Hand at home", ["switch.matrix-12", "switch.matrix-37"], "Both home switches made. The manual does not print where home is. The retained table closes 12 over X positions 0-2 and 37 over Y positions 0-1502 of its 3400-unit axes and catches the popper ball with X near 0 and Y inside that range."),
				("ball-held", "Ball in the hand", ["switch.generic-115"], "Ball In Hand switch closed by the ball's weight."),
			],
			MANUAL_SOURCE, SB85_SOURCE, SB87_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20500",
		),
		mechanism(
			"mechanism.hand-popper", "Hand popper", "kicker", [output_id("Popper")], ["switch.matrix-36"],
			"A ball entering the popper at the rear left (the rules' center 'popper' lane) is seen by the A-16908/A-16909 opto (36) of "
			"the A-20498 Hand Popper Assembly and shot straight up by solenoid 3 (AE-24-900) to the hand's magnet waiting over it.",
			[("ball", "Ball in the popper", ["switch.matrix-36"], "Popper opto.")],
			MANUAL_SOURCE, SB85_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20498",
		),
		mechanism(
			"mechanism.cyberspace-matrix", "Cyberspace Matrix", "other", [output_id("Clear Matrix")],
			[f"switch.matrix-{address}" for address in (51, 52, 53, 61, 62, 63, 71, 72, 73)],
			"A-20447 Cyber Space Assembly at the upper right: a cover with nine holes over nine red rollover buttons on springs, each "
			"over a switch (51-53 rear row, 61-63 middle, 71-73 front, named column-then-row), with the nine matrix lamps on the "
			"04-10277 PC board beneath. The hand drops balls into the holes; per the rules each hole gives an award, three balls start "
			"Cyberspace Multiball, and the placement of the locked balls determines its jackpot shots. Solenoid 5 (Clear Matrix, AE-25-1000) drives a plunger, "
			"link and pivot arm on the assembly's base, which rides two nylined bearings; the retained script models the stroke as "
			"kicking every held ball out of the matrix.",
			matrix_positions,
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20447",
		),
		mechanism(
			"mechanism.crazy-bobs-eject", "Crazy Bob's eject", "kicker", [output_id("Crazy Bob's Eject")], ["switch.matrix-47"],
			"A hole at the centre left (switch 47) with the A-20496 eject assembly (AE-26-1500 coil, bell armature) under it; the "
			"retained script kicks the ball straight up out of the hole.",
			[("ball", "Ball in Crazy Bob's", ["switch.matrix-47"], "Crazy Bob's switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20496",
		),
		mechanism(
			"mechanism.drop-target", "Controlled drop target", "drop_target_bank",
			[output_id("Drop Target Up"), output_id("Drop Target Down")], ["switch.matrix-43"],
			"A-20587 single drop target beside the popper at the rear: solenoid 15 (AE-26-1200) raises it through the reset plate and "
			"solenoid 16 (SM1-26-600, the A-14908 Target K/Down Assembly) knocks it down; its mini micro switch is 43. The rules call it "
			"the controlled drop target.",
			[("down", "Target down", ["switch.matrix-43"], "Drop target switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-20587",
		),
		mechanism(
			"mechanism.diverters", "Left and right diverters", "diverter",
			[output_id("Left Diverter Power"), output_id("Left Diverter Hold"), output_id("Right Diverter Power"), output_id("Right Diverter Hold")], [],
			"Two A-20497 Diverter Assemblies on the Fliptronic upper flipper circuits: the Left Diverter on the upper-right circuit "
			"(33 power, 34 hold) and the Right Diverter on the upper-left circuit (35 power, 36 hold), each an FL-11753 coil whose "
			"plunger turns a drive arm on the blade shaft (diverter assemblies #1 and #2), sprung back when off. No switch senses "
			"either position. Per the rules, the left standup target opens 'the diverter which channels SPINNER and RIGHT LOOP shots "
			"into the JET BUMPERS'. The retained script binds only the hold windings (34 and 36); the left diverter sits at the top of "
			"the left orbit and the right one at the rear, just right of the popper.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-20497",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other",
			[output_id("Left Jet Bumper"), output_id("Bottom Jet Bumper"), output_id("Right Jet Bumper")],
			["switch.matrix-44", "switch.matrix-45", "switch.matrix-46"],
			"Three A-9415-2 jet bumpers at the upper left, below the three jet lanes (64-66) and lit by the Jets Flasher (17). The "
			"retained script's Bumper1/Bumper2/Bumper3 handlers pulse 44/45/46, matching the printed Left/Bottom/Right names to the "
			"objects' positions.",
			[
				("left", "Left jet", ["switch.matrix-44"], "Table object Bumper1, upper left."),
				("bottom", "Bottom jet", ["switch.matrix-45"], "Table object Bumper2, lowest."),
				("right", "Right jet", ["switch.matrix-46"], "Table object Bumper3, right."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-25", "switch.matrix-26"],
			"B-9362-L-2 and B-9362-R-3 slingshot assemblies (AE-26-1200); each carries a kick switch (A-17800) and a score switch "
			"(A-17794) on one address, and a #906 flasher (19, 20) under the plastic.",
			[("left", "Left slingshot", ["switch.matrix-25"], "Left slingshot."), ("right", "Right slingshot", ["switch.matrix-26"], "Right slingshot.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.flippers", "Two flippers", "other",
			[output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"), output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold")],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114"],
			"Lower right (A-19223-R) and lower left (A-15849-L-2) Fliptronic flippers with FL-11629 blue coils and separate power and "
			"hold windings, each with a cabinet opto (112, 114) and an end-of-stroke leaf switch (111, 113). The ROM energizes both "
			"windings on the button and drops the power winding when the end-of-stroke closes. Per the rules, the flipper buttons also "
			"'LANE CHANGE' the three jet lane lamps.",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112, EOS 111."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114, EOS 113."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Knocker", "other", [output_id("Knocker")], [],
			"Solenoid 7 fires the A-10686-1 knocker (AE-23-800), wired through the backbox connections and not drawn on the playfield.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-10686-1",
		),
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
			"id": "williams.johnny-mnemonic.1995",
			"name": "Johnny Mnemonic",
			"manufacturer": "Williams",
			"year": 1995,
			"kind": "physical_pinball",
			"ipdb_id": 3683,
			"opdb_id": "GR6W8-Mb55B",
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
				"spatial_placement": "observed",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-security",
			"hardware_generation": "0x20",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": [],
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Johnny Mnemonic device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	observed_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		address = int(device["binding"]["device"])
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
			continue
		placement_count += len(spatial["placements"])
		(observed_inputs if spatial["status"] == "observed" else located_inputs).append(address)
	located_outputs: list[dict[str, Any]] = []
	observed_outputs: list[dict[str, Any]] = []
	unplaced_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unplaced_outputs.append(binding)
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
			continue
		placement_count += len(spatial["placements"])
		(observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
	order = lambda item: (item["group"], item["address"])  # noqa: E731
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "observed",
		"blockers": [
			"The Clear Matrix coil (5) and flashers 17-20 and 25-28 have no table object at their location: the retained VPW table drives its flasher lightmaps from lights parked at "
			"the cabinet edge. Their coordinates are measured on the manual's solenoid/flashlamp location drawing through a nine-point "
			"least-squares fit (worst residual 0.013) and stay observed. Promotion needs a socket survey of a real machine or a "
			"retained table with modelled flasher sockets.",
			"The Left Ramp Flasher (25) has no callout on the location drawing; it is placed on an unlabelled dome the drawing shows "
			"at the far left, identified by the 2020 archive table's solenoid-25 glow sprite 0.021 away, and stays observed.",
			"G.I. string 4 (public 3) is a playfield-only string with no factory socket list and no placed table light, so it has no "
			"coordinate.",
			"Playfield G.I. strings 1-3 have no factory socket list; every coordinate comes from the retained table's GIString1-3 "
			"collections and stays observed.",
			"Trough Jam (31) has no table object and is projected onto the Trough Ball 1 kicker, so it stays observed.",
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
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/johnny-mnemonic-1995/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool git:v0.33.3",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"manual_reconciliation": {
			"artifact": "external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py",
			"artifact_sha256": DRAWING_FIT_SHA256,
			"output": "external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.out.txt",
			"output_sha256": DRAWING_FIT_OUTPUT_SHA256,
			"transform": "Least-squares affine fit of the 300 dpi render of printed 2-37 onto table coordinates through nine shared features (four corner matrix holes, two upper jet bumper centres, both flipper pivots, the Crazy Bob's eject box); worst control residual 0.013 normalized.",
			"switch_drawing": "The switch-location drawing (printed 2-35) was compared by eye: every placed switch's callout reaches the feature its table object stands on, and the drawing's Cyber Space Assy. inset puts 51/52/53 on the rear row and 71/72/73 at the front, as the script binds the Matrix kickers.",
			"coil_callouts": "Coil callouts measured through the same fit (pixel readings in the artifact): 01 ends 0.051 from its trough eject kicker, 02 0.003 from its autoplunger trigger, 33 (Left Diverter) 0.060 from the table's left diverter walls, and 05 (Clear Matrix) on the coil at the matrix's right rear corner, 0.129 from the centre hole, which is where solenoid 5 is placed. The other coil leaders were not measured.",
			"extrapolation": "The control points span x 0.18-0.79 and y 0.06-0.85; flashers 25, 26 and 28 and the Clear Matrix coil (5) lie outside that range, so their placements are extrapolated and the residual does not bound their error.",
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"observed_input_addresses": sorted(observed_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=order),
		"observed_output_bindings": sorted(observed_outputs, key=order),
		"unplaced_output_bindings": sorted(unplaced_outputs, key=order),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": f"Measured on the location drawing at {feature} through the affine fit; not a table object."}
			for address, (_, feature) in sorted({**DRAWING_FLASHER_POSITIONS, **DRAWING_COIL_POSITIONS}.items())
		],
		"coordinate_origins": {
			"drag_point_means": ["Wall Leftslingshot (switch 25, solenoid 9)", "Wall Rightslingshot (switch 26, solenoid 10)", "Wall sw38", "Wall sw43 (switch 43, solenoids 15/16)", "Wall LeftDiverterOpen (solenoids 33/34)", "Wall RightDiverterOpen (solenoids 35/36)"],
			"object_centers": "every other table placement uses its retained object's own center",
			"drawing_measurements": "flashers 17-20 and 25-28 and the Clear Matrix coil (5), rounded to three places",
		},
		"excluded_object_classes": [
			"Flasher lights l117-l128 and G.I. light l143a: lightmap drivers parked in a row at the cabinet edge (y 2129), not sockets.",
			"Cabinet-button lights l86-l88, placed in the same cabinet-edge row.",
			"Baked Blender primitives (BM_*/LM_*), whose object origins are not device positions.",
			"The LeftDiverterClosed/RightDiverterClosed walls, which the table raises only while the diverter coil is on.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Johnny Mnemonic (Williams, 1995) spatial review",
		"",
		f"Status: {report['status']}. Every switch, coil, magnet and lamp that has a playfield location is placed from the retained "
		"table or carries a controlled `not_applicable` record, except the Clear Matrix coil and the flashers, which are measured on "
		"the manual's location drawing and stay `observed`; the playfield G.I. strings are placed from the table's G.I. collections and stay `observed`, and "
		"G.I. string 4 has no coordinate, which keeps the record at `machines/partial/williams/johnny-mnemonic-1995.json`.",
		"",
		f"The geometry source is the retained known-working `Johnny Mnemonic (Williams 1995) VPW v1.2.2.vpx` (SHA-256 "
		f"`{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding authority. Exact playfield bounds "
		f"are `{TABLE_BOUNDS}`; every table coordinate is x/964 and y/2162 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime authority; the September 1995 operations manual and its service bulletins are the "
		"physical inventory, construction and wiring authority; pinned PinMAME owns controller topology; the retained table supplies "
		"geometry for named objects.",
		f"- Manual reconciliation (`{report['manual_reconciliation']['artifact']}`): {report['manual_reconciliation']['transform']} "
		f"{report['manual_reconciliation']['switch_drawing']} {report['manual_reconciliation']['coil_callouts']}",
		"- The hand's home switches, encoders, Ball In Hand switch and motor-control lines ride the moving Data Glove and carry "
		"`internal_nonvisual` records; the hand magnet is placed where the retained table's hand catches the popper ball.",
		"- Flashers 18, 20, 25 and 28 also light a backbox insert-panel bulb, which is not placed; G.I. strings 1-3 also feed #555 "
		"backbox bulbs, and string 5 is backbox and cabinet only.",
		"",
		"## Blockers",
		"",
	]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Explicit projections and measurements", ""]
	lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
		f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
		f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
		f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
		f"- Output bindings with no coordinate: {len(report['unplaced_output_bindings'])}",
	]
	lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
	lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Refused. `coverage.missing` is `[\"spatial_placement\"]`: the flasher sockets are known only from the factory drawing's "
		"callouts (corroborated only by a second community table's glow sprites), the playfield G.I. sockets only from one community "
		"table's light collections, and G.I. string 4 is not placed at all.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Operations manual SHA-256 `{MANUAL_SHA256}`.",
		f"- Drawing fit `{report['manual_reconciliation']['artifact']}` SHA-256 `{DRAWING_FIT_SHA256}`, output SHA-256 `{DRAWING_FIT_OUTPUT_SHA256}`.",
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
	stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("Stale Johnny Mnemonic author-ready definition is still present")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"Johnny Mnemonic artifact is missing: {path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Johnny Mnemonic definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Johnny Mnemonic seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Johnny Mnemonic spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Johnny Mnemonic spatial review drifted from its deterministic curator: {markdown_path}")
	print("Johnny Mnemonic definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the canonical definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, seed and spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		print(f"Johnny Mnemonic extraction manifest written: {write_extraction_manifest(root)}")
	elif args.verify_extraction:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		verify_extraction_manifest(root)
		print("Johnny Mnemonic retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
