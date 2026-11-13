"""Curate the physical Williams No Fear: Dangerous Sports (1995) machine definition.

The builder is side-effect free and deterministic: it embeds every reviewed label, wiring detail and runtime-derived fact
as a literal, so regeneration reproduces the canonical artifact byte-for-byte without reading the external evidence roots.
``--check`` refuses drift, and ``--regenerate`` is the only path that writes the definition, its knowledge note and its
spatial report.
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

MACHINE_ID = "williams.no-fear-dangerous-sports.1995"
PARTIAL_PATH = ROOT / "machines/partial/williams/no-fear-dangerous-sports-1995.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/no-fear-dangerous-sports-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/no-fear-dangerous-sports-1995.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/williams/no-fear-dangerous-sports-1995.md"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/williams/no-fear-dangerous-sports-1995.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams/no-fear-dangerous-sports-1995.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/williams/no-fear-dangerous-sports-1995-spatial.json"
LEGACY_ALIAS_SEED_PATH = ROOT / "tools/seeds/williams/no-fear-dangerous-sports-1995-legacy-aliases.json"

PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-security"
IDENTITY_SOURCE = "identity.williams.no-fear-dangerous-sports.1995"
MANUAL_SOURCE = "manual.williams.no-fear-dangerous-sports.1995"
EDGES_SOURCE = "runtime.no-fear.switch-edges"
SOLENOID_TEST_SOURCE = "runtime.no-fear.solenoid-test"
FLASHER_TEST_SOURCE = "runtime.no-fear.flasher-names"
FLIPPER_TEST_SOURCE = "runtime.no-fear.flipper-coil-test"
GI_TEST_SOURCE = "runtime.no-fear.gi-test"
LAMP_TEST_SOURCE = "runtime.no-fear.single-lamps"
ACCELERATOR_SOURCE = "runtime.no-fear.ball-accelerator-test"
TROUGH_TEST_SOURCE = "runtime.no-fear.underground-trough-test"
SKULL_TEST_SOURCE = "runtime.no-fear.skull-test"
# The earlier flasher run that settled solenoid 19's legacy label conflict (tools/settle_legacy_label_conflicts.py).
FLASHER_HISTORY_SOURCE = "runtime.no-fear.nf-23x.flasher-test"
FLASHER_HISTORY_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
FLASHER_HISTORY_SHA256 = "4a02e69ca499c4db30b2e7c4a4501f4339a1bc71204cc940e84ee396f1e06ba5"
EVIDENCE_DIRECTORY = "evidence/runtime/wpc-security"
VPX_TABLE_SOURCE = "vpx-table.no-fear-vpw-1-1-1"
VPX_SCRIPT_SOURCE = "vpx-script.no-fear-vpw-1-1-1"
VPX_EXTRACTION_SOURCE = "vpx-extraction.no-fear-vpw-1-1-1"

TABLE_NAME = "No Fear (Williams 1995) VPW v1.1.1.vpx"
TABLE_SHA256 = "3523285c6829c44068f8d81c5d886af8ab89156ed0e5aac18fbcfbf7a918d14f"
SCRIPT_SHA256 = "580749d770efe2e887fd92f7d05b3afa7f848f64e9f2736204986353b00817c5"
PLAYFIELD_WIDTH = 964.0
PLAYFIELD_HEIGHT = 2162.0
TABLE_BOUNDS = "left=0 top=0 right=964 bottom=2162"
EXTRACTION_FILE_COUNT = 1703
EXTRACTION_TOTAL_BYTES = 454347325
EXTRACTION_MANIFEST_SHA256 = "a5595fa7a8200924cf77ff843d6f6c88d21b3d8acb5a53e4198b9c84544264a9"
EXTRACTION_RELATIVE_PATH = Path("williams/no-fear-dangerous-sports-1995/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/no-fear-dangerous-sports-1995/extracted-vpxtool.manifest.json")
VPX_SOURCE_DIRECTORY = "pinmame-vpx-sources/williams/no-fear-dangerous-sports-1995"

MANUAL_NAME = "Williams_1995_No_Fear_Dangerous_Sports_English_Manual.pdf"
MANUAL_SHA256 = "176d5c887bf89ca35c0a6d558a757a1939da7145814f477ce099a16d50e2752b"
IPDB_PAGE_SHA256 = "7c61e99631fd3342007cb3358c08d2085735cc438b7649461c08e50075baf3b8"
MANUALS_DIRECTORY = "pinmame-manuals/by-machine/williams.no-fear-dangerous-sports.1995/ipdb"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=2852"
ACQUIRED_AT = "2026-11-13T14:17:00Z"
IPDB_PAGE_ACQUIRED_AT = "2026-11-13T15:19:00Z"
RIGHTS_NOTE = "Williams Electronics Games, Inc.; scan hosted by the Internet Pinball Machine Database"
TABLE_ATTRIBUTION = "VPW (Sixtoe, Kevv, Tomate, Apophis and others), after Ninuzzu's original table"

EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID

SWITCH_GROUP = "pinmame.input.switch"
DIP_GROUP = "pinmame.input.dip"
SOLENOID_GROUP = "pinmame.output.solenoid"
LAMP_GROUP = "pinmame.output.lamp"
GI_GROUP = "pinmame.output.gi"

# --- Drivers -----------------------------------------------------------------------------------------
DRIVER_IDS = ("nf_23x", "nf_23", "nf_23f", "nf_22", "nf_20", "nf_11x", "nf_10f", "nf_101", "nf_08x")
SAME_MAP = " Pinned nf.c declares it on wpc_mSecurityS with the same nfGameData I/O map as nf_23x."
S11 = " with the S1.1 sound ROMs (U2 nfu2s, which pinned nf.c comments as L-2, and nfu3s-nfu7s)"
S10 = " with the S1.0 sound set (U2 SND-U2.SL1 and nfu3s-nfu7s)"
DRIVER_COMPATIBILITY = {
	"nf_23x": ("identical", "Game ROM 2.3X Export (nofe2_3x.rom)" + S11 + ", the parent driver; it identifies itself as NO FEAR PINBALL / 50025 REV. 2.3 X and every service-test run behind this definition booted it."),
	"nf_23": ("identical", "Game ROM 2.3 (nofe2_3.rom)" + S11 + "." + SAME_MAP),
	"nf_23f": ("identical", "Game ROM 2.3F, the French build (nofe2_3f.rom)" + S11 + "." + SAME_MAP),
	"nf_22": ("identical", "Game ROM 2.2 (nofe2_2a.rom)" + S11 + "." + SAME_MAP),
	"nf_20": ("identical", "Game ROM 2.0 (nofe2_0a.rom)" + S11 + "." + SAME_MAP),
	"nf_11x": ("identical", "Game ROM 1.1X Export (nofe1_1x.rom)" + S11 + "." + SAME_MAP),
	"nf_10f": ("identical", "Game ROM 1.0F, the French build (nofe1_0.rom)" + S10 + "; pinned nf.c notes that the revision history names the SL-1 sound ROM's checksum for game revision 1.0." + SAME_MAP),
	"nf_101": ("identical", "Game ROM 1.01F (nofe1_01.rom), which pinned nf.c names the LED Ghost Fix of the French 1.0 build: it changes lamp-matrix timing against LED ghosting and no controller address or playfield device" + S10 + "." + SAME_MAP),
	"nf_08x": ("unknown", "Game ROM 0.8X Export Prototype (nofe0_8x.rom)" + S10 + "; pinned nf.c notes that at least one 0.8x machine carried the SL-1 sound ROM." + SAME_MAP + " No retained source says what playfield or hardware this prototype ROM was built for, so its physical compatibility stays unknown."),
}

# --- Switch data (switch-matrix.md, switch-locations.md, opto-boards.md) ----------------------------------
# address -> (switch part cell, printed description) from the Switch Locations list (2-37).
SWITCH_LOCATIONS = {
	11: ("20-9663-B-8", "Ball Launch"), 13: ("20-9663-1", "Start Button"), 14: ("A-15361", "Plumb Bob Tilt*"),
	15: ("A-18973", "Shooter Lane"), 16: ("5647-12693-24", "Spinner"), 17: ("5647-12693-19", "Right Outlane"),
	18: ("5647-12693-19", "Right Return"), 21: ("A-17238", "Slam Tilt*"), 22: ("5643-09268-00", "Coin Door Closed*"),
	23: ("20-9663-18", "Buy Extra Ball"), 24: ("5643-09112-00", "Always Closed*"), 25: ("5647-12693-19", "Kickback"),
	26: ("5647-12693-19", "Left Return"), 27: ("A-17800 (Kick) / A-17794 (Score)", "Left Slingshot"),
	28: ("A-17800 (Kick) / A-17794 (Score)", "Right Slingshot"),
	31: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough Stack"), 32: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 1 (Right)"),
	33: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 2"), 34: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 3"),
	35: ("A-18617-1 (LED) / A-18618-1 (Trans.)", "Trough 4"), 37: ("A-16908 (LED) / A-16909 (Trans.)", "Center Trough Enter"),
	38: ("A-16908 (LED) / A-16909 (Trans.)", "Left Trough Enter"), 41: ("A-16908 (LED) / A-16909 (Trans.)", "Right Popper 1"),
	42: ("A-16908 (LED) / A-16909 (Trans.)", "Right Popper 2"), 46: ("A-16908 (LED) / A-16909 (Trans.)", "Left Magnet"),
	47: ("A-16908 (LED) / A-16909 (Trans.)", "Center Magnet"), 48: ("A-16908 (LED) / A-16909 (Trans.)", "Right Magnet"),
	51: ("5647-12693-31", "Drop Target"), 54: ("5647-12693-13", "Left Wireform"), 55: ("5647-12693-19", "Inner Loop"),
	56: ("SW-1A-170-15", "Light Kickback Bottom"), 57: ("SW-1A-170-15", "Light Kickback Top"), 58: ("5647-12693-19", "Right Loop"),
	61: ("5647-12133-11", "Eject Hole"), 62: ("5647-12693-19", "Left Loop"), 63: ("5647-12693-24", "Left Ramp Enter"),
	64: ("5647-12693-11", "Left Ramp Middle"), 66: ("5647-12693-24", "Right Ramp Enter"), 67: ("5647-12693-11", "Right Ramp Exit"),
}
SWITCH_LABELS = {
	11: "Ball Launch", 13: "Start Button", 14: "Plumb Bob Tilt", 15: "Shooter Lane", 16: "Spinner", 17: "Right Outlane",
	18: "Right Return", 21: "Slam Tilt", 22: "Coin Door Closed", 23: "Buy Extra Ball", 24: "Always Closed", 25: "Kickback",
	26: "Left Return", 27: "Left Slingshot", 28: "Right Slingshot", 31: "Trough Stack", 32: "Trough 1 (Right)", 33: "Trough 2",
	34: "Trough 3", 35: "Trough 4", 37: "Center Trough Enter", 38: "Left Trough Enter", 41: "Right Popper 1", 42: "Right Popper 2",
	46: "Left Magnet Opto", 47: "Center Magnet Opto", 48: "Right Magnet Opto", 51: "Drop Target", 54: "Left Wireform",
	55: "Inner Loop", 56: "Light Kickback Bottom", 57: "Light Kickback Top", 58: "Right Loop", 61: "Eject Hole", 62: "Left Loop",
	63: "Left Ramp Enter", 64: "Left Ramp Middle", 66: "Right Ramp Enter", 67: "Right Ramp Exit",
}
SWITCH_TYPES = {
	11: "button", 13: "button", 14: "tilt", 15: "other", 16: "microswitch", 17: "microswitch", 18: "microswitch", 21: "tilt",
	22: "microswitch", 23: "button", 24: "other", 25: "microswitch", 26: "microswitch", 27: "leaf", 28: "leaf", 31: "opto",
	32: "opto", 33: "opto", 34: "opto", 35: "opto", 37: "opto", 38: "opto", 41: "opto", 42: "opto", 46: "opto", 47: "opto",
	48: "opto", 51: "microswitch", 54: "microswitch", 55: "microswitch", 56: "other", 57: "other", 58: "microswitch",
	61: "microswitch", 62: "microswitch", 63: "microswitch", 64: "microswitch", 66: "microswitch", 67: "microswitch",
}
SWITCH_ROLES = {11: "cabinet.launch", 13: "cabinet.start", 14: "cabinet.tilt", 21: "cabinet.slam-tilt", 22: "cabinet.coin-door", 23: "cabinet.buy-in"}
SWITCH_LOCATIONS_TEXT = {11: "cabinet front", 13: "cabinet front", 14: "cabinet interior", 21: "coin door", 22: "coin door", 23: "cabinet front"}
# Positions the matrix and the list print NOT USED and the ROM's T.1 shows as UNUSED, and the columns T.1 never reports.
UNUSED_NAMED = frozenset({12, 36, 43, 44, 45, 52, 53, 65, 68})
UNSCANNED = frozenset(column * 10 + row for column in (7, 8) for row in range(1, 9))
UNUSED_MATRIX_ADDRESSES = UNUSED_NAMED | UNSCANNED
# PinMAME's nfGameData invSw {0x00,0x00,0x00,0xff,0xe3,0x00,...} inverts these public addresses through wpc_sw2m
# (core_setSw indexes invSw by wpc_sw2m(no)/8); the test recomputes the set from the mask.
MASKED_SWITCHES = frozenset({31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 46, 47, 48})
# Cells the matrix page shades "Opto, Typically Closed" (switch-matrix.md): all of columns 3 and 4, and F2, F4, F6, F8.
SHADED_SWITCHES = frozenset(set(range(31, 39)) | set(range(41, 49)) | {112, 114, 116, 118})
# The ROM's own T.1 names (switch-edges run).
ROM_SWITCH_NAMES = {
	11: "BALL LAUNCH", 13: "START BUTTON", 14: "PLUMB BOB TILT", 15: "SHOOTER LANE", 16: "SPINNER", 17: "RIGHT OUTLANE",
	18: "RIGHT RETURN", 21: "SLAM TILT", 23: "BUY EXTRA BALL", 24: "ALWAYS CLOSED", 25: "KICKBACK", 26: "LEFT RETURN",
	27: "LEFT SLINGSHOT", 28: "RIGHT SLINGSHOT", 31: "TROUGH STACK", 32: "TROUGH 1 (RIGHT)", 33: "TROUGH 2", 34: "TROUGH 3",
	35: "TROUGH 4", 37: "CENTER TR. ENTR.", 38: "LEFT TR. ENTR.", 41: "RIGHT POPPER 1", 42: "RIGHT POPPER 2",
	46: "LEFT MAGNET", 47: "CENTER MAGNET", 48: "RIGHT MAGNET", 51: "DROP TARGET", 54: "LEFT WIREFORM", 55: "INNER LOOP",
	56: "LIGHT KB. BOTTOM", 57: "LIGHT KB. TOP", 58: "RIGHT LOOP", 61: "EJECT HOLE", 62: "LEFT LOOP", 63: "LEFT RAMP ENTER",
	64: "LEFT RMP. MIDDLE", 66: "RIGHT RMP. ENTER", 67: "RIGHT RAMP EXIT",
}
# Switches whose closure makes the ROM fire their own coil even inside T.1 (switch-edges run).
SWITCH_FIRES = {27: 11, 28: 10}
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
# Dedicated switches (switch-matrix.md: the matrix column and the DEDICATED SWITCHES drawing 3-3): wire, CPU pin, coin door J1 and J3 pins.
DEDICATED_SWITCH_WIRING = {
	1: ("Orange-Brown", "J205-1", "J1-14", "J3-4"), 2: ("Orange-Red", "J205-2", "J1-13", "J3-5"), 3: ("Orange-Black", "J205-3", "J1-12", "J3-6"),
	4: ("Orange-Yellow", "J205-4", "J1-17", None), 5: ("Orange-Green", "J205-6", "J1-11", "J3-7"), 6: ("Orange-Blue", "J205-7", "J1-10", "J3-8"),
	7: ("Orange-Violet", "J205-8", "J1-8", "J3-9"), 8: ("Orange-Gray", "J205-9", "J1-9", "J3-11"),
}
DEDICATED_SWITCH_LABELS = {
	1: ("Left Coin Chute", "cabinet.coin.1", "Left coin chute."),
	2: ("Center Coin Chute", "cabinet.coin.2", "Center coin chute."),
	3: ("Right Coin Chute", "cabinet.coin.3", "Right coin chute."),
	4: ("4th Coin Chute", "cabinet.coin.4", "Fourth coin chute."),
	5: ("Service Credit / Escape", "service.escape", "Adds a service credit in normal play and acts as Escape inside the menu system."),
	6: ("Volume Down / Down", "service.down", "Lowers the volume in normal play and acts as Down inside the menu system."),
	7: ("Volume Up / Up", "service.up", "Raises the volume in normal play and acts as Up inside the menu system."),
	8: ("Begin Test / Enter", "service.enter", "Enters the menu system in normal play and acts as Enter inside the menu system."),
}
# Opto boards behind the shaded switches (opto-boards.md): address -> board sentence.
_TROUGH = "of the Trough IR LED board A-18617-1 and the Trough IR Photo Transistor board A-18618-1"
_SINGLE = "an LED Board A-16908 and Photo Transistor Board A-16909 pair"
OPTO_BOARDS = {
	31: f"position JAM BALL {_TROUGH} (LED1 on J1-7, photo transistor Q1 on J1-3), wired to the 16-Opto Switch Board A-16998.1 at J1-9 and J2-10",
	32: f"position BALL 1 {_TROUGH} (LED2 on J1-6, Q2 on J1-4), wired to the 16-Opto Switch Board at J1-7 and J2-9",
	33: f"position BALL 2 {_TROUGH} (LED3 on J1-5, Q3 on J1-5), wired to the 16-Opto Switch Board at J1-6 and J2-8",
	34: f"position BALL 3 {_TROUGH} (LED4 on J1-4, Q4 on J1-6), wired to the 16-Opto Switch Board at J1-5 and J2-7",
	35: f"position BALL 4 {_TROUGH} (LED5 on J1-3, Q5 on J1-7), wired to the 16-Opto Switch Board at J1-4 and J2-6",
	37: f"{_SINGLE} wired to the 16-Opto Switch Board at J1-2 and J2-3",
	38: f"{_SINGLE} wired to the 16-Opto Switch Board at J1-1 and J2-2",
	41: f"{_SINGLE} in the Ball Popper Assembly A-19965 (which carries two pairs), wired to the 16-Opto Switch Board at J3-3 and J4-2",
	42: f"{_SINGLE} in the Ball Popper Assembly A-19965, wired to the 16-Opto Switch Board at J3-4 and J4-3",
	46: f"{_SINGLE} on the left Opto Mounting Bracket A-20034 of the Back Panel Assembly A-20033, wired to the 16-Opto Switch Board at J3-8 and J4-8 (printed 'SW. #46 RAMP LEFT MAGNET')",
	47: f"{_SINGLE} on the centre Opto Mounting Bracket A-20034, wired to the 16-Opto Switch Board at J3-9 and J4-9 (printed 'SW. #47 RAMP CENTER MAGNET')",
	48: f"{_SINGLE} on the right Opto Mounting Bracket A-20034, wired to the 16-Opto Switch Board at J3-10 and J4-10 (printed 'SW. #48 RAMP RIGHT MAGNET')",
}


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
		raise RuntimeError(f"No Fear retained extraction is missing: {extraction_root}")
	paths = sorted((path for path in extraction_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(extraction_root).as_posix())
	return {
		"format": "pinmame-vpx-extraction-manifest",
		"version": 1,
		"files": [{"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": _file_sha256(path)} for path in paths],
	}


def configured_vpx_sources_root(*, required: bool) -> Path | None:
	value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
	if not value:
		if required:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained No Fear extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"No Fear retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	if canonical_bytes(actual) != canonical_bytes(build_extraction_manifest(extraction_root)):
		raise RuntimeError(f"No Fear retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
	if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(f"No Fear retained extraction identity mismatch: files={identity[0]}, bytes={identity[1]}, manifest_sha256={identity[2]}")
	return actual


def provenance(status: str, *source_refs: str) -> dict[str, Any]:
	return {"status": status, "source_refs": list(source_refs)}


def not_applicable(reason: str, *source_refs: str) -> dict[str, Any]:
	return {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *source_refs)}


_LEGACY_ALIASES: dict[str, Any] = {}


def _legacy_aliases() -> dict[str, Any]:
	"""The legacy import's numeric, zero-padded and named aliases by binding group and address, kept while compatibility needs them."""
	if not _LEGACY_ALIASES:
		_LEGACY_ALIASES.update(load_json(LEGACY_ALIAS_SEED_PATH)["aliases"])
	return _LEGACY_ALIASES


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
	legacy = _legacy_aliases().get(group, {}).get(str(address))
	if legacy:
		device["aliases"] = list(device.get("aliases", [])) + [{"namespace": namespace, "value": value} for namespace, value in legacy]
	return device


