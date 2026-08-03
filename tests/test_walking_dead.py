from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-walking-dead-premium-limited-edition-2014.json"
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "the-walking-dead-pro-2014.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "walking-dead-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


class WalkingDeadDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.premium = load_json(PREMIUM_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)

	def test_physical_editions_have_disjoint_exact_driver_sets_and_independent_coverage(self) -> None:
		self.assertEqual(2, self.premium["schema_version"])
		self.assertEqual("author_ready", self.premium["coverage"]["status"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertEqual([], self.premium["coverage"]["missing"])
		self.assertEqual("validated", self.premium["coverage"]["dimensions"]["spatial_placement"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		premium_drivers = {driver["id"] for driver in self.premium["drivers"]}
		pro_drivers = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"twd_111h", "twd_119h", "twd_124h", "twd_125h", "twd_128h", "twd_141h", "twd_153h", "twd_156h", "twd_156hc", "twd_160h", "twd_160hc"}, premium_drivers)
		self.assertEqual({"twd_105", "twd_111", "twd_119", "twd_124", "twd_125", "twd_128", "twd_141", "twd_153", "twd_156", "twd_156c", "twd_160", "twd_160c"}, pro_drivers)
		self.assertFalse(premium_drivers & pro_drivers)

	def test_pro_switch_and_dip_spaces_are_complete_and_model_specific(self) -> None:
		switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.pro, "inputs", "pinmame.input.dip")))
		self.assertEqual(96, len(self.pro["inputs"]))
		self.assertEqual("unused", switches[1]["availability"])
		self.assertEqual("Star rollover (top)", switches[12]["label"])
		self.assertEqual("Star rollover (bottom)", switches[13]["label"])
		self.assertEqual("unused", switches[40]["availability"])
		self.assertEqual("unused", switches[70]["availability"])
		self.assertEqual("unused", switches[71]["availability"])
		self.assertEqual("unused", switches[72]["availability"])

	def test_pro_runtime_rest_states_do_not_change_physical_contact_types(self) -> None:
		by_id = {item["id"]: item for item in self.pro["inputs"]}
		well = by_id["switch.well-walker"]
		doors = by_id["switch.prison-doors-closed"]
		self.assertFalse(well["normally_closed"])
		self.assertEqual("microswitch", well["physical"]["switch_type"])
		self.assertIn("position.rest", well["roles"])
		self.assertIn("position.closed-runtime", doors["roles"])
		self.assertFalse(doors["normally_closed"])

	def test_pro_physical_outputs_override_nonphysical_script_callbacks(self) -> None:
		coils = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(coils))
		self.assertEqual("virtual", coils[33]["kind"])
		self.assertNotIn("wiring", coils[33])
		self.assertEqual({5, 6, 17, 18, 20, 22, 23, 30}, {address for address, item in coils.items() if item["availability"] == "unused"})
		self.assertEqual({8, 24}, {address for address, item in coils.items() if item["availability"] == "optional"})
		self.assertEqual("Horde flasher", coils[21]["label"])
		self.assertEqual("unused", coils[23]["availability"])
		self.assertEqual(["manual.walking-dead-pro"], coils[23]["provenance"]["source_refs"])

	def test_pro_lamp_matrix_and_gi_are_complete(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		gi = bindings(self.pro, "outputs", "pinmame.output.gi")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual({0}, set(gi))
		self.assertEqual("Killing spree", lamps[10]["label"])
		self.assertEqual("Katana multi-kill", lamps[16]["label"])
		self.assertEqual("Pistol multi-kill", lamps[18]["label"])
		self.assertEqual("Chair multi-kill", lamps[20]["label"])
		self.assertIn("omits its render callback", lamps[2]["physical"]["notes"])

	def test_pro_custom_mechanisms_capture_recreation_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		self.assertEqual({"mechanism.trough", "mechanism.auto-launcher", "mechanism.prison-doors", "mechanism.prison-magnet", "mechanism.left-drop-bank", "mechanism.well-walker", "mechanism.prison-walker-target", "mechanism.pop-bumpers", "mechanism.slingshots", "mechanism.flippers"}, set(mechanisms))
		self.assertIn("angle 90 and force 4", mechanisms["mechanism.trough"]["behavior"])
		self.assertIn("power 50", mechanisms["mechanism.auto-launcher"]["behavior"])
		self.assertIn("clears switch 4", mechanisms["mechanism.prison-doors"]["behavior"])
		self.assertIn("speed from 15 up to 20", mechanisms["mechanism.prison-magnet"]["behavior"])
		self.assertEqual([], mechanisms["mechanism.well-walker"]["actuators"])
		self.assertNotIn("mechanism.crossbow-cannon", mechanisms)
		self.assertNotIn("mechanism.bicycle-girl-ramp", mechanisms)

	def test_runtime_trace_anchors_display_gi_and_activity_without_inventing_hardware(self) -> None:
		runtime = self.pro_evidence["runtime"]
		self.assertEqual("9f0fa7803236c566829037612c9d7732c153e5fa35681b7513324d3ae380a716", runtime["rom_archive_sha256"])
		self.assertEqual("ffb741cfa5f1238d756035c4c113b77ad94fdd2a9e015c21a92af0813595bccb", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		self.assertEqual([23, 24], runtime["observations"]["solenoid_addresses_seen"])
		self.assertEqual("unused", bindings(self.pro, "outputs", "pinmame.output.solenoid")[23]["availability"])

	def test_premium_auxiliary_outputs_and_extended_lamps_remain_distinct(self) -> None:
		aux = {
			item["binding"]["device"]: item
			for item in self.premium["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid" and item["binding"]["device"] >= 51
		}
		self.assertEqual({51, 52, 53, 54, 55, 56}, set(aux))
		self.assertEqual("32-1800 / 090-5031-00-ND", aux[52]["physical"]["part_number"])
		premium_lamps = {item["id"]: item["binding"]["device"] for item in self.premium["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual(168, premium_lamps["lamp.right-loop-arrow.red"])
		self.assertEqual(106, premium_lamps["lamp.gi-white"])
		self.assertEqual(107, premium_lamps["lamp.gi-back-panel-red"])
		self.assertEqual(108, premium_lamps["lamp.gi-left-drop-target-bank"])
		self.assertEqual(109, premium_lamps["lamp.gi-red"])

	def test_premium_spatial_inventory_disposes_every_device_and_reconciles_physical_emitters(self) -> None:
		devices = [*self.premium["inputs"], *self.premium["outputs"]]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		self.assertEqual(46, sum(device["spatial"]["status"] == "validated" for device in self.premium["inputs"]))
		lamps = bindings(self.premium, "outputs", "pinmame.output.lamp")
		self.assertEqual((23, 23), (lamps[106]["physical"]["quantity"], len(lamps[106]["spatial"]["placements"])))
		self.assertEqual((2, 2), (lamps[107]["physical"]["quantity"], len(lamps[107]["spatial"]["placements"])))
		self.assertEqual((3, 3), (lamps[108]["physical"]["quantity"], len(lamps[108]["spatial"]["placements"])))
		self.assertEqual((14, 14), (lamps[109]["physical"]["quantity"], len(lamps[109]["spatial"]["placements"])))
		self.assertTrue(all(point["y"] == 0 for address in (107, 108) for point in lamps[address]["spatial"]["placements"]))
		self.assertEqual([0.9679, 0.771], [point["x"] for point in lamps[107]["spatial"]["placements"]])
		self.assertEqual([0.5464, 0.48, 0.4158], [point["x"] for point in lamps[108]["spatial"]["placements"]])
		self.assertIn("service/rear-face view", lamps[107]["physical"]["notes"])
		self.assertIn("077-5000-00", lamps[107]["physical"]["notes"])
		self.assertIn("does not assert", lamps[108]["physical"]["notes"])
		self.assertNotIn("above the left drop-target bank", lamps[108]["physical"]["location"])
		self.assertIn("vpx.walking-dead-premium-le-vpw-day-1.1", lamps[106]["provenance"]["source_refs"])
		flashers = {address: item for address, item in bindings(self.premium, "outputs", "pinmame.output.solenoid").items() if item["kind"] == "flasher"}
		self.assertEqual(2, len(flashers[27]["spatial"]["placements"]))
		self.assertTrue(all(len(item["spatial"]["placements"]) == item["physical"]["quantity"] for item in flashers.values()))
		for device in devices:
			if device["spatial"]["status"] == "validated":
				for point in device["spatial"]["placements"]:
					self.assertGreaterEqual(point["x"], 0)
					self.assertLessEqual(point["x"], 1)
					self.assertGreaterEqual(point["y"], 0)
					self.assertLessEqual(point["y"], 1)

	def test_sources_are_hash_anchored_identity_is_model_specific_and_partial_is_removed(self) -> None:
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual(6155, self.pro["machine"]["ipdb_id"])
		self.assertEqual(6156, self.premium["machine"]["ipdb_id"])
		self.assertEqual("03bbf27093ad8b851ffe5b6284b1f14a4ccbce1ca0a68e79800db728bc92a5ae", sources["manual.walking-dead-pro"]["sha256"])
		self.assertEqual("18d92b612f8d4f0fe1c0f20131fbeb3588d8393502330ca321deb36c9fcbcac4", sources["vpx.walking-dead-pro.jp-salas-v5.5.0"]["sha256"])
		self.assertEqual("bfc4e21042b59e7c6495604166e9219d52c6b813", sources["vpx.walking-dead-pro.jp-salas-v5.5.0"]["revision"])
		self.assertEqual("ffb741cfa5f1238d756035c4c113b77ad94fdd2a9e015c21a92af0813595bccb", sources["runtime.walking-dead-pro.boot-start"]["sha256"])
		self.assertEqual("complete", self.pro["knowledge"]["status"])
		self.assertTrue((ROOT / "machines" / "partial" / "stern" / "the-walking-dead-pro-2014.json").exists())
		premium_sources = {source["id"]: source for source in self.premium["sources"]}
		self.assertEqual("2aca72eb73ac11cc1f8d5633cd8bb302146ac2dd91bfa5fb8364a314b5179987", premium_sources["vpx-table.walking-dead-premium-le-vpw-day-1.1"]["sha256"])
		self.assertEqual("c8f78d6bd0d52632049f1f1ee445e47d10db698355a681dc7e8d1da14b6c4a64", premium_sources["runtime.walking-dead-premium-le.gi-lamp-diagnostic"]["sha256"])
		self.assertEqual("dc40cfe85c90de2cc8c2ae16a8ca5a0d3cf2f8cbdc24d7eba39600601506fa77", premium_sources["runtime.walking-dead-premium-le.boot-start"]["sha256"])
		rom = premium_sources["rom-static.walking-dead-premium-le-output-names"]
		self.assertEqual("rom_static_analysis", rom["kind"])
		self.assertEqual("e09cba4477c9d551e858c0b4c8ee005fb041d3008a4cc5e928d502127329d3fd", rom["sha256"])
		self.assertIn("TWD160h.BIN", rom["locator"])
		self.assertIn("SHA-256 5f618c875d160ce27a73a0edf30659b63f08478147c4476b5b8916a614d6d6a3", rom["locator"])
		self.assertIn("SHA-1 1fbaa077ec834ff9d289008ef1169e0e7fd68271", rom["locator"])
		self.assertIn("CRC32 1ed7b80a", rom["locator"])
		self.assertIn("0x1090c8-0x1090e0", rom["locator"])
		self.assertIn("WHITE, BACK PANEL, LEFT DROP TARGET BANK, and RED", rom["locator"])
		self.assertIn("public lamp 82+i", rom["locator"])
		self.assertIn("IDs 25-28 are indices 24-27", rom["locator"])
		self.assertTrue(PREMIUM_PATH.exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "the-walking-dead-premium-limited-edition-2014.json").exists())


if __name__ == "__main__":
	unittest.main()
