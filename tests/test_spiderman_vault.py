from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "stern" / "spider-man-vault-edition-2016.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


class SpiderManVaultSpatialTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")[0]

	def test_definition_is_author_ready_and_every_device_is_disposed(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(96, len(self.definition["inputs"]))
		self.assertEqual(126, len(self.definition["outputs"]))
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in [*self.definition["inputs"], *self.definition["outputs"]]))
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "spider-man-vault-edition-2016.json").exists())

	def test_exact_vpx_table_source_is_retained_without_a_machine_local_path(self) -> None:
		source = next(source for source in self.definition["sources"] if source["id"] == "vpx-table.spider-man-ve-2.2")
		self.assertEqual("b258efeecc3dcbffd7dae79c52fdd39bba8c9a82e918034f170ab75c90764f11", source["sha256"])
		self.assertEqual("Spider-Man_VE_2.2.vpx", source["original_filename"])
		self.assertIn("85,819,392 bytes", source["locator"])
		self.assertNotIn("L:\\", source["locator"])

	def test_switch_locations_preserve_trough_order_and_single_assembly_limits(self) -> None:
		trough = [self.switches[address]["spatial"]["placements"][0] for address in (18, 19, 20, 21, 22)]
		self.assertEqual(sorted(point["x"] for point in trough), [point["x"] for point in trough])
		self.assertEqual(sorted((point["y"] for point in trough), reverse=True), [point["y"] for point in trough])
		for address in (49, 50):
			self.assertEqual([(0.50199, 0.312554)], [(point["x"], point["y"]) for point in self.switches[address]["spatial"]["placements"]])
		for left, right in ((53, 54), (57, 58)):
			left_point = self.switches[left]["spatial"]["placements"][0]
			right_point = self.switches[right]["spatial"]["placements"][0]
			self.assertEqual((left_point["x"], left_point["y"]), (right_point["x"], right_point["y"]))
		self.assertEqual("not_applicable", self.switches[84]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[84]["spatial"]["reason"])
		self.assertEqual("not_applicable", self.switches[86]["spatial"]["status"])
		self.assertEqual("unused", self.switches[86]["spatial"]["reason"])

	def test_flashers_keep_physical_multiplicity_and_back_panel_projection(self) -> None:
		for address, quantity in ((23, 2), (25, 2), (31, 3)):
			self.assertEqual(quantity, self.solenoids[address]["physical"]["quantity"])
			self.assertEqual(quantity, len(self.solenoids[address]["spatial"]["placements"]))
		self.assertEqual(2, self.solenoids[28]["physical"]["quantity"])
		self.assertEqual([(0.136924, 0.589677)], [(point["x"], point["y"]) for point in self.solenoids[28]["spatial"]["placements"]])
		self.assertIn("single drilled Green Goblin toy", self.solenoids[28]["physical"]["notes"])
		self.assertLess(self.solenoids[29]["spatial"]["placements"][0]["y"], 0.05)
		self.assertLess(self.solenoids[30]["spatial"]["placements"][0]["y"], 0.05)
		self.assertEqual("used", self.solenoids[19]["availability"])
		self.assertEqual("validated", self.solenoids[19]["spatial"]["status"])
		self.assertEqual((0.136924, 0.589677), (self.solenoids[19]["spatial"]["placements"][0]["x"], self.solenoids[19]["spatial"]["placements"][0]["y"]))
		self.assertIn("SolCallback(19) disabled", self.solenoids[19]["physical"]["notes"])

	def test_lamps_use_direct_inserts_and_project_only_true_back_panel_groups(self) -> None:
		self.assertEqual((0.703425, 0.584499), (self.lamps[63]["spatial"]["placements"][0]["x"], self.lamps[63]["spatial"]["placements"][0]["y"]))
		for address in range(66, 72):
			self.assertEqual(0.0, self.lamps[address]["spatial"]["placements"][0]["y"])
		for address in (74, 75, 76, 77):
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]))
		for address in (55, 56, 73, 79, 80):
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"])

	def test_gi_records_manual_topology_without_counting_render_fanout(self) -> None:
		placements = self.gi["spatial"]["placements"]
		self.assertEqual(44, self.gi["physical"]["quantity"])
		self.assertEqual(42, len(placements))
		circuits = Counter(point["id"].split(".emitter.", 1)[1].split(".", 1)[0] for point in placements)
		self.assertEqual({"brown": 8, "yellow": 11, "violet": 13, "green": 10}, dict(circuits))
		self.assertEqual(10, sum(point["y"] == 0.0 for point in placements))
		self.assertEqual([0.090187, 0.181075, 0.27243, 0.363551, 0.45514, 0.542056, 0.632243, 0.724533, 0.815888, 0.907009], [point["x"] for point in placements if ".green." in point["id"]])
		self.assertTrue(all(point["provenance"]["source_refs"] == ["manual.spider-man-ve.500-55a0-01"] for point in placements))
		self.assertIn("coin door", self.gi["physical"]["notes"])
		self.assertIn("circuit-4 prose says upper right", self.gi["physical"]["notes"])
		self.assertIn("rear view, so x is mirrored", self.gi["physical"]["notes"])

	def test_cabinet_service_and_virtual_outputs_are_not_forced_onto_playfield(self) -> None:
		self.assertEqual("cabinet_or_service", self.lamps[1]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", self.solenoids[6]["spatial"]["reason"])
		self.assertEqual("virtual", self.solenoids[33]["spatial"]["reason"])


if __name__ == "__main__":
	unittest.main()
