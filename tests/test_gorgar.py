import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_gorgar as curator
from pinmame_game_defs.jsonio import load_json


class GorgarTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.definition = load_json(ROOT / curator.DEFINITION)
		cls.devices = {
			(d["binding"]["group"], d["binding"]["device"]): d
			for section in ("inputs", "outputs") for d in cls.definition[section]
		}

	def test_driver_family(self):
		catalog = load_json(ROOT / "catalog/pinmame.json")
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(set(drivers), {"grgar_c1", "grgar_l1", "grgar_l1ff", "grgar_l2", "grgar_t1", "grgar_t1ff"})
		self.assertTrue(all(d.get("clone_of") == "grgar_l1" for k, d in drivers.items() if k != "grgar_l1"))
		self.assertEqual(drivers["grgar_l2"]["physical_compatibility"], "unknown")
		records = [m for m in catalog["machines"] if m["id"] in {curator.MACHINE, "stub.pinmame.grgar_l1"}]
		self.assertEqual([m["id"] for m in records], [curator.MACHINE])

	def test_full_controller_inventory(self):
		profile = load_json(ROOT / "controllers/pinmame/system-6.json")
		for group in profile["groups"]:
			expected = {
				n for rule in group["address_rules"] for n in range(rule["minimum"], rule["maximum"] + 1)
			}
			actual = {address for group_id, address in self.devices if group_id == group["id"]}
			self.assertEqual(actual, expected, group["id"])
		self.assertEqual(
			[(d["segment_start"], d["width"]) for d in self.definition["displays"]],
			[(0, 6), (8, 6), (20, 6), (28, 6), (14, 2), (6, 2)],
		)

	def test_physical_and_emulator_contracts(self):
		solenoid = lambda address: self.devices[curator.SOLENOID, address]
		lamp = lambda address: self.devices[curator.LAMP, address]
		self.assertEqual(solenoid(5)["id"], "relay.magnet-relay")
		self.assertEqual(solenoid(6)["kind"], "flasher")
		self.assertEqual(solenoid(6)["physical"]["quantity"], 2)
		self.assertNotIn("spatial", solenoid(6))
		self.assertEqual(solenoid(15)["availability"], "unused")
		self.assertEqual(lamp(56)["availability"], "used")
		self.assertEqual(lamp(47)["availability"], "unknown")
		self.assertEqual(lamp(47)["spatial"]["reason"], "unused")
		self.assertEqual(lamp(63)["physical"]["quantity"], 2)
		self.assertEqual(lamp(63)["spatial"]["reason"], "cabinet_or_service")
		self.assertEqual(self.devices[curator.SWITCH, 26]["spatial"]["status"], "observed")
		self.assertIn(curator.RETRO_TABLE, self.devices[curator.SWITCH, 24]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertNotIn("spatial", self.devices[curator.SWITCH, 29])
		self.assertEqual(self.definition["coverage"]["status"], "partial")
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])
		self.assertIn("output_semantics", self.definition["coverage"]["missing"])

	def test_lamp_wire_order(self):
		for address, expected in enumerate(("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY"), 1):
			self.assertEqual(self.devices[curator.LAMP, address]["wiring"]["return_wire"], f"RED-{expected}")
		self.assertEqual(self.devices[curator.LAMP, 64]["wiring"]["drive_wire"], "YEL-GRY")
		self.assertEqual(self.devices[curator.LAMP, 64]["wiring"]["drive_connection"], "9J1-7")

	def test_gameplay_evidence(self):
		runtime = load_json(ROOT / curator.RUNTIME)
		observed = {
			int(step["label"].split()[-1]): (step["input_address"], step["transitioned_solenoid_addresses"])
			for step in runtime["runtime"]["observations"]["named_action_observations"]
		}
		self.assertEqual(observed[12], (23, [5, 6]))
		self.assertEqual(observed[14], (15, [2]))
		self.assertEqual(observed[18], (20, []))
		self.assertEqual(observed[19], (21, [4]))
		self.assertEqual(observed[26], (43, []))
		self.assertEqual(observed[27], (44, [3]))
		self.assertEqual(observed[32], (9, [1, 3, 4]))
		self.assertIn(47, runtime["runtime"]["observations"]["lamp_addresses_seen"])

	def test_generation(self):
		curator.curate(ROOT, check=True)

	def test_external_evidence(self):
		roots = [
			Path(value) if (value := os.getenv(env)) else None
			for env in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
		]
		if not any(roots):
			self.skipTest("external evidence roots are not configured")
		curator.verify_external(load_json(ROOT / curator.SEED), *roots)
