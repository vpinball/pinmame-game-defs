"""Mata Hari curation and retained-evidence checks."""

from __future__ import annotations

from collections import Counter
from hashlib import sha1, sha256
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


def output_transitions(trace, channel, number):
    return [(event["time_s"], event["state"]) for event in trace["events"]
            if event["event"] == channel and event["number"] == number]


def segment_text(display):
    return "".join(SEGMENTS.get(value & 0x7f, " " if value == 0 else "?") for value in display["segments"])


def display_text(snapshot, index):
    return next((segment_text(display) for display in snapshot["displays"] if display["index"] == index), "").strip()


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
        self.assertEqual(88, next(m["completion_score"] for m in catalog["machines"] if m["id"] == curator.ID))
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
        dips = by_group(self.record["inputs"], "pinmame.input.dip")
        self.assertEqual(set(range(1, 33)), set(dips))
        self.assertEqual({14, 15, 29}, {n for n, dip in dips.items() if dip["availability"] == "optional"})
        self.assertEqual({22}, {n for n, dip in dips.items() if dip["availability"] == "unknown"})
        self.assertFalse(any(dip["availability"] == "unused" for dip in dips.values()))
        for n in (14, 15, 22, 29):
            self.assertEqual(f"dip.s{n}-unverified-option", dips[n]["id"])
            self.assertEqual("observed" if n == 22 else "validated", dips[n]["provenance"]["status"])
            self.assertLessEqual({curator.STOCK_CODE, curator.DERIVATIVE_DIP_CODE}, set(dips[n]["provenance"]["source_refs"]))
        for n in (14, 15, 22):
            self.assertIn(curator.MATATEST_DIP_STARTUP, dips[n]["provenance"]["source_refs"])
        for n in (14, 15):
            self.assertEqual(f"S{n} Revision 7 attract timer seed (unassigned in factory firmware)", dips[n]["label"])
        self.assertEqual("S29 V22 award table (unassigned in factory firmware)", dips[29]["label"])
        self.assertIn(curator.QUENCH, dips[29]["provenance"]["source_refs"])
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
        for device in (self.coils[17], self.coils[20], self.lamps[4], self.lamps[20]):
            self.assertEqual("unused", device["availability"])
            self.assertIn(curator.STOCK_CODE, device["provenance"]["source_refs"])
            self.assertIn(curator.FOLLOWUP_PLAY, device["provenance"]["source_refs"])
            self.assertEqual("validated", device["provenance"]["status"])
        self.assertTrue(all(d["kind"] not in {"gi", "flasher"} for d in self.record["outputs"]))

    def test_partial_and_deterministic(self):
        self.assertEqual("partial", self.record["coverage"]["status"])
        self.assertEqual(["input_semantics", "spatial_placement"], self.record["coverage"]["missing"])
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])
        for n in (36, 52):
            self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
            self.assertEqual(2, len(self.lamps[n]["spatial"]["placements"]))
        for n, side, point in ((13, "left", (0.14, 0.44)), (15, "right", (0.76, 0.45))):
            self.assertEqual(1, self.coils[n]["physical"]["quantity"])
            self.assertEqual("observed", self.coils[n]["spatial"]["status"])
            placement, = self.coils[n]["spatial"]["placements"]
            self.assertEqual(("effect", *point), (placement["role"], placement["x"], placement["y"]))
            mechanism = next(m for m in self.record["mechanisms"] if m["id"] == f"mech.{side}-four-drop-bank")
            self.assertEqual([self.coils[n]["id"]], mechanism["actuators"])
            self.assertEqual(4, len(mechanism["sensors"]))
            self.assertIn(curator.CHARLTON, mechanism["provenance"]["source_refs"])
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
        self.assertEqual([0.222, 0.578], self.report["photo_registration"]["panel_tilt_xy"])
        self.assertEqual([], self.report["unplaced_switches"])
        self.assertEqual([], self.report["unplaced_solenoid_drives"])
        self.assertEqual([28, 43, 44, 60], self.report["photo_registration"]["arrow_outputs"])
        credit, = self.lamps[59]["spatial"]["placements"]
        self.assertEqual((0.162939, 0.874696), (credit["x"], credit["y"]))
        self.assertIn(curator.GEOMETRY_UNCLE, credit["provenance"]["source_refs"])
        self.assertEqual({"Light.GI_Bulb15", "Light.GI_Bulb24", "Light.GI_Bulb25", "Light.GI_Bulb26"},
                         set(self.report["observed_gi_subset"]))
        for source in self.record["sources"]:
            for excerpt in source.get("excerpts", []):
                self.assertEqual(excerpt["sha256"], file_sha256(ROOT / excerpt["path"]))
        for scenario in SCENARIOS.glob("*.json"):
            errors = validate_against_schema(load_json(scenario), ROOT / "schemas/harness-scenario.schema.json", str(scenario))
            self.assertEqual([], errors)
        subprocess.run([sys.executable, "-B", str(ROOT / "tools/curate_mata_hari.py"), "--check"],
                       cwd=ROOT, check=True, capture_output=True)

    def test_fixture_registration_rejects_unsupported_lamp_anchors(self):
        geometry = load_json(curator.SEEDS / f"{curator.SLUG}-geometry.json")["1978"]
        register = load_json(curator.PHOTO_REGISTER)
        arrow = register["arrow_sockets"]["targets"]["28"]
        arrow["object"], arrow["effect"] = arrow["effect"], arrow["object"]
        with self.assertRaisesRegex(ValueError, "chosen socket anchor for lamp 28"):
            curator.build_lamps(geometry, register)

        register = load_json(curator.PHOTO_REGISTER)
        register["independent_table"]["feature_targets"]["26"][0][0] = "Light.L26b"
        with self.assertRaisesRegex(ValueError, "no longer corroborates Light.L26b"):
            curator.build_lamps(geometry, register)

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
        self.assertEqual(curator.LIT_PLAYFIELD_SHA256, file_sha256(directory / curator.LIT_PLAYFIELD_FILE))
        for filename, digest in curator.CHARLTON_FILES.items():
            self.assertEqual(digest, file_sha256(directory / "charlton-2014" / filename))
        filename, digest = curator.FOLLOWUP_FILES[curator.OLIVER_REV7]
        self.assertEqual(digest, file_sha256(directory / "oliver-rev7" / filename))
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

    @unittest.skipUnless(os.getenv("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root unavailable")
    def test_independent_fixture_sources(self):
        directory = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally" / curator.SLUG
        table = curator.UNCLE_TABLE
        vpx, extraction = directory / table["file"], directory / table["extraction"]
        self.assertEqual(table["sha256"], file_sha256(vpx))
        self.assertEqual(table["vpx_size"], vpx.stat().st_size)
        self.assertEqual(table["manifest_sha256"], check_manifest(extraction, "matahari"))
        listed = load_json(extraction / "manifest.json")["files"]
        self.assertEqual((table["file_count"], table["file_bytes"]), (len(listed), sum(row["size"] for row in listed)))
        self.assertEqual(table["script_sha256"], file_sha256(extraction / "script.vbs"))
        collections = {row["name"]: row["items"] for row in load_json(extraction / "collections.json")}
        independent = load_json(curator.PHOTO_REGISTER)["independent_table"]
        fixtures = [(name, coords) for targets in independent["feature_targets"].values() for _, name, coords in targets]
        fixtures.append((independent["apron_credit"]["emitter"], independent["apron_credit"]["raw_xy"]))
        for name, expected in fixtures:
            path = extraction / "gameitems" / f"Primitive.{name}.json"
            kind, _, obj = _item_record(path, load_json(path))
            self.assertEqual(tuple(expected), _item_point(kind, obj)[:2], name)
        self.assertIn("Bulb_Prim_028", collections["GIBulbPrims"])
        for name in ("l59", "l59a"):
            self.assertIn(name, collections["AllLamps"])
            path = extraction / "gameitems" / f"Light.{name}.json"
            _, _, obj = _item_record(path, load_json(path))
            self.assertEqual(59, obj["timer_interval"])

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

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained follow-up root unavailable")
    def test_followup_artifacts_and_native_observations(self):
        directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "online-followup"
        for path, digest in curator.FOLLOWUP_FILES.values():
            self.assertEqual(digest, file_sha256(directory / path))
        self.assertEqual(curator.STOCK_READER_SHA256, file_sha256(directory / "trace-stock-code.py"))
        self.assertEqual(curator.FREE_PLUS_TEXT, file_sha256(directory / "MataHari_Update.txt"))
        self.assertEqual(curator.UNCLE_TABLE["register_sha256"], file_sha256(directory / "newtable-objects-controls.json"))
        root = directory / "native-followup"
        self.assertEqual(curator.FOLLOWUP_MANIFEST, check_manifest(root, "matahari"))
        traces = {}
        snapshots = {}
        steps = {}
        dip_configuration = {}
        lamp_counts = Counter()
        for name, driver, digest in curator.table_rows("native-followup", "| Native run directory"):
            run = root / name
            self.assertEqual(digest.strip("`"), file_sha256(run / "trace.json"))
            traces[name] = trace = load_json(run / "trace.json")
            self.assertIsNone(trace["failure"], name)
            self.assertEqual(driver, trace["game"])
            self.assertEqual(0, trace["handle_mechanics"])
            self.assertEqual("8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5", trace["library_sha256"])
            self.assertEqual(file_sha256(run / "scenario.json"), trace["scenario"]["sha256"])
            inputs = load_json(run / "inputs.json")
            self.assertEqual(inputs["initial_nvram_sha256"], file_sha256(run / "initial.nv"))
            self.assertEqual(inputs["input_dips"], list((run / "initial.nv").read_bytes()[-6:]))
            self.assertEqual(inputs["input_dips"], list((run / "state" / "nvram" / f"{driver}.nv").read_bytes()[-6:]))
            dip_configuration[name] = inputs["input_dips"][:4]
            snapshots[name] = {snap["label"]: snap for snap in trace["snapshots"]}
            steps[name] = {step["label"]: step for step in trace["steps"]}
            lamp = output_transitions(trace, "lamp", 4)
            self.assertEqual(lamp, output_transitions(trace, "lamp", 20), name)
            spare_times = {time_s for time_s, _ in lamp}
            ab_times = {time_s for n in (36, 52) for time_s, _ in output_transitions(trace, "lamp", n)}
            if driver == "matatest":
                self.assertEqual({42: 12, 51: 15}[len(spare_times)], len(spare_times & ab_times), name)
            else:
                self.assertLessEqual(spare_times, ab_times, name)
            lamp_counts[driver, len(lamp)] += 1
            booted = snapshots[name]["booted"]
            for n in (17, 20):
                transitions = output_transitions(trace, "solenoid", n)
                self.assertEqual([1, 0], [state for _, state in transitions], (name, n))
                self.assertLess(transitions[0][0], transitions[1][0], (name, n))
                self.assertLess(transitions[1][0], booted["time_s"], (name, n))

        manifest_paths = {entry["path"] for entry in load_json(root / "manifest.json")["files"]}
        self.assertEqual({path for path in manifest_paths if path.endswith("/trace.json")},
                         {f"{name}/trace.json" for name in traces})
        self.assertEqual({("matahari", 17): 3, ("mataharb", 18): 2, ("mataharb", 19): 2,
                          ("mataharc", 17): 2, ("mataharc", 22): 1, ("matahard", 17): 3,
                          ("matahard", 18): 1, ("matahard7", 17): 3,
                          ("matatest", 42): 7, ("matatest", 51): 2}, lamp_counts)

        self.assertEqual([0, 0, 0x18, 0], dip_configuration["stock-baseline"])
        self.assertEqual([0, 0x60, 0x38, 0x10], dip_configuration["stock-unassigned"])
        self.assertEqual([0, 0x80, 0x18, 0], dip_configuration["stock-five-ball"])
        baseline = list(snapshots["stock-baseline"].values())[2:]
        alternate = list(snapshots["stock-unassigned"].values())[2:]
        for stock, unused_on in zip(baseline, alternate, strict=True):
            self.assertEqual(stock["label"], unused_on["label"])
            for channel in ("active_lamps", "active_solenoids"):
                self.assertEqual(stock[channel], unused_on[channel], stock["label"])
            self.assertEqual(display_text(stock, 0), display_text(unused_on, 0), stock["label"])
        for step in steps["stock-baseline"]:
            self.assertEqual(rising(steps["stock-baseline"][step], "solenoids"),
                             rising(steps["stock-unassigned"][step], "solenoids"), step)
        for name, first_expected in (("stock-baseline", {41, 57}), ("stock-five-ball", {57})):
            self.assertEqual(first_expected, {41, 57} & set(snapshots[name]["B first pair"]["active_lamps"]))
            self.assertEqual({41, 57}, {41, 57} & set(snapshots[name]["A second pair"]["active_lamps"]))
        for i, multiplier in enumerate((58, 60, 44, 28), 1):
            label = f"saucer visit {i}"
            self.assertIn(1, rising(steps["stock-baseline"][label], "solenoids"))
            self.assertIn(multiplier, snapshots["stock-baseline"][label]["active_lamps"])

        for name, expected, second_player in (("oliver-b-credit-enabled", "01", True),
                                             ("oliver-b-credit-control", "00", False)):
            self.assertEqual(expected, display_text(snapshots[name]["start after coin"], 4))
            self.assertEqual(second_player, 30 in snapshots[name]["add second player"]["active_lamps"])
        self.assertEqual("3000", display_text(snapshots["oliver-test-visible-enabled"]["A first pair"], 0))
        self.assertEqual("01", display_text(snapshots["oliver-test-visible-enabled"]["start after coin"], 4))
        for name, credit, joined in (("user-freeplus-clear", "", ""), ("user-freeplus-preserve", "08", "07")):
            self.assertIn(19, rising(steps[name]["start without coin"], "solenoids"))
            self.assertEqual(credit, display_text(snapshots[name]["start without coin"], 4))
            self.assertEqual(joined, display_text(snapshots[name]["start to add player"], 4))
            self.assertTrue({30, 59} <= set(snapshots[name]["start to add player"]["active_lamps"]))
        for name in ("user-freeplus-control", "quench-control"):
            self.assertNotIn(19, rising(steps[name]["start without coin"], "solenoids"))
        for name in ("user-freeplus-clear", "user-freeplus-preserve", "quench-six", "quench-seven"):
            self.assertEqual(["500", "500", "1000"], [display_text(snapshots[name][step], 0)
                             for step in ("hit right D", "reclose right D", "next target C")])

        six = traces["quench-six-million-idle"]
        idle_begin = snapshots["quench-six-million-idle"]["cycle 12: score settles"]["time_s"]
        alternation = {segment_text(event) for event in six["events"]
                       if event["event"] == "display" and event["index"] == 0 and event["time_s"] > idle_begin + 5}
        self.assertTrue({"172400", "117240"} <= alternation)
        seven = snapshots["quench-seven-million-idle"]["million score idle"]
        self.assertEqual("1172400", display_text(seven, 0))
        self.assertEqual([7, 7, 7, 7, 2, 2], [d["layout"]["length"] for d in seven["displays"] if "segments" in d])

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained follow-up root unavailable")
    def test_matatest_dip_startup_controls(self):
        followup = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "online-followup"
        manifest, digest = curator.FOLLOWUP_FILES[curator.MATATEST_DIP_STARTUP]
        root = (followup / manifest).parent
        self.assertEqual(digest, check_manifest(root, "matatest"))
        expected_dips = {"baseline": [0, 0, 0x18, 0], "s14": [0, 0x20, 0x18, 0],
                         "s15": [0, 0x40, 0x18, 0], "s22": [0, 0, 0x38, 0]}
        rows = curator.table_rows("derivative-dip-read-path", "| Startup run")
        self.assertEqual(set(expected_dips), {name for name, *_ in rows})
        for name, _, first_fall, trace_digest in rows:
            with self.subTest(name=name):
                directory = root / name
                self.assertEqual(expected_dips[name], list((directory / "initial.nv").read_bytes()[-6:-2]))
                self.assertEqual(["wait"], [a["type"] for a in load_json(directory / "scenario.json")["actions"]])
                trace_path = directory / "trace.json"
                self.assertEqual(trace_digest.strip("`"), file_sha256(trace_path))
                trace = load_json(trace_path)
                self.assertIsNone(trace["failure"])
                self.assertEqual("matatest", trace["game"])
                for number in (36, 52):
                    self.assertEqual([(8.5, 1), (float(first_fall), 0)],
                                     output_transitions(trace, "lamp", number)[:2])

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained follow-up root unavailable")
    def test_matatest_initialized_credit_floor_and_coin_cap(self):
        followup = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "online-followup"
        manifest, digest = curator.FOLLOWUP_FILES[curator.MATATEST_PLAY]
        directory = (followup / manifest).parent
        self.assertEqual(digest, check_manifest(directory, "matatest"))
        for prefix, switch in (("zero", 6), ("cap", 10), ("centre", 11), ("right-coin", 9)):
            for setting in range(4):
                with self.subTest(prefix=prefix, setting=setting):
                    root = directory / f"{prefix}-{setting}"
                    start = prefix == "zero"
                    floor_enabled = setting == 3
                    scenario = load_json(root / "scenario.json")
                    self.assertEqual([switch] * (1 if start else 37), [a["switch"] for a in scenario["actions"]])
                    trace = load_json(root / "trace.json")
                    self.assertIsNone(trace["failure"])
                    self.assertEqual("matatest", trace["game"])
                    final = (root / "state/nvram/matatest.nv").read_bytes()
                    self.assertEqual(bytes([0, 0, 0, 4 | setting, 0, 0]), final[-6:])
                    if start:
                        self.assertEqual("01" if floor_enabled else "00", display_text(trace["snapshots"][-1], 4))
                        self.assertEqual(floor_enabled, 19 in rising(trace["steps"][-1], "solenoids"))
                    else:
                        self.assertEqual("09", display_text(trace["snapshots"][0], 4))
                        self.assertEqual("25", display_text(trace["snapshots"][-1], 4))
                        self.assertEqual(b"\x5f\x2f", final[0xad:0xaf])

    @unittest.skipUnless(os.getenv("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained follow-up root unavailable")
    def test_v22_audit_record_and_display_gates(self):
        directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "online-followup/audit12-native-final"
        expected = {
            "freeplay-reset": (0x0B, False, 9, 2, 9, ["02", "02", "09"]),
            "freeplay-count": (0x0B, True, 23, 2, 2, ["15", "23", "23"]),
            "paid": (0x09, False, 10, 2, 2, ["10", "10", "10"]),
            "freeplay-reset-higher-record": (0x0B, False, 9, 20, 20, ["20", "20", "20"]),
            "freeplay-reset-hidden": (0x03, False, 9, 2, 9, ["", "", ""]),
        }
        cases = {row[0].strip("`"): row[-1].strip("`")
                 for row in curator.table_rows("firmware-variants", "| Audit 12 native run")}
        self.assertEqual(expected.keys(), cases.keys())
        for name, (dips, count, balance, prior, saved, credits) in expected.items():
            with self.subTest(name=name):
                root = directory / name
                initial = (root / "initial.nv").read_bytes()
                final = (root / "state/nvram/matahard.nv").read_bytes()
                self.assertEqual((dips, count), (initial[-4], bool(initial[0x9f] & 0x40)))
                self.assertEqual((dips, count), (final[-4], bool(final[0x9f] & 0x40)))
                self.assertEqual((prior % 10, prior // 10), tuple(value >> 4 for value in initial[0xfe:0x100]))
                self.assertEqual((saved % 10, saved // 10), tuple(value >> 4 for value in final[0xfe:0x100]))
                self.assertEqual((balance % 10, balance // 10), tuple(value >> 4 for value in final[0xd4:0xd6]))
                trace_path = root / "trace.json"
                self.assertEqual(cases[name], file_sha256(trace_path))
                trace = load_json(trace_path)
                self.assertEqual("matahard", trace["game"])
                self.assertIsNone(trace["failure"])
                snapshots = {row["label"]: row for row in trace["snapshots"]}
                for label, credit in zip(("attract pre 2", "drain 2: ball closes outhole", "attract post 5"), credits):
                    row = snapshots[label]
                    self.assertIn(29, row["active_lamps"])
                    self.assertEqual(["432100"] * 4, [display_text(row, i) for i in range(4)])
                    self.assertEqual(credit, display_text(row, 4))
                service = [row for row in snapshots.values() if row["label"].startswith("self-test step ")]
                index = next(i for i, row in enumerate(service) if display_text(row, 5) == "12")
                self.assertEqual(["11", "12", "13"], [display_text(row, 5) for row in service[index - 1:index + 2]])
                self.assertEqual([str(saved)] * 4, [display_text(service[index], i) for i in range(4)])

    @unittest.skipUnless(all(os.getenv(name) for name in ("PINMAME_REVIEW_ARTIFACTS_ROOT", "PINMAME_ROM_LIBRARY_ROOT", "PINMAME_SOURCE_ROOT")),
                         "retained stock ROM and opcode-table roots unavailable")
    def test_disassembly_replays_from_pinned_roms(self):
        directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.ID / "online-followup"
        archives = Path(os.environ["PINMAME_ROM_LIBRARY_ROOT"])
        source_root = Path(os.environ["PINMAME_SOURCE_ROOT"])
        opcodes = source_root / "src/cpu/m6800/6800dasm.c"
        self.assertEqual(curator.MC6800_TABLE_SHA256, file_sha256(opcodes))
        reader = directory / "trace-stock-code.py"
        self.assertEqual(curator.STOCK_READER_SHA256, file_sha256(reader))
        for driver, source in (("matahari", curator.STOCK_CODE), ("matatest", curator.MATATEST_CODE)):
            with self.subTest(driver=driver):
                listing = subprocess.run([sys.executable, "-B", str(reader), str(archives / f"{driver}.zip"), str(opcodes)],
                                         check=True, capture_output=True, text=True)
                expected = (directory / curator.FOLLOWUP_FILES[source][0]).read_text(encoding="utf-8")
                self.assertEqual(expected.splitlines(), listing.stdout.splitlines())
        dip_reader = directory / "check-dip-consumers.py"
        self.assertEqual(curator.DIP_READER_SHA256, file_sha256(dip_reader))
        listing = subprocess.run([sys.executable, "-B", str(dip_reader), str(archives), str(source_root)],
                                 check=True, capture_output=True, text=True)
        expected = (directory / curator.FOLLOWUP_FILES[curator.DERIVATIVE_DIP_CODE][0]).read_text(encoding="utf-8")
        self.assertEqual(expected.splitlines(), listing.stdout.splitlines())

    @unittest.skipUnless(os.getenv("PINMAME_ROM_LIBRARY_ROOT"), "authorized ROM root unavailable")
    def test_archive_member_provenance(self):
        root = Path(os.environ["PINMAME_ROM_LIBRARY_ROOT"])
        expected = {
            "matahari": ("93c96382262c7624bbde461f5f3f59d5be9c876f9f0804a0fb7ee2d139259f8d",
                         {"725-21_2.716": "2347342f1281c097ea39c79236d85b00a1dfc7b2",
                          "720-20_6.716": "729e61a29691857112579efcdb96a35e8e5b1279"}, 2048),
            "mataharb": ("3f287eb0b89055537f8689a780d87fc9d34dd47cbfd9bc1faf1451725f1d52ad",
                         {"mata2732.u2": "7ccce6633fe16ec82ad387cd7e0913cf89be0cb1",
                          "72132fn.u6": "66046454d3b56aac52fcb303fd7bb7ef33296982"}, 4096),
            "mataharc": ("066693d3a9a953d529bf1deddc3d7f6793eef92a063f2399d15d49b945a622d4",
                         {"MataHari_U2.2716": "a8e9b7366d79685a96b7552e6c76ba0efafc3124",
                          "System-17_U6.2716": "7997a8733a29d0f2f883e02f9b635799f8d679f5"}, 2048),
            "matahard7": ("94ab62eabd52ba20c17c6c932c509ccdf73da3466c6da95788fd4492bd7703ee",
                          {"mataharif_U2_V22.2732": "1f1b3c3397040618da70c12072daee0ea9ce8dd2",
                           "mataharif_U6_V22.2732": "05b670c1571c2db2a865e1728d405b8f41db66a3"}, 4096),
            "matatest": ("f41dedbc954dd74be51c3652f429cd9a71de4dc6465e150bf2fe5c62733bf5c9",
                         {"matat0n.u2": "ced5fcd18009106ac3c7b42e36cdc10ce410eeeb",
                          "ptestn.u6": "8defbe8e11a75d26daf1351f439dd409f1efc608"}, 4096),
        }
        expected["matahard"] = expected["matahard7"]
        docs = {
            "mataharb": ("info.txt", "0eaa1a58ec17117f420e1e0757daa068ff786ebcbab889ceff62598ee973ad0c"),
            "mataharc": ("MataHari_Update.txt", curator.FREE_PLUS_TEXT),
            "matahard": ("MataHari_2732_Update_2025-04-13.txt", curator.FOLLOWUP_FILES[curator.QUENCH][1]),
        }
        docs["matahard7"] = docs["matahard"]
        for driver, (digest, members, member_size) in expected.items():
            path = root / f"{driver}.zip"
            self.assertEqual(digest, file_sha256(path))
            with zipfile.ZipFile(path) as archive:
                for filename, member_digest in members.items():
                    data = archive.read(filename)
                    self.assertEqual(member_size, len(data))
                    self.assertEqual(member_digest, sha1(data).hexdigest())
                if driver in docs:
                    member, text_digest = docs[driver]
                    self.assertEqual(text_digest, sha256(archive.read(member)).hexdigest())


if __name__ == "__main__":
    unittest.main()
