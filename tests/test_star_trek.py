from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = ROOT / "machines" / "partial" / "stern" / "star-trek-premium-limited-edition-2013.json"
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "star-trek-pro-2013.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "star-trek-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class StarTrekDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.premium = load_json(PREMIUM_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_both_physical_editions_are_fail_closed_for_spatial_retrofit(self) -> None:
		for definition in (self.premium, self.pro):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			self.assertIn("spatial_placement", definition["coverage"]["missing"])
			self.assertEqual("complete", definition["knowledge"]["status"])
		self.assertTrue((ROOT / "machines" / "partial" / "stern" / "star-trek-pro-2013.json").exists())

	def test_editions_split_the_complete_driver_family(self) -> None:
		premium = {driver["id"] for driver in self.premium["drivers"]}
		pro = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"st_140h", "st_141h", "st_142h", "st_150h", "st_160h", "st_161h", "st_161hc", "st_162h", "st_162hc"}, premium)
		self.assertEqual({"st_120", "st_130", "st_140", "st_150", "st_160", "st_161", "st_161c", "st_162", "st_162c"}, pro)
		self.assertFalse(premium & pro)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("st_")}, premium | pro)
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.premium["drivers"]))
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.pro["drivers"]))

	def test_switch_matrix_names_and_dedicated_bindings_match_the_physical_machine(self) -> None:
		for definition in (self.premium, self.pro):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertEqual("Left pop bumper", switches[30]["label"])
			self.assertEqual("Bottom pop bumper", switches[32]["label"])
			self.assertEqual("Center 3-bank top", switches[39]["label"])
			self.assertEqual("Center 3-bank bottom", switches[41]["label"])
			self.assertEqual("Left 2-bank top", switches[42]["label"])
			self.assertEqual("Left 2-bank bottom", switches[43]["label"])
			self.assertEqual("Upper-right flipper button", switches[86]["label"])
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		pro_switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual("unused", pro_switches[53]["availability"])
		self.assertEqual("Vengeance crash opto", bindings(self.premium, "inputs", "pinmame.input.switch")[53]["label"])

	def test_trough_has_four_positions_and_a_downstream_jam_opto(self) -> None:
		by_address = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual(["microswitch"] * 4, [by_address[number]["physical"]["switch_type"] for number in range(18, 22)])
		self.assertEqual("opto", by_address[22]["physical"]["switch_type"])
		trough = next(item for item in self.pro["mechanisms"] if item["id"] == "mechanism.trough")
		self.assertEqual(5, len(trough["sensors"]))
		self.assertIn("18-21", trough["behavior"])

	def test_pro_has_only_the_32_main_outputs(self) -> None:
		solenoids = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(solenoids))
		self.assertEqual("virtual", solenoids[33]["kind"])
		self.assertNotIn("wiring", solenoids[33])
		self.assertEqual("Center lock magnet", solenoids[3]["label"])
		self.assertEqual("Upper-right flipper", solenoids[12]["label"])
		self.assertEqual("optional", solenoids[8]["availability"])
		self.assertEqual("optional", solenoids[24]["availability"])
		self.assertFalse(set(range(51, 67)) & set(solenoids))

	def test_premium_auxiliary_board_uses_pinmame_public_compatibility_addresses(self) -> None:
		by_address = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		self.assertEqual("Q51", by_address[51]["wiring"]["driver_transistor"])
		self.assertEqual("Q41", by_address[59]["wiring"]["driver_transistor"])
		self.assertEqual("YEL-ORG", by_address[53]["wiring"]["control_wire"])
		self.assertEqual("unused", by_address[57]["availability"])
		self.assertEqual("unused", by_address[66]["availability"])

	def test_pro_standard_lamp_matrix_is_complete_and_physical(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual({1, 2, 6, 31, 39, 47, 58, 77, 78, 79}, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("Fire button", lamps[3]["label"])
		self.assertEqual("Black hole arrow", lamps[61]["label"])
		self.assertEqual("Right-side blue playfield spotlight", lamps[80]["label"])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))

	def test_pro_rgb_insert_channels_preserve_color_and_position(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		expected = {
			25: "Left orbit emblem red", 33: "Left orbit emblem green", 41: "Left orbit emblem blue",
			26: "Left ramp emblem red", 34: "Left ramp emblem green", 42: "Left ramp emblem blue",
			29: "Left eject emblem red", 37: "Left eject emblem green", 45: "Left eject emblem blue",
			30: "Center lane emblem red", 38: "Center lane emblem green", 46: "Center lane emblem blue",
			28: "Right ramp emblem red", 36: "Right ramp emblem green", 44: "Right ramp emblem blue",
			27: "Right orbit emblem red", 35: "Right orbit emblem green", 43: "Right orbit emblem blue",
		}
		self.assertEqual(expected, {address: lamps[address]["label"] for address in expected})
		self.assertTrue(all(lamps[address]["kind"] == "rgb_lamp" for address in expected))
		self.assertIn("x=200.0, y=1502.0", lamps[25]["physical"]["location"])

	def test_pro_mechanisms_are_complete_and_exclude_premium_hardware(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		expected = {"mechanism.trough", "mechanism.auto-launcher", "mechanism.left-eject", "mechanism.center-drop-target", "mechanism.center-lock", "mechanism.vengeance", "mechanism.flippers", "mechanism.pop-bumpers", "mechanism.slingshots", "mechanism.spinner", "mechanism.beam-target-bank", "mechanism.trek-target-bank", "mechanism.right-target-bank", "mechanism.center-target-bank", "mechanism.left-target-bank", "mechanism.red-targets", "mechanism.ramps-and-orbits", "mechanism.laser", "mechanism.optional-shaker"}
		self.assertEqual(expected, set(mechanisms))
		self.assertEqual(["device.vengeance-super-speed-kickback"], mechanisms["mechanism.vengeance"]["actuators"])
		self.assertIn("passive bash", mechanisms["mechanism.vengeance"]["behavior"])
		self.assertIn("switch 90", mechanisms["mechanism.flippers"]["behavior"])
		all_actuators = {actuator for item in mechanisms.values() for actuator in item["actuators"]}
		self.assertFalse({"device.vengeance-ship-actuator", "device.vengeance-ship-latch", "device.rotating-vuk", "device.bottom-drain-kickback"} & all_actuators)

	def test_premium_custom_mechanisms_use_corrected_switch_names(self) -> None:
		by_id = {item["id"]: item for item in self.premium["mechanisms"]}
		self.assertEqual(["switch.center-lock-bottom", "switch.center-lock-top"], by_id["mechanism.center-lock"]["sensors"])
		self.assertIn("device.rotating-vuk", by_id["mechanism.left-eject"]["actuators"])
		self.assertIn("100 Hz", by_id["mechanism.vengeance"]["behavior"])

	def test_bindings_are_unique_within_each_controller_group(self) -> None:
		for definition in (self.premium, self.pro):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))

	def test_pro_sources_and_exact_rom_run_are_content_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("23cb9e6683d7b357ada48678a8e157a8b64102ea012821c350a3f033fae66b28", sources["manual.star-trek-pro"]["sha256"])
		self.assertEqual("abc5dbb6ead12f16886143a50cfd2534c9baf855b070924dd7d82e404b4d69bf", sources["vpx.star-trek-pro-fss"]["sha256"])
		self.assertEqual("2976e3313a6fa1ee6f26709d515661b81ade8f01894a847b907a5e608e5bb9e7", sources["vpx-table.star-trek-pro-fss"]["sha256"])
		runtime = self.evidence["runtime"]
		self.assertEqual("st_161c", runtime["game"])
		self.assertEqual("f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0", runtime["rom_archive_sha256"])
		self.assertEqual("a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])


if __name__ == "__main__":
	unittest.main()
