"""Curate the physical Stern The Simpsons Pinball Party (2003) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring
detail, and normalized coordinate as a literal, so regeneration reproduces the canonical
artifact byte-for-byte without reading the external evidence roots. ``--check`` refuses
drift, and ``--regenerate`` is the only path that writes the canonical definition and its
pinned seed.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text


ROOT = Path(__file__).resolve().parents[1]
# This record stays partial for two reasons. Public lamps 81-96 are published by pinned
# PinMAME (hw.lampCol = 4 gives twelve lamp columns) and fed only by CPU writes to ports
# $3406/$3407, which no retained source ties to hardware, so their availability is unknown
# (output_semantics). And lamp 80 is two red LEDs (L8 bottom-left, L9 bottom-right of the
# mode sign) while every retained table models one, so its second emitter has no coordinate
# (spatial_placement). Both former conflicts were settled on 2026-09-25: switches 14/15 by
# the known-working script and hash-pinned ROM runs, DS-5 (public 88) by the manual's own
# doubled right-button drawing and a ROM run showing it fires solenoids 13 and 14.
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/the-simpsons-pinball-party-2003.json"
PARTIAL_PATH = ROOT / "machines/partial/stern/the-simpsons-pinball-party-2003.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/stern/the-simpsons-pinball-party-2003.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/stern/the-simpsons-pinball-party-2003.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/stern/the-simpsons-pinball-party-2003.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-whitestar"
MANUAL_SOURCE = "manual.stern.the-simpsons-pinball-party.2003"
MANUAL_SUPPORT_SOURCE = "manual-support.stern.the-simpsons-pinball-party.2003"
VPX_TABLE_SOURCE = "vpx-table.simpsons-party-0-8-2"
VPX_SCRIPT_SOURCE = "vpx-script.simpsons-party-0-8-2"
VPX_EXTRACTION_SOURCE = "vpx-extraction.simpsons-party-0-8-2"
PINNED_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
PINNED_CORE_SOURCE = f"pinmame.core.{PINNED_REVISION[:12]}"
VPM_CORE_SOURCE = "vpm-script-library.core-vbs-3-61"
RUNTIME_STACKING = "runtime.simpsons-pinball-party.stacking-opto"
RUNTIME_STACKING_PATH = "evidence/runtime/whitestar/simpsons-pinball-party-stacking-opto.json"
RUNTIME_FLIPPERS = "runtime.simpsons-pinball-party.flipper-buttons"
RUNTIME_FLIPPERS_PATH = "evidence/runtime/whitestar/simpsons-pinball-party-flipper-buttons.json"
VPM_CORE_SHA256 = "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"

TABLE_SHA256 = "c7d14c512ae81eb0e26cddf9f74690818ae2259350cd334fc98be5e7ece79034"
SCRIPT_SHA256 = "5378f6baf3106ed013c6d1a787f4b6789bc1febe925903f05cb2eda9327b98ee"
MANUAL_SHA256 = "412023c67f699d68c10c6a70120712d34d71417b7dd16f1662e252a66561c898"
MANUAL_TRANSCRIPTION_SHA256 = "18a1d499a3525bd72340f0e5a98af98c3fb8b867f0f3b1b655242f5cc7ef37e8"

EXTRACTION_RELATIVE_PATH = Path("stern/the-simpsons-pinball-party-2003/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("stern/the-simpsons-pinball-party-2003/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "9f21a0b4af3387d3b7b3dbd7480909d141c2cfeb00c6c9b59f417723918338bc"
EXTRACTION_FILE_COUNT = 1348
EXTRACTION_TOTAL_BYTES = 167511025

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=2115"

DRIVER_IDS = (
	"simpprty", "simpprtf", "simpprtg", "simpprti", "simpprtl",
	"simp400", "simp400f", "simp400g", "simp400i", "simp400l",
	"simp300", "simp300f", "simp300i", "simp300l",
	"simp204", "simp204f", "simp204i", "simp204l",
)
DRIVER_COMPATIBILITY = {
	driver_id: (
		"identical",
		"Stern Whitestar game-ROM revision/localization for the same physical machine; the "
		"switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are "
		"unchanged. simpprty is the shipped 5.00 production ROM this driver family's static "
		"core_tGameData (simpprtyGameData) is shared by every clone through CORE_CLONEDEFNV."
		+ (
			"" if driver_id == "simpprty" else
			" One emulator-side difference: se.c publishes the fast-flip/game-on state at public "
			"solenoid 15 only when the running driver's own name matches \"simpprty\" in its first "
			"eight characters, so on this driver public 15 stays at zero."
		),
	)
	for driver_id in DRIVER_IDS
}

# --- Printed switch matrix (manual PDF page 30, printed page 16).
SWITCH_LABELS = {
	9: "Comic Book Guy Standup", 10: "5-Ball Trough #1 (Left)", 11: "5-Ball Trough #2",
	12: "5-Ball Trough #3", 13: "5-Ball Trough #4", 14: "5-Ball Trough VUK Opto",
	15: "5-Ball Stacking Opto", 16: "Shooter Lane",
	17: "Drop Target #1 (Top)", 18: "Drop Target #2 (Mid)", 19: "Drop Target #3 (Bot)",
	20: "Itchy & Scratchy Saucer", 21: "Spinner", 22: "Bart Skateboard Top",
	23: "Bart Skateboard", 24: "Upper Right Saucer",
	25: "Upper Playfield Exit", 26: "Garage Ramp Enter", 29: "Kwik-E-Mart Loop",
	30: "Kwik-E-Mart Standup", 31: "Adv. Pops Standup", 32: "Light Otto Standup",
	33: "UPF Light Standup", 34: "UPF Lock Standup", 35: "UPF Top Standup",
	36: "Couch Enter", 37: "TV Lockup", 38: "Couch Lock (Bot)", 39: "Couch Lock (Mid)",
	40: "Couch Lock (Top)",
	41: "Bully 3-Bank (Top)", 42: "Bully 3-Bank (Mid)", 43: "Bully 3-Bank (Bot)",
	44: "Up Right Saucer Backup", 45: "Right Ramp Enter", 46: "Right Ramp Made",
	47: "Left Ramp Enter", 48: "Garage Door",
	49: "Left Bumper", 50: "Right Bumper", 51: "Bottom Bumper", 52: "Pop Side Standup",
	55: "Upper Left VUK", 57: "Left Outlane", 58: "Left Return Lane", 59: "Left Slingshot",
	60: "Right Outlane", 61: "Right Return Lane", 62: "Right Slingshot", 63: "Left Orbit",
	64: "Right Orbit",
}
# Coin-door and cabinet matrix positions handled with dedicated roles/spatial below.
CABINET_MATRIX_LABELS = {
	1: "Left Button (UK Only)", 8: "Right Button (UK Only)",
	2: "4th Coin Slot", 4: "Right Coin Slot", 5: "Center Coin Slot / DBA", 6: "Left Coin Slot",
	3: "6th Coin Slot", 7: "5th Coin Slot",
	53: "Tournament Button", 54: "Start Button", 56: "Plumb Bob Tilt",
}
UNUSED_MATRIX_ADDRESSES = {27, 28}
# Manual footnote "Sw. 14 & 15 Part Note": the only two switches this manual identifies as
# opto construction anywhere in the document (no shaded-cell legend exists on this manual's
# switch-matrix page; see evidence/excerpts/.../switch-locations-footnotes.md). The switch-
# location drawing stamps them together as "14:15" at the trough's right-hand exit end.
OPTO_SWITCHES = {14, 15}
# Public sense of the two optos. se.c's switch_r returns ~core_getSwCol, so public 1 is what
# the CPU reads as a closed matrix contact. Switch 14 is the exit position of the retained
# script's bsTrough.InitSw 0,14,13,12,11,10,0,0, and core.vbs's cvpmBallStack writes
# Controller.Switch(position switch) = True for every occupied position, so the known-working
# table asserts 14 at 1 while a ball waits at the up-kicker. Switch 15 is settled by the
# RUNTIME_STACKING ROM runs (the ROM acts on 1 and is quiet at 0); the same script's
# SolRelease also pulses it to 1 as each kicked ball passes the stacking beam.
SCRIPT_EVIDENCED_OPTOS = {
	14: "its bsTrough.InitSw 0,14,13,12,11,10,0,0 makes 14 the trough's exit position, and "
	    "core.vbs 3.61's cvpmBallStack.SetSw writes Controller.Switch(14) = True whenever a ball occupies it "
	    "and False once KickOut clears position 1",
	15: "its SolRelease pulses it with vpmTimer.PulseSw 15 each time the up-kicker fires, "
	    "asserting 1 while the kicked ball passes the stacking beam",
}
HARNESS_EVIDENCED_OPTOS = {15}
# The eight mode-sign LEDs (lamps 73-80) sit on LED PCB (Mode Signifier) 520-5225-00, bolted to
# the back panel next to the TV (manual PDF 82, 114, 170). The sign is vertical and faces the
# player, so L1-L7 (lamps 73-79) stack in one column and project onto one playfield point; each
# lamp is placed at its own retained Primitive's position (l73-l79, x/952, y/2115), which
# differ only in height (z 305 down to 185 in 20-unit steps). Lamp 80 is two red LEDs, L8 at
# the bottom-left and L9 at the bottom-right of the plastic; every retained table models one
# object (l80, z 165), so lamp 80 carries no spatial key rather than a one-of-two placement.
MODE_SIGN_LAMP_POSITIONS: dict[int, tuple[float, float]] = {
	73: (0.576284, 0.034467), 74: (0.57628, 0.03446), 75: (0.576295, 0.034466), 76: (0.576286, 0.034485),
	77: (0.576341, 0.034505), 78: (0.576309, 0.034468), 79: (0.57633, 0.034485),
}
MODE_SIGN_LED = {73: "L1", 74: "L2", 75: "L3", 76: "L4", 77: "L5", 78: "L6", 79: "L7", 80: "L8 and L9"}
# hw.lampCol = 4 makes PinMAME publish twelve lamp columns, public 1-96 (se.c:425 nLamps =
# 64 + lampCol*8; vpintf.c vp_getChangedLamps scans CORE_STDLAMPCOLS + lampCol columns). The
# printed 8x10 matrix fills 1-80; 81-88 and 89-96 are coreGlobals.lampMatrix[10]/[11], written
# only by se.c's gilamp_w when the CPU writes port $3406/$3407.
AUX_PORT_LAMP_ADDRESSES = range(81, 97)
# core.c:2455 memcpy's coreGlobals.invSw from core_gameData->wpc.invSw, and
# simpprtyGameData's positional-aggregate initializer never sets the trailing wpc/sxx struct
# members, so that array is all-zero: PinMAME applies ZERO switch-matrix inversion for this
# driver. Confirmed platform-wide: `grep -rn invSw src/wpc/segames.c` matches nothing in the
# whole ~3600-line Whitestar game-table file, so no SE/Whitestar game ever populates invSw.
PINMAME_NORMALIZED_OPTO_SWITCHES: set[int] = set()
# Positions printed "Future Use" (address wired but no coin-slot hardware fitted by default).
FUTURE_USE_MATRIX_ADDRESSES = {3, 7}
# Regional (UK-only) cabinet buttons, printed but not part of the base configuration.
OPTIONAL_MATRIX_ADDRESSES = {1, 8, 53}
# vpmTimer.PulseSw callers in the retained script (momentary/pulsed switches).
PULSED_SWITCHES = {9, 21, 30, 31, 32, 33, 34, 35, 41, 42, 43, 45, 46, 47, 52}

SWITCH_TYPES = {
	9: "microswitch", 10: "microswitch", 11: "microswitch", 12: "microswitch",
	13: "microswitch", 14: "opto", 15: "opto", 16: "microswitch",
	17: "microswitch", 18: "microswitch", 19: "microswitch", 20: "microswitch",
	21: "other", 22: "microswitch", 23: "microswitch", 24: "microswitch",
	25: "microswitch", 26: "microswitch", 29: "microswitch", 30: "microswitch",
	31: "microswitch", 32: "microswitch",
	33: "microswitch", 34: "microswitch", 35: "microswitch", 36: "microswitch",
	37: "microswitch", 38: "microswitch", 39: "microswitch", 40: "microswitch",
	41: "microswitch", 42: "microswitch", 43: "microswitch", 44: "microswitch",
	45: "microswitch", 46: "microswitch", 47: "microswitch", 48: "microswitch",
	49: "microswitch", 50: "microswitch", 51: "microswitch", 52: "microswitch",
	55: "microswitch", 57: "microswitch", 58: "microswitch", 59: "leaf",
	60: "microswitch", 61: "microswitch", 62: "leaf", 63: "microswitch", 64: "microswitch",
}
CABINET_SWITCH_TYPES = {
	1: "button", 8: "button", 2: "other", 4: "other", 5: "other", 6: "other",
	3: "other", 7: "other", 53: "button", 54: "button", 56: "tilt",
}

# address -> printed switch part number (None where the manual prints no part, e.g. a
# footnote reference).
SWITCH_PARTS = {
	1: "180-5160-00", 2: "180-5204-00", 3: None, 4: "180-5204-00", 5: "180-5204-00",
	6: "180-5204-00", 7: None, 8: "180-5160-00",
	9: "515-6027-08", 10: "180-5119-02", 11: "180-5119-02", 12: "180-5119-02",
	13: "180-5119-02", 14: None, 15: None, 16: "180-5157-00",
	17: "180-5158-00", 18: "180-5158-00", 19: "180-5158-00", 20: "180-5116-01",
	21: "180-5010-04", 22: "180-5190-48", 23: "180-5190-48", 24: "180-5186-00",
	25: "180-5190-28", 26: "180-5190-28", 29: "500-6227-02", 30: "500-6227-02",
	31: "500-6227-02", 32: "500-6227-02",
	33: "515-5966-04", 34: "515-5966-04", 35: "515-5966-02", 36: "180-5190-28",
	37: "500-6227-02", 38: "180-5119-02", 39: "180-5119-02", 40: "180-5119-02",
	41: "515-6027-08", 42: "515-6027-08", 43: "515-6027-08", 44: "180-5119-02",
	45: "180-5190-28", 46: "180-5190-28", 47: "180-5190-28", 48: "500-6138-01R",
	49: "180-5015-03", 50: "180-5015-03", 51: "180-5015-03", 52: "515-6027-08",
	53: "180-5174-00", 54: "180-5174-00", 55: "180-5116-01", 56: None,
	57: "500-6227-02", 58: "500-6227-02", 59: "180-5054-00 (x2)", 60: "500-6227-02",
	61: "500-6227-02", 62: "180-5054-00 (x2)", 63: "500-6227-02", 64: "500-6227-02",
}
# Cells additionally marked "Diode On Terminal Strip" on the printed matrix.
DOTS_MATRIX_ADDRESSES = {17, 18, 19, 20}
# Row/column drive-and-return wiring, printed matrix page (PDF 30).
SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "CN5-P1", "Q1"), 2: ("Green-Red", "CN5-P3", "Q2"),
	3: ("Green-Orange", "CN5-P4", "Q3"), 4: ("Green-Yellow", "CN5-P5", "Q4"),
	5: ("Green-Black", "CN5-P6", "Q5"), 6: ("Green-Blue", "CN5-P7", "Q6"),
	7: ("Green-Violet", "CN5-P8", "Q7"), 8: ("Green-Gray", "CN5-P9", "Q8"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "CN7-P9", "U400"), 2: ("White-Red", "CN7-P8", "U400"),
	3: ("White-Orange", "CN7-P7", "U400"), 4: ("White-Yellow", "CN7-P6", "U400"),
	5: ("White-Green", "CN7-P5", "U401"), 6: ("White-Blue", "CN7-P3", "U401"),
	7: ("White-Violet", "CN7-P2", "U401"), 8: ("White-Gray", "CN7-P1", "U401"),
}
# Dedicated switch wiring, printed matrix page GROUND/IC U206 INPUTS block.
DEDICATED_SWITCH_WIRING = {
	84: ("Gray-Brown", "CN6-P2"), 83: ("Gray-Red", "CN6-P3"), 82: ("Gray-Orange", "CN6-P4"),
	81: ("Gray-Yellow", "CN6-P6"), 88: ("Gray-Green", "CN6-P7"), -2: ("Gray-Blue", "CN6-P8"),
	-1: ("Gray-Violet", "CN6-P9"), 0: ("Gray-Black", "CN6-P10"),
}
DEDICATED_SWITCH_LABELS = {
	84: ("Left Flipper Button", "DS-1", "flipper.lower.left.button", "180-5160-00", "button"),
	83: ("Left Flipper E.O.S.", "DS-2", "internal.flipper.lower.left.eos", "180-5149-00 on Flipper", "leaf"),
	82: ("Right Flipper Button", "DS-3", "flipper.lower.right.button", "180-5164-00 Doubled", "button"),
	81: ("Right Flipper E.O.S.", "DS-4", "internal.flipper.lower.right.eos", "180-5149-00 on Flipper", "leaf"),
	88: ("Upper Rt. Flipper Button", "DS-5", "flipper.upper.right.button", "180-5164-00 Doubled", "button"),
	-2: ("Volume (Red Button)", "DS-6", "service.down", "180-5192-02", "button"),
	-1: ("Serv. Cred. (Green Button)", "DS-7", "service.up", "180-5192-04", "button"),
	0: ("Begin Test (Black Button)", "DS-8", "service.enter", "180-5192-00", "button"),
}
# What the flipper-button run (RUNTIME_FLIPPERS) showed the ROM doing with each button, plus the
# construction facts that explain DS-5. The ROM owns every flipper here: hw.flippers declares
# FLIP_SOL(FLIP_L), so each coil below fires only because the ROM read the button.
_EOS_NOTE = (
	" Written by PinMAME, not by a host: simpprtyGameData declares FLIP_SOL(FLIP_L), which sets "
	"the lower-flipper FLIP_EOS bits, so core.c's end-of-stroke simulation rewrites this address "
	"every frame from the flipper coil's state (the flipper-button harness run shows it rising while "
	"the matching button is held). A recreation must leave it alone and drive only the buttons."
)
DEDICATED_SWITCH_NOTES = {
	81: _EOS_NOTE,
	83: _EOS_NOTE,
	84: (
		" With a game in progress the ROM answers this input alone by energising the lower left flipper "
		"(public 47/48) and solenoid 12, the upper mini-playfield's left flipper (hash-pinned harness run, "
		"see runtime.simpsons-pinball-party.flipper-buttons)."
	),
	82: (
		" With a game in progress the ROM answers this input alone by energising the lower right flipper "
		"(public 45/46) only; solenoids 13 and 14 stay off (hash-pinned harness run, see "
		"runtime.simpsons-pinball-party.flipper-buttons). Part 180-5164-00 Doubled: the right cabinet "
		"button carries a second contact, DS-5 (public 88), and the manual's switch-location drawing "
		"stamps DS-3 and DS-5 on the same button."
	),
	88: (
		" The second contact of the doubled right cabinet flipper button (part 180-5164-00 Doubled, the "
		"same part as DS-3; the manual's switch-location drawing stamps DS-3 and DS-5 on one right "
		"button), wired GRY-GRN to CN6-P7; it is not a separate button. se.c's dedswitch_r reads it as "
		"DED #5 from flipper-column bit 0x80 (the bit PinMAME's core.h calls CORE_SWULFLIPBUTBIT; its "
		"own source comment reads \"Not Used (Upper Flipper on some games!)\"). simpprtyGameData declares "
		"FLIP_SW(FLIP_L) only, so core.c's flipMask omits that bit and PinMAME never synthesizes public "
		"88 from its own keyboard handling; but core_updateSw rewrites only the bits inside flipMask and "
		"preserves the rest, so a host that writes public 88 reaches the ROM unchanged. A hash-pinned "
		"harness run with a game in progress shows the ROM answering 88 alone by energising solenoid 13 "
		"(UPF Right Flipper) and solenoid 14 (Top Right Flipper), and not the lower right flipper. A "
		"recreation must therefore drive 82 and 88 together from its right flipper button, as the "
		"physical doubled switch does; driving 82 alone leaves both upper-right flippers dead."
	),
}


# --- Normalized playfield coordinates derived from the retained VPX table extraction
# (x/952, y/2115; vpx-geometry.txt). Objects named "swNN"/"SWNN" bind directly to
# Controller.Switch(NN)/vpmTimer.PulseSw NN calls in the retained script.
SWITCH_POSITIONS: dict[int, list[tuple[float, float]]] = {
	9: [(0.284496, 0.362626)], 16: [(0.939282, 0.8812)],
	17: [(0.841389, 0.510159)], 18: [(0.85557, 0.538298)], 19: [(0.869724, 0.566933)],
	20: [(0.919662, 0.51358)], 21: [(0.873153, 0.334596)], 22: [(0.83638, 0.255916)],
	23: [(0.783215, 0.34016)], 24: [(0.843156, 0.212669)],
	25: [(0.324736, 0.239885)], 26: [(0.448229, 0.101437)], 29: [(0.302914, 0.149233)],
	30: [(0.352248, 0.195782)], 31: [(0.345683, 0.513749)], 32: [(0.208604, 0.596466)],
	33: [(0.174107, 0.109279)], 34: [(0.210347, 0.08753)], 35: [(0.31995, 0.028369)],
	36: [(0.190947, 0.037386)], 37: [(0.508004, 0.05061)],
	38: [(0.062792, 0.28393)], 39: [(0.064452, 0.259946)], 40: [(0.060717, 0.235234)],
	41: [(0.645745, 0.207544)], 42: [(0.63524, 0.238749)], 43: [(0.625787, 0.272319)],
	44: [(0.852425, 0.184991)],
	45: [(0.693276, 0.300503)], 46: [(0.627548, 0.048122)], 47: [(0.23392, 0.286257)],
	48: [(0.425044, 0.136436)],
	49: [(0.082799, 0.468807)], 50: [(0.302074, 0.482273)], 51: [(0.167804, 0.560972)],
	52: [(0.052354, 0.408489)],
	55: [(0.07153, 0.048448)], 57: [(0.061876, 0.750421)], 58: [(0.135647, 0.737638)],
	59: [(0.231191, 0.727249)], 60: [(0.850768, 0.751016)], 61: [(0.774656, 0.739985)],
	62: [(0.69015, 0.724369)], 63: [(0.138991, 0.139329)], 64: [(0.925746, 0.080332)],
	# 10-14 are the five-ball trough (bsTrough.InitSw 0,14,13,12,11,10,0,0); the shared
	# cvpmBallStack helper synthesizes their state from ball proximity to the release
	# kicker rather than exposing five separate playfield objects, so all five are
	# projected onto the trough mechanism's own kicker (BallRelease). Switch 15 (5-Ball
	# Stacking Opto, sharing the Sw.14/15 opto-PC-board note) has no dedicated object
	# either and is projected onto the same anchor.
	10: [(0.869901, 0.858728)], 11: [(0.869901, 0.858728)], 12: [(0.869901, 0.858728)],
	13: [(0.869901, 0.858728)], 14: [(0.869901, 0.858728)], 15: [(0.869901, 0.858728)],
}
SWITCH_PROJECTIONS = {
	10: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center): bsTrough.InitSw 0,14,13,12,11,10,0,0 reads all five trough positions through the shared cvpmBallStack helper's internal ball-queue logic, which exposes no separate playfield object per position.",
	11: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.",
	12: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.",
	13: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10.",
	14: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center); see switch 10. Switch 14 is also the trough VUK opto nearest the kicker (Sw. 14 & 15 Part Note).",
	15: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center): the 5-Ball Stacking Opto shares its Transmitter/Receiver OPTO PC Board note with switch 14 and has no dedicated playfield object in the retained extraction either.",
}

SOLENOID_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.869901, 0.858728)], 2: [(0.939551, 0.96666)], 3: [(0.066492, 0.280003)],
	4: [(0.85557, 0.538298)], 5: [(0.919662, 0.51358)], 6: [(0.07153, 0.048448)],
	7: [(0.508774, 0.061277)], 8: [(0.750992, 0.114326)],
	9: [(0.082799, 0.468807)], 10: [(0.302074, 0.482273)], 11: [(0.167804, 0.560972)],
	12: [(0.146008, 0.190544)], 13: [(0.519958, 0.103073)], 14: [(0.881561, 0.437677)],
	17: [(0.231191, 0.727249)], 18: [(0.69015, 0.724369)], 19: [(0.843156, 0.212669)],
	20: [(0.422957, 0.130954)],
	21: [(0.070504, 0.501178), (0.068826, 0.501003)],
	22: [(0.915957, 0.030272), (0.918495, 0.029516)],
	23: [(0.910896, 0.217616), (0.911209, 0.217718)],
	25: [(0.936124, 0.585242), (0.936114, 0.585205)],
	26: [(0.95557, 0.410025)],
	27: [(0.745782, 0.137667), (0.746155, 0.10312)],
	28: [(0.110869, 0.309826), (0.109282, 0.30992)],
	29: [(0.220923, 0.344955), (0.220927, 0.346212)],
	30: [(0.85557, 0.538298)],
	31: [(0.179229, 0.106751), (0.179478, 0.106711)],
	32: [(0.333227, 0.028891), (0.335623, 0.028533)],
	45: [(0.622557, 0.84258)], 46: [(0.622557, 0.84258)],
	47: [(0.287992, 0.842009)], 48: [(0.287992, 0.842009)],
}
SOLENOID_PROJECTIONS = {
	1: "Projected onto the five-ball trough's own release kicker (BallRelease, table object center): SolRelease pulses bsTrough.ExitSol_On, the shared cvpmBallStack ejector for the whole trough, not a fixed visible coil body.",
	4: "Projected onto the drop-target bank's own middle target (SW18/Drop Target #2, table object center): dtDrop.SolDropUp resets all three bank positions together and the retained table exposes no separate reset-bar mesh.",
	30: "Projected onto the drop-target bank's own middle target (SW18/Drop Target #2, table object center): SolDropBankTrips (dtDrop.Hit 1/2/3) trips all three bank positions together; see solenoid 4.",
}

# 1-70 base lamp-matrix Light objects (l18a/l19a are the retained table's own object names
# for matrix positions 18/19). Lamp 32 (Tournament Button) has no Light object at all --
# the retained script's UpdateLamps skips straight from NFadeL 31 to NFadeL 33 -- matching
# the manual's own "Optional with Tournament Kit" footnote for that position.
LAMP_POSITIONS: dict[int, list[tuple[float, float]]] = {
	1: [(0.062862, 0.715097)], 2: [(0.136615, 0.679376)], 3: [(0.457788, 0.851608)],
	4: [(0.777561, 0.68107)], 5: [(0.852648, 0.717957)], 6: [(0.890687, 0.626244)],
	7: [(0.238377, 0.622325)], 8: [(0.375094, 0.538737)], 9: [(0.695245, 0.510208)],
	10: [(0.706707, 0.532225)], 11: [(0.718626, 0.553971)], 12: [(0.728228, 0.575315)],
	13: [(0.765539, 0.599739)], 14: [(0.690423, 0.622341)], 15: [(0.742075, 0.637148)],
	16: [(0.205712, 0.486672)], 17: [(0.083679, 0.475017)], 18: [(0.302146, 0.486855)],
	19: [(0.173931, 0.563719)], 20: [(0.154629, 0.418044)], 21: [(0.379138, 0.437807)],
	22: [(0.07863, 0.31311)], 23: [(0.100019, 0.344326)], 24: [(0.119027, 0.371225)],
	25: [(0.413837, 0.390658)], 26: [(0.39439, 0.409993)], 27: [(0.742565, 0.412332)],
	28: [(0.703494, 0.439526)], 29: [(0.68892, 0.471203)], 30: [(0.613913, 0.489476)],
	31: [(0.957361, 0.921393)],
	33: [(0.399734, 0.332123)], 34: [(0.447864, 0.364783)], 35: [(0.480431, 0.343746)],
	36: [(0.512734, 0.371229)], 37: [(0.655513, 0.364874)], 38: [(0.616575, 0.397686)],
	39: [(0.675313, 0.401049)], 40: [(0.633864, 0.428295)], 41: [(0.344298, 0.249351)],
	42: [(0.373078, 0.272778)], 43: [(0.407553, 0.298767)], 44: [(0.450858, 0.16993)],
	45: [(0.419465, 0.208457)], 46: [(0.48574, 0.212133)], 47: [(0.45418, 0.239363)],
	48: [(0.923593, 0.219325)], 49: [(0.585051, 0.139051)], 50: [(0.552393, 0.176155)],
	51: [(0.613967, 0.177198)], 52: [(0.588098, 0.219489)], 53: [(0.577909, 0.258216)],
	54: [(0.564959, 0.295862)], 55: [(0.917512, 0.252545)], 56: [(0.909024, 0.281423)],
	57: [(0.512729, 0.657924)], 58: [(0.379795, 0.661519)], 59: [(0.493069, 0.616344)],
	60: [(0.439227, 0.669492)], 61: [(0.42455, 0.633539)], 62: [(0.481563, 0.701975)],
	63: [(0.333983, 0.722684)], 64: [(0.611777, 0.704346)], 65: [(0.223818, 0.170579)],
	66: [(0.217224, 0.133444)], 67: [(0.253728, 0.110979)], 68: [(0.300005, 0.08935)],
	69: [(0.341266, 0.111958)], 70: [(0.344673, 0.065322)],
}

# --- Printed Coils Detailed Chart Table (manual PDF pages 32/34, printed 18/20).
SOLENOID_LABELS = {
	1: "Trough Up-Kicker", 2: "Auto Launch", 3: "Couch Release", 4: "Drops Reset Up",
	5: "Itchy & Scratchy Eject (VUK)", 6: "Upper Left VUK", 7: "TV Release", 8: "Homer Head",
	9: "Left Bumper", 10: "Right Bumper", 11: "Bottom Bumper",
	12: "UPF Left Flipper", 13: "UPF Right Flipper", 14: "Top Right Flipper",
	17: "Left Slingshot", 18: "Right Slingshot", 19: "Upper Right Eject", 20: "Garage Door (Eject)",
	21: "Flash: Pops Clear", 22: "Flash: R.Ramp Red", 23: "Flash: R.Ramp Orange",
	24: "Optional Coil", 25: "Flash: Itchy", 26: "Flash: Scratchy", 27: "Flash: Homer Head",
	28: "Flash: Couch", 29: "Flash: Comic Book Guy", 30: "Drop Bank Trips",
	31: "Flash: UPF Orange", 32: "Flash: UPF Red",
}
FLASHER_SOLENOIDS = {21, 22, 23, 25, 26, 27, 28, 29, 31, 32}
AUX_SOLENOID_LABELS = {33: "Left Up/Down Post", 34: "Center Up/Down Post", 35: "Right Up/Down Post"}
NOT_FITTED_SOLENOID_LABELS = {
	15: "Fast-Flip Game-On State", 16: "Not Used Raw Solenoid Position 16",
	36: "Unused Auxiliary Board Output 36",
	37: "Reserved Compatibility Hole 37", 38: "Reserved Compatibility Hole 38",
	39: "Reserved Compatibility Hole 39", 40: "Reserved Compatibility Hole 40",
	41: "Reserved Compatibility Hole 41", 42: "Reserved Compatibility Hole 42",
	43: "Reserved Compatibility Hole 43", 44: "Reserved Compatibility Hole 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC-Family Output 50",
}
FLIPPER_SOLENOID_LABELS = {
	45: "Right Flipper Power", 46: "Right Flipper Hold", 47: "Left Flipper Power", 48: "Left Flipper Hold",
}

# address -> {control_connection, power_connection, power_wire, driver_transistor, part_number, printed_type}
SOLENOID_WIRING = {
	1: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q1", control_wire="BRN-BLK", control_connection="J8-P1", part_number="26-1200/090-5044-00T"),
	2: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q2", control_wire="BRN-RED", control_connection="J8-P3", part_number="26-1200/090-5044-00T"),
	3: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q3", control_wire="BRN-ORG", control_connection="J8-P4", part_number="28-1050/090-5046-00"),
	4: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q4", control_wire="BRN-YEL", control_connection="J8-P5", part_number="26-1200/090-5044-00T"),
	5: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q5", control_wire="BRN-GRN", control_connection="J8-P6", part_number="27-1500/090-5004-00T"),
	6: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q6", control_wire="BRN-BLU", control_connection="J8-P7", part_number="26-1200/090-5044-00B"),
	7: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q7", control_wire="BRN-VIO", control_connection="J8-P8", part_number="28-1050/090-5046-00"),
	8: dict(power_wire="GRY~3A Fuse~BRN", power_connection="J7-P1", driver_transistor="Q8", control_wire="BRN-GRY", control_connection="J8-P9", part_number="22-900/090-5020-20T"),
	9: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q9", control_wire="BLU-BRN", control_connection="J9-P1", part_number="26-1200/090-5044-00T"),
	10: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q10", control_wire="BLU-RED", control_connection="J9-P2", part_number="26-1200/090-5044-00T"),
	11: dict(power_wire="YEL-VIO", power_connection="J10-P4/5", driver_transistor="Q11", control_wire="BLU-ORG", control_connection="J9-P4", part_number="26-1200/090-5044-00T"),
	12: dict(power_wire="GRY~3A Fuse~RED-YEL", power_connection="J10-P1/2", driver_transistor="Q12", control_wire="BLU-YEL", control_connection="J9-P5", part_number="25-1800/090-5041-00T"),
	13: dict(power_wire="BLU-YEL~3A Fuse~RED-YEL", power_connection="J10-P1/2", driver_transistor="Q13", control_wire="BLU-GRN", control_connection="J9-P6", part_number="24-1570/090-5025-00T"),
	14: dict(power_wire="BLU-YEL~3A Fuse~RED-YEL", power_connection="J10-P1/2", driver_transistor="Q14", control_wire="BLU-BLK", control_connection="J9-P7", part_number="23-1100/090-5030-00T"),
	15: dict(power_wire="GRY-YEL~3A Fuse~RED-YEL", power_connection="J10-P1/2", driver_transistor="Q15", control_wire="ORG-GRY", control_connection="J9-P8", part_number="22-1080/090-5032-00T"),
	16: dict(power_wire="BLU-YEL~3A Fuse~RED-YEL", power_connection="J10-P1/2", driver_transistor="Q16", control_wire="ORG-VIO", control_connection="J9-P9", part_number="22-1080/090-5032-00T"),
	17: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q17", control_wire="VIO-BRN", control_connection="J7-P2", part_number="23-800/090-5001-00T"),
	18: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q18", control_wire="VIO-RED", control_connection="J7-P3", part_number="23-800/090-5001-00T"),
	19: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q19", control_wire="VIO-ORG", control_connection="J7-P4", part_number="26-1200/090-5044-00T"),
	20: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q20", control_wire="VIO-YEL", control_connection="J7-P6", part_number="26-1200/090-5044-00T"),
	21: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q21", control_wire="VIO-GRN", control_connection="J7-P7", part_number="#906 Bulb 165-5004-00"),
	22: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q22", control_wire="VIO-BLU", control_connection="J7-P8", part_number="#906 Bulb 165-5004-00"),
	23: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q23", control_wire="VIO-BLK", control_connection="J7-P9", part_number="#906 Bulb 165-5004-00"),
	24: dict(power_wire="RED", power_connection="J16-P7", driver_transistor="Q24", control_wire="VIO-GRY", control_connection="J7-P10", part_number="Opt. 5v"),
	25: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q25", control_wire="BLK-BRN", control_connection="J6-P1", part_number="#906 Bulb 165-5004-00"),
	26: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q26", control_wire="BLK-RED", control_connection="J6-P2", part_number="#906 Bulb 165-5004-00"),
	27: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q27", control_wire="BLK-ORG", control_connection="J6-P3", part_number="#906 Bulb 165-5004-00"),
	28: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q28", control_wire="BLK-YEL", control_connection="J6-P4", part_number="#906 Bulb 165-5004-00"),
	29: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q29", control_wire="BLK-GRN", control_connection="J6-P5", part_number="#906 Bulb 165-5004-00"),
	30: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q30", control_wire="BLK-BLU", control_connection="J6-P6", part_number="32-1250/515-6916-01"),
	31: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q31", control_wire="BLK-VIO", control_connection="J6-P7", part_number="#906 Bulb 165-5004-00"),
	32: dict(power_wire="ORG", power_connection="J6-P10", driver_transistor="Q32", control_wire="BLK-GRY", control_connection="J6-P8", part_number="#906 Bulb 165-5004-00"),
}
AUX_SOLENOID_WIRING = {
	33: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q1", control_wire="WHT", control_connection="CN2-P5", part_number="26-1200/090-5044-00T"),
	34: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q2", control_wire="RED", control_connection="CN2-P4", part_number="23-1100/090-5030-00T"),
	35: dict(power_wire="BRN", power_connection="J7-P1", driver_transistor="Q3", control_wire="ORG", control_connection="CN2-P3", part_number="26-1200/090-5044-00T"),
}
# Retained-script solenoid callback names, for provenance notes.
SOLENOID_CALLBACKS = {
	1: "SolRelease (bsTrough.ExitSol_On, vpmTimer.PulseSw 15)", 2: "Auto_Plunger (plungerIM.AutoFire)",
	3: "CouchExit", 4: "dtDrop.SolDropUp", 5: "bsBR.SolOut", 6: "bsVUK.SolOut", 7: "SolTVRelease",
	8: "SolHomer", 12: "SolUPFLeftFlipper", 13: "SolUPFRightFlipper", 14: "SolTopRightFlipper",
	19: "bsTR.SolOut", 20: "GarageUp", 30: "SolDropBankTrips",
	21: 'SetLamp 121,', 22: 'SetLamp 122,', 23: 'SetLamp 123,', 25: 'SetLamp 125,',
	26: 'SetLamp 126,', 27: 'SetLamp 127,', 28: 'SetLamp 128,', 29: 'SetLamp 129,',
	31: 'SetLamp 131,', 32: 'SetLamp 132,',
	45: "SolRFlipper (canonical callback sLRFlipper)", 47: "SolLFlipper (canonical callback sLLFlipper)",
}

# --- Printed Lamp Matrix Grid (manual PDF page 36, printed 22). First digit is the column.
LAMP_LABELS = {
	1: "Left Out Extra Ball", 2: "Left Return Extra Ball", 3: "Shoot Again",
	4: "Right Return Extra Ball", 5: "Special", 6: "Shooter Lane Skill Shot",
	7: "Light Otto", 8: "Adv. Pops",
	9: "Spay Anything", 10: "Kitty Kitty Bang Bang", 11: "Field Of Screams",
	12: "Esophagus Now", 13: "I&S Arrow", 14: "Start I&S Multiball", 15: "I&S 2X Scoring",
	16: "Pops 2X Scoring",
	17: "Left Pop Bumper", 18: "Right Pop Bumper", 19: "Bottom Pop Bumper", 20: "More Time",
	21: "Collect Nuclear Plant", 22: "Left Orbit Arrow", 23: "Cletus 2X Scoring",
	24: "Left Orbit Hurry Up",
	25: "CBG Skill Shot", 26: "CBG Start Hurry Up", 27: "Daredevil Ramps",
	28: "Daredevil Bumpers", 29: "Daredevil Loops", 30: "Daredevil Targets",
	31: "Start Button", 32: "Tournament Button",
	33: "Left Ramp Arrow", 34: "Treehouse Of Horror", 35: "Treehouse 2X Scoring",
	36: "Left Ramp Hurry Up", 37: "Right Ramp Arrow", 38: "Get Duffed!",
	39: "Moe's 2X Scoring", 40: "Right Ramp Hurry Up",
	41: "Mini Loop Arrow", 42: "2X Scoring Kwik-E-Mart", 43: "Kwik-E-Mart Hurry Up",
	44: "Garage Arrow", 45: "Clean The Garage", 46: "Garage 2X Scoring",
	47: "Garage Hurry Up", 48: "Right Orbit Arrow",
	49: "Right Loop Arrow", 50: "Otto's Bus Tours", 51: "Elementary 2X Scoring",
	52: "Bully 3-Bank (Top)", 53: "Bully 3-Bank (Mid)", 54: "Bully 3-Bank (Bot)",
	55: "Krusty 2X Scoring", 56: "Right Orbit Hurry Up",
	57: "Homer", 58: "Marge", 59: "Bart", 60: "Lisa", 61: "Maggie", 62: "Grandpa",
	63: "Left Headlight", 64: "Right Headlight",
	65: "Living Room 2X Scoring", 66: "(Light) Lock", 67: "Light (Lock)", 68: "Lock (Square)",
	69: "Super Jackpot", 70: "TV Arrow",
	73: "(LED) Duffman", 74: "(LED) Homer's Day", 75: "(LED) Willie's Woes",
	76: "(LED) Wiggum Vs Snake", 77: "(LED) Bart's Day", 78: "(LED) Krusty's Last Stand",
	79: "(LED) Stop The Monorail", 80: "(LED) Alien Invasion",
}
LAMP_BULBS: dict[int, str] = {}
for _addr in range(1, 71):
	if _addr in (32, 71, 72):
		continue
	LAMP_BULBS[_addr] = "#44" if _addr in (16, 63, 64) else "#555"
for _addr in range(73, 80):
	LAMP_BULBS[_addr] = "Green LED"
LAMP_BULBS[80] = "Red LED"
del _addr
LAMP_QUANTITIES = {16: 2, 80: 2}
UNUSED_LAMP_ADDRESSES = {71, 72}
DOTS_LAMP_ADDRESSES = {17, 18, 19, 31, 65, 66, 67, 68, 69}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J13-P9", "U17"), 2: ("Yellow-Red", "J13-P8", "U16"),
	3: ("Yellow-Orange", "J13-P7", "U15"), 4: ("Yellow-Black", "J13-P6", "U14"),
	5: ("Yellow-Green", "J13-P5", "U13"), 6: ("Yellow-Blue", "J13-P4", "U12"),
	7: ("Yellow-Violet", "J13-P3", "U11"), 8: ("Yellow-Gray", "J13-P1", "U10"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J12-P1", "Q33"), 2: ("Red-Black", "J12-P2", "Q34"),
	3: ("Red-Orange", "J12-P3", "Q35"), 4: ("Red-Yellow", "J12-P4", "Q36"),
	5: ("Red-Green", "J12-P5", "Q37"), 6: ("Red-Blue", "J12-P6", "Q38"),
	7: ("Red-Violet", "J12-P8", "Q39"), 8: ("Red-Gray", "J12-P9", "Q40"),
	9: ("Red-White", "J12-P10", "Q41"), 10: ("Red", "J12-P11", "Q42"),
}

GI_POSITIONS: list[tuple[float, float]] = [
	(0.763655, 0.793243), (0.173319, 0.805537), (0.948996, 0.626498), (0.150438, 0.072166),
	(0.142323, 0.089766), (0.144374, 0.186887), (0.796739, 0.154132), (0.67629, 0.153711),
	(0.689362, 0.216333), (0.942694, 0.322637), (0.025794, 0.503356), (0.302249, 0.179042),
	(0.880228, 0.007174), (0.925668, 0.022304), (0.508909, 0.10171), (0.105859, 0.26758),
	(0.222572, 0.228494), (0.682593, 0.24155), (0.019024, 0.347433), (0.933123, 0.373911),
	(0.02556, 0.366766), (0.91725, 0.413417), (0.037698, 0.620194), (0.186158, 0.716438),
	(0.71557, 0.715597), (0.211368, 0.756364), (0.685691, 0.757205), (0.807263, 0.767829),
	(0.926939, 0.314358), (0.314896, 0.242022), (0.234473, 0.250159), (0.220408, 0.760034),
	(0.688507, 0.761434), (0.177458, 0.809907), (0.768805, 0.79814), (0.923801, 0.027768),
	(0.878361, 0.012638), (0.680726, 0.237347), (0.687495, 0.21213), (0.674423, 0.149509),
	(0.794871, 0.149929), (0.906449, 0.567225),
]


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Simpsons Pinball Party retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Simpsons Pinball Party extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Simpsons Pinball Party retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Simpsons Pinball Party retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Simpsons Pinball Party retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the simpprty clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/segames.c simpprtyGameData = { GEN_WS, dispSPP, {FLIP_SW(FLIP_L) | "
				"FLIP_SOL(FLIP_L), 0, 4, 0, 0, SE_BOARDID_520_5068_01 | SE_BOARDID_520_5219_00 }} "
				"(positional aggregate init leaves wpc.invSw all-zero, confirmed by no invSw "
				"assignment anywhere in the file); src/wpc/se.c SWITCH_UPDATE(se), dedswitch_r "
				"(DED #1-#8 bit layout and the D4/public-88 dead upper-flipper bit), se_solenoid_w "
				"(the /* move flipper power solenoids (L=15,R=16) to (R=45,L=47) */ remap), "
				"gilamp_w/gilamp_r (auxiliary lamp columns 10-11, driver's own \"GI lamps on "
				"Simpsons?\" comment), coreGlobals.nGI = 1; src/wpc/se.h SE_SWBLACK/SE_SWGREEN/"
				"SE_SWRED/SE_SWMEMORYPROTECT, SE_BOARDID_520_5068_01/520_5219_00; src/wpc/core.c "
				"core_updateSw locals.flipMask construction (unconditional lower-flipper button "
				"bits, conditional EOS/upper bits gated on hw.flippers), core.c:2455 invSw memcpy; "
				"src/wpc/core.h CORE_SWLRFLIPEOSBIT..CORE_SWULFLIPBUTBIT, CORE_FLIPPERSWCOL=11, "
				"FLIP_L/FLIP_SW/FLIP_SOL/FLIP_EOS macros; src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_WS=0x0004000000000"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": PINNED_CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINNED_REVISION,
			"locator": (
				"Operational pinned baseline, read for the 2026-09-25 polarity, flipper-input and lamp-range pass: "
				"src/wpc/se.c:635 switch_r returns ~core_getSwCol(selocals.swCol), so public 1 is the CPU's "
				"closed-contact reading; se.c:648-656 dedswitch_r builds D0-D4 from the flipper column "
				"(core_revnyb(fls & 0x0f) | ((fls & 0x80)>>3)), so public 88 (column 11 bit 0x80) is DED #5; "
				"src/wpc/core.c:1776-1777 core_updateSw rewrites only the flipper-column bits in locals.flipMask "
				"and preserves the rest, and core.c:2508-2517 builds flipMask from hw.flippers, which for "
				"simpprtyGameData (segames.c:1211-1212, FLIP_SW(FLIP_L) | FLIP_SOL(FLIP_L), lampCol 4) omits "
				"the upper-flipper bits, so PinMAME never synthesizes public 88 but a host write to it persists "
				"(core.c:2136 core_setSw); se.c:183-192 sets public 15 from RAM byte fastflipaddr-1 as the "
				"fast-flip state, and se.c:355/375-376 assigns fastflipaddr 0x04+1 only when the running "
				"driver's own name matches \"simpprty\" in its first eight characters, so the seventeen clones "
				"leave it unset and publish 15 as constant zero; se.c:425 nLamps = 64 + lampCol*8 and "
				"src/wpc/vpintf.c:65-110 vp_getChangedLamps scans CORE_STDLAMPCOLS + lampCol = 12 columns, so "
				"public lamps run 1-96; se.c:628-632 gilamp_w/gilamp_r and the memory map at se.c:1099/1118 "
				"(\"GI lamps on Simpsons?\") are the only writers of lampMatrix columns 10-11 (public 81-96), "
				"and no PWM output is written for them on this driver."
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": VPM_CORE_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/vpm-script-libs/core.vbs",
			"original_filename": "core.vbs",
			"sha256": VPM_CORE_SHA256,
			"locator": (
				"Visual PinMAME script library core.vbs (Const VPinMAMEDriverVer = 3.61), copied from the "
				"contributor's installed VPX Scripts folder. Class cvpmBallStack: SetSw (line 901) writes "
				"Controller.Switch(mSw(aNo)) = aStatus; Reset (lines 915-917) asserts True for every occupied "
				"ball position; InitSw (line 1038) stores aSw1 as position 1; KickOut (line 1001) clears "
				"position 1 with SetSw 1, False when the exit ball leaves. The retained table does not pin "
				"which core.vbs it ran against, so this is the library revision installed beside it."
			),
			"license": "NOASSERTION",
			"attribution": "Visual PinMAME contributors",
			"rights": "NOASSERTION",
		},
		{
			"id": RUNTIME_STACKING,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_STACKING_PATH}",
			"revision": PINNED_REVISION,
			"locator": (
				"Two hash-pinned LibPinMAME harness runs of simpprty from empty NVRAM with five balls resting on "
				"trough switches 10-14 (scenarios tools/harness-scenarios/whitestar/simpprty-stacking-opto.json "
				"and simpprty-stacking-opto-boot-active.json). With the 5-Ball Stacking Opto 15 held at public 1 "
				"from power-up, or raised to 1 in attract mode, the ROM fires the trough up-kicker (public 1) six "
				"times and the auto launch (public 2) once; with 15 at 0 at boot, or lowered back to 0, no coil "
				"fires. No lamp above 80 changes in either run."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": RUNTIME_FLIPPERS,
			"kind": "runtime_scenario",
			"uri": f"internal:{RUNTIME_FLIPPERS_PATH}",
			"revision": PINNED_REVISION,
			"locator": (
				"One hash-pinned LibPinMAME harness run of simpprty from empty NVRAM (scenario "
				"tools/harness-scenarios/whitestar/simpprty-flipper-buttons.json) with keyboard handling off: four "
				"coins on public 6 (the ROM pulses solenoid 24 once per coin), Start on 54, one ball moved from 14 "
				"to the shooter lane 16, then each flipper input held alone for 2 s. Public 82 (DS-3) energises "
				"45/46 only; public 88 (DS-5) energises solenoids 13 and 14 only; 82 and 88 together energise "
				"13, 14, 45 and 46; public 84 (DS-1) energises 47/48 and solenoid 12. Public 15 rises to 1 when "
				"the game starts and stays there. No lamp above 80 changes."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
		{
			"id": "ipdb.the-simpsons-pinball-party.4674",
			"kind": "human_review",
			"uri": "https://www.ipdb.org/machine.cgi?id=4674",
			"revision": "repository",
			"locator": (
				"Physical identity, manufacturer, and release year for IPDB 4674, The Simpsons "
				"Pinball Party (Stern, 2003). The legacy migration's games/simp.json record carries "
				"the correct ipdb_id 4674 itself, but an earlier pass in this repository's history "
				"mis-linked a different source entry to https://www.ipdb.org/machine.cgi?id=6154 -- "
				"IPDB 6154 link belongs to Iron Man Vault Edition (stern.iron-man-vault-edition.2014), "
				"a completely unrelated physical machine. This record cites 4674 directly and "
				"exclusively."
			),
			"license": "NOASSERTION",
			"attribution": "Internet Pinball Database",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/whitestar.json",
			"revision": "repository",
			"locator": "Whitestar public switch, DIP, solenoid, lamp, and single-channel GI address rules, confirmed unchanged against pinned source for this driver",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/stern.the-simpsons-pinball-party.2003/archive-Stern_Pinball_The_Simpsons_Pinball_Party_Manual/The_Simpsons_Manual.pdf",
			"original_filename": "The_Simpsons_Manual.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"216-page Stern Pinball operations manual (Internet Archive item "
				"Stern_Pinball_The_Simpsons_Pinball_Party_Manual). PDF page 30 (printed page 16) "
				"carries the SWITCH MATRIX GRID & DEDICATED SWITCHES data table; PDF page 31 "
				"(printed 17) carries the switch-locations diagram, mounting-location legend, and "
				"the Sw.14/15/56 footnotes; PDF pages 32/34 (printed 18/20) carry the Coils "
				"Detailed Chart Table; PDF page 33 (printed 19) carries the coil/flash-lamp "
				"mounting-location legend and the Optional-Coil/AUX-UK-Only footnotes; PDF page 36 "
				"(printed 22) carries the Lamp Matrix Grid; PDF page 37 (printed 23) carries the "
				"lamp-locations legend and the Lamp 31/32 footnotes; PDF pages 82, 114 and 170 (printed 64, 96 "
				"and 141) identify the LED Mode Signifier board 520-5225-00 on the back panel next to the TV, and "
				"PDF page 42 (printed 28) ties its LEDs to lamps 73-80; PDF page 121 (Section 5 "
				"Chapter 2, printed 103) carries the General Illumination Circuit Detailed Wiring "
				"Diagram. The text layer double-doubles most characters and, on the diagnostics "
				"chapter specifically, shifts character codes by a constant +29 with no ToUnicode "
				"correction on some pages; every table cited here was read from a rendered page, "
				"never from pdftotext output."
			),
			"license": "NOASSERTION",
			"attribution": "Stern Pinball, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.simpsons-party.switch-matrix-dedicated-switches",
					"locator": "PDF page 30, printed page 16, SWITCH MATRIX GRID & DEDICATED SWITCHES",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/switch-matrix-dedicated-switches.md",
					"sha256": "615ff2dc023f468a68b5325fdc2479a469a7cd7e596f93af717b22bf35e66a2f",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/switch-matrix-dedicated-switches.webp",
					"image_sha256": "e38f07025824a5a489333a3005825c1fc4b4e65eaeac2d92f5c47d6cc71209da",
					"image_derivation": "The_Simpsons_Manual.pdf page 30, crop box 0.08,0.51,0.92,0.84, born-digital page rendered for legibility (smallest type in region 5.0pt, targeting 11px glyphs), rendered at 126 dpi, capped to 900px wide, grayscale, 901x458 WebP quality 50",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.switch-locations-footnotes",
					"locator": "PDF page 31, printed page 17, switch-locations diagrams, schematics, and footnotes",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/switch-locations-footnotes.md",
					"sha256": "aa587c89f8c34dd3a9375be6c876a41d3c4b9dbf9a38740193d2cc3d802aed76",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/switch-locations-footnotes.webp",
					"image_sha256": "633ec410f5b85f8fdb52ee5dfef38b64f06337fa76f803e2a7da40832218bf50",
					"image_derivation": "The_Simpsons_Manual.pdf page 31, crop box 0.03,0.04,0.97,0.8, born-digital page rendered for legibility (smallest type in region 7.0pt, targeting 11px glyphs), rendered at 114 dpi, grayscale, 910x952 WebP quality 55",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.coils-detailed-chart",
					"locator": "PDF page 34 (printed 20, full chart) cross-checked against PDF page 32 (printed 18, preview), COILS DETAILED CHART TABLE",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/coils-detailed-chart.md",
					"sha256": "8276c4feecb1e8306b53595c4020efebe06f4b5a7c1bebcdb3a1fc93322f7ca0",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/coils-detailed-chart.webp",
					"image_sha256": "142771f3dc6419b4795fbc2c1f6e939975c9d35c80a91bd5faf53b94bf56145b",
					"image_derivation": "The_Simpsons_Manual.pdf page 34, crop box 0.08,0.1,0.92,0.86, born-digital page rendered for legibility (smallest type in region 6.0pt, targeting 11px glyphs), rendered at 98 dpi, capped to 700px wide, grayscale, 701x821 WebP quality 30",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.coil-flash-lamp-locations",
					"locator": "PDF page 33, printed page 19, COIL & FLASH LAMP LOCATIONS legend and footnotes",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/coil-flash-lamp-locations.md",
					"sha256": "8abc7a63e7b784fb6092095c8cb4bd7fa8dc60dd56cdfd2ca9ffff0bf89b3986",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/coil-flash-lamp-locations.webp",
					"image_sha256": "3f5341bbcc731cb8e5399e5f847ae1db4f9cee9282f119a13e29cfdd4836df6f",
					"image_derivation": "The_Simpsons_Manual.pdf page 33, crop box 0.06,0.06,0.94,0.78, born-digital page rendered for legibility (smallest type in region 6.0pt, targeting 11px glyphs), rendered at 120 dpi, capped to 900px wide, grayscale, 901x954 WebP quality 45",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.lamp-matrix-grid",
					"locator": "PDF page 36 (printed 22, LAMP MATRIX GRID) and PDF page 37 (printed 23, locations legend and footnotes)",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/lamp-matrix-grid.md",
					"sha256": "8a09f1da691c466715862d210cad89298ee8f489bc0ee726f177129b04b6507c",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/lamp-matrix-grid.webp",
					"image_sha256": "34ee9bcbe750f818337fbb91e7ac1484214c590b08c4efe73d9243ccc874b403",
					"image_derivation": "The_Simpsons_Manual.pdf page 37, crop box 0.03,0.04,0.97,0.82, born-digital page rendered for legibility (smallest type in region 6.0pt, targeting 11px glyphs), rendered at 132 dpi, capped to 1000px wide, colour, 1001x1074 WebP quality 50",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.led-mode-sign",
					"locator": "PDF page 114 (printed Section 4 Chapter 2 page 96, TV and LED Mode Signifier parts and drawing), cross-checked against PDF page 82 (printed 64, items 19/20/D), PDF page 170 (printed Section 5 Chapter 4 page 141, LED PC Board component layout) and PDF page 42 (printed 28, LED test note)",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/led-mode-sign.md",
					"sha256": "da0a18d5d3ae786207a34b7a0a883f729609b8788592be4e60f4e854e33d0d23",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/led-mode-sign.webp",
					"image_sha256": "65d92ab65fdc43fa00b2fb7d3043ad0931ad8239e1b64a87567638bf5b712183",
					"image_derivation": "The_Simpsons_Manual.pdf page 114, crop box 0.05,0.03,0.92,0.5, born-digital page rendered for legibility (smallest type in region 6.0pt, targeting 11px glyphs), rendered at 132 dpi, grayscale, 977x683 WebP quality 70",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered pages",
					"reviewed": True,
				},
				{
					"id": "excerpt.simpsons-party.general-illumination",
					"locator": "PDF page 121, Section 5 Chapter 2, printed page 103, General Illumination Circuit Detailed Wiring Diagram",
					"path": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/general-illumination.md",
					"sha256": "cb3ad1b12ae358b31dd45ccb87bd1fbcc7778ee8210d78b28e9834638865b29a",
					"image": "evidence/excerpts/stern.the-simpsons-pinball-party.2003/general-illumination.webp",
					"image_sha256": "2274c15a61f607eb3cb1286aa108a6700e1dd2c3407f80e1fe2c54ec4d528baf",
					"image_derivation": "The_Simpsons_Manual.pdf page 121, crop box 0.06,0.03,0.98,0.97 of the page, rendered at 150 dpi with pdftoppm, reduced to 750px wide grayscale, quality 60 WebP",
					"method": "mixed",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table and diagram used by "
				"this definition, together with the rendered PNG page cache under "
				"external:pinmame-manuals/rendered/stern.the-simpsons-pinball-party.2003/ and the "
				"pinned-source/retained-script cross-reference notes. The retained PDF's text layer "
				"is unreliable (see the manual source locator), so this transcription is the source "
				"of record and the OCR text is never an authority."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/source/The%20Simpsons%20Pinball%20Party%20v0.8.2.vpx",
			"original_filename": "The Simpsons Pinball Party v0.8.2.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working, non-VPW, pre-1.0 community recreation of the physical "
				f"machine, VPX table version 10.x. Exact playfield bounds are {TABLE_BOUNDS}; "
				"normalized coordinates are x/952 and y/2115. This is a thin table: its 40,788-byte "
				"script is a fifth the size of the VPW-authored scripts used earlier in this "
				"project, so it is geometry authority for named table objects only, judged honestly "
				"rather than assumed complete. Lamps 73-80 are eight Primitive objects l73-l80 "
				"(mesh MoesSignLight, image moesred_off/on) at one playfield point (x 548.6, y 72.9) "
				"stacked in height from z 305 (l73) down to z 165 (l80); they are the LED mode sign "
				"on the back panel. Two further local tables of the same lineage (Coindropper/"
				"32assassin script base) place l73-l80 at identical coordinates, so they corroborate "
				"nothing independently."
			),
			"license": "NOASSERTION",
			"attribution": "unattributed community table author",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded script (40,788 bytes). Runtime and mechanism-causality '
				'authority: Const cGameName = "simpprty", UseSolenoids=1, UseLamps=0, UseGI=0, '
				"UseSync=1, HandleMech=1; the SolCallback table for solenoids 1-8, 12-14, 17-23, "
				"25-32 plus core.vbs sLRFlipper/sLLFlipper for 45-48; the Controller.Switch and "
				"vpmTimer.PulseSw switch semantics for every matrix switch with a named sw-object; "
				"bsTrough/bsBR/bsTR/bsVuk cvpmBallStack initialization for the trough and three "
				"saucers/VUKs; dtDrop cvpmDropTarget for the three-target bank; the SolRFlipper "
				"triple-object rotate (RightFlipper, RightFlipper2, TopRightFlipper) alongside "
				"solenoid 13's and 14's own SolUPFRightFlipper/SolTopRightFlipper callbacks; "
				"SolRelease's vpmTimer.PulseSw 15 on every up-kicker pulse; UpdateLamps's NFadeObj "
				"73-80 onto the l73-l80 mode-sign primitives; and the UpdateLeds LampCallback, which "
				"reads Controller.ChangedLEDs for the TV's 14x10 mini-DMD into the r*/g*/y* light "
				"arrays REDL/GREENL/YELLOWL (the LEDY/LEDG/LEDR collections it hides at start-up are "
				"empty and carry no lamp)."
			),
			"license": "NOASSERTION",
			"attribution": "unattributed community table author",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size, and "
				f"SHA-256 under extracted-vpxtool; manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; "
				f"{EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with "
				f"vpxtool from the retained table. Bounds are {TABLE_BOUNDS}."
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
	column, row = divmod(address - 1, 8)
	column += 1
	row += 1
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_component = SWITCH_ROW_WIRING[row]
	return {
		"board": "Whitestar CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column drive {drive_component}; row return {return_component}",
	}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	# Matrix switches 1-64. Whitestar publishes sequential addresses ordered by column then
	# row (se_m2sw(col, row) = col*8+(7-row)+1 in the driver's own 0-indexed terms), which
	# in 1-indexed printed-manual terms is address = (column-1)*8 + row -- confirmed against
	# every transcribed cell in the manual's own SWITCH MATRIX GRID table.
	for column in range(1, 9):
		for row in range(1, 9):
			address = (column - 1) * 8 + row
			identifier = f"switch.matrix-{address}"
			unused = address in UNUSED_MATRIX_ADDRESSES
			cabinet_label = CABINET_MATRIX_LABELS.get(address)
			label = cabinet_label or SWITCH_LABELS.get(address)
			part_number = SWITCH_PARTS.get(address)
			physical: dict[str, Any] = {}
			if part_number:
				physical["part_number"] = part_number
			switch_type = CABINET_SWITCH_TYPES.get(address) or SWITCH_TYPES.get(address)
			if switch_type:
				physical["switch_type"] = switch_type
			notes = f"Printed switch-matrix drive column {column}, return row {row}."
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"wiring": _switch_wiring(address),
			}
			if unused:
				notes += " Shaded gray \"NOT USED\" on the printed matrix (PDF 30, printed 16)."
				physical["notes"] = notes
				extra["physical"] = physical
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(_device(identifier, f"Not Used Matrix Position {address}", "switch", "pinmame.input.switch", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			if address in FUTURE_USE_MATRIX_ADDRESSES:
				notes += ' Printed switch part number is "Future Use" -- the matrix position and coin-door harness are wired, but no coin-slot hardware is fitted by default.'
			if address in DOTS_MATRIX_ADDRESSES:
				notes += ' Also marked "Diode On Terminal Strip" (DOTS) on the printed matrix.'
			if address in OPTO_SWITCHES:
				notes += (
					' Identified as opto construction by the manual\'s inline "Sw. 14 & 15 Part '
					'Note" (Transmitter & Receiver OPTO PC Boards, parts 515-0173-00/515-0174-00), '
					"which names the board pair and says nothing about the contact's rest state; "
					"this manual's switch-matrix page carries no shaded-cell opto legend at all, and "
					'its switch-location drawing stamps the pair as one "14:15" location at the '
					"trough's right-hand exit end. Pinned PinMAME applies no inversion for this "
					"driver -- simpprtyGameData's positional aggregate initializer (segames.c:1211) "
					"leaves the wpc member, and with it wpc.invSw, zero-initialized, and core.c "
					"copies those zeros into the live mask -- and se.c's switch_r returns "
					"~core_getSwCol, so public 1 is what the CPU reads as a closed matrix contact. "
				)
				if address == 14:
					notes += (
						"The retained known-working script settles this address by observation: "
						+ SCRIPT_EVIDENCED_OPTOS[14]
						+ ". That makes the opto board's matrix-facing contact rest open and close "
						"while a ball blocks the beam; nothing in the firmware compensates for a "
						"closed rest state. A recreation holds 14 at 1 while a ball waits at the "
						"up-kicker, at 0 otherwise, and never inverts it."
					)
				else:
					notes += (
						"Its sense was asked of the ROM directly. Hash-pinned LibPinMAME runs of "
						"simpprty with five balls held on 10-14 show that the ROM acts on public 1 "
						"and is quiet at 0: held at 1 from power-up, or raised to 1 in attract mode, "
						"it fires the trough up-kicker (public 1), and because the harness never "
						"lets a ball move it fires it six times and then fires the auto launch "
						"(public 2) once; 0 at boot and a fall back to 0 draw no coil. The retained "
						"known-working script agrees: "
						+ SCRIPT_EVIDENCED_OPTOS[15]
						+ ", and it leaves 15 at 0 otherwise. That 1 means a ball blocking the "
						"stacking beam is an inference, corroborated by switch 14 on the same "
						"515-0173-00/515-0174-00 board pair. The opto board's matrix-facing contact "
						"therefore rests open and closes while a ball blocks the beam. A recreation "
						"holds 15 at 0 at rest, drives it to 1 only while a ball blocks the stacking "
						"beam, and never inverts it."
					)
			if address in CABINET_MATRIX_LABELS:
				role_map = {
					1: "cabinet.left-button-uk", 8: "cabinet.right-button-uk",
					2: "cabinet.coin.4", 4: "cabinet.coin.right", 5: "cabinet.coin.center",
					6: "cabinet.coin.left", 3: "cabinet.coin.6th-reserved", 7: "cabinet.coin.5th-reserved",
					53: "cabinet.tournament-button", 54: "cabinet.start", 56: "cabinet.tilt",
				}
				extra["roles"] = [role_map[address]]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				if address == 56:
					notes += (
						' Switch 56 Part Note: "The Switch is comprised of a Hanger Bracket '
						'(535-5319-00) and Contact Wire (535-7563-01) located in the Cabinet" -- a '
						"plumb-bob tilt pendulum, not opto construction."
					)
				availability = "used"
				if address in OPTIONAL_MATRIX_ADDRESSES:
					availability = "optional"
					if address in (1, 8):
						notes += " Printed \"(UK ONLY)\" -- a regional cabinet button not fitted on the base configuration."
					else:
						notes += " In Cabinet; requires the Optional Tournament Kit (matches lamp 32's identical footnote)."
				physical["location"] = "cabinet" if address not in (2, 4, 5, 6, 3, 7) else "coin door"
				physical["notes"] = notes
				extra["physical"] = physical
				refs = (MANUAL_SOURCE, CORE_SOURCE)
				items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))
				continue
			physical["notes"] = notes
			extra["physical"] = physical
			# The opto boards' matrix-facing contact rests open (see the opto note above), so no
			# matrix switch on this machine is normally closed.
			extra["normally_closed"] = False
			if address in PULSED_SWITCHES:
				extra["pulse"] = True
			if address in SWITCH_PROJECTIONS:
				coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE)
			else:
				coordinate_refs = (VPX_TABLE_SOURCE,)
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], *coordinate_refs)
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			if address in OPTO_SWITCHES:
				refs += (PINNED_CORE_SOURCE,)
				refs += (VPM_CORE_SOURCE,) if address == 14 else (RUNTIME_STACKING,)
			items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, "used", refs, **extra))

	# Dedicated switches DS-1..DS-8.
	for address, (label, ds_number, role, part_number, switch_type) in DEDICATED_SWITCH_LABELS.items():
		wire, connection = DEDICATED_SWITCH_WIRING[address]
		physical = {
			"part_number": part_number,
			"switch_type": switch_type,
			"notes": f"Printed dedicated switch {ds_number}." + DEDICATED_SWITCH_NOTES.get(address, ""),
		}
		wiring = {"board": "Whitestar CPU board", "drive_wire": wire, "drive_connection": connection}
		if address == 88:
			refs = (MANUAL_SOURCE, PINNED_CORE_SOURCE, RUNTIME_FLIPPERS)
		elif address in (84, 82):
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, RUNTIME_FLIPPERS)
		elif address in (81, 83):
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE, PINNED_CORE_SOURCE, RUNTIME_FLIPPERS)
		else:
			refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
		items.append(
			_device(
				f"switch.dedicated-{ds_number.lower()}", label, "switch", "pinmame.input.switch", address, "used", refs,
				aliases=[
					{"namespace": "pinmame.switch", "value": str(address)},
					{"namespace": "manual.address", "value": ds_number},
				],
				roles=[role],
				wiring=wiring,
				physical=physical,
				normally_closed=False,
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	# Flipper-column bits 0x10-0x40 (public 85-87) exist in PinMAME's switch space but se.c's
	# dedswitch_r reads only bits 0x0f and 0x80, flipMask excludes them, and the manual prints no
	# dedicated input for them.
	for address in (85, 86, 87):
		items.append(
			_device(
				f"switch.flipper-column-{address}", f"Unused Flipper-Column Input {address}", "switch",
				"pinmame.input.switch", address, "unused", (PINNED_CORE_SOURCE, CONTROLLER_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}],
				physical={
					"notes": (
						f"Flipper-column bit 0x{1 << (address - 81):02x}. se.c's dedswitch_r builds the eight "
						"DED inputs from the service-button bits and flipper-column bits 0x0f and 0x80 only, "
						"simpprtyGameData's flipMask excludes this bit, and the manual's DS-1..DS-8 table has "
						"no input for it, so the ROM never reads this address."
					)
				},
				spatial=not_applicable("unused", PINNED_CORE_SOURCE),
			)
		)

	# Coin-door memory-protect interlock (SE_SWMEMORYPROTECT = -3), not one of DS-1..DS-8.
	items.append(
		_device(
			"switch.memory-protect",
			"Coin Door Memory Protect Interlock",
			"switch",
			"pinmame.input.switch",
			-3,
			"used",
			(MANUAL_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.switch", "value": "-3"}],
			roles=["cabinet.memory-protect"],
			normally_closed=False,
			physical={
				"switch_type": "other",
				"notes": (
					"The Dual Switch Bracket just inside the coin-door frame holds the Playfield "
					"Power Interlock switch and the Memory Protect switch (manual PDF page 23, "
					'"Important: The Dual Switch Bracket holds the Playfield Power Interlock & '
					'Memory Protect Switches"). se.h defines SE_SWMEMORYPROTECT = -3; se.c reads '
					"it directly with core_getSw(SE_SWMEMORYPROTECT) to gate battery-backed RAM "
					"writes while the coin door is open."
				),
			},
			spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
		)
	)

	# CPU-board country-configuration DIP bank (SW300).
	for address in range(1, 9):
		used = address <= 5
		items.append(
			_device(
				f"switch.dip-{address}",
				f"CPU DIP {address} (SW300 country selector)" if used else f"CPU DIP {address} (unused bit)",
				"dip_switch",
				"pinmame.input.dip",
				address,
				"used" if used else "unused",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}],
				physical={
					"location": "Whitestar CPU board SW300",
					"switch_type": "dip",
					"notes": (
						'se.h SE_COMPORTS declares "Dip SW300" as a 5-bit country selector '
						"(COREPORT_DIPNAME 0x001f); bits 6-8 are unused padding in the eight-address "
						"public DIP contract."
					),
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


def output_id(label: str) -> str:
	import re

	slug = re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed"
	return f"device.{slug}"


def _solenoid_wiring(address: int, table: dict[int, dict[str, str]]) -> dict[str, Any]:
	data = table[address]
	return {
		"board": "I/O Power Driver board" if table is SOLENOID_WIRING else "Solenoid Expander Auxiliary board",
		"driver_transistor": data["driver_transistor"],
		"power_wire": data["power_wire"],
		"power_connection": data["power_connection"],
		"control_wire": data["control_wire"],
		"control_connection": data["control_connection"],
	}


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			kind = "flasher" if address in FLASHER_SOLENOIDS else "motor" if address in (8, 20) else "coil"
			wiring_data = SOLENOID_WIRING[address]
			physical: dict[str, Any] = {"part_number": wiring_data["part_number"]}
			notes = f"Printed coils-detailed-chart entry #{address}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
			if address == 8:
				notes += (
					" Homer Head toy motor; the retained script's HomerOn_Timer/HomerOff_Timer "
					"animate the figure's rotation while HomerActive is set, gated by ball position "
					"relative to the Homer/Homer2/Homer3/homer4 internal VPX triggers (none of which "
					"assert a public switch)."
				)
			if address == 12:
				notes += (
					" Upper-mini-playfield left flipper. A plain numbered solenoid the ROM drives from "
					"the left cabinet button: with a game in progress, holding DS-1 (public 84) alone "
					"energises it together with the lower left flipper (47/48) in a hash-pinned harness "
					"run. PinMAME's own flipper subsystem does not know it (simpprtyGameData.hw.flippers "
					"declares FLIP_L only)."
				)
			if address == 13:
				notes += (
					" Upper-mini-playfield right flipper. The ROM drives it from DS-5 (public 88), the "
					"second contact of the doubled right cabinet button: holding 88 alone energises it "
					"together with solenoid 14, while holding DS-3 (public 82) alone does not "
					"(hash-pinned harness run)."
				)
			if address == 14:
				notes += (
					" Printed \"Top Right Flipper\", a third main-playfield flipper coil distinct "
					"from both the lower-right flipper (15/16, remapped to public 45-48) and the "
					"upper-mini-playfield pair (12/13). The ROM drives it from DS-5 (public 88), "
					"together with solenoid 13; DS-3 (public 82) alone leaves it off (hash-pinned "
					"harness run). The retained script's SolRFlipper (the lower-right flipper's "
					"callback on public 46) also rotates this coil's table object (RightFlipper2) and "
					"solenoid 13's (TopRightFlipper), a table-side workaround for a host that never "
					"writes public 88; a recreation should drive 88 with its right flipper button "
					"instead."
				)
			if address in FLASHER_SOLENOIDS:
				notes += " #906 wedge-base flashlamp (165-5004-00)."
			if address == 24:
				notes += (
					' Manual footnote: "Coil Q24 is Optional. If a Coin Meter, Token Dispenser or '
					'Knocker is required (both optional) call Technical Support..." -- enumerated but '
					"not part of the base fitment; which accessory (if any) is installed cannot be "
					"determined from this evidence. The ROM pulses this driver once per inserted coin "
					"in a hash-pinned harness run, so a coin meter wired here would count coins."
				)
			if address == 30:
				notes += " Trips (knocks down) the three-target drop bank; solenoid 4 resets it."
			physical["notes"] = notes
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.solenoid", "value": str(address)},
					{"namespace": "manual.address", "value": str(address)},
				],
				"physical": physical,
				"wiring": _solenoid_wiring(address, SOLENOID_WIRING),
			}
			availability = "optional" if address == 24 else "used"
			role = "emitter" if kind == "flasher" else "effect"
			if address == 24:
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			else:
				coordinate_refs = (VPX_TABLE_SOURCE, MANUAL_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], *coordinate_refs)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE) if address in SOLENOID_CALLBACKS else (MANUAL_SOURCE, CORE_SOURCE)
			if address in (12, 13, 14, 24):
				refs += (RUNTIME_FLIPPERS,)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		if address in AUX_SOLENOID_LABELS:
			label = AUX_SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = AUX_SOLENOID_WIRING[address]
			physical = {
				"part_number": wiring_data["part_number"],
				"notes": (
					f"Printed AUX {address - 32} on the \"Solenoid Expander Auxiliary\" board "
					f"(SE_BOARDID_520_5068_01, matching simpprtyGameData.hw.display), the same "
					'physical board whitestar.json documents as "expos[ing] three outputs at 33-35". '
					'Manual footnote: "Auxiliary Coils AUX 1 - AUX 3 are typically for UK Only" -- '
					"the retained VPX table (a US/export-configuration recreation) models no object "
					"for these positions."
				),
			}
			items.append(
				_device(
					identifier, label, "coil", "pinmame.output.solenoid", address, "optional",
					(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
					aliases=[
						{"namespace": "pinmame.solenoid", "value": str(address)},
						{"namespace": "manual.address", "value": f"AUX {address - 32}"},
					],
					physical=physical,
					wiring=_solenoid_wiring(address, AUX_SOLENOID_WIRING),
					spatial=not_applicable("unused", MANUAL_SOURCE),
				)
			)
			continue

		if address in FLIPPER_SOLENOID_LABELS:
			label = FLIPPER_SOLENOID_LABELS[address]
			identifier = output_id(label)
			physical_solenoid = 16 if address in (45, 46) else 15
			wiring_data = SOLENOID_WIRING[physical_solenoid]
			role_word = "power" if address in (45, 47) else "hold"
			notes = (
				f"se.c se_solenoid_w: \"move flipper power solenoids (L=15,R=16) to (R=45,L=47)\" -- "
				f"physical Q{physical_solenoid} ({'RIGHT' if physical_solenoid == 16 else 'LEFT'} "
				f"FLIPPER, printed coil #{physical_solenoid}) is masked out of raw address "
				f"{physical_solenoid} and exposed here as its {role_word}-phase public address. "
				"PinMAME synthesizes the paired hold/power state from the same physical coil; a "
				"recreation must bind one physical flipper coil per side, never two."
			)
			items.append(
				_device(
					identifier, label, "coil", "pinmame.output.solenoid", address, "used",
					(MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_CALLBACKS else (MANUAL_SOURCE, CORE_SOURCE),
					aliases=[
						{"namespace": "pinmame.solenoid", "value": str(address)},
						{"namespace": "manual.address", "value": str(physical_solenoid)},
					],
					physical={"part_number": wiring_data["part_number"], "notes": notes},
					wiring=_solenoid_wiring(physical_solenoid, SOLENOID_WIRING),
					spatial=located(identifier, "effect", SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE),
				)
			)
			continue

		label = NOT_FITTED_SOLENOID_LABELS[address]
		identifier = output_id(label)
		notes = {
			15: "PinMAME's synthetic fast-flip and game-on state, not a machine output. se_solenoid_w masks physical Q15 (LEFT FLIPPER 50v RED/YEL) out of this raw address (`sols &= 0xffff3fff`) and exposes that coil at public 47 (power) and 48 (hold); se.c then sets public 15 from ROM RAM byte 0x04 (fastflipaddr) so a host can gate fast flips on it. A hash-pinned harness run of simpprty shows 15 rising to 1 when a game starts and staying there. Only the simpprty driver publishes it: se.c assigns fastflipaddr when the running driver's own name matches \"simpprty\" in its first eight characters, so on the seventeen clone drivers public 15 stays at zero.",
			16: "Physical Q16 (RIGHT FLIPPER 50v RED/YEL); masked the same way as 15. The real physical coil is exposed at public 45 (power) and 46 (hold).",
			36: "whitestar.json: \"board 520-5068-01 exposes three outputs at 33-35 and leaves 36 unused\"; this driver declares no fourth auxiliary output.",
			49: "PinMAME's simulator-only ball-shooter channel; no Whitestar hardware output.",
			50: "Reserved output position at the top of the public solenoid range; simpprtyGameData declares no custSol.",
		}.get(address, "Reserved WPC-family compatibility hole in the public solenoid address space; not populated by any Whitestar hardware on this driver.")
		items.append(
			_device(
				identifier, label, "virtual", "pinmame.output.solenoid", address, "used" if address == 15 else "unused",
				(CONTROLLER_SOURCE, PINNED_CORE_SOURCE, RUNTIME_FLIPPERS) if address == 15 else (CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
				physical={"notes": notes},
				spatial=not_applicable("virtual" if address in (15, 49) else "unused", PINNED_CORE_SOURCE if address == 15 else CORE_SOURCE),
			)
		)
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 11):
			address = (row - 1) * 8 + column
			identifier = f"lamp.matrix-{address}"
			unused = address in UNUSED_LAMP_ADDRESSES
			label = LAMP_LABELS.get(address, f"Not Used Lamp Position {address}")
			bulb = LAMP_BULBS.get(address)
			quantity = LAMP_QUANTITIES.get(address, 1)
			physical: dict[str, Any] = {"quantity": quantity}
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in DOTS_LAMP_ADDRESSES:
				notes += ' Also marked "Diode On Terminal Strip" (DOTS) on the printed matrix.'
			if quantity > 1:
				notes += f" Printed bulb quantity {quantity}."
			drive_wire, drive_connection, drive_component = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, return_component = LAMP_ROW_WIRING[row]
			extra: dict[str, Any] = {
				"aliases": [
					{"namespace": "pinmame.lamp", "value": str(address)},
					{"namespace": "manual.address", "value": str(address)},
				],
				"wiring": {
					"board": "Whitestar power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"column drive {drive_component}; row return {return_component}",
				},
			}
			if unused:
				notes += " Shaded \"NOT USED\" on the printed lamp matrix."
				physical["notes"] = notes
				extra["physical"] = physical
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "unused", (MANUAL_SOURCE, CONTROLLER_SOURCE), **extra))
				continue
			if address == 32:
				notes += (
					' Manual footnote: "Lamp 32, Tournament Button (Optional with Tournament Kit, '
					'Diode in Connector)". The retained script\'s UpdateLamps sequence skips directly '
					"from `NFadeL 31, l31` to `NFadeL 33, l33` -- there is no `l32` object at all -- "
					"matching switch 53's identical optional-tournament-kit status."
				)
				physical["notes"] = notes
				extra["physical"] = physical
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "optional", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE), **extra))
				continue
			if 73 <= address <= 80:
				led = MODE_SIGN_LED[address]
				notes += (
					f" Mode-sign LED {led}. The manual's lamp-location page stamps 73-80 in one column "
					'"on Sign" at the rear of the playfield, above it (white stamp), and its parts pages '
					"put them on LED PCB (Mode Signifier) 520-5225-00, bolted through bracket 535-9232-00 "
					"to the back panel next to the TV and read through the screened mode plastic (manual "
					"PDF 82, 114, 170; its test note on PDF 42 calls these LEDs lamps 73-80). The lamp "
					"page's own footnote names board 520-5219-00 instead, which the same manual gives to "
					"the TV's Color Dot Display; the three specific pages agree, so that footnote is a "
					"typo and not a separate device. The LEDs are ordinary lamp-matrix positions on row "
					"10 (J12-P11, Q42); they are not the TV's dot matrix, which pinned PinMAME publishes "
					"as the separate mini-DMD display, and se.c types 73-80 as strobed LEDs. The "
					"retained known-working script drives them with NFadeObj onto Primitive l"
					f"{address} of the table's sign (a table-side name, \"Moes Sign\")."
				)
				if address == 80:
					notes += (
						" Two red LEDs share this address: L8 at the bottom-left and L9 at the "
						"bottom-right of the ALIEN INVASION panel (manual PDF 114 and 170; the lamp "
						"page stamps 80 twice). Every retained table models one object, l80, at the "
						"column position (z 165), so no coordinate exists for L9 and no spatial key is "
						"claimed rather than a one-of-two placement."
					)
				else:
					notes += (
						" The sign is vertical and faces the player, so L1-L7 stack in one column and "
						"share one playfield point; this lamp is placed at its own primitive's x/y "
						f"(normalized {MODE_SIGN_LAMP_POSITIONS[address][0]}, "
						f"{MODE_SIGN_LAMP_POSITIONS[address][1]}), and its height on the sign "
						"(retained z 305 for lamp 73 falling 20 units per lamp) is the only thing that "
						"separates it from its neighbours."
					)
				physical["notes"] = notes
				physical["location"] = "back panel LED mode sign (above the playfield)"
				extra["physical"] = physical
				if address in MODE_SIGN_LAMP_POSITIONS:
					extra["spatial"] = located(
						identifier, "emitter", [MODE_SIGN_LAMP_POSITIONS[address]], VPX_TABLE_SOURCE, MANUAL_SOURCE
					)
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, PINNED_CORE_SOURCE, RUNTIME_STACKING)
				items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
				continue
			physical["notes"] = notes
			extra["physical"] = physical
			extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
			items.append(_device(identifier, label, "lamp", "pinmame.output.lamp", address, "used", refs, **extra))
	# Public 81-96: published by PinMAME, fed only by CPU ports $3406/$3407, tied to no hardware.
	for address in AUX_PORT_LAMP_ADDRESSES:
		port, bit = (0x3406, address - 81) if address <= 88 else (0x3407, address - 89)
		items.append(
			_device(
				f"lamp.aux-port-{address}", f"Unassigned Lamp Port ${port:04X} Bit {bit}", "virtual",
				"pinmame.output.lamp", address, "unknown",
				(PINNED_CORE_SOURCE, MANUAL_SOURCE, RUNTIME_STACKING, RUNTIME_FLIPPERS),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={
					"notes": (
						f"PinMAME publishes public lamps 1-96 for this driver because simpprtyGameData declares "
						f"hw.lampCol = 4 (se.c nLamps = 64 + 4*8; vpintf.c vp_getChangedLamps scans 8 + 4 columns). "
						f"The printed 8x10 matrix fills 1-80; this address is bit {bit} of coreGlobals.lampMatrix"
						f"[{10 + (address - 81) // 8}], which only se.c's gilamp_w writes, copying the byte the CPU stores at port "
						f"${port:04X} (the memory map's own comment: \"GI lamps on Simpsons?\"). In LibPinMAME's "
						"physical-output mode nothing writes this output for this driver, so it reads zero there. "
						"No lamp circuit exists for it: the manual's lamp matrix has exactly eight drive columns "
						"(J13, U10-U17) and ten return rows (J12, Q33-Q42), all of them accounted for by 1-80. "
						"Three hash-pinned harness runs (boot, attract mode and a started game, about 210 s in "
						"all) never saw it change; that does not prove the ROM never writes it, so availability "
						"stays unknown. "
						"Resolution path: static analysis of simpprty's CPU ROM for every write that can reach "
						"$3406-$3407, or a harness run of the ROM's own lamp tests watching 81-96."
					)
				},
				spatial=not_applicable("virtual", PINNED_CORE_SOURCE),
			)
		)
	return items


def gi_outputs() -> list[dict[str, Any]]:
	identifier = "gi.string-1"
	notes = (
		"Whitestar publishes exactly one aggregate GI relay (coreGlobals.nGI = 1, se.c). The "
		"manual's General Illumination Circuit Detailed Wiring Diagram (PDF 121, printed 103) "
		"shows one relay (U206 74HCT273 data-latch bit through Q200 2N3904) closing four "
		"separately-fused branches simultaneously (F24 backpanel, F25 left playfield + right "
		"return lane, F26 upper mini-playfield + spotlights + coin door, F27 right playfield) -- "
		"a single-relay, multi-fuse design, not four independently switched circuits, matching "
		"PinMAME's single-channel model exactly. The retained script's UpdateGI toggles every "
		"member of its own `GI` collection together (`For each xx in GI:xx.State = ...`), the "
		"same single-relay behavior. Bulb quantity/location per fused branch is transcribed in "
		"evidence/excerpts/.../general-illumination.md; the manual's own quantities are printed "
		'"may change during production", so the retained table\'s 42-member `GI` collection (37 '
		"`GI_N` Light objects plus 5 `spotlightright*` objects) is used as the placement set "
		"rather than a hand count from the diagram."
	)
	return [
		_device(
			identifier, "General Illumination", "gi", "pinmame.output.gi", 0, "used",
			(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.gi", "value": "0"}],
			physical={"quantity": len(GI_POSITIONS), "notes": notes},
			spatial=located(identifier, "emitter", GI_POSITIONS, VPX_TABLE_SOURCE),
		)
	]


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
		},
		{
			"id": "display.mini-dmd",
			"label": "Mini DMD (14x10 bicolor LED sign)",
			"kind": "video",
			"controller_index": 3,
			"width": 10,
			"height": 14,
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
			"Five-ball trough and ball release",
			"kicker",
			[output_id("Trough Up-Kicker")],
			["switch.matrix-10", "switch.matrix-11", "switch.matrix-12", "switch.matrix-13", "switch.matrix-14", "switch.matrix-15"],
			"Five balls rest in a trough that the manual's switch-location drawing shows rising "
			"from left to right: 5-Ball Trough #1 (switch 10) at the far left end, then 11, 12 and "
			"13, and the 5-Ball Trough VUK Opto (14) at the right-hand exit end under the up-kicker, "
			"with the 5-Ball Stacking Opto (15) stamped at the same exit location above it. The "
			"retained script's bsTrough.InitSw 0,14,13,12,11,10,0,0 agrees: 14 is the exit position "
			"the kicker empties, 10 the last. core.vbs's cvpmBallStack reads all five through its "
			"internal ball queue, asserting each occupied position at 1, rather than exposing five "
			"playfield trigger objects. Solenoid 1 (Trough Up-Kicker, SolRelease) kicks the exit "
			"ball up into the shooter lane, and the script pulses 15 as the ball passes the stacking "
			"beam. With five balls on 10-14, the ROM answers 15 at 1 by firing the up-kicker "
			"(six attempts in a hash-pinned harness run where no ball can move) and then the auto "
			"launch; 15 at 0 draws nothing. Switches 14 and "
			"15 share one Transmitter/Receiver opto-PC-board pair per the manual's Sw.14/15 "
			"footnote.",
			[
				("position-1", "Trough exit (VUK opto)", ["switch.matrix-14"], "5-Ball Trough VUK Opto, the ball the up-kicker lifts next."),
				("position-2", "Trough Ball 4", ["switch.matrix-13"], "5-Ball Trough #4."),
				("position-3", "Trough Ball 3", ["switch.matrix-12"], "5-Ball Trough #3."),
				("position-4", "Trough Ball 2", ["switch.matrix-11"], "5-Ball Trough #2."),
				("position-5", "Trough Ball 1 (far end)", ["switch.matrix-10"], "5-Ball Trough #1 (Left), the last position to fill."),
				("stacking-opto", "Trough stacking opto", ["switch.matrix-15"], "Senses a ball stacked above the exit ball, or passing up the kicker path."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE, VPM_CORE_SOURCE, RUNTIME_STACKING,
		),
		mechanism(
			"mechanism.drop-target-bank",
			"Three-target drop bank",
			"drop_target_bank",
			[output_id("Drops Reset Up"), output_id("Drop Bank Trips")],
			["switch.matrix-17", "switch.matrix-18", "switch.matrix-19"],
			"Three printed drop targets (#1 Top, #2 Mid, #3 Bot) share one reset solenoid "
			"(4, Drops Reset Up) and one trip solenoid (30, Drop Bank Trips, used for testing/"
			"rule resets). The retained script's dtDrop = New cvpmDropTarget, "
			"dtDrop.InitDrop Array(sw17, sw18, sw19), Array(17, 18, 19) wires the three "
			"HitTarget objects directly to matrix switches 17-19; SolDropBankTrips fires "
			"dtDrop.Hit 1/2/3 to knock all three down together.",
			[
				("top", "Drop Target #1 (Top)", ["switch.matrix-17"], "Topmost target in the bank."),
				("mid", "Drop Target #2 (Mid)", ["switch.matrix-18"], "Middle target."),
				("bot", "Drop Target #3 (Bot)", ["switch.matrix-19"], "Bottom target."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="180-5158-00",
		),
		mechanism(
			"mechanism.couch-lock",
			"Couch multiball lock",
			"gate",
			[output_id("Couch Release")],
			["switch.matrix-38", "switch.matrix-39", "switch.matrix-40", "switch.matrix-36"],
			"A ball enters through the Couch Enter gate (switch 36) and stacks on up to three "
			"lock positions (38 Bot, 39 Mid, 40 Top). Solenoid 3 (Couch Release, script sub "
			"CouchExit) opens a drop gate (CouchDrop) to release the stack; CouchDrop_Hit clears "
			"switch 38 as the released ball passes, and a DropCheck timer resets the Drop1 table "
			"object afterward.",
			[
				("bot", "Couch Lock (Bot)", ["switch.matrix-38"], "Lowest/first lock position."),
				("mid", "Couch Lock (Mid)", ["switch.matrix-39"], "Middle lock position."),
				("top", "Couch Lock (Top)", ["switch.matrix-40"], "Highest/last lock position."),
				("enter", "Couch Enter gate", ["switch.matrix-36"], "Entry gate switch."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="28-1050/090-5046-00",
		),
		mechanism(
			"mechanism.tv-lock-post",
			"TV lock post",
			"diverter",
			[output_id("TV Release")],
			["switch.matrix-37"],
			"Solenoid 7 (TV Release) raises and lowers a post (TopPost) that holds a ball at the "
			"TV Lockup switch (37): SolTVRelease sets TopPost.IsDropped = 1 to release, 0 to "
			"block. There is no separate lock-position sensor beyond switch 37 itself.",
			[("locked", "Ball held at TV lockup", ["switch.matrix-37"], "TV Lockup switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="28-1050/090-5046-00",
		),
		mechanism(
			"mechanism.garage-door",
			"Motorized garage door",
			"motorized",
			[output_id("Garage Door (Eject)")],
			["switch.matrix-48"],
			"Solenoid 20 (Garage Door (Eject)) drives an incremental open/close motion: the "
			"retained script's GarageUp sets DoorStatus and enables a GDoorT timer that steps "
			"Gdoor.RotX by 4 degrees per tick (0-60 degrees) rather than firing a single pulse; "
			"switch 48 (Garage Door) is set/cleared only once the door reaches its open or closed "
			"limit (sw48.isdropped = 1/0), not continuously during the sweep.",
			[("open", "Garage door open", ["switch.matrix-48"], "Door-open limit, asserted once RotX reaches 60 degrees.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="500-6138-01R",
		),
		mechanism(
			"mechanism.homer-head",
			"Homer Head toy",
			"toy",
			[output_id("Homer Head")],
			[],
			"Solenoid 8 (Homer Head) actuates a moving figure (HHead); the retained script's "
			"HomerOn_Timer/HomerOff_Timer animate its rotation while HomerActive is set. Ball "
			"position relative to the figure is tracked by four internal VPX trigger objects "
			"(Homer, Homer2, Homer3, homer4) that contain no Controller.Switch call anywhere in "
			"the retained script -- they drive only the figure's own animation state, not any "
			"public switch address.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="22-900/090-5020-20T",
		),
		mechanism(
			"mechanism.upper-and-top-right-flippers",
			"Upper mini-playfield flippers and Top Right Flipper",
			"other",
			[output_id("UPF Left Flipper"), output_id("UPF Right Flipper"), output_id("Top Right Flipper")],
			["switch.dedicated-ds-1", "switch.dedicated-ds-5"],
			"Three flipper coils (12 UPF Left Flipper, 13 UPF Right Flipper, 14 Top Right "
			"Flipper) are ordinary numbered solenoids outside PinMAME's synthesized flipper "
			"subsystem (simpprtyGameData.hw.flippers declares FLIP_L only); the ROM fires them from "
			"the cabinet buttons. A hash-pinned harness run with a game in progress shows the left "
			"button DS-1 (public 84) energising 12 together with the lower left flipper, and DS-5 "
			"(public 88) energising 13 and 14 together, while DS-3 (public 82) alone fires only the "
			"lower right flipper. DS-5 is the second contact of the doubled right cabinet button "
			"(part 180-5164-00 Doubled, drawn on the same button as DS-3), so on the machine one "
			"right-button press fires the lower right, upper-mini-playfield right and top right "
			"flippers together. PinMAME never synthesizes public 88 from its own keyboard handling, "
			"but it preserves a host write to it, so a recreation drives 82 and 88 together from its "
			"right flipper button.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, PINNED_CORE_SOURCE, RUNTIME_FLIPPERS,
		),
		mechanism(
			"mechanism.lower-flippers",
			"Lower flipper pair",
			"other",
			[
				output_id("Right Flipper Power"), output_id("Right Flipper Hold"),
				output_id("Left Flipper Power"), output_id("Left Flipper Hold"),
			],
			["switch.dedicated-ds-1", "switch.dedicated-ds-2", "switch.dedicated-ds-3", "switch.dedicated-ds-4"],
			"Two 50V flipper coils (printed #15 Left, #16 Right) with separate power and hold "
			"windings; se_solenoid_w masks physical 15/16 out of the raw solenoid group and "
			"exposes each coil at a power-phase and canonical-callback public address pair "
			"(16->45/46, 15->47/48). Dedicated switches DS-1..DS-4 (public 84/83/82/81) supply "
			"the button and end-of-stroke inputs; se.c's dedswitch_r nibble-reverses the raw "
			"flipper-column byte to present them in DS-1..DS-4 order.",
			[
				("right", "Lower right flipper", ["switch.dedicated-ds-3", "switch.dedicated-ds-4"], "Button DS-3 (public 82) and E.O.S. DS-4 (public 81)."),
				("left", "Lower left flipper", ["switch.dedicated-ds-1", "switch.dedicated-ds-2"], "Button DS-1 (public 84) and E.O.S. DS-2 (public 83)."),
			],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="22-1080/090-5032-00T",
		),
		mechanism(
			"mechanism.jet-bumpers",
			"Three-bumper jet nest",
			"other",
			[output_id("Left Bumper"), output_id("Right Bumper"), output_id("Bottom Bumper")],
			["switch.matrix-49", "switch.matrix-50", "switch.matrix-51"],
			"Three jet bumpers. The retained script's object names do not match printed side "
			"directly: Bumper1_Hit pulses switch 50 (Right Bumper) and fires solenoid 10; "
			"Bumper2_Hit pulses switch 51 (Bottom Bumper) and fires solenoid 11; Bumper3_Hit "
			"pulses switch 49 (Left Bumper) and fires solenoid 9. Confirmed geometrically: "
			"Bumper3 (leftmost x) -> Left Bumper, Bumper1 (rightmost x) -> Right Bumper, Bumper2 "
			"(largest y / frontmost) -> Bottom Bumper.",
			[
				("left", "Left jet bumper", ["switch.matrix-49"], "Bumper3 object; leftmost of the nest."),
				("right", "Right jet bumper", ["switch.matrix-50"], "Bumper1 object; rightmost of the nest."),
				("bottom", "Bottom jet bumper", ["switch.matrix-51"], "Bumper2 object; frontmost of the nest."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="26-1200/090-5044-00T",
		),
		mechanism(
			"mechanism.slingshots",
			"Left and right slingshots",
			"other",
			[output_id("Left Slingshot"), output_id("Right Slingshot")],
			["switch.matrix-59", "switch.matrix-62"],
			"Two slingshots; the retained table's LeftSlingShot/RightSlingShot wall objects sit "
			"at matrix switches 59 and 62, fired by solenoids 17 and 18 respectively (23-800/"
			"090-5001-00T coils).",
			[
				("left", "Left slingshot", ["switch.matrix-59"], "Left slingshot score switch."),
				("right", "Right slingshot", ["switch.matrix-62"], "Right slingshot score switch."),
			],
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="23-800/090-5001-00T",
		),
		mechanism(
			"mechanism.itchy-and-scratchy-eject",
			"Itchy & Scratchy VUK saucer",
			"kicker",
			[output_id("Itchy & Scratchy Eject (VUK)")],
			["switch.matrix-20"],
			"A ball resting in the Itchy & Scratchy saucer (switch 20, Kicker object sw20) is "
			"ejected by solenoid 5; the retained script's bsBR = New cvpmBallStack, "
			"bsBR.InitSaucer sw20, 20, 232, 18 confirms the switch/solenoid pairing.",
			[("held", "Ball in Itchy & Scratchy saucer", ["switch.matrix-20"], "Saucer switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="27-1500/090-5004-00T",
		),
		mechanism(
			"mechanism.upper-right-eject",
			"Upper Right saucer",
			"kicker",
			[output_id("Upper Right Eject")],
			["switch.matrix-24"],
			"A ball resting in the Upper Right saucer (switch 24, Kicker object sw24) is ejected "
			"by solenoid 19; bsTR.InitSaucer sw24, 24, 100, 1 confirms the pairing.",
			[("held", "Ball in Upper Right saucer", ["switch.matrix-24"], "Saucer switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="26-1200/090-5044-00T",
		),
		mechanism(
			"mechanism.upper-left-vuk",
			"Upper Left VUK",
			"kicker",
			[output_id("Upper Left VUK")],
			["switch.matrix-55"],
			"A ball resting on the Upper Left VUK opto (switch 55, Kicker object sw55) is "
			"ejected by solenoid 6 through kicker object VukOut; bsVuk.InitSw 0,55,0,0,0,0,0,0 "
			"with bsVuk.InitKick VukOut, 180, 0 confirms the pairing.",
			[("held", "Ball at Upper Left VUK", ["switch.matrix-55"], "VUK opto switch.")],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="26-1200/090-5044-00B",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-release-stacking-opto",
			"kind": "pulse",
			"source": output_id("Trough Up-Kicker"),
			"destination": "switch.matrix-15",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	# Both former conflicts were settled on 2026-09-25 and removed rather than ignored, because
	# neither left a disagreement about the machine standing.
	# conflict.whitestar-invsw-never-populated: switch 14's public sense comes from the
	# known-working script (cvpmBallStack asserts the exit position at 1 while a ball is there)
	# and switch 15's from the RUNTIME_STACKING ROM runs; both are recorded on the devices.
	# conflict.upper-flipper-button-not-read: the manual's "doubled" right button and its
	# switch-location drawing make DS-5 the right button's second contact, and pinned core.c
	# preserves a host write to public 88 (it only never synthesizes it). The RUNTIME_FLIPPERS
	# run shows the ROM firing solenoids 13 and 14 from 88. A fitted input and an emulator that
	# does not synthesize it are two compatible facts, now stated on switch 88 and solenoids 13/14.
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
			"id": "stern.the-simpsons-pinball-party.2003",
			"name": "The Simpsons Pinball Party",
			"manufacturer": "Stern",
			"year": 2003,
			"kind": "physical_pinball",
			"ipdb_id": 4674,
			"playfield": {"width": 952.0, "height": 2115.0, "units": "vpx"},
			"opdb_id": "GRvBL-MP3Ev",
		},
		"coverage": {
			"status": "partial",
			# output_semantics: public lamps 81-96 are enumerated but their availability is
			# unknown (only CPU ports $3406/$3407 feed them). spatial_placement: lamp 80's second
			# red LED (L9) has no retained coordinate.
			"missing": ["output_semantics", "spatial_placement"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "candidate",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "candidate",
			},
		},
		"controller": {
			"platform": "pinmame.whitestar",
			"hardware_generation": "0x4000000000",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/stern/the-simpsons-pinball-party-2003.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Simpsons Pinball Party device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	omitted_inputs: list[int] = []
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			omitted_inputs.append(address)
		elif spatial["status"] == "not_applicable":
			not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
		else:
			located_inputs.append(address)
	located_outputs: list[dict[str, Any]] = []
	not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
	omitted_outputs: list[dict[str, Any]] = []
	placement_count = 0
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
			"Lamp 80 (ALIEN INVASION) is two red LEDs on the mode-sign board, L8 at the bottom-left "
			"and L9 at the bottom-right of the plastic (manual PDF 114 and 170; the lamp page stamps "
			"80 twice). Every retained table models one object, l80, at the sign's column position, "
			"so L9 has no coordinate. Lamp 80 carries no spatial key rather than a one-of-two "
			"placement that would understate its quantity.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2115.0},
			"x": "x/952; 0=left, 1=right",
			"y": "y/2115; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/extracted-vpxtool.manifest.json",
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
		"omitted_inputs": sorted(omitted_inputs),
		"omitted_outputs": sorted(omitted_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": (
			[{"group": "pinmame.input.switch", "address": address, "reason": reason} for address, reason in sorted(SWITCH_PROJECTIONS.items())]
			+ [{"group": "pinmame.output.solenoid", "address": address, "reason": reason} for address, reason in sorted(SOLENOID_PROJECTIONS.items())]
		),
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/stern.the-simpsons-pinball-party.2003/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"Homer, Homer2, Homer3, homer4 internal VPX triggers (Homer Head figure animation helpers; no Controller.Switch call)",
			"Trigger1-Trigger6 (PlaySound-only audio-cue helpers; no Controller.Switch call)",
			"swplunger (internal ball-detection helper for the cvpmImpulseP shooter-lane class; switch 16 itself is bound to the separately-named sw16 object)",
			"CapKicker/capBall (a static decorative captive-ball prop with no switch or solenoid binding)",
			"l80 Primitive (models only one of lamp 80's two LEDs; see blockers)",
			"LEDY, LEDG and LEDR collections (empty; hidden by the script at start-up and bound to no lamp)",
			"r*/g*/y* TV LED lights (the 14x10 mini-DMD, driven from Controller.ChangedLEDs, a display rather than lamps)",
		],
		"unresolved": [],
		"mode_sign": {
			"board": "LED PCB (Mode Signifier) 520-5225-00 on bracket 535-9232-00, bolted to the back panel next to the TV",
			"manual_pages": "PDF 37, 42, 82, 114, 170",
			"construction": "vertical sign facing the player; L1-L7 (lamps 73-79) in one column, L8 and L9 (lamp 80) at the bottom-left and bottom-right",
			"placement_rule": "each of lamps 73-79 placed at its own retained Primitive's x/y; they differ only in height (z 305 down to 185), which the playfield plane does not represent",
			"control_object": "Primitive.RubberPostT23 position (411.9, 127.2) coincides with Rubber.Rubber33's drag-point centroid (411.3, 126.7), and the l73-l80 meshes are local (every vertex within 7 units of the origin), so a Primitive position is its world placement here",
		},
		"additional_tables_checked": [
			{
				"original_filename": "Simpsons Pinball Party, The (Stern 2003).vpx",
				"found_in": "the contributor's Tables and Tables Archive folders (byte-identical copies)",
				"table_sha256": "c15f41e42921dfaebbd42e382573e2bcc09d5af45860218565a2e3b3de041561",
				"script_sha256": "145c65db98712a916f678078b519fc6c13c93b56acf46e8f2c70a3f8ac7f9c10",
				"manifest_uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/alt-tables/Simpsons Pinball Party, The (Stern 2003).manifest.json",
				"manifest_sha256": "da51e690d8b51c45864d5214ab3e7b9da5cca6d704effb85755cc5942a698005",
				"file_count": 1320,
				"total_bytes": 105934503,
				"finding": "same Coindropper/32assassin script base; l73-l80 at the same coordinates as the retained table",
			},
			{
				"original_filename": "The Simpsons Pinball Party (Stern 2003).vpx",
				"found_in": "the contributor's Tables Archive folder",
				"table_sha256": "6db86f7609ec68e220d0115289a48218a5076bfa6ff0301bb0c00b279d124ee1",
				"script_sha256": "a77a5dcabe6f4748c5ab8abb6f2f07f09065c9bb8e1a74c808a5c6cb29f7422e",
				"manifest_uri": "external:pinmame-vpx-sources/stern/the-simpsons-pinball-party-2003/alt-tables/The Simpsons Pinball Party (Stern 2003).manifest.json",
				"manifest_sha256": "eab2a2606c183dc42b49a93ae1a3c38f366e9eb6238e98f2621aa432647e9b20",
				"file_count": 1406,
				"total_bytes": 173391321,
				"finding": "same script base with added lighting code; l73-l80 at the same coordinates as the retained table",
			},
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# The Simpsons Pinball Party (Stern, 2003) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record itself is `partial` at "
		"`machines/partial/stern/the-simpsons-pinball-party-2003.json` for the reasons below; "
		"every located device carries a validated placement or a documented projection, and one "
		"honest gap remains: the second red LED of lamp 80.",
		"",
		"The matching source is the retained known-working, non-VPW `The Simpsons Pinball Party "
		f"v0.8.2.vpx` at SHA-256 `{TABLE_SHA256}`. The retained `vpxtool` extraction produced the "
		f"embedded script at SHA-256 `{SCRIPT_SHA256}`; that embedded stream is the runtime and "
		f"causality authority. Exact playfield bounds are `{TABLE_BOUNDS}`, and every canonical "
		"coordinate is x/952 and y/2115 rounded to at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Stern "
		"operations manual is the physical inventory, quantity, polarity, and wiring authority; "
		"pinned PinMAME owns controller topology and public address arithmetic; the retained "
		"table supplies geometry.",
		"- The retained manual's text layer double-doubles most characters and additionally "
		"shifts character codes by a constant on the diagnostics chapter's own embedded font "
		"subset; every printed table used here was read from a rendered page and transcribed "
		"into `external:pinmame-review-artifacts/the-simpsons-pinball-party-2003/"
		"manual-transcription.md`, never from `pdftotext` output.",
		"- Trough switches 10-14 and the stacking opto 15 have no dedicated playfield trigger "
		"object because the retained script reads the five ball positions through the shared "
		"cvpmBallStack helper class and pulses 15 from SolRelease rather than from Hit/Unhit "
		"events; all six are documented projections onto the trough's own release-kicker object "
		"(BallRelease). The manual's switch-location drawing puts 10 at the trough's far left end "
		"and stamps 14 and 15 together at its right-hand exit.",
		"- Solenoids 4 (Drops Reset Up) and 30 (Drop Bank Trips) act on all three drop-target "
		"bank positions at once and have no separate reset-bar mesh in the retained table; both "
		"are documented projections onto the bank's own middle target (Drop Target #2).",
		"- Lamp 32 (Tournament Button) and matrix switch 53 (Tournament Button) are both "
		"optional, gated behind the Optional Tournament Kit per matching manual footnotes on "
		"both the switch- and lamp-locations pages; lamp 32 additionally has no `l32` object in "
		"the retained script's own lamp-fade sequence at all.",
		"- Lamps 73-80 are the LEDs of the mode sign (LED PCB Mode Signifier 520-5225-00) bolted "
		"to the back panel next to the TV, above the playfield (manual PDF 37, 42, 82, 114, 170). "
		"The sign is vertical and faces the player, so L1-L7 share one playfield point and differ "
		"only in height. The retained script drives them with NFadeObj onto primitives l73-l80, "
		"which sit at one x/y and step down in z in the manual's order; lamps 73-79 are each "
		"placed at their own primitive's x/y. Lamp 80 is two LEDs and the tables model one, so it "
		"has no spatial key. Two further local tables were extracted and checked; both share the "
		"retained table's script base and place l73-l80 identically, so they add no independent "
		"geometry. The earlier reading of these lamps as the empty LEDY/LEDG/LEDR collections was "
		"wrong: those collections are unused, and the script's UpdateLeds drives the TV's 14x10 "
		"mini-DMD, which PinMAME publishes as a display.",
		"- Public lamps 81-96 are enumerated as virtual outputs with unknown availability and a "
		"controlled `virtual` record; no lamp circuit exists for them.",
		"- General illumination is a single aggregate PinMAME channel (`coreGlobals.nGI = 1`); "
		"its 42 placements come directly from the retained table's own `GI` collection (37 "
		"`GI_N` Light objects plus 5 `spotlightright*` objects), which the script's UpdateGI "
		"toggles together, matching the manual's own single-relay, multi-fuse wiring diagram.",
		"- Solenoid 24 (Optional Coil) and solenoids 33-35 (AUX 1-3, UK-only up/down posts) take "
		"controlled `not_applicable`/`unused` records per their explicit manual footnotes; the "
		"retained table (a US/export-configuration recreation) models no object for any of them.",
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
		f"- Inputs with no spatial key at all: {len(report['omitted_inputs'])}",
		f"- Outputs with no spatial key at all: {len(report['omitted_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"This record stays `partial`. Its conflicts are settled: switch 14's public sense comes "
		"from the known-working script and switch 15's from hash-pinned ROM runs, and DS-5 (public "
		"88) is the right button's second contact, which PinMAME does not synthesize but does "
		"deliver to the ROM, which fires solenoids 13 and 14 from it. Two gaps remain. Lamp 80's "
		"second LED has no coordinate (`spatial_placement`), and public lamps 81-96, which PinMAME "
		"publishes because the driver declares four auxiliary lamp columns, are fed only by CPU "
		"ports $3406/$3407 and have unknown availability (`output_semantics`). "
		"`coverage.missing = [\"output_semantics\", \"spatial_placement\"]` records both.",
		"",
		"## Retained evidence",
		"",
		f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 "
		f"`{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
		f"- Human transcription of every printed table and diagram read from the rendered manual "
		f"pages, SHA-256 `{MANUAL_TRANSCRIPTION_SHA256}`.",
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
		raise RuntimeError(f"Stale Simpsons Pinball Party author-ready definition is present: {stale_author_ready_path}")
	if not definition_path.is_file():
		raise RuntimeError(f"Simpsons Pinball Party definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Simpsons Pinball Party seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Simpsons Pinball Party definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Simpsons Pinball Party seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Simpsons Pinball Party spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Simpsons Pinball Party spatial review drifted from its deterministic curator: {markdown_path}")
	print("Simpsons Pinball Party definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Simpsons Pinball Party extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Simpsons Pinball Party retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
