from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "theatre-of-magic-1995.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "theatre-of-magic-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "theatre-of-magic-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "theatre-of-magic-1995.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-security.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "theatre-of-magic-1995.json"

DRIVER_IDS = {
	"tom_13", "tom_06", "tom_061", "tom_10f", "tom_101f", "tom_12", "tom_12a",
	"tom_121", "tom_13c", "tom_13f", "tom_14h", "tom_14hb",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 16, 17, 18, 46, 68, 72, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 55, 56, 57, 58}
EDDY_ADDRESSES = {45, 48, 85}
PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2594.1


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
	import curate_theatre_of_magic as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_theatre_of_magic.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class TheatreOfMagicDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["unresolved_conflicts", "spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"physical_wiring", "spatial_placement"}:
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.theatre-of-magic.1995", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2358, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1995, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertEqual("0x20", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_playfield_uses_the_tall_bounds_not_the_common_2162_divisor(self) -> None:
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual(PLAYFIELD_WIDTH, playfield["width"])
		self.assertEqual(PLAYFIELD_HEIGHT, playfield["height"])
		self.assertEqual("vpx", playfield["units"])
		self.assertNotEqual(2162.0, playfield["height"], "must not silently reuse the common WPC bottom bound")

	def test_gi_backbox_playfield_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.gi-strings-1-2-backbox-vs-script-playfield-binding"}, set(conflicts))
		conflict = conflicts["conflict.gi-strings-1-2-backbox-vs-script-playfield-binding"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("backbox", description)
		self.assertIn("playfield", description)

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_tom_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["tom_13"])
		for driver_id in DRIVER_IDS - {"tom_13"}:
			self.assertEqual("tom_13", by_id[driver_id]["clone_of"], driver_id)
		# Hazard: the retained script binds tom_14hb, which is a driver variant, not the
		# machine's production firmware.
		self.assertIn("tom_14hb", by_id)
		self.assertIn("Home version", by_id["tom_14h"]["variant_notes"])
		self.assertIn("Home version", by_id["tom_14hb"]["variant_notes"])

	def test_the_full_wpc_security_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_opto_polarity_matches_pinmame_normalization_with_zero_disagreement(self) -> None:
		import curate_theatre_of_magic as curator

		self.assertEqual(curator.OPTO_SWITCHES, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
			if address in EDDY_ADDRESSES:
				self.assertEqual("other", switch["physical"]["switch_type"], address)
				self.assertIn("eddy", switch["physical"]["notes"].lower())
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_cube_position_optos_project_onto_the_trunk(self) -> None:
		for address in (55, 56, 57, 58):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"], address)
			placement = switch["spatial"]["placements"][0]
			self.assertAlmostEqual(0.335084, placement["x"], places=6)
			self.assertAlmostEqual(0.357928, placement["y"], places=6)

	def test_fliptronic_block_has_no_upper_flippers(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertFalse(self.switches[111]["roles"][0].endswith(".button"))
		self.assertTrue(self.switches[112]["roles"][0].endswith(".button"))
		# The switch-matrix wiring page mislabels 115-118 as real upper-flipper hardware; the
		# parts list (Not Used, blank part number) is authoritative and disclosed in notes.
		self.assertIn("stale", self.switches[115]["physical"]["notes"].lower())

	def test_the_full_wpc_security_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in (17, 18):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (20, 24, 25, 26, 27, 28):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_repurposed_upper_flipper_circuits_33_to_36(self) -> None:
		self.assertEqual("Cube Magnet", self.solenoids[33]["label"])
		self.assertEqual("used", self.solenoids[33]["availability"])
		self.assertEqual("Sub Ball Release", self.solenoids[34]["label"])
		self.assertEqual("used", self.solenoids[34]["availability"])
		self.assertEqual("Left Drain Magnet", self.solenoids[35]["label"])
		self.assertEqual("used", self.solenoids[35]["availability"])
		self.assertEqual("unused", self.solenoids[36]["availability"])
		for address in (33, 34, 35, 36):
			self.assertIn("repurposed", self.solenoids[address]["physical"]["notes"].lower())

	def test_prototype_and_optional_solenoids_are_unused_but_documented(self) -> None:
		for address in (19, 22, 23, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)
		self.assertIn("prototype", self.solenoids[19]["physical"]["notes"].lower())
		self.assertIn("tigersaw", self.solenoids[19]["physical"]["notes"].lower().replace(" ", ""))
		self.assertIn("centerpost", self.solenoids[23]["physical"]["notes"].lower().replace(" ", ""))
		self.assertIn("centerpost", self.solenoids[36]["physical"]["notes"].lower().replace(" ", ""))

	def test_knocker_is_fitted_and_cabinet_scoped(self) -> None:
		knocker = self.solenoids[7]
		self.assertEqual("Knocker", knocker["label"])
		self.assertEqual("used", knocker["availability"])
		self.assertEqual("not_applicable", knocker["spatial"]["status"])
		self.assertEqual("cabinet_or_service", knocker["spatial"]["reason"])

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
		self.assertEqual("Lower Left Flipper Power", self.solenoids[47]["label"])

	def test_gi_backbox_strings_are_not_applicable_and_playfield_strings_are_located(self) -> None:
		for address in (0, 1):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
		for address in (2, 3):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(15, len(self.gi[2]["spatial"]["placements"]))
		self.assertEqual(10, len(self.gi[3]["spatial"]["placements"]))
		self.assertNotIn("spatial", self.gi[4])

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		for address in (26, 45, 54, 63, 81):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in sorted(MATRIX_ADDRESSES - {26, 45, 54, 63, 81, 82, 83, 84, 87, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (82, 83, 84):
			self.assertEqual("unused", self.lamps[address]["availability"], address)
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"], address)
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)

	def test_lamp_85_projects_onto_the_trunk(self) -> None:
		placement = self.lamps[85]["spatial"]["placements"][0]
		self.assertAlmostEqual(0.335084, placement["x"], places=6)
		self.assertAlmostEqual(0.357928, placement["y"], places=6)

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
		self.assertEqual("partial", report["status"])
		self.assertEqual(located, report["placement_count"])

	def test_front_devices_land_near_y_1_and_top_lanes_near_y_0(self) -> None:
		# Sanity check for the tall-playfield normalization hazard: using the common 2162
		# bottom bound here would compress every y coordinate by about 20%.
		outhole_area = self.switches[32]["spatial"]["placements"][0]["y"]
		self.assertGreater(outhole_area, 0.85)
		flipper = self.solenoids[45]["spatial"]["placements"][0]["y"]
		self.assertGreater(flipper, 0.8)
		top_lane = self.switches[66]["spatial"]["placements"][0]["y"]
		self.assertLess(top_lane, 0.3)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: dev["spatial"]["placements"][0]["x"] for addr, dev in self.switches.items() if dev["spatial"]["status"] != "not_applicable"}
		switch_y = {addr: dev["spatial"]["placements"][0]["y"] for addr, dev in self.switches.items() if dev["spatial"]["status"] != "not_applicable"}
		lamp_x = {addr: dev["spatial"]["placements"][0]["x"] for addr, dev in self.lamps.items() if dev["spatial"]["status"] != "not_applicable"}
		lamp_y = {addr: dev["spatial"]["placements"][0]["y"] for addr, dev in self.lamps.items() if dev["spatial"]["status"] != "not_applicable"}
		# Left flipper is left of right flipper.
		self.assertLess(self.solenoids[47]["spatial"]["placements"][0]["x"], self.solenoids[45]["spatial"]["placements"][0]["x"])
		# Left/right outlanes are outboard of their return lanes.
		self.assertLess(switch_x[25], switch_x[26])
		self.assertGreater(switch_x[28], switch_x[27])
		# Top lane 1 is left of Top lane 2, for both switches and lamps.
		self.assertLess(switch_x[66], switch_x[67])
		self.assertLess(lamp_x[37], lamp_x[38])
		# Jet bumpers ascend top -> middle -> bottom in y.
		self.assertLess(switch_y[65], switch_y[64])
		self.assertLess(switch_y[64], switch_y[63])
		# Trough balls 1-4 ascend toward the drain (increasing y as the address rises).
		self.assertLess(switch_y[32], switch_y[33])
		self.assertLess(switch_y[33], switch_y[34])
		self.assertLess(switch_y[34], switch_y[35])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.trunk",
				"mechanism.subway-lock", "mechanism.vanish-lock", "mechanism.captive-ball",
				"mechanism.magnetic-outlanes", "mechanism.diverters-and-gates", "mechanism.knocker",
				"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.lower-flippers",
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
		self.assertIn("TrunkAngle", mechanisms["mechanism.trunk"]["behavior"])

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
		self.assertIn("vpx-script.tom-2-4", sources)
		self.assertTrue(sources["vpx-script.tom-2-4"]["known_working"])
		self.assertEqual(
			"596c926f27c1782819a0184566f083a161be362fec7a3bbc634a9138d97b47c3",
			sources["vpx-script.tom-2-4"]["sha256"],
		)
		self.assertEqual(
			"5f8bb3e0493c408484e475516e2f2c3d84b3487dcfb63eb231bca2c40b531253",
			sources["vpx-table.tom-2-4"]["sha256"],
		)
		self.assertNotIn("runtime.theatre-of-magic", sources)
		self.assertNotIn("rom.tom", sources)
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
		self.assertEqual("pinmame.wpc-security", profile["id"])
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


class TheatreOfMagicCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_theatre_of_magic as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_theatre_of_magic as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_theatre_of_magic as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Theatre of Magic", b"Theatre of Tragic", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_theatre_of_magic as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class TheatreOfMagicRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_theatre_of_magic as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_theatre_of_magic as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "bally/theatre-of-magic-1995/source/Theatre of Magic (Bally 1995) 2.4.vpx"
		script = source_root / "bally/theatre-of-magic-1995/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_and_geometry_dump_match_their_pinned_hashes(self) -> None:
		import curate_theatre_of_magic as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "theatre-of-magic-1995" / "manual-transcription.md"
		geometry = Path(root) / "theatre-of-magic-1995" / "vpx-geometry.txt"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))
		self.assertEqual(curator.VPX_GEOMETRY_SHA256, curator._file_sha256(geometry))


if __name__ == "__main__":
	unittest.main()
