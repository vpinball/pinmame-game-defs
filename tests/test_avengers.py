from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LE_PATH = ROOT / "machines" / "partial" / "stern" / "avengers-limited-edition-2012.json"
PRO_PATH = ROOT / "machines" / "author-ready" / "stern" / "avengers-pro-2012.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avengers-limited-edition-boot-start.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avengers-pro-boot-start.json"
PRO_SCRIPT_EVIDENCE_PATH = ROOT / "evidence" / "vpx" / "vpxtable-scripts" / "avs_170c" / "85ea928246dbdf4b.json"


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
		cls.pro_script_evidence = load_json(PRO_SCRIPT_EVIDENCE_PATH)

	def test_only_pro_is_promoted_after_spatial_reconciliation(self) -> None:
		self.assertEqual("partial", self.le["coverage"]["status"])
		self.assertEqual("author_ready", self.pro["coverage"]["status"])
		self.assertEqual(2, self.le["schema_version"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertIn("spatial_placement", self.le["coverage"]["missing"])
		self.assertEqual([], self.pro["coverage"]["missing"])
		self.assertEqual("validated", self.pro["coverage"]["dimensions"]["spatial_placement"])
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

	def test_pro_spatial_dispositions_cover_every_device_and_preserve_physical_multiplicity(self) -> None:
		pro_inputs = bindings(self.pro, "inputs", "pinmame.input.switch")
		pro_outputs = {
			(item["binding"]["group"], item["binding"]["device"]): item
			for item in self.pro["outputs"]
		}
		for device in [*self.pro["inputs"], *self.pro["outputs"]]:
			self.assertIn("spatial", device)
			self.assertIn(device["spatial"]["status"], {"validated", "not_applicable"})
			if device["spatial"]["status"] == "validated":
				for placement in device["spatial"]["placements"]:
					self.assertEqual("playfield", placement["space"])
					self.assertTrue(0 <= placement["x"] <= 1)
					self.assertTrue(0 <= placement["y"] <= 1)
		trough_positions = {
			address: [(placement["x"], placement["y"]) for placement in pro_inputs[address]["spatial"]["placements"]]
			for address in (18, 19, 20, 21, 22)
		}
		self.assertEqual({18, 19, 20, 21, 22}, {address for address, item in pro_inputs.items() if item["spatial"]["status"] == "validated" and address in {18, 19, 20, 21, 22}})
		self.assertEqual([(0.532206, 0.948554)], trough_positions[18])
		self.assertEqual([(0.641676, 0.922299)], trough_positions[19])
		self.assertEqual([(0.751147, 0.896045)], trough_positions[20])
		self.assertEqual([(0.860617, 0.86979)], trough_positions[21])
		self.assertEqual([(0.898, 0.883)], trough_positions[22])
		for address in (18, 19, 20, 21):
			self.assertEqual(["ball.position"], pro_inputs[address]["roles"])
		self.assertEqual(["ball.jam"], pro_inputs[22]["roles"])
		self.assertEqual("validated", pro_outputs[("pinmame.output.solenoid", 1)]["spatial"]["status"])
		self.assertEqual([(0.860617, 0.86979)], [(placement["x"], placement["y"]) for placement in pro_outputs[("pinmame.output.solenoid", 1)]["spatial"]["placements"]])
		self.assertIn("BallRelease", pro_outputs[("pinmame.output.solenoid", 1)]["physical"]["notes"])
		for address in (41, 42):
			self.assertEqual([(0.393908, 0.220213)], [(placement["x"], placement["y"]) for placement in pro_inputs[address]["spatial"]["placements"]])
		for address in (45, 46):
			self.assertEqual([(0.536243, 0.379225)], [(placement["x"], placement["y"]) for placement in pro_inputs[address]["spatial"]["placements"]])
		self.assertEqual("not_applicable", pro_outputs[("pinmame.output.solenoid", 27)]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", pro_outputs[("pinmame.output.solenoid", 27)]["spatial"]["reason"])
		flasher_positions = {
			address: [(placement["x"], placement["y"]) for placement in pro_outputs[("pinmame.output.solenoid", address)]["spatial"]["placements"]]
			for address in {18, 19, 20, 21, 25}
		}
		self.assertEqual([(0.043766, 0.43)], flasher_positions[18])
		self.assertEqual([(0.954245, 0.49)], flasher_positions[19])
		self.assertEqual([(0.707750, 0.735671), (0.197012, 0.728527)], flasher_positions[20])
		self.assertEqual([(0.374, 0.252)], flasher_positions[21])
		self.assertEqual([(0.790702, 0.232974)], flasher_positions[25])
		lamp_positions = {
			address: [(placement["x"], placement["y"]) for placement in pro_outputs[("pinmame.output.lamp", address)]["spatial"]["placements"]]
			for address in {71, 73, 75}
		}
		self.assertEqual([(0.157235, 0.068047)], lamp_positions[71])
		self.assertEqual([(0.156911, 0.068193)], lamp_positions[73])
		self.assertEqual([(0.163438, 0.067535)], lamp_positions[75])
		self.assertEqual(3, len({position[0] for position in lamp_positions.values()}))
		self.assertEqual(2, pro_outputs[("pinmame.output.solenoid", 20)]["physical"]["quantity"])
		for address in {18, 19, 21, 25}:
			self.assertEqual(1, pro_outputs[("pinmame.output.solenoid", address)]["physical"]["quantity"])
		self.assertEqual(27, pro_outputs[("pinmame.output.gi", 0)]["physical"]["quantity"])
		self.assertEqual(27, len(pro_outputs[("pinmame.output.gi", 0)]["spatial"]["placements"]))
		self.assertEqual("not_applicable", pro_outputs[("pinmame.output.solenoid", 53)]["spatial"]["status"])
		self.assertEqual("virtual", pro_outputs[("pinmame.output.solenoid", 53)]["spatial"]["reason"])

	def test_pro_spatial_placement_keeps_manual_physics_separate_from_vpx_callback_names(self) -> None:
		pro_inputs = bindings(self.pro, "inputs", "pinmame.input.switch")
		pro_outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual([(0.678933, 0.213986)], [(placement["x"], placement["y"]) for placement in pro_inputs[30]["spatial"]["placements"]])
		self.assertEqual([(0.880455, 0.1929)], [(placement["x"], placement["y"]) for placement in pro_inputs[31]["spatial"]["placements"]])
		self.assertEqual([(0.80385, 0.297933)], [(placement["x"], placement["y"]) for placement in pro_inputs[32]["spatial"]["placements"]])
		self.assertEqual([(0.678933, 0.213986)], [(placement["x"], placement["y"]) for placement in pro_outputs[9]["spatial"]["placements"]])
		self.assertEqual([(0.880455, 0.1929)], [(placement["x"], placement["y"]) for placement in pro_outputs[10]["spatial"]["placements"]])
		self.assertEqual([(0.80385, 0.297933)], [(placement["x"], placement["y"]) for placement in pro_outputs[11]["spatial"]["placements"]])
		self.assertEqual([(0.057307, 0.47)], [(placement["x"], placement["y"]) for placement in pro_outputs[12]["spatial"]["placements"]])
		for address in (12, 18, 19, 21):
			placement = pro_outputs[address]["spatial"]["placements"][0]
			self.assertEqual(["manual.avengers-pro"], placement["provenance"]["source_refs"])
			self.assertIn("manual", pro_outputs[address]["physical"]["notes"].casefold())
		for address in (30, 31, 9, 10):
			device = pro_inputs[address] if address in (30, 31) else pro_outputs[address]
			self.assertIn("anomaly", device["physical"]["notes"].casefold())
		script_switches = {entry["label"]: entry["address"] for entry in self.pro_script_evidence["switches"]}
		self.assertEqual(31, script_switches["Bumper1b"])
		self.assertEqual(30, script_switches["Bumper2b"])

	def test_catalog_and_definition_paths_promote_pro_only(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		machines = {machine["id"]: machine for machine in catalog["machines"] if machine["id"] in {"stern.avengers-limited-edition.2012", "stern.avengers-pro.2012"}}
		self.assertEqual("partial", machines["stern.avengers-limited-edition.2012"]["coverage_status"])
		self.assertEqual("machines/partial/stern/avengers-limited-edition-2012.json", machines["stern.avengers-limited-edition.2012"]["definition"])
		self.assertEqual("author_ready", machines["stern.avengers-pro.2012"]["coverage_status"])
		self.assertEqual("physical_pinball", machines["stern.avengers-pro.2012"]["machine_kind"])
		self.assertEqual("machines/author-ready/stern/avengers-pro-2012.json", machines["stern.avengers-pro.2012"]["definition"])

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
		self.assertEqual("45de396493ddf562f06baa6950a5b3b46d7803f4aca1ed1df4ad7f45a6a4c5df", pro_sources["vpx-table.avengers-pro-archive-45de3964"]["sha256"])
		self.assertIn("952,2115", pro_sources["vpx-table.avengers-pro-archive-45de3964"]["locator"])
		self.assertIn("avs_170", pro_sources["vpx-table.avengers-pro-archive-45de3964"]["locator"])
		self.assertNotIn("vpx-table.avengers-pro-archive-45de3964", le_sources)
		self.assertFalse((ROOT / "machines" / "stubs" / "avs_170h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "avs_170h.md").exists())
		self.assertEqual("complete", self.le["knowledge"]["status"])
		self.assertEqual("complete", self.pro["knowledge"]["status"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "avengers-pro-2012.json").exists())


if __name__ == "__main__":
	unittest.main()
