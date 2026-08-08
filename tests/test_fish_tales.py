from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "fish-tales-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "fish-tales-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "fish-tales-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "fish-tales-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "fish-tales-1992.json"

DRIVER_IDS = {"ft_l5", "ft_l5p", "ft_d5", "ft_d6", "ft_l3", "ft_l4", "ft_p2", "ft_p4", "ft_p5"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
MANUAL_OPTO_ADDRESSES = {37, 38}
PINMAME_NORMALIZED_ADDRESSES = {47, 48}
NOT_FITTED_UPPER_FLIPPER_SOLENOIDS = {33, 34, 35, 36}
FAKE_REEL_SOLENOIDS = {51, 52, 53}


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
	import curate_fish_tales as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_fish_tales.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class FishTalesDefinitionTests(unittest.TestCase):
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
		self.assertEqual("williams.fish-tales.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(861, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_two_polarity_conflicts_are_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{"conflict.reel-opto-switches-not-normalized", "conflict.ball-popper-drop-target-normalized-non-opto"},
			set(conflicts),
		)
		reel = conflicts["conflict.reel-opto-switches-not-normalized"]
		self.assertGreaterEqual(len(reel["source_refs"]), 2)
		self.assertIn("unresolved", reel["description"].lower())
		self.assertIn("harness", reel["description"].lower())
		for address in (37, 38):
			self.assertIn(str(address), reel["path"])
		popper = conflicts["conflict.ball-popper-drop-target-normalized-non-opto"]
		self.assertGreaterEqual(len(popper["source_refs"]), 2)
		self.assertIn("unresolved", popper["description"].lower())
		for address in (47, 48):
			self.assertIn(str(address), popper["path"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_ft_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in DRIVER_IDS - {"ft_l5"}:
			self.assertEqual("ft_l5", by_id[driver_id]["clone_of"], driver_id)
		self.assertNotIn("clone_of", by_id["ft_l5"])

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_matrix_polarity_reflects_the_two_documented_conflicts_not_a_uniform_convention(self) -> None:
		for address in sorted(MANUAL_OPTO_ADDRESSES):
			switch = self.switches[address]
			self.assertEqual("opto", switch["physical"]["switch_type"], address)
			self.assertNotIn("normally_closed", switch, address)
		for address in sorted(PINMAME_NORMALIZED_ADDRESSES):
			switch = self.switches[address]
			self.assertTrue(switch["normally_closed"], address)
			self.assertEqual("microswitch", switch["physical"]["switch_type"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24} - MANUAL_OPTO_ADDRESSES - PINMAME_NORMALIZED_ADDRESSES):
			switch = self.switches[address]
			self.assertFalse(switch["normally_closed"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_reel_opto_mask_bit_arithmetic(self) -> None:
		# Column index 4 (1-based, matching the manual/driver convention) is 0xc0: bits 6 and 7 are
		# the only set bits anywhere in ftGameData's twelve-column inverted-switch mask, and they land
		# on public switches 47 and 48, not the manual-documented reel optos 37/38 (column 3, 0x00).
		mask = (0x00, 0x00, 0x00, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		self.assertEqual(0x00, mask[2])
		self.assertEqual(0xC0, mask[3])
		set_bits = [bit + 1 for bit in range(8) if (mask[3] >> bit) & 1]
		self.assertEqual([7, 8], set_bits)
		self.assertEqual({47, 48}, {40 + bit for bit in set_bits})

	def test_no_upper_flippers_despite_the_driver_declaration(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
			self.assertNotIn("wiring", self.switches[address], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		for address in sorted(NOT_FITTED_UPPER_FLIPPER_SOLENOIDS):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)
			self.assertIn("not fitted", self.solenoids[address]["physical"]["notes"].lower())
		# No conflicts entry documents the flipper-fitment disagreement -- it is a resolved finding,
		# not an open one, matching this project's precedent for asymmetric-evidence corrections.
		conflict_ids = {conflict["id"] for conflict in self.definition["conflicts"]}
		self.assertFalse(any("flipper" in identifier for identifier in conflict_ids))

	def test_lower_flipper_supply_and_drive_connections_are_distinct(self) -> None:
		expected = {
			45: ("J907-8, 9", "J902-13"),
			46: ("J907-8, 9", "J902-11"),
			47: ("J907-6, 7", "J902-9"),
			48: ("J907-6, 7", "J902-7"),
		}
		for address, (power, control) in expected.items():
			self.assertEqual(power, self.solenoids[address]["wiring"]["power_connection"], address)
			self.assertEqual(control, self.solenoids[address]["wiring"]["control_connection"], address)

	def test_fake_reel_solenoids_are_virtual_pinmame_only_bookkeeping(self) -> None:
		for address in sorted(FAKE_REEL_SOLENOIDS):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"], address)
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("virtual", device["spatial"]["reason"], address)
			self.assertIn("CORE_CUSTSOLNO", device["physical"]["notes"], address)
		self.assertIn("never references", self.solenoids[51]["physical"]["notes"])

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 54))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 28):
			if address == 24:
				continue
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		self.assertEqual("flasher", self.solenoids[24]["kind"])
		self.assertEqual("unused", self.solenoids[24]["availability"])
		self.assertEqual("motor", self.solenoids[28]["kind"])
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50, 51, 52, 53):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in (29, 30, 31):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		self.assertEqual("unused", self.solenoids[32]["availability"])
		self.assertEqual(["internal.unused.wpc-output"], self.solenoids[32]["roles"])

	def test_knocker_and_backbox_fish_are_cabinet_devices_not_playfield(self) -> None:
		for address, label in ((7, "Knocker"), (8, "Backbox Fish")):
			device = self.solenoids[address]
			self.assertEqual(label, device["label"])
			self.assertEqual("used", device["availability"])
			self.assertEqual("not_applicable", device["spatial"]["status"])
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (2, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(21, len(self.gi[2]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[4]["spatial"]["placements"]))
		for address in (0, 1, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamps_16_17_18_are_backbox_devices_despite_matching_boat_switch_theme(self) -> None:
		for address in (16, 17, 18):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], lamp["roles"], address)
		for address in (44, 45, 46):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"], address)

	def test_lamp_48_has_two_disclosed_placements_and_no_lamp_is_unused(self) -> None:
		self.assertEqual(2, self.lamps[48]["physical"]["quantity"])
		self.assertEqual(2, len(self.lamps[48]["spatial"]["placements"]))
		self.assertIn("inferred", self.lamps[48]["physical"]["notes"].lower())
		for lamp in self.lamps.values():
			self.assertEqual("used", lamp["availability"], lamp["id"])

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
		self.assertEqual([], report["unresolved"])
		self.assertEqual(located, report["placement_count"])

	def test_reel_opto_switches_are_projected_onto_the_reel_object(self) -> None:
		for address in (37, 38):
			switch = self.switches[address]
			self.assertEqual("validated", switch["spatial"]["status"])
			placement = switch["spatial"]["placements"][0]
			self.assertAlmostEqual(0.122796, placement["x"], places=6)
			self.assertAlmostEqual(0.457965, placement["y"], places=6)

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		lamp_y = {addr: pos[1] for addr, pos in _emitter_positions(self.lamps).items()}
		# Left jet bumper (51) is left of right jet bumper (53); center (52) sits between them.
		self.assertLess(switch_x[51], switch_x[52])
		self.assertLess(switch_x[52], switch_x[53])
		# Left slingshot is left of right slingshot.
		self.assertLess(switch_x[57], switch_x[58])
		# Left standup targets are left of right standup targets.
		self.assertLess(switch_x[27], switch_x[54])
		self.assertLess(switch_x[28], switch_x[55])
		# Left/right boat entry and exit lanes keep left-right ordering.
		self.assertLess(switch_x[43], switch_x[42])
		# Left fish lamps (45-47) sit left of the matching right fish lamps (55-57).
		self.assertLess(lamp_x[45], lamp_x[55])
		self.assertLess(lamp_x[46], lamp_x[56])
		self.assertLess(lamp_x[47], lamp_x[57])
		# Trough position 1 (nearest the release exit) sits closer to the shooter lane (larger x,
		# toward the Plunger at x=0.939) than trough position 3 (nearest the outhole).
		self.assertGreater(switch_x[16], switch_x[18])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.reel", "mechanism.catapult",
				"mechanism.casters-club", "mechanism.fish-finder", "mechanism.gate",
				"mechanism.drop-target-ramp", "mechanism.jet-bumpers", "mechanism.slingshots",
				"mechanism.knocker", "mechanism.backbox-fish", "mechanism.boat",
				"mechanism.lower-flippers",
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
		self.assertIn("reel", mechanisms["mechanism.reel"]["kind"])
		self.assertIn("Habit Trail", mechanisms["mechanism.casters-club"]["behavior"])

	def test_relationships_field_is_present_and_empty(self) -> None:
		# No causal solenoid-to-different-switch pulse relationship was independently evidenced for
		# this machine's trough/catapult/reel routing beyond ordinary direct switch assertions, so
		# the (schema-optional, non-empty-not-required) relationships array stays empty rather than
		# asserting an unevidenced causal link.
		self.assertEqual([], self.definition["relationships"])

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
		self.assertIn("vpx-script.ft-vpw-1-1", sources)
		self.assertTrue(sources["vpx-script.ft-vpw-1-1"]["known_working"])
		self.assertEqual(
			"b6289a7087f11bd1902d8b059fe663723a6319c6490d1a2fa124d3dd7089e1f5",
			sources["vpx-script.ft-vpw-1-1"]["sha256"],
		)
		self.assertEqual(
			"1f82c0237831b50c514e53c8938636f59ee584fc4346c143a3216b9f5d8a1029",
			sources["vpx-table.ft-vpw-1-1"]["sha256"],
		)
		self.assertNotIn("runtime.fish-tales", sources)
		self.assertNotIn("rom.ft", sources)
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

	def test_manual_source_excerpts_are_reviewed_and_hashed(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.williams.fish-tales.1992"]
		excerpts = manual.get("excerpts") or []
		self.assertGreaterEqual(len(excerpts), 7)
		for excerpt in excerpts:
			self.assertTrue(excerpt["reviewed"])
			self.assertEqual("manual", excerpt["method"])
			self.assertTrue((ROOT / excerpt["path"]).is_file(), excerpt["path"])

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


def _switch_positions(switches: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in switches.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


def _emitter_positions(lamps: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in lamps.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class FishTalesCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_fish_tales as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_fish_tales as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_fish_tales as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Fish Tales", b"Fish Sales", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_fish_tales as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class FishTalesRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_fish_tales as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_fish_tales as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/fish-tales-1992/source/Fish Tales (Williams 1992) VPW 1.1.vpx"
		script = source_root / "williams/fish-tales-1992/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_fish_tales as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "fish-tales" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
