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
DEFINITION_PATH = ROOT / "machines" / "partial" / "data-east" / "torpedo-alley-1988.json"
SEED_PATH = ROOT / "tools" / "seeds" / "data-east" / "torpedo-alley-1988.json"
MANIFEST_PATH = ROOT / "tools" / "seeds" / "data-east" / "torpedo-alley-1988-extraction-manifest.json"
REPORT_PATH = ROOT / "reports" / "spatial" / "data-east" / "torpedo-alley-1988.json"
REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "data-east" / "torpedo-alley-1988.md"
KNOWLEDGE_PATH = ROOT / "knowledge" / "data-east" / "torpedo-alley-1988.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.torpedo-alley.1988"
OWN_DRIVERS = {"torp_e21", "torp_a16"}


PRINTED_SWITCHES = [
    "Plumb Tilt", None, "Credit Button", "Right Coin", "Center Coin", "Left Coin", "Slam Tilt", None,
    None, "Outhole", "Trough :1", "Trough :2", "Trough :3", "Shooter Lane", "Left EOS", "Right EOS",
    "Laser Kick", "Left Return", None, "Left Green Target", "Center Green Target", "Right Green Target",
    "Bottom Left Star Rollover", "Spots Laser Kick Target", "Top Left Spinner", '"S" Lane', '"U" Lane',
    '"B" Lane', "Left Drop Target", "Center Drop Target", "Right Drop Target", "Right Spinner",
    "Left Yellow Target", "Center Yellow Target", "Right Yellow Target", "Right Star Rollover",
    "Left 50 Point Switch", "Left Blue Target", "Center Blue Target", "Right Blue Target", "Left Kicker :1",
    "Left Kicker :2", "Vertical Up Kicker", "Center Kicker :1", "Center Kicker :2", "Ramp", None, None,
    "Left Thumper Bumper", "Right Thumper Bumper", "Center Thumper Bumper", "Left Slingshot",
    "Right Slingshot", "Right Outlane", "Right Return", "Right 50 Point Switch",
    None, None, None, None, None, None, None, None,
]

SWITCH_LABEL_OVERRIDES = {
    11: "Trough #1", 12: "Trough #2", 13: "Trough #3", 15: "Left Flipper EOS",
    16: "Right Flipper EOS", 41: "Left Kicker #1", 42: "Left Kicker #2",
    44: "Center Kicker #1", 45: "Center Kicker #2",
}

LAMPS = [
    "Lockball :2 (2)", "Spot Laser Kick", "Destroy Fleet 100K", "Destroy Fleet 25K Green",
    "Destroy Fleet 25K Blue", "Destroy Fleet 25K Yellow", "Top Left Playfield 2X",
    "Release Torpedoes Hotdog (2)", '"S" Lane', '"U" Lane', '"B" Lane', "Extra Ball Triangle",
    "Flagship 25K Clear", "Flagship 50K Yellow", "Flagship 100K Orange", "Insert 2 Torpedo",
    "Top Right Playfield 2X", "5K When Lit", "Yellow Arrow :1", "Yellow Arrow :2", "Yellow Arrow :3",
    "Aircraft Carrier Hotdog", "Lockball :1 (2)", "Insert 1 Torpedo (2)", "Ramp 20K Clear",
    "Ramp 30K Yellow", "Ramp 40K Green", "Ramp Hold Bonus Orange", "Ramp Extra Ball Amber",
    "Ramp Hotdog Special", "Periscope Left (2)", "Periscope Right (2)", "Green Arrow :1",
    "Green Arrow :2", "Green Arrow :3", "Destroyer Hotdog", "Blue Arrow :1", "Blue Arrow :2",
    "Blue Arrow :3", "Cruiser Hotdog", "Shield Playfield 2X", "Blue 10K", "Green 10K", "Yellow 10K",
    "Blue 20K", "Green 20K", "Yellow 20K", "Right Return", "Laser Kick", "Green 30K", "Yellow 30K",
    "2X", "3X", "5X", "Fire Again", "Right Outlane", "Jackpot 100K Shield", "Blue 40K",
    "Green 40K", "Yellow 40K", "Blue 30K", "Left Special", "Left Return", "Release Balls",
]

