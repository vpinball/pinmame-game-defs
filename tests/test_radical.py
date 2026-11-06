from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tools")]

import build_external_evidence_manifest as manifests
import curate_radical as curator
import drawing_callouts
import radical_spatial
import radical_evidence
from pinmame_game_defs.schema_validation import validate_against_schema
from pinmame_game_defs.spatial import extract_spatial_candidates
from pinmame_game_defs.validation import validate_machine

SW, DIP = "pinmame.input.switch", "pinmame.input.dip"
SOL, LAMP = "pinmame.output.solenoid", "pinmame.output.lamp"
NAMES = ("radical-1990", "radical-prototype-1990")


def read(path: Path):
    return json.loads(path.read_bytes())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def devices(definition, collection, group):
    rows = [d for d in definition[collection] if d["binding"]["group"] == group]
    result = {d["binding"]["device"]: d for d in rows}
    if len(rows) != len(result):
        raise AssertionError(f"duplicate binding in {group}")
    return result


def aliases(device):
    return {(a["namespace"], a["value"]) for a in device.get("aliases", [])}


class RadicalDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definitions = [read(ROOT / f"machines/partial/bally/{name}.json") for name in NAMES]

    def test_schema_validation_and_promotion_guard(self):
        for definition in self.definitions:
            with self.subTest(machine=definition["machine"]["id"]):
                self.assertEqual([], validate_against_schema(definition, ROOT / "schemas/machine.schema.json", "radical"))
                self.assertEqual([], validate_machine(definition, ROOT))
                self.assertEqual("partial", definition["coverage"]["status"])
                self.assertIn("spatial_placement", definition["coverage"]["missing"])
                promoted = copy.deepcopy(definition)
                promoted["coverage"].update(status="author_ready", missing=[])
                self.assertTrue(validate_machine(promoted, ROOT), "unresolved evidence must prevent promotion")
        self.assertIn("identity", self.definitions[1]["coverage"]["missing"])

    def test_driver_ownership_family_and_exact_opdb(self):
        production, prototype = self.definitions
        self.assertEqual({"radcl_l1": "identical", "radcl_g1": "identical", "radcl_l1c": "identical"},
                         {d["id"]: d["physical_compatibility"] for d in production["drivers"]})
        self.assertEqual({"radcl_p3"}, {d["id"] for d in prototype["drivers"]})
        self.assertEqual("G59ZY-MD8p7", production["machine"]["opdb_id"])
        self.assertNotIn("opdb_id", prototype["machine"])
        family = read(ROOT / "families/opdb/g59zy.json")
        self.assertEqual([], validate_against_schema(family, ROOT / "schemas/family.schema.json", "radical family"))
        self.assertEqual("G59ZY", family["family"]["opdb_id"])
        self.assertIn(production["machine"]["id"], {m["machine_id"] for m in family["members"]})
        claimed = {d["id"] for game in self.definitions for d in game["drivers"]}
        for path in (ROOT / "machines/stubs").rglob("*.json"):
            self.assertFalse(claimed & {d["id"] for d in read(path).get("drivers", [])}, str(path))

    def test_addresses_displays_and_legacy_aliases_by_binding(self):
        seed = read(ROOT / "tools/seeds/bally/radical-1990-legacy-aliases.json")["groups"]
        expected = {SW: set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)),
                    DIP: {0}, SOL: set(range(1, 65)), LAMP: set(range(1, 65))}
        for definition in self.definitions:
            indexes = {group: devices(definition, "inputs" if group in (SW, DIP) else "outputs", group) for group in expected}
            for group, addresses in expected.items():
                self.assertEqual(addresses, set(indexes[group]), group)
                for device in indexes[group].values():
                    self.assertIn(device["availability"], {"used", "unused", "unknown", "optional"})
            for group, entries in seed.items():
                for number, old in entries.items():
                    target_group, address = (SOL, 16) if (group, number) == (LAMP, "116") else (group, int(number))
                    self.assertIn(address, indexes[target_group], (group, number))
                    self.assertLessEqual({(a["namespace"], a["value"]) for a in old}, aliases(indexes[target_group][address]), (group, number))
            self.assertEqual([(0, 16, 1), (20, 16, 1)], sorted((d["segment_start"], d["width"], d["height"]) for d in definition["displays"]))
            self.assertTrue(all(d["kind"] == "segment" for d in definition["displays"]))

    def test_all_address_dispositions(self):
        unused_switches = {9, 13, 21, 25, 26, 33, 34, 35, 36, 41, 42, 45, 59, 60, 61, 62, 63, 64, 81, 83, 85, 86, 87, 88}
        unused_coils = {24, *range(33, 45), *range(49, 65)}
        for prototype, definition in enumerate(self.definitions):
            switches = devices(definition, "inputs", SW)
            coils = devices(definition, "outputs", SOL)
            for n, d in switches.items():
                expected = "optional" if n == 5 else "unused" if n in unused_switches or (n == 49 and not prototype) else "used"
                self.assertEqual(expected, d["availability"], n)
            for n, d in coils.items():
                expected = "unused" if n in unused_coils or (n in (3, 15) and not prototype) else "used"
                self.assertEqual(expected, d["availability"], n)
            for d in devices(definition, "outputs", LAMP).values():
                self.assertEqual("used", d["availability"])
            self.assertEqual("used", devices(definition, "inputs", DIP)[0]["availability"])

    def test_physical_and_virtual_hardware_differences(self):
        for prototype, definition in enumerate(self.definitions):
            switches = devices(definition, "inputs", SW)
            coils = devices(definition, "outputs", SOL)
            self.assertEqual(("virtual", "used"), (switches[2]["kind"], switches[2]["availability"]))
            for n in (57, 58):
                self.assertEqual(("virtual", "used"), (switches[n]["kind"], switches[n]["availability"]))
            for n in (81, 83, 85, 86, 87, 88):
                self.assertEqual("unused", switches[n]["availability"])
            for n in (82, 84):
                self.assertEqual("used", switches[n]["availability"])
            for n in (22, 23, 24, 30, 31, 32):
                self.assertEqual("opto", switches[n]["physical"]["switch_type"])
                self.assertIs(switches[n]["normally_closed"], False)
            self.assertEqual("microswitch", switches[20]["physical"]["switch_type"])
            self.assertEqual("switch", switches[20]["kind"])
            self.assertIn("popper" if prototype else "snake run", switches[16]["label"].lower())
            self.assertEqual("used" if prototype else "unused", switches[49]["availability"])
            for n in (3, 15):
                self.assertEqual("used" if prototype else "unused", coils[n]["availability"])
            self.assertEqual("flasher", coils[32]["kind"])
            self.assertEqual(2, len(coils[32]["spatial"]["placements"]))
            self.assertIn("1p", coils[32]["physical"]["notes"].lower())
            self.assertIn("1b", coils[32]["physical"]["notes"].lower())

    def test_mechanisms_and_relationships_refer_to_real_devices(self):
        for definition in self.definitions:
            all_devices = {d["id"] for field in ("inputs", "outputs") for d in definition[field]}
            for mechanism in definition["mechanisms"]:
                self.assertLessEqual(set(mechanism["actuators"] + mechanism["sensors"]), all_devices)
            switches = devices(definition, "inputs", SW)
            coils = devices(definition, "outputs", SOL)
            pairs = {(r["source"], r["destination"]) for r in definition["relationships"]}
            for src, dst in ((coils[12], switches[2]), (switches[82], switches[57]), (switches[84], switches[58])):
                self.assertIn((src["id"], dst["id"]), pairs)
            banks = {m["id"]: m for m in definition["mechanisms"]}
            for name, coil, sensors in (("bottom-bank", 6, (22, 23, 24)), ("top-bank", 4, (30, 31, 32)), ("bowtie", 7, (20,))):
                mechanism = banks["mechanism." + name]
                self.assertIn(coils[coil]["id"], mechanism["actuators"])
                self.assertEqual({switches[n]["id"] for n in sensors}, set(mechanism["sensors"]))

    def test_runtime_provenance_matches_physical_edition(self):
        for is_prototype, definition in enumerate(self.definitions):
            sw = devices(definition, "inputs", SW)
            sol = devices(definition, "outputs", SOL)
            expected = {"runtime.p3"} if is_prototype else {"runtime.l1", "runtime.g1"}
            for device in (sw[16], sw[49], sol[3], sol[15]):
                actual = {r for r in device["provenance"]["source_refs"] if r.startswith("runtime.")}
                self.assertEqual(expected, actual)

    def test_provenance_hashes_and_spatial_report(self):
        for definition in self.definitions:
            source_ids = {s["id"] for s in definition["sources"]}
            self.assertEqual(len(source_ids), len(definition["sources"]))
            for source in definition["sources"]:
                for excerpt in source.get("excerpts", []):
                    self.assertEqual(excerpt["sha256"], digest(ROOT / excerpt["path"]))
                    if "image" in excerpt:
                        self.assertEqual(excerpt["image_sha256"], digest(ROOT / excerpt["image"]))
            for device in definition["inputs"] + definition["outputs"]:
                self.assertLessEqual(set(device["provenance"]["source_refs"]), source_ids)
                spatial = device.get("spatial", {})
                if "placements" in spatial:
                    self.assertEqual("observed", spatial["status"])
                    for p in spatial["placements"]:
                        self.assertLessEqual(set(p["provenance"]["source_refs"]), source_ids)
                        self.assertTrue(0 <= p["x"] <= 1 and 0 <= p["y"] <= 1)
            report = radical_spatial.build_report(definition)
            self.assertEqual([], validate_against_schema(report, ROOT / "schemas/spatial-report.schema.json", "radical spatial"))
            self.assertEqual(definition["machine"]["id"], report["machine_id"])
            name = NAMES[self.definitions.index(definition)]
            self.assertEqual(report, read(ROOT / f"reports/spatial/bally/{name}.json"))
            self.assertEqual(radical_spatial.report_markdown(report), (ROOT / f"reports/spatial/bally/{name}.md").read_text(encoding="utf-8"))
            self.assertTrue((ROOT / definition["knowledge"]["path"]).is_file())
            actual = {d["id"]: d["spatial"]["placements"] for d in definition["inputs"] + definition["outputs"] if "placements" in d.get("spatial", {})}
            self.assertEqual(actual, {r["id"]: r["placements"] for r in report["located"]})
            self.assertEqual(sum(map(len, actual.values())), report["placement_count"])

    def test_source_roles_follow_the_claims(self):
        for definition in self.definitions:
            sources = {s["id"]: s for s in definition["sources"]}
            switches = devices(definition, "inputs", SW)
            for n in (20, 22, 23, 24, 30, 31, 32):
                kinds = {sources[ref]["kind"] for ref in switches[n]["provenance"]["source_refs"]}
                self.assertIn("manual", kinds)
                self.assertIn("pinmame_core", kinds)
            self.assertTrue(any(s["kind"] == "vpx_script" and s.get("known_working") for s in sources.values()))
            self.assertTrue(any(s["kind"] == "manual" and s.get("excerpts") for s in sources.values()))

    def test_drawing_fit_and_insert_projections(self):
        seed = read(ROOT / radical_spatial.SEED)
        drawing = seed["drawing"]
        pairs = [(tuple(c["pixel"]), tuple(c["normalized"])) for c in drawing["controls"]]
        fit = drawing_callouts.fit(pairs)
        for expected, actual in zip(drawing["transform"], fit):
            for a, b in zip(expected, actual):
                self.assertAlmostEqual(a, b, places=12)
        for a, b in zip(drawing["leave_one_out_errors"], drawing_callouts.leave_one_out(pairs)):
            self.assertAlmostEqual(a, b, places=12)
        self.assertEqual(58, len(drawing["lamps"]))
        solenoids = seed["solenoid_drawing"]
        fitted = drawing_callouts.fit([(c["pixel"], c["normalized"]) for c in solenoids["controls"]])
        self.assertEqual(solenoids["transform"], list(fitted))
        xy = drawing_callouts.apply(fitted, solenoids["flasher16"]["pixel"])
        self.assertEqual((.270, .480), tuple(round(v, 3) for v in xy))
        self.assertTrue(solenoids["flasher16"]["extrapolated"])
        switches = seed["switch_drawing"]
        switch_fit = drawing_callouts.fit([(c["pixel"], c["normalized"]) for c in switches["controls"]])
        self.assertEqual(switches["transform"], list(switch_fit))
        xy = drawing_callouts.apply(switch_fit, switches["switch27"]["pixel"])
        self.assertEqual((.876, .303), tuple(round(v, 3) for v in xy))
        self.assertTrue(switches["switch27"]["extrapolated"])
        for definition in self.definitions:
            lamps = devices(definition, "outputs", LAMP)
            for address, reading in drawing["lamps"].items():
                xy = drawing_callouts.apply(fit, reading["pixel"])
                self.assertEqual((round(xy[0], 3), round(xy[1], 3)), (reading["x"], reading["y"]))
                placement = lamps[int(address)]["spatial"]["placements"][0]
                self.assertEqual((reading["x"], reading["y"]), (placement["x"], placement["y"]))
            gi = devices(definition, "outputs", SOL)[10]
            centers = {(p["x"], p["y"]) for p in gi["spatial"]["placements"]}
            self.assertEqual(39, len(centers))
            self.assertEqual(len(centers), len(gi["spatial"]["placements"]))
            self.assertNotIn("quantity", gi["physical"])
            flasher = devices(definition, "outputs", SOL)[16]["spatial"]
            self.assertEqual("observed", flasher["status"])
            self.assertEqual((.270, .480), tuple(flasher["placements"][0][axis] for axis in ("x", "y")))
            self.assertIn(radical_spatial.SOLENOID_DRAWING_SOURCE, flasher["placements"][0]["provenance"]["source_refs"])
            middle_man = devices(definition, "inputs", SW)[27]["spatial"]["placements"][0]
            self.assertEqual((.876, .303), tuple(middle_man[axis] for axis in ("x", "y")))
            self.assertIn(radical_spatial.SWITCH_DRAWING_SOURCE, middle_man["provenance"]["source_refs"])


