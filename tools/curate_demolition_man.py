"""Curate the physical Williams Demolition Man (1994) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived
fact as a literal and reads one committed seed for the placements (the retained table's object coordinates, rebuilt
by tools/demolition_man_spatial_seed.py), so regeneration reproduces the canonical artifact byte-for-byte without
reading the external evidence roots. ``--check`` refuses drift, and ``--regenerate`` is the only path that writes the
definition, its knowledge note and its spatial report.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]

MACHINE_ID = "williams.demolition-man.1994"
PARTIAL_PATH = ROOT / "machines/partial/williams/demolition-man-1994.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/demolition-man-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/demolition-man-1994.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/williams/demolition-man-1994.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/williams/demolition-man-1994-spatial.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/williams/demolition-man-1994-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/demolition-man-1994.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/demolition-man-1994.md"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = "pinmame.catalog.97aa922bf8e4"
CORE_SOURCE = "pinmame.core.97aa922bf8e4"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-dcs"
IDENTITY_SOURCE = "identity.williams.demolition-man.1994"
MANUAL_SOURCE = "manual.williams.demolition-man.1994"
PARTS_LIST_SOURCE = "parts-list.williams.demolition-man.1994"
VPX_TABLE_SOURCE = "vpx-table.dm-knorr-kiwi-1-3-1"
VPX_SCRIPT_SOURCE = "vpx-script.dm-knorr-kiwi-1-3-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.dm-knorr-kiwi-1-3-1"
VPM_LIBRARY_SOURCE = "vpm-script-library.wpc-vbs"
EDGES_SOURCE = "runtime.demolition-man.switch-edges"
CLAW_TEST_SOURCE = "runtime.demolition-man.claw-test"
CLAW_FUNCTIONS_SOURCE = "runtime.demolition-man.claw-functions"
SOLENOID_TEST_SOURCE = "runtime.demolition-man.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.demolition-man.flasher-test"
GI_TEST_SOURCE = "runtime.demolition-man.gi-test"
FLIPPER_TEST_SOURCE = "runtime.demolition-man.flipper-coil-test"
LAMP_TEST_SOURCE = "runtime.demolition-man.single-lamps"
CALLOUT_SOURCE = "drawing-callouts.demolition-man.2026-10-09"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-dcs"
RUNTIME_LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"

TABLE_NAME = "Demolition Man (Knorr-Kiwi) 1.3.1.vpx"
TABLE_SHA256 = "099c70add2201ea3e49c34c9f910e365bd88218d8bf755846ceee93bce82fbd3"
SCRIPT_SHA256 = "0af7e1f50985d5a36d7b3f74ac1254a9d54594189c92934072a8951e7bf75e12"
MANUAL_NAME = "Williams_1994_Demolition_Man_Operations_Manual_English_OCR_searchable.pdf"
MANUAL_SHA256 = "faa0c6f426dcac85fbc9f167e7d3a8b78ac3269b8b65530fb3111e1811f88981"
PARTS_LIST_NAME = "Williams_1994_Demolition_Man_Parts_List.txt"
PARTS_LIST_SHA256 = "0cc6686b9c5fb09f2031c66a720310bd97ac30470cba56b41a40f66860d2a557"
IPDB_PAGE_SHA256 = "38881a6c827637e5f874f4d2f16d94d5e43b5bb4434121ba710627ec43f885e8"
VPM_WPC_SHA256 = "1a290886eb2c2fd2c13f82e5f8a1961fdc95238122096642d32fddf1cfbb1a8d"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"
PLAYFIELD_WIDTH = 1093.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=1093 bottom=2162"

EXTRACTION_FILE_COUNT = 1027
EXTRACTION_TOTAL_BYTES = 215888219
EXTRACTION_MANIFEST_SHA256 = "a72529f25cbcc1be65bfc8d2113a502e6e7b4c5c532d5c786a025ca835028676"
EXTRACTION_RELATIVE_PATH = Path("williams/demolition-man-1994/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/demolition-man-1994/extracted-vpxtool.manifest.json")

EXCERPT_ROOT = ROOT / f"evidence/excerpts/{MACHINE_ID}"
MANUALS_DIRECTORY = f"pinmame-manuals/by-machine/{MACHINE_ID}/ipdb-662"
IPDB_WAYBACK = "https://web.archive.org/web/20260904082252id_/https://www.ipdb.org/machine.cgi?id=662"
MANUAL_WAYBACK = "https://web.archive.org/web/20180814111452id_/https://www.ipdb.org/files/662/" + MANUAL_NAME
PARTS_LIST_WAYBACK = "https://web.archive.org/web/20180814110944id_/https://www.ipdb.org/files/662/" + PARTS_LIST_NAME
RIGHTS_NOTE = "Williams Electronics Games; scan hosted by the Internet Pinball Machine Database"
EXCERPT_CREDIT = "curator, read from the rendered page"

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = (
	"dm_lx4", "dm_dx4", "dm_lx4c", "dm_lx3", "dm_dx3", "dm_la1", "dm_da1", "dm_h5", "dm_dh5", "dm_h5b", "dm_dh5b",
	"dm_h6", "dm_h6b", "dm_h6c", "dm_pa2", "dm_pa3", "dm_px5", "dm_px6", "dm_dt099", "dm_dt101",
)
_GHOST = "a community 'LED Ghost Fix' revision of {base}, which changes the lamp-matrix timing against LED ghosting and no controller address or playfield device"
_HOME = (
	"Williams home ROM {name} for the same physical machine, built with the eight-ROM DCS sound set (dm.2-dm.9). The manual's "
	"A-16917-50028 sound board prints sockets U8 and U9 as 'Not Used' on the arcade build, so the home sound set fills sockets the "
	"board already carries; the game ROM runs on the same WPC-DCS CPU and I/O"
)
DRIVER_COMPATIBILITY = {
	"dm_lx4": ("identical", "Production LX-4 game ROM, the pinned parent driver; the retained known-working Knorr/Kiwi 1.3.1 table binds it directly (Const cGameName = \"dm_lx4\") and every runtime run behind this definition booted it."),
	"dm_dx4": ("identical", "DX-4: " + _GHOST.format(base="LX-4") + "."),
	"dm_lx4c": ("identical", "LX-4C 'Competition + LED Ghost MOD' (2020), a community patch of LX-4 (pinned dm.c: 'L-4X patch 00c6'); it changes game rules and lamp timing, not the hardware, and pairs with the same L-2 sound ROMs."),
	"dm_lx3": ("identical", "LX-3, an earlier production game ROM of the same machine with the same L-2 sound ROMs."),
	"dm_dx3": ("identical", "DX-3: " + _GHOST.format(base="LX-3") + "."),
	"dm_la1": ("identical", "LA-1, the first production game ROM, paired with the L-1 U2 sound ROM (dm_u2_s.l1) and the L-2 U3-U7 set."),
	"dm_da1": ("identical", "DA-1: " + _GHOST.format(base="LA-1") + "."),
	"dm_h5": ("identical", _HOME.format(name="H-5") + "."),
	"dm_dh5": ("identical", "DH-5: " + _GHOST.format(base="H-5") + "."),
	"dm_h5b": ("identical", _HOME.format(name="H-5B ('Coin Play')") + "."),
	"dm_dh5b": ("identical", "DH-5B: " + _GHOST.format(base="H-5B") + "."),
	"dm_h6": ("identical", _HOME.format(name="H-6") + "."),
	"dm_h6b": ("identical", _HOME.format(name="H-6B ('Coin Play')") + "."),
	"dm_h6c": ("identical", "H-6C 'Competition MOD' (2019), a community patch of the H-6 home ROM (pinned dm.c: 'L-6H patch 4d2b') with the same eight-ROM sound set."),
	"dm_pa2": ("unknown", "PA-2 prototype game ROM paired with the prototype P-4 sound ROMs (dmsndp4.u2-u7). Pinned dm.c gives it the production dmGameData, which proves the emulator's routing, not the prototype machines' hardware: no retained source documents their playfield, harness or mechanisms, so its physical compatibility with the production machine stays unknown."),
	"dm_pa3": ("unknown", "PA-3: " + _GHOST.format(base="the PA-2 prototype") + "; prototype firmware like PA-2, whose hardware no retained source documents."),
	"dm_px5": ("unknown", "PX-5 prototype game ROM with the prototype P-4 sound ROMs; as dm_pa2, no retained source documents the hardware it ran on."),
	"dm_px6": ("unknown", "PX-6: " + _GHOST.format(base="the PX-5 prototype") + "; prototype firmware like PX-5, whose hardware no retained source documents."),
	"dm_dt099": ("compatible", "FreeWPC 'Demolition Time' 0.99 (2014), community firmware written for the physical machine and paired with the H-5 home sound set. Its game image is 1 MB (pinned dm.c loads a 0x100000-byte ROM) where the production U6 ROM is a 27c040 (512 KB) and the manual's ROM jumper chart covers only 1M/2M/4M parts, so fitting it needs a larger EPROM than the machine shipped with; its rules and its use of the outputs differ from the Williams ROMs."),
	"dm_dt101": ("compatible", "FreeWPC 'Demolition Time' 1.01 (2014); as dm_dt099. Pinned dm.c's P-ROC hook notes that this firmware 'doesn't use solenoids 28/30', so a recreation cannot assume its output use matches the Williams ROMs."),
}

# --- Switch data -------------------------------------------------------------------------------------
# address -> (manual label, Switch Locations part cell(s), switch type, role or None). Part cells are literal.
SWITCHES: dict[int, tuple[str, str | None, str, str | None]] = {
	11: ("Ball Launch", "20-9663-B-4 (cabinet); 20-9804 (button); 5647-12693-11 (trigger)", "button", "cabinet.launch"),
	12: ("Left Handle Button", "20-9804 (button); 5647-12693-11 (trigger)", "button", "cabinet.left-handle-button"),
	13: ("Start Button", "20-9663-1", "button", "cabinet.start"),
	14: ("Plumb Bob Tilt", "20-6502-A", "tilt", "cabinet.tilt"),
	15: ("Left Outlane", "5467-12693-19", "microswitch", None),
	16: ("Left Inlane", "5467-12693-19", "microswitch", None),
	17: ("Right Inlane", "5467-12693-19", "microswitch", None),
	18: ("Right Outlane", "5467-12693-19", "microswitch", None),
	21: ("Slam Tilt", "A-17238", "tilt", "cabinet.slam-tilt"),
	22: ("Coin Door Closed", "5643-09268-00", "microswitch", "cabinet.coin-door"),
	23: ("Buy-in Button", "20-9663-9", "button", "cabinet.buy-in"),
	24: ("Always Closed", "5643-09112-00", "other", None),
	25: ("Claw Position 1 (Claw Right)", "A-16986", "opto", None),
	26: ("Claw Position 2 (Claw Left)", "A-16986", "opto", None),
	27: ("Shooter Lane", "A-16759", "microswitch", None),
	31: ("Trough 1", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	32: ("Trough 2", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	33: ("Trough 3", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	34: ("Trough 4", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	35: ("Trough 5", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	36: ("Trough Jam", "A-16927 (LED); A-16926 (transistor)", "opto", None),
	38: ("Standup 5", "A-8017-6", "leaf", None),
	41: ("Left Slingshot", "A-17801 (count); SW-1A-120 (score)", "leaf", None),
	42: ("Right Slingshot", "A-17801 (count); SW-1A-120 (score)", "leaf", None),
	43: ("Left Jet Bumper", "A-12030-3", "leaf", None),
	44: ("Top Slingshot", "A-17801 (count); SW-1A-120 (score)", "leaf", None),
	45: ("Right Jet Bumper", "A-12030-3", "leaf", None),
	46: ("Right Ramp Enter", "55647-12693-36", "microswitch", None),
	47: ("Right Ramp Exit", "5647-12693-11", "microswitch", None),
	48: ("Right Freeway", "5467-12693-19", "microswitch", None),
	51: ("Left Ramp Enter", "5647-12693-11", "microswitch", None),
	52: ("Left Ramp Exit", "5647-12693-11", "microswitch", None),
	53: ("Center Ramp", "5647-12693-11", "microswitch", None),
	54: ("Upper Rebound", "SW-1A-120", "leaf", None),
	55: ("Left Loop", "5647-12693-19", "microswitch", None),
	56: ("Standup 2", "A-18017-6", "leaf", None),
	57: ("Standup 3", "A-18019-6", "leaf", None),
	58: ("Standup 4", "A-18019-6", "leaf", None),
	61: ("Side Ramp Enter", "5647-12693-11", "microswitch", None),
	62: ("Side Ramp Exit", "5647-12693-11", "microswitch", None),
	63: ("Left Rollover (M)", "5467-12693-19", "microswitch", None),
	64: ("Center Rollover (T)", "5467-12693-19", "microswitch", None),
	65: ("Right Rollover (L)", "5467-12693-19", "microswitch", None),
	66: ("Eject", "5647-12133-11", "microswitch", None),
	67: ("Elevator Index", "A-17596", "opto", None),
	71: ("Chase Car 1", "A-16908 (LED); A-16909 (Transistor)", "opto", None),
	72: ("Chase Car 2", "A-16908 (LED); A-16909 (Transistor)", "opto", None),
	73: ("Top Popper", "A-16908 (LED); A-16909 (Transistor)", "opto", None),
	74: ("Elevator Hold", "A-16908 (LED); A-16909 (Transistor)", "opto", None),
	76: ("Bottom Popper", "A-16908 (LED); A-16909 (Transistor)", "opto", None),
	77: ("Eyeball Standup", "A-18018-4", "leaf", None),
	78: ("Standup 1", "A-18017-6", "leaf", None),
	81: ('Claw "Capture Simon"', "5647-12073-17", "microswitch", None),
	82: ('Claw "Super Jets"', "5647-12693-21", "microswitch", None),
	83: ('Claw "Prison Break"', "5647-12693-21", "microswitch", None),
	84: ('Claw "Freeze"', "5647-12693-21", "microswitch", None),
	85: ('Claw "ACMAG"', "5647-12693-21", "microswitch", None),
	86: ("Upper Left Flipper Gate", "5647-12693-11", "microswitch", None),
	87: ("Car Chase Standup", "A-18018-4", "leaf", None),
	88: ("Lower Rebound", "SW-1A-120", "leaf", None),
}
UNUSED_MATRIX_ADDRESSES = (28, 37, 68, 75)
# Matrix labels the Switch Matrix page prints differently from the Switch Locations list.
MATRIX_LABELS = {
	25: "Claw Position 1", 26: "Claw Position 2", 63: "Left Rollover", 64: "Center Rollover", 65: "Right Rollover",
	82: 'Claw "Sup. Jets"',
}
# The name the ROM's T.1 SWITCH EDGES prints (runtime.demolition-man.switch-edges).
ROM_SWITCH_NAMES = {
	11: "BALL LAUNCH", 12: "L. HANDLE BUTTON", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "LEFT OUTLANE", 16: "LEFT INLANE",
	17: "RIGHT INLANE", 18: "RIGHT OUTLANE", 21: "SLAM TILT", 23: "BUY-IN BUTTON", 24: "ALWAYS CLOSED", 25: "CLAW RIGHT",
	26: "CLAW LEFT", 27: "SHOOTER LANE", 28: "NOT USED", 31: "TROUGH 1 (RIGHT)", 32: "TROUGH 2", 33: "TROUGH 3", 34: "TROUGH 4",
	35: "TROUGH 5 (LEFT)", 36: "TROUGH JAM", 37: "NOT USED", 38: "STANDUP 5", 41: "LEFT SLING", 42: "RIGHT SLING", 43: "LEFT JET",
	44: "TOP SLING", 45: "RIGHT JET", 46: "R. RAMP ENTER", 47: "R. RAMP EXIT", 48: "RIGHT LOOP", 51: "L. RAMP ENTER",
	52: "L. RAMP EXIT", 53: "CENTER RAMP", 54: "UPPER REBOUND", 55: "LEFT LOOP", 56: "STANDUP 2", 57: "STANDUP 3", 58: "STANDUP 4",
	61: "SIDE RAMP ENTER", 62: "SIDE RAMP EXIT", 63: "(M)TL ROLLOVER", 64: "M(T)L ROLLOVER", 65: "MT(L) ROLLOVER", 66: "EJECT",
	67: "ELEVATOR INDEX", 68: "NOT USED", 71: "CAR CRASH 1", 72: "CAR CRASH 2", 73: "TOP POPPER", 74: "ELEVATOR HOLD",
	75: "NOT USED", 76: "BOTTOM POPPER", 77: "EYEBALL STANDUP", 78: "STANDUP 1", 81: 'CLAW "CAPT. SIM."', 82: 'CLAW "SUP. JETS"',
	83: 'CLAW "PR. BREAK"', 84: 'CLAW "FREEZE"', 85: 'CLAW "ACMAG"', 86: "UL. FLIPPER GATE", 87: "CAR CR. STANDUP", 88: "LOWER REBOUND",
}
# Shaded 'Opto Switch' cells of the Switch Matrix page; PinMAME's dmGameData invSw inverts the same set (tests decode it).
OPTO_SWITCHES = frozenset({25, 26, 31, 32, 33, 34, 35, 36, 67, 71, 72, 73, 74, 76})
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"), 3: ("Green-Orange", "J207-3", "U20-16"),
	4: ("Green-Yellow", "J207-4", "U20-15"), 5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"), 3: ("White-Orange", "J209-3", "U18-5"),
	4: ("White-Yellow", "J209-4", "U18-7"), 5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1"), 2: ("Orange-Red", "J205-2"), 3: ("Orange-Black", "J205-3"), 4: ("Orange-Yellow", "J205-4"),
	5: ("Orange-Green", "J205-6"), 6: ("Orange-Blue", "J205-7"), 7: ("Orange-Violet", "J205-8"), 8: ("Orange-Gray", "J205-9"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute (printed 'Forth Coin Chute' on the Section 3 dedicated-switch drawing, which draws no J3 pin for it)."),
	5: ("Service Credits / Escape", "service.escape", "Service Credits in normal play and Escape inside the menu system; the harness runs pulse it to leave the fresh-NVRAM message loop."),
	6: ("Volume Down / Down", "service.down", "Volume Down in normal play and Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Volume Up in normal play and Up inside the menu system; the harness runs step every service test with it."),
	8: ("Begin Test / Enter", "service.enter", "Begin Test in normal play and Enter inside the menu system."),
}
# What the retained known-working script does with each matrix switch.
SWITCH_SCRIPT = {
	11: "the plunger key writes Controller.Switch(11) and Controller.Switch(12) together", 12: "the plunger key writes it together with 11",
	14: "vpmNudge.TiltSwitch is set to 14 in Table1_Init and then overwritten with 1 after the FastFlips setup, so the table's nudge tilt pulses the left coin chute instead; a defect of the table, not of the machine",
	15: "sw15_Hit/_UnHit follow the ball", 16: "sw16_Hit/_UnHit follow the ball", 17: "sw17_Hit/_UnHit follow the ball", 18: "sw18_Hit/_UnHit follow the ball",
	22: "Table1_Init closes it (Controller.Switch(22) = 1)", 23: "the front key writes Controller.Switch(23)", 24: "Table1_Init holds it closed (Controller.Switch(24) = 1)",
	25: "the claw cvpmMech (sol1 = 19, sol2 = 20, 147 steps) sets it at positions 0-2, the end nearest the elevator",
	26: "the claw cvpmMech sets it at positions 140-147, the far end",
	27: "sw27_Hit/_UnHit follow the ball",
	31: "cvpmBallStack bsTrough (InitSw 0, 31, 32, 33, 34, 35) keeps it", 32: "cvpmBallStack bsTrough keeps it", 33: "cvpmBallStack bsTrough keeps it",
	34: "cvpmBallStack bsTrough keeps it", 35: "cvpmBallStack bsTrough keeps it (the entry position)",
	36: "SolRelease pulses it each time solenoid 1 releases a ball",
	38: "Standup38_Hit pulses it", 41: "LeftSlingShot_Slingshot pulses it", 42: "RightSlingShot_Slingshot pulses it",
	43: "leftjetbumper_Hit pulses it", 44: "TopSlingShot_Slingshot pulses it", 45: "rightjetbumper_Hit pulses it",
	46: "sw46_Hit/_UnHit follow the ball", 47: "sw47_Hit/_UnHit follow the ball", 48: "sw48_Hit/_UnHit follow the ball",
	51: "sw51_Hit/_UnHit follow the ball", 52: "sw52_Hit/_UnHit follow the ball", 53: "sw53_Hit/_UnHit follow the ball",
	54: "UpperRebound_Slingshot pulses it", 55: "sw55_Hit/_UnHit follow the ball", 56: "Standup56_Hit pulses it",
	57: "Standup57_Hit pulses it", 58: "Standup58_Hit pulses it", 61: "sw61_Hit/_UnHit follow the ball", 62: "sw62_Hit/_UnHit follow the ball",
	63: "sw63_Hit/_UnHit follow the ball", 64: "sw64_Hit/_UnHit follow the ball", 65: "sw65_Hit/_UnHit follow the ball",
	66: "cvpmBallStack bsEject (InitSaucer sw66, 66) keeps it",
	67: "the elevator cvpmMech (sol1 = 18, 70 steps, vpmMechReverse) sets it at positions 0-2",
	71: "Table1_Init sets it to 1 and sw71_Hit sets it to 0 while the Oldsmobile car's hidden captive ball rests in the trigger (sw71_UnHit sets 1 again)",
	72: "Table1_Init sets it to 1 and sw72_Hit sets it to 0 while the GM Ultralite car's hidden captive ball rests in the trigger (sw72_UnHit sets 1 again)",
	73: "cvpmBallStack bsTopPopper (InitSaucer sw73, 73) keeps it",
	74: "ElevatorKicker_Hit sets it when a ball enters the elevator, and the elevator cvpmMech sets it at positions 65-70; the table never clears it from the kicker side",
	75: "sw75_Hit/_UnHit write it from a trigger on the elevator ramp",
	76: "cvpmBallStack BottomPopper (InitSw 0, 76) keeps it", 77: "Standup77_Hit pulses it", 78: "Standup78_Hit pulses it",
	81: "ClawRampKicker_Hit pulses it when the claw drops a ball at Capture Simon", 82: "sw82_Hit/_UnHit follow the ball", 83: "sw83_Hit/_UnHit follow the ball",
	84: "sw84_Hit/_UnHit follow the ball", 85: "sw85_Hit/_UnHit follow the ball", 86: "sw86_Hit/_UnHit follow the ball",
	87: "Standup87_Hit pulses it", 88: "LowerRebound_Slingshot pulses it",
}
SWITCH_NOTES = {
	11: "The Switch Locations list prints three parts for this switch: the cabinet Launch Ball button 20-9663-B-4 (lit by lamp 87), the handle button 20-9804 and the trigger part 5647-12693-11; the manual's game-control page says the handle buttons or the Launch Ball button launch a ball, so the cabinet button and the right handle's thumb button share this address. The Control Handle assemblies A-18016-1/-2 each carry a Thumb Button Switch Assembly A-18511.",
	12: "The left handle's thumb button (20-9804 button, 5647-12693-11 per the Switch Locations list). The game uses it to launch a ball and for player choices such as dropping the claw (rules page: 'select the claw goal by dropping the ball with the launch button or the gun buttons').",
	13: "The lit Start Button (lamp 88).",
	21: "Cabinet slam tilt.", 22: "Closed while the coin door is closed.",
	23: "The cabinet Buy-in (Extra Ball) button 20-9663-9, lit by lamp 86; the cabinet parts list calls it 'Extra Ball Button, Yellow'.",
	24: "Always Closed switch 5643-09112-00. Unlike every other swept switch the ROM's T.1 names it when public 24 falls to 0 (an opening of a contact that should never open) and not when it rises; a recreation holds it at 1, as the retained script does.",
	25: "On the Cryoclaw Opto PCB A-16986 (captioned 'SW. #25 CLAW POSITION 1'), Opto 1, wired column 2 Green-Red J1-4 and row 5 White-Green J1-5. The manual's Cryoclaw theory: Claw Right blocked with Claw Left open means the arm is at right, above the elevator.",
	26: "On the Cryoclaw Opto PCB A-16986 ('SW. #26 CLAW POSITION 2'), Opto 2, row 6 White-Blue J1-6. The manual's Cryoclaw theory: Claw Left blocked with Claw Right open means the arm is at left, away from the elevator; both blocked is 'arm out of range' and the CPU will not run the motor.",
	27: "Shooter-lane switch under a ball waiting for the auto plunger (solenoid 3).",
	31: "Trough opto pair on the 7 Ball Trough LED and Photo Transistor boards (A-17982 / A-17981); the ROM calls position 1 the right end, the exit toward the shooter lane.",
	35: "The ROM calls position 5 the left end, where a drained ball enters.",
	36: "Trough Jam opto at the trough's exit end; the retained script pulses it on every ball release.",
	41: "The Score slingshot switches have diodes across them (Switch Locations footnote); A-17801 is the count switch and SW-1A-120 the score switch of the kicker arm.",
	42: "Score switch with a diode across it (Switch Locations footnote).", 44: "Score switch with a diode across it (Switch Locations footnote); the third slingshot, below the jet bumpers.",
	48: "The ROM calls it RIGHT LOOP; the manual prints Right Freeway.",
	55: "PinMAME's dm.c names this swLoopCenter with the comment 'in manual as Left Loop'.",
	63: "The ROM labels it (M)TL ROLLOVER, the M of the three M-T-L lanes above the jet bumpers.", 64: "The T of the M-T-L lanes.", 65: "The L of the M-T-L lanes.",
	66: "The eject saucer beside the Retina Scan; solenoid 14 kicks the ball out.",
	67: "On the Elevator Opto PCB A-17596 ('SW. #67 ELEVATOR INDEX'), wired row 7 White-Violet and column 6 Green-Blue. The manual: 'The elevator has a single opto (index) switch for detecting the DOWN position of the elevator'; the motor coasts so the actuator normally stops just beyond it.",
	71: "One of the five optos of the A-15576 7-Opto Switch Board (position E1); the shot pushes the first Matchbox car up its tunnel into the beam.",
	72: "7-Opto Switch Board position E2; the second car.",
	73: "7-Opto Switch Board position E3, the opto under the Top Popper (A-17215 Ball Popper Assembly - Rear, which carries an RTV LED/photo-transistor pair).",
	74: "7-Opto Switch Board position E4. The Cryoclaw errors say a broken Elevator Hold switch can raise 'Magnet Broken'; PinMAME's model notes the opto also reads blocked while the elevator rises without a ball.",
	76: "7-Opto Switch Board position E6, the opto of the Bottom Popper (the A-17620 Chute Assembly carries an A-16908/A-16909 pair).",
	77: "The standup the custom Retina Scan captive ball ('eyeball') strikes.",
	81: "Rollover the claw drops a ball onto at the Capture Simon goal; the ball then runs to the bottom popper.",
	82: "Claw goal rollover: Super Jets.", 83: "Claw goal rollover: Prison Break.", 84: "Claw goal rollover: Freeze.", 85: "Claw goal rollover: ACMAG.",
	86: "PinMAME's dm.c names it swLoopLeft with the comment 'in manual as Upper Left Flipper Gate'.",
	87: "The standup at the end of the car-chase tunnel.",
}
# The seven stationary (standup) targets: Target Assemblies page (PDF 90, printed 2-34) lists three A-17795-6, two A-17799-6 and
# two A-18018-4 assemblies, seven in all, each drawn as a leaf-contact stack with a diode.
STANDUP_TARGETS = frozenset({38, 56, 57, 58, 77, 78, 87})
UNUSED_SWITCH_NOTES = {
	28: "The Switch Matrix prints Not Used; the Switch Locations list prints part 5467-12693-19 against 'Not Used'.",
	37: "The Switch Matrix and the Switch Locations list print Not Used.",
	68: "The Switch Matrix and the Switch Locations list print Not Used.",
	75: (
		"The Switch Matrix page (PDF 100, printed 2-44) prints this cell 'Elevator Ramp' and the switch drawing carries a balloon 75 near the "
		"top popper, but the Switch Locations list prints 'Not Used' in its part column, the Section 3 reprint of the matrix (PDF 106) prints "
		"'Not Used', the 7-Opto board and the elevator pages name no switch 75, and the ROM's own T.1 names public 75 'NOT USED'. The ROM "
		"therefore reads nothing at this address; the retained script nevertheless writes it from an elevator-ramp trigger and pinned dm.c "
		"defines swElevatorRamp 75 without using it, both harmless. A recreation need not drive it."
	),
}
# Fliptronic grounded switches: address -> (label, printed number, wire, connector, type, role, availability).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J906-1", "leaf", "internal.flipper.lower.right.eos", "used"),
	112: ("Lower Right Flipper Cabinet Opto", "F2", "Blue-Violet", "J905-1", "opto", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J906-3", "leaf", "internal.flipper.lower.left.eos", "used"),
	114: ("Lower Left Flipper Cabinet Opto", "F4", "Blue-Gray", "J905-2", "opto", "flipper.lower.left.button", "used"),
	115: ("Not Used Upper Right Flipper EOS", "F5", "Black-Violet", "J906-4", None, "internal.unused.flipper", "unused"),
	116: ("Not Used Upper Right Flipper Cabinet Opto", "F6", "Black-Yellow", "J905-3", None, "internal.unused.flipper", "unused"),
	117: ("Upper Left Flipper EOS", "F7", "Black-Gray", "J906-5", "leaf", "internal.flipper.upper.left.eos", "used"),
	118: ("Upper Left Flipper Cabinet Opto", "F8", "Black-Blue", "J905-5", "opto", "flipper.upper.left.button", "used"),
}

# --- Solenoid data -----------------------------------------------------------------------------------
# address -> (manual function, printed type, voltage connection(s), transistor, drive connection(s), wire, part, location assembly).
SOLENOID_TABLE: dict[int, tuple[str, str | None, str | None, str, str | None, str, str | None, str | None]] = {
	1: ("Ball Release", "High Power", "J107-3", "Q82", "J130-1", "Vio-Brn", "AE-26-1500", "A-16765"),
	2: ("Bottom Popper", "High Power", "J107-3", "Q80", "J130-2", "Vio-Red", "AE-23-800", "A-17620"),
	3: ("Auto Plunger", "High Power", "J107-3", "Q78", "J130-4", "Vio-Org", "AE-23-800", "A-14525"),
	4: ("Top Popper", "High Power", "J107-3", "Q76", "J130-5", "Vio-Yel", "AE-28-1500", "A-17215"),
	5: ("Diverter Power", "High Power", "J107-3", "Q64", "J130-6", "Vio-Grn", "A-15943-1", "A-17241"),
	6: ("Not Used", "High Power", None, "Q66", None, "Vio-Blu", None, None),
	7: ("Knocker", "High Power", "J107-3 (backbox)", "Q68", "J130-8 (backbox)", "Vio-Blk", "AE-23-800", "B-10686-1"),
	8: ("Not Used", "High Power", None, "Q70", None, "Vio-Gry", None, None),
	9: ("Left Slingshot", "Low Power", "J107-2", "Q58", "J127-1", "Brn-Blk", "AE-26-1200", "A-17809"),
	10: ("Right Slingshot", "Low Power", "J107-2", "Q56", "J127-3", "Brn-Red", "AE-26-1200", "A-17809-1"),
	11: ("Left Jet Bumper", "Low Power", "J107-2", "Q54", "J127-4", "Brn-Org", "AE-26-1200", "A-9415-2"),
	12: ("Top Slingshot", "Low Power", "J107-2", "Q52", "J127-5", "Brn-Yel", "AE-26-1200", "A-17809"),
	13: ("Right Jet Bumper", "Low Power", "J107-2", "Q50", "J127-6", "Brn-Grn", "AE-26-1200", "A-9415-2"),
	14: ("Eject", "Low Power", "J107-2", "Q48", "J127-7", "Brn-Blu", "AE-26-1200", "A-17809"),
	15: ("Diverter Hold", "Low Power", "J107-2", "Q46", "J127-8", "Brn-Vio", "A-15943-1", "A-17241"),
	16: ("Not Used", "Low Power", None, "Q44", None, "Brn-Gry", None, None),
	17: ("Claw Flasher", "Low Power", "J107-6, J106-5", "Q42", "J126-1, J125-1", "Blk-Brn", "#906 (1) playfield, #906 (1) backbox", "C-13337"),
	18: ("Elevator Motor", None, "J118-2", "Q40", "J126-2", "Blk-Red", "14-7993", "A-17597"),
	19: ("Claw Motor Left", None, "J118-2", "Q38", "J126-3", "Blk-Org", "14-7992", "A-16989"),
	20: ("Claw Motor Right", None, "J118-2", "Q36", "J126-4", "Blk-Yel", "14-7992", "A-16989"),
	21: ("Jets Flasher", "Flasher", "J107-6, J106-5", "Q28", "J126-5, J125-6", "Blu-Grn", "#89 (1) playfield, #906 (1) backbox", "A-17803"),
	22: ("Side Ramp Flasher", "Flasher", "J107-6, J106-5", "Q30", "J126-6, J125-7", "Blu-Blk", "#89 (1) playfield, #906 (1) backbox", "A-17983"),
	23: ("Left Ramp Up Flshr", "Flasher", "J107-6, J106-5", "Q34", "J126-7, J125-8", "Blu-Vio", "#906 (1) playfield, #906 (1) backbox", None),
	24: ("Left Ramp Lwr Flshr", "Flasher", "J107-6, J106-5", "Q32", "J126-8, J125-9", "Blu-Gry", "#89 (1) playfield, #906 (1) backbox", "A-17983"),
	25: ("Car Chase Cntr Flshr", "Gen. Purpose", "J107-6, J106-5", "Q26", "J122-1, J124-1", "Blu-Brn", "#89 (1) playfield, #906 (1) backbox", "A-17803"),
	26: ("Car Chase Lwr Flshr", "Gen. Purpose", "J107-6, J106-5", "Q24", "J122-2, J124-2", "Blu-Red", "#89 (1) playfield, #906 (1) backbox", "A-17803"),
	27: ("Right Ramp Flasher", "Gen. Purpose", "J107-6, J106-5", "Q22", "J122-3, J124-3", "Blu-Org", "#89 (1) playfield, #906 (1) backbox", "A-17983"),
	28: ("Eject Flasher", "Gen. Purpose", "J107-6, J106-5", "Q20", "J122-4, J124-5", "Blu-Yel", "#89 (1) playfield, #906 (1) backbox", "A-17983"),
}
# Auxiliary 8-Driver board flashers: public address -> (printed number, function, transistor, J connection, wire, flashlamp, assembly, count).
AUX_FLASHERS = {
	51: (37, "Car Chase Up Flshr", "Q16", "J4-2", "Brn-Wht", "#89", "A-17803", 1),
	52: (38, "Lower Rebound Flshr", "Q15", "J4-4", "Blk-Wht", "#89", "A-17983", 1),
	53: (39, "Eyeball Flasher", "Q14", "J4-5", "Org-Wht", "#89", "A-17803", 1),
	54: (40, "Center Ramp Flasher", "Q13", "J4-6", "Yel-Wht", "#89", "A-17983", 1),
	55: (41, "Elevator 2 Flasher", "Q9", "J3-2", "Grn-Wht", "#906", "C-13337", 2),
	56: (42, "Elevator 1 Flasher", "Q10", "J3-3", "Blu-Wht", "#906", "C-13337", 1),
	57: (43, "Diverter Flasher", "Q11", "J3-4", "Vio-Wht", "#906", None, 1),
	58: (44, "Rt. Ramp Up Flasher", "Q12", "J3-5", "Gry-Wht", "#906", None, 1),
}
SOLENOID_LABELS = {
	1: "Ball Release", 2: "Bottom Popper", 3: "Auto Plunger", 4: "Top Popper", 5: "Diverter Power", 7: "Knocker",
	9: "Left Slingshot", 10: "Right Slingshot", 11: "Left Jet Bumper", 12: "Top Slingshot", 13: "Right Jet Bumper", 14: "Eject",
	15: "Diverter Hold", 17: "Claw Flasher", 18: "Elevator Motor", 19: "Claw Motor Left", 20: "Claw Motor Right",
	21: "Jets Flasher", 22: "Side Ramp Flasher", 23: "Left Ramp Upper Flasher", 24: "Left Ramp Lower Flasher",
	25: "Car Chase Center Flasher", 26: "Car Chase Lower Flasher", 27: "Right Ramp Flasher", 28: "Eject Flasher",
	33: "Claw Magnet", 35: "Upper Left Flipper Power", 36: "Upper Left Flipper Hold",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold", 47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
	51: "Car Chase Upper Flasher", 52: "Lower Rebound Flasher", 53: "Eyeball Flasher", 54: "Center Ramp Flasher",
	55: "Elevator 2 Flasher", 56: "Elevator 1 Flasher", 57: "Diverter Flasher", 58: "Right Ramp Upper Flasher",
}
NOT_USED_SOLENOIDS = {6: "Not Used Solenoid 6", 8: "Not Used Solenoid 8", 16: "Not Used Solenoid 16", 34: "Not Used Upper Right Flipper Hold"}
FLASHER_SOLENOIDS = frozenset({17, 21, 22, 23, 24, 25, 26, 27, 28, 51, 52, 53, 54, 55, 56, 57, 58})
BACKBOX_FLASHER_SOLENOIDS = frozenset({17, 21, 22, 23, 24, 25, 26, 27, 28})
# The ROM's own name, printed number and wires (T.4, T.5 and T.12 runs).
ROM_OUTPUT_NAMES = {
	1: ("T.4", "BALL RELEASE", "01", "VIO-BRN RED-BRN"), 2: ("T.4", "BOTTOM POPPER", "02", "VIO-RED RED-BRN"),
	3: ("T.4", "AUTO PLUNGER", "03", "VIO-ORN RED-BRN"), 4: ("T.4", "TOP POPPER", "04", "VIO-YEL RED-BRN"),
	5: ("T.4", "DIVERTER POWER", "05", "VIO-GRN RED-BRN"), 6: ("T.4", "NOT USED", "06", "VIO-BLU RED-BRN"),
	7: ("T.4", "KNOCKER", "07", "VIO-BLK RED-BRN"), 8: ("T.4", "NOT USED", "08", "VIO-GRY RED-BLK"),
	9: ("T.4", "LEFT SLING", "09", "BRN-BLK RED-BLK"), 10: ("T.4", "RIGHT SLING", "10", "BRN-RED RED-BLK"),
	11: ("T.4", "LEFT JET", "11", "BRN-ORN RED-BLK"), 12: ("T.4", "TOP SLING", "12", "BRN-YEL RED-BLK"),
	13: ("T.4", "RIGHT JET", "13", "BRN-GRN RED-BLK"), 14: ("T.4", "EJECT", "14", "BRN-BLU RED-BLK"),
	15: ("T.4", "DIVERTER HOLD", "15", "BRN-VIO RED-BLK"), 16: ("T.4", "NOT USED", "16", "BRN-GRY RED-BLK"),
	33: ("T.4", "CLAW MAGNET", "33", "YEL-VIO RED-VIO"), 34: ("T.4", "NOT USED", "34", "ORN-VIO RED-VIO"),
	17: ("T.5", "CLAW FLASHER", "17", "BLK-BRN RED-WHT"), 21: ("T.5", "JETS FLASHER", "21", "BLU-GRN RED-WHT"),
	22: ("T.5", "SIDE RAMP", "22", "BLU-BLK RED-WHT"), 23: ("T.5", "LEFT RAMP UPPER", "23", "BLU-VIO RED-WHT"),
	24: ("T.5", "LEFT RAMP LOWER", "24", "BLU-GRY RED-WHT"), 25: ("T.5", "CAR CRASH CENTER", "25", "BLU-BRN RED-WHT"),
	26: ("T.5", "CAR CRASH LOWER", "26", "BLU-RED RED-WHT"), 27: ("T.5", "RIGHT RAMP", "27", "BLU-ORN RED-WHT"),
	28: ("T.5", "EJECT FLASHER", "28", "BLU-YEL RED-WHT"), 51: ("T.5", "CAR CRASH UPPER", "37", "BRN-WHT RED-WHT"),
	52: ("T.5", "LOWER REBOUND", "38", "BLK-WHT RED-WHT"), 53: ("T.5", "EYEBALL FLASHER", "39", "ORN-WHT RED-WHT"),
	54: ("T.5", "CENTER RAMP", "40", "YEL-WHT RED-WHT"), 55: ("T.5", "ELEVATOR FLASH 2", "41", "GRN-WHT RED-WHT"),
	56: ("T.5", "ELEVATOR FLASH 1", "42", "BLU-WHT RED-WHT"), 57: ("T.5", "DIVERTER FLASHER", "43", "VIO-WHT RED-WHT"),
	58: ("T.5", "RIGHT RAMP UPPER", "44", "GRY-WHT RED-WHT"),
	45: ("T.12", "R. FLIP. POWER", "01", "BLU-VIO BLU-YEL"), 46: ("T.12", "R. FLIP. HOLD", "02", "ORN-GRN BLU-YEL"),
	47: ("T.12", "L. FLIP. POWER", "03", "BLU-GRY GRY-YEL"), 48: ("T.12", "L. FLIP. HOLD", "04", "ORN-BLU GRY-YEL"),
	35: ("T.12", "U.L. FLIP. POWER", "07", "BLK-BLU GRY-YEL"), 36: ("T.12", "U.L. FLIP. HOLD", "08", "ORN-GRY GRY-YEL"),
}
SOLENOID_CALLBACKS = {
	1: "SolRelease (bsTrough.ExitSol_On, pulses switch 36)", 2: "BottomPopper.SolOut", 3: "AutoPlunge (kicks Kicker1)", 4: "bsTopPopper.SolOut",
	7: "vpmSolSound (knocker sound)", 14: "bsEject.SolOut", 15: "DiverterRight (moves the DiverterR flipper and swaps the diverter walls)",
	19: "SolClawMotorLeft (motor sound only; the claw cvpmMech reads 19 and 20 itself)", 33: "ClawMagnetOn",
	17: "Flash117 (SolModCallback)", 21: "Flash121 (SolModCallback)", 22: "Flash122 (SolModCallback)", 23: "Flash123 (SolModCallback)",
	24: "Flash124 (SolModCallback)", 25: "Flash125 (SolModCallback)", 26: "Flash126 (SolModCallback)", 27: "Flash127 (SolModCallback)",
	28: "Flash128 (SolModCallback)", 51: "Flash137 (SolModCallback)", 52: "Flash138 (SolModCallback)", 53: "Flash139 (SolModCallback)",
	54: "Flash140 (SolModCallback)", 55: "Flash141 (SolModCallback)", 56: "Flash142 (SolModCallback)", 57: "Flash143 (SolModCallback)",
	58: "Flash144 (SolModCallback)",
}
SOLENOID_NOTES = {
	1: "Releases the ball at the right end of the A-16765-1 Outhole Ball Trough toward the shooter lane; there is no separate outhole kicker, a drained ball rolls straight into the trough.",
	2: "Kicks the ball up out of the Bottom Popper (the A-17620 Chute Assembly under the 'Underground'/'Computer' shot, opto 76) back to the playfield; the Solenoid Wiring drawing labels the same box 'Bottom Plunger'.",
	3: "The auto plunger (A-14525 Kicker Bracket Assembly) that launches a ball resting on the shooter-lane switch 27; there is no manual plunger.",
	4: "Kicks the ball out of the Top Popper (A-17215 Ball Popper Assembly - Rear, AE-28-1500 coil) at the top of the playfield, opto 73.",
	5: "Power winding of the right-ramp diverter (A-17241 Ramp Diverter Assembly, coil A-15943-1 on the table, FL-11753-1 'Flipper Coil Assembly, Yellow' on the assembly page). Opening the diverter sends a right-ramp ball to the elevator and the Cryoclaw; the retained script registers no callback for 5 and moves the diverter from 15 alone.",
	7: "Knocker (B-10686-1) in the backbox: the table prints its voltage, drive and part only in the Backbox columns.",
	9: "Kicker-arm slingshot with its coil and bracket (A-17809); the ROM fires it from switch 41 (T.1 run).",
	10: "Kicker-arm slingshot (A-17809-1); the ROM fires it from switch 42.",
	11: "Jet bumper coil (A-9415-2); the ROM fires it from switch 43.",
	12: "The third slingshot, below the jets (A-17809); the ROM fires it from switch 44.",
	13: "Jet bumper coil (A-9415-2); the ROM fires it from switch 45.",
	14: "Kicks the ball out of the eject saucer (switch 66) beside the Retina Scan (B-9361-R Ball Eject Assembly, A-17809 coil and bracket).",
	15: "Hold winding of the right-ramp diverter (same A-17241 assembly as solenoid 5). The Cryoclaw theory: when the CPU detects a claw/elevator malfunction 'it will not open the diverter on the right ramp leading to the Cryoclaw/Elevator'; the errors 'Ramp Diverter Is Stuck Open/Closed' watch it.",
	17: "Claw flasher: one #906 flashlamp in a C-13337 assembly and one insert-panel #906 in the backbox (the table's Backbox columns). The location drawing puts its balloon above the playfield's top edge, on the back panel behind the claw.",
	18: "Elevator gear motor 14-7993 (A-17597 Elevator Assembly), through the A-15542 Motor EMI board; it runs one way only and the CPU pulses it to slow it.",
	19: "One of the two drive lines of the A-16120 D.C. Motor Control board for the Cryoclaw gear motor 14-7992 (A-16989); the board's J1-2 takes 'sol. 19'. 'Claw Left' is away from the elevator.",
	20: "The other drive line of the A-16120 D.C. Motor Control board (J1-1, 'sol. 20'); 'Claw Right' is toward the elevator.",
	21: "Jets flasher (#89 playfield bulb in an A-17803 assembly) plus a #906 insert-panel flashlamp in the backbox.",
	22: "Side ramp flasher (#89 playfield bulb, A-17983) plus a #906 backbox insert flasher. The ROM's T.5 prints 'SIDE RAMP'.",
	23: "Left ramp upper flasher: a #906 playfield flashlamp (the only #906 among 21-28 on the playfield) plus a #906 backbox insert flasher.",
	24: "Left ramp lower flasher (#89, A-17983) plus a #906 backbox insert flasher.",
	25: "Car chase centre flasher (#89, A-17803) plus a #906 backbox insert flasher; printed type 'Gen. Purpose'.",
	26: "Car chase lower flasher (#89, A-17803) plus a #906 backbox insert flasher; printed type 'Gen. Purpose'.",
	27: "Right ramp flasher (#89, A-17983) plus a #906 backbox insert flasher; printed type 'Gen. Purpose'.",
	28: "Eject flasher (#89, A-17983) plus a #906 backbox insert flasher; printed type 'Gen. Purpose'.",
	33: "The Fliptronic II upper-right flipper power drive, used as the claw electromagnet drive (flipper circuit diagram footnote: 'Upper right flipper power drive is used as the Claw magnet drive. Upper right flipper holding drive is not used.'). Coil SZ-33-3000 on the A-16989 Cryoclaw Assembly. The ROM's T.4 tests it as 'CLAW MAGNET'; the claw test's MAGNET ON holds it, 'on solidly for a short period and then pulsed for a longer period'. PinMAME's dm.c names the address sClawMagnet; because dmGameData sets no FLIP_SOL(FLIP_UR), core_getSol publishes the raw upper-right power bit here.",
	34: "Upper-right flipper hold drive (Q7, J902-4 Orange-Violet): the solenoid table prints 'Not Used' and the flipper footnote says the holding drive is not used; the ROM's T.4 still pulses public 34 and prints 'NOT USED'.",
	6: "Printed 'Not Used': driver Q66 with no voltage or drive connection. The ROM's T.4 pulses it and prints 'NOT USED'.",
	8: "Printed 'Not Used': driver Q70 with no connection. The ROM's T.4 pulses it and prints 'NOT USED'.",
	16: "Printed 'Not Used': driver Q44 with no connection. The ROM's T.4 pulses it and prints 'NOT USED'.",
}
# Fliptronic circuits: public address -> (stage, side, voltage, control connection, transistor, control wire, coil part, coil colour).
FLIPPER_COILS = {
	35: ("power", "Upper Left", "J907-8 (Red-Gry)", "J902-3", "Q1", "Yel-Gry", "FL-11630", "Red"),
	36: ("hold", "Upper Left", "J907-8 (Red-Gry)", "J902-1", "Q5", "Org-Gry", "FL-11630", "Red"),
	45: ("power", "Lower Right", "J907-1 (Red-Grn)", "J902-13", "Q4", "Yel-Grn", "FL-11629", "Blue"),
	46: ("hold", "Lower Right", "J907-1 (Red-Grn)", "J902-11", "Q11", "Org-Grn", "FL-11629", "Blue"),
	47: ("power", "Lower Left", "J907-4 (Red-Blu)", "J902-9", "Q3", "Yel-Blu", "FL-11629", "Blue"),
	48: ("hold", "Lower Left", "J907-4 (Red-Blu)", "J902-7", "Q9", "Org-Blu", "FL-11629", "Blue"),
}
PRINTED_FLIPPER_NUMBERS = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
VIRTUAL_SOLENOID_NOTES = {
	29: ("used", "WPC State Bit 29 (J111 GPIO mirror)", "core_getSol publishes solenoids2 bit 8 here, the remapped WPC GameOn/J111 GPIO state; dmGameData calls no wpc_set_fastflip_addr. Every Demolition Man harness run found it active from boot. Not a playfield device."),
	30: ("used", "WPC State Bit 30 (J111 GPIO mirror)", "core_getSol publishes solenoids2 bit 9 here, the second remapped J111 GPIO bit. No Demolition Man run found it active, which does not make it dead: the ROM can write it. Not a playfield device."),
	31: ("used", "WPC State Bit 31 (game-on mirror)", "The third remapped bit, which PinMAME documents as the game-on state; it was active in the service menu of every run and the retained table's cFastFlips enables its flippers from it (SolCallBack(31) = \"FastFlips.TiltSol\"). Not a relay on this machine."),
	32: ("unused", "Unused WPC State Channel 32", "PinMAME's WPC remap has no fourth state bit; public 32 is constant zero."),
}

# --- Lamp data ---------------------------------------------------------------------------------------
# address -> (manual label, bulb, lamp assembly). Labels are the lamp matrix's; the Lamp Locations list adds the bulb type.
LAMPS = {
	11: ("Ball Save", "24-8768 #555", "A-17898"), 12: ("Fortress Multiball", "24-8768 #555", "A-17898"),
	13: ("Museum Multiball", "24-8768 #555", "A-17898"), 14: ("Cryoprison Multiball", "24-8768 #555", "A-17898"),
	15: ("Wasteland Multiball", "24-8768 #555", "A-17898"), 16: ("Shoot Again", "24-6549 #44", "A-17807"),
	17: ("Access Claw", "24-6549 #44", "A-17807"), 18: ("Left Ramp Explode", "24-8768 #555", "A-17899"),
	21: ("Right Ramp Jackpot", "24-8768 #555", "A-17899"), 22: ("Right Loop Explode", "24-8768 #555", "A-17899"),
	23: ("Light Quick Freeze", "24-8768 #555", "A-17899"), 24: ("Freeze 4", "24-8768 #555", "A-17899"),
	25: ("Claw Ready", "24-8768 #555", "A-17899"), 26: ("Freeze 3", "24-8768 #555", "A-17899"),
	27: ("Freeze 2", "24-8768 #555", "A-17899"), 28: ("Freeze 1", "24-8768 #555", "A-17899"),
	31: ("Right Loop Jackpot", "24-8768 #555", "A-17899"), 32: ("Standup 5", "24-8768 #555", "A-17899"),
	33: ("Right Ramp Arrow", "24-8768 #555", "A-17899"), 34: ("Left Ramp Jackpot", "24-8768 #555", "A-17899"),
	35: ("Left Loop Jackpot", "24-8768 #555", "A-17899"), 36: ("Car Crash Top", "24-8768 #555", "A-17899"),
	37: ("Standup 1", "24-8768 #555", "A-17899"), 38: ("Car Crash Center", "24-8768 #555", "A-17899"),
	41: ("Right Ramp Explode", "24-8768 #555", "A-17899"), 42: ("Right Ramp Car Chase", "24-8768 #555", "A-17899"),
	43: ("Quick Freeze", "24-8768 #555", "A-17899"), 44: ("Left Ramp Car Chase", "24-8768 #555", "A-17899"),
	45: ("Extra Ball", "24-8768 #555", "A-17899"), 46: ("Start Multiball", "24-8768 #555", "A-17899"),
	47: ("Car Crash Bottom", "24-8768 #555", "A-17899"), 48: ("Left Loop Explode", "24-8768 #555", "A-17899"),
	51: ("Underground Arrow", "24-8768 #555", "A-17916"), 52: ("Underground Jackpot", "24-8768 #555", "A-17916"),
	53: ("Standup 2", "24-8768 #555", "A-17916"), 54: ("Left Ramp Arrow", "24-8768 #555", "A-17916"),
	55: ("Side Ramp Jackpot", "24-8768 #555", "A-17916"), 56: ("Side Ramp Arrow", "24-8768 #555", "A-17916"),
	57: ("Left Loop Arrow", "24-6549 #44", "A-17835"), 58: ("Center Ramp Jackpot", "24-6549 #44", "A-17807"),
	61: ('Claw "Capture Simon"', "24-8768 #555", "A-18056"), 62: ('Claw "Sup. Jets"', "24-8768 #555", "A-18056"),
	63: ('Claw "Prison Break"', "24-8768 #555", "A-18056"), 64: ('Claw "Freeze"', "24-8768 #555", "A-18056"),
	65: ('Claw "ACMAG"', "24-8768 #555", "A-18056"), 66: ("Middle Rollover", "24-8768 #555", "A-17624"),
	67: ("Top Rollover", "24-8768 #555", "A-17624"), 68: ("Lower Rollover", "24-8768 #555", "A-17624"),
	71: ('"Super Jackpot"', "24-8768 #555", None), 72: ('"Computer"', "24-8768 #555", "A-17272"),
	73: ('"Demo Time"', "24-8768 #555", "A-17272"), 76: ("Standup 4", "24-6549 #44", "A-17835"),
	77: ("Standup 3", "24-6549 #44", "A-17835"), 78: ("Retina Scan", "24-6549 #44", "A-17807"),
	81: ("Center Ramp Middle", "24-8768 #555", "A-17902"), 82: ("Center Ramp Outer", "24-8768 #555", "A-17902"),
	83: ("Center Ramp Inner", "24-8768 #555", "A-17902"), 84: ("Center Ramp Arrow", "24-6549 #44", "A-17807"),
	85: ("Right Loop Arrow", "24-6549 #44", "A-17835"), 86: ("Buy-in Button", None, "20-9663-9"),
	87: ("Ball Launch", None, "20-9663-B-4"), 88: ("Start Button", None, "20-9663-2"),
}
UNUSED_LAMPS = (74, 75)
LAMP_LIST_DIFFERENCES = {63: 'Claw "Prison. Break"', 66: '"M" Rollover', 67: '"T" Rollover', 68: '"L" Rollover'}
ROM_LAMP_NAMES = {
	11: "BALL SAVE", 12: '"FORTRESS MB"', 13: '"MUSEUM MB"', 14: '"CRYOPRISON MB"', 15: '"WASTELAND MB"', 16: '"SHOOT AGAIN"',
	17: '"ACCESS CLAW"', 18: 'L. RAMP "EXPLODE"', 21: 'R. RAMP "JACKPOT"', 22: 'R. LOOP "EXPLODE"', 23: '"LITE QU. FREEZE"',
	24: '"FREEZE" 4 (R)', 25: '"CLAW READY"', 26: '"FREEZE" 3', 27: '"FREEZE" 2', 28: '"FREEZE" 1 (L)', 31: 'R. LOOP "JACKPOT"',
	32: "STANDUP 5", 33: "R. RAMP ARROW", 34: 'L. RAMP "JACKPOT"', 35: 'L. LOOP "JACKPOT"', 36: "CAR CRASH TOP", 37: "STANDUP 1",
	38: "CAR CRASH CENTER", 41: 'R. RAMP "EXPLODE"', 42: "R. RAMP CAR CHASE", 43: '"QUICK FREEZE"', 44: "L. RAMP CAR CHASE",
	45: '"EXTRA BALL"', 46: '"START M. BALL"', 47: "CAR CRASH BOTTOM", 48: 'L. LOOP "EXPLODE"', 51: "UNDERG. ARROW",
	52: 'UNDERG. "JACKPOT"', 53: "STANDUP 2", 54: "L. RAMP ARROW", 55: 'S. RAMP "JACKPOT"', 56: "S. RAMP ARROW",
	57: "L. LOOP ARROW", 58: 'C. RAMP "JACKPOT"', 61: 'CLAW "CAPT. SIM."', 62: 'CLAW "SUP. JETS"', 63: 'CLAW "PR. BREAK"',
	64: 'CLAW "FREEZE"', 65: 'CLAW "ACMAG"', 66: "(M)TL ROLLOVER", 67: "M(T)L ROLLOVERR", 68: "MT(L) ROLLOVER",
	71: '"SUPER JACKPOT"', 72: '"COMPUTER"', 73: '"DEMO. TIME"', 74: "NOT USED", 75: "NOT USED", 76: "STANDUP 4", 77: "STANDUP 3",
	78: '"RETINA SCAN"', 81: "C. RAMP MIDDLE", 82: "C. RAMP OUTER (2)", 83: "C. RAMP INNER (2)", 84: "C. RAMP ARROW",
	85: "R. LOOP ARROW", 86: "BUY-IN BUTTON", 87: '"LAUNCH BALL"', 88: "START BUTTON",
}
TWO_BULB_LAMPS = {11: "the lamp drawing prints two balloons 11, one at each side of the centre insert stack", 82: "the centre-ramp light bar's balloons read 82, 83, 81, 83, 82, so 82 is the outer pair", 83: "the centre-ramp light bar's balloons read 82, 83, 81, 83, 82, so 83 is the inner pair"}
CABINET_LAMPS = {86: "cabinet.buy-in", 87: "cabinet.launch", 88: "cabinet.start"}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
# Row pins: the lamp matrix page prints J133-; the Power Driver Board connector list and the Section 3 reprint print J134- for the
# playfield branch (J133-7 to -9 are the cabinet branch of rows 6-8).
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J134-1", "Q90"), 2: ("Red-Black", "J134-2", "Q89"), 3: ("Red-Orange", "J134-4", "Q88"),
	4: ("Red-Yellow", "J134-5", "Q87"), 5: ("Red-Green", "J134-6", "Q86"), 6: ("Red-Blue", "J134-7", "Q85"),
	7: ("Red-Violet", "J134-8", "Q84"), 8: ("Red-Gray", "J134-9", "Q83"),
}
CABINET_ROW_PINS = {6: "J133-7", 7: "J133-8", 8: "J133-9"}

# --- General illumination ----------------------------------------------------------------------------
# public string -> (manual label, ROM T.6 name, return wire, playfield return/feed, backbox return/feed, cabinet return/feed, triac).
GI_STRINGS = {
	0: ("Back Panel G.I.", "BACK PANEL", "Wht-Brn", "J121-1 / J121-7", "J120-1 / J120-7", None, "Q18"),
	1: ("Upper Right G.I.", "UPPER RIGHT", "Wht-Org", "J121-2 / J121-8", "J120-2 / J120-8", None, "Q10"),
	2: ("Upper Left G.I.", "UPPER LEFT", "Wht-Yel", "J121-3 / J121-9", "J120-3 / J120-9", None, "Q14"),
	3: ("Lower Right G.I.", "LOWER RIGHT", "Wht-Grn", "J121-5 / J121-10", "J120-5 / J120-10", None, "Q16"),
	4: ("Lower Left G.I.", "LOWER LEFT", "Wht-Vio", "J121-6 / J121-11", "J120-6 / J120-11", "J119-3 / J119-1", "Q12"),
}
GI_TABLE_COLLECTIONS = {1: "GIString2", 2: "GIString3", 3: "GIString4", 4: "GIString5"}


# --- Shared helpers ------------------------------------------------------------------------------------
def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def _excerpt_digests() -> dict[str, str]:
	return {path.name: _file_sha256(path) for path in sorted(EXCERPT_ROOT.glob("*")) if path.is_file()}


EXCERPT_FILE_HASHES = _excerpt_digests()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Demolition Man retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Demolition Man extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Demolition Man retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Demolition Man retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Demolition Man retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(dict.fromkeys(source_refs))}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], status: str = "validated", **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier,
		"label": label,
		"kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability,
		"provenance": provenance(status, *refs),
	}
	device.update({key: value for key, value in extra.items() if value is not None})
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")


# --- Placements ----------------------------------------------------------------------------------------
def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Observed spatial record for one device from the committed placement seed, or None."""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append(
			{
				"id": f"{identifier}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": entry["x"],
				"y": entry["y"],
				"provenance": provenance("observed", VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE),
			}
		)
	return {"status": "observed", "placements": placements}


