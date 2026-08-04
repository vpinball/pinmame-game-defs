from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-rolling-stones-standard-2011.json"
LE_PATH = ROOT / "machines" / "partial" / "stern" / "the-rolling-stones-limited-edition-2011.json"
STANDARD_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "rolling-stones-standard-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "rolling-stones-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class RollingStonesDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.standard = load_json(STANDARD_PATH)
		cls.le = load_json(LE_PATH)
		cls.standard_evidence = load_json(STANDARD_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)

	def test_standard_is_spatially_ready_and_le_remains_fail_closed(self) -> None:
		self.assertEqual(2, self.standard["schema_version"])
		self.assertEqual("author_ready", self.standard["coverage"]["status"])
		self.assertEqual([], self.standard["coverage"]["missing"])
		self.assertEqual("validated", self.standard["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(2, self.le["schema_version"])
		self.assertEqual("partial", self.le["coverage"]["status"])
		self.assertIn("spatial_placement", self.le["coverage"]["missing"])
		for definition in (self.standard, self.le):
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "rsn_110h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "rsn_110h.md").exists())

	def test_standard_spatial_inventory_is_complete_and_excludes_le_only_hardware(self) -> None:
		for collection in (self.standard["inputs"], self.standard["outputs"]):
			self.assertTrue(all("spatial" in device for device in collection))
			self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in collection))
		self.assertEqual("not_applicable", self.standard["displays"][0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.standard["displays"][0]["spatial"]["reason"])
		outputs = bindings(self.standard, "outputs", "pinmame.output.solenoid")
		switches = bindings(self.standard, "inputs", "pinmame.input.switch")
		self.assertEqual((0.4745, 0.9745), (switches[18]["spatial"]["placements"][0]["x"], switches[18]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.5385, 0.9775), (switches[19]["spatial"]["placements"][0]["x"], switches[19]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.727167, 0.982), (switches[22]["spatial"]["placements"][0]["x"], switches[22]["spatial"]["placements"][0]["y"]))
		self.assertNotEqual((0.664, 0.979), (switches[22]["spatial"]["placements"][0]["x"], switches[22]["spatial"]["placements"][0]["y"]))
		self.assertIn("disclosed", switches[22]["physical"]["notes"])
		self.assertEqual("not_applicable", switches[82]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[82]["spatial"]["reason"])
		self.assertEqual("not_applicable", switches[84]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[84]["spatial"]["reason"])
		for address in (81, 83):
			self.assertEqual("validated", switches[address]["spatial"]["status"])
			self.assertIn("hidden-switch convention", switches[address]["physical"]["notes"])
			self.assertEqual(1, len(switches[address]["spatial"]["placements"]))
		self.assertEqual((0.664, 0.979), (outputs[1]["spatial"]["placements"][0]["x"], outputs[1]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.916, 0.92625), (outputs[2]["spatial"]["placements"][0]["x"], outputs[2]["spatial"]["placements"][0]["y"]))
		self.assertTrue(all(outputs[address]["spatial"]["reason"] == "cabinet_or_service" for address in (20, 21)))
		for address in (5, 7, 17, 29, 30, 32):
			self.assertEqual("unused", outputs[address]["spatial"]["reason"])
		self.assertEqual(7, len(bindings(self.standard, "inputs", "pinmame.input.switch")[72]["spatial"]["placements"]))
		for address in (25, 27, 28):
			self.assertEqual(1, outputs[address]["physical"]["quantity"])
			self.assertEqual(1, len(outputs[address]["spatial"]["placements"]))
			self.assertIn("synchronized LE render layers", outputs[address]["physical"]["notes"])
		gi = bindings(self.standard, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(40, len(gi["spatial"]["placements"]))
		self.assertEqual(40, gi["physical"]["quantity"])
		lamp20 = bindings(self.standard, "outputs", "pinmame.output.lamp")[20]["spatial"]["placements"][0]
		self.assertNotIn((lamp20["x"], lamp20["y"]), {(point["x"], point["y"]) for point in gi["spatial"]["placements"]})
		sources = {source["id"]: source for source in self.standard["sources"]}
		self.assertEqual("vpx_table", sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["kind"])
		self.assertFalse(sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["known_working"])
		self.assertIn("LE-only", sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["locator"])
		self.assertIn("rsn_110h", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertIn("disqualified", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertNotIn("exact-looking", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertNotIn("inaccessible", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])

	def test_editions_exhaustively_split_the_supported_driver_family(self) -> None:
		standard = {driver["id"] for driver in self.standard["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"rsn_103", "rsn_105", "rsn_110"}, standard)
		self.assertEqual({"rsn_100h", "rsn_110h"}, limited_edition)
		self.assertFalse(standard & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("rsn_")}, standard | limited_edition)
		self.assertEqual(5668, self.standard["machine"]["ipdb_id"])
		self.assertEqual(5708, self.le["machine"]["ipdb_id"])

	def test_complete_switch_and_dip_address_space_is_explicit(self) -> None:
		for definition in (self.standard, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertEqual("Moving Mick target hit", switches[72]["label"])
			self.assertTrue(switches[72]["pulse"])
		standard = bindings(self.standard, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertEqual("unused", standard[17]["availability"])
		self.assertEqual("used", limited_edition[17]["availability"])
		self.assertEqual("unused", standard[50]["availability"])
		self.assertEqual("used", limited_edition[50]["availability"])
		self.assertEqual("Magnetic ball detector", limited_edition[71]["label"])
		self.assertTrue(limited_edition[71]["normally_closed"])
		self.assertEqual("unused", standard[71]["availability"])
		self.assertIn("must not build a second start switch", standard[14]["physical"]["notes"])
		self.assertIn("vpx.rolling-stones-le-1.0.6i", standard[14]["provenance"]["source_refs"])

	def test_premium_real_and_virtual_cabinet_inputs_are_distinguished(self) -> None:
		standard = bindings(self.standard, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertTrue(all(standard[address]["availability"] == "unused" for address in (85, 86, 87, 88)))
		self.assertEqual("switch", limited_edition[88]["kind"])
		self.assertEqual("switch", limited_edition[86]["kind"])
		self.assertEqual("virtual", limited_edition[87]["kind"])
		self.assertEqual("virtual", limited_edition[85]["kind"])
		self.assertNotIn("switch_type", limited_edition[87]["physical"])
		self.assertNotIn("switch_type", limited_edition[85]["physical"])
		self.assertIn("must not build", limited_edition[87]["physical"]["notes"])
		self.assertIn("must not build", limited_edition[85]["physical"]["notes"])

	def test_main_outputs_are_complete_and_edition_specific(self) -> None:
		standard = bindings(self.standard, "outputs", "pinmame.output.solenoid")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(standard))
		self.assertEqual(set(range(1, 34)), set(limited_edition))
		edition_only = {5, 7, 17, 29, 30, 32}
		self.assertTrue(all(standard[address]["availability"] == "unused" for address in edition_only))
		self.assertTrue(all(limited_edition[address]["availability"] == "used" for address in edition_only))
		self.assertEqual("magnet", limited_edition[5]["kind"])
		self.assertEqual("magnet", limited_edition[7]["kind"])
		self.assertEqual("unused", standard[12]["availability"])
		self.assertEqual("optional", standard[8]["availability"])
		self.assertEqual("optional", standard[24]["availability"])
		self.assertEqual(5, standard[24]["wiring"]["nominal_voltage_v"])
		self.assertEqual("virtual", standard[33]["kind"])
		self.assertNotIn("wiring", standard[33])
		self.assertEqual("J8-P11", standard[9]["wiring"]["control_connection"])

	def test_lamp_matrix_and_general_illumination_are_complete(self) -> None:
		used = set(range(1, 54)) | {58, 60, 61, 62}
		for definition in (self.standard, self.le):
			lamps = bindings(definition, "outputs", "pinmame.output.lamp")
			self.assertEqual(set(range(1, 81)), set(lamps))
			self.assertEqual(used, {address for address, lamp in lamps.items() if lamp["availability"] == "used"})
			self.assertEqual("Mick position 1 home", lamps[53]["label"])
			self.assertEqual("unused", lamps[54]["availability"])
			self.assertIn("no Mick-position-5", lamps[54]["physical"]["notes"])
			self.assertEqual({0}, set(bindings(definition, "outputs", "pinmame.output.gi")))

	def test_moving_mick_causality_is_complete(self) -> None:
		for definition in (self.standard, self.le):
			mechanisms = {item["id"]: item for item in definition["mechanisms"]}
			mick = mechanisms["mechanism.moving-mick"]
			self.assertEqual(["device.mick-motor-relay-left", "device.mick-motor-relay-right"], mick["actuators"])
			self.assertEqual(8, len(mick["sensors"]))
			self.assertEqual(7, len(mick["positions"]))
			self.assertIn("share dedicated hit switch 72", mick["behavior"])
			self.assertIn("-27..+36 degrees", mick["behavior"])
			self.assertEqual(["switch.mick-position-5-park"], mick["positions"][4]["sensors"])

	def test_le_ceramic_ball_and_magnetized_diverter_are_recreatable(self) -> None:
		standard = {item["id"]: item for item in self.standard["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertNotIn("mechanism.magnetic-ball-diverter", standard)
		self.assertNotIn("mechanism.ceramic-ball", standard)
		diverter = limited_edition["mechanism.magnetic-ball-diverter"]
		self.assertEqual({"device.left-magnet", "device.right-magnet", "device.left-up-down-post", "device.center-up-down-post", "device.right-up-down-post"}, set(diverter["actuators"]))
		self.assertIn("Public 87/85", diverter["behavior"])
		ceramic = limited_edition["mechanism.ceramic-ball"]
		self.assertIn("preserves its identity", ceramic["behavior"])
		self.assertIn("restores it after shooter switch 23 clears", ceramic["behavior"])

	def test_source_and_exact_rom_hash_constants_are_pinned(self) -> None:
		for definition in (self.standard, self.le):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf", sources["manual.rolling-stones-standard-le.2011"]["sha256"])
			self.assertEqual("969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033", sources["vpx.rolling-stones-le-1.0.6i"]["sha256"])
		self.assertEqual("1d17d6faf937bfa583e7c8f0a822bc9db0aee74b205f043f9068fbcff58bb563", self.standard_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59", self.standard_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("cd01ff42364505034e9bdaabf211852a8ecc6ae499371840687e8297abfcaadf", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		for evidence in (self.standard_evidence, self.le_evidence):
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], evidence["runtime"]["observations"]["display_layouts_seen"])
			self.assertEqual({1} | set(range(3, 54)) | {58, 60, 61, 62}, set(evidence["runtime"]["observations"]["lamp_addresses_seen"]))
		self.assertIn("<external-json>", self.standard_evidence["runtime"]["command_template"])
		self.assertNotIn("E:\\", self.standard_evidence["runtime"]["command_template"])
		self.assertNotIn("L:\\", self.standard_evidence["runtime"]["command_template"])

	def test_every_runtime_observation_resolves_to_a_declared_output(self) -> None:
		for definition, evidence in ((self.standard, self.standard_evidence), (self.le, self.le_evidence)):
			groups = {
				"solenoid_addresses_seen": bindings(definition, "outputs", "pinmame.output.solenoid"),
				"lamp_addresses_seen": bindings(definition, "outputs", "pinmame.output.lamp"),
				"gi_addresses_seen": bindings(definition, "outputs", "pinmame.output.gi"),
			}
			for observation, declared in groups.items():
				self.assertFalse(set(evidence["runtime"]["observations"][observation]) - set(declared), observation)

	def test_bindings_and_semantic_ids_are_unique(self) -> None:
		for definition in (self.standard, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
	unittest.main()
