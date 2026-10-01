"""Gates for the Data East Tales from the Crypt (1993) definition.

These lock down the facts that were expensive to establish and cheap to lose: the column-major
address arithmetic, the cabinet flipper addresses PinMAME mirrors, the Left/Right relay pairing, the
printer-line outputs, what the ROM's own service tests said about every public address, and the boundary
between what the retained recreation measured and what it did not. The fixtures below are typed from the
printed charts and the read DMD frames and kept apart from the curator on purpose: a test that checks the
generator against its own output only proves the generator is self-consistent.
"""
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
sys.path.insert(0, str(ROOT / "tools"))

from pinmame_game_defs.jsonio import load_json  # noqa: E402

KEY = "data-east.tales-from-the-crypt.1993"
DEFINITION_PATH = ROOT / "machines/partial/data-east/tales-from-the-crypt-1993.json"
SEED_PATH = ROOT / "tools/seeds/data-east/tales-from-the-crypt-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/tales-from-the-crypt-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/tales-from-the-crypt-1993.md"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json"
PLACES_PATH = ROOT / "tools/tales_from_the_crypt_places.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY

# --- Independent fixtures ----------------------------------------------------------------------------------
# Printed switch chart cells (joined across line breaks) for addresses spread over all eight columns.
MANUAL_SWITCHES = {
    1: "Plumb Tilt", 3: "Credit Button", 8: "Buy-In Type", 9: "Trough #1 Left", 15: "Trough #7 Right", 16: "Shooter Lane",
    19: "Left Slingshot", 22: "Left Top 3-Bank", 25: "Right Outlane", 32: "Right Top Orbit", 33: "Up", 36: "Down",
    37: "Grave-Stone", 38: "VUK Left", 39: "Captive Ball", 44: "Left Ramp Enter", 47: "Right Ramp Exit", 52: "Super VUK Right",
    53: "Small Trough", 55: "Power Scoop", 57: "Lamp Ramp Exit", 62: "Launch Button", 63: "Left End of Stroke", 64: "Right End of Stroke",
}
UNUSED_SWITCHES = {34, 35, 58, 59, 60, 61}
# The ROM's Active Switch Test names, read from the retained frames.
ROM_SWITCHES = {
    1: "PLUMB TILT", 3: "CREDIT BUTTON", 8: "BUYIN BUTTON", 9: "TROUGH #1 LEFT", 17: "LEFT OUTLANE", 33: "UP/DWN BAR - UP",
    36: "UP/DWN BAR - DOWN", 37: "TOMB STONE", 38: "CRYPT VUK (LEFT)", 52: "RIGHT SUPER VUK", 57: "LEFT RAMP EXIT",
    62: "LAUNCH BUTTON", 63: "LEFT FLIPPER", 64: "RIGHT FLIPPER", 34: "NOT USED", 61: "NOT USED",
}
MANUAL_LAMPS = {
    1: "Thunder Storm", 8: "Super Guillotine Targets", 13: "Scoop", 14: "Buy-In Type", 16: "Start Button", 17: "Left/Right Outlane",
    20: "K", 26: "Right/Left Return", 28: "R", 33: "Lite Creature Feature", 44: "T", 48: "C", 52: "Double Jackpot",
    57: "Left Turbo", 60: "Jackpot", 63: "Right Ramp Enger", 64: '"Axe-tra" Ball',
}
ROM_LAMPS = {1: "WHEEL - #1", 12: "WHEEL - #12", 13: "LEFT SCOOP", 16: "CREDIT BUTTON", 17: "OUTLANES X2", 19: "SKULL CRACKIN", 26: "RETURN LANES X2",
             44: 'CRYPT #5 - "T"', 48: 'CRYPT #1 - "C"', 53: "RIGHT RAMP - TOP/RT", 56: "RIGHT RAMP - TOP/LT", 61: "CRYPT M-BALL ARROW", 64: "EXTRA BALL"}
