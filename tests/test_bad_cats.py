from pathlib import Path
import subprocess
import sys
import unittest

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
MACHINE = "williams.bad-cats.1989"
DEFINITION = "machines/partial/williams/bad-cats-1989.json"


class BadCatsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(ROOT / DEFINITION)
        cls.devices = {
            (d["binding"]["group"], d["binding"]["device"]): d
            for d in cls.definition["inputs"] + cls.definition["outputs"]
        }

    def test_single_physical_record_for_all_seven_drivers(self):
        drivers = {d["id"] for d in self.definition["drivers"]}
        self.assertEqual(drivers, {
            "bcats_l5", "bcats_l2", "bcats_g4", "bcats_f1",
            "bcats_tcm", "bcats_tcm12", "bcats_tcm13",
        })
        catalog = load_json(ROOT / "catalog/pinmame.json")
        self.assertEqual(
            {d["id"] for d in catalog["drivers"] if d["definition"] == DEFINITION},
            drivers,
        )
        self.assertFalse(list((ROOT / "machines/stubs").rglob("bad-cats-1989.json")))
        self.assertEqual(self.definition["machine"]["ipdb_id"], 127)
        self.assertEqual(self.definition["machine"]["model_number"], "575")

    def test_public_io_and_service_observations(self):
        addresses = {
            group: {address for g, address in self.devices if g == group}
            for group, _ in self.devices
        }
        self.assertEqual(addresses, {
            "pinmame.input.dip": {0},
            "pinmame.input.switch": set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)),
            "pinmame.output.lamp": set(range(1, 65)),
            "pinmame.output.solenoid": set(range(1, 51)),
        })
        switches = "pinmame.input.switch"
        self.assertEqual(self.devices[switches, 2]["id"], "switch.c-side-power-a-c-relay-feedback")
        self.assertEqual(self.devices[switches, 11]["label"], "T Rollover")
        self.assertEqual(self.devices[switches, 33]["label"], "Rubber 1")
        self.assertEqual(self.devices[switches, 44]["physical"]["switch_type"], "opto")
        self.assertNotIn("normally_closed", self.devices[switches, 44])
        self.assertFalse(self.devices[switches, 10]["normally_closed"])
        self.assertIn("vpx-script.bcats.unclewilly", self.devices[switches, 10]["provenance"]["source_refs"])
        self.assertEqual([(d["width"], d["segment_start"]) for d in self.definition["displays"]], [(16, 0), (16, 20)])
        coils = "pinmame.output.solenoid"
        self.assertEqual(self.devices[coils, 15]["label"], "Seafood Wheel Winding 2")
        self.assertEqual(self.devices[coils, 16]["label"], "Seafood Wheel Winding 1")
        self.assertEqual(self.devices[coils, 30]["physical"]["quantity"], 3)
        self.assertNotIn("spatial", self.devices[coils, 30])
        for address in (7, 8, 22):
            self.assertEqual(self.devices[coils, address]["availability"], "unused")
            self.assertIn("NOT USED", self.devices[coils, address]["physical"]["notes"])
        lamps = "pinmame.output.lamp"
        for address in range(9, 14):
            self.assertEqual(self.devices[lamps, address]["physical"]["location"], "Tiger Ramp")
        for address in range(17, 20):
            self.assertEqual(self.devices[lamps, address]["physical"]["location"], "rear playfield panel")
        self.assertEqual(self.devices[lamps, 31]["label"], "Doghouse")
        self.assertEqual(self.devices[lamps, 32]["availability"], "unknown")
        self.assertEqual(self.devices[lamps, 55]["label"], "Barbecue (Backglass)")
        wheel = next(d for d in self.definition["mechanisms"] if d["id"] == "mechanism.wheel")
        self.assertEqual(wheel["actuators"], [self.devices[coils, n]["id"] for n in (15, 16)])
        self.assertEqual(wheel["sensors"], [self.devices[switches, 44]["id"]])

    def test_coverage_and_reproducibility(self):
        self.assertEqual(validate_machine(self.definition, ROOT), [])
        self.assertEqual(self.definition["coverage"]["status"], "partial")
        self.assertEqual(set(self.definition["coverage"]["missing"]), {
            "mechanism_behavior", "output_semantics", "polarity", "spatial_placement",
        })
        self.assertEqual(
            self.devices["pinmame.input.switch", 60]["spatial"]["placements"][0]["x"], 0.62933,
        )
        self.assertEqual(
            self.devices["pinmame.output.solenoid", 26]["spatial"]["placements"][0]["y"], 0.06668,
        )
        subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/curate_bad_cats.py"), "--check"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )

    def test_runtime_evidence_and_scenarios_match_schema(self):
        path = ROOT / "evidence/runtime/system-11/bcats_l5-service.json"
        evidence = load_json(path)
        self.assertEqual(validate_against_schema(evidence, ROOT / "schemas/evidence.schema.json", str(path)), [])
        self.assertEqual(evidence["machine_ids"], [MACHINE])
        observations = evidence["runtime"]["observations"]
        self.assertEqual(
            observations["ordered_solenoid_on_sequence"],
            [address for a in range(1, 9) for address in (a, a + 24)] + list(range(9, 23)),
        )
        self.assertIn("BARBECUE IN B.B.", observations["runs"]["lamps"]["note"])
        for run in evidence["runtime"]["raw_runs"]:
            scenario = ROOT / run["scenario_path"]
            self.assertEqual(
                validate_against_schema(load_json(scenario), ROOT / "schemas/harness-scenario.schema.json", str(scenario)),
                [],
            )


if __name__ == "__main__":
    unittest.main()
