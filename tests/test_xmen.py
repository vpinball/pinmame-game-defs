from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LE_PATH = ROOT / "machines" / "author-ready" / "stern" / "x-men-limited-edition-2012.json"
PRO_PATH = ROOT / "machines" / "author-ready" / "stern" / "x-men-pro-2012.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "x-men-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class XMenDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.le = load_json(LE_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_both_editions_are_author_ready(self) -> None:
		for definition in (self.le, self.pro):
			self.assertEqual("author_ready", definition["coverage"]["status"])
			self.assertEqual([], definition["coverage"]["missing"])
			self.assertTrue(all(value == "validated" for value in definition["coverage"]["dimensions"].values()))
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "x-men-le-2012.json").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "x-men-pro-2012.json").exists())

	def test_editions_split_every_supported_xmen_driver(self) -> None:
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		pro = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"xmn_102", "xmn_120h", "xmn_121h", "xmn_122h", "xmn_123h", "xmn_124h", "xmn_130h", "xmn_150h", "xmn_151h", "xmn_151hc"}, limited_edition)
		self.assertEqual({"xmn_100", "xmn_104", "xmn_105", "xmn_130", "xmn_150", "xmn_151", "xmn_151c"}, pro)
		self.assertFalse(limited_edition & pro)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("xmn_")}, limited_edition | pro)

	def test_switch_inventory_is_complete_and_marks_le_only_hardware(self) -> None:
		for definition in (self.le, self.pro):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Iceman home", bindings(self.le, "inputs", "pinmame.input.switch")[34]["label"])
		self.assertEqual("Right Nightcrawler down", bindings(self.le, "inputs", "pinmame.input.switch")[56]["label"])
		pro_switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertTrue(all(pro_switches[address]["availability"] == "unused" for address in (12, 34, 35, 50, 51, 56)))

	def test_le_main_auxiliary_and_virtual_outputs_are_distinct(self) -> None:
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 59)), set(outputs))
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		self.assertEqual("Q41", outputs[51]["wiring"]["driver_transistor"])
		self.assertEqual("Q48", outputs[58]["wiring"]["driver_transistor"])
		self.assertEqual("ORG-BLU", outputs[56]["wiring"]["control_wire"])
		self.assertEqual("Iceman ramp motor", outputs[27]["label"])
		self.assertEqual("Disc motor power", outputs[23]["label"])

	def test_le_lamp_matrix_and_gi_are_complete(self) -> None:
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		expected_unused = set(range(1, 17)) | {40, 44, 61, 62, 63, 64}
		self.assertEqual(expected_unused, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("Dark Phoenix", lamps[45]["label"])
		self.assertEqual("Magneto green", lamps[65]["label"])
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_capture_sensor_and_actuator_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertEqual(["device.magneto-magnet", "device.disc-motor-power"], mechanisms["mechanism.magneto-disc"]["actuators"])
		self.assertIn("no index or home switch exists", mechanisms["mechanism.magneto-disc"]["behavior"])
		self.assertEqual(["switch.iceman-home", "switch.iceman-away"], mechanisms["mechanism.iceman-ramp"]["sensors"])
		self.assertEqual([["switch.iceman-home"], ["switch.iceman-away"]], [position["sensors"] for position in mechanisms["mechanism.iceman-ramp"]["positions"]])
		self.assertEqual([], mechanisms["mechanism.left-nightcrawler"]["positions"][1]["sensors"])
		self.assertIn("mechanically", mechanisms["mechanism.left-nightcrawler"]["behavior"])
		self.assertIn("255 minus the output value", mechanisms["mechanism.color-gi"]["behavior"])
		self.assertEqual(["switch.center-lock-1-bottom", "switch.center-lock-2", "switch.center-lock-3", "switch.center-lock-4-top"], mechanisms["mechanism.center-lock"]["sensors"])

	def test_pro_excludes_le_auxiliary_devices_and_preserves_known_difference(self) -> None:
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(outputs))
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		self.assertEqual("Wolverine magnet", outputs[32]["label"])
		self.assertFalse(set(range(51, 59)) & set(outputs))
		mechanisms = {item["id"] for item in self.pro["mechanisms"]}
		self.assertFalse({"mechanism.iceman-ramp", "mechanism.left-nightcrawler", "mechanism.right-nightcrawler", "mechanism.magneto-disc", "mechanism.color-gi"} & mechanisms)

	def test_pro_lamp_matrix_is_complete_semantic_and_hash_locked(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		expected_used = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 60, 61, 62, 65, 66, 67, 68, 69, 70, 71}
		self.assertEqual(expected_used, {address for address, lamp in lamps.items() if lamp["availability"] == "used"})
		self.assertEqual("Left Nightcrawler feature insert", lamps[11]["label"])
		self.assertEqual("Magneto completion medallion right", lamps[49]["label"])
		self.assertEqual("Bottom pop bumper", lamps[62]["label"])
		self.assertIn("x=742.9, y=1130.5", lamps[49]["physical"]["location"])
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8", sources["vpx-table.x-men-pro-physmod5"]["sha256"])

	def test_sources_and_exact_rom_run_are_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("0812b91d0950ff8c1b15c5bc17afc827029ca8aaaa0bbb78cc11ea606b629bf8", sources["manual.x-men-pro-le.2012"]["sha256"])
		self.assertEqual("d793836fefab6c0de53463943e36245c7ed800d5ca86675e3c2b2f46df693643", sources["manual.x-men-pro-le.2012.high-resolution"]["sha256"])
		self.assertEqual("6d445e52398640bd35a498553bb0ba32f1b9ce23e2964d0694c18ff2e9225650", sources["vpx.x-men-le-vpw-1.0.6"]["sha256"])
		runtime = self.evidence["runtime"]
		self.assertEqual("xmn_151h", runtime["game"])
		self.assertEqual("cc8069743e6a0f45c3b310c0804230241739b5cf8c51f0481d96810f9edab5be", runtime["rom_archive_sha256"])
		self.assertEqual("72730b25d7cec239eac1d8df6039f0c465e2c729070d49acebec8d22aa5cb61c", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])

	def test_bindings_are_unique_within_each_controller_group(self) -> None:
		for definition in (self.le, self.pro):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))


if __name__ == "__main__":
	unittest.main()
