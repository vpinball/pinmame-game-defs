from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "transformers-pro-2011.json"
LE_PATH = ROOT / "machines" / "partial" / "stern" / "transformers-limited-edition-2011.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "transformers-pro-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "transformers-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class TransformersDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.le = load_json(LE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)

	def test_both_editions_are_fail_closed_for_spatial_retrofit(self) -> None:
		for definition in (self.pro, self.le):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			self.assertIn("spatial_placement", definition["coverage"]["missing"])
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "tf_180h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "tf_180h.md").exists())

	def test_editions_exhaustively_split_the_supported_driver_family(self) -> None:
		pro = {driver["id"] for driver in self.pro["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"tf_120", "tf_140", "tf_150", "tf_160", "tf_170", "tf_180"}, pro)
		self.assertEqual({"tf_088h", "tf_100h", "tf_120h", "tf_130h", "tf_140h", "tf_150h", "tf_180h"}, limited_edition)
		self.assertFalse(pro & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("tf_")}, pro | limited_edition)

	def test_complete_switch_and_dip_address_space_is_explicit(self) -> None:
		for definition in (self.pro, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Right ramp exit", bindings(self.pro, "inputs", "pinmame.input.switch")[14]["label"])
		self.assertEqual("unused", bindings(self.le, "inputs", "pinmame.input.switch")[14]["availability"])
		self.assertEqual("Right ramp exit", bindings(self.le, "inputs", "pinmame.input.switch")[52]["label"])
		self.assertEqual("Starscream left limit", bindings(self.le, "inputs", "pinmame.input.switch")[71]["label"])
		self.assertEqual("unused", bindings(self.pro, "inputs", "pinmame.input.switch")[71]["availability"])
		roles = {role for item in self.pro["inputs"] for role in item.get("roles", [])}
		self.assertTrue({"cabinet.start", "cabinet.coin.left", "cabinet.tilt", "service.back", "service.down", "service.up", "service.enter", "flipper.lower.left.button", "flipper.lower.right.button"} <= roles)

	def test_pro_main_outputs_resolve_the_shared_script_gate_exception(self) -> None:
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(outputs))
		self.assertEqual("unused", outputs[4]["availability"])
		self.assertIn("official Pro chart", outputs[4]["physical"]["notes"])
		self.assertEqual("Orbit control gate", outputs[5]["label"])
		self.assertEqual("Optimus Prime bash solenoid", outputs[12]["label"])
		self.assertEqual("Optimus Prime ramp motor relay", outputs[30]["label"])
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		le_outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual("J16-P4", le_outputs[24]["wiring"]["power_connection"])
		self.assertEqual(20, le_outputs[24]["wiring"]["nominal_voltage_v"])

	def test_le_auxiliary_board_serialization_is_explicit(self) -> None:
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(outputs))
		self.assertTrue(all(outputs[address]["availability"] == "unused" for address in set(range(51, 59)) | {65, 66}))
		self.assertEqual("Q41", outputs[59]["wiring"]["driver_transistor"])
		self.assertEqual("Q46", outputs[64]["wiring"]["driver_transistor"])
		self.assertEqual("Starscream platform motor", outputs[59]["label"])
		self.assertEqual("Optimus Prime bash solenoid", outputs[62]["label"])
		self.assertEqual("Ironhide mini-playfield left", outputs[63]["label"])

	def test_lamp_matrices_are_complete_and_edition_specific(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(pro))
		self.assertEqual(set(range(1, 81)), set(limited_edition))
		self.assertEqual({56} | set(range(63, 81)), {address for address, lamp in pro.items() if lamp["availability"] == "unused"})
		self.assertEqual(set(range(1, 17)) | {60}, {address for address, lamp in limited_edition.items() if lamp["availability"] == "unused"})
		self.assertEqual("Megatron bottom", pro[57]["label"])
		self.assertEqual("Ironhide mini-playfield 1", limited_edition[59]["label"])
		self.assertEqual("Start button", limited_edition[80]["label"])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_capture_complete_causality(self) -> None:
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertIn("four-position vertical mini-trough", pro["mechanism.megatron-lock"]["behavior"])
		self.assertEqual([["switch.optimus-ramp-down"], ["switch.optimus-ramp-up"]], [position["sensors"] for position in pro["mechanism.optimus-ramp"]["positions"]])
		self.assertEqual(["device.orbit-control-gate"], pro["mechanism.orbit-gate"]["actuators"])
		self.assertNotIn("mechanism.starscream", pro)
		self.assertEqual(["switch.starscream-left-limit", "switch.starscream-right-limit", "switch.starscream-target"], limited_edition["mechanism.starscream"]["sensors"])
		self.assertEqual("511-6979-00", limited_edition["mechanism.starscream"]["assembly_part_number"])
		self.assertEqual(4, len(limited_edition["mechanism.ironhide-mini-playfield"]["sensors"]))
		self.assertIn("does not physically travel through the cannon", limited_edition["mechanism.megatron-figure-and-cannon"]["behavior"])
		actuators = [actuator for mechanism in limited_edition.values() for actuator in mechanism["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))

	def test_source_and_exact_rom_hash_constants_are_pinned(self) -> None:
		pro_sources = {source["id"]: source for source in self.pro["sources"]}
		le_sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8", pro_sources["manual.transformers-pro-le.2011"]["sha256"])
		self.assertEqual("9a4ff4cc3f5391bf730d226eb969c855c7c8c0f429c33e66d846d4069c7898b8", le_sources["manual.transformers-pro-le.2011"]["sha256"])
		self.assertEqual("987b8cae80fbe6cb00c652507fba2eaf422afef8a57852a7e4c59d5b3f9e157b", pro_sources["vpx.transformers-pro-vpw-2.3.1"]["sha256"])
		self.assertEqual("8689f01315ad4f6b7001c7a99147093c64297631104610a7ac03e34152e8f352", self.pro_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("5f7c0caa85b1b5b8799e6cceef8e7d9ec7d9ddd63f0b8364ab5e9168c88443da", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("0ce389603bb0ccc237e71937ddadb8a5534f2499fdf610f6ec4087bdf29d22f4", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("b3a32d9033023bc9c3d2d36b32f56645e5f002225f43f2fdbe4779b81b6045f7", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		for evidence in (self.pro_evidence, self.le_evidence):
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], evidence["runtime"]["observations"]["display_layouts_seen"])

	def test_every_runtime_observation_resolves_to_a_declared_output(self) -> None:
		for definition, evidence in ((self.pro, self.pro_evidence), (self.le, self.le_evidence)):
			groups = {
				"solenoid_addresses_seen": bindings(definition, "outputs", "pinmame.output.solenoid"),
				"lamp_addresses_seen": bindings(definition, "outputs", "pinmame.output.lamp"),
				"gi_addresses_seen": bindings(definition, "outputs", "pinmame.output.gi"),
			}
			for observation, declared in groups.items():
				self.assertFalse(set(evidence["runtime"]["observations"][observation]) - set(declared), observation)

	def test_bindings_and_semantic_ids_are_unique(self) -> None:
		for definition in (self.pro, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
	unittest.main()
