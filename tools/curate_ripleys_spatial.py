"""Apply reviewed spatial evidence to the fail-closed Ripley's partial."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
from typing import Any, Sequence

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from curate_ripleys import KNOWLEDGE, TABLE_SOURCE, build
from pinmame_game_defs.jsonio import write_json, write_text
from pinmame_game_defs.spatial import fail_closed_spatial_knowledge, fail_closed_spatial_partial

MANUAL_SOURCE = "manual.stern-ripleys.2004"
VPX_SOURCE = "vpx.ripleys-vpwmod-1.3"
CORE_SOURCE = "pinmame.core.4ec52ff0ac13"
TABLE_BOUNDS = (952, 2115)
TABLE_VPX_RELATIVE_PATH = Path("stern/ripley-s-believe-it-or-not-2004/Ripley_s Believe It or Not (Stern 2004)1.0.3.vpx")
TABLE_VPX_SHA256 = "6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48"
TABLE_CONTENT_REVISION = TABLE_VPX_SHA256[:40]
SCRIPT_ENV_VAR = "PINMAME_VPX_SOURCES_ROOT"
SCRIPT_RELATIVE_PATH = Path("stern/ripley-s-believe-it-or-not-2004/extracted-vpxtool/script.vbs")
EXTRACTION_RELATIVE_PATH = SCRIPT_RELATIVE_PATH.parent
SCRIPT_SHA256 = "717696937a92b076620c2564982a7b514786e72fdab01d761b3b2a301346e014"
SCRIPT_ENCODING = "cp1252"
EXTRACTION_MANIFEST_SHA256 = "79cdb19cd01d46d795b32b7638a0f75c19bf824256de89a879d9d5328ce6b61d"
EXTRACTION_MANIFEST_FILE_COUNT = 1152


def provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(dict.fromkeys(source_refs))}


class _ObjectSpec:
	def __init__(self, kind: str, name: str, property: str, suffix: str | None = None) -> None:
		self.kind = kind
		self.name = name
		self.property = property
		self.suffix = suffix

	@property
	def filename(self) -> str:
		return f"{self.kind}.{self.name}.json"


def _spec(kind: str, name: str, property: str, suffix: str | None = None) -> _ObjectSpec:
	return _ObjectSpec(kind, name, property, suffix)


class _VPXExtraction:
	"""Resolve only explicitly selected objects from the retained vpxtool tree."""

	def __init__(self, path: Path) -> None:
		self.path = path.resolve()
		if not self.path.is_dir():
			raise ValueError(f"Retained Ripley's extraction must be a directory: {self.path}")
		self.manifest_sha256, self.manifest_file_count = self._manifest()
		if (self.manifest_sha256, self.manifest_file_count) != (EXTRACTION_MANIFEST_SHA256, EXTRACTION_MANIFEST_FILE_COUNT):
			raise ValueError(
				"Retained Ripley's extraction manifest mismatch: "
				f"expected {EXTRACTION_MANIFEST_SHA256}/{EXTRACTION_MANIFEST_FILE_COUNT}, "
				f"got {self.manifest_sha256}/{self.manifest_file_count}"
			)
		self.bounds = self._read_bounds()
		if self.bounds != (0.0, 0.0, float(TABLE_BOUNDS[0]), float(TABLE_BOUNDS[1])):
			raise ValueError(f"Unexpected retained Ripley's extraction bounds: {self.bounds}")
		self.audit: list[dict[str, object]] = []

	def _manifest(self) -> tuple[str, int]:
		entries = []
		for path in self.path.rglob("*"):
			if not path.is_file():
				continue
			relative = path.relative_to(self.path).as_posix()
			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			entries.append((relative, digest))
		entries.sort()
		payload = "".join(f"{digest}  {relative}\n" for relative, digest in entries).encode("utf-8")
		return hashlib.sha256(payload).hexdigest(), len(entries)

	def _read_json(self, path: Path) -> Any:
		try:
			return json.loads(path.read_bytes().decode("utf-8-sig"))
		except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
			raise ValueError(f"Unable to read retained VPX extraction JSON {path}: {error}") from error

	def _read_bounds(self) -> tuple[float, float, float, float]:
		path = self.path / "gamedata.json"
		if not path.is_file():
			raise ValueError(f"Retained Ripley's extraction has no gamedata.json: {path}")
		value = self._read_json(path)
		if not isinstance(value, dict):
			raise ValueError("Retained Ripley's gamedata.json is not an object")
		try:
			bounds = tuple(float(value[key]) for key in ("left", "top", "right", "bottom"))
		except (KeyError, TypeError, ValueError) as error:
			raise ValueError("Retained Ripley's gamedata.json has incomplete bounds") from error
		if not all(math.isfinite(item) for item in bounds) or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
			raise ValueError(f"Invalid retained Ripley's extraction bounds: {bounds}")
		return bounds

	def resolve(self, spec: _ObjectSpec, device_id: str | None = None) -> dict[str, object] | None:
		path = self.path / "gameitems" / spec.filename
		if not path.is_file():
			raise ValueError(f"Selected VPX object is missing: {path}")
		document = self._read_json(path)
		if not isinstance(document, dict) or len(document) != 1:
			raise ValueError(f"Selected VPX object has an unexpected document shape: {path}")
		kind, value = next(iter(document.items()))
		if kind != spec.kind or not isinstance(value, dict):
			raise ValueError(f"Selected VPX object kind mismatch for {path}: expected {spec.kind}, got {kind}")
		if value.get("name") != spec.name:
			raise ValueError(f"Selected VPX object name mismatch for {path}: expected {spec.name!r}, got {value.get('name')!r}")

		if spec.property == "center":
			point = value.get("center")
		elif spec.property == "position":
			point = value.get("position")
		elif spec.property == "pos_x/pos_y":
			point = {"x": value.get("pos_x"), "y": value.get("pos_y")}
		elif spec.property == "drag_points.centroid":
			points = value.get("drag_points")
			if not isinstance(points, list) or not points:
				point = None
			else:
				coordinates = [(item.get("x"), item.get("y")) for item in points if isinstance(item, dict)]
				if not coordinates or any(not isinstance(x, (int, float)) or not isinstance(y, (int, float)) for x, y in coordinates):
					point = None
				else:
					point = {"x": sum(float(x) for x, _ in coordinates) / len(coordinates), "y": sum(float(y) for _, y in coordinates) / len(coordinates)}
		else:
			raise ValueError(f"Unsupported selected VPX coordinate property: {spec.property}")
		if not isinstance(point, dict) or not isinstance(point.get("x"), (int, float)) or not isinstance(point.get("y"), (int, float)):
			raise ValueError(f"Selected VPX object has no usable {spec.property} point: {path}")
		raw_x, raw_y = float(point["x"]), float(point["y"])
		left, top, right, bottom = self.bounds
		normalized_x = (raw_x - left) / (right - left)
		normalized_y = (raw_y - top) / (bottom - top)
		record: dict[str, object] = {
			"filename": spec.filename,
			"kind": spec.kind,
			"name": spec.name,
			"property": spec.property,
			"raw_x": raw_x,
			"raw_y": raw_y,
			"normalized_x": round(normalized_x, 6),
			"normalized_y": round(normalized_y, 6),
		}
		if device_id is not None:
			record["device_id"] = device_id
		if spec.suffix is not None:
			record["placement_suffix"] = spec.suffix
		if not 0 <= normalized_x <= 1 or not 0 <= normalized_y <= 1:
			record["status"] = "unresolved"
			if spec.kind.casefold() == "flasher":
				record["reason"] = "The selected Flasher is a graphical render helper and its point is outside the retained playfield bounds; no polygon centroid, nearby object, or proxy may replace it, and no physical socket is asserted."
			else:
				record["reason"] = "The selected object point is outside the retained playfield bounds; no polygon centroid, nearby object, or proxy may replace it."
			self.audit.append(record)
			return None
		if spec.kind.casefold() == "flasher":
			record["status"] = "unresolved"
			record["reason"] = "The selected Flasher is a graphical render helper; its in-bounds pos_x/pos_y and polygon do not establish physical socket evidence, so placement is withheld pending physical/manual corroboration."
			self.audit.append(record)
			return None
		record["status"] = "validated"
		self.audit.append(record)
		return record


def _located_from_objects(device: dict[str, object], role: str, specs: list[_ObjectSpec], extraction: _VPXExtraction, source_refs: tuple[str, ...]) -> list[dict[str, object]]:
	placements = []
	unresolved = []
	for index, spec in enumerate(specs, start=1):
		record = extraction.resolve(spec, str(device["id"]))
		if record is None:
			unresolved.append(extraction.audit[-1])
			continue
		x, y = float(record["normalized_x"]), float(record["normalized_y"])
		placement_suffix = f".{spec.suffix}" if spec.suffix else (f".{index:02d}" if len(specs) > 1 else "")
		placements.append({
			"id": f"{device['id']}.{role}{placement_suffix}",
			"role": role,
			"space": "playfield",
			"x": x,
			"y": y,
			"provenance": provenance(*source_refs),
		})
	if placements:
		device["spatial"] = {"status": "validated", "placements": placements}
	return [
		{
			"filename": record["filename"],
			"kind": record["kind"],
			"name": record["name"],
			"property": record["property"],
			"reason": record["reason"],
		}
		for record in unresolved
	]


def not_applicable(device: dict[str, object], reason: str, *source_refs: str) -> None:
	device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": provenance(*source_refs)}


# Which retained table Bumper body carries each pop-bumper address, for all three device types
# (switch, coil, lamp) that sit on one physical bumper.
#
# The retained known-working table is internally inconsistent here and only one half of it can be
# right. Its switch handlers bind Bumper5 -> switch 27 ("lower bottom") and Bumper6 -> switch 26
# ("lower right"), with the same inversion upstairs (Bumper2 -> 51, Bumper3 -> 50). Its lamp
# handling in the same file binds the opposite way: BumperLight5 -> lamp 34 ("lower right"),
# BumperLight6 -> lamp 35 ("lower bottom"), BumperLight2 -> lamp 61 ("upper right"),
# BumperLight3 -> lamp 62 ("upper bottom"). BumperLightN sits on top of BumperN, so the
# light-to-body association is not in doubt; the two halves genuinely disagree.
#
# The manual settles it against the switch half, on two independent drawings:
#
#   * Coil & Flash Lamp Locations (PDF page 35, printed Sec. 3 Chp. 2 Page 19) places #7 LOWER
#     RIGHT POP at normalized x ~0.266 and #8 LOWER BOTTOM POP at ~0.156, and #10 UPPER RIGHT POP
#     at ~0.831 with #11 UPPER BOTTOM POP at ~0.790.
#   * Switch Matrix Grid Locations (PDF page 33, printed Sec. 3 Chp. 2 Page 17) labels the same
#     three bodies in the same order.
#
# In both drawings "right" is the greatest x and "bottom" is the body nearest the player (greatest
# y). Reading "bottom" as "the body drawn lowest in the cluster" is what produces the reversal,
# because the rightmost body is drawn higher up than the bottom one. An earlier revision of this
# curator followed the script's switch half and shipped eight reversed `validated` placements.
# Keyed per device type on purpose: the switch, solenoid and lamp namespaces overlap numerically
# (switch 9 is the head stand-up, solenoid 9 is the upper-left pop, lamp 33 is a pop-bumper lamp
# while switch 33 is a playfield trigger), so a single flat table keyed by bare address would let a
# lookup silently mean the wrong device.
POP_BUMPER_BODIES: dict[str, dict[int, str]] = {
	#                     lower left  lower right  lower bottom  upper left  upper right  upper bottom
	"switch": {25: "Bumper4", 26: "Bumper5", 27: "Bumper6", 49: "Bumper1", 50: "Bumper2", 51: "Bumper3"},
	"solenoid": {6: "Bumper4", 7: "Bumper5", 8: "Bumper6", 9: "Bumper1", 10: "Bumper2", 11: "Bumper3"},
	"lamp": {33: "Bumper4", 34: "Bumper5", 35: "Bumper6", 60: "Bumper1", 61: "Bumper2", 62: "Bumper3"},
}

INPUT_OBJECTS: dict[int, list[_ObjectSpec]] = {
	9: [_spec("HitTarget", "sw9", "position")], 16: [_spec("Trigger", "swPlunger", "center")],
	17: [_spec("HitTarget", "sw17", "position")], 18: [_spec("Trigger", "sw18", "center")],
	19: [_spec("HitTarget", "sw19", "position")], 20: [_spec("Spinner", "sw20", "center")],
	21: [_spec("Spinner", "sw21", "center")], 22: [_spec("HitTarget", "sw22", "position")],
	23: [_spec("Trigger", "SMagnet", "center")], 24: [_spec("Trigger", "IMagnet", "center")],
	# Pop bumpers come from POP_BUMPER_BODIES, not from the retained script's own *_Hit switch
	# bindings. See the comment on that table: the script's switch half and lamp half disagree
	# about which body is "right" and which is "bottom", and the manual settles it against the
	# switch half.
	25: [_spec("Bumper", POP_BUMPER_BODIES["switch"][25], "center")], 26: [_spec("Bumper", POP_BUMPER_BODIES["switch"][26], "center")],
	27: [_spec("Bumper", POP_BUMPER_BODIES["switch"][27], "center")], 28: [_spec("Kicker", "sw28", "center")],
	29: [_spec("Kicker", "sw29", "center")], 52: [_spec("Kicker", "sw52", "center")],
	49: [_spec("Bumper", POP_BUMPER_BODIES["switch"][49], "center")], 50: [_spec("Bumper", POP_BUMPER_BODIES["switch"][50], "center")],
	51: [_spec("Bumper", POP_BUMPER_BODIES["switch"][51], "center")], 30: [_spec("Trigger", "sw30", "center")],
	31: [_spec("Trigger", "sw31", "center")],
	32: [_spec("HitTarget", "sw32", "position", "a"), _spec("HitTarget", "sw32a", "position", "b")],
	33: [_spec("Trigger", "sw33", "center")], 34: [_spec("Trigger", "sw34", "center")],
	35: [_spec("Trigger", "sw35", "center")], 36: [_spec("Trigger", "sw36", "center")],
	38: [_spec("Trigger", "sw38", "center")], 39: [_spec("Trigger", "sw39", "center")],
	40: [_spec("Trigger", "sw40", "center")], 41: [_spec("Trigger", "sw41", "center")],
	42: [_spec("Trigger", "sw42", "center")], 43: [_spec("Trigger", "sw43", "center")],
	47: [_spec("Trigger", "sw47", "center")], 48: [_spec("Trigger", "sw48", "center")],
	53: [_spec("Trigger", "sw53", "center")], 57: [_spec("Trigger", "sw57", "center")],
	58: [_spec("Trigger", "sw58", "center")], 59: [_spec("Wall", "Leftslingshot", "drag_points.centroid")],
	60: [_spec("Trigger", "sw60", "center")], 61: [_spec("Trigger", "sw61", "center")],
	62: [_spec("Wall", "Rightslingshot", "drag_points.centroid")],
	81: [_spec("Flipper", "RightFlipper", "center")], 83: [_spec("Flipper", "LeftFlipper", "center")],
}

UNRESOLVED_INPUTS = {11, 12, 13, 14, 15, 44, 45, 46}
CABINET_INPUTS = {1, 2, 3, 4, 5, 6, 7, 8, 54, 55, 56, -3, -2, -1, 0, 82, 84, 88}


LAMP_OBJECTS: dict[int, list[_ObjectSpec]] = {
	address: [_spec("Flasher", f"l{address}", "pos_x/pos_y")] if address == 16 else [_spec("Light", f"l{address}", "center")]
	for address in (set(range(1, 33)) | set(range(36, 60)) | set(range(63, 76)))
}
# The six pop-bumper lamps sit inside their bumper body, so each is placed on the body its own
# BumperLight object sits on -- which is also the body the manual's drawings put that lamp's
# printed name on, and the body this file now places that bumper's switch and coil on. All three
# device types on one physical bumper therefore agree.
LAMP_OBJECTS.update({
	address: [_spec("Light", f"BumperLight{POP_BUMPER_BODIES['lamp'][address][len('Bumper'):]}", "center")]
	for address in POP_BUMPER_BODIES["lamp"]
})

# 76/77/78 (Back Panel A/B/C) stay unresolved. Unlike the six above they have no Light object at
# all: the table models them only as three Flasher sprites sharing one (x, y) = 0.567396/0.492008,
# differing solely in stacked height (220/175/130 with rot_x = -90). That is a single vertical
# panel rather than three distinct bulb positions, the same shape The Simpsons Pinball Party's
# Mini-DMD sign panel took, so no coordinate is asserted.
UNRESOLVED_LAMPS = {76, 77, 78}


GI_OBJECTS: list[_ObjectSpec] = [_spec("Light", f"gi{number}", "center", f"gi.{number:02d}") for number in range(1, 40)]


SOLENOID_OBJECTS: dict[int, list[_ObjectSpec]] = {
	1: [_spec("Kicker", "BallRelease", "center")], 2: [_spec("Plunger", "Plunger", "center")],
	3: [_spec("Kicker", "sw52", "center")], 4: [_spec("Flipper", "TempleDiv", "center")],
	5: [_spec("Flipper", "LockDiverter", "center")], 6: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][6], "center")],
	7: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][7], "center")], 8: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][8], "center")],
	9: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][9], "center")], 10: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][10], "center")],
	11: [_spec("Bumper", POP_BUMPER_BODIES["solenoid"][11], "center")], 12: [_spec("Kicker", "sw29", "center")],
	13: [_spec("Kicker", "Lock", "center")], 14: [_spec("Flipper", "RightFlipper1", "center")],
	15: [_spec("Flipper", "LeftFlipper", "center")], 16: [_spec("Flipper", "RightFlipper", "center")],
	17: [_spec("Wall", "Leftslingshot", "drag_points.centroid")], 18: [_spec("Wall", "Rightslingshot", "drag_points.centroid")],
	19: [_spec("Trigger", "IMagnet", "center")], 20: [_spec("Trigger", "SMagnet", "center")],
	22: [_spec("Light", "f22", "center")], 23: [_spec("Wall", "TopPost", "drag_points.centroid")],
	25: [_spec("Light", "f25", "center", "a"), _spec("Flasher", "f25b", "pos_x/pos_y", "b")],
	26: [_spec("Flasher", "f26", "pos_x/pos_y")], 27: [_spec("Flasher", "f27", "pos_x/pos_y")],
	28: [_spec("Light", "f28a", "center", "a"), _spec("Flasher", "f28", "pos_x/pos_y", "b")], 29: [_spec("Flasher", "f29", "pos_x/pos_y")],
	30: [_spec("Light", "f30", "center", "a"), _spec("Flasher", "f30b", "pos_x/pos_y", "b")],
	31: [_spec("Flasher", "f31", "pos_x/pos_y")], 32: [_spec("Flasher", "f32", "pos_x/pos_y")],
}
UNRESOLVED_SOLENOIDS = {21}


def _by_binding(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {int(item["binding"]["device"]): item for item in definition[collection] if item["binding"]["group"] == group}


def apply_spatial(definition: dict[str, object], extraction: _VPXExtraction) -> None:
	switches = _by_binding(definition, "inputs", "pinmame.input.switch")
	for device in definition["inputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		if group == "pinmame.input.dip":
			not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in CABINET_INPUTS:
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif address in UNRESOLVED_INPUTS:
			device.setdefault("physical", {})["location"] = "Under-playfield or lock assembly; the exact retained table does not expose a named per-address sensor center."
			device.setdefault("physical", {})["notes"] = "Spatial placement is intentionally withheld until the manual drawing and the exact table's shared ball-stack/lock objects can be reconciled per switch address."
		elif address in INPUT_OBJECTS:
			unresolved = _located_from_objects(device, "sensor", INPUT_OBJECTS[address], extraction, (TABLE_SOURCE,))
			if unresolved:
				device.setdefault("physical", {})["notes"] = (
					"The selected exact callback object has no in-bounds point under its retained extraction property "
					f"({', '.join(item['kind'] + '.' + item['name'] + ':' + item['property'] for item in unresolved)}); placement is withheld."
				)
		else:
			raise ValueError(f"Ripley's input {group} {address} has no reviewed spatial disposition")

	if switches[32]["physical"].get("quantity") != 2:
		switches[32]["physical"]["quantity"] = 2
		switches[32]["physical"]["notes"] = "Two named VPX hit targets share controller switch 32; retain both physical target assemblies and one public input."
	for address in (41, 42, 43):
		switches[address].setdefault("physical", {})["notes"] = "The three exact table trigger objects intentionally overlap on the shared vari-target opto board; do not fan them out into guessed positions."
	for address in (59, 62):
		switches[address].setdefault("physical", {})["notes"] = "The exact table exposes one named slingshot collision assembly for the controller address; the manual specifies two parallel physical contacts."

	outputs = _by_binding(definition, "outputs", "pinmame.output.solenoid")
	q_outputs = {
		int(device["wiring"]["driver_transistor"][1:]): device
		for device in outputs.values()
		if isinstance(device.get("wiring"), dict) and str(device["wiring"].get("driver_transistor", "")).startswith("Q")
	}
	for device in definition["outputs"]:
		device.pop("spatial", None)
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		q_number = int(str(device.get("wiring", {}).get("driver_transistor", "Q0"))[1:]) if str(device.get("wiring", {}).get("driver_transistor", "Q0")).startswith("Q") else address
		if device["availability"] == "unused":
			not_applicable(device, "unused", MANUAL_SOURCE)
		elif kind == "virtual":
			not_applicable(device, "virtual", CORE_SOURCE)
		elif group == "pinmame.output.lamp" and address in {79, 80}:
			device["roles"] = ["cabinet.tournament"] if address == 79 else ["cabinet.start"]
			not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
		elif group == "pinmame.output.lamp" and address in LAMP_OBJECTS:
			unresolved = _located_from_objects(device, "emitter", LAMP_OBJECTS[address], extraction, (TABLE_SOURCE,))
			device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.lamp" and address in UNRESOLVED_LAMPS:
			device.setdefault("physical", {})["quantity"] = 1
			device.setdefault("physical", {})["notes"] = "The exact retained table models the three back-panel lamps only as Flasher sprites sharing one position, differing solely in stacked height on a vertical panel, so no per-bulb playfield coordinate is asserted."
		elif group == "pinmame.output.gi" and address == 0:
			_located_from_objects(device, "emitter", GI_OBJECTS, extraction, (TABLE_SOURCE,))
			device.setdefault("physical", {})["notes"] = "The exact table's 39 named GI Light objects are retained as rendered emitter positions. They map to the manual's four separately fused physical strings; duplicate centers are preserved as separate named emitters, not collapsed or reinterpreted as extra controller channels."
		elif group == "pinmame.output.solenoid" and address == 24:
			not_applicable(device, "no_physical_device", MANUAL_SOURCE, TABLE_SOURCE)
			device.setdefault("physical", {})["notes"] = "The official manual identifies Q24 as optional unassigned 5 V. The exact archived table's Q24 routine is sound-only; the retained VPW v1.3 script deliberately comments out its callback. Neither establishes a stock physical knocker."
		elif group == "pinmame.output.solenoid" and address in {33, 34, 35}:
			device.setdefault("physical", {})["notes"] = "Optional UK 520-5068 three-post output. The selected exact table is a UK model, but it exposes no named Q33-Q35 actuator geometry; standard-machine projection is forbidden, so spatial placement remains unresolved."
		elif group == "pinmame.output.solenoid" and q_number in UNRESOLVED_SOLENOIDS:
			device.setdefault("physical", {})["notes"] = "The exact table exposes the visible vari-target assembly and Q21 callback semantics, but no named reset-coil actuator center. The visible target point is not promoted as a coil location."
		elif group == "pinmame.output.solenoid" and q_number in SOLENOID_OBJECTS:
			role = "emitter" if kind == "flasher" else "effect"
			unresolved = _located_from_objects(device, role, SOLENOID_OBJECTS[q_number], extraction, (TABLE_SOURCE,))
			if unresolved:
				physical = device.setdefault("physical", {})
				existing_notes = str(physical.get("notes", "")).strip()
				blocker_note = (
					" The selected exact callback object has no meaningful in-playfield point under its retained extraction property "
					f"({', '.join(item['kind'] + '.' + item['name'] + ':' + item['property'] for item in unresolved)}); its placement is intentionally withheld."
				)
				physical["notes"] = f"{existing_notes}{blocker_note}".strip()
			if kind == "flasher":
				physical = device.setdefault("physical", {})
				existing_notes = str(physical.get("notes", "")).strip()
				spatial_notes = "Each retained position is a direct named Light object used by the exact table's callback; graphical Flasher/Flashm/flare objects are render helpers and are not counted as physical sockets without physical/manual corroboration."
				physical["notes"] = f"{existing_notes} {spatial_notes}".strip()
		elif group == "pinmame.output.solenoid" and address in q_outputs:
			raise ValueError(f"Unexpected duplicate physical Q mapping at public address {address}")
		else:
			raise ValueError(f"Ripley's output {group} {address} ({kind}) has no reviewed spatial disposition")

	# Q22 is a switched opto emitter, not a decorative lamp, but it is still an
	# exact physical emitter in the playfield spatial model.
	q_outputs[22].setdefault("physical", {})["notes"] += " Exact Light.f22 is the switched-ground opto emitter position."

	# The DMD and the three Mini-DMD sign panels are backbox/cabinet devices. The schema restricts
	# a display's spatial record to `not_applicable` (see $defs/displaySpatial), which is a
	# controlled record to be written rather than a reason to omit the key: leaving it absent makes
	# a positively-known cabinet device indistinguishable from one nobody has looked at. Provenance
	# names both the emulator source that declares the display layout and the manual that places
	# the boards physically.
	for display in definition["displays"]:
		display.pop("spatial", None)
		not_applicable(display, "cabinet_or_service", CORE_SOURCE, MANUAL_SOURCE)


def _assert_contract(definition: dict[str, object]) -> None:
	inputs = _by_binding(definition, "inputs", "pinmame.input.switch")
	outputs = _by_binding(definition, "outputs", "pinmame.output.solenoid")
	for address in (32, 41, 42, 43, 59, 62):
		if "spatial" not in inputs[address]:
			raise ValueError(f"Expected exact switch spatial record for {address}")
	for address, minimum in ((25, 1), (28, 1), (30, 1)):
		placements = outputs[address].get("spatial", {}).get("placements", [])
		if len(placements) < minimum:
			raise ValueError(f"Q{address} requires at least {minimum} exact emitter positions")
	if len(_by_binding(definition, "outputs", "pinmame.output.gi")[0]["spatial"]["placements"]) != 39:
		raise ValueError("GI 0 requires all 39 exact table GI Light objects")
	for collection in (definition["inputs"], definition["outputs"]):
		for device in collection:
			for placement in device.get("spatial", {}).get("placements", []):
				if placement["provenance"]["source_refs"] != [TABLE_SOURCE]:
					raise ValueError(f"{placement['id']} must use only the exact VPX table as coordinate provenance")
				if not (0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1):
					raise ValueError(f"{placement['id']} must retain normalized canonical coordinates")


CONFLICTS = [
	{
		"id": "conflict.ripleys.uk-table-scope",
		"description": "The selected exact 1.0.3 VPX is explicitly a UK model with All-Skill extra posts. The canonical record covers the shared 2004 physical product plus optional UK hardware, so common named playfield objects are promoted while Q33-Q35 and any UK-only geometry remain unresolved; no standard-machine coordinates are projected from the UK table. Resolution path: a UK-market source that locates the three optional posts rather than only wiring them -- a playfield location drawing or post-kit installation sheet for the 520-5068-01 auxiliary board naming where the 090-5044-00T and 090-5030-00T posts mount, a photograph of a UK-configured playfield showing all three, or a second retained known-working VPX recreation of a UK machine that binds public 33-35 to named actuator objects -- because the retained manual's own UK 3X auxiliary-board pages (PDF 162-166) give wiring only; Ripley's was mass-produced, so a UK operator or owner can supply the photograph and a curator can search the community table archives for the second recreation. Unresolved.",
		"path": "outputs[pinmame.output.solenoid:33|34|35]",
		"source_refs": [TABLE_SOURCE, MANUAL_SOURCE, CORE_SOURCE],
	},
	{
		"id": "conflict.ripleys-q24-script-revision",
		"description": "The exact archived table's Q24 callback invokes a sound-only vpmsolsound routine, while the retained VPW v1.3 script comments out its Q24 SolKnocker callback. The Stern manual calls Q24 an optional unassigned 5 V output. The physical disposition is therefore no stock Q24 device, but the two table scripts are not behavior-identical for an optional external installation. Resolution path: a Stern accessory or parts listing, or a service bulletin, naming what the optional 5 V output at J7-P10 is sold to drive, or a photograph of an unmodified 2004 machine's Whitestar I/O Power Driver board showing whether anything is connected at that pin, either of which an operator or owner of this mass-produced machine can supply; the retained gameplay trace already observed public 24 carrying state, so what is open is physical fitment rather than whether the ROM drives the address. Unresolved.",
		"path": "outputs[pinmame.output.solenoid:24]",
		"source_refs": [TABLE_SOURCE, VPX_SOURCE, MANUAL_SOURCE],
	},
]


SPATIAL_KNOWLEDGE_APPENDIX = """## Exact-table spatial evidence and fail-closed blockers

