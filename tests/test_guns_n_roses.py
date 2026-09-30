"""Game-specific regression and retained-evidence gates for Guns N' Roses."""
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

from jsonschema import Draft202012Validator
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_guns_n_roses as curator
from guns_n_roses_harness import MASKS, match_header


class GunsNRosesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.machine = load_json(ROOT / "machines/partial/data-east/guns-n-roses-1994.json")
        cls.switches = {d["binding"]["device"]:d for d in cls.machine["inputs"]
                        if d["binding"]["group"] == "pinmame.input.switch"}
        cls.solenoids = {d["binding"]["device"]:d for d in cls.machine["outputs"]
                         if d["binding"]["group"] == "pinmame.output.solenoid"}
        cls.lamps = {d["binding"]["device"]:d for d in cls.machine["outputs"]
                     if d["binding"]["group"] == "pinmame.output.lamp"}

    def test_identity_variants_display_and_partial_gate(self):
        self.assertEqual("data-east.guns-n-roses.1994", self.machine["machine"]["id"])
        self.assertEqual(1100,self.machine["machine"]["ipdb_id"])
        self.assertEqual({"gnr_300","gnr_300f","gnr_300d"},{d["id"] for d in self.machine["drivers"]})
        self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.machine["drivers"]))
        self.assertEqual((128,32,0),tuple(self.machine["displays"][0][k] for k in ["width","height","controller_index"]))
        self.assertEqual("partial",self.machine["coverage"]["status"])
        self.assertEqual({"spatial_placement","output_semantics","unresolved_conflicts"},
                         set(self.machine["coverage"]["missing"]))
        self.assertFalse((ROOT/"machines/author-ready/data-east/guns-n-roses-1994.json").exists())
        self.assertEqual([],validate_machine(self.machine,ROOT))

    def test_complete_outer_namespaces_and_precise_dispositions(self):
        self.assertEqual(set(range(1,65))|{-7,-6}|set(range(81,89)),set(self.switches))
        self.assertEqual(set(range(1,65)),set(self.solenoids))
        self.assertEqual(set(range(1,65)),set(self.lamps))
        self.assertEqual([0],[d["binding"]["device"] for d in self.machine["inputs"]
                              if d["binding"]["group"] == "pinmame.input.dip"])
        self.assertEqual({31,32,41,42,43,44,45,46,47,61},
                         {n for n in range(1,65) if self.switches[n]["availability"] == "unused"})
        self.assertEqual({82,84},{n for n in range(81,89) if self.switches[n]["availability"] == "used"})
        self.assertTrue(all(d["availability"] == "used" for d in self.lamps.values()))
        self.assertEqual("unused",self.solenoids[49]["availability"])
        self.assertEqual("Extra-Ball Button",self.lamps[63]["label"])
        self.assertEqual("Credit",self.lamps[64]["label"])

    def test_flipper_aliases_do_not_invent_hardware(self):
        self.assertEqual(("virtual","unused"),(self.solenoids[36]["kind"],self.solenoids[36]["availability"]))
        self.assertEqual("device.upper-left-flipper",self.solenoids[36]["id"])
        for n in [45,46,47,48]:
            self.assertEqual("virtual",self.solenoids[n]["kind"])
            self.assertEqual("used",self.solenoids[n]["availability"])
            self.assertNotIn("quantity",self.solenoids[n].get("physical",{}))
        for n in [63,64]:
            self.assertIn("direct writes",self.switches[n]["physical"]["notes"])
        upper = next(m for m in self.machine["mechanisms"] if m["id"] == "mechanism.upper-left-flipper")
        self.assertEqual([],upper["actuators"])
        self.assertIn("staged",upper["behavior"])

    def test_factory_wiring_typo_resolution_and_magnet_permutation(self):
        self.assertEqual("PPB J2-7",self.solenoids[7]["wiring"]["control_connection"])
        self.assertEqual("CPU CN12-2",self.solenoids[10]["wiring"]["control_connection"])
        self.assertEqual("25-1240",self.solenoids[5]["physical"]["part_number"])
        self.assertEqual("500-5839-00",self.solenoids[5]["physical"]["assembly_part_number"])
        self.assertEqual("CN8-5",self.switches[37]["wiring"]["drive_connection"])
        self.assertEqual("CN10-5",self.switches[37]["wiring"]["return_connection"])
        self.assertEqual("CN6-9",self.lamps[64]["wiring"]["return_connection"])
        for n,pin,transistor in [(51,"J2-4","Q2"),(52,"J2-3","Q1"),(53,"J2-7","Q3")]:
            self.assertEqual("magnet",self.solenoids[n]["kind"])
            self.assertEqual(pin,self.solenoids[n]["wiring"]["control_connection"])
            self.assertEqual(transistor,self.solenoids[n]["wiring"]["driver_transistor"])
        self.assertTrue(all(self.solenoids[n]["kind"] == "virtual" for n in [37,38,39]))

    def test_six_initial_balls_and_real_seventh_sensor(self):
        self.assertEqual(set(range(9,15)),{n for n,d in self.switches.items() if d.get("initial_active")})
        self.assertEqual("switch",self.switches[15]["kind"])
        self.assertEqual("180-5118-00",self.switches[15]["physical"]["part_number"])
        self.assertIn("Real seventh",self.switches[15]["physical"]["notes"])
        self.assertEqual("Right Slingshot",self.switches[28]["label"])
        self.assertEqual("Left Slingshot",self.switches[29]["label"])

    def test_geometry_is_per_object_not_bloom_or_primitive_origin(self):
        for obj in curator.GEOMETRY["objects"].values():
            self.assertNotIn(obj["type"],{"Primitive","Flasher"})
            self.assertEqual([round(obj["raw_xy"][0]/1000,6),
                              round(obj["raw_xy"][1]/1902,6)],obj["xy"])
        self.assertEqual([0.362401,0.174744],
                         [self.switches[25]["spatial"]["placements"][0][k] for k in ["x","y"]])
        self.assertEqual(2,self.lamps[55]["physical"]["quantity"])
        self.assertEqual(2,len(self.lamps[55]["spatial"]["placements"]))
        self.assertTrue(all("spatial" not in self.switches[n] for n in range(9,16)))
        self.assertTrue(all(self.switches[n]["physical"]["quantity"] == 2 for n in [28,29,30]))
        self.assertTrue(all("spatial" not in self.switches[n] for n in [28,29,30]))
        self.assertTrue(all("spatial" not in self.solenoids[n] for n in range(25,33)))
        self.assertTrue(all(self.solenoids[n]["physical"]["quantity"] == 4 for n in range(25,33)))
        self.assertEqual("pinmame-spatial-blockers",
                         load_json(ROOT/"reports/spatial/data-east/guns-n-roses-1994.json")["format"])
        audit=load_json(ROOT/"reports/spatial/data-east/guns-n-roses-1994.json")
        self.assertEqual(3,len(audit["physical_flipper_anchors"]))
        upper=next(a for a in audit["physical_flipper_anchors"] if a["object"]=="LeftFlipper1")
        self.assertEqual((0.120201,0.419499),(upper["x"],upper["y"]))

    def test_legacy_identifiers_and_aliases_are_preserved(self):
        for group,devices in [("inputs",self.switches),("outputs",self.solenoids)]:
            for key,original in curator.GEOMETRY["legacy"][group].items():
                if group == "outputs":
                    namespace,n=key.rsplit(":",1)
                    current = (self.lamps if namespace == "pinmame.output.lamp" else devices)[int(n)]
                else:current=devices[int(key)]
                self.assertEqual(original["id"],current["id"])
                self.assertEqual(original["aliases"],current["aliases"])

    def test_canonical_seed_curator_and_complete_excerpts(self):
        for path,payload in curator.artifacts().items():
            self.assertEqual(payload,(ROOT/path).read_bytes().replace(b"\r\n",b"\n"),str(path))
        self.assertEqual(canonical_bytes(self.machine),
                         (ROOT/"tools/seeds/data-east/guns-n-roses-1994.json").read_bytes())
        for name in ["switch-chart.md","lamp-chart.md"]:
            text=(ROOT/curator.EXCERPTS/name).read_text(encoding="utf-8")
            self.assertEqual(64,sum(line.startswith("| ") and line[2:].split(" | ")[0].isdigit()
                                    for line in text.splitlines()))
        promoted=copy.deepcopy(self.machine);promoted["coverage"]={"status":"author_ready","missing":[],
                                                                 "dimensions":self.machine["coverage"]["dimensions"]}
        self.assertTrue(validate_machine(promoted,ROOT),"Dishonest promotion must fail")
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/"machines/author-ready"/f"{curator.STEM}.json"
            target.parent.mkdir(parents=True)
            target.write_text("existing author-ready artifact",encoding="utf-8")
            with patch.object(sys,"argv",["curate_guns_n_roses.py","--regenerate","--repository-root",directory]):
                with self.assertRaisesRegex(ValueError,"author-ready"):curator.main()
            self.assertEqual("existing author-ready artifact",target.read_text(encoding="utf-8"))
            self.assertFalse((Path(directory)/"machines/partial").exists())

    def test_reusable_scenarios_and_header_fail_closed(self):
        schema=load_json(ROOT/"schemas/harness-scenario.schema.json")
        for name in ["gnr-300-magnet-laser.json","gnr-300-active-switches.json"]:
            Draft202012Validator(schema).validate(load_json(ROOT/"tools/harness-scenarios"/name))
        for title,mask in MASKS.items():
            frame=mask+bytes(4096-len(mask))
            self.assertEqual(title,match_header(frame,128,32))
            self.assertEqual("",match_header(bytes(4096),128,32))
            altered=bytearray(frame);altered[0]^=1
            self.assertEqual("",match_header(altered,128,32))
            self.assertEqual("",match_header(frame,128,64))


