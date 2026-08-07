from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "cactus-canyon-1998.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "cactus-canyon-1998.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "cactus-canyon-1998.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "cactus-canyon-1998.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "cactus-canyon-1998.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "bally" / "cactus-canyon-1998.md"

DRIVER_IDS = {"cc_10", "cc_104", "cc_12", "cc_13", "cc_13k"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 25, 38, 43, 45, 74, 76, 81, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37, 41, 42, 71, 77, 78}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def _run_curator_without_mode() -> None:
	"""Invoke the curator's CLI with no mode so argparse rejects it instead of writing files."""
	import curate_cactus_canyon as curator

	argv = sys.argv
	sys.argv = ["curate_cactus_canyon.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


def _placement_xy(spatial: dict[str, object]) -> tuple[float, float]:
	placement = spatial["placements"][0]
	return float(placement["x"]), float(placement["y"])


class CactusCanyonDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "spatial_placement":
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.cactus-canyon.1998", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(4445, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1998, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_no_opto_polarity_conflict_is_recorded(self) -> None:
		# Unlike Monster Bash's Dracula-position column, the full opto sweep found
		# ccGameData normalizes every physically normally-closed opto -- so this
		# machine's conflicts array must be empty.
		self.assertEqual([], self.definition["conflicts"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_MARKDOWN_PATH.is_file())
		self.assertTrue(CONTROLLER_PATH.is_file())

	def test_every_cc_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("cc_13", by_id["cc_10"]["clone_of"])
		self.assertEqual("cc_13", by_id["cc_12"]["clone_of"])
		self.assertEqual("cc_13", by_id["cc_104"]["clone_of"])
		self.assertEqual("cc_13", by_id["cc_13k"]["clone_of"])
		self.assertNotIn("clone_of", by_id["cc_13"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)
		# There are no upper flippers: 115-118 are unused, 111-114 are used.
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_is_normalized_for_every_opto(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertIn("opto", switch["physical"]["switch_type"], address)
		for address in (112, 114):
			self.assertTrue(self.switches[address]["normally_closed"], address)

	def test_always_closed_switch_is_constant(self) -> None:
		switch = self.switches[24]
		self.assertEqual("constant", switch["kind"])
		self.assertTrue(switch["constant_active"])
		self.assertTrue(switch["initial_active"])

	def test_solenoid_7_and_23_are_enumerated_unfitted_not_missing(self) -> None:
		for address in (7, 23):
			solenoid = self.solenoids[address]
			self.assertEqual("unused", solenoid["availability"], address)
			self.assertEqual("unused", solenoid["spatial"]["reason"], address)

	def test_lpdc_train_motor_mirrors_are_virtual_not_duplicate_devices(self) -> None:
		for address in (41, 42):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"], address)
			self.assertEqual("virtual", solenoid["spatial"]["reason"], address)
		fitted_train = {self.solenoids[37]["label"], self.solenoids[38]["label"]}
		self.assertEqual({"Train Reverse", "Train Forward"}, fitted_train)

	def test_bart_toy_repurposes_upper_flipper_solenoid_circuit_asymmetrically(self) -> None:
		self.assertEqual("Move Bart Toy", self.solenoids[33]["label"])
		self.assertEqual("Bart Toy Hat", self.solenoids[36]["label"])
		self.assertEqual("unused", self.solenoids[34]["availability"])
		self.assertEqual("unused", self.solenoids[35]["availability"])

	def test_flipper_lower_flipper_public_addresses_carry_manual_alias(self) -> None:
		expected = {45: "29", 46: "30", 47: "31", 48: "32"}
		for address, manual_address in expected.items():
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(manual_address, aliases["manual.address"], address)

	def test_flasher_dual_bulb_addresses_declare_two_quantity_but_only_two_have_two_placements(self) -> None:
		dual_bulb_addresses = (24, 26, 27, 28)
		for address in dual_bulb_addresses:
			solenoid = self.solenoids[address]
			self.assertEqual(2, solenoid["physical"]["quantity"], address)
		# 27/28 resolve two distinguishable coordinates; 24/26 do not (documented gap).
		self.assertEqual(2, len(self.solenoids[27]["spatial"]["placements"]))
		self.assertEqual(2, len(self.solenoids[28]["spatial"]["placements"]))
		self.assertEqual(1, len(self.solenoids[24]["spatial"]["placements"]))
		self.assertEqual(1, len(self.solenoids[26]["spatial"]["placements"]))

	def test_lamp_matrix_is_enumerated_with_correct_unused_positions(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address in (85, 86, 87):
			self.assertEqual("unused", self.lamps[address]["availability"], address)
		for address in MATRIX_ADDRESSES - {85, 86, 87}:
			self.assertEqual("used", self.lamps[address]["availability"], address)
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])

	def test_lamp_23_excludes_the_second_render_object(self) -> None:
		lamp = self.lamps[23]
		self.assertEqual(1, len(lamp["spatial"]["placements"]))
		self.assertEqual(1, lamp["physical"]["quantity"])

	def test_gi_addresses_zero_through_four_are_enumerated(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))
		self.assertEqual(10, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(12, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(16, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"])

	def test_geometric_ordering_left_right_ascending(self) -> None:
		# Slingshots: left (51) west of right (52).
		self.assertLess(_placement_xy(self.switches[51]["spatial"])[0], _placement_xy(self.switches[52]["spatial"])[0])
		# Jet bumpers: left (53) west of right (54); bottom (55) is further toward the player (higher y) than both.
		left_x, left_y = _placement_xy(self.switches[53]["spatial"])
		right_x, right_y = _placement_xy(self.switches[54]["spatial"])
		bottom_x, bottom_y = _placement_xy(self.switches[55]["spatial"])
		self.assertLess(left_x, right_x)
		self.assertGreater(bottom_y, left_y)
		self.assertGreater(bottom_y, right_y)
		# Gunfight posts: left solenoid 14 west of right solenoid 15.
		self.assertLess(_placement_xy(self.solenoids[14]["spatial"])[0], _placement_xy(self.solenoids[15]["spatial"])[0])
		# Lower flippers: right flipper (45/46) west of... no, left flipper (47/48) is west of right (45/46).
		self.assertLess(_placement_xy(self.solenoids[47]["spatial"])[0], _placement_xy(self.solenoids[45]["spatial"])[0])
		# Drop target bank ascends left to right across all four targets.
		xs = [_placement_xy(self.switches[address]["spatial"])[0] for address in (61, 62, 63, 64)]
		self.assertEqual(sorted(xs), xs)
		# Loop gates: left gate west of right gate.
		self.assertLess(_placement_xy(self.solenoids[21]["spatial"])[0], _placement_xy(self.solenoids[22]["spatial"])[0])

	def test_flipper_switch_matches_flipper_solenoid_side(self) -> None:
		# Lower right flipper button switch (112) should be on the same side as the
		# lower right flipper solenoid (45/46), and likewise for left (114 vs 47/48).
		right_switch_x = _placement_xy(self.switches[112]["spatial"])[0]
		left_switch_x = _placement_xy(self.switches[114]["spatial"])[0]
		right_solenoid_x = _placement_xy(self.solenoids[45]["spatial"])[0]
		left_solenoid_x = _placement_xy(self.solenoids[47]["spatial"])[0]
		self.assertLess(left_switch_x, right_switch_x)
		self.assertLess(left_solenoid_x, right_solenoid_x)

	def test_train_and_mine_projected_switches_share_mechanism_coordinate(self) -> None:
		# Switches 71/72 both project onto the train mechanism; 77/78 both project
		# onto the mine mechanism; the two mechanisms are at different locations.
		self.assertEqual(_placement_xy(self.switches[71]["spatial"]), _placement_xy(self.switches[72]["spatial"]))
		self.assertEqual(_placement_xy(self.switches[77]["spatial"]), _placement_xy(self.switches[78]["spatial"]))
		self.assertNotEqual(_placement_xy(self.switches[71]["spatial"]), _placement_xy(self.switches[77]["spatial"]))

	def test_dip_switches_are_cabinet_service_devices(self) -> None:
		dips = bindings(self.definition, "inputs", "pinmame.input.dip")
		self.assertEqual(set(range(1, 9)), set(dips))
		for dip in dips.values():
			self.assertEqual("not_applicable", dip["spatial"]["status"])

	def test_display_is_cabinet_hardware(self) -> None:
		display = self.definition["displays"][0]
		self.assertEqual("dmd", display["kind"])
		self.assertEqual("not_applicable", display["spatial"]["status"])
		self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_mechanisms_reference_only_declared_devices(self) -> None:
		switch_ids = set(self.definition["inputs"] and [item["id"] for item in self.definition["inputs"]])
		output_ids = {item["id"] for item in self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			for sensor in mechanism["sensors"]:
				self.assertIn(sensor, switch_ids, mechanism["id"])
			for actuator in mechanism["actuators"]:
				self.assertIn(actuator, output_ids, mechanism["id"])

	def test_seed_is_byte_identical_to_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_is_idempotent(self) -> None:
		import curate_cactus_canyon as curator

		curator.check(ROOT)
		curator.check(ROOT)


class CactusCanyonCatalogReconciliationTests(unittest.TestCase):
	def test_catalog_binds_every_cc_driver_to_this_definition(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		by_id = {record["id"]: record for record in catalog["drivers"]}
		for driver_id in DRIVER_IDS:
			self.assertIn(driver_id, by_id)
			record = by_id[driver_id]
			self.assertEqual("bally.cactus-canyon.1998", record["machine_id"])
			self.assertEqual("machines/partial/bally/cactus-canyon-1998.json", record["definition"])
			self.assertEqual("partial", record["coverage_status"])
			self.assertEqual("cc_13", record["root_driver"])


if __name__ == "__main__":
	unittest.main()