def _placement_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	parts = []
	for entry in entries:
		text = f"{entry['type']} {entry['object']}"
		if entry.get("projection"):
			text += f" (projection: {entry['projection']})"
		if entry.get("note"):
			text += f" ({entry['note']})"
		parts.append(text)
	return f" Placement from the retained table's {', '.join(parts)}." if parts else ""


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	if address in UNUSED_MATRIX_ADDRESSES:
		notes += " " + UNUSED_SWITCH_NOTES[address] + f" The ROM's T.1 SWITCH EDGES names public {address} 'NOT USED'."
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, EDGES_SOURCE, CONTROLLER_SOURCE) + ((VPX_SCRIPT_SOURCE,) if address == 75 else ()),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE, EDGES_SOURCE), **extra,
		)
	label, part, switch_type, role = SWITCHES[address]
	physical: dict[str, Any] = {"switch_type": switch_type}
	if part:
		physical["part_number"] = part
	printed = MATRIX_LABELS.get(address)
	notes += f' Switch Locations description "{label.split(" (")[0] if address in {25, 26, 63, 64, 65} else label}"'
	notes += f'; the Switch Matrix prints "{printed}".' if printed else "."
	notes += f' The ROM names it "{ROM_SWITCH_NAMES[address]}" in T.1 SWITCH EDGES.' if address in ROM_SWITCH_NAMES else ""
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
	if address in ROM_SWITCH_NAMES:
		refs += (EDGES_SOURCE,)
	if address in SWITCH_NOTES:
		notes += " " + SWITCH_NOTES[address]
	if address in STANDUP_TARGETS:
		notes += (
			" A stationary target: the Target Assemblies page (PDF 90, printed 2-34) draws all three of the machine's stationary target "
			"assemblies (A-17795-6, A-17799-6, A-18018-4; seven targets in all) with a leaf-contact stack and a diode."
		)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	if address in OPTO_SWITCHES:
		notes += (
			" Opto switch: the Switch Matrix page shades this cell 'Opto Switch', and PinMAME's dmGameData inverted-switch mask inverts this "
			"address. The manual's opto theory reads the receiver at 0.1-0.7 V with the beam unblocked and 11-13 V blocked, so the matrix "
			"contact is closed while the beam is clear. The ROM's T.1 names it at public 1 and clears the name at 0; through the mask public 1 "
			"is an open contact, a blocked beam, which is when the ROM reads it as active, so normally_closed is true."
		)
		if address in {25, 26, 67, 74}:
			notes += (
				" The ROM's T.14 CLAW TEST, which draws an X in a switch's box 'when the switch is activated (blocked)', marks it while public "
				f"{address} is 1 and clears it at 0."
			)
			refs += (CLAW_TEST_SOURCE,)
	elif address in ROM_SWITCH_NAMES and address != 24:
		notes += " The ROM's T.1 names it at public 1 and clears the name at public 0, an ordinary normally open contact."
	elif address == 22:
		notes += " The T.1 sweep left it released (the service buttons need the coin door open), so no run read its level."
	if role:
		extra["roles"] = [role]
	normally_closed = address in OPTO_SWITCHES or address == 24
	location = None
	if role and role.startswith("cabinet."):
		location = "cabinet" if address in {11, 12, 13, 23} else "cabinet interior"
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _placement_note("switch", address)
			refs += (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif address == 24:
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
	if location:
		physical["location"] = location
	physical["notes"] = notes
	return _device(identifier, label, "switch", SWITCH_GROUP, address, "used", refs, normally_closed=normally_closed, physical=physical, **extra)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE) + ((EDGES_SOURCE,) if address in {5, 7, 8} else ()),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}, wired through the A-17051-1 Coin Door Interface board. {note}"},
				wiring={"board": "WPC CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, switch_type, role, availability) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} ({wire}, {connection} on the Fliptronic II board)."
		refs: tuple[str, ...] = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"roles": [role],
			"wiring": {"board": "Fliptronic II board", "drive_wire": wire, "drive_connection": connection},
		}
		physical: dict[str, Any] = {}
		if address == 115:
			notes += (
				" Not used: the Switch Matrix marks it '*' (Not Used), the Switch Locations list prints 'Not Used' for its switch, and the flipper "
				"circuit diagram prints '*Not used on this game'; the upper-right flipper circuit drives the claw magnet instead. PinMAME does "
				"not synthesize this end-of-stroke bit: core.c selects the synthesized EOS bits through FLIP_EOS, which only FLIP_SOL supplies, and "
				"dmGameData's FLIP_SOL(FLIP_L | FLIP_UL) leaves the upper right out. In the T.1 run a host write of 1 read back as 1 (where 111, "
				"113 and 117 were overwritten to 0), and the ROM named nothing and fired nothing for it."
			)
			physical["location"] = "not installed"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif address == 116:
			notes += (
				" Not used: the Switch Matrix marks it '*', the Switch Locations list prints 'Not Used' and the flipper circuit diagram prints "
				"'*Not used on this game'. The right A-17316 Flipper Opto PCB (the same two-opto part as the left) has a second opto position that "
				"the Fliptronic connector lists wire to J905-3, but no retained page names an actuator for it. The ROM would treat it as a second "
				"right-flipper input: in the T.1 run a host write of 1 made the ROM fire the lower right flipper (45/46), exactly as for 112. "
				"The opto itself is fitted (the cabinet carries two A-17316 boards, each with two optos); what, if anything, interrupts it is "
				"not documented."
			)
			physical["location"] = "cabinet"
			physical["switch_type"] = "opto"
			physical["part_number"] = "A-17316"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif role.endswith(".button"):
			physical["switch_type"] = "opto"
			physical["location"] = "cabinet"
			physical["part_number"] = "A-17316"
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			fired = "45 and 46 (the lower right flipper)" if address == 112 else "47 and 48 together with 35 and 36 (the lower and upper left flippers)"
			notes += (
				" One opto of an A-17316 Flipper Opto PCB (two optos per board; the cabinet parts list fits two boards beside two red flipper "
				"buttons A-16883-4, and the rules page says the triggers on the gun handles also operate the flippers, through the "
				"handles' mechanical triggers 03-9015). No retained page says which actuator interrupts which opto. This generation's "
				"WPC_FLIPPERS read returns the complement of the flipper switch column, so the public state is already normalized: public 1 "
				f"is a pressed input and the contact the matrix sees is open at rest. In the T.1 run a host write of 1 made the ROM fire {fired}."
			)
			if address in {112, 114}:
				notes += f" The retained table's wpc.vbs library writes it from the {'right' if address == 112 else 'left'} flipper key (swLRFlip = 112, swLLFlip = 114)."
				refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				notes += (
					" The ROM fires the same left flippers for 114 and 118, so the upper-left cabinet opto is a second input for the left side; "
					"the retained table never writes 118 (wpc.vbs writes it only from a staged flipper key with an upper-left solenoid "
					"registered, and this table's flipper keys call cFastFlips, which drives the lower and upper left flipper objects together)."
				)
				refs += (VPM_LIBRARY_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			physical["switch_type"] = "leaf"
			physical["location"] = "flipper assembly"
			physical["part_number"] = "SW-1A-193" if address == 117 else "SW-1A-194"
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
			notes += (
				" End-of-stroke switch on the flipper assembly; the maintenance pages say the Fliptronic II end-of-stroke switches are "
				"normally open and close when the flipper is energized. PinMAME synthesizes this address from the flipper coil state after "
				"the flip stroke time, and in the T.1 run a host write was overwritten to 0, so its public level is not a measurement of the "
				"physical contact."
			)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, availability, refs, **extra))
	for address in range(1, 9):
		dip_note = (
			"WPC CPU-board DIP bank. The manual's Country DIP Switch Chart prints Sw4-Sw8 only: American On On On On On, European On On Off On On, "
			"French On On On Off Off, German On On On On Off, Spanish On Off On On On (Sw4 to Sw8)."
			if address >= 4
			else "WPC CPU-board DIP bank; the manual's Country DIP Switch Chart prints no setting for Sw1-Sw3."
		)
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP {address} (country/option configuration bit)", "dip_switch", DIP_GROUP, address,
				"used" if address >= 4 else "optional", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"Sw{address}"}],
				physical={"location": "WPC CPU board", "switch_type": "dip", "notes": dip_note},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Outputs -------------------------------------------------------------------------------------------