The exact byte-preserved source for this pass is `Ripley_s Believe It or Not (Stern 2004)1.0.3.vpx`, SHA-256 `6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48`, extracted with vpxtool git:v0.33.3. The retained 1,152-file extraction snapshot has deterministic manifest SHA-256 `79cdb19cd01d46d795b32b7638a0f75c19bf824256de89a879d9d5328ce6b61d`. Its playfield bounds are 952 x 2115; normalized coordinates use x=0 at the left, x=1 at the right, y=0 at the rear/backglass end, and y=1 at the apron. The table identifies itself as the UK model and includes the All-Skill extra-post configuration. It is authoritative for each named common playfield object and for its direct script semantics, but it is not evidence for a standard-machine-only installation.

The spatial overlay promotes named direct objects for the head/tombstones, spinners, ramps, mini-playfield, magnet optos, scoop/VUK, vari-target optos, shooter, EOS/flipper assemblies, slingshot collision assemblies, six pop bumpers, Q1-Q20/Q22-Q23, direct Q25-Q32 callback objects only where a retained Light or other physical object provides socket evidence, the directly exposed matrix-lamp objects that pass the same rule, and all 39 named GI Light objects. Coordinates are derived from the selected object's exact property: `center` for direct center-bearing objects, `position` for hit targets, and `drag_points.centroid` only for the named slingshot/TopPost collision assemblies. Q25 retains only physical `Light.f25`; its graphical `Flasher.f25b` point is withheld. Q28 uses physical `Light.f28a`, not graphical `Flasher.f28`; Q30 retains its in-bounds `Light.f30` while `Flasher.f30b` is an explicit blocker. Q26, Q31, and lamp 16 remain unlocated pending physical/manual corroboration. All selected `Flasher` objects, including the out-of-bounds f27/f29/f30b/f32 callbacks, are render helpers and are not counted as sockets. Switch 32 retains two named physical target positions under one controller address; switches 41-43 intentionally share the exact overlapping vari-target opto-board anchor; switch 59 and 62 each retain one exact slingshot assembly anchor while their manual quantity remains two parallel contacts.

