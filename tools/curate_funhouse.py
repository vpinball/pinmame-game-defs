"""Curate the physical Williams FunHouse (1990) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses drift,
and ``--regenerate`` is the only path that writes the canonical definition and its pinned seed.

Note on directory naming: the seeding task brief for this game named the target paths
``machines/<state>/bally/`` and ``tools/seeds/bally/funhouse.json``. FunHouse is unambiguously a
Williams machine (pinned ``CORE_GAMEDEF(fh,l9,...,"Williams",...)`` in ``fh.c``), and every other
path this task specifies (``knowledge/williams/``, ``reports/spatial/williams/``) already uses
the correct manufacturer, so "bally" is treated as a template artifact carried over from a
different game's brief -- the same class of deviation recorded for Stern The Simpsons Pinball
Party. This curator writes under ``machines/<state>/williams/`` and ``tools/seeds/williams/``.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/williams/funhouse-1990.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/funhouse-1990.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/williams/funhouse-1990.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/funhouse-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/funhouse-1990.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-alpha"
MANUAL_SOURCE = "manual.williams.funhouse.1990"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.funhouse.1990"
VPX_TABLE_SOURCE = "vpx-table.fh-1-3"
VPX_SCRIPT_SOURCE = "vpx-script.fh-1-3"
VPX_EXTRACTION_SOURCE = "vpx-extraction.fh-1-3"

TABLE_SHA256 = "69c37fa9a84e669a2934d6da0e5ee0277c4a0ef01e71eaa19e7271ba3396873e"
SCRIPT_SHA256 = "322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863"
MANUAL_SHA256 = "b658e7d0985a5e8588981c974d9c9448ea7cc574b2d21e5acb386c718a1f0f47"

EXTRACTION_RELATIVE_PATH = Path("williams/funhouse-1990/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/funhouse-1990/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "85620e05458bd72bc57c2e203001a0f35db9806431e66e07ee08f05e90346ba9"
EXTRACTION_FILE_COUNT = 2212
EXTRACTION_TOTAL_BYTES = 219908807

TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"

# --- Driver tree -----------------------------------------------------------------------------
DRIVER_IDS = (
	"fh_l9", "fh_d9", "fh_l9b", "fh_d9b", "fh_905h", "fh_906h", "fh_907h", "fh_pa1",
	"fh_l2", "fh_l3", "fh_d3", "fh_l4", "fh_d4", "fh_l5", "fh_d5", "fh_f91",
)
DRIVER_COMPATIBILITY = {
	"fh_l9": ("identical", "Williams production L-9 game ROM (sound level SL-3) shipped with the physical machine; the switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are the reference for this definition."),
	"fh_d9": ("identical", "D-9 game ROM; an LED ghost-fix revision of L-9 with no controller-address or playfield change."),
	"fh_l9b": ("identical", "L-9 with an unofficial improved German translation MOD; no controller-address or playfield change."),
	"fh_d9b": ("identical", "D-9 with the same unofficial improved German translation MOD and LED ghost fix; no controller-address or playfield change."),
	"fh_905h": ("identical", "9.05H game ROM. This is the driver the retained known-working script binds to (Const cGameName=\"fh_905h\"); it drives the identical I/O inventory as L-9."),
	"fh_906h": ("identical", "9.06H Coin Play game ROM; a later firmware revision of the same physical machine with no controller-address or playfield change."),
	"fh_907h": ("identical", "9.07H LED ghost fix plus ball-saver MOD, a community patch of 9.05H; no controller-address or playfield change."),
	"fh_pa1": ("compatible", "Prototype PA-1 game ROM (labeled L-2, System 11 sound). Pinned PinMAME binds it to a distinct GEN_WPCALPHA_1 core_tGameData (fhpa1GameData) rather than the production fhGameData, reflecting the earlier WPC-Alpha-1/System-11 sound-board generation used before the machine's WPC-Alpha-2 sound board shipped. The switch, solenoid, lamp, and mechanism definitions transcribed here are unchanged between the two structs (fhpa1GameData copies fhGameData's flipper/mech/lamp-display fields and inverted-switch mask verbatim), so this remains the same physical playfield with an earlier sound subsystem, not a different machine."),
	"fh_l2": ("identical", "L-2 game ROM, the earliest production-generation firmware retained by PinMAME; no controller-address or playfield change from L-9."),
	"fh_l3": ("identical", "L-3 game ROM; no controller-address or playfield change."),
	"fh_d3": ("identical", "D-3 game ROM, an LED ghost-fix revision of L-3; no controller-address or playfield change."),
	"fh_l4": ("identical", "L-4 game ROM; no controller-address or playfield change."),
	"fh_d4": ("identical", "D-4 game ROM, an LED ghost-fix revision of L-4; no controller-address or playfield change."),
	"fh_l5": ("identical", "L-5 game ROM; no controller-address or playfield change."),
	"fh_d5": ("identical", "D-5 game ROM, an LED ghost-fix revision of L-5; no controller-address or playfield change."),
	"fh_f91": ("identical", "FreeWPC 0.91 community firmware for the same physical hardware; no controller-address or playfield change asserted by the pinned driver record."),
}

# --- Printed switch tables (manual pages 2-38 locations, 2-39 wiring/matrix) ------------------
SWITCH_LABELS = {
	11: "Right Flipper", 12: "Left Flipper", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Steps Lights Frenzy", 16: "Upper Ramp Switch", 17: 'S-T-E-P "S"', 18: "Left Jet Bumper",
	21: "Slam Tilt", 22: "Front Door", 24: "Test Position (Always Closed)",
	25: "Lock Mech Right", 26: "Steps Lights Ex. Ball", 27: "Lock Mech Center", 28: "Lock Mech Left",
	31: 'S-T-E-P "P"', 32: "Top Superdog Standup Target", 33: "Lt. Gangway Rollunder",
	34: "Bottom Superdog Standup Target", 35: "Steps Track Lower", 36: "Steps 500,000",
	37: "Center Superdog Standup Target", 38: "Steps Track Upper",
	41: "Left Slingshot", 42: "Lt. Flipper Return Lane", 43: "Left Outlane",
	44: "Wind Tunnel Hole", 45: "Trap Door Open", 46: "Rudy Hideout Kickbig",
	47: "Left Ballshooter", 48: "Ramp Exit Track",
	51: "Dummy Jaw", 52: "Right Outlane", 53: "Right Slingshot", 54: 'S-T-E-P "T"',
	55: "Steps Superdog", 56: "Ramp Entrance", 57: "Jet Bumper Lane", 58: "Tunnel Kickout",
	61: "Rt. Inside Return Lane", 62: "Right Ballshooter", 63: "Right Trough", 64: 'S-T-E-P "E"',
	65: "Dummy Eject Hole", 66: "Right Gangway Lane", 67: "Lower Right Drop Hole", 68: "Lower Jet Bumper",
	71: "Rt. Outside Return Lane", 72: "Left Trough", 73: "Outhole", 74: "Center Trough",
	75: "Upper Right Loop", 76: "Trap Door Closed", 77: "Right Jet Bumper",
}
# 78, 81-88 are all printed "Not Used"; 23 (Ticket Dispenser) is separately printed "Not Used".
UNUSED_MATRIX_ADDRESSES = {23, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# The only two switches this manual marks "(opto)" anywhere -- neither the switch-locations page
# nor the switch-matrix page shades any cell for opto construction on this machine.
OPTO_SWITCHES = {51, 55}
SWITCH_PARTS = {
	11: "A-9990-1", 12: "A9989-1", 13: "20-9663-1", 14: "20-6502-A", 15: "5647-12073-21",
	16: "5647-12073-21", 17: "B-12001-1", 18: "B-12030-2",
	21: "27-1066", 22: "A-8630", 24: "A-8630",
	25: "A-14138", 26: "5647-12073-21", 27: "A-14138", 28: "A-14138",
	31: "B-12001-1", 32: "B-12001-4", 33: "A-12010", 34: "B-12001-4", 35: "5647-12073-21",
	36: "5647-12073-21", 37: "B-12001-4", 38: "5647-12073-21",
	41: "A-4834-H", 42: "A-12688", 43: "A-12688", 44: "A-12238", 45: "A-12238",
	46: "A-11608", 47: "A-11619-1", 48: "5647-12073-21",
	51: "A-13901", 52: "A-12688", 53: "A-4843-H", 54: "B-12583-1", 55: "A-13901",
	56: "5647-12073-21", 57: "A-12688", 58: "5647-12073-25",
	61: "A-12688", 62: "A-11619", 63: "p/o B-8925", 64: "B-12583-1", 65: "5647-12073-43",
	66: "A-12688", 67: "A-12238", 68: "B-12030-2",
	71: "A-12688", 72: "A-11680", 73: "A-10417", 74: "p/o B-8925", 75: "A-12688",
	76: "5647-12001-00", 77: "B-12030-2",
}
SWITCH_TYPES = {
	11: "leaf", 12: "leaf", 13: "button", 14: "tilt", 15: "microswitch", 16: "microswitch",
	17: "microswitch", 18: "other", 21: "leaf", 22: "microswitch", 24: "other",
	25: "microswitch", 26: "microswitch", 27: "microswitch", 28: "microswitch",
	31: "microswitch", 32: "microswitch", 33: "microswitch", 34: "microswitch",
	35: "microswitch", 36: "microswitch", 37: "microswitch", 38: "microswitch",
	41: "leaf", 42: "microswitch", 43: "microswitch", 44: "microswitch", 45: "microswitch",
	46: "microswitch", 47: "microswitch", 48: "microswitch",
	51: "opto", 52: "microswitch", 53: "leaf", 54: "microswitch", 55: "opto",
	56: "microswitch", 57: "microswitch", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch",
	65: "microswitch", 66: "microswitch", 67: "microswitch", 68: "other",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "microswitch",
	75: "microswitch", 76: "microswitch", 77: "other",
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
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J207-1", "U20-18"), 2: ("Green-Red", "J207-2", "U20-17"),
	3: ("Green-Orange", "J207-3", "U20-16"), 4: ("Green-Yellow", "J207-4", "U20-15"),
	5: ("Green-Black", "J207-5", "U20-14"), 6: ("Green-Blue", "J207-6", "U20-13"),
	7: ("Green-Violet", "J207-7", "U20-12"), 8: ("Green-Gray", "J207-8", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J209-1", "U18-11"), 2: ("White-Red", "J209-2", "U18-9"),
	3: ("White-Orange", "J209-3", "U18-5"), 4: ("White-Yellow", "J209-4", "U18-7"),
	5: ("White-Green", "J209-5", "U19-11"), 6: ("White-Blue", "J209-7", "U19-9"),
	7: ("White-Violet", "J209-8", "U19-5"), 8: ("White-Gray", "J209-9", "U19-7"),
}

# --- Printed solenoid/GI table (manual page 2-40) ---------------------------------------------
SOLENOID_LABELS = {
	1: "Outhole", 2: "Ramp Diverter", 3: "Kickbig", 4: "Tunnel Kickbig",
	5: "Trap Door Open", 6: "Trap Door Closed", 7: "Knocker", 8: "Multi-ball Release",
	9: "Left Jet Bumper", 10: "Right Jet Bumper", 11: "Lower Jet Bumper",
	12: "Left Slingshot", 13: "Right Slingshot", 14: "Steps Gate", 15: "Trough",
	16: "Dummy Eject Hole", 17: "3 Blue Flashers", 18: "Dummy Flashers", 19: "2 Clock Flashers",
	20: "2 Superdog Flashers", 21: "Mouth Motor", 22: "Up/Down Driver", 23: "3 Red Flashers",
	24: "3 Clear Flashers", 25: "Eyes Right", 26: "Eyelids Open", 27: "Eyelids Close", 28: "Eyes Left",
}
SOLENOID_PARTS = {
	1: "AE-26-1200", 2: "AE-26-1200", 3: "AE-26-1500", 4: "AE-26-1200", 5: "AE-26-1500",
	6: "SM1-26-600", 7: "AE-23-800", 8: "A-14189", 9: "AE-26-1200", 10: "AE-26-1200",
	11: "AE-26-1200", 12: "AE-26-1500", 13: "AE-26-1500", 14: "SZ-34-3500", 15: "AE-26-1200",
	16: "AE-26-1500", 17: "#906", 18: "#906", 19: "#906", 20: "#906", 21: "A-13997",
	22: "C-13963", 23: "#906", 24: "#906", 25: "SM-30-1100", 26: "SM-30-1100",
	27: "SM-30-1100", 28: "SM-30-1100",
}
FLASHER_QUANTITIES = {17: 3, 18: 1, 19: 2, 20: 2, 23: 3, 24: 3}
SOLENOID_WIRING = {
	1: dict(control_connection="J130-1", driver_transistor="Q82", printed_type="High Power"),
	2: dict(control_connection="J130-2", driver_transistor="Q80", printed_type="High Power"),
	3: dict(control_connection="J130-4", driver_transistor="Q78", printed_type="High Power"),
	4: dict(control_connection="J130-5", driver_transistor="Q76", printed_type="High Power"),
	5: dict(control_connection="J130-6", driver_transistor="Q64", printed_type="High Power"),
	6: dict(control_connection="J130-7", driver_transistor="Q66", printed_type="High Power"),
	7: dict(control_connection="J130-8", driver_transistor="Q68", printed_type="High Power"),
	8: dict(control_connection="J130-9", driver_transistor="Q70", printed_type="High Power"),
	9: dict(control_connection="J127-1", driver_transistor="Q58", printed_type="Low Power"),
	10: dict(control_connection="J127-2", driver_transistor="Q56", printed_type="Low Power"),
	11: dict(control_connection="J127-4", driver_transistor="Q54", printed_type="Low Power"),
	12: dict(control_connection="J127-5", driver_transistor="Q52", printed_type="Low Power"),
	13: dict(control_connection="J127-6", driver_transistor="Q50", printed_type="Low Power"),
	14: dict(control_connection="J127-7", driver_transistor="Q48", printed_type="Low Power"),
	15: dict(control_connection="J127-8", driver_transistor="Q46", printed_type="Low Power"),
	16: dict(control_connection="J127-9", driver_transistor="Q44", printed_type="Low Power"),
}
# Retained VPW-style script callbacks (SolCallback array), per solenoid address.
SOLENOID_CALLBACKS = {
	1: "kisort (Outhole)", 2: "SolRampDiverter", 3: "bsHideout.SolOut", 4: "SolKickout",
	5: "SolTrapDoorO", 6: "SolTrapDoorC", 7: 'vpmSolSound SoundFX("fx_knocker",DOFKnocker)',
	8: "MBRelease", 14: "SolFlipperDiverter", 15: "KickBallToLane", 16: "bsRudy.SolOut",
	17: "SetBlueDome", 18: "setlamp 118,", 19: "setlamp 119,", 20: "setlamp 120,",
	23: "SetRedDome", 24: "SetWhiteDome", 25: "SolEyesRight", 26: "SolEyesOpen",
	27: "SolEyesClosed", 28: "SolEyesLeft",
}

# --- Printed general-illumination table (manual page 2-40) ------------------------------------
GI_LABELS = {
	0: "Upper Backglass G.I.", 1: "Front Playfield G.I.", 2: "Rear Playfield G.I.",
	3: "Cntr Bckglss/Rt. Rr Plfld G.I.", 4: "Top Playfield G.I.",
}
GI_SCRIPT_REGIONS = {
	0: "Upper BackGlass (Case 0)", 1: "Rudy (Case 1)", 2: "Upper Playfield (Case 2)",
	3: "Center BackGlass (Case 3)", 4: "Lower Playfield (Case 4)",
}
GI_FEED_WIRING = {
	0: dict(control_connection="J120-5", driver_transistor="Q12", insert_connection="J121-5"),
	1: dict(control_connection="J120-6", driver_transistor="Q10", insert_connection="J121-6", cabinet_connection="J119-3"),
	2: dict(control_connection="J120-1", driver_transistor="Q18", insert_connection="J121-1"),
	3: dict(control_connection="J120-3", driver_transistor="Q14", insert_connection="J121-3"),
	4: dict(control_connection="J120-2", driver_transistor="Q16", insert_connection="J121-2"),
}

# --- Printed lamp table (manual pages 2-36 locations, 2-37 wiring) ----------------------------
LAMP_LABELS = {
	11: "Gangway 75,000", 12: "Gangway 100,000", 13: "Gangway 150,000", 14: "Gangway 200,000",
	15: "Gangway 250,000", 16: "Gangway Lights Extra Ball", 17: "Shoot Again", 18: "Steps Open (Gate)",
	21: "Clock 45 Minutes", 22: "Clock 8 O'Clock", 23: "Clock 6 O'Clock", 24: "Clock 25 Minutes",
	25: "Clock 15 Minutes", 26: "Clock 10 Minutes", 27: "Clock 12 Minutes", 28: "Clock 0 Minutes",
	31: "Clock 40 Minutes", 32: "Clock 35 Minutes", 33: "Clock 30 Minutes", 34: "Clock 20 Minutes",
	35: "Clock 3 O'Clock", 36: "Clock 1 O'Clock", 37: "Clock 11 O'Clock", 38: "Clock 50 Minutes",
	41: "Clock 9 O'Clock", 42: "Clock 7 O'Clock", 43: "Clock 5 O'Clock", 44: "Clock 4 O'Clock",
	45: "Clock 2 O'Clock", 46: "Clock 5 Minutes", 47: "Clock 55 Minutes", 48: "Clock 10 O'Clock",
	51: "Lower Jet Bumper", 52: "Upper Jet Bumper", 53: "Superdog Lamp", 54: "Steps Lights Frenzy",
	55: "Steps Lights Ex. Ball", 56: "Steps 500,000", 57: "Ramp Overhead Lamp",
	58: "Rt. Gangway Overhead Lamp", 61: "Rt. Flipper Lanes", 62: 'S-T-E-P "S"',
	63: "Trap Door Bonus", 64: "Ramp Scores 250,000", 65: 'S-T-E-P "T"', 66: "Upper Lt. Gangway Lane",
	67: "Extra Ball Lamp", 68: "Lock", 71: "Magic Mirror Lights Ex. Ball", 72: "Upper Rt. Jet Bumper",
	73: 'S-T-E-P "P"', 74: "Magic Mirror Lights Million", 75: "Magic Mirror Lights Jet Bumper",
	76: "Magic Mirror Lights Superdog", 77: "Magic Mirror Opens Gate",
	78: "Magic Mirror Lights Quick Multi-ball", 81: "Million Plus", 82: "Special Outlanes",
	83: "Trap Door Frenzy", 84: 'Ramp "Steps" Lamp', 85: "Magic Mirror Arrow", 86: 'S-T-E-P "E"',
	87: "Million", 88: "Start Button",
}
LAMP_BULBS = {addr: ("#44" if addr in {17, 53, 57, 58, 61, 62, 65, 66, 73, 82, 85, 86, 87} else "#555") for addr in LAMP_LABELS}
LAMP_QUANTITIES = {53: 2, 61: 2, 82: 2}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J138-1", "Q98"), 2: ("Yellow-Red", "J138-2", "Q97"),
	3: ("Yellow-Orange", "J138-3", "Q96"), 4: ("Yellow-Black", "J138-4", "Q95"),
	5: ("Yellow-Green", "J138-5", "Q94"), 6: ("Yellow-Blue", "J138-6", "Q93"),
	7: ("Yellow-Violet", "J138-7", "Q92"), 8: ("Yellow-Gray", "J138-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J133-1", "Q90"), 2: ("Red-Black", "J133-2", "Q89"),
	3: ("Red-Orange", "J133-3", "Q88"), 4: ("Red-Yellow", "J133-5", "Q87"),
	5: ("Red-Green", "J133-6", "Q86"), 6: ("Red-Blue", "J133-7", "Q85"),
	7: ("Red-Violet", "J133-8", "Q84"), 8: ("Red-Gray", "J133-9", "Q83"),
}

# --- Normalized playfield coordinates from the retained VPX extraction (x/964, y/2162) --------
SWITCH_POSITIONS = {
	11: [(0.60409, 0.842652)], 12: [(0.264227, 0.842652)], 15: [(0.145448, 0.30695)],
	16: [(0.687465, 0.112309)], 17: [(0.15384, 0.596574)], 18: [(0.615994, 0.443693)],
	25: [(0.288262, 0.135109)], 26: [(0.145027, 0.263304)], 27: [(0.239196, 0.147339)],
	28: [(0.193812, 0.158922)], 31: [(0.554663, 0.521479)], 32: [(0.512372, 0.454203)],
	33: [(0.158116, 0.067089)], 34: [(0.528313, 0.504013)], 35: [(0.140276, 0.628762)],
	36: [(0.146513, 0.217511)], 37: [(0.520533, 0.479226)], 38: [(0.761925, 0.390557)],
	41: [(0.211364, 0.738475)], 42: [(0.131072, 0.7303)], 43: [(0.054941, 0.715251)],
	44: [(0.374725, 0.280513)], 45: [(0.711618, 0.346901)], 46: [(0.78147, 0.13193)],
	47: [(0.059097, 0.89204)], 48: [(0.831538, 0.427095)], 51: [(0.630723, 0.273491)],
	52: [(0.875051, 0.75622)], 53: [(0.657699, 0.73899)], 54: [(0.209337, 0.383022)],
	55: [(0.400243, 0.157399)], 56: [(0.262034, 0.325482)], 57: [(0.859425, 0.623967)],
	58: [(0.732298, 0.567893)], 61: [(0.73663, 0.720266)], 62: [(0.943105, 0.888831)],
	64: [(0.33837, 0.348324)], 65: [(0.660429, 0.20844)], 66: [(0.93145, 0.187398)],
	67: [(0.820074, 0.578718)], 68: [(0.764603, 0.518256)], 71: [(0.804597, 0.71963)],
	72: [(0.769422, 0.891111)], 74: [(0.824195, 0.877197)], 75: [(0.849795, 0.10813)],
	76: [(0.81201, 0.238809)], 77: [(0.843763, 0.431839)],
	73: [(0.500721, 0.960313)],
}
# Switches with no dedicated VPX trigger/target object found in the retained extraction.
SWITCH_SPATIAL_UNRESOLVED = {63}

SOLENOID_POSITIONS = {
	1: [(0.500721, 0.960313)], 2: [(0.900092, 0.335841)], 3: [(0.78147, 0.13193)],
	4: [(0.693624, 0.61287)], 5: [(0.81201, 0.238809)], 6: [(0.81201, 0.238809)],
	8: [(0.433493, 0.564827)], 9: [(0.615994, 0.443693)], 10: [(0.843763, 0.431839)],
	11: [(0.764603, 0.518256)], 12: [(0.211364, 0.738475)], 13: [(0.657699, 0.73899)],
	14: [(0.100533, 0.84034)], 15: [(0.877269, 0.863859)], 16: [(0.660429, 0.20844)],
	17: [(0.607818, 0.066095)], 18: [(0.585264, 0.326788)], 19: [(0.434362, 0.658164)],
	20: [(0.446452, 0.46247)], 23: [(0.766934, 0.087572)], 24: [(0.929512, 0.109304)],
	21: [(0.630723, 0.273491)], 22: [(0.630723, 0.273491)],
	25: [(0.630723, 0.273491)], 26: [(0.630723, 0.273491)],
	27: [(0.630723, 0.273491)], 28: [(0.630723, 0.273491)],
}

LAMP_POSITIONS = {
	11: [(0.277891, 0.790845)], 12: [(0.333362, 0.807742)], 13: [(0.402002, 0.816214)],
	14: [(0.466973, 0.815765)], 15: [(0.532204, 0.80782)], 16: [(0.588464, 0.791557)],
	17: [(0.433283, 0.874712)], 18: [(0.054838, 0.789026)], 21: [(0.278513, 0.657338)],
	22: [(0.359429, 0.676949)], 23: [(0.434301, 0.69581)], 24: [(0.510799, 0.716611)],
	25: [(0.58777, 0.658429)], 26: [(0.568217, 0.624502)], 27: [(0.43313, 0.609972)],
	28: [(0.433493, 0.564827)], 31: [(0.299, 0.691676)], 32: [(0.356261, 0.71648)],
	33: [(0.432843, 0.725435)], 34: [(0.567373, 0.692154)], 35: [(0.519884, 0.657824)],
	36: [(0.476797, 0.625099)], 37: [(0.390122, 0.625103)], 38: [(0.299934, 0.623783)],
	41: [(0.347821, 0.657825)], 42: [(0.390515, 0.690546)], 43: [(0.476207, 0.690458)],
	44: [(0.509063, 0.676773)], 45: [(0.508473, 0.638964)], 46: [(0.511423, 0.59882)],
	47: [(0.356393, 0.598672)], 48: [(0.359823, 0.638964)], 51: [(0.765445, 0.51738)],
	52: [(0.61674, 0.442817)], 57: [(0.264182, 0.328014)], 58: [(0.665193, 0.541238)],
	53: [(0.453204, 0.476406), (0.459149, 0.498521)],
	61: [(0.129717, 0.690238), (0.735779, 0.675768)], 62: [(0.185918, 0.623502)],
	63: [(0.437713, 0.41654)], 64: [(0.283597, 0.377782)], 65: [(0.230091, 0.418084)],
	66: [(0.158393, 0.410765)], 67: [(0.468272, 0.293594)], 68: [(0.47594, 0.255018)],
	71: [(0.33818, 0.207722)],
	72: [(0.844033, 0.430917)], 73: [(0.542804, 0.551548)], 74: [(0.337743, 0.208183)],
	75: [(0.337751, 0.211662)], 76: [(0.337771, 0.215925)], 77: [(0.337741, 0.21955)],
	78: [(0.33772, 0.225376)], 81: [(0.267608, 0.453786)], 82: [(0.054208, 0.678508), (0.876241, 0.698937)],
	83: [(0.357697, 0.433994)], 84: [(0.302018, 0.41577)], 85: [(0.391661, 0.348521)],
	86: [(0.350594, 0.378278)], 87: [(0.4368, 0.382814)],
}
# 54/55/56 (Steps Lights Frenzy/Ex.Ball/500,000) are each modeled in the retained table by four
# distinct "finger"-shaped Light objects forming a chase-lit arrow icon (Bot_finger_1-4 /
# Mid_finger_1-4 / Top_finger_1-4), not by one bulb at one coordinate; the manual's Lamps table
# lists a single #555/#44 bulb for each address with no quantity marker. Rather than guess which
# of the four finger segments represents "the" bulb, spatial placement for these three addresses
# is left unresolved.
LAMP_SPATIAL_UNRESOLVED = {54, 55, 56}

GI_RUDY_POSITIONS = [(0.698912, 0.09342), (0.83687, 0.113912), (0.76868, 0.317499)]


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"FunHouse retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained FunHouse extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"FunHouse retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"FunHouse retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"FunHouse retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the fh_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/fh.c fhGameData GEN_WPCALPHA_2 with wpc_dispAlpha, FLIP_SWNO(12,11) "
				"(flipper switches only, no FLIP_SOL -- no CPU-controlled flipper solenoid is declared for this "
				"driver), the inverted-switch mask {0x00,0x00,0x00,0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00,0x00} "
				"(column 5 = 0x11 = bits 1 and 5 = addresses 51 and 55), swStart/swTilt/swSlamTilt/swCoinDoor "
				"dedicated switches, every swXX/sXX #define, fh_handleMech (diverter, step gate, trap door, Rudy "
				"jaw/eyes causality), fhpa1GameData (GEN_WPCALPHA_1 prototype variant), and init_fh's driver-name "
				"dispatch between the two; src/wpc/wpc.c wpc_dispAlpha layout and GENWPC_HASFLIPTRON/GENWPC_HASDMD "
				"exclusion of GEN_WPCALPHA_1/GEN_WPCALPHA_2; src/wpc/core.h CORE_MAXSWCOL=16 (columns 0-9 matrix, "
				"10 coin door, 11 cabinet/flippers) and CORE_FIRSTLFLIPSOL/CORE_FIRSTUFLIPSOL; src/wpc/gen.h "
				"GEN_WPCALPHA_1/GEN_WPCALPHA_2 definitions."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-alpha.json",
			"revision": "repository",
			"locator": "WPC-Alpha public switch, DIP, solenoid, lamp, and five-GI address rules, reused unchanged for this first WPC-Alpha machine curated in the project",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/williams.funhouse.1990/archive-arcademanual_Funhouse_OPS/Funhouse_OPS.pdf",
			"original_filename": "Funhouse_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"122-page Williams FunHouse operations manual scan (Internet Archive item "
				"arcademanual_Funhouse_OPS), with a working but multi-column-scrambled text layer. Printed pages "
				"2-36 through 2-40 carry the lamp/switch/solenoid/G.I. location parts lists and their matrix and "
				"wiring tables; printed pages 2-24 and 2-32 carry the Jaw Drive/Eject Assembly and Unique Parts "
				"pages that fix Rudy's and the trap door's mechanism construction; Section 3 (printed 3-15 "
				"through 3-17) carries the Interboard Wiring switch/lamp/solenoid/G.I./flipper circuit tables."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics Games, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.funhouse.switch-locations",
					"locator": "PDF page 99, printed 2-38, switch-locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-locations.md",
					"sha256": "998d63a2d06cc9b5afcf444ad652179af47e1b1af392fb26d22cd6dee789fcbb",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.switch-matrix",
					"locator": "PDF page 100, printed 2-39, FUNHOUSE Switch Matrix wiring table",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-matrix.md",
					"sha256": "93d8858c53f0a3a961fe99b17ff7218707e6110cc2d4eef3dc495eabb738a610",
					"image": "evidence/excerpts/williams.funhouse.1990/switch-matrix.webp",
					"image_sha256": "d2221b041e00de17f4831c5fd1c9445e146024542ab5a9a3461d79611a84abc8",
					"image_derivation": "Funhouse_OPS.pdf page 100, crop box 0.08,0.04,0.68,0.46 of the page, rendered at 300 dpi with pdftoppm, reduced to 900px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.lamp-locations",
					"locator": "PDF page 97, printed 2-36, lamp-locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/lamp-locations.md",
					"sha256": "0a05d47eb1ec1159498d978ab1a1cdeee669ac444bfec6a49c94d13916455c53",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.lamp-matrix",
					"locator": "PDF page 98, printed 2-37, lamp matrix wiring table",
					"path": "evidence/excerpts/williams.funhouse.1990/lamp-matrix.md",
					"sha256": "ccbca902876402a125e4448c8a799f5d0a76a3d96080823efff30865e9808793",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page (address 12 confirmed at 600 dpi)",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.solenoid-locations",
					"locator": "PDF page 101, printed 2-40, solenoid and general-illumination locations parts list",
					"path": "evidence/excerpts/williams.funhouse.1990/solenoid-locations.md",
					"sha256": "89084bb0a0524c3701b9f0134ddf00ff9bcfac24235a2c2e714dd0e91ee410d2",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.switch-lamp-solenoid-circuits",
					"locator": "PDF page 119, printed 3-16, Switch/Lamp/Solenoid Circuits interboard wiring tables",
					"path": "evidence/excerpts/williams.funhouse.1990/switch-lamp-solenoid-circuits.md",
					"sha256": "b5b143551a0fd5255ee211d7cdc959a52cd776db56ffa708c9ceff95c7d45de4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.general-illumination-flipper-circuits",
					"locator": "PDF page 120, printed 3-17, General Illumination/Flipper/Power/Logic/Display Circuits interboard wiring tables",
					"path": "evidence/excerpts/williams.funhouse.1990/general-illumination-flipper-circuits.md",
					"sha256": "56b81515ce01cb20c11d3f9137ef93c6f40381c316e3ad56f08406aab7b2e1a5",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.funhouse.rudy-mechanism-parts",
					"locator": "PDF pages 85 and 93, printed 2-24 and 2-32, Jaw Drive/Eject Assembly and Unique Parts pages",
					"path": "evidence/excerpts/williams.funhouse.1990/rudy-mechanism-parts.md",
					"sha256": "45a06c3150ef08f2380452187cd7baec4f77ad8448e7e0990e0c6307ceb81966",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/funhouse/manual-transcription.md",
			"revision": "2026-08-07",
			"locator": (
				"Consolidated retained human transcription of every rendered manual table used by this "
				"definition, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/williams.funhouse.1990/. Duplicates the in-repository "
				"evidence excerpts in one document for reviewer convenience."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/source/Funhouse%20%28Williams%201990%29_1.3.vpx",
			"original_filename": "Funhouse (Williams 1990)_1.3.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine, version 1.3. Exact playfield bounds "
				f"are {TABLE_BOUNDS}; normalized coordinates are x/964 and y/2162. Geometry authority only for "
				"named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPX table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": "322fba2dec939b50e0730da8caca177545aa8f8bc055ba136360ae55deb4e863",
			"known_working": True,
			"locator": (
				'Retained embedded script (80,593 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "fh_905h" (line 64; the commented-out line 63 reads "fh_905" and is not the '
				"active binding), the SolCallback table for solenoids 1-8, 14-28, the UpdateLamps per-address "
				"light bindings, the UpdateGI/UpdateGI2 G.I. region dispatch (Case 0/1/2/3/4), the trap door "
				"TrapMover_Timer state machine (Controller.Switch(76) set from PrTrap.RotX), and the "
				"SolCallback(sLRFlipper)/SolCallback(sLLFlipper) generic core.vbs registration that this driver "
				"never exercises (fhGameData declares no FLIP_SOL)."
			),
			"license": "NOASSERTION",
			"attribution": "table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json",
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
		"board": "WPC-Alpha CPU board",
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
				"used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": f"D{address}"},
				],
				normally_closed=False,
				roles=[role],
				physical={"location": "coin door", "switch_type": "button", "notes": f"Printed dedicated grounded switch D{address}. {note}"},
				wiring={"board": "WPC-Alpha CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = address in UNUSED_MATRIX_ADDRESSES or label is None
			identifier = f"switch.matrix-{address}"
			kind = "constant" if address == 24 else "switch"
			part_number = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part_number:
				physical["part_number"] = part_number
			if address in SWITCH_TYPES:
				physical["switch_type"] = SWITCH_TYPES[address]
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			if unused:
				notes += " The switch-locations and switch-matrix pages both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				notes += (
					' Printed "(opto)" on both the switch-locations page (2-38) and the switch-matrix page '
					"(2-39) -- the only two switch-matrix positions on this machine identified as optical "
					"construction. Pinned PinMAME's fhGameData inverted-switch mask (column 5 = 0x11 = bits 1 "
					"and 5) normalizes both addresses, so the public switch state is already normalized and "
					"must not be inverted again. This is the only pair of optos in the entire FunHouse switch "
					"matrix; every other position is a plain leaf/microswitch/button/tilt construction with no "
					"opto marking on either printed page."
				)
			if address == 24:
				notes += " Physical part A-8630, the same part number printed for switch 22 (Front Door); a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 23:
				notes += ' Pinned fh.c declares a vestigial #define swTicket 23 never referenced elsewhere in the driver, matching the manual\'s "Not Used" fitment; treated as unfitted.'
			if address == 63:
				notes += " No dedicated VPX trigger/target object was found for this address in the retained extraction; spatial placement is left unresolved."
			if address == 73:
				notes += " Projected onto the retained table's Drain kicker object, which the outhole solenoid (1) also shares; no separate switch-only object exists."
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
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
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, 21, 22}:
					role = {13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door"}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet"
					if address == 22:
						extra["initial_active"] = True
				elif address in SWITCH_SPATIAL_UNRESOLVED:
					pass
				else:
					extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

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
					"location": "WPC-Alpha CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-Alpha CPU-board country/option configuration DIP bank. The retained transcription of "
						"this manual does not include a per-country switch-combination chart, so no specific "
						"ON/OFF combination is asserted here."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	return f"device.{label.lower().replace(chr(39), '').replace('/', '-').replace(',', '').replace('.', '').replace(' ', '-')}"


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		is_flasher = address in FLASHER_QUANTITIES
		is_flipper_related = False
		kind = "flasher" if is_flasher else "motor" if address in {21, 22} else "coil"
		physical: dict[str, Any] = {}
		part_number = SOLENOID_PARTS.get(address)
		if part_number and not is_flasher:
			physical["part_number"] = part_number
		notes = f"Printed solenoid table entry {address:02d}."
		if is_flasher:
			quantity = FLASHER_QUANTITIES[address]
			physical["quantity"] = quantity
			notes += f" Printed flashlamp complement: {quantity} {part_number} bulb(s) on this circuit."
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		if address == 7:
			notes += " Cabinet-mounted knocker; no playfield location."
		if address in {21, 22}:
			notes += (
				" Rudy's jaw is driven by a continuously-running DC gearmotor (A-13997, Jaw Drive Assembly) "
				"through a worm gear/sector pair, not a coil stroke; solenoid 22 (Up/Down Driver) is the "
				"motor's direction relay. Pinned fh_handleMech opens the jaw when both 21 and 22 are energized "
				"together and closes it when 21 alone is energized. Projected onto switch 51 (Dummy Jaw), the "
				"only fixed point recorded for Rudy's Head Assembly, since no dedicated jaw-motor VPX object "
				"was identified separately from the head figure itself."
			)
		if address in {25, 26, 27, 28}:
			notes += (
				" One of four independent drive lines on Rudy's Head Assembly: 25/28 select eye left/right "
				"position, 26/27 latch the eyelids open/closed. Pinned fh_handleMech treats eyelid open/close "
				"as a persistent latch and eye left/right as a momentary position read each mechanics tick. "
				"Projected onto switch 51 (Dummy Jaw), the only fixed point recorded for Rudy's Head Assembly."
			)
		if address in {5, 6}:
			notes += " Trap door open/close drive; trap-door-closed switch 76 is set programmatically from the trap door's own rotation angle rather than read from a separate switch object (see mechanism.trap-door)."
		physical["notes"] = notes

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.solenoid", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address:02d}"},
			],
			"physical": physical,
		}
		if address in SOLENOID_WIRING:
			wiring_data = SOLENOID_WIRING[address]
			extra["wiring"] = {
				"board": "WPC-Alpha power driver board",
				"control_connection": wiring_data["control_connection"],
				"driver_transistor": wiring_data["driver_transistor"],
			}
		role = "emitter" if is_flasher else "effect" if kind == "motor" else "effect"
		if address == 7:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_CALLBACKS else (MANUAL_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS.get(address)
			unused = label is None
			identifier = f"lamp.matrix-{address}"
			bulb = LAMP_BULBS.get(address)
			physical: dict[str, Any] = {"quantity": LAMP_QUANTITIES.get(address, 1)}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in LAMP_QUANTITIES:
				notes += f' The lamp-matrix page marks this insert "(x {LAMP_QUANTITIES[address]})" and the retained table binds that many distinct, non-co-located bulb positions.'
			if address == 12:
				notes += (
					' The lamp-locations page (2-36) reads "Gangway 10,000" while the lamp-matrix page (2-37) '
					'reads "Gangway 100,000" for this same address (both confirmed at 600 dpi); see '
					"conflict.gangway-lamp-12-value. This label uses the matrix page's value, which fits the "
					"ascending 75,000/100,000/150,000/200,000/250,000/Extra-Ball award ladder implied by its "
					"neighbors."
				)
			if address == 51:
				notes += ' The lamp-matrix page additionally prints "(Left)" on this cell; the lamp-locations page has no such qualifier, and there are only three jet bumpers on this machine (Left/Right/Lower per the solenoid table), so this is read as a positional descriptor rather than a naming conflict.'
			if address == 88:
				notes += " Cabinet Start-button backlight, explicitly annotated \"(cabinet)\" on the lamp-locations page."
			if address in LAMP_SPATIAL_UNRESOLVED:
				notes += (
					" The retained table models this address with four distinct 'finger'-shaped Light objects "
					"forming a chase-lit arrow icon rather than one bulb at one coordinate, and the manual states "
					"a single bulb with no quantity marker; spatial placement is left unresolved rather than "
					"guessing which finger segment is authoritative."
				)
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
					"board": "WPC-Alpha power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				label = f"Not Used Lamp Position {address}"
			elif address == 88:
				availability = "used"
				extra["roles"] = ["cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				availability = "used"
				if address in LAMP_SPATIAL_UNRESOLVED:
					pass
				else:
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
		identifier = f"gi.string-{address}"
		wiring_data = GI_FEED_WIRING[address]
		notes = (
			f"Printed general-illumination string {address + 1:02d} ({label}). Retained script region: "
			f"{GI_SCRIPT_REGIONS[address]}. Insert-panel connector: {wiring_data['insert_connection']}."
		)
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-Alpha power driver board",
				"control_connection": wiring_data["control_connection"],
				"driver_transistor": wiring_data["driver_transistor"],
			},
		}
		physical: dict[str, Any] = {}
		if address == 1:
			notes += (
				" Retained script UpdateGI2/UpdateGI Case 1 drives only the Rudy sign/shade collection "
				"(RudySign1, RudySign2, RudyShade) -- it does not implement a generic 'front playfield' "
				"lighting effect. The manual's 'Front Playfield' label and the script's Rudy-specific behavior "
				"are recorded as a disagreement about which physical region this string illuminates; see "
				"conflict.gi-region-naming. Spatial placement uses the three real implemented objects, "
				"projected onto Rudy's own sign/shade assembly."
			)
			physical["quantity"] = len(GI_RUDY_POSITIONS)
			extra["spatial"] = located(identifier, "emitter", GI_RUDY_POSITIONS, VPX_SCRIPT_SOURCE, VPX_TABLE_SOURCE)
		elif address in {2, 4}:
			region = "GI_Upper (19 members)" if address == 2 else "GI_Lower (45 members)"
			notes += (
				f" Retained script drives a real playfield light collection ({region}) for this string, but "
				"individual per-bulb spatial extraction for that collection was not completed in this pass; "
				"spatial placement is left unresolved rather than guessing representative positions."
			)
			if address == 4:
				notes += (
					' The manual\'s "Top Playfield" label directly contradicts the script\'s own region comment '
					'"Lower Playfield" for this address; see conflict.gi-region-naming.'
				)
		else:
			notes += " Backbox-only circuit; the retained script implements no case for this address, so it has no playfield coordinate."
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			if address == 3:
				notes += ' The manual additionally claims a "Rt. Rr Plfld" (playfield) component for this circuit that the retained script never implements; no playfield coordinate is asserted for that claim.'
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
			"id": "display.player-1-alphanumeric",
			"label": "Player 1/3 sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 0,
			"segment_start": 0,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
		{
			"id": "display.player-2-alphanumeric",
			"label": "Player 2/4 sixteen-character alphanumeric display",
			"kind": "segment",
			"controller_index": 1,
			"segment_start": 20,
			"width": 16,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		},
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
		if positions:
			record["positions"] = [
				{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
				for position_id, position_label, position_sensors, description in positions
			]
		return record

	return [
		mechanism(
			"mechanism.rudy-jaw",
			"Rudy's motorized jaw",
			"motorized",
			[output_id("Mouth Motor"), output_id("Up/Down Driver")],
			["switch.matrix-51"],
			"A DC gearmotor (A-13997 Jaw Motor Assembly) drives Rudy's jaw open and closed through a worm "
			"gear/sector pair (Jaw Drive Assembly A-13752), not a coil stroke. Pinned fh_handleMech: if the "
			"jaw is open and solenoid 21 (Mouth Motor) is energized while solenoid 22 (Up/Down Driver) is "
			"not, the jaw closes; if the jaw is closed and both 21 and 22 are energized together, the jaw "
			"opens. Dummy Jaw opto 51 senses a ball landing in Rudy's open mouth (printed opto, normalized "
			"by PinMAME's inverted-switch mask).",
			[("open", "Jaw open", ["switch.matrix-51"], "Ball can land in Rudy's mouth.")],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.rudy-eyes",
			"Rudy's eyes",
			"motorized",
			[output_id("Eyes Right"), output_id("Eyelids Open"), output_id("Eyelids Close"), output_id("Eyes Left")],
			[],
			"Four independent drive lines on Rudy's Head Assembly. Eyelids open (solenoid 26) and close "
			"(solenoid 27) latch a persistent open/closed state; eyes right (25) and eyes left (28) are read "
			"as momentary position signals each mechanics tick, with neither held meaning the eyes rest "
			"straight ahead. Pinned fh_handleMech tracks both the open/closed latch and the left/right/"
			"straight position independently. There is no dedicated switch for eye position or eyelid state; "
			"it is purely a scored callback effect with no sensor feedback to the controller.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.trap-door",
			"Trap door",
			"gate",
			[output_id("Trap Door Open"), output_id("Trap Door Closed")],
			["switch.matrix-76", "switch.matrix-75"],
			"Solenoid 5 opens and solenoid 6 closes a trap door in the upper-right loop path. Pinned "
			"fh_handleMech and the retained script's TrapMover_Timer both derive Trap Door Closed switch 76 "
			"directly from the door's own rotation angle rather than reading a separate contact switch -- the "
			"retained script sets Controller.Switch(76)=1 once the door primitive's RotX falls to 90 degrees "
			"(closed) and clears it back to 0 once the door opens past 90 degrees. Upper Right Loop switch 75 "
			"senses a ball taking the loop shot when the door is closed, and the printed manual documents a "
			"scoring loop feature (Trap Door Bonus lamp 63, Trap Door Frenzy lamp 83) tied to whether the "
			"door is open when a ball reaches it.",
			[
				("closed", "Trap door closed", ["switch.matrix-76"], "Door primitive RotX at or below 90 degrees; projected onto the door's own mechanism (no separate contact switch object)."),
				("loop", "Upper right loop shot", ["switch.matrix-75"], "Ball takes the loop path past the trap door."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.step-gate",
			"Left outlane step gate",
			"gate",
			[output_id("Steps Gate")],
			[],
			"Solenoid 14 (printed \"Steps Gate\"; the retained script's own comment calls it the \"Steps "
			"shooter lane diverter\") opens a gate that reroutes a ball in the left outlane back to the left "
			"ballshooter lane (switch 47) instead of draining, functioning as a kickback-style save feature "
			"gated by whatever awards the STEP letters. Pinned fh_handleMech holds the gate open for a fixed "
			"50-tick timer after the solenoid fires, then auto-closes it; there is no separate open/closed "
			"sensor switch for the gate itself.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.ramp-diverter",
			"Upper ramp/Steps track diverter",
			"diverter",
			[output_id("Ramp Diverter")],
			["switch.matrix-16", "switch.matrix-35", "switch.matrix-38"],
			"Solenoid 2 diverts a ball on the upper ramp between the Steps track (S-T-E-P letters, switches "
			"17/31/54/64/86/73) and the main upper-ramp path (Upper Ramp Switch 16, Steps Track Lower/Upper "
			"35/38, Ramp Exit Track 48, Ramp Entrance 56). Pinned fh_handleMech asserts the diverter open for "
			"a fixed 25-tick window after the solenoid fires (matching the printed \"Ramp Diverter\" high-"
			"power coil, AE-26-1200) and auto-closes it afterward; there is no separate diverter-position "
			"sensor switch.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.trough-and-shooters",
			"Ball trough, outhole, and dual shooter lanes",
			"kicker",
			[output_id("Outhole"), output_id("Trough")],
			["switch.matrix-73", "switch.matrix-72", "switch.matrix-74", "switch.matrix-47", "switch.matrix-62"],
			"FunHouse has two manual shooter lanes (left, switch 47; right, switch 62) feeding a shared trough. "
			"Solenoid 1 (Outhole) kicks a drained ball into the trough; solenoid 15 (Trough, retained script "
			"comment \"Main trough kickout\") ejects a trough ball back to a shooter lane. Trough positions are "
			"Left Trough (72), Center Trough (74), and Right Trough (63, no VPX geometry resolved in this "
			"pass -- see coverage.missing).",
			[
				("outhole", "Ball in outhole", ["switch.matrix-73"], "Drain sensor before the trough kickout."),
				("left-shooter", "Left shooter lane", ["switch.matrix-47"], "Manual left plunger lane."),
				("right-shooter", "Right shooter lane", ["switch.matrix-62"], "Manual right plunger lane."),
			],
			CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.tunnel-kickout",
			"Tunnel kickout hole",
			"kicker",
			[output_id("Tunnel Kickbig")],
			["switch.matrix-58"],
			"A ball resting on opto-free microswitch 58 (Tunnel Kickout) is kicked back to the playfield by "
			"solenoid 4 (printed \"Tunnel Kickbig\"). The retained script's SolKickout handler fires two "
			"physical kicker objects in sequence (a primary kick followed by a delayed second-chute kick), "
			"consistent with the tunnel's own captive ball-return geometry rather than a single simple "
			"saucer.",
			[("held", "Ball in the tunnel kickout", ["switch.matrix-58"], "Tunnel kickout switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.rudys-hideout",
			"Rudy's Hideout kickback",
			"kicker",
			[output_id("Kickbig")],
			["switch.matrix-46"],
			"A ball landing behind Rudy's head (Rudy Hideout Kickbig switch 46, a skill-shot landing spot per "
			"the printed player rules) is returned to play by solenoid 3.",
			[("held", "Ball in Rudy's Hideout", ["switch.matrix-46"], "Rudy Hideout Kickbig switch.")],
			MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.dummy-eject-hole",
			"Dummy eject hole",
			"kicker",
			[output_id("Dummy Eject Hole")],
			["switch.matrix-65"],
			"A separate saucer near Rudy's head (Dummy Eject Hole switch 65) is kicked back to play by "
			"solenoid 16 (retained script comment \"Rudy's mouth kickout\", though it is a distinct switch "
			"and coil from the jaw mechanism proper).",
			[("held", "Ball in the dummy eject hole", ["switch.matrix-65"], "Dummy eject hole switch.")],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.multiball-lock",
			"Three-ball lock and multi-ball release",
			"kicker",
			[output_id("Multi-ball Release")],
			["switch.matrix-25", "switch.matrix-27", "switch.matrix-28"],
			"Three lock switches (Lock Mech Right 25, Lock Mech Center 27, Lock Mech Left 28) share one "
			"printed 3-Switch Assembly (A-14138). The retained script's MBRelease handler fires solenoid 8, "
			"drops the WaSw28 lock wall, and rotates a release object to feed all locked balls to the "
			"trough together for multi-ball.",
			[
				("right", "Right lock position", ["switch.matrix-25"], "Rightmost of the three lock positions."),
				("center", "Center lock position", ["switch.matrix-27"], "Middle lock position."),
				("left", "Left lock position", ["switch.matrix-28"], "Leftmost lock position, released by MBRelease."),
			],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Jet Bumper"), output_id("Right Jet Bumper"), output_id("Lower Jet Bumper")],
			["switch.matrix-18", "switch.matrix-77", "switch.matrix-68"],
			"Three jet bumpers. The retained script's Bumper1_Hit, Bumper2_Hit, and Bumper3_Hit handlers "
			"pulse switches 18, 77, and 68 and fire coils 9, 10, and 11 respectively, matching printed Left/"
			"Right/Lower Jet Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-18"], "Left bumper of the nest."),
				("right", "Right jet bumper", ["switch.matrix-77"], "Right bumper of the nest."),
				("lower", "Lower jet bumper", ["switch.matrix-68"], "Bumper closest to the player."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-41", "switch.matrix-53"],
			"Each slingshot (printed \"Kicker\" on the solenoid table, \"(sling) Kicker\"/\"Slingshot "
			"(Kicker)\" on the switch tables) fires its own coil on the same event. The retained script's "
			"LeftSlingShot_Slingshot and RightSlingShot_Slingshot handlers pulse matrix addresses 41 and 53 "
			"and fire coils 12/13 together.",
			[
				("left", "Left slingshot", ["switch.matrix-41"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-53"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.flippers",
			"Lower flipper pair (no CPU-controlled solenoid)",
			"other",
			[],
			["switch.matrix-11", "switch.matrix-12"],
			"FunHouse is a pre-Fliptronics WPC-Alpha machine: fhGameData declares FLIP_SWNO(12,11) (flipper "
			"switches only) with no FLIP_SOL() call, so pinned PinMAME's core_getSol never routes any public "
			"solenoid address to a flipper coil for this driver. The printed Flipper Circuits wiring page "
			"(page 120) confirms the physical construction: Left/Right Flipper Power and four Upper/Lower "
			"Flipper positions are wired through a dedicated flipper driver board (J109/J110) directly to "
			"the flipper buttons and end-of-stroke switches, entirely separate from the CPU-addressable "
			"solenoid matrix (1-50). Switches 11 (Right Flipper) and 12 (Left Flipper) sit in the ordinary "
			"switch matrix (not a dedicated Fliptronic column, which does not exist on this hardware "
			"generation) and are read by the CPU for scoring/combo purposes only; they do not gate whether "
			"the flipper fires. FunHouse has no upper flippers.",
			[],
			CORE_SOURCE, MANUAL_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.gangway-lamp-12-value",
			"path": "outputs[binding.device=12,group=pinmame.output.lamp]",
			"description": (
				"The lamp-locations parts list (manual printed page 2-36) reads \"Gangway 10,000\" for lamp "
				"12, confirmed at 600 dpi. The lamp-matrix wiring page (printed page 2-37) reads \"Gangway "
				"100,000\" for the same address, also confirmed at 600 dpi. Lamps 11/13/14/15/16 print an "
				"unambiguous ascending award ladder on both pages (75,000 / 150,000 / 200,000 / 250,000 / "
				"Extra Ball), which only 100,000 continues monotonically; 10,000 would be a value smaller "
				"than the first rung. No independent third source (the retained script does not implement "
				"scoring-value text) was available to settle this outright. The promoted definition's label "
				"uses \"Gangway 100,000\" on the strength of the award-ladder pattern, but the disagreement "
				"itself is unresolved and the smaller-value reading has not been ruled out as a genuine "
				"factory print. Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, MANUAL_SUPPORT_SOURCE],
		},
		{
			"id": "conflict.gi-region-naming",
			"path": "outputs[binding.group=pinmame.output.gi,binding.device=1,4]",
			"description": (
				"The manual's printed general-illumination locations page (2-40) labels G.I. string 02 "
				"\"Front Playfield\" and string 05 \"Top Playfield\". The retained known-working script's own "
				"UpdateGI/UpdateGI2 region header comment labels the same two addresses (0-based Case 1 and "
				"Case 4) \"Rudy\" and \"Lower Playfield\" respectively, and its actual implemented behavior "
				"matches those script labels exactly: Case 1 drives only the RudySign1/RudySign2/RudyShade "
				"collection (not a generic front-playfield wash), and Case 4 drives the GI_Lower collection "
				"(the reverse of \"Top\"). G.I. string 01 (\"Upper Backglass\"/Case 0) agrees between both "
				"sources, and string 03 (\"Rear Playfield\"/Case 2 \"Upper Playfield\") is a plausible "
				"reconciliation under this project's y=0-is-rear coordinate convention, but strings 02 and 05 "
				"remain a direct disagreement about which physical region each address illuminates. The "
				"promoted definition uses the manual's printed label as the device name (physical-construction "
				"authority) while using the script's real implemented objects for spatial placement (runtime "
				"authority) and discloses the disagreement in each device's notes. Unresolved."
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
			"id": "williams.funhouse.1990",
			"name": "FunHouse",
			"manufacturer": "Williams",
			"year": 1990,
			"kind": "physical_pinball",
			"ipdb_id": 860,
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts", "recreation_notes"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "conflicted",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.wpc-alpha",
			"hardware_generation": "0x2",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/funhouse-1990.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"FunHouse device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	unresolved_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	unresolved_outputs: list[dict[str, Any]] = []
	placement_count = 0
	for device in definition["outputs"]:
		binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
		spatial = device.get("spatial")
		if spatial is None:
			unresolved_outputs.append(binding)
		elif spatial["status"] == "not_applicable":
			not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
		else:
			placement_count += len(spatial["placements"])
			located_outputs.append(binding)
	for device in definition["inputs"]:
		spatial = device.get("spatial")
		if spatial is not None and spatial["status"] != "not_applicable":
			placement_count += len(spatial["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "partial",
		"blockers": [
			"Switch 63 (Right Trough) has no dedicated VPX trigger/target object in the retained "
			"extraction; spatial placement is left unresolved.",
			"Lamps 54, 55, and 56 (Steps Lights Frenzy/Ex.Ball/500,000) are each modeled by four "
			"distinct 'finger'-shaped Light objects forming a chase-lit arrow rather than one bulb at "
			"one coordinate; the manual states a single bulb per address with no quantity marker, so "
			"no single representative coordinate is asserted.",
			"G.I. strings 2 (Rear Playfield) and 4 (Top Playfield) each drive a real playfield light "
			"collection in the retained script (GI_Upper, 19 members; GI_Lower, 45 members), but "
			"individual per-bulb spatial extraction for those two collections was not completed in "
			"this pass.",
			"conflict.gangway-lamp-12-value and conflict.gi-region-naming are both unresolved.",
			"knowledge/williams/funhouse-1990.md has not yet had the mandatory independent high-tier "
			"cross-provider review.",
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
			"manifest_uri": "external:pinmame-vpx-sources/williams/funhouse-1990/extracted-vpxtool.manifest.json",
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
		"unresolved_input_addresses": sorted(unresolved_inputs),
		"unresolved_output_bindings": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": 76, "reason": "Projected onto the trap door primitive's own rotation state (PrTrap.RotX); the retained script sets this switch programmatically rather than reading a separate contact-switch object."},
			{"group": "pinmame.output.solenoid", "address": 5, "reason": "Projected onto the trap door primitive; open/close solenoids share the mechanism's own position with switch 76."},
			{"group": "pinmame.output.solenoid", "address": 6, "reason": "Projected onto the trap door primitive; see solenoid 5."},
			{"group": "pinmame.output.solenoid", "address": 3, "reason": "Projected onto switch 46's position; the retained script's bsHideout saucer helper shares switch 46's own kicker object."},
			{"group": "pinmame.output.solenoid", "address": 16, "reason": "Projected onto switch 65's position; the retained script's bsRudy saucer helper shares switch 65's own kicker object."},
			{"group": "pinmame.output.solenoid", "address": 8, "reason": "Projected onto switch 28's position; the retained script's MBRelease handler acts directly on the WaSw28 lock-wall object with no separate release-mechanism object."},
			{"group": "pinmame.output.gi", "address": 1, "reason": "Projected onto Rudy's own sign/shade assembly (RudySign1, RudySign2, RudyShade); the retained script's GI Case 1 drives that collection directly rather than a generic playfield wash."},
			{"group": "pinmame.output.solenoid", "address": 21, "reason": "Projected onto switch 51 (Dummy Jaw); no dedicated jaw-motor VPX object was identified separately from Rudy's head figure."},
			{"group": "pinmame.output.solenoid", "address": 22, "reason": "Projected onto switch 51 (Dummy Jaw); see solenoid 21."},
			{"group": "pinmame.output.solenoid", "address": 25, "reason": "Projected onto switch 51 (Dummy Jaw); the only fixed point recorded for Rudy's Head Assembly."},
			{"group": "pinmame.output.solenoid", "address": 26, "reason": "Projected onto switch 51 (Dummy Jaw); see solenoid 25."},
			{"group": "pinmame.output.solenoid", "address": 27, "reason": "Projected onto switch 51 (Dummy Jaw); see solenoid 25."},
			{"group": "pinmame.output.solenoid", "address": 28, "reason": "Projected onto switch 51 (Dummy Jaw); see solenoid 25."},
			{"group": "pinmame.input.switch", "address": 73, "reason": "Projected onto the retained table's Drain kicker object, shared with the outhole solenoid (1)."},
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.funhouse.1990/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/funhouse/manual-transcription.md",
			},
		},
		"excluded_object_classes": [
			"l51a/l51b, l52a/l52b, l72a/l72b co-located brightness-doubling and same-fixture secondary Light objects (manual prints one bulb per address with no quantity marker)",
			"fmflNN / cfXX flash-modulation and clock-face helper Light/Flasher objects paired with each primary lNN lamp object",
			"LBballoon/LRballoon/LYballoon/lHotDogCartB optional-mod decorative objects gated behind BalloonMod/HotDogCartMod table toggles",
		],
		"unresolved": (
			[{"group": "pinmame.input.switch", "address": address} for address in sorted(unresolved_inputs)]
			+ sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"]))
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# FunHouse (Williams, 1990) spatial review",
		"",
		f"Status: {report['status']}. This is the first WPC-Alpha machine curated in this project. "
		"The physical machine record lives at `machines/partial/williams/funhouse-1990.json`.",
		"",
		"The matching source is the retained known-working `Funhouse (Williams 1990)_1.3.vpx` at "
		f"SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact "
		f"playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/964 and y/2162 "
		"rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded script is the runtime address and causality authority; the Williams operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns "
		"controller topology; the retained table supplies geometry.",
		"- This manual carries a working `pdftotext` text layer, but its multi-column tables scramble "
		"under extraction, so every printed table used here was still read from 300/600 dpi rendered "
		"page images, not OCR text.",
		"- FunHouse's switch matrix has exactly two opto positions (51, 55), both marked \"(opto)\" in "
		"the manual and both normalized by pinned PinMAME's inverted-switch mask -- a clean sweep with "
		"zero polarity disagreement.",
		"- FunHouse is pre-Fliptronics WPC-Alpha hardware: `fhGameData` declares flipper switches only "
		"(`FLIP_SWNO(12,11)`) with no `FLIP_SOL()`, so no public solenoid address drives a flipper coil. "
		"Flipper power is wired through a dedicated flipper driver board (printed Flipper Circuits page) "
		"entirely outside the CPU-addressable solenoid matrix.",
		"- Several switches and solenoids have no dedicated trigger/kicker object because the retained "
		"script sets their public state directly from another mechanism's own position (the trap door's "
		"rotation angle) or shares a saucer helper's underlying kicker object with a co-located switch. "
		"Those addresses are documented projections onto the real object that carries the underlying "
		"state, listed below.",
		"- Two addresses (switch 63; G.I. strings 2 and 4's individual bulbs) and three lamps (54/55/56) "
		"have no asserted spatial placement at all rather than an invented or approximated coordinate.",
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
		f"- Unresolved input addresses: {len(report['unresolved_input_addresses'])}",
		f"- Unresolved output bindings: {len(report['unresolved_output_bindings'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"This record stays `partial`. Two unresolved conflicts (`conflict.gangway-lamp-12-value`, "
		"`conflict.gi-region-naming`), six addresses with no spatial placement (switch 63; lamps 54/55/56; "
		"G.I. strings 2 and 4's individual playfield bulbs), and the absence of the mandatory independent "
		"high-tier cross-provider review together keep `coverage.status = \"partial\"` with "
		"`coverage.missing = [\"spatial_placement\", \"unresolved_conflicts\", \"recreation_notes\"]`. "
		"Every other dimension -- catalog identity, address enumeration, physical wiring, mechanism "
		"inventory and behavior, and variant coverage across the fifteen-driver `fh_l9` clone tree -- is "
		"validated.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, "
		f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		"- Human transcription of every printed table read from the rendered manual pages: "
		"`external:pinmame-review-artifacts/funhouse/manual-transcription.md`.",
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
		raise RuntimeError(f"Stale FunHouse author-ready definition is still present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"FunHouse definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"FunHouse seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"FunHouse definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"FunHouse seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"FunHouse spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"FunHouse spatial review drifted from its deterministic curator: {markdown_path}")
	print("FunHouse definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"FunHouse extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("FunHouse retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
