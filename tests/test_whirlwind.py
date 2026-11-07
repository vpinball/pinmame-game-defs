from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "whirlwind-1990.json"
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

	def test_author_ready_identity_and_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.whirlwind.1990", machine["id"])
		self.assertEqual("Williams", machine["manufacturer"])
		self.assertEqual(1990, machine["year"])
		coverage = self.definition["coverage"]
		self.assertEqual("author_ready", coverage["status"])
		self.assertEqual([], coverage["missing"])
		self.assertEqual("validated", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("validated", coverage["dimensions"]["physical_wiring"])
		from pinmame_game_defs.validation import validate_machine
		self.assertEqual([], validate_machine(self.definition))

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
		matrix_only = {address for address in self.switches if 0 < address <= 64}
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

	def test_opto_matrix_contacts_are_normally_open_from_read_path_and_runtime(self) -> None:
		for address in OPTO_ADDRESSES:
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual("validated", self.switches[26]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.switches[57]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", self.switches[58]["spatial"]["reason"])

	def test_flipper_buttons_have_no_matrix_address_but_lane_change_optos_do(self) -> None:
		for address, switch in self.switches.items():
			if address <= 64:
				self.assertNotIn("Flipper Button", switch["label"])
		self.assertIn("Lane Change", self.switches[57]["label"])
		self.assertIn("Lane Change", self.switches[58]["label"])

	def test_flipper_column_81_to_88_is_enumerated_and_only_82_84_are_live(self) -> None:
		# core_updateSw copies public 82 (CORE_SWLRFLIPBUTBIT) into FLIP_SWR = 57 and 84
		# (CORE_SWLLFLIPBUTBIT) into FLIP_SWL = 58; FLIP_SWNO(58,57) sets no FLIP_EOS or upper FLIP_SW bit.
		column = {address: self.switches[address] for address in range(81, 89)}
		self.assertEqual({82, 84}, {address for address, switch in column.items() if switch["availability"] == "used"})
		self.assertEqual({81, 83, 85, 86, 87, 88}, {address for address, switch in column.items() if switch["availability"] == "unused"})
		self.assertEqual(["flipper.lower.right.button"], column[82]["roles"])
		self.assertEqual(["flipper.lower.left.button"], column[84]["roles"])
		self.assertIn("matrix switch 57", column[82]["physical"]["notes"])
		self.assertIn("matrix switch 58", column[84]["physical"]["notes"])
		self.assertIn("vpm-script-library.s11-vbs", column[82]["provenance"]["source_refs"])
		for address in (82, 84):
			self.assertFalse(column[address]["normally_closed"])
			self.assertIn("manual.williams.whirlwind.1990", column[address]["provenance"]["source_refs"])
			self.assertIn("open at rest", column[address]["physical"]["notes"])
		for address in (81, 83):
			self.assertIn("vpm-script-library.s11-vbs", column[address]["provenance"]["source_refs"])
		relationships = {(item["source"], item["destination"]) for item in self.definition["relationships"]}
		self.assertIn(("switch.flipper-column-82", "switch.matrix-57"), relationships)
		self.assertIn(("switch.flipper-column-84", "switch.matrix-58"), relationships)
		for address in (57, 58):
			self.assertIn("A consumer cannot drive this address", self.switches[address]["physical"]["notes"])
		self.assertIn("public 82", self.solenoids[45]["physical"]["notes"])
		self.assertNotIn("switch-57 state", json.dumps(self.solenoids[45]))

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
		self.assertEqual("validated", gi_11["spatial"]["status"])
		self.assertEqual(15, len(gi_11["spatial"]["placements"]))
		self.assertEqual(15, gi_11["physical"]["quantity"])
		gi_16 = self.solenoids[16]
		self.assertEqual("validated", gi_16["spatial"]["status"])
		self.assertEqual(11, len(gi_16["spatial"]["placements"]))
		self.assertEqual(29, gi_16["physical"]["quantity"])
		for address in (11, 16):
			self.assertIn("darkness", self.solenoids[address]["physical"]["notes"])

	def test_synthetic_flipper_solenoids_are_virtual_with_no_physical_device(self) -> None:
		for address in (45, 46, 47, 48):
			solenoid = self.solenoids[address]
			self.assertEqual("virtual", solenoid["kind"])
			self.assertEqual("not_applicable", solenoid["spatial"]["status"])
			self.assertEqual("virtual", solenoid["spatial"]["reason"])
			# PinMAME publishes live state here from public 82/84 while enable 23 is on.
			self.assertEqual("used", solenoid["availability"])

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

	def test_factory_flasher_counts_are_kept_separate_from_renderer_proxy_counts(self) -> None:
		for address in (37, 39, 40):
			self.assertEqual("validated", self.solenoids[address]["spatial"]["status"])
			self.assertEqual(self.solenoids[address]["physical"]["quantity"], len(self.solenoids[address]["spatial"]["placements"]))
		for address in (25, 26, 27, 29, 30, 31):
			self.assertEqual("validated", self.solenoids[address]["spatial"]["status"])
		for address in (28, 32):
			self.assertEqual("validated", self.solenoids[address]["spatial"]["status"])
			self.assertEqual(2, len(self.solenoids[address]["spatial"]["placements"]))
			self.assertIn("two native physical photographs", self.solenoids[address]["physical"]["notes"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual([1, 1, 2, 2, 2, 1, 2, 2], [self.solenoids[n]["physical"]["quantity"] for n in range(25, 33)])
		self.assertIn("three-left-bulb entry is a quantity erratum", self.solenoids[37]["physical"]["notes"])
		self.assertEqual([2, 1, 2], [self.solenoids[n]["physical"]["quantity"] for n in (37, 39, 40)])
		self.assertEqual(13, sum(len(self.solenoids[n]["spatial"]["placements"]) for n in range(25, 33)))

	def test_rear_inventory_is_reconciled_with_actual_lmp_designators(self) -> None:
		import curate_whirlwind as curator

		for address in (37, 39, 40):
			refs = self.solenoids[address]["provenance"]["source_refs"]
			self.assertIn(curator.REAR_ASSEMBLY_SOURCE, refs)
			self.assertIn(curator.REAR_PHOTO_SOURCE, refs)
			self.assertIn(curator.HANDBOOK_SOURCE, refs)
			self.assertIn("five flashers", self.solenoids[address]["physical"]["notes"])
		refs = self.solenoids[11]["provenance"]["source_refs"]
		self.assertIn(curator.REAR_GI_BRANCH_SOURCE, refs)
		self.assertIn("LMP6-LMP10", self.solenoids[11]["physical"]["notes"])
		self.assertEqual(15, self.solenoids[11]["physical"]["quantity"])

	def test_corrected_labels_preserve_existing_semantic_ids(self) -> None:
		self.assertEqual("device.top-upper-jet-bumper", self.solenoids[21]["id"])
		self.assertEqual("device.right-ramp-bottom-flasher", self.solenoids[30]["id"])
		self.assertIn("Left Playfield", self.solenoids[30]["label"])

	def test_jet_bumper_21_duplicate_label_is_resolved_and_disclosed(self) -> None:
		solenoid_21 = self.solenoids[21]
		self.assertIn("Top Lower Jet Bumper", solenoid_21["physical"]["notes"])
		self.assertEqual("Bottom Upper Jet Bumper", solenoid_21["label"])
		self.assertIn("Lower Top Jet Bumper", solenoid_21["physical"]["notes"])

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
				"excerpt.whirlwind.power-wiring",
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
		import curate_whirlwind as curator
		self.assertEqual("knowledge/williams/whirlwind-1990.md", self.definition["knowledge"]["path"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertEqual(curator.KNOWLEDGE_TEXT.rstrip(), KNOWLEDGE_PATH.read_text(encoding="utf-8").rstrip())


class WhirlwindCuratorTests(unittest.TestCase):
	def test_portable_numeric_ranges_remain_utf8_text(self) -> None:
		excerpt_root = ROOT / "evidence/excerpts/williams.whirlwind.1990"
		seed_root = ROOT / "tools/seeds/williams"
		paths = [
			*excerpt_root.glob("*.md"), *seed_root.glob("whirlwind-1990*.json"),
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH,
			SPATIAL_REPORT_PATH.with_suffix(".md"), ROOT / "tools/curate_whirlwind.py",
		]
		for path in paths:
			with self.subTest(path=path.relative_to(ROOT)):
				text = path.read_text(encoding="utf-8")
				self.assertNotIn("\u00e2\u20ac", text)
				self.assertNotIn("\ufffd", text)
		for path in [seed_root / "whirlwind-1990-hidden-bulbs.json", excerpt_root / "hidden-flasher-placement.md"]:
			with self.subTest(path=path.relative_to(ROOT)):
				text = path.read_text(encoding="utf-8")
				for numeric_range in ["219–249 px", "2650–3375", "1550–2600"]:
					self.assertIn(numeric_range, text)

	def test_hidden_bulbs_have_enclosing_controls_and_independent_physical_views(self) -> None:
		import curate_whirlwind as curator

		seed = curator.hidden_bulbs()
		self.assertEqual(4, len(seed["photos"]))
		self.assertEqual([28, 32], [p["address"] for p in seed["placements"]])
		self.assertEqual([[.527, .331], [.616, .352]], [p["normalized_xy"] for p in seed["placements"]])
		self.assertEqual([12, 10], [len(p["controls_world_xy"]) for p in seed["placements"]])
		for row in seed["placements"]:
			certificate = row["hull_certificate"]
			self.assertTrue(all(w > 0 for w in certificate["weights"]))
			self.assertAlmostEqual(1, sum(certificate["weights"]))
			# Each certificate uses a new independently read enclosing control.
			self.assertTrue(any(i >= (9 if row["address"] == 28 else 8) for i in certificate["indices"]))
			for axis in (0, 1):
				value = sum(w * row["controls_world_xy"][i][axis] for i, w in zip(certificate["indices"], certificate["weights"]))
				self.assertAlmostEqual(row["normalized_xy"][axis], value / row["bounds"][axis])
		self.assertEqual(9, seed["million"]["withheld_forward_control_check"]["variant_count"])

	def test_hidden_bulb_seed_drift_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "hidden.json"
			path.write_bytes(curator.HIDDEN_BULB_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "HIDDEN_BULB_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "hidden bulb projection seed changed"):
					curator.build()

	def test_matrix_bulbs_use_own_meshes_and_preserve_physical_quantities(self) -> None:
		import curate_whirlwind as curator

		seed = curator.matrix_bulbs()
		self.assertEqual({1, *range(9, 65)}, {p["address"] for p in seed["ordinary_and_jet_objects"]})
		self.assertEqual(6, sum("bigus_bulb" in p for p in seed["ordinary_and_jet_objects"]))
		lamps = bindings(curator.build(), "outputs", "pinmame.output.lamp")
		for row in seed["cellar_bulbs"]:
			point = lamps[row["address"]]["spatial"]["placements"][0]
			self.assertEqual(row["normalized_xy"], [point["x"], point["y"]])
			self.assertIn(curator.FLASHER_TABLE_SOURCE, point["provenance"]["source_refs"])
			self.assertIn("colored cover", lamps[row["address"]]["physical"]["notes"])
		for lamp in lamps.values():
			self.assertEqual(1, lamp["physical"]["quantity"])

	def test_matrix_bulb_seed_drift_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "matrix.json"
			path.write_bytes(curator.MATRIX_BULB_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "MATRIX_BULB_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "matrix bulb inventory changed"):
					curator.build()

	def test_rear_panel_projection_reproduces_and_has_independent_checks(self) -> None:
		import curate_whirlwind as curator

		seed = curator.rear_panel_seed()
		self.assertEqual(10, len(seed["sockets"]))
		self.assertEqual([37, 37, 39, 40, 40, 11, 11, 11, 11, 11], [p["address"] for p in seed["sockets"]])
		self.assertEqual([.120, .221, .397, .623, .846, .063, .248, .506, .793, .933], [p["normalized_xy"][0] for p in seed["sockets"]])
		self.assertTrue(all(p["normalized_xy"][1] == .112843 for p in seed["sockets"]))
		self.assertEqual(5, sum(p["outside_four_post_x_span"] for p in seed["sockets"]))
		self.assertLess(max(abs(x) for p in seed["assembled_elevation"]["variants"] for x in p["socket_x_delta_norm"]), .011)
		self.assertLess(max(abs(x) for p in seed["second_board_elevation"]["variants"] for x in p["bulb_x_delta_vs_socket_fit"]), .009)
		self.assertEqual(28, len(seed["mounted_panel_plane_check"]["held_out_screw_variants"]))

	def test_rear_panel_seed_drift_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "projection.json"
			path.write_bytes(curator.REAR_PLACEMENT_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "REAR_PLACEMENT_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "rear panel projection seed changed"):
					curator.build()

	def test_gi_bank_measurements_reproduce_and_both_belong_to_lower(self) -> None:
		import curate_whirlwind as curator
		import drawing_callouts

		seed = curator.gi_bank_seed()
		self.assertEqual(curator.flasher_seed()["pages"]["73"]["controls"], seed["pages"]["73"]["controls"])
		self.assertEqual((.381, .364), drawing_callouts.measured(seed, "region.three-bank-gi.rear"))
		self.assertEqual((.397, .375), drawing_callouts.measured(seed, "region.three-bank-gi.front"))
		devices = bindings(curator.build(), "outputs", "pinmame.output.solenoid")
		bank = [p for p in devices[16]["spatial"]["placements"] if "three-bank" in p["id"]]
		self.assertEqual([(.381, .364), (.397, .375)], [(p["x"], p["y"]) for p in bank])
		self.assertFalse(any("three-bank" in p["id"] for p in devices[11]["spatial"]["placements"]))
		for point in bank:
			self.assertIn(curator.GI_BANK_SOURCE, point["provenance"]["source_refs"])

	def test_gi_inventory_excludes_renderer_doubles_and_false_wire_bore(self) -> None:
		import curate_whirlwind as curator

		rows = curator.gi_inventory()["placements"]
		self.assertEqual(21, len(rows))
		self.assertEqual(10, sum(p["branch"] == "upper" for p in rows))
		self.assertEqual(11, sum(p["branch"] == "lower" for p in rows))
		self.assertEqual(20, len({p["object"] for p in rows if "object" in p}))
		self.assertFalse({"Light66", "Light67"} & {p.get("object") for p in rows})
		self.assertTrue(all(p.get("crosscheck_distance", 0) < .025 for p in rows))
		self.assertEqual("lower", next(p["branch"] for p in rows if p.get("object") == "Light81"))
		self.assertLess(curator.gi_inventory()["photo_control_fit"]["max_held_out_distance"], .009)

	def test_gi_inventory_drift_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "inventory.json"
			path.write_bytes(curator.GI_INVENTORY_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "GI_INVENTORY_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "physical GI inventory changed"):
					curator.build()

	def test_changing_gi_bank_measurement_seed_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "readings.json"
			path.write_bytes(curator.GI_BANK_SEED_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "GI_BANK_SEED_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "GI bank measurement seed changed"):
					curator.build()

	def test_factory_measurements_and_dome_checks_reproduce(self) -> None:
		import curate_whirlwind as curator
		import drawing_callouts

		seed = curator.flasher_seed()
		placements = drawing_callouts.placements_of(curator.build())
		self.assertEqual(6, len(seed["measurements"]))
		for pid in seed["measurements"]:
			self.assertEqual(drawing_callouts.measured(seed, pid), placements[pid], pid)
		decisions = drawing_callouts.evaluate(seed, placements)
		self.assertEqual(11, len(decisions["placements"]))
		self.assertTrue(all(q["agrees"] for q in decisions["placements"].values()))
		self.assertEqual(2, len(seed["excluded_checks"]))
		self.assertLess(decisions["pages"]["73"]["callout_loo_max"], .07)

	def test_changing_measurement_seed_is_rejected(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			path = Path(temporary) / "readings.json"
			path.write_bytes(curator.FLASHER_SEED_PATH.read_bytes() + b" ")
			with mock.patch.object(curator, "FLASHER_SEED_PATH", path):
				with self.assertRaisesRegex(RuntimeError, "measurement seed changed"):
					curator.build()

	def test_replacing_an_extraction_file_and_its_manifest_still_fails_the_pin(self) -> None:
		import curate_whirlwind as curator
		from pinmame_game_defs.jsonio import canonical_bytes
		import hashlib

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			(root / "extracted").mkdir()
			fixture = root / "extracted/script.vbs"
			fixture.write_bytes(b"one")
			manifest = curator.build_extraction_manifest(root / "extracted")
			(root / "manifest.json").write_bytes(canonical_bytes(manifest))
			with mock.patch.multiple(curator, EXTRACTION_RELATIVE_PATH=Path("extracted"), EXTRACTION_MANIFEST_RELATIVE_PATH=Path("manifest.json"), EXTRACTION_FILE_COUNT=1, EXTRACTION_TOTAL_BYTES=3, EXTRACTION_MANIFEST_SHA256=hashlib.sha256(canonical_bytes(manifest)).hexdigest()):
				curator.verify_extraction_manifest(root)
				fixture.write_bytes(b"two")  # Same count and byte total; only the pinned identity detects this.
				(root / "manifest.json").write_bytes(canonical_bytes(curator.build_extraction_manifest(root / "extracted")))
				with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
					curator.verify_extraction_manifest(root)

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

	def test_regenerate_refuses_changed_author_ready_output_before_writing(self) -> None:
		import curate_whirlwind as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			target = root / "machines/author-ready/williams/whirlwind-1990.json"
			target.parent.mkdir(parents=True)
			target.write_bytes(b"existing reviewed contribution\n")
			with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
				curator.generate(root)
			self.assertEqual(b"existing reviewed contribution\n", target.read_bytes())
			self.assertFalse((root / "tools/seeds/williams/whirlwind-1990.json").exists())

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
		self.assertEqual("pinmame-spatial-audit", report["format"])
		self.assertEqual([], report["blockers"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual([], report["incomplete_outputs"])
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class WhirlwindRetainedEvidenceTests(unittest.TestCase):
	def test_all_matrix_objects_and_script_bound_cellar_bulbs_match_sources(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/whirlwind-1990"
		seed = curator.matrix_bulbs()
		for row in seed["ordinary_and_jet_objects"]:
			path = root / f"extracted-vpxtool/gameitems/{row['original_object']}.json"
			self.assertEqual(row["original_object_sha256"], curator._file_sha256(path))
			if "raw_xy" in row:
				lamp = load_json(path)["Light"]
				self.assertTrue(lamp["is_bulb_light"])
				self.assertEqual(row["raw_xy"], [lamp["center"]["x"], lamp["center"]["y"]])
				self.assertEqual(row["original_xy"], [round(row["raw_xy"][0] / 964, 6), round(row["raw_xy"][1] / 2162, 6)])
			if "bigus_bulb" in row:
				bulb = row["bigus_bulb"]
				path = root / f"supplemental-20261106/primary-bigus/extracted/gameitems/{bulb['object']}.json"
				self.assertEqual(bulb["sha256"], curator._file_sha256(path))
				lamp = load_json(path)["Light"]
				self.assertTrue(lamp["show_bulb_mesh"])
				self.assertEqual(row["raw_xy"], [lamp["center"]["x"], lamp["center"]["y"]])
		fourk = root / "supplemental-20261106/primary-4k-1113/extracted"
		for bulb in seed["cellar_bulbs"]:
			self.assertEqual(bulb["primitive_json_sha256"], curator._file_sha256(fourk / f"gameitems/Primitive.{bulb['object']}.json"))
		script = (fourk / "script.vbs").read_text(encoding="utf-8")
		self.assertRegex(script, r"(?is)case 39\s+CellarLeftNew = PfInsertStateNew\(ii\) \* 7\s+case 40\s+CellarRightNew = PfInsertStateNew\(ii\) \* 7")
		for side in ("Left", "Right"):
			self.assertIn(f'Bulb{side}.image = "simplelightwhite" & Cellar{side}Current', script)

	def test_gi_bulb_objects_and_independent_coordinates_match_retained_sources(self) -> None:
		import math
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/whirlwind-1990/supplemental-20261106/primary-bigus/extracted"
		collections = {c["name"]: set(c["items"]) for c in load_json(root / "collections.json")}
		for row in curator.gi_inventory()["placements"]:
			if "object" not in row:
				continue
			path = root / f"gameitems/Light.{row['object']}.json"
			self.assertEqual(row["object_sha256"], curator._file_sha256(path))
			lamp = load_json(path)["Light"]
			self.assertTrue(lamp["is_bulb_light"])
			self.assertTrue(lamp["show_bulb_mesh"])
			self.assertEqual(row["raw_xy"], [lamp["center"]["x"], lamp["center"]["y"]])
			x, y = row["raw_xy"][0] / 964, row["raw_xy"][1] / 2162
			distance = math.dist((x, y), (row["fourk_socket_xy"][0] / 952, row["fourk_socket_xy"][1] / 2164))
			self.assertAlmostEqual(row["crosscheck_distance"], distance, places=12)
			self.assertLess(distance, .025)
			actual_group = "UpperGI" if row["branch"] == "upper" or row["object"] == "Light81" else "LowerGI"
			self.assertIn(row["object"], collections[actual_group])

	def test_supplemental_domes_and_factory_controls_match_retained_objects(self) -> None:
		import curate_whirlwind as curator
		from pinmame_game_defs.jsonio import canonical_bytes
		import hashlib

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/whirlwind-1990"
		supplement = root / "supplemental-20261106/primary-4k-1113"
		manifest = curator.build_extraction_manifest(supplement / "extracted")
		self.assertEqual(3016, len(manifest["files"]))
		self.assertEqual(351873613, sum(q["size"] for q in manifest["files"]))
		self.assertEqual("018991497f6b90ca112c4dc1ca1f582fd6f8bf05d2aec5a38daf40c4d50905a6", hashlib.sha256(canonical_bytes(manifest)).hexdigest())
		self.assertEqual("4ef5614e92109aa8c9362957e0b8390c56bcf04b098aaacad7cabb8482ffbd54", curator._file_sha256(supplement / "table.vpx"))
		self.assertEqual("704319827005cfaa196b4415cd9e42db3ff8b4d55192b711d08884456d7f2501", curator._file_sha256(supplement / "extracted/script.vbs"))
		for address, name in curator.FLASHER_DOME_OBJECTS.items():
			obj = load_json(supplement / f"extracted/gameitems/Primitive.{name}.json")["Primitive"]
			self.assertEqual(curator.FLASHER_DOME_POSITIONS[address], (round(obj["position"]["x"]/952,6), round(obj["position"]["y"]/2164,6)))
		for q in curator.flasher_seed()["pages"]["73"]["controls"]:
			path = root / "extracted-vpxtool/gameitems" / q["object_file"]
			self.assertEqual(q["object_sha256"], curator._file_sha256(path))
			center = next(iter(load_json(path).values()))["center"]
			self.assertEqual(q["xy"], [center["x"]/964, center["y"]/2162])

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

	def test_retained_vpm_script_library_matches_its_pinned_hashes(self) -> None:
		import curate_whirlwind as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		library = Path(root) / "vpm-script-libs"
		self.assertEqual(curator.VPM_S11_SHA256, curator._file_sha256(library / "s11.vbs"))
		self.assertEqual(curator.VPM_CORE_SHA256, curator._file_sha256(library / "core.vbs"))
		s11 = (library / "s11.vbs").read_text(encoding="utf-8", errors="replace")
		self.assertRegex(s11, r"Const swLRFlip\s*=\s*82")
		self.assertRegex(s11, r"Const swLLFlip\s*=\s*84")

@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained runtime evidence root is not configured")
class WhirlwindRuntimeEvidenceTests(unittest.TestCase):
	def test_hidden_bulb_native_sources_and_frozen_reproduction_inputs_match(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106"
		seed = curator.hidden_bulbs()
		for item in seed["photos"] + seed["external_reproduction_inputs"]:
			self.assertEqual(item["sha256"], curator._file_sha256(root / item["path"]), item["path"])

	def test_cellar_bulb_world_mesh_bounds_recompute(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106"
		seed = curator.matrix_bulbs()
		path = root / seed["cellar_world_obj_path"]
		self.assertEqual(seed["cellar_world_obj_sha256"], curator._file_sha256(path))
		vertices, selected, current = [], {}, None
		wanted = {p["object"] for p in seed["cellar_bulbs"]}
		for line in path.read_text(encoding="utf-8").splitlines():
			if line.startswith("v "):
				vertices.append(tuple(map(float, line.split()[1:4])))
			elif line.startswith(("o ", "g ")):
				current = line.split(" ", 1)[1]
			elif line.startswith("f ") and current in wanted:
				selected.setdefault(current, set()).update(int(p.split("/")[0]) - 1 for p in line.split()[1:])
		for bulb in seed["cellar_bulbs"]:
			points = [vertices[i] for i in selected[bulb["object"]]]
			self.assertEqual(bulb["vertices"], len(points))
			self.assertEqual(bulb["bounds_min"], [min(v[i] for v in points) for i in range(3)])
			self.assertEqual(bulb["bounds_max"], [max(v[i] for v in points) for i in range(3)])

	def test_rear_panel_projection_sources_and_frozen_checks_match(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106"
		seed = curator.rear_panel_seed()
		for item in seed["external_reproduction_inputs"]:
			self.assertEqual(item["sha256"], curator._file_sha256(root / item["path"]))
		for relative, digest in {
			"web/eyi-images/whirlwind_rear_storm_lamp_board_start.jpg": seed["assembled_elevation"]["source_sha256"],
			"web/eyi-images/whirlwind_rear_storm_lamp_board_dirty.jpg": seed["second_board_elevation"]["source_sha256"],
			"web/eyi-images/whirlwind_rear_storm_lamp_board_plastic_clean.jpg": seed["plastic_art_registration"]["source_sha256"],
			"parent-gi-voltage-and-rescue/rescue-selected-4.jpeg": seed["mounted_panel_plane_check"]["source_sha256"],
			"primary-bigus-world/table.obj": seed["world_obj_sha256"],
		}.items():
			self.assertEqual(digest, curator._file_sha256(root / relative), relative)

	def test_original_stock_gi_photographs_match_portable_inventory(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106/primary-google-selected"
		for name, digest in {
			"under-upper.jpg": "013ca8b2cb3fbaea765ea10e85005dddd34267cd6a59255e21e071fcad9e54f3",
			"under-wide.jpg": "5c8261f6f6353329ad8ff7fcc51d7c3e4cdee3a66b22a247701206c84cf4de3c",
			"under-compass.jpg": "90e81857fc47c66164432518190ef9b46c0b315ac8fa42591e0f2839a3195ded",
			"under-bare.jpg": "65d1725bd5f015ae346355da9e43e9cff7329ac37c5263c13a74f38305030ef2",
		}.items():
			self.assertEqual(digest, curator._file_sha256(root / name), name)
		additional = root.parent / "parent-google-rear-gallery/selected-originals"
		for name, digest in {
			"lower-near.jpg": "411b623faf59a418a9a80cc0a1267b4775e25e40417472a0ebe74b36883c1365",
			"lower-reverse.jpg": "d2fecb09ce889ed8c02e82ce193fe67897bc296beed2a9898f73a436eb7c2c38",
		}.items():
			self.assertEqual(digest, curator._file_sha256(additional / name), name)

	def test_rear_factory_drawing_photo_and_repair_match_retained_hashes(self) -> None:
		import curate_whirlwind as curator

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		for source in curator.source_records():
			if source["id"] not in {curator.REAR_ASSEMBLY_SOURCE, curator.REAR_PHOTO_SOURCE, curator.REAR_GI_BRANCH_SOURCE, curator.HANDBOOK_SOURCE, curator.GI_STOCK_SOURCE, curator.GI_CURVE_SOURCE, curator.GI_CORNER_SOURCE, curator.GI_WIRE_SOURCE, curator.RAMP_DOME_SOURCE}:
				continue
			path = root / source["uri"].removeprefix("external:pinmame-review-artifacts/")
			self.assertEqual(source["sha256"], curator._file_sha256(path), source["id"])
		self.assertEqual("ebd2a2eef166271ae8f5e3614fccd06d836a48bbb1f48fbf6970532df61e254e", curator._file_sha256(root / "whirlwind-20261106/primary-red-parts/page0473_i2-wrapper.pdf"))

	def test_rom_displays_identify_each_exercised_input_at_level_one(self) -> None:
		import curate_whirlwind as curator
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106"
		path = root / "harness-all-levels.json"
		self.assertEqual(curator.SERVICE_RUN_SHA256, curator._file_sha256(path))
		run = load_json(path)
		self.assertIsNone(run["failure"])
		events = run["events"]
		seen = set()
		for step in run["steps"]:
			if step.get("type") != "set_switch" or step.get("state") != 1 or step.get("switch", 0) < 0:
				continue
			host = step["switch"]
			matrix = {82: 57, 84: 58}.get(host, host)
			start = next(e["time_s"] for e in events if e["event"] == "switch" and e.get("step") == step["step"] and e["state"] == 1)
			end = next(e["time_s"] for e in events if e["event"] == "switch" and e.get("step", 0) > step["step"])
			numbers = []
			for event in events:
				if event["event"] != "display" or event["index"] != 1 or not start + 0.05 < event["time_s"] < end:
					continue
				for token in event.get("text", "").split()[1:]:
					token = token.replace("O", "0").replace("S", "5")
					if token.isdigit():
						numbers.append(int(token))
			self.assertIn(matrix, numbers, f"host {host}: ROM never displayed its matrix number while high")
			seen.add(host)
		self.assertEqual((MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {2, 57, 58}) | {82, 84}, seen)

	def test_coil_test_corroborates_the_five_sound_overlay_addresses(self) -> None:
		import curate_whirlwind as curator
		path = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "whirlwind-20261106/harness-coils.json"
		self.assertEqual(curator.COIL_RUN_SHA256, curator._file_sha256(path))
		run = load_json(path)
		self.assertIsNone(run["failure"])
		checkpoint = next(s["time_s"] for s in run["snapshots"] if s["label"] == "locate Coil Test")
		published = {e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"] and e["time_s"] > checkpoint}
		self.assertEqual(set(range(1, 23)) | set(range(25, 33)) | set(range(37, 42)), published)
		lower = ""
		matched = set()
		for event in run["events"]:
			if event["event"] == "display" and event["index"] == 1:
				lower = event.get("text", "").replace("O", "0").replace("S", "5")
			if event["event"] == "solenoid" and event["state"] and 37 <= event["number"] <= 41 and event["time_s"] > checkpoint:
				self.assertEqual(event["number"] - 14, int(lower.split()[1]))
				matched.add(event["number"])
		self.assertEqual({37, 38, 39, 40, 41}, matched)


if __name__ == "__main__":
	unittest.main()