def output_id(label: str) -> str:
	return "device." + (re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "unnamed")


def _spatial_seed() -> dict[str, Any]:
	return load_json(SPATIAL_SEED_PATH)


# Placements projected onto a table object that models the device's mechanism rather than the device itself: the manual
# locates the device in that mechanism, so it is cited beside the table and script.
PROJECTED_PLACEMENTS = frozenset({("switch", 31)})

# Placements on a table light that is a light-map source with no bulb, set where the table throws the light rather than on a
# modelled socket: the G.I. lights, the raised sign and skull-eye lamps and every flasher light. They are only candidates. An
# insert lamp's light sits on its insert, over the socket, and stays observed.
CANDIDATE_PLACEMENTS = frozenset(
	{("gi", address) for address in (0, 1, 2)}
	| {("lamp", address) for address in (38, 82, 83, 84, 85)}
	| {("solenoid", address) for address in (17, 18, 19, 20, 21, 23, 24, 25, 28)}
)
LIGHT_MAP_NOTE = (
	" The table's light is an invisible light-map source with no bulb: it marks where the table throws the light, not a modelled "
	"socket, so the placement is only a candidate."
)


def located(category: str, address: int, identifier: str, role: str) -> dict[str, Any] | None:
	"""Located spatial record for one device from the committed placement seed, or None.

	Table-derived placements are ``observed``, citing the table for the coordinate and the script for the binding that
	picks the object; a projection also cites the manual. No factory location drawing has been checked against them.
	A placement in ``CANDIDATE_PLACEMENTS`` sits on a light-map source with no bulb, not on the physical part, and is only a
	``candidate``.
	"""
	entries = _spatial_seed()[category].get(str(address))
	if not entries:
		return None
	status = "candidate" if (category, address) in CANDIDATE_PLACEMENTS else "observed"
	refs = (VPX_TABLE_SOURCE, VPX_SCRIPT_SOURCE) + ((MANUAL_SOURCE,) if (category, address) in PROJECTED_PLACEMENTS else ())
	placements = []
	for index, entry in enumerate(entries, start=1):
		suffix = f".{index}" if len(entries) > 1 else ""
		placements.append({
			"id": f"{identifier}.{role}{suffix}", "role": role, "space": "playfield", "x": entry["x"], "y": entry["y"],
			"provenance": provenance(status, *refs),
		})
	return {"status": status, "placements": placements}


def _spatial_note(category: str, address: int) -> str:
	entries = _spatial_seed()[category].get(str(address)) or []
	notes = [entry["note"] for entry in entries if entry.get("note")]
	return (" " + " ".join(dict.fromkeys(notes))) if notes else ""


# --- Inputs --------------------------------------------------------------------------------------------
def _switch_wiring(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	drive_wire, drive_connection, drive_ic = SWITCH_COLUMN_WIRING[column]
	return_wire, return_connection, return_ic = SWITCH_ROW_WIRING[row]
	return {
		"board": "WPC Security CPU board",
		"drive_wire": drive_wire,
		"drive_connection": drive_connection,
		"return_wire": return_wire,
		"return_connection": return_connection,
		"return_component": f"column driver {drive_ic}; row receiver {return_ic}",
	}


SWITCH_NOTES = {
	11: "The cabinet BALL LAUNCH button (20-9663-B-8); its lamp is 86, and the lamp list gives the same part as the lamp's assembly.",
	13: "The cabinet START button (20-9663-1); its lamp is 88.",
	14: "The plumb bob tilt of the Tilt Mechanism Assembly A-15361 inside the cabinet.",
	15: (
		"The shooter lane switch (A-18973): a ball waits on it for the AUTO PLUNGER (2). In T.18's AUTOMATIC cycle the ROM fired the auto "
		"plunger while the host held 15 closed and dropped it when 15 opened."
	),
	16: "The spinner (5647-12693-24) of the Spin Target A-20074 with its Spinner Sign A-20212; the SUPER SPINNER lamp (53) lights it.",
	17: "The right outlane.",
	18: "The right return (inlane); the matrix prints it 'RIGHT RETRUN' on both of its printings.",
	21: "The slam tilt (A-17238) on the coin door.",
	22: "Its part 5643-09268-00 is the one the interlock notice (PDF page 4) names as the memory protect switch on the coin door's interlock bracket.",
	23: (
		"The cabinet BUY EXTRA BALL button (20-9663-18); its lamp is 87. IPDB: unlimited buy-in balls per player (operator option). "
		"Pinned nf.c names switch 23 swTicket; the matrix, the switch list and the ROM's T.1 all name the buy-in button here, so the record follows them."
	),
	24: "Its part 5643-09112-00 is the one the interlock notice (PDF page 4) names as the new interlock switch.",
	25: "The kickback lane switch at the left of the playfield (the matrix prints KICKBACK): the KICKBACK coil (4) fires a ball resting on it back into play when the kickback is lit (lamp 68 KICKBACK).",
	26: "The left return (inlane).",
	27: "The left slingshot: its kick switch (A-17800) and score switch (A-17794) share this address.",
	28: "The right slingshot: its kick switch (A-17800) and score switch (A-17794) share this address.",
	31: "It sees a ball stacked over the ball at position 1, at the eject end of the Outhole Ball Trough Assembly (the trough list prints A-19663, its parts page A-19963).",
	37: "The centre entrance of the underground trough (Underside Ball Trough Assy. A-19948), which T.18 UNDERGROUND TROUGH TEST shows as CTR. ENTR.",
	38: (
		"The left entrance of the underground trough, behind the drop target, which T.18 shows as LEFT ENTR. and its error list calls the "
		"drop target entrance; in T.18 MANUAL the ROM pulses the DROP TARGET DOWN coil (8) when it closes."
	),
	41: (
		"The right popper's resting position, which T.18 shows as POPPER 1: while the host held it in the AUTOMATIC cycle the ROM fired the "
		"RIGHT POPPER coil (1) and dropped it when 41 opened."
	),
	42: "The right popper's second opto (T.18 POPPER 2): a ball from the underground trough passes it before it settles on POPPER 1 (41).",
	46: "The left ball-accelerator opto: in T.16 BALL ACCELERATOR TEST a pulse of it fires the LEFT MAGNET (6) while that magnet is enabled and nothing once it is disabled.",
	47: "The centre ball-accelerator opto: in T.16 a pulse of it fires the CENTER MAGNET (5) while that magnet is enabled.",
	48: "The right ball-accelerator opto: in T.16 a pulse of it fires the RIGHT MAGNET (3) while that magnet is enabled and nothing once it is disabled.",
	51: (
		"The drop target switch, a Mini Micro Switch 5647-12693-31 on the 1-Bank Drop Target Assembly A-14615 (the playfield list calls the "
		"drop target A-20202); T.17 DROP TARGET TEST reports it."
	),
	54: "The left wireform (Left Wire Ramp A-20078, whose parts list carries the Mini Micro Switch 5647-12693-13).",
	55: "The inner loop.",
	56: "The lower of the two LIGHT KICKBACK standup targets (SW-1A-170-15); lamp 72 LIGHT KICKBACK BOTTOM sits at it.",
	57: "The upper of the two LIGHT KICKBACK standup targets (SW-1A-170-15); lamp 71 LIGHT KICKBACK TOP sits at it.",
	58: "The right loop.",
	61: "The eject hole (switch 5647-12133-11, Eject Assembly A-20134): the EJECT coil (15) kicks the ball out.",
	62: "The left loop.",
	63: "The left ramp entrance.",
	64: "The middle of the left ramp.",
	66: "The right ramp entrance.",
	67: "The right ramp exit.",
}


# What the retained known-working version 1.1.1 script does for each matrix switch.
SWITCH_SCRIPT = {
	11: "PlungerKey and LockBarKey set it while held", 14: "vpmNudge.TiltSwitch = 14",
	16: "sw16_spin pulses it", 22: "the controller start-up sets .Switch(22) = 1 ('close coin door')",
	23: "keyFront sets it while held ('buy-in')", 24: "the controller start-up sets .Switch(24) = 1 ('always closed')",
	25: "sw25_hit sets it and hands the ball to the kickback impulse plunger KickBackIM; sw25_unhit clears it",
	27: "sw27_Slingshot pulses it", 28: "sw28_Slingshot pulses it",
	31: "ReleaseBall (solenoid 14) pulses it each time it kicks a ball out of the trough",
	41: "sw41_Hit sets it and holds the ball for SubwayVUK; sw41_UnHit clears it",
	51: "sw51_hit calls DTHit 51", 56: "sw56_hit calls STHit 56", 57: "sw57_hit calls STHit 57",
	61: "sw61_Hit sets it and holds the ball for LeftKicker; sw61_UnHit clears it",
}
for _address in (15, 17, 18, 26, 37, 38, 42, 54):
	SWITCH_SCRIPT[_address] = f"sw{_address}_hit sets it and sw{_address}_unhit clears it"
for _address in (32, 33, 34, 35):
	SWITCH_SCRIPT[_address] = (
		f"the start-up creates a ball in the trough kicker sw{_address} and sets it; sw{_address}_Hit sets it and sw{_address}_UnHit clears "
		"it, and UpdateTrough rolls the trough's balls down"
	)
for _address in (46, 47, 48, 55, 58, 62, 63, 64, 66, 67):
	SWITCH_SCRIPT[_address] = f"sw{_address}_hit pulses it"


def _matrix_switch(address: int) -> dict[str, Any]:
	column, row = divmod(address, 10)
	identifier = f"switch.matrix-{address}"
	notes = f"Printed switch-matrix drive column {column}, return row {row}."
	extra: dict[str, Any] = {"aliases": [{"namespace": "pinmame.switch", "value": str(address)}], "wiring": _switch_wiring(address)}
	if address in UNUSED_MATRIX_ADDRESSES:
		if address in UNUSED_NAMED:
			notes += (
				" The Switch Matrix and the Switch Locations list print NOT USED for this position. The ROM still scans it: in its T.1 "
				"SWITCH EDGES sweep a host write of 1 drew 'UNUSED', and 0 cleared it."
			)
		else:
			notes += (
				" The Switch Matrix prints NOT USED and the Switch Locations list says '68 through 88 are NOT USED'. In the T.1 SWITCH EDGES "
				"sweep the ROM reported no edge here at either level and kept its last line for 68, so its switch test reports nothing in "
				"matrix columns 7 and 8."
			)
		if address in MASKED_SWITCHES:
			notes += " PinMAME's nfGameData inverted-switch mask still covers it, and the matrix page shades it with the rest of column 3."
		elif address in SHADED_SWITCHES:
			notes += " The matrix page shades it with the rest of column 4, but PinMAME's mask does not cover it."
		return _device(
			identifier, f"Not Used Matrix Position {address}", "switch", SWITCH_GROUP, address, "unused",
			(MANUAL_SOURCE, CONTROLLER_SOURCE, EDGES_SOURCE),
			physical={"notes": notes}, spatial=not_applicable("unused", MANUAL_SOURCE),
			normally_closed=False, **extra,
		)
	part, description = SWITCH_LOCATIONS[address]
	physical: dict[str, Any] = {"switch_type": SWITCH_TYPES[address]}
	if " / " in part:
		physical["assembly_part_number"] = part
	elif address in {14, 15}:
		physical["assembly_part_number"] = part
	else:
		physical["part_number"] = part
	notes += f" Switch Locations description \"{description}\"."
	if description.endswith("*"):
		notes += " The list's '*' marks a switch its location drawing does not show."
	refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE)
	if address == 22:
		notes += (
			" Every service-test run held public 22 at 0 (door open), as the WPC service buttons require, so T.1 did not sweep it; the "
			"controller profile and the coin door wiring give its role."
		)
		refs = (MANUAL_SOURCE, CORE_SOURCE, CONTROLLER_SOURCE)
	elif address == 24:
		notes += (
			" PinMAME holds public 24 at 1 from power-up. In T.1 SWITCH EDGES the redundant write of 1 drew nothing new and the 1 -> 0 "
			"edge drew 'ALWAYS CLOSED / T.1 LAST SW. 24', so the ROM reports this position when it opens."
		)
	else:
		notes += f" The ROM names it \"{ROM_SWITCH_NAMES[address]}\" in T.1 SWITCH EDGES while the host holds public {address} at 1, and clears the name at 0."
	if address in SWITCH_FIRES:
		notes += f" Closing it made the ROM fire its own coil, public solenoid {SWITCH_FIRES[address]}, even inside T.1."
	if address in MASKED_SWITCHES:
		notes += (
			" PinMAME's nfGameData inverted-switch mask inverts this address, so public 1 is an open matrix contact; the ROM reads the "
			"switch as active at public 1, so its matrix contact rests closed and normally_closed is true. The matrix page shades the cell "
			"'Opto, Typically Closed'."
		)
	if address in OPTO_BOARDS:
		notes += f" It is {OPTO_BOARDS[address]}."
	if address in {32, 33, 34, 35}:
		notes += f" It reports a ball at trough position {address - 31}; position 1 is the eject end, so it is blocked while the trough holds at least {address - 31} ball{'s' if address > 32 else ''} (No Fear is a four-ball game)."
	if address in SWITCH_NOTES:
		notes += " " + SWITCH_NOTES[address]
	if address in {37, 38, 41, 42}:
		refs += (TROUGH_TEST_SOURCE,)
	if address in {46, 47, 48}:
		refs += (ACCELERATOR_SOURCE,)
	if address == 15:
		refs += (TROUGH_TEST_SOURCE,)
	if address == 23:
		refs += (IDENTITY_SOURCE,)
	label = SWITCH_LABELS[address]
	role = SWITCH_ROLES.get(address)
	if role:
		extra["roles"] = [role]
		extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["location"] = SWITCH_LOCATIONS_TEXT[address]
	elif address == 24:
		extra["spatial"] = not_applicable("constant", MANUAL_SOURCE)
		physical["location"] = "coin door"
	else:
		spatial = located("switch", address, identifier, "sensor")
		if spatial:
			extra["spatial"] = spatial
			notes += _spatial_note("switch", address)
	if address in SWITCH_SCRIPT:
		notes += f" Retained script: {SWITCH_SCRIPT[address]}."
		refs += (VPX_SCRIPT_SOURCE,)
	kind = "constant" if address == 24 else "switch"
	if address == 24:
		extra["constant_active"] = True
		extra["initial_active"] = True
	else:
		extra["normally_closed"] = address in MASKED_SWITCHES
	if address == 22:
		extra["initial_active"] = True
		notes += " It is closed while the coin door is closed."
	physical["notes"] = notes
	return _device(identifier, label, kind, SWITCH_GROUP, address, "used", refs, physical=physical, **extra)


