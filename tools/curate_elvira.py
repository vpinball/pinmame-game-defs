"""Curate the physical Bally Elvira and the Party Monsters (1989) machine definition.

The builder is deterministic: every reviewed label, wiring detail and normalized coordinate is a
literal, and the only repository files it reads are the pinned catalog (for driver records) and the
committed manual excerpts (for their digests). ``--check`` refuses drift and ``--regenerate`` is the
only path that writes the canonical definition, its pinned seed and the spatial audit.

Elvira is the third System 11-family machine curated here (pinned PinMAME declares Whirlwind GEN_S11B
too). It reuses
``controllers/pinmame/system-11.json`` unchanged. ``eatpmGameData`` (src/wpc/sims/s11/prelim/eatpm.c)
declares GEN_S11B, two 16-character 16-segment displays, ``FLIP_SWNO(58,57)`` with no FLIP_SOL bit,
``S11_LOWALPHA|S11_DISPINV`` display flags, ``hw.gameSpecific1 = S11_MUXSW2`` and ``sxx.muxSol = 12``
with an empty ``sxx.ssSw``: an A/C select relay on solenoid 12 whose state PinMAME mirrors onto
switch 2, a populated 25-32 C-side bank, no sound-overlay board, and special solenoids 17-22 that
PinMAME only drives through the PIA path.
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
DEFINITION_PATH = ROOT / "machines/partial/bally/elvira-and-the-party-monsters-1989.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/bally/elvira-and-the-party-monsters-1989.json"
SEED_PATH = ROOT / "tools/seeds/bally/elvira-and-the-party-monsters-1989.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/elvira-and-the-party-monsters-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/elvira-and-the-party-monsters-1989.md"
EXCERPT_DIR = "evidence/excerpts/bally.elvira-and-the-party-monsters.1989"

MACHINE_ID = "bally.elvira-and-the-party-monsters.1989"
KNOWLEDGE_PATH = "knowledge/bally/elvira-and-the-party-monsters-1989.md"

PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.bally.elvira-and-the-party-monsters.1989"
VPX_TABLE_SOURCE = "vpx-table.elvira-and-the-party-monsters-1989"
VPX_SCRIPT_SOURCE = "vpx-script.elvira-and-the-party-monsters-1989"
VPX_EXTRACTION_SOURCE = "vpx-extraction.elvira-and-the-party-monsters-1989"
CORPUS_SCRIPT_SOURCE = "vpx-script.elvira-and-the-party-monsters-v1-03"
GEOMETRY_SOURCE = "human-review.elvira-and-the-party-monsters-1989.vpx-geometry"
VPM_LIBRARY_SOURCE = "vpm-script-library.s11-vbs"
VPM_S11_SHA256 = "5582155ffbdaeeeb3d86fcb54d7738d9ea5f9c24951b607e30a316f88dfd5f91"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

MANUAL_SHA256 = "d1bc4d1c1e436733b6f84db35b874558f0c85a85ba6371196b5dfa63dd120445"
TABLE_SHA256 = "b9f54017274ccb4f3bddb08f6a999723502745527cdd8e237d639c1222552330"
SCRIPT_SHA256 = "aaa5bc0f1893d27dc4e49c2d3829a03ad79769f6328e6e4a8138fc4308d0bc4b"
CORPUS_SCRIPT_SHA256 = "c251128e2dd0cc79a17ae868b244b7550ac6bf4dbb6bea66ca1989fd5be0773d"
VPXTABLE_SCRIPTS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"

EXTRACTION_RELATIVE_PATH = Path("bally/elvira-and-the-party-monsters-1989/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/elvira-and-the-party-monsters-1989/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 1263
EXTRACTION_TOTAL_BYTES = 58249735
EXTRACTION_MANIFEST_SHA256 = "fa3ddac51285909c3763a87c017e2bfddac9ec422082bfae1fcedce4b3623fa5"

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0

DRIVER_IDS = ("eatpm_l4", "eatpm_l1", "eatpm_l2", "eatpm_f1", "eatpm_4u", "eatpm_4g", "eatpm_3g", "eatpm_p7")
SHARED_GAME_DATA = (
	" Declared with CORE_CLONEDEF of eatpm_l4 in src/wpc/sims/s11/prelim/eatpm.c, so it binds the same "
	"init_eatpm/eatpmGameData and the same elvira machine driver: switch, lamp, solenoid, display and "
	"flipper routing are identical to the parent."
)
DRIVER_COMPATIBILITY = {
	"eatpm_l4": (
		"identical",
		"LA-4, the pinned catalog's clone-tree parent and the driver both retained VPX scripts bind "
		"(cGameName = \"eatpm_l4\"). Game ROMs elvi_u26.l4 and elvi_u27.l4 with the L-1 sound ROMs.",
	),
	"eatpm_l1": ("identical", "LA-1, an earlier production game ROM pair (u26-la1, u27-la1)." + SHARED_GAME_DATA),
	"eatpm_l2": ("identical", "LA-2, an earlier production game ROM pair (u26-la2, u27-la2)." + SHARED_GAME_DATA),
	"eatpm_f1": (
		"identical",
		"LF-1 French game ROM (u26-lf1) paired with the LA-1 U27. Language localization only." + SHARED_GAME_DATA,
	),
	"eatpm_4u": ("identical", "LU-4 Europe game ROM (u26-lu4) paired with the L-4 U27." + SHARED_GAME_DATA),
	"eatpm_4g": (
		"identical",
		"LG-4 German game ROM (u26-lg4) paired with the L-4 U27. The manual's Country jumper, German "
		"pricing and German install adjustments are the operator-facing side of the same hardware."
		+ SHARED_GAME_DATA,
	),
	"eatpm_3g": (
		"compatible",
		"LG-3 German. The pinned ROM set pairs a U27 from an LG-3 board with the LG-4 U26 and flags that "
		"U26 BAD_DUMP (\"the U27 came without matching U26\"), so this driver is an emulator "
		"reconstruction rather than a verified factory pairing. The hardware contract is the parent's."
		+ SHARED_GAME_DATA,
	),
	"eatpm_p7": (
		"compatible",
		"PA-7 prototype game ROMs (u26-pa7, u27-pa7). The driver runs against the production hardware "
		"contract, but no retained source says whether prototype cabinets matched the production "
		"playfield, so compatibility rather than identity is claimed." + SHARED_GAME_DATA,
	),
}

# --- Switch matrix (public address = (column-1)*8+row, printed on the manual's own grid).
# Labels of record come from the Switch Location Diagram parts list (printed 2-37); the matrix page
# (printed 2-36) wording is kept where it differs.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "A/C Relay Select", 3: "Credit Button", 4: "Right Coin Switch",
	5: "Center Coin Switch", 6: "Left Coin Switch", 7: "Slam Tilt", 8: "High Score Reset",
	9: "Outhole", 11: "Trough 1, Right", 12: "Trough 2, Middle", 13: "Trough 3, Left",
	15: "Right Standup #1", 16: "Right Standup #2",
	17: "Left Outlane", 18: "Left Return", 19: "Right Return", 20: "Right Outlane",
	21: "Shooter Lane", 22: "Top Right Rollover", 23: "Right Side Rollunder",
	25: "Left Standup #1", 26: "Left Standup #2", 27: "Left Standup #3", 28: "Left Standup #4",
	29: "Lock Entry", 30: "Left Ramp Entry", 31: "Left Ramp End", 32: "Ball Popper",
	33: "Left Slingshot", 34: "Right Slingshot", 35: "Left Bumper", 36: "Right Bumper", 37: "Bottom Bumper",
	41: "Left Drop Target \"J\"", 42: "Center Drop Target \"A\"", 43: "Right Drop Target \"M\"",
	44: "Right Ramp Entry", 45: "\"B\" Lane", 46: "\"A\" Lane", 47: "\"T\" Lane", 48: "Eject Hole",
	49: "Lock 1", 50: "Lock 2", 51: "Lock 3", 52: "Lock Safety",
	53: "Flip Up Target #1", 54: "Flip Up Target #2", 55: "Flip Up #1 Open", 56: "Flip Up #2 Open",
	57: "Right Flipper", 58: "Left Flipper",
}
UNUSED_MATRIX_ADDRESSES = frozenset({10, 14, 24, 38, 39, 40, 59, 60, 61, 62, 63, 64})
MATRIX_PAGE_WORDING = {
	2: "A/C Relay Position", 4: "Right Coin", 5: "Center Coin", 6: "Left Coin",
	11: "Trough Sw. 1 Right", 12: "Trough Sw. 2 Center", 13: "Trough Sw. 3 Left",
	15: "Right Standup 1", 16: "Right Standup 2", 18: "Left Return Lane", 19: "Right Return Lane",
	21: "Ball Shooter", 25: "Left Standup Target 1", 26: "Left Standup Target 2",
	27: "Left Standup Target 3", 28: "Left Standup Target 4", 35: "Left Thumper Bumper",
	36: "Right Thumper Bumper", 41: "Left Drop Target", 42: "Center Drop Target", 43: "Right Drop Target",
	45: "B", 46: "A", 47: "T", 53: "Flip Up Target 1", 54: "Flip Up Target 2",
	55: "Flip Up 1 Open", 56: "Flip Up 2 Open",
}
SWITCH_PARTS = {
	3: "SW-1A-126", 4: "27-1092", 6: "27-1092", 7: "27-1066", 8: "27-1008",
	9: "5647-12133-12", 11: "5647-12073-08", 12: "5647-09957-00", 13: "5647-09957-00",
	15: "SW-1A-185-17", 16: "SW-1A-185-17", 17: "5647-12073-19", 18: "5647-12073-19", 19: "5647-12073-19",
	20: "5647-12073-19", 21: "5647-12073-04", 22: "5647-12073-19", 23: "5647-12073-19",
	25: "SW-1A-186-17", 26: "SW-1A-182-17", 27: "SW-1A-186-17", 28: "SW-1A-182-17",
	29: "5647-12073-19", 30: "A-13068", 31: "5647-12073-11", 32: "A-11657",
	35: "p/o C-12872", 36: "p/o C-12872", 37: "p/o C-12872",
	41: "p/o C-12559", 42: "p/o C-12559", 43: "p/o C-12559", 44: "A-13068",
	45: "5647-12073-19", 46: "5647-12073-19", 47: "5647-12073-19", 48: "5647-12133-11",
	49: "5647-12073-27", 50: "5647-12073-28", 51: "5647-12073-26", 52: "5647-12073-25",
	53: "SW-1A-170-4", 54: "SW-1A-170-4", 55: "5647-12073-30", 56: "5647-12073-30",
}
SWITCH_TYPES = {
	1: "tilt", 3: "button", 7: "tilt", 8: "button",
	15: "leaf", 16: "leaf", 25: "leaf", 26: "leaf", 27: "leaf", 28: "leaf", 53: "leaf", 54: "leaf",
	2: "opto", 41: "opto", 42: "opto", 43: "opto", 57: "opto", 58: "opto",
}
SWITCH_COLUMN_WIRING = {
	1: ("GRN-BRN", "1J8-1", "Q45"), 2: ("GRN-RED", "1J8-2", "Q49"), 3: ("GRN-ORN", "1J8-3", "Q44"),
	4: ("GRN-YEL", "1J8-4", "Q48"), 5: ("GRN-BLK", "1J8-5", "Q43"), 6: ("GRN-BLU", "1J8-7", "Q47"),
	7: ("GRN-VIO", "1J8-8", "Q42"), 8: ("GRN-GRY", "1J8-9", "Q46"),
}
SWITCH_ROW_WIRING = {
	1: ("WHT-BRN", "1J10-9"), 2: ("WHT-RED", "1J10-8"), 3: ("WHT-ORN", "1J10-7"), 4: ("WHT-YEL", "1J10-6"),
	5: ("WHT-GRN", "1J10-5"), 6: ("WHT-BLU", "1J10-3"), 7: ("WHT-VIO", "1J10-2"), 8: ("WHT-GRY", "1J10-1"),
}
DEDICATED_LABELS = {
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Auto-Up/Manual-Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic", "service.cpu-diag"), -4: ("Sound Diagnostic", "service.sound-diag"),
}
# Script handler and object that assert each playfield switch in the retained known-working table.
SWITCH_SCRIPT_BINDING = {
	9: "Drain_Hit feeds bsTrough (InitSw 9, 11, 12, 13)",
	11: "bsTrough.InitSw 9, 11, 12, 13 (first ball position, kicked by BallRelease)",
	12: "bsTrough.InitSw 9, 11, 12, 13", 13: "bsTrough.InitSw 9, 11, 12, 13",
	15: "sw15_Hit: vpmTimer.PulseSw 15", 16: "sw16_Hit: vpmTimer.PulseSw 16",
	17: "sw17_Hit/UnHit", 18: "sw18_Hit/UnHit", 19: "sw19_Hit/UnHit", 20: "sw20_Hit/UnHit",
	21: "sw21_Hit/UnHit", 22: "sw22_Hit/UnHit", 23: "sw23_Hit/UnHit",
	25: "sw25_Hit: vpmTimer.PulseSw 25", 26: "sw26_Hit: vpmTimer.PulseSw 26",
	27: "sw27_Hit: vpmTimer.PulseSw 27", 28: "sw28_Hit: vpmTimer.PulseSw 28",
	29: "sw29_Hit/UnHit", 30: "sw30_Hit: vpmTimer.PulseSw 30", 31: "sw31_Hit: vpmTimer.PulseSw 31",
	32: "sw32_Hit feeds bsBP (InitSaucer sw32, 32)",
	33: "LeftSlingShot_Slingshot: vpmTimer.PulseSw 33", 34: "RightSlingShot_Slingshot: vpmTimer.PulseSw 34",
	35: "Bumper1_Hit: vpmTimer.PulseSw 35", 36: "Bumper2_Hit: vpmTimer.PulseSw 36", 37: "Bumper3_Hit: vpmTimer.PulseSw 37",
	41: "dtbank.InitDrop Array(sw41, sw42, sw43), array(41, 42, 43)",
	42: "dtbank.InitDrop Array(sw41, sw42, sw43), array(41, 42, 43)",
	43: "dtbank.InitDrop Array(sw41, sw42, sw43), array(41, 42, 43)",
	44: "sw44_Hit: vpmTimer.PulseSw 44",
	45: "sw45_Hit/UnHit", 46: "sw46_Hit/UnHit", 47: "sw47_Hit/UnHit",
	48: "sw48_Hit feeds bsTP (InitSaucer sw48, 48)",
	49: "bsLock.InitSw 0, 49, 50, 51", 50: "bsLock.InitSw 0, 49, 50, 51", 51: "bsLock.InitSw 0, 49, 50, 51",
	52: "sw52_Hit: vpmTimer.PulseSw 52",
	53: "sw53_Hit: Controller.Switch(53) = 1 and vpmTimer.PulseSw 55; SolFlipReset clears it",
	54: "sw54_Hit: Controller.Switch(54) = 1 and vpmTimer.PulseSw 56; SolFlipReset clears it",
	55: "pulsed from sw53_Hit only", 56: "pulsed from sw54_Hit only",
	57: "Table1_KeyDown/KeyUp: Controller.Switch(57) on RightFlipperKey",
	58: "Table1_KeyDown/KeyUp: Controller.Switch(58) on LeftFlipperKey",
}
# Preliminary simulator symbols in src/wpc/sims/s11/prelim/eatpm.c whose gameplay name differs from the
# manual's device name. They describe the same device; they are cross-reference only.
SIMULATOR_SYMBOLS = {
	2: "swRelay", 22: "swPizzaTop", 23: "swPizzaBot", 25: "swDHwake", 26: "swDHthee", 27: "swDHdead",
	28: "swDHheads", 45: "swbAT", 46: "swBaT", 47: "swBAt", 53: "swFlip1Tar", 54: "swFlip2Tar",
	55: "swFlip1Op", 56: "swFlip2Op",
}

# --- Normalized playfield coordinates, x/952 and y/1974, from the retained VPX extraction. The full
# object-by-object dump is external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpx-geometry-raw.tsv.
SWITCH_POSITIONS = {
	9: [(0.454331, 0.966750)],
	11: [(0.874847, 0.873597)], 12: [(0.874847, 0.873597)], 13: [(0.874847, 0.873597)],
	15: [(0.853514, 0.554043)], 16: [(0.852844, 0.582144)],
	17: [(0.060388, 0.747407)], 18: [(0.142123, 0.745298)], 19: [(0.770353, 0.745987)], 20: [(0.853438, 0.747907)],
	21: [(0.945358, 0.892678)], 22: [(0.910737, 0.089012)], 23: [(0.935114, 0.280412)],
	25: [(0.106505, 0.516826)], 26: [(0.106057, 0.543416)], 27: [(0.106505, 0.571087)], 28: [(0.105608, 0.598758)],
	29: [(0.059166, 0.232809)], 30: [(0.188416, 0.291540)], 31: [(0.362162, 0.016098)], 32: [(0.273117, 0.083053)],
	33: [(0.229364, 0.739857)], 34: [(0.681711, 0.735746)],
	35: [(0.604813, 0.220739)], 36: [(0.812558, 0.221619)], 37: [(0.708029, 0.306336)],
	41: [(0.577831, 0.352642)], 42: [(0.606603, 0.376124)], 43: [(0.637035, 0.399606)],
	44: [(0.824243, 0.340205)], 45: [(0.614347, 0.129899)], 46: [(0.707481, 0.130009)], 47: [(0.798423, 0.128842)],
	48: [(0.488445, 0.102204)],
	49: [(0.185836, 0.212467)], 50: [(0.185836, 0.212467)], 51: [(0.185836, 0.212467)], 52: [(0.308526, 0.198249)],
	53: [(0.324144, 0.304030)], 54: [(0.375267, 0.298921)], 55: [(0.298730, 0.241744)], 56: [(0.352271, 0.237074)],
}
# Placements the manual's own drawing does not corroborate get "observed" instead of "validated".
OBSERVED_SWITCH_PLACEMENTS = frozenset({31, 52, 55, 56})
SWITCH_PROJECTIONS = {
	9: (
		"Projected onto the Drain kicker (Kicker.Drain, object centre): the retained script manages the outhole "
		"inside its bsTrough cvpmBallStack and has no object of the switch's own. The manual draws callout 9 at "
		"the outhole end of the trough."
	),
	11: (
		"Projected onto the BallRelease kicker (Kicker.BallRelease, object centre): the three trough positions "
		"have no individual objects, bsTrough.InitSw 9, 11, 12, 13 managing them against the single exit kicker. "
		"The manual draws 11 nearest the shooter lane, then 12, then 13."
	),
	12: "Projected onto the BallRelease kicker; see switch 11.",
	13: "Projected onto the BallRelease kicker; see switch 11.",
	31: (
		"Taken from Trigger.sw31, the invisible trigger the script's sw31_Hit handler pulses, which sits at the "
		"rear edge where the left (Monster Slide) ramp ends. The manual's switch drawing prints no callout 31, "
		"so the position is observed rather than validated."
	),
	33: (
		"Projected onto the drag-point centroid of Wall.LeftSlingShot, whose _Slingshot event the script uses to "
		"pulse this address; the switch is part of the slingshot assembly (manual note ***, paired kicker "
		"actuating switch B-12459/B-12715)."
	),
	34: "Projected onto the drag-point centroid of Wall.RightSlingShot; see switch 33.",
	49: (
		"Projected onto the BallLock kicker (Kicker.BallLock, object centre): bsLock.InitSw 0, 49, 50, 51 manages "
		"the three lock positions against that single kicker. The manual's leaders for 49, 50, 51 and 52 all "
		"end in the upper-left lock lane."
	),
	50: "Projected onto the BallLock kicker; see switch 49.",
	51: "Projected onto the BallLock kicker; see switch 49.",
	52: (
		"Taken from Trigger.sw52, the invisible trigger the script's sw52_Hit handler pulses. It sits about 0.1 "
		"right of where the manual's leader for 52 ends in the lock lane, so the position is observed."
	),
	55: (
		"Projected onto Primitive.Coffin_Elvira, the open-state visual the script shows when target 53 is hit. "
		"The retained table has no object for the flip-up position switch; the manual's leader for 55 ends at "
		"the first flip-up. Observed, not validated; see conflict.flip-up-switch-roles."
	),
	56: "Projected onto Primitive.Coffin_Drac, the open-state visual shown for target 54; see switch 55.",
}

# --- Solenoid table (public address = the manual's own Sol. No.; 01A-08A are public 1-8 and 01C-08C
# are public 25-32 through the A/C select relay on solenoid 12).
SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Ball Eject (Shooter Lane Feeder)", 3: "Drop Target Bank",
	4: "Not Used Solenoid Position 4A", 5: "Eject Hole", 6: "Ball Popper", 7: "Knocker", 8: "Ball Lock Release",
	9: "ELVIRA Flashers", 10: "Insert GI Relay", 11: "Playfield GI Relay", 12: "A/C Select Relay",
	13: "Rightside / Graveyard Flashers", 14: "Boogie Monsters", 15: "Backboard Left Side / Dead Head Flashers",
	16: "Boogie Monsters Flashers",
	17: "Left Thumper Bumper", 18: "Left Slingshot Kicker", 19: "Right Thumper Bumper",
	20: "Right Slingshot Kicker", 21: "Bottom Thumper Bumper", 22: "Flip Up Reset",
	25: "Jets / Bats Flashers", 26: "Organ Flasher", 27: "Right Ramp / Punch Flashers",
	28: "Left Ramp / Drac Flashers", 29: "Moon / Wolfman Flashers", 30: "Right Return / Hot Dog, BBQ, Bun Flashers",
	31: "Left Return / Letters Flashers", 32: "Skull / House Flashers",
}
SOLENOID_TABLE_WORDING = {
	1: "01A Outhole Kicker", 2: "02A Ball Eject (Shtr Lane Feeder)", 3: "03A Drop Target Bank", 4: "04A (blank)",
	5: "05A Eject Hole", 6: "06A Ball Popper", 7: "07A Knocker", 8: "08A Ball Lock Release",
	9: "09 ELVIRA", 10: "10 INSERT GI", 11: "11 PLAYFIELD GI", 12: "12 A/C Select Relay",
	13: "13 Rightside (p)/Graveyard (i)", 14: "14 Boogie Monsters", 15: "15 B/board L. Side (p)/DHead (i)",
	16: "16 Boogie Monsters", 17: "17 Left Thumper Bumper", 18: "18 Left Slingshot Kicker",
	19: "19 Right Thumper Bumper", 20: "20 Right Slingshot Kicker", 21: "21 Bottom Thumper Bumper",
	22: "22 Flip Up Reset",
	25: "01C Jets (p)/Bats (i)", 26: "02C Organ Flasher", 27: "03C Right Ramp (p)/Punch (i)",
	28: "04C Left Ramp (p)/Drac (i)", 29: "05C Moon (p)/ Wolfman (i)",
	30: "06C Right Return (p)/ Hot Dog,BBQ,Bun (i)", 31: "07C Left Return (p)/Letters (i)",
	32: "08C Skull (p)/ House (i)",
}
SOLENOID_TYPE = {address: "Switched" for address in list(range(1, 9)) + list(range(25, 33))}
SOLENOID_TYPE.update({address: "Controlled" for address in range(9, 17)})
SOLENOID_TYPE.update({address: f"Special #{address - 16}" for address in range(17, 23)})
SOLENOID_WIRE = {
	1: "Vio-Brn", 2: "Vio-Red", 3: "Vio-Orn", 4: "Vio-Yel", 5: "Vio-Grn", 6: "Vio-Blu", 7: "Vio-Blk", 8: "Vio-Gry",
	9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio", 16: "Brn-Gry",
	17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
	25: "Blk-Brn", 26: "Blk-Red", 27: "Blk-Orn", 28: "Blk-Yel", 29: "Blk-Grn", 30: "Blk-Blu", 31: "Blk-Vio", 32: "Blk-Gry",
}
SOLENOID_CPU = {
	1: "1P11-1", 2: "1P11-3", 3: "1P11-4", 4: "1P11-5", 5: "1P11-6", 6: "1P11-7", 7: "1P11-8", 8: "1P11-9",
	9: "1P12-1", 10: "1P12-2", 11: "1P12-4", 12: "1P12-5", 13: "1P12-6", 14: "1P12-7", 15: "1P12-8", 16: "1P12-9",
	17: "1P10-7", 18: "1P19-4", 19: "1P19-3", 20: "1P19-6", 21: "1P19-8", 22: "1P19-9",
}
CONTROL_WIRE = {1: "Gry-Brn", 2: "Gry-Red", 3: "Gry-Orn", 4: "Gry-Yel", 5: "Gry-Grn", 6: "Gry-Blu", 7: "Gry-Vio", 8: "Gry-Blk"}
SOLENOID_POWER = {
	1: "5J1-9: 5J4-9 (A)", 2: "5J1-7: 5J4-8 (A)", 3: "5J1-6: 5J4-7 (A)", 4: "5J1-5: 5J4-6 (A)",
	5: "5J1-4: 5J4-5 (A)", 6: "5J1-3: 5J4-4 (A)", 7: "5J1-2: 5J4-3 (A)", 8: "5J1-1: 5J4-2 (A)",
	9: "5J2-9: 5J6-9:2J4-3", 10: "5J2-8: 5J6-8:2J4-5", 11: "5J2-6: 5J6-7:2J4-6", 12: "5J2-5",
	13: "5J2-4: 5J6-5", 14: "5J2-3: 5J6-3", 15: "5J5-2: 5J6-2", 16: "5J2-1: 5J6-1",
	17: "5J3-7: 5J7-7", 18: "5J3-6: 5J7-6", 19: "5J3-3: 5J7-3", 20: "5J3-4: 5J7-5", 21: "5J3-2: 5J7-2", 22: "5J3-1: 5J7-1",
	25: "5J5-9 (C)", 26: "5J5-8 (C)", 27: "5J5-7 (C)", 28: "5J5-6 (C)", 29: "5J4-5 (C)", 30: "5J5-4 (C)",
	31: "5J5-3 (C)", 32: "5J5-2 (C)",
}
SOLENOID_DRIVER = {
	1: "Q33", 2: "Q25", 3: "Q32", 4: "Q24", 5: "Q31", 6: "Q23", 7: "Q30", 8: "Q22",
	9: "Q17", 10: "Q9", 11: "Q16", 12: "Q8", 13: "Q15", 14: "Q7", 15: "Q14", 16: "Q6",
	17: "Q75", 18: "Q71", 19: "Q73", 20: "Q69", 21: "Q77", 22: "Q79",
	25: "Q33", 26: "Q25", 27: "Q32", 28: "Q24", 29: "Q31", 30: "Q23", 31: "Q30", 32: "Q22",
}
SOLENOID_PART = {
	1: "AE-23-800", 2: "AE-23-800", 3: "AE-26-1200", 5: "AE-23-800", 6: "AE-23-800", 7: "AE-23-800", 8: "AE-23-800",
	9: "#89 flashlamp", 10: "5580-09555-01", 11: "5580-09555-01", 12: "5580-09555-01",
	13: "#906/#89 flashlamps", 14: "AE-26-1200", 15: "#906/#89 flashlamps", 16: "#906 flashlamp",
	17: "AE-23-800", 18: "AE-26-1500", 19: "AE-23-800", 20: "AE-26-1500", 21: "AE-23-800", 22: "AE-26-1200",
	25: "#906/#89 flashlamps", 26: "#906 flashlamp", 27: "#906/#89 flashlamps", 28: "#906/#89 flashlamps",
	29: "#906/#89 flashlamps", 30: "#906/#89 flashlamps", 31: "#906/#89 flashlamps", 32: "#906/#89 flashlamps",
}
# Printed flashlamp location cells, and their counts: playfield (p) and insert board (i).
FLASHER_PRINTED = {
	9: "3i", 13: "1p,1i", 15: "2p,1i", 16: "2p", 25: "1p,1i", 26: "1p", 27: "1p,1i", 28: "1p,1i",
	29: "2p,1i", 30: "1p,3i", 31: "1p,3i", 32: "1p,1i",
}
FLASHER_BULBS = {
	9: (0, 3), 13: (1, 1), 15: (2, 1), 16: (2, 0),
	25: (1, 1), 26: (1, 0), 27: (1, 1), 28: (1, 1), 29: (2, 1), 30: (1, 3), 31: (1, 3), 32: (1, 1),
}
SOLENOID_KIND = {address: "coil" for address in (1, 2, 3, 4, 5, 6, 7, 8, 14, 17, 18, 19, 20, 21, 22)}
SOLENOID_KIND.update({address: "flasher" for address in (9, 13, 15, 16, 25, 26, 27, 28, 29, 30, 31, 32)})
SOLENOID_KIND.update({10: "gi", 11: "gi", 12: "relay"})
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn", 2: "bsTrough.SolOut", 3: "dtbank.SolDropUp", 5: "bsTP.SolOut", 6: "SolPopper",
	7: "vpmSolSound SoundFX(\"Knocker\",DOFKnocker)", 8: "bsLock.SolOut", 11: "SolGI", 13: "vpmflasher f13",
	14: "SolBoogie", 15: "vpmflasher f15", 16: "vpmflasher array(f16,f16a,f16b)", 22: "SolFlipReset",
	25: "vpmflasher f25", 26: "vpmflasher f26", 27: "vpmflasher f27", 28: "vpmflasher f28",
	29: "vpmflasher f29", 30: "vpmflasher f30", 31: "vpmflasher f31", 32: "vpmflasher f32",
}
SOLENOID_POSITIONS = {
	1: [(0.454331, 0.966750)], 2: [(0.874847, 0.873597)], 3: [(0.606603, 0.376124)],
	5: [(0.488445, 0.102204)], 6: [(0.273117, 0.083053)], 8: [(0.185836, 0.212467)],
	13: [(0.895775, 0.500507)], 14: [(0.276522, 0.151153), (0.337421, 0.124650)], 15: [(0.057306, 0.448722)],
	16: [(0.224693, 0.101030), (0.406670, 0.073041), (0.326994, 0.170765)],
	17: [(0.604813, 0.220739)], 18: [(0.229364, 0.739857)], 19: [(0.812558, 0.221619)],
	20: [(0.681711, 0.735746)], 21: [(0.708029, 0.306336)], 22: [(0.324144, 0.304030), (0.375267, 0.298921)],
	25: [(0.708246, 0.249303)], 26: [(0.639902, 0.358525)], 27: [(0.786568, 0.358255)], 28: [(0.241193, 0.345242)],
	29: [(0.483844, 0.475450)], 30: [(0.761876, 0.800655)], 31: [(0.147195, 0.802395)], 32: [(0.052404, 0.305978)],
}
OBSERVED_SOLENOID_PLACEMENTS = frozenset({15, 16, 29, 32})
CONFLICTED_SOLENOIDS = frozenset({15, 16})
SOLENOID_PROJECTIONS = {
	1: "Projected onto the Drain kicker (Kicker.Drain), the object bsTrough.SolIn kicks from; the manual draws 01A at the outhole.",
	2: "Projected onto the BallRelease kicker (Kicker.BallRelease), the object bsTrough.SolOut ejects from; the manual draws 02A at the shooter-lane feed.",
	3: (
		"Projected onto the centre target of the bank (HitTarget.sw42): one reset coil lifts all three targets, "
		"and the manual draws 03A at the bank."
	),
	5: "Projected onto the eject-hole saucer (Kicker.sw48) that bsTP.SolOut ejects; the manual draws 05A there.",
	6: (
		"Projected onto the popper's saucer (Kicker.sw32). SolPopper lifts the ball from sw32 to the raised kicker "
		"sw32a before bsBP ejects it; the manual draws 06A at the popper."
	),
	8: "Projected onto the lock kicker (Kicker.BallLock) that bsLock.SolOut ejects; the manual draws 08A at the lock release.",
	14: (
		"Two effect placements at the two rubber boogie men (Primitive.boogie1 and Primitive.boogie2) that "
		"SolBoogie moves. The Boogie Monsters Assembly C-12920 has one coil driving a rocker link between two "
		"shafts, so the placements mark where the one coil's effect is seen, not two coils."
	),
	15: (
		"Placed at Light.f15, the one object the script flashes for this address. The location drawing's single "
		"leader for callout 15 ends on the left side rail, which agrees with this position, but the solenoid "
		"table prints two playfield bulbs; observed pending conflict.flasher-bulb-quantities."
	),
	16: (
		"Three placements at Light.f16, f16a and f16b, the array the script flashes for this address. The manual's "
		"location drawing gives callout 16 three leaders in the upper-left quadrant, but the solenoid table prints "
		"\"#906 flashlamp 2p\". Observed pending conflict.flasher-bulb-quantities."
	),
	17: "Projected onto the upper-left bumper (Bumper.Bumper1) whose hit pulses switch 35; the manual draws 17 inside the upper-left bumper.",
	18: "Projected onto the drag-point centroid of Wall.LeftSlingShot; the manual draws 18 inside the left slingshot.",
	19: "Projected onto the upper-right bumper (Bumper.Bumper2) whose hit pulses switch 36; the manual draws 19 inside the upper-right bumper.",
	20: "Projected onto the drag-point centroid of Wall.RightSlingShot; the manual draws 20 inside the right slingshot.",
	21: "Projected onto the lower bumper (Bumper.Bumper3) whose hit pulses switch 37; the manual draws 21 at the lower bumper.",
	22: (
		"Two effect placements at the two flip-up targets (HitTarget.sw53 and sw54) that SolFlipReset resets. One "
		"reset coil (B-12916) serves the Flip Up Targets Assembly; the manual draws 22 at the flip-up targets."
	),
	32: (
		"Placed at Light.f32, the object the script flashes for this address. The manual's leader for 08C runs "
		"toward the skull passage roughly 0.1 lower and further right than this object, so the position is "
		"observed rather than validated."
	),
}

VIRTUAL_SOLENOID_LABELS = {
	23: "PinMAME Flipper/Switched-Solenoid Enable State", 24: "Unassigned Solenoid Slot 24",
	33: "Unused Upper Flipper Coil 33", 34: "Unused Upper Flipper Coil 34",
	35: "Unused Upper Flipper Coil 35", 36: "Unused Upper Flipper Coil 36",
	37: "Unused Sound Overlay Board Slot 37", 38: "Unused Sound Overlay Board Slot 38",
	39: "Unused Sound Overlay Board Slot 39", 40: "Unused Sound Overlay Board Slot 40",
	41: "Unused Sound Overlay Board Slot 41", 42: "Unused Sound Overlay Board Slot 42",
	43: "Unused Sound Overlay Board Slot 43", 44: "Unused Sound Overlay Board Slot 44",
	45: "Synthetic Lower Right Flipper Power", 46: "Synthetic Lower Right Flipper Hold",
	47: "Synthetic Lower Left Flipper Power", 48: "Synthetic Lower Left Flipper Hold",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Unassigned Solenoid Slot 50",
}
VIRTUAL_SOLENOID_NOTES = {
	23: (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL: the flipper and switched-solenoid enable set from PIA0 CB2, "
		"gating both the six special solenoids and the synthetic flipper outputs 45-48. It has no driver "
		"transistor and no Sol. No. in the manual; the manual's flipper rows take their CPU-board feed from "
		"1P19-1 and 1P19-2 on the special-solenoid connector this enable controls. The retained script binds no "
		"callback to it."
	),
	24: "Unassigned platform gap between the enable state (23) and the C-side bank (25-32).",
	33: (
		"Platform upper-flipper address (CORE_FIRSTUFLIPSOL = 33). eatpmGameData's hw.flippers is FLIP_SWNO(58,57), "
		"which sets no FLIP_SW or FLIP_SOL bit for either upper position, and core_getSol serves 33-36 only for "
		"WPC and S.A.M. generations, so this address always reads zero. The machine has two flippers."
	),
	45: (
		"PinMAME's synthetic lower-right-flipper power output (CORE_FIRSTLFLIPSOL = 45). FLIP_SWNO(58,57) with no "
		"FLIP_SOL bit makes core_updateSw fabricate 45-48 from live flipper-button state, gated by ssEn. The "
		"manual confirms no driver-board output exists: its flipper rows carry no Sol. No. and no driver "
		"transistor, and note [1] says the CPU-board wire runs to the flipper switch. The button state it uses "
		"comes from PinMAME's flipper switch column, public 82 (right) and 84 (left), not from matrix 57/58; "
		"see switch 57."
	),
	49: (
		"CORE_FIRSTSIMSOL (sim.h sShooterRel): the fake ball-shooter solenoid the driver's preliminary built-in "
		"simulator uses in its stShooter state. It carries state only while PinMAME keyboard handling runs the "
		"simulator; it is not a machine output."
	),
	50: (
		"Unassigned platform gap. eatpmGameData declares no custSol, so MACHINE_INIT(s11) sizes nSolenoids as "
		"CORE_FIRSTCUSTSOL - 1 = 50 and addresses 51 and above are not modelled for this game."
	),
}
UPPER_FLIPPER_SLOT_NOTE = "Platform upper-flipper address; always zero on this machine, see address 33."
OVERLAY_SLOT_NOTE = (
	"Platform sound-overlay address range 37-44. eatpmGameData's hw.gameSpecific1 is S11_MUXSW2 alone, so "
	"S11_SNDOVERLAY is unset and pia5cb2_w never turns the sound byte into a solenoid pattern. The manual's "
	"solenoid table ends at 22 plus the flippers."
)
SYNTHETIC_FLIPPER_SLOT_NOTE = {
	46: (
		"PinMAME's synthetic lower-right-flipper hold output; see address 45. The retained script binds "
		"SolCallback(sLRFlipper) = SolRFlipper, and the VPinMAME core.vbs it loads through S11.VBS defines "
		"sLRFlipper = 46 (retained copy, excerpt vpm-script-library-flippers), so the table's right flipper "
		"follows this address."
	),
	47: (
		"PinMAME's synthetic lower-left-flipper power output; see address 45. Its button is matrix switch 58 "
		"(FLIP_SWL of FLIP_SWNO(58,57))."
	),
	48: (
		"PinMAME's synthetic lower-left-flipper hold output; see address 47. The retained script binds "
		"SolCallback(sLLFlipper) = SolLFlipper, and core.vbs defines sLLFlipper = 48 (retained copy), so the "
		"table's left flipper follows this address."
	),
}

# --- Lamp matrix (public address = (column-1)*8+row).
LAMP_LABELS = {
	1: "E", 2: "L", 3: "V", 4: "I", 5: "R", 6: "A", 7: "2X", 8: "3X", 9: "4X", 10: "5X",
	11: "Left Slingshot", 12: "3 Million", 13: "Lock", 14: "Left Flip Up", 15: "Right Flip Up",
	16: "Bonus Held", 17: "Eye 1", 18: "Eye 2", 19: "Shoot Again", 20: "Right Slingshot",
	21: "Dead Head 1T", 22: "Dead Head 2T", 23: "Dead Head 3T", 24: "Dead Head 4T",
	25: "Left Ramp Sign", 26: "Left Ramp Spots Elvira", 27: "Left Ramp Million", 28: "Left Ramp Special",
	29: "Left Outlane", 30: "Right Outlane", 31: "Left Return Lane", 32: "Right Return Lane",
	33: "Right Ramp Potion 1", 34: "Right Ramp Potion 2", 35: "Right Ramp Potion 3", 36: "Right Ramp Potion 4",
	37: "Right Ramp Extra Ball", 38: "J", 39: "A", 40: "M", 41: "Hold Bonus", 42: "Million",
	43: "Barbeque", 44: "Boogie", 45: "B", 46: "A", 47: "T", 48: "Center Jackpot",
	49: "Pizza Standup 1", 50: "Pizza Standup 2", 51: "Pizza Passage 1", 52: "Pizza Passage 2",
	53: "Pizza Passage 3", 54: "Left Thumper Bumper", 55: "Right Thumper Bumper", 56: "Bottom Thumper",
	57: "Dead Head 1", 58: "Dead Head 2", 59: "Dead Head 3",
	60: "Barbeque 1", 61: "Barbeque 2", 62: "Barbeque 3", 63: "Barbeque 4", 64: "Barbeque 5",
}
LAMP_ROLE_CONTEXT = {
	1: "ELVIRA letter", 2: "ELVIRA letter", 3: "ELVIRA letter", 4: "ELVIRA letter", 5: "ELVIRA letter", 6: "ELVIRA letter",
	38: "JAM drop-target letter", 39: "JAM drop-target letter", 40: "JAM drop-target letter",
	45: "BAT lane letter", 46: "BAT lane letter", 47: "BAT lane letter",
}
BACKBOARD_LAMPS = frozenset({57, 58, 59})
BACKBOX_LAMPS = frozenset({60, 61, 62, 63, 64})
UNPLACED_LAMPS = (11, 20)
LAMP_COLUMN_WIRING = {
	1: ("YEL-BRN", "1J7-1", "Q66"), 2: ("YEL-RED", "1J7-2", "Q64"), 3: ("YEL-ORN", "1J7-3", "Q62"),
	4: ("YEL-BLK", "1J7-4", "Q60"), 5: ("YEL-GRN", "1J7-6", "Q58"), 6: ("YEL-BLU", "1J7-7", "Q56"),
	7: ("YEL-VIO", "1J7-8", "Q54"), 8: ("YEL-GRY", "1J7-9", "Q52"),
}
LAMP_ROW_WIRING = {
	1: ("RED-BRN", "1J6-1", "Q80"), 2: ("RED-BLK", "1J6-2", "Q81"), 3: ("RED-ORN", "1J6-3", "Q82"),
	4: ("RED-YEL", "1J6-5", "Q83"), 5: ("RED-GRN", "1J6-6", "Q84"), 6: ("RED-BLU", "1J6-7", "Q85"),
	7: ("RED-VIO", "1J6-8", "Q86"), 8: ("RED-GRY", "1J6-9", "Q87"),
}
LAMP_POSITIONS = {
	1: (0.299238, 0.673951), 2: (0.356749, 0.664706), 3: (0.422138, 0.656790), 4: (0.488183, 0.656474),
	5: (0.551864, 0.660526), 6: (0.614102, 0.670531), 7: (0.346288, 0.736937), 8: (0.563417, 0.738197),
	9: (0.334917, 0.790423), 10: (0.575334, 0.790673), 12: (0.179753, 0.482271), 13: (0.136292, 0.432214),
	14: (0.342831, 0.345010), 15: (0.397584, 0.339912), 16: (0.455882, 0.701156), 17: (0.068008, 0.422524),
	18: (0.122509, 0.413822), 19: (0.457327, 0.892613), 21: (0.195247, 0.536823), 22: (0.195772, 0.562659),
	23: (0.195509, 0.588748), 24: (0.194722, 0.615218), 25: (0.256515, 0.399036), 26: (0.369879, 0.578774),
	27: (0.330488, 0.518302), 28: (0.287946, 0.451560), 29: (0.058824, 0.691562), 30: (0.853598, 0.691752),
	31: (0.138655, 0.680164), 32: (0.772059, 0.679848), 33: (0.605173, 0.528742), 34: (0.678900, 0.543797),
	35: (0.550420, 0.584957), 36: (0.624737, 0.601168), 37: (0.692489, 0.485287), 38: (0.515494, 0.371337),
	39: (0.550945, 0.398408), 40: (0.584559, 0.425510), 41: (0.481092, 0.286808), 42: (0.482931, 0.239868),
	43: (0.487395, 0.183194), 44: (0.489364, 0.141591), 45: (0.602153, 0.077581), 46: (0.707458, 0.077074),
	47: (0.812500, 0.077581), 48: (0.485672, 0.481528), 49: (0.784795, 0.571881), 50: (0.785189, 0.604872),
	51: (0.790244, 0.519449), 52: (0.839089, 0.471070), 53: (0.875985, 0.428834), 54: (0.602454, 0.221176),
	55: (0.803845, 0.222534), 56: (0.708102, 0.307924),
}
LAMP_OBJECTS = {17: "Primitive.L17", 18: "Primitive.L18", 25: "Primitive.L25", 29: "Light.L29", 32: "Light.L32"}

EXCERPTS = [
	("switch-matrix", "PDF page 88, printed page 2-36, Switch Wiring Diagram & Matrix"),
	("switch-locations", "PDF page 89, printed page 2-37, Switch Location Diagram and parts list"),
	("lamp-matrix", "PDF page 90, printed page 2-38, Lamp Wiring Diagram & Matrix"),
	("lamp-locations", "PDF page 91, printed page 2-39, Lamp Location Diagram"),
	("solenoid-table-switched", "PDF page 66, printed page 2-14, Solenoids & Flashers table rows 01A-08C"),
	("solenoid-table-controlled-special", "PDF page 66, printed page 2-14, Solenoids & Flashers table rows 09-22, flippers and notes"),
	("solenoid-flasher-locations", "PDF page 67, printed page 2-15, Solenoids & Flashers Location Diagram"),
	("cabinet-wiring", "PDF page 94, printed page 3-2, ELVIRA Cabinet Wiring"),
	("drop-target-opto-board", "PDF pages 79 and 95, printed pages 2-27 and 3-3, 3-Bank Drop Target Opto Board C-12559"),
	("assemblies-and-rules", "PDF pages 4, 44, 63, 64, 82, 83, 84 and 86: rules, special-solenoid logic, lamp boards, playfield parts, flip-up targets, Boogie Monsters, skull lights and backbox parts"),
	("interconnect-board-optos", "PDF pages 110 and 62, printed pages 3-18 and 2-10, Backbox Interconnect Board schematic and parts list: opto isolators U1-U3"),
]
EXCERPT_DERIVATIONS = {
	"switch-matrix": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 88, crop box 0.07,0.555,0.85,0.875, scanned page rendered at its native resolution (embedded image xref 1519, 2562px across 8.54in), rendered at 189 dpi, capped to 1250px wide, grayscale, 1251x664 WebP quality 70",
	"switch-locations": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 89, crop box 0.14,0.08,0.95,0.93, scanned page rendered at its native resolution (embedded image xref 1517, 2562px across 8.54in), rendered at 300 dpi, grayscale, 2066x2805 WebP quality 80",
	"lamp-matrix": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 90, crop box 0.06,0.555,0.83,0.875, scanned page rendered at its native resolution (embedded image xref 1514, 2556px across 8.52in), rendered at 191 dpi, capped to 1250px wide, grayscale, 1251x674 WebP quality 70",
	"lamp-locations": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 91, crop box 0.3,0.1,0.8,0.9, scanned page rendered at its native resolution (embedded image xref 1512, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1275x2640 WebP quality 80",
	"solenoid-table-switched": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 66, crop box 0.07,0.1,0.83,0.425, scanned page rendered at its native resolution (embedded image xref 1571, 2556px across 8.52in), rendered at 186 dpi, capped to 1200px wide, grayscale, 1201x665 WebP quality 66",
	"solenoid-table-controlled-special": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 66, crop box 0.07,0.42,0.83,0.69, scanned page rendered at its native resolution (embedded image xref 1571, 2556px across 8.52in), rendered at 170 dpi, capped to 1100px wide, grayscale, 1101x507 WebP quality 62",
	"solenoid-flasher-locations": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 67, crop box 0.2,0.1,0.87,0.9, scanned page rendered at its native resolution (embedded image xref 1568, 2556px across 8.52in), rendered at 300 dpi, grayscale, 1709x2640 WebP quality 80",
	"cabinet-wiring": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 94, crop box 0.1,0.17,0.86,0.8, scanned page rendered at its native resolution (embedded image xref 1505, 2562px across 8.54in), rendered at 300 dpi, grayscale, 1938x2079 WebP quality 80",
	"drop-target-opto-board": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 95, crop box 0.27,0.52,0.82,0.93, scanned page rendered at its native resolution (embedded image xref 1502, 2550px across 8.50in), rendered at 300 dpi, grayscale, 1403x1353 WebP quality 76",
	"interconnect-board-optos": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 110, crop box 0.57,0.03,0.78,0.56, scanned page rendered at its native resolution (embedded image xref 1458, 5119px across 17.06in), rendered at 300 dpi, grayscale, 1071x1749 WebP quality 70",
	"assemblies-and-rules": "Elvira_and_the_Partymonsters_OCR_searchable.pdf page 82, crop box 0.06,0.1,0.86,0.8, scanned page rendered at its native resolution (embedded image xref 1533, 2569px across 8.56in), rendered at 162 dpi, capped to 1100px wide, grayscale, 1101x1247 WebP quality 64",
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Elvira retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Elvira extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Elvira retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError("Elvira retained extraction manifest does not match the files on disk")
	files = actual["files"]
	identity = (len(files), sum(item["size"] for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"Elvira retained extraction identity mismatch: {identity}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str, status: str = "validated") -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield",
			"x": round(x, 6), "y": round(y, 6), "provenance": provenance(*source_refs, status=status),
		})
	return {"status": status, "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(address: int) -> str:
	return f"device.{slug(SOLENOID_LABELS[address])}"


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def excerpt_records(root: Path = ROOT) -> list[dict[str, Any]]:
	records = []
	for name, locator in EXCERPTS:
		markdown = f"{EXCERPT_DIR}/{name}.md"
		image = f"{EXCERPT_DIR}/{name}.webp"
		records.append({
			"id": f"excerpt.elvira.{name}",
			"locator": locator,
			"path": markdown,
			"sha256": _file_sha256(root / markdown),
			"image": image,
			"image_sha256": _file_sha256(root / image),
			"image_derivation": EXCERPT_DERIVATIONS[name],
			"method": "manual",
			"transcribed_by": "curator, read from the native-resolution render",
			"reviewed": True,
		})
	return records


def source_records(root: Path = ROOT) -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": "PinmameGetGames records for eatpm_l4 and its seven clones",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/s11/prelim/eatpm.c: S11_INPUT_PORTS_START(eatpm,3) at lines 37-48; the *** PRELIMINARY *** "
				"simulator #define block at lines 53-112 and eatpm_stateDef (cross-reference only); S11_ROMSTART48 sets "
				"at lines 200-270 (eatpm_3g's U26 flagged BAD_DUMP); MACHINE_DRIVER_START(elvira) importing s11_s11aS at "
				"lines 275-279; CORE_GAMEDEF(eatpm,l4) and CORE_CLONEDEF for l1/f1/l2/3g/4g/4u/p7 at lines 281-288; "
				"eatpmSimData at 293-303; dispeatpm {0,0,0,16,CORE_SEG16},{0,33,20,16,CORE_SEG16} at 308-310; "
				"eatpmGameData = {GEN_S11B, dispeatpm, {FLIP_SWNO(swLFlip,swRFlip),0,0,0,0,S11_LOWALPHA|S11_DISPINV,"
				"S11_MUXSW2}, &eatpmSimData, {{0}}, {12}} at 312-316 (swLFlip = 58, swRFlip = 57; wpc.invSw all zero; "
				"sxx.muxSol = 12; sxx.ssSw all zero). src/wpc/s11.c: s11_irqline/s11_irq periodic interrupt with the "
				"Advance and Up/Down inputs on PIA2 CA1/CB1 (lines 101-127); setSSSol with ssSolNo = {{5,4,1,2,0,3},"
				"{3,4,5,1,0,2}} (lines 537-556); updsol and the sxx.muxSol-gated C-side copy into bits 24-31 "
				"(lines 558-575); pia1ca2_w..pia4cb2_w -> setSSSol handlers 0-5 (lines 618-623) with the PIA comment "
				"block naming them F SS6, E SS5, B SST2, C SST3, A SS1, D SS4 (lines 700-760); SWITCH_UPDATE(s11) "
				"copying the keyboard port into matrix columns 0 and 1 and, because S11_MUXSW2 is set, writing "
				"core_getSol(12) to switch 2 (lines 774-797); MACHINE_INIT(s11) nSolenoids sizing (line 873) and the "
				"eatpm_ output-type block (lines 977-984: 9 #89, 10 and 11 #44 AC GI, 13 #89, 15-16 #89, 25-32 eight "
				"muxed #89 outputs); s11_s11aS (lines 1376-1383). src/wpc/s11.h: S11_COMPORTS (lines 9-28), "
				"S11_LOWALPHA/S11_DISPINV/S11_MUXSW2/S11_SNDOVERLAY (lines 222-226), s11_mS11BS = s11_s11aS (line 209). "
				"src/wpc/gen.h GEN_S11B = GEN_S11X = 0x100. src/wpc/sim.h sShooterRel = CORE_FIRSTSIMSOL. "
				"src/wpc/core.h CORE_FIRSTSSSOL = 17, CORE_SSFLIPENSOL = 23, CORE_FIRSTUFLIPSOL = 33, "
				"CORE_FIRSTLFLIPSOL = 45, CORE_FIRSTSIMSOL = 49, CORE_FIRSTCUSTSOL = 51. src/wpc/core.c core_swSeq2m, "
				"core_updateSw synthetic-flipper fallback, core_getSol GEN_ALLS11 branch."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json",
			"revision": "repository",
			"locator": (
				"System 11 sequential column-major switch and lamp numbering 1-64, the four negative diagnostic "
				"addresses, the Country jumper, and the switched/controlled/special/A-C-mux/overlay/synthetic-flipper "
				"solenoid address rules"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.elvira-and-the-party-monsters.1989/Elvira_and_the_Partymonsters_OCR_searchable.pdf",
			"original_filename": "Elvira_and_the_Partymonsters_OCR_searchable.pdf", "sha256": MANUAL_SHA256,
			"acquired_at": "2026-09-25T11:43:00Z",
			"locator": (
				"118-page Bally Midway Elvira and the Party Monsters Operations and Parts Information Manual "
				"16-2011-101, August 1989, scanned at 300 dpi with an Acrobat Paper Capture text layer. IPDB machine "
				"782 (https://www.ipdb.org/machine.cgi?id=782, Midway 'Elvira and the Party Monsters', September 05, "
				"1989, model 2011, System 11B), resource https://www.ipdb.org/files/782/Elvira_and_the_Partymonsters_OCR_searchable.pdf, "
				"downloaded through the contributor's browser because IPDB is Cloudflare-gated; the untouched download "
				"is retained under this hash and the saved IPDB machine page beside it. Printed page = PDF page - 52 "
				"through Section 2; PDF 2 is an unpaginated ROM and solenoid summary, PDF 4 the rules page, PDF 117 a "
				"quick-reference switch and lamp matrix page. The text layer mis-orders some tables, so every cited "
				"table was read from the rendered page."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company (Bally); scan hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
			"excerpts": excerpt_records(root),
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/elvira-and-the-party-monsters-1989/Elvira%20and%20the%20Party%20Monsters%20%28Bally%201989%29%20nude.vpx",
			"original_filename": "Elvira and the Party Monsters (Bally 1989) nude.vpx", "sha256": TABLE_SHA256,
			"locator": (
				"Retained VPX table from the contributor's table collection (dated 2020-01-20): an artwork variant of "
				"the 32assassin Elvira and the Party Monsters table, whose script is the same lineage as the pinned "
				f"corpus v1.03 script. Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/952 and "
				"y/1974. Geometry authority for named, script-bound table objects only, and only where the manual's "
				"numbered location drawings agree."
			),
			"license": "NOASSERTION", "attribution": "32assassin (table); artwork modification author unrecorded",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/elvira-and-the-party-monsters-1989/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Embedded script of the retained table (33,177 bytes): cGameName = \"eatpm_l4\", UseSolenoids = 1, "
				"UseLamps = 0 with an explicit LampTimer/UpdateLamps routine; SolCallback for 1, 2, 3, 5, 6, 7, 8, 11, "
				"13, 14, 15, 16, 22, 25-32 and sLRFlipper/sLLFlipper; bsTrough (9, 11, 12, 13), bsLock (49, 50, 51), "
				"bsTP saucer 48, bsBP saucer 32 with the raised sw32a popper kicker, dtbank (41, 42, 43); switch "
				"handlers for the lanes, targets, bumpers, slingshots and the flip-up targets; flipper keys writing "
				"Controller.Switch 57/58. Full object cross-reference in "
				"external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpx-geometry-raw.tsv."
			),
			"license": "NOASSERTION", "attribution": "32assassin", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/elvira-and-the-party-monsters-1989/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
				f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
				f"bytes, produced with vpxtool git:v0.33.3 from the retained table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{VPXTABLE_SCRIPTS_REVISION}/Elvira%20and%20the%20Party%20Monsters%20%28Bally%201989%29%20v1.03.vbs",
			"revision": VPXTABLE_SCRIPTS_REVISION, "sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				"Elvira and the Party Monsters (Bally 1989) v1.03.vbs (129,154 bytes) in the pinned corpus: the same "
				"32assassin table with updated physics, cGameName = \"eatpm_l4\", UseSolenoids = 2 and the identical "
				"SolCallback table, trough/lock/saucer/drop-target helpers, flip-up target handlers and "
				"UpdateLamps bindings (including the same lamp 54 binding on the 55 and 56 bumper bodies). Same "
				"lineage as the retained script, so it corroborates the bindings without being independent."
			),
			"license": "NOASSERTION", "attribution": "32assassin and later contributors; corpus by sverrewl", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpm-script-libs/s11.vbs",
			"original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads at runtime (script.vbs line 11 LoadVPM "
				"\"01560000\", \"S11.VBS\", 3.26; S11.VBS executes core.vbs), retained from the contributor's working "
				f"installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and "
				"swLLFlip = 84 and sets them from the flipper keys in vpmKeyDown/vpmKeyUp; core.vbs routes "
				"KeyDownHandler to vpmKeyDown and defines sLRFlipper = 46, sLLFlipper = 48."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.elvira.vpm-script-library-flippers",
					"locator": "s11.vbs lines 10-14, 37-40, 69-80 and 104-115; core.vbs lines 2854 and 2861-2865",
					"path": f"{EXCERPT_DIR}/vpm-script-library-flippers.md",
					"sha256": _file_sha256(root / f"{EXCERPT_DIR}/vpm-script-library-flippers.md"),
					"method": "manual",
					"transcribed_by": "curator, read from the installed library files",
					"reviewed": True,
				}
			],
		},
		{
			"id": GEOMETRY_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpx-geometry-raw.tsv",
			"revision": "2026-09-25",
			"locator": (
				"Object-by-object dump of every gameitem in the retained extraction (type, name, centre or drag-point "
				"centroid, normalized x/952 and y/1974, visibility), cross-checked against the manual's switch, lamp "
				"and solenoid location drawings."
			),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		},
	]


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11B CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection,
		"return_component": f"column driver {drive_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append(
			_device(
				f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				roles=[role],
				physical={
					"location": "coin door (Advance, Auto-Up/Manual-Down) and CPU board (diagnostic switches)",
					"switch_type": "button",
					"notes": (
						"System 11 diagnostic input on the upper byte of S11_COMINPORT (core_swSeq2m maps public n to "
						"internal matrix index n+7, so these land in column 0; s11_irqline latches Advance and Up/Down "
						"onto PIA2 CA1/CB1). The manual's Cabinet Wiring (printed 3-2) wires ADVANCE (7SW75) and "
						"AUTO-UP/MANUAL-DOWN (7SW74) through 1J14 pins 3 and 4, beside the Memory Protect switch "
						"(7SW76, 1J14 pin 1), which PinMAME does not publish. The Up/Down input is a PinMAME toggle "
						"(COREPORT_BITTOG)."
					),
				},
				spatial=not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			)
		)

	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		unused = address in UNUSED_MATRIX_ADDRESSES
		identifier = f"switch.matrix-{address}"
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		physical: dict[str, Any] = {}
		if address in SWITCH_PARTS:
			physical["part_number"] = SWITCH_PARTS[address]
		if address in SWITCH_TYPES:
			physical["switch_type"] = SWITCH_TYPES[address]
		notes = f"Printed switch-matrix drive column {column}, return row {row}."
		if unused:
			notes += " The switch location list prints this position \"Not Used\" and the matrix cell carries only its number."
		if address in MATRIX_PAGE_WORDING:
			notes += f" The Switch Matrix page prints \"{MATRIX_PAGE_WORDING[address]}\"; the label is the switch location list wording."
		if address in SWITCH_SCRIPT_BINDING:
			notes += f" Retained script: {SWITCH_SCRIPT_BINDING[address]}."
		if address in SIMULATOR_SYMBOLS:
			notes += (
				f" The driver's preliminary simulator names this address {SIMULATOR_SYMBOLS[address]}, a gameplay "
				"name for the same device."
			)
		if address == 2:
			notes += (
				" Not a playfield switch. eatpmGameData sets S11_MUXSW2 with sxx.muxSol = 12, so SWITCH_UPDATE(s11) "
				"overwrites this address every update with the live state of the A/C Select Relay (solenoid 12). The "
				"manual prints it \"A/C Relay Select\" with \"No part number\"; the Backbox Interconnect Board "
				"schematic (printed 3-18) draws opto isolator U1 (4N25) with its LED fed from the 28V 'C' SIDE supply "
				"and its transistor closing column 1 (GRN/BRN) to row 2 (WHT/RED), so the matrix sees the C-side "
				"supply the relay selects."
			)
		if address == 5:
			notes += " The switch location list prints its part as \"Not Used (USA)\": the centre coin chute is fitted only on non-USA doors."
		if address == 8:
			notes += " Note * on the switch location list: the part number is for the entire Diagnostic Switch Assembly, including the High Score Reset switch."
		if address in (33, 34):
			notes += (
				" Note *** on the switch location list: \"Paired Kicker Actuating Sw: B-12459; B-12715\". This "
				"switch is part of the slingshot assembly and has no separate part number."
			)
		if address in (35, 36, 37):
			notes += " The location list prints \"p/o C-12872\"; the Playfield Parts list prints the Thumper Bumpers assembly as C-12842."
		if address in (41, 42, 43):
			notes += (
				" An opto on the 3-Bank Drop Target Opto Board C-12559: three opto interrupters feed three LM339 "
				"comparator sections whose outputs drive matrix rows through 1N4004 diodes on the drop-target column, "
				"so the board presents each opto to the matrix as an ordinary diode-isolated closure. The retained "
				"script's cvpmDropTarget asserts this address while the target is down and clears it on reset; "
				"eatpmGameData's wpc.invSw is all zero, so PinMAME publishes the matrix unchanged and a consumer "
				"drives 1 for a dropped target. The manual prints no opto legend on the matrix page."
			)
		if address in (53, 54):
			notes += (
				" A standup target switch (SW-1A-170-4, Standup Target Assembly B-11696-4) paired with the flip-up "
				"target. Its runtime role is disputed: see conflict.flip-up-switch-roles."
			)
		if address in (55, 56):
			notes += (
				" The position switch mounted on the Flip Up Targets Assembly C-12922 bracket (printed there as "
				"5674-12073-30, on the location list as 5647-12073-30). Its runtime role is disputed: see "
				"conflict.flip-up-switch-roles."
			)
		if address in (57, 58):
			notes += (
				" Not a playfield switch and not an end-of-stroke contact. The Cabinet Wiring (printed 3-2) draws the "
				"flipper buttons switching the coils directly, and the Backbox Interconnect Board schematic (printed "
				"3-18) senses each flipper circuit with a 4N25 opto isolator whose LED spans the flipper coil's 50 V "
				"supply and coil-return lines: "
				f"{'U3, labelled RT L.C., closes column 8 (GRN/GRY) to row 1 (WHT/BRN)' if address == 57 else 'U2, labelled LT L.C., closes column 8 (GRN/GRY) to row 2 (WHT/RED)'}. "
				"The physical sense therefore closes only while the button is pressed and the flipper circuit "
				"conducts. The switch location list's orphaned note \"**Optotransistor on Backbox Interconnect "
				"Board\" refers to these. "
				"A consumer that drives this address directly is overwritten: with keyboard handling off (the LibPinMAME "
				"default, and the retained script sets HandleKeyboard = 0), core_updateSw reads the cabinet flipper "
				"buttons from PinMAME's flipper switch column and rewrites 57/58 from them on every update. On this "
				"platform that column is public 82 (right button, CORE_SWLRFLIPBUTBIT) and 84 (left button, "
				"CORE_SWLLFLIPBUTBIT), which the VPinMAME S11.VBS library drives from the flipper keys (swLRFlip = 82, "
				"swLLFlip = 84) before the table's own Controller.Switch(57/58) writes. Drive 82/84; they sit outside "
				"the System 11 profile's declared switch ranges and are not enumerated as inputs here."
			)
		if address in SWITCH_PROJECTIONS:
			notes += " " + SWITCH_PROJECTIONS[address]
		physical["notes"] = notes

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address:02d}"},
			],
			"physical": physical,
			"wiring": _switch_wiring(column, row),
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if unused:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif address == 2:
			availability = "used"
			extra["roles"] = ["internal.ac-relay-feedback"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address in (1, 7):
			availability = "used"
			extra["roles"] = ["cabinet.tilt"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in (3, 8):
			availability = "used"
			extra["roles"] = ["cabinet.service"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in (4, 5, 6):
			availability = "used"
			extra["roles"] = ["cabinet.coin"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in (57, 58):
			availability = "used"
			extra["roles"] = ["cabinet.flipper-button"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE)
		else:
			availability = "used"
			status = "observed" if address in OBSERVED_SWITCH_PLACEMENTS else "validated"
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE, status=status)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		device = _device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra)
		if address in (53, 54, 55, 56):
			device["provenance"]["status"] = "conflicted"
		items.append(device)

	items.append(
		_device(
			"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": "0"}],
			physical={
				"location": "System 11B CPU board",
				"switch_type": "dip",
				"notes": (
					"System 11's single Country jumper (S11_COMPORTS port 1, Germany/USA). The manual's ROM and Jumper "
					"Table (PDF page 2) lists the CPU-board jumpers fitted for ELVIRA as W1, 2, 4, 5, 7, 8, 11, 14, 16, "
					"17 and 18, while the Control Board text (printed 1-2) lists W1, W2, W4, W5, W7, W8, W11, W14, W16, "
					"W17 and W19; its adjustment section notes that German ROMs preset certain adjustments."
				),
			},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		)
	)
	return items


def _flasher_note(address: int) -> str:
	playfield, insert = FLASHER_BULBS[address]
	parts = []
	if playfield:
		parts.append(f"{playfield} on the playfield")
	if insert:
		parts.append(f"{insert} on the backbox Insert Board")
	return f" The table's location cell prints \"{FLASHER_PRINTED[address]}\": {' and '.join(parts)}, {playfield + insert} bulbs in total."


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	physical_addresses = list(range(1, 23)) + list(range(25, 33))
	for address in physical_addresses:
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		kind = SOLENOID_KIND[address]
		notes = f"Printed Solenoids & Flashers table row \"{SOLENOID_TABLE_WORDING[address]}\", Solenoid Type \"{SOLENOID_TYPE[address]}\"."
		if 1 <= address <= 8:
			notes += (
				f" Circuit {address:02d}A, pulsed while solenoid 12 (A/C Select Relay) is de-energized; it shares "
				f"driver {SOLENOID_DRIVER[address]} and CPU pin {SOLENOID_CPU[address]} with circuit {address:02d}C "
				f"at public address {address + 24}."
			)
		if 25 <= address <= 32:
			notes += (
				f" Circuit {address - 24:02d}C, pulsed while solenoid 12 (A/C Select Relay) is energized; it shares "
				f"driver {SOLENOID_DRIVER[address]} and CPU pin {SOLENOID_CPU[address - 24]} with circuit "
				f"{address - 24:02d}A at public address {address - 24}. PinMAME's updsol copies the switched byte "
				"into bits 24-31 while solenoid 12 is on, and the eatpm_ MACHINE_INIT block types 25-32 as eight "
				"muxed #89 flashlamp outputs."
			)
		if address in FLASHER_BULBS:
			notes += _flasher_note(address)
		if 17 <= address <= 22:
			notes += (
				f" Special solenoid #{address - 16}. The six special-solenoid PIA handlers are named F SS6, E SS5, B SST2, "
				"C SST3, A SS1 and D SS4 in s11.c's PIA comment block, and setSSSol's Williams permutation "
				"ssSolNo[0] = {5,4,1,2,0,3} maps them back to public 17-22 in SS1-SS6 order, so the printed Special # "
				"and the public address agree. eatpmGameData's sxx.ssSw is empty, so PinMAME does not model the "
				"switch-triggered path; it publishes this address only from the ROM's PIA writes. On the machine the "
				"switch trigger is gated too: the manual's special-solenoid logic (printed 1-38) passes it only "
				"\"Low, with flippers enabled\"."
			)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		elif 17 <= address <= 21:
			notes += " The retained script binds no callback; the table animates the bumper or slingshot from its own switch."
		if address == 4:
			notes += (
				" Printed with a blank Function cell and a blank part-number cell, while the wire, CPU pin, board "
				"terminal and driver are printed because every A/C pair has them on the Aux Power Driver Board. No "
				"callout 04A appears on the location drawing, the retained script binds nothing to 4, and PinMAME "
				"types no bulb there. Recorded as an unfitted position; failing to observe a device is not proof the "
				"ROM never pulses the address."
			)
		if address == 7:
			notes += " Backbox device: the Backbox Parts list prints item 2, Knocker & Bracket Assy B-10686-1, and the location drawing has no 07A callout."
		if address == 9:
			notes += " Backbox device: all three bulbs are on the Insert Board (\"3i\") and the location drawing has no callout 09."
		if address == 10:
			notes += (
				" Backbox device: note [4b] mounts this relay on the Insert Board (Relay Board C-11998-1; the Backbox "
				"Parts list's Bally Insert Assembly includes \"Drop Mount Relay C-11998-1\"). It switches the "
				"backbox insert general illumination. Pinned PinMAME's eatpm_ MACHINE_INIT block comments address 10 "
				"\"Playfield GI output\" and 11 \"Backbox GI output\", the opposite of the manual; both addresses are "
				"typed with the same #44 AC GI bulb model, so the comments do not change what PinMAME publishes. The "
				"retained script binds no callback here."
			)
		if address == 11:
			notes += (
				" Note [4a] mounts this relay on the playfield (Relay Board C-11998-1). It switches playfield general "
				"illumination; the retained script's SolGI handler turns the 29-member GI light collection off while "
				"the relay is energized. The manual enumerates no GI bulb count or socket position, so no spatial "
				"record is asserted. PinMAME's MACHINE_INIT comment calls this address \"Backbox GI output\"; see "
				"address 10."
			)
		if address == 12:
			notes += (
				" Note [5] mounts this relay on the Aux Power Driver Board D-12247 in the backbox. De-energized it "
				"powers the A circuits (public 1-8), energized the C circuits (public 25-32). PinMAME's updsol "
				"multiplexes on it (sxx.muxSol = 12) and SWITCH_UPDATE mirrors its state onto switch 2."
			)
		if address == 14:
			notes += (
				" The Boogie Monsters Assembly C-12920 has one AE-26-1200 coil whose plunger moves a rocker link "
				"between two shafts carrying the two rubber boogie men (23-6639), returned by an extension spring. "
				"No switch is part of the assembly."
			)
		if address == 15:
			notes += (
				" The manual abbreviates the playfield half \"B/board L. Side\", but the location drawing puts the "
				"callout on the left side rail, not on the backboard. The table prints the playfield connection "
				"\"5J5-2: 5J6-2\" where the neighbouring controlled rows print 5J2- pins; transcribed as printed. "
				"See conflict.flasher-bulb-quantities for the bulb count."
			)
		if address == 16:
			notes += " Flashes the Boogie Monsters; see conflict.flasher-bulb-quantities for the bulb count."
		if address == 17:
			notes += " The table prints the CPU pin \"1P10-7\" where the other five special solenoids print 1P19- pins; transcribed as printed."
		if address == 22:
			notes += (
				" Flip Up Reset Coil Assembly B-12916 (bell armature A-6306-1, coil AE-26-1200). One coil resets both "
				"flip-up targets; the retained script's SolFlipReset clears switches 53 and 54 and restores both "
				"coffin visuals."
			)
		if address == 29:
			notes += (
				" The table prints the C-side connection \"5J4-5 (C)\", the same pin as 05A, where every other C row "
				"prints a 5J5- pin; transcribed as printed. The retained table has one flasher object for two "
				"playfield bulbs, so one observed placement is recorded against two playfield bulbs."
			)
		if address in SOLENOID_PROJECTIONS:
			notes += " " + SOLENOID_PROJECTIONS[address]

		wiring: dict[str, Any] = {
			"board": "System 11B CPU board",
			"driver_transistor": SOLENOID_DRIVER[address],
			"drive_wire": SOLENOID_WIRE[address],
			"power_connection": SOLENOID_POWER[address],
		}
		if address in SOLENOID_CPU:
			wiring["control_connection"] = SOLENOID_CPU[address]
		if address in CONTROL_WIRE:
			wiring["control_wire"] = CONTROL_WIRE[address]
		if 25 <= address <= 32:
			wiring["control_connection"] = SOLENOID_CPU[address - 24]
			wiring["control_wire"] = CONTROL_WIRE[address - 24]
		physical: dict[str, Any] = {"notes": notes}
		if address in SOLENOID_PART:
			physical["part_number"] = SOLENOID_PART[address]
		if address in FLASHER_BULBS and address != 16:
			physical["quantity"] = sum(FLASHER_BULBS[address])
		manual_alias = SOLENOID_TABLE_WORDING[address].split(" ", 1)[0]
		aliases = [
			{"namespace": "pinmame.solenoid", "value": str(address)},
			{"namespace": "manual.address", "value": manual_alias},
		]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		availability = "used"
		if address == 4:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif address == 7:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 9:
			extra["roles"] = ["cabinet.backbox-flasher"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 10:
			extra["roles"] = ["gi.backbox-insert"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 11:
			extra["roles"] = ["gi.playfield"]
		elif address == 12:
			extra["roles"] = ["internal.ac-select-relay"]
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		else:
			role = "emitter" if kind == "flasher" else "effect"
			status = "observed" if address in OBSERVED_SOLENOID_PLACEMENTS else "validated"
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE, status=status)
		device = _device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra)
		if address in CONFLICTED_SOLENOIDS:
			device["provenance"]["status"] = "conflicted"
		items.append(device)

	for address in list(range(23, 25)) + list(range(33, 51)):
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = f"device.{slug(label)}"
		if address in VIRTUAL_SOLENOID_NOTES:
			notes = VIRTUAL_SOLENOID_NOTES[address]
		elif 34 <= address <= 36:
			notes = UPPER_FLIPPER_SLOT_NOTE
		elif 37 <= address <= 44:
			notes = OVERLAY_SLOT_NOTE
		else:
			notes = SYNTHETIC_FLIPPER_SLOT_NOTE[address]
		if address == 23:
			roles = ["internal.game-on-enable"]
		elif 45 <= address <= 48:
			roles = ["internal.synthetic-flipper"]
		elif address == 49:
			roles = ["internal.simulator-channel"]
		else:
			roles = ["internal.unused-platform-slot"]
		used = address in (23, 45, 46, 47, 48, 49)
		items.append(
			_device(
				identifier, label, "virtual", "pinmame.output.solenoid", address,
				"used" if used else "unused",
				(CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE) if address in (23, 45) else (CONTROLLER_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE) if address in (46, 48) else (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"lamp.matrix-{address}"
		label = LAMP_LABELS[address]
		notes = f"Printed lamp-matrix drive column {column}, return row {row}."
		if address in LAMP_ROLE_CONTEXT:
			notes += f" Insert role: {LAMP_ROLE_CONTEXT[address]}."
		object_name = LAMP_OBJECTS.get(address, f"Light.l{address}")
		if address in (17, 18):
			notes += (
				" A skull eye in the Skull Bracket and Lights Assembly B-13069, whose parts list includes a green "
				f"light bulb sleeve (03-8063-2). The retained script drives {object_name} (the green bulb cover) and "
				f"the glow Flasher.fl{address} for this address, but the two glow objects sit beside the opposite "
				"eyes' covers. The placement is the bulb cover, which matches the Lamp Location Diagram's ordering "
				"(18 above and right of 17)."
			)
		if address == 25:
			notes += " The retained script drives the red bulb cover Primitive.L25 (commented \"Ramp Entrance RED LED\") and the glow Flasher.fl25 for this address; the placement is the bulb cover."
		if address in (21, 22, 23, 24):
			notes += (
				f" The retained script also drives Light.l{address}a beside the standup target; the manual shows one "
				f"insert per address, so only Light.l{address} is placed."
			)
		if address == 54:
			notes += " Inside the upper-left bumper; the script's co-located l54a/l54b helpers are not separate bulbs."
		if address in (55, 56):
			notes += (
				f" Inside the {'upper-right' if address == 55 else 'lower'} bumper. The retained script (and the corpus "
				f"v1.03 script) drives Light.l{address} from lamp 54's state and only its l{address}a/l{address}b "
				f"helpers from this address, a table defect; the placement is Light.l{address}'s centre."
			)
		if address in (11, 20):
			notes += (
				" The lamp matrix prints this address \"Left Slingshot\"" if address == 11 else
				" The lamp matrix prints this address \"Right Slingshot\""
			)
			notes += (
				", and the retained script drives the lights inside that slingshot "
				f"({'l11, l11a, L11b, L11c' if address == 11 else 'l20, l20a, L20b, L20c'}). The manual's Lamp Location "
				f"Diagram prints {address} inside the {'right' if address == 11 else 'left'} slingshot instead. No "
				"spatial record is asserted until conflict.slingshot-lamp-sides is resolved."
			)
		if address in BACKBOARD_LAMPS:
			notes += (
				" A backboard lamp, not a playfield insert: the rules page says completing the four Dead Head "
				"standups lights one Dead Head on the Backboard, the Lamp Boards page lists a 3-Lamp Back Stop "
				"C-13066, and the playfield lamp drawing has no callout for 57-64. The retained script flashes "
				f"Flasher.f{address} (commented \"BackWall\") at the rear edge as a visual proxy."
			)
		if address in BACKBOX_LAMPS:
			notes += (
				" A backbox lamp, not a playfield insert: the playfield lamp drawing has no callout for 57-64, and "
				f"the retained script flashes Flasher.l{address} (commented \"BackGlass\"), an object placed beyond "
				"the playfield's right edge."
			)
		physical: dict[str, Any] = {"notes": notes}
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.lamp", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address:02d}"},
			],
			"physical": physical,
			"wiring": {
				"board": "System 11B CPU board",
				"drive_wire": LAMP_COLUMN_WIRING[column][0],
				"drive_connection": LAMP_COLUMN_WIRING[column][1],
				"return_wire": LAMP_ROW_WIRING[row][0],
				"return_connection": LAMP_ROW_WIRING[row][1],
				"driver_transistor": f"column driver {LAMP_COLUMN_WIRING[column][2]}, row driver {LAMP_ROW_WIRING[row][2]}",
			},
		}
		if address in BACKBOARD_LAMPS:
			extra["roles"] = ["cabinet.backboard-indicator"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address in BACKBOX_LAMPS:
			extra["roles"] = ["cabinet.backglass-indicator"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address in UNPLACED_LAMPS:
			pass
		else:
			extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, MANUAL_SOURCE)
		device = _device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra)
		if address in UNPLACED_LAMPS:
			device["provenance"]["status"] = "conflicted"
		items.append(device)
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index,
			"segment_start": start, "width": 16, "height": 1,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}

	return [
		display("display.left-alphanumeric", "Left 16-character alphanumeric display (Player 1 and 2 scores), Bally Left Display Bd D-12706, called the Hi-Display Board on printed 1-2", 0, 0),
		display("display.right-alphanumeric", "Right 16-character alphanumeric display (Player 3 and 4 scores), Bally Right Display Bd D-12502-1, called the Lo-Display Board on printed 1-2", 1, 20),
	]


def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly_part_number: str | None = None, status: str = "validated") -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		"behavior": behavior, "provenance": provenance(*refs, status=status),
	}
	if assembly_part_number:
		record["assembly_part_number"] = assembly_part_number
	return record


def mechanisms() -> list[dict[str, Any]]:
	return [
		mechanism(
			"mechanism.trough", "Outhole, three-ball trough and shooter-lane feeder", "kicker",
			[output_id(1), output_id(2)], ["switch.matrix-9", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-21"],
			"A drained ball lands in the outhole (switch 9) and solenoid 1 (Outhole Kicker, AE-23-800, circuit 01A) "
			"kicks it into the trough, where up to three balls rest on switches 11 (Trough 1, Right), 12 (Trough 2, "
			"Middle) and 13 (Trough 3, Left). Solenoid 2 (Ball Eject, Shooter Lane Feeder assembly C-9638, "
			"AE-23-800, circuit 02A) feeds the ball nearest the shooter, on switch 11, into the shooter lane "
			"(switch 21). Both coils are A-side circuits, so the ROM fires them with the A/C relay (solenoid 12) "
			"de-energized. The retained script models the stack with bsTrough.InitSw 9, 11, 12, 13 and "
			"bsTrough.InitKick BallRelease.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="B-8623",
		),
		mechanism(
			"mechanism.drop-targets", "JAM 3-bank drop targets", "drop_target_bank",
			[output_id(3)], ["switch.matrix-41", "switch.matrix-42", "switch.matrix-43"],
			"Three drop targets lettered J, A, M (switches 41, 42, 43, lamps 38, 39, 40) on the 3-Bank Drop Target "
			"assembly C-11223-1, sensed by the three optos of board C-12559 rather than by leaf switches. Solenoid 3 "
			"(Drop Target Bank, AE-26-1200, circuit 03A) resets all three together. Completing JAM enables a ball "
			"lock if needed and builds BOOGIE BONUS on the eject hole (rules page). The retained script uses one "
			"cvpmDropTarget over sw41-sw43 with dtbank.SolDropUp on solenoid 3.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="C-11223-1",
		),
		mechanism(
			"mechanism.ball-lock", "Skull ball lock", "kicker",
			[output_id(8)], ["switch.matrix-29", "switch.matrix-49", "switch.matrix-50", "switch.matrix-51", "switch.matrix-52"],
			"The lock lane on the upper left (entered past Lock Entry, switch 29) queues up to three balls on Lock 1, "
			"2 and 3 (switches 49, 50, 51) above Lock Safety (switch 52). Solenoid 8 (Ball Lock Release, Ball Lock "
			"Kicker B-11051-R with coil B-9362-R-1, circuit 08A) releases a ball. The rules page: completing the "
			"B-A-T lanes or the JAM targets enables the Skull to lock a ball, and going through the Skull locks "
			"balls if enabled. The retained script models it with bsLock.InitSw 0, 49, 50, 51 kicking from "
			"Kicker.BallLock and pulses 52 from its own trigger.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="B-11051-R",
		),
		mechanism(
			"mechanism.eject-hole", "Eject hole", "kicker",
			[output_id(5)], ["switch.matrix-48"],
			"A saucer at the top centre (switch 48, Ball Eject Hole B-9361-R-1) ejected by solenoid 5 (coil "
			"B-9362-R-1, circuit 05A). The Hold Bonus, Million, Barbeque and Boogie awards on lamps 41-44 are "
			"collected here. The retained script models it with bsTP.InitSaucer sw48.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="B-9361-R-1",
		),
		mechanism(
			"mechanism.ball-popper", "Ball popper", "kicker",
			[output_id(6)], ["switch.matrix-32"],
			"A ball in the upper-left popper (switch 32, Ball Popper D-11335-1) is popped up by solenoid 6 "
			"(AE-23-800, circuit 06A) onto the Popper Wire Ramp (12-6860). The retained script's SolPopper lifts the "
			"ball from Kicker.sw32 to the raised Kicker.sw32a and then ejects it with bsBP.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="D-11335-1",
		),
		mechanism(
			"mechanism.flip-up-targets", "Two flip-up targets with a shared reset coil", "other",
			[output_id(22)], ["switch.matrix-53", "switch.matrix-54", "switch.matrix-55", "switch.matrix-56"],
			"Two flip-up targets below the left ramp (Flip Up Targets Assembly C-12922, each with a Standup Target "
			"Assembly B-11696-4). Each position has a standup target switch (53, 54; SW-1A-170-4) and a position "
			"switch on the flip-up bracket (55, 56 \"Flip Up #1/#2 Open\"). A hit flips the top target over; one "
			"reset coil (solenoid 22, Flip Up Reset Coil Assembly B-12916, Special #6) restores both. Completing both "
			"lights BARBEQUE on the eject hole. The retained script instead holds 53/54 closed from the hit until "
			"SolFlipReset and only pulses 55/56 once, which disagrees with the parts layout about which switch "
			"reports the flipped state; see conflict.flip-up-switch-roles.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="C-12922", status="conflicted",
		),
		mechanism(
			"mechanism.boogie-monsters", "Boogie Monsters", "toy",
			[output_id(14), output_id(16)], [],
			"Two rubber boogie men (23-6639) on two shafts joined by a rocker link (Boogie Monsters Assembly C-12920). "
			"Solenoid 14 (AE-26-1200) pulls one end of the link so both figures move, and an extension spring "
			"returns them; the assembly has no switch. Solenoid 16 flashes the Boogie Monsters flashlamps. The "
			"retained script's SolBoogie shifts boogie1 and boogie2 in opposite directions while 14 is on.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="C-12920",
		),
		mechanism(
			"mechanism.ramps", "Monster Slide and Party Punch ramps", "other",
			[], ["switch.matrix-30", "switch.matrix-31", "switch.matrix-44"],
			"The left ramp is the Monster Slide (L. (Monster Slide) Ramp D-13007) with Left Ramp Entry (switch 30, "
			"Switch Gate Assy A-13068) and Left Ramp End (switch 31); the right ramp is the Party Punch (R. (Party "
			"Punch) Ramp D-13008) with Right Ramp Entry (switch 44, A-13068). The playfield parts also list an R. "
			"(Slide Return) Ramp D-13006 and a Release (Metal) Ramp B-13011. No coil acts on either ramp.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers", "Three thumper bumpers", "kicker",
			[output_id(17), output_id(19), output_id(21)], ["switch.matrix-35", "switch.matrix-36", "switch.matrix-37"],
			"Left, right and bottom thumper bumpers (Thumper Bumpers C-12842) with switches 35, 36, 37 and special "
			"solenoids 17, 19, 21 (AE-23-800), and lamps 54, 55, 56 inside them. Actuating the bumpers increases "
			"BOOGIE BONUS when lit (rules page).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="C-12842",
		),
		mechanism(
			"mechanism.slingshots", "Two slingshots", "kicker",
			[output_id(18), output_id(20)], ["switch.matrix-33", "switch.matrix-34"],
			"Left and right slingshot kickers (B-12665 with coils B-11203-L-1 and B-11203-R-1, AE-26-1500) on "
			"special solenoids 18 and 20, actuated by the paired kicker switches 33 and 34.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="B-12665",
		),
		mechanism(
			"mechanism.flippers", "Two cabinet-wired flippers", "other",
			[f"device.{slug(VIRTUAL_SOLENOID_LABELS[45])}", f"device.{slug(VIRTUAL_SOLENOID_LABELS[47])}"],
			["switch.matrix-57", "switch.matrix-58"],
			"Left and right flipper assemblies (C-11626-L-3, C-11626-R-3, coils FL-11630/50VDC) wired from the "
			"cabinet buttons straight to the coils (Cabinet Wiring, printed 3-2), enabled through 1P19. The CPU "
			"reads the buttons on switches 57 (right) and 58 (left) through opto isolators U3 and U2 on the "
			"Backbox Interconnect Board, whose LEDs span each coil's supply and return. PinMAME rewrites 57/58 "
			"from its flipper switch column, public 82 (right) and 84 (left), which is what a recreation must "
			"drive. There is no CPU-driven flipper coil "
			"and no end-of-stroke switch in the matrix; PinMAME fabricates 45-48 from the button state.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, VPM_LIBRARY_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other",
			[output_id(7)], [],
			"Solenoid 7 (circuit 07A, AE-23-800) raps the Knocker & Bracket Assy B-10686-1 in the backbox.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE, assembly_part_number="B-10686-1",
		),
	]


# Printed special-solenoid pairing: each special solenoid is fired in hardware through its Special Switch
# Trigger input (manual printed 1-38 "on" state logic), paired here with the switch the manual names for
# the same device.
SPECIAL_SOLENOID_SWITCH = {17: 35, 18: 33, 19: 36, 20: 34, 21: 37}


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": f"relationship.special-solenoid-{solenoid}",
			"kind": "direct",
			"source": f"switch.matrix-{switch}",
			"destination": output_id(solenoid),
			"provenance": provenance(MANUAL_SOURCE),
		}
		for solenoid, switch in sorted(SPECIAL_SOLENOID_SWITCH.items())
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.slingshot-lamp-sides",
			"path": "outputs[binding.group=pinmame.output.lamp,binding.device=11|20]",
			"description": (
				"The manual disagrees with itself about which slingshot carries lamps 11 and 20. The Lamp Wiring "
				"Diagram & Matrix (printed 2-38) and its two repeats (printed 1-36 and PDF page 117) name 11 \"Left "
				"Slingshot\" and 20 \"Right Slingshot\", and the retained known-working script drives the lights "
				"inside the left slingshot from 11 and inside the right slingshot from 20. The Lamp Location "
				"Diagram (printed 2-39) prints callout 20 inside the left slingshot and 11 inside the right. The "
				"script follows the matrix names, so it cannot independently confirm the physical wiring. Both "
				"lamps are recorded with their matrix labels and without spatial records. Resolution path: a "
				"Single Lamps diagnostic on a real machine (the manual's test 04 blinks one address at a time) or a "
				"look at the wire colours at the left slingshot insert (YEL-RED/RED-ORN for 11, YEL-ORN/RED-YEL for "
				"20), which an owner or a photograph of an unrestored underside can supply."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
		},
		{
			"id": "conflict.flasher-bulb-quantities",
			"path": "outputs[binding.group=pinmame.output.solenoid,binding.device=15|16]",
			"description": (
				"Two flasher circuits have different bulb counts in the table and in the location drawing of the "
				"same manual. The Solenoids & Flashers table (printed 2-14) prints 16 Boogie Monsters \"#906 flashlamp "
				"2p\", but the Solenoids & Flashers Location Diagram (printed 2-15) draws three leaders from callout "
				"16, and the retained script flashes three objects (f16, f16a, f16b) for it. The same table prints "
				"15 \"#906/#89 flashlamps 2p,1i\", but the drawing gives callout 15 one leader and the script one "
				"object. Address 16 carries three observed placements and no quantity; address 15 records the "
				"table's total of three bulbs with one placement. Resolution path: counting the #906 sockets on the "
				"Boogie Men area and along the left rail of a real playfield, or a Williams parts catalogue listing "
				"the flasher socket harness for these circuits."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
		},
		{
			"id": "conflict.flip-up-switch-roles",
			"path": "mechanisms[id=mechanism.flip-up-targets]",
			"description": (
				"The manual and the retained script describe the flip-up target switches differently, and the "
				"difference changes what a recreation must hold. The manual's parts pages give each flip-up two "
				"switches: a standup target switch (53, 54; SW-1A-170-4 in the Standup Target Assembly) and a "
				"switch mounted on the flip-up bracket under the pivot (55, 56, printed \"Flip Up #1/#2 Open\"), "
				"which reads as a position switch that stays closed while the target is flipped. The retained "
				"known-working script instead holds 53/54 closed from the hit until solenoid 22 fires and only "
				"pulses 55/56 once; the pinned corpus v1.03 script is the same lineage. The table plays, but the "
				"ROM may tolerate either pattern. Resolution path: the ROM's Switch Levels test (test 06) on a real "
				"machine with a target flipped shows which address stays closed, or a gameplay harness trace once "
				"the libpinmame System 11B boot stall is resolved, or static analysis of the L-4 game ROMs' switch "
				"handlers."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORPUS_SCRIPT_SOURCE],
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


def build(root: Path = ROOT) -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "Elvira and the Party Monsters",
			"manufacturer": "Bally",
			"year": 1989,
			"kind": "physical_pinball",
			"ipdb_id": 782,
			"opdb_id": "Grlxp-MVKBW",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["input_semantics", "output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "conflicted",
				"physical_wiring": "validated",
				"mechanisms": "candidate",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.system-11",
			"hardware_generation": "0x100",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(root),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Elvira device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	placement_count = 0
	observed: list[dict[str, Any]] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
			placement_count += len(spatial["placements"])
			if spatial["status"] == "observed":
				observed.append({"group": device["binding"]["group"], "address": address})
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	omitted_outputs: list[dict[str, Any]] = []
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
			if spatial["status"] == "observed":
				observed.append(binding)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "observed",
		"blockers": [
			"Lamps 11 and 20 (slingshot inserts) carry no spatial record: the manual's lamp matrix and its location "
			"drawing put them on opposite slingshots (conflict.slingshot-lamp-sides).",
			"Solenoid 11 (Playfield GI Relay) switches playfield general illumination, but the manual enumerates no "
			"GI bulb count or position; the retained table's 29-member GI collection is not adopted.",
			"Solenoid 16 (Boogie Monsters flashers) carries three observed placements against a printed two-bulb "
			"count, and solenoid 15 one placement against two printed playfield bulbs (conflict.flasher-bulb-quantities).",
			"Solenoid 29 (Moon / Wolfman) has one retained object for two printed playfield bulbs; its placement is observed.",
			"Flashers 13, 25, 27, 28, 29, 30, 31 and 32 also light Insert Board bulbs in the backbox (1 to 3 each, "
			"included in physical.quantity); only their playfield bulbs are placed.",
			"Switches 31, 52, 55 and 56 and solenoids 15, 16, 29 and 32 have observed rather than validated "
			"placements: the manual's drawings print no callout, end the leader visibly away from the retained "
			"object, or print more bulbs than the table models.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH:.0f}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT:.0f}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"table_sha256": TABLE_SHA256,
		},
		"placement_count": placement_count,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"observed_bindings": sorted(observed, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
		"not_applicable_outputs": {
			reason: sorted(bindings, key=lambda item: (item["group"], item["address"]))
			for reason, bindings in sorted(not_applicable_outputs.items())
		},
		"omitted_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())]
		),
		"excluded_object_classes": [
			"l11a/L11b/L11c and l20a/L20b/L20c: additional lights inside each slingshot driven with lamps 11 and 20",
			"l21a-l24a: lights beside the four left standups driven with lamps 21-24; the manual shows one insert per address",
			"l54a/l54b, l55a/l55b, l56a/l56b: co-located bumper-cap helpers of lamps 54-56",
			"fl17/fl18/fl25 flashers: glow effects driven with lamps 17, 18 and 25; the bulb-cover primitives L17/L18/L25 are placed, and fl17/fl18 each sit beside the other eye's cover",
			"f57-f59 (\"BackWall\") and l60-l64 (\"BackGlass\"): proxies for backboard and backglass lamps, recorded as not_applicable cabinet_or_service",
			"Coffin_1/Coffin_2 and Coffin_Elvira/Coffin_Drac: closed and open flip-up target visuals; the open visuals anchor the projections for 55 and 56",
			"Trigger2-Trigger5, Balldrop1/2 and the LeftDrop/RightDrop kickers: sound and ball-routing helpers with no Controller.Switch call",
			"GI collection (29 lights): playfield GI effect lights with no manual bulb inventory",
		],
		"unresolved": [conflict["id"] for conflict in definition["conflicts"]],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Elvira and the Party Monsters (Bally, 1989) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at "
		"`machines/partial/bally/elvira-and-the-party-monsters-1989.json`; see the promotion decision.",
		"",
		"The geometry source is the retained `Elvira and the Party Monsters (Bally 1989) nude.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`, an artwork variant of the 32assassin table. Its embedded script, SHA-256 "
		f"`{SCRIPT_SHA256}`, is the runtime binding authority. Playfield bounds are `{TABLE_BOUNDS}`; every "
		"coordinate is x/952 and y/1974 rounded to six places.",
		"",
		"## Evidence decisions",
		"",
		"- Positions come only from objects the retained script binds to an address. Each was compared with the "
		"manual's switch, lamp and solenoid location drawings (printed 2-37, 2-39, 2-15); where the drawing "
		"prints no callout or ends its leader visibly elsewhere, the placement is `observed`.",
		"- The manual owns physical construction and location; the known-working script owns runtime binding; "
		"pinned PinMAME owns the System 11B address space. The table's objects agree with the manual's drawings "
		"on every bumper, slingshot, lane, target, saucer and lock callout checked.",
		"- Trough, lock, slingshot, drop-bank, popper, eject and flip-up addresses without an object of their own "
		"are documented projections onto the object of their own mechanism.",
		"- Cabinet and backbox devices get controlled `not_applicable` records: the cabinet switches, the two "
		"flipper-button optos, the diagnostic inputs, the Country jumper, the knocker, the ELVIRA insert "
		"flashers, the insert GI relay, the A/C relay, the backboard Dead Head lamps 57-59, the backglass "
		"Barbeque lamps 60-64 and both displays.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Observed (not validated) bindings: {len(report['observed_bindings'])}",
		f"- Outputs with an intentionally omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += ["", "## Blockers", ""]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition and its printed wiring, and polarity "
		"is settled: `eatpmGameData` leaves `wpc.invSw` all zero, the drop-target optos reach the matrix through "
		"the C-12559 comparator board as ordinary closures, and the flipper-button optos carry button state. "
		"Promotion is refused because the slingshot lamps and the playfield GI have no placement, two flasher "
		"counts disagree inside the manual, and the flip-up switch roles are disputed. `coverage.missing` is "
		"`[\"input_semantics\", \"output_semantics\", \"mechanism_behavior\", \"spatial_placement\", "
		"\"unresolved_conflicts\"]`; the addresses the three conflicts name (switches 53-56, lamps 11 and 20, "
		"flashers 15 and 16) carry `conflicted` provenance.",
		"",
		"## Retained evidence",
		"",
		f"- Retained vpxtool extraction, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, manifest SHA-256 `{EXTRACTION_MANIFEST_SHA256}`.",
		"- Object-by-object geometry dump `external:pinmame-review-artifacts/elvira-and-the-party-monsters/vpx-geometry-raw.tsv`.",
		f"- Eleven transcribed manual excerpts with rendered crops under `{EXCERPT_DIR}/`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build(root)
	author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if author_ready.exists():
		raise RuntimeError(f"Refusing to overwrite an existing author-ready Elvira artifact: {author_ready}")
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
		raise RuntimeError("Elvira is recorded partial but an author-ready artifact exists")
	for path in (definition_path, seed_path):
		if not path.is_file():
			raise RuntimeError(f"Elvira artifact is missing: {path}")
	definition = build(root)
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Elvira definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Elvira seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Elvira spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Elvira spatial review drifted from its deterministic curator: {markdown_path}")
	print("Elvira definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed and the spatial audit")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Elvira extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Elvira retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
