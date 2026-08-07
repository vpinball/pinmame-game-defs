from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "funhouse-1990.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "funhouse-1990.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "funhouse-1990.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "funhouse-1990.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-alpha.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.md"

DRIVER_IDS = {
	"fh_l9", "fh_d9", "fh_l9b", "fh_d9b", "fh_905h", "fh_906h", "fh_907h", "fh_pa1",
	"fh_l2", "fh_l3", "fh_d3", "fh_l4", "fh_d4", "fh_l5", "fh_d5", "fh_f91",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {51, 55}


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
	import curate_funhouse as curator

	argv = sys.argv
	sys.argv = ["curate_funhouse.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class FunHouseDefinitionTests(unittest.TestCase):
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
		self.assertEqual(
			["spatial_placement", "unresolved_conflicts", "recreation_notes"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["semantic_naming"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual("williams.funhouse.1990", self.definition["machine"]["id"])
		self.assertEqual("Williams", self.definition["machine"]["manufacturer"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1990, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-alpha", self.definition["controller"]["platform"])
		self.assertEqual("0x2", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		driver_ids = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, driver_ids)
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["fh_l9"])
		for driver_id in DRIVER_IDS - {"fh_l9"}:
			self.assertEqual("fh_l9", by_id[driver_id]["clone_of"], driver_id)
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"})
			self.assertGreater(len(driver["variant_notes"]), 0)
		self.assertEqual("compatible", by_id["fh_pa1"]["physical_compatibility"])
		self.assertIn("GEN_WPCALPHA_1", by_id["fh_pa1"]["variant_notes"])

	def test_controller_profile_reused_unchanged(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-alpha", profile["id"])
		group_ids = {group["id"] for group in profile["groups"]}
		self.assertEqual(
			{"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi"},
			group_ids,
		)

	def test_switch_matrix_enumeration_and_unused_positions(self) -> None:
		matrix_switches = {addr: sw for addr, sw in self.switches.items() if addr in MATRIX_ADDRESSES}
		self.assertEqual(MATRIX_ADDRESSES, set(matrix_switches))
		for address, switch in matrix_switches.items():
			if address in UNUSED_MATRIX_ADDRESSES:
				self.assertEqual("unused", switch["availability"], address)
				self.assertEqual("not_applicable", switch["spatial"]["status"], address)
				self.assertEqual("unused", switch["spatial"]["reason"], address)
			else:
				self.assertEqual("used", switch["availability"], address)
		for address in range(1, 9):
			self.assertIn(address, self.switches, f"cabinet switch {address}")
			self.assertEqual("switch.cabinet-" + str(address), self.switches[address]["id"])
		for address in range(1, 9):
			key = 1000 + address
			# DIP switches are a separate binding group; verified below.
		dips = bindings(self.definition, "inputs", "pinmame.input.dip")
		self.assertEqual(set(range(1, 9)), set(dips))

	def test_only_two_optos_and_pinmame_normalizes_both(self) -> None:
		for address, switch in self.switches.items():
			if address not in MATRIX_ADDRESSES:
				continue
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"].get("switch_type"), address)
				self.assertTrue(switch["normally_closed"], address)
			elif address not in UNUSED_MATRIX_ADDRESSES and address != 24:
				self.assertNotEqual("opto", switch["physical"].get("switch_type"), address)

	def test_constant_switch_24(self) -> None:
		switch = self.switches[24]
		self.assertEqual("constant", switch["kind"])
		self.assertTrue(switch["constant_active"])
		self.assertTrue(switch["initial_active"])
		self.assertEqual("constant", switch["spatial"]["reason"])

	def test_flipper_switches_have_no_cpu_solenoid(self) -> None:
		solenoid_addresses = set(self.solenoids)
		for address in (33, 34, 35, 36, 45, 46, 47, 48):
			self.assertNotIn(address, solenoid_addresses, f"no flipper solenoid should exist at {address}")
		self.assertIn(11, self.switches)
		self.assertIn(12, self.switches)
		self.assertEqual("Right Flipper", self.switches[11]["label"])
		self.assertEqual("Left Flipper", self.switches[12]["label"])
		flipper_mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.flippers")
		self.assertEqual([], flipper_mechanism["actuators"])

	def test_solenoid_enumeration(self) -> None:
		self.assertEqual(set(range(1, 29)), set(self.solenoids))
		flasher_addresses = {17, 18, 19, 20, 23, 24}
		for address in flasher_addresses:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
			self.assertGreaterEqual(self.solenoids[address]["physical"]["quantity"], 1)
		self.assertEqual("motor", self.solenoids[21]["kind"])
		self.assertEqual("motor", self.solenoids[22]["kind"])
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])

	def test_lamp_matrix_fully_populated_with_no_unused_position(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address, lamp in self.lamps.items():
			self.assertEqual("used", lamp["availability"], address)

	def test_multi_bulb_lamp_quantities_match_manual_markers(self) -> None:
		for address in (53, 61, 82):
			lamp = self.lamps[address]
			self.assertEqual(2, lamp["physical"]["quantity"], address)
			self.assertEqual(2, len(lamp["spatial"]["placements"]), address)
		for address in (51, 52, 72):
			lamp = self.lamps[address]
			self.assertEqual(1, lamp["physical"]["quantity"], address)
			self.assertEqual(1, len(lamp["spatial"]["placements"]), address)

	def test_lamps_without_resolved_spatial_are_named_and_omit_the_key(self) -> None:
		for address in (54, 55, 56):
			lamp = self.lamps[address]
			self.assertNotIn("spatial", lamp, address)
			self.assertIn("finger", lamp["physical"]["notes"], address)

	def test_switch_63_has_no_resolved_spatial(self) -> None:
		self.assertNotIn("spatial", self.switches[63])

	def test_gangway_lamp_conflict_is_recorded(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertIn("conflict.gangway-lamp-12-value", conflicts)
		conflict = conflicts["conflict.gangway-lamp-12-value"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		self.assertIn("unresolved", conflict["description"].lower())
		self.assertEqual("Gangway 100,000", self.lamps[12]["label"])

	def test_gi_region_conflict_is_recorded(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertIn("conflict.gi-region-naming", conflicts)
		self.assertEqual({"conflict.gangway-lamp-12-value", "conflict.gi-region-naming"}, set(conflicts))

	def test_gi_enumeration_and_dispositions(self) -> None:
		self.assertEqual(set(range(5)), set(self.gi))
		self.assertEqual("not_applicable", self.gi[0]["spatial"]["status"])
		self.assertEqual("validated", self.gi[1]["spatial"]["status"])
		self.assertEqual(3, len(self.gi[1]["spatial"]["placements"]))
		self.assertNotIn("spatial", self.gi[2])
		self.assertEqual("not_applicable", self.gi[3]["spatial"]["status"])
		self.assertNotIn("spatial", self.gi[4])

	def test_displays_are_two_sixteen_character_segment_displays(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(2, len(displays))
		for display in displays:
			self.assertEqual("segment", display["kind"])
			self.assertEqual(16, display["width"])
			self.assertEqual("not_applicable", display["spatial"]["status"])
		by_index = {display["controller_index"]: display for display in displays}
		self.assertEqual({0, 1}, set(by_index))
		self.assertEqual(0, by_index[0]["segment_start"])
		self.assertEqual(20, by_index[1]["segment_start"])

	def test_mechanisms_present(self) -> None:
		mechanism_ids = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		expected = {
			"mechanism.rudy-jaw", "mechanism.rudy-eyes", "mechanism.trap-door", "mechanism.step-gate",
			"mechanism.ramp-diverter", "mechanism.trough-and-shooters", "mechanism.tunnel-kickout",
			"mechanism.rudys-hideout", "mechanism.dummy-eject-hole", "mechanism.multiball-lock",
			"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.flippers",
		}
		self.assertEqual(expected, mechanism_ids)

	def test_spatial_positions_are_in_range_and_at_most_six_decimals(self) -> None:
		for collection in (self.switches, self.solenoids, self.lamps, self.gi):
			for device in collection.values():
				spatial = device.get("spatial")
				if spatial is None or spatial["status"] != "validated":
					continue
				for placement in spatial["placements"]:
					for axis in ("x", "y"):
						self.assertGreaterEqual(placement[axis], 0.0)
						self.assertLessEqual(placement[axis], 1.0)
						self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: sw["spatial"]["placements"][0]["x"] for addr, sw in self.switches.items() if sw.get("spatial") and sw["spatial"]["status"] == "validated"}
		switch_y = {addr: sw["spatial"]["placements"][0]["y"] for addr, sw in self.switches.items() if sw.get("spatial") and sw["spatial"]["status"] == "validated"}
		lamp_x = {addr: lamp["spatial"]["placements"][0]["x"] for addr, lamp in self.lamps.items() if lamp.get("spatial") and lamp["spatial"]["status"] == "validated"}

		# Left flipper (12) sits left of right flipper (11).
		self.assertLess(switch_x[12], switch_x[11])
		# Left slingshot (41) sits left of right slingshot (53).
		self.assertLess(switch_x[41], switch_x[53])
		# Left outlane (43) sits left of right outlane (52).
		self.assertLess(switch_x[43], switch_x[52])
		# Jet bumpers: Left (18) < Lower (68) < Right (77), matching the switch labels' own naming.
		self.assertLess(switch_x[18], switch_x[68])
		self.assertLess(switch_x[68], switch_x[77])
		# Left ballshooter (47) sits left of right ballshooter (62).
		self.assertLess(switch_x[47], switch_x[62])

		# Rear/front: the trap door (76) sits well toward the rear/backglass end relative to the
		# flippers (11/12), which sit at the front/apron end.
		self.assertLess(switch_y[76], switch_y[11])
		self.assertLess(switch_y[76], switch_y[12])

		# Gangway lamp row (11-16) reads left to right in ascending address order.
		self.assertLess(lamp_x[11], lamp_x[12])
		self.assertLess(lamp_x[12], lamp_x[13])
		self.assertLess(lamp_x[13], lamp_x[14])
		self.assertLess(lamp_x[14], lamp_x[15])
		self.assertLess(lamp_x[15], lamp_x[16])

		# Lamp 61's two placements: the "Left" one is left of the "Inside Rt" one.
		placements_61 = self.lamps[61]["spatial"]["placements"]
		self.assertLess(placements_61[0]["x"], placements_61[1]["x"])
		# Lamp 82's two placements (Special Outlanes, left and right) likewise.
		placements_82 = self.lamps[82]["spatial"]["placements"]
		self.assertLess(placements_82[0]["x"], placements_82[1]["x"])

	def test_lamp_position_agrees_with_the_bumper_switch_it_names(self) -> None:
		# Lamp 51 ("Lower Jet Bumper") should sit close to switch/solenoid 68's Lower Jet Bumper
		# object (both bind to the retained table's Bumper3 object).
		lamp_x = self.lamps[51]["spatial"]["placements"][0]["x"]
		switch_x = self.switches[68]["spatial"]["placements"][0]["x"]
		self.assertAlmostEqual(lamp_x, switch_x, delta=0.01)

	def test_seed_is_byte_identical_to_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_no_stale_author_ready_definition(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_curator_check_passes(self) -> None:
		import curate_funhouse as curator

		curator.check(ROOT)

	def test_curator_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_spatial_report_matches_curator(self) -> None:
		import curate_funhouse as curator

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_device_identifiers_are_unique(self) -> None:
		identifiers = [device["id"] for device in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_excerpts_referenced_by_manual_source_exist_and_hash_match(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.williams.funhouse.1990"]
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), excerpt["path"])
			import hashlib

			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			self.assertEqual(excerpt["sha256"], digest, excerpt["path"])
			if "image" in excerpt:
				image_path = ROOT / excerpt["image"]
				self.assertTrue(image_path.is_file(), excerpt["image"])
				image_digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
				self.assertEqual(excerpt["image_sha256"], image_digest, excerpt["image"])


if __name__ == "__main__":
	unittest.main()
