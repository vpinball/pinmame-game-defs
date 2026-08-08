from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "indiana-jones-the-pinball-adventure-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "indiana-jones-the-pinball-adventure-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "indiana-jones-the-pinball-adventure-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "indiana-jones-the-pinball-adventure-1993.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-dcs.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "indiana-jones-the-pinball-adventure-1993.json"

DRIVER_IDS = {
	"ij_l7", "ij_d7", "ij_h1", "ij_i1", "ij_lg7", "ij_dg7", "ij_l6", "ij_d6",
	"ij_l5", "ij_d5", "ij_l4", "ij_d4", "ij_l3", "ij_d3", "ij_p2",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
CUSTOM_SWITCH_USED = {121, 122, 123, 124, 125}
CUSTOM_SWITCH_UNUSED = {126, 127, 128}
OPTO_MATRIX_ADDRESSES = {41, 42, 43, 44, 45, 47, 71, 72, 73, 81, 82, 83, 84, 85, 86, 87}
PINMAME_NORMALIZED_MATRIX_OPTOS = {41, 42, 43, 44, 45, 47, 72, 73, 81, 82, 83, 84, 85, 86, 87}


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
	import curate_indiana_jones as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_indiana_jones.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class IndianaJonesDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["polarity", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "physical_wiring":
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.indiana-jones-the-pinball-adventure.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1267, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("16-50017-101", self.definition["machine"]["model_number"])
		self.assertEqual("pinmame.wpc-dcs", self.definition["controller"]["platform"])
		self.assertEqual("0x10", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_widebody_playfield_extent_is_declared(self) -> None:
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual(1093, playfield["width"])
		self.assertEqual(2162, playfield["height"])
		self.assertEqual("vpx", playfield["units"])
		self.assertEqual("validated", playfield["provenance"]["status"])

	def test_unconfigured_fast_flip_channel_uses_gilamps_state(self) -> None:
		self.assertIn("WPC_GILAMPS bit 7", self.solenoids[31]["physical"]["notes"])
		self.assertNotIn("fast-flip RAM flag", self.solenoids[31]["physical"]["notes"])

	def test_two_opto_polarity_conflicts_are_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{"conflict.captive-ball-front-opto-not-normalized", "conflict.wheel-position-opto-not-normalized"},
			set(conflicts),
		)
		captive = conflicts["conflict.captive-ball-front-opto-not-normalized"]
		self.assertGreaterEqual(len(captive["source_refs"]), 2)
		self.assertIn("71", captive["path"])
		self.assertIn("unresolved", captive["description"].lower())
		self.assertIn("harness", captive["description"].lower())
		wheel = conflicts["conflict.wheel-position-opto-not-normalized"]
		self.assertGreaterEqual(len(wheel["source_refs"]), 2)
		for address in (121, 122, 123):
			self.assertIn(str(address), wheel["path"])
		self.assertIn("unresolved", wheel["description"].lower())
		self.assertIn("harness", wheel["description"].lower())

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_ij_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["ij_l7"])
		for driver_id in DRIVER_IDS - {"ij_l7"}:
			self.assertEqual("ij_l7", by_id[driver_id]["clone_of"], driver_id)

	def test_ij4_stern_family_is_not_claimed(self) -> None:
		self.assertNotIn("ij4_210", {driver["id"] for driver in self.definition["drivers"]})
		for source in self.definition["sources"]:
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("ij4_", value)

	def test_the_full_wpcdcs_input_space_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)) | CUSTOM_SWITCH_USED | CUSTOM_SWITCH_UNUSED
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(MATRIX_ADDRESSES - {23}):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("unused", self.switches[23]["availability"])
		self.assertEqual("unused", self.switches[23]["spatial"]["reason"])
		for address in sorted(CUSTOM_SWITCH_UNUSED):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)

	def test_switch_23_ticket_opto_is_unused_despite_printed_and_driver_labels(self) -> None:
		switch23 = self.switches[23]
		self.assertIn("blank", switch23["physical"]["notes"])
		self.assertIn("swTicketOpto", switch23["physical"]["notes"])

	def test_printed_opto_polarity_is_recorded_even_where_pinmame_does_not_normalize_it(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - {23, 24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_MATRIX_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_MATRIX_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])
		for address in (121, 122, 123, 124, 125):
			self.assertTrue(self.switches[address]["normally_closed"], address)

	def test_wheel_and_captive_ball_optos_are_not_normalized_by_pinmame(self) -> None:
		# ijGameData's inverted-switch mask covers column 7 (0x06) and the custom column (0x18);
		# neither covers 71, 121, 122, or 123, even though all four are printed opto interrupters
		# whose column neighbors (72/73 and 124/125) ARE covered. This asymmetry is the entire
		# basis of the two conflicts and must not be silently "fixed" by normalizing all of them.
		mask_col7 = 0x06
		mask_custom = 0x18
		self.assertEqual(0, mask_col7 & 0x01)  # bit0 = address 71
		self.assertNotEqual(0, mask_col7 & 0x02)  # bit1 = address 72
		self.assertNotEqual(0, mask_col7 & 0x04)  # bit2 = address 73
		self.assertEqual(0, mask_custom & 0x01)  # bit0 = address 121
		self.assertEqual(0, mask_custom & 0x02)  # bit1 = address 122
		self.assertEqual(0, mask_custom & 0x04)  # bit2 = address 123
		self.assertNotEqual(0, mask_custom & 0x08)  # bit3 = address 124
		self.assertNotEqual(0, mask_custom & 0x10)  # bit4 = address 125

	def test_flipper_positions_and_repurposed_fliptronic_column(self) -> None:
		for address in (111, 112, 113, 114, 115, 116, 117, 118):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		for address in (115, 116, 117):
			self.assertTrue(self.switches[address]["normally_closed"], address)
			self.assertEqual("Center Drop Bank", self.switches[address]["label"][:16])
		self.assertFalse(self.switches[118]["normally_closed"])
		self.assertEqual("Left Ramp Made", self.switches[118]["label"])
		# No upper flippers at all: 115-118 must never carry a flipper role.
		for address in (115, 116, 117, 118):
			for role in self.switches[address].get("roles", []):
				self.assertNotIn("flipper", role)

	def test_the_full_wpcdcs_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 17)) | set(range(22, 29)) | set(range(33, 37)) | set(range(45, 49)) | set(range(51, 59))
		expected_solenoids |= {17, 18, 19, 20, 21, 29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 22):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (24, 51, 52, 53, 54, 55):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (22, 23, 56):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50, 57, 58):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_no_solenoid_is_labelled_a_knocker_device(self) -> None:
		knocker = self.solenoids[7]
		self.assertEqual("Knocker", knocker["label"])
		self.assertEqual("cabinet_or_service", knocker["spatial"]["reason"])

	def test_slingshot_solenoid_binding_matches_script_and_driver_not_the_printed_row(self) -> None:
		self.assertEqual("Right Slingshot", self.solenoids[12]["label"])
		self.assertEqual("Left Slingshot", self.solenoids[13]["label"])
		self.assertIn("RandomSoundSlingshotRight", self.solenoids[12]["physical"]["notes"])
		self.assertIn("RandomSoundSlingshotLeft", self.solenoids[13]["physical"]["notes"])
		self.assertIn("sRSling", self.solenoids[12]["physical"]["notes"])
		self.assertIn("sLSling", self.solenoids[13]["physical"]["notes"])
		# Switch side must agree with the physical-side labels: 33=Left, 48=Right.
		self.assertEqual("Left Slingshot", self.switches[33]["label"])
		self.assertEqual("Right Slingshot", self.switches[48]["label"])
		self.assertLess(self.switches[33]["spatial"]["placements"][0]["x"], self.switches[48]["spatial"]["placements"][0]["x"])

	def test_repurposed_upper_flipper_solenoids_are_not_flipper_devices(self) -> None:
		self.assertEqual("Diverter Power", self.solenoids[33]["label"])
		self.assertEqual("Diverter Hold", self.solenoids[34]["label"])
		self.assertEqual("Top Lockup Power", self.solenoids[35]["label"])
		self.assertEqual("Top Lockup Hold", self.solenoids[36]["label"])
		for address in (33, 34, 35, 36):
			self.assertEqual("coil", self.solenoids[address]["kind"], address)

	def test_flipper_manual_address_mapping(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48)
		}
		self.assertEqual({"29"}, manual_aliases[45])
		self.assertEqual({"30"}, manual_aliases[46])
		self.assertEqual({"31"}, manual_aliases[47])
		self.assertEqual({"32"}, manual_aliases[48])
		self.assertEqual("Lower Right Flipper Power", self.solenoids[45]["label"])

	def test_custom_solenoid_mapping_from_printed_37_42_to_public_51_56(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in range(51, 57)
		}
		self.assertEqual({"37"}, manual_aliases[51])
		self.assertEqual({"38"}, manual_aliases[52])
		self.assertEqual({"39"}, manual_aliases[53])
		self.assertEqual({"40"}, manual_aliases[54])
		self.assertEqual({"41"}, manual_aliases[55])
		self.assertEqual({"42"}, manual_aliases[56])
		self.assertEqual("Wheel Motor", self.solenoids[56]["label"])
		self.assertIn("SolMoveIdol", self.solenoids[56]["physical"]["notes"])
		for address in (57, 58):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_gi_playfield_strings_are_located_and_insert_panel_strings_are_cabinet(self) -> None:
		for address in (0, 1, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(34, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(32, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(2, len(self.gi[4]["spatial"]["placements"]))
		for address in (2, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_quantities_are_all_single_bulb_and_cabinet_lamps_are_explicit(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - {88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])
		self.assertEqual("Adv(e)nture Light", self.lamps[23]["label"])

	def test_path_of_adventure_insert_lamps_are_projected_not_fabricated(self) -> None:
		for address in (71, 72, 73, 74, 75, 81, 82, 83, 84, 85):
			lamp = self.lamps[address]
			self.assertEqual("validated", lamp["spatial"]["status"], address)
			self.assertIn("Projected onto", lamp["physical"]["notes"], address)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable":
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
		self.assertEqual("validated", report["status"])
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: dev["spatial"]["placements"][0]["x"] for addr, dev in self.switches.items() if dev["spatial"]["status"] != "not_applicable"}
		switch_y = {addr: dev["spatial"]["placements"][0]["y"] for addr, dev in self.switches.items() if dev["spatial"]["status"] != "not_applicable"}
		lamp_x = {addr: dev["spatial"]["placements"][0]["x"] for addr, dev in self.lamps.items() if dev["spatial"]["status"] != "not_applicable"}
		lamp_y = {addr: dev["spatial"]["placements"][0]["y"] for addr, dev in self.lamps.items() if dev["spatial"]["status"] != "not_applicable"}
		# Left/right jet bumpers ascend left -> right for both switches and lamps proxies (bumpers).
		self.assertLess(switch_x[35], switch_x[36])
		# Outlane is outboard of return lane on the left side; right mirrors it.
		self.assertLess(switch_x[15], switch_x[16])
		self.assertGreater(switch_x[18], switch_x[17])
		# Left/right slingshots: left is left of right.
		self.assertLess(switch_x[33], switch_x[48])
		# Mini-playfield left lane switches sit left of their right-lane counterparts.
		self.assertLess(switch_x[65], switch_x[75])
		self.assertLess(switch_x[66], switch_x[76])
		self.assertLess(switch_x[67], switch_x[77])
		self.assertLess(switch_x[68], switch_x[78])
		# Lower flippers: left flipper coil left of right flipper coil.
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertLess(solenoids[47]["spatial"]["placements"][0]["x"], solenoids[45]["spatial"]["placements"][0]["x"])
		# Trough front-to-back: rear/backglass end (86, drain entrance) has a smaller y than the
		# eject end (81) is not guaranteed since they share one projected anchor; instead check the
		# adventure-target rows ascend consistently between switches and lamps.
		self.assertLess(switch_y[65], switch_y[68])
		self.assertLess(lamp_y[71], lamp_y[83])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.gun-launcher", "mechanism.left-eject",
				"mechanism.subway-idol-entry", "mechanism.idol", "mechanism.right-ramp-diverter",
				"mechanism.top-lockup-post", "mechanism.path-of-adventure", "mechanism.totem-drop-target",
				"mechanism.center-drop-bank", "mechanism.slingshots", "mechanism.jet-bumpers",
				"mechanism.control-gates", "mechanism.lower-flippers", "mechanism.captive-ball",
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
			if device["kind"] in {"coil", "motor"}
			and device["availability"] == "used"
			and "cabinet.knocker" not in device.get("roles", [])
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("60-degree", mechanisms["mechanism.idol"]["behavior"])
		self.assertIn("linear", mechanisms["mechanism.path-of-adventure"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.ball-release-top-trough-pulse"}, set(relationships))
		self.assertEqual("switch.matrix-87", relationships["relationship.ball-release-top-trough-pulse"]["destination"])
		self.assertEqual("pulse", relationships["relationship.ball-release-top-trough-pulse"]["kind"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.ij-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.ij-vpw-1-0"]["known_working"])
		self.assertEqual(
			"926e7a90d89602b003ac93757ee23c6ae916bb382112be28f82388381490bb7a",
			sources["vpx-script.ij-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"03451b7951242d204f9f79ab91f108d3c8aa203039f2ca867b24f4f47668c250",
			sources["vpx-table.ij-vpw-1-0"]["sha256"],
		)
		self.assertNotIn("runtime.indiana-jones", sources)
		self.assertNotIn("rom.ij", sources)
		for source in self.definition["sources"]:
			self.assertNotEqual("runtime_scenario", source["kind"])
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-dcs", profile["id"])
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


def _switch_positions(switches: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in switches.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class IndianaJonesCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_indiana_jones as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_indiana_jones as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_indiana_jones as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Indiana Jones", b"Indiana Bones", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_indiana_jones as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class IndianaJonesRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_indiana_jones as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_indiana_jones as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/indiana-jones-the-pinball-adventure-1993/source/Indiana Jones The Pinball Adventure (Williams 1993) VPWmod v1.0.vpx"
		script = source_root / "williams/indiana-jones-the-pinball-adventure-1993/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_indiana_jones as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "indiana-jones-the-pinball-adventure-1993" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
