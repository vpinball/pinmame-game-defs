from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "high-speed-1986.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "high-speed-1986.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "high-speed-1986.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "high-speed-1986.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "high-speed-1986.json"
SPATIAL_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "high-speed-1986.md"
EXCERPT_DIR = ROOT / "evidence" / "excerpts" / "williams.high-speed.1986"

DRIVER_IDS = {"hs_l4", "hs_l3", "hs_l1", "hs_p4g", "hs_l4c"}
MATRIX_ADDRESSES = set(range(1, 65))
UNUSED_MATRIX_ADDRESSES = set(range(53, 65))
CABINET_SWITCH_ADDRESSES = {1, 2, 3, 4, 5, 6, 7, 8, 41}
BACKGLASS_LAMPS = {1, 2, 6}
UNPLACED_LAMPS = {42, 43, 44}
TWO_BULB_LAMPS = {1, 3, 9, 40}
# sxx.ssSw = {49,50,35,34,33,0} for hsGameData: public solenoid 17+i is driven by switch ssSw[i].
SPECIAL_SOLENOID_SWITCH = {17: 49, 18: 50, 19: 35, 20: 34, 21: 33}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _run_curator_without_mode() -> None:
	import curate_high_speed as curator

	argv = sys.argv
	sys.argv = ["curate_high_speed.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class HighSpeedDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_partial_identity_and_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.high-speed.1986", machine["id"])
		self.assertEqual("High Speed", machine["name"])
		self.assertEqual("Williams", machine["manufacturer"])
		self.assertEqual(1986, machine["year"])
		self.assertEqual({"width": 952.0, "height": 1974.0, "units": "vpx"}, machine["playfield"])
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual({"spatial_placement", "unresolved_conflicts"}, set(coverage["missing"]))
		self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("validated", coverage["dimensions"]["physical_wiring"])
		self.assertFalse(AUTHOR_READY_PATH.exists(), "a partial record must not have an author-ready twin")

	def test_the_machine_id_matches_its_directory_and_file_paths(self) -> None:
		# Three earlier games in this project shipped artifacts under the wrong manufacturer directory.
		machine_id = self.definition["machine"]["id"]
		manufacturer, _, _ = machine_id.partition(".")
		self.assertEqual("williams", manufacturer)
		self.assertEqual(manufacturer, DEFINITION_PATH.parent.name)
		self.assertEqual(manufacturer, SEED_PATH.parent.name)
		self.assertEqual(manufacturer, KNOWLEDGE_PATH.parent.name)
		self.assertEqual(manufacturer, SPATIAL_REPORT_PATH.parent.name)
		self.assertEqual(machine_id, EXCERPT_DIR.name)
		self.assertEqual(machine_id, load_json(SPATIAL_REPORT_PATH)["machine_id"])

	def test_controller_is_system_11_at_the_gen_s11x_bit(self) -> None:
		controller = self.definition["controller"]
		self.assertEqual("pinmame.system-11", controller["platform"])
		# GEN_S11X == GEN_S11A == GEN_S11B == 0x100 in src/wpc/gen.h.
		self.assertEqual("0x100", controller["hardware_generation"])
		self.assertTrue(controller["inversion_applied_by_emulator"])

	def test_every_hs_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		drivers = self.definition["drivers"]
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in drivers})
		for driver in drivers:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip())
		parent = next(driver for driver in drivers if driver["id"] == "hs_l4")
		self.assertNotIn("clone_of", parent)
		for driver in drivers:
			if driver["id"] != "hs_l4":
				self.assertEqual("hs_l4", driver["clone_of"])
		licence_build = next(driver for driver in drivers if driver["id"] == "hs_l1")
		self.assertEqual("1985", licence_build["year"])
		self.assertIn("Unidesa", licence_build["manufacturer"])
		self.assertIn("not a different physical machine", licence_build["variant_notes"])

	def test_the_full_system_11_switch_matrix_is_enumerated_column_major(self) -> None:
		matrix_only = {address for address in self.switches if address > 0}
		self.assertEqual(MATRIX_ADDRESSES, matrix_only)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
		diagnostic = {
			device["binding"]["device"]
			for device in self.definition["inputs"]
			if device["binding"]["group"] == "pinmame.input.switch" and device["binding"]["device"] < 0
		}
		self.assertEqual({-7, -6, -5, -4}, diagnostic)
		self.assertEqual(1, len(self.dips))
		self.assertIn(0, self.dips)

	def test_switch_address_formula_is_sequential_column_major(self) -> None:
		# address = (column-1)*8+row, so each of the eight columns is a contiguous run of eight.
		for column in range(8):
			for address in range(column * 8 + 1, column * 8 + 9):
				self.assertIn(address, self.switches)
				notes = self.switches[address]["physical"]["notes"]
				self.assertIn(f"drive column {column + 1}", notes)

	def test_the_manual_documents_no_opto_and_no_normally_closed_switch(self) -> None:
		# hsGameData's wpc struct is written by the positional initializer {{0}}, so wpc.invSw is
		# entirely unset and PinMAME normalizes no address; the manual shades nothing.
		for address, switch in self.switches.items():
			self.assertNotEqual("opto", switch.get("physical", {}).get("switch_type"), address)
			self.assertNotIn("normally_closed", switch, address)
		self.assertNotIn("polarity", self.definition["coverage"]["missing"])

	def test_untyped_switches_say_why_they_are_untyped(self) -> None:
		import curate_high_speed as curator

		for address in curator.UNTYPED_SWITCH_ADDRESSES:
			physical = self.switches[address]["physical"]
			self.assertNotIn("switch_type", physical, address)
			self.assertIn("never states the switch", physical["notes"], address)

	def test_flipper_lane_change_switches_are_not_eos_switches(self) -> None:
		for address in (37, 38):
			switch = self.switches[address]
			self.assertIn("Lane Change", switch["label"])
			self.assertIn("SW-1A-150", switch["physical"]["part_number"])
			self.assertIn("(EOS)", switch["physical"]["notes"])
			self.assertIn("03-7811", switch["physical"]["notes"])
		self.assertEqual("SW-1A-150-1", self.switches[37]["physical"]["part_number"])
		self.assertEqual("SW-1A-150", self.switches[38]["physical"]["part_number"])

	def test_switch_two_is_ball_roll_tilt_not_mux_feedback(self) -> None:
		# hw.gameSpecific1 is 0, so S11_MUXSW2 is unset for this driver.
		switch_two = self.switches[2]
		self.assertEqual("Ball Roll Tilt", switch_two["label"])
		self.assertIn("S11_MUXSW2 is unset", switch_two["physical"]["notes"])
		self.assertEqual("cabinet_or_service", switch_two["spatial"]["reason"])

	def test_cabinet_switches_have_no_playfield_coordinate(self) -> None:
		for address in CABINET_SWITCH_ADDRESSES:
			spatial = self.switches[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], address)
			self.assertEqual("cabinet_or_service", spatial["reason"], address)

	def test_projected_switches_say_they_are_projected(self) -> None:
		import curate_high_speed as curator

		for address in curator.SWITCH_PROJECTIONS:
			notes = self.switches[address]["physical"]["notes"]
			self.assertTrue(
				"rojected" in notes or "Taken from" in notes,
				f"switch {address} must disclose its projection",
			)
			self.assertEqual("validated", self.switches[address]["spatial"]["status"], address)

	def test_the_full_solenoid_address_space_1_to_50_is_enumerated_with_no_gaps(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(), set(self.solenoids) & set(range(51, 65)))

	def test_the_ac_mux_alias_bank_is_unpopulated_because_muxsol_is_zero(self) -> None:
		for address in range(25, 33):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"], address)
			self.assertEqual("unused", solenoid["availability"], address)
			self.assertIn("sxx.muxSol = 0", solenoid["physical"]["notes"], address)
			self.assertIn(f"alias of solenoid {address - 24}", solenoid["physical"]["notes"], address)

	def test_the_sound_overlay_range_is_unpopulated_because_gamespecific1_is_zero(self) -> None:
		for address in range(37, 45):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"], address)
			self.assertEqual("unused", solenoid["availability"], address)
			self.assertIn("S11_SNDOVERLAY is unset", solenoid["physical"]["notes"], address)

	def test_synthetic_flipper_solenoids_are_virtual_with_no_physical_device(self) -> None:
		for address in (45, 46, 47, 48):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"], address)
			self.assertEqual("used", solenoid["availability"], address)
			self.assertEqual("virtual", solenoid["spatial"]["reason"], address)
		self.assertIn("no FLIP_SOL bit", self.solenoids[45]["physical"]["notes"])
		for address in (33, 34, 35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_special_solenoids_are_driven_from_their_own_switch_via_sssw(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual(len(SPECIAL_SOLENOID_SWITCH), len(relationships))
		for solenoid, switch in SPECIAL_SOLENOID_SWITCH.items():
			key = f"relationship.special-solenoid-{solenoid}"
			self.assertIn(key, relationships)
			record = relationships[key]
			self.assertEqual("direct", record["kind"])
			self.assertEqual(f"switch.matrix-{switch}", record["source"])
			notes = self.solenoids[solenoid]["physical"]["notes"]
			self.assertIn(f"sxx.ssSw entry for this slot is {switch}", notes)
			self.assertIn(f"switch {switch}", notes)
		# Special #6 (public 22) is the one slot left at zero and must have no relationship.
		self.assertNotIn("relationship.special-solenoid-22", relationships)
		self.assertIn("no direct switch", self.solenoids[22]["physical"]["notes"])
		for address in range(17, 23):
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(f"Special #{address - 16}", aliases["manual.special-solenoid"])

	def test_relationship_endpoints_all_resolve(self) -> None:
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for record in self.definition["relationships"]:
			self.assertIn(record["source"], device_ids, record["id"])
			self.assertIn(record["destination"], device_ids, record["id"])

	def test_gi_is_one_solenoid_bound_address_with_no_invented_placement(self) -> None:
		gi_devices = [device for device in self.definition["outputs"] if device["kind"] == "gi"]
		self.assertEqual(1, len(gi_devices))
		gi = gi_devices[0]
		self.assertEqual(11, gi["binding"]["device"])
		self.assertEqual("pinmame.output.solenoid", gi["binding"]["group"])
		self.assertNotIn("spatial", gi)
		self.assertIn("9J2", gi["physical"]["notes"])
		self.assertIn("7J4", gi["physical"]["notes"])
		self.assertIn("8J4", gi["physical"]["notes"])
		self.assertIn("Backbox GI output", gi["physical"]["notes"])

	def test_backbox_and_cabinet_solenoids_have_controlled_records(self) -> None:
		for address in (4, 10, 15, 16):
			spatial = self.solenoids[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], address)
			self.assertEqual("cabinet_or_service", spatial["reason"], address)
		police = self.solenoids[4]
		self.assertEqual("relay", police["kind"])
		self.assertIn("#1683", police["physical"]["notes"])
		self.assertIn("Backbox", police["wiring"]["power_connection"])

	def test_the_hideout_coils_use_the_amended_name(self) -> None:
		for address in (7, 8):
			solenoid = self.solenoids[address]
			self.assertIn("Hideout Coil", solenoid["label"])
			self.assertIn("Hideout Relay", solenoid["physical"]["notes"])
			self.assertIn("B-11160", solenoid["physical"]["notes"])

	def test_solenoid_wiring_matches_the_printed_connector_banks(self) -> None:
		for address in range(1, 9):
			self.assertTrue(self.solenoids[address]["wiring"]["control_connection"].startswith("1P11-"), address)
		for address in range(9, 17):
			self.assertTrue(self.solenoids[address]["wiring"]["control_connection"].startswith("1P12-"), address)
		for address in range(17, 23):
			self.assertTrue(self.solenoids[address]["wiring"]["control_connection"].startswith("1P19-"), address)
		# The Amendments sheet's own special-solenoid transistor list.
		expected = {17: "Q75", 18: "Q71", 19: "Q73", 20: "Q69", 21: "Q77", 22: "Q79"}
		for address, transistor in expected.items():
			self.assertEqual(transistor, self.solenoids[address]["wiring"]["driver_transistor"], address)

	def test_the_full_lamp_matrix_is_enumerated_with_the_printed_two_bulb_circuits(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address in MATRIX_ADDRESSES:
			expected = 2 if address in TWO_BULB_LAMPS else 1
			self.assertEqual(expected, self.lamps[address]["physical"]["quantity"], address)
		for address in BACKGLASS_LAMPS:
			spatial = self.lamps[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], address)
			self.assertEqual("cabinet_or_service", spatial["reason"], address)
		for address in UNPLACED_LAMPS:
			self.assertNotIn("spatial", self.lamps[address], address)
			self.assertIn("B-10921", self.lamps[address]["physical"]["notes"], address)
		# Lamp 3's two bulbs straddle backglass and playfield, so one placement is correct.
		self.assertEqual(1, len(self.lamps[3]["spatial"]["placements"]))
		# Lamp 9's two bulbs are both on the playfield.
		self.assertEqual(2, len(self.lamps[9]["spatial"]["placements"]))
		# Lamp 40's second bulb is unlocated and the note must say so.
		self.assertEqual(1, len(self.lamps[40]["spatial"]["placements"]))
		self.assertIn("never says where the second one is", self.lamps[40]["physical"]["notes"])

	def test_lamp_wiring_names_both_a_column_and_a_row_driver(self) -> None:
		# Unlike the switch matrix, this manual's lamp matrix prints row transistors Q80-Q87.
		for address in (1, 8, 57, 64):
			transistor = self.lamps[address]["wiring"]["driver_transistor"]
			self.assertIn("column driver Q", transistor)
			self.assertIn("row driver Q8", transistor)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device.get("spatial")
			if spatial is None or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("validated", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				located += 1
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				self.assertEqual("playfield", placement["space"])
				for axis in ("x", "y"):
					self.assertGreaterEqual(placement[axis], 0.0)
					self.assertLessEqual(placement[axis], 1.0)
					self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)
				self.assertEqual("validated", placement["provenance"]["status"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(located, report["placement_count"])

	def test_the_trough_and_flippers_land_near_the_front_of_the_playfield(self) -> None:
		switch_pos = _positions(self.switches)
		self.assertGreater(switch_pos[9][1], 0.9)  # outhole
		for address in (10, 11, 12):
			self.assertGreater(switch_pos[address][1], 0.8)
		for address in (37, 38):
			self.assertGreater(switch_pos[address][1], 0.8)
		self.assertGreater(switch_pos[36][1], 0.8)  # ball shooter

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		lamp_pos = _positions(self.lamps)
		solenoid_pos = _positions(self.solenoids)
		# The jet-bumper triangle. The retained table binds 34 and 35 to the wrong two objects; these
		# three assertions are what make that error impossible to reintroduce silently.
		self.assertLess(switch_pos[34][0], switch_pos[35][0], "Lower Left bumper must be left of the Right bumper")
		self.assertLess(switch_pos[33][1], switch_pos[34][1], "Upper Left bumper must sit behind the Lower Left one")
		self.assertLess(switch_pos[33][0], switch_pos[35][0], "Upper Left bumper must be left of the Right bumper")
		# Each bumper coil sits on its own bumper.
		self.assertEqual(switch_pos[33], solenoid_pos[21])
		self.assertEqual(switch_pos[34], solenoid_pos[20])
		self.assertEqual(switch_pos[35], solenoid_pos[19])
		# Hideouts: upper switch behind lower one on each side, and left lane left of right lane.
		self.assertLess(switch_pos[39][1], switch_pos[40][1])
		self.assertLess(switch_pos[47][1], switch_pos[48][1])
		self.assertLess(switch_pos[39][0], switch_pos[47][0])
		self.assertLess(switch_pos[40][0], switch_pos[48][0])
		# Left/right pairs keep their sides.
		self.assertLess(switch_pos[20][0], switch_pos[21][0])  # flipper return lanes
		self.assertLess(switch_pos[31][0], switch_pos[32][0])  # outlanes
		self.assertLess(switch_pos[49][0], switch_pos[50][0])  # slingshot kickers
		self.assertLess(switch_pos[42][0], switch_pos[43][0])  # ramp rollovers
		self.assertLess(switch_pos[51][0], switch_pos[52][0])  # star rollovers
		self.assertLess(switch_pos[37][0], switch_pos[38][0])  # flipper lane change
		self.assertLess(solenoid_pos[17][0], solenoid_pos[18][0])  # slingshot coils
		# Spinners run left, centre, right.
		self.assertLess(switch_pos[44][0], switch_pos[45][0])
		self.assertLess(switch_pos[45][0], switch_pos[46][0])
		# Each spinner's own 1000-point arrow insert keeps the same order (lamps 7, 10, 8).
		self.assertLess(lamp_pos[7][0], lamp_pos[10][0])
		self.assertLess(lamp_pos[10][0], lamp_pos[8][0])
		# Freeway score ladder runs left to right, 25,000 through Lights Extra Ball.
		for lower, upper in zip(range(31, 35), range(32, 36)):
			self.assertLess(lamp_pos[lower][0], lamp_pos[upper][0], (lower, upper))
		# Stoplight banks: red behind yellow behind green on the two vertical banks.
		for red, yellow, green in ((13, 14, 15), (17, 18, 19)):
			self.assertLess(lamp_pos[red][1], lamp_pos[yellow][1])
			self.assertLess(lamp_pos[yellow][1], lamp_pos[green][1])
			self.assertLess(switch_pos[red][1], switch_pos[yellow][1])
			self.assertLess(switch_pos[yellow][1], switch_pos[green][1])
		# The right stoplight bank runs diagonally left to right instead.
		self.assertLess(lamp_pos[22][0], lamp_pos[23][0])
		self.assertLess(lamp_pos[23][0], lamp_pos[24][0])
		self.assertLess(switch_pos[22][0], switch_pos[23][0])
		self.assertLess(switch_pos[23][0], switch_pos[24][0])
		# Each arrow standup's insert sits on the same side of the playfield as its target.
		for address in (25, 26, 27):
			self.assertLess(lamp_pos[address][0], 0.5, address)
			self.assertLess(switch_pos[address][0], 0.5, address)
		for address in (28, 29, 30):
			self.assertGreater(lamp_pos[address][0], 0.5, address)
			self.assertGreater(switch_pos[address][0], 0.5, address)
		# Outlane specials keep their sides.
		self.assertLess(lamp_pos[4][0], lamp_pos[5][0])
		# The two Left Red flashers are both on the left, the two Right Red ones both on the right.
		for placement in self.solenoids[9]["spatial"]["placements"]:
			self.assertLess(placement["x"], 0.5)
		for placement in self.solenoids[12]["spatial"]["placements"]:
			self.assertGreater(placement["x"], 0.5)
		# The two Top Playfield flashers are both near the rear edge.
		for placement in self.solenoids[22]["spatial"]["placements"]:
			self.assertLess(placement["y"], 0.1)
		# Lamp 9's two bulbs are one per flipper return lane.
		left, right = sorted(placement["x"] for placement in self.lamps[9]["spatial"]["placements"])
		self.assertLess(left, 0.5)
		self.assertGreater(right, 0.5)

	def test_mechanism_inventory_covers_every_used_coil_motor_and_relay(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.eject-hole", "mechanism.left-hideout", "mechanism.right-hideout",
				"mechanism.ramp-gate", "mechanism.main-ramp", "mechanism.outlane-kickback",
				"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.spin-targets",
				"mechanism.stoplight-target-banks", "mechanism.standup-target-arrows", "mechanism.flippers",
				"mechanism.police-beacon", "mechanism.traffic-light", "mechanism.knocker",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
		}
		self.assertEqual(set(), physical - set(owners))

	def test_there_are_no_drop_targets_on_this_machine(self) -> None:
		for mechanism in self.definition["mechanisms"]:
			self.assertNotEqual("drop_target_bank", mechanism["kind"], mechanism["id"])
		banks = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.stoplight-target-banks")
		self.assertEqual(9, len(banks["sensors"]))
		self.assertEqual([], banks["actuators"])
		self.assertIn("standup", banks["behavior"])

	def test_the_ramp_gate_has_no_position_sensor(self) -> None:
		gate = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.ramp-gate")
		self.assertEqual("gate", gate["kind"])
		self.assertEqual([], gate["sensors"])
		self.assertIn("D-10884", gate["assembly_part_number"])
		self.assertIn("no switch, opto or sensor part of any kind", gate["behavior"])

	def test_the_police_beacon_is_a_backbox_mechanism_on_solenoid_four(self) -> None:
		beacon = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.police-beacon")
		self.assertEqual("motorized", beacon["kind"])
		self.assertEqual([], beacon["sensors"])
		self.assertEqual("C-10933", beacon["assembly_part_number"])
		self.assertIn("Backbox", beacon["behavior"])
		self.assertEqual([self.solenoids[4]["id"]], beacon["actuators"])

	def test_display_inventory_is_the_six_displays_the_manual_names(self) -> None:
		displays = {display["id"]: display for display in self.definition["displays"]}
		self.assertEqual(
			{
				"display.speeder-1", "display.speeder-2", "display.speeder-3", "display.speeder-4",
				"display.ball-in-play-match", "display.credits",
			},
			set(displays),
		)
		for display in displays.values():
			self.assertEqual("segment", display["kind"])
			self.assertEqual("not_applicable", display["spatial"]["status"])
			self.assertEqual("cabinet_or_service", display["spatial"]["reason"])
		# s11_dispS11: two 7-digit 16-segment, two 7-digit 7-segment, four single small digits.
		self.assertEqual([1, 9, 21, 29], [displays[f"display.speeder-{n}"]["segment_start"] for n in (1, 2, 3, 4)])
		for n in (1, 2, 3, 4):
			self.assertEqual(7, displays[f"display.speeder-{n}"]["width"])
		self.assertEqual(2, displays["display.ball-in-play-match"]["width"])
		self.assertEqual(2, displays["display.credits"]["width"])
		self.assertEqual(0, displays["display.ball-in-play-match"]["segment_start"])
		self.assertEqual(20, displays["display.credits"]["segment_start"])
		for identifier in ("display.ball-in-play-match", "display.credits"):
			self.assertIn("non-contiguous", displays[identifier]["label"])
		self.assertEqual(
			{0, 1, 2, 3, 4, 5},
			{display["controller_index"] for display in displays.values()},
		)

	def test_two_conflicts_are_recorded_and_named_in_the_spatial_report(self) -> None:
		conflicts = {item["id"]: item for item in self.definition["conflicts"]}
		self.assertEqual(
			{"conflict.upper-flipper-driving-button", "conflict.coin-lockout-relay-part-number"},
			set(conflicts),
		)
		for conflict in conflicts.values():
			self.assertGreaterEqual(len(conflict["source_refs"]), 2)
			self.assertIn("Unresolved.", conflict["description"])
		self.assertIn("16", conflicts["conflict.coin-lockout-relay-part-number"]["path"])
		self.assertIn("904218-696", conflicts["conflict.coin-lockout-relay-part-number"]["description"])
		self.assertIn("404603-22", conflicts["conflict.coin-lockout-relay-part-number"]["description"])
		self.assertEqual("404603-22", self.solenoids[16]["physical"]["part_number"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(sorted(conflicts), sorted(report["unresolved"]))

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.high-speed-1986", sources)
		self.assertTrue(sources["vpx-script.high-speed-1986"]["known_working"])
		self.assertEqual(
			"149cab01a1fbe7657ffae87f72fa6982ed631653627b938186d5d8ed893195eb",
			sources["vpx-script.high-speed-1986"]["sha256"],
		)
		self.assertEqual(
			"f57801a428f78f85b6cd40f4e47a74bd8e063227355d26ec4f15ef7f11d78af1",
			sources["vpx-table.high-speed-1986"]["sha256"],
		)
		self.assertEqual(
			"4aa21267d2edf016c2450f35e23b01eea74ff07e25b4b9a9d9c472f5c9e8c1dd",
			sources["manual.williams.high-speed.1986"]["sha256"],
		)
		for source in self.definition["sources"]:
			self.assertNotEqual("runtime_scenario", source["kind"])
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("e:\\", value.lower())
					self.assertNotIn("e:/", value.lower())
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_the_pinmame_source_locator_records_the_decoded_initgamefull_expansion(self) -> None:
		core = next(source for source in self.definition["sources"] if source["kind"] == "pinmame_core")
		locator = core["locator"]
		for fragment in (
			"INITGAMEFULL(hs,GEN_S11X,s11_dispS11,0,FLIP_SWNO(37,38),S11_BCDDIAG,0,0,0,49,50,35,34,33,0)",
			"sxx.ssSw = {49,50,35,34,33,0}",
			"sxx.muxSol = 0",
			"wpc.invSw",
			"lines 191-200",
		):
			self.assertIn(fragment, locator, fragment)

	def test_manual_source_declares_every_excerpt_and_every_crop_is_derived(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["id"] == "manual.williams.high-speed.1986")
		excerpts = {excerpt["id"]: excerpt for excerpt in manual["excerpts"]}
		self.assertEqual(
			{
				"excerpt.high-speed.switch-matrix", "excerpt.high-speed.switch-locations",
				"excerpt.high-speed.lamp-matrix", "excerpt.high-speed.lamp-locations",
				"excerpt.high-speed.solenoid-table", "excerpt.high-speed.solenoid-flasher-locations",
				"excerpt.high-speed.general-illumination", "excerpt.high-speed.boards-and-assemblies",
				"excerpt.high-speed.diagnostics-and-amendments",
			},
			set(excerpts),
		)
		for excerpt in excerpts.values():
			self.assertEqual("manual", excerpt["method"])
			self.assertTrue(excerpt["reviewed"])
			self.assertTrue(excerpt["path"].startswith("evidence/excerpts/williams.high-speed.1986/"))
			if excerpt.get("image"):
				self.assertTrue(excerpt["image_derivation"])
		self.assertEqual(
			3,
			sum(1 for excerpt in excerpts.values() if excerpt.get("image")),
			"the switch matrix, the lamp matrix and the GI wiring are the three drawing-shaped facts",
		)

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.system-11", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])
		groups = {group["id"]: group for group in profile["groups"]}
		used = {device["binding"]["group"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		self.assertTrue(used <= set(groups))

		def allowed(group_id: str, address: int) -> bool:
			for rule in groups[group_id]["address_rules"]:
				if "values" in rule and address in rule["values"]:
					return True
				if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
					return True
			return False

		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			self.assertTrue(allowed(device["binding"]["group"], device["binding"]["device"]), device["id"])

	def test_knowledge_note_exists_and_is_referenced(self) -> None:
		self.assertEqual("knowledge/williams/high-speed-1986.md", self.definition["knowledge"]["path"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("sxx.ssSw", text)
		self.assertIn("The Getaway", text)  # the sequel must be explicitly disambiguated
		self.assertIn("no drop-target", text.lower().replace("drop targets", "drop-target"))


class HighSpeedCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_high_speed as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_high_speed as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_high_speed as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"High Speed", b"Hgih Speed", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_curator_refuses_to_overwrite_an_author_ready_artifact(self) -> None:
		import curate_high_speed as curator

		self.assertFalse(AUTHOR_READY_PATH.exists())
		AUTHOR_READY_PATH.parent.mkdir(parents=True, exist_ok=True)
		AUTHOR_READY_PATH.write_text("{}", encoding="utf-8")
		try:
			with self.assertRaises(RuntimeError):
				curator.generate(ROOT)
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			AUTHOR_READY_PATH.unlink()
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_high_speed as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())
		self.assertEqual(
			curator.render_spatial_report(report),
			SPATIAL_MARKDOWN_PATH.read_text(encoding="utf-8"),
		)

	def test_spatial_report_names_every_omitted_output(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		omitted = {entry["address"] for entry in report["omitted_outputs"]}
		self.assertEqual({11, 42, 43, 44}, omitted)
		self.assertEqual(3, len(report["blockers"]))


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class HighSpeedRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_high_speed as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_high_speed as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/high-speed-1986/source/High Speed (Williams 1986).vpx"
		script = source_root / "williams/high-speed-1986/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_hash_matches_the_definition(self) -> None:
		import curate_high_speed as curator

		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("manuals root is not configured")
		manual = (
			Path(root)
			/ "by-machine"
			/ "williams.high-speed.1986"
			/ "archive-williams-high-speed-instruction-manual"
			/ "high_speed_instruction_manual.pdf"
		)
		self.assertEqual(curator.MANUAL_SHA256, curator._file_sha256(manual))

	def test_review_artifacts_match_their_pinned_hashes(self) -> None:
		import curate_high_speed as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		base = Path(root) / "high-speed-1986"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(base / "manual-transcription.md"))
		self.assertEqual(curator.VPX_GEOMETRY_SHA256, curator._file_sha256(base / "vpx-geometry.txt"))


if __name__ == "__main__":
	unittest.main()
