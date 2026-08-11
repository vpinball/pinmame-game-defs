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
KNOWLEDGE_PATH = ROOT / "knowledge" / "data-east" / "laser-war-1987.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.laser-war.1987"
OWN_DRIVERS = {"lwar_a81", "lwar_a83", "lwar_e90"}


TECH_CHART_SWITCHES = [
    "Plumb Bob Tilt", "Ball Roll Tilt", "Start Button", "Right Coin Switch", "Center Coin Switch", "Left Coin Switch", "Slam Tilt", None,
    "Playfield Tilt", "Ball Trough 3", "Ball Trough 2", "Ball Trough 1", "Outhole", "Right Slingshot", "Left Slingshot", None,
    "Laser Kick", "Left Flipper Return Lane", "Right Flipper Return Lane", "Right Outlane", "10 Point Rubber Right (2 Switches)",
    "Red Target (Left)", "Red Target (Center)", "Red Target (Right)", "Red Eject", "Red Star", "Red Spinner", None, "Ramp",
    "Yellow Target (Left)", "Yellow Target (Center)", "Yellow Target (Right)", "Yellow Eject", "Yellow Star",
    "Blue Target (Left)", "Blue Target (Center)", "Blue Target (Right)", "Blue Eject", "Blue Star", "W", "A", "R",
    "Pop Bumper Red", "Pop Bumper Yellow", "Pop Bumper Blue", "Right Flipper (EOS)", "Left Flipper (EOS)",
    "Red Star (Upper Right)", "Yellow Star (Upper Right)", "Blue Star (Upper Right)", "Yellow Spinner", "Shooter Lane",
    None, None, None, None, None, None, None, None, None, None, None, None,
]

TECH_CHART_LAMPS = [
    "Ball in Play", "Match", "Blast Again", "W", "A", "R", "Ramp Multiplier", "Return to Base",
    "Cannon Red", "Cannon Yellow", "Cannon Blue", "Ramp Green Shield", "Ramp Orange Arrow", "Ramp Amber Arrow", "Ramp Clear Arrow",
    "Red Target (Left)", "Red Target (Center)", "Red Target (Right)", "Hot Dog Red", "Lock Red Eject",
    "Red Eject Clear Arrow", "Red Eject Amber Arrow", "Red Eject Orange Arrow", "Yellow Target (Left)", "Yellow Target (Center)",
    "Yellow Target (Right)", "Hot Dog Yellow", "Lock Yellow Eject", "Yellow Eject Clear Arrow", "Yellow Eject Amber Arrow",
    "Yellow Eject Orange Arrow", "Blue Target (Left)", "Blue Target (Center)", "Blue Target (Right)", "Hot Dog Blue", "Lock Blue Eject",
    "Blue Eject Clear Arrow", "Blue Eject Amber Arrow", "Blue Eject Orange Arrow", "Left Outlane",
    "Flipper Return Lanes (Left & Right)", "Bonus Holds", "2 X", "3 X", "4 X", "5 X", "Laser Kick", "Right Outlane",
    "Ion Cannon (Tip)", "Bonus 1K Red", "Bonus 2K Red", "Bonus 4K Red", "Bonus 8K Red", "Bonus 16K Red",
    "Bonus 1K Yellow", "Bonus 2K Yellow", "Bonus 4K Yellow", "Bonus 8K Yellow", "Bonus 16K Yellow",
    "Bonus 1K Blue", "Bonus 2K Blue", "Bonus 4K Blue", "Bonus 8K Blue", "Bonus 16K Blue",
]

