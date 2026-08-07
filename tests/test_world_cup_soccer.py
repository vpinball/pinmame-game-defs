from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "midway" / "world-cup-soccer-1994.json"
SEED_PATH = ROOT / "tools" / "seeds" / "midway" / "world-cup-soccer-1994.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "midway" / "world-cup-soccer-1994.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "midway" / "world-cup-soccer-1994.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-security.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "midway" / "world-cup-soccer-1994.json"

DRIVER_IDS = {
	"wcs_l2", "wcs_l3c", "wcs_la2", "wcs_l1", "wcs_la1", "wcs_d2",
	"wcs_p2", "wcs_p5", "wcs_p3", "wcs_p6",
	"wcs_f10", "wcs_f50", "wcs_f62", "wcs_f62b",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 46, 57, 58, 68, 73}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 45, 51, 52, 53}


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
	import curate_world_cup_soccer as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_world_cup_soccer.py"]
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


class WorldCupSoccerDefinitionTests(unittest.TestCase):
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
		self.assertEqual("midway.world-cup-soccer.1994", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2361, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1994, self.definition["machine"]["year"])
		self.assertEqual("Bally", self.definition["machine"]["manufacturer"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertEqual("0x20", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_wcs_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for freewpc in ("wcs_f10", "wcs_f50", "wcs_f62", "wcs_f62b"):
			self.assertEqual("compatible", by_id[freewpc]["physical_compatibility"])
			self.assertEqual("wcs_l2", by_id[freewpc]["clone_of"])
		self.assertNotIn("clone_of", by_id["wcs_l2"])

	def test_the_full_wpc_security_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_pinmame_with_zero_disagreement_in_the_ordinary_matrix(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_wcs_game_data_inverted_switch_mask_is_re_derived_in_code(self) -> None:
		import curate_world_cup_soccer as curator

		# Column index is the array index (0=coin/dedicated .. 11=Fliptronic); this is re-derived by
		# bit position, not hand-copied, so a transcription slip cannot silently survive.
		mask = (0x00, 0x00, 0x00, 0x3f, 0x1f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		normalized_by_column = {
			3: {31 + row for row in range(6) if (mask[3] >> row) & 1},
			4: {41 + row for row in range(5) if (mask[4] >> row) & 1},
			5: {51 + row for row in range(3) if (mask[5] >> row) & 1},
		}
		expected = set().union(*normalized_by_column.values())
		self.assertEqual(expected, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		self.assertEqual(0x00, mask[11], "the Fliptronic column must stay unnormalized")
		for address in (112, 114):
			self.assertNotIn(address, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)

	def test_flipper_positions_and_cabinet_opto_conflict(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertEqual("not_applicable", self.switches[112]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[112]["spatial"]["reason"])
		self.assertEqual("internal_nonvisual", self.switches[111]["spatial"]["reason"])

	def test_the_flipper_cabinet_opto_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual(
			{
				"conflict.flipper-cabinet-opto-not-normalized",
				"conflict.jet-bumper-script-binding-vs-physical-position",
			},
			set(conflicts),
		)
		conflict = conflicts["conflict.flipper-cabinet-opto-not-normalized"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("unresolved", description)
		self.assertIn("harness", description)
		for address in (112, 114):
			self.assertIn(str(address), conflict["path"])

	def test_the_full_wpc_security_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 52))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in (17, 18, 19, 20, 22, 25, 26, 27, 28):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (21, 23, 24):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in range(37, 45):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in (49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_the_lower_flipper_solenoids_carry_the_manuals_own_printed_numbers_unchanged(self) -> None:
		# Unlike WPC-95, WPC-Security has no LPDC board, so the printed circuit numbers already
		# equal the public addresses -- no manual.address remap is expected here.
		for address in (45, 46, 47, 48):
			manual_aliases = {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			self.assertEqual({f"{address:02d}"}, manual_aliases, address)
			self.assertEqual("coil", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])

	def test_solenoid_36_is_unfitted_and_none_is_mislabelled(self) -> None:
		self.assertEqual("unused", self.solenoids[36]["availability"])
		self.assertEqual("unused", self.solenoids[36]["spatial"]["reason"])
		# The manual genuinely fits a knocker on this machine (unlike some other WPC-era games in
		# this project), so it must be present, fitted, and cabinet-mounted -- not absent.
		self.assertEqual("used", self.solenoids[7]["availability"])
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])
		self.assertIn("knocker", self.solenoids[7]["label"].lower())
		# Solenoid 4 (Lock Release) must NOT be flagged unfitted -- an early transcription error
		# briefly claimed it had no table row; the corrected manual reading has it fully populated.
		self.assertEqual("used", self.solenoids[4]["availability"])
		self.assertEqual("validated", self.solenoids[4]["spatial"]["status"])

	def test_solenoid_34_has_no_spatial_key_and_is_named_in_the_spatial_report(self) -> None:
		self.assertEqual("used", self.solenoids[34]["availability"])
		self.assertNotIn("spatial", self.solenoids[34])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(
			[{"group": "pinmame.output.solenoid", "address": 34, "reason": "no_evidence"}],
			report["unresolved"],
		)
		self.assertEqual([{"group": "pinmame.output.solenoid", "address": 34}], report["no_spatial_key_outputs"])

	def test_solenoid_51_is_a_virtual_mirror_not_a_fourth_diverter_device(self) -> None:
		self.assertEqual("virtual", self.solenoids[51]["kind"])
		self.assertEqual("used", self.solenoids[51]["availability"])
		self.assertEqual(["internal.duplicate.mirror"], self.solenoids[51]["roles"])
		self.assertEqual("not_applicable", self.solenoids[51]["spatial"]["status"])
		self.assertEqual("virtual", self.solenoids[51]["spatial"]["reason"])

	def test_gi_playfield_strings_are_located_and_insert_panel_strings_are_cabinet(self) -> None:
		for address in (0, 1, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(11, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(22, len(self.gi[4]["spatial"]["placements"]))
		for address in (2, 3):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_gi_top_clamped_placements_stay_in_range(self) -> None:
		for placement in self.gi[4]["spatial"]["placements"]:
			self.assertGreaterEqual(placement["y"], 0.0)
			self.assertLessEqual(placement["y"], 1.0)
		zero_y = [p for p in self.gi[4]["spatial"]["placements"] if p["y"] == 0.0]
		self.assertEqual(3, len(zero_y))

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		for address in (46, 47, 71, 78):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in sorted(MATRIX_ADDRESSES - {46, 47, 71, 78, 87, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (87, 88):
			self.assertEqual("used", self.lamps[address]["availability"], address)
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual('Chicago "P"', self.lamps[11]["label"])
		self.assertEqual("Start Button", self.lamps[88]["label"])

	def test_no_lamp_is_marked_not_used(self) -> None:
		for address in MATRIX_ADDRESSES:
			self.assertEqual("used", self.lamps[address]["availability"], address)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device.get("spatial")
			if spatial is None:
				continue
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
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		lamp_y = {addr: pos[1] for addr, pos in _emitter_positions(self.lamps).items()}

		# Jet bumpers: Bumper2 (switch 81, printed "Left") sits to the right of Bumper3 (switch 83,
		# printed "Lower"), on the reading that the manual's naming is relative to the cluster, not
		# absolute cabinet left/right -- asserted here so it is never "corrected" silently.
		#
		# That reading is DISPUTED as of 2026-08-08 and the disagreement is recorded as
		# conflict.jet-bumper-script-binding-vs-physical-position. A review read the two location
		# diagrams as putting 81 leftmost, which would rotate all six placements; an independent
		# 400 dpi re-render of printed 2-49 could not confirm it. These assertions therefore pin the
		# CURRENT values, not a settled fact. If the conflict is resolved in favour of the review,
		# both the assertions below and the curator's coordinates change together.
		self.assertGreater(switch_x[81], switch_x[83])
		self.assertGreater(switch_x[82], switch_x[83])

		# Trough kickers descend in x from Trough 1 (nearest eject) to Trough 5 (nearest drain),
		# and ascend in y (moving further from the top of the table) in the same order.
		self.assertGreater(switch_x[31], switch_x[32])
		self.assertGreater(switch_x[32], switch_x[33])
		self.assertGreater(switch_x[33], switch_x[34])
		self.assertGreater(switch_x[34], switch_x[35])
		self.assertLess(switch_y[31], switch_y[32])
		self.assertLess(switch_y[32], switch_y[33])
		self.assertLess(switch_y[33], switch_y[34])
		self.assertLess(switch_y[34], switch_y[35])

		# Left/right slingshots stay on their printed sides.
		self.assertLess(switch_x[84], 0.5)
		self.assertGreater(switch_x[85], 0.5)

		# Upper left/right lanes ascend left -> right for both switches and lamps.
		self.assertLess(switch_x[87], switch_x[88])
		self.assertLess(lamp_x[66], lamp_x[67])

		# Rollovers 1 (High) through 4 (Low) ascend in both x and y together (a single arc).
		self.assertLess(switch_x[61], switch_x[62])
		self.assertLess(switch_x[62], switch_x[63])
		self.assertLess(switch_x[63], switch_x[64])
		self.assertLess(switch_y[61], switch_y[62])
		self.assertLess(switch_y[62], switch_y[63])
		self.assertLess(switch_y[63], switch_y[64])

		# Skill shot lane: Front (nearest the player/apron) has the largest y; Rear (deepest into
		# the playfield) has the smallest, descending in that printed order.
		self.assertGreater(switch_y[51], switch_y[52])
		self.assertGreater(switch_y[52], switch_y[53])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.skill-shot",
				"mechanism.goalie", "mechanism.spinning-ball", "mechanism.magna-goalie",
				"mechanism.lock-magnet", "mechanism.ramp-lock-post", "mechanism.ramp-diverter",
				"mechanism.loop-gate", "mechanism.goal-tv-poppers", "mechanism.eject-holes",
				"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.kickback",
				"mechanism.knocker", "mechanism.lower-flippers",
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
		self.assertIn("35-segment", mechanisms["mechanism.goalie"]["behavior"])
		self.assertIn("MECH_LINEAR|MECH_REVERSE|MECH_ONESOL", mechanisms["mechanism.goalie"]["behavior"])
		self.assertNotIn("positions", mechanisms["mechanism.loop-gate"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-eject-stack-pulse"}, set(relationships))
		self.assertEqual("switch.matrix-36", relationships["relationship.trough-eject-stack-pulse"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-eject-stack-pulse"]["kind"])

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
		self.assertIn("vpx-script.wcs-vpw-1-5", sources)
		self.assertTrue(sources["vpx-script.wcs-vpw-1-5"]["known_working"])
		self.assertEqual(
			"c18cfbaa4e8c3b67259ac5d6c7b6842dfdaaf308b0fd71a64071118b57ac73c5",
			sources["vpx-script.wcs-vpw-1-5"]["sha256"],
		)
		self.assertEqual(
			"ab7e07fce7b589f9732f458a7a09ad08b87237852d97d7b5bf9a74f6b0f6d23d",
			sources["vpx-table.wcs-vpw-1-5"]["sha256"],
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

	def test_manual_source_carries_every_expected_excerpt(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.midway.world-cup-soccer.1994"]
		excerpt_ids = {excerpt["id"] for excerpt in manual["excerpts"]}
		self.assertEqual(
			{
				"excerpt.world-cup-soccer.switch-matrix",
				"excerpt.world-cup-soccer.switch-locations",
				"excerpt.world-cup-soccer.lamp-matrix",
				"excerpt.world-cup-soccer.lamp-locations",
				"excerpt.world-cup-soccer.solenoid-flasher-wiring",
				"excerpt.world-cup-soccer.solenoid-flasher-locations",
				"excerpt.world-cup-soccer.general-illumination",
				"excerpt.world-cup-soccer.boards-and-assemblies",
			},
			excerpt_ids,
		)
		for excerpt in manual["excerpts"]:
			self.assertTrue(excerpt["reviewed"], excerpt["id"])
			self.assertEqual("manual", excerpt["method"], excerpt["id"])
		matrix = next(e for e in manual["excerpts"] if e["id"] == "excerpt.world-cup-soccer.switch-matrix")
		self.assertIn("image", matrix)
		self.assertLessEqual((ROOT / matrix["image"]).stat().st_size, 100_000)

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


class WorldCupSoccerCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_world_cup_soccer as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_world_cup_soccer as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_world_cup_soccer as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"World Cup Soccer", b"World Cup Soccerr", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_world_cup_soccer as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class WorldCupSoccerRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_world_cup_soccer as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_world_cup_soccer as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "midway/world-cup-soccer-1994/source/World Cup Soccer (Bally 1994) VPW v1.5.vpx"
		script = source_root / "midway/world-cup-soccer-1994/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_world_cup_soccer as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "world-cup-soccer" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
