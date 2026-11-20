"""Mata Hari curation and retained-evidence checks."""

from __future__ import annotations

from hashlib import sha1
import os
from pathlib import Path
import subprocess
import sys
import unittest
import zipfile

from pinmame_game_defs.jsonio import file_sha256, load_json
from pinmame_game_defs.spatial import _item_point, _item_record, extract_spatial_candidates
from pinmame_game_defs.schema_validation import validate_against_schema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_mata_hari as curator
from build_external_evidence_manifest import check_manifest


SERVICE_SEQUENCE = [7, 6, 2, 3, 4, 5, 8, 9, 10, 11, 12, 14, 1, 13, 15, 18, 19]
LAMPS = set(range(1, 64)) - {16, 32, 48}
SCENARIOS = ROOT / "tools/harness-scenarios/by17"
SEGMENTS = {v: str(i) for i, v in enumerate((63, 6, 91, 79, 102, 109, 125, 7, 127, 111))}


def by_group(devices, group):
    return {d["binding"]["device"]: d for d in devices if d["binding"]["group"] == group}


def rising(step, channel):
    return {item["number"] for item in step["transitions"][channel] if 1 in item["states"]}


def window_values(events, start, stop):
    return {
        "".join(SEGMENTS[segment & 0x7f] for segment in event["segments"][-2:])
        for event in events
        if event["event"] == "display" and event["index"] == 0
        and start <= event["time_s"] < stop
        and all((segment & 0x7f) in SEGMENTS for segment in event["segments"][-2:])
    }


class MataHariTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = load_json(curator.DEFINITION)
        cls.report = load_json(curator.REPORT.with_suffix(".json"))
        cls.switches = by_group(cls.record["inputs"], "pinmame.input.switch")
        cls.coils = by_group(cls.record["outputs"], "pinmame.output.solenoid")
        cls.lamps = by_group(cls.record["outputs"], "pinmame.output.lamp")

    def test_identity_display_and_catalog_scope(self):
        self.assertEqual({
            "id": "bally.mata-hari.1977", "name": "Mata Hari", "manufacturer": "Bally",
            "year": 1978, "kind": "physical_pinball", "model_number": "1104-E",
            "ipdb_id": 4501, "opdb_id": "G417e-MDvXz",
        }, self.record["machine"])
        drivers = {d["id"]: d for d in self.record["drivers"]}
        self.assertEqual({"matahari", "mataharb", "mataharc", "matahard", "matahard7", "matatest"}, set(drivers))
        self.assertEqual({"matahari"}, {d["clone_of"] for d in drivers.values() if "clone_of" in d})
        self.assertEqual("identical", drivers["mataharc"]["physical_compatibility"])
        self.assertEqual("compatible", drivers["matahard7"]["physical_compatibility"])
        self.assertEqual(["matahard7"], [d["id"] for d in drivers.values() if "display_overrides" in d])
        self.assertEqual([(i, start, 7) for i, start in enumerate((1, 9, 17, 25))],
                         [(o["controller_index"], o["segment_start"], o["width"])
                          for o in drivers["matahard7"]["display_overrides"]])
        self.assertEqual([(2, 6), (10, 6), (18, 6), (26, 6), (35, 2), (38, 2)],
                         [(d["segment_start"], d["width"]) for d in self.record["displays"]])
        self.assertTrue(all(d["spatial"]["reason"] == "cabinet_or_service" for d in self.record["displays"]))
        catalog = load_json(ROOT / "catalog/pinmame.json")
        linked = [d for d in catalog["drivers"] if d["id"] in drivers]
        self.assertEqual(set(drivers), {d["id"] for d in linked})
        self.assertEqual({curator.ID}, {d["machine_id"] for d in linked})
        self.assertEqual({file_sha256(curator.DEFINITION)}, {d["definition_sha256"] for d in linked})
        self.assertFalse(any(m["id"] == "stub.pinmame.matahari" for m in catalog["machines"]))
        note = curator.KNOWLEDGE.read_text(encoding="utf-8")
        self.assertIn("September 26, 1977", note)
        self.assertIn("April 1978", note)
        self.assertIn("1557", note)

    def test_address_disposition(self):
        self.assertEqual("pinmame.by17", self.record["controller"]["platform"])
        self.assertEqual("0x200000", self.record["controller"]["hardware_generation"])
        profile = load_json(ROOT / "controllers/pinmame/by17.json")
        self.assertEqual("Bally MPU AS-2518-17", profile["hardware_family"])
        self.assertEqual([5, 6, 1, 3], [g["transports"]["controller_plugin"]["group_id"] for g in profile["groups"]])
        for entry in profile["groups"] + profile["sources"]:
            self.assertNotIn("mata hari", (entry.get("notes") or entry["locator"]).casefold())
        self.assertEqual({-7, -6, -5} | set(range(1, 49)) | set(range(81, 89)), set(self.switches))
        self.assertEqual(set(range(1, 33)), set(by_group(self.record["inputs"], "pinmame.input.dip")))
        self.assertEqual("optional", self.switches[11]["availability"])
        self.assertEqual("unused", self.switches[-5]["availability"])
        self.assertEqual(2, self.switches[27]["physical"]["quantity"])
        self.assertEqual({82, 84}, {n for n in range(81, 89) if self.switches[n]["availability"] == "used"})
        self.assertTrue(all(self.switches[n]["availability"] == "unused" for n in range(41, 49)))
        self.assertTrue(all(not self.switches[n]["normally_closed"] for n in (7, 8, 16, 17, 27, 82, 84)))
        self.assertEqual(set(range(1, 16)) | {17, 18, 19, 20, 45, 46, 47, 48}, set(self.coils))
        mapping = {int(alias["value"]): n for n, d in self.coils.items() for alias in d["aliases"]}
        self.assertEqual(dict(enumerate(SERVICE_SEQUENCE, 1)), mapping)
        self.assertEqual({"relay_gated"}, {r["kind"] for r in self.record["relationships"]
                                          if r["source"] == self.coils[19]["id"]})
        self.assertEqual(LAMPS, set(self.lamps))
        self.assertEqual("A5J3-1", self.lamps[49]["wiring"]["drive_connection"])
        self.assertEqual("Q25", self.lamps[24]["wiring"]["driver_transistor"])
        self.assertEqual("Q24", self.lamps[25]["wiring"]["driver_transistor"])
        self.assertEqual("A5J3-21", self.lamps[41]["wiring"]["drive_connection"])
        self.assertEqual("A5J3-10", self.lamps[57]["wiring"]["drive_connection"])
        self.assertTrue(all(d["kind"] not in {"gi", "flasher"} for d in self.record["outputs"]))

    def test_partial_and_deterministic(self):
        self.assertEqual("partial", self.record["coverage"]["status"])
        self.assertEqual({"input_semantics", "output_semantics", "mechanism_behavior", "variant_differences", "spatial_placement"},
                         set(self.record["coverage"]["missing"]))
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])
        for n in (36, 52):
            self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
            self.assertNotIn("spatial", self.lamps[n])
        for n in (13, 15):
            self.assertNotIn("quantity", self.coils[n]["physical"])
            self.assertNotIn("spatial", self.coils[n])
        for n in (41, 57):
            self.assertEqual("observed", self.lamps[n]["spatial"]["status"])
            self.assertEqual(1, len(self.lamps[n]["spatial"]["placements"]))
            self.assertLessEqual({curator.A5, curator.AB_PLAY, curator.CORPUS},
                                 set(self.lamps[n]["provenance"]["source_refs"]))
        self.assertEqual(16, self.report["factory_callouts"]["validated"])
        self.assertEqual([9, 8, 7, 6], [
            int(self.report["placement_objects"][self.switches[n]["id"]][0][-1]) for n in range(17, 21)
        ])
        self.assertTrue(all(self.switches[n]["spatial"]["status"] == "validated" for n in range(17, 21)))
        for source in self.record["sources"]:
            for excerpt in source.get("excerpts", []):
                self.assertEqual(excerpt["sha256"], file_sha256(ROOT / excerpt["path"]))
        for scenario in SCENARIOS.glob("*.json"):
            errors = validate_against_schema(load_json(scenario), ROOT / "schemas/harness-scenario.schema.json", str(scenario))
            self.assertEqual([], errors)
        subprocess.run([sys.executable, "-B", str(ROOT / "tools/curate_mata_hari.py"), "--check"],
                       cwd=ROOT, check=True, capture_output=True)

    @unittest.skipUnless(os.getenv("PINMAME_MANUALS_ROOT"), "retained manuals root unavailable")
    def test_factory_bytes(self):
        directory = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.ID
        for filename, digest, _ in curator.FACTORY_FILES.values():
            self.assertEqual(digest, file_sha256(directory / filename))
        self.assertEqual(curator.BULLETIN_SHA256, file_sha256(directory / curator.BULLETIN_FILE))
        for filename, _, _, digest, _ in curator.PHOTOS.values():
            self.assertEqual(digest, file_sha256(directory / filename))
        details = next(s for s in self.record["sources"] if s["id"] == curator.DETAIL)
        self.assertEqual(details["sha256"], file_sha256(directory / details["original_filename"]))
        page = load_json(curator.CALLOUTS)["pages"]["fo579-18"]["image"]
        render = Path(os.environ["PINMAME_MANUALS_ROOT"]) / page["relative_path"]
        self.assertEqual(page["sha256"], file_sha256(render))

    @unittest.skipUnless(os.getenv("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root unavailable")
    def test_extraction_and_exact_geometry(self):
        directory = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally" / curator.SLUG
        seed = load_json(curator.SEEDS / f"{curator.SLUG}-geometry.json")
        points_primary = {}
        for year, table in curator.TABLES.items():
            with self.subTest(year=year):
                extraction = directory / f"extracted-{year}"
                vpx = directory / f"Mata Hari (Bally {year}).vpx"
                self.assertEqual(table["sha256"], file_sha256(vpx))
                self.assertEqual(table["vpx_size"], vpx.stat().st_size)
                self.assertEqual(table["manifest_sha256"], check_manifest(extraction, "matahari"))
                files = load_json(extraction / "manifest.json")["files"]
                self.assertEqual((table["file_count"], table["file_bytes"]),
                                 (len(files), sum(item["size"] for item in files)))
                self.assertEqual(table["script_sha256"], file_sha256(extraction / "script.vbs"))
                script = (extraction / "script.vbs").read_bytes().decode("latin-1").casefold()
                self.assertIn('const cgamename="matahari"', script)
                self.assertIn("vpmmaplights insertlights", script)
                self.assertIn("const senable=19", script)
                self.assertIn("dtR.initdrop array(target6,target7,target8,target9),array(17,18,19,20)".lower(), script)
                geometry = seed[str(year)]
                collections = {c["name"]: c["items"] for c in load_json(extraction / "collections.json")}
                self.assertEqual(geometry["insert_lights"], collections["InsertLights"])
                self.assertEqual(geometry["gi_lights"], collections["GILights"])
                extracted = extract_spatial_candidates(extraction, vpx, "git:v0.33.3")
                self.assertEqual(geometry["bounds"], extracted["bounds"])
                for name, points in geometry["objects"].items():
                    source_path = extraction / "gameitems" / f"{name}.json"
                    kind, object_name, obj = _item_record(source_path, load_json(source_path))
                    self.assertEqual(name, f"{kind}.{object_name}")
                    self.assertEqual(tuple(points[:2]), _item_point(kind, obj)[:2], name)
                    if kind == "Light":
                        self.assertEqual(points[2:], [obj["timer_interval"], obj["show_bulb_mesh"]], name)
                if year == 1978:
                    points_primary = {f'{i["type"]}.{i["name"]}': (i["x"], i["y"]) for i in extracted["objects"]}
        for d in self.record["inputs"] + self.record["outputs"]:
            if d["id"] not in self.report["placement_objects"]:
                continue
            actual = [(p["x"], p["y"]) for p in d["spatial"]["placements"]]
            self.assertEqual([points_primary[obj] for obj in self.report["placement_objects"][d["id"]]], actual)
        self.assertEqual(41, seed["1978"]["objects"]["Light.BumpLight1"][2])
        self.assertTrue(seed["1977"]["objects"]["Light.BumpLight1"][3])

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained trace root unavailable")
    def test_runtime_observations(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "native-traces"
        self.assertEqual(curator.NATIVE_MANIFEST, check_manifest(root, "matahari"))
        traces = {}
        for key, (name, digest, _, _) in curator.RUNTIME.items():
            path = root / name
            self.assertEqual(digest, file_sha256(path))
            traces[key] = trace = load_json(path)
            self.assertIsNone(trace["failure"])
            self.assertEqual("8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5", trace["library_sha256"])
            self.assertEqual(0, trace["handle_mechanics"])
            if trace["scenario"]:
                suffix = "gameplay" if key == curator.PLAY else "service"
                self.assertEqual(file_sha256(SCENARIOS / f"matahari-{suffix}.json"), trace["scenario"]["sha256"])
        play = {s["label"]: s for s in traces[curator.PLAY]["steps"]}
        for label, expected in {
            "start with ball in outhole": {5, 7, 13, 15, 19},
            "right flipper button": {45, 46}, "left flipper button": {47, 48},
            "bottom left thumper": {3, 8}, "top left thumper": {3, 9},
            "top right thumper": {3, 10}, "bottom right thumper": {3, 11},
            "right slingshot": {2, 14}, "left slingshot": {2, 12},
            "ball held in saucer": {1, 4},
            "left target A completes both banks": {5, 13, 15},
            "right button after tilt": set(),
        }.items():
            self.assertEqual(expected, rising(play[label], "solenoids"), label)
        self.assertEqual([{"number": 19, "states": [0]}], play["cabinet tilt"]["transitions"]["solenoids"])
        self.assertIn(51, rising(play["left target A completes both banks"], "lamps"))
        self.assertFalse({13, 15} & rising(play["right target A completes the bank"], "solenoids"))
        stock = traces[curator.PLAY]
        blink = {
            n: [(e["time_s"], e["state"]) for e in stock["events"] if e["event"] == "lamp" and e["number"] == n]
            for n in (4, 20)
        }
        self.assertEqual(blink[4], blink[20])
        self.assertEqual(((8.110, 1), (27.485, 1)), (blink[4][0], blink[4][-1]))
        self.assertEqual([1, 0] * 9 + [1], [state for _, state in blink[4]])
        for (t0, _), (t1, _) in zip(blink[4][1:], blink[4][2:]):
            self.assertAlmostEqual(t1 - t0, 1, delta=0.05)
        start = next(i for i, s in enumerate(stock["snapshots"]) if s["label"] == "start with ball in outhole")
        self.assertTrue(all({4, 20} <= set(s["active_lamps"]) for s in stock["snapshots"][start:]))
        service = traces[curator.SERVICE]
        self.assertEqual(LAMPS, rising(service["steps"][1], "lamps"))
        snapshots = {s["label"]: s["time_s"] for s in service["snapshots"]}
        start = snapshots["display test"]
        end = snapshots["capture a full solenoid sweep"]
        coil_events = [event for event in service["events"] if event["event"] == "solenoid"
                       and event["state"] == 1 and start <= event["time_s"] < end]
        self.assertEqual(SERVICE_SEQUENCE * 2, [e["number"] for e in coil_events[:34]])
        for i, event in enumerate(coil_events[:34]):
            displayed = window_values(service["events"], event["time_s"] - 0.15, event["time_s"] + 0.50)
            self.assertIn(f"{i % 17 + 1:02d}", displayed, event)
        for event_value, label, prior in (("32", "saucer closed", "switch test"),
                                          ("12", "unfitted matrix position 12 closed", "saucer open")):
            self.assertIn(event_value, window_values(service["events"], snapshots[prior], snapshots[label]))
        for key, width, seg_type in ((curator.SERVICE, 6, 6), (curator.V22, 7, 8)):
            available = [e for e in traces[key]["events"] if e["event"] == "display_available"]
            self.assertEqual([(i, width, seg_type) for i in range(4)] + [(4, 2, 6), (5, 2, 6), (6, 0, 14)],
                             [(e["index"], e["length"], e["type"]) for e in available])

    @unittest.skipUnless(os.getenv("PINMAME_VPX_SCRIPTS_ROOT"), "pinned script checkout unavailable")
    def test_corpus_bumper_binding(self):
        root = Path(os.environ["PINMAME_VPX_SCRIPTS_ROOT"])
        script = root / curator.CORPUS_SCRIPT
        self.assertEqual(curator.CORPUS_SHA256, file_sha256(script))
        lines = script.read_bytes().decode("latin-1").casefold().splitlines()
        self.assertIn("pulsesw 38", lines[1209])
        self.assertIn("pulsesw 37", lines[1210])
        body = "\n".join(lines[3736:3742])
        self.assertIn("flbumpvalue3 = bumperflashlevel * (l41.getinplayintensity / l41.intensity)", body)
        self.assertIn("flbumpvalue4 = bumperflashlevel * (l41.getinplayintensity / l41.intensity)", body)

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained trace root unavailable")
    def test_stock_ab_lamp_trace(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / curator.AB_FOLDER
        path = root / "trace.json"
        self.assertEqual(curator.AB_MANIFEST, check_manifest(root, "matahari"))
        self.assertEqual(curator.AB_SHA256, file_sha256(path))
        trace = load_json(path)
        self.assertIsNone(trace["failure"])
        self.assertEqual("matahari", trace["game"])
        self.assertEqual("8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5", trace["library_sha256"])
        self.assertEqual(0, trace["handle_mechanics"])
        self.assertEqual(file_sha256(SCENARIOS / "matahari-ab-lamps.json"), trace["scenario"]["sha256"])
        steps = {s["label"]: s for s in trace["steps"]}
        snapshots = {s["label"]: s for s in trace["snapshots"]}
        targets = {41, 57}
        self.assertEqual(
            [(41, 38.031, 1), (57, 38.031, 1)],
            [(e["number"], e["time_s"], e["state"]) for e in trace["events"]
             if e["event"] == "lamp" and e["number"] in targets],
        )
        completions = ["first pair B via top", "second pair A via side", "third pair B via top"]
        self.assertEqual(targets, rising(steps[completions[0]], "lamps") & targets)
        for label, award in zip(completions, (22, 38, 54), strict=True):
            self.assertIn(award, rising(steps[label], "lamps"))
        for label, expected in [
            ("first pair A via top", set()),
            *((label, targets) for label in completions),
            ("lower right bumper after third pair", targets),
        ]:
            self.assertEqual(expected, set(snapshots[label]["active_lamps"]) & targets)
        for label, score in {
            "lower left bumper before lanes": 100, "lower right bumper before lanes": 200,
            "first pair B via top": 1700, "lower left bumper after first pair": 2700,
            "lower right bumper after first pair": 3700, "third pair B via top": 9700,
            "lower left bumper after third pair": 10700, "lower right bumper after third pair": 11700,
        }.items():
            segments = snapshots[label]["displays"][0]["segments"]
            self.assertEqual(score, int("".join(SEGMENTS.get(v & 0x7f, " ") for v in segments)), label)

    @unittest.skipUnless(os.getenv("PINMAME_ROM_LIBRARY_ROOT"), "authorized ROM root unavailable")
    def test_archive_member_provenance(self):
        root = Path(os.environ["PINMAME_ROM_LIBRARY_ROOT"])
        expected = {
            "matahari": ("93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d",
                         {"725-21_2.716": "2347342f1281c097ea39c79236d85b00a1dfc7b2",
                          "720-20_6.716": "729e61a29691857112579efcdb96a35e8e5b1279"}, 2048),
            "matahard7": ("94ab62eabd52ba20c17c6c932c509ccdf73da3466c6da95788fd4492bd7703ee",
                          {"mataharif_U2_V22.2732": "1f1b3c3397040618da70c12072daee0ea9ce8dd2",
                           "mataharif_U6_V22.2732": "05b670c1571c2db2a865e1728d405b8f41db66a3"}, 4096),
        }
        for driver, (digest, members, member_size) in expected.items():
            path = root / f"{driver}.zip"
            self.assertEqual(digest, file_sha256(path))
            with zipfile.ZipFile(path) as archive:
                for filename, member_digest in members.items():
                    data = archive.read(filename)
                    self.assertEqual(member_size, len(data))
                    self.assertEqual(member_digest, sha1(data).hexdigest())


if __name__ == "__main__":
    unittest.main()
