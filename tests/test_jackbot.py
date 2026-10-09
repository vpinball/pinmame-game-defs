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
sys.path.insert(0, str(ROOT / "src"))

import curate_jackbot as curator  # noqa: E402
import drawing_callouts  # noqa: E402
import jackbot_runtime_evidence as evidence_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "jackbot-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "jackbot-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "jackbot-1995.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "jackbot-1995.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-95"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "williams.jackbot.1995"

DRIVER_IDS = {"jb_10r", "jb_101r", "jb_10b", "jb_101b", "jb_04a"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = set(range(71, 79)) | set(range(81, 89))
# src/wpc/sims/wpc/prelim/jb.c jbGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
JB_INVERTED_SWITCH_MASK = (0x00, 0xE0, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
SCRIPT_SHA256 = "8edd32cea57460f1d76b864e39b742bb3bc77c0c201816a72094e4476c516c8b"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "182acb5047d5ccfd0a795a8c705d375856a4ae7fd134bf9595523f323b8a4238"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class JackBotTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["id"]: item for item in cls.definition["outputs"]}
		cls.switches = {item["binding"]["device"]: item for item in cls.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		cls.coils = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.gi = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.gi"}

	def _placement(self, placement_id: str) -> dict:
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				if placement["id"] == placement_id:
					return placement
		raise AssertionError(placement_id)

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("williams.jackbot.1995", 3619, 1995, "GRKOX-MLyrW"), (machine["id"], machine["ipdb_id"], machine["year"], machine["opdb_id"]))
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		# jbGameData declares GEN_WPC95DCS, PINMAME_HARDWARE_GEN_WPC95DCS = 0x40 in libpinmame.h.
		self.assertEqual("0x40", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"jb_10r": "identical", "jb_101r": "identical", "jb_10b": "identical", "jb_101b": "identical", "jb_04a": "unknown"}, compatibility)
		self.assertIn("WPC-S 5-Board", next(d for d in self.definition["drivers"] if d["id"] == "jb_04a")["variant_notes"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["variant_differences", "spatial_placement"], self.definition["coverage"]["missing"])
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
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual({2, 32, 50} | set(range(33, 45)), {a for a, c in self.coils.items() if c["availability"] == "unused"})
		self.assertEqual(("virtual", "used", ["internal.simulator-ball-shooter"]), (self.coils[49]["kind"], self.coils[49]["availability"], self.coils[49]["roles"]))

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (JB_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual({16, 17, 18, 31, 32, 33, 34, 35}, inverted)
		self.assertEqual(inverted, curator.MASKED_SWITCHES)
		self.assertEqual(inverted, set(evidence_tool.PINMAME_MASKED))
		for address in inverted:
			self.assertTrue(self.switches[address]["normally_closed"], address)
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
			self.assertIn("runtime.jackbot.switch-edges-sweep", self.switches[address]["provenance"]["source_refs"], address)
		# The visor targets are shaded on the matrix page, but the mask leaves them alone and the ROM reads them active at 1.
		for address in (41, 42, 43, 44, 45):
			self.assertFalse(self.switches[address]["normally_closed"], address)
			self.assertIn("rests open and normally_closed is false", self.switches[address]["physical"]["notes"], address)
		for address in set(self.switches) - inverted - {24} - UNUSED_MATRIX_ADDRESSES:
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])
		self.assertEqual({16, 17, 18, 41, 42, 43, 44, 45, 112, 114, 116, 118}, set(curator.SHADED_SWITCHES))

	def test_the_visor_switches_and_the_upper_flipper_optos(self) -> None:
		for address, name in ((115, "Visor Closed"), (117, "Visor Open")):
			switch = self.switches[address]
			self.assertEqual((name, "used", False), (switch["label"], switch["availability"], switch["normally_closed"]))
			self.assertNotIn("roles", switch)
			self.assertIn("runtime.jackbot.visor-test", switch["provenance"]["source_refs"])
			self.assertIn("stops the visor motor (28)", switch["physical"]["notes"])
		for upper, lower, side in ((116, 112, "right"), (118, 114, "left")):
			self.assertEqual("used", self.switches[upper]["availability"])
			self.assertEqual(self.switches[lower]["roles"], self.switches[upper]["roles"])
			self.assertEqual([f"flipper.lower.{side}.button"], self.switches[upper]["roles"])
			self.assertIn("NOT USED", self.switches[upper]["physical"]["notes"])
			self.assertIn("fire the lower", self.switches[upper]["physical"]["notes"])
		for address in (112, 116):
			self.assertIn("Page 3-14's pin list for the right Flipper Opto Board", self.switches[address]["physical"]["notes"], address)
		for address in (111, 113):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"])
		self.assertEqual({112: {45, 46}, 114: {47, 48}, 116: {45, 46}, 118: {47, 48}}, {a: set(v) for a, v in curator.FLIPPER_FIRES.items()})
		self.assertEqual(curator.FLIPPER_FIRES, {a: frozenset(v) for a, v in evidence_tool.FLIPPER_FIRES.items()})

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual(curator.ROM_SWITCH_NAMES, evidence_tool.EDGE_NAMES)
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES}, evidence_tool.T4_NAMES)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual(set(evidence_tool.T4_ORDER), set(curator.T4_ADDRESSES))
		self.assertEqual(set(evidence_tool.T5_ORDER), set(curator.T5_ADDRESSES))
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})
		self.assertEqual(curator.ROM_LAMP_NAMES, evidence_tool.LAMP_NAMES)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f'prints "{name}"', self.lamps[address]["physical"]["notes"], address)

	def test_bonus_lamps_follow_the_rom_and_the_table_against_the_manual(self) -> None:
		self.assertEqual({27: "Bonus 2X", 47: "Bonus 3X", 28: "Bonus 4X", 38: "Bonus 5X"}, {a: self.lamps[a]["label"] for a in (27, 28, 38, 47)})
		for address, (matrix, listed) in curator.LAMP_MANUAL_MISPRINTS.items():
			notes = self.lamps[address]["physical"]["notes"]
			self.assertIn(f"prints this cell '{matrix}'", notes, address)
			self.assertEqual("validated", self.lamps[address]["spatial"]["placements"][0]["provenance"]["status"], address)
		# The printed cells stay literal in the excerpts.
		matrix = (EXCERPT_DIRECTORY / "lamp-matrix.md").read_text(encoding="utf-8")
		for cell in ("28 BONUS 3X", "38 BONUS 4X", "47 BONUS 5X"):
			self.assertIn(cell, matrix)
		for address in (71, 73, 74):
			self.assertIn(curator.LAMP_LIST_MISPRINTS[address], self.lamps[address]["physical"]["notes"], address)

	def test_output_kinds_and_unfitted_positions(self) -> None:
		self.assertEqual(set(range(15, 28)), {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual("motor", self.coils[28]["kind"])
		for address in (41, 42, 43, 44):
			self.assertEqual(("virtual", "unused", ["internal.duplicate.lpdc-mirror"]), (self.coils[address]["kind"], self.coils[address]["availability"], self.coils[address]["roles"]), address)
		for address in (33, 34, 35, 36):
			self.assertEqual(("coil", "unused"), (self.coils[address]["kind"], self.coils[address]["availability"]), address)
			self.assertIn("FLIP_SOL(FLIP_L)", self.coils[address]["physical"]["notes"])
		self.assertEqual({45: "29", 46: "30", 47: "31", 48: "32"}, {a: next(x["value"] for x in self.coils[a]["aliases"] if x["namespace"] == "manual.address") for a in (45, 46, 47, 48)})
		self.assertEqual(("not_applicable", ["cabinet.knocker"]), (self.coils[7]["spatial"]["status"], self.coils[7]["roles"]))
		for address in (15, 16):
			self.assertEqual(2, self.coils[address]["physical"]["quantity"], address)
		# Parts page 2-17 and the factory parts list print the trough A-19963; the locations list's A-19663 stays in the note.
		self.assertEqual("A-19963", self.coils[1]["physical"]["assembly_part_number"])
		self.assertIn("prints A-19663", self.coils[1]["physical"]["notes"])
		for address in (33, 34, 45, 46):
			self.assertIn("Page 3-12's right flipper circuit", self.coils[address]["physical"]["notes"], address)
		for address in (35, 36, 47, 48):
			self.assertNotIn("Page 3-12's right flipper circuit", self.coils[address]["physical"]["notes"], address)
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
		self.assertEqual(["cabinet.buy-in"], self.switches[23]["roles"])
		self.assertEqual(["cabinet.buy-in"], self.lamps[87]["roles"])
		for address, coil in self.coils.items():
			if coil["availability"] == "used" and coil["kind"] != "virtual":
				self.assertNotIn("'NOT USED'", coil["physical"]["notes"], address)

	def test_gi_strings_all_dim_and_the_insert_string_is_not_placed(self) -> None:
		for address in range(5):
			self.assertIn(f"steps the brightness of public GI {address} alone", self.gi[address]["physical"]["notes"], address)
			self.assertIn("J120 pins 'G.I. to insert panel'", self.gi[address]["physical"]["notes"], address)
		for address in range(4):
			self.assertEqual("observed", self.gi[address]["spatial"]["status"], address)
		self.assertEqual(("not_applicable", "backbox"), (self.gi[4]["spatial"]["status"], self.gi[4]["physical"]["location"]))

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
		visor = mechanisms["mechanism.visor"]
		self.assertEqual(self.coils[28]["id"], visor["actuators"][0])
		self.assertEqual([["switch.generic-115"], ["switch.generic-117"]], [p["sensors"] for p in visor["positions"]])
		ramp = mechanisms["mechanism.lifting-ramp"]
		self.assertEqual([self.coils[6]["id"], self.coils[14]["id"]], ramp["actuators"])
		self.assertEqual(["switch.matrix-15"], ramp["positions"][0]["sensors"])
		self.assertEqual([], self.definition["relationships"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
			spatial = item.get("spatial") or {}
			cited.update(spatial.get("provenance", {}).get("source_refs", []))
			for placement in spatial.get("placements", []):
				cited.update(placement["provenance"]["source_refs"])
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertLessEqual(cited, set(sources))
		uncited = {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.IDENTITY_SOURCE, curator.BULLETIN_SOURCE}
		self.assertEqual(set(sources), cited | uncited)
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("native resolution", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.webp")}, {"switch-locations", "lamp-locations", "solenoid-flashlamp-locations"})
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])
		for path in EXCERPT_DIRECTORY.glob("*.md"):
			self.assertNotIn(b"\r", path.read_bytes(), path.name)

	def test_placements_are_in_range_unique_and_quantities_align(self) -> None:
		ids = []
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
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
				self.assertGreaterEqual(quantity, len(spatial["placements"]), item["id"])
		self.assertEqual(len(ids), len(set(ids)))
		report = load(SPATIAL_REPORT_PATH)
		self.assertEqual([], report["without_placements"])

	def test_seed_coordinates_match_the_retained_bindings(self) -> None:
		# Every table placement is the normalized coordinate of its named object; the trough optos share the BallRelease kicker.
		seed = load(curator.SPATIAL_SEED_PATH)
		self.assertEqual({"width": 952.0, "height": 1974.0, "units": "vpx"}, seed["table"])
		trough = {tuple((entry["x"], entry["y"])) for address in (31, 32, 33, 34, 35) for entry in seed["switch"][str(address)]}
		self.assertEqual(1, len(trough))
		self.assertEqual(seed["solenoid"]["1"][0]["object"], "BallRelease")
		self.assertEqual({(entry["x"], entry["y"]) for entry in seed["solenoid"]["1"]}, trough)
		for address in (11, 12, 15, 66, 115, 117):
			self.assertTrue(seed["switch"][str(address)][0]["measured"], address)

	def test_drawing_callout_check_decides_every_placement_status(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		decisions = drawing_callouts.evaluate(seed, drawing_callouts.placements_of(self.definition), seed.get("limit", drawing_callouts.LIMIT))
		agreeing = {pid for pid, decision in decisions["placements"].items() if decision["agrees"]}
		validated = {
			placement["id"]
			for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]
			for placement in (item.get("spatial") or {}).get("placements", [])
			if placement["provenance"]["status"] == "validated"
		}
		self.assertEqual(agreeing, validated)
		self.assertGreaterEqual(len(validated), 70)
		self.assertEqual(
			{"lamp.matrix-67.emitter", "lamp.matrix-75.emitter", "lamp.matrix-76.emitter", "lamp.matrix-85.emitter", "switch.matrix-36.sensor"},
			set(decisions["placements"]) - agreeing,
		)
		for key, page in seed["pages"].items():
			self.assertEqual(5, len(page["controls"]), key)
			self.assertLessEqual(decisions["pages"][key]["control_loo_max"], 0.02, key)
			self.assertFalse(any(read["region"] == "inset" for read in page["reads"]), key)
		for pid in seed["measurements"]:
			placement = self._placement(pid)
			self.assertEqual(drawing_callouts.measured(seed, pid), (placement["x"], placement["y"]), pid)
			self.assertEqual("observed", placement["provenance"]["status"], pid)
			self.assertEqual([curator.MANUAL_SOURCE, curator.CALLOUT_SOURCE], placement["provenance"]["source_refs"], pid)
			self.assertNotIn(pid, seed["checks"])
		self.assertEqual(12, len(seed["measurements"]))
		# The visor switches sit on the motor bracket at the top centre, closed (F5) left of open (F7) as drawn.
		closed, opened = self._placement("switch.generic-115.sensor"), self._placement("switch.generic-117.sensor")
		self.assertLess(closed["x"], opened["x"])
		self.assertLess(max(closed["y"], opened["y"]), 0.1)

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Three catalog driver ids are ordinary words in this record's prose: "robot" (the robot theme), "vortex" (the Vortex holes)
		# and "break" (a Python statement in the evidence tool).
		ordinary_words = {"robot", "vortex", "break"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"williams.jackbot.1995"}
		)
		self.assertIn("nbaf_31", forbidden)
		self.assertIn("bally.nba-fastbreak.1997", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_jackbot.py", ROOT / "tools" / "jackbot_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "williams").glob("jackbot-1995*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted((ROOT / "tools" / "harness-scenarios" / "wpc-95").glob("jb-*.json")),
		]
		found_any = {}
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			if found:
				found_any[path.name] = found
			self.assertNotIn("NBA Fastbreak", text, path.name)
			self.assertNotIn("nbafGameData", text, path.name)
		self.assertEqual({}, found_any)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("visor", "lifting ramp", "WPC Security", "GEN_WPC95DCS", "spatial_placement", "never invert 16-18 or 31-35 again", "BONUS 3X"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (_directory, scenario, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-95" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["williams.jackbot.1995"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn("--handle-mechanics 0 ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id, name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "jackbot-jb_10r-switch-edges-sweep.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		self.assertTrue(texts["115 -> 1"].startswith("VISOR IS CLOSED"))
		self.assertTrue(texts["117 -> 1"].startswith("VISOR IS OPEN"))
		visor = load(RUNTIME_DIRECTORY / "jackbot-jb_10r-visor-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[28]] * 4, [item["transitioned_solenoid_addresses"] for item in visor])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _scenario, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, "jb_10r")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(0, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_retained_callout_artifacts_match_the_seed(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		checked = drawing_callouts.verify_retained(seed, ROOT, None, Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))
		self.assertGreater(checked, 3)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX sources root is not configured")
	def test_the_retained_extraction_matches_its_pinned_manifest(self) -> None:
		curator.verify_extraction_manifest(Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]))

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX sources root is not configured")
	def test_every_table_coordinate_recomputes_from_the_retained_gameitems(self) -> None:
		"""Each table-derived seed coordinate is its object's own point: a light, kicker, bumper or flipper centre, a hit
		target's position, a trigger's or wall's drag-point centroid, or a baked primitive's mesh bounding-box centre."""
		gameitems = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		by_name = {path.stem.split(".", 1)[1].lower(): path for path in gameitems.glob("*.json")}

		def point(name: str) -> tuple[float, float]:
			path = by_name[name.lower()]
			kind = path.stem.split(".")[0]
			data = json.loads(path.read_text(encoding="utf-8"))[kind]
			if kind in {"Trigger", "Wall"}:
				vertices = [item.get("vertex", item) for item in data["drag_points"]]
				return sum(v["x"] for v in vertices) / len(vertices), sum(v["y"] for v in vertices) / len(vertices)
			if kind == "Primitive":
				# Baked meshes: world = mesh vertex * size + position, with no rotation or translation (checked here).
				self.assertEqual([0.0] * 9, data["rot_and_tra"], name)
				vertices = [[float(value) for value in line.split()[1:3]] for line in path.with_suffix(".obj").read_text(encoding="utf-8").splitlines() if line.startswith("v ")]
				xs, ys = [v[0] for v in vertices], [v[1] for v in vertices]
				return (
					(min(xs) + max(xs)) / 2 * data["size"]["x"] + data["position"]["x"],
					(min(ys) + max(ys)) / 2 * data["size"]["y"] + data["position"]["y"],
				)
			if kind == "HitTarget":
				return data["position"]["x"], data["position"]["y"]
			return data["center"]["x"], data["center"]["y"]

		def normalized(x: float, y: float) -> tuple[float, float]:
			return round(x / curator.PLAYFIELD_WIDTH, 6), round(y / curator.PLAYFIELD_HEIGHT, 6)

		seed = load(curator.SPATIAL_SEED_PATH)
		checked = 0
		for category in ("switch", "solenoid", "lamp", "gi"):
			for address, entries in seed[category].items():
				for entry in entries:
					if entry.get("measured"):
						continue
					expected = normalized(*point(entry["object"]))
					self.assertAlmostEqual(expected[0], entry["x"], delta=2e-6, msg=(category, address, entry["object"]))
					self.assertAlmostEqual(expected[1], entry["y"], delta=2e-6, msg=(category, address, entry["object"]))
					checked += 1
		self.assertGreaterEqual(checked, 150)
