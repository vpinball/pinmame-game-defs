from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import file_sha256

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_external_evidence_manifest import check_manifest
import curate_data_east_star_trek as curator


class DataEastStarTrekTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.definition, _ = curator.build()
		cls.switches = cls.devices("inputs", "pinmame.input.switch")
		cls.solenoids = cls.devices("outputs", "pinmame.output.solenoid")
		cls.lamps = cls.devices("outputs", "pinmame.output.lamp")

	@classmethod
	def devices(cls, field, group):
		return {d["binding"]["device"]: d for d in cls.definition[field] if d["binding"]["group"] == group}

	def test_generated_artifacts_match(self):
		for path, expected in curator.artifacts().items():
			with self.subTest(path=path.relative_to(ROOT)):
				self.assertEqual(path.read_bytes(), expected)
		self.assertFalse(curator.AUTHOR_READY.exists())
		self.assertEqual(file_sha256(curator.SCENARIO), curator.SCENARIO_HASH)

	def test_driver_group_display_and_address_envelopes(self):
		drivers = {d["id"]: d for d in self.definition["drivers"]}
		self.assertEqual(set(drivers), {f"trek_{suffix}" for suffix in ("110", "117", "11a", "120", "200", "201", "300", "301")})
		self.assertEqual({d.get("clone_of") for d in drivers.values() if d["id"] != "trek_201"}, {"trek_201"})
		self.assertEqual(drivers["trek_11a"]["physical_compatibility"], "identical")
		self.assertNotIn("display_overrides", drivers["trek_11a"])
		self.assertIn("520-5042-00", drivers["trek_11a"]["variant_notes"])
		self.assertEqual(self.definition["machine"]["ipdb_id"], 2356)
		display, = self.definition["displays"]
		self.assertEqual((display["controller_index"], display["width"], display["height"]), (0, 128, 16))
		self.assertEqual(set(self.switches), {-7, -6, *range(1, 65), *range(81, 89)})
		self.assertEqual(set(self.solenoids), set(range(1, 54)))
		self.assertEqual(set(self.lamps), set(range(1, 65)))

	def test_j8_and_upper_left_hole_cover_factory_inputs(self):
		dip, = self.devices("inputs", "pinmame.input.dip").values()
		self.assertEqual(dip["label"], "CPU PA7 Jumper J8")
		self.assertEqual(dip["availability"], "used")
		self.assertFalse(dip["initial_active"])
		self.assertIn(curator.PA7_ROM, dip["provenance"]["source_refs"])
		for address, label, wire in ((28, "Upper Left Hole Top", "GRN-YEL"), (52, "Upper Left Hole Bottom", "GRN-VIO")):
			contact = self.switches[address]
			self.assertEqual(contact["label"], label)
			self.assertFalse(contact["normally_closed"])
			self.assertEqual(contact["wiring"]["drive_wire"], wire)
			self.assertIn(curator.SWITCH_TEST, contact["provenance"]["source_refs"])
		self.assertNotIn("input_semantics", self.definition["coverage"]["missing"])

	def test_auxiliary_lines_and_rear_lamp_id_stability(self):
		for address in range(40, 45):
			output = self.solenoids[address]
			self.assertEqual((output["kind"], output["availability"]), ("virtual", "unused"))
			self.assertIn(curator.CHASE_ROM, output["provenance"]["source_refs"])
		for address, label, previous_slug in (
			(44, "Left Ramp Green", "left-ramp-red"),
			(45, "Left Million Red", "left-million-green"),
			(63, "Right Million Red", "right-million-green"),
			(64, "Right Ramp Green", "right-ramp-red"),
		):
			lamp = self.lamps[address]
			self.assertEqual(lamp["id"], f"lamp.{previous_slug}")
			self.assertEqual(lamp["label"], label)
			self.assertIn(curator.REAR_PHOTO, lamp["provenance"]["source_refs"])
		self.assertNotIn("variant_differences", self.definition["coverage"]["missing"])

	def test_mirrors_are_distinct_from_physical_devices(self):
		pairs = {(link["source"], link["destination"]) for link in self.definition["relationships"]}
		for button, matrix in ((84, 15), (82, 16)):
			self.assertEqual(self.switches[button]["kind"], "switch")
			self.assertEqual(self.switches[matrix]["kind"], "virtual")
			self.assertIn((self.switches[button]["id"], self.switches[matrix]["id"]), pairs)
		for origin, output in zip(range(37, 40), range(51, 54), strict=True):
			self.assertEqual(self.solenoids[origin]["kind"], "virtual")
			self.assertEqual(self.solenoids[output]["kind"], "lamp")
			self.assertIn((self.solenoids[origin]["id"], self.solenoids[output]["id"]), pairs)

	def test_physical_quantities_and_partial_gate(self):
		self.assertEqual(self.solenoids[11]["kind"], "gi")
		self.assertEqual(self.solenoids[13]["kind"], "motor")
		self.assertEqual(self.lamps[36]["spatial"]["reason"], "cabinet_or_service")
		self.assertEqual(self.lamps[36]["provenance"]["status"], "conflicted")
		self.assertNotIn("quantity", self.lamps[36]["physical"])
		self.assertEqual(self.definition["conflicts"][0]["id"], "lamp36-additional-playfield-load")
		self.assertEqual(self.lamps[50]["physical"]["quantity"], 2)
		self.assertEqual(len(self.lamps[50]["spatial"]["placements"]), 2)
		self.assertEqual(self.solenoids[25]["physical"]["quantity"], 4)
		self.assertLess(len(self.solenoids[25]["spatial"]["placements"]), 4)
		for address, pixels in ((19, [(403, 3077), (468, 3261)]), (51, [(1419, 3076), (1355, 3260)])):
			switch = self.switches[address]
			self.assertEqual(switch["physical"]["quantity"], 2)
			placements = switch["spatial"]["placements"]
			self.assertEqual([(p["x"], p["y"]) for p in placements],
			                 [(round(x / 1992, 6), round(y / 4295, 6)) for x, y in pixels])
			for placement in placements:
				self.assertEqual(placement["role"], "sensor")
				self.assertIn(curator.SLING_PHOTO, placement["provenance"]["source_refs"])
				self.assertIn(curator.SLING_BOARD, placement["provenance"]["source_refs"])
		self.assertEqual(self.definition["coverage"]["status"], "partial")
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])
		self.assertIn("unresolved_conflicts", self.definition["coverage"]["missing"])
		report = json.loads(curator.artifacts()[curator.REPORT.with_suffix(".json")])
		inventory = report["flasher_inventory"]
		self.assertEqual(inventory["flasher.circuit-1b"]["unplaced_playfield_bulbs"], 2)
		self.assertEqual(inventory["flasher.circuit-7b"]["backbox_bulbs"], 3)
		for row in inventory.values():
			self.assertEqual(row["total_bulbs"], row["backbox_bulbs"] + row["placed_playfield_bulbs"] + row["unplaced_playfield_bulbs"])

	def test_retained_vpx_source_when_configured(self):
		root = os.getenv("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("VPX evidence root is not configured")
		curator.verify_vpx(Path(root))

	def test_retained_manuals_when_configured(self):
		root = os.getenv("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("Manual evidence root is not configured")
		root = Path(root)
		self.assertEqual(file_sha256(root / curator.SHORT), curator.SHORT_HASH)
		self.assertEqual(file_sha256(root / curator.FULL), curator.FULL_HASH)
		for number, _, digest, _, _ in curator.BULLETINS:
			self.assertEqual(file_sha256(root / curator.MANUAL_REL / "factory-bulletins" / f"Sb{number}.pdf"), digest)
		report = json.loads(curator.REPORT.with_suffix(".json").read_bytes())
		for drawing in report["drawings"].values():
			self.assertEqual(file_sha256(root / curator.SHORT.parent / drawing["render"]), drawing["sha256"])

	def test_retained_runtime_source_when_configured(self):
		root = os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("Review evidence root is not configured")
		path = Path(root) / curator.TRACE_REL
		self.assertEqual(check_manifest(path.parent, curator.DRIVER), curator.TRACE_MANIFEST_HASH)
		self.assertEqual(file_sha256(path), curator.TRACE_HASH)
		self.assertEqual(file_sha256(path.with_name("trek-201-start.json")), curator.RAW_SCENARIO_HASH)
		self.assertEqual(json.loads(curator.SCENARIO.read_bytes()), json.loads(path.with_name("trek-201-start.json").read_bytes()))
		trace = json.loads(path.read_bytes())
		self.assertIsNone(trace["failure"])
		transitions = [{t["number"]: t["states"] for t in step["transitions"]["solenoids"]} for step in trace["steps"]]
		self.assertEqual(transitions[3][2], [1, 0, 1, 0])
		self.assertEqual(transitions[6][3], [1, 0])
		self.assertEqual(transitions[8][1], [1, 0, 1])
		for step in transitions:
			for original in range(37, 40):
				self.assertEqual(step.get(original), step.get(original + 14))

	def test_retained_follow_up_sources_when_configured(self):
		root = os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("Review evidence root is not configured")
		root = Path(root)
		for path, expected in ((curator.MOTOR_REL, curator.MOTOR_HASH), (curator.CHASE_REL, curator.CHASE_HASH),
		                       (curator.PA7_REL, curator.PA7_HASH)):
			self.assertEqual(file_sha256(root / path), expected)
		for photo in json.loads(curator.SEED.read_bytes())["photos"]:
			if photo.get("source_id") in (curator.SLING_PHOTO, curator.SLING_BOARD):
				self.assertEqual(file_sha256(root / photo["retained"]), photo["sha256"])
		display_path = root / curator.DISPLAY_REL
		self.assertEqual(check_manifest(display_path.parent, curator.MACHINE), curator.DISPLAY_HASH)
		switch_path = root / curator.SWITCH_TEST_REL
		self.assertEqual(check_manifest(switch_path.parent, curator.DRIVER), curator.SWITCH_TEST_HASH)
		self.assertEqual(file_sha256(curator.SWITCH_TEST_SCENARIO), curator.SWITCH_TEST_SCENARIO_HASH)
		for dip in (0, 1):
			trace = json.loads((switch_path.parent / f"switch-test-{dip}.json").read_bytes())
			self.assertIsNone(trace["failure"])
			self.assertEqual(trace["scenario"]["sha256"], curator.SWITCH_TEST_SCENARIO_HASH)
			stimulus, = [event for event in trace["events"] if event["event"] == "dip_stimulus"]
			self.assertEqual((stimulus["bank"], stimulus["default"], stimulus["state"]), (0, 0, dip))
			self.assertEqual(trace["steps"][3]["matched_text"], "STAR TREK SWITCH EDGES")
			samples = {row["label"]: row["displays"][0]["pixel_sha256"] for row in trace["snapshots"]}
			self.assertEqual(samples["18 reference left return first sample"],
			                 "ffc2ec9a47e28cd886ef2f467a4703a4ef8db22b8903af988d77c8cd60958758")
			self.assertEqual(samples["18 reference left return repeated first sample"],
			                 samples["18 reference left return first sample"])
			self.assertEqual(samples["28 upper-left top first sample"],
			                 "9ef4dc004b028b12181d4704998005dc3fd1ba8e2ce3fb4d4d235f6ab9ca5551")
			self.assertEqual(samples["52 upper-left bottom first sample"],
			                 "3dd0cadfecbe86a0a9e9c0ced1cc164e405f2b13b4f079d650121b1391023d9b")
			self.assertEqual(samples["28 release"], samples["reach the switch test"])
			self.assertEqual(samples["52 release"], samples["reach the switch test"])
