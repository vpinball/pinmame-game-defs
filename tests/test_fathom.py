"""Fail-closed tests for the Bally Fathom (1981) definition.

The interesting facts on this machine are all things a plausible-looking guess would get wrong: the
fifth INITGAME2 argument is a lamp-column count and not a switch-column count, the sixth switch
strobe eats public solenoid 20 rather than 17, the printed Self Test numbers are a test order, five
driver outputs serve two coils each through a relay, and one lamp address drives that relay instead
of a bulb. Each of those has a test here, plus the cheap geometric ordering assertions that catch a
reversed left/right identity.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "fathom-1981.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "fathom-1981.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "fathom-1981.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "fathom-1981.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "by35.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "fathom-1981.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "bally" / "fathom-1981.md"
EXCERPT_DIR = ROOT / "evidence" / "excerpts" / "bally.fathom.1981"
STUB_PATH = ROOT / "machines" / "stubs" / "fathom.json"

DRIVER_IDS = {"fathom", "fathoma", "fathomb"}
MATRIX_ADDRESSES = set(range(1, 49))
UNUSED_MATRIX_ADDRESSES = {8, 41, 45}
DIAGNOSTIC_ADDRESSES = {-7, -6, -5}
MOMENTARY_ADDRESSES = set(range(1, 16))
CONTINUOUS_ADDRESSES = {17, 18, 19, 20}
FLIPPER_ADDRESSES = {46, 48}
MAIN_LAMP_ADDRESSES = (
	set(range(1, 16)) | set(range(17, 32)) | set(range(33, 48)) | set(range(49, 64))
)
AUX_LAMP_ADDRESSES = (
	set(range(65, 73)) | set(range(81, 89)) | set(range(97, 105)) | set(range(113, 121))
)
# Read off the ROM's own solenoid self test in the retained harness run: the coils fire in printed
# order 01 through 21, so this is printed number -> public address.
SELF_TEST_TO_PUBLIC = {
	"01": 6, "02": 13, "03": 14, "04": 8, "05": 9, "06": 10, "07": 11, "08": 12,
	"09": 1, "10": 2, "11": 3, "12": 4, "13": 7,
	"14": 1, "15": 2, "16": 3, "17": 13, "18": 14, "19": 15,
	"20": 18, "21": 19,
}
RELAY_GATED_SOLENOIDS = {1, 2, 3, 13, 14}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def only_placement(device: dict) -> tuple[float, float]:
	placements = device["spatial"]["placements"]
	assert len(placements) == 1, device["id"]
	return placements[0]["x"], placements[0]["y"]


class FathomIdentityTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)

	def test_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("bally.fathom.1981", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual(1981, self.definition["machine"]["year"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			["output_semantics", "spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		self.assertFalse(AUTHOR_READY_PATH.exists(), "a partial record must not leave an author-ready file behind")

	def test_manufacturer_directory_matches_machine_id(self) -> None:
		"""A generated brief has put artifacts in the wrong manufacturer directory before now."""
		manufacturer = self.definition["machine"]["id"].split(".")[0]
		for path in (DEFINITION_PATH, SEED_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_MARKDOWN_PATH):
			self.assertEqual(manufacturer, path.parent.name, path)

	def test_playfield_extent_matches_the_retained_table_bounds(self) -> None:
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual("vpx", playfield["units"])
		self.assertEqual(952.0, playfield["width"])
		self.assertEqual(1974.0, playfield["height"])

	def test_clone_tree_is_the_three_fathom_drivers(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertNotIn("clone_of", drivers["fathom"])
		for clone in ("fathoma", "fathomb"):
			self.assertEqual("fathom", drivers[clone]["clone_of"])
			self.assertEqual("2004", drivers[clone]["year"])
			self.assertEqual("Bally / Oliver", drivers[clone]["manufacturer"])
			self.assertEqual("identical", drivers[clone]["physical_compatibility"])
		self.assertEqual("1981", drivers["fathom"]["year"])

	def test_2004_clones_do_not_move_the_physical_year(self) -> None:
		"""Later firmware for the same machine must not drag the physical release year forward."""
		self.assertEqual(1981, self.definition["machine"]["year"])
		for clone in ("fathoma", "fathomb"):
			notes = {driver["id"]: driver["variant_notes"] for driver in self.definition["drivers"]}[clone]
			self.assertIn("same physical machine", notes)

	def test_superseded_stub_has_been_pruned(self) -> None:
		"""The generated stub this definition supersedes must not survive integration.

		While the curation worktree was open this asserted the opposite - the stub was deliberately
		left in place because that worktree does not regenerate the catalog, and pruning it there
		would have broken test_classification against a stale catalog. rebuild_catalog removes it
		centrally on merge via _prune_generated_stubs, so post-integration its absence is the
		correct invariant: if it ever reappears, one physical machine is being counted twice.
		"""
		self.assertFalse(
			STUB_PATH.is_file(),
			f"{STUB_PATH} should have been pruned when the catalog was regenerated",
		)

	def test_controller_profile_is_the_shared_by35_profile(self) -> None:
		self.assertEqual("pinmame.by35", self.definition["controller"]["platform"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.by35", profile["id"])
		self.assertEqual("Bally MPU AS-2518-35", profile["hardware_family"])


class FathomSwitchTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")

	def test_every_matrix_position_and_diagnostic_contact_is_enumerated(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES | DIAGNOSTIC_ADDRESSES, set(self.switches))

	def test_six_columns_of_eight_and_nothing_beyond(self) -> None:
		"""Fathom wires forty-eight switches; declaring a 49th would mean a seventh column."""
		self.assertEqual(48, max(self.switches))
		for address in MATRIX_ADDRESSES:
			column = (address - 1) // 8 + 1
			self.assertLessEqual(column, 6)
			wiring = self.switches[address]["wiring"]
			self.assertIn(f"strobe ST {column - 1}", wiring["return_component"])

	def test_the_sixth_strobe_comes_from_a_different_mpu_connector(self) -> None:
		for address in range(41, 49):
			self.assertEqual("A4J4-8", self.switches[address]["wiring"]["drive_connection"])
		for address in range(1, 41):
			self.assertTrue(self.switches[address]["wiring"]["drive_connection"].startswith("A4J2-"))

	def test_the_three_printed_blanks_are_the_only_unused_positions(self) -> None:
		unused = {address for address, switch in self.switches.items() if switch["availability"] == "unused"}
		self.assertEqual(UNUSED_MATRIX_ADDRESSES, unused)

	def test_no_switch_is_declared_normally_closed(self) -> None:
		"""A 1981 Bally has leaf switches throughout and fathomGameData populates no inverted mask."""
		for address, switch in self.switches.items():
			if switch["availability"] == "unused":
				continue
			self.assertFalse(switch["normally_closed"], address)
			self.assertNotEqual("opto", switch["physical"].get("switch_type"), address)

	def test_cabinet_and_door_switches_carry_no_playfield_coordinate(self) -> None:
		for address in (6, 7, 9, 10, 11, 15, 16):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"], address)

	def test_shared_matrix_positions_carry_the_right_number_of_placements(self) -> None:
		self.assertEqual(3, len(self.switches[20]["spatial"]["placements"]))
		self.assertEqual(2, len(self.switches[19]["spatial"]["placements"]))

	def test_all_thirty_two_option_switches_are_enumerated(self) -> None:
		self.assertEqual(set(range(1, 33)), set(self.dips))
		for address in (14, 15, 21):
			self.assertEqual("unknown", self.dips[address]["availability"], address)
			self.assertIn("do not document this switch", self.dips[address]["physical"]["notes"])


class FathomSolenoidTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")

	def test_address_space_is_the_by35_shape(self) -> None:
		self.assertEqual(MOMENTARY_ADDRESSES | CONTINUOUS_ADDRESSES | FLIPPER_ADDRESSES, set(self.solenoids))
		self.assertNotIn(16, self.solenoids, "selector 15 is the idle state, so there is no public address 16")

	def test_printed_self_test_numbers_map_to_the_harness_observed_addresses(self) -> None:
		observed: dict[str, int] = {}
		for address, solenoid in self.solenoids.items():
			for alias in solenoid.get("aliases", []):
				if alias["namespace"] == "manual.self-test":
					self.assertNotIn(alias["value"], observed, alias["value"])
					observed[alias["value"]] = address
		self.assertEqual(SELF_TEST_TO_PUBLIC, observed)

	def test_printed_number_is_never_reused_as_the_public_address(self) -> None:
		"""The printed column is a test order; treating it as an address is the classic BY35 mistake."""
		self.assertEqual(6, SELF_TEST_TO_PUBLIC["01"])
		self.assertEqual(7, SELF_TEST_TO_PUBLIC["13"])
		self.assertEqual("Knocker", self.solenoids[6]["label"])
		self.assertEqual("Outhole Kicker", self.solenoids[7]["label"])

	def test_five_outputs_are_relay_gated_between_two_coils(self) -> None:
		gated = set()
		for address, solenoid in self.solenoids.items():
			printed = [a["value"] for a in solenoid.get("aliases", []) if a["namespace"] == "manual.self-test"]
			if len(printed) > 1:
				gated.add(address)
				self.assertEqual(2, len(printed), address)
				self.assertIn("Solenoid Expander", solenoid["physical"]["notes"], address)
		self.assertEqual(RELAY_GATED_SOLENOIDS, gated)

	def test_the_relay_gate_relationships_all_come_from_the_expander_lamp(self) -> None:
		relay_lamp = "lamp.solenoid-expander-relay-drive-47"
		gated = {
			item["destination"]
			for item in self.definition["relationships"]
			if item["kind"] == "relay_gated" and item["source"] == relay_lamp
		}
		self.assertEqual(5, len(gated))
		labels = {self.solenoids[address]["id"] for address in RELAY_GATED_SOLENOIDS}
		self.assertEqual(labels, gated)

	def test_the_sixth_switch_strobe_occupies_public_twenty_not_seventeen(self) -> None:
		strobe = self.solenoids[20]
		self.assertEqual("control_signal", strobe["kind"])
		self.assertIn("internal.switch-strobe", strobe["roles"])
		self.assertEqual("A4J4-8", strobe["wiring"]["control_connection"])
		self.assertIn("PB7", strobe["physical"]["notes"])
		self.assertEqual("unused", self.solenoids[17]["availability"])

	def test_public_five_and_seventeen_are_the_only_spare_outputs(self) -> None:
		unused = {address for address, solenoid in self.solenoids.items() if solenoid["availability"] == "unused"}
		self.assertEqual({5, 17}, unused)

	def test_flipper_coils_have_no_driver_board_output(self) -> None:
		for address in FLIPPER_ADDRESSES:
			notes = self.solenoids[address]["physical"]["notes"]
			self.assertIn("no driver-board output", notes)
			self.assertIn("K1", notes)
		self.assertEqual("relay", self.solenoids[19]["kind"])
		self.assertIn("internal.flipper-enable", self.solenoids[19]["roles"])

	def test_upper_right_flipper_shares_the_lower_right_address(self) -> None:
		self.assertEqual(2, len(self.solenoids[46]["spatial"]["placements"]))
		self.assertEqual(1, len(self.solenoids[48]["spatial"]["placements"]))


class FathomLampTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_lamp_address_space(self) -> None:
		self.assertEqual(MAIN_LAMP_ADDRESSES | AUX_LAMP_ADDRESSES, set(self.lamps))
		for unreachable in (16, 32, 48, 64):
			self.assertNotIn(unreachable, self.lamps, unreachable)

	def test_no_general_illumination_channel_is_declared(self) -> None:
		"""System 11, WPC, Whitestar and SAM have a GI channel; the Bally MPU does not."""
		self.assertEqual({}, bindings(self.definition, "outputs", "pinmame.output.gi"))

	def test_every_main_board_address_carries_a_printed_connector_pin(self) -> None:
		for address in sorted(MAIN_LAMP_ADDRESSES):
			pin = self.lamps[address]["wiring"]["control_connection"]
			self.assertRegex(pin, r"^A5J[123]-\d+$", address)

	def test_main_board_pins_are_unique_and_the_four_runs_are_right(self) -> None:
		pins = [self.lamps[address]["wiring"]["control_connection"] for address in MAIN_LAMP_ADDRESSES]
		self.assertEqual(len(pins), len(set(pins)))
		for address in sorted(MAIN_LAMP_ADDRESSES):
			data_line, decoder_output = divmod(address - 1, 16)
			self.assertLessEqual(decoder_output, 14, address)
			self.assertIn(f"PD{data_line}", self.lamps[address]["physical"]["notes"], address)

	def test_lamp_forty_seven_drives_the_solenoid_expander_relay_not_a_bulb(self) -> None:
		relay = self.lamps[47]
		self.assertEqual("relay", relay["kind"])
		self.assertEqual("A5J2-2", relay["wiring"]["control_connection"])
		self.assertIn("internal.solenoid-expander-gate", relay["roles"])
		self.assertEqual("not_applicable", relay["spatial"]["status"])
		self.assertEqual("internal_nonvisual", relay["spatial"]["reason"])

	def test_bally_platform_status_lamps_sit_at_their_usual_addresses(self) -> None:
		expected = {11: "Shoot Again", 13: "Ball In Play", 27: "Match", 29: "High Score To Date",
			45: "Game Over", 61: "Tilt"}
		for address, label in expected.items():
			self.assertEqual(label, self.lamps[address]["label"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)

	def test_the_eight_branch_outputs_are_declared(self) -> None:
		branched = {
			address
			for address in MAIN_LAMP_ADDRESSES
			if "also reaches" in self.lamps[address]["physical"]["notes"]
		}
		self.assertEqual({11, 12, 27, 28, 43, 44, 59, 60}, branched)

	def test_auxiliary_board_uses_only_seven_decoder_outputs_per_chip(self) -> None:
		for address in sorted(AUX_LAMP_ADDRESSES):
			data_line, decoder_output = divmod(address - 65, 16)
			self.assertLessEqual(decoder_output, 7, address)
			self.assertIn("AS-2518-52", self.lamps[address]["wiring"]["board"], address)
		for n_u in (72, 88, 104, 120):
			self.assertEqual("unused", self.lamps[n_u]["availability"], n_u)

	def test_only_the_seven_annotated_auxiliary_addresses_are_named(self) -> None:
		named = {
			address
			for address in AUX_LAMP_ADDRESSES
			if self.lamps[address]["provenance"]["status"] == "validated"
			and not self.lamps[address]["label"].startswith("Auxiliary Lamp Driver Position")
		}
		self.assertEqual({65, 66, 81, 82, 97, 98, 113}, named)

	def test_unobserved_auxiliary_addresses_are_unknown_rather_than_unused(self) -> None:
		"""Failing to observe an address is not proof that it is unused."""
		for address in (68, 69, 70, 71, 84, 85, 86, 87, 100, 101, 102, 103, 116, 117, 118, 119):
			self.assertEqual("unknown", self.lamps[address]["availability"], address)
		for address in (67, 83, 99, 114, 115):
			self.assertEqual("used", self.lamps[address]["availability"], address)


class FathomGeometryTests(unittest.TestCase):
	"""Cheap ordering assertions. These are what catch a reversed left/right identity."""

	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_every_coordinate_is_in_range_with_six_places(self) -> None:
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				spatial = device.get("spatial")
				if not spatial or spatial["status"] == "not_applicable":
					continue
				for placement in spatial["placements"]:
					for axis in ("x", "y"):
						value = placement[axis]
						self.assertGreaterEqual(value, 0.0, placement["id"])
						self.assertLessEqual(value, 1.0, placement["id"])
						self.assertEqual(round(value, 6), value, placement["id"])

	def test_flippers_trough_and_plunger_sit_near_the_player_end(self) -> None:
		self.assertGreater(only_placement(self.solenoids[48])[1], 0.8)
		self.assertGreater(only_placement(self.switches[1])[1], 0.9)
		self.assertGreater(only_placement(self.switches[2])[1], 0.8)

	def test_lower_flippers_are_left_and_right_of_each_other(self) -> None:
		left = only_placement(self.solenoids[48])
		right = self.solenoids[46]["spatial"]["placements"][0]
		self.assertLess(left[0], right["x"])

	def test_slingshot_sides(self) -> None:
		self.assertLess(only_placement(self.switches[37])[0], only_placement(self.switches[36])[0])
		self.assertLess(only_placement(self.solenoids[11])[0], only_placement(self.solenoids[12])[0])

	def test_thumper_bumper_geometry(self) -> None:
		left = only_placement(self.switches[40])
		bottom = only_placement(self.switches[39])
		right = only_placement(self.switches[38])
		self.assertLess(left[0], bottom[0])
		self.assertLess(bottom[0], right[0])
		self.assertGreater(bottom[1], left[1])
		self.assertGreater(bottom[1], right[1])

	def test_thumper_bumper_lamps_agree_with_the_switch_the_manual_names(self) -> None:
		"""The lamp is inside the bumper body, so it must sit on the same bumper as its switch."""
		for lamp_address, switch_address in ((12, 38), (28, 39), (44, 40)):
			lamp = only_placement(self.lamps[lamp_address])
			switch = only_placement(self.switches[switch_address])
			self.assertAlmostEqual(lamp[0], switch[0], places=6, msg=f"lamp {lamp_address}")
			self.assertAlmostEqual(lamp[1], switch[1], places=6, msg=f"lamp {lamp_address}")

	def test_abc_lanes_run_left_to_right(self) -> None:
		a = only_placement(self.switches[14])
		b = only_placement(self.switches[13])
		c = only_placement(self.switches[12])
		self.assertLess(a[0], b[0])
		self.assertLess(b[0], c[0])

	def test_abc_lane_lamps_sit_above_their_own_lane_switch(self) -> None:
		for lamp_address, switch_address in ((42, 14), (26, 13), (10, 12)):
			lamp = only_placement(self.lamps[lamp_address])
			switch = only_placement(self.switches[switch_address])
			self.assertAlmostEqual(lamp[0], switch[0], delta=0.02, msg=f"lamp {lamp_address}")
			self.assertLess(lamp[1], switch[1], f"lamp {lamp_address}")

	def test_left_six_bank_ascends_the_playfield(self) -> None:
		ys = [only_placement(self.switches[address])[1] for address in range(27, 33)]
		self.assertEqual(ys, sorted(ys, reverse=True))

	def test_middle_three_bank_runs_right_to_left_as_the_address_falls(self) -> None:
		self.assertLess(
			only_placement(self.switches[35])[0],
			only_placement(self.switches[34])[0],
		)
		self.assertLess(
			only_placement(self.switches[34])[0],
			only_placement(self.switches[33])[0],
		)

	def test_blue_inline_bank_runs_across_the_top(self) -> None:
		first, second, third = (only_placement(self.switches[address]) for address in (44, 43, 42))
		self.assertLess(first[0], second[0])
		self.assertLess(second[0], third[0])
		for position in (first, second, third):
			self.assertLess(position[1], 0.1)

	def test_green_inline_bank_ascends_the_right_side(self) -> None:
		first, second, third = (only_placement(self.switches[address]) for address in (48, 47, 46))
		self.assertGreater(first[1], second[1])
		self.assertGreater(second[1], third[1])
		for position in (first, second, third):
			self.assertGreater(position[0], 0.8)

	def test_return_lane_lamps_sit_beside_their_own_return_lane_switch(self) -> None:
		for lamp_address, switch_address in ((1, 21), (49, 24)):
			lamp = only_placement(self.lamps[lamp_address])
			switch = only_placement(self.switches[switch_address])
			self.assertAlmostEqual(lamp[0], switch[0], delta=0.03, msg=f"lamp {lamp_address}")
			self.assertAlmostEqual(lamp[1], switch[1], delta=0.08, msg=f"lamp {lamp_address}")

	def test_blue_and_green_bonus_ladders_climb_monotonically(self) -> None:
		blue = [2, 18, 34, 50, 3, 19, 35]
		green = [6, 22, 38, 54, 7, 23, 39]
		for ladder in (blue, green):
			ys = [only_placement(self.lamps[address])[1] for address in ladder]
			self.assertEqual(ys, sorted(ys, reverse=True))
			xs = [only_placement(self.lamps[address])[0] for address in ladder]
			self.assertLess(max(xs) - min(xs), 0.02)
		self.assertLess(
			only_placement(self.lamps[2])[0],
			only_placement(self.lamps[6])[0],
			"the blue ladder is the left-hand column and the green ladder the right-hand one",
		)

	def test_scan_rollover_button_lamps_land_on_the_three_left_rollovers(self) -> None:
		rollovers = self.switches[20]["spatial"]["placements"]
		for lamp_address in (65, 81, 97):
			lamp = only_placement(self.lamps[lamp_address])
			self.assertTrue(
				any(abs(lamp[0] - p["x"]) < 0.01 and abs(lamp[1] - p["y"]) < 0.01 for p in rollovers),
				f"auxiliary lamp {lamp_address} does not sit on a switch-20 rollover",
			)


class FathomMechanismAndConflictTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.mechanisms = {item["id"]: item for item in cls.definition["mechanisms"]}

	def test_the_expected_mechanisms_exist(self) -> None:
		expected = {
			"mechanism.outhole-and-trough",
			"mechanism.solenoid-expander",
			"mechanism.left-six-bank",
			"mechanism.middle-three-bank",
			"mechanism.blue-inline-bank",
			"mechanism.green-inline-bank",
			"mechanism.top-saucer",
			"mechanism.right-saucer",
			"mechanism.thumper-bumpers",
			"mechanism.slingshots",
			"mechanism.flippers",
			"mechanism.spinner",
			"mechanism.captive-balls",
		}
		self.assertEqual(expected, set(self.mechanisms))

	def test_the_trough_has_three_stations(self) -> None:
		sensors = self.mechanisms["mechanism.outhole-and-trough"]["sensors"]
		self.assertEqual(["switch.matrix-1", "switch.matrix-2", "switch.matrix-3"], sensors)

	def test_the_expander_is_actuated_by_a_lamp_address(self) -> None:
		actuators = self.mechanisms["mechanism.solenoid-expander"]["actuators"]
		self.assertEqual(["lamp.solenoid-expander-relay-drive-47"], actuators)

	def test_both_inline_banks_have_three_targets(self) -> None:
		self.assertEqual(3, len(self.mechanisms["mechanism.blue-inline-bank"]["sensors"]))
		self.assertEqual(3, len(self.mechanisms["mechanism.green-inline-bank"]["sensors"]))
		self.assertEqual(6, len(self.mechanisms["mechanism.left-six-bank"]["sensors"]))

	def test_captive_balls_have_no_actuator(self) -> None:
		self.assertEqual([], self.mechanisms["mechanism.captive-balls"]["actuators"])

	def test_the_single_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {item["id"]: item for item in self.definition["conflicts"]}
		self.assertEqual({"conflict.thumper-bumper-lamp-address-swap"}, set(conflicts))
		self.assertIn("Unresolved", conflicts["conflict.thumper-bumper-lamp-address-swap"]["description"])


class FathomProvenanceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def test_required_sources_are_present(self) -> None:
		for identifier in (
			"pinmame.catalog.4ec52ff0ac13",
			"pinmame.core.4ec52ff0ac13",
			"controller-profile.pinmame-by35",
			"board-mapping.as-2518-23",
			"manual.bally.fathom.1981",
			"manual-schematics.bally.fathom.1981",
			"runtime.fathom.solenoid-self-test",
			"vpx-table.fathom-bally-1981",
			"vpx-script.fathom-bally-1981",
			"vpx-extraction.fathom-bally-1981",
		):
			self.assertIn(identifier, self.sources)

	def test_every_provenance_reference_resolves(self) -> None:
		def walk(node) -> None:
			if isinstance(node, dict):
				if "source_refs" in node:
					for ref in node["source_refs"]:
						self.assertIn(ref, self.sources, ref)
				for value in node.values():
					walk(value)
			elif isinstance(node, list):
				for value in node:
					walk(value)

		walk(self.definition)

	def test_manual_and_schematics_hashes_are_pinned(self) -> None:
		self.assertEqual(
			"ce44bcc4470f395ed1498350079bb435e5dbced75daa948471eee33cd93d5e07",
			self.sources["manual.bally.fathom.1981"]["sha256"],
		)
		self.assertEqual(
			"badb849dcf110846335967024596d2e3853cfef531eae36a6e88d649aedb47a9",
			self.sources["manual-schematics.bally.fathom.1981"]["sha256"],
		)

	def test_the_harness_source_records_what_it_observed(self) -> None:
		locator = self.sources["runtime.fathom.solenoid-self-test"]["locator"]
		self.assertIn("6, 13, 14, 8, 9, 10, 11, 12, 1, 2, 3, 4, 7, 1, 2, 3, 13, 14, 15, 18, 19", locator)
		self.assertIn("lamp 47", locator)
		self.assertEqual("runtime_scenario", self.sources["runtime.fathom.solenoid-self-test"]["kind"])

	def test_excerpts_cover_every_table_region_the_definition_rests_on(self) -> None:
		names = {
			Path(excerpt["path"]).name
			for source in self.definition["sources"]
			for excerpt in source.get("excerpts", [])
		}
		self.assertEqual(
			{
				"self-test-tables.md",
				"game-adjustments.md",
				"auxiliary-lamp-driver-a9.md",
				"solenoid-driver-a3.md",
				"lamp-driver-a5.md",
				"playfield-wiring.md",
				"lamp-driver-a5-u1-fanout.webp",
				"aux-lamp-driver-a9-annotated-outputs.webp",
			},
			names,
		)

	def test_the_script_source_records_the_dead_solenoid_callbacks(self) -> None:
		locator = self.sources["vpx-script.fathom-bally-1981"]["locator"]
		self.assertIn("dead code", locator)
		self.assertIn("25, 26, 27, 37 and 38", locator)


class FathomCuratorTests(unittest.TestCase):
	def test_curator_check_mode_is_idempotent(self) -> None:
		import curate_fathom as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_seed_is_byte_identical_to_the_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_curator_refuses_to_run_without_a_mode(self) -> None:
		import curate_fathom as curator

		argv = sys.argv
		sys.argv = ["curate_fathom.py"]
		try:
			with self.assertRaises(SystemExit):
				curator.main()
		finally:
			sys.argv = argv

	def test_spatial_report_and_knowledge_note_exist(self) -> None:
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_MARKDOWN_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("bally.fathom.1981", report["machine_id"])
		self.assertEqual("partial", report["status"])
		self.assertEqual(952.0, report["coordinate_convention"]["source_bounds"]["right"])
		self.assertEqual(1974.0, report["coordinate_convention"]["source_bounds"]["bottom"])
		self.assertGreater(len(report["blockers"]), 0)

	def test_knowledge_note_records_the_platform_lessons(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("auxiliary lamp-column count", text)
		self.assertIn("public solenoid 20", text)
		self.assertIn("AS-2518-66", text)
		self.assertIn("AS-2518-52", text)
		self.assertIn("dead code", text)


class FathomRetainedEvidenceTests(unittest.TestCase):
	"""Skips cleanly when the external evidence roots are not configured."""

	def setUp(self) -> None:
		value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not value:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		self.source_root = Path(value).expanduser().resolve()

	def test_retained_extraction_matches_its_pinned_manifest(self) -> None:
		import curate_fathom as curator

		manifest = curator.verify_extraction_manifest(self.source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match(self) -> None:
		import curate_fathom as curator

		table = self.source_root / "bally/fathom-1981/source/Fathom (Bally 1981).vpx"
		script = self.source_root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))


if __name__ == "__main__":
	unittest.main()
