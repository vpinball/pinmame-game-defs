"""Xenon's physical contracts and reproducible evidence, separate from curator fixtures."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import drawing_callouts as callouts
from tools import curate_xenon
from pinmame_game_defs.jsonio import canonical_bytes
from pinmame_game_defs.spatial import _item_point, _round_point
from pinmame_game_defs.validation import validate_machine


def load(path):
	return json.loads(path.read_text(encoding="utf-8"))


class XenonDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.seed = curate_xenon.load_seed()
		cls.d = cls.seed["definition"]
		cls.report = cls.seed["spatial_report"]
		cls.sw = {d["binding"]["device"]: d for d in cls.d["inputs"] if d["binding"]["group"] == "pinmame.input.switch"}
		cls.co = {d["binding"]["device"]: d for d in cls.d["outputs"] if d["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {d["binding"]["device"]: d for d in cls.d["outputs"] if d["binding"]["group"] == "pinmame.output.lamp"}

	def test_identity_variants_and_canonical_bytes(self):
		self.assertEqual(("bally.xenon.1980", "1196", 2821), tuple(self.d["machine"][k] for k in ("id", "model_number", "ipdb_id")))
		self.assertEqual("physical_pinball", self.d["machine"]["kind"])
		self.assertEqual({"xenon", "xenonf", "xenona", "xenonfa"}, {d["id"] for d in self.d["drivers"]})
		self.assertTrue(all(d["physical_compatibility"] == "identical" for d in self.d["drivers"]))
		source_ids = {s["id"] for s in self.d["sources"]}
		self.assertIn("pinmame.games.xenon", source_ids)
		self.assertFalse(any(s.startswith("pinmame.driver.") for s in source_ids))
		self.assertEqual(canonical_bytes(self.d), (ROOT / "machines/partial/bally/xenon-1980.json").read_bytes())
		self.assertFalse((ROOT / "machines/author-ready/bally/xenon-1980.json").exists())
		self.assertEqual([], validate_machine(self.d))

	def test_complete_address_disposition_and_contact_construction(self):
		self.assertEqual(set(range(1, 49)) | set(range(81, 89)) | {-7, -6, -5}, set(self.sw))
		self.assertEqual(set(range(1, 16)) | set(range(17, 21)) | set(range(45, 49)), set(self.co))
		self.assertEqual({16*d+a for d in range(8) for a in range(1, 16)}, set(self.lamps))
		for n in [12, 13, 14, 15, *range(41, 49), 81, 83, 85, 86, 87, 88]:
			self.assertEqual("unused", self.sw[n]["availability"], n)
		for d in self.sw.values():
			if d["availability"] == "used": self.assertIs(d["normally_closed"], False)
		self.assertEqual(32, sum(d["kind"] == "dip_switch" for d in self.d["inputs"]))
		self.assertEqual(3, self.sw[7]["physical"]["quantity"])
		self.assertEqual(2, self.sw[16]["physical"]["quantity"])
		self.assertEqual(2, self.sw[26]["physical"]["quantity"])

	def test_service_numbers_are_separate_from_public_addresses(self):
		expected = {1: 7, 2: 6, 3: 8, 4: 9, 5: 14, 6: 15, 7: 10, 8: 11, 9: 12, 10: 13, 11: 1, 12: 2, 13: 3, 14: 4, 15: 5, 16: 18, 17: 19, 18: 17}
		for selector, address in expected.items():
			self.assertIn({"namespace": "manual.self-test", "value": f"{selector:02}"}, self.co[address]["aliases"])
		evidence = load(ROOT / "evidence/runtime/by35/xenon-1980.json")
		self.assertEqual({str(k): v for k, v in expected.items()}, evidence["runtime"]["observations"]["physical_service_solenoid_to_public"])
		self.assertEqual("used", self.co[17]["availability"])
		self.assertEqual("unused", self.co[20]["availability"])
		self.assertIn("power-up", self.co[20]["physical"]["notes"])
		for n in [45, 47]: self.assertEqual(("virtual", "used"), (self.co[n]["kind"], self.co[n]["availability"]))

	def test_drop_bank_and_two_ball_stack_are_distinct_physical_devices(self):
		mechanisms = {m["id"]: m for m in self.d["mechanisms"]}
		self.assertEqual({self.co[n]["id"] for n in range(1, 6)}, set(mechanisms["mech.four-drop-bank"]["actuators"]))
		self.assertEqual({self.sw[n]["id"] for n in [8, 2, 28]}, set(mechanisms["mech.release-stack"]["sensors"]))
		self.assertEqual([self.co[9]["id"]], mechanisms["mech.tube-exit-chamber"]["actuators"])
		self.assertEqual([self.co[17]["id"]], mechanisms["mech.top-saucer"]["actuators"])
		pairs = {(r["source"], r["destination"]) for r in self.d["relationships"] if r["id"].startswith("rel.reflex-")}
		self.assertEqual({(self.sw[s]["id"], self.co[c]["id"]) for s, c in [(35,15),(36,14),(37,13),(38,12),(39,11),(40,10)]}, pairs)
		self.assertIn("clears 20", self.sw[29]["physical"]["notes"])

	def test_lamp_fanout_and_auxiliary_decoder_order(self):
		self.assertEqual({1}, {n for n in range(1,64) if n in self.lamps and self.lamps[n]["availability"] == "unused"})
		self.assertEqual(26, sum(d["availability"] == "used" for n, d in self.lamps.items() if n > 64))
		for n in [15,31,47,63]:
			self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
			self.assertEqual(1, len(self.lamps[n]["spatial"]["placements"]))
		for n in [5,21,37,53,52,26]:
			self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
			self.assertEqual(2, len(self.lamps[n]["spatial"]["placements"]))
		for n in [13,27,29,43,45,61]: self.assertEqual("cabinet_or_service", self.lamps[n]["spatial"]["reason"])
		for n, pin in [(69,"A9J2-9"),(85,"A9J2-17"),(101,"A9J3-10")]:
			self.assertEqual("used", self.lamps[n]["availability"])
			self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
			self.assertEqual("observed", self.lamps[n]["provenance"]["status"])
			self.assertIn("repair.xenon-auxiliary", self.lamps[n]["provenance"]["source_refs"])
			self.assertEqual(pin, self.lamps[n]["wiring"]["drive_connection"])
			self.assertNotIn("spatial", self.lamps[n])
		for n in [71,73,79,117,127]:self.assertEqual("unused", self.lamps[n]["availability"])
		for n in [72,88,104,120]:
			d = self.lamps[n]
			self.assertEqual(("virtual", "unknown", "observed"), (d["kind"], d["availability"], d["provenance"]["status"]))
			self.assertIn("runtime.xenon", d["provenance"]["source_refs"])
			self.assertIn("no resistor/SCR/load branch", d["physical"]["notes"])
			self.assertEqual(("not_applicable", "virtual", "validated"), (d["spatial"]["status"], d["spatial"]["reason"], d["spatial"]["provenance"]["status"]))
		self.assertEqual("4 RING CIRCLE", self.lamps[86]["label"])
		self.assertEqual("END OF TUBE", self.lamps[85]["label"])

	def test_unfitted_main_lamp_keeps_physical_disposition_with_runtime_explanation(self):
		lamp = self.lamps[1]
		self.assertEqual(("lamp", "unused", "validated"), (lamp["kind"], lamp["availability"], lamp["provenance"]["status"]))
		self.assertEqual("unused", lamp["spatial"]["reason"])
		self.assertTrue({"runtime.xenon", "pinmame.core-common.xenon"} <= set(lamp["provenance"]["source_refs"]))
		for text in ["regardless of physical fitment", "startup pulse", "service sequence", "not established"]:
			self.assertIn(text, lamp["physical"]["notes"])
		self.assertNotIn("sweep", lamp["physical"]["notes"])

	def test_tube_is_ten_actual_bulbs_not_glow_centers(self):
		tube = {10,14,30,46,62}
		maps = [m for m in self.report["placements"] if m["device_id"] in {self.lamps[n]["id"] for n in tube}]
		self.assertEqual({"Primitive1", *{f"Primitive{n}" for n in range(84,93)}}, {m["object"] for m in maps})
		self.assertEqual(10, len(maps))
		for n in tube:
			self.assertEqual("lamp", self.lamps[n]["kind"])
			self.assertEqual(2, self.lamps[n]["physical"]["quantity"])
			self.assertEqual("observed", self.lamps[n]["spatial"]["status"])

	def test_drawing_checks_recompute_and_fail_closed(self):
		seed = load(ROOT / "tools/seeds/bally/xenon-1980-callouts.json")
		decisions = callouts.evaluate(seed, callouts.placements_of(self.d))
		self.assertEqual(self.report["callout_decisions"], decisions)
		self.assertEqual(39, len(decisions["placements"]))
		self.assertEqual(38, sum(d["agrees"] for d in decisions["placements"].values()))
		for coll in ["inputs", "outputs"]:
			for d in self.d[coll]:
				for p in d.get("spatial", {}).get("placements", []):
					if p["id"] in decisions["placements"]:
						self.assertEqual("validated" if decisions["placements"][p["id"]]["agrees"] else "observed", p["provenance"]["status"])
		bad = json.loads(json.dumps(seed))
		for read in bad["pages"]["figure-v-switches"]["reads"]:
			if read["label"] == "40": read["pixel"] = [1500,2100]
		changed = callouts.evaluate(bad, callouts.placements_of(self.d))
		pid = self.sw[40]["spatial"]["placements"][0]["id"]
		self.assertFalse(changed["placements"][pid]["agrees"])

	def test_promotion_gate_and_uncontrolled_gi_remain_honest(self):
		self.assertEqual("partial", self.d["coverage"]["status"])
		self.assertEqual({"output_semantics", "spatial_placement"}, set(self.d["coverage"]["missing"]))
		self.assertEqual([], self.d["conflicts"])
		self.assertTrue(all(d["binding"]["group"] != "pinmame.output.gi" for d in self.d["outputs"]))
		gi = self.report["uncontrolled_lighting"]
		self.assertEqual(19, len(gi["modeled_playfield_bulb_candidates"]))
		self.assertTrue(all(c["quantity"] == "unknown" for c in gi["physical_circuits"]))
		self.assertEqual([7,7,7,7,2,2], [d["width"] for d in self.d["displays"]])
		self.assertEqual([1,9,17,25,35,38], [d["segment_start"] for d in self.d["displays"]])
		self.assertIn("OPDB `G42Pk-MZe2e`", self.seed["knowledge_note"])
		self.assertIn("AS-2518-60", self.seed["knowledge_note"])
		self.assertTrue(any(set(b["devices"]) == {self.lamps[n]["id"] for n in [72,88,104,120]} and b["dimension"] == "output_semantics" for b in self.report["blockers"]))

	def test_diagnostics_document_their_separate_driver_paths(self):
		for n, path in [(-7, "PIA0 CA1"), (-6, "CPU 0 NMI"), (-5, "sndbrd_0_diag")]:
			note = self.sw[n]["physical"]["notes"]
			self.assertIn(path, note)
			self.assertNotIn("Factory five-column matrix", note)

	def test_excerpts_sources_and_raw_normalization(self):
		for s in self.d["sources"]:
			for e in s.get("excerpts", []):
				for path, digest in [("path","sha256"),("image","image_sha256")]:
					if path in e:self.assertEqual(e[digest], hashlib.sha256((ROOT / e[path]).read_bytes()).hexdigest(), e[path])
		points = callouts.placements_of(self.d)
		for m in self.report["placements"]:
			self.assertEqual((_round_point(m["raw_x"]/952),_round_point(m["raw_y"]/1974)), points[m["placement_id"]])


class XenonRetainedEvidenceTests(unittest.TestCase):
	def retained_session(self):
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("optional evidence roots not configured")
		return Path(root) / "bally.xenon.1980/session-20261106"

	def test_main_lamp_startup_and_service_observations_recompute_from_raw_runs(self):
		session = self.retained_session()
		excerpt = (ROOT / "evidence/excerpts/bally.xenon.1980/runtime-observations.md").read_text(encoding="utf-8")
		for name, count in [("selftest",10), ("aux",2), ("play2",2)]:
			run = load(session / f"{name}-run.json")
			events = [e for e in run["events"] if e["event"] == "lamp" and e["number"] == 1]
			self.assertEqual(count, len(events), name)
			self.assertEqual([1,0] * (count // 2), [e["state"] for e in events])
			self.assertIn(f'{events[0]["time_s"]:.6f}-{events[1]["time_s"]:.6f}', excerpt)
			if name == "selftest":
				self.assertIn(f'from {events[2]["time_s"]:.6f} to {events[-1]["time_s"]:.6f}', excerpt)
				self.assertTrue(all(25 < e["time_s"] < 29 for e in events[2:]))
			else:
				self.assertFalse(any(1 in s["active_lamps"] for s in run["snapshots"] if s["label"] != "booted"))
				self.assertLess(events[-1]["time_s"], 5)

	def test_unfitted_output7_state_is_not_only_a_lamp_test_sweep(self):
		session = self.retained_session()
		active = {72,88,104,120}
		padding = {65+16*d+a for d in range(4) for a in range(8,15)}
		for name, count in [("selftest",5), ("aux",22), ("play2",30)]:
			run = load(session / f"{name}-run.json")
			snapshots = [s for s in run["snapshots"] if s["label"] != "booted"]
			self.assertEqual(count, len(snapshots))
			for snapshot in snapshots:
				self.assertTrue(active <= set(snapshot["active_lamps"]), (name,snapshot["label"]))
				self.assertFalse(padding & set(snapshot["active_lamps"]))
			for n in active:
				events = [e for e in run["events"] if e["event"] == "lamp" and e["number"] == n]
				self.assertEqual(7 if n == 72 else 1, len(events), (name,n))
				self.assertEqual(1, events[-1]["state"])
				self.assertTrue(8 < events[0]["time_s"] < 9)
			self.assertFalse(any(e["event"] == "lamp" and e["number"] in padding for e in run["events"]))

	def test_tube_coordinates_recompute_from_world_mesh_vertices(self):
		session = self.retained_session()
		mappings = [m for m in curate_xenon.load_seed()["spatial_report"]["placements"] if m["file"].endswith(".obj")]
		vertices = {m["object"]: [] for m in mappings}
		current = None
		with (session / "table-obj/Xenon (Bally 1980) v2.5.2.obj").open(encoding="utf-8") as stream:
			for line in stream:
				if line.startswith("o "):
					current = line[2:].strip()
				elif line.startswith("v ") and current in vertices:
					vertices[current].append(tuple(map(float, line.split()[1:3])))
		self.assertEqual(10, len(mappings))
		for m in mappings:
			points = vertices[m["object"]]
			self.assertTrue(points, m["object"])
			center = tuple((min(p[i] for p in points) + max(p[i] for p in points))/2 for i in range(2))
			self.assertEqual((m["raw_x"], m["raw_y"]), center, m["object"])

	def test_service_and_gameplay_mappings_recompute_from_raw_runs(self):
		session = self.retained_session()
		service = load(session / "selftest-run.json")
		digits = {0x3f: "0", 0x06: "1", 0x5b: "2", 0x4f: "3", 0x66: "4", 0x6d: "5", 0x7d: "6", 0x07: "7", 0x7f: "8", 0x6f: "9"}
		displays = [e for e in service["events"] if "segments" in e and e.get("index") == 0 and all((v & 127) in digits for v in e["segments"][-2:])]
		observed = {}
		for event in service["events"]:
			if event["event"] != "solenoid" or event["state"] != 1 or event["time_s"] < 28:
				continue
			near = [d for d in displays if event["time_s"] <= d["time_s"] < event["time_s"] + .5]
			if not near:
				continue
			nearest = min(near, key=lambda d: d["time_s"])
			selector = int("".join(digits[v & 127] for v in nearest["segments"][-2:]))
			observed.setdefault(str(selector), set()).add(event["number"])
		compact = load(ROOT / "evidence/runtime/by35/xenon-1980.json")["runtime"]["observations"]
		self.assertEqual({k: {v} for k, v in compact["physical_service_solenoid_to_public"].items()}, observed)
		play = load(session / "play2-run.json")
		steps = {s["label"]: s["transitions"]["solenoids"] for s in play["steps"]}
		for switch, coil in [(35,15), (36,14), (37,13), (38,12), (39,11), (40,10), (20,2)]:
			self.assertEqual([coil], [e["number"] for e in steps[f"isolated playfield switch {switch}"] if 1 in e["states"]])
		self.assertEqual([], steps["no-change control"])
		for label, coil in [("drop switch 24 held down",1), ("top saucer first entry",17), ("exit chamber entry before lock qualified",9)]:
			self.assertIn(coil, [e["number"] for e in steps[label] if 1 in e["states"]])
		self.assertEqual([{"number":19,"states":[0]}], steps["tilt drops flipper relay"])
		for key, runs, event in [("solenoid_addresses_seen", [service,play], "solenoid"), ("lamp_addresses_seen", [service], "lamp"), ("lamp_addresses_driven_outside_self_test", [play], "lamp")]:
			self.assertEqual(compact[key], sorted({e["number"] for run in runs for e in run["events"] if e["event"] == event}))

	def test_all_retained_artifacts_and_both_manifests(self):
		if not os.environ.get("PINMAME_VPX_SOURCES_ROOT"):self.skipTest("optional evidence roots not configured")
		seed = curate_xenon.load_seed()
		curate_xenon.verify_evidence(seed, required=True)
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "bally/xenon-1980/extracted-v2.5.2"
		for m in seed["spatial_report"]["placements"]:
			if not m["file"].startswith("gameitems/"):continue
			kind, data = next(iter(load(root / m["file"]).items()))
			x,y,_ = _item_point(kind.lower(),data)
			self.assertEqual((x,y),(m["raw_x"],m["raw_y"]),m["object"])
		callouts.verify_retained(load(ROOT / "tools/seeds/bally/xenon-1980-callouts.json"), ROOT, Path(os.environ["PINMAME_MANUALS_ROOT"]), Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))
		checkout = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).parent / "source-checkouts/pinmame-46e1a01a/src/wpc"
		for s in seed["definition"]["sources"]:
			if s["id"] in {"pinmame.games.xenon","pinmame.core.xenon","pinmame.core-common.xenon"}:
				self.assertEqual(s["sha256"], hashlib.sha256((checkout / s["uri"].rsplit("/",1)[1]).read_bytes()).hexdigest())


if __name__ == "__main__": unittest.main()
