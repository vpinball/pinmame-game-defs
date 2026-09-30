from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
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
        self.assertIn("Unshaded", self.switches[47]["physical"]["notes"])
        self.assertEqual("constant", self.switches[24]["kind"])
        self.assertTrue(self.switches[24]["constant_active"])
        self.assertEqual("candidate", self.switches[115]["spatial"]["status"])
        self.assertEqual((0.837256, 0.356449), (self.switches[115]["spatial"]["placements"][0]["x"],
                                                   self.switches[115]["spatial"]["placements"][0]["y"]))
        self.assertIn(curator.RUNTIME_SRC, self.switches[115]["provenance"]["source_refs"])

    def test_manual_bulbs_reels_and_flipper_circuits(self) -> None:
        for address in (56, 57, 58):
            self.assertEqual("24-8768", self.lamps[address]["physical"]["part_number"])
            self.assertEqual("A-20527", self.lamps[address]["physical"]["assembly_part_number"])
        self.assertEqual("J138-7", self.lamps[71]["wiring"]["drive_connection"])
        self.assertEqual("J138-9", self.lamps[81]["wiring"]["drive_connection"])
        self.assertEqual("J902-1 playfield", self.solenoids[36]["wiring"]["drive_connection"])
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
            self.assertEqual("FL-15411",output["physical"]["part_number"])
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
        for address in (23, 24, 25, 26, 27, 28):
            self.assertEqual("14-8024 12V", self.solenoids[address]["physical"]["part_number"])
        self.assertEqual("24-8704", self.solenoids[18]["physical"]["part_number"])
        self.assertEqual(3, self.solenoids[20]["physical"]["quantity"])
        self.assertEqual("24-6549", self.gi[0]["physical"]["part_number"])
        self.assertEqual("24-8768", self.gi[4]["physical"]["part_number"])
        self.assertEqual(["solenoid.23", "solenoid.24"],
                         next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.left-reel")["actuators"])

    def test_real_factory_conflict_is_fail_closed(self) -> None:
        self.assertNotIn("part_number", self.solenoids[13]["physical"])
        conflicts = self.definition["conflicts"]
        self.assertEqual(1, len(conflicts))
        self.assertEqual("unresolved", conflicts[0]["status"])
        self.assertIn("Resolution path:", conflicts[0]["description"])
        self.assertIn("AE-26-1500", conflicts[0]["description"])
        self.assertIn("AE-26-1200", conflicts[0]["description"])

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
        names = ("PINMAME_VPX_SOURCES_ROOT", "PINMAME_MANUALS_ROOT", "PINMAME_REVIEW_ARTIFACTS_ROOT")
        if not all(os.environ.get(name) for name in names):
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
        opto_trace = read(base / "traces/07-opto-edges.json")
        for address in (12, 25, 48, 31, 41, 47):
            self.assertTrue(any(snapshot["label"] == f"Opto {address} raw 1"
                                for snapshot in opto_trace["snapshots"]))


if __name__ == "__main__":
    unittest.main()