def _rom_note(address: int) -> tuple[str, tuple[str, ...]]:
	if address not in ROM_OUTPUT_NAMES:
		return "", ()
	test, name, number, wires = ROM_OUTPUT_NAMES[address]
	source = {"T.4": SOLENOID_TEST_SOURCE, "T.5": FLASHER_TEST_SOURCE, "T.12": FLIPPER_TEST_SOURCE}[test]
	title = {"T.4": "SOLENOID TEST", "T.5": "FLASHER TEST", "T.12": "FLIPPER COIL"}[test]
	return f' {test} {title}: the ROM pulses public {address} and prints "{name}", number {number}, wires {wires}.', (source,)


def _solenoid_wiring(address: int) -> dict[str, Any]:
	_, _, voltage, transistor, drive, wire, _, _ = SOLENOID_TABLE[address]
	wiring: dict[str, Any] = {"board": "WPC power driver board", "driver_transistor": transistor, "control_wire": wire}
	if drive:
		wiring["control_connection"] = drive
	if voltage:
		wiring["power_connection"] = voltage
	return wiring


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 59):
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		if 1 <= address <= 28:
			if address in NOT_USED_SOLENOIDS:
				function, printed_type, _, transistor, _, wire, _, _ = SOLENOID_TABLE[address]
				rom, rom_refs = _rom_note(address)
				items.append(
					_device(
						output_id(NOT_USED_SOLENOIDS[address]), NOT_USED_SOLENOIDS[address], "coil", SOLENOID_GROUP, address, "unused",
						(MANUAL_SOURCE, CORE_SOURCE) + rom_refs,
						aliases=aliases + [{"namespace": "manual.address", "value": f"{address:02d}"}],
						physical={"notes": f"Printed solenoid table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire}). {SOLENOID_NOTES[address]}{rom}"},
						wiring=_solenoid_wiring(address), spatial=not_applicable("unused", MANUAL_SOURCE),
					)
				)
				continue
			function, printed_type, voltage, transistor, drive, wire, part, assembly = SOLENOID_TABLE[address]
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("motor" if address in {18, 19, 20} else "coil")
			physical: dict[str, Any] = {}
			if part and kind != "flasher":
				physical["part_number"] = part
			if assembly:
				physical["assembly_part_number"] = assembly
			if address in BACKBOX_FLASHER_SOLENOIDS:
				physical["quantity"] = 2
			notes = f'Printed solenoid table entry {address:02d} "{function}" ({printed_type or "no printed type"}, driver {transistor}, wire {wire}).'
			if kind == "flasher":
				notes += f" Printed flashlamps: {part}."
			notes += " " + SOLENOID_NOTES[address]
			rom, rom_refs = _rom_note(address)
			notes += rom
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE) + rom_refs
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
				refs += (VPX_SCRIPT_SOURCE,)
			elif address in {9, 10, 11, 12, 13}:
				notes += " The retained script registers no callback for it: the table's slingshot and bumper objects kick on their own."
				refs += (VPX_SCRIPT_SOURCE, EDGES_SOURCE)
			elif address == 20:
				notes += " The retained script registers no callback for it; its claw cvpmMech reads 19 and 20 directly."
				refs += (VPX_SCRIPT_SOURCE,)
			elif address == 18:
				notes += " The retained script's elevator cvpmMech (sol1 = 18) reads it; no SolCallback is registered."
				refs += (VPX_SCRIPT_SOURCE,)
			elif address == 5:
				refs += (VPX_SCRIPT_SOURCE,)
			if address in {18, 19, 20}:
				refs += (CLAW_FUNCTIONS_SOURCE,)
				notes += {
					18: " The ROM's T.14 CLAW TEST drives it for AUTO RUN, RUN ELEVATOR and PARK ELEVATOR.",
					19: " The ROM's T.14 CLAW RIGHT function drives 19 and 20 together; the manual pulses the claw motor 'to vary the speed of the claw arm'.",
					20: " The ROM's T.14 CLAW RIGHT function drives 19 and 20 together.",
				}[address]
			extra: dict[str, Any] = {"aliases": aliases + [{"namespace": "manual.address", "value": f"{address:02d}"}], "wiring": _solenoid_wiring(address)}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, identifier, role)
				if spatial:
					extra["spatial"] = spatial
					notes += _placement_note("solenoid", address)
					refs += (VPX_TABLE_SOURCE,)
				elif address == 17:
					notes += " No placement: the retained table models it only with glow sprites (Flasher f17, f117), and a sprite is not a socket."
				if address in BACKBOX_FLASHER_SOLENOIDS:
					notes += " Only the playfield flashlamp is placed; the second bulb is the backbox insert flasher."
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(identifier, label, kind, SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		if 29 <= address <= 32:
			availability, label, note = VIRTUAL_SOLENOID_NOTES[address]
			refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((EDGES_SOURCE, SOLENOID_TEST_SOURCE) if availability == "used" else ())
			if address == 31:
				refs += (VPX_SCRIPT_SOURCE,)
			items.append(
				_device(
					output_id(label), label, "virtual", SOLENOID_GROUP, address, availability, refs, aliases=aliases,
					roles=["internal.wpc-state"] if availability == "used" else ["internal.unused.wpc-output"],
					physical={"notes": note}, spatial=not_applicable("virtual", CORE_SOURCE),
				)
			)
			continue
		if address in {33, 34}:
			rom, rom_refs = _rom_note(address)
			if address == 33:
				identifier = output_id(SOLENOID_LABELS[33])
				notes = SOLENOID_NOTES[33] + rom + " Retained script callback: ClawMagnetOn (shows the ball on the claw while BallinClaw is set, drops it from the claw position on release)."
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, CLAW_FUNCTIONS_SOURCE, VPX_TABLE_SOURCE) + rom_refs
				extra = {
					"aliases": aliases + [{"namespace": "manual.address", "value": "33"}],
					"physical": {"part_number": "SZ-33-3000", "assembly_part_number": "A-16989", "notes": notes + _placement_note("solenoid", 33)},
					"wiring": {"board": "Fliptronic II controller board", "driver_transistor": "Q2", "control_connection": "J902-6", "control_wire": "Yel-Vio", "power_connection": "J907-6 (Red-Vio)"},
				}
				spatial = located("solenoid", 33, identifier, "effect")
				if spatial:
					extra["spatial"] = spatial
				items.append(_device(identifier, SOLENOID_LABELS[33], "magnet", SOLENOID_GROUP, 33, "used", refs, **extra))
			else:
				label = NOT_USED_SOLENOIDS[34]
				items.append(
					_device(
						output_id(label), label, "coil", SOLENOID_GROUP, 34, "unused", (MANUAL_SOURCE, CORE_SOURCE) + rom_refs,
						aliases=aliases + [{"namespace": "manual.address", "value": "34"}],
						physical={"notes": SOLENOID_NOTES[34] + rom},
						wiring={"board": "Fliptronic II controller board", "driver_transistor": "Q7", "control_connection": "J902-4", "control_wire": "Org-Vio", "power_connection": "J907-6 (Red-Vio)"},
						spatial=not_applicable("unused", MANUAL_SOURCE),
					)
				)
			continue
		if address in FLIPPER_COILS:
			stage, side, voltage, control, transistor, control_wire, part, colour = FLIPPER_COILS[address]
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			rom, rom_refs = _rom_note(address)
			notes = (
				f"{side} flipper {stage} winding on the Fliptronic II board (driver {transistor}, {control}, {control_wire}); coil {part} ({colour}). "
				f"The manual numbers this circuit ({PRINTED_FLIPPER_NUMBERS[address]}); PinMAME publishes it at {address}.{rom}"
			)
			if side == "Upper Left":
				notes += " The ROM fires it together with the lower left flipper from either left cabinet input (114 or 118); the retained table's cFastFlips moves LeftFlipper1 together with LeftFlipper from the left flipper key."
			else:
				notes += f" The retained table drives its {'RightFlipper' if side == 'Lower Right' else 'LeftFlipper'} object through cFastFlips, which bypasses PinMAME's flipper callbacks and enables the flippers from public 31."
			extra = {
				"aliases": aliases + [{"namespace": "manual.address", "value": PRINTED_FLIPPER_NUMBERS[address]}],
				"physical": {"part_number": part, "assembly_part_number": {"Upper Left": "A-14876-L", "Lower Right": "A-15849-R-2", "Lower Left": "A-15849-L-2"}[side]},
				"wiring": {"board": "Fliptronic II controller board", "driver_transistor": transistor, "control_connection": control, "control_wire": control_wire, "power_connection": voltage},
			}
			spatial = located("solenoid", address, identifier, "effect")
			if spatial:
				extra["spatial"] = spatial
				notes += _placement_note("solenoid", address)
			extra["physical"]["notes"] = notes
			items.append(_device(identifier, label, "coil", SOLENOID_GROUP, address, "used", (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE, EDGES_SOURCE) + rom_refs, **extra))
			continue
		if 37 <= address <= 44:
			label = f"Unused WPC-DCS Output {address}"
			items.append(
				_device(
					output_id(label), label, "virtual", SOLENOID_GROUP, address, "unused", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases,
					roles=["internal.unused.wpc-output"],
					physical={"notes": (
						"This WPC-DCS generation has no integrated LPDC board, so pinned PinMAME's core_getSol serves 37-44 only for WPC-95 and "
						f"System 11 and returns nothing here. The manual's auxiliary 8-driver flasher printed {address} is public {address + 14} (T.5 run)."
					)},
					spatial=not_applicable("virtual", CORE_SOURCE),
				)
			)
			continue
		if address in {49, 50}:
			label = "PinMAME Simulator Ball-Shooter Channel" if address == 49 else "Reserved WPC Output 50"
			note = (
				"PinMAME's simulator-only ball-shooter channel; Demolition Man's real launcher is the auto plunger at public 3."
				if address == 49 else "Reserved position before the first custom output (CORE_FIRSTCUSTSOL = 51)."
			)
			items.append(
				_device(output_id(label), label, "virtual", SOLENOID_GROUP, address, "unused", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases,
					roles=["internal.unused.wpc-output"], physical={"notes": note}, spatial=not_applicable("virtual", CORE_SOURCE))
			)
			continue
		if address in AUX_FLASHERS:
			printed, function, transistor, connection, wire, lamp, assembly, count = AUX_FLASHERS[address]
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			rom, rom_refs = _rom_note(address)
			notes = (
				f'Printed solenoid table entry {printed}* "{function}" (printed type Low Power, driver {transistor} on the auxiliary 8-Driver '
				f"board, {connection}, wire {wire}, flashlamp {lamp} ({count})); the footnote reads '*Note: Controlled from the 8-Driver Board, not the "
				"Power Driver Board'. Pinned dm.c's dm_getSol publishes WPC_EXTBOARD1 bit "
				f"{address - 51} as custom output CORE_CUSTSOLNO({address - 50}) = public {address}, and init_dm calls wpc_set_modsol_aux_board(1).{rom}"
			)
			if address == 55:
				notes += " The location drawing puts two balloons 41 above the playfield's top edge, on the back panel either side of the elevator, matching the printed count (2)."
			if address in {55, 56}:
				notes += " No placement: the retained table models it only with glow sprites (Flasher f141/f141a/f141b or f142/f142b), and a sprite is not a socket."
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) + rom_refs
			extra = {
				"aliases": aliases + [{"namespace": "manual.address", "value": str(printed)}],
				"physical": {"quantity": count},
				"wiring": {"board": "A-16100-2 auxiliary 8-driver board", "driver_transistor": transistor, "control_connection": connection, "control_wire": wire, "power_connection": "J107-6"},
			}
			if assembly:
				extra["physical"]["assembly_part_number"] = assembly
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			spatial = located("solenoid", address, identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
				notes += _placement_note("solenoid", address)
				refs += (VPX_TABLE_SOURCE,)
			extra["physical"]["notes"] = notes
			items.append(_device(identifier, label, "flasher", SOLENOID_GROUP, address, "used", refs, **extra))
			continue
		label = f"Unused WPC-DCS Output {address}"
		items.append(
			_device(output_id(label), label, "virtual", SOLENOID_GROUP, address, "unused", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases,
				roles=["internal.unused.wpc-output"], physical={"notes": "No WPC-DCS output is published here: the upper-flipper and lower-flipper circuits and the custom range are at other addresses."},
				spatial=not_applicable("virtual", CORE_SOURCE))
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
			if address in CABINET_LAMPS:
				drive_connection, return_connection = "J136-3", CABINET_ROW_PINS[row]
			wiring = {
				"board": "WPC power driver board", "drive_wire": drive_wire, "drive_connection": drive_connection,
				"return_wire": return_wire, "return_connection": return_connection,
				"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
			}
			aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
			notes = f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire})."
			if address in UNUSED_LAMPS:
				notes += f" The lamp matrix and the Lamp Locations list print Not Used, and the ROM's T.8 SINGLE LAMPS names public {address} 'NOT USED'."
				items.append(
					_device(identifier, f"Not Used Lamp {address}", "lamp", LAMP_GROUP, address, "unused", (MANUAL_SOURCE, LAMP_TEST_SOURCE, CORE_SOURCE),
						aliases=aliases, physical={"notes": notes}, wiring=wiring, spatial=not_applicable("unused", MANUAL_SOURCE))
				)
				continue
			label, bulb, assembly = LAMPS[address]
			physical: dict[str, Any] = {"quantity": 2 if address in TWO_BULB_LAMPS else 1, "assembly_part_number": assembly} if assembly else {"quantity": 2 if address in TWO_BULB_LAMPS else 1}
			notes += f' Lamp matrix label "{label}".'
			if address in LAMP_LIST_DIFFERENCES:
				notes += f' The Lamp Locations list prints "{LAMP_LIST_DIFFERENCES[address]}".'
			if bulb:
				notes += f" Printed bulb {bulb}."
			if address == 71:
				notes += " The Lamp Locations list prints no lamp assembly for it."
			notes += f' T.8 SINGLE LAMPS lights public {address} and prints "{ROM_LAMP_NAMES[address]}".'
			if address in TWO_BULB_LAMPS:
				notes += f" Two bulbs: {TWO_BULB_LAMPS[address]}."
			if address == 83:
				notes += " The retained table's fader drives the inner pair (l83, l83a) from lamp 82 and never reads lamp 83, a table defect; the inner inserts are placed from those lights."
			if address == 82:
				notes += " The retained table's fader drives all four centre-ramp inserts from this lamp (see lamp 83)."
			if address in {71, 72, 73}:
				notes += (
					" The lamp drawing shows 71, 72 and 73 as one stacked three-lamp bar near the centre of the upper playfield, with a single leader. "
					"The retained table renders them only as Flasher sprites (f71, f72, f73), which are not sockets, so no placement is recorded."
				)
			if address in {61, 62, 63, 64, 65}:
				notes += " One of the five claw-goal lamps beside the Cryoclaw's drop positions."
			refs: tuple[str, ...] = (MANUAL_SOURCE, LAMP_TEST_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			extra: dict[str, Any] = {"aliases": aliases, "wiring": wiring}
			if address in CABINET_LAMPS:
				notes += (
					" Cabinet button lamp: the Power Driver Board connector list sends lamp column 8 'to cabinet' on J136-3 and rows 7 and 8 'to cabinet' "
					"on J133-8/J133-9, and prints row 6's J133-7 'not used' although the Coin Door Interface list takes that Red-Blue wire to its cabinet "
					"lamps (wiring detail kept in the excerpts)."
				)
				extra["roles"] = [CABINET_LAMPS[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
					notes += _placement_note("lamp", address)
					refs += (VPX_TABLE_SOURCE,)
			physical["notes"] = notes + (
				" The lamp matrix page prints this row's connector as J133-; the Power Driver Board connector list and the Section 3 reprint print J134- "
				"for the playfield branch, which the wiring here follows."
				if address not in CABINET_LAMPS else ""
			)
			extra["physical"] = physical
			items.append(_device(identifier, label, "lamp", LAMP_GROUP, address, "used", refs, **extra))
	return items


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, rom_name, wire, playfield, backbox, cabinet, transistor) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = (
			f"Printed general-illumination string {address + 1:02d} ({label}): printed bulbs #44 on the playfield and #555 in the backbox, "
			f"wire {wire}, triac driver {transistor}; return/feed pins {playfield} toward the playfield and {backbox} toward the backbox"
			+ (f" and {cabinet} toward the coin door." if cabinet else ".")
			+ f' The ROM\'s T.6 GEN\'L. ILLUM. steps the brightness of public G.I. {address} under the name "{rom_name}".'
		)
		refs: tuple[str, ...] = (MANUAL_SOURCE, GI_TEST_SOURCE, CORE_SOURCE)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{address + 1:02d}"}],
			"wiring": {"board": "WPC power driver board", "driver_transistor": transistor, "control_connection": ", ".join(item for item in (playfield, backbox, cabinet) if item)},
		}
		if address in GI_TABLE_COLLECTIONS:
			notes += (
				f" The retained table's UpdateGI drives collection {GI_TABLE_COLLECTIONS[address]} for this string (wpc.vbs passes zero-based string numbers); "
				"the placements are that collection's Light objects with co-located render doubles collapsed, kept observed and without a quantity "
				"because the manual prints no per-string bulb count and no drawing locates G.I. bulbs."
			)
			refs += (VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE)
			spatial = located("gi", address, identifier, "emitter")
			if spatial:
				extra["spatial"] = spatial
		else:
			notes += (
				" The back panel is the panel standing at the rear of the playfield. The retained table's UpdateGI has no case for string 0, so the "
				"table models none of its bulbs and no placement is recorded."
			)
			refs += (VPX_SCRIPT_SOURCE,)
		extra["physical"] = {"notes": notes}
		items.append(_device(identifier, label, "gi", GI_GROUP, address, "used", refs, **extra))
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
			"physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE, EDGES_SOURCE),
		}
	]


