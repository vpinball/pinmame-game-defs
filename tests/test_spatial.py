from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.cli import main as cli_main
from pinmame_game_defs.conflicts import unresolved_conflicts
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
		"displays": [{"id": "display.dmd", "label": "Display", "kind": "dmd", "width": 128, "height": 32, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}, "provenance": provenance()}],
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
		definition = author_ready_definition()
		del definition["displays"][0]["spatial"]
		errors = validate_machine(definition)
		self.assertTrue(any("author-ready displays require spatial evidence" in error for error in errors))

	def test_author_ready_display_spatial_is_controlled_and_not_playfield(self) -> None:
		definition = author_ready_definition()
		definition["displays"][0]["spatial"] = {
			"status": "not_applicable",
			"reason": "cabinet_or_service",
			"provenance": provenance(),
		}
		self.assertEqual([], validate_machine(definition))
		definition["displays"][0]["spatial"] = {
			"status": "validated",
			"placements": [placement("display.dmd.screen", "emitter")],
		}
		errors = validate_machine(definition)
		self.assertTrue(any("located playfield display coordinates are not supported" in error for error in errors))
		definition["displays"][0]["spatial"] = {
			"status": "not_applicable",
			"reason": "internal_nonvisual",
			"provenance": provenance(),
		}
		errors = validate_machine(definition)
		self.assertTrue(any("displays must use reason cabinet_or_service" in error for error in errors))

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
		definition["inputs"][0]["roles"] = ["internal.trough"]
		definition["inputs"][0]["spatial"] = {"status": "not_applicable", "reason": "internal_nonvisual", "provenance": provenance()}
		self.assertEqual([], validate_machine(definition))
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

	def test_author_ready_physical_displays_are_fail_closed_to_cabinet_service_na(self) -> None:
		definition = author_ready_definition()
		self.assertEqual([], validate_machine(definition))
		for reason in ("dip_switch", "unused", "virtual", "optional_absent", "internal_nonvisual"):
			invalid = author_ready_definition()
			invalid["displays"][0]["spatial"]["reason"] = reason
			errors = validate_machine(invalid)
			self.assertTrue(any("displays must use reason cabinet_or_service" in error for error in errors), reason)

		valid = author_ready_definition()
		valid["displays"][0]["spatial"] = {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": provenance()}
		self.assertEqual([], validate_machine(valid))

	def test_located_playfield_displays_are_rejected_by_the_canonical_policy(self) -> None:
		definition = author_ready_definition()
		definition["displays"][0]["spatial"] = {
			"status": "validated",
			"placements": [{"id": "display.dmd.emitter", "role": "emitter", "space": "playfield", "x": 0.5, "y": 0.5, "provenance": provenance()}],
		}
		errors = validate_machine(definition)
		self.assertEqual(
			"$.displays[0].spatial.status: located playfield display coordinates are not supported; displays must use not_applicable with reason cabinet_or_service",
			next(error for error in errors if "located playfield display coordinates" in error),
		)

	def test_local_l_drive_source_is_rejected(self) -> None:
		definition = author_ready_definition()
		definition["sources"][0]["locator"] = "Acquired from L:\\Visual Pinball\\Tables\\Spatial Test.vpx"
		self.assertTrue(any("local L: paths" in error for error in validate_machine(definition)))


class SpatialToolTests(unittest.TestCase):
	def _populate_extraction_fixture(self, extracted: Path) -> None:
		(extracted / "gameitems").mkdir(parents=True)
		(extracted / "gamedata.json").write_text(json.dumps({"left": 100, "top": 200, "right": 1100, "bottom": 2200}), encoding="utf-8")
		(extracted / "gameitems" / "Trigger.Zeta.json").write_text(json.dumps({"Trigger": {"center": {"x": 600, "y": 1200}, "name": "Zeta"}}), encoding="utf-8")
		(extracted / "gameitems" / "Bumper.Alpha.json").write_text(json.dumps({"Bumper": {"center": {"x": 350, "y": 700}, "name": "Alpha"}}), encoding="utf-8")
		(extracted / "gameitems" / "Flasher.Beta.json").write_text(json.dumps({"Flasher": {"pos_x": 850, "pos_y": 1700, "name": "Beta"}}), encoding="utf-8")
		(extracted / "gameitems" / "HitTarget.Gamma.json").write_text(json.dumps({"HitTarget": {"position": {"x": 1100, "y": 2200}, "name": "Gamma"}}), encoding="utf-8")
		(extracted / "gameitems" / "Primitive.Delta.json").write_text(json.dumps({"Primitive": {"position": {"x": 400, "y": 800}, "name": "Delta"}}), encoding="utf-8")
		(extracted / "gameitems" / "Wall.Sling.json").write_text(json.dumps({"Wall": {"drag_points": [{"x": 300, "y": 600}, {"x": 500, "y": 600}, {"x": 500, "y": 1000}, {"x": 300, "y": 1000}], "name": "Sling"}}), encoding="utf-8")

	def _write_extraction_fixture(self, root: Path) -> Path:
		extracted = root / "table-extracted"
		self._populate_extraction_fixture(extracted)
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
			self.assertEqual(2, first_report["version"])
			self.assertEqual(
				[
					{"type": "Bumper", "name": "Alpha", "x": 0.25, "y": 0.25},
					{"type": "Flasher", "name": "Beta", "x": 0.75, "y": 0.75},
					{"type": "HitTarget", "name": "Gamma", "x": 1.0, "y": 1.0},
					{"type": "Primitive", "name": "Delta", "x": 0.3, "y": 0.3, "center_method": "position", "source_path": "gameitems/Primitive.Delta.json"},
					{"type": "Trigger", "name": "Zeta", "x": 0.5, "y": 0.5},
					{"type": "Wall", "name": "Sling", "x": 0.3, "y": 0.3, "center_method": "drag_point_centroid", "source_path": "gameitems/Wall.Sling.json"},
				],
				first_report["objects"],
			)
			self.assertEqual([], validate_against_schema(first_report, ROOT / "schemas" / "vpx-spatial-candidates.schema.json", "fixture"))
			invalid_report = copy.deepcopy(first_report)
			del invalid_report["objects"][3]["source_path"]
			self.assertTrue(validate_against_schema(invalid_report, ROOT / "schemas" / "vpx-spatial-candidates.schema.json", "fixture"))

	def test_cli_vpx_route_uses_fresh_extraction_root_and_schema_contract(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			root = Path(temporary_directory)
			source_vpx = root / "source.vpx"
			vpxtool = root / "vpxtool"
			output = root / "fresh-report.json"
			source_vpx.write_bytes(b"fresh source bytes")
			vpxtool.write_text("fake vpxtool", encoding="utf-8")

			def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
				if "extract" in command:
					destination = Path(command[command.index("--output-dir") + 1])
					self._populate_extraction_fixture(destination)
					return subprocess.CompletedProcess(command, 0, "", "")
				return subprocess.CompletedProcess(command, 0, "vpxtool test 1.0\n", "")

			with patch("pinmame_game_defs.spatial.subprocess.run", side_effect=fake_run):
				with self.assertRaises(SystemExit) as exit_result:
					cli_main(["--repository-root", str(ROOT), "extract-spatial", "--vpx", str(source_vpx), "--vpxtool", str(vpxtool), "--output", str(output)])
				self.assertEqual(0, exit_result.exception.code)

			report = load_json(output)
			self.assertEqual("vpxtool test 1.0", report["source"]["vpxtool_version"])
			self.assertEqual([], validate_against_schema(report, ROOT / "schemas" / "vpx-spatial-candidates.schema.json", "fresh-vpx-route"))
			self.assertTrue(all(item["source_path"].startswith("gameitems/") for item in report["objects"] if item["type"] in {"Primitive", "Wall"}))

	def test_overlay_is_deterministic_and_includes_markers_and_na_counts(self) -> None:
		definition = author_ready_definition()
		definition["outputs"][0]["availability"] = "unused"
		definition["outputs"][0]["spatial"] = {"status": "not_applicable", "reason": "unused", "provenance": provenance()}
		first = render_spatial_overlay(definition)
		self.assertEqual(first, render_spatial_overlay(copy.deepcopy(definition)))
		self.assertIn("switch.target:switch.target.sensor", first)
		self.assertIn("N/A devices: unused=1", first)
		self.assertIn("#1769aa", first)

	def test_rolling_stones_spatial_promotion_has_no_fixed_review_artifact_path(self) -> None:
		source = (ROOT / "tools" / "curate_rolling_stones_le_spatial.py").read_text(encoding="utf-8").casefold()
		self.assertNotIn("e:\\_vpe-2025", source)
		self.assertNotIn("e:/_vpe-2025", source)
		self.assertIn("explicit-output", source)


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
		self.assertEqual(12, len(migrated))
		for definition in migrated.values():
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			if definition["machine"]["id"] == "stern.twenty-four.2009":
				self.assertEqual({"input_semantics", "output_semantics", "mechanism_behavior", "recreation_notes", "spatial_placement", "unresolved_conflicts"}, set(definition["coverage"]["missing"]))
				self.assertEqual("observed", definition["coverage"]["dimensions"]["spatial_placement"])
				self.assertEqual("conflicted", definition["coverage"]["dimensions"]["physical_wiring"])
			elif definition["machine"]["id"] == "stern.x-men-pro.2012":
				self.assertEqual(["spatial_placement", "unresolved_conflicts"], definition["coverage"]["missing"])
				self.assertEqual("unknown", definition["coverage"]["dimensions"]["spatial_placement"])
				self.assertTrue(all(value == "validated" for key, value in definition["coverage"]["dimensions"].items() if key != "spatial_placement"))
			else:
				# A pending retrofit that also holds unresolved conflicts must
				# list both; the downgrade used to append only spatial_placement.
				expected = ["spatial_placement"]
				if unresolved_conflicts(definition):
					expected.append("unresolved_conflicts")
				self.assertEqual(expected, definition["coverage"]["missing"])
				self.assertEqual("unknown", definition["coverage"]["dimensions"]["spatial_placement"])
				self.assertTrue(all(value == "validated" for key, value in definition["coverage"]["dimensions"].items() if key != "spatial_placement"))
		self.assertEqual(25, len(list((ROOT / "machines" / "author-ready").rglob("*.json"))))
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		report = build_coverage_report(ROOT)
		self.assertEqual(catalog["summary"]["machine_count"], report["catalog_record_count"])
		self.assertEqual(catalog["summary"]["game_count"], report["machine_count"])
		self.assertEqual(catalog["summary"]["author_ready_count"], report["author_ready_count"])
		self.assertEqual(789, report["machine_count"])
		self.assertEqual(25, report["author_ready_count"])
		self.assertEqual(96, report["partial_count"])
		self.assertEqual(668, report["stub_count"])
		self.assertEqual(1, report["non_game_record_count"])
		self.assertEqual(790, report["catalog_record_count"])
		# The Pinball 2000 baseline adds Revenge From Mars and Star Wars Episode I as two
		# honest physical-game stubs. Its other new root, taf_i4bs, joins the existing
		# Addams Family definition and therefore does not add another physical record.
		# The twelve retrofit-pending machines above (which already include X-Men Pro), plus
		# Terminator 2, plus Centaur, plus Twilight Zone. Centaur is not a retrofit: every one of
		# its devices carries a spatial record except auxiliary lamp 113, a fitted A9 circuit whose
		# function the factory schematic leaves blank and which nothing locates. Monster Bash is
		# also not a retrofit: it was demoted for an unresolved switch-polarity conflict (74-78),
		# not a missing spatial record, so it is not counted here either. Twilight Zone genuinely
		# has unresolved spatial gaps (switches 26/31-33/45/46/55 and GI address 2 have no bound
		# VPX object), so it is counted alongside Centaur/Terminator 2.
		# Cactus Canyon is also not a retrofit: every switch/solenoid/lamp/GI address has a resolved
		# placement or a controlled not_applicable record except flashers 24 and 26, whose second
		# documented (playfield vs insert-panel) bulb has no independently resolvable VPX coordinate.
		# Star Trek: The Next Generation is likewise not a retrofit: it was curated directly from a
		# legacy candidate-only stub, and three lamps (53, 85, 86) have no world-space Light object
		# in the retained extraction (only a local-origin Primitive with an unresolved parent
		# transform), so it is counted as an 18th machine with a genuine spatial gap.
		# Tales of the Arabian Nights is likewise not a retrofit: it was curated directly from a
		# legacy stub, and two GI addresses (3, 4) -- the manual's genuine playfield strings -- have
		# no VPX object bound to them in the retained (non-VPW) extraction, so it is counted as a
		# 19th machine with a genuine spatial gap.
		# Theatre of Magic is likewise not a retrofit: it was curated directly from a legacy stub,
		# and GI address 4 (String 5) -- playfield-wired per the manual -- has no UpdateGI case and
		# therefore no VPX object binding, so it is counted as a 20th machine with a genuine spatial
		# gap.
		# Scared Stiff is likewise not a retrofit: it was curated directly from a legacy candidate-
		# only partial record, and sixteen driver-declared auxiliary lamp addresses (91-98, 101-108)
		# have no spatial key at all because their fitment is a genuine, unresolved two-source
		# disagreement (conflict.aux-lamp-column-fitment), so it is counted as a 21st machine with a
		# genuine spatial gap.
		# The Simpsons Pinball Party is likewise not a retrofit: it was curated directly from a
		# legacy candidate-only partial record, and eight Mini-DMD sign-panel lamps (73-80) have no
		# spatial key at all because the retained table's LEDY/LEDG/LEDR light collections are empty
		# and the l73-l80 Primitive objects that do exist share one (x, y) with only a stacked z
		# offset, so it is counted as a 22nd machine with a genuine spatial gap.
		# Creature from the Black Lagoon is likewise not a retrofit: it was curated directly from a
		# legacy candidate-only partial record. Its retained table is the smallest extraction in the
		# project at 856 files, so GI address 3, the Sequential G.I. chase lamps 91-98 and six fitted
		# flasher solenoids have no bound object, and it is counted as a 23rd machine with a genuine
		# spatial gap.
		# Bally Flash Gordon and Bally Judge Dredd each added one genuine spatial gap (33 from 31):
		# Flash Gordon's two outlane Special inserts sit on the wrong sides in the retained table and
		# are recorded as an unresolved conflict rather than swapped, and Judge Dredd's remaining
		# unplaced devices are named in its own spatial report. Neither replaced a stub, so the
		# partial/stub totals below are unchanged by those two passes.
		# Every catalog count above is one higher than before Bally Eight Ball Deluxe was curated,
		# and none of that increase is a newly covered machine. Curating it claimed the production
		# eballdlx tree and left the four Motorola-68701 hardware prototypes (eballdp1-eballdp4,
		# declared clones by PinMAME but living in by68701.c on different boards) holding the
		# leftover stub, exactly as Kiss's Intel-8035 prototypes did. So the physical-game count
		# went 786 -> 787 by splitting one record into two, not by adding coverage.
		# Lord of the Rings and Data East Batman each replace a legacy candidate-only partial
		# record in place, so the physical coverage totals remain unchanged. Their unresolved
		# placements stay represented in the generated repository-wide count below.
		# Data East Lethal Weapon 3 replaces a legacy candidate-only partial record in place, so
		# partial/stub/author-ready totals are unchanged by it. Every one of its 64 lamp addresses
		# resolved, but exactly one recreation was retained, so the placements are observed rather
		# than validated and the dimension stays incomplete.
		# Playboy 35th Anniversary replaces one residual stub with one partial definition, so it
		# moves only the partial/stub totals and leaves the physical-machine total unchanged.
		# Data East Time Machine likewise replaces one residual stub with one partial definition;
		# its honest partial blockers add one spatial-placement and one unresolved-conflict gap.
		# Torpedo Alley replaces one stub with a partial record and adds a genuine spatial gap: its
		# known-working table supplies candidate geometry, but a physical socket/address and
		# under-playfield actuator survey is still required for validated placement.
		# Data East Secret Service replaces another residual stub with one partial definition. Its
		# unresolved lamp bindings and manual/emulator output conflict add one gap in each count.
		# Data East Laser War replaces one residual stub with one partial definition. Its unresolved
		# tower/GI placements and special-solenoid public mapping add one gap in each count.
		# No Good Gofers replaces one residual stub with one partial definition and adds one spatial
		# gap. Its apparent auxiliary-output discrepancy is a PinMAME type-metadata defect, not an
		# unresolved runtime address map, so it does not add an unresolved-conflict gap.
		# FunHouse's evidence pass resolved its prior semantic conflicts but deliberately retains one
		# spatial gap for the unidentified right-rear-playfield emitters on mixed G.I. circuit 04.
		# Revenge from Mars now resolves its stock geometry from the four factory location drawings;
		# its supplied hybrid AFM table remains rejected; documented expansion optos have observed
		# positions while the remaining per-firmware expansion fitment stays a variant blocker.
		self.assertEqual(44, report["missing_requirement_counts"]["spatial_placement"])
		# 33 until the coverage rule was made symmetric. Eighteen definitions held
		# unresolved conflicts while omitting the requirement — fourteen because
		# `import-legacy` wrote a fixed `MIGRATION_MISSING` list whatever it had just
		# emitted, and four because `fail_closed_spatial_partial` appended only
		# `spatial_placement` when it downgraded an author-ready record. Both are
		# fixed at source; this count is now the honest one.
		# FunHouse resolves one of the 51 unresolved-conflict requirements present on the rebased
		# baseline, leaving only its independently documented spatial blocker.
		self.assertEqual(50, report["missing_requirement_counts"]["unresolved_conflicts"])
		self.assertEqual(790, len(catalog["machines"]))
		self.assertEqual(789, catalog["summary"]["game_count"])
		self.assertEqual(790, catalog["summary"]["machine_count"])
		self.assertEqual(25, catalog["summary"]["author_ready_count"])
		self.assertEqual(668, catalog["summary"]["stub_count"])
		# The catalog count includes the separately classified partial diagnostic; coverage counts
		# only the 789 physical games and therefore reports 96 partial records above.
		self.assertEqual(97, catalog["summary"]["partial_count"])
		self.assertEqual(1, catalog["summary"]["non_game_count"])
		note_paths = {definition["knowledge"]["path"] for definition in migrated.values()}
		self.assertEqual(12, len(note_paths))
		for relative_path in note_paths:
			note = (ROOT / relative_path).read_text(encoding="utf-8")
			if relative_path == "knowledge/stern/twenty-four-2009.md":
				self.assertTrue(note.splitlines()[2].startswith("Coverage: **partial -"))
			else:
				self.assertIn("Coverage: **partial — normalized spatial placements pending.**", note.splitlines())
			self.assertFalse(any(line.startswith("Coverage: **author-ready") for line in note.splitlines()))


if __name__ == "__main__":
	unittest.main()
