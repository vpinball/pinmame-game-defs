"""Curate the physical Bally Scared Stiff (1996) machine definition.

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
# Kept partial 2026-08-07: sixteen driver-declared auxiliary lamp addresses (91-98, 101-108)
# have no resolvable semantic identity or spatial placement (conflict.aux-lamp-column-fitment),
# so the record cannot honestly promote past machines/partial.
PARTIAL_PATH = ROOT / "machines/partial/bally/scared-stiff-1996.json"
DEFINITION_PATH = PARTIAL_PATH
SEED_PATH = ROOT / "tools/seeds/bally/scared-stiff-1996.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/bally/scared-stiff-1996.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/bally/scared-stiff-1996.md"

PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-95"
MANUAL_SOURCE = "manual.bally.scared-stiff.1996"
MANUAL_SUPPORT_SOURCE = "manual-support.bally.scared-stiff.1996"
VPX_TABLE_SOURCE = "vpx-table.ss-vpw-1-0"
VPX_SCRIPT_SOURCE = "vpx-script.ss-vpw-1-0"
VPX_EXTRACTION_SOURCE = "vpx-extraction.ss-vpw-1-0"

TABLE_SHA256 = "bede6f6c5b7592c4610af444a196c42432949468f708e79b4b112a73692cdc1e"
SCRIPT_SHA256 = "4c9a63e77e10ea65d1146e33f81197bb41b719d70027d8fa0c2d258f823211b4"
MANUAL_SHA256 = "f96109c68c7e0cc008f72e9be9f18405a216d5c40165aed130f1e87b65c44b09"
MANUAL_TRANSCRIPTION_SHA256 = "493e070b4244cefd99acf907103a758d70bc9e55d5605fea412f9e7ed0696537"

EXTRACTION_RELATIVE_PATH = Path("bally/scared-stiff-1996/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("bally/scared-stiff-1996/extracted-vpxtool.manifest.json")
EXTRACTION_MANIFEST_SHA256 = "8cf07f3cef5678fdac96b27b0974a2c8653a7070ed69ea364ca5ebffd386756d"
EXTRACTION_FILE_COUNT = 2302
EXTRACTION_TOTAL_BYTES = 937624764

PLAYFIELD_WIDTH = 952.941
PLAYFIELD_HEIGHT = 2164.706
TABLE_BOUNDS = f"left=0 top=0 right={PLAYFIELD_WIDTH} bottom={PLAYFIELD_HEIGHT}"

DRIVER_IDS = ("ss_15", "ss_14", "ss_12", "ss_11", "ss_11s10", "ss_03", "ss_01", "ss_01b")
DRIVER_COMPATIBILITY = {
	"ss_15": ("identical", "Bally 1.5 game ROM shipped with the physical machine. This is the driver the retained known-working VPW table binds to (Const cGameName = \"SS_15\")."),
	"ss_14": ("identical", "Bally 1.4 game ROM; a firmware revision of the same physical machine with no controller-address or playfield change."),
	"ss_12": ("identical", "Bally 1.2 game ROM; a firmware revision of the same physical machine with no controller-address or playfield change."),
	"ss_11": ("identical", "Bally 1.1 game ROM; a firmware revision of the same physical machine with no controller-address or playfield change."),
	"ss_11s10": ("identical", "Bally 1.1 game ROM paired with the earlier 1.0 sound ROM set; same physical machine and controller addresses as ss_11."),
	"ss_03": ("identical", "Bally 0.3 prototype game ROM for the same physical machine; the switch matrix, lamp matrix, solenoid/flasher table, and playfield hardware are unchanged."),
	"ss_01": ("identical", "Bally D.01R prototype game ROM (Sound 0.25) for the same physical machine."),
	"ss_01b": ("identical", "Bally D.01R prototype coin-play game ROM (Sound 0.25) for the same physical machine as ss_01."),
}

# --- Printed switch matrix (manual page 2-44 locations, 2-44/2-45 wiring; PDF pages 109-110).
SWITCH_LABELS = {
	12: "Wheel Index", 13: "Start Button", 14: "Plumb Bob Tilt",
	16: "Kickback", 17: "Right Flipper Lane", 18: "Shooter Lane",
	21: "Slam Tilt",
	22: "Coin Door Closed", 23: "Buy In Button", 24: "Always Closed", 25: "Extra Ball Lane",
	26: "Left Flipper Lane", 27: "Right Outlane", 28: "Single Standup",
	31: "Trough Eject", 32: "Trough Ball 1", 33: "Trough Ball 2", 34: "Trough Ball 3", 35: "Trough Ball 4",
	36: "Right Popper", 37: "Left Kickout", 38: "Crate Entrance",
	41: "Coffin Left", 42: "Coffin Center", 43: "Coffin Right", 44: "Left Ramp Enter",
	45: "Right Ramp Enter", 46: "Left Ramp Made", 47: "Right Ramp Made", 48: "Coffin Entrance",
	51: "Left Slingshot", 52: "Right Slingshot", 53: "Upper Jet", 54: "Center Jet", 55: "Lower Jet",
	56: "Upper Slingshot", 57: "Crate Sensor", 58: "Left Loop",
	61: "Three Bank Upper", 62: "Three Bank Middle", 63: "Three Bank Lower",
	64: "Left Leaper", 65: "Center Leaper", 66: "Right Leaper", 67: "Left Ramp 10 Point", 68: "Right Loop",
	71: "Left Skull Lane", 72: "Center Skull Lane", 73: "Right Skull Lane", 74: "Secret Passage",
}
# Printed "Not Used" positions on both the switch-matrix page and the Switch Locations parts list.
UNUSED_MATRIX_ADDRESSES = {11, 15, 21, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
SLAM_TILT_ADDRESS = 21

# Every switch identified as an opto through the manual's "(LED)" + "(Trans.)" two-row Switch
# Part No. construction disclosure (see manual-transcription.md), plus switch 12 (Wheel Index),
# a single-part D-12046 optical home-position sensor for the Spider Wheel mechanism. This is the
# full column-3 and column-4 address range plus one column-1 address.
OPTO_SWITCHES = {12, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48}
# PinMAME's ssGameData inverted-switch mask {0x00,0x02,0x00,0xff,0xff,0x00,...,0x00}, indexed by
# column with bit = row-1: index 1 bit 1 (address 12), index 3 = 0xff (31-38), index 4 = 0xff
# (41-48). Identical to OPTO_SWITCHES -- zero disagreement.
PINMAME_NORMALIZED_OPTO_SWITCHES = set(OPTO_SWITCHES)

SWITCH_TYPES = {
	12: "opto", 13: "button", 14: "tilt", 16: "microswitch", 17: "microswitch", 18: "microswitch",
	21: "leaf",
	22: "microswitch", 23: "button", 24: "other", 25: "microswitch", 26: "microswitch",
	27: "microswitch", 28: "microswitch",
	31: "opto", 32: "opto", 33: "opto", 34: "opto", 35: "opto", 36: "opto", 37: "opto", 38: "opto",
	41: "opto", 42: "opto", 43: "opto", 44: "opto", 45: "opto", 46: "opto", 47: "opto", 48: "opto",
	51: "leaf", 52: "leaf", 53: "leaf", 54: "leaf", 55: "leaf", 56: "leaf", 57: "other", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 65: "microswitch",
	66: "microswitch", 67: "microswitch", 68: "microswitch",
	71: "microswitch", 72: "microswitch", 73: "microswitch", 74: "microswitch",
}

# address -> (assembly/opto part, switch part), transcribed verbatim from printed 2-44/2-45.
SWITCH_PARTS: dict[int, tuple[str | None, str | None]] = {
	12: (None, "D-12046"), 13: (None, "20-9663-16"), 14: (None, "04-10346"),
	16: (None, "5647-12693-19"), 17: (None, "5647-12693-19"), 18: (None, "5647-12693-65"),
	21: (None, "A-17195"),
	22: (None, "5643-09288-00"), 24: (None, "5643-09112-00"),
	25: (None, "5647-12693-19"), 26: (None, "5647-12693-19"), 27: (None, "5647-12693-19"),
	28: (None, "A-12912-23"),
	31: ("A-18617-1 (LED) with A-18618-1 (Trans.)", None),
	32: ("A-18617-1 (LED) with A-18618-1 (Trans.)", None),
	33: ("A-18617-1 (LED) with A-18618-1 (Trans.)", None),
	34: ("A-18617-1 (LED) with A-18618-1 (Trans.)", None),
	35: ("A-18617-1 (LED) with A-18618-1 (Trans.)", None),
	36: ("A-16908 (LED) with A-16909 (Trans.)", None),
	37: ("A-16908 (LED) with A-16909 (Trans.)", None),
	38: ("A-16908 (LED) with A-16909 (Trans.)", None),
	41: ("A-16908 (LED) with A-16909 (Trans.)", None),
	42: ("A-16908 (LED) with A-16909 (Trans.)", None),
	43: ("A-16908 (LED) with A-16909 (Trans.)", None),
	44: ("A-16908 (LED) with A-16909 (Trans.)", None),
	45: ("A-16908 (LED) with A-16909 (Trans.)", None),
	46: ("A-16908 (LED) with A-16909 (Trans.)", None),
	47: ("A-16908 (LED) with A-16909 (Trans.)", None),
	48: ("A-16908 (LED) with A-16909 (Trans.)", None),
	51: (None, "SW-1A-114 (Kicker) with SW-1A-120 (Score)"),
	52: (None, "SW-1A-114 (Kicker) with SW-1A-120 (Score)"),
	53: (None, "SW-11A-37"), 54: (None, "SW-11A-37"), 55: (None, "SW-11A-37"),
	56: (None, "SW-1A-120"), 57: (None, "A-19237"), 58: (None, "5647-12693-19"),
	61: (None, "A-12912-23"), 62: (None, "A-12912-23"), 63: (None, "A-12912-23"),
	64: (None, "A-20783-7"), 65: (None, "A-20783-7"), 66: (None, "A-20783-7"),
	67: (None, "SW-1A-120"), 68: (None, "5647-12693-19"),
	71: (None, "5647-12693-19"), 72: (None, "5647-12693-19"), 73: (None, "5647-12693-19"),
	74: (None, "5647-12693-19"),
}

SWITCH_COLUMN_WIRING = {
	1: ("Green-Brown", "J206-1", "U20-18"), 2: ("Green-Red", "J206-2", "U20-17"),
	3: ("Green-Orange", "J206-3", "U20-16"), 4: ("Green-Yellow", "J206-4", "U20-15"),
	5: ("Green-Black", "J206-5", "U20-14"), 6: ("Green-Blue", "J206-6", "U20-13"),
	7: ("Green-Violet", "J206-7", "U20-12"), 8: ("Green-Gray", "J206-9", "U20-11"),
}
SWITCH_ROW_WIRING = {
	1: ("White-Brown", "J208-1", "U18-11"), 2: ("White-Red", "J208-2", "U18-9"),
	3: ("White-Orange", "J208-3", "U18-5"), 4: ("White-Yellow", "J208-4", "U18-7"),
	5: ("White-Green", "J208-5", "U19-11"), 6: ("White-Blue", "J208-7", "U19-9"),
	7: ("White-Violet", "J208-8", "U19-5"), 8: ("White-Gray", "J208-9", "U19-7"),
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
# Fliptronic F1-F8 wiring, printed 2-44.
FLIPPER_SWITCH_WIRING = {
	111: ("Black-Green", "J208-13"), 112: ("Blue-Violet", "J212-12"),
	113: ("Black-Blue", "J208-12"), 114: ("Blue-Gray", "J212-11"),
	115: ("Black-Violet", "J208-11"), 116: ("Black-Yellow", "J212-10"),
	117: ("Black-Gray", "J208-10"), 118: ("Black-Blue", "J212-9"),
}

# --- Printed solenoid/flasher table (manual pages 2-46/2-47 locations, 3-5/3-6 wiring; PDF 111-112, 118-120).
SOLENOID_LABELS = {
	1: "Auto Plunger", 2: "Loop Gate", 3: "Right Popper", 4: "Coffin Popper", 5: "Coffin Door",
	6: "Crate Kickout", 7: "Knocker", 8: "Crate Post Power",
	9: "Trough Eject", 10: "Left Sling", 11: "Right Sling", 12: "Center Jet", 13: "Upper Jet",
	14: "Lower Jet", 15: "Upper Slingshot", 16: "Crate Post Hold",
	17: "Top Jet Flasher", 18: "Middle Jet Flasher", 19: "Lower Jet Flasher", 20: "Playfield Bolts",
	21: "Skull Flasher Left", 22: "Upper Right Flasher", 23: "Left Ramp Flasher",
	24: "Center Left Flasher", 25: "Skull Flasher Right", 26: "Center TV",
	27: "Upper Left Flasher", 28: "Center Right Flasher",
	33: "Left Diverter Power", 34: "Left Diverter Hold",
	35: "Lower Left Flasher", 36: "Lower Right Flasher",
	37: "Aux Lamp Clock", 38: "Aux Lamp Data",
	39: "Spider Wheel 1", 40: "Spider Wheel 2",
	45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A",
	30: "WPC J111 General-Purpose State Bit B",
	31: "PinMAME Fast-Flip Game-On State",
	32: "Unused WPC State Channel 32",
	41: "Aux Lamp Clock LPDC Mirror",
	42: "Aux Lamp Data LPDC Mirror",
	43: "Spider Wheel 1 LPDC Mirror",
	44: "Spider Wheel 2 LPDC Mirror",
	49: "PinMAME Simulator Ball-Shooter Channel",
	50: "Reserved WPC Output 50",
}

# Retained VPW script callbacks/handlers, per solenoid address.
SOLENOID_CALLBACKS = {
	1: "AutoPlunge (Gate008.collidable + PlungerIM.AutoFire)", 2: "LoopGate (GateLoop.Open)",
	3: "scoop_right (kicks the ball resting on switch 36)", 4: "CoffinPopper (kicks the ball resting on switch 41)",
	5: "CoffinDoor (CoffinFlipper.RotateToEnd/Start, animates BP_cDoorClose/BP_cDoorOpen)",
	6: "scoop_topleft (kicks the ball resting on switch 37)",
	7: 'vpmSolSound SoundFX("Knocker_1",DOFKnocker),',
	8: "commented out in the retained script ('Not Required, just for initial power surge'); CratePostHold below is the live handler",
	9: "SolRelease (vpmTimer.PulseSw 31; sw32.kick 60,9)",
	16: "CratePostHold (Crate_Pin.Collidable = Not Enabled)",
	17: "SolFlash17 (f17.state)", 18: "SolFlash18 (f18.state)", 19: "SolFlash19 (f19.state)",
	20: "SolFlash20 (f20.state, f20a.state)", 21: "SolFlash21 (f21.state)", 22: "SolFlash22 (f22.state)",
	23: "SolFlash23 (f23.state, f23a.state)", 24: "SolFlash24 (f24.state)", 25: "SolFlash25 (f25.state)",
	26: "SolFlash26 (f26.state)", 27: "SolFlash27 (f27.state)", 28: "SolFlash28 (f28.state)",
	33: "DiverterPower (LockFlipper.RotateToEnd; drives BP_CoffinDiverter via LockFlipper_Animate)",
	34: "DiverterHold (LockFlipper.RotateToStart when neither power nor hold is enabled)",
	35: "SolFlash35 (f35.state)", 36: "SolFlash36 (f36.state)",
	45: "SolRFlipper (core.vbs sLRFlipper)", 47: "SolLFlipper (core.vbs sLLFlipper)",
}

SOLENOID_ASSEMBLIES = {
	1: "A-21022", 2: "A-17796", 3: "A-20716", 4: "A-20717", 5: "A-20717", 6: "A-20788",
	7: "B-10686-1", 8: "A-20850", 9: "A-19963-1", 10: "B-9362-L-4", 11: "B-9362-R-5",
	12: "A-9415-2", 13: "A-9415-2", 14: "A-9415-2", 15: "A-21303", 16: "A-20850",
}
# {control_connection, driver_transistor, power_connection, part_number, printed_type}. Xistor
# readings for 21-24 are best-effort (see manual-transcription.md); they are secondary provenance
# and do not gate address, function, or polarity, all of which are independently confirmed by the
# retained script's SolModCallback table and the Solenoid Locations parts list.
SOLENOID_WIRING = {
	1: dict(power_connection="J133-2", driver_transistor="Q72", control_connection="J116-1", part_number="AE-23-800", printed_type="High Power"),
	2: dict(power_connection="J133-2", driver_transistor="Q68", control_connection="J116-2", part_number="A-14406", printed_type="High Power"),
	3: dict(power_connection="J133-2", driver_transistor="Q71", control_connection="J116-4", part_number="AE-24-900", printed_type="High Power"),
	4: dict(power_connection="J133-2", driver_transistor="Q67", control_connection="J116-5", part_number="AE-23-800", printed_type="High Power"),
	5: dict(power_connection="J133-2", driver_transistor="Q70", control_connection="J116-6", part_number="AE-26-1500", printed_type="High Power"),
	6: dict(power_connection="J133-2", driver_transistor="Q66", control_connection="J116-7", part_number="AE-24-900", printed_type="High Power"),
	7: dict(power_connection="J133-2", driver_transistor="Q69", control_connection="J116-8", part_number="AE-23-800", printed_type="High Power (backbox)"),
	8: dict(power_connection="J133-2", driver_transistor="Q65", control_connection="J116-9", part_number="FL-11629", printed_type="High Power"),
	9: dict(power_connection="J133-3", driver_transistor="Q44", control_connection="J113-1", part_number="AE-26-1500", printed_type="Low Power"),
	10: dict(power_connection="J133-3", driver_transistor="Q48", control_connection="J113-3", part_number="AE-25-1000", printed_type="Low Power"),
	11: dict(power_connection="J133-3", driver_transistor="Q43", control_connection="J113-4", part_number="AE-25-1000", printed_type="Low Power"),
	12: dict(power_connection="J133-3", driver_transistor="Q47", control_connection="J113-5", part_number="AE-26-1200", printed_type="Low Power"),
	13: dict(power_connection="J133-3", driver_transistor="Q42", control_connection="J113-6", part_number="AE-26-1200", printed_type="Low Power"),
	14: dict(power_connection="J133-3", driver_transistor="Q46", control_connection="J113-7", part_number="AE-26-1200", printed_type="Low Power"),
	15: dict(power_connection="J133-3", driver_transistor="Q41", control_connection="J113-8", part_number="AE-26-1200", printed_type="Low Power"),
	16: dict(power_connection="J133-2", driver_transistor="Q45", control_connection="J113-9", part_number="FL-11629", printed_type="Low Power"),
	17: dict(power_connection="J133-6", driver_transistor="Q28", control_connection="J111-1", part_number="24-8802", printed_type="Flasher"),
	18: dict(power_connection="J133-6", driver_transistor="Q32", control_connection="J111-2", part_number="24-8802", printed_type="Flasher"),
	19: dict(power_connection="J133-6", driver_transistor="Q27", control_connection="J111-3", part_number="24-8802", printed_type="Flasher"),
	20: dict(power_connection="J133-6", driver_transistor="Q31", control_connection="J111-4", part_number="24-8704", printed_type="Flasher"),
	21: dict(power_connection="J133-6", driver_transistor="Q25", control_connection="J111-5", part_number="24-8802", printed_type="Flasher"),
	22: dict(power_connection="J133-6", driver_transistor="Q30", control_connection="J111-6", part_number="24-8802", printed_type="Flasher"),
	23: dict(power_connection="J133-6", driver_transistor="Q26", control_connection="J111-7", part_number="24-8802", printed_type="Flasher"),
	24: dict(power_connection="J133-6", driver_transistor="Q29", control_connection="J111-8", part_number="24-8802", printed_type="Flasher"),
	25: dict(power_connection="J133-6", driver_transistor="Q16", control_connection="J109-1", part_number="24-8802", printed_type="Gen. Purpose"),
	26: dict(power_connection="J133-6", driver_transistor="Q15", control_connection="J109-2", part_number="24-8802", printed_type="Gen. Purpose"),
	27: dict(power_connection="J133-6", driver_transistor="Q14", control_connection="J109-3", part_number="24-8802", printed_type="Gen. Purpose"),
	28: dict(power_connection="J133-6", driver_transistor="Q13", control_connection="J109-4", part_number="24-8802", printed_type="Gen. Purpose"),
	33: dict(power_connection="J119-6", driver_transistor="Q84", control_connection="J120-6", part_number="A-20099", printed_type="Fliptronic power (repurposed)"),
	34: dict(power_connection="J119-6", driver_transistor="Q86", control_connection="J120-4", part_number="A-20099", printed_type="Fliptronic hold (repurposed)"),
	35: dict(power_connection="J133-6", driver_transistor="Q81", control_connection="J120-3", part_number="24-8802", printed_type="Fliptronic power (repurposed, DLPDC)"),
	36: dict(power_connection="J133-6", driver_transistor="Q83", control_connection="J120-1", part_number="24-8802", printed_type="Fliptronic hold (repurposed, DLPDC)"),
	37: dict(power_connection="J133-6", control_connection="J110-1", part_number="A-20781", printed_type="Low Power Device Controls"),
	38: dict(power_connection="J133-6", control_connection="J110-3", part_number="A-20781", printed_type="Low Power Device Controls"),
	39: dict(power_connection="J133-6", control_connection="J110-4", part_number="14-8024", printed_type="Low Power Device Controls"),
	40: dict(power_connection="J133-6", control_connection="J110-5", part_number="14-8024", printed_type="Low Power Device Controls"),
	45: dict(power_connection="J119-1", driver_transistor="Q90", control_connection="J120-13", part_number="FL-11629", printed_type="Fliptronic power"),
	46: dict(power_connection="J119-1", driver_transistor="Q92", control_connection="J120-11", part_number="FL-11629", printed_type="Fliptronic hold"),
	47: dict(power_connection="J119-4", driver_transistor="Q87", control_connection="J120-9", part_number="FL-11629", printed_type="Fliptronic power"),
	48: dict(power_connection="J119-4", driver_transistor="Q89", control_connection="J120-7", part_number="FL-11629", printed_type="Fliptronic hold"),
}
FLIPPER_DRIVE_WIRE = {45: "Yel-Grn", 46: "Org-Grn", 47: "Yel-Blu", 48: "Org-Blu", 33: "Yel-Vio", 34: "Org-Vio", 35: "Yel-Gry", 36: "Org-Gry"}

FLASHER_BULBS = {
	17: ("#906 playfield plus a matching backbox flashlamp", 1, 1),
	18: ("#906 playfield plus a matching backbox flashlamp", 1, 1),
	19: ("#906 playfield plus a matching backbox flashlamp", 1, 1),
	20: ("#89 (2) on the playfield", 2, 2),
	21: ("#906 (1) on the playfield", 1, 1),
	22: ("#906 (1) on the playfield", 1, 1),
	23: ("#906 (2) on the playfield", 2, 2),
	24: ("#906 (1) on the playfield", 1, 1),
	25: ("#906 (1) on the playfield", 1, 1),
	26: ("#906 (1) on the playfield", 1, 1),
	27: ("#906 (1) on the playfield", 1, 1),
	28: ("#906 (1) on the playfield", 1, 1),
	35: ("#906 (1) on the playfield", 1, 1),
	36: ("#906 (1) on the playfield", 1, 1),
}

# --- Printed lamp matrix (manual page 2-42 locations, 2-42/2-43 wiring; PDF pages 107-108).
LAMP_LABELS = {
	11: "Stiff Level 7", 12: "Stiff Level 6", 13: "Stiff Level 5", 14: "Stiff Level 4",
	15: "Stiff Level 3", 16: "Stiff Level 2", 17: "Stiff Level 1", 18: "Ramp Left Eye",
	21: "Stiff Level 8", 22: "Stiff Level 9", 23: "Scared Stiff", 24: "Center Leaper",
	25: "Three Bank Lower", 26: "Three Bank Middle", 27: "Three Bank Upper", 28: "Spider Popper",
	31: "Crate Left Eye", 32: "Crate Center Left", 33: "Crate Center Right", 34: "Crate Right Eye",
	35: "Left Outlane", 36: "Right Leaper", 37: "Right Ramp Jackpot", 38: "Light Spin Spider",
	41: "Left Leaper", 42: "Left Ramp Jackpot", 43: "Light Lock", 44: "Ramp Right Eye",
	45: "Right Outlane", 46: "Skill Shot", 47: "Crate Jackpot", 48: "Extra Ball",
	51: "Ramp Item", 52: "Coffin Multiball Item", 53: "Leaper Item", 54: "Coffin Spotlight",
	55: "Shoot Again", 56: "Lock Lamp", 57: "Left Loop Center", 58: "Left Loop Upper",
	61: "Laboratory Item", 62: "Crate Item", 63: "Skull Item", 64: "Web Award 2",
	65: "Web Award 3", 66: "Web Award 4", 67: "Web Award 5", 68: "Web Award 6",
	71: "Web Award 7", 72: "Web Award 8", 73: "Web Award 9", 74: "Web Award 10",
	75: "Web Award 11", 76: "Web Award 12", 77: "Web Award 13", 78: "Web Award 14",
	81: "Web Award 15", 82: "Web Award 16", 83: "Web Award 1", 84: "Left Skull Lane",
	85: "Center Skull Lane", 86: "Right Skull Lane", 87: "Buy In", 88: "Start Button",
}
LAMP_ASSEMBLIES: dict[int, tuple[str | None, str | None]] = {
	11: (None, "#555"), 12: (None, "#555"), 13: (None, "#555"), 14: (None, "#555"),
	15: (None, "#555"), 16: (None, "#555"), 17: (None, "#555"), 18: (None, "#44"),
	21: (None, "#555"), 22: (None, "#555"), 23: (None, "#555"), 24: (None, "#555"),
	25: (None, "#555"), 26: (None, "#555"), 27: (None, "#555"), 28: (None, "#555"),
	31: (None, None), 32: (None, None), 33: (None, None), 34: (None, None),
	35: (None, "#44"), 36: (None, "#555"), 37: (None, "#555"), 38: (None, "#555"),
	41: (None, "#44"), 42: (None, "#44"), 43: (None, "#44"), 44: (None, "#44"),
	45: (None, "#44"), 46: (None, "#44"), 47: (None, "#555"), 48: (None, "#44"),
	51: (None, "#44"), 52: (None, "#44"), 53: (None, "#44"), 54: (None, "#555"),
	55: (None, "#44"), 56: (None, "#555"), 57: (None, "#555"), 58: (None, "#555"),
	61: (None, "#44"), 62: (None, "#44"), 63: (None, "#44"),
	64: (None, "#555"), 65: (None, "#555"), 66: (None, "#555"), 67: (None, "#555"), 68: (None, "#555"),
	71: (None, "#555"), 72: (None, "#555"), 73: (None, "#555"), 74: (None, "#555"),
	75: (None, "#555"), 76: (None, "#555"), 77: (None, "#555"), 78: (None, "#555"),
	81: (None, "#555"), 82: (None, "#555"), 83: (None, "#555"),
	84: (None, "#555"), 85: (None, "#555"), 86: (None, "#555"),
	87: (None, None), 88: (None, None),
}
# Sixteen "Web Award" lamps printed "*Located in backbox" on the Lamp Locations (continued) page,
# corroborated by the retained table's own Light objects for 64-83 sitting at strongly negative
# normalized x (roughly -0.41 to -0.52), i.e. physically placed off the visible playfield.
WEB_AWARD_ADDRESSES = {64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J121-1", "Q96"), 2: ("Yellow-Red", "J121-2", "Q100"),
	3: ("Yellow-Orange", "J121-3", "Q95"), 4: ("Yellow-Black", "J121-4", "Q99"),
	5: ("Yellow-Green", "J121-5", "Q94"), 6: ("Yellow-Blue", "J121-6", "Q98"),
	7: ("Yellow-Violet", "J121-7", "Q93"), 8: ("Yellow-Gray", "J121-9", "Q97"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J125-1", "Q104"), 2: ("Red-Black", "J125-2", "Q108"),
	3: ("Red-Orange", "J125-4", "Q103"), 4: ("Red-Yellow", "J125-5", "Q107"),
	5: ("Red-Green", "J125-6", "Q102"), 6: ("Red-Blue", "J125-7", "Q106"),
	7: ("Red-Violet", "J125-8", "Q101"), 8: ("Red-Gray", "J125-9", "Q105"),
}
# ss.c declares hw.lampCol = 2 (two auxiliary lamp columns, public 91-98 and 101-108), driven by
# a pair of HC4094 shift registers clocked through solenoids 37/38. Unresolved: see conflicts().
AUX_LAMP_ADDRESSES = (91, 92, 93, 94, 95, 96, 97, 98, 101, 102, 103, 104, 105, 106, 107, 108)

GI_STRINGS = {
	0: ("Upper Playfield", "J105-1", "Q5", "J105-7", "#44", True),
	1: ("Center Playfield", "J105-2", "Q4", "J105-8", "#44", True),
	2: ("Lower Playfield", "J105-3", "Q3", "J105-9", "#44", True),
	3: ("Illum String 4", "J106-7", "Q2", "J106-10", "#555", False),
	4: ("Illum String 5", "J106-6", "Q1", "J106-11", "#555", False),
}

# --- Normalized playfield coordinates derived from the retained VPW extraction
# (x/952.941, y/2164.706; review-artifacts/scared-stiff-1996/vpx-geometry.txt).
SWITCH_POSITIONS = {
	16: [(0.05411, 0.791096)], 17: [(0.775698, 0.746812)], 18: [(0.943048, 0.887567)],
	25: [(0.588021, 0.083243)], 26: [(0.138543, 0.748781)], 27: [(0.859789, 0.748969)],
	28: [(0.808822, 0.611665)],
	32: [(0.796216, 0.896386)], 33: [(0.739002, 0.912728)], 34: [(0.682224, 0.928686)], 35: [(0.625447, 0.944836)],
	36: [(0.820753, 0.436861)], 37: [(0.302613, 0.23582)], 38: [(0.310848, 0.195849)],
	41: [(0.102566, 0.516366)], 42: [(0.159093, 0.510944)], 43: [(0.215811, 0.505067)],
	44: [(0.188886, 0.235347)], 45: [(0.747248, 0.330631)], 46: [(0.464471, 0.047249)],
	47: [(0.188697, 0.031976)], 48: [(0.143666, 0.255156)],
	57: [(0.477159, 0.218679)], 58: [(0.063793, 0.1271)],
	61: [(0.144732, 0.562814)], 62: [(0.119102, 0.584636)], 63: [(0.093371, 0.606518)],
	64: [(0.188446, 0.386076)], 65: [(0.350505, 0.35907)], 66: [(0.609215, 0.407142)],
	67: [(0.629276, 0.353667)], 68: [(0.756392, 0.065617)],
	71: [(0.295351, 0.100527)], 72: [(0.386894, 0.100527)], 73: [(0.479717, 0.100366)], 74: [(0.202859, 0.124117)],
	51: [(0.238719, 0.736235)], 52: [(0.675484, 0.736403)], 56: [(0.314102, 0.303318)],
	53: [(0.891316, 0.161243)], 54: [(0.738491, 0.228164)], 55: [(0.891886, 0.294326)],
}
# Switches with no dedicated collision object because the retained script sets their public
# state from another mechanism's own event instead of a discrete playfield sensor.
SWITCH_PROJECTIONS = {
	31: "Projected onto the trough Ball 1 kicker position (switch 32): the retained script's SolRelease handler "
	"(solenoid 9) kicks the ball resting on switch 32 (sw32.kick 60,9) and pulses switch 31 in the same event "
	"(vpmTimer.PulseSw 31); there is no separate Trough Eject collision object.",
}
# switch 12 (Wheel Index) and the two Spider Wheel motor solenoids (39/40) have no playfield
# coordinate; see MECHANISM_SPIDER_WHEEL_NOTE and the not_applicable spatial records below.

SOLENOID_POSITIONS = {
	1: [(0.942193, 0.970734)], 2: [(0.601422, 0.034011)], 3: [(0.820753, 0.436861)],
	4: [(0.102566, 0.516366)], 5: [(0.09205, 0.563001)], 6: [(0.302613, 0.23582)],
	8: [(0.310848, 0.195849)], 9: [(0.796216, 0.896386)],
	10: [(0.238719, 0.736235)], 11: [(0.675484, 0.736403)],
	12: [(0.738491, 0.228164)], 13: [(0.891316, 0.161243)], 14: [(0.891886, 0.294326)],
	15: [(0.314102, 0.303318)], 16: [(0.310848, 0.195849)],
	17: [(0.892178, 0.161619)], 18: [(0.739092, 0.227051)], 19: [(0.892892, 0.294357)],
	20: [(0.411952, 0.814563), (0.49854, 0.814706)],
	21: [(0.828562, 0.001413)], 22: [(0.634771, 0.001468)],
	23: [(0.167063, 0.192096), (0.228315, 0.313971)],
	24: [(0.042939, 0.422852)], 25: [(0.892016, 0.001537)], 26: [(0.455652, 0.668714)],
	27: [(0.092942, 0.001409)], 28: [(0.952983, 0.342466)],
	33: [(0.094605, 0.22731)], 34: [(0.094605, 0.22731)],
	35: [(0.048795, 0.632412)], 36: [(0.878027, 0.639437)],
	45: [(0.625964, 0.844152)], 46: [(0.625964, 0.844152)],
	47: [(0.290104, 0.843323)], 48: [(0.290104, 0.843323)],
}
SOLENOID_PROJECTIONS = {
	5: "Projected onto the coffin-door proxy primitive BM_cDoorClose: the retained script's CoffinFlipper_animate "
	"drives BP_cDoorClose/BP_cDoorOpen from an off-playfield helper Flipper object (CoffinFlipper, negative x), so "
	"the visible door primitive's own position is used instead of the invisible helper's coordinate.",
	8: "Projected onto switch 38 (Crate Entrance): the Crate Post assembly's own primitive (Crate_Pin) sits at local "
	"origin (0,0,0), a meaningless raw mesh coordinate, not a playfield position, so the post is projected onto the "
	"crate mechanism's own entrance opto instead.",
	16: "Projected onto switch 38 (Crate Entrance); see solenoid 8 -- both solenoids actuate the same Crate Post.",
	33: "Projected onto the diverter proxy primitive BM_CoffinDiverter: the retained script's LockFlipper_Animate "
	"drives BP_CoffinDiverter from an off-playfield helper Flipper object (LockFlipper, negative x), so the visible "
	"diverter primitive's own position is used instead of the invisible helper's coordinate.",
	34: "Projected onto the diverter proxy primitive BM_CoffinDiverter; see solenoid 33.",
}

GI_POSITIONS = {
	0: [
		(0.916304, 0.093941), (0.579182, 0.146367), (0.577059, 0.114826), (0.057514, 0.07318),
		(0.855701, 0.070079), (0.762674, 0.040951), (0.686158, 0.022101), (0.192983, 0.016716),
		(0.116333, 0.038919), (0.120814, 0.121799), (0.725645, 0.082265), (0.679885, 0.102488),
		(0.639614, 0.074392), (0.523985, 0.10034), (0.433701, 0.099836), (0.340758, 0.099898),
		(0.2483, 0.10009),
	],
	1: [
		(0.709425, 0.163962), (0.094395, 0.227721), (0.938145, 0.244615), (0.80158, 0.36418),
		(0.733464, 0.372921), (0.718028, 0.341701), (0.038371, 0.389509), (0.05855, 0.415236),
	],
	2: [
		(0.762891, 0.803078), (0.885708, 0.614411), (0.860841, 0.559256), (0.06415, 0.588728),
		(0.098581, 0.558835), (0.721765, 0.727292), (0.688291, 0.765185), (0.695942, 0.822866),
		(0.219649, 0.822024), (0.153477, 0.802604), (0.22671, 0.765304), (0.190396, 0.726404),
	],
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"Scared Stiff retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Scared Stiff extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"Scared Stiff retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"Scared Stiff retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"Scared Stiff retained extraction identity mismatch: "
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
			"locator": "Pinned catalog driver records for the ss_* clone tree",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE,
			"kind": "pinmame_core",
			"uri": "https://github.com/vpinball/pinmame",
			"revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/full/ss.c ssGameData GEN_WPC95 with wpc_dispDMD, the inverted-switch mask "
				"{0x00,0x02,0x00,0xff,0xff,0x00,0x00,0x00,0x00,0x00,0x00,0x00}, FLIP_SW(FLIP_L|FLIP_U)|FLIP_SOL(FLIP_L), "
				"hw.lampCol=2, sw*/s* defines, ss_wheelMech (mech_add(0,&ss_wheelMech): Sol1/Sol2 39/40, MECH_LINEAR|"
				"MECH_CIRCLE|MECH_TWOSTEPSOL|MECH_FAST, 200-step range, home switch swWheelIndex=12 at steps 25-199), "
				"ss_wpc_w's HC4094 aux-lamp shift-register handling on WPC_SOLENOID1/WPC_SOLENOID3, and init_ss's "
				"wpc_set_fastflip_addr(0x81); src/wpc/core.h WPC solenoid numbering and CORE_FIRSTLFLIPSOL=45/"
				"CORE_FIRSTUFLIPSOL=33; src/wpc/core.c core_getSol WPC95 37..40 to 41..44 duplication; src/wpc/wpc.c "
				"WPC_FLIPPERSW95 inversion; src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPC95=0x80"
			),
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE,
			"kind": "human_review",
			"uri": "internal:controllers/pinmame/wpc-95.json",
			"revision": "repository",
			"locator": "WPC-95 public switch, DIP, solenoid, lamp, and five-GI address rules with the Fliptronic and LPDC mirror notes",
			"license": "BSD-3-Clause",
			"attribution": "PinMAME contributors",
		},
		{
			"id": MANUAL_SOURCE,
			"kind": "manual",
			"uri": "external:pinmame-manuals/by-machine/bally.scared-stiff.1996/archive-arcademanual_Scared_Stiff_OPS/Scared_Stiff_OPS.pdf",
			"original_filename": "Scared_Stiff_OPS.pdf",
			"sha256": MANUAL_SHA256,
			"locator": (
				"147-page Bally/Midway Scared Stiff operations manual, part 16-50048-101, September 1996 FINAL "
				"(Internet Archive item arcademanual_Scared_Stiff_OPS). Printed pages 2-42 through 2-47 carry the "
				"lamp/switch/solenoid location parts lists; printed pages 3-2 through 3-10 carry Section 3 Game "
				"Wiring and Schematics, including the Switch Matrix, Lamp Matrix, Solenoid/Flasher Table, and "
				"General Illumination Circuit pages actually used here."
			),
			"license": "NOASSERTION",
			"attribution": "Midway Manufacturing Company; scan hosted by the Internet Archive",
			"rights": "NOASSERTION",
			"excerpts": [
				{
					"id": "excerpt.scared-stiff.switch-matrix",
					"locator": "PDF page 109, printed 2-44, Switch Matrix",
					"path": "evidence/excerpts/bally.scared-stiff.1996/switch-matrix.md",
					"sha256": "0eec1a26e5cb45f0f6ce41c9277b28940ec2f5f672de547c828e16dc1a1490e7",
					"image": "evidence/excerpts/bally.scared-stiff.1996/switch-matrix.webp",
					"image_sha256": "96e775f6db98b723a839cf5dd415d259e66b9df4913b8955af65eb688dcd26d0",
					"image_derivation": "Scared_Stiff_OPS.pdf page 109, crop box 0.06,0.06,0.95,0.51 of the page, rendered at 300 dpi with pdftoppm, reduced to 700px wide grayscale, quality 75 WebP",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.scared-stiff.switch-locations-opto-sweep",
					"locator": "PDF pages 109-110, printed 2-44/2-45, Switch Locations parts list and opto sweep",
					"path": "evidence/excerpts/bally.scared-stiff.1996/switch-locations-opto-sweep.md",
					"sha256": "77d5659cd97d4e78a969249174c14e440acd544a5b5b4cef047e41a5ab243a5b",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.scared-stiff.solenoid-flasher-wiring",
					"locator": "PDF page 2 and PDF pages 118-120, printed 3-5/3-6, Solenoid/Flasher Table",
					"path": "evidence/excerpts/bally.scared-stiff.1996/solenoid-flasher-wiring.md",
					"sha256": "4280ee3062f347f129a1c4da851e4d0b28900ceeb18c5aabb6e168dc98b26fdc",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.scared-stiff.solenoid-flasher-locations",
					"locator": "PDF page 111, printed 2-46, Solenoid Locations parts list",
					"path": "evidence/excerpts/bally.scared-stiff.1996/solenoid-flasher-locations.md",
					"sha256": "4f3555a8b11a8d6afb31d5c37a8875913db7acc6cf3037497b78fb249bfaa1a3",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.scared-stiff.general-illumination",
					"locator": "PDF page 111 (printed 2-46 continuation) and PDF page 123 (printed 3-10), General Illumination",
					"path": "evidence/excerpts/bally.scared-stiff.1996/general-illumination.md",
					"sha256": "6e8d48e90326bb78882516259b3376d34ba5060812255db90f16c14f3839fecb",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
				{
					"id": "excerpt.scared-stiff.lamp-matrix-and-locations",
					"locator": "PDF pages 107-108, printed 2-42/2-43, Lamp Matrix and Lamp Locations",
					"path": "evidence/excerpts/bally.scared-stiff.1996/lamp-matrix-and-locations.md",
					"sha256": "36f653c442f9b77202985f3520b9d00b2b415216707e5566b49af1df9a6c1c64",
					"method": "manual",
					"transcribed_by": "curator, read from the rendered page",
					"reviewed": True,
				},
			],
		},
		{
			"id": MANUAL_SUPPORT_SOURCE,
			"kind": "human_review",
			"uri": "external:pinmame-review-artifacts/scared-stiff-1996/manual-transcription.md",
			"revision": "2026-08-07",
			"sha256": MANUAL_TRANSCRIPTION_SHA256,
			"locator": (
				"Retained human transcription of every rendered manual table used by this definition, produced from "
				"300-600 dpi renders because the retained PDF's own OCR text layer is garbled multi-column output "
				"that is never treated as authoritative. Rendered PNG pages are cached under "
				"external:pinmame-manuals/rendered/bally.scared-stiff.1996/."
			),
			"license": "NOASSERTION",
			"attribution": "pinmame-game-defs curation",
		},
		{
			"id": VPX_TABLE_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/scared-stiff-1996/source/Scared%20Stiff%20%28Bally%201996%29%20VPW%20v1.0.vpx",
			"original_filename": "Scared Stiff (Bally 1996) VPW v1.0.vpx",
			"sha256": TABLE_SHA256,
			"locator": (
				"Retained known-working VPW v1.0 recreation of the physical machine. "
				f"Exact playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH} and "
				f"y/{PLAYFIELD_HEIGHT}. Geometry authority only for named table objects."
			),
			"license": "NOASSERTION",
			"attribution": "VPW",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE,
			"kind": "vpx_script",
			"uri": "external:pinmame-vpx-sources/bally/scared-stiff-1996/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs",
			"sha256": SCRIPT_SHA256,
			"known_working": True,
			"locator": (
				'Retained embedded VPW script (222,402 bytes). Runtime and mechanism-causality authority: '
				'Const cGameName = "SS_15", Const UseSolenoids = 2 (fast flips), Const UseLamps = 1 (built-in VPX '
				"lamp-timer handling via vpmMapLights AllLamps), the SolCallback/SolModCallback tables for solenoids "
				"1-9, 16-28, 33-36, and core.vbs sLRFlipper/sLLFlipper, the cvpmMech mSpider object (Sol1=39, Sol2=40, "
				"Addsw 12, 48 visual steps) driving the pSpider primitive, the GIUpdates2 GI dispatch for GI 0-4, and "
				"the ZBOO Boogie Monsters wobble-physics section (no switch or solenoid binding)."
			),
			"license": "NOASSERTION",
			"attribution": "VPW table authors",
			"rights": "NOASSERTION",
		},
		{
			"id": VPX_EXTRACTION_SOURCE,
			"kind": "vpx_table",
			"uri": "external:pinmame-vpx-sources/bally/scared-stiff-1996/extracted-vpxtool.manifest.json",
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
		"board": "WPC-95 CPU board",
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
				wiring={"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection, "return_component": component},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)

	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = SWITCH_LABELS.get(address)
			unused = label is None
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
			if unused:
				notes += " The printed matrix and the switch-locations parts list both mark this position Not Used."
			elif address in OPTO_SWITCHES:
				pair = SWITCH_PARTS[address][0] or ""
				if "(LED)" in pair:
					notes += (
						" Identified as an opto by the Switch Locations parts list's two-row construction disclosure "
						f"({pair}). PinMAME's ssGameData inverted-switch mask normalizes this address (index/bit match "
						"the printed column/row), so the public switch state is already normalized and must not be "
						"inverted again. Zero disagreement between the manual's opto sweep and PinMAME's mask."
					)
				else:
					notes += (
						" Single-part D-12046 optical home-position sensor for the 200-step Spider Wheel mechanism "
						"(mech_add(0,&ss_wheelMech) in ss.c). PinMAME's ssGameData inverted-switch mask normalizes "
						"this address, so the public switch state is already normalized."
					)
			if address == 24:
				notes += " Physical part 5643-09112-00 is a permanently closed link used to prove the matrix is connected."
			if address == 22:
				notes += " Closed while the coin door is closed."
			if address == 67:
				notes += (
					' The retained script names this address\'s Hit sub "Top Right Rubber Switch" in an inline '
					'comment, and its own table geometry places the object on the right half of the playfield '
					'(normalized x=0.629); the printed Switch Locations label "Left Ramp 10 Point" is used here as '
					"the manual is this project's naming authority for physical parts, but the disagreement is "
					"disclosed rather than silently dropped."
				)
			if address in SWITCH_PROJECTIONS:
				notes += " " + SWITCH_PROJECTIONS[address]
			if address == 12:
				notes += (
					" Mounted inside the Spider Wheel motor assembly, itself a backbox device (see mechanism.spider-"
					"wheel); it has no playfield collision object in the retained extraction."
				)
			physical["notes"] = notes

			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
				"physical": physical,
				"wiring": _switch_wiring(address),
			}
			if unused:
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CONTROLLER_SOURCE)
				label = f"Not Used Matrix Position {address}"
			elif kind == "constant":
				availability = "used"
				extra["constant_active"] = True
				extra["initial_active"] = True
				extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				availability = "optional" if address == 23 else "used"
				extra["normally_closed"] = address in OPTO_SWITCHES
				refs = (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE)
				if address in {13, 14, SLAM_TILT_ADDRESS, 22, 23, 12}:
					role = {
						13: "cabinet.start",
						14: "cabinet.tilt",
						SLAM_TILT_ADDRESS: "cabinet.slam-tilt",
						22: "cabinet.coin-door",
						23: "cabinet.buy-in",
						12: "internal.spider-wheel.index",
					}[address]
					extra["roles"] = [role]
					extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
					physical["location"] = "cabinet" if address in {13, 23} else "cabinet interior"
					if address == 22:
						extra["initial_active"] = True
				else:
					if address in SWITCH_PROJECTIONS:
						position = SWITCH_POSITIONS[32]
						coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE)
					else:
						position = SWITCH_POSITIONS[address]
						coordinate_refs = (VPX_TABLE_SOURCE,)
					extra["spatial"] = located(identifier, "sensor", position, *coordinate_refs)
			items.append(_device(identifier, label, kind, "pinmame.input.switch", address, availability, refs, **extra))

	flipper_inputs = {
		111: ("Lower Right Flipper EOS", "internal.flipper.lower.right.eos", "used", False, "leaf", "SW-1A-194", None),
		112: ("Lower Right Flipper Button", "flipper.lower.right.button", "used", True, "opto", None, "A-17316"),
		113: ("Lower Left Flipper EOS", "internal.flipper.lower.left.eos", "used", False, "leaf", "SW-1A-194", None),
		114: ("Lower Left Flipper Button", "flipper.lower.left.button", "used", True, "opto", None, "A-17316"),
		115: ("Not Used Upper Right Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		116: ("Not Used Upper Right Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
		117: ("Not Used Upper Left Flipper EOS", "internal.unused.flipper", "unused", None, None, None, None),
		118: ("Not Used Upper Left Flipper Button", "internal.unused.flipper", "unused", None, None, None, None),
	}
	for address, (label, role, availability, normally_closed, switch_type, part_number, assembly) in flipper_inputs.items():
		wire, connection = FLIPPER_SWITCH_WIRING[address]
		physical: dict[str, Any] = {"location": "cabinet flipper button" if role.endswith(".button") else "flipper assembly"}
		if switch_type:
			physical["switch_type"] = switch_type
		if part_number:
			physical["part_number"] = part_number
		if assembly:
			physical["assembly_part_number"] = assembly
		notes = f"Printed Fliptronic grounded switch F{address - 110}."
		if availability == "unused":
			notes += (
				" Scared Stiff has no upper flippers. The switch-locations parts list on manual page 2-44 marks "
				"this position Not Used (both assembly and switch part print a blank dash), correcting the "
				"legacy-migrated record, which incorrectly modeled 116/118 as used Upper Right/Left Flipper switches."
			)
			physical["location"] = "not installed"
		else:
			notes += " The matrix-page wiring is drawn as a plain (non-opto) end-of-stroke leaf for the EOS position and a printed opto for the button position."
		physical["notes"] = notes
		extra = {
			"aliases": [
				{"namespace": "pinmame.switch", "value": str(address)},
				{"namespace": "manual.address", "value": f"F{address - 110}"},
			],
			"roles": [role],
			"physical": physical,
		}
		if availability == "used":
			extra["wiring"] = {"board": "WPC-95 CPU board", "drive_wire": wire, "drive_connection": connection}
			extra["normally_closed"] = bool(normally_closed)
			extra["spatial"] = not_applicable(
				"cabinet_or_service" if role.endswith(".button") else "internal_nonvisual",
				MANUAL_SOURCE,
			)
		else:
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		items.append(
			_device(
				f"switch.generic-{address}",
				label,
				"switch",
				"pinmame.input.switch",
				address,
				availability,
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				**extra,
			)
		)

	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}",
				f"CPU DIP {address} (country/option configuration bit)",
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
					"location": "WPC-95 CPU board",
					"switch_type": "dip",
					"notes": (
						"WPC-95 CPU-board country/option configuration DIP bank. The retained transcription of this "
						"manual's Dip Switch Chart (printed page 2) lists only the country jumper pattern, so no "
						"specific per-address ON/OFF combination is asserted here."
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
	for address in range(1, 51):
		if address in SOLENOID_LABELS:
			label = SOLENOID_LABELS[address]
			identifier = output_id(label)
			wiring_data = SOLENOID_WIRING[address]
			kind = "flasher" if 17 <= address <= 28 or address in {35, 36} else "coil"
			if address in {39, 40}:
				kind = "motor"
			if address in {37, 38}:
				kind = "control_signal"
			physical: dict[str, Any] = {}
			part_number = wiring_data.get("part_number")
			if part_number and kind != "flasher":
				physical["part_number"] = part_number
			if address in SOLENOID_ASSEMBLIES:
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			printed_type = wiring_data.get("printed_type", "")
			notes = f"Printed solenoid/flasher table entry {address:02d} ({printed_type})."
			if kind == "flasher" and address in FLASHER_BULBS:
				bulbs, quantity, playfield_emitters = FLASHER_BULBS[address]
				physical["quantity"] = quantity
				notes += f" Printed flashlamp complement: {bulbs}."
			if address in SOLENOID_CALLBACKS:
				notes += f" Retained script callback/driver: {SOLENOID_CALLBACKS[address]}."
			if address in {33, 34}:
				notes += (
					" Printed on the generic WPC-95 Flipper Circuits legend as \"Upr. Rt. Power/Hold\" (coil part "
					"'SEE ABOVE'), but the game-specific Solenoid/Flasher table and ss.c's own #define sLDiverterPower "
					"33 / #define sLDiverterHold 34 both name this the Left Diverter. ssGameData declares "
					"FLIP_SOL(FLIP_L) only (no FLIP_UR/FLIP_UL bit), so core_getSol never routes public 33/34 through "
					"a flipper-coil path; they pass straight through untranslated, the same pattern Tales of the "
					"Arabian Nights established for its own repurposed upper-flipper circuits."
				)
			if address in {35, 36}:
				notes += (
					" Printed on the generic WPC-95 Flipper Circuits legend as \"Upr. Lt. Power/Hold\" (coil part "
					"'SEE ABOVE'), but the game-specific table names these plain Lower Left/Right Flashers driven "
					"through the WPC-95 Low Power Device Controls (DLPDC)."
				)
			if address in {37, 38}:
				notes += (
					" Serial clock/data line for a pair of HC4094 shift registers (ss.c's ss_wpc_w intercepts "
					"WPC_SOLENOID1 bit5/bit4 for data/clock and WPC_SOLENOID3 bit3 for strobe/output-enable) that "
					"feed the driver-declared auxiliary lamp columns (public 91-98, 101-108); it is a data signal, "
					"not a discrete mechanical actuator, so it has no playfield placement of its own. See "
					"conflict.aux-lamp-column-fitment for the unresolved fitment of the lamps it drives."
				)
			if address in {39, 40}:
				notes += (
					" Two-phase stepper drive for the Spider Wheel motor. The retained script's mSpider cvpmMech "
					"object (.Sol1=39, .Sol2=40, .Addsw 12) rotates the pSpider primitive, which sits at a strongly "
					"negative normalized y (behind the playfield's own rear edge) -- consistent with the sixteen "
					"backbox-mounted Web Award lamps this wheel selects among. This is a backbox mechanism, not a "
					"playfield toy; see mechanism.spider-wheel."
				)
			if address in {45, 46, 47, 48}:
				notes += " Fliptronic circuit fed from the +50 V supply; Scared Stiff has no upper flippers, so only the lower-flipper pair (45-48) is fitted."
			physical["notes"] = notes

			wiring: dict[str, Any] = {"board": "WPC-95 power driver board"}
			if "driver_transistor" in wiring_data:
				wiring["driver_transistor"] = wiring_data["driver_transistor"]
			if "control_connection" in wiring_data:
				wiring["control_connection"] = wiring_data["control_connection"]
			if "power_connection" in wiring_data:
				wiring["power_connection"] = wiring_data["power_connection"]
			if address in FLIPPER_DRIVE_WIRE:
				wiring["control_wire"] = FLIPPER_DRIVE_WIRE[address]
			aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
			extra: dict[str, Any] = {"aliases": aliases, "physical": physical, "wiring": wiring}
			availability = "used"
			role = "emitter" if kind == "flasher" else ("effect" if kind in {"motor", "control_signal"} else None)
			if role:
				extra["roles"] = [role]
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in {37, 38, 39, 40}:
				extra["roles"] = ["internal.backbox-mechanism"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_SCRIPT_SOURCE)
			else:
				coordinate_refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) if address in SOLENOID_PROJECTIONS else (VPX_TABLE_SOURCE,)
				extra["spatial"] = located(identifier, role or "effect", SOLENOID_POSITIONS[address], *coordinate_refs)
				if address in SOLENOID_PROJECTIONS:
					physical["notes"] += " " + SOLENOID_PROJECTIONS[address]
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			if address in SOLENOID_CALLBACKS or address in {39, 40}:
				refs = (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
			items.append(_device(identifier, label, kind, "pinmame.output.solenoid", address, availability, refs, **extra))
			continue

		label = VIRTUAL_SOLENOID_LABELS[address]
		identifier = output_id(label)
		availability = "used" if address in {29, 30, 31, 41, 42, 43, 44} else "unused"
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a Scared Stiff playfield device.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a Scared Stiff playfield device.",
			31: "PinMAME's synthetic game-on state. Scared Stiff sets wpc_set_fastflip_addr(0x81), so this channel reflects the ROM's fast-flip flag rather than a physical game-on relay.",
			32: "PinMAME reports this WPC state channel as always zero once a fast-flip address is configured.",
			41: "PinMAME's backward-compatibility mirror of LPDC output 37 (Aux Lamp Clock). It reports the same physical shift-register clock line and is not an additional device.",
			42: "PinMAME's backward-compatibility mirror of LPDC output 38 (Aux Lamp Data); see 41.",
			43: "PinMAME's backward-compatibility mirror of LPDC output 39 (Spider Wheel 1); it reports the same physical motor-phase drive line and is not an additional device.",
			44: "PinMAME's backward-compatibility mirror of LPDC output 40 (Spider Wheel 2); see 43.",
			49: "PinMAME's simulator-only ball-shooter channel; it has no WPC-95 hardware output.",
			50: "Reserved PinMAME output position before the first custom-output boundary. ssGameData declares no custSol.",
		}[address]
		roles = ["internal.duplicate.lpdc-mirror"] if address in {41, 42, 43, 44} else ["internal.unused.wpc-output"]
		if address in {29, 30, 31}:
			roles = ["internal.wpc-state"]
		virtual_aliases = [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}]
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
	return items


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			label = LAMP_LABELS[address]
			identifier = f"lamp.matrix-{address}"
			assembly, bulb = LAMP_ASSEMBLIES[address]
			physical: dict[str, Any] = {"quantity": 1}
			if assembly:
				physical["assembly_part_number"] = assembly
			notes = f"Printed lamp-matrix drive column {column}, return row {row}."
			if bulb:
				notes += f" Printed bulb type {bulb}."
			if address in {31, 32, 33, 34}:
				notes += " Crate-eye insert on the A-21379 Crate LED PCB Assembly; the printed Lamp Locations page shows no separate bulb number for these four inserts."
			if address in WEB_AWARD_ADDRESSES:
				notes += (
					' Printed "*Located in backbox" on the Lamp Locations (continued) page. The retained table\'s '
					"own Light object for this address sits at strongly negative normalized x (outside the 0..1 "
					"playfield), independently corroborating the backbox placement."
				)
			if address in {87, 88}:
				notes += " Cabinet lamp inside the illuminated Buy-In/Start button assembly."
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
					"board": "WPC-95 power driver board",
					"drive_wire": drive_wire,
					"drive_connection": drive_connection,
					"return_wire": return_wire,
					"return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			if address in {87, 88}:
				availability = "used"
				extra["roles"] = ["cabinet.buy-in" if address == 87 else "cabinet.start"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			elif address in WEB_AWARD_ADDRESSES:
				availability = "used"
				extra["roles"] = ["cabinet.insert-panel"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_TABLE_SOURCE)
			else:
				availability = "used"
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

	for address in AUX_LAMP_ADDRESSES:
		column = address // 10 - (7 if address >= 100 else 0)
		row = address % 10
		identifier = f"lamp.aux-{address}"
		items.append(
			_device(
				identifier,
				f"Unresolved Auxiliary Lamp Column {9 if address < 100 else 10} Position {row}",
				"lamp",
				"pinmame.output.lamp",
				address,
				"unknown",
				(CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE),
				aliases=[{"namespace": "pinmame.lamp", "value": str(address)}],
				physical={
					"notes": (
						"ssGameData declares hw.lampCol=2 (two driver-published auxiliary lamp columns beyond the "
						"standard 8x8 matrix), driven through the HC4094 shift registers clocked by solenoids 37/38. "
						"The driver's own comment calls the matching 16-LED board a rev-0.1-prototype part 'not kept "
						"in the production build', but the retained production manual (16-50048-101, Sept. 1996) "
						"still prints solenoids 37/38 with real connectors and wire colors, not NOT USED, and its "
						"Lower Playfield Parts page still lists an A-21287-1 16-LED Skull Driver PCB Assembly. The "
						"retained VPX table implements no Light object at this address (confirmed by an exhaustive "
						"name sweep), and the sixteen-lamp Web Award ring is already fully accounted for on the "
						"ordinary matrix (64-68/71-78/81-83), leaving no obvious gap for this board to fill. See "
						"conflict.aux-lamp-column-fitment; unresolved."
					)
				},
			)
		)
	return items


LAMP_POSITIONS = {
	11: [(0.47048, 0.41102)], 12: [(0.475062, 0.435225)], 13: [(0.479873, 0.459732)],
	14: [(0.484455, 0.484038)], 15: [(0.489037, 0.508141)], 16: [(0.493619, 0.53285)],
	17: [(0.499117, 0.557055)], 18: [(0.1627, 0.227482)],
	21: [(0.466127, 0.387017)], 22: [(0.461316, 0.362509)], 23: [(0.453916, 0.326693)],
	24: [(0.360034, 0.381333)], 25: [(0.14697, 0.621498)], 26: [(0.174286, 0.597053)],
	27: [(0.202499, 0.573003)], 28: [(0.754716, 0.501731)],
	31: [(0.367671, 0.184603)], 32: [(0.41916, 0.179503)], 33: [(0.469362, 0.173553)],
	34: [(0.521495, 0.16732)], 35: [(0.056223, 0.719853)], 36: [(0.591037, 0.427683)],
	37: [(0.65843, 0.458676)], 38: [(0.622999, 0.501562)],
	41: [(0.196445, 0.407788)], 42: [(0.297252, 0.423266)], 43: [(0.330797, 0.486066)],
	44: [(0.22169, 0.218715)], 45: [(0.85776, 0.696275)], 46: [(0.404043, 0.256386)],
	47: [(0.541064, 0.249144)], 48: [(0.63108, 0.201004)],
	51: [(0.633882, 0.690414)], 52: [(0.456041, 0.730745)], 53: [(0.279799, 0.690468)],
	54: [(0.053936, 0.552051)], 55: [(0.455704, 0.868073)], 56: [(0.121994, 0.4057)],
	57: [(0.095982, 0.355367)], 58: [(0.081111, 0.319973)],
	61: [(0.598592, 0.626943)], 62: [(0.454701, 0.602088)], 63: [(0.31412, 0.626975)],
	84: [(0.294449, 0.049957)], 85: [(0.385752, 0.041861)], 86: [(0.478887, 0.050092)],
}


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (label, drive_connection, transistor, power_connection, bulb, dimmable) in GI_STRINGS.items():
		identifier = f"gi.string-{address + 1}"
		notes = f"Printed general-illumination string {address + 1:02d} ({label}); printed bulb type {bulb}."
		notes += (
			" Triac-driven and dimmable (manual General Illumination Circuit Figure #1)." if dimmable
			else " Diode-bridge only, always ON, never brightened or dimmed (manual General Illumination Circuit Figure #2 "
			"and the printed footnote); the retained script's GIUpdates2 independently comments this address "
			'"(Backbox)".'
		)
		extra: dict[str, Any] = {
			"aliases": [
				{"namespace": "pinmame.gi", "value": str(address)},
				{"namespace": "manual.address", "value": f"{address + 1:02d}"},
			],
			"wiring": {
				"board": "WPC-95 power driver board",
				"control_connection": drive_connection,
				"driver_transistor": transistor,
				"power_connection": power_connection,
			},
		}
		physical: dict[str, Any] = {}
		if address in GI_POSITIONS:
			positions = GI_POSITIONS[address]
			physical["quantity"] = len(positions)
			notes += (
				" The manual prints no per-string bulb count, so the physical quantity and every emitter coordinate "
				"come from the retained table's own GI emitter collection for this string (GIUpdates2 in the "
				"retained script: GI 0 drives GI_Upper, GI 1 drives GI_Mid, GI 2 drives GI_Lower)."
			)
			extra["spatial"] = located(identifier, "emitter", positions, VPX_TABLE_SOURCE)
		else:
			notes += (
				" Backbox illumination string; the retained script's GIUpdates2 drives it through a single render-"
				"proxy Light object (lbggi04/lbggi05) at strongly negative normalized x, off the visible playfield, "
				"so this record carries no playfield coordinate."
			)
			extra["roles"] = ["cabinet.insert-panel"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE, VPX_TABLE_SOURCE)
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
			"Four-ball trough and ball release",
			"kicker",
			[output_id("Trough Eject")],
			["switch.matrix-31", "switch.matrix-32", "switch.matrix-33", "switch.matrix-34", "switch.matrix-35"],
			"Four balls rest on trough optos 32-35, with Trough Ball 1 (32) at the eject end nearest the shooter "
			"lane and Trough Ball 4 (35) at the drain entrance. Solenoid 9 ejects the ball resting on 32; the "
			"retained script's SolRelease handler pulses trough-eject opto 31 in the same event (vpmTimer.PulseSw "
			"31; sw32.kick 60,9). All five positions are printed LED/phototransistor optos, normalized by PinMAME's "
			"inverted-switch mask, so a recreation asserts the public switch when a ball is present.",
			[
				("ball-1", "Trough Ball 1 (eject position)", ["switch.matrix-32"], "Ball nearest the eject coil."),
				("ball-2", "Trough Ball 2", ["switch.matrix-33"], "Second trough position."),
				("ball-3", "Trough Ball 3", ["switch.matrix-34"], "Third trough position."),
				("ball-4", "Trough Ball 4 (drain entrance)", ["switch.matrix-35"], "Drain entrance and fourth trough position."),
				("eject", "Trough eject", ["switch.matrix-31"], "Opto pulsed as the ejected ball leaves."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-19963-1",
		),
		mechanism(
			"mechanism.shooter-lane",
			"Shooter lane and auto plunger",
			"kicker",
			[output_id("Auto Plunger")],
			["switch.matrix-18"],
			"The ball ejected from the trough rests on shooter-lane switch 18. Auto-plunger coil 1 launches it; the "
			"retained script's AutoPlunge handler also opens Gate008 (a one-way shooter-lane gate) before firing "
			"PlungerIM.AutoFire. ss.c's ss_handleBallState comments that Scared Stiff has both a manual and an auto "
			"plunger.",
			[("shooter", "Ball in shooter lane", ["switch.matrix-18"], "Shooter-lane switch.")],
			MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE,
			assembly_part_number="A-21022",
		),
		mechanism(
			"mechanism.spider-wheel",
			"Motorized Spider Wheel bonus selector (backbox)",
			"motorized",
			[output_id("Spider Wheel 1"), output_id("Spider Wheel 2")],
			["switch.matrix-12"],
			"A two-phase stepper motor rotates a Spider figure behind a backbox window, matching ss.c's own "
			"mech_add(0,&ss_wheelMech) (solenoids 39/40, MECH_LINEAR|MECH_CIRCLE|MECH_TWOSTEPSOL|MECH_FAST, a "
			"200-count range, and home switch swWheelIndex=12 asserting across steps 25-199). The retained script "
			"independently registers the identical mechanism through its own cvpmMech helper (mSpider: .Sol1=39, "
			".Sol2=40, .Addsw 12, 0, 0; 48 visual steps) and rotates the pSpider primitive, which sits at a strongly "
			"negative normalized y -- behind the playfield's own rear edge -- consistent with the sixteen backbox-"
			"mounted Web Award lamps (64-68/71-78/81-83) this wheel selects among when the player chooses a Spider "
			"Wheel bonus item (ss.c's spiderWheelText array: Collect Deadhead, Jackpot Is Lit, Double Trouble, "
			"Collect Eyeball, Beat The Crate, Coffin Multiball, Telepathetic Power (x2), Laboratory, Boogie Man "
			"Boogie, Crate Multiball, Collect Eyeball, Leaper Mania, Beast Hurry Up, Collect Deadhead (x2)). This is "
			"the machine's only motorized, continuously rotating mechanism; it is a backbox device, not a playfield "
			"toy, and the task brief's characterization of the Crate as \"motorised spinning\" does not match this "
			"or any other primary source -- see mechanism.crate.",
			[],
			CORE_SOURCE, VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
		mechanism(
			"mechanism.crate",
			"Crate ball lock and kickout (not motorized or spinning)",
			"kicker",
			[output_id("Crate Kickout"), output_id("Crate Post Power"), output_id("Crate Post Hold")],
			["switch.matrix-38", "switch.matrix-57"],
			"A ball diverted into the Crate subway trips the entrance opto (switch 38, ss.c's swCrateEntrance) and "
			"comes to rest against a solenoid-held post (solenoids 8/16, CratePostPower/CratePostHold; the retained "
			"script's CratePostHold toggles Crate_Pin.Collidable). Hitting the crate door trips the door sensor "
			"(switch 57, swDoorSensor / \"Crate Sensor\"; ss.c's ball-state table routes stHitCrate through "
			"sCratePostHold into stInsideCrate), and the ball is kicked back out through solenoid 6 (Crate Kickout, "
			"scoop_topleft), sensed leaving on switch 37 (Left Kickout). The retained script's crate_pin_Hit handler "
			"rotates a door primitive (BP_crate_door) a few degrees and back on contact -- a wobble reaction, not a "
			"continuous rotation. Neither ss.c nor the retained script implements any motor or ongoing spin for this "
			"mechanism; it does not match the task brief's \"motorised spinning Crate\" description, and that "
			"framing is not reproduced as fact here (the motorized, spinning mechanism on this machine is the "
			"backbox Spider Wheel -- see mechanism.spider-wheel).",
			[
				("locked", "Ball held against the Crate post", ["switch.matrix-38"], "Crate entrance opto."),
				("door-hit", "Crate door struck", ["switch.matrix-57"], "Crate/door sensor."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20850",
		),
		mechanism(
			"mechanism.coffin",
			"Coffin three-ball lock, door, and popper",
			"kicker",
			[output_id("Coffin Popper"), output_id("Coffin Door")],
			["switch.matrix-41", "switch.matrix-42", "switch.matrix-43", "switch.matrix-48"],
			"A ball enters through the Coffin Entrance opto (switch 48) and travels to a three-position trough "
			"sensed by switches 41 (Left/nearest), 42 (Center), and 43 (Right/deepest) -- ss.c's ball-state table "
			"chains Coffin Right -> Coffin Center -> Coffin Left, with Coffin Left releasing the ball through "
			"solenoid 4 (Coffin Popper, ss.c's sCoffinPopper) into the left inlane. Solenoid 5 (Coffin Door) opens "
			"and closes a door at the entrance; the retained script's CoffinDoor handler rotates an off-playfield "
			"helper object (CoffinFlipper) whose angle drives the visible door primitives (BP_cDoorClose/"
			"BP_cDoorOpen). Locking three balls here starts Coffin Multiball, one of the eight Tales of Terror.",
			[
				("right", "Coffin Right (first ball)", ["switch.matrix-43"], "Deepest trough position."),
				("center", "Coffin Center (second ball)", ["switch.matrix-42"], "Middle trough position."),
				("left", "Coffin Left (third ball, release position)", ["switch.matrix-41"], "Releases through the Coffin Popper."),
				("entrance", "Coffin Entrance", ["switch.matrix-48"], "Entry opto."),
			],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE,
			assembly_part_number="A-20717",
		),
		mechanism(
			"mechanism.left-diverter",
			"Left loop diverter/lock gate",
			"diverter",
			[output_id("Left Diverter Power"), output_id("Left Diverter Hold")],
			["switch.matrix-58"],
			"Solenoids 33/34 (printed on the generic Fliptronic upper-flipper circuit legend, actually game-specific "
			"per ss.c's #define sLDiverterPower 33 / #define sLDiverterHold 34) raise and hold a gate that diverts a "
			"ball from the Left Loop toward the Coffin lock subway instead of continuing around the loop. The "
			"retained script's DiverterPower/DiverterHold handlers rotate an off-playfield helper object "
			"(LockFlipper) whose angle drives the visible diverter primitive (BP_CoffinDiverter).",
			[("open", "Diverter open", ["switch.matrix-58"], "Left Loop switch senses the ball approaching the diverter.")],
			VPX_SCRIPT_SOURCE, CORE_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-20099",
		),
		mechanism(
			"mechanism.loop-gate",
			"Right loop one-way gate",
			"gate",
			[output_id("Loop Gate")],
			[],
			"Solenoid 2 (Loop Gate) opens a one-way gate (the retained script's LoopGate handler sets "
			"GateLoop.Open) admitting a ball into the right loop while blocking return travel. There is no printed "
			"switch dedicated to this gate.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
			assembly_part_number="A-17796",
		),
		mechanism(
			"mechanism.boogie-monsters",
			"Boogie Monster wobble figures (cosmetic, not drop targets)",
			"toy",
			[],
			[],
			"Four small figures (BM_LBoogie01, BM_LBoogie02, BM_RBoggie01, BM_RBoggie02, near the lower inlanes) "
			"wobble when the cabinet is nudged or a slingshot fires. The retained script's ZBOO section implements "
			"this purely as nudge-reactive physics (BoogUpdate/BoogNudge/BoogRandNudge/BoogLSlingNudge/"
			"BoogRSlingNudge driven from NudgeAnim and the slingshot-hit handlers) with no Controller.Switch or "
			"SolCallback binding anywhere in the file. They are not drop targets, do not reset, and have no reset "
			"solenoid. The three standup targets actually wired to switches 61-63 are a separate, unrelated feature "
			"printed \"Three Bank Upper/Middle/Lower\" on every manual page and handled by the retained script's "
			"generic STHit standup routine; this record's mechanism list therefore does not include a Boogie-Men "
			"drop-target bank, correcting the task brief's framing.",
			[],
			VPX_SCRIPT_SOURCE, MANUAL_SOURCE,
		),
	]


def relationships() -> list[dict[str, Any]]:
	return [
		{
			"id": "relationship.trough-eject-opto",
			"kind": "pulse",
			"source": output_id("Trough Eject"),
			"destination": "switch.matrix-31",
			"provenance": provenance(VPX_SCRIPT_SOURCE, MANUAL_SOURCE),
		},
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{
			"id": "conflict.aux-lamp-column-fitment",
			"path": "outputs[binding.device=91,92,93,94,95,96,97,98,101,102,103,104,105,106,107,108]",
			"description": (
				"Pinned ss.c declares core_tGameData.hw.lampCol = 2, publishing two driver-side auxiliary lamp "
				"columns beyond the standard 8x8 matrix at public addresses 91-98 and 101-108, driven through a pair "
				"of HC4094 serial shift registers that ss.c's own ss_wpc_w handler clocks from solenoids 37/38 "
				"(WPC_SOLENOID1 bit5/bit4 for data/clock, WPC_SOLENOID3 bit3 for strobe/output-enable). The driver's "
				"own source comment says the matching '16 LED Skull driver board assembly A-20781' belongs only to "
				"a 'Prototype 0.1' and 'was not kept in production build'. The retained production manual (part "
				"16-50048-101, September 1996 FINAL, 1.5 ROM) disagrees: its Solenoid/Flasher Table still prints "
				"solenoids 37 ('AUX LAMP CLOCK') and 38 ('AUX LAMP DATA') with real J110-1/J110-3 connectors and "
				"Brn-Wht/Org-Wht wire colors, not NOT USED, and its Lower Playfield Parts page still lists item 6, "
				"'A-21287-1 16-LED Skull Driver PCB Assy.', with no not-shown or deleted annotation. Neither source "
				"is preferred by fiat: the driver comment is not self-verifying (a stale driver comment or macro name "
				"is not automatically correct, the same lesson Star Trek: The Next Generation's CORE_CUSTSWNO/"
				"CORE_CUSTSOLNO comments already established), but the retained known-working VPX table also "
				"implements no Light object at any of these sixteen addresses (confirmed by an exhaustive name sweep "
				"of the extraction), and the sixteen-lamp 'Web Award' ring the board's own name suggests is already "
				"fully and exactly accounted for on the ordinary 8x8 matrix (addresses 64-68, 71-78, and 81-83), "
				"leaving no obvious sixteen-lamp gap for a second board to fill. Resolution path: a LibPinMAME "
				"gameplay-harness trace against a legal ss_15 ROM driving solenoids 37/38 and reading lamp addresses "
				"91-98/101-108 directly, or an unrestored machine's own J110 harness photograph/continuity check. "
				"Unresolved."
			),
			"source_refs": [CORE_SOURCE, MANUAL_SOURCE, VPX_SCRIPT_SOURCE],
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
			"id": "bally.scared-stiff.1996",
			"name": "Scared Stiff",
			"manufacturer": "Bally",
			"year": 1996,
			"kind": "physical_pinball",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": ["output_semantics", "spatial_placement", "unresolved_conflicts"],
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
			"platform": "pinmame.wpc-95",
			"hardware_generation": "0x80",
			"inversion_applied_by_emulator": True,
		},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/bally/scared-stiff-1996.md", "status": "partial"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"Scared Stiff device identifiers are not unique: {duplicates}")
	return definition


def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	"""Summarize every spatial disposition so the promotion decision is auditable."""
	located_inputs: list[int] = []
	not_applicable_inputs: dict[str, list[int]] = {}
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		spatial = device.get("spatial")
		if spatial is None:
			continue
		if spatial["status"] == "not_applicable":
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
			continue
		if spatial["status"] == "not_applicable":
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
			"Sixteen driver-declared auxiliary lamp addresses (91-98, 101-108) have no spatial key at all -- the "
			"retained VPX table implements no Light object at any of them, and their fitted status is a genuine, "
			"unresolved two-source disagreement (conflict.aux-lamp-column-fitment). This is the sole reason the "
			"record stays partial; every other spatial dimension this report audits is complete.",
		],
		"coordinate_convention": {
			"space": "playfield",
			"source_bounds": {"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT},
			"x": f"x/{PLAYFIELD_WIDTH}; 0=left, 1=right",
			"y": f"y/{PLAYFIELD_HEIGHT}; 0=rear/backglass, 1=apron/player",
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": "external:pinmame-vpx-sources/bally/scared-stiff-1996/extracted-vpxtool.manifest.json",
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
		"unresolved_outputs": sorted(unresolved_outputs, key=lambda item: (item["group"], item["address"])),
		"projections": [
			{"group": "pinmame.input.switch", "address": address, "reason": reason}
			for address, reason in sorted(SWITCH_PROJECTIONS.items())
		]
		+ [
			{"group": "pinmame.output.solenoid", "address": address, "reason": reason}
			for address, reason in sorted(SOLENOID_PROJECTIONS.items())
		],
		"visual_review_cache": {
			"root": "external:pinmame-manuals/rendered/bally.scared-stiff.1996/",
			"transcription": {
				"path": "external:pinmame-review-artifacts/scared-stiff-1996/manual-transcription.md",
				"sha256": MANUAL_TRANSCRIPTION_SHA256,
			},
		},
		"excluded_object_classes": [
			"CoffinFlipper/LockFlipper off-playfield helper Flipper objects (negative normalized x) -- their own "
			"coordinate is a physics-helper position, not a device location; solenoids 5/33/34 project onto the "
			"visible door/diverter primitive their animation drives instead.",
			"Crate_Pin local-origin Primitive mesh (0,0,0) -- not a coordinate; solenoids 8/16 project onto the "
			"crate mechanism's own entrance opto (switch 38) instead.",
			"pSpider primitive (negative normalized y, behind the playfield rear edge) -- a backbox mechanism "
			"proxy; solenoids 39/40 and switch 12 take a controlled cabinet_or_service record instead of this "
			"off-board coordinate.",
			"RampTrigger1-6 and TriggerLF/TriggerRF physics-only Trigger objects -- confirmed by their own script "
			"handlers to carry no Controller.Switch binding (wire-ramp detection and flipper live-catch timing "
			"helpers only).",
		],
		"unresolved": [
			{
				"group": "pinmame.output.lamp",
				"addresses": list(AUX_LAMP_ADDRESSES),
				"reason": "conflict.aux-lamp-column-fitment; no spatial key recorded (schema has no third spatial status for this case).",
			}
		],
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# Scared Stiff (Bally, 1996) spatial review",
		"",
		f"Status: {report['status']}. Every spatial dimension audited here is complete except the sixteen "
		"driver-declared auxiliary lamp addresses (91-98, 101-108), which carry no spatial key at all because "
		"their fitted status is itself unresolved (see the promotion decision below).",
		"",
		"The matching source is the retained known-working `Scared Stiff (Bally 1996) VPW v1.0.vpx` at SHA-256 "
		f"`{TABLE_SHA256}`. The retained `vpxtool git:v0.33.3` extraction produced the embedded script at SHA-256 "
		f"`{SCRIPT_SHA256}`; that embedded stream is the runtime and causality authority. Exact playfield bounds are "
		f"`{TABLE_BOUNDS}`, and every canonical coordinate is x/{PLAYFIELD_WIDTH} and y/{PLAYFIELD_HEIGHT} rounded to "
		"at most six fractional places.",
		"",
		"## Evidence decisions",
		"",
		"- The embedded VPW script is the runtime address and causality authority; the Bally/Midway operations "
		"manual is the physical inventory, quantity, polarity, and wiring authority; pinned PinMAME owns controller "
		"topology; the retained table supplies geometry.",
		"- The retained manual PDF has a real but badly garbled multi-column OCR text layer for its Section 2/3 "
		"tables (unlike Monster Bash's fully image-only scan); every printed table used here was still read from "
		"rendered 300-600 dpi pages and transcribed into "
		"`external:pinmame-review-artifacts/scared-stiff-1996/manual-transcription.md`, never trusted from "
		"`pdftotext` alone.",
		"- The switch-matrix page's own opto legend (a small box, 'OPTO, TYPICALLY CLOSED') shades zero cells on "
		"this manual, unlike Monster Bash's. Opto identity instead comes from the Switch Locations parts list's own "
		"two-row `(LED)` + `(Trans.)` construction disclosure, swept exhaustively; it produced exactly the same "
		"17-address set PinMAME's own inverted-switch mask normalizes, with zero disagreement.",
		"- Switch 31 (Trough Eject) and solenoids 5/8/16/33/34 have no dedicated collision object because the "
		"retained script sets their public state, or animates their visible proxy, from another object's own event "
		"or rotation angle rather than from a Hit/Trigger event on a coordinate of their own. Those addresses are "
		"explicit documented projections onto the real table object that carries the underlying mechanism state.",
		"- Sixteen 'Web Award' lamps (64-68, 71-78, 81-83) and general-illumination strings 3/4 are backbox devices: "
		"the manual's own `*Located in backbox` annotation and the retained table's strongly negative normalized-x "
		"Light-object coordinates agree independently, so they take a controlled `cabinet_or_service` record rather "
		"than a fabricated playfield position.",
		"- Switch 12 (Wheel Index) and solenoids 39/40 (Spider Wheel motor) are part of a backbox mechanism -- the "
		"rotated `pSpider` primitive sits at a strongly negative normalized y, behind the playfield's own rear edge "
		"-- and take a controlled `cabinet_or_service` record for the same reason.",
		"- Solenoids 41-44 are PinMAME's LPDC mirrors of physical drive lines 37-40 (aux lamp clock/data, Spider "
		"Wheel motor phases) and are declared virtual with a `virtual` spatial record so no duplicate device is ever "
		"placed on the playfield.",
		"- The 128x32 DMD is backbox hardware, so its spatial record is a controlled `not_applicable` with both "
		"PinMAME core and manual provenance.",
		"- Flasher addresses 21, 22, 25, and 27 sit at normalized y between 0.0014 and 0.0015 -- within the y<0.005 "
		"band this project treats as a required manual check before recording a placement. Each is the sole, "
		"non-suffixed Light object at its address (not a duplicate/halo variant), the manual's printed table shows "
		"a single Playfield-only flashlamp part for each (no Backbox pairing, unlike addresses 17-19 which do print "
		"a Backbox part alongside Playfield), and neighboring Skull Lane switches/lamps independently cluster at a "
		"similarly low y -- consistent with real flasher domes mounted at the very top of the playfield, not a "
		"back-panel render proxy of the kind Monster Bash and Theatre of Magic both found at y=0.000. Kept as "
		"validated placements with this reasoning disclosed.",
		"",
		"## Explicit projections",
		"",
	]
	for entry in report["projections"]:
		lines.append(f"- {entry['group'].rsplit('.', 1)[-1].capitalize()} {entry['address']}: {entry['reason']}")
	lines += [
		"",
		"## Counts",
		"",
		f"- Placements: {report['placement_count']}",
		f"- Located input addresses: {len(report['resolved_input_addresses'])}",
		f"- Located output bindings: {len(report['resolved_output_bindings'])}",
		f"- Outputs with no spatial key at all (unresolved fitment): {len(report['unresolved_outputs'])}",
	]
	for reason, addresses in report["not_applicable_inputs"].items():
		lines.append(f"- Inputs with a controlled `{reason}` record: {len(addresses)}")
	for reason, bindings in report["not_applicable_outputs"].items():
		lines.append(f"- Outputs with a controlled `{reason}` record: {len(bindings)}")
	lines += [
		"",
		"## Promotion decision",
		"",
		"No authoring-critical placement, quantity, or semantic question remains unresolved for any address this "
		"audit could resolve, and the deterministic curator reproduces the canonical artifact and its pinned seed "
		"byte-for-byte. However, sixteen driver-declared auxiliary lamp addresses (91-98, 101-108) remain genuinely "
		"unresolved: pinned PinMAME's ss.c declares them (hw.lampCol=2) and the retained production manual still "
		"prints their driving solenoids (37/38) as wired with real connectors, while the driver's own source "
		"comment calls the matching board a deleted prototype-only part, and the retained known-working VPX table "
		"implements no Light object at any of the sixteen addresses -- recorded as "
		"`conflict.aux-lamp-column-fitment`, unresolved. The definition therefore carries a non-empty `conflicts` "
		"array, `coverage.dimensions.semantic_naming = \"conflicted\"`, and sixteen output records with `availability: "
		"\"unknown\"` and no `spatial` key at all, so promotion to `author_ready` is refused; the record stays "
		"`partial` with `coverage.missing = [\"output_semantics\", \"spatial_placement\", \"unresolved_conflicts\"]` "
		"until a LibPinMAME harness trace against a legal `ss_15` ROM, or a physical machine's own J110 harness "
		"inspection, settles what (if anything) is fitted there.",
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
	return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
	definition_path = root / DEFINITION_PATH.relative_to(ROOT)
	seed_path = root / SEED_PATH.relative_to(ROOT)
	if not definition_path.is_file():
		raise RuntimeError(f"Scared Stiff definition is missing: {definition_path}")
	if not seed_path.is_file():
		raise RuntimeError(f"Scared Stiff seed is missing: {seed_path}")
	definition = build()
	expected = canonical_bytes(definition)
	if definition_path.read_bytes() != expected:
		raise RuntimeError(f"Scared Stiff definition drifted from its deterministic curator: {definition_path}")
	if seed_path.read_bytes() != expected:
		raise RuntimeError(f"Scared Stiff seed is not byte-identical to the promoted definition: {seed_path}")
	report = build_spatial_report(definition)
	report_path = root / SPATIAL_REPORT_PATH.relative_to(ROOT)
	markdown_path = root / SPATIAL_REPORT_MARKDOWN_PATH.relative_to(ROOT)
	if not report_path.is_file() or report_path.read_bytes() != canonical_bytes(report):
		raise RuntimeError(f"Scared Stiff spatial audit drifted from its deterministic curator: {report_path}")
	if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != render_spatial_report(report):
		raise RuntimeError(f"Scared Stiff spatial review drifted from its deterministic curator: {markdown_path}")
	print("Scared Stiff definition, seed, and spatial audit match the deterministic curator.")


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
		print(f"Scared Stiff extraction manifest written: {write_extraction_manifest(source_root)}")
	elif args.verify_extraction:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		verify_extraction_manifest(source_root)
		print("Scared Stiff retained extraction matches its pinned manifest identity.")
	elif args.check:
		check(ROOT)
	elif args.regenerate:
		print(f"Wrote {generate(ROOT)}")
	else:
		raise AssertionError("unreachable")


if __name__ == "__main__":
	main()
