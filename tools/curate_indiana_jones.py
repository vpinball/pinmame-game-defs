"""Curate the physical Williams Indiana Jones: The Pinball Adventure (1993) machine definition.

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
# Stays partial: public switches 71 (Captive Ball Front) and 121-123 (Wheel Position 1-3) are
# printed opto interrupters that pinned PinMAME's ijGameData inverted-switch mask does not
# normalize (see conflict.captive-ball-front-opto-not-normalized and
# conflict.wheel-position-opto-not-normalized, both unresolved).
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/indiana-jones-the-pinball-adventure-1993.json"
PARTIAL_PATH = ROOT / "machines/partial/williams/indiana-jones-the-pinball-adventure-1993.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/indiana-jones-the-pinball-adventure-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/indiana-jones-the-pinball-adventure-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/indiana-jones-the-pinball-adventure-1993.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-dcs"
MANUAL_SOURCE = "manual.williams.indiana-jones-the-pinball-adventure.1993"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.indiana-jones-the-pinball-adventure.1993"
VPX_TABLE_SOURCE = "vpx-table.ij-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.ij-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ij-vpw-1-0"

TABLE_SHA256 = "03451b7951242d204f9f79ab91f108d3c8aa203039f2ca867b24f4f47668c250"
SCRIPT_SHA256 = "926e7a90d89602b003ac93757ee23c6ae916bb382112be28f82388381490bb7a"
MANUAL_SHA256 = "97a8202c5d95de743db7acf36567342cb71b2334188225d9b107787b5691ad43"
MANUAL_TRANSCRIPTION_SHA256 = "5a083e87ffc8aa0237d72b98848fa58d4450f848e25535e5ae4a945d6015c8f3"

EXTRACTION_RELATIVE_PATH = Path("williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "438995cdc586b0ba83f6e683b9e0576530517f6e0a5afa86f2dd1236d5bbfb40"
EXTRACTION_FILE_COUNT = 2027
EXTRACTION_TOTAL_BYTES = 362116168

# WIDE-BODY "Superpin" playfield: normalize x/1093, y/2162 (not the 952-wide divisor every other
# curated WPC game uses). Using 952 here would stretch every x coordinate ~15% and corrupt the set.
TABLE_BOUNDS = "left=0 top=0 right=1093 bottom=2162"
PLAYFIELD_WIDTH = 1093.0
PLAYFIELD_HEIGHT = 2162.0

DRIVER_IDS = (
	"ij_l7", "ij_d7", "ij_h1", "ij_i1", "ij_lg7", "ij_dg7", "ij_l6", "ij_d6",
	"ij_l5", "ij_d5", "ij_l4", "ij_d4", "ij_l3", "ij_d3", "ij_p2",
)
DRIVER_COMPATIBILITY = {
	"ij_l7": ("identical", "Williams production L-7 game ROM shipped with the physical machine; the retained known-working VPW table binds to this driver (cGameName = \"ij_l7\")."),
	"ij_d7": ("identical", "D-7 LED Ghost Fix revision of L-7; corrects a dot-matrix display artifact only, same switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware."),
	"ij_h1": ("identical", "HK-1 \"No Hate Speech\" localization revision; text/audio content change only, no controller-address or playfield change."),
	"ij_i1": ("identical", "I-1 \"No Hate Speech, LED Ghost Fix\" combined localization/display revision of the same physical machine."),
	"ij_lg7": ("identical", "LG-7 German-language revision of L-7; text/audio content change only."),
	"ij_dg7": ("identical", "DG-7 German-language revision with the LED Ghost Fix."),
	"ij_l6": ("identical", "L-6 game ROM; an earlier firmware revision of the same physical machine with no controller-address or playfield change."),
	"ij_d6": ("identical", "D-6 LED Ghost Fix revision of L-6."),
	"ij_l5": ("identical", "L-5 game ROM; an earlier firmware revision of the same physical machine."),
	"ij_d5": ("identical", "D-5 LED Ghost Fix revision of L-5."),
	"ij_l4": ("identical", "L-4 game ROM; an earlier firmware revision of the same physical machine."),
	"ij_d4": ("identical", "D-4 LED Ghost Fix revision of L-4."),
	"ij_l3": ("identical", "L-3 game ROM; an earlier firmware revision of the same physical machine, using the earlier DCS sound ROM set (ijsnd_l1)."),
	"ij_d3": ("identical", "D-3 LED Ghost Fix revision of L-3."),
	"ij_p2": ("compatible", "P-2 prototype game ROM for the same physical machine; pre-production firmware, retained as a documented prototype variant rather than the shipped default."),
}

# --- Printed switch matrix (manual page 2-46 grid, 2-47 parts list "Where Used" column).
SWITCH_LABELS = {
	11: "Single Drop Target", 12: "Buy-in Button", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Left Outlane", 16: "Left Return Lane", 17: "Right Return Lane", 18: "Right Outlane Top",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Opto", 24: "Always Closed",
	25: "(I)ndy Lane", 26: "I(n)dy Lane", 27: "In(d)y Lane", 28: "Ind(y) Lane",
	31: "Left Eject", 32: "Exit Idol", 33: "Left Slingshot", 34: "Gun Trigger",
	35: "Left Jet", 36: "Right Jet", 37: "Bottom Jet", 38: "Center Standup",
	41: "Left Ramp Enter", 42: "Right Ramp Enter", 43: "Top Idol Enter", 44: "Right Popper",
	45: "Center Enter", 46: "Top Post", 47: "Subway Lockup", 48: "Right Slingshot",
	51: "Advent(u)re Target", 52: "Adventu(r)e Target", 53: "Adventur(e) Target",
	54: "Left Loop Top", 55: "Left Loop Bottom", 56: "Right Loop Top", 57: "Right Loop Bottom",
	58: "Right Outlane Bottom",
	61: "(A)dventure Target", 62: "A(d)venture Target", 63: "Ad(v)enture Target",
	64: "Captive Ball Back", 65: "Mini Top Left", 66: "Mini Middle Top Left",
	67: "Mini Middle Bottom Left", 68: "Mini Bottom Left",
	71: "Captive Ball Front", 72: "Mini Top Hole", 73: "Mini Bottom Hole", 74: "Right Ramp Made",
	75: "Mini Top Right", 76: "Mini Middle Top Right", 77: "Mini Middle Bottom Right",
	78: "Mini Bottom Right",
	81: "Trough 6", 82: "Trough 5", 83: "Trough 4", 84: "Trough 3", 85: "Trough 2",
	86: "Trough 1", 87: "Top Trough", 88: "Shooter",
}
# Printed on the A-13901-2 "3-sw. Opto PCB Assembly (for idol)" and A-16657 "Motor Opto Switch
# PCB Assembly (for mini playfield)" schematics as switch column 9 (public 91-95); PinMAME's own
# CORE_CUSTSWCOL=12 constant reports the same physical switches at public 121-125. See
# manual-transcription.md "Custom switch column" for the full derivation.
CUSTOM_SWITCH_LABELS = {
	121: "Wheel Position 1", 122: "Wheel Position 2", 123: "Wheel Position 3",
	124: "Mini Playfield Left Limit", 125: "Mini Playfield Right Limit",
}
CUSTOM_SWITCH_MANUAL_ALIAS = {121: "91", 122: "92", 123: "93", 124: "94", 125: "95"}
CUSTOM_SWITCH_UNUSED = (126, 127, 128)

# Every switch shaded/identified as an opto interrupter on 2-47 (LED+phototransistor part pair,
# or a board the Section 3 TOC itself names "Opto": A-16384-1 Flipper Opto PCB, A-13609 3-bank
# Opto Drop Target, A-16657 Motor Opto Switch PCB).
OPTO_SWITCHES = {41, 42, 43, 44, 45, 47, 71, 72, 73, 81, 82, 83, 84, 85, 86, 87, 112, 114, 115, 116, 117, 121, 122, 123, 124, 125}
# ijGameData.wpc.invSw = {0x00,0x00,0x00,0x00,0x5F,0x00,0x00,0x06,0x7F,0x00,0x00,0x70,0x18}
# decoded per switch-matrix column (see manual-transcription.md). Column 4 (0x5F) normalizes
# 41,42,43,44,45,47; column 7 (0x06) normalizes only 72,73 (NOT 71); column 8 (0x7F) normalizes
# all seven trough optos 81-87; the flipper column (0x70) normalizes 115,116,117 through the
# same invSw path (111-114 are separately, unconditionally complemented by the unique WPC_FLIPPERS
# hardware register read, per controllers/pinmame/wpc-dcs.json); the custom column (0x18)
# normalizes only 124,125 (NOT 121,122,123).
PINMAME_NORMALIZED_OPTO_SWITCHES = {41, 42, 43, 44, 45, 47, 72, 73, 81, 82, 83, 84, 85, 86, 87, 115, 116, 117, 124, 125}
# vpmTimer.PulseSw / momentary-hit callers in the retained VPW script.
PULSED_SWITCHES = {33, 35, 36, 37, 38, 48, 51, 52, 53, 64, 65, 66, 67, 68, 75, 76, 77, 78}

SWITCH_TYPES = {
	11: "leaf", 12: "button", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch",
	17: "microswitch", 18: "microswitch", 21: "tilt", 22: "microswitch", 24: "other",
	25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "other", 32: "microswitch", 33: "leaf", 34: "other", 35: "leaf", 36: "leaf", 37: "leaf",
	38: "microswitch", 41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto",
	46: "other", 47: "opto", 48: "leaf",
	51: "microswitch", 52: "microswitch", 53: "microswitch", 54: "microswitch", 55: "microswitch",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "microswitch",
	71: "opto", 72: "opto", 73: "opto", 74: "microswitch", 75: "microswitch", 76: "microswitch",
	77: "microswitch", 78: "microswitch",
	81: "opto", 82: "opto", 83: "opto", 84: "opto", 85: "opto", 86: "opto", 87: "opto",
	88: "microswitch",
}

# address -> (assembly/opto part, switch part), transcribed verbatim from printed 2-47.
SWITCH_PARTS = {
	11: (None, "5647-12693-31"), 12: (None, "20-9663-12"), 13: (None, "20-9663-11"),
	14: (None, "A-6502-A"), 15: (None, "A-12688"), 16: (None, "A-12688"), 17: (None, "A-12688"),
	18: (None, "A-12688-1"), 21: (None, "SW-1A-117"), 22: (None, "5643-09288-00"),
	24: (None, "5643-09288-00"), 25: (None, "A-12688"), 26: (None, "A-12688"),
	27: (None, "A-12688"), 28: (None, "A-12688"),
	31: (None, "5647-12133-11"), 32: (None, "5647-12693-25"),
	33: (None, "SW-1A-114 (kick) with SW-1A-120 (score)"), 34: (None, "5647-12133-12"),
	35: (None, "SW-11A-37"), 36: (None, "SW-11A-37"), 37: (None, "SW-11A-37"),
	38: (None, "A-16816-4"),
	41: ("A-16908 (LED) with A-16909 (phototransistor)", None),
	42: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	43: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	44: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	45: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	46: (None, "5647-12693-56"),
	47: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	48: (None, "SW-1A-114 (kick) with SW-1A-120 (score)"),
	51: (None, "A-14691-4"), 52: (None, "A-14691-4"), 53: (None, "A-14691-4"),
	54: (None, "A-12688"), 55: (None, "A-12688"), 56: (None, "A-12688"), 57: (None, "A-12688"),
	58: (None, "A-12688"),
	61: (None, "A-14691-4"), 62: (None, "A-14691-4"), 63: (None, "A-14691-4"),
	64: (None, "A-16418"), 65: (None, "A-12688"), 66: (None, "A-12688"), 67: (None, "A-12688"),
	68: (None, "A-12688"),
	71: ("A-14231 (LED) with A-14232 (phototransistor)", None),
	72: ("A-16908 (LED) with A-16909 (phototransistor)", None),
	73: ("A-16908 (LED) with A-16909 (phototransistor)", None),
	74: (None, "5647-12693-21"), 75: (None, "A-12688-1"), 76: (None, "A-12688-1"),
	77: (None, "A-12688-1"), 78: (None, "A-12688-1"),
	81: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	82: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	83: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	84: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	85: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	86: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	87: ("A-16927 (LED) with A-16926 (phototransistor)", None),
	88: (None, "A-12688"),
	121: ("A-13901-2 3-sw. Opto PCB Assembly (OPTO1)", None),
	122: ("A-13901-2 3-sw. Opto PCB Assembly (OPTO2)", None),
	123: ("A-13901-2 3-sw. Opto PCB Assembly (OPTO3)", None),
	124: ("A-16657 Motor Opto Switch PCB Assembly (OPTO2)", None),
	125: ("A-16657 Motor Opto Switch PCB Assembly (OPTO1)", None),
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
# Fliptronic F1-F8 wiring, printed 2-46. F5-F8 are footnoted "*Used as switches other than
# flipper switches in this game" -- Center Drop Bank optos and the Left Ramp Made sensor.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J906-1"), 112: ("Blue-Violet", "J905-1"),
	113: ("Black-Blue", "J906-3"), 114: ("Blue-Gray", "J905-2"),
	115: ("Black-Violet", "J906-4"), 116: ("Black-Yellow", "J905-3"),
	117: ("Black-Gray", "J906-5"), 118: ("Black-Blue", "J905-5"),
}
FLIPPER_LABELS = {
	111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", False, "leaf", "SW-1A-194", None),
	112: ("Lower Right Flipper Button", "flipper.lower.right.button", True, "opto", None, "A-16384-1"),
	113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", False, "leaf", "SW-1A-194", None),
	114: ("Lower Left Flipper Button", "flipper.lower.left.button", True, "opto", None, "A-16384-1"),
	115: ("Center Drop Bank Left", "internal.dropbank.center.left", True, "opto", None, "A-13609"),
	116: ("Center Drop Bank Middle", "internal.dropbank.center.middle", True, "opto", None, "A-13609"),
	117: ("Center Drop Bank Right", "internal.dropbank.center.right", True, "opto", None, "A-13609"),
	118: ("Left Ramp Made", "internal.ramp.left.made", False, "microswitch", "5647-12693-21", None),
}

# --- Normalized playfield coordinates derived from the retained VPWmod v1.0 extraction
# (x/1093, y/2162; vpx-geometry.txt).
SWITCH_POSITIONS = {
	11: [(0.714280, 0.143273)], 15: [(0.109276, 0.738360)], 16: [(0.171582, 0.737311)],
	17: [(0.743077, 0.730381)], 18: [(0.821624, 0.698680)],
	25: [(0.343934, 0.107536)], 26: [(0.436105, 0.097570)], 27: [(0.528381, 0.086009)],
	28: [(0.621249, 0.076131)],
	31: [(0.218935, 0.334221)], 32: [(0.886135, 0.642738)], 33: [(0.254015, 0.727135)],
	35: [(0.388764, 0.195046)], 36: [(0.573051, 0.171427)], 37: [(0.519479, 0.260665)],
	38: [(0.434378, 0.357059)],
	41: [(0.316737, 0.307639)], 42: [(0.747484, 0.324472)], 43: [(0.885013, 0.452825)],
	44: [(0.885800, 0.420444)], 45: [(0.498416, 0.328160)], 46: [(0.212015, 0.032900)],
	47: [(0.819061, 0.419203)], 48: [(0.659250, 0.725416)],
	51: [(0.792932, 0.530032)], 52: [(0.792551, 0.555538)], 53: [(0.793345, 0.580452)],
	54: [(0.129995, 0.387402)], 55: [(0.110753, 0.248745)], 56: [(0.931038, 0.214986)],
	57: [(0.871258, 0.323506)], 58: [(0.821661, 0.778811)],
	61: [(0.131860, 0.558002)], 62: [(0.132943, 0.530771)], 63: [(0.134206, 0.502726)],
	64: [(0.780986, 0.009628)],
	65: [(0.116786, 0.093645)], 66: [(0.105965, 0.176222)], 67: [(0.116792, 0.255833)],
	68: [(0.105997, 0.338951)],
	71: [(0.739447, 0.088151)], 72: [(0.164755, 0.174972)], 73: [(0.163853, 0.333311)],
	74: [(0.647551, 0.120534)], 75: [(0.211864, 0.094018)], 76: [(0.223033, 0.177296)],
	77: [(0.212619, 0.255002)], 78: [(0.222763, 0.339082)],
	88: [(0.946736, 0.898720)],
}
# Trough 6..Top(81-87) have no distinct playfield object; cvpmTrough's own construction
# (`.InitSwitches Array(86,85,84,83,82,81)` and `.InitExit BallRelease,70,15`) shares the single
# retained "Ballrelease" kicker as the trough's own exit mechanism.
TROUGH_ANCHOR = (0.871128, 0.877620)
# Wheel Position 1-3 (121-123) sense the rotating idol figure's angular position, not a fixed
# point; projected onto the figure's own table-object center exactly like Monster Bash's
# Dracula-position optos.
IDOL_FIGURE_ANCHOR = (0.884721, 0.505550)
# Mini Playfield Left/Right Limit (124/125) sense the tilting mini-playfield's own extremes;
# projected onto the mini-playfield assembly's own table-object center.
MINI_PLAYFIELD_ANCHOR = (0.163769, 0.253080)

SWITCH_PROJECTIONS = {
	81: "Projected onto the retained \"Ballrelease\" kicker (trough exit / Ball Release coil position): cvpmTrough's own construction (.InitSwitches Array(86,85,84,83,82,81), .InitExit BallRelease,70,15) has no individual playfield object per ball position, only the shared exit kicker.",
	82: "Projected onto the retained \"Ballrelease\" kicker; see switch 81.",
	83: "Projected onto the retained \"Ballrelease\" kicker; see switch 81.",
	84: "Projected onto the retained \"Ballrelease\" kicker; see switch 81.",
	85: "Projected onto the retained \"Ballrelease\" kicker; see switch 81.",
	86: "Projected onto the retained \"Ballrelease\" kicker; see switch 81.",
	87: "Projected onto the retained \"Ballrelease\" kicker (trough exit): the retained script pulses this switch from SolBallRelease whenever bsTrough.Balls is nonzero (relationship.ball-release-top-trough-pulse), not from a distinct Top Trough playfield object.",
	121: "Projected onto the rotating idol figure (Primitive totem, table object center): the retained script's UpdateIdol_timer sets Controller.Switch(121/122/123) directly from a 360-degree motor-position counter (60-degree sextants), not from three separate playfield objects.",
	122: "Projected onto the rotating idol figure (Primitive totem, table object center); see switch 121.",
	123: "Projected onto the rotating idol figure (Primitive totem, table object center); see switch 121.",
	124: "Projected onto the tilting mini-playfield assembly (Primitive minipf, table object center): the retained script's POAMech (vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear, .AddSw 124,0,0) sets this switch from the mechanism's own 9-step linear position counter, not from a separate playfield sensor object.",
	125: "Projected onto the tilting mini-playfield assembly (Primitive minipf, table object center); see switch 124.",
}

# --- Printed solenoid/flasher table (manual pages 2-50 table, 2-51 wiring/location).
SOLENOID_LABELS = {
	1: "Ball Popper", 2: "Ball Launch", 3: "Totem Drop Up", 4: "Ball Release",
	5: "Center Drop Bank", 6: "Idol Release", 7: "Knocker", 8: "Left Eject",
	9: "Left Jet Bumper", 10: "Right Jet Bumper", 11: "Bottom Jet Bumper",
	12: "Right Slingshot", 13: "Left Slingshot",
	14: "Left Control Gate", 15: "Right Control Gate", 16: "Totem Drop Down",
	17: "Eternal Life", 18: "Light Jackpot", 19: "Super Jackpot", 20: "Jackpot",
	21: "Path Of Adventure", 22: "Mini Motor Left", 23: "Mini Motor Right",
	24: "Plane Gun LEDs", 25: "Dogfight Hurry Up", 26: "Right Ramp", 27: "Left Ramp",
	28: "Subway Release",
	33: "Diverter Power", 34: "Diverter Hold", 35: "Top Lockup Power", 36: "Top Lockup Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	51: "Left Side Flasher", 52: "Right Side Flasher", 53: "Special Flasher",
	54: "Totem Flasher", 55: "Jackpot Multiplier Flasher", 56: "Wheel Motor",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	37: "Unused WPC-DCS Address 37",
	38: "Unused WPC-DCS Address 38",
	39: "Unused WPC-DCS Address 39",
	40: "Unused WPC-DCS Address 40",
	41: "Unused WPC-DCS Address 41",
	42: "Unused WPC-DCS Address 42",
	43: "Unused WPC-DCS Address 43",
	44: "Unused WPC-DCS Address 44",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
	57: "Unused 8-Driver Board Position 7",
	58: "Unused 8-Driver Board Position 8",
}
# Manual solenoid/flasher table addresses that differ from the PinMAME public address.
MANUAL_SOLENOID_ALIASES = {45: "29", 46: "30", 47: "31", 48: "32", 51: "37", 52: "38", 53: "39", 54: "40", 55: "41", 56: "42"}

SOLENOID_WIRING = {
	1: dict(driver_transistor="Q82", control_connection="J130-1", power_connection="J107-3", control_wire="Vio-Brn", part_number="AE-26-1200", printed_type="High Power"),
	2: dict(driver_transistor="Q80", control_connection="J130-2", power_connection="J107-3", control_wire="Vio-Red", part_number="AE-23-800", printed_type="High Power"),
	3: dict(driver_transistor="Q78", control_connection="J130-4", power_connection="J107-3", control_wire="Vio-Org", part_number="AE-26-1200", printed_type="High Power"),
	4: dict(driver_transistor="Q76", control_connection="J130-5", power_connection="J107-3", control_wire="Vio-Yel", part_number="AE-26-1500", printed_type="High Power"),
	5: dict(driver_transistor="Q64", control_connection="J130-6", power_connection="J107-3", control_wire="Vio-Grn", part_number="AE-26-1200", printed_type="High Power"),
	6: dict(driver_transistor="Q66", control_connection="J130-7", power_connection="J107-3", control_wire="Vio-Blu", part_number="AE-26-1200", printed_type="High Power"),
	7: dict(driver_transistor="Q68", control_connection="J130-8", power_connection="J107-3", control_wire="Vio-Blk", part_number="AE-23-800", printed_type="High Power"),
	8: dict(driver_transistor="Q70", control_connection="J130-9", power_connection="J107-3", control_wire="Vio-Gry", part_number="AE-26-1200", printed_type="High Power"),
	9: dict(driver_transistor="Q58", control_connection="J127-1", power_connection="J107-2", control_wire="Brn-Blk", part_number="AE-26-1200", printed_type="Low Power"),
	10: dict(driver_transistor="Q56", control_connection="J127-3", power_connection="J107-2", control_wire="Brn-Red", part_number="AE-26-1200", printed_type="Low Power"),
	11: dict(driver_transistor="Q54", control_connection="J127-4", power_connection="J107-2", control_wire="Brn-Org", part_number="AE-26-1200", printed_type="Low Power"),
	12: dict(driver_transistor="Q52", control_connection="J127-5", power_connection="J107-2", control_wire="Brn-Yel", part_number="AE-27-1200", printed_type="Low Power"),
	13: dict(driver_transistor="Q50", control_connection="J127-6", power_connection="J107-2", control_wire="Brn-Grn", part_number="AE-27-1200", printed_type="Low Power"),
	14: dict(driver_transistor="Q48", control_connection="J127-7", power_connection="J107-2", control_wire="Brn-Blu", part_number="A-14406", printed_type="Low Power"),
	15: dict(driver_transistor="Q46", control_connection="J127-8", power_connection="J107-2", control_wire="Brn-Vio", part_number="A-14406", printed_type="Low Power"),
	16: dict(driver_transistor="Q44", control_connection="J127-9", power_connection="J107-2", control_wire="Brn-Gry", part_number="SM1-26-600", printed_type="Low Power"),
	17: dict(driver_transistor="Q42", control_connection="J126-1", power_connection="J107-6", control_wire="Blk-Brn", printed_type="Flasher"),
	18: dict(driver_transistor="Q40", control_connection="J126-2", power_connection="J107-6", control_wire="Blk-Red", printed_type="Flasher"),
	19: dict(driver_transistor="Q38", control_connection="J126-3", power_connection="J107-6", control_wire="Blk-Org", printed_type="Flasher"),
	20: dict(driver_transistor="Q36", control_connection="J126-4", power_connection="J107-6", control_wire="Blk-Yel", printed_type="Flasher"),
	21: dict(driver_transistor="Q28", control_connection="J126-5", power_connection="J107-6", control_wire="Blu-Grn", printed_type="Flasher"),
	22: dict(driver_transistor="Q30", control_connection="J126-6", power_connection="J118-2", control_wire="Blu-Blk", printed_type="Low Power motor"),
	23: dict(driver_transistor="Q34", control_connection="J126-7", power_connection="J118-2", control_wire="Blu-Vio", part_number="14-7988", printed_type="Low Power motor"),
	24: dict(driver_transistor="Q32", control_connection="J126-8", power_connection="J118-2", control_wire="Blu-Gry", part_number="A-16834", printed_type="Flasher"),
	25: dict(driver_transistor="Q26", control_connection="J122-1", power_connection="J107-6", control_wire="Blu-Brn", printed_type="Gen. Purpose"),
	26: dict(driver_transistor="Q24", control_connection="J122-2", power_connection="J107-6", control_wire="Blu-Red", printed_type="Gen. Purpose"),
	27: dict(driver_transistor="Q22", control_connection="J122-3", power_connection="J107-6", control_wire="Blu-Org", printed_type="Gen. Purpose"),
	28: dict(driver_transistor="Q20", control_connection="J122-4", power_connection="J107-1", control_wire="Blu-Yel", part_number="AE-26-1500", printed_type="Gen. Purpose"),
	33: dict(driver_transistor="Q2", control_connection="J902-6", power_connection="J907-1", control_wire="Blk-Yel", part_number="FL-11753-1", printed_type="Diverter power"),
	34: dict(driver_transistor="Q7", control_connection="J902-4", power_connection="J907-1", control_wire="Org-Vio", part_number="FL-11753-1", printed_type="Diverter hold"),
	35: dict(driver_transistor="Q1", control_connection="J902-3", power_connection="J907-4", control_wire="Blk-Blu", part_number="A-15943", printed_type="Top Lockup power"),
	36: dict(driver_transistor="Q5", control_connection="J902-1", power_connection="J907-4", control_wire="Org-Gry", part_number="A-15943", printed_type="Top Lockup hold"),
	45: dict(driver_transistor="Q4", control_connection="J902-13", power_connection="J907-7", control_wire="Blu-Vio", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(driver_transistor="Q11", control_connection="J902-11", power_connection="J907-7", control_wire="Org-Grn", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(driver_transistor="Q3", control_connection="J902-9", power_connection="J907-9", control_wire="Blu-Gry", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(driver_transistor="Q9", control_connection="J902-7", power_connection="J907-9", control_wire="Org-Blu", part_number="FL-11629", printed_type="Fliptronic hold"),
	51: dict(driver_transistor="Q16", control_connection="J4-2", power_connection="J107-6", control_wire="Brn-Wht", printed_type="Flasher (8-Driver Board)"),
	52: dict(driver_transistor="Q15", control_connection="J4-4", power_connection="J107-6", control_wire="Blk-Wht", printed_type="Flasher (8-Driver Board)"),
	53: dict(driver_transistor="Q14", control_connection="J4-5", power_connection="J107-6", control_wire="Org-Wht", printed_type="Flasher (8-Driver Board)"),
	54: dict(driver_transistor="Q13", control_connection="J4-6", power_connection="J107-6", control_wire="Yel-Wht", printed_type="Flasher (8-Driver Board)"),
	55: dict(driver_transistor="Q9", control_connection="J3-2", power_connection="J107-6", control_wire="Grn-Wht", printed_type="Flasher (8-Driver Board)"),
	56: dict(driver_transistor="Q10", control_connection="J3-3", power_connection="J118-2", control_wire="Blu-Wht", part_number="14-7982", printed_type="Low Power motor (8-Driver Board)"),
}
SOLENOID_ASSEMBLIES = {
	1: "A-16231", 2: "A-14525", 3: "A-14615", 4: "A-16765", 5: "A-16032-2", 6: "A-16226",
	7: "B-10686-1", 8: "A-17073", 9: "A-9415-2", 10: "A-9415-2", 11: "A-9415-2",
	12: "A-14369-R", 13: "A-14369-L", 14: "A-14422", 15: "A-14422", 16: "A-14615",
	17: "A-12336-1", 18: "A-16824", 19: "A-9302", 20: "A-8798", 21: "A-8798",
	22: "A-16738", 23: "A-16738", 24: "A-16834", 25: "A-9359", 26: "A-8798/A-16861",
	27: "A-16861", 28: "A-16317",
	33: "A-16301", 34: "A-16301", 35: "A-16656", 36: "A-16656",
	45: "A-15205-R-2", 46: "A-15205-R-2", 47: "A-15205-L-2", 48: "A-15205-L-2",
	51: "A-8798", 52: "A-8798", 53: "A-9302", 54: "A-9302", 55: "A-8798", 56: "A-16228",
}
# Retained VPW script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "bsPopper.SolOut", 2: "AutoPlunger (Plunger.Fire)", 3: "TotemDropUP",
	4: "SolBallRelease (bsTrough.ExitSol_On, pulses switch 87)", 5: "ResetDrops (DTRaise 115/116/117)",
	6: "SolIdol", 7: "vpmSolSound SoundFX(\"fx_Knocker\")", 8: "bsLEject.SolOut",
	12: "RandomSoundSlingshotRight", 13: "RandomSoundSlingshotLeft",
	14: "vpmSolGate LeftGate", 15: "vpmSolGate RightGate", 16: "TotemDropDOWN",
	17: "SolFlash17 (SetLamp 117,1)", 18: "SolFlash18", 19: "SetLamp 119",
	20: "SetModLamp 20", 21: "SetModLamp 21", 22: "PoAMoveLeft", 23: "PoAMoveRight",
	24: "SetModLamp 24", 25: "SetLamp 125", 26: "SolFlash26", 27: "SolFlash27",
	28: "bsSubway.SolOut", 33: "SolDivPower", 34: "SolDivHold", 35: "SolTopPostPower",
	36: "SolTopPostHold", 45: "SolRFlipper (core.vbs sLRFlipper)", 47: "SolLFlipper (core.vbs sLLFlipper)",
	51: "solflash51", 52: "SolFlash52", 53: "SetLamp 116 (-> L153L, L153R)",
	54: "SetLamp 115 (-> f54)", 55: "solflash55", 56: "SolMoveIdol",
}

FLASHER_BULBS = {
	17: ("#906 (1) on the playfield and #906 (3) on the back panel", 1),
	18: ("#906 (1) on the playfield", 1),
	19: ("#89 (1) on the playfield", 1),
	20: ("#89 (1) on the playfield and #906 (2) on the back panel", 1),
	21: ("#89 (1) on the playfield and #906 (4) on the back panel", 1),
	24: ("A-16834 gun-flash LEDs on both biplane toys", 2),
	25: ("#89 (1) on the playfield", 1),
	26: ("#89 (3) on the playfield and #906 (1) on the back panel", 1),
	27: ("#89 (1) on the playfield and #906 (1) on the back panel", 1),
	51: ("#89 (2) on the playfield and #906 (1) on the back panel", 2),
	52: ("#89 (2) on the playfield and #906 (1) on the back panel; only one distinct playfield object was located in the retained extraction despite the printed (2) quantity", 1),
	53: ("#89 (2) on the playfield", 2),
	54: ("#89 (1) on the playfield", 1),
	55: ("#89 (1) on the playfield", 1),
}
FLASHER_POSITIONS = {
	17: [(0.457200, 0.863595)],
	18: [(0.317540, 0.282086)],
	19: [(0.610776, 0.367581)],
	20: [(0.709729, 0.337388)],
	21: [(0.769128, 0.343295)],
	24: [(0.784908, 0.258922), (0.874642, 0.284902)],
	25: [(0.527575, 0.372064)],
	26: [(0.640753, 0.179440)],
	27: [(0.355951, 0.179590)],
	51: [(0.055378, 0.627677), (0.069451, 0.560307)],
	52: [(0.782251, 0.392114)],
	53: [(0.111182, 0.677388), (0.821803, 0.736443)],
	54: [(0.669210, 0.238419)],
	55: [(0.570108, 0.298602)],
}

# --- Printed lamp matrix (manual page 2-48 grid, 2-49 parts list). First digit is the column.
LAMP_LABELS = {
	11: "Mode Start", 12: "Hand of Fate", 13: "Eject Extra Ball", 14: "Ad(v)enture Light",
	15: "A(d)venture Light", 16: "(A)dventure Light", 17: "Shoot Again", 18: "Get The Idol",
	21: "Tank Chase", 22: "Adven(t)ure Light", 23: "Adv(e)nture Light", 24: "Adve(n)ture Light",
	25: "Steal The Stones", 26: "Grail Jackpot", 27: "Streets Of Cairo", 28: "Stones Jackpot",
	31: "Left Ramp Arrow", 32: "Castle Grunewald", 33: "Left Plane Top", 34: "Monkey Brains",
	35: "Left Plane Middle", 36: "Sallah", 37: "Bonus 4X", 38: "Left Plane Bottom",
	41: "Mine Cart", 42: "Ark Jackpot", 43: "Raven Bar", 44: "Right Plane Middle",
	45: "Bonus 6X", 46: "Right Plane Bottom", 47: "Well Of Souls", 48: "Left Loop",
	51: "Choose Wisely", 52: "Right Plane Top", 53: "Rope Bridge", 54: "Advent(u)re Light",
	55: "Adventu(r)e Light", 56: "Adventur(e) Light", 57: "The 3 Challenges", 58: "Right Loop",
	61: "(I)-N-D-Y", 62: "I-(N)-D-Y", 63: "I-N-(D)-Y", 64: "I-N-D-(Y)", 65: "Willie",
	66: "Bonus 2X", 67: "Shorty", 68: "Right Ramp Arrow",
	71: "Mini Top Left", 72: "Mini Top Right", 73: "Mini Middle Top Left",
	74: "Mini Middle Top Right", 75: "Mini Top Arrow", 76: "Marion", 77: "Bonus 8X",
	78: "Dr. Jones",
	81: "Mini Middle Bottom Left", 82: "Mini Middle Bottom Right", 83: "Mini Bottom Left",
	84: "Mini Bottom Right", 85: "Mini Bottom Arrow", 86: "Totem Top Arrow",
	87: "Center Lock", 88: "Start Button",
}
LAMP_ASSEMBLIES = {
	11: "A-16716-2", 12: "A-16716-2", 13: "A-16716-2", 14: "A-16716-2", 15: "A-16716-2",
	16: "A-16716-2", 17: "A-16716-2", 18: "A-16716-2",
	21: "A-16716-2", 22: "A-16716-2", 23: "A-16716-2", 24: "A-16716-2", 25: "A-16716-2",
	26: "A-16716-2", 27: "A-16716-2", 28: "A-16716-2",
	31: "A-16716-2", 32: "A-16716-2", 33: "A-16716-2", 34: "A-16716-2", 35: "A-16716-2",
	36: "A-16716-2", 37: "A-16716-2", 38: "A-16716-2",
	41: "A-16716-2", 42: "A-16716-2", 43: "A-16716-2", 44: "A-16716-2", 45: "A-16716-2",
	46: "A-16716-2", 47: "A-16716-2", 48: "A-11754",
	51: "A-16716-2", 52: "A-16716-2", 53: "A-16716-2", 54: "A-16716-2", 55: "A-16716-2",
	56: "A-16716-2", 57: "A-16716-2", 58: "B-15648",
	61: "A-16739", 62: "A-16739", 63: "A-16739", 64: "A-16739", 65: "A-16823",
	66: "A-16823", 67: "A-16823", 68: "A-11754",
	71: "A-16746", 72: "A-16746", 73: "A-16746", 74: "A-16746", 75: "A-16746",
	76: "A-16823", 77: "A-16823", 78: "A-16823",
	81: "A-16747", 82: "A-16747", 83: "A-16747", 84: "A-16747", 85: "A-16747",
	86: "A-11754", 87: "A-11754", 88: "20-9663-11",
}
LAMP_BULB_TYPES = {48: "#44", 68: "#44", 86: "#44", 87: "#44"}
# Typographic slip on the lamp-matrix page (2-48) against the authoritative parts list (2-49).
LAMP_MATRIX_PAGE_TYPOS = {23: "ADV(E)TURE LIGHT"}
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
LAMP_POSITIONS = {
	11: [(0.242438, 0.393964)], 12: [(0.256729, 0.426855)], 13: [(0.269461, 0.459373)],
	14: [(0.187662, 0.512837)], 15: [(0.187177, 0.540333)], 16: [(0.186417, 0.568758)],
	17: [(0.210565, 0.609789)], 18: [(0.286764, 0.643392)],
	21: [(0.397898, 0.467435)], 22: [(0.488456, 0.420840)], 23: [(0.391549, 0.396916)],
	24: [(0.439210, 0.408910)], 25: [(0.395538, 0.541587)], 26: [(0.458964, 0.501976)],
	27: [(0.398588, 0.617327)], 28: [(0.458338, 0.576330)],
	31: [(0.334208, 0.415917)], 32: [(0.285450, 0.494122)], 33: [(0.292720, 0.531033)],
	34: [(0.284052, 0.566229)], 35: [(0.292867, 0.607097)], 36: [(0.457489, 0.697675)],
	37: [(0.384570, 0.696819)], 38: [(0.294058, 0.679592)],
	41: [(0.523042, 0.540992)], 42: [(0.459804, 0.650463)], 43: [(0.629552, 0.643185)],
	44: [(0.625813, 0.605496)], 45: [(0.534935, 0.697395)], 46: [(0.625711, 0.682390)],
	47: [(0.521767, 0.618522)], 48: [(0.161254, 0.434987)],
	51: [(0.630997, 0.493787)], 52: [(0.626020, 0.530651)], 53: [(0.631685, 0.567693)],
	54: [(0.742539, 0.537134)], 55: [(0.741859, 0.565334)], 56: [(0.741705, 0.592639)],
	57: [(0.522886, 0.466869)], 58: [(0.778669, 0.450581)],
	61: [(0.344493, 0.047961)], 62: [(0.436225, 0.043678)], 63: [(0.527738, 0.037143)],
	64: [(0.621701, 0.030863)], 65: [(0.353297, 0.732614)], 66: [(0.329906, 0.760139)],
	67: [(0.337889, 0.797691)], 68: [(0.682419, 0.445444)],
	76: [(0.563087, 0.735181)], 77: [(0.586000, 0.763291)], 78: [(0.573940, 0.799810)],
	86: [(0.692583, 0.188473)], 87: [(0.498354, 0.357866)],
}
# 71-75/81-85 (mini-playfield inserts) have no distinct retained-table object of their own -- the
# script drives every one of them through `DisableLighting Li<n>on, 600,` against Primitive
# objects that all share one raw local coordinate because they are children of the tilting
# mini-playfield group. Each is projected onto the real switch/trigger object at the same lane
# position.
LAMP_PROJECTIONS = {
	71: ("switch.matrix-65", "Projected onto the Mini Top Left switch/trigger object (table object center): the mini-playfield insert lamp has no distinct retained-table object -- the script drives it through `DisableLighting Li71on, 600,` against a Primitive that shares a single raw local coordinate with every other mini-playfield insert lamp because it is a child of the tilting mini-playfield group."),
	72: ("switch.matrix-75", "Projected onto the Mini Top Right switch/trigger object (table object center); see lamp 71."),
	73: ("switch.matrix-66", "Projected onto the Mini Middle Top Left switch/trigger object (table object center); see lamp 71."),
	74: ("switch.matrix-76", "Projected onto the Mini Middle Top Right switch/trigger object (table object center); see lamp 71."),
	75: ("mechanism.path-of-adventure entrance (Trigger EnterPoA, table object center)", "Projected onto the retained \"EnterPoA\" trigger, the Path of Adventure entrance sensor immediately behind the Top Post; the \"Mini Top Arrow\" insert marks the entrance and has no distinct lamp object of its own; see lamp 71."),
	81: ("switch.matrix-67", "Projected onto the Mini Middle Bottom Left switch/trigger object (table object center); see lamp 71."),
	82: ("switch.matrix-77", "Projected onto the Mini Middle Bottom Right switch/trigger object (table object center); see lamp 71."),
	83: ("switch.matrix-68", "Projected onto the Mini Bottom Left switch/trigger object (table object center); see lamp 71."),
	84: ("switch.matrix-78", "Projected onto the Mini Bottom Right switch/trigger object (table object center); see lamp 71."),
	85: ("mechanism.path-of-adventure exit (Trigger ExitPoA, table object center)", "Projected onto the retained \"ExitPoA\" trigger, the Path of Adventure exit sensor; the \"Mini Bottom Arrow\" insert marks the exit and has no distinct lamp object of its own; see lamp 71."),
}
LAMP_PROJECTED_ADDRESSES = frozenset(LAMP_PROJECTIONS)
# Coordinate for each projected lamp's target object (see LAMP_PROJECTIONS for the citation).
LAMP_PROJECTION_POSITIONS = {
	71: (0.116786, 0.093645),  # switch 65 (Mini Top Left)
	72: (0.211864, 0.094018),  # switch 75 (Mini Top Right)
	73: (0.105965, 0.176222),  # switch 66 (Mini Middle Top Left)
	74: (0.223033, 0.177296),  # switch 76 (Mini Middle Top Right)
	75: (0.163837, 0.058434),  # Trigger EnterPoA
	81: (0.116792, 0.255833),  # switch 67 (Mini Middle Bottom Left)
	82: (0.212619, 0.255002),  # switch 77 (Mini Middle Bottom Right)
	83: (0.105997, 0.338951),  # switch 68 (Mini Bottom Left)
	84: (0.222763, 0.339082),  # switch 78 (Mini Bottom Right)
	85: (0.116309, 0.444351),  # Trigger ExitPoA
}

GI_STRINGS = {
	0: ("Top Playfield", "J121-1", "Q18", "J121-7", "#44"),
	1: ("Bottom Playfield", "J121-2", "Q10", "J121-8", "#44"),
	2: ("Insert Top", "J120-3", "Q14", "J120-9", "#555"),
	3: ("Insert Bottom", "J120-4", "Q16", "J120-10", "#555"),
	4: ("Return Lane/Coin", "J121-6 and J119-3", "Q12", "J121-11 and J119-1", "#44"),
}
# GI address 0 = retained script collections GITop (28 gi0NN Light objects) union GIBumpers (6
# jet-bumper-cap Light objects l1/l2/l3/l3b/l3b1/l3b2). GI address 1 = collection GiBot (32
# gi0NN Light objects). Every coordinate below is that object's own retained-table center;
# gi060/gi061 exist in the table but belong to no active collection (GiTopSides/GiBotSides are
# both declared empty) and are excluded.
GI_POSITIONS = {
	0: [
		(0.089637, 0.065337), (0.424430, 0.337427), (0.929839, 0.036519), (0.929318, 0.036306),
		(0.089115, 0.065124), (0.297345, 0.112708), (0.296824, 0.112495), (0.390462, 0.100865),
		(0.389941, 0.100652), (0.481822, 0.090503), (0.481301, 0.090290), (0.573769, 0.078068),
		(0.573248, 0.077855), (0.666886, 0.073035), (0.666365, 0.072822), (0.850192, 0.129584),
		(0.849671, 0.129371), (0.892358, 0.142316), (0.891837, 0.142102), (0.875960, 0.201530),
		(0.875439, 0.201317), (0.797484, 0.224624), (0.796963, 0.224411), (0.844336, 0.266074),
		(0.843815, 0.265861), (0.423908, 0.337214), (0.162691, 0.092537), (0.163514, 0.256810),
		(0.573804, 0.170915), (0.390371, 0.194213), (0.519963, 0.259640), (0.519107, 0.260650),
		(0.572947, 0.171924), (0.389514, 0.195633),
	],
	1: [
		(0.217382, 0.696177), (0.190103, 0.796768), (0.189582, 0.797377), (0.246800, 0.816777),
		(0.246279, 0.817387), (0.216861, 0.696786), (0.244139, 0.760331), (0.244661, 0.759722),
		(0.041211, 0.721877), (0.040690, 0.721664), (0.055474, 0.588877), (0.087088, 0.439284),
		(0.086567, 0.439071), (0.094460, 0.542087), (0.093939, 0.541874), (0.054953, 0.588664),
		(0.840640, 0.580561), (0.669426, 0.818650), (0.668905, 0.818437), (0.727124, 0.798384),
		(0.726602, 0.798171), (0.659236, 0.760969), (0.658715, 0.760756), (0.697475, 0.699256),
		(0.696954, 0.699043), (0.840119, 0.580348), (0.884965, 0.504800), (0.884443, 0.504587),
		(0.648114, 0.735533), (0.255312, 0.733066), (0.108112, 0.499538), (0.935193, 0.214308),
	],
	4: [(0.170824, 0.676908), (0.742613, 0.672384)],
}
GI_PLAYFIELD_QUANTITY = {0: 34, 1: 32}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Indiana Jones retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Indiana Jones extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Indiana Jones retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Indiana Jones retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Indiana Jones retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the ij_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/ij.c ijGameData GEN_WPCDCS with wpc_dispDMD, hw={FLIP_SW(FLIP_L)|FLIP_SOL(FLIP_L), "
				"swCol=1, lampCol=0, custSol=7}, the inverted-switch mask {0x00,0x00,0x00,0x00,0x5F,0x00,0x00,0x06,0x7F,"
				"0x00,0x00,0x70,0x18}, swSDropTop..swShooter/swCLDrop../swLRampMade/swIdolPos1../swLL_PoA/swRL_PoA defines, "
				"sBallPopper..sSubwayRelease/sDivPower../sTopPostHold defines, ij_getSol reading WPC_EXTBOARD1 bits for "
				"CORE_CUSTSOLNO(1..8), ij_handleMech (mech bit 0x01 center-drop-bank reset, 0x02 Totem drop up/down, 0x04 "
				"Path of Adventure PoAPos 0-359 with swLL_PoA/swRL_PoA thresholds at 176/184, 0x08 idol motor 0-359 in "
				"IJ_IDOLTICK=2 steps bucketed into six 60-degree sextants toggling swIdolPos1-3), and "
				"comSw={swStart,swTilt,swSlamTilt,swCoinDoor,swGunTrigger}; src/wpc/core.h CORE_COINDOORSWCOL=0, "
				"CORE_FLIPPERSWCOL=11, CORE_STDSWCOLS=12, CORE_CUSTSWCOL=12, CORE_CUSTSWNO(c,r)=((11+c)*10+r), "
				"CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, CORE_FIRSTCUSTSOL=51; src/wpc/gen.h GEN_WPCDCS; src/wpc/wpc.c "
				"GENWPC_HASFLIPTRON, WPC_FLIPPERS unconditional complement, wpc_sw2m/wpc_m2sw=col*10+row+1; src/wpc/core.c "
				"core_getSol full dispatch; src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCDCS=0x10"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-dcs.json",
			"revision": "repository",
			"locator": "WPC-DCS public switch, DIP, solenoid, lamp, and five-GI address rules derived from pinned PinMAME source",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.indiana-jones-the-pinball-adventure-1993/archive-arcademanual_Indiana_Jones_OPS/Indiana_Jones_OPS.pdf",
			"original_filename": "Indiana_Jones_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"152-page image-only scan of the Williams Indiana Jones: The Pinball Adventure operations manual "
				"(Internet Archive item arcademanual_Indiana_Jones_OPS, part number 16-50017-101, July 1993). Printed "
				"pages 2-46 through 2-51 carry the switch/lamp/solenoid matrix, location, and wiring tables; printed "
				"pages 3-20, 3-22/3-23, and 3-24 carry the 3-sw Opto (idol), 8-Driver, and Motor Opto Switch (mini "
				"playfield) board schematics that fix the custom switch-column and custom-solenoid physical construction."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.indiana-jones.switch-matrix",
					"locator": "PDF page 110, printed 2-46, Switch Matrix",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/switch-matrix.md",
					"sha256": "d47e4a344e980a7dd2d4fb5316c3e0fba351f0faa1aaf38bff2f77c0175a5a72",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.indiana-jones.switch-locations",
					"locator": "PDF page 111, printed 2-47, Switch Locations parts list plus custom switch column",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/switch-locations.md",
					"sha256": "4d6e096e0a2d461d54c23a3c3f0f6d52dbb6216cf7918e7e13168e44a31457c7",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.indiana-jones.solenoid-flasher-wiring",
					"locator": "PDF page 114, printed 2-50, Solenoid/Flasher Table and Flipper Circuits",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/solenoid-flasher-wiring.md",
					"sha256": "999d00a8cc7a8d596235eecafe6be42799ccb1669cf071f7cad29f734df99afd",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.indiana-jones.general-illumination",
					"locator": "PDF page 114, printed 2-50, General Illumination",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/general-illumination.md",
					"sha256": "24239e9145aed7698b37a145d917b44054d0e027eb4db6b90559535aadafedb4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.indiana-jones.lamp-matrix-and-locations",
					"locator": "PDF pages 112-113, printed 2-48/2-49, Lamp Matrix and Lamp Locations",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/lamp-matrix-and-locations.md",
					"sha256": "600683138b2f8f9d168fa2395d4d707393485f7e246b009c715ec769fe850516",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.indiana-jones.board-assemblies",
					"locator": "PDF pages 136, 138-139, 140, printed 3-20, 3-22/3-23, 3-24, board identification",
					"path": "evidence/excerpts/williams.indiana-jones-the-pinball-adventure.1993/board-assemblies.md",
					"sha256": "f395e1e8e2ac92ad0bccca9f816a26f6144528e399e302731d1282eda42d9b5a",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/indiana-jones-the-pinball-adventure-1993/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, together with the "
				"rendered PNG page cache under external:pinmame-manuals/rendered/williams.indiana-jones-the-pinball-"
				"adventure.1993/. pdftotext yields ~512KB of scrambled/duplicated OCR text from the Paper Capture layer, "
				"so this transcription is the source of record and the OCR text is never an authority."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/indiana-jones-the-pinball-adventure-1993/source/Indiana%20Jones%20The%20Pinball%20Adventure%20%28Williams%201993%29%20VPWmod%20v1.0.vpx",
			"original_filename": "Indiana Jones The Pinball Adventure (Williams 1993) VPWmod v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW Mod v1.0 recreation of the physical machine (table_version \"1.0\", "
				"table_description citing IPDB No. 1267 and the \"Widebody 'Superpin' Line\"). Exact playfield bounds "
				f"are {TABLE_BOUNDS}; normalized coordinates are x/1093 and y/2162 because this is a wide-body table. "
				"Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script. Runtime and mechanism-causality authority: cGameName = "ij_l7", Const '
				"UseSolenoids = 2 (fast flips), Const HandleMech = 0, the SolCallback/SolModCallback table for solenoids "
				"1-28, 33-36, 45-56 (including the definitive Right/Left Slingshot binding at 12/13 and the printed-"
				"37..42-to-public-51..56 custom solenoid mapping), the cvpmTrough/cvpmSaucer/cvpmMech constructions for "
				"the ball trough, left eject, subway, popper, idol lock, and Path of Adventure mechanisms, and the "
				"UpdateIdol_timer/ResetPoA_timer mechanism-position handlers."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool.manifest.json",
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
				"optional" if address == 4 else "used",
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
			label = SWITCH_LABELS[address]
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
			if address == 23:
				notes += (
					" The printed switch matrix (2-46) labels this position \"Ticket Opto\" and pinned PinMAME's ij.c "
					"independently defines #define swTicketOpto 23, but the printed Switch Locations parts list (2-47) "
					"prints item 23 blank with no switch or opto part number, and the swTicketOpto constant is never "
					"referenced anywhere else in the driver (no state, mechanism, or inport table entry uses it). The "
					"blank parts-list entry is the physical-fitment authority: no device is installed at this position "
					"on this machine, and \"Ticket Opto\" is a vestigial template label."
				)
			elif address in OPTO_SWITCHES:
				assembly_text = assembly or "its opto assembly"
				notes += f" Opto interrupter per {assembly_text} on the printed Switch Locations page (2-47)."
				if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
					notes += (
						" Pinned PinMAME's ijGameData inverted-switch mask normalizes this address, so the public switch "
						"state is already normalized and must not be inverted again."
					)
				else:
					notes += (
						" Pinned PinMAME's ijGameData inverted-switch mask does NOT cover this address even though it is "
						"printed opto construction; see the corresponding unresolved conflicts entry."
					)
			if address == 24:
				notes += " Physical part 5643-09288-00 is a permanently closed link used to prove the matrix is connected."
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
			if address == 23:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE)
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
				if address in {12, 13, 14, 21, 22, 34}:
					role = {
						12: "cabinet.buy-in",
						13: "cabinet.start",
						14: "cabinet.tilt",
						21: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
						34: "cabinet.launch",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {12, 13, 34} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				elif address == 81:
					extra["spatial"] = located(identifier, "sensor", [TROUGH_ANCHOR], VPX_TABLE_SOURCE, MANUAL_SOURCE)
				elif address in range(82, 88):
					extra["spatial"] = located(identifier, "sensor", [TROUGH_ANCHOR], VPX_TABLE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
				else:
					coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SWITCH_PROJECTIONS else (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	for address in list(CUSTOM_SWITCH_LABELS) + list(CUSTOM_SWITCH_UNUSED):
		if address in CUSTOM_SWITCH_LABELS:
			label = CUSTOM_SWITCH_LABELS[address]
			identifier = f"switch.custom-{address}"
			manual_alias = CUSTOM_SWITCH_MANUAL_ALIAS[address]
			assembly, _ = SWITCH_PARTS[address]
			physical = {
				"assembly_part_number": assembly,
				"switch_type": "opto",
				"notes": (
					f"Custom switch column (declared by ijGameData hw.swCol=1), internal array index 12, public address "
					f"{address}. Printed on the schematic as switch column 9 position {manual_alias} (captured as a "
					"manual.address alias). Opto interrupter per the 3-sw Opto PCB Assembly (idol) or Motor Opto Switch "
					"PCB Assembly (mini playfield); see manual-transcription.md 'Custom switch column'."
				),
			}
			if address in PINMAME_NORMALIZED_OPTO_SWITCHES:
				physical["notes"] += (
					" Pinned PinMAME's ijGameData inverted-switch mask (column index 12, 0x18) normalizes this address."
				)
			else:
				physical["notes"] += (
					" Pinned PinMAME's ijGameData inverted-switch mask (column index 12, 0x18) does NOT cover this "
					"address even though it is printed opto construction; see the corresponding unresolved conflicts "
					"entry."
				)
			items.append(
				_device(
					identifier,
					label,
					"switch",
					"pinmame.input.switch",
					address,
					"used",
					(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE),
					aliases=[
						{"namespace": "pinmame.switch", "value": str(address)},
						{"namespace": "manual.address", "value": manual_alias},
					],
					normally_closed=True,
					physical=physical,
					wiring={
						"board": "3-sw. Opto PCB (idol) / Motor Opto Switch PCB (mini playfield)",
						"drive_wire": "Violet-White",
						"drive_connection": "8-Driver PCB J5-4",
						"return_component": "CPU board J209 rows 1-5",
					},
					spatial=located(
						identifier,
						"sensor",
						[IDOL_FIGURE_ANCHOR if address in (121, 122, 123) else MINI_PLAYFIELD_ANCHOR],
						VPX_TABLE_SOURCE,
						MANUAL_SOURCE,
						VPX_SCRIPT_SOURCE,
					),
				)
			)
		else:
			items.append(
				_device(
					f"switch.custom-{address}",
					f"Unused Custom Switch Column Position {address}",
					"switch",
					"pinmame.input.switch",
					address,
					"unused",
					(MANUAL_SOURCE, CORE_SOURCE),
					aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
					physical={
						"notes": (
							"Custom switch column, internal array index 12. Both the 3-sw Opto PCB Assembly (idol, "
							"connectors J5-J7 explicitly marked \"Not Used\" on its own schematic) and the Motor Opto "
							"Switch PCB Assembly (mini playfield, two-opto board) leave this row position unpopulated; "
							"ijGameData declares only hw.swCol=1 with no driver reference to this address."
						),
					},
					spatial=not_applicable("unused", MANUAL_SOURCE, CORE_SOURCE),
				)
			)

	for address, (label, role, opto, switch_type, part_number, assembly) in FLIPPER_LABELS.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if address in (115, 116, 117):
			notes += (
				" Footnoted \"*Used as switches other than flipper switches in this game\" on the printed matrix page: "
				"this position is one of the three Center Drop Bank opto sensors (A-13609, \"3-bank Opto Drop Target\" "
				"per the Section 3 TOC), not an upper-flipper position. ijGameData declares only FLIP_SW(FLIP_L) (no "
				"FLIP_U), and pinned PinMAME's core_getSol falls back to the generic solenoids2-bit path for 33-36 "
				"because this driver never sets FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) either."
			)
		elif address == 118:
			notes += (
				" Footnoted \"*Used as switches other than flipper switches in this game\": this position is the Left "
				"Ramp Made sensor, not an upper-flipper position."
			)
		elif switch_type == "opto":
			notes += " Opto per the Flipper Opto PCB Assembly (A-16384-1, per the Section 3 TOC)."
		physical["notes"] = notes
		normally_closed = opto
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
			"normally_closed": normally_closed,
			"wiring": {"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
		}
		if address in (115, 116, 117):
			extra["spatial"] = located(f"switch.generic-{address}", "sensor", [(
				{115: 0.416079, 116: 0.465217, 117: 0.514394}[address],
				{115: 0.366854, 116: 0.378773, 117: 0.390578}[address],
			)], VPX_TABLE_SOURCE)
		elif address == 118:
			extra["spatial"] = located(f"switch.generic-{address}", "sensor", [(0.453563, 0.147677)], VPX_TABLE_SOURCE)
		else:
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
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				**extra,
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
					"location": "WPC CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC CPU-board country/option configuration DIP bank. The retained transcription of this manual "
						"includes the Country DIP Switch Chart (American/European/French/German/Spanish, SW4-SW8) but not "
						"a bit-by-bit function map, so no specific ON/OFF combination is asserted here beyond the country "
						"table."
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
	fitted_addresses = sorted(SOLENOID_LABELS)
	for address in range(1, 59):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			if 17 <= address <= 21 or 51 <= address <= 55 or address in (24, 25, 26, 27):
				kind = "flasher"
			elif address in (22, 23, 56):
				kind = "motor"
			else:
				kind = "coil"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			manual_number = MANUAL_SOLENOID_ALIASES.get(address, f"{address:02d}")
			notes = f"Printed solenoid/flasher table entry {manual_number} ({printed_type})."
			if kind == "flasher" and address in FLASHER_BULBS:
				bulbs, quantity = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in (12, 13):
				matching_switch = 48 if address == 12 else 33
				notes += (
					f" The printed Solenoid/Flasher Table (2-50) transposes 12/13: it labels {address} "
					f"\"{'Left' if address == 12 else 'Right'} Slingshot\", the opposite of this binding. The retained "
					"known-working script (SolCallback(12)=\"RandomSoundSlingshotRight\", SolCallback(13)="
					"\"RandomSoundSlingshotLeft\") and pinned PinMAME's own ij.c (#define sRSling 12, #define sLSling "
					"13) independently agree with each other and with the undisputed switch-side labels (switch 33 = "
					"Left Slingshot = swLSling, switch 48 = Right Slingshot = swRSling), and the retained table's own "
					f"Left/RightSlingShot wall objects sit on the geometrically correct side for switch {matching_switch}. "
					"Resolved in favor of the script+driver majority; the manual's transposed row is disclosed rather "
					"than silently corrected."
				)
			if address in (33, 34):
				notes += " Right-ramp diverter (Diverter Power/Hold); repurposes the printed upper-right-flipper circuit position because this machine has no upper-right flipper."
			if address in (35, 36):
				notes += " Top Lockup post (Top Lockup Power/Hold), sensed by switch 46 (Top Post); repurposes the printed upper-left-flipper circuit position because this machine has no upper-left flipper."
			if address in (45, 46, 47, 48):
				notes += " PinMAME's public lower-flipper addresses are 45-48 while the printed table numbers the same circuits 29-32; the manual number is preserved as an alias."
			if 51 <= address <= 56:
				notes += (
					f" Printed on the 8-Driver PCB (controlled from the 8-Driver Board, not the Power Driver Board); the "
					f"printed item number {manual_number} is the board's own silkscreen, not the public address -- see "
					"manual-transcription.md 'Custom solenoid mapping'."
				)
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "8-Driver PCB" if 51 <= address <= 56 else "WPC power driver board", "driver_transistor": wiring_data["driver_transistor"]}
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			if "control_wire" in wiring_data:
				wiring["control_wire"] = wiring_data["control_wire"]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
			if address in MANUAL_SOLENOID_ALIASES:
				aliases.append({"namespace": "manual.address", "value": MANUAL_SOLENOID_ALIASES[address]})
			else:
				aliases.append({"namespace": "manual.address", "value": f"{address:02d}"})
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			availability = "used"
			role_map = {
				7: ["cabinet.knocker"],
			}
			if address in role_map:
				extra["roles"] = role_map[address]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address == 1:
				extra["spatial"] = located(identifier, "effect", [(0.885800, 0.420444)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 2:
				extra["spatial"] = located(identifier, "effect", [(0.946773, 0.992130)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address in (3, 16):
				extra["spatial"] = located(identifier, "effect", [(0.714280, 0.143273)], VPX_TABLE_SOURCE)
			elif address == 4:
				extra["spatial"] = located(identifier, "effect", [TROUGH_ANCHOR], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 5:
				extra["spatial"] = located(identifier, "effect", [(0.465217, 0.378773)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 6:
				extra["spatial"] = located(identifier, "effect", [(0.886713, 0.535677)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 8:
				extra["spatial"] = located(identifier, "effect", [(0.218935, 0.334221)], VPX_TABLE_SOURCE)
			elif address == 9:
				extra["spatial"] = located(identifier, "effect", [(0.388764, 0.195046)], VPX_TABLE_SOURCE)
			elif address == 10:
				extra["spatial"] = located(identifier, "effect", [(0.573051, 0.171427)], VPX_TABLE_SOURCE)
			elif address == 11:
				extra["spatial"] = located(identifier, "effect", [(0.519479, 0.260665)], VPX_TABLE_SOURCE)
			elif address == 12:
				extra["spatial"] = located(identifier, "effect", [(0.659250, 0.725416)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 13:
				extra["spatial"] = located(identifier, "effect", [(0.254015, 0.727135)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 14:
				extra["spatial"] = located(identifier, "effect", [(0.302468, 0.035847)], VPX_TABLE_SOURCE)
			elif address == 15:
				extra["spatial"] = located(identifier, "effect", [(0.651618, 0.028462)], VPX_TABLE_SOURCE)
			elif address in FLASHER_POSITIONS:
				role = "emitter"
				extra["spatial"] = located(identifier, role, FLASHER_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address in (22, 23):
				extra["spatial"] = located(identifier, "effect", [MINI_PLAYFIELD_ANCHOR], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address == 28:
				extra["spatial"] = located(identifier, "effect", [(0.819061, 0.419203)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address in (33, 34):
				extra["spatial"] = located(identifier, "effect", [(0.789570, 0.083719)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address in (35, 36):
				extra["spatial"] = located(identifier, "effect", [(0.212015, 0.032900)], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			elif address in (45, 46):
				extra["spatial"] = located(identifier, "effect", [(0.601620, 0.842276)], VPX_TABLE_SOURCE)
			elif address in (47, 48):
				extra["spatial"] = located(identifier, "effect", [(0.312707, 0.842276)], VPX_TABLE_SOURCE)
			elif address == 56:
				extra["spatial"] = located(identifier, "effect", [IDOL_FIGURE_ANCHOR], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				raise RuntimeError(f"Indiana Jones solenoid {address} has no spatial disposition")
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 32} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not an Indiana Jones playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not an Indiana Jones playfield device.",
			31: "PinMAME's synthetic game-on state, taken from the driver's fast-flip RAM flag.",
			32: "PinMAME reports this WPC state channel as always zero.",
			37: "WPC-DCS has no integrated LPDC board (unlike WPC-95/WPC-95DCS); pinned PinMAME's core_getSol dispatch returns constant 0 for 37-44 on this generation, and ijGameData claims no other use of this address.",
			38: "Unused WPC-DCS address; see 37.",
			39: "Unused WPC-DCS address; see 37.",
			40: "Unused WPC-DCS address; see 37.",
			41: "Unused WPC-DCS address; see 37.",
			42: "Unused WPC-DCS address; see 37.",
			43: "Unused WPC-DCS address; see 37.",
			44: "Unused WPC-DCS address; see 37.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-DCS hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. ijGameData declares custSol=7, starting at public 51.",
			57: "Seventh of the seven custom solenoids ijGameData declares (custSol=7, CORE_CUSTSOLNO(7)=57); no printed function and no retained script binding.",
			58: "Eighth possible custom-solenoid position that ij_getSol's range check (CORE_CUSTSOLNO(8)=58) admits, one beyond the declared custSol=7 count; no printed function and no retained script binding.",
		}[address]
		roles = ["internal.unused.wpc-output"]
		if address in {29, 30, 31, 32}:
			roles = ["internal.wpc-state"]
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
	assert set(SOLENOID_LABELS) == set(fitted_addresses)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly = LAMP_ASSEMBLIES[address]
			bulb = LAMP_BULB_TYPES.get(address, "#555")
			physical: dict[str, Any] = {"quantity": 1, "assembly_part_number": assembly}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}. Printed bulb type {bulb}."
			if address in LAMP_MATRIX_PAGE_TYPOS:
				notes += (
					f' The lamp-matrix page (2-48) prints this insert as "{LAMP_MATRIX_PAGE_TYPOS[address]}"; the '
					"lamp-locations parts list (2-49) label used here is taken as authoritative."
				)
			if address in {87, 88}:
				notes += " Cabinet button/insert lamp; 88 shares the illuminated Start Button assembly with switch 13."
			if address in LAMP_PROJECTED_ADDRESSES:
				_, projection_note = LAMP_PROJECTIONS[address]
				notes += " " + projection_note
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
			if address == 88:
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in LAMP_PROJECTED_ADDRESSES:
				extra["spatial"] = located(identifier, "emitter", [LAMP_PROJECTION_POSITIONS[address]], VPX_TABLE_SOURCE, MANUAL_SOURCE)
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
					(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
					**extra,
				)
			)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
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
		if address in GI_PLAYFIELD_QUANTITY:
			quantity = GI_PLAYFIELD_QUANTITY[address]
			physical["quantity"] = quantity
			collection = "GITop plus GIBumpers" if address == 0 else "GiBot"
			notes += (
				f" The manual prints no per-string bulb count, so the physical quantity ({quantity}) and every emitter "
				f"coordinate come from the retained table's {collection} emitter collection(s) (script UpdateGi/"
				"ModLampz dispatch). Two further Light objects (gi060, gi061) exist in the table but belong to no "
				"active collection (GiTopSides/GiBotSides are both declared empty) and are excluded as orphaned "
				"table-modeling objects rather than distinct physical bulbs."
			)
			extra["spatial"] = located(identifier, "emitter", GI_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 4:
			quantity = 2
			physical["quantity"] = quantity
			notes += (
				" The manual prints no per-string bulb count. The retained script's ModLampz dispatch assigns "
				"collection GiRLaneCoin (LiteHOF_L, LiteHOF_R) to this address, plus a cabinet feed through J119 (the "
				"only cabinet connection on the printed general-illumination wiring page). LiteHOF_La/LiteHOF_Ra are "
				"co-located brightness-doubling duplicates of L/R and are excluded, leaving 2 playfield placements."
			)
			extra["spatial"] = located(identifier, "emitter", GI_POSITIONS[4], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			notes += (
				" Backbox insert-panel illumination behind the translite; the retained script's ModLampz dispatch "
				"assigns no playfield collection to this address (only 0, 1, and 4 are wired)."
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
			"mechanism.trough",
			"Six-ball trough and ball release",
			"kicker",
			[output_id("Ball Release")],
			["switch.matrix-81", "switch.matrix-82", "switch.matrix-83", "switch.matrix-84", "switch.matrix-85", "switch.matrix-86", "switch.matrix-87"],
			"Six balls rest on trough optos 86 (nearest the drain entrance) through 81 (nearest the eject end); "
			"cvpmTrough.InitSwitches Array(86,85,84,83,82,81) and .InitExit BallRelease,70,15. Solenoid 4 (Ball "
			"Release) ejects the ball resting on 81 toward the shooter lane; the retained script's SolBallRelease "
			"handler pulses Top Trough opto 87 in the same event whenever bsTrough.Balls is nonzero "
			"(relationship.ball-release-top-trough-pulse). All seven positions are printed optos that rest closed "
			"(inverted-switch mask column 8, 0x7F), so a recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough Ball (drain entrance)", ["switch.matrix-86"], "Ball nearest the drain entrance."),
				("ball-2", "Trough Ball", ["switch.matrix-85"], "Second trough position."),
				("ball-3", "Trough Ball", ["switch.matrix-84"], "Third trough position."),
				("ball-4", "Trough Ball", ["switch.matrix-83"], "Fourth trough position."),
				("ball-5", "Trough Ball", ["switch.matrix-82"], "Fifth trough position."),
				("ball-6", "Trough Ball (eject position)", ["switch.matrix-81"], "Ball nearest the Ball Release coil."),
				("top", "Top Trough", ["switch.matrix-87"], "Opto pulsed as the released ball leaves toward the shooter lane."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16765",
		),
		mechanism(
			"mechanism.gun-launcher",
			"Gun Handle auto-launcher",
			"kicker",
			[output_id("Ball Launch")],
			["switch.matrix-88", "switch.matrix-34"],
			"Indiana Jones has no manual plunger knob; the player instead pulls a spring-loaded Gun Handle trigger "
			"mounted on the front of the cabinet (A-16113 Gun Handle Assembly, printed page 2-20). ijGameData's "
			"comSw declares swGunTrigger (34) as the shooter switch. The ball rests on Shooter switch 88 in the "
			"shooter lane; pulling the trigger closes switch 34, and the retained script's AutoPlunger handler fires "
			"the physical Plunger object (solenoid 2, Ball Launch) to auto-plunge the ball -- a powered launcher "
			"rather than a player-driven mechanical plunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-88"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16113",
		),
		mechanism(
			"mechanism.left-eject",
			"Left eject hole",
			"kicker",
			[output_id("Left Eject")],
			["switch.matrix-31"],
			"A ball resting on switch 31 (Left Eject) is kicked back to the playfield by solenoid 8; the retained "
			"script's cvpmSaucer bsLEject construction (.InitKicker Sw31,31,160,17,0) confirms the kicker angle.",
			[("held", "Ball in the left eject hole", ["switch.matrix-31"], "Left eject switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-17073",
		),
		mechanism(
			"mechanism.subway-idol-entry",
			"Center hole, subway, and idol-popper entry chain",
			"kicker",
			[output_id("Subway Release"), output_id("Ball Popper")],
			["switch.matrix-45", "switch.matrix-47", "switch.matrix-44", "switch.matrix-43"],
			"A ball entering the Center hole (switch 45, opto) rolls down the subway and rests on Subway Lockup "
			"opto 47; solenoid 28 (Subway Release, cvpmSaucer bsSubway) ejects it onto Right Popper opto 44, where "
			"solenoid 1 (Ball Popper, cvpmSaucer bsPopper) pops it up into the idol entry, sensed a final time by "
			"Top Idol Enter opto 43 before it reaches the rotating idol lock (mechanism.idol).",
			[
				("center", "Center hole", ["switch.matrix-45"], "Ball drops into the subway."),
				("subway", "Subway lockup", ["switch.matrix-47"], "Ball held before the Subway Release kick."),
				("popper", "Right popper", ["switch.matrix-44"], "Ball held before the Ball Popper kick."),
				("idol-enter", "Top idol enter", ["switch.matrix-43"], "Ball crosses into the idol lock mechanism."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.idol",
			"Rotating idol figure and ball lock",
			"rotary",
			[output_id("Idol Release"), output_id("Wheel Motor")],
			["switch.custom-121", "switch.custom-122", "switch.custom-123", "switch.matrix-32"],
			"A DC gearmotor (solenoid 56, Wheel Motor, controlled from the 8-Driver Board) rotates the idol figure "
			"(Primitive totem) continuously; the retained script's UpdateIdol_timer advances a 0-359 degree counter "
			"in IJ_IDOLTICK=2-degree ticks and bucket-decodes it into six 60-degree sextants, toggling "
			"Controller.Switch(121/122/123) at each 60-degree boundary (case 0/60/120/180/240/300) so that three "
			"opto sensors (A-13901-2 3-sw Opto PCB) report which of six lock pockets is presented at the entry/exit "
			"point. Pinned PinMAME's own ij_handleMech mech-bit-0x08 branch implements the identical six-case "
			"toggle table independently. Balls enter via Top Idol Enter (switch 43, see "
			"mechanism.subway-idol-entry) into the rotating lock (cvpmTrough bsIdol, size 3, "
			".InitExit IdolExit,180,0); solenoid 6 (Idol Release) opens the lock doors and ejects a held ball, "
			"sensed leaving on Exit Idol (switch 32).",
			[
				("position-1", "Idol lock pocket 1", ["switch.custom-121"], "Sextant 300-359 degrees / 0-59 degrees per the toggle table."),
				("position-2", "Idol lock pocket 2", ["switch.custom-122"], "Sextant boundary at 180 degrees."),
				("position-3", "Idol lock pocket 3", ["switch.custom-123"], "Sextant boundary at 60 degrees."),
				("exit", "Idol exit", ["switch.matrix-32"], "Ball leaves the lock after solenoid 6 opens the doors."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16228",
		),
		mechanism(
			"mechanism.right-ramp-diverter",
			"Right-ramp diverter",
			"diverter",
			[output_id("Diverter Power"), output_id("Diverter Hold")],
			[],
			"Solenoids 33/34 (Diverter Power/Hold, repurposing the printed upper-right-flipper circuit position) "
			"rotate a diverter flap (Primitive DiverterP) near the right ramp entrance. The retained script's own "
			"state table pulses Diverter Hold (sDivHold) as a ball crosses Right Ramp Enter (switch 42) and "
			"transitions toward the Rope Bridge/Path of Adventure entrance, so the diverter routes a ball either up "
			"the right ramp proper or across to the Path of Adventure feature depending on its hold state. There is "
			"no dedicated diverter-position sensor; its state is inferred from solenoid drive only.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16301",
		),
		mechanism(
			"mechanism.top-lockup-post",
			"Top Lockup post",
			"gate",
			[output_id("Top Lockup Power"), output_id("Top Lockup Hold")],
			["switch.matrix-46"],
			"Solenoids 35/36 (Top Lockup Power/Hold, repurposing the printed upper-left-flipper circuit position) "
			"raise and hold a post (sTopPostPower/sTopPostHold) sensed by Top Post switch 46. The post sits at the "
			"entrance to the Path of Adventure mini-playfield; the retained script's state table raises it on entry "
			"and holds it to route a ball across the Rope Bridge toward the Path of Adventure (see "
			"mechanism.path-of-adventure) rather than continuing along the main playfield.",
			[("post-up", "Top Lockup post raised", ["switch.matrix-46"], "Post-position sense switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-16656",
		),
		mechanism(
			"mechanism.path-of-adventure",
			"Path of Adventure tilting mini-playfield",
			"motorized",
			[output_id("Mini Motor Left"), output_id("Mini Motor Right")],
			[
				"switch.matrix-65", "switch.matrix-66", "switch.matrix-67", "switch.matrix-68",
				"switch.matrix-75", "switch.matrix-76", "switch.matrix-77", "switch.matrix-78",
				"switch.matrix-72", "switch.matrix-73", "switch.custom-124", "switch.custom-125",
			],
			"A small secondary playfield (Primitive minipf, the retained script's own \"mini playfield\") is "
			"mounted on a motorized tilt mechanism driven by solenoids 22/23 (Mini Motor Left/Right, an H-bridge "
			"pair). The retained script's POAMech (vpmMechTwoDirSol + vpmMechStopEnd + vpmMechLinear, Sol1=23, "
			"Sol2=22, Length=9, Steps=9) advances a 0-8 linear position counter; pinned PinMAME's ij_handleMech "
			"mech-bit-0x04 branch independently implements the same idea with its own 0-359 PoAPos counter and "
			"176/184-degree thresholds around a 180-degree center (IJ_POA_LLIMIT/IJ_POA_MIDPOS/IJ_POA_RLIMIT). A "
			"ball enters through the Top Post/Rope Bridge diverter at the top of the mini-playfield and rolls down "
			"whichever of two forked lanes the tilt favors, passing four switches per lane (top, middle-top, "
			"middle-bottom, bottom: 65/66/67/68 left, 75/76/77/78 right) before reaching a Pit Hole (72) or Extra "
			"Ball Hole (73) at the bottom center. Mini Playfield Left/Right Limit optos (124/125) mark the two tilt "
			"extremes.",
			[
				("left-top", "Mini Top Left", ["switch.matrix-65"], "Left lane, first switch."),
				("left-mid-top", "Mini Middle Top Left", ["switch.matrix-66"], "Left lane, second switch."),
				("left-mid-bottom", "Mini Middle Bottom Left", ["switch.matrix-67"], "Left lane, third switch."),
				("left-bottom", "Mini Bottom Left", ["switch.matrix-68"], "Left lane, fourth switch."),
				("right-top", "Mini Top Right", ["switch.matrix-75"], "Right lane, first switch."),
				("right-mid-top", "Mini Middle Top Right", ["switch.matrix-76"], "Right lane, second switch."),
				("right-mid-bottom", "Mini Middle Bottom Right", ["switch.matrix-77"], "Right lane, third switch."),
				("right-bottom", "Mini Bottom Right", ["switch.matrix-78"], "Right lane, fourth switch."),
				("pit", "Path of Adventure pit hole", ["switch.matrix-72"], "Bottom-center pit hole."),
				("extra-ball", "Path of Adventure extra-ball hole", ["switch.matrix-73"], "Bottom-center extra-ball hole."),
				("left-limit", "Tilt left limit", ["switch.custom-124"], "Motor position counter step 0."),
				("right-limit", "Tilt right limit", ["switch.custom-125"], "Motor position counter step 8."),
			],
			VPX_SCRIPT_SOURCE, CORE_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16738",
		),
		mechanism(
			"mechanism.totem-drop-target",
			"Totem single drop target",
			"drop_target_bank",
			[output_id("Totem Drop Up"), output_id("Totem Drop Down")],
			["switch.matrix-11"],
			"A single reciprocating drop target (\"Totem\", switch 11, Single Drop Target) is raised by solenoid 3 "
			"(Totem Drop Up) and knocked back down by solenoid 16 (Totem Drop Down). Pinned PinMAME's ij_handleMech "
			"mech-bit-0x02 branch sets/clears swSDropTop directly from whichever coil is asserted; the retained "
			"script's TotemDropUP/TotemDropDOWN callbacks (DTRaise 11 / equivalent) agree.",
			[("down", "Totem down (hit)", ["switch.matrix-11"], "Target knocked down by a ball hit or solenoid 16.")],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14615",
		),
		mechanism(
			"mechanism.center-drop-bank",
			"Center three-bank drop target",
			"drop_target_bank",
			[output_id("Center Drop Bank")],
			["switch.generic-115", "switch.generic-116", "switch.generic-117"],
			"A three-target opto drop bank (A-16032-2, A-13609 opto sensors) spells three letters of the "
			"\"ADVENTURE\" chase. Solenoid 5 (Center Drop Bank) resets all three targets up in one pulse; the "
			"retained script's ResetDrops handler raises table objects DTRaise 115/116/117 together, and pinned "
			"PinMAME's ij_handleMech mech-bit-0x01 branch clears all three switches together on the same coil, "
			"confirming a single shared reset coil with no separate per-target coil.",
			[
				("left", "Center Drop Bank left", ["switch.generic-115"], "Leftmost of the three opto drop targets."),
				("middle", "Center Drop Bank middle", ["switch.generic-116"], "Middle opto drop target."),
				("right", "Center Drop Bank right", ["switch.generic-117"], "Rightmost opto drop target."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-16032-2",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-33", "switch.matrix-48"],
			"Each slingshot carries a kick switch (SW-1A-114) and a separate scored switch (SW-1A-120) with a diode "
			"attached. The retained script's RandomSoundSlingshotLeft/RandomSoundSlingshotRight handlers pulse "
			"matrix addresses 33/48 and fire coils 13/12 respectively (see the public solenoid address note on "
			"device.left-slingshot / device.right-slingshot for the printed-table transposition this resolves).",
			[
				("left", "Left slingshot", ["switch.matrix-33"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-48"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Bottom Jet Bumper")],
			["switch.matrix-35", "switch.matrix-36", "switch.matrix-37"],
			"Three SW-11A-37 jet bumpers. The retained script's Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit handlers "
			"pulse switches 35, 36, and 37 and fire coils 9, 10, and 11 respectively, matching printed Left/Right/"
			"Bottom Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-35"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-36"], "Right bumper of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-37"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-9415-2",
		),
		mechanism(
			"mechanism.control-gates",
			"Left and right control gates",
			"gate",
			[output_id("Left Control Gate"), output_id("Right Control Gate")],
			[],
			"Two solenoid-operated one-way gates (LeftGate solenoid 14, RightGate solenoid 15) admit a ball into a "
			"loop while blocking return travel; the retained script drives both through the shared vpmSolGate "
			"helper. Neither gate has a dedicated position sensor.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-14422",
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
			"Two Fliptronic flippers. Each flipper has a separate power and hold winding: the ROM energizes the "
			"power winding on the cabinet button opto (112 right, 114 left), then drops to the hold winding once "
			"the end-of-stroke leaf switch (111 right, 113 left) closes. Indiana Jones runs Const UseSolenoids = 2 "
			"fast flips, so the ROM drives the coils directly. There are no upper flippers; the upper-flipper "
			"Fliptronic circuits (33-36, 115-118) are entirely repurposed for other devices (see "
			"mechanism.right-ramp-diverter, mechanism.top-lockup-post, mechanism.center-drop-bank, and the Left Ramp "
			"Made sensor).",
			[
				("right", "Lower right flipper", ["switch.generic-111", "switch.generic-112"], "Button opto 112 and end-of-stroke switch 111."),
				("left", "Lower left flipper", ["switch.generic-113", "switch.generic-114"], "Button opto 114 and end-of-stroke switch 113."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-15205-R-2 right with A-15205-L-2 left",
		),
		mechanism(
			"mechanism.captive-ball",
			"Totem captive ball",
			"toy",
			[],
			["switch.matrix-64", "switch.matrix-71"],
			"A captive ball rolls between two sensors (Captive Ball Back, switch 64; Captive Ball Front, switch 71) "
			"behind the Totem drop target. Pinned PinMAME's ij_handleBallState marks the first simulated ball "
			"IJ_CAPTUREDBALL and routes it through stCapturedIdle/stCapturedF/stCapturedB states rather than the "
			"trough; hitting it while the hitCaptiveBall flag is set (raised when Totem switch 11 registers a hit) "
			"drives the captive ball forward and back rather than draining it. There is no dedicated actuator -- "
			"the ball is hand-pushed by the incoming ball's momentum.",
			[
				("back", "Captive ball at rest", ["switch.matrix-64"], "Captive ball's rest position."),
				("front", "Captive ball struck forward", ["switch.matrix-71"], "Captive ball's forward position after being struck."),
			],
			CORE_SOURCE, MANUAL_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.ball-release-top-trough-pulse",
			"kind": "pulse",
			"source": output_id("Ball Release"),
			"destination": "switch.matrix-87",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.captive-ball-front-opto-not-normalized",
			"path": "inputs[binding.device=71]",
			"description": (
				"The manual's Switch Locations parts list (2-47) documents public switch 71 (Captive Ball Front) as an "
				"opto interrupter -- assembly A-14231 (LED) with A-14232 (phototransistor), the identical part pair "
				"used by the ramp/idol/subway optos 42-45 and 47, all of which pinned PinMAME does normalize. Pinned "
				"PinMAME's ijGameData inverted-switch mask, however, covers column 7 (which carries 71-78) with only "
				"0x06 (binary 00000110): bits 1 and 2 (addresses 72 and 73, Mini Top/Bottom Hole, also opto) are "
				"normalized, but bit 0 (address 71) is not. The manual is physical-construction ground truth and "
				"pinned PinMAME is public-address and emulator-normalization ground truth, and the two disagree on "
				"whether a recreation must invert this one address while its column neighbors are already normalized. "
				"Resolution path: run the implemented LibPinMAME gameplay harness against a legal ij_l7 ROM, strike "
				"the captive ball forward and back, and observe the idle and transition public state of switch 71. "
				"Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.wheel-position-opto-not-normalized",
			"path": "inputs[binding.device=121,122,123]",
			"description": (
				"The manual documents public switches 121-123 (Wheel Position 1-3, printed switch-column-9 positions "
				"91-93) as opto interrupters on the A-13901-2 \"3-sw. Opto PCB Assembly (for idol)\" -- three onboard "
				"LED/phototransistor pairs (OPTO1/OPTO2/OPTO3). Pinned PinMAME's ijGameData inverted-switch mask "
				"covers the custom switch column (index 12) with only 0x18 (binary 00011000): bits 3 and 4 (addresses "
				"124 and 125, Mini Playfield Left/Right Limit, also opto per the A-16657 Motor Opto Switch PCB on the "
				"very same physical column) are normalized, but bits 0-2 (121-123) are not, even though all five "
				"addresses share one physical harness and one opto-sensor technology. The manual is physical-"
				"construction ground truth and pinned PinMAME is public-address and emulator-normalization ground "
				"truth, and the two disagree on whether a recreation must invert the wheel-position trio while the "
				"limit-switch pair on the same column is already normalized. Resolution path: run the implemented "
				"LibPinMAME gameplay harness against a legal ij_l7 ROM, drive the idol motor through a full rotation, "
				"and observe the idle and transition public state of switches 121-123 at each 60-degree boundary. "
				"Unresolved."
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
			"id": "williams.indiana-jones-the-pinball-adventure.1993",
			"name": "Indiana Jones: The Pinball Adventure",
			"manufacturer": "Williams",
			"year": 1993,
			"kind": "physical_pinball",
			"ipdb_id": 1267,
			"model_number": "16-50017-101",
			"playfield": {
				"width": PLAYFIELD_WIDTH,
				"height": PLAYFIELD_HEIGHT,
				"units": "vpx",
				"provenance": provenance(VPX_TABLE_SOURCE),
			},
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
		"knowledge": {"path": "knowledge/williams/indiana-jones-the-pinball-adventure-1993.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Indiana Jones device identifiers are not unique: {duplicates}")
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
		elif spatial["status"] == "validated":
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
			"Public switch 71 (Captive Ball Front) is a printed normally-closed opto interrupter that pinned "
			"PinMAME's ijGameData inverted-switch mask does not normalize, unlike its two column neighbors 72/73 "
			"-- recorded conflict.captive-ball-front-opto-not-normalized, unresolved. This is a polarity conflict, "
			"not a spatial gap; every dimension this report audits is complete and validated.",
			"Public switches 121-123 (Wheel Position 1-3) are printed normally-closed opto interrupters on the same "
			"physical switch column as normalized addresses 124/125, but pinned PinMAME's inverted-switch mask does "
			"not cover them -- recorded conflict.wheel-position-opto-not-normalized, unresolved. Also a polarity "
			"conflict, not a spatial gap.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/1093; 0=left, 1=right (wide-body table)",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool.manifest.json",
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
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		] + [
			{"group": "pinmame.output.lamp", "address": address, "reason": note}
			for address, (_, note) in sorted(LAMP_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.indiana-jones-the-pinball-adventure.1993/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/indiana-jones-the-pinball-adventure-1993/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"LightNNa co-located brightness-doubling Light objects (every matrix lamp)",
			"gi060, gi061 Light objects that are members of no active GI collection (GiTopSides/GiBotSides both declared empty)",
			"LiteHOF_La, LiteHOF_Ra co-located brightness-doubling duplicates of GI address 4's LiteHOF_L/LiteHOF_R",
			"Flasher.FL_LJackpotb, Light.FL_SJackpota/FL_SJackpotb, Light.f54a, Light.FL_JackpotMultib -- secondary render-duplicate objects for flasher addresses the manual prints at quantity 1",
			"PLAYFIELD_GI, PLAYFIELD_LRamp, PLAYFIELD_RRamp, PLAYFIELD_leftside, PLAYFIELD_ruins Flasher objects at the exact table center (0.5, 0.5) -- table-modeling visibility-toggle utility objects, not physical emitters",
		],
		"unresolved": ["conflict.captive-ball-front-opto-not-normalized", "conflict.wheel-position-opto-not-normalized"],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Indiana Jones: The Pinball Adventure (Williams, 1993) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete, but the physical machine "
		"record itself remains `partial` at "
		"`machines/partial/williams/indiana-jones-the-pinball-adventure-1993.json` because of two unresolved "
		"switch-polarity conflicts outside this audit's scope; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Indiana Jones The Pinball Adventure (Williams 1993) "
		f"VPWmod v1.0.vpx` at SHA-256 `{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the "
		f"embedded script at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality "
		f"authority. This is a WIDE-BODY table: exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical "
		"coordinate is x/1093 and y/2162 rounded to at most six fractional places -- not the 952-wide divisor "
		"every other curated WPC game uses.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Williams operations manual "
		"is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- The retained manual PDF has a Paper Capture OCR text layer that scrambles/duplicates table cells under "
		"`pdftotext -layout`. Every printed table used here was read from rendered pages and transcribed into "
		"`external:pinmame-review-artifacts/indiana-jones-the-pinball-adventure-1993/manual-transcription.md`.",
		"- Several switches have no dedicated playfield trigger object because the retained script sets their "
		"public state directly from another mechanism's continuous position (idol motor angle, Path of Adventure "
		"linear tilt counter) or because the trough's own ball-stack class has no per-position object. Those "
		"addresses are explicit documented projections onto the real table object that carries the underlying "
		"mechanism state.",
		"- The Path of Adventure insert lamps (71-75, 81-85) share one raw local-space Primitive coordinate because "
		"they are children of the tilting mini-playfield group; each is projected onto the playfield-fixed switch "
		"or trigger object at the same lane position instead of using that shared placeholder.",
		"- gi060 and gi061 are Light objects that belong to no active GI collection (`GiTopSides`/`GiBotSides` are "
		"both declared empty in `collections.json`) and are excluded as orphaned table-modeling objects.",
		"- GI addresses 0 (Top Playfield) and 1 (Bottom Playfield) use the retained table's own GITop/GIBumpers and "
		"GiBot emitter collections; every one of their 34 and 32 members has an individually transcribed and "
		"validated placement.",
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
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for the addresses this "
		"audit covers, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. However, public switch 71 (Captive Ball Front) and switches 121-123 (Wheel Position 1-3) "
		"are printed normally-closed opto interrupters per the manual's own board schematics that pinned PinMAME's "
		"ijGameData inverted-switch mask does not normalize, unlike their opto column neighbors (72/73 and "
		"124/125 respectively) -- two unresolved polarity conflicts recorded as `conflict.captive-ball-front-opto-"
		"not-normalized` and `conflict.wheel-position-opto-not-normalized`. The definition therefore carries a "
		"non-empty `conflicts` array and `coverage.dimensions.physical_wiring = \"conflicted\"`, so promotion to "
		"`author_ready` is refused; the record stays `partial` with `coverage.missing = [\"polarity\", "
		"\"unresolved_conflicts\"]` until a LibPinMAME harness trace against a legal ij_l7 ROM observes the true "
		"idle and transition public state of all four addresses.",
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
		raise RuntimeError(f"Stale Indiana Jones author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Indiana Jones definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Indiana Jones seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Indiana Jones definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Indiana Jones seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Indiana Jones spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Indiana Jones spatial review drifted from its deterministic curator: {markdown_path}")
	print("Indiana Jones definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Indiana Jones extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Indiana Jones retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
