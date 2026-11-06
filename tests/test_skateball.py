"""Regression checks for Skateball's physical and public-controller mappings."""
from __future__ import annotations

import hashlib
import io
import json
import os
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest import mock
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tools")]
import build_external_evidence_manifest as manifest  # noqa: E402
import curate_skateball  # noqa: E402
import skateball_spatial_report  # noqa: E402
import skateball_runtime_summary  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

MACHINE = "bally.skateball.1980"
DEFINITION = ROOT / "machines/partial/bally/skateball-1980.json"
AUTHOR_READY = ROOT / "machines/author-ready/bally/skateball-1980.json"
SPATIAL = ROOT / "tools/seeds/bally/skateball-1980-spatial.json"
SUMMARY = ROOT / "evidence/runtime/by35/skateball-1980-solenoid-tests.json"
READINGS = ROOT / "tools/seeds/bally/skateball-1980-display-readings.json"
CURATOR = ROOT / "tools/curate_skateball.py"
DRIVERS = {"skatebll", "skatebla", "skateblb"}
TEST_TO_PUBLIC = {1: 7, 2: 6, 3: 2, 4: 14, 5: 15, 6: 11, 7: 12, 8: 13, 9: 8, 10: 9, 11: 10, 12: 18, 13: 19}
ANCHORS = {("switch", 13): "Trigger.sw15", ("switch", 15): "Trigger.sw13", ("lamp", 25): "Bumper.Bumper2", ("lamp", 57): "Bumper.Bumper1", ("lamp", 41): "Bumper.Bumper3"}
LANE_PHOTO = "human-review.skateball.photo-026"
LANE_PHOTO_SHA256 = "8703e7d2fee918fb5838ccc7fd36a0b1a9563d019c0c4e984bce390049032a40"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def configured(name: str) -> Path | None:
    value = os.environ.get(name)
    return Path(value) if value else None


class SkateballTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load(DEFINITION)
        cls.spatial = load(SPATIAL)
        cls.summary = load(SUMMARY)
        cls.groups = {}
        for device in cls.definition["inputs"] + cls.definition["outputs"]:
            binding = device["binding"]
            group = cls.groups.setdefault(binding["group"], {})
            if binding["device"] in group:
                raise AssertionError(f"duplicate binding: {binding}")
            group[binding["device"]] = device
        cls.switches = cls.groups["pinmame.input.switch"]
        cls.dips = cls.groups["pinmame.input.dip"]
        cls.coils = cls.groups["pinmame.output.solenoid"]
        cls.lamps = cls.groups["pinmame.output.lamp"]

    def assert_spatial_geometry(self, seed: dict, raw_positions: dict[str, tuple[float, float]]) -> None:
        """Check every derivation against independently supplied raw object positions."""
        bounds = seed["bounds"]
        self.assertEqual({"left": 0.0, "right": 952.0, "top": 0.0, "bottom": 1974.0}, bounds)
        self.assertEqual(set(seed["objects"]), set(raw_positions))

        def normalized(x: float, y: float) -> dict:
            # Player view: left/rear are zero; right/front are one.
            return {"x": round((x - bounds["left"]) / (bounds["right"] - bounds["left"]), 6),
                    "y": round((y - bounds["top"]) / (bounds["bottom"] - bounds["top"]), 6)}

        self.assertEqual({"x": 0.0, "y": 0.0}, normalized(bounds["left"], bounds["top"]))
        self.assertEqual({"x": 1.0, "y": 1.0}, normalized(bounds["right"], bounds["bottom"]))
        for name, obj in seed["objects"].items():
            x, y = raw_positions[name]
            self.assertEqual((x, y), (obj["raw_x"], obj["raw_y"]), name)
            self.assertEqual(normalized(x, y), {k: obj[k] for k in ("x", "y")}, name)

        one_per_anchor = {"direct", "physical-lane-override", "wall-contact-projection", "wall-centroid",
                          "assembly-projection", "flipper-pivot-projection", "hidden-bulb-projection"}
        self.assertEqual(one_per_anchor | {"bank-centroid-projection"}, {d["method"] for d in seed["derivations"].values()})
        self.assertEqual(set(seed["device_spatial"]), set(seed["derivations"]))
        devices = {"switch": self.switches, "solenoid": self.coils, "lamp": self.lamps}
        for key, derivation in seed["derivations"].items():
            family, address = key.split(":")
            points = [raw_positions[name] for name in derivation["anchors"]]
            self.assertTrue(points, key)
            if derivation["method"] == "bank-centroid-projection":
                points = [(sum(x for x, _ in points) / len(points), sum(y for _, y in points) / len(points))]
            else:
                self.assertIn(derivation["method"], one_per_anchor, key)
            positions = [normalized(x, y) for x, y in points]
            self.assertEqual(positions, derivation["normalized_positions"], key)
            seed_spatial = seed["device_spatial"][key]
            self.assertEqual(positions, [{k: p[k] for k in ("x", "y")} for p in seed_spatial["placements"]], key)
            self.assertEqual(seed_spatial, devices[family][int(address)]["spatial"], key)
            self.assertTrue(all(p["provenance"]["status"] == "observed" for p in seed_spatial["placements"]), key)

    def test_every_spatial_derivation_and_mutation_guard(self) -> None:
        raw = {name: (obj["raw_x"], obj["raw_y"]) for name, obj in self.spatial["objects"].items()}
        self.assert_spatial_geometry(self.spatial, raw)
        altered = copy.deepcopy(self.spatial)
        altered["derivations"]["switch:13"]["normalized_positions"][0]["x"] += 0.01
        with self.assertRaises(AssertionError):
            self.assert_spatial_geometry(altered, raw)
        altered = copy.deepcopy(self.spatial)
        altered["objects"]["Trigger.sw15"]["x"] += 0.01
        with self.assertRaises(AssertionError):
            self.assert_spatial_geometry(altered, raw)

    def test_identity_catalog_and_complete_address_enumeration(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual((MACHINE, "Skateball", "Bally", 1980, 2170), (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["ipdb_id"]))
        self.assertEqual(DRIVERS, {d["id"] for d in self.definition["drivers"]})
        catalog = load(ROOT / "catalog/pinmame.json")
        self.assertEqual(DRIVERS, {d["id"] for d in catalog["drivers"] if d["machine_id"] == MACHINE})
        self.assertEqual(set(range(-7, -4)) | set(range(1, 49)) | set(range(81, 89)), set(self.switches))
        self.assertEqual(set(range(1, 33)), set(self.dips))
        self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | {45, 46, 47, 48}, set(self.coils))
        self.assertEqual({n for n in range(1, 64) if n % 16}, set(self.lamps))
        self.assertEqual(6, len(self.definition["displays"]))
        self.assertFalse(AUTHOR_READY.exists())

    def test_partial_coverage_and_undocumented_options(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual({"input_semantics", "output_semantics", "spatial_placement"}, set(coverage["missing"]))
        self.assertEqual({6, 21, 22, 29}, {n for n, d in self.dips.items() if d["availability"] == "unknown"})
        self.assertEqual("partial", self.definition["knowledge"]["status"])
        self.assertEqual([], self.definition["conflicts"])

    def test_core_and_catalog_licensing_preserves_per_file_scope(self) -> None:
        sources = {source["id"]: source for source in self.definition["sources"]}
        for source_id in ("pinmame.core.46e1a01a0f73", "pinmame.catalog.46e1a01a0f73"):
            source = sources[source_id]
            self.assertEqual("PinMAME license", source["license"])
            self.assertIn("LICENSE", source["locator"])
            excerpt = next(e for e in source["excerpts"] if e["path"].endswith("pinmame-license-notes.md"))
            self.assertEqual(sha(ROOT / excerpt["path"]), excerpt["sha256"])
        self.assertIn("unmarked core.c/core.h", sources["pinmame.core.46e1a01a0f73"]["locator"])

    def test_retained_source_license_file_markers(self) -> None:
        review_root = configured("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if review_root is None:
            self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
        checkout = review_root.parent / "source-checkouts/pinmame-46e1a01a"
        licensing = (checkout / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Every file that doesn't, will stay (for now) under the 'old MAME' license.", licensing)
        excerpt_text = (ROOT / "evidence/excerpts/bally.skateball.1980/pinmame-license-notes.md").read_text(encoding="utf-8")
        for name in ("LICENSE", "src/wpc/by35.c", "src/wpc/by35.h", "src/wpc/by35games.c",
                     "src/wpc/core.c", "src/wpc/core.h", "src/lisy/lisy35.c",
                     "src/libpinmame/libpinmame.cpp", "src/libpinmame/libpinmame.h"):
            self.assertIn(sha(checkout / name), excerpt_text, name)
            if name != "LICENSE":
                first_line = (checkout / name).read_text(encoding="utf-8").splitlines()[0]
                self.assertEqual(name not in ("src/wpc/core.c", "src/wpc/core.h"), first_line == "// license:BSD-3-Clause", name)

    def test_legacy_tilt_and_aliases(self) -> None:
        self.assertEqual("unused", self.switches[1]["availability"])
        self.assertEqual("switch.middle-right-drop-target", self.switches[2]["id"])
        self.assertEqual("switch.tilt", self.switches[7]["id"])
        expected = {"s_self_test": -7, "s_cpu_diagnose": -6, "s_sound_diagnose": -5, "s_start_button": 6, "s_tilt": 7, "s_coin_3": 9, "s_coin_2": 10, "s_coin_1": 11, "s_slam_tilt": 16, "s_flipper_lower_right": 82, "s_flipper_lower_left": 84}
        coils = {"c_game_on": 19, "c_flipper_lower_right": 46, "c_flipper_upper_right": 46,
                 "c_flipper_lower_left": 48, "c_flipper_upper_left": 48}
        for devices, namespace, named in ((self.switches, "vpe-legacy.switch", expected), (self.coils, "vpe-legacy.coil", coils)):
            alias_to_devices = {}
            for number, device in devices.items():
                for alias in device.get("aliases", []):
                    if alias["namespace"] == namespace:
                        alias_to_devices.setdefault(alias["value"], []).append(number)
                for value in {str(number), f"{number:02d}", f"{number:03d}"}:
                    self.assertIn({"namespace": namespace, "value": value}, device["aliases"], (number, value))
            for name, number in named.items():
                self.assertEqual([number], alias_to_devices.get(name), name)
            self.assertTrue(all(len(numbers) == 1 for numbers in alias_to_devices.values()), alias_to_devices)
        for n in (46, 48):
            self.assertIn("continuous outputs 17/18/19/20", self.coils[n]["physical"]["notes"])
            self.assertIn("Numeric aliases remain address-bound", self.coils[n]["physical"]["notes"])
        self.assertNotIn({"namespace": "vpe-legacy.coil", "value": "c_flipper_upper_right"}, self.coils[19]["aliases"])

    def test_self_test_mappings_in_all_three_rom_runs(self) -> None:
        rows = load(READINGS)["runs"]
        self.assertEqual(DRIVERS, {row["driver"] for row in rows})
        for row in rows:
            self.assertEqual(TEST_TO_PUBLIC, {p["self_test_number"]: p["public_address"] for p in row["pairings"]}, row["driver"])
            self.assertEqual(13, len(row["pairings"]))
            for pair in row["pairings"]:
                self.assertEqual(pair["segments_sha256"], hashlib.sha256(canonical_bytes(pair["segments"])).hexdigest())
                self.assertEqual(f"{pair['self_test_number']:02d}", skateball_runtime_summary.decode(pair["segments"]))
                self.assertTrue(0 < pair["display_time_s"] - pair["rising_edge_time_s"] < 0.15)
        self.assertEqual({str(k): v for k, v in TEST_TO_PUBLIC.items()}, self.summary["runtime"]["observations"]["physical_service_solenoid_to_public"])
        for test, public in TEST_TO_PUBLIC.items():
            self.assertIn({"namespace": "manual.self-test", "value": f"{test:02d}"}, self.coils[public]["aliases"])

    def test_unfitted_continuous_outputs_and_synthetic_flippers(self) -> None:
        for n in (17, 20):
            self.assertEqual("unknown", self.coils[n]["availability"])
            self.assertEqual(f"output.unfitted-continuous-{n}", self.coils[n]["id"])
            self.assertEqual(f"Unfitted continuous output {n}", self.coils[n]["label"])
            self.assertEqual("observed", self.coils[n]["provenance"]["status"])
            self.assertEqual("unused", self.coils[n]["spatial"]["reason"])
            self.assertIn("marks the physical load", self.coils[n]["physical"]["notes"])
            self.assertIn("have not been established", self.coils[n]["physical"]["notes"])
            for driver in DRIVERS:
                note = self.summary["runtime"]["observations"]["runs"][driver + "-solenoid-test"]["note"]
                pulses = json.loads(note.split("Continuous startup output pulses: ", 1)[1].split(". The schematic", 1)[0])
                self.assertIn(n, {p["number"] for p in pulses if p["state"] == 1})
        self.assertEqual("device.k1-flipper-enable-relay", self.coils[19]["id"])
        for n, side in ((46, "right"), (48, "left")):
            device = self.coils[n]
            self.assertEqual(("used", "coil", 2), (device["availability"], device["kind"], device["physical"]["quantity"]))
            self.assertEqual(2, len(device["spatial"]["placements"]))
            self.assertIn(side, device["label"].lower())
        for n in (45, 47):
            self.assertEqual(("used", "virtual", "virtual"), (self.coils[n]["availability"], self.coils[n]["kind"], self.coils[n]["spatial"]["reason"]))
        snapshots = {s["label"]: s["active_solenoid_addresses"] for s in self.summary["runtime"]["observations"]["runs"]["skatebll-flippers-tilt"]["named_action_observations"]}
        self.assertTrue({45, 46} <= set(snapshots["right button before tilt (held)"]))
        self.assertTrue({47, 48} <= set(snapshots["left button before tilt (held)"]))
        self.assertEqual([18], snapshots["physical tilt7 drops enable (held)"])

    def test_seven_shared_contacts_and_proven_causality(self) -> None:
        self.assertEqual(7, self.switches[17]["physical"]["quantity"])
        self.assertEqual(7, len(self.switches[17]["spatial"]["placements"]))
        actual = {(r["source"], r["destination"], r["kind"]) for r in self.definition["relationships"]}
        expected = {(self.switches[s]["id"], self.coils[c]["id"], "pulse") for s, c in ((37, 14), (36, 15), (40, 11), (39, 12), (38, 13))}
        expected |= {(self.coils[19]["id"], self.coils[c]["id"], "relay_gated") for c in (46, 48)}
        self.assertEqual(expected, actual)
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        for slug, coil, switches in (("skate-bank", 8, (20, 21, 22, 23, 24)), ("top-bank", 9, (26, 27, 28)), ("middle-bank", 10, (2, 3, 4))):
            mechanism = mechanisms[f"mechanism.{slug}"]
            self.assertEqual([self.coils[coil]["id"]], mechanism["actuators"])
            self.assertEqual({self.switches[n]["id"] for n in switches}, set(mechanism["sensors"]))

    def test_observed_lane_layout_and_factory_bumper_placements(self) -> None:
        for (group, address), object_name in ANCHORS.items():
            device = (self.switches if group == "switch" else self.lamps)[address]
            obj = self.spatial["objects"][object_name]
            p = device["spatial"]["placements"][0]
            self.assertEqual((obj["x"], obj["y"]), (p["x"], p["y"]), (group, address))
            self.assertEqual("observed", p["provenance"]["status"])
        self.assertGreater(self.switches[13]["spatial"]["placements"][0]["x"], self.switches[15]["spatial"]["placements"][0]["x"])
        self.assertGreater(self.lamps[25]["spatial"]["placements"][0]["x"], self.lamps[57]["spatial"]["placements"][0]["x"])
        for n in (13, 15):
            self.assertIn("observed layout mismatch", self.switches[n]["physical"]["notes"].lower())
            self.assertIn("original 1980 artwork orientation remains unverified", self.switches[n]["physical"]["notes"].lower())
            self.assertIn(LANE_PHOTO, self.switches[n]["spatial"]["placements"][0]["provenance"]["source_refs"])
        for n in (25, 57):
            self.assertIn("swap", self.lamps[n]["physical"]["notes"].lower())
        for device in self.definition["inputs"] + self.definition["outputs"]:
            for p in device.get("spatial", {}).get("placements", []):
                self.assertEqual("observed", p["provenance"]["status"], device["id"])
                self.assertTrue(0 <= p["x"] <= 1 and 0 <= p["y"] <= 1, device["id"])

    def test_replacement_board_scope_and_matching_lane_lamp_mismatch(self) -> None:
        sources = {source["id"]: source for source in self.definition["sources"]}
        photo = sources[LANE_PHOTO]
        self.assertEqual(("human_review", LANE_PHOTO_SHA256), (photo["kind"], photo["sha256"]))
        self.assertTrue(photo["uri"].startswith("https://imgproxy.pinside.com/"))
        self.assertIn("https://pinside.com/pinball/forum/topic/bally-skateball-playfield-swap", photo["locator"])
        self.assertIn("replacement reproduction", photo["rights"])
        self.assertIn("does not independently authenticate original 1980 artwork", photo["rights"])
        self.assertEqual("observed", self.spatial["lane_orientation"]["status"])
        self.assertFalse(self.spatial["lane_orientation"]["original_1980_artwork_authenticated"])
        self.assertEqual({"left": 1, "middle": 2, "right": 3}, self.spatial["lane_orientation"]["replacement_labels"])
        self.assertEqual({"left": {"switch": 13, "lamp": 24}, "middle": {"switch": 14, "lamp": 40},
                          "right": {"switch": 15, "lamp": 56}}, self.spatial["lane_orientation"]["table_pairing"])
        manual = sources["manual.bally.skateball.1980"]
        relative_order = next(e for e in manual["excerpts"] if e["id"] == "excerpt.skateball.manual-lane-relative-order")
        self.assertEqual("980467aa90c5971db50c228be52c94c53b5790494f4b1dc07090558ef2ebbf01", relative_order["image_sha256"])
        self.assertIn("left-to-right 15, 14, 13", self.spatial["lane_orientation"]["manual_role"])
        for number, lane in ((13, 3), (15, 1)):
            self.assertEqual(f"switch.number-{lane}-lane", self.switches[number]["id"])
            self.assertEqual(f"Number {lane} lane", self.switches[number]["label"])
            self.assertEqual(f"Rear rollover lane #{lane}", self.switches[number]["physical"]["location"])
            self.assertFalse(self.spatial["derivations"][f"switch:{number}"]["original_artwork_authenticated"])
        for number in (24, 56):
            self.assertNotIn("spatial", self.lamps[number], "render-light centers are not adopted as sockets")
            self.assertIn("lamp 24 through Light.l24 on the left", self.lamps[number]["physical"]["notes"])
            self.assertIn("lamp 56 through Light.l56 on the right", self.lamps[number]["physical"]["notes"])
            self.assertIn("observed mismatch", self.lamps[number]["physical"]["notes"])
            self.assertIn(LANE_PHOTO, self.lamps[number]["provenance"]["source_refs"])
        for device in self.switches.values():
            self.assertNotIn("asserts a closure at public 1.", device.get("physical", {}).get("notes", ""))

    def test_game_text_is_utf8_without_replacement_characters(self) -> None:
        def check(content: bytes) -> None:
            self.assertNotIn("\ufffd", content.decode("utf-8"))

        paths = {DEFINITION, SPATIAL, CURATOR, curate_skateball.SOURCES, curate_skateball.KNOWLEDGE_SEED,
                 curate_skateball.KNOWLEDGE, skateball_spatial_report.REPORT, skateball_spatial_report.MARKDOWN,
                 ROOT / "tools/skateball_spatial_report.py", Path(__file__)}
        paths.update(ROOT / excerpt["path"] for source in self.definition["sources"] for excerpt in source.get("excerpts", []))
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                check(path.read_bytes())
        with self.assertRaises(AssertionError):
            check("corrupted \ufffd text".encode("utf-8"))
        with self.assertRaises(UnicodeDecodeError):
            check(b"invalid UTF-8 \xff")

    def test_excerpt_hashes_and_determinism(self) -> None:
        excerpts = 0
        sources = {source["id"]: source for source in self.definition["sources"]}
        self.assertEqual("ddbcae8cdc87ccdd7305f02ad853bd039d4b6489b25bcd2b82c0c8e03e07fb02", self.spatial["source_vpx_sha256"])
        self.assertEqual(self.spatial["source_vpx_sha256"], sources["vpx-table.skateball.1-0-4"]["sha256"])
        self.assertEqual(self.spatial["source_script_sha256"], sources["vpx-script.skateball.1-0-4"]["sha256"])
        for source in self.definition["sources"]:
            for excerpt in source.get("excerpts", []):
                excerpts += 1
                self.assertEqual(excerpt["sha256"], sha(ROOT / excerpt["path"]), excerpt["path"])
                if "image" in excerpt:
                    self.assertEqual(excerpt["image_sha256"], sha(ROOT / excerpt["image"]), excerpt["image"])
        self.assertGreater(excerpts, 0)
        for _ in range(2):
            result = subprocess.run([sys.executable, "-B", str(CURATOR), "--check"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, result.returncode, result.stderr)

    def test_runtime_bundle_satisfies_evidence_schema(self) -> None:
        validator = jsonschema.Draft202012Validator(load(ROOT / "schemas/evidence.schema.json"))
        self.assertEqual([], list(validator.iter_errors(self.summary)))
        broken = copy.deepcopy(self.summary)
        del broken["runtime"]["game"]
        self.assertTrue(list(validator.iter_errors(broken)), "schema check must reject a missing required field")

    def test_curator_refuses_drift_and_an_existing_author_ready_record(self) -> None:
        built = curate_skateball.build_definition()
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            definition, knowledge, promoted = base / "partial.json", base / "knowledge.md", base / "promoted.json"
            definition.write_bytes(DEFINITION.read_bytes())
            knowledge.write_bytes(curate_skateball.KNOWLEDGE.read_bytes())
            errors = io.StringIO()
            with mock.patch.object(curate_skateball, "ROOT", base), mock.patch.object(curate_skateball, "build_definition", return_value=built), mock.patch.object(curate_skateball, "DEFINITION", definition), mock.patch.object(curate_skateball, "KNOWLEDGE", knowledge), mock.patch.object(curate_skateball, "AUTHOR_READY", promoted), mock.patch.object(sys, "argv", ["curate_skateball.py", "--check"]), redirect_stderr(errors):
                self.assertEqual(0, curate_skateball.main())
                definition.write_bytes(definition.read_bytes() + b" ")
                self.assertNotEqual(0, curate_skateball.main())
                self.assertIn("Curated artifact drift", errors.getvalue())
            promoted.write_bytes(b"existing author-ready data")
            before = (definition.read_bytes(), knowledge.read_bytes(), promoted.read_bytes())
            with mock.patch.object(curate_skateball, "DEFINITION", definition), mock.patch.object(curate_skateball, "KNOWLEDGE", knowledge), mock.patch.object(curate_skateball, "AUTHOR_READY", promoted), mock.patch.object(sys, "argv", ["curate_skateball.py", "--regenerate"]), redirect_stderr(io.StringIO()):
                self.assertNotEqual(0, curate_skateball.main())
            self.assertEqual(before, (definition.read_bytes(), knowledge.read_bytes(), promoted.read_bytes()))

    def test_extraction_refuses_an_unconfigured_root(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "PINMAME_VPX_SOURCES_ROOT"}
        result = subprocess.run([sys.executable, "-B", str(CURATOR), "--verify-extraction"], env=env, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("PINMAME_VPX_SOURCES_ROOT", result.stderr)

    def test_spatial_report_matches_inputs_and_detects_drift(self) -> None:
        report_path = ROOT / "reports/spatial/bally/skateball-1980.json"
        markdown_path = ROOT / "reports/spatial/bally/skateball-1980.md"
        report = load(report_path)
        self.assertEqual("pinmame-spatial-blockers", report["format"])
        self.assertEqual(sha(DEFINITION), report["definition_sha256"])
        self.assertEqual(sha(SPATIAL), report["source_hashes"]["spatial_seed_sha256"])
        unplaced = sorted(d["id"] for group in ("inputs", "outputs") for d in self.definition[group] if d.get("availability") == "used" and "spatial" not in d)
        self.assertEqual(unplaced, [d["id"] for d in report["unplaced_physical_devices"]])
        altered = copy.deepcopy(self.definition)
        next(d for d in altered["inputs"] if d["binding"] == {"group": "pinmame.input.switch", "device": 13})["spatial"]["placements"][0]["x"] = 0.1
        with self.assertRaisesRegex(ValueError, "spatial data differs"):
            skateball_spatial_report.build_report(altered, self.spatial, "definition-hash", "seed-hash")
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            json_copy, md_copy = base / "report.json", base / "report.md"
            json_copy.write_bytes(report_path.read_bytes())
            md_copy.write_bytes(markdown_path.read_bytes())
            errors = io.StringIO()
            with mock.patch.object(skateball_spatial_report, "ROOT", base), mock.patch.object(skateball_spatial_report, "REPORT", json_copy), mock.patch.object(skateball_spatial_report, "MARKDOWN", md_copy), mock.patch.object(sys, "argv", ["skateball_spatial_report.py", "--check"]), redirect_stderr(errors):
                self.assertEqual(0, skateball_spatial_report.main())
                md_copy.write_bytes(md_copy.read_bytes() + b"drift")
                self.assertNotEqual(0, skateball_spatial_report.main())
                self.assertIn("Spatial report drift", errors.getvalue())

    def test_retained_extraction_and_exact_anchor_recomputation(self) -> None:
        root = configured("PINMAME_VPX_SOURCES_ROOT")
        if root is None:
            self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
        base = root / "bally/skateball-1980"
        extraction = base / "extracted-vpxtool"
        self.assertEqual(self.spatial["source_vpx_sha256"], sha(base / "Skateball (Bally 1980) 1.0.4.vpx"))
        self.assertEqual(self.spatial["source_script_sha256"], sha(extraction / "script.vbs"))
        script = (extraction / "script.vbs").read_text(encoding="utf-8")
        for number in (13, 15):
            self.assertRegex(script, rf"(?im)^\s*Sub sw{number}_Hit:Controller\.Switch\({number}\)\s*=\s*1")
        for number, light in ((25, "Bumper1L"), (41, "Bumper3L"), (57, "Bumper2L")):
            self.assertRegex(script, rf"(?im)^\s*NFadeL\s+{number},\s*{light}\s*$")
        for number, x in ((24, 481.5), (56, 685.6491)):
            self.assertRegex(script, rf"(?im)^\s*NFadeLm\s+{number},\s*l{number}\s*$")
            light = load(extraction / f"gameitems/Light.l{number}.json")["Light"]
            self.assertEqual(x, light["center"]["x"])
        self.assertLess(load(extraction / "gameitems/Light.l24.json")["Light"]["center"]["x"],
                        load(extraction / "gameitems/Light.l56.json")["Light"]["center"]["x"])
        self.assertEqual(self.spatial["extraction_manifest_sha256"], manifest.check_manifest(extraction, "skatebll"))
        actual_manifest = manifest.build_manifest(extraction, "skatebll")
        self.assertEqual(self.spatial["extraction_file_count"], len(actual_manifest["files"]))
        self.assertEqual(self.spatial["extraction_total_bytes"], sum(f["size"] for f in actual_manifest["files"]))
        game = load(extraction / "gamedata.json")
        self.assertEqual(self.spatial["bounds"], {k: game[k] for k in ("left", "top", "right", "bottom")})
        raw_positions = {}
        for name, obj in self.spatial["objects"].items():
            item = load(extraction / obj["file"])[obj["type"]]
            self.assertEqual(obj["sha256"], sha(extraction / obj["file"]))
            self.assertEqual(obj["name"], item["name"], name)
            if obj["method"] == "drag_point_centroid":
                points = [{k: p[k] for k in ("x", "y")} for p in item["drag_points"]]
                self.assertEqual(points, obj["drag_points"], name)
                self.assertTrue(points, name)
                raw_positions[name] = tuple(sum(p[k] for p in points) / len(points) for k in ("x", "y"))
            else:
                self.assertIn(obj["method"], {"center", "position"}, name)
                position = item[obj["method"]]
                raw_positions[name] = (position["x"], position["y"])
        self.assert_spatial_geometry(self.spatial, raw_positions)
        result = subprocess.run([sys.executable, "-B", str(CURATOR), "--verify-extraction"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stderr)

    def test_retained_supplemental_table_and_mesh_export(self) -> None:
        root = configured("PINMAME_VPX_SOURCES_ROOT")
        if root is None:
            self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
        audit = self.spatial["supplemental_vpw_audit"]
        base = root / "bally/skateball-1980/vpw-1.0"
        extraction = base / "extracted-vpxtool"
        sources = {source["id"]: source for source in self.spatial["sources"]}
        self.assertEqual(audit["table_sha256"], sources["vpx-table.skateball.vpw-1-0"]["sha256"])
        self.assertEqual(audit["script_sha256"], sources["vpx-script.skateball.vpw-1-0"]["sha256"])
        self.assertEqual(audit["table_sha256"], sha(base / "Skateball (Bally 1980) VPW 1.0.vpx"))
        self.assertEqual(audit["script_sha256"], sha(extraction / "script.vbs"))
        self.assertEqual(audit["extraction_manifest_sha256"], manifest.check_manifest(extraction, "skatebll"))
        files = load(extraction / "manifest.json")["files"]
        self.assertEqual(audit["extraction_file_count"], len(files))
        self.assertEqual(audit["extraction_total_bytes"], sum(f["size"] for f in files))
        self.assertTrue(audit["world_obj_path"].startswith("vpx-sources/"))
        self.assertEqual(audit["world_obj_sha256"], sha(root / audit["world_obj_path"].removeprefix("vpx-sources/")))
        lights = [load(path)["Light"] for path in (extraction / "gameitems").glob("Light.*.json")]
        self.assertEqual(audit["light_objects"], len(lights))
        self.assertEqual(audit["show_bulb_mesh_true"], sum(bool(light["show_bulb_mesh"]) for light in lights))
        primitives = list((extraction / "gameitems").glob("Primitive.*.json"))
        self.assertEqual(audit["primitive_objects"], len(primitives))
        mesh = load(extraction / "gameitems/Primitive.BM_Parts.json")["Primitive"]
        self.assertEqual(audit["combined_mesh"], mesh["name"])
        self.assertEqual((audit["combined_mesh_stored_x"], audit["combined_mesh_stored_y"]), (mesh["position"]["x"], mesh["position"]["y"]))

    def test_retained_photos_and_mesh_inventory(self) -> None:
        root = configured("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if root is None:
            self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
        sources = {source["id"]: source for source in self.spatial["sources"]}
        for number in ("022", "026", "036"):
            self.assertEqual(sources[f"human-review.skateball.photo-{number}"]["sha256"], sha(root / f"skateball-1980/photos/photo-{number}.jpg"))
        audit = self.spatial["supplemental_vpw_audit"]
        for stem in ("component_inventory", "component_map", "isolated_profiles"):
            relative = audit[f"{stem}_path"]
            self.assertTrue(relative.startswith("review-artifacts/"))
            self.assertEqual(audit[f"{stem}_sha256"], sha(root / relative.removeprefix("review-artifacts/")), stem)

    def test_runtime_summary_recomputes_from_four_retained_runs(self) -> None:
        root = configured("PINMAME_REVIEW_ARTIFACTS_ROOT")
        roms = configured("PINMAME_ROM_LIBRARY_ROOT")
        if root is None or roms is None:
            self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT and PINMAME_ROM_LIBRARY_ROOT are required")
        runs = root / "skateball-1980/harness"
        records = self.summary["runtime"]["raw_runs"]
        self.assertEqual(4, len(records))
        for record in records:
            self.assertEqual(record["sha256"], sha(runs / record["retained_from"].rsplit("/", 1)[-1]))
        startup_excerpt = (ROOT / "evidence/excerpts/bally.skateball.1980/continuous-startup-observations.md").read_text(encoding="utf-8")
        for driver in DRIVERS:
            run = load(runs / f"{driver}-coil-run.json")
            for number in (17, 18, 19, 20):
                events = [e for e in run["events"] if e["event"] == "solenoid" and e["number"] == number and e["time_s"] < 8]
                self.assertEqual([1, 0], [e["state"] for e in events])
                self.assertIn(f"| {driver} | {number} | {events[0]['time_s']:.6f} | {events[1]['time_s']:.6f} |", startup_excerpt)
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/skateball_runtime_summary.py"), "--runs", str(runs), "--rom-root", str(roms), "--check"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(self.summary["source"]["sha256"], manifest.check_manifest(runs, "skatebll"))
        with tempfile.TemporaryDirectory() as temporary:
            altered = load(READINGS)
            altered["runs"][0]["pairings"][0]["segments"][-1] |= 0x80
            alternate = Path(temporary) / "readings.json"
            alternate.write_bytes(canonical_bytes(altered))
            with mock.patch.object(skateball_runtime_summary, "READINGS", alternate):
                with self.assertRaisesRegex(ValueError, "differ from the pinned readings"):
                    skateball_runtime_summary.build(runs, roms)
                before = alternate.read_bytes()
                with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
                    skateball_runtime_summary.build(runs, roms, write_readings=True)
                self.assertEqual(before, alternate.read_bytes())

    def test_retained_manual_sources_match_pins(self) -> None:
        root = configured("PINMAME_MANUALS_ROOT")
        if root is None:
            self.skipTest("PINMAME_MANUALS_ROOT is not configured")
        base = root / "by-machine" / MACHINE
        sources = {s["id"]: s for s in self.definition["sources"]}
        for source, name, digest in (
            ("manual.bally.skateball.1980", "skateball-bally-1980-ipdb-manual.pdf", "0758b23c3d33b28c06be006ba768151075b0f31ae9cddad6739e6c5ab7513a1a"),
            ("schematic.bally.skateball.1980", "skateball-bally-1980-ipdb-schematics.pdf", "1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c"),
        ):
            self.assertEqual(digest, sources[source]["sha256"])
            self.assertEqual(digest, sha(base / name))


if __name__ == "__main__":
    unittest.main()
