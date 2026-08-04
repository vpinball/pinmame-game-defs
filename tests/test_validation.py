from __future__ import annotations

import copy
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import _validate_runtime_observations, validate_machine, validate_repository


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.transformers = load_json(ROOT / "machines" / "partial" / "stern" / "transformers-limited-edition-2011.json")

	def author_ready_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		definition["coverage"]["status"] = "author_ready"
		definition["coverage"]["missing"] = []
		definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
		return definition

	def shared_rgb_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		definition["coverage"]["status"] = "partial"
		definition["coverage"]["missing"] = ["spatial_placement"]
		template = next(output for output in definition["outputs"] if output["kind"] == "lamp")
		for address, channel in ((900, "blue"), (901, "green"), (902, "red")):
			output = copy.deepcopy(template)
			output["id"] = f"lamp.test-rgb-{address}"
			output["label"] = f"Test RGB {channel}"
			output["availability"] = "used"
			output["binding"] = {"group": "test.rgb", "device": address}
			output["physical"] = {
				"quantity": 2,
				"shared_emitter_group": "rgb.test",
				"emitter_channel": channel,
				"co_located_addresses": [900, 901, 902],
				"shared_physical_quantity": 2,
				"notes": "Three independently controlled channels on one physical RGB emitter group.",
			}
			output["spatial"] = {
				"status": "observed",
				"placements": [
					{
						"id": f"lamp.test-rgb-{address}.emitter",
						"role": "emitter",
						"space": "playfield",
						"x": 0.5,
						"y": 0.5,
						"provenance": copy.deepcopy(template["provenance"]),
					}
				],
			}
			definition["outputs"].append(output)
		return definition

	def test_repository_is_valid(self) -> None:
		self.assertEqual([], validate_repository(ROOT))

	def test_author_ready_display_na_provenance_has_core_and_physical_manual_evidence(self) -> None:
		checked = []
		display_count = 0
		for path in sorted((ROOT / "machines" / "author-ready").rglob("*.json")):
			definition = load_json(path)
			if definition.get("coverage", {}).get("status") != "author_ready":
				continue
			for display in definition.get("displays", []):
				spatial = display.get("spatial")
				display_count += 1
				self.assertIsNotNone(spatial, path.as_posix())
				self.assertEqual("not_applicable", spatial.get("status"), path.as_posix())
				self.assertEqual("cabinet_or_service", spatial.get("reason"), path.as_posix())
				sources = {source["id"]: source for source in definition["sources"]}
				refs = spatial["provenance"]["source_refs"]
				self.assertTrue(any(sources[ref].get("kind") == "pinmame_core" for ref in refs), path.as_posix())
				self.assertTrue(any(sources[ref].get("kind") in {"manual", "human_review"} for ref in refs), path.as_posix())
				checked.append(path)
		self.assertGreater(display_count, 0)
		self.assertEqual(display_count, len(checked))

	def test_author_ready_driver_must_match_containing_physical_definition(self) -> None:
		definition = self.author_ready_fixture()
		definition["drivers"][0]["physical_compatibility"] = "different"
		errors = validate_machine(definition)
		self.assertTrue(any("physically compatible with the containing machine definition" in error for error in errors))

	def display_override_fixture(self) -> dict[str, object]:
		definition = copy.deepcopy(self.transformers)
		driver = definition["drivers"][0]
		driver["physical_compatibility"] = "compatible"
		driver["display_overrides"] = [
			{
				"target": definition["displays"][0]["id"],
				"width": definition["displays"][0].get("width", 128) + 1,
				"provenance": {"status": "validated", "source_refs": [definition["sources"][0]["id"]]},
			}
		]
		return definition

	def test_display_override_accepts_a_canonical_display_target(self) -> None:
		self.assertEqual([], validate_machine(self.display_override_fixture()))

	def test_display_override_rejects_invalid_targets_and_duplicate_targets(self) -> None:
		definition = self.display_override_fixture()
		definition["drivers"][0]["display_overrides"].append(
			{
				"target": definition["displays"][0]["id"],
				"controller_index": 9,
				"provenance": {"status": "validated", "source_refs": [definition["sources"][0]["id"]]},
			}
		)
		for override in definition["drivers"][0]["display_overrides"]:
			override["target"] = "display.not-declared"
		errors = validate_machine(definition)
		self.assertTrue(any("must resolve to a canonical display ID" in error for error in errors))
		self.assertTrue(any("duplicate display override target" in error for error in errors))

	def test_display_override_requires_resolved_validated_provenance_and_nonidentical_driver(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		override["provenance"]["source_refs"] = ["missing.source"]
		definition["drivers"][0]["physical_compatibility"] = "identical"
		errors = validate_machine(definition)
		self.assertTrue(any("unknown source reference 'missing.source'" in error for error in errors))
		self.assertTrue(any("physically identical drivers cannot carry display overrides" in error for error in errors))
		definition = self.author_ready_fixture()
		definition["drivers"][0]["physical_compatibility"] = "compatible"
		definition["drivers"][0]["display_overrides"] = [
			{
				"target": definition["displays"][0]["id"],
				"width": definition["displays"][0].get("width", 128),
				"provenance": {"status": "candidate", "source_refs": [definition["sources"][0]["id"]]},
			}
		]
		errors = validate_machine(definition)
		self.assertTrue(any("author-ready display override provenance must be validated" in error for error in errors))

	def test_display_override_schema_requires_a_dimension_and_rejects_extra_fields(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		del override["width"]
		override["unexpected"] = True
		errors = validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "fixture")
		self.assertTrue(any("is not valid under any of the given schemas" in error for error in errors))
		self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

	def test_segment_start_is_valid_only_for_segment_displays(self) -> None:
		definition = self.display_override_fixture()
		display = definition["displays"][0]
		override = definition["drivers"][0]["display_overrides"][0]
		display["segment_start"] = 2
		override["segment_start"] = 1
		errors = validate_machine(definition)
		self.assertTrue(any("segment_start: is only valid for segment displays" in error for error in errors))
		display["kind"] = "segment"
		del display["height"]
		self.assertEqual([], validate_machine(definition))

	def test_author_ready_segment_displays_require_index_start_and_width(self) -> None:
		definition = self.author_ready_fixture()
		display = definition["displays"][0]
		display["kind"] = "segment"
		del display["height"]
		display["segment_start"] = 2
		errors = validate_machine(definition)
		self.assertTrue(any("segment displays require controller_index, segment_start, and width" in error for error in errors))
		display["controller_index"] = 0
		errors = validate_machine(definition)
		self.assertFalse(any("segment displays require" in error for error in errors))

	def test_display_override_must_change_a_canonical_value(self) -> None:
		definition = self.display_override_fixture()
		override = definition["drivers"][0]["display_overrides"][0]
		override["width"] = definition["displays"][0]["width"]
		errors = validate_machine(definition)
		self.assertTrue(any("must change at least one canonical display value" in error for error in errors))

	def test_virtual_machine_records_and_virtual_only_drivers_are_rejected(self) -> None:
		definition = self.author_ready_fixture()
		definition["machine"]["kind"] = "virtual_pinball"
		definition["drivers"][0]["id"] = "che_cho"
		errors = validate_machine(definition)
		self.assertTrue(any("outside the physical-machine scope" in error and "$.machine.kind" in error for error in errors))
		self.assertTrue(any("outside the physical-machine scope" in error and "$.drivers[0].id" in error for error in errors))

	def test_mechanism_actuator_can_have_only_one_owner(self) -> None:
		definition = self.author_ready_fixture()
		actuator = definition["mechanisms"][0]["actuators"][0]
		definition["mechanisms"][1]["actuators"].append(actuator)
		errors = validate_machine(definition)
		self.assertTrue(any("is already owned" in error for error in errors))

	def test_physical_solenoid_connection_can_have_only_one_owner(self) -> None:
		definition = self.author_ready_fixture()
		physical_outputs = [output for output in definition["outputs"] if output["binding"]["group"] == "pinmame.output.solenoid" and output.get("kind") != "virtual" and output.get("availability") in {"used", "optional"} and output.get("wiring", {}).get("control_connection")]
		physical_outputs[1]["wiring"]["board"] = physical_outputs[0]["wiring"]["board"]
		physical_outputs[1]["wiring"]["control_connection"] = physical_outputs[0]["wiring"]["control_connection"]
		errors = validate_machine(definition)
		self.assertTrue(any("duplicates physical output connection" in error for error in errors))

	def test_shared_rgb_emitter_metadata_is_atomic_and_cross_checked(self) -> None:
		definition = self.shared_rgb_fixture()
		self.assertEqual([], validate_against_schema(definition, ROOT / "schemas" / "machine.schema.json", "shared-rgb"))
		self.assertFalse(any("shared RGB emitter" in error for error in validate_machine(definition)))

		cases = (
			("missing field", lambda value: value["outputs"][-1]["physical"].pop("shared_physical_quantity"), "metadata fields must appear together"),
			("missing sibling", lambda value: value["outputs"][-1]["physical"].update({"co_located_addresses": [900, 901, 999]}), "not present in the same output group"),
			("own address omitted", lambda value: value["outputs"][-3]["physical"].update({"co_located_addresses": [901, 902]}), "own address must be included"),
			("address disagreement", lambda value: value["outputs"][-2]["physical"].update({"co_located_addresses": [900, 901]}), "agree on the complete address set"),
			("group disagreement", lambda value: value["outputs"][-2]["physical"].update({"shared_emitter_group": "rgb.other"}), "agree on shared emitter group identity"),
			("quantity disagreement", lambda value: value["outputs"][-2]["physical"].update({"quantity": 3, "shared_physical_quantity": 3}), "agree on the shared physical quantity"),
			("quantity mismatch", lambda value: value["outputs"][-2]["physical"].update({"quantity": 3}), "must equal shared_physical_quantity"),
			("channel set", lambda value: value["outputs"][-2]["physical"].update({"emitter_channel": "blue"}), "unique exact blue/green/red set"),
			("coordinate mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"x": 0.6}), "equivalent coordinates, roles, and coordinate space"),
			("role mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"role": "effect"}), "equivalent coordinates, roles, and coordinate space"),
			("space mismatch", lambda value: value["outputs"][-2]["spatial"]["placements"][0].update({"space": "backglass"}), "equivalent coordinates, roles, and coordinate space"),
		)
		for name, mutate, expected in cases:
			with self.subTest(name=name):
				invalid = self.shared_rgb_fixture()
				mutate(invalid)
				self.assertTrue(any(expected in error for error in validate_machine(invalid)), name)
		missing = self.shared_rgb_fixture()
		missing["outputs"][-1]["physical"].pop("shared_physical_quantity")
		self.assertTrue(validate_against_schema(missing, ROOT / "schemas" / "machine.schema.json", "shared-rgb-missing-field"))

	def test_author_ready_sam_requires_one_unwired_virtual_game_on_output(self) -> None:
		definition = self.author_ready_fixture()
		definition["outputs"] = [output for output in definition["outputs"] if output["binding"] != {"device": 33, "group": "pinmame.output.solenoid"}]
		self.assertTrue(any("must declare public solenoid 33 exactly once" in error for error in validate_machine(definition)))
		definition = self.author_ready_fixture()
		game_on = next(output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"})
		game_on["kind"] = "coil"
		game_on["wiring"] = {"board": "invented"}
		errors = validate_machine(definition)
		self.assertTrue(any("never a physical device" in error for error in errors))
		self.assertTrue(any("cannot have physical wiring" in error for error in errors))

	def test_runtime_observations_must_map_to_author_ready_outputs(self) -> None:
		definition = self.author_ready_fixture()
		evidence = {"machine_ids": [definition["machine"]["id"]], "runtime": {"observations": {"solenoid_addresses_seen": [999]}}}
		errors: list[str] = []
		_validate_runtime_observations(evidence, "evidence/test.json", {definition["machine"]["id"]: definition}, errors)
		self.assertTrue(any("address 999 is not declared" in error for error in errors))

	def test_current_sam_partials_retain_consistent_game_on_semantics(self) -> None:
		for path in (ROOT / "machines" / "partial" / "stern").rglob("*.json"):
			definition = load_json(path)
			if definition.get("controller", {}).get("platform") != "pinmame.sam":
				continue
			matches = [output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"}]
			self.assertEqual(1, len(matches), path.as_posix())
			self.assertEqual("virtual", matches[0]["kind"], path.as_posix())
			self.assertNotIn("wiring", matches[0], path.as_posix())

	def test_controller_plugin_routes_match_pinmame_contract(self) -> None:
		for filename in ("sam.json", "stern-mpu200.json", "wpc-alpha.json"):
			profile = load_json(ROOT / "controllers" / "pinmame" / filename)
			groups = {group["id"]: group for group in profile["groups"]}
			self.assertEqual(1, groups["pinmame.input.switch"]["transports"]["controller_plugin"]["group_id"])
			self.assertEqual(1, groups["pinmame.output.solenoid"]["transports"]["controller_plugin"]["group_id"])
			self.assertEqual(512, groups["pinmame.output.lamp"]["transports"]["controller_plugin"]["group_id"])
			if "pinmame.output.gi" in groups:
				self.assertEqual(256, groups["pinmame.output.gi"]["transports"]["controller_plugin"]["group_id"])
			if filename == "sam.json":
				self.assertEqual({}, groups["physical.output.ticket"]["transports"])
			self.assertEqual("https://github.com/vpinball/pinmame", profile["sources"][-1]["uri"])


if __name__ == "__main__":
	unittest.main()
