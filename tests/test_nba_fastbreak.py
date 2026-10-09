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

import curate_nba_fastbreak as curator  # noqa: E402
import drawing_callouts  # noqa: E402
import nba_fastbreak_runtime_evidence as evidence_tool  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "nba-fastbreak-1997.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "nba-fastbreak-1997.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "nba-fastbreak-1997.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "nba-fastbreak-1997.json"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-95"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.nba-fastbreak.1997"

DRIVER_IDS = {"nbaf_31", "nbaf_11", "nbaf_11a", "nbaf_11s", "nbaf_115", "nbaf_21", "nbaf_22", "nbaf_23"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = set(range(71, 79)) | set(range(81, 89))
# src/wpc/sims/wpc/full/nbaf.c nbafGameData inverted switches: Coin, columns 1-8, 9, 10, Cab., Cust.
NBAF_INVERTED_SWITCH_MASK = (0x00, 0x00, 0x00, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10)
SCRIPT_SHA256 = "69537260b7bc976a136a8ea1a4bd63ce7e0c09f81c766eafcbb765e9cb0b1a31"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "d5fd2c89752419a77d84965ac4cbe05d42d5c373337241cc0265b403e3bfc2fa"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class NbaFastbreakTests(unittest.TestCase):
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
		self.assertEqual(("bally.nba-fastbreak.1997", 4023, 1997), (machine["id"], machine["ipdb_id"], machine["year"]))
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			if driver["id"] in {"nbaf_21", "nbaf_22", "nbaf_23", "nbaf_31"}:
				self.assertIn("Linking Kit 58030", driver["variant_notes"], driver["id"])
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
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual({2, 21, 23, 32, 49, 50}, {a for a, c in self.coils.items() if c["availability"] == "unused"})

	def test_inverted_switch_mask_arithmetic_and_polarity(self) -> None:
		candidates = MATRIX_ADDRESSES | set(range(111, 119))
		inverted = {number for number in candidates if (NBAF_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual({31, 32, 33, 34, 35, 36, 37, 115}, inverted)
		self.assertEqual(inverted, curator.MASKED_SWITCHES)
		for address in inverted:
			self.assertTrue(self.switches[address]["normally_closed"], address)
			self.assertIn("runtime.nba-fastbreak.switch-edges-sweep", self.switches[address]["provenance"]["source_refs"], address)
		# The defender optos are shaded optos the mask leaves alone and the ROM reads active at public 1: contacts rest open.
		for address in (51, 52, 53, 54, 55):
			self.assertFalse(self.switches[address]["normally_closed"], address)
			self.assertIn("printed legend marks opto construction", self.switches[address]["physical"]["notes"], address)
		for address in set(self.switches) - inverted - {24} - UNUSED_MATRIX_ADDRESSES:
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])
		self.assertEqual(curator.SHADED_SWITCHES - {112, 114, 116, 118}, curator.OPTO_SWITCHES)

	def test_the_upper_flipper_optos_are_second_optos_of_the_lower_buttons(self) -> None:
		for upper, lower, side in ((116, 112, "right"), (118, 114, "left")):
			self.assertEqual("used", self.switches[upper]["availability"])
			self.assertEqual(self.switches[lower]["roles"], self.switches[upper]["roles"])
			self.assertEqual([f"flipper.lower.{side}.button"], self.switches[upper]["roles"])
			self.assertIn("rebuts a 'NOT USED' row", self.switches[upper]["physical"]["notes"])
		for address in (111, 113):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])
			self.assertIn("read back 0", self.switches[address]["physical"]["notes"])

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			if address == 24 or address > 100:
				continue
			self.assertIn(f'The ROM names it "{name}"', self.switches[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SWITCH_NAMES.items() if k < 100}, evidence_tool.EDGE_NAMES)
		for address, (name, wires) in curator.ROM_SOLENOID_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {wires}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T4_NAMES and k != 41}, {k: v for k, v in evidence_tool.T4_NAMES.items() if k != 41})
		self.assertEqual({k: v for k, v in curator.ROM_SOLENOID_NAMES.items() if k in evidence_tool.T5_NAMES}, evidence_tool.T5_NAMES)
		self.assertEqual(curator.SWITCH_FIRES, {address: fired for address, (fired, _) in evidence_tool.SWITCH_FIRES.items()})

	def test_output_kinds_mirrors_and_cabinet_devices(self) -> None:
		self.assertEqual({17, 18, 19, 20, 22, 24}, {a for a, c in self.coils.items() if c["kind"] == "flasher"})
		self.assertEqual("magnet", self.coils[8]["kind"])
		self.assertEqual({37, 38, 39, 40}, {a for a, c in self.coils.items() if c["kind"] == "control_signal"})
		for address in (41, 42, 43, 44):
			self.assertEqual(("virtual", "used", ["internal.duplicate.lpdc-mirror"]), (self.coils[address]["kind"], self.coils[address]["availability"], self.coils[address]["roles"]), address)
		self.assertIn("41 COIN METER", self.coils[41]["physical"]["notes"])
		for address in (33, 34, 35, 36):
			self.assertEqual(f"device.shoot-{address - 32}", self.coils[address]["id"])
			self.assertIn("FLIP_SOL(FLIP_L)", self.coils[address]["physical"]["notes"])
		self.assertEqual({45: "29", 46: "30", 47: "31", 48: "32"}, {a: next(x["value"] for x in self.coils[a]["aliases"] if x["namespace"] == "manual.address") for a in (45, 46, 47, 48)})
		self.assertEqual("not_applicable", self.coils[7]["spatial"]["status"])
		self.assertEqual("not_applicable", self.switches[12]["spatial"]["status"])
		for address in (19, 20, 24):
			self.assertEqual(2, self.coils[address]["physical"]["quantity"], address)
		self.assertEqual(2, self.lamps[61]["physical"]["quantity"])
		self.assertEqual(2, len(self.lamps[61]["spatial"]["placements"]))
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
		self.assertIn("40", self.coils[40]["physical"]["notes"])
		self.assertIn("GRN-WHT", self.coils[40]["physical"]["notes"])

	def test_gi_strings_dim_or_stay_on_as_the_rom_says(self) -> None:
		for address in (0, 1, 2):
			self.assertIn(f"steps its brightness on public GI {address} alone", self.gi[address]["physical"]["notes"], address)
			self.assertEqual("observed", self.gi[address]["spatial"]["status"], address)
		for address in (3, 4):
			self.assertIn("'ON ONLY'", self.gi[address]["physical"]["notes"], address)
			self.assertNotIn("spatial", self.gi[address], address)

	def test_displays_include_the_playfield_shot_clock(self) -> None:
		displays = {item["id"]: item for item in self.definition["displays"]}
		self.assertEqual({"display.dmd", "display.shot-clock"}, set(displays))
		clock = displays["display.shot-clock"]
		self.assertEqual(("segment", 1, 2, "playfield"), (clock["kind"], clock["controller_index"], clock["width"], clock["physical_location"]))
		self.assertEqual("observed", clock["spatial"]["status"])
		self.assertEqual("not_applicable", displays["display.dmd"]["spatial"]["status"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		paint = mechanisms["mechanism.in-the-paint"]
		self.assertEqual([f"switch.matrix-{a}" for a in (68, 67, 66, 65)], paint["sensors"])
		self.assertEqual({self.coils[a]["id"] for a in (15, 16, 25, 26, 27, 28, 33, 34, 35, 36)}, set(paint["actuators"]))
		defender = mechanisms["mechanism.defender"]
		self.assertEqual([self.coils[37]["id"], self.coils[38]["id"]], defender["actuators"])
		self.assertEqual(["position-1", "position-2", "lock", "position-3", "position-4"], [p["id"] for p in defender["positions"]])
		self.assertEqual([[f"switch.matrix-{a}"] for a in (55, 54, 53, 52, 51)], [p["sensors"] for p in defender["positions"]])
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
		uncited = {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE, curator.MANUAL_MARCH_SOURCE}
		self.assertEqual(set(sources), cited | uncited)
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("/Mask", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.webp")}, {"switch-locations", "lamp-locations", "solenoid-flashlamp-locations"})
		self.assertTrue(sources[curator.VPX_SCRIPT_SOURCE]["known_working"])
		self.assertEqual(SCRIPT_SHA256, sources[curator.VPX_SCRIPT_SOURCE]["sha256"])

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
		self.assertGreaterEqual(len(validated), 100)
		for key, page in seed["pages"].items():
			self.assertEqual(5, len(page["controls"]), key)
			self.assertLessEqual(decisions["pages"][key]["control_loo_max"], 0.02, key)
		for pid in seed["measurements"]:
			placement = self._placement(pid)
			self.assertEqual(drawing_callouts.measured(seed, pid), (placement["x"], placement["y"]), pid)
			self.assertEqual("observed", placement["provenance"]["status"], pid)
			self.assertEqual([curator.MANUAL_SOURCE, curator.CALLOUT_SOURCE], placement["provenance"]["source_refs"], pid)
			self.assertNotIn(pid, seed["checks"])
		self.assertEqual(
			{"switch.matrix-51.sensor", "switch.matrix-52.sensor", "switch.matrix-53.sensor", "switch.matrix-54.sensor", "switch.matrix-55.sensor",
			 "device.defender-motor-enable.effect", "device.defender-motor-direction.effect", "device.shot-clock-enable.effect",
			 "device.shot-clock-count.effect", "device.trophy-insert-flasher.emitter"},
			set(seed["measurements"]),
		)
		# The five defender optos lie along the arc from position 1 (left) to position 4 (right).
		xs = [self._placement(f"switch.matrix-{a}.sensor")["x"] for a in (55, 54, 53, 52, 51)]
		self.assertEqual(sorted(xs), xs)

	def test_legacy_compatibility_aliases_are_preserved_by_binding(self) -> None:
		seed = load(curator.LEGACY_ALIAS_SEED_PATH)["aliases"]
		by_group = {"pinmame.input.switch": self.switches, "pinmame.output.lamp": self.lamps, "pinmame.output.solenoid": self.coils}
		self.assertEqual(set(by_group), set(seed))
		for group, entries in seed.items():
			for address, aliases in entries.items():
				present = {(a["namespace"], a["value"]) for a in by_group[group][int(address)]["aliases"]}
				self.assertLessEqual({tuple(a) for a in aliases}, present, (group, address))
		self.assertIn(("vpe-legacy.switch", "007"), {(a["namespace"], a["value"]) for a in self.switches[7]["aliases"]})

	def test_no_artifact_names_another_machines_driver_or_record(self) -> None:
		catalog = load(ROOT / "catalog" / "pinmame.json")
		# Two catalog driver ids are ordinary words in this record's prose: "real" (the real launcher) and "v1" (table v1.3).
		ordinary_words = {"real", "v1"}
		forbidden = ({driver["id"] for driver in catalog["drivers"]} - DRIVER_IDS - ordinary_words) | (
			{machine["id"] for machine in catalog["machines"]} - {"bally.nba-fastbreak.1997"}
		)
		self.assertIn("stargzr", forbidden)
		self.assertIn("bally.attack-from-mars.1995", forbidden)
		paths = [
			DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md"),
			ROOT / "tools" / "curate_nba_fastbreak.py", ROOT / "tools" / "nba_fastbreak_runtime_evidence.py",
			*sorted((ROOT / "tools" / "seeds" / "bally").glob("nba-fastbreak-1997*")),
			*[RUNTIME_DIRECTORY / filename for filename in evidence_tool.RUNS],
			*sorted((ROOT / "tools" / "harness-scenarios" / "wpc-95").glob("nbaf-*.json")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			found = sorted(item for item in forbidden if re.search(rf"(?<![\w.-]){re.escape(item)}(?![\w-])", text))
			self.assertEqual([], found, path.name)
			self.assertNotIn("Doctor Who", text, path.name)

	def test_fitted_outputs_never_carry_the_not_used_wording(self) -> None:
		for address, coil in self.coils.items():
			notes = coil.get("physical", {}).get("notes", "")
			if coil["availability"] == "unused" and coil["kind"] != "virtual":
				self.assertIn("print NOT USED", notes, address)
			else:
				self.assertNotIn("print NOT USED", notes, address)
				self.assertNotIn("skips", notes, address)

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("In The Paint", "defender", "shot clock", "Backbox basketball", "spatial_placement", "never invert 31-37 or 115 again"):
			self.assertIn(phrase.casefold(), note.casefold(), phrase)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (_directory, scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-95" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.nba-fastbreak.1997"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertIn(f"--handle-mechanics {mechanics} ", document["runtime"]["command_template"], filename)
			self.assertEqual(len(load(scenario_path)["actions"]), raw["action_count"], filename)
		sources = {source["id"]: source for source in self.definition["sources"]}
		for source_id, name, _ in curator.RUNTIME_SOURCES:
			self.assertTrue((ROOT / sources[source_id]["uri"].removeprefix("internal:")).is_file(), source_id)
		edges = load(RUNTIME_DIRECTORY / "nba-fastbreak-nbaf_31-switch-edges-sweep.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address in curator.MASKED_SWITCHES:
			self.assertTrue(texts[f"{address} -> 1"].startswith(curator.ROM_SWITCH_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
		self.assertTrue(texts["24 -> 0"].startswith("ALWAYS CLOSED"))
		solenoids = load(RUNTIME_DIRECTORY / "nba-fastbreak-nbaf_31-solenoid-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([list(sorted(evidence_tool.T4_PUBLISHED[a])) for a in evidence_tool.T4_ORDER], [item["transitioned_solenoid_addresses"] for item in solenoids])

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (directory, _scenario, mechanics, _builder) in evidence_tool.RUNS.items():
			path = root / evidence_tool.HARNESS_DIRECTORY / directory
			check_manifest(path, "nbaf_31")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(mechanics, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_retained_callout_artifacts_match_the_seed(self) -> None:
		seed = load(curator.CALLOUT_SEED_PATH)
		checked = drawing_callouts.verify_retained(seed, ROOT, None, Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]))
		self.assertGreater(checked, 3)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "nba-fastbreak-1997" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		for snippet in ('Const cGameName = "nbaf_31"', ".Sol1 = 37", ".Sol2 = 38", "SolCallBack(7) = \"SolBasket\"", "SolCallBack(33) = \"bsSaucer1.SolOut\""):
			self.assertIn(snippet, text)


if __name__ == "__main__":
	unittest.main()