# Fliptronic column (switch-matrix.md; switch-locations.md; fliptronic-board.md; opto-boards.md):
# public -> (label, printed position, matrix wire, connector, type, role, availability).
FLIPPER_SWITCHES = {
	111: ("Lower Right Flipper EOS", "F1", "Black-Green", "J906-1", "leaf", "internal.flipper.lower.right.eos", "used"),
	112: ("Right Flipper Button Opto (F2)", "F2", "Blue-Violet", "J905-1", "opto", "flipper.lower.right.button", "used"),
	113: ("Lower Left Flipper EOS", "F3", "Black-Blue", "J906-3", "leaf", "internal.flipper.lower.left.eos", "used"),
	114: ("Left Flipper Button Opto (F4)", "F4", "Blue-Gray", "J905-2", "opto", "flipper.lower.left.button", "used"),
	115: ("Upper Right Flipper EOS", "F5", "Black-Violet", "J906-4", "leaf", "internal.flipper.upper.right.eos", "used"),
	116: ("Right Flipper Button Opto (F6)", "F6", "Black-Yellow", "J905-3", "opto", "flipper.upper.right.button", "used"),
	117: ("Not Used Fliptronic Position F7", "F7", "Black-Gray", "J906-5", "leaf", None, "unused"),
	118: ("Left Flipper Button Opto (F8)", "F8", "Black-Blue", "J905-5", "opto", "flipper.lower.left.button", "used"),
}
# The ROM's T.1 text while the host holds the opto at 1 (switch-edges run): name, position and wires.
FLIPPER_ROM_TEXT = {
	112: ("R. FLIPPER E.O.S.", "F1 BLK-GRN ORN"), 114: ("L. FLIPPER E.O.S.", "F3 BLK-BLU ORN"),
	116: ("U.R. FLIPPER E.O.S.", "F5 BLK-VIO ORN"), 118: ("L. FLIPPER E.O.S.", "F3 BLK-BLU ORN"),
}
FLIPPER_FIRES = {
	112: "the lower right flipper (public 45 and 46)", 114: "the lower left flipper (public 47 and 48)",
	116: "the lower right and the upper right flippers (public 45, 46, 33 and 34)", 118: "the lower left flipper (public 47 and 48)",
}
FLIPPER_BOARD_WIRES = {
	112: "Blue-Violet, F2 to right flipper opto J1-2", 114: "Blue-Gray, F4 to left flipper opto J1-2",
	116: "Black-Yellow, F6 to right flipper opto J1-1", 118: "Black-Blue, F8 to left flipper opto J1-1 (not used)",
}
FLIPPER_ASSEMBLIES = {111: ("lower right", "A-14876-R-3"), 113: ("lower left", "A-15849-L-2"), 115: ("upper right", "A-19945")}


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 9):
		label, role, note = DEDICATED_SWITCH_LABELS[address]
		wire, connection, j1, j3 = DEDICATED_SWITCH_WIRING[address]
		note += f" The DEDICATED SWITCHES drawing (3-3) runs it from CPU {connection} to the Coin Door Interface board's {j1}"
		note += f" and the switch on {j3}." if j3 else ", and draws no J3 pin or switch for it."
		if address == 7:
			note += " The drawing prints its wire 'Orange-Vioiet'."
		if address == 5:
			note += " The matrix prints 'Service Credit'; the drawing's text spells it 'Service Credits'."
		if address == 4:
			note += " The matrix prints '4th Coin Chute' and the drawing's text 'Fourth Coin Chute'."
		items.append(
			_device(
				f"switch.cabinet-{address}", label, "switch", SWITCH_GROUP, address,
				"optional" if address == 4 else "used", (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": f"D{address}"}],
				normally_closed=False, roles=[role],
				physical={
					"location": "coin door", "switch_type": "button",
					"notes": (
						f"Printed dedicated grounded switch D{address}. {note} The dedicated switches reach the CPU through the Coin Door "
						"Interface P.C.B. A-17051-1; the drawing prints the IC pin '(U17-5)' on every line, so no per-line receiver is recorded."
					),
				},
				wiring={"board": "WPC Security CPU board", "drive_wire": wire, "drive_connection": connection},
				spatial=not_applicable("cabinet_or_service", MANUAL_SOURCE),
			)
		)
	for column in range(1, 9):
		for row in range(1, 9):
			items.append(_matrix_switch(column * 10 + row))
	for address, (label, printed, wire, connection, switch_type, role, availability) in FLIPPER_SWITCHES.items():
		notes = f"Printed Fliptronic grounded switch {printed} ({wire}, {connection} on the Fliptronic II board)."
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.switch", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
			"wiring": {"board": "Fliptronic II board A-15472-1", "drive_wire": wire, "drive_connection": connection},
		}
		if role:
			extra["roles"] = [role]
		refs = (MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE, EDGES_SOURCE)
		physical: dict[str, Any] = {"switch_type": switch_type}
		if address in FLIPPER_ASSEMBLIES:
			flipper, assembly = FLIPPER_ASSEMBLIES[address]
			physical["part_number"] = "SW-1A-194"
			physical["assembly_part_number"] = assembly
			physical["location"] = "flipper assembly"
			notes += (
				f" End-of-stroke switch SW-1A-194 on the {flipper} flipper (Flipper Assembly {assembly}). nfGameData declares "
				"FLIP_SOL(FLIP_L | FLIP_UR), so PinMAME rewrites this bit from the flipper coil state on every update: in the T.1 sweep a host "
				"write of 1 read back 0 and drew no name. Its public level is not a measurement of the contact; normally_closed records the "
				"grounded switch's open rest state."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("internal_nonvisual", MANUAL_SOURCE)
		elif address == 117:
			notes += (
				" The matrix prints F7 'Upper Left E.O.S.', but the Switch Locations list prints F7 NOT USED, the Fliptronic II pin list prints "
				"J906-5 N/C, the flipper-circuit page footnotes 'THE UPPER LEFT FLIPPER IS NOT USED', and in the T.1 sweep a host write of 1 "
				"round-tripped and drew no name."
			)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
		else:
			side = "right" if address in {112, 116} else "left"
			rom_name, rom_text = FLIPPER_ROM_TEXT[address]
			physical["location"] = "cabinet flipper button"
			physical["assembly_part_number"] = "A-17316"
			notes += (
				f" An opto of the {side} Flipper Opto Board A-17316 at the {side} cabinet button; the Fliptronic II pin list prints "
				f"'{FLIPPER_BOARD_WIRES[address]}'. Each button's board carries two optos ({'F2 and F6' if side == 'right' else 'F4 and F8'}), "
				"so one press interrupts both. WPC-Security reads the flipper column complemented (WPC_FLIPPERS returns ~swMatrix), so public 1 "
				"is the pressed button and the contact the column sees is open at rest: normally_closed is false. The matrix shades the cell as "
				f"an opto. In the T.1 sweep a host write of 1 showed '{rom_name}' ({rom_text}) and fired {FLIPPER_FIRES[address]}."
			)
			if address in {112, 116}:
				notes += (
					" The Flipper Opto Board's own pin list wires its J1-1 (Black-Yellow) from J905-1 and J1-2 (Blue-Violet) from J905-3, the "
					"J905 pins crossed against the Fliptronic II list; the wire colours and the opto positions agree, so the pin is a wiring detail."
				)
			if address == 112:
				notes += " The Switch Locations list prints F2 'Lwr Right Flipper Cab.'."
			if address == 116:
				notes += (
					" The matrix prints F6 'Upper Right Opto' and the list 'Upr Right Flipper Cab.'. The ROM fires the upper right flipper only "
					"from this opto and the lower right flipper from it and from F2, so it is the right button's second opto with the upper "
					"flipper's role; a consumer writes 112 and 116 together from the right button."
				)
			if address == 114:
				notes += " The Switch Locations list prints F4 'Lwr Left Flipper Cab.'."
			if address == 118:
				notes += (
					" The matrix prints F8 'Upper Left Opto' and the Switch Locations list prints F8 NOT USED, and the Fliptronic II list adds "
					"'(not used)', but the left Flipper Opto Board's pin list wires its J1-1 (Black-Blue) from J905-5 and the ROM fires the lower "
					"left flipper from it as from F4. No Fear has no upper left flipper, so the left button's second opto is a second lower-left "
					"input; a consumer writes 114 and 118 together from the left button."
				)
			extra["normally_closed"] = False
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
		physical["notes"] = notes
		extra["physical"] = physical
		items.append(_device(f"switch.generic-{address}", label, "switch", SWITCH_GROUP, address, availability, refs, **extra))
	chart = {1: "Off, Off, Off, Off, Off", 2: "Off, Off, Off, Off, Off", 3: "On, On, On, On, On", 4: "On, On, On, On, On", 5: "On, On, On, On, Off", 6: "On, Off, On, On, On", 7: "On, On, Off, On, On", 8: "On, On, Off, Off, On"}
	for address in range(1, 9):
		items.append(
			_device(
				f"switch.dip-{address}", f"CPU DIP SW{address} (country setting)", "dip_switch", DIP_GROUP, address, "used",
				(MANUAL_SOURCE, CONTROLLER_SOURCE, CORE_SOURCE),
				aliases=[{"namespace": "pinmame.dip", "value": str(address)}, {"namespace": "manual.address", "value": f"SW{address}"}],
				physical={
					"location": "WPC Security CPU board", "switch_type": "dip",
					"notes": f"CPU-board DIP position SW{address}. The printed DIP SWITCH SETTINGS chart (PDF page 2) sets it, for America, European, French, German and Spain in that order: {chart[address]}.",
				},
				spatial=not_applicable("dip_switch", MANUAL_SOURCE),
			)
		)
	return items


# --- Solenoid data (solenoid-flasher-table.md, solenoid-flasher-locations.md, power-driver-board.md) ------
SOLENOID_LABELS = {
	1: "Right Popper", 2: "Auto Plunger", 3: "Right Magnet", 4: "Kickback", 5: "Center Magnet", 6: "Left Magnet", 7: "Knocker",
	8: "Drop Target Down", 9: "Not Used Driver 9", 10: "Right Slingshot", 11: "Left Slingshot", 12: "Drop Target Up",
	13: "Not Used Driver 13", 14: "Trough Eject", 15: "Eject Hole Kicker", 16: "Skull Mouth", 17: "Flipper Return Flasher",
	18: "Spinner Flasher", 19: "No Fear Flasher", 20: "Right Ramp Flasher", 21: "Skull Flasher", 22: "Insert Explode Flasher",
	23: "Left Ramp Flasher", 24: "Top Left Flasher", 25: "Autofire Flasher", 26: "Top Left Insert Flasher",
	27: "Top Right Insert Flasher", 28: "Right Popper Flasher",
	33: "Upper Right Flipper Power", 34: "Upper Right Flipper Hold", 35: "Not Used Upper Left Flipper Power",
	36: "Not Used Upper Left Flipper Hold", 45: "Lower Right Flipper Power", 46: "Lower Right Flipper Hold",
	47: "Lower Left Flipper Power", 48: "Lower Left Flipper Hold",
}
VIRTUAL_SOLENOID_LABELS = {
	29: "WPC J111 General-Purpose State Bit A", 30: "WPC J111 General-Purpose State Bit B", 31: "WPC Game-On State",
	32: "Unused WPC State Channel 32", 37: "Unused WPC-Security Output 37", 38: "Unused WPC-Security Output 38",
	39: "Unused WPC-Security Output 39", 40: "Unused WPC-Security Output 40", 41: "Unused WPC-Security Output 41",
	42: "Unused WPC-Security Output 42", 43: "Unused WPC-Security Output 43", 44: "Unused WPC-Security Output 44",
	49: "PinMAME Simulator Ball-Shooter Channel", 50: "Reserved WPC Output 50",
}
# The table's NOT USED auxiliary driver rows for 37-44 (solenoid-flasher-table.md): transistor and wire.
AUX_ROWS = {37: ("Q16", "BRN-WHT"), 38: ("Q15", "BLK-WHT"), 39: ("Q14", "ORG-WHT"), 40: ("Q13", "YEL-WHT"), 41: ("Q9", "GRN-WHT"), 42: ("Q10", "BLU-WHT"), 43: ("Q11", "VIO-WHT"), 44: ("Q12", "GRY-WHT")}
# address -> printed (type, voltage connection, transistor, drive connection, wire, part or flashlamp), Solenoid/Flashlamp Table (2-38).
SOLENOID_TABLE = {
	1: ("High Power", "J107-2", "Q82", "J130-1", "VIO-BRN", "AE-23-800"), 2: ("High Power", "J107-2", "Q80", "J130-2", "VIO-RED", "AE-23-800"),
	3: ("High Power", "J107-2", "Q78", "J130-4", "VIO-ORG", "20-10197-2*"), 4: ("High Power", "J107-2", "Q76", "J130-5", "VIO-YEL", "AE-23-800"),
	5: ("High Power", "J107-2", "Q64", "J130-6", "VIO-GRN", "20-10197-1*"), 6: ("High Power", "J107-2", "Q66", "J130-7", "VIO-BLU", "20-10197*"),
	7: ("High Power", "J107-2", "Q68", "J130-8", "VIO-BLK", "AE-23-800"), 8: ("High Power", "J107-2", "Q70", "J130-9", "VIO-GRY", "SM1-26-600"),
	9: ("Low Power", None, "Q58", None, "BRN-BLK", None), 10: ("Low Power", "J107-3", "Q56", "J127-3", "BRN-RED", "AE-26-1200"),
	11: ("Low Power", "J107-3", "Q54", "J127-4", "BRN-ORG", "AE-26-1200"), 12: ("Low Power", "J107-3", "Q52", "J127-5", "BRN-YEL", "AE-26-1200"),
	13: ("Low Power", None, "Q50", None, "BRN-GRN", None), 14: ("Low Power", "J107-3", "Q48", "J127-7", "BRN-BLU", "AE-26-1500"),
	15: ("Low Power", "J107-3", "Q46", "J127-8", "BRN-VIO", "AE-27-1200"), 16: ("Low Power", "J107-3", "Q44", "J127-9", "BRN-GRY", "SM-30-1100"),
	17: ("Flashlamp", "J107-6", "Q42", "J126-1", "BLK-BRN", "#89 (2)"), 18: ("Flashlamp", "J107-6", "Q40", "J126-2", "BLK-RED", "#906 (1)"),
	19: ("Flashlamp", "J107-6", "Q38", "J126-3", "BLK-ORG", "#906 (1)"), 20: ("Flashlamp", "J107-6, J106-5", "Q36", "J126-4, J125-5", "BLK-YEL", "#89 (1), #906 (2)"),
	21: ("Flashlamp", "J107-6, J106-5", "Q28", "J126-5, J125-6", "BLU-GRN", "#906 (2), #906 (1)"), 22: ("Flashlamp", "J106-5", "Q30", "J125-7", "BLU-BLK", "#906 (1)"),
	23: ("Flashlamp", "J107-6, J106-5", "Q34", "J126-7, J125-8", "BLU-VIO", "#89 (1), #906 (2)"), 24: ("Flashlamp", "J107-6", "Q32", "J126-8", "BLU-GRY", "#906 (1)"),
	25: ("Gen. Purpose", "J107-6", "Q26", "J122-1", "BLU-BRN", "#89 (2)"), 26: ("Gen. Purpose", "J106-5", "Q24", "J124-2", "BLU-RED", "#906 (1)"),
	27: ("Gen. Purpose", "J106-5", "Q22", "J124-3", "BLU-ORG", "#906 (1)"), 28: ("Gen. Purpose", "J107-6", "Q20", "J122-4", "BLU-YEL", "#89 (1)"),
}
# Coil or bulb part numbers the definition records (the locations list prints 24-8704 = #89 and 24-8802 = #906).
SOLENOID_PARTS = {
	1: "AE-23-800", 2: "AE-23-800", 3: "20-10197-2", 4: "AE-23-800", 5: "20-10197-1", 6: "20-10197", 7: "AE-23-800", 8: "SM1-26-600",
	10: "AE-26-1200", 11: "AE-26-1200", 12: "AE-26-1200", 14: "AE-26-1500", 15: "AE-27-1200", 16: "SM-30-1100",
	17: "24-8704", 18: "24-8802", 19: "24-8802", 20: "24-8704, 24-8802", 21: "24-8802", 22: "24-8802", 23: "24-8704, 24-8802",
	24: "24-8802", 25: "24-8704", 26: "24-8802", 27: "24-8802", 28: "24-8704",
}
FLASHER_QUANTITY = {17: 2, 18: 1, 19: 1, 20: 3, 21: 3, 22: 1, 23: 3, 24: 1, 25: 2, 26: 1, 27: 1, 28: 1}
# Locations-list assembly for each coil/flasher (solenoid-flasher-locations.md, 2-39).
SOLENOID_ASSEMBLIES = {
	1: "A-19965", 2: "A-14525", 3: "A-20034", 4: "B-11873", 5: "A-20034", 6: "A-20034", 7: "A-10686-1", 8: "A-20202", 10: "B-9362-R-3",
	11: "B-9362-L-2", 12: "A-20202", 14: "A-19663", 15: "A-20134", 16: "A-20144", 17: "A-17983", 18: "C-13337", 19: "C-13337",
	20: "A-17983", 21: "A-17802", 23: "A-17983", 24: "C-13337", 25: "A-17803", 28: "A-17983",
}
# The ROM's own T.4 and T.5 names and wires (solenoid-test and flasher-names runs).
ROM_SOLENOID_NAMES = {
	1: ("RIGHT POPPER", "VIO-BRN RED-BRN"), 2: ("AUTO PLUNGER", "VIO-RED RED-BRN"), 3: ("RIGHT MAGNET", "VIO-ORN RED-BRN"),
	4: ("KICKBACK", "VIO-YEL RED-BRN"), 5: ("CENTER MAGNET", "VIO-GRN RED-BRN"), 6: ("LEFT MAGNET", "VIO-BLU RED-BRN"),
	7: ("KNOCKER", "VIO-BLK RED-BRN"), 8: ("DROP TARGET DOWN", "VIO-GRY RED-BRN"), 9: ("UNUSED", "BRN-BLK RED-BLK"),
	10: ("RIGHT SLINGSHOT", "BRN-RED RED-BLK"), 11: ("LEFT SLINGSHOT", "BRN-ORN RED-BLK"), 12: ("DROP TARGET UP", "BRN-YEL RED-BLK"),
	13: ("UNUSED", "BRN-GRN RED-BLK"), 14: ("TROUGH", "BRN-BLU RED-BLK"), 15: ("EJECT", "BRN-VIO RED-BLK"),
	16: ("SKULL MOUTH", "BRN-GRY RED-BLK"),
	17: ("FLS.(2) FLPR. RTRN.", "BLK-BRN RED-WHT"), 18: ("FLS. SPINNER", "BLK-RED RED-WHT"), 19: ("FLS. NO FEAR", "BLK-ORN RED-WHT"),
	20: ("FLS.(3) RT. RAMP", "BLK-YEL RED-WHT"), 21: ("FLS.(2) SKULL", "BLU-GRN RED-WHT"), 22: ("FLS. BKBOX EXPL.", "BLU-BLK RED-WHT"),
	23: ("FLS.(3) LEFT RAMP", "BLU-VIO RED-WHT"), 24: ("FLS. TOP LEFT", "BLU-GRY RED-WHT"), 25: ("FLS.(2) AUTO-FIRE", "BLU-BRN RED-WHT"),
	26: ("FLS. BKBOX L TOP", "BLU-RED RED-WHT"), 27: ("FLS. BKBOX R TOP", "BLU-ORN RED-WHT"), 28: ("FLS. RT. POPPER", "BLU-YEL RED-WHT"),
	45: ("R. FLIP. POWER", "YEL-GRN RED-GRN"), 46: ("R. FLIP. HOLD", "ORN-GRN RED-GRN"), 47: ("L. FLIP. POWER", "YEL-BLU RED-BLU"),
	48: ("L. FLIP. HOLD", "ORN-BLU RED-BLU"), 33: ("U.R. FLIP. POWER", "YEL-VIO RED-VIO"), 34: ("U.R. FLIP. HOLD", "ORN-VIO RED-VIO"),
}
T5_ADDRESSES = frozenset(range(17, 29))
T12_ADDRESSES = frozenset({33, 34, 45, 46, 47, 48})
FLASHER_SOLENOIDS = frozenset(range(17, 29))
MAGNET_SOLENOIDS = frozenset({3, 5, 6})
BACKBOX_FLASHERS = frozenset({22, 26, 27})
_MAGNET = (
	" It is one of three Coil Magnet/Breaker assemblies (20-10197, -1, -2) on the Opto Mounting Brackets A-20034 of the Back Panel "
	"Assembly A-20033; each magnet carries a thermal breaker in its bulge that cuts it off when it overheats (Unit Disassembly, PDF page 72), "
	"and each uses a wave spring washer 20-9612 (the table's '*' footnote)."
)
SOLENOID_NOTES = {
	1: "The RIGHT POPPER coil (AE-23-800, Ball Popper Assembly A-19965): it kicks the ball resting on POPPER 1 (41) out of the underground trough's exit.",
	2: "The AUTO PLUNGER coil (AE-23-800; the locations list gives assembly A-14525, which the playfield parts list calls the Autoplunger): it launches the ball resting on the shooter lane switch (15).",
	3: "The RIGHT MAGNET of the ball accelerator (20-10197-2): the ROM fires it once when the right accelerator opto (48) is blocked while the magnet is enabled." + _MAGNET,
	4: "The KICKBACK coil (AE-23-800, Bottom Arch Kicker Assembly B-11873): it fires the ball resting on the kickback lane switch (25) back into play when the kickback is lit.",
	5: "The CENTER MAGNET of the ball accelerator (20-10197-1; the locations list prints 'Centr Magnet'): the ROM fires it once when the centre opto (47) is blocked while the magnet is enabled." + _MAGNET,
	6: "The LEFT MAGNET of the ball accelerator (20-10197): the ROM fires it once when the left opto (46) is blocked while the magnet is enabled." + _MAGNET,
	7: "The KNOCKER (AE-23-800). The table prints its voltage (J107-2) and drive (J130-8) connections and its part in the Backbox columns; the locations list prints assembly A-10686-1 with the footnote mark '**' (Not Shown), and the parts page lists the Knocker Assembly as B-10686-1.",
	8: "The DROP TARGET DOWN coil (SM1-26-600, the target knock-down coil of the 1-Bank Drop Target Assembly A-14615; the locations list prints A-20202): it drops the target (51). T.18 MANUAL pulses it as it starts and again when the left trough entrance (38) closes.",
	9: "Printed NOT USED: the table prints transistor Q58 and wire BRN-BLK but no connection or coil, and the locations list prints none. The ROM's T.4 still offers the driver and prints UNUSED while it pulses public 9, so the pulse is the sweep, not a fitted load.",
	10: "The right slingshot coil (AE-26-1200, Coil & Bracket Assy. B-9362-R-3); the ROM fired it when the T.1 sweep closed 28.",
	11: "The left slingshot coil (AE-26-1200, B-9362-L-2); the ROM fired it when the T.1 sweep closed 27.",
	12: "The DROP TARGET UP coil (AE-26-1200, the reset coil of the 1-Bank Drop Target Assembly A-14615; the locations list prints A-20202): it raises the drop target (51).",
	13: "Printed NOT USED: the table prints transistor Q50 and wire BRN-GRN but no connection or coil, and the locations list prints none. The ROM's T.4 still offers the driver and prints UNUSED while it pulses public 13, so the pulse is the sweep, not a fitted load.",
	14: "The trough eject coil (AE-26-1500; the locations list prints assembly A-19663, the parts page the Outhole Ball Trough Assembly A-19963), printed TROUGH: it kicks the ball at the trough's eject end into the shooter lane. In T.18's AUTOMATIC cycle the ROM held it until trough position 4 (35) opened.",
	15: "The EJECT coil (AE-27-1200, Eject Assembly A-20134): it kicks the ball out of the eject hole (61).",
	16: "The SKULL MOUTH coil (SM-30-1100-DC on the Skull Base Assembly A-20144, which carries the lower jaw of the Skull Assembly A-20142): it opens the skull's jaw. T.19 SKULL TEST pulses it with the skull flashers (21) while it plays speech calls.",
	17: "The FLIPPER RETURN flashers: two #89 (24-8704) on the playfield (A-17983), one at each flipper return.",
	18: "The SPINNER flasher: one #906 (24-8802) on a Single Flasher Lamp Assy. C-13337.",
	19: "The NO FEAR flasher: one #906 (24-8802) on a Single Flasher Lamp Assy. C-13337. The Solenoid/Flashlamp Table, its Section 3 and PDF page 2 copies and the flashlamp wiring drawing (PDF page 120, one bulb on J126-3) print one bulb; the locations list prints 24-8802 (2). The quantity follows the table and the wiring drawing.",
	20: "The RIGHT RAMP flasher circuit, printed '(3)': one #89 (24-8704) on the playfield (A-17983) and two #906 on the insert panel, on separate playfield (J126-4) and insert-panel (J125-5) drive connections of one driver.",
	21: "The SKULL flasher circuit, printed '(3)': two #906 inside the skull (Skull Assembly; the locations list prints A-17802) and one #906 on the insert panel (J126-5 and J125-6). The skull's unit-disassembly page counts two #906 and two #44 bulbs in it; the #44 are the eye lamps 82 and 85.",
	22: "The INSERT EXPLODE flasher: one #906 on the insert panel (J125-7), with no playfield connection. The ROM calls it FLS. BKBOX EXPL.",
	23: "The LEFT RAMP flasher circuit, printed '(3)': one #89 on the playfield (A-17983) and two #906 on the insert panel (J126-7 and J125-8).",
	24: "The TOP LEFT flasher: one #906 on a Single Flasher Lamp Assy. C-13337, which the Back Panel Assembly A-20033 carries (the locations drawing marks it '(Back Panel)').",
	25: "The AUTOFIRE flashers (Gen. Purpose driver): two #89 (24-8704) on the playfield (A-17803).",
	26: "The TOP LEFT INSERT flasher (Gen. Purpose driver): one #906 on the insert panel (J124-2). The ROM calls it FLS. BKBOX L TOP.",
	27: "The TOP RIGHT INSERT flasher (Gen. Purpose driver; printed 'TOP RT INSERT FLS'): one #906 on the insert panel (J124-3). The ROM calls it FLS. BKBOX R TOP.",
	28: "The RIGHT POPPER flasher (Gen. Purpose driver): one #89 (24-8704) on the playfield (A-17983).",
}
SOLENOID_TYPE_NOTE = (
	" The table types 21-24 'Flashlamp' though their drive wires are Blue, the colour of the general-purpose circuits; their supply is "
	"the flashlamp supply on J107-6 / J106-5 like every circuit from 17 to 28."
)
# What the retained known-working version 1.1.1 script does for each solenoid (SolCallback table and the subs it names).
SOLENOID_SCRIPT = {
	1: "SolCallback(1) = \"SubwayVUK\": while the trigger sw41 holds a ball it kicks it out and clears 41",
	2: "SolCallback(2) = \"SolAutoPlungerIM\": fires the impulse plunger PlungerIM",
	3: "SolCallback(3) = \"Rmag\": while it is on, a ball over the trigger RightMagnet moving right is set to MagnetSpeed; RightMagnet_unhit stops the ball when the centre magnet is on and the right one off",
	4: "SolCallback(4) = \"SolKickbackIM\": fires the impulse plunger KickBackIM, which sw25 loads",
	5: "SolCallback(5) = \"Cmag\": while it is on, a ball over the trigger CenterMagnet moving right is set to MagnetSpeed",
	6: "SolCallback(6) = \"Lmag\": while it is on, a ball over the trigger LeftMagnet moving right is set to MagnetSpeed",
	7: "SolCallback(7) = \"SolKnocker\" calls the knocker sound routine KnockerSolenoid",
	8: "SolCallback(8) = \"DropTargetDOWN\": drops the target (DTDrop 51)",
	9: "the SolCallback line is commented out ('9-N.U.')",
	10: "the SolCallback line is commented out: the table fires the slingshot from the wall's own Slingshot event",
	11: "the SolCallback line is commented out: the table fires the slingshot from the wall's own Slingshot event",
	12: "SolCallback(12) = \"DropTargetUP\": raises the target (DTRaise 51)",
	13: "the SolCallback line is commented out ('13-N.U.')",
	14: "SolCallback(14) = \"ReleaseBall\": pulses 31 and kicks the ball out of the trough kicker sw32",
	15: "SolCallback(15) = \"LeftKicker\": while the trigger sw61 holds a ball it kicks it out, and clears 61",
	16: "SolCallback(16) = \"SolMouth\": rotates the invisible flipper FlipperJaw, whose angle FlipperJaw_Animate copies to the skull jaw primitives",
	17: "SolModCallback(17) = \"FlashMod117\" (commented 'Flipper Return (x2)'): drives the lights f117a and f117b",
	18: "SolModCallback(18) = \"FlashMod118\": drives the light f118",
	19: "SolModCallback(19) = \"FlashMod119\" (commented 'No Fear (x2)'): drives the light f119 and the glow f119_mayo",
	20: "SolModCallback(20) = \"FlashMod120\": drives the light f120",
	21: "SolModCallback(21) = \"FlashMod121\" (commented 'Skull (x2)'): drives the light f121",
	22: "SolModCallback(22) = \"FlashMod122\" (commented 'BKBok EXPL'): drives the light f122",
	23: "SolModCallback(23) = \"FlashMod123\": drives the light f123",
	24: "SolModCallback(24) = \"FlashMod124\": drives the light f124",
	25: "SolModCallback(25) = \"FlashMod125\" (commented 'AutoFire (x2)'): drives the lights f125a and f125b",
	26: "SolModCallback(26) = \"FlashMod126\" (commented 'BKBok L Top'): drives the light f126",
	27: "SolModCallback(27) = \"FlashMod127\" (commented 'BKBok R Top'): drives the light f127",
	28: "SolModCallback(28) = \"FlashMod128\": drives the light f128",
	33: "SolCallback(sURFlipper) = \"SolURFlipper\" rotates RightUpFlipper", 34: "SolCallback(sURFlipper) = \"SolURFlipper\" rotates RightUpFlipper",
	45: "SolCallback(sLRFlipper) = \"SolRFlipper\" fires RightFlipper", 46: "SolCallback(sLRFlipper) = \"SolRFlipper\" fires RightFlipper",
	47: "SolCallback(sLLFlipper) = \"SolLFlipper\" fires LeftFlipper", 48: "SolCallback(sLLFlipper) = \"SolLFlipper\" fires LeftFlipper",
}
FLIPPER_COILS = {
	45: ("power", "29", "lower right", "J907-1 (RED-GRN)", "Q4", "J902-13", "YEL-GRN", "A-14876-R-3", "flipper.lower.right", 1),
	46: ("hold", "30", "lower right", "J907-1 (RED-GRN)", "Q11", "J902-11", "ORG-GRN", "A-14876-R-3", "flipper.lower.right", 2),
	47: ("power", "31", "lower left", "J907-4 (RED-BLU)", "Q3", "J902-9", "YEL-BLU", "A-15849-L-2", "flipper.lower.left", 3),
	48: ("hold", "32", "lower left", "J907-4 (RED-BLU)", "Q9", "J902-7", "ORG-BLU", "A-15849-L-2", "flipper.lower.left", 4),
	33: ("power", "33", "upper right", "J907-6 (RED-VIO)", "Q2", "J902-6", "YEL-VIO", "A-19945", "flipper.upper.right", 5),
	34: ("hold", "34", "upper right", "J907-6 (RED-VIO)", "Q7", "J902-4", "ORG-VIO", "A-19945", "flipper.upper.right", 6),
}
UNUSED_FLIPPER_COILS = {35: ("power", "Q1", "J902-3", "YEL-GRY"), 36: ("hold", "Q5", "J902-1", "ORG-GRY")}


def _solenoid_wiring(address: int) -> dict[str, Any]:
	printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
	wiring = {"board": "WPC power driver board A-12697-3", "control_wire": wire, "driver_transistor": transistor}
	if drive:
		wiring["control_connection"] = drive
	if voltage:
		wiring["power_connection"] = voltage
	return wiring


def _rom_note(address: int) -> str:
	if address not in ROM_SOLENOID_NAMES:
		return ""
	name, wires = ROM_SOLENOID_NAMES[address]
	test = "T.5 FLASHER TEST" if address in T5_ADDRESSES else ("T.12 FLIPPER COIL TEST" if address in T12_ADDRESSES else "T.4 SOLENOID TEST")
	return f" {test}: the ROM pulses public {address} and prints \"{name}\" with the wires {wires}."


def solenoid_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 51):
		if address in FLIPPER_COILS:
			stage, printed, flipper, voltage, transistor, control, wire, assembly, role, number = FLIPPER_COILS[address]
			label = SOLENOID_LABELS[address]
			notes = (
				f"The {flipper} flipper's {stage} winding (coil FL-11629, printed coil colour BLUE, Flipper Assembly {assembly}), printed "
				f"flipper circuit {printed} (driver {transistor}, {control}, {wire}, supply {voltage})."
			)
			if address in {45, 46, 47, 48}:
				notes += f" The table numbers it {printed}; PinMAME publishes the lower flipper windings at 45-48."
			else:
				notes += " nfGameData declares FLIP_SOL(FLIP_L | FLIP_UR), so PinMAME publishes the upper right flipper's ROM drive at 33-34."
			if address in {45, 46, 33, 34}:
				notes += (
					" The RIGHT FLIPPER CIRCUIT page (3-12) prints the right side's J902 pins as 9/7 and 3/1, the left side's numbers; the "
					"table, the Section 3 copy and the circuit diagram (3-11) print the pins recorded here, so the page's pins are a misprint."
				)
			notes += _rom_note(address)
			notes += f" T.12 numbers it {number:02d}."
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE)
			spatial = located("solenoid", address, output_id(label), "effect")
			notes += _spatial_note("solenoid", address)
			items.append(_device(
				output_id(label), label, "coil", SOLENOID_GROUP, address, "used", refs,
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": printed}],
				roles=[role],
				physical={"part_number": "FL-11629", "assembly_part_number": assembly, "notes": notes},
				wiring={"board": "Fliptronic II board A-15472-1", "driver_transistor": transistor, "control_connection": control, "control_wire": wire, "power_connection": voltage.split(" ")[0]},
				spatial=spatial,
			))
			continue
		if address in UNUSED_FLIPPER_COILS:
			stage, transistor, control, wire = UNUSED_FLIPPER_COILS[address]
			label = SOLENOID_LABELS[address]
			notes = (
				f"The Fliptronic II upper-left {stage} circuit (driver {transistor}, {control}, {wire}, supply J907-8 RED-GRY). The table prints "
				f"its row {'NOT USED' if address == 35 else 'UPPER LEFT FLIPPER'} with coil part and colour NOT USED, the locations list prints "
				f"35-36 NOT USED, the Fliptronic II pin list prints {control} and J907-8 N/C, and the flipper-circuit page footnotes 'THE UPPER "
				"LEFT FLIPPER IS NOT USED', so no coil is fitted. nfGameData declares no upper left flipper, the ROM's T.12 FLIPPER COIL TEST "
				"offers no upper-left item, and no run here saw the address change."
			)
			items.append(_device(
				output_id(label), label, "coil", SOLENOID_GROUP, address, "unused",
				(MANUAL_SOURCE, CORE_SOURCE, FLIPPER_TEST_SOURCE),
				aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": str(address)}],
				physical={"notes": notes},
				wiring={"board": "Fliptronic II board A-15472-1", "driver_transistor": transistor, "control_wire": wire},
				spatial=not_applicable("unused", MANUAL_SOURCE),
			))
			continue
		if address in SOLENOID_TABLE:
			label = SOLENOID_LABELS[address]
			printed_type, voltage, transistor, drive, wire, part = SOLENOID_TABLE[address]
			notes = f"Printed Solenoid/Flashlamp Table entry {address:02d} ({printed_type}, driver {transistor}, wire {wire}"
			notes += f", part or flashlamp {part})." if part else ")."
			notes += " " + SOLENOID_NOTES[address]
			if address in {21, 22, 23, 24}:
				notes += SOLENOID_TYPE_NOTE
			notes += _rom_note(address)
			unused = address in {9, 13}
			kind = "flasher" if address in FLASHER_SOLENOIDS else ("magnet" if address in MAGNET_SOLENOIDS else "coil")
			physical: dict[str, Any] = {}
			if SOLENOID_ASSEMBLIES.get(address):
				physical["assembly_part_number"] = SOLENOID_ASSEMBLIES[address]
			if address in SOLENOID_PARTS:
				physical["part_number"] = SOLENOID_PARTS[address]
			if address in FLASHER_QUANTITY:
				physical["quantity"] = FLASHER_QUANTITY[address]
			refs = (MANUAL_SOURCE, CORE_SOURCE)
			refs += (FLASHER_TEST_SOURCE,) if address in T5_ADDRESSES else (SOLENOID_TEST_SOURCE,)
			if address in {10, 11}:
				refs += (EDGES_SOURCE,)
			if address in MAGNET_SOLENOIDS:
				refs += (ACCELERATOR_SOURCE,)
			if address in {1, 2, 8, 14}:
				refs += (TROUGH_TEST_SOURCE,)
			if address in {16, 21}:
				refs += (SKULL_TEST_SOURCE,)
			if address == 19:
				refs += (FLASHER_HISTORY_SOURCE,)
				notes += (
					" An earlier pinned run of the same ROM (scenario nf-flasher-test.json) already showed T.5 pulsing 19 as FLS. NO FEAR, which "
					"settled the legacy import's 'ROM Started' label on this address; no WPC generation has a game-on output at 19."
				)
			notes += f" Retained script: {SOLENOID_SCRIPT[address]}."
			refs += (VPX_SCRIPT_SOURCE,)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": _solenoid_wiring(address),
			}
			if address == 7:
				extra["roles"] = ["cabinet.knocker"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet"
			elif address in BACKBOX_FLASHERS:
				extra["roles"] = ["cabinet.backbox"]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "backbox insert panel"
				notes += " The insert-panel bulb has no playfield position."
			elif unused:
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			else:
				role = "emitter" if kind == "flasher" else "effect"
				spatial = located("solenoid", address, output_id(label), role)
				if spatial:
					extra["spatial"] = spatial
					notes += _spatial_note("solenoid", address)
					if ("solenoid", address) in CANDIDATE_PLACEMENTS:
						notes += LIGHT_MAP_NOTE
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(output_id(label), label, kind, SOLENOID_GROUP, address, "unused" if unused else "used", refs, **extra))
			continue
		label = VIRTUAL_SOLENOID_LABELS[address]
		used = address in {29, 30, 31}
		notes = {
			29: "PinMAME mirrors one of the WPC J111 general-purpose register bits here; it is not a No Fear playfield device. The service-test runs saw it change.",
			30: "PinMAME mirrors the second WPC J111 general-purpose register bit here; it is not a No Fear playfield device, and no run here saw it change.",
			31: "PinMAME publishes WPC_GILAMPS bit 7 here as the game-on / flipper-enable state because nf.c configures no fast-flip address; the service-test runs saw it change.",
			32: "PinMAME reports this WPC state channel as always zero; nfGameData declares no use for it.",
			49: "PinMAME's simulator ball-shooter channel: core_getSol serves 49 from sim_getSol, the keyboard simulator's shooter flag, and nfSimData sets 'Simulate manual shooter?' FALSE. It carries no ROM or machine state and stayed 0 in every run here; No Fear launches with the AUTO PLUNGER coil (2).",
			50: "Reserved PinMAME output position before the first custom-output boundary (51); nfGameData declares no custom solenoids.",
		}.get(address)
		if notes is None:
			transistor, wire = AUX_ROWS[address]
			notes = (
				"Unused WPC-Security output: this generation has no LPDC board, so core_getSol returns constant 0 for 37-44 outside WPC-95 and "
				f"System 11. The Solenoid/Flashlamp Table prints row {address} NOT USED (Low Power, {transistor}, {wire}) with no connection, "
				"and its footnote names the auxiliary driver board those rows would sit on."
			)
		roles = ["internal.wpc-state"] if used else ["internal.unused.wpc-output"]
		refs = (CONTROLLER_SOURCE, CORE_SOURCE) + ((MANUAL_SOURCE,) if address in AUX_ROWS else ())
		items.append(_device(
			output_id(label), label, "virtual", SOLENOID_GROUP, address, "used" if used else "unused", refs,
			aliases=[{"namespace": "pinmame.solenoid", "value": str(address)}],
			roles=roles, physical={"notes": notes}, spatial=not_applicable("virtual", CORE_SOURCE),
		))
	return items


