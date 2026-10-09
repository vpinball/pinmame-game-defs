"""Curate the physical Williams Pin-Bot (1986) machine definition.

The builder is side-effect free and deterministic: every reviewed label, wiring detail and
normalized coordinate is a literal here, and the factory-drawing callout check is recomputed from
its committed seed, so regeneration reproduces the canonical definition, its pinned seed and the
spatial report byte for byte without reading the external evidence roots. ``--check`` refuses
drift, and ``--regenerate`` is the only path that writes them.

Pin-Bot is a System 11A machine (``GEN_S11X``) with an A/C select relay at solenoid 14:
``pbGameData`` sets ``sxx.muxSol = 14``, so pinned PinMAME publishes the eight switched "A" loads at
1-8 while the relay is released and their "C" partners at 25-32 while it is energized. Its
``sxx.ssSw`` map fires five of the six special solenoids directly from their own switch, and its
flippers are cabinet-wired with ``FLIP_SWNO(10,11)`` copying the cabinet buttons into the two lane
change switches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

import drawing_callouts
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_flipper_column import (
	VPM_CORE_SHA256,
	VPM_LIBRARY_SOURCE,
	VPM_LIBRARY_URI,
	VPM_S11_SHA256,
	flipper_column_inputs,
	flipper_column_relationships,
	vpm_staged_flipper_notes,
)


ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.pinbot.1986"
PARTIAL_PATH = ROOT / "machines/partial/williams/pinbot-1986.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/pinbot-1986.json"
STATUS = "partial"
DEFINITION_PATH = AUTHOR_READY_PATH if STATUS == "author_ready" else PARTIAL_PATH
STALE_DEFINITION_PATH = PARTIAL_PATH if STATUS == "author_ready" else AUTHOR_READY_PATH
SEED_PATH = ROOT / "tools/seeds/williams/pinbot-1986.json"
CALLOUT_SEED_PATH = ROOT / "tools/seeds/williams/pinbot-1986-callouts.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/pinbot-1986.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/pinbot-1986.md"
KNOWLEDGE_PATH = "knowledge/williams/pinbot-1986.md"
EXCERPT_DIRECTORY = ROOT / "evidence/excerpts" / MACHINE_ID
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/pinbot-l5-service-and-mechanisms.json"

PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.pinbot.1986"
IPDB_MANUAL_SOURCE = "manual.williams.pinbot.1986.ipdb"
ROM_SOURCE = "rom.pinbot.name-tables"
RUNTIME_SOURCE = "runtime.pinbot.l5-service-and-mechanisms"
VPX_TABLE_SOURCE = "vpx-table.pinbot-bord-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.pinbot-bord-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.pinbot-bord-1-1"
CORPUS_SCRIPT_SOURCE = "vpx-script.pinbot-2-1-1"
CALLOUT_SOURCE = "drawing-callouts.pinbot.2026-10-09"

# (left, right) in the driver's own FLIP_SWNO macro order.
FLIP_SWNO = (10, 11)

MANUAL_SHA256 = "b20e98516ec75d5af42f2dff5304221d7eaea0e6bc7734898c64d98305d22e53"
IPDB_MANUAL_SHA256 = "6654a2d03e35ea5d87aaa6928bedad7c9dfe00936201efd39eaf00bba88b0aaf"
TABLE_SHA256 = "5d0f4c4c0908065a7550864e290bff6ed0afcecf1bce5ba46553bb74903f9e56"
SCRIPT_SHA256 = "164eb3b24ae1be991ad2646d2b80292453712eb6f76658f06d9f936e35a23776"
CORPUS_SCRIPT_SHA256 = "9dfb664a26dc1f4d7163d8ada0ad2b50870dc3724513dc8c4746794e9661ce91"
CORPUS_REVISION = "15d112648a1b94b9f59eb8b3c335d57283653c50"
ROM_ARCHIVE_SHA256 = "f7b86e6688ef990f990d85564c3aaa264a14927d78402bab49880fafa74c5b6c"

EXTRACTION_RELATIVE_PATH = Path("williams/pinbot-1986/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/pinbot-1986/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 1840
# SHA-256 of the canonical manifest bytes, so a changed extraction with a refreshed manifest is refused.
EXTRACTION_MANIFEST_SHA256 = "870e4119cb59871d2df447995e5b357bcae17bdbc8b7b7d4a011b0a93300b926"

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0

DRIVER_IDS = ("pb_l5", "pb_l3", "pb_l2", "pb_l1", "pb_p4", "pb_l5h", "pb_j1", "pb_j2", "pb_j3", "pb_j5")
_SHARED = (
	"Shares pbGameData/init_pb with the parent through CORE_CLONEDEF (pinned src/wpc/s11games.c lines 274-275 and "
	"357-366), and so the same GEN_S11X generation, display layout, A/C select relay, special-solenoid switch map and "
	"flipper wiring, and it plays on the same sound ROMs."
)
DRIVER_COMPATIBILITY = {
	"pb_l5": (
		"identical",
		"Williams production L-5 game ROM, the pinned clone-tree parent and the driver the retained known-working table "
		"binds (cGameName = \"pb_l5\"). The runtime evidence was recorded on it.",
	),
	"pb_l3": (
		"identical",
		"Williams L-3 production game ROM (U27 L-3 paired with the U26 L-1). " + _SHARED + " Its U27 carries the same lamp, "
		"switch and coil name tables, entry for entry, as L-5.",
	),
	"pb_l2": (
		"identical",
		"Williams L-2 production game ROM (U27 L-2 paired with the U26 L-1). " + _SHARED + " Its U27 carries the same lamp, "
		"switch and coil name tables, entry for entry, as L-5.",
	),
	"pb_l1": (
		"identical",
		"Williams L-1, the earliest dumped production game ROM. " + _SHARED + " Its U27 carries the same lamp, switch and "
		"coil name tables, entry for entry, as L-5.",
	),
	"pb_p4": (
		"identical",
		"Williams P-4 prototype game ROM (U27 P-4 paired with the U26 L-1). " + _SHARED + " Its U27 names every lamp, switch "
		"and coil exactly as L-5 does, so it addresses no device the production machine lacks.",
	),
	"pb_l5h": (
		"identical",
		"2012 community modification of the L-5 game ROMs by Francis (free play and a Solar Value change). " + _SHARED +
		" It changes rules and pricing only; its U27 name tables match L-5 entry for entry.",
	),
	"pb_j1": (
		"identical",
		"2020 PEMBOT community game ROM by A.M. Thurnherr for the Pin-Bot hardware. " + _SHARED + " Its archive is not in "
		"the local ROM corpus, so its name tables were not read; nothing in the pinned source gives it hardware of its own.",
	),
	"pb_j2": (
		"identical",
		"2023 PEMBOT community game ROM by idealjoker (\"Minor bug fixes and improvements\" per the pinned source). " + _SHARED +
		" Its archive is not in the local ROM corpus, so its name tables were not read.",
	),
	"pb_j3": (
		"identical",
		"2023 PEMBOT community game ROM by idealjoker (\"Knocker did not fire on match awards\" per the pinned source). " +
		_SHARED + " Its archive is not in the local ROM corpus, so its name tables were not read.",
	),
	"pb_j5": (
		"identical",
		"2026 PEMBOT community game ROM by idealjoker (outhole-handler and Sun Special fixes per the pinned source). " +
		_SHARED + " Its U27 holds the same lamp, switch and coil name tables as L-5, entry for entry, at offsets 0x2b lower.",
	),
}

# --- Switch matrix (public address = (column-1)*8+row; System 11 sequential column-major).
# Labels of record follow the Switch-Matrix Table (printed page 29) with detail from the Switches
# parts list (printed page 52); the ROM's own switch-table text is kept per address.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "Ball Roll Tilt", 3: "Credit Button", 4: "Right Coin Chute", 5: "Center Coin Chute",
	6: "Left Coin Chute", 7: "Slam Tilt", 8: "High Score Reset",
	9: "Playfield Tilt", 10: "Left Lane Change", 11: "Right Lane Change", 12: "Left Outlane", 13: "Left Return Lane",
	14: "Right Return Lane", 15: "Right Outlane", 16: "Outhole",
	17: "Ball Trough #1 (Lower Right)", 18: "Ball Trough #2 (Center)", 19: "Advance Planet", 20: "Shooter Lane",
	22: "Vortex 20K", 23: "Vortex 100K", 24: "Vortex 5K (Exit)",
	25: "Left Eye Eject", 26: "Right Eye Eject",
	28: "Visor Target 1 (Left, Yellow)", 29: "Visor Target 2 (Blue)", 30: "Visor Target 3 (Center, Amber)",
	31: "Visor Target 4 (Green)", 32: "Visor Target 5 (Right, Red)",
	33: "Right 5-Bank Target 1 (Top)", 34: "Right 5-Bank Target 2", 35: "Right 5-Bank Target 3 (Center)",
	36: "Right 5-Bank Target 4", 37: "Right 5-Bank Target 5 (Bottom)", 38: "Single Eject", 39: "Exit Ramp",
	40: "Enter Ramp", 44: "Ramp Down", 45: "Score Energy", 46: "Visor Closed", 47: "Visor Open",
	48: "Left Jet Bumper", 49: "Left Drop Target (Upper)", 50: "Left Drop Target (Mid)", 51: "Left Drop Target (Lower)",
	52: "Top Jet Bumper", 53: "Bottom Jet Bumper", 54: "Left Sling", 55: "Right Sling",
	56: "10 Point (Left Rubber)", 59: "10 Point (Right Rubber)", 60: "10 Point (Upper Left Rubber)",
}
UNUSED_SWITCHES = frozenset({21, 27, 41, 42, 43, 57, 58, 61, 62, 63, 64})
# Switch-Matrix Table wording where the label of record adds detail.
MATRIX_WORDING = {
	17: "Ball Trough #1 (Lower Right)", 18: "Ball Trough #2 (Center)", 20: "Shooter Lane", 24: "Vortex 5K (Exit)",
	25: "Left Eject", 26: "Right Eject", 28: "Visor Target 1 (Left)", 29: "Visor Target 2", 30: "Visor Target 3 (Center)",
	31: "Visor Target 4", 32: "Visor Target 5 (Right)", 33: "Right 5-Bank (Top)", 34: "Right 5-Bank",
	35: "Right 5-Bank (Center)", 36: "Right 5-Bank", 37: "Right 5-Bank (Bottom)", 39: "Exit Ramp", 40: "Enter Ramp",
	56: "10 Point", 59: "10 Point", 60: "10 Point", 8: "High-Score Reset",
}
# Switches parts list (printed page 52) wording, kept where it differs from the matrix.
PARTS_LIST_WORDING = {
	17: "Ball Trough #1 (lwr right)", 18: "Ball Trough #2", 20: "Ball Shooter Lane", 25: "Left Eye Eject",
	26: "Right Eye Eject", 28: "Visor Target 1 (left, yellow)", 29: "Visor Target 2 (blue)",
	30: "Visor Target 3 (amber)", 31: "Visor Target 4 (green)", 32: "Visor Target 5 (right, red)",
	33: "Visor Target top,yellow)", 34: "Right 5-bank (top, yellow)", 35: "Right 5-bank (blue)",
	36: "Right 5-bank (amber)", 37: "Right 5-bank (red)", 39: "Ramp Exit", 40: "Ramp Entrance",
	45: "Score Energy (yellow)", 54: "Left Kicker (scoring)**", 55: "Right Kicker (scoring)**", 56: "10 Point",
	59: "10 Point", 60: "10 Point",
}
ROM_SWITCH_NAMES = {
	1: "PLUMB TILT", 2: "BALL TILT", 3: "CREDIT BUTTON", 4: "RIGHT COIN SW.", 5: "CENTER COIN SW.", 6: "LEFT COIN SW.",
	7: "SLAM TILT", 8: "HISCORE RESET", 9: "PLAYFLD TILT", 10: "L. LANE CHANGE", 11: "R. LANE CHANGE",
	12: "LEFT OUTLANE", 13: "LEFT RETURN", 14: "RIGHT RETURN", 15: "RIGHT OUTLANE", 16: "OUTHOLE", 17: "TROUGH 1 SW",
	18: "TROUGH 2 SW", 19: "ADVANCE PLANET", 20: "SHOOTER SWITCH", 21: "21 NOT USED", 22: "VORTEX 20K",
	23: "VORTEX 100K", 24: "VORTEX EXIT", 25: "LEFT EJECT", 26: "RIGHT EJECT", 27: "27 NOT USED", 28: "VISOR LEFT",
	29: "VISOR LEFT 2", 30: "VISOR CENTER", 31: "VISOR RIGHT 2", 32: "VISOR RIGHT", 33: "R. 5BANK 1  TOP",
	34: "R. 5BANK 2", 35: "R. 5BANK 3  MID", 36: "R. 5BANK 4", 37: "R. 5BANK 5  BOT", 38: "SINGLE EJECT",
	39: "EXIT RAMP", 40: "ENTER RAMP", 41: "41 NOT USED", 42: "42 NOT USED", 43: "43 NOT USED", 44: "RAMP DOWN",
	45: "SCORE ENERGY", 46: "VISOR CLOSED", 47: "VISOR OPEN", 48: "LEFT JET", 49: "LEFT D.T. TOP",
	50: "LEFT D.T. MIDDLE", 51: "LEFT D.T. BOTTOM", 52: "TOP JET", 53: "BOTTOM JET", 54: "LEFT SLING",
	55: "RIGHT SLING", 56: "10 PT SWITCH", 57: "57 NOT USED", 58: "58 NOT USED", 59: "10 PT SWITCH",
	60: "10 PT SWITCH", 61: "61 NOT USED", 62: "62 NOT USED", 63: "63 NOT USED", 64: "64 NOT USED",
}
SWITCH_PARTS = {
	1: "A-8476", 2: "B-6572", 3: "SW-1A-126", 4: "904845", 5: "904845", 6: "904845", 7: "904704", 8: "5641-09369-00",
	9: "SW-1A-117", 10: "SW-1A-150-1", 11: "SW-1A-150", 12: "SW-1A-124", 13: "SW-1A-124", 14: "SW-1A-124",
	15: "SW-1A-124", 16: "17-1067", 17: "5647-09957-00", 18: "5647-09633-00", 19: "A-11055", 20: "SW-1A-138",
	22: "SW-1A-118", 23: "SW-1A-118", 24: "SW-1A-124", 25: "17-1012", 26: "17-1012", 28: "SW-1A-161",
	29: "SW-1A-163-1", 30: "SW-1A-163-4", 31: "SW-1A-163-2", 32: "SW-1A-163-3", 34: "A-11317-3",
	35: "A-11317-3", 36: "A-11317-3", 37: "A-11317-3", 38: "17-1012", 39: "SW-1A-164", 40: "SW-1A-164",
	44: "5647-12001-00", 45: "A-11054", 46: "5647-10529-00", 47: "5647-10529-00", 48: "A-7459-7", 49: "17-1042",
	50: "17-1042", 51: "17-1042", 52: "A-7459-7", 53: "A-7459-7", 54: "SW-1A-122", 55: "SW-1A-122", 56: "SW-1A-120",
	59: "SW-1A-120", 60: "SW-1A-120",
}
# Construction is asserted only where a part number or an assembly page identifies it.
SWITCH_TYPES = {
	1: "tilt", 2: "tilt", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button", 9: "tilt",
	10: "leaf", 11: "leaf", 12: "leaf", 13: "leaf", 14: "leaf", 15: "leaf", 17: "microswitch", 18: "microswitch",
	19: "leaf", 20: "leaf", 22: "leaf", 23: "leaf", 24: "leaf", 28: "leaf", 29: "leaf", 30: "leaf", 31: "leaf",
	32: "leaf", 33: "leaf", 34: "leaf", 35: "leaf", 36: "leaf", 37: "leaf", 39: "leaf", 40: "leaf",
	44: "microswitch", 45: "leaf", 46: "microswitch", 47: "microswitch", 48: "leaf", 52: "leaf", 53: "leaf",
	54: "leaf", 55: "leaf", 56: "leaf", 59: "leaf", 60: "leaf",
}
UNTYPED_SWITCHES = (16, 25, 26, 38, 49, 50, 51)
UNTYPED_NOTE = (
	" The Switches parts list prints only a 17-series part number for this position and the manual never states "
	"its construction, so no switch_type is asserted. It is not an opto: no row of that list carries an opto part, "
	"neither copy of the Switch-Matrix Table shades a cell or prints an opto legend, and the ROM reads it active at "
	"public 1 like every other matrix switch."
)
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
	-5: ("CPU Diagnostic (SW2)", "service.cpu-diag"), -4: ("Sound Diagnostic (SW1)", "service.sound-diag"),
}
CABINET_SWITCH_ROLES = {
	1: "cabinet.tilt", 2: "cabinet.tilt", 3: "cabinet.start", 4: "cabinet.coin", 5: "cabinet.coin", 6: "cabinet.coin",
	7: "cabinet.slam-tilt", 8: "cabinet.service", 9: "cabinet.tilt",
}
# sxx.ssSw for pbGameData = {53,0,48,54,55,52} (pinned src/wpc/s11games.c lines 274-275). The VBLANK loop
# at src/wpc/s11.c lines 191-200 drives CORE_FIRSTSSSOL+ii from core_getSw(ssSw[ii]) for ii = 0..5.
SPECIAL_SOLENOID_SWITCH = {17: 53, 18: 0, 19: 48, 20: 54, 21: 55, 22: 52}

# --- Switch placements: normalized table-object centres (x/952, y/1974), object named per address.
SWITCH_OBJECTS = {
	12: ("Trigger sw12", (0.063226, 0.710471)), 13: ("Trigger sw13", (0.133122, 0.711459)),
	14: ("Trigger sw14", (0.77689, 0.710754)), 15: ("Trigger sw15", (0.847616, 0.710942)),
	19: ("HitTarget sw19", (0.860723, 0.544918)), 20: ("Trigger sw20", (0.934679, 0.874496)),
	22: ("Trigger sw22", (0.768949, 0.104766)), 23: ("Trigger sw23", (0.764782, 0.144973)),
	24: ("Trigger sw24", (0.752719, 0.194965)), 25: ("Kicker sw25", (0.354364, 0.08926)),
	26: ("Kicker sw26", (0.552448, 0.089794)),
	28: ("HitTarget sw28", (0.333914, 0.205682)), 29: ("HitTarget sw29", (0.396109, 0.205421)),
	30: ("HitTarget sw30", (0.455267, 0.205721)), 31: ("HitTarget sw31", (0.516361, 0.205721)),
	32: ("HitTarget sw32", (0.577245, 0.205666)),
	33: ("HitTarget sw33", (0.604038, 0.309709)), 34: ("HitTarget sw34", (0.617686, 0.337283)),
	35: ("HitTarget sw35", (0.630597, 0.363433)), 36: ("HitTarget sw36", (0.643138, 0.390474)),
	37: ("HitTarget sw37", (0.656049, 0.41698)), 38: ("Kicker sw38", (0.132672, 0.049946)),
	39: ("Trigger sw39", (0.943377, 0.128377)), 40: ("Trigger sw40", (0.196475, 0.08104)),
	45: ("HitTarget sw45", (0.131013, 0.129856)),
	48: ("Bumper sw48_bumper2", (0.708361, 0.335162)), 49: ("HitTarget sw49", (0.113898, 0.424672)),
	50: ("HitTarget sw50", (0.107013, 0.4532)), 51: ("HitTarget sw51", (0.100765, 0.48141)),
	52: ("Bumper sw52_bumper1", (0.838217, 0.255778)), 53: ("Bumper sw53_bumper3", (0.837834, 0.415864)),
	54: ("Wall LeftSlingShot (drag-point mean)", (0.232276, 0.706052)),
	55: ("Wall RightSlingShot (drag-point mean)", (0.680511, 0.703157)),
	56: ("Primitive WallLaa (baked mesh bounding-box centre)", (0.096301, 0.55211)),
	59: ("Primitive Wallrb (baked mesh bounding-box centre)", (0.800939, 0.509362)),
	60: ("Primitive WallLcc (baked mesh bounding-box centre)", (0.217171, 0.275641)),
}
DRAIN = (0.527346, 0.950467)
BALL_RELEASE = (0.867647, 0.85309)
LEFT_FLIPPER = (0.288368, 0.829647)
RIGHT_FLIPPER = (0.619273, 0.829647)
VISOR = (0.455649, 0.066475)
RAMP_LEVER = (0.19503, 0.317427)
# Documented projections: a sensor with no table object of its own, placed on its own mechanism's object.
SWITCH_PROJECTIONS = {
	10: (LEFT_FLIPPER, (
		"Projected onto the left flipper's own assembly (Flipper LeftFlipper, object centre). The Lane Change switch is "
		"item 2b (SW-1A-150) of the C-9954 Flipper Base/Lane Change Assembly below the playfield, and the switch drawing "
		"(printed page 52) ends leader 10 on a dashed switch outline beside the left flipper's pivot. The retained script "
		"never drives this address; core_updateSw copies public 84 into it."
	)),
	11: (RIGHT_FLIPPER, "Projected onto the right flipper's own assembly (Flipper RightFlipper, object centre); see switch 10."),
	16: (DRAIN, (
		"Projected onto the table's drain kicker (Kicker Drain, object centre), where its cvpmBallStack receives a "
		"drained ball (bsTrough.InitSw 16,17,18). The switch drawing ends leader 16 at the lower-left end of the "
		"outhole tube, 0.04 normalized from that kicker."
	)),
	17: (BALL_RELEASE, (
		"Projected onto the table's ball-release kicker (Kicker BallRelease, object centre): the retained script models the "
		"two-ball trough as one cvpmBallStack (bsTrough.InitSw 16,17,18 with bsTrough.InitKick BallRelease) and has no "
		"object per trough position. The switch drawing ends leader 17 at the shooter end of the trough tube."
	)),
	18: (BALL_RELEASE, (
		"Projected onto the table's ball-release kicker (Kicker BallRelease); see switch 17. The switch drawing ends "
		"leader 18 further down the same trough tube, where the second ball waits behind the first."
	)),
	44: (RAMP_LEVER, (
		"Projected onto the table's ramp-lift lever (Primitive lramplever_prim, object position), the ramp lifting "
		"mechanism's own moving part. The Ramp Down switch is the B-11304 Ramp Lifting Mechanism's microswitch "
		"(5647-12001-00, item 14) below the playfield; the retained script writes this address from its RampTimer when "
		"the ramp reaches its lowered position and has no switch object. The switch drawing's leader 44 runs to the "
		"lifting mechanism beside the ramp lever, about 0.02 normalized from this point."
	)),
	46: (VISOR, (
		"Projected onto the visor (Primitive visorflat_prim, object position): Visor Closed is one of the two "
		"5647-10529-00 limit switches on the visor motor's cam (Visor Motor Assembly B-11169, item 7) below the "
		"playfield, and the retained script models it as position 0 of its cvpmMech visor (mVisor.AddSw 46,0,0). The "
		"switch drawing draws only a dashed leader line towards the visor box for 46 and 47."
	)),
	47: (VISOR, (
		"Projected onto the visor (Primitive visorflat_prim, object position), the other cam limit switch; the retained "
		"script places it at the end of the visor's travel (mVisor.AddSw 47,58,58). See switch 46."
	)),
}
SWITCH_OBJECT_NOTES = {
	24: (
		"The switch drawing's leader 24 continues in a straight line under the drawn guide arm to the rollover slot at "
		"the Vortex exit, which is where this trigger sits."
	),
	28: "The table also carries combo HitTargets between neighbouring visor targets that pulse two switches at once; they are table helpers, not separate sensors.",
	40: (
		"The retained trigger sits at the top of the ramp's curve, while the switch drawing ends leader 40 on the dashed "
		"rollover outline further down the same curve."
	),
	49: "The table also carries two combo walls between the drop targets that report two targets at once; they are table helpers, not separate sensors.",
	60: (
		"The retained script pulses this address from two rubber primitives (WallLcc_Hit and WallLccc_Hit). The manual "
		"lists one switch at this address and the switch drawing draws one callout, which lands on WallLcc, so WallLcc "
		"supplies the placement and WallLccc is a table embellishment."
	),
}

# --- Solenoid table (printed page 27) and Solenoids/Flashers list (printed page 50).
# Switched A/C pairs: (A-side public, C-side public, printed pair, CPU connection, power connection, driver).
AC_PAIRS = {
	1: (1, 25, "1P11-1", "8P3-1 (to B1 on Diode Sw. Bd.)", "Q33", "Gry-Brn"),
	2: (2, 26, "1P11-3", "8P3-2 (to B2 on Diode Sw. Bd.)", "Q25", "Gry-Red"),
	3: (3, 27, "1P11-4", "8P3-3 (to B3 on Diode Sw. Bd.)", "Q32", "Gry-Orn"),
	4: (4, 28, "1P11-5", "8P3-4 (to B4 on Diode Sw. Bd.)", "Q24", "Gry-Yel"),
	5: (5, 29, "1P11-6", "8P3-5 (to B5 on Diode Sw. Bd.)", "Q31", "Gry-Grn"),
	6: (6, 30, "1P11-7", "8P3-6 (to B6 on Diode Sw. Bd.)", "Q23", "Gry-Blu"),
	7: (7, 31, "1P11-8", "8P3-7 (to B7 on Diode Sw. Bd.)", "Q30", "Gry-Vio"),
	8: (8, 32, "1P11-9", "8P3-8 (to B8 on Diode Sw. Bd.)", "Q22", "Gry-Blk"),
}
SOLENOID_LABELS = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Single Eject Hole", 4: "3-Bank Drop Target Reset",
	5: "Ramp Raise", 6: "Ramp Lower", 7: "Left Eye Eject Hole", 8: "Right Eye Eject Hole",
	9: "Robot Face Flashers (Insert Board)", 10: "Right Visor G.I.", 11: "Insert Board G.I. Relay",
	12: "Playfield G.I. Relay", 13: "Visor Motor Relay", 14: "Solenoid Select (A/C) Relay",
	15: "Top Backbox Flashers #3", 16: "Top Backbox Flashers #4 (Center)", 17: "Lower Jet Bumper", 18: "Left Visor G.I.",
	19: "Left Jet Bumper", 20: "Left Kicker", 21: "Right Kicker", 22: "Upper Jet Bumper",
	25: "Knocker", 26: "Upper Playfield and Top Backbox Flashers #2", 27: "Left Insert Board Flasher",
	28: "Right Insert Board Flasher", 29: "Lower Playfield and Top Backbox Flashers #1", 30: "Energy Flashers",
	31: "Left Playfield Flashers", 32: "Sun Flasher",
}
SOLENOID_MANUAL_NUMBER = {address: f"{address:02d}A" for address in range(1, 9)}
SOLENOID_MANUAL_NUMBER.update({address: f"{address - 24:02d}C" for address in range(25, 33)})
SOLENOID_MANUAL_NUMBER.update({address: f"{address:02d}" for address in range(9, 23)})
SOLENOID_TABLE_WORDING = {
	1: "Outhole", 2: "Ball Trough Feeder", 3: "Single Eject Hole", 4: "Drop Target (3-Bank)", 5: "Ramp Raise",
	6: "Ramp Lower (Outer)", 7: "Left Eject Hole (Visor)", 8: "Right Eject Hole (Visor)", 9: "Robot Face - Insert Bd.",
	10: "Right Visor - Gen. Illumin.", 11: "General Illumin. - Insert Bd.", 12: "General Illumin. - Playfield",
	13: "Visor Motor", 14: "Solenoid Select Relay", 15: "\"Top\" Flashers (3)", 16: "\"Top\" Flashers (4, center)",
	17: "Lower Jet Bumper", 18: "Left Visor Gen. Illumin.", 19: "Left Jet Bumper", 20: "Left Kicker",
	21: "Right Kicker", 22: "Upper Jet Bumper", 25: "Knocker", 26: "Upper P'fld & \"Top\" Flashers (2)",
	27: "Left Insert Bd. Flasher", 28: "Right Insert Bd. Flasher", 29: "Lower P'fld & \"Top\" Flashers (1)",
	30: "Energy Flashers", 31: "Left Playfield Flasher", 32: "Sun Flasher",
}
LIST_WORDING = {
	1: "Outhole Kicker", 2: "Ball Shooter Lane Feeder", 3: "Single Eject Hole", 4: "Drop Target (3-bank)",
	5: "Ramp Raise", 6: "Ramp Down", 7: "Left Eye Eject Hole (visor)", 8: "Right Eye Eject Hole (visor)",
	9: "Robot Face - Insert Board", 10: "Right Visor - Gen. Illumin.", 11: "Gen. Illumin. Relay - Insert Bd.",
	12: "Gen. Illumin. Relay - Playfield", 13: "Visor Motor Relay", 14: "Solenoid Select Relay",
	15: "\"Top\" Backbox Flashers (#3)", 16: "\"Top\" Backbox Flashers (#4, center)", 17: "Lower Jet Bumper",
	18: "Left Visor - Gen. Illumin.", 19: "Left Jet Bumper", 20: "Left Kicker", 21: "Right Kicker",
	22: "Upper Jet Bumper", 25: "Knocker", 26: "Upper P'fld & \"Top\" B. Box (#2)", 27: "Insert Board - Left",
	28: "Insert Board - Right", 29: "Lower P'fld & \"Top\" B. Box (#1, outer)", 30: "Energy Flashers",
	31: "Left Playfield Flasher", 32: "Sun Flashers",
}
ROM_COIL_NAMES = {
	1: "OUTHOLE", 25: "KNOCKER", 2: "BALL RELEASE", 26: "UP.  F.L. TOP F.L.2", 3: "SINGLE EJECT",
	27: "BACKGLS. L. FLASH", 4: "DROP TARGET", 28: "BACKGLS. R. FLASH", 5: "RAISE RAMP", 29: "LOW. F.L. TOP F.L.1",
	6: "LOWER RAMP", 30: "ENERGY FLASH L.", 7: "LEFT EJECT", 31: "LEFT FLASH L.", 8: "RIGHT EJECT",
	32: "SUN FLASH L.", 9: "BACKGLS. FACE", 10: "R. VISOR G.I.", 11: "BACKGLS G.I.", 12: "PLAYFLD G.I.",
	13: "VISOR MOTOR", 14: "A-C SELECT", 15: "TOP F.L.3", 16: "TOP F.L.4 CENTER", 17: "BOTTOM JET",
	18: "L. VISOR G.I.", 19: "LEFT JET", 20: "LEFT KICKER", 21: "RIGHT KICKER", 22: "TOP JET",
}
COIL_TEST_ORDER = (1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
SOLENOID_WIRE = {
	1: "Vio-Brn", 25: "Blk-Brn", 2: "Vio-Red", 26: "Blk-Red", 3: "Vio-Orn", 27: "Blk-Orn", 4: "Vio-Yel", 28: "Blk-Yel",
	5: "Vio-Grn", 29: "Blk-Grn", 6: "Vio-Blu", 30: "Blk-Blu", 7: "Vio-Vio", 31: "Blk-Vio", 8: "Vio-Gry", 32: "Blk-Gry",
	9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel", 13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio",
	16: "Brn-Gry", 17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
}
CONTROLLED = {
	9: ("1P12-1", "8P3-9", "Q17"), 10: ("1P12-2", "8P3-10", "Q9"), 11: ("1P12-4", "8P3-12", "Q16"),
	12: ("1P12-5", "3P7-1", "Q8"), 13: ("1P12-6", "8P3-13", "Q15"), 14: ("1P12-7", "8P3-14", "Q7"),
	15: ("1P12-8", "8P3-15", "Q14"), 16: ("1P12-9", "8P3-16", "Q6"),
	17: ("1P19-7", "8P3-17", "Q75"), 18: ("1P19-4", "8P3-18", "Q71"), 19: ("1P19-3", "8P3-19", "Q73"),
	20: ("1P19-6", "8P3-20", "Q69"), 21: ("1P19-8", "8P3-21", "Q77"), 22: ("1P19-9", "8P3-22", "Q79"),
}
SOLENOID_PART = {
	1: "AE-23-800-01", 25: "AE-23-800-02", 2: "AE-23-800-03", 26: "#89 flashlamps", 3: "AE-23-800-03",
	27: "#89 flashlamps", 4: "AE-23-800-04", 28: "#89 flashlamps", 5: "AE-24-900-02", 29: "#89 flashlamps",
	6: "SM-26-600-DC", 30: "#89 flashlamps", 7: "AE-23-800-03", 31: "#89 flashlamps", 8: "AE-23-800-03",
	32: "#89 flashlamps", 9: "#1251 flashlamps", 10: "#1251 flashlamps", 11: "5580-09555-01", 12: "5580-09555-01",
	13: "5580-09555-01", 14: "5580-09555-01", 15: "#89 flashlamps", 16: "#89 flashlamps", 17: "AE-23-800-03",
	18: "#1251 flashlamps", 19: "AE-23-800-03", 20: "AE-23-800-03", 21: "AE-23-800-03", 22: "AE-23-800-03",
}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "coil", 5: "coil", 6: "coil", 7: "coil", 8: "coil", 9: "flasher", 10: "gi",
	11: "gi", 12: "gi", 13: "relay", 14: "relay", 15: "flasher", 16: "flasher", 17: "coil", 18: "gi", 19: "coil",
	20: "coil", 21: "coil", 22: "coil", 25: "coil", 26: "flasher", 27: "flasher", 28: "flasher", 29: "flasher",
	30: "flasher", 31: "flasher", 32: "flasher",
}
# What the retained known-working script does with each address (geometry review, script.vbs).
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn (script line 173)", 2: "bsTrough.SolOut, kicking from Kicker BallRelease (line 174)",
	3: "bsSaucer.SolOut on Kicker sw38 (line 175)", 4: "dtDTBank.SolDropUp, raising drop targets 49-51 (line 176)",
	5: "solRampUp, which raises the table's lift ramp (line 177)",
	6: "solRampDwn, which lowers it and, through RampTimer, closes switch 44 at the bottom (line 178)",
	7: "bsLEye.SolOut on Kicker sw25 (line 179)", 8: "bsREye.SolOut on Kicker sw26 (line 180)",
	9: "Sol9, which shows the backglass robot-face flasher sprites (line 2666)",
	10: "SetLamp 101 (commented \"RightEye Flash\"), one Flasher sprite between the eyes (line 182)",
	11: "Sol11, which shows or hides the backglass G.I. sprites; on means G.I. off (line 2667)",
	12: "PFGI, which turns every Light of its 54-member GI collection off while the solenoid is on (line 184)",
	13: "the cvpmMech visor (mVisor.Sol1 = 13); SolCallback(13) itself is commented out (lines 97-107 and 186)",
	18: "SetLamp 104 (commented \"LeftEye Flash\"), the same Flasher sprite position as solenoid 10 (line 190)",
	25: "vpmSolSound Knocker (line 196)", 26: "SetLamp 105 (commented \"Flashers Top\"), the two upper flasher domes (line 197)",
	27: "Sol27, a backglass flasher sprite (line 2668)", 28: "Sol28, a backglass flasher sprite (line 2669)",
	29: "SetLamp 106 (commented \"Flashers Lower\"), the two lower side flasher domes (line 200)",
	30: "SetLamp 107 (commented \"Bumper Flasher\"), light l107 beside the jet bumpers (line 201)",
	31: "SetLamp 108 (commented \"Flashers Left\"), the two left-side flasher domes (line 202)",
	32: "SetLamp 109 (commented \"sun flasher\"), light l109 in the sun (line 203)",
}
# Placements: (object, coordinate) per bulb or effect location.
SOLENOID_OBJECTS = {
	1: [("Kicker Drain", DRAIN)], 2: [("Kicker BallRelease", BALL_RELEASE)], 3: [("Kicker sw38", (0.132672, 0.049946))],
	4: [("HitTarget sw50, the bank's middle target", (0.107013, 0.4532))],
	5: [("Primitive lramplever_prim", RAMP_LEVER)], 6: [("Primitive lramplever_prim", RAMP_LEVER)],
	7: [("Kicker sw25", (0.354364, 0.08926))], 8: [("Kicker sw26", (0.552448, 0.089794))],
	13: [("Primitive visorflat_prim", VISOR)],
	17: [("Bumper sw53_bumper3", (0.837834, 0.415864))], 19: [("Bumper sw48_bumper2", (0.708361, 0.335162))],
	20: [("Wall LeftSlingShot (drag-point mean)", (0.232276, 0.706052))],
	21: [("Wall RightSlingShot (drag-point mean)", (0.680511, 0.703157))],
	22: [("Bumper sw52_bumper1", (0.838217, 0.255778))],
	26: [("Primitive flash3_l_prim (dome mesh centre)", (0.175908, 0.039784)), ("Primitive flash3_r_prim (dome mesh centre)", (0.945512, 0.033964))],
	29: [("Primitive flash1l_prim (dome mesh centre)", (0.06581, 0.578971)), ("Primitive flash1r_prim (dome mesh centre)", (0.849591, 0.592918))],
	30: [("Light l107", (0.882583, 0.318104))],
	31: [("Primitive flash2_b_prim (dome mesh centre)", (0.066374, 0.371859)), ("Primitive flash2_t_prim (dome mesh centre)", (0.061269, 0.064612))],
	32: [("Light l109", (0.460727, 0.59438))],
}
# Placements that are documented projections rather than the device's own table object.
SOLENOID_PROJECTED = {
	1: "the drain kicker the trough's cvpmBallStack receives balls on; the outhole kicker coil has no object of its own",
	2: "the ball-release kicker the script kicks from; the trough feeder coil has no object of its own",
	4: "the bank's middle drop target; the reset coil sits below the bank and has no object of its own",
	5: "the ramp-lift lever, the moving part the B-11304 mechanism's raise coil drives",
	6: "the ramp-lift lever; the lowering coil (SM-26-600-DC, item 22) acts on the same mechanism",
	13: "the visor the motor moves; the relay and motor sit below the playfield and have no object of their own",
}
FLASHER_NOTES = {
	26: (
		"The printed function covers playfield bulbs and the backbox's \"Top\" flasher #2. The playfield bulbs are the two "
		"upper flasher domes the retained script lights for this address (its Flasher2TL/Flasher2TR glow sprites sit on "
		"the modelled domes flash3_l_prim and flash3_r_prim), and the placements are those domes; the backbox flasher is "
		"part of the D-11380 Top Backbox Flasher assembly and has no playfield position. The manual prints no bulb count."
	),
	29: (
		"The printed function covers playfield bulbs and the backbox's \"Top\" flasher #1 (outer). The playfield bulbs are "
		"the two lower side flasher domes the retained script lights for this address (flash1l_prim and flash1r_prim), "
		"which are the placements; the backbox flasher has no playfield position. The manual prints no bulb count."
	),
	30: (
		"The retained script lights light l107 beside the jet bumpers for this address and also paints a glow sprite on "
		"the bumper nest; the placement is l107. In the gameplay runs the ROM flashes this output with each jet-bumper "
		"hit, which matches the Energy Value feature the jets build. The manual prints the plural \"flashlamps\" but no "
		"count, and the table models one bulb."
	),
	31: (
		"The retained script lights the two left-side flasher domes for this address (flash2_b_prim at the drop-target "
		"side and flash2_t_prim in the upper-left corner), which are the placements. The manual prints the singular "
		"\"Left Playfield Flasher\" with plural \"flashlamps\" and no count."
	),
	32: "The retained script lights light l109 in the centre of the sun insert for this address; the placement is l109.",
}

VIRTUAL_SOLENOIDS = {
	23: ("PinMAME Flipper/Special-Solenoid Enable State", "used", "internal.game-on-enable", (
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (pinned src/wpc/s11.h S11_GAMEONSOL 23), set from PIA0 CB2 in "
		"pia0cb2_w and used to gate the six special solenoids and the synthetic flipper outputs 45-48. It has no driver "
		"transistor and no Sol. No. of its own. In the retained runs it rises when a game starts and stays on (runs "
		"gameplay and gameplay-reactive), and the retained script binds it to vpmNudge.SolGameOn."
	)),
	24: ("Unassigned Solenoid Slot 24", "unused", "internal.unused-platform-slot", (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay C-side bank (25-32); no "
		"System 11 driver populates it and no Pin-Bot run published it."
	)),
	45: ("Synthetic Lower Right Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-right flipper power output (CORE_FIRSTLFLIPSOL = 45). pbGameData declares "
		"FLIP_SWNO(10,11) with no FLIP_SOL, so core_updateSw fabricates 45/46 from the right button bit at public 82 and "
		"47/48 from the left bit at public 84 while the enable (23) is on. The manual confirms there is no driver behind "
		"them: the two flipper rows of the Solenoid Table carry no Sol. No. and no transistor, and note 1 says the "
		"CPU-board wire runs to the flipper switch. The retained script binds SolCallback(sLRFlipper) = SolRFlipper."
	)),
	46: ("Synthetic Lower Right Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-right flipper hold output; see address 45."),
	47: ("Synthetic Lower Left Flipper Power", "used", "internal.synthetic-flipper", (
		"PinMAME's synthetic lower-left flipper power output; see address 45. The retained script binds "
		"SolCallback(sLLFlipper) = SolLFlipper."
	)),
	48: ("Synthetic Lower Left Flipper Hold", "used", "internal.synthetic-flipper", "PinMAME's synthetic lower-left flipper hold output; see address 47."),
	49: ("PinMAME Simulator Ball-Shooter Channel", "unused", "internal.unused-platform-slot", (
		"Platform-wide simulator-only output (CORE_FIRSTSIMSOL = 49); pbGameData declares no simulator."
	)),
	50: ("Unassigned Solenoid Slot 50", "unused", "internal.unused-platform-slot", (
		"Unassigned gap below the custom-solenoid base (51). pbGameData declares no custSol, so MACHINE_INIT(s11) sizes "
		"coreGlobals.nSolenoids as CORE_FIRSTCUSTSOL-1+0 = 50 and nothing above 50 is modelled."
	)),
}
UPPER_FLIPPER_NOTE = (
	"Platform generic upper-flipper address (CORE_FIRSTUFLIPSOL = 33). pbGameData's FLIP_SWNO(10,11) sets no upper "
	"FLIP_SW or FLIP_SOL bit and core_getSol serves 33-36 only for WPC and SAM generations, so it reads as always zero. "
	"Pin-Bot has two flippers only: the Solenoid Table and the Solenoids/Flashers list name a right and a left flipper "
	"and nothing else."
)
OVERLAY_NOTE = (
	"Platform sound-overlay range (37-44). pbGameData's hw.gameSpecific1 is 0, so S11_SNDOVERLAY is unset and "
	"pia5cb2_w never diverts the sound byte to a solenoid pattern. Unpopulated on this machine."
)

# --- Lamp matrix (public address = (column-1)*8+row). Labels from the Lamps list (printed page 51).
LAMP_LABELS = {
	1: "Game Over", 2: "Match", 3: "Ball In Play", 4: "Mouth 1 (Left)", 5: "Mouth 2", 6: "Mouth 3", 7: "Mouth 4",
	8: "Mouth 5 (Right)", 9: "Bonus 2X", 10: "Bonus 3X", 11: "Bonus 4X", 12: "Bonus 5X", 13: "Single Eject 25K",
	14: "Single Eject 50K", 15: "Single Eject 75K", 16: "Single Eject Lites Extra Ball", 17: "Drop Target Single Timer",
	18: "Advance Planet", 19: "Pluto", 20: "Neptune", 21: "Uranus", 22: "Saturn", 23: "Jupiter", 24: "Mars",
	25: "Earth", 26: "Venus", 27: "Mercury", 33: "Shoot Again", 34: "Score Energy", 35: "Solar Energy Value",
	41: "Drop Target (Upper)", 42: "Drop Target (Middle)", 43: "Drop Target (Lower)", 49: "Left Outlane Extra Ball",
	50: "Left Return Extra Ball", 51: "Special", 57: "Right Outlane Extra Ball", 58: "Right Return Extra Ball",
}
CHEST_COLOURS = {4: "Yellow", 5: "Blue", 6: "Amber", 7: "Green", 8: "Red"}
for _column, _colour in CHEST_COLOURS.items():
	for _row in range(4, 9):
		_position = _row - 3
		_qualifier = {1: " (Upper)", 3: " (Middle)", 5: " (Lower)"}.get(_position, "")
		LAMP_LABELS[(_column - 1) * 8 + _row] = f"Chest {_colour} {_position}{_qualifier}"
CHEST_LAMPS = frozenset(address for address in LAMP_LABELS if LAMP_LABELS[address].startswith("Chest "))
BACKBOX_LAMPS = frozenset(range(1, 9))
LAMP_MATRIX_WORDING = {
	1: "Game Over (Backbox)", 2: "Match (Backbox)", 3: "Ball In Play (Backbox)", 4: "Mouth 1 (Backbox Left)",
	5: "Mouth 2 (Backbox)", 6: "Mouth 3 (Backbox)", 7: "Mouth 4 (Backbox)", 8: "Mouth 5 (Backbox Right)", 9: "2X",
	10: "3X", 11: "4X", 12: "5X", 13: "Single Eject's 25K", 14: "Single Eject's 50K", 15: "Single Eject's 75K",
	16: "Single Eject's Light Extra Ball", 17: "Drop Targets' Single Timer Lamp", 33: "Shoot Again (Playfield)",
	34: "Score ENERGY", 41: "Drop Targets' Top Lamp", 42: "Drop Targets' Middle Lamp", 43: "Drop Targets' Bottom Lamp",
	49: "Left Outlane Extra Ball", 50: "Left Return Extra Ball", 57: "Right Outlane Extra Ball",
	58: "Right Return Extra Ball",
}
ROM_LAMP_NAMES = {
	1: "GAME OVER", 2: "MATCH LAMP", 3: "BALL IN PLAY", 4: "MOUTH 1  LEFT", 5: "MOUTH 2", 6: "MOUTH 3", 7: "MOUTH 4",
	8: "MOUTH 5 RIGHT", 9: "BONUS 2X", 10: "BONUS 3X", 11: "BONUS 4X", 12: "BONUS 5X", 13: "S. EJECT 25K",
	14: "S. EJECT 50K", 15: "S. EJECT 75K", 16: "S. EJECT EX. BALL", 17: "LEFT D.T. TIMER", 18: "ADVANCE PLANET",
	19: "BONUS PLUTO", 20: "BONUS NEPTUNE", 21: "BONUS URANUS", 22: "BONUS SATURN", 23: "BONUS JUPITER",
	24: "BONUS MARS", 25: "BONUS EARTH", 26: "BONUS VENUS", 27: "BONUS MERCURY", 33: "SHOOT AGAIN",
	34: "SCORE ENERGY", 35: "SCORE SOLAR", 41: "LEFT D.T. TOP", 42: "LEFT D.T. MIDDLE", 43: "LEFT D.T. BOTTOM",
	49: "LEFT OUTLANE", 50: "LEFT RETURN", 51: "SPECIAL", 57: "RIGHT OUTLANE", 58: "RIGHT RETURN", 59: "NOT USED",
}
_ROM_ROW = {1: "TOP", 2: "2ND TOP", 3: "MIDDLE", 4: "2ND BOT", 5: "BOTTOM"}
for _column, _colour in CHEST_COLOURS.items():
	for _row in range(4, 9):
		ROM_LAMP_NAMES[(_column - 1) * 8 + _row] = f"{_colour.upper()} {_ROM_ROW[_row - 3]}"
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
# Script-bound insert lights (the lN member of each FadeLights triple), normalized.
LAMP_POSITIONS = {
	9: (0.416631, 0.713453), 10: (0.495374, 0.714654), 11: (0.497934, 0.752179), 12: (0.413208, 0.751879),
	13: (0.234983, 0.21054), 14: (0.219551, 0.174653), 15: (0.204514, 0.140841), 16: (0.249587, 0.245836),
	17: (0.237215, 0.460258), 18: (0.804696, 0.555068), 19: (0.17616, 0.570783), 20: (0.296839, 0.537171),
	21: (0.458858, 0.543041), 22: (0.622967, 0.569365), 23: (0.625075, 0.641642), 24: (0.519186, 0.653416),
	25: (0.378185, 0.651937), 26: (0.295252, 0.614486), 27: (0.35709, 0.595618), 28: (0.346696, 0.31649),
	29: (0.347414, 0.343497), 30: (0.347717, 0.369769), 31: (0.347414, 0.396503), 32: (0.347414, 0.423382),
	33: (0.456312, 0.811959), 34: (0.083291, 0.242658), 35: (0.184687, 0.397774), 36: (0.402072, 0.316312),
	37: (0.402625, 0.343174), 38: (0.401887, 0.36968), 39: (0.402625, 0.396437), 40: (0.402625, 0.423299),
	41: (0.169566, 0.425283), 42: (0.16335, 0.454972), 43: (0.158103, 0.484641), 44: (0.457646, 0.31609),
	45: (0.457646, 0.342774), 46: (0.458015, 0.369451), 47: (0.458015, 0.395957), 48: (0.457646, 0.422998),
	49: (0.06295, 0.651669), 50: (0.133774, 0.65188), 51: (0.704119, 0.589849), 52: (0.512026, 0.315932),
	53: (0.512371, 0.343003), 54: (0.512371, 0.369657), 55: (0.512371, 0.396209), 56: (0.513062, 0.422863),
	57: (0.84908, 0.65144), 58: (0.777576, 0.651774), 60: (0.567773, 0.316173), 61: (0.567428, 0.343243),
	62: (0.567773, 0.369898), 63: (0.567773, 0.396718), 64: (0.568119, 0.423259),
}
# Playfield G.I. bulbs: the Light member of each retained GI socket pair that draws the bulb mesh.
GI_POSITIONS = (
	("Light1", (0.21546, 0.738469)), ("Light2", (0.186195, 0.67496)), ("Light3", (0.75837, 0.784472)),
	("Light4", (0.695547, 0.738237)), ("Light5", (0.152342, 0.783904)), ("Light6", (0.726304, 0.673855)),
	("Light7", (0.86362, 0.583699)), ("Light8", (0.064374, 0.603601)), ("Light9", (0.055271, 0.550077)),
	("Light10", (0.055485, 0.45015)), ("Light11", (0.062371, 0.400887)), ("Light12", (0.068875, 0.343691)),
	("Light13", (0.05472, 0.322473)), ("Light14", (0.641591, 0.312079)), ("Light15", (0.640684, 0.279716)),
	("Light16", (0.655815, 0.189072)), ("Light17", (0.850888, 0.207732)), ("Light18", (0.148659, 0.232743)),
	("Light19", (0.281805, 0.147236)), ("Light20", (0.653852, 0.364728)), ("Light21", (0.23497, 0.060388)),
	("Light22", (0.134512, 0.109163)), ("Light23", (0.762438, 0.075472)), ("Light24", (0.806058, 0.077116)),
	("Light25", (0.838424, 0.416073)), ("Light26", (0.707084, 0.335457)), ("Light27", (0.837926, 0.2582)),
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Pin-Bot retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Pin-Bot extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Pin-Bot retained extraction manifest is missing: {manifest_path}")
	if _file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
		raise RuntimeError(f"Pin-Bot retained extraction manifest is not the pinned one: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH)):
		raise RuntimeError("Pin-Bot retained extraction manifest does not match the extracted files")
	if len(actual["files"]) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"Pin-Bot retained extraction file count mismatch: {len(actual['files'])} != {EXTRACTION_FILE_COUNT}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def placement(identifier: str, role: str, xy: tuple[float, float], status: str, *refs: str) -> dict[str, Any]:
	return {"id": identifier, "role": role, "space": "playfield", "x": round(xy[0], 6), "y": round(xy[1], 6), "provenance": provenance(*refs, status=status)}


def located(identifier: str, role: str, points: list[tuple[float, float]], status: str, *refs: str) -> dict[str, Any]:
	placements = [
		placement(f"{identifier}.{role}" + (f".{index}" if len(points) > 1 else ""), role, xy, status, *refs)
		for index, xy in enumerate(points, start=1)
	]
	order = {"candidate": 0, "observed": 1, "validated": 2}
	return {"status": min((p["provenance"]["status"] for p in placements), key=order.__getitem__), "placements": placements}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


def output_id(address: int) -> str:
	if address in SOLENOID_LABELS:
		return f"device.{slug(SOLENOID_LABELS[address])}"
	return f"device.{slug(VIRTUAL_SOLENOIDS[address][0]) if address in VIRTUAL_SOLENOIDS else slug(solenoid_platform_label(address))}"


def solenoid_platform_label(address: int) -> str:
	if 33 <= address <= 36:
		return f"Unused Upper Flipper Slot {address}"
	if 37 <= address <= 44:
		return f"Unused Sound Overlay Slot {address}"
	raise KeyError(address)


def _device(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind, "binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def _excerpt(identifier: str, locator: str, filename: str, method: str = "manual", transcribed_by: str = "curator, read from the rendered pages") -> dict[str, Any]:
	path = EXCERPT_DIRECTORY / filename
	return {
		"id": identifier, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": _file_sha256(path),
		"method": method, "transcribed_by": transcribed_by, "reviewed": True,
	}


def source_records() -> list[dict[str, Any]]:
	callout_seed_sha = _file_sha256(CALLOUT_SEED_PATH)
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned PinmameGetGames catalog records for the ten-driver pb_* clone tree rooted at pb_l5",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c lines 38-41 INITGAMEFULL macro and lines 274-275 INITGAMEFULL(pb, GEN_S11X, s11_dispS11, 14, "
				"FLIP_SWNO(10,11), 0,0,0,0, 53, 0, 48, 54, 55,52): hw.display, gameSpecific1 and gameSpecific2 are 0, sxx.muxSol "
				"= 14 and sxx.ssSw = {53,0,48,54,55,52}; lines 276-356 the pb_* ROM sets and lines 357-366 CORE_GAMEDEF(pb,l5) "
				"and the nine CORE_CLONEDEFs; src/wpc/s11.c lines 61-65 s11_dispS11 (DISP_SEG_7 rows of CORE_SEG16 and CORE_SEG8 "
				"plus four single CORE_SEG7S digits), lines 191-200 the switch-driven special-solenoid loop, setSSSol's ssSolNo "
				"table, lines 558-580 updsol (the muxSol copy of the low solenoid byte to 25-32 while 14 is pulsed), pia0cb2_w "
				"(S11_GAMEONSOL), pia4a_r returning core_getSwCol without inversion, MACHINE_INIT(s11) output sizing and the "
				"pb_ output-type block (9-10 typed as #89 bulbs and then 10 as reverse #44 \"Playfield GI\", 11 \"Backbox GI\", "
				"15-16, 18 \"Aux board\" and 26-32 as #89 bulbs, commented \"Mux relay is solenoid #12\"); src/wpc/s11.h "
				"S11_GAMEONSOL 23 and the diagnostic switch numbers; src/wpc/core.h CORE_FIRSTSSSOL 17, CORE_SSFLIPENSOL 23, "
				"CORE_FIRSTLFLIPSOL 45, CORE_FIRSTSIMSOL 49, CORE_FIRSTCUSTSOL 51, CORE_FLIPPERSWCOL 11 and DISP_SEG_7; "
				"src/wpc/core.c core_updateSw's FLIP_SWNO copy and synthetic 45-48; src/wpc/gen.h GEN_S11X"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json", "revision": "repository",
			"locator": "System 11 sequential switch/lamp matrices, dedicated diagnostic inputs, the Country jumper, the A/C mux alias bank, special solenoids, the sound-overlay range, synthetic flipper outputs and the 81-88 flipper column",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.pinbot.1986/archive-PinBotInstructionManualSchematics600dpi/PinBot%20Instruction%20Manual%20%26%20Schematics%20600%20dpi%20scan.pdf",
			"original_filename": "PinBot Instruction Manual & Schematics 600 dpi scan.pdf", "sha256": MANUAL_SHA256,
			"acquired_at": "2026-10-09T11:05:22Z", "source_id": "PinBotInstructionManualSchematics600dpi",
			"locator": (
				"72-page 600 dpi colour scan of the Williams PIN-BOT Instruction Manual 16-549-101 (October 6, 1986) with its "
				"Section 3 schematics, no text layer. Internet Archive item PinBotInstructionManualSchematics600dpi, details page "
				"https://archive.org/details/PinBotInstructionManualSchematics600dpi, file "
				"https://archive.org/download/PinBotInstructionManualSchematics600dpi/PinBot%20Instruction%20Manual%20%26%20Schematics%20600%20dpi%20scan.pdf, "
				"uploader mhkohne@kohne.org, published 2014-10-27, no rights or licence metadata on the item, SHA-1 "
				"20a97870b386b4526dd7d6e18032d34175394fe9 per the item metadata. For Sections 1 and 2 the "
				"printed folio \"PIN-BOT n\" is PDF page n + 6. PDF 2 repeats the Solenoid Table beside the ROM and Jumper "
				"Table; PDF 32 Lamp-Matrix Table; PDF 33 Solenoid Table; PDF 35 Switch-Matrix Table; PDF 41-54 board and "
				"mechanism assembly pages; PDF 55 Playfield Parts; PDF 56-58 the Solenoids/Flashers, Lamps and Switches lists "
				"with their numbered locations drawings; PDF 69 Power Wiring Diagram; PDF 71 a foldout repeating the lamp and "
				"switch matrices."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronic Games, Inc.; scan by mhkohne hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.pinbot.switch-matrix", "PDF page 35 (printed 29) and the foldout on PDF page 71, PIN-BOT Switch-Matrix Table", "switch-matrix.md"),
				_excerpt("excerpt.pinbot.lamp-matrix", "PDF page 32 (printed 26) and the foldout on PDF page 71, PIN-BOT Lamp-Matrix Table", "lamp-matrix.md"),
				_excerpt("excerpt.pinbot.solenoid-table", "PDF page 33 (printed 27) and the copy on PDF page 2, PIN-BOT Solenoid Table", "solenoid-table.md"),
				_excerpt("excerpt.pinbot.switch-locations", "PDF page 58 (printed 52), Switches parts list", "switch-locations.md"),
				_excerpt("excerpt.pinbot.lamp-locations", "PDF page 57 (printed 51), Lamps list", "lamp-locations.md"),
				_excerpt("excerpt.pinbot.solenoid-flasher-locations", "PDF page 56 (printed 50), Solenoids/Flashers and Rubber Parts lists", "solenoid-flasher-locations.md"),
				_excerpt("excerpt.pinbot.playfield-parts", "PDF page 55 (printed 49), Playfield Parts", "playfield-parts.md"),
				_excerpt("excerpt.pinbot.mechanism-assemblies", "PDF pages 41 and 47-54 (printed 35 and 41-48), board, backbox and mechanism assembly parts lists", "mechanism-assemblies.md"),
				_excerpt("excerpt.pinbot.diagnostics-and-operation", "PDF pages 2, 7-8, 10-12 and 31-36 (printed 1-2, 4-6 and 25-30), ROM summary, game operation and Test/Diagnostic Procedures", "diagnostics-and-operation.md"),
			],
		},
		{
			"id": IPDB_MANUAL_SOURCE, "kind": "manual",
			"uri": "https://web.archive.org/web/20251127185102id_/https://www.ipdb.org/files/1796/Williams_1986_Pin_bot_Manual.pdf",
			"original_filename": "Williams_1986_Pin_bot_Manual.pdf", "sha256": IPDB_MANUAL_SHA256,
			"acquired_at": "2026-10-09T11:04:45Z", "source_id": "ipdb.1796",
			"locator": (
				"IPDB machine 1796 (Williams PIN*BOT, model 549, manufactured October 6, 1986; machine page "
				"https://www.ipdb.org/machine.cgi?id=1796, read through https://web.archive.org/web/2024id_/https://www.ipdb.org/machine.cgi?id=1796, "
				"resource https://www.ipdb.org/files/1796/Williams_1986_Pin_bot_Manual.pdf) manual download through the "
				"Wayback Machine, a 79-page 150 dpi bilevel scan of the same instruction manual. Retained as an identity "
				"cross-check of the machine page; every cited cell is read from the 600 dpi scan."
			),
			"license": "NOASSERTION", "attribution": "Williams Electronic Games, Inc.; hosted by the Internet Pinball Machine Database",
			"rights": "NOASSERTION",
		},
		{
			"id": ROM_SOURCE, "kind": "rom_static_analysis",
			"uri": "external:pinmame-review-artifacts/williams.pinbot.1986/rom-name-tables/",
			"revision": "pbot_u27.l5",
			"locator": (
				"Lamp, switch and coil name tables of the U27 program ROM of every pb_* set in the local corpus (l5, l5h, l3, "
				"l2, l1, p4, j5), decoded by tools/pinbot_rom_name_tables.py as 14-byte entries (seven characters per player "
				"display). The lamp and switch tables run in public-address order and the coil table in coil-test order; the "
				"excerpt lists the ROM member hashes and every entry."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronic Games program ROMs and community ROMs, user-authorized local copies; ROM bytes are not redistributed",
			"excerpts": [
				_excerpt("excerpt.pinbot.rom-name-tables", "U27 lamp, switch and coil tables of the seven local pb_* sets", "rom-name-tables.md", method="mixed", transcribed_by="tools/pinbot_rom_name_tables.py, checked by the curator against the service-test displays"),
			],
		},
		{
			"id": RUNTIME_SOURCE, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/system-11/pinbot-l5-service-and-mechanisms.json",
			"revision": PINMAME_REVISION, "sha256": _file_sha256(RUNTIME_EVIDENCE_PATH),
			"locator": (
				"Pinned LibPinMAME runs of pb_l5, each from a new state directory inheriting only the retained initialization "
				"run's NVRAM: the Coil Test paired step by step with the ROM coil table, the Single Lamps test stepped through "
				"designators 01-64 with the Credit button, the Switch Levels test over public 1-64 and 81-88, ten power-up "
				"probes with switches held from start, two visor probes, and two gameplay runs (one with static switches, one "
				"answering the visor and ramp drives). Raw runs, manifest and hashes are retained outside the repository."
			),
			"license": "NOASSERTION", "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/pinbot-1986/source/PinBot%20(Williams%201986).vpx",
			"original_filename": "PinBot (Williams 1986).vpx", "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPX recreation of the physical machine by bord (table_version 1.1, March 2019, per "
				f"info.json), copied from the contributor's table collection. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/952 and y/1974. Geometry authority for script-bound table objects, checked against "
				"the manual's numbered locations drawings."
			),
			"license": "NOASSERTION", "attribution": "bord", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/pinbot-1986/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded script (2,868 lines). Runtime authority: cGameName = \"pb_l5\", UseLamps = 0 with a "
				"FrameTimer/ChangedLamps loop into a LampFader whose FadeLights.obj(n) arrays bind lamps 9-58 and 60-64 to their "
				"lN/lNa/lNz lights; SolCallback 1-8, 10, 12, 18, 23, 25, 26, 29-32, 9/11/27/28 (backglass sprites) and "
				"sLRFlipper/sLLFlipper; cvpmBallStack trough (16, 17, 18; two balls), single eject (38) and eye saucers (25, "
				"26); cvpmDropTarget bank 49-51; cvpmMech visor on solenoid 13 with switches 46 (position 0) and 47 (58); the "
				"ramp timer writing switch 44. Object-by-object cross-reference in "
				"external:pinmame-review-artifacts/williams.pinbot.1986/geometry/script-bindings.md."
			),
			"license": "NOASSERTION", "attribution": "bord", "rights": "NOASSERTION",
		},
		{
			"id": CORPUS_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "https://github.com/jsm174/vpx-standalone-scripts/blob/15d112648a1b94b9f59eb8b3c335d57283653c50/" + quote("PinBot (Williams 1986) 2.1.1/PinBot (Williams 1986) 2.1.1.vbs.original", safe="/"),
			"revision": CORPUS_REVISION, "sha256": CORPUS_SCRIPT_SHA256,
			"locator": (
				"Pinned known-working script of the later 2.1.1 build of bord's table (vpx-standalone-scripts). It keeps the "
				"retained table's bindings for every address this definition cites (the same trough, saucer, drop-bank, visor "
				"mechanism and SolCallback assignments, and the same eye-flash sprite for solenoids 10 and 18)."
			),
			"license": "NOASSERTION", "attribution": "bord and later contributors credited in the script", "rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI, "original_filename": "s11.vbs", "sha256": VPM_S11_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads (script.vbs line 13 LoadVPM \"01560000\", \"S11.VBS\", "
				f"3.26), retained with core.vbs (SHA-256 {VPM_CORE_SHA256}). S11.VBS defines swLRFlip = 82 and swLLFlip = 84 and "
				"sets them from the flipper keys in vpmKeyDown/vpmKeyUp; core.vbs routes KeyDownHandler/KeyUpHandler to them."
			),
			"license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
			"excerpts": [
				_excerpt("excerpt.pinbot.vpm-script-library-flippers", "s11.vbs lines 37-40, 69-80 and 104; core.vbs lines 2854-2855; script.vbs lines 13, 49-50, 128, 159 and 209-210", "vpm-script-library-flippers.md", transcribed_by="curator, read from the library and script files"),
			],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/pinbot-1986/extracted-vpxtool.manifest.json",
			"sha256": EXTRACTION_MANIFEST_SHA256,
			"locator": (
				f"Retained vpxtool git:v0.33.3 extraction of the retained table, {EXTRACTION_FILE_COUNT} files, with a full sorted "
				f"path/size/SHA-256 manifest whose own SHA-256 is this record's sha256. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
		{
			"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:tools/seeds/williams/pinbot-1986-callouts.json", "sha256": callout_seed_sha,
			"locator": (
				"2026-10-09 factory location-drawing callout check of the solenoid (PDF 56), lamp (PDF 57) and switch (PDF 58) "
				"drawings: every callout read independently on gridded tiles of the retained renders without table data, one "
				"verifier correction recorded with its reason, per-page control and callout fits; a table placement whose own "
				"callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py)."
			),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		},
	]


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11A CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
		"return_wire": return_wire, "return_connection": return_connection, "driver_transistor": f"column {drive_component}",
	}


RUNTIME_SWITCH_NOTE = (
	" In the ROM's Switch Levels test (run switch-levels) holding public {address} at 1 makes the player 1 and 2 displays "
	"show the ROM's name for it, so the ROM reads it active at 1. pbGameData has no inverted-switch mask and pia4a_r returns "
	"core_getSwCol raw, so the contact the matrix sees is open at rest and closed when actuated."
)


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, role) in DEDICATED_LABELS.items():
		items.append(_device(
			f"switch.diagnostic-{abs(address)}", label, "switch", "pinmame.input.switch", address, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": str(address)}], roles=[role], normally_closed=False,
			physical={
				"location": "coin door and CPU board diagnostic switches", "switch_type": "button",
				"notes": (
					"System 11 diagnostic input on the S11_COMINPORT keyboard port. The manual's Test/Diagnostic Procedures "
					"drive every test from the coin-door ADVANCE button and AUTO-UP/MANUAL-DOWN switch and name the CPU board's "
					"SW1 the Sound Diagnostic and SW2 the CPU Diagnostic switch. The retained runs enter and step the tests with "
					"-6 and -7."
				),
			},
			spatial=not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
		))
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"switch.matrix-{address}"
		unused = address in UNUSED_SWITCHES
		label = f"Not Used (Matrix Position {address})" if unused else SWITCH_LABELS[address]
		physical: dict[str, Any] = {}
		notes = f"Printed switch-matrix column {column} ({SWITCH_COLUMN_WIRING[column][0]}), row {row} ({SWITCH_ROW_WIRING[row][0]})."
		notes += f" The ROM's switch table names it \"{ROM_SWITCH_NAMES[address]}\"."
		if unused:
			notes += (
				" The Switch-Matrix Table and the Switches parts list both print \"Not Used\" here and the ROM's own entry "
				"says NOT USED."
			)
			if address in (57, 58):
				notes += (
					" The Switch Levels test still reports a closure here by that name, so the ROM scans the position; no "
					"switch is fitted."
				)
			elif address >= 61:
				notes += " The Switch Levels test showed nothing while this address was held, so the ROM does not report it."
		else:
			if address in SWITCH_PARTS:
				physical["part_number"] = SWITCH_PARTS[address]
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			if address in MATRIX_WORDING and MATRIX_WORDING[address] != label:
				notes += f" The Switch-Matrix Table prints \"{MATRIX_WORDING[address]}\"."
			if address in PARTS_LIST_WORDING and PARTS_LIST_WORDING[address] != label:
				notes += f" The Switches parts list prints \"{PARTS_LIST_WORDING[address]}\"."
			if address in UNTYPED_SWITCHES:
				notes += UNTYPED_NOTE
			if address == 33:
				notes += (
					" The Switches parts list misprints rows 33-37: it gives 33 a visor-target part and the words \"Visor "
					"Target top,yellow)\" and lists only four 5-bank colours for 34-37. The Switch-Matrix Table, the ROM's "
					"switch table (\"R. 5BANK 1  TOP\" through \"R. 5BANK 5  BOT\") and the retained script all put the five "
					"right 5-bank targets at 33-37, top to bottom, so the label follows them and the parts-list row is kept "
					"here as printed. That row's part number (SW-1A-163-1) is the misprint's, so no part number is asserted for this "
					"target; the list gives A-11317-3 for 34-37."
				)
			if 34 <= address <= 37:
				notes += " See switch 33 for the parts list's misprinted 5-bank rows; the targets select the chest rows, not a colour."
			if address in (10, 11):
				side = "left" if address == 10 else "right"
				button = 84 if address == 10 else 82
				notes += (
					f" The Lane Change switch is item 2b (SW-1A-150) of the {side} C-9954 Flipper Base/Lane Change Assembly, a "
					"different part from the same assembly's End of Stroke switch 03-7811, which has no matrix address. "
					f"pbGameData's FLIP_SWNO(10,11) makes core_updateSw rewrite this address from PinMAME's flipper column, "
					f"public {button}, on every update, so a consumer cannot drive it directly: it drives {button}, and the "
					f"Switch Levels test shows \"{ROM_SWITCH_NAMES[address]}\" while {button} is held."
				)
			if address in SPECIAL_SOLENOID_SWITCH.values():
				special = next(sol for sol, sw in SPECIAL_SOLENOID_SWITCH.items() if sw == address)
				notes += (
					f" This switch also fires solenoid {special} directly: it is entry {special - 16} of pbGameData's "
					"sxx.ssSw, so while the enable (23) is on PinMAME asserts that special solenoid from this switch's own "
					"state, and in the gameplay run each closure fired it within one poll."
				)
			if address in (54, 55):
				notes += (
					" A separate kicker actuating switch (A-4834-H, or B-8734 with an RC network, per the Switches list's "
					"footnote) completes the coil circuit itself and has no matrix address."
				)
			notes += RUNTIME_SWITCH_NOTE.format(address=address)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
			"wiring": _switch_wiring(column, row),
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if unused:
			availability = "unused"
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE, ROM_SOURCE)
		elif address in CABINET_SWITCH_ROLES:
			availability = "used"
			extra["roles"] = [CABINET_SWITCH_ROLES[address]]
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address == 9:
				notes += (
					" A playfield-mounted tilt (SW-1A-117) that senses the cabinet being tipped, not a ball; the switch drawing "
					"marks it at the lower left of the playfield underside, and it is treated like the cabinet tilts."
				)
		else:
			availability = "used"
			extra["normally_closed"] = False
			refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			if address in SWITCH_PROJECTIONS:
				xy, reason = SWITCH_PROJECTIONS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "validated", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += " " + reason
			else:
				obj, xy = SWITCH_OBJECTS[address]
				extra["spatial"] = located(identifier, "sensor", [xy], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
				notes += f" Placed at the retained table's {obj}, which the script binds to this address."
				if address in SWITCH_OBJECT_NOTES:
					notes += " " + SWITCH_OBJECT_NOTES[address]
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	column = flipper_column_inputs(
		flip_swno=FLIP_SWNO, flip_swno_text="FLIP_SWNO(10,11)",
		core_refs=(CORE_SOURCE, CONTROLLER_SOURCE), button_refs=(VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE, RUNTIME_SOURCE),
		button_notes={
			side: (
				f"The retained known-working script drives it: Table1_KeyDown and Table1_KeyUp pass the {side} flipper key to "
				"KeyDownHandler/KeyUpHandler, which core.vbs routes to S11.VBS vpmKeyDown/vpmKeyUp, and those set "
				f"Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
				f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). In the Switch "
				f"Levels run holding this address showed \"{'L. LANE CHANGE' if side == 'left' else 'R. LANE CHANGE'}\". The "
				f"physical counterpart is the {side} cabinet flipper button (SW-1010A-13), which fires the flipper coil "
				"through the switched-solenoid supply with no matrix address of its own."
			)
			for side in ("left", "right")
		},
		unused_notes=vpm_staged_flipper_notes(), unused_note_refs=(VPM_LIBRARY_SOURCE,),
	)
	for item in column:
		if item["availability"] == "used":
			item["normally_closed"] = False
	items.extend(column)
	items.append(_device(
		"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used",
		(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
		aliases=[{"namespace": "pinmame.dip", "value": "0"}],
		physical={
			"location": "System 11A CPU board", "switch_type": "dip",
			"notes": (
				"System 11's single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7. The manual's ROM and Jumper Table "
				"(PDF 2) and its circuit-board text name jumper W7 on the CPU board, cut for West German games (pinned s11.c labels "
				"pia2a_r \"Jumper W7\" too), and its Special Preset "
				"Adjustments (Install German 1-6 and others) are the operator-facing counterpart."
			),
		},
		spatial=not_applicable("dip_switch", MANUAL_SOURCE),
	))
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	pair_of = {a: pair for pair, (a, c, *_rest) in AC_PAIRS.items() for a in (a, c)}
	for address in list(range(1, 23)) + list(range(25, 33)):
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		kind = SOLENOID_KIND[address]
		number = SOLENOID_MANUAL_NUMBER[address]
		step = COIL_TEST_ORDER.index(address) + 1
		notes = f"Solenoid Table entry {number} (\"{SOLENOID_TABLE_WORDING[address]}\")"
		if LIST_WORDING[address] != SOLENOID_TABLE_WORDING[address]:
			notes += f"; the Solenoids/Flashers list prints \"{LIST_WORDING[address]}\""
		notes += "."
		if address in pair_of:
			pair = pair_of[address]
			a_side, c_side, cpu, power, driver, cpu_wire = AC_PAIRS[pair]
			notes += (
				f" Switched pair {pair:02d}A/{pair:02d}C on driver {driver}: the \"A\" load is pulsed with the Solenoid Select "
				f"relay (14) released and the \"C\" load with it energized (the table's note 3). Pinned updsol publishes the "
				f"A load at {a_side} and the C load at {c_side}."
			)
			wiring = {
				"board": "System 11A CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu if address == a_side else f"{cpu} (C side, through the Solenoid Select relay)",
				"control_wire": cpu_wire, "power_connection": power,
			}
		else:
			cpu, power, driver = CONTROLLED[address]
			kind_word = "Controlled" if address <= 16 else f"Special #{address - 16}"
			notes += f" Solenoid Type \"{kind_word}\"."
			wiring = {
				"board": "System 11A CPU board", "driver_transistor": driver, "drive_wire": SOLENOID_WIRE[address],
				"control_connection": cpu, "power_connection": power,
			}
		notes += (
			f" The ROM's coil table names it \"{ROM_COIL_NAMES[address]}\", and the ROM's Coil Test (run coil-test) pulses "
			f"this address at step {step} while displaying that name."
		)
		if 17 <= address <= 22:
			ss_switch = SPECIAL_SOLENOID_SWITCH[address]
			if ss_switch:
				notes += (
					f" pbGameData's sxx.ssSw entry for this special solenoid is switch {ss_switch} ({SWITCH_LABELS[ss_switch]}), "
					"so while the enable (23) is on PinMAME drives this output from that switch's own state, PinMAME's model of "
					"the switched-solenoid circuit in which the switch fires the coil itself; the gameplay run fired it on each "
					"closure."
				)
			else:
				notes += (
					" pbGameData's sxx.ssSw entry for this slot is 0: it has no actuating switch and is fired only by the CPU "
					"through setSSSol, which fits a lamp load on a special driver."
				)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		else:
			notes += " The retained script has no callback for this address."
		physical: dict[str, Any] = {"part_number": SOLENOID_PART[address]}
		extra_roles: list[str] = []
		spatial: dict[str, Any] | None = None
		handled = True
		refs: tuple[str, ...] = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		if address == 25:
			notes += " The Backbox Parts Listing carries the Knocker Assembly (B-10686), so the knocker is in the backbox."
			extra_roles = ["cabinet.knocker"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in (9, 27, 28):
			notes += (
				" A backbox load: the manual puts it on the insert board behind the backglass and the ROM names it a "
				"\"BACKGLS.\" output."
			)
			extra_roles = ["cabinet.backbox-flasher"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE, ROM_SOURCE)
		elif address in (15, 16):
			notes += (
				" A backbox load: the \"Top\" flashers are the D-11380 Flashbar and D-11381 domes of the Top Backbox Flasher "
				"assembly in the Backbox Parts Listing."
			)
			extra_roles = ["cabinet.backbox-flasher"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 11:
			notes += (
				" A relay (5580-09555-01 on the C-11232-1 Relay Snubber board, the table's note 4) switching the insert-board "
				"general illumination behind the backglass; the ROM calls it \"BACKGLS G.I.\". The retained script treats it as "
				"active-low (on means backglass G.I. off). Pinned PinMAME types it as a reverse-acting #44 G.I. output, its "
				"brightness model for the same behaviour."
			)
			extra_roles = ["gi.backbox"]
			spatial = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 12:
			notes += (
				" A relay (5580-09555-01 on the C-11232-1 Relay Snubber board) feeding the playfield general illumination from "
				"the power supply board (connection 3P7-1). The retained script's PFGI handler treats it as active-low: on "
				"turns its 54-light GI collection off. In attract mode the ROM toggles 11 and 12 alternately (power-up probes). "
				"Pinned PinMAME leaves it a plain two-state output and instead types address 10 as the reverse-acting "
				"\"Playfield GI\", a brightness-model label that disagrees with the manual's wiring and the ROM's \"PLAYFLD G.I.\" "
				"name for 12; the manual and the ROM decide the physical role. The manual prints no G.I. bulb count; the "
				"placements are the 27 bulb sockets of the retained table's GI collection (the Light member of each pair, "
				"which draws the bulb mesh), three of them the #44 bulbs in the B-9414 jet bumper caps. A table's G.I. grouping is not "
				"the machine's wiring, so these placements stay observed and no quantity is asserted."
			)
			extra_roles = ["gi.playfield"]
			spatial = located(identifier, "emitter", [xy for _, xy in GI_POSITIONS], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE)
		elif address in (10, 18):
			side = "right" if address == 10 else "left"
			notes += (
				f" #1251 flash lamps lighting the {side} side of the visor; the manual and the ROM (\"{ROM_COIL_NAMES[address]}\") "
				"call it general illumination. Neither the manual nor the retained table gives the bulbs a position: the "
				"manual's locations drawings mark no visor lamp and the Visor Assembly list holds no socket, and the table "
				"lights one Flasher sprite between the eyes for both 10 and 18, a glow on the part the bulbs light rather than "
				"a socket. The spatial key is omitted."
			)
			if address == 10:
				notes += " Pinned PinMAME's pb_ block types this address as a reverse-acting \"Playfield GI\" output; see address 12."
			else:
				notes += " Pinned PinMAME's pb_ block types this address as a #89 bulb with the comment \"Aux board\"."
			spatial = None
		elif address == 14:
			notes += (
				" The A/C select relay (5580-09555-01 on the C-11232-1 Relay Snubber board, connection 8P3-14). Pinned "
				"PinMAME publishes its own state here and, while it is pulsed, moves the low solenoid byte to 25-32. In the "
				"Coil Test and in play the ROM energizes it ahead of each C-side pulse and releases it for A-side pulses; "
				"pinned s11.c's comment \"Mux relay is solenoid #12\" in the pb_ block is wrong for this machine, where the "
				"driver data and the manual both say 14."
			)
			extra_roles = ["internal.ac-select"]
			spatial = not_applicable("internal_nonvisual", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 13:
			notes += (
				" The relay (5580-09555-01) that runs the visor motor, an 11 rpm 24 VAC motor (14-7941) turning the A-11154 cam "
				"of the B-11169 Visor Motor Assembly; the cam's two snap-action limit switches are Visor Closed (46) and Visor "
				"Open (47). The ROM runs it from about 1.7 s after power-up, and the visor probes show it stopping when 47 "
				"closes; see the visor mechanism."
			)
			handled = False
		else:
			handled = False
		if not handled:
			if address not in SOLENOID_OBJECTS:
				raise RuntimeError(f"no spatial disposition for solenoid {address}")
			objects = SOLENOID_OBJECTS[address]
			role = "emitter" if kind in ("flasher", "gi", "lamp") else "effect"
			status = "validated" if address in SOLENOID_PROJECTED or kind == "flasher" else "observed"
			spatial = located(identifier, role, [xy for _, xy in objects], status, VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)
			if address in SOLENOID_PROJECTED:
				notes += f" Placed at the retained table's {objects[0][0]}, a documented projection onto {SOLENOID_PROJECTED[address]}."
			elif kind == "flasher":
				notes += " " + FLASHER_NOTES[address] + " The manual's locations drawings draw no flasher, so these are the table's modelled bulbs, validated by their script binding and the manual's location wording."
			else:
				notes += f" Placed at the retained table's {objects[0][0]}."
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": number}]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		if extra_roles:
			extra["roles"] = extra_roles
		if spatial is not None:
			extra["spatial"] = spatial
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	for address in (23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
		if address in VIRTUAL_SOLENOIDS:
			label, availability, role, notes = VIRTUAL_SOLENOIDS[address]
		elif address <= 36:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", UPPER_FLIPPER_NOTE
		else:
			label, availability, role, notes = solenoid_platform_label(address), "unused", "internal.unused-platform-slot", OVERLAY_NOTE
		refs = (CONTROLLER_SOURCE, CORE_SOURCE, RUNTIME_SOURCE) if availability == "used" else (CONTROLLER_SOURCE, CORE_SOURCE)
		items.append(_device(
			f"device.{slug(label)}", label, "virtual", "pinmame.output.solenoid", address, availability, refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}], roles=[role], physical={"notes": notes},
			spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 65):
		column, remainder = divmod(address - 1, 8)
		column += 1
		row = remainder + 1
		identifier = f"lamp.matrix-{address}"
		wiring = {
			"board": "System 11A CPU board",
			"drive_wire": LAMP_COLUMN_WIRING[column][0], "drive_connection": LAMP_COLUMN_WIRING[column][1],
			"return_wire": LAMP_ROW_WIRING[row][0], "return_connection": LAMP_ROW_WIRING[row][1],
			"driver_transistor": f"column {LAMP_COLUMN_WIRING[column][2]}, row {LAMP_ROW_WIRING[row][2]}",
		}
		aliases = [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}]
		notes = f"Printed lamp-matrix column {column}, row {row}. The ROM's lamp table names it \"{ROM_LAMP_NAMES[address]}\""
		if address == 59:
			notes += (
				"; the Lamp-Matrix Table and the Lamps list print \"Not Used\". No socket is fitted: the retained script "
				"comments out its FadeLights line and has no l59 object, and the manual's lamp drawing draws no 59. The Single "
				"Lamps test still steps designator 59 and blinks this matrix position, which is the test's own sweep, not a "
				"load."
			)
			items.append(_device(
				identifier, "Not Used (Lamp Matrix Position 59)", "lamp", "pinmame.output.lamp", address, "unused",
				(MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE), aliases=aliases, wiring=wiring,
				physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
			))
			continue
		label = LAMP_LABELS[address]
		notes += (
			f", and in the Single Lamps test (run single-lamps) designator {address:02d} blinks this address while the displays "
			"show that name."
		)
		if address in LAMP_MATRIX_WORDING and LAMP_MATRIX_WORDING[address] != label:
			notes += f" The Lamp-Matrix Table prints \"{LAMP_MATRIX_WORDING[address]}\"."
		physical: dict[str, Any] = {"quantity": 2 if address == 1 else 1}
		if address in CHEST_LAMPS:
			physical["part_number"] = "#555 (24-8768)"
			notes += (
				" One of the 25 chest-panel lamps: the Lamp-Matrix Table marks it with its #555 triangle and the C-11309 Chest "
				"Lamp Matrix Board carries it with its own diode. The visor targets select the chest column (colour) and the "
				"right 5-bank targets the row."
			)
		else:
			physical["part_number"] = "#44 (24-6549)"
		if address == 1:
			notes += " The Lamp-Matrix Table marks this circuit with its boxed \"2\" Double Lamp legend; both bulbs are in the backbox."
		if address in BACKBOX_LAMPS:
			notes += " The manual puts it in the backbox, so it has no playfield position."
			if 4 <= address <= 8:
				notes += " The retained script mirrors it onto backglass flasher sprites (UpdateMultipleLamps)."
			extra = {"roles": ["cabinet.backglass-indicator"], "spatial": not_applicable("cabinet_or_service", MANUAL_SOURCE)}
		else:
			light = f"l{address}"
			notes += f" Placed at the retained table's Light {light}, the insert light the script's FadeLights.obj({address}) drives."
			if address in (34, 51):
				notes += " The retained script also mirrors this lamp onto a backglass flasher sprite; the physical lamp is the playfield insert."
			if address in (49, 57):
				notes += " The script's FadeLights array for this lamp also holds a Flasher sprite whose position fields disagree with its drag points; the light is the bulb."
			extra = {"spatial": located(identifier, "emitter", [LAMP_POSITIONS[address]], "observed", VPX_TABLE_SOURCE, VPX_EXTRACTION_SOURCE, MANUAL_SOURCE)}
		physical["notes"] = notes
		items.append(_device(
			identifier, label, "lamp", "pinmame.output.lamp", address, "used",
			(MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
			aliases=aliases, wiring=wiring, physical=physical, **extra,
		))
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int, width: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index, "segment_start": start,
			"width": width, "height": 1, "physical_location": "cabinet_or_service",
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		}

	return [
		display("display.player-1", "Player 1 score, seven 16-segment alphanumeric digits (C-10866 panel)", 0, 1, 7),
		display("display.player-2", "Player 2 score, seven 16-segment alphanumeric digits (C-10866 panel)", 1, 9, 7),
		display("display.player-3", "Player 3 score, seven 7-segment digits with commas (C-8364-1 panel)", 2, 21, 7),
		display("display.player-4", "Player 4 score, seven 7-segment digits with commas (C-8364-1 panel)", 3, 29, 7),
		display("display.ball-in-play-match-left", "Ball In Play / Match, left digit (C-8365-1 panel)", 4, 0, 1),
		display("display.ball-in-play-match-right", "Ball In Play / Match, right digit (C-8365-1 panel)", 5, 8, 1),
		display("display.credits-left", "Credits, left digit (C-8365-1 panel)", 6, 20, 1),
		display("display.credits-right", "Credits, right digit (C-8365-1 panel)", 7, 28, 1),
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly:
			record["assembly_part_number"] = assembly
		return record

	m = (MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
	return [
		mechanism(
			"mechanism.trough", "Outhole and two-ball trough", "kicker", [output_id(1), output_id(2)],
			["switch.matrix-16", "switch.matrix-17", "switch.matrix-18"],
			"A drained ball rests on the outhole switch (16) at the lower-left end of the trough tube, and the Outhole Kicker "
			"(1, AE-23-800-01) kicks it up the tube, where the two balls queue on Ball Trough #1 (17, lower right, nearest the "
			"shooter lane) and #2 (18). The Ball Shooter Lane Feeder (2, the C-9638 Ball Trough Feeder) kicks the lead ball into "
			"the shooter lane. In the power-up probes the ROM retries the outhole kick about every 2.2 s while 16 stays closed; "
			"in the gameplay run it serves a ball with 2 at game start and repeats the serve about every 1.8 s until the "
			"shooter-lane switch (20) closes, and after a drain it kicks the outhole and serves the next ball. The retained script "
			"models the trough as one two-ball cvpmBallStack.",
			*m, assembly="C-9638",
		),
		mechanism(
			"mechanism.shooter-lane-vortex", "Shooter lane and Vortex skill shot", "other", [],
			["switch.matrix-20", "switch.matrix-22", "switch.matrix-23", "switch.matrix-24"],
			"The manual plunger fires the ball from the shooter lane (20) into the \"Vortex\" (ramp B-11152) at the top right, "
			"whose three rollover switches score 20K (22, upper), 100K (23, middle) and 5K (24, lower, the exit) per the "
			"Miscellaneous Parts decals and the switch names; the manual's rules call 5K easy, 20K medium and 100K hard, and "
			"each plunge into the Vortex multiplies the hole values, X1 up to X10 and back to X1. No coil is involved.",
			*m, assembly="B-11152",
		),
		mechanism(
			"mechanism.single-eject", "Single eject hole", "kicker", [output_id(3)], ["switch.matrix-38"],
			"A saucer at the top left. A ball resting on switch 38 (17-1012) is kicked out by the Single Eject Hole coil (3). "
			"Lamps 13-16 advertise its 25K/50K/75K/Extra Ball awards. The ROM kicks it about every 2.1 s while 38 stays closed "
			"(power-up probe), and in play kicks it once the ball rests there.",
			*m,
		),
		mechanism(
			"mechanism.visor", "Motorized visor and teeth targets", "motorized", [output_id(13)],
			["switch.matrix-46", "switch.matrix-47", "switch.matrix-28", "switch.matrix-29", "switch.matrix-30", "switch.matrix-31", "switch.matrix-32"],
			"The robot's visor (C-11159) hinges up to uncover the two eye eject holes. One 11 rpm 24 VAC motor (14-7941), run "
			"by the Visor Motor Relay (13), turns the A-11154 cam that moves both the visor and the Visor Teeth Target Carrier "
			"(B-11156) through a lever arm and connecting link; the carrier holds the five teeth targets 28-32, which stand "
			"in front of the closed visor and drop with it as it opens. The cam's two snap-action limit switches report the "
			"ends of travel: Visor Closed (46) and Visor Open (47). The motor turns one way only, so the relay alone decides "
			"motion. At power-up the ROM runs the motor from about 1.7 s; in the visor probes it stopped the motor when 47 "
			"closed and pulsed the right then the left eye eject (8, 7). With both balls in the trough it restarts the motor "
			"to close the visor and stops it when 46 closes (gameplay-reactive). With 46 or 47 held closed from power-up the "
			"motor ran for the whole 30 s probe, consistent with the ROM acting on the limit switch closing while the motor "
			"runs. Completing the chest opens the visor for multiball. The retained script models a 58-step one-solenoid "
			"cvpmMech with 46 at step 0 and 47 at step 58.",
			*m, assembly="B-11169 with B-11156 and C-11159",
		),
		mechanism(
			"mechanism.eye-ejects", "Left and right eye eject holes", "kicker", [output_id(7), output_id(8)],
			["switch.matrix-25", "switch.matrix-26"],
			"Two saucers behind the visor, the robot's eyes, reachable only while the visor is open: Left Eye Eject (25) with its "
			"coil (7) and Right Eye Eject (26) with its coil (8). Locking a ball in each starts multiball. The ROM does not kick "
			"them while their switches are held at power-up; it kicks both, right then left, when the visor reaches its open "
			"position.",
			*m,
		),
		mechanism(
			"mechanism.lift-ramp", "Lifting ramp", "diverter", [output_id(5), output_id(6)],
			["switch.matrix-44", "switch.matrix-40", "switch.matrix-39"],
			"The B-11304 Ramp Lifting Mechanism raises and lowers the end of the left ramp. Ramp Raise (5, AE-24-900-02) drives "
			"the lift crank through a plunger; Ramp Lower (6, SM-26-600-DC) works the armature and lock crank that let it drop; "
			"the mechanism's microswitch (44, 5647-12001-00) closes when the ramp is down. Shots up the ramp pass Enter Ramp (40) "
			"and Exit Ramp (39), advance the bonus multiplier and build or collect the Solar Value; the manual's rules say \"Hitting "
			"flashing Drop Target raises Ramp and lights target to collect Energy Value\", the target being Score Energy (45) "
			"beside the lifted ramp. At power-up the ROM pulses 5 once, and retries it about "
			"every 1.3 s (four times) while 44 is held closed. At game start it pulses 6, together with 5, about every 1.7 s "
			"until 44 closes (gameplay runs).",
			*m, assembly="B-11304",
		),
		mechanism(
			"mechanism.drop-target-bank", "Left 3-bank drop targets", "drop_target_bank", [output_id(4)],
			["switch.matrix-49", "switch.matrix-50", "switch.matrix-51"],
			"Three drop targets on the left (D-9355), upper 49, middle 50 and lower 51 (17-1042 switches), reset together by "
			"the AE-23-800-04 coil (4). Lamps 41-43 sit in front of them and lamp 17 times them. In play the ROM resets the bank "
			"at game start and, while all three are held down, retries the reset about every 1.25 s; it does not reset them at "
			"power-up.",
			*m, assembly="D-9355",
		),
		mechanism(
			"mechanism.right-5-bank", "Right 5-bank standup targets", "other", [],
			["switch.matrix-33", "switch.matrix-34", "switch.matrix-35", "switch.matrix-36", "switch.matrix-37"],
			"Five standup targets along the chest's right side, 33 at the top to 37 at the bottom (the Switches list gives "
			"A-11317-3 for 34-37; its row 33 is misprinted). Each lights the "
			"chest-panel row it faces, while the five visor teeth targets light the columns.",
			*m,
		),
		mechanism(
			"mechanism.chest-panel", "Chest lamp panel", "other", [], [],
			"A 5 x 5 grid of #555 lamps on the C-11309 Chest Lamp Matrix Board (one diode per lamp) in the robot's chest: "
			"columns Yellow, Blue, Amber, Green, Red (lamps 28-32, 36-40, 44-48, 52-56, 60-64), rows 1 (upper) to 5 (lower). "
			"Teeth targets light it vertically and 5-bank targets horizontally; lighting all five rows opens the visor.",
			MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, assembly="C-11309",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three jet bumpers", "other", [output_id(17), output_id(19), output_id(22)],
			["switch.matrix-53", "switch.matrix-48", "switch.matrix-52"],
			"Three B-9414 jet bumpers with B-9415 coils on the right: Upper (22, switch 52), Left (19, switch 48) and Lower "
			"(17, switch 53). Each is a special solenoid that pbGameData's sxx.ssSw fires from its own switch, and each hit "
			"also flashes the Energy flashers (30) and adds Energy value. The #44 bulbs in the caps are playfield G.I.",
			*m, assembly="B-9414 with B-9415",
		),
		mechanism(
			"mechanism.slingshots", "Left and right kickers", "other", [output_id(20), output_id(21)], ["switch.matrix-54", "switch.matrix-55"],
			"Two slingshot kickers above the flippers. Each has a scoring switch the CPU reads (54 left, 55 right, SW-1A-122) "
			"and a kicker actuating switch that fires the coil itself; solenoids 20 and 21 are special solenoids whose ssSw "
			"entries are 54 and 55.",
			*m,
		),
		mechanism(
			"mechanism.flippers", "Two flippers, cabinet-wired", "other", [], ["switch.matrix-10", "switch.matrix-11"],
			"Two FL-23/600-30/2600 flippers (C-9952-R and -L). The cabinet buttons fire the coils through the switched-solenoid "
			"supply, so no Sol. No. or driver is printed for them and PinMAME fabricates 45-48 from the buttons at public 82 "
			"and 84. Each flipper base carries a Lane Change switch the CPU reads (10 left, 11 right), which core_updateSw "
			"copies from 84 and 82, and an End of Stroke switch (03-7811) in the coil circuit with no matrix address.",
			*m, assembly="C-9952-R with C-9952-L",
		),
		mechanism(
			"mechanism.standup-targets", "Advance Planet and Score Energy targets", "other", [], ["switch.matrix-19", "switch.matrix-45"],
			"Two single standup targets: Advance Planet (19, A-11055) on the right advances the planet ladder (lamps 19-27), and "
			"Score Energy (45, A-11054) at the top left collects the Energy value.",
			*m,
		),
		mechanism(
			"mechanism.ten-point-rubbers", "Ten-point rubber switches", "other", [], ["switch.matrix-56", "switch.matrix-59", "switch.matrix-60"],
			"Three SW-1A-120 switches behind rubbers that score 10 points: left side (56), right side above the Advance Planet "
			"target (59) and upper left beside the ramp (60).",
			*m,
		),
		mechanism(
			"mechanism.ac-select", "A/C solenoid select relay", "other", [output_id(14)], [],
			"The Solenoid Select Relay (14) switches the solenoid B+ between two busses so that each of the eight switched drivers "
			"(Q22-Q25, Q30-Q33) serves an \"A\" load while it is released and a \"C\" load while it is energized, through the "
			"Diode Switching Board. Pinned PinMAME publishes the C loads separately at 25-32, so a consumer reads them directly; "
			"the relay's own state is published at 14.",
			MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other", [output_id(25)], [],
			"The C-side load of pair 01 (25, AE-23-800-02) raps the B-10686 Knocker Assembly in the backbox for replays and "
			"specials.",
			MANUAL_SOURCE, ROM_SOURCE, RUNTIME_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": f"relationship.special-solenoid-{solenoid}", "kind": "direct", "source": f"switch.matrix-{switch}",
			"destination": output_id(solenoid), "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE, RUNTIME_SOURCE),
		}
		for solenoid, switch in sorted(SPECIAL_SOLENOID_SWITCH.items()) if switch
	] + flipper_column_relationships(flip_swno=FLIP_SWNO, matrix_ids={10: "switch.matrix-10", 11: "switch.matrix-11"}, refs=(CORE_SOURCE, RUNTIME_SOURCE))


def drivers() -> list[dict[str, Any]]:
	catalog = load_json(ROOT / "catalog/pinmame.json")
	by_id = {record["id"]: record for record in catalog["drivers"]}
	items = []
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


COVERAGE_MISSING = ["spatial_placement"]


def build_base() -> dict[str, Any]:
	definition = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID, "name": "Pinbot", "manufacturer": "Williams", "year": 1986, "kind": "physical_pinball",
			"ipdb_id": 1796, "opdb_id": "G41Z8-MJKvP",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": STATUS,
			"missing": COVERAGE_MISSING,
			"dimensions": {
				"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
				"physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated",
				"recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed",
			},
		},
		"controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": [],
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Pin-Bot device identifiers are not unique: {duplicates}")
	return definition


def build() -> tuple[dict[str, Any], dict[str, Any]]:
	definition = build_base()
	seed = json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8"))
	decisions = drawing_callouts.apply_to_definition(definition, seed, CALLOUT_SOURCE)
	return definition, decisions


def build_spatial_report(definition: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
	located_inputs, located_outputs, omitted = [], [], []
	na_inputs: dict[str, list[int]] = {}
	na_outputs: dict[str, list[dict[str, Any]]] = {}
	statuses: dict[str, int] = {}
	placement_count = 0
	for device in definition["inputs"]:
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			na_inputs.setdefault(spatial["reason"], []).append(device["binding"]["device"])
		else:
			located_inputs.append(device["binding"]["device"])
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": device["binding"]["device"]}
		spatial = device.get("spatial")
		if spatial is None:
			omitted.append(binding)
		elif spatial["status"] == "not_applicable":
			na_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			located_outputs.append(binding)
			for item in spatial["placements"]:
				placement_count += 1
				statuses[item["provenance"]["status"]] = statuses.get(item["provenance"]["status"], 0) + 1
	unvalidated = sorted(
		item["id"] for collection in ("inputs", "outputs") for device in definition[collection]
		for item in (device.get("spatial") or {}).get("placements", []) if item["provenance"]["status"] != "validated"
	)
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": MACHINE_ID,
		"status": "validated",
		"blockers": [
			"Solenoids 10 and 18 (Right and Left Visor G.I.) are #1251 flash lamps that light the visor, but neither the "
			"manual nor the retained table gives their sockets a position: the locations drawings mark no visor lamp, and the "
			"table lights one Flasher sprite between the eyes for both. Their spatial keys are omitted.",
			"Switch 40 (Enter Ramp): the retained table's trigger sits about 0.075 normalized from where the switch drawing's "
			"leader 40 ends further down the same ramp curve, beyond the 0.07 callout limit, so its placement stays observed.",
			"Solenoid 12 (Playfield G.I. Relay): the 27 placements are the sockets of the retained table's GI collection. The "
			"manual prints no G.I. bulb count or layout and a table's grouping is not the machine's wiring, so they stay "
			"observed without a quantity.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": "x/952; 0=left, 1=right",
			"y": "y/1974; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {"fail_closed": True, "file_count": EXTRACTION_FILE_COUNT, "source_ref": VPX_EXTRACTION_SOURCE},
		"source_hashes": {"embedded_script_sha256": SCRIPT_SHA256, "manual_sha256": MANUAL_SHA256, "table_sha256": TABLE_SHA256},
		"placement_count": placement_count,
		"placement_status_counts": dict(sorted(statuses.items())),
		"unvalidated_placements": unvalidated,
		"resolved_input_addresses": sorted(located_inputs),
		"resolved_output_bindings": sorted(located_outputs, key=lambda item: (item["group"], item["address"])),
		"not_applicable_inputs": {reason: sorted(values) for reason, values in sorted(na_inputs.items())},
		"not_applicable_outputs": {reason: sorted(values, key=lambda item: (item["group"], item["address"])) for reason, values in sorted(na_outputs.items())},
		"omitted_outputs": sorted(omitted, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, (_, reason) in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": f"Projected onto {reason}."} for address, reason in sorted(SOLENOID_PROJECTED.items())]
		),
		"callout_check": drawing_callouts.summary(
			json.loads(CALLOUT_SEED_PATH.read_text(encoding="utf-8")), decisions,
			CALLOUT_SEED_PATH.relative_to(ROOT).as_posix(), _file_sha256(CALLOUT_SEED_PATH),
		),
		"excluded_object_classes": [
			"lNa and lNz Light objects: glow companions of each script-bound insert light lN",
			"GIn Light objects: the non-bulb-mesh half of each GI socket pair, at the same socket as LightN (Light5/Light6 sit on GI6/GI5)",
			"Flasher sprites (Flasher2TL*, Flasher2TR*, Flasher1L*, Flasher1R*, Flasher2L*, BumpFlash, FlasherB, Flash101, Flash104, f49, f57, shadowson, shadowsoff): glow and shadow overlays",
			"combo HitTargets sw2829-sw3637 and combo walls sw4950/sw5051: table helpers that report two switches at once",
			"WallLccc: a second rubber the script also binds to switch 60",
			"350 unreferenced display-segment Flashers (ax*, led*), backglass flashers, LeafSwitch1-7 visuals",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	check = report["callout_check"]
	lines = [
		"# Pin-Bot (Williams, 1986) spatial review",
		"",
		f"Status: {report['status']}. The machine record stays `partial` at `machines/partial/williams/pinbot-1986.json` "
		f"because of the {len(report['blockers'])} spatial blockers below.",
		"",
		f"The geometry source is the retained known-working `PinBot (Williams 1986).vpx` by bord (v1.1), SHA-256 `{TABLE_SHA256}`, "
		f"whose embedded script (SHA-256 `{SCRIPT_SHA256}`) is the binding authority. Bounds are `{TABLE_BOUNDS}`; every "
		"coordinate is x/952 and y/1974, rounded to at most six places.",
		"",
		"## Evidence decisions",
		"",
		"- A placement is the centre of the table object the script binds to the address: a trigger, target, kicker or bumper "
		"for a switch, the `lN` insert light of each lamp's FadeLights triple, the modelled flasher dome or script-driven Light "
		"for a flasher, and the bulb-mesh `LightN` of each GI socket pair.",
		f"- {check['validated']} of the {check['checked']} table placements the manual's numbered drawings check land within 0.07 "
		"normalized of their own callout under both fits (rule below) and are validated; the others keep the table's `observed` "
		"status.",
		"- Sensors and coils with no table object of their own (the lane-change, outhole, trough, ramp-down and visor limit "
		"switches, and the outhole, trough-feeder, drop-reset, ramp and visor drives) are documented projections onto their own "
		"mechanism's object and are not checked against the drawings.",
		"- Flashers have no factory drawing; their placements are the table's modelled domes or lights, bound by the script "
		"and matching the manual's location wording. Playfield G.I. sockets come from the table's GI collection and stay "
		"`observed`.",
		"- Backbox and cabinet devices take controlled `not_applicable` records: lamps 1-8, the robot-face, insert-board and "
		"top backbox flashers, the backbox G.I. relay, the knocker, the cabinet and diagnostic switches, the Country jumper "
		"and all eight display positions.",
		"",
		"## Callout check",
		"",
		f"Rule: {check['rule']}",
		"",
	]
	for key, page in check["pages"].items():
		lines.append(
			f"- {key} ({page['locator']}): {page['controls']} controls, control RMS {page['control_rms']}, control leave-one-out max "
			f"{page['control_loo_max']}; {page['callout_pairs']} callout pairs, {page['callout_fit_pairs']} in the callout fit, "
			f"leave-one-out max {page['callout_loo_max']}."
		)
	lines += ["", f"Checked {check['checked']}, validated {check['validated']}."]
	if check["not_validated"]:
		lines += ["", "Not validated by the check:", ""]
		for pid, item in check["not_validated"].items():
			lines.append(f"- `{pid}`: " + ", ".join(f"{k} {v}" for k, v in item.items()))
	lines += ["", "## Explicit projections", ""]
	for entry in report["projections"]:
		short = "Switch" if entry["group"] == "pinmame.input.switch" else "Solenoid"
		lines.append(f"- {short} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']} ({', '.join(f'{k} {v}' for k, v in report['placement_status_counts'].items())})",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with an omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, values in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(values)}")
	for reason, values in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(values)}")
	lines += ["", "## Blockers", ""] + [f"- {blocker}" for blocker in report["blockers"]]
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated with a semantic disposition, every printed wiring detail is recorded, the "
		"mechanisms are covered, and polarity is settled by the ROM's Switch Levels test. Promotion to `author_ready` is "
		"refused because two visor G.I. outputs have no placement, the playfield G.I. placements come only from the table's "
		"grouping and one switch placement is not validated, so `coverage.missing` is `[\"spatial_placement\"]`. A "
		"photograph or drawing of the visor lamp sockets, a G.I. lamp layout from the machine, and a second, independent "
		"recreation or measurement of the ramp-entrance switch would close them.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition, decisions = build()
	stale = root / STALE_DEFINITION_PATH.relative_to(ROOT)
	if stale.exists():
		stale.unlink()
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition, decisions)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if (root / STALE_DEFINITION_PATH.relative_to(ROOT)).exists():
		raise RuntimeError(f"Pin-Bot is recorded {STATUS} but a stale artifact exists at {STALE_DEFINITION_PATH}")
	definition, decisions = build()
	expected = canonical_bytes(definition)
	if not definition_path.is_file() or definition_path.read_bytes() != expected:
		raise RuntimeError(f"Pin-Bot definition drifted from its deterministic curator: {definition_path}")
	if not seed_path.is_file() or seed_path.read_bytes() != expected:
		raise RuntimeError(f"Pin-Bot seed is not byte-identical to the definition: {seed_path}")
	report = build_spatial_report(definition, decisions)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Pin-Bot spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Pin-Bot spatial review drifted from its deterministic curator: {markdown_path}")
	print("Pin-Bot definition, seed, and spatial audit match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator, the definition, and the pinned seed")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, the pinned seed and the spatial report")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
	mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest")
	args = parser.parse_args()
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"Pin-Bot extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Pin-Bot retained extraction matches its pinned manifest.")
	elif args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
