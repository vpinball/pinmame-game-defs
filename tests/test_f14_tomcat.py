"""F-14 materializer regression tests. All mutable inputs are temporary copies."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_f14_tomcat as curator
import build_external_evidence_manifest as manifests
from pinmame_game_defs.jsonio import canonical_bytes

MANUAL_SHA = "a4ee36637957f770040db76015e784f000f90bab9cf7e8087bb86c37bd8dc10b"
TABLE_SHA = "db99410e18312f2166888586fb1bb79f6a3a2c8f992eea4ed7eb1b6d21f0ad4e"
GEOMETRY_EXCERPT = Path("evidence/excerpts/williams.f-14-tomcat.1987/geometry-anchors.md")
PLACEMENT_ROLES = {
    ("inputs", "switch"): "sensor",
    ("outputs", "coil"): "effect",
    ("outputs", "lamp"): "emitter",
    ("outputs", "flasher"): "emitter",
    ("outputs", "gi"): "emitter",
}
GROUPS = {
    ("inputs", "pinmame.input.switch"): set(range(-7, -3)) | set(range(1, 65)) | set(range(81, 89)),
    ("inputs", "pinmame.input.dip"): {0},
    ("outputs", "pinmame.output.solenoid"): set(range(1, 65)),
    ("outputs", "pinmame.output.lamp"): set(range(1, 65)),
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def by_address(definition, collection, group):
    return {d["binding"]["device"]: d for d in definition[collection] if d["binding"]["group"] == group}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def geometry_rows(root):
    text = (root / GEOMETRY_EXCERPT).read_text(encoding="utf-8")
    return json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])


def assert_exact_geometry(case, definition, rows):
    """Compare every authored placement with the pinned raw-coordinate read."""
    keyed = {f"{r['device']}.{r['object'].casefold()}": r for r in rows}
    case.assertEqual(len(rows), len(keyed), "duplicate raw geometry identity")
    expected = {key: row for key, row in keyed.items() if not row.get("excluded")}
    excluded = set(keyed) - set(expected)
    case.assertEqual(100, len(expected))
    case.assertEqual(6, len(excluded))
    actual = {}
    for collection in ("inputs", "outputs", "displays"):
        for device in definition[collection]:
            for placement in device.get("spatial", {}).get("placements", []):
                key = placement["id"]
                case.assertNotIn(key, actual, "duplicate canonical placement identity")
                actual[key] = (collection, device, placement)
    case.assertFalse(excluded.intersection(actual), "excluded rear domes must remain unplaced")
    case.assertEqual(set(expected), set(actual), "complete physical placement identity set")
    for key, row in expected.items():
        collection, device, placement = actual[key]
        case.assertEqual(row["device"], device["id"], key)
        point = (round(row["raw_x"] / 952, 6), round(row["raw_y"] / 1974, 6))
        case.assertEqual(point, (placement["x"], placement["y"]), f"{key}: coordinate drift")
        case.assertEqual(point, (row["x"], row["y"]), f"{key}: excerpt normalization drift")
        case.assertEqual(PLACEMENT_ROLES[collection, device["kind"]], placement["role"], f"{key}: role drift")
        case.assertEqual("playfield", placement["space"], key)


class TempCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="f14-test-", dir=os.environ.get("PINMAME_TEST_TMP_ROOT"))
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "repo"
        self.root.mkdir()


class MissingSeedTests(TempCase):
    def test_missing_and_malformed_seed_fail_without_other_inputs(self):
        with self.assertRaises(RuntimeError):
            curator.build(self.root)
        seed = self.root / curator.SEED
        seed.parent.mkdir(parents=True, exist_ok=True)
        seed.write_bytes(b"{broken")
        with self.assertRaises(RuntimeError):
            curator.build(self.root)


class RetainedFixtureTests(TempCase):
    """Synthetic retained evidence tests do not require the authored seed or actual evidence."""
    def setUp(self):
        super().setUp()
        self.roots = {name: self.base / name for name in ("vpx", "manuals", "review")}
        for root in self.roots.values():
            root.mkdir()
        self.files = []
        for name in self.roots:
            path = self.roots[name] / "file.bin"
            payload = (name + " fixture").encode()
            path.write_bytes(payload)
            self.files.append({"root": name, "path": "file.bin", "size": len(payload), "sha256": digest(payload)})
        self.extraction = self.roots["vpx"] / "extract"
        self.extraction.mkdir()
        (self.extraction / "script.vbs").write_bytes(b"script\n")
        (self.extraction / "geometry.json").write_bytes(b"{}\n")
        pin = manifests.write_manifest(self.extraction, "f14_l1")
        self.register = {"files": self.files, "extractions": [{"path": "extract/manifest.json", "sha256": pin, "file_count": 2, "total_bytes": 10}]}
        self.save_register()

    def save_register(self):
        write_json(self.root / curator.EVIDENCE, self.register)

    def verify(self):
        curator.verify_retained(self.roots["vpx"], self.roots["manuals"], self.roots["review"], root=self.root)

    def test_fixture_is_valid_and_every_external_root_is_verified(self):
        self.verify()
        for entry in self.files:
            path = self.roots[entry["root"]] / entry["path"]
            original = path.read_bytes()
            for mutation in ("change", "missing"):
                with self.subTest(root=entry["root"], mutation=mutation):
                    if mutation == "change":
                        path.write_bytes(original + b"!")
                    else:
                        path.unlink()
                    with self.assertRaises((RuntimeError, ValueError, OSError)):
                        self.verify()
                    path.write_bytes(original)
                    self.verify()

    def test_extraction_content_and_refreshed_manifest_cannot_evade_pin(self):
        self.verify()
        path = self.extraction / "script.vbs"
        path.write_bytes(b"changed\n")
        with self.assertRaises((RuntimeError, ValueError, OSError)):
            self.verify()
        manifests.write_manifest(self.extraction, "f14_l1")
        with self.assertRaises((RuntimeError, ValueError, OSError)):
            self.verify()

    def test_extraction_count_and_byte_pins_are_enforced(self):
        self.verify()
        item = self.register["extractions"][0]
        for field in ("file_count", "total_bytes"):
            original = item[field]
            item[field] += 1
            self.save_register()
            with self.subTest(field=field), self.assertRaises((RuntimeError, ValueError)):
                self.verify()
            item[field] = original
            self.save_register()
            self.verify()

    def test_unsafe_file_and_extraction_paths_are_refused(self):
        self.verify()
        bad_paths = ("../file.bin", "/absolute/file.bin", "C:/file.bin", "C:relative", "sub/../../file.bin", "sub\\file.bin")
        for section in ("files", "extractions"):
            item = self.register[section][0]
            original = item["path"]
            for bad in bad_paths:
                item["path"] = bad
                self.save_register()
                with self.subTest(section=section, path=bad), self.assertRaises((RuntimeError, ValueError)):
                    self.verify()
            item["path"] = original
        self.save_register()
        self.verify()

    def test_reparse_escape_is_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "file.bin").write_bytes(b"outside")
        link = self.roots["manuals"] / "link"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"directory symlink unavailable: {error}")
        item = self.files[1]
        item.update(path="link/file.bin", size=7, sha256=digest(b"outside"))
        self.save_register()
        with self.assertRaisesRegex(RuntimeError, "escapes|Unsafe"):
            self.verify()

    def test_spatial_report_uses_new_bounds_and_hashes_definition(self):
        definition = {"inputs": [], "outputs": [], "displays": [], "sources": [], "coverage": {"status": "partial", "missing": ["spatial_placement"]}}
        report = curator.spatial_report(definition, self.root)
        self.assertEqual(digest(canonical_bytes(definition)), report["definition_sha256"])
        self.assertEqual("playfield: x0 left, x1 right, y0 rear, y1 front; at most six decimals", report["coordinate_convention"])
        self.assertIn("952", report["transformation"])
        self.assertIn("1974", report["transformation"])
        self.assertIn("Earlier 964x2162 extractions are not coordinate sources", report["transformation"])


class AuthoredSeedTests(TempCase):
    """Use precisely the authored inputs, copied into an isolated temporary tree."""
    def setUp(self):
        super().setUp()
        required = (curator.SEED, curator.KNOWLEDGE_SEED, curator.EVIDENCE)
        absent = [str(p) for p in required if not (curator.ROOT / p).is_file()]
        if absent:
            self.fail("required authored seed inputs are missing: " + ", ".join(absent))
        for relative in required:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(curator.ROOT / relative, target)
        excerpt_dir = Path("evidence/excerpts") / curator.MACHINE_ID
        if (curator.ROOT / excerpt_dir).is_dir():
            shutil.copytree(curator.ROOT / excerpt_dir, self.root / excerpt_dir)
        for source in json.loads((self.root / curator.SEED).read_bytes())["sources"]:
            uri = source["uri"]
            if uri.startswith("evidence/") and not (self.root / uri).exists():
                target = self.root / uri
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(curator.ROOT / uri, target)
        self.definition = curator.build(self.root)

    def save_seed(self, definition):
        write_json(self.root / curator.SEED, definition)

    def test_identity_address_enumeration_and_partial_status(self):
        d = self.definition
        self.assertEqual("williams.f-14-tomcat.1987", d["machine"]["id"])
        self.assertEqual({"f14_l1", "f14_p3", "f14_p4", "f14_p5"}, {x["id"] for x in d["drivers"]})
        self.assertEqual(4, len(d["drivers"]))
        self.assertEqual("partial", d["coverage"]["status"])
        self.assertTrue({"spatial_placement", "variant_differences"}.issubset(d["coverage"]["missing"]))
        self.assertEqual(
            [("display.player-1", 0, 1, 7), ("display.player-2", 1, 9, 7),
             ("display.player-3", 2, 21, 7), ("display.player-4", 3, 29, 7)],
            [(display["id"], display["controller_index"], display["segment_start"], display["width"])
             for display in d["displays"]],
        )
        for (collection, group), expected in GROUPS.items():
            addresses = [x["binding"]["device"] for x in d[collection] if x["binding"]["group"] == group]
            self.assertEqual(expected, set(addresses), group)
            self.assertEqual(len(expected), len(addresses), group)
        self.assertNotIn("pinmame.output.gi", {x["binding"]["group"] for x in d["outputs"]})

    def test_flipper_routing_virtual_outputs_and_lamp_quantities(self):
        d = self.definition
        switches = by_address(d, "inputs", "pinmame.input.switch")
        coils = by_address(d, "outputs", "pinmame.output.solenoid")
        lamps = by_address(d, "outputs", "pinmame.output.lamp")
        edges = {(r["source"], r["destination"]) for r in d["relationships"]}
        for source, target in ((82, 15), (84, 63)):
            self.assertIn((switches[source]["id"], switches[target]["id"]), edges)
        for address in (45, 46, 47, 48):
            self.assertEqual("virtual", coils[address]["kind"], address)
        for side, addresses in (("right", (45, 46)), ("left", (47, 48))):
            for address in addresses:
                text = (coils[address]["label"] + " " + coils[address]["id"].replace("-", " ")).lower()
                self.assertIn(side, text, address)
        for address in (34, 36):
            self.assertEqual("virtual", coils[address]["kind"])
            self.assertEqual("unused", coils[address]["availability"])
        self.assertEqual(66, sum(x.get("physical", {}).get("quantity", 1) for x in lamps.values()))
        self.assertEqual(2, lamps[24]["physical"]["quantity"])
        self.assertEqual(2, lamps[39]["physical"]["quantity"])
        expected_ids = {2: 'lamp.lites-release', 3: 'lamp.blue-lite-special', 4: 'lamp.fly-again', 9: 'lamp.alpha-kill', 11: 'lamp.charlie-kill', 12: 'lamp.delta-kill', 17: 'lamp.1k-bonus', 18: 'lamp.2k-bonus', 20: 'lamp.8k-bonus', 21: 'lamp.16k-bonus', 22: 'lamp.32k-bonus', 23: 'lamp.64k-bonus', 24: 'lamp.special-drain-lanes', 25: 'lamp.2x-bonus-multiplier', 26: 'lamp.3x-bonus-multiplier', 27: 'lamp.4x-bonus-multiplier', 28: 'lamp.5x-bonus-multiplier', 29: 'lamp.6x-bonus-multiplier', 30: 'lamp.7x-bonus-multiplier', 31: 'lamp.8x-bonus-multiplier', 32: 'lamp.bonus-x-left-loop', 39: 'lamp.lites-kill-flipper-lanes', 40: 'lamp.landing-ball-popper', 47: 'lamp.release-ball-popper', 48: 'lamp.lock-on-ball-popper', 55: 'lamp.bonus-x-right-loop', 63: 'lamp.ripoff-line-of-death', 64: 'lamp.extra-ball-line-of-death'}
        self.assertEqual(expected_ids, {n: lamps[n]["id"] for n in expected_ids})

    def test_exact_sources_geometry_and_placements(self):
        d = self.definition
        assert_exact_geometry(self, d, geometry_rows(self.root))
        self.assertIn(MANUAL_SHA, {s.get("sha256") for s in d["sources"] if s["kind"] == "manual"})
        tables = [s for s in d["sources"] if s["kind"] == "vpx_table" and s.get("sha256") == TABLE_SHA]
        self.assertTrue(tables, "newest VPW geometry source must be recorded")
        table_ids = {s["id"] for s in tables}
        self.assertEqual((952, 1974), (d["machine"]["playfield"]["width"], d["machine"]["playfield"]["height"]))
        for collection in ("inputs", "outputs", "displays"):
            for device in d[collection]:
                for p in device.get("spatial", {}).get("placements", []):
                    self.assertTrue(table_ids.intersection(p["provenance"]["source_refs"]), device["id"])
                    for axis in ("x", "y"):
                        self.assertGreaterEqual(p[axis], 0)
                        self.assertLessEqual(p[axis], 1)
                        self.assertAlmostEqual(p[axis], round(p[axis], 6), places=9)
        report = curator.spatial_report(d, self.root)
        self.assertIn("952", report["transformation"])
        self.assertIn("1974", report["transformation"])
        self.assertIn("Earlier 964x2162 extractions are not coordinate sources", report["transformation"])

    def test_exact_geometry_guard_rejects_legal_coordinate_and_role_drift(self):
        rows = geometry_rows(self.root)
        for field, replacement in (("x", 0.500156), ("role", "emitter")):
            changed = copy.deepcopy(self.definition)
            device = next(d for d in changed["inputs"] if d["id"] == "switch.outhole")
            device["spatial"]["placements"][0][field] = replacement
            self.save_seed(changed)
            curator.build(self.root)  # Both mutations remain legal schema/semantic values.
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, "coordinate drift|role drift"):
                assert_exact_geometry(self, changed, rows)

    def test_mutated_seed_is_rejected(self):
        original = self.definition
        mutations = {}
        wrong = copy.deepcopy(original); wrong["machine"]["id"] = "williams.wrong.1987"; mutations["machine"] = wrong
        wrong = copy.deepcopy(original); wrong["drivers"][0]["id"] = "f14_wrong"; mutations["drivers"] = wrong
        for (collection, group), expected in GROUPS.items():
            matching = [i for i, d in enumerate(original[collection]) if d["binding"]["group"] == group]
            missing = copy.deepcopy(original); del missing[collection][matching[0]]; mutations[group + " missing"] = missing
            duplicate = copy.deepcopy(original)
            duplicate[collection][matching[0]]["binding"]["device"] = duplicate[collection][matching[-1]]["binding"]["device"] if len(matching) > 1 else 999
            mutations[group + " duplicate or wrong"] = duplicate
        gi = copy.deepcopy(original)
        gi["outputs"].append({"id": "device.fixture-gi", "label": "Fixture GI", "kind": "gi",
                              "binding": {"group": "pinmame.output.gi", "device": 1}, "aliases": [],
                              "provenance": copy.deepcopy(gi["outputs"][0]["provenance"])})
        mutations["independent GI"] = gi
        for name, value in mutations.items():
            with self.subTest(mutation=name):
                self.save_seed(value)
                with self.assertRaises((RuntimeError, ValueError)):
                    curator.build(self.root)
        self.save_seed(original)
        curator.build(self.root)

    def test_missing_or_malformed_inputs_and_excerpt_drift_are_refused(self):
        for relative, replacement in ((curator.SEED, None), (curator.SEED, b"{broken"), (curator.KNOWLEDGE_SEED, None)):
            path = self.root / relative
            original = path.read_bytes()
            if replacement is None: path.unlink()
            else: path.write_bytes(replacement)
            with self.subTest(path=relative, replacement=replacement), self.assertRaises((RuntimeError, ValueError)):
                curator.build(self.root)
            path.write_bytes(original)
        excerpts = [e for s in self.definition["sources"] for e in s.get("excerpts", [])]
        self.assertTrue(excerpts, "authored sources must include excerpts")
        excerpt = self.root / excerpts[0]["path"]
        data = excerpt.read_bytes()
        for missing in (False, True):
            if missing: excerpt.unlink()
            else: excerpt.write_bytes(data + b"drift")
            with self.subTest(missing=missing), self.assertRaises((RuntimeError, ValueError)):
                curator.build(self.root)
            excerpt.write_bytes(data)
        curator.build(self.root)

    def test_reproducible_regeneration_checks_and_generated_drift(self):
        paths = (curator.DEFINITION, curator.KNOWLEDGE, curator.REPORT, curator.REPORT_MD)
        curator.run(root=self.root)
        first = {p: (self.root / p).read_bytes() for p in paths}
        curator.run(root=self.root)
        self.assertEqual(first, {p: (self.root / p).read_bytes() for p in paths})
        for _ in range(2):
            curator.run(check=True, root=self.root)
            self.assertEqual(first, {p: (self.root / p).read_bytes() for p in paths})
        for p in paths:
            path = self.root / p
            path.write_bytes(first[p] + b"drift")
            before = {q: (self.root / q).read_bytes() for q in paths}
            with self.subTest(path=p), self.assertRaises(RuntimeError):
                curator.run(check=True, root=self.root)
            self.assertEqual(before, {q: (self.root / q).read_bytes() for q in paths})
            path.write_bytes(first[p])

    def test_author_ready_existing_artifact_blocks_both_modes_without_writes(self):
        curator.run(root=self.root)
        paths = (curator.DEFINITION, curator.KNOWLEDGE, curator.REPORT, curator.REPORT_MD)
        ready = self.root / curator.AUTHOR_READY
        ready.parent.mkdir(parents=True, exist_ok=True)
        ready.write_bytes(b"existing author-ready artifact")
        before = {p: (self.root / p).read_bytes() for p in paths}
        for check in (True, False):
            with self.subTest(check=check), self.assertRaisesRegex(RuntimeError, "author-ready"):
                curator.run(check=check, root=self.root)
            self.assertEqual(b"existing author-ready artifact", ready.read_bytes())
            self.assertEqual(before, {p: (self.root / p).read_bytes() for p in paths})


ROOT_NAMES = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")


@unittest.skipUnless(all(os.environ.get(name) for name in ROOT_NAMES), "all three retained evidence roots must be set")
class ActualRetainedEvidenceTests(unittest.TestCase):
    def test_actual_retained_evidence(self):
        curator.verify_retained(*(Path(os.environ[name]) for name in ROOT_NAMES))

    def test_representative_geometry_recomputed_from_retained_sources(self):
        vpx_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
        table = vpx_root / "williams/f-14-tomcat-1987/vpw-2025"
        rows = geometry_rows(curator.ROOT)
        selected = {name: next(r for r in rows if r["object"] == name) for name in
                    ("sw10", "LeftSlingShot", "Flasherbase1", "pDiverter1", "pBulb001")}
        for name, row in selected.items():
            raw = (table / "extracted" / row["file"]).read_bytes()
            self.assertEqual(row["sha256"], digest(raw), name)
            item = json.loads(raw)[row["kind"]]
            if name == "sw10":
                point = (item["center"]["x"], item["center"]["y"])
            elif name == "LeftSlingShot":
                points = item["drag_points"]
                point = tuple(sum(p[axis] for p in points) / len(points) for axis in ("x", "y"))
            elif name == "Flasherbase1":
                point = (item["position"]["x"], item["position"]["y"])
            else:
                continue  # Baked gate/bulb geometry needs the world mesh, not its stored origin.
            for actual, expected in zip(point, (row["raw_x"], row["raw_y"])):
                self.assertAlmostEqual(expected, actual, places=8, msg=name)

        register = json.loads((curator.ROOT / curator.EVIDENCE).read_bytes())
        pin = next(e for e in register["extractions"] if e["path"].endswith("/vpw-2025/world-obj/manifest.json"))
        manifest_path = vpx_root / pin["path"]
        raw = manifest_path.read_bytes()
        self.assertEqual(pin["sha256"], digest(raw))
        obj = next(f for f in json.loads(raw)["files"] if f["path"].endswith(".obj"))
        obj_path = manifest_path.parent / obj["path"]
        with obj_path.open("rb") as stream:
            self.assertEqual(obj["sha256"], hashlib.file_digest(stream, "sha256").hexdigest())
        mesh_names = {"pDiverter1", "pBulb001"}
        vertices = {name: [] for name in mesh_names}
        current = None
        with obj_path.open(encoding="utf-8") as stream:
            for line in stream:
                if line.startswith("o "):
                    current = line[2:].strip()
                elif current in mesh_names and line.startswith("v "):
                    vertices[current].append(tuple(float(n) for n in line.split()[1:4]))
        for name, points in vertices.items():
            row = selected[name]
            bounds = row["mesh_bounds"]
            self.assertEqual(bounds["vertices"], len(points), name)
            minimum = [min(p[axis] for p in points) for axis in range(3)]
            maximum = [max(p[axis] for p in points) for axis in range(3)]
            self.assertEqual(bounds["min"], minimum, name)
            self.assertEqual(bounds["max"], maximum, name)
            point = tuple((minimum[axis] + maximum[axis]) / 2 for axis in (0, 1))
            self.assertEqual((row["raw_x"], row["raw_y"]), point, name)


if __name__ == "__main__":
    unittest.main()
