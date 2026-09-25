"""Curate the physical Bally The Shadow (1994) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal below, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition, its pinned seed and the
spatial audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# Kept partial: every coordinate comes from one community table and has not yet been reconciled
# against the manual's legible location drawings (printed 2-39, 2-41, 2-43), and the playfield G.I.
# sockets come only from the table's G.I. collections.
PARTIAL_PATH = ROOT / "machines/partial/bally/the-shadow-1994.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/the-shadow-1994.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/the-shadow-1994.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/the-shadow-1994.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/the-shadow-1994.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts/bally.the-shadow.1994"
EXCERPT_PREFIX = "evidence/excerpts/bally.the-shadow.1994"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
MANUAL_SOURCE = "manual.bally.the-shadow.1994.operations-manual"
VPX_TABLE_SOURCE = "vpx-table.the-shadow-vpw-mod-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.the-shadow-vpw-mod-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.the-shadow-vpw-mod-1-0"
LEGACY_TABLE_SOURCE = "vpx-table.the-shadow-skitso-detail-mod"
LEGACY_SCRIPT_SOURCE = "vpx-script.the-shadow-skitso-detail-mod"

MANUAL_SHA256 = "900c94825a940a34abaae5d14284098b44dda1e6c7f79d47a92e60f7bd0c4b9e"
TABLE_SHA256 = "f256caa5f7af3f17c5da3fa62b23ae49a6f4e9f80ab24acaac953db8d2cfe13e"
SCRIPT_SHA256 = "973a9ad5b2ccbc31334dc3752e065f7a94265c69f9a89f3bcf58e2f3eec51f77"
DOWNLOAD_ARCHIVE_SHA256 = "dd37589b9a16d868f55e42ddbec7d9aef3f9d343dcb66f9bbecc3cc2f660d069"
LEGACY_TABLE_SHA256 = "2d5b7b25969fac748f79dfab765633a29a05f65cbd423dc1f6497bba239c71b4"
LEGACY_SCRIPT_SHA256 = "4d6952c53aea9d52f919c98e35e389a87fe864e4bdf340a6004499f943c9b559"

EXTRACTION_RELATIVE_PATH = Path("bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "0ffe2c6f22c92bae205ece4dcc8d2d904009c1ed80dbc3d9693d0bfccedc1b59"
EXTRACTION_FILE_COUNT = 1608
EXTRACTION_TOTAL_BYTES = 203264122

TABLE_BOUNDS = "left=0 top=0 right=975 bottom=1974"

DRIVER_IDS = (
	"ts_lx5", "ts_dx5", "ts_lh6", "ts_lh6p", "ts_dh6", "ts_la6", "ts_da6", "ts_lf6", "ts_df6", "ts_lm6", "ts_dm6",
	"ts_lx4", "ts_dx4", "ts_la4", "ts_da4", "ts_lf4", "ts_la2", "ts_da2", "ts_pa1", "ts_pa2",
)
_SHARED = "It is declared with the same wpc_mSecurityS machine driver and init_ts, shares the parent's tsGameData and changes no public address."
DRIVER_COMPATIBILITY = {
	"ts_lx5": ("identical", "Bally LX-5 game ROM, the parent of the ts clone tree and the firmware the retained script runs."),
	"ts_dx5": ("identical", "LX-5 with the community LED ghost fix. " + _SHARED),
	"ts_lh6": ("identical", "Bally LH-6 game ROM. " + _SHARED),
	"ts_lh6p": ("identical", "LH-6 with a community text-index patch. " + _SHARED),
	"ts_dh6": ("identical", "LH-6 with the community LED ghost fix. " + _SHARED),
	"ts_la6": ("identical", "Bally LA-6 game ROM. " + _SHARED),
	"ts_da6": ("identical", "LA-6 with the community LED ghost fix. " + _SHARED),
	"ts_lf6": ("identical", "Bally LF-6 French game ROM. " + _SHARED),
	"ts_df6": ("identical", "LF-6 French with the community LED ghost fix. " + _SHARED),
	"ts_lm6": ("identical", "Bally LM-6 'Mild' game ROM. " + _SHARED),
	"ts_dm6": ("identical", "LM-6 'Mild' with the community LED ghost fix. " + _SHARED),
	"ts_lx4": ("identical", "Bally LX-4 earlier game ROM. " + _SHARED),
	"ts_dx4": ("identical", "LX-4 with the community LED ghost fix. " + _SHARED),
	"ts_la4": ("identical", "Bally LA-4 earlier game ROM. " + _SHARED),
	"ts_da4": ("identical", "LA-4 with the community LED ghost fix. " + _SHARED),
	"ts_lf4": ("identical", "Bally LF-4 French earlier game ROM. " + _SHARED),
	"ts_la2": ("identical", "Bally LA-2 early game ROM (catalog year 1994). " + _SHARED),
	"ts_da2": ("identical", "LA-2 with the community LED ghost fix. " + _SHARED),
	"ts_pa1": (
		"compatible",
		"PA-1 prototype game ROM (catalog year 1994). PinMAME runs it with the production tsGameData and differs only in "
		"its U2 sound ROM (su2-sp2.rom); whether prototype machines differed physically is not recorded in any retained source.",
	),
	"ts_pa2": (
		"compatible",
		"PA-1 prototype with the community LED ghost fix (catalog 'PA-2 LED Ghost Fix'); same prototype sound ROM set as ts_pa1.",
	),
}

# --- Printed switch matrix (manual printed 2-40).
SWITCH_LABELS = {
	11: "Gun Trigger", 12: "Right Phurba Control", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Right Outlane",
	16: "Right Return Lane", 17: "Left Return Lane", 18: "Left Outlane",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy-In Button", 24: "Always Closed", 25: "(M)ONGOL Target",
	26: "M(O)NGOL Target", 27: "MONGO(L) Target", 28: "MONG(O)L Target",
	31: "Left Ramp Enter", 32: "Right Ramp Enter", 33: "Inner Sanctum", 34: "Left Phurba Control", 35: "Left Rubber",
	36: "Mini Kicker", 37: "Mini Limit Left", 38: "Mini Limit Right",
	41: "Trough 1", 42: "Trough 2", 43: "Trough 3", 44: "Trough 4", 45: "Trough 5", 46: "Top Trough",
	47: "Inner Loop Enter", 48: "Shooter",
	51: "Wall Target Down", 52: "MO(N)GOL Target", 53: "MON(G)OL Target", 54: "Left Loop Enter", 55: "Battle Drop Down",
	56: "Center Standup", 57: "Right Loop Enter", 58: "Mini Exit Tube",
	61: "Left Slingshot", 62: "Right Slingshot", 63: "Lockup Right", 64: "Lockup Middle", 65: "Lockup Left",
	66: "Left Eject", 67: "Right Eject", 68: "Popper",
	71: "Mini Left Standup 1", 72: "Mini Left Standup 2", 73: "Mini Left Standup 3", 74: "Mini Left Standup 4",
	75: "Left Ramp Left Made", 76: "Left Ramp Right Made", 77: "Right Ramp Left Made", 78: "Right Ramp Right Made",
	81: "Mini Right Standup 4", 82: "Mini Right Standup 3", 84: "Mini Right Standup 1",
	85: "Mini Drop Left", 86: "Mini Drop Middle Left", 87: "Mini Drop Middle Right", 88: "Mini Drop Right",
}
# Printed "NOT USED" on the matrix and "---" / "Not Used" in the switch-locations list.
UNUSED_MATRIX_ADDRESSES = {83}
MINI_RIGHT_STANDUP_INSET_NOTE = (
	"The mini-playfield inset of the printed 2-41 switch location drawing labels the three right standups 84, 83 and 81 from the rear and draws no 82, so its middle callout is a misprint for 82; the retained table's sw82 sits between sw84 and sw81."
)
# Shaded "Opto, Typically Closed" on the printed matrix.
OPTO_SWITCHES = {31, 32, 33, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 85, 86, 87, 88}
# tsGameData's inverted-switch mask {0x00,0x00,0x00,0xe7,0x7f,0x00,0x00,0x00,0xf0,0x00,0x00,0x00} is indexed
# by matrix column: 0xe7 normalizes 31-33 and 36-38, 0x7f normalizes 41-47 and 0xf0 normalizes 85-88.
PINMAME_INVERTED_MASK = (0x00, 0x00, 0x00, 0xE7, 0x7F, 0x00, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00)
# vpmTimer.PulseSw / PulseSwitch callers in the retained script.
PULSED_SWITCHES = {25, 26, 27, 28, 35, 36, 52, 53, 56, 61, 62, 71, 72, 73, 74, 81, 82, 84}

SWITCH_TYPES = {
	11: "button", 12: "button", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch", 17: "microswitch",
	18: "microswitch", 21: "tilt", 22: "microswitch", 23: "button", 24: "other",
	25: "leaf", 26: "leaf", 27: "leaf", 28: "leaf", 31: "opto", 32: "opto", 33: "opto", 34: "button", 35: "leaf",
	36: "opto", 37: "opto", 38: "opto", 41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto", 46: "opto",
	47: "opto", 48: "microswitch", 51: "microswitch", 52: "leaf", 53: "leaf", 54: "microswitch", 55: "microswitch",
	56: "leaf", 57: "microswitch", 58: "microswitch", 61: "leaf", 62: "leaf", 63: "microswitch", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "microswitch", 71: "leaf", 72: "leaf", 73: "leaf",
	74: "leaf", 75: "microswitch", 76: "microswitch", 77: "microswitch", 78: "microswitch", 81: "leaf", 82: "leaf",
	84: "leaf", 85: "opto", 86: "opto", 87: "opto", 88: "opto",
}
_LED = "A-16908 LED with A-16909 transistor"
_TROUGH = "A-18617 LED with A-18618 transistor"
SWITCH_PARTS = {
	11: "5647-12133-16", 12: "SW-1A-195", 13: "20-9663-2", 14: "A-15361", 15: "5647-12693-19", 16: "5647-12693-19",
	17: "5647-12693-19", 18: "5647-12693-19", 21: "A-17238", 22: "5643-09288-00", 23: "20-9663-18", 24: "5643-09112-00",
	25: "A-18019-6", 26: "A-18019-6", 27: "A-18019-6", 28: "A-18019-6", 31: _LED, 32: _LED, 33: _LED, 34: "SW-1A-195",
	35: "SW-1A-120", 36: _LED, 37: "A-14534", 38: "A-14534", 41: _TROUGH, 42: _TROUGH, 43: _TROUGH, 44: _TROUGH,
	45: _TROUGH, 46: _TROUGH, 47: _LED, 48: "5647-12693-32", 51: "5647-12693-31", 52: "A-18530-6", 53: "A-18530-6",
	54: "5647-12693-19", 55: "5647-12693-31", 56: "A-18530-6", 57: "5647-12693-19", 58: "5647-12693-13",
	61: "SW-1A-114 (kicker) with SW-1A-120 (score)", 62: "SW-1A-114 (kicker) with SW-1A-120 (score)",
	63: "5647-12073-34", 64: "5647-12073-33", 65: "5647-12693-32", 66: "5647-12693-43", 67: "5647-12133-11",
	68: "5647-12693-24", 71: "A-18378-6", 72: "A-18378-6", 73: "A-18378-6", 74: "A-18378-6", 75: "5647-12693-13",
	76: "5647-12693-13", 77: "5647-12693-13", 78: "5647-12693-13", 81: "A-18378-6", 82: "A-18378-6", 84: "A-18378-6",
	85: "A-19666", 86: "A-19666", 87: "A-19666", 88: "A-19666",
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
	5: ("Service Credits / Escape", "service.escape", "Printed Normal Function Ser Credits, Test Function Esc."),
	6: ("Volume Down / Down", "service.down", "Printed Normal Function Vol Down, Test Function Down."),
	7: ("Volume Up / Up", "service.up", "Printed Normal Function Vol Up, Test Function Up."),
	8: ("Begin Test / Enter", "service.enter", "Printed Normal Function Begin Test, Test Function Enter."),
}
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "leaf", "SW-1A-194", "Black-Green", "J906-1"),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", "opto", "A-17316", "Black-Violet", "J905-1"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "leaf", "SW-1A-194", "Black-Blue", "J906-3"),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", "opto", "A-17316", "Black-Gray", "J905-2"),
	115: ("Upper Right Flipper EOS", "internal.flipper.upper.right.eos", "leaf", "SW-1A-194", "Black-Violet", "J906-4"),
	116: ("Upper Right Flipper Button", "flipper.upper.right.button", "opto", "A-17316", "Black-Yellow", "J905-3"),
}
UNUSED_FLIPPER_SWITCHES = {117: ("Black-Gray", "J906-5", "Upper Left Flipper EOS"), 118: ("Black-Blue", "J905-5", "Upper Left Flipper Opto")}
# CPU DIP positions SW1-SW8 against the printed Dip Switch Chart (PDF page 2).
DIP_COUNTRY_CHART = {
	"America": ("Off", "Off", "On", "On", "On", "On", "On", "On"),
	"Euopean": ("Off", "Off", "On", "On", "On", "Off", "On", "On"),
	"French": ("Off", "Off", "On", "On", "On", "On", "Off", "Off"),
	"German": ("Off", "Off", "On", "On", "On", "On", "On", "Off"),
	"Spain": ("Off", "Off", "On", "On", "Off", "On", "On", "On"),
}

# --- Normalized playfield coordinates from the retained VPW Mod 1.0 table, x/975 and y/1974
# (external:pinmame-review-artifacts/the-shadow/vpw-object-positions.json).
SWITCH_POSITIONS = {
	15: (0.85151, 0.722253), 16: (0.781007, 0.721486), 17: (0.11881, 0.72242), 18: (0.044916, 0.722387),
	25: (0.096494, 0.555991), 26: (0.096494, 0.525455), 27: (0.824194, 0.553743), 28: (0.835424, 0.5249),
	31: (0.265587, 0.427159), 32: (0.72729, 0.213515), 33: (0.554872, 0.174265), 35: (0.345672, 0.423151),
	36: (0.189547, 0.287608), 37: (0.060895, 0.214383), 38: (0.362844, 0.21537),
	41: (0.866575, 0.873897), 42: (0.866575, 0.873897), 43: (0.866575, 0.873897), 44: (0.866575, 0.873897),
	45: (0.866575, 0.873897), 46: (0.866575, 0.873897), 47: (0.284323, 0.208848), 48: (0.934218, 0.904409),
	51: (0.55453, 0.120905), 52: (0.235109, 0.48471), 53: (0.35837, 0.470268), 54: (0.078633, 0.297872),
	55: (0.421425, 0.15843), 56: (0.484001, 0.196511), 57: (0.922735, 0.168787), 58: (0.472821, 0.035799),
	61: (0.215103, 0.719041), 62: (0.674512, 0.718964), 63: (0.707675, 0.079858), 64: (0.707675, 0.079858),
	65: (0.707675, 0.079858), 66: (0.326137, 0.36152), 67: (0.83759, 0.200763), 68: (0.455185, 0.119123),
	71: (0.017436, 0.08346), 72: (0.017436, 0.118668), 73: (0.017436, 0.153875), 74: (0.017436, 0.188956),
	75: (0.085115, 0.390353), 76: (0.393422, 0.35732), 77: (0.547931, 0.123008), 78: (0.925792, 0.21582),
	81: (0.352308, 0.189032), 82: (0.355897, 0.153698), 84: (0.352308, 0.082474),
	85: (0.07955, 0.065563), 86: (0.149123, 0.065563), 87: (0.217555, 0.065504), 88: (0.287668, 0.065504),
}
SWITCH_OBJECTS = {
	15: "Trigger sw15", 16: "Trigger sw16", 17: "Trigger sw17", 18: "Trigger sw18", 25: "HitTarget sw25",
	26: "HitTarget sw26", 27: "HitTarget sw27", 28: "HitTarget sw28", 31: "Trigger sw31", 32: "Trigger sw32",
	33: "Trigger sw33", 35: "Wall sw35 (bounding-box center of its drag points)", 37: "Trigger sw37", 38: "Trigger sw38",
	47: "Trigger sw47", 48: "Trigger ShooterLane (the script's shooterlane handler)", 51: "Wall WallTarget (bounding-box center of its drag points)",
	52: "HitTarget sw52", 53: "HitTarget sw53", 54: "Trigger sw54", 55: "Wall sw55 (bounding-box center of its drag points)",
	56: "HitTarget sw56", 57: "Trigger sw57", 58: "Trigger sw58",
	61: "Wall Leftslingshot (bounding-box center of its drag points)",
	62: "Wall Rightslingshot (bounding-box center of its drag points)", 66: "Kicker sw66", 67: "Kicker sw67",
	68: "Kicker Popper", 71: "Wall sw71", 72: "Wall sw72", 73: "Wall sw73", 74: "Wall sw74", 75: "Trigger sw75",
	76: "Trigger SW76", 77: "Trigger sw77", 78: "Trigger sw78", 81: "Wall sw81", 82: "Wall sw82", 84: "Wall sw84",
	85: "Wall sw85", 86: "Wall sw86", 87: "Wall sw87", 88: "Wall sw88",
}
SWITCH_PROJECTIONS = {
	**{
		address: (
			"Projected onto the trough eject kicker (Kicker BallRelease): the retained script's cvpmBallStack holds the "
			"balls virtually on 41-45 (InitSw 0, 41, 42, 43, 44, 45) and the table has no object for the individual "
			"trough opto positions or for Top Trough 46; the manual draws the A-18753 outhole ball trough at the lower right."
		)
		for address in (41, 42, 43, 44, 45, 46)
	},
	36: (
		"Projected onto the Battlefield kicker head (Primitive SlingMiniPF, a mesh baked at world coordinates whose vertex "
		"bounding-box center is used, at the head's middle position): the Mini Kicker opto rides on the moving A-19070 "
		"coil/slide assembly, and the retained script pulses 36 from the Slingshot events of the nineteen position walls "
		"bf_k01-bf_k19 that it switches with Controller.GetMech(0)."
	),
	63: (
		"Projected onto the lockup kicker (Kicker Lockup): the retained script's cvpmBallStack bsLock holds the locked "
		"balls virtually on 63-65 (InitSw 0, 63, 64, 65) and the table has no object per lock position."
	),
	64: "Projected onto the lockup kicker (Kicker Lockup); see switch 63.",
	65: "Projected onto the lockup kicker (Kicker Lockup); see switch 63.",
}

SOLENOID_LABELS = {
	1: "Ball Launch", 2: "Lockup Kickout", 3: "Left Diverter Left", 4: "Left Diverter Right", 5: "Right Diverter Right",
	6: "Right Diverter Left", 7: "Knocker", 8: "Wall Target Up", 9: "Left Slingshot", 10: "Right Slingshot",
	11: "Right Eject", 12: "Left Eject", 13: "Ball Release", 14: "Ball Popper", 15: "Mini Kicker", 16: "Wall Target Down",
	17: "Mini Playfield Flasher", 18: "Left Side Flasher", 19: "Mini Motor Right", 20: "Mini Motor Left",
	21: "Right Side Flasher", 22: "Right Ramp Flasher", 23: "Left Ramp Flasher", 24: "Mini Drop Bank",
	25: "Single Drop Up", 26: "Left Back Flasher", 27: "Center Back Flasher", 28: "Right Back Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold", 35: "Magnet", 36: "Single Drop Down",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
FLASHERS = {17, 18, 21, 22, 23, 26, 27, 28}
MOTORS = {19, 20}
MAGNETS = {35}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B",
	31: "WPC Game-On State", 32: "Unused WPC State Channel 32",
	**{address: f"Unused WPC-Security Output {address}" for address in range(37, 45)},
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
	51: "PinMAME Magnet Hold-Down Countdown",
}
# address -> (printed type, voltage connection, transistor, drive connection, drive wire, part / lamp type)
SOLENOID_WIRING = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "Vio-Brn", "AE-23-800"),
	2: ("High Power", "J107-2", "Q80", "J130-2", "Vio-Red", "A-14189"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "Vio-Org", "AE-25-1000"),
	4: ("High Power", "J107-2", "Q76", "J130-5", "Vio-Yel", "AE-25-1000"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "Vio-Grn", "AE-25-1000"),
	6: ("High Power", "J107-2", "Q66", "J130-7", "Vio-Blu", "AE-25-1000"),
	7: ("High Power", "J107-2 (Backbox)", "Q68", "J130-8 (Backbox)", "Vio-Blk", "AE-23-800"),
	8: ("High Power", "J107-2", "Q70", "J130-9", "Vio-Gry", "AE-23-800"),
	9: ("Low Power", "J107-3", "Q58", "J127-1", "Brn-Blk", "AE-26-1200"),
	10: ("Low Power", "J107-3", "Q56", "J127-3", "Brn-Red", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "Brn-Org", "AE-27-1200"),
	12: ("Low Power", "J107-3", "Q52", "J127-5", "Brn-Yel", "AE-26-1500"),
	13: ("Low Power", "J107-3", "Q50", "J127-6", "Brn-Grn", "AE-26-1500"),
	14: ("Low Power", "J107-3", "Q48", "J127-7", "Brn-Blu", "AE-25-1000"),
	15: ("Low Power", "J107-3", "Q46", "J127-8", "Brn-Vio", "AE-25-1000"),
	16: ("Low Power", "J107-3", "Q44", "J127-9", "Brn-Gry", "SM-30-1100-DC"),
	17: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q42", "J126-1 (Playfield) / J125-1 (Backbox)", "Blk-Brn", "#89 playfield, #906 (2) backbox"),
	18: ("Flasher", "J107-6 (Playfield) / J106-5 (Backbox)", "Q40", "J126-2 (Playfield) / J125-2 (Backbox)", "Blk-Red", "#89 playfield, #906 backbox"),
	19: ("Flasher", "J116-2", "Q38", "J126-3", "Blk-Org", "14-8014"),
	20: ("Flasher", "J116-2", "Q36", "J126-4", "Blk-Yel", "14-8014"),
	21: ("Flasher", "J107-6", "Q28", "J126-5", "Blu-Grn", "#906, #89"),
	22: ("Flasher", "J107-6", "Q30", "J126-6", "Blu-Blk", "#906, #89"),
	23: ("Flasher", "J107-6", "Q34", "J126-7", "Blu-Vio", "#906, #89"),
	24: ("Flasher", "J107-1", "Q32", "J126-8", "Blu-Gry", "AE-25-1000"),
	25: ("Gen. Purpose", "J107-1", "Q26", "J122-1", "Blu-Brn", "AE-26-1200"),
	26: ("Gen. Purpose", "J107-6 (Playfield) / J106-5 (Backbox)", "Q24", "J122-2 (Playfield) / J124-2 (Backbox)", "Blu-Red", "#906 playfield, #906 backbox"),
	27: ("Gen. Purpose", "J107-6 (Playfield) / J106-5 (Backbox)", "Q22", "J122-3 (Playfield) / J124-3 (Backbox)", "Blu-Org", "#906 playfield, #906 backbox"),
	28: ("Gen. Purpose", "J107-6 (Playfield) / J106-5 (Backbox)", "Q20", "J122-4 (Playfield) / J124-5 (Backbox)", "Blu-Yel", "#906 playfield, #906 backbox"),
	33: ("Fliptronic power", "J907-6 (Red-Vio)", "Q2", "J902-6", "Yel-Vio", "FL-15411"),
	34: ("Fliptronic hold", "J907-6 (Red-Vio)", "Q7", "J902-4", "Org-Vio", "FL-15411"),
	35: ("High Power", "J907-8,9", "Q1", "J902-3", "Yel-Gry", "20-9247"),
	36: ("Low Power", "J907-8,9", "Q5", "J902-1", "Org-Gry", "SM1-26-600"),
	45: ("Fliptronic power", "J907-1 (Red-Grn)", "Q4", "J902-13", "Yel-Grn", "FL-11629"),
	46: ("Fliptronic hold", "J907-1 (Red-Grn)", "Q11", "J902-11", "Org-Grn", "FL-11629"),
	47: ("Fliptronic power", "J907-4 (Red-Blu)", "Q3", "J902-9", "Yel-Blu", "FL-11629"),
	48: ("Fliptronic hold", "J907-4 (Red-Blu)", "Q9", "J902-7", "Org-Blu", "FL-11629"),
}
# Printed flipper-circuit numbers (manual.address aliases) for the public Fliptronic addresses.
PRINTED_FLIPPER_CIRCUITS = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34"}
SOLENOID_ASSEMBLIES = {
	1: "A-14525", 2: "A-18952", 3: "A-18954", 4: "A-18954", 5: "A-18955", 6: "A-18955", 7: "B-10686-1",
	8: "A-18622", 9: "B-9362-R-3", 10: "B-9362-L-2", 11: "A-15368", 12: "A-18768", 13: "A-18753", 14: "A-18950",
	15: "A-19070", 16: "A-18622", 17: "A-17803", 18: "A-17983", 19: "A-19170", 20: "A-19170", 21: "A-17983 with B-12156",
	22: "A-17983 with B-12156", 23: "A-17983 with A-12156", 24: "A-18783", 25: "A-19642", 26: "B-12156", 27: "B-12156",
	28: "B-12156", 33: "A-15849-R-4", 34: "A-15849-R-4", 35: "A-18388", 36: "A-19642", 45: "A-15849-R-2",
	46: "A-15849-R-2", 47: "A-15849-L-2", 48: "A-15849-L-2",
}
SOLENOID_CALLBACKS = {
	1: "Auto_Plunger (fires the cvpmImpulseP plunger at swplunger)", 2: "SolLockupKickout (ejects bsLock through LockupKickerEject 250 ms later)",
	3: "SolLeftPhurbaLeft", 4: "SolLeftPhurbaRight", 5: "SolRightPhurbaRight", 6: "SolRightPhurbaLeft", 7: "SolKnocker",
	8: "SolWallTargetUp (raises WallTarget and releases switch 51)", 9: "solLSling", 10: "solRSling",
	11: "bsRightEject.SolOut (saucer sw67)", 12: "bsLeftEject.SolOut (saucer sw66)", 13: "SolBallRelease (bsTrough)",
	14: "SolBallPopper (lifts the ball from Popper to PopperEject and releases switch 68)",
	16: "SolWallTargetDown (drops WallTarget and closes switch 51)",
	17: "SolModCallback(17) = SolFlash17, which only sets the helper light L117 parked off the playfield (x < 0)",
	18: "SolModCallback(18) = SolFlash18, which only sets the helper light L118 parked off the playfield (x < 0)",
	21: "SolModCallback(21) = SolFlash21 (ModFlashFlasher 1, Flupper dome 1)", 22: "SolModCallback(22) = SolFlash22 (ModFlashFlasher 2, Flupper dome 2)",
	23: "SolModCallback(23) = SolFlash23 (ModFlashFlasher 3, Flupper dome 3)", 24: "SolMiniDropbank (resets the four mini drops and opens 85-88)",
	25: "SolSingleDropUp (raises sw55 and opens switch 55)",
	26: "SolModCallback(26) = SolFlash26 (ModFlashFlasher 4, Flupper dome 4, and helper light L126)",
	27: "SolModCallback(27) = SolFlash27 (ModFlashFlasher 5, Flupper dome 5, and helper light L127)",
	28: "SolModCallback(28) = SolFlash28 (ModFlashFlasher 6, Flupper dome 6, and helper light L128)",
	35: "SolMagnetOn (catches and holds a ball at MagnetHold, releases it when the magnet drops)",
	36: "SolSingleDropDown (drops sw55 and closes switch 55)",
	46: "SolRFlipper through SolCallback(sLRFlipper); its RightFlipper2 lines are commented out, so it moves only the lower right flipper",
	48: "SolLFlipper through SolCallback(sLLFlipper)",
}
SOLENOID_POSITIONS = {
	1: [(0.934616, 0.909387)], 2: [(0.818445, 0.114981)], 3: [(0.243063, 0.382423)], 4: [(0.243063, 0.382423)],
	5: [(0.766178, 0.152853)], 6: [(0.766178, 0.152853)], 8: [(0.55453, 0.120905)], 9: [(0.215103, 0.719041)],
	10: [(0.674512, 0.718964)], 11: [(0.83759, 0.200763)], 12: [(0.326137, 0.36152)], 13: [(0.866575, 0.873897)],
	14: [(0.455185, 0.119123)], 15: [(0.189547, 0.287608)], 16: [(0.55453, 0.120905)], 19: [(0.189547, 0.287608)], 20: [(0.189547, 0.287608)],
	21: [(0.860255, 0.349046)], 22: [(0.863611, 0.230943)], 23: [(0.066094, 0.357522)], 24: [(0.183339, 0.065534)],
	25: [(0.421425, 0.15843)], 26: [(0.591069, 0.0089)], 27: [(0.74644, 0.0089)], 28: [(0.900849, 0.0089)],
	33: [(0.898598, 0.44595)], 34: [(0.898598, 0.44595)], 35: [(0.553504, 0.172914)], 36: [(0.421425, 0.15843)],
	45: [(0.608205, 0.843465)], 46: [(0.608205, 0.843465)], 47: [(0.282051, 0.843465)], 48: [(0.282051, 0.843465)],
}
SOLENOID_OBJECTS = {
	1: "Trigger swplunger (the cvpmImpulseP launch position)", 2: "Kicker LockupKickerEject",
	3: "midpoint of the left diverter's two baked blade meshes Div_Bot_Left and Div_Bot_Right (vertex bounding-box centers)",
	4: "midpoint of the left diverter's two baked blade meshes Div_Bot_Left and Div_Bot_Right (vertex bounding-box centers)",
	5: "midpoint of the right diverter's two baked blade meshes Div_Top_Left and Div_Top_Right (vertex bounding-box centers)",
	6: "midpoint of the right diverter's two baked blade meshes Div_Top_Left and Div_Top_Right (vertex bounding-box centers)",
	8: "Wall WallTarget bounding-box center", 9: "Wall Leftslingshot bounding-box center",
	10: "Wall Rightslingshot bounding-box center", 11: "Kicker sw67", 12: "Kicker sw66", 13: "Kicker BallRelease",
	14: "Kicker Popper", 15: "Primitive SlingMiniPF, the Battlefield kicker head (vertex bounding-box center)",
	16: "Wall WallTarget bounding-box center",
	19: "Primitive SlingMiniPF, the kicker head the coil slide motor drives along the bf_k01-bf_k19 rail",
	20: "Primitive SlingMiniPF, the kicker head the coil slide motor drives along the bf_k01-bf_k19 rail",
	21: "Flupper dome Primitive Flasherbase1 (one of the two printed sockets)",
	22: "Flupper dome Primitive Flasherbase2 (one of the two printed sockets)",
	23: "Flupper dome Primitive Flasherbase3 (one of the two printed sockets)",
	24: "midpoint between the two middle mini drop targets sw86 and sw87",
	25: "Wall sw55 bounding-box center", 26: "Flupper dome Primitive Flasherbase4", 27: "Flupper dome Primitive Flasherbase5",
	28: "Flupper dome Primitive Flasherbase6", 33: "Flipper RightFlipper2", 34: "Flipper RightFlipper2",
	35: "Kicker MagnetHold", 36: "Wall sw55 bounding-box center",
	45: "Flipper RightFlipper", 46: "Flipper RightFlipper", 47: "Flipper LeftFlipper", 48: "Flipper LeftFlipper",
}
# Playfield flasher sockets printed per flasher output (the backbox bulbs are not counted).
FLASHER_QUANTITIES = {17: 1, 18: 1, 21: 2, 22: 2, 23: 2, 26: 1, 27: 1, 28: 1}
# Solenoid placements derived from table geometry rather than read off one object's own center.
_DIVERTER_PROJECTION = (
	"Projection: the midpoint of the {side} diverter's two baked blade meshes {a} and {b}, each taken as the center of "
	"its vertex bounding box in the retained extraction's .obj (world x = obj x, world y = obj y); the coil sits under "
	"the blades, and the table models no coil object."
)
_KICKER_HEAD_PROJECTION = (
	"Projection: the vertex bounding-box center of the baked kicker-head mesh SlingMiniPF (world x = obj x, world y = obj y); "
	"the head travels along the bf_k01-bf_k19 rail, so this is its modelled resting position, not a fixed socket."
)
SOLENOID_PROJECTIONS = {
	3: _DIVERTER_PROJECTION.format(side="left", a="Div_Bot_Left", b="Div_Bot_Right"),
	4: _DIVERTER_PROJECTION.format(side="left", a="Div_Bot_Left", b="Div_Bot_Right"),
	5: _DIVERTER_PROJECTION.format(side="right", a="Div_Top_Left", b="Div_Top_Right"),
	6: _DIVERTER_PROJECTION.format(side="right", a="Div_Top_Left", b="Div_Top_Right"),
	15: _KICKER_HEAD_PROJECTION,
	19: _KICKER_HEAD_PROJECTION,
	20: _KICKER_HEAD_PROJECTION,
	24: (
		"Projection: the midpoint of the drag-point bounding-box centers of the two middle Battlefield drop-target walls "
		"sw86 and sw87; the reset coil sits under the bank, and the table models no coil object."
	),
}
# How each derived placement is recomputed from the retained extraction (checked by an evidence-gated test).
DERIVED_PLACEMENTS = {
	("pinmame.output.solenoid", 3): ("mesh", ("Div_Bot_Left", "Div_Bot_Right")),
	("pinmame.output.solenoid", 4): ("mesh", ("Div_Bot_Left", "Div_Bot_Right")),
	("pinmame.output.solenoid", 5): ("mesh", ("Div_Top_Left", "Div_Top_Right")),
	("pinmame.output.solenoid", 6): ("mesh", ("Div_Top_Left", "Div_Top_Right")),
	("pinmame.output.solenoid", 15): ("mesh", ("SlingMiniPF",)),
	("pinmame.output.solenoid", 19): ("mesh", ("SlingMiniPF",)),
	("pinmame.output.solenoid", 20): ("mesh", ("SlingMiniPF",)),
	("pinmame.output.solenoid", 24): ("wall", ("sw86", "sw87")),
	("pinmame.input.switch", 36): ("mesh", ("SlingMiniPF",)),
}

# --- Lamp matrix (manual printed 2-38) and lamp locations (2-38/2-39).
LAMP_LABELS = {
	11: "Shoot Again", 12: "Left Outlane", 13: "Left Return Lane", 14: "Right Return Lane", 15: "Right Outlane",
	16: "MONGO(L)", 17: "Right Loop Arrow", 18: "Right Mongol Hurry",
	21: "Left Ramp Jackpot", 22: "MON(G)OL", 23: "Left Ramp Arrow", 24: "MO(N)GOL", 25: "M(O)NGOL", 26: "(M)ONGOL",
	27: "Farley Claymore", 28: "Underwater Doom",
	31: "Scarf Scenes Complete", 32: "Scarf Battlefield", 33: "Scarf Shadow Multiball", 34: "Scarf Khan Multiball",
	35: "Punish Guilty", 36: "Duel of Wills", 37: "Beryllium Sphere", 38: "Hotel Monolith",
	41: "Right Ramp Arrow", 42: "Right Ramp Jackpot", 43: "\"Start Scene\"", 44: "Who Knows", 45: "Extra Ball",
	46: "Final Battle", 47: "Shadow Loop", 48: "Inner Loop Jackpot",
	51: "Lock 2", 52: "Lock 3", 53: "Lock 1", 54: "Inner Sanctum Arrow", 55: "Center Standup", 56: "Battlefield Ready",
	57: "Battle Drop Jackpot", 58: "Inner Loop Arrow",
	61: "Mini Left Standup 4", 62: "Mini Left Standup 3", 63: "Mini Left Standup 2", 64: "Mini Left Standup 1",
	65: "Mini Top Center Left", 66: "Khan Multiball", 67: "Super Jackpot", 68: "Battle Drop Arrow",
	71: "Mini Right Standup 4", 72: "Mini Right Standup 3", 73: "Mini Right Standup 2", 74: "Mini Right Standup 1",
	75: "Mini Top Center Right", 76: "Left Loop Jackpot", 77: "Left Mongol Hurry", 78: "Left Loop Arrow",
	81: "Left Ramp Left Ring", 82: "Left Ramp Right Ring", 83: "Right Ramp Left Ring", 84: "Right Ramp Right Ring",
	85: "Right Eject Arrow", 86: "MONG(O)L", 87: "Buy-In Button", 88: "Credit Button",
}
LAMP_BULBS = {
	**{address: "24-6549" for address in (11, 12, 13, 14, 15, 16, 17, 18, 65, 75, 85, 86)},
	**{address: "24-8855" for address in (81, 82, 83, 84)},
}
LAMP_ASSEMBLIES = {
	11: "A-17807", 12: "A-17807", 13: "A-17835", 14: "A-17835", 15: "A-17835", 16: "A-17835", 17: "A-17807", 18: "A-17807",
	**{address: "A-19108" for address in (21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38)},
	**{address: "A-19109" for address in (41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 66, 67, 68)},
	**{address: "A-19107" for address in (61, 62, 63, 64, 71, 72, 73, 74)},
	65: "A-17807", 75: "A-17807", 76: "A-17624", 77: "A-17624", 78: "A-17624",
	81: "A-19545-1", 82: "A-19545-2", 83: "A-19545-1", 84: "A-19545-2", 85: "A-17807", 86: "A-17835",
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"), 3: ("Red-Orange", "J133-4", "Q88"),
	4: ("Red-Yellow", "J133-5", "Q87"), 5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}
LAMP_POSITIONS = {
	11: (0.444814, 0.877632), 12: (0.046126, 0.672596), 13: (0.121093, 0.671811), 14: (0.778378, 0.671384),
	15: (0.852386, 0.671628), 16: (0.769053, 0.556994), 17: (0.913141, 0.269062), 18: (0.905507, 0.312345),
	21: (0.340076, 0.560362), 22: (0.382902, 0.501839), 23: (0.31901, 0.519367), 24: (0.248763, 0.516925),
	25: (0.14897, 0.529083), 26: (0.14957, 0.56478), 27: (0.281013, 0.632337), 28: (0.368767, 0.682356),
	31: (0.475233, 0.509506), 32: (0.527098, 0.538918), 33: (0.591688, 0.562401), 34: (0.667564, 0.579241),
	35: (0.446181, 0.592959), 36: (0.445543, 0.6362), 37: (0.609556, 0.631674), 38: (0.52388, 0.681407),
	41: (0.661715, 0.338197), 42: (0.646049, 0.377853), 43: (0.781233, 0.349936), 44: (0.757642, 0.383914),
	45: (0.735612, 0.417092), 46: (0.711541, 0.449928), 47: (0.621973, 0.410673), 48: (0.526645, 0.382478),
	51: (0.543084, 0.305103), 52: (0.542954, 0.328974), 53: (0.543657, 0.281776), 54: (0.541959, 0.248004),
	55: (0.485555, 0.227074), 56: (0.434509, 0.263364), 57: (0.446447, 0.298511), 58: (0.455071, 0.355538),
	61: (0.087069, 0.208946), 62: (0.088241, 0.171721), 63: (0.089477, 0.135544), 64: (0.088965, 0.098874),
	65: (0.152409, 0.099658), 66: (0.572555, 0.448255), 67: (0.5095, 0.42432), 68: (0.423813, 0.226882),
	71: (0.288938, 0.208129), 72: (0.287723, 0.171321), 73: (0.28671, 0.134728), 74: (0.285338, 0.099699),
	75: (0.220557, 0.099083), 76: (0.150802, 0.477034), 77: (0.128692, 0.437382), 78: (0.107344, 0.396465),
	85: (0.801471, 0.313278), 86: (0.782978, 0.522526),
}
# Ramp ring lamps: the VPW table maps 81-84 to off-playfield helper lights (l81-l84, x < 0) and models no bulb; the
# Skitso script binds them to the glow sprites F181-F184, which are not sockets, so 81-84 stay unplaced.
RING_LAMPS = (81, 82, 83, 84)

# (label, triac-switched return pin, triac, 6.8VAC supply pin, return wire, supply wire, bulbs). The table prints the
# return pin under "Voltage" and the supply pin under "Drive"; the printed 3-10 G.I. circuit puts the triac on the return
# side, and the 3-28 connector list names each pin (return colours from the list, supply colours from the table).
GI_STRINGS = {
	0: ("Bottom Playfield", "J121-1 (Playfield)", "Q18", "J121-7 (Playfield)", "Brown", "Wht-Brn", "#44 playfield"),
	1: ("Top Left Playfield", "J121-2 (Playfield)", "Q10", "J121-8 (Playfield)", "Orange", "Wht-Org", "#44 playfield"),
	2: ("Insert Bottom", "J120-3 (Backbox)", "Q14", "J120-9 (Backbox)", "Yellow", "Wht-Yel", "#555 backbox"),
	3: ("Insert Top", "J120-5 (Backbox)", "Q16", "J120-10 (Backbox)", "Green", "Wht-Grn", "#555 backbox"),
	4: ("Top Right Playfield", "J121-6 (Playfield)", "Q12", "J121-11 (Playfield)", "Violet", "Wht-Vio", "#44 playfield"),
}
GI_COLLECTIONS = {0: "aGiBottomLights", 1: "aGiLeftLights", 4: "aGiRightLights"}
GI_CONNECTOR_LIST_NOTE = (
	"The power driver board connector list (manual printed 3-28) labels J120 'to playfield' and J121 'to insert', the "
	"reverse of the G.I. table's Playfield/Backbox columns. The table, printed identically three times (PDF pages 2, 137 "
	"and 151), agrees with itself on columns, bulbs and names: J121 strings 01, 02 and 05 carry #44 playfield bulbs and are "
	"named Bottom, Top Left and Top Right Playfield, and J120 strings 03 and 04 carry #555 backbox bulbs and are named "
	"Insert Bottom and Insert Top. The VPW script dispatches 01, 02 and 05 to playfield light collections and marks 03 and "
	"04 'Not on playfield'. The connector list also misprints two pins (J121-8 'Not Used', where string 02's Wht-Org feed "
	"lands, and a White-Green feed on J121-10), so the table is recorded."
)
# One Light per distinct position in each playfield G.I. collection (co-located duplicates share one entry).
GI_POSITIONS = {
	0: [
		(0.224757, 0.823959), (0.119493, 0.792683), (0.678281, 0.822889), (0.773551, 0.795714),
		(0.209134, 0.75281), (0.684957, 0.748166), (0.172872, 0.698484), (0.708045, 0.707508),
	],
	1: [
		(0.06154, 0.551849), (0.049742, 0.441944), (0.190074, 0.404941), (0.139912, 0.298051), (0.329482, 0.405712),
		(0.522198, 0.07526), (0.534355, 0.020033), (0.366901, 0.043085), (0.400531, 0.051187), (0.050479, 0.459501),
		(0.037256, 0.389591),
	],
	4: [
		(0.946395, 0.727328), (0.953704, 0.623538), (0.860455, 0.55504), (0.942012, 0.422115),
		(0.770545, 0.202813), (0.89461, 0.056385), (0.716205, 0.014588), (0.612668, 0.169303),
	],
}
GI_EXCLUDED = {
	0: "nothing: its eight lights LB1-LB8 each stand at their own position",
	1: "the co-located duplicates LB10, LB31, LB30, LB16 and LB37",
	4: "the wide fill LB13 (falloff 350) and the co-located duplicates LB23, LB14, LB38 and LB33",
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
		raise RuntimeError(f"The Shadow retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained The Shadow extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"The Shadow retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"The Shadow retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"The Shadow retained extraction identity mismatch: {identity}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "observed") -> dict[str, Any]:
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


# (excerpt id suffix, transcription file, locator, image derivation)
MANUAL_EXCERPTS: tuple[tuple[str, str, str, str], ...] = (
	("switch-matrix-1", "switch-matrix.md", "PDF page 135, printed page 2-40, SWITCH MATRIX columns 1-4, rows 1-4, with the dedicated grounded switches D1-D4", "Manual_Bally_1994_The_Shadow.pdf page 135, crop box 0.17,0.075,0.58,0.305, scanned page rendered at its native resolution (embedded image xref 536, 2550px across 8.50in), rendered at 258 dpi, capped to 900px wide, grayscale, 901x654 WebP quality 80"),
	("switch-matrix-2", "switch-matrix.md", "PDF page 135, printed page 2-40, SWITCH MATRIX columns 4-8, rows 1-4, with the flipper grounded switches F1-F4", "Manual_Bally_1994_The_Shadow.pdf page 135, crop box 0.55,0.075,0.93,0.305, scanned page rendered at its native resolution (embedded image xref 536, 2550px across 8.50in), rendered at 279 dpi, capped to 900px wide, grayscale, 901x706 WebP quality 80"),
	("switch-matrix-3", "switch-matrix.md", "PDF page 135, printed page 2-40, SWITCH MATRIX columns 1-4, rows 5-8, with the dedicated grounded switches D5-D8", "Manual_Bally_1994_The_Shadow.pdf page 135, crop box 0.17,0.295,0.58,0.53, scanned page rendered at its native resolution (embedded image xref 536, 2550px across 8.50in), rendered at 244 dpi, capped to 850px wide, grayscale, 851x631 WebP quality 80"),
	("switch-matrix-4", "switch-matrix.md", "PDF page 135, printed page 2-40, SWITCH MATRIX columns 4-8, rows 5-8, with the flipper grounded switches F5-F8", "Manual_Bally_1994_The_Shadow.pdf page 135, crop box 0.55,0.295,0.93,0.53, scanned page rendered at its native resolution (embedded image xref 536, 2550px across 8.50in), rendered at 232 dpi, capped to 750px wide, grayscale, 751x601 WebP quality 80"),
	("switch-locations-1", "switch-locations.md", "PDF page 135, printed page 2-40, SWITCH LOCATIONS items F1-43", "Manual_Bally_1994_The_Shadow.pdf page 135, crop box 0.13,0.56,0.97,0.875, scanned page rendered at its native resolution (embedded image xref 536, 2550px across 8.50in), rendered at 189 dpi, capped to 1350px wide, grayscale, 1351x656 WebP quality 80"),
	("switch-locations-2", "switch-locations.md", "PDF page 136, printed page 2-41, SWITCH LOCATIONS (continued) items 44-88", "Manual_Bally_1994_The_Shadow.pdf page 136, crop box 0.1,0.59,0.92,0.88, scanned page rendered at its native resolution (embedded image xref 541, 2550px across 8.50in), rendered at 179 dpi, capped to 1250px wide, grayscale, 1251x574 WebP quality 80"),
	("lamp-matrix-1", "lamp-matrix.md", "PDF page 133, printed page 2-38, LAMP MATRIX columns 1-4, rows 1-4", "Manual_Bally_1994_The_Shadow.pdf page 133, crop box 0.18,0.075,0.6,0.31, scanned page rendered at its native resolution (embedded image xref 528, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1071x776 WebP quality 80"),
	("lamp-matrix-2", "lamp-matrix.md", "PDF page 133, printed page 2-38, LAMP MATRIX columns 4-8, rows 1-4", "Manual_Bally_1994_The_Shadow.pdf page 133, crop box 0.55,0.075,0.91,0.31, scanned page rendered at its native resolution (embedded image xref 528, 2550px across 8.50in), rendered at 300 dpi, grayscale, 919x776 WebP quality 80"),
	("lamp-matrix-3", "lamp-matrix.md", "PDF page 133, printed page 2-38, LAMP MATRIX columns 1-4, rows 5-8", "Manual_Bally_1994_The_Shadow.pdf page 133, crop box 0.18,0.3,0.6,0.49, scanned page rendered at its native resolution (embedded image xref 528, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1071x627 WebP quality 80"),
	("lamp-matrix-4", "lamp-matrix.md", "PDF page 133, printed page 2-38, LAMP MATRIX columns 4-8, rows 5-8", "Manual_Bally_1994_The_Shadow.pdf page 133, crop box 0.55,0.3,0.91,0.49, scanned page rendered at its native resolution (embedded image xref 528, 2550px across 8.50in), rendered at 300 dpi, grayscale, 919x627 WebP quality 80"),
	("lamp-locations-1", "lamp-locations.md", "PDF page 133, printed page 2-38, LAMP LOCATIONS items 11-48", "Manual_Bally_1994_The_Shadow.pdf page 133, crop box 0.13,0.53,0.97,0.84, scanned page rendered at its native resolution (embedded image xref 528, 2550px across 8.50in), rendered at 154 dpi, capped to 1100px wide, grayscale, 1101x526 WebP quality 80"),
	("lamp-locations-2", "lamp-locations.md", "PDF page 134, printed page 2-39, LAMP LOCATIONS (continued) items 51-88", "Manual_Bally_1994_The_Shadow.pdf page 134, crop box 0.08,0.56,0.93,0.86, scanned page rendered at its native resolution (embedded image xref 532, 2550px across 8.50in), rendered at 152 dpi, capped to 1100px wide, grayscale, 1101x504 WebP quality 80"),
	("solenoid-flasher-table-1", "solenoid-flasher-table.md", "PDF page 137, printed page 2-42, SOLENOID/FLASHER TABLE rows 01-15", "Manual_Bally_1994_The_Shadow.pdf page 137, crop box 0.1,0.07,0.95,0.3, scanned page rendered at its native resolution (embedded image xref 545, 2550px across 8.50in), rendered at 159 dpi, capped to 1150px wide, grayscale, 1151x404 WebP quality 80"),
	("solenoid-flasher-table-2", "solenoid-flasher-table.md", "PDF page 137, printed page 2-42, SOLENOID/FLASHER TABLE rows 15-36 and General Illumination", "Manual_Bally_1994_The_Shadow.pdf page 137, crop box 0.1,0.29,0.95,0.53, scanned page rendered at its native resolution (embedded image xref 545, 2550px across 8.50in), rendered at 145 dpi, capped to 1050px wide, grayscale, 1051x385 WebP quality 80"),
	("solenoid-flasher-table-3", "solenoid-flasher-table.md", "PDF page 137, printed page 2-42, SOLENOID/FLASHER TABLE Flipper Circuits and footnotes", "Manual_Bally_1994_The_Shadow.pdf page 137, crop box 0.1,0.52,0.95,0.665, scanned page rendered at its native resolution (embedded image xref 545, 2550px across 8.50in), rendered at 221 dpi, capped to 1600px wide, grayscale, 1601x354 WebP quality 80"),
	("solenoid-flasher-locations-1", "solenoid-flasher-locations.md", "PDF page 137, printed page 2-42, SOLENOID/FLASHER LOCATIONS items 01-20", "Manual_Bally_1994_The_Shadow.pdf page 137, crop box 0.1,0.695,0.97,0.905, scanned page rendered at its native resolution (embedded image xref 545, 2550px across 8.50in), rendered at 216 dpi, capped to 1600px wide, grayscale, 1601x500 WebP quality 80"),
	("solenoid-flasher-locations-2", "solenoid-flasher-locations.md", "PDF page 138, printed page 2-43, SOLENOID/FLASHER LOCATIONS (continued), General Illumination Circuits and Flipper Coils", "Manual_Bally_1994_The_Shadow.pdf page 138, crop box 0.08,0.645,0.9,0.9, scanned page rendered at its native resolution (embedded image xref 549, 2550px across 8.50in), rendered at 208 dpi, capped to 1450px wide, grayscale, 1451x584 WebP quality 80"),
	("power-driver-gi-connectors-1", "power-driver-gi-connectors.md", "PDF page 173, printed page 3-28, power driver board connector list, J120 block", "Manual_Bally_1994_The_Shadow.pdf page 173, crop box 0.155,0.608,0.55,0.765, scanned page rendered at its native resolution (embedded image xref 689, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1008x519 WebP quality 80"),
	("power-driver-gi-connectors-2", "power-driver-gi-connectors.md", "PDF page 173, printed page 3-28, power driver board connector list, J121 block", "Manual_Bally_1994_The_Shadow.pdf page 173, crop box 0.565,0.06,0.945,0.22, scanned page rendered at its native resolution (embedded image xref 689, 2550px across 8.50in), rendered at 300 dpi, grayscale, 970x528 WebP quality 80"),
	("dip-switch-chart", "dip-switch-chart.md", "PDF page 2, DIP SWITCH SETTINGS AND JUMPERS", "Manual_Bally_1994_The_Shadow.pdf page 2, crop box 0.08,0.1,0.95,0.27, scanned page rendered at its native resolution (embedded image xref 4, 2550px across 8.50in), rendered at 216 dpi, capped to 1600px wide, grayscale, 1601x406 WebP quality 80"),
	("trough-ired-pcb", "trough-ired-pcb.md", "PDF page 106, printed page 2-11, A-18617 Trough 7 IRED PCB Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 106, crop box 0.27,0.275,0.72,0.335, scanned page rendered at its native resolution (embedded image xref 420, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1148x199 WebP quality 80"),
	("opto-switch-pcb", "opto-switch-pcb.md", "PDF page 107, printed page 2-12, A-14534 Opto Switch PCB Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 107, crop box 0.46,0.775,0.86,0.85, scanned page rendered at its native resolution (embedded image xref 424, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1020x248 WebP quality 80"),
	("dc-motor-control-pcb", "dc-motor-control-pcb.md", "PDF page 110, printed page 2-15, A-16120 D.C. Motor Control PCB Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 110, crop box 0.26,0.375,0.82,0.67, scanned page rendered at its native resolution (embedded image xref 436, 2550px across 8.50in), rendered at 242 dpi, capped to 1150px wide, grayscale, 1151x785 WebP quality 80"),
	("slingshot-assembly", "slingshot-assembly.md", "PDF page 113, printed page 2-18, A-17811 Kicker Arm (Slingshot) Assembly parts tables", "Manual_Bally_1994_The_Shadow.pdf page 113, crop box 0.12,0.64,0.93,0.83, scanned page rendered at its native resolution (embedded image xref 448, 2550px across 8.50in), rendered at 232 dpi, capped to 1600px wide, grayscale, 1601x486 WebP quality 80"),
	("outhole-ball-trough", "outhole-ball-trough.md", "PDF page 114, printed page 2-19, A-18753 Outhole Ball Trough Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 114, crop box 0.05,0.63,0.84,0.805, scanned page rendered at its native resolution (embedded image xref 452, 2550px across 8.50in), rendered at 238 dpi, capped to 1600px wide, grayscale, 1601x459 WebP quality 80"),
	("left-eject-assembly", "left-eject-assembly.md", "PDF page 116, printed page 2-21, A-18768 Eject Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 116, crop box 0.53,0.12,0.88,0.26, scanned page rendered at its native resolution (embedded image xref 460, 2550px across 8.50in), rendered at 300 dpi, grayscale, 893x462 WebP quality 80"),
	("ball-launch-kicker-bracket", "ball-launch-kicker-bracket.md", "PDF page 116, printed page 2-21, A-14525 Kicker Bracket Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 116, crop box 0.53,0.595,0.88,0.75, scanned page rendered at its native resolution (embedded image xref 460, 2550px across 8.50in), rendered at 300 dpi, grayscale, 893x512 WebP quality 80"),
	("ball-kicker-assembly", "ball-kicker-assembly.md", "PDF page 117, printed page 2-22, A-18952 Ball Kicker Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 117, crop box 0.35,0.595,0.8,0.85, scanned page rendered at its native resolution (embedded image xref 464, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1148x842 WebP quality 80"),
	("extended-target-assembly", "extended-target-assembly.md", "PDF page 118, printed page 2-23, A-18622 Extended Target Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 118, crop box 0.08,0.575,0.99,0.845, scanned page rendered at its native resolution (embedded image xref 468, 2550px across 8.50in), rendered at 168 dpi, capped to 1300px wide, grayscale, 1301x500 WebP quality 80"),
	("left-divertor-assembly", "left-divertor-assembly.md", "PDF page 119, printed page 2-24, A-18954 Divertor Mechanism Assembly (Left Side) parts tables", "Manual_Bally_1994_The_Shadow.pdf page 119, crop box 0.16,0.58,0.96,0.845, scanned page rendered at its native resolution (embedded image xref 472, 2550px across 8.50in), rendered at 235 dpi, capped to 1600px wide, grayscale, 1600x687 WebP quality 80"),
	("right-divertor-assembly", "right-divertor-assembly.md", "PDF page 120, printed page 2-25, A-18955 Divertor Mechanism Assembly (Right Side) parts tables", "Manual_Bally_1994_The_Shadow.pdf page 120, crop box 0.03,0.58,0.99,0.845, scanned page rendered at its native resolution (embedded image xref 476, 2550px across 8.50in), rendered at 196 dpi, capped to 1600px wide, grayscale, 1600x573 WebP quality 80"),
	("magnet-opto-assembly", "magnet-opto-assembly.md", "PDF page 121, printed page 2-26, A-18388 Magnet & Opto Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 121, crop box 0.6,0.11,1,0.285, scanned page rendered at its native resolution (embedded image xref 480, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1020x578 WebP quality 80"),
	("right-eject-assembly", "right-eject-assembly.md", "PDF page 121, printed page 2-26, A-15368 Eject Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 121, crop box 0.58,0.635,0.98,0.79, scanned page rendered at its native resolution (embedded image xref 480, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1020x512 WebP quality 80"),
	("ball-popper-assembly", "ball-popper-assembly.md", "PDF page 122, printed page 2-27, A-18950 Ball Popper Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 122, crop box 0.27,0.58,0.72,0.88, scanned page rendered at its native resolution (embedded image xref 484, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1148x990 WebP quality 80"),
	("mini-playfield-assembly", "mini-playfield-assembly.md", "PDF page 123, printed page 2-28, A-18382 Mini-Playfield Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 123, crop box 0.07,0.615,0.93,0.9, scanned page rendered at its native resolution (embedded image xref 488, 2550px across 8.50in), rendered at 164 dpi, capped to 1200px wide, grayscale, 1201x516 WebP quality 80"),
	("coil-slide-motor-assembly", "coil-slide-motor-assembly.md", "PDF page 124, printed page 2-29, A-17789 Coil Slide Motor Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 124, crop box 0.33,0.385,0.74,0.545, scanned page rendered at its native resolution (embedded image xref 492, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1046x529 WebP quality 80"),
	("four-bank-drop-target-assembly", "four-bank-drop-target-assembly.md", "PDF page 125, printed page 2-30, A-18783 4-Bank Drop Target Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 125, crop box 0.3,0.595,0.75,0.9, scanned page rendered at its native resolution (embedded image xref 496, 2550px across 8.50in), rendered at 275 dpi, capped to 1050px wide, grayscale, 1050x922 WebP quality 80"),
	("one-bank-drop-target-assembly", "one-bank-drop-target-assembly.md", "PDF page 127, printed page 2-32, A-14615-1 1-Bank Drop Target Assembly parts table", "Manual_Bally_1994_The_Shadow.pdf page 127, crop box 0.4,0.12,0.86,0.635, scanned page rendered at its native resolution (embedded image xref 504, 2550px across 8.50in), rendered at 166 dpi, capped to 650px wide, grayscale, 651x943 WebP quality 80"),
)


def _excerpts() -> list[dict[str, Any]]:
	records = []
	for suffix, transcription, locator, derivation in MANUAL_EXCERPTS:
		records.append(
			{
				"id": f"excerpt.the-shadow.{suffix}",
				"locator": locator,
				"path": f"{EXCERPT_PREFIX}/{transcription}",
				"sha256": _text_sha256(EXCERPT_DIRECTORY / transcription),
				"image": f"{EXCERPT_PREFIX}/{suffix}.webp",
				"image_sha256": _file_sha256(EXCERPT_DIRECTORY / f"{suffix}.webp"),
				"image_derivation": derivation,
				"method": "manual",
				"transcribed_by": "curator, read from the native-resolution render",
				"reviewed": True,
			}
		)
	return records


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames records for ts_lx5 and its nineteen clones",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/ts.c: CORE_GAMEDEF(ts,lx5) and CORE_CLONEDEF(ts,dx5/lh6/lh6p/dh6/la6/da6/lf6/df6/lm6/"
				"dm6/lx4/dx4/la4/da4/lf4/la2/da2/pa1/pa2) all with wpc_mSecurityS; tsGameData GEN_WPCSECURITY with wpc_dispDMD, "
				"FLIP_SW(FLIP_L|FLIP_UR)|FLIP_SOL(FLIP_L|FLIP_UR), one custom solenoid (custSol 1) answered by ts_getSol, the "
				"inverted-switch mask {0x00,0x00,0x00,0xe7,0x7f,0x00,0x00,0x00,0xf0,0x00,0x00,0x00} and no fast-flip address; "
				"ts_paddleMech {19, 20, MECH_LINEAR|MECH_STOPEND|MECH_TWODIRSOL, 21, 19, {{37,0,0},{38,18,18}}} added by "
				"init_ts; ts_handleMech (magnetCnt = 8 while core_getSol(35) is on, counting down otherwise, only when "
				"mechanics bit 1 is enabled); ts_getSol and ts_getMech; the SHADOW_SOUND DCS set and the prototype su2-sp2.rom "
				"U2 sound ROM of ts_pa1/ts_pa2; the *** PRELIMINARY *** simulator's #define block is cross-reference only. "
				"src/wpc/mech.c mech_updateAll/mech_update (a ROM-declared mech runs only when mechanics bit 0 is set; "
				"MECH_TWODIRSOL moves toward the last position while only sol1 is on and toward 0 while only sol2 is on). "
				"src/wpc/core.h CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, CORE_FIRSTCUSTSOL=51. src/wpc/core.c core_getSol "
				"(29-32 J111/GameOn remap, 33-36 solenoids2 with the upper-right flipper mask because FLIP_SOL(FLIP_UR) is set "
				"and raw bits at 35/36 because FLIP_SOL(FLIP_UL) is not, 37-44 zero outside WPC-95/System 11, 45-48 lower "
				"flippers, 51 through hw.getSol). src/wpc/wpc.c WPC_FLIPPERS complement read for non-WPC-95 generations and "
				"the always-closed switch 24 set at machine reset."
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
			"uri": "external:pinmame-manuals/by-machine/bally.the-shadow.1994/ipdb-2528/Manual_Bally_1994_The_Shadow.pdf",
			"original_filename": "Manual_Bally_1994_The_Shadow.pdf",
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T22:06:00Z",
			"locator": (
				"183-page image-only scan (1-bit CCITT at 300 dpi, 'Scanned by Woz', 2003) of the Bally The Shadow Operations "
				"Manual 16-50032-101, November 1994, IPDB machine 2528 (https://www.ipdb.org/machine.cgi?id=2528, Midway 'The "
				"Shadow'), resource https://www.ipdb.org/files/2528/Manual_Bally_1994_The_Shadow.pdf, which IPDB describes as "
				"'Operations Manual (November 1994, includes schematics, missing pages 2-47, 3-9)'; downloaded through an "
				"authenticated browser. A contributor-run Windows OCR text layer (ocr-windows/) is retained beside it for "
				"search only. PDF page 2 (DIP switch chart); rules PDF pages 12-29; Section 2 printed 2-38 to 2-43 (lamp, "
				"switch and solenoid/flasher tables, location lists and drawings) and the assembly pages; Section 3 printed "
				"3-3 (dedicated switches), 3-10 (general illumination circuit) and 3-28 (power driver board connector list)."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": _excerpts(),
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/vpw-mod-1.0/source/The%20Shadow%20(Bally%201994)%20VPW%20Mod%20v1.0.vpx",
			"original_filename": "The Shadow (Bally 1994) VPW Mod v1.0.vpx",
			"sha256": TABLE_SHA256,
			"acquired_at": "2026-09-25T22:36:00Z",
			"locator": (
				"The Shadow VPW Mod (Bally 1994) version 1.0.0 by VPinWorkshop (https://vpuniverse.com/files/file/"
				"31690-the-shadow-vpw-mod-bally-1994/, submitted September 6), downloaded through an authenticated VPU session "
				f"as 'The Shadow (Bally 1994) VPW Mod v1.0.vpx.zip' (SHA-256 {DOWNLOAD_ARCHIVE_SHA256}). The VPW build is a "
				"refactor of Sixtoe's VR mod of Skitso's detail mod of Alessio's original table, with a new physical build and "
				f"a rebuilt Battlefield. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/975 and "
				"y/1974. Geometry authority for named table objects only; it shares ancestry with the Skitso table, so their "
				"agreement is not independent confirmation."
			),
			"license": "NOASSERTION",
			"attribution": "VPinWorkshop (Sixtoe, Burger, tomate, apophis, Dough Nut, DGrimmReaper); Alessio, Skitso, Markrock76 and Bord",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script of the VPW table (152,956 bytes): cGameName = "ts_lx5", UseSolenoids = 2, UseLamps = 1, '
				"UseVPMModSol = 2, HandleMechanics = 1, MotorCallback HandleMiniPF reading Controller.GetMech(0); SolCallback for "
				"1-14, 16, 24, 25, 35, 36, sLRFlipper, sLLFlipper and sURFlipper; SolModCallback for flashers 17, 18, 21-23 and "
				"26-28 (Flupper domes 1-6 for 21-23 and 26-28); bsTrough InitSw 0,41,42,43,44,45; bsLock InitSw 0,63,64,65; "
				"vpmMapLights AllLamps; UpdateGI dispatching 0 bottom, 1 left, 2/3 inserts (commented 'Not on playfield', empty "
				"collections) and 4 right."
			),
			"license": "NOASSERTION",
			"attribution": "VPinWorkshop; Alessio, Skitso, Markrock76 and Bord",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the VPW table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": LEGACY_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/source/The%20Shadow%20(Bally%201994).vpx",
			"original_filename": "The Shadow (Bally 1994).vpx",
			"sha256": LEGACY_TABLE_SHA256,
			"locator": (
				"The contributor's older table (2020) by Alessio with visual, sound and physics enhancements by Skitso, "
				"Markrock76 and Bord, Thalamus 2019 sound patch ('Table not verified yet'), VPX 10.6, the same bounds "
				f"{TABLE_BOUNDS}. An ancestor of the VPW build: most switch and lamp objects sit at identical coordinates. "
				"Corroboration only."
			),
			"license": "NOASSERTION",
			"attribution": "Alessio, Skitso, Markrock76, Bord and Thalamus",
			"rights": "NOASSERTION",
		},
		{
			"id": LEGACY_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": LEGACY_SCRIPT_SHA256,
			"locator": (
				'Embedded script of the older table (67,345 bytes): cGameName = "ts_lx5", the same SolCallback table for 1-14, '
				"16, 24, 25, 35 and 36, SetLamp fading for flashers 17, 18, 21-23 and 26-28, the same switch handlers, and an "
				"UpdateLamps routine that binds the ramp-ring lamps 81-84 to the F181-F184 flasher objects (Flash 81-84)."
			),
			"license": "NOASSERTION",
			"attribution": "Alessio, Skitso, Markrock76, Bord and Thalamus",
			"rights": "NOASSERTION",
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
	if address in OPTO_SWITCHES:
		notes += (
			' Printed shaded "Opto, Typically Closed" on the switch matrix. Pinned PinMAME\'s tsGameData inverted-switch '
			"mask normalizes this address, so the public state is already normalized (1 = beam interrupted / ball present) "
			"and must not be inverted again."
		)
	if address in {41, 42, 43, 44, 45, 46}:
		notes += " Trough LED/phototransistor pair (A-18617 Trough 7 IRED PCB with A-18618) in the A-18753 Outhole Ball Trough Assembly."
	if address in {31, 32, 47}:
		notes += " LED/phototransistor pair (A-16908/A-16909) across the ball path."
	if address == 33:
		notes += (
			" The A-16908/A-16909 opto pair of the A-18388 Magnet & Opto Assembly under the Inner Sanctum (center wall): it "
			"reports a ball over the magnet (solenoid 35)."
		)
	if address == 36:
		notes += " The A-16908/A-16909 opto pair on the Battlefield kicker head that tells the ROM a ball is in front of it."
	if address in {37, 38}:
		notes += (
			" A-14534 Opto Switch PCB (an opto interrupter) located under the mini-playfield assembly; it marks the "
			f"{'left' if address == 37 else 'right'} end of the Battlefield kicker head's travel. PinMAME's ts_paddleMech "
			f"closes it at position {0 if address == 37 else 18} of the 19-step head model when mechanics bit 0 is enabled."
		)
	if address in {85, 86, 87, 88}:
		notes += " One of the four target positions read by the A-19666 4-Drop Target Opto PCB of the A-18783 4-Bank Drop Target Assembly on the Battlefield."
	if address in {71, 72, 73, 74, 81, 82, 84}:
		notes += " Battlefield side standup (A-18378-6 switch) on the mini-playfield."
	if address == 82:
		notes += " " + MINI_RIGHT_STANDUP_INSET_NOTE
	if address in {12, 34}:
		notes += (
			" Blue Phurba cabinet button above the "
			f"{'right' if address == 12 else 'left'} flipper button (SW-1A-195); the rules say it toggles the "
			f"{'right' if address == 12 else 'left'} ramp divertor. The retained script sets it from the "
			f"{'right' if address == 12 else 'left'} MagnaSave key."
		)
	if address == 11:
		notes += " Trigger of the A-18536 Gun Assembly on the cabinet (5647-12133-16); the ROM fires the auto launch (solenoid 1) from it. The retained script sets it from the plunger key."
	if address in {25, 26, 27, 28, 52, 53}:
		notes += " One of the six M-O-N-G-O-L standup targets."
	if address in {61, 62}:
		notes += " The slingshot kicker switch (SW-1A-114) and the separate score switch (SW-1A-120) share this address."
	if address == 35:
		notes += " Rubber-mounted scoring switch (SW-1A-120); the retained script pulses it from the sw35 wall's Hit event."
	if address == 51:
		notes += " Switch (5647-12693-31, item 24) of the A-18622 Extended Target Assembly: closed while the wall target is down."
	if address == 55:
		notes += " Switch (5647-12693-31, item 17) of the A-14615-1 1-Bank Drop Target Assembly: closed while the Battle drop target is down."
	if address == 68:
		notes += " Mini micro switch (item 4) of the A-18950 Ball Popper Assembly that lifts the ball to the Battlefield."
	if address in {63, 64, 65}:
		notes += " Lockup switch at the rear right; the three positions hold up to three locked balls."
	if address == 24:
		notes += (
			" Physical part 5643-09112-00 is a permanently closed link that proves the matrix is connected; pinned PinMAME "
			"sets it closed at machine reset. Both retained scripts also pulse 24 from each Battlefield drop target's Hit "
			"event (sw85-sw88), a table quirk rather than a fact about the machine."
		)
	if address == 22:
		notes += " Closed while the coin door is closed."
	if address == 17:
		notes += " The switch-locations list prints this item 'Left Lane'; the matrix prints LEFT RETURN LANE."
	if address in SWITCH_PROJECTIONS:
		notes += " " + SWITCH_PROJECTIONS[address]
	elif address in SWITCH_OBJECTS:
		notes += f" Placement: retained VPW table object {SWITCH_OBJECTS[address]}."
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
		11: "cabinet.launch", 12: "cabinet.action", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt",
		22: "cabinet.coin-door", 23: "cabinet.buy-in", 34: "cabinet.action",
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
				physical["notes"] = (
					f"Printed switch-matrix drive column {column}, return row {row}. The printed matrix and the switch-locations "
					"list both mark this position Not Used, so there is no Mini Right Standup 2 switch although lamp 73 "
					"(Mini Right Standup 2) is printed. "
					+ MINI_RIGHT_STANDUP_INSET_NOTE
				)
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			label = SWITCH_LABELS[address]
			physical["notes"] = _switch_notes(address, column, row)
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address == 24:
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE, CORE_SOURCE)
				items.append(_device(identifier, label, "constant", "pinmame.input.switch", address, "used", (MANUAL_SOURCE, CORE_SOURCE), **extra))
				continue
			extra["normally_closed"] = address in OPTO_SWITCHES
			if address in PULSED_SWITCHES:
				extra["pulse"] = True
			if address in cabinet_roles:
				extra["roles"] = [cabinet_roles[address]]
				physical["location"] = "cabinet" if address in {11, 12, 13, 23, 34} else "cabinet interior"
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if address == 22:
					extra["initial_active"] = True
			else:
				physical["location"] = "mini-playfield" if address in {36, 37, 38, 58, 71, 72, 73, 74, 81, 82, 84, 85, 86, 87, 88} else "playfield"
				coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, "sensor", [SWITCH_POSITIONS[address]], *coordinate_refs)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, **extra))

	for address, (label, role, switch_type, part, wire, connection) in FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		notes = f"Printed Fliptronic grounded switch {position} ({wire}, {connection}); switch-locations part {part}."
		if switch_type == "opto":
			notes += (
				" Printed shaded as an opto (A-17316 Flipper Opto PCB Assembly, cabinet mounted). On this generation "
				"PinMAME's WPC_FLIPPERS register read returns the complement of the whole Fliptronic column, so the "
				"public state is already normalized (1 = button pressed) and must not be inverted again."
			)
			if address == 116:
				notes += " The upper right flipper has its own cabinet opto position on the right flipper button."
		else:
			notes += " Plain end-of-stroke leaf switch (SW-1A-194) on the flipper assembly."
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
	for address, (wire, connection, printed) in UNUSED_FLIPPER_SWITCHES.items():
		position = f"F{address - 110}"
		items.append(
			_device(
				f"switch.generic-{address}", f"Not Used Upper Left Flipper Position {position}", "switch",
				"pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": position},
				],
				physical={"location": "not installed", "notes": f"The switch matrix prints Fliptronic position {position} '{printed}' ({wire}, {connection}); the switch-locations list prints {position} Not Used with no part. The Shadow has no upper left flipper, and tsGameData declares no FLIP_SW(FLIP_UL)."},
				spatial=not_applicable("unused", MANUAL_SOURCE),
			)
		)

	for address in range(1, 9):
		settings = ", ".join(f"{country} {values[address - 1]}" for country, values in DIP_COUNTRY_CHART.items())
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP SW{address} (country setting)", "dip_switch",
				"pinmame.input.dip", address, "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC-Security CPU board",
					"switch_type": "dip",
					"notes": f"CPU-board DIP position SW{address}. The printed Dip Switch Chart (PDF page 2) sets it per country: {settings}.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace(chr(39), '').replace(chr(34), '')}"


def _solenoid_notes(address: int, printed_type: str) -> str:
	printed_number = PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")
	notes = f"Printed solenoid/flasher table entry {printed_number} ({printed_type})."
	if address in SOLENOID_CALLBACKS:
		notes += f" Retained VPW script callback: {SOLENOID_CALLBACKS[address]}."
	if address in {9, 10}:
		notes += " The retained VPW script's slingshot callback animates the arm; the table's slingshot walls pulse the switch."
	if address == 1:
		notes += (
			" A-14525 Kicker Bracket Assembly at the foot of the shooter lane. There is no plunger: the ROM fires it when "
			"the player pulls the gun trigger (switch 11) with a ball on the shooter switch (48)."
		)
	if address == 2:
		notes += (
			" A-14189 coil of the A-18952 Ball Kicker Assembly, a flipper-style crank link that kicks the locked balls "
			"out of the lockup at the rear right."
		)
	if address in {3, 4, 5, 6}:
		side = "left" if address in {3, 4} else "right"
		notes += (
			f" One of the two AE-25-1000 coils of the A-{18954 if side == 'left' else 18955} Divertor Mechanism Assembly "
			f"({'Left' if side == 'left' else 'Right'} Side): the {side} ramp's Phurba dagger diverter has one coil for each "
			"direction, and the rules let the player toggle it with the blue Phurba button on that side."
		)
	if address == 7:
		notes += " Backbox-mounted knocker (printed backbox voltage and drive connections)."
	if address in {8, 16}:
		notes += (
			" One of the two coils of the A-18622 Extended Target Assembly (the Inner Sanctum wall target): "
			f"{'the AL-23-800 coil raises it' if address == 8 else 'the SM-30-1100-DC coil pulls it down'}; switch 51 "
			"reports it down. The solenoid/flasher locations list prints item 08's coil as AL-23-800, the solenoid table "
			"prints AE-23-800; the assembly parts list agrees with AL-23-800."
		)
	if address in {25, 36}:
		notes += (
			" One of the two coils of the A-14615-1 1-Bank Drop Target Assembly (the Battle drop target; printed assembly "
			f"A-19642 in the locations list): {'the AE-26-1200 reset coil raises it' if address == 25 else 'the SM1-26-600 coil of its A-14908 Target Knock Down Assembly drops it'}; "
			"switch 55 reports it down."
		)
	if address == 36:
		notes += (
			" It runs on the Fliptronic upper-left hold circuit (J902-1, Org-Gry): the main table prints drive transistor Q7 "
			"while the flipper block prints Q5 for the same connector, and gives Q7 to the upper right hold; Q5 is recorded, "
			"following the flipper block, which gives each circuit its own transistor."
		)
	if address == 35:
		notes += (
			" 20-9247 Coil Magnet & Thermal Breaker of the A-18388 Magnet & Opto Assembly under the Inner Sanctum; opto "
			"switch 33 reports a ball over it. It runs on the Fliptronic upper-left power circuit (J902-3, Yel-Gry): the main "
			"table prints drive transistor Q2 while the flipper block prints Q1 for the same connector and gives Q2 to the "
			"upper right power; Q1 is recorded, following the flipper block, which gives each circuit its own transistor. "
			"FLIP_SOL(FLIP_UL) is not set, so PinMAME publishes the raw bit here."
		)
	if address == 13:
		notes += " A-18753 Outhole Ball Trough Assembly eject coil."
	if address in {11, 12}:
		notes += f" Eject saucer coil ({'A-15368' if address == 11 else 'A-18768'} Eject Assembly)."
	if address == 14:
		notes += " A-18950 Ball Popper Assembly: the Battle popper at the top left that lifts the ball onto the Battlefield mini-playfield."
	if address == 15:
		notes += (
			" The coil of the A-19070 Coil/Slide Assembly, the Battlefield kicker head. The retained scripts bind no "
			"callback: the tables fake the kick with nineteen slingshot walls along the head's rail."
		)
	if address in {19, 20}:
		notes += (
			" Printed in the Flasher category, but its part is 14-8014 (A-19170 Motor/Opto Assembly of the A-17789 Coil "
			"Slide Motor Assembly), fed from J116-2 through the A-16120 D.C. Motor Control PCB. It drives the Battlefield "
			f"kicker head {'right' if address == 19 else 'left'}: pinned PinMAME's ts_paddleMech moves the head toward "
			f"position {'18 (Mini Limit Right, 38)' if address == 19 else '0 (Mini Limit Left, 37)'} while only this output is on."
		)
	if address == 24:
		notes += " AE-25-1000 reset coil of the A-18783 4-Bank Drop Target Assembly on the Battlefield. The printed drive connection carries an asterisk: 'Tieback Diode J122-5 (loop) from J126-11 (end)'."
	if address == 25:
		notes += " The printed drive connection *J122-1 carries the same tieback-diode asterisk."
	if address in FLASHER_QUANTITIES:
		notes += f" The playfield carries {FLASHER_QUANTITIES[address]} printed flasher socket(s) for this output."
	if address == 17:
		notes += " A-17803 flasher on the Battlefield; the output also lights two #906 backbox bulbs (backbox connections), which are not placed."
	if address == 18:
		notes += " A-17983 flasher on the left side; the output also lights one #906 backbox bulb, which is not placed."
	if address in {17, 18}:
		notes += (
			f" The playfield socket is not placed: the VPW table models no bulb or dome object for it, and its script "
			f"drives only an off-playfield helper light. The older Skitso script binds this output (Flash {100 + address}) "
			f"to the Flasher image F{100 + address} and its reflection sprites, which are glow images, not sockets. The socket's position has to be measured on the printed 2-43 solenoid/flasher location drawing."
		)
	if address in {21, 22, 23}:
		notes += (
			" The locations list prints two sockets, a 24-8704 #89 bulb in an A-17983 assembly and a 24-8802 #906 bulb in a "
			f"{'A-12156' if address == 23 else 'B-12156'} assembly. The VPW table models one Flupper dome for this output, "
			"so one socket is placed and the other is not."
		)
	if address in {26, 27, 28}:
		notes += " B-12156 flasher on the back panel (printed '22-8802', which the page legend decodes as 24-8802 #906); the output also lights one #906 backbox bulb, which is not placed."
	if address in {33, 34}:
		notes += (
			" Upper right flipper (A-15849-R-4, FL-15411 orange coil) on the right side of the playfield. tsGameData sets "
			"FLIP_SOL(FLIP_UR), so core_getSol reports public 33 as the power winding alone and 34 as power OR hold. The "
			"VPW script binds SolCallback(sURFlipper) (34); the older Skitso script swung this flipper from the lower right "
			"flipper callback instead."
		)
	if address in {45, 46, 47, 48}:
		notes += (
			f" Printed flipper circuit {printed_number}; PinMAME publishes the lower flippers at 45-48, odd addresses "
			"the power winding alone and even addresses power OR hold."
		)
	if address in SOLENOID_OBJECTS:
		notes += f" Placement: retained VPW table object {SOLENOID_OBJECTS[address]}."
	if address in SOLENOID_PROJECTIONS:
		notes += " " + SOLENOID_PROJECTIONS[address]
	return notes


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 52):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_WIRING[address]
			kind = "flasher" if address in FLASHERS else "motor" if address in MOTORS else "magnet" if address in MAGNETS else "coil"
			physical: dict[str, Any] = {}
			if part and not part.startswith("#") and kind != "flasher":
				physical["part_number"] = part
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if kind == "flasher":
				physical["quantity"] = FLASHER_QUANTITIES[address]
			physical["notes"] = _solenoid_notes(address, printed_type) + (f" Printed flashlamp type {part}." if kind == "flasher" else "")
			wiring: dict[str, Any] = {
				"board": "Fliptronic II board" if address in {33, 34, 35, 36, 45, 46, 47, 48} else "WPC-Security power driver board",
				"driver_transistor": transistor,
				"power_connection": voltage,
				"control_connection": drive,
				"control_wire": wire,
			}
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": PRINTED_FLIPPER_CIRCUITS.get(address, f"{address:02d}")}]
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in SOLENOID_POSITIONS:
				role = "emitter" if kind == "flasher" else "effect"
				refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *refs)
			if address in {33, 34, 45, 46, 47, 48}:
				extra["roles"] = [f"flipper.{'upper.right' if address in {33, 34} else 'lower.right' if address in {45, 46} else 'lower.left'}"]
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {21, 22, 23, 26, 27, 28, 34}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in {17, 18}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, LEGACY_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31, 51}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; not a Shadow playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; not a Shadow playfield device.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the Game-On / flipper-enable state because ts.c configures no fast-flip address.",
			32: "PinMAME reports this WPC state channel as always zero; tsGameData declares no use for it.",
			49: "PinMAME's simulator-only ball-shooter channel; The Shadow's auto launch is solenoid 1 and has no output here.",
			50: "Reserved PinMAME output position before the first custom-output boundary.",
			51: (
				"tsGameData declares hw.custSol = 1, so PinMAME publishes this address (CORE_CUSTSOLNO(1)) through ts_getSol: "
				"it reads 1 while the driver's magnetCnt is positive. ts_handleMech sets magnetCnt to 8 while the magnet "
				"(public 35) is on and counts it down otherwise, but only when mechanics bit 1 is enabled, so the address stays "
				"0 with LibPinMAME's default of 0 and with the retained tables' HandleMechanics = 1. It is a derived "
				"simulator state for the *** PRELIMINARY *** driver, not a physical control line; solenoid 35 is the magnet."
			),
		}.get(address, "Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and System 11.")
		roles = ["internal.duplicate.decaying-fire-state"] if address == 51 else ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
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
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			refs: tuple[str, ...] = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			physical: dict[str, Any] = {"quantity": 1}
			extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring, "physical": physical}
			if address in {87, 88}:
				notes += (
					f" Lamp inside the cabinet {'Buy-In' if address == 87 else 'Start'} button; the lamp-locations list prints "
					f"the button part {'20-9663-18' if address == 87 else '20-9663-2'} in the bulb column and no lamp assembly. "
					f"The lamp matrix prints {'BUY-IN BUTTON' if address == 87 else 'CREDIT BUTTON'}."
				)
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE)
			else:
				physical["assembly_part_number"] = LAMP_ASSEMBLIES[address]
				bulb = LAMP_BULBS.get(address, "24-8768")
				decoded = {"24-6549": "#44", "24-8768": "#555"}.get(bulb)
				notes += f" Printed bulb {bulb}" + (f" ({decoded})." if decoded else ", which neither legend decodes.")
				if address in {62, 63}:
					notes += (
						f" The lamp matrix misprints this cell 'MINI LEFT STANDUP {'23' if address == 62 else '12'}'"
						f"{' with the number box 2' if address == 62 else ''}; the lamp-locations list names it Mini Left "
						f"Standup {'3' if address == 62 else '2'}, continuing the 61-64 = 4-1 order."
					)
				if address == 36:
					notes += " Printed 'DUAL OF WILLS' on the matrix and the locations list; the rules name the scene Duel of Wills."
				if address in {61, 62, 63, 64, 65, 71, 72, 73, 74, 75}:
					notes += " Battlefield mini-playfield lamp."
				if address == 73:
					notes += " The matching Mini Right Standup 2 switch position (83) is printed Not Used."
				if address in RING_LAMPS:
					notes += (
						" A ring on the ramp (A-19545 assembly). It is not placed: the VPW table maps this address to an "
						f"off-playfield helper light (l{address}, x < 0) and models no bulb for it, and the older Skitso script's "
						f"Flash {address} binding drives F{100 + address}, an additive wallreflect_white glow sprite, not a socket. "
						"The socket has to be measured on the printed 2-39 lamp location drawing (callout 81 on its main playfield "
						"drawing, 82-84 in its ramp inset)."
					)
					refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, LEGACY_SCRIPT_SOURCE, CORE_SOURCE)
				else:
					notes += f" Placement: retained VPW table Light l{address} (vpmMapLights AllLamps, TimerInterval {address})."
					extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE)
			physical["notes"] = notes
			items.append(_device(identifier, LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, return_pin, transistor, supply_pin, return_wire, supply_wire, bulbs) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination string {address + 1:02d} '{label}' (G.I. String {address + 1}); printed lamps {bulbs}. "
			f"The table prints the return pin {return_pin.split()[0]} under its Voltage column and the 6.8VAC supply pin "
			f"{supply_pin.split()[0]} under Drive. The 3-28 connector list names the first pin 'Return G.I.' and the second "
			f"'6.8VAC', and the printed 3-10 G.I. circuit draws the triac ({transistor}) on the return side, so the return is "
			"the switched connection."
		)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}],
			"wiring": {
				"board": "WPC-Security power driver board",
				"control_connection": return_pin,
				"control_wire": return_wire,
				"driver_transistor": transistor,
				"power_connection": supply_pin,
				"power_wire": supply_wire,
			},
		}
		physical: dict[str, Any] = {}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				f" The manual prints no per-string bulb list or count, so the quantity counts the placed playfield emitters "
				f"only, and every coordinate comes from the VPW table's {GI_COLLECTIONS[address]} collection, which its "
				f"UpdateGI dispatches for this string; one light per distinct position is placed (excluded: {GI_EXCLUDED[address]}). "
				"These placements are observed, not validated: no factory source lists the sockets."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		else:
			notes += (
				" A backbox string (printed backbox connections only, the backbox insert panel). The VPW script's UpdateGI "
				"keeps an empty collection for it with the comment 'Not on playfield'."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		physical["notes"] = notes + " " + GI_CONNECTOR_LIST_NOTE
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

	return [
		mechanism(
			"mechanism.trough", "Five-ball trough", "kicker", [output_id("Ball Release")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-44", "switch.matrix-45", "switch.matrix-46"],
			"Five balls rest on the trough optos 41 (Trough 1) to 45 (Trough 5) of the A-18753 Outhole Ball Trough "
			"Assembly, with Top Trough (46) above them; all six are A-18617/A-18618 LED/phototransistor pairs normalized by "
			"PinMAME. Solenoid 13 (Ball Release) ejects a ball into the shooter lane. The retained scripts' cvpmBallStack "
			"holds the balls on 41-45 and has no ball on 46.",
			[
				("ball-1", "Trough 1", ["switch.matrix-41"], "First trough position."),
				("ball-2", "Trough 2", ["switch.matrix-42"], "Second trough position."),
				("ball-3", "Trough 3", ["switch.matrix-43"], "Third trough position."),
				("ball-4", "Trough 4", ["switch.matrix-44"], "Fourth trough position."),
				("ball-5", "Trough 5", ["switch.matrix-45"], "Fifth trough position."),
				("top", "Top Trough", ["switch.matrix-46"], "Opto above the stack."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-18753",
		),
		mechanism(
			"mechanism.gun-launch", "Gun-trigger auto launch", "kicker", [output_id("Ball Launch")],
			["switch.matrix-48", "switch.matrix-11"],
			"There is no plunger. A ball served from the trough rests on the Shooter switch (48); the player pulls the "
			"trigger of the cabinet A-18536 Gun Assembly (switch 11) and the ROM fires solenoid 1, the A-14525 kicker bracket "
			"at the foot of the lane. The retained scripts set 11 from the plunger key and fire a cvpmImpulseP plunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-48"], "Shooter switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-14525",
		),
		mechanism(
			"mechanism.lockup", "Three-ball lockup", "kicker", [output_id("Lockup Kickout")],
			["switch.matrix-63", "switch.matrix-64", "switch.matrix-65"],
			"A lock at the rear right holds up to three balls on Lockup Right (63), Middle (64) and Left (65); solenoid 2, "
			"the A-14189 crank-link coil of the A-18952 Ball Kicker Assembly, kicks them out. The rules light the locks from "
			"the center wall target and start Shadow Multi-ball on the third lock.",
			[
				("right", "Lockup Right", ["switch.matrix-63"], "First lock position."),
				("middle", "Lockup Middle", ["switch.matrix-64"], "Second lock position."),
				("left", "Lockup Left", ["switch.matrix-65"], "Third lock position."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18952",
		),
		mechanism(
			"mechanism.left-diverter", "Left ramp Phurba diverter", "diverter",
			[output_id("Left Diverter Left"), output_id("Left Diverter Right")], ["switch.matrix-75", "switch.matrix-76", "switch.matrix-34"],
			"The A-18954 Divertor Mechanism Assembly (Left Side) swings a dagger-shaped blade at the left ramp's fork with "
			"two AE-25-1000 coils, one per direction (3 Left, 4 Right). The ball then leaves the ramp on the left or right "
			"branch, reported by Left Ramp Left Made (75) or Left Ramp Right Made (76). The player toggles it with the left "
			"blue Phurba cabinet button (34); the rules use it to light ring lamps and return the ball to the wanted flipper.",
			[
				("left", "Diverted left", ["switch.matrix-75"], "Left branch made."),
				("right", "Diverted right", ["switch.matrix-76"], "Right branch made."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18954",
		),
		mechanism(
			"mechanism.right-diverter", "Right ramp Phurba diverter", "diverter",
			[output_id("Right Diverter Right"), output_id("Right Diverter Left")], ["switch.matrix-77", "switch.matrix-78", "switch.matrix-12"],
			"The A-18955 Divertor Mechanism Assembly (Right Side) does the same on the right ramp (5 Right, 6 Left), "
			"reported by Right Ramp Left Made (77) or Right Ramp Right Made (78) and toggled by the right blue Phurba cabinet "
			"button (12).",
			[
				("left", "Diverted left", ["switch.matrix-77"], "Left branch made."),
				("right", "Diverted right", ["switch.matrix-78"], "Right branch made."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18955",
		),
		mechanism(
			"mechanism.inner-sanctum", "Inner Sanctum wall target and magnet", "other",
			[output_id("Wall Target Up"), output_id("Wall Target Down"), output_id("Magnet")],
			["switch.matrix-51", "switch.matrix-33"],
			"The center wall target is the A-18622 Extended Target Assembly: an AL-23-800 coil (solenoid 8) raises it and an "
			"SM-30-1100-DC coil (solenoid 16) pulls it down, and its switch (51) closes while it is down. Behind it the "
			"A-18388 Magnet & Opto Assembly puts a 20-9247 magnet (solenoid 35) under the Inner Sanctum with an opto pair "
			"(33) that sees a ball over it. The retained scripts catch and hold a ball on the magnet while 35 is on and "
			"release it when the magnet drops.",
			[
				("down", "Wall target down", ["switch.matrix-51"], "Wall Target Down switch."),
				("ball", "Ball over the magnet", ["switch.matrix-33"], "Inner Sanctum opto."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="A-18622",
		),
		mechanism(
			"mechanism.battle-drop", "Battle drop target", "drop_target_bank",
			[output_id("Single Drop Up"), output_id("Single Drop Down")], ["switch.matrix-55"],
			"The A-14615-1 1-Bank Drop Target Assembly: an AE-26-1200 reset coil (solenoid 25) raises the target and the "
			"SM1-26-600 coil of its A-14908 Target Knock Down Assembly (solenoid 36) drops it; its switch (55) closes while "
			"it is down. The rules say hitting it opens the way to the Battle popper.",
			[("down", "Battle drop down", ["switch.matrix-55"], "Battle Drop Down switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-14615-1",
		),
		mechanism(
			"mechanism.battle-popper", "Battle popper", "kicker", [output_id("Ball Popper")], ["switch.matrix-68"],
			"A ball dropping into the Battle popper (switch 68, A-18950 Ball Popper Assembly) is raised by solenoid 14 onto "
			"the Battlefield mini-playfield.",
			[("ball", "Ball in the popper", ["switch.matrix-68"], "Popper switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18950",
		),
		mechanism(
			"mechanism.battlefield", "Battlefield mini-playfield", "motorized",
			[output_id("Mini Motor Right"), output_id("Mini Motor Left"), output_id("Mini Kicker"), output_id("Mini Drop Bank")],
			[
				"switch.matrix-36", "switch.matrix-37", "switch.matrix-38", "switch.matrix-58", "switch.matrix-71", "switch.matrix-72",
				"switch.matrix-73", "switch.matrix-74", "switch.matrix-81", "switch.matrix-82", "switch.matrix-84",
				"switch.matrix-85", "switch.matrix-86", "switch.matrix-87", "switch.matrix-88",
			],
			"The A-18382 Mini-Playfield Assembly at the back left of the playfield. A kicker head (A-19070 Coil/Slide "
			"Assembly, coil solenoid 15, opto 36 seeing the ball in front of it) rides on a slide driven by the 14-8014 "
			"motor of the A-17789 Coil Slide Motor Assembly; solenoid 19 drives it right and 20 left, through the A-16120 "
			"D.C. Motor Control PCB, and the A-14534 opto boards under the assembly mark the left (37) and right (38) ends. "
			"The rules have the player steer the head with the flipper buttons while it fires automatically at the side "
			"standups (71-74 on the left, 81, 82 and 84 on the right) and then at the A-18783 4-Bank Drop Target Assembly "
			"at the back (optos 85-88, reset by solenoid 24) for the Battlefield Jackpot; the ball leaves through the Mini "
			"Exit Tube (58). Pinned PinMAME models the head as a 19-step linear mech (ts_paddleMech, stop at both ends, "
			"solenoid 19 alone toward position 18 closing 38, solenoid 20 alone toward position 0 closing 37) that runs only "
			"when mechanics bit 0 is enabled. The retained scripts read Controller.GetMech(0) to show the head at one of "
			"nineteen positions and pulse 36 from walls at those positions instead of firing solenoid 15.",
			[
				("left-limit", "Head at the left end", ["switch.matrix-37"], "Mini Limit Left opto."),
				("right-limit", "Head at the right end", ["switch.matrix-38"], "Mini Limit Right opto."),
				("ball-at-head", "Ball in front of the kicker head", ["switch.matrix-36"], "Mini Kicker opto."),
				("drops", "Back drop targets down", ["switch.matrix-85", "switch.matrix-86", "switch.matrix-87", "switch.matrix-88"], "4-bank drop optos."),
				("exit", "Ball leaving the Battlefield", ["switch.matrix-58"], "Mini Exit Tube."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18382",
		),
		mechanism(
			"mechanism.left-eject", "Left eject", "kicker", [output_id("Left Eject")], ["switch.matrix-66"],
			"A saucer on the left (switch 66) kicked by solenoid 12 (A-18768 Eject Assembly).",
			[("ball", "Ball in the left eject", ["switch.matrix-66"], "Left Eject switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-18768",
		),
		mechanism(
			"mechanism.right-eject", "Right eject", "kicker", [output_id("Right Eject")], ["switch.matrix-67"],
			"A saucer at the upper right (switch 67) kicked by solenoid 11 (A-15368 Eject Assembly).",
			[("ball", "Ball in the right eject", ["switch.matrix-67"], "Right Eject switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-15368",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshots", "other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")], ["switch.matrix-61", "switch.matrix-62"],
			"A-17811 slingshot kicker assemblies; each carries a kicker switch (SW-1A-114) and a score switch (SW-1A-120) on one address.",
			[("left", "Left slingshot", ["switch.matrix-61"], "Left slingshot."), ("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="A-17811",
		),
		mechanism(
			"mechanism.flippers", "Three flippers", "other",
			[
				output_id("Lower Right Flipper Power"), output_id("Lower Right Flipper Hold"),
				output_id("Lower Left Flipper Power"), output_id("Lower Left Flipper Hold"),
				output_id("Upper Right Flipper Power"), output_id("Upper Right Flipper Hold"),
			],
			["switch.generic-111", "switch.generic-112", "switch.generic-113", "switch.generic-114", "switch.generic-115", "switch.generic-116"],
			"Lower right (A-15849-R-2) and lower left (A-15849-L-2) flippers with FL-11629 blue coils, and an upper right "
			"flipper (A-15849-R-4) with an FL-15411 orange coil on the right side of the playfield. Each is a Fliptronic "
			"flipper with separate power and hold windings, a cabinet opto (112, 114, 116) and an end-of-stroke leaf switch "
			"(111, 113, 115). The ROM energizes the power and hold windings on the button and switches the power transistor "
			"off when it reads the end-of-stroke switch close; the hold winding keeps the flipper up while the button stays pressed.",
			[
				("lower-right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112, EOS 111."),
				("lower-left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114, EOS 113."),
				("upper-right", "Upper right flipper", ["switch.generic-115", "switch.generic-116"], "Button opto 116, EOS 115."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [output_id("Knocker")], [],
			"Solenoid 7 fires the B-10686-1 knocker in the backbox.",
			[],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, assembly_part_number="B-10686-1",
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


COVERAGE_MISSING = ("spatial_placement",)


def build() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": "bally.the-shadow.1994",
			"name": "The Shadow",
			"manufacturer": "Bally",
			"year": 1994,
			"kind": "physical_pinball",
			"ipdb_id": 2528,
			"opdb_id": "G4jPX-M85YZ",
		},
		"coverage": {
			"status": "partial",
			"missing": list(COVERAGE_MISSING),
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
		"knowledge": {"path": "knowledge/bally/the-shadow-1994.md", "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"The Shadow device identifiers are not unique: {duplicates}")
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
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unplaced_outputs: list[dict[str, Any]] = []
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
			"Every coordinate comes from one table lineage (the VPW Mod 1.0 build and its Skitso ancestor, which agree "
			"almost everywhere because they share geometry) and has not yet been checked against the manual's location "
			"drawings. The lamp (printed 2-39), switch (2-41) and solenoid/flasher (2-43) drawings carry legible callout "
			"numbers, so a least-squares fit of each drawing and a per-callout distance check can validate the placements.",
			"Flashers 21, 22 and 23 each print two playfield sockets; the VPW table models one Flupper dome per output, so "
			"the second socket of each is not placed.",
			"Flashers 17 (Mini Playfield) and 18 (Left Side) are not placed: the VPW table models no bulb or dome for them "
			"and drives only off-playfield helper lights, and the older table's F117/F118 are glow images, not sockets. "
			"Their sockets have to be measured on the printed 2-43 location drawing.",
			"The ramp-ring lamps 81-84 are not placed for the same reason: the VPW table drives only off-playfield helper "
			"lights, and the older table's F181-F184 are glow sprites. Their sockets have to be measured on the printed "
			"2-39 lamp location drawing.",
			"Playfield general illumination (G.I. strings 1, 2 and 5, public 0, 1 and 4) has no factory socket list; every "
			"coordinate comes from the table's G.I. collections.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 975.0, "bottom": 1974.0},
			"x": "x/975; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/the-shadow-1994/vpw-mod-1.0/extracted-vpxtool.manifest.json",
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
		"observed_input_addresses": sorted(observed_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=order),
		"observed_output_bindings": sorted(observed_outputs, key=order),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
		"unplaced_output_bindings": sorted(unplaced_outputs, key=order),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())
		] + [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"coordinate_origins": {
			"bounding_box_centers": [
				"Walls Leftslingshot and Rightslingshot (switches 61/62, solenoids 9/10), WallTarget (51, 8, 16), sw35, sw55 "
				"(55, 25, 36), sw71-sw74, sw81, sw82, sw84 and sw85-sw88",
			],
			"mesh_bounding_box_centers": [
				"Primitive SlingMiniPF (switch 36, solenoids 15, 19, 20) and the diverter blade meshes Div_Bot_Left/Div_Bot_Right "
				"and Div_Top_Left/Div_Top_Right (solenoids 3-6, placed at the midpoint of each pair); these primitives are baked "
				"at world coordinates, so the vertex bounding-box centers of their .obj files in the manifest-pinned extraction "
				"are used (world x = obj x, world y = obj y)",
			],
			"wall_pair_midpoints": [
				"Solenoid 24: the midpoint of the drag-point bounding-box centers of walls sw86 and sw87",
			],
			"object_centers": "every other placement uses its retained object's own center",
		},
		"excluded_object_classes": [
			"Off-playfield helper lights l81-l84 and L117, L118, L126-L128 (x < 0) that the VPW script drives.",
			"The Flasher glow images F117, F118 and F181-F184 and their reflection sprites, which only the older Skitso script binds.",
			"Reflection sprites (*_ref) and the Flupper dome flash, bloom and light layers; only each dome's base primitive is placed.",
			"The co-located duplicate G.I. lights and the wide G.I. fill LB13.",
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Shadow (Bally, 1994) spatial review",
		"",
		f"Status: {report['status']}. Every switch, coil, motor, magnet and lamp and every flasher except 17 and 18 and every lamp except the ramp rings 81-84 is placed "
		"from the retained VPW table or carries a controlled `not_applicable` record, but every placement stays `observed`, which keeps the "
		"record at `machines/partial/bally/the-shadow-1994.json`.",
		"",
		f"The geometry source is `The Shadow (Bally 1994) VPW Mod v1.0.vpx` (SHA-256 `{TABLE_SHA256}`); its embedded script "
		f"(SHA-256 `{SCRIPT_SHA256}`) is the runtime binding authority. Exact playfield bounds are `{TABLE_BOUNDS}`; every "
		"coordinate is x/975 and y/1974 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- The VPW script is the runtime authority; the November 1994 operations manual is the physical inventory, "
		"construction and wiring authority; pinned PinMAME owns controller topology; the retained table supplies geometry.",
		"- The trough optos, the lock positions and the Battlefield kicker opto are documented projections onto the "
		"mechanism that carries them; the diverter, kicker-head, slide-motor and mini drop-target reset coils are projections "
		"derived from the geometry of the parts they move.",
		"- G.I. strings 3 and 4 (the insert strings) and the backbox bulbs of flashers 17, 18 and 26-28 are backbox "
		"devices and are not placed.",
		"",
		"## Blockers",
		"",
	]
	lines += [f"- {blocker}" for blocker in report["blockers"]]
	lines += ["", "## Explicit projections", ""]
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
		f"- Unplaced output bindings: {len(report['unplaced_output_bindings'])}",
	]
	lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
	lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Refused. `coverage.missing` is `" + json.dumps(list(COVERAGE_MISSING)) + "`: the placements come from one table "
		"lineage and have not been reconciled against the manual's location drawings, three flashers have an unplaced "
		"second socket, flashers 17 and 18 and the ramp-ring lamps 81-84 are not placed, and the playfield G.I. sockets come only from the table's G.I. collections.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Operations manual SHA-256 `{MANUAL_SHA256}`.",
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
		raise RuntimeError("Stale The Shadow author-ready definition is still present")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"The Shadow artifact is missing: {path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"The Shadow definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"The Shadow seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"The Shadow spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"The Shadow spatial review drifted from its deterministic curator: {markdown_path}")
	print("The Shadow definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"The Shadow extraction manifest written: {write_extraction_manifest(root)}")
	elif args.verify_extraction:
		root = configured_vpx_sources_root(required=True)
		assert root is not None
		verify_extraction_manifest(root)
		print("The Shadow retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