The definition remains schema-v2 partial. Individual trough/stacking contacts 11-15 have no per-seat geometry in the exact table's shared `cvpmBallStack`; lock contacts 44-46 have no reconciled per-seat sensor objects; Q21 exposes no named reset-coil actuator; graphical Flasher callbacks f25b, f26, f27, f28, f29, f30b, f31, and f32 are withheld as render-helper blockers even when their points are in bounds, while the out-of-bounds points are also withheld rather than replaced by polygon centroids; lamp 16's graphical Flasher.l16 is withheld pending physical/manual corroboration; optional UK Q33-Q35 have no named actuator geometry; and lamps 76-78 are modelled only as three Flasher sprites sharing one position on a vertical back panel, differing solely in stacked height, so they are withheld rather than falsely triplicated. The six pop-bumper lamps 33-35 and 60-62 are now placed on their own bumper bodies, and the four displays now carry controlled not_applicable/cabinet_or_service records rather than no record at all. These are actionable authoring blockers, not plausibility gaps.

The exact table's Q24 routine is sound-only, whereas the retained VPW v1.3 script comments out its Q24 callback. The official manual calls Q24 optional unassigned 5 V. The canonical definition therefore marks Q24 `no_physical_device` and records the script conflict without inventing a stock knocker. The exact table's GI callback style also differs from the VPW modulated callback wrapper, but both drive the same public GI 0; the manual's four fused GI strings remain the physical authority.
"""


def _geometry_blockers(audit: list[dict[str, object]]) -> list[dict[str, object]]:
	blockers = []
	for record in audit:
		if record.get("status") != "unresolved":
			continue
		device_id = str(record["device_id"])
		collection = "inputs" if device_id.startswith("switch.") else "outputs"
		blockers.append({
			"blocker": (
				f"The exact callback object {record['kind']}.{record['name']} uses {record['property']} at "
				f"({record['raw_x']}, {record['raw_y']}): {record['reason']}"
			),
			"devices": {collection: [device_id]},
			"source_object": {key: record[key] for key in ("filename", "kind", "name", "property", "raw_x", "raw_y", "normalized_x", "normalized_y")},
		})
	return blockers


def _report(definition: dict[str, object], extraction: _VPXExtraction) -> dict[str, object]:
	located_inputs = [device["id"] for device in definition["inputs"] if device.get("spatial", {}).get("status") == "validated"]
	located_outputs = [device["id"] for device in definition["outputs"] if device.get("spatial", {}).get("status") == "validated"]
	return {
		"format": "pinmame-spatial-blockers",
		"version": 1,
		"machine_id": definition["machine"]["id"],
		"coordinate_space": "playfield",
		"coordinate_convention": {"x": "left_to_right", "y": "rear_to_apron"},
		"evidence_policy": "Exact named VPX objects only; no standard-machine projection from the selected UK model; render helpers and collapsed multiplicity are withheld.",
		"selected_source": {
			"source_id": TABLE_SOURCE,
			"original_filename": "Ripley_s Believe It or Not (Stern 2004)1.0.3.vpx",
			"sha256": "6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48",
			"bounds": {"left": 0, "top": 0, "right": TABLE_BOUNDS[0], "bottom": TABLE_BOUNDS[1]},
			"vpxtool": "git:v0.33.3",
			"embedded_script_sha256": "717696937a92b076620c2564982a7b514786e72fdab01d761b3b2a301346e014",
			"extraction_manifest_sha256": EXTRACTION_MANIFEST_SHA256,
			"extraction_manifest_file_count": EXTRACTION_MANIFEST_FILE_COUNT,
			"edition": "UK model / All-Skill extra-post configuration",
		},
		"search_order": [
			{"location": "first requested local table directory", "result": "no exact Ripley's VPX found"},
			{"location": "second requested local table archive directory", "result": "exact VPX selected and retained"},
			{"location": "authenticated VPUniverse", "result": "not searched after exact local source satisfied selection"},
			{"location": "VPForums", "result": "not searched after exact local source satisfied selection"},
		],
		"promoted": {"inputs": sorted(located_inputs), "outputs": sorted(located_outputs)},
		"rejected_candidates": [
			{"filename": "Ripley_s Believe It or Not (2004).directb2s", "disposition": "rejected_non_vpx_geometry", "reason": "Backglass media is not a VPX table and cannot provide controller or playfield object geometry."},
			{"filename": "Ripley_s Believe It or Not (Stern 2004)1.0.3.directb2s", "disposition": "rejected_non_vpx_geometry", "reason": "Backglass media paired with the selected VPX; it is not a source of physical playfield object coordinates."},
		],
		"unresolved_blockers": [
			{"blocker": "The exact table's shared cvpmBallStack does not expose individual normalized seats for trough/stacking switches 11-15.", "devices": {"inputs": [11, 12, 13, 14, 15]}},
			{"blocker": "The visible lock path has Kicker.Lock and generic triggers but no exact per-seat public sensor mapping for contacts 44-46.", "devices": {"inputs": [44, 45, 46]}},
			{"blocker": "Q21's exact table exposes the vari-target assembly but no named reset-coil actuator center.", "devices": {"outputs": ["device.q21-vari-target-reset"]}},
			{"blocker": "UK-only Q33-Q35 are physical optional posts, but the selected table supplies no named actuator geometry and standard-machine projection is prohibited.", "devices": {"outputs": ["device.aux1-optional-uk-left-up-down-post", "device.aux2-optional-uk-center-up-down-post", "device.aux3-optional-uk-right-up-down-post"]}},
			{"blocker": "The exact table collapses lamps 76-78 to one shared back-panel render anchor, so their three physical multiplicity positions are withheld.", "devices": {"outputs": ["lamp.76-back-panel-a", "lamp.77-back-panel-b", "lamp.78-back-panel-c"]}},
		] + _geometry_blockers(extraction.audit),
		"object_audit": extraction.audit,
		"conflicts": CONFLICTS,
	}


class _VerifiedScript:
	"""Read the retained script and refuse provenance from any other bytes."""

	def __init__(self, path: Path) -> None:
		self.path = path
		try:
			payload = path.read_bytes()
		except OSError as error:
			raise RuntimeError(f"Unable to read retained Ripley's script: {path}") from error
		actual_sha256 = hashlib.sha256(payload).hexdigest()
		if actual_sha256 != SCRIPT_SHA256:
			raise ValueError(f"Retained Ripley's script hash mismatch: expected {SCRIPT_SHA256}, got {actual_sha256}")
		self.lines = payload.decode(SCRIPT_ENCODING).splitlines()

	def location(self, line: int, symbol: str, expected_text: str | None = None) -> dict[str, object]:
		if line < 1 or line > len(self.lines):
			raise ValueError(f"Ripley's script line {line} is outside the retained source")
		actual_text = self.lines[line - 1]
		if expected_text is not None and actual_text != expected_text:
			raise ValueError(
				f"Ripley's script provenance drift at line {line} for {symbol!r}: "
				f"expected {expected_text!r}, got {actual_text!r}"
			)
		return {"symbol": symbol, "line": line, "source_text": actual_text}


def _resolve_script_path(script_path: Path | str | None = None) -> Path:
	"""Resolve the retained script without consulting external evidence at import time."""
	if script_path is not None:
		try:
			resolved_path = Path(script_path).expanduser()
		except TypeError as error:
			raise TypeError(f"Ripley's script path must be path-like, got {type(script_path).__name__}") from error
		if not resolved_path.exists():
			raise FileNotFoundError(f"Ripley's script path does not exist: {resolved_path}")
		if not resolved_path.is_file():
			raise ValueError(f"Ripley's script path must be a regular file, got: {resolved_path}")
		return resolved_path.resolve()

	root = _resolve_source_root()
	resolved_path = root / SCRIPT_RELATIVE_PATH
	if not resolved_path.exists():
		raise FileNotFoundError(f"Retained Ripley's script does not exist below {SCRIPT_ENV_VAR}: {resolved_path}")
	if not resolved_path.is_file():
		raise ValueError(f"Retained Ripley's script must be a regular file, got: {resolved_path}")
	return resolved_path.resolve()


def _resolve_source_root() -> Path:
	root_value = os.environ.get(SCRIPT_ENV_VAR)
	if not root_value:
		raise RuntimeError(f"{SCRIPT_ENV_VAR} is unset; use the retained VPX sources root")
	try:
		root = Path(root_value).expanduser().resolve()
	except TypeError as error:
		raise TypeError(f"{SCRIPT_ENV_VAR} must name a filesystem directory") from error
	if not root.exists():
		raise FileNotFoundError(f"{SCRIPT_ENV_VAR} directory does not exist: {root}")
	if not root.is_dir():
		raise ValueError(f"{SCRIPT_ENV_VAR} must name a directory, got: {root}")
	return root


def _resolve_extraction_path() -> Path:
	"""Resolve only the pinned extraction below the configured source root."""
	resolved_path = (_resolve_source_root() / EXTRACTION_RELATIVE_PATH).resolve()
	if not resolved_path.is_dir():
		raise FileNotFoundError(f"Retained Ripley's extraction does not exist: {resolved_path}")
	return resolved_path


def _verify_retained_table(source_root: Path) -> Path:
	path = (source_root / TABLE_VPX_RELATIVE_PATH).resolve()
	if not path.is_file():
		raise FileNotFoundError(f"Retained Ripley's VPX does not exist: {path}")
	actual_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
	if actual_sha256 != TABLE_VPX_SHA256:
		raise ValueError(f"Retained Ripley's VPX hash mismatch: expected {TABLE_VPX_SHA256}, got {actual_sha256}")
	return path


def _locations(script: _VerifiedScript, *specs: tuple[int, str, str]) -> list[dict[str, object]]:
	return [script.location(line, symbol, expected_text) for line, symbol, expected_text in specs]


def _operation_location(script: _VerifiedScript, line: int, operation: str, address: int, object_symbol: str) -> dict[str, object]:
	location = script.location(line, object_symbol)
	location["operation"] = operation
	location["address"] = address
	return location


def _parse_operations(script: _VerifiedScript, line_start: int, line_end: int) -> list[dict[str, object]]:
	operation_pattern = re.compile(r"^\s*(NFadeLm|NFadeL|Flashm|Flash)\s+(\d+),\s+(.+?)\s*$", re.IGNORECASE)
	operations = []
	for line in range(line_start, line_end + 1):
		match = operation_pattern.match(script.lines[line - 1])
		if match is None:
			continue
		operation, address_text, object_symbol = match.groups()
		operations.append(_operation_location(script, line, operation, int(address_text), object_symbol))
	return operations


def _address_candidate(location: dict[str, object], address: int, label: str, group: str, symbol: str | None = None) -> dict[str, object]:
	return {
		"symbol": symbol or location["symbol"],
		"address": address,
		"label": label,
		"group": group,
		"line": location["line"],
		"status": "candidate",
	}


def _vpx_script_evidence(
	definition: dict[str, object],
	script_path: Path | str | None = None,
	extraction: _VPXExtraction | None = None,
) -> dict[str, object]:
	script = _VerifiedScript(_resolve_script_path(script_path))

	# These are reviewed event locations, not inferred switch-number ranges. The
	# source symbol and exact source line are both checked before emission.
	switch_specs: list[tuple[int, list[tuple[int, str, str]]]] = [
		(9, [(291, "sw9_Hit", 'Sub sw9_Hit:vpmTimer.PulseSw 9:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(17, [(292, "sw17_Hit", 'Sub sw17_Hit:vpmTimer.PulseSw 17:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(18, [(293, "sw18_Hit", 'Sub sw18_Hit:Controller.Switch(18) = 1:ActiveBall.VelX = - 1:ActiveBall.VelY = 1:PlaySound SoundFX("fx_balldrop", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(19, [(295, "sw19_Hit", 'Sub sw19_Hit:vpmTimer.PulseSw 19:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(20, [(296, "sw20_Spin", 'Sub sw20_Spin:PlaySound "fx_spinner", 0, 1, -0.01:vpmTimer.PulseSw 20:End Sub')]),
		(21, [(297, "sw21_Spin", 'Sub sw21_Spin:PlaySound "fx_spinner", 0, 1, 0.01:vpmTimer.PulseSw 21:End Sub')]),
		(22, [(298, "sw22_Hit", 'Sub sw22_Hit:vpmTimer.PulseSw 22:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(23, [(263, "SMagnet_Hit", "Sub SMagnet_Hit"), (264, "Controller.Switch(23)", "    Controller.Switch(23) = 1")]),
		(24, [(300, "IMagnet_Hit", "Sub IMagnet_Hit:mIdolMag.AddBall ActiveBall:Controller.Switch(24) = 1:End Sub")]),
		(25, [(304, "Bumper4_Hit", 'Sub Bumper4_Hit:vpmTimer.PulseSw 25:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0,15, 0.15:End Sub')]),
		(26, [(306, "Bumper6_Hit", 'Sub Bumper6_Hit:vpmTimer.PulseSw 26:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0.05, 0.15:End Sub')]),
		(27, [(305, "Bumper5_Hit", 'Sub Bumper5_Hit:vpmTimer.PulseSw 27:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0.15, 0.15:End Sub')]),
		(28, [(308, "sw28_Hit", 'Sub sw28_Hit:sw28.DestroyBall:PlaySound "fx_hole-enter", 0, 1, -0.005:vpmTimer.PulseSwitch(28), 100, "AddToSkill":End Sub')]),
		(29, [(313, "sw29_Hit", "Sub sw29_Hit")]),
		(30, [(331, "sw30_Hit", 'Sub sw30_Hit:Controller.Switch(30) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(31, [(333, "sw31_Hit", "Sub sw31_Hit:Controller.Switch(31) = 1:End Sub")]),
		(32, [(335, "sw32_Hit", 'Sub sw32_Hit:vpmTimer.PulseSw 32:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub'), (336, "sw32b_Hit", 'Sub sw32b_Hit:vpmTimer.PulseSw 32:PlaySound SoundFX("fx_target", DOFTargets), 0, 1, pan(ActiveBall):End Sub')]),
		(33, [(337, "sw33_Hit", 'Sub sw33_Hit:Controller.Switch(33) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(34, [(339, "sw34_Hit", 'Sub sw34_Hit:Controller.Switch(34) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(35, [(341, "sw35_Hit", 'Sub sw35_Hit:Controller.Switch(35) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(36, [(343, "sw36_Hit", 'Sub sw36_Hit:Controller.Switch(36) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(38, [(345, "sw38_Hit", 'Sub sw38_Hit:Controller.Switch(38) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(39, [(347, "sw39_Hit", 'Sub sw39_Hit:Controller.Switch(39) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(40, [(349, "sw40_Hit", 'Sub sw40_Hit:Controller.Switch(40) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(41, [(385, "sw41_Hit", "Sub sw41_Hit"), (387, "Controller.Switch(41)", "        Controller.Switch(41) = 1")]),
		(42, [(371, "sw42_Hit", "Sub sw42_Hit"), (373, "Controller.Switch(42)", "        Controller.Switch(42) = 1")]),
		(43, [(378, "sw43_Hit", "Sub sw43_Hit"), (380, "Controller.Switch(43)", "        Controller.Switch(43) = 1")]),
		(47, [(352, "sw47_Hit", 'Sub sw47_Hit:Controller.Switch(47) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(48, [(354, "sw48_Hit", 'Sub sw48_Hit:Controller.Switch(48) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(49, [(357, "Bumper1_Hit", 'Sub Bumper1_Hit:vpmTimer.PulseSw 49:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0, 0.15:End Sub')]),
		(50, [(359, "Bumper3_Hit", 'Sub Bumper3_Hit:vpmTimer.PulseSw 50:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0.05, 0.15:End Sub')]),
		(51, [(358, "Bumper2_Hit", 'Sub Bumper2_Hit:vpmTimer.PulseSw 51:PlaySound SoundFX("fx_bumper", DOFContactors), 0, 1, 0.15, 0.15:End Sub')]),
		(52, [(407, "sw52_Hit", 'Sub sw52_Hit():bsVUK.AddBall Me:PlaySound "fx_kicker_enter", 0, 1, 0.01:End Sub')]),
		(53, [(413, "sw53_Hit", "Sub sw53_Hit:Controller.Switch(53) = 1:End Sub")]),
		(57, [(416, "sw57_Hit", 'Sub sw57_Hit:Controller.Switch(57) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(58, [(419, "sw58_Hit", 'Sub sw58_Hit:Controller.Switch(58) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(59, [(434, "LeftSlingShot_Slingshot", "Sub LeftSlingShot_Slingshot"), (439, "vpmTimer.PulseSw(59)", "    vpmTimer.PulseSw 59")]),
		(60, [(425, "sw60_Hit", 'Sub sw60_Hit:Controller.Switch(60) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(61, [(422, "sw61_Hit", 'Sub sw61_Hit:Controller.Switch(61) = 1:PlaySound "fx_sensor", 0, 1, pan(ActiveBall):End Sub')]),
		(62, [(452, "RightSlingShot_Slingshot", "Sub RightSlingShot_Slingshot"), (457, "vpmTimer.PulseSw(62)", "    vpmTimer.PulseSw 62")]),
	]
	switches = []
	for address, specs in switch_specs:
		for location in _locations(script, *specs):
			switches.append(_address_candidate(location, address, f"Embedded-table switch {address}", "pinmame.input.switch"))

	callback_specs = [
		(1, "SolCallBack(1)", 169, 'SolCallBack(1) = "SolTrough"'),
		(2, "SolCallBack(2)", 170, 'SolCallBack(2) = "Auto_Plunger"'),
		(3, "SolCallBack(3)", 171, 'SolCallBack(3) = "bsVUK.SolOut"'),
		(4, "SolCallBack(4)", 172, 'SolCallBack(4) = "vpmSolDiverter TempleDiv,1,"'),
		(5, "SolCallBack(5)", 173, 'SolCallBack(5) = "vpmSolDiverter LockDiverter,1,"'),
		(12, "SolCallBack(12)", 175, 'SolCallBack(12) = "bsSkill.SolOut"'),
		(13, "SolCallback(13)", 176, 'SolCallback(13) = "bsLock.SolOut"'),
		(20, "SolCallback(20)", 177, 'SolCallback(20) = "SolUpperMagnet"'),
		(21, "SolCallBack(21)", 178, 'SolCallBack(21) = "SolVReset"'),
		(22, "SolCallBack(22)", 179, 'SolCallBack(22) = "SetLamp 122,"'),
		(23, "SolCallBack(23)", 180, 'SolCallBack(23) = "SolPost"'),
		(24, "SolCallBack(24)", 181, 'SolCallBack(24) = "vpmsolsound SoundFX(""fx_knocker"",DOFKnocker),"'),
		(25, "SolCallBack(25)", 182, 'SolCallBack(25) = "SetLamp 125,"'),
		(26, "SolCallBack(26)", 183, 'SolCallBack(26) = "SetLamp 126,"'),
		(27, "SolCallBack(27)", 184, 'SolCallBack(27) = "SetLamp 127,"'),
		(28, "SolCallBack(28)", 185, 'SolCallBack(28) = "SetLamp 128,"'),
		(29, "SolCallBack(29)", 186, 'SolCallBack(29) = "SetLamp 129,"'),
		(30, "SolCallBack(30)", 187, 'SolCallBack(30) = "SetLamp 130,"'),
		(31, "SolCallBack(31)", 188, 'SolCallBack(31) = "SetLamp 131,"'),
		(32, "SolCallBack(32)", 189, 'SolCallBack(32) = "SetLamp 132,"'),
	]
	flasher_operations = _parse_operations(script, 649, 664)
	flasher_by_address: dict[int, list[dict[str, object]]] = {}
	for operation in flasher_operations:
		flasher_by_address.setdefault(int(operation["address"]), []).append(operation)
	expected_flasher_addresses = {122, 125, 126, 127, 128, 129, 130, 131, 132}
	if set(flasher_by_address) != expected_flasher_addresses:
		raise ValueError(f"Unexpected exact-table flasher mappings: {sorted(flasher_by_address)}")
	outputs = []
	for address, symbol, line, expected_text in callback_specs:
		location = script.location(line, symbol, expected_text)
		outputs.append(_address_candidate(location, address, f"Embedded-table Q{address}", "pinmame.output.solenoid"))
	outputs.append(_address_candidate(script.location(98, "mIdolMag.Solenoid", "        .Solenoid = 19"), 19, "Embedded-table Q19", "pinmame.output.solenoid"))

	lamp_operations = _parse_operations(script, 540, 645)
	if {int(operation["address"]) for operation in lamp_operations} != set(range(1, 79)):
		raise ValueError("The exact-table UpdateLamps section no longer exposes exactly lamps 1-78")
	outputs.extend(
		_address_candidate(operation, int(operation["address"]), f"Embedded-table lamp {operation['address']}", "pinmame.output.lamp")
		for operation in lamp_operations
	)
	outputs.extend(
		_address_candidate(location, 0, "Embedded-table general illumination", "pinmame.output.gi", symbol="GIUpdate")
		for location in _locations(
			script,
			(1004, "GICallback", 'Set GICallback = GetRef("GIUpdate")'),
			(1006, "GIUpdate", "Sub GIUpdate(no, Enabled)"),
			(1007, "aGiLights", "    For each x in aGiLights"),
			(1008, "x.State", "        x.State = ABS(Enabled)"),
		)
	)

	mechanisms = [
		{"kind": "trough_and_shooter", "locations": _locations(script,
			(87, "bsTrough", "    Set bsTrough = New cvpmBallStack"),
			(89, "bsTrough.InitSw", "        .InitSw 0, 14, 13, 12, 11, 0, 0, 0"),
			(90, "bsTrough.InitKick", "        .InitKick BallRelease, 100, 3"),
			(123, "bsVUK", "    Set bsVUK = new cvpmBallStack"),
			(125, "bsVUK.InitSw", "        .InitSw 0, 52, 0, 0, 0, 0, 0, 0"),
			(126, "bsVUK.InitKick", "        .InitKick sw52, 0, 36"),
			(134, "plungerIM", "    Set plungerIM = New cvpmImpulseP"),
			(136, "plungerIM.InitImpulseP", "        .InitImpulseP swPlunger, IMPowerSetting, IMTime"),
			(140, "plungerIM.CreateEvents", '        .CreateEvents "plungerIM"'),
			(169, "SolCallBack(1)", 'SolCallBack(1) = "SolTrough"'),
			(236, "Auto_Plunger", "Sub Auto_Plunger(Enabled)"),
			(252, "SolTrough", "Sub SolTrough(Enabled)"),
			(255, "vpmTimer.PulseSw(15)", "        vpmTimer.PulseSw 15"),
		), "status": "candidate"},
		{"kind": "vari_target", "locations": _locations(script,
			(178, "SolCallBack(21)", 'SolCallBack(21) = "SolVReset"'),
			(242, "SolVReset", "Sub SolVReset(Enabled)"),
			(244, "VariTimerDown.Enabled", "        VariTimerDown.Enabled = 1"),
			(365, "aVariPos_Hit", "Sub aVariPos_Hit(idx)"),
			(367, "VariTarget.RotY", "        VariTarget.RotY = 14 - idx"),
			(371, "sw42_Hit", "Sub sw42_Hit"),
			(373, "Controller.Switch(42)", "        Controller.Switch(42) = 1"),
			(378, "sw43_Hit", "Sub sw43_Hit"),
			(380, "Controller.Switch(43)", "        Controller.Switch(43) = 1"),
			(385, "sw41_Hit", "Sub sw41_Hit"),
			(387, "Controller.Switch(41)", "        Controller.Switch(41) = 1"),
			(392, "VariTimerDown_Timer", "Sub VariTimerDown_Timer"),
			(394, "Controller.Switch(41)", "    If VariTarget.RotY = -5 Then Controller.Switch(41) = 0"),
			(395, "Controller.Switch(43)", "    If VariTarget.RotY = 5 Then Controller.Switch(43) = 0"),
			(398, "Controller.Switch(42)", "        Controller.Switch(42) = 0"),
		), "status": "candidate"},
		{"kind": "magnets", "locations": _locations(script,
			(95, "mIdolMag", "    Set mIdolMag = New cvpmMagnet"),
			(97, "mIdolMag.InitMagnet", "        .InitMagnet IMagnet, 50"),
			(102, "mShrunkenMag", "    Set mShrunkenMag = New cvpmMagnet"),
			(104, "mShrunkenMag.InitMagnet", "        .InitMagnet SMagnet, 70"),
			(263, "SMagnet_Hit", "Sub SMagnet_Hit"),
			(264, "Controller.Switch(23)", "    Controller.Switch(23) = 1"),
			(268, "SMagnet_unHit", "Sub SMagnet_unHit"),
			(269, "Controller.Switch(23)", "    Controller.Switch(23) = 0"),
			(273, "SolUpperMagnet", "Sub SolUpperMagnet(Enabled)"),
			(276, "mShrunkenMag.MagnetOn", "        mShrunkenMag.MagnetOn = 1"),
			(278, "mShrunkenMag.MagnetOn", "        mShrunkenMag.MagnetOn = 0"),
			(300, "IMagnet_Hit", "Sub IMagnet_Hit:mIdolMag.AddBall ActiveBall:Controller.Switch(24) = 1:End Sub"),
			(301, "IMagnet_unHit", "Sub IMagnet_unHit:mIdolMag.RemoveBall ActiveBall:Controller.Switch(24) = 0:End Sub"),
		), "status": "candidate"},
		{"kind": "diverters_and_lock", "locations": _locations(script,
			(108, "bsLock", "    Set bsLock = New cvpmBallStack"),
			(110, "bsLock.InitSw", "        .InitSw 0, 46, 45, 44, 0, 0, 0, 0"),
			(111, "bsLock.InitKick", "        .InitKick Lock, 0, 36"),
			(172, "SolCallBack(4)", 'SolCallBack(4) = "vpmSolDiverter TempleDiv,1,"'),
			(173, "SolCallBack(5)", 'SolCallBack(5) = "vpmSolDiverter LockDiverter,1,"'),
			(176, "SolCallback(13)", 'SolCallback(13) = "bsLock.SolOut"'),
			(351, "Lock_Hit", 'Sub Lock_Hit:bsLock.AddBall Me:PlaySound "fx_kicker_enter", 0, 1, 0.01:End Sub'),
		), "status": "candidate"},
		{"kind": "render_helper_exclusion", "locations": _locations(script,
			(651, "f25", "    NFadeLm 125, f25"),
			(652, "f25a", "    Flashm 125, f25a"),
			(653, "f25b", "    Flash 125, f25b"),
			(659, "f30", "    NFadeLm 130, f30"),
			(660, "f30a", "    Flashm 130, f30a"),
			(661, "f30c", "    Flashm 130, f30c"),
			(662, "f30b", "    Flash 130, f30b"),
			(771, "Flashm", "Sub Flashm(nr, object) 'multiple flashers, it doesn't change anything, it just follows the main flasher"),
		), "status": "candidate"},
	]
	recreation_notes = [
		{"text": "Q24's exact-table callback invokes the sound routine vpmsolsound.", "locations": _locations(script, (181, "SolCallBack(24)", 'SolCallBack(24) = "vpmsolsound SoundFX(""fx_knocker"",DOFKnocker),"')), "status": "candidate"},
		{"text": "The exact script declares Flashm as a multiple-flasher follower and uses it for f25a, f30a, and f30c.", "locations": _locations(script,
			(652, "f25a", "    Flashm 125, f25a"),
			(660, "f30a", "    Flashm 130, f30a"),
			(661, "f30c", "    Flashm 130, f30c"),
			(771, "Flashm", "Sub Flashm(nr, object) 'multiple flashers, it doesn't change anything, it just follows the main flasher"),
		), "status": "candidate"},
	]
	mechanism_records = []
	for mechanism in mechanisms:
		for location in mechanism["locations"]:
			mechanism_records.append({"kind": mechanism["kind"], "line": location["line"], "raw": location["source_text"], "status": "candidate"})
	recreation_records = []
	for note in recreation_notes:
		for location in note["locations"]:
			recreation_records.append({"text": location["source_text"], "line_start": location["line"], "line_end": location["line"], "status": "candidate"})
	state_records = []
	for label, specs in (
		("vari-target boot switch initialization", ((70, "Controller.Switch(42)", "        .Switch(42) = 1"), (71, "Controller.Switch(43)", "        .Switch(43) = 1"))),
		("four-ball trough stack initialization", ((89, "bsTrough.InitSw", "        .InitSw 0, 14, 13, 12, 11, 0, 0, 0"),)),
	):
		for location in _locations(script, *specs):
			state_records.append({"label": label, "line": location["line"], "raw": location["source_text"]})
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "ripleys-vpx-spatial-review", "version": 3},
		"source": {"kind": "vpx_script", "repository": "external:pinmame-vpx-sources/stern/ripley-s-believe-it-or-not-2004", "revision": TABLE_CONTENT_REVISION, "path": "extracted-vpxtool/script.vbs", "sha256": SCRIPT_SHA256, "license": "NOASSERTION", "attribution": "JPSalas table authors and local user-authorized source; exact VPX SHA-256 is " + TABLE_VPX_SHA256 + "; retained extraction manifest SHA-256 is " + EXTRACTION_MANIFEST_SHA256, "quality": "validated", "encoding": "windows-1252"},
		"driver_ids": ["ripleys"],
		"machine_ids": [definition["machine"]["id"]],
		"switches": switches,
		"outputs": outputs,
		"states": state_records,
		"mechanisms": mechanism_records,
		"recreation_notes": recreation_records,
	}
	return evidence


def refuse_if_canonical_definition_exists(path: Path) -> None:
	if path.exists():
		raise RuntimeError(f"Refusing to regenerate canonical author-ready definition: {path}")


def generate(root: Path = ROOT) -> None:
	source_root = _resolve_source_root()
	_verify_retained_table(source_root)
	resolved_script_path = _resolve_script_path()
	extraction = _VPXExtraction(_resolve_extraction_path())
	partial_path = root / "machines/partial/stern/ripley-s-believe-it-or-not-2004.json"
	author_ready_path = root / "machines/author-ready/stern/ripley-s-believe-it-or-not-2004.json"
	refuse_if_canonical_definition_exists(author_ready_path)
	definition = build()
	definition["conflicts"] = CONFLICTS
	apply_spatial(definition, extraction)
	_assert_contract(definition)
	definition = fail_closed_spatial_partial(definition)
	write_json(partial_path, definition)
	write_json(root / "reports/spatial/stern/ripley-s-believe-it-or-not-2004.json", _report(definition, extraction))
	write_json(root / "evidence/vpx/ripleys-exact-table-1.0.3.json", _vpx_script_evidence(definition, resolved_script_path, extraction))
	knowledge = fail_closed_spatial_knowledge(definition["machine"]["id"], KNOWLEDGE)
	write_text(root / "knowledge/stern/ripley-s-believe-it-or-not-2004.md", knowledge.rstrip() + "\n\n" + SPATIAL_KNOWLEDGE_APPENDIX.rstrip() + "\n")


def main(argv: Sequence[str] | None = None) -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository checkout to update; defaults to this checkout.")
	args = parser.parse_args(argv)
	generate(root=args.repository_root)


if __name__ == "__main__":
	main()
