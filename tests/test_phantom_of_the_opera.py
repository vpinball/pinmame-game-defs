from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import curate_phantom_of_the_opera as curator
from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.jsonio import content_sha256

ID = "data-east.phantom-of-the-opera.1990"
SLUG = "phantom-of-the-opera-1990"
MACHINE = ROOT / "machines/partial/data-east" / f"{SLUG}.json"
REPORT = ROOT / "reports/spatial/data-east" / f"{SLUG}.json"
MANUAL = "manual.data-east.phantom-of-the-opera.1990"
SCRIPT = "vpx-script.phantom-of-the-opera-1.25"
TABLE = "vpx-table.phantom-of-the-opera-1.25"
EXTRACTION = "vpx-extraction.phantom-of-the-opera-1.25"
CORE = "pinmame.core.46e1a01a0f73"
PINS = {
    MANUAL: "1feebf59ab838056591fd67853bd2b54a9524447038e2a7a2c7ad3fe4765cd09",
    SCRIPT: "e373bf66dab343166e954fb2a7ed9c1ee0d8627ae5e125b13e4339b46757d5f6",
    TABLE: "e609fdfe0c358957ac2314f298cc6236523a62cd5cd6b979d0c1bc4f475e3bd9",
    EXTRACTION: "029e0bdb66b39060e5de73294a1f9cd5b72f5615ea1ecab2c10ec282091e0c12",
    "vpm-script-library.phantom-de-vbs":
        "8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04",
    "human-review.phantom-knocker-owners":
        "ad9d5ebc5811d7a869f7aedbb0daa0a38f49c890638fd10dbfd46d3d0bb7161c",
    "human-review.phantom-output20-rom-analysis":
        "6a038fd88ead731c1d6a885304359ca2b301441f42de46caeb6fc1bc3462b06e",
}
DRIVERS = {"poto_a29", "poto_a31", "poto_a32"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def bindings(machine, collection, group):
    rows = [d for d in machine[collection] if d["binding"]["group"] == group]
    result = {d["binding"]["device"]: d for d in rows}
    if len(result) != len(rows):
        raise AssertionError(f"duplicate binding in {group}")
    return result


def retained_root(test, variable):
    value = os.environ.get(variable)
    if not value:
        test.skipTest(f"{variable} is not set")
    root = Path(value)
    test.assertTrue(root.is_dir(), f"configured evidence root is missing: {root}")
    return root


class PhantomDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = read_json(MACHINE)
        cls.report = read_json(REPORT)
        cls.manual = read_json(ROOT / curator.MANUAL_DATA)
        cls.places = read_json(ROOT / curator.PLACES)
        cls.switches = bindings(cls.machine, "inputs", "pinmame.input.switch")
        cls.lamps = bindings(cls.machine, "outputs", "pinmame.output.lamp")
        cls.solenoids = bindings(cls.machine, "outputs", "pinmame.output.solenoid")

    def test_identity_and_driver_family(self):
        identity = self.machine["machine"]
        for key, value in {
            "id": ID, "name": "Phantom of the Opera", "manufacturer": "Data East",
            "year": 1990, "ipdb_id": 1777, "opdb_id": "Grq1D-MQokp",
            "model_number": "500-5508-01",
        }.items():
            self.assertEqual(value, identity[key], key)
        drivers = {d["id"]: d for d in self.machine["drivers"]}
        self.assertEqual(DRIVERS, set(drivers))
        for driver in ("poto_a29", "poto_a31"):
            self.assertEqual("poto_a32", drivers[driver]["clone_of"])
        self.assertFalse(drivers["poto_a32"].get("clone_of"))
        self.assertTrue(all(d["physical_compatibility"] == "identical"
                            for d in drivers.values()))

    def test_complete_public_address_spaces(self):
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)},
                         set(self.switches))
        self.assertEqual({0}, set(bindings(
            self.machine, "inputs", "pinmame.input.dip")))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(
            [(0, 0, 16), (1, 20, 16)],
            sorted((d["controller_index"], d["segment_start"], d["width"])
                   for d in self.machine["displays"]),
        )

    def assert_factory_jumper_contract(self, machine):
        dip = bindings(machine, "inputs", "pinmame.input.dip")[0]
        self.assertEqual("dip.emulator-configuration-0", dip["id"])
        self.assertIn("J8", dip["label"])
        self.assertEqual("CPU board in backbox", dip["physical"]["location"])
        self.assertEqual("dip_switch", dip["spatial"]["reason"])
        self.assertEqual("candidate", dip["provenance"]["status"])
        self.assertIn("input_semantics", machine["coverage"]["missing"])
        notes = dip["physical"]["notes"]
        for fact in ("J8 installed", "PA7 pin 9", "RA4 4.7K", "value 0", "purpose remains unresolved"):
            self.assertIn(fact, notes)
        for false_claim in ("no W7 country jumper", "not a fitted physical DIP or country jumper"):
            self.assertNotIn(false_claim, notes)

    def test_factory_jumper_is_physical_with_unresolved_firmware_purpose(self):
        self.assert_factory_jumper_contract(self.machine)
        table = self.manual["cpu_jumper_table"]
        self.assertEqual(9, len(table))
        self.assertEqual("", table[1][0])
        phantom = next(row for row in table if row[0] == "Phantom of the Opera")
        self.assertEqual(["Ver 2", "5B,5C"], phantom[1:3])
        self.assertEqual("J1b,J3,J4,J5b,J6b,J7b,&J8", phantom[3])
        self.assertEqual("J1a,J2,J5,J5a,J6a,&J7a", phantom[4])

    def test_factory_jumper_guard_rejects_the_previous_false_claim(self):
        wrong = copy.deepcopy(self.machine)
        dip = bindings(wrong, "inputs", "pinmame.input.dip")[0]
        dip["physical"]["notes"] = "No W7 country jumper is fitted on this net."
        dip["spatial"]["reason"] = "no_physical_device"
        with self.assertRaises(AssertionError):
            self.assert_factory_jumper_contract(wrong)

    def assert_motor_parts_provenance(self, machine):
        source = next(s for s in machine["sources"] if s["id"] == MANUAL)
        rows = [e for e in source["excerpts"] if e["path"].endswith("/playfield-parts.md")]
        self.assertEqual(1, len(rows))
        self.assertIn("rows 1-74", rows[0]["locator"])
        parts = self.manual["playfield_parts"]
        self.assertEqual(list(range(1, 75)), [row[0] for row in parts])
        self.assertEqual([1, "Organ Motor", "041-5001-00"], parts[0])
        motor = bindings(machine, "outputs", "pinmame.output.solenoid")[14]
        self.assertEqual(parts[0][2], motor["physical"]["part_number"])
        self.assertIn(MANUAL, motor["provenance"]["source_refs"])

    def test_motor_part_has_complete_list_provenance(self):
        self.assert_motor_parts_provenance(self.machine)

    def test_motor_parts_guard_rejects_a_missing_excerpt(self):
        wrong = copy.deepcopy(self.machine)
        source = next(s for s in wrong["sources"] if s["id"] == MANUAL)
        source["excerpts"] = [e for e in source["excerpts"] if not e["path"].endswith("/playfield-parts.md")]
        with self.assertRaises(AssertionError):
            self.assert_motor_parts_provenance(wrong)

    def test_switch_fitment_construction_and_organ_limits(self):
        unused = {2, 8, 9, 24, 32, 38, 39, 40, *range(54, 65)}
        self.assertEqual(unused, {
            n for n in range(1, 65)
            if self.switches[n]["availability"] == "unused"
        })
        self.assertEqual(unused, {
            n for n, label in enumerate(self.manual["switch_matrix"], 1)
            if label == "Not Used"
        })
        for n in set(range(1, 65)) - unused - {15, 16}:
            self.assertIs(self.switches[n]["normally_closed"], False, n)
        for n in (-7, -6, 82, 84):
            self.assertIs(self.switches[n]["normally_closed"], False, n)
        for n, label, initial in ((52, "Organ Open", False),
                                  (53, "Organ Closed", True)):
            switch = self.switches[n]
            self.assertEqual(label, switch["label"])
            self.assertEqual("180-5052-00", switch["physical"]["part_number"])
            self.assertIs(switch["initial_active"], initial)
        organ = next(m for m in self.machine["mechanisms"]
                     if m["id"] == "mechanism.organ")
        positions = {p["id"]: p["sensors"] for p in organ["positions"]}
        self.assertEqual(["switch.matrix-52"], positions["open"])
        self.assertEqual(["switch.matrix-53"], positions["closed"])
        self.assertIn("coil.driver-14", organ["actuators"])

    def test_special_mapping_and_no_matrix_to_special_coil_causality(self):
        # Public addresses are a Data East permutation, not SP-number order.
        for public, sp, transistor in (
            (17, 1, "Q8"), (18, 3, "Q10"), (19, 4, "Q11"),
            (20, 6, "Q13"), (21, 5, "Q12"), (22, 2, "Q9"),
        ):
            output = self.solenoids[public]
            aliases = {(a["namespace"], a["value"]) for a in output["aliases"]}
            self.assertIn(("manual.address", f"SP{sp}"), aliases)
            self.assertEqual(transistor, output["wiring"]["driver_transistor"])
            self.assertEqual("unknown" if sp == 6 else "used",
                             output["availability"])
        matrix = {f"switch.matrix-{n}" for n in (21, 22, 46, 47, 48)}
        special = {f"coil.driver-{n}" for n in (17, 18, 19, 21, 22)}
        for relation in self.machine["relationships"]:
            self.assertFalse(relation["source"] in matrix
                             and relation["destination"] in special, relation)

    def test_flipper_copy_and_synthetic_outputs(self):
        relations = {(r["source"], r["destination"], r["kind"])
                     for r in self.machine["relationships"]}
        for column, matrix in ((82, 16), (84, 15)):
            self.assertIn((f"switch.flipper-column-{column}",
                           f"switch.matrix-{matrix}", "direct"), relations)
            self.assertEqual("used", self.switches[column]["availability"])
        for n in range(45, 49):
            output = self.solenoids[n]
            self.assertEqual(("virtual", "used"),
                             (output["kind"], output["availability"]))
            self.assertEqual("virtual", output["spatial"]["reason"])

    def test_relay_motor_and_unfitted_branches(self):
        mux, gi, motor = (self.solenoids[n] for n in (10, 11, 14))
        self.assertEqual(("relay", "Q29", "PPB J6-9"),
                         (mux["kind"], mux["wiring"]["driver_transistor"],
                          mux["wiring"]["drive_connection"]))
        self.assertEqual(("gi", "Q28", "PS CN7-1"),
                         (gi["kind"], gi["wiring"]["driver_transistor"],
                          gi["wiring"]["drive_connection"]))
        self.assertEqual(("motor", "Q25", 25, "ac"),
                         (motor["kind"], motor["wiring"]["driver_transistor"],
                          motor["wiring"]["nominal_voltage_v"],
                          motor["wiring"]["voltage_type"]))
        self.assertEqual("500-5212-00-08",
                         motor["physical"]["assembly_part_number"])
        self.assertEqual({20}, {n for n, d in self.solenoids.items()
                                if d["availability"] == "unknown"})
        for n in (30, 31, 32):
            self.assertEqual("unused", self.solenoids[n]["availability"])
            self.assertEqual("no_physical_device",
                             self.solenoids[n]["spatial"]["reason"])
        self.assertEqual("virtual", self.solenoids[32]["kind"])
        self.assertFalse(any(d["kind"] == "knocker"
                             for d in self.machine["outputs"]))

    def test_flashers_match_printed_totals_and_backbox_inset(self):
        backbox = {1: 3, 2: 1, 3: 0, 4: 1, 5: 3, 6: 2,
                   7: 2, 8: 2, 9: 0, 12: 0, 13: 0, 15: 2}
        self.assertEqual(16, sum(backbox.values()))
        for n, count in backbox.items():
            output = self.solenoids[n]
            total = 3 if n == 1 else 4
            self.assertEqual(("flasher", total),
                             (output["kind"], output["physical"]["quantity"]))
            location = ("backbox" if count == total else
                        "playfield and backbox" if count else "playfield")
            self.assertEqual(location, output["physical"]["location"])
            row = next(r for r in self.manual["driver_rows"] if r[0] == n)
            self.assertEqual(total, row[8])
        self.assertEqual("cabinet_or_service",
                         self.solenoids[1]["spatial"]["reason"])

    def test_output20_static_boundary_keeps_unknown(self):
        output = self.solenoids[20]
        self.assertEqual("unknown", output["availability"])
        self.assertIn(curator.ROM_ANALYSIS, output["provenance"]["source_refs"])
        sources = {s["id"]: s for s in self.machine["sources"]}
        source = sources[curator.ROM_ANALYSIS]
        self.assertEqual("human_review", source["kind"])
        self.assertEqual(curator.PIN, source["revision"])
        excerpt = (ROOT / source["excerpts"][0]["path"]).read_text(encoding="utf-8")
        for address in ("$2401", "$0102", "$4C96", "$4CA3", "$45ED"):
            self.assertIn(address, excerpt)
        self.assertIn("Dynamic targets and indexed-store base/value ranges were not resolved", excerpt)
        blocker = next(b for b in self.report["blockers"] if b["dimension"] == "output_semantics")
        self.assertEqual(["coil.driver-20"], blocker["devices"])
        self.assertIn("$45ED", blocker["would_resolve"])

    def test_lamps_and_candidate_geometry(self):
        self.assertEqual("Right Circle", self.manual["lamp_matrix"][24])
        self.assertEqual("Left Circle", self.lamps[25]["label"])
        self.assertEqual("unused", self.lamps[56]["availability"])
        self.assertEqual("unused", self.lamps[56]["spatial"]["reason"])
        for n in (39, 40, 47, 48):
            self.assertEqual("cabinet_or_service",
                             self.lamps[n]["spatial"]["reason"])
        for n in range(49, 56):
            self.assertNotIn("placements", self.lamps[n].get("spatial", {}))
            self.assertIn("rear", self.lamps[n]["physical"]["location"].lower())
        inserts = {*range(1, 39), *range(41, 47), *range(57, 65)}
        self.assertEqual(inserts, set(map(int, self.places["lamps"])))
        for n in inserts:
            spatial = self.lamps[n]["spatial"]
            self.assertEqual("candidate", spatial["status"])
            self.assertEqual(1, len(spatial["placements"]))
            self.assertEqual("candidate",
                             spatial["placements"][0]["provenance"]["status"])
        gi = self.solenoids[11]
        self.assertNotIn("quantity", gi["physical"])
        self.assertEqual(12, len(gi["spatial"]["placements"]))
        blockers = {b["dimension"]: b for b in self.report["blockers"]}
        self.assertIn("coil.driver-11", blockers["spatial_placement"]["devices"])

    def test_partial_gate_and_catalog_reconciliation(self):
        missing = {"input_semantics", "output_semantics", "spatial_placement"}
        self.assertEqual("partial", self.machine["coverage"]["status"])
        self.assertEqual(missing, set(self.machine["coverage"]["missing"]))
        self.assertEqual(missing, {b["dimension"] for b in self.report["blockers"]})
        self.assertFalse(self.report["promotion_decision"]["author_ready"])
        self.assertEqual("partial", self.report["promotion_decision"]["status"])
        catalog = read_json(ROOT / "catalog/pinmame.json")
        rows = [r for r in catalog["machines"] if r["id"] == ID]
        self.assertEqual(1, len(rows))
        self.assertEqual(content_sha256(self.machine), rows[0]["definition_sha256"])
        self.assertEqual("partial", rows[0]["coverage_status"])
        self.assertEqual(missing, set(rows[0]["missing"]))
        claimed = [d for d in catalog["drivers"] if d["machine_id"] == ID]
        self.assertEqual(DRIVERS, {d["id"] for d in claimed})
        self.assertEqual(3, len(claimed))
        for path in (ROOT / "machines/stubs").rglob("*.json"):
            stub = read_json(path)
            self.assertNotEqual(ID, stub["machine"]["id"], str(path))
            self.assertFalse(DRIVERS & {d["id"] for d in stub.get("drivers", [])},
                             str(path))

    def test_pinned_sources_and_excerpt_digests(self):
        sources = {s["id"]: s for s in self.machine["sources"]}
        for source_id, sha in PINS.items():
            self.assertEqual(sha, sources[source_id]["sha256"], source_id)
        self.assertTrue(sources[SCRIPT]["known_working"])
        self.assertEqual("46e1a01a0f73dc5ce163d98db1ae435883ecc450",
                         sources[CORE]["revision"])
        self.assertEqual(PINS[MANUAL], self.manual["manual_sha256"])
        self.assertEqual(PINS[SCRIPT], self.places["source_sha256"])
        excerpt_paths = set()
        for source in sources.values():
            for excerpt in source.get("excerpts", []):
                path = ROOT / excerpt["path"]
                self.assertTrue(path.is_file(), str(path))
                self.assertEqual(excerpt["sha256"], digest(path), str(path))
                self.assertTrue(excerpt["method"])
                self.assertTrue(excerpt["transcribed_by"])
                if excerpt.get("image"):
                    self.assertEqual(excerpt["image_sha256"], digest(ROOT / excerpt["image"]))
                    self.assertTrue(excerpt["image_derivation"])
                excerpt_paths.add(path.name)
        self.assertTrue({"switch-matrix.md", "lamp-matrix.md",
                         "coil-and-flipper.md", "script-bindings.md",
                         "mechanism-construction.md",
                         "vpm-script-library-flippers.md"} <= excerpt_paths)

    def test_rom_names_and_synthetic_organ_contract(self):
        sources = {s["id"]: s for s in self.machine["sources"]}
        for source_id, path, expected in (
            (curator.SERVICE, curator.SERVICE_EVIDENCE, curator.SERVICE_SHA),
            (curator.ORGAN, curator.ORGAN_EVIDENCE, curator.ORGAN_SHA),
        ):
            self.assertEqual(expected, digest(ROOT / path))
            self.assertEqual(expected, sources[source_id]["sha256"])
        for n in (30, 31, 32):
            aliases = {(a["namespace"], a["value"]) for a in self.solenoids[n]["aliases"]}
            self.assertIn(("rom.diagnostic.name", "UNUSED   COIL"), aliases)
        organ = read_json(ROOT / curator.ORGAN_EVIDENCE)
        runs = organ["runtime"]["observations"]["runs"]
        self.assertEqual({"closed-narrow", "closed-wide", "midway-narrow",
                          "midway-wide", "jammed-no-limits"}, set(runs))
        for name, run in runs.items():
            summary = json.loads(run["note"])
            cycles = summary["automatic_cycles"]
            endpoints = [(c["host_52_at_stop"], c["host_53_at_stop"]) for c in cycles]
            if name == "jammed-no-limits":
                self.assertEqual([(0, 0)] * 3, endpoints)
                self.assertTrue(all(5.5 < c["powered_duration_s"] < 6.5 for c in cycles))
            else:
                self.assertEqual(([(0, 1)] if name.startswith("midway") else [])
                                 + [(1, 0), (0, 1)], endpoints)
            self.assertGreaterEqual(summary["organ_test_motor_pulses"], 10)
            self.assertIn("synthetic host feedback", run["limitation"])


