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
DEFINITION_PATH = ROOT / "machines" / "partial" / "data-east" / "secret-service-1988.json"
SEED_PATH = ROOT / "tools" / "seeds" / "data-east" / "secret-service-1988.json"
MANIFEST_PATH = ROOT / "tools" / "seeds" / "data-east" / "secret-service-1988-extraction-manifest.json"
REPORT_PATH = ROOT / "reports" / "spatial" / "data-east" / "secret-service-1988.json"
REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "data-east" / "secret-service-1988.md"
KNOWLEDGE_PATH = ROOT / "knowledge" / "data-east" / "secret-service-1988.md"
INSTRUCTIONS_PATH = ROOT / "docs" / "INSTRUCTIONS.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.secret-service.1988"
DATA_EAST_CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "data-east.json"
OWN_DRIVERS = {"ssvc_a26", "ssvc_b26", "ssvc_e40", "ssvc_a42"}


SWITCH_FIXTURE = [
    "Plumb Tilt", None, "Credits Button", "Right Coin", "Center Coin", "Left Coin", "Slam Tilt", None,
    "Shooter Lane", "Bullet Target", "Eater 1 (KGB Hideout)", "Eater 2 (KGB Hideout)",
    "Eater Target (KGB Hideout)", "Target 1", "Target 2", "Target 3", "Right Spinner", "Top 310 Point",
    "Top Right Eject", "Red Pop Bumper", "Clear Pop Bumper", "Blue Pop Bumper", "S Lane", "P Lane",
    "Y Lane", "Left Spinner", "Left 310 Point", "Left Slingshot", "Right Slingshot", "Left Flipper EOS",
    "Right Flipper EOS", "Laser Kickback", "Left Return", "Right Return", "Right Outlane", "Drop 1",
    "Drop 2", "Drop 3", "Drop 4", "Drop 5", "Kickbig 1 (Whitehouse)", "Kickbig 2 (Whitehouse)",
    "Top Left Switch (Ramp)", "Top Right Switch (Ramp)", "310 Point Behind Drops", "Outhole",
    "Trough 1", "Trough 2", "Trough 3", "Star Rollover", None, "Up Post",
    None, None, None, None, None, None, None, None, None, None, None, None,
]

LAMP_FIXTURE = [
    "Spy Again", "White House #2", "Russian Embassy #2", "Jefferson Memorial #1 (Jackpot)",
    "Jefferson Memorial #1 (Jackpot)", '"S" Lane', '"P" Lane', '"Y" Lane', "Left Red Arrow",
    "Left Red Circle", "Center Red Circle", "Right Red Circle", "Right Red Arrow",
    "Russian Embassy Green? Shield", "Russian Embassy Yellow Shield", "Russian Embassy Clear Shield",
    "Left Clear Arrow", "Left Clear Circle", "Center Clear Circle", "Right Clear Circle", "Right Clear Arrow",
    "All Scores Double", "Bonus Held", "Up Post", "Left Blue Arrow", "Left Blue Circle", "Center Blue Circle",
    "Right Blue Circle", "Right Blue Arrow", "Super Arrow", "Left Spinner", "Right Spinner", "5-Bank Arrow 1",
    "5-Bank Arrow 2", "5-Bank Arrow 3", "5-Bank Arrow 4", "5-Bank Arrow 5", "Bullet Target",
    "Hotline (White House)", "Eject Green Shield", "5-Bank Green Shield", "5-Bank Orange Shield",
    "5-Bank Amber Shield", "5-Bank Clear Shield", "Eject Red Arrow", "Eject Clear Arrow", "Eject Blue Arrow",
    "Eject Amber Shield", "Laser Kickback", "Left Outlane Special", "Left Return Lane", "Right Return Lane",
    "Right Outlane Special", "1K Bonus", "2K Bonus", "4K Bonus", "8K Bonus", "16K Bonus", "32K Bonus",
    "64K Bonus", "2X", "3X", "4X", "5X",
]