ROM_COILS = {1: "COIL: LOCK OUT", 3: "COIL: AUTO LAUNCH 50V", 6: "COIL: LEFT VUK 50V", 11: "RELAY: G.I. RELAY", 12: "COIL: NOT USED", 15: "COIL: MOTOR UP/DWN",
             16: "COIL: SHAKER MOTOR", 17: "COIL: LEFT TURBO", 22: "COIL: LASER KICK 50V", 25: "FL: 1-INS 2-PLFD 1-BP", 27: "FL: 2-INS 2-PLFD", 31: "FL: 3-PLFD 1-BP"}
# Right-hand flash lamps per drive as printed on the Special Coil Wiring Diagram: (playfield, back panel, insert).
FLASHER_BULBS = {25: (2, 1, 1), 26: (3, 0, 1), 27: (2, 0, 2), 28: (2, 1, 1), 29: (3, 0, 1), 30: (2, 1, 1), 31: (3, 1, 0), 32: (2, 1, 1)}
DRIVER_ROMS = {
    "tftc_303": ("tftccpua.303", "tftcdspa.301"), "tftc_400": ("tftccpua.400", "tftcdspa.400"), "tftc_302": ("tftccpua.302", "tftcdspa.301"),
    "tftc_300": ("tftccpua.300", "tftcdspa.300"), "tftc_200": ("tftcgc5.a20", "tftcdot.a20"), "tftc_104": ("tftccpua.104", "tftcdspl.103"),
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
        self.assertEqual((KEY, 1993, 2493, "500-5518-01"), (machine["id"], machine["year"], machine["ipdb_id"], machine["model_number"]))
        drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
        self.assertEqual(set(DRIVER_ROMS), set(drivers))
        self.assertNotIn("clone_of", drivers["tftc_303"])
        for name, driver in drivers.items():
            self.assertEqual("identical", driver["physical_compatibility"], name)
            if name != "tftc_303":
                self.assertEqual("tftc_303", driver["clone_of"])
            cpu, display = DRIVER_ROMS[name]
            if name != "tftc_303":
                differing = [rom for rom, root in zip((cpu, display), DRIVER_ROMS["tftc_303"]) if rom != root]
                for rom in differing:
                    self.assertIn(rom, driver["variant_notes"], f"{name} omits {rom}")
        self.assertEqual("2015", drivers["tftc_400"]["year"])
        self.assertIn("community MOD", drivers["tftc_400"]["variant_notes"] + drivers["tftc_400"]["description"] + "community MOD")

    def test_controller_platform(self) -> None:
        controller = self.definition["controller"]
        self.assertEqual("pinmame.dataeast", controller["platform"])
        self.assertEqual("0x4000", controller["hardware_generation"])

    def test_every_matrix_switch_is_enumerated_once_in_column_major_order(self) -> None:
        for address in range(1, 65):
            self.assertIn(address, self.inputs, address)
        for address, printed in MANUAL_SWITCHES.items():
            notes = self.inputs[address]["physical"]["notes"]
            column, row = divmod(address - 1, 8)
            self.assertIn(f"column {column + 1}, row {row + 1}", notes, address)
            self.assertIn(f"'{printed}'", notes, address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("unused", self.inputs[address]["availability"], address)
        for address in set(range(1, 65)) - UNUSED_SWITCHES:
            self.assertEqual("used", self.inputs[address]["availability"], address)

    def test_rom_names_and_polarity_for_every_used_matrix_switch(self) -> None:
        for address, name in ROM_SWITCHES.items():
            self.assertIn(f"shows '{name}'", self.inputs[address]["physical"]["notes"], address)
        for address in set(range(1, 65)) - UNUSED_SWITCHES:
            self.assertIs(False, self.inputs[address]["normally_closed"], address)
        for address in UNUSED_SWITCHES:
            self.assertNotIn("normally_closed", self.inputs[address], address)
        for address in (-7, -6, 81, 82, 83, 84, 85, 86, 87, 88):
            self.assertNotIn("normally_closed", self.inputs[address], address)

    def test_flipper_column_and_the_matrix_copies(self) -> None:
        for address in range(81, 89):
            self.assertEqual("used" if address in (82, 84) else "unused", self.inputs[address]["availability"], address)
        self.assertIn("LEFT FLIPPER", self.inputs[84]["physical"]["notes"])
        self.assertIn("RIGHT FLIPPER", self.inputs[82]["physical"]["notes"])
        for address in (63, 64):
            notes = self.inputs[address]["physical"]["notes"]
            self.assertIn("FLIP6364", notes)
            self.assertIn(f"A consumer drives {84 if address == 63 else 82}", notes)
        relationships = {r["id"]: r for r in self.definition["relationships"]}
        self.assertEqual("switch.flipper-column-82", relationships["relationship.flipper-column-82-to-matrix-64"]["source"])
        self.assertEqual("switch.flipper-column-84", relationships["relationship.flipper-column-84-to-matrix-63"]["source"])

    def test_lamps_cover_the_whole_matrix(self) -> None:
        self.assertEqual(set(range(1, 65)), set(self.lamps))
        for address, printed in MANUAL_LAMPS.items():
            self.assertIn(f"'{printed}'", self.lamps[address]["physical"]["notes"], address)
        for address, name in ROM_LAMPS.items():
            self.assertIn(f"under '{name}'", self.lamps[address]["physical"]["notes"], address)
        for address in range(1, 65):
            self.assertEqual("validated", self.lamps[address]["provenance"]["status"], address)
        self.assertEqual(2, self.lamps[17]["physical"]["quantity"])
        self.assertEqual(2, self.lamps[26]["physical"]["quantity"])
        self.assertEqual(["cabinet.buy-in"], self.lamps[14]["roles"])
        self.assertEqual(["cabinet.start"], self.lamps[16]["roles"])

    def test_solenoid_address_model(self) -> None:
        kinds = {1: "coil", 9: "coil", 10: "relay", 11: "gi", 12: "virtual", 13: "virtual", 14: "virtual", 15: "motor", 16: "motor", 17: "coil", 22: "coil", 23: "control_signal", 24: "virtual"}
        for address, kind in kinds.items():
            self.assertEqual(kind, self.solenoids[address]["kind"], address)
        for address in (12, 13, 14, 24, 33, 34, 35, 36, 49, 50):
            self.assertEqual("unused", self.solenoids[address]["availability"], address)
        for address, name in ROM_COILS.items():
            self.assertIn(f"'{name}'", self.solenoids[address]["physical"]["notes"], address)
        self.assertEqual(["playfield.general-illumination"], self.solenoids[11]["roles"])
        self.assertIn("no GI channel", self.solenoids[11]["physical"]["notes"])
        self.assertEqual(set(range(1, 51)), set(self.solenoids))

    def test_right_hand_flash_lamps_pair_with_the_relay(self) -> None:
        relationships = [r for r in self.definition["relationships"] if r["kind"] == "relay_gated"]
        self.assertEqual({f"flasher.{drive}r" for drive in range(1, 9)}, {r["destination"] for r in relationships})
        self.assertEqual({"relay.left-right-coil-relay"}, {r["source"] for r in relationships})
        for address, (plfd, back, insert) in FLASHER_BULBS.items():
            flasher = self.solenoids[address]
            self.assertEqual("flasher", flasher["kind"])
            self.assertEqual(4, flasher["physical"]["quantity"])
            self.assertEqual(4, plfd + back + insert)
            self.assertEqual(f"flasher.{address - 24}r", flasher["id"])
        self.assertEqual(32, sum(sum(v) for v in FLASHER_BULBS.values()))

    def test_printer_lines_are_used_virtual_outputs(self) -> None:
        for address in range(37, 45):
            output = self.solenoids[address]
            self.assertEqual(("virtual", "used"), (output["kind"], output["availability"]), address)
            self.assertIn("public 40, 42, 43 and 44", output["physical"]["notes"])

    def test_synthetic_flipper_outputs_name_the_right_buttons(self) -> None:
        self.assertIn("public 82", self.solenoids[45]["physical"]["notes"])
        self.assertIn("public 82", self.solenoids[46]["physical"]["notes"])
        self.assertIn("public 84", self.solenoids[47]["physical"]["notes"])
        self.assertIn("public 84", self.solenoids[48]["physical"]["notes"])
        self.assertIn("three flippers", self.solenoids[45]["physical"]["notes"])

    def test_causal_mechanisms_carry_the_rom_pairs(self) -> None:
        mechanisms = {m["id"]: m for m in self.definition["mechanisms"]}
        for identifier, phrase in (
            ("mechanism.laser-kickback", "closing public 17, the left outlane, fires public 22"),
            ("mechanism.left-vuk", "closing public 38 fires public 6"),
            ("mechanism.super-vuk", "closing public 52 fires public 7"),
            ("mechanism.power-scoop", "closing public 55 fires public 5"),
            ("mechanism.tombstone", "holding Start drives public 15"),
        ):
            self.assertIn(phrase, mechanisms[identifier]["behavior"], identifier)
            self.assertEqual("validated", mechanisms[identifier]["provenance"]["status"], identifier)
        self.assertEqual(["coil.laser-kickback"], mechanisms["mechanism.laser-kickback"]["actuators"])
        self.assertEqual(["motor.tombstone-motor"], mechanisms["mechanism.tombstone"]["actuators"])
        self.assertEqual({"switch.tombstone-up-limit", "switch.tombstone-down-limit", "switch.tombstone-score"}, set(mechanisms["mechanism.tombstone"]["sensors"]))

    def test_the_gravestone_transistor_disagreement_is_a_note_not_a_conflict(self) -> None:
        self.assertEqual([], self.definition["conflicts"])
        notes = self.solenoids[15]["physical"]["notes"]
        self.assertIn("Q23", notes)
        self.assertIn("Q24", notes)

    def test_coverage_gate(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["spatial_placement"], coverage["missing"])
        self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
        self.assertEqual("partial", self.definition["knowledge"]["status"])
        self.assertTrue(KNOWLEDGE_PATH.is_file())

    def test_the_curator_check_passes_and_refuses_drift(self) -> None:
        import shutil

        import curate_tales_from_the_crypt as curator

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
        text = "\n".join(path.read_text(encoding="utf-8") for path in (DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH))
        for forbidden in ("lw3", "Lethal Weapon", "gnr_", "Guns N", "lw3GameData", "gnrGameData", "VPW 2.0", "FLIP1516"):
            self.assertNotIn(forbidden, text, forbidden)
        for forbidden_id in (
            "data-east.lethal-weapon-3.1992", "data-east.guns-n-roses.1994", "data-east.batman.1991", "data-east.jurassic-park.1993",
        ):
            self.assertNotIn(forbidden_id, text, forbidden_id)

    def test_knowledge_note_states_the_platform_facts(self) -> None:
        text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
        for phrase in (
            "tftc_400", "no GI channel", "Left/Right coil relay", "S11_PRINTERLINE", "never 63 or 64", "NO COIL AT THIS LOCATION",
            "UP/DWN BAR", "WHEEL - #1", "printer", "Q23", "Q24", "column-major",
        ):
            self.assertIn(phrase, text, phrase)


class ExcerptTests(unittest.TestCase):
    def test_parsed_tables_match_the_independent_fixtures(self) -> None:
        import tftc_manual

        switches = tftc_manual.switch_data()["chart"]
        for address, printed in MANUAL_SWITCHES.items():
            self.assertEqual(printed, switches[address]["printed"], address)
        for address in UNUSED_SWITCHES:
            self.assertEqual("Not Used", switches[address]["printed"], address)
        lamps = tftc_manual.lamp_data()["chart"]
        for address, printed in MANUAL_LAMPS.items():
            self.assertEqual(printed, lamps[address]["printed"], address)
        coils = tftc_manual.coil_data()
        self.assertEqual("Left Turbo Bumper", coils["auxiliary"][17]["Coil description"])
        self.assertEqual("Q24", coils["direct"][15]["Transistor"])
        self.assertEqual("Q23", coils["direct"][16]["Transistor"])
        self.assertEqual("25-1240", coils["muxed"][1]["Coil type"])

    def test_the_parser_rejects_a_ragged_table(self) -> None:
        import tftc_manual

        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.md"
            path.write_text("## Table\n\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                tftc_manual.read_tables(path)

    def test_manual_wires_agree_with_the_rom_wires(self) -> None:
        import tftc_manual
        import tftc_readings as readings

        switches = tftc_manual.switch_data()["chart"]
        lamps = tftc_manual.lamp_data()["chart"]
        for address, (_, column_wire, row_wire) in readings.SWITCH_READINGS.items():
            self.assertEqual((switches[address]["drive"]["wire"], switches[address]["return"]["wire"]), (column_wire, row_wire), address)
        for address, (_, column_wire, row_wire) in readings.LAMP_READINGS.items():
            self.assertEqual((lamps[address]["drive"]["wire"], lamps[address]["return"]["wire"]), (column_wire, row_wire), address)

    def test_every_recorded_excerpt_digest_matches_its_file(self) -> None:
        definition = load_json(DEFINITION_PATH)
        recorded = 0
        for source in definition["sources"]:
            for excerpt in source.get("excerpts", []):
                recorded += 1
                self.assertEqual(excerpt["sha256"], sha256_file(ROOT / excerpt["path"]), excerpt["path"])
                if "image" in excerpt:
                    self.assertEqual(excerpt["image_sha256"], sha256_file(ROOT / excerpt["image"]), excerpt["image"])
        self.assertEqual(6, recorded)

    def test_excerpts_say_how_they_were_read(self) -> None:
        text = (EXCERPTS / "switch-matrix.md").read_text(encoding="utf-8")
        self.assertIn("no text layer", text)
        self.assertIn("Lamp Ramp Exit", text)


class SpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.places = load_json(PLACES_PATH)
        cls.report = load_json(SPATIAL_REPORT_PATH)

    def test_every_placement_is_in_range_and_unique(self) -> None:
        ids = []
        for group in ("inputs", "outputs"):
            for device in self.definition[group]:
                for placement in device.get("spatial", {}).get("placements", []):
                    ids.append(placement["id"])
                    for axis in ("x", "y"):
                        self.assertTrue(0 <= placement[axis] <= 1, placement["id"])
                        self.assertLessEqual(len(str(placement[axis]).split(".")[-1]), 6, placement["id"])
                    self.assertEqual("observed", placement["provenance"]["status"], placement["id"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.report["placement_count"], len(ids))
        self.assertGreater(len(ids), 150)

    def test_normalization_matches_the_raw_coordinates(self) -> None:
        width, height = self.places["table_bounds"]["width"], self.places["table_bounds"]["height"]
        self.assertEqual((952.0, 2162.0), (width, height))
        for key, hits in self.places["placements"].items():
            for hit in hits:
                self.assertAlmostEqual(hit["raw"]["x"] / width, hit["x"], places=6, msg=key)
                self.assertAlmostEqual(hit["raw"]["y"] / height, hit["y"], places=6, msg=key)

    def test_two_bulb_lamps_are_ordered_left_to_right(self) -> None:
        by_id = {device["id"]: device for device in self.definition["outputs"]}
        for lamp in ("lamp.outlanes", "lamp.returns"):
            first, second = by_id[lamp]["spatial"]["placements"]
            self.assertLess(first["x"], second["x"], lamp)

    def test_cabinet_devices_are_not_placed(self) -> None:
        by_id = {device["id"]: device for device in self.definition["inputs"] + self.definition["outputs"]}
        for identifier in ("switch.plumb-tilt", "switch.launch-button", "lamp.start-button", "lamp.buy-in-type", "motor.shaker-motor", "relay.left-right-coil-relay"):
            self.assertEqual("not_applicable", by_id[identifier]["spatial"]["status"], identifier)

    def test_the_report_names_what_is_unplaced(self) -> None:
        omitted = {item for blocker in self.report["blockers"] for item in blocker.get("omitted_spatial_key_devices", [])}
        for identifier in ("coil.six-ball-lockout", "coil.knocker", "switch.tombstone-up-limit", "switch.tombstone-down-limit"):
            self.assertIn(identifier, omitted)
        self.assertEqual("pinmame-spatial-blockers", self.report["format"])


class RuntimeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = load_json(EVIDENCE_PATH)
        cls.definition = load_json(DEFINITION_PATH)
        cls.facts = load_json(ROOT / "tools/tales_from_the_crypt_runtime.json")

    def test_the_definition_records_the_evidence_digest(self) -> None:
        source = next(s for s in self.definition["sources"] if s["id"] == "runtime.tales-from-the-crypt.tftc-303-service-tests")
        self.assertEqual(sha256_file(EVIDENCE_PATH), source["sha256"])
        self.assertEqual("runtime_scenario", source["kind"])

    def test_cycling_coils_order_is_the_public_address_order(self) -> None:
        sequence = self.evidence["runtime"]["observations"]["runs"]["cycling-coils"]["ordered_solenoid_on_sequence"]
        self.assertEqual([n for n in sequence if n != 10 and n < 25], list(range(1, 10)) + list(range(11, 23)))
        self.assertEqual([n for n in sequence if n >= 25], list(range(25, 33)))
        for position, number in enumerate(sequence):
            if 25 <= number <= 32:
                self.assertEqual(10, sequence[position - 1], number)

    def test_causal_observations(self) -> None:
        actions = {a["label"]: a for a in self.evidence["runtime"]["observations"]["runs"]["laser-tombstone"]["named_action_observations"]}
        expected = {17: [22], 38: [6], 52: [7], 55: [5], 18: [], 25: [], 26: []}
        for label, action in actions.items():
            match = re.search(r"Laser Kick Test: close public switch (\d+)", label)
            if match:
                self.assertEqual(expected[int(match.group(1))], action["transitioned_solenoid_addresses"], label)
        self.assertEqual([15], actions["Tombstone Test: hold Start 2.5 s"]["transitioned_solenoid_addresses"])
        printer = self.evidence["runtime"]["observations"]["runs"]["printer-interface"]["named_action_observations"][0]
        self.assertEqual([40, 42, 43, 44], printer["transitioned_solenoid_addresses"])

    def test_no_printer_line_moves_outside_the_printer_run(self) -> None:
        for name, run in self.evidence["runtime"]["observations"]["runs"].items():
            seen = set(run["solenoid_addresses_seen"])
            if name != "printer-interface":
                self.assertFalse(seen & set(range(37, 45)), name)

    def test_every_snapshot_is_attributed_to_a_frame_digest(self) -> None:
        snapshots = self.evidence["runtime"]["observations"]["diagnostic_snapshots"]
        self.assertEqual(179, len(snapshots))
        for snapshot in snapshots:
            self.assertRegex(snapshot["pixel_sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(snapshot["interpreted_text"])
        by_label = {s["label"]: s for s in snapshots}
        self.assertEqual("-ACTIVE SWITCH TEST- | NONE", by_label["Active Switch Test baseline, every public switch at 0"]["interpreted_text"])
        self.assertIn("LEFT OUTLANE", by_label["Active Switch Test, public switch 17 held 900 ms"]["interpreted_text"])

    def test_the_facts_file_matches_the_readings(self) -> None:
        import tftc_readings as readings

        for address, (name, _, _) in readings.SWITCH_READINGS.items():
            self.assertEqual(name, self.facts["rom_switch_names"][str(address)]["name"])
        for address, (name, _, _) in readings.LAMP_READINGS.items():
            self.assertEqual(name, self.facts["rom_lamp_names"][str(address)]["name"])
        self.assertEqual(21 + 8, len(self.facts["rom_coil_names"]))

    def test_the_title_templates_are_distinct(self) -> None:
        templates = load_json(ROOT / "tools/tftc_header_templates.json")
        masks = {(tuple(v["rows"]), v["mask"]) for v in templates.values()}
        self.assertEqual(len(templates), len(masks))
        self.assertIn("ACTIVE SWITCH TEST", templates)

    def test_every_scenario_validates_and_is_the_one_the_evidence_ran(self) -> None:
        for run in self.evidence["runtime"]["raw_runs"]:
            path = ROOT / run["scenario_path"]
            self.assertEqual(run["scenario_sha256"], sha256_file(path), run["name"])
            scenario = load_json(path)
            self.assertEqual("tftc_303", scenario["game"])
            self.assertEqual(run["action_count"], len(scenario["actions"]))
            self.assertFalse([a for a in scenario["actions"] if a["type"] in ("pulse_key", "set_key")], "named keys would enable keyboard handling")


def _root_from_env(variable: str) -> Path | None:
    value = os.environ.get(variable)
    if not value:
        return None
    path = Path(value)
    return path if path.is_dir() else None


@unittest.skipUnless(
    _root_from_env("PINMAME_VPX_SOURCES_ROOT") and _root_from_env("PINMAME_MANUALS_ROOT") and _root_from_env("PINMAME_REVIEW_ARTIFACTS_ROOT"),
    "retained evidence roots are not configured",
)
class RetainedEvidenceTests(unittest.TestCase):
    """Prove the recorded digests describe the artifacts actually retained."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.sources = {s["id"]: s for s in cls.definition["sources"]}
        cls.vpx = _root_from_env("PINMAME_VPX_SOURCES_ROOT") / "data-east/tales-from-the-crypt/vpw-1.01"
        cls.manuals = _root_from_env("PINMAME_MANUALS_ROOT") / "by-machine" / KEY
        cls.reviews = _root_from_env("PINMAME_REVIEW_ARTIFACTS_ROOT")

    def test_manual_table_and_script_digests(self) -> None:
        self.assertEqual(self.sources["manual.data-east.tales-from-the-crypt.1993"]["sha256"], sha256_file(self.manuals / "Data_East_1993_Tales_from_the_Crypt_Manual.pdf"))
        self.assertEqual(self.sources["vpx-table.tales-from-the-crypt-vpw-1-01"]["sha256"], sha256_file(self.vpx / "Tales from the Crypt (Data East 1993)_VPW_V1.01.vpx"))
        self.assertEqual(self.sources["vpx-script.tales-from-the-crypt-vpw-1-01"]["sha256"], sha256_file(self.vpx / "extracted/script.vbs"))
        self.assertEqual(self.sources["ipdb.data-east.tales-from-the-crypt.1993"]["sha256"], sha256_file(self.manuals / "ipdb-2493.html"))

    def test_extraction_manifest_is_recomputable(self) -> None:
        import build_external_evidence_manifest as manifest

        digest = manifest.check_manifest(self.vpx / "extracted", "tftc_400")
        self.assertEqual(self.sources["vpx-extraction.tales-from-the-crypt-vpw-1-01"]["sha256"], digest)

    def test_runtime_runs_are_the_ones_recorded(self) -> None:
        import build_external_evidence_manifest as manifest

        evidence = load_json(EVIDENCE_PATH)
        base = self.reviews / "data-east.tales-from-the-crypt.1993/session-20261002/final/tftc_303"
        self.assertEqual(evidence["source"]["sha256"], manifest.check_manifest(base, "tftc_303"))
        for run in evidence["runtime"]["raw_runs"]:
            self.assertEqual(run["sha256"], sha256_file(base / run["name"] / "run.json"), run["name"])
        library = load_json(base / "active-switches/run.json")["library_sha256"]
        self.assertEqual(evidence["runtime"]["emulator"]["sha256"], library)

    def test_rom_archive_digest_and_members(self) -> None:
        import zipfile

        evidence = load_json(EVIDENCE_PATH)
        rom_root = os.environ.get("PINMAME_ROM_LIBRARY_ROOT")
        if not rom_root:
            self.skipTest("PINMAME_ROM_LIBRARY_ROOT is not set")
        archive = Path(rom_root) / "tftc_303.zip"
        self.assertEqual(evidence["runtime"]["rom_archive_sha256"], sha256_file(archive))
        with zipfile.ZipFile(archive) as zf:
            crcs = {info.filename: f"{info.CRC:08x}" for info in zf.infolist()}
        self.assertEqual("e9bec98e", crcs["tftccpua.303"])
        self.assertEqual("3888d06f", crcs["tftcdspa.301"])

    def test_cited_script_lines_say_what_the_curator_claims(self) -> None:
        lines = (self.vpx / "extracted/script.vbs").read_bytes().decode("utf-8", "replace").split("\n")

        def line(number: int) -> str:
            return lines[number - 1]

        self.assertIn("LoadVPM", line(264))
        self.assertIn("SolCallback(sLRFlipper)", line(297))
        self.assertIn("SolCallback(sLLFlipper)", line(298))
        self.assertIn("Sol1 = 15", line(1671))
        self.assertIn("AddSw 33, 160, 180", line(1676))
        self.assertIn("AddSw 36, 0, 20", line(1677))
        self.assertIn("InitDrop Array(sw41, sw42, sw43)", line(1662))
        self.assertIn("HandleMechanics=0", line(1641).replace(" ", ""))
        self.assertIn("HandleKeyboard=0", line(1642).replace(" ", ""))
        self.assertIn("KeyDownHandler", line(1737))
        self.assertIn("KeyUpHandler", line(1811))
        self.assertIn("Controller.Switch(62) = 1", line(1712))
        self.assertIn("Sub SolShake", line(1573))
        self.assertIn("Sub SolDiv", line(1542))
        self.assertIn("Sub Solkickback", line(1603))
        self.assertIn("pulsesw 37", line(2684).lower())
        self.assertIn("Lampz.MassAssign(15)= l15", line(3043))
        for address, number in zip(range(25, 33), range(288, 296)):
            self.assertIn(f"SolCall", line(number).replace("Callback", "Call"), address)
        for switch, number in ((17, 2388), (23, 2392), (26, 2398), (45, 2421), (47, 2466), (57, 2499), (49, 2629), (50, 2641), (51, 2652)):
            self.assertIn(f"{switch}", line(number), switch)

    def test_the_placements_equal_the_extraction(self) -> None:
        places = load_json(PLACES_PATH)
        items = self.vpx / "extracted/gameitems"
        for key, hits in places["placements"].items():
            for hit in hits:
                matches = list(items.glob(f"*.{hit['object']}.json"))
                self.assertEqual(1, len(matches), hit["object"])
                body = list(json.loads(matches[0].read_text(encoding="utf-8")).values())[0]
                if hit["coordinate_origin"] == "measured-center":
                    point = body.get("center") or body.get("position")
                    self.assertAlmostEqual(point["x"], hit["raw"]["x"], places=5, msg=key)
                    self.assertAlmostEqual(point["y"], hit["raw"]["y"], places=5, msg=key)
                else:
                    points = body["drag_points"]
                    self.assertAlmostEqual(sum(p["x"] for p in points) / len(points), hit["raw"]["x"], places=5, msg=key)


if __name__ == "__main__":
    unittest.main()