# --- Lamp data (lamp-matrix.md, lamp-locations.md) -------------------------------------------------------
# address -> (bulb part number, lamp assembly, printed description), Lamp Locations lists (2-35).
LAMP_LOCATIONS = {
	11: ("24-8768", "A-20043", "Raceway  Awd. 3"), 12: ("24-8768", "A-20043", "Raceway Awd. 2"), 13: ("24-8768", "A-20043", "Raceway Awd. 1"),
	14: ("24-8768", "A-20043", "Lt. Over the Edge"), 15: ("24-8768", "A-20043", "Dirt"), 16: ("24-8768", "A-20043", "Asphalt"),
	17: ("24-8768", "A-20043", "No Limits"), 18: ("24-8768", "A-20043", "Water"), 21: ("24-8768", "A-20043", "No Fear"),
	22: ("24-8768", "A-20043", "Raceway Awd. 4"), 23: ("24-8768", "A-20043", "Raceway Awd. 5"), 24: ("24-8768", "A-20043", "Rt. Over the Edge"),
	25: ("24-8768", "A-20043", "Air"), 26: ("24-8768", "A-20043", "Snow"), 27: ("24-8768", "A-20043", "Fear Fest"),
	28: ("24-8768", "A-20043", "Meet Your Maker"), 31: ("24-8768", "A-20041", "Skull"), 32: ("24-8768", "A-20041", "Right Track"),
	33: ("24-8768", "A-20041", "Center Jackpot"), 34: ("24-8768", "A-20041", "Extra Ball"), 35: ("24-8768", "A-20041", "Start Challenge"),
	36: ("24-8768", "A-20041", "Center Lock"), 37: ("24-6549", "A-17835", "Right Autofire (2)"), 38: ("24-8768", "B-12224", "Left Hurry Up"),
	41: ("24-8768", "A-20041", "Left Track"), 42: ("24-8768", "A-20041", "First Place"), 43: ("24-8768", "A-20041", "Second Place"),
	44: ("24-8768", "A-20041", "Third Place"), 45: ("24-6549", "A-17807", "Skydive"), 46: ("24-8768", "A-20041", "Drop Jackpot"),
	47: ("24-8768", "A-20041", "Drop Lock"), 48: ("24-6549", "A-17835", "Left Autofire (2)"), 51: ("24-8768", "A-20044", "Raceway"),
	52: ("24-8768", "A-20044", "Left Ramp Turn"), 53: ("24-8768", "A-20044", "Super Spinner"), 54: ("24-8768", "A-20044", "Left Ramp Start"),
	55: ("24-8768", "A-20044", "Left Ramp Win"), 56: ("24-8768", "A-20044", "Hill Climb"), 57: ("24-8768", "A-20044", "Screamer"),
	58: (None, None, "NOT USED"), 61: ("24-6549", "A-17807", "Tube"), 62: ("24-8768", "A-20044", "Video Mode"),
	63: ("24-8768", "A-20042", "Right Ramp Win"), 64: ("24-8768", "A-20042", "Right Ramp Turn"), 65: ("24-8768", "A-20042", "Right Ramp Start"),
	66: ("24-6549", "A-17835", "Left Flipper Lane"), 67: ("24-6549", "A-17807", "Left Outlane"), 68: ("24-6549", "A-17835", "Kickback"),
	71: ("24-6549", "A-17835", "Light Kickbck Top"), 72: ("24-6549", "A-17835", "Light Kickbck Bttm"), 73: ("24-6549", "A-17835", "Right Flipper Lane"),
	74: ("24-6549", "A-17835", "Right Outlane"), 75: ("24-6549", "A-17807", "Hairpin"), 76: ("24-6549", "A-17835", "Downhill"),
	77: ("24-6549", "A-17807", "Summit"), 78: ("24-6549", "A-17835", "Right Hurry Up"), 81: ("24-6549", "A-17807", "Shoot Again"),
	82: ("24-6549", "04-10083", "Left Skull Eye"), 83: ("24-8768", "B-12224", "Jump Now"), 84: ("24-8768", "B-12224", "Super Jackpot"),
	85: ("24-6549", "04-10083", "Right Skull Eye"), 86: (None, "20-9663-B-8", "Ball Launch"), 87: (None, "20-9663-18", "Buy-in Button"),
	88: (None, "20-9663-1", "Start Button"),
}
LAMP_LABELS = {
	11: "Raceway Award 3 (15 Million)", 12: "Raceway Award 2 (10 Million)", 13: "Raceway Award 1 (5 Million)", 14: "Left Over the Edge",
	15: "Dirt", 16: "Asphalt", 17: "No Limits", 18: "Water", 21: "No Fear", 22: "Raceway Award 4 (20 Million)",
	23: "Raceway Award 5 (Light Extra Ball)", 24: "Right Over the Edge", 25: "Air", 26: "Snow", 27: "Fear Fest", 28: "Meet Your Maker",
	31: "Skull", 32: "Right Track", 33: "Center Jackpot", 34: "Extra Ball", 35: "Start Challenge", 36: "Center Lock", 37: "Right Autofire",
	38: "Left Hurry Up", 41: "Left Track", 42: "First Place", 43: "Second Place", 44: "Third Place", 45: "Skydive", 46: "Drop Jackpot",
	47: "Drop Lock", 48: "Left Autofire", 51: "Raceway", 52: "Left Ramp Turn", 53: "Super Spinner", 54: "Left Ramp Start",
	55: "Left Ramp Win", 56: "Hill Climb", 57: "Screamer", 58: "Not Used Lamp 58", 61: "Tube", 62: "Video Mode", 63: "Right Ramp Win",
	64: "Right Ramp Turn", 65: "Right Ramp Start", 66: "Left Flipper Lane", 67: "Left Outlane", 68: "Kickback", 71: "Light Kickback Top",
	72: "Light Kickback Bottom", 73: "Right Flipper Lane", 74: "Right Outlane", 75: "Hairpin", 76: "Downhill", 77: "Summit",
	78: "Right Hurry Up", 81: "Shoot Again", 82: "Left Skull Eye", 83: "Jump Now", 84: "Super Jackpot", 85: "Right Skull Eye",
	86: "Ball Launch Button", 87: "Buy-In Button", 88: "Start Button",
}
# The matrix cell text where the label does not reproduce it (lamp-matrix.md).
LAMP_MATRIX_TEXT = {
	11: "RACEWAY AWARD 3", 12: "RACEWAY AWARD 2", 13: "RACEWAY AWARD 1", 22: "RACEWAY AWARD 4", 23: "RACEWAY AWARD 5",
	37: "RIGHT AUTOFIRE (2)", 48: "LEFT AUTOFIRE (2)", 86: "BALL LAUNCH", 87: "BUY-IN BUTTON", 88: "START BUTTON",
}
LAMP_COLUMN_WIRING = {
	1: ("Yellow-Brown", "J137-1", "Q98"), 2: ("Yellow-Red", "J137-2", "Q97"), 3: ("Yellow-Orange", "J137-3", "Q96"),
	4: ("Yellow-Black", "J137-4", "Q95"), 5: ("Yellow-Green", "J137-5", "Q94"), 6: ("Yellow-Blue", "J137-6", "Q93"),
	7: ("Yellow-Violet", "J137-7", "Q92"), 8: ("Yellow-Gray", "J137-9", "Q91"),
}
LAMP_ROW_WIRING = {
	1: ("Red-Brown", "J134-1", "Q90"), 2: ("Red-Black", "J134-2", "Q89"), 3: ("Red-Orange", "J134-4", "Q88"),
	4: ("Red-Yellow", "J134-5", "Q87"), 5: ("Red-Green", "J134-6", "Q87"), 6: ("Red-Blue", "J134-7", "Q86"),
	7: ("Red-Violet", "J134-8", "Q84"), 8: ("Red-Gray", "J134-9", "Q83"),
}
# The ROM's T.8 SINGLE LAMPS names (single-lamps run).
ROM_LAMP_NAMES = {
	11: "15 MILLION", 12: "10 MILLION", 13: "5 MILLION", 14: "L. OVER THE EDGE", 15: "DIRT", 16: "ASPHALT", 17: "NO LIMITS",
	18: "WATER", 21: "NO FEAR", 22: "20 MILLION", 23: "LIGHT EXTRA BALL", 24: "R. OVER THE EDGE", 25: "AIR", 26: "SNOW",
	27: "FEAR FEST", 28: "MEET YOUR MAKER", 31: "SKULL", 32: "R. TRACK", 33: "CENTER JACKPOT", 34: "EXTRA BALL",
	35: "START CHALLENGE", 36: "CENTER LOCK", 37: "R. AUTOFIRE (2)", 38: "L. HURRY UP", 41: "L. TRACK", 42: "1ST", 43: "2ND",
	44: "3RD", 45: "SKYDIVE", 46: "DROP JACKPOT", 47: "DROP LOCK", 48: "L. AUTOFIRE (2)", 51: "RACEWAY", 52: 'L. RAMP "TURN"',
	53: "SUPER SPIN", 54: 'L. RAMP "START"', 55: 'L. RAMP "WIN!"', 56: "HILL CLIMB", 57: "SCREAMER", 58: "UNUSED", 61: "TUBE",
	62: "VIDEO MODE", 63: 'R. RAMP "WIN!"', 64: 'R. RAMP "TURN"', 65: 'R. RAMP "START"', 66: "L. FLIPPER LANE", 67: "L. OUTLANE",
	68: "KICKBACK", 71: "LIGHT KB. TOP", 72: "LIGHT KB. BOTTOM", 73: "R. FLIPPER LANE", 74: "R. OUTLANE", 75: "HAIRPIN",
	76: "DOWNHILL", 77: "SUMMIT", 78: "R. HURRY UP", 81: "SHOOT AGAIN", 82: "L. SKULL EYE", 83: "JUMP NOW", 84: "SUPER JACKPOT",
	85: "R. SKULL EYE", 86: "BALL LAUNCH", 87: "BUY-IN BUTTON", 88: "START BUTTON",
}
ROW_WIRE = ("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")
COLUMN_WIRE = ("BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY")
LAMP_BOARDS = {"A-20043": "16-Lamp Board Assembly", "A-20041": "12-Lamp PCB Assembly", "A-20044": "8-Lamp Board Assembly", "A-20042": "3-Lamp Board Assembly"}
CABINET_LAMPS = {86: ("cabinet.launch-button-lamp", "Ball Launch"), 87: ("cabinet.buy-in", "Buy Extra Ball"), 88: ("cabinet.start-button-lamp", "Start")}
# What the retained script does with each cabinet button lamp besides mapping its invisible light through AllLamps.
CABINET_LAMP_SCRIPT = {
	86: "; FrameTimer_Timer lights the cabinet primitive LaunchButton from l86 (LaunchButton.blenddisablelighting = 0.2 * l86.state)",
	87: "; nothing else in the script reads l87",
	88: "; FrameTimer_Timer shows the Flasher f88 while l88 is on (f88.visible = l88.state)",
}


