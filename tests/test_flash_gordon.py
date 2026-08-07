"""Regression tests for the Bally Flash Gordon definition and the by35 profile it reuses.

The regression this file guards hardest is the BY35 continuous-output rule, because it is the one
that genuinely differs per game rather than per platform. Centaur is a six-column game and spends
public 17 on the sixth switch-column strobe; Kiss is a five-column game and spends public 17 on a
real coil. Flash Gordon declares eight columns in its INITGAME2 but wires five, and its public 17
and 20 are unused. Nothing here may be "tidied" into a rule that holds across all three machines.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "flash-gordon-1980.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "flash-gordon-1980.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "flash-gordon-1980.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "flash-gordon-1980.json"


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class FlashGordonDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.inputs = {
			int(device["binding"]["device"]): device
			for device in cls.definition["inputs"]
			if device["binding"]["group"] == "pinmame.input.switch"
		}
		cls.solenoids = {
			int(device["binding"]["device"]): device
			for device in cls.definition["outputs"]
			if device["binding"]["group"] == "pinmame.output.solenoid"
		}
		cls.lamps = {
			int(device["binding"]["device"]): device
			for device in cls.definition["outputs"]
			if device["binding"]["group"] == "pinmame.output.lamp"
		}

	def test_identity_and_controller_platform(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.flash-gordon.1980", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1980, machine["year"])
		self.assertEqual("physical_pinball", machine["kind"])
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])

	def test_playfield_extent_matches_the_normalization_divisors(self) -> None:
		"""Every coordinate here was divided by these, so a change to one must change the other."""
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual("vpx", playfield["units"])
		self.assertAlmostEqual(952.9412, playfield["width"], places=4)
		self.assertAlmostEqual(1976.471, playfield["height"], places=3)

	def test_driver_family_is_the_ten_flash_gordon_drivers(self) -> None:
		self.assertEqual(
			{
				"flashgda", "flashgdf", "flashgdn", "flashgdp", "flashgdv",
				"flashgfa", "flashgp2", "flashgva", "flashgvf", "flashgvffp",
			},
			{driver["id"] for driver in self.definition["drivers"]},
		)

	def test_forty_matrix_switches_are_enumerated_with_no_gaps(self) -> None:
		self.assertEqual(set(range(1, 41)), set(self.inputs))

	# ------------------------------------------------------------- solenoids --

	def test_momentary_solenoids_run_1_to_15_with_no_address_16(self) -> None:
		"""Selector 15 is the idle state on a BY35, so there is no public 16."""
		for address in range(1, 16):
			self.assertIn(address, self.solenoids, f"momentary solenoid {address} missing")
		self.assertNotIn(16, self.solenoids)

	def test_exactly_four_continuous_outputs_at_17_to_20(self) -> None:
		self.assertEqual({17, 18, 19, 20}, {a for a in self.solenoids if a >= 17})

	def test_five_wired_switch_columns_leave_17_and_20_unused(self) -> None:
		"""The per-game rule, not a platform rule.

		A BY35 game only spends a continuous output on a switch-column strobe when it needs a
		column beyond the five the main board strobes directly. Centaur needs a sixth and burns
		public 17 on it; this machine does not, so 17 is unused and carries no coil. 18 and 19 are
		real devices (coin lockout, flipper-enable relay) and 20 is unused.
		"""
		self.assertEqual("unused", self.solenoids[17]["availability"])
		self.assertEqual("unused", self.solenoids[20]["availability"])
		self.assertEqual("used", self.solenoids[18]["availability"])
		self.assertEqual("used", self.solenoids[19]["availability"])

	def test_unused_continuous_outputs_have_a_controlled_spatial_record(self) -> None:
		for address in (17, 20):
			spatial = self.solenoids[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], f"solenoid {address}")
			self.assertEqual("unused", spatial["reason"], f"solenoid {address}")

	# ----------------------------------------------------------------- lamps --

	def test_no_lamp_sits_on_an_unreachable_decoder_slot(self) -> None:
		"""The BY35 lamp strobe ignores decoder selector 0x0f, so every multiple of 16 is a slot
		no bulb can occupy. Public address is 16*d + lampadr + 1, which never lands on one."""
		self.assertEqual([], [address for address in self.lamps if address % 16 == 0])

	def test_auxiliary_lamp_addresses_are_present_above_64(self) -> None:
		"""Flash Gordon fits the AS-2518-43 auxiliary board, so the +64 range is real."""
		self.assertTrue(any(address > 64 for address in self.lamps))

	# ------------------------------------------------------------- conflicts --

	def test_all_three_conflicts_are_present_and_the_record_stays_partial(self) -> None:
		self.assertEqual(
			{
				"conflict.outlane-special-insert-side-transposition",
				"conflict.right-side-target-upper-lower-transposition",
				"conflict.aux-lamp-100-left-rollover-fitment",
			},
			{conflict["id"] for conflict in self.definition["conflicts"]},
		)
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])


class FlashGordonSpatialOrderingTests(unittest.TestCase):
	"""The cheap ordering checks the Centaur post-mortem asked for.

	Centaur shipped two auxiliary lamps reversed and the lesson recorded was that asserting the
	left, middle and right members of a row have ascending x would have caught it. These are those
	assertions. They are deliberately written against device *names*, so a placement that lands on
	the wrong side of the playfield fails regardless of which source it came from.
	"""

	@classmethod
	def setUpClass(cls) -> None:
		definition = load_json(DEFINITION_PATH)
		cls.points = {}
		for group in ("inputs", "outputs"):
			for device in definition[group]:
				placements = (device.get("spatial") or {}).get("placements") or []
				if placements:
					cls.points[device["id"]] = (placements[0]["x"], placements[0]["y"])

	def test_left_named_devices_sit_left_of_their_right_named_partner(self) -> None:
		pairs = [
			("switch.left-outlane", "switch.right-outlane"),
			("switch.left-slingshot", "switch.right-slingshot"),
			("switch.flipper-feed-lane-left", "switch.flipper-feed-lane-right"),
			("lamp.flipper-feed-lane-left", "lamp.flipper-feed-lane-right"),
			("switch.left-spinner", "switch.right-spinner"),
			("lamp.left-spinner", "lamp.right-spinner"),
			("switch.left-thumper-bumper", "switch.right-thumper-bumper"),
			("device.left-slingshot", "device.right-slingshot"),
			("device.left-thumper-bumper", "device.right-thumper-bumper"),
		]
		for left_id, right_id in pairs:
			left = self.points[left_id]
			right = self.points[right_id]
			self.assertLess(left[0], right[0], f"{left_id} must sit left of {right_id}")

	def test_the_outlane_special_inserts_are_the_one_known_exception(self) -> None:
		"""Guards conflict.outlane-special-insert-side-transposition against silent "repair".

		These two are on the wrong sides and that is recorded as an unresolved conflict rather than
		fixed, because the retained table supplies no observed coordinate for an insert of either
		name on the correct side. This test pins the current state so that anyone who swaps them
		has to come here, read the conflict, and justify the swap with real evidence. If the
		conflict is ever resolved, this test should be replaced by an ordinary ordering assertion
		in the list above.
		"""
		self.assertGreater(
			self.points["lamp.left-outlane-special"][0],
			self.points["lamp.right-outlane-special"][0],
			"the known transposition is gone; resolve the conflict entry too",
		)
		conflicts = {conflict["id"] for conflict in load_json(DEFINITION_PATH)["conflicts"]}
		self.assertIn("conflict.outlane-special-insert-side-transposition", conflicts)

	def test_slingshot_switch_and_coil_of_one_side_are_co_located(self) -> None:
		for side in ("left", "right"):
			self.assertEqual(
				self.points[f"switch.{side}-slingshot"],
				self.points[f"device.{side}-slingshot"],
				f"{side} slingshot switch and coil are one assembly",
			)

	def test_every_placement_is_in_range_with_at_most_six_decimals(self) -> None:
		for device_id, (x, y) in self.points.items():
			self.assertGreaterEqual(x, 0.0, device_id)
			self.assertLessEqual(x, 1.0, device_id)
			self.assertGreaterEqual(y, 0.0, device_id)
			self.assertLessEqual(y, 1.0, device_id)
			for axis, value in (("x", x), ("y", y)):
				self.assertEqual(
					round(value, 6), value, f"{device_id} {axis} has more than six decimals"
				)


class ByThirtyFiveProfileTests(unittest.TestCase):
	def test_profile_is_unmodified_by_this_game(self) -> None:
		profile = load_json(PROFILE_PATH)
		self.assertEqual("pinmame.by35", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])


class FlashGordonArtifactTests(unittest.TestCase):
	def test_seed_and_definition_are_byte_identical(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_knowledge_note_exists_and_is_declared_complete(self) -> None:
		definition = load_json(DEFINITION_PATH)
		self.assertEqual("knowledge/bally/flash-gordon-1980.md", definition["knowledge"]["path"])
		self.assertEqual("complete", definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_spatial_report_is_a_partial_report_for_this_machine(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("bally.flash-gordon.1980", report["machine_id"])


if __name__ == "__main__":
	unittest.main()
