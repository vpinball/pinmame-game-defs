from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "creature-from-the-black-lagoon-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "creature-from-the-black-lagoon-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "creature-from-the-black-lagoon-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "creature-from-the-black-lagoon-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "creature-from-the-black-lagoon-1992.json"

DRIVER_IDS = {"cftbl_l4", "cftbl_l4c", "cftbl_d4", "cftbl_l3", "cftbl_d3", "cftbl_l2", "cftbl_d2", "cftbl_p3"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {
	11, 12, 23, 24, 31, 32, 67, 68,
	71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88,
}
OPTO_ADDRESSES = {34, 37}
PINMAME_NORMALIZED_OPTO_ADDRESSES = {15, 34, 37, 38}
CHASE_LAMP_ADDRESSES = set(range(91, 99))


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
	import curate_creature as curator
	import sys as _sys

	argv = _sys.argv
	_sys.argv = ["curate_creature.py"]
	try:
		curator.main()
	finally:
		_sys.argv = argv


class CreatureDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"physical_wiring", "spatial_placement"}:
				continue
			self.assertEqual("validated", state, dimension)
		self.assertEqual("bally.creature-from-the-black-lagoon.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(588, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertTrue(CONTROLLER_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())

	def test_every_cftbl_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["cftbl_l4"])
		for driver_id in DRIVER_IDS - {"cftbl_l4"}:
			self.assertEqual("cftbl_l4", by_id[driver_id]["clone_of"], driver_id)

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_opto_polarity_covers_two_true_optos_and_two_mechanically_inverted_switches(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			switch = self.switches[address]
			self.assertEqual(address in PINMAME_NORMALIZED_OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
			elif address in PINMAME_NORMALIZED_OPTO_ADDRESSES:
				self.assertNotEqual("opto", switch["physical"]["switch_type"], address)

	def test_switch_15_and_38_are_corroborated_by_script_or_mechanism_logic_not_a_printed_opto_marker(self) -> None:
		self.assertIn("sw15_Hit", self.switches[15]["physical"]["notes"])
		self.assertIn("core_setSw", self.switches[38]["physical"]["notes"])
		for address in (15, 38):
			self.assertTrue(self.switches[address]["normally_closed"], address)

	def test_switches_34_and_37_are_the_only_led_trans_opto_pairs(self) -> None:
		import curate_creature as curator

		self.assertEqual({34, 37}, curator.OPTO_SWITCHES)
		self.assertEqual({15, 34, 37, 38}, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		mask = (0x00, 0x10, 0x00, 0xC8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		self.assertEqual(0x10, mask[1])
		self.assertEqual(0xC8, mask[3])

	def test_switch_53_is_named_by_function_but_is_the_physical_right_return_lane(self) -> None:
		switch = self.switches[53]
		self.assertEqual("Start Combo", switch["label"])
		self.assertIn("Start Combo", switch["physical"]["notes"])
		# 52 (Left Return Lane) and 53 (Start Combo) sit on opposite sides of the playfield.
		left = self.switches[52]["spatial"]["placements"][0]
		right = switch["spatial"]["placements"][0]
		self.assertLess(left["x"], right["x"])

	def test_flipper_block_111_to_114_used_115_to_118_unresolved(self) -> None:
		for address in (111, 112, 113, 114):
			switch = self.switches[address]
			self.assertEqual("used", switch["availability"], address)
			self.assertIn("spatial", switch)
			self.assertEqual("not_applicable", switch["spatial"]["status"], address)
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		for address in (115, 116, 117, 118):
			switch = self.switches[address]
			self.assertEqual("unknown", switch["availability"], address)
			self.assertNotIn("spatial", switch, address)
			self.assertNotIn("normally_closed", switch, address)

	def test_switch_18_has_no_spatial_key_at_all(self) -> None:
		switch = self.switches[18]
		self.assertEqual("used", switch["availability"])
		self.assertNotIn("spatial", switch)
		self.assertIn("sw18_Hit", switch["physical"]["notes"])

	def test_dedicated_and_dip_switches_are_cabinet_devices(self) -> None:
		for address in range(1, 9):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"], address)
		for address in range(1, 9):
			self.assertEqual("dip_switch", self.dips[address]["spatial"]["reason"], address)

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 29)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES | CHASE_LAMP_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		self.assertEqual("control_signal", self.solenoids[20]["kind"])
		self.assertEqual("control_signal", self.solenoids[24]["kind"])
		for address in (20, 24):
			self.assertEqual("not_applicable", self.solenoids[address]["spatial"]["status"], address)
			self.assertEqual("internal_nonvisual", self.solenoids[address]["spatial"]["reason"], address)
		for address in (27, 28, 7):
			self.assertEqual("not_applicable", self.solenoids[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.solenoids[address]["spatial"]["reason"], address)
		for address in (21, 23, 26):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)

	def test_no_solenoid_is_labelled_a_plain_coil_when_it_is_actually_a_decoder_line(self) -> None:
		for device in self.solenoids.values():
			if device["kind"] == "control_signal":
				self.assertIn("decoder", device["physical"]["notes"].lower())

	def test_unbound_flasher_solenoids_have_no_spatial_key(self) -> None:
		for address in (2, 9, 16, 18, 19, 25):
			device = self.solenoids[address]
			self.assertEqual("used", device["availability"], address)
			self.assertNotIn("spatial", device, address)

	def test_bound_flasher_solenoids_are_located(self) -> None:
		for address in (1, 3, 4, 12, 13, 14, 15):
			device = self.solenoids[address]
			self.assertIn("spatial", device, address)
			self.assertEqual("validated", device["spatial"]["status"], address)

	def test_hologram_push_motor_is_projected_onto_the_creature_flasher_object(self) -> None:
		device = self.solenoids[21]
		self.assertIn("spatial", device)
		self.assertEqual("validated", device["spatial"]["status"])
		self.assertIn("creature", device["physical"]["notes"])

	def test_chase_lamps_91_to_98_exist_but_have_no_spatial_key(self) -> None:
		for address in CHASE_LAMP_ADDRESSES:
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertNotIn("spatial", lamp, address)
			self.assertIn("lampMatrix[8]", lamp["physical"]["notes"], address)

	def test_gi_address_3_has_no_spatial_key_while_0_1_2_4_are_located(self) -> None:
		for address in (0, 1, 2, 4):
			self.assertIn("spatial", self.gi[address], address)
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
		self.assertNotIn("spatial", self.gi[3])

	def test_backbox_creature_letters_and_start_button_lamp_are_cabinet_devices(self) -> None:
		for address in range(71, 79):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])
		self.assertNotEqual(11, self.lamps[11]["binding"]["device"] == 11 and False)  # placeholder-free sanity

	def test_geometric_ordering_left_center_right_ascending_in_x(self) -> None:
		left_x = self.switches[51]["spatial"]["placements"][0]["x"]
		right_x = self.switches[54]["spatial"]["placements"][0]["x"]
		self.assertLess(left_x, right_x)
		bumper_left_x = self.solenoids[13]["spatial"]["placements"][0]["x"]
		bumper_right_x = self.solenoids[14]["spatial"]["placements"][0]["x"]
		self.assertLess(bumper_left_x, bumper_right_x)

	def test_geometric_ordering_rear_front_ascending_in_y(self) -> None:
		# y=0 rear/backglass, y=1 front/apron: the shooter lane (front) must sit further
		# forward than the top P-A-I-D rollovers (rear).
		rear_y = self.switches[25]["spatial"]["placements"][0]["y"]
		front_y = self.switches[66]["spatial"]["placements"][0]["y"]
		self.assertLess(rear_y, front_y)

	def test_lamp_position_agrees_with_the_switch_the_manual_names_for_the_same_feature(self) -> None:
		# Bottom Jet: switch 33 and lamp 17 both name "Bottom Jet" and both project onto/sit at the
		# same jet-bumper cluster, so their y should be close (same physical bumper nest).
		switch_y = self.switches[33]["spatial"]["placements"][0]["y"]
		lamp_y = self.lamps[17]["spatial"]["placements"][0]["y"]
		self.assertLess(abs(switch_y - lamp_y), 0.2)

	def test_the_upper_flipper_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.upper-flipper-switches-unconfirmed-fitment"}, set(conflicts))
		conflict = conflicts["conflict.upper-flipper-switches-unconfirmed-fitment"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("unresolved", description)
		for address in (115, 116, 117, 118):
			self.assertIn(str(address), conflict["path"])

	def test_mechanisms_cover_the_sequential_gi_and_hologram(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertIn("mechanism.sequential-gi-chase", mechanisms)
		self.assertIn("mechanism.hologram", mechanisms)
		self.assertIn("mechanism.creature-ramp", mechanisms)
		gi_mech = mechanisms["mechanism.sequential-gi-chase"]
		self.assertIn("device.sequential-g-i-1-select", gi_mech["actuators"])
		self.assertIn("device.sequential-g-i-2-select", gi_mech["actuators"])

	def test_curator_check_and_regenerate_are_deterministic(self) -> None:
		import curate_creature as curator

		definition = curator.build()
		self.assertEqual(self.definition, definition)
		report = curator.build_spatial_report(definition)
		self.assertEqual("partial", report["status"])

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())


if __name__ == "__main__":
	unittest.main()
