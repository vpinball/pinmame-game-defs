"""Identity, System 1 routing and evidence guards for Joker Poker's honest partial."""
from __future__ import annotations

import copy
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curate_joker_poker as curator
from pinmame_game_defs.jsonio import canonical_bytes, load_json
from pinmame_game_defs.validation import validate_machine


def addressed(items, group):
	return {item["binding"]["device"]: item for item in items if item["binding"]["group"] == group}


class JokerPokerTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.definition = load_json(ROOT / curator.DEFINITION_PATH)
		cls.switches = addressed(cls.definition["inputs"], curator.SWITCH)
		cls.dips = addressed(cls.definition["inputs"], curator.DIP)
		cls.solenoids = addressed(cls.definition["outputs"], curator.SOLENOID)
		cls.lamps = addressed(cls.definition["outputs"], curator.LAMP)

	def test_exact_identity_and_single_physical_driver(self):
		machine = self.definition["machine"]
		self.assertEqual((curator.MACHINE_ID, "417 SS", 1978, 1306, "GR9o1-MQjj8"),
			(machine["id"], machine["model_number"], machine["year"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual(["jokrpokr"], [x["id"] for x in self.definition["drivers"]])
		self.assertEqual("identical", self.definition["drivers"][0]["physical_compatibility"])
		self.assertEqual("pinmame.gts1", self.definition["controller"]["platform"])
		self.assertEqual("0x100000000", self.definition["controller"]["hardware_generation"])
		catalog = load_json(ROOT / "catalog/pinmame.json")
		owners = [x for x in catalog["machines"] if x["id"] == curator.MACHINE_ID]
		self.assertEqual(1, len(owners))
		self.assertFalse((ROOT / "machines/stubs/pinmame/jokrpokr.json").exists())

	def test_complete_controller_enumeration(self):
		self.assertEqual(set(range(-8, 0)) | {10*r+s for r in range(8) for s in range(8)} | set(range(81, 89)), set(self.switches))
		self.assertEqual(set(range(1, 25)), set(self.dips))
		self.assertEqual(set(range(1, 49)), set(self.solenoids))
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual({5,15,25,35,45,55,65,75,46,14,24,34,60,61,62,63,64,70,71,72,73,74}, {n for n,x in self.switches.items() if x["availability"] == "unknown"})
		self.assertEqual(set(range(9,13)), {n for n,x in self.solenoids.items() if x["availability"] == "unknown"})
		self.assertEqual({5,6,7} | set(range(29,45)), {n for n,x in self.lamps.items() if x["availability"] == "unknown"})
		for n in range(5):
			self.assertEqual({str(n), f"{n:02}", f"{n:03}"}, {a["value"] for a in self.switches[n]["aliases"]})

	def test_lamp_17_is_the_kings_coil_and_ten_jacks_share_a_reset(self):
		self.assertEqual(("coil.kings-reset", "coil"), (self.lamps[17]["id"], self.lamps[17]["kind"]))
		mechanisms = {x["id"]: x for x in self.definition["mechanisms"]}
		self.assertEqual(["coil.kings-reset"], mechanisms["mechanism.kings"]["actuators"])
		self.assertEqual(["coil.ten-jacks-reset"], mechanisms["mechanism.ten-jacks"]["actuators"])
		self.assertEqual(["switch.ten-drop", "switch.jack-drop-1", "switch.jack-drop-2"], mechanisms["mechanism.ten-jacks"]["sensors"])
		self.assertEqual("switch.joker-drop", self.switches[52]["id"])
		self.assertEqual([], self.definition["relationships"])
		self.assertEqual(6, len(self.definition["mechanisms"]))

	def test_shared_inputs_have_all_observed_locations(self):
		for address in set(range(5)) | set(curator.SWITCH_OBJECTS):
			self.assertIn(curator.CHART, self.switches[address]["provenance"]["source_refs"])
		self.assertNotIn(curator.CHART, self.switches[56]["provenance"]["source_refs"])
		for n, count in {10:2, 11:2, 12:3, 13:2, 40:11}.items():
			self.assertEqual(count, len(self.switches[n]["spatial"]["placements"]))
		self.assertEqual("candidate", self.switches[40]["spatial"]["status"])
		self.assertNotIn("spatial", self.switches[66])
		self.assertNotIn("quantity", self.switches[40]["physical"])
		for item in self.definition["inputs"]:
			self.assertNotIn("normally_closed", item)

	def test_no_lamp_glow_or_synthetic_flipper_is_claimed_as_a_physical_emitter(self):
		for n, item in self.lamps.items():
			if item["kind"] == "lamp" and n != 3:
				self.assertNotIn("spatial", item, n)
		for n in range(45,49):
			self.assertEqual("used", self.solenoids[n]["availability"])
			self.assertEqual("virtual", self.solenoids[n]["kind"])
			self.assertEqual("virtual", self.solenoids[n]["spatial"]["reason"])
		self.assertEqual("button.flipper.right", self.switches[82]["roles"][0])
		self.assertEqual("button.flipper.left", self.switches[84]["roles"][0])
		self.assertFalse(any(x["binding"]["group"] == "pinmame.output.gi" for x in self.definition["outputs"]))

	def test_display_memory_order_matches_sys1_disp(self):
		self.assertEqual([(0,12,6),(1,18,6),(2,0,6),(3,6,6),(4,40,2),(5,32,2)],
			[(d["controller_index"],d["segment_start"],d["width"]) for d in self.definition["displays"]])
		self.assertTrue(all(d["spatial"]["reason"] == "cabinet_or_service" for d in self.definition["displays"]))
		for display in self.definition["displays"]:
			self.assertEqual("observed", display["provenance"]["status"])
			self.assertTrue({curator.GAME, curator.SCRIPT, curator.BACKBOX_PHOTO} <= set(display["provenance"]["source_refs"]))

	def test_partial_does_not_gain_readiness_from_controller_enumeration(self):
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual({"input_semantics","output_semantics","mechanism_inventory","mechanism_behavior","polarity","provenance","spatial_placement"}, set(self.definition["coverage"]["missing"]))
		promoted = copy.deepcopy(self.definition)
		promoted["coverage"]["status"] = "author_ready"
		promoted["coverage"]["missing"] = []
		self.assertTrue(validate_machine(promoted))
		self.assertFalse((ROOT / "machines/author-ready/gottlieb/joker-poker-1978.json").exists())

	def test_reproducible_definition_seed_knowledge_and_spatial_report(self):
		for path, expected in curator.artifacts().items():
			self.assertEqual(expected, (ROOT/path).read_bytes(), str(path))
		self.assertEqual((ROOT/curator.DEFINITION_PATH).read_bytes(), (ROOT/curator.SEED_PATH).read_bytes())
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT/excerpt["path"]).read_bytes()).hexdigest())
		self.assertEqual(False, next(x for x in self.definition["sources"] if x["id"] == curator.SCRIPT)["known_working"])

	def test_check_guards_reject_knowledge_drift_and_unreviewed_promotion(self):
		with tempfile.TemporaryDirectory() as text:
			root = Path(text)
			paths = set(curator.artifacts()) | {curator.KNOWLEDGE_SEED_PATH}
			paths |= {Path(e["path"]) for s in self.definition["sources"] for e in s.get("excerpts",[])}
			for path in paths:
				(root/path).parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(ROOT/path, root/path)
			with patch.object(curator, "check_external_evidence"):
				curator.check(root)
				(root/curator.KNOWLEDGE_PATH).write_bytes(b"drift")
				with self.assertRaisesRegex(RuntimeError,"artifact drift"):
					curator.check(root)
				shutil.copyfile(ROOT/curator.KNOWLEDGE_PATH, root/curator.KNOWLEDGE_PATH)
				ready = root/"machines/author-ready/gottlieb/joker-poker-1978.json"
				ready.parent.mkdir(parents=True)
				ready.write_text("{}",encoding="utf-8")
				with self.assertRaisesRegex(RuntimeError,"author-ready"):
					curator.check(root)

	def test_explicit_wrong_external_root_fails_instead_of_skipping(self):
		with tempfile.TemporaryDirectory() as text, patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": text}):
			with self.assertRaisesRegex(RuntimeError, "external evidence"):
				curator.check_external_evidence()

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX root not enabled")
	def test_retained_extraction_manifest_and_every_bound_object(self):
		curator.check_external_evidence()
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])/curator.VPX_RELATIVE
		manifest = load_json(root/"extracted/manifest.json")
		report = load_json(ROOT/curator.REPORT_PATH)
		self.assertEqual(report["evidence"]["vpx"]["file_count"], len(manifest["files"]))
		self.assertEqual(report["evidence"]["vpx"]["byte_count"], sum(x["size"] for x in manifest["files"]))
		script = (root/"extracted/script.vbs").read_text(encoding="windows-1252")
		self.assertIn('cGameName="jokrpokr"',script)
		self.assertIn('SolCallback(6)="dtjj.SolDropUp"',script)
		self.assertIn('N1=Controller.Lamp(17)',script)
		self.assertIn('If N1 Then dtkk.DropSol_On',script)
		import re
		mappings = {int(n): name.lower() for n,name in re.findall(r"(?im)^Set Lights\((\d+)\)\s*=\s*(\w+)",script)}
		self.assertEqual({n:f"l{n}" for n in (4,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,27,28)},mappings)
		for n,name in mappings.items():
			light = load_json(root/"extracted/gameitems"/f"Light.{name}.json")["Light"]
			self.assertFalse(light["show_bulb_mesh"], n)

	def test_system_1_profile_keeps_read_paths_and_physical_fitment_separate(self):
		profile = load_json(ROOT/"controllers/pinmame/gts1.json")
		groups = {x["id"]:x for x in profile["groups"]}
		self.assertEqual("pinmame.gts1",profile["id"])
		self.assertIn("46/56/66/76",groups[curator.SWITCH]["notes"])
		self.assertIn("1..44",groups[curator.LAMP]["notes"])
		self.assertIn("not proof of twelve fitted coils",groups[curator.SOLENOID]["notes"])


if __name__ == "__main__":
	unittest.main()
