"""Focused partial-record and evidence regression checks for Embryon."""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_embryon as curator
import embryon_runtime
from build_external_evidence_manifest import check_manifest

EXPECTED_COILS = {1: 14, 2: 15, 3: 10, 4: 11, 5: 12, 6: 13, 7: 6,
                  8: 5, 9: 1, 10: 2, 11: 3, 12: 4, 13: 18, 14: 19, 15: 20}


def contract(record: dict) -> None:
    assert record["coverage"]["status"] == "partial"
    assert {x["id"] for x in record["drivers"]} == {"embryon", "embryona", "embryonb", "embryonc", "embryond", "embryone"}
    for d in record["drivers"]:
        if d["id"] != "embryon":
            assert d["physical_compatibility"] == "compatible"
            assert [(o["segment_start"], o["width"]) for o in d["display_overrides"]] == [(1, 7), (9, 7), (17, 7), (25, 7)]
    ins = record["inputs"]
    assert {i["binding"]["device"] for i in ins if i["kind"] != "dip_switch"} == set(range(1, 49)) | set(range(81, 89)) | {-7, -6, -5}
    assert {i["binding"]["device"] for i in ins if i["kind"] == "dip_switch"} == set(range(1, 33))
    dips = {i["binding"]["device"]: i for i in ins if i["kind"] == "dip_switch"}
    assert dips[1]["label"] == "Coin chute 1 pricing bit 1"
    assert dips[9]["label"] == "Coin chute 3 pricing bit 9"
    assert dips[17]["label"] == "Coin chute 2 pricing bit 17"
    assert dips[28]["label"] == "Match feature"
    out = record["outputs"]
    assert {x["binding"]["device"] for x in out if x["binding"]["group"] == "pinmame.output.lamp"} == {n for b in (1, 17, 33, 49, 65, 81, 97, 113) for n in range(b, b + 15)}
    coils = [x for x in out if x["binding"]["group"] == "pinmame.output.solenoid"]
    actual = {int(a["value"]): x["binding"]["device"] for x in coils for a in x["aliases"] if a["namespace"] == "manual.self-test"}
    assert actual == EXPECTED_COILS
    unfitted = next(x for x in coils if x["binding"]["device"] == 17)
    assert unfitted["availability"] == "unused" and unfitted["label"] == "Unfitted output 17"
    assert unfitted["provenance"]["status"] == "validated"
    assert {curator.CORE, curator.SOLENOID_SCHEMATIC, curator.RUN, curator.FLIP_RUN,
            curator.RESET_RUN + "-1", curator.RESET_RUN + "-2"} <= set(unfitted["provenance"]["source_refs"])
    switches = {i["binding"]["device"]: i for i in ins if i["binding"]["group"] == "pinmame.input.switch"}
    physical_switches = {n: d for n, d in switches.items() if d["kind"] == "switch" and d["availability"] == "used"}
    assert len(physical_switches) == 45
    assert all(d.get("normally_closed") is False for d in physical_switches.values())
    for n, source in { -7: curator.CABINET_SCHEMATIC, -6: curator.MPU_SCHEMATIC,
                       -5: curator.SOUND_SCHEMATIC, 82: curator.CABINET_SCHEMATIC,
                       84: curator.CABINET_SCHEMATIC }.items():
        assert {curator.CORE, source, "manual.embryon.color"} <= set(switches[n]["provenance"]["source_refs"])
    for n in range(41, 49):
        assert switches[n]["availability"] == "unused"
        assert switches[n]["provenance"]["status"] == "validated"
        assert {curator.MANUAL, curator.SWITCH_SCHEMATIC, curator.SOLENOID_SCHEMATIC,
                curator.CORE} <= set(switches[n]["provenance"]["source_refs"])
    assert switches[17]["physical"]["quantity"] == 2 and switches[17]["normally_closed"] is False
    assert "normally-closed" in switches[17]["physical"]["notes"]
    assert all(switches[n]["kind"] == "switch" and switches[n]["spatial"]["reason"] == "cabinet_or_service" for n in (82, 84))
    assert all(next(x for x in coils if x["binding"]["device"] == n)["availability"] == "unused" for n in (7, 8, 9))
    lamps = {x["binding"]["device"]: x for x in out if x["binding"]["group"] == "pinmame.output.lamp"}
    lamp_seed = json.loads((ROOT / "tools/seeds/bally/embryon-1981-lamps.json").read_text(encoding="utf-8"))
    assert all(lamps[int(n)]["label"] == label for n, label in lamp_seed["main"]["labels"].items())
    assert all(lamps[n]["availability"] == "unknown" for n in (52, 63, 117))
    assert {n for n in lamps if n < 65 and lamps[n].get("spatial", {}).get("reason") == "cabinet_or_service"} == {11, 13, 14, 15, 27, 29, 30, 31, 45, 46, 47, 61, 62}
    assert lamps[11]["label"] == "SHOOT AGAIN (BACKBOX)" and lamps[11]["availability"] == "used"
    assert lamps[27]["label"] == "MATCH" and lamps[27]["spatial"]["reason"] == "cabinet_or_service"
    assert lamps[56]["kind"] == "flasher" and lamps[56]["physical"]["quantity"] == 5
    assert lamps[59]["physical"]["location"] == "Apron credit indicator"
    assert all(lamps[n]["availability"] == "unused" for n in (72, 88, 104, 120))
    assert sum(lamps[n]["availability"] == "used" for n in lamps if n >= 65) == 27
    assert all(lamps[n]["availability"] == "unknown" for n in (73, 89, 105, 121))
    assert lamps[87]["physical"]["quantity"] == 2 and lamps[102]["physical"]["quantity"] == 1
    assert all("quantity" not in lamps[n]["physical"] for n in (70, 86))
    assert record["conflicts"][0]["source_refs"] == ["schematic.embryon.a9", "schematic.embryon.w1255"]
    assert "Resolution path:" in record["conflicts"][0]["description"]
    excerpts = {e["id"]: e for s in record["sources"] for e in s.get("excerpts", [])}
    assert excerpts["manual-page-22"]["reviewed"] is True
    assert excerpts["manual-pages-10-12"]["reviewed"] is True
    assert next(x for x in coils if x["binding"]["device"] == 18)["kind"] == "coil"