SOLENOIDS = [
    "Destroyer Hotdog", "Release Torpedo Hotdog", "Flagship Hotdog", "Aircraft Carrier Hotdog",
    "Special Hotdog", "Cruiser Hotdog", "Scope", "Insert Top", "Left Pair", "Left/Right Coil Relay",
    "General Illumination Relay", "Unused Solenoid 12", "Unused Solenoid 13", "Center Pair", "Right Pair",
    "Trough", "Center Thumper Bumper", "Left Slingshot", "Left Thumper Bumper", "Unused SP6 Driver",
    "Right Slingshot", "Right Thumper Bumper", "Game On / Flipper and Special-Solenoid Enable",
    "Unused Solenoid 24", "Laser Kicker", "Left Kickback", "Vertical Up Kicker", "Center Kickback",
    "3-Bank Drop Target Reset", "Knocker", "Outhole", "Sinking Ship", "Inert Solenoid Address 33",
    "Inert Solenoid Address 34", "Inert Solenoid Address 35", "Inert Solenoid Address 36",
    "Inert Solenoid Address 37", "Inert Solenoid Address 38", "Inert Solenoid Address 39",
    "Inert Solenoid Address 40", "Inert Solenoid Address 41", "Inert Solenoid Address 42",
    "Inert Solenoid Address 43", "Inert Solenoid Address 44", "Synthetic Right Flipper Power",
    "Synthetic Right Flipper Hold", "Synthetic Left Flipper Power", "Synthetic Left Flipper Hold",
    "Simulation Ball Shooter", "Reserved Solenoid 50",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class TorpedoAlleyDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
        cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
        cls.sources = {item["id"]: item for item in cls.definition["sources"]}

    def test_identity_generation_parent_and_bounds(self) -> None:
        self.assertEqual("data-east.torpedo-alley.1988", self.definition["machine"]["id"])
        self.assertEqual(
            {"platform": "pinmame.dataeast", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True},
            self.definition["controller"],
        )
        self.assertEqual(OWN_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
        parent = next(driver for driver in self.definition["drivers"] if driver["id"] == "torp_e21")
        clone = next(driver for driver in self.definition["drivers"] if driver["id"] == "torp_a16")
        self.assertNotIn("clone_of", parent)
        self.assertEqual("torp_e21", clone["clone_of"])
        self.assertEqual("Torpedo Alley (2.1 Europe)", parent["description"])
        self.assertEqual("Torpedo Alley (1.6)", clone["description"])
        self.assertTrue(all(driver["year"] == "1988" and driver["manufacturer"] == "Data East" for driver in self.definition["drivers"]))
        self.assertEqual(1000.0, self.definition["machine"]["playfield"]["width"])
        self.assertEqual(2000.0, self.definition["machine"]["playfield"]["height"])

    def test_data_east_controller_and_public_namespace_ranges(self) -> None:
        self.assertEqual("pinmame.dataeast", self.definition["controller"]["platform"])
        groups = {}
        for collection in (self.definition["inputs"],self.definition["outputs"]):
            for item in collection:
                groups.setdefault(item["binding"]["group"],set()).add(item["binding"]["device"])
        self.assertEqual({-7,-6}|set(range(1,65)),groups["pinmame.input.switch"])
        self.assertEqual({0},groups["pinmame.input.dip"])
        self.assertEqual(set(range(1,51)),groups["pinmame.output.solenoid"])
        self.assertEqual(set(range(1,65)),groups["pinmame.output.lamp"])
        diagnostics = {
            item["binding"]["device"] for item in self.definition["inputs"]
            if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] < 0
        }
        self.assertEqual({-7, -6}, diagnostics)
        self.assertNotIn(-5, diagnostics)
        self.assertNotIn(-4, diagnostics)

    def test_coverage_is_partial_and_fail_closed(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(
            ["output_semantics", "mechanism_behavior", "polarity", "recreation_notes", "spatial_placement", "unresolved_conflicts"],
            coverage["missing"],
        )
        self.assertEqual("validated", coverage["dimensions"]["address_enumeration"])
        self.assertEqual("conflicted", coverage["dimensions"]["mechanisms"])
        self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
        self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])

    def test_switch_namespace_is_complete_and_15_16_are_printed_eos(self) -> None:
        switches = {
            item["binding"]["device"]: item for item in self.definition["inputs"]
            if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] > 0
        }
        self.assertEqual(set(range(1, 65)), set(switches))
        for address, printed in enumerate(PRINTED_SWITCHES, start=1):
            item = switches[address]
            expected = SWITCH_LABEL_OVERRIDES.get(address, printed)
            self.assertEqual("unused" if printed is None else "used", item["availability"], address)
            self.assertEqual(f"Unused Switch {address}" if printed is None else expected, item["label"], address)
        self.assertEqual("Left Flipper EOS", switches[15]["label"])
        self.assertEqual("Right Flipper EOS", switches[16]["label"])
        self.assertTrue(all(switches[address]["provenance"]["status"] == "conflicted" for address in (15, 16, 23, 36)))
        self.assertIn("part 180-5026-00", switches[15]["physical"]["notes"])
        self.assertIn("does not star it as a cabinet switch", switches[16]["physical"]["notes"])
        self.assertEqual({11, 12, 13}, {address for address, item in switches.items() if item.get("initial_active") is True})
        cabinet = {address for address, item in switches.items() if any(role.startswith("cabinet.") for role in item.get("roles", []))}
        self.assertEqual({1, 3, 4, 5, 6, 7}, cabinet)

    def test_lamp_namespace_is_complete_but_binding_strength_is_conservative(self) -> None:
        lamps = {
            item["binding"]["device"]: item for item in self.definition["outputs"]
            if item["binding"]["group"] == "pinmame.output.lamp"
        }
        self.assertEqual(set(range(1, 65)), set(lamps))
        self.assertEqual(LAMPS, [lamps[address]["label"] for address in range(1, 65)])
        self.assertTrue(all(lamps[address]["spatial"]["status"] == "candidate" for address in range(1, 65)))
        self.assertTrue(all(len(lamps[address]["spatial"]["placements"]) == 1 for address in range(1, 65)))
        self.assertTrue(all("coordinate candidate, not an observed physical" in lamps[address]["physical"]["notes"] for address in range(1, 65)))
        self.assertEqual("conflicted", lamps[24]["provenance"]["status"])
        self.assertIn("whole-line commented", lamps[24]["physical"]["notes"])
        self.assertIn("shared VPM core", lamps[1]["physical"]["notes"])

    def test_solenoid_namespace_typing_mux_and_dispositions_are_explicit(self) -> None:
        solenoids = {
            item["binding"]["device"]: item for item in self.definition["outputs"]
            if item["binding"]["group"] == "pinmame.output.solenoid"
        }
        self.assertEqual(set(range(1, 51)), set(solenoids))
        self.assertEqual(SOLENOIDS, [solenoids[address]["label"] for address in range(1, 51)])
        self.assertTrue(all(solenoids[address]["kind"] == "flasher" for address in range(1, 10)))
        self.assertEqual("relay", solenoids[10]["kind"])
        self.assertEqual("gi", solenoids[11]["kind"])
        self.assertTrue(all(solenoids[address]["kind"] == "flasher" for address in (14, 15)))
        self.assertTrue(all(solenoids[address]["kind"] == "coil" for address in (16, 17, 18, 19, 21, 22)))
        self.assertTrue(all(solenoids[address]["kind"] == "coil" for address in (12, 13, 20)))
        self.assertTrue(all("quantity" not in solenoids[address]["physical"] for address in (12, 13, 20)))
        self.assertTrue(all(solenoids[address]["kind"] == "coil" for address in range(25, 33)))
        self.assertTrue(all(solenoids[address]["provenance"]["status"] == "conflicted" for address in set(range(1, 9)) | set(range(25, 33))))
        self.assertEqual({12, 13, 20, 24}, {address for address in range(1, 33) if solenoids[address]["availability"] == "unused"})
        self.assertTrue(all(solenoids[address]["availability"] == "unused" and solenoids[address]["kind"] == "virtual" for address in range(33, 45)))
        self.assertTrue(all(solenoids[address]["availability"] == "used" and solenoids[address]["kind"] == "virtual" for address in range(45, 49)))
        self.assertTrue(all(solenoids[address]["availability"] == "unused" and solenoids[address]["kind"] == "virtual" for address in (49, 50)))
        self.assertTrue(all("spatial" not in solenoids[address] for address in (7, 8, 11)))
        self.assertEqual(["playfield.general-illumination"], solenoids[11]["roles"])
        self.assertTrue(all(solenoids[address]["physical"]["quantity"] == 2 for address in range(1, 9)))
        self.assertTrue(all(len(solenoids[address]["spatial"]["placements"]) == 1 for address in range(1, 7)))
        self.assertTrue(all("spatial" not in solenoids[address] for address in (17, 18, 19, 21, 22)))
        self.assertEqual("not_applicable", solenoids[20]["spatial"]["status"])
        self.assertEqual("unused", solenoids[20]["spatial"]["reason"])
        self.assertEqual("internal_nonvisual", solenoids[23]["spatial"]["reason"])
        self.assertEqual("virtual", solenoids[24]["spatial"]["reason"])
        for address in range(45, 49):
            self.assertEqual("virtual", solenoids[address]["spatial"]["reason"], address)
            self.assertNotIn("quantity", solenoids[address]["physical"], address)
            self.assertNotIn("part_number", solenoids[address]["physical"], address)
            self.assertNotIn("wiring", solenoids[address], address)

    def test_display_topology_is_exactly_de_disp_alpha2(self) -> None:
        displays = self.definition["displays"]
        self.assertEqual([(0, 1, 7), (1, 9, 7), (2, 21, 7), (3, 29, 7)], [
            (item["controller_index"], item["segment_start"], item["width"]) for item in displays
        ])
        self.assertEqual(4, len(displays))
        self.assertTrue(all(item["spatial"]["status"] == "not_applicable" for item in displays))
        labels = " ".join(item["label"].casefold() for item in displays)
        self.assertNotIn("credit", labels)
        self.assertNotIn("ball-in-play", labels)

    def test_mechanism_topology_uses_runtime_causality_and_manual_construction(self) -> None:
        mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
        self.assertEqual(19, len(mechanisms))
        self.assertEqual(["coil.driver-31"], mechanisms["mechanism.outhole"]["actuators"])
        self.assertEqual(["coil.driver-16"], mechanisms["mechanism.ball-trough"]["actuators"])
        self.assertEqual(["switch.matrix-11", "switch.matrix-12", "switch.matrix-13"], mechanisms["mechanism.ball-trough"]["sensors"])
        self.assertEqual(["coil.driver-26"], mechanisms["mechanism.left-lock"]["actuators"])
        self.assertEqual(["switch.matrix-41", "switch.matrix-42"], mechanisms["mechanism.left-lock"]["sensors"])
        self.assertEqual(
            [["switch.matrix-42"], ["switch.matrix-41"]],
            [position["sensors"] for position in mechanisms["mechanism.left-lock"]["positions"]],
        )
        self.assertEqual(["coil.driver-28"], mechanisms["mechanism.center-lock"]["actuators"])
        self.assertEqual(
            [["switch.matrix-45"], ["switch.matrix-44"]],
            [position["sensors"] for position in mechanisms["mechanism.center-lock"]["positions"]],
        )
        self.assertEqual(["coil.driver-27"], mechanisms["mechanism.vertical-up-kicker"]["actuators"])
        self.assertEqual("500-5067-00", mechanisms["mechanism.vertical-up-kicker"]["assembly_part_number"])
        self.assertEqual(["coil.driver-32"], mechanisms["mechanism.ship-tilt"]["actuators"])
        self.assertEqual("500-5084-00", mechanisms["mechanism.ship-tilt"]["assembly_part_number"])
        self.assertIn("fourteen-step", mechanisms["mechanism.ship-tilt"]["behavior"])
        self.assertEqual(["coil.driver-47", "coil.driver-48"], mechanisms["mechanism.left-flipper"]["actuators"])
        self.assertEqual(["coil.driver-45", "coil.driver-46"], mechanisms["mechanism.right-flippers"]["actuators"])
        self.assertEqual(["coil.driver-19"], mechanisms["mechanism.left-pop-bumper"]["actuators"])
        self.assertEqual(["coil.driver-22"], mechanisms["mechanism.right-pop-bumper"]["actuators"])
        self.assertEqual(["coil.driver-17"], mechanisms["mechanism.center-pop-bumper"]["actuators"])
        self.assertEqual(["coil.driver-18"], mechanisms["mechanism.left-slingshot"]["actuators"])
        self.assertEqual(["coil.driver-21"], mechanisms["mechanism.right-slingshot"]["actuators"])

    def test_relay_relationships_cover_public_25_through_32(self) -> None:
        relationships = self.definition["relationships"]
        relay = [item for item in relationships if item["id"].startswith("relationship.lr-relay-")]
        special = [item for item in relationships if item["id"].startswith("relationship.special-")]
        self.assertEqual(13, len(relationships))
        self.assertEqual(8, len(relay))
        self.assertEqual({f"coil.driver-{address}" for address in range(25, 33)}, {item["destination"] for item in relay})
        self.assertTrue(all(item["source"] == "coil.driver-10" for item in relay))
        self.assertTrue(all(item["provenance"]["status"] == "validated" for item in relay))
        self.assertEqual({
            ("switch.matrix-49", "coil.driver-19"), ("switch.matrix-50", "coil.driver-22"),
            ("switch.matrix-51", "coil.driver-17"), ("switch.matrix-52", "coil.driver-18"),
            ("switch.matrix-53", "coil.driver-21"),
        }, {(item["source"], item["destination"]) for item in special})
        self.assertEqual({"conflicted", "validated"}, {item["provenance"]["status"] for item in special})

    def test_all_eight_conflicts_are_first_class(self) -> None:
        self.assertEqual({
            "conflict.left-flipper-eos-runtime", "conflict.right-flipper-eos-runtime",
            "conflict.mux-bank-output-typing", "conflict.special-solenoid-sp1-sp2-schematic-swap",
            "conflict.output-11-callback-overwrite", "conflict.switch-23-runtime-misroute",
            "conflict.switch-36-runtime-misroute", "conflict.lamp-24-runtime-omission",
        }, {item["id"] for item in self.definition["conflicts"]})
        self.assertTrue(all(len(item["source_refs"]) >= 2 for item in self.definition["conflicts"]))

    def test_spatial_report_asserts_1000_by_2000_and_lists_projection_classes(self) -> None:
        report = load_json(REPORT_PATH)
        self.assertEqual({"left": 0.0, "top": 0.0, "right": 1000.0, "bottom": 2000.0}, report["coordinate_system"]["raw_bounds"])
        self.assertEqual("x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top)", report["coordinate_system"]["normalization"])
        placements = []
        for collection in (self.definition["inputs"], self.definition["outputs"]):
            for item in collection:
                placements.extend(item.get("spatial", {}).get("placements", []))
        self.assertTrue(placements)
        self.assertTrue(all(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1 for item in placements))
        self.assertEqual(114, len(report["resolved"]))
        self.assertEqual(4, len(report["unresolved"]))
        origins = report["coordinate_origins"]
        self.assertEqual((99, 18, 17, 1), (
            origins["measured_center"], origins["computed_centroid"],
            origins["drag_point_centroid"], origins["object_group_centroid"],
        ))
        self.assertEqual(origins["computed_centroid"], len(origins["computed_devices"]))
        resolved = {item["id"]: item for item in report["resolved"]}
        self.assertTrue(all(resolved[device]["status"] == "candidate" for device in origins["computed_devices"]))
        classes = {item["class"]: item for item in report["projection_classes"]}
        self.assertEqual(17, len(classes["drag-point-centroid"]["devices"]))
        self.assertEqual({"coil.driver-29"}, set(classes["object-group-centroid"]["devices"]))
        self.assertEqual({f"coil.driver-{address}" for address in range(1, 9)}, set(classes["physical-quantity-exceeds-effect-placement-count"]["devices"]))
        self.assertEqual({f"lamp.matrix-{address}" for address in (1, 8, 16, 23, 24, 31, 32)}, set(classes["physical-lamp-quantity-exceeds-placement-count"]["devices"]))
        quantity_gap = next(item for item in report["unresolved"] if item["dimension"] == "flasher_socket_quantity_placement")
        self.assertEqual({f"coil.driver-{address}" for address in range(1, 9)}, set(quantity_gap["devices"]))
        markdown = REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
        self.assertIn("x: `raw_x / 1000`", markdown)
        self.assertIn("y: `raw_y / 2000`", markdown)
        self.assertIn("## Coordinate origins", markdown)
        self.assertIn("Computed centroids: 18 (17 drag-point; 1 object-group)", markdown)
        self.assertIn("## Explicit projection classes", markdown)
        self.assertIn("Keep partial", markdown)

    def test_scope_and_gi_do_not_publish_misleading_spatial_records(self) -> None:
        outputs = {item["id"]: item for item in self.definition["outputs"]}
        self.assertNotIn("spatial", outputs["coil.driver-7"])
        self.assertNotIn("spatial", outputs["coil.driver-11"])
        report = load_json(REPORT_PATH)
        excluded = report["excluded_helpers"]
        self.assertIn("two widely separated clusters", excluded["scope_flasher_group"])
        self.assertNotIn("coil.driver-7", report["coordinate_origins"]["computed_devices"])

    def test_evidence_excerpts_hash_and_preserve_literal_cells(self) -> None:
        excerpts = self.sources["manual.data-east.torpedo-alley.1988"]["excerpts"]
        self.assertEqual(4, len(excerpts))
        for excerpt in excerpts:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertEqual("manual", excerpt["method"])
            self.assertTrue(excerpt["reviewed"])
        switch = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
        lamp = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
        coil = (EXCERPT_ROOT / "coil-and-flipper.md").read_text(encoding="utf-8")
        parts = (EXCERPT_ROOT / "mechanism-parts.md").read_text(encoding="utf-8")
        self.assertIn("| 15 | GRN-RED | WHT-VIO | Left EOS | Left EOS |", switch)
        self.assertIn("| 16 | GRN-RED | WHT-GRY | Right EOS | Right EOS |", switch)
        self.assertIn("part `180-5026-00`", switch)
        self.assertIn("| 16 | YEL-RED | RED-GRY | Insert 2 Torpedo (2) | Insert 2 Torpedo |", lamp)
        self.assertIn("| 24 | YEL-ORN | RED-GRY | Insert 1 Torpedo (2) | Insert 1 Torpedo (2) |", lamp)
        self.assertIn("RED-ORG", lamp)
        self.assertIn("| SP3 | Left Slingsho |", coil)
        self.assertIn("| 01L | Destroyer Hotdog | GRY-BRN | VIO-GRN | BRN (+32 V) | Q46 | #906 | 2 |", coil)
        self.assertIn("every 01L-08L branch with `(2)`", coil)
        self.assertIn("01L and 05L both print device wire `VIO-GRN`", coil)
        self.assertIn("SP1 and SP4 both print trigger wire `ORN-BRN`", coil)
        self.assertIn("SP2 prints connector prefix `CPN CN18-3`", coil)
        self.assertNotIn("| 17 | SP1 |", coil)
        self.assertIn("The L/R and SP printed numbers above are manual aliases only", coil)
        self.assertIn("SP2 `CENTER THUMPER BUMPER` and SP1 `RIGHT THUMPER BUMPER`", coil)
        self.assertIn("`500-5084-00 Ship. Tilt Assembly`", parts)
        self.assertIn("`500-5067-00 Vertical Up Kicker`", parts)

    def test_manifest_canonical_digest_and_shape(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(2111, manifest["file_count"])
        self.assertEqual(156_444_993, manifest["total_bytes"])
        self.assertEqual(2111, len(manifest["files"]))
        algorithm = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
        self.assertEqual(algorithm, manifest["manifest_algorithm"])
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("6ba07f0ac3d1e9e2bb1e441dde4066d99033bf5e7b11b81337708b16d1afe92e", manifest["manifest_sha256"])
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
        self.assertIn(f"algorithm: {algorithm}", self.sources["vpx-extraction.torpedo-alley-hybrid-mod-1-1"]["locator"])

    def test_catalog_reassigns_both_drivers_and_removes_stub_normally(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        records = {item["id"]: item for item in catalog["drivers"]}
        for driver_id in OWN_DRIVERS:
            self.assertEqual("data-east.torpedo-alley.1988", records[driver_id]["machine_id"])
            self.assertEqual("machines/partial/data-east/torpedo-alley-1988.json", records[driver_id]["definition"])
            self.assertEqual("partial", records[driver_id]["coverage_status"])
        self.assertFalse((ROOT / "machines" / "stubs" / "torp_e21.json").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "torp_e21.md").exists())
        self.assertFalse((ROOT / "machines" / "stubs" / "torp_e21.json.disabled").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "torp_e21.md.disabled").exists())

    def test_dynamic_contamination_guard_is_catalog_derived(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        artifact_paths = [DEFINITION_PATH, SEED_PATH, REPORT_PATH, REPORT_MARKDOWN_PATH, KNOWLEDGE_PATH]
        artifact_text = "\n".join(path.read_text(encoding="utf-8").casefold() for path in artifact_paths)
        identifier_tokens = set(re.findall(r'["`]([a-z0-9_]+)["`]', artifact_text))
        machine_tokens = set(re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)+", artifact_text))
        other_driver_ids = {
            value.casefold() for item in catalog["drivers"] for value in (item["id"], item.get("root_driver"))
            if isinstance(value, str) and value not in OWN_DRIVERS
        }
        self.assertEqual(set(), identifier_tokens & other_driver_ids)
        other_machine_ids = {item["id"].casefold() for item in catalog["machines"] if item["id"] != "data-east.torpedo-alley.1988"}
        self.assertEqual(set(), machine_tokens & other_machine_ids)

        own_locator = self.sources["pinmame.core.4ec52ff0ac13"]["locator"]
        for fragment in ("lines 714-715", "737-738", "746-747", "SP6, SP5, SP2, SP3, SP1, and SP4"):
            self.assertIn(fragment, own_locator)
        own_generations = set(re.findall(r"\bGEN_[A-Z0-9_]+\b", own_locator))
        self.assertEqual({"GEN_DE"}, own_generations)
        foreign_generations: set[str] = set()
        foreign_hardware: set[str] = set()
        foreign_tables: set[str] = set()
        for machine in catalog["machines"]:
            if machine["id"] == "data-east.torpedo-alley.1988":
                continue
            path = ROOT / machine["definition"]
            if not path.is_file():
                continue
            other = load_json(path)
            other_text = path.read_text(encoding="utf-8")
            knowledge_path = other.get("knowledge", {}).get("path")
            if isinstance(knowledge_path, str) and (ROOT / knowledge_path).is_file():
                other_text += "\n" + (ROOT / knowledge_path).read_text(encoding="utf-8")
            foreign_generations.update(re.findall(r"\bGEN_[A-Z0-9_]+\b", other_text))
            hardware = other.get("controller", {}).get("hardware_generation")
            if isinstance(hardware, str) and hardware != self.definition["controller"]["hardware_generation"]:
                foreign_hardware.add(hardware.casefold())
            for source in other.get("sources", []):
                if source.get("kind") != "vpx_table":
                    continue
                for key in ("id", "original_filename", "source_id", "sha256"):
                    value = source.get(key)
                    if isinstance(value, str) and len(value) >= 8:
                        foreign_tables.add(value.casefold())
        artifact_upper = artifact_text.upper()
        self.assertEqual(set(), {token for token in foreign_generations - own_generations if token in artifact_upper})
        self.assertEqual(set(), foreign_hardware & set(re.findall(r"\b0x[0-9a-f]+\b", artifact_text)))
        self.assertEqual(set(), {value for value in foreign_tables if value in artifact_text})
        own_table = self.sources["vpx-table.torpedo-alley-hybrid-mod-1-1"]
        self.assertEqual("Torpedo Alley (Data East 1988) Physics Sound Hybrid MOD 1.1.vpx", own_table["original_filename"])
        self.assertEqual("f876db907452c59da2e6589536ab9df19945a91f06dc6d5e32f6e679e3ac2472", own_table["sha256"])

    def test_seed_is_byte_identical_and_knowledge_names_concrete_blockers(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("sampled_characters=76035", self.sources["manual.data-east.torpedo-alley.1988"]["locator"])
        self.assertIn("exactly 64 Light objects named `L1` through `L64`", knowledge)
        self.assertIn("shared VPM core loaded through DE.VBS", knowledge)
        self.assertIn("left=0 top=0 right=1000 bottom=2000", knowledge)
        self.assertIn("record remains partial", knowledge)
        self.assertIn("Public 17, 18, 19, 21 and 22 are the five fitted switch-triggered coils; public 20 is the unfitted SP6 slot", knowledge)
        self.assertNotIn("Outputs 17-21 are the five fitted switch-triggered coils; 22 is SP6 Not Used", knowledge)
        self.assertIn("17=SP1, 22=SP2, 18=SP3, 19=SP4, 21=SP5 and 20=SP6", knowledge)
        self.assertIn("archive/IPDB metadata is intentionally not asserted", knowledge)
        self.assertNotIn("ipdb_id", self.definition["machine"])
        self.assertEqual("https://github.com/vpinball/pinmame", self.sources["pinmame.core.4ec52ff0ac13"]["uri"])
        self.assertEqual("external:pinmame-vpx-sources/data-east/torpedo-alley-1988/vpxtool-extract/script.vbs", self.sources["vpx-script.torpedo-alley-hybrid-mod-1-1"]["uri"])
        self.assertEqual("external:pinmame-manuals/by-machine/data-east.torpedo-alley.1988/contributor-supplied/Data_East_1988_Torpedo_Alley_Manual_English.pdf", self.sources["manual.data-east.torpedo-alley.1988"]["uri"])


class TorpedoAlleyCuratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "tools"))
        import curate_torpedo_alley
        cls.curator = curate_torpedo_alley

    def test_check_is_clean_and_crlf_tolerant_but_not_reformat_tolerant(self) -> None:
        self.curator._check(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            target_root = Path(scratch)
            for path, _payload in self.curator._artifacts(ROOT):
                target = target_root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            self.curator._check(target_root)
            definition = target_root / DEFINITION_PATH.relative_to(ROOT)
            definition.write_text(json.dumps(load_json(definition), indent=4, sort_keys=True) + "\n", encoding="utf-8", newline="")
            with self.assertRaises(RuntimeError):
                self.curator._check(target_root)

    def test_special_solenoid_mapping_is_derived_from_pia_comments_and_offsets(self) -> None:
        derived = {17 + self.curator._SPECIAL_DE_PERMUTATION[handler]: printed for handler, printed in self.curator._SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
        self.assertEqual({17:"SP1",18:"SP3",19:"SP4",20:"SP6",21:"SP5",22:"SP2"}, derived)
        self.assertEqual(derived, self.curator._SPECIAL_PUBLIC_TO_PRINTED)

    def test_regenerator_refuses_existing_author_ready_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            target = root / "machines" / "author-ready" / "data-east" / "torpedo-alley-1988.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                self.curator._write(root)


class TorpedoAlleyExternalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vpx_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) if os.environ.get("PINMAME_VPX_SOURCES_ROOT") else None
        cls.manual_anchor = Path(os.environ["PINMAME_MANUALS_ROOT"]) if os.environ.get("PINMAME_MANUALS_ROOT") else None

    def test_exact_retained_table_script_lamp_idiom_and_bounds(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        base = self.vpx_root / "data-east" / "torpedo-alley-1988"
        extraction = base / "vpxtool-extract"
        table = base / "Torpedo Alley (Data East 1988) Physics Sound Hybrid MOD 1.1.vpx"
        self.assertEqual("f876db907452c59da2e6589536ab9df19945a91f06dc6d5e32f6e679e3ac2472", sha256(table))
        self.assertEqual("5123b70af3dcfaba40f19ee4f941111621b35e24707dc7f461e76c0514fea61b", sha256(extraction / "script.vbs"))
        script = (extraction / "script.vbs").read_text(encoding="utf-8")
        self.assertIn('Const cGameName="torp_e21",UseSolenoids=2,UseLamps=1,UseSync=0,UseGI=0', script)
        active = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("'"))
        self.assertNotRegex(active, r"Lampz\.MassAssign|vpmMapLights|\bSetLamp\b|LampCallback|UpdateLamps|AllLamps")
        assigned = {int(value) for value in re.findall(r"Lights\((\d+)\)\s*=", active, re.I)}
        self.assertEqual(set(range(1, 65)) - {24}, assigned)
        self.assertRegex(script, r"(?mi)^\s*'\s*Set\s+Lights\(24\)\s*=")
        self.assertRegex(active, r"(?i)SW23_hit\(\).*PulseSw\s+18")
        self.assertRegex(active, r"(?i)SW36_hit\(\).*PulseSw\s+26")
        light_names = []
        for path in (extraction / "gameitems").glob("*.json"):
            outer = load_json(path)
            kind, item = next(iter(outer.items()))
            if kind == "Light" and re.fullmatch(r"L([1-9]|[1-5][0-9]|6[0-4])", item.get("name", "")):
                light_names.append(item["name"])
        self.assertEqual({f"L{address}" for address in range(1, 65)}, set(light_names))
        table_json = load_json(extraction / "gamedata.json")
        self.assertEqual((0.0, 0.0, 1000.0, 2000.0), tuple(float(table_json[key]) for key in ("left", "top", "right", "bottom")))

    def test_extraction_manifest_recomputes_every_file(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.vpx_root / "data-east" / "torpedo-alley-1988" / "vpxtool-extract"
        manifest = load_json(MANIFEST_PATH)
        actual = [path.relative_to(extraction).as_posix() for path in sorted(path for path in extraction.rglob("*") if path.is_file())]
        self.assertEqual(actual, [entry["path"] for entry in manifest["files"]])
        for entry in manifest["files"]:
            path = extraction / entry["path"]
            self.assertEqual(entry["bytes"], path.stat().st_size, entry["path"])
            self.assertEqual(entry["sha256"], sha256(path), entry["path"])

    def test_exact_manual_hashes_via_supplied_anchor(self) -> None:
        if self.manual_anchor is None:
            self.skipTest("retained manuals are not available")
        roots = [
            self.manual_anchor / "by-machine" / "data-east.torpedo-alley.1988" / "contributor-supplied",
            self.manual_anchor.parent / "manual-cache" / "by-machine" / "data-east.torpedo-alley.1988" / "contributor-supplied",
        ]
        root = next((path for path in roots if path.is_dir()), None)
        self.assertIsNotNone(root, roots)
        manual = root / "Data_East_1988_Torpedo_Alley_Manual_English.pdf"
        self.assertEqual(8_924_940, manual.stat().st_size)
        self.assertEqual("63ca7a98a303713487318c1f1d8ee77cc8b9ba37b20c918aa51e469e5aee5960", sha256(manual))
        hashes = load_json(root / "hashes.json")[manual.name]
        self.assertEqual(68, hashes["page_count"])
        self.assertEqual(76035, hashes["sampled_characters"])


if __name__ == "__main__":
    unittest.main()