class RadicalEvidenceAndGenerationTests(unittest.TestCase):
    def test_configured_evidence_roots_and_paths_fail_closed(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("RADICAL_TEST_TMP")) as temp:
            root = Path(temp)
            self.assertEqual(root / "safe/file.json", radical_evidence.safe_path(root, "safe/file.json"))
            for path in ("../file", "/absolute", "C:/file", "dir\\file", "dir/../file", "dir//file"):
                with self.subTest(path=path), self.assertRaises(RuntimeError):
                    radical_evidence.safe_path(root, path)
            for env in radical_evidence.ROOT_ENV.values():
                with self.subTest(root=env), mock.patch.dict(os.environ, {env: temp}):
                    with self.assertRaisesRegex(RuntimeError, "retained evidence missing or changed"):
                        radical_evidence.verify_external_evidence(ROOT)

    def test_set_but_empty_vpx_root_fails_closed(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("RADICAL_TEST_TMP")) as temp, mock.patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": temp}):
            with self.assertRaises((RuntimeError, OSError, ValueError)):
                radical_spatial.verify_spatial_evidence(root=ROOT)

    def test_world_mesh_bounds_are_recomputed_beyond_the_file_digest(self):
        seed = read(ROOT / radical_spatial.SEED)
        mesh = seed["vpw"]["world_mesh"]
        expected = next(o for o in mesh["objects"] if o["name"] == "Flasherbase1")
        with tempfile.TemporaryDirectory(dir=os.environ.get("RADICAL_TEST_TMP")) as temp:
            root = Path(temp)
            path = root / "selected.obj"
            rows = ["o Flasherbase1"] + ["v " + " ".join(map(str, point)) for point in [expected["bounds_min"]] * (expected["vertex_count"] - 1) + [expected["bounds_max"]]]
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            mesh.update(relative_path="selected.obj", sha256=digest(path), objects=[expected])
            radical_spatial.verify_world_mesh(root, seed)
            rows[-1] = "v 999 999 999"
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            mesh["sha256"] = digest(path)
            with self.assertRaisesRegex(RuntimeError, "mesh bounds differ"):
                radical_spatial.verify_world_mesh(root, seed)

    @unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "VPX evidence root is unset")
    def test_retained_manifests_and_recompute_all_selected_geometry(self):
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally/radical-1990"
        seed = read(ROOT / radical_spatial.SEED)
        radical_spatial.verify_spatial_evidence(root=ROOT)
        old_points = [*seed["inputs"].values(), seed["production_switch_16"], seed["bowtie_sensor_projection"], *seed["solenoids"].values(), *seed["gi_bulbs"]]
        vpw = seed["vpw"]
        new_points = [vpw["prototype_sensor16"], vpw["prototype_popper_exit"], vpw["prototype_sling49"], *(p for points in vpw["flasher_bases"].values() for p in points)]
        for directory, table_hash, script_hash, manifest_hash, points in (
            (base, seed["table_sha256"], seed["script_sha256"], "3f1e5814729c29dad37e70ed401aad9480c67c425e176597289740da9b7a99c8", old_points),
            (base / "vpw-1.0.1", vpw["table_sha256"], vpw["script_sha256"], "437e81bf975dae1819f78b3bd01705c94ac11d74bcdd09cd1198179386dc1371", new_points),
            (base / "jpsalas-6.0.0", "8684ab7b113a3fdc5cdfb104e0b6da847ca571b985052d06870909b56cc16a13", "2c2c2c26c6922c08c3d09a9f6633aa0712219a18a345c9864f0eb341ed28619a", "529efc5ae37548e03d0a1a01269a12d9e42d22afec35788cf32c287858077532", []),
        ):
            extraction = directory / "extracted-vpxtool"
            manifest = read(extraction / "manifest.json")
            self.assertEqual(manifest_hash, digest(extraction / "manifest.json"))
            manifests.check_manifest(extraction, manifest["game"])
            self.assertEqual(script_hash, digest(extraction / "script.vbs"))
            tables = [p for p in (directory / "source").glob("*.vpx") if digest(p) == table_hash]
            self.assertEqual(1, len(tables), str(directory))
            candidates = extract_spatial_candidates(extraction, tables[0])["objects"]
            self.assertFalse((extraction / "gameitems/Trigger.sw27.json").exists())
            self.assertFalse(any(c["name"].lower() == "sw27" for c in candidates))
            f16 = read(extraction / "gameitems/Light.f16.json")["Light"]
            self.assertFalse(f16["show_bulb_mesh"])
            for point in points:
                self.assertEqual(point["sha256"], digest(extraction / point["artifact"]))
                matches = [c for c in candidates if c["type"].lower() == point["type"].lower() and c["name"] == point["name"] and (c["x"], c["y"]) == (point["x"], point["y"])]
                self.assertEqual(1, len(matches), point["artifact"])
        collection = next(c for c in read(base / "extracted-vpxtool/collections.json") if c["name"] == "aGiLights")
        bulbs = {}
        for name in collection["items"]:
            path = base / "extracted-vpxtool/gameitems" / f"Light.{name}.json"
            if not path.exists():
                continue
            light = read(path)["Light"]
            if not light.get("show_bulb_mesh") or light.get("is_backglass"):
                continue
            center = (light["center"]["x"], light["center"]["y"])
            candidate = (light["falloff_radius"], name)
            bulbs[center] = min(bulbs.get(center, candidate), candidate)
        self.assertEqual({name for _, name in bulbs.values()}, {p["name"] for p in seed["gi_bulbs"]})

    @unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "manual evidence root is unset")
    def test_retained_handbook_hash(self):
        path = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine/bally.radical.1990/ipdb-1904/Bally_1990_Radical_Operator_Handbook.pdf"
        self.assertEqual(curator.MANUAL_SHA, digest(path))

    def test_seed_matches_artifact_and_check(self):
        for prototype, name in enumerate(NAMES):
            artifact = ROOT / f"machines/partial/bally/{name}.json"
            self.assertEqual((ROOT / f"tools/seeds/bally/{name}.json").read_bytes(), artifact.read_bytes())
            self.assertEqual(read(artifact), curator.build(prototype=bool(prototype)))
        result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(ROOT / "tools/curate_radical.py"), "--check"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_checked_inputs_reject_mutation(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("RADICAL_TEST_TMP")) as temp:
            for original in (curator.MANUAL, curator.ALIASES):
                path = Path(temp) / original.name
                path.write_bytes(original.read_bytes())
                expected = digest(path)
                curator.checked(path, expected)
                path.write_bytes(path.read_bytes() + b" ")
                with self.assertRaises(RuntimeError):
                    curator.checked(path, expected)

    def test_regeneration_and_mutation_guards_in_isolated_tree(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("RADICAL_TEST_TMP")) as temp:
            root = Path(temp)
            for directory in ("schemas", "catalog", "evidence/excerpts/bally.radical.1990", "evidence/runtime/system-11", "machines/partial/bally", "tools/seeds/bally"):
                target = root / directory
                target.mkdir(parents=True, exist_ok=True)
                source = ROOT / directory
                patterns = ("*radical*",) if directory.endswith(("system-11", "bally")) else ("*",)
                for pattern in patterns:
                    for path in source.glob(pattern):
                        if path.is_file():
                            shutil.copy2(path, target / path.name)
            (root / "tools").mkdir(exist_ok=True)
            for path in (ROOT / "tools").glob("*.py"):
                shutil.copy2(path, root / "tools" / path.name)
            for directory in ("knowledge/bally", "reports/spatial/bally", "families/opdb"):
                target = root / directory
                target.mkdir(parents=True, exist_ok=True)
                for path in (ROOT / directory).glob("g59zy.json" if directory == "families/opdb" else "*radical*"):
                    if path.is_file():
                        shutil.copy2(path, target / path.name)
            env = os.environ.copy()
            for variable in ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT"):
                env.pop(variable, None)
            env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "src"), str(root / "tools")))

            def run(flag):
                return subprocess.run([sys.executable, "-X", "utf8", "-B", str(root / "tools/curate_radical.py"), flag], cwd=root, env=env, capture_output=True, text=True)

            def snapshot():
                return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}

            before = snapshot()
            result = run("--regenerate")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(before, snapshot(), "regeneration drifted in the isolated copy")
            result = run("--check")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)

            manual = next(s for s in read(root / "machines/partial/bally/radical-1990.json")["sources"] if s["kind"] == "manual" and s.get("excerpts"))
            mutations = [root / "tools/seeds/bally/radical-1990-manual.json", root / "tools/seeds/bally/radical-1990-legacy-aliases.json", *[root / relative for relative in curator.CHECKED_INPUTS], root / manual["excerpts"][0]["path"], root / "evidence/excerpts/bally.radical.1990/lamp-location-drawing.webp", root / "evidence/excerpts/bally.radical.1990/solenoid-location-drawing.webp", root / "machines/partial/bally/radical-1990.json"]
            for path in mutations:
                with self.subTest(tampered=path.name):
                    original = path.read_bytes()
                    path.write_bytes(original + b" ")
                    try:
                        result = run("--check")
                        self.assertNotEqual(0, result.returncode, f"tampering accepted: {path}")
                    finally:
                        path.write_bytes(original)
            path = root / manual["excerpts"][0]["path"]
            original = path.read_bytes()
            path.unlink()
            try:
                self.assertNotEqual(0, run("--check").returncode, "missing source excerpt was accepted")
            finally:
                path.write_bytes(original)
            for name in NAMES:
                ready = root / f"machines/author-ready/bally/{name}.json"
                ready.parent.mkdir(parents=True, exist_ok=True)
                ready.write_bytes(b"author-ready sentinel\n")
                before = snapshot()
                result = run("--regenerate")
                self.assertNotEqual(0, result.returncode, "author-ready replacement was accepted")
                self.assertEqual(before, snapshot(), "guard must fail before any writes")
                ready.unlink()


if __name__ == "__main__":
    unittest.main()
