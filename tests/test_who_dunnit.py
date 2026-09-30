from __future__ import annotations

import copy
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
        self.assertEqual(3, len(conflicts))
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
        self.assertEqual("J137-1",self.lamps[11]["wiring"]["drive_connection"])
        self.assertEqual("J133-1",self.lamps[11]["wiring"]["return_connection"])
        self.assertIn("J134-8",self.lamps[87]["physical"]["notes"])
        self.assertIn("J134-9",self.lamps[88]["physical"]["notes"])
        opto=by_id["conflict.left-flipper-opto-wire"]
        self.assertIn("Black-Gray",opto["description"])
        self.assertIn("Blue-Gray",opto["description"])
        self.assertEqual("conflicted",self.switches[114]["provenance"]["status"])
        self.assertEqual("J905-2 / J905-5",self.switches[114]["wiring"]["control_connection"])
        self.assertNotIn("control_wire",self.switches[114]["wiring"])
        self.assertEqual("conflicted",self.definition["coverage"]["dimensions"]["physical_wiring"])

    def test_relied_core_artifacts_are_pinned_and_mismatch_rejected(self) -> None:
        sources={source["id"]:source for source in self.definition["sources"]}
        self.assertEqual({"wd.c","core.c","wpc.c","core.h"},{Path(path).name for path in curator.CORE_ARTIFACTS})
        for path,(source_id,digest,_) in curator.CORE_ARTIFACTS.items():
            source=sources[source_id]
            self.assertEqual(curator.PIN,source["revision"])
            self.assertEqual(digest,source["sha256"])
            self.assertTrue(source["uri"].endswith(f"/{curator.PIN}/{path}"))
            self.assertIn(source_id,self.solenoids[45]["provenance"]["source_refs"])
        if os.environ.get("PINMAME_MANUALS_ROOT"):
            source_id,_,locator=curator.CORE_ARTIFACTS["src/wpc/core.h"]
            with patch.dict(curator.CORE_ARTIFACTS,{"src/wpc/core.h":(source_id,"0"*64,locator)}):
                with self.assertRaisesRegex(RuntimeError,"core artifact mismatch: src/wpc/core.h"):
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
        curator.verify_opto_evidence(base)
        opto_source=next(source for source in self.definition["sources"] if source["id"]=="runtime.who-dunnit.optos.wd-12")
        for address,states in curator.OPTO_FRAMES.items():
            self.assertEqual({0,1},set(states))
            for state,(step,frame,digest) in states.items():
                self.assertIn(f"public {address} raw {state}, action/trace step {step}",opto_source["locator"])
                self.assertIn(f"DMD {frame} SHA-256 {digest}",opto_source["locator"])

    def test_supplied_missing_evidence_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(os.environ,{"PINMAME_REVIEW_ARTIFACTS_ROOT":directory},clear=True):
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
