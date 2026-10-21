"""Focused regression and deterministic-curator checks for Bally Viking (1979)."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import curate_viking as curator  # noqa: E402
import build_external_evidence_manifest as manifest_tool  # noqa: E402

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json  # noqa: E402
from pinmame_game_defs.validation import validate_machine  # noqa: E402
from pinmame_game_defs.workspace import resolve_working_root  # noqa: E402

MACHINE_ID = "bally.viking.1979"
ROOT_DRIVER_RELEASE_YEAR = "1980"
DRIVERS = {"viking", "vikingb"}
SWITCHES = set(range(-7, -4)) | set(range(1, 49)) | set(range(81, 89))
MATRIX_SWITCHES = set(range(1, 49))
DIPS = set(range(1, 33))
LAMPS = set(range(1, 64)) - {16, 32, 48}
SOLENOIDS = set(range(1, 16)) | set(range(17, 21)) | {45, 46, 47, 48}
LITERAL_BLANK_SWITCH_ROWS = {20, 21, 22, 23, 31, 34}
THIRD_COLUMN_UNUSED_SWITCHES = set(range(41, 49))
UNUSED_FLIPPER_BUTTONS = {81, 83, 85, 86, 87, 88}
SELF_TEST_TO_PUBLIC = {
    1: 7, 2: 6, 3: 8, 4: 9, 5: 14, 6: 15, 7: 1, 8: 2, 9: 10,
    10: 11, 11: 12, 12: 13, 13: 3, 14: 4, 15: 5, 16: 18, 17: 19, 18: 17,
}
EXTERNAL_ENVIRONMENT = {
    "vpx_sources": "PINMAME_VPX_SOURCES_ROOT",
    "manuals": "PINMAME_MANUALS_ROOT",
    "review_artifacts": "PINMAME_REVIEW_ARTIFACTS_ROOT",
}


def _devices_by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
    return {
        device["binding"]["device"]: device
        for device in definition[collection]
        if device.get("binding", {}).get("group") == group
    }


class VikingDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(curator.DEFINITION_PATH)
        cls.definition_seed = load_json(curator.DEFINITION_SEED_PATH)
        cls.spatial_seed = load_json(curator.SPATIAL_SEED_PATH)
        cls.knowledge = curator.KNOWLEDGE_PATH.read_bytes()
        cls.switches = _devices_by_address(cls.definition, "inputs", "pinmame.input.switch")
        cls.dips = _devices_by_address(cls.definition, "inputs", "pinmame.input.dip")
        cls.lamps = _devices_by_address(cls.definition, "outputs", "pinmame.output.lamp")
        cls.solenoids = _devices_by_address(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.sources = {source["id"]: source for source in cls.definition["sources"]}

    def test_schema_v2_identity_and_partial_gate_preserve_project_vs_release_year(self) -> None:
        self.assertEqual([], validate_machine(self.definition, ROOT))
        self.assertEqual(2, self.definition["schema_version"])
        machine = self.definition["machine"]
        self.assertEqual((MACHINE_ID, 1980), (machine["id"], machine["year"]))
        self.assertEqual("partial", self.definition["coverage"]["status"])
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        self.assertEqual(DRIVERS, set(drivers))
        self.assertEqual(ROOT_DRIVER_RELEASE_YEAR, drivers["viking"]["year"])
        self.assertEqual("viking", drivers["vikingb"]["clone_of"])
        self.assertEqual("2004", drivers["vikingb"]["year"])

    def test_variants_keep_six_digit_root_and_seven_digit_compatible_conversion_overrides(self) -> None:
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        root = drivers["viking"]
        converted = drivers["vikingb"]
        self.assertEqual("identical", root["physical_compatibility"])
        self.assertNotIn("display_overrides", root)
        player_ids = {f"display.player-{number}-score" for number in range(1, 5)}
        base_displays = {display["id"]: display for display in self.definition["displays"]}
        self.assertEqual({6}, {base_displays[display_id]["width"] for display_id in player_ids})
        self.assertEqual("compatible", converted["physical_compatibility"])
        overrides = {override["target"]: override for override in converted["display_overrides"]}
        self.assertEqual(player_ids, set(overrides))
        self.assertEqual([1, 9, 17, 25], [overrides[f"display.player-{number}-score"]["segment_start"] for number in range(1, 5)])
        self.assertEqual({7}, {override["width"] for override in overrides.values()})

    def test_exact_controller_address_contract_and_unused_rows(self) -> None:
        self.assertEqual(SWITCHES, set(self.switches))
        self.assertEqual(DIPS, set(self.dips))
        self.assertEqual(LAMPS, set(self.lamps))
        self.assertEqual(SOLENOIDS, set(self.solenoids))
        self.assertEqual(
            LITERAL_BLANK_SWITCH_ROWS | THIRD_COLUMN_UNUSED_SWITCHES | UNUSED_FLIPPER_BUTTONS,
            {address for address, device in self.switches.items() if device["availability"] == "unused"},
        )
        self.assertTrue(all(self.switches[address]["availability"] == "unused" for address in LITERAL_BLANK_SWITCH_ROWS))
        self.assertTrue(all(self.switches[address]["availability"] == "unused" for address in THIRD_COLUMN_UNUSED_SWITCHES))
        self.assertEqual("used", self.switches[82]["availability"])
        self.assertEqual("used", self.switches[84]["availability"])
        for address in MATRIX_SWITCHES:
            if self.switches[address]["availability"] == "used":
                self.assertIs(False, self.switches[address]["normally_closed"], address)

    def test_raw_rom_self_test_mapping_uses_public_solenoid_addresses_not_printed_numbers(self) -> None:
        runtime_sources = {
            source_id
            for source_id, source in self.sources.items()
            if source.get("kind") in {"runtime_scenario", "service_diagnostic"}
        }
        self.assertTrue(runtime_sources, "the raw ROM self-test source must be retained")
        observed: dict[int, int] = {}
        for public_address in sorted(SELF_TEST_TO_PUBLIC.values()):
            device = self.solenoids[public_address]
            self_test_aliases = [
                alias["value"]
                for alias in device["aliases"]
                if alias.get("namespace") == "manual.self-test"
            ]
            self.assertEqual(1, len(self_test_aliases), public_address)
            printed_number = int(self_test_aliases[0])
            self.assertNotIn(printed_number, observed)
            observed[printed_number] = public_address
            self.assertTrue(set(device["provenance"]["source_refs"]) & runtime_sources, public_address)
        self.assertEqual(SELF_TEST_TO_PUBLIC, observed)
        self.assertTrue(all(printed != public for printed, public in observed.items()))
        for public_address in SOLENOIDS - set(SELF_TEST_TO_PUBLIC.values()):
            self.assertEqual(
                [],
                [alias for alias in self.solenoids[public_address]["aliases"] if alias.get("namespace") == "manual.self-test"],
                public_address,
            )

    def test_excerpts_are_pinned_to_their_retained_bytes(self) -> None:
        checked = 0
        for source in self.definition["sources"]:
            for excerpt in source.get("excerpts", []):
                path = ROOT / excerpt["path"]
                self.assertTrue(path.is_file(), excerpt["path"])
                self.assertEqual(excerpt["sha256"], file_sha256(path), excerpt["id"])
                if "image" in excerpt:
                    image = ROOT / excerpt["image"]
                    self.assertTrue(image.is_file(), excerpt["image"])
                    self.assertEqual(excerpt["image_sha256"], file_sha256(image), excerpt["id"])
                checked += 1
        self.assertGreater(checked, 0)

    def test_seed_outputs_report_and_external_evidence_contract(self) -> None:
        self.assertEqual(canonical_bytes(self.definition_seed), curator.DEFINITION_PATH.read_bytes())
        self.assertEqual((ROOT / "tools" / "seeds" / "bally" / "viking-1979-knowledge.md").read_bytes(), self.knowledge)
        report = load_json(curator.REPORT_JSON_PATH)
        self.assertEqual("pinmame-spatial-blockers", report["format"])
        self.assertEqual(MACHINE_ID, report["machine_id"])
        self.assertEqual(hashlib.sha256(canonical_bytes(self.definition)).hexdigest(), report["definition_sha256"])
        self.assertEqual(self.spatial_seed["projection_disclosures"], report["projection_disclosures"])
        self.assertEqual(self.spatial_seed["unresolved"], report["unresolved"])
        self.assertEqual(self.spatial_seed["evidence_artifacts"], report["evidence_artifacts"])
        self.assertEqual(
            hashlib.sha256(canonical_bytes(self.spatial_seed)).hexdigest(),
            report["coordinate_evidence"]["spatial_seed_sha256"],
        )
        expected_hashes = {source["id"]: source["sha256"] for source in self.definition["sources"] if "sha256" in source}
        self.assertEqual(expected_hashes, report["source_hashes"])
        self.assertTrue(any(
            artifact["root"] == "vpx_sources" and artifact["path"].startswith("bally/viking-1979/extracted")
            for artifact in self.spatial_seed["evidence_artifacts"]
        ))
        markdown = curator.REPORT_MD_PATH.read_text(encoding="utf-8")
        for blocker in self.spatial_seed["unresolved"]:
            self.assertIn(blocker, markdown)

    def test_optional_external_source_pins_when_all_roots_are_configured(self) -> None:
        required_roots = {artifact["root"] for artifact in self.spatial_seed["evidence_artifacts"]}
        missing = [EXTERNAL_ENVIRONMENT[root] for root in required_roots if not os.environ.get(EXTERNAL_ENVIRONMENT[root])]
        if missing:
            self.skipTest("optional external evidence roots are not configured: " + ", ".join(sorted(missing)))
        for artifact in self.spatial_seed["evidence_artifacts"]:
            root = Path(os.environ[EXTERNAL_ENVIRONMENT[artifact["root"]]])
            path = root.joinpath(*Path(artifact["path"]).parts)
            self.assertTrue(path.is_file(), str(path))
            self.assertEqual(artifact["sha256"], file_sha256(path), artifact["path"])

    def test_no_stale_stub_claims_a_viking_driver(self) -> None:
        for path in (ROOT / "machines" / "stubs").rglob("*.json"):
            definition = load_json(path)
            self.assertFalse(DRIVERS & {driver["id"] for driver in definition.get("drivers", [])}, path)

    def test_curator_is_deterministic_and_check_refuses_drift_without_writes(self) -> None:
        committed_check = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools" / "curate_viking.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, committed_check.returncode, committed_check.stderr)
        working_root = resolve_working_root(ROOT)
        with tempfile.TemporaryDirectory(dir=working_root, prefix="viking-curator-") as temporary:
            base = Path(temporary)
            targets = {
                "definition": base / "definition.json",
                "knowledge": base / "knowledge.md",
                "report_json": base / "report.json",
                "report_md": base / "report.md",
            }
            marker = base / "unrelated.txt"
            marker.write_bytes(b"preserve me")
            command = [
                sys.executable, "-B", str(ROOT / "tools" / "curate_viking.py"),
                "--definition", str(targets["definition"]),
                "--knowledge", str(targets["knowledge"]),
                "--report-json", str(targets["report_json"]),
                "--report-md", str(targets["report_md"]),
            ]
            regenerated = subprocess.run(command + ["--regenerate"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, regenerated.returncode, regenerated.stderr)
            self.assertEqual(b"preserve me", marker.read_bytes())
            before_check = {name: path.read_bytes() for name, path in targets.items()}
            checked = subprocess.run(command + ["--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, checked.returncode, checked.stderr)
            self.assertEqual(before_check, {name: path.read_bytes() for name, path in targets.items()})
            targets["definition"].write_bytes(before_check["definition"] + b" ")
            drifted = subprocess.run(command + ["--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(0, drifted.returncode)
            self.assertIn("canonical content mismatch", drifted.stderr)
            self.assertEqual(before_check["definition"] + b" ", targets["definition"].read_bytes())

    def test_regeneration_refuses_an_author_ready_twin_without_touching_it(self) -> None:
        working_root = resolve_working_root(ROOT)
        with tempfile.TemporaryDirectory(dir=working_root, prefix="viking-author-ready-") as temporary:
            base = Path(temporary)
            author_ready = base / "viking-1979.json"
            author_ready.write_bytes(b"author-ready artifact")
            outputs = ((base / "definition.json", b"definition"),)
            with mock.patch.object(curator, "AUTHOR_READY_PATH", author_ready):
                with self.assertRaisesRegex(curator.CuratorError, "author-ready"):
                    curator.write_artifacts(outputs)
            self.assertEqual(b"author-ready artifact", author_ready.read_bytes())
            alternate = base / "custom-target.json"
            alternate.write_text(json.dumps({"format": "pinmame-machine-definition", "coverage": {"status": "author_ready"}}), encoding="utf-8")
            before = alternate.read_bytes()
            with self.assertRaisesRegex(curator.CuratorError, "author-ready"):
                curator.write_artifacts(((alternate, b"replacement"),))
            self.assertEqual(before, alternate.read_bytes())

    def test_physical_lamp_fanouts_and_script_defects_remain_explicit(self) -> None:
        shoot_again = self.lamps[11]
        self.assertEqual(2, shoot_again["physical"]["quantity"])
        self.assertEqual("A5J1-26 and A5J2-21", shoot_again["wiring"]["drive_connection"])
        self.assertEqual(1, len(shoot_again["spatial"]["placements"]))
        self.assertIn("backglass", shoot_again["physical"]["notes"])
        arrow = self.lamps[26]
        objects = {item["name"]: item for item in self.spatial_seed["objects"]}
        self.assertEqual(
            {(objects[name]["x"], objects[name]["y"]) for name in ("L26", "L10a")},
            {(point["x"], point["y"]) for point in arrow["spatial"]["placements"]},
        )
        self.assertEqual(1, len(self.lamps[10]["spatial"]["placements"]))
        self.assertNotIn("quantity", arrow["physical"])
        self.assertEqual("cabinet_or_service", self.lamps[59]["spatial"]["reason"])
        self.assertIn("empty", self.solenoids[3]["physical"]["notes"])
        self.assertEqual("virtual", self.solenoids[45]["kind"])
        self.assertEqual("virtual", self.solenoids[47]["kind"])
        self.assertEqual("used", self.solenoids[45]["availability"])
        self.assertEqual("used", self.solenoids[47]["availability"])

    def test_geometry_normalization_and_coarse_drawing_projection(self) -> None:
        bounds = self.spatial_seed["bounds"]
        for item in self.spatial_seed["objects"]:
            self.assertEqual(round((item["raw_x"] - bounds["left"]) / (bounds["right"] - bounds["left"]), 6), item["x"], item["name"])
            self.assertEqual(round((item["raw_y"] - bounds["top"]) / (bounds["bottom"] - bounds["top"]), 6), item["y"], item["name"])
        drawing = self.spatial_seed["manual_measurements"]["rebound33"]
        controls = drawing["controls"]
        self.assertGreaterEqual(len(controls), 4)
        self.assertGreater(max(c["normalized_y"] for c in controls) - min(c["normalized_y"] for c in controls), 0.5)
        def fitted(pixel: str, normalized: str, point: int) -> float:
            xs = [c[pixel] for c in controls]
            ys = [c[normalized] for c in controls]
            mean_x, mean_y = sum(xs) / len(xs), sum(ys) / len(ys)
            slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum((x - mean_x) ** 2 for x in xs)
            return round(mean_y + slope * (point - mean_x), 2)
        point = self.switches[33]["spatial"]["placements"][0]
        self.assertEqual(fitted("pixel_x", "normalized_x", drawing["switch33_pixels"][0]), point["x"])
        self.assertEqual(fitted("pixel_y", "normalized_y", drawing["switch33_pixels"][1]), point["y"])
        self.assertEqual("observed", self.switches[33]["spatial"]["status"])
        self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
        self.assertIn("socket", " ".join(self.spatial_seed["unresolved"]))
        self.assertNotIn("\ufffd", self.knowledge.decode("utf-8"))

    def test_guards_reject_wrong_release_year_unknown_sources_and_excerpt_drift(self) -> None:
        for mutation in (
            lambda s: s.pop("extraction_inventory"),
            lambda s: s["extraction_inventory"].update(file_count=0),
        ):
            changed_spatial = json.loads(json.dumps(self.spatial_seed))
            mutation(changed_spatial)
            with self.assertRaises(curator.CuratorError):
                curator._validate_spatial_seed(changed_spatial)
        for mutation, message in (
            (lambda d: d["machine"].update(year=1979), "physical release year"),
            (lambda d: d["inputs"][0]["provenance"].update(source_refs=["missing.source"]), "unknown source"),
            (lambda d: next(s for s in d["sources"] if s.get("excerpts"))["excerpts"][0].update(sha256="0" * 64), "hash mismatch"),
        ):
            changed = json.loads(json.dumps(self.definition))
            mutation(changed)
            with self.subTest(message=message), self.assertRaisesRegex(curator.CuratorError, message):
                curator._validate_definition(changed)

    def test_optional_extraction_manifest_and_coordinates_are_recomputed(self) -> None:
        configured = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        if not configured:
            self.skipTest("optional retained VPX root is not configured")
        extracted = Path(configured) / "bally" / "viking-1979" / "extracted"
        self.assertEqual(self.spatial_seed["extraction_manifest_sha256"], manifest_tool.check_manifest(extracted, "viking"))
        from pinmame_game_defs.spatial import _item_point
        for item in self.spatial_seed["objects"]:
            document = load_json(extracted / item["path"])
            item_type, content = next(iter(document.items()))
            x, y, method = _item_point(item_type, content)
            self.assertEqual((x, y, method), (item["raw_x"], item["raw_y"], item["center_method"]), item["name"])
        script = (extracted / "script.vbs").read_text(encoding="utf-8")
        for coil in (3, 4, 5):
            self.assertRegex(script, rf'(?mi)^\s*SolCallback\({coil}\)\s*=\s*""')
        self.assertNotRegex(script, r'(?mi)^\s*Sub\s+sw33_(?:Hit|UnHit)\b')

    def test_optional_runtime_observations_are_derived_from_raw_events(self) -> None:
        configured = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not configured:
            self.skipTest("optional retained runtime root is not configured")
        folder = Path(configured) / MACHINE_ID / "harness"
        summary = load_json(ROOT / "evidence" / "runtime" / "by35" / "viking-1979-harness.json")
        self.assertEqual(summary["source"]["sha256"], manifest_tool.check_manifest(folder, "viking"))
        glyphs = {0: " ", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 7: "7", 127: "8", 111: "9"}
        def number(event: dict) -> str:
            return "".join(glyphs.get(segment & 127, "?") for segment in event.get("segments", [])).strip()
        for raw in summary["runtime"]["raw_runs"]:
            run = load_json(folder / (raw["name"] + ".json"))
            self.assertIsNone(run["failure"])
            self.assertEqual(raw["sha256"], file_sha256(folder / (raw["name"] + ".json")))
            self.assertEqual(raw["action_count"], len(run["steps"]))
            self.assertEqual(raw["snapshot_count"], len(run["snapshots"]))
            self.assertEqual(raw["scenario_sha256"], file_sha256(ROOT / raw["scenario_path"]))
            self.assertEqual(summary["runtime"]["emulator"]["sha256"], run["library_sha256"])
            if raw["name"] not in ("solenoid-test", "vikingb-solenoid-test"):
                continue
            readings = {}
            entered = next(s["time_s"] for s in run["snapshots"] if s["label"] == "self test: solenoid cycle") - 0.4
            for event in run["events"]:
                if event["event"] != "solenoid" or not event["state"] or event["time_s"] < entered:
                    continue
                candidates = [
                    display for display in run["events"]
                    if display["event"] == "display" and display.get("index") == 0
                    and event["time_s"] - 0.05 <= display["time_s"] <= event["time_s"] + 0.45
                    and len(number(display)) == 2 and number(display).isdecimal()
                ]
                for display in candidates:
                    readings.setdefault(int(number(display)), set()).add(event["number"])
            self.assertEqual({test: {public} for test, public in SELF_TEST_TO_PUBLIC.items()}, readings, raw["name"])
        gameplay = load_json(folder / "gameplay.json")
        expected = {"playfield switch 35": 15, "playfield switch 36": 14, "playfield switch 37": 13,
                    "playfield switch 38": 12, "playfield switch 39": 11, "playfield switch 40": 10,
                    "unlit two-way saucer occupied": 9, "bonus-collect two-way saucer occupied": 8,
                    "top saucer occupied": 17, "right bank bottom target17 down": 2}
        for label, public in expected.items():
            step = next(s for s in gameplay["steps"] if s["label"] == label)
            active = {output["number"] for output in step["transitions"]["solenoids"] if any(output["states"])}
            self.assertIn(public, active, label)


if __name__ == "__main__":
    unittest.main()
