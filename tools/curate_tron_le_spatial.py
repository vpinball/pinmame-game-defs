"""Promote the exact TRON: Legacy Limited Edition table with reviewed spatial evidence."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from curate_tron import (  # noqa: E402
	CORE_SOURCE,
	LE_KNOWLEDGE,
	LE_Q19_Q25_CONFLICT,
	MANUAL_SOURCE,
	VPX_SOURCE,
	build,
)
from pinmame_game_defs.jsonio import content_sha256, file_sha256, load_json, write_json, write_text  # noqa: E402


PARTIAL_PATH = ROOT / "machines/partial/stern/tron-legacy-limited-edition-2011.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/tron-legacy-limited-edition-2011.json"
KNOWLEDGE_PATH = ROOT / "knowledge/stern/tron-legacy-limited-edition-2011.md"
SPATIAL_EVIDENCE_PATH = ROOT / "evidence/vpx/tron-legacy-limited-edition-2011-v11-spatial-candidates.json"

TABLE_SOURCE = "vpx-table.tron-legacy-le-v11"
TABLE_SHA256 = "56ad2f5318c33dbc12f3aa2515a41d819eb8b95b2ffcd94ebe1044cec4281ae5"
TABLE_SIZE = 133521408
TABLE_BOUNDS = {"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2115.0}
SPATIAL_EVIDENCE_SHA256 = "318297fb178098929d62078075f891ee301067cff58ad778f683b577f83b8ff4"
SPATIAL_EVIDENCE_VPXTOOL_VERSION = "vpxtool git:v0.33.3"
TABLE_URI = (
	"external:pinmame-vpx-sources/stern/tron-legacy-limited-edition-2011/"
	"VR Room Tron Legacy (Limited Edition) (Stern 2011) V11.vpx"
)

DIRECT_SOURCES = (MANUAL_SOURCE, VPX_SOURCE, TABLE_SOURCE)
MANUAL_ONLY_SOURCES = (MANUAL_SOURCE,)


def _provenance(*source_refs: str) -> dict[str, object]:
	return {"status": "validated", "source_refs": list(source_refs)}


def _append_note(device: dict[str, Any], note: str) -> None:
	physical = device.setdefault("physical", {})
	existing = str(physical.get("notes", "")).strip()
	physical["notes"] = f"{existing} {note}".strip()


def _located(
	device: dict[str, Any],
	role: str,
	positions: list[tuple[float, float]],
	source_refs: tuple[str, ...],
) -> None:
	placements = []
	for index, (x, y) in enumerate(positions, start=1):
		suffix = f".{index}" if len(positions) > 1 else ""
		placements.append(
			{
				"id": f"{device['id']}.{role}{suffix}",
				"role": role,
				"space": "playfield",
				"x": x,
				"y": y,
				"provenance": _provenance(*source_refs),
			}
		)
	device["spatial"] = {"status": "validated", "placements": placements}


def _not_applicable(device: dict[str, Any], reason: str, *source_refs: str) -> None:
	device["spatial"] = {
		"status": "not_applicable",
		"reason": reason,
		"provenance": _provenance(*source_refs),
	}


class CandidateGeometry:
	"""Resolve only direct, retained vpxtool candidate points."""

	def __init__(self, path: Path) -> None:
		if not path.is_file():
			raise ValueError(f"TRON LE spatial candidate report does not exist: {path}")
		if file_sha256(path) != SPATIAL_EVIDENCE_SHA256:
			raise ValueError(f"TRON LE spatial candidate report SHA-256 does not match the retained report: {path}")
		evidence = load_json(path)
		if evidence.get("format") != "pinmame-vpx-spatial-candidates":
			raise ValueError(f"Unexpected spatial candidate format in {path}")
		if evidence.get("version") != 2:
			raise ValueError("TRON LE candidates must use spatial candidate report version 2")
		if evidence.get("coordinate_space") != "playfield":
			raise ValueError("TRON LE candidates must use playfield coordinates")
		source = evidence.get("source")
		if not isinstance(source, dict):
			raise ValueError("TRON LE candidate report source metadata is missing")
		if source.get("vpxtool_version") != SPATIAL_EVIDENCE_VPXTOOL_VERSION:
			raise ValueError("TRON LE candidate report vpxtool version does not match the retained extraction")
		if source.get("vpx_sha256") != TABLE_SHA256:
			raise ValueError("TRON LE candidate source hash does not match the retained exact table")
		if source.get("vpx_size") != TABLE_SIZE:
			raise ValueError("TRON LE candidate source size does not match the retained exact table")
		if evidence.get("bounds") != TABLE_BOUNDS:
			raise ValueError("TRON LE candidate bounds do not match the retained exact table")
		objects = evidence.get("objects")
		if not isinstance(objects, list) or not objects:
			raise ValueError("TRON LE candidate report has no objects")
		self.points: dict[tuple[str, str], tuple[float, float]] = {}
		self.records: dict[tuple[str, str], dict[str, Any]] = {}
		for item in objects:
			name = item.get("name")
			object_type = item.get("type")
			if not isinstance(name, str) or not isinstance(object_type, str):
				raise ValueError(f"Invalid spatial candidate record: {item!r}")
			key = (object_type.casefold(), name.casefold())
			if key in self.points:
				raise ValueError(f"Duplicate or invalid spatial candidate name: {name!r}")
			self.points[key] = (round(float(item["x"]), 6), round(float(item["y"]), 6))
			self.records[key] = item

	def point(self, name: str, object_type: str | None = None) -> tuple[float, float]:
		matches = [key for key in self.points if key[1] == name.casefold() and (object_type is None or key[0] == object_type.casefold())]
		if len(matches) != 1:
			qualifier = f"{object_type}.{name}" if object_type else name
			raise ValueError(f"Missing or ambiguous exact TRON LE candidate point {qualifier!r}")
		return self.points[matches[0]]

	def names(self, prefix: str, pattern: str | None = None, object_type: str | None = None) -> list[str]:
		selected = [name for object_name, name in ((key[0], key[1]) for key in self.points) if name.startswith(prefix.casefold()) and (object_type is None or object_name == object_type.casefold())]
		if pattern is not None:
			selected = [name for name in selected if re.fullmatch(pattern, name, re.IGNORECASE)]
		return sorted(selected, key=_natural_key)


def _natural_key(value: str) -> tuple[object, ...]:
	return tuple(int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", value))


def _average(points: list[tuple[float, float]]) -> tuple[float, float]:
	return (
		round(sum(point[0] for point in points) / len(points), 6),
		round(sum(point[1] for point in points) / len(points), 6),
	)


def _point(geometry: CandidateGeometry, name: str) -> list[tuple[float, float]]:
	return [geometry.point(name)]


def _typed_point(geometry: CandidateGeometry, object_type: str, name: str) -> list[tuple[float, float]]:
	return [geometry.point(name, object_type)]


def _points(geometry: CandidateGeometry, names: list[str]) -> list[tuple[float, float]]:
	return [geometry.point(name) for name in names]


def _typed_points(geometry: CandidateGeometry, object_type: str, names: list[str]) -> list[tuple[float, float]]:
	return [geometry.point(name, object_type) for name in names]


def _manual_projection(x: float, y: float) -> list[tuple[float, float]]:
	return [(round(x, 6), round(y, 6))]


def _source_record() -> dict[str, object]:
	return {
		"id": TABLE_SOURCE,
		"kind": "vpx_table",
		"uri": TABLE_URI,
		"sha256": TABLE_SHA256,
		"known_working": True,
		"original_filename": "VR Room Tron Legacy (Limited Edition) (Stern 2011) V11.vpx",
		"locator": (
			"Exact local LE table selected from the primary Visual Pinball/Tables folder after vpxtool identity check: "
			"Table Name Tron Legacy LE, IPDB 5707, romname trn_174h; copied unchanged and extracted "
			f"with vpxtool git:v0.33.3. Normalized candidate report SHA-256 {SPATIAL_EVIDENCE_SHA256}."
		),
		"license": "NOASSERTION",
		"attribution": "Table authors credited in the retained VPX; local evidence acquisition",
	}


def _input_positions(geometry: CandidateGeometry) -> dict[int, list[tuple[float, float]]]:
	positions: dict[int, list[tuple[float, float]]] = {
		1: _typed_point(geometry, "Primitive", "sw1p"),
		2: _typed_point(geometry, "Primitive", "sw2p"),
		3: _typed_point(geometry, "Primitive", "sw3p"),
		4: _typed_point(geometry, "Primitive", "sw4p"),
		7: _typed_point(geometry, "Primitive", "sw7p"),
		8: _typed_point(geometry, "Primitive", "sw8p"),
		11: _point(geometry, "sw11"),
		12: _point(geometry, "sw12"),
		13: _typed_point(geometry, "Primitive", "sw13p"),
		14: _point(geometry, "sw14"),
		18: _manual_projection(0.612000, 0.850000),
		19: _manual_projection(0.680000, 0.846000),
		20: _manual_projection(0.752000, 0.841000),
		21: _point(geometry, "BallRelease"),
		22: _manual_projection(0.790000, 0.855000),
		23: _point(geometry, "ShooterLane"),
		24: _point(geometry, "sw24"),
		25: _point(geometry, "sw25"),
		26: _typed_point(geometry, "Wall", "LeftSlingShot"),
		27: _typed_point(geometry, "Wall", "RightSlingShot"),
		28: _point(geometry, "sw28"),
		29: _point(geometry, "sw29"),
		30: _point(geometry, "Bumper2b"),
		31: _point(geometry, "Bumper1b"),
		32: _point(geometry, "Bumper3b"),
		34: _point(geometry, "Laneexit"),
		35: _point(geometry, "sw35"),
		36: _point(geometry, "sw36"),
		37: _point(geometry, "sw37"),
		38: _point(geometry, "sw38"),
		39: _point(geometry, "sw39"),
		41: _point(geometry, "Disc1Trigger"),
		43: _point(geometry, "sw43"),
		44: _point(geometry, "sw44"),
		46: _point(geometry, "sw46"),
		48: _typed_point(geometry, "Primitive", "sw48p"),
		49: _typed_point(geometry, "Primitive", "SW49P"),
		50: _typed_point(geometry, "Primitive", "SW50P"),
		51: _typed_point(geometry, "Primitive", "SW51P"),
		52: _typed_point(geometry, "Primitive", "MotorBank"),
		53: _typed_point(geometry, "Primitive", "MotorBank"),
		54: _typed_point(geometry, "Primitive", "recognizer"),
		55: _typed_point(geometry, "Primitive", "recognizer"),
		56: _typed_point(geometry, "Primitive", "recognizer"),
	}
	return positions


def _output_positions(geometry: CandidateGeometry) -> dict[int, list[tuple[float, float]]]:
	# The reset acts on the four exact target-face Primitive centers.
	targets = _typed_points(geometry, "Primitive", ["sw1p", "sw2p", "sw3p", "sw4p"])
	return {
		1: _point(geometry, "BallRelease"),
		2: _point(geometry, "Plunger"),
		3: [_average(targets)],
		4: _point(geometry, "sw11"),
		5: _typed_point(geometry, "Primitive", "Disc1"),
		6: _typed_point(geometry, "Primitive", "MotorBank"),
		7: _typed_point(geometry, "Wall", "UpPost"),
		9: _point(geometry, "Bumper2b"),
		10: _point(geometry, "Bumper1b"),
		11: _point(geometry, "Bumper3b"),
		12: _point(geometry, "LeftFlipper1"),
		13: _typed_point(geometry, "Wall", "LeftSlingShot"),
		14: _typed_point(geometry, "Wall", "RightSlingShot"),
		15: _point(geometry, "LeftFlipper"),
		16: _point(geometry, "RightFlipper"),
		17: _point(geometry, "F117"),
		18: _point(geometry, "Flasher7"),
		19: _points(geometry, ["Flasher5", "Flasher6"]),
		20: _manual_projection(0.082000, 0.885000),
		21: _point(geometry, "Lanelight"),
		22: _typed_point(geometry, "Primitive", "Disc1"),
		23: _typed_point(geometry, "Primitive", "recognizer"),
		25: _points(geometry, ["Flasher1", "Flasher2"]),
		26: _point(geometry, "F126"),
		27: _point(geometry, "F127"),
		28: _points(geometry, ["Flasher3a", "Flasher4a"]),
		29: _point(geometry, "f129"),
		30: _typed_point(geometry, "Primitive", "Disc1"),
		31: _points(geometry, ["f131a", "f131b"]),
		32: _points(geometry, ["f132a", "f132b"]),
	}


def _apply_input_spatial(definition: dict[str, Any], geometry: CandidateGeometry) -> None:
	positions = _input_positions(geometry)
	for device in definition["inputs"]:
		address = int(device["binding"]["device"])
		if device["binding"]["group"] == "pinmame.input.dip":
			_not_applicable(device, "dip_switch", MANUAL_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif address in positions:
			refs = DIRECT_SOURCES
			if address in {18, 19, 20, 22}:
				refs = MANUAL_ONLY_SOURCES
			elif address in {26, 27}:
				refs = (MANUAL_SOURCE, TABLE_SOURCE)
			_located(device, "sensor", positions[address], refs)
			if address in {1, 2, 3, 4}:
				_append_note(device, f"The exact extracted Primitive.sw{address}p center is the target-face anchor; the under-playfield contact remains a distinct physical device.")
			elif address in {7, 8, 13}:
				_append_note(device, f"The exact extracted Primitive.sw{address}p center is the target-face anchor; the under-playfield contact remains a distinct physical device.")
			elif address in {18, 19, 20, 21, 22}:
				_append_note(device, "The official LE switch map places these contacts in the four-ball trough/jam assembly. The exact VPX exposes the BallRelease kicker and shooter lane but not individual trough contact centers; 18-20 and jam opto 22 are disclosed manual-map regional projections, while switch 21 uses the exact BallRelease anchor.")
			elif address in {26, 27}:
				wall_name = "LeftSlingShot" if address == 26 else "RightSlingShot"
				_append_note(device, f"The switch is implicit in the exact extracted Wall.{wall_name} collision wall. Its centroid is the manual-confirmed assembly anchor, not an invented internal leaf-contact center.")
			elif address in {49, 50, 51}:
				_append_note(device, f"The exact extracted Primitive.SW{address}P center is the recognizer target-face anchor; the under-playfield microswitch remains a separate physical contact behind the face.")
			elif address in {52, 53}:
				_append_note(device, "The exact extracted Primitive.MotorBank center is the canonical moving-bank assembly anchor; up/down contacts remain separate controller sensors.")
			elif address in {54, 55, 56}:
				_append_note(device, "The exact extracted Primitive.recognizer center is the moving Recognizer assembly anchor; the three narrow internal position contacts remain distinct controller sensors.")
			elif address == 48:
				_append_note(device, "The exact extracted Primitive.sw48p center is the ZUSE target-face anchor; the spinner contact remains a distinct physical device.")
		else:
			roles = [str(role) for role in device.get("roles", [])]
			if any(role.startswith(("cabinet.", "service.", "flipper.")) for role in roles):
				_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
			else:
				raise ValueError(f"TRON LE input {device['id']} has no reviewed spatial disposition")

	for address in (81, 83):
		device = next(device for device in definition["inputs"] if int(device["binding"]["device"]) == address)
		device["roles"] = ["flipper.lower.right.eos" if address == 81 else "flipper.lower.left.eos"]
		flipper = "RightFlipper" if address == 81 else "LeftFlipper"
		_located(device, "sensor", _point(geometry, flipper), DIRECT_SOURCES)
		_append_note(device, "The normally-closed EOS contact is implicit in the exact lower-flipper assembly; this is the assembly center, not a claim that the leaf stack is on the playfield surface.")


def _apply_output_spatial(definition: dict[str, Any], geometry: CandidateGeometry) -> None:
	positions = _output_positions(geometry)
	for device in definition["outputs"]:
		group = str(device["binding"]["group"])
		address = int(device["binding"]["device"])
		kind = str(device["kind"])
		if kind == "virtual":
			_not_applicable(device, "virtual", CORE_SOURCE, VPX_SOURCE)
		elif device["availability"] == "unused":
			_not_applicable(device, "unused", MANUAL_SOURCE)
		elif group == "pinmame.output.gi" and address == 0:
			gi_names = [f"GI_{number}" for number in range(1, 33)] + ["GI_35", "GI_66", "GI_67"]
			gi_points = _points(geometry, gi_names)
			_located(device, "emitter", gi_points, DIRECT_SOURCES)
			device.setdefault("physical", {})["quantity"] = 35
			_append_note(device, "The exact LE VPX exposes 35 direct GI authoring-light objects: GI_1-GI_32, GI_35, GI_66, and GI_67. Render-only GIWhite/gibleed/Reflect/MaterialColor objects are intentionally excluded.")
		elif group == "pinmame.output.solenoid" and address == 8:
			device["roles"] = ["cabinet.shaker"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
			_append_note(device, "The optional shaker is a cabinet motor, outside normalized playfield space.")
		elif group == "pinmame.output.solenoid" and address == 24:
			device["roles"] = ["cabinet.coin-meter"]
			_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
			_append_note(device, "The optional coin meter is a cabinet/service device, outside normalized playfield space.")
		elif group == "pinmame.output.lamp" and 1 <= address <= 80 and device["availability"] == "used":
			if address in {65, 66}:
				device["roles"] = ["cabinet.start" if address == 65 else "cabinet.tournament"]
				_not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
				_append_note(device, "The LE manual identifies this as a cabinet button lamp; it is not a playfield emitter.")
			else:
				_located(device, "emitter", _point(geometry, f"l{address}"), DIRECT_SOURCES)
				device.setdefault("physical", {})["quantity"] = 1
		elif group == "pinmame.output.lamp" and 101 <= address <= 106 and device["availability"] == "used":
			prefix = "Rampenlicht1" if address in {104, 105, 106} else "Rampenlicht2"
			pattern = rf"{re.escape(prefix)}(?:a\d+)?"
			names = geometry.names(prefix, pattern, "Light")
			_located(device, "emitter", _points(geometry, names), DIRECT_SOURCES)
			device.setdefault("physical", {})["quantity"] = len(names)
			_append_note(device, "This public address is one color channel of the LE tricolor ramp-light assembly. The exact table supplies the shared RGB-light path; do not create separate geometry for each B/G/R channel.")
		elif group == "pinmame.output.solenoid" and address in positions:
			role = "emitter" if kind == "flasher" else "effect"
			refs = DIRECT_SOURCES
			if address == 20:
				refs = MANUAL_ONLY_SOURCES
			_located(device, role, positions[address], refs)
			if kind == "flasher":
				device.setdefault("physical", {})["quantity"] = len(positions[address])
			if address == 3:
				_append_note(device, "The reset coil acts on the complete four-target bank. Its point is the centroid of the four exact target faces, not a claim that the under-playfield coil sits on the playfield surface.")
			elif address in {5, 22, 30}:
				_append_note(device, "The exact extracted Primitive.Disc1 center is the rotating disc assembly anchor; output-specific motor, direction, and relay semantics remain separate devices.")
			elif address == 6:
				_append_note(device, "The actuator belongs to the moving Recognizer target-bank assembly. The exact extracted Primitive.MotorBank center is retained as its shared assembly anchor and internal motor/relay components are not falsely separated.")
			elif address == 7:
				_append_note(device, "The exact extracted Wall.UpPost centroid is the orbit-post assembly anchor; the table models one physical post with collision geometry, not multiple physical posts.")
			elif address == 23:
				_append_note(device, "The actuator belongs to the moving Recognizer toy. The exact extracted Primitive.recognizer center is retained as its shared assembly anchor and internal motor/relay components are not falsely separated.")
			elif address in {13, 14}:
				wall_name = "LeftSlingShot" if address == 13 else "RightSlingShot"
				_append_note(device, f"The exact extracted Wall.{wall_name} centroid is the manual-confirmed coil assembly anchor, not an invented internal coil center.")
			elif address in {19, 25, 28, 31, 32}:
				_append_note(device, "Multiplicity follows the official LE flasher chart. The exact VPX exposes the listed direct flasher anchors; no render-only helper lights are promoted.")
			if address in {19, 25}:
				_append_note(device, LE_Q19_Q25_CONFLICT)
			elif address == 20:
				_append_note(device, "The exact working script drives Linkerflasher for this bottom-arch output, but that light is outside normalized playfield bounds in the VR table. The manual LE flasher map supplies this disclosed left bottom-arch projection.")
			elif address == 21:
				_append_note(device, "The exact working script drives the in-bounds Lanelight plus an outside-bounds Rechterflasher. This placement retains the in-bounds exact light; the manual confirms the paired cabinet/arch assembly.")
		else:
			raise ValueError(f"TRON LE output {group} {address} ({kind}) has no reviewed spatial disposition")


def apply_spatial(definition: dict[str, Any]) -> None:
	if any("spatial" in device for collection in (definition["inputs"], definition["outputs"]) for device in collection):
		raise ValueError("TRON LE spatial curation requires an unspatialized base definition")
	geometry = CandidateGeometry(SPATIAL_EVIDENCE_PATH)
	_apply_input_spatial(definition, geometry)
	_apply_output_spatial(definition, geometry)


SPATIAL_KNOWLEDGE = LE_KNOWLEDGE.rstrip() + f"""

