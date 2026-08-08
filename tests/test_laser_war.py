from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "data-east" / "laser-war-1987.json"
SEED_PATH = ROOT / "tools" / "seeds" / "data-east" / "laser-war-1987.json"
MANIFEST_PATH = ROOT / "tools" / "seeds" / "data-east" / "laser-war-1987-extraction-manifest.json"
REPORT_PATH = ROOT / "reports" / "spatial" / "data-east" / "laser-war-1987.json"
REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "data-east" / "laser-war-1987.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "data-east" / "laser-war-1987.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.laser-war.1987"
OWN_DRIVERS = {"lwar_a81", "lwar_a83", "lwar_e90"}


MANUAL_SWITCHES = [
    "Plumb Tilt", "Ball Roll Tilt", "Start Button", "Right Coin", "Center Coin", "Left Coin", "Slam Tilt", None,
    "Playfield Tilt", "Ball Trough 3", "Ball Trough 2", "Ball Trough 1", "Outhole", "Sling Shot Right", "Sling Shot Left", None,
    "Laser Kick", "Left Flipper Return Lane", "Right Flipper Return Lane", "Right Outlane", "10 Point Rubber Right (2 Switches)",
    "Red Target (Left)", "Red Target (Center)", "Red Target (Right)", "Red Eject", "Star Red", "Red Spinner", None, "Ramp",
    "Yellow Target (Left)", "Yellow Target Spot (Center)", "Yellow Target (Right)", "Yellow Eject", "Yellow Star",
    "Blue Target (Left)", "Blue Target (Center)", "Blue Target (Right)", "Blue Eject", "Star Blue", "W", "A", "R",
    "Pop Bumper Red", "Pop Bumper Yellow", "Pop Bumper Blue", "Right E.O.S.", "Left E.O.S.",
    "Star Red (Upper Right)", "Star Yellow (Upper Right)", "Star Blue (Upper Right)", "Yellow Spinner", "Shooter Lane",
    None, None, None, None, None, None, None, None, None, None, None, None,
]

MANUAL_LAMPS = [
    "Ball in Play", "Match", "Blast Again", "W", "A", "R", "Ramp Multiplier", "Return to Base",
    "Cannon Red", "Cannon Yellow", "Cannon Blue", "Ramp Green Shield", "Ramp Orange Arrow", "Ramp Amber Arrow", "Ramp Clear Arrow",
    "Red Target (Left)", "Red Target (Center)", "Red Target (Right)", "Hot Dog Red", "Lock Eject Red",
    "Red Eject Arrow Clear", "Red Eject Arrow Amber", "Red Eject Arrow Orange", "Yellow Target (Left)", "Yellow Target (Center)",
    "Yellow Target (Right)", "Hot Dog Yellow", "Eject Lock Yellow", "Yellow Eject Arrow Clear", "Yellow Eject Arrow Amber",
    "Yellow Eject Arrow Orange", "Blue Target (Left)", "Blue Target (Center)", "Blue Target (Right)", "Hot Dog Blue", "Eject Blue",
    "Blue Eject Arrow Clear", "Blue Eject Arrow Amber", "Blue Eject Arrow Orange", "Left Outlane",
    "Flipper Return Lanes (Left & Right)", "Bonus Holds", "2 X", "3 X", "4 X", "5 X", "Laser Kick", "Right Outlane",
    "Ion Cannon (Tip)", "Bonus 1K Red", "Bonus 2K Red", "Bonus 4K Red", "Bonus 8K Red", "Bonus 16K Red",
    "Bonus 1K Yellow", "Bonus 2K Yellow", "Bonus 4K Yellow", "Bonus 8K Yellow", "Bonus 16K Yellow",
    "Bonus 1K Blue", "Bonus 2K Blue", "Bonus 4K Blue", "Bonus 8K Blue", "Bonus 16K Blue",
]

