"""Regression gates for Baywatch's physical revision, public paths and retained evidence.

The fixtures below protect independently read facts rather than copying the curator's arrays.
External gates recompute manifests, raw observations and geometry when evidence roots are supplied.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import curate_baywatch as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json

KEY = "sega.baywatch.1995"
RUNTIME = ROOT / "evidence/runtime/data-east/baywatch-usa-400-service-tests.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def devices(definition, field, group):
    return {d["binding"]["device"]: d for d in definition[field] if d["binding"]["group"] == group}


class BaywatchDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = load_json(curator.DEFINITION_PATH)
        cls.switches = devices(cls.definition, "inputs", "pinmame.input.switch")
        cls.coils = devices(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = devices(cls.definition, "outputs", "pinmame.output.lamp")
        cls.sources = {s["id"]: s for s in cls.definition["sources"]}
        cls.places = load_json(ROOT / "tools/baywatch_places.json")
        cls.runtime = load_json(RUNTIME)["runtime"]

    def test_identity_variants_and_controller_are_data_east_3b(self):
        machine = self.definition["machine"]
        self.assertEqual((KEY, 2848, "33", "Grxvy-M4oZj"),
                         (machine["id"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"]))
        self.assertEqual({"baywatch", "bay_d300", "bay_d400", "bay_e400", "bay_f201",
                          "bay_g300", "bay_401", "bay_402"}, {d["id"] for d in self.definition["drivers"]})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.definition["drivers"]))
        self.assertEqual("pinmame.dataeast", self.definition["controller"]["platform"])
        self.assertEqual("0x8000", self.definition["controller"]["hardware_generation"])
        self.assertEqual([(192, 64)], [(d["width"], d["height"]) for d in self.definition["displays"]])

    def test_entire_public_inventory_and_availability(self):
        self.assertEqual({-7, -6, *range(1, 65), *range(81, 89)}, set(self.switches))
        self.assertEqual(75, len(self.definition["inputs"]))  # includes country bit zero
        self.assertEqual(set(range(1, 65)), set(self.coils))
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        self.assertEqual({27, 29, 34, 35, 51}, {n for n in range(1, 65) if self.switches[n]["availability"] == "unused"})
        self.assertEqual({15, *range(37, 45)}, {n for n, d in self.coils.items() if d["availability"] == "unknown"})
        self.assertEqual({24, *range(33, 37), *range(49, 65)}, {n for n, d in self.coils.items() if d["availability"] == "unused"})
        self.assertIn("Unassigned", self.coils[15]["label"])
        self.assertIn("gameplay", self.coils[15]["physical"]["notes"])
        self.assertIn(curator.RUNTIME, self.coils[15]["provenance"]["source_refs"])
        self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))

    def test_physical_opto_and_service_polarity_are_separate(self):
        opto = self.switches[15]
        self.assertEqual("opto", opto["physical"]["switch_type"])
        self.assertIs(False, opto["normally_closed"])
        self.assertIn("blocked beam = closed", opto["physical"]["notes"])
        for n in (-7, -6):
            self.assertIs(False, self.switches[n]["normally_closed"])
            self.assertTrue(self.switches[n]["pulse"])
            self.assertIn(curator.BULLETIN, self.switches[n]["provenance"]["source_refs"])
        country = devices(self.definition, "inputs", "pinmame.input.dip")[0]
        self.assertEqual("unknown", country["availability"])
        self.assertNotIn("polarity", self.definition["coverage"]["missing"])

    def test_cabinet_buttons_drive_the_copy_and_synthetic_pairs(self):
        for button, matrix, side in ((84, 63, "left"), (82, 64, "right")):
            self.assertEqual("used", self.switches[button]["availability"])
            self.assertIn(str(button), self.switches[matrix]["physical"]["notes"])
            links = [r for r in self.definition["relationships"] if r["source"] == self.switches[button]["id"]]
            self.assertEqual([self.switches[matrix]["id"]], [r["destination"] for r in links])
            self.assertIn(side, self.switches[button]["label"].lower())
        for n in (81, 83, 85, 86, 87, 88):
            self.assertEqual("unused", self.switches[n]["availability"])
        pairs = [a for a in self.runtime["observations"]["runs"]["gameplay-other-mechanisms"]["named_action_observations"]
                 if "held_synthetic_solenoid_addresses" in a]
        self.assertEqual({84: {47, 48}, 82: {45, 46}},
                         {p["input_address"]: set(p["held_synthetic_solenoid_addresses"]) for p in pairs})

    def test_literal_coil_parts_and_connector_cells_do_not_follow_siblings(self):
        parts = {1: "25-1240", 2: "23-800", 3: "23-800", 4: "24-940",
                 5: "24-940", 6: "24-940", 7: "24-940", 12: "27-950",
                 16: "23-800", 22: "23-700"}
        for n, part in parts.items():
            self.assertEqual(part, self.coils[n]["physical"]["part_number"], n)
        for n in (17, 18, 19):
            self.assertEqual("PS CN3-6", self.coils[n]["wiring"]["power_connection"])
        for n in (20, 21, 22):
            self.assertEqual("PS CN6-6,7", self.coils[n]["wiring"]["power_connection"])
        self.assertEqual("CN7-5", self.lamps[33]["wiring"]["drive_connection"])
        for n in range(33, 41):
            self.assertIn("pin 6", self.lamps[n]["physical"]["notes"])
        self.assertIn("PS CN3-6 | 32v | 23-700", (curator.EXCERPTS / "coils.md").read_text(encoding="utf-8"))
        self.assertIn("50v Q1,Q10", (curator.EXCERPTS / "coils.md").read_text(encoding="utf-8"))

    def test_upper_flippers_have_two_physical_coils_and_parallel_controls(self):
        upper = self.coils[13]
        self.assertEqual(2, upper["physical"]["quantity"])
        self.assertIn("LT 24-1570 RT 23-1100", upper["physical"]["part_number"])
        self.assertEqual({"LeftFlipper1", "RightFlipper1"},
                         {p["object"] for p in self.places["placements"]["solenoid.13"]})
        self.assertIn("N.O. cabinet buttons", upper["physical"]["notes"])
        self.assertIn("diode-isolated CPU input in parallel", upper["physical"]["notes"])
        self.assertEqual("No causal 54-to-13 proof is asserted from this run.",
                         self.runtime["observations"]["runs"]["shark-service"]["limitation"])

    def test_mechanism_ownership_and_three_eject_routes(self):
        by_id = {d["id"]: n for n, d in self.coils.items()}
        sw_id = {d["id"]: n for n, d in self.switches.items()}
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        expected = {"trough": ({1, 2}, {10, 11, 12, 13, 14, 15}),
                    "auto-launch": ({3}, {16, 50}), "upper-launch": ({4}, {47}),
                    "upper-vuk": ({5}, {44}), "lower-vuk": ({6}, {55, 46}),
                    "shark-scoop": ({7}, {56}), "tower-trapdoor": ({12}, {25, 26, 55, 46}),
                    "drops": ({16}, {22, 23, 24}), "laser-kick": ({22}, {57})}
        for name, (coils, switches) in expected.items():
            m = mechanisms["mech." + name]
            self.assertEqual(coils, {by_id[n] for n in m["actuators"]}, name)
            self.assertEqual(switches, {sw_id[n] for n in m["sensors"]}, name)
        owned = [a for m in mechanisms.values() for a in m["actuators"]]
        self.assertEqual(len(owned), len(set(owned)))
        self.assertEqual(set(), {d["id"] for d in self.coils.values() if d["kind"] in ("coil", "relay") and d["availability"] == "used"} - set(owned))
        self.assertGreater(self.places["placements"]["solenoid.3"][0]["y"],
                           self.places["placements"]["solenoid.4"][0]["y"])

    def test_trough_serves_lane_before_the_separate_launcher(self):
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        trough = mechanisms["mech.trough"]["behavior"]
        launch = mechanisms["mech.auto-launch"]["behavior"]
        self.assertIn("output 2 lifts that ball to shooter lane 16", trough)
        self.assertIn("Output 3 then launches it onto the elevated shooter wire ramp", trough)
        self.assertNotRegex(trough, r"output 2[^.]*to the shooter wire ramp")
        self.assertIn("Output 3 fires Plunger1", launch)
        self.assertIn("feeding the elevated shooter wire ramp", launch)

    def test_printer_comment_does_not_supply_elided_connector_pins(self):
        for address, pin in {37: 9, 38: 8, 39: 7, 44: 1}.items():
            self.assertIn(f"explicitly names CN3 pin {pin}", self.coils[address]["physical"]["notes"])
        for address in range(37, 45):
            self.assertEqual("unknown", self.coils[address]["availability"])
            self.assertIn(f"PIA2:B bit {address - 37}", self.coils[address]["physical"]["notes"])
        for address in range(40, 44):
            notes = self.coils[address]["physical"]["notes"]
            self.assertNotRegex(notes, r"(?i)CN3[- ](?:pin[- ]*)?\d")
            self.assertNotIn("wiring", self.coils[address])
            self.assertIn("elides bits 3-6", notes)
        excerpt = (curator.EXCERPTS / "controller.md").read_text(encoding="utf-8")
        self.assertNotIn("pin 2 is skipped", excerpt)
        self.assertIn("literal `....` elides bits 3-6", excerpt)

    def test_public_artifacts_use_neutral_provenance(self):
        for source in self.sources.values():
            for excerpt in source.get("excerpts", []):
                self.assertTrue(excerpt["transcribed_by"].startswith("Curator;"))
        for filename in ("coils.md", "drawings.md", "lamps.md", "mechanisms.md",
                         "script-bindings.md", "switches.md"):
            attribution = (curator.EXCERPTS / filename).read_text(encoding="utf-8").splitlines()[2]
            self.assertRegex(attribution, r"(?i)\bcurator\b", filename)
        photos = (curator.EXCERPTS / "physical-photos.md").read_text(encoding="utf-8")
        receipt = re.search(r"`(photo-receipts\.[a-z]+)`", photos)[1]
        self.assertTrue((curator.EXCERPTS / receipt).is_file())

    def test_elevated_lamp_discrepancy_is_explicit_without_replacing_observed_points(self):
        report = load_json(curator.SPATIAL_REPORT_PATH)
        comparison = report["drawing_table_comparison"]
        self.assertEqual(curator.drawing_comparison(self.places), comparison)
        self.assertEqual({"left": 335.5, "right": 1594.5, "rear": 140.5, "front": 3001.5},
                         comparison["comparison_rectangle_px"])
        # Independent arithmetic: drawing pixels, not a fit to the table controls.
        for point in comparison["floor_controls"] + comparison["elevated_lamps"]:
            px, py = point["centre_px"]
            self.assertEqual([round((px - 335.5) / 1259, 6), round((py - 140.5) / 2861, 6)],
                             point["drawing_normalized"])
        floor_delta = max(abs(v) for p in comparison["floor_controls"] for v in p["table_minus_drawing"])
        self.assertLess(floor_delta, .006)
        self.assertEqual({12, 33, 34, 35}, {p["address"] for p in comparison["elevated_lamps"]})
        self.assertIn("elevated-lamp-drawing-table-difference", {b["id"] for b in report["blockers"]})
        for point in comparison["elevated_lamps"]:
            n = point["address"]
            self.assertGreater(abs(point["table_minus_drawing"][1]), .09)
            lamp = self.lamps[n]
            self.assertIn("Unreconciled drawing/table position", lamp["physical"]["notes"])
            self.assertIn("unquantified projection uncertainty", lamp["physical"]["notes"])
            self.assertIn(curator.DRAWING_COMPARISON, lamp["provenance"]["source_refs"])
            self.assertEqual("observed", lamp["spatial"]["status"])
            placement = lamp["spatial"]["placements"][0]
            self.assertEqual(point["table_normalized"], [placement["x"], placement["y"]])
            self.assertIn(curator.DRAWING_COMPARISON, placement["provenance"]["source_refs"])
        self.assertEqual(["conflict.flasher-bulb-composition"], [c["id"] for c in self.definition["conflicts"]])
        self.assertEqual(digest(ROOT / "tools/baywatch_lamp_drawing.json"),
                         self.sources[curator.DRAWING_COMPARISON]["sha256"])

    def test_socket_counts_and_categories_exclude_render_doubles(self):
        self.assertEqual(2, self.lamps[25]["physical"]["quantity"])
        self.assertEqual({"lL25", "lR25"}, {p["object"] for p in self.places["placements"]["lamp.25"]})
        for n in range(25, 33):
            self.assertEqual(4, self.coils[n]["physical"]["quantity"])
            if n in (26,31):
                self.assertEqual("Bulb #89", self.coils[n]["physical"]["part_number"])
            else:
                self.assertNotIn("part_number", self.coils[n]["physical"])
                self.assertEqual("conflicted", self.coils[n]["provenance"]["status"])
                self.assertIn("conflict.flasher-bulb-composition", self.coils[n]["physical"]["notes"])
        for n in (6, 11, 12, 13, 33, 34, 35):
            self.assertEqual([f"BulboF{n}"], [p["object"] for p in self.places["placements"][f"lamp.{n}"]])
        for n in (7, 8, 64):
            self.assertEqual("cabinet_or_service", self.lamps[n]["spatial"]["reason"])
        gi = self.coils[11]
        self.assertEqual("gi", gi["kind"])
        self.assertNotIn("quantity", gi["physical"])
        self.assertEqual(35, len(gi["spatial"]["placements"]))
        self.assertNotIn("solenoid.29", self.places["placements"])
        self.assertEqual(1, len(self.places["placements"]["solenoid.30"]))
        self.assertEqual({"DomeBW191", "DomeBW191a"}, {p["object"] for p in self.places["placements"]["solenoid.25"]})

    def test_placements_are_observed_world_positions_with_explicit_omissions(self):
        for key, points in self.places["placements"].items():
            for p in points:
                self.assertNotEqual("Flasher", p["type"], key)
                self.assertEqual(round(p["raw_x"] / 952, 6), p["x"])
                self.assertEqual(round(p["raw_y"] / 2162, 6), p["y"])
                self.assertTrue(0 <= p["x"] <= 1 and 0 <= p["y"] <= 1, key)
                if p["type"] == "Primitive":
                    self.assertIn("world_mesh_bounds", p)
        for n in range(10, 15):
            self.assertNotIn("spatial", self.switches[n])
        self.assertNotIn("spatial", self.coils[1])
        self.assertEqual({"Bumper1", "Bumper2", "Bumper3"}, {c["anchor"] for c in self.places["mesh_controls"]})
        self.assertTrue(all(abs(c[axis]) <= 2 for c in self.places["mesh_controls"] for axis in ("dx", "dy")))
        report = load_json(curator.SPATIAL_REPORT_PATH)
        self.assertEqual(self.places["mechanical_anchors"], report["mechanical_anchors"])
        self.assertEqual("partial", report["status"])

    def test_complete_reviewed_regions_and_drawing_crops_are_hash_bound(self):
        self.assertEqual(set(range(1, 65)), {int(r[0]) for r in curator.rows("switches.md", 5)})
        self.assertEqual(set(range(1, 65)), {int(r[0]) for r in curator.rows("lamps.md", 3)})
        self.assertEqual(30, len([r for r in curator.rows("coils.md", 10) if r[0] not in {"1", "2"}]))
        for source in self.sources.values():
            for excerpt in source.get("excerpts", []):
                self.assertEqual(digest(ROOT / excerpt["path"]), excerpt["sha256"])
                self.assertTrue(excerpt["reviewed"])
                if "image" in excerpt:
                    self.assertLessEqual((ROOT / excerpt["image"]).stat().st_size, 100_000)
                    self.assertEqual(digest(ROOT / excerpt["image"]), excerpt["image_sha256"])
        self.assertEqual(8, len([e for e in self.sources[curator.MANUAL]["excerpts"] if "image" in e]))

    def test_runtime_readings_and_checkpoints_keep_failure_boundaries(self):
        runtime = self.runtime
        self.assertEqual(digest(RUNTIME), self.sources[curator.RUNTIME]["sha256"])
        readings = runtime["observations"]["diagnostic_snapshots"]
        self.assertEqual(set(range(1, 65)), {int(re.search(r"#(\d+)$", r["interpreted_text"])[1])
                                          for r in readings if r["label"].startswith("lamp-")})
        game = runtime["observations"]["runs"]["gameplay-other-mechanisms"]
        self.assertEqual({1, 2, 3, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22},
                         {n for a in game["named_action_observations"] if "held_synthetic_solenoid_addresses" not in a
                          for n in a["transitioned_solenoid_addresses"]})
        self.assertIn(15, game["ordered_solenoid_on_sequence"])
        self.assertEqual(set(), set(runtime["observations"]["runs"]["printer-explore"]["solenoid_addresses_seen"]) & set(range(37, 45)))
        self.assertFalse(set(runtime["observations"]["runs"]) & {"gameplay", "gameplay-long-start", "gameplay-causal", "gameplay-serve-launch"})
        for run in runtime["raw_runs"]:
            self.assertEqual(run["scenario_sha256"], digest(ROOT / run["scenario_path"]))

    def test_no_sibling_record_leak_and_precise_partial_dimensions(self):
        catalog = load_json(ROOT / "catalog/pinmame.json")
        foreign = {d["id"] for d in catalog["drivers"] if d["machine_id"] != KEY}
        content = " ".join(p.read_text(encoding="utf-8") for p in
                           (curator.DEFINITION_PATH, curator.KNOWLEDGE_PATH, curator.SPATIAL_REPORT_PATH))
        # These real English terms are also other driver IDs; no sibling curator was used.
        self.assertEqual(set(), {t.lower() for t in re.findall(r"[A-Za-z0-9_]+", content)} & foreign - {"pinball", "real", "shark"})
        self.assertEqual({"input_semantics", "output_semantics", "spatial_placement", "unresolved_conflicts"},
                         set(self.definition["coverage"]["missing"]))
        self.assertEqual("conflict.flasher-bulb-composition", self.definition["conflicts"][0]["id"])
        self.assertIn("Resolution path:", self.definition["conflicts"][0]["description"])
        self.assertEqual("partial", self.definition["coverage"]["status"])

    def test_curator_seed_and_all_generated_artifacts_are_deterministic(self):
        first = curator.artifacts()
        self.assertEqual(first, curator.artifacts())
        for path, expected in first:
            self.assertEqual(expected.replace(b"\r\n", b"\n"), path.read_bytes().replace(b"\r\n", b"\n"), str(path))
        self.assertEqual(canonical_bytes(self.definition), curator.SEED_PATH.read_bytes().replace(b"\r\n", b"\n"))

    def test_curator_guards_fail_on_drift_missing_rows_and_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path, payload in curator.artifacts():
                target = root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            args = ["curate_baywatch.py", "--check", "--repository-root", str(root)]
            with patch.object(sys, "argv", args), patch.object(curator, "verify_external"):
                curator.main()
                drifted = root / curator.DEFINITION_PATH.relative_to(ROOT)
                saved = drifted.read_bytes()
                drifted.write_bytes(saved.replace(b"Trough Lock Ball", b"Wrong Trough Coil", 1))
                with self.assertRaisesRegex(ValueError, "drifted"):
                    curator.main()
                drifted.write_bytes(saved)
                ready = root / "machines/author-ready/sega/baywatch-1995.json"
                ready.parent.mkdir(parents=True)
                ready.write_text("{}")
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.main()
        with patch.object(curator, "rows", return_value=[]):
            with self.assertRaisesRegex(ValueError, "incomplete"):
                curator.build()


class BaywatchExternalRootGuardTests(unittest.TestCase):
    """Exercise optional-root routing and failure paths without scanning large raw bundles."""

    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for name in ("PINMAME_MANUALS_ROOT", "PINMAME_VPX_SOURCES_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"):
            os.environ.pop(name, None)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.repository = self.base / "repository"
        self.review = self.base / "review"
        self.vpx = self.base / "vpx"
        self.obj = self.review / KEY / "world-obj/Baywatch (Sega) 1.0.5.obj"
        self.obj.parent.mkdir(parents=True)
        self.obj.write_bytes(b"o Fixture\nv 1 2 3\n")
        self.places = {"obj_sha256": digest(self.obj), "placements": {"fixture": [1, 2]}}
        self.runtime = {"runtime": {"game": "baywatch"}}
        self.places_path = self.repository / "tools/baywatch_places.json"
        self.runtime_path = self.repository / "evidence/runtime/data-east/baywatch-usa-400-service-tests.json"
        for path, data in ((self.places_path, self.places), (self.runtime_path, self.runtime)):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data), encoding="utf-8")
        root = patch.object(curator, "ROOT", self.repository)
        root.start()
        self.addCleanup(root.stop)
        for target, attribute, result in (
            ("build_baywatch_runtime.build", "build_runtime", self.runtime),
            ("build_baywatch_places.build", "build_places", self.places),
        ):
            mocked = patch(target, return_value=result)
            setattr(self, attribute, mocked.start())
            self.addCleanup(mocked.stop)

    def test_undeclared_roots_remain_optional(self):
        curator.verify_external()
        self.build_runtime.assert_not_called()
        self.build_places.assert_not_called()

    def test_review_root_alone_verifies_obj_and_rebuilds_runtime_once(self):
        os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(self.review)
        curator.verify_external()
        self.build_runtime.assert_called_once_with(self.review)
        self.build_places.assert_not_called()

    def test_declared_review_root_refuses_missing_or_mutated_obj(self):
        for fault in ("missing-root", "missing-obj", "mutated-obj"):
            with self.subTest(fault=fault):
                os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(
                    self.base / "missing-review" if fault == "missing-root" else self.review
                )
                if fault == "missing-obj":
                    self.obj.unlink()
                elif fault == "mutated-obj":
                    self.obj.write_bytes(b"o Changed\nv 3 2 1\n")
                with self.assertRaisesRegex(ValueError, "OBJ missing or changed"):
                    curator.verify_external()
        self.build_runtime.assert_not_called()
        self.build_places.assert_not_called()

    def test_review_root_refuses_runtime_drift_and_rechecks_each_call(self):
        os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(self.review)
        curator.verify_external()
        self.runtime_path.write_text('{"runtime":{"game":"wrong-game"}}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "runtime evidence differs"):
            curator.verify_external()
        self.assertEqual(2, self.build_runtime.call_count)
        self.build_places.assert_not_called()

    def test_review_root_propagates_missing_and_mutated_raw_evidence(self):
        os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(self.review)
        for failure in (FileNotFoundError("missing raw run"), ValueError("raw manifest changed")):
            with self.subTest(failure=str(failure)):
                self.build_runtime.reset_mock()
                self.build_runtime.side_effect = failure
                with self.assertRaises(type(failure)):
                    curator.verify_external()
                self.build_runtime.assert_called_once_with(self.review)
        self.build_places.assert_not_called()

    def test_both_roots_delegate_each_rebuild_once_without_duplicate_manifest_scan(self):
        os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(self.review)
        os.environ["PINMAME_VPX_SOURCES_ROOT"] = str(self.vpx)
        with patch("build_external_evidence_manifest.check_manifest") as manifest:
            curator.verify_external()
        self.build_runtime.assert_called_once_with(self.review)
        self.build_places.assert_called_once_with(self.vpx, self.obj)
        # The builders own their manifest checks; verify_external must not repeat them.
        manifest.assert_not_called()

    def test_both_roots_refuse_placement_drift(self):
        os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"] = str(self.review)
        os.environ["PINMAME_VPX_SOURCES_ROOT"] = str(self.vpx)
        self.build_places.return_value = {**self.places, "placements": {"fixture": [2, 1]}}
        with self.assertRaisesRegex(ValueError, "placements differ"):
            curator.verify_external()
        self.build_runtime.assert_called_once_with(self.review)
        self.build_places.assert_called_once_with(self.vpx, self.obj)

    def test_declared_vpx_root_remains_fail_closed_without_review_root(self):
        os.environ["PINMAME_VPX_SOURCES_ROOT"] = str(self.base / "missing-vpx")
        with self.assertRaises(FileNotFoundError):
            curator.verify_external()
        self.build_runtime.assert_not_called()
        self.build_places.assert_not_called()


class BaywatchRetainedEvidenceTests(unittest.TestCase):
    def root(self, name):
        if not os.environ.get(name):
            self.skipTest(f"{name} is not set")
        return Path(os.environ[name])

    def test_recompute_exact_table_geometry_and_extraction(self):
        from build_baywatch_places import build
        vpx = self.root("PINMAME_VPX_SOURCES_ROOT")
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")
        world = review / KEY / "world-obj/Baywatch (Sega) 1.0.5.obj"
        self.assertEqual(load_json(ROOT / "tools/baywatch_places.json"), build(vpx, world))

    def test_retained_script_bindings_do_not_collapse_the_capture_devices(self):
        script = (self.root("PINMAME_VPX_SOURCES_ROOT") / "sega/baywatch-1995/extracted-vpxtool/script.vbs").read_text(encoding="latin-1")
        callbacks = {int(n): value for n, value in re.findall(r'(?im)^SolCallback\((\d+)\)\s*=\s*"([^"]+)"', script)}
        self.assertEqual({1: "TroughLock", 2: "bsTroughUpSolOut", 3: "AutoBallLaunch",
                          4: "UpBallLaunch", 5: "bsUpVUKSolOut", 6: "bsLowSVukSolOut",
                          7: "bsSSScoopSolOut", 11: "GIRelay", 12: "LockTrap", 13: "AutoFlipper"},
                         {n: callbacks[n] for n in (1, 2, 3, 4, 5, 6, 7, 11, 12, 13)})
        self.assertNotIn(15, callbacks)
        for binding in (".InitSw 0, 14, 13, 12, 11, 10, 0, 0", ".InitSaucer sw44, 44",
                        ".InitSaucer sw46, 46", ".InitSaucer sw56, 56", "SetLamp 200, GIoffon",
                        ".InitSaucer BallRelease, 15", "Controller.Switch(16)", "Plunger1.Fire"):
            self.assertIn(binding.lower(), script.lower())
        upper = re.search(r"(?is)Sub AutoFlipper\(Enabled\)(.*?)End Sub", script)[1]
        self.assertIn("LeftFlipper1", upper)
        self.assertIn("RightFlipper1", upper)

    def test_measured_drawing_source_and_candidate_object_roles(self):
        from PIL import Image
        comparison = load_json(ROOT / "tools/baywatch_lamp_drawing.json")
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT") / KEY
        render = review / comparison["source"]["render"]
        self.assertEqual(comparison["source"]["render_sha256"], digest(render))
        with Image.open(render) as image:
            self.assertEqual(comparison["source"]["render_dimensions_px"], list(image.size))
        extraction = self.root("PINMAME_VPX_SOURCES_ROOT") / "sega/baywatch-1995/extracted-vpxtool"
        script = (extraction / "script.vbs").read_text(encoding="latin-1")
        for n in (12, 33, 34, 35):
            self.assertIn(f"FlashDLm {n}, 1, BulboF{n}", script)
            self.assertIn(f"Flash {n}, f{n}", script)
            self.assertIn("Flasher", load_json(extraction / f"gameitems/Flasher.f{n}.json"))
        for n, xy in ((20, (102, 500.75)), (21, (223, 469.25))):
            for suffix in ("", "g"):
                name = f"GIBulb{n}{suffix}"
                obj = load_json(extraction / f"gameitems/Light.{name}.json")["Light"]
                self.assertEqual(xy, (obj["center"]["x"], obj["center"]["y"]))
                self.assertIn(f"NFadeLm 200, {name}", script)
                self.assertNotRegex(script, rf"(?:FlashDLm|NFadeLm) (?:12|33|34|35),[^\n]*\b{name}\b")

    def test_pinned_driver_and_rom_members_match_the_dmd64_initializer(self):
        from pinmame_game_defs.workspace import resolve_working_root
        working = resolve_working_root(ROOT)
        source = Path(os.environ["PINMAME_SOURCE_ROOT"]) if os.environ.get("PINMAME_SOURCE_ROOT") else working / "source-checkouts/pinmame" if working else None
        if source is None or not (source / "src/wpc/degames.c").is_file():
            self.skipTest("pinned PinMAME source is unavailable")
        text = (source / "src/wpc/degames.c").read_text(encoding="utf-8")
        self.assertIn("INITGAMES11(baywatch,GEN_DEDMD64, de_192x64DMD, FLIP6364, SNDBRD_DE2S, SNDBRD_DEDMD64, S11_PRINTERLINE)", text)
        block = text[text.index("INITGAMES11(baywatch,"):text.index("#define init_bay_401")]
        for member in load_json(ROOT / "tools/baywatch_runtime_readings.json")["rom_members"]:
            self.assertIn(member["name"], block)
            self.assertIn(member["sha1"], block)
        for clone in ("bay_401", "bay_402", "bay_d300", "bay_d400", "bay_e400", "bay_f201", "bay_g300"):
            self.assertIn(f"#define init_{clone} init_baywatch", text)

    def test_manual_and_extraction_pins_fail_when_declared_root_is_wrong(self):
        curator.verify_external()
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": directory}):
                with self.assertRaisesRegex(ValueError, "manual missing or changed"):
                    curator.verify_external()

    def test_selected_physical_photographs_match_their_acquisition_receipts(self):
        from PIL import Image
        photos = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT") / KEY / "photos"
        text = (curator.EXCERPTS / "photo-receipts.md").read_text(encoding="utf-8")
        receipts = json.loads(text.split("```json\n", 1)[1].split("```", 1)[0])
        for receipt in receipts["ipdb"] + receipts["pinside"]:
            path = photos / receipt["path"]
            self.assertEqual(receipt["sha256"], digest(path))
            self.assertEqual(receipt["size"], path.stat().st_size)
            if "dimensions" in receipt:
                self.assertEqual(receipt["dimensions"], list(Image.open(path).size))

    def test_raw_runtime_manifest_frame_readings_and_causal_checkpoints_recompute(self):
        from build_baywatch_runtime import build
        self.assertEqual(load_json(RUNTIME), build(self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")))

    def test_runtime_builder_refuses_changed_run_and_scenario_identity(self):
        import build_baywatch_runtime as builder
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT")
        original = builder.digest
        for filename in ("coil-cycle.json", "probe_harness.py"):
            with self.subTest(filename=filename):
                with patch.object(builder, "digest", side_effect=lambda p: "0" * 64 if p.name == filename else original(p)):
                    with self.assertRaises(ValueError):
                        builder.build(review)
        read_text = Path.read_text
        scenario = ROOT / "tools/harness-scenarios/data-east/baywatch-cycling-coils.json"

        def changed_scenario(path, *args, **kwargs):
            text = read_text(path, *args, **kwargs)
            return text.replace('"game": "baywatch"', '"game": "wrong-game"', 1) if path == scenario else text

        with patch.object(Path, "read_text", changed_scenario):
            with self.assertRaisesRegex(ValueError, "scenario changed"):
                builder.build(review)

    def test_bounded_dmd_adapter_and_rejection_of_unknown_screens(self):
        from PIL import Image
        from baywatch_harness import MASKS, TEMPLATES, check_targets, match_titles
        review = self.root("PINMAME_REVIEW_ARTIFACTS_ROOT") / KEY / "harness"
        frames = {p.name: p for p in review.glob("*-dmd/*.pgm")}
        for name, template in TEMPLATES.items():
            frame = Image.open(frames[template["source_frame"]])
            self.assertEqual(template["sha256"], digest(frames[template["source_frame"]]))
            self.assertIn(name, match_titles(frame.tobytes(), 192, 64))
        self.assertEqual([], match_titles(bytes(192 * 64), 192, 64))
        self.assertEqual([], match_titles(bytes(128 * 32), 128, 32))
        with self.assertRaises(ValueError):
            check_targets({"actions": [{"type": "pulse_until_display", "texts": ["UNKNOWN"]}]})
        self.assertGreater(len(MASKS), 1)


if __name__ == "__main__":
    unittest.main()
