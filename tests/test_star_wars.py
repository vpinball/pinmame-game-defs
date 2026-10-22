"""Star Wars placements stay observed and reproduce from the retained VPW table."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_star_wars_geometry as geometry
import curate_star_wars_spatial as curator
from build_external_evidence_manifest import build_manifest, canonical_bytes, sha256_file


class StarWarsSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = json.loads(curator.DEFINITION.read_text(encoding="utf-8"))
        cls.report = json.loads(curator.REPORT.read_text(encoding="utf-8"))

    def test_valid_partial_and_no_unverified_validation_claim(self):
        self.assertEqual([], validate_machine(self.machine, ROOT))
        self.assertEqual("partial", self.machine["coverage"]["status"])
        self.assertEqual("observed", self.machine["coverage"]["dimensions"]["spatial_placement"])
        self.assertIn("spatial_placement", self.machine["coverage"]["missing"])
        self.assertIn("unresolved_conflicts", self.machine["coverage"]["missing"])
        conflict = next(c for c in self.machine["conflicts"] if c["id"] == "conflict.star-wars-flash-bank-counts")
        self.assertIn("Resolution path:", conflict["description"])
        for device in self.machine["inputs"] + self.machine["outputs"]:
            if "spatial" in device and device["spatial"]["status"] != "not_applicable":
                self.assertEqual("observed", device["spatial"]["status"])
                for placement in device["spatial"]["placements"]:
                    self.assertEqual("observed", placement["provenance"]["status"])
                    self.assertIn(curator.TABLE, placement["provenance"]["source_refs"])
                    self.assertIn(curator.SCRIPT, placement["provenance"]["source_refs"])

    def test_every_device_is_placed_or_has_an_explicit_evidence_gap(self):
        unplaced = set()
        for section in ("inputs", "outputs"):
            for device in self.machine[section]:
                binding = device["binding"]
                key = binding["device"] if section == "inputs" else (binding["group"], binding["device"])
                missing = curator.UNPLACED_INPUTS if section == "inputs" else curator.UNPLACED_OUTPUTS
                self.assertEqual(key not in missing, "spatial" in device, device["id"])
                if key in missing:
                    unplaced.add(device["id"])
        self.assertEqual(unplaced, set(self.report["unplaced_records"]))
        # In particular, a missing bulb model is not evidence of a nonphysical lamp.
        lamp48 = next(d for d in self.machine["outputs"]
                      if d["binding"] == {"group": "pinmame.output.lamp", "device": 48})
        self.assertEqual("observed", lamp48["spatial"]["status"])
        self.assertIn(curator.MANUAL, lamp48["spatial"]["placements"][0]["provenance"]["source_refs"])

    def test_coordinates_match_each_bound_object_and_never_a_flasher_sprite(self):
        for section in ("inputs", "outputs"):
            for device in self.machine[section]:
                if "spatial" not in device:
                    continue
                if device["spatial"]["status"] == "not_applicable":
                    self.assertNotEqual(
                        ("pinmame.output.solenoid", 11),
                        (device["binding"].get("group"), device["binding"]["device"]),
                    )
                    continue
                address = device["binding"]["device"]
                placements = device["spatial"]["placements"]
                if "manual" in placements[0]["id"]:
                    page = curator.MANUAL_GEOMETRY["flash_page" if address == 30 and
                        device["binding"]["group"] == "pinmame.output.solenoid" else "lamp_page"]
                    pixels = page["flashers"]["30"] if "flashers" in page else [page["lamps"][str(address)]]
                    self.assertEqual(curator.drawn_spatial(device["id"], page, pixels), device["spatial"])
                    continue
                if section == "inputs":
                    names = curator.names_of(curator.GEOMETRY["switches"], address)
                elif device["binding"]["group"] == "pinmame.output.solenoid":
                    names = (tuple(curator.GEOMETRY["gi"]) if address == 11 else
                             curator.FLASH_LIGHTS[address] if address in curator.FLASH_LIGHTS else
                             curator.names_of(curator.GEOMETRY["coils"], address))
                else:
                    names = (curator.GEOMETRY["gi"] if address == 111 else
                             curator.names_of(curator.GEOMETRY["lamps"], address))
                    if address in (49, 50, 51):
                        names = (f"l{address}",)
                self.assertEqual(len(names), len(placements))
                for name, placement in zip(names, placements):
                    obj = curator.GEOMETRY["objects"][name]
                    self.assertNotEqual("Flasher", obj["type"])
                    if placement["role"] == "emitter":
                        self.assertTrue(obj["light"]["is_bulb_light"])
                        self.assertFalse(obj["light"]["is_image_mode"])
                    self.assertEqual(obj["xy"], [placement["x"], placement["y"]])
                    self.assertEqual("playfield", placement["space"])

    def test_curator_reproduces_definition_and_report(self):
        built = curator.build()
        self.assertEqual(curator.canonical(built), curator.DEFINITION.read_bytes().replace(b"\r\n", b"\n"))
        self.assertEqual(curator.canonical(curator.report(built)), curator.REPORT.read_bytes().replace(b"\r\n", b"\n"))
        self.assertFalse(self.report["promotion"]["allowed"])
        self.assertEqual(sorted(built["coverage"]["missing"]), self.report["promotion"]["missing"])

    def test_outhole_is_at_drain_and_separate_from_trough_release(self):
        switches = {d["binding"]["device"]: d for d in self.machine["inputs"]
                    if d["binding"]["group"] == "pinmame.input.switch"}
        coils = {d["binding"]["device"]: d for d in self.machine["outputs"]
                 if d["binding"]["group"] == "pinmame.output.solenoid"}
        for device in (switches[10], coils[1]):
            self.assertEqual("Outhole", device["label"])
            placement = device["spatial"]["placements"][0]
            self.assertTrue(placement["id"].endswith("-drain"))
            self.assertAlmostEqual(493.758 / 946, placement["x"], places=6)
            self.assertAlmostEqual(2071.8584 / 2162, placement["y"], places=6)
            self.assertIn(curator.SCHEMATIC, placement["provenance"]["source_refs"])
        release = coils[2]["spatial"]["placements"][0]
        self.assertTrue(release["id"].endswith("-ballrelease"))
        self.assertGreater(release["x"], coils[1]["spatial"]["placements"][0]["x"] + 0.3)

    def test_sources_pin_only_the_verified_new_evidence(self):
        sources = {s["id"]: s for s in self.machine["sources"]}
        self.assertEqual(curator.TABLE_SHA, sources[curator.TABLE]["sha256"])
        self.assertEqual(curator.SCRIPT_SHA, sources[curator.SCRIPT]["sha256"])
        for source in (sources[curator.TABLE], sources[curator.SCRIPT]):
            self.assertEqual("NOASSERTION", source["license"])
            self.assertTrue(source["attribution"])
        self.assertFalse(any("bigus" in s or s == "manual.star-wars-1992" for s in sources))
        self.assertNotIn("supplement", self.report)

    def test_manual_evidence_and_cabinet_identification(self):
        excerpt = ROOT / "evidence/excerpts/data-east.star-wars.1992/manual-spatial.md"
        self.assertEqual(curator.EXCERPT_SHA, hashlib.sha256(excerpt.read_bytes()).hexdigest())
        for key in ("lamp_page", "flash_page"):
            page = curator.MANUAL_GEOMETRY[key]
            self.assertEqual(page["image_sha256"], sha256_file(ROOT / page["image"]))
            _, pairs = curator.drawing_fit(page)
            self.assertLess(max(curator.leave_one_out(pairs)), 0.025)
        expected = {1: "Plumb Tilt", 50: "Shift Button", 51: "Shift Down"}
        for d in self.machine["inputs"]:
            if d["binding"]["device"] in expected:
                self.assertEqual(expected[d["binding"]["device"]], d["label"])
                self.assertEqual("cabinet_or_service", d["spatial"]["reason"])
        # A corrupt fit must fail instead of quietly moving all manual placements.
        import copy
        page = copy.deepcopy(curator.MANUAL_GEOMETRY["lamp_page"])
        page["controls"]["Bumper1"] = [10000, 10000]
        with self.assertRaises(ValueError):
            curator.drawing_fit(page)

    def test_bad_candidate_coordinates_and_sprites_are_rejected(self):
        for candidate in ({"type": "Flasher", "xy": [0.5, 0.5]},
                          {"type": "Light", "xy": [-0.1, 0.5],
                           "light": {"is_bulb_light": True, "is_image_mode": False}},
                          {"type": "Light", "xy": [0.5, 0.5],
                           "light": {"is_bulb_light": True, "is_image_mode": True}}):
            with patch.dict(curator.GEOMETRY["objects"], {"bad": candidate}):
                with self.assertRaises(ValueError):
                    curator.spatial("test", "emitter", ("bad",))


class StarWarsRetainedEvidenceTests(unittest.TestCase):
    def test_retained_manuals_match_source_records(self):
        configured = os.environ.get("PINMAME_MANUALS_ROOT")
        if not configured:
            self.skipTest("PINMAME_MANUALS_ROOT is not configured")
        root = Path(configured) / "by-machine" / curator.KEY
        self.assertTrue(root.is_dir(), root)
        for name, digest in (("Star_Wars_DE_OPS.pdf", curator.MANUAL_SHA),
                             ("starwars_schematics.pdf", curator.SCHEMATIC_SHA)):
            self.assertEqual(digest, sha256_file(root / name))

    def test_complete_extraction_and_geometry_are_reproducible(self):
        configured = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        if not configured:
            self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
        root = Path(configured)
        extraction = root / curator.EXTRACTION
        self.assertTrue(extraction.is_dir(), extraction)
        table = root / curator.STEM / "tables/vpw-1.2.2-ea240a0193d6/Star Wars (Data East 1992) VPW v1.2.2.vpx"
        self.assertEqual(curator.TABLE_SHA, sha256_file(table))
        self.assertEqual(curator.SCRIPT_SHA, sha256_file(extraction / "script.vbs"))
        manifest = build_manifest(extraction, "stwr_106")
        self.assertEqual(curator.EXTRACTION_MANIFEST, hashlib.sha256(canonical_bytes(manifest) + b"\n").hexdigest())
        self.assertEqual(curator.EXTRACTION_FILES, len(manifest["files"]))
        self.assertEqual(curator.EXTRACTION_BYTES, sum(f["size"] for f in manifest["files"]))
        obj_dir = root / curator.OBJ
        pinned_obj = curator.GEOMETRY["objects"]["DeathStar"]["sha256"]
        self.assertEqual(pinned_obj, geometry.obj_sha256(obj_dir))
        self.assertEqual(curator.GEOMETRY, geometry.build(extraction, obj_dir))


if __name__ == "__main__":
    unittest.main()