def lamp_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for column in range(1, 9):
		for row in range(1, 9):
			address = column * 10 + row
			bulb, assembly, description = LAMP_LOCATIONS[address]
			drive_wire, drive_connection, column_driver = LAMP_COLUMN_WIRING[column]
			return_wire, return_connection, row_driver = LAMP_ROW_WIRING[row]
			physical: dict[str, Any] = {}
			if bulb:
				physical["quantity"] = 2 if address in {37, 48} else 1
				physical["part_number"] = bulb
			if assembly:
				physical["assembly_part_number"] = assembly
			bulb_name = {"24-8768": "#555", "24-6549": "#44"}.get(bulb or "")
			notes = f"Printed lamp-matrix drive column {column} ({drive_wire}), return row {row} ({return_wire}). Lamp Locations description \"{description}\""
			if bulb:
				notes += f", bulb {bulb} ({bulb_name})."
			elif address == 58:
				notes += ", with blank bulb and assembly cells."
			else:
				notes += f", bulb printed '-------' and assembly {assembly}."
			if address in LAMP_MATRIX_TEXT:
				notes += f" The matrix cell prints \"{LAMP_MATRIX_TEXT[address]}\"."
			if assembly in LAMP_BOARDS:
				notes += f" Its socket is on the {LAMP_BOARDS[assembly]} {assembly}."
			notes += (
				f" The Power Driver Board's pin list (3-30) prints J137 Not Used and routes the playfield lamp columns on J138-{(1, 2, 3, 4, 5, 6, 7, 9)[column - 1]}, "
				"where the Lamp Matrix prints J137; the rows on J134 and the wire colours agree, so the connector is a wiring detail and the "
				"wiring record follows the game's own matrix page."
			)
			if row in {4, 5}:
				notes += " The matrix prints transistor Q87 for both rows 4 and 5 (and no Q85); the record keeps the printed designator."
			notes += (
				f" The ROM's T.8 SINGLE LAMPS TEST lights public lamp {address} alone and names it \"{ROM_LAMP_NAMES[address]}\" "
				f"(RED-{ROW_WIRE[row - 1]} YEL-{COLUMN_WIRE[column - 1]})."
			)
			extra: dict[str, Any] = {
				"aliases": [{"namespace": "pinmame.lamp", "value": str(address)}, {"namespace": "manual.address", "value": f"{address:02d}"}],
				"wiring": {
					"board": "WPC power driver board A-12697-3", "drive_wire": drive_wire, "drive_connection": drive_connection,
					"return_wire": return_wire, "return_connection": return_connection,
					"driver_transistor": f"{column_driver} column driver with {row_driver} row driver",
				},
			}
			refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, LAMP_TEST_SOURCE)
			availability = "used"
			if address == 58:
				notes += (
					" The matrix and the list print NOT USED and the list gives no bulb or assembly, so no lamp is fitted; T.8 still lights the "
					"position and prints UNUSED, which is the sweep, not a fitted load. The retained table binds no light to it."
				)
				availability = "unused"
				extra["spatial"] = not_applicable("unused", MANUAL_SOURCE)
			elif address in CABINET_LAMPS:
				role, button = CABINET_LAMPS[address]
				extra["roles"] = [role]
				extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
				physical["location"] = "cabinet button"
				notes += (
					f" The lamp inside the lit {button} button: the list gives the button's part as its assembly, the same part the switch list "
					"gives the button's switch. The Power Driver Board's pin list brings lamp column 8 to the cabinet on J136-3 and rows 6-8 on "
					"J135-7 to J135-9. Retained script: vpmMapLights AllLamps maps the invisible light "
					f"l{address}, placed on the apron (TimerInterval {address}), to it{CABINET_LAMP_SCRIPT[address]}."
				)
				refs += (VPX_SCRIPT_SOURCE,)
			else:
				identifier = f"lamp.matrix-{address}"
				spatial = located("lamp", address, identifier, "emitter")
				if spatial:
					extra["spatial"] = spatial
				if address in {37, 48}:
					notes += " The list's '(2)' and the ROM's '(2)' make this circuit two bulbs; the table models one light, which is the only placement."
				if address in {38, 83, 84}:
					notes += " Its socket is a B-12224 sign lamp assembly raised above the playfield."
				if address in {82, 85}:
					notes += " One of the skull's two #44 eye bulbs (socket 04-10083; the skull's unit-disassembly page counts two #906 and two #44 bulbs)."
				notes += f" Retained script: vpmMapLights AllLamps maps the light l{address} (TimerInterval {address}) to it."
				notes += _spatial_note("lamp", address)
				if ("lamp", address) in CANDIDATE_PLACEMENTS:
					notes += LIGHT_MAP_NOTE
				refs += (VPX_SCRIPT_SOURCE,)
			physical["notes"] = notes
			extra["physical"] = physical
			items.append(_device(f"lamp.matrix-{address}", LAMP_LABELS[address], "lamp", LAMP_GROUP, address, availability, refs, **extra))
	return items