# --- Mechanisms, relationships, drivers ----------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _matrix(*addresses: int) -> list[str]:
	return [f"switch.matrix-{address}" for address in addresses]


def _mechanism(suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...], positions: list[tuple[str, str, list[str], str]] | None = None, assembly: str | None = None, status: str = "observed") -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}",
		"label": label,
		"kind": kind,
		"actuators": actuators,
		"sensors": sensors,
		"behavior": behavior,
		"provenance": provenance(status, *refs),
	}
	if assembly:
		record["assembly_part_number"] = assembly
	if positions:
		record["positions"] = [
			{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
			for position_id, position_label, position_sensors, description in positions
		]
	return record


def mechanisms() -> list[dict[str, Any]]:
	claw_refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, CLAW_TEST_SOURCE, CLAW_FUNCTIONS_SOURCE)
	return [
		_mechanism(
			"cryoclaw", "Cryoclaw", "motorized", [_coil(19), _coil(20), _coil(33)], _matrix(25, 26),
			"The A-16989 Cryoclaw Assembly is a swinging arm on a reversible 12 V DC gear motor (14-7992) with an electromagnet "
			"(SZ-33-3000) at its end. The A-16120 D.C. Motor Control board takes two drive lines, solenoid 19 (printed 'Claw Motor Left', "
			"away from the elevator) and solenoid 20 ('Claw Motor Right', toward the elevator); the CPU pulses them to vary the arm's speed, "
			"and in the T.14 run its CLAW RIGHT function drove 19 and 20 together (pinned dm.c's P-ROC notes say the game 'pulses the drive by "
			"enabling both Claw Right and Claw Left' and record 1.15 s for a full swing). The magnet is the Fliptronic upper-right flipper "
			"power drive (public 33). The A-16986 Cryoclaw Opto PCB reads the arm with two optos, switch 25 (Claw Position 1, Claw Right) and "
			"26 (Claw Position 2, Claw Left). The manual's state table: Right blocked with Left open, arm at right above the elevator; Right "
			"open with Left blocked, arm at left; both open, within range; both blocked, out of range, when the CPU will not run the motor (a "
			"disconnected opto reads the same way). The ROM reads a blocked position opto as active at public 1 (T.14 marks it). A cycle: the "
			"arm moves right over the elevator, the magnet comes on, the elevator lifts the ball to it, the arm swings left under player "
			"control (flipper buttons or triggers) and releasing the magnet drops the ball onto one of five goal lanes (switches 81-85). In "
			"multiball and ball search the CPU runs it automatically, and after a detected fault it keeps the right-ramp diverter closed. The "
			"retained script models the arm as a two-solenoid cvpmMech (sol1 = 19, sol2 = 20, 147 steps) with switches 25 at 0-2 and 26 at "
			"140-147, and releases the ball at the drop kicker matching the arm's angle.",
			claw_refs,
			[
				("right", "Arm at right (over the elevator)", _matrix(25), "Claw Right (25) active, Claw Left (26) inactive: pick-up position."),
				("left", "Arm at left (away from the elevator)", _matrix(26), "Claw Left (26) active, Claw Right (25) inactive: far end of travel."),
			],
			"A-16989",
		),
		_mechanism(
			"elevator", "Elevator", "motorized", [_coil(18)], _matrix(67, 74),
			"The A-17597 Elevator Assembly lifts a ball from the end of the right-ramp diverter path to the Cryoclaw. Its 14-7993 gear motor "
			"(solenoid 18, through the A-15542 Motor EMI board) runs in one direction only, and the CPU pulses it to slow it. The single "
			"Elevator Index opto (switch 67, A-17596 Elevator Opto PCB) detects the DOWN position; because of the motor's inertia it normally "
			"stops with the actuator just past the index. The Elevator Hold opto (switch 74, on the 7-Opto board) sees a ball waiting on the "
			"elevator; pinned dm.c notes it also reads active while the elevator rises without a ball, and that the game expects Hold to clear "
			"shortly before Index sets when lowering an empty elevator. 'Magnet Broken' is raised when the claw fails to take the ball off "
			"the elevator (magnet or Elevator Hold at fault); 'Elevator Broken' when the index opto or the motor fails. The T.14 functions "
			"RUN ELEVATOR and PARK ELEVATOR drive 18 ('Park Elevator runs the elevator motor until the elevator index'). The retained script "
			"models it as a one-solenoid cvpmMech (sol1 = 18, reversing, 70 steps) with 67 at 0-2 and 74 at 65-70, and sets 74 when a ball "
			"enters ElevatorKicker.",
			claw_refs,
			[
				("down", "Down (index)", _matrix(67), "Elevator Index active: the elevator is down and can take a ball."),
				("ball-held", "Ball on the elevator", _matrix(74), "Elevator Hold active: a ball is waiting on the elevator (or the elevator is rising)."),
			],
			"A-17597",
		),
		_mechanism(
			"right-ramp-diverter", "Right-ramp diverter", "diverter", [_coil(5), _coil(15)], _matrix(46, 47),
			"The A-17241 Ramp Diverter Assembly on the right ramp: a flipper-style coil (A-15943-1 on the solenoid table, FL-11753-1 'Flipper "
			"Coil Assembly, Yellow' on the assembly page) with a power winding (solenoid 5, Diverter Power, high power) and a hold winding "
			"(solenoid 15, Diverter Hold, low power) moves an A-16636 plunger. Open, it sends a right-ramp ball (Right Ramp Enter 46) to the "
			"elevator and Cryoclaw; closed, the ball runs on down the right ramp (Right Ramp Exit 47). The CPU keeps it closed while the claw "
			"is faulted or disabled, and reports 'Ramp Diverter Is Stuck Open' or 'Stuck Closed'. The Diverter Flasher (public 57) sits beside "
			"it. The retained script moves its DiverterR flipper from solenoid 15 only.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, CORE_SOURCE),
			None, "A-17241",
		),
		_mechanism(
			"claw-goals", "Cryoclaw goal lanes", "other", [], _matrix(81, 82, 83, 84, 85),
			"Five goals under the Cryoclaw's swing, each a rollover the dropped ball crosses: Capture Simon (81), Super Jets (82), Prison Break "
			"(83), Freeze (84) and ACMAG (85), lit by lamps 61-65. A Capture Simon ball runs on to the bottom popper. The rules: load the claw by "
			"shooting the right ramp when the diverter is open, move the claw with the flipper buttons or the gun trigger, and drop the ball with "
			"the launch button or the gun buttons.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE),
		),
		_mechanism(
			"ball-trough", "Ball trough", "kicker", [_coil(1)], _matrix(31, 32, 33, 34, 35, 36),
			"The A-16765-1 Outhole Ball Trough holds the five balls on the A-17982/A-17981 7 Ball Trough LED and Photo Transistor boards: optos "
			"31-35 count them (the ROM calls 31 the right end and 35 the left end) and Trough Jam (36) sits at the exit. A drained ball rolls "
			"straight into the trough (there is no outhole kicker) and the Ball Release coil (solenoid 1, AE-26-1500) kicks one into the "
			"shooter lane. The manual's assembly pages call it a 5-ball game, although one error passage says the game 'normally uses six balls'.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE),
			[
				("trough-1", "Trough 1 (exit)", _matrix(31), "A ball at the release end."),
				("trough-5", "Trough 5 (entry)", _matrix(35), "A ball at the drain end: the trough is full."),
				("jam", "Trough Jam", _matrix(36), "A ball jammed at the release."),
			],
			"A-16765-1",
		),
		_mechanism(
			"auto-plunger", "Auto plunger and launch buttons", "kicker", [_coil(3)], _matrix(27, 11, 12),
			"There is no manual plunger: the A-14525 Kicker Bracket auto plunger (solenoid 3) launches the ball resting on the shooter-lane "
			"switch 27 when the player presses the cabinet Launch Ball button or a handle thumb button (switch 11; the left handle's button is "
			"12), and the ROM also launches automatically. A launched ball feeds the upper left flipper by way of the right loop.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE, CORE_SOURCE),
			None, "A-14525",
		),
		_mechanism(
			"top-popper", "Top popper", "kicker", [_coil(4)], _matrix(73),
			"The A-17215 Ball Popper Assembly - Rear at the top of the playfield: a ball drops onto the opto pair (switch 73) and the AE-28-1500 "
			"coil (solenoid 4) pops it back out toward the M-T-L lanes.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "A-17215",
		),
		_mechanism(
			"bottom-popper", "Bottom popper (Underground / Computer)", "kicker", [_coil(2)], _matrix(76),
			"The A-17620 Chute Assembly under the Underground shot: a ball entering it (or dropped at Capture Simon) rests on the opto (switch 76) "
			"and the AE-23-800 coil (solenoid 2) kicks it up and out to the right inlane wireform.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "A-17620",
		),
		_mechanism(
			"eject", "Eject saucer", "kicker", [_coil(14)], _matrix(66),
			"A saucer on the left side (switch 66) beside the Retina Scan; the B-9361-R Ball Eject Assembly (solenoid 14) kicks the ball out "
			"toward the left inlane.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SOLENOID_TEST_SOURCE),
			None, "B-9361-R",
		),
		_mechanism(
			"car-chase", "Car chase", "toy", [], _matrix(71, 72, 87),
			"Two Matchbox cars (an Olds 442 and a GM Ultralite, IPDB: 'used like sequential captive balls') sit in the Opto Car Tunnel "
			"(A-17644) on the left; the ball pushes the first car up the tunnel into the second, and each car breaks an opto of the 7-Opto board "
			"(switches 71 and 72, Car Crash 1 and 2) before the Car Chase Standup (87) at the tunnel's end. The cars fall back to rest. The "
			"retained script models each car as a hidden captive ball and holds 71/72 at 0 while the car rests on its trigger.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, IDENTITY_SOURCE, EDGES_SOURCE),
		),
		_mechanism(
			"retina-scan", "Retina Scan eyeball", "toy", [], _matrix(77),
			"A custom captive ball (the eyeball, part 20-9935) behind the Retina Scan shot strikes the Eyeball Standup (switch 77) when hit; "
			"lamp 78 lights the Retina Scan insert and the Eyeball Flasher (public 53) flashes it. The retained script models it as a "
			"cvpmCaptiveBall with a spinning eyeball primitive.",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, IDENTITY_SOURCE),
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)], ["switch.generic-111", "switch.generic-112"],
			"Fliptronic II flipper A-15849-R-2 with an FL-11629 coil (power 45 / hold 46, Q4/Q11) and a SW-1A-194 end-of-stroke switch (F1, "
			"public 111, synthesized by PinMAME). Its cabinet input is F2 (public 112) on the right A-17316 opto board; in the T.1 run 112 and "
			"the unused F6 position (116) each made the ROM fire it.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE), None, "A-15849-R-2",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)], ["switch.generic-113", "switch.generic-114"],
			"Fliptronic II flipper A-15849-L-2 with an FL-11629 coil (power 47 / hold 48, Q3/Q9) and a SW-1A-194 end-of-stroke switch (F3, "
			"public 113, synthesized). Its cabinet input is F4 (public 114); the ROM fires it together with the upper left flipper from 114 or 118.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE), None, "A-15849-L-2",
		),
		_mechanism(
			"upper-left-flipper", "Upper left flipper", "other", [_coil(35), _coil(36)], ["switch.generic-117", "switch.generic-118"],
			"An upper left flipper (A-14876-L) with an FL-11630 coil (power 35 / hold 36, Q1/Q5) and a SW-1A-193 end-of-stroke switch (F7, public "
			"117). It flips with the lower left flipper: the ROM fires 35/36 with 47/48 from either left cabinet input (114, 118). The Upper Left "
			"Flipper Gate switch (86) is at its loop. There is no upper right flipper; that circuit drives the claw magnet.",
			(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE), None, "A-14876-L",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(9), _coil(10), _coil(12)], _matrix(41, 42, 44),
			"Three A-17809 kicker-arm slingshots: left (switch 41, solenoid 9), right (42, 10) and top, below the jet bumpers (44, 12). Each has "
			"an A-17801 count switch and a SW-1A-120 score switch with a diode across it. The ROM fires each coil from its switch (T.1 run).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "A-17809",
		),
		_mechanism(
			"jet-bumpers", "Jet bumpers", "other", [_coil(11), _coil(13)], _matrix(43, 45),
			"Two B-9414 jet bumpers with A-9415-2 coil assemblies: left (switch 43, solenoid 11) and right (45, 13). The ROM fires each coil from "
			"its switch (T.1 run).",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE), None, "A-9415-2",
		),
	]


