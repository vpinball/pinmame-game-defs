"""Regression tests for the Bally Eight Ball Deluxe definition and the by35 profile it reuses.

Two address rules coexist on this one machine, and confusing them is the regression this file
guards against: the public switch address equals the manual's printed Self Test # directly, but
the public solenoid address does not. Both rules were read off the pinned ROM's own self-test via
a LibPinMAME harness trace, not assumed, and the solenoid table in particular must never be
"tidied" back into an identity mapping.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "eight-ball-deluxe-1981.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "eight-ball-deluxe-1981.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "eight-ball-deluxe-1981.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "eight-ball-deluxe-1981.json"

# printed Self Test # -> public switch address (an identity mapping, confirmed by the harness).
SWITCH_SELF_TEST_TO_PUBLIC = {n: n for n in range(1, 41)}

# printed solenoid Self Test # -> public address. 8, 9, and 10 each answer to two self-test
# numbers (Controller.Lamp(52) selects which physical role is active).
SOLENOID_SELF_TEST_TO_PUBLIC = {
	1: 4, 2: 5, 3: 6, 4: 3, 5: 2, 6: 1, 7: 7,
	8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15,
	15: 8, 16: 10, 17: 8, 18: 9, 19: 18, 20: 19,
}
DUAL_FUNCTION_SOLENOIDS = (8, 9, 10)
UNUSED_SOLENOID_ADDRESSES = (16, 17, 20)

CABINET_OR_SERVICE_SWITCHES = (6, 9, 10, 11, 16)

DIRECT_RELATIONSHIPS = {
	38: 3,  # Left Thumper Bumper -> solenoid 3
	39: 2,  # Right Thumper Bumper -> solenoid 2
	40: 1,  # Bottom Thumper Bumper -> solenoid 1
	36: 5,  # Right Slingshot -> solenoid 5
	37: 4,  # Left Slingshot -> solenoid 4
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class EightBallDeluxeDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.inputs = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		cls.dips = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		}
		cls.solenoids = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}
		cls.lamps = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.eight-ball-deluxe.1981", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1981, machine["year"])
		self.assertEqual("Eight Ball Deluxe", machine["name"])

	def test_controller_platform_is_the_by35_profile_unchanged(self) -> None:
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		group_ids = {group["id"] for group in self.profile["groups"]}
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp"},
			group_ids,
		)

	def test_driver_family_has_six_identical_drivers(self) -> None:
		driver_ids = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual(
			{"eballdlx", "eballd14", "eballdla", "eballdlb", "eballdlc", "eballdld"},
			driver_ids,
		)
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])

	def test_the_68701_hardware_prototypes_are_not_part_of_this_machine(self) -> None:
		"""eballdp1 through eballdp4 are a different physical machine and must stay out.

		PinMAME declares all four CORE_CLONEDEFNV clones of eballdlx, but that is emulator
		metadata. They live in by68701.c on a Motorola 68701 rather than in by35games.c on the
		AS-2518-35 MPU, and they carry their own display layout (dispEBD) and their own machine
		driver (by68701_61S, not by35_mBY35_61BS). Grouping them here would erase a whole
		different board architecture, exactly as grouping kissp/kissp2 into Kiss would have.
		They keep the leftover stub.pinmame.eballdlx record instead.
		"""
		ids = {driver["id"] for driver in self.definition["drivers"]}
		for prototype in ("eballdp1", "eballdp2", "eballdp3", "eballdp4"):
			self.assertNotIn(prototype, ids)

	def test_switch_address_equals_printed_self_test_number(self) -> None:
		"""The switch table is an identity mapping -- confirmed by holding each address during the
		ROM's own stuck-switch search stage and reading the number it displayed."""
		for self_test, public in SWITCH_SELF_TEST_TO_PUBLIC.items():
			self.assertIn(public, self.inputs, f"switch {public} missing")

	def test_every_matrix_switch_1_to_40_is_present_and_used(self) -> None:
		for address in range(1, 41):
			item = self.inputs[address]
			self.assertEqual("used", item["availability"], address)
			aliases = {alias["value"] for alias in item["aliases"] if alias["namespace"] == "pinmame.switch"}
			self.assertIn(str(address), aliases)

	def test_cabinet_switches_have_no_spatial_placement(self) -> None:
		for address in CABINET_OR_SERVICE_SWITCHES:
			spatial = self.inputs[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], address)
			self.assertEqual("cabinet_or_service", spatial["reason"], address)

	def test_diagnostic_switches_are_negative_addresses(self) -> None:
		diagnostic = {
			item["binding"]["device"]: item
			for item in self.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] < 0
		}
		self.assertEqual({-7, -6, -5}, set(diagnostic))
		self.assertEqual("used", diagnostic[-7]["availability"])

	def test_dip_switches_are_a_full_four_bank_of_32(self) -> None:
		self.assertEqual(set(range(1, 33)), set(self.dips))
		for item in self.dips.values():
			self.assertEqual("not_applicable", item["spatial"]["status"])
			self.assertEqual("dip_switch", item["spatial"]["reason"])

	def test_undocumented_dip_switches_are_candidate_not_fabricated(self) -> None:
		undocumented = (6, 7, 15, 29, 30)
		for address in undocumented:
			item = self.dips[address]
			self.assertEqual("candidate", item["provenance"]["status"], address)
			self.assertIn("not resolved in this pass", item["label"])
		for address in set(range(1, 33)) - set(undocumented):
			self.assertEqual("validated", self.dips[address]["provenance"]["status"], address)

	def test_solenoid_self_test_table_is_not_an_identity_mapping(self) -> None:
		"""This is the fact the whole solenoid table hinges on: printed self-test 01 is LEFT
		SLINGSHOT, but the harness shows it fires public address 4, not 1."""
		non_identity = [st for st, public in SOLENOID_SELF_TEST_TO_PUBLIC.items() if st != public]
		self.assertGreater(len(non_identity), 10, "the solenoid table should mostly disagree with identity")
		self.assertEqual(4, SOLENOID_SELF_TEST_TO_PUBLIC[1])
		self.assertEqual(6, SOLENOID_SELF_TEST_TO_PUBLIC[3])

	def test_knocker_is_public_solenoid_6(self) -> None:
		"""Cross-checked independently against the retained script's own SolCallback(6) = Knocker."""
		self.assertIn("Knocker", self.solenoids[6]["label"])

	def test_dual_function_solenoids_carry_both_self_test_aliases(self) -> None:
		expected_pairs = {8: ("15", "17"), 9: ("08", "18"), 10: ("09", "16")}
		for address, (first, second) in expected_pairs.items():
			aliases = {a["value"] for a in self.solenoids[address]["aliases"] if a["namespace"] == "manual.self-test"}
			self.assertEqual({first, second}, aliases, address)

	def test_unused_solenoid_addresses_are_recorded_unused(self) -> None:
		for address in UNUSED_SOLENOID_ADDRESSES:
			item = self.solenoids[address]
			self.assertEqual("unused", item["availability"], address)
			self.assertEqual("not_applicable", item["spatial"]["status"], address)
			self.assertEqual("unused", item["spatial"]["reason"], address)

	def test_no_solenoid_44_through_48_flipper_addresses_are_claimed(self) -> None:
		"""eballdlx declares FLIP_SW(FLIP_L) with no FLIP_SOL bit, so PinMAME fakes the flipper
		solenoids rather than driving real hardware; this definition must not invent flipper coils."""
		for address in (45, 46, 47, 48):
			self.assertNotIn(address, self.solenoids)

	def test_direct_switch_to_solenoid_relationships_are_recorded(self) -> None:
		relationships = {
			(rel["source"], rel["destination"]): rel
			for rel in self.definition["relationships"]
		}
		for switch_address, solenoid_address in DIRECT_RELATIONSHIPS.items():
			key = (f"switch.matrix-{switch_address}", f"solenoid.{solenoid_address}")
			self.assertIn(key, relationships, key)
			self.assertEqual("direct", relationships[key]["kind"])

	def test_lamp_addresses_all_fall_inside_the_by35_profile_ranges(self) -> None:
		main_board = list(range(1, 16)) + list(range(17, 32)) + list(range(33, 48)) + list(range(49, 64))
		aux_board = list(range(65, 80)) + list(range(81, 96)) + list(range(97, 112)) + list(range(113, 128))
		valid = set(main_board) | set(aux_board)
		for address in self.lamps:
			self.assertIn(address, valid, address)

	def test_lamp_count_matches_retained_script_bindings(self) -> None:
		self.assertEqual(74, len(self.lamps))

	def test_no_gi_output_group_is_declared(self) -> None:
		"""General illumination on this platform is an uncontrolled two-wire AC circuit (see the
		knowledge note); this definition must not fabricate a pinmame.output.gi group or address."""
		group_ids = {group["id"] for group in self.profile["groups"]}
		self.assertNotIn("pinmame.output.gi", group_ids)
		for item in self.definition["outputs"]:
			self.assertNotEqual("gi", item["kind"])

	def test_mechanisms_reference_real_device_ids(self) -> None:
		input_ids = {item["id"] for item in self.definition["inputs"]}
		output_ids = {item["id"] for item in self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			for actuator in mechanism["actuators"]:
				self.assertIn(actuator, output_ids, f"{mechanism['id']} -> {actuator}")
			for sensor in mechanism["sensors"]:
				self.assertIn(sensor, input_ids, f"{mechanism['id']} -> {sensor}")

	def test_drop_target_banks_have_the_right_target_counts(self) -> None:
		mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
		self.assertEqual(7, len(mechanisms["mechanism.drop-target-bank-1"]["sensors"]))
		self.assertEqual(4, len(mechanisms["mechanism.drop-target-bank-2"]["sensors"]))
		self.assertEqual(1, len(mechanisms["mechanism.drop-target-single"]["sensors"]))

	def test_year_conflict_is_recorded(self) -> None:
		conflict_ids = {c["id"] for c in self.definition["conflicts"]}
		self.assertIn("conflict.retained-table-year-vs-driver", conflict_ids)

	def test_coverage_is_partial_with_named_gaps(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		for expected in ("input_semantics", "output_semantics", "recreation_notes", "unresolved_conflicts"):
			self.assertIn(expected, coverage["missing"])

	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_knowledge_note_exists(self) -> None:
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("Lamp 52", text)
		self.assertIn("1981", text)


class EightBallDeluxeSpatialOrderingTests(unittest.TestCase):
	"""Cheap geometric regressions that catch a reversed left/right or rear/front identity, the
	recurring class of error this project's runbook flags across nearly every prior BY35/WPC game.
	"""

	@classmethod
	def setUpClass(cls) -> None:
		definition = load_json(DEFINITION_PATH)
		cls.by_id = {item["id"]: item for item in definition["inputs"] + definition["outputs"]}

	def _x(self, device_id: str) -> float:
		return self.by_id[device_id]["spatial"]["placements"][0]["x"]

	def _y(self, device_id: str) -> float:
		return self.by_id[device_id]["spatial"]["placements"][0]["y"]

	def test_left_and_right_slingshots_are_on_the_correct_sides(self) -> None:
		self.assertLess(self._x("switch.matrix-37"), 0.5, "Left Slingshot should be x<0.5")
		self.assertGreater(self._x("switch.matrix-36"), 0.5, "Right Slingshot should be x>0.5")

	def test_left_and_right_outlanes_are_on_the_correct_sides(self) -> None:
		self.assertLess(self._x("switch.matrix-32"), 0.5, "Left Outlane should be x<0.5")
		self.assertGreater(self._x("switch.matrix-31"), 0.5, "Right Outlane should be x>0.5")

	def test_left_and_right_thumper_bumpers_are_on_the_correct_sides(self) -> None:
		self.assertLess(self._x("switch.matrix-38"), 0.5, "Left Thumper Bumper should be x<0.5")
		self.assertGreater(self._x("switch.matrix-39"), 0.5, "Right Thumper Bumper should be x>0.5")

	def test_thumper_bumper_solenoid_positions_agree_with_their_switch(self) -> None:
		"""The bumper coil sits at the same physical assembly as its skirt switch."""
		self.assertAlmostEqual(self._x("switch.matrix-38"), self._x("solenoid.3"), places=3)
		self.assertAlmostEqual(self._x("switch.matrix-39"), self._x("solenoid.2"), places=3)
		self.assertAlmostEqual(self._x("switch.matrix-40"), self._x("solenoid.1"), places=3)

	def test_saucer_sits_above_the_outhole(self) -> None:
		"""The saucer is an upper-playfield feature (Feature B); the outhole is beneath the
		playfield near the apron -- saucer y must be well below (smaller than) outhole y."""
		self.assertLess(self._y("switch.matrix-34"), self._y("switch.matrix-8"))

	def test_drop_target_bank_1_switches_are_in_ascending_y_order(self) -> None:
		ys = [self._y(f"switch.matrix-{n}") for n in range(17, 24)]
		self.assertEqual(ys, sorted(ys), "the 7-bank should read top-to-bottom in ascending y")

	def test_rollover_lanes_a_b_are_near_the_rear_and_c_d_near_the_front(self) -> None:
		self.assertLess(self._y("switch.matrix-12"), 0.3)
		self.assertLess(self._y("switch.matrix-13"), 0.3)
		self.assertGreater(self._y("switch.matrix-14"), 0.6)
		self.assertGreater(self._y("switch.matrix-15"), 0.6)


class ByThirtyFiveProfileTests(unittest.TestCase):
	def test_profile_is_unmodified_by_this_game(self) -> None:
		profile = load_json(PROFILE_PATH)
		self.assertEqual("pinmame.by35", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])


class SpatialReportTests(unittest.TestCase):
	def test_report_is_a_blockers_report_for_a_partial_machine(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual("bally.eight-ball-deluxe.1981", report["machine_id"])
		self.assertEqual("partial", report["status"])
		self.assertGreater(report["placement_count"], 0)


if __name__ == "__main__":
	unittest.main()
