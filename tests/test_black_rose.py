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

import black_rose_runtime_evidence as evidence_tool  # noqa: E402
import curate_black_rose as curator  # noqa: E402
import drawing_callouts  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "black-rose-1992.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "black-rose-1992.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "black-rose-1992.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "black-rose-1992.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "bally" / "black-rose-1992.md"
RUNTIME_DIRECTORY = ROOT / "evidence" / "runtime" / "wpc-fliptronic"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / "bally.black-rose.1992"

DRIVER_IDS = {"br_l4", "br_d4", "br_l3", "br_d3", "br_l1", "br_d1", "br_p17", "br_p18"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 23, 67, 68, 73, 74, 75, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# brGameData's inverted-switch mask (src/wpc/sims/wpc/full/br.c) is twelve zero bytes.
BR_INVERTED_SWITCH_MASK = (0x00,) * 12
SCRIPT_SHA256 = "c860e49c2b8be296ce73a64b5e9715245e290b3c2a799f24640234534f799f25"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "8b66e2656562c39590033f51253bb630220178457b1c1c6e09ac023fc1a540a3"
RUNTIME_FILES = {
	"black-rose-br_l4-switch-edges.json": ("br-switch-edges", "switch-edges"),
	"black-rose-br_l4-switch-edges-upper-left.json": ("br-switch-edges-upper-left", "switch-edges-upper-left"),
	"black-rose-br_l4-solenoid-test.json": ("br-solenoid-test", "solenoid-test"),
	"black-rose-br_l4-flasher-test-names.json": ("br-flasher-test-names", "flasher-test-names"),
	"black-rose-br_l4-gi-test.json": ("br-gi-test", "gi-test"),
	"black-rose-br_l4-single-lamps.json": ("br-single-lamps", "single-lamps"),
	"black-rose-br_l4-flipper-coil-test.json": ("br-flipper-coil-test", "flipper-coil-test"),
	"black-rose-br_l4-cannon-test.json": ("br-cannon-test", "cannon-test"),
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def seed_entries(category: str) -> dict:
	return load(curator.SPATIAL_SEED_PATH)[category]


def sw2m(number: int) -> int:
	# src/wpc/wpc.c: wpc_sw2m(no) = (no/10)*8 + (no%10 - 1); core_setSw indexes invSw by wpc_sw2m(no)/8.
	return (number // 10) * 8 + (number % 10 - 1)


class BlackRoseTests(unittest.TestCase):
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
		for item in self.definition["inputs"] + self.definition["outputs"]:
			for placement in (item.get("spatial") or {}).get("placements", []):
				if placement["id"] == placement_id:
					return placement
		raise AssertionError(placement_id)

	def test_identity_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.black-rose.1992", 313, 1992, "G5vZd-MQpWZ"), (machine["id"], machine["ipdb_id"], machine["year"], machine["opdb_id"]))
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS - {"br_p17", "br_p18"}, {key for key, value in compatibility.items() if value == "identical"})
		self.assertEqual({"br_p17", "br_p18"}, {key for key, value in compatibility.items() if value == "unknown"})
		catalog = {item["id"]: item for item in load(ROOT / "catalog/pinmame.json")["drivers"]}
		self.assertEqual(DRIVER_IDS, {key for key, item in catalog.items() if item.get("machine_id") == "bally.black-rose.1992"})
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "variant_differences"], self.definition["coverage"]["missing"])
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
		self.assertEqual(UNUSED_MATRIX_ADDRESSES, curator.UNUSED_MATRIX_ADDRESSES)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertIn("FAKE!", self.switches[77]["physical"]["notes"])

	def test_a_zero_inverted_switch_mask_leaves_every_matrix_switch_normally_open(self) -> None:
		inverted = {number for number in MATRIX_ADDRESSES if (BR_INVERTED_SWITCH_MASK[sw2m(number) // 8] >> (sw2m(number) % 8)) & 1}
		self.assertEqual(set(), inverted)
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}:
			switch = self.switches[address]
			self.assertIs(False, switch["normally_closed"], address)
			self.assertNotEqual("opto", switch["physical"].get("switch_type"), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[22]["initial_active"])
		for address in (*range(1, 9), 111, 112, 113, 114, 115, 116, 118):
			self.assertIs(False, self.switches[address]["normally_closed"], address)
		# Every switch the T.1 run swept is named at public 1 and cleared at 0 in the retained frames' readings.
		edges = load(RUNTIME_DIRECTORY / "black-rose-br_l4-switch-edges.json")["runtime"]["observations"]
		texts = {item["label"]: item["interpreted_text"] for item in edges["diagnostic_snapshots"]}
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertTrue(texts[f"{address} -> 1"].startswith(evidence_tool.EDGE_NAMES[address]), address)
			self.assertTrue(texts[f"{address} -> 0"].startswith("SWITCH EDGES"), address)
			self.assertIn("runtime.black-rose.switch-edges", self.switches[address]["provenance"]["source_refs"], address)

	def test_rom_printed_names_are_literal_in_the_device_notes(self) -> None:
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f'run names it "{name}" while public {address} is 1', self.switches[address]["physical"]["notes"], address)
			expected = evidence_tool.EDGE_NAMES[address]
			self.assertEqual(expected, name.replace("(R)", ""), address)
		for address, name in curator.T4_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {curator.T4_WIRES[address]}', self.coils[address]["physical"]["notes"], address)
		self.assertEqual(curator.T4_NAMES, evidence_tool.T4_NAMES)
		self.assertEqual(curator.T4_WIRES, evidence_tool.T4_WIRES)
		self.assertEqual(curator.T5_NAMES, evidence_tool.T5_NAMES)
		for address, name in curator.T5_NAMES.items():
			self.assertIn(f'prints "{name}" with the wires {evidence_tool.T5_WIRES[address]} RED-WHT', self.coils[address]["physical"]["notes"], address)
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertEqual(evidence_tool.T8_NAMES[address], name.replace("(R)", ""), address)
			self.assertIn(f'names it "{name}"', self.lamps[address]["physical"]["notes"], address)
		for address, (_, _, _, _, _, _, rom_name, rom_wires) in curator.GI_STRINGS.items():
			self.assertEqual((evidence_tool.GI_NAMES[address], evidence_tool.GI_WIRES[address]), (rom_name, rom_wires), address)
			self.assertIn(f'names it "{rom_name}"', self.gi[address]["physical"]["notes"], address)
		for address, entry in curator.FLIPPER_COILS.items():
			self.assertEqual((evidence_tool.T12_NAMES[address], evidence_tool.T12_WIRES[address]), entry[6:], address)

	def test_the_rom_settles_the_jet_bumper_transposition_in_the_switch_list(self) -> None:
		self.assertEqual(("Bottom Jet", "Right Jet"), (curator.SWITCH_LOCATIONS[47][2], curator.SWITCH_LOCATIONS[48][2]))
		self.assertEqual(("Right Jet Bumper", "Bottom Jet Bumper"), (self.switches[47]["label"], self.switches[48]["label"]))
		self.assertEqual({28: 6, 38: 5, 46: 13, 47: 14, 48: 15}, curator.EDGE_COILS)
		self.assertEqual(curator.EDGE_COILS, evidence_tool.EDGE_COILS)
		observations = load(RUNTIME_DIRECTORY / "black-rose-br_l4-switch-edges.json")["runtime"]["observations"]["named_action_observations"]
		fired = {item["input_address"]: item["transitioned_solenoid_addresses"] for item in observations}
		for switch, coil in curator.EDGE_COILS.items():
			self.assertEqual([coil], fired[switch], switch)
			self.assertIn(f"fires solenoid {coil} on the closure", self.switches[switch]["physical"]["notes"], switch)
		self.assertEqual({112: [45, 46], 114: [47, 48], 116: [33, 34]}, {k: fired[k] for k in (112, 114, 116)})
		for address in (47, 48):
			self.assertIn("the other way round from the Switch Matrix", self.switches[address]["physical"]["notes"], address)

	def test_flipper_inputs_and_outputs(self) -> None:
		self.assertEqual("unused", self.switches[117]["availability"])
		self.assertEqual("optional", self.switches[118]["availability"])
		for address in (111, 112, 113, 114, 115, 116):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (35, 36):
			self.assertEqual("unused", self.coils[address]["availability"], address)
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		for address in (33, 34, 45, 46, 47, 48):
			self.assertEqual(("coil", "used"), (self.coils[address]["kind"], self.coils[address]["availability"]), address)
		self.assertEqual("device.upper-right-flipper-power", self.coils[33]["id"])
		flips = load(RUNTIME_DIRECTORY / "black-rose-br_l4-flipper-coil-test.json")["runtime"]["observations"]["named_action_observations"]
		self.assertEqual([[45, 46], [46], [47, 48], [48], [33, 34], [34]], [item["transitioned_solenoid_addresses"] for item in flips])
		upper = load(RUNTIME_DIRECTORY / "black-rose-br_l4-switch-edges-upper-left.json")["runtime"]["observations"]
		self.assertEqual({118, 117}, {item["input_address"] for item in upper["named_action_observations"]})
		self.assertTrue(all(not item["transitioned_solenoid_addresses"] for item in upper["named_action_observations"]))
		self.assertEqual([], [a for a in upper["solenoid_addresses_seen"] if a not in (31,)])

	def test_output_kinds_and_availability(self) -> None:
		for address in range(17, 29):
			self.assertEqual("flasher", self.coils[address]["kind"], address)
		self.assertEqual("motor", self.coils[3]["kind"])
		for address in (29, 30, 31):
			self.assertEqual(("virtual", "used"), (self.coils[address]["kind"], self.coils[address]["availability"]), address)
		for address in (12, 16, 32, 35, 36, *range(37, 45), 49, 50):
			self.assertEqual("unused", self.coils[address]["availability"], address)
		for address in (7, 27):
			self.assertEqual("not_applicable", self.coils[address]["spatial"]["status"], address)
		self.assertNotIn("spatial", self.coils[25])
		self.assertEqual(2, self.coils[25]["physical"]["quantity"])
		self.assertEqual(2, self.coils[26]["physical"]["quantity"])
		self.assertEqual(2, len(self.coils[26]["spatial"]["placements"]))
		self.assertEqual(curator.SOLENOID_CONNECTIONS, {a: self.coils[a]["wiring"]["control_connection"] for a in (25, 26, 27, 28)})
		for address in (78, 87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
		for address in (11, 86):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual({3, 4}, {a for a, g in self.gi.items() if g["spatial"]["status"] == "not_applicable"})
		for address in (0, 1, 2):
			self.assertIn("'to insert board'", self.gi[address]["physical"]["notes"], address)

	def test_mechanisms_reference_declared_devices(self) -> None:
		known = set(self.inputs) | set(self.outputs)
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for mechanism in mechanisms.values():
			self.assertLessEqual(set(mechanism["actuators"]) | set(mechanism["sensors"]), known, mechanism["id"])
		self.assertEqual({self.coils[3]["id"], self.coils[8]["id"]}, set(mechanisms["mechanism.cannon"]["actuators"]))
		self.assertEqual({"switch.matrix-35", "switch.matrix-66"}, set(mechanisms["mechanism.cannon"]["sensors"]))
		self.assertEqual({self.coils[10]["id"], self.coils[11]["id"]}, set(mechanisms["mechanism.davy-jones-locker-ramp"]["actuators"]))
		self.assertEqual(["switch.matrix-54"], mechanisms["mechanism.davy-jones-locker-ramp"]["sensors"])
		self.assertEqual({"switch.matrix-71", "switch.matrix-63", "switch.matrix-64"}, set(mechanisms["mechanism.pirates-cove-lockup"]["sensors"]))
		cannon = load(RUNTIME_DIRECTORY / "black-rose-br_l4-cannon-test.json")["runtime"]["observations"]
		self.assertEqual([[8], [3]], [item["transitioned_solenoid_addresses"] for item in cannon["named_action_observations"]])
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
		self.assertEqual(set(sources), cited | {curator.CATALOG_SOURCE, curator.VPX_EXTRACTION_SOURCE})
		excerpts = set()
		for source in sources.values():
			self.assertIn("license", source)
			for excerpt in source.get("excerpts", []):
				excerpts.add(Path(excerpt["path"]).stem)
				self.assertEqual(hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["sha256"], excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image_sha256"], excerpt["id"])
					self.assertIn("WebP", excerpt["image_derivation"])
		self.assertEqual({path.stem for path in EXCERPT_DIRECTORY.glob("*.md")}, excerpts)
		images = {path.stem for path in EXCERPT_DIRECTORY.glob("*.webp")}
		self.assertEqual(images, {Path(e["image"]).stem for s in sources.values() for e in s.get("excerpts", []) if "image" in e})
		self.assertEqual(curator.MANUAL_SHA256, sources[curator.MANUAL_SOURCE]["sha256"])
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
		for pid in seed["measurements"]:
			placement = self._placement(pid)
			self.assertEqual("observed", placement["provenance"]["status"], pid)
			self.assertEqual([curator.MANUAL_SOURCE, curator.CALLOUT_SOURCE], placement["provenance"]["source_refs"], pid)
			self.assertEqual(tuple(seed["measurements"][pid]["normalized"]), (placement["x"], placement["y"]), pid)
		self.assertEqual(
			{"switch.matrix-16.sensor", "switch.matrix-17.sensor", "switch.matrix-18.sensor", "switch.matrix-54.sensor", "device.ramp-up.effect", "device.ramp-down.effect"},
			set(seed["measurements"]),
		)
		# The sword lamps 14-17 are never checked: the lamp drawing numbers those inserts in reverse.
		for address in (14, 15, 16, 17):
			pid = f"lamp.matrix-{address}.emitter"
			self.assertNotIn(pid, seed["checks"])
			self.assertIn("reverse", seed["excluded_checks"][pid])
			self.assertEqual("observed", self._placement(pid)["provenance"]["status"])
			self.assertIn(curator.PHOTO_SOURCE, self.lamps[address]["provenance"]["source_refs"])

	def test_legacy_compatibility_aliases_are_preserved_by_binding(self) -> None:
		seed = load(curator.LEGACY_ALIAS_SEED_PATH)
		self.assertEqual("bally.black-rose.1992", seed["machine_id"])
		by_group = {"pinmame.input.switch": self.switches, "pinmame.output.lamp": self.lamps, "pinmame.output.solenoid": self.coils}
		self.assertEqual(set(by_group), set(seed["aliases"]))
		for group, entries in seed["aliases"].items():
			for address, aliases in entries.items():
				present = {(a["namespace"], a["value"]) for a in by_group[group][int(address)]["aliases"]}
				self.assertLessEqual({tuple(a) for a in aliases}, present, (group, address))
		self.assertIn(("vpe-legacy.switch", "007"), {(a["namespace"], a["value"]) for a in self.switches[7]["aliases"]})
		# The legacy platform's game-on alias at 19 was retired when the ROM's flasher test named the address.
		self.assertNotIn(("vpe-legacy.coil", "c_game_on"), {(a["namespace"], a["value"]) for a in self.coils[19].get("aliases", [])})

	def test_gi_bulbs_cannot_be_validated_so_the_record_stays_partial(self) -> None:
		for address in (0, 1, 2):
			spatial = self.gi[address]["spatial"]
			self.assertEqual("observed", spatial["status"], address)
			self.assertTrue(all(p["provenance"]["status"] == "observed" for p in spatial["placements"]), address)
			self.assertNotIn("quantity", self.gi[address].get("physical", {}), address)
		report = load(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual([self.coils[25]["id"]], report["without_placements"])
		self.assertEqual(0, len(report["placement_status"]["candidate"]))
		for gi_id in ("gi.string-1", "gi.string-2", "gi.string-3"):
			self.assertIn(gi_id, report["placement_status"]["observed"])
		self.assertEqual(["spatial_placement", "variant_differences"], self.definition["coverage"]["missing"])

	def test_the_curator_reproduces_every_artifact_and_the_knowledge_note(self) -> None:
		curator.check()
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), KNOWLEDGE_PATH.read_bytes())
		self.assertNotIn(b"\r", KNOWLEDGE_PATH.read_bytes())
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for phrase in ("The ball cannon (headline mechanism)", "Davy Jones' Locker", "47 RIGHT JET", "spatial_placement", "FAKE!"):
			self.assertIn(phrase, note)
		with self.assertRaises(RuntimeError):
			original = KNOWLEDGE_PATH.read_bytes()
			try:
				KNOWLEDGE_PATH.write_bytes(original + b"\n")
				curator.check()
			finally:
				KNOWLEDGE_PATH.write_bytes(original)

	def test_no_artifact_names_the_sibling_whose_curator_was_the_template(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")["drivers"]
		sibling = {item["id"] for item in catalog if item.get("machine_id") == "bally.doctor-who.1992"} | {"bally.doctor-who.1992", "doctor-who", "Doctor Who", "dwGameData", "Dalek", "Tardis"}
		self.assertIn("dw_l2", sibling)
		paths = [DEFINITION_PATH, KNOWLEDGE_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_MARKDOWN_PATH, curator.SPATIAL_SEED_PATH, curator.CALLOUT_SEED_PATH,
			curator.LEGACY_ALIAS_SEED_PATH, evidence_tool.FRAME_READINGS_PATH, ROOT / "tools/curate_black_rose.py", ROOT / "tools/black_rose_runtime_evidence.py"]
		paths += sorted(EXCERPT_DIRECTORY.glob("*.md")) + [RUNTIME_DIRECTORY / name for name in RUNTIME_FILES]
		for path in paths:
			text = path.read_text(encoding="utf-8")
			for name in sorted(sibling):
				self.assertNotIn(name, text, (path.name, name))

	def test_compact_runtime_evidence_is_tied_to_its_scenario_and_pinned_binary(self) -> None:
		for filename, (scenario, directory) in RUNTIME_FILES.items():
			document = load(RUNTIME_DIRECTORY / filename)
			(raw,) = document["runtime"]["raw_runs"]
			scenario_path = ROOT / "tools" / "harness-scenarios" / "wpc-fliptronic" / f"{scenario}.json"
			self.assertEqual(hashlib.sha256(scenario_path.read_bytes()).hexdigest(), raw["scenario_sha256"], filename)
			self.assertNotIn(b"\r", scenario_path.read_bytes(), filename)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"], filename)
			self.assertEqual(curator.PINMAME_REVISION, document["runtime"]["emulator"]["built_from_revision"], filename)
			self.assertEqual(ROM_ARCHIVE_SHA256, document["runtime"]["rom_archive_sha256"], filename)
			self.assertEqual(["bally.black-rose.1992"], document["machine_ids"], filename)
			self.assertEqual(raw["sha256"], document["source"]["sha256"], filename)
			self.assertTrue(raw["retained_from"].endswith(f"/{directory}/br_l4/run.json"), filename)
			scenario_document = load(scenario_path)
			self.assertEqual("pinmame-harness-scenario", scenario_document["format"], filename)
			self.assertEqual(len(scenario_document["actions"]), raw["action_count"], filename)
		# Every reading the compact evidence carries is the pinned reading of that exact frame, and every pinned reading is cited.
		pins = load(evidence_tool.FRAME_READINGS_PATH)["runs"]
		self.assertEqual({directory for _, directory in RUNTIME_FILES.values()}, set(pins))
		for filename, (_scenario, directory) in RUNTIME_FILES.items():
			snapshots = load(RUNTIME_DIRECTORY / filename)["runtime"]["observations"]["diagnostic_snapshots"]
			self.assertEqual(
				{label: (pin["pixel_sha256"], pin["reading"]) for label, pin in pins[directory].items()},
				{item["label"]: (item["pixel_sha256"], item["interpreted_text"]) for item in snapshots},
				filename,
			)
		solenoids = load(RUNTIME_DIRECTORY / "black-rose-br_l4-solenoid-test.json")["runtime"]["observations"]
		self.assertEqual(list(evidence_tool.T4_ORDER), [item["transitioned_solenoid_addresses"][0] for item in solenoids["named_action_observations"]])
		lamps = load(RUNTIME_DIRECTORY / "black-rose-br_l4-single-lamps.json")["runtime"]["observations"]
		self.assertEqual(64, len(lamps["named_action_observations"]))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from build_external_evidence_manifest import check_manifest

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		evidence_tool.check(root)
		for filename, (_scenario, directory) in RUNTIME_FILES.items():
			path = root / "black-rose-1992" / "harness" / directory / "br_l4"
			check_manifest(path, "br_l4")
			run = json.loads((path / "run.json").read_bytes())
			self.assertIsNone(run["failure"], filename)
			self.assertEqual(0, run["handle_mechanics"], filename)
			self.assertEqual([{"state": 0, "switch": 22}], run["initial_switches"], filename)
			self.assertEqual(hashlib.sha256((path / "run.json").read_bytes()).hexdigest(), load(RUNTIME_DIRECTORY / filename)["runtime"]["raw_runs"][0]["sha256"], filename)
		seed = load(curator.CALLOUT_SEED_PATH)
		self.assertGreater(drawing_callouts.verify_retained(seed, ROOT, None, root), 0)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_the_evidence_builder_refuses_frames_and_transitions_that_do_not_support_its_readings(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		original = evidence_tool._load_run

		def mutated(change):
			def load_run(review_root, directory, scenario):
				run = original(review_root, directory, scenario)
				change(directory, run)
				return run
			return load_run

		def blank_frame(directory, run):
			if directory == "cannon-test":
				snapshot = next(item for item in run["snapshots"] if item["label"] == "T.14 after the first toggle, frame 3")
				snapshot["displays"][0]["pixel_sha256"] = hashlib.sha256(bytes(128 * 32)).hexdigest()
				snapshot["displays"][0]["nonzero_pixels"] = 0

		def motor_never_stops(directory, run):
			if directory == "cannon-test":
				step = next(item for item in run["steps"] if item["label"] == "Enter (toggle the cannon motor again)")
				for item in step["transitions"]["solenoids"]:
					if item["number"] == 3:
						item["states"] = [1]

		def substituted_frame(directory, run):
			# A valid, non-blank frame of another step (MOTOR = OFF) must not inherit the MOTOR = ON reading.
			if directory == "cannon-test":
				by_label = {item["label"]: item for item in run["snapshots"]}
				by_label["T.14 after the first toggle, frame 3"]["displays"] = by_label["T.14 after the second toggle, frame 3"]["displays"]

		def missing_release(directory, run):
			if directory == "switch-edges":
				run["snapshots"] = [item for item in run["snapshots"] if item["label"] != "47 -> 0"]

		def wrong_initial_flasher(directory, run):
			# The first T.5 selection must be proven by its own step and checkpoint, not assumed.
			if directory == "flasher-test-names":
				for step in run["steps"]:
					if step["label"] in ("Enter (start T.5 FLASHER TEST)", "checkpoint: T.5 pulses flasher 17") or step["label"].startswith("T.5 step 0"):
						for item in list(step["transitions"].get("solenoids", [])) + list(step.get("matched_outputs") or []):
							if item["number"] == 17:
								item["number"] = 26

		builders = {blank_frame: evidence_tool.build_cannon, motor_never_stops: evidence_tool.build_cannon,
			substituted_frame: evidence_tool.build_cannon, missing_release: evidence_tool.build_edges,
			wrong_initial_flasher: evidence_tool.build_flashers}
		for change, builder in builders.items():
			evidence_tool._load_run = mutated(change)
			try:
				with self.assertRaises(ValueError, msg=change.__name__):
					builder(root)
			finally:
				evidence_tool._load_run = original
		evidence_tool.build_cannon(root)
		evidence_tool.build_edges(root)
		evidence_tool.build_flashers(root)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_vpx_extraction_matches_its_pinned_identity(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		manifest = curator.verify_extraction_manifest(root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))
		table = root / "bally" / "black-rose-1992" / "source" / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_text(encoding="utf-8", errors="replace")
		for fragment in ('Const cGameName = "br_l4"', ".initSwitches Array(16, 17, 18)", ".EntrySw = 15", "Controller.Switch(54) = 1", "Controller.Switch(35) = 1",
			'SolCallback(8) = \t"FireCannon"', 'SolCallback(3) = \t"CannonMotor"', "vpmTimer.PulseSw(47)"):
			self.assertIn(fragment, text, fragment)
		# The committed script excerpt quotes the retained script line for line.
		lines = script.read_bytes().decode("cp1252").splitlines()
		excerpt = (EXCERPT_DIRECTORY / "vpx-script-bindings.md").read_text(encoding="utf-8")
		self.assertIn(SCRIPT_SHA256, excerpt)
		quoted = [line for line in excerpt.split("```vbscript", 1)[1].split("```", 1)[0].splitlines() if line.strip()]
		self.assertGreater(len(quoted), 300)
		for line in quoted:
			number, _, body = line.partition(": ")
			self.assertEqual(lines[int(number) - 1].rstrip().replace(chr(9), "    "), body, number)
		# Every Light a lamp or flasher placement uses, and every render double collapsed into it, is one the script assigns.
		assigned = {name.casefold() for name in re.findall(r"^\s*(?:Mod)?Lampz\.MassAssign\(\d+\)\s*=\s*(\w+)", text, re.M)}
		for category in ("lamp", "solenoid"):
			for address, entries in seed_entries(category).items():
				for entry in entries:
					names = entry.get("collapsed", [entry["object"]] if entry.get("object") else [])
					if category == "solenoid" and not 17 <= int(address) <= 28:
						continue
					for name in names:
						self.assertIn(name.casefold(), assigned, (category, address, name))
		seed = load(curator.SPATIAL_SEED_PATH)
		gameitems = root / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		for category in ("switch", "lamp", "solenoid"):
			for address, entries in seed[category].items():
				for entry in entries:
					if entry.get("object"):
						self.assertTrue(any(gameitems.glob(f"*.{entry['object']}.json")), (category, address, entry["object"]))


if __name__ == "__main__":
	unittest.main()