COIL_FIXTURE = {
    1: "Top Left Red Hotdog / Left Red Marquee", 2: "Top Left Yellow Hotdog / Left Yellow Marquee",
    3: "Blue Mars (backstop) / Blue Marquee", 4: "Top Right Yellow Hotdog / Right Yellow Marquee",
    5: "Top Right Red Hotdog / Right Red Marquee", 6: "White House / Backglass (2)",
    7: "Russian Embassy / Backglass (2)", 8: "Shield, Clear Mars (backstop)",
    9: "KGB Hideout / Music Credits (Speaker panel)", 10: "Left/Right Coil Relay",
    11: "General Illumination Relay", 12: "2 Spies (Backglass)", 13: "Secret Service (Backglass)",
    14: "Post", 15: "Laser Kickback relay and coil", 16: "Kickbig relay and coil",
    17: "Red Pop Bumper", 18: "Clear Pop Bumper", 19: "Blue Pop Bumper",
    20: "Left Slingshot", 21: "Right Slingshot", 25: "Ball Eater Down", 26: "Outhole",
    27: "Eject Hole", 28: "5-Bank Reset", 30: "Ball Eater Up", 31: "Knocker", 32: "Trough",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class SecretServiceDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
        cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
        cls.sources = {item["id"]: item for item in cls.definition["sources"]}

    def test_identity_generation_and_four_driver_tree(self) -> None:
        self.assertEqual("data-east.secret-service.1988", self.definition["machine"]["id"])
        self.assertEqual(
            {"platform": "pinmame.dataeast", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True},
            self.definition["controller"],
        )
        self.assertEqual(OWN_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
        root = next(driver for driver in self.definition["drivers"] if driver["id"] == "ssvc_a26")
        self.assertNotIn("clone_of", root)
        self.assertEqual(OWN_DRIVERS - {"ssvc_a26"}, {driver["id"] for driver in self.definition["drivers"] if driver.get("clone_of") == "ssvc_a26"})
        self.assertTrue(all(driver["year"] == "1988" and driver["manufacturer"] == "Data East" for driver in self.definition["drivers"]))
        self.assertEqual(952.0, self.definition["machine"]["playfield"]["width"])
        self.assertEqual(2162.0, self.definition["machine"]["playfield"]["height"])

    def test_data_east_controller_is_not_borrowed_from_system_11(self) -> None:
        self.assertTrue(DATA_EAST_CONTROLLER_PATH.exists())
        self.assertEqual("pinmame.dataeast", load_json(DATA_EAST_CONTROLLER_PATH)["id"])
        self.assertEqual("pinmame.dataeast", self.definition["controller"]["platform"])
        self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
        self.assertNotIn("controller_platform", self.definition["coverage"]["missing"])
        diagnostics = {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] < 0}
        self.assertEqual({-7, -6}, diagnostics)
        self.assertNotIn(-5, diagnostics)
        self.assertNotIn(-4, diagnostics)

    def test_coverage_is_partial_and_fail_closed(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(
            ["output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"],
            coverage["missing"],
        )
        self.assertNotIn("controller_platform", coverage["dimensions"])
        self.assertEqual("conflicted", coverage["dimensions"]["semantic_naming"])
        self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
        self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])

    def test_switch_namespace_is_complete_and_flippers_are_eos_contacts(self) -> None:
        switches = {
            item["binding"]["device"]: item for item in self.definition["inputs"]
            if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] > 0
        }
        self.assertEqual(set(range(1, 65)), set(switches))
        for address, expected in enumerate(SWITCH_FIXTURE, start=1):
            item = switches[address]
            self.assertEqual("unused" if expected is None else "used", item["availability"], address)
            self.assertEqual(f"Unused Switch {address}" if expected is None else expected, item["label"], address)
        self.assertEqual("Left Flipper EOS", switches[30]["label"])
        self.assertEqual("Right Flipper EOS", switches[31]["label"])
        self.assertEqual("conflicted", switches[30]["provenance"]["status"])
        self.assertEqual("conflicted", switches[31]["provenance"]["status"])
        self.assertEqual({12, 47, 48, 49, 52}, {address for address, item in switches.items() if item.get("initial_active") is True})

    def test_lamp_namespace_uses_custom_object_name_candidates(self) -> None:
        lamps = {
            item["binding"]["device"]: item for item in self.definition["outputs"]
            if item["binding"]["group"] == "pinmame.output.lamp"
        }
        self.assertEqual(set(range(1, 65)), set(lamps))
        self.assertEqual(LAMP_FIXTURE, [lamps[address]["label"] for address in range(1, 65)])
        self.assertTrue(all(lamps[address]["spatial"]["status"] == "candidate" for address in range(1, 65)))
        self.assertTrue(all(len(lamps[address]["spatial"]["placements"]) == 1 for address in range(1, 65)))
        self.assertTrue(all("object-name candidate" in lamps[address]["physical"]["notes"] for address in range(1, 65)))

    def test_solenoid_namespace_and_machine_specific_typing_are_explicit(self) -> None:
        solenoids = {
            item["binding"]["device"]: item for item in self.definition["outputs"]
            if item["binding"]["group"] == "pinmame.output.solenoid"
        }
        self.assertEqual(set(range(1, 51)), set(solenoids))
        for address, label in COIL_FIXTURE.items():
            self.assertEqual(label, solenoids[address]["label"], address)
        self.assertTrue(all(solenoids[address]["kind"] == "flasher" for address in range(1, 9)))
        self.assertEqual("flasher", solenoids[9]["kind"])
        self.assertEqual("gi", solenoids[11]["kind"])
        self.assertTrue(all(solenoids[address]["kind"] == "coil" for address in (25, 26, 27, 28, 30, 31, 32)))
        self.assertEqual("unused", solenoids[22]["availability"])
        self.assertEqual("unused", solenoids[29]["availability"])
        self.assertTrue(all(solenoids[address]["kind"] == "coil" for address in (22, 29)))
        self.assertTrue(all(solenoids[address]["spatial"]["reason"] == "unused" for address in (22, 29)))
        self.assertEqual({17: "SP1", 18: "SP2", 19: "SP3", 20: "SP4", 21: "SP5", 22: "SP6"}, {
            address: next(alias["value"] for alias in solenoids[address]["aliases"] if alias["namespace"] == "manual.coil-number")
            for address in range(17, 23)
        })
        self.assertEqual({17: "Q11", 18: "Q9", 19: "Q8", 20: "Q10", 21: "Q12", 22: "Q13"}, {
            address: solenoids[address]["wiring"]["driver_transistor"] for address in range(17, 23)
        })
        self.assertEqual(1, solenoids[10]["physical"]["quantity"])
        self.assertEqual(1, solenoids[11]["physical"]["quantity"])
        self.assertEqual(2, solenoids[9]["physical"]["quantity"])
        self.assertTrue(all(solenoids[address]["physical"]["quantity"] == 2 for address in range(1, 9)))
        self.assertTrue(all(solenoids[address]["physical"]["quantity"] == 1 for address in (17, 18, 19, 20, 21)))
        self.assertNotIn("quantity", solenoids[22]["physical"])
        self.assertTrue(all(solenoids[address]["provenance"]["status"] == "conflicted" for address in range(17, 23)))
        self.assertIn("Table prints Q8", solenoids[17]["physical"]["notes"])
        self.assertIn("schematics assign SP1 to Q11", solenoids[17]["physical"]["notes"])
        self.assertEqual("internal_nonvisual", solenoids[23]["spatial"]["reason"])
        self.assertEqual("virtual", solenoids[24]["spatial"]["reason"])
        virtual_addresses = {address for address, item in solenoids.items() if item["kind"] == "virtual"}
        self.assertEqual({24, *range(33, 51)}, virtual_addresses)
        for address in range(45, 49):
            self.assertEqual("used", solenoids[address]["availability"])
            self.assertEqual("virtual", solenoids[address]["spatial"]["reason"])
            self.assertNotIn("quantity", solenoids[address]["physical"])
            self.assertNotIn("wiring", solenoids[address])
        emulator_only_addresses = virtual_addresses - set(range(45, 49))
        self.assertTrue(all(
            all(source_ref != "manual.data-east.secret-service.1988"
                for source_ref in solenoids[address]["provenance"]["source_refs"])
            and all(alias["namespace"] != "manual.coil-number" for alias in solenoids[address]["aliases"])
            for address in emulator_only_addresses
        ))
        self.assertTrue(all(solenoids[address]["provenance"]["status"] == "conflicted" for address in set(range(1, 9)) | set(range(25, 33))))
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("types only output 9 and muxed public 25-32 as #89 bulbs", knowledge)
        self.assertIn("GI at 11, and K1 at 10", knowledge)
        self.assertIn("Playboy, Time Machine, and Torpedo Alley definitions", knowledge)
        instructions = INSTRUCTIONS_PATH.read_text(encoding="utf-8")
        self.assertIn("Preserve only identities actually printed by the cited source", instructions)
        self.assertIn("never manufacture SP1-SP6 aliases from sequential public numbers", instructions)
        self.assertIn("every affected binding must stay conflicted and require a LibPinMAME trace before resolution", instructions)

    def test_display_topology_is_exactly_de_disp_alpha2(self) -> None:
        layout = [(item["controller_index"], item["segment_start"], item["width"]) for item in self.definition["displays"]]
        self.assertEqual([(0, 1, 7), (1, 9, 7), (2, 21, 7), (3, 29, 7)], layout)
        self.assertEqual(4, len(self.definition["displays"]))
        self.assertTrue(all(item["spatial"]["status"] == "not_applicable" and item["spatial"]["reason"] == "cabinet_or_service" for item in self.definition["displays"]))
        labels = " ".join(item["label"].casefold() for item in self.definition["displays"])
        self.assertNotIn("credit", labels)
        self.assertNotIn("ball-in-play", labels)

    def test_mechanism_topology_comes_from_script_causality(self) -> None:
        mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
        self.assertEqual(["coil.driver-32"], mechanisms["mechanism.ball-trough"]["actuators"])
        self.assertEqual(["switch.matrix-47", "switch.matrix-48", "switch.matrix-49"], mechanisms["mechanism.ball-trough"]["sensors"])
        self.assertEqual(["coil.driver-26"], mechanisms["mechanism.outhole"]["actuators"])
        self.assertEqual(["coil.driver-25", "coil.driver-30"], mechanisms["mechanism.kgb-eater"]["actuators"])
        self.assertEqual(["coil.driver-16"], mechanisms["mechanism.whitehouse-lock"]["actuators"])
        self.assertEqual(["coil.driver-45", "coil.driver-46"], mechanisms["mechanism.right-flipper-pair"]["actuators"])
        self.assertEqual(["coil.driver-20"], mechanisms["mechanism.left-slingshot"]["actuators"])
        self.assertEqual(["coil.driver-21"], mechanisms["mechanism.right-slingshot"]["actuators"])
        self.assertEqual(["coil.driver-17"], mechanisms["mechanism.red-pop-bumper"]["actuators"])
        self.assertEqual(["coil.driver-18"], mechanisms["mechanism.clear-pop-bumper"]["actuators"])
        self.assertEqual("conflicted", mechanisms["mechanism.clear-pop-bumper"]["provenance"]["status"])
        self.assertEqual(["coil.driver-19"], mechanisms["mechanism.blue-pop-bumper"]["actuators"])

    def test_relay_relationships_cover_public_25_through_32(self) -> None:
        self.assertEqual(8, len(self.definition["relationships"]))
        self.assertEqual({f"coil.driver-{address}" for address in range(25, 33)}, {item["destination"] for item in self.definition["relationships"]})
        self.assertTrue(all(item["source"] == "coil.driver-10" and item["provenance"]["status"] == "conflicted" for item in self.definition["relationships"]))

    def test_all_ten_conflicts_are_first_class(self) -> None:
        self.assertEqual({
            "conflict.switch-score-labels-matrix-vs-list", "conflict.left-flipper-eos-runtime",
            "conflict.right-flipper-eos-runtime", "conflict.lamp-matrix-vs-description-list",
            "conflict.mux-bank-output-typing", "conflict.right-flipper-power-wire",
            "conflict.output-13-description",
            "conflict.special-solenoid-public-mapping", "conflict.special-coil-driver-transistors",
            "conflict.synthetic-flipper-public-state",
        }, {item["id"] for item in self.definition["conflicts"]})
        self.assertTrue(all(len(item["source_refs"]) >= 2 for item in self.definition["conflicts"]))
        right_wire = next(item for item in self.definition["conflicts"] if item["id"] == "conflict.right-flipper-power-wire")
        self.assertEqual("/mechanisms/mechanism.right-flipper-pair", right_wire["path"])
        self.assertEqual(["manual.data-east.secret-service.1988", "human-review.secret-service-production-renders"], right_wire["source_refs"])
        self.assertIn("production playfield wiring diagram labels CN3 pin 6 BLU-YEL", right_wire["description"])
        self.assertNotIn("manual.data-east.secret-service.1988-preliminary", right_wire["source_refs"])

    def test_spatial_report_uses_952_bounds_and_names_every_projection(self) -> None:
        report = load_json(REPORT_PATH)
        self.assertEqual({"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2162.0}, report["coordinate_system"]["raw_bounds"])
        self.assertEqual("x=(raw_x-left)/(right-left); y=(raw_y-top)/(bottom-top)", report["coordinate_system"]["normalization"])
        placements = []
        for collection in (self.definition["inputs"], self.definition["outputs"]):
            for item in collection:
                placements.extend(item.get("spatial", {}).get("placements", []))
        self.assertTrue(placements)
        self.assertTrue(all(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1 for item in placements))
        self.assertNotIn("spatial", self.inputs["switch.matrix-27"])
        self.assertNotIn("spatial", self.outputs["coil.driver-11"])
        for output_id in ("coil.driver-6", "coil.driver-7", "coil.driver-9", "coil.driver-13"):
            self.assertNotIn("spatial", self.outputs[output_id], output_id)
        self.assertEqual(2, len(self.outputs["coil.driver-3"]["spatial"]["placements"]))
        markdown = REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
        self.assertIn("x: `raw_x / 952`", markdown)
        self.assertIn("## Explicit projection classes", markdown)
        self.assertIn("Keep partial", markdown)
        blockers = {item["dimension"]: item for item in report["blockers"]}
        self.assertNotIn("controller_platform", blockers)
        output_gap = next(item for item in report["unresolved"] if item["dimension"] == "output_placement")
        for output_id in ("coil.driver-6", "coil.driver-7", "coil.driver-9", "coil.driver-13"):
            self.assertIn(output_id, output_gap["devices"])
            self.assertIn(output_id, blockers["spatial_placement"]["devices"])

    def test_evidence_excerpts_exist_hash_and_preserve_literal_cells(self) -> None:
        excerpts = self.sources["manual.data-east.secret-service.1988"]["excerpts"]
        self.assertEqual(10, len(excerpts))
        for excerpt in excerpts:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertEqual("manual", excerpt["method"])
            self.assertTrue(excerpt["reviewed"])
        schematic_excerpts = [excerpt for excerpt in excerpts if excerpt["path"].endswith("production-schematics.md")]
        self.assertEqual({
            "excerpt.secret-service.cabinet-flipper-switches", "excerpt.secret-service.special-coil-circuits",
            "excerpt.secret-service.flipper-power-circuits", "excerpt.secret-service.lr-driver-banks",
            "excerpt.secret-service.switch-wiring", "excerpt.secret-service.lamp-gi-wiring",
        }, {excerpt["id"] for excerpt in schematic_excerpts})
        for excerpt in schematic_excerpts:
            image = ROOT / excerpt["image"]
            self.assertTrue(image.is_file(), image)
            self.assertEqual(excerpt["image_sha256"], sha256(image), excerpt["id"])
            self.assertLessEqual(image.stat().st_size, 100_000, excerpt["id"])
            self.assertIn("rotated 90 degrees counter-clockwise", excerpt["image_derivation"])
        for source_id in ("pinmame.catalog.4ec52ff0ac13", "pinmame.core.4ec52ff0ac13"):
            source = self.sources[source_id]
            self.assertEqual("BSD-3-Clause", source["license"])
            self.assertEqual("https://github.com/vpinball/pinmame", source["uri"])
        manual = self.sources["manual.data-east.secret-service.1988"]
        self.assertEqual("https://archive.org/details/Data_East__Secret_Service_Manual", manual["uri"])
        self.assertEqual("Data_East__Secret_Service_Manual", manual["source_id"])
        self.assertEqual("2026-08-09T20:45:42Z", manual["acquired_at"])
        self.assertIn("archive-org/Data_East_1988_Secret_Service_Manual.pdf", manual["locator"])
        for source_id in ("vpx-table.secret-service-bigus-mod-1-1", "vpx-script.secret-service-bigus-mod-1-1"):
            self.assertTrue(self.sources[source_id]["uri"].startswith("external:pinmame-vpx-sources/data-east/secret-service-1988/"))
        core_locator = self.sources["pinmame.core.4ec52ff0ac13"]["locator"]
        for fragment in ("lines 714-715", "737-738", "746-747", "SP6, SP5, SP2, SP3, SP1, and SP4"):
            self.assertIn(fragment, core_locator)
        self.assertIn("ssSolNo={3,4,5,1,0,2}", core_locator)
        self.assertIn("SP6, SP5, SP2, SP3, SP1, and SP4", core_locator)
        switch = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
        lamp = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
        coil = (EXCERPT_ROOT / "coil-chart.md").read_text(encoding="utf-8")
        schematic = (EXCERPT_ROOT / "production-schematics.md").read_text(encoding="utf-8")
        self.assertIn("| 18 | GRN-ORN | WHT-RED | Top 10 Point |", switch)
        self.assertIn("| 18 | Top 310 Point |", switch)
        self.assertIn("| 5 | YEL-BRN | RED-GRN | Jefferson Memorial #2 |", lamp)
        self.assertIn("| 5 | Jefferson Memorial #1 (Jackpot) |", lamp)
        self.assertIn("| 07L | Russian Embassy / Backglass (2) | GRY-VIO | VIO-BLK |", coil)
        self.assertIn("| SP3 | Blue Pop Bumper | BLU-ORN | (ORN-BLK) |", coil)
        self.assertIn("| -- | Right Flipper | (BLU-VIO) | -- | BIU-YEL |", coil)
        self.assertIn("SP6's device-type cell is blank", coil)
        self.assertIn("printed 17-22 explicitly pair SP1-SP6", coil)
        self.assertIn("derive SP1, SP3, SP4, SP6, SP5 and SP2 at public 17-22", coil)
        self.assertIn("source interpretation remains a first-class conflict", coil)
        self.assertIn("`CLEAR POP BUMPER`", schematic)
        self.assertIn("SP1/SP2/SP3/SP4/SP5/SP6 to Q11/Q9/Q8/Q10/Q12/Q13", schematic)
        self.assertIn("CN3 pin 6 `BLU-YEL`", schematic)
        self.assertIn("literally prints `BIU-YEL`", schematic)

    def test_manifest_canonical_digest_and_shape(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(972, manifest["file_count"])
        self.assertEqual(53_434_484, manifest["total_bytes"])
        self.assertEqual(972, len(manifest["files"]))
        algorithm = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
        self.assertEqual(algorithm, manifest["manifest_algorithm"])
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("5c80483c2010460c736a8d2e91ef887a72766f08b98fbf939e8abb727aae68ce", manifest["manifest_sha256"])
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
        extraction_source = self.sources["vpx-extraction.secret-service-bigus-mod-1-1"]
        self.assertEqual("6bd34670c2b4880831dde9a843e7c1a6e7365f9c4aea868452f6fe00f25335ac", extraction_source["sha256"])
        self.assertIn(f"algorithm: {algorithm}", extraction_source["locator"])

    def test_catalog_reassigns_four_drivers_and_removes_stub_normally(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        records = {item["id"]: item for item in catalog["drivers"]}
        for driver_id in OWN_DRIVERS:
            self.assertEqual("data-east.secret-service.1988", records[driver_id]["machine_id"])
            self.assertEqual("machines/partial/data-east/secret-service-1988.json", records[driver_id]["definition"])
            self.assertEqual("partial", records[driver_id]["coverage_status"])
        self.assertFalse((ROOT / "machines" / "stubs" / "ssvc_a26.json").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "ssvc_a26.md").exists())
        self.assertFalse((ROOT / "machines" / "stubs" / "ssvc_a26.json.disabled").exists())
        self.assertFalse((ROOT / "knowledge" / "stubs" / "ssvc_a26.md.disabled").exists())

    def test_dynamic_contamination_guard_is_catalog_derived(self) -> None:
        catalog = load_json(ROOT / "catalog" / "pinmame.json")
        artifact_paths = [DEFINITION_PATH, SEED_PATH, REPORT_PATH, REPORT_MARKDOWN_PATH, KNOWLEDGE_PATH]
        artifact_text = "\n".join(path.read_text(encoding="utf-8").casefold() for path in artifact_paths)
        # Driver claims occur as exact JSON strings or backticked short names.  Restricting the
        # lexical context avoids treating ordinary English words that happen to be very short
        # catalog IDs (for example, a theme noun) as an identifier claim.
        identifier_tokens = set(re.findall(r'["`]([a-z0-9_]+)["`]', artifact_text))
        machine_tokens = set(re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)+", artifact_text))

        other_driver_ids = {
            value.casefold() for item in catalog["drivers"] for value in (item["id"], item.get("root_driver"))
            if isinstance(value, str) and value not in OWN_DRIVERS
        }
        self.assertEqual(set(), identifier_tokens & other_driver_ids)
        other_machine_ids = {item["id"].casefold() for item in catalog["machines"] if item["id"] != "data-east.secret-service.1988"}
        self.assertEqual(set(), machine_tokens & other_machine_ids)

        own_core_locator = self.sources["pinmame.core.4ec52ff0ac13"]["locator"]
        own_generation_constants = set(re.findall(r"\bGEN_[A-Z0-9_]+\b", own_core_locator))
        self.assertEqual(1, len(own_generation_constants), "own generation constant must derive from the exact initializer locator")
        foreign_generation_constants: set[str] = set()
        foreign_hardware_generations: set[str] = set()
        foreign_table_fingerprints: set[str] = set()
        for machine in catalog["machines"]:
            if machine["id"] == "data-east.secret-service.1988":
                continue
            path = ROOT / machine["definition"]
            if not path.is_file():
                continue
            other = load_json(path)
            other_text = path.read_text(encoding="utf-8")
            knowledge_path = other.get("knowledge", {}).get("path")
            if isinstance(knowledge_path, str) and (ROOT / knowledge_path).is_file():
                other_text += "\n" + (ROOT / knowledge_path).read_text(encoding="utf-8")
            foreign_generation_constants.update(re.findall(r"\bGEN_[A-Z0-9_]+\b", other_text))
            hardware = other.get("controller", {}).get("hardware_generation")
            if isinstance(hardware, str) and hardware != self.definition["controller"]["hardware_generation"]:
                foreign_hardware_generations.add(hardware.casefold())
            for source in other.get("sources", []):
                if source.get("kind") != "vpx_table":
                    continue
                for key in ("id", "original_filename", "source_id", "sha256"):
                    value = source.get(key)
                    if isinstance(value, str) and len(value) >= 8:
                        foreign_table_fingerprints.add(value.casefold())
        forbidden_generations = foreign_generation_constants - own_generation_constants
        artifact_upper = artifact_text.upper()
        claimed_hardware_generations = set(re.findall(r"\b0x[0-9a-f]+\b", artifact_text))
        self.assertEqual(set(), {token for token in forbidden_generations if token in artifact_upper})
        self.assertEqual(set(), foreign_hardware_generations & claimed_hardware_generations)
        self.assertEqual(set(), {value for value in foreign_table_fingerprints if value in artifact_text})

        own_table = self.sources["vpx-table.secret-service-bigus-mod-1-1"]
        self.assertEqual("Secret Service (Data East 1988)_Bigus(MOD)1.1.vpx", own_table["original_filename"])
        self.assertEqual("5d724f84cfd2b9580a0e438655397919d0ba289be356adea67e7f12f4d7e19e8", own_table["sha256"])

    def test_seed_is_byte_identical_and_knowledge_names_concrete_blockers(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        generated_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (DEFINITION_PATH, SEED_PATH, REPORT_PATH, REPORT_MARKDOWN_PATH, KNOWLEDGE_PATH)
        )
        self.assertNotIn('"platform": "pinmame.system-11"', generated_text)
        self.assertNotIn("manual-cache/", generated_text)
        self.assertIn("zero extractable characters", knowledge)
        self.assertIn("Exactly 64 Light objects are named `L1` through `L64`", knowledge)
        self.assertIn("Whole-line-commented callbacks 12 and 13 are stripped", knowledge)
        self.assertIn("Schematic pages 30 and 32-34 were rendered at 300 dpi", knowledge)
        self.assertIn("not Williams System 11 hardware", knowledge)
        self.assertIn("reviewed `pinmame.dataeast` profile", knowledge)
        self.assertIn("inversion_applied_by_emulator` flag is true", knowledge)
        self.assertNotIn("pinmame.system-11", knowledge)
        self.assertNotIn("manual-cache/", knowledge)
        self.assertNotIn("preliminary", generated_text.casefold())
        self.assertIn("record remains partial", knowledge)


class SecretServiceCuratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(ROOT / "tools"))
        import curate_secret_service
        cls.curator = curate_secret_service

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

    def test_regenerator_refuses_existing_author_ready_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            target = root / "machines" / "author-ready" / "data-east" / "secret-service-1988.json"
            target.parent.mkdir(parents=True)
            target.write_text("{}\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                self.curator._write(root)

    def test_special_solenoid_mapping_follows_explicit_coil_test_and_preserves_source_conflict(self) -> None:
        derived = {17 + self.curator.SPECIAL_DE_PERMUTATION[handler]: printed for handler, printed in self.curator.SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
        self.assertEqual({17:"SP1",18:"SP3",19:"SP4",20:"SP6",21:"SP5",22:"SP2"}, derived)
        self.assertEqual(derived, self.curator.SPECIAL_SOURCE_INFERRED_PUBLIC_TO_PRINTED)
        self.assertEqual({17:"SP1",18:"SP2",19:"SP3",20:"SP4",21:"SP5",22:"SP6"}, self.curator.SPECIAL_PUBLIC_TO_PRINTED)
        self.assertNotEqual(derived, self.curator.SPECIAL_PUBLIC_TO_PRINTED)


class SecretServiceExternalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vpx_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) if os.environ.get("PINMAME_VPX_SOURCES_ROOT") else None
        cls.manual_anchor = Path(os.environ["PINMAME_MANUALS_ROOT"]) if os.environ.get("PINMAME_MANUALS_ROOT") else None

    def test_exact_retained_table_script_and_lamp_idiom(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        base = self.vpx_root / "data-east" / "secret-service-1988"
        extraction = base / "vpxtool-extract"
        self.assertEqual("5d724f84cfd2b9580a0e438655397919d0ba289be356adea67e7f12f4d7e19e8", sha256(base / "Secret Service (Data East 1988)_Bigus(MOD)1.1.vpx"))
        self.assertEqual("b49f27dd97ad6a106a2f2bf4a0181bda86e58e31b0e88efe3663e614ace237e3", sha256(extraction / "script.vbs"))
        script = (extraction / "script.vbs").read_text(encoding="utf-8")
        self.assertIn('Const cGameName="ssvc_a26",UseSolenoids=2,UseLamps=0,UseGI=0', script)
        self.assertEqual(0, len(re.findall(r"Lampz\.MassAssign", script, re.I)))
        self.assertEqual(0, len(re.findall(r"vpmMapLights", script, re.I)))
        active = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("'"))
        self.assertNotRegex(active, r"SolCallback\s*\(\s*12\s*\)")
        self.assertNotRegex(active, r"SolCallback\s*\(\s*13\s*\)")
        self.assertEqual(26, len(re.findall(r"SolCallback", script, re.I)))
        light_names = []
        for path in (extraction / "gameitems").glob("*.json"):
            outer = load_json(path)
            kind, item = next(iter(outer.items()))
            if kind == "Light" and re.fullmatch(r"L([1-9]|[1-5][0-9]|6[0-4])", item.get("name", "")):
                light_names.append(item["name"])
        self.assertEqual({f"L{address}" for address in range(1, 65)}, set(light_names))

    def test_extraction_manifest_recomputes_every_file(self) -> None:
        if self.vpx_root is None:
            self.skipTest("retained VPX sources are not available")
        extraction = self.vpx_root / "data-east" / "secret-service-1988" / "vpxtool-extract"
        manifest = load_json(MANIFEST_PATH)
        actual = [path.relative_to(extraction).as_posix() for path in sorted(path for path in extraction.rglob("*") if path.is_file())]
        self.assertEqual(actual, [entry["path"] for entry in manifest["files"]])
        for entry in manifest["files"]:
            path = extraction / entry["path"]
            self.assertEqual(entry["bytes"], path.stat().st_size, entry["path"])
            self.assertEqual(entry["sha256"], sha256(path), entry["path"])

    def test_exact_archive_org_manual_hash_via_supplied_anchor(self) -> None:
        if self.manual_anchor is None:
            self.skipTest("retained manuals are not available")
        root = self.manual_anchor / "by-machine" / "data-east.secret-service.1988" / "archive-org"
        self.assertTrue(root.is_dir(), root)
        production = root / "Data_East_1988_Secret_Service_Manual.pdf"
        self.assertEqual(5_290_463, production.stat().st_size)
        self.assertEqual("f2d9c030951d1d8fef3db36447457689b69bac557935053293dd3c143ec4252a", sha256(production))


if __name__ == "__main__":
    unittest.main()