def relationships() -> list[dict[str, Any]]:
	pairs = ((41, 9, "left-slingshot"), (42, 10, "right-slingshot"), (44, 12, "top-slingshot"), (43, 11, "left-jet-bumper"), (45, 13, "right-jet-bumper"))
	return [
		{
			"id": f"relationship.{name}-kick",
			"kind": "pulse",
			"source": f"switch.matrix-{switch}",
			"destination": _coil(coil),
			"provenance": provenance("validated", MANUAL_SOURCE, EDGES_SOURCE),
		}
		for switch, coil, name in pairs
	]


def conflicts() -> list[dict[str, Any]]:
	return []


def drivers() -> list[dict[str, Any]]:
	by_id = {item["id"]: item for item in load_json(ROOT / "catalog/pinmame.json")["drivers"]}
	result = []
	for driver_id in DRIVER_IDS:
		item = {key: value for key, value in by_id[driver_id].items() if key in {"id", "clone_of", "description", "year", "manufacturer", "flags"}}
		compatibility, notes = DRIVER_COMPATIBILITY[driver_id]
		item["physical_compatibility"] = compatibility
		item["variant_notes"] = notes
		result.append(item)
	return result


# --- Sources -------------------------------------------------------------------------------------------
def _derivation(page: int, box: str, xref: int, width: int, inches: str, dpi: int, capped: int | None, size: str, quality: int = 80) -> str:
	cap = f", capped to {capped}px wide" if capped else ""
	return (
		f"{MANUAL_NAME} page {page}, crop box {box}, scanned page rendered at its native resolution (embedded image xref {xref}, "
		f"{width}px across {inches}in), rendered at {dpi} dpi{cap}, grayscale, {size} WebP quality {quality}"
	)


