"""Curate the physical Williams High Speed (1986) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail,
and normalized coordinate as a literal, so regeneration reproduces the canonical artifact
byte-for-byte without reading the external evidence roots. ``--check`` refuses drift, and
``--regenerate`` is the only path that writes the canonical definition and its pinned seed.

High Speed is the second System 11 machine curated in this project and reuses
``controllers/pinmame/system-11.json`` unchanged, but almost none of Whirlwind's per-game reasoning
transfers. ``hsGameData`` declares ``sxx.muxSol = 0``, so there is no A/C select relay and the
platform's 25-32 "C"-side alias bank is never populated; ``hw.gameSpecific1 = 0``, so there is no
sound-overlay board at 37-44 and switch 2 is never overwritten by mux feedback; general illumination
is a single relay at solenoid 11 rather than Whirlwind's two; and it is the first game in the project
to populate ``sxx.ssSw``, the special-solenoid-to-switch map that makes public solenoids 17-22 follow
their own actuating switch directly.
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
DEFINITION_PATH = ROOT / "machines/partial/williams/high-speed-1986.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/high-speed-1986.json"
SEED_PATH = ROOT / "tools/seeds/williams/high-speed-1986.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/high-speed-1986.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/high-speed-1986.md"

MACHINE_ID = "williams.high-speed.1986"
KNOWLEDGE_PATH = "knowledge/williams/high-speed-1986.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-system-11"
MANUAL_SOURCE = "manual.williams.high-speed.1986"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.high-speed.1986"
VPX_TABLE_SOURCE = "vpx-table.high-speed-1986"
VPX_SCRIPT_SOURCE = "vpx-script.high-speed-1986"
VPX_EXTRACTION_SOURCE = "vpx-extraction.high-speed-1986"

TABLE_SHA256 = "f57801a428f78f85b6cd40f4e47a74bd8e063227355d26ec4f15ef7f11d78af1"
SCRIPT_SHA256 = "149cab01a1fbe7657ffae87f72fa6982ed631653627b938186d5d8ed893195eb"
MANUAL_SHA256 = "4aa21267d2edf016c2450f35e23b01eea74ff07e25b4b9a9d9c472f5c9e8c1dd"
MANUAL_TRANSCRIPTION_SHA256 = "7ec30ad943a45cf4407cc0ce6001c6dad1b6f5eaf28c7420f349cd531551aa98"
VPX_GEOMETRY_SHA256 = "58b98d92fc633c8b5ef2f02adda885d8195a2d63dc76cd018041a338fb7f2c0f"

EXTRACTION_RELATIVE_PATH = Path("williams/high-speed-1986/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/high-speed-1986/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 1712

TABLE_BOUNDS = "left=0 top=0 right=952 bottom=1974"
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 1974.0

DRIVER_IDS = ("hs_l4", "hs_l3", "hs_l1", "hs_p4g", "hs_l4c")
DRIVER_COMPATIBILITY = {
	"hs_l4": (
		"identical",
		"Williams production L-4 ROM shipped with the physical machine; the pinned catalog's clone-tree "
		"parent and the driver the retained known-working VPX table binds (cGameName = \"hs_l4\").",
	),
	"hs_l3": (
		"identical",
		"Williams L-3 game ROM revision (U26 only; the pinned ROM set pairs it with the same L-4 U27, "
		"flagged '//!! L-4?!' in the driver source). Shares hsGameData/init_hs with the parent through "
		"CORE_CLONEDEF, so the switch matrix, lamp matrix, solenoid table, special-solenoid switch map "
		"and playfield hardware are all unchanged.",
	),
	"hs_l1": (
		"identical",
		"Earliest dumped game ROM revision, dumped from a Unidesa / Cirsa licensed board and catalogued "
		"at 1985. The pinned driver's own comment says the board is 'identical to the Williams board "
		"(also same P/N)' and that the dump is 'very likely to match the (so far undumped) L-1 original "
		"Williams ROMs'. The licensed cabinet additionally carried a Credit Conversion PCB (an 8035 with "
		"its own 2716 EPROM, a 4-position DIP bank and a 6.144 MHz crystal, undumped) which is coin-door "
		"pricing hardware outside the CPU board's own address space and changes no playfield device. The "
		"1985 catalogue year is the licensee's build date, not a different physical machine: this driver "
		"shares hsGameData/init_hs with the parent and PinMAME declares it a clone of hs_l4.",
	),
	"hs_p4g": (
		"identical",
		"German export game ROM (the pinned source records a board whose U26 was stickered 'PROTO4' but "
		"reports as G-4, paired with an L-4 U27, with the German text held in the extra 8K of the larger "
		"EPROM and selected by Adjustment #51). Firmware localization only; shares hsGameData/init_hs "
		"with the parent. The manual's own Special Preset Adjustments 53-60 ('Install German 1' through "
		"'Install German 4') show the production machine already carries German pricing and rules "
		"presets, so no hardware differs.",
	),
	"hs_l4c": (
		"identical",
		"2018 community 'Competition MOD' patch of the L-4 game ROMs (the pinned source retains both the "
		"older 6b05 patch, commented out, and the newer f43c patch that is registered). Runs on the "
		"unmodified physical machine and shares hsGameData/init_hs with the parent; it changes rules and "
		"scoring only.",
	),
}

# --- Switch matrix (public address = (column-1)*8+row; System 11 sequential column-major).
# Labels of record come from the Switches parts list (printed page 32). Where the Switch-Matrix Table
# (printed page 26) wording differs it is preserved in MATRIX_PAGE_WORDING below.
SWITCH_LABELS = {
	1: "Plumb Bob Tilt", 2: "Ball Roll Tilt", 3: "Credit Button",
	4: "Right Coin Chute", 5: "Center Coin Chute", 6: "Left Coin Chute",
	7: "Slam Tilt", 8: "High Score Reset",
	9: "Outhole", 10: "Left Trough", 11: "Center Trough", 12: "Right Trough",
	13: "Red Target (Lower Left Stoplight Bank)", 14: "Yellow Target (Lower Left Stoplight Bank)",
	15: "Green Target (Lower Left Stoplight Bank)", 16: "Eject Hole",
	17: "Red Target (Upper Left Stoplight Bank)", 18: "Yellow Target (Upper Left Stoplight Bank)",
	19: "Green Target (Upper Left Stoplight Bank)",
	20: "Left Flipper Return Lane", 21: "Right Flipper Return Lane",
	22: "Red Target (Right Stoplight Bank)", 23: "Yellow Target (Right Stoplight Bank)",
	24: "Green Target (Right Stoplight Bank)",
	25: "Standup Target Arrow 1", 26: "Standup Target Arrow 2", 27: "Standup Target Arrow 3",
	28: "Standup Target Arrow 4", 29: "Standup Target Arrow 5", 30: "Standup Target Arrow 6",
	31: "Left Outlane", 32: "Right Outlane",
	33: "Upper Left Jet Bumper", 34: "Lower Left Jet Bumper", 35: "Right Jet Bumper",
	36: "Ball Shooter",
	37: "Left Flipper Lane Change (Engine Revs)", 38: "Right Flipper Lane Change (Engine Revs)",
	39: "Upper Left Hideout", 40: "Lower Left Hideout",
	41: "Playfield Tilt", 42: "Left Ramp", 43: "Right Ramp",
	44: "Left Spinner", 45: "Center Spinner", 46: "Right Spinner",
	47: "Upper Right Hideout", 48: "Lower Right Hideout",
	49: "Left Kicker (scoring)", 50: "Right Kicker (scoring)",
	51: "Left Star Rollover", 52: "Right Star Rollover",
}
# Printed "Not Used" on both the Switches parts list ("53-64 Not Used") and every one of the twelve
# matching cells of the Switch-Matrix Table.
UNUSED_MATRIX_ADDRESSES = frozenset(range(53, 65))
# Switch-Matrix Table wording where it differs from the parts list.
MATRIX_PAGE_WORDING = {
	10: "Ball Trough #3 (Upper Left)", 11: "Ball Trough #2 (Center)", 12: "Ball Trough #1 (Lower Right)",
	13: "Lower Left Stoplight Bank - Red Target", 14: "Lower Left Stoplight Bank - Yel Target",
	15: "Lower Left Stoplight Bank - Grn Target",
	17: "Upper Left Stoplight Bank - Red Target", 18: "Upper Left Stoplight Bank - Yel Target",
	19: "Upper Left Stoplight Bank - Grn Target",
	22: "Right Stoplight Bank - Red Target", 23: "Right Stoplight Bank - Yellow Target",
	24: "Right Stoplight Bank - Green Target",
	37: "Left Flipper Engine Revving (EOS)", 38: "Right Flipper Engine Revving (EOS)",
	49: "Left Kicker", 50: "Right Kicker",
}
SWITCH_PARTS = {
	1: "A-8476", 2: "B-6572", 3: "SW-1A-126", 4: "904845", 5: "904845", 6: "904845", 7: "904704",
	8: "5641-09369-00", 9: "17-1067", 10: "5647-09957-00", 11: "5647-09957-00", 12: "5647-09933-00",
	13: "A-11022", 14: "A-11054", 15: "A-11055", 16: "17-1012",
	17: "A-11022", 18: "A-11054", 19: "A-11055", 20: "SW-1A-124", 21: "SW-1A-124",
	22: "A-11022", 23: "A-11054", 24: "A-11055",
	25: "A-8253", 26: "A-8253", 27: "A-8253", 28: "A-8253", 29: "A-8253", 30: "A-8253",
	31: "SW-1A-124", 32: "SW-1A-124", 33: "A-7459-7", 34: "A-7459-7", 35: "A-7459-7",
	36: "SW-1A-138", 37: "SW-1A-150-1", 38: "SW-1A-150", 39: "A-11047", 40: "17-1085",
	41: "SW-1A-117", 42: "SW-1A-160", 43: "SW-1A-160", 44: "SW-1A-118", 45: "SW-1A-118",
	46: "SW-1A-118", 47: "A-11047", 48: "17-1085", 49: "SW-1A-122", 50: "SW-1A-122",
	51: "SW-1A-157", 52: "SW-1A-157",
}
# switch_type is set only where the printed part number identifies the construction. The 17-* and
# A-11047 assemblies are left without a type rather than guessed; see UNTYPED_SWITCH_NOTE.
SWITCH_TYPES = {
	1: "tilt", 2: "tilt", 3: "button", 4: "other", 5: "other", 6: "other", 7: "tilt", 8: "button",
	10: "microswitch", 11: "microswitch", 12: "microswitch",
	13: "leaf", 14: "leaf", 15: "leaf",
	17: "leaf", 18: "leaf", 19: "leaf", 20: "leaf", 21: "leaf",
	22: "leaf", 23: "leaf", 24: "leaf",
	25: "leaf", 26: "leaf", 27: "leaf", 28: "leaf", 29: "leaf", 30: "leaf",
	31: "leaf", 32: "leaf", 33: "leaf", 34: "leaf", 35: "leaf", 36: "leaf",
	37: "leaf", 38: "leaf", 41: "tilt", 42: "leaf", 43: "leaf",
	44: "leaf", 45: "leaf", 46: "leaf", 49: "leaf", 50: "leaf", 51: "leaf", 52: "leaf",
}
UNTYPED_SWITCH_ADDRESSES = (9, 16, 39, 40, 47, 48)
UNTYPED_SWITCH_NOTE = (
	" The Switches parts list prints only a part number for this position and never states the switch "
	"construction, so no switch_type is asserted here. It is certainly neither an opto nor a documented "
	"normally-closed contact: no row of that list carries an opto or photo-transistor part number, no row "
	"is printed blank, and neither copy of the Switch-Matrix Table carries an opto legend or a single "
	"shaded cell."
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
	-7: ("Advance (Diagnostic)", "service.advance"), -6: ("Up/Down (Diagnostic)", "service.updown"),
	-5: ("CPU Diagnostic (SW2)", "service.cpu-diag"), -4: ("Sound Diagnostic (SW1)", "service.sound-diag"),
}

# --- Solenoid table (public address = the manual's own Sol. No. for 1-22).
SOLENOID_LABELS = {
	1: "Outhole", 2: "Ball Release", 3: "Eject Hole", 4: "Police Light Relay",
	5: "Left Blue Playfield Flashers", 6: "Right Blue Playfield Flashers",
	7: "Left Hideout Coil", 8: "Right Hideout Coil",
	9: "Left Red Flashers", 10: "Insert Board Flashers", 11: "General Illumination Relay",
	12: "Right Red Flashers", 13: "Ramp Gates", 14: "Left Outlane Kickback", 15: "Knocker",
	16: "Coin-Lockout Relay",
	17: "Left Kicker", 18: "Right Kicker", 19: "Right Jet Bumper", 20: "Lower Left Jet Bumper",
	21: "Upper Left Jet Bumper", 22: "Top Playfield Flashers",
}
SOLENOID_TABLE_WORDING = {
	5: "Flasher No. 2 (Left Blue)", 6: "Flasher No. 3 (Right Blue)",
	7: "Left Hideout Relay", 8: "Right Hideout Relay",
	9: "Flasher No. 1 (Left Red)", 11: "General Illumination Relay",
	12: "Flasher No. 4 (Right Red)", 14: "Kickback (Left Outlane)",
}
SOLENOID_TYPE = {address: "Controlled" for address in range(1, 17)}
SOLENOID_TYPE.update({address: f"Special #{address - 16}" for address in range(17, 23)})
SOLENOID_WIRE = {
	1: "Gry-Brn", 2: "Gry-Red", 3: "Gry-Orn", 4: "Gry-Yel", 5: "Gry-Grn", 6: "Gry-Blu",
	7: "Gry-Vio", 8: "Gry-Blk", 9: "Brn-Blk", 10: "Brn-Red", 11: "Brn-Orn", 12: "Brn-Yel",
	13: "Brn-Grn", 14: "Brn-Blu", 15: "Brn-Vio", 16: "Brn-Gry",
	17: "Blu-Brn", 18: "Blu-Red", 19: "Blu-Orn", 20: "Blu-Yel", 21: "Blu-Grn", 22: "Blu-Blk",
}
SOLENOID_CPU = {
	1: "1P11-1", 2: "1P11-3", 3: "1P11-4", 4: "1P11-5", 5: "1P11-6", 6: "1P11-7", 7: "1P11-8",
	8: "1P11-9", 9: "1P12-1", 10: "1P12-2", 11: "1P12-4", 12: "1P12-5", 13: "1P12-6", 14: "1P12-7",
	15: "1P12-8", 16: "1P12-9",
	17: "1P19-7", 18: "1P19-4", 19: "1P19-3", 20: "1P19-6", 21: "1P19-8", 22: "1P19-9",
}
SOLENOID_POWER = {
	1: "8P3-1", 2: "8P3-2", 3: "8P3-3", 4: "Backbox", 5: "8P3-5", 6: "8P3-6", 7: "8P3-7", 8: "8P3-8",
	9: "8P3-9", 10: "9P1-7", 11: "3P7-1", 12: "8P3-12", 13: "8P3-13", 14: "8P3-14", 15: "Backbox",
	16: "7P1-7, 7P2-4",
	17: "8P3-17", 18: "8P3-18", 19: "8P3-19", 20: "8P3-20", 21: "8P3-21", 22: "8P3-22",
}
SOLENOID_DRIVER = {
	1: "Q33", 2: "Q25", 3: "Q32", 4: "Q24", 5: "Q31", 6: "Q23", 7: "Q30", 8: "Q22", 9: "Q17",
	10: "Q9", 11: "Q16", 12: "Q8", 13: "Q15", 14: "Q7", 15: "Q14", 16: "Q6",
	17: "Q75", 18: "Q71", 19: "Q73", 20: "Q69", 21: "Q77", 22: "Q79",
}
SOLENOID_PART = {
	1: "AE-23-800-01", 2: "AE-23-800-03", 3: "AE-23-800-03", 4: "5580-10883-00",
	5: "#63 flashlamps", 6: "#63 flashlamps", 7: "AE-24-900-02", 8: "AE-24-900-02",
	9: "#63 flashlamps", 10: "#63 flashlamps", 11: "5580-09555-00", 12: "#63 flashlamps",
	13: "AL-23-800-01", 14: "AE-24-900-01 & Relay", 15: "AE-23-800-02", 16: "404603-22",
	17: "AE-23-800-03", 18: "AE-23-800-03", 19: "AE-23-800-03", 20: "AE-23-800-03",
	21: "AE-23-800-03", 22: "#63 flashlamps",
}
SOLENOID_KIND = {
	1: "coil", 2: "coil", 3: "coil", 4: "relay", 5: "flasher", 6: "flasher", 7: "coil", 8: "coil",
	9: "flasher", 10: "flasher", 11: "gi", 12: "flasher", 13: "coil", 14: "coil", 15: "coil",
	16: "relay", 17: "coil", 18: "coil", 19: "coil", 20: "coil", 21: "coil", 22: "flasher",
}
# sxx.ssSw for hsGameData: {49,50,35,34,33,0} at src/wpc/s11games.c line 143. The VBLANK loop at
# src/wpc/s11.c lines 191-200 indexes CORE_FIRSTSSSOL+ii with ii = 0..5 against ssSw[ii], so the
# mapping is sequential: public 17 <- switch 49, 18 <- 50, 19 <- 35, 20 <- 34, 21 <- 33, 22 <- none.
SPECIAL_SOLENOID_SWITCH = {17: 49, 18: 50, 19: 35, 20: 34, 21: 33, 22: 0}
# Retained known-working VPX script callbacks, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "bsTrough.SolIn", 2: "bstrough.SolOut", 3: "bsSaucer.SolOut",
	5: "SetLamp 105 (four F105* glow lights)", 6: "SetLamp 106 (four F106* glow lights)",
	7: "bsLeftLock.SolOut (commented 'Left Hideout Eject')",
	8: "bsRightLock.SolOut (commented 'Right Hideout Eject')",
	9: "SetLamp 109 (two Flupper flasher assemblies)", 11: "PFGI",
	12: "SetLamp 112 (two Flupper flasher assemblies)", 13: "Divert", 14: "SolKickback",
	15: 'vpmSolSound SoundFX("Knocker",DOFKnocker)', 22: "SetLamp 122 (two Flupper flasher assemblies)",
}

VIRTUAL_SOLENOID_LABELS = {
	23: "PinMAME Flipper/Switched-Solenoid Enable State", 24: "Unassigned Solenoid Slot 24",
	25: "Unpopulated A/C Mux C-Side Slot 25", 26: "Unpopulated A/C Mux C-Side Slot 26",
	27: "Unpopulated A/C Mux C-Side Slot 27", 28: "Unpopulated A/C Mux C-Side Slot 28",
	29: "Unpopulated A/C Mux C-Side Slot 29", 30: "Unpopulated A/C Mux C-Side Slot 30",
	31: "Unpopulated A/C Mux C-Side Slot 31", 32: "Unpopulated A/C Mux C-Side Slot 32",
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
		"PinMAME's CORE_SSFLIPENSOL / S11_GAMEONSOL (src/wpc/s11.h S11_GAMEONSOL 23): the 'flipper and "
		"switched-solenoid enable' state, set from PIA0 CB2 in pia0cb2_w and used to gate both the six "
		"special solenoids and the synthetic flipper outputs 45-48. It has no driver transistor and no "
		"Sol. No. of its own in the manual, but it is not fictional: the Solenoid Table's three flipper "
		"rows take their CPU-board feed from 1P19-1 and 1P19-2, on the same special-solenoid connector "
		"this enable controls, which is why disabling it disables the flippers on real hardware. The "
		"retained script binds SolCallback(23) to FastFlips.TiltSol on pre-3.57 VPinMAME only."
	),
	24: (
		"Unassigned platform gap between the special-solenoid enable (23) and the A/C-relay-multiplexed "
		"'C'-side alias bank (25-32). No known driver populates this address."
	),
	33: (
		"Platform generic upper-flipper-coil address (CORE_FIRSTUFLIPSOL = 33). hsGameData's hw.flippers "
		"is FLIP_SWNO(37,38), which sets FLIP_SW(FLIP_L) only and no FLIP_SW/FLIP_SOL bit for either "
		"upper position, and core_getSol serves 33-36 only for GEN_ALLWPC/GEN_SAM, so this address reads "
		"as always zero. High Speed does have a third, upper-right flipper coil, but the manual gives it "
		"no Sol. No. at all and PinMAME never publishes it here; see conflict.upper-flipper-driving-button."
	),
	45: (
		"PinMAME's synthetic lower-right-flipper power output (CORE_FIRSTLFLIPSOL = 45). hsGameData "
		"declares FLIP_SWNO(37,38) with no FLIP_SOL bit, so core_updateSw's 'fake solenoids if not CPU "
		"controlled' branch fabricates 45-48 from live flipper-button state, gated by the same ssEn the "
		"driver passes in (src/wpc/s11.c core_updateSw(locals.ssEn)). The manual confirms there is no "
		"driver-board output behind them: its three flipper rows carry no Sol. No. and no driver "
		"transistor, and note 1 says the CPU-board wire runs to the flipper switch rather than to the "
		"coil. The retained script binds SolCallback(sLRFlipper) = SolRFlipper, which rotates both the "
		"lower-right flipper and the upper-right flipper together."
	),
	49: (
		"Platform-wide simulator-only fake solenoid for the ball shooter (CORE_FIRSTSIMSOL = 49); not "
		"System-11-specific and not a High Speed hardware output."
	),
	50: (
		"Unassigned platform gap between the simulator slot (49) and the custom-solenoid base (51). "
		"hsGameData declares no custSol, so MACHINE_INIT(s11) sizes coreGlobals.nSolenoids as "
		"CORE_FIRSTCUSTSOL-1+0 = 50 and addresses 51 and above are not modelled at all for this game."
	),
}
MUX_SLOT_NOTE = (
	"Platform 'C'-side alias of solenoid {a_address} under the A/C select relay. High Speed has no A/C "
	"select relay: hsGameData sets sxx.muxSol = 0 (src/wpc/s11games.c line 143, the fourth INITGAMEFULL "
	"argument), so updsol()'s mux copy branch never runs and bits 24-31 of the solenoid word are never "
	"written. MACHINE_INIT(s11)'s hs_ block likewise sets no output type at or above address 25, unlike "
	"the many System 11B blocks that declare eight muxed flasher outputs there. The manual agrees from "
	"the other side: its Solenoid Table has no A/C column, no 'nnA'/'nnC' circuit pairs, and no relay "
	"row other than the police light, GI and coin lockout. Unpopulated on this machine."
)
OVERLAY_SLOT_NOTE = (
	"Outer bound of the platform's 'Sound overlay board' address range (37-44 per src/wpc/core.h's own "
	"doc comment and core_getSol's GEN_ALLS11 branch). High Speed declares no sound-overlay board: the "
	"seventh INITGAMEFULL argument that becomes hw.gameSpecific1 is 0, so S11_SNDOVERLAY is unset and "
	"pia5cb2_w never diverts the sound byte to a solenoid pattern. Unpopulated on this machine."
)
UPPER_FLIPPER_SLOT_NOTE = "Platform generic upper-flipper-coil address; unused, see address 33."
SYNTHETIC_FLIPPER_SLOT_NOTE = {
	46: "PinMAME's synthetic lower-right-flipper hold output; see address 45.",
	47: (
		"PinMAME's synthetic lower-left-flipper power output; see address 45. Its button is matrix switch "
		"37 (FLIP_SWL of FLIP_SWNO(37,38)); the retained script binds SolCallback(sLLFlipper) = "
		"SolLFlipper."
	),
	48: "PinMAME's synthetic lower-left-flipper hold output; see address 47.",
}

# --- Lamp matrix (public address = (column-1)*8+row). Labels of record from the Lamps list
# (printed page 33); Lamp-Matrix Table wording kept where it differs.
LAMP_LABELS = {
	1: "Game Over", 2: "Match", 3: "Shoot Again / Drive Again",
	4: "Left Outlane Special", 5: "Right Outlane Special", 6: "Ball In Play",
	7: "Left Spinner 1000 Arrow", 8: "Right Spinner 1000 Arrow",
	9: "20,000 Light Kickback", 10: "Center Spinner 1000 Arrow",
	11: "Extra Ball (Eject Hole)", 12: "Escape (Eject Hole)",
	13: "Red Light (Lower Left Target Bank)", 14: "Yellow Light (Lower Left Target Bank)",
	15: "Green Light (Lower Left Target Bank)", 16: "Kickback Arrow (Left Outlane)",
	17: "Red Light (Upper Left Target Bank)", 18: "Yellow Light (Upper Left Target Bank)",
	19: "Green Light (Upper Left Target Bank)",
	20: "Left Freeway Arrow", 21: "Right Freeway Arrow",
	22: "Red Light (Right Target Bank)", 23: "Yellow Light (Right Target Bank)",
	24: "Green Light (Right Target Bank)",
	25: "Standup Target Arrow 1", 26: "Standup Target Arrow 2", 27: "Standup Target Arrow 3",
	28: "Standup Target Arrow 4", 29: "Standup Target Arrow 5", 30: "Standup Target Arrow 6",
	31: "Freeway Scores 25,000", 32: "Freeway Scores 50,000", 33: "Freeway Scores 75,000",
	34: "Freeway Scores 100,000", 35: "Freeway Lights Extra Ball",
	36: "Ramp Earns Bonus X", 37: "Ramp Earns Ramp Bonus", 38: "Ramp Earns Getaway",
	39: "Ramp Earns Hideout", 40: "Ramp Earns Hideout Jackpot",
	41: "Stoplights Light Escape (Center)",
	42: "Red Light (Ramp Stoplight)", 43: "Yellow Light (Ramp Stoplight)",
	44: "Green Light (Ramp Stoplight)",
	45: "Bonus 1000", 46: "Bonus 2000", 47: "Bonus 3000", 48: "Bonus 4000", 49: "Bonus 5000",
	50: "Bonus 6000", 51: "Bonus 7000", 52: "Bonus 8000", 53: "Bonus 9000", 54: "Bonus 10,000",
	55: "Bonus 20,000", 56: "Bonus 30,000", 57: "Bonus 40,000", 58: "Bonus 50,000",
	59: "Bonus 60,000", 60: "Bonus 5X", 61: "Bonus 4X", 62: "Hold Bonus", 63: "Bonus 3X",
	64: "Bonus 2X",
}
LAMP_MATRIX_PAGE_WORDING = {
	9: "Flipper Return Lanes", 3: "Shoot Again - Drive Again",
	13: "Lower Left Target Bank - Red Light", 14: "Lower Left Target Bank - Yellow Light",
	15: "Lower Left Target Bank - Green Light",
	17: "Upper Left Target Bank - Red Light", 18: "Upper Left Target Bank - Yellow Light",
	19: "Upper Left Target Bank - Green Light",
	22: "Right Target Bank - Red Light", 23: "Right Target Bank - Yellow Light",
	24: "Right Target Bank - Green Light",
	42: "Ramp Stoplight Red Light", 43: "Ramp Stoplight Yellow Light",
	44: "Ramp Stoplight Green Light",
}
# The Lamp-Matrix Table's boxed "[2] Two lamps in circuit" marker, swept across all 64 cells of the
# rendered page, appears on these four addresses.
TWO_BULB_LAMPS = frozenset({1, 3, 9, 40})
# The Lamps list marks these locations "(Backglass)". Lamp 3's circuit has one backglass bulb and one
# playfield bulb, so it is not in this set.
BACKGLASS_ONLY_LAMPS = frozenset({1, 2, 6})
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

# --- Normalized playfield coordinates, x/952 and y/1974, derived from the retained VPX extraction.
# The full object-by-object derivation is in review-artifacts/high-speed-1986/vpx-geometry.txt.
SWITCH_POSITIONS = {
	9: [(0.449580, 0.960993)],
	10: [(0.872195, 0.853659)], 11: [(0.872195, 0.853659)], 12: [(0.872195, 0.853659)],
	13: [(0.292367, 0.308892)], 14: [(0.277116, 0.339825)], 15: [(0.263007, 0.369044)],
	16: [(0.781537, 0.113455)],
	17: [(0.292621, 0.118656)], 18: [(0.292136, 0.147283)], 19: [(0.291747, 0.176519)],
	20: [(0.124983, 0.711203)], 21: [(0.783734, 0.709515)],
	22: [(0.457515, 0.243723)], 23: [(0.511726, 0.257873)], 24: [(0.563604, 0.270992)],
	25: [(0.109453, 0.555279)], 26: [(0.127470, 0.531263)], 27: [(0.146144, 0.507180)],
	28: [(0.786354, 0.522468)], 29: [(0.805941, 0.548122)], 30: [(0.825284, 0.573111)],
	31: [(0.054186, 0.785593)], 32: [(0.851563, 0.733872)],
	33: [(0.465887, 0.102360)], 34: [(0.495917, 0.201653)], 35: [(0.655096, 0.138951)],
	36: [(0.948380, 0.875271)],
	37: [(0.288241, 0.829684)], 38: [(0.623109, 0.829684)],
	39: [(0.052875, 0.389543)], 40: [(0.054186, 0.425195)],
	42: [(0.405369, 0.020317)], 43: [(0.549315, 0.022516)],
	44: [(0.099823, 0.236832)], 45: [(0.735100, 0.216918)], 46: [(0.897385, 0.180465)],
	47: [(0.934141, 0.387710)], 48: [(0.947405, 0.423246)],
	49: [(0.212637, 0.704064)], 50: [(0.694870, 0.703124)],
	51: [(0.089693, 0.072122)], 52: [(0.930546, 0.071980)],
}
SWITCH_PROJECTIONS = {
	9: (
		"Projected onto the Drain kicker (Kicker.Drain, table object centre): the outhole switch has no "
		"dedicated VPX object because the retained script's cvpmBallStack helper manages it abstractly "
		"(bsTrough.InitSw 9,12,11,10) and Drain_Hit is what feeds the stack. The manual's own "
		"switch-locations drawing puts switch 9 at the left end of the outhole/trough tube."
	),
	10: (
		"Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre): the three trough "
		"positions have no individual VPX objects, the retained script managing all four trough switches "
		"through one cvpmBallStack against the single BallRelease exit kicker "
		"(bsTrough.InitKick BallRelease,90,10)."
	),
	11: "Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre); see switch 10.",
	12: "Projected onto the BallRelease kicker (Kicker.BallRelease, table object centre); see switch 10.",
	37: (
		"Projected onto the left flipper's own assembly (Flipper.LeftFlipper, table object centre). The "
		"Lane Change switch is item 2b of the C-9952-R Flipper Base/Lane Change Assembly, mounted below "
		"the playfield as part of that assembly, and the manual's own switch-locations drawing places "
		"callout 37 at the left flipper. The retained script never drives this address: pinned PinMAME "
		"fabricates it from live flipper-button state in core_updateSw."
	),
	38: (
		"Projected onto the right flipper's own assembly (Flipper.RightFlipper, table object centre); see "
		"switch 37, with callout 38 at the right flipper."
	),
	39: (
		"Taken from the retained table's Trigger.sw39, an object with no _Hit handler anywhere in the "
		"script. It is used rather than discarded because three things agree: its name matches this "
		"address, it sits directly above Kicker.LKick which the script does bind to switch 40 "
		"(bsLeftLock.InitSaucer LKick,40), and the manual's own switch-locations drawing draws callout 39 "
		"above callout 40 in the same left ball chute."
	),
	47: (
		"Taken from the retained table's Trigger.sw37, whose name is a misnomer -- switch 37 is the left "
		"flipper's Lane Change switch at the bottom of the playfield, and this object sits high on the "
		"right side. It is the exact mirror of Trigger.sw39: it lies directly above Kicker.RKick, which "
		"the script binds to switch 48 (bsRightLock.InitSaucer RKick,48), and the manual draws callout 47 "
		"above callout 48 in the right ball chute. The coordinate is therefore derived from the mirror "
		"geometry of the right hideout lane plus the manual's own ordering, not from the object's name."
	),
	49: (
		"Kicker (slingshot) scoring switch, projected onto the centroid of its own slingshot wall's four "
		"drag points (Wall.LeftSlingShot), the assembly the switch is part of; the script's "
		"LeftSlingShot_Slingshot handler is what pulses this address."
	),
	50: (
		"Kicker (slingshot) scoring switch, projected onto the centroid of Wall.RightSlingShot's four drag "
		"points; see switch 49."
	),
}
SOLENOID_POSITIONS = {
	1: [(0.449580, 0.960993)], 2: [(0.872195, 0.853659)], 3: [(0.781537, 0.113455)],
	5: [(0.290704, 0.490248)], 6: [(0.618567, 0.491356)],
	7: [(0.054186, 0.425195)], 8: [(0.947405, 0.423246)],
	9: [(0.115550, 0.450855), (0.036569, 0.564326)],
	12: [(0.871876, 0.429466), (0.950630, 0.254143)],
	13: [(0.500308, 0.016624)], 14: [(0.050625, 0.879699)],
	17: [(0.212637, 0.704064)], 18: [(0.694870, 0.703124)],
	19: [(0.655096, 0.138951)], 20: [(0.495917, 0.201653)], 21: [(0.465887, 0.102360)],
	22: [(0.324930, 0.038501), (0.911339, 0.000558)],
}
SOLENOID_PROJECTIONS = {
	1: (
		"Projected onto the Drain kicker (Kicker.Drain, table object centre): the outhole kicker coil has "
		"no separate actuator object, the retained script routing it through bsTrough.SolIn."
	),
	3: (
		"Projected onto the eject-hole saucer's own kicker object (Kicker.sw16, table object centre), the "
		"object the retained script initialises as the saucer (bsSaucer.InitSaucer sw16,16,96,5)."
	),
	5: (
		"Placed at the centre of the single elongated flasher lens the manual's own solenoid-locations "
		"drawing gives item 5, taken from Light.F105. The retained table models that lens with three "
		"lights: a co-located bulb/glow pair (F105/F105b) at the centre plus F105c and F105d offset about "
		"(43.5, -28.5) either side of it. Because the manual draws one lens with one leader line, this is "
		"one device location, not three."
	),
	6: "Placed at the centre of item 6's elongated lens (Light.F106); see solenoid 5 for the derivation.",
	7: (
		"Projected onto the left hideout's own kicker object (Kicker.LKick, table object centre), the "
		"object the retained script binds to switch 40 and ejects with bsLeftLock.SolOut."
	),
	8: "Projected onto the right hideout's own kicker object (Kicker.RKick, table object centre); see solenoid 7.",
	13: (
		"Projected onto the retained table's left ramp-gate object (Wall.Diverter1, four-drag-point "
		"centroid). The manual's Ramp Gate Assembly D-10884 parts list has one coil, one drive arm, one "
		"drive link and one gate (C-10888), and the assembly appears once in the Playfield Parts list, so "
		"there is one physical gate; the retained table splits it into two gate objects that its single "
		"Divert handler moves together, the second at normalized (0.666716, 0.017356). The left object is "
		"used as the anchor."
	),
	14: (
		"Projected onto the left outlane kickback's own plunger object (Plunger.Plunger1, table object "
		"position), which the retained script's SolKickback handler fires."
	),
	17: (
		"Projected onto the centroid of its own slingshot wall's four drag points (Wall.LeftSlingShot); "
		"the kicker coil and its scoring switch 49 are the same assembly."
	),
	18: "Projected onto the centroid of Wall.RightSlingShot's four drag points; see solenoid 17.",
	22: (
		"Placed at the two Light members of the two Flupper flasher assemblies the retained script drives "
		"for this address (Light.Flasherlight5 and Light.Flasherlight6). Their dome base and lit "
		"primitives (Flasherbase5/6, Flasherlit5/6) are parked off-table at raw x about -2000, so only "
		"the lights carry usable coordinates; both sit along the top edge of the playfield, matching the "
		"manual's own item-22 callout to a slot along the top edge."
	),
}
LAMP_POSITIONS = {
	3: [(0.453354, 0.869241)], 4: [(0.055231, 0.695098)], 5: [(0.851047, 0.693584)],
	7: [(0.122946, 0.287022)], 8: [(0.879025, 0.216913)],
	9: [(0.125153, 0.659865), (0.781415, 0.658995)],
	10: [(0.725286, 0.251208)], 11: [(0.696858, 0.295986)], 12: [(0.672499, 0.341875)],
	13: [(0.350070, 0.318255)], 14: [(0.335848, 0.347323)], 15: [(0.322508, 0.376400)],
	16: [(0.055350, 0.747473)],
	17: [(0.358067, 0.119382)], 18: [(0.358417, 0.150575)], 19: [(0.358028, 0.180234)],
	20: [(0.153477, 0.344954)], 21: [(0.845178, 0.274459)],
	22: [(0.430989, 0.272411)], 23: [(0.485603, 0.286559)], 24: [(0.538681, 0.300464)],
	25: [(0.164811, 0.588064)], 26: [(0.178899, 0.564525)], 27: [(0.194468, 0.541106)],
	28: [(0.735348, 0.555993)], 29: [(0.751663, 0.580309)], 30: [(0.766700, 0.603344)],
	31: [(0.300588, 0.759766)], 32: [(0.376927, 0.773510)], 33: [(0.454395, 0.777487)],
	34: [(0.534202, 0.772916)], 35: [(0.607701, 0.759378)],
	36: [(0.765267, 0.467183)], 37: [(0.696425, 0.438222)], 38: [(0.620822, 0.404167)],
	39: [(0.550377, 0.373346)], 40: [(0.467318, 0.338833)], 41: [(0.453519, 0.618274)],
	45: [(0.278170, 0.670528)], 46: [(0.247755, 0.641320)], 47: [(0.235459, 0.608673)],
	48: [(0.248903, 0.576756)], 49: [(0.279222, 0.547755)], 50: [(0.326838, 0.524488)],
	51: [(0.387441, 0.509903)], 52: [(0.453185, 0.505954)], 53: [(0.521768, 0.510321)],
	54: [(0.583027, 0.523493)], 55: [(0.632781, 0.547011)], 56: [(0.660767, 0.576700)],
	57: [(0.670071, 0.608383)], 58: [(0.661313, 0.641411)], 59: [(0.632681, 0.671319)],
	60: [(0.599612, 0.706766)], 61: [(0.529745, 0.722432)], 62: [(0.454044, 0.723433)],
	63: [(0.376786, 0.722476)], 64: [(0.306184, 0.705110)],
}
# Lamp addresses with a real bulb per the manual but no derivable playfield coordinate.
UNPLACED_LAMPS = (42, 43, 44)
UNPLACED_LAMP_NOTE = (
	" The three Ramp Stoplight bulbs live in the playfield Traffic Light Assembly (B-10921, item 9 of the "
	"Playfield Parts list), but no playfield coordinate for it can be derived from the retained "
	"extraction. UpdateLamps drives this address as NFadeL against a Light object parked at raw x about "
	"-2237, far off-table, and the commented-out alternative in the same routine addressed "
	"Primitive.stoplight_prim, which sits at position (0,0,0) with an all-zero rot_and_tra and its "
	"geometry baked into mesh hslight.ob; deriving that mesh's centroid through the table's own "
	"position-plus-size convention puts it at raw y about -499, also off-table. Two independent object "
	"families therefore agree the coordinate is absent, so the spatial key is omitted rather than "
	"invented. See coverage.missing spatial_placement."
)


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"High Speed retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained High Speed extraction")
		return None
	return Path(value).expanduser().resolve()


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	return manifest_path


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"High Speed retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"High Speed retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	if len(files) != EXTRACTION_FILE_COUNT:
		raise RuntimeError(f"High Speed retained extraction file count mismatch: files={len(files)}, expected={EXTRACTION_FILE_COUNT}")
	return actual


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*source_refs: str) -> dict[str, Any]:
	return {"status": "validated", "source_refs": list(source_refs)}


def located(identifier: str, role: str, positions: list[tuple[float, float]], *source_refs: str) -> dict[str, Any]:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield",
			"x": round(x, 6), "y": round(y, 6), "provenance": provenance(*source_refs),
		})
	return {"status": "validated", "placements": placements}


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


def source_records() -> list[dict[str, Any]]:
	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION, "locator": "Pinned catalog driver records for the hs_* clone tree",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/s11games.c line 38 INITGAMEFULL macro definition and line 143 "
				"INITGAMEFULL(hs,GEN_S11X,s11_dispS11,0,FLIP_SWNO(37,38),S11_BCDDIAG,0,0,0,49,50,35,34,33,0), "
				"expanding to hsGameData = {GEN_S11X, s11_dispS11, {FLIP_SWNO(37,38),0,0,0,0,S11_BCDDIAG,0,0}, "
				"NULL, {{0}}, {0,{49,50,35,34,33,0}}} -- so hw.swCol/lampCol/custSol/soundBoard are 0, "
				"hw.display = S11_BCDDIAG, hw.gameSpecific1 = hw.gameSpecific2 = 0, the whole wpc struct "
				"(including wpc.invSw) is zero-initialised, sxx.muxSol = 0 and sxx.ssSw = {49,50,35,34,33,0}; "
				"CORE_GAMEDEF(hs,l4)/CORE_CLONEDEF for hs_l3/hs_l1/hs_p4g/hs_l4c, input_ports_hs = "
				"input_ports_s11; src/wpc/s11.c lines 191-200 (the ssEn VBLANK loop that drives "
				"CORE_FIRSTSSSOL+ii from core_getSw(sxx.ssSw[ii]) for ii = 0..5), setSSSol/ssSolNo PIA-to-address "
				"table, pia0cb2_w (locals.ssEn, S11_GAMEONSOL), updsol (the sxx.muxSol-gated 'C'-side copy that "
				"never runs here), pia0b_w/latch2200/pia1a_w/pia1b_w/pia2a_r/pia5cb2_w, s11_readmem/s11_writemem, "
				"core_updateSw(locals.ssEn) at line 358, MACHINE_INIT(s11) coreGlobals.nLamps/nSolenoids sizing "
				"and the per-game hs_ output-type block at lines 1011-1018 (addresses 4, 5-6, 9-10, 11, 12, 22); "
				"src/wpc/s11.h S11_BCDDIAG/S11_BCDDISP/S11_LOWALPHA/S11_DISPINV display flags, "
				"S11_MUXSW2/S11_SNDOVERLAY/S11_RKMUX/S11_MUXDELAY gameSpecific1 flags, S11_GAMEONSOL = 23, "
				"S11_SWADVANCE/S11_SWUPDN/S11_SWCPUDIAG/S11_SWSOUNDDIAG, S11_COMINPORT/S11_COMPORTS, "
				"COREPORT_DIPNAME Country jumper; src/wpc/s11.c lines 61-65 core_tLCDLayout s11_dispS11; "
				"src/wpc/core.h core_tGameData field order (hw, wpc.invSw, sxx.muxSol, sxx.ssSw), "
				"FLIP_SWNO/FLIP_SWL/FLIP_SWR/FLIP_SW/FLIP_SOL macros, CORE_FIRSTSSSOL = 17, "
				"CORE_SSFLIPENSOL = 23, CORE_FIRSTUFLIPSOL = 33, CORE_FIRSTEXTSOL = 37, "
				"CORE_FIRSTLFLIPSOL = 45, CORE_FIRSTSIMSOL = 49, CORE_FIRSTCUSTSOL = 51, CORE_MAXSOL = 64, "
				"DISP_SEG_7/DISP_SEG_16 layout macros, CORE_SEG16/CORE_SEG8/CORE_SEG7S; src/wpc/core.c "
				"core_swSeq2m/core_m2swSeq/core_getSw/core_setSw, core_updateSw synthetic-flipper-solenoid "
				"fallback, core_getSol GEN_ALLS11 branch, MACHINE_DRIVER_START(PinMAME) "
				"MDRV_SWITCH_CONV/MDRV_LAMP_CONV; src/wpc/gen.h GEN_S11X; src/libpinmame/libpinmame.h "
				"PINMAME_HARDWARE_GEN_S11X"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/system-11.json",
			"revision": "repository",
			"locator": (
				"System 11 public switch/lamp sequential column-major 1-64 numbering, the four negative "
				"diagnostic addresses, the single Country jumper, and the solenoid address rules for the "
				"switched/controlled/special banks, the S11_GAMEONSOL enable, the A/C mux alias bank, the "
				"sound-overlay range, the synthetic flipper outputs and the custom-solenoid base"
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE, "kind": "manual",
			"uri": (
				"external:pinmame-manuals/by-machine/williams.high-speed.1986/"
				"archive-williams-high-speed-instruction-manual/high_speed_instruction_manual.pdf"
			),
			"original_filename": "high_speed_instruction_manual.pdf", "sha256": MANUAL_SHA256,
			"locator": (
				"92-page scan of the Williams High Speed Instruction Manual (title page dated February 24, 1986; "
				"inner title page 16-541-101, January 28, 1986) with an Acrobat Paper-Capture OCR text layer. "
				"For Sections 1 and 2, printed page = PDF page - 8, verified against the printed footers. The "
				"copy is rebound and partly out of order: PDF page 4 is an unpaginated quick-reference foldout "
				"carrying both the Switch-Matrix Table and the Lamp-Matrix Table; PDF 34 repeats the "
				"Switch-Matrix Table at printed page 26; PDF 33 is the Solenoid Table at printed page 25; "
				"PDF 40/41/42 are the Switches, Lamps and Solenoids/Flashers parts lists at printed 32/33/34; "
				"PDF 43-47 are the mechanism assembly pages at printed 35-39; PDF 49 is the Master Display "
				"Board at printed 41; PDF 55-58 are the four-page Amendments sheet in reverse order (PDF 58 is "
				"Amendment Page 1); PDF 59 duplicates the Solenoid Table beside the ROM Summary; PDF 81 is the "
				"Power Wiring Diagram at printed page 47."
			),
			"license": "NOASSERTION",
			"attribution": "Williams Electronics, Inc.; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.high-speed.switch-matrix",
					"locator": "PDF page 4 (unpaginated quick-reference foldout) and PDF page 34 (printed page 26), HIGH SPEED Switch-Matrix Table",
					"path": "evidence/excerpts/williams.high-speed.1986/switch-matrix.md",
					"sha256": "d6936ce37f54a1e7aebdd353b35f9b0421a0a3557b5766f15e7bb878efe19d5c",
					"image": "evidence/excerpts/williams.high-speed.1986/switch-matrix.webp",
					"image_sha256": "a43cd1b076716545fe8b53d37036c5b8cae63124cef8d4ad02acf68e7d64c1fa",
					"image_derivation": (
						"high_speed_instruction_manual.pdf page 4, crop box 0.155,0.118,0.89,0.425 of the page, "
						"rendered at 300 dpi with pdftoppm, reduced to 1300px wide grayscale, quality 60 WebP"
					),
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.switch-locations",
					"locator": "PDF page 40, printed page 32, Switches parts list and numbered switch-locations drawing",
					"path": "evidence/excerpts/williams.high-speed.1986/switch-locations.md",
					"sha256": "e6a898af8284af9f4db709b0703b72fb7d5fdd41b3e2d39b9e0bab6a60187a0b",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.lamp-matrix",
					"locator": "PDF page 4 (unpaginated quick-reference foldout), HIGH SPEED Lamp-Matrix Table with its two-lamps-in-circuit legend",
					"path": "evidence/excerpts/williams.high-speed.1986/lamp-matrix.md",
					"sha256": "1467c109cb15bc6414f7fcc333f2f62db5564a8e3af9a261c91fb89b630688ad",
					"image": "evidence/excerpts/williams.high-speed.1986/lamp-matrix.webp",
					"image_sha256": "1c41dfc629c5adc2c5e7c11f35367c33a8e873d5c14e3e5f72ca66849e7fee34",
					"image_derivation": (
						"high_speed_instruction_manual.pdf page 4, crop box 0.163,0.583,0.90,0.898 of the page, "
						"rendered at 300 dpi with pdftoppm, reduced to 1240px wide grayscale, quality 58 WebP"
					),
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.lamp-locations",
					"locator": "PDF page 41, printed page 33, Lamps list",
					"path": "evidence/excerpts/williams.high-speed.1986/lamp-locations.md",
					"sha256": "e1445fb3a4a43b1a83962f34806288ce2a9449e9970bd56b2b718a045ee2604c",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.solenoid-table",
					"locator": "PDF page 33, printed page 25, HIGH SPEED Solenoid Table and SOLENOID TEST text",
					"path": "evidence/excerpts/williams.high-speed.1986/solenoid-table.md",
					"sha256": "d0acbd7c48baacccb0e23d1fccff7a921092a6f390afb40bf8c71731fc1b6e4e",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.solenoid-flasher-locations",
					"locator": "PDF page 42, printed page 34, Solenoids/Flashers and Rubber Parts lists with the numbered locations drawing",
					"path": "evidence/excerpts/williams.high-speed.1986/solenoid-flasher-locations.md",
					"sha256": "16e6a560409d220cad6cec815fefd5ba8d8e21a0db53c87594d7ecdd8fd973ff",
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.general-illumination",
					"locator": "PDF page 81, printed page 47, Power Wiring Diagram: the general-illumination relay contacts and the 3P8 lamp-string fan-out",
					"path": "evidence/excerpts/williams.high-speed.1986/general-illumination.md",
					"sha256": "b327cc5d0b93b253866dcb55a90811e8e321008d34fa8967be9502b173d0b74a",
					"image": "evidence/excerpts/williams.high-speed.1986/general-illumination.webp",
					"image_sha256": "937dedf826a1e31813642aa7c0f8ccb249592193a7caeb59e560152ffc477517",
					"image_derivation": (
						"high_speed_instruction_manual.pdf page 81, crop box 0.09,0.44,0.99,0.665 of the page, "
						"rendered at 300 dpi with pdftoppm, reduced to 1300px wide grayscale, quality 62 WebP"
					),
					"method": "manual", "transcribed_by": "curator, read from the rendered page", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.boards-and-assemblies",
					"locator": "PDF pages 10, 39, 43, 44, 45, 46, 47 and 49 (printed pages 2, 31, 35, 36, 37, 38, 39 and 41), board list, Playfield Parts and the mechanism assembly pages",
					"path": "evidence/excerpts/williams.high-speed.1986/boards-and-assemblies.md",
					"sha256": "2ef9071abb55a4098ac2406528e649a7e8bcc24568783b33aaef5929b2d6d95e",
					"method": "manual", "transcribed_by": "curator, read from the rendered pages", "reviewed": True,
				},
				{
					"id": "excerpt.high-speed.diagnostics-and-amendments",
					"locator": "PDF pages 31 and 35 (printed pages 23 and 27) and PDF pages 55-58 (the Amendments and Additions sheet, dated 040286)",
					"path": "evidence/excerpts/williams.high-speed.1986/diagnostics-and-amendments.md",
					"sha256": "9fe622d4650933cb6dbbba52a87d68facc5668524e7969729c6708a92c3ced51",
					"method": "manual", "transcribed_by": "curator, read from the rendered pages", "reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE, "kind": "human_review",
			"uri": "external:pinmame-review-artifacts/high-speed-1986/manual-transcription.md", "revision": "2026-08-08",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained reading log for the manual: the verified printed-to-PDF page offset, the out-of-order "
				"sheets in this rebound copy, which page settled which fact, and the list of questions the "
				"manual does not answer."
			),
			"license": "NOASSERTION", "attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/high-speed-1986/source/High%20Speed%20%28Williams%201986%29.vpx",
			"original_filename": "High Speed (Williams 1986).vpx", "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working VPX recreation of the physical machine (table_version 2.0, "
				f"author_name 32assassin, release_date 1-12-2017 per info.json). Exact playfield bounds are "
				f"{TABLE_BOUNDS}; normalized coordinates are x/952 and y/1974. Geometry authority only for "
				"named table objects, and only where the manual's own numbered locations drawings agree."
			),
			"license": "NOASSERTION", "attribution": "32assassin", "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/williams/high-speed-1986/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				'Retained embedded script (92,314 bytes). Runtime and mechanism-causality authority: cGameName = '
				'"hs_l4", UseLamps = 0 with an explicit UpdateLamps routine (so lamp bindings come from that '
				"routine and not from object-name patterns), UseGI = 0 with an explicit PFGI routine, the "
				"SolCallback table for solenoids 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 22, 23 and "
				"sLRFlipper/sLLFlipper, the cvpmBallStack helpers for the trough, the eject-hole saucer and the "
				"two hideouts, and the Controller.Switch/vpmTimer.PulseSw switch semantics for the lanes, "
				"targets, bumpers, spinners and slingshots. Full object-by-object cross-reference in "
				"external:pinmame-review-artifacts/high-speed-1986/vpx-geometry.txt."
			),
			"license": "NOASSERTION", "attribution": "32assassin", "rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/williams/high-speed-1986/extracted-vpxtool/",
			"locator": (
				f"Retained vpxtool extraction, {EXTRACTION_FILE_COUNT} files, produced from the retained table "
				f"with vpxtool git:v0.33.3. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	]


def _switch_wiring(column: int, row: int) -> dict[str, Any]:
	drive_wire, drive_connection, drive_component = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection = SWITCH_ROW_WIRING[row]
	return {
		"board": "System 11 CPU board", "drive_wire": drive_wire, "drive_connection": drive_connection,
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
					"location": "coin door and CPU board diagnostic switches",
					"switch_type": "button",
					"notes": (
						"System 11 diagnostic input, the upper nibble of the shared S11_COMINPORT keyboard port "
						"(core_swSeq2m maps public n to internal matrix index n+7, so these four land in column 0). "
						"The manual's Test/Diagnostic Procedures section drives the whole test sequence from the "
						"coin-door ADVANCE button and AUTO-UP/MANUAL-DOWN switch and names the CPU board's own SW1 "
						"as the Sound Diagnostic switch and SW2 as the CPU Diagnostic switch."
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
		if not unused:
			physical["part_number"] = SWITCH_PARTS[address]
		if address in SWITCH_TYPES:
			physical["switch_type"] = SWITCH_TYPES[address]
		notes = f"Printed switch-matrix drive column {column}, return row {row}."
		if unused:
			notes += (
				" The Switches parts list prints one collapsed row, \"53-64 Not Used / Not Used\", and the "
				"Switch-Matrix Table prints \"Not Used\" in each of the twelve matching cells."
			)
		if address in MATRIX_PAGE_WORDING:
			notes += (
				f" The Switch-Matrix Table prints this position \"{MATRIX_PAGE_WORDING[address]}\"; the label "
				"here is the Switches parts list wording."
			)
		if address in UNTYPED_SWITCH_ADDRESSES:
			notes += UNTYPED_SWITCH_NOTE
		if address in (37, 38):
			notes += (
				" The two manual pages disagree about this switch and the parts list wins: the Switch-Matrix "
				"Table annotates it \"(EOS)\", but the Switches parts list gives part SW-1A-150-1 (left) / "
				"SW-1A-150 (right), and the C-9952-R Flipper Assemblies parts list identifies SW-1A-150 as item "
				"2b, the Lane Change Switch, a different part from that same assembly's item 2a End of Stroke "
				"(EOS) Switch 03-7811, which carries no matrix address anywhere in the manual. Pinned PinMAME "
				"agrees with the parts list by construction: hsGameData's FLIP_SWNO(37,38) makes core_updateSw "
				"drive this address from live flipper-button state, and because hw.flippers carries no FLIP_SOL "
				"bit no EOS bit is ever added to locals.flipMask, so PinMAME models no EOS switch at all here."
			)
		if address == 2:
			notes += (
				" hsGameData's hw.gameSpecific1 is 0, so S11_MUXSW2 is unset and SWITCH_UPDATE(s11) does not "
				"overwrite this address with mux-relay feedback the way it does on a System 11B game that sets "
				"that flag. The manual's own label for the position is a real device, the Ball Roll Tilt."
			)
		if address in (33, 34, 35):
			notes += (
				" The retained VPX table binds this bumper group to the wrong two addresses and the manual "
				"resolves it: both of the manual's own numbered locations drawings (switches 33/34/35 on printed "
				"page 32, solenoids 21/20/19 on printed page 34) place the Upper Left bumper highest and "
				"leftmost, the Lower Left bumper directly below it, and the Right bumper to the right of both, "
				"whereas the retained script binds Bumper2_Hit (the rightmost object) to switch 34 and "
				"Bumper3_Hit (the lowest object) to switch 35. The coordinate recorded here follows the manual."
			)
		if address in SPECIAL_SOLENOID_SWITCH.values():
			special = next(sol for sol, sw in SPECIAL_SOLENOID_SWITCH.items() if sw == address)
			notes += (
				f" This switch also fires solenoid {special} directly in hardware: it is entry "
				f"{special - 16} of hsGameData's sxx.ssSw array, so whenever the switched-solenoid enable is "
				"active PinMAME asserts that special solenoid from this switch's own state rather than from any "
				"CPU write (src/wpc/s11.c lines 191-200)."
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
		elif address in (1, 2, 7, 41):
			availability = "used"
			extra["roles"] = ["cabinet.tilt"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 3:
			availability = "used"
			extra["roles"] = ["cabinet.service"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address in (4, 5, 6):
			availability = "used"
			extra["roles"] = ["cabinet.coin"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 8:
			availability = "used"
			extra["roles"] = ["cabinet.service"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			availability = "used"
			extra["spatial"] = located(identifier, "sensor", SWITCH_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device(identifier, label, "switch", "pinmame.input.switch", address, availability, refs, **extra))

	items.append(
		_device(
			"switch.dip-0", "Country Jumper (USA/Germany)", "dip_switch", "pinmame.input.dip", 0, "used",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
			aliases=[{"namespace": "pinmame.dip", "value": "0"}],
			physical={
				"location": "System 11 CPU board",
				"switch_type": "dip",
				"notes": (
					"System 11's single Country jumper, read via core_getDip(0)<<7 on PIA2 PA7; MDRV_DIPS(1) and "
					"the port's own comment call it a jumper rather than a DIP bank. The manual's Special Preset "
					"Adjustments 53-66 (Install German 1 through 4, Install French, Install Belgium, Install "
					"Novelty, Install Extra Hard and so on) plus its Pricing Table's separate USA & Canada, West "
					"Germany and Belgium blocks are the operator-facing counterpart. The CPU-board jumper list is "
					"in the Amendments sheet: W1, W2, W4, W5, W7 on a Revision A board, plus W8, W11-W14, W16-W18 "
					"on a Revision B board."
				),
			},
			spatial=not_applicable("dip_switch", MANUAL_SOURCE),
		)
	)
	return items


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []

	for address in range(1, 23):
		identifier = output_id(address)
		label = SOLENOID_LABELS[address]
		kind = SOLENOID_KIND[address]
		notes = f"Printed Solenoid Table entry {address:02d}, Solenoid Type \"{SOLENOID_TYPE[address]}\"."
		if address in SOLENOID_TABLE_WORDING:
			notes += (
				f" The Solenoid Table's Function column reads \"{SOLENOID_TABLE_WORDING[address]}\"; the label "
				"here is the Solenoids/Flashers parts list wording."
			)
		if address in (7, 8):
			notes += (
				" Both manual pages print \"Hideout Relay\", and the manufacturer's own Amendments sheet corrects "
				"that to \"COIL\": \"change the description, LEFT HIDEOUT RELAY, to LEFT HIDEOUT COIL. (The same "
				"change applies to the Right Hideout Relay designator; it should be 'coil'.)\" The part "
				"AE-24-900-02 is a coil in any case. A separate snubbed 2-pole 24 VDC relay does sit in the "
				"circuit (Relay Snubber Assembly B-11160, which the same amendment substitutes for the original "
				"black relay in both hideout kicker circuits and in the outlane kickback circuit)."
			)
		if 17 <= address <= 22:
			ss_switch = SPECIAL_SOLENOID_SWITCH[address]
			notes += (
				f" This is special solenoid #{address - 16}, resolved to public address {address} both by the "
				"Solenoid Table's own sequential Special # column and by setSSSol's ssSolNo[0] = {5,4,1,2,0,3} "
				"PIA-to-address table. hsGameData's sxx.ssSw entry for this slot is "
				f"{ss_switch}"
			)
			if ss_switch:
				notes += (
					f", so while the switched-solenoid enable is active PinMAME drives this output directly from "
					f"switch {ss_switch} ({SWITCH_LABELS[ss_switch]}) rather than from a CPU write "
					"(src/wpc/s11.c lines 191-200). That is the emulator's model of real System 11 switched-"
					"solenoid hardware, where the switch completes the coil circuit itself for zero-latency "
					"response, and it matches the manual pairing exactly."
				)
			else:
				notes += (
					", i.e. no direct switch: this is the one special solenoid with no actuating switch of its "
					"own, so it is only ever fired by a CPU write through setSSSol. That is consistent with it "
					"being a flasher circuit rather than a kicker or bumper."
				)
		if address in SOLENOID_CALLBACKS:
			notes += f" Retained script callback: {SOLENOID_CALLBACKS[address]}."
		if address == 4:
			notes += (
				" Backbox device. The Solenoid Table's Playfield/Cabinet column reads \"Backbox\" and the "
				"Solenoids/Flashers list repeats \"(Backbox)\"; the Police Light Assembly C-10933 is a 100 rpm "
				"24 VAC motor (14-7939) turning a reflector assembly in front of a single #1683 28 V bulb "
				"(24-8771) under a red lens. Pinned PinMAME's own MACHINE_INIT comment for this address says the "
				"same thing with the bulb number transposed: \"In fact, this is a relay controlling police light "
				"which is a #1628 28V bulb\". The retained script has no callback for this address at all and "
				"instead animates its police-beacon flashers off lamp 41's own state, a table shortcut rather "
				"than evidence about the machine."
			)
		if address == 10:
			notes += (
				" Backbox device: its only connection is 9P1-7, and connector prefix 9 is the backbox Insert "
				"Board per the manual's own circuit-board number list. The retained script has no callback for "
				"this address."
			)
		if address == 11:
			notes += (
				" The game's single general-illumination relay, described by the Solenoids/Flashers list as a "
				"\"Pwr Sup Bd Relay\" and wired to 3P7-1 on the Power Supply Board (D-8345-541). The Power Wiring "
				"Diagram (printed page 47) shows its two contact sets in series with the supply legs feeding "
				"3J6/3P8, whose eight fused lines fan out to the backbox Insert Board (9J2 pins 1-4), the cabinet "
				"(7J6-2/7J6-3 through 7J4-1/7J4-2) and the playfield (8J4 pins 3-6), so this one address switches "
				"playfield, cabinet and backbox general illumination together. Two other sources describe it more "
				"narrowly and neither is authoritative for physical wiring: pinned PinMAME's hs_ MACHINE_INIT "
				"block comments it \"Backbox GI output\", and the retained script's PFGI handler drives a "
				"playfield-only 68-member GI light collection (inverted, so energising the relay turns that "
				"collection off). No page of the manual enumerates a GI bulb count, bulb type or position, so no "
				"spatial record is asserted; see coverage.missing spatial_placement."
			)
		if address == 15:
			notes += (
				" Backbox device: the Solenoid Table's Playfield/Cabinet column reads \"Backbox\", and no "
				"knocker appears on either numbered playfield locations drawing."
			)
		if address == 16:
			notes += (
				" Cabinet device: connector prefix 7 is the cabinet per the manual's board list, and the coin "
				"lockout relay lives in the coin door. The two manual pages give different Coinco part numbers "
				"for it; see conflict.coin-lockout-relay-part-number."
			)
		if address == 13:
			notes += (
				" One coil driving one gate: the Ramp Gate Assembly D-10884 parts list has a single Coil "
				"Assembly (AL-23-800-01), a single Drive Arm Assembly, a single Drive Link and a single Gate "
				"(C-10888), and the assembly appears once as item 13 of the Playfield Parts list, so the "
				"Solenoid Table's plural \"Ramp Gates\" is not matched by a second gate part. The assembly "
				"contains no switch of any kind and no matrix address names it."
			)
		if address in SOLENOID_PROJECTIONS:
			notes += " " + SOLENOID_PROJECTIONS[address]

		wiring: dict[str, Any] = {
			"board": "System 11 CPU board",
			"driver_transistor": SOLENOID_DRIVER[address],
			"drive_wire": SOLENOID_WIRE[address],
			"control_connection": SOLENOID_CPU[address],
			"power_connection": SOLENOID_POWER[address],
		}
		physical: dict[str, Any] = {"part_number": SOLENOID_PART[address], "notes": notes}
		aliases = [
			{"namespace": "pinmame.solenoid", "value": str(address)},
			{"namespace": "manual.address", "value": f"{address:02d}"},
		]
		if 17 <= address <= 22:
			aliases.append({"namespace": "manual.special-solenoid", "value": f"Special #{address - 16}"})
		extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE)
		if address in SOLENOID_CALLBACKS:
			refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)

		if address == 4:
			extra["roles"] = ["cabinet.beacon"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
		elif address == 10:
			extra["roles"] = ["cabinet.backbox-flasher"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 11:
			extra["roles"] = ["gi.playfield-cabinet-and-backbox"]
			# spatial intentionally omitted; the manual enumerates no GI bulb position.
		elif address == 15:
			extra["roles"] = ["cabinet.knocker"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		elif address == 16:
			extra["roles"] = ["cabinet.coin-lockout"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		else:
			role = "emitter" if kind == "flasher" else "effect"
			extra["spatial"] = located(identifier, role, SOLENOID_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
		items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, "used", refs, **extra))

	for address in range(23, 51):
		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = f"device.{slug(label)}"
		if address in VIRTUAL_SOLENOID_NOTES:
			notes = VIRTUAL_SOLENOID_NOTES[address]
		elif 25 <= address <= 32:
			notes = MUX_SLOT_NOTE.format(a_address=address - 24)
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
		else:
			roles = ["internal.unused-platform-slot"]
		items.append(
			_device(
				identifier, label, "virtual", "pinmame.output.solenoid", address,
				"used" if address in (23, 45, 46, 47, 48) else "unused",
				(CONTROLLER_SOURCE, CORE_SOURCE) if address not in (23, 45) else (CONTROLLER_SOURCE, CORE_SOURCE, MANUAL_SOURCE),
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
		quantity = 2 if address in TWO_BULB_LAMPS else 1
		notes = f"Printed lamp-matrix drive column {column}, return row {row}."
		if address in LAMP_MATRIX_PAGE_WORDING:
			notes += (
				f" The Lamp-Matrix Table prints this insert \"{LAMP_MATRIX_PAGE_WORDING[address]}\"; the label "
				"here is the Lamps list wording."
			)
		if address in TWO_BULB_LAMPS:
			notes += (
				" The Lamp-Matrix Table marks this address with its boxed \"[2] Two lamps in circuit\" legend; "
				"sweeping all 64 cells of the rendered page, that marker appears on addresses 1, 3, 9 and 40 and "
				"nowhere else."
			)
		if address in BACKGLASS_ONLY_LAMPS:
			notes += (
				" The Lamps list gives this address the location \"(Backglass)\", so it has no playfield "
				"position. UpdateLamps drives it with FadeReel against a Reel object (a member of the retained "
				"table's BG collection) rather than a Light."
			)
		if address == 3:
			notes += (
				" The Lamps list splits this two-bulb circuit across the backbox and the playfield: \"Shoot "
				"Again (Backglass) / Drive Again (Playfield)\". Only the playfield bulb has a coordinate; "
				"UpdateLamps drives the backglass bulb through FadeReel against Reel L3a and the playfield bulb "
				"through NFadeLm against Light l3, so quantity is 2 but a single placement is correct."
			)
		if address == 9:
			notes += (
				" Both bulbs of this circuit are on the playfield, one in each flipper return lane per the Lamps "
				"list (\"20,000 Light Kickback (Left & Right Flipper Lanes)\"), and UpdateLamps drives two Light "
				"objects (l9, L9b) accordingly."
			)
		if address == 40:
			notes += (
				" The manual states two bulbs for this circuit but never says where the second one is: neither "
				"the Lamp-Matrix Table nor the Lamps list breaks the location down, and there is no third lamp "
				"page. The retained table models a single Light object at the coordinate recorded here, so this "
				"address carries one placement against a quantity of two. See coverage.missing "
				"spatial_placement."
			)
		if address == 8:
			notes += " The Lamps list prints \"Arow\" here; its symmetric partners at 7 and 10 print \"Arrow\"."
		if address == 41:
			notes += (
				" A centre-playfield insert, not one of the Ramp Stoplight trio at 42-44. The retained table "
				"additionally uses this address's own light state as the trigger for its police-beacon "
				"animation, which is a table shortcut for solenoid 4 rather than a property of the lamp."
			)
		if address in UNPLACED_LAMPS:
			notes += UNPLACED_LAMP_NOTE

		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.lamp", "value": str(address)},
				{"namespace": "manual.address", "value": str(address)},
			],
			"physical": {"quantity": quantity, "notes": notes},
			"wiring": {
				"board": "System 11 CPU board",
				"drive_wire": LAMP_COLUMN_WIRING[column][0],
				"drive_connection": LAMP_COLUMN_WIRING[column][1],
				"return_wire": LAMP_ROW_WIRING[row][0],
				"return_connection": LAMP_ROW_WIRING[row][1],
				"driver_transistor": f"column driver {LAMP_COLUMN_WIRING[column][2]}, row driver {LAMP_ROW_WIRING[row][2]}",
			},
		}
		if address in BACKGLASS_ONLY_LAMPS:
			extra["roles"] = ["cabinet.backglass-indicator"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
		elif address in UNPLACED_LAMPS:
			pass  # spatial intentionally omitted; see UNPLACED_LAMP_NOTE.
		else:
			extra["spatial"] = located(identifier, "emitter", LAMP_POSITIONS[address], VPX_TABLE_SOURCE, MANUAL_SOURCE)
		items.append(
			_device(
				identifier, label, "lamp", "pinmame.output.lamp", address, "used",
				(MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), **extra
			)
		)
	return items


def displays() -> list[dict[str, Any]]:
	def display(identifier: str, label: str, index: int, start: int, width: int) -> dict[str, Any]:
		return {
			"id": identifier, "label": label, "kind": "segment", "controller_index": index,
			"segment_start": start, "width": width, "height": 1,
			"spatial": not_applicable("cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}

	return [
		display("display.speeder-1", "SPEEDER 1 player score, seven 16-segment alphanumeric digits", 0, 1, 7),
		display("display.speeder-2", "SPEEDER 2 player score, seven 16-segment alphanumeric digits", 1, 9, 7),
		display("display.speeder-3", "SPEEDER 3 player score, seven 7-segment-plus-comma digits", 2, 21, 7),
		display("display.speeder-4", "SPEEDER 4 player score, seven 7-segment-plus-comma digits", 3, 29, 7),
		display(
			"display.ball-in-play-match",
			"BALL IN PLAY / MATCH, two small 7-segment digits at non-contiguous controller segment positions 0 and 8",
			4, 0, 2,
		),
		display(
			"display.credits",
			"Credits, two small 7-segment digits at non-contiguous controller segment positions 20 and 28",
			5, 20, 2,
		),
	]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, *refs: str, assembly_part_number: str | None = None) -> dict[str, Any]:
		record: dict[str, Any] = {
			"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
			"behavior": behavior, "provenance": provenance(*refs),
		}
		if assembly_part_number:
			record["assembly_part_number"] = assembly_part_number
		return record

	return [
		mechanism(
			"mechanism.trough", "Outhole and three-position ball trough", "kicker",
			[output_id(1), output_id(2)],
			["switch.matrix-9", "switch.matrix-10", "switch.matrix-11", "switch.matrix-12"],
			"A ball draining from the playfield lands in the outhole (switch 9, part 17-1067) and solenoid 1 "
			"(Outhole, AE-23-800-01) kicks it into the trough tube, where up to three balls queue on switches "
			"10 (Left Trough), 11 (Centre Trough) and 12 (Right Trough). Solenoid 2 (Ball Release, "
			"AE-23-800-03) ejects the lead ball into the shooter lane. The manual's own switch-locations "
			"drawing runs the tube from callout 9 at the left end of the cabinet's lower edge up to callout 12 "
			"nearest the shooter feed, so 12 is the position closest to release; the retained script's "
			"cvpmBallStack initialisation (bsTrough.InitSw 9,12,11,10 followed by bsTrough.InitKick "
			"BallRelease,90,10) independently declares the same order. No individual trough position has its "
			"own object in the retained table.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.eject-hole", "Upper-right eject hole", "kicker",
			[output_id(3)], ["switch.matrix-16"],
			"A ball entering the eject hole at the top right of the playfield rests on switch 16 (part "
			"17-1012, shielded by the Metal Eject Shield 01-6933-2) and is kicked back out by solenoid 3 "
			"(Eject Hole, AE-23-800-03). The retained script models it as a saucer "
			"(bsSaucer.InitSaucer sw16,16,96,5). Two lamp inserts sit in this hole per the Lamps list, "
			"\"Extra Ball (Eject Hole)\" at lamp 11 and \"Escape (Eject Hole)\" at lamp 12, which is what makes "
			"it the escape-from-the-chase feature rather than a plain kickout.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.left-hideout", "Left hideout ball lane", "kicker",
			[output_id(7)], ["switch.matrix-39", "switch.matrix-40"],
			"The left-hand pair of ball chutes (Ball Chute, Upper Left D-10863 and Ball Chute, Lower Left "
			"D-11050) forms a two-switch lane: a ball entering passes switch 39 (Upper Left Hideout, assembly "
			"A-11047) and comes to rest on switch 40 (Lower Left Hideout, part 17-1085). Solenoid 7 kicks it "
			"back out. Both manual pages print the coil \"Left Hideout Relay\" and the manufacturer's own "
			"Amendments sheet corrects that to \"Left Hideout Coil\"; a separate snubbed relay (Relay Snubber "
			"Assembly B-11160) does sit in the circuit. The retained script models only the resting position "
			"(bsLeftLock.InitSw 0,0,40 with bsLeftLock.InitSaucer LKick,40) and never drives switch 39.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.right-hideout", "Right hideout ball lane", "kicker",
			[output_id(8)], ["switch.matrix-47", "switch.matrix-48"],
			"The mirror of the left hideout, built from Ball Chute, Upper Right D-10862 and Ball Chute, Lower "
			"Right D-11049: switch 47 (Upper Right Hideout, A-11047) on the way in, switch 48 (Lower Right "
			"Hideout, 17-1085) at rest, solenoid 8 to eject. Locking a ball in each hideout is what stages "
			"the machine's multiball, and lamps 39 and 40 (\"Ramp Earns Hideout\" and \"Ramp Earns Hideout "
			"Jackpot\") are the inserts that advertise it -- High Speed is the machine that introduced the "
			"multiball jackpot.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
		mechanism(
			"mechanism.ramp-gate", "Ramp gate", "gate",
			[output_id(13)], [],
			"A single pivoting gate at the top of the playfield, driven by solenoid 13 through a drive arm and "
			"drive link, that selects which way a ball leaving the two-level main ramp is sent. The Ramp Gate "
			"Assembly D-10884 parts list contains exactly one Coil Assembly (AL-23-800-01), one Drive Arm "
			"Assembly (A-10886), one Drive Link (01-8201), one Gate Mech. Subassembly (D-10885) and one Gate "
			"(C-10888), and contains no switch, opto or sensor part of any kind; no matrix address names the "
			"gate either, so the mechanism has no position feedback at all and its state must be tracked from "
			"the drive signal. The retained script's Divert handler drops and raises two gate objects together "
			"and moves two companion primitives in z, i.e. it splits the one physical gate in two.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="D-10884",
		),
		mechanism(
			"mechanism.main-ramp", "Two-level main ramp with two rollover switches", "other",
			[], ["switch.matrix-42", "switch.matrix-43"],
			"The HIGH SPEED Ramp Assembly D-10905 carries two SW-1A-160 rollover switches, which the Switches "
			"parts list numbers 42 (Left Ramp) and 43 (Right Ramp); the manual's own switch-locations drawing "
			"places both across the very top of the playfield with 42 to the left of 43. The ramp is the "
			"machine's main scoring shot: lamps 36-40 are the \"Ramp Earns\" ladder (Bonus X, Ramp Bonus, "
			"Getaway, Hideout, Hideout Jackpot) and lamps 42-44 are the Ramp Stoplight trio that shows which "
			"award is live. The ramp itself has no coil; solenoid 13's gate is what steers its exit.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="D-10905",
		),
		mechanism(
			"mechanism.outlane-kickback", "Left outlane kickback", "kicker",
			[output_id(14)], ["switch.matrix-31"],
			"A bell-armature kickback (Outlane Kickback Assembly A-11041, coil AE-24-900-01) mounted at the "
			"left outlane. A ball rolling over switch 31 (Left Outlane) can be fired back into play while the "
			"kickback is lit -- lamp 16 is the \"Kickback Arrow (Left Outlane)\" insert and lamp 9 the "
			"\"20,000 Light Kickback\" pair in the return lanes. The Amendments sheet adds the circuit's own "
			"wiring diagram: the coil sits in the 50 V DC circuit fed through 8J4 VIO-YEL with a 100 ohm 3 W "
			"resistor on the +34 V side, switched through the relay the same amendment replaces with the "
			"snubbed B-11160 assembly. There is no matching kickback on the right outlane (switch 32).",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-11041",
		),
		mechanism(
			"mechanism.jet-bumpers", "Three-bumper jet nest", "other",
			[output_id(21), output_id(20), output_id(19)],
			["switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Three jet bumpers in a triangle in the upper-left half of the playfield: Upper Left (switch 33, "
			"solenoid 21), Lower Left (switch 34, solenoid 20) and Right (switch 35, solenoid 19). Each is a "
			"B-9414 Jet Bumper Assembly carrying its own #44 bulb in the cap, sitting over a B-9415 Jet Bumper "
			"Coil Assembly, with an A-7459-7 switch. All three coils are special solenoids fired directly by "
			"their own switch through the switched-solenoid supply: hsGameData's sxx.ssSw pairs solenoid 21 "
			"with switch 33, solenoid 20 with switch 34 and solenoid 19 with switch 35, exactly as the manual "
			"names them. The cap bulbs are part of the general illumination, not of the strobed lamp matrix -- "
			"no lamp address names a jet bumper.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-9414 with B-9415",
		),
		mechanism(
			"mechanism.slingshots", "Left and right slingshot kickers", "other",
			[output_id(17), output_id(18)], ["switch.matrix-49", "switch.matrix-50"],
			"Two kicker arm assemblies (B-11051-R and its left-hand counterpart) above the flippers. Each has "
			"two switches: an SW-1A-122 scoring switch the CPU reads (matrix 49 left, 50 right) and a separate "
			"kicker actuating switch (A-4834-H, or B-8734 with an RC network) that completes the coil circuit "
			"itself -- the Switches parts list prints that second part in a bracketed annotation beside rows "
			"49 and 50. Solenoids 17 and 18 are special solenoids whose sxx.ssSw entries are switches 49 and "
			"50, so PinMAME models the same direct-switch firing.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-11051-R",
		),
		mechanism(
			"mechanism.spin-targets", "Three freeway spin targets", "rotary",
			[], ["switch.matrix-44", "switch.matrix-45", "switch.matrix-46"],
			"Three rotating decal-screened spin targets, each an SW-1A-118 switch on a shaft with a switch "
			"actuator wire (12-6620): Left (switch 44), Centre (switch 45) and Right (switch 46). The "
			"Playfield Parts list names them as Spin Target Assemblies B-11019-2 \"Bayshore Freeway\", "
			"B-11019-1 \"Santa Monica Freeway\" and B-11019-3 \"San Diego Freeway\" (items 8, 20 and 21) but "
			"does not say which decal is fitted at which of the three positions. They have no coil; lamps 7, "
			"10 and 8 are their matching 1000-point arrow inserts and lamps 31-35 the Freeway score ladder.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="B-11019-1, B-11019-2, B-11019-3",
		),
		mechanism(
			"mechanism.stoplight-target-banks", "Three three-target stoplight banks", "other",
			[],
			[
				"switch.matrix-13", "switch.matrix-14", "switch.matrix-15",
				"switch.matrix-17", "switch.matrix-18", "switch.matrix-19",
				"switch.matrix-22", "switch.matrix-23", "switch.matrix-24",
			],
			"Three banks of three standup targets, each bank a red/yellow/green set matching a traffic light: "
			"Lower Left (switches 13/14/15), Upper Left (17/18/19) and Right (22/23/24). Each target is a "
			"separate assembly by colour -- A-11022 red, A-11054 yellow, A-11055 green -- and each has its own "
			"lamp insert of the same colour (13-15, 17-19 and 22-24 on the lamp side). These are standup "
			"targets, not drop targets: no solenoid in the Solenoid Table resets a target bank, no bank appears "
			"on either locations drawing as a drop unit, and the retained table models all nine as HitTarget "
			"objects pulsed through vpmTimer.PulseSw. Completing them is what lights Escape at lamp 41.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-11022, A-11054, A-11055",
		),
		mechanism(
			"mechanism.standup-target-arrows", "Six arrow standup targets", "other",
			[],
			[
				"switch.matrix-25", "switch.matrix-26", "switch.matrix-27",
				"switch.matrix-28", "switch.matrix-29", "switch.matrix-30",
			],
			"Six A-8253 standup targets, three along the left inner wall (switches 25, 26, 27) and three "
			"along the right (28, 29, 30), each with its own matching arrow insert at the same lamp address. "
			"No coil is associated with any of them.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="A-8253",
		),
		mechanism(
			"mechanism.flippers", "Three flippers, none CPU-driven", "other",
			[], ["switch.matrix-37", "switch.matrix-38"],
			"Three FL 23/600-30/2600-50VDC flipper coils: lower left, lower right, and an upper-right flipper "
			"the manual's Solenoids/Flashers list calls simply \"Upper Flipper\". None of the three has a Sol. "
			"No. or a driver transistor in the Solenoid Table, and note 1 says the CPU-board wires that do "
			"appear (Orn-Vio at 1P19-1, Orn-Gry at 1P19-2) run to the flipper switch rather than to a coil, "
			"with a second wire running from the switch on to the coil (note 3): the coils are fired by the "
			"cabinet button through the switched-solenoid supply, which is why PinMAME's public flipper "
			"addresses 45-48 are fabricated from button state rather than read from hardware. What the CPU "
			"does read is a Lane Change switch on each lower flipper's own base assembly (C-9954-R Flipper "
			"Base/Lane Change Assembly, switch SW-1A-150), reported at matrix 37 (left) and 38 (right) and "
			"used for lane change and for the engine-revving sound. Each assembly also carries an End of "
			"Stroke switch (03-7811) in the coil circuit, normally closed and opening at end of stroke per the "
			"page's own adjustment note, with no matrix address at all. The retained script rotates the "
			"upper-right flipper from the lower-right flipper's own callback; see "
			"conflict.upper-flipper-driving-button.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
			assembly_part_number="C-9952-R with C-9953-L unique parts",
		),
		mechanism(
			"mechanism.police-beacon", "Backbox police beacon", "motorized",
			[output_id(4)], [],
			"The machine's signature police light: a 100 rpm 24 VAC motor (14-7939) turning a reflector "
			"assembly (B-10917) in front of a single #1683 28 V bulb (24-8771) behind a red lens (03-7981), "
			"held on with a lens clip assembly, washer and wing nut. Solenoid 4 energises the relay "
			"(5580-10883-00) that powers it, so the CPU controls only on and off, not rotation speed or "
			"phase. The Solenoid Table puts it in the Backbox and the parts list repeats \"(Backbox)\", so it "
			"has no playfield coordinate. It has no switch of any kind.",
			MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="C-10933",
		),
		mechanism(
			"mechanism.traffic-light", "Playfield ramp traffic light", "other",
			[], [],
			"A three-bulb playfield fixture (Traffic Light Assembly B-10921, item 9 of the Playfield Parts "
			"list) built from a light housing plate, a housing subassembly, a PCB standoff and one Light "
			"Socket & Cable Assembly (C-10915) covering all three sockets. Its bulbs are lamp-matrix "
			"addresses 42, 43 and 44 (Red, Yellow, Green Light (Ramp Stoplight)), which show which Ramp Earns "
			"award is currently live. It has no coil and no switch. The retained table carries no usable "
			"playfield coordinate for it; see coverage.missing spatial_placement.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="B-10921",
		),
		mechanism(
			"mechanism.knocker", "Backbox knocker", "other",
			[output_id(15)], [],
			"Solenoid 15 (AE-23-800-02) raps a knocker coil in the backbox for replay and award signals. The "
			"Solenoid Table's Playfield/Cabinet column reads \"Backbox\" and no switch is associated with it.",
			MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": f"relationship.special-solenoid-{solenoid}",
			"kind": "direct",
			"source": f"switch.matrix-{switch}",
			"destination": output_id(solenoid),
			"provenance": provenance(CORE_SOURCE, MANUAL_SOURCE),
		}
		for solenoid, switch in sorted(SPECIAL_SOLENOID_SWITCH.items())
		if switch
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.upper-flipper-driving-button",
			"path": "mechanisms[id=mechanism.flippers]",
			"description": (
				"High Speed has a third, upper-right flipper, but no source states which cabinet button fires "
				"it. The manual's Solenoid Table lists it as \"Upper Flipper\" with no Sol. No., no driver "
				"transistor and no CPU-board connection, giving it only its own playfield connector pins "
				"(Blk-Yel to 7J1-19 and 8P3-33) which sit between the left flipper's 8P3-32 and the right "
				"flipper's 8P3-34; the Solenoids/Flashers parts list repeats the bare name; and neither page "
				"names a side. Pinned PinMAME models no upper flipper at all for this driver, since "
				"hsGameData's hw.flippers is FLIP_SWNO(37,38) with no FLIP_SW or FLIP_SOL bit for either upper "
				"position, so public addresses 33-36 read as always zero and no third synthetic output exists. "
				"The only source that asserts anything is the retained known-working VPX table, whose "
				"SolRFlipper handler rotates RightFlipper and RightFlipper1 together, i.e. it assumes the "
				"upper-right flipper shares the lower-right flipper's button and coil circuit. That is "
				"plausible and matches the position -- the manual's own switch-locations drawing does place a "
				"third flipper bat on the right side of the playfield above the right hideout lane, and the "
				"Switches parts list has no third flipper-button row anywhere, so the coil must be fed from one "
				"of the two existing button circuits -- but it rests on a single community source. Resolution "
				"path: the Section 3 flipper-circuit schematic sheet (not transcribed here) or a photograph of "
				"an unrestored machine's 8P3 harness would show which button feed 8P3-33 is paralleled onto. "
				"Unresolved."
			),
			"source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE],
		},
		{
			"id": "conflict.coin-lockout-relay-part-number",
			"path": "outputs[binding.device=16]",
			"description": (
				"The manual gives two different Coinco part numbers for the same coin-door lockout relay. The "
				"Solenoid Table (printed page 25) prints 404603-22 in its Solenoid Part No. column with note 2, "
				"\"Solenoid 16 has a Coinco part number\"; the Solenoids/Flashers parts list (printed page 34) "
				"prints 904218-696 with the annotation \"Coin-Lockout Relay (Coinco p/n)\". Both pages agree on "
				"the device, its address, its wiring (Brn-Gry, 1P12-9, 7P1-7 and 7P2-4, driver Q6) and that the "
				"part is Coinco's rather than Williams'; nothing in the manual or in the Amendments sheet "
				"reconciles the two numbers, and the retained table has no callback for the address. The "
				"definition records 404603-22, from the wiring table of record, and this conflict preserves the "
				"other. Authoring impact is nil -- the device is a cabinet coin-door relay with no playfield "
				"presence -- but a part number that two pages of one manual disagree about should not be "
				"presented as settled. Resolution path: a Williams parts catalogue or a Coinco cross-reference. "
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
			"id": MACHINE_ID,
			"name": "High Speed",
			"manufacturer": "Williams",
			"year": 1986,
			"kind": "physical_pinball",
			"ipdb_id": 1176,
			"opdb_id": "GRvzd-MLxV8",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["spatial_placement", "unresolved_conflicts"],
			"dimensions": {
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
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
		"sources": source_records(),
		"knowledge": {"path": KNOWLEDGE_PATH, "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"High Speed device identifiers are not unique: {duplicates}")
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
		if device["spatial"]["status"] != "not_applicable":
			placement_count += len(device["spatial"]["placements"])
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"status": "validated",
		"blockers": [
			"Lamp addresses 42, 43 and 44 (Red/Yellow/Green Light (Ramp Stoplight)) are real bulbs in the "
			"playfield Traffic Light Assembly B-10921 but have no derivable coordinate: the retained table's "
			"Light objects for them are parked at raw x about -2237 and its stoplight primitives sit at "
			"position (0,0,0) with the geometry baked into a mesh whose derived centre is off the top of the "
			"playfield. Their spatial keys are omitted rather than invented.",
			"Lamp address 40 (Ramp Earns Hideout Jackpot) is marked a two-bulb circuit by the Lamp-Matrix "
			"Table but the manual never says where the second bulb is and the retained table models only one "
			"Light object, so its placement count is one against a quantity of two.",
			"Solenoid address 11 (General Illumination Relay) switches playfield, cabinet and backbox general "
			"illumination together per the Power Wiring Diagram, but no page of the manual enumerates a GI "
			"bulb count, bulb type or position. The retained table's 68-member playfield GI light collection "
			"is not adopted as a placement set: it is unverifiable against the manual, contains three "
			"jet-bumper cap lights that belong to those assemblies, duplicates one member, and includes one "
			"light above the top playfield edge. The spatial key is omitted.",
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
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/williams.high-speed.1986/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/high-speed-1986/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
			"vpx_geometry": {
				"path": "external:pinmame-review-artifacts/high-speed-1986/vpx-geometry.txt",
				"sha256": VPX_GEOMETRY_SHA256,
			},
		},
		"excluded_object_classes": [
			"a00-a3f and LED* Light objects: alphanumeric display segment simulation (the script's Digits() and Leds() arrays), not playfield lamps",
			"f109*/f112* Light objects: glow companions clustered on the Flasherbase1-4 flasher dome positions",
			"F105b/F106b: co-located bulb-and-glow doubles of F105/F106; F105c/F105d/F106c/F106d: end-of-lens glow lights of the same single elongated lens",
			"Flasherflash*/Flasherlit* objects: Flupper flasher render members of the dome assemblies already placed through their bases or lights",
			"FlasherRed/FlasherBlue/FlRoundRed/FlRoundBlue/FlWideRed/FlWideBlue: the table's police-beacon effect, driven from lamp 41's state rather than from solenoid 4",
			"L1/L2/L3a/L6 Reel objects (the BG collection): backglass indicators, recorded as not_applicable cabinet_or_service lamp records",
			"kicker1-kicker4: subway teleport pairs used by the hideout ball paths, not switch or coil positions",
			"Trigger1-Trigger11 and Trigger111-Trigger113: sound-only triggers with no Controller.Switch call",
		],
		"unresolved": ["conflict.upper-flipper-driving-button", "conflict.coin-lockout-relay-part-number"],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# High Speed (Williams, 1986) spatial review",
		"",
		f"Status: {report['status']}. The physical machine record itself remains `partial` at "
		"`machines/partial/williams/high-speed-1986.json` because of the three spatial gaps and two "
		"unresolved conflicts named below; see the promotion decision.",
		"",
		"The matching source is the retained known-working `High Speed (Williams 1986).vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained vpxtool extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield "
		f"bounds are `{TABLE_BOUNDS}`, and every canonical coordinate is x/952 and y/1974 rounded to at most "
		"six fractional places. The y bound of 1974 is much shorter than the 2115-2594 of the later "
		"machines curated in this project, which is what a mid-1980s playfield measures.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPX script is the runtime address and causality authority; the Williams instruction "
		"manual is the physical inventory, quantity, wiring and location authority; pinned PinMAME owns "
		"controller topology and the System 11 address-space rules; the retained table supplies geometry, "
		"but only where the manual's own numbered locations drawings agree with it.",
		"- That last qualification matters on this machine. The retained table binds switch 34 to the "
		"rightmost jet bumper and switch 35 to the lowest, which is the opposite of both of the manual's own "
		"numbered locations drawings; the coordinates recorded here follow the manual, and the disagreement "
		"is disclosed on all three bumper switches.",
		"- System 11 has no separate GI address space: general illumination is one ordinary solenoid address "
		"(11) whose per-game bulb-type metadata happens to be a continuous AC GI type, resolved from pinned "
		"PinMAME's own per-game MACHINE_INIT block. High Speed has one GI relay where Whirlwind has two.",
		"- High Speed declares no A/C select relay (`sxx.muxSol = 0`) and no sound-overlay board "
		"(`hw.gameSpecific1 = 0`), so the platform's 25-32 alias bank and 37-44 overlay range are both "
		"enumerated as unpopulated rather than mapped to devices. This is the largest single difference from "
		"the project's other System 11 machine.",
		"- Switches 9-12 (outhole and trough), 37/38 (flipper lane change) and 49/50 (slingshot scoring) have "
		"no object of their own in the retained table and are documented projections onto their own "
		"mechanism's retained object; switches 39 and 47 take their coordinates from two unbound triggers "
		"whose positions are corroborated by the manual's own upper-above-lower ordering in each hideout "
		"lane.",
		"- Cabinet and backbox devices get controlled `not_applicable` records rather than coordinates: the "
		"eight cabinet switches, the four diagnostic buttons, the Country jumper, the police-light relay, the "
		"insert-board flashers, the knocker, the coin-lockout relay, the three backglass lamps and all six "
		"displays.",
		"- The police beacon is backbox hardware. Both the Solenoid Table's Playfield/Cabinet column and the "
		"Solenoids/Flashers parts list say so explicitly, so it takes a controlled `not_applicable` record "
		"despite being the machine's signature device.",
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
		f"- Outputs with an intentionally omitted spatial key: {len(report['omitted_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Blockers",
		"",
	]
	for blocker in report["blockers"]:
		lines.append(f"- {blocker}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"Every controller address is enumerated and given a semantic disposition, every printed wiring "
		"detail is recorded, and the whole mechanism inventory is covered. Polarity is not a gap on this "
		"machine: `hsGameData`'s `wpc` struct is zero-initialised by its own `{{0}}` positional "
		"initializer so `wpc.invSw` is entirely unset and PinMAME normalizes no address, and the manual "
		"documents no opto and no normally-closed matrix switch anywhere -- no row of the Switches parts "
		"list carries an opto part number or is printed blank, and neither copy of the Switch-Matrix Table "
		"has an opto legend or a single shaded cell.",
		"",
		"Promotion to `author_ready` is nonetheless refused. Three addresses have real bulbs with no "
		"derivable coordinate (lamps 42-44), one has a manual-stated bulb quantity its placement count "
		"cannot meet (lamp 40), one has no enumerable emitter set at all (solenoid 11), and the definition "
		"carries two unresolved `conflicts` entries. `coverage.missing` is therefore "
		"`[\"spatial_placement\", \"unresolved_conflicts\"]` and the record stays `partial` until a second "
		"independent recreation or a photograph of an unrestored playfield places the Traffic Light "
		"Assembly and lamp 40's second bulb, a GI bulb inventory turns up, and the Section 3 flipper "
		"schematic settles which button feeds the upper-right flipper coil.",
		"",
		"## Retained evidence",
		"",
		f"- Retained vpxtool extraction, {EXTRACTION_FILE_COUNT} files.",
		f"- Manual reading log with the verified page offset and the questions the manual does not answer, "
		f"SHA-256 `{MANUAL_TRANSCRIPTION_SHA256}`.",
		f"- VPX script/geometry cross-reference, SHA-256 `{VPX_GEOMETRY_SHA256}`.",
		"- Nine transcribed manual excerpts and three rendered crops under "
		"`evidence/excerpts/williams.high-speed.1986/`.",
		"",
	]
	return "\n".join(lines)


def generate(root: Path = ROOT) -> Path:
	definition = build()
	author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if author_ready.exists():
		raise RuntimeError(
			f"Refusing to overwrite an existing author-ready High Speed artifact: {author_ready}. "
			"This curator only writes the partial record; promotion is a separate reviewed decision."
		)
	write_json(root / DEFINITION_PATH.relative_to(ROOT), definition)
	write_json(root / SEED_PATH.relative_to(ROOT), definition)
	report = build_spatial_report(definition)
	write_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT), report)
	write_text(root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT), render_spatial_report(report))
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	author_ready = root / AUTHOR_READY_PATH.relative_to(ROOT)
	if author_ready.exists():
		raise RuntimeError(
			f"High Speed is recorded partial but an author-ready artifact exists: {author_ready}"
		)
	if not definition_path.is_file():
		raise RuntimeError(f"High Speed definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"High Speed seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"High Speed definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"High Speed seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"High Speed spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"High Speed spatial review drifted from its deterministic curator: {markdown_path}")
	print("High Speed definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"High Speed extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("High Speed retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise RuntimeError("No curator mode was selected")


if __name__ == "__main__":
	main()