class PhantomCuratorGuards(unittest.TestCase):
    def run_check(self):
        with mock.patch.object(sys, "argv", ["curator", "--check"]), \
             mock.patch.object(curator, "verify_external"):
            return curator.main()

    def test_check_twice_without_regeneration(self):
        self.assertEqual(0, self.run_check())
        self.assertEqual(0, self.run_check())

    def test_check_rejects_artifact_drift(self):
        with mock.patch.object(curator, "desired",
                               return_value={curator.MACHINE: "wrong\n"}):
            with self.assertRaises(SystemExit):
                self.run_check()

    def test_check_rejects_author_ready_artifact(self):
        original_exists = Path.exists

        def exists(path):
            if path == ROOT / "machines/author-ready/data-east" / f"{SLUG}.json":
                return True
            return original_exists(path)

        with mock.patch.object(Path, "exists", exists):
            with self.assertRaises(ValueError):
                self.run_check()

    def test_check_rejects_bad_pins_and_incomplete_matrix(self):
        original_load = curator.load_json
        for mutation in ("manual_pin", "script_pin", "matrix", "manual_mapping", "motor_part", "jumper_factory"):
            def load(path):
                data = original_load(path)
                if path == ROOT / curator.MANUAL_DATA:
                    data = copy.deepcopy(data)
                    if mutation == "manual_pin":
                        data["manual_sha256"] = "0" * 64
                    if mutation == "matrix":
                        data["switch_matrix"].pop()
                    if mutation == "manual_mapping":
                        data["switch_matrix"][51] = "Organ Closed"
                    if mutation == "motor_part":
                        data["playfield_parts"][0][2] = "wrong"
                    if mutation == "jumper_factory":
                        data["cpu_jumper_table"][-1][3] = "J8 removed"
                if path == ROOT / curator.PLACES and mutation == "script_pin":
                    data = copy.deepcopy(data)
                    data["source_sha256"] = "0" * 64
                return data

            with self.subTest(mutation=mutation), \
                 mock.patch.object(curator, "load_json", side_effect=load):
                with self.assertRaises(ValueError):
                    self.run_check()

    def test_check_rejects_compact_runtime_drift(self):
        original = curator.sha
        for target in (curator.SERVICE_EVIDENCE, curator.ORGAN_EVIDENCE):
            with self.subTest(target=target), mock.patch.object(
                curator, "sha", side_effect=lambda path: "0" * 64 if path == ROOT / target else original(path)
            ):
                with self.assertRaises(ValueError):
                    self.run_check()

    def test_each_configured_wrong_source_root_is_rejected(self):
        for variable in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT",
                         "PINMAME_REVIEW_ARTIFACTS_ROOT"):
            with self.subTest(variable=variable), \
                 mock.patch.dict(os.environ, {
                     variable: str(ROOT / "__nonexistent_phantom_evidence_root__")
                 }, clear=True):
                with self.assertRaises(ValueError):
                    curator.verify_external()


