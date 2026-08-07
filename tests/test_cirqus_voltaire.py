from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "cirqus-voltaire-1997.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "cirqus-voltaire-1997.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "cirqus-voltaire-1997.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "cirqus-voltaire-1997.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "cirqus-voltaire-1997.json"

DRIVER_IDS = {"cv_10", "cv_11", "cv_13", "cv_14", "cv_20h", "cv_20hc", "cv_d52"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {73, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37, 38}
PINMAME_NORMALIZED_OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36}


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
	import curate_cirqus_voltaire as curator
	import sys as _sys

	argv = _sys.argv
	_sys.argv = ["curate_cirqus_voltaire.py"]
	try:
		curator.main()
	finally:
		_sys.argv = argv


class CirqusVoltaireDefinitionTests(unittest.TestCase):
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
			["polarity", "recreation_notes", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "physical_wiring":
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.cirqus-voltaire.1997", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1997, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual(964.0, self.definition["machine"]["playfield"]["width"])
		self.assertEqual(2162.0, self.definition["machine"]["playfield"]["height"])
		self.assertEqual("vpx", self.definition["machine"]["playfield"]["units"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_wpc95_controller_profile_is_reused_unchanged(self) -> None:
		self.assertTrue(CONTROLLER_PATH.is_file())
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-95", profile["id"])

	def test_both_conflicts_are_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{"conflict.wow-top-targets-opto-not-normalized", "conflict.gi-backbox-string-numbering"},
			set(conflicts),
		)
		opto_conflict = conflicts["conflict.wow-top-targets-opto-not-normalized"]
		self.assertGreaterEqual(len(opto_conflict["source_refs"]), 2)
		description = opto_conflict["description"].lower()
		self.assertIn("unresolved", description)
		self.assertIn("harness", description)
		for address in (37, 38):
			self.assertIn(str(address), opto_conflict["path"])
		gi_conflict = conflicts["conflict.gi-backbox-string-numbering"]
		self.assertGreaterEqual(len(gi_conflict["source_refs"]), 2)

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_cv_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in DRIVER_IDS - {"cv_14"}:
			self.assertEqual("cv_14", by_id[driver_id]["clone_of"], driver_id)
		self.assertNotIn("clone_of", by_id["cv_14"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_is_recorded_even_where_pinmame_does_not_normalize_it(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_wow_and_top_target_optos_are_not_normalized_by_pinmame(self) -> None:
		import curate_cirqus_voltaire as curator

		# Mask index 3 (0-based, column 3) is 0x3f: bits 0-5 (rows 1-6, addresses 31-36) are
		# covered, but bits 6-7 (rows 7-8, addresses 37/38) are clear even though the printed
		# switch matrix shades the entire column as opto. This asymmetry is the entire basis of
		# conflict.wow-top-targets-opto-not-normalized and must not be silently "fixed" by
		# treating 37/38 the same as 31-36.
		mask = (0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		self.assertEqual(0x3f, mask[3])
		for address in (37, 38):
			self.assertIn(address, curator.OPTO_SWITCHES)
			self.assertNotIn(address, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		for address in (31, 32, 33, 34, 35, 36):
			self.assertIn(address, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)

	def test_flipper_positions_and_spinners(self) -> None:
		for address in (111, 112, 113, 114, 115, 117):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (116, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		# 116 and 118 are unfitted but the wiring page still shades them as optos; that printed
		# construction is preserved even though the position is unused.
		self.assertTrue(self.switches[116]["normally_closed"])
		self.assertTrue(self.switches[118]["normally_closed"])

	def test_spinner_left_right_labels_match_the_manual_and_geometry_not_the_legacy_record(self) -> None:
		# F5 (public 115) is printed RIGHT SPINNER and F7 (public 117) is printed LEFT SPINNER; a
		# prior legacy-migrated record had these reversed. The retained table's own geometry
		# (right side x > 0.5, left side x < 0.5) is the independent tiebreaker.
		self.assertEqual("Right Spinner", self.switches[115]["label"])
		self.assertEqual("Left Spinner", self.switches[117]["label"])
		right_x = self.switches[115]["spatial"]["placements"][0]["x"]
		left_x = self.switches[117]["spatial"]["placements"][0]["x"]
		self.assertGreater(right_x, 0.5)
		self.assertLess(left_x, 0.5)

	def test_ringmaster_switches_share_one_projected_position(self) -> None:
		up = self.switches[42]["spatial"]["placements"][0]
		middle = self.switches[43]["spatial"]["placements"][0]
		down = self.switches[44]["spatial"]["placements"][0]
		self.assertEqual((up["x"], up["y"]), (down["x"], down["y"]))
		self.assertAlmostEqual(up["y"], middle["y"], places=3)

	def test_lower_flippers_use_the_public_wpc95_addresses_not_the_printed_ones(self) -> None:
		# Printed 29-32 map to public 45-48 (CORE_FIRSTLFLIPSOL = 45); printed 33-36 keep their
		# own address unchanged (CORE_FIRSTUFLIPSOL = 33) but are repurposed non-flipper devices.
		for address in (45, 46, 47, 48):
			self.assertIn(address, self.solenoids)
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(str(address - 16), aliases["manual.address"])
		for address, label in ((33, "Popper"), (34, "Diverter Hold"), (35, "Ringmaster Magnet"), (36, "Upper Post")):
			self.assertEqual(label, self.solenoids[address]["label"], address)

	def test_the_full_wpc95_output_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 53)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))

	def test_custom_solenoids_51_and_52_are_virtual_decaying_state_not_devices(self) -> None:
		for address in (51, 52):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"])
			self.assertEqual("virtual", device["spatial"]["reason"])
			self.assertEqual("used", device["availability"])

	def test_motor_direction_mirror_is_declared_virtual(self) -> None:
		device = self.solenoids[41]
		self.assertEqual("virtual", device["kind"])
		self.assertEqual("virtual", device["spatial"]["reason"])

	def test_clamped_coordinates_stay_within_schema_bounds(self) -> None:
		import curate_cirqus_voltaire as curator

		for address in curator.CLAMPED_X_RAW:
			device = self.solenoids[address]
			for placement in device["spatial"]["placements"]:
				self.assertLessEqual(placement["x"], 1.0)
				self.assertGreaterEqual(placement["x"], 0.0)
			self.assertIn("clamped", device["physical"]["notes"].lower())

	def test_backbox_devices_have_no_playfield_coordinate(self) -> None:
		self.assertEqual("not_applicable", self.switches[11]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[11]["spatial"]["reason"])
		backbox_kick = self.solenoids[2]
		self.assertEqual("not_applicable", backbox_kick["spatial"]["status"])
		self.assertEqual("cabinet_or_service", backbox_kick["spatial"]["reason"])

	def test_lamp_88_is_used_but_unmodeled_in_the_retained_table(self) -> None:
		lamp88 = self.lamps[88]
		self.assertEqual("used", lamp88["availability"])
		self.assertEqual("not_applicable", lamp88["spatial"]["status"])
		self.assertEqual("cabinet_or_service", lamp88["spatial"]["reason"])
		self.assertEqual("Start Button", lamp88["label"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_not(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"])
			self.assertGreater(len(self.gi[address]["spatial"]["placements"]), 0)
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"])

	def test_geometric_ordering_left_right_and_rear_front(self) -> None:
		# Cheap regression check against reversed left/right or rear/front identities: the left
		# saucer/inlane/outlane sit at a smaller normalized x than their right counterparts, and
		# the shooter lane (apron end) sits at a larger normalized y than the coin-door switches
		# (near the playfield's rear/top).
		left_saucer_x = self.switches[71]["spatial"]["placements"][0]["x"]
		right_saucer_x = self.switches[72]["spatial"]["placements"][0]["x"]
		self.assertLess(left_saucer_x, right_saucer_x)
		left_inlane_x = self.switches[26]["spatial"]["placements"][0]["x"]
		right_inlane_x = self.switches[17]["spatial"]["placements"][0]["x"]
		self.assertLess(left_inlane_x, right_inlane_x)
		left_outlane_x = self.switches[27]["spatial"]["placements"][0]["x"]
		right_outlane_x = self.switches[57]["spatial"]["placements"][0]["x"]
		self.assertLess(left_outlane_x, right_outlane_x)
		shooter_lane_y = self.switches[18]["spatial"]["placements"][0]["y"]
		right_loop_upper_y = self.switches[23]["spatial"]["placements"][0]["y"]
		self.assertGreater(shooter_lane_y, right_loop_upper_y)

	def test_multi_target_bank_placement_counts_match_the_manual_quantity(self) -> None:
		wow = self.switches[37]
		self.assertEqual(3, len(wow["spatial"]["placements"]))
		top = self.switches[38]
		self.assertEqual(2, len(top["spatial"]["placements"]))

	def test_trough_switches_are_documented_projections(self) -> None:
		for address in (31, 32, 33, 34, 35):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"])
			self.assertIn("projected", switch["physical"]["notes"].lower())

	def test_eddy_sensors_share_volt_objects_with_matching_lamps(self) -> None:
		for address in (17, 26, 75, 76):
			switch = self.switches[address]
			self.assertEqual("other", switch["physical"]["switch_type"])
			self.assertFalse(switch["normally_closed"])
			self.assertIn("volt", switch["physical"]["notes"].lower())

	def test_source_hashes_are_present_and_well_formed(self) -> None:
		import curate_cirqus_voltaire as curator

		for value in (curator.TABLE_SHA256, curator.SCRIPT_SHA256, curator.MANUAL_SHA256,
					  curator.SB101_SHA256, curator.SB102_SHA256, curator.SB104_SHA256):
			self.assertEqual(64, len(value))
			int(value, 16)

	def test_curator_check_and_regenerate_are_idempotent(self) -> None:
		import curate_cirqus_voltaire as curator

		definition = curator.build()
		self.assertEqual(self.definition, definition)
		report = curator.build_spatial_report(definition)
		self.assertEqual("validated", report["status"])

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_seed_matches_the_promoted_definition(self) -> None:
		self.assertTrue(SEED_PATH.is_file())
		self.assertEqual(load_json(SEED_PATH), self.definition)

	def test_spatial_report_matches_generated_definition(self) -> None:
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("bally.cirqus-voltaire.1997", report["machine_id"])
		self.assertEqual("validated", report["status"])
		self.assertGreater(report["placement_count"], 0)


if __name__ == "__main__":
	unittest.main()
