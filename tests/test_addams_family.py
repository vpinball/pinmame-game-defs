from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "the-addams-family-1992.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "the-addams-family-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "the-addams-family-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "the-addams-family-1992.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "the-addams-family-1992.json"
STUB_PATH = ROOT / "machines" / "stubs" / "taf_l5.json"
GOLD_STUB_PATH = ROOT / "machines" / "stubs" / "tafg_lx3.json"

DRIVER_IDS = {
	"taf_l5", "taf_p2", "taf_p3", "taf_l1", "taf_d1", "taf_l2", "taf_d2", "taf_l3", "taf_d3",
	"taf_l4", "taf_d4", "taf_l5c", "taf_l7", "taf_d7", "taf_d7bs", "taf_l6", "taf_d6", "taf_h4",
	"taf_i4", "taf_d5",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 28, 46, 52, 83, 88}
OPTO_ADDRESSES = {53, 54, 55, 56, 57, 84, 85}


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
	import curate_addams_family as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_addams_family.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


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


class AddamsFamilyDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["recreation_notes"], self.definition["coverage"]["missing"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["recreation_knowledge"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "recreation_knowledge":
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.the-addams-family.1992", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(20, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1992, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])

	def test_the_stale_stub_is_gone_and_gold_stub_is_untouched(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertFalse(STUB_PATH.exists(), "taf_l5 stub must be pruned once the curated definition claims it")
		self.assertTrue(GOLD_STUB_PATH.is_file(), "tafg_lx3 (Gold, a separate physical machine) must stay untouched")
		gold_stub = load_json(GOLD_STUB_PATH)
		self.assertEqual("stub", gold_stub["coverage"]["status"])
		self.assertEqual("stub.pinmame.tafg_lx3", gold_stub["machine"]["id"])

	def test_every_taf_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["taf_l5"])
		for driver_id in DRIVER_IDS - {"taf_l5"}:
			self.assertEqual("taf_l5", by_id[driver_id]["clone_of"], driver_id)
		# tafg_* (Gold, 1994 Williams reissue) must never appear here -- it is a separate physical machine.
		self.assertFalse(any(driver_id.startswith("tafg") for driver_id in DRIVER_IDS))

	def test_the_full_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_ticket_opto_is_enumerated_but_unfitted_despite_its_name(self) -> None:
		# Address 23 prints "Ticket Opto." in its description, but both the Switch Number and
		# Switch Assy columns of the parts list read blank/"Not Used" -- unlike the seven genuine
		# optos, no opto assembly part number is printed, so it must not be treated as fitted.
		switch = self.switches[23]
		self.assertEqual("unused", switch["availability"])
		self.assertEqual("unused", switch["spatial"]["reason"])
		self.assertNotIn(23, OPTO_ADDRESSES)

	def test_opto_polarity_matches_pinmames_inverted_switch_mask_with_zero_conflicts(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])
		# Unlike Monster Bash's Dracula-position optos, this project found full agreement between
		# the manual's opto sweep and tafGameData's inverted-switch mask, so there is no conflict.
		self.assertEqual([], self.definition["conflicts"])
		self.assertNotIn("unresolved_conflicts", self.definition["coverage"]["missing"])

	def test_pinmame_inverted_mask_column_by_column(self) -> None:
		import curate_addams_family as curator

		# {Coin,1,2,3,4,5,6,7,8,9,10,Cab.} -- column 5 (0x7c, bits 2-6) = 53-57; column 8 (0x18,
		# bits 3-4) = 84-85. Every other column is 0x00.
		mask = (0x00, 0x00, 0x00, 0x00, 0x00, 0x7c, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00)
		self.assertEqual(0x7c, mask[5])
		self.assertEqual(0x18, mask[8])
		self.assertEqual(0, sum(mask) - 0x7c - 0x18)
		for address in (53, 54, 55, 56, 57, 84, 85):
			self.assertIn(address, curator.OPTO_SWITCHES)
			self.assertIn(address, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)

	def test_both_upper_fliptronic_flippers_are_fitted_hardware(self) -> None:
		# Unlike Monster Bash (upper positions 115/116/118 unused, F7 repurposed as a spinner), TAF
		# genuinely fits both upper flippers: tafGameData sets FLIP_SW(FLIP_U) and FLIP_SOL(FLIP_U),
		# the manual prints full illustrated parts breakdowns for both, and the retained script wires
		# both SolURFlipper and SolULFlipper to independently animated table objects.
		for address in (111, 112, 113, 114, 115, 116, 117, 118):
			self.assertEqual("used", self.switches[address]["availability"], address)
			self.assertFalse(self.switches[address]["normally_closed"], address)
		for address in (33, 34, 35, 36, 45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
		self.assertIn("Thing Flips", self.solenoids[35]["physical"]["notes"])
		self.assertIn("Thing Flips", self.solenoids[36]["physical"]["notes"])

	def test_the_full_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address in (41, 76):
			self.assertEqual("unused", self.lamps[address]["availability"], address)
			self.assertEqual("unused", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 23):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (25, 27):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (16, 23, 24):
			self.assertEqual("magnet", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		# Every printed solenoid table row (1-28) is a real, fitted device -- unlike Monster Bash's
		# unfitted 4 and 7, TAF has no NOT_USED position in its solenoid table.
		for address in range(1, 29):
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_cousin_it_shares_one_switch_across_four_targets(self) -> None:
		switch = self.switches[44]
		self.assertEqual("used", switch["availability"])
		self.assertEqual("validated", switch["spatial"]["status"])
		self.assertEqual(4, len(switch["spatial"]["placements"]))
		xs = [placement["x"] for placement in switch["spatial"]["placements"]]
		ys = [placement["y"] for placement in switch["spatial"]["placements"]]
		self.assertLess(max(xs) - min(xs), 0.03)
		self.assertLess(max(ys) - min(ys), 0.1)

	def test_bookcase_and_thing_hand_switches_project_onto_their_own_mechanism(self) -> None:
		for address in (81, 82):
			switch = self.switches[address]
			self.assertEqual("not_applicable", switch["spatial"]["status"], address)
			self.assertEqual("internal_nonvisual", switch["spatial"]["reason"], address)
		for address in (84, 85):
			switch = self.switches[address]
			self.assertEqual("not_applicable", switch["spatial"]["status"], address)
			self.assertEqual("internal_nonvisual", switch["spatial"]["reason"], address)
			self.assertEqual("opto", switch["physical"]["switch_type"], address)

	def test_lamp_header_row_boundary_clamp(self) -> None:
		for address in (81, 82, 83, 84, 85, 86, 87):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			placement = lamp["spatial"]["placements"][0]
			self.assertEqual(0.0, placement["y"], address)
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_not(self) -> None:
		for address in (0, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(7, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(4, len(self.gi[4]["spatial"]["placements"]))
		for address in (1, 2):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
		self.assertEqual("unused", self.gi[3]["availability"])
		self.assertEqual("not_applicable", self.gi[3]["spatial"]["status"])
		self.assertEqual("unused", self.gi[3]["spatial"]["reason"])

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
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual("partial", report["status"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual(located, report["placement_count"])
		self.assertTrue(report["blockers"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}

		# Jet bumper cluster: upper-left left of upper-right; center-left left of center-right.
		self.assertLess(switch_x[31], switch_x[32])
		self.assertLess(switch_x[33], switch_x[34])

		# Left-named devices keep x < 0.5 and right-named devices keep x > 0.5, for switches with
		# independent objects on each side.
		self.assertLess(switch_x[36], 0.5)
		self.assertGreater(switch_x[37], 0.5)
		self.assertLess(switch_x[38], 0.5)
		self.assertGreater(switch_x[67], 0.5)

		# Lower flippers: left flipper x < right flipper x, level apron (same y).
		flippers = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		right_lower = flippers[45]["spatial"]["placements"][0]
		left_lower = flippers[47]["spatial"]["placements"][0]
		self.assertLess(left_lower["x"], right_lower["x"])
		self.assertEqual(left_lower["y"], right_lower["y"])

		# Upper flippers: the "Thing" (upper-left) flipper sits left of center; the upper-right
		# flipper sits right of center.
		upper_left = flippers[35]["spatial"]["placements"][0]
		upper_right = flippers[33]["spatial"]["placements"][0]
		self.assertLess(upper_left["x"], 0.5)
		self.assertGreater(upper_right["x"], 0.5)

		# Bookcase optos 53-56 ascend in x, matching their printed 1-4 order.
		self.assertLess(switch_x[53], switch_x[54])
		self.assertLess(switch_x[54], switch_x[55])
		self.assertLess(switch_x[55], switch_x[56])

		# Trough order: left trough nearest the drain has the largest y (closest to the apron);
		# right trough (release position) has the smallest y among the three.
		self.assertGreater(switch_y[15], switch_y[16])
		self.assertGreater(switch_y[16], switch_y[17])

		# Grave letters: lamp 43 ("G") and lamp 44 ("R") stay left of lamp 48 ("E").
		self.assertLess(lamp_x[43], lamp_x[48])
		self.assertLess(lamp_x[44], lamp_x[48])

	def test_mechanism_inventory_covers_every_used_coil_motor_or_magnet(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.bookcase", "mechanism.thing-hand", "mechanism.thing-saucer",
				"mechanism.thing-kickout", "mechanism.swamp-lock", "mechanism.ramp-diverter",
				"mechanism.trough-and-shooter", "mechanism.jet-bumpers", "mechanism.slingshots",
				"mechanism.magnets", "mechanism.lower-flippers", "mechanism.upper-right-flipper",
				"mechanism.upper-left-flipper", "mechanism.chair-kickout", "mechanism.cabinet-knocker",
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
			if device["kind"] in {"coil", "motor", "magnet"} and device["availability"] == "used"
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("bookPos", mechanisms["mechanism.bookcase"]["behavior"])
		self.assertIn("thingPos", mechanisms["mechanism.thing-hand"]["behavior"])
		self.assertIn("Thing Flips", mechanisms["mechanism.upper-left-flipper"]["behavior"])

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
		self.assertIn("vpx-script.taf-g5k-2-3-2", sources)
		self.assertTrue(sources["vpx-script.taf-g5k-2-3-2"]["known_working"])
		self.assertEqual(
			"c5f1aedc5f05c277459d97be18046f07e2617522841545317ebdfad4ec34e2fc",
			sources["vpx-script.taf-g5k-2-3-2"]["sha256"],
		)
		self.assertEqual(
			"85af088f0ed6d59c83599102e6245cc2eab5674e69d29882db6f0eaacf05e858",
			sources["vpx-table.taf-g5k-2-3-2"]["sha256"],
		)
		for source in self.definition["sources"]:
			self.assertNotEqual("runtime_scenario", source["kind"])
			self.assertNotEqual("rom_static_analysis", source["kind"])
			self.assertNotEqual("ipdb", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_controller_profile_is_reused_unchanged_and_declares_every_used_binding_group(self) -> None:
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


class AddamsFamilyCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_addams_family as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_addams_family as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_addams_family as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"The Addams Family", b"The Addams Fam1ly", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_addams_family as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class AddamsFamilyRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_addams_family as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_addams_family as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "bally/the-addams-family-1992/source/The Addams Family (Bally1992) v2.3.2 (g5k).vpx"
		script = source_root / "bally/the-addams-family-1992/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_addams_family as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "the-addams-family-1992" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
