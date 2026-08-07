from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "the-getaway-high-speed-ii-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "the-getaway-high-speed-ii-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "the-getaway-high-speed-ii-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "the-getaway-high-speed-ii-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "the-getaway-high-speed-ii-1992.json"

DRIVER_IDS = {
	"gw_l5", "gw_d5", "gw_l5c", "gw_pb", "gw_pc", "gw_pd", "gw_p7", "gw_p8",
	"gw_l1", "gw_d1", "gw_l2", "gw_d2", "gw_l3", "gw_d3",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 35, 47, 48, 64, 66, 68}
OPTO_ADDRESSES = {81, 82, 83, 84, 85}


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
	import curate_getaway as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_getaway.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class GetawayDefinitionTests(unittest.TestCase):
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
			["output_semantics", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["semantic_naming"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["output_semantics"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("williams.the-getaway-high-speed-ii.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1000, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])

	def test_both_conflicts_are_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{
				"conflict.switch-84-85-manual-vs-script-semantics",
				"conflict.solenoid-31-fastflip-address-not-declared",
			},
			set(conflicts),
		)
		for conflict in conflicts.values():
			self.assertGreaterEqual(len(conflict["source_refs"]), 2)
			self.assertIn("unresolved", conflict["description"].lower())
		self.assertIn("84", conflicts["conflict.switch-84-85-manual-vs-script-semantics"]["path"])
		self.assertIn("85", conflicts["conflict.switch-84-85-manual-vs-script-semantics"]["path"])
		self.assertIn("31", conflicts["conflict.solenoid-31-fastflip-address-not-declared"]["path"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_gw_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in DRIVER_IDS - {"gw_l5"}:
			self.assertEqual("gw_l5", by_id[driver_id]["clone_of"], driver_id)
		self.assertNotIn("clone_of", by_id["gw_l5"])

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {23}):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("optional", self.switches[23]["availability"])

	def test_printed_opto_polarity_matches_pinmames_inverted_switch_mask_exactly(self) -> None:
		# gwGameData's mask ({...,0x1f,0x00,0x00,0x00}) sets column 8 bits 0-4 (rows 1-5): exactly
		# addresses 81-85. Every other switch must not be normally_closed=True.
		mask = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1f, 0x00, 0x00, 0x00)
		self.assertEqual(0x1f, mask[8])
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_switches_with_no_vpx_geometry_have_no_spatial_key(self) -> None:
		for address in (33, 34, 56, 57, 58):
			self.assertNotIn("spatial", self.switches[address], address)
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_upper_left_flipper_is_confirmed_unfitted_by_three_independent_sources(self) -> None:
		for address in (111, 112, 113, 114, 115, 116):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		description = self.switches[117]["physical"]["notes"]
		self.assertIn("NOT USED", description)
		self.assertIn("Black/Blue(NU)", description)
		self.assertIn("A-15205-L", description)

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 29)) | {33, 34, 35, 36, 45, 46, 47, 48} | {29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 25):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (25, 26, 27, 28):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_flipper_coil_solenoids_match_the_switch_fitment(self) -> None:
		for address in (33, 34, 45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
		for address in (35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)

	def test_driver_guessed_slingshot_solenoid_labels_are_corrected_by_the_manual(self) -> None:
		left = self.solenoids[5]
		right = self.solenoids[6]
		self.assertEqual("Left Slingshot", left["label"])
		self.assertEqual("Right Slingshot", right["label"])
		self.assertIn("sRSling", left["physical"]["notes"])
		self.assertIn("guessed", left["physical"]["notes"])

	def test_solenoid_27_is_backbox_and_solenoid_7_is_cabinet(self) -> None:
		mars_lamp = self.solenoids[27]
		self.assertEqual("Revolving Lamp", mars_lamp["label"])
		self.assertEqual("not_applicable", mars_lamp["spatial"]["status"])
		self.assertEqual("cabinet_or_service", mars_lamp["spatial"]["reason"])
		self.assertIn("Mars Lamp", mars_lamp["physical"]["notes"])
		knocker = self.solenoids[7]
		self.assertEqual("not_applicable", knocker["spatial"]["status"])
		self.assertEqual("cabinet_or_service", knocker["spatial"]["reason"])

	def test_solenoids_with_no_confirmed_vpx_object_have_no_spatial_key(self) -> None:
		for address in (1, 25, 26, 28):
			self.assertNotIn("spatial", self.solenoids[address], address)
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_gi_playfield_strings_are_undifferentiated_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertEqual(["playfield.gi"], self.gi[address]["roles"], address)
		for address in (2, 3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_quantities_and_stop_light_gap_are_explicit(self) -> None:
		doubled = {16, 18, 35, 63, 64, 65}
		for address in doubled:
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in sorted(MATRIX_ADDRESSES - doubled - {68, 73, 74, 75}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual("not_applicable", self.lamps[68]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[68]["spatial"]["reason"])
		for address in (73, 74, 75):
			self.assertNotIn("spatial", self.lamps[address], address)

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
		self.assertEqual("partial", report["status"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		lamp_pos = _positions(self.lamps)
		# Freeway loops: left is left of right on both switches and lamps.
		self.assertLess(switch_pos[15][0], switch_pos[17][0])
		self.assertLess(switch_pos[16][0], switch_pos[18][0])
		# Outlanes are outboard of return lanes on both sides.
		self.assertLess(switch_pos[25][0], switch_pos[26][0])
		self.assertGreater(switch_pos[28][0], switch_pos[27][0])
		# Right bank targets ascend bottom(44) -> middle(45) -> top(46) in y (top has smaller y).
		self.assertGreater(switch_pos[44][1], switch_pos[45][1])
		self.assertGreater(switch_pos[45][1], switch_pos[46][1])
		# Left bank targets: same ascending pattern for 86/87/88.
		self.assertGreater(switch_pos[86][1], switch_pos[87][1])
		self.assertGreater(switch_pos[87][1], switch_pos[88][1])
		# Lock ladder: top (74) has the smallest y, bottom (76) the largest.
		self.assertLess(switch_pos[74][1], switch_pos[75][1])
		self.assertLess(switch_pos[75][1], switch_pos[76][1])
		# Left slingshot switch is left of right slingshot switch.
		self.assertLess(switch_pos[31][0], switch_pos[32][0])
		# Lamp side check: Left Return Lane (62) is left of Right Return Lane (61).
		self.assertLess(lamp_pos[62][0], lamp_pos[61][0])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.supercharger-loop", "mechanism.supercharger-diverter", "mechanism.ramp-lift",
				"mechanism.ball-lock", "mechanism.kickback", "mechanism.trough", "mechanism.shooter-lane",
				"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.eject-hole",
				"mechanism.gear-shifter", "mechanism.lower-flippers", "mechanism.upper-right-flipper",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
		self.assertIn(
			"conflict.switch-84-85-manual-vs-script-semantics",
			json.dumps(self.definition["mechanisms"]) or "",
		)

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
		self.assertIn("vpx-script.gw-v1.2", sources)
		self.assertTrue(sources["vpx-script.gw-v1.2"]["known_working"])
		self.assertEqual(
			"4f91dbf71bf134b1113939a517900c27d87fa1a142109e79ad64306a40aeb78e",
			sources["vpx-script.gw-v1.2"]["sha256"],
		)
		self.assertEqual(
			"22e7257316dcb3c414f62a0543f6a68063e8f50524ad9559f1ff98bd38184efc",
			sources["vpx-table.gw-v1.2"]["sha256"],
		)
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
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])
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


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class GetawayCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_getaway as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_getaway as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_getaway as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"The Getaway", b"The Getawoy", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_getaway as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class GetawayRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_getaway as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_getaway as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/the-getaway-high-speed-ii-1992/source/Getaway, The - High Speed II v1.2.vpx"
		script = source_root / "williams/the-getaway-high-speed-ii-1992/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_getaway as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "getaway" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