MANUAL_COILS = {
    1: "Explosion", 2: "Red Hot Dog", 3: "Yellow Hot Dog", 4: "Blue Hot Dog", 5: "Ion Cannon",
    6: "Mars Yellow", 7: "Mars Red", 8: "Mars Blue", 9: "Ball Trough Eject", 10: "L/R Power Relay",
    11: "G.I. Relay", 12: "Red Eject", 13: "Yellow Eject", 14: "Blue Eject", 15: "Laser Kick Relay",
    16: "Outhole", 25: "Ramp Multiplier", 26: "Green Shield", 27: "Warriors (Back Glass)",
    28: "Laser Wire (Back Glass)", 29: "Knocker",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class LaserWarDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
        cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
        cls.sources = {item["id"]: item for item in cls.definition["sources"]}

    def test_identity_generation_and_driver_tree(self) -> None:
        self.assertEqual("data-east.laser-war.1987", self.definition["machine"]["id"])
        self.assertEqual({"platform": "pinmame.system-11", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True},
                         self.definition["controller"])
        self.assertEqual(OWN_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
        root = next(driver for driver in self.definition["drivers"] if driver["id"] == "lwar_a83")
        self.assertNotIn("clone_of", root)
        self.assertEqual({"lwar_a81", "lwar_e90"}, {driver["id"] for driver in self.definition["drivers"] if driver.get("clone_of") == "lwar_a83"})
        self.assertTrue(all(driver["year"] == "1987" and driver["manufacturer"] == "Data East" for driver in self.definition["drivers"]))
        self.assertEqual({"width": 964.0, "height": 2162.0, "units": "vpx", "provenance": {"status": "validated", "source_refs": ["vpx-table.laser-war-vr-2-0"]}},
                         self.definition["machine"]["playfield"])

    def test_upstream_system_11_profile_covers_exact_laser_war_subsets(self) -> None:
        profile = load_json(CONTROLLER_PATH)
        self.assertEqual("pinmame.system-11", profile["id"])
        groups = {group["id"]: group for group in profile["groups"]}

        def allowed(group_id: str, address: int) -> bool:
            for rule in groups[group_id]["address_rules"]:
                if address in rule.get("values", []):
                    return True
                if rule.get("minimum", address + 1) <= address <= rule.get("maximum", address - 1):
                    return True
            return False

        for address in (-7, -6, 1, 64):
            self.assertTrue(allowed("pinmame.input.switch", address), address)
        for address in range(1, 51):
            self.assertTrue(allowed("pinmame.output.solenoid", address), address)
        self.assertTrue(allowed("pinmame.input.dip", 0))
        self.assertTrue(all(allowed("pinmame.output.lamp", address) for address in range(1, 65)))
        self.assertEqual({-7, -6}, {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["device"] < 0})
        self.assertEqual(set(range(1, 51)), {item["binding"]["device"] for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"})

    def test_coverage_is_fail_closed_and_names_every_missing_dimension(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"], coverage["missing"])
        self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
        self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])

    def test_switch_namespace_is_complete_and_matches_independent_fixture(self) -> None:
        matrix = {item["binding"]["device"]: item for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] > 0}
        self.assertEqual(set(range(1, 65)), set(matrix))
        for address, printed in enumerate(MANUAL_SWITCHES, start=1):
            item = matrix[address]
            self.assertEqual("unused" if printed is None else "used", item["availability"], address)
            if printed is None:
                self.assertEqual(f"Unused Switch {address}", item["label"])
            elif address == 17:
                self.assertEqual("Laser Kick / Kickback", item["label"])
            else:
                self.assertEqual(printed, item["label"], address)
        self.assertEqual({-7, -6}, {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] < 0})
        self.assertEqual(2, matrix[21]["physical"]["quantity"])
        self.assertTrue(all(matrix[address].get("initial_active") is True for address in (10, 11, 12)))

    def test_lamp_namespace_is_complete_and_matches_independent_fixture(self) -> None:
        lamps = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
        self.assertEqual(set(range(1, 65)), set(lamps))
        self.assertEqual(MANUAL_LAMPS, [lamps[address]["label"] for address in range(1, 65)])
        self.assertTrue(all(item["availability"] == "used" for item in lamps.values()))
        self.assertEqual(2, lamps[41]["physical"]["quantity"])
        self.assertNotIn("spatial", lamps[8])
        self.assertNotIn("spatial", lamps[49])

    def test_solenoid_namespace_is_exactly_public_1_through_50(self) -> None:
        solenoids = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        self.assertEqual(set(range(1, 51)), set(solenoids))
        for address, label in MANUAL_COILS.items():
            self.assertEqual(label, solenoids[address]["label"], address)
        self.assertEqual("gi", solenoids[11]["kind"])
        self.assertEqual({30, 31, 32}, {address for address in (25, 26, 27, 28, 29, 30, 31, 32) if solenoids[address]["availability"] == "unused"})
        self.assertTrue(all(solenoids[address]["availability"] == "unknown" for address in range(17, 23)))
        self.assertTrue(all("device mapping unresolved" in solenoids[address]["label"] for address in range(17, 23)))
        self.assertTrue(all(solenoids[address]["availability"] == "unused" for address in range(33, 45)))
        self.assertEqual("flasher", solenoids[6]["kind"])
        self.assertNotIn("part_number", solenoids[6]["physical"])
        self.assertIn("COIL: 23-800", solenoids[6]["physical"]["notes"])
        self.assertEqual(
            {("manual.coil-id-chart", "2L"), ("manual.coil-location", "1R")},
            {(alias["namespace"], alias["value"]) for alias in solenoids[25]["aliases"] if alias["namespace"].startswith("manual.coil-")},
        )

    def test_display_topology_matches_de_disp_alpha_1(self) -> None:
        layout = [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]]
        self.assertEqual([(0, 1, 7), (1, 9, 7), (2, 21, 7), (3, 29, 7), (4, 20, 1), (5, 28, 1), (6, 0, 1), (7, 8, 1)], layout)
        self.assertTrue(all(item["kind"] == "segment" for item in self.definition["displays"]))
        self.assertTrue(all(item["spatial"]["status"] == "not_applicable" and item["spatial"]["reason"] == "cabinet_or_service" for item in self.definition["displays"]))

    def test_mechanism_topology_comes_from_runtime_causality(self) -> None:
        mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
        trough = mechanisms["mechanism.ball-trough"]
        self.assertEqual(["coil.driver-9"], trough["actuators"])
        self.assertEqual(["switch.matrix-10", "switch.matrix-11", "switch.matrix-12"], trough["sensors"])
        self.assertEqual(["coil.driver-16"], mechanisms["mechanism.outhole"]["actuators"])
        self.assertEqual(["switch.matrix-13"], mechanisms["mechanism.outhole"]["sensors"])
        self.assertEqual(["coil.driver-12"], mechanisms["mechanism.red-eject"]["actuators"])
        self.assertEqual(["coil.driver-13"], mechanisms["mechanism.yellow-eject"]["actuators"])
        self.assertEqual(["coil.driver-14"], mechanisms["mechanism.blue-eject"]["actuators"])
        for identifier in ("mechanism.left-slingshot", "mechanism.right-slingshot", "mechanism.red-pop-bumper", "mechanism.yellow-pop-bumper", "mechanism.blue-pop-bumper"):
            self.assertEqual([], mechanisms[identifier]["actuators"], "labels/proximity must not invent a special-coil mapping")
            self.assertEqual("unknown", mechanisms[identifier]["provenance"]["status"])

    def test_relay_mux_relationships_cover_the_whole_right_bank(self) -> None:
        relationships = self.definition["relationships"]
        self.assertEqual(8, len(relationships))
        self.assertEqual({f"coil.driver-{address}" for address in range(25, 33)}, {item["destination"] for item in relationships})
        self.assertTrue(all(item["source"] == "coil.driver-10" and item["kind"] == "relay_gated" for item in relationships))

    def test_conflicts_are_preserved_not_silently_resolved(self) -> None:
        self.assertEqual({
            "conflict.switch-17-name", "conflict.right-flipper-eos-runtime",
            "conflict.left-flipper-eos-runtime", "conflict.lamp-8-runtime-binding",
            "conflict.ramp-multiplier-printed-coil-label", "conflict.mars-yellow-printed-device-type",
        }, {item["id"] for item in self.definition["conflicts"]})
        self.assertEqual("conflicted", self.inputs["switch.matrix-46"]["provenance"]["status"])
        self.assertEqual("conflicted", self.inputs["switch.matrix-47"]["provenance"]["status"])
        self.assertEqual("conflicted", self.outputs["lamp.matrix-8"]["provenance"]["status"])

    def test_spatial_records_use_normalized_bounds_and_exclude_helpers(self) -> None:
        report = load_json(REPORT_PATH)
        self.assertEqual("pinmame-spatial-blockers", report["format"])
        self.assertEqual({"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0}, report["coordinate_system"]["raw_bounds"])
        placements = []
        for collection in (self.definition["inputs"], self.definition["outputs"]):
            for item in collection:
                placements.extend(item.get("spatial", {}).get("placements", []))
        self.assertTrue(placements)
        self.assertTrue(all(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1 for item in placements))
        self.assertEqual(2, len(self.inputs["switch.matrix-21"]["spatial"]["placements"]))
        self.assertEqual(2, len(self.outputs["lamp.matrix-41"]["spatial"]["placements"]))
        report_text = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("suffix-a glow/lightmap", report_text)
        self.assertNotIn('"id": "lamp.matrix-9.placement-', DEFINITION_PATH.read_text(encoding="utf-8"))
        markdown = REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
        self.assertIn("# Data East Laser War (1987) spatial audit", markdown)
        self.assertIn("## Explicit projection classes", markdown)
        self.assertIn("Keep partial", markdown)

    def test_evidence_excerpts_exist_and_hashes_match_source_records(self) -> None:
        manual = self.sources["manual.data-east.laser-war.1987"]
        self.assertEqual(3, len(manual["excerpts"]))
        for excerpt in manual["excerpts"]:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertEqual("manual", excerpt["method"])
            self.assertTrue(excerpt["reviewed"])
            self.assertIn("Human transcription", path.read_text(encoding="utf-8"))
        self.assertIn("PDF text layer is OCR", (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8"))
        switch_text = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
        lamp_text = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
        coil_text = (EXCERPT_ROOT / "coil-chart.md").read_text(encoding="utf-8")
        self.assertIn("PDF page 19; printed page 17", switch_text)
        self.assertIn('| 4 | YEL-BRN | RED-YEL | "W" |', lamp_text)
        self.assertIn("Flipper Return Lanes (Left&Right)", lamp_text)
        self.assertIn("FLIPPER RETURN LANES (LEFT AND RIGHT)", lamp_text)
        id_chart_text = coil_text.split("## Playfield Coil Location Illustration list", 1)[0]
        self.assertEqual(2, id_chart_text.count("| 2L |"))
        self.assertIn("| 6L | MARS YELLOW | VIO-BLU | BRN | Q 41 | COIL: 23-800 |", coil_text)
        self.assertIn("WARRIIRS (Back Glass)", coil_text)
        self.assertIn("## Reconciliation to PinMAME public addresses and semantic kinds", coil_text)
        self.assertIn("`1R` is public address 25", coil_text)
        manifest_source = self.sources["vpx-extraction.laser-war-vr-2-0"]
        self.assertEqual(manifest_source["sha256"], sha256(MANIFEST_PATH))

    def test_manifest_canonical_digest_and_shape(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(2927, manifest["file_count"])
        self.assertEqual(163816471, manifest["total_bytes"])
        self.assertEqual(manifest["file_count"], len(manifest["files"]))
        self.assertEqual(len({entry["path"] for entry in manifest["files"]}), manifest["file_count"])
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("3bfd3b8d21bdeeca6d6a83daf60d7694a4052bff881cbeae6409f6b3a44031b0", manifest["manifest_sha256"])
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())

    def test_catalog_reassigns_all_three_drivers_and_stale_stub_is_absent(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        records = {item["id"]: item for item in catalog["drivers"]}
        for driver_id in OWN_DRIVERS:
            self.assertEqual("data-east.laser-war.1987", records[driver_id]["machine_id"])
            self.assertEqual("machines/partial/data-east/laser-war-1987.json", records[driver_id]["definition"])
            self.assertEqual("partial", records[driver_id]["coverage_status"])
        self.assertFalse((ROOT / "machines" / "stubs" / "lwar_a83.json").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "lwar_a83.md").exists())
        self.assertFalse((ROOT / "machines" / "stubs" / "lwar_a83.json.disabled").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "lwar_a83.md.disabled").exists())

    def test_dynamic_contamination_guard_uses_the_catalog_not_a_hand_list(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        texts = [DEFINITION_PATH.read_text(encoding="utf-8"), SEED_PATH.read_text(encoding="utf-8"), REPORT_PATH.read_text(encoding="utf-8"), REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")]
        artifact_text = "\n".join(texts).casefold()
        artifact_identifier_tokens = set(re.findall(r"[a-z0-9_]+", artifact_text))
        artifact_machine_tokens = set(re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)+", artifact_text))
        evidence_tokens = set(re.findall(r"[a-z0-9_]+", "\n".join(path.read_text(encoding="utf-8").casefold() for path in EXCERPT_ROOT.glob("*.md"))))

        other_driver_ids = {item["id"].casefold() for item in catalog["drivers"] if item["id"] not in OWN_DRIVERS}
        unexplained_driver_hits = (artifact_identifier_tokens & other_driver_ids) - evidence_tokens
        self.assertEqual(set(), unexplained_driver_hits, "another short name leaked without appearing in Laser War's own printed evidence")
        other_machine_ids = {item["id"].casefold() for item in catalog["machines"] if item["id"] != "data-east.laser-war.1987"}
        self.assertEqual(set(), artifact_machine_tokens & other_machine_ids)

        generation_constants = set(re.findall(r"\bGEN_[A-Z0-9_]+\b", "\n".join(texts)))
        self.assertLessEqual(generation_constants, {"GEN_DE"})
        hardware_tokens = set(re.findall(r"\b0x[0-9a-f]+\b", artifact_text))
        self.assertEqual({"0x1000"}, hardware_tokens)

        other_table_fingerprints = set()
        for machine in catalog["machines"]:
            if machine["id"] == "data-east.laser-war.1987":
                continue
            definition_path = ROOT / machine["definition"]
            if not definition_path.is_file():
                continue
            other_definition = load_json(definition_path)
            for source in other_definition.get("sources", []):
                if source.get("kind") != "vpx_table":
                    continue
                for key in ("id", "original_filename", "source_id", "sha256"):
                    value = source.get(key)
                    if isinstance(value, str) and len(value) >= 8:
                        other_table_fingerprints.add(value.casefold())
        self.assertEqual(set(), {value for value in other_table_fingerprints if value in artifact_text})
        own_table = self.sources["vpx-table.laser-war-vr-2-0"]
        self.assertEqual("Laser War (Data East 1987) w VR Room v2.0.vpx", own_table["original_filename"])
        self.assertEqual("43b88ba675a1e8430d822930100c386f5cf63c2e18fa048b339cf54eb4fed586", own_table["sha256"])

    def test_seed_is_byte_identical_and_knowledge_names_the_damage(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("Pages 25-34 are missing their right halves", knowledge)
        self.assertIn("circuits 17-22", knowledge)
        self.assertIn("42-page ClearScan/OCR scan", knowledge)
        self.assertIn("fresh 400 dpi Poppler renders", knowledge)
        self.assertIn("profile is reused unchanged", knowledge)


class LaserWarCuratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "tools"))
        import curate_laser_war
        cls.curator = curate_laser_war

    def test_check_is_clean_and_crlf_tolerant_but_not_reformat_tolerant(self) -> None:
        self.curator._check(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            target_root = Path(scratch)
            for path, _payload in self.curator._artifacts(ROOT):
                relative = path.relative_to(ROOT)
                target = target_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
                target.write_bytes(data)
            self.curator._check(target_root)
            definition = target_root / DEFINITION_PATH.relative_to(ROOT)
            definition.write_text(json.dumps(load_json(definition), indent=4, sort_keys=True) + "\n", encoding="utf-8", newline="")
            with self.assertRaises(RuntimeError):
                self.curator._check(target_root)

    def test_regenerator_refuses_existing_author_ready_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            author_ready = root / "machines" / "author-ready" / "data-east" / "laser-war-1987.json"
            author_ready.parent.mkdir(parents=True)
            author_ready.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                self.curator._write(root)


class LaserWarExternalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vpx_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) if os.environ.get("PINMAME_VPX_SOURCES_ROOT") else None
        cls.manual_anchor = Path(os.environ["PINMAME_MANUALS_ROOT"]) if os.environ.get("PINMAME_MANUALS_ROOT") else None

    def test_exact_retained_table_and_script_hashes(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        base = self.vpx_root / "data-east" / "laser-war-1987"
        self.assertEqual("43b88ba675a1e8430d822930100c386f5cf63c2e18fa048b339cf54eb4fed586", sha256(base / "Laser War (Data East 1987) w VR Room v2.0.vpx"))
        self.assertEqual("18c2679106173f13dc4a2b38f3d41e76c6be9d86f0637be04a6c6b8ec749d163", sha256(base / "vpxtool-extract" / "script.vbs"))

    def test_extraction_manifest_recomputes_every_retained_file(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.vpx_root / "data-east" / "laser-war-1987" / "vpxtool-extract"
        manifest = load_json(MANIFEST_PATH)
        actual = [path.relative_to(extraction).as_posix() for path in sorted(path for path in extraction.rglob("*") if path.is_file())]
        self.assertEqual(actual, [entry["path"] for entry in manifest["files"]])
        for entry in manifest["files"]:
            path = extraction / entry["path"]
            self.assertEqual(entry["bytes"], path.stat().st_size, entry["path"])
            self.assertEqual(entry["sha256"], sha256(path), entry["path"])

    def test_exact_manual_hash_via_supplied_manual_root_anchor(self) -> None:
        if self.manual_anchor is None:
            self.skipTest("retained manuals are not available")
        candidates = [
            self.manual_anchor / "by-machine" / "data-east.laser-war.1987" / "contributor-supplied" / "laser-war-1987-instruction-manual.pdf",
            self.manual_anchor.parent / "manual-cache" / "by-machine" / "data-east.laser-war.1987" / "contributor-supplied" / "laser-war-1987-instruction-manual.pdf",
        ]
        manual = next((path for path in candidates if path.is_file()), None)
        self.assertIsNotNone(manual, candidates)
        self.assertEqual(12_035_989, manual.stat().st_size)
        self.assertEqual("f6c6a09a6c9be42d8851790a5b40060fef7a4dbd6e452e1aa89af4765783a3db", sha256(manual))


if __name__ == "__main__":
    unittest.main()
