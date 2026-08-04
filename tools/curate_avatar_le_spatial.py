"""Curate the physical Stern Avatar Limited Edition with fail-closed spatial data.

The two retained local VPX files are Pro tables.  They are used only for geometry
which is shared with LE after the script/manual/ROM reconciliation.  LE-only
devices use the official manual, LE physical record, and exact service diagnostics;
no Pro-only object is used to manufacture LE-only geometry.  Unresolved spatial
records remain absent and keep the machine partial until exact LE physical/manual
anchors are available.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, write_bytes
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, render_spatial_overlay

from curate_avatar import (
	CORE_SOURCE,
	LE_DETECTOR_SOURCE,
	LE_DUMP_SOURCE,
	LE_IPDB_SOURCE,
	LE_KNOWLEDGE,
	LE_ROM_SOURCE,
	LE_RUNTIME_SOURCE,
	MANUAL_SOURCE,
	TRANSPORTER_DOWN_SOURCE,
	TRANSPORTER_UP_SOURCE,
	build,
	dedicated_id,
	output_id,
	switch_id,
)


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/avatar-limited-edition-2010.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/avatar-limited-edition-2010.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/avatar-limited-edition-2010.md"

LOCAL_ARCHIVE_SOURCE = "vpx-table.avatar-pro.local-archive-2020"
LOCAL_PRIMARY_SOURCE = "vpx-table.avatar-pro.local-primary-2020"
LE_PLAYFIELD_PHOTO_SOURCE = "photo.avatar-le.playfield-vendor"

LE_ONLY_SWITCHES = {41, 47, 48, 72}
SPATIAL_BLOCKED_FLASHERS = {20, 22, 23, 25, 26, 28, 29, 30, 31, 32}
FLASHER_QUANTITIES = {20: 1, 21: 2, 22: 1, 23: 1, 25: 1, 26: 1, 27: 2, 28: 2, 29: 1, 30: 1, 31: 1, 32: 1}

# These are the only retained Avatar LE placements: direct centers from named
# objects in the retained Pro VPX extraction, after reconciling the Pro object
# semantics with the common LE device inventory.  A numeric point without that
# reproducible named-object anchor is intentionally absent below.
INPUT_POSITIONS = {
	1: [(0.186581, 0.707801)], 2: [(0.085534, 0.523703)], 3: [(0.098460, 0.495226)],
	4: [(0.111825, 0.466916)], 5: [(0.122831, 0.440730)], 7: [(0.802521, 0.710875)],
	9: [(0.128414, 0.328960)], 10: [(0.102416, 0.082506)],
	11: [(0.340902, 0.060967)], 12: [(0.431239, 0.061913)], 13: [(0.518423, 0.067114)],
	14: [(0.339811, 0.266371)], 17: [(0.451031, 0.257531)], 24: [(0.047966, 0.743852)],
	25: [(0.120071, 0.702405)],
	28: [(0.799874, 0.714500)], 29: [(0.884150, 0.747728)], 30: [(0.310465, 0.142791)],
	31: [(0.575565, 0.133134)], 32: [(0.443293, 0.214691)], 35: [(0.889747, 0.069832)],
	36: [(0.731480, 0.173037)], 37: [(0.619375, 0.262815)], 38: [(0.754474, 0.273313)],
	39: [(0.771875, 0.379573)], 40: [(0.836774, 0.422809)],
	52: [(0.941477, 0.167447)],
}

# Most retained switch anchors come from the archive candidate. These nine
# object centers exist only in the primary candidate and must cite that exact
# table so every normalized point can be re-derived from its source hash.
PRIMARY_INPUT_POSITION_ADDRESSES = {2, 3, 4, 5, 17, 36, 37, 38, 39}

INPUT_SPATIAL_BLOCKERS = {
	8: "The Pro right-bank target has no retained named-object center after semantic reconciliation; its previous point was manually calibrated and is omitted.",
	18: "The four-ball trough is under-apron hardware; runtime and the Pro script prove occupancy semantics, but no retained named object identifies the physical switch-18 socket.",
	19: "The four-ball trough is under-apron hardware; runtime and the Pro script prove occupancy semantics, but no retained named object identifies the physical switch-19 socket.",
	20: "The four-ball trough is under-apron hardware; runtime and the Pro script prove occupancy semantics, but no retained named object identifies the physical switch-20 socket.",
	21: "The four-ball trough is under-apron hardware; runtime and the Pro script prove occupancy semantics, but no retained named object identifies the physical switch-21 socket.",
	22: "The trough jam opto is hidden under the apron; the Pro script proves its role but no retained named object identifies its physical socket.",
	23: "The shooter-lane switch is a hidden under-apron/lane projection; the Pro script proves its role but no retained named object supplies a reproducible center.",
	26: "The left slingshot switch point was manually calibrated; no retained named Pro object supplies a reproducible center.",
	27: "The right slingshot switch point was manually calibrated; no retained named Pro object supplies a reproducible center.",
	41: "LE-only left-ramp entrance semantics are proven, but the Pro LeftRampStart object is not LE geometry and no exact LE physical/manual coordinate is available.",
	42: "The moving AMP-bank target point was manually projected from assembly geometry; no retained named Pro object supplies a reproducible switch-42 center.",
	43: "The moving AMP-bank target point was manually projected from assembly geometry; no retained named Pro object supplies a reproducible switch-43 center.",
	44: "The moving AMP-bank target point was manually projected from assembly geometry; no retained named Pro object supplies a reproducible switch-44 center.",
	45: "The AMP-bank down endpoint is a moving/hidden assembly contact; the current point was manually projected and no retained named Pro object supplies its physical center.",
	46: "The AMP-bank up endpoint is a moving/hidden assembly contact; the current point was manually projected and no retained named Pro object supplies its physical center.",
	47: "LE-only transporter-down semantics are proven by service diagnostics, but no exact LE physical/manual anchor reproduces its normalized endpoint.",
	48: "LE-only transporter-up semantics are proven by service diagnostics, but no exact LE physical/manual anchor reproduces its normalized endpoint.",
	57: "The AMP-suit down endpoint is a hidden mechanism contact; service diagnostics prove semantics but no retained named Pro object supplies a reproducible playfield center.",
	58: "The AMP-suit up endpoint is a hidden mechanism contact; service diagnostics prove semantics but no retained named Pro object supplies a reproducible playfield center.",
	72: "The LE ceramic-ball detector is physically proven at the shooter-lane rails, but the photo/diagnostics do not reproduce a normalized Pro-frame coordinate.",
}

# The table contains alpha helpers for lamps.  Only lN centers are retained for
# insert emitters; helper bloom objects are deliberately not counted as sockets.
LAMP_POSITIONS = {
	3: (0.490606, 0.871016), 4: (0.489311, 0.803019), 5: (0.490046, 0.775875),
	6: (0.490108, 0.748433), 7: (0.490320, 0.721313), 8: (0.491633, 0.694519),
	9: (0.490593, 0.666413), 10: (0.204757, 0.458810), 11: (0.197404, 0.486528),
	12: (0.190051, 0.514483), 13: (0.183092, 0.542734), 14: (0.881488, 0.671041),
	15: (0.796750, 0.645379), 16: (0.718503, 0.598145), 17: (0.186950, 0.658666),
	18: (0.120206, 0.653066), 19: (0.048361, 0.691689), 21: (0.794232, 0.563551),
	22: (0.784566, 0.535861), 23: (0.205179, 0.261519), 24: (0.302713, 0.636794),
	26: (0.227358, 0.590894), 27: (0.546577, 0.531511), 28: (0.651375, 0.534054),
	29: (0.448355, 0.489142), 30: (0.568368, 0.486411), 31: (0.686702, 0.491590),
	32: (0.767487, 0.501427), 33: (0.802111, 0.457354), 34: (0.728551, 0.437536),
	35: (0.651247, 0.435080), 36: (0.596263, 0.436781), 37: (0.549382, 0.424034),
	38: (0.424333, 0.443473), 39: (0.186908, 0.410505), 40: (0.343304, 0.460807),
	41: (0.312156, 0.416686), 42: (0.157942, 0.371003), 43: (0.392223, 0.379691),
	47: (0.273348, 0.354630), 48: (0.463374, 0.291765), 49: (0.473082, 0.348597),
	50: (0.479694, 0.392849), 51: (0.681430, 0.273536), 52: (0.182784, 0.227682),
	53: (0.710730, 0.214331), 54: (0.361170, 0.095972), 55: (0.427346, 0.104674),
	56: (0.503360, 0.103347), 57: (0.381010, 0.624996), 58: (0.452981, 0.616932),
	59: (0.530136, 0.616860), 60: (0.305714, 0.141477), 61: (0.574984, 0.135021),
	62: (0.448272, 0.216258), 63: (0.605783, 0.625215), 64: (0.681766, 0.636594),
}

LE_LAMP_SPATIAL_BLOCKERS = {
	20: "LE-only lamp-20 insert is physically present, but its manual/IPDB/photo point was a calibration, not a retained named Pro VPX center.",
	44: "LE-only lamp-44 insert is physically present, but its manual/IPDB/photo point was a calibration, not a retained named Pro VPX center.",
	45: "LE-only lamp-45 insert is physically present, but its manual/IPDB/photo point was a calibration, not a retained named Pro VPX center.",
	46: "LE-only lamp-46 insert is physically present, but its manual/IPDB/photo point was a calibration, not a retained named Pro VPX center.",
}

SOLENOID_POSITIONS = {
	1: [(0.848214, 0.871661)], 2: [(0.951090, 0.977482)], 3: [(0.621849, 0.385057)],
	6: [(0.774160, 0.376832)], 7: [(0.774160, 0.376832)], 9: [(0.310465, 0.142791)],
	10: [(0.575565, 0.133134)], 11: [(0.443293, 0.214691)],
	15: [(0.320378, 0.831324)], 16: [(0.663720, 0.829669)],
}

# The remaining solenoid anchors come from the primary candidate. These seven
# centers are archive-candidate geometry and therefore cite the archive hash.
ARCHIVE_SOLENOID_POSITION_ADDRESSES = {2, 3, 6, 7, 11, 15, 16}

SOLENOID_SPATIAL_BLOCKERS = {
	4: "LE-only marching-leg actuator semantics and presence are proven, but no exact LE physical/manual anchor supplies a normalized playfield point.",
	5: "The AMP-bank relay controls a moving/hidden assembly; its previous point was a manual assembly projection, not a retained named Pro VPX center.",
	12: "LE-only marching-leg actuator semantics and presence are proven, but no exact LE physical/manual anchor supplies a normalized playfield point.",
	13: "The AMP-suit direction relay is an internal mechanism load; its previous shared AMP point was manually calibrated and is omitted.",
	14: "LE-only transporter motor semantics are proven by diagnostics, but no exact LE physical/manual anchor reproduces a normalized motor point.",
	17: "The left slingshot coil point was manually calibrated; no retained named Pro object supplies a reproducible effect center.",
	18: "The right slingshot coil point was manually calibrated; no retained named Pro object supplies a reproducible effect center.",
	19: "The AMP-suit motor is an internal mechanism load; its previous shared AMP point was manually calibrated and is omitted.",
	27: "LE-only bottom-arch flasher multiplicity is physically proven, but the two normalized points were manually calibrated and no exact LE/manual socket anchors are retained.",
}

CABINET_INPUT_ADDRESSES = {15, 16, 65, 66, 67, 68, 69, 84, 82, -7, -6, -5, -3, -2, -1, 0}
CABINET_OUTPUT_ROLES = {
	8: "cabinet.shaker", 21: "cabinet.backpanel-flasher", 24: "cabinet.coin-meter",
}


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _located(device: dict[str, object], role: str, positions: list[tuple[float, float]], source_refs: tuple[str, ...]) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append({"id": f"{device['id']}.{role}{suffix}", "role": role, "space": "playfield", "x": x, "y": y, "provenance": _provenance(*source_refs)})
	device["spatial"] = {"status": "candidate", "placements": placements}


def _not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": _provenance(*source_refs)}


def _spatial_blocked(device: dict[str, object], text: str) -> None:
	device.pop("spatial", None)
	_note(device, f"Spatial blocker: {text}")


def _note(device: dict[str, object], text: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {text}".strip()


def _source_refs_for_input(address: int) -> tuple[str, ...]:
	geometry_source = LOCAL_PRIMARY_SOURCE if address in PRIMARY_INPUT_POSITION_ADDRESSES else LOCAL_ARCHIVE_SOURCE
	return (MANUAL_SOURCE, geometry_source)


def _source_refs_for_solenoid(address: int) -> tuple[str, ...]:
	geometry_source = LOCAL_ARCHIVE_SOURCE if address in ARCHIVE_SOLENOID_POSITION_ADDRESSES else LOCAL_PRIMARY_SOURCE
	return (MANUAL_SOURCE, geometry_source)


def apply_spatial(definition: dict[str, object]) -> None:
	if any("spatial" in device for device in [*definition["inputs"], *definition["outputs"]]):
		raise ValueError("Avatar LE spatial curation requires a fresh build(True) definition")

	seen_le_only_switches: set[int] = set()
	for device in definition["inputs"]:
		binding = device["binding"]
		group, address = str(binding["group"]), int(binding["device"])
		if group == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE, CORE_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE, LE_ROM_SOURCE)
		elif group != "pinmame.input.switch":
			raise ValueError(f"Unexpected Avatar LE input group {group!r}")
		elif address in {83, 81}:
			positions = [(0.320378, 0.831324)] if address == 83 else [(0.663720, 0.829669)]
			_located(device, "sensor", positions, (MANUAL_SOURCE, LOCAL_ARCHIVE_SOURCE))
			_note(device, "The EOS contact is an implicit part of the exact flipper assembly; the flipper center is the reviewed assembly anchor, not a second virtual switch.")
		elif address in INPUT_SPATIAL_BLOCKERS:
			if address in LE_ONLY_SWITCHES:
				seen_le_only_switches.add(address)
			_spatial_blocked(device, INPUT_SPATIAL_BLOCKERS[address])
		elif address in CABINET_INPUT_ADDRESSES:
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif address in INPUT_POSITIONS:
			_located(device, "sensor", INPUT_POSITIONS[address], _source_refs_for_input(address))
		else:
			raise ValueError(f"Avatar LE input {group} {address} has no reviewed spatial disposition")
	if seen_le_only_switches != LE_ONLY_SWITCHES:
		raise ValueError(f"Avatar LE LE-only switch spatial audit mismatch: {sorted(seen_le_only_switches)}")

	for device in definition["outputs"]:
		binding = device["binding"]
		group, address = str(binding["group"]), int(binding["device"])
		kind, availability = str(device["kind"]), str(device["availability"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE, LE_RUNTIME_SOURCE)
		elif availability == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE, LE_ROM_SOURCE)
		elif group == "pinmame.output.gi" and address == 0:
			_spatial_blocked(device, "GI-0 is one table-wide controller channel. The retained VPX GIWhite/light helpers are render aids rather than physical sockets, so no quantity or normalized emitter coordinates are asserted without an exact LE physical/manual socket map.")
		elif group == "pinmame.output.lamp":
			if address in {1, 2}:
				device.setdefault("roles", ["cabinet.start" if address == 1 else "cabinet.tournament-start"])
				_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
			elif address in LE_LAMP_SPATIAL_BLOCKERS:
				_spatial_blocked(device, LE_LAMP_SPATIAL_BLOCKERS[address])
				device.setdefault("physical", {})["quantity"] = 1
			elif address in LAMP_POSITIONS:
				_located(device, "emitter", [LAMP_POSITIONS[address]], (MANUAL_SOURCE, LOCAL_ARCHIVE_SOURCE))
				device.setdefault("physical", {})["quantity"] = 1
			elif availability == "unused":
				_not_applicable(device, "unused", MANUAL_SOURCE, LE_ROM_SOURCE)
			else:
				raise ValueError(f"Avatar LE lamp {address} has no reviewed spatial disposition")
		elif group == "pinmame.output.solenoid" and address in CABINET_OUTPUT_ROLES:
			device.setdefault("roles", [CABINET_OUTPUT_ROLES[address]])
			if address == 21:
				device.setdefault("physical", {})["quantity"] = 2
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.solenoid" and kind == "flasher" and address in SPATIAL_BLOCKED_FLASHERS:
			device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES[address]
			if address == 22:
				_spatial_blocked(device, "Q22 is a physical Link flasher, but its retained Pro VPX Light.f22 record is explicitly a fantasy placement; no exact LE/manual socket coordinate is available, so the spatial assertion is omitted.")
			else:
				_spatial_blocked(device, "Physical flasher quantity is retained, but no exact LE/manual socket coordinate is available. Pro VPX glow/render helpers are not accepted as spatial evidence; the spatial assertion is omitted pending a physical/manual-backed anchor.")
		elif group == "pinmame.output.solenoid" and address in SOLENOID_SPATIAL_BLOCKERS:
			_spatial_blocked(device, SOLENOID_SPATIAL_BLOCKERS[address])
			device.setdefault("physical", {})["quantity"] = FLASHER_QUANTITIES.get(address, 1)
		elif group == "pinmame.output.solenoid" and address in SOLENOID_POSITIONS:
			positions = SOLENOID_POSITIONS[address]
			_located(device, "emitter" if kind == "flasher" else "effect", positions, _source_refs_for_solenoid(address))
			device.setdefault("physical", {})["quantity"] = len(positions)
			if address == 3:
				_note(device, "The AMP suit magnet uses the retained shared Pro named-object anchor; its normalized point is a physical assembly location, not a ball teleport target.")
		else:
			raise ValueError(f"Avatar LE output {group} {address} ({kind}) has no reviewed spatial disposition")

def _append_sources(definition: dict[str, object]) -> None:
	definition["sources"].extend([
		{"id": LOCAL_ARCHIVE_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/stern/avatar-limited-edition-2010/archive-local/Avatar.vpx", "sha256": "aaff981437470f8c4edf6b2902e7a6d78db19d826a04d9662e3bcb812dd9740d", "locator": "Exact retained local archive candidate; 177713152 bytes; vpxtool v0.33.3 extraction retained externally. Embedded controller script is Pro avr_200. Only directly named Pro playfield objects whose semantics reconcile to a common LE device are accepted; their extracted bounds, object names, and centers are the reproducible anchor record. No trough, hidden, LE-only, or render-helper point is accepted.", "license": "NOASSERTION", "attribution": "Local authorized VPX inventory"},
		{"id": LOCAL_PRIMARY_SOURCE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/stern/avatar-limited-edition-2010/primary-local/avatar 080116a mod 1.19.vpx", "sha256": "0ec4b08799eb3470b518a431142943c9a8548166da596c5e1cd9e856b15ca9ad", "locator": "Exact retained local primary candidate; 60641280 bytes; vpxtool v0.33.3 extraction retained externally. Embedded controller script is Pro avr_200. Only directly named Pro playfield objects whose semantics reconcile to a common LE device are accepted; their extracted bounds, object names, and centers are the reproducible anchor record. No LE-only actuator, hidden projection, or render-helper point is accepted.", "license": "NOASSERTION", "attribution": "Local authorized VPX inventory"},
		{"id": LE_PLAYFIELD_PHOTO_SOURCE, "kind": "human_review", "uri": "external:pinmame-review-artifacts/stern/avatar-limited-edition-2010/physical-references/avatar-le-spielfeld99.jpg", "sha256": "cf8c494c797d9ad744e4f2cd7730a61153bcc3ee43e718729852f5507581dab8", "locator": "Retained vendor-hosted Avatar LE playfield photo used to verify the LE transporter-cover and LE-only assembly regions; photo is a visual reference, not a VPX geometry source.", "license": "NOASSERTION", "attribution": "Pinball Universe product photography"},
	])


def _spatial_knowledge() -> str:
	text = fail_closed_spatial_knowledge("stern.avatar-limited-edition.2010", LE_KNOWLEDGE)
	spatial = """## Spatial review status

