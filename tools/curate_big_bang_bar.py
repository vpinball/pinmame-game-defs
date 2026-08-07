"""Curate the physical Capcom Big Bang Bar (1996) machine definition.

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
DEFINITION_PATH = ROOT / "machines/partial/capcom/big-bang-bar-1996.json"
SEED_PATH = ROOT / "tools/seeds/capcom/big-bang-bar-1996.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/capcom/big-bang-bar-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/capcom/big-bang-bar-1996.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-capcom"
MANUAL_SOURCE = "manual.capcom.big-bang-bar.1996"
SCHEMATIC_SOURCE = "manual-schematic.capcom.big-bang-bar.1996"
MANUAL_SUPPORT_SOURCE = "manual-support.capcom.big-bang-bar.1996"
VPX_TABLE_SOURCE = "vpx-table.bbb-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.bbb-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.bbb-vpw-1-0"

TABLE_SHA256 = "7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5"
SCRIPT_SHA256 = "db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7"
MANUAL_SHA256 = "5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5"
SCHEMATIC_SHA256 = "fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603"
MANUAL_TRANSCRIPTION_SHA256 = "3e503420d32c307f409edaa57c80d6f4bfa9f01d90cd0e47dbc6ddc755188994"
MANUAL_TRANSCRIPTION_SOLENOIDS_SHA256 = "b996714bd9cd3811481ab0eb0ccce071c3d019819844eaffffaf5318e28c4bd5"
VPX_GEOMETRY_NOTES_SHA256 = "e1339971328d98e365b6574733b08f8dc1849814806bb2973019482c93468ac5"

EXTRACTION_RELATIVE_PATH = Path("capcom/big-bang-bar-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("capcom/big-bang-bar-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "8b1b7c6f35b98b0fecf1d88ac0746d81599fd8006189d58998c255de62fc2e90"
EXTRACTION_FILE_COUNT = 2874
EXTRACTION_TOTAL_BYTES = 1091052346

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2162"

DRIVER_IDS = ("bbb109", "bbb108")
DRIVER_COMPATIBILITY = {
	"bbb109": (
		"identical",
		"Capcom Beta 1.9 (US) game ROM, the pinned catalog's clone-tree parent. Built with the "
		"INITGAMEFF macro (src/wpc/capgames.c), which declares hw.custSol=1 and a name##_getsol "
		"callback reading a RAM 'Fast Flips' game-on/off flag, publishing public solenoid address "
		"51. The retained known-working VPX table binds this driver (Const cGameName = \"bbb109\").",
	),
	"bbb108": (
		"identical",
		"Capcom Beta 1.8 (US) game ROM; a slightly earlier firmware revision of the same physical "
		"machine sharing identical switch/lamp/solenoid roms u2l/u2h and CAPCOMS sound ROMs with "
		"bbb109, differing only in the u1l/u1h program ROMs. Built with the plain INITGAME macro "
		"(hw.custSol=0), so it does not publish public solenoid address 51 at all.",
	),
}

# --- Manual "Location of Switches & Optos" (printed page 83, PDF 87) and companion schematic
# sheet 6 cross-check. Cabinet switches 1-16 (cc_m2sw col 9 = 1-8, col 0 = 9-16); playfield
# matrix 17-80 (cc_m2sw col 1-8).
CABINET_SWITCH_LABELS = {
	1: "Coin Chute 1", 2: "Coin Chute 2", 3: "Coin Chute 3", 4: "Coin Chute 4",
	5: "Left Flipper Button", 6: "Right Flipper Button", 7: "Start Button",
	8: "Coin Door Open (Mode)", 9: "Coin Door Slam Tilt", 10: "Tilt Bob",
	15: "Token Dispense", 16: "Ticket Dispense",
}
CABINET_SWITCH_UNUSED = {11, 12, 13, 14}
CABINET_SWITCH_PARTS = {
	5: "SW00127", 6: "SW00127", 7: "SW00130", 8: "SW00132", 9: "SW00121", 10: "A-00065-1",
}
CABINET_SWITCH_TYPE = {
	5: "button", 6: "button", 7: "button", 8: "other", 9: "tilt", 10: "tilt",
	15: "other", 16: "other", 1: "other", 2: "other", 3: "other", 4: "other",
}

SWITCH_LABELS = {
	17: "4-Bank Mercury", 18: "4-Bank Venus", 19: "4-Bank Pythos", 20: "4-Bank Mars",
	21: "Ramp Standup Left", 22: "Ramp Standup Right", 23: "Ramp Standup Side",
	24: "Ramp Entrance", 25: "Spinner", 26: "Outer Orbit Left", 27: "Inner Orbit Left",
	28: 'Rollover "B"', 29: 'Rollover "A"', 30: 'Rollover "R"', 31: "Tube Entrance",
	32: "Ramp Exit", 33: "Left Flipper EOS", 34: "Right Flipper EOS", 35: "Outhole",
	36: "Trough 1 Ball", 37: "Trough 2 Balls", 38: "Trough 3 Balls", 39: "Trough 4 Balls",
	41: "Left Slingshot", 42: "Right Slingshot", 43: "Shooter Lane", 44: "Outlane Left",
	45: "Inlane Left", 46: "Lower Lock 1 Ball", 47: "Lower Lock 2 Balls",
	48: "Lower Lock 3 Balls", 49: "3-Bank Uranus", 50: "3-Bank Neptune", 51: "3-Bank Pluto",
	52: "3-Bank Standup Left", 53: "3-Bank Standup Right", 54: "Star Bumper Left",
	55: "Star Bumper Right", 56: "Star Bumper Middle", 57: "Alien Motor", 58: "1-Bank",
	59: "Inner Orbit Right", 60: "Outer Orbit Right", 61: "Alien Lock Left",
	62: "Alien Lock Right", 65: "Inlane Right", 66: "Outlane Right", 67: "Eject Hole",
	68: "Upper Right Flipper EOS", 69: "Island Entrance", 70: "Island Exit Left",
	71: "Island Exit Right", 77: "Captive Bottom Left", 78: "Captive Top Left",
	79: "Captive Bottom Right", 80: "Captive Top Right",
}
# Printed "UNUSED" on the switch-matrix page.
UNUSED_MATRIX_ADDRESSES = {40, 63, 64, 72, 73, 74, 75, 76}
SWITCH_PARTS = {
	17: "SW00106", 18: "SW00106", 19: "SW00106", 20: "SW00106",
	21: "A-00583-FGT", 22: "A-00583-FGT", 23: "A-00585-FGT", 24: "SW00117",
	25: "SW00107", 26: "SW00111", 27: "SW00111", 28: "SW00111", 29: "SW00111", 30: "SW00111",
	31: "SW00142", 32: "SW00117", 33: "SW00127", 34: "SW00127", 35: "SW00113",
	41: "SW00138", 42: "SW00138", 43: "SW00112", 44: "SW00111", 45: "SW00111",
	46: "SW00142", 47: "SW00142", 48: "SW00142", 49: "SW00106", 50: "SW00106", 51: "SW00106",
	52: "SW00141", 53: "SW00141", 54: "SW00126", 55: "SW00126", 56: "SW00126",
	58: "SW00106", 59: "SW00111", 60: "SW00111", 61: "SW00146", 62: "SW00146",
	65: "SW00111", 66: "SW00111", 67: "SW00139", 68: "SW00127", 69: "SW00142",
	70: "A-00578-L", 71: "A-00578-R", 77: "SW00111", 78: "SW00111", 79: "SW00111", 80: "SW00111",
}
# PinMAME's per-game capInvSw10 mask (src/wpc/capgames.c), the mask bbb109/bbb108 share
# (both INITGAME/INITGAMEFF calls pass gameno=10): {0, 0x00, 0x01, 0x78, 0x00, 0x00, 0x01},
# indexed by internal switch column 0-6 (column 7-8 implicitly 0, C tail zero-fill).
# col2=0x01 -> bit0=row0 -> address 25; col3=0x78=0b01111000 -> bits3-6=row3-6 -> addresses
# 36,37,38,39; col6=0x01 -> bit0=row0 -> address 57.
PINMAME_NORMALIZED_OPTO_SWITCHES = {25, 36, 37, 38, 39, 57}
# Manual positively documents these four by opto receiver/transmitter part number
# (A0015604-4R / A0015702-4R, matching the Opto Boards page); 25 and 57 have a blank
# "Switch Part Number" cell (consistent with no mechanical switch fitted) but the manual's
# own Opto Receiver/Xmtr P/N columns are illegible for every row except 36-39 (a uniform
# scan/print defect, not a deliberate shading convention -- see switch-locations.md).
CONFIRMED_OPTO_PART_NUMBER = {36, 37, 38, 39}
OPTO_RECEIVER_PART = "A0015604-4R"
OPTO_XMTR_PART = "A0015702-4R"
# Blank "Switch Part Number" cell with no legible opto part -- consistent with opto
# construction (no mechanical switch fitted) but not independently confirmed by part number.
BLANK_SWITCH_PART = {25, 57}

SWITCH_TYPE = {
	21: "microswitch", 22: "microswitch", 23: "microswitch", 24: "microswitch",
	25: "opto", 26: "microswitch", 27: "microswitch", 28: "microswitch", 29: "microswitch",
	30: "microswitch", 31: "microswitch", 32: "microswitch",
	33: "microswitch", 34: "microswitch", 35: "microswitch",
	36: "opto", 37: "opto", 38: "opto", 39: "opto",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch",
	45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	49: "microswitch", 50: "microswitch", 51: "microswitch", 52: "microswitch",
	53: "microswitch", 54: "microswitch", 55: "microswitch", 56: "microswitch",
	57: "opto", 58: "microswitch", 59: "microswitch", 60: "microswitch",
	61: "microswitch", 62: "microswitch", 65: "microswitch", 66: "microswitch",
	67: "microswitch", 68: "microswitch", 69: "microswitch", 70: "microswitch",
	71: "microswitch", 77: "microswitch", 78: "microswitch", 79: "microswitch", 80: "microswitch",
}

# vpmTimer.PulseSw / momentary callers in the retained script (src=script.vbs).
PULSED_SWITCHES = {25, 41, 42, 54, 55, 56}
# Trigger/HitTarget/Kicker/Spinner/Wall object each switch resolves to (from
# review-artifacts/big-bang-bar/vpx-geometry.txt), normalized x/y already computed by the
# extraction (x/952, y/2162, rounded to 6 places).
SWITCH_POSITIONS: dict[int, list[tuple[float, float]]] = {
	17: [(0.106602, 0.611911)], 18: [(0.115986, 0.585663)], 19: [(0.125458, 0.559367)],
	20: [(0.134723, 0.532262)],
	21: [(0.218323, 0.44073)], 22: [(0.363966, 0.424006)], 23: [(0.35455, 0.396394)],
	24: [(0.231843, 0.325462)], 25: [(0.113601, 0.348638)], 26: [(0.069855, 0.153751)],
	27: [(0.203484, 0.173696)], 28: [(0.371375, 0.10952)], 29: [(0.476401, 0.107483)],
	30: [(0.5877, 0.10275)], 31: [(0.06224, 0.129192)], 32: [(0.427824, 0.060041)],
	33: [(0.285743, 0.848334)], 34: [(0.618202, 0.84836)],
	35: [(0.501755, 0.95971)], 36: [(0.835873, 0.863827)], 37: [(0.755261, 0.885004)],
	38: [(0.680011, 0.908394)], 39: [(0.595908, 0.933245)],
	41: [(0.229376, 0.735796)], 42: [(0.674001, 0.733646)],
	43: [(0.940669, 0.888357)], 44: [(0.05624, 0.795441)], 45: [(0.12984, 0.742781)],
	46: [(0.210707, 0.705074)], 47: [(0.210707, 0.728646)], 48: [(0.209462, 0.751396)],
	49: [(0.444456, 0.336556)], 50: [(0.497771, 0.327576)], 51: [(0.550396, 0.318153)],
	52: [(0.460986, 0.31988)], 53: [(0.515982, 0.31053)],
	54: [(0.585404, 0.178991)], 55: [(0.526188, 0.267465)], 56: [(0.380918, 0.20046)],
	57: [(0.71318, 0.067239)],
	58: [(0.708865, 0.130149)],
	59: [(0.855848, 0.159649)], 60: [(0.870128, 0.0691)], 61: [(0.808287, 0.030843)],
	62: [(0.876093, 0.06363)], 65: [(0.773654, 0.742016)], 66: [(0.849492, 0.742471)],
	67: [(0.844337, 0.521704)], 68: [(0.618202, 0.84836)],
	69: [(0.945941, 0.313365)], 70: [(0.877041, 0.371875)], 71: [(0.946006, 0.39118)],
	77: [(0.690652, 0.315622)], 78: [(0.715059, 0.281322)], 79: [(0.752141, 0.323543)],
	80: [(0.777439, 0.288554)],
}
SWITCH_PROJECTIONS = {
	25: "Projected onto the Spinner table object's own center (Spinner.sw25); a physical spinner has no separate fixed sensor position.",
	57: "Projected onto the rotating Alien mechanism's own anchor (Primitive Alien1_BM_Lit_Room): the retained script's ALockTimer_timer reads a single 0-31 motor-position counter and toggles this one opto through a repeating home/quarter/half/three-quarter-turn notch pattern, not a fixed playfield sensor object -- the same pattern established for Monster Bash's Dracula-position optos.",
	33: "Projected onto the LeftFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolLFlipper with no separate sensor object.",
	34: "Projected onto the RightFlipper table object's own center; the retained script sets this synthetic EOS switch directly inside Sub SolRFlipper with no separate sensor object.",
	68: "Projected onto the RightFlipper table object's own center, the same object switch 34 projects onto: the retained script sets both switches together inside Sub SolRFlipper with no separate Upper Right Flipper EOS sensor object modeled.",
	35: "Projected onto the same Kicker object as the Outhole coil (solenoid 1): the manual's Switch Locations table names Ref.35 \"Outhole\" and the retained script kicks the ball resting on this object from Sub SolTrough.",
	41: "Projected onto the Wall.LeftSlingShot object's own drag-point centroid; resolved via the retained script's LeftSlingShot_Slingshot event sub rather than a differently-named sw41 object.",
	42: "Projected onto the Wall.RightSlingShot object's own drag-point centroid; resolved via the retained script's RightSlingShot_Slingshot event sub rather than a differently-named sw42 object.",
	54: "Projected onto the Bumper2 table object's own center; resolved via the retained script's Bumper2_Hit event sub, which pulses this switch.",
	55: "Projected onto the Bumper3 table object's own center; resolved via the retained script's Bumper3_Hit event sub.",
	56: "Projected onto the Bumper1 table object's own center; resolved via the retained script's Bumper1_Hit event sub.",
}

# --- Manual "Solenoids, Motors, & Flashers" (printed page 82) and schematic sheet 7's own
# "DEVICE # & DESCRIPTION" table (the authoritative per-device source; see
# evidence/excerpts/capcom.big-bang-bar.1996/solenoid-schematic-device-table.md).
SOLENOID_LABELS = {
	1: "Outhole", 2: "Trough", 3: "Knocker", 4: "Left Slingshot", 5: "Right Slingshot",
	6: "Kickback", 7: "4-Bank Reset", 8: "Lower Lock Post", 9: "Left Flipper",
	10: "Right Flipper", 11: "Upper Right Flipper", 12: "Eject Hole",
	13: "Island Diverter", 14: "Ramp Diverter 1", 15: "Ramp Diverter 2", 16: "Alien Lock Post",
	17: "3-Bank Reset", 18: "Star Bumper Left", 19: "Star Bumper Middle",
	20: "Star Bumper Right", 21: "Backbox Left Flasher",
	22: "Tube Dancer & Backbox Right Flasher", 23: "Dance Floor Flasher",
	24: "Eject Hole Flasher", 25: "Aliens Flasher", 26: "Lower Lock Flasher",
	27: "Orbit Gate Left", 28: "Orbit Gate Right", 29: "1-Bank Reset",
	30: "Tube Dancer Motor", 31: "Aliens Forward Motor", 32: "Aliens Reverse Motor",
}
SOLENOID_PART_NUMBERS = {
	1: "CL00109", 2: "CL00109", 3: "CL00109", 4: "CL00109", 5: "CL00109", 6: "CL00109",
	7: "CL00109", 8: "CL00109", 9: "CL00109", 10: "CL00109", 11: "CL00109", 12: "CL00109",
	13: "CL00112", 14: "CL00109", 15: "CL00109", 16: "CL00109", 17: "CL00109",
	18: "CL00109", 19: "CL00109", 20: "CL00109", 21: "LP00101", 22: "CL00109",
	23: "LP00101", 24: "LP00101", 25: "LP00101", 26: "LP00101", 27: "CL00112",
	28: "CL00112", 29: "CL00109", 30: "MR00108", 31: "MR00108", 32: "MR00108",
}
# CORE_MODOUT_BULB_89_20V_DC_WPC per-game override (src/wpc/capcom.c MACHINE_INIT(cc),
# strncasecmp(gn,"bbb",3) branch): core_set_pwm_output_type(CORE_MODOUT_SOL0+21-1,6,...) --
# addresses 21-26 are flasher-bulb driver type, confirmed by schematic sheet 7's own bulb
# symbol shapes for 21,23,24,25,26 and the shared bulb-shaped pair at 22.
FLASHER_SOLENOIDS = {21, 22, 23, 24, 25, 26}
MOTOR_SOLENOIDS = {30, 31, 32}
GATE_SOLENOIDS = {13, 27, 28}
SOLENOID_CALLBACKS = {
	1: "SolTrough (sw35.kick 57,20)", 2: "SolRelease (sw36.kick 90,10)",
	3: 'vpmSolSound SoundFX("knocker",...) -- sound only, no table object',
	4: 'SolCallback(4) commented out ("LeftSling); passive rubber slingshot, no coil object in the retained table',
	5: 'SolCallback(5) commented out ("RightSling); passive rubber slingshot, no coil object',
	6: "SolKickBack (kickback.Fire / .PullBack)", 7: "sol4Bank (DTRaise 17,18,19,20)",
	8: "SolLowerLockPin (MissionLockPin.IsDropped)",
	9: 'SolCallback(9) commented out ("SolLFlipper); native address unbound, see conflict.flipper-mirror-address-left-right-naming',
	10: 'SolCallback(10) commented out ("SolRFlipper); native address unbound, see conflict.flipper-mirror-address-left-right-naming',
	11: 'SolCallback(11) commented out ("SolURFlipper); unbound anywhere in the retained script',
	12: "bsRHole.SolOut (cvpmBallStack helper wrapping sw67)",
	13: "SolLRDIvert (DivLR.IsDropped)", 14: "SolRDivert1 (DivTubef.RotateToEnd/DivTube.isDropped)",
	15: "SolRDivert2 (DivTube2f.RotateToEnd/DivTube2.isDropped)",
	16: "SolRDivert3 (AliensLockPin.IsDropped)", 17: "sol3Bank (DTRaise 49,50,51)",
	18: 'SolCallback(18) commented out ("Left Bumper); candidate Bumper1, order-inferred only',
	19: 'SolCallback(19) commented out ("Middle Bumper); candidate Bumper2, order-inferred only',
	20: 'SolCallback(20) commented out ("Right Bumper); candidate Bumper3, order-inferred only',
	21: "Flash1 (Lampz.state(161), Light F21)", 22: "Flash2 (Lampz.state(162), Light F22)",
	23: "Flash3 (Lampz.state(163), Light F23)", 24: "Flash4 (Lampz.state(164), Light F24)",
	25: "Flash5 (Lampz.state(165), Light F25)", 26: "Flash6 (Lampz.state(166), Light F26)",
	27: "GateLeft (GateL.Open=true, auto-closes after 1000ms)",
	28: "GateRight (GateR.Open=true, auto-closes after 1000ms)",
	29: "sol1Bank (DTRaise 58)", 30: "solDancer (dancerT.enabled, rotx/roty wobble loop)",
	31: "SolAlienForward (sets 'forward' flag consumed by ALockTimer_timer)",
	32: "SolAlienReverse (sets 'reverse' flag, same mechanism as 31)",
}
SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.501755, 0.95971)], 2: [(0.835873, 0.863827)],
	6: [(0.059848, 0.87525)],
	7: [(0.106602, 0.611911), (0.115986, 0.585663), (0.125458, 0.559367), (0.134723, 0.532262)],
	8: [(0.20852, 0.766107)],
	12: [(0.844337, 0.521704)], 13: [(0.947213, 0.371481)],
	16: [(0.862307, 0.018598)],
	17: [(0.444456, 0.336556), (0.497771, 0.327576), (0.550396, 0.318153)],
	18: [(0.585404, 0.178991)], 19: [(0.380918, 0.20046)], 20: [(0.526188, 0.267465)],
	21: [(0.062763, 0.088922)], 22: [(0.252177, 0.13264)], 23: [(0.495536, 0.215657)],
	24: [(0.873687, 0.493178)], 25: [(0.942772, 0.058572)], 26: [(0.150773, 0.80503)],
	27: [(0.289968, 0.047017)], 28: [(0.671092, 0.034329)],
	29: [(0.708865, 0.130149)],
	30: [(0.252247, 0.132496)],
	31: [(0.71318, 0.067239), (0.782786, 0.11226)],
	32: [(0.71318, 0.067239), (0.782786, 0.11226)],
	45: [(0.285743, 0.848334)], 47: [(0.618202, 0.84836)],
}
# Ramp Diverter 1/2 (solenoids 14/15) each drive a rotating Flipper-type gate arm
# (DivTubeF/DivTube2f, near the front apron) plus one or two drop-wall panels
# (DivTube/DivTube1, DivTube2, near the rear/top) under the SAME script name family; the
# retained extraction's raw coordinates for the two halves of each mechanism are wildly
# inconsistent (front apron vs rear/top), so neither half is promoted to a validated
# placement -- see conflict.ramp-diverter-geometry-inconsistent below.

VIRTUAL_SOLENOID_LABELS = {
	33: "Upper Right Flip Power Mirror", 34: "Unused Upper Right Flip Hold Mirror",
	35: "Eject Hole Position Mirror (Mislabeled Upper Left Flip Power)",
	36: "Unused Upper Left Flip Hold Mirror",
	37: "Unused WPC-style LPDC Output 37", 38: "Unused WPC-style LPDC Output 38",
	39: "Unused WPC-style LPDC Output 39", 40: "Unused WPC-style LPDC Output 40",
	41: "Unused WPC-style LPDC Mirror 41", 42: "Unused WPC-style LPDC Mirror 42",
	43: "Unused WPC-style LPDC Mirror 43", 44: "Unused WPC-style LPDC Mirror 44",
	45: "Left Flipper Power Mirror", 46: "Unused Lower Right Flip Hold Mirror",
	47: "Right Flipper Power Mirror", 48: "Unused Lower Left Flip Hold Mirror",
	49: "Unused Platform Gap 49", 50: "Unused Platform Gap 50",
	51: "Fast-Flips Game On/Off Diagnostic Channel",
}
VIRTUAL_SOLENOID_NOTES = {
	33: (
		"Mirror of physical solenoid 11 (Upper Right Flipper): src/wpc/capcom.c io_w case "
		"0x20000d writes core_write_pwm_output(CORE_MODOUT_SOL0+sURFlipPow-1,1,(soldata>>10)&0x01), "
		"a genuine flipper-to-flipper correspondence (both name the Upper Right Flipper). It "
		"receives live data whenever address 11 does, but address 11 itself has no live "
		"SolCallback binding anywhere in the retained script (SolCallback(11)=\"SolURFlipper\" is "
		"commented out), so this address is always zero during actual play with this table."
	),
	34: "sLRFlip (CORE_FIRSTUFLIPSOL+1=34, the 'hold' half of the upper-right pair); src/wpc/capcom.c io_w never writes any PWM value to this address for the cc family, so it is permanently zero regardless of what fires on address 11 or 33.",
	35: (
		"src/wpc/capcom.c's io_w mirror code unconditionally treats physical addresses 9/10/11/12 "
		"as the four flipper-power circuits and writes address 12's live state into sULFlipPow=35 "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sULFlipPow-1,1,(soldata>>11)&0x01)) -- but Big "
		"Bang Bar wires physical address 12 to Eject Hole (S12, confirmed by both the manual and "
		"schematic sheet 7), not an upper-left flipper; this machine has no upper-left flipper "
		"circuit anywhere in the S1-S32 table. Address 35 therefore mirrors the Eject Hole coil's "
		"own state under PinMAME's generic 'Upper Left Flip Power' name purely as an accident of "
		"the mirror code's fixed positional assumption, not a genuine flipper mirror; see "
		"conflict.solenoid-35-eject-hole-mirror-mislabeled."
	),
	36: "sULFlip (CORE_FIRSTUFLIPSOL+3=36, the 'hold' half of the upper-left pair); never written by cc's io_w for any address in this range, permanently zero.",
	45: (
		"sLRFlipPow (CORE_FIRSTLFLIPSOL+0=45). src/wpc/capcom.c io_w case 0x20000d mirrors "
		"physical solenoid 9 (S9, 'L. Flipper') into this address "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sLRFlipPow-1,1,(soldata>>8)&0x01)) -- the only "
		"live source of data for this address. The retained script's active "
		"SolCallback(sLRFlipper)=\"SolRFlipper\" binding invokes the visual/sound handler named "
		"for the RIGHT flipper on an address that mirrors the LEFT physical circuit; see "
		"conflict.flipper-mirror-address-left-right-naming."
	),
	47: (
		"sLLFlipPow (CORE_FIRSTLFLIPSOL+2=47). src/wpc/capcom.c io_w case 0x20000d mirrors "
		"physical solenoid 10 (S10, 'R. Flipper') into this address "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sLLFlipPow-1,1,(soldata>>9)&0x01)) -- the only "
		"live source of data for this address. The retained script's active "
		"SolCallback(sLLFlipper)=\"SolLFlipper\" binding invokes the visual/sound handler named "
		"for the LEFT flipper on an address that mirrors the RIGHT physical circuit; see "
		"conflict.flipper-mirror-address-left-right-naming."
	),
	37: "WPC-style LPDC output range (CORE_FIRSTUFLIPSOL..CORE_FIRSTLFLIPSOL-1=37-44); src/wpc/capcom.c's io_w only ever writes addresses 1-32 directly and never references this range at all, unlike WPC-95's genuine LPDC duplication. Permanently unused address space on every cc-family driver.",
	38: "See address 37; permanently unused.", 39: "See address 37; permanently unused.",
	40: "See address 37; permanently unused.", 41: "See address 37; permanently unused.",
	42: "See address 37; permanently unused.", 43: "See address 37; permanently unused.",
	44: "See address 37; permanently unused.",
	46: "sLRFlip (CORE_FIRSTLFLIPSOL+1=46, the 'hold' half of the lower-right pair); src/wpc/capcom.c io_w never writes this address, permanently zero.",
	48: "sLLFlip (CORE_FIRSTLFLIPSOL+3=48, the 'hold' half of the lower-left pair); never written, permanently zero.",
	49: "CORE_FIRSTCUSTSOL-2=49; no cc-family driver references this address (the CORE_FIRSTSIMSOL=49 convention documented on other generations' profiles is not exercised by the Capcom driver, which has its own simulator-address scheme). Unused platform gap.",
	50: "CORE_FIRSTCUSTSOL-1=50; unused platform gap immediately before the first custom-solenoid address.",
	51: (
		"CORE_FIRSTCUSTSOL=51 (src/wpc/core.h); published only by the bbb109 driver (INITGAMEFF, "
		"hw.custSol=1) via a name##_getsol callback that reads a live RAM flag rather than any "
		"physical driver-board circuit (src/wpc/capgames.c INITGAMEFF; src/wpc/capcom.c "
		"MACHINE_INIT(cc), CORE_MODOUT_SOL_CUSTOM comment 'GameOn solenoid for Fast Flips'). The "
		"retained script's SolCallback(51)=\"SolGameOn\" toggles a GameStateOn flag gating whether "
		"the flipper callbacks fire at all. bbb108 (INITGAME, hw.custSol=0) does not publish this "
		"address."
	),
}

# --- Lamp matrix (manual printed page 81, "CABINET, PLAYFIELD, & BACKBOX LAMPS"). Test-ref
# column/row/bank notation converted to the public PinMAME address by the same arithmetic the
# retained script's Lampz.MassAssign bindings confirm: bank A address=(col-1)*8+row (1-64);
# bank B address=64+(col-1)*8+row (65-128). (label, bulb, part) as printed; entries omitted
# here are the eighteen positions the table itself prints "UNUSED".
LAMP_ROWS_BANK_A = [
	(1, 1, "Coin Door 1&2", "259", "LP00113"), (1, 2, "Coin Door 3&4", "259", "LP00113"),
	(1, 3, "Start", "555", "LP00100"),
	(2, 1, "4-Bank G.I. 1", "44", "LP00104"), (2, 2, "4-Bank G.I. 2", "44", "LP00104"),
	(2, 3, "4-Bank G.I. 3", "44", "LP00104"), (2, 4, "L. Slingshot G.I. 1", "44", "LP00104"),
	(2, 6, "L. Flipper G.I. 1", "44", "LP00104"),
	(3, 1, "U.R. Flipper G.I. 1", "44", "LP00104"), (3, 2, "Eject Hole G.I. 1", "44", "LP00104"),
	(3, 3, "Spaceship G.I. 1", "44", "LP00104"), (3, 4, "Spaceship G.I. 2", "44", "LP00104"),
	(3, 5, "R. Slingshot G.I. 1", "44", "LP00104"), (3, 6, "R. Slingshot G.I. 2", "44", "LP00104"),
	(3, 7, "R. Flipper G.I. 1", "44", "LP00104"), (3, 8, "R. Flipper G.I. 2", "44", "LP00104"),
	(4, 1, "Tube G.I. 1", "44", "LP00104"), (4, 2, "Tube G.I. 2", "44", "LP00104"),
	(4, 3, "Tube G.I. 3", "44", "LP00104"), (4, 4, "Tube G.I. 4", "44", "LP00104"),
	(4, 5, "Tube G.I. 5", "44", "LP00104"), (4, 6, "L. Orbit Chase 1", "44", "LP00104"),
	(4, 7, "L. Orbit Chase 2", "44", "LP00104"), (4, 8, "L. Orbit Chase 3", "44", "LP00104"),
	(5, 1, "Hoot G.I. 1", "44", "LP00104"), (5, 2, "Hoot G.I. 2", "44", "LP00104"),
	(5, 3, "Hoot G.I. 3", "44", "LP00104"), (5, 4, "Hoot G.I. 4", "44", "LP00104"),
	(5, 5, "Alien G.I. 1", "44", "LP00104"), (5, 6, "Alien G.I. 2", "44", "LP00104"),
	(5, 7, "Alien G.I. 3", "44", "LP00104"), (5, 8, "Captive G.I. 1", "44", "LP00104"),
	(6, 1, "R. Orbit Chase 1", "44", "LP00104"), (6, 2, "R. Orbit Chase 2", "44", "LP00104"),
	(6, 3, "R. Orbit Chase 3", "44", "LP00104"), (6, 4, "Alien Lock Left", "44", "LP00104"),
	(6, 5, "Alien Lock Right", "44", "LP00104"),
	(7, 1, 'Rollover "B"', "44", "LP00104"), (7, 2, 'Rollover "A"', "44", "LP00104"),
	(7, 3, 'Rollover "R"', "44", "LP00104"), (7, 4, "Tube Sign X-Ball", "44", "LP00104"),
	(7, 5, "Tube Sign 10 Mill", "44", "LP00104"), (7, 6, "Tube Sign Jackpot", "44", "LP00104"),
	(8, 1, "(Electro) Ramp 1", "44", "LP00104"), (8, 2, "(Electro) Ramp 2", "44", "LP00104"),
	(8, 3, "(Electro) Ramp 3", "44", "LP00104"),
	(8, 6, "(Electro) Black Light", "44", "LP00109"),
]
LAMP_ROWS_BANK_B = [
	(1, 1, "Bonus 2X", "44", "LP00104"), (1, 2, "Bonus 3X", "44", "LP00104"),
	(1, 3, "Mode: Underground", "44", "LP00104"), (1, 4, "Mode: Big Bang", "555", "LP00100"),
	(1, 5, "Mode: Bar Room Brawl", "555", "LP00100"),
	(1, 6, "Mode: Ray's Ball Busters", "555", "LP00100"),
	(1, 7, "Mode: Looped In Space", "555", "LP00100"), (1, 8, "Shoot Again", "555", "LP00100"),
	(2, 1, "Mode: Babe Scanner", "44", "LP00104"), (2, 2, "Mode: Chase Waitress", "44", "LP00104"),
	(2, 3, "Shoot: Cosmic Dartz", "44", "LP00104"),
	(2, 4, "Special (Outlane R.)", "555", "LP00100"), (2, 5, "Inlane Right", "555", "LP00100"),
	(2, 6, "Bonus 5X", "44", "LP00104"), (2, 7, "Bonus 4X", "555", "LP00100"),
	(2, 8, "Mode: Tube Dancer", "555", "LP00100"),
	(3, 1, "Shoot: Left Orbit", "555", "LP00100"), (3, 2, "Shoot: Babe Scanner", "555", "LP00100"),
	(3, 3, "4-Bank Mars", "555", "LP00100"), (3, 4, "4-Bank Pythos", "555", "LP00100"),
	(3, 5, "4-Bank Venus", "555", "LP00100"), (3, 6, "4-Bank Mercury", "555", "LP00100"),
	(3, 7, "Free Shot (Outlane L.)", "44", "LP00104"), (3, 8, "Inlane Left", "44", "LP00104"),
	(4, 1, "Mode: Cosmic Dartz", "44", "LP00104"), (4, 2, "Mode: Tour De Bar", "44", "LP00104"),
	(4, 3, "Mode: Mosh A Go-Go", "44", "LP00104"), (4, 4, "Mode: Happy Hour", "44", "LP00104"),
	(4, 5, "Mode: Extra Ball", "44", "LP00104"), (4, 6, "Mode: Get Lucky", "44", "LP00104"),
	(4, 7, "Mode: Luna Palooza", "44", "LP00104"),
	(5, 1, "Ramp Jackpot", "44", "LP00104"), (5, 2, "Ramp Standup Left", "44", "LP00104"),
	(5, 3, "Ramp Standup Right", "44", "LP00104"), (5, 4, "Ramp Standup Side", "44", "LP00104"),
	(5, 5, "Double Jackpot", "44", "LP00104"), (5, 6, "Shoot: Tour De Bar", "555", "LP00100"),
	(5, 7, "Shoot: Underground 1", "555", "LP00100"), (5, 8, "Qualify Mode", "44", "LP00104"),
	(6, 1, "Captive: Left 4", "555", "LP00100"), (6, 2, "Captive: Left 3", "555", "LP00100"),
	(6, 3, "Captive: Left 2", "555", "LP00100"), (6, 4, "Captive: Left 1", "555", "LP00100"),
	(6, 5, "Captive: Right 4", "555", "LP00100"), (6, 6, "Captive: Right 3", "555", "LP00100"),
	(6, 7, "Captive: Right 2", "555", "LP00100"), (6, 8, "Captive: Right 1", "555", "LP00100"),
	(7, 1, "3-Bank Uranus", "44", "LP00104"), (7, 2, "3-Bank Neptune", "44", "LP00104"),
	(7, 3, "3-Bank Pluto", "44", "LP00104"), (7, 4, "Shoot: Right Orbit", "555", "LP00100"),
	(7, 5, "D.J. Eyes G.I.", "555", "LP00100"), (7, 6, "Shoot: Luna Palooza", "44", "LP00104"),
	(7, 7, "Island: Lock Ready", "44", "LP00104"), (7, 8, "Island: Mode Ready", "44", "LP00104"),
	(8, 1, "Shoot: Underground 2", "44", "LP00104"), (8, 2, "Star Bumper Left", "555", "LP00100"),
	(8, 3, "Star Bumper Middle", "555", "LP00100"), (8, 4, "Star Bumper Right", "555", "LP00100"),
	(8, 5, "Dance Floor", "44", "LP00104"), (8, 6, "Shoot: Extra Ball", "555", "LP00100"),
	(8, 7, "Shoot: Big Bang", "555", "LP00100"), (8, 8, "U.R. Flipper G.I.2", "44", "LP00104"),
]
LAMP_UNUSED_BANK_A = {(1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 5), (2, 7), (2, 8),
	(6, 6), (6, 7), (6, 8), (7, 7), (7, 8), (8, 4), (8, 5), (8, 7), (8, 8)}
LAMP_UNUSED_BANK_B = {(4, 8)}


def lamp_address(bank: str, column: int, row: int) -> int:
	base = 0 if bank == "A" else 64
	return base + (column - 1) * 8 + row


LAMP_LABELS: dict[int, tuple[str, str, str]] = {}
for _col, _row, _label, _bulb, _part in LAMP_ROWS_BANK_A:
	LAMP_LABELS[lamp_address("A", _col, _row)] = (_label, _bulb, _part)
for _col, _row, _label, _bulb, _part in LAMP_ROWS_BANK_B:
	LAMP_LABELS[lamp_address("B", _col, _row)] = (_label, _bulb, _part)
LAMP_UNUSED_ADDRESSES = {lamp_address("A", c, r) for c, r in LAMP_UNUSED_BANK_A} | {
	lamp_address("B", c, r) for c, r in LAMP_UNUSED_BANK_B
}

# Object positions from review-artifacts/big-bang-bar/vpx-geometry.txt (Lampz.MassAssign(N)
# = L<N> in the retained script; normalized x/952, y/2162). Three used addresses (3, 38,
# 125) have no Lampz.MassAssign entry at all in the retained table -- confirmed absent by an
# independent re-check of every gameitems/*.json filename -- and are deliberately omitted
# from this position table rather than assigned a coordinate.
LAMP_POSITIONS: dict[int, tuple[float, float]] = {
	1: (0.903003, 0.849605), 2: (1.404579, 1.081786), 9: (0.059856, 0.451509),
	10: (0.04778, 0.535578), 11: (0.05008, 0.628763), 12: (0.180504, 0.725154),
	14: (0.217308, 0.826695), 17: (0.889706, 0.462419), 18: (0.864444, 0.596312),
	19: (0.754818, 0.613627), 20: (0.666602, 0.618512), 21: (0.724267, 0.724989),
	22: (0.696089, 0.765251), 23: (0.751295, 0.806019), 24: (0.689279, 0.82653),
	25: (0.149153, 0.305581), 26: (0.277389, 0.270681), 27: (0.203042, 0.228505),
	28: (0.046201, 0.112265), 29: (0.068053, 0.031741), 30: (0.069758, 0.273134),
	31: (0.062184, 0.196057), 32: (0.098363, 0.120097), 33: (0.317321, 0.104225),
	34: (0.421576, 0.099907), 35: (0.536328, 0.09563), 36: (0.644345, 0.091544),
	37: (0.77823, 0.093346), 39: (0.943273, 0.059667), 40: (0.79686, 0.173909),
	41: (0.880381, 0.272261), 42: (0.927109, 0.199592), 43: (0.92965, 0.119817),
	44: (0.768468, 0.042665), 45: (0.944744, 0.081137), 49: (0.367689, 0.05075),
	50: (0.48028, 0.048698), 51: (0.592016, 0.04647), 52: (0.342155, 0.145303),
	53: (0.339765, 0.144853), 54: (0.343178, 0.144853), 57: (0.244109, 0.348185),
	58: (0.205349, 0.28074), 59: (0.16866, 0.21628), 62: (1.406105, 1.104979),
	65: (0.147726, 0.776616), 66: (0.208455, 0.795416), 67: (0.280809, 0.811051),
	68: (0.451392, 0.75685), 69: (0.450317, 0.789862), 70: (0.449796, 0.815156),
	71: (0.449268, 0.838972), 72: (0.451854, 0.875188), 73: (0.646282, 0.562258),
	74: (0.571762, 0.61343), 75: (0.762082, 0.563196), 76: (0.849115, 0.680505),
	77: (0.774299, 0.68032), 78: (0.756282, 0.775896), 79: (0.695016, 0.794802),
	80: (0.622323, 0.810679), 81: (0.164532, 0.44903), 82: (0.187535, 0.477623),
	83: (0.18556, 0.55622), 84: (0.174795, 0.583463), 85: (0.165779, 0.610267),
	86: (0.155953, 0.636838), 87: (0.055574, 0.715822), 88: (0.129689, 0.681298),
	89: (0.259744, 0.577409), 90: (0.363196, 0.549071), 91: (0.454552, 0.548748),
	92: (0.54802, 0.558707), 93: (0.319534, 0.609321), 94: (0.411993, 0.584683),
	95: (0.480076, 0.612996), 97: (0.312662, 0.473276), 98: (0.247992, 0.463076),
	99: (0.362434, 0.449188), 100: (0.405714, 0.409051), 101: (0.37596, 0.359386),
	102: (0.444372, 0.398476), 103: (0.518483, 0.425461), 104: (0.474962, 0.303103),
	105: (0.652335, 0.367477), 106: (0.637046, 0.388324), 107: (0.622133, 0.40922),
	108: (0.608498, 0.429533), 109: (0.71388, 0.376244), 110: (0.699528, 0.396845),
	111: (0.685258, 0.417314), 112: (0.669355, 0.438668), 113: (0.473351, 0.366144),
	114: (0.530774, 0.356273), 115: (0.589187, 0.346477), 116: (0.830555, 0.34098),
	117: (0.80812, 0.373845), 118: (0.772851, 0.406213), 119: (0.888516, 0.295416),
	120: (0.845144, 0.35238), 121: (0.480652, 0.150643), 122: (0.380839, 0.2009),
	123: (0.525051, 0.267565), 124: (0.586008, 0.178721), 126: (0.679244, 0.171843),
	127: (0.651828, 0.210395), 128: (0.892774, 0.333949),
}
# Lamp addresses out of the retained table's own 0..1 normalized bounds; kept as reported,
# never clipped or reassigned. Recorded here for transparency; excluded from validated
# placements below (see build_spatial_report's excluded_object_classes).
LAMP_OUT_OF_BOUNDS = {2, 62}
# Used lamp addresses with no resolvable VPX object (no Lampz.MassAssign(N) entry exists in
# the retained table for these three, independently re-checked against every
# gameitems/*.json filename, case-insensitive and zero-padded).
LAMP_USED_NO_GEOMETRY = {3, 38, 125}

# Diagnostic-LED column (nLamps-8 .. nLamps-1 = 129-136 for lampCol=9): only the first two
# positions are populated (src/wpc/capcom.c MACHINE_INIT(cc)).
DIAG_LED_LABELS = {129: "CPU Board Diagnostic LED", 130: "Sound Board Diagnostic LED"}
DIAG_LED_UNUSED = {131, 132, 133, 134, 135, 136}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Big Bang Bar retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Big Bang Bar extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Big Bang Bar retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Big Bang Bar retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Big Bang Bar retained extraction identity mismatch: "
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


def candidate(*source_refs: str) -> dict[str, Any]:
	return {"status": "candidate", "source_refs": list(source_refs)}


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
			"locator": "Pinned catalog driver records for the bbb108/bbb109 clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/capcom.c (file header hardware/lamp/switch/solenoid comment; "
				"SWITCH_UPDATE(cc), io_r/io_w, MACHINE_INIT(cc) including the strncasecmp(gn,\"bbb\",3) "
				"flasher-type block, cc_sw2m/cc_m2sw); src/wpc/capgames.c (capInvSw10, "
				"#define FLIP FLIP_SWNO(5,6)+FLIP_SOL(FLIP_LL|FLIP_LR|FLIP_UR|FLIP_UL), "
				"INITGAME(bbb108,...)/INITGAMEFF(bbb109,...,0x6234d)); src/wpc/core.h "
				"(core_tGameData hw field order, CORE_FIRSTUFLIPSOL=33, CORE_FIRSTLFLIPSOL=45, "
				"CORE_FIRSTCUSTSOL=51, sLRFlip/sLRFlipPow/sLLFlip/sLLFlipPow/sURFlip/sURFlipPow/"
				"sULFlip/sULFlipPow, CORE_MAXSWCOL=16, CORE_STDSWCOLS=12, CORE_FLIPPERSWCOL=11); "
				"src/wpc/core.c (core_getSw/core_setSw generic invSw application, core_updateSw "
				"synthetic flipper switch/EOS handling); src/libpinmame/libpinmame.h "
				"(PINMAME_HARDWARE_GEN enum: no Capcom entry exists, confirmed by core_tGameData.gen "
				"being the literal 0 in every cc-family INITGAME/INITGAMEFF expansion)"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/capcom.json",
			"revision": "repository",
			"locator": "Capcom cabinet/matrix/synthetic-flipper switch, 32-solenoid plus synthetic-mirror, and two-matrix lamp address rules, derived entirely from src/wpc/capcom.c/capcom.h/capgames.c",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/capcom.big-bang-bar.1996/ipdb/Capcom_1996_Big_Bang_Bar_Manual.pdf",
			"original_filename": "Capcom_1996_Big_Bang_Bar_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"138-page Adobe Paper Capture OCR'd scan of the Capcom Big Bang Bar operators manual "
				"(PM00131, issue date 08/07/96). PDF page number = printed page number + 4. Printed "
				"page 76 carries the Opto Boards parts page; printed page 82 carries the Solenoids, "
				"Motors, & Flashers location table; printed page 83 carries the Location of Switches "
				"& Optos table (cabinet 1-18, playfield matrix 19-80); printed page 81 carries the "
				"Cabinet, Playfield, & Backbox Lamps address table. Section on Playfield Mechanisms "
				"(printed 85-114) and the Game Diagnostics section (printed 34-44) supply mechanism "
				"and calibration-test corroboration."
			),
			"license": "NOASSERTION",
			"attribution": "Capcom Coin-Op, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.big-bang-bar.switch-locations",
					"locator": "PDF page 87, printed page 83, Location of Switches & Optos",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/switch-locations.md",
					"sha256": "f0b343c23695e10ea94c42a37e80229f36e622ee12d586292efa4fd5fc50e094",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.big-bang-bar.lamp-locations",
					"locator": "PDF page 85, printed page 81, Cabinet, Playfield, & Backbox Lamps",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-locations.md",
					"sha256": "e42b56a3cab198c0dd02b225af4ec6617fa879a1f2641b235f326badb43ea8df",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.big-bang-bar.solenoid-locations",
					"locator": "PDF page 86, printed page 82, Solenoids, Motors, & Flashers",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-locations.md",
					"sha256": "b4b65db7b910736ed230487d8d2c722c3d366928a537f43302f858044be7a4f4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.big-bang-bar.opto-boards",
					"locator": "PDF page 80, printed page 76, Opto Boards",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/opto-boards.md",
					"sha256": "2b8c6c1e686270510340d9368badc9ad51f15eca9afbd07f6d17aa63cbc43eba",
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/opto-boards.png",
					"image_sha256": "898aff92b068cadde41c7ca98630ddee97b0065ded5a2e77a8220d8de6a892b0",
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf PDF page 80, rendered at 300 dpi with pdftoppm, grayscale PNG",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": SCHEMATIC_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/capcom.big-bang-bar.1996/ipdb/Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf",
			"original_filename": "Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf",
			"sha256": SCHEMATIC_SHA256,
			"locator": (
				"12-page companion schematic set (PB-5 WIRING, drawn by B. Ziegler, dated 6/7/96), "
				"separately paginated from the operators manual. Sheet 2/12 (Driver Board Wiring) "
				"documents the SOL1-32 connector/wire-color layout; sheet 7/12 (Playfield Devices, "
				"Flashers, Wiring) carries the authoritative S1-S32 'DEVICE # & DESCRIPTION' table "
				"and per-device coil/bulb/motor symbol shapes. Sheets 3,6,8,9,10 cover switch/lamp "
				"wiring (cited only for the cabinet switch/lamp cross-check) and sheets 1,4,5,11,12 "
				"are out of this definition's scope (power/display/transformer/coin-door/printer)."
			),
			"license": "NOASSERTION",
			"attribution": "Capcom Coin-Op, Inc.",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.big-bang-bar.solenoid-schematic-device-table",
					"locator": "Sheet 7/12, \"DIAGRAM, PLFD DEVICES, FLASHERS, WIRING\", DEVICE # & DESCRIPTION table",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-schematic-device-table.md",
					"sha256": "7b02fbdacd91ee25a82b540f9ee8822c92f97261c3548cfefeab086b5be0d4ca",
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-schematic-device-table.png",
					"image_sha256": "647525cf95f2459d709c81810c4dbd586db92d363e733c3d2c5bc413fa689cb6",
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf sheet 7, rendered at 400 dpi with pdftoppm, cropped to the device-table legend, grayscale PNG",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered switch/lamp manual table used by "
				"this definition, together with a companion solenoid/schematic transcription "
				"(external:pinmame-review-artifacts/big-bang-bar/manual-transcription-solenoids.md, "
				f"SHA-256 {MANUAL_TRANSCRIPTION_SOLENOIDS_SHA256}) and the rendered PNG page cache "
				"under external:pinmame-manuals/rendered/capcom.big-bang-bar.1996/. The retained PDF "
				"is Adobe Paper Capture OCR'd but the text layer is unreliable on dense multi-column "
				"tables, so this transcription (read from rendered page images at 200-600 dpi) is the "
				"source of record."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/capcom/big-bang-bar-1996/source/Big%20Bang%20Bar%20%28Capcom%201996%29%20VPW%20v1.0.vpx",
			"original_filename": "Big Bang Bar (Capcom 1996) VPW v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPW v1.0 recreation of the physical machine. Exact playfield "
				f"bounds are {TABLE_BOUNDS} (confirmed against gamedata.json); normalized coordinates "
				"are x/952 and y/2162. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/capcom/big-bang-bar-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (289,215 bytes). Runtime and mechanism-causality '
				'authority: Const cGameName = "bbb109", Const UseSolenoids = 2, Const UseLamps = 0, '
				"the SolCallback table for solenoids 1-32 and 51 plus the symbolic sLRFlipper/"
				"sLLFlipper flipper-power bindings, the Controller.Switch and vpmTimer.PulseSw switch "
				"semantics for the trough/Alien/Tube-Dancer/drop-target state machines, and "
				"LampTimer_Timer's Controller.ChangedLamps -> Lampz.state dispatch, whose "
				"Lampz.MassAssign(N)=L<N> registrations in Sub LampzHelper are the address-to-object "
				"binding for every lamp placement in this definition."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/capcom/big-bang-bar-1996/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and SHA-256 "
				f"under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with "
				f"vpxtool from the retained table. Bounds are {TABLE_BOUNDS}. A companion note "
				f"(external:pinmame-review-artifacts/big-bang-bar/vpx-geometry.txt, SHA-256 "
				f"{VPX_GEOMETRY_NOTES_SHA256}) records every object resolved and every address "
				"searched but not found."
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

	for address in range(1, 17):
		label = CABINET_SWITCH_LABELS.get(address)
		unused = address in CABINET_SWITCH_UNUSED
		identifier = f"switch.cabinet-{address}"
		physical: dict[str, Any] = {"location": "cabinet"}
		part = CABINET_SWITCH_PARTS.get(address)
		if part:
			physical["part_number"] = part
		if address in CABINET_SWITCH_TYPE:
			physical["switch_type"] = CABINET_SWITCH_TYPE[address]
		notes = f"Printed cabinet switch Ref. {address}."
		if address in (1, 2, 3, 4):
			notes += " Footnoted '* SWITCH IS LOCATED IN CABINET' and '** NOT SERVICED SEPARATELY' -- integral to the coin acceptor mechanism, no discrete replaceable switch part."
		if address in (5, 6):
			notes += " CC_COMPORTS reserves this bit outside the CORE_SETKEYSW(...,0xcf,9) mask (src/wpc/capcom.c SWITCH_UPDATE(cc)) because FLIP_SWNO(5,6) (src/wpc/capgames.c) claims it as a real flipper-button switch rather than a keyboard-simulated cabinet input."
		if unused:
			notes += " CC_COMPORTS labels this bit a generic 'Unused #N' keyboard-simulation placeholder (src/wpc/capcoms.h); the manual confirms this specific game leaves the position genuinely unfitted."
		if address in (15, 16):
			notes += " Wired to this game's redemption/ticket hardware at a keyboard-simulation position CC_COMPORTS generically labels 'Unused' (src/wpc/capcoms.h); the printed part-number cell is blank."
		physical["notes"] = notes
		items.append(
			_device(
				identifier,
				label or f"Unused Cabinet Position {address}",
				"constant" if unused else "switch",
				"pinmame.input.switch",
				address,
				"unused" if unused else "used",
				(MANUAL_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				normally_closed=False,
				physical=physical,
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for address in range(17, 81):
		label = SWITCH_LABELS.get(address)
		unused = address in UNUSED_MATRIX_ADDRESSES
		identifier = f"switch.matrix-{address}"
		physical: dict[str, Any] = {}
		part = SWITCH_PARTS.get(address)
		if part:
			physical["part_number"] = part
		if address in SWITCH_TYPE:
			physical["switch_type"] = SWITCH_TYPE[address]
		notes = f"Printed switch-matrix Ref. {address}."
		if unused:
			notes += " Printed 'UNUSED' on the switch-matrix page."
		if address in CONFIRMED_OPTO_PART_NUMBER:
			notes += (
				f" Blank Switch Part Number cell (no mechanical switch); Opto Receiver P/N "
				f"{OPTO_RECEIVER_PART}, Opto Xmtr. P/N {OPTO_XMTR_PART}, matching the Opto Boards "
				"page's receiver/transmitter pair. PinMAME's per-game capInvSw10 mask "
				"(src/wpc/capgames.c) normalizes this address, so the public switch state is "
				"already inverted and must not be inverted again."
			)
		elif address in BLANK_SWITCH_PART:
			notes += (
				" Blank Switch Part Number cell (no mechanical switch fitted), consistent with "
				"opto construction, but this manual's Opto Receiver/Xmtr P/N columns are illegible "
				"for this row (a uniform scan/print defect affecting every row on this table except "
				"36-39, not a deliberate shading convention -- see switch-locations.md) so no opto "
				"part number can be positively cited. PinMAME's per-game capInvSw10 mask "
				"(src/wpc/capgames.c) does normalize this address; see coverage.missing=['polarity']."
			)
		if address in PULSED_SWITCHES:
			notes += " Set via vpmTimer.PulseSw in the retained script (momentary)."
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.switch", "value": str(address)}]
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
		if address in SWITCH_PROJECTIONS:
			extra["physical"]["notes"] += f" {SWITCH_PROJECTIONS[address]}"
		if unused:
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		elif address in SWITCH_POSITIONS:
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		refs = (MANUAL_SOURCE, CORE_SOURCE) if not label else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(
			_device(
				identifier,
				label or f"Unused Matrix Position {address}",
				"switch",
				"pinmame.input.switch",
				address,
				"unused" if unused else "used",
				refs,
				pulse=address in PULSED_SWITCHES,
				**extra,
			)
		)

	items.append(
		_device(
			"switch.dmd-synthetic-flipper-column",
			"PinMAME Synthetic Flipper Button/EOS Column",
			"virtual",
			"pinmame.input.switch",
			81,
			"unused",
			(CORE_SOURCE,),
			aliases=[{"namespace": "pinmame.switch", "value": "81"}],
			physical={
				"notes": (
					"Addresses 81-88 (internal 'col 11', CORE_FLIPPERSWCOL=11, src/wpc/core.h) are "
					"PinMAME's own synthetic flipper-button and stroke-timed EOS bits fabricated by "
					"core_updateSw, not real hardware. bbb's hw.flippers (FLIP_SWNO(5,6)+FLIP_SOL(FLIP_LL"
					"|FLIP_LR|FLIP_UR|FLIP_UL)) populates the lower-flipper button bits (81/82 LR EOS/BUT, "
					"83/84 LL EOS/BUT) and all four EOS bits (81,83,85,87) but no upper-flipper BUTTON "
					"bits (86,88 stay unset), since only two physical flipper buttons exist. This single "
					"placeholder device documents the whole synthetic column; individual bits are never "
					"exposed to a table script and have no playfield object."
				)
			},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	items.append(
		_device(
			"switch.unused-platform-column-10",
			"Unused Platform Switch Column 10",
			"virtual",
			"pinmame.input.switch",
			89,
			"unused",
			(CORE_SOURCE,),
			aliases=[{"namespace": "pinmame.switch", "value": "89"}],
			physical={
				"notes": (
					"Addresses 89-96 exist only because CORE_STDSWCOLS fixes every generation at 12 "
					"switch columns (src/wpc/core.h) regardless of what a driver uses; no cc-family "
					"driver reads or writes this column. Permanently zero, unused address space."
				)
			},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 33):
		label = SOLENOID_LABELS[address]
		identifier = output_id(label)
		kind = "flasher" if address in FLASHER_SOLENOIDS else "motor" if address in MOTOR_SOLENOIDS else "coil"
		physical: dict[str, Any] = {}
		part = SOLENOID_PART_NUMBERS.get(address)
		if part:
			physical["part_number"] = part
		notes = f"Manual/schematic Ref./S{address} ({label})."
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		if address == 22:
			notes += (
				" Schematic sheet 7 draws S22 feeding TWO device symbols in parallel from one "
				"connector pin (VIO/BLU, J20/J21 pin 6): the Tube Dancer effect and the Backbox "
				"Right flasher, resolving the manual's page-82 unnumbered 'BACKBOX RIGHT (FLASHER)' "
				"row (it shares this address with 'TUBE DANCER' rather than being a numbering gap). "
				"Both S22 symbols are drawn as the circular bulb shape used for lamps/flashers "
				"elsewhere on the sheet, not the coil symbol S1-S20/S27-S29 use -- yet the Tube Lady "
				"Assembly mechanism parts page shows a genuine coil (item 1A) as part of the same "
				"mechanism. This construction question is unresolved; see "
				"conflict.solenoid-22-shared-device-construction."
			)
		if address in (9, 10, 11):
			notes += (
				" Native SolCallback is commented out in the retained script; see "
				"conflict.flipper-mirror-address-left-right-naming."
			)
		if address in (4, 5):
			notes += " No coil object in the retained table; VPX models this as a passive rubber slingshot wall (see the corresponding switch's projection note)."
		if address in (18, 19, 20):
			notes += (
				" Bumper1/Bumper2/Bumper3 VPX-object correspondence is inferred only from the order "
				"SolCallback comments and Bumper1_Hit/Bumper2_Hit/Bumper3_Hit subs appear in the "
				"retained script, not independently confirmed from a per-bumper wiring page."
			)
		if address in (14, 15):
			notes += (
				" The retained table's rotating gate-arm object (DivTubef/DivTube2f, a Flipper-type "
				"primitive) and its associated drop-wall panel object(s) (DivTube/DivTube1, DivTube2) "
				"report wildly inconsistent raw positions (front-apron vs rear/top of the playfield) "
				"for what the script treats as one mechanism; neither half is promoted to a validated "
				"placement. See conflict.ramp-diverter-geometry-inconsistent."
			)
		if address == 3:
			notes += " Sound-only in the retained script (vpmSolSound); no table object."
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
		if address in (3, 4, 5):
			extra["spatial"] = not_applicable("no_physical_device", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address in (14, 15):
			pass  # Real physical devices with internally inconsistent retained-table geometry;
			# omit `spatial` entirely rather than invent a coordinate or a not_applicable reason
			# that doesn't fit (see conflict.ramp-diverter-geometry-inconsistent).
		elif address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		refs = (MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, SCHEMATIC_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))

	for address, label in VIRTUAL_SOLENOID_LABELS.items():
		identifier = output_id(label)
		availability = "used" if address in (33, 45, 47, 51) else "unused"
		roles = ["internal.duplicate.mirror"] if address in (33, 35, 45, 47) else ["internal.unused"]
		if address == 51:
			roles = ["internal.diagnostic"]
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
			"roles": roles,
			"physical": {"notes": VIRTUAL_SOLENOID_NOTES[address]},
		}
		if address in SOLENOID_POSITIONS:
			extra["spatial"] = located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		else:
			extra["spatial"] = not_applicable("virtual", CORE_SOURCE)
		items.append(
			_device(
				identifier,
				label,
				"virtual",
				"pinmame.output.solenoid",
				address,
				availability,
				(CORE_SOURCE, VPX_SCRIPT_SOURCE) if address in (35, 45, 47, 51) else (CORE_SOURCE,),
				**extra,
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 129):
		if address in LAMP_UNUSED_ADDRESSES:
			items.append(
				_device(
					f"lamp.matrix-{address}",
					f"Unused Matrix Position {address}",
					"lamp",
					"pinmame.output.lamp",
					address,
					"unused",
					(MANUAL_SOURCE,),
					aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
					physical={"notes": "Printed 'UNUSED' on the Cabinet, Playfield, & Backbox Lamps table."},
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue
		label_row = LAMP_LABELS.get(address)
		if label_row is None:
			# Not in the manual's printed table at all -- should not happen for 1-128,
			# but fail closed rather than silently invent a label.
			raise RuntimeError(f"Big Bang Bar lamp address {address} has no manual label or UNUSED marking")
		label, bulb, part = label_row
		identifier = f"lamp.matrix-{address}"
		physical: dict[str, Any] = {}
		if part:
			physical["part_number"] = part
		notes = f"Printed lamp-matrix address {address} ('{label}'), bulb type #{bulb}."
		physical["notes"] = notes
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}],
			"physical": physical,
		}
		if address in LAMP_USED_NO_GEOMETRY:
			extra["physical"]["notes"] += (
				" No Lampz.MassAssign(N) entry exists for this address in the retained table "
				"(independently re-checked against every gameitems/*.json filename); the manual "
				"documents this as a real, fitted device, but this recreation has no bound VPX "
				"object and therefore no coordinate."
			)
		elif address in LAMP_POSITIONS:
			position = LAMP_POSITIONS[address]
			if address in LAMP_OUT_OF_BOUNDS:
				extra["physical"]["notes"] += (
					f" The retained table's object (raw position far outside the {TABLE_BOUNDS} "
					"playfield bounds) normalizes outside 0..1; excluded from validated placement as "
					"a table-modeling anomaly rather than clamped or reassigned."
				)
			else:
				extra["spatial"] = located(identifier, "emitter", [position], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE), **extra))

	for address, label in DIAG_LED_LABELS.items():
		items.append(
			_device(
				f"lamp.diag-{address}",
				label,
				"lamp",
				"pinmame.output.lamp",
				address,
				"used",
				(CORE_SOURCE,),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={"notes": "PWM-integrated diagnostic LED (src/wpc/capcom.c MACHINE_INIT(cc), CORE_MODOUT_LED); reports ok/error state, not a player-visible playfield bulb."},
				spatial=not_applicable("cabinet_or_service", CORE_SOURCE),
			)
		)
	for address in sorted(DIAG_LED_UNUSED):
		items.append(
			_device(
				f"lamp.diag-unused-{address}",
				f"Unused Diagnostic Column Position {address}",
				"virtual",
				"pinmame.output.lamp",
				address,
				"unused",
				(CORE_SOURCE,),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={"notes": "core_set_pwm_output_type(...,CORE_MODOUT_NONE) for the six unused positions of the diagnostic column (src/wpc/capcom.c MACHINE_INIT(cc))."},
				spatial=not_applicable("unused", CORE_SOURCE),
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
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		item: dict[str, Any] = {
			"id": identifier,
			"label": label,
			"kind": kind,
			"actuators": actuators,
			"sensors": sensors,
			"behavior": behavior,
			"provenance": provenance(*refs),
		}
		if assembly_part_number:
			item["assembly_part_number"] = assembly_part_number
		return item

	return [
		mechanism(
			"mechanism.trough",
			"Outhole and Ball Trough",
			"kicker",
			[output_id("Outhole"), output_id("Trough")],
			["switch.matrix-35", "switch.matrix-36", "switch.matrix-37", "switch.matrix-38", "switch.matrix-39"],
			(
				"A drained ball settles on Outhole opto-adjacent switch 35 (SW00113, mechanical); "
				"Sub SolTrough kicks it (sw35.kick 57,20) into the four-position trough, sensed by "
				"opto switches 36-39 (Trough 1-4 Balls, A0015604-4R/A0015702-4R receiver/transmitter "
				"pair). The retained script's UpdateTroughTimer settles balls forward one position at "
				"a time (sw36.kick if sw37 empty, etc.) until they queue against switch 39. "
				"SolRelease (address 2) kicks the queued ball out to the shooter lane (switch 43)."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.4-bank-drop-targets",
			"4-Bank Drop Target",
			"drop_target_bank",
			[output_id("4-Bank Reset")],
			["switch.matrix-17", "switch.matrix-18", "switch.matrix-19", "switch.matrix-20"],
			(
				"Four standup-style drop targets (Mercury/Venus/Pythos/Mars, switches 17-20, SW00106) "
				"reset together off one coil (solenoid 7): the retained script's sol4Bank handler "
				"calls DTRaise on all four target objects in one pulse. The mechanism parts page "
				"(printed page 96) confirms one shared reset bar/coil for the bank, printed 'TYPICAL "
				"(4 REQUIRED)' for the target sub-assemblies themselves."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.3-bank-drop-targets",
			"3-Bank Drop Target",
			"drop_target_bank",
			[output_id("3-Bank Reset")],
			["switch.matrix-49", "switch.matrix-50", "switch.matrix-51"],
			(
				"Three standup-style drop targets (Uranus/Neptune/Pluto, switches 49-51, SW00106) "
				"reset together off one coil (solenoid 17, sol3Bank: DTRaise 49,50,51), matching the "
				"mechanism parts page's 'TYPICAL (3 REQUIRED)' callout for the target sub-assemblies "
				"sharing one reset mechanism."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.1-bank-drop-target",
			"1-Bank Drop Target",
			"drop_target_bank",
			[output_id("1-Bank Reset")],
			["switch.matrix-58"],
			"Single drop target (switch 58, SW00106) reset by solenoid 29 (sol1Bank: DTRaise 58).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.alien-mechanism",
			"Alien Mechanism",
			"rotary",
			[output_id("Aliens Forward Motor"), output_id("Aliens Reverse Motor"), output_id("Alien Lock Post")],
			["switch.matrix-57", "switch.matrix-61", "switch.matrix-62"],
			(
				"One reversible DC gearmotor (Alien Mech Assembly parts page, printed page 104: one "
				"motor item driving two gears on two independent shafts, each carrying one alien "
				"figure) drives both alien figures together through a 32-step position counter "
				"(retained script ALockTimer_timer, OldPos/NewPos 0-31). Switch 57 (Alien Motor, opto, "
				"blank switch part) toggles through a repeating home/quarter/half/three-quarter-turn "
				"notch pattern as the counter advances -- the diagnostic C2-02 Alien Motor calibration "
				"test independently confirms one motor calibrated at two power levels with a "
				"'Can't Find Home Position' failure mode tied to a dirty/misaligned double-notch "
				"encoder wheel opto, matching this switch's role. Solenoids 31/32 (Aliens Forward/"
				"Reverse) are this one gearmotor's two drive-direction outputs, not two independent "
				"motors. Solenoid 16 (Alien Lock Post) raises/lowers a separate ball-lock post sensed "
				"by switches 61/62 (Alien Lock Left/Right, SW00146); the retained script's sw61_Hit/"
				"sw62_Hit handlers set AlienLBall/AlienRBall lock-state flags independently of the "
				"rotating figures' own position."
			),
			MANUAL_SOURCE, SCHEMATIC_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.tube-dancer",
			"Tube Dancer",
			"motorized",
			[output_id("Tube Dancer Motor"), output_id("Tube Dancer & Backbox Right Flasher")],
			[],
			(
				"The Tube Lady Assembly parts page (printed page 108) shows one coil (item 1A) and a "
				"separate DC gearmotor (item 1F) driving a dancing figure inside a clear backbox tube "
				"via a rack/pinion or belt. The retained script models only the motor half: solDancer "
				"(solenoid 30) enables a continuous wobble-rotation timer (dancerT_timer, no discrete "
				"position and no switch) while enabled. The coil half's exact address and behavior are "
				"unresolved -- see conflict.solenoid-22-shared-device-construction."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.orbit-gates",
			"Orbit One-Way Gates",
			"gate",
			[output_id("Orbit Gate Left"), output_id("Orbit Gate Right")],
			["switch.matrix-26", "switch.matrix-27", "switch.matrix-59", "switch.matrix-60"],
			(
				"Two solenoid-operated one-way gates (Left Power Gate / Right Power Gate assembly "
				"pages, printed page 112) admit a ball into the outer/inner orbit loops while "
				"blocking return travel. The retained script's GateLeft/GateRight handlers open the "
				"gate for 1000ms on a solenoid pulse (solenoids 27/28) then auto-close."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
		mechanism(
			"mechanism.island-and-ramp-diverters",
			"Island and Ramp Diverters",
			"diverter",
			[output_id("Island Diverter"), output_id("Ramp Diverter 1"), output_id("Ramp Diverter 2")],
			["switch.matrix-31", "switch.matrix-69", "switch.matrix-70", "switch.matrix-71"],
			(
				"Three independent diverter solenoids (13 Island Diverter, 14 Ramp Diverter 1, 15 Ramp "
				"Diverter 2) each raise/lower a wall or rotate a gate arm to route a ball between the "
				"tube/island area and the ramp; the Left and Right Diverter Assembly parts page "
				"(printed page 102) documents one coil per diverter. The retained table's own drop-"
				"wall and rotating-arm object positions for 14/15 are internally inconsistent (see "
				"conflict.ramp-diverter-geometry-inconsistent) and neither is promoted to a validated "
				"placement."
			),
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-release-to-shooter-lane",
			"kind": "pulse",
			"source": output_id("Trough"),
			"destination": "switch.matrix-43",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.flipper-mirror-address-left-right-naming",
			"path": "outputs[binding.device=45,47]",
			"description": (
				"src/wpc/capcom.c's io_w mirrors physical solenoid 9 (S9, manual/schematic-confirmed "
				"'L. Flipper') into PinMAME's synthetic sLRFlipPow=45 address, and physical solenoid "
				"10 (S10, 'R. Flipper') into sLLFlipPow=47 -- the opposite left/right sense from "
				"PinMAME's own core.h naming ('Lower RIGHT Flip Power' mirrors the physical LEFT "
				"circuit, and vice versa). The driver's own source comment admits this: 'This should "
				"be removed as this push the legacy PinMAME specific mapping forward while it does "
				"not correspond to manuals or any other reference.' The retained script's active "
				"flipper bindings, SolCallback(sLRFlipper)=\"SolRFlipper\" and "
				"SolCallback(sLLFlipper)=\"SolLFlipper\", use symbolic VPX/VPinMAME automation "
				"constants whose exact numeric value this curation could not verify from any pinned "
				"source (neither src/wpc/core.h nor the two pinned VPX script corpora define "
				"'sLRFlipper' locally; it is presumably a COM-exposed constant from a library outside "
				"the pinned PinMAME checkout). If sLRFlipper/sLLFlipper follow the common WPC-derived "
				"convention (45/47), they resolve to the only two addresses in this range the emulator "
				"ever writes live data to -- but under the driver's own admitted mirror-naming defect, "
				"the script's 'SolRFlipper' visual/sound handler would then be driven by the mirror of "
				"the physical LEFT flipper circuit. This definition binds the two used mirror "
				"addresses (45, 47) to their physical correspondence (45 mirrors S9/Left Flipper; 47 "
				"mirrors S10/Right Flipper) per the source-code mirror logic, not per PinMAME's "
				"'Lower Right/Lower Left' constant names. Unresolved: the exact value of the script's "
				"own sLRFlipper/sLLFlipper symbols, and therefore whether the retained table's visual "
				"flipper handlers are internally consistent with this physical mapping."
			),
			"source_refs": [CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE, SCHEMATIC_SOURCE],
		},
		{
			"id": "conflict.solenoid-35-eject-hole-mirror-mislabeled",
			"path": "outputs[binding.device=35]",
			"description": (
				"src/wpc/capcom.c's io_w mirror code unconditionally treats physical solenoid "
				"addresses 9/10/11/12 as the four flipper-power circuits and writes address 12's live "
				"state into sULFlipPow=35 under the generic name 'Upper Left Flip Power'. The manual "
				"and schematic sheet 7 both independently and exactly agree that physical address 12 "
				"is 'Eject Hole' (S12), not an upper-left flipper -- and the S1-S32 device table shows "
				"no upper-left flipper circuit anywhere on this machine at all (only S9/S10/S11, "
				"Left/Right/Upper-Right). Address 35 therefore mirrors an unrelated device (the Eject "
				"Hole coil, already separately modeled at address 12) purely as an artifact of "
				"PinMAME's fixed positional mirror assumption, not a genuine flipper address on this "
				"specific game."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE, SCHEMATIC_SOURCE],
		},
		{
			"id": "conflict.solenoid-22-shared-device-construction",
			"path": "outputs[binding.device=22]",
			"description": (
				"Schematic sheet 7 draws both devices sharing solenoid address 22 (Tube Dancer and "
				"Backbox Right flasher) with the identical circular bulb symbol used for lamps/"
				"flashers elsewhere on the sheet, not the coil-plus-flyback-diode symbol used for "
				"S1-S20/S27-S29. The manual's own page-82 location table separately prints Ref. 22 "
				"'TUBE DANCER' with the generic coil part number CL00109 (not the LP00101 flasher-lamp "
				"part its neighbors use), and the Tube Lady Assembly mechanism parts page (printed "
				"page 108) shows a genuine coil (item 1A) as part of the same physical mechanism. "
				"Whether the Tube Dancer's mechanical pop/bounce action is actually solenoid-driven "
				"through address 22 (despite the bulb-shaped schematic symbol) or is purely "
				"spring/gravity return with address 22 driving only lamp effects is not resolved by "
				"any source available to this curation."
			),
			"source_refs": [MANUAL_SOURCE, SCHEMATIC_SOURCE],
		},
		{
			"id": "conflict.ramp-diverter-geometry-inconsistent",
			"path": "outputs[binding.device=14,15]",
			"description": (
				"The retained table's rotating gate-arm objects for Ramp Diverter 1/2 (DivTubef, "
				"DivTube2f -- Flipper-type primitives reused for rotation animation) sit near the "
				"front apron (normalized y=0.98-0.99), while their same-named companion drop-wall "
				"panel objects (DivTube/DivTube1, DivTube2) sit near the rear/top of the playfield "
				"(normalized y=0.10-0.11) -- a difference far too large for one physical diverter "
				"mechanism. The retained script's own SolRDivert1/SolRDivert2 handlers manipulate both "
				"halves together as if they were one mechanism (DivTubef.RotateToEnd alongside "
				"DivTube.isDropped/DivTube1.isDropped in the same Sub), so this is not a case of two "
				"unrelated devices sharing a name by coincidence. No coordinate for either address is "
				"promoted to a validated placement."
			),
			"source_refs": [VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "capcom.big-bang-bar.1996",
			"name": "Big Bang Bar",
			"manufacturer": "Capcom",
			"year": 1996,
			"kind": "physical_pinball",
			"ipdb_id": 4001,
			"playfield": {"width": 952.0, "height": 2162.0, "units": "vpx", "provenance": provenance(VPX_TABLE_SOURCE)},
		},
		"coverage": {
			"status": "partial",
			"missing": ["polarity", "output_semantics", "mechanism_behavior", "spatial_placement", "unresolved_conflicts", "recreation_notes"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "candidate",
				"physical_wiring": "conflicted",
				"mechanisms": "candidate",
				"variant_coverage": "validated",
				"recreation_knowledge": "candidate",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.capcom",
			"hardware_generation": "0x0",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/capcom/big-bang-bar-1996.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Big Bang Bar device identifiers are not unique: {duplicates}")
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
		"status": "validated",
		"blockers": [
			"Three used lamp addresses (3, 38, 125) have no Lampz.MassAssign object in the retained "
			"table at all, so no coordinate can be reported; their `spatial` key is omitted rather "
			"than invented.",
			"Solenoids 14 (Ramp Diverter 1) and 15 (Ramp Diverter 2) each resolve to two table "
			"objects whose raw positions are inconsistent by most of the playfield's length; neither "
			"is promoted to a validated placement (conflict.ramp-diverter-geometry-inconsistent).",
			"Lamps 2 and 62 resolve to retained-table objects whose raw positions fall outside the "
			"table's own 0..1 normalized playfield bounds; excluded as a table-modeling anomaly "
			"rather than clamped.",
			"Four unresolved conflicts (flipper mirror address left/right naming, the address-35 "
			"Eject Hole mirror mislabeled as an upper-left flipper, solenoid 22's shared "
			"bulb-vs-coil device construction, and the ramp-diverter geometry inconsistency above) "
			"keep coverage.dimensions.physical_wiring conflicted and the record partial.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2162.0},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2162; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/capcom/big-bang-bar-1996/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"vpxtool_version": "vpxtool",
		},
		"source_hashes": {
			"embedded_script_sha256": SCRIPT_SHA256,
			"manual_sha256": MANUAL_SHA256,
			"schematic_sha256": SCHEMATIC_SHA256,
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
		"unresolved_inputs": sorted(unresolved_inputs),
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/capcom.big-bang-bar.1996/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"solenoid_transcription": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/manual-transcription-solenoids.md",
				"sha256": MANUAL_TRANSCRIPTION_SOLENOIDS_SHA256,
			},
			"geometry_notes": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_NOTES_SHA256,
			},
		},
		"excluded_object_classes": [
			"Light objects L02/L62 -- raw position far outside the retained table's 0..1 playfield bounds (table-modeling anomaly, not a distinct physical bulb position)",
			"F21-F26 flasher Light objects reported under their owning solenoid address (21-26), never as a separate lamp address",
			"DivTubeF/DivTube/DivTube1 and DivTube2f/DivTube2 (solenoids 14/15) -- internally inconsistent raw positions for what the script treats as one mechanism each; excluded pending human review",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Big Bang Bar (Capcom, 1996) spatial review",
		"",
		f"Status: {report['status']}. This audit is complete for every address it covers, but the "
		"physical machine record itself remains `partial` at "
		"`machines/partial/capcom/big-bang-bar-1996.json` because of unresolved conflicts and "
		"output-semantics gaps outside this audit's scope; see the promotion decision below.",
		"",
		"The matching source is the retained known-working `Big Bang Bar (Capcom 1996) VPW v1.0.vpx` "
		f"at SHA-256 `{TABLE_SHA256}`. The retained extraction produced the embedded script at "
		f"SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. "
		f"Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and "
		"y/2162 rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Capcom "
		"operators manual and its companion schematic set are the physical inventory, quantity, "
		"polarity, wiring, and device-identity authority (the schematic's own per-device "
		"\"DEVICE # & DESCRIPTION\" table on sheet 7 is the single most authoritative solenoid "
		"source found); pinned PinMAME source owns controller topology and per-game hardware "
		"metadata; the retained table supplies geometry.",
		"- The manual is an Adobe Paper Capture OCR'd scan whose text layer is unreliable on dense "
		"multi-column tables; every printed table used here was read from rendered page images at "
		"200-600 dpi and transcribed into "
		"`external:pinmame-review-artifacts/big-bang-bar/manual-transcription.md` and its companion "
		"solenoid/schematic document.",
		"- Several switches have no dedicated playfield trigger object because the retained script "
		"sets their public state directly from another mechanism's continuous position (the Alien "
		"rotating mechanism's 32-step motor counter) or reuses a table object that also serves "
		"another role (kickers, slingshot walls, bumpers). Those addresses are explicit documented "
		"projections onto the real table object that carries the underlying mechanism state.",
		"- Two Light objects (lamp addresses 2 and 62) sit outside the retained table's 0..1 "
		"normalized playfield bounds and are excluded as a table-modeling anomaly.",
		"- Three used lamp addresses (3, 38, 125) and two solenoid addresses' mechanism geometry "
		"(14, 15) have no resolvable coordinate in the retained table; their `spatial` key is "
		"omitted entirely rather than an invented status or coordinate.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled "
		"`not_applicable` with both PinMAME core and manual provenance.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- Switch {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Unresolved input addresses (used, no coordinate): {len(report['unresolved_inputs'])}",
		f"- Unresolved output bindings (used, no coordinate): {len(report['unresolved_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement question remains silently unresolved: every address this "
		"audit covers is either a validated placement, a controlled `not_applicable` record, or an "
		"explicitly named unresolved gap. However, four first-class conflicts remain open (flipper "
		"mirror address left/right naming, the address-35 Eject Hole mirror mislabeled as an "
		"upper-left flipper, solenoid 22's shared bulb-vs-coil device construction, and the "
		"ramp-diverter geometry inconsistency), and three output devices (the inferred Bumper "
		"1/2/3 solenoid correspondence) rest on ordering evidence rather than a confirmed wiring "
		"page. The definition therefore carries a non-empty `conflicts` array and "
		"`coverage.dimensions.physical_wiring = \"conflicted\"`, so promotion to `author_ready` is "
		"refused; the record stays `partial` with `coverage.missing = [\"polarity\", "
		"\"output_semantics\", \"mechanism_behavior\", \"spatial_placement\", "
		"\"unresolved_conflicts\", \"recreation_notes\"]`. This curation pass was also run without "
		"the mandatory independent high-tier cross-provider review described in "
		"`docs/INSTRUCTIONS.md`, which alone would keep `recreation_notes` in `coverage.missing` "
		"even if every other gap were closed.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} "
		"bytes.",
		f"- Human transcription of every printed switch/lamp table, SHA-256 "
		f"`{MANUAL_TRANSCRIPTION_SHA256}`, and its companion solenoid/schematic transcription, "
		f"SHA-256 `{MANUAL_TRANSCRIPTION_SOLENOIDS_SHA256}`.",
		f"- VPX object-geometry notes, SHA-256 `{VPX_GEOMETRY_NOTES_SHA256}`.",
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
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if not definition_path.is_file():
		raise RuntimeError(f"Big Bang Bar definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Big Bang Bar seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Big Bang Bar definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Big Bang Bar seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Big Bang Bar spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Big Bang Bar spatial review drifted from its deterministic curator: {markdown_path}")
	print("Big Bang Bar definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Big Bang Bar extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Big Bang Bar retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
