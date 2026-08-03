from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_PATH = ROOT / "machines" / "partial" / "stern" / "iron-man-2010.json"
VAULT_PATH = ROOT / "machines" / "author-ready" / "stern" / "iron-man-vault-edition-2014.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "iron-man-vault-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class IronManDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.original = load_json(ORIGINAL_PATH)
		cls.vault = load_json(VAULT_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_physical_products_are_split_and_only_the_reviewed_vault_product_is_author_ready(self) -> None:
		for definition in (self.original, self.vault):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertEqual("partial", self.original["coverage"]["status"])
		self.assertIn("spatial_placement", self.original["coverage"]["missing"])
		self.assertEqual("author_ready", self.vault["coverage"]["status"])
		self.assertEqual([], self.vault["coverage"]["missing"])
		self.assertEqual("validated", self.vault["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual({"id": "stern.iron-man.2010", "ipdb_id": 5550, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "I-00B3", "name": "Iron Man", "year": 2010}, self.original["machine"])
		self.assertEqual({"id": "stern.iron-man-vault-edition.2014", "ipdb_id": 6154, "kind": "physical_pinball", "manufacturer": "Stern", "model_number": "I-00B0", "name": "Iron Man Pro Vault Edition", "year": 2014}, self.vault["machine"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "iron-man-vault-edition-2010.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stern" / "iron-man-vault-edition-2010.md").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "iron-man-vault-edition-2014.json").exists())

	def test_driver_split_exhaustively_covers_the_clone_family(self) -> None:
		original = {driver["id"] for driver in self.original["drivers"]}
		vault = {driver["id"] for driver in self.vault["drivers"]}
		self.assertEqual({"im_100", "im_110", "im_120", "im_140", "im_160", "im_181", "im_182", "im_183", "im_185", "im_186"}, original)
		self.assertEqual({"im_183ve", "im_185ve", "im_186ve"}, vault)
		self.assertFalse(original & vault)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("im_")}, original | vault)
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.original["drivers"] + self.vault["drivers"]))
		self.assertTrue(all("2010 physical product" in driver["variant_notes"] for driver in self.original["drivers"]))
		self.assertTrue(all("2014 Pro Vault Edition" in driver["variant_notes"] for driver in self.vault["drivers"]))

	def test_complete_matrix_dedicated_and_dip_spaces_are_explicit(self) -> None:
		expected_switches = set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1))
		for definition in (self.original, self.vault):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(expected_switches, set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertEqual("unused", switches[2]["availability"])
			self.assertEqual("unused", switches[17]["availability"])
			self.assertEqual("unused", switches[51]["availability"])
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertTrue(switches[-6]["normally_closed"])
			self.assertEqual("unused", switches[68]["availability"])
			self.assertEqual("optional", switches[69]["availability"])
			self.assertEqual("unused", switches[71]["availability"])
			self.assertEqual("unused", switches[72]["availability"])
			self.assertEqual("J2-P2", switches[65]["wiring"]["drive_connection"])
			self.assertEqual("J3-P2", switches[83]["wiring"]["drive_connection"])
			self.assertEqual("J13-P9", switches[0]["wiring"]["drive_connection"])

	def test_manual_corrects_legacy_switch_labels_and_monger_endpoints(self) -> None:
		for definition in (self.original, self.vault):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			expected = {
				1: "Iron Monger motor down", 3: "Iron Monger motor up", 12: "Left ramp entrance", 15: "Tournament start", 16: "Start button",
				23: "Shooter lane", 25: "Left return lane", 37: "Right ramp exit", 38: "Top lane left", 39: "Top lane right", 43: "Right ramp entrance", 49: "Left ramp exit",
			}
			for address, label in expected.items():
				self.assertEqual(label, switches[address]["label"])
			self.assertFalse(switches[1]["pulse"])
			self.assertFalse(switches[3]["pulse"])
			self.assertIn("only when the moving assembly reaches the endpoint", switches[1]["physical"]["notes"])
			self.assertEqual(["position.down"], switches[1]["roles"])
			self.assertEqual(["position.up"], switches[3]["roles"])
			for address in (7, 9, 12, 24, 25, 28, 29, 37, 38, 39, 43, 49):
				self.assertFalse(switches[address]["pulse"], f"switch {address} has paired Hit/UnHit handlers and must retain sustained state")
			for address in (4, 5, 6, 11, 13, 14):
				self.assertTrue(switches[address]["pulse"])

	def test_q_outputs_game_on_and_auxiliary_capacity_are_complete(self) -> None:
		for definition in (self.original, self.vault):
			outputs = bindings(definition, "outputs", "pinmame.output.solenoid")
			self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(outputs))
			self.assertEqual("virtual", outputs[33]["kind"])
			self.assertNotIn("wiring", outputs[33])
			for address in range(51, 67):
				self.assertEqual(("virtual", "unused"), (outputs[address]["kind"], outputs[address]["availability"]))
			for address in (7, 13, 14):
				self.assertEqual("unused", outputs[address]["availability"])
				self.assertNotIn("power_wire", outputs[address]["wiring"])
			self.assertEqual("optional", outputs[8]["availability"])
			self.assertEqual(16, outputs[8]["wiring"]["nominal_voltage_v"])
			self.assertEqual("ac", outputs[8]["wiring"]["voltage_type"])
			self.assertEqual("optional", outputs[24]["availability"])
			self.assertEqual("J17-P7", outputs[8]["wiring"]["power_connection"])
			self.assertIn("Q8 table prints 50 VDC", outputs[8]["physical"]["notes"])
			self.assertIn("16 VAC secondary", outputs[8]["physical"]["notes"])
			self.assertIn("SetLampMod 120-132 flasher callback block", outputs[24]["physical"]["notes"])
			self.assertIn("physical manual construction governs", outputs[24]["physical"]["notes"])
			self.assertEqual("J7-P4", outputs[19]["wiring"]["control_connection"])
			self.assertEqual("J10-P8", outputs[4]["wiring"]["power_connection"])

	def test_original_and_vault_lighting_technology_stays_distinct(self) -> None:
		original_outputs = bindings(self.original, "outputs", "pinmame.output.solenoid")
		vault_outputs = bindings(self.vault, "outputs", "pinmame.output.solenoid")
		for address in list(range(20, 24)) + list(range(25, 33)):
			self.assertIn("incandescent", original_outputs[address]["physical"]["notes"])
			self.assertNotIn("part_number", original_outputs[address]["physical"])
			self.assertIn("LED flasher module", vault_outputs[address]["physical"]["notes"])
			self.assertTrue(vault_outputs[address]["physical"]["part_number"].startswith("113-5034-"))
		original_lamps = bindings(self.original, "outputs", "pinmame.output.lamp")
		vault_lamps = bindings(self.vault, "outputs", "pinmame.output.lamp")
		self.assertIn("incandescent", original_lamps[1]["physical"]["notes"])
		self.assertEqual("112-5033-08", vault_lamps[1]["physical"]["part_number"])
		self.assertIn("#555-form-factor", vault_lamps[54]["physical"]["notes"])
		self.assertIn("#555-form-factor", vault_lamps[56]["physical"]["notes"])
		self.assertNotIn("part_number", vault_lamps[54]["physical"])

	def test_lamp_matrix_and_unlabeled_load_bulbs_are_exhaustive(self) -> None:
		expected_unused = {64} | set(range(65, 73)) | set(range(74, 79))
		for definition in (self.original, self.vault):
			lamps = bindings(definition, "outputs", "pinmame.output.lamp")
			self.assertEqual(set(range(1, 81)), set(lamps))
			self.assertEqual(expected_unused, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
			for address in (73, 79, 80):
				self.assertEqual("used", lamps[address]["availability"])
				self.assertIn("clear matrix bulb", lamps[address]["label"])
				self.assertIn("hidden", lamps[address]["physical"]["notes"].casefold())
				self.assertEqual(["internal.load"], lamps[address]["roles"])
			self.assertEqual(2, lamps[55]["physical"]["quantity"])
			self.assertRegex(lamps[55]["physical"]["notes"], r"two .*emitters")
			self.assertEqual("J13-P9", lamps[1]["wiring"]["drive_connection"])
			self.assertEqual("J12-P11", lamps[80]["wiring"]["return_connection"])
			self.assertEqual({0}, set(bindings(definition, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_capture_runtime_causality(self) -> None:
		for definition in (self.original, self.vault):
			mechanisms = {mechanism["id"]: mechanism for mechanism in definition["mechanisms"]}
			trough = mechanisms["mechanism.trough"]
			self.assertEqual(5, len(trough["sensors"]))
			self.assertIn("physical switch 15 is Tournament Start", trough["behavior"])
			monger = mechanisms["mechanism.iron-monger"]
			self.assertEqual(2, len(monger["actuators"]))
			self.assertEqual(5, len(monger["sensors"]))
			self.assertEqual(2, len(monger["positions"]))
			self.assertIn("240-unit travel range", monger["behavior"])
			self.assertIn("Keep endpoint sensing tied to actual travel", monger["behavior"])
			self.assertIn("non-centering magnet force", mechanisms["mechanism.whiplash-magnet"]["behavior"])
			self.assertEqual(["switch.10-war-machine-opto"], mechanisms["mechanism.war-machine"]["sensors"])
			self.assertEqual([], mechanisms["mechanism.orbit-up-post"]["sensors"])
			self.assertEqual([], mechanisms["mechanism.center-lane-up-post"]["sensors"])
			self.assertEqual("500-6318-24-ND", mechanisms["mechanism.trough"]["assembly_part_number"])
			self.assertEqual(15, len(mechanisms["mechanism.routes"]["sensors"]))
			self.assertEqual(11, len(mechanisms["mechanism.fixed-targets"]["sensors"]))
			self.assertIn("Hit/UnHit", mechanisms["mechanism.routes"]["behavior"])
		self.assertIn("original 2010 multi-piece Iron Monger", {mechanism["id"]: mechanism for mechanism in self.original["mechanisms"]}["mechanism.iron-monger"]["behavior"])
		self.assertIn("strengthened one-piece molded Iron Monger", {mechanism["id"]: mechanism for mechanism in self.vault["mechanisms"]}["mechanism.iron-monger"]["behavior"])

	def test_cross_edition_multiplicity_is_structured_and_explicitly_qualified(self) -> None:
		expected_quantities = {20: 1, 21: 1, 22: 2, 23: 1, 25: 2, 26: 1, 27: 3, 28: 3, 29: 2, 30: 2, 31: 2, 32: 1}
		for definition in (self.original, self.vault):
			solenoids = bindings(definition, "outputs", "pinmame.output.solenoid")
			self.assertEqual(expected_quantities, {address: solenoids[address]["physical"]["quantity"] for address in expected_quantities})
		self.assertIn("Cross-edition evidence", bindings(self.original, "outputs", "pinmame.output.solenoid")[31]["physical"]["notes"])
		self.assertIn("2010 parts book does not number", bindings(self.original, "outputs", "pinmame.output.lamp")[55]["physical"]["notes"])

	def test_exact_manual_script_rom_and_runtime_hashes_are_pinned(self) -> None:
		for definition in (self.original, self.vault):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("0948d154156860d351daa943ab3b5882ef4c86bb42cde630bcd04067ab85ed1a", sources["manual.iron-man-original-parts.2010"]["sha256"])
			self.assertEqual("20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990", sources["manual.iron-man-vault-edition.2014"]["sha256"])
			self.assertEqual("d0d37548468d67aa895121fd6ff82fdacc1d1a301a702c92325fb3ee9d7a89ea", sources["vpx.iron-man-vault-vpw-1.0.1"]["sha256"])
			self.assertEqual("756dadd23ad0dd8cadd3cb98d25553a27788230cc3f8fe04ee39c7a7effce37c", sources["vpx.iron-man-vault-vpw-1.0"]["sha256"])
			self.assertEqual("e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f", sources["rom.iron-man-vault.im-185ve"]["sha256"])
			self.assertIn("c827da1c3f5305b27e9e504d7553bcd9c39547f357dd3827122adcc4c173c257", sources["rom.iron-man-vault.im-185ve"]["locator"])
			self.assertEqual("2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9", sources["runtime.iron-man-vault.boot-start"]["sha256"])
			self.assertIn("16 VAC secondary", sources["manual.iron-man-vault-edition.2014"]["locator"])
			model = "PINBALL I-00B0" if definition is self.vault else "I-00B3"
			ipdb = sources["ipdb.iron-man-vault-edition.6154"] if definition is self.vault else sources["ipdb.iron-man.5550"]
			self.assertIn(model, ipdb["locator"])
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertIn("human-review.stern.iron-man-code-1.86", switches[1]["provenance"]["source_refs"])
		vault_sources = {source["id"]: source for source in self.vault["sources"]}
		self.assertEqual("c0abc5d90d77a4cf7c3f0455cff91d4f0b9f7e750264742b987e9ddb30ab7a4b", vault_sources["vpx-table.iron-man-vault-vpw-1.0-geometry"]["sha256"])
		self.assertTrue(vault_sources["vpx-table.iron-man-vault-vpw-1.0-geometry"]["known_working"])

	def test_vault_spatial_inventory_disposes_every_device_and_preserves_physical_multiplicity(self) -> None:
		devices = self.vault["inputs"] + self.vault["outputs"]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		self.assertEqual(47, sum(device["spatial"]["status"] == "validated" for device in self.vault["inputs"]))
		self.assertEqual(89, sum(device["spatial"]["status"] == "validated" for device in self.vault["outputs"]))
		switches = bindings(self.vault, "inputs", "pinmame.input.switch")
		self.assertEqual((0.446429, 0.42113), tuple(switches[1]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.930439, 0.845121), tuple(switches[22]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual(["vpx-table.iron-man-vault-vpw-1.0-geometry"], switches[22]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertIn("least-squares continuation", switches[22]["physical"]["notes"])
		self.assertEqual(["flipper.lower.left.button"], switches[84]["roles"])
		self.assertEqual(["flipper.lower.right.button"], switches[82]["roles"])
		self.assertEqual(["cabinet.tournament-start"], switches[15]["roles"])

		solenoids = bindings(self.vault, "outputs", "pinmame.output.solenoid")
		expected_quantities = {20: 1, 21: 1, 22: 2, 23: 1, 25: 2, 26: 1, 27: 3, 28: 3, 29: 2, 30: 2, 31: 2, 32: 1}
		self.assertEqual(expected_quantities, {address: solenoids[address]["physical"]["quantity"] for address in expected_quantities})
		self.assertEqual(3, len(solenoids[27]["spatial"]["placements"]))
		self.assertEqual(2, len(solenoids[31]["spatial"]["placements"]))
		for address in expected_quantities:
			self.assertEqual(expected_quantities[address], len(solenoids[address]["spatial"]["placements"]))
		for address in (22, 28):
			self.assertIn("shared assembly/cluster anchor", solenoids[address]["physical"]["notes"])
		self.assertEqual([(0.410511, 0.720898), (0.563715, 0.721215)], [tuple(point[axis] for axis in ("x", "y")) for point in solenoids[30]["spatial"]["placements"]])
		self.assertEqual([(0.055666, 0.542583), (0.05488, 0.614537)], [tuple(point[axis] for axis in ("x", "y")) for point in solenoids[31]["spatial"]["placements"]])
		for address in (30, 31):
			self.assertTrue(all(point["provenance"]["source_refs"] == ["manual.iron-man-vault-edition.2014"] for point in solenoids[address]["spatial"]["placements"]))
		self.assertEqual(["manual.iron-man-vault-edition.2014"], solenoids[27]["spatial"]["placements"][2]["provenance"]["source_refs"])
		self.assertIn("official coil-location map marks two", solenoids[31]["physical"]["notes"])

		lamps = bindings(self.vault, "outputs", "pinmame.output.lamp")
		self.assertEqual((2, 2), (lamps[55]["physical"]["quantity"], len(lamps[55]["spatial"]["placements"])))
		self.assertEqual([(0.484716, 0.68168), (0.484376, 0.707115)], [tuple(point[axis] for axis in ("x", "y")) for point in lamps[55]["spatial"]["placements"]])
		self.assertTrue(all(point["provenance"]["source_refs"] == ["manual.iron-man-vault-edition.2014"] for point in lamps[55]["spatial"]["placements"]))
		self.assertIn("individual placement IDs", lamps[55]["physical"]["notes"])
		for address in (73, 79, 80):
			self.assertEqual(("not_applicable", "internal_nonvisual"), (lamps[address]["spatial"]["status"], lamps[address]["spatial"]["reason"]))

		gi = bindings(self.vault, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(39, gi["physical"]["quantity"])
		self.assertEqual(37, len(gi["spatial"]["placements"]))
		self.assertEqual(10, sum(point["y"] == 0 for point in gi["spatial"]["placements"]))
		self.assertEqual({"brown": 10, "yellow": 7, "violet": 10, "green": 10}, {
			circuit: sum(f".{circuit}." in point["id"] for point in gi["spatial"]["placements"])
			for circuit in ("brown", "yellow", "violet", "green")
		})
		self.assertIn("European cabinets use three", gi["physical"]["notes"])
		self.assertIn("gi024/gi027/gi030/gi031", gi["physical"]["notes"])
		self.assertIn("25 under-playfield #44 bulbs plus two above-playfield #555 bulbs", gi["physical"]["notes"])
		self.assertIn("gi004/gi014", gi["physical"]["notes"])
		gi_points = {point["id"]: point for point in gi["spatial"]["placements"]}
		self.assertEqual((0.230629, 0.685078), tuple(gi_points["gi.master.emitter.yellow.above-playfield-555"][axis] for axis in ("x", "y")))
		self.assertEqual((0.743541, 0.692584), tuple(gi_points["gi.master.emitter.violet.above-playfield-555"][axis] for axis in ("x", "y")))
		self.assertTrue(all(point["provenance"]["source_refs"] == ["vpx-table.iron-man-vault-vpw-1.0-geometry"] for point in gi["spatial"]["placements"][:27]))
		self.assertTrue(all(point["provenance"]["source_refs"] == ["manual.iron-man-vault-edition.2014"] for point in gi["spatial"]["placements"][27:]))

		for device in devices:
			if device["spatial"]["status"] == "validated":
				for point in device["spatial"]["placements"]:
					self.assertGreaterEqual(point["x"], 0)
					self.assertLessEqual(point["x"], 1)
					self.assertGreaterEqual(point["y"], 0)
					self.assertLessEqual(point["y"], 1)

	def test_runtime_evidence_records_exact_observed_addresses(self) -> None:
		self.assertEqual(["stern.iron-man.2010", "stern.iron-man-vault-edition.2014"], self.evidence["machine_ids"])
		self.assertEqual(["im_185ve"], self.evidence["driver_ids"])
		runtime = self.evidence["runtime"]
		self.assertEqual("e04c56ca08cdd6b0aaa6fcacd601e183d338dae7a863a4486216f76b25d6738f", runtime["rom_archive_sha256"])
		self.assertEqual("2b1f7d59482a7428eaf4413dfa3fdf25a5eccc8bdad5479da5532947cecbdab9", runtime["raw_runs"][0]["sha256"])
		self.assertEqual({1} | set(range(3, 64)), set(runtime["observations"]["lamp_addresses_seen"]))
		self.assertEqual([33], runtime["observations"]["solenoid_addresses_seen"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		self.assertIn("--initial-switch 1", runtime["command_template"])
		self.assertEqual(6, runtime["command_template"].count("--pulse 65:300"))

	def test_ids_bindings_and_actuator_ownership_are_unique(self) -> None:
		for definition in (self.original, self.vault):
			for collection in (definition["inputs"], definition["outputs"]):
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))
				controller_bindings = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(controller_bindings), len(set(controller_bindings)))
			actuators = [actuator for mechanism in definition["mechanisms"] for actuator in mechanism["actuators"]]
			self.assertEqual(len(actuators), len(set(actuators)))


if __name__ == "__main__":
	unittest.main()