The ordered table search found no exact LE VPX table. The two retained local candidates are Pro `avr_200` tables. The partial definition retains only direct centers of named Pro playfield objects whose semantics reconcile to common LE devices; the source hashes and retained extraction object records are the reproducible anchors. The canonical space is normalized player view: x=0 left, x=1 right, y=0 rear/backglass end, and y=1 front/apron end.

Exact blockers are deliberately visible:

- Inputs 8, 18-23, 26-27, 41-46, 47-48, 57-58, and 72 are explicit blockers. Their switch semantics and physical presence are retained, but the prior right-bank/slingshot/trough/AMP/transporter/detector points were manual, hidden, or LE-only projections without a reproducible named Pro anchor.
- Outputs Q4, Q5, Q12-Q14, Q17-Q19, and Q27 are explicit blockers. Their physical devices and quantities remain documented, but marching-leg, AMP-bank, suit, slingshot, transporter, and bottom-arch coordinates are not asserted without exact LE/manual socket anchors.
- Q20, Q22, Q23, Q25, Q26, and Q28-Q32 retain physical flasher quantities but no spatial records. Q22's Pro `Light.f22` is explicitly a fantasy placement, and the other retained VPX flasher objects are not proven physical sockets.
- Lamps 20 and 44-46 retain their LE physical inventory but no spatial records because the previous manual/IPDB/photo points were calibrated projections, not named Pro centers.
- GI-0 retains its one controller channel but no physical quantity or coordinates. `GIWhite` is a table-wide render light, not a physical socket map. The DMD is explicitly controlled N/A because it is a cabinet display.

