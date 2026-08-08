from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "capcom" / "big-bang-bar-1996.json"
SEED_PATH = ROOT / "tools" / "seeds" / "capcom" / "big-bang-bar-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "capcom" / "big-bang-bar-1996.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "capcom.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "capcom" / "big-bang-bar-1996.json"

DRIVER_IDS = {"bbb108", "bbb109"}


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
	import curate_big_bang_bar as curator

	argv = sys.argv
	sys.argv = ["curate_big_bang_bar.py"]
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


class BigBangBarDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			["polarity", "output_semantics", "mechanism_behavior", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("capcom.big-bang-bar.1996", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual("Capcom", self.definition["machine"]["manufacturer"])
		self.assertEqual(1996, self.definition["machine"]["year"])
		self.assertEqual("pinmame.capcom", self.definition["controller"]["platform"])
		self.assertEqual("0x0", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["recreation_knowledge"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_no_hardware_generation_bit_exists_for_capcom(self) -> None:
		# Distinct from every WPC/System-11/Whitestar/SAM game curated so far: capcom.c's own
		# core_tGameData literal is {0, disp, ...} -- gen is the literal zero, not a bitmask.
		self.assertEqual("0x0", self.definition["controller"]["hardware_generation"])

	def test_every_bbb_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		bbb109 = next(driver for driver in self.definition["drivers"] if driver["id"] == "bbb109")
		bbb108 = next(driver for driver in self.definition["drivers"] if driver["id"] == "bbb108")
		self.assertNotIn("clone_of", bbb109)
		self.assertEqual("bbb109", bbb108["clone_of"])

	def test_cabinet_and_matrix_switch_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 17)) | set(range(17, 81)) | {81, 89}, set(self.switches))
		# Cabinet dedicated switches (1-16) are all cabinet/service spatially.
		for address in range(1, 17):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"], address)
		# 11-14 genuinely unfitted per the manual; 15/16 are this game's Token/Ticket dispense.
		for address in (11, 12, 13, 14):
			self.assertEqual("unused", self.switches[address]["availability"], address)
		for address in (15, 16):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("Tilt Bob", self.switches[10]["label"])
		self.assertEqual("Left Flipper Button", self.switches[5]["label"])

	def test_pinmame_normalized_opto_switches_match_capinvsw10_with_zero_disagreement(self) -> None:
		# capInvSw10 = {0, 0x00, 0x01, 0x78, 0x00, 0x00, 0x01} (src/wpc/capgames.c), re-derived
		# in code rather than by hand: col2 bit0->25, col3 bits3-6->36/37/38/39, col6 bit0->57.
		mask = [0, 0x00, 0x01, 0x78, 0x00, 0x00, 0x01]
		normalized: set[int] = set()
		for column, byte in enumerate(mask):
			for bit in range(8):
				if byte & (1 << bit):
					normalized.add(9 + bit + column * 8)
		self.assertEqual({25, 36, 37, 38, 39, 57}, normalized)
		for address in normalized:
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)

	def test_trough_optos_carry_confirmed_part_numbers(self) -> None:
		for address in (36, 37, 38, 39):
			physical = self.switches[address]["physical"]
			self.assertIn("A0015604-4R", physical["notes"])
			self.assertIn("A0015702-4R", physical["notes"])

	def test_synthetic_flipper_column_and_platform_gap_are_virtual(self) -> None:
		self.assertEqual("virtual", self.switches[81]["kind"])
		self.assertEqual("not_applicable", self.switches[81]["spatial"]["status"])
		self.assertEqual("virtual", self.switches[81]["spatial"]["reason"])
		self.assertEqual("virtual", self.switches[89]["kind"])

	def test_solenoid_space_is_enumerated_with_honest_kinds(self) -> None:
		expected = set(range(1, 33)) | {33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51}
		self.assertEqual(expected, set(self.solenoids))
		for address in range(21, 27):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (30, 31, 32):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in range(1, 21):
			if address in (21, 22, 23, 24, 25, 26):
				continue
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
		self.assertEqual("Left Flipper", self.solenoids[9]["label"])
		self.assertEqual("Right Flipper", self.solenoids[10]["label"])
		self.assertEqual("Upper Right Flipper", self.solenoids[11]["label"])

	def test_flipper_mirror_addresses_bind_to_physical_correspondence(self) -> None:
		# Address 45 (sLRFlipPow) mirrors physical 9 (Left Flipper); 47 (sLLFlipPow) mirrors
		# physical 10 (Right Flipper) -- the opposite left/right sense from PinMAME's own
		# constant names, per capcom.c's own admitted mirror-naming defect.
		self.assertIn("Left Flipper", self.solenoids[45]["label"])
		self.assertIn("Right Flipper", self.solenoids[47]["label"])
		self.assertEqual("used", self.solenoids[45]["availability"])
		self.assertEqual("used", self.solenoids[47]["availability"])
		for address in (34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_solenoid_35_is_documented_as_an_eject_hole_mirror_not_a_flipper(self) -> None:
		device = self.solenoids[35]
		self.assertEqual("virtual", device["kind"])
		self.assertIn("Eject Hole", device["label"])
		self.assertIn("conflict.solenoid-35-eject-hole-mirror-mislabeled", device["physical"]["notes"])

	def test_fast_flips_solenoid_51_is_diagnostic_only(self) -> None:
		device = self.solenoids[51]
		self.assertEqual("virtual", device["kind"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("virtual", device["spatial"]["reason"])

	def test_no_gi_output_group_exists_for_capcom(self) -> None:
		groups = {device["binding"]["group"] for device in self.definition["outputs"]}
		self.assertNotIn("pinmame.output.gi", groups)
		for device in self.definition["outputs"]:
			self.assertNotEqual("gi", device["kind"], device["id"])

	def test_lamp_matrix_is_fully_enumerated_across_both_banks(self) -> None:
		self.assertEqual(set(range(1, 129)) | {129, 130} | set(range(131, 137)), set(self.lamps))
		unused = {address for address, device in self.lamps.items() if device["availability"] == "unused" and address <= 128}
		self.assertEqual(18, len(unused))
		used = {address for address in range(1, 129) if address not in unused}
		self.assertEqual(110, len(used))

	def test_lamps_missing_retained_geometry_omit_spatial_rather_than_invent_it(self) -> None:
		for address in (3, 38, 125):
			self.assertNotIn("spatial", self.lamps[address])
			self.assertEqual("used", self.lamps[address]["availability"])

	def test_out_of_bounds_lamps_are_excluded_from_validated_placement(self) -> None:
		for address in (2, 62):
			self.assertNotIn("spatial", self.lamps[address])

	def test_diagnostic_lamp_column_is_cabinet_hardware(self) -> None:
		for address in (129, 130):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])
		for address in range(131, 137):
			self.assertEqual("unused", self.lamps[address]["availability"], address)

	def test_ramp_diverter_solenoids_have_no_promoted_placement(self) -> None:
		for address in (14, 15):
			self.assertNotIn("spatial", self.solenoids[address])

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
		self.assertEqual("validated", report["status"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		# Left flipper sits left of right flipper.
		self.assertLess(switch_pos[33][0], switch_pos[34][0])
		# 4-Bank targets 17-20 are laid out in ascending y (nearer the rear as index rises).
		self.assertLess(switch_pos[20][1], switch_pos[19][1])
		self.assertLess(switch_pos[19][1], switch_pos[18][1])
		self.assertLess(switch_pos[18][1], switch_pos[17][1])
		# Trough balls 1-4 (36-39): 36 is nearest the SolRelease exit point (kicked out to the
		# shooter lane), 39 is nearest the Outhole/drain entry (largest y, closest to the apron).
		self.assertLess(switch_pos[36][1], switch_pos[37][1])
		self.assertLess(switch_pos[37][1], switch_pos[38][1])
		self.assertLess(switch_pos[38][1], switch_pos[39][1])
		self.assertLess(switch_pos[39][1], switch_pos[35][1])
		# Left slingshot sits left of right slingshot.
		self.assertLess(switch_pos[41][0], switch_pos[42][0])

	def test_mechanism_inventory_covers_every_used_coil_or_motor_with_a_geometry_home(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.4-bank-drop-targets", "mechanism.3-bank-drop-targets",
				"mechanism.1-bank-drop-target", "mechanism.alien-mechanism", "mechanism.tube-dancer",
				"mechanism.orbit-gates", "mechanism.island-and-ramp-diverters",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-release-to-shooter-lane"}, set(relationships))
		self.assertEqual("switch.matrix-43", relationships["relationship.trough-release-to-shooter-lane"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-release-to-shooter-lane"]["kind"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_four_conflicts_are_recorded_with_multiple_source_refs(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{
				"conflict.flipper-mirror-address-left-right-naming",
				"conflict.solenoid-35-eject-hole-mirror-mislabeled",
				"conflict.solenoid-22-shared-device-construction",
				"conflict.ramp-diverter-geometry-inconsistent",
			},
			set(conflicts),
		)
		for conflict in conflicts.values():
			self.assertGreaterEqual(len(conflict["source_refs"]), 2, conflict["id"])
			self.assertTrue(conflict["description"].strip(), conflict["id"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.bbb-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.bbb-vpw-1-0"]["known_working"])
		self.assertEqual(
			"db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7",
			sources["vpx-script.bbb-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5",
			sources["vpx-table.bbb-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5",
			sources["manual.capcom.big-bang-bar.1996"]["sha256"],
		)
		self.assertEqual(
			"fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603",
			sources["manual-schematic.capcom.big-bang-bar.1996"]["sha256"],
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

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.capcom", profile["id"])
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

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_big_bang_bar as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_big_bang_bar as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_big_bang_bar as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Big Bang Bar", b"Big Bang Car", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_big_bang_bar as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class BigBangBarRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_big_bang_bar as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_big_bang_bar as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "capcom/big-bang-bar-1996/source/Big Bang Bar (Capcom 1996) VPW v1.0.vpx"
		script = source_root / "capcom/big-bang-bar-1996/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_big_bang_bar as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "big-bang-bar" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
