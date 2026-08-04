from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.spatial import (
	SPATIAL_RETROFIT_PENDING_MACHINE_IDS,
	extract_spatial_candidates,
	fail_closed_spatial_knowledge,
	render_spatial_overlay,
)
from pinmame_game_defs.coverage import build_coverage_report
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]


def provenance() -> dict[str, object]:
	return {"status": "validated", "source_refs": ["review.geometry"]}


def placement(identifier: str, role: str, x: float = 0.25, y: float = 0.75) -> dict[str, object]:
	return {"id": identifier, "role": role, "space": "playfield", "x": x, "y": y, "provenance": provenance()}


def author_ready_definition() -> dict[str, object]:
	return {
		"format": "pinmame-machine-definition",
		"schema_version": 2,
		"machine": {"id": "test.spatial.2000", "name": "Spatial Test", "manufacturer": "Test", "year": 2000},
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
		"drivers": [{"id": "testspat", "description": "Spatial Test", "year": "2000", "manufacturer": "Test", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Same physical test machine."}],
		"inputs": [{"id": "switch.target", "label": "Target", "kind": "switch", "binding": {"group": "test.input", "device": 1}, "aliases": [], "availability": "used", "normally_closed": False, "provenance": provenance(), "spatial": {"status": "validated", "placements": [placement("switch.target.sensor", "sensor")]}}],
		"outputs": [{"id": "lamp.target", "label": "Target lamp", "kind": "lamp", "binding": {"group": "test.output", "device": 1}, "aliases": [], "availability": "used", "provenance": provenance(), "spatial": {"status": "validated", "placements": [placement("lamp.target.emitter", "emitter", 0.5, 0.5)]}}],
		"displays": [{"id": "display.dmd", "label": "Display", "kind": "dmd", "width": 128, "height": 32, "provenance": provenance()}],
		"mechanisms": [{"id": "mechanism.target", "label": "Target", "kind": "other", "actuators": ["lamp.target"], "sensors": ["switch.target"], "behavior": "Test mechanism.", "provenance": provenance()}],
		"relationships": [],
		"sources": [{"id": "review.geometry", "kind": "human_review", "uri": "https://example.invalid/spatial-test", "locator": "reviewed geometry", "known_working": True}],
		"knowledge": {"path": "knowledge/test/spatial.md", "status": "complete"},
		"conflicts": [],
	}


class SpatialSchemaAndValidationTests(unittest.TestCase):
	def test_v1_partial_remains_schema_compatible(self) -> None:
		definition = author_ready_definition()
		definition["schema_version"] = 1
		definition["coverage"]["status"] = "partial"
		definition["coverage"]["missing"] = ["spatial_placement"]
		del definition["coverage"]["dimensions"]["spatial_placement"]
		self.assertEqual([], validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "fixture"))

	def test_schema_rejects_v1_author_ready(self) -> None:
		definition = author_ready_definition()
		definition["schema_version"] = 1
		errors = validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "fixture")
		self.assertTrue(errors)
		self.assertIn("schema_version", " ".join(errors))

	def test_source_extensions_include_known_working_and_vpe_scene(self) -> None:
		definition = author_ready_definition()
		definition["sources"][0]["kind"] = "vpe_scene"
		self.assertEqual([], validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "fixture"))

	def test_author_ready_requires_v2_and_complete_spatial_records(self) -> None:
		definition = author_ready_definition()
		definition["schema_version"] = 1
		errors = validate_machine(definition)
		self.assertTrue(any("author-ready definitions must use schema version 2" in error for error in errors))
		definition = author_ready_definition()
		del definition["inputs"][0]["spatial"]
		errors = validate_machine(definition)
		self.assertTrue(any("author-ready devices require spatial evidence" in error for error in errors))

	def test_schema_shape_and_coordinate_rules_fail_closed(self) -> None:
		self.assertEqual([], validate_machine(author_ready_definition()))
		for coordinate, value, expected in (("x", 1.1, "inclusive 0..1"), ("y", float("nan"), "finite number"), ("x", 0.1234567, "six fractional")):
			definition = author_ready_definition()
			definition["inputs"][0]["spatial"]["placements"][0][coordinate] = value
			self.assertTrue(any(expected in error for error in validate_machine(definition)), coordinate)
		definition = author_ready_definition()
		definition["outputs"][0]["spatial"]["placements"][0]["id"] = "switch.target.sensor"
		self.assertTrue(any("duplicate spatial placement ID" in error for error in validate_machine(definition)))

	def test_spatial_provenance_roles_and_na_alignment_are_enforced(self) -> None:
		definition = author_ready_definition()
		definition["inputs"][0]["spatial"]["placements"][0]["provenance"]["source_refs"] = ["missing.source"]
		self.assertTrue(any("unknown source reference" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["outputs"][0]["spatial"]["placements"][0]["role"] = "sensor"
		self.assertTrue(any("require only emitter placements" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["outputs"][0]["kind"] = "coil"
		definition["outputs"][0]["spatial"]["placements"][0]["role"] = "emitter"
		self.assertTrue(any("require only effect placements" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["inputs"][0]["roles"] = ["cabinet.start"]
		definition["inputs"][0]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
		definition["inputs"][0]["spatial"]["reason"] = "unused"
		self.assertTrue(any("does not align" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["inputs"][0]["roles"] = ["flipper.lower.left.button"]
		definition["inputs"][0]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
		definition["inputs"][0]["roles"] = ["flipper.lower.left.eos"]
		self.assertTrue(any("does not align" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["outputs"][0]["kind"] = "coil"
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "internal_nonvisual", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
		definition = author_ready_definition()
		definition["outputs"][0]["roles"] = ["cabinet.start"]
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
		definition["outputs"][0]["spatial"]["reason"] = "internal_nonvisual"
		self.assertTrue(any("does not align" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["outputs"][0]["roles"] = ["internal.load"]
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "internal_nonvisual", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
		definition["outputs"][0]["spatial"]["reason"] = "cabinet_or_service"
		self.assertTrue(any("does not align" in error for error in validate_machine(definition)))
		definition = author_ready_definition()
		definition["outputs"][0]["kind"] = "coil"
		definition["outputs"][0]["roles"] = ["cabinet.knocker"]
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))

	def test_local_l_drive_source_is_rejected(self) -> None:
		definition = author_ready_definition()
		definition["sources"][0]["locator"] = "Acquired from L:\\Visual Pinball\\Tables\\Spatial Test.vpx"
		self.assertTrue(any("local L: paths" in error for error in validate_machine(definition)))


class SpatialToolTests(unittest.TestCase):
	def _write_extraction_fixture(self, root: Path) -> Path:
		extracted = root / "table-extracted"
		(extracted / "gameitems").mkdir(parents=True)
		(extracted / "gamedata.json").write_text(json.dumps({"left": 100, "top": 200, "right": 1100, "bottom": 2200}), encoding="utf-8")
		(extracted / "gameitems" / "Trigger.Zeta.json").write_text(json.dumps({"Trigger": {"center": {"x": 600, "y": 1200}, "name": "Zeta"}}), encoding="utf-8")
		(extracted / "gameitems" / "Bumper.Alpha.json").write_text(json.dumps({"Bumper": {"center": {"x": 350, "y": 700}, "name": "Alpha"}}), encoding="utf-8")
		(extracted / "gameitems" / "Flasher.Beta.json").write_text(json.dumps({"Flasher": {"pos_x": 850, "pos_y": 1700, "name": "Beta"}}), encoding="utf-8")
		(extracted / "gameitems" / "HitTarget.Gamma.json").write_text(json.dumps({"HitTarget": {"position": {"x": 1100, "y": 2200}, "name": "Gamma"}}), encoding="utf-8")
		(extracted / "gameitems" / "Light.Backglass.json").write_text(json.dumps({"Light": {"center": {"x": 500, "y": 500}, "name": "Backglass", "is_backglass": True}}), encoding="utf-8")
		(extracted / "gameitems" / "Light.Outside.json").write_text(json.dumps({"Light": {"center": {"x": 1200, "y": 500}, "name": "Outside"}}), encoding="utf-8")
		(extracted / "gameitems" / "Primitive.Ignore.json").write_text(json.dumps({"data": {"x": 999, "y": 999}}), encoding="utf-8")
		return extracted

	def test_extractor_normalizes_orders_and_ignores_paths(self) -> None:
		with tempfile.TemporaryDirectory() as first_directory, tempfile.TemporaryDirectory() as second_directory:
			first = Path(first_directory)
			second = Path(second_directory)
			first_vpx = first / "source.vpx"
			second_vpx = second / "different-name.vpx"
			first_vpx.write_bytes(b"same source bytes")
			second_vpx.write_bytes(b"same source bytes")
			first_report = extract_spatial_candidates(self._write_extraction_fixture(first), first_vpx)
			second_report = extract_spatial_candidates(self._write_extraction_fixture(second), second_vpx)
			self.assertEqual(first_report, second_report)
			self.assertEqual(
				[
					{"type": "Bumper", "name": "Alpha", "x": 0.25, "y": 0.25},
					{"type": "Flasher", "name": "Beta", "x": 0.75, "y": 0.75},
					{"type": "HitTarget", "name": "Gamma", "x": 1.0, "y": 1.0},
					{"type": "Trigger", "name": "Zeta", "x": 0.5, "y": 0.5},
				],
				first_report["objects"],
			)

	def test_overlay_is_deterministic_and_includes_markers_and_na_counts(self) -> None:
		definition = author_ready_definition()
		definition["outputs"][0]["availability"] = "unused"
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "unused", "provenance": provenance()}
		first = render_spatial_overlay(definition)
		self.assertEqual(first, render_spatial_overlay(copy.deepcopy(definition)))
		self.assertIn("switch.target:switch.target.sensor", first)
		self.assertIn("N/A devices: unused=1", first)
		self.assertIn("#1769aa", first)


class SpatialMigrationTests(unittest.TestCase):
	def test_knowledge_banner_is_idempotent_and_nonpending_is_unchanged(self) -> None:
		machine_id = SPATIAL_RETROFIT_PENDING_MACHINE_IDS[0]
		text = "# Example recreation knowledge\n\nCoverage: **author-ready - switches and wiring validated**\n\nBody."
		expected = (
			"# Example recreation knowledge\n"
			"\nCoverage: **partial — normalized spatial placements pending.**\n"
			"Previously validated non-spatial scope: **switches and wiring validated**\n\nBody."
		)
		transformed = fail_closed_spatial_knowledge(machine_id, text)
		self.assertEqual(expected, transformed)
		self.assertEqual(transformed, fail_closed_spatial_knowledge(machine_id, transformed))
		self.assertEqual(text, fail_closed_spatial_knowledge("stern.not-pending.2000", text))
		self.assertFalse(fail_closed_spatial_knowledge(machine_id, text).endswith("\n"))
		self.assertTrue(fail_closed_spatial_knowledge(machine_id, text + "\n").endswith("\n"))

	def test_pending_spatial_retrofits_are_conspicuous_v2_partials_and_reports_reconcile(self) -> None:
		definitions = [load_json(path) for path in sorted((ROOT / "machines" / "partial").rglob("*.json"))]
		migrated = {definition["machine"]["id"]: definition for definition in definitions if definition["machine"]["id"] in SPATIAL_RETROFIT_PENDING_MACHINE_IDS}
		self.assertEqual(set(SPATIAL_RETROFIT_PENDING_MACHINE_IDS), set(migrated))
		self.assertEqual(25, len(migrated))
		for definition in migrated.values():
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			self.assertEqual(["spatial_placement"], definition["coverage"]["missing"])
			self.assertEqual("unknown", definition["coverage"]["dimensions"]["spatial_placement"])
			self.assertTrue(all(value == "validated" for key, value in definition["coverage"]["dimensions"].items() if key != "spatial_placement"))
		self.assertEqual(8, len(list((ROOT / "machines" / "author-ready").rglob("*.json"))))
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		report = build_coverage_report(ROOT)
		self.assertEqual(catalog["summary"]["machine_count"], report["catalog_record_count"])
		self.assertEqual(catalog["summary"]["game_count"], report["machine_count"])
		self.assertEqual(catalog["summary"]["author_ready_count"], report["author_ready_count"])
		self.assertEqual(785, report["machine_count"])
		self.assertEqual(8, report["author_ready_count"])
		self.assertEqual(94, report["partial_count"])
		self.assertEqual(683, report["stub_count"])
		self.assertEqual(1, report["non_game_record_count"])
		self.assertEqual(786, report["catalog_record_count"])
		self.assertEqual(25, report["missing_requirement_counts"]["spatial_placement"])
		self.assertEqual(786, len(catalog["machines"]))
		self.assertEqual(785, catalog["summary"]["game_count"])
		self.assertEqual(786, catalog["summary"]["machine_count"])
		self.assertEqual(8, catalog["summary"]["author_ready_count"])
		self.assertEqual(683, catalog["summary"]["stub_count"])
		self.assertEqual(95, catalog["summary"]["partial_count"])
		self.assertEqual(1, catalog["summary"]["non_game_count"])
		note_paths = {definition["knowledge"]["path"] for definition in migrated.values()}
		self.assertEqual(25, len(note_paths))
		for relative_path in note_paths:
			note = (ROOT / relative_path).read_text(encoding="utf-8")
			self.assertIn("Coverage: **partial — normalized spatial placements pending.**", note.splitlines())
			self.assertFalse(any(line.startswith("Coverage: **author-ready") for line in note.splitlines()))


if __name__ == "__main__":
	unittest.main()