def startup_bank_times(raw: dict) -> dict:
    """Recompute coincident output callbacks inside the host's initial wait."""
    boot = raw["steps"][0]
    assert (boot["type"], boot["label"], boot["seconds"]) == ("wait", "boot stabilization", 25)
    start = next(s["time_s"] for s in raw["snapshots"] if s["label"] == "booted")
    end = next(s["time_s"] for s in raw["snapshots"] if s["label"] == boot["label"])
    times = {"on_s": {}, "off_s": {}}
    for n in range(17, 21):
        events = [e for e in raw["events"] if e.get("event") == "solenoid" and e.get("number") == n]
        assert [e["state"] for e in events[:2]] == [1, 0]
        assert start < events[0]["time_s"] < events[1]["time_s"] < end
        assert next(t["states"] for t in boot["transitions"]["solenoids"] if t["number"] == n)[:2] == [1, 0]
        if n == 17:
            assert len(events) == 2  # The only retained 17 activity is this bank pulse.
        times["on_s"][str(n)] = events[0]["time_s"]
        times["off_s"][str(n)] = events[1]["time_s"]
    for edge in times.values():
        assert max(edge.values()) - min(edge.values()) <= .001
    assert max(times["on_s"].values()) < min(times["off_s"].values())
    return times


class EmbryonTests(unittest.TestCase):
    def test_contract_and_mutation_guard(self):
        data = curator.build()
        contract(data)
        for n in (-7, -6, -5, 82, 84):
            for value in (None, True):
                altered = copy.deepcopy(data)
                switch = next(x for x in altered["inputs"] if x["binding"]["group"] == "pinmame.input.switch" and x["binding"]["device"] == n)
                if value is None:
                    del switch["normally_closed"]
                else:
                    switch["normally_closed"] = value
                with self.assertRaises(AssertionError):
                    contract(altered)
            altered = copy.deepcopy(data)
            switch = next(x for x in altered["inputs"] if x["binding"]["group"] == "pinmame.input.switch" and x["binding"]["device"] == n)
            switch["provenance"]["source_refs"] = [curator.CORE]
            with self.assertRaises(AssertionError):
                contract(altered)
        altered = copy.deepcopy(data)
        altered["drivers"][1]["physical_compatibility"] = "identical"
        with self.assertRaises(AssertionError):
            contract(altered)
        altered = copy.deepcopy(data)
        next(x for x in altered["outputs"] if x["id"] == "solenoid.17")["availability"] = "unknown"
        with self.assertRaises(AssertionError):
            contract(altered)
        altered = copy.deepcopy(data)
        next(x for x in altered["inputs"] if x["id"] == "switch.41")["provenance"]["source_refs"] = [curator.CORE]
        with self.assertRaises(AssertionError):
            contract(altered)
        altered = copy.deepcopy(data)
        next(x for x in altered["outputs"] if x["id"] == "lamp.11")["availability"] = "unused"
        with self.assertRaises(AssertionError):
            contract(altered)
        altered = copy.deepcopy(data)
        next(x for x in altered["outputs"] if x["id"] == "lamp.70")["physical"]["quantity"] = 2
        with self.assertRaises(AssertionError):
            contract(altered)
        altered = copy.deepcopy(data)
        next(x for x in altered["outputs"] if x["binding"]["group"] == "pinmame.output.solenoid" and x["binding"]["device"] == 14)["binding"]["device"] = 15
        with self.assertRaises(AssertionError):
            contract(altered)

    def test_excerpt_guard_rejects_modified_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "excerpt.md"
            path.write_bytes(curator.EXCERPT.read_bytes() + b"mutation")
            with mock.patch.object(curator, "EXCERPT", path):
                with self.assertRaises(ValueError):
                    curator.build()

    def test_schema_and_repository_validation(self):
        from jsonschema import Draft202012Validator
        from pinmame_game_defs.validation import validate_machine
        data = curator.build()
        schema = json.loads((ROOT / "schemas/machine.schema.json").read_text(encoding="utf-8"))
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(data)))
        self.assertEqual([], validate_machine(data, ROOT))

    def test_spatial_coordinates_are_derived_from_seed(self):
        data = curator.build()
        seed = json.loads(curator.SPATIAL_SEED.read_text(encoding="utf-8"))
        switches = {d["binding"]["device"]: d for d in data["inputs"] if d["binding"]["group"] == "pinmame.input.switch"}
        x, y = seed["objects"]["Bumper.Bumper1"]
        point = switches[40]["spatial"]["placements"][0]
        self.assertEqual((curator._round_point(x / 1257), curator._round_point(y / 1974)), (point["x"], point["y"]))
        self.assertEqual("observed", switches[40]["spatial"]["status"])
        self.assertNotIn("spatial", switches[5])
        self.assertEqual("cabinet_or_service", switches[3]["spatial"]["reason"])

    def test_check_is_read_only_and_detects_drift(self):
        paths = [curator.OUTPUT] + [target for target, _ in curator.TEXT_SEEDS.values()]
        before = [p.read_bytes() for p in paths]
        for _ in range(2):
            subprocess.run([sys.executable, "-B", str(ROOT / "tools/curate_embryon.py"), "--check"], cwd=ROOT, check=True, capture_output=True)
        self.assertEqual(before, [p.read_bytes() for p in paths])
        with tempfile.TemporaryDirectory() as directory:
            drifted = Path(directory) / "record.json"
            drifted.write_bytes(b"{}\n")
            with mock.patch.object(curator, "OUTPUT", drifted), mock.patch.object(sys, "argv", ["curator", "--check"]):
                with self.assertRaises(SystemExit):
                    curator.main()
            with mock.patch.object(curator, "PROMOTED", drifted), mock.patch.object(sys, "argv", ["curator", "--check"]):
                with self.assertRaises(SystemExit):
                    curator.main()

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "optional VPX evidence root not configured")
    def test_external_extraction_and_script(self):
        root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally/embryon-1981/local-v1.4/extraction"
        self.assertEqual("77e7c44ae196fed770dc82cbf2adedd0f725a409ee5230e10818b02d5b9ccae9", check_manifest(root, "embryon"))
        script = (root / "script.vbs").read_bytes()
        self.assertEqual("60703a639ca2d19a2a4caf2501e2ae62c38c4e76c568f58aa64e9aa2661fde75", hashlib.sha256(script).hexdigest())
        text = script.decode("latin-1").lower()
        for fragment in ("solcallback(1)", "dtright.soldropup", "solcallback(2)", "dtleft.soldropup", "solcallback(3)", "dtcenter.soldropup", "solcallback(4)", "solsaucereject", "solcallback(5)", "soltroughout", "solcallback(20)", "solrlflipper", "bstrough.initsw 0, 8, 5"):
            self.assertIn(fragment, text)
        seed = json.loads(curator.SPATIAL_SEED.read_text(encoding="utf-8"))
        for name, expected in seed["objects"].items():
            raw = json.loads((root / "gameitems" / (name + ".json")).read_text(encoding="utf-8"))
            obj = next(iter(raw.values()))
            if name.startswith("Wall."):
                points = obj["drag_points"]
                if "Slingshot" in name:
                    i = next(i for i, point in enumerate(points) if point["is_slingshot"])
                    actual = [(points[i][a] + points[(i + 1) % len(points)][a]) / 2 for a in ("x", "y")]
                else:
                    actual = [sum(p[a] for p in points) / len(points) for a in ("x", "y")]
            else:
                actual = [obj["center"]["x"], obj["center"]["y"]]
            self.assertEqual(expected, actual, name)
        modern = root.parent.parent / "unclepaulie-2.0.2/extraction"
        self.assertEqual("b54f92817455a7da1716c7929adafab4bf96acfe3a30093d87fa2649eede89d8", check_manifest(modern, "embryond"))
        self.assertEqual("7c4630d1d1805020b24b578013a5ad3255ee943495a6931c69ec2c7a427d503e", hashlib.sha256((modern / "script.vbs").read_bytes()).hexdigest())
        table = modern.parent / "download/Embryon (Bally 1981) w VR Room v2.0.2.vpx"
        self.assertEqual("b825e72293a452017a28f5ece39ed71b8fd6ab28edfdf6d0aef9addb14e5bb83", hashlib.sha256(table.read_bytes()).hexdigest())
        library = (root.parent.parent / "libraries/core.vbs").read_bytes()
        self.assertEqual("a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69", hashlib.sha256(library).hexdigest())
        code = library.decode("latin-1").lower()
        self.assertIn("controller.switch(mquecopy) = true", code)
        self.assertIn("controller.switch(mquecopy) = false", code)

    @unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "optional manual evidence root not configured")
    def test_external_manual(self):
        directory = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine/bally.embryon.1981"
        path = directory / "Embryon-arcarc.pdf"
        self.assertEqual("bca8ac2a339d9b49631f579d90c516cae2713fec5cfe149c2024a7ed23eb03f2", hashlib.sha256(path.read_bytes()).hexdigest())
        full = directory / "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf"
        self.assertEqual("55c800db586661821e84300aaf57fa24d825a492e78a94d41130b5916dcbe07b", hashlib.sha256(full.read_bytes()).hexdigest())
        self.assertEqual("c92a259d772ae57e6e99e3b62135307c76e71f281536ce0e7daa8fa01aa67029", hashlib.sha256((directory / "embryon_schematics.zip").read_bytes()).hexdigest())
        for name, digest in [("lamp.tif", "7e618f66ec4844a71114e2af264aaa9f4d92b32342ee30789faf348ad320315f"), ("lampaux.tif", "21e883165297b2052e364249eac59d64a2b1aaad3cffdb30f0d6e8c7d34dc9f9"), ("wiring1.tif", "470792c15ef8907ab1524634b99ce787472a10d3a0eed87125c518f3c18618f5"), ("switch.tif", "cd75ab89604b39a2b755f46ae2c3d4682ac50f982ef78b028e0cff92c2d0383f"), ("sol.tif", "cbda1f7f1c2f184f1ec339aa6ff0716ca40ae02684c8a06ceb5b5475dee7bd43")]:
            self.assertEqual(digest, hashlib.sha256((directory / "ipdb-schematics" / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(directory / "embryon_schematics.zip") as archive:
                member = next(m for m in archive.namelist() if Path(m).name.lower() == name)
                self.assertEqual(digest, hashlib.sha256(archive.read(member)).hexdigest())
        for name, digest in [("switch1.tif", "8395c33a4cd59785f39b546e5dca73b35a6049e2463062606980997a0e041496"),
                             ("mpu.tif", "edb79950e418341c862666e69eef28f8292bbd641a8eb8622fbaca9a485477f3"),
                             ("sound.tif", "d364f4e7c2483f200d96e484c4ce3fd20c9799ac760fa71bd542fc0dd77410d8")]:
            self.assertEqual(digest, hashlib.sha256((directory / "ipdb-schematics" / name).read_bytes()).hexdigest())
            with zipfile.ZipFile(directory / "embryon_schematics.zip") as archive:
                member = next(m for m in archive.namelist() if Path(m).name.lower() == name)
                self.assertEqual(digest, hashlib.sha256(archive.read(member)).hexdigest())
        # Derivation and geometry are portable across supported renderer versions;
        # committed image hashes are independently enforced by the curator.
        import render_excerpt_image
        from PIL import Image
        color = next(s for s in curator.build()["sources"] if s["id"] == "manual.embryon.color")
        self.assertEqual({"switch17-series-p40.webp", "a10-flasher.webp",
                          "solenoid-unfitted.webp", "solenoid-continuous.webp",
                          "service-cabinet-switches.webp", "cpu-diagnostic-contact.webp",
                          "sound-diagnostic-contact.webp"},
                         {Path(e["image"]).name for e in color["excerpts"]})
        for excerpt in color["excerpts"]:
            page, box = excerpt["locator"].removeprefix("PDF page ").split(", crop box ")
            output = mock.Mock()
            derivation, _ = render_excerpt_image.render(
                full, int(page), output, tuple(float(v) for v in box.split(",")),
                render_excerpt_image.DEFAULT_MIN_GLYPH_PIXELS,
                render_excerpt_image.DEFAULT_MAX_WIDTH, 80, rotate=270, color=False)
            self.assertEqual(excerpt["image_derivation"], derivation)
            output.write_bytes.assert_called_once()
            rendered = output.write_bytes.call_args.args[0]
            with Image.open(io.BytesIO(rendered)) as actual, Image.open(ROOT / excerpt["image"]) as committed:
                self.assertEqual(committed.size, actual.size)

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "optional runtime evidence root not configured")
    def test_external_trace_and_mapping_mutation(self):
        path = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "embryon-1981/harness/solenoid-run-1.json"
        self.assertEqual(EXPECTED_COILS, embryon_runtime.verify_trace(path))
        raw = json.loads(path.read_bytes())
        compact = json.loads(curator.RUNTIME_EVIDENCE.read_text(encoding="utf-8"))
        original_scenario = path.parent.parent / "solenoid-test.json"
        scenario = ROOT / "tools/harness-scenarios/by35/embryon-solenoid-test.json"
        self.assertEqual(raw["scenario"]["sha256"], hashlib.sha256(original_scenario.read_bytes()).hexdigest())
        self.assertEqual(original_scenario.read_bytes().replace(b"\r\n", b"\n"), scenario.read_bytes())
        self.assertEqual(raw["library_sha256"], compact["library_sha256"])
        for row in compact["observations"]:
            edge = {"event": "solenoid", "number": row["public"], "state": 1, "time_s": row["edge_s"]}
            self.assertIn(edge, raw["events"])
            display = next(e for e in raw["events"] if e.get("event") == "display" and e.get("index") == 0 and e["time_s"] == row["display_s"])
            self.assertEqual(row["segments"], display["segments"][-2:])
            self.assertEqual(row["self_test"], embryon_runtime.SEGMENTS[row["segments"][0]] * 10 + embryon_runtime.SEGMENTS[row["segments"][1]])
        bank = compact["startup_continuous_bank"]["runs"]["solenoid-self-test"]
        self.assertEqual({k: bank[k] for k in ("on_s", "off_s")}, startup_bank_times(raw))
        wrong = dict(EXPECTED_COILS, **{})
        wrong[1] = 15
        with mock.patch.object(embryon_runtime, "EXPECTED", wrong):
            with self.assertRaises(ValueError):
                embryon_runtime.verify_trace(path)
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "run.json"
            changed.write_bytes(path.read_bytes() + b" ")
            with self.assertRaises(ValueError):
                embryon_runtime.verify_trace(changed)

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "optional runtime evidence root not configured")
    def test_flipper_snapshots(self):
        path = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "embryon-1981/harness/flipper-run-1.json"
        raw_bytes = path.read_bytes()
        self.assertEqual("5edf495a5eab7262fcd3fb9d7d7ae3d7506f193bf705d2ac8c376e2c22e647b7", hashlib.sha256(raw_bytes).hexdigest())
        raw = json.loads(raw_bytes)
        self.assertIsNone(raw["failure"])
        scenario = ROOT / "tools/harness-scenarios/by35/embryon-flippers-and-tilt.json"
        original = path.parent.parent / "flippers-and-tilt.json"
        self.assertEqual(raw["scenario"]["sha256"], hashlib.sha256(original.read_bytes()).hexdigest())
        self.assertEqual(original.read_bytes().replace(b"\r\n", b"\n"), scenario.read_bytes())
        compact = json.loads(curator.FLIP_EVIDENCE.read_bytes())
        self.assertEqual(raw["library_sha256"], compact["library_sha256"])
        for row in compact["observations"]:
            sample = next(s for s in raw["snapshots"] if s["label"] == row["label"])
            self.assertEqual(row["time_s"], sample["time_s"])
            self.assertEqual(row["active_solenoids"], sample["active_solenoids"])

    def test_bulbs_and_physical_part_contract(self):
        record = curator.build()
        lamps = {d["binding"]["device"]: d for d in record["outputs"] if d["binding"]["group"] == "pinmame.output.lamp"}
        placed = [d for d in lamps.values() if d.get("spatial", {}).get("placements")]
        self.assertEqual(64, len(placed))
        self.assertEqual(65, sum(len(d["spatial"]["placements"]) for d in placed))
        for n in (6, 22, 38, 56, 59, 70, 86, 103):
            self.assertNotIn("spatial", lamps[n])
        coils = {d["binding"]["device"]: d for d in record["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
        self.assertEqual("FO-36-7000", coils[18]["physical"]["part_number"])
        self.assertEqual("AQ-25-500/34-4500", coils[46]["physical"]["part_number"])
        self.assertEqual("AO-27-1300", coils[20]["physical"]["part_number"])
        for lamp, coil in ((12, 13), (28, 12), (44, 11), (60, 10)):
            p = lamps[lamp]["spatial"]["placements"][0]
            q = coils[coil]["spatial"]["placements"][0]
            self.assertLess(((1257 * (p["x"] - q["x"])) ** 2 + (1974 * (p["y"] - q["y"])) ** 2) ** .5, 5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bulbs.json"
            path.write_bytes(curator.BULB_SEED.read_bytes() + b" ")
            with mock.patch.object(curator, "BULB_SEED", path), self.assertRaises(ValueError):
                curator.build()

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "optional runtime evidence root not configured")
    def test_single_drop_causality_and_mutation(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "embryon-1981"
        compact = json.loads(curator.RESET_EVIDENCE.read_bytes())
        scenario = ROOT / "tools/harness-scenarios/by35/embryon-single-drop.json"
        original = root / "single-drop.json"
        self.assertEqual(compact["scenario_sha256"], hashlib.sha256(original.read_bytes()).hexdigest())
        self.assertEqual(original.read_bytes().replace(b"\r\n", b"\n"), scenario.read_bytes())
        self.assertEqual(2, len(compact["runs"]))
        for run in compact["runs"]:
            raw_bytes = (root / run["raw_path"]).read_bytes()
            self.assertEqual(run["raw_sha256"], hashlib.sha256(raw_bytes).hexdigest())
            raw = json.loads(raw_bytes)
            self.assertEqual(run["library_sha256"], raw["library_sha256"])
            self.assertEqual(compact["scenario_sha256"], raw["scenario"]["sha256"])
            self.assertEqual(run["phases"], embryon_runtime.verify_single_drop(raw))
            self.assertEqual(run["reset_edges"], [e for e in raw["events"] if e.get("event") == "solenoid" and e.get("number") == 1])
            altered = copy.deepcopy(raw)
            phase = next(s for s in altered["steps"] if s["label"] == "NC back target restores")
            phase["transitions"]["solenoids"] = []
            with self.assertRaises(ValueError):
                embryon_runtime.verify_single_drop(altered)

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "optional review evidence root not configured")
    def test_lamp_seed_matches_current_primary_and_schematic(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "embryon-1981"
        primary = json.loads((root / "primary-main-lamps.json").read_text(encoding="utf-8"))
        schematic = json.loads((root / "terra-schematics/mapping.json").read_text(encoding="utf-8"))
        seed = json.loads((ROOT / "tools/seeds/bally/embryon-1981-lamps.json").read_text(encoding="utf-8"))
        self.assertEqual(primary, seed["main"])
        self.assertEqual(schematic["a9_outputs_including_selector7"], seed["aux"])
        self.assertEqual({str(row["public_lamp"]): row["scr"] for row in schematic["a5_outputs"]}, seed["main_scr"])

    @unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "optional runtime evidence root not configured")
    def test_standard_runtime_bundle_matches_raw_runs(self):
        root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "embryon-1981"
        bundle = json.loads((ROOT / "evidence/runtime/by35/embryon-1981-harness.json").read_bytes())
        self.assertEqual(bundle["source"]["sha256"], check_manifest(root / "harness", "embryon"))
        runtime = bundle["runtime"]
        bank = json.loads(curator.RUNTIME_EVIDENCE.read_bytes())["startup_continuous_bank"]
        self.assertEqual([17, 18, 19, 20], bank["public_addresses"])
        self.assertEqual({r["name"] for r in runtime["raw_runs"]}, set(bank["runs"]))
        self.assertEqual({str(k): v for k, v in EXPECTED_COILS.items()}, runtime["observations"]["physical_service_solenoid_to_public"])
        self.assertEqual(4, len(runtime["raw_runs"]))
        all_lamps, all_coils, normal_lamps = set(), set(), set()
        states = set()
        for run in runtime["raw_runs"]:
            relative = Path(run["retained_from"]).relative_to("review-artifacts/embryon-1981")
            raw_bytes = (root / relative).read_bytes()
            self.assertEqual(run["sha256"], hashlib.sha256(raw_bytes).hexdigest())
            raw = json.loads(raw_bytes)
            self.assertIsNone(raw["failure"])
            self.assertEqual(runtime["emulator"]["sha256"], raw["library_sha256"])
            self.assertEqual(run["scenario_sha256"], raw["scenario"]["sha256"])
            self.assertEqual(run["action_count"], len(raw["steps"]))
            self.assertEqual(run["snapshot_count"], len(raw["snapshots"]))
            self.assertEqual(run["initial_switches"], raw["initial_switches"])
            self.assertEqual([] if run["name"] == "solenoid-self-test" else [{"state": 1, "switch": 8}], raw["initial_switches"])
            scenario_name = raw["scenario"]["path"].replace("\\", "/").rsplit("/", 1)[-1]
            scenario_bytes = (root / scenario_name).read_bytes()
            self.assertEqual(raw["scenario"]["sha256"], hashlib.sha256(scenario_bytes).hexdigest())
            self.assertEqual(scenario_bytes.replace(b"\r\n", b"\n"), (ROOT / run["scenario_path"]).read_bytes())
            self.assertEqual({"type": "wait", "label": "boot stabilization", "seconds": 25}, json.loads(scenario_bytes)["actions"][0])
            pulse = bank["runs"][run["name"]]
            self.assertEqual(run["sha256"], pulse["raw_trace_sha256"])
            self.assertEqual({k: pulse[k] for k in ("on_s", "off_s")}, startup_bank_times(raw))
            altered = copy.deepcopy(raw)
            edge = next(e for e in altered["events"] if e.get("event") == "solenoid" and e.get("number") == 20)
            edge["time_s"] += .01
            with self.assertRaises(AssertionError):
                startup_bank_times(altered)
            states.add(raw["work_dir"])
            lamps = {e["number"] for e in raw["events"] if e.get("event") == "lamp" and e.get("state") == 1}
            coils = {e["number"] for e in raw["events"] if e.get("event") == "solenoid" and e.get("state") == 1}
            all_lamps.update(lamps)
            if run["name"] != "solenoid-self-test":
                normal_lamps.update(lamps)
            all_coils.update(coils)
            observations = runtime["observations"]["runs"][run["name"]]
            self.assertIn("startup_continuous_bank", observations["note"])
            self.assertEqual(sorted(coils), observations["solenoid_addresses_seen"])
            for action in observations.get("named_action_observations", []):
                self.assertEqual([], action["observed_switch_addresses"])
                self.assertEqual([action["input_address"]], action["host_stimulus_switch_addresses"])
                label = action["label"].removesuffix(" (held)")
                step = next(s for s in raw["steps"] if s["label"] == label)
                self.assertEqual(sorted(c["number"] for c in step["transitions"]["solenoids"]), action["transitioned_solenoid_addresses"])
                if action["label"].endswith(" (held)"):
                    snapshot = next(s for s in raw["snapshots"] if s["label"] == action["label"])
                    self.assertEqual(snapshot["active_solenoids"], action["active_solenoid_addresses"])
        self.assertEqual(4, len(states))
        self.assertEqual(sorted(all_lamps), runtime["observations"]["lamp_addresses_seen"])
        self.assertEqual(sorted(normal_lamps), runtime["observations"]["lamp_addresses_driven_outside_self_test"])
        self.assertTrue({52, 63, 72, 88, 104, 117, 120} <= normal_lamps)
        self.assertEqual(sorted(all_coils), runtime["observations"]["solenoid_addresses_seen"])
        source = root.parent.parent / "source-checkouts/pinmame-46e1a01a/src/wpc/by35.c"
        code = source.read_bytes()
        self.assertEqual("91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2", hashlib.sha256(code).hexdigest())
        self.assertEqual(bank["pinmame_source"]["sha256"], hashlib.sha256(code).hexdigest())
        self.assertEqual("src/wpc/by35.c", bank["pinmame_source"]["path"])
        self.assertEqual(bundle["source"]["revision"], bank["pinmame_source"]["revision"])
        lines = code.decode("utf-8").splitlines()
        self.assertEqual("data ^= 0xf0;", lines[356].strip())
        self.assertEqual("coreGlobals.pulsedSolState = (coreGlobals.pulsedSolState & 0xfff0ffff) | ((data & 0xf0)<<12);", lines[357].strip())
        self.assertEqual("locals.solenoids |= (data & 0xf0)<<12;", lines[358].strip())
        text = code.decode("utf-8")
        self.assertIn("if (lampadr != 0x0f)", text)
        self.assertIn("int lampdata = (locals.a0>>4)^0x0f;", text)
        self.assertIn("if (core_gameData->hw.lampCol > 0) by35_lampStrobe(1,locals.lampadr2);", text)


if __name__ == "__main__":
    unittest.main()