# --- General illumination (solenoid-flasher-table.md G.I. block; power-driver-board.md; gi-test run) -----------
# public -> (string, name, triac, voltage connections, drive connections, wire, bulbs, ROM name, ROM wires, location)
GI_STRINGS = {
	0: (1, "Playfield Top", "Q18", "J121-1", "J121-7", "WHT-BRN", "#555", "PLAYFIELD TOP", "WHT-BRN BRN", "playfield"),
	1: (2, "Playfield Right", "Q10", "J121-2, J120-2", "J121-8, J120-8", "WHT-ORG", "#555 and #44", "PLAYFIELD RIGHT", "WHT-ORN ORN", "playfield"),
	2: (3, "Playfield Left", "Q14", "J121-3", "J121-9", "WHT-YEL", "#555", "PLAYFIELD LEFT", "WHT-YEL YEL", "playfield"),
	3: (4, "Insert Title", "Q16", "J120-5", "J120-10", "WHT-GRN", "#44", "INSERT TITLE", "WHT-GRN GRN", "backbox"),
	4: (5, "Insert Background", "Q12", "J120-6, J119-3", "J120-11, J119-1", "WHT-VIO", "#44", "INSERT BKGROUND", "WHT-VIO VIO", "backbox"),
}
GI_TABLE_COLUMNS = {
	0: "prints J121-1 / J121-7 and the #555 bulb under its BACKBOX columns",
	1: "prints J120-2 / J120-8 with #44 under its PLAYFIELD columns and J121-2 / J121-8 with #555 under its BACKBOX columns",
	2: "prints J121-3 / J121-9 and the #555 bulb under its BACKBOX columns",
	3: "prints J120-5 / J120-10 and the #44 bulb under its PLAYFIELD columns",
	4: "prints J120-6 / J120-11 and the #44 bulb under its PLAYFIELD columns and J119-3 / J119-1 under its CABINET columns",
}
GI_COLUMN_NOTE = (
	" The table's PLAYFIELD and BACKBOX columns are swapped against everything else: the Power Driver Board's pin list sends J121 'G.I. to "
	"playfield' and J120 'G.I. to insert panel', and the string names, the ROM's own T.6 names and the bulbs (#555 on the playfield J121 "
	"pins, #44 on the insert-panel J120 pins) agree with the board list. The record follows the board list; the table's column placement "
	"is a printing disagreement of that one table, kept literally in the excerpt."
)


def gi_outputs() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, (string, name, triac, voltage, drive, wire, bulbs, rom_name, rom_wires, location) in GI_STRINGS.items():
		notes = (
			f"Printed general-illumination row {string:02d} '{name.upper()}': triac {triac}, wire {wire}, bulbs {bulbs}. The table "
			f"{GI_TABLE_COLUMNS[address]}." + GI_COLUMN_NOTE +
			f" The locations list's G.I. item {string:02d} is '{name}'. The ROM's T.6 GENERAL ILLUMINATION TEST names it '{rom_name}' "
			f"({rom_wires}) and steps its brightness on public GI {address} alone."
		)
		extra: dict[str, Any] = {
			"aliases": [{"namespace": "pinmame.gi", "value": str(address)}, {"namespace": "manual.address", "value": f"{string:02d}"}],
			"wiring": {"board": "WPC power driver board A-12697-3", "driver_transistor": triac, "control_connection": drive, "control_wire": wire, "power_connection": voltage},
		}
		refs: tuple[str, ...] = (MANUAL_SOURCE, CORE_SOURCE, GI_TEST_SOURCE)
		if location == "backbox":
			notes += " It lights the backbox insert panel" + (" and, through J119, the coin door." if address == 4 else ".")
			notes += f" Retained script: UpdateGI has no active case for {address}."
			extra["roles"] = ["cabinet.backbox"]
			extra["spatial"] = not_applicable("cabinet_or_service", MANUAL_SOURCE)
			extra["physical"] = {"location": "backbox", "notes": notes}
			refs += (VPX_SCRIPT_SOURCE,)
		else:
			if address == 1:
				notes += " Besides its playfield #555 bulbs it feeds #44 bulbs on the insert panel (J120-2 / J120-8); those have no playfield position."
			spatial = located("gi", address, f"gi.string-{string}", "emitter")
			notes += (
				f" Retained script: GiCallBack2 UpdateGI switches the light collection {('GI_Top', 'GI_Right', 'GI_Left')[address]} from public GI "
				f"{address}; its lights are invisible light-map sources with no bulb of their own, so they give only candidate placements, "
				f"and their number is the table's, not a bulb count."
			)
			notes += _spatial_note("gi", address)
			if spatial:
				extra["spatial"] = spatial
			extra["physical"] = {"notes": notes}
			refs += (VPX_SCRIPT_SOURCE,)
		items.append(_device(f"gi.string-{string}", f"General Illumination {name}", "gi", GI_GROUP, address, "used", refs, **extra))
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
			"provenance": provenance("validated", CORE_SOURCE, MANUAL_SOURCE),
		},
	]


# --- Mechanisms, drivers and conflicts -------------------------------------------------------------------
def _coil(address: int) -> str:
	return output_id(SOLENOID_LABELS[address])


def _mechanism(
	suffix: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, refs: tuple[str, ...],
	positions: list[tuple[str, str, list[str], str]] | None = None, assembly: str | None = None, status: str = "observed",
) -> dict[str, Any]:
	record: dict[str, Any] = {
		"id": f"mechanism.{suffix}", "label": label, "kind": kind, "actuators": actuators, "sensors": sensors,
		"behavior": behavior, "provenance": provenance(status, *refs),
	}
	if assembly:
		record["assembly_part_number"] = assembly
	if positions:
		record["positions"] = [
			{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description}
			for position_id, position_label, position_sensors, description in positions
		]
	return record


def _matrix(*addresses: int) -> list[str]:
	return [f"switch.matrix-{address}" for address in addresses]


