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
DEFINITION_PATH = ROOT / "machines/author-ready/capcom/big-bang-bar-1996.json"
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
# Second retained recreation (the earlier community build that predates VPW v1.0).
# Its script and geometry corroborate the flasher binding of solenoid 22, the
# star-bumper solenoid identity, and the solenoid-15 diverter wall coordinate.
CORROBORATION_TABLE_SOURCE = "vpx-table.bbb-archive-2013"
CORROBORATION_SCRIPT_SOURCE = "vpx-script.bbb-archive-2013"
# The VPinMAME script library (core.vbs / Capcom.VBS) the retained table loads at
# runtime, retained from the contributor's installation; its flipper constants
# resolve the sLRFlipper/sLLFlipper symbol values the table script binds.
VPM_LIBRARY_SOURCE = "vpm-script-library.core-vbs"
# IPDB machine-page photographs retained for physical corroboration (the Tube Lady
# assembly standing on the playfield, and a full overhead playfield view).
IPDB_PHOTO_TUBE_LADY_SOURCE = "ipdb-photo.capcom.big-bang-bar.1996.tube-lady"
IPDB_PHOTO_OVERHEAD_SOURCE = "ipdb-photo.capcom.big-bang-bar.1996.overhead"

TABLE_SHA256 = "7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5"
SCRIPT_SHA256 = "db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7"
MANUAL_SHA256 = "5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5"
SCHEMATIC_SHA256 = "fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603"
MANUAL_TRANSCRIPTION_SHA256 = "3e503420d32c307f409edaa57c80d6f4bfa9f01d90cd0e47dbc6ddc755188994"
MANUAL_TRANSCRIPTION_SOLENOIDS_SHA256 = "b996714bd9cd3811481ab0eb0ccce071c3d019819844eaffffaf5318e28c4bd5"
VPX_GEOMETRY_NOTES_SHA256 = "e1339971328d98e365b6574733b08f8dc1849814806bb2973019482c93468ac5"
CORROBORATION_TABLE_SHA256 = "ba5d1384397b8a1a9115b089e4a281634acb9bfb760fe096a320774a8fa2ba46"
CORROBORATION_SCRIPT_SHA256 = "cefa47a25952eb96fef752e2c0e718c00f9ce9d0e733aaa86f92ced7c18c5a84"
VPM_CORE_LIBRARY_SHA256 = "d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72"
VPM_CAPCOM_LIBRARY_SHA256 = "03323ded224c5e67b0f7703978529889339e1fd7f73ebdd15002a4a6b794a95e"
IPDB_TUBE_LADY_PHOTO_SHA256 = "ac3ba370260155e1d1288cc95017ee3c88605d5b0ac56948ef369c47dc7fabd5"
IPDB_OVERHEAD_PHOTO_SHA256 = "abb750b69bb58cff40f9265785cb91682ad101815a07628a00f5a983d46adf11"
# gameitems cited from the corroboration extraction (path -> SHA-256), pinned so the
# corroboration assertions stay checkable without retaining the whole extraction.
CORROBORATION_CITED_FILES = {
	"Wall.DivTube2.json": "bef7b8082c6882e06d10e0ca3359d2fbdf6e71d148c3a3ad058933fbbd2eb509",
	"Light.l38.json": "2f78e5f75ea725a25fea34e7abc6339b364f19af9714a29e7ca488be1a2a21f8",
	"Light.l125.json": "e9ecbe161f3395ddd6697edac49b7d78902df7b5624515de5111786279f509f4",
	"Light.F22.json": "fe857f8c3c109b8c4a6a5be66f644a1be900f8c67f6fbe2de6a1697295f2af8b",
	"Bumper.Bumper1.json": "9fea99905eed651862f7af79a4d87bf1b2b0ed40f73166eb09ac79a2924b0449",
	"Bumper.Bumper2.json": "5f3e0341e7230403e918f43cc6127ba7f0d5fda584ac68bba8af21ddeaa5b630",
	"Bumper.Bumper3.json": "e95cf3e0469698521fbb9612f11ebcf710c8c11ea523cc749c4e936ebdbc151d",
}

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
# Author-ready spatial alignment roles: cabinet switches carry the platform role
# vocabulary so the controlled cabinet_or_service records validate structurally.
CABINET_SWITCH_ROLES = {
	1: ["cabinet.coin.1"], 2: ["cabinet.coin.2"], 3: ["cabinet.coin.3"], 4: ["cabinet.coin.4"],
	5: ["flipper.lower.left.button"], 6: ["flipper.lower.right.button"],
	7: ["cabinet.start"], 8: ["cabinet.coin-door"], 9: ["cabinet.slam-tilt"], 10: ["cabinet.tilt"],
	15: ["service.ticket"], 16: ["service.ticket"],
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
# (A0015604-4R / A0015702-4R, matching the Opto Boards page); 25 and 57's own location-table
# opto columns are illegible in this scan, but each carries decisive manufacturer
# construction evidence elsewhere in the same document set: 25 via the Playfield Features
# page's "the opto spinner" scoring text, 57 via the Alien Mech Assembly parts list's
# MT00501 encoder disc + A0020000 opto PCB and the C2-02 diagnostic's "the opto (which
# reads the encoder wheel)" failure text. All six mask addresses are therefore
# positively documented optos with zero disagreement against PinMAME's mask.
CONFIRMED_OPTO_PART_NUMBER = {36, 37, 38, 39}
OPTO_RECEIVER_PART = "A0015604-4R"
OPTO_XMTR_PART = "A0015702-4R"

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
	# Star bumpers: 54 Left / 55 Right / 56 Middle. An earlier revision inferred these from the
	# retained script's bumper DECLARATION order, which is y-order (Bumper1 top, Bumper2, Bumper3
	# bottom), and read it as a left-to-right physical order. The manual's own numbered
	# "SOLENOIDS, MOTORS, & FLASHERS" playfield diagram marks 18 leftmost, 20 upper-right and 19
	# lower-centre, and this definition's OWN lamp records agree: lamps 122/123/124 come from
	# per-address-named Light objects (l122/l123/l124) rather than an inferred order, and place
	# Left at x=0.3808, Middle at 0.5251 and Right at 0.5860. The switch and solenoid coordinates
	# below are corrected to match.
	54: [(0.380918, 0.20046)], 55: [(0.585404, 0.178991)], 56: [(0.526188, 0.267465)],
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
	9: 'SolCallback(9) commented out ("SolLFlipper); native address unbound -- the ROM drives this coil while the retained table animates the bat from key handlers (see outputs 45/47)',
	10: 'SolCallback(10) commented out ("SolRFlipper); native address unbound -- see outputs 45/47',
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
	8: [(0.20852, 0.766107)],
	12: [(0.844337, 0.521704)], 13: [(0.947213, 0.371481)],
	16: [(0.862307, 0.018598)],
	18: [(0.380918, 0.20046)], 19: [(0.526188, 0.267465)], 20: [(0.585404, 0.178991)],
	21: [(0.062763, 0.088922)], 22: [(0.252177, 0.13264)], 23: [(0.495536, 0.215657)],
	24: [(0.873687, 0.493178)], 25: [(0.942772, 0.058572)], 26: [(0.150773, 0.80503)],
	27: [(0.289968, 0.047017)], 28: [(0.671092, 0.034329)],
	29: [(0.708865, 0.130149)],
	30: [(0.252247, 0.132496)],
}
# Solenoid 21 is backbox hardware, not a playfield emitter: the device's own printed name
# is "BACKBOX LEFT (FLASHER)", the manual's printed page-82 diagram marks callout 21
# inside the backbox box, and the retained table's F21 Light object is a render proxy.
SOLENOID_BACKBOX_ADDRESSES: dict[int, str] = {
	21: (
		"Backbox flasher (callout 21 in the backbox box of the manual's printed page-82 "
		"playfield diagram, directly beside its Backbox Right partner's shared callout 22). "
		"The retained table's F21 Light object sits at a playfield-coordinate render proxy "
		"(rear-left of the playfield), which is presentation geometry, not the physical "
		"socket; the manual controls the physical and spatial classification and no "
		"playfield coordinate is promoted."
	),
}
# Documented coil placements for addresses whose retained-table objects are the
# assembly the coil actuates. Coordinates come from the retained table's own
# objects; the manual's printed page-82 numbered playfield diagram corroborates
# each (balloon-centre tolerance ~0.02-0.05; see
# evidence/excerpts/capcom.big-bang-bar.1996/solenoid-location-diagram.md).
SOLENOID_PROJECTION_PLACEMENTS: dict[int, tuple[str, list[tuple[float, float]], tuple[str, ...]]] = {
	# Slingshot coils project onto their own slingshot wall assemblies; the retained
	# table models both slingshots as passive rubber walls and binds no coil object.
	4: (
		"Projected onto the Wall.LeftSlingShot assembly's own drag-point centroid; the "
		"manual's printed page-82 playfield diagram marks callout 4 at the left "
		"slingshot coil position (balloon measures to (0.227, 0.756), within ~0.02).",
		[(0.229376, 0.735796)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	5: (
		"Projected onto the Wall.RightSlingShot assembly's own drag-point centroid; the "
		"manual's printed page-82 playfield diagram marks callout 5 at the right "
		"slingshot coil position (balloon measures to (0.698, 0.754), within ~0.03).",
		[(0.674001, 0.733646)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	9: (
		"Projected onto the LeftFlipper table object's own pivot centre; the manual's "
		"printed page-82 playfield diagram marks callout 9 at the left flipper coil "
		"(balloon measures to (0.306, 0.863), within ~0.02).",
		[(0.285743, 0.848334)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	10: (
		"Projected onto the RightFlipper table object's own pivot centre; the manual's "
		"printed page-82 playfield diagram marks callout 10 at the right flipper coil "
		"(balloon measures to (0.633, 0.863), within ~0.02).",
		[(0.618202, 0.84836)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	11: (
		"Projected onto the RightFlipper1 table object's own pivot centre (the upper-right "
		"flipper's own bat, positioned mid-playfield); the manual's printed page-82 "
		"playfield diagram marks callout 11 at the upper-right flipper coil on the right "
		"side (balloon measures to (0.824, 0.491), within ~0.03 of this pivot).",
		[(0.827363, 0.457798)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
}
# Ramp Diverter 1 (solenoid 14) actuates a two-panel drop wall; both retained tables
# model it as walls at the rear-left of the playfield, and the manual's page-82
# diagram marks callout 14 at that same rear-left position (balloon (0.133, 0.067)).
# Ramp Diverter 2 (solenoid 15) actuates a single drop wall at the top-centre-left;
# the manual's callout 15 (balloon (0.258, 0.034)) and the earlier retained
# recreation's Wall.DivTube2 agree on that position, while the VPW v1.0 table's
# same-named wall sits ~0.17 normalized units to the right and is disclosed as
# divergent retained geometry rather than promoted. The tables' Flipper-type
# DivTubef/DivTube2f rotation helpers are is_visible=false animation primitives
# parked at the front apron (y~=0.98-0.99) in both tables and are never physical
# locations.
# Mechanism-coil projections: shared reset coils and the reversible alien motor are placed
# onto the mechanism members their own switches/parts pages identify, never at an invented
# coil-body coordinate.
SOLENOID_MECHANISM_PROJECTIONS: dict[int, tuple[str, list[tuple[float, float]], tuple[str, ...]]] = {
	7: (
		"Projected onto the four 4-Bank drop targets' own switch positions (switches 17-20): "
		"one reset coil actuates the whole bank -- the retained script's sol4Bank raises all "
		"four targets in one pulse and the mechanism parts page documents one shared reset "
		"bar/coil -- so the placement set is the bank's four target positions, not a single "
		"coil-body coordinate.",
		[(0.106602, 0.611911), (0.115986, 0.585663), (0.125458, 0.559367), (0.134723, 0.532262)],
		(VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
	),
	17: (
		"Projected onto the three 3-Bank drop targets' own switch positions (switches 49-51): "
		"one reset coil actuates the whole bank (sol3Bank; the mechanism parts page's shared "
		"reset callout), so the placement set is the bank's three target positions.",
		[(0.444456, 0.336556), (0.497771, 0.327576), (0.550396, 0.318153)],
		(VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
	),
	31: (
		"Projected onto the two rotating alien figures' own anchors: the forward motor output "
		"drives the same reversible mechanism whose encoder the switch-57 opto senses, so the "
		"placement set is the two figure anchors.",
		[(0.71318, 0.067239), (0.782786, 0.11226)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	32: (
		"Projected onto the two rotating alien figures' own anchors: the reverse motor output "
		"drives the same reversible mechanism as solenoid 31, so both direction records carry "
		"the same two figure anchors.",
		[(0.71318, 0.067239), (0.782786, 0.11226)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
}
# Author-ready spatial alignment roles for outputs whose controlled cabinet records
# need the platform role vocabulary.
SOLENOID_ROLES: dict[int, list[str]] = {
	3: ["cabinet.knocker"],
	21: ["cabinet.backbox"],
}
LAMP_CABINET_ROLES: dict[int, list[str]] = {
	1: ["cabinet.coin-door"],
	2: ["cabinet.coin-door"],
	3: ["cabinet.start-lamp"],
	129: ["service.cpu-diagnostic"],
	130: ["service.sound-diagnostic"],
}
SOLENOID_DIVERTER_PLACEMENTS: dict[int, tuple[str, list[tuple[float, float]], tuple[str, ...]]] = {	14: (
		"Two-panel drop wall for Ramp Diverter 1; coordinates are the retained table's own "
		"Wall.DivTube and Wall.DivTube1 drag-point centroids. The manual's printed page-82 "
		"playfield diagram marks callout 14 at the same rear-left position (balloon "
		"(0.133, 0.067), within ~0.02-0.04 of both panels).",
		[(0.111295, 0.113743), (0.129284, 0.099031)],
		(VPX_TABLE_SOURCE, MANUAL_SOURCE),
	),
	15: (
		"Drop wall for Ramp Diverter 2; the coordinate is the earlier retained recreation's "
		"Wall.DivTube2 drag-point centroid, which agrees with the manual's printed page-82 "
		"callout 15 (balloon (0.258, 0.034), within ~0.034). The VPW v1.0 table's "
		"same-named wall sits at (0.433, 0.032), ~0.17 normalized units right of both the "
		"manual's callout and this recreation, and is disclosed as divergent retained "
		"geometry rather than promoted.",
		[(0.291495, 0.023552)],
		(CORROBORATION_TABLE_SOURCE, MANUAL_SOURCE),
	),
}

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
		"receives live data whenever address 11 does; the retained script binds no native "
		"SolCallback for address 11 (SolCallback(11)=\"SolURFlipper\" is commented out), which "
		"is a statement about that table's bindings, not about the address's availability."
	),
	34: "sURFlip (CORE_FIRSTUFLIPSOL+1=34, the 'hold' half of the upper-right pair); src/wpc/capcom.c io_w never writes any PWM value to this address for the cc family, so it is permanently zero regardless of what fires on address 11 or 33.",
	35: (
		"src/wpc/capcom.c's io_w mirror code unconditionally treats physical addresses 9/10/11/12 "
		"as the four flipper-power circuits and writes address 12's live state into sULFlipPow=35 "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sULFlipPow-1,1,(soldata>>11)&0x01)) -- but Big "
		"Bang Bar wires physical address 12 to Eject Hole (S12, confirmed by both the manual and "
		"schematic sheet 7), not an upper-left flipper; this machine has no upper-left flipper "
		"circuit anywhere in the S1-S32 table. Address 35 therefore mirrors the Eject Hole coil's "
		"own state under PinMAME's generic 'Upper Left Flip Power' name purely as an accident of "
		"the mirror code's fixed positional assumption, not a genuine flipper mirror. The "
		"single write site makes the mirror relation structural: every value 35 ever publishes "
		"is bit 11 of the same soldata word that drives physical 12. The emulator-facing name is "
		"the driver's own admitted defect ('does not correspond to manuals or any other "
		"reference'); the machine's wiring was never in disagreement."
	),
	36: "sULFlip (CORE_FIRSTUFLIPSOL+3=36, the 'hold' half of the upper-left pair); never written by cc's io_w for any address in this range, permanently zero.",
	45: (
		"sLRFlipPow (CORE_FIRSTLFLIPSOL+0=45). src/wpc/capcom.c io_w case 0x20000d mirrors "
		"physical solenoid 9 (S9, 'L. Flipper') into this address "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sLRFlipPow-1,1,(soldata>>8)&0x01)) -- the only "
		"live source of data for this address. The retained script's symbolic "
		"SolCallback(sLRFlipper)=\"SolRFlipper\" binding resolves against the installed VPinMAME "
		"script library's own constants (core.vbs: sLRFlipper=46, sLLFlipper=48, sURFlipper=34, "
		"sULFlipper=36 -- the library's flipper-solenoid symbols name the hold-side addresses; "
		"see vpm-script-library-constants.md), so that binding listens on hold address 46, which "
		"capcom.c never writes -- the retained table's flipper callbacks receive no emulator "
		"data at all under this library revision (a consumed-table/environment defect; the "
		"table's flippers animate from its own key handlers while the ROM drives physical 9/10 "
		"directly). PinMAME's 'Lower RIGHT Flip Power' constant name for address 45 is the "
		"driver's own admitted mirror-naming defect: the address carries the physical LEFT "
		"circuit, and this definition binds it accordingly."
	),
	47: (
		"sLLFlipPow (CORE_FIRSTLFLIPSOL+2=47). src/wpc/capcom.c io_w case 0x20000d mirrors "
		"physical solenoid 10 (S10, 'R. Flipper') into this address "
		"(core_write_pwm_output(CORE_MODOUT_SOL0+sLLFlipPow-1,1,(soldata>>9)&0x01)) -- the only "
		"live source of data for this address. The retained script's symbolic "
		"SolCallback(sLLFlipper)=\"SolLFlipper\" binding resolves against the installed VPinMAME "
		"script library's own constants (core.vbs: sLLFlipper=48, i.e. hold address 48, which "
		"capcom.c never writes; see vpm-script-library-constants.md), so it receives no emulator data "
		"under this library revision. PinMAME's 'Lower LEFT Flip Power' constant name for "
		"address 47 is the driver's own admitted mirror-naming defect: the address carries the "
		"physical RIGHT circuit, and this definition binds it accordingly."
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
# = L<N> in the retained script; normalized x/952, y/2162). Used addresses without an entry
# here are placed explicitly below (38/125 from the earlier retained recreation, 62 as a
# documented projection) or carry a controlled cabinet record (1/2/3).
LAMP_POSITIONS: dict[int, tuple[float, float]] = {
	9: (0.059856, 0.451509),
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
	58: (0.205349, 0.28074), 59: (0.16866, 0.21628), 65: (0.147726, 0.776616), 66: (0.208455, 0.795416), 67: (0.280809, 0.811051),
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
# Two used lamp addresses have no object in the retained VPW v1.0 table but ARE modeled
# by the earlier retained recreation (corroboration extraction, gameitems Light.l38 /
# Light.l125); each coordinate agrees with the same-feature neighbours the primary table
# does model (Alien G.I. 1/3 for 38; the dance-floor area's own flasher F23 for 125).
LAMP_CORROBORATION_POSITIONS: dict[int, tuple[float, float, str]] = {
	38: (
		0.863445, 0.018851,
		"Coordinate from the earlier retained recreation's Light.l38 (822.0, 40.75 in its own "
		"952x2162 playfield space). The VPW v1.0 table models no object for this address; the "
		"position agrees with the Alien G.I. strip the primary table does model (lamp 37 at "
		"(0.778, 0.093), lamp 39 at (0.943, 0.060)), completing the same rear-right alien-area "
		"row the manual's lamp table names Alien G.I. 1/2/3.",
	),
	125: (
		0.502167, 0.213736,
		"Coordinate from the earlier retained recreation's Light.l125 (478.0625, 462.0935 in "
		"its own 952x2162 playfield space). The VPW v1.0 table models no object for this "
		"address; the position sits inside the dance-floor feature between the star bumpers, "
		"beside that feature's own flasher (solenoid 23 at (0.496, 0.216)), matching the "
		"manual's lamp-table name. The schematic's matrix-B sheet marks this address X2 -- two "
		"#44 bulbs share it; the recreation models one, so the second bulb's socket position "
		"is not individually surveyed.",
	),
}
# The (Electro) Black Light has no object in either retained recreation (the VPW table's
# L62 is an out-of-bounds playfield-sized wash mesh, excluded as a modeling artifact).
# The manual names it for the (Electro) Ramp feature, whose three feature lamps the
# primary table models along the rear-right ramp; the placement is a documented
# projection onto that feature's centroid, not a surveyed socket position.
LAMP_ELECTRO_BLACK_LIGHT_PROJECTION = (
	0.880954, 0.081206,
	"Documented projection: centroid of the three (Electro) Ramp feature lamps the "
	"retained table models (lamp 44 (0.768, 0.043), lamp 45 (0.945, 0.081), lamp 46 "
	"(0.930, 0.120)). The manual's lamp table names address 62 '(ELECTRO) BLACK LIGHT' "
	"(#44, LP00109) for that feature; the exact tube/socket position is not surveyed and "
	"neither retained recreation models a usable object (the VPW table's L62 is an "
	"out-of-bounds playfield-sized wash mesh, excluded as a modeling artifact).",
)
# Cabinet lamps the manual's own lamp table names after cabinet hardware. The START lamp
# illuminates the cabinet start button, not a playfield insert: the retained script binds
# Lampz.Callback(03) to the PinCab_Start_Button object ('For VR StartButton Lighting'),
# the manual's lamp table lists it directly beside the two coin-door lamp rows, and no
# playfield START insert exists in either retained recreation or in any retained
# photograph of the machine.
LAMP_CABINET_ADDRESSES: dict[int, str] = {
	1: "Coin-door lamp pair 'Coin Door 1&2' (#259, LP00113): cabinet coin-door hardware. The "
	"schematic's matrix-A sheet marks this address X2 -- two bulbs. The retained table's "
	"object sits far outside the playfield bounds (a room-render glow proxy) and is excluded "
	"as a modeling artifact rather than promoted.",
	2: "Coin-door lamp pair 'Coin Door 3&4' (#259, LP00113): cabinet coin-door hardware. The "
	"schematic's matrix-A sheet marks this address X2 -- two bulbs. The retained table's "
	"object sits far outside the playfield bounds (a room-render glow proxy) and is excluded "
	"as a modeling artifact rather than promoted.",
	3: "The START lamp (#555, LP00100) illuminates the cabinet start button, not a playfield "
	"insert: the retained script binds Lampz.Callback(03) to the PinCab_Start_Button object "
	"('For VR StartButton Lighting'), the manual's lamp table lists it directly beside the "
	"two coin-door lamp rows, and neither retained recreation models a playfield START "
	"insert nor does any retained photograph of the machine show one.",
}

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


# Committed crops are binary, so unlike the transcriptions they are hashed from
# the file on disk rather than from a literal in this curator.
EXCERPT_IMAGE_HASHES = {
	path.name: hashlib.sha256(path.read_bytes()).hexdigest()
	for path in sorted((ROOT / "evidence/excerpts/capcom.big-bang-bar.1996").glob("*.webp"))
}


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
				"flipper-column handling: the keyboard-off button-bit read, the 'set switches in "
				"matrix for non-fliptronic games' FLIP_SWL/FLIP_SWR copy into switches 5/6, and "
				"synthetic EOS bits); src/libpinmame/libpinmame.cpp (int g_fHandleKeyboard = 0, "
				"the LibPinMAME keyboard-handling default); src/libpinmame/libpinmame.h "
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
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/switch-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["switch-locations.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 87, crop box 0.03,0.095,0.98,0.945, scanned page rendered at its native resolution (embedded image xref 386, 4960px across 8.27in), rendered at 331 dpi, capped to 2600px wide, 2601x3089 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.lamp-locations",
					"locator": "PDF page 85, printed page 81, Cabinet, Playfield, & Backbox Lamps",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-locations.md",
					"sha256": "e42b56a3cab198c0dd02b225af4ec6617fa879a1f2641b235f326badb43ea8df",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-locations.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 85, crop box 0.03,0.1,0.98,0.925, scanned page rendered at its native resolution (embedded image xref 378, 4960px across 8.27in), rendered at 331 dpi, capped to 2600px wide, 2601x2998 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.solenoid-locations",
					"locator": "PDF page 86, printed page 82, Solenoids, Motors, & Flashers",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-locations.md",
					"sha256": "b4b65db7b910736ed230487d8d2c722c3d366928a537f43302f858044be7a4f4",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-locations.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-locations.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 86, crop box 0.02,0.1,0.44,0.6, scanned page rendered at its native resolution (embedded image xref 382, 4960px across 8.27in), rendered at 600 dpi, 2084x3293 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.solenoid-location-diagram",
					"locator": (
						"PDF page 86, printed page 82, the numbered playfield location drawing "
						"printed beside the Ref. table (backbox box above, playfield below; "
						"callouts 1-32)"
					),
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-location-diagram.md",
					"sha256": "39e0248f2197832818b2d568e106cb7fd01f06eefd93e8a35566929d669c5b72",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/solenoid-location-diagram.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["solenoid-location-diagram.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 86, crop box 0.47,0.045,0.99,0.93, scanned page rendered at its native resolution (embedded image xref 382, 4960px across 8.27in), rendered at 600 dpi, grayscale, 2580x5828 WebP quality 80",
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
				{
					"id": "excerpt.big-bang-bar.game-rules-spinner-opto",
					"locator": "PDF page 10, printed page 6, Playfield Features, SPINNER section",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/game-rules-spinner-opto.md",
					"sha256": "3661064d09bb26a51c0fd50551132adad7f16575aecdb61db881206f571381bd",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/game-rules-spinner-opto.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["game-rules-spinner-opto.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 10, crop box 0.05,0.3,0.72,0.5, scanned page rendered at its native resolution (embedded image xref 41, 4972px across 8.29in), rendered at 469 dpi, capped to 2600px wide, grayscale, 2601x1031 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.alien-mech-parts-list",
					"locator": "PDF page 109, printed page 105, Alien Mech Assembly parts list (rows 1-10; the drawing whose callouts 2/3/5 sit beside the motor is printed page 104)",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/alien-mech-parts-list.md",
					"sha256": "6928561988d19ded39c86ca3c0f9b0e7310c86dfe030136901a665390b0626e7",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/alien-mech-parts-list.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["alien-mech-parts-list.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 109, crop box 0.08,0.075,0.93,0.375, scanned page rendered at its native resolution (embedded image xref 488, 4960px across 8.27in), rendered at 256 dpi, capped to 1800px wide, grayscale, 1801x845 WebP quality 60",
				},
				{
					"id": "excerpt.big-bang-bar.alien-motor-diagnostic-opto",
					"locator": "PDF page 46, printed page 42, C2-02 Alien Motor failure messages",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/alien-motor-diagnostic-opto.md",
					"sha256": "d524c62738710baa99c587ea1ef046e5316f21c516539e016d1bee4379c9ba77",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/alien-motor-diagnostic-opto.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["alien-motor-diagnostic-opto.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 46, crop box 0.07,0.06,0.93,0.15, scanned page rendered at its native resolution (embedded image xref 199, 4992px across 8.32in), rendered at 363 dpi, capped to 2600px wide, grayscale, 2601x360 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.tube-lady-parts-list",
					"locator": "PDF page 113, printed page 109, Tube Lady Assembly parts list",
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/tube-lady-parts-list.md",
					"sha256": "cc0ae084feee1632e93944a028003dd5d3eec8d6214bbb8607142115b055d98a",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/tube-lady-parts-list.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["tube-lady-parts-list.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Manual.pdf page 113, crop box 0.105,0.08,0.69,0.445, scanned page rendered at its native resolution (embedded image xref 506, 4960px across 8.27in), rendered at 285 dpi, capped to 1380px wide, grayscale, 1381x1144 WebP quality 48",
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
				{
					"id": "excerpt.big-bang-bar.lamp-matrix-b-x2-quantities",
					"locator": (
						"Sheet 10/12, \"DIAGRAM, LAMP MATRIX \"B\" WIRING\", the complete matrix-B "
						"wiring grid (columns 11-88) carrying the sheet's two X2 bulb-quantity "
						"annotations (B-37 = public 87, B-85 = public 125)"
					),
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-matrix-b-x2-quantities.md",
					"sha256": "609f76b4229cf162d2d298c1baefd97b6bf61aab5aa4d9ce13e1f71f43849117",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered sheet",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-matrix-b-x2-quantities.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-matrix-b-x2-quantities.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf page 10, crop box 0.01,0.15,0.58,0.78, scanned page rendered at its native resolution (embedded image xref 43, 9984px across 16.64in), rendered at 274 dpi, capped to 2600px wide, grayscale, 2601x1896 WebP quality 80",
				},
				{
					"id": "excerpt.big-bang-bar.lamp-matrix-a-x2-quantities",
					"locator": (
						"Sheet 9/12, \"DIAGRAM, LAMP MATRIX \"A\" WIRING\", the complete matrix-A "
						"wiring grid (columns 11-88) carrying the sheet's two X2 bulb-quantity "
						"annotations (A-11 = public 1, A-12 = public 2, both coin-door lamp pairs) "
						"plus the sheet's two-bulb X2 detail legend"
					),
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-matrix-a-x2-quantities.md",
					"sha256": "6e6ebeb8523d750a6c974e6b30fd08d1448f73ba713dca8c793f371327f53a7c",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered sheet",
					"reviewed": True,
					"image": "evidence/excerpts/capcom.big-bang-bar.1996/lamp-matrix-a-x2-quantities.webp",
					"image_sha256": EXCERPT_IMAGE_HASHES["lamp-matrix-a-x2-quantities.webp"],
					"image_derivation": "Capcom_1996_Big_Bang_Bar_Schematic_Diagrams_paginated.pdf page 9, crop box 0.01,0.15,0.58,0.78, scanned page rendered at its native resolution (embedded image xref 39, 9984px across 16.64in), rendered at 274 dpi, capped to 2600px wide, grayscale, 2601x1896 WebP quality 80",
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
		{
			"id": CORROBORATION_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/capcom/big-bang-bar-1996/corroboration/source/Big Bang Bar  (Capcom 1996).vpx",
			"original_filename": "Big Bang Bar  (Capcom 1996).vpx",
			"sha256": CORROBORATION_TABLE_SHA256,
			"locator": (
				"The earlier community recreation retained from the contributor's Tables Archive as "
				f"corroboration evidence (a different implementation from VPW v1.0; its 99,636-byte "
				"script shares the DivTube object-naming family with VPW v1.0, so the two are NOT "
				"treated as independent for geometry consensus -- corroboration claims below are "
				"always paired with a manual citation). Bounds are " f"{TABLE_BOUNDS}, identical to "
				"the primary table. Cited for: the flasher binding of solenoid 22 ('setlamp 162' / "
				"Light.F22), the star-bumper switch identities (Bumper1_Hit->56, Bumper2_Hit->54, "
				"Bumper3_Hit->55 over the same three bumper-ring positions the primary table "
				"models), and the Wall.DivTube2 coordinate used for solenoid 15's placement. "
				"Cited gameitems are pinned by SHA-256 under "
				"external:pinmame-review-artifacts/big-bang-bar/corroboration-table-cited/."
			),
			"license": "NOASSERTION",
			"attribution": "Big Bang Bar (Capcom 1996) community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": CORROBORATION_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/corroboration-table-cited/script.vbs",
			"original_filename": "script.vbs",
			"sha256": CORROBORATION_SCRIPT_SHA256,
			"locator": (
				"The earlier recreation's embedded script (99,636 bytes), retained with its cited "
				"gameitems. Runtime corroboration only: Const cGameName = \"bbb109\", "
				"SolCallback(22)=\"setlamp 162,\" ('Tube Dancer Flasher'), "
				"SolCallback(18/19/20) commented sound-only handlers labelled 'Left Bumper' / "
				"'Middle Bumper' / 'Right Bumper', Bumper1_Hit->56 / Bumper2_Hit->54 / "
				"Bumper3_Hit->55, and the same SolRDivert1/SolRDivert2 structure as the primary "
				"table."
			),
			"license": "NOASSERTION",
			"attribution": "Big Bang Bar (Capcom 1996) community table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPM_LIBRARY_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/vpm-script-libs/core.vbs",
			"original_filename": "core.vbs",
			"sha256": VPM_CORE_LIBRARY_SHA256,
			"locator": (
				"The VPinMAME script library the retained table loads at runtime (script.vbs line "
				"130 ExecuteGlobal GetTextFile(\"controller.vbs\"), line 134 LoadVPM "
				"\"01560000\", \"Capcom.VBS\", 3.10; Capcom.VBS executes core.vbs), retained from "
				"the contributor's working installation together with Capcom.VBS (SHA-256 "
				f"{VPM_CAPCOM_LIBRARY_SHA256}). Decisive for the flipper-mirror resolution: its "
				"'-- Flipper solenoids (all games)' block defines Const sLRFlipper = 46, "
				"sLLFlipper = 48, sURFlipper = 34, sULFlipper = 36 -- hold-side synthetic "
				"addresses src/wpc/capcom.c never writes -- so the retained table's symbolic "
				"flipper callbacks are dead bindings under this library revision. Transcribed "
				"excerpt: evidence/excerpts/capcom.big-bang-bar.1996/vpm-script-library-constants.md."
			),
			"license": "NOASSERTION",
			"attribution": "VPinMAME / Visual Pinball script-library maintainers",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.big-bang-bar.vpm-script-library-constants",
					"locator": (
						"core.vbs '-- Flipper solenoids (all games)' block plus the Capcom.VBS "
						"switch constants and its vpmKeyDown/vpmKeyUp flipper cases, with the "
						"retained table's HandleKeyboard setting and key-handler calls, retained "
						"from the contributor's working installation (SHA-256 values in the "
						"source record)"
					),
					"path": "evidence/excerpts/capcom.big-bang-bar.1996/vpm-script-library-constants.md",
					"sha256": "e1243a83e17554eb26b22fc9f4db97ed62b9b45147e945f39dfa7c5ef971f0a8",
					"method": "manual",
					"transcribed_by": "curator, read from the installed library files",
					"reviewed": True,
				},
			],
		},
		{
			"id": IPDB_PHOTO_TUBE_LADY_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/ipdb-photos/ipdb-4001-image-13-tube-lady-playfield.jpg",
			"original_filename": "image-13.jpg",
			"sha256": IPDB_TUBE_LADY_PHOTO_SHA256,
			"locator": (
				"IPDB machine 4001 photograph (retrieved from https://www.ipdb.org/machine.cgi?id=4001 "
				"via an authenticated browser session, 2026-08-28): the physical Tube Lady assembly "
				"standing in its clear tube on the playfield at the rear-left, beside the ADD-A-BALL / "
				"10 MILL / TOP UP JACKPOT tube-sign rollover buttons, with no coil visible -- "
				"corroborating the printed page-82 diagram's playfield callout-22/30 circle, the "
				"retained tables' tube-dancer placement, and the parts list's motor-belt "
				"construction. Identity/corroboration evidence only; no coordinate is derived from it."
			),
			"license": "NOASSERTION",
			"attribution": "IPDB contributor photograph, Internet Pinball Machine Database",
			"rights": "NOASSERTION",
		},
		{
			"id": IPDB_PHOTO_OVERHEAD_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/big-bang-bar/ipdb-photos/ipdb-4001-image-6-playfield-overhead.jpg",
			"original_filename": "image-6.jpg",
			"sha256": IPDB_OVERHEAD_PHOTO_SHA256,
			"locator": (
				"IPDB machine 4001 full overhead playfield photograph (retrieved from "
				"https://www.ipdb.org/machine.cgi?id=4001 via an authenticated browser session, "
				"2026-08-28): whole-playfield view used to visually cross-check feature positions "
				"(alien area, mode-ladder inserts, sling/apron area) against the retained tables' "
				"geometry; no START playfield insert exists anywhere on it, corroborating the "
				"cabinet START-button lamp disposition. Identity/corroboration evidence only."
			),
			"license": "NOASSERTION",
			"attribution": "IPDB contributor photograph, Internet Pinball Machine Database",
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


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


# FLIP_SWNO(5,6): with keyboard handling off, core_updateSw (src/wpc/core.c, "set
# switches in matrix for non-fliptronic games") copies the flipper column's lower
# button bits into the ROM-read switches 5/6 every frame, so a host presses the
# buttons through the flipper-column addresses instead.
FLIPPER_BUTTON_HOST_INPUTS = {
	# ROM-read switch: (host address, side, button bit)
	5: (84, "left", "CORE_SWLLFLIPBUTBIT (0x08)"),
	6: (82, "right", "CORE_SWLRFLIPBUTBIT (0x02)"),
}
FLIPPER_BUTTON_HOST_NOTES = {
	address: (
		f" The ROM reads the {side} flipper button here, but under PinMAME a host must drive "
		f"public {host} instead: with keyboard handling off, core_updateSw (src/wpc/core.c, "
		"'set switches in matrix for non-fliptronic games') overwrites this switch every frame "
		f"from the flipper column's {bit} bit, so a direct write here lasts at most one frame "
		f"(see switch.flipper-column-{host})."
	)
	for address, (host, side, bit) in FLIPPER_BUTTON_HOST_INPUTS.items()
}


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
			notes += FLIPPER_BUTTON_HOST_NOTES[address]
		if unused:
			notes += " CC_COMPORTS labels this bit a generic 'Unused #N' keyboard-simulation placeholder (src/wpc/capcoms.h); the manual confirms this specific game leaves the position genuinely unfitted."
		if address in (15, 16):
			notes += " Wired to this game's redemption/ticket hardware at a keyboard-simulation position CC_COMPORTS generically labels 'Unused' (src/wpc/capcoms.h); the printed part-number cell is blank."
		physical["notes"] = notes
		extra_kwargs: dict[str, Any] = {}
		roles = CABINET_SWITCH_ROLES.get(address)
		if roles:
			extra_kwargs["roles"] = roles
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
				spatial=not_applicable("constant" if unused else "cabinet_or_service", MANUAL_SOURCE),
				**extra_kwargs,
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
		elif address == 25:
			notes += (
				" Spinner: the manufacturer's own Playfield Features page (printed page 6) "
				"states '110 score per revolution (the opto spinner is fast; about 200 revs "
				"per solid hit!)' -- positive opto construction, resolving the question this "
				"address's illegible Opto Receiver/Xmtr P/N cells (a uniform scan defect "
				"affecting every row except 36-39 -- see switch-locations.md) left open. "
				"PinMAME's per-game capInvSw10 mask (src/wpc/capgames.c) normalizes this "
				"address, so the public switch state is already inverted and must not be "
				"inverted again."
			)
		elif address == 57:
			notes += (
				" Alien Motor: the Alien Mech Assembly parts list (printed page 105) carries "
				"the MT00501 encoder disc read by the A0020000 slotted-opto PCB assembly, and "
				"the C2-02 Alien Motor diagnostic describes 'the opto (which reads the encoder "
				"wheel)' -- positive opto construction, resolving the question this address's "
				"illegible Opto Receiver/Xmtr P/N cells (a uniform scan defect affecting every "
				"row except 36-39 -- see switch-locations.md) left open. PinMAME's per-game "
				"capInvSw10 mask (src/wpc/capgames.c) normalizes this address, so the public "
				"switch state is already inverted and must not be inverted again."
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
				normally_closed=address in PINMAME_NORMALIZED_OPTO_SWITCHES,
				pulse=address in PULSED_SWITCHES,
				**extra,
			)
		)

	items.append(
		_device(
			"switch.dmd-synthetic-flipper-column",
			"PinMAME Synthetic Flipper EOS and Upper-Button Bits",
			"virtual",
			"pinmame.input.switch",
			81,
			"unused",
			(CORE_SOURCE, CONTROLLER_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": "81"}],
			physical={
				"notes": (
					"Addresses 81-88 are PinMAME's flipper column (internal 'col 11', "
					"CORE_FLIPPERSWCOL=11, src/wpc/core.h; public 81 + row by cc_m2sw). This record "
					"covers 81, 83 and 85-88. bbb's hw.flippers (FLIP_SWNO(5,6)+FLIP_SOL(FLIP_LL|FLIP_LR"
					"|FLIP_UR|FLIP_UL)) implies FLIP_EOS for all four positions, so core_updateSw's "
					"end-of-stroke model overwrites the EOS bits 81, 83, 85 and 87 every frame; it "
					"declares no FLIP_SW(FLIP_U), so the upper-button bits 86 and 88 lie outside "
					"locals.flipMask: core_updateSw leaves a host write there unchanged and acts on "
					"neither. No Capcom circuit is behind any of these six bits and the ROM never "
					"reads the column; only two physical flipper buttons "
					"exist (cabinet switches 5 and 6). The two lower-flipper button bits are recorded "
					"separately at 82 and 84, because PinMAME copies them into the ROM-read "
					"switches 6 and 5."
				)
			},
			spatial=not_applicable("virtual", CORE_SOURCE),
		)
	)
	for rom_address, (host, side, bit) in sorted(FLIPPER_BUTTON_HOST_INPUTS.items(), key=lambda item: item[1][0]):
		items.append(
			_device(
				f"switch.flipper-column-{host}",
				f"{side.capitalize()} Flipper Button Host Input",
				"virtual",
				"pinmame.input.switch",
				host,
				"used",
				(CORE_SOURCE, CONTROLLER_SOURCE, VPX_SCRIPT_SOURCE, VPM_LIBRARY_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(host)}],
				physical={
					"notes": (
						f"PinMAME's {side} flipper button bit {bit} in the flipper column, public "
						f"{host} by cc_m2sw. bbb108 and bbb109 declare FLIP_SWNO(5,6), and with "
						"keyboard handling off (LibPinMAME's default, and the retained table's "
						"HandleKeyboard = 0) core_updateSw reads this bit and writes it into matrix "
						f"switch {rom_address} every frame (src/wpc/core.c, 'set switches in matrix "
						f"for non-fliptronic games'). A host therefore presses the physical {side} "
						f"flipper button (switch.cabinet-{rom_address}) by driving {host}; a direct "
						f"write to {rom_address} lasts at most one frame. The retained table does "
						"exactly this: its flipper keys reach Capcom.VBS's vpmKeyDown/vpmKeyUp, "
						f"which write swL{side[0].upper()}Flip = {host}. The bit has no playfield "
						"object; the button it stands for is a cabinet device."
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
		if address == 22:
			# The location table prints CL00109 for this row, but the assembly's own parts
			# list proves no coil exists; the bulbs are the flasher-lamp part the sibling
			# flasher rows print.
			physical["part_number"] = "LP00101"
		else:
			part = SOLENOID_PART_NUMBERS.get(address)
			if part:
				physical["part_number"] = part
		notes = f"Manual/schematic Ref./S{address} ({label})."
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script: {SOLENOID_CALLBACKS[address]}."
		if address == 22:
			notes += (
				" Schematic sheet 7 draws S22 feeding TWO device symbols in parallel from one "
				"connector pin (VIO/BLU, J20/J21 pin 6): the Tube Dancer flasher effect at the "
				"playfield tube and the Backbox Right flasher, resolving the manual's page-82 "
				"unnumbered 'BACKBOX RIGHT (FLASHER)' row (it shares this address with 'TUBE "
				"DANCER' rather than being a numbering gap). Both symbols are the circular bulb "
				"shape, PinMAME's MACHINE_INIT types all of 21-26 as flasher-bulb outputs, and "
				"both retained recreations bind 22 to a flasher lamp only. The Tube Lady "
				"Assembly's own parts list (printed page 109) settles the construction question "
				"definitively: the assembly contains NO coil -- sub-assembly 1 is "
				"'ASSEMBLY, MOTOR, TUBE LADY' (1A SM00221 COUPLING, SHAFT; 1F MR00108 MOTOR, 12 "
				"VDC, 65 RPM -- the same part number the solenoid table prints for the Ref. "
				"30/31/32 motors) driving the 2E belt assembly and 2F figure through the 2G "
				"clear tube. The location table's CL00109 coil part number printed for Ref. 22 "
				"is a manual-internal error against its own parts list, recorded here rather "
				"than resolved by inventing a second device. Address 22 is a flasher output "
				"driving two bulb locations: this playfield tube-dancer flasher, and the "
				"backbox-right flasher (a backbox device with no playfield coordinate; "
				"callout 22 appears in both the backbox box and the playfield circle on the "
				"printed page-82 diagram)."
			)
		if address in (9, 10, 11):
			notes += (
				" The physical flipper coil. The retained script's native SolCallback is "
				"commented out and its symbolic flipper bindings resolve to never-written "
				"hold-side mirror addresses under the installed VPinMAME script library (see "
				"output 45/47), so the ROM drives this coil while the retained table animates "
				"the bat from its own key handlers."
			)
		if address in (4, 5):
			notes += (
				" The physical slingshot coil (CL00109, callout 4/5 on the manual's printed "
				"page-82 playfield diagram). The retained table models the slingshot as a "
				"passive rubber wall with no coil object and binds no SolCallback, so the "
				"coordinate is a documented projection onto the wall assembly (see the "
				"placement note)."
			)
		if address in (18, 19, 20):
			notes += (
				" Star-bumper identity is validated by the manual's own printed page-82 "
				"playfield diagram, which marks callout 18 leftmost, 20 upper-right and 19 "
				"lower-centre -- matching this definition's switch/lamp geometry for the same "
				"three bumpers (switches 54/55/56) and both retained recreations' bumper "
				"object positions. Which Bumper1/Bumper2/Bumper3 VPX object each callback "
				"would have driven is a retained-table detail only (the script comments these "
				"callbacks out)."
			)
		if address in (14, 15):
			notes += (
				" The physical diverter coil. The retained tables' Flipper-type "
				"DivTubef/DivTube2f rotation helpers are is_visible=false animation primitives "
				"parked at the front apron in both recreations and are excluded from placement "
				"consideration; the drop-wall panels are the physical mechanism (see the "
				"placement note and the printed page-82 diagram's callouts 14/15 at the "
				"playfield's rear)."
			)
		if address == 3:
			notes += (
				" Backbox knocker: the manual's printed page-82 playfield diagram marks "
				"callout 3 inside the backbox box (top-right). Sound-only in the retained "
				"script (vpmSolSound); no table object."
			)
		if address == 21:
			notes += f" {SOLENOID_BACKBOX_ADDRESSES[21]}"
		physical["notes"] = notes
		aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}]
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical}
		if address in SOLENOID_ROLES:
			extra["roles"] = SOLENOID_ROLES[address]
		if address == 21:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 3:
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, SCHEMATIC_SOURCE)
		elif address in SOLENOID_PROJECTION_PLACEMENTS:
			reason, positions, refs = SOLENOID_PROJECTION_PLACEMENTS[address]
			physical["notes"] += f" Placement: {reason}"
			extra["spatial"] = located(identifier, "effect", positions, *refs)
		elif address in SOLENOID_MECHANISM_PROJECTIONS:
			reason, positions, refs = SOLENOID_MECHANISM_PROJECTIONS[address]
			physical["notes"] += f" Placement: {reason}"
			extra["spatial"] = located(identifier, "effect", positions, *refs)
		elif address in SOLENOID_DIVERTER_PLACEMENTS:
			reason, positions, refs = SOLENOID_DIVERTER_PLACEMENTS[address]
			physical["notes"] += f" Placement: {reason}"
			extra["spatial"] = located(identifier, "effect", positions, *refs)
		elif address in SOLENOID_POSITIONS:
			role = "emitter" if kind == "flasher" else "effect"
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE)
		refs = (MANUAL_SOURCE, SCHEMATIC_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, SCHEMATIC_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))

	for address, label in VIRTUAL_SOLENOID_LABELS.items():
		identifier = output_id(label)
		availability = "used" if address in (33, 35, 45, 47, 51) else "unused"
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
		if address in LAMP_CABINET_ROLES:
			extra["roles"] = LAMP_CABINET_ROLES[address]
		if address in LAMP_CABINET_ADDRESSES:
			physical["notes"] += f" {LAMP_CABINET_ADDRESSES[address]}"
			if address in (1, 2):
				physical["quantity"] = 2
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE, SCHEMATIC_SOURCE)
		elif address in LAMP_CORROBORATION_POSITIONS:
			x, y, reason = LAMP_CORROBORATION_POSITIONS[address]
			physical["notes"] += f" Placement: {reason}"
			if address == 125:
				physical["quantity"] = 2
			extra["spatial"] = located(identifier, "emitter", [(x, y)], CORROBORATION_TABLE_SOURCE, MANUAL_SOURCE)
		elif address == 62:
			x, y, reason = LAMP_ELECTRO_BLACK_LIGHT_PROJECTION
			physical["notes"] += f" Placement: {reason}"
			extra["spatial"] = located(identifier, "emitter", [(x, y)], MANUAL_SOURCE, VPX_TABLE_SOURCE)
		elif address == 87:
			physical["quantity"] = 2
			physical["notes"] += (
				" The schematic's matrix-B sheet marks this address X2 -- two #44 bulbs in "
				"parallel (the sheet set's own detail legend shows the two-bulb circuit); the "
				"retained table models one Light object at the free-shot outlane area, so the "
				"placement records the modelled socket and the second parallel bulb's socket "
				"position is not individually surveyed."
			)
			extra["spatial"] = located(identifier, "emitter", [LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
		elif address in LAMP_POSITIONS:
			position = LAMP_POSITIONS[address]
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
				roles=LAMP_CABINET_ROLES[address],
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
				spatial=not_applicable("virtual", CORE_SOURCE),
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
				"One reversible DC gearmotor (Alien Mech Assembly parts list, printed page 105, "
				"with its exploded drawing on printed page 104: "
				"one motor item driving two gears on two independent shafts, each carrying one alien "
				"figure) drives both alien figures together through a 32-step position counter "
				"(retained script ALockTimer_timer, OldPos/NewPos 0-31). Switch 57 (Alien Motor, opto, "
				"blank switch part) toggles through a repeating home/quarter/half/three-quarter-turn "
				"notch pattern as the counter advances -- the mechanism's own parts list carries the "
				"MT00501 encoder disc read by the A0020000 slotted-opto PCB assembly, and the "
				"diagnostic C2-02 Alien Motor calibration test confirms one motor calibrated at two "
				"power levels with a 'Can't Find Home Position' failure mode tied to 'the opto "
				"(which reads the encoder wheel)', matching this switch's role. Solenoids 31/32 "
				"(Aliens Forward/Reverse) are this one gearmotor's two drive-direction outputs, not "
				"two independent motors. Solenoid 16 (Alien Lock Post) raises/lowers a separate "
				"ball-lock post sensed by switches 61/62 (Alien Lock Left/Right, SW00146); the "
				"retained script's sw61_Hit/sw62_Hit handlers set AlienLBall/AlienRBall lock-state "
				"flags independently of the rotating figures' own position."
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
				"The Tube Lady Assembly parts list (printed page 109) and its exploded drawing "
				"(printed page 108) prove a purely motorized mechanism with no coil anywhere: "
				"sub-assembly 1 (A-00649, 'ASSEMBLY, MOTOR, TUBE LADY') is the 1F MR00108 motor "
				"(12 VDC, 65 RPM -- the same part number the solenoid table prints for the "
				"Ref. 30/31/32 motors) driving through the 1A SM00221 shaft coupling (the "
				"cylindrical part an earlier curation misread off the drawing as a coil) and the "
				"1G motor shaft; sub-assembly 2 (A-00650, 'ASSEMBLY, TUBE LADY') is the 2G clear "
				"tube, 2D base, 2B insert shaft, 2C wireform, and the 2E belt assembly carrying "
				"the 2F figure. The assembly stands on the playfield at the rear-left circle the "
				"printed page-82 diagram marks with callouts 22/30 (corroborated by the retained "
				"IPDB photograph showing the figure in its tube beside the tube-sign rollovers). "
				"Solenoid 30 is the motor's single drive output (the retained script's solDancer "
				"enables a continuous wobble-rotation timer while energized); address 22 drives "
				"the feature's flasher effect at the tube plus the Backbox Right flasher in "
				"parallel (two bulb symbols on schematic sheet 7; the location table's CL00109 "
				"cell for Ref. 22 is a manual-internal error against its own parts list). The "
				"diagnostics section's C2 tests cover the alien motor but define no tube-dancer "
				"coil test, consistent with the parts list."
			),
			MANUAL_SOURCE, SCHEMATIC_SOURCE, VPX_SCRIPT_SOURCE, IPDB_PHOTO_TUBE_LADY_SOURCE,
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
			"(printed page 102) documents one coil per diverter. The manual's printed page-82 "
			"playfield diagram marks callout 14 at the rear-left playfield edge and callout 15 at "
			"the top-centre-left ramp, and both retained recreations model the physical halves as "
			"drop-wall panels there (DivTube/DivTube1 for 14; DivTube2 for 15 in the earlier "
			"recreation, whose coordinate the VPW v1.0 table's same-named wall contradicts by "
			"~0.17 normalized units and is disclosed on the placement). The tables' Flipper-type "
			"DivTubef/DivTube2f gate-arm objects are is_visible=false rotation-animation helpers "
			"parked at the front apron in both recreations -- table artifacts, not device "
			"locations."
		),
		MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORROBORATION_TABLE_SOURCE,
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
	"""The 2026-08-07 curation carried four first-class conflicts; every one has since
	been resolved by evidence obtained within the retained document set and the
	contributor's own working installation, so the promoted definition carries none:

	1. conflict.flipper-mirror-address-left-right-naming -- the symbolic
	   sLRFlipper/sLLFlipper values are environment-owned core.vbs constants naming the
	   hold-side addresses (46/48/34/36), which capcom.c never writes; the retained
	   table's flipper callbacks are dead bindings under that library (a
	   consumed-table defect recorded on outputs 45/47), while the machine-level
	   45->S9-Left / 47->S10-Right mirror binding was always consistent across
	   capcom.c, the manual and schematic sheet 7.
	2. conflict.solenoid-35-eject-hole-mirror-mislabeled -- capcom.c's single io_w
	   write site makes the 35-repeats-12 mirror structural; the manual and schematic
	   agree on the machine's wiring and the emulator-facing name is the driver's own
	   admitted defect (recorded on output 35).
	3. conflict.solenoid-22-shared-device-construction -- the Tube Lady Assembly's own
	   parts list (printed page 109) contains no coil: item 1A is SM00221 COUPLING,
	   SHAFT and the drive is the 1F MR00108 motor through a belt; address 22 is
	   flasher-only, exactly as the schematic's bulb symbols, PinMAME's output typing
	   and both retained recreations bind it (recorded on output 22).
	4. conflict.ramp-diverter-geometry-inconsistent -- the retained tables'
	   DivTubef/DivTube2f gate-arm objects are is_visible=false animation helpers
	   parked at the front apron, not device locations; the drop-wall panels agree
	   with the manual's printed page-82 callouts 14/15 at the playfield rear, and
	   both diverters now carry validated placements (recorded on outputs 14/15).
	"""
	return []




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
			"opdb_id": "G56vo-MLl1Z",
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
		"knowledge": {"path": "knowledge/capcom/big-bang-bar-1996.md", "status": "complete"},
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
		"format": "pinmame-spatial-audit",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [],
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
			"corroboration_table_sha256": CORROBORATION_TABLE_SHA256,
			"corroboration_script_sha256": CORROBORATION_SCRIPT_SHA256,
			"vpm_core_library_sha256": VPM_CORE_LIBRARY_SHA256,
			"vpm_capcom_library_sha256": VPM_CAPCOM_LIBRARY_SHA256,
			"ipdb_tube_lady_photo_sha256": IPDB_TUBE_LADY_PHOTO_SHA256,
			"ipdb_overhead_photo_sha256": IPDB_OVERHEAD_PHOTO_SHA256,
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
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, (reason, _, _) in sorted({**SOLENOID_PROJECTION_PLACEMENTS, **SOLENOID_MECHANISM_PROJECTIONS, **SOLENOID_DIVERTER_PLACEMENTS}.items())
		]
		+ [
			{"group": "pinmame.output.lamp", "address": 62, "reason": LAMP_ELECTRO_BLACK_LIGHT_PROJECTION[2]},
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
			"corroboration_cited_files": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/corroboration-table-cited/",
				"files": dict(sorted(CORROBORATION_CITED_FILES.items())),
			},
			"vpm_script_libraries": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/vpm-script-libs/",
				"core_vbs_sha256": VPM_CORE_LIBRARY_SHA256,
				"capcom_vbs_sha256": VPM_CAPCOM_LIBRARY_SHA256,
			},
			"ipdb_photos": {
				"path": "external:pinmame-review-artifacts/big-bang-bar/ipdb-photos/",
				"tube_lady_sha256": IPDB_TUBE_LADY_PHOTO_SHA256,
				"overhead_sha256": IPDB_OVERHEAD_PHOTO_SHA256,
			},
		},
		"excluded_object_classes": [
			"Flipper.DivTubef/DivTube2f (solenoids 14/15) -- is_visible=false rotation-animation helpers parked at the front apron (y~=0.98-0.99) in BOTH retained recreations; table artifacts, never physical device locations (the physical halves are the drop-wall panels, placed)",
			"F21-F26 flasher Light objects reported under their owning solenoid address (21-26), never as a separate lamp address",
			"Light L01/L02 and the VPW L62 wash mesh -- room-render glow proxies far outside the playfield bounds; the physical coin-door lamps (1/2) carry controlled cabinet records and the black light (62) carries a documented feature-centroid projection",
			"Primitive.PinCab_Start_Button / VR start-button props -- cabinet render objects bound to lamp 3 by the retained script, consistent with its cabinet disposition",
		],
		"unresolved": [],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Big Bang Bar (Capcom, 1996) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record is `author_ready` at "
		"`machines/author-ready/capcom/big-bang-bar-1996.json`: every address is a validated "
		"placement or a controlled `not_applicable` record, and no unresolved conflict remains.",
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
		"source found, and the Tube Lady Assembly's own parts list on printed page 109 is the "
		"decisive construction source for that mechanism); pinned PinMAME source owns controller "
		"topology and per-game hardware metadata; the retained tables supply geometry.",
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
		"- Solenoid coils whose retained-table objects are the assembly they actuate (the two "
		"slingshot coils, the three flipper coils, and the two ramp-diverter drop walls) are "
		"documented projections onto those objects, each corroborated by the manual's printed "
		"page-82 numbered playfield diagram (balloon-centre tolerance ~0.02-0.05, measurement "
		"record committed with the diagram excerpt).",
		"- The manual's own parts lists settle the two construction questions the 2026-08-07 "
		"curation left open: the Tube Lady Assembly contains no coil (item 1A is a shaft "
		"coupling; the drive is the MR00108 motor through a belt), and the alien mechanism's "
		"position sensor is the A0020000 slotted-opto PCB reading the MT00501 encoder disc.",
		"- Cabinet lamps 1/2 (coin door, X2) and 3 (START, which the retained script binds to the "
		"cabinet start button) carry controlled `cabinet_or_service` records; the retained "
		"tables' out-of-bounds glow proxies for them are excluded as modeling artifacts.",
		"- Lamp 62 ((Electro) Black Light) carries a documented projection onto the (Electro) Ramp "
		"feature's centroid; lamps 38/125 carry coordinates from the earlier retained recreation "
		"where the primary table models no object, each corroborated by same-feature geometry.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled "
		"`not_applicable` with both PinMAME core and manual provenance.",
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
		"Every used address carries a validated placement or a controlled `not_applicable` "
		"record; `conflicts` is empty; the six capInvSw10-normalized switch addresses all carry "
		"positive manufacturer construction evidence (trough opto board part numbers, the "
		"'opto spinner' scoring text, and the alien mechanism's encoder disc + opto PCB); the "
		"star-bumper solenoid identity is the manual diagram's own callout positions; and the "
		"four former conflicts are resolved with the resolutions documented on the affected "
		"devices and in the curator's conflicts() docstring. The record is promoted to "
		"`author_ready` with `coverage.missing = []` and every coverage dimension validated.",
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
		f"- Corroboration recreation table SHA-256 `{CORROBORATION_TABLE_SHA256}` and its embedded "
		f"script SHA-256 `{CORROBORATION_SCRIPT_SHA256}`, with the cited gameitems pinned under "
		"external:pinmame-review-artifacts/big-bang-bar/corroboration-table-cited/.",
		f"- VPinMAME script libraries core.vbs SHA-256 `{VPM_CORE_LIBRARY_SHA256}` and Capcom.VBS "
		f"SHA-256 `{VPM_CAPCOM_LIBRARY_SHA256}` under "
		"external:pinmame-review-artifacts/big-bang-bar/vpm-script-libs/.",
		f"- IPDB machine-4001 photographs SHA-256 `{IPDB_TUBE_LADY_PHOTO_SHA256}` (tube lady on "
		f"the playfield) and `{IPDB_OVERHEAD_PHOTO_SHA256}` (overhead playfield) under "
		"external:pinmame-review-artifacts/big-bang-bar/ipdb-photos/.",
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