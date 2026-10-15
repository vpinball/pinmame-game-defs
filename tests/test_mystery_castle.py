from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_mystery_castle as curator
import drawing_callouts
from build_external_evidence_manifest import build_manifest, canonical_bytes, check_manifest
from pinmame_game_defs.spatial import extract_spatial_candidates
from pinmame_game_defs.validation import validate_machine

DEFINITION = ROOT / "machines/partial/alvin-g/mystery-castle-1993.json"
SEED = ROOT / "tools/seeds/alvin-g/mystery-castle-1993.json"
FACTS = ROOT / "tools/seeds/alvin-g/mystery-castle-1993-facts.json"
MANIFEST = ROOT / "tools/seeds/alvin-g/mystery-castle-1993-extraction-manifest.json"
RUNTIME = ROOT / "evidence/excerpts/alvin-g.mystery-castle.1993/coil-service-summary.md"


def load(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        text = text.split("```json\n", 1)[1].split("\n```", 1)[0]
    return json.loads(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MysteryCastleDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load(DEFINITION)
        cls.facts = load(FACTS)
        cls.switches = {v["binding"]["device"]: v for v in cls.d["inputs"]}
        cls.lamps = {v["binding"]["device"]: v for v in cls.d["outputs"] if v["binding"]["group"] == "pinmame.output.lamp"}
        cls.coils = {v["binding"]["device"]: v for v in cls.d["outputs"] if v["binding"]["group"] == "pinmame.output.solenoid"}

    def test_identity_generation_and_exact_driver_family(self):
        self.assertEqual(("alvin-g.mystery-castle.1993", 1647, "G5vZZ-MQNNo", "AG08"), tuple(self.d["machine"][k] for k in ("id", "ipdb_id", "opdb_id", "model_number")))
        self.assertEqual({"mystcast", "mystcasa"}, {v["id"] for v in self.d["drivers"]})
        drivers = {v["id"]: v for v in self.d["drivers"]}
        self.assertNotIn("clone_of", drivers["mystcast"])
        self.assertEqual("mystcast", drivers["mystcasa"]["clone_of"])
        self.assertEqual("199?", drivers["mystcasa"]["year"])
        self.assertTrue(all(v["physical_compatibility"] == "identical" for v in drivers.values()))
        self.assertEqual({"platform": "pinmame.alvin-g", "hardware_generation": "0x400000000000", "inversion_applied_by_emulator": True}, self.d["controller"])

    def test_complete_public_namespaces_and_non_fitment(self):
        self.assertEqual(set(range(1, 97)) | {-7, -6, -5} | set(range(113, 121)), set(self.switches))
        self.assertEqual(set(range(1, 97)), set(self.lamps))
        self.assertEqual(set(range(1, 51)), set(self.coils))
        expected = set(range(1, 56)) - {6, 11, 12, 13, 19, 20, 22, 40}
        self.assertEqual(expected, {n for n, v in self.switches.items() if n > 0 and n < 100 and v["availability"] == "used"})
        self.assertEqual(set(range(1, 62)), {n for n, v in self.lamps.items() if v["availability"] == "used"})
        self.assertEqual(set(range(1, 33)) - {7, 8, 25, 28}, {n for n, v in self.coils.items() if n <= 32 and v["availability"] == "used"})
        for n in {7, 8, 25, 28}:
            self.assertEqual("unused", self.coils[n]["availability"])
            self.assertIn("No fitted load", self.coils[n]["physical"]["notes"])

    def test_physical_polarity_is_not_an_emulator_inversion(self):
        for n, row in self.switches.items():
            if row["kind"] == "switch" and row["availability"] == "used":
                self.assertIs(False, row["normally_closed"], n)
        self.assertIn("not a fitted ticket switch", (ROOT / "knowledge/alvin-g/mystery-castle-1993.md").read_text(encoding="utf-8"))
        self.assertEqual(("virtual", "optional"), (self.switches[-5]["kind"], self.switches[-5]["availability"]))
        self.assertEqual("Enter / Begin Test", self.switches[-7]["label"])
        self.assertEqual("Exit / Service Credits", self.switches[-6]["label"])

    def test_flipper_drive_addresses_and_grouped_assembly_signals(self):
        self.assertIn("114", self.switches[8]["physical"]["notes"])
        self.assertIn("116", self.switches[7]["physical"]["notes"])
        self.assertEqual({114, 116}, {n for n in range(113, 121) if self.switches[n]["availability"] == "used"})
        for n in (45, 47):
            self.assertEqual(("virtual", "used", "virtual"), (self.coils[n]["kind"], self.coils[n]["availability"], self.coils[n]["spatial"]["reason"]))
        self.assertEqual(1, self.coils[46]["physical"]["quantity"])
        self.assertEqual(2, self.coils[48]["physical"]["quantity"])
        self.assertIn("CLL-003", self.coils[48]["physical"]["notes"])
        mech = next(v for v in self.d["mechanisms"] if v["id"] == "mech.left-flippers")
        self.assertIn("normally-open Upper Flipper Activator", mech["behavior"])
        self.assertIn("separate coil branches", mech["behavior"])
        self.assertIn("normally-closed EOS", mech["behavior"])
        self.assertEqual([], mech["sensors"])

    def test_mechanism_topology_and_no_coil_to_ball_sensor_shortcut(self):
        mech = {v["id"]: v for v in self.d["mechanisms"]}
        self.assertEqual(14, len(mech))
        self.assertEqual(["solenoid.13", "solenoid.30"], mech["mech.trough"]["actuators"])
        self.assertEqual(["switch.17", "switch.18", "switch.21"], mech["mech.trough"]["sensors"])
        self.assertIn("Two balls", mech["mech.trough"]["behavior"])
        self.assertEqual(["switch.23", "switch.24"], mech["mech.megamode"]["sensors"])
        self.assertEqual(["solenoid.11"], mech["mech.castle-c-a-s"]["actuators"])
        self.assertEqual(["solenoid.12"], mech["mech.castle-t-l-e"]["actuators"])
        for relationship in self.d["relationships"]:
            self.assertFalse(relationship["source"].startswith("solenoid.") and relationship["destination"].startswith("switch."))

    def test_gi_region_conflict_preserves_all_readings_without_promotion(self):
        for n in (16, 26):
            row = self.coils[n]
            self.assertEqual(f"GI Relay {n} (Region Unresolved)", row["label"])
            self.assertEqual("used", row["availability"])
            self.assertEqual("conflicted", row["provenance"]["status"])
            self.assertEqual("playfield region unresolved", row["physical"]["location"])
            self.assertNotIn("quantity", row["physical"])
            self.assertIn("13 clear plus 13 red", row["physical"]["notes"])
            self.assertIn("12 bottom-playfield bulbs", row["physical"]["notes"])
            self.assertIn("2-4 coin-door bulbs", row["physical"]["notes"])
            self.assertIn("unswitched supply context", row["physical"]["notes"])
        self.assertEqual(24, self.coils[29]["physical"]["quantity"])
        self.assertNotIn("quantity", self.coils[31]["physical"])
        self.assertEqual("candidate", self.coils[31]["provenance"]["status"])
        self.assertIn("separate parallel branch", self.coils[31]["physical"]["notes"])
        self.assertIn("[4/6] BULBS", self.coils[31]["physical"]["notes"])
        self.assertIn("voltage digit is also uncertain between 5 and 6", self.coils[31]["physical"]["notes"])
        for n in (29, 31):
            self.assertEqual("backbox", self.coils[n]["physical"]["location"])
            self.assertEqual("cabinet_or_service", self.coils[n]["spatial"]["reason"])
        self.assertNotIn("spatial", self.coils[16])
        self.assertNotIn("spatial", self.coils[26])
        conflict, = self.d["conflicts"]
        self.assertEqual("gi-region-16-26", conflict["id"])
        self.assertEqual("unresolved", conflict["status"])
        self.assertIn("Resolution path:", conflict["description"])
        self.assertIn("physical-machine service video", conflict["description"])
        self.assertIn("public trace confirms addresses and labels, not the physical region", conflict["description"])

    def test_flasher_quantities_and_socket_helpers_fail_closed(self):
        self.assertEqual([2, 2, 2, 1, 1, 2, 1, 4], [self.coils[n]["physical"]["quantity"] for n in range(17, 25)])
        for n in (17, 18, 19, 22):
            self.assertEqual(1, len(self.coils[n]["spatial"]["placements"]))
            self.assertEqual("observed", self.coils[n]["spatial"]["status"])
        self.assertNotIn("spatial", self.coils[23])
        self.assertEqual("cabinet_or_service", self.coils[24]["spatial"]["reason"])
        destinations = {v["destination"] for v in self.d["relationships"] if v["source"] == "solenoid.15"}
        self.assertEqual({f"solenoid.{n}" for n in range(17, 25)}, destinations)

    def test_cabinet_buttons_and_playfield_billboards_are_distinct(self):
        for n in (47, 48):
            self.assertEqual("cabinet_or_service", self.lamps[n]["spatial"]["reason"])
        for n in set(range(1, 62)) - {47, 48}:
            self.assertEqual("candidate" if n in {39, 40, 59, 60} else "validated", self.lamps[n]["spatial"]["status"])
        for n in range(57, 62):
            self.assertEqual("playfield", self.lamps[n]["physical"]["location"])
            self.assertIn("Billboard", self.lamps[n]["label"])
        self.assertEqual("? Bottom", self.lamps[21]["label"])
        self.assertEqual("? Tunnel", self.lamps[38]["label"])

    def test_factory_callout_fit_is_independent_and_reproducible(self):
        seed = load(ROOT / curator.CALLOUTS)
        decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.d))
        self.assertEqual(57, len(decisions["placements"]))
        self.assertEqual({"lamp.59.p1", "lamp.60.p1"}, {pid for pid, row in decisions["placements"].items() if not row["agrees"]})
        self.assertEqual({"39", "40"}, set(seed["excluded_checks"]))
        self.assertNotIn("lamp.39.p1", seed["checks"])
        self.assertNotIn("lamp.40.p1", seed["checks"])
        self.assertEqual(4, decisions["pages"]["3-5"]["controls"])
        self.assertLess(decisions["pages"]["3-5"]["control_loo_max"], .07)
        self.assertEqual(self.facts["evidence"]["drawing_callouts_seed_sha256"], sha(ROOT / curator.CALLOUTS))
        bad = copy.deepcopy(seed)
        next(row for row in bad["pages"]["3-5"]["reads"] if row["label"] == "2")["pixel"] = [10, 10]
        wrong = drawing_callouts.evaluate(bad, drawing_callouts.placements_of(self.d))
        self.assertFalse(wrong["placements"]["lamp.02.p1"]["agrees"])
        for n in set(range(1, 62)) - {39, 40, 47, 48, 59, 60}:
            self.assertIn(curator.DRAWING, self.lamps[n]["spatial"]["placements"][0]["provenance"]["source_refs"])

    def test_display_and_precise_partial_gate(self):
        self.assertEqual(["output_semantics", "spatial_placement", "unresolved_conflicts"], self.d["coverage"]["missing"])
        self.assertEqual("partial", self.d["coverage"]["status"])
        self.assertEqual("conflicted", self.d["coverage"]["dimensions"]["output_semantics"])
        self.assertEqual("conflicted", self.d["coverage"]["dimensions"]["physical_wiring"])
        self.assertEqual((128, 32, 0, "cabinet_or_service"), tuple(self.d["displays"][0][k] for k in ("width", "height", "controller_index", "physical_location")))
        self.assertEqual([], validate_machine(self.d, ROOT))
        wrong = copy.deepcopy(self.d)
        wrong["coverage"]["status"] = "author_ready"
        wrong["coverage"]["missing"] = []
        self.assertTrue(validate_machine(wrong, ROOT), "author-ready mutation must fail on unresolved spatial evidence")

    def test_portable_excerpts_preserve_whole_tables_and_literal_errors(self):
        base = ROOT / curator.EXCERPTS
        for name in ("switches.md", "lamps.md"):
            text = (base / name).read_text(encoding="utf-8")
            for n in range(1, 97):
                self.assertIn(f"| {n:02} |", text)
        text = (base / "switches.md").read_text(encoding="utf-8")
        self.assertIn("| 15 | TEST PLUS | TEST MINUS |", text)
        self.assertIn("row 36 is damaged", text)
        self.assertIn("HP4-13/-14", text)
        self.assertEqual("GRN-BLK", self.switches[5]["wiring"]["return_wire"])
        self.assertEqual("HP4-11", self.switches[81]["wiring"]["drive_connection"])
        for source in self.d["sources"]:
            for excerpt in source.get("excerpts", []):
                self.assertEqual(excerpt["sha256"], sha(ROOT / excerpt["path"]))
                if "image" in excerpt:
                    self.assertEqual(excerpt["image_sha256"], sha(ROOT / excerpt["image"]))
        wiring = (base / "wiring.md").read_text(encoding="utf-8")
        for n in (16, 26, 29, 31):
            self.assertIn(f"(SEE COIL #{n})", wiring)
        self.assertIn("PP1-16, WHT/GRY", wiring)
        self.assertIn("controlled coil BLU/BRN A1HP7-12", wiring)
        self.assertIn("BACKBOX GI RELAY #1", wiring)
        for pin in ("PP1-10", "PP1-09", "PP1-15", "PP1-16", "PP2-10", "PP1-11", "PP1-12", "PP1-13"):
            self.assertIn(pin, wiring)
        self.assertEqual(4, wiring.count("| +[5 or 6]VAC RETURN (digit uncertain) |"))
        self.assertIn("[4/6] BULBS (count digit uncertain)", wiring)
        self.assertIn("WHT/RED", wiring)
        self.assertIn("2-4 BULBS", wiring)
        self.assertIn("before the relay contact", wiring)
        self.assertNotIn("3-4 BULBS", wiring)

    def test_core_license_scope_is_pinned_and_not_bsd(self):
        source = next(v for v in self.d["sources"] if v["id"] == curator.CORE)
        self.assertEqual("LicenseRef-PinMAME-legacy", source["license"])
        self.assertIn("Steve Ellenoff and Gerrit", source["attribution"])
        self.assertEqual("21cde7ac6cffe0fa9e3a66beb89e0db1b78caa7bb8b8041d1b483f36460e026e", self.facts["evidence"]["pinmame_license_sha256"])
        excerpt = next(v for v in source["excerpts"] if v["id"] == "pinmame-license-scope")
        self.assertEqual(self.facts["evidence"]["pinmame_license_excerpt_sha256"], sha(ROOT / excerpt["path"]))
        text = (ROOT / excerpt["path"]).read_text(encoding="utf-8")
        self.assertIn("None has the required first-line BSD marker", text)
        self.assertIn("source-code reuse", text)
        bad = copy.deepcopy(self.facts)
        bad["evidence"]["pinmame_license_excerpt_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "license scope excerpt"):
            curator.verify_inputs(ROOT, bad)

    def test_promotion_prose_tracks_computed_drawing_summary(self):
        text = curator.promotion_decision({"validated": 7, "checked": 9, "not_validated": {"lamp.12.p1": {}}}, {"excluded_checks": {"40": "control"}})
        self.assertIn("7 of 9", text)
        self.assertIn("lamp.12.p1", text)
        self.assertIn("excluded lamp controls: lamp.40", text)
        self.assertNotIn("55 of 57", text)
        self.assertNotIn("lamp.59.p1", text)

    def test_runtime_service_summary_contains_every_fitted_selector(self):
        summary = load(RUNTIME)
        entries = summary["entries"]
        self.assertEqual(set(range(1, 33)) - {7, 8, 25, 28}, {v["displayed_number"] for v in entries})
        self.assertTrue(all(v["displayed_number"] == v["public_solenoid"] for v in entries))
        for entry in entries:
            self.assertIn(entry["public_solenoid"], {v["number"] for v in entry["observed_transitions"]})
        self.assertEqual("ee137a0ba7dcbd7da9699d7e3c6860f76f7463d9726ac75788527d44507590c2", summary["source_run_sha256"])
        self.assertFalse(summary["keyboard_handling"])
        self.assertTrue(summary["clean_state"])

    def test_curator_is_byte_identical_and_inputs_fail_closed(self):
        self.assertEqual(DEFINITION.read_bytes(), SEED.read_bytes())
        curator.run(ROOT, True)
        curator.run(ROOT, True)
        bad = copy.deepcopy(self.facts)
        bad["switches"]["25"][0]["x"] += 0.000001
        with self.assertRaisesRegex(ValueError, "coordinate"):
            curator.verify_inputs(ROOT, bad)
        bad = copy.deepcopy(self.facts)
        bad["sources"][1]["excerpts"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "excerpt"):
            curator.verify_inputs(ROOT, bad)
        working = ROOT.parent.parent if ROOT.parent.name == "worktrees" else ROOT.parent / "pinmame-game-defs-working-dir"
        scratch = working / "review-artifacts" / curator.MACHINE_ID
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="curator-guard-", dir=scratch) as temporary:
            root = Path(temporary)
            path = root / "machines/author-ready/alvin-g/mystery-castle-1993.json"
            path.parent.mkdir(parents=True)
            path.write_text("{}", encoding="utf-8")
            for check in (False, True):
                with self.assertRaisesRegex(ValueError, "author-ready"):
                    curator.run(root, check)

    def test_manifest_and_catalog_reconciliation(self):
        manifest = load(MANIFEST)
        self.assertEqual("mystcast", manifest["game"])
        self.assertEqual(800, len(manifest["files"]))
        self.assertEqual(94_419_481, sum(v["size"] for v in manifest["files"]))
        self.assertEqual("164159268a87a15862a5f6c42d94dd1ce00d754e754934e0eb69370a6a8a01e5", hashlib.sha256(canonical_bytes(manifest) + b"\n").hexdigest())
        catalog = load(ROOT / "catalog/pinmame.json")
        rows = [v for v in catalog["drivers"] if v["id"] in {"mystcast", "mystcasa"}]
        self.assertEqual({"mystcast", "mystcasa"}, {v["id"] for v in rows})
        self.assertEqual(2, len(rows))
        for row in rows:
            self.assertEqual(curator.MACHINE_ID, row["machine_id"])
            self.assertEqual(DEFINITION.relative_to(ROOT).as_posix(), row["definition"])
            self.assertEqual(sha(DEFINITION), row["definition_sha256"])
        machine = next(v for v in catalog["machines"] if v["id"] == curator.MACHINE_ID)
        self.assertEqual((81, "partial", ["output_semantics", "spatial_placement", "unresolved_conflicts"]), (machine["completion_score"], machine["coverage_status"], machine["missing"]))
        for path in (ROOT / "machines/stubs").rglob("*.json"):
            self.assertTrue({"mystcast", "mystcasa"}.isdisjoint({v["id"] for v in load(path).get("drivers", [])}), path)


