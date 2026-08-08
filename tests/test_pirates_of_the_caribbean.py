"""Fail-closed tests for the Stern Pirates of the Caribbean (2006) definition.

The assertions that matter most here are the cheap geometric ordering ones. A reversed
left/right identity survives every schema check and every hash check, and the only thing that
catches it is asserting that the lamp or switch the manual calls "left" really does have a
smaller normalized x than the one it calls "right" -- and, where the manual names the same
feature on both sides of the machine, that the lamp and the switch agree with each other.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "pirates-of-the-caribbean-2006.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "pirates-of-the-caribbean-2006.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "pirates-of-the-caribbean-2006.json"
SUPERSEDED_STUB_PATH = ROOT / "machines" / "stubs" / "potc_600af.json"
SUPERSEDED_STUB_KNOWLEDGE_PATH = ROOT / "knowledge" / "stubs" / "potc_600af.md"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "pirates-of-the-caribbean-2006.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "sam.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "pirates-of-the-caribbean-2006.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "stern" / "pirates-of-the-caribbean-2006.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "stern.pirates-of-the-caribbean.2006"

MACHINE_ID = "stern.pirates-of-the-caribbean.2006"
PARENT_DRIVER = "potc_600af"
CLONE_DRIVER_COUNT = 27

PLAYFIELD_WIDTH = 952.0
PLAYFIELD_HEIGHT = 2155.0

MATRIX_ADDRESSES = set(range(1, 65))
UNUSED_MATRIX_ADDRESSES = {5, 7, 17, 33, 34, 35, 36, 38, 40, 41, 48, 49, 59, 64}
CABINET_MATRIX_ADDRESSES = {15, 16}
MANUAL_OPTO_ADDRESSES = {3, 4, 11, 21, 22, 60, 61}
SERVICE_SWITCH_ADDRESSES = set(range(-7, 1))
DEDICATED_SWITCH_ADDRESSES = set(range(65, 73))
FLIPPER_SWITCH_ADDRESSES = set(range(81, 89))
UNREACHABLE_FLIPPER_SWITCHES = {85, 86, 87, 88}

PRINTED_SOLENOID_ADDRESSES = set(range(1, 33))
UNFITTED_SOLENOID_ADDRESSES = {7, 8, 12, 13, 14, 17}
FLASHER_ADDRESSES = {20, 22, 30, 31, 32}
GAME_ON_SOLENOID = 33
VIRTUAL_SOLENOID_ADDRESSES = set(range(33, 51))
AUX_SOLENOID_ADDRESSES = set(range(51, 67))
LAMP_ADDRESSES = set(range(1, 81))
BACK_PANEL_LAMPS = {33, 34, 35, 36, 37, 38, 39, 78, 79, 80}
CABINET_LAMPS = {1, 2}

EXPECTED_CONFLICT_IDS = {
	"conflict.coin-door-adjust-button-order",
	"conflict.flasher-back-panel-bulb-count",
	"conflict.pop-bumper-position-naming",
	"conflict.sam-invsw-never-populated",
}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def only_placement(device: dict) -> dict:
	placements = device["spatial"]["placements"]
	assert len(placements) == 1, device["id"]
	return placements[0]


class IdentityTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)

	def test_machine_identity_uses_the_physical_year_not_the_parent_driver_year(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(MACHINE_ID, machine["id"])
		self.assertEqual("Stern", machine["manufacturer"])
		self.assertEqual("Pirates of the Caribbean", machine["name"])
		self.assertEqual(2006, machine["year"], "the physical machine is 2006; potc_600af's own 2008 year belongs on that driver only")
		self.assertEqual("physical_pinball", machine["kind"])
		self.assertNotIn("ipdb_id", machine, "IPDB was unreachable during curation; the id must not be guessed")

	def test_machine_id_manufacturer_segment_matches_its_directory(self) -> None:
		self.assertEqual("stern", MACHINE_ID.split(".")[0])
		self.assertEqual("stern", DEFINITION_PATH.parent.name)
		self.assertEqual("stern", SEED_PATH.parent.name)
		self.assertEqual("stern", KNOWLEDGE_PATH.parent.name)
		self.assertEqual("stern", SPATIAL_REPORT_PATH.parent.name)

	def test_playfield_uses_this_table_s_own_bounds(self) -> None:
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual(PLAYFIELD_WIDTH, playfield["width"])
		self.assertEqual(PLAYFIELD_HEIGHT, playfield["height"], "this table is 2155 units tall, not the 2162 most WPC tables use")
		self.assertEqual("vpx", playfield["units"])

	def test_every_potc_driver_is_enumerated_exactly_once(self) -> None:
		drivers = self.definition["drivers"]
		ids = [driver["id"] for driver in drivers]
		self.assertEqual(len(ids), len(set(ids)))
		self.assertEqual(1 + CLONE_DRIVER_COUNT, len(ids))
		parents = [driver for driver in drivers if "clone_of" not in driver]
		self.assertEqual([PARENT_DRIVER], [driver["id"] for driver in parents])
		for driver in drivers:
			if driver["id"] != PARENT_DRIVER:
				self.assertEqual(PARENT_DRIVER, driver["clone_of"], driver["id"])
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertEqual("Stern", driver["manufacturer"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])

	def test_the_unrelated_stern_sam_prefixes_are_absent(self) -> None:
		"""PinMAME short-name prefixes are not machine identity; nothing outside potc_* belongs here."""
		for driver in self.definition["drivers"]:
			self.assertTrue(driver["id"].startswith("potc_"), driver["id"])

	def test_controller_platform_is_the_sam_profile_at_the_sam_generation_bit(self) -> None:
		controller = self.definition["controller"]
		self.assertEqual("pinmame.sam", controller["platform"])
		self.assertEqual("0x100000000000", controller["hardware_generation"], "PINMAME_HARDWARE_GEN_SAM")
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.sam", profile["id"])

	def test_definition_and_seed_are_byte_identical(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_no_author_ready_artifact(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists(), "this record is partial and must not have an author-ready twin")

	def test_the_superseded_stub_and_its_knowledge_note_are_pruned(self) -> None:
		"""Both must be gone once this definition claims the potc_* clone-tree root.

		Inside the curation worktree this asserted the opposite, and correctly so: that worktree does
		not regenerate the shared catalog, and deleting the stub there would have left
		catalog/pinmame.json pointing at a missing file. rebuild_catalog prunes the stub definition
		and its knowledge note centrally on merge, so post-integration their absence is the invariant
		- if either reappears, one physical machine is represented twice.
		"""
		self.assertFalse(SUPERSEDED_STUB_PATH.is_file(), f"{SUPERSEDED_STUB_PATH} was not pruned")
		self.assertFalse(
			SUPERSEDED_STUB_KNOWLEDGE_PATH.is_file(),
			f"{SUPERSEDED_STUB_KNOWLEDGE_PATH} was not pruned",
		)

	def test_knowledge_note_exists_and_is_referenced(self) -> None:
		self.assertEqual("knowledge/stern/pirates-of-the-caribbean-2006.md", self.definition["knowledge"]["path"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())


class CoverageTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)

	def test_coverage_is_honestly_partial(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(
			["polarity", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
			coverage["missing"],
		)
		self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
		self.assertEqual("observed", coverage["dimensions"]["recreation_knowledge"])
		self.assertEqual(2, self.definition["schema_version"])

	def test_unresolved_conflicts_are_declared_and_non_empty(self) -> None:
		conflicts = self.definition["conflicts"]
		self.assertEqual(EXPECTED_CONFLICT_IDS, {conflict["id"] for conflict in conflicts})
		for conflict in conflicts:
			self.assertGreaterEqual(len(conflict["source_refs"]), 2, conflict["id"])
			self.assertGreater(len(conflict["description"]), 400, conflict["id"])

	def test_promotion_gate_refuses_author_ready_while_conflicts_remain(self) -> None:
		self.assertNotEqual("author_ready", self.definition["coverage"]["status"])
		self.assertTrue(self.definition["conflicts"])
		self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])


class AddressEnumerationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_switch_address_space_is_complete_and_skips_the_dead_column(self) -> None:
		expected = SERVICE_SWITCH_ADDRESSES | MATRIX_ADDRESSES | DEDICATED_SWITCH_ADDRESSES | FLIPPER_SWITCH_ADDRESSES
		self.assertEqual(expected, set(self.switches))
		for address in range(73, 81):
			self.assertNotIn(
				address,
				self.switches,
				"public 73-80 is swMatrix[10], which Stern S.A.M. never writes, and the profile's address rules exclude it",
			)

	def test_dip_bank_is_the_full_eight_positions(self) -> None:
		self.assertEqual(set(range(1, 9)), set(self.dips))
		for device in self.dips.values():
			self.assertEqual("dip_switch", device["kind"])
			self.assertEqual("dip_switch", device["spatial"]["reason"])

	def test_solenoid_address_space_covers_one_to_sixty_six(self) -> None:
		self.assertEqual(set(range(1, 67)), set(self.solenoids))

	def test_lamp_address_space_covers_one_to_eighty(self) -> None:
		self.assertEqual(LAMP_ADDRESSES, set(self.lamps))

	def test_general_illumination_is_a_single_aggregate_channel(self) -> None:
		self.assertEqual({0}, set(self.gi))

	def test_every_address_carries_a_semantic_disposition(self) -> None:
		for device in list(self.switches.values()) + list(self.solenoids.values()) + list(self.lamps.values()) + list(self.gi.values()):
			self.assertIn(device["availability"], {"used", "unused", "optional"}, device["id"])
			self.assertTrue(device["label"].strip(), device["id"])

	def test_printed_not_used_matrix_positions_stay_unused(self) -> None:
		for address in UNUSED_MATRIX_ADDRESSES:
			device = self.switches[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("unused", device["spatial"]["reason"], address)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_unfitted_solenoid_circuits_are_enumerated_but_not_created(self) -> None:
		for address in UNFITTED_SOLENOID_ADDRESSES:
			device = self.solenoids[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("unused", device["spatial"]["reason"], address)
			self.assertIn("populated", device["physical"]["notes"], address)
			self.assertNotIn("part_number", device["physical"], address)

	def test_the_flipper_column_upper_bits_are_recorded_unreachable(self) -> None:
		for address in UNREACHABLE_FLIPPER_SWITCHES:
			device = self.switches[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertIn("locals.flipMask", device["physical"]["notes"], address)
		for address in FLIPPER_SWITCH_ADDRESSES - UNREACHABLE_FLIPPER_SWITCHES:
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_flippers_are_ordinary_solenoids_fifteen_and_sixteen(self) -> None:
		self.assertEqual("Left Flipper", self.solenoids[15]["label"])
		self.assertEqual("Right Flipper", self.solenoids[16]["label"])
		for address in (45, 46, 47, 48):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"], address)
			self.assertEqual("unused", device["availability"], address)

	def test_game_on_address_matches_the_project_wide_sam_convention(self) -> None:
		"""tests/test_validation.py and the author-ready validator both require kind "virtual" here."""
		game_on = self.solenoids[GAME_ON_SOLENOID]
		self.assertEqual("virtual", game_on["kind"])
		self.assertEqual("used", game_on["availability"])
		self.assertNotIn("wiring", game_on, "the synthetic game-on state has no physical wiring")
		for address in VIRTUAL_SOLENOID_ADDRESSES - {GAME_ON_SOLENOID}:
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_auxiliary_solenoid_range_is_enumerated_but_unfitted(self) -> None:
		for address in AUX_SOLENOID_ADDRESSES:
			device = self.solenoids[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertIn("SAM_NO_AUX", device["physical"]["notes"], address)

	def test_printed_flashers_are_exactly_the_five_the_manual_and_pinmame_agree_on(self) -> None:
		actual = {
			address for address, device in self.solenoids.items()
			if device["kind"] == "flasher"
		}
		self.assertEqual(FLASHER_ADDRESSES, actual)

	def test_start_and_tournament_start_sit_inside_the_matrix_range(self) -> None:
		self.assertEqual("Tournament Start", self.switches[15]["label"])
		self.assertEqual("Start Button", self.switches[16]["label"])
		for address in CABINET_MATRIX_ADDRESSES:
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"], address)


class PolarityTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")

	def test_the_manual_identified_optos_are_exactly_the_swept_set(self) -> None:
		actual = {
			address for address, device in self.switches.items()
			if device.get("physical", {}).get("switch_type") == "opto"
		}
		self.assertEqual(MANUAL_OPTO_ADDRESSES, actual)

	def test_no_switch_claims_a_polarity_pinned_sam_source_cannot_supply(self) -> None:
		"""Stern S.A.M. populates no inverted-switch mask, so normally_closed must stay unasserted."""
		for address, device in self.switches.items():
			self.assertNotIn("normally_closed", device, address)

	def test_every_opto_discloses_the_platform_wide_normalization_gap(self) -> None:
		for address in MANUAL_OPTO_ADDRESSES:
			notes = self.switches[address]["physical"]["notes"]
			self.assertIn("conflict.sam-invsw-never-populated", notes, address)

	def test_polarity_is_named_in_coverage_missing(self) -> None:
		self.assertIn("polarity", self.definition["coverage"]["missing"])


class SpatialTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")
		cls.report = load_json(SPATIAL_REPORT_PATH)

	def test_every_placement_is_in_range_with_at_most_six_decimals(self) -> None:
		seen = 0
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if spatial is None or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				seen += 1
				self.assertEqual("playfield", placement["space"])
				self.assertGreaterEqual(placement["x"], 0.0)
				self.assertLessEqual(placement["x"], 1.0)
				self.assertGreaterEqual(placement["y"], 0.0)
				self.assertLessEqual(placement["y"], 1.0)
				for axis in ("x", "y"):
					text = repr(placement[axis])
					if "." in text:
						self.assertLessEqual(len(text.split(".")[1]), 6, placement["id"])
		self.assertGreater(seen, 100, "the spatial set would pass vacuously")

	def test_placement_identifiers_are_unique(self) -> None:
		identifiers: list[str] = []
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if spatial and spatial["status"] != "not_applicable":
				identifiers += [placement["id"] for placement in spatial["placements"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_lamp_placement_count_equals_the_printed_bulb_quantity(self) -> None:
		for address, device in self.lamps.items():
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable":
				continue
			quantity = device["physical"].get("quantity", 1)
			self.assertEqual(quantity, len(spatial["placements"]), f"lamp {address}")

	def test_back_panel_and_cabinet_lamps_get_no_playfield_coordinate(self) -> None:
		for address in BACK_PANEL_LAMPS | CABINET_LAMPS:
			spatial = self.lamps[address]["spatial"]
			self.assertEqual("not_applicable", spatial["status"], address)
			self.assertEqual("cabinet_or_service", spatial["reason"], address)
		for address in LAMP_ADDRESSES - BACK_PANEL_LAMPS - CABINET_LAMPS:
			self.assertEqual("validated", self.lamps[address]["spatial"]["status"], address)

	def test_rear_center_flasher_is_a_backbox_device_with_two_bulbs(self) -> None:
		device = self.solenoids[22]
		self.assertEqual(2, device["physical"]["quantity"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("cabinet_or_service", device["spatial"]["reason"])

	def test_the_two_unresolved_addresses_omit_spatial_entirely(self) -> None:
		"""The schema has no 'unresolved' spatial status, so omitting the key is the honest form."""
		self.assertNotIn("spatial", self.solenoids[30])
		self.assertNotIn("spatial", self.gi[0])
		self.assertEqual(3, self.solenoids[30]["physical"]["quantity"])
		self.assertEqual(
			[
				{"address": 30, "group": "pinmame.output.solenoid"},
				{"address": 0, "group": "pinmame.output.gi"},
			],
			self.report["unresolved"],
		)

	def test_every_other_device_has_a_spatial_disposition(self) -> None:
		allowed_without = {("pinmame.output.solenoid", 30), ("pinmame.output.gi", 0)}
		for device in self.definition["inputs"] + self.definition["outputs"]:
			key = (device["binding"]["group"], device["binding"]["device"])
			if key in allowed_without:
				continue
			self.assertIn("spatial", device, device["id"])

	def test_spatial_report_matches_the_definition(self) -> None:
		self.assertEqual(MACHINE_ID, self.report["machine_id"])
		self.assertEqual("partial", self.report["status"])
		self.assertTrue(self.report["blockers"])
		bounds = self.report["coordinate_convention"]["source_bounds"]
		self.assertEqual({"left": 0.0, "top": 0.0, "right": PLAYFIELD_WIDTH, "bottom": PLAYFIELD_HEIGHT}, bounds)
		self.assertTrue(SPATIAL_REPORT_MARKDOWN_PATH.is_file())

	def test_every_projection_is_declared_in_the_report(self) -> None:
		projections = {(entry["group"], entry["address"]) for entry in self.report["projections"]}
		for address in (18, 19, 20, 21, 22, 62, 63, 81, 83):
			self.assertIn(("pinmame.input.switch", address), projections, address)
		for address in (5, 21, 27, 28):
			self.assertIn(("pinmame.output.solenoid", address), projections, address)
		for entry in self.report["projections"]:
			self.assertGreater(len(entry["reason"]), 60, entry)


class GeometricOrderingTests(unittest.TestCase):
	"""Cheap ordering assertions. These are what catch a reversed left/right identity."""

	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def _x(self, table: dict[int, dict], address: int) -> float:
		return only_placement(table[address])["x"]

	def _y(self, table: dict[int, dict], address: int) -> float:
		return only_placement(table[address])["y"]

	def test_left_and_right_switch_pairs_ascend_in_x(self) -> None:
		pairs = (
			(1, 2, "Left Lane / Right Lane"),
			(8, 58, "Left Orbit / Right Orbit"),
			(24, 29, "Left Outlane / Right Outlane"),
			(25, 28, "Left Inlane / Right Inlane"),
			(26, 27, "Left Sling / Right Sling"),
			(37, 39, "L. Bonus Treasure / R. Bonus Treasure"),
		)
		for left, right, label in pairs:
			self.assertLess(self._x(self.switches, left), self._x(self.switches, right), label)

	def test_outlanes_sit_outboard_of_their_inlanes(self) -> None:
		self.assertLess(self._x(self.switches, 24), self._x(self.switches, 25), "left outlane outboard of left inlane")
		self.assertGreater(self._x(self.switches, 29), self._x(self.switches, 28), "right outlane outboard of right inlane")

	def test_top_lanes_ascend_left_to_middle_to_right(self) -> None:
		self.assertLess(self._x(self.switches, 12), self._x(self.switches, 13))
		self.assertLess(self._x(self.switches, 13), self._x(self.switches, 14))

	def test_pirate_targets_one_to_six_ascend_left_to_right(self) -> None:
		xs = [self._x(self.switches, address) for address in range(50, 56)]
		self.assertEqual(xs, sorted(xs), "Pirate 1 is printed (LEFT) and Pirate 6 (RIGHT)")

	def test_pirate_lamps_track_the_pirate_switches(self) -> None:
		"""Lamps 49-53 and 41 are PIRATE 1-6; they must run left to right like switches 50-55."""
		lamp_addresses = [49, 50, 51, 52, 53, 41]
		xs = [self._x(self.lamps, address) for address in lamp_addresses]
		self.assertEqual(xs, sorted(xs))
		for lamp_address, switch_address in zip(lamp_addresses, range(50, 56)):
			self.assertLess(
				abs(self._x(self.lamps, lamp_address) - self._x(self.switches, switch_address)),
				0.09,
				f"lamp {lamp_address} should sit near switch {switch_address}",
			)

	def test_heart_letters_ascend_left_to_right(self) -> None:
		xs = [self._x(self.lamps, address) for address in (24, 32, 40, 48, 56)]
		self.assertEqual(xs, sorted(xs), "H, E, A, R, T on board 520-5258-00")

	def test_jack_and_key_letter_sets_ascend(self) -> None:
		key = [self._x(self.lamps, address) for address in (62, 63, 55)]
		self.assertEqual(key, sorted(key), "(K)EY, K(E)Y, KE(Y)")

	def test_lane_lamps_track_their_lane_switches(self) -> None:
		pairs = ((4, 24), (5, 25), (6, 28), (7, 29))
		for lamp_address, switch_address in pairs:
			self.assertLess(
				abs(self._x(self.lamps, lamp_address) - self._x(self.switches, switch_address)),
				0.09,
				f"lamp {lamp_address} should sit near switch {switch_address}",
			)

	def test_flippers_are_near_the_apron_and_ordered_left_to_right(self) -> None:
		left = only_placement(self.solenoids[15])
		right = only_placement(self.solenoids[16])
		self.assertLess(left["x"], right["x"])
		for placement in (left, right):
			self.assertGreater(placement["y"], 0.75, "flippers sit toward the front of the playfield")

	def test_the_trough_is_at_the_front_and_the_top_lanes_at_the_rear(self) -> None:
		for address in (18, 19, 20, 21, 22):
			self.assertGreater(self._y(self.switches, address), 0.75, address)
		for address in (12, 13, 14):
			self.assertLess(self._y(self.switches, address), 0.25, address)

	def test_pop_bumper_naming_follows_the_manual_not_the_script_object_order(self) -> None:
		"""Left is the leftmost of the trio, right the rightmost, bottom the player-nearest."""
		for table in (self.switches, self.solenoids):
			left, right, bottom = (30, 31, 32) if table is self.switches else (9, 10, 11)
			xs = {name: self._x(table, address) for name, address in (("left", left), ("right", right), ("bottom", bottom))}
			ys = {name: self._y(table, address) for name, address in (("left", left), ("right", right), ("bottom", bottom))}
			self.assertLess(xs["left"], xs["bottom"])
			self.assertLess(xs["bottom"], xs["right"])
			self.assertGreater(ys["bottom"], ys["left"])
			self.assertGreater(ys["bottom"], ys["right"])

	def test_the_bumper_switch_and_coil_for_one_bumper_share_a_position(self) -> None:
		for switch_address, solenoid_address in ((30, 9), (31, 10), (32, 11)):
			self.assertEqual(
				(self._x(self.switches, switch_address), self._y(self.switches, switch_address)),
				(self._x(self.solenoids, solenoid_address), self._y(self.solenoids, solenoid_address)),
			)

	def test_back_left_and_back_right_flashers_are_on_opposite_sides(self) -> None:
		self.assertLess(self._x(self.solenoids, 31), 0.35, "Flash: Back Left")


class MechanismTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.mechanisms = {mechanism["id"]: mechanism for mechanism in cls.definition["mechanisms"]}
		cls.device_ids = {device["id"] for device in cls.definition["inputs"] + cls.definition["outputs"]}

	def test_expected_mechanisms_are_present(self) -> None:
		self.assertEqual(
			{
				"mech.auto-launch",
				"mech.ball-trough",
				"mech.black-pearl-ship",
				"mech.plunder-disc",
				"mech.pop-bumper-eject",
				"mech.top-center-vuk",
				"mech.treasure-chest",
			},
			set(self.mechanisms),
		)

	def test_every_actuator_and_sensor_resolves_to_a_declared_device(self) -> None:
		for mechanism in self.mechanisms.values():
			for identifier in mechanism["actuators"] + mechanism["sensors"]:
				self.assertIn(identifier, self.device_ids, f"{mechanism['id']} -> {identifier}")
			for position in mechanism.get("positions", []):
				for identifier in position["sensors"]:
					self.assertIn(identifier, self.device_ids, f"{mechanism['id']} -> {identifier}")

	def test_the_ship_reports_three_states_not_a_continuous_position(self) -> None:
		ship = self.mechanisms["mech.black-pearl-ship"]
		self.assertEqual("motorized", ship["kind"])
		positions = {position["id"]: position for position in ship["positions"]}
		self.assertEqual({"ship.home", "ship.travelling", "ship.fully-sunk"}, set(positions))
		self.assertEqual(["switch.matrix-63"], positions["ship.home"]["sensors"])
		self.assertEqual(["switch.matrix-62"], positions["ship.fully-sunk"]["sensors"])
		self.assertEqual([], positions["ship.travelling"]["sensors"], "no sensor reports intermediate travel")

	def test_the_ship_motor_direction_is_a_relay_not_the_motor_output(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		relay = relationships["rel.ship-motor-direction-relay"]
		self.assertEqual("relay_gated", relay["kind"])
		self.assertEqual("solenoid.27", relay["source"])
		self.assertEqual("solenoid.21", relay["destination"])

	def test_the_ship_home_switch_declares_its_startup_state(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertTrue(switches[63]["initial_active"])
		self.assertNotIn("initial_active", switches[62])

	def test_the_plunder_disc_has_no_position_sensor(self) -> None:
		disc = self.mechanisms["mech.plunder-disc"]
		self.assertEqual("rotary", disc["kind"])
		self.assertIn("solenoid.6", disc["actuators"])
		self.assertIn("no position sensor", disc["behavior"])
		self.assertEqual([], disc.get("positions", []))

	def test_no_mechanism_claims_a_coil_actuates_a_switch_directly(self) -> None:
		"""Only the ship's direction relay is a declared causal relationship; the rest is ball-mediated."""
		self.assertEqual(1, len(self.definition["relationships"]))


class ProvenanceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def test_every_provenance_reference_resolves(self) -> None:
		def walk(node) -> None:
			if isinstance(node, dict):
				if set(node) == {"status", "source_refs"}:
					for reference in node["source_refs"]:
						self.assertIn(reference, self.sources, reference)
				for value in node.values():
					walk(value)
			elif isinstance(node, list):
				for value in node:
					walk(value)

		walk({key: value for key, value in self.definition.items() if key != "sources"})

	def test_manual_and_table_sources_carry_licence_and_attribution(self) -> None:
		for identifier, source in self.sources.items():
			if source["kind"] in {"manual", "vpx_script", "vpx_table"}:
				self.assertIn("license", source, identifier)
				self.assertIn("attribution", source, identifier)

	def test_retained_artifact_hashes_are_pinned(self) -> None:
		self.assertEqual(
			"faa493698371d4e6d2d821c9f6489ce780d50cfd92c5a0ed71c50a99df1875be",
			self.sources["manual.stern.pirates-of-the-caribbean.2006"]["sha256"],
		)
		self.assertEqual(
			"d69fea24ad8d1dd4fc49c84214e71b448d6a602b6ef768a329a55a94f15aad59",
			self.sources["vpx-table.potc-stern-2006"]["sha256"],
		)
		self.assertEqual(
			"fb6cec754fc907f1fbb41f1f71273d6585db73365073b3a18cfe2c12d90c39e3",
			self.sources["vpx-script.potc-stern-2006"]["sha256"],
		)
		self.assertTrue(self.sources["vpx-script.potc-stern-2006"]["known_working"])

	def test_the_manual_source_carries_every_transcribed_region(self) -> None:
		excerpts = {excerpt["id"] for excerpt in self.sources["manual.stern.pirates-of-the-caribbean.2006"]["excerpts"]}
		self.assertEqual(
			{
				"excerpt.potc.switch-matrix",
				"excerpt.potc.dedicated-switches",
				"excerpt.potc.lamp-matrix",
				"excerpt.potc.coils-detailed-chart",
				"excerpt.potc.back-panel-lamp-locations",
				"excerpt.potc.back-panel-assembly",
			},
			excerpts,
		)

	def test_every_excerpt_transcription_lives_under_this_machine_s_directory(self) -> None:
		for excerpt in self.sources["manual.stern.pirates-of-the-caribbean.2006"]["excerpts"]:
			self.assertTrue(excerpt["path"].startswith("evidence/excerpts/stern.pirates-of-the-caribbean.2006/"), excerpt["id"])
			self.assertTrue((ROOT / excerpt["path"]).is_file(), excerpt["path"])
			self.assertEqual("manual", excerpt["method"], excerpt["id"])
			self.assertTrue(excerpt["reviewed"], excerpt["id"])

	def test_the_excerpt_directory_has_no_uncited_files(self) -> None:
		cited = set()
		for excerpt in self.sources["manual.stern.pirates-of-the-caribbean.2006"]["excerpts"]:
			for field in ("path", "image"):
				if excerpt.get(field):
					cited.add((ROOT / excerpt[field]).resolve())
		on_disk = {path.resolve() for path in EXCERPT_ROOT.rglob("*") if path.is_file()}
		self.assertEqual(set(), on_disk - cited)

	def test_the_switch_matrix_excerpt_transcribes_every_printed_cell(self) -> None:
		text = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
		for address in MATRIX_ADDRESSES:
			self.assertIn(f"SW. #{address} ", text + " ", address)
		self.assertIn("shaded-cell opto legend", text)

	def test_the_lamp_matrix_excerpt_transcribes_every_printed_cell(self) -> None:
		text = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
		for address in LAMP_ADDRESSES:
			self.assertIn(f"LP. #{address} ", text + " ", address)

	def test_the_coils_excerpt_transcribes_every_printed_row(self) -> None:
		text = (EXCERPT_ROOT / "coils-detailed-chart.md").read_text(encoding="utf-8")
		for address in PRINTED_SOLENOID_ADDRESSES:
			self.assertIn(f"| #{address} |", text, address)


