"""Haunted House facts that generic System80 or legacy imports get wrong."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"tools"),str(ROOT/"src")]

import curate_haunted_house as c
from haunted_house_layout import plan
from haunted_house_runtime_evidence import derive
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_against_schema, validate_machine


def by_address(definition: dict, collection: str, group: str) -> dict:
	return {d["binding"]["device"]:d for d in definition[collection] if d["binding"]["group"]==group}


class HauntedHouseTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition=load_json(ROOT/c.DEFINITION)
		cls.facts=load_json(ROOT/c.FACTS)
		cls.inputs=by_address(cls.definition,"inputs",c.SWITCH)
		cls.dips=by_address(cls.definition,"inputs",c.DIP)
		cls.lamps=by_address(cls.definition,"outputs",c.LAMP)
		cls.solenoids=by_address(cls.definition,"outputs",c.SOL)

	def test_deterministic_definition_seed_knowledge_and_reports(self) -> None:
		for name,data in c.artifacts().items():
			self.assertEqual(data,(ROOT/name).read_bytes(),name)
		self.assertEqual((ROOT/c.SEED).read_bytes(),(ROOT/c.DEFINITION).read_bytes())
		self.assertEqual([],validate_machine(self.definition,ROOT))
		self.assertEqual([],validate_against_schema(self.definition,ROOT/"schemas/machine.schema.json",c.DEFINITION))

	def test_identity_all_nine_drivers_and_no_cross_game_leak(self) -> None:
		self.assertEqual((c.MACHINE_ID,"669",1133,1982),tuple(self.definition["machine"][k] for k in ("id","model_number","ipdb_id","year")))
		catalog=load_json(ROOT/"catalog/pinmame.json")
		expected={d["id"] for d in catalog["drivers"] if d["machine_id"]==c.MACHINE_ID}
		actual={d["id"] for d in self.definition["drivers"]}
		self.assertEqual({"hh","hh7","hh_1","hh_3","hh_3a","hh_3b","hh_4","hh_4a","hh_4b"},actual)
		self.assertEqual(expected,actual)
		text=json.dumps(self.definition)+"\n"+(ROOT/c.KNOWLEDGE).read_text(encoding="utf-8")
		for machine in catalog["machines"]:
			if machine["id"]!=c.MACHINE_ID:
				self.assertNotIn(machine["id"],text)

	def test_exact_profile_address_enumeration(self) -> None:
		profile=load_json(ROOT/"controllers/pinmame/gts80.json")
		for group,devices in [(c.SWITCH,self.inputs),(c.DIP,self.dips),(c.LAMP,self.lamps),(c.SOL,self.solenoids)]:
			rules=next(g["address_rules"] for g in profile["groups"] if g["id"]==group)
			expected=set()
			for rule in rules:
				expected.update(rule["values"] if "values" in rule else range(rule["minimum"],rule["maximum"]+1))
			self.assertEqual(expected,set(devices),group)
		self.assertEqual(1,len(by_address(self.definition,"outputs",c.GI)))
		self.assertEqual("unknown",self.lamps[4]["availability"])
		self.assertEqual({4},{a for a,d in self.lamps.items() if d["availability"]=="unknown"})

	def test_physical_switch_assignments_and_shared_contacts(self) -> None:
		for address in (4,6,16,26,36,45,46,65,67):
			self.assertIn("main",self.inputs[address]["physical"]["location"])
		self.assertIn("cellar",self.inputs[21]["physical"]["location"])
		self.assertIn("Right Side Kicker",self.inputs[65]["label"])
		self.assertNotIn("Shooter",self.inputs[65]["label"])
		self.assertEqual({42:2,44:2,51:3,66:2},{a:self.inputs[a]["physical"]["quantity"] for a in (42,44,51,66)})
		self.assertEqual(2,self.inputs[57]["physical"]["quantity"])
		self.assertTrue(all(self.inputs[a]["availability"]=="unused" for a in range(70,78)))
		for address in (0,1,2,3,4,5,6):
			aliases={(a["namespace"],a["value"]) for a in self.inputs[address]["aliases"]}
			for value in (str(address),f"{address:02}",f"{address:03}"):
				self.assertIn(("vpe-legacy.switch",value),aliases)

	def test_polarity_and_delivered_slam_level(self) -> None:
		self.assertTrue(self.inputs[-1]["normally_closed"])
		self.assertFalse(self.inputs[-1]["initial_active"])
		self.assertIn("opened/slammed",self.inputs[-1]["physical"]["notes"])
		for a,d in self.inputs.items():
			if d["availability"]=="used" and a!=-1:
				self.assertFalse(d["normally_closed"],a)
		self.assertFalse(self.inputs[36]["normally_closed"])
		self.assertIn("separate",self.inputs[36]["physical"]["notes"])

	def test_lamp_driven_actuators_and_k_relay_topology(self) -> None:
		self.assertEqual({0:"relay",1:"relay",2:"coil",12:"relay",13:"coil",15:"coil",16:"coil",17:"relay"},{a:self.lamps[a]["kind"] for a in (0,1,2,12,13,15,16,17)})
		lockout=self.lamps[2]
		self.assertEqual("coil.coin-lockout",lockout["id"])
		self.assertNotIn("part_number",self.solenoids[8]["physical"])
		self.assertEqual({("pinmame.lamp","2")},{(a["namespace"],a["value"]) for a in lockout["aliases"]})
		self.assertEqual(("cabinet coin door","cabinet_or_service"),(lockout["physical"]["location"],lockout["spatial"]["reason"]))
		self.assertNotIn("part_number",lockout["physical"])
		self.assertEqual(("877",24,"dc"),tuple(lockout["wiring"][k] for k in ("drive_wire","nominal_voltage_v","voltage_type")))
		self.assertEqual(("A3J5-2","Q3"),tuple(lockout["wiring"][k] for k in ("drive_connection","driver_transistor")))
		for address in (12,13,15,16):
			self.assertEqual((24,"dc"),tuple(self.lamps[address]["wiring"][k] for k in ("nominal_voltage_v","voltage_type")))
			self.assertIn("drive_wire",self.lamps[address]["wiring"])
			self.assertIn("part_number",self.lamps[address]["physical"])
		self.assertEqual("A-20558",self.lamps[12]["physical"]["part_number"])
		self.assertIn("A-21741",self.lamps[12]["physical"]["notes"])
		self.assertEqual("A-17891",self.lamps[13]["physical"]["part_number"])
		self.assertEqual("A-17875",self.lamps[16]["physical"]["part_number"])
		self.assertNotIn("lamp",self.lamps[15]["id"])
		self.assertEqual(2,self.lamps[3]["physical"]["quantity"])
		self.assertEqual("Q4",self.lamps[3]["wiring"]["driver_transistor"])
		for address,expected in {2:set(),3:{"L2","L3"},10:{"L11"},11:{"L10"}}.items():
			self.assertEqual(expected,{a["value"] for a in self.lamps[address]["aliases"] if a["namespace"]=="manual.address"})
		self.assertEqual(("A3J2-2","Q5 MPS-A13"),tuple(self.lamps[4]["wiring"][k] for k in ("drive_connection","driver_transistor")))
		self.assertIn("High Game to Date",self.lamps[10]["label"])
		self.assertIn("Game Over",self.lamps[11]["label"])
		self.assertEqual("control_signal",self.lamps[9]["kind"])

	def test_solenoid_projection_notes_belong_to_their_devices(self) -> None:
		for address in (1,2,5,6,8,9):
			note=self.solenoids[address]["physical"]["notes"].lower()
			self.assertEqual(address==5, "reset" in note and "bank" in note, address)
		self.assertNotIn("project",self.solenoids[8]["physical"]["notes"].lower())
		self.assertEqual("cabinet_or_service",self.solenoids[8]["spatial"]["reason"])
		self.assertIn("Kicker1 is a hidden trough surrogate",self.solenoids[9]["physical"]["notes"])

	def test_synthetic_outputs_and_inverted_latches_are_not_extra_coils(self) -> None:
		for a in (10,11,45,46,47,48):
			self.assertEqual("virtual",self.solenoids[a]["kind"])
			self.assertEqual("virtual",self.solenoids[a]["spatial"]["reason"])
		for a in (3,4,7):
			self.assertEqual("optional",self.solenoids[a]["availability"])
		for a in (48,49,50):
			self.assertEqual(("virtual","used"),(self.lamps[a]["kind"],self.lamps[a]["availability"]))
		self.assertEqual("lamp",self.lamps[51]["kind"])
		pairs={(r["source"],r["destination"]) for r in self.definition["relationships"] if r["kind"]=="inverted"}
		self.assertEqual({(self.lamps[a]["id"],self.lamps[a+4]["id"]) for a in range(44,48)},pairs)
		for a in range(52,61):
			self.assertEqual(("virtual","optional"),(self.lamps[a]["kind"],self.lamps[a]["availability"]))

	def test_displays_and_driver_specific_conversions(self) -> None:
		displays={d["controller_index"]:d for d in self.definition["displays"]}
		self.assertEqual(set(range(9)),set(displays))
		self.assertEqual([2,9,22,29,40,41,42,43,50],[displays[i]["segment_start"] for i in range(9)])
		self.assertEqual([6,6,6,6,1,1,1,1,6],[displays[i]["width"] for i in range(9)])
		self.assertTrue(all(displays[i]["physical_location"]=="cabinet_or_service" for i in range(8)))
		self.assertEqual("playfield",displays[8]["physical_location"])
		self.assertEqual("observed",displays[8]["spatial"]["status"])
		drivers={d["id"]:d for d in self.definition["drivers"]}
		self.assertEqual({"identical"},{drivers[a]["physical_compatibility"] for a in ("hh","hh_1","hh_3","hh_3a","hh_3b")})
		self.assertEqual({"compatible"},{drivers[a]["physical_compatibility"] for a in ("hh7","hh_4","hh_4a","hh_4b")})
		self.assertEqual({7},{o["width"] for o in drivers["hh7"]["display_overrides"]})
		self.assertEqual(4,len(drivers["hh7"]["display_overrides"]))
		self.assertIn("no new physical tunnel gate",drivers["hh_3b"]["variant_notes"])
		self.assertIn("NO_DUMP",drivers["hh_4"]["variant_notes"])
		self.assertEqual("optional",self.dips[38]["availability"])
		self.assertEqual("optional",self.dips[39]["availability"])
		self.assertIn("Speech",self.dips[38]["label"])

	def test_mechanism_inventory_does_not_invent_cpu_reflex_coils(self) -> None:
		m={m["id"]:m for m in self.definition["mechanisms"]}
		self.assertEqual([],m["mechanism.secret-passage"]["actuators"])
		self.assertIn("spring",m["mechanism.secret-passage"]["behavior"])
		self.assertEqual([self.inputs[26]["id"]],m["mechanism.secret-passage"]["sensors"])
		self.assertEqual([self.inputs[36]["id"]],m["mechanism.trap-door"]["sensors"])
		self.assertEqual([],m["mechanism.local-reflex-devices"]["actuators"])
		self.assertEqual([],m["mechanism.eight-flippers"]["actuators"])
		self.assertIn("Eight",m["mechanism.eight-flippers"]["label"])
		self.assertIn("#313",m["mechanism.illumination-selection"]["behavior"])

	def test_drawing_measurements_exclude_labels_and_disclose_extrapolation(self) -> None:
		layout=load_json(ROOT/c.LAYOUT)
		p=plan(self.facts,layout)
		self.assertEqual([.794,.133],p["measurements"]["lamp:40"]["xy"])
		self.assertNotIn("lamp:8",p["measurements"])
		self.assertNotIn("lamp:21",p["measurements"])
		self.assertNotIn("lamp:44",p["measurements"])
		self.assertTrue(p["measurements"]["switch:67"]["extrapolated"])
		self.assertTrue(p["frames"]["main"]["minimum_full_field_span_met"])
		self.assertFalse(p["frames"]["upper"]["minimum_full_field_span_met"])
		bad=copy.deepcopy(layout)
		read=next(r for r in bad["frames"]["upper"]["reads"] if r["label"]=="L40")
		read["point"]="balloon_center"
		self.assertNotIn("lamp:40",plan(self.facts,bad)["measurements"])
		self.assertNotIn("spatial",self.lamps[21])
		self.assertEqual("observed",self.lamps[16]["spatial"]["status"])
		self.assertIn("vpx.haunted-house.vpw-table",self.lamps[16]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertIn("drawing-projection",self.inputs[67]["spatial"]["placements"][0]["id"])

	def test_partial_gate_cannot_be_bypassed_with_status_edit(self) -> None:
		self.assertEqual(["output_semantics","provenance","spatial_placement"],self.definition["coverage"]["missing"])
		self.assertEqual("partial",self.definition["coverage"]["status"])
		bad=copy.deepcopy(self.definition)
		bad["coverage"].update(status="author_ready",missing=[])
		errors=validate_machine(bad,ROOT)
		self.assertTrue(any("unknown" in e or "validated" in e or "spatial" in e for e in errors),errors)
		report=load_json(ROOT/c.REPORT)
		self.assertEqual("pinmame-spatial-blockers",report["format"])
		self.assertIn(self.lamps[4]["id"],report["unplaced"])

	def test_check_refuses_drift_and_existing_author_ready_artifact(self) -> None:
		with tempfile.TemporaryDirectory() as name:
			root=Path(name)
			for relative,data in c.artifacts().items():
				p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
			c.check(root)
			(root/c.KNOWLEDGE).write_text("changed",encoding="utf-8")
			with self.assertRaisesRegex(RuntimeError,"curation drift"):
				c.check(root)
			protected=root/f"machines/author-ready/{c.RELATIVE}.json"
			protected.parent.mkdir(parents=True,exist_ok=True);protected.write_text("protected",encoding="utf-8")
			with self.assertRaisesRegex(RuntimeError,"author-ready"):
				c.generate(root)
			self.assertEqual("protected",protected.read_text(encoding="utf-8"))

	def test_excerpt_digest_guard_and_external_root_guard_can_fail(self) -> None:
		with tempfile.TemporaryDirectory() as name:
			root=Path(name)
			source=copy.deepcopy(self.facts["sources"][0])
			source["excerpts"]=source["excerpts"][:1]
			p=root/source["excerpts"][0]["path"];p.parent.mkdir(parents=True);p.write_text("altered cell",encoding="utf-8")
			with mock.patch.object(c,"ROOT",root),self.assertRaisesRegex(RuntimeError,"changed excerpt"):
				c.source_records({"sources":[source]})
			with mock.patch.dict(os.environ,{"PINMAME_MANUALS_ROOT":str(root)}),self.assertRaisesRegex(RuntimeError,"external evidence"):
				c.verify_external_inputs()
			p=root/self.facts["runtime_runs"][0]["scenario_path"]
			p.parent.mkdir(parents=True,exist_ok=True);p.write_text("{}",encoding="utf-8")
			with mock.patch.object(c,"ROOT",root),mock.patch.object(c,"load_json",return_value=self.facts),self.assertRaisesRegex(RuntimeError,"changed committed scenario"):
				c.verify_external_inputs()

	def test_runtime_evidence_has_no_host_write_as_rom_observation(self) -> None:
		for run in self.facts["runtime_runs"]:
			path=ROOT/run["scenario_path"]
			self.assertEqual(run["scenario_sha256"],hashlib.sha256(path.read_bytes()).hexdigest())
			self.assertEqual("hh",load_json(path)["game"])
		evidence=load_json(ROOT/"evidence/runtime/gottlieb.haunted-house.1982.json")
		self.assertEqual([],validate_against_schema(evidence,ROOT/"schemas/evidence.schema.json","Haunted House runtime"))
		observations=evidence["runtime"]["observations"]
		self.assertEqual([1,2,5,6,8,9],observations["ordered_solenoid_on_sequence"])
		actions={a["label"]:a for a in observations["runs"]["gameplay"]["named_action_observations"]}
		self.assertTrue(all(not a["observed_switch_addresses"] for a in actions.values()))
		self.assertEqual([112],actions["right main flipper synthetic state"]["host_stimulus_switch_addresses"])
		self.assertEqual([45,46],actions["right main flipper synthetic state"]["transitioned_solenoid_addresses"])
		self.assertEqual([],actions["right flipper after tilt"]["transitioned_solenoid_addresses"])


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"),"retained VPX root not configured")
class HauntedHouseRetainedVpxTests(unittest.TestCase):
	def test_source_manifests_and_exact_bound_object_centres(self) -> None:
		from pinmame_game_defs.spatial import _item_point
		c.verify_external_inputs()
		root=Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		facts=load_json(ROOT/c.FACTS)
		for name,p in facts["table_points"].items():
			file=root/p["path"]
			self.assertEqual(p["sha256"],hashlib.sha256(file.read_bytes()).hexdigest(),name)
			if p["method"]=="world_mesh_bounds_center":
				from haunted_house_layout import world_object_bounds
				bounds=world_object_bounds(file,{p["object_name"]})[p["object_name"]]
				self.assertEqual(p["bounds"],bounds["bounds"])
				self.assertEqual((p["x"],p["y"]),tuple(bounds["center"][:2]))
				continue
			kind,raw=next(iter(load_json(file).items()))
			x,y,method=_item_point(kind,raw)
			self.assertEqual((p["x"],p["y"],p["method"]),(x,y,method),name)


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"),"retained review/runtime root not configured")
class HauntedHouseRetainedRuntimeTests(unittest.TestCase):
	def test_recompute_from_raw_rom_outputs_and_refuse_changed_trace(self) -> None:
		root=Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).parent/"runtime-evidence"
		self.assertEqual(canonical_bytes(derive(root)),(ROOT/"evidence/runtime/gottlieb.haunted-house.1982.json").read_bytes())
		with tempfile.TemporaryDirectory() as name:
			fake=Path(name)
			info=load_json(ROOT/c.FACTS)["runtime_runs"][0]
			p=fake/info["raw_run_relative_path"];p.parent.mkdir(parents=True);p.write_text("{}",encoding="utf-8")
			with self.assertRaisesRegex(RuntimeError,"changed raw trace"):
				derive(fake)


if __name__=="__main__":
	unittest.main()