def _excerpt(name: str, locator: str, *, image: str | None = None, method: str = "manual", reviewed: bool = True, credit: str = EXCERPT_CREDIT) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"excerpt.demolition-man.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
	}
	if image is not None:
		record["image"] = f"evidence/excerpts/{MACHINE_ID}/{name}.webp"
		record["image_sha256"] = EXCERPT_FILE_HASHES[f"{name}.webp"]
		record["image_derivation"] = image
	record["method"] = method
	record["transcribed_by"] = credit
	record["reviewed"] = reviewed
	return record


def _manual_excerpts() -> list[dict[str, Any]]:
	ocr = "curator; text from the PDF text layer corrected against the rendered pages"
	return [
		_excerpt("switch-matrix", "PDF page 100, printed 2-44, Switch Matrix with the dedicated and flipper grounded-switch blocks; compared with the PDF 106 reprint and the PDF 107 dedicated-switch drawing",
			image=_derivation(100, "0.065,0.062,0.855,0.555", 331, 2581, "8.38", 153, 1000, "1001x883", 15)),
		_excerpt("switch-locations", "PDF page 101, printed 2-45, Switch Locations parts list and playfield drawing",
			image=_derivation(101, "0.1,0.035,0.97,0.998", 335, 2560, "8.31", 308, None, "2216x3469")),
		_excerpt("lamp-matrix", "PDF page 98, printed 2-42, Lamp Matrix; compared with the PDF 108 reprint and the PDF 139 foldout",
			image=_derivation(98, "0.09,0.055,0.88,0.51", 323, 2553, "8.29", 147, 960, "961x783")),
		_excerpt("lamp-locations", "PDF page 99, printed 2-43, Lamp Locations parts list and playfield drawing",
			image=_derivation(99, "0,0.02,1,0.97", 327, 2567, "8.33", 242, 2000, "2000x2689"), reviewed=False),
		_excerpt("solenoid-flasher-table", "PDF page 102, printed 2-46, Solenoid/Flasher Table with the general-illumination and flipper-circuit blocks; compared with the PDF 109 reprint",
			image=_derivation(102, "0.045,0.09,0.905,0.73", 339, 2581, "8.38", 127, 900, "901x948", 10)),
		_excerpt("solenoid-flasher-locations", "PDF page 103, printed 2-47, Solenoid/Flasher Location parts list and playfield drawing",
			image=_derivation(103, "0.07,0.035,0.995,0.935", 342, 2546, "8.27", 308, None, "2356x3242"), reviewed=False),
		_excerpt("solenoid-flasher-wiring", "PDF pages 110 and 111, printed 3-6 and 3-7, Solenoid Wiring and Flashlamp Wiring drawings (image: page 111)",
			image=_derivation(111, "0.12,0.04,0.95,0.96", 372, 2553, "8.29", 308, None, "2114x3314"), reviewed=False),
		_excerpt("ramp-locations", "PDF page 104, printed 2-48, Ramp Locations parts list", reviewed=False),
		_excerpt("power-driver-board-connectors", "PDF pages 136-138, printed 3-32 to 3-34, A-12697-3 Power Driver Board connector lists (image: the G.I. connectors on page 137)",
			image=_derivation(137, "0.5,0.15,0.97,0.52", 472, 2574, "8.36", 206, 800, "801x892"), reviewed=False),
		_excerpt("general-illumination", "PDF page 114, printed 3-10, General Illumination Circuit, with the G.I. block of the PDF 102 table",
			image=_derivation(114, "0.08,0.04,0.95,0.9", 383, 2553, "8.29", 181, 1300, "1301x1819"), reviewed=False),
		_excerpt("flipper-circuits", "PDF pages 115-118, printed 3-11 to 3-14, flipper circuit diagram, coil circuits, cabinet switch circuit and A-17316 Flipper Opto PCB, with the flipper block of the PDF 102 table (image: page 115)",
			image=_derivation(115, "0.1,0.07,0.95,0.95", 387, 2567, "8.33", 213, 1500, "1501x2198"), reviewed=False),
		_excerpt("mechanism-boards", "PDF pages 119-131, printed 3-15 to 3-27, opto, trough, Cryoclaw, motor, elevator, 8-driver and coin-door boards (image: the Cryoclaw Opto PCB and D.C. Motor Control page 124)",
			image=_derivation(124, "0.08,0.05,0.85,0.9", 421, 2581, "8.38", 204, 1300, "1301x2031"), reviewed=False),
		_excerpt("cpu-and-fliptronic-connectors", "PDF pages 133 and 135, printed 3-29 and 3-31, CPU board and Fliptronic II board connector lists", reviewed=False),
		_excerpt("boards-and-assemblies", "PDF pages 58-96, printed 2-2 to 2-40, backbox, cabinet, board and mechanism assembly parts pages", method="mixed", reviewed=False, credit=ocr),
		_excerpt("game-rules", "PDF pages 5, 6 and 12-17, rules, assembly instructions and game control locations", method="mixed", reviewed=False, credit=ocr),
		_excerpt("service-tests", "PDF pages 2, 11, 18-19, 23-28 and 46-49, ROM summary, DIP chart, menu system, test descriptions, error messages and Cryoclaw/Elevator theory of operation", method="mixed", reviewed=False, credit=ocr),
		_excerpt("maintenance-and-disassembly", "PDF pages 52-55, lubrication and playfield disassembly (Cryoclaw, ramps, diverter ramp)", method="mixed", reviewed=False, credit=ocr),
	]


