from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "batman-the-dark-knight-pro-2008.json"
HOME_PATH = ROOT / "machines" / "partial" / "stern" / "batman-the-dark-knight-standard-home-edition-2010.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "batman-the-dark-knight-pro-boot-start.json"
HOME_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "batman-the-dark-knight-home-boot-start-and-diagnostics.json"
HOME_KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "batman-the-dark-knight-standard-home-edition-2010.md"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class BatmanDarkKnightDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.home = load_json(HOME_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.home_evidence = load_json(HOME_EVIDENCE_PATH)
		cls.home_knowledge = HOME_KNOWLEDGE_PATH.read_text(encoding="utf-8")

	def test_two_physical_products_are_fail_closed_for_spatial_retrofit(self) -> None:
		self.assertEqual(("stern.batman-the-dark-knight-pro.2008", 5307, 2008), (self.pro["machine"]["id"], self.pro["machine"]["ipdb_id"], self.pro["machine"]["year"]))
		self.assertEqual(("stern.batman-the-dark-knight-standard-home-edition.2010", 5583, 2010), (self.home["machine"]["id"], self.home["machine"]["ipdb_id"], self.home["machine"]["year"]))
		for definition in (self.pro, self.home):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			self.assertIn("spatial_placement", definition["coverage"]["missing"])
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "bdk_294.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "bdk_294.md").exists())

	def test_driver_family_is_exhaustive_and_split_at_bdk_300(self) -> None:
		pro_drivers = {driver["id"] for driver in self.pro["drivers"]}
		home_drivers = {driver["id"] for driver in self.home["drivers"]}
		self.assertEqual({"bdk_130", "bdk_150", "bdk_160", "bdk_200", "bdk_210", "bdk_220", "bdk_240", "bdk_290", "bdk_294"}, pro_drivers)
		self.assertEqual({"bdk_300"}, home_drivers)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(pro_drivers | home_drivers, {driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("bdk_")})
		self.assertEqual("stern.batman-the-dark-knight-standard-home-edition.2010", next(driver for driver in catalog["drivers"] if driver["id"] == "bdk_300")["machine_id"])

	def test_complete_input_spaces_and_model_specific_start_troughs(self) -> None:
		expected_switches = set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1))
		for definition in (self.pro, self.home):
			self.assertEqual(expected_switches, set(bindings(definition, "inputs", "pinmame.input.switch")))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		home = bindings(self.home, "inputs", "pinmame.input.switch")
		self.assertEqual(("Start button", "Tournament Start"), (pro[16]["label"], pro[15]["label"]))
		self.assertEqual(("Start button", "Tournament Start"), (home[35]["label"], home[34]["label"]))
		self.assertEqual(["Trough 4 left", "Trough 3", "Trough 2", "Trough 1 right", "Trough jam"], [pro[number]["label"] for number in range(18, 23)])
		self.assertEqual(["Trough 3 left", "Trough 2", "Trough 1 right", "Trough jam"], [home[number]["label"] for number in range(53, 57)])
		self.assertEqual("Scarecrow crane hit", home[85]["label"])
		self.assertIn("matrix sweep covers only addresses 1-64", home[85]["physical"]["notes"])
		self.assertTrue(home[83]["normally_closed"])
		self.assertTrue(home[81]["normally_closed"])
		self.assertEqual("opto", pro[23]["physical"]["switch_type"])

	def test_switch_pulse_contract_distinguishes_observed_pro_behavior_from_home_inference(self) -> None:
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		home = bindings(self.home, "inputs", "pinmame.input.switch")
		pro_matrix_pulses = {address for address in range(1, 65) if pro[address]["availability"] == "used" and pro[address]["pulse"]}
		home_matrix_pulses = {address for address in range(1, 65) if home[address]["availability"] == "used" and home[address]["pulse"]}
		self.assertEqual({1, 2, 3, 4, 5, 6, 11, 13, 14, 26, 27, 30, 31, 32, 34, 35, 36, 37, 38, 39, 41, 42, 47, 48, 49}, pro_matrix_pulses)
		self.assertEqual({4, 5, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22, 23, 25, 29, 45, 48, 49, 59, 60, 61, 62, 63, 64}, home_matrix_pulses)
		self.assertFalse(home[26]["pulse"])
		self.assertIn("not contact duration", home[26]["physical"]["notes"])
		self.assertIn("functional inference", home[26]["physical"]["notes"])

	def test_q_outputs_are_complete_and_variant_specific(self) -> None:
		expected = set(range(1, 34)) | set(range(51, 67))
		pro = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		home = bindings(self.home, "outputs", "pinmame.output.solenoid")
		self.assertEqual(expected, set(pro))
		self.assertEqual(expected, set(home))
		self.assertEqual({20}, {address for address in range(1, 33) if pro[address]["availability"] == "unused"})
		self.assertEqual({5, 7, 12, 13, 14, 20, 30}, {address for address in range(1, 33) if home[address]["availability"] == "unused"})
		self.assertEqual(("Joker motor", "motor", "BRN"), (pro[26]["label"], pro[26]["kind"], pro[26]["wiring"]["power_wire"]))
		self.assertEqual(("Batmobile flasher", "flasher", "ORG"), (home[26]["label"], home[26]["kind"], home[26]["wiring"]["power_wire"]))
		self.assertEqual(("VIO-WHT", "J7-P6"), (pro[20]["wiring"]["control_wire"], pro[20]["wiring"]["control_connection"]))
		self.assertEqual("used", pro[33]["availability"])
		self.assertEqual("unused", home[33]["availability"])
		for address in range(51, 67):
			self.assertEqual(("virtual", "unused"), (pro[address]["kind"], pro[address]["availability"]))
			self.assertEqual(("virtual", "unused"), (home[address]["kind"], home[address]["availability"]))

	def test_lamp_spaces_and_home_transport_correction_are_explicit(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		home = bindings(self.home, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 89)), set(pro))
		self.assertEqual(set(range(1, 89)), set(home))
		self.assertEqual({30, 46, 81, 82, 83, 84, 85}, {address for address, item in pro.items() if item["availability"] == "unused"})
		self.assertEqual({47, 68, 73, 74, 75, 81, 82, 83, 84, 85}, {address for address, item in home.items() if item["availability"] == "unused"})
		self.assertEqual(("Harvey Dent", "used"), (home[30]["label"], home[30]["availability"]))
		self.assertEqual(("Crane Position 3", "used"), (home[46]["label"], home[46]["availability"]))
		for address in (30, 46):
			self.assertIn("restore a non-NONE lamp output type", home[address]["physical"]["notes"])
		self.assertIn("ignore any callback", home[47]["physical"]["notes"])
		self.assertEqual("165-5000-44-HF", pro[76]["physical"]["part_number"])
		self.assertEqual("112-5024-08", pro[70]["physical"]["part_number"])
		self.assertEqual("The Scarecrow (Lamp 44)", home[44]["label"])
		self.assertIn("same The Scarecrow text as lamp 28", home[44]["physical"]["notes"])
		self.assertIn("manual.stern-batman-the-dark-knight.2008", home[86]["provenance"]["source_refs"])

	def test_pro_custom_mechanisms_capture_working_script_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		joker = mechanisms["mechanism.joker-reveal"]
		self.assertEqual(["device.26-joker-motor", "device.30-joker-motor-relay"], joker["actuators"])
		self.assertIn("1500 ms, 360-step", joker["behavior"])
		self.assertIn("178-182", joker["behavior"])
		crane = mechanisms["mechanism.scarecrow-crane"]
		self.assertEqual(["device.31-scarecrow-motor", "device.28-scarecrow-motor-relay"], crane["actuators"])
		self.assertIn("56=0-1", crane["behavior"])
		self.assertIn("two factory crane/motor assembly variants", crane["behavior"])
		self.assertEqual(["Crane position 6 away", "Crane position 5", "Crane position 4", "Crane position 3", "Crane position 2", "Crane position 1 home"], [position["label"] for position in crane["positions"]])
		batmobile = mechanisms["mechanism.batmobile-ramp"]
		self.assertIn("moving its collision geometry and any captured ball", batmobile["behavior"])
		self.assertIn("invisible helper ball is implementation scaffolding", batmobile["behavior"])
		self.assertIn("mechanism.upper-mini-playfield", mechanisms)
		self.assertNotIn("switch.15-tournament-start", mechanisms["mechanism.routes-and-targets"]["sensors"])
		self.assertNotIn("switch.16-start-button", mechanisms["mechanism.routes-and-targets"]["sensors"])

	def test_home_mechanisms_capture_omissions_and_readdressed_crane(self) -> None:
		mechanisms = {item["id"]: item for item in self.home["mechanisms"]}
		crane = mechanisms["mechanism.scarecrow-crane"]
		self.assertEqual(["device.31-scarecrow-motor", "device.28-scarecrow-motor-relay"], crane["actuators"])
		self.assertEqual([f"switch.{number}-{['crane-position-6-away', 'crane-position-5', 'crane-position-4', 'crane-position-3', 'crane-position-2', 'crane-position-1-home'][number - 10]}" for number in range(10, 16)], crane["sensors"][:6])
		self.assertEqual(["Crane position 6 away", "Crane position 5", "Crane position 4", "Crane position 3", "Crane position 2", "Crane position 1 home"], [position["label"] for position in crane["positions"]])
		self.assertIn("do not copy Pro switch numbers", crane["behavior"])
		fixed = mechanisms["mechanism.fixed-batmobile-ramp"]
		self.assertEqual([], fixed["actuators"])
		self.assertIn("no Q13 pivoting bridge", fixed["behavior"])
		self.assertNotIn("mechanism.joker-reveal", mechanisms)
		self.assertNotIn("mechanism.joker-drop", mechanisms)
		self.assertNotIn("mechanism.upper-mini-playfield", mechanisms)
		self.assertNotIn("switch.34-tournament-start", mechanisms["mechanism.routes-and-targets"]["sensors"])
		self.assertNotIn("switch.35-start-button", mechanisms["mechanism.routes-and-targets"]["sensors"])

	def test_runtime_evidence_locks_correct_initial_state_and_metadata_defect(self) -> None:
		self.assertEqual(["stern.batman-the-dark-knight-pro.2008"], self.pro_evidence["machine_ids"])
		self.assertEqual(["stern.batman-the-dark-knight-standard-home-edition.2010"], self.home_evidence["machine_ids"])
		self.assertEqual("e54ff7c90c52a3305e10961f5e5833a20506e04f373b58d955f47a40b8780bb4", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual([33], self.pro_evidence["runtime"]["observations"]["solenoid_addresses_seen"])
		self.assertIn("--initial-switch 18", self.pro_evidence["runtime"]["command_template"])
		self.assertIn("--initial-switch 53", self.home_evidence["runtime"]["command_template"])
		self.assertEqual([30, 46], self.home_evidence["runtime"]["observations"]["lamp_decoder_holes_not_seen"])
		self.assertIn(47, self.home_evidence["runtime"]["observations"]["lamp_addresses_seen"])
		self.assertNotIn(30, self.home_evidence["runtime"]["observations"]["lamp_addresses_seen"])
		self.assertEqual([], self.home_evidence["runtime"]["observations"]["solenoid_addresses_seen"])

	def test_home_knowledge_repeats_contact_duration_and_d16_evidence_limits(self) -> None:
		self.assertIn("not contact duration; pulse/sustained behavior is a functional inference", self.home_knowledge)
		self.assertIn("D16 lies outside the 1-64 matrix sweep", self.home_knowledge)
		self.assertIn("shared `SAM_GAME_3LEDS_BSTB` configuration", self.home_knowledge)

	def test_sources_pin_manual_script_rom_and_diagnostic_hashes(self) -> None:
		pro = {source["id"]: source for source in self.pro["sources"]}
		home = {source["id"]: source for source in self.home["sources"]}
		self.assertEqual("c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219", pro["manual.stern-batman-the-dark-knight.2008"]["sha256"])
		self.assertIn("PDF pages 6, 8, and 10", pro["manual.stern-batman-the-dark-knight.2008"]["locator"])
		self.assertEqual("1c6bc48c74e7bb8e48293152ee226318a9a8dce230bd6b63554f9c92075dbff0", pro["vpx.batman-the-dark-knight-pro-1.16"]["sha256"])
		self.assertIn("semantic ground truth for Pro", pro["vpx.batman-the-dark-knight-pro-1.16"]["locator"])
		self.assertEqual("b82a4b996c6561b273a7eda6bcf2a540cb67b3b8947bf439b8e9a8928ace3f49", pro["rom.stern-batman-the-dark-knight.bdk-294"]["sha256"])
		self.assertEqual("4d34254e60422503a203206e2a50970a2becdb20941f008da159927ed8292612", home["rom.stern-batman-the-dark-knight-home.bdk-300"]["sha256"])
		self.assertEqual("028db927129a01aeb2226081b21c63203b0f6fc547187e7b487113538f16a7d1", home["runtime.batman-the-dark-knight-home.switch-diagnostic"]["sha256"])
		self.assertEqual("cb5eedfa59f79658cd91f68104c8062dd329cbe9cc582d504b822c16584f50f6", home["runtime.batman-the-dark-knight-home.lamp-diagnostic"]["sha256"])
		self.assertEqual("fb2850475661a0e3470e7dbeb2d5d1ff852db86e421a625204fa1b0640a4c52e", home["runtime.batman-the-dark-knight-home.coil-diagnostic"]["sha256"])
		self.assertIn("incorrectly applies Pro unused lamps 30/46", home["pinmame.core.4ec52ff0ac13"]["locator"])

	def test_ids_bindings_and_actuator_ownership_are_unique(self) -> None:
		for definition in (self.pro, self.home):
			for collection in (definition["inputs"], definition["outputs"]):
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))
				controller_bindings = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(controller_bindings), len(set(controller_bindings)))
			actuators = [actuator for mechanism in definition["mechanisms"] for actuator in mechanism["actuators"]]
			self.assertEqual(len(actuators), len(set(actuators)))


if __name__ == "__main__":
	unittest.main()
