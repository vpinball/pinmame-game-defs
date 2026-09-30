from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOTS = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_who_dunnit as curator  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def addresses(definition: dict, collection: str, group: str) -> dict[int, dict]:
    return {item["binding"]["device"]: item for item in definition[collection]
            if item["binding"]["group"] == group}


class WhoDunnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = read(curator.PARTIAL)
        cls.switches = addresses(cls.definition, "inputs", "pinmame.input.switch")
        cls.dips = addresses(cls.definition, "inputs", "pinmame.input.dip")
        cls.solenoids = addresses(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = addresses(cls.definition, "outputs", "pinmame.output.lamp")
        cls.gi = addresses(cls.definition, "outputs", "pinmame.output.gi")

    def test_driver_identity_and_honest_gate(self) -> None:
        definition = self.definition
        self.assertEqual("bally.who-dunnit.1995", definition["machine"]["id"])
        self.assertEqual(3685, definition["machine"]["ipdb_id"])
        self.assertEqual("0x40", definition["controller"]["hardware_generation"])
        self.assertEqual(set(curator.DRIVERS), {item["id"] for item in definition["drivers"]})
        catalog = read(ROOT / "catalog/pinmame.json")
        self.assertEqual(set(curator.DRIVERS), {item["id"] for item in catalog["drivers"]
                                                if item["machine_id"] == definition["machine"]["id"]})
        self.assertEqual("partial", definition["coverage"]["status"])
        self.assertIn("spatial_placement", definition["coverage"]["missing"])
        self.assertIn("unresolved_conflicts", definition["coverage"]["missing"])
        self.assertFalse(curator.READY.exists())

    def test_full_public_addresses_including_cpu_dips(self) -> None:
        matrix = {col * 10 + row for col in range(1, 9) for row in range(1, 9)}
        self.assertEqual(set(range(1, 9)) | matrix | set(range(111, 119)), set(self.switches))
        self.assertEqual(set(range(1, 9)), set(self.dips))
        self.assertEqual(set(range(1, 51)), set(self.solenoids))
        self.assertEqual(matrix, set(self.lamps))
        self.assertEqual(set(range(5)), set(self.gi))
        self.assertEqual((88, 119, 11), (len(self.definition["inputs"]), len(self.definition["outputs"]), len(self.definition["mechanisms"])))
        self.assertEqual("dip_switch", self.dips[8]["spatial"]["reason"])

    def test_manual_switches_and_emulator_normalization(self) -> None:
        optos = {address for address in self.switches if address in curator.OPTO}
        self.assertEqual({12, 25, *range(31, 38), *range(41, 45), 47, 48}, optos)
        self.assertTrue(all(self.switches[address]["normally_closed"] for address in optos))
        self.assertTrue(all(self.switches[address]["physical"]["switch_type"] == "opto" for address in optos))
        self.assertIn("Unshaded", self.switches[12]["physical"]["notes"])
        shaded = {25, *range(31, 38), *range(41, 45), 47, 48}
        for address in shaded:
            self.assertIn("Printed shaded opto cell", self.switches[address]["physical"]["notes"])
            self.assertNotIn("Unshaded", self.switches[address]["physical"]["notes"])
        excerpt = (curator.EXCERPTS / "switch-matrix.md").read_text(encoding="utf-8")
        markers = {int(value) for value in re.findall(r"\| (\d{2}) O \|", excerpt)}
        self.assertEqual(shaded, markers)
        self.assertEqual("constant", self.switches[24]["kind"])
        self.assertTrue(self.switches[24]["constant_active"])
        self.assertEqual("candidate", self.switches[115]["spatial"]["status"])
        self.assertEqual((0.837256, 0.356449), (self.switches[115]["spatial"]["placements"][0]["x"],
                                                   self.switches[115]["spatial"]["placements"][0]["y"]))
        self.assertIn(curator.RUNTIME_SRC, self.switches[115]["provenance"]["source_refs"])

    def test_lower_eos_factory_construction_is_distinct_from_synthesized_transport(self) -> None:
        sources = {source["id"]: source for source in self.definition["sources"]}
        locator = sources[curator.FLIPPER_PART_SRC]["locator"]
        for reading in ("item 2 as SW-1A-194 Switch Assembly", "generic PDF 98 Flipper Notes block (Notes 2/4)",
                        "0.062 (+/- 0.015) inch", "PDF 99 item 2 identifies the same SW-1A-194 part"):
            self.assertIn(reading, locator)
        self.assertNotIn("Note 1", locator)
        expected = {
            111: ("A-14876-R-5", "F1", "J906-1"),
            113: ("A-15849-L-4", "F3", "J906-3"),
        }
        for address, (assembly, manual_address, connector) in expected.items():
            switch = self.switches[address]
            self.assertFalse(switch["normally_closed"])
            self.assertEqual("leaf", switch["physical"]["switch_type"])
            self.assertEqual("SW-1A-194", switch["physical"]["part_number"])
            self.assertEqual(connector, switch["wiring"]["control_connection"])
            self.assertEqual(manual_address, switch["aliases"][1]["value"])
            self.assertEqual("validated", switch["provenance"]["status"])
            self.assertIn(curator.FLIPPER_PART_SRC, switch["provenance"]["source_refs"])
            self.assertNotIn(curator.RUNTIME_SRC, switch["provenance"]["source_refs"])
            self.assertIn(assembly, switch["physical"]["notes"])
            self.assertIn("generic PDF 98 Flipper Notes block (Notes 2/4)", switch["physical"]["notes"])
            self.assertIn("normally-open physical rest leaf contact", switch["physical"]["notes"])
            self.assertIn("does not measure live physical travel, current or timing", switch["physical"]["notes"])
        self.assertEqual("opto", self.switches[112]["physical"]["switch_type"])
        self.assertEqual("opto", self.switches[114]["physical"]["switch_type"])
        excerpt = (curator.EXCERPTS / "flipper-circuits.md").read_text(encoding="utf-8")
        self.assertIn("## Lower E.O.S. switch construction", excerpt)
        self.assertIn("The note block occurs on PDF 98; PDF 99", excerpt)
        self.assertIn("| 4 | 4105-01019-10 | 4105-01019-10 | Sh. Metal Screw, #5 x 5/8 inch |", excerpt)
        self.assertIn("| 18g | 4410-01132-00 | 4410-01132-00 | Nut 10-32 ESN |", excerpt)
        self.assertNotIn("4105-0119-10", excerpt)
        self.assertNotIn("4401-01132-00", excerpt)
        for mechanism_id in ("mechanism.lower-right-flipper", "mechanism.lower-left-flipper"):
            mechanism = next(item for item in self.definition["mechanisms"] if item["id"] == mechanism_id)
            self.assertIn("leaf contact open at physical rest", mechanism["behavior"])
            self.assertIn("does not measure live travel, current or timing", mechanism["behavior"])

    def test_manual_bulbs_reels_and_flipper_circuits(self) -> None:
        for address in (56, 57, 58):
            self.assertEqual("24-8768", self.lamps[address]["physical"]["part_number"])
            self.assertEqual("A-20527", self.lamps[address]["physical"]["assembly_part_number"])
        self.assertEqual("J138-7", self.lamps[71]["wiring"]["drive_connection"])
        self.assertEqual("J138-9", self.lamps[81]["wiring"]["drive_connection"])
        self.assertEqual("J902-1 playfield", self.solenoids[36]["wiring"]["drive_connection"])
        self.assertEqual("Fliptronic II board A-15472-1", self.solenoids[36]["wiring"]["board"])
        for address in range(37,45):
            self.assertEqual("unknown",self.solenoids[address]["availability"])
            self.assertEqual("virtual",self.solenoids[address]["spatial"]["reason"])
            self.assertIn("remain unproven",self.solenoids[address]["physical"]["notes"])
        self.assertEqual(["29"], [a["value"] for a in self.solenoids[45]["aliases"]
                                   if a["namespace"] == "manual.solenoid"])
        self.assertEqual("J902-13", self.solenoids[45]["wiring"]["drive_connection"])
        self.assertEqual("J902-7", self.solenoids[48]["wiring"]["drive_connection"])
        expected={45:("Q4","J902-13","Yel-Grn","J907-1","Red-Grn","A-14876-R-5"),
                  46:("Q11","J902-11","Org-Grn","J907-1","Red-Grn","A-14876-R-5"),
                  47:("Q3","J902-9","Yel-Blu","J907-4","Red-Blu","A-15849-L-4"),
                  48:("Q9","J902-7","Org-Blu","J907-4","Red-Blu","A-15849-L-4")}
        for address,(driver,connector,wire,feed,feed_wire,assembly) in expected.items():
            output=self.solenoids[address]
            self.assertNotIn("part_number",output["physical"])
            self.assertEqual("conflicted",output["provenance"]["status"])
            self.assertEqual(assembly,output["physical"]["assembly_part_number"])
            self.assertEqual((driver,connector,wire,feed,feed_wire),
                             tuple(output["wiring"][key] for key in ("driver_transistor","drive_connection","drive_wire","power_connection","power_wire")))
        flippers={m["id"]:m for m in self.definition["mechanisms"] if "flipper" in m["id"]}
        self.assertEqual({"mechanism.lower-right-flipper","mechanism.lower-left-flipper"},set(flippers))
        self.assertEqual((["solenoid.45","solenoid.46"],["switch.fliptronic-111","switch.fliptronic-112"]),
                         (flippers["mechanism.lower-right-flipper"]["actuators"],flippers["mechanism.lower-right-flipper"]["sensors"]))
        self.assertEqual((["solenoid.47","solenoid.48"],["switch.fliptronic-113","switch.fliptronic-114"]),
                         (flippers["mechanism.lower-left-flipper"]["actuators"],flippers["mechanism.lower-left-flipper"]["sensors"]))
        self.assertIn("construction",flippers["mechanism.lower-right-flipper"]["behavior"])
        for mechanism in flippers.values():
            self.assertEqual("conflicted", mechanism["provenance"]["status"])
            self.assertIn("FL-15411", mechanism["behavior"])
            self.assertIn("FL-11541", mechanism["behavior"])
            self.assertIn(curator.RUNTIME_SRC, mechanism["provenance"]["source_refs"])
        for address in (23, 24, 25, 26, 27, 28):
            self.assertEqual("14-8024 12V", self.solenoids[address]["physical"]["part_number"])
            notes = self.solenoids[address]["physical"]["notes"]
            self.assertIn("A-19745-1 Stepper Motor PCB w/Spacers (3)", notes)
            self.assertIn("A-19043-1", notes)
            self.assertIn("relationship and identical assembly identity are unverified", notes)
        self.assertEqual("24-8704", self.solenoids[18]["physical"]["part_number"])
        self.assertEqual(3, self.solenoids[20]["physical"]["quantity"])
        self.assertEqual("24-6549", self.gi[0]["physical"]["part_number"])
        self.assertEqual("24-8768", self.gi[4]["physical"]["part_number"])
        self.assertEqual(["solenoid.23", "solenoid.24"],
                         next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.left-reel")["actuators"])

    def test_pdf_128_solenoid_table_is_complete_and_separate_from_gi(self) -> None:
        rows = curator.solenoid_table()
        self.assertEqual(set(range(1, 29)) | {36}, set(rows))
        expected = {
            1: ("Q82", "J130-1 playfield", "Vio-Brn", "AE-26-1500"),
            2: ("Q80", "J130-2 playfield", "Vio-Red", "AE-23-800"),
            3: ("Q78", "J130-4 playfield", "Vio-Org", "AE-27-1200"),
            4: ("Q76", "J130-5 playfield", "Vio-Yel", "AE-24-900"),
            5: ("Q64", "J130-6 playfield", "Vio-Grn", "AE-26-1200"),
        }
        for address, (transistor, connector, wire, part) in expected.items():
            self.assertEqual(("J107-2 playfield", transistor, connector, wire, part),
                             tuple(rows[address][index] for index in (3, 4, 5, 6, 7)))
            output = self.solenoids[address]
            self.assertEqual("WPC Security Power Driver Board", output["wiring"]["board"])
            self.assertEqual(("J107-2 playfield", transistor, connector, wire),
                             tuple(output["wiring"][key] for key in
                                   ("power_connection", "driver_transistor", "drive_connection", "drive_wire")))
            self.assertEqual(part, output["physical"]["part_number"])
        self.assertEqual(("J121-1", "J121-7", "24-6549"),
                         (self.gi[0]["wiring"]["power_connection"], self.gi[0]["wiring"]["return_connection"],
                          self.gi[0]["physical"]["part_number"]))

    def test_solenoid_table_rejects_duplicate_incomplete_or_unrecognized_table(self) -> None:
        source = (curator.EXCERPTS / "solenoid-flasher.md").read_text(encoding="utf-8")
        header = "| No. | Function | Printed type | Voltage connector | Drive transistor | Drive connector | Wire | Fitted device |"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "solenoid-flasher.md"
            path.write_text(source.replace("| 02 | Plunger |", "| 01 | Plunger |", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate printed solenoid address 1"):
                curator.solenoid_table(path)
            incomplete = "\n".join(line for line in source.splitlines()
                                   if not line.startswith("| 36 | Up Down Post |")) + "\n"
            path.write_text(incomplete, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "incomplete printed WHO dunnit solenoid table"):
                curator.solenoid_table(path)
            path.write_text(source.replace(header, "| Circuit | Function | Printed type | Voltage connector | Drive transistor | Drive connector | Wire | Fitted device |", 1), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing required WHO dunnit Solenoid/Flasher table header"):
                curator.solenoid_table(path)

    def test_fliptronic_runtime_provenance_is_limited_to_exercised_inputs(self) -> None:
        runtime_inputs = {address for address in range(111, 119)
                          if curator.RUNTIME_SRC in self.switches[address]["provenance"]["source_refs"]}
        self.assertEqual({112, 114, 115}, runtime_inputs)
        self.assertEqual("unused", self.switches[117]["availability"])
        for address in (45, 46, 47, 48):
            self.assertIn(curator.RUNTIME_SRC, self.solenoids[address]["provenance"]["source_refs"])

    def test_real_factory_conflict_is_fail_closed(self) -> None:
        self.assertNotIn("part_number", self.solenoids[13]["physical"])
        conflicts = self.definition["conflicts"]
        self.assertEqual(6, len(conflicts))
        by_id={conflict["id"]:conflict for conflict in conflicts}
        for conflict in conflicts:
            self.assertEqual("unresolved", conflict["status"])
            self.assertIn("Resolution path:", conflict["description"])
            self.assertEqual(2,len(set(conflict["source_refs"])))
        jet=by_id["conflict.right-jet-coil-part"]
        self.assertIn("AE-26-1500", jet["description"])
        self.assertIn("AE-26-1200", jet["description"])
        lamps=by_id["conflict.lamp-matrix-connectors"]
        for reading in ("J137-1..6","J133-1,2,4..9","J133 Not Used","J137 Not Used",
                        "J138-1..7/9","J138-8 Key","J135-1,2,4..9","J134-7..9","J136-3"):
            self.assertIn(reading,lamps["description"])
        for lamp in self.lamps.values():
            self.assertEqual("conflicted",lamp["provenance"]["status"])
            self.assertIn(curator.LAMP_CONNECTOR_SRC,lamp["provenance"]["source_refs"])
            self.assertIn("not settled physical wiring",lamp["physical"]["notes"])
            self.assertIn("PDF 159 (3-27) lists", lamp["physical"]["notes"])
            self.assertIn("J138-7/column 7 and J138-9/column 8", lamp["physical"]["notes"])
            self.assertIn("J138-8 is a key", lamp["physical"]["notes"])
            self.assertNotIn("instead lists", lamp["physical"]["notes"])
        self.assertEqual("J137-1",self.lamps[11]["wiring"]["drive_connection"])
        self.assertEqual("J133-1",self.lamps[11]["wiring"]["return_connection"])
        self.assertIn("J134-8",self.lamps[87]["physical"]["notes"])
        self.assertIn("J134-9",self.lamps[88]["physical"]["notes"])
        opto=by_id["conflict.left-flipper-opto-wire"]
        self.assertIn("Black-Gray",opto["description"])
        self.assertIn("Blue-Gray",opto["description"])
        self.assertEqual("conflicted",self.switches[114]["provenance"]["status"])
        self.assertEqual("J905-2",self.switches[114]["wiring"]["control_connection"])
        self.assertNotIn("control_wire",self.switches[114]["wiring"])
        self.assertEqual("conflicted",self.definition["coverage"]["dimensions"]["physical_wiring"])
        flippers = by_id["conflict.lower-flipper-coil-part"]
        self.assertEqual({curator.FLIPPER_PART_SRC, curator.DUPLICATE_TABLE_SRC}, set(flippers["source_refs"]))
        for reading in ("PDF 98–99", "PDF 128–129", "PDF 137", "FL-15411", "FL-11541"):
            self.assertIn(reading, flippers["description"])
        for address in (45, 46, 47, 48):
            self.assertTrue(set(flippers["source_refs"]) <= set(self.solenoids[address]["provenance"]["source_refs"]))
            self.assertIn("no physical coil part number is selected", self.solenoids[address]["physical"]["notes"])

    def test_gi_table_claims_do_not_become_board_confirmed_locations(self) -> None:
        expected = (("J121-1", "J121-7", "24-6549", "playfield"),
                    ("J121-2", "J121-8", "24-6549", "playfield"),
                    ("J121-3", "J121-9", "24-6549", "playfield"),
                    ("J120-5", "J120-10", "24-8768", "backbox"),
                    ("J120-6", "J120-11", "24-8768", "backbox"))
        for address, (power, ret, bulb, location) in enumerate(expected):
            output = self.gi[address]
            self.assertEqual((power, ret), (output["wiring"]["power_connection"], output["wiring"]["return_connection"]))
            self.assertEqual((bulb, location), (output["physical"]["part_number"], output["physical"]["location"]))
            self.assertEqual("candidate", output["provenance"]["status"])
            self.assertIn(curator.LAMP_CONNECTOR_SRC, output["provenance"]["source_refs"])
            self.assertIn("J112–J127 pin destinations are omitted", output["physical"]["notes"])
            self.assertIn("Public bindings come separately", output["physical"]["notes"])
            if address >= 3:
                self.assertEqual("not_applicable", output["spatial"]["status"])
                self.assertEqual("cabinet_or_service", output["spatial"]["reason"])
                self.assertEqual("candidate", output["spatial"]["provenance"]["status"])
            else:
                self.assertEqual("candidate", output["spatial"]["status"])
        self.assertFalse(any("gi.string" in conflict["path"] for conflict in self.definition["conflicts"]))
        report = read(curator.REPORT)
        self.assertIn("backbox exclusions remain candidate", report["projection_classes"]["gi"])

    def test_applicable_bulb_legend_is_retained_in_hashed_excerpt(self) -> None:
        excerpt = (curator.EXCERPTS / "solenoid-flasher.md").read_text(encoding="utf-8")
        self.assertEqual({("24-6549", "#44"), ("24-8704", "#89"),
                          ("24-8768", "#555"), ("24-8802", "#906")},
                         set(re.findall(r"^\| (24-\d+) \| (#\d+) \|$", excerpt, re.MULTILINE)))

    def test_reel_connector_claims_remain_source_specific(self) -> None:
        conflict = next(item for item in self.definition["conflicts"]
                        if item["id"] == "conflict.reel-drive-connectors")
        self.assertEqual({curator.REEL_TABLE_SRC, curator.REEL_BOARD_SRC}, set(conflict["source_refs"]))
        sources = {source["id"]: source for source in self.definition["sources"]}
        self.assertIn("PDF page 128, printed 2-46", sources[curator.REEL_TABLE_SRC]["locator"])
        self.assertIn("PDF page 155, printed 3-23", sources[curator.REEL_BOARD_SRC]["locator"])
        expected = {23: ("J126-7", "J122-3", "Blue-Orange"),
                    24: ("J126-8", "J122-4", "Blue-Yellow"),
                    27: ("J122-3", "J126-7", "Blue-Violet"),
                    28: ("J122-4", "J126-8", "Blue-Gray")}
        for address, (table_pin, board_pin, board_wire) in expected.items():
            output = self.solenoids[address]
            self.assertEqual(f"{table_pin} playfield", output["wiring"]["drive_connection"])
            self.assertEqual("conflicted", output["provenance"]["status"])
            self.assertTrue(set(conflict["source_refs"]) <= set(output["provenance"]["source_refs"]))
            self.assertIn(f"{board_pin} {board_wire}", output["physical"]["notes"])
            self.assertIn("not a physical connector choice", output["physical"]["notes"])
        for address, connector in ((25, "J122-1"), (26, "J122-2")):
            self.assertEqual(f"{connector} playfield", self.solenoids[address]["wiring"]["drive_connection"])
            self.assertEqual("validated", self.solenoids[address]["provenance"]["status"])

    def test_auxiliary_opto_fitment_does_not_inherit_keyboard_proof(self) -> None:
        self.assertEqual("J905-1", self.switches[112]["wiring"]["control_connection"])
        self.assertEqual("J905-2", self.switches[114]["wiring"]["control_connection"])
        conflict = next(item for item in self.definition["conflicts"]
                        if item["id"] == "conflict.auxiliary-flipper-opto-fitment")
        self.assertIn("PDF 126 (printed 2-44)", conflict["description"])
        self.assertIn("PDF 157 (printed 3-25)", conflict["description"])
        for address, connector, wire in ((116, "J905-3", "Black-Yellow"),
                                         (118, "J905-5", "Black-Blue")):
            switch = self.switches[address]
            self.assertEqual("unknown", switch["availability"])
            self.assertEqual("unknown", switch["physical"]["switch_type"])
            self.assertEqual("candidate", switch["provenance"]["status"])
            self.assertEqual((connector, wire), (switch["wiring"]["control_connection"],
                                               switch["wiring"]["control_wire"]))
            self.assertNotIn("normally_closed", switch)
            self.assertNotIn("part_number", switch["physical"])
            self.assertNotIn(curator.RUNTIME_SRC, switch["provenance"]["source_refs"])
            self.assertIn(curator.CORE_ARTIFACTS["src/wpc/core.c"][0], switch["provenance"]["source_refs"])
            self.assertIn("only inside if(g_fHandleKeyboard)", switch["physical"]["notes"])
            self.assertIn("physical usage, ROM consumption and polarity remain unproven", switch["physical"]["notes"])
            self.assertEqual("cabinet_or_service", switch["spatial"]["reason"])
            self.assertEqual("candidate", switch["spatial"]["provenance"]["status"])
        self.assertEqual("unused", self.switches[117]["availability"])
        for address in (33, 34, 35):
            self.assertEqual("unused", self.solenoids[address]["availability"])

    def test_relied_core_artifacts_are_pinned_and_mismatch_rejected(self) -> None:
        sources={source["id"]:source for source in self.definition["sources"]}
        self.assertEqual({"wd.c","core.c","wpc.c","core.h"},{Path(path).name for path in curator.CORE_ARTIFACTS})
        for path,(source_id,digest,_) in curator.CORE_ARTIFACTS.items():
            source=sources[source_id]
            self.assertEqual(curator.PIN,source["revision"])
            self.assertEqual(digest,source["sha256"])
            self.assertTrue(source["uri"].endswith(f"/{curator.PIN}/{path}"))
            self.assertIn(source_id,self.solenoids[45]["provenance"]["source_refs"])
        configured_root = next((os.environ[name] for name in EVIDENCE_ROOTS if os.environ.get(name)), None)
        if configured_root:
            source_id, _, locator = curator.CORE_ARTIFACTS["src/wpc/core.h"]
            with patch.dict(curator.CORE_ARTIFACTS, {"src/wpc/core.h": (source_id, "0" * 64, locator)}):
                for name in EVIDENCE_ROOTS:
                    supplied = {root: configured_root if root == name else "" for root in EVIDENCE_ROOTS}
                    with self.subTest(root=name), patch.dict(os.environ, supplied):
                        with self.assertRaisesRegex(RuntimeError, "core artifact missing or mismatch: src/wpc/core.h"):
                            curator.verify_external()

    def test_core_check_is_required_by_each_evidence_root_only(self) -> None:
        with patch.dict(os.environ, {}, clear=True), patch.object(curator, "verify_core_checkout") as check:
            curator.verify_external()
            check.assert_not_called()
        for name in EVIDENCE_ROOTS:
            with self.subTest(root=name), patch.dict(os.environ, {name: "supplied"}, clear=True):
                with patch.object(curator, "verify_core_checkout", side_effect=RuntimeError("core check required")) as check:
                    with self.assertRaisesRegex(RuntimeError, "core check required"):
                        curator.verify_external()
                    check.assert_called_once_with()
        with tempfile.TemporaryDirectory() as directory:
            for name in EVIDENCE_ROOTS:
                with self.subTest(missing_core_root=name), patch.dict(os.environ, {name: directory}, clear=True):
                    with patch.object(curator, "resolve_working_root", return_value=Path(directory)):
                        with self.assertRaisesRegex(RuntimeError, "core checkout missing"):
                            curator.verify_external()

    def test_exact_local_artifacts_and_determinism(self) -> None:
        self.assertEqual(curator.PARTIAL.read_bytes(), curator.SEED.read_bytes())
        self.assertEqual(canonical_bytes(curator.build()), curator.PARTIAL.read_bytes())
        self.assertEqual(curator.KNOWLEDGE_SEED.read_bytes(),curator.KNOWLEDGE.read_bytes())
        report=read(curator.REPORT)
        self.assertEqual((47,46,0),(len(report["geometry_candidates"]),len(report["projected_device_ids"]),len(report["without_placements"])))
        self.assertIn("rejected",report["projection_classes"]["manual_drawing"])
        self.assertEqual("direct_flipper_pivot",next(c for c in report["geometry_candidates"] if c["device_id"]=="solenoid.45")["projection_class"])
        self.assertEqual("effect",self.solenoids[17]["spatial"]["placements"][0]["role"])
        self.assertEqual("effect",self.switches[12]["spatial"]["placements"][0]["role"])
        self.assertEqual("sensor",self.switches[66]["spatial"]["placements"][0]["role"])
        for source in self.definition["sources"]:
            if source["id"] == curator.MANUAL_SRC:
                for excerpt in source["excerpts"]:
                    data = (ROOT / excerpt["path"]).read_bytes()
                    self.assertEqual(hashlib.sha256(data).hexdigest(), excerpt["sha256"])
        curator.check()

    def test_knowledge_note_drift_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            changed=Path(directory)/"who-dunnit-1995.md"
            changed.write_bytes(curator.KNOWLEDGE_SEED.read_bytes()+b"unexpected drift\n")
            with patch.object(curator,"KNOWLEDGE",changed):
                with self.assertRaisesRegex(RuntimeError,"deterministic artifact drift"):
                    curator.check()

    def test_geometry_seed_and_supplied_source_mismatch_fail_closed(self) -> None:
        seed=read(curator.GEOMETRY_SEED)
        with tempfile.TemporaryDirectory() as directory:
            bad=Path(directory)/"geometry.json"
            seed["candidates"][0]["normalized_playfield"]["x"]=-1
            bad.write_text(json.dumps(seed),encoding="utf-8")
            with patch.object(curator,"GEOMETRY_SEED",bad):
                with self.assertRaisesRegex(ValueError,"invalid WHO dunnit geometry candidate"):
                    curator.geometry_candidates()
            if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
                seed["candidates"][0]["normalized_playfield"]["x"]=round(seed["candidates"][0]["raw_vpu"]["x"]/953,6)
                seed["candidates"][0]["projection_class"]="wrong_class"
                bad.write_text(json.dumps(seed),encoding="utf-8")
                with patch.object(curator,"GEOMETRY_SEED",bad):
                    with self.assertRaisesRegex(RuntimeError,"differ from pinned measurements"):
                        curator.verify_external()

    def test_external_source_roots_when_configured(self) -> None:
        if not all(os.environ.get(name) for name in EVIDENCE_ROOTS):
            self.skipTest("retained external roots not configured")
        curator.verify_external()
        base = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / curator.MID / "session-20260930/sol-runtime"
        expected = {"bank": {22}, "ramp-up": {16}, "ramp-down": {5}, "reels": {23, 24, 25, 26, 27, 28}}
        for key, outputs in expected.items():
            name = curator.SOL_RUNTIME[key][0]
            trace = read(base / "traces" / f"{name}.json")
            scenario = read(base / "scenarios" / f"{name}.json")
            self.assertIsNone(trace["failure"], key)
            self.assertFalse(any(action["type"] in {"pulse_key", "set_key"} for action in scenario["actions"]), key)
            asserted = {event["number"] for event in trace["events"]
                        if event.get("event") == "solenoid" and event.get("state") == 1}
            self.assertTrue(outputs <= asserted, (key, asserted))
        curator.verify_opto_evidence(base)
        opto_source=next(source for source in self.definition["sources"] if source["id"]=="runtime.who-dunnit.optos.wd-12")
        for address,states in curator.OPTO_FRAMES.items():
            self.assertEqual({0,1},set(states))
            for state,(step,frame,digest) in states.items():
                self.assertIn(f"public {address} raw {state}, action/trace step {step}",opto_source["locator"])
                self.assertIn(f"DMD {frame} SHA-256 {digest}",opto_source["locator"])

    def test_supplied_missing_evidence_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ,{"PINMAME_REVIEW_ARTIFACTS_ROOT":directory},clear=True), patch.object(curator,"verify_core_checkout"):
                with self.assertRaises(FileNotFoundError):
                    curator.verify_external()

    def test_opto_release_frame_and_causal_mismatches_rejected(self) -> None:
        review_root=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not review_root:
            self.skipTest("retained runtime root not configured")
        base=Path(review_root)/curator.MID/"session-20260930/sol-runtime"
        curator.verify_opto_evidence(base)
        bad_frames=copy.deepcopy(curator.OPTO_FRAMES)
        step,frame,_=bad_frames[12][0]
        bad_frames[12][0]=(step,frame,"0"*64)
        with patch.object(curator,"OPTO_FRAMES",bad_frames):
            with self.assertRaisesRegex(RuntimeError,"DMD frame mismatch: 12 raw 0"):
                curator.verify_opto_evidence(base)
        original_load=curator.load_json
        for target,mutate,message in (
            ("scenarios",lambda result:result["actions"][9].update(state=1),"causal action/trace mismatch"),
            ("traces",lambda result:result["steps"][9].update(step=9),"causal action/trace mismatch"),
            ("traces",lambda result:next(e for e in result["events"] if e.get("event")=="switch" and e.get("step")==10).update(number=25),"causal switch event mismatch"),
            ("traces",lambda result:result["snapshots"][10]["displays"][0].update(artifact=result["snapshots"][9]["displays"][0]["artifact"]),"causal native frame mismatch"),
            ("traces",lambda result:result["snapshots"][10]["displays"][0].update(pixel_sha256="0"*64),"ROM pixel/trace mismatch"),
        ):
            with self.subTest(target=target,message=message):
                def changed_load(path: Path) -> dict:
                    result=original_load(path)
                    if path.parent.name==target:
                        mutate(result)
                    return result
                with patch.object(curator,"load_json",side_effect=changed_load):
                    with self.assertRaisesRegex(RuntimeError,message):
                        curator.verify_opto_evidence(base)


if __name__ == "__main__":
    unittest.main()
