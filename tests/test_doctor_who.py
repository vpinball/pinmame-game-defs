from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_doctor_who as curator  # noqa: E402
import doctor_who_runtime_evidence as evidence_tool  # noqa: E402
import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "doctor-who-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "doctor-who-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "doctor-who-1992.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "doctor-who-1992.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-fliptronic"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.doctor-who.1992"

DRIVER_IDS = {"dw_l2", "dw_d2", "dw_l1", "dw_d1", "dw_p5", "dw_p6"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 81, 83, 84, 85, 86, 87}
OPTO_ADDRESSES = {31, 32, 33, 71, 72, 73, 74, 75, 76, 77}
DW_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x7F, 0x01, 0x00, 0x00, 0x00)
SCRIPT_SHA256 = "6c31324ab557a70e4caa1920c6f4be3b96c4d97d7306bf96243584f80518e232"
LIBRARY_SHA256 = "deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c"
ROM_ARCHIVE_SHA256 = "9e0a1e1257ca595f06f1367d7f96773ceb12d20be43061a9630216a8f0c5a162"
RUNTIME_FILES = {
	"doctor-who-dw_l2-switch-edges.json": ("dw-switch-edges-optos", "switch-edges"),
	"doctor-who-dw_l2-solenoid-test.json": ("dw-solenoid-test", "solenoid-test"),
	"doctor-who-dw_l2-mini-playfield-test.json": ("dw-mini-playfield-test", "mini-playfield-test-exploratory"),
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class DoctorWhoTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.doctor-who.1992", machine["id"])
		self.assertEqual(738, machine["ipdb_id"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"dw_l2", "dw_d2", "dw_l1", "dw_d1"}, {key for key, value in compatibility.items() if value == "identical"})
		self.assertEqual({"dw_p5", "dw_p6"}, {key for key, value in compatibility.items() if value == "compatible"})
		self.assertIn("Dalek", next(driver for driver in self.definition["drivers"] if driver["id"] == "dw_p5")["variant_notes"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(len(self.switches), sum(1 for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"})
		self.assertEqual(set(range(1, 51)), set(self.coils))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gi))
		identifiers = [item["id"] for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		inverted = {number for number in MATRIX_ADDRESSES if (DW_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(OPTO_ADDRESSES | {81}, inverted)
		self.assertEqual(inverted, curator.MASKED_SWITCHES)
		self.assertEqual(OPTO_ADDRESSES, curator.OPTO_SWITCHES)
		for address in OPTO_ADDRESSES - {32}:
			switch = self.switches[address]
			self.assertTrue(switch["normally_closed"], address)
			self.assertIn("normally_closed is true", switch["physical"]["notes"], address)
			self.assertIn("runtime.doctor-who.switch-edges", switch["provenance"]["source_refs"], address)
		# 32 is the one opto the ROM reads as active at public 0, so its contact is open while the ROM reads it inactive.
		self.assertFalse(self.switches[32]["normally_closed"])
		self.assertIn("Mixed-level exception", self.switches[32]["physical"]["notes"])
		self.assertEqual({32}, curator.ROM_ACTIVE_AT_PUBLIC_ZERO)
		for address in (112, 114, 118, 111, 113, 117):
			self.assertFalse(self.switches[address]["normally_closed"], address)
		for address in range(1, 9):
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		for address in (22, 82):
			self.assertTrue(self.switches[address]["initial_active"], address)

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		for address, name in curator.T4_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {curator.T4_WIRES[address]}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual(curator.ROM_SWITCH_NAMES, {k: v for k, v in evidence_tool.EDGE_NAMES.items() if k in curator.ROM_SWITCH_NAMES})
		self.assertEqual(curator.T4_NAMES, evidence_tool.T4_NAMES)
		self.assertEqual(curator.T4_WIRES, evidence_tool.T4_WIRES)

	def test_output_kinds_and_availability(self) -> None:
		for address in (6, 8, 14, 17, 18, 19, 20, 21, 22, 23, 24):
			self.assertEqual("flasher", self.coils[address]["kind"], address)
		self.assertEqual("motor", self.coils[28]["kind"])
		self.assertEqual("control_signal", self.coils[27]["kind"])
		self.assertIn("direction", self.coils[27]["physical"]["notes"].casefold())
		for address in (29, 30, 31):
			self.assertEqual(("virtual", "used"), (self.coils[address]["kind"], self.coils[address]["availability"]), address)
		for address in (25, 26, 33, 34, 32, *range(37, 45), 50):
			self.assertEqual("unused", self.coils[address]["availability"], address)
		self.assertEqual("device.upper-left-flipper-power", self.coils[35]["id"])
		for address in (7, 8, 14):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
		for address in (23, 36, 48, 67, 71, 72, 82, 86):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
		self.assertEqual({0, 1}, {a for a, g in self.gi.items() if g["spatial"]["status"] == "not_applicable"})

	def test_mechanisms_reference_declared_devices_and_cover_the_levels(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		levels = {item["id"]: set(item["sensors"]) for item in mechanisms["mechanism.mini-playfield"]["positions"]}
		self.assertEqual(
			{"level-1": {f"switch.matrix-{a}" for a in (76, 77, 78)}, "level-2": {f"switch.matrix-{a}" for a in range(71, 76)}, "level-3": {f"switch.matrix-{a}" for a in (38, 68, 88)}},
			levels,
		)
		self.assertEqual(
			{self.coils[28]["id"], self.coils[27]["id"]}, set(mechanisms["mechanism.mini-playfield"]["actuators"]),
		)
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"]:
			cited.update(item["provenance"]["source_refs"])
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
			for placement in spatial.get("placements", []):
				cited.update(placement["provenance"]["source_refs"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		self.assertEqual(set(sources), cited | {source["id"] for source in self.definition["sources"] if source["id"] in {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.IDENTITY_SOURCE, curator.AMENDMENT_SOURCE}})
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("WebP", excerpt["image_derivation"])
		manual = sources[curator.MANUAL_SOURCE]
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")} - {"handy-technician-chart", "manual-amendment", "ipdb-page"}, {Path(item["path"]).stem for item in manual["excerpts"]})
		self.assertEqual(curator.MANUAL_SHA256, manual["sha256"])
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])
		self.assertEqual(curator.TABLE_SHA256, sources[curator.VPX_TABLE_SOURCE]["sha256"])

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				for value in (placement["x"], placement["y"]):
					self.assertLessEqual(len(f"{value:.10f}".rstrip("0").split(".")[1]), 6, placement["id"])
			quantity = item.get("physical", {}).get("quantity")
			if quantity is not None and item["kind"] in {"lamp", "flasher"}:
				# A quantity may exceed the placements (an insert-panel bulb is counted but not placed), never the reverse.
				self.assertGreaterEqual(quantity, len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		placements = drawing_callouts.placements_of(self.definition)
		decisions = drawing_callouts.evaluate(seed, placements, seed.get("limit", drawing_callouts.LIMIT))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		validated = {
			placement["id"]
			for item in self.definition["inputs"] + self.definition["outputs"]
			for placement in (item.get("spatial") or {}).get("placements", [])
			if placement["provenance"]["status"] == "validated"
		}
		self.assertEqual(agreeing, validated)
		self.assertTrue(all(curator.CALLOUT_SOURCE in self._placement(pid)["provenance"]["source_refs"] for pid in validated))
		# Measured placements stay observed and cite the manual's drawing, not the table.
		for pid in ("switch.matrix-32.sensor", "lamp.matrix-67.emitter", "device.mini-playfield-motor-on-off.effect", "device.mini-playfield-motor-direction.effect"):
			placement = self._placement(pid)
			self.assertEqual("observed", placement["provenance"]["status"], pid)
			self.assertIn(curator.MANUAL_SOURCE, placement["provenance"]["source_refs"], pid)
			self.assertNotIn(curator.VPX_TABLE_SOURCE, placement["provenance"]["source_refs"], pid)

	def _placement(self, placement_id: str) -> dict:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				if placement["id"] == placement_id:
					return placement
		raise AssertionError(placement_id)

	def test_flasher_20_has_two_measured_bulbs_and_the_quantity_is_the_printed_count(self) -> None:
		flasher = self.coils[20]
		self.assertEqual(2, flasher["physical"]["quantity"])
		self.assertEqual(4, self.coils[6]["physical"]["quantity"])
		placements = flasher["spatial"]["placements"]
		self.assertEqual(["device.jet-bumpers-doctor-5-flasher.emitter.1", "device.jet-bumpers-doctor-5-flasher.emitter.2"], [p["id"] for p in placements])
		for placement in placements:
			self.assertEqual("observed", placement["provenance"]["status"])
			self.assertEqual(0.0, placement["y"])
			self.assertNotIn(curator.VPX_TABLE_SOURCE, placement["provenance"]["source_refs"])
		self.assertIn("invisible rotated Flasher sprite", flasher["physical"]["notes"])
		self.assertNotIn("switch.matrix-46.sensor", load(curator.CALLOUT_SEED_PATH)["checks"])
		self.assertIn("cannot be followed", self.switches[46]["physical"]["notes"])

	def test_legacy_compatibility_aliases_are_preserved_by_binding(self) -> None:
		seed = load(curator.LEGACY_ALIAS_SEED_PATH)["aliases"]
		by_group = {"pinmame.input.switch": self.switches, "pinmame.output.lamp": self.lamps, "pinmame.output.solenoid": self.coils}
		self.assertEqual(set(by_group), set(seed))
		for group, entries in seed.items():
			for address, aliases in entries.items():
				present = {(a["namespace"], a["value"]) for a in by_group[group][int(address)]["aliases"]}
				self.assertLessEqual({tuple(a) for a in aliases}, present, (group, address))
		self.assertIn(("vpe-legacy.switch", "007"), {(a["namespace"], a["value"]) for a in self.switches[7]["aliases"]})
		self.assertIn(("vpe-legacy.switch", "s_up"), {(a["namespace"], a["value"]) for a in self.switches[7]["aliases"]})

	def test_gi_bulbs_cannot_be_validated_so_the_record_stays_partial(self) -> None:
		for address in (2, 3, 4):
			spatial = self.gi[address]["spatial"]
			self.assertEqual("observed", spatial["status"], address)
			self.assertTrue(all(p["provenance"]["status"] == "observed" for p in spatial["placements"]), address)
			self.assertNotIn("quantity", self.gi[address].get("physical", {}), address)
		report = load(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual([], report["without_placements"])
		self.assertEqual(0, len(report["placement_status"]["candidate"]))
		for gi_id in ("gi.string-3", "gi.string-4", "gi.string-5"):
			self.assertIn(gi_id, report["placement_status"]["observed"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("Time Expander mini-playfield", "is the exception", "Prototype hardware this definition does not declare", "spatial_placement"):
			self.assertTrue(phrase.casefold() in note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (scenario, _directory) in RUNTIME_FILES.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.doctor-who.1992"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			scenario_document = load(scenario_path)
			self.assertEqual("pinmame-harness-scenario", scenario_document["format"], filename)
			self.assertEqual(len(scenario_document["actions"]), raw["action_count"], filename)
		edges = load(RUNTIME_DIRECTORY / "doctor-who-dw_l2-switch-edges.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		self.assertTrue(texts["32 -> 0"].startswith("Mini. Home Opto"))
		self.assertTrue(texts["32 -> 1 again"].startswith("SWITCH EDGES"))
		for address in sorted(OPTO_ADDRESSES - {32}):
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		solenoids = load(RUNTIME_DIRECTORY / "doctor-who-dw_l2-solenoid-test.json")["runtime"]["observations"]
		self.assertEqual(
			list(evidence_tool.T4_ORDER),
			[item["transitioned_solenoid_addresses"][0] for item in solenoids["named_action_observations"]],
		)
		mini = load(RUNTIME_DIRECTORY / "doctor-who-dw_l2-mini-playfield-test.json")["runtime"]["observations"]
		self.assertEqual({4, 5, 17, 27, 28}, {address for item in mini["named_action_observations"] for address in item["transitioned_solenoid_addresses"]})

	def retained_run(self, filename: str) -> dict:
		"""Parse a retained raw run only after it matches the SHA-256 its compact evidence records.

		A stale local copy must fail as a named hash mismatch, not as a KeyError on a label or field the
		copy predates.
		"""
		directory = RUNTIME_FILES[filename][1]
		data = (Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "doctor-who-1992" / "harness" / directory / "dw_l2" / "run.json").read_bytes()
		expected = load(RUNTIME_DIRECTORY / filename)["runtime"]["raw_runs"][0]["sha256"]
		self.assertEqual(expected, hashlib.sha256(data).hexdigest(), f"retained {directory}/dw_l2/run.json does not match the SHA-256 {filename} records")
		return json.loads(data)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		# Hash every run before evidence_tool rebuilds from them, so a stale copy fails here by name.
		runs = {filename: self.retained_run(filename) for filename in RUNTIME_FILES}
		evidence_tool.check(root)
		for filename, (_scenario, directory) in RUNTIME_FILES.items():
			path = root / "doctor-who-1992" / "harness" / directory / "dw_l2"
			from build_external_evidence_manifest import check_manifest

			check_manifest(path, "dw_l2")
			run = runs[filename]
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(0, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_raw_runs_support_the_polarity_and_wiring_claims(self) -> None:
		edges = self.retained_run("doctor-who-dw_l2-switch-edges.json")
		for snapshot in edges["snapshots"]:
			if " -> " not in snapshot["label"]:
				continue
			address, state = (int(part.split()[0]) for part in snapshot["label"].split(" -> "))
			levels = {item["number"]: item["state"] for item in snapshot["watched_switches"]}
			self.assertEqual(state, levels[address], snapshot["label"])
		steps = {step["label"]: step for step in evidence_tool_steps(edges)}
		self.assertTrue({45, 46} & evidence_tool._risen(steps["112 -> 1"]))
		self.assertTrue({47, 48} & evidence_tool._risen(steps["114 -> 1"]))
		mini = self.retained_run("doctor-who-dw_l2-mini-playfield-test.json")
		steps = {step["label"]: step for step in evidence_tool_steps(mini)}
		self.assertEqual({28}, evidence_tool._risen(steps["114 -> 1 (left flipper button held)"]) & {27, 28})
		self.assertEqual({27, 28}, evidence_tool._risen(steps["T.14 sub-test 1 with both flipper buttons held, second 4"]) & {27, 28})
		self.assertEqual({4}, evidence_tool._risen(steps["T.14 sub-test 2, frame 1"]) & {4, 5})

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "doctor-who-1992" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		self.assertIn('Const cGameName = "dw_l2"', text)
		self.assertIn(".sol1=28", text)
		self.assertIn(".sol2=27", text)
		self.assertIn("Controller.Switch(32)", text)


def evidence_tool_steps(run: dict) -> list[dict]:
	return run["steps"]


if __name__ == "__main__":
	unittest.main()
