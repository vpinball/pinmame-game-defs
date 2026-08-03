from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "author-ready" / "stern" / "tron-legacy-pro-2011.json"
LE_PATH = ROOT / "machines" / "author-ready" / "stern" / "tron-legacy-limited-edition-2011.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "tron-legacy-pro-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "tron-legacy-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class TronDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.le = load_json(LE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)

	def test_both_physical_editions_are_author_ready_and_replace_partial(self) -> None:
		for definition in (self.pro, self.le):
			self.assertEqual("author_ready", definition["coverage"]["status"])
			self.assertEqual([], definition["coverage"]["missing"])
			self.assertTrue(all(value == "validated" for value in definition["coverage"]["dimensions"].values()))
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "tron-legacy-limited-edition-2011.json").exists())

	def test_supported_driver_family_is_exhaustively_split_by_physical_model(self) -> None:
		pro = {driver["id"] for driver in self.pro["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"trn_110", "trn_120", "trn_140", "trn_150", "trn_160", "trn_170", "trn_174", "trn_17402"}, pro)
		self.assertEqual({"trn_100h", "trn_110h", "trn_130h", "trn_140h", "trn_174h"}, limited_edition)
		self.assertFalse(pro & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("trn_")}, pro | limited_edition)
		self.assertEqual(5682, self.pro["machine"]["ipdb_id"])
		self.assertEqual(5707, self.le["machine"]["ipdb_id"])
		self.assertEqual("I-00B9", self.pro["machine"]["model_number"])
		self.assertEqual("I-00C2", self.le["machine"]["model_number"])

	def test_complete_switch_and_dip_spaces_include_model_differences(self) -> None:
		for definition in (self.pro, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertEqual("unused", switches[33]["availability"])
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertTrue(all(pro[address]["availability"] == "unused" for address in (54, 55, 56)))
		self.assertTrue(all(limited_edition[address]["availability"] == "used" for address in (54, 55, 56)))
		self.assertEqual("used", pro[88]["availability"])
		self.assertEqual("used", pro[87]["availability"])
		self.assertTrue(pro[87]["normally_closed"])
		self.assertEqual("unused", limited_edition[88]["availability"])
		self.assertEqual("unused", limited_edition[87]["availability"])
		self.assertIn("stages the upper-left flipper from the left-flipper control", limited_edition[88]["physical"]["notes"])
		self.assertIn("PDF page 49, D-13", pro[88]["physical"]["notes"])
		self.assertIn("PDF page 55, D-13", limited_edition[88]["physical"]["notes"])
		for switches in (pro, limited_edition):
			self.assertTrue(switches[22]["pulse"])
			for address in (14, 25, 28):
				self.assertFalse(switches[address]["pulse"])
				self.assertEqual("leaf", switches[address]["physical"]["switch_type"])

	def test_main_outputs_are_complete_and_model_specific(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 35)), set(pro))
		self.assertEqual(set(range(1, 35)), set(limited_edition))
		self.assertEqual("Disc direction relay", pro[3]["label"])
		self.assertEqual("TRON four-bank drop-target reset", limited_edition[3]["label"])
		self.assertEqual("Lower left flasher", pro[22]["label"])
		self.assertEqual("Disc direction relay", limited_edition[22]["label"])
		self.assertEqual("Lower right flasher", pro[23]["label"])
		self.assertEqual("Recognizer motor relay", limited_edition[23]["label"])
		self.assertEqual("Left dome flashers x2", limited_edition[19]["label"])
		self.assertEqual("Right dome flashers x2", limited_edition[25]["label"])
		self.assertIn("Resolved source disagreement", limited_edition[19]["physical"]["notes"])
		self.assertEqual("Upper-left flipper", limited_edition[12]["label"])
		self.assertEqual("optional", limited_edition[8]["availability"])
		self.assertEqual("optional", limited_edition[24]["availability"])
		self.assertEqual("virtual", limited_edition[33]["kind"])
		self.assertEqual("unused", limited_edition[34]["availability"])
		self.assertIn("commented-out SolCallback(34)", limited_edition[34]["physical"]["notes"])
		self.assertEqual("J8-P11", limited_edition[9]["wiring"]["control_connection"])
		self.assertNotIn("vpx.tron-legacy-le-vpm-1.1.4", pro[3]["provenance"]["source_refs"])

	def test_lamp_maps_and_tricolor_public_order_are_exact(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.lamp")
		expected_addresses = set(range(1, 81)) | set(range(101, 107))
		self.assertEqual(expected_addresses, set(pro))
		self.assertEqual(expected_addresses, set(limited_edition))
		self.assertEqual(set(range(1, 36)) | set(range(37, 46)) | set(range(48, 54)) | set(range(55, 65)) | {66}, {address for address, lamp in pro.items() if lamp["availability"] == "used"})
		self.assertEqual(set(range(1, 41)) | {42, 43} | set(range(45, 67)) | set(range(101, 107)), {address for address, lamp in limited_edition.items() if lamp["availability"] == "used"})
		self.assertTrue(all(pro[address]["availability"] == "unused" for address in range(101, 107)))
		self.assertEqual(["Right ramp blue", "Right ramp green", "Right ramp red", "Left ramp blue", "Left ramp green", "Left ramp red"], [limited_edition[address]["label"] for address in range(101, 107)])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))
		self.assertNotIn("vpx.tron-legacy-le-vpm-1.1.4", pro[1]["provenance"]["source_refs"])

	def test_custom_mechanisms_are_recreatable_and_not_cross_contaminated(self) -> None:
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertIn("mechanism.tron-standups", pro)
		self.assertNotIn("mechanism.tron-drop-bank", pro)
		self.assertNotIn("mechanism.recognizer-toy", pro)
		self.assertIn("mechanism.tron-drop-bank", limited_edition)
		self.assertIn("mechanism.recognizer-toy", limited_edition)
		self.assertEqual(["device.tron-four-bank-drop-target-reset"], limited_edition["mechanism.tron-drop-bank"]["actuators"])
		self.assertEqual(3, len(limited_edition["mechanism.recognizer-toy"]["positions"]))
		self.assertIn("initializes down on switch 52", limited_edition["mechanism.recognizer-bank"]["behavior"])
		for definition in (pro, limited_edition):
			disc = definition["mechanism.disc"]
			self.assertEqual({"device.disc-motor-power", "device.disc-direction-relay", "device.disc-motor-relay"}, set(disc["actuators"]))
			self.assertIn("carry and throw balls", disc["behavior"])

	def test_manual_script_and_exact_rom_evidence_are_pinned(self) -> None:
		for definition in (self.pro, self.le):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84", sources["manual.tron-legacy-pro-le.2011"]["sha256"])
			self.assertEqual("d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc", sources["vpx.tron-legacy-le-vpm-1.1.4"]["sha256"])
		self.assertEqual("610e8fc71fdd83a94748ebe8691aeaa5964986e2d236ce6b7c46ed13602ff772", self.pro_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("7ae5392a3bf6f9a7d282bf3ca002eea00a84ffd8cf39ff9af2e77a75e0eac44b", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual({101, 102, 103, 104, 105, 106}, set(self.le_evidence["runtime"]["observations"]["lamp_addresses_seen"]) & set(range(101, 107)))
		self.assertFalse(set(self.pro_evidence["runtime"]["observations"]["lamp_addresses_seen"]) & set(range(101, 107)))
		self.assertIn("--initial-switch 52", self.pro_evidence["runtime"]["command_template"])

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
