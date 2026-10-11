"""Game-specific spatial gate for Data East Star Wars (1992).

Every device carries exactly one spatial disposition, the disposition agrees with the pinned
VPW v1.2.2 geometry (flash banks 5R/7R with the pinned Bigus 3.0 geometry), the Bigus supplement
section reconciles with the two pinned geometries, the curator reproduces byte-for-byte, and the
spatial report reconciles with the definition.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_star_wars_spatial as curator

KEY = "data-east.star-wars.1992"
DEFINITION = ROOT / "machines/partial/data-east/star-wars-1992.json"
REPORT = ROOT / "reports/spatial/data-east/star-wars-1992.json"
GEOMETRY = ROOT / "tools/star_wars_geometry.json"
LOCATED_ROLE = {"switch": "sensor", "coil": "effect", "flasher": "emitter", "lamp": "emitter"}


class StarWarsSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = load_json(DEFINITION)
        cls.geometry = load_json(GEOMETRY)
        cls.report = load_json(REPORT)
        cls.inputs = {d["binding"]["device"]: d for d in cls.machine["inputs"]}
        cls.outputs = {(d["binding"]["group"], d["binding"]["device"]): d for d in cls.machine["outputs"]}

    def test_definition_validates_and_stays_partial(self):
        self.assertEqual([], validate_machine(self.machine, ROOT))
        self.assertEqual("partial", self.machine["coverage"]["status"])
        self.assertEqual("observed", self.machine["coverage"]["dimensions"]["spatial_placement"])
        self.assertIn("spatial_placement", self.machine["coverage"]["missing"])

    def test_every_device_carries_exactly_one_spatial_disposition(self):
        for device in self.machine["inputs"] + self.machine["outputs"]:
            self.assertIn("spatial", device, device["id"])
        self.assertEqual(39, sum(1 for d in self.machine["inputs"] if d["spatial"]["status"] != "not_applicable")
                         + len(curator.INPUT_NOT_APPLICABLE))
        located = [d for d in self.machine["outputs"] if d["spatial"]["status"] != "not_applicable"]
        self.assertEqual(89, len(located) + len(curator.OUTPUT_NOT_APPLICABLE))

    def test_not_applicable_dispositions_are_the_controlled_three_and_two(self):
        self.assertEqual({1, 50, 51}, {d["binding"]["device"] for d in self.machine["inputs"]
                                       if d["spatial"]["status"] == "not_applicable"})
        self.assertEqual({("pinmame.output.solenoid", 11), ("pinmame.output.lamp", 48)},
                         {(d["binding"]["group"], d["binding"]["device"]) for d in self.machine["outputs"]
                          if d["spatial"]["status"] == "not_applicable"})
        for device in self.machine["inputs"] + self.machine["outputs"]:
            if device["spatial"]["status"] == "not_applicable":
                self.assertIn(device["spatial"]["reason"],
                              {"cabinet_or_service", "internal_nonvisual"})

    def test_placements_match_the_pinned_geometry_object_for_each_address(self):
        for address, device in self.inputs.items():
            if device["spatial"]["status"] != "observed":
                continue
            names = [v.split(".", 1)[1] for v in
                     ([self.geometry["switches"][str(address)]])]
            self.assertEqual(LOCATED_ROLE["switch"], device["spatial"]["placements"][0]["role"])
            self._assert_positions(device, names)
        for (group, address), device in self.outputs.items():
            if device["spatial"]["status"] != "observed":
                continue
            if group == "pinmame.output.solenoid" and str(device["kind"]) == "flasher":
                if address in curator.BIGUS_FLASH_PLACEMENTS:
                    names = [curator.BIGUS_FLASH_PLACEMENTS[address][0]]
                    self._assert_positions(device, names, curator.BIGUS_GEOMETRY["objects"])
                    continue
                names = [n for n in self.geometry["flashers"][str(address)]
                         if n.lower() not in {x.lower() for x in curator.DROPPED_BULBS}]
            elif group == "pinmame.output.solenoid":
                names = [self.geometry["coils"][str(address)].split(".", 1)[1]]
            elif address == 111:
                names = self.geometry["gi"]
            else:
                names = self.geometry["lamps"][str(address)]
            self.assertEqual(LOCATED_ROLE[device["kind"]], device["spatial"]["placements"][0]["role"])
            self._assert_positions(device, names)

    def _assert_positions(self, device, names, objects=None):
        objects = objects if objects is not None else self.geometry["objects"]
        placements = device["spatial"]["placements"]
        self.assertEqual(len(names), len(placements), device["id"])
        for name, placement in zip(names, placements):
            self.assertEqual(objects[name]["xy"], [placement["x"], placement["y"]], name)
            self.assertEqual("playfield", placement["space"])
            self.assertEqual(device["spatial"]["status"], placement["provenance"]["status"])
            self.assertIn(placement["provenance"]["source_refs"],
                          ([curator.TABLE, curator.SCRIPT, curator.MANUAL],
                           [curator.BIGUS, curator.BIGUS_SCRIPT, curator.MANUAL],
                           [curator.TABLE, curator.SCRIPT, curator.MANUAL,
                            curator.BIGUS, curator.BIGUS_SCRIPT]))

    def test_out_of_range_wall_sprites_are_dropped_not_clamped(self):
        placed = {p["id"].rsplit("-", 1)[1] for d in self.machine["outputs"]
                  for p in d["spatial"].get("placements", [])}
        for dropped in curator.DROPPED_BULBS:
            self.assertNotIn(dropped.lower(), {name.lower() for name in placed})

    def test_curator_is_deterministic_and_the_report_reconciles(self):
        built = curator.build()
        built.pop("_spatial_notes")
        self.assertEqual(curator.canonical(built), DEFINITION.read_bytes())
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])
        self.assertEqual(KEY, self.report["machine_id"])
        self.assertEqual(sorted(self.machine["coverage"]["missing"]),
                         self.report["promotion"]["missing"])
        self.assertFalse(self.report["promotion"]["allowed"])
        self.assertEqual(self.geometry["bounds"], self.report["bounds"])

    def test_sources_are_declared_with_exact_hashes(self):
        sources = {s["id"]: s for s in self.machine["sources"]}
        self.assertEqual(curator.TABLE_SHA, sources[curator.TABLE]["sha256"])
        self.assertEqual(curator.SCRIPT_SHA, sources[curator.SCRIPT]["sha256"])
        self.assertEqual(curator.MANUAL_SHA, sources[curator.MANUAL]["sha256"])
        self.assertEqual(curator.GEOMETRY["script_sha256"], curator.SCRIPT_SHA)
        self.assertEqual(curator.GEOMETRY["table_sha256"], curator.TABLE_SHA)
        self.assertEqual(curator.BIGUS_TABLE_SHA, sources[curator.BIGUS]["sha256"])
        self.assertEqual(curator.BIGUS_SCRIPT_SHA, sources[curator.BIGUS_SCRIPT]["sha256"])
        self.assertEqual(curator.BIGUS_GEOMETRY["table_sha256"], curator.BIGUS_TABLE_SHA)
        self.assertEqual(curator.BIGUS_GEOMETRY["script_sha256"], curator.BIGUS_SCRIPT_SHA)
        for source_id in (curator.BIGUS, curator.BIGUS_SCRIPT):
            self.assertEqual("NOASSERTION", sources[source_id]["license"])
            self.assertTrue(sources[source_id]["attribution"])

    def test_bigus_supplement_reconciles_with_the_pinned_geometries(self):
        supplement = self.report["supplement"]
        distances = curator.supplement_distances()
        self.assertEqual(distances, supplement["distances"])
        fitted = distances["fitted"]
        summary = supplement["summary"]
        self.assertEqual(len(fitted), summary["compared"])
        self.assertEqual(sum(1 for d in fitted.values() if d <= curator.AGREE),
                         summary["agree_within_0_025_fitted"])
        self.assertEqual(max(fitted.values()), summary["max_fitted_distance"])
        self.assertEqual(len(curator.validated_addresses()), summary["validated_addresses"])
        self.assertEqual(sorted(curator.KIT_EXCLUDED), supplement["kit_excluded"])
        self.assertEqual(curator.BIGUS_GEOMETRY["frame"], supplement["frame"])
        self.assertEqual({"bigus-3-0": 16, "vpw-1-2-2": 17}, supplement["gi_bulb_counts"])
        self.assertEqual(curator.BIGUS_GEOMETRY["unbound"], supplement["unbound"])
        self.assertEqual("observed", self.machine["coverage"]["dimensions"]["spatial_placement"])
        self.assertFalse(self.report["promotion"]["allowed"])

    def test_validation_follows_the_fitted_agreement_rule(self):
        def key_of(device):
            group = str(device["binding"]["group"])
            address = int(device["binding"]["device"])
            if group == "pinmame.output.solenoid":
                return f"flasher.{address}" if str(device["kind"]) == "flasher" else f"coil.{address}"
            if group == "pinmame.output.lamp" and address == 111:
                return "gi"
            if group == "pinmame.output.lamp":
                return f"lamp.{address}"
            return None
        validated = curator.validated_addresses()
        for device in self.machine["inputs"]:
            if device["spatial"]["status"] == "not_applicable":
                continue
            address = int(device["binding"]["device"])
            key = f"switch.{address}"
            expected = "validated" if key in validated else "observed"
            self.assertEqual(expected, device["spatial"]["status"], key)
        for device in self.machine["outputs"]:
            if device["spatial"]["status"] == "not_applicable":
                continue
            key = key_of(device)
            expected = "validated" if key in validated else "observed"
            self.assertEqual(expected, device["spatial"]["status"], key)
        # The conversion-kit region, the GI channel, the diverging positions and the
        # Bigus-only banks never validate. Flash bank 28's position agrees (its disclosed
        # emitter-count divergence is a note, not a position disagreement).
        for key in sorted(curator.KIT_EXCLUDED) + ["gi", "lamp.58", "flasher.26", "flasher.27",
                                                   "flasher.29", "flasher.31"]:
            self.assertNotIn(key, validated)
        self.assertIn("flasher.28", validated)

    def test_cabinet_and_relay_dispositions_are_corroborated_by_the_second_table(self):
        for address in (1, 50, 51):
            refs = self.inputs[address]["spatial"]["provenance"]["source_refs"]
            self.assertIn(curator.BIGUS_SCRIPT, refs)
        relay = self.outputs[("pinmame.output.solenoid", 11)]["spatial"]["provenance"]["source_refs"]
        self.assertIn(curator.BIGUS_SCRIPT, relay)
        jabba = self.outputs[("pinmame.output.lamp", 48)]["spatial"]["provenance"]["source_refs"]
        self.assertNotIn(curator.BIGUS_SCRIPT, jabba)

    def test_flash_banks_29_and_31_are_placed_from_the_second_table_alone(self):
        for address in (29, 31):
            device = self.outputs[("pinmame.output.solenoid", address)]
            spatial = device["spatial"]
            self.assertEqual("observed", spatial["status"])
            self.assertEqual(1, len(spatial["placements"]))
            placement = spatial["placements"][0]
            self.assertEqual([curator.BIGUS, curator.BIGUS_SCRIPT, curator.MANUAL],
                             placement["provenance"]["source_refs"])
            name = curator.BIGUS_FLASH_PLACEMENTS[address][0]
            self.assertEqual(curator.BIGUS_GEOMETRY["objects"][name]["xy"],
                             [placement["x"], placement["y"]])
            self.assertIn("Bigus", device["physical"]["notes"])


if __name__ == "__main__":
    unittest.main()
