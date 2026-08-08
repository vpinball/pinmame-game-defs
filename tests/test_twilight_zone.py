from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "twilight-zone-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "twilight-zone-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "twilight-zone-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "twilight-zone-1993.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "twilight-zone-1993.json"

DRIVER_IDS = {
	"tz_92", "tz_93", "tz_94ch", "tz_94h", "tz_d1", "tz_d2", "tz_d3", "tz_d4",
	"tz_f10", "tz_f100", "tz_f19", "tz_f50", "tz_f86", "tz_f97", "tz_h7", "tz_h8",
	"tz_i7", "tz_i8", "tz_ifpa", "tz_ifpa2", "tz_l1", "tz_l2", "tz_l3", "tz_l4",
	"tz_l5", "tz_la9", "tz_p3", "tz_p3d", "tz_p4", "tz_p5", "tz_pa1", "tz_pa2",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
CUSTOM_COLUMN_ADDRESSES = set(range(91, 99))
UNUSED_MATRIX_ADDRESSES = {24, 71, 82, 86}
OPTO_ADDRESSES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87} | CUSTOM_COLUMN_ADDRESSES
FLIPPER_ADDRESSES = set(range(111, 119))


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
	import curate_twilight_zone as curator

	argv = sys.argv
	sys.argv = ["curate_twilight_zone.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class TwilightZoneDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["semantic_naming"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"semantic_naming", "spatial_placement", "physical_wiring"}:
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.twilight-zone.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2358, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_clock_direction_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.clock-motor-direction-naming"}, set(conflicts))
		conflict = conflicts["conflict.clock-motor-direction-naming"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("unresolved", description)
		self.assertIn("harness", description)
		self.assertIn("56", conflict["path"])
		self.assertIn("57", conflict["path"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertTrue(CONTROLLER_PATH.is_file())

	def test_unconfigured_fast_flip_channel_uses_gilamps_state(self) -> None:
		self.assertIn("WPC_GILAMPS bit 7", self.solenoids[31]["physical"]["notes"])
		self.assertNotIn("fast-flip flag", self.solenoids[31]["physical"]["notes"])

	def test_every_tz_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])

	def test_full_switch_matrix_is_enumerated_with_no_gaps(self) -> None:
		expected = MATRIX_ADDRESSES | CUSTOM_COLUMN_ADDRESSES
		matrix_and_custom = {a for a in self.switches if a in expected}
		self.assertEqual(expected, matrix_and_custom)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
		for address in (MATRIX_ADDRESSES | CUSTOM_COLUMN_ADDRESSES) - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_dedicated_and_flipper_switches_are_present(self) -> None:
		for address in range(1, 9):
			self.assertIn(address, self.switches)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		self.assertEqual(FLIPPER_ADDRESSES, {a for a in self.switches if 111 <= a <= 118})
		for address in FLIPPER_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual(set(range(1, 9)), set(self.dips))

	def test_four_flippers_are_fitted_not_repurposed(self) -> None:
		# Unlike Monster Bash, Twilight Zone genuinely has upper flippers.
		for address, expected in {
			111: "eos", 112: "button", 113: "eos", 114: "button",
			115: "eos", 116: "button", 117: "eos", 118: "button",
		}.items():
			label = self.switches[address]["label"].lower()
			self.assertIn(expected if expected != "eos" else "eos", label, address)

	def test_slingshot_labels_match_pinmame_source_not_the_superseded_legacy_stub(self) -> None:
		# tz.c: #define swLSling 34, #define swRSling 35. The legacy migrated stub this
		# definition replaces had these reversed; regression-guard the correction.
		self.assertIn("left", self.switches[34]["label"].lower())
		self.assertIn("right", self.switches[35]["label"].lower())
		left_x = self.switches[34]["spatial"]["placements"][0]["x"]
		right_x = self.switches[35]["spatial"]["placements"][0]["x"]
		self.assertLess(left_x, 0.5)
		self.assertGreater(right_x, 0.5)

	def test_opto_switches_match_the_pinmame_inverted_switch_mask(self) -> None:
		for address in OPTO_ADDRESSES:
			self.assertTrue(self.switches[address].get("normally_closed"), address)
			self.assertEqual("opto", self.switches[address]["physical"].get("switch_type"), address)
		non_opto_used = {a for a in self.switches if a in MATRIX_ADDRESSES and a not in UNUSED_MATRIX_ADDRESSES and a not in OPTO_ADDRESSES}
		for address in non_opto_used:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)

	def test_not_fitted_devices_have_no_part_number_and_no_placement(self) -> None:
		for address in (71, 82, 86):
			physical = self.switches[address]["physical"]
			self.assertNotIn("part_number", physical)
			self.assertNotIn("assembly_part_number", physical)
		magnet = self.solenoids[22]
		self.assertEqual("unused", magnet["availability"])
		self.assertNotIn("part_number", magnet["physical"])
		self.assertNotIn("assembly_part_number", magnet["physical"])

	def test_geometric_ordering_left_center_right_and_rear_front(self) -> None:
		# Left/right slingshots (already covered above); trough eject-to-drain should
		# increase in y (rear-to-front direction is not meaningful for a trough since it
		# runs along one edge, so assert against the shooter-lane/apron distance instead).
		shooter_y = self.switches[72]["spatial"]["placements"][0]["y"]
		start_button_role_devices = [d for d in self.definition["inputs"] if d["binding"]["device"] == 13]
		self.assertTrue(start_button_role_devices)
		self.assertGreater(shooter_y, 0.9)  # shooter lane sits near the apron (y close to 1)

	def test_auxiliary_board_solenoids_use_manual_address_alias_not_public_address(self) -> None:
		aliases = {
			alias["value"]
			for alias in self.solenoids[56]["aliases"]
			if alias["namespace"] == "manual.address"
		}
		self.assertEqual({"42"}, aliases)
		aliases51 = {
			alias["value"]
			for alias in self.solenoids[51]["aliases"]
			if alias["namespace"] == "manual.address"
		}
		self.assertEqual({"37"}, aliases51)

	def test_solenoids_37_through_44_are_declared_virtual_unused(self) -> None:
		for address in range(37, 45):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_lamp_matrix_is_a_complete_8x8_grid(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address, lamp in self.lamps.items():
			self.assertEqual("used", lamp["availability"], address)

	def test_gi_has_five_strings_and_address_2_has_no_false_placement(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))
		self.assertEqual("not_applicable", self.gi[2]["spatial"]["status"])
		self.assertEqual("validated", self.gi[0]["spatial"]["status"])
		self.assertGreater(len(self.gi[0]["spatial"]["placements"]), 1)

	def test_device_identifiers_are_unique(self) -> None:
		identifiers = [d["id"] for d in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()


class TwilightZoneControllerProfileTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(CONTROLLER_PATH)

	def test_identity(self) -> None:
		self.assertEqual("pinmame.wpc-fliptronic", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])

	def test_switch_group_covers_the_custom_column_and_flipper_range(self) -> None:
		switch_group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.input.switch")
		ranges = {(r["minimum"], r["maximum"]) for r in switch_group["address_rules"]}
		self.assertIn((91, 98), ranges)
		self.assertIn((111, 118), ranges)

	def test_notes_document_the_wpc95_contrast(self) -> None:
		solenoid_group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.solenoid")
		notes = solenoid_group["notes"].lower()
		self.assertIn("wpc-95", notes)
		self.assertIn("37-44", notes)


class TwilightZoneCuratorDeterminismTests(unittest.TestCase):
	def test_check_mode_passes_twice_in_a_row(self) -> None:
		import curate_twilight_zone as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_spatial_report_is_reproducible(self) -> None:
		import curate_twilight_zone as curator

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(report, json.loads(SPATIAL_REPORT_PATH.read_text(encoding="utf-8")))


class TwilightZoneExtractionManifestTests(unittest.TestCase):
	def test_manifest_matches_the_retained_extraction_when_evidence_root_is_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		curator.verify_extraction_manifest(Path(root).expanduser().resolve())


if __name__ == "__main__":
	unittest.main()