TECH_CHART_COILS = {
    1: "Explosion", 2: "Red Hot Dog", 3: "Yellow Hot Dog", 4: "Blue Hot Dog", 5: "Ion Cannon",
    6: "Mars Yellow", 7: "Mars Red", 8: "Mars Blue", 9: "Ball Trough Eject", 10: "L/R Power Relay",
    11: "General Illumination Relay", 12: "Red Eject", 13: "Yellow Eject", 14: "Blue Eject", 15: "Laser Kick (Relay)",
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
        self.assertEqual({"platform": "pinmame.dataeast", "hardware_generation": "0x1000", "inversion_applied_by_emulator": False},
                         self.definition["controller"])
        self.assertEqual(OWN_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
        root = next(driver for driver in self.definition["drivers"] if driver["id"] == "lwar_a83")
        self.assertNotIn("clone_of", root)
        self.assertEqual({"lwar_a81", "lwar_e90"}, {driver["id"] for driver in self.definition["drivers"] if driver.get("clone_of") == "lwar_a83"})
        self.assertTrue(all(driver["year"] == "1987" and driver["manufacturer"] == "Data East" for driver in self.definition["drivers"]))
        self.assertEqual({"width": 964.0, "height": 2162.0, "units": "vpx", "provenance": {"status": "validated", "source_refs": ["vpx-table.laser-war-vr-2-0"]}},
                         self.definition["machine"]["playfield"])

    def test_data_east_controller_gap_is_explicit_and_namespaces_are_exact(self) -> None:
        self.assertFalse((ROOT / "controllers" / "pinmame" / "dataeast.json").exists())
        blockers = [item for item in load_json(REPORT_PATH)["blockers"] if item["dimension"] == "controller_platform"]
        self.assertEqual([["pinmame.dataeast"]], [item["devices"] for item in blockers])
        self.assertEqual({-7, -6}, {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["device"] < 0})
        self.assertEqual(set(range(1, 51)), {item["binding"]["device"] for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"})
        self.assertEqual(set(range(1, 65)), {item["binding"]["device"] for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"})
        aliases = [alias for collection in (self.definition["inputs"], self.definition["outputs"]) for item in collection for alias in item.get("aliases", [])]
        self.assertFalse(any(alias["namespace"].startswith("manual.") for alias in aliases))

    def test_coverage_is_fail_closed_and_names_every_missing_dimension(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["controller_platform", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"], coverage["missing"])
        self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
        self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])
        blockers = load_json(REPORT_PATH)["blockers"]
        blocker_dimensions = {item["dimension"] for item in blockers}
        self.assertTrue(set(coverage["missing"]) - {"unresolved_conflicts"} <= blocker_dimensions)
        output_semantics = next(item for item in blockers if item["dimension"] == "output_semantics")
        self.assertEqual(
            {f"coil.driver-{address}" for address in (*range(17, 23), 30, 31, 32)},
            set(output_semantics["devices"]),
        )
        self.assertIn("PIA or K1-multiplexed public state", output_semantics["reason"])

    def test_switch_namespace_is_complete_and_matches_independent_fixture(self) -> None:
        matrix = {item["binding"]["device"]: item for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] > 0}
        self.assertEqual(set(range(1, 65)), set(matrix))
        for address, printed in enumerate(TECH_CHART_SWITCHES, start=1):
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
        self.assertEqual(TECH_CHART_LAMPS, [lamps[address]["label"] for address in range(1, 65)])
        self.assertTrue(all(item["availability"] == "used" for item in lamps.values()))
        self.assertEqual(2, lamps[41]["physical"]["quantity"])
        self.assertNotIn("spatial", lamps[8])
        self.assertNotIn("spatial", lamps[49])

    def test_solenoid_namespace_is_exactly_public_1_through_50(self) -> None:
        solenoids = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        self.assertEqual(set(range(1, 51)), set(solenoids))
        for address, label in TECH_CHART_COILS.items():
            self.assertEqual(label, solenoids[address]["label"], address)
        self.assertEqual("relay", solenoids[11]["kind"])
        self.assertEqual(1, solenoids[11]["physical"]["quantity"])
        self.assertEqual({30, 31, 32}, {address for address in (25, 26, 27, 28, 29, 30, 31, 32) if solenoids[address]["availability"] == "unknown"})
        self.assertEqual({30: "Unfitted Mux Branch 6R", 31: "Unfitted Mux Branch 7R", 32: "Unfitted Mux Branch 8R"}, {address: solenoids[address]["label"] for address in (30, 31, 32)})
        self.assertEqual(
            {17: "Blue Pop Bumper", 18: "Yellow Pop Bumper", 19: "Left Slingshot", 20: "Red Pop Bumper", 21: "Right Slingshot", 22: "Unfitted Special-Solenoid Driver"},
            {address: solenoids[address]["label"] for address in range(17, 23)},
        )
        self.assertEqual({22}, {address for address in range(17, 23) if solenoids[address]["availability"] == "unknown"})
        self.assertEqual("virtual", solenoids[22]["kind"])
        self.assertEqual("virtual", solenoids[22]["spatial"]["reason"])
        self.assertTrue(all(solenoids[address]["physical"].get("quantity") == 1 for address in range(17, 22)))
        self.assertNotIn("quantity", solenoids[22]["physical"])
        printed = {17: (17, "Q8"), 18: (18, "Q9"), 19: (19, "Q10"), 20: (20, "Q11"), 21: (21, "Q12"), 22: (22, "Q13")}
        for address, (coil_number, transistor) in printed.items():
            aliases = {(alias["namespace"], alias["value"]) for alias in solenoids[address]["aliases"]}
            self.assertIn(("technical-chart.coil-number", str(coil_number)), aliases)
            self.assertFalse(any(namespace.endswith("special-solenoid") for namespace, _value in aliases))
            self.assertEqual(transistor, solenoids[address]["wiring"]["driver_transistor"])
            self.assertEqual("conflicted", solenoids[address]["provenance"]["status"])
        self.assertNotIn("power_wire", solenoids[22]["wiring"])
        self.assertEqual("BRN-BLK", solenoids[9]["wiring"]["drive_wire"])
        for address in (30, 31, 32):
            self.assertNotIn("drive_wire", solenoids[address]["wiring"])
            self.assertNotIn("power_wire", solenoids[address]["wiring"])
            self.assertNotIn("device: .", solenoids[address]["physical"]["notes"])
            self.assertIn("public-address availability remains unknown", solenoids[address]["physical"]["notes"])
            self.assertEqual("virtual", solenoids[address]["spatial"]["reason"])
        for address in range(45, 49):
            self.assertEqual("virtual", solenoids[address]["kind"])
            self.assertEqual("used", solenoids[address]["availability"])
            self.assertNotIn("quantity", solenoids[address]["physical"])
            self.assertEqual("virtual", solenoids[address]["spatial"]["reason"])
        self.assertTrue(all(solenoids[address]["availability"] == "unused" for address in range(33, 45)))
        self.assertEqual("flasher", solenoids[6]["kind"])
        self.assertNotIn("part_number", solenoids[6]["physical"])
        self.assertIn("type 23-800", solenoids[6]["physical"]["notes"])
        self.assertIn(
            ("technical-chart.coil-number", "1R"),
            {(alias["namespace"], alias["value"]) for alias in solenoids[25]["aliases"]},
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
        self.assertEqual([], mechanisms["mechanism.kickback"]["actuators"])
        self.assertEqual("candidate", mechanisms["mechanism.kickback"]["provenance"]["status"])
        self.assertEqual({
            "mechanism.left-slingshot": ["coil.driver-19"],
            "mechanism.right-slingshot": ["coil.driver-21"],
            "mechanism.red-pop-bumper": ["coil.driver-20"],
            "mechanism.yellow-pop-bumper": ["coil.driver-18"],
            "mechanism.blue-pop-bumper": ["coil.driver-17"],
        }, {identifier: mechanisms[identifier]["actuators"] for identifier in ("mechanism.left-slingshot", "mechanism.right-slingshot", "mechanism.red-pop-bumper", "mechanism.yellow-pop-bumper", "mechanism.blue-pop-bumper")})
        self.assertTrue(all(mechanisms[identifier]["provenance"]["status"] == "conflicted" for identifier in ("mechanism.left-slingshot", "mechanism.right-slingshot", "mechanism.red-pop-bumper", "mechanism.yellow-pop-bumper", "mechanism.blue-pop-bumper")))

    def test_relay_mux_relationships_cover_the_whole_right_bank(self) -> None:
        relationships = self.definition["relationships"]
        mux = [item for item in relationships if item["source"] == "coil.driver-10"]
        self.assertEqual(8, len(mux))
        self.assertEqual({f"coil.driver-{address}" for address in range(25, 33)}, {item["destination"] for item in mux})
        self.assertTrue(all(item["kind"] == "relay_gated" for item in mux))
        kickback = next(item for item in relationships if item["id"] == "relationship.kickback-relay-gate")
        self.assertEqual(("coil.driver-15", "mechanism.kickback", "relay_gated"),
                         (kickback["source"], kickback["destination"], kickback["kind"]))

    def test_conflicts_are_preserved_not_silently_resolved(self) -> None:
        self.assertEqual({
            "conflict.switch-17-name", "conflict.right-flipper-eos-runtime",
            "conflict.left-flipper-eos-runtime", "conflict.lamp-8-runtime-binding",
            "conflict.lamp-26-printed-label-duplicate",
            "conflict.mars-yellow-printed-device-type",
            "conflict.mux-bank-output-typing",
            "conflict.special-solenoid-public-mapping", "conflict.synthetic-flipper-public-state",
        }, {item["id"] for item in self.definition["conflicts"]})
        self.assertEqual("conflicted", self.inputs["switch.matrix-46"]["provenance"]["status"])
        self.assertEqual("conflicted", self.inputs["switch.matrix-47"]["provenance"]["status"])
        self.assertEqual("conflicted", self.outputs["lamp.matrix-8"]["provenance"]["status"])
        self.assertEqual("conflicted", self.outputs["lamp.matrix-26"]["provenance"]["status"])
        self.assertEqual("Yellow Target (Right)", self.outputs["lamp.matrix-26"]["label"])
        self.assertIn("literally prints Red Target (Right)", self.outputs["lamp.matrix-26"]["physical"]["notes"])
        self.assertTrue(all(self.outputs[f"coil.driver-{address}"]["provenance"]["status"] == "conflicted" for address in range(17, 23)))
        self.assertTrue(all(self.outputs[f"coil.driver-{address}"]["provenance"]["status"] == "conflicted" for address in range(45, 49)))
        self.assertTrue(all(self.outputs[f"coil.driver-{address}"]["provenance"]["status"] == "conflicted"
                            for address in (4, 5, 6, 7, 8, 29, 30, 31, 32)))

    def test_spatial_records_use_normalized_bounds_and_exclude_helpers(self) -> None:
        report = load_json(REPORT_PATH)
        self.assertEqual("pinmame-spatial-blockers", report["format"])
        self.assertIn("conflict.lamp-26-printed-label-duplicate", report["conflicts"])
        self.assertEqual({"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0}, report["coordinate_system"]["raw_bounds"])
        placements = []
        for collection in (self.definition["inputs"], self.definition["outputs"]):
            for item in collection:
                placements.extend(item.get("spatial", {}).get("placements", []))
        self.assertTrue(placements)
        self.assertTrue(all(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1 for item in placements))
        self.assertEqual(2, len(self.inputs["switch.matrix-21"]["spatial"]["placements"]))
        self.assertTrue(all(self.inputs[f"switch.matrix-{address}"]["spatial"]["status"] == "candidate" for address in (14, 15, 21)))
        self.assertEqual(2, len(self.outputs["lamp.matrix-41"]["spatial"]["placements"]))
        self.assertEqual("not_applicable", self.outputs["coil.driver-11"]["spatial"]["status"])
        self.assertEqual("internal_nonvisual", self.outputs["coil.driver-11"]["spatial"]["reason"])
        self.assertNotIn("placements", self.outputs["coil.driver-11"]["spatial"])
        report_text = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("suffix-a glow/lightmap", report_text)
        self.assertNotIn('"id": "lamp.matrix-9.placement-', DEFINITION_PATH.read_text(encoding="utf-8"))
        markdown = REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
        self.assertIn("# Data East Laser War (1987) spatial audit", markdown)
        self.assertIn("## Explicit projection classes", markdown)
        self.assertIn("special-solenoid-to-mechanism", markdown)
        self.assertIn("wall-drag-point-centroid", markdown)
        self.assertIn("Keep partial", markdown)

    def test_evidence_excerpts_exist_and_hashes_match_source_records(self) -> None:
        manual = self.sources["manual.data-east.laser-war.1987"]
        self.assertNotIn("excerpts", manual)
        self.assertIn("typeset chart text is absent", manual["locator"])
        self.assertEqual("2026-08-09T18:37:51Z", manual["acquired_at"])
        tech_chart = self.sources["tech-chart.pinballrebel.data-east-laser-war"]
        self.assertEqual("service_diagnostic", tech_chart["kind"])
        self.assertIn("secondary evidence", tech_chart["locator"])
        self.assertIn("https://www.pinballrebel.com/", tech_chart["locator"])
        self.assertEqual("Data_East_Laser_War_Tech_Chart.pdf", tech_chart["original_filename"])
        self.assertTrue(tech_chart["uri"].startswith("external:pinmame-manuals/"))
        self.assertEqual("2026-08-09T18:53:30Z", tech_chart["acquired_at"])
        self.assertEqual(5, len(tech_chart["excerpts"]))
        for excerpt in tech_chart["excerpts"]:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertEqual("manual", excerpt["method"])
            self.assertTrue(excerpt["reviewed"])
            self.assertIn("Human transcription", path.read_text(encoding="utf-8"))
        switch_text = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
        lamp_text = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
        coil_text = (EXCERPT_ROOT / "coil-chart.md").read_text(encoding="utf-8")
        self.assertIn("community technical chart", switch_text)
        self.assertIn("| 1 | Green-Brown | CN8-1 | Q55 |", switch_text)
        self.assertIn("| 6 | Green-Blue | CN8-7 | Q50 |", switch_text)
        self.assertIn("| 1 | White-Brown | CN10-9 | [not printed] |", switch_text)
        self.assertIn("| 6 | White-Blue | CN10-3 | [not printed] |", switch_text)
        self.assertIn("| 1 | 1 | 1 | Plump Bob Tilt |", switch_text)
        self.assertNotIn("Playfield Switch Location Illustration list", switch_text)
        self.assertIn("| 1 | Yellow-Brown | CN7-1 | Q71 |", lamp_text)
        self.assertIn("| 5 | Yellow-Green | CN7-6 | Q67 |", lamp_text)
        self.assertIn("| 1 | Red-Brown | CN6-1 | Q72 |", lamp_text)
        self.assertIn("| 4 | Red-Yellow | CN6-5 | Q75 |", lamp_text)
        self.assertIn('| 4 | 1 | 4 | "W" |', lamp_text)
        self.assertIn("| 8 | 1 | 8 | Return To Base |", lamp_text)
        self.assertIn("| 26 | 4 | 2 | Red Target (Right) |", lamp_text)
        self.assertIn("literally repeats `Red Target (Right)`", lamp_text)
        self.assertIn("Flipper Return Lanes (Left & Right)", lamp_text)
        self.assertIn("| 43 | 6 | 3 | 2X |", lamp_text)
        self.assertNotIn("`NOT USED` is preserved", lamp_text)
        self.assertNotIn("Playfield Lamp Location Illustration list", lamp_text)
        self.assertIn("| 8 | 1 | 8 | Not Used |", switch_text)
        self.assertNotIn("| 8 | 1 | 8 | NOT USED |", switch_text)
        self.assertIn("| 1R | Ramp Multiplier Flasher | Q46 | Gry-Brn | Blk-Brn | to diode board | Orn | 4M-9 | 32V R | #89 |", coil_text)
        self.assertEqual(1, coil_text.count("| 2L |"))
        self.assertIn("| 6L | Mars Yellow | Q41 | CPU to DB | Vio-Blu | CPU CN11-7 | Brn | 4M-8 | 32V L | 23-800 |", coil_text)
        self.assertIn("| 6R | Not Used | Q41 | Gry-Blu | [blank] | to diode board | [blank] | [blank] | [blank] | [blank] |", coil_text)
        self.assertIn("| 9 | Ball Trough Eject | Q30 | CPU | Brn-Blk | CN12-1 | Red | PS CN3-6 | 32V | 23-840 |", coil_text)
        self.assertIn("Warriors (Back Glass) Flasher", coil_text)
        self.assertIn("## Reconciliation to PinMAME public addresses and semantic kinds", coil_text)
        self.assertIn("maps printed 1R-8R to public addresses 25-32", coil_text)
        self.assertNotIn("INSTALL ADD-A-BALL", coil_text)
        self.assertEqual("30a1def10178a2cf7e753046ed44f07d01075a6333791669e4fe0c4e165ddfe7", tech_chart["sha256"])
        tech_excerpt = next(item for item in tech_chart["excerpts"] if item["id"] == "excerpt.laser-war.technical-chart-special-solenoids")
        tech_excerpt_path = ROOT / tech_excerpt["path"]
        self.assertTrue(tech_excerpt_path.is_file())
        self.assertEqual(tech_excerpt["sha256"], sha256(tech_excerpt_path))
        self.assertEqual("manual", tech_excerpt["method"])
        self.assertTrue(tech_excerpt["reviewed"])
        tech_excerpt_text = tech_excerpt_path.read_text(encoding="utf-8")
        self.assertIn("| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil or Flash Type |", tech_excerpt_text)
        self.assertIn("| 17 | Blue Pop Bumper | Q8 | CPU | Blu-Orn | CN19-3 | Red | PS CN3-6 | 32V | 23-800 |", tech_excerpt_text)
        self.assertIn("| 22 | Not Used | Q13 | CPU | Blu-Blk | CN19-9 | [blank] | [blank] | [blank] | [blank] |", tech_excerpt_text)
        flipper_excerpt = next(item for item in tech_chart["excerpts"] if item["id"] == "excerpt.laser-war.flipper-circuits")
        flipper_text = (ROOT / flipper_excerpt["path"]).read_text(encoding="utf-8")
        self.assertIn("| Left flipper | CN3-1,2 | Gry-Yel / 4M/F4-5 | [blank] |", flipper_text)
        self.assertIn("23-620/30-2600 (090-5000-00)", flipper_text)
        manifest_source = self.sources["vpx-extraction.laser-war-vr-2-0"]
        self.assertEqual(manifest_source["sha256"], sha256(MANIFEST_PATH))

    def test_manifest_canonical_digest_and_shape(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(2927, manifest["file_count"])
        self.assertEqual(163816471, manifest["total_bytes"])
        self.assertEqual(manifest["file_count"], len(manifest["files"]))
        self.assertEqual(len({entry["path"] for entry in manifest["files"]}), manifest["file_count"])
        algorithm = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
        self.assertEqual(algorithm, manifest["manifest_algorithm"])
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("9642a642737c4513b1a26d311a5c298e0f7c511e83f7bdfad7d70f0e211c10c1", manifest["manifest_sha256"])
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
        manifest_source = self.sources["vpx-extraction.laser-war-vr-2-0"]
        self.assertEqual("a4a2c13176cc604fc88bc20b277e2cffb65a2d5abb8c787e4449d01c8ccfc03d", manifest_source["sha256"])
        self.assertIn(f"algorithm: {algorithm}", manifest_source["locator"])

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
        semantic_text = artifact_text
        for source in self.definition["sources"]:
            for metadata_key in ("uri", "locator", "attribution", "license", "original_filename", "source_id"):
                metadata_value = source.get(metadata_key)
                if isinstance(metadata_value, str):
                    semantic_text = semantic_text.replace(metadata_value.casefold(), "")
        artifact_identifier_tokens = set(re.findall(r"[a-z0-9_]+", semantic_text))
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

    def test_seed_is_byte_identical_and_knowledge_names_remaining_blockers(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("42-page image-only archive", knowledge)
        self.assertIn("Blue Pop/17, Yellow Pop/18, Left Sling/19, Red Pop/20, Right Sling/21 and unfitted/22", knowledge)
        self.assertIn("addresses 22 and 30-32", knowledge)
        self.assertIn("Nine disagreements", knowledge)
        self.assertIn("lamp 26", knowledge)
        self.assertIn("controller_platform", knowledge)
        self.assertIn("Synthetic flipper outputs 45-48 are virtual", knowledge)


class LaserWarCuratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "tools"))
        import curate_laser_war
        cls.curator = curate_laser_war

    def test_data_east_special_solenoid_conflict_preserves_both_orders(self) -> None:
        derived = {
            17 + self.curator.SPECIAL_DE_PERMUTATION[handler]: source_label
            for handler, source_label in self.curator.SPECIAL_PIA_HANDLER_TO_SOURCE_LABEL.items()
        }
        self.assertEqual({17: "SS1", 18: "SST3", 19: "SS4", 20: "SS6", 21: "SS5", 22: "SST2"}, derived)
        self.assertEqual(derived, self.curator.SPECIAL_SOURCE_INFERRED_PUBLIC_TO_LABEL)
        self.assertEqual(set(range(17, 23)), set(self.curator.SPECIAL_CHART_DEVICES))

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
        cls.sources = {source["id"]: source for source in load_json(DEFINITION_PATH)["sources"]}

    def retained_manual_path(self, source_id: str) -> Path:
        assert self.manual_anchor is not None
        prefix = "external:pinmame-manuals/"
        uri = self.sources[source_id]["uri"]
        self.assertTrue(uri.startswith(prefix), (source_id, uri))
        return self.manual_anchor / uri.removeprefix(prefix)

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
        actual = sorted(path.relative_to(extraction).as_posix() for path in extraction.rglob("*") if path.is_file())
        self.assertEqual(actual, [entry["path"] for entry in manifest["files"]])
        for entry in manifest["files"]:
            path = extraction / entry["path"]
            self.assertEqual(entry["bytes"], path.stat().st_size, entry["path"])
            self.assertEqual(entry["sha256"], sha256(path), entry["path"])

    def test_exact_manual_and_technical_chart_hashes_via_supplied_manual_root_anchor(self) -> None:
        if self.manual_anchor is None:
            self.skipTest("retained manuals are not available")
        manual = self.retained_manual_path("manual.data-east.laser-war.1987")
        tech_chart = self.retained_manual_path("tech-chart.pinballrebel.data-east-laser-war")
        self.assertEqual(2_370_660, manual.stat().st_size)
        self.assertEqual("e8e55768c990f2967594f4112bc2ec7403c55e5283c7b69fae2ff5c1d21fefbf", sha256(manual))
        self.assertEqual(183_399, tech_chart.stat().st_size)
        self.assertEqual("30a1def10178a2cf7e753046ed44f07d01075a6333791669e4fe0c4e165ddfe7", sha256(tech_chart))


if __name__ == "__main__":
    unittest.main()
