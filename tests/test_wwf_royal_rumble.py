"""Independent WWF facts and evidence-integrity regressions.

The manual fixtures below protect distinctions lost by the previous catalog
stub and by related table scripts: six trough contacts versus a release contact,
TAG versus the shooter, fitted lamps omitted by the recreation, physical flippers
versus synthetic paired states, and the nonsequential Data East special outputs.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import statistics
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_wwf_royal_rumble as curator
import build_wwf_runtime_evidence as runtime_builder
import wwf_harness
import build_wwf_static_evidence as static_builder
from build_external_evidence_manifest import check_manifest
from pinmame_game_defs.spatial import extract_spatial_candidates, _round_point

KEY = "data-east.wwf-royal-rumble.1994"
SLUG = "wwf-royal-rumble-1994"
GAMES = {"wwfr_106", "wwfr_103", "wwfr_103f"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class WWFDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition = read(ROOT / curator.DEFINITION)
        cls.evidence = read(ROOT / "tools/wwf_evidence.json")
        cls.inputs = {d["binding"]["device"]: d for d in cls.definition["inputs"] if d["binding"]["group"] == "pinmame.input.switch"}
        cls.lamps = {d["binding"]["device"]: d for d in cls.definition["outputs"] if d["binding"]["group"] == "pinmame.output.lamp"}
        cls.coils = {d["binding"]["device"]: d for d in cls.definition["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}

    def test_identity_and_exact_family(self):
        machine = self.definition["machine"]
        self.assertEqual((KEY, 1994, 2820, "500-5523-01", "G57y6-MLej6"),
                         tuple(machine[k] for k in ["id", "year", "ipdb_id", "model_number", "opdb_id"]))
        self.assertEqual(GAMES, {d["id"] for d in self.definition["drivers"]})
        for driver in self.definition["drivers"]:
            self.assertEqual("identical", driver["physical_compatibility"])
        self.assertEqual("0x4000", self.definition["controller"]["hardware_generation"])
        self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
        self.assertEqual((128, 32), tuple(self.definition["displays"][0][k] for k in ("width", "height")))
        catalog = read(ROOT/"catalog/pinmame.json")
        for driver in catalog["drivers"]:
            if driver["id"] in GAMES:
                self.assertEqual(KEY,driver["machine_id"])
                self.assertEqual(curator.DEFINITION,driver["definition"])

    def test_full_address_disposition(self):
        self.assertEqual(set(range(1,65)) | set(range(81,89)) | {-7,-6}, set(self.inputs))
        self.assertEqual(set(range(1,65)), set(self.lamps))
        self.assertEqual(set(range(1,51)), set(self.coils))
        self.assertEqual({48,57,59,60,61}, {n for n in range(1,65) if self.inputs[n]["availability"] == "unused"})
        self.assertEqual({14,15,24,33,34,35,36,49,50}, {n for n,d in self.coils.items() if d["availability"] == "unused"})
        self.assertEqual(set(range(37,45)), {n for n,d in self.coils.items() if d["availability"] == "unknown"})
        for n in range(1,65):
            if self.inputs[n]["availability"] == "used":
                self.assertFalse(self.inputs[n]["normally_closed"], n)

    def test_independent_switch_and_wiring_facts(self):
        for n, label in {16:"Shooter Lane",19:"Left Slingshot",20:"Super VUK (Right Side)",
                         27:"Right Slingshot",40:"VUK (Middle)",62:"TAG Button"}.items():
            self.assertEqual(label, self.inputs[n]["label"], n)
        for n in range(9,15):
            self.assertIn("Trough", self.inputs[n]["label"])
        self.assertEqual("GRN-BRN", self.inputs[1]["wiring"]["drive_wire"])
        self.assertEqual("WHT-GRY", self.inputs[64]["wiring"]["return_wire"])
        self.assertEqual("CN8-9", self.inputs[64]["wiring"]["drive_connection"])
        self.assertEqual("Ball Trough #7 Right", self.inputs[15]["label"])
        self.assertNotEqual(self.inputs[16]["id"], self.inputs[62]["id"])

    def test_fitment_is_not_effect_object_count(self):
        for n in [15,16,27,59]:
            self.assertEqual("used", self.lamps[n]["availability"])
        self.assertEqual(2, self.lamps[28]["physical"]["quantity"])
        for n in range(25,33):
            self.assertEqual(4, self.coils[n]["physical"]["quantity"])
            self.assertFalse(self.coils[n].get("spatial", {}).get("placements"))
        self.assertIn("misprint", self.coils[32]["physical"]["notes"])
        self.assertEqual("gi", self.coils[11]["kind"])
        self.assertNotIn("quantity", self.coils[11]["physical"])
        self.assertEqual({61},{n for n,d in self.lamps.items() if d.get("spatial", {}).get("placements")})

    def test_flippers_configuration_and_printer_are_not_invented_hardware(self):
        for n in range(45,49):
            self.assertEqual("virtual", self.coils[n]["kind"])
            self.assertEqual("used", self.coils[n]["availability"])
            self.assertIn("together", self.coils[n]["physical"]["notes"])
        dips = [d for d in self.definition["inputs"] if d["binding"]["group"] == "pinmame.input.dip"]
        self.assertEqual(1, len(dips))
        self.assertEqual("unknown", dips[0]["availability"])
        self.assertIn("no Country DIP", dips[0]["physical"]["notes"])
        for n in range(37,45):
            self.assertEqual("observed", self.coils[n]["provenance"]["status"])
            self.assertEqual("virtual", self.coils[n]["kind"])

    def test_mechanism_topology_without_fake_coil_sensor_relations(self):
        mechanisms = {m["id"]:m for m in self.definition["mechanisms"]}
        self.assertEqual(14, len(mechanisms))
        for name, addresses in [("trough",range(9,16)),("scoop-vuk",[39,40]),("lower-drop-bank",range(21,25)),("upper-drop-bank",[30,31,32])]:
            self.assertEqual({self.inputs[n]["id"] for n in addresses}, set(mechanisms["mechanism."+name]["sensors"]))
        right = mechanisms["mechanism.right-diverter"]
        self.assertEqual([self.coils[22]["id"]], right["actuators"])
        self.assertEqual([], right["sensors"])
        self.assertIn("does not establish physical home", right["behavior"])
        self.assertEqual("observed", right["provenance"]["status"])

    def test_partial_gate_and_byte_reproduction(self):
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertEqual({"input_semantics","output_semantics","mechanism_behavior","spatial_placement","unresolved_conflicts"}, set(self.definition["coverage"]["missing"]))
        self.assertEqual(self.definition, curator.build(ROOT))
        self.assertEqual((ROOT/curator.DEFINITION).read_bytes(), (ROOT/curator.SEED).read_bytes())
        self.assertEqual((ROOT/curator.KNOWLEDGE).read_bytes(), (ROOT/"tools/wwf_knowledge.md").read_bytes())
        self.assertEqual(5, len(read(ROOT/curator.REPORT)["blockers"]))
        self.assertFalse((ROOT/f"machines/author-ready/data-east/{SLUG}.json").exists())

    def test_source_excerpts_are_complete_and_hashed(self):
        ids = {s["id"] for s in self.evidence["sources"]}
        self.assertTrue({"manual.wwf","photos.wwf","runtime.wwf","runtime.wwf-103","runtime.wwf-103f"} <= ids)
        for source in self.evidence["sources"]:
            for e in source.get("excerpts", []):
                self.assertTrue(e["reviewed"])
                self.assertEqual("manual", e["method"])
                self.assertEqual(e["sha256"], sha(ROOT/e["path"]))
                if e.get("image"):
                    self.assertEqual(e["image_sha256"], sha(ROOT/e["image"]))
                    self.assertLess((ROOT/e["image"]).stat().st_size, 100000)
                    self.assertIn("native resolution", e["image_derivation"])

    def test_new_source_does_not_overpromote_lighting_or_static_unknowns(self):
        audit=read(ROOT/"tools/wwf_lighting_audit.json")
        self.assertEqual((36,36),(audit["gi"]["old"]["collection_member_count"],audit["gi"]["old"]["own_mesh_count"]))
        self.assertEqual((77,38),(audit["gi"]["new"]["collection_member_count"],audit["gi"]["new"]["own_mesh_count"]))
        self.assertEqual(2,audit["manual_flash_playfield_counts"]["32"])
        self.assertEqual("observed",self.lamps[61]["spatial"]["status"])
        self.assertEqual(1,len(self.lamps[61]["spatial"]["placements"]))
        for n in (62,63):
            self.assertFalse(self.lamps[n].get("spatial",{}).get("placements"))
            self.assertEqual("conflicted",self.lamps[n]["provenance"]["status"])
        self.assertFalse(self.coils[11].get("spatial",{}).get("placements"))
        static=read(ROOT/"tools/wwf_static_evidence.json")
        self.assertEqual(GAMES,{row["driver"] for row in static["inputs"]})
        self.assertTrue(all("bytes" not in row for rows in static["shared_instructions"].values() for row in rows))
        setup={row["pc"]:row for row in static["shared_instructions"]["normal_pia_setup"]}
        self.assertEqual(("ldb",255),(setup[0x4585]["op"],setup[0x4585]["arg"]))
        self.assertEqual(("stb",0x2800),(setup[0x458c]["op"],setup[0x458c]["arg"]))
        self.assertIn("Indexed/scheduler",next(x for x in self.definition["inputs"] if x["kind"]=="dip_switch")["physical"]["notes"])
        for n in range(37,45):
            self.assertEqual("unknown",self.coils[n]["availability"])
            self.assertIn("CA2",self.coils[n]["physical"]["notes"])

    def test_bumper_lamp_drawing_is_not_the_switch_map(self):
        # Literal spatial relationships visually checked in two different manual
        # drawings, not inferred from the swapped Bottom/Right switch labels.
        audit=read(ROOT/"tools/wwf_lighting_audit.json")
        self.assertEqual({"61":"rear/left","62":"front/bottom","63":"rear/right"},audit["manual_bumper_locations"]["lamps_printed31"])
        self.assertEqual({"49":"rear/left","50":"rear/right","51":"front/bottom"},audit["manual_bumper_locations"]["switches_printed29"])
        self.assertLess(audit["matrix_bulbs"]["62"]["new"]["y"],audit["matrix_bulbs"]["63"]["new"]["y"])
        self.assertLess(self.inputs[50]["spatial"]["placements"][0]["y"],self.inputs[51]["spatial"]["placements"][0]["y"])
        conflicts=self.definition["conflicts"]
        self.assertEqual({"wwf.lamp-62-physical-position","wwf.lamp-63-physical-position"},{row["id"] for row in conflicts})
        self.assertTrue(all(row["status"]=="unresolved" and "socket" in row["description"] for row in conflicts))
        for row in conflicts:
            self.assertIn("Resolution path: a production-machine owner or service technician",row["description"])
            self.assertTrue(row["description"].endswith("socket's lamp-matrix wire pair."))
            self.assertNotRegex(row["description"],r"\b(?:printed|puts|bind|lamp)\d")

    def test_guards_reject_missing_changed_inputs_and_promotion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in ["tools/wwf_evidence.json", "tools/wwf_places.json", "tools/wwf_mechanisms.json", "tools/wwf_static_evidence.json", "tools/wwf_lighting_audit.json"]:
                (root/path).parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,root/path)
            shutil.copytree(ROOT/"evidence/excerpts"/KEY,root/"evidence/excerpts"/KEY)
            (root/"evidence/runtime/data-east").mkdir(parents=True)
            for game in GAMES:
                path = f"evidence/runtime/data-east/wwf-royal-rumble-{game}-service-tests.json"
                shutil.copyfile(ROOT/path,root/path)
            self.assertEqual(self.definition, curator.build(root))
            static=root/"tools/wwf_static_evidence.json"
            original_static=static.read_bytes()
            static.write_bytes(original_static+b" ")
            with self.assertRaisesRegex(ValueError,"portable input"):
                curator.build(root)
            static.write_bytes(original_static)
            excerpt = root/"evidence/excerpts"/KEY/"switches.md"
            original = excerpt.read_bytes()
            excerpt.write_bytes(original.replace(b"Plumb", b"Wrong", 1))
            with self.assertRaisesRegex(ValueError,"excerpt"):
                curator.build(root)
            excerpt.write_bytes(original)
            image = root/"evidence/excerpts"/KEY/"flash-loads.webp"
            image.unlink()
            with self.assertRaisesRegex(ValueError,"image"):
                curator.build(root)
            shutil.copyfile(ROOT/"evidence/excerpts"/KEY/"flash-loads.webp",image)
            places = read(root/"tools/wwf_places.json")
            places["devices"].pop("switch.16")
            (root/"tools/wwf_places.json").write_text(json.dumps(places),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"placement inventory"):
                curator.build(root)
            shutil.copyfile(ROOT/"tools/wwf_places.json",root/"tools/wwf_places.json")
            (root/"evidence/runtime/data-east/wwf-royal-rumble-wwfr_103-service-tests.json").unlink()
            with self.assertRaisesRegex(ValueError,"runtime evidence"):
                curator.build(root)
            promoted=root/f"machines/author-ready/data-east/{SLUG}.json"
            promoted.parent.mkdir(parents=True)
            promoted.write_text("{}",encoding="utf-8")
            with patch.object(sys,"argv",["curator","--check","--repository-root",str(root)]):
                with self.assertRaisesRegex(ValueError,"author-ready"):
                    curator.main()

    def test_title_guard_can_fail(self):
        self.assertEqual([],wwf_harness.match_titles(bytes(4096),128,32))
        for title, data in wwf_harness.TEMPLATES.items():
            first,last = data["rows"]
            frame = bytearray(4096)
            frame[first*128:(last+1)*128] = base64.b64decode(data["mask"])
            self.assertIn(title,wwf_harness.match_titles(frame,128,32))
            frame[first*128] ^= 1
            self.assertNotIn(title,wwf_harness.match_titles(frame,128,32))
            self.assertEqual([],wwf_harness.match_titles(frame,64,64))
        for target in ["SWITCH TEST","LAMP","WWF UNREAD TEST"]:
            with self.assertRaises(ValueError):
                wwf_harness.check_targets({"actions":[{"type":"pulse_until_display","texts":[target]}]})
        with patch.object(wwf_harness.harness,"build_parser") as parser:
            parser.return_value.parse_args.return_value=SimpleNamespace(game="unsupported",scenario=None)
            with self.assertRaisesRegex(ValueError,"three production"):
                wwf_harness.main()


EXTERNAL = all(os.environ.get(k) for k in ["PINMAME_VPX_SOURCES_ROOT","PINMAME_MANUALS_ROOT","PINMAME_REVIEW_ARTIFACTS_ROOT"])


@unittest.skipUnless(EXTERNAL,"WWF external evidence roots not configured")
class WWFExternalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = read(ROOT/"tools/wwf_evidence.json")["retained"]
        cls.vpx = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])/cls.facts["vpx"]["relative_path"]
        cls.manual = Path(os.environ["PINMAME_MANUALS_ROOT"])/cls.facts["manual"]["relative_path"]
        cls.review_root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
        cls.session = cls.review_root/runtime_builder.SESSION

    def test_table_and_full_extraction_manifest(self):
        f = self.facts["vpx"]
        self.assertEqual(f["sha256"],sha(self.vpx/f["filename"]))
        self.assertEqual(f["script_sha256"],sha(self.vpx/"extracted-vpxtool/script.vbs"))
        self.assertEqual(f["manifest_sha256"],check_manifest(self.vpx/"extracted-vpxtool",f["manifest_game"]))
        m = read(self.vpx/"extracted-vpxtool/manifest.json")
        self.assertEqual(f["file_count"],len(m["files"]))
        self.assertEqual(f["total_bytes"],sum(x["size"] for x in m["files"]))
        text = (self.vpx/"extracted-vpxtool/script.vbs").read_text(encoding="utf-8")
        self.assertRegex(text,r'(?i)cGameName\s*=\s*"wwfr_103"')
        self.assertEqual(1,len(__import__('re').findall(r'(?im)^\s*Sub\s+SW26_Hit\b',text)))

    def test_new_table_original_bytes_manifest_and_lighting_audit(self):
        fact=self.facts["vpx_vpu203"]
        base=Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])/fact["relative_path"]
        self.assertEqual(fact["manifest_sha256"],check_manifest(base/"extracted","wwfr_106"))
        for kind in ["vpx","zip"]:
            self.assertEqual(fact[kind]["sha256"],sha(base/fact[kind]["path"]))
        with zipfile.ZipFile(base/fact["zip"]["path"]) as archive:
            self.assertEqual(fact["vpx"]["sha256"],hashlib.sha256(archive.read(fact["zip"]["member_name"])).hexdigest())
        self.assertEqual(fact["reviewed_inventory_sha256"],sha(base/"inventory-parent-reviewed.json"))
        self.assertEqual(fact["source_page_sha256"],sha(base/"source-page.json"))
        script=(base/"extracted/script.vbs").read_text(encoding="utf-8")
        self.assertEqual(fact["script_sha256"],sha(base/"extracted/script.vbs"))
        self.assertRegex(script,r'(?i)cGameName\s*=\s*"wwfr_106"')
        self.assertRegex(script,r'(?i)NFadeL\s+15,\s*L15')
        audit=read(ROOT/"tools/wwf_lighting_audit.json")
        roots={"old":self.vpx/"extracted-vpxtool","new":base/"extracted"}
        for which,root in roots.items():
            collection=next(c for c in read(root/"collections.json") if c["name"]=="GI")["items"]
            objects={p.stem[6:].lower():p for p in (root/"gameitems").glob("Light.*.json")}
            meshes={name for name in collection if read(objects[name.lower()])["Light"]["show_bulb_mesh"]}
            self.assertEqual(meshes,{p["objects"][0] for p in audit["gi"][which]["own_mesh_candidates"]})
            rows=audit["gi"][which]["own_mesh_candidates"]+[r[which] for r in audit["matrix_bulbs"].values()]
            for row in rows:
                path=root/row["source_file"]
                self.assertEqual(row["sha256"],sha(path))
                light=read(path)["Light"]
                self.assertEqual(row["raw"],light["center"])
                self.assertTrue(light["show_bulb_mesh"])
                self.assertEqual((row["x"],row["y"]),(_round_point(light["center"]["x"]/1093),_round_point(light["center"]["y"]/2162)))
        for number,item in audit["matrix_bulbs"].items():
            bumper=read(roots["new"]/"gameitems"/("Bumper."+item["assembly"]+".json"))["Bumper"]["center"]
            bulb=item["new"]["raw"]
            self.assertLess(abs(bulb["x"]-bumper["x"]),5)
            self.assertLess(abs(bulb["y"]-bumper["y"]),5)

    def test_static_facts_against_immutable_archive_and_exact_cpu_members(self):
        static=read(ROOT/"tools/wwf_static_evidence.json")
        self.assertEqual(static,static_builder.build(self.review_root))
        base=self.review_root/static_builder.RELATIVE
        original=read(base/"focused-code-evidence.json")
        for row in static["inputs"]:
            with zipfile.ZipFile(row["archive"]) as archive:
                data=archive.read(row["member"])
            self.assertEqual(row["sha256"],hashlib.sha256(data).hexdigest())
            for region in static["shared_region_digests"]:
                self.assertEqual(region["sha256"],hashlib.sha256(data[int(region["start"],16):int(region["end_exclusive"],16)]).hexdigest())
            # Compare retained decoding to the exact bytes at every selected PC;
            # bytes never enter the portable JSON. A shifted instruction fails.
            for region in original[row["member"]]["regions"]:
                for instruction in region["instructions"]:
                    pc=instruction["pc"]
                    self.assertEqual(bytes.fromhex(instruction["bytes"]),data[pc:pc+instruction["size"]])
        for row in static["source_files"]:
            self.assertEqual(row["sha256"],sha(self.review_root.parent/"source-checkouts/pinmame-46e1a01a"/row["path"]))

    def test_static_manifest_guard_rejects_drift_and_incomplete_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            base=Path(temporary)
            rows=[]
            for n in range(23):
                path=base/f"f{n}"
                path.write_text(str(n),encoding="utf-8")
                rows.append({"path":path.name,"size":path.stat().st_size,"sha256":sha(path)})
            manifest=base/"SHA256SUMS.json"
            manifest.write_text(json.dumps(rows),encoding="utf-8")
            self.assertEqual(rows,static_builder.verify_archive(base))
            (base/"f1").write_text("changed",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"drift"):
                static_builder.verify_archive(base)
            manifest.write_text(json.dumps(rows[:-1]),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"Incomplete"):
                static_builder.verify_archive(base)

    def test_manual_all_pages_and_both_photo_archives(self):
        self.assertEqual(self.facts["manual"]["sha256"],sha(self.manual/self.facts["manual"]["filename"]))
        self.assertEqual(90,len(list((self.manual/"native-renders").glob("page-*.png"))))
        path = Path(os.environ["PINMAME_MANUALS_ROOT"])/self.facts["photos"]["relative_path"]
        self.assertEqual(self.facts["photos"]["sha256"],sha(path))
        photos = read(path)["photos"]
        self.assertEqual({"Pinside":29,"IPDB":8},{site:sum(x["site"]==site for x in photos) for site in ["Pinside","IPDB"]})
        for photo in photos:
            self.assertEqual(photo["sha256"],sha(path.parent/photo["filename"]))

    def test_pinned_source_bytes_and_all_variant_rom_members(self):
        working = self.review_root.parent
        sources = read(ROOT/"tools/wwf_evidence.json")["sources"]
        source_root = working/"source-checkouts/pinmame-46e1a01a"
        for source in sources:
            if source["kind"] == "pinmame_core":
                self.assertEqual(source["sha256"],sha(source_root/"src"/source["uri"].split("/src/",1)[1]))
        code = (source_root/"src/wpc/degames.c").read_text(encoding="utf-8")
        rom_root = Path(os.environ.get("PINMAME_ROM_LIBRARY_ROOT", "L:/Visual Pinball/VPinMAME/roms"))
        for game in GAMES:
            archive = working/"roms"/KEY/"assembled/wwfr_103f.zip" if game == "wwfr_103f" else rom_root/(game+".zip")
            self.assertEqual(runtime_builder.ROM_HASHES[game],sha(archive))
            block = re.search(r"DE_ROMSTARTx0\("+game+r"\s*,(.*?)DE_ROMEND",code,re.S).group(1)
            expected = dict(re.findall(r'"([^"\n]+)"\s*,\s*CRC\([0-9a-f]+\)\s*SHA1\(([0-9a-f]+)\)',block))
            self.assertEqual(6,len(expected))
            with zipfile.ZipFile(archive) as zip_file:
                actual = {Path(name).name.lower():hashlib.sha1(zip_file.read(name)).hexdigest()
                          for name in zip_file.namelist() if not name.endswith("/")}
            self.assertEqual(expected,actual,game)
        for source in sources:
            if source["id"] in {"vpm.wwf-de","vpm.wwf-core"}:
                self.assertEqual(source["sha256"],sha(self.vpx/"libraries"/source["uri"].rsplit("/",1)[1]))
        for filename,digest in self.facts["libraries"].items():
            self.assertEqual(digest,sha(self.vpx/"libraries"/filename))

    def test_all_spatial_points_recomputed_from_objects_and_world_mesh(self):
        table = self.vpx/self.facts["vpx"]["filename"]
        candidates = extract_spatial_candidates(self.vpx/"extracted-vpxtool",table,"vpxtool git:v0.33.3")
        objects = {o["name"].lower():o for o in candidates["objects"]}
        mesh = self.review_root/self.facts["world_mesh"]["path"]
        self.assertEqual(self.facts["world_mesh"]["sha256"],sha(mesh))
        places_fixture=read(ROOT/"tools/wwf_places.json")
        controls=places_fixture["mesh_control_check"]
        wanted={c["mesh_object"] for c in controls["controls"]}|{"RampDiverter","RightDiverter"}
        vertices={};name=""
        for line in mesh.read_text(encoding="utf-8").splitlines():
            if line.startswith("o "):name=line[2:].strip()
            elif line.startswith("v ") and name in wanted:
                vertices.setdefault(name,[]).append([float(x) for x in line.split()[1:4]])
        for control in controls["controls"]:
            points=vertices[control["mesh_object"]]
            other=objects[control["table_object"].lower()]
            for i,(axis,size) in enumerate([("x",1093),("y",2162)]):
                centre=(min(p[i] for p in points)+max(p[i] for p in points))/2
                self.assertLessEqual(abs(centre-other[axis]*size),controls["tolerance_vpu"],control)
        for key, places in read(ROOT/"tools/wwf_places.json")["devices"].items():
            for p in places:
                if "world_bounds" in p:
                    pts = vertices[p["objects"][0]]
                    low=[min(v[i] for v in pts) for i in range(3)]
                    high=[max(v[i] for v in pts) for i in range(3)]
                    self.assertEqual([low,high],p["world_bounds"])
                    x,y=[_round_point((low[i]+high[i])/2/size) for i,size in enumerate([1093,2162])]
                else:
                    pts=[objects[name.lower()] for name in p["objects"]]
                    x,y=(_round_point(statistics.mean(o[k] for o in pts)) for k in ("x","y"))
                self.assertEqual((x,y),(p["x"],p["y"]),key)
        self.assertNotEqual(objects["rightdiverter"]["x"],read(ROOT/"tools/wwf_places.json")["devices"]["solenoid.22"][0]["x"])

    def test_recompute_every_runtime_figure_and_hash(self):
        for game in GAMES:
            expected=read(ROOT/f"evidence/runtime/data-east/wwf-royal-rumble-{game}-service-tests.json")
            self.assertEqual(expected,runtime_builder.build(self.review_root,game))
            for run in expected["runtime"]["raw_runs"]:
                self.assertEqual(run["sha256"],sha(self.review_root/run["retained_from"]))
                self.assertEqual(run["scenario_sha256"],sha(self.review_root/run["scenario_path"]))
            lamp_run=next(name for name in runtime_builder.RUNS[game] if name.endswith("-lamps"))
            raw=read(self.session/"harness"/(lamp_run+".json"))
            self.assertEqual(set(range(1,65)),{n for snap in raw["snapshots"]
                             if snap["label"].startswith("lamp-step-") for n in snap["active_lamps"]})
        for name in ["106-printer","103-printer","106-dip1-printer"]:
            raw=read(self.session/"harness"/(name+".json"))
            self.assertTrue(any(step.get("matched_text")=="WWF PRINTER53" for step in raw["steps"]))
            self.assertFalse(any(e["event"]=="solenoid" and 37<=e["number"]<=44 for e in raw["events"]))
        for run_name in ["106-gameplay-v3","103-gameplay-v3","french-gameplay-v4"]:
            raw=read(self.session/"harness"/(run_name+".json"))
            actions={x["label"]:x for x in raw["steps"]}
            for switch,coil in [(49,17),(50,18),(51,19),(19,20),(27,21)]:
                step=actions[f"isolated-play-switch-{switch}"]
                self.assertIn(coil,[x["number"] for x in step["transitions"]["solenoids"] if 1 in x["states"]])
            for switch,pair in [(82,{45,46}),(84,{47,48})]:
                step=actions[f"isolated-play-switch-{switch}"]
                self.assertEqual(pair,{x["number"] for x in step["transitions"]["solenoids"] if 1 in x["states"]})
                self.assertEqual(1,len({tuple(x["states"]) for x in step["transitions"]["solenoids"] if x["number"] in pair}))

    def test_read_frames_and_title_masks_against_raw_pixels(self):
        from PIL import Image
        for title,template in wwf_harness.TEMPLATES.items():
            with Image.open(self.session/template["frame_path"]) as image:
                frame=image.tobytes()
            self.assertEqual(template["pixel_sha256"],hashlib.sha256(frame).hexdigest())
            self.assertIn(title,wwf_harness.match_titles(frame,128,32))
        for game in GAMES:
            compact=read(ROOT/f"evidence/runtime/data-east/wwf-royal-rumble-{game}-service-tests.json")
            for reading in compact["runtime"]["observations"]["diagnostic_snapshots"]:
                run,label=reading["label"].split(": ",1)
                raw=read(self.session/"harness"/(run+".json"))
                snap=next(x for x in raw["snapshots"] if x["label"]==label)
                display=snap["displays"][0]
                path=self.session/"harness"/Path(display["artifact"]).parent.name/Path(display["artifact"]).name
                with Image.open(path) as image:
                    frame=image.tobytes()
                self.assertEqual(reading["pixel_sha256"],hashlib.sha256(frame).hexdigest())
                self.assertEqual(reading["nonzero_pixels"],sum(bool(x) for x in frame))
                if run == "106-selector":
                    number=int(reading["interpreted_text"].rsplit("#",1)[1])
                    action_label=label.rsplit("-sample-",1)[0]+"-start"
                    step=next(x for x in raw["steps"] if x["label"]==action_label)
                    self.assertIn(number,[x["number"] for x in step["transitions"]["solenoids"] if 1 in x["states"]])


if __name__ == "__main__":
    unittest.main()
