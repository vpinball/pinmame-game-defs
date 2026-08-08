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
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "data-east.secret-service.1988"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
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
            {"platform": "pinmame.system-11", "hardware_generation": "0x1000", "inversion_applied_by_emulator": True},
            self.definition["controller"],
        )
        self.assertEqual(OWN_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})
        root = next(driver for driver in self.definition["drivers"] if driver["id"] == "ssvc_a26")
        self.assertNotIn("clone_of", root)
        self.assertEqual(OWN_DRIVERS - {"ssvc_a26"}, {driver["id"] for driver in self.definition["drivers"] if driver.get("clone_of") == "ssvc_a26"})
        self.assertTrue(all(driver["year"] == "1988" and driver["manufacturer"] == "Data East" for driver in self.definition["drivers"]))
        self.assertEqual(952.0, self.definition["machine"]["playfield"]["width"])
        self.assertEqual(2162.0, self.definition["machine"]["playfield"]["height"])

    def test_upstream_system_11_profile_covers_exact_data_east_subsets(self) -> None:
        profile = load_json(CONTROLLER_PATH)
        groups = {group["id"]: group for group in profile["groups"]}

        def allowed(group_id: str, address: int) -> bool:
            return any(
                address in rule.get("values", [])
                or rule.get("minimum", address + 1) <= address <= rule.get("maximum", address - 1)
                for rule in groups[group_id]["address_rules"]
            )

        self.assertTrue(all(allowed("pinmame.input.switch", address) for address in (-7, -6, 1, 64)))
        self.assertTrue(all(allowed("pinmame.output.solenoid", address) for address in range(1, 51)))
        self.assertTrue(all(allowed("pinmame.output.lamp", address) for address in range(1, 65)))
        self.assertTrue(allowed("pinmame.input.dip", 0))
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
        self.assertTrue(all(solenoids[address]["provenance"]["status"] == "conflicted" for address in set(range(1, 9)) | set(range(25, 33))))
        knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        self.assertIn("types only output 9 and muxed public 25-32 as #89 bulbs", knowledge)
        self.assertIn("GI at 11, and K1 at 10", knowledge)

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
        for identifier in (
            "mechanism.left-slingshot", "mechanism.right-slingshot", "mechanism.red-pop-bumper",
            "mechanism.clear-pop-bumper", "mechanism.blue-pop-bumper",
        ):
            self.assertEqual([], mechanisms[identifier]["actuators"], "printed labels must not fabricate a retained runtime binding")

    def test_relay_relationships_cover_public_25_through_32(self) -> None:
        self.assertEqual(8, len(self.definition["relationships"]))
        self.assertEqual({f"coil.driver-{address}" for address in range(25, 33)}, {item["destination"] for item in self.definition["relationships"]})
        self.assertTrue(all(item["source"] == "coil.driver-10" and item["provenance"]["status"] == "conflicted" for item in self.definition["relationships"]))

    def test_all_eight_conflicts_are_first_class(self) -> None:
        self.assertEqual({
            "conflict.switch-score-labels-matrix-vs-list", "conflict.left-flipper-eos-runtime",
            "conflict.right-flipper-eos-runtime", "conflict.lamp-matrix-vs-description-list",
            "conflict.mux-bank-output-typing", "conflict.clear-vs-yellow-pop-bumper",
            "conflict.right-flipper-power-wire", "conflict.output-13-description",
        }, {item["id"] for item in self.definition["conflicts"]})
        self.assertTrue(all(len(item["source_refs"]) >= 2 for item in self.definition["conflicts"]))

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
        self.assertEqual(2, len(self.outputs["coil.driver-3"]["spatial"]["placements"]))
        markdown = REPORT_MARKDOWN_PATH.read_text(encoding="utf-8")
        self.assertIn("x: `raw_x / 952`", markdown)
        self.assertIn("## Explicit projection classes", markdown)
        self.assertIn("Keep partial", markdown)

    def test_evidence_excerpts_exist_hash_and_preserve_literal_cells(self) -> None:
        excerpts = self.sources["manual.data-east.secret-service.1988"]["excerpts"] + self.sources["manual.data-east.secret-service.1988-preliminary"]["excerpts"]
        self.assertEqual(5, len(excerpts))
        for excerpt in excerpts:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
            self.assertEqual("manual", excerpt["method"])
            self.assertTrue(excerpt["reviewed"])
        switch = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
        lamp = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
        coil = (EXCERPT_ROOT / "coil-chart.md").read_text(encoding="utf-8")
        schematic = (EXCERPT_ROOT / "preliminary-schematics.md").read_text(encoding="utf-8")
        self.assertIn("| 18 | GRN-ORN | WHT-RED | Top 10 Point |", switch)
        self.assertIn("| 18 | Top 310 Point |", switch)
        self.assertIn("| 5 | YEL-BRN | RED-GRN | Jefferson Memorial #2 |", lamp)
        self.assertIn("| 5 | Jefferson Memorial #1 (Jackpot) |", lamp)
        self.assertIn("| 07L | Russian Embassy / Backglass (2) | GRY-VIO | VIO-BLK |", coil)
        self.assertIn("| SP3 | Blue Pop Bumper | BLU-ORN | (ORN-BLK) |", coil)
        self.assertIn("| -- | Right Flipper | (BLU-VIO) | -- | BIU-YEL |", coil)
        self.assertIn("SP6's device-type cell is blank", coil)
        self.assertIn("YELLOW POP BUMPER", schematic)
        self.assertIn("production label governs", schematic)

    def test_manifest_canonical_digest_and_shape(self) -> None:
        manifest = load_json(MANIFEST_PATH)
        self.assertEqual(972, manifest["file_count"])
        self.assertEqual(53_434_484, manifest["total_bytes"])
        self.assertEqual(972, len(manifest["files"]))
        body = {key: value for key, value in manifest.items() if key != "manifest_sha256"}
        canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertEqual("3f66d44a4e523f9e8b4cda576f36d2500354024276935ea092ec2cbe12d4bde7", manifest["manifest_sha256"])
        self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())

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
        self.assertIn("zero extractable characters", knowledge)
        self.assertIn("Exactly 64 Light objects are named `L1` through `L64`", knowledge)
        self.assertIn("Whole-line-commented callbacks 12 and 13 are stripped", knowledge)
        self.assertIn("preliminary scan omits its printed page 20", knowledge)
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

    def test_exact_manual_hashes_via_supplied_anchor(self) -> None:
        if self.manual_anchor is None:
            self.skipTest("retained manuals are not available")
        roots = [
            self.manual_anchor / "by-machine" / "data-east.secret-service.1988" / "contributor-supplied",
            self.manual_anchor.parent / "manual-cache" / "by-machine" / "data-east.secret-service.1988" / "contributor-supplied",
        ]
        root = next((path for path in roots if path.is_dir()), None)
        self.assertIsNotNone(root, roots)
        production = root / "Data_East_1988_Secret_Service_Manual.pdf"
        preliminary = root / "Data_East_1988_Secret_Service_Preliminary_Instruction_Manual_with_schematics_missing_page_20.pdf"
        self.assertEqual(5_290_463, production.stat().st_size)
        self.assertEqual("f2d9c030951d1d8fef3db36447457689b69bac557935053293dd3c143ec4252a", sha256(production))
        self.assertEqual(14_510_943, preliminary.stat().st_size)
        self.assertEqual("8d3b1f4035bf43c4fac33a6ec464bc5ad5771d0bdc615fd8ba2efd853051c14e", sha256(preliminary))


if __name__ == "__main__":
    unittest.main()