class MysteryCastleExternalEvidenceTests(unittest.TestCase):
    def vpx_base(self):
        root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        if not root:
            self.skipTest("retained VPX sources unavailable")
        return Path(root) / "alvin-g/mystery-castle-1993"

    def test_retained_vpx_every_extraction_file_and_every_coordinate(self):
        base = self.vpx_base()
        ext = base / "extracted"
        table = base / "Mystery Castle (Alvin G 1993) v2.1.0.vpx"
        self.assertEqual("cf9a40e430a490428ca989a10fac4ac01aeac6cd8783e6da3d6c74f56f32cda5", sha(table))
        self.assertEqual(load(MANIFEST), build_manifest(ext, "mystcast"))
        self.assertEqual(load(FACTS)["evidence"]["extraction_manifest_sha256"], check_manifest(ext, "mystcast"))
        objects = {v["name"].lower(): v for v in extract_spatial_candidates(ext, table, "git:v0.33.3")["objects"]}
        facts = load(FACTS)
        for key in ("switches", "lamps", "solenoids"):
            for records in facts[key].values():
                for record in records:
                    self.assertEqual(record["object_sha256"], sha(ext / record["path"]))
                    actual = objects[record["object"].split(".", 1)[1].lower()]
                    self.assertEqual((record["x"], record["y"]), (actual["x"], actual["y"]))
        groups = load(ext / "collections.json")
        members = next(v["items"] for v in groups if v["name"] == "AllLights")
        mapping = {}
        for name in members:
            light = next(iter(load(ext / "gameitems" / f"Light.{name}.json").values()))
            mapping.setdefault(str(light["timer_interval"]), []).append(name)
        self.assertEqual(facts["all_lights_membership"], mapping)
        for n in range(17, 23):
            light = load(ext / f"gameitems/Light.F{n}b.json")["Light"]
            self.assertTrue(light["show_bulb_mesh"])

    def test_exact_manual(self):
        root = os.environ.get("PINMAME_MANUALS_ROOT")
        if not root:
            self.skipTest("retained manuals unavailable")
        p = Path(root) / "by-machine/alvin-g.mystery-castle.1993/1993_Mystery_Castle_Manual.pdf"
        self.assertEqual(3_717_123, p.stat().st_size)
        self.assertEqual("9fa91108ba60a181218c06420267a2f950109716c665385ac9b62daee329face", sha(p))
        self.assertEqual(1, drawing_callouts.verify_retained(load(ROOT / curator.CALLOUTS), ROOT, Path(root), None))

    def test_exact_runtime_traces_libraries_frames_and_transitions(self):
        root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not root:
            self.skipTest("retained runtime artifacts unavailable")
        root = Path(root)
        base = root / curator.MACHINE_ID
        summary = load(RUNTIME)
        raw = load(base / "harness/coil-service/run.json")
        self.assertIsNone(raw["failure"])
        self.assertEqual(summary["source_run_sha256"], sha(base / "harness/coil-service/run.json"))
        self.assertEqual("b8643ce6bb4b09d8e6b8eddde400836621e9d8219268c596e06b5a77176f126a", check_manifest(base / "harness/coil-service", "mystcasa"))
        steps = {v["label"]: v for v in raw["steps"]}
        frames = {v["label"]: v["displays"][0] for v in raw["snapshots"] if v["displays"]}
        for entry in summary["entries"]:
            self.assertEqual(entry["observed_transitions"], steps[entry["step_label"]]["transitions"]["solenoids"])
            self.assertEqual(entry["pixel_sha256"], frames[entry["step_label"]]["pixel_sha256"])
            self.assertEqual(entry["file_sha256"], sha(base / "harness/coil-service" / entry["snapshot"]))
        self.assertEqual("63a758ecb79e879924831f2140476a31531c5c9f90b116253356b2e856ba143d", sha(root / "vpm-script-libs/alvinG.vbs"))
        self.assertEqual("a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69", sha(root / "vpm-script-libs/core.vbs"))
        for survey in load(FACTS)["evidence"]["photo_surveys"]:
            self.assertEqual(survey["sha256"], sha(root.parent / survey["manifest"]))
        drawing = load(FACTS)["evidence"]["gi_native_drawing"]
        self.assertEqual(drawing["sha256"], sha(root.parent / drawing["render"]))
        self.assertGreater(drawing_callouts.verify_retained(load(ROOT / curator.CALLOUTS), ROOT, None, root), 8)


if __name__ == "__main__":
    unittest.main()
