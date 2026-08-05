"""Derive the fail-closed Transformers Pro spatial-review evidence."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
	sys.path.insert(0, str(SOURCE_ROOT))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json
from pinmame_game_defs.spatial import extract_spatial_candidates


MACHINE_ID = "stern.transformers-pro.2011"
TABLE_SOURCE_ID = "vpx-table.transformers-pro-sg1bson-mod-of-jpsalas-1.0.0"
TABLE_FILENAME = "Transformers (Stern 2011) SG1bsoN Mod.vpx"
TABLE_RELATIVE_PATH = Path("stern/transformers-pro-2011/source") / TABLE_FILENAME
EXTRACTION_RELATIVE_PATH = Path("stern/transformers-pro-2011/analysis/vpxtool-0.33.3-extracted")
CANDIDATE_REGISTER_RELATIVE_PATH = Path("evidence/vpx/transformers-pro-2011-sg1bson-candidate-register.json")
VPX_SHA256 = "c4615c93a4cb16b794308d65867015805a58b332b4f93fb995209c05107242cc"
VPX_SIZE = 43503616
VPXTOOL_VERSION = "git:v0.33.3"
MANUAL_SOURCE_ID = "manual.transformers-pro-le.2011"
MANUAL_SHA256 = "9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8"


def _extraction_manifest(extraction_root: Path) -> dict[str, Any]:
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
				"sha256": file_sha256(path),
			}
			for path in paths
		],
	}


def _collection_items(extraction_root: Path, collection_name: str) -> list[str]:
	collections = load_json(extraction_root / "collections.json")
	for collection in collections:
		if collection.get("name") == collection_name:
			items = collection.get("items")
			if isinstance(items, list) and all(isinstance(item, str) for item in items):
				return items
	raise RuntimeError(f"VPX extraction has no usable {collection_name} collection")


def _script_line(script: str, expression: str) -> int:
	for line_number, line in enumerate(script.splitlines(), start=1):
		if line.strip().casefold() == expression.casefold():
			return line_number
	raise RuntimeError(f"VPX script does not contain expected expression: {expression}")


def _script_romname(script: str) -> str:
	match = re.search(r'^\s*(?:Const\s+)?cGameName\s*=\s*"([^"]+)"', script, re.IGNORECASE | re.MULTILINE)
	if match is None:
		raise RuntimeError("VPX script does not declare cGameName")
	return match.group(1)


def _item(extraction_root: Path, relative_path: str, kind: str) -> dict[str, Any]:
	record = load_json(extraction_root / relative_path)
	value = record.get(kind)
	if not isinstance(value, dict):
		raise RuntimeError(f"VPX extraction item is not a {kind}: {relative_path}")
	return value


def build_candidate_register(source_root: Path) -> dict[str, Any]:
	"""Rebuild the committed candidate register from retained VPX extraction bytes."""
	source_root = source_root.expanduser().resolve()
	table_path = source_root / TABLE_RELATIVE_PATH
	extraction_root = source_root / EXTRACTION_RELATIVE_PATH
	if not table_path.is_file():
		raise RuntimeError(f"Retained Transformers Pro table is missing: {table_path}")
	if not extraction_root.is_dir():
		raise RuntimeError(f"Retained Transformers Pro VPX extraction is missing: {extraction_root}")
	if table_path.stat().st_size != VPX_SIZE or file_sha256(table_path) != VPX_SHA256:
		raise RuntimeError(f"Retained Transformers Pro table identity mismatch: {table_path}")

	info = load_json(extraction_root / "info.json")
	gamedata = load_json(extraction_root / "gamedata.json")
	script = (extraction_root / "script.vbs").read_text(encoding="utf-8")
	gi_members = _collection_items(extraction_root, "aGiLights")
	extracted_candidates = extract_spatial_candidates(extraction_root, table_path, VPXTOOL_VERSION)
	candidates_by_name = {candidate["name"]: candidate for candidate in extracted_candidates["objects"]}
	gi_anchors = []
	for name in gi_members:
		if not name.casefold().startswith("gi"):
			continue
		candidate = candidates_by_name.get(name)
		if candidate is None:
			raise RuntimeError(f"VPX candidate extraction did not yield GI anchor {name}")
		gi_anchors.append({key: candidate[key] for key in ("name", "type", "x", "y")})

	f20 = _item(extraction_root, "gameitems/Light.f20.json", "Light")
	f20a = _item(extraction_root, "gameitems/Flasher.f20a.json", "Flasher")
	f32 = _item(extraction_root, "gameitems/Flasher.f32.json", "Flasher")
	f20a_polygon = f20a.get("drag_points")
	polygon = f32.get("drag_points")
	if not isinstance(f20a_polygon, list) or len(f20a_polygon) != 4:
		raise RuntimeError("VPX f20a flasher must retain its complete four-point polygon")
	if not isinstance(polygon, list) or len(polygon) != 4:
		raise RuntimeError("VPX f32 flasher must retain its complete four-point polygon")
	if not all(isinstance(point, dict) and isinstance(point.get("x"), (int, float)) and isinstance(point.get("y"), (int, float)) for point in f20a_polygon):
		raise RuntimeError("VPX f20a polygon has unusable coordinates")
	if not all(isinstance(point, dict) and isinstance(point.get("x"), (int, float)) and isinstance(point.get("y"), (int, float)) for point in polygon):
		raise RuntimeError("VPX f32 polygon has unusable coordinates")
	center = f20.get("center")
	if not isinstance(center, dict) or not isinstance(center.get("x"), (int, float)) or not isinstance(center.get("y"), (int, float)):
		raise RuntimeError("VPX f20 light has no usable center")

	manifest = _extraction_manifest(extraction_root)
	manifest_files = manifest["files"]
	non_gi_members = [name for name in gi_members if not name.casefold().startswith("gi")]
	return {
		"format": "pinmame-vpx-spatial-candidate-register",
		"version": 1,
		"machine_id": MACHINE_ID,
		"source": {
			"table": {
				"source_id": TABLE_SOURCE_ID,
				"relative_path": TABLE_RELATIVE_PATH.as_posix(),
				"original_filename": TABLE_FILENAME,
				"bytes": VPX_SIZE,
				"sha256": VPX_SHA256,
				"vpxtool_romname": _script_romname(script),
				"known_working": False,
				"derivative": {
					"base_table_name": info.get("table_name"),
					"base_author_name": info.get("author_name"),
					"base_table_version": info.get("table_version"),
					"mod_filename_marker": "SG1bsoN Mod",
					"table_save_rev": info.get("table_save_rev"),
					"table_save_date": info.get("table_save_date"),
				},
			},
			"extraction": {
				"relative_path": EXTRACTION_RELATIVE_PATH.as_posix(),
				"vpxtool_version": VPXTOOL_VERSION,
				"manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
				"file_count": len(manifest_files),
				"total_bytes": sum(item["size"] for item in manifest_files),
				"manifest_sha256": hashlib.sha256(canonical_bytes(manifest)).hexdigest(),
			},
			"manual": {"source_id": MANUAL_SOURCE_ID, "sha256": MANUAL_SHA256},
		},
		"bounds_coordinate_space": "vpx_table_units",
		"bounds": {key: gamedata[key] for key in ("left", "top", "right", "bottom")},
		"review": {
			"q20": {
				"controller_output": 20,
				"coordinate_space": "vpx_table_units",
				"script_mappings": [
					{"path": "script.vbs", "line": _script_line(script, "Lampm 120, f20"), "expression": "Lampm 120, f20"},
					{"path": "script.vbs", "line": _script_line(script, "Flash 120, f20a"), "expression": "Flash 120, f20a"},
				],
				"objects": [
					{
						"path": "gameitems/Light.f20.json",
						"sha256": file_sha256(extraction_root / "gameitems/Light.f20.json"),
						"name": f20.get("name"),
						"candidate_center": {"x": center["x"], "y": center["y"]},
					},
					{
						"path": "gameitems/Flasher.f20a.json",
						"sha256": file_sha256(extraction_root / "gameitems/Flasher.f20a.json"),
						"name": f20a.get("name"),
						"declared_origin": {"x": f20a.get("pos_x"), "y": f20a.get("pos_y")},
						"polygon": [{"x": point["x"], "y": point["y"]} for point in f20a_polygon],
					},
				],
				"canonical_placement": None,
				"disposition": "unresolved",
				"reason": "The f20 light and f20a flasher are render candidates driven together; neither establishes the physical Q20 emitter inventory or a canonical placement.",
			},
			"q32": {
				"controller_output": 32,
				"coordinate_space": "vpx_table_units",
				"script_mapping": {"path": "script.vbs", "line": _script_line(script, "Flash 132, f32"), "expression": "Flash 132, f32"},
				"object": {
					"path": "gameitems/Flasher.f32.json",
					"sha256": file_sha256(extraction_root / "gameitems/Flasher.f32.json"),
					"name": f32.get("name"),
					"declared_origin": {"x": f32.get("pos_x"), "y": f32.get("pos_y")},
					"polygon": [{"x": point["x"], "y": point["y"]} for point in polygon],
				},
				"manual_location": {"source_ref": MANUAL_SOURCE_ID, "pdf_page": 132, "status": "unreconciled"},
				"canonical_placement": None,
				"disposition": "unresolved",
				"reason": "The declared origin and polygon disagree, the flasher is a render surface rather than an observed socket, and manual page 132 remains unreconciled.",
			},
			"gi": {
				"collection": "aGiLights",
				"coordinate_space": "normalized_playfield_0_1",
				"members": gi_members,
				"candidate_anchors": gi_anchors,
				"non_gi_members": non_gi_members,
				"unresolved_members": non_gi_members,
				"manual_supplement": {"source_ref": MANUAL_SOURCE_ID, "missing_footer_pages": [6, 7, 8, 11, 14], "status": "incomplete"},
				"canonical_placement": None,
				"disposition": "unresolved",
				"reason": "Candidate render objects and co-located layers have not been reconciled to physical GI sockets or manual multiplicity.",
			},
		},
	}


def load_candidate_register(root: Path = ROOT) -> dict[str, Any]:
	"""Load the portable committed record that review prose is allowed to cite."""
	register_path = root / CANDIDATE_REGISTER_RELATIVE_PATH
	if not register_path.is_file():
		raise RuntimeError(f"Transformers Pro spatial candidate register is missing: {register_path}")
	register = load_json(register_path)
	if register.get("format") != "pinmame-vpx-spatial-candidate-register" or register.get("version") != 1 or register.get("machine_id") != MACHINE_ID:
		raise RuntimeError(f"Transformers Pro spatial candidate register has an unexpected identity: {register_path}")
	return register


def spatial_review_disposition(root: Path = ROOT) -> dict[str, Any]:
	"""Derive only fail-closed disposition figures from the committed candidate register."""
	register = load_candidate_register(root)
	review = register.get("review")
	if not isinstance(review, dict):
		raise RuntimeError("Transformers Pro spatial candidate register has no review section")
	q20 = review.get("q20")
	q32 = review.get("q32")
	gi = review.get("gi")
	if not all(isinstance(item, dict) for item in (q20, q32, gi)):
		raise RuntimeError("Transformers Pro spatial candidate register has incomplete Q20/Q32/GI review evidence")
	if q20.get("canonical_placement") is not None or q32.get("canonical_placement") is not None or gi.get("canonical_placement") is not None:
		raise RuntimeError("Transformers Pro spatial review must not emit an unsupported canonical placement")
	if q20.get("disposition") != "unresolved" or q32.get("disposition") != "unresolved" or gi.get("disposition") != "unresolved":
		raise RuntimeError("Transformers Pro spatial review disposition must remain unresolved")
	if q20.get("coordinate_space") != "vpx_table_units" or q32.get("coordinate_space") != "vpx_table_units" or gi.get("coordinate_space") != "normalized_playfield_0_1":
		raise RuntimeError("Transformers Pro candidate coordinate spaces are missing or inconsistent")
	q20_objects = q20.get("objects")
	q20_mappings = q20.get("script_mappings")
	if not isinstance(q20_objects, list) or len(q20_objects) != 2 or {item.get("name") for item in q20_objects if isinstance(item, dict)} != {"f20", "f20a"}:
		raise RuntimeError("Transformers Pro Q20 evidence must retain both f20 and f20a candidates")
	if not isinstance(q20_mappings, list) or len(q20_mappings) != 2 or {item.get("expression") for item in q20_mappings if isinstance(item, dict)} != {"Lampm 120, f20", "Flash 120, f20a"}:
		raise RuntimeError("Transformers Pro Q20 evidence must retain both script mappings")
	members = gi.get("members")
	anchors = gi.get("candidate_anchors")
	unresolved_members = gi.get("unresolved_members")
	non_gi_members = gi.get("non_gi_members")
	manual_supplement = gi.get("manual_supplement")
	if not isinstance(members, list) or not isinstance(anchors, list) or not isinstance(non_gi_members, list) or not isinstance(unresolved_members, list) or not isinstance(manual_supplement, dict):
		raise RuntimeError("Transformers Pro GI review evidence is malformed")
	if {member.get("name") for member in anchors if isinstance(member, dict)} != {member for member in members if isinstance(member, str) and member.casefold().startswith("gi")}:
		raise RuntimeError("Transformers Pro GI anchors no longer match the gi-prefixed members of aGiLights")
	expected_non_gi = [member for member in members if isinstance(member, str) and not member.casefold().startswith("gi")]
	if non_gi_members != expected_non_gi:
		raise RuntimeError("Transformers Pro non-GI members are not derived from the complete aGiLights collection")
	positions = {(anchor.get("x"), anchor.get("y")) for anchor in anchors if isinstance(anchor, dict)}
	if len(positions) != len({position for position in positions if all(isinstance(value, (int, float)) for value in position)}):
		raise RuntimeError("Transformers Pro GI anchors have unsupported coordinates")
	if unresolved_members != non_gi_members:
		raise RuntimeError("Every unclassified non-GI render member must remain unresolved")
	missing_pages = manual_supplement.get("missing_footer_pages")
	if not isinstance(missing_pages, list) or not missing_pages or not all(isinstance(page, int) and page > 0 for page in missing_pages) or missing_pages != sorted(set(missing_pages)):
		raise RuntimeError("Transformers Pro GI manual supplement gap is malformed")
	return {
		"register": {
			"path": CANDIDATE_REGISTER_RELATIVE_PATH.as_posix(),
			"sha256": file_sha256(root / CANDIDATE_REGISTER_RELATIVE_PATH),
		},
		"q20": q20,
		"q32": q32,
		"gi": {
			"collection": gi.get("collection"),
			"member_count": len(members),
			"anchor_count": len(anchors),
			"distinct_position_count": len(positions),
			"unresolved_members": tuple(unresolved_members),
			"missing_footer_pages": tuple(missing_pages),
		},
	}


def _page_ranges(pages: tuple[int, ...]) -> str:
	ranges: list[str] = []
	start = previous = pages[0]
	for page in pages[1:]:
		if page == previous + 1:
			previous = page
			continue
		ranges.append(str(start) if start == previous else f"{start}-{previous}")
		start = previous = page
	ranges.append(str(start) if start == previous else f"{start}-{previous}")
	return ", ".join(ranges)


def spatial_review_markdown(root: Path = ROOT) -> str:
	"""Render the knowledge-note disposition from portable, derived evidence only."""
	disposition = spatial_review_disposition(root)
	register = disposition["register"]
	gi = disposition["gi"]
	unresolved_members = ", ".join(f"`{member}`" for member in gi["unresolved_members"])
	return f"""## Spatial review disposition

Spatial promotion is fail-closed. The portable record is `{register["path"]}`, SHA-256 `{register["sha256"]}`. It retains both table objects driven by Q20: `Lampm 120, f20` and `Flash 120, f20a`; no canonical Q20 placement is asserted because both remain render candidates and the complete physical emitter inventory is not reconciled, and the prior BallRelease anchor is rejected. Q32 maps to f32, and `Flasher.f32.json` retains its complete four-point polygon. No Q32 placement is emitted because f32's declared origin disagrees with that polygon, the flasher is a render surface rather than an observed socket, and official coil/flasher location PDF page 132 remains unreconciled.

The table's `{gi["collection"]}` collection has {gi["member_count"]} members. Its deterministic candidate register contains {gi["anchor_count"]} `gi*` anchors at {gi["distinct_position_count"]} distinct positions. Every non-`gi` collection member remains explicitly unresolved: {unresolved_members}. The retained Pro supplement is incomplete: footer pages {_page_ranges(gi["missing_footer_pages"])} are missing. Therefore GI quantity and placements remain unresolved: no physical GI count is asserted and no GI render helper is promoted as a physical emitter. Restore author-ready status only after the exact member list, physical-object classification, manual multiplicity, and every deduplication decision are recorded and tested.

"""
