"""Curate the physical Williams Terminator 2 machine definition.

The semantic builder is intentionally side-effect free.  The spatial curator
owns the canonical output so a later semantic regeneration cannot erase the
reviewed table geometry.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PINMAME_REVISION = "4ec52ff0ac133ac251681518aed2249e19fe26eb"
CORE_SOURCE = f"pinmame.core.{PINMAME_REVISION[:12]}"
CATALOG_SOURCE = f"pinmame.catalog.{PINMAME_REVISION[:12]}"
CONTROLLER_SOURCE = "controller-profile.pinmame-wpc-alpha"
MANUAL_SOURCE = "manual.williams.terminator-2-judgment-day.1991"
MANUAL_SUPPORT_SOURCE = "manual-support.williams.terminator-2-judgment-day.1991"
VPX_TABLE_SOURCE = "vpx-table.t2-vpw-0022"
VPX_SCRIPT_SOURCE = "vpx-script.t2-vpw-0022"
VPX_EXTRACTION_SOURCE = "vpx-extraction.t2-vpw-0022"
G5K_SCRIPT_SOURCE = "vpx-script.t2-g5k-v1-1a"
MODERN_SCRIPT_SOURCE = "vpx-script.t2-modern-comparison"
ROM_SOURCE = "rom.t2-l8-authorized-corpus"

TABLE_SHA256 = "3727bf57102fceb13b9f8e6370bd7bc4fbd2571d95affb7bff34eb7c5f2e9f8c"
SCRIPT_SHA256 = "b5153ac46f6d4b58afb676c1f7bfdff17c6ffb953941daed8dd841c679f4e831"
EXTRACTION_MANIFEST_SHA256 = "f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9"
MANUAL_SHA256 = "8540d654b39c58ad3b19ece0f42eb1dfdb8460d249e9480f8906385c8ecdb16b"
ROM_SHA256 = "4cdd95d435334c3bd6fe19556b410b558e67266b30e7fb767f52f4d14ed525b1"

EXTRACTION_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/extracted-vpxtool")
EXTRACTION_MANIFEST_RELATIVE_PATH = Path("williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json")
EXTRACTION_FILE_COUNT = 548
EXTRACTION_TOTAL_BYTES = 132477924

DRIVER_IDS = (
	"t2_d2", "t2_d3", "t2_d4", "t2_d6", "t2_d8", "t2_l2", "t2_l2sp1",
	"t2_l3", "t2_l4", "t2_l6", "t2_l8", "t2_l81", "t2_l82", "t2_l83",
	"t2_l84", "t2_p2f", "t2_p2g", "t2_f19", "t2_f20", "t2_f32",
)

MATRIX_LABELS = {
	11: "Right Flipper", 12: "Left Flipper", 13: "Start Button", 14: "Plumb Bob Tilt",
	15: "Trough Left", 16: "Trough Center", 17: "Trough Right", 18: "Outhole",
	21: "Slam Tilt", 22: "Coin Door Closed", 23: "Ticket Dispenser", 24: "Test Position Always Closed",
	25: "Left Outlane", 26: "Left Return Lane", 27: "Right Return Lane", 28: "Right Outlane",
	31: "Gun Loaded", 32: "Gun Mark", 33: "Gun Home", 34: "Grip Trigger",
	36: "Mid Left Standup Target", 37: "Mid Center Standup Target", 38: "Mid Right Standup Target",
	41: "Left Jet", 42: "Right Jet", 43: "Bottom Jet", 44: "Left Sling", 45: "Right Sling",
	46: "Top Right Standup Target", 47: "Mid Right Standup Target", 48: "Bottom Right Standup Target",
	51: "Left Lock", 53: "Low Escape Route", 54: "High Escape Route", 55: "Top Lock",
	56: "Top Lane Left", 57: "Top Lane Center", 58: "Top Lane Right",
	61: "Left Ramp Entry", 62: "Left Ramp Made", 63: "Right Ramp Entry", 64: "Right Ramp Made",
	65: "Low Chase Loop", 66: "High Chase Loop", 71: "Target 1 High", 72: "Target 2",
	73: "Target 3", 74: "Target 4", 75: "Target 5 Low", 76: "Ball Popper",
	77: "Drop Target", 78: "Shooter",
}
MATRIX_PULSES = {11, 12, 13, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 61, 63, 71, 72, 73, 74, 75}

LAMP_LABELS = {
	11: "Multiplier 2x", 12: "Multiplier 4x", 13: "Hold Bonus", 14: "Multiplier 6x", 15: "Multiplier 8x", 16: "Shoot Again", 17: "Mouth", 18: "Not Used",
	21: "Kickback", 22: "Special", 23: "Left Return Lane", 24: "Right Return Lane", 25: "Data Base 3", 26: "Load Gun", 27: "Extra Ball", 28: "Load for Jackpot",
	31: "Target 1 High", 32: "Target 2", 33: "Target 3", 34: "Target 4", 35: "Target 5 Low", 36: "Middle Target Bank Left", 37: "Middle Target Bank Center", 38: "Middle Target Bank Right",
	41: "Lock Two", 42: "Data Base 2", 43: "10 Million", 44: "Extra Ball", 45: "Multi-ball", 46: "Light Hurry Up", 47: "Hold Bonus", 48: "Security Pass",
	51: "Eyes Lower", 52: "Eyes Upper", 53: "5 Million", 54: "3 Million", 55: "1 Million", 56: "750 Thousand", 57: "500 Thousand", 58: "250 Thousand",
	61: "Left CPU Lit", 62: "Left Vault Key", 63: "Left Silent Alarm", 64: "Left Passcode", 65: "Left Checkpoint", 66: "Lock 1", 67: "Data Base 1", 68: "Left Ramp",
	71: "Right CPU Lit", 72: "Right Vault Key", 73: "Right Silent Alarm", 74: "Right Passcode", 75: "Right Checkpoint", 76: "Right Bank Top", 77: "Right Bank Middle", 78: "Right Bank Bottom",
	81: "Chase Values", 82: "Right Ramp", 83: "Hurry Up", 84: "Start Button", 85: "Drop Target", 86: "Top Lane Left", 87: "Top Lane Center", 88: "Top Lane Right",
}

SOLENOID_LABELS = {
	1: "Ball Popper", 2: "Gun Kicker", 3: "Outhole", 4: "Trough", 5: "Right Sling", 6: "Left Sling", 7: "Knocker", 8: "Kickback", 9: "Plunger", 10: "Top Lock", 11: "Gun Motor", 12: "Knock Down", 13: "Left Jet", 14: "Right Jet", 15: "Bottom Jet", 16: "Left Lock",
	17: "Hot Dog Flashlamps", 18: "Right Sling Flashlamps", 19: "Left Sling Flashlamps", 20: "Left Lock Flashlamps", 21: "Gun Flashlamps", 22: "Right Ramp Flashlamps", 23: "Left Ramp Flashlamps", 24: "Backglass Flashlamp", 25: "Targets Flashlamps", 26: "Left Popper Flashlamps", 27: "Right Popper Flashlamps", 28: "Drop Target",
}

SOLENOID_SCRIPT_CALLBACKS = {
	1: "SolSkull (retained script callback; opens the skull/ball-popper path from switch 76)", 2: "SolFireGun", 3: "bsTrough.SolIn (outhole)", 4: "bsTrough.SolOut (ball release)", 7: "Knocker sound callback", 8: "SolAPlunger (left outer-lane kicker saver)", 9: "SolShooter (auto plunger)", 10: "SolTopPopper", 11: "MECHGUN motor", 16: "SolLeftPopper", 28: "dtDrop1.SolDropUp",
}

SOLENOID_WIRING = {
	1: ("Vio-Brn", "J130-1", "Q82", "AE-23-800"), 2: ("Vio-Red", "J130-2", "Q80", "AE-24-900"), 3: ("Vio-Orn", "J130-4", "Q78", "AE-27-1200"), 4: ("Vio-Yel", "J130-5", "Q76", "AE-26-1200"),
	5: ("Vio-Grn", "J130-6", "Q64", "AE-26-1500"), 6: ("Vio-Blu", "J130-7", "Q66", "AE-26-1500"), 7: ("Vio-Blk", "J130-8", "Q68", "AE-23-800"), 8: ("Vio-Gry", "J130-9", "Q70", "AE-23-800"),
	9: ("Brn-Blk", "J127-1", "Q58", "AE-23-800"), 10: ("Brn-Red", "J127-3", "Q56", "AE-26-1500"), 11: ("Brn-Orn", "J127-4", "Q54", "14-7963"), 12: ("Brn-Yel", "J127-5", "Q52", "SM1-26-600"),
	13: ("Brn-Grn", "J127-6", "Q50", "AE-26-1200"), 14: ("Brn-Blu", "J127-7", "Q48", "AE-26-1200"), 15: ("Brn-Vio", "J127-8", "Q46", "AE-26-1200"), 16: ("Brn-Gry", "J127-9", "Q44", "AE-26-1500"),
	17: ("Blk-Brn", "J126-1", "Q42", "#906 (4 PL)"), 18: ("Blk-Red", "J126-2", "Q40", "#906 (1 BB), #89 (1 PL)"), 19: ("Blk-Orn", "J126-3", "Q38", "#906 (1 BB), #89 (1 PL)"), 20: ("Blk-Yel", "J126-4 + J125-2", "Q36", "#906 (1 BB), #89 (1 PL)"),
	21: ("Blu-Grn", "J126-5 + J125-3", "Q28", "#89 (2 PL)"), 22: ("Blu-Blk", "J126-6 + J125-5", "Q30", "#906 (1 BB), #89 (1 PL)"), 23: ("Blu-Vio", "J126-7", "Q34", "#906 (1 BB), #89 (1 PL)"), 24: ("Blu-Gry", "J125-7", "Q32", "#906 (1 BB)"),
	25: ("Blu-Brn", "J122-1 + J125-8", "Q26", "#89 (2 PL)"), 26: ("Blu-Red", "J122-2 + J125-9", "Q24", "#89 (2 PL)"), 27: ("Blu-Orn", "J122-3", "Q22", "#89 (2 PL)"), 28: ("Blu-Yel", "J122-4", "Q20", "AE-26-1200"),
}

GI_WIRING = {
	0: ("Wht-Brn", "J120-7", "Q18", "#555"), 1: ("Wht-Vio", "J119-1", "Q10", "#555"), 2: ("Wht-Yel", "J121-9", "Q14", "#555"), 3: ("Wht-Orn", "J120-8", "Q16", ""), 4: ("Wht-Grn", "J120-10", "Q12", "#555"),
}


def _file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		while chunk := stream.read(1024 * 1024):
			digest.update(chunk)
	return digest.hexdigest()


def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
	if not extraction_root.is_dir():
		raise RuntimeError(f"T2 retained extraction is missing: {extraction_root}")
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
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained T2 extraction")
		return None
	return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	if not manifest_path.is_file():
		raise RuntimeError(f"T2 retained extraction manifest is missing: {manifest_path}")
	actual = load_json(manifest_path)
	expected = build_extraction_manifest(extraction_root)
	if canonical_bytes(actual) != canonical_bytes(expected):
		raise RuntimeError(f"T2 retained extraction manifest does not match all files under {extraction_root}")
	files = actual["files"]
	file_count = len(files)
	total_bytes = sum(int(item["size"]) for item in files)
	manifest_sha256 = hashlib.sha256(canonical_bytes(actual)).hexdigest()
	if (file_count, total_bytes, manifest_sha256) != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
		raise RuntimeError(
			"T2 retained extraction identity mismatch: "
			f"files={file_count}, bytes={total_bytes}, manifest_sha256={manifest_sha256}"
		)
	return actual


def write_extraction_manifest(source_root: Path) -> Path:
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
	write_json(manifest_path, build_extraction_manifest(extraction_root))
	verify_extraction_manifest(source_root)
	return manifest_path


def slug(value: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-") or "unnamed"


def provenance(*refs: str, status: str = "validated") -> dict[str, Any]:
	return {"status": status, "source_refs": list(refs)}


def aliases(namespace: str, address: int, *extra: str) -> list[dict[str, str]]:
	return [{"namespace": namespace, "value": str(address)}, *({"namespace": "manual.address", "value": value} for value in extra)]


def output_id(label: str) -> str:
	return f"device.{slug(label)}"


def source_records() -> list[dict[str, Any]]:
	return [
		{"id": CATALOG_SOURCE, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "locator": "Pinned catalog driver records for the t2_* family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CORE_SOURCE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION, "sha256": "e894868e68958d1343abfd89dcd229ff7c7d629effb364026b57d8aedb6924e7", "locator": "src/libpinmame/libpinmame.h PINMAME_HARDWARE_GEN_WPCDMD=0x4; src/wpc/sims/wpc/full/t2.c GEN_WPCDMD, wpc_dispDMD, t2 driver family", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": CONTROLLER_SOURCE, "kind": "human_review", "uri": "internal:controllers/pinmame/wpc-alpha.json", "revision": "repository", "locator": "WPC public switch, lamp, solenoid, and five-GI address rules; emulator lamp remapping", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
		{"id": MANUAL_SOURCE, "kind": "manual", "uri": "external:pinmame-manuals/by-machine/williams.terminator-2-judgment-day.1991/arcarc/Terminator%202%20Judgement%20Day%20Operations%20Manual.pdf", "sha256": MANUAL_SHA256, "locator": "Manifest ID other.arcarc.williams.terminator-2-judgment-day.1991.8540d654b39c; 118-page image-only Williams operations manual: switch tables pp.45-46,102-103,117; coil tables pp.2,47-50,104-105,112,114; lamp tables pp.51-53,79,100-101,117; mechanism map p.70; assemblies pp.68-96; cannon pp.10,24,54,70,86,90-92,110-114; rules pp.6-20", "license": "NOASSERTION", "attribution": "Williams Electronics"},
		{"id": MANUAL_SUPPORT_SOURCE, "kind": "human_review", "uri": "external:pinmame-manuals/by-machine/williams.terminator-2-judgment-day.1991/arcarc/extracted", "locator": "Retained page index, mechanism notes, rendered pages, contact sheets, and reference PNGs used for visual verification", "license": "NOASSERTION", "attribution": "Williams manual extraction"},
		{"id": VPX_TABLE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/source/Terminator%202%20VPW_0022.vpx", "original_filename": "Terminator 2 VPW_0022.vpx", "sha256": TABLE_SHA256, "locator": "Retained known-working VPW 0022 physical table; geometry source only for named VPX objects and embedded-script container", "license": "NOASSERTION", "attribution": "VPW table authors"},
		{"id": VPX_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool/script.vbs", "original_filename": "script.vbs", "sha256": SCRIPT_SHA256, "known_working": True, "locator": "Retained embedded VPW script; evidence authority is semantic_controller and mechanism_causality: cGameName=t2_l8, callbacks, switch semantics, ball stacks, gun mechanism, drop target, flashers, and GI callback behavior", "license": "NOASSERTION", "attribution": "VPW table authors"},
		{"id": VPX_EXTRACTION_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/extracted-vpxtool.manifest.json", "locator": "Canonical manifest covers every sorted relative POSIX path, byte size, and SHA-256 under extracted-vpxtool; manifest SHA-256 f56ab9a0b6287c71b984c42d97c88cbf98345a0614a8a920e93374e06ba2fab9; 548 files, 132477924 bytes, bounds left=0 top=0 right=964 bottom=2162; normalized coordinates are x/964 and y/2162", "license": "NOASSERTION", "attribution": "vpxtool extraction"},
		{"id": G5K_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/scripts/Terminator%202%20(Williams%201991)%20g5k%20v1.1a.vbs", "sha256": "f6c3d5ec0aa95bb6c3ac3160b35adff9a6b1c6d282e64e15a3709f426f08949a", "known_working": False, "locator": "Corroborating g5k script inventory; consulted where it agrees with the retained VPW script, never promoted over it", "license": "NOASSERTION", "attribution": "g5k table authors"},
		{"id": MODERN_SCRIPT_SOURCE, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/williams/terminator-2-judgment-day-1991/scripts/Terminator%202%20(Williams%201991).vbs", "sha256": "1bbcc5873a1db87fe59d1daefbb69b68872cf58f029320a9d7d9410db7c59d97", "known_working": False, "locator": "Comparison-only modern script; its four-position trough, pulsed 62/64, virtual devices, and keyframed/magnet cannon are excluded from this physical VPW definition", "license": "NOASSERTION", "attribution": "Modern community table authors"},
		{"id": ROM_SOURCE, "kind": "rom_static_analysis", "uri": "external:pinmame-roms/t2_l8.zip", "sha256": ROM_SHA256, "locator": "Pre-existing authorized local ROM evidence; bytes are not copied into this repository", "license": "NOASSERTION", "attribution": "Authorized local evidence"},
	]


def _device_base(identifier: str, label: str, kind: str, group: str, address: int, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	device: dict[str, Any] = {
		"id": identifier, "label": label, "kind": kind,
		"binding": {"group": group, "device": address},
		"availability": availability, "provenance": provenance(*refs),
	}
	device.update(extra)
	return device


def input_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address, label, role in (
		(1, "Coin Chute 1", "cabinet.coin.1"), (2, "Coin Chute 2", "cabinet.coin.2"), (3, "Coin Chute 3", "cabinet.coin.3"), (4, "Coin Chute 4", "cabinet.coin.4"),
		(5, "Coin-Door Cancel", "service.cancel"), (6, "Coin-Door Down", "service.down"), (7, "Coin-Door Up", "service.up"), (8, "Coin-Door Enter", "service.enter"),
	):
		items.append(_device_base(f"switch.cabinet-{address}", label, "switch", "pinmame.input.switch", address, "optional" if address == 4 else "used", (CONTROLLER_SOURCE, MANUAL_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=False, roles=[role], physical={"location": "coin door / cabinet"}))
	for row in range(1, 9):
		for column in range(1, 9):
			address = row * 10 + column
			label = MATRIX_LABELS.get(address, f"Unused matrix position {address}")
			unused = address not in MATRIX_LABELS
			kind = "constant" if address == 24 else "switch"
			extra: dict[str, Any] = {"aliases": aliases("pinmame.switch", address, f"{row}-{column}")}
			if kind == "constant":
				extra["constant_active"] = True
				extra["initial_active"] = True
			elif not unused:
				extra["normally_closed"] = address in {21, 22}
				extra["pulse"] = address in MATRIX_PULSES
			if address in {11, 12}:
				extra["roles"] = ["flipper.lower.right.switch" if address == 11 else "flipper.lower.left.switch"]
			elif address == 13:
				extra["roles"] = ["cabinet.start"]
			elif address == 14:
				extra["roles"] = ["cabinet.tilt"]
			elif address == 22:
				extra["roles"] = ["cabinet.coin-door"]
				extra["initial_active"] = True
			elif address == 23:
				extra["roles"] = ["service.ticket"]
			extra["physical"] = {"switch_type": "microswitch" if not unused else "unknown", "notes": f"Printed WPC matrix row {row}, column {column}; {'retained VPW switch semantic' if not unused else 'printed Not Used position'}."}
			items.append(_device_base(f"switch.matrix-{address}", label, kind, "pinmame.input.switch", address, "unused" if unused else "used", (MANUAL_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if not unused else (MANUAL_SOURCE, CORE_SOURCE), **extra))
	for address, label, role in (
		(111, "Lower Right Flipper Button", "flipper.lower.right.button"), (112, "Lower Right Flipper EOS", "internal.flipper.lower.right.eos"),
		(113, "Lower Left Flipper Button", "flipper.lower.left.button"), (114, "Lower Left Flipper EOS", "internal.flipper.lower.left.eos"),
		(115, "Unused Generic Flipper Input 115", "internal.unused.flipper"), (116, "Unused Generic Flipper Input 116", "internal.unused.flipper"),
		(117, "Unused Generic Flipper Input 117", "internal.unused.flipper"), (118, "Unused Generic Flipper Input 118", "internal.unused.flipper"),
	):
		unused = address >= 115
		items.append(_device_base(f"switch.generic-{address}", label, "switch", "pinmame.input.switch", address, "unused" if unused else "optional", (CONTROLLER_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.switch", address), normally_closed=address in {112, 114}, roles=[role], physical={"location": "lower flipper cabinet/playfield interface", "switch_type": "leaf" if not unused else "unknown"}))
	for address in range(1, 9):
		items.append(_device_base(f"switch.dip-{address}", f"CPU/Sound Board DIP {address}", "dip_switch", "pinmame.input.dip", address, "used", (CONTROLLER_SOURCE, MANUAL_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.dip", address), physical={"location": "CPU/Sound board"}))
	return items


def _solenoid_output(address: int, label: str, kind: str, availability: str, refs: tuple[str, ...], **extra: Any) -> dict[str, Any]:
	return _device_base(output_id(label), label, kind, "pinmame.output.solenoid", address, availability, refs, aliases=aliases("pinmame.solenoid", address), **extra)


def output_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in range(1, 29):
		kind = "flasher" if 17 <= address <= 27 else "coil"
		availability = "optional" if address in {12, 24} else "used"
		physical: dict[str, Any] = {"notes": f"Manual physical device: {SOLENOID_LABELS[address]}; printed coil/driver references are on manual pages 48-50, 104-105, 112, and 114."}
		wire_color, connection, transistor, part_number = SOLENOID_WIRING[address]
		physical["part_number"] = part_number
		if address in SOLENOID_SCRIPT_CALLBACKS:
			physical["notes"] += f" Retained script callback: {SOLENOID_SCRIPT_CALLBACKS[address]}."
		if address == 12:
			physical["notes"] += " Conflict: the early manual solenoid/location list calls this Knock Down (SM1-26-600), but the later electrical table marks solenoid 12 Not Used. The retained VPW script has no SolCallback(12). Availability is optional until the printed conflict is resolved."
		if address == 24:
			physical["notes"] += " Conflict: the manual identifies a backglass flashlamp, while the retained VPW script has no SolCallback(24); the physical output is retained without inventing script behavior."
		sources = (MANUAL_SOURCE, CORE_SOURCE) if address == 12 else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_solenoid_output(address, SOLENOID_LABELS[address], kind, availability, sources, physical=physical, wiring={"board": "WPC driver board", "control_wire": wire_color, "control_connection": connection, "driver_transistor": transistor}))
	for address, label, availability in ((34, "Unused Generic Flipper Output 34", "unused"), (36, "Unused Generic Flipper Output 36", "unused"), (46, "Lower Right Flipper", "used"), (48, "Lower Left Flipper", "used")):
		roles = ["flipper.lower.right"] if address == 46 else ["flipper.lower.left"] if address == 48 else ["internal.unused.generic-flipper"]
		wire_color, connection, part_number = ("Blu-Yel", "J109-7", "FL-11630") if address == 46 else ("Gry-Yel", "J109-5", "FL-11630") if address == 48 else ("", "", "")
		extra = {"notes": f"Lower flipper controller output; callback is {'sLRFlipper' if address == 46 else 'sLLFlipper' if address == 48 else 'not used'}."}
		if part_number:
			extra["part_number"] = part_number
		wiring = {"board": "WPC driver board", "control_wire": wire_color, "control_connection": connection} if connection else None
		items.append(_solenoid_output(address, label, "coil", availability, (CONTROLLER_SOURCE, CORE_SOURCE, VPX_SCRIPT_SOURCE) if availability == "used" else (CONTROLLER_SOURCE, CORE_SOURCE), roles=roles, physical=extra, **({"wiring": wiring} if wiring else {})))
	for address in range(29, 51):
		if address in {34, 36, 46, 48}:
			continue
		state_channel = address in {29, 30, 31}
		if address == 31:
			label = "Game-On Solenoid Relay"
			kind = "relay"
			notes = "On this pre-Fliptronic WPC generation, pinned wpc.c identifies public address 31 as the real Game-On solenoid controlled by WPC_GILAMPS bit 7 through the power-driver relay chain to the cabinet switch and flippers. It is a cabinet/flipper-enable relay, not a playfield device."
		elif state_channel:
			label = f"WPC State Channel {address}"
			kind = "virtual"
			notes = "PinMAME publishes meaningful WPC controller state at this address; it is not a physical playfield device."
		elif address == 32:
			label = f"Unused WPC State/Generic Output {address}"
			kind = "virtual"
			notes = "PinMAME's WPC remap has no fourth state bit; this public address is constant zero and is not a physical output."
		else:
			label = f"Unused WPC State/Generic Output {address}"
			kind = "virtual"
			notes = "PinMAME compatibility/state channel; not a physical playfield device."
		items.append(_solenoid_output(address, label, kind, "used" if state_channel else "unused", (CONTROLLER_SOURCE, CORE_SOURCE), roles=["internal.wpc-state" if state_channel else "internal.unused.wpc-output"], physical={"notes": notes}))
	return items


def lamp_devices() -> list[dict[str, Any]]:
	items: list[dict[str, Any]] = []
	for address in sorted(LAMP_LABELS):
		unused = address == 18
		availability = "unused" if unused else "optional" if address == 84 else "used"
		extra: dict[str, Any] = {"aliases": aliases("pinmame.lamp", address, f"{address:03d}"), "physical": {"notes": f"Printed lamp matrix address {address // 10}-{address % 10}; manual lamp address {address}."}}
		if address == 84:
			extra["roles"] = ["cabinet.start"]
		if address == 18:
			extra["physical"]["notes"] += " Printed lamp matrix says Not Used; no L18 object exists in the retained VPX table."
		refs = (MANUAL_SOURCE, CORE_SOURCE) if unused else (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE)
		items.append(_device_base(f"lamp.matrix-{address}", LAMP_LABELS[address], "lamp", "pinmame.output.lamp", address, availability, refs, **extra))
	return items


def gi_devices() -> list[dict[str, Any]]:
	labels = {0: "GI 1: Top Insert", 1: "GI 2: Left Playfield", 2: "GI 3: Right Playfield", 3: "GI 4: Not Used", 4: "GI 5: Bottom Insert"}
	items: list[dict[str, Any]] = []
	for address in range(5):
		unused = address == 3
		physical: dict[str, Any] = {"notes": f"Manual GI string: {labels[address]}; printed GI table on manual pages 48-50."}
		if address == 3:
			physical["notes"] += " Later manual GI table marks GI 4 Not Used; the retained script has a Case 3 visual Light2-Light5 branch, so those facts are not merged into a physical string mapping."
		else:
			physical["notes"] += " Manual five-string naming is retained; the VPW script exposes only GI2/GI3 emitter arrays and a separate Light2-Light5 branch. See the conflict record and spatial audit."
		wire_color, connection, transistor, part_number = GI_WIRING[address]
		if part_number:
			physical["part_number"] = part_number
		items.append(_device_base(f"gi.string-{address + 1}", labels[address], "gi", "pinmame.output.gi", address, "unused" if unused else "used", (MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CORE_SOURCE), aliases=aliases("pinmame.gi", address), physical=physical, wiring={"board": "WPC driver board", "control_wire": wire_color, "control_connection": connection, "driver_transistor": transistor}))
	return items


def displays() -> list[dict[str, Any]]:
	return [{"id": "display.dmd", "label": "128x32 dot-matrix display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance(CORE_SOURCE, MANUAL_SOURCE)}, "provenance": provenance(CORE_SOURCE, VPX_SCRIPT_SOURCE)}]


def mechanisms() -> list[dict[str, Any]]:
	def mechanism(identifier: str, label: str, kind: str, actuators: list[str], sensors: list[str], behavior: str, positions: list[tuple[str, str, list[str], str]], *refs: str) -> dict[str, Any]:
		return {"id": identifier, "label": label, "kind": kind, "actuators": actuators, "sensors": sensors, "positions": [{"id": position_id, "label": position_label, "sensors": position_sensors, "description": description} for position_id, position_label, position_sensors, description in positions], "behavior": behavior, "provenance": provenance(*refs)}
	return [
		mechanism("mechanism.three-ball-trough", "Three-ball trough and outhole", "other", [output_id("Trough"), output_id("Outhole")], ["switch.matrix-15", "switch.matrix-16", "switch.matrix-17", "switch.matrix-18"], "Retained VPW initialization is bsTrough.InitSw 18,17,16,15 with Balls=3; BallRelease kicks at 90 degrees and strength 8. The script does not prove a four-ball trough.", [("left", "Left trough", ["switch.matrix-15"], "Manual trough left position."), ("center", "Center trough", ["switch.matrix-16"], "Manual trough center position."), ("right", "Right trough", ["switch.matrix-17"], "Manual trough right position."), ("outhole", "Outhole", ["switch.matrix-18"], "Manual outhole position.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.shooter-lane", "Shooter lane and auto plunger", "kicker", [output_id("Plunger")], ["switch.matrix-78"], "The retained saucer stack uses switch 78, a 0-degree/50-strength kick, and kick-force variance 3.", [("shooter", "Shooter lane", ["switch.matrix-78"], "Shooter switch and lane.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.left-lock", "Left lock saucer", "kicker", [output_id("Left Lock")], ["switch.matrix-51"], "The retained left lock stack uses switch 51 and kicks at 160 degrees with strength 13.", [("locked", "Left lock occupied", ["switch.matrix-51"], "Left lock saucer.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.top-lock", "Top lock saucer", "kicker", [output_id("Top Lock")], ["switch.matrix-55"], "The retained top lock stack uses switch 55, kicks at 270 degrees with strength 5, and has kick-force variance 6.", [("locked", "Top lock occupied", ["switch.matrix-55"], "Top lock saucer.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.gun-traverse", "Motorized cannon traverse", "motorized", [output_id("Gun Motor")], ["switch.matrix-31", "switch.matrix-32", "switch.matrix-33"], "cvpmMech one-solenoid/reverse/non-linear; solenoid 11, length 240, steps 240; home switch 33 window 0-5, mark switch 32 window 98-105; visual callback uses CurrentPos=aNewPos/3. The retained script moves T2_Gun and its held ball, not a keyframed or magnet cannon.", [("home", "Gun home", ["switch.matrix-33"], "Position window 0-5."), ("mark", "Gun mark", ["switch.matrix-32"], "Position window 98-105."), ("loaded", "Gun loaded", ["switch.matrix-31"], "Ball-loaded sensor at the cannon." )], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.gun-fire", "Cannon fire and gun-loaded kicker", "kicker", [output_id("Gun Kicker")], ["switch.matrix-31", "switch.matrix-34"], "Solenoid 2 fires the loaded ball from switch 31 by -CurrentPos at strength 45, clears the loaded ball, and is commanded by the grip trigger switch 34.", [("loaded", "Gun loaded", ["switch.matrix-31"], "Loaded-ball firing state.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.skull-ball-popper", "Skull ball popper", "toy", [output_id("Ball Popper")], ["switch.matrix-76", "switch.matrix-77"], "SolSkull is the retained callback: manual solenoid 1 Ball Popper opens the skull/ball path from switch 76. The callback name is retained and is not turned into a virtual skull device.", [("popper", "Ball popper", ["switch.matrix-76"], "Ball popper switch."), ("skull-down", "Skull target down", ["switch.matrix-77"], "Drop-target state." )], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.drop-target", "Single skull drop target", "drop_target_bank", [output_id("Drop Target")], ["switch.matrix-77"], "A single switch 77 target is reset by dtDrop1.SolDropUp on solenoid 28.", [("target", "Drop target", ["switch.matrix-77"], "Single-bank target.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
		mechanism("mechanism.kickback", "Left outer-lane kickback", "kicker", [output_id("Kickback")], ["switch.matrix-25"], "SolAPlunger is the left outer-lane kicker saver; it is distinct from the auto-plunger output 9.", [("left-outlane", "Left outlane", ["switch.matrix-25"], "Kickback entry switch.")], VPX_SCRIPT_SOURCE, MANUAL_SOURCE, CORE_SOURCE),
	]


def conflicts() -> list[dict[str, Any]]:
	return [
		{"id": "conflict.solenoid-12-physical-presence", "path": "outputs.pinmame.output.solenoid.12", "description": "The early manual coil/location list identifies solenoid 12 as Knock Down / SM1-26-600, while the later manual electrical table says Not Used. The retained VPW script has no SolCallback(12). The definition retains the channel as optional and does not manufacture a resolution.", "source_refs": [MANUAL_SOURCE, CORE_SOURCE]},
		{"id": "conflict.lamp-schematic-connector-labels", "path": "outputs.pinmame.output.lamp", "description": "The later lamp schematic connector labels do not match the matrix table labels one-for-one. Matrix address/name identity is preserved from the printed matrix table; connector labels are not synthesized into wiring fields.", "source_refs": [MANUAL_SOURCE, MANUAL_SUPPORT_SOURCE, CORE_SOURCE]},
		{"id": "conflict.gi-string-routing", "path": "outputs.pinmame.output.gi", "description": "The manual names five GI strings (GI 1 Top Insert, GI 2 Left Playfield, GI 3 Right Playfield, GI 4 Not Used, GI 5 Bottom Insert), while the retained VPW script exposes GI2/GI3 emitter arrays and a separate Case 3 Light2-Light5 branch; legacy mapping names also differ. Physical five-channel routing and script callback grouping remain explicit, unresolved evidence rather than an averaged map.", "source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE, CONTROLLER_SOURCE]},
		{"id": "conflict.flashing-channel-24", "path": "outputs.pinmame.output.solenoid.24", "description": "The manual lists a Backglass Flashlamp at solenoid 24, but the retained script has no SolCallback(24). Physical inventory and emulator address are retained without inventing a callback or playfield emitter.", "source_refs": [MANUAL_SOURCE, VPX_SCRIPT_SOURCE]},
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
		item["physical_compatibility"] = "compatible" if driver_id in {"t2_l83", "t2_l84", "t2_f19", "t2_f20", "t2_f32"} else "identical"
		item["variant_notes"] = {
			"t2_l83": "Community profanity/bugfix/MOD ROM; retained as a physical-compatible ROM variant with the same Williams WPC-DMD I/O and playfield.",
			"t2_l84": "Community profanity/bugfix/MOD ROM; retained as a physical-compatible ROM variant with the same Williams WPC-DMD I/O and playfield.",
			"t2_f19": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme.",
			"t2_f20": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme.",
			"t2_f32": "FreeWPC alternative firmware for the stock physical T2 machine; it is a compatible controller variant, not a separate physical machine or retheme.",
		}.get(driver_id, "Firmware, sound, attract-score, profanity, or LED ghost-fix revision; physical playfield, controller generation, and I/O are unchanged.")
		items.append(item)
	return items


def build_semantic() -> dict[str, Any]:
	return {
		"format": "pinmame-machine-definition", "schema_version": 2,
		"machine": {"id": "williams.terminator-2-judgment-day.1991", "name": "Terminator 2: Judgment Day", "manufacturer": "Williams", "year": 1991, "kind": "physical_pinball", "ipdb_id": 2524, "model_number": "T2"},
		"coverage": {"status": "partial", "missing": ["spatial_placement", "unresolved_conflicts"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated", "physical_wiring": "conflicted", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "unknown"}},
		"controller": {"platform": "pinmame.wpc-alpha", "hardware_generation": "0x4", "inversion_applied_by_emulator": True},
		"drivers": drivers(), "inputs": input_devices(), "outputs": output_devices() + lamp_devices() + gi_devices(), "displays": displays(), "mechanisms": mechanisms(),
		"relationships": [
			{"id": "relationship.trough-release", "kind": "pulse", "source": output_id("Trough"), "destination": "switch.matrix-15", "provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE)},
			{"id": "relationship.drop-target-reset", "kind": "pulse", "source": output_id("Drop Target"), "destination": "switch.matrix-77", "provenance": provenance(MANUAL_SOURCE, VPX_SCRIPT_SOURCE)},
		],
		"sources": source_records(), "knowledge": {"path": "knowledge/williams/terminator-2-judgment-day-1991.md", "status": "complete"}, "conflicts": conflicts(),
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group()
	mode.add_argument("--check", action="store_true", help="Delegate a non-destructive determinism check to the spatial curator")
	mode.add_argument("--regenerate", action="store_true", help="Delegate canonical generation to the spatial curator")
	mode.add_argument("--write-extraction-manifest", action="store_true", help="Write and verify the retained full-file VPX extraction manifest")
	args = parser.parse_args()
	from curate_terminator_2_spatial import check, generate
	if args.write_extraction_manifest:
		source_root = configured_vpx_sources_root(required=True)
		assert source_root is not None
		print(f"T2 extraction manifest written and verified: {write_extraction_manifest(source_root)}")
	elif args.check:
		check(ROOT)
	else:
		generate(ROOT)


if __name__ == "__main__":
	main()