def _runtime(source_id: str, filename: str, locator: str) -> dict[str, Any]:
	return {
		"id": source_id,
		"kind": "runtime_scenario",
		"uri": f"internal:{EVIDENCE_DIRECTORY}/{filename}",
		"revision": PINMAME_REVISION,
		"locator": locator,
		"license": "NOASSERTION",
		"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
	}


def source_records() -> list[dict[str, Any]]:
	harness = (
		"One hash-pinned LibPinMAME harness run of dm_lx4 (library SHA-256 " + RUNTIME_LIBRARY_SHA256[:12] + "..., built from "
		+ PINMAME_REVISION[:8] + ") from empty NVRAM (scenario tools/harness-scenarios/wpc-dcs/{scenario}.json): {what}"
	)
	return [
		{
			"id": CATALOG_SOURCE,
			"kind": "pinmame_catalog",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the dm_* clone tree (" + ", ".join(DRIVER_IDS) + ")",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/dm.c dmGameData with GEN_WPCDCS, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L | FLIP_UL), "
				"custSol 8 with dm_getSol publishing WPC_EXTBOARD1 bits 0-7 at CORE_CUSTSOLNO(1)-(8) = 51-58, init_dm calling "
				"wpc_set_modsol_aux_board(1) and no wpc_set_fastflip_addr, the inverted-switch mask {0x00, 0x00, 0x30, 0x3f, 0x00, 0x00, 0x40, "
				"0x2f, ...} (index n is matrix column n under wpc_sw2m, so core_setSw inverts public 25, 26, 31-36, 67, 71-74 and 76), the "
				"switch and solenoid #defines (swClawPosRight 25, swClawPosLeft 26, swElevatorIndex 67, swElevatorHold 74, swElevatorRamp 75, "
				"sElevatorMotor 18, sClawLeft 19, sClawRight 20, sClawMagnet 33) and dm_handleMech's claw/elevator/magnet model (used only by "
				"runs with --handle-mechanics 15); src/wpc/core.c core_getSol and core_updateSw; src/wpc/wpc.c WPC_FLIPPERS complement and the "
				"WPC_EXTBOARD1 aux-board write; src/wpc/core.h CORE_FIRSTCUSTSOL=51, CORE_FLIPPERSWCOL=11."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-dcs.json",
			"revision": "repository",
			"locator": "WPC-DCS public switch, DIP, solenoid, lamp and five-GI address rules, including the Fliptronic block, the no-LPDC 37-44 range and the custom-output range from 51",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE,
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=662",
			"revision": "Wayback capture 2026-09-04T08:22:52Z",
			"sha256": IPDB_PAGE_SHA256,
			"acquired_at": "2026-10-09T13:16:00Z",
			"locator": (
				"IPDB machine 662 'Demolition Man' (Williams, February 1994, model 50028, Williams WPC (DCS), 4 players, 7,019 units, "
				f"widebody SuperPin). IPDB is Cloudflare-gated, so the page was read from the raw Wayback capture {IPDB_WAYBACK} "
				"(retained gzip-encoded as served, ipdb-662-page-wayback.html.gz). Title, manufacturer, date and model number match the manual's "
				"cover (16-50028-101) and the machine being curated."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", f"IPDB machine 662 page, Wayback capture {IPDB_WAYBACK}", reviewed=False, credit="curator, read from the retained HTML")],
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": f"external:{MANUALS_DIRECTORY}/{MANUAL_NAME}",
			"original_filename": MANUAL_NAME,
			"sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-09T13:17:00Z",
			"locator": (
				"Williams Demolition Man Operations Manual 16-50028-101 (March 1994), 140 pages of 1-bit 308 ppi scans with an OCR text layer. "
				"PDF 98-104 (printed 2-42 to 2-48) carry the lamp matrix, lamp locations, switch matrix, switch locations, solenoid/flasher table, "
				"solenoid/flasher locations and ramp locations; PDF 105-138 (Section 3) the reprinted matrices, wiring drawings, board pages and the "
				"Power Driver Board connector lists; PDF 139 is a foldout reprint of the lamp and switch matrices. Every table cell was read from "
				f"a rendered page; the text layer only located pages. Direct resource: {MANUAL_WAYBACK}."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
			"excerpts": _manual_excerpts(),
		},
		{
			"id": PARTS_LIST_SOURCE,
			"kind": "manual",
			"uri": f"external:{MANUALS_DIRECTORY}/{PARTS_LIST_NAME}",
			"original_filename": PARTS_LIST_NAME,
			"sha256": PARTS_LIST_SHA256,
			"acquired_at": "2026-10-09T13:17:00Z",
			"locator": (
				"IPDB-hosted plain-text Demolition Man parts list (2,587 lines). Supporting only: its assembly numbers do not always match the "
				f"manual's (for example the standup targets), so no device field is taken from it. Direct resource: {PARTS_LIST_WAYBACK}."
			),
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("parts-list-switches", "Lines naming switches, optos, targets and the control handles", reviewed=False, credit="curator, quoted from the text file")],
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": f"external:pinmame-vpx-sources/williams/demolition-man-1994/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME,
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working Knorr/Kiwi 1.3.1 recreation (copied from the contributor's Visual Pinball table library). Exact "
				f"playfield bounds are {TABLE_BOUNDS}, the widebody size; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and "
				f"y/{PLAYFIELD_HEIGHT:g}. Geometry authority only for named table objects the script binds; the placement seed "
				"tools/seeds/williams/demolition-man-1994-spatial.json lists them."
			),
			"license": "NOASSERTION",
			"attribution": "Knorr and Kiwi (table authors)",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/demolition-man-1994/source/Demolition%20Man%20(Knorr-Kiwi)%201.3.1.vbs",
			"original_filename": "Demolition Man (Knorr-Kiwi) 1.3.1.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Embedded script extracted with vpxtool extractvbs (47,148 bytes). Runtime authority: Const cGameName = "dm_lx4", LoadVPM '
				'"01560000", "WPC.VBS", 3.36, HandleMechanics = 0, the bsTrough/bsTopPopper/BottomPopper/bsEject ball stacks, the claw and '
				"elevator cvpmMechs, the SolCallback/SolModCallback table, the NFadeLm lamp calls and UpdateGI. The pinned vpxtable_scripts "
				"corpus carries a sound-modified copy of the same release, not this byte stream."
			),
			"license": "NOASSERTION",
			"attribution": "Knorr and Kiwi (table authors)",
			"rights": "NOASSERTION",
			"excerpts": [_excerpt("vpx-script-bindings", "Every non-comment script line that binds the controller, with its line number", credit="curator, quoted from the script file")],
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/demolition-man-1994/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION",
			"attribution": "vpxtool extraction",
		},
		{
			"id": VPM_LIBRARY_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/vpm-script-libs/wpc.vbs",
			"original_filename": "wpc.vbs",
			"sha256": VPM_WPC_SHA256,
			"locator": (
				"VPinMAME WPC script library the retained table loads (LoadVPM ... \"WPC.VBS\"), retained from the contributor's working "
				f"installation beside the core.vbs it executes (SHA-256 {VPM_CORE_SHA256}). Lines 58-61 define swLRFlip = 112, swLLFlip = 114, "
				"swURFlip = 116 and swULFlip = 118; vpmKeyDown/vpmKeyUp (lines 101-151) write 112 and 114 from the flipper keys and the upper "
				"pair only from a staged flipper key with an upper flipper solenoid registered."
			),
			"license": "NOASSERTION",
			"attribution": "VPinMAME script authors",
			"excerpts": [_excerpt("vpm-script-library-flippers", "Lines 58-61 and the vpmKeyDown/vpmKeyUp switch writes (lines 102-158)", credit="curator, quoted from the library file")],
		},
		_runtime(EDGES_SOURCE, "demolition-man-dm-lx4-switch-edges.json", harness.format(scenario="dm-switch-edges", what=(
			"with built-in mechanisms disabled, T.1 SWITCH EDGES while every matrix address 11-88 (but 22) and every Fliptronic address "
			"111-118 is set to 1 and back to 0. The ROM names every matrix switch at public 1 (24 Always Closed at 0), fires 9-13 from the "
			"slingshot and jet switches, fires the lower right flipper from 112 or 116 and the lower and upper left flippers from 114 or 118."))),
		_runtime(CLAW_TEST_SOURCE, "demolition-man-dm-lx4-claw-test.json", harness.format(scenario="dm-claw-test", what=(
			"with built-in mechanisms disabled, T.14 CLAW TEST marks the CLAW R., CLAW L., ELEV. INDEX and ELEV. HOLD boxes while public 25, "
			"26, 67 and 74 are 1."))),
		_runtime(CLAW_FUNCTIONS_SOURCE, "demolition-man-dm-lx4-claw-functions.json", harness.format(scenario="dm-claw-functions", what=(
			"with PinMAME's claw and elevator model enabled, the six T.14 functions held in turn: AUTO RUN, RUN ELEVATOR and PARK ELEVATOR drive "
			"18, CLAW RIGHT drives 19 and 20, MAGNET ON drives 33, CLAW LEFT (already at left) drives nothing."))),
		_runtime(SOLENOID_TEST_SOURCE, "demolition-man-dm-lx4-solenoid-test.json", harness.format(scenario="dm-solenoid-test", what=(
			"T.4 SOLENOID TEST stepped through 1-16, 33 and 34, each named with its wires and pulsed at that public address."))),
		_runtime(FLASHER_TEST_SOURCE, "demolition-man-dm-lx4-flasher-test.json", harness.format(scenario="dm-flasher-test", what=(
			"T.5 FLASHER TEST stepped through 17, 21-28 and the auxiliary flashers the ROM numbers 37-44 while it pulses public 51-58."))),
		_runtime(GI_TEST_SOURCE, "demolition-man-dm-lx4-gi-test.json", harness.format(scenario="dm-gi-test", what=(
			"T.6 GEN'L. ILLUM. steps ALL ILLUMINATION and then BACK PANEL, UPPER RIGHT, UPPER LEFT, LOWER RIGHT and LOWER LEFT, which change "
			"public G.I. 0-4 in that order."))),
		_runtime(FLIPPER_TEST_SOURCE, "demolition-man-dm-lx4-flipper-coil-test.json", harness.format(scenario="dm-flipper-coil-test", what=(
			"T.12 FLIPPER COIL pulses 45, 46, 47, 48, 35 and 36 under the names R./L./U.L. FLIP. POWER/HOLD and the numbers 01-04, 07, 08."))),
		{
			"id": CALLOUT_SOURCE,
			"kind": "human_review",
			"uri": "internal:tools/seeds/williams/demolition-man-1994-callouts.json",
			"sha256": _file_sha256(CALLOUT_SEED_PATH),
			"locator": (
				"2026-10-09 factory location-drawing callout check of PDF 99, 101 and 103 (printed 2-43, 2-45 and 2-47): every callout "
				"transcribed independently on the committed excerpt crops, per-page control and callout fits; a table placement whose own "
				"callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays and the "
				"generator are retained under review-artifacts with a pinned manifest."
			),
			"license": "NOASSERTION",
			"attribution": "PinMAME game definitions contributors",
		},
		_runtime(LAMP_TEST_SOURCE, "demolition-man-dm-lx4-single-lamps.json", harness.format(scenario="dm-single-lamps", what=(
			"T.8 SINGLE LAMPS lights each public lamp 11-88 in turn and prints its name."))),
	]