class CuratorDeterminismTests(unittest.TestCase):
	def test_curator_reproduces_every_artifact_byte_for_byte(self) -> None:
		import curate_pirates_of_the_caribbean as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_refuses_to_run_without_a_mode(self) -> None:
		import curate_pirates_of_the_caribbean as curator

		argv = sys.argv
		sys.argv = ["curate_pirates_of_the_caribbean.py"]
		try:
			with self.assertRaises(SystemExit):
				curator.main()
		finally:
			sys.argv = argv

	def test_curator_data_tables_agree_with_the_generated_definition(self) -> None:
		import curate_pirates_of_the_caribbean as curator

		self.assertEqual(28, len(curator.DRIVER_IDS))
		self.assertEqual(set(range(1, 65)), set(curator.SWITCH_MATRIX))
		self.assertEqual(set(range(1, 33)), set(curator.SOLENOIDS))
		self.assertEqual(set(range(1, 81)), set(curator.LAMPS))
		self.assertEqual(MANUAL_OPTO_ADDRESSES, set(curator.OPTO_SWITCHES))
		self.assertEqual(FLASHER_ADDRESSES, set(curator.FLASHER_ADDRESSES))
		self.assertEqual(BACK_PANEL_LAMPS, set(curator.BACK_PANEL_LAMPS))


class RetainedExtractionTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest(self) -> None:
		import curate_pirates_of_the_caribbean as curator

		root = curator.configured_vpx_sources_root(required=False)
		if root is None:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		if not (root / curator.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("the retained Pirates of the Caribbean extraction is not present")
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_review_artifacts_match_their_recorded_digests(self) -> None:
		import hashlib

		import curate_pirates_of_the_caribbean as curator

		value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not value:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		root = Path(value).expanduser().resolve() / "pirates-of-the-caribbean-2006"
		if not root.is_dir():
			self.skipTest("the retained Pirates of the Caribbean review artifacts are not present")
		for name, expected in (
			("manual-transcription.md", curator.MANUAL_TRANSCRIPTION_SHA256),
			("vpx-geometry.txt", curator.VPX_GEOMETRY_SHA256),
		):
			path = root / name
			self.assertTrue(path.is_file(), path)
			self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest(), name)


if __name__ == "__main__":
	unittest.main()