## Spatial coordinate model

Every normalized playfield placement uses the exact selected LE VPX's 952 by 2115 playfield frame: x=0 is left, x=1 is right, y=0 is the rear/backglass end, and y=1 is the front/apron end. Direct object centers come from the retained `vpxtool git:v0.33.3` extraction and candidate report. The working LE script establishes controller semantics before any object is promoted. The official Stern manual remains physical truth for installed quantities, cabinet/back-panel locations, and assembly identity.

The exact LE table exposes direct points for all ordinary lamps 1-40, 42, 43, and 45-64, 35 GI authoring lights, both 23/29-point ramp RGB paths, direct flasher objects, switches, bumpers, flippers, kickers, and visible target faces. Render-only helpers (`lNa` overlays, reflective/material objects, `GIWhite`, `gibleed`, and similar) are not promoted. Lamp addresses 65/66 are cabinet button lamps; unused matrix lamps and absent LE dedicated contacts are explicit non-applicable records.

The official LE switch map proves four individual trough contacts and a jam opto, while this exact VPX models the trough as one BallRelease/kicker assembly. Switches 18-20 and 22 therefore retain manual-map regional projections with disclosure; switch 21 uses the exact BallRelease anchor. Slingshot contacts/coils, recognizer target-bank contacts, motorized Recognizer endpoints, the three internal Recognizer-toy contacts, EOS leaves, and target-bank reset are likewise distinct controller devices with assembly anchors where the VPX does not expose an internal component center. No helper/render object is used as a physical switch or coil.

