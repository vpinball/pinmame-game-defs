from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines/partial/williams/no-good-gofers-1997.json"
SEED_PATH = ROOT / "tools/seeds/williams/no-good-gofers-1997.json"
SPATIAL_PATH = ROOT / "reports/spatial/williams/no-good-gofers-1997.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams/no-good-gofers-1997.md"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams/no-good-gofers-1997.json"

MATRIX = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
OPTO = {31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 44, 45, 46, 63, 64}
UNUSED = {11, 43, 87, 88}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bound(definition: dict, collection: str, group: str) -> dict[int, dict]:
    return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class NoGoodGofersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = read(DEFINITION_PATH)
        cls.switches = bound(cls.definition, "inputs", "pinmame.input.switch")
        cls.dips = bound(cls.definition, "inputs", "pinmame.input.dip")
        cls.solenoids = bound(cls.definition, "outputs", "pinmame.output.solenoid")
        cls.lamps = bound(cls.definition, "outputs", "pinmame.output.lamp")
        cls.gi = bound(cls.definition, "outputs", "pinmame.output.gi")

    def test_partial_status_is_fail_closed_and_not_promoted(self) -> None:
        coverage = self.definition["coverage"]
        self.assertEqual("partial", coverage["status"])
        self.assertEqual(["spatial_placement"], coverage["missing"])
        self.assertEqual("candidate", coverage["dimensions"]["spatial_placement"])
        self.assertFalse(AUTHOR_READY_PATH.exists())
        self.assertTrue(KNOWLEDGE_PATH.is_file())

    def test_complete_wpc95_input_and_output_contract_is_enumerated(self) -> None:
        self.assertEqual(set(range(1, 9)) | MATRIX | set(range(111, 119)), set(self.switches))
        self.assertEqual(set(range(1, 9)), set(self.dips))
        self.assertEqual(set(range(1, 59)), set(self.solenoids))
        self.assertEqual(MATRIX, set(self.lamps))
        self.assertEqual(set(range(5)), set(self.gi))
        for address in UNUSED:
            self.assertEqual("unused", self.switches[address]["availability"])
        self.assertEqual("constant", self.switches[24]["kind"])
        self.assertTrue(self.switches[24]["constant_active"])

    def test_opto_polarity_matches_manual_and_pinned_mask(self) -> None:
        for address in MATRIX - UNUSED - {24}:
            self.assertEqual(address in OPTO, self.switches[address]["normally_closed"], address)
        mask = (0x00, 0x00, 0x00, 0xFF, 0x3B, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00)
        normalized = {column * 10 + row for column in (3, 4, 6) for row in range(1, 9) if (mask[column] >> (row - 1)) & 1}
        self.assertEqual(OPTO, normalized)
        for address in (112, 114, 116):
            self.assertTrue(self.switches[address]["normally_closed"])

    def test_flipper_fitment_and_public_mapping_are_exact(self) -> None:
        for address in (111, 112, 113, 114, 115, 116):
            self.assertEqual("used", self.switches[address]["availability"])
        for address in (117, 118):
            self.assertEqual("unused", self.switches[address]["availability"])
        aliases = {address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"} for address in (33, 34, 35, 36, 45, 46, 47, 48)}
        self.assertEqual({"33"}, aliases[33]); self.assertEqual({"34"}, aliases[34]); self.assertEqual({"35"}, aliases[35]); self.assertEqual({"29"}, aliases[45]); self.assertEqual({"30"}, aliases[46]); self.assertEqual({"31"}, aliases[47]); self.assertEqual({"32"}, aliases[48])
        self.assertEqual("coil", self.solenoids[36]["kind"])

    def test_auxiliary_public_mapping_follows_working_vpx_and_core_custom_range(self) -> None:
        expected = {51: "42", 52: "43", 53: "44", 54: "45", 55: "46", 56: "47", 57: "48", 58: "49"}
        for public, manual in expected.items():
            aliases = {alias["value"] for alias in self.solenoids[public]["aliases"] if alias["namespace"] == "manual.address"}
            self.assertEqual({manual}, aliases, public)
            self.assertEqual("flasher", self.solenoids[public]["kind"])
        self.assertEqual([], self.definition["conflicts"])
        core = next(source for source in self.definition["sources"] if source["id"] == "pinmame.core.4ec52ff0ac13")
        self.assertIn("does not map or drive public state", core["locator"])

    def test_manual_inventory_has_64_lamps_and_exact_multi_bulb_quantities(self) -> None:
        for address in MATRIX:
            self.assertEqual("used", self.lamps[address]["availability"], address)
        for address in (13, 28, 55, 68, 71):
            self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
        self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])
        self.assertEqual("coil", self.solenoids[24]["kind"])
        self.assertEqual("flasher", self.solenoids[25]["kind"])

    def test_coordinates_are_normalized_retained_vpx_points_or_explicitly_absent(self) -> None:
        for item in self.definition["inputs"] + self.definition["outputs"]:
            spatial = item.get("spatial")
            if not spatial or spatial["status"] == "not_applicable":
                continue
            self.assertIn(spatial["status"], {"observed", "validated"}, item["id"])
            for placement in spatial["placements"]:
                self.assertEqual("playfield", placement["space"])
                self.assertGreaterEqual(placement["x"], 0.0); self.assertLessEqual(placement["x"], 1.0)
                self.assertGreaterEqual(placement["y"], 0.0); self.assertLessEqual(placement["y"], 1.0)
                self.assertLessEqual(len(str(placement["x"]).partition(".")[2]), 6)
        self.assertNotIn("spatial", self.switches[31])
        self.assertNotIn("spatial", self.solenoids[37])
        for address in (0, 1, 2):
            self.assertNotIn("spatial", self.gi[address])
        report = read(SPATIAL_PATH)
        self.assertEqual([31, 32, 33, 34, 35, 36, 37, 41, 42, 47, 48, 63, 64, 66, 76], report["unresolved_input_addresses"])
        unresolved_outputs = {(item["group"], item["address"]) for item in report["unresolved_output_bindings"]}
        self.assertEqual(
            {("pinmame.output.solenoid", address) for address in (10, 11, 27, 28, 37, 38, 54, 55)}
            | {("pinmame.output.gi", address) for address in (0, 1, 2)},
            unresolved_outputs,
        )
        partial = {(item["group"], item["address"]):(item["placement_count"],item["physical_quantity"]) for item in report["partially_placed_output_bindings"]}
        self.assertEqual(
            {("pinmame.output.lamp", address):(1,2) for address in (13,28,68)}
            | {("pinmame.output.solenoid", address):(1,2) for address in (20,25)},
            partial,
        )
        for group,address in partial:
            item = (self.lamps if group == "pinmame.output.lamp" else self.solenoids)[address]
            self.assertEqual("observed",item["spatial"]["status"])
            self.assertIn("second bulb remains spatially unplaced",item["physical"]["notes"])

    def test_gi_connectors_are_populated_in_the_transcribed_wiring_lists(self) -> None:
        excerpt = (ROOT / "evidence/excerpts/williams.no-good-gofers.1997/general-illumination.md").read_text(encoding="utf-8")
        expected = {
            0:("J106-7","J106-1"), 1:("J106-8","J106-2"),
            2:("J106-9 / J105-9","J106-3 / J105-3"), 3:("J105-10","J105-5"),
            4:("J105-11 / J104-1","J105-6 / J104-3"),
        }
        for address,(control,return_connection) in expected.items():
            self.assertEqual(control,self.gi[address]["wiring"]["control_connection"])
            self.assertEqual(return_connection,self.gi[address]["wiring"]["return_connection"])
            for pin in (control + " / " + return_connection).split(" / "):
                match = re.search(rf"^\| {re.escape(pin)} \| ([^|]+) \|",excerpt,re.MULTILINE)
                self.assertIsNotNone(match,pin)
                self.assertNotEqual("N/C",match.group(1).strip(),pin)

    def test_unfitted_driver_circuits_preserve_physical_wiring(self) -> None:
        expected = {22:("Q30","BLU-BLK"),23:("Q25","BLU-VIO"),36:("Q83","ORG-GRY")}
        for address,(transistor,wire) in expected.items():
            item = self.solenoids[address]
            self.assertEqual("coil",item["kind"])
            self.assertEqual("unused",item["availability"])
            self.assertEqual(transistor,item["wiring"]["driver_transistor"])
            self.assertEqual(wire,item["wiring"]["drive_wire"])
            self.assertIn("manual.williams.no-good-gofers.1997",item["provenance"]["source_refs"])

    def test_mechanisms_cover_the_author_relevant_custom_hardware(self) -> None:
        mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
        required = {"mechanism.trough", "mechanism.left-gofer-and-ramp", "mechanism.right-gofer-and-ramp", "mechanism.putt-out-and-underground-pass", "mechanism.slam-ramp", "mechanism.wheel-and-golf-cart", "mechanism.upper-right-flipper"}
        self.assertTrue(required <= set(mechanisms))
        device_ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
        for mechanism in mechanisms.values():
            self.assertTrue(mechanism["behavior"].strip())
            self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= device_ids)

    def test_all_drivers_and_hashed_manual_excerpts_are_retained(self) -> None:
        self.assertEqual({"ngg_13", "ngg_p06", "ngg_10", "ngg_12"}, {item["id"] for item in self.definition["drivers"]})
        manual = next(source for source in self.definition["sources"] if source["id"] == "manual.williams.no-good-gofers.1997")
        self.assertEqual("736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d", manual["sha256"])
        self.assertEqual(12, len(manual["excerpts"]))
        for excerpt in manual["excerpts"]:
            payload = ROOT / excerpt["path"]
            self.assertEqual(excerpt["sha256"], hashlib.sha256(payload.read_bytes()).hexdigest())
            self.assertTrue(excerpt["reviewed"])

    def test_curator_is_reproducible_without_external_roots(self) -> None:
        import curate_no_good_gofers as curator

        old = os.environ.pop("PINMAME_VPX_SOURCES_ROOT", None)
        try:
            curator.check(ROOT)
        finally:
            if old is not None:
                os.environ["PINMAME_VPX_SOURCES_ROOT"] = old
        self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main()