# --- Build ---------------------------------------------------------------------------------------------
def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Demolition Man",
			"manufacturer": "Williams",
			"year": 1994,
			"kind": "physical_pinball",
			"model_number": "50028",
			"ipdb_id": 662,
			"opdb_id": "G5bv3-MLW68",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["variant_differences", "spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "observed",
				"variant_coverage": "observed",
				"recreation_knowledge": "validated",
				"spatial_placement": "observed",
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
		"knowledge": {"path": "knowledge/williams/demolition-man-1994.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Demolition Man device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] if item not in known]
		if unknown:
			raise RuntimeError(f"Demolition Man mechanism {mechanism['id']} names unknown devices: {unknown}")
	for relationship in definition["relationships"]:
		if relationship["source"] not in known or relationship["destination"] not in known:
			raise RuntimeError(f"Demolition Man relationship {relationship['id']} names unknown devices")
	drawing_callouts.apply_to_definition(definition, load_json(CALLOUT_SEED_PATH), CALLOUT_SOURCE)
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device["availability"] in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
	seed = load_json(CALLOUT_SEED_PATH)
	check = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(definition), seed.get("limit", drawing_callouts.LIMIT))
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:g}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:g}; 0=rear/backglass, 1=apron/player",
		},
		"source_hashes": {
			"table_sha256": TABLE_SHA256,
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"spatial_seed_sha256": _file_sha256(SPATIAL_SEED_PATH),
			"callout_seed_sha256": _file_sha256(CALLOUT_SEED_PATH),
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/williams/demolition-man-1994/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"drawing_callout_check": drawing_callouts.summary(seed, check, "tools/seeds/williams/demolition-man-1994-callouts.json", _file_sha256(CALLOUT_SEED_PATH)),
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": "The centre of the VPX object the retained script binds to each matrix switch (trigger, kicker, standup or slingshot wall drag-point centroid, bumper). Sensors the table does not model are projected onto their mechanism's object: the trough optos onto BallRelease, the claw position optos onto the Claw arm's pivot, the elevator index onto ElevatorKicker.",
			"lamp": "The centre of the insert Light each lamp's NFadeLm call drives (not its 'b' halo double). Lamps 11, 82 and 83 place both bulbs; lamp 83's inner pair comes from l83/l83a, which the table's fader wrongly drives from lamp 82.",
			"solenoid": "The kicker, slingshot wall, bumper or flipper the script fires; for flashers the script-driven Light at the flasher. The diverter's power winding and the claw motor lines and magnet are projected onto the mechanism they move.",
			"gi": "The Light members of the collection UpdateGI drives for strings 1-4, with render doubles closer than 0.006 normalized collapsed; observed only, without a quantity.",
		},
		"unresolved_geometry": [
			"G.I. string 1 (Back Panel) has no placement: the table models none of its bulbs, and no factory drawing locates G.I. bulbs, so spatial_placement stays in coverage.missing.",
			"The G.I. placements of strings 2-5 rest on the table's own grouping; no drawing or per-string bulb count validates them.",
			"Lamps 71-73 (a stacked three-lamp bar on the lamp drawing) and the back-panel flashers 17, 55 and 56 have no placement: the table renders them only as Flasher sprites.",
			"The lamp drawing hides its jet bumpers under ramp linework, so its control fit rests on the three flipper pivots and the Cryoclaw pivot hub; its leave-one-out control error is large, and the leave-one-out callout fit carries the check.",
			"Hidden mechanism contacts (trough optos, claw position optos, elevator index, end-of-stroke switches) have whole-mechanism projections or none.",
		],
		"promotion_decision": "partial: every used device has a placement or a controlled not-applicable record except the back-panel G.I. string, three lamps and three back-panel flashers; the factory drawings validate most checked table placements, but the G.I. bulbs cannot be validated from any retained drawing or count.",
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Demolition Man (Williams, 1994) spatial blockers",
		"",
		f"Retained VPX SHA-256 `{TABLE_SHA256}`; script `{SCRIPT_SHA256}`; {EXTRACTION_FILE_COUNT}-file extraction manifest "
		f"`{EXTRACTION_MANIFEST_SHA256}`; manual `{MANUAL_SHA256}`.",
		"",
		f"Bounds: `{TABLE_BOUNDS}`. Every canonical coordinate is x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g} rounded to at most six places.",
		"",
		"## Placement status",
		"",
	]
	for name, items in report["placement_status"].items():
		lines.append(f"- `{name}`: {len(items)} devices")
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(report['without_placements'])}",
		"",
	]
	lines += [f"  - `{item}`" for item in report["without_placements"]]
	lines += ["", "## Projection classes", ""]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	check = report["drawing_callout_check"]
	lines += [
		"",
		"## Drawing callout check",
		"",
		f"{check['rule']} It validates {check['validated']} of the {check['checked']} table placements it checks "
		f"([seed](../../../{check['seed']})); the rest keep their observed status:",
		"",
	]
	for placement_id, item in check["not_validated"].items():
		if "control_offset" in item:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {max(item['control_offset'], item['callout_offset']):.3f} normalized away.")
		else:
			lines.append(f"- `{placement_id}`: callout {item['label']} on {item['page']}, {item['reason']}.")
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready Demolition Man artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale Demolition Man author-ready artifact: {AUTHOR_READY_PATH}")
	definition = build()
	report = build_spatial_report(definition)
	expected = (
		(PARTIAL_PATH, canonical_bytes(definition)),
		(SPATIAL_REPORT_PATH, canonical_bytes(report)),
		(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report).encode("utf-8")),
		(KNOWLEDGE_PATH, KNOWLEDGE_SEED_PATH.read_bytes()),
	)
	for path, content in expected:
		if not path.is_file() or path.read_bytes() != content:
			raise RuntimeError(f"Demolition Man deterministic artifact drift: {path}")
	print("Demolition Man definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Demolition Man extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Demolition Man retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
