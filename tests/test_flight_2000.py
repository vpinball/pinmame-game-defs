from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import file_sha256, load_json
from pinmame_game_defs.schema_validation import validate_against_schema
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

    def test_modified_driver_hardware_conditions(self) -> None:
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        sources = {source["id"]: source for source in self.definition["sources"]}
        for driver_id, source_id in (("flight2m", flight.IDLEMAN_33), ("flight2mb", flight.IDLEMAN_3347)):
            driver = drivers[driver_id]
            self.assertEqual(driver["physical_compatibility"], "compatible")
            self.assertIn(source_id, driver["variant_notes"])
            self.assertIn(source_id, sources)
            self.assertIn("Retained runtime traces cover flight2k and flightfp", driver["variant_notes"])
            self.assertNotIn("overrides", driver)
        rules = drivers["flight2m"]["variant_notes"]
        self.assertIn("A3J2-8 (public 18) to the knocker", rules)
        self.assertIn("walker at A3J5-12 (public 9)", rules)
        self.assertIn("DIP 14 routing selection is documented from subversion 39 onward", rules)
        speech = drivers["flight2mb"]["variant_notes"]
        self.assertIn("DIP 14 ON, keep the walker at A3J5-12 (public 9)", speech)
        self.assertIn("DIP 14 OFF, swap those leads so A3J2-8 (public 18) drives the walker", speech)
        self.assertIn("A3J5-12 (public 9) drives the knocker", speech)
        self.assertIn("two revised 2716 speech images at U9 and U10", speech)

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

    def test_dip23_stock_boot_test_and_modified_special(self) -> None:
        dips = self.by_address("inputs", "pinmame.input.dip")
        self.assertEqual(set(dips), set(range(1, 33)))
        self.assertEqual(dips[23]["id"], "dip.mpu-dip-23")
        self.assertEqual(dips[23]["availability"], "used")
        self.assertEqual(dips[23]["provenance"]["status"], "validated")
        self.assertTrue({flight.STOCK_DIPS, flight.DIP_RUNTIME, flight.IDLEMAN_33, flight.IDLEMAN_3347}
                        <= set(dips[23]["provenance"]["source_refs"]))
        notes = dips[23]["physical"]["notes"]
        self.assertIn("all-DIPs-off boot test", notes)
        self.assertIn("center Special award an extra ball", notes)

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
        self.assertEqual(lamps[44]["availability"], "used")
        self.assertIn(flight.STOCK_GAME, lamps[44]["provenance"]["source_refs"])
        self.assertEqual(lamps[44]["wiring"]["driver_transistor"], "Q39")
        self.assertNotIn("drive_connection", lamps[44]["wiring"])
        self.assertEqual(lamps[59]["wiring"]["drive_connection"], "J3-13")

    def test_q31_is_an_unfitted_physical_output(self) -> None:
        q31 = self.by_address("outputs", "pinmame.output.lamp")[47]
        self.assertEqual(q31["id"], "lamp.q31-unfitted-lamp-output")
        self.assertEqual(q31["availability"], "unused")
        self.assertEqual(q31["kind"], "lamp")
        self.assertEqual(q31["spatial"]["status"], "not_applicable")
        self.assertEqual(q31["spatial"]["reason"], "unused")
        self.assertEqual(set(q31["provenance"]["source_refs"]),
                         {flight.CORE, flight.MANUAL, flight.SCHEMATIC, flight.RUNTIME,
                          flight.LAMP_TECH_CHART, flight.SCRIPT})
        self.assertEqual(q31["wiring"]["driver_transistor"], "Q31")
        self.assertEqual(q31["wiring"]["drive_connection"], "J2-2")
        self.assertIn("Q31's exact pin remains uncertain", q31["physical"]["notes"])
        self.assertIn("J2-21", self.by_address("outputs", "pinmame.output.lamp")[11]["physical"]["notes"])
        report = load_json(ROOT / flight.REPORT.with_suffix(".json"))
        self.assertEqual(report["unfitted_lamp_public_addresses"], [47])
        self.assertNotIn(q31["id"], report["missing_device_positions"])
        self.assertNotIn(q31["id"], report["candidate_insert_apertures"])
        with patch.dict(flight.data.LAMP_ROWS, {47: (1,)}):
            with self.assertRaisesRegex(ValueError, "factory lamp load row must be assigned exactly once"):
                flight.products()

    def test_rear_gi_places_only_the_observed_subset(self) -> None:
        gi = self.by_address("outputs", "physical.output.gi")[1]
        self.assertNotIn("quantity", gi["physical"])
        self.assertEqual(gi["spatial"]["status"], "observed")
        positions = gi["spatial"]["placements"]
        self.assertEqual([(p["id"], p["x"], p["y"]) for p in positions], [
            ("gi.rear-l-a-socket", 0.594498, 0.11241),
            ("gi.rear-a-s-socket", 0.682381, 0.113178),
            ("gi.rear-s-t-socket", 0.772752, 0.1134),
        ])
        for point in positions:
            self.assertEqual(point["role"], "emitter")
            self.assertIn(flight.GI_ORIGINAL_PHOTO, point["provenance"]["source_refs"])

    def test_mechanism_actuators_and_display_callback_layout(self) -> None:
        bank = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.left-five-bank")
        self.assertIn("coil.left-drop-target-bank-reset", bank["actuators"])
        self.assertEqual(len(bank["actuators"]), 6)
        self.assertEqual(len(bank["sensors"]), 5)
        walker = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.ball-walker")
        self.assertEqual(walker["assembly_part_number"], "B-758")
        self.assertEqual(walker["actuators"], ["coil.ball-launcher-walker-release"])
        self.assertEqual(walker["sensors"], ["switch.ball-launcher-contact", "switch.release-next-rocket-rollover"])
        self.assertTrue({flight.WALKER_PHOTO, flight.ENTRY_PHOTO, flight.STOCK_GAME, flight.STOCK_BOOT}
                        <= set(walker["provenance"]["source_refs"]))
        self.assertEqual([(d["segment_start"], d["width"]) for d in self.definition["displays"]],
                         [(1, 7), (9, 7), (17, 7), (25, 7), (35, 2), (38, 2)])

    def test_reproducible_products_and_promotion_gate(self) -> None:
        for path, expected in flight.products().items():
            self.assertEqual((ROOT / path).read_bytes(), expected, path)
        self.assertEqual(self.definition["coverage"]["status"], "partial")
        self.assertEqual(self.definition["coverage"]["missing"], ["spatial_placement"])
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

    def test_compact_runtime_evidence(self) -> None:
        scenario_paths = set()
        for path in flight.FOLLOWUP_SUMMARIES:
            summary = load_json(path)
            self.assertEqual(validate_against_schema(summary, ROOT / "schemas/evidence.schema.json", path.name), [])
            runtime = summary["runtime"]
            self.assertEqual(set(runtime["observations"]["runs"]), {row["name"] for row in runtime["raw_runs"]})
            scenario_paths.update(run["scenario_path"] for run in runtime["raw_runs"])
        for relative in scenario_paths:
            self.assertEqual(validate_against_schema(load_json(ROOT / relative),
                             ROOT / "schemas/harness-scenario.schema.json", relative), [])
        sources = {source["id"]: source["uri"] for source in self.definition["sources"]}
        dips = self.by_address("inputs", "pinmame.input.dip")
        self.assertTrue({flight.DIP_RUNTIME, flight.DIP_FREE_RUNTIME} <= set(dips[23]["provenance"]["source_refs"]))
        self.assertEqual(sources[flight.DIP_FREE_RUNTIME], "internal:evidence/runtime/stern/flight-2000-free-play-dip23.json")

    def test_retained_stock_runtime_observations_when_available(self) -> None:
        root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not root:
            self.skipTest("External review artifacts are unavailable")
        root = Path(root) / flight.ID
        stock, free_play = [load_json(path)["runtime"]["observations"]["runs"] for path in flight.FOLLOWUP_SUMMARIES]
        service = load_json(root / "service-occupied/trace.json")
        self.assertEqual(service["game"], "flight2k")
        self.assertEqual([step["label"] for step in service["steps"]
                          if any(event["number"] == 47 and 1 in event["states"]
                                 for event in step["transitions"]["lamps"])],
                         ["Service edge 1", "Service edge 2"])
        for driver, runs in (("flight2k", stock), ("flightfp", free_play)):
            for bank, expected in (("00", {1, *range(3, 16)}), ("40", set())):
                with self.subTest(driver=driver, bank=bank):
                    case = f"{driver}-bank3-{bank}"
                    trace = load_json(root / f"followup-dip23-scripted/{case}/trace.json")
                    self.assertIsNone(trace["failure"])
                    self.assertEqual(trace["game"], driver)
                    self.assertEqual({event["number"] for event in trace["events"]
                                      if event["event"] == "solenoid" and event["state"] == 1
                                      and 1 <= event["number"] <= 15}, expected)
                    self.assertEqual(runs[case]["solenoid_addresses_seen"], sorted(expected))

        boot = load_json(root / "followup-stock-boot-observation/trace.json")
        self.assertIsNone(boot["failure"])
        self.assertEqual(boot["game"], "flight2k")
        self.assertEqual(boot["initial_switches"], [{"switch": 33, "state": 1}, {"switch": 34, "state": 1}])
        self.assertEqual([(step["type"], step["seconds"]) for step in boot["steps"]], [("wait", 65)])
        self.assertFalse([e for e in boot["events"] if e["event"] == "switch" and not e.get("initial")])
        recovery = [event for event in boot["events"]
                    if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > 8
                    and event["number"] in {9, 17, 20}]
        observed = stock["followup-stock-boot-observation"]
        self.assertEqual([event["number"] for event in recovery], observed["ordered_solenoid_on_sequence"])
        self.assertEqual([event["number"] for event in recovery], [17, 20, 9] * 7)
        self.assertGreater(boot["events"][-1]["time_s"] - recovery[-1]["time_s"], 25)

        gameplay = load_json(root / "followup-stock-game/trace.json")
        self.assertIsNone(gameplay["failure"])
        self.assertEqual(gameplay["game"], "flight2k")
        self.assertEqual(gameplay["scenario"]["sha256"], file_sha256(root / "followup-stock-game/scenario.json"))
        for index in (1, 13, 21):
            solenoids = gameplay["steps"][index - 1]["transitions"]["solenoids"]
            self.assertFalse(any(event["number"] == 9 and 1 in event["states"] for event in solenoids))
        for index in (9, 17):
            solenoids = gameplay["steps"][index - 1]["transitions"]["solenoids"]
            self.assertEqual([event["states"] for event in solenoids if event["number"] == 9], [[0]])
        arrivals = [event["time_s"] for event in gameplay["events"]
                    if event["event"] == "switch" and event["number"] == 39 and event["state"] == 1]
        walker = [event["time_s"] for event in gameplay["events"]
                  if event["event"] == "solenoid" and event["number"] == 9]
        self.assertEqual([round(walker[2 * i] - arrivals[i], 2) for i in range(2)], [0.24, 0.22])
        self.assertEqual([round(walker[2 * i + 1] - walker[2 * i], 2) for i in range(2)], [1.24, 1.24])
        for index, expected in ((4, {7, 10, 15, 19}), (8, {9, 10}), (12, {7, 10, 15}),
                                (16, {9, 10}), (20, {7, 10, 15}), (43, {9}), (46, {17, 20})):
            with self.subTest(step=index):
                step = gameplay["steps"][index - 1]
                self.assertEqual({event["number"] for event in step["transitions"]["solenoids"]
                                  if 1 in event["states"]}, expected)
        for index, expected in ((8, {62: [1]}), (16, {46: [1]}), (28, {53: [0], 55: [1]}),
                                (29, {37: [0]}), (40, {44: [1], 60: [1]})):
            with self.subTest(step=index):
                lamps = gameplay["steps"][index - 1]["transitions"]["lamps"]
                self.assertEqual({event["number"]: event["states"] for event in lamps if event["number"] in expected},
                                 expected)
