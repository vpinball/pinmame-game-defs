"""Medusa regressions at the source-authority boundaries that guesses miss."""
from __future__ import annotations

import copy
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_medusa as c
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.spatial import extract_spatial_candidates
from pinmame_game_defs.validation import validate_machine
from pinmame_game_defs.schema_validation import validate_against_schema


def by_address(items, group):
    return {x["binding"]["device"]: x for x in items if x["binding"]["group"] == group}


class MedusaDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = c.build_definition()
        cls.switches = by_address(cls.definition["inputs"], "pinmame.input.switch")
        cls.solenoids = by_address(cls.definition["outputs"], "pinmame.output.solenoid")
        cls.lamps = by_address(cls.definition["outputs"], "pinmame.output.lamp")

    def test_identity_and_complete_public_clone_tree(self):
        d = self.definition
        self.assertEqual({x["id"] for x in d["drivers"]}, {"medusa", "medusaa"})
        self.assertTrue(all(x["physical_compatibility"] == "identical" for x in d["drivers"]))
        self.assertEqual(d["machine"]["year"], 1981)
        self.assertEqual((d["machine"]["model_number"], d["machine"]["ipdb_id"]), ("1245", 1565))
        self.assertEqual(int(d["controller"]["hardware_generation"], 16), 0x400000)
        catalog = load_json(ROOT / "catalog/pinmame.json")
        self.assertEqual({x["id"] for x in catalog["drivers"] if x["machine_id"] == c.MACHINE_ID}, {"medusa", "medusaa"})
        claimants = [p for p in (ROOT / "machines").rglob("*.json") if any(x["id"] in {"medusa", "medusaa"} for x in load_json(p).get("drivers", []))]
        self.assertEqual(claimants, [c.DEFINITION_PATH])

    def test_full_address_dispositions_and_no_local_callback_bank(self):
        self.assertEqual(set(self.switches), {-7, -6, -5} | set(range(1, 49)) | set(range(81, 89)))
        self.assertEqual(set(by_address(self.definition["inputs"], "pinmame.input.dip")), set(range(1, 33)))
        self.assertEqual(set(self.solenoids), set(range(1, 16)) | {17, 18, 19, 20, 45, 46, 47, 48})
        self.assertEqual(set(self.lamps), {x for x in range(1, 129) if x % 16})
        self.assertEqual({n for n in range(1, 49) if self.switches[n]["availability"] == "unused"}, {5, 7})
        self.assertEqual(self.solenoids[17]["availability"], "used")
        self.assertEqual(self.solenoids[17]["kind"], "control_signal")
        self.assertIn("Display Data Strobe", self.solenoids[17]["label"])
        self.assertEqual(self.solenoids[20]["kind"], "control_signal")
        self.assertNotIn(16, self.solenoids)
        self.assertTrue(all(x["availability"] in {"used", "unused", "unknown"} for x in self.definition["outputs"]))

    def test_expander_is_lamp34_and_every_shared_driver_is_explicit(self):
        self.assertEqual(self.lamps[34]["kind"], "relay")
        self.assertEqual(self.lamps[34]["wiring"]["driver_transistor"], "Q38")
        self.assertEqual(self.lamps[34]["wiring"]["control_connection"], "A5J3-25")
        gated = {r["destination"] for r in self.definition["relationships"] if r["source"] == "lamp.main-34"}
        self.assertEqual(gated, {c.SOLENOID_IDS[n] for n in {1, 2, 3, 4, 5, 6, 8}})
        for address in [1, 2, 3, 4, 5, 6, 8]:
            self.assertIn("Lamp34=0", self.solenoids[address]["physical"]["notes"])

    def test_own_board_scr_branches_and_literal_misprints(self):
        self.assertEqual(self.lamps[11]["wiring"]["control_connection"], "A5J2-21")
        self.assertEqual(self.lamps[43]["wiring"]["control_connection"], "A5J3-22")
        self.assertEqual(self.lamps[47]["label"], "Top Middle Back Target")
        self.assertEqual(self.lamps[63]["label"], "Special Medusa")
        self.assertEqual(self.lamps[50]["availability"], "unused")
        self.assertEqual(self.lamps[84]["label"], "Olympus Top Panel #14")
        self.assertEqual(self.lamps[100]["provenance"]["status"], "candidate")
        self.assertEqual(self.lamps[100]["spatial"]["status"], "candidate")
        self.assertNotIn("spatial", self.lamps[47])
        self.assertNotIn("spatial", self.lamps[59])
        self.assertNotIn("quantity", self.lamps[47]["physical"])
        unknown = {65 + 16 * d + s for d in range(4) for s in range(8, 15)}
        self.assertEqual({n for n, v in self.lamps.items() if v["availability"] == "unknown"}, unknown)
        for n in [72, 88, 104, 120]:
            self.assertEqual(self.lamps[n]["availability"], "unused")
            self.assertEqual(self.lamps[n]["kind"], "virtual")

    def test_own_game_bumper_positions_rebut_rotated_table_handlers(self):
        points = {n: self.switches[n]["spatial"]["placements"][0] for n in [37, 38, 39, 40]}
        self.assertGreater(points[37]["x"], points[38]["x"])
        self.assertGreater(points[39]["x"], points[40]["x"])
        self.assertLess(points[37]["y"], points[39]["y"])
        for switch, coil in {37: 12, 38: 11, 39: 10, 40: 9}.items():
            a = self.switches[switch]["spatial"]["placements"][0]
            b = self.solenoids[coil]["spatial"]["placements"][0]
            self.assertEqual((a["x"], a["y"]), (b["x"], b["y"]))
        self.assertIn("table handler is a defect", self.switches[37]["physical"]["notes"])

    def test_polarity_and_synthetic_flipper_states_are_separate(self):
        for n, item in self.switches.items():
            if item["availability"] == "used":
                self.assertIs(item["normally_closed"], False, n)
        for n in [45, 47]:
            self.assertEqual(self.solenoids[n]["kind"], "virtual")
            self.assertEqual(self.solenoids[n]["availability"], "used")
        for n in [46, 48]:
            self.assertEqual(len(self.solenoids[n]["spatial"]["placements"]), 2)
        self.assertIn("does not identify which assembly leaf stack", self.switches[41]["physical"]["notes"])
        self.assertNotIn("initial_active", self.switches[41])

    def test_nine_segment_regions_and_no_physical_dmd(self):
        displays = self.definition["displays"]
        self.assertEqual([x["segment_start"] for x in displays], [1, 9, 17, 25, 35, 38, 42, 44, 46])
        self.assertEqual([x["width"] for x in displays], [7, 7, 7, 7, 2, 2, 2, 2, 2])
        self.assertTrue(all(x["kind"] == "segment" for x in displays))
        for d in displays[6:]:
            self.assertEqual(d["physical_location"], "playfield")
            self.assertIn(c.CORE, d["spatial"]["placements"][0]["provenance"]["source_refs"])
        xs = [d["spatial"]["placements"][0]["x"] for d in displays[6:]]
        self.assertEqual(xs, sorted(xs))

    def test_only_modelled_bulbs_become_lamp_emitters(self):
        seed = load_json(c.BULBS_PATH)
        bulbs = seed["bulbs"]
        objects = {o["name"]: o for o in load_json(c.GEOMETRY_PATH)["objects"]}
        self.assertEqual(len(bulbs), 21)
        self.assertEqual(len({b["primitive"] for b in bulbs}), 21)
        self.assertEqual({n for n, lamp in self.lamps.items() if "placements" in lamp.get("spatial", {})}, {b["address"] for b in bulbs})
        for bulb in bulbs:
            box = bulb["bounds_vpu"]
            self.assertEqual((bulb["x"], bulb["y"]), (round((box[0] + box[3]) / 2 / 952, 6), round((box[1] + box[4]) / 2 / 1974, 6)))
            self.assertLess(abs(objects[bulb["light"]]["x"] - bulb["x"]), .002)
            placement = self.lamps[bulb["address"]]["spatial"]["placements"][0]
            self.assertEqual((placement["x"], placement["y"]), (bulb["x"], bulb["y"]))
        for control in seed["controls"]:
            box = control["bounds_vpu"]
            obj = objects[control["bumper"]]
            self.assertLess(abs((box[0] + box[3]) / 2 - obj["x"] * 952), 1)
            self.assertLess(abs((box[1] + box[4]) / 2 - obj["y"] * 1974), 1)
        self.assertNotIn("spatial", self.switches[8])
        self.assertEqual(len(self.solenoids[8]["spatial"]["placements"]), 1)
        for n in [3, 4, 5, 6]:
            self.assertIn("callback reversal is a table defect", self.solenoids[n]["physical"]["notes"])

    def test_mechanism_inventory_and_driver_ownership(self):
        mechs = {x["id"]: x for x in self.definition["mechanisms"]}
        self.assertEqual(len(mechs["mechanism.memory-targets"]["sensors"]), 7)
        self.assertEqual(len(mechs["mechanism.right-targets"]["sensors"]), 4)
        self.assertEqual(mechs["mechanism.zipper"]["assembly_part_number"], "ASE-2397-4")
        self.assertEqual(mechs["mechanism.shield"]["assembly_part_number"], "ASE-2593-7")
        self.assertEqual(set(mechs["mechanism.expander"]["actuators"]), {"lamp.main-34"} | {c.SOLENOID_IDS[n] for n in c.PAIRED})
        self.assertEqual(mechs["mechanism.gi"]["actuators"], [])
        self.assertIn("29 GI objects", mechs["mechanism.gi"]["behavior"])

    def test_exact_partial_gate_and_failed_promotion(self):
        self.assertEqual(self.definition["coverage"]["missing"], ["output_semantics", "spatial_placement"])
        self.assertEqual(validate_machine(self.definition, ROOT), [])
        promoted = copy.deepcopy(self.definition)
        promoted["coverage"]["status"] = "author_ready"
        promoted["coverage"]["missing"] = []
        self.assertTrue(validate_machine(promoted, ROOT))
        self.assertEqual(c.build_report(self.definition)["format"], "pinmame-spatial-blockers")

    def test_seed_and_all_generated_artifacts_are_identical(self):
        expected = canonical_bytes(self.definition)
        self.assertEqual(c.DEFINITION_PATH.read_bytes(), expected)
        self.assertEqual(c.SEED_PATH.read_bytes(), expected)
        self.assertEqual(c.NOTE_PATH.read_bytes(), c.NOTE_SEED.read_bytes())
        report = c.build_report(self.definition)
        self.assertEqual(c.REPORT_PATH.read_bytes(), canonical_bytes(report))
        self.assertEqual(c.REPORT_MD_PATH.read_text(encoding="utf-8"), c.report_markdown(report))
        self.assertEqual(validate_against_schema(load_json(c.GEOMETRY_PATH), ROOT / "schemas/vpx-spatial-candidates.schema.json", "medusa geometry"), [])

    def test_explicit_bad_evidence_root_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": temp}):
            with self.assertRaisesRegex(ValueError, "Missing or changed"):
                c.verify_retained_evidence()

    def test_missing_excerpt_fails_before_regeneration(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(c, "EXCERPTS", Path(temp)):
            with self.assertRaisesRegex(ValueError, "Missing required Medusa excerpt"):
                c.build_definition()

    def test_preserved_numerical_aliases(self):
        self.assertTrue({"1", "01", "001"} <= {a["value"] for a in self.switches[1]["aliases"]})
        self.assertTrue({"7", "07", "007"} <= {a["value"] for a in self.solenoids[7]["aliases"]})
        self.assertEqual({a["value"] for a in self.solenoids[1]["aliases"] if a["namespace"] == "manual.solenoid-self-test"}, {"01", "16"})
        self.assertEqual({a["value"] for a in self.solenoids[19]["aliases"] if a["namespace"] == "manual.solenoid-self-test"}, {"24"})

    def test_incomplete_electrical_table_fails_before_writing(self):
        with patch.object(c, "MAIN_LAMPS", "\n".join(c.MAIN_LAMPS.splitlines()[1:])):
            with self.assertRaisesRegex(ValueError, "Incomplete or duplicate Medusa address table"):
                c.validate_definition(c.build_definition())

    def test_check_rejects_missing_artifact_without_writing(self):
        missing = ROOT / "machines/partial/bally/medusa-missing-check-artifact.json"
        self.assertFalse(missing.exists())
        output = io.StringIO()
        with patch.object(c, "DEFINITION_PATH", missing), patch.object(sys, "argv", ["curate_medusa.py", "--check"]), redirect_stdout(output):
            self.assertEqual(c.main(), 1)
        self.assertIn("Medusa curator drift", output.getvalue())
        self.assertFalse(missing.exists())

    def test_regeneration_refuses_existing_author_ready_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            promoted = root / "machines/author-ready/bally/medusa-1981.json"
            promoted.parent.mkdir(parents=True)
            promoted.write_bytes(b"preserve promoted contribution")
            output = io.StringIO()
            with patch.object(c, "ROOT", root), patch.object(sys, "argv", ["curate_medusa.py", "--regenerate"]), redirect_stdout(output):
                self.assertEqual(c.main(), 1)
            self.assertIn("existing author-ready", output.getvalue())
            self.assertEqual(promoted.read_bytes(), b"preserve promoted contribution")


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not supplied")
class MedusaRetainedTableTests(unittest.TestCase):
    def test_every_retained_geometry_point_recomputes(self):
        root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally/medusa-1981"
        c.verify_retained_evidence()
        actual = extract_spatial_candidates(root / "extracted-vpxtool", root / "Medusa (Bally 1981).vpx", "git:v0.33.3")
        expected = load_json(c.GEOMETRY_PATH)
        actual_objects = {(o["type"], o["name"]): o for o in actual["objects"]}
        self.assertEqual(expected["bounds"], actual["bounds"])
        self.assertEqual(expected["source"], actual["source"])
        for obj in expected["objects"]:
            self.assertEqual(obj, actual_objects[(obj["type"], obj["name"])])
        script = (root / "extracted-vpxtool/script.vbs").read_text(encoding="utf-8")
        self.assertIn('Const cGameName = "medusa"', script)
        self.assertRegex(script, r"(?i)If Controller\.Lamp\(34\)Then")
        self.assertRegex(script, r"(?i)Sub Bumper1_Hit:vpmTimer.PulseSw 37")
        for name, expected_hash in [("Bally.vbs", "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c"), ("core.vbs", "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69")]:
            self.assertEqual(c.digest(root / name), expected_hash)


@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manuals root not supplied")
class MedusaRetainedManualTests(unittest.TestCase):
    def test_render_and_original_hashes(self):
        c.verify_retained_evidence()
        root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine/bally.medusa.1981"
        seed = load_json(c.MANUAL_GEOMETRY_PATH)
        self.assertEqual(c.digest(root / seed["render"]), seed["render_sha256"])
        from PIL import Image
        with Image.open(root / seed["render"]) as im:
            self.assertEqual(list(im.size), seed["pixel_size"])


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained trace root not supplied")
class MedusaRetainedRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "bally.medusa.1981/harness"

    def test_self_test_numbers_are_decoded_with_gate_at_each_pulse(self):
        d = load_json(self.root / "explore-solenoid-run.json")
        self.assertIsNone(d["failure"])
        glyph = {v: n for n, v in enumerate([0x3f, 6, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 7, 0x7f, 0x6f])}
        observed = set()
        for event in d["events"]:
            if event["event"] != "solenoid" or not event["state"] or event["number"] > 15 or event["time_s"] < 28:
                continue
            gate, segments = None, None
            for e in d["events"]:
                if e["time_s"] > event["time_s"] + .3:
                    break
                if e["event"] == "lamp" and e["number"] == 34 and e["time_s"] <= event["time_s"]:
                    gate = e["state"]
                if e["event"] == "display" and e["index"] == 0 and "segments" in e:
                    segments = e["segments"]
            if segments and all((s & 0x7f) in glyph for s in segments[-2:]):
                number = glyph[segments[-2] & 0x7f] * 10 + glyph[segments[-1] & 0x7f]
                observed.add((number, event["number"], gate))
        expected = {(n, n, 0) for n in range(1, 16)} | {(n, public, 1) for n, public in zip(range(16, 23), [1, 2, 3, 4, 5, 6, 8])}
        self.assertTrue(expected <= observed, expected - observed)

    def test_isolated_reflex_responses_and_no_host_readback_claims(self):
        d = load_json(self.root / "explore-gameplay-run.json")
        self.assertIsNone(d["failure"])
        steps = {s["label"]: s for s in d["steps"]}
        for switch, coil in {37: 12, 38: 11, 39: 10, 40: 9, 34: 15, 35: 14, 36: 13, 17: 7}.items():
            transitions = steps[f"isolated-{switch}"]["transitions"]["solenoids"]
            self.assertEqual([x["number"] for x in transitions if 1 in x["states"]], [coil])
        self.assertIn({"number": 19, "states": [0]}, steps["tilt-control"]["transitions"]["solenoids"])

    def test_synthetic_pairs_in_the_same_enabled_run(self):
        d = load_json(self.root / "explore-flippers-run.json")
        self.assertEqual(c.digest(self.root / "explore-flippers-run.json"), "c512588616944d75fb3a74e21a985ec7f78429181666903d9435c6683f3cec17")
        for n in range(81, 89):
            held = next(x for x in d["snapshots"] if x["label"] == f"flipper-column-{n} (held)")
            self.assertIn(19, held["active_solenoids"])
            pair = {x for x in held["active_solenoids"] if x in {45, 46, 47, 48}}
            self.assertEqual(pair, {45, 46} if n == 82 else {47, 48} if n == 84 else set())

    def test_pinned_checkout_reuse_is_verified_independently(self):
        source = self.root.parents[2] / "source-checkouts/pinmame-46e1a01a"
        self.assertEqual(subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip(), c.REVISION)
        self.assertEqual(subprocess.check_output(["git", "-C", str(source), "status", "--porcelain"], text=True), "")
        origin = subprocess.check_output(["git", "-C", str(source), "remote", "get-url", "origin"], text=True).strip()
        self.assertIn(origin, {"https://github.com/vpinball/pinmame.git", "git@github.com:vpinball/pinmame.git"})
        self.assertEqual(c.digest(source / "src/wpc/by35games.c"), "1c00fca170c7549a399a89fb0f76d4318fce08a6620becd4558fe8cb803bf00d")

    def test_exact_world_mesh_bounds_and_photo_manifest(self):
        c.verify_retained_evidence()
        seed = load_json(c.BULBS_PATH)
        path = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / seed["relative_path"]
        self.assertEqual(path.stat().st_size, seed["source_size"])
        objects, name = {}, None
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                if line.startswith("o "):
                    name = line[2:].strip()
                    objects[name] = []
                elif line.startswith("v ") and name:
                    objects[name].append([float(v) for v in line.split()[1:4]])
        for row in seed["bulbs"] + seed["controls"]:
            vertices = objects[row["primitive"]]
            actual = [min(v[i] for v in vertices) for i in range(3)] + [max(v[i] for v in vertices) for i in range(3)]
            self.assertEqual(actual, row["bounds_vpu"])
            if row in seed["bulbs"]:
                self.assertEqual(len(vertices), 67)


if __name__ == "__main__":
    unittest.main()