class GunsNRosesExternalTests(unittest.TestCase):
    def setUp(self):
        root=os.environ.get("PINMAME_WORKING_ROOT")
        if not root:self.skipTest("PINMAME_WORKING_ROOT not supplied; external verification intentionally skipped")
        self.working=Path(root)

    def test_complete_retained_extraction_manual_and_runtime(self):
        curator.verify_external(self.working)

    def test_runtime_wrong_game_output_mirror_and_emulator_fail_closed(self):
        raw=load_json(self.working/"review-artifacts"/curator.KEY/
                      "session-20260930/runtime/magnet-laser-v2-run.json")
        curator.verify_runtime(raw)
        wrong=copy.deepcopy(raw);wrong["game"]="gnr_300f"
        with self.assertRaisesRegex(ValueError,"Wrong game"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw);wrong["library_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"DLL"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw);wrong["scenario"]["sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"scenario"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw)
        step=next(s for s in wrong["steps"] if s["label"] == "Find ROM Magnet Test header")
        step["matched_text"]="SWITCH TEST"
        with self.assertRaisesRegex(ValueError,"display checkpoint"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw)
        step=next(s for s in wrong["steps"] if s["label"] == "Wait for Laser Kick Test to enable outputs")
        step["matched_outputs"]=[{"number":23,"states":[0]}]
        with self.assertRaisesRegex(ValueError,"idle/enable"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw)
        step=next(s for s in wrong["steps"] if s["label"] == "Left outlane closure tests Laser Kick")
        step["transitions"]["solenoids"][0]["number"]=13
        with self.assertRaisesRegex(ValueError,"output14"):curator.verify_runtime(wrong)
        wrong=copy.deepcopy(raw)
        step=next(s for s in wrong["steps"] if s["label"] == "Hold Start and cycle all three magnets")
        next(s for s in step["transitions"]["solenoids"] if s["number"] == 51)["states"]=[0]
        with self.assertRaisesRegex(ValueError,"mirror"):curator.verify_runtime(wrong)


if __name__ == "__main__":
    unittest.main()
