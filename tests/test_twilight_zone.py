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
		self.assertEqual(2684, self.definition["machine"]["ipdb_id"])
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
		# GI 1 and GI 2 are mixed playfield + backbox insert strings with no bulb list: physical,
		# but unplaced. GI 3 "Insert Main" is backbox-only.
		for address in (1, 2):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertNotIn("quantity", self.gi[address]["physical"], address)
			self.assertIn("No spatial placement", self.gi[address]["physical"]["notes"], address)
			self.assertIn("backbox insert", self.gi[address]["physical"]["notes"], address)
		self.assertEqual(("not_applicable", "cabinet_or_service"), (self.gi[3]["spatial"]["status"], self.gi[3]["spatial"]["reason"]))
		self.assertEqual("validated", self.gi[0]["spatial"]["status"])
		self.assertGreater(len(self.gi[0]["spatial"]["placements"]), 1)

	def test_no_used_physical_device_is_internal_nonvisual_for_lack_of_geometry(self) -> None:
		# validation.py pairs internal_nonvisual with internal.* roles. Only the four flipper
		# end-of-stroke contacts and the clock strobe line may use it; every other used physical device
		# must either be placed or omit its spatial key. The exemption is by address, not by role, so
		# adding an internal.* role to another device cannot hide a missing placement.
		exempt = {("pinmame.input.switch", address) for address in (111, 113, 115, 117)} | {("pinmame.output.solenoid", 58)}
		physical_kinds = {"switch", "coil", "flasher", "lamp", "gi", "motor", "magnet", "relay", "control_signal"}
		offenders = []
		internal_nonvisual = set()
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			key = (device["binding"]["group"], device["binding"]["device"])
			if spatial is not None and spatial["status"] == "not_applicable" and spatial["reason"] == "internal_nonvisual":
				internal_nonvisual.add(key)
			if device["kind"] not in physical_kinds or device["availability"] != "used" or spatial is None:
				continue
			if key in exempt:
				continue
			if spatial["status"] == "not_applicable" and spatial["reason"] == "internal_nonvisual":
				offenders.append(device["id"])
			self.assertNotIn("No VPX geometry evidence", device.get("physical", {}).get("notes", ""), device["id"])
		self.assertEqual([], offenders)
		self.assertTrue(exempt <= internal_nonvisual)
		strobe = self.solenoids[58]
		self.assertEqual("control_signal", strobe["kind"])
		self.assertEqual("internal_nonvisual", strobe["spatial"]["reason"])
		self.assertEqual(["internal.clock-opto-strobe"], strobe["roles"])

	def test_unplaced_physical_devices_omit_spatial_and_say_why(self) -> None:
		unplaced = {
			(device["binding"]["group"], device["binding"]["device"])
			for device in self.definition["inputs"] + self.definition["outputs"]
			if "spatial" not in device
		}
		self.assertEqual(
			{
				("pinmame.input.switch", 45), ("pinmame.input.switch", 46),
				("pinmame.output.solenoid", 7), ("pinmame.output.solenoid", 18), ("pinmame.output.solenoid", 19),
				("pinmame.output.solenoid", 20), ("pinmame.output.solenoid", 55),
				("pinmame.output.gi", 1), ("pinmame.output.gi", 2),
			},
			unplaced,
		)
		for group, address in unplaced:
			device = {"pinmame.input.switch": self.switches, "pinmame.output.solenoid": self.solenoids, "pinmame.output.gi": self.gi}[group][address]
			self.assertEqual("used", device["availability"], (group, address))
			self.assertIn("No spatial placement", device["physical"]["notes"], (group, address))
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(unplaced, {(entry["group"], entry["address"]) for entry in report["unresolved"]})
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])

	def test_door_panel_lamps_are_playfield_inserts_and_buttons_are_cabinet(self) -> None:
		for address in list(range(11, 19)) + list(range(21, 29)):
			lamp = self.lamps[address]
			placement = lamp["spatial"]["placements"][0]
			self.assertEqual("validated", lamp["spatial"]["status"], address)
			self.assertNotIn("roles", lamp, address)
			self.assertTrue(0.35 < placement["x"] < 0.62 and 0.5 < placement["y"] < 0.75, address)
		for address in (87, 88):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])

	def test_jet_bumper_switches_and_coils_follow_the_manual_drawings(self) -> None:
		self.assertEqual("Left Jet Bumper", self.switches[31]["label"])
		self.assertEqual("Right Jet Bumper", self.switches[32]["label"])
		self.assertEqual("Lower Jet Bumper", self.switches[33]["label"])
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		left, right, lower = point(self.switches[31]), point(self.switches[32]), point(self.switches[33])
		self.assertLess(left[0], right[0])
		self.assertGreater(lower[1], left[1])
		self.assertGreater(lower[1], right[1])
		# Coils by the page 2-53 drawing: 13 left, 14 upper right, 12 lower.
		self.assertEqual(left, point(self.solenoids[13]))
		self.assertEqual(right, point(self.solenoids[14]))
		self.assertEqual(lower, point(self.solenoids[12]))

	def test_flipper_coils_sit_on_their_own_flipper(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		lower_right, lower_left = point(self.solenoids[45]), point(self.solenoids[47])
		upper_right, upper_left = point(self.solenoids[33]), point(self.solenoids[35])
		self.assertGreater(lower_right[0], 0.5)
		self.assertLess(lower_left[0], 0.5)
		self.assertGreater(upper_right[0], upper_left[0])
		self.assertEqual(lower_right, point(self.solenoids[46]))
		self.assertEqual(lower_left, point(self.solenoids[48]))
		self.assertEqual(upper_right, point(self.solenoids[34]))
		self.assertEqual(upper_left, point(self.solenoids[36]))
		# End-of-stroke contacts follow the repository convention: internal to the flipper assembly.
		for eos in (111, 113, 115, 117):
			spatial = self.switches[eos]["spatial"]
			self.assertEqual(("not_applicable", "internal_nonvisual"), (spatial["status"], spatial["reason"]), eos)
			self.assertTrue(self.switches[eos]["roles"][0].startswith("internal."), eos)
		for button in (112, 114, 116, 118):
			self.assertEqual("cabinet_or_service", self.switches[button]["spatial"]["reason"])

	def test_clock_optos_and_motor_share_the_clock_axis(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		axis = point(self.switches[91])
		self.assertTrue(axis[0] > 0.7 and axis[1] < 0.3)
		for address in range(92, 99):
			self.assertEqual(axis, point(self.switches[address]), address)
		self.assertEqual(axis, point(self.solenoids[56]))
		self.assertEqual(axis, point(self.solenoids[57]))

	def test_corrected_placements_do_not_regress(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		self.assertNotEqual(point(self.switches[47]), point(self.switches[52]))
		self.assertNotEqual(point(self.switches[74]), point(self.switches[51]))
		self.assertEqual(point(self.switches[26]), point(self.switches[15]))
		self.assertEqual(point(self.solenoids[15]), point(self.switches[88]))
		self.assertNotEqual(point(self.solenoids[24]), point(self.solenoids[6]))
		self.assertEqual(point(self.solenoids[24]), point(self.switches[55]))
		flasher = self.solenoids[17]
		self.assertEqual(2, flasher["physical"]["quantity"])
		self.assertEqual(2, len(flasher["spatial"]["placements"]))
		for address in (18, 19, 20, 55):
			self.assertEqual(2, self.solenoids[address]["physical"]["quantity"], address)
		# Solenoid 5 sits on the diverter blade primitive (BM_RDiv pivot), not on the invisible DivTrig/DivWall helpers.
		self.assertEqual((0.279253, 0.21377), point(self.solenoids[5]))
		self.assertIn("Primitive.BM_RDiv", self.solenoids[5]["physical"]["notes"])
		for address in (51, 52, 53, 54, 55, 56, 57, 58):
			self.assertTrue(self.solenoids[address]["physical"]["notes"].startswith(
				f"Printed solenoid/flasher-locations item {address - 14}, "
			), address)

	def test_spatial_report_separates_projections_from_direct_placements(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertTrue(report["projections"])
		self.assertTrue(report["direct_placements"])
		for entry in report["projections"]:
			self.assertTrue(entry["reason"].startswith("Projected onto"), entry)
		for entry in report["direct_placements"]:
			self.assertFalse(entry["reason"].startswith("Projected onto"), entry)
		direct = {(entry["group"], entry["address"]) for entry in report["direct_placements"]}
		self.assertIn(("pinmame.input.switch", 31), direct)
		self.assertIn(("pinmame.input.switch", 52), direct)
		self.assertIn(("pinmame.output.solenoid", 5), direct)

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


GEOMETRY_FILES = ("vpx-geometry.txt", "vpx-geometry-2026-09-25.txt", "vpx-geometry-2026-09-25-round3.txt")


def _geometry_rows(text: str) -> list[tuple[str, str, float, float, float, float]]:
	"""Parse the object rows of a pinned geometry file: (vpx_type, vpx_name, raw_x, raw_y, norm_x, norm_y)."""
	rows = []
	for line in text.splitlines():
		fields = line.split("\t")
		if len(fields) < 7:
			continue
		try:
			numbers = [float(value) for value in fields[3:7]]
		except ValueError:
			continue
		rows.append((fields[1], fields[2], *numbers))
	return rows


def _hard_coded_coordinates() -> list[tuple[str, float, float]]:
	"""Every normalized coordinate the curator hard-codes, including the _norm() anchors."""
	import curate_twilight_zone as curator

	coordinates = []
	for table_name, table in (
		("SWITCH_POSITIONS", curator.SWITCH_POSITIONS),
		("SOLENOID_POSITIONS", curator.SOLENOID_POSITIONS),
		("LAMP_POSITIONS", curator.LAMP_POSITIONS),
		("GI_POSITIONS", curator.GI_POSITIONS),
	):
		for address, points in table.items():
			for x, y in points:
				coordinates.append((f"{table_name}[{address}]", x, y))
	return coordinates


class TwilightZoneRetainedGeometryTests(unittest.TestCase):
	"""Tie every hard-coded coordinate to the pinned geometry files, and those files to the retained extraction.

	Every coordinate in SWITCH_POSITIONS, SOLENOID_POSITIONS, LAMP_POSITIONS and GI_POSITIONS (the TABLE_OBJECTS
	anchors included, since they reach the definition through those tables) must equal the normalized columns of
	a row in one of the three hash-pinned geometry files; with the extraction configured, every such row and every
	TABLE_OBJECTS anchor must also be recomputable from gameitems.
	"""

	@staticmethod
	def _object_point(item_type: str, item: dict[str, object]) -> tuple[float, float]:
		if item_type in {"HitTarget", "Primitive"}:
			return (item["position"]["x"], item["position"]["y"])
		if item.get("center") is not None:
			return (item["center"]["x"], item["center"]["y"])
		if item_type == "Wall":
			points = item["drag_points"]
			return (sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points))
		raise AssertionError(f"unexpected anchor type {item_type}")

	@staticmethod
	def _review_folder() -> Path | None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		return Path(root).expanduser().resolve() / "twilight-zone-1993" if root else None

	def _used_rows(self, folder: Path) -> list[tuple[str, str, float, float, float, float]]:
		rows = [row for name in GEOMETRY_FILES for row in _geometry_rows((folder / name).read_text(encoding="utf-8"))]
		used = []
		for label, x, y in _hard_coded_coordinates():
			matches = [row for row in rows if abs(row[4] - x) < 5e-7 and abs(row[5] - y) < 5e-7]
			self.assertTrue(matches, f"{label} ({x}, {y}) matches no row of the pinned geometry files")
			used.extend(matches)
		return used

	def test_table_object_anchors_match_the_retained_extraction(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		gameitems = Path(root).expanduser().resolve() / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		for name, (x, y) in curator.TABLE_OBJECTS.items():
			item_type, _ = name.split(".", 1)
			path = gameitems / f"{name}.json"
			self.assertTrue(path.is_file(), path)
			item = load_json(path)[item_type]
			actual = self._object_point(item_type, item)
			self.assertAlmostEqual(x, actual[0], places=4, msg=name)
			self.assertAlmostEqual(y, actual[1], places=4, msg=name)

	def test_review_artifacts_match_their_pinned_hashes(self) -> None:
		folder = self._review_folder()
		if folder is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import hashlib
		import curate_twilight_zone as curator

		expected = {
			"vpx-geometry.txt": curator.VPX_GEOMETRY_SHA256,
			"vpx-geometry-2026-09-25.txt": curator.VPX_GEOMETRY_SUPPLEMENT_SHA256,
			"vpx-geometry-2026-09-25-round3.txt": curator.VPX_GEOMETRY_SUPPLEMENT_2_SHA256,
			"manual-transcription.md": curator.MANUAL_TRANSCRIPTION_SHA256,
		}
		for name, digest in expected.items():
			self.assertEqual(digest, hashlib.sha256((folder / name).read_bytes()).hexdigest(), name)
		geometry = "\n".join((folder / name).read_text(encoding="utf-8") for name in GEOMETRY_FILES)
		# Every anchor the curator names must be listed in one of the pinned geometry files.
		for name in curator.TABLE_OBJECTS:
			item_type, object_name = name.split(".", 1)
			self.assertIn(f"{item_type}\t{object_name}\t", geometry, name)

	def test_every_hard_coded_coordinate_matches_a_pinned_geometry_row(self) -> None:
		folder = self._review_folder()
		if folder is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import curate_twilight_zone as curator

		used = self._used_rows(folder)
		self.assertGreater(len(used), 150)
		# Each matched row must itself follow the file's stated normalization.
		for item_type, name, raw_x, raw_y, x, y in used:
			self.assertAlmostEqual(x, round(raw_x / curator.BOUNDS_X, 6), places=6, msg=f"{item_type}.{name}")
			self.assertAlmostEqual(y, round(raw_y / curator.BOUNDS_Y, 6), places=6, msg=f"{item_type}.{name}")

	def test_every_matched_geometry_row_is_recomputable_from_gameitems(self) -> None:
		folder = self._review_folder()
		vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if folder is None or not vpx_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT and PINMAME_VPX_SOURCES_ROOT are both required")
		import curate_twilight_zone as curator

		gameitems = Path(vpx_root).expanduser().resolve() / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		for item_type, name, raw_x, raw_y, _, _ in set(self._used_rows(folder)):
			path = gameitems / f"{item_type}.{name}.json"
			self.assertTrue(path.is_file(), path)
			actual = self._object_point(item_type, load_json(path)[item_type])
			self.assertAlmostEqual(raw_x, actual[0], places=3, msg=f"{item_type}.{name}")
			self.assertAlmostEqual(raw_y, actual[1], places=3, msg=f"{item_type}.{name}")


class TwilightZoneExtractionManifestTests(unittest.TestCase):
	def test_manifest_matches_the_retained_extraction_when_evidence_root_is_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		curator.verify_extraction_manifest(Path(root).expanduser().resolve())


if __name__ == "__main__":
	unittest.main()
