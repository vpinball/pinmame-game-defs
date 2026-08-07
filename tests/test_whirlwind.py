from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "whirlwind-1990.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "whirlwind-1990.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "whirlwind-1990.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "whirlwind-1990.json"

DRIVER_IDS = {"whirl_l3", "whirl_l2", "whirl_g1", "whirl_g2", "whirl_g3"}
MATRIX_ADDRESSES = set(range(1, 65))
UNUSED_MATRIX_ADDRESSES = {9, 14, 31, 32, 46, 62, 63, 64}
OPTO_ADDRESSES = {26, 27, 28, 29, 57, 58}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _run_curator_without_mode() -> None:
	import curate_whirlwind as curator

	argv = sys.argv
	sys.argv = ["curate_whirlwind.py"]
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


class WhirlwindDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_partial_identity_and_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.whirlwind.1990", machine["id"])
		self.assertEqual("Williams", machine["manufacturer"])
		self.assertEqual(1990, machine["year"])
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual({"polarity", "spatial_placement", "unresolved_conflicts"}, set(coverage["missing"]))
		self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("validated", coverage["dimensions"]["physical_wiring"])

	def test_controller_is_system_11_not_wpc(self) -> None:
		controller = self.definition["controller"]
		self.assertEqual("pinmame.system-11", controller["platform"])
		self.assertEqual("0x100", controller["hardware_generation"])
		self.assertTrue(controller["inversion_applied_by_emulator"])

	def test_every_whirl_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		drivers = self.definition["drivers"]
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in drivers})
		for driver in drivers:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip())
		parent = next(driver for driver in drivers if driver["id"] == "whirl_l3")
		self.assertNotIn("clone_of", parent)
		for driver in drivers:
			if driver["id"] != "whirl_l3":
				self.assertEqual("whirl_l3", driver["clone_of"])

	def test_the_full_system_11_switch_matrix_is_enumerated_column_major(self) -> None:
		matrix_only = {address for address in self.switches if address > 0}
		self.assertEqual(MATRIX_ADDRESSES, matrix_only)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"])
		used = MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {5}
		for address in used:
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("optional", self.switches[5]["availability"])
		diagnostic_addresses = {device["binding"]["device"] for device in self.definition["inputs"] if device["binding"]["group"] == "pinmame.input.switch" and device["binding"]["device"] < 0}
		self.assertEqual({-7, -6, -5, -4}, diagnostic_addresses)
		self.assertEqual(1, len(self.dips))
		self.assertIn(0, self.dips)

	def test_switch_address_formula_is_sequential_column_major(self) -> None:
		# address = (column-1)*8+row; column boundaries 1,9,17,...,57 must all start a new column.
		for column in range(8):
			first = column * 8 + 1
			last = column * 8 + 8
			for address in range(first, last + 1):
				self.assertIn(address, self.switches)

	def test_opto_switches_are_flagged_but_polarity_is_left_unconfirmed(self) -> None:
		for address in OPTO_ADDRESSES:
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
			self.assertNotIn("normally_closed", self.switches[address], address)
		self.assertEqual("validated", self.switches[26]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[57]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", self.switches[58]["spatial"]["reason"])

	def test_flipper_buttons_have_no_matrix_address_but_lane_change_optos_do(self) -> None:
		for switch in self.switches.values():
			self.assertNotIn("Flipper Button", switch["label"])
		self.assertIn("Lane Change", self.switches[57]["label"])
		self.assertIn("Lane Change", self.switches[58]["label"])

	def test_mux_relay_feedback_switch_two_is_not_ball_tilt(self) -> None:
		switch_two = self.switches[2]
		self.assertIn("A/C Relay", switch_two["label"])
		self.assertEqual("internal_nonvisual", switch_two["spatial"]["reason"])

	def test_trough_switches_are_projected_not_invented(self) -> None:
		for address in (10, 11, 12, 13):
			spatial = self.switches[address]["spatial"]
			self.assertEqual("validated", spatial["status"])
			self.assertIn("Projected", self.switches[address]["physical"]["notes"])

	def test_the_full_solenoid_address_space_1_to_50_is_enumerated_with_no_gaps(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(set(), set(self.solenoids) & set(range(51, 65)))

	def test_ac_mux_c_side_addresses_share_the_a_side_driver_transistor(self) -> None:
		for a_address in range(1, 9):
			c_address = a_address + 24
			a_driver = self.solenoids[a_address]["wiring"]["driver_transistor"]
			c_driver = self.solenoids[c_address]["wiring"]["driver_transistor"]
			self.assertEqual(a_driver, c_driver, f"{a_address}/{c_address}")

	def test_gi_addresses_are_solenoid_bound_not_a_separate_gi_group(self) -> None:
		gi_devices = [device for device in self.definition["outputs"] if device["kind"] == "gi"]
		self.assertEqual({11, 16}, {device["binding"]["device"] for device in gi_devices})
		for device in gi_devices:
			self.assertEqual("pinmame.output.solenoid", device["binding"]["group"])
		gi_11 = self.solenoids[11]
		self.assertNotIn("spatial", gi_11)
		gi_16 = self.solenoids[16]
		self.assertEqual("validated", gi_16["spatial"]["status"])

	def test_synthetic_flipper_solenoids_are_virtual_with_no_physical_device(self) -> None:
		for address in (45, 46, 47, 48):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"])
			self.assertEqual("not_applicable", solenoid["spatial"]["status"])
			self.assertEqual("virtual", solenoid["spatial"]["reason"])

	def test_sound_overlay_board_offset_is_manual_item_plus_14(self) -> None:
		for address, manual_item in {37: 23, 38: 24, 39: 25, 40: 26, 41: 27}.items():
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(str(manual_item), aliases["manual.address"])

	def test_fan_and_wheels_motor_are_confirmed_by_script_callback(self) -> None:
		fan = self.solenoids[38]
		self.assertEqual("motor", fan["kind"])
		self.assertEqual("not_applicable", fan["spatial"]["status"])
		self.assertEqual("cabinet_or_service", fan["spatial"]["reason"])
		motor = self.solenoids[41]
		self.assertEqual("motor", motor["kind"])
		self.assertEqual("validated", motor["spatial"]["status"])

	def test_backglass_only_flashers_have_no_spatial_key_and_are_conflicted(self) -> None:
		from curate_whirlwind import SOLENOID_BACKGLASS_ONLY

		for address in SOLENOID_BACKGLASS_ONLY:
			self.assertNotIn("spatial", self.solenoids[address], address)
		conflicts = {item["id"]: item for item in self.definition["conflicts"]}
		self.assertIn("conflict.flasher-backglass-vs-playfield-mounting", conflicts)
		for address in SOLENOID_BACKGLASS_ONLY:
			self.assertIn(str(address), conflicts["conflict.flasher-backglass-vs-playfield-mounting"]["path"])

	def test_jet_bumper_21_duplicate_label_is_resolved_and_disclosed(self) -> None:
		solenoid_21 = self.solenoids[21]
		self.assertIn("Top Lower Jet Bumper", solenoid_21["physical"]["notes"])
		self.assertIn("proofing duplication", solenoid_21["physical"]["notes"])

	def test_special_solenoids_resolve_to_sequential_public_addresses(self) -> None:
		for address in range(17, 23):
			self.assertIn(address, self.solenoids)
			self.assertEqual("used", self.solenoids[address]["availability"])

	def test_the_full_lamp_matrix_is_enumerated(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address in range(2, 9):
			backglass = self.lamps[address]
			self.assertEqual("not_applicable", backglass["spatial"]["status"])
			self.assertEqual("cabinet_or_service", backglass["spatial"]["reason"])
		self.assertEqual("validated", self.lamps[1]["spatial"]["status"])

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

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		lamp_pos = _positions(self.lamps)
		# Ball lock: lower (22) sits nearer the player (larger y) than upper (24).
		self.assertGreater(switch_pos[22][1], switch_pos[24][1])
		self.assertGreater(switch_pos[23][1], switch_pos[24][1])
		# Left/right slingshots keep left-of-right ordering.
		self.assertLess(switch_pos[55][0], switch_pos[56][0])
		# Upper jet bumper cluster: left (49) left of right (50).
		self.assertLess(switch_pos[49][0], switch_pos[50][0])
		# Lower jet bumper cluster: left (52) left of right (53).
		self.assertLess(switch_pos[52][0], switch_pos[53][0])
		# The three spinning-disc lamps/objects: left disc left of right disc.
		self.assertLess(lamp_pos[36][0], lamp_pos[37][0])
		# Outlanes are outboard of return lanes on both sides.
		self.assertLess(switch_pos[17][0], switch_pos[18][0])
		self.assertGreater(switch_pos[16][0], switch_pos[15][0])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.spinning-discs", "mechanism.knocker", "mechanism.fan", "mechanism.trough", "mechanism.cellar",
				"mechanism.ball-lock", "mechanism.top-saucer", "mechanism.right-ramp",
				"mechanism.drop-targets", "mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.flippers",
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

	def test_display_inventory_is_the_alphanumeric_segment_display(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("segment", displays[0]["kind"])
		self.assertEqual(16, displays[0]["width"])
		self.assertEqual(2, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.whirlwind-1990", sources)
		self.assertTrue(sources["vpx-script.whirlwind-1990"]["known_working"])
		self.assertEqual("e478206db1045fa9e0f82668a4b78d00678b323c151245df02f9e14d096cf8d2", sources["vpx-script.whirlwind-1990"]["sha256"])
		self.assertEqual("105477078e68547c24167fc9ba99baeff24ec48ce16c46ec2530184a67f92e23", sources["vpx-table.whirlwind-1990"]["sha256"])
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

	def test_manual_source_declares_every_excerpt(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["id"] == "manual.williams.whirlwind.1990")
		excerpt_ids = {excerpt["id"] for excerpt in manual["excerpts"]}
		self.assertEqual(
			{
				"excerpt.whirlwind.switch-locations", "excerpt.whirlwind.switch-matrix",
				"excerpt.whirlwind.lamp-matrix", "excerpt.whirlwind.lamp-locations",
				"excerpt.whirlwind.solenoid-flasher-locations", "excerpt.whirlwind.solenoid-flasher-wiring",
				"excerpt.whirlwind.general-illumination", "excerpt.whirlwind.boards-and-assemblies",
			},
			excerpt_ids,
		)
		for excerpt in manual["excerpts"]:
			self.assertTrue(excerpt["reviewed"])
			self.assertEqual("manual", excerpt["method"])

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
		self.assertEqual("knowledge/williams/whirlwind-1990.md", self.definition["knowledge"]["path"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertGreater(KNOWLEDGE_PATH.stat().st_size, 0)


class WhirlwindCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_whirlwind as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_whirlwind as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_whirlwind as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Whirlwind", b"Whirlwund", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_whirlwind as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class WhirlwindRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_whirlwind as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_whirlwind as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/whirlwind-1990/source/Whirlwind (Williams 1990).vpx"
		script = source_root / "williams/whirlwind-1990/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_whirlwind as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "whirlwind" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