def mechanisms() -> list[dict[str, Any]]:
	flipper_refs = (MANUAL_SOURCE, CORE_SOURCE, EDGES_SOURCE, FLIPPER_TEST_SOURCE)
	return [
		_mechanism(
			"ball-accelerator", "Magnetic ball accelerator", "other", [_coil(6), _coil(5), _coil(3)], _matrix(46, 47, 48),
			"Three magnets on the Back Panel Assembly A-20033, the left (6, 20-10197), centre (5, 20-10197-1) and right (3, 20-10197-2) "
			"Coil Magnet/Breaker assemblies, each on an Opto Mounting Bracket A-20034 with an opto ahead of it: left (46), centre (47) and "
			"right (48). They throw the ball along the accelerator up the jump ramp (IPDB calls the toy a magnetic ball accelerator; the "
			"rules' skill shot and JUMP shots are shots up this ramp). The ROM fires each magnet once when its own opto is blocked: in T.16 "
			"BALL ACCELERATOR TEST a 150 ms pulse of 46 fired 6, of 47 fired 5 and of 48 fired 3, and a magnet that Enter had disabled fired "
			"nothing for its opto. Each magnet carries a thermal breaker that cuts it off when it overheats, and its opto must work for the "
			"magnet to capture and throw the ball (manual T.16). The retained known-working table approximates the throw: while a magnet's "
			"output is on, a ball over its trigger (LeftMagnet, CenterMagnet, RightMagnet) moving right is set to a fixed speed, and the ball "
			"is stopped past the right trigger when the centre magnet is on and the right one off; the ROM decides when each fires.",
			(MANUAL_SOURCE, IDENTITY_SOURCE, ACCELERATOR_SOURCE, SOLENOID_TEST_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("left", "Left magnet", _matrix(46), "The ball blocks the left opto; the left magnet (6) fires."),
				("centre", "Centre magnet", _matrix(47), "The ball blocks the centre opto; the centre magnet (5) fires."),
				("right", "Right magnet", _matrix(48), "The ball blocks the right opto; the right magnet (3) fires."),
			],
			"A-20033",
		),
		_mechanism(
			"underground-trough", "Underground trough and right popper", "kicker", [_coil(1)], _matrix(38, 37, 42, 41),
			"The Underside Ball Trough Assy. A-19948 carries a ball from the top of the playfield, behind the drop target and under the "
			"skull, to the lower right popper (manual T.18). It has two entrances, the left one behind the drop target (38, LEFT ENTR.) and "
			"the centre one (37, CTR. ENTR.); a ball passes POPPER 2 (42) and settles on POPPER 1 (41) in the Ball Popper Assembly A-19965, "
			"and the RIGHT POPPER coil (1) kicks it back onto the playfield. In T.18 UNDERGROUND TROUGH TEST the MANUAL mode pulses the DROP "
			"TARGET DOWN coil (8) as it starts and when 38 closes, so a ball can reach the left entrance; the AUTOMATIC cycle ejected a ball "
			"from the trough (14), fired the auto plunger (2) with the shooter lane switch (15) closed, and fired the popper (1) once 41 was "
			"held after 38, 37 and 42 had been pulsed. The retained known-working table holds the ball on the trigger sw41 and kicks it "
			"upward from there.",
			(MANUAL_SOURCE, TROUGH_TEST_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("left-entrance", "Left entrance", _matrix(38), "A ball enters behind the drop target."),
				("centre-entrance", "Centre entrance", _matrix(37), "A ball enters at the centre."),
				("popper-2", "Popper 2", _matrix(42), "The ball passes the popper's second opto."),
				("popper-1", "Popper 1", _matrix(41), "The ball rests in the popper; the right popper coil (1) kicks it out."),
			],
			"A-19948",
		),
		_mechanism(
			"ball-trough", "Ball trough", "kicker", [_coil(14)], _matrix(31, 32, 33, 34, 35),
			"Outhole Ball Trough Assembly A-19963 (the locations list prints A-19663) with the Trough IR LED and photo transistor boards and "
			"four balls: drained balls collect over BALL 1-4 (32-35, position 1 at the eject end) and the trough coil (14) kicks the ball at "
			"the eject end into the shooter lane; the JAM BALL opto (31, TROUGH STACK) sees a ball stacked over it. The optos read a ball at "
			"public 1. The retained known-working table pulses 31 on each eject and rolls the remaining balls down.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, TROUGH_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			[
				("trough-stack", "Trough stack", _matrix(31), "A ball stacked over the ball at the eject end."),
				("trough-1", "Trough, 1 ball", _matrix(32), "At least one ball in the trough."),
				("trough-2", "Trough, 2 balls", _matrix(33), "At least two balls."),
				("trough-3", "Trough, 3 balls", _matrix(34), "At least three balls."),
				("trough-4", "Trough, 4 balls", _matrix(35), "All four balls."),
			],
			"A-19963",
		),
		_mechanism(
			"drop-target", "Drop target", "drop_target_bank", [_coil(8), _coil(12)], _matrix(51),
			"A single drop target (1-Bank Drop Target Assembly A-14615; the playfield list calls the target A-20202) in front of the "
			"underground trough's left entrance, with its switch on 51: DROP TARGET DOWN (8, SM1-26-600) knocks it down and DROP TARGET UP "
			"(12, AE-26-1200) resets it. Hitting it lights the locks (rules page 20). T.17 DROP TARGET TEST pulses the two coils and shows "
			"51's state.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, TROUGH_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE),
			[("up", "Up", [], "The target stands; the left entrance is blocked."), ("down", "Down", [], "The target is down; a ball can reach the left entrance.")],
			"A-14615",
		),
		_mechanism(
			"skull", "Talking skull", "toy", [_coil(16)], [],
			"The Skull Assembly A-20142 on the Skull Base Assembly A-20144: the SKULL MOUTH coil (16, SM-30-1100-DC with a compression "
			"spring) opens the lower jaw, which sits in the base. The skull carries two #906 bulbs on the SKULL flasher circuit (21) and two "
			"#44 eye bulbs (lamps 82 and 85). The ROM's T.19 SKULL TEST pulses 16 with 21 while it plays speech calls. The retained "
			"known-working table rotates its jaw primitives from 16.",
			(MANUAL_SOURCE, SKULL_TEST_SOURCE, SOLENOID_TEST_SOURCE, FLASHER_TEST_SOURCE, VPX_SCRIPT_SOURCE), None, "A-20144",
		),
		_mechanism(
			"auto-plunger", "Auto plunger", "kicker", [_coil(2)], _matrix(15, 11),
			"The AUTO PLUNGER coil (2, AE-23-800, assembly A-14525) launches the ball resting on the shooter lane switch (15); the cabinet "
			"BALL LAUNCH button (11, lamp 86) asks for it. In T.18's AUTOMATIC cycle the ROM fired 2 while 15 was closed and dropped it when "
			"15 opened.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, TROUGH_TEST_SOURCE, VPX_SCRIPT_SOURCE), None, "A-14525",
		),
		_mechanism(
			"kickback", "Kickback", "kicker", [_coil(4)], _matrix(25),
			"The KICKBACK coil (4, AE-23-800, Bottom Arch Kicker Assembly B-11873) fires a ball on the kickback lane switch (25) back into "
			"play when lamp 68 KICKBACK is lit; the LIGHT KICKBACK targets (56, 57; lamps 72 and 71) relight it.",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, LAMP_TEST_SOURCE, VPX_SCRIPT_SOURCE), None, "B-11873",
		),
		_mechanism(
			"eject-hole", "Eject hole", "kicker", [_coil(15)], _matrix(61),
			"The EJECT coil (15, AE-27-1200, Eject Assembly A-20134 with plunger A-15371) kicks a ball out of the eject hole (61).",
			(MANUAL_SOURCE, SOLENOID_TEST_SOURCE, EDGES_SOURCE, VPX_SCRIPT_SOURCE), None, "A-20134",
		),
		_mechanism(
			"slingshots", "Slingshots", "kicker", [_coil(11), _coil(10)], _matrix(27, 28),
			"Two slingshots (Kicker Arm Assembly A-17811 with Coil & Bracket Assy. B-9362-L-2 left and B-9362-R-3 right, AE-26-1200 coils) "
			"with kick and score switches on 27 and 28; the ROM fired 11 for 27 and 10 for 28 even inside the T.1 test.",
			(MANUAL_SOURCE, EDGES_SOURCE, SOLENOID_TEST_SOURCE),
		),
		_mechanism(
			"lower-right-flipper", "Lower right flipper", "other", [_coil(45), _coil(46)], ["switch.generic-111", "switch.generic-112", "switch.generic-116"],
			"Flipper Assembly A-14876-R-3 with an FL-11629 coil (power 45, hold 46) and an end-of-stroke switch (F1, 111) that PinMAME "
			"synthesizes. The right cabinet button's board carries two optos, F2 (112) and F6 (116), and the ROM fires this flipper from either.",
			flipper_refs, None, "A-14876-R-3",
		),
		_mechanism(
			"lower-left-flipper", "Lower left flipper", "other", [_coil(47), _coil(48)], ["switch.generic-113", "switch.generic-114", "switch.generic-118"],
			"Flipper Assembly A-15849-L-2 with an FL-11629 coil (power 47, hold 48) and an end-of-stroke switch (F3, 113) that PinMAME "
			"synthesizes. The left cabinet button's board carries two optos, F4 (114) and F8 (118), and the ROM fires this flipper from either.",
			flipper_refs, None, "A-15849-L-2",
		),
		_mechanism(
			"upper-right-flipper", "Upper right flipper", "other", [_coil(33), _coil(34)], ["switch.generic-115", "switch.generic-116"],
			"Flipper Assembly A-19945 (Flipper Assembly, Upper Right) with an FL-11629 coil (power 33, hold 34) and an end-of-stroke switch "
			"(F5, 115) that PinMAME synthesizes, worked by the right button's second opto (F6, 116); the right button therefore fires both "
			"right flippers.",
			flipper_refs, None, "A-19945",
		),
	]


def relationships() -> list[dict[str, Any]]:
	return []


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
TRANSCRIBED = "curator, read from the rendered page"
DELEGATED = "delegated transcription from the rendered page; spot-checked by the curator, not checked cell by cell"
CHECKED = "delegated transcription from the rendered page; checked against the page by the curator"


def _excerpt(name: str, locator: str, *, method: str = "manual", reviewed: bool = True, credit: str = TRANSCRIBED) -> dict[str, Any]:
	return {
		"id": f"excerpt.no-fear.{name}",
		"locator": locator,
		"path": f"evidence/excerpts/{MACHINE_ID}/{name}.md",
		"sha256": EXCERPT_FILE_HASHES[f"{name}.md"],
		"method": method,
		"transcribed_by": credit,
		"reviewed": reviewed,
	}


def _manual_excerpts() -> list[dict[str, Any]]:
	return [
		_excerpt("front-matter", "PDF pages 1-9: cover, DIP SWITCH SETTINGS AND JUMPERS (page 2), the Security CPU and interlock notices and the table of contents", method="mixed", reviewed=False, credit=DELEGATED),
		_excerpt("game-rules", "PDF pages 10-20, the rules divider, RULES and the shot-map pages", method="mixed", reviewed=False, credit=DELEGATED),
		_excerpt("service-tests", "PDF pages 28-39, printed 1-8 to 1-18, the menu system and T.1-T.20; PDF pages 61-63, printed 1-41 to 1-43, error messages and opto theory", method="mixed", reviewed=False, credit=DELEGATED),
		_excerpt("mechanism-assemblies", "PDF pages 67-73, printed 1-47 to 1-53, unit disassembly (skull, ramps, magnets, underground trough); PDF pages 86-98 and 103-106, printed 2-13 to 2-25 and 2-30 to 2-33, every row of the assembly, playfield and ramp parts lists", method="mixed", reviewed=False, credit="delegated transcription from the rendered page; the parts tables checked row by row against "
			"the page by the curator, the unit-disassembly prose OCR-based and not checked line by line"),
		_excerpt("lamp-matrix", "PDF page 107, printed 2-34, Lamp Matrix Table; Section 3 copy PDF page 117 (3-4) compared", credit=CHECKED),
		_excerpt("lamp-locations", "PDF page 108, printed 2-35, Lamp Locations lists and bulb legend", reviewed=False, credit=DELEGATED),
		_excerpt("switch-matrix", "PDF page 109, printed 2-36, Switch Matrix Table with the dedicated and flipper columns and the opto shading; Section 3 copy PDF page 115 (3-2) compared; DEDICATED SWITCHES drawing PDF page 116 (3-3)", credit=CHECKED),
		_excerpt("switch-locations", "PDF page 110, printed 2-37, Switch Locations lists", reviewed=False, credit=DELEGATED),
		_excerpt("solenoid-flasher-table", "PDF page 111, printed 2-38, Solenoid/Flashlamp Table with its GENERAL ILLUMINATION and FLIPPER CIRCUITS blocks; Section 3 copy PDF page 118 (3-5) and the PDF page 2 copy compared", credit="delegated transcription from the rendered page; checked cell by cell against the page by the curator"),
		_excerpt("solenoid-flasher-locations", "PDF page 112, printed 2-39, Solenoid/Flashlamp Locations, flipper and G.I. lists and bulb legend", credit=CHECKED),
		_excerpt("solenoid-wiring-pages", "PDF pages 119-123, printed 3-6 to 3-10, coil and flashlamp wiring drawings and driver-circuit pages", reviewed=False, credit=DELEGATED),
		_excerpt("flipper-circuits", "PDF pages 124-126, printed 3-11 to 3-13, flipper circuit diagram, coil and end-of-stroke circuits and cabinet switch circuit", reviewed=False, credit=DELEGATED),
		_excerpt("opto-boards", "PDF pages 127-134, printed 3-14 to 3-21, Flipper Opto Board, trough boards, single LED and photo transistor boards and the 16-Opto Switch Board; PDF pages 84-85, printed 2-11 and 2-12, their parts lists", reviewed=False, credit=DELEGATED),
		_excerpt("coin-door-board", "PDF page 135, printed 3-22, Coin Door Interface Board A-17051-1", reviewed=False, credit=DELEGATED),
		_excerpt("cpu-board", "PDF page 137, printed 3-24, Security CPU Board A-17651-50025 interboard wiring list", reviewed=False, credit=DELEGATED),
		_excerpt("fliptronic-board", "PDF page 140, printed 3-27, Fliptronic II Board A-15472-1 interboard wiring list", reviewed=False, credit=DELEGATED),
		_excerpt("power-driver-board", "PDF pages 141-143, printed 3-28 to 3-30, Power Driver Board A-12697-3 interboard wiring list", credit="delegated transcription from the rendered page; the PDF page 142 list checked against the page by the curator"),
	]


RUNTIME_SOURCES = (
	(EDGES_SOURCE, "switch-edges", "One hash-pinned LibPinMAME harness run of nf_23x from empty NVRAM with built-in mechanisms disabled (tools/harness-scenarios/wpc-security/nf-switch-edges.json): inside T.1 SWITCH EDGES every public matrix address 11-88 except 22 and every Fliptronic address 111-118 is set to 1 and back to 0. The ROM names each fitted switch at public 1 (24 on its 1 -> 0 edge), shows UNUSED for 12, 36, 43-45, 52, 53, 65 and 68, reports no edge in matrix columns 7 and 8, fires the slingshot coils 11 and 10 for 27 and 28, the lower right flipper for 112, the lower right and upper right flippers for 116 and the lower left flipper for 114 and 118; 111, 113 and 115 read back 0."),
	(SOLENOID_TEST_SOURCE, "solenoid-test", "One hash-pinned run of nf_23x (nf-solenoid-test.json) stepping T.4 SOLENOID TEST: it walks 01-16, offering 09 and 13 as UNUSED, naming each driver and its wires and pulsing that public address, and wraps to 01."),
	(FLASHER_TEST_SOURCE, "flasher-names", "One hash-pinned run of nf_23x (nf-flasher-names.json) stepping T.5 FLASHER TEST through 17-28, each named with its wires and pulsed, and wrapping to 17."),
	(FLIPPER_TEST_SOURCE, "flipper-coil-test", "One hash-pinned run of nf_23x (nf-flipper-coil-test.json) stepping T.12 FLIPPER COIL TEST: R. FLIP. POWER drives 45 and 46, R. FLIP. HOLD 46, L. FLIP. POWER 47 and 48, L. FLIP. HOLD 48, U.R. FLIP. POWER 33 and 34, U.R. FLIP. HOLD 34; it offers no upper-left item."),
	(GI_TEST_SOURCE, "gi-test", "One hash-pinned run of nf_23x (nf-gi-test.json) stepping T.6 GENERAL ILLUMINATION TEST: ALL ILLUMINATION dims public GI 0-4 together, then PLAYFIELD TOP, PLAYFIELD RIGHT, PLAYFIELD LEFT, INSERT TITLE and INSERT BKGROUND dim GI 0-4 alone in that order."),
	(LAMP_TEST_SOURCE, "single-lamps", "One hash-pinned run of nf_23x (nf-single-lamps.json) stepping T.8 SINGLE LAMPS TEST through public lamps 11-88, each lit alone and named with its wires, and wrapping to 11; 58 is named UNUSED."),
	(ACCELERATOR_SOURCE, "ball-accelerator-test", "One hash-pinned run of nf_23x (nf-ball-accelerator-test.json) in T.16 BALL ACCELERATOR TEST: a 150 ms pulse of ramp opto 46, 47 or 48 makes the ROM fire the left (6), centre (5) or right (3) magnet once while that magnet is enabled, and nothing once Enter has disabled it."),
	(TROUGH_TEST_SOURCE, "underground-trough-test", "One hash-pinned run of nf_23x (nf-underground-trough-test.json) in T.18 UNDERGROUND TROUGH TEST: MANUAL pulses the drop target down coil (8) as it starts and when the left entrance 38 closes and marks 38, 37, 42 and 41; AUTOMATIC fires the trough coil (14) until trough position 4 (35) opens, the auto plunger (2) while the shooter lane switch 15 is closed, and the right popper (1) while popper opto 41 is held."),
	(SKULL_TEST_SOURCE, "skull-test", "One hash-pinned run of nf_23x (nf-skull-test.json) in T.19 SKULL TEST: the ROM pulses the skull mouth coil (16) and the skull flashers (21) and no other coil."),
)


