from __future__ import annotations

import copy
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import _validate_runtime_observations, validate_machine, validate_repository


ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.transformers = load_json(ROOT / "machines" / "author-ready" / "stern" / "transformers-limited-edition-2011.json")

	def test_repository_is_valid(self) -> None:
		self.assertEqual([], validate_repository(ROOT))

	def test_author_ready_driver_must_match_containing_physical_definition(self) -> None:
		definition = copy.deepcopy(self.transformers)
		definition["drivers"][0]["physical_compatibility"] = "different"
		errors = validate_machine(definition)
		self.assertTrue(any("physically compatible with the containing machine definition" in error for error in errors))

	def test_virtual_machine_records_and_virtual_only_drivers_are_rejected(self) -> None:
		definition = copy.deepcopy(self.transformers)
		definition["machine"]["kind"] = "virtual_pinball"
		definition["drivers"][0]["id"] = "che_cho"
		errors = validate_machine(definition)
		self.assertTrue(any("outside the physical-machine scope" in error and "$.machine.kind" in error for error in errors))
		self.assertTrue(any("outside the physical-machine scope" in error and "$.drivers[0].id" in error for error in errors))

	def test_mechanism_actuator_can_have_only_one_owner(self) -> None:
		definition = copy.deepcopy(self.transformers)
		actuator = definition["mechanisms"][0]["actuators"][0]
		definition["mechanisms"][1]["actuators"].append(actuator)
		errors = validate_machine(definition)
		self.assertTrue(any("is already owned" in error for error in errors))

	def test_physical_solenoid_connection_can_have_only_one_owner(self) -> None:
		definition = copy.deepcopy(self.transformers)
		physical_outputs = [output for output in definition["outputs"] if output["binding"]["group"] == "pinmame.output.solenoid" and output.get("kind") != "virtual" and output.get("availability") in {"used", "optional"} and output.get("wiring", {}).get("control_connection")]
		physical_outputs[1]["wiring"]["board"] = physical_outputs[0]["wiring"]["board"]
		physical_outputs[1]["wiring"]["control_connection"] = physical_outputs[0]["wiring"]["control_connection"]
		errors = validate_machine(definition)
		self.assertTrue(any("duplicates physical output connection" in error for error in errors))

	def test_author_ready_sam_requires_one_unwired_virtual_game_on_output(self) -> None:
		definition = copy.deepcopy(self.transformers)
		definition["outputs"] = [output for output in definition["outputs"] if output["binding"] != {"device": 33, "group": "pinmame.output.solenoid"}]
		self.assertTrue(any("must declare public solenoid 33 exactly once" in error for error in validate_machine(definition)))
		definition = copy.deepcopy(self.transformers)
		game_on = next(output for output in definition["outputs"] if output["binding"] == {"device": 33, "group": "pinmame.output.solenoid"})
		game_on["kind"] = "coil"
		game_on["wiring"] = {"board": "invented"}
		errors = validate_machine(definition)
		self.assertTrue(any("never a physical device" in error for error in errors))
		self.assertTrue(any("cannot have physical wiring" in error for error in errors))

	def test_runtime_observations_must_map_to_author_ready_outputs(self) -> None:
		evidence = {"machine_ids": [self.transformers["machine"]["id"]], "runtime": {"observations": {"solenoid_addresses_seen": [999]}}}
		errors: list[str] = []
		_validate_runtime_observations(evidence, "evidence/test.json", {self.transformers["machine"]["id"]: self.transformers}, errors)
		self.assertTrue(any("address 999 is not declared" in error for error in errors))

	def test_every_author_ready_sam_definition_has_consistent_game_on_semantics(self) -> None:
		for path in (ROOT / "machines" / "author-ready").rglob("*.json"):
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
