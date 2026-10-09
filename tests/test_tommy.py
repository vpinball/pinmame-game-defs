"""Gates for the Data East The Who's Tommy Pinball Wizard (1994) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major address
arithmetic, the cabinet flipper addresses PinMAME mirrors, the Left/Right relay pairing, the blinder's two
PinMAME addresses (CN3 line 44 and custom solenoid 51), what the ROM's own service tests said about every
public address, and the boundary between what the retained recreation measured and what it did not. The
fixtures below are typed from the printed charts and the read DMD frames and kept apart from the curator on
purpose: a test that checks the generator against its own output only proves the generator is self-consistent.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

KEY = "data-east.the-who-s-tommy-pinball-wizard.1994"
SLUG = "the-who-s-tommy-pinball-wizard-1994"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/the-who-s-tommy-pinball-wizard-tomy_400-service-tests.json"
PLACES_PATH = ROOT / "tools/tommy_places.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY
REVIEW_ROOT = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
VPX_ROOT = os.environ.get("PINMAME_VPX_SOURCES_ROOT")

# --- Independent fixtures ----------------------------------------------------------------------------------
# Printed switch chart cells (joined across line breaks), spread over all eight columns.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 3: "Credit Button", 8: "Extra Ball Button", 9: "Ball Trough #1 LT", 15: "Ball Trough #7 RT", 16: "Shooter Lane",
    19: "VUK", 22: "Right RampS-U", 24: "Silver Ball Target", 28: "Mirror Up", 31: "Mirror Down", 32: "Mirror Target", 37: "RT Return Lane",
    41: "Mirror Trough", 42: "Skill Trough", 43: "Captive Ball", 47: "Eject", 51: "RT Turbo Bumper", 55: "Left Outlane",
    58: "Left Ramp Exit", 62: "Right Ramp Exit", 63: "Left Flipper", 64: "Right Flipper",
}
UNUSED_SWITCHES = {44, 45, 46, 52, 53, 54, 59, 60, 61}
# The ROM's Active Switch Test names, read from the retained frames.
ROM_SWITCHES = {
    1: "PLUMB TILT", 8: "EXTRA BALL BUTTON", 9: "TROUGH #1 LT", 22: "RIGHT RAMP S-U", 28: "MIRROR UP", 32: "MIRROR TARGET",
    41: "MIRROR TROUGH", 49: "LEFT POP BUMPER", 63: "LEFT END OF STROKE", 64: "RIGHT END OF STROKE", 44: "NOT USED", 61: "NOT USED",
}
MANUAL_LAMPS = {
    1: "Insert X2 (T)OMMY", 8: "Grid: Wizard", 9: "Skill Shot", 22: "RT. Ramp S-U Top", 23: "Extra Ball Button", 37: "Insert X2 TOMM(Y)",
    42: "P/F T(O)MMY", 46: "Outlanes X2", 56: "Airplane", 63: "Collect Union Jack", 64: "Credit Button",
}
ROM_LAMPS = {27: "LT 3-BANK S-U TOP", 46: "OUTLANES X 2", 54: "HOLIDAY CAMP", 1: "INSERT X2 (T)OMMY", 8: "GRID: PINBALL WIZARD", 22: "RT RAMP S-U", 42: "T(O)MMY", 55: "RETURN LANES X 2", 56: "AIRPLANE", 64: "CREDIT BUTTON"}
# Coil Test entries: (printed number, ROM name, public addresses Start fires).
ROM_COIL_TEST = {
    "#1L": ("COIL: LOCK OUT", [1]), "#1R": ("FLASH: ARCH LT/RT X4", [10, 25]), "#3L": ("COIL: AUTO LAUNCH 50V", [3]),
    "#4R": ("FLASH: INS X2 EJECT X2", [10, 28]), "#7L": ("NOT USED", [7]), "#09": ("NOT USED", [9]), "#12": ("COIL: TOP DIVERTER", [12]),
    "#13": ("MOTOR: AIRPLANE", [13]), "#14": ("MOTOR: MIRROR", [14]), "#15": ("FLASH: INS X3 MIRROR X1", [15]), "#16": ("NOT USED", []),
    "#17": ("COIL: LEFT POP BUMPER", [17]), "#21": ("COIL: RIGHT SLINGSHOT", [21]), "#22": ("NOT USED", []),
}
# Flash-lamp drives as printed in the coil table: playfield count (the "X#") of four bulbs.
FLASHER_PLAYFIELD = {25: 4, 26: 4, 27: 2, 28: 2, 29: 4, 30: 4, 31: 2, 32: 4}
DRIVER_ROMS = {
    "tomy_400": ("tomcpua.400", "tommydva.400"), "tomy_500": ("tomcpua.500", "tommydva.500"),
    "tomy_301g": ("tom_3.00_german_cpu_c5.bin", "tom_3.00_german_display_rom0.bin"), "tomy_201d": ("Tommy_2.01_Dutch_cpu.bin", "Tommy_2.00_display.bin"),
    "tomy_h30": ("tomcpuh.300", "tommydva.300"), "tomy_102": ("tomcpua.102", "tommydva.300"), "tomy_102be": ("tomcpub.102", "tommydvb.102"),
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.inputs = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}

    def test_identity_and_variants(self) -> None:
        machine = self.definition["machine"]
        self.assertEqual((KEY, 1994, 2579, "500-5528-01", "GR6do-MLBq4"), (machine["id"], machine["year"], machine["ipdb_id"], machine["model_number"], machine["opdb_id"]))
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        self.assertEqual(set(DRIVER_ROMS), set(drivers))
        self.assertNotIn("clone_of", drivers["tomy_400"])
        for name, driver in drivers.items():
            self.assertEqual("identical", driver["physical_compatibility"], name)
            if name != "tomy_400":
                self.assertEqual("tomy_400", driver["clone_of"])
                for rom, root in zip(DRIVER_ROMS[name], DRIVER_ROMS["tomy_400"]):
                    if rom != root:
                        self.assertIn(rom, driver["variant_notes"], f"{name} omits {rom}")
        self.assertEqual("2016", drivers["tomy_500"]["year"])
        self.assertIn("later community software", drivers["tomy_500"]["variant_notes"])

    def test_controller_platform(self) -> None:
        self.assertEqual(("pinmame.dataeast", "0x4000"), (self.definition["controller"]["platform"], self.definition["controller"]["hardware_generation"]))

    def test_every_matrix_switch_is_enumerated_once_in_column_major_order(self) -> None:
        self.assertEqual(set(range(1, 65)) | {-7, -6} | set(range(81, 89)), set(self.inputs))
        for address, printed in MANUAL_SWITCHES.items():
            notes = self.inputs[address]["physical"]["notes"]
            column, row = divmod(address - 1, 8)
            self.assertIn(f"column {column + 1}, row {row + 1}", notes, address)
            self.assertIn(f"'{printed}'", notes, address)
        for address in range(1, 65):
            self.assertEqual("unused" if address in UNUSED_SWITCHES else "used", self.inputs[address]["availability"], address)

    def test_rom_names_and_polarity(self) -> None:
        for address, name in ROM_SWITCHES.items():
            self.assertIn(f"shows '{name}'", self.inputs[address]["physical"]["notes"], address)
        for address in set(range(1, 65)) - UNUSED_SWITCHES:
            self.assertIs(False, self.inputs[address]["normally_closed"], address)
        for address in UNUSED_SWITCHES:
            self.assertNotIn("normally_closed", self.inputs[address], address)
        for address in (-7, 82, 84):
            self.assertIs(False, self.inputs[address]["normally_closed"], address)
        for address in (-6, 81, 83, 85, 86, 87, 88):
            self.assertNotIn("normally_closed", self.inputs[address], address)
        self.assertIn("left undeclared", self.inputs[-6]["physical"]["notes"])

    def test_flipper_column_and_the_matrix_copies(self) -> None:
        for address in range(81, 89):
            self.assertEqual("used" if address in (82, 84) else "unused", self.inputs[address]["availability"], address)
        self.assertIn("LEFT END OF STROKE", self.inputs[84]["physical"]["notes"])
        self.assertIn("RIGHT END OF STROKE", self.inputs[82]["physical"]["notes"])
        for address in (63, 64):
            notes = self.inputs[address]["physical"]["notes"]
            self.assertIn("FLIP6364", notes)
            self.assertIn(f"A consumer drives {84 if address == 63 else 82}", notes)

    def test_lamps_cover_the_whole_matrix(self) -> None:
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        for address, printed in MANUAL_LAMPS.items():
            self.assertIn(f"'{printed}'", self.lamps[address]["physical"]["notes"], address)
        for address, name in ROM_LAMPS.items():
            self.assertIn(f"under '{name}'", self.lamps[address]["physical"]["notes"], address)
        for address in range(1, 65):
            self.assertIn("ROM evidence (US 4.00 Lamp Test): the single-lamp test lights public lamp", self.lamps[address]["physical"]["notes"], address)
        for address in (1, 10, 19, 28, 37, 46, 55):
            self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
        for address in (1, 10, 19, 28, 37, 23, 64):
            self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
        self.assertIn("misprint", self.lamps[42]["physical"]["notes"])

    def test_solenoid_address_model(self) -> None:
        self.assertEqual(set(range(1, 52)), set(self.solenoids))
        unused = {address for address, item in self.solenoids.items() if item["availability"] == "unused"}
        self.assertEqual({7, 9, 16, 22, 24, 33, 34, 35, 36, 49, 50}, unused)
        unknown = {address for address, item in self.solenoids.items() if item["availability"] == "unknown"}
        self.assertEqual(set(range(37, 44)), unknown)
        self.assertEqual("gi", self.solenoids[11]["kind"])
        self.assertEqual("relay", self.solenoids[10]["kind"])
        self.assertEqual("servo", self.solenoids[51]["kind"])
        self.assertEqual("used", self.solenoids[44]["availability"])
        self.assertIn("CORE_FIRSTCUSTSOL 51", self.solenoids[51]["physical"]["notes"])
        self.assertIn("Blinder on Tommy", self.solenoids[44]["physical"]["notes"])

    def test_rom_coil_test_names_and_responses(self) -> None:
        for number, (name, fired) in ROM_COIL_TEST.items():
            if not fired:
                address = int(number.strip("#"))
                self.assertIn(f"entry {number} is named '{name}'", self.solenoids[address]["physical"]["notes"], number)
                self.assertIn("fires nothing", self.solenoids[address]["physical"]["notes"], number)
                continue
            address = fired[-1]
            self.assertIn(f"entry {number} is named '{name}'", self.solenoids[address]["physical"]["notes"], number)

    def test_right_hand_flash_lamps_pair_with_the_relay(self) -> None:
        relationships = {(item["source"], item["destination"]) for item in self.definition["relationships"] if item["kind"] == "relay_gated"}
        for address, playfield in FLASHER_PLAYFIELD.items():
            drive = address - 24
            self.assertIn(("relay.left-right-relay", f"flasher.{drive}r"), relationships)
            self.assertEqual(4, self.solenoids[address]["physical"]["quantity"])
            self.assertIn(f"{playfield} outside the insert", self.solenoids[address]["physical"]["notes"], address)
        self.assertIn("misprint", self.solenoids[28]["physical"]["notes"])

    def test_blinder_relationship(self) -> None:
        self.assertIn(
            ("direct", "virtual.cn3-line-44", "servo.blinder"),
            {(item["kind"], item["source"], item["destination"]) for item in self.definition["relationships"]},
        )

    def test_mechanisms_carry_the_rom_pairs(self) -> None:
        mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
        for mechanism_id, sentence in (
            ("mechanism.auto-ball-launch", "closing the shooter lane switch 16 fires public 3"),
            ("mechanism.vuk", "closing the VUK switch 19 fires public 4"),
            ("mechanism.left-scoop", "closing the Left Scoop switch 23 fires public 5"),
            ("mechanism.eject", "closing the Eject switch 47 fires public 6"),
            ("mechanism.mirror", "holding Start drives public 14"),
        ):
            self.assertIn(sentence, mechanisms[mechanism_id]["behavior"], mechanism_id)
        for mechanism in mechanisms.values():
            self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
        self.assertEqual(["servo.blinder"], mechanisms["mechanism.blinder"]["actuators"])

    def test_transistor_disagreements_are_notes_not_conflicts(self) -> None:
        self.assertEqual([], self.definition["conflicts"])
        self.assertIn("Q23", self.solenoids[14]["physical"]["notes"])
        self.assertIn("Q25", self.solenoids[14]["physical"]["notes"])

    def test_coverage_gate(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["input_semantics", "output_semantics", "polarity", "spatial_placement"], coverage["missing"])
        self.assertEqual("complete", self.definition["knowledge"]["status"])

    def test_the_curator_check_passes_and_refuses_drift(self) -> None:
        import curate_tommy as curator

        curator._check(ROOT)
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, KNOWLEDGE_PATH):
                target = root / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
            curator._check(root)
            definition = root / DEFINITION_PATH.relative_to(ROOT)
            definition.write_bytes(definition.read_bytes().replace(b'"Left Outlane"', b'"Left Outlane X"', 1))
            with self.assertRaises(RuntimeError):
                curator._check(root)

    def test_seed_is_byte_identical_to_the_definition(self) -> None:
        self.assertEqual(DEFINITION_PATH.read_bytes().replace(b"\r\n", b"\n"), SEED_PATH.read_bytes().replace(b"\r\n", b"\n"))

    def test_other_machines_are_not_named_in_the_artifacts(self) -> None:
        catalog = load_json(ROOT / "catalog/pinmame.json")
        text = "\n".join(path.read_text(encoding="utf-8") for path in (DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH))
        for machine in catalog["machines"]:
            if machine["id"] != KEY and machine["id"].startswith("data-east."):
                self.assertNotIn(machine["id"], text)
        for forbidden in ("tftc", "Tales from the Crypt", "gnr_", "Guns N", "wwfr_", "mav_"):
            self.assertNotIn(forbidden, text, forbidden)

    def test_knowledge_note_states_the_platform_facts(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in (
            "tomy_500", "no GI channel", "Left/Right relay", "S11_PRINTERLINE", "never 63 or 64", "Blinder on Tommy", "**51**",
            "column-major", "END OF STROKE", "Q23", "Q25", "28 VAC",
        ):
            self.assertIn(phrase, text, phrase)


class ExcerptTests(unittest.TestCase):
    def test_parsed_tables_match_the_independent_fixtures(self) -> None:
        import tommy_manual

        switches = tommy_manual.switch_data()["chart"]
        for address, printed in MANUAL_SWITCHES.items():
            self.assertEqual(printed, switches[address]["printed"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("Not Used", switches[address]["printed"], address)
        lamps = tommy_manual.lamp_data()["chart"]
        for address, printed in MANUAL_LAMPS.items():
            self.assertEqual(printed, lamps[address]["printed"], address)
        coils = tommy_manual.coil_data()
        self.assertEqual("Q46", coils["drivers"]["1L"]["Drive transistor"])
        self.assertEqual("Q25", coils["drivers"]["14"]["Drive transistor"])
        self.assertEqual("22-600", coils["drivers"]["3L"]["Coil or flash type"])
        self.assertEqual("Flashlamp: X1 Tommy", coils["drivers"]["15"]["Description"])
        self.assertEqual("DATA", coils["servo_input"][4]["Signal"])

    def test_the_parser_rejects_a_ragged_table(self) -> None:
        import tommy_manual

        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.md"
            path.write_bytes(b"## Table\n\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n")
            with self.assertRaises(ValueError):
                tommy_manual.read_tables(path)

    def test_every_recorded_excerpt_digest_matches_its_file(self) -> None:
        definition = load_json(DEFINITION_PATH)
        recorded = [excerpt for source in definition["sources"] for excerpt in source.get("excerpts", [])]
        self.assertEqual(sorted(path.name for path in EXCERPTS.iterdir()), sorted(Path(item["path"]).name for item in recorded))
        for excerpt in recorded:
            self.assertEqual(sha256_file(ROOT / excerpt["path"]), excerpt["sha256"], excerpt["id"])
            self.assertTrue(excerpt["reviewed"], excerpt["id"])

    def test_the_readings_agree_with_the_manual_wires(self) -> None:
        import build_tommy_runtime_evidence as builder
        import tommy_manual

        readings = load_json(ROOT / "tools/tommy_readings.json")
        switches = tommy_manual.switch_data()["chart"]
        lamps = tommy_manual.lamp_data()["chart"]
        for key, reading in readings["switches"].items():
            chart = switches[int(key)]
            self.assertEqual(f"{chart['drive']['wire']} {chart['return']['wire']}", builder.normalize_wires(reading["wires"]), key)
        for key, reading in readings["lamps"].items():
            chart = lamps[int(key)]
            self.assertEqual(f"{chart['drive']['wire']} {chart['return']['wire']}", builder.normalize_wires(reading["wires"]), key)


class SpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.places = load_json(PLACES_PATH)

    def test_every_placement_is_in_range_unique_and_observed(self) -> None:
        ids = []
        for device in self.definition["inputs"] + self.definition["outputs"]:
            for placement in device.get("spatial", {}).get("placements", []):
                ids.append(placement["id"])
                self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
                self.assertEqual("observed", placement["provenance"]["status"], placement["id"])
        self.assertEqual(len(ids), len(set(ids)))
        report = load_json(SPATIAL_REPORT_PATH)
        self.assertEqual(len(ids), report["placement_count"])

    def test_normalization_matches_the_raw_coordinates(self) -> None:
        width, height = self.places["table_bounds"]["width"], self.places["table_bounds"]["height"]
        for key, hits in self.places["placements"].items():
            for hit in hits:
                self.assertAlmostEqual(round(hit["raw"]["x"] / width, 6), hit["x"], places=6, msg=key)
                self.assertAlmostEqual(round(hit["raw"]["y"] / height, 6), hit["y"], places=6, msg=key)

    def test_cabinet_and_backbox_devices_are_not_placed(self) -> None:
        devices = {(item["binding"]["group"], item["binding"]["device"]): item for item in self.definition["inputs"] + self.definition["outputs"]}
        for key in [("pinmame.input.switch", n) for n in (1, 2, 3, 4, 5, 6, 7, 8, 63, 64)] + [("pinmame.output.solenoid", n) for n in (8, 10)]:
            self.assertEqual("not_applicable", devices[key]["spatial"]["status"], key)

    def test_the_mirror_limits_are_a_declared_projection(self) -> None:
        inputs = {item["binding"]["device"]: item for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
        for address in (28, 31):
            self.assertIn("projection onto the retained table's mirror mechanism", inputs[address]["physical"]["notes"])

    def test_the_gi_is_not_placed(self) -> None:
        gi = [item for item in self.definition["outputs"] if item["binding"] == {"group": "pinmame.output.solenoid", "device": 11}][0]
        self.assertNotIn("spatial", gi)
        self.assertIn("gi.general-illumination", load_json(SPATIAL_REPORT_PATH)["blockers"][1]["omitted_spatial_key_devices"])

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_the_placements_equal_the_extraction(self) -> None:
        import subprocess

        extracted = Path(VPX_ROOT) / "data-east/the-who-s-tommy-pinball-wizard/vpw-mod-1.2.1/extracted"
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/build_tommy_places.py"), "--extracted", str(extracted), "--output", str(PLACES_PATH), "--check"],
            capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")])},
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    @unittest.skipUnless(VPX_ROOT, "PINMAME_VPX_SOURCES_ROOT is not set")
    def test_extraction_manifest_is_recomputable(self) -> None:
        import build_external_evidence_manifest as manifest

        extracted = Path(VPX_ROOT) / "data-east/the-who-s-tommy-pinball-wizard/vpw-mod-1.2.1/extracted"
        self.assertEqual("fc3f74ec1c6a35dac4a56050b394ef6e7c7ff0de36a61344bb2940a5d3e2696b", manifest.check_manifest(extracted, "tomy_500"))


class RuntimeEvidenceTests(unittest.TestCase):
    def test_the_definition_records_the_evidence_digest(self) -> None:
        sources = {item["id"]: item for item in load_json(DEFINITION_PATH)["sources"]}
        self.assertEqual(sha256_file(EVIDENCE_PATH), sources["runtime.the-who-s-tommy-pinball-wizard.tomy-400-service-tests"]["sha256"])

    def test_cycling_coils_order_is_the_public_address_order(self) -> None:
        runs = load_json(EVIDENCE_PATH)["runtime"]["observations"]["runs"]
        expected = [n for drive in range(1, 9) for n in (drive, drive + 24)] + [9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]
        self.assertEqual(expected, runs["cycling-coils"]["ordered_solenoid_on_sequence"])

    def test_only_the_blinder_line_moves_on_cn3(self) -> None:
        facts = load_json(ROOT / "tools/tommy_runtime.json")
        self.assertEqual([44, 51], facts["cn3_lines"]["moving"])
        self.assertEqual([], facts["cn3_lines"]["printer_start_fired"])
        self.assertEqual({"mirror-test": [14], "arch-test": [44, 51]}, facts["mirror_and_arch"]["start"])
        self.assertEqual({"16": [3], "19": [4], "23": [5], "47": [6]}, facts["mirror_and_arch"]["switch_to_coil"])

    def test_every_scenario_is_committed_and_valid(self) -> None:
        evidence = load_json(EVIDENCE_PATH)
        for run in evidence["runtime"]["raw_runs"]:
            path = ROOT / run["scenario_path"]
            self.assertEqual(run["scenario_sha256"], sha256_file(path), run["name"])
            scenario = load_json(path)
            self.assertEqual("tomy_400", scenario["game"])
            self.assertEqual(run["action_count"], len(scenario["actions"]))
            self.assertFalse([a for a in scenario["actions"] if a["type"] in ("pulse_key", "set_key")], "named keys would enable keyboard handling")

    def test_the_harness_refuses_ambiguous_title_targets(self) -> None:
        import tommy_harness

        with self.assertRaises(ValueError):
            tommy_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["SWITCH TEST"]}]})
        with self.assertRaises(ValueError):
            tommy_harness.check_targets({"actions": [{"type": "pulse_until_display", "texts": ["NOT A TITLE"]}]})

    @unittest.skipUnless(REVIEW_ROOT, "PINMAME_REVIEW_ARTIFACTS_ROOT is not set")
    def test_the_evidence_rebuilds_from_the_retained_runs(self) -> None:
        import subprocess

        session = Path(REVIEW_ROOT) / KEY / "session-20261009/final/tomy_400"
        manifest_files = [session / "manifest.json", session / "manifest.sha256"]
        before = [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files]
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/build_tommy_runtime_evidence.py"), "--check"],
            capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT / "src"), str(ROOT / "tools")])},
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        # --check verifies the pinned external manifest and must never rewrite it.
        self.assertEqual(before, [(path.stat().st_mtime_ns, path.read_bytes()) for path in manifest_files])


if __name__ == "__main__":
    unittest.main()