def source_records() -> list[dict[str, Any]]:
	def pdf(source_id: str, kind: str, name: str, locator: str, sha: str, excerpts: list[dict[str, Any]]) -> dict[str, Any]:
		record = {
			"id": source_id,
			"kind": kind,
			"uri": f"external:{MANUALS_DIRECTORY}/{name}",
			"original_filename": name,
			"sha256": sha,
			"acquired_at": ACQUIRED_AT,
			"locator": locator + f" Direct resource: https://www.ipdb.org/files/2852/{name}, downloaded through an interactive browser session.",
			"license": "NOASSERTION",
			"rights": "NOASSERTION",
			"attribution": RIGHTS_NOTE,
		}
		if excerpts:
			record["excerpts"] = excerpts
		return record

	return [
		{
			"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": "Pinned catalog driver records for the nf_* clone tree (nf_23x parent; nf_23, nf_23f, nf_22, nf_20, nf_11x, nf_10f, nf_101, nf_08x)",
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
			"locator": (
				"src/wpc/sims/wpc/prelim/nf.c (a preliminary simulator) nfGameData: GEN_WPCSECURITY, wpc_dispDMD, FLIP_SW(FLIP_L | FLIP_U) | "
				"FLIP_SOL(FLIP_L | FLIP_UR), the inverted-switch mask {0x00,0x00,0x00,0xff,0xe3,0x00,0x00,0x00,0x00,0x00,0x00,0x00} (public "
				"31-38, 41, 42 and 46-48 under wpc_sw2m), no custom solenoids, the switch names (swTicket 23) and the ROM set definitions with "
				"their sound sets and the SL-1 comment; nfSimData's manual shooter FALSE; src/wpc/wpc.c WPC_FLIPPERS returning ~swMatrix and the "
				"29-31 state mirror; src/wpc/core.c core_getSol (37-44 constant zero outside WPC-95) and core_updateSw (end-of-stroke synthesis). "
				"The runtime runs used a library built from this revision."
			),
			"license": "BSD-3-Clause", "attribution": "PinMAME contributors",
		},
		{
			"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-security.json", "revision": "repository",
			"locator": "WPC-Security public switch, DIP, solenoid, lamp and five-GI address rules with the Fliptronic normalization notes",
			"license": "MIT", "attribution": "PinMAME game definitions contributors",
		},
		{
			"id": IDENTITY_SOURCE, "kind": "human_review", "uri": IPDB_URL, "revision": "retained page, 2026-11-13",
			"sha256": IPDB_PAGE_SHA256, "acquired_at": IPDB_PAGE_ACQUIRED_AT,
			"locator": (
				"IPDB machine 2852 'No Fear: Dangerous Sports' (Williams Electronics Games, May 1995, model 50025, Williams WPC Security, 4,540 "
				"units, three flippers, two ramps, automatic plunger, kickback, no pop bumpers; toys: magnetic ball accelerator and talking "
				"skull), read through an interactive browser session and retained as ipdb2852.html. Its model number matches the manual "
				"(16-50025-101) and the ROM's own identification (50025)."
			),
			"license": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
			"excerpts": [_excerpt("ipdb-page", "IPDB machine 2852 page, title line to file list", credit="curator, from the retained HTML")],
		},
		pdf(
			MANUAL_SOURCE, "manual", MANUAL_NAME,
			"Williams No Fear: Dangerous Sports operations manual 16-50025-101 (April 1995): a 144-page scan without a text layer (Windows OCR "
			"used only to find pages). PDF 107-112 carry the lamp, switch and solenoid tables, the location lists and drawings (2-34 to "
			"2-39), PDF 114-143 Section 3 wiring.",
			MANUAL_SHA256, _manual_excerpts(),
		),
		{
			"id": VPX_TABLE_SOURCE, "kind": "vpx_table",
			"uri": f"external:{VPX_SOURCE_DIRECTORY}/source/{TABLE_NAME.replace(' ', '%20')}",
			"original_filename": TABLE_NAME, "sha256": TABLE_SHA256,
			"locator": (
				f"Retained known-working recreation of the physical machine ({TABLE_ATTRIBUTION}; table_version 1.1, saved 2026-01-25). Exact "
				f"playfield bounds are {TABLE_BOUNDS}; normalized coordinates are x/{PLAYFIELD_WIDTH:g} and y/{PLAYFIELD_HEIGHT:g}. Geometry "
				"authority only for named table objects."
			),
			"license": "NOASSERTION", "attribution": TABLE_ATTRIBUTION, "rights": "NOASSERTION",
		},
		{
			"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script",
			"uri": f"external:{VPX_SOURCE_DIRECTORY}/extracted-vpxtool/script.vbs",
			"original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True,
			"locator": (
				"Retained embedded version 1.1.1 script (4,135 lines). Runtime and mechanism-causality authority: cGameName = \"nf_23x\", "
				"HandleMechanics = 0, Controller.Switch(22) and (24) set to 1 at start-up, the SolCallback and SolModCallback tables and the "
				"subs they name, the ramp magnet subs, the trough, popper and eject kickers, the switch event subs, vpmMapLights AllLamps and "
				"GiCallBack2 UpdateGI."
			),
			"license": "NOASSERTION", "attribution": TABLE_ATTRIBUTION, "rights": "NOASSERTION",
			"excerpts": [_excerpt(
				"vpx-script-contract", "script.vbs line ranges quoted verbatim with their line numbers (controller and ROM, start-up, cabinet "
				"keys, ramp magnets, SolCallback table and drop target coils, flasher callbacks, G.I., flipper callbacks, auto plunger, "
				"kickback, skull mouth and knocker, switch events, kickers and trough, drop and standup target helpers)",
				credit="curator; quoted verbatim from the retained script by a line-range generator retained under review-artifacts",
			)],
		},
		{
			"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table",
			"uri": f"external:{VPX_SOURCE_DIRECTORY}/extracted-vpxtool.manifest.json",
			"locator": (
				"Canonical manifest covering every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; manifest "
				f"SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with vpxtool "
				f"0.33.3 from the retained version 1.1.1 table. Bounds are {TABLE_BOUNDS}."
			),
			"license": "NOASSERTION", "attribution": "vpxtool extraction",
		},
	] + [
		{
			"id": source_id, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/no-fear-nf_23x-{name}.json",
			"revision": PINMAME_REVISION, "locator": locator, "license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		}
		for source_id, name, locator in RUNTIME_SOURCES
	] + [
		{
			"id": FLASHER_HISTORY_SOURCE, "kind": "runtime_scenario", "uri": f"internal:{EVIDENCE_DIRECTORY}/no-fear-nf_23x-flasher-test.json",
			"revision": FLASHER_HISTORY_REVISION, "sha256": FLASHER_HISTORY_SHA256,
			"locator": (
				"One hash-pinned LibPinMAME harness run of nf_23x from empty NVRAM (scenario tools/harness-scenarios/wpc-security/"
				"nf-flasher-test.json) that steps T.5 FLASHER TEST through flashers 17-28 in repeat mode. At step 19 the ROM pulses public "
				"solenoid 19 and prints FLS. NO FEAR with the wires BLK-ORN RED-WHT."
			),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external",
		},
	]


# --- Build ---------------------------------------------------------------------------------------------
MISSING = ["variant_differences", "spatial_placement"]


def build() -> dict[str, Any]:
	definition: dict[str, Any] = {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {
			"id": MACHINE_ID,
			"name": "No Fear: Dangerous Sports",
			"manufacturer": "Williams",
			"year": 1995,
			"kind": "physical_pinball",
			"model_number": "50025",
			"ipdb_id": 2852,
			"opdb_id": "Gr2Y2-MDxZq",
			"playfield": {"width": PLAYFIELD_WIDTH, "height": PLAYFIELD_HEIGHT, "units": "vpx"},
		},
		"coverage": {
			"status": "partial",
			"missing": MISSING,
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
		"controller": {"platform": "pinmame.wpc-security", "hardware_generation": "0x20", "inversion_applied_by_emulator": True},
		"drivers": drivers(),
		"inputs": input_devices(),
		"outputs": solenoid_outputs() + lamp_outputs() + gi_outputs(),
		"displays": displays(),
		"mechanisms": mechanisms(),
		"relationships": relationships(),
		"sources": source_records(),
		"knowledge": {"path": "knowledge/williams/no-fear-dangerous-sports-1995.md", "status": "complete"},
		"conflicts": conflicts(),
	}
	identifiers = [device["id"] for device in definition["inputs"] + definition["outputs"]]
	duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
	if duplicates:
		raise RuntimeError(f"No Fear device identifiers are not unique: {duplicates}")
	known = set(identifiers)
	for mechanism in definition["mechanisms"]:
		unknown = [item for item in mechanism["actuators"] + mechanism["sensors"] + [s for p in mechanism.get("positions", []) for s in p["sensors"]] if item not in known]
		if unknown:
			raise RuntimeError(f"No Fear mechanism {mechanism['id']} names unknown devices: {unknown}")
	return definition


# --- Spatial report ------------------------------------------------------------------------------------
def build_spatial_report(definition: dict[str, Any]) -> dict[str, Any]:
	devices = definition["inputs"] + definition["outputs"] + definition["displays"]
	statuses: dict[str, list[str]] = {"validated": [], "observed": [], "candidate": []}
	without: list[str] = []
	not_applicable_count = 0
	for device in devices:
		spatial = device.get("spatial")
		if spatial is None:
			if device.get("availability", "used") in {"used", "optional"}:
				without.append(device["id"])
			continue
		if spatial["status"] == "not_applicable":
			not_applicable_count += 1
			continue
		statuses[spatial["status"]].append(device["id"])
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
		},
		"extraction": {
			"fail_closed": True,
			"file_count": EXTRACTION_FILE_COUNT,
			"total_bytes": EXTRACTION_TOTAL_BYTES,
			"manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"manifest_uri": f"external:{VPX_SOURCE_DIRECTORY}/extracted-vpxtool.manifest.json",
			"source_ref": VPX_EXTRACTION_SOURCE,
		},
		"placement_status": {name: sorted(items) for name, items in statuses.items()},
		"not_applicable_device_count": not_applicable_count,
		"without_placements": sorted(without),
		"projection_classes": {
			"switch": (
				"The retained table's object for the switch (trigger, spinner, target, kicker or slingshot wall), chosen by what the script "
				"binds. One projection: the trough-stack (jam) opto 31, which the table does not model, sits on the trough kicker sw32 at the "
				"eject end, where the manual's trough boards put the jam position."
			),
			"lamp": (
				"The light the script maps through vpmMapLights AllLamps (TimerInterval = lamp number), at its own centre. An insert lamp's "
				"light sits on its insert, over the socket; the raised sign lights 38, 83 and 84 and the skull's eye lights 82 and 85 are "
				"invisible light-map sources with no bulb, so those placements are only candidates. 37 and 48 are two-bulb circuits with one "
				"table light each. 58 is not fitted and the cabinet button lamps 86-88 are not applicable."
			),
			"solenoid": (
				"The object the solenoid callback moves or lights: the popper, eject and trough kickers, the impulse-plunger triggers of the "
				"auto plunger and kickback, the magnet triggers, the drop target wall, the slingshot walls, the skull jaw primitive at its "
				"stored position, the flippers, and the flasher lights. The flasher lights are invisible light-map sources with no bulb, so "
				"their placements are only candidates, and the skull flasher 21's one light stands for its two playfield bulbs. The flasher "
				"circuits 20, 21 and 23 carry insert-panel bulbs as well; only their playfield bulbs are placed. The backbox flashers 22, 26 "
				"and 27 and the knocker are not applicable."
			),
			"gi": (
				"The lights of the table's GI_Top, GI_Right and GI_Left collections, which UpdateGI switches from public GI 0, 1 and 2 and whose "
				"split agrees with the ROM's PLAYFIELD TOP, RIGHT and LEFT names; they are invisible light-map sources with no bulb, so the "
				"placements are only candidates, and their number is not a bulb count. The insert-panel strings 3 and 4 are not applicable."
			),
		},
		"unresolved_geometry": [
			"No factory location drawing has been checked against the table: none of the placements is validated. The flasher, G.I. "
			"and raised lamp placements are candidates and every other placement is observed. The manual's lamp (2-35), switch (2-37) "
			"and solenoid/flashlamp (2-39) drawings carry numbered callouts that a drawing callout check could compare with these "
			"placements.",
			"The trough-stack opto 31 is projected onto the trough kicker sw32; the table models no jam position.",
			"The playfield G.I. strings 0-2 carry only candidate placements: the table's light-map sources model no bulb, and no drawing "
			"or other source locates or counts the playfield bulbs on each string.",
			"The flasher lights and the raised lamps 38, 82, 83, 84 and 85 carry only candidate placements: the table's lights are "
			"light-map sources with no bulb, set where the table throws the light, so they do not locate the sockets.",
			"Lamps 37 and 48 and the skull flasher 21's playfield pair light two bulbs each and the table models one light for each, so "
			"one bulb of each has no placement.",
			"Flasher 19's bulb count: the Solenoid/Flashlamp Table, its two copies and the flashlamp wiring drawing print one #906, the "
			"locations list prints two; the record follows the table and places the table's single light.",
		],
		"promotion_decision": (
			"partial: every fitted playfield device has an observed placement or a controlled not-applicable record except the flashers, "
			"the raised lamps 38, 82, 83, 84 and 85 and the three playfield G.I. strings, which carry only candidate light-map positions; "
			"no placement has been validated against the manual's location drawings, the jam opto is projected, and lamps 37 and 48 and "
			"the skull flasher 21 lack a placement for their second playfield bulb."
		),
	}


def render_spatial_report(report: dict[str, Any]) -> str:
	lines = [
		"# No Fear: Dangerous Sports (Williams, 1995) spatial blockers",
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
	without = report["without_placements"]
	lines += [
		f"- controlled `not_applicable` records: {report['not_applicable_device_count']}",
		f"- used devices with no placement record: {len(without)}" + (f" ({', '.join(f'`{item}`' for item in without)})" if without else ""),
		"",
		"## Projection classes",
		"",
	]
	lines += [f"- **{name}:** {text}" for name, text in report["projection_classes"].items()]
	lines += ["", "## Unresolved physical geometry", ""]
	lines += [f"- {item}" for item in report["unresolved_geometry"]]
	lines += ["", "## Promotion decision", "", report["promotion_decision"], ""]
	return "\n".join(lines)


# --- Generation ----------------------------------------------------------------------------------------
def generate(root: Path = ROOT) -> Path:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to overwrite an author-ready No Fear artifact: {AUTHOR_READY_PATH}")
	definition = build()
	write_json(PARTIAL_PATH, definition)
	report = build_spatial_report(definition)
	write_json(SPATIAL_REPORT_PATH, report)
	write_text(SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(report))
	KNOWLEDGE_PATH.write_bytes(KNOWLEDGE_SEED_PATH.read_bytes())
	return PARTIAL_PATH


def check(root: Path = ROOT) -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Stale No Fear author-ready artifact: {AUTHOR_READY_PATH}")
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
			raise RuntimeError(f"No Fear deterministic artifact drift: {path}")
	print("No Fear definition, knowledge note and spatial report match the deterministic curator.")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and its generated artifacts")
	mode.add_argument("--regenerate", action="store_true", help="Write the definition, knowledge note and spatial report")
	args = parser.parse_args()
	if args.check:
		check(ROOT)
	else:
		print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
	main()