The exact ROM/service diagnostics, manual, IPDB record, and photo continue to establish LE-only semantics, quantities, and mechanism causality. They do not manufacture missing normalized coordinates.

"""
	return text.replace("## Sources\n", spatial + "## Sources\n", 1)


_ARTIFACT_SUMMARY = """# Avatar LE spatial review summary

The canonical schema-v2 partial definition is generated by `tools/curate_avatar_le_spatial.py` from `build(True)`.

- Coordinate space: normalized playfield, x=0 left / x=1 right / y=0 rear-backglass / y=1 apron.
- Exact edition VPX search: local Tables, local Tables Archive, authenticated VPU, then VPForums. No exact LE VPX table was found; the two retained local candidates are Pro `avr_200` and are shared-geometry evidence only.
- Explicit spatial blockers are inputs 8, 18-23, 26-27, 41-46, 47-48, 57-58, and 72; outputs Q4, Q5, Q12-Q14, Q17-Q19, Q20, Q22-Q23, Q25-Q32; lamps 20 and 44-46; and GI-0.
- Q22 `Light.f22`, `GIWhite`, all render helpers, and all manual/physical-only projections are excluded as placement anchors. Switch 41, unresolved flasher sockets, and GI-0 remain intentionally blocked.
- Retained candidate projections and controlled N/A records are explicit in the definition; missing spatial evidence remains `coverage.missing = ["spatial_placement"]`.
"""


def _build_definition() -> dict[str, object]:
	definition = build(True)
	_append_sources(definition)
	apply_spatial(definition)
	definition["schema_version"] = 2
	definition["coverage"]["status"] = "partial"
	definition["coverage"]["missing"] = ["spatial_placement"]
	definition["coverage"]["dimensions"]["spatial_placement"] = "unknown"
	for display in definition["displays"]:
		display["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": _provenance(CORE_SOURCE, MANUAL_SOURCE)}
	return definition


def _canonical_outputs(definition: dict[str, object]) -> dict[Path, bytes]:
	return {
		PARTIAL_PATH: canonical_bytes(definition),
		KNOWLEDGE_PATH: _spatial_knowledge().encode("utf-8"),
	}


def _ensure_author_ready_absent() -> None:
	if AUTHOR_READY_PATH.exists():
		raise RuntimeError(f"Refusing to curate Avatar LE partial state while author-ready artifact exists: {AUTHOR_READY_PATH}")


def curate(artifact_root: Path | None = None) -> None:
	_ensure_author_ready_absent()
	definition = _build_definition()
	for path, content in _canonical_outputs(definition).items():
		write_bytes(path, content)
	if artifact_root is None:
		return
	artifact_root = artifact_root.resolve()
	write_bytes(artifact_root / "analysis/canonical-spatial-summary.md", _ARTIFACT_SUMMARY.encode("utf-8"))
	write_bytes(artifact_root / "analysis/canonical-spatial-overlay.svg", render_spatial_overlay(definition).encode("utf-8"))


def check(artifact_root: Path | None = None) -> int:
	"""Rebuild expected canonical state in memory and compare it without writing."""
	definition = _build_definition()
	mismatches: list[str] = []
	for path, expected in _canonical_outputs(definition).items():
		if not path.exists():
			mismatches.append(f"missing canonical file: {path}")
		elif path.read_bytes() != expected:
			mismatches.append(f"canonical content mismatch: {path}")
	if AUTHOR_READY_PATH.exists():
		mismatches.append(f"refusing to curate while author-ready artifact exists (preserved): {AUTHOR_READY_PATH}")
	if mismatches:
		for mismatch in mismatches:
			print(mismatch, file=sys.stderr)
		return 1
	print("Avatar LE canonical curator check passed; no files were written or deleted.")
	return 0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	mode = parser.add_mutually_exclusive_group(required=True)
	mode.add_argument("--write", action="store_true", help="Explicitly write canonical partial, knowledge, and optional external artifacts.")
	mode.add_argument("--check", action="store_true", help="Reconstruct expected canonical state and compare it without writing or deleting files.")
	parser.add_argument("--artifact-root", type=Path, help="Optional portable directory for review summary and SVG artifacts.")
	args = parser.parse_args()
	if args.check:
		raise SystemExit(check(args.artifact_root))
	curate(args.artifact_root)
