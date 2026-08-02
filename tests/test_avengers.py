from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LE_PATH = ROOT / "machines" / "author-ready" / "stern" / "avengers-limited-edition-2012.json"
PRO_PATH = ROOT / "machines" / "author-ready" / "stern" / "avengers-pro-2012.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avengers-limited-edition-boot-start.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avengers-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


class AvengersDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.le = load_json(LE_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)

	def test_both_physical_editions_are_author_ready_and_driver_sets_do_not_overlap(self) -> None:
		self.assertEqual("author_ready", self.le["coverage"]["status"])
		self.assertEqual("author_ready", self.pro["coverage"]["status"])
		self.assertEqual([], self.le["coverage"]["missing"])
		self.assertEqual([], self.pro["coverage"]["missing"])
		le_drivers = {driver["id"] for driver in self.le["drivers"]}
		pro_drivers = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"avs_120h", "avs_140h", "avs_170h", "avs_170hc"}, le_drivers)
		self.assertEqual({"avs_110", "avs_140", "avs_170", "avs_170c"}, pro_drivers)
		self.assertFalse(le_drivers & pro_drivers)

	def test_complete_switch_and_dip_spaces_are_explicit(self) -> None:
		for definition in (self.le, self.pro):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertEqual(96, len(definition["inputs"]))

	def test_model_specific_switch_topology_is_not_shared(self) -> None:
		le = bindings(self.le, "inputs", "pinmame.input.switch")
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual("Trough #6 left", le[17]["label"])
		self.assertEqual("Trough jam", le[23]["label"])
		self.assertEqual("Shooter lane", le[86]["label"])
		self.assertEqual("Right orbit", le[58]["label"])
		self.assertEqual("Bridge motor down", le[8]["label"])
		self.assertEqual("unused", pro[17]["availability"])
		self.assertEqual("Shooter lane", pro[23]["label"])
		self.assertEqual("unused", pro[86]["availability"])
		self.assertEqual("Right orbit", pro[61]["label"])
		self.assertEqual("unused", pro[58]["availability"])
		self.assertEqual("unused", pro[8]["availability"])

	def test_le_auxiliary_public_addresses_preserve_physical_driver_numbers(self) -> None:
		le = bindings(self.le, "outputs", "pinmame.output.solenoid")
		pro = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 59)), set(le))
		self.assertEqual(set(range(1, 34)) | {53, 54}, set(pro))
		self.assertEqual("virtual", le[33]["kind"])
		self.assertEqual("virtual", pro[33]["kind"])
		self.assertNotIn("wiring", le[33])
		self.assertTrue(all(pro[address]["kind"] == "virtual" and pro[address]["availability"] == "unused" for address in (53, 54)))
		for public, physical in zip(range(51, 59), range(41, 49)):
			manual_alias = next(alias["value"] for alias in le[public]["aliases"] if alias["namespace"] == "manual.address")
			self.assertEqual(str(physical), manual_alias)
			self.assertEqual("520-5325-00 eight-transistor auxiliary driver board", le[public]["wiring"]["board"])
		self.assertEqual("Center 4-bank drop reset", le[51]["label"])
		self.assertEqual("Hulk magnet", le[54]["label"])
		self.assertEqual("Hulk arms", le[56]["label"])
		self.assertEqual("Right orbit control gate", le[57]["label"])
		self.assertEqual("Center 4-bank drop reset", pro[6]["label"])
		self.assertEqual("Left ramp control gate", pro[12]["label"])
		self.assertEqual("Hulk arms", pro[17]["label"])
		self.assertEqual("Loki lockup", pro[22]["label"])
		self.assertEqual("Hulk magnet", pro[23]["label"])

	def test_lamp_matrices_are_complete_and_edition_specific(self) -> None:
		le = bindings(self.le, "outputs", "pinmame.output.lamp")
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(le))
		self.assertEqual(set(range(1, 81)), set(pro))
		self.assertEqual({13, 69, 70, 71, 79}, {address for address, item in le.items() if item["availability"] == "unused"})
		self.assertEqual({40, 56, 59, 64, 72, 74, 76, 77, 79, 80}, {address for address, item in pro.items() if item["availability"] == "unused"})
		self.assertEqual("THO(R)", le[1]["label"])
		self.assertEqual("Start button", pro[1]["label"])
		self.assertEqual("Right orbit red", le[80]["label"])
		self.assertEqual("Right orbit red", pro[53]["label"])

	def test_troughs_and_custom_mechanisms_capture_recreation_behavior(self) -> None:
		le = {item["id"]: item for item in self.le["mechanisms"]}
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		self.assertIn("6-ball", le["mechanism.trough"]["label"])
		self.assertEqual(7, len(le["mechanism.trough"]["sensors"]))
		self.assertIn("4-ball", pro["mechanism.trough"]["label"])
		self.assertEqual(5, len(pro["mechanism.trough"]["sensors"]))
		self.assertTrue({"mechanism.bridge", "mechanism.thor-drop-bank", "mechanism.rgb-gi-relays", "mechanism.hulk-magnet", "mechanism.loki-lock", "mechanism.tesseract-spinner"}.issubset(le))
		self.assertNotIn("mechanism.bridge", pro)
		self.assertNotIn("mechanism.rgb-gi-relays", pro)
		self.assertIn("mechanism.thor-target-bank", pro)
		self.assertEqual([], pro["mechanism.thor-target-bank"]["actuators"])
		self.assertEqual([], le["mechanism.tesseract-spinner"]["actuators"])
		self.assertEqual([], pro["mechanism.tesseract-spinner"]["actuators"])
		self.assertEqual(3, len(le["mechanism.loki-lock"]["positions"]))
		self.assertEqual(3, len(pro["mechanism.loki-lock"]["positions"]))

	def test_exact_rom_runs_anchor_display_gi_and_clone_root_artifact(self) -> None:
		le_runtime = self.le_evidence["runtime"]
		pro_runtime = self.pro_evidence["runtime"]
		self.assertEqual("a5ea0eafcc45671ce66b29336c81f875f49515235034520f53e3042dfdefc74d", le_runtime["rom_archive_sha256"])
		self.assertEqual("5bf37fe0f4a7a101d941de3659dd29dd9913b01f020d3202d644a86ed8802cc3", pro_runtime["rom_archive_sha256"])
		self.assertEqual("3fdb8e048c0c8ff130163333e508953b6ec3bfb0670931af9cbddc957c011bd3", le_runtime["raw_runs"][0]["sha256"])
		self.assertEqual("4fa936ed6307059ef69f17100390a96ef91b9a28a65346d6ca8f45e1823122d6", pro_runtime["raw_runs"][0]["sha256"])
		for runtime in (le_runtime, pro_runtime):
			self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		self.assertEqual([24, 53, 54], pro_runtime["observations"]["solenoid_addresses_seen"])
		pro_outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertTrue(all(pro_outputs[address]["kind"] == "virtual" and pro_outputs[address]["availability"] == "unused" for address in (53, 54)))

	def test_sources_are_hash_anchored_and_stub_is_replaced(self) -> None:
		le_sources = {source["id"]: source for source in self.le["sources"]}
		pro_sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("4687ae0ed0ac249411deff3b0284d5c13d8fab154e430e95b6bd9f7bb82dca62", le_sources["manual.avengers-limited-edition"]["sha256"])
		self.assertEqual("c6da231a360a0f062fa5b434d08faca3c1b7b6a5436cc51b5b54dac924e1a3b4", le_sources["vpx.avengers-le.jp-salas-v600"]["sha256"])
		self.assertEqual("fdabec154947bc814d1b172fe68e91ad440780282c759f71668cfe7754f50031", pro_sources["manual.avengers-pro"]["sha256"])
		self.assertEqual("85ea928246dbdf4b59a73e5237b6d248970770d3146381b06a1620c92cba21e8", pro_sources["vpx.avengers-pro.vpw-1-3-1"]["sha256"])
		self.assertFalse((ROOT / "machines" / "stubs" / "avs_170h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "avs_170h.md").exists())
		self.assertEqual("complete", self.le["knowledge"]["status"])
		self.assertEqual("complete", self.pro["knowledge"]["status"])


if __name__ == "__main__":
	unittest.main()
