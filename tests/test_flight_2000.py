from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import file_sha256, load_json
from pinmame_game_defs.validation import validate_machine


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_flight_2000 as flight


class Flight2000Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(ROOT / flight.DEFINITION)

    def by_address(self, inventory: str, group: str) -> dict:
        return {item["binding"]["device"]: item for item in self.definition[inventory]
                if item["binding"]["group"] == group}

    def test_physical_identity_and_driver_split(self) -> None:
        self.assertEqual({driver["id"] for driver in self.definition["drivers"]},
                         {"flight2k", "flightfp", "flight2m", "flight2mb"})
        speech_variant = next(driver for driver in self.definition["drivers"] if driver["id"] == "flight2mb")
        self.assertEqual(speech_variant["physical_compatibility"], "compatible")
        self.assertIn("U10", speech_variant["variant_notes"])
        conversion = load_json(ROOT / flight.CONVERSION)
        self.assertEqual(conversion["machine"]["ipdb_id"], 984)
        self.assertEqual([(driver["id"], driver["clone_of"]) for driver in conversion["drivers"]],
                         [("gamatron", "flight2k")])
        catalog = load_json(ROOT / "catalog/pinmame.json")
        for definition in (self.definition, conversion):
            for driver in definition["drivers"]:
                entries = [row["machine_id"] for row in catalog["drivers"] if row["id"] == driver["id"]]
                self.assertEqual(entries, [definition["machine"]["id"]])
        extraction = load_json(ROOT / "reports/vpx-script-extraction.json")
        gamatron = next(row for row in extraction["entries"] if row["driver_ids"] == ["gamatron"])
        self.assertEqual(gamatron["machine_ids"], [flight.CONVERSION_ID])
        self.assertEqual(load_json(ROOT / gamatron["evidence"])["machine_ids"], [flight.CONVERSION_ID])

    def test_enumeration_and_physical_shared_contacts(self) -> None:
        switches = self.by_address("inputs", "pinmame.input.switch")
        self.assertEqual(set(switches), {-7, -6, -5, *range(1, 41), *range(81, 85)})
        shared = switches[17]
        self.assertFalse(shared["normally_closed"])
        self.assertEqual(shared["physical"]["quantity"], 3)
        self.assertEqual(len(shared["spatial"]["placements"]), 3)
        self.assertEqual(switches[39]["id"], "switch.ball-launcher-contact")
        self.assertEqual(switches[40]["id"], "switch.release-next-rocket-rollover")
        self.assertNotIn("spatial", switches[33])
        self.assertEqual(switches[82]["spatial"]["reason"], "cabinet_or_service")
        direct = self.by_address("inputs", "physical.input.direct")
        self.assertTrue(direct[1]["normally_closed"])
        self.assertTrue(direct[2]["normally_closed"])

    def test_decoder_routes_and_under_review_lamps(self) -> None:
        coils = self.by_address("outputs", "pinmame.output.solenoid")
        self.assertEqual(set(coils), {*range(1, 16), *range(17, 21), *range(45, 49)})
        self.assertEqual([coils[n]["wiring"]["driver_transistor"] for n in (1, 2, 9, 10, 17, 18, 19, 20)],
                         ["Q2", "Q1", "Q13", "Q14", "Q17", "Q19", "Q15", "Q18"])
        lamps = self.by_address("outputs", "pinmame.output.lamp")
        self.assertEqual(set(lamps), set(range(1, 64)) - {16, 32, 48})
        self.assertEqual(lamps[11]["physical"]["quantity"], 2)
        self.assertNotIn("spatial", lamps[11])
        report = load_json(ROOT / flight.REPORT.with_suffix(".json"))
        self.assertEqual(report["candidate_insert_apertures"][lamps[11]["id"]]["name"], "L11")
        self.assertEqual(lamps[24]["wiring"]["driver_transistor"], "Q25")
        self.assertEqual(lamps[25]["wiring"]["driver_transistor"], "Q24")
        self.assertEqual(lamps[44]["availability"], "unknown")
        self.assertEqual(lamps[47]["availability"], "unknown")
        self.assertNotIn("wiring", lamps[44])
        self.assertNotIn("spatial", self.by_address("outputs", "physical.output.gi")[1])

    def test_mechanism_actuators_and_display_callback_layout(self) -> None:
        bank = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.left-five-bank")
        self.assertIn("coil.left-drop-target-bank-reset", bank["actuators"])
        self.assertEqual(len(bank["actuators"]), 6)
        self.assertEqual(len(bank["sensors"]), 5)
        self.assertEqual([(d["segment_start"], d["width"]) for d in self.definition["displays"]],
                         [(1, 7), (9, 7), (17, 7), (25, 7), (35, 2), (38, 2)])

    def test_reproducible_products_and_promotion_gate(self) -> None:
        for path, expected in flight.products().items():
            self.assertEqual((ROOT / path).read_bytes(), expected, path)
        self.assertEqual(self.definition["coverage"]["status"], "partial")
        self.assertEqual(self.definition["coverage"]["missing"],
                         ["input_semantics", "output_semantics", "mechanism_behavior",
                          "variant_differences", "spatial_placement"])
        self.assertEqual(validate_machine(self.definition, ROOT), [])
        trace = load_json(flight.RUNTIME_EVIDENCE)
        run = trace["runtime"]["raw_runs"][0]
        self.assertEqual(file_sha256(ROOT / run["scenario_path"]), run["scenario_sha256"])
        self.assertEqual(set(trace["runtime"]["observations"]["lamp_addresses_seen"]),
                         set(self.by_address("outputs", "pinmame.output.lamp")))

    def test_retained_evidence_when_available(self) -> None:
        if not any(os.environ.get(name) for name in
                   ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")):
            self.skipTest("External evidence roots are unavailable")
        seed = load_json(flight.SEEDS / f"{flight.SLUG}-evidence.json")
        flight.verify_external(seed)