{LE_Q19_Q25_CONFLICT} Outputs 20/21 retain their distinct left/right bottom-arch semantics; 20 is manual-only because `Linkerflasher` is outside the table frame, while 21 keeps exact in-bounds `Lanelight` and documents the outside-bounds companion. GI output 0 is the aggregate physical GI circuit and has 35 exact direct emitters, not a second compatibility lamp. RGB outputs 101-103 and 104-106 are independent blue/green/red controller channels that co-locate on one physical 29-module right-ramp or 23-module left-ramp RGB emitter string respectively; each channel repeats the shared coordinate set for channel addressability and is not a separate physical string.

The selected exact table is retained at `{TABLE_URI}` with VPX SHA-256 `{TABLE_SHA256}`. The deterministic candidate report is `evidence/vpx/tron-legacy-limited-edition-2011-v11-spatial-candidates.json` with SHA-256 `{SPATIAL_EVIDENCE_SHA256}`. Rejected local alternatives include the explicitly re-themed `TRON Classic (Original 2018) Mod v1.02.vpx`; Pro/non-LE candidates were not promoted.
"""


def _write_generated_json(path: Path, value: dict[str, Any]) -> None:
	if path.exists():
		try:
			current = load_json(path)
		except (OSError, ValueError) as error:
			raise RuntimeError(f"Refusing to clobber non-JSON generated artifact {path}: {error}") from error
		if current == value:
			return
		raise RuntimeError(f"Refusing to overwrite existing generated artifact {path}; verify the source inputs, remove this generated output, and rerun tools/curate_tron.py")
	write_json(path, value)


def _write_generated_text(path: Path, value: str) -> None:
	if path.exists():
		try:
			current = path.read_text(encoding="utf-8")
		except OSError as error:
			raise RuntimeError(f"Refusing to clobber unreadable generated artifact {path}: {error}") from error
		if current == value:
			return
		raise RuntimeError(f"Refusing to overwrite existing generated artifact {path}; verify the source inputs, remove this generated output, and rerun tools/curate_tron.py")
	write_text(path, value)


def promote() -> None:
	if PARTIAL_PATH.exists():
		raise RuntimeError(f"Refusing to promote TRON LE while the stale partial artifact exists: {PARTIAL_PATH}")
	definition = build(True)
	definition["sources"].append(_source_record())
	definition["schema_version"] = 2
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(definition)
	_write_generated_json(AUTHOR_READY_PATH, definition)
	_write_generated_text(KNOWLEDGE_PATH, SPATIAL_KNOWLEDGE.rstrip() + "\n")


if __name__ == "__main__":
	promote()
	print(f"wrote {AUTHOR_READY_PATH.relative_to(ROOT)}")
	print(f"definition_sha256={content_sha256(load_json(AUTHOR_READY_PATH))}")
