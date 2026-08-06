"""Regression tests for the Bally Centaur definition and the Bally MPU-35 profile.

The solenoid numbering here is the expensive fact: the manual's printed Self Test
number and PinMAME's public solenoid address are two different numberings, and
neither retained community script matches the manual. The mapping asserted below
was read off the ROM's own solenoid self test, which pulses each coil while
displaying that coil's identification number. Anything that quietly "tidies" it
back into an identity mapping is a regression.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "centaur-1981.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"

# printed Self Test number -> public PinMAME solenoid address
SELF_TEST_TO_PUBLIC_SOLENOID = {
	1: 7,
	2: 6,
	3: 8,
	4: 9,
	5: 10,
	6: 11,
	7: 12,
	8: 13,
	9: 1,
	10: 2,
	11: 3,
	12: 4,
	13: 5,
	14: 15,
	15: 14,
	16: 18,
	17: 19,
	18: 20,
}

UNUSED_SWITCH_ADDRESSES = (7, 13, 14, 23, 35, 36)

# addresses the manual prints with a parenthesised physical quantity
SHARED_SWITCH_QUANTITIES = {12: 4, 15: 3, 16: 2, 18: 2, 21: 2, 34: 5}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class CentaurDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.inputs = {item["binding"]["device"]: item for item in cls.definition["inputs"]}
		cls.solenoids = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.centaur.1981", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1981, machine["year"])
		self.assertEqual(476, machine["ipdb_id"])

	def test_controller_platform_is_the_bally_mpu_35_profile(self) -> None:
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertEqual("pinmame.by35", self.profile["id"])
		self.assertEqual("Bally MPU AS-2518-35", self.profile["hardware_family"])

	def test_driver_variants_are_the_same_physical_machine(self) -> None:
		drivers = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual({"centaur", "centaura", "centaurb"}, drivers)
		# The Inder game of the same name is a different physical machine and must not be grouped.
		self.assertNotIn("centauri", drivers)
		self.assertNotIn("centaurj", drivers)

	def test_solenoid_self_test_numbers_map_to_the_observed_public_addresses(self) -> None:
		for self_test, public in SELF_TEST_TO_PUBLIC_SOLENOID.items():
			device = self.solenoids.get(public)
			self.assertIsNotNone(device, f"public solenoid {public} is missing")
			aliases = {
				alias["value"]
				for alias in device["aliases"]
				if alias["namespace"] == "manual.self-test"
			}
			self.assertEqual({f"{self_test:02d}"}, aliases, f"public solenoid {public}")

	def test_printed_fourteen_and_fifteen_are_transposed(self) -> None:
		"""The single easiest thing to get wrong: the numbers collide but the devices swap."""
		self.assertEqual("device.ball-kick-to-playfield", self.solenoids[14]["id"])
		self.assertEqual("device.ball-release", self.solenoids[15]["id"])

	def test_public_seven_is_the_outhole_kicker_not_a_ball_release(self) -> None:
		"""Both retained community scripts label public 7 a release to the shooter lane."""
		self.assertEqual("device.outhole-kicker", self.solenoids[7]["id"])

	def test_magnet_and_flipper_relay_are_present_on_the_continuous_outputs(self) -> None:
		self.assertEqual("device.magnet", self.solenoids[20]["id"])
		self.assertEqual("magnet", self.solenoids[20]["kind"])
		self.assertEqual("device.k1-relay-flipper-enable", self.solenoids[19]["id"])
		self.assertEqual("relay", self.solenoids[19]["kind"])

	def test_continuous_output_one_stays_an_unresolved_conflict(self) -> None:
		"""It is asserted and never released, so it is neither used-and-named nor unused.

		A continuous output that is held never appears as a pulse, so absence of a pulse in the
		self-test trace is not evidence that the address is unused. Two sources disagree about what
		it drives, and the record must stay fail-closed until that is settled.
		"""
		device = self.solenoids[17]
		self.assertEqual("unknown", device["availability"])
		self.assertEqual("conflicted", device["provenance"]["status"])
		paths = [conflict["path"] for conflict in self.definition["conflicts"]]
		self.assertIn("binding:pinmame.output.solenoid/17", paths)
		self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])

	def test_every_declared_solenoid_is_legal_for_the_profile(self) -> None:
		group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.solenoid")
		allowed = set()
		for rule in group["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		for address in self.solenoids:
			self.assertIn(address, allowed, f"solenoid {address} is outside the profile")

	def test_switch_matrix_covers_the_printed_forty_eight_addresses(self) -> None:
		matrix = {address for address in self.inputs if 1 <= address <= 48}
		self.assertEqual(set(range(1, 49)), matrix)

	def test_blank_switch_positions_are_declared_unused(self) -> None:
		for address in UNUSED_SWITCH_ADDRESSES:
			device = self.inputs[address]
			self.assertEqual("unused", device["availability"], f"switch {address}")

	def test_shared_switch_addresses_record_their_physical_quantity(self) -> None:
		for address, quantity in SHARED_SWITCH_QUANTITIES.items():
			device = self.inputs[address]
			self.assertEqual(
				quantity,
				device.get("physical", {}).get("quantity"),
				f"switch {address} should record {quantity} physical contacts",
			)

	def test_legacy_switch_label_conflicts_are_resolved_from_the_manual(self) -> None:
		"""All seven inherited conflicts; the platform source was right in every case."""
		self.assertEqual("switch.5th-ball-trough", self.inputs[2]["id"])
		self.assertEqual("switch.credit-button", self.inputs[6]["id"])
		self.assertEqual("switch.coin-3-right", self.inputs[9]["id"])
		self.assertEqual("switch.coin-1-left", self.inputs[10]["id"])
		self.assertEqual("switch.coin-2-middle", self.inputs[11]["id"])
		self.assertEqual("switch.slam", self.inputs[16]["id"])
		# Neither legacy source was right about 7: the manual prints no description there.
		self.assertEqual("unused", self.inputs[7]["availability"])
		# All seven legacy label conflicts are gone; the only conflict left is a new, honest one.
		switch_conflicts = [
			conflict for conflict in self.definition["conflicts"]
			if conflict["path"].startswith("binding:pinmame.input.switch")
		]
		self.assertEqual([], switch_conflicts)

	def test_display_inventory_matches_dispby7(self) -> None:
		displays = {item["controller_index"]: item for item in self.definition["displays"]}
		self.assertEqual(set(range(6)), set(displays))
		for index in range(4):
			self.assertIn("Player", displays[index]["label"])
			self.assertIn("seven digits", displays[index]["label"])
		self.assertIn("two digits", displays[4]["label"])
		self.assertIn("two digits", displays[5]["label"])
		for display in displays.values():
			self.assertEqual("segment", display["kind"])
			# Backbox devices never carry playfield coordinates.
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_definition_cites_the_manual_and_the_runtime_scenario(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("manual.bally.centaur.1981", sources)
		self.assertIn("runtime.centaur.solenoid-self-test", sources)
		self.assertEqual("runtime_scenario", sources["runtime.centaur.solenoid-self-test"]["kind"])
		manual = sources["manual.bally.centaur.1981"]
		self.assertTrue(manual["revision"].startswith("sha256:"))
		self.assertIn("license", manual)
		self.assertIn("attribution", manual)

	def test_coverage_stays_partial_and_names_its_gaps(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertIn("spatial_placement", coverage["missing"])
		self.assertIn("mechanism_inventory", coverage["missing"])
		self.assertTrue(coverage["missing"], "a partial must name what it is missing")


class By35ProfileTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(PROFILE_PATH)
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}

	def _allowed(self, group_id: str) -> set[int]:
		allowed: set[int] = set()
		for rule in self.groups[group_id]["address_rules"]:
			if "values" in rule:
				allowed.update(rule["values"])
			else:
				allowed.update(range(rule["minimum"], rule["maximum"] + 1))
		return allowed

	def test_momentary_solenoids_stop_at_fifteen(self) -> None:
		"""Selector 15 is the idle state, so there is no public address 16."""
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual(set(range(1, 16)), allowed)
		self.assertNotIn(16, allowed)

	def test_four_continuous_outputs_are_published_at_seventeen_through_twenty(self) -> None:
		allowed = self._allowed("pinmame.output.solenoid")
		self.assertLessEqual({17, 18, 19, 20}, allowed)

	def test_lamp_decoder_slots_are_not_addressable(self) -> None:
		allowed = self._allowed("pinmame.output.lamp")
		for slot in (16, 32, 48, 64, 80, 96, 112, 128):
			self.assertNotIn(slot, allowed, f"lamp {slot} is a skipped decoder slot")
		self.assertEqual(120, len(allowed))

	def test_switch_matrix_is_six_columns_of_eight_plus_diagnostics(self) -> None:
		allowed = self._allowed("pinmame.input.switch")
		self.assertLessEqual(set(range(1, 49)), allowed)
		self.assertLessEqual({-7, -6, -5}, allowed)
		self.assertNotIn(49, allowed)

	def test_emulator_normalization_is_declared_and_not_reapplied(self) -> None:
		self.assertTrue(self.profile["inversion_applied_by_emulator"])

	def test_profile_pins_its_pinmame_revision(self) -> None:
		revisions = {source["revision"] for source in self.profile["sources"]}
		self.assertIn("4ec52ff0ac133ac251681518aed2249e19fe26eb", revisions)


if __name__ == "__main__":
	unittest.main()
