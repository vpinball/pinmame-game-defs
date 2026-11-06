from __future__ import annotations

import copy
import importlib
import json
import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_xmen_pro_spatial as curator
import xmen_pro_harness as dmd
import xmen_pro_vpt_geometry as biff
import xmen_pro_drawing_geometry as drawings
import drawing_callouts
from build_external_evidence_manifest import write_manifest
from pinmame_game_defs.jsonio import load_json, write_json


def addresses(definition, collection, group):
    return {d["binding"]["device"]: d for d in definition[collection] if d["binding"]["group"] == group}


def record(tag: str, payload: bytes = b"") -> bytes:
    return struct.pack("<I", len(payload) + 4) + tag.encode("ascii") + payload


def light(*extra: bytes) -> bytes:
    return struct.pack("<I", 7) + record("VCEN", struct.pack("<ff", 40.25, 100.5)) + record("NAME", struct.pack("<I", 4) + "l3".encode("utf-16-le")) + b"".join(extra) + record("ENDB")


class XMenProSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.definition, cls.report = curator.build()
        cls.seed = load_json(ROOT / curator.SEED_RELATIVE)

    def without_measurements(self,seed):
        definition=copy.deepcopy(self.definition)
        ids={m["device_id"] for m in [*seed["measurements"].values(),*seed["elevation_measurements"].values(),*seed["local_photo_measurements"].values(),*seed["trough_contact_projection"]["contacts"]]}
        for device in definition["inputs"]+definition["outputs"]:
            if device["id"] in ids:device.pop("spatial",None)
        return definition

    def test_physical_pro_flasher_inventory_and_magnet_are_edition_matched(self):
        coils = addresses(self.definition, "outputs", "pinmame.output.solenoid")
        expected = {17: 2, 18: 2, 21: 1, 22: 2, 25: 1, 27: 1, 28: 3, 29: 3, 31: 1}
        self.assertEqual(expected, curator.FLASHER_QUANTITIES)
        for address, quantity in expected.items():
            self.assertEqual(quantity, coils[address]["physical"]["quantity"])
            if address in {17,18,21,22,25,27}:
                self.assertEqual(quantity, len(coils[address]["spatial"]["placements"]))
                self.assertEqual("validated", coils[address]["spatial"]["status"])
            elif address in {28,29}:
                self.assertEqual(quantity,len(coils[address]["spatial"]["placements"]))
                self.assertEqual("observed",coils[address]["spatial"]["status"])
            else:
                self.assertNotIn("spatial", coils[address], "an ambiguous fitting or sprite is not a socket")
            self.assertIn(curator.MANUAL_SOURCE, coils[address]["provenance"]["source_refs"])
        self.assertEqual("Magneto spotlight", coils[27]["label"])
        self.assertEqual("Magneto figure flasher", coils[31]["label"])
        self.assertEqual(("VIO-YEL", "J10-P8", 50), tuple(coils[32]["wiring"][k] for k in ("power_wire", "power_connection", "nominal_voltage_v")))
        self.assertEqual(("ORG", "J6-P10", 20), tuple(coils[27]["wiring"][k] for k in ("power_wire", "power_connection", "nominal_voltage_v")))
        self.assertEqual("165-5032-00", coils[27]["physical"]["part_number"])
        self.assertFalse(set(range(51,59)) & set(coils))

    def test_complete_pro_lamp_matrix_closes_only_the_real_lamp_59_conflict(self):
        lamps = addresses(self.definition, "outputs", "pinmame.output.lamp")
        self.assertEqual(set(range(1,81)), set(lamps))
        self.assertEqual(set(curator.LAMP_NAMES), {n for n,d in lamps.items() if d["availability"] == "used"})
        for n in (1,2):
            self.assertEqual("cabinet_or_service", lamps[n]["spatial"]["reason"])
        self.assertEqual("Left eject top", lamps[59]["label"])
        self.assertEqual("validated", lamps[59]["provenance"]["status"])
        self.assertEqual("validated", lamps[59]["spatial"]["status"])
        self.assertEqual((0.171,0.505), tuple(lamps[59]["spatial"]["placements"][0][k] for k in ("x","y")))
        self.assertIn("reflection helper", lamps[59]["physical"]["notes"])
        self.assertEqual("unused", lamps[63]["availability"])
        self.assertEqual("Right two-bank top", lamps[48]["label"])
        self.assertEqual("Right two-bank bottom", lamps[49]["label"])
        self.assertEqual([], self.definition["conflicts"])
        self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])

    def test_each_observed_point_recomputes_from_its_own_exact_object(self):
        objects = {row["name"]: row for row in self.seed["items"]}
        switches = addresses(self.definition, "inputs", "pinmame.input.switch")
        coils = addresses(self.definition, "outputs", "pinmame.output.solenoid")
        lamps = addresses(self.definition, "outputs", "pinmame.output.lamp")
        mappings = [(switches[n],name) for n,name in curator.INPUT_OBJECTS.items()] + [(coils[n],name) for n,name in curator.COIL_OBJECTS.items()] + [(lamps[n],f"l{n}") for n in curator.LAMP_NAMES if n not in {1,2,59}]
        for device, name in mappings:
            with self.subTest(device=device["id"], name=name):
                x,y = curator.object_position(objects[name])
                point = device["spatial"]["placements"][0]
                self.assertEqual((round(x/959,6),round(y/2162,6)), (point["x"],point["y"]))
                validated_ids = set(load_json(ROOT / drawings.SEED)["checks"]) - set(self.report["drawing_reconciliation"]["not_validated"])
                self.assertEqual("validated" if point["id"] in validated_ids else "observed", device["spatial"]["status"])
                self.assertFalse(any(ref.startswith("vpx-table.x-men-le") for ref in point["provenance"]["source_refs"]))

    def test_custom_fade_loop_overrides_stale_timer_intervals(self):
        rows = {row["name"]: row for row in self.seed["items"]}
        bindings = {row["address"]: row["objects"] for row in self.seed["script_fade_l_bindings"]}
        lamps = addresses(self.definition, "outputs", "pinmame.output.lamp")
        for n in range(50,58):
            self.assertEqual(52, rows[f"l{n}"]["timer_interval"])
            self.assertEqual([f"l{n}",f"l{n}a"], bindings[n])
        for n in (60,61,62):
            self.assertEqual(100, rows[f"l{n}"]["timer_interval"])
            self.assertIn("custom ChangedLamps/FadeL", lamps[n]["physical"]["notes"])

    def test_missing_sensors_and_gi_cannot_be_satisfied_by_one_projection(self):
        switches = addresses(self.definition,"inputs","pinmame.input.switch")
        for n in range(18,21):
            self.assertEqual("observed",switches[n]["spatial"]["status"])
        contact_points=[tuple(switches[n]["spatial"]["placements"][0][k] for k in ("x","y")) for n in (18,19,20)]
        self.assertEqual(3,len(set(contact_points)))
        self.assertTrue(contact_points[0][0]<contact_points[1][0]<contact_points[2][0])
        beam21 = switches[21]["spatial"]["placements"][0]
        beam22 = switches[22]["spatial"]["placements"][0]
        self.assertEqual(tuple(beam21[k] for k in ("x","y")), tuple(beam22[k] for k in ("x","y")))
        self.assertIn("Vertically stacked", switches[21]["physical"]["notes"])
        self.assertIn(curator.MANUAL_HIRES_SOURCE, beam21["provenance"]["source_refs"])
        self.assertEqual("opto", switches[21]["physical"]["switch_type"])
        gi = addresses(self.definition,"outputs","pinmame.output.gi")[0]
        self.assertEqual("observed",gi["spatial"]["status"])
        self.assertEqual(35,len(gi["spatial"]["placements"]))
        self.assertNotIn("quantity", gi["physical"])
        self.assertEqual("partial", self.definition["coverage"]["status"])
        self.assertEqual("observed", self.definition["coverage"]["dimensions"]["spatial_placement"])
        self.assertEqual("remain_partial", self.report["promotion_decision"]["decision"])

    def test_report_preserves_failed_history_and_distinguishes_successor_scope(self):
        self.assertEqual(2, self.report["version"])
        self.assertEqual(9, len(self.report["historical_audit"]["unresolved_blockers"]))
        self.assertEqual(101, self.report["historical_audit"]["extraction"]["vpxtool"]["failure"]["exit_code"])
        self.assertEqual(biff.RAW_MANIFEST_SHA256,self.report["extraction"]["successor"]["raw_manifest_sha256"])
        self.assertFalse(self.report["extraction"]["successor"]["full_semantic_parse"])
        self.assertEqual({"gi-0-pro-socket-geometry","physical-emitter-centers","switches-18-through-20-trough-centers","observed-layout-reconciliation"}, {row["id"] for row in self.report["unresolved_blockers"]})

    def test_independent_drawing_reads_recompute_and_do_not_validate_controls(self):
        seed=load_json(ROOT/drawings.SEED)
        decisions=drawing_callouts.evaluate(seed,drawing_callouts.placements_of(self.definition))
        self.assertEqual(64,len(decisions["placements"]))
        self.assertTrue(all(d["agrees"] for d in decisions["placements"].values()))
        self.assertTrue(all(page["control_loo_max"] < .032 for page in decisions["pages"].values()))
        lamps=addresses(self.definition,"outputs","pinmame.output.lamp")
        for n in (3,60,61,62):
            self.assertNotIn(lamps[n]["spatial"]["placements"][0]["id"],seed["checks"])
            self.assertEqual("observed",lamps[n]["spatial"]["status"])
        self.assertEqual(38,len(seed["measurements"]))
        self.assertEqual(12,len(seed["elevation_measurements"]))
        self.assertEqual({"q22-left","q22-right"},set(seed["historically_rejected_measurements"]))
        self.assertEqual("q22_identity_resolved_by_new_pro_evidence",seed["reassessment"]["status"])
        for pid, measurement in seed["measurements"].items():
            self.assertNotIn(pid,seed["checks"])
            self.assertEqual(tuple(measurement["normalized"]),drawing_callouts.measured(seed,pid))

    def test_rear_photo_reverses_view_and_cannot_be_promoted_by_status_edit(self):
        seed=load_json(ROOT/drawings.SEED)
        coils=addresses(self.definition,"outputs","pinmame.output.solenoid")
        self.assertLess(max(p["x"] for p in coils[28]["spatial"]["placements"]),min(p["x"] for p in coils[29]["spatial"]["placements"]))
        for pid,item in seed["elevation_measurements"].items():
            self.assertEqual(tuple(item["normalized"]),drawing_callouts.elevation_measured(seed,pid))
            self.assertEqual(0,item["normalized"][1])
        next(iter(seed["elevation_measurements"].values()))["status"]="validated"
        definition=self.without_measurements(seed)
        with self.assertRaisesRegex(ValueError,"perspective"):
            drawings.add_measurements(definition,seed,curator.MANUAL_SOURCE)

    def test_partial_gi_census_cannot_become_a_whole_quantity(self):
        seed=load_json(ROOT/drawings.SEED)
        self.assertFalse(seed["partial_censuses"]["gi.master"]["complete"])
        self.assertEqual(35,len(seed["partial_censuses"]["gi.master"]["known_emitter_ids"]))
        # Test the declared census gate without re-adding existing placements.
        for mutation in ("complete","missing"):
            changed=copy.deepcopy(seed)
            if mutation=="complete":changed["partial_censuses"]["gi.master"]["complete"]=True
            else:changed["partial_censuses"]["gi.master"]["known_emitter_ids"].pop()
            definition=self.without_measurements(changed)
            with self.assertRaises(ValueError):drawings.add_measurements(definition,changed,curator.MANUAL_SOURCE)

    def test_local_photo_cannot_extrapolate_or_replace_independent_controls(self):
        original=load_json(ROOT/drawings.SEED)
        proof=self.report["drawing_measurements"]["flasher.magneto-spotlight.emitter"]
        self.assertTrue(proof["inside_control_hull"])
        self.assertLess(proof["control_loo_max"],.027)
        for mutation in ("outside","few","wrong"):
            seed=copy.deepcopy(original);m=seed["local_photo_measurements"]["flasher.magneto-spotlight.emitter"]
            if mutation=="outside":m["pixel"]=[500,500]
            elif mutation=="few":m["controls"]=m["controls"][:5]
            else:m["controls"][0]["xy"][0]+=.01
            with self.assertRaises(ValueError):drawings.add_measurements(self.without_measurements(seed),seed,curator.MANUAL_SOURCE)

    def test_raised_trough_contacts_preserve_their_parallax_limit(self):
        seed=load_json(ROOT/drawings.SEED)
        for pid in ("switch.trough-4-left.sensor","switch.trough-3.sensor","switch.trough-2.sensor"):
            self.assertLess(self.report["drawing_measurements"][pid]["cross_plane_coordinate"],0)
            self.assertFalse(self.report["drawing_measurements"][pid]["coplanarity_validated"])
        seed["trough_contact_projection"]["contacts"][0]["status"]="validated"
        with self.assertRaisesRegex(ValueError,"raised contact"):
            drawings.add_measurements(self.without_measurements(seed),seed,curator.MANUAL_SOURCE)
        with self.assertRaisesRegex(ValueError,"degenerate"):
            drawings.rectify_quadrilateral([[0,0]]*4,[1,1])

    def test_changed_calibration_or_weakened_limit_is_rejected(self):
        objects={row["name"]:row for row in self.seed["items"]}
        original=load_json(ROOT/drawings.SEED)
        for mutation in ("limit","coordinate","cluster"):
            seed=copy.deepcopy(original)
            if mutation=="limit":seed["limit"]=.1
            elif mutation=="coordinate":seed["pages"]["lamps"]["controls"][0]["xy"][0]+=.01
            else:seed["pages"]["coils"]["controls"][0]["pixel"]=[10000,10000]
            with self.assertRaises(ValueError):
                drawings.validate_controls(seed,objects,curator.object_position)

    def test_extrapolation_needs_a_second_drawing_and_never_checks_itself(self):
        original=load_json(ROOT/drawings.SEED)
        pid="flasher.left-side.emitter.upper"
        self.assertFalse(drawings.inside_hull(original["measurements"][pid]["pixel"],original["pages"]["coils"]["controls"]))
        for mutation in ("missing","self","wrong"):
            seed=copy.deepcopy(original);measurement=seed["measurements"][pid]
            if mutation=="missing":measurement.pop("second_read")
            elif mutation=="self":measurement["second_read"]["page"]="coils"
            else:measurement["second_read"]["pixel"]=[2000,3000]
            # Remove existing drawing placements to test the safety gate itself.
            definition=copy.deepcopy(self.definition)
            for d in definition["outputs"]:
                if d["id"] in {v["device_id"] for v in seed["measurements"].values()}:d.pop("spatial",None)
            with self.assertRaises(ValueError):
                drawings.add_measurements(definition,seed,curator.MANUAL_SOURCE)

    def test_curator_is_idempotent_and_drift_check_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            curator.generate(root=root)
            before=(root/"machines/partial/stern/x-men-pro-2012.json").read_bytes()
            curator.generate(root=root)
            self.assertEqual(before,(root/"machines/partial/stern/x-men-pro-2012.json").read_bytes())
            curator.generate(root=root,check=True)
            (root/"machines/partial/stern/x-men-pro-2012.json").write_bytes(before+b"\n")
            with self.assertRaisesRegex(ValueError,"output drift"):
                curator.generate(root=root,check=True)
            self.assertFalse((root/"machines/author-ready/stern/x-men-limited-edition-2012.json").exists())

    def test_curator_refuses_an_existing_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=root/"machines/author-ready/stern/x-men-pro-2012.json"
            path.parent.mkdir(parents=True);path.write_text("owned",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"author-ready"):
                curator.generate(root=root)
            self.assertEqual("owned",path.read_text())

    def test_seed_missing_or_wrong_lamp_binding_fails_closed(self):
        real_load=curator.load_json
        for mutation in ("missing", "binding"):
            seed=copy.deepcopy(self.seed)
            if mutation=="missing": seed["items"].pop()
            else: seed["script_fade_l_bindings"][0]["objects"][0]="l63"
            def loader(path):
                return seed if path.as_posix().endswith(curator.SEED_RELATIVE) else real_load(path)
            with patch.object(curator,"load_json",side_effect=loader), self.assertRaises(ValueError):
                curator.build()

    def test_upstream_status_change_cannot_silently_promote(self):
        original=curator.build_pro();original["coverage"]["status"]="author_ready"
        with patch.object(curator,"build_pro",return_value=original), self.assertRaisesRegex(ValueError,"cannot be promoted"):
            curator.build()

    def test_unrelated_upstream_conflict_cannot_be_silently_cleared(self):
        original=copy.deepcopy(curator.build_pro())
        original["conflicts"].append({
            "id":"conflict.unrelated-upstream",
            "path":"outputs[pinmame.output.solenoid:32]",
            "description":"A separate upstream ambiguity.",
            "source_refs":[curator.PRO_VPX_TABLE_SOURCE],
        })
        with patch.object(curator,"build_pro",return_value=original), self.assertRaisesRegex(ValueError,"cannot be silently cleared"):
            curator.build()

    def test_reproducible_figure_candidate_does_not_establish_fixture_identity(self):
        seed=load_json(ROOT/drawings.SEED)
        candidate=seed["q31_candidate"]
        page=seed["pages"][candidate["page"]]
        primary=drawing_callouts.apply(drawing_callouts.fit((c["pixel"],c["xy"]) for c in page["controls"]),candidate["pixel"])
        other=seed["pages"][candidate["second_read"]["page"]]
        secondary=drawing_callouts.apply(drawing_callouts.fit((c["pixel"],c["xy"]) for c in other["controls"]),candidate["second_read"]["pixel"])
        self.assertEqual(candidate["candidate_normalized"],[round(v,3) for v in primary])
        self.assertAlmostEqual(candidate["second_page_offset"],drawing_callouts.distance(primary,secondary),places=6)
        self.assertLess(drawing_callouts.distance(primary,secondary),drawing_callouts.LIMIT)
        self.assertEqual("candidate_only_not_canonical",candidate["status"])
        self.assertNotIn("spatial",addresses(self.definition,"outputs","pinmame.output.solenoid")[31])

    def test_sprite_and_outside_point_are_rejected(self):
        with self.assertRaisesRegex(ValueError,"sprite"):
            curator.object_position({"name":"f59b","type":"Flasher","center":[10,20]})
        with self.assertRaisesRegex(ValueError,"out-of-range"):
            curator.observed_location({"id":"test"},"sensor",{"name":"bad","type":"Trigger","center":[-1,0],"stream":"fake"},"")

    def test_biff_reader_rejects_truncated_duplicate_and_nonfinite_coordinates(self):
        self.assertEqual([40.25,100.5],biff.item(light(),"GameStg/GameItem0")["center"])
        variants=[light()[:-1],light(record("VCEN",struct.pack("<ff",0,0))),light().replace(struct.pack("<ff",40.25,100.5),struct.pack("<ff",float("nan"),0)),light().replace(struct.pack("<I",4)+"l3".encode("utf-16-le"),struct.pack("<I",8)+"l3".encode("utf-16-le"))]
        for data in variants:
            with self.assertRaises((ValueError,UnicodeError,struct.error)):
                biff.item(data,"GameStg/GameItem0")

    def test_resealed_wrong_raw_tree_is_not_accepted_as_the_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/"arbitrary").write_text("changed")
            write_manifest(root,"xmn_151")
            with self.assertRaisesRegex(ValueError,"differs from the exact"):
                biff.recover(root)

    def test_title_adapter_refuses_unknown_or_ambiguous_targets(self):
        with self.assertRaises(ValueError):
            dmd.check_targets({"actions":[{"type":"pulse_until_display","texts":["SWITCH TEST"]}]})
        self.assertEqual([],dmd.match_titles(bytes(4096),128,32))
        self.assertEqual([],dmd.match_titles(bytes(4096),64,64))
        import base64
        for title,data in dmd.TEMPLATES.items():
            frame=bytearray(4096);mask=base64.b64decode(data["mask"]);first,last=data["rows"];left,right=data["columns"]
            for index,(y,x) in enumerate((y,x) for y in range(first,last+1) for x in range(left,right)):
                frame[y*128+x]=mask[index]
            self.assertIn(title,dmd.match_titles(frame,128,32))
            index=next(i for i,v in enumerate(frame) if v);frame[index]=0
            self.assertNotIn(title,dmd.match_titles(frame,128,32),"a changed title must not checkpoint")

    def test_portable_runtime_readings_pair_selector_and_public_address(self):
        readings=load_json(ROOT/curator.RUNTIME_RELATIVE)
        lamps={r["address"]:r for r in readings["runs"]["lamp"]["readings"]}
        coils={r["address"]:r for r in readings["runs"]["coil"]["readings"]}
        self.assertEqual(set(range(1,81)),set(lamps))
        self.assertEqual("LEFT EJECT TOP",lamps[59]["interpreted_text"])
        self.assertEqual("NOT USED",lamps[63]["interpreted_text"])
        self.assertEqual("FLASH: MAGNETO (LEFT/RIGHT) (X2)",coils[22]["interpreted_text"])
        self.assertEqual(20,coils[22]["selector_ordinal"])
        self.assertFalse({19,20,23,30}&set(coils))

    def test_external_evidence_roots_when_configured_are_strict(self):
        if not any(os.environ.get(name) for name in ("PINMAME_VPX_SOURCES_ROOT","PINMAME_MANUALS_ROOT","PINMAME_REVIEW_ARTIFACTS_ROOT")):
            self.skipTest("external evidence roots not configured")
        curator.verify_external(ROOT)

    def test_wrong_manual_root_fails_instead_of_skipping(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ,{"PINMAME_MANUALS_ROOT":directory},clear=True):
            with self.assertRaises(FileNotFoundError):
                curator.verify_external(ROOT)


if __name__=="__main__":
    unittest.main()