class PhantomRetainedEvidenceTests(unittest.TestCase):
    def test_output20_analysis_manifest(self):
        root = retained_root(self, "PINMAME_REVIEW_ARTIFACTS_ROOT")
        self.assertEqual(curator.ROM_ANALYSIS_SHA,
                         check_manifest(root / SLUG / "output20-re", "poto_a32"))

    def test_vpx_hashes_and_full_extraction_manifest(self):
        base = retained_root(self, "PINMAME_VPX_SOURCES_ROOT") / "data-east" / SLUG
        for name, expected in (
            ("Phantom Of The Opera (Data East 1990) v1.25.vpx", PINS[TABLE]),
            ("extracted/script.vbs", PINS[SCRIPT]),
            ("de.vbs", PINS["vpm-script-library.phantom-de-vbs"]),
            ("core.vbs", "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69"),
        ):
            self.assertEqual(expected, digest(base / name), name)
        extraction = base / "extracted"
        self.assertEqual(PINS[EXTRACTION], check_manifest(extraction, "poto_a32"))
        manifest = read_json(extraction / "manifest.json")
        self.assertEqual(2699, len(manifest["files"]))
        self.assertEqual(272164712, sum(f["size"] for f in manifest["files"]))

    def test_manual_capture(self):
        manual_root = retained_root(self, "PINMAME_MANUALS_ROOT")
        path = (manual_root / "by-machine" / ID / "ipdb-1777" /
                "Data_East_1990_Phantom_of_the_Opera_English_Manual_with_paginated_schematics.pdf")
        self.assertEqual(PINS[MANUAL], digest(path))

    def test_owner_capture(self):
        root = retained_root(self, "PINMAME_REVIEW_ARTIFACTS_ROOT")
        self.assertEqual(PINS["human-review.phantom-knocker-owners"],
                         digest(root / SLUG / "pinside-knocker-page.json"))

    def test_raw_objects_reproduce_coordinates(self):
        base = retained_root(self, "PINMAME_VPX_SOURCES_ROOT") / "data-east" / SLUG
        extraction = base / "extracted"
        game = read_json(extraction / "gamedata.json")
        self.assertEqual((0, 0, 952, 2162),
                         tuple(game[k] for k in ("left", "top", "right", "bottom")))
        machine = read_json(MACHINE)
        lamps = bindings(machine, "outputs", "pinmame.output.lamp")
        switches = bindings(machine, "inputs", "pinmame.input.switch")
        places = read_json(ROOT / curator.PLACES)

        def point(path, kind, field):
            obj = read_json(extraction / "gameitems" / path)[kind]
            raw = obj[field]
            return (round((raw["x"] - game["left"]) /
                          (game["right"] - game["left"]), 6),
                    round((raw["y"] - game["top"]) /
                          (game["bottom"] - game["top"]), 6))

        for n in map(int, places["lamps"]):
            placement = lamps[n]["spatial"]["placements"][0]
            self.assertEqual(point(f"Light.l{n}.json", "Light", "center"),
                             (placement["x"], placement["y"]), n)
        for n, filename, kind, field in (
            (14, "Trigger.sw14.json", "Trigger", "center"),
            (33, "HitTarget.sw33.json", "HitTarget", "position"),
            (46, "Bumper.Bumper1.json", "Bumper", "center"),
            (47, "Bumper.Bumper3.json", "Bumper", "center"),
            (48, "Bumper.Bumper2.json", "Bumper", "center"),
        ):
            placement = switches[n]["spatial"]["placements"][0]
            self.assertEqual(point(filename, kind, field),
                             (placement["x"], placement["y"]), n)
        gi = bindings(machine, "outputs", "pinmame.output.solenoid")[11]
        actual = [(p["x"], p["y"]) for p in gi["spatial"]["placements"]]
        expected = [point(item["file"], "Light", "center")
                    for item in places["gi_bulb_candidates"]]
        self.assertEqual(expected, actual)
        solenoids = bindings(machine, "outputs", "pinmame.output.solenoid")
        for n, filename, kind in ((16, "Plunger.Plunger1.json", "Plunger"),
                                  (26, "Kicker.BallRelease.json", "Kicker")):
            placement = solenoids[n]["spatial"]["placements"][0]
            self.assertEqual(point(filename, kind, "center"),
                             (placement["x"], placement["y"]), n)


if __name__ == "__main__":
    unittest.main()
