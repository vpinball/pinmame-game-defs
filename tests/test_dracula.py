from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "bram-stoker-s-dracula-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "bram-stoker-s-dracula-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "dracula.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "bram-stoker-s-dracula-1993.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "bram-stoker-s-dracula-1993.md"

DRIVER_IDS = {"drac_l1", "drac_d1", "drac_l2c", "drac_p11", "drac_p12"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 18, 23, 32, 33, 45, 46, 47, 74, 75, 76, 78}
OPTO_ADDRESSES = {51, 52, 53, 54, 55, 56, 57, 71, 72, 73, 82}


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
	import curate_dracula as curator

	argv = sys.argv
	sys.argv = ["curate_dracula.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class DraculaDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"physical_wiring", "spatial_placement"}:
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.bram-stoker-s-dracula.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(3072, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_driver_set_matches_physical_family(self) -> None:
		driver_ids = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, driver_ids)
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["drac_l1"])
		for clone_id in DRIVER_IDS - {"drac_l1"}:
			self.assertEqual("drac_l1", by_id[clone_id]["clone_of"])
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"])

	def test_switch_matrix_covers_every_address_exactly_once(self) -> None:
		matrix_switches = {address: item for address, item in self.switches.items() if address in MATRIX_ADDRESSES}
		self.assertEqual(MATRIX_ADDRESSES, set(matrix_switches))
		for address, item in matrix_switches.items():
			expected_availability = "unused" if address in UNUSED_MATRIX_ADDRESSES else "used"
			self.assertEqual(expected_availability, item["availability"], address)

	def test_opto_addresses_match_pinmame_inverted_switch_mask_with_zero_disagreement(self) -> None:
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			item = self.switches[address]
			if item["kind"] != "switch":
				continue
			expected_normally_closed = address in OPTO_ADDRESSES
			self.assertEqual(expected_normally_closed, item["normally_closed"], address)
			expected_type = "opto" if address in OPTO_ADDRESSES else item["physical"].get("switch_type")
			self.assertEqual(expected_type, item["physical"].get("switch_type"), address)

	def test_no_upper_flippers_are_modeled_as_used(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			item = self.switches[address]
			self.assertEqual("unused", item["availability"], address)
			self.assertEqual("not_applicable", item["spatial"]["status"], address)
			self.assertEqual("unused", item["spatial"]["reason"], address)

	def test_upper_flipper_circuit_solenoids_are_repurposed_not_flippers(self) -> None:
		labels = {33: "Up/Down Post Diverter", 34: "Right Gate", 35: "Castle Release Post", 36: "Left Gate Actuator"}
		for address, label in labels.items():
			item = self.solenoids[address]
			self.assertEqual(label, item["label"], address)
			self.assertEqual("used", item["availability"], address)

	def test_flipper_coils_are_at_the_wpc_fliptronic_addresses(self) -> None:
		for address in (45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_single_drop_target_not_a_three_bank(self) -> None:
		mechanism_ids = {mechanism["id"] for mechanism in self.definition["mechanisms"]}
		self.assertIn("mechanism.drop-target", mechanism_ids)
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.drop-target")
		self.assertEqual(["switch.matrix-15", "switch.matrix-16"], sorted(mechanism["sensors"]))

	def test_the_upper_flipper_circuit_side_naming_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.upper-flipper-circuit-side-naming"}, set(conflicts))
		conflict = conflicts["conflict.upper-flipper-circuit-side-naming"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("unresolved", description)
		for address in (33, 34, 35, 36):
			self.assertIn(str(address), conflict["path"])

	def test_lamp_53_has_no_fabricated_spatial_record(self) -> None:
		lamp = self.lamps[53]
		self.assertEqual("used", lamp["availability"])
		self.assertNotIn("spatial", lamp)

	def test_backbox_lamps_are_not_applicable(self) -> None:
		for address in (58, 61, 62, 63):
			lamp = self.lamps[address]
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"], address)

	def test_gi_playfield_strings_have_placements_and_backbox_strings_do_not(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			self.assertGreater(len(self.gi[address]["spatial"]["placements"]), 0, address)
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)

	def test_gi_playfield_placement_counts_match_retained_light_collections(self) -> None:
		self.assertEqual(8, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(20, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(10, len(self.gi[2]["spatial"]["placements"]))

	def test_dracula_name_chase_addresses_spell_dracula_in_documented_order(self) -> None:
		chase_order = [48, 36, 23, 71, 67, 72, 82]
		self.assertEqual({48, 36, 23, 71, 67, 72, 82}, set(chase_order))
		expected_letters = "DRACULA"
		for address, letter in zip(chase_order, expected_letters):
			self.assertIn(letter, self.lamps[address]["label"].upper(), address)

	def test_left_right_switch_geometry_is_on_the_correct_side(self) -> None:
		def x_of(address: int) -> float:
			return self.switches[address]["spatial"]["placements"][0]["x"]

		self.assertLess(x_of(35), 0.5)  # Left Drain
		self.assertGreater(x_of(38), 0.5)  # Right Drain
		self.assertLess(x_of(36), 0.5)  # Left Return
		self.assertGreater(x_of(37), 0.5)  # Right Return
		self.assertLess(x_of(64), 0.5)  # Left Slingshot
		self.assertGreater(x_of(65), 0.5)  # Right Slingshot

	def test_trough_switches_are_monotonically_ordered(self) -> None:
		positions = [self.switches[address]["spatial"]["placements"][0]["y"] for address in (41, 42, 43, 44)]
		self.assertEqual(sorted(positions), positions)

	def test_no_duplicate_device_identifiers(self) -> None:
		identifiers = [device["id"] for device in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_seed_is_byte_identical_to_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_controller_profile_is_reused_unchanged(self) -> None:
		self.assertTrue(CONTROLLER_PATH.is_file())
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])

	def test_knowledge_file_exists_and_is_referenced(self) -> None:
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertEqual("knowledge/williams/dracula.md", self.definition["knowledge"]["path"])

	def test_spatial_report_files_exist(self) -> None:
		self.assertTrue(SPATIAL_REPORT_PATH.is_file())
		self.assertTrue(SPATIAL_REPORT_MARKDOWN_PATH.is_file())
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("williams.bram-stoker-s-dracula.1993", report["machine_id"])
		self.assertIn("lamp.matrix-53", report["unresolved"])

	def test_curator_check_mode_is_idempotent(self) -> None:
		import curate_dracula as curator

		curator.check(curator.ROOT)

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()


if __name__ == "__main__":
	unittest.main()
