from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
DEFINITION_PATH = ROOT / "machines/partial/data-east/time-machine-1988.json"
SEED_PATH = ROOT / "tools/seeds/data-east/time-machine-1988.json"
MANIFEST_PATH = ROOT / "tools/seeds/data-east/time-machine-1988-extraction-manifest.json"
REPORT_PATH = ROOT / "reports/spatial/data-east/time-machine-1988.json"
REPORT_MD_PATH = ROOT / "reports/spatial/data-east/time-machine-1988.md"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/time-machine-1988.md"
EXCERPT_ROOT = ROOT / "evidence/excerpts/data-east.time-machine.1988"
OWN_DRIVERS = {"tmac_a24", "tmac_a18", "tmac_g18"}
OWN_MACHINE = "data-east.time-machine.1988"


SWITCHES = [
	"Plumb Tilt", "Not Used", "Credit Button", "Right Coin", "Center Coin", "Left Coin", "Slam Tilt", "Not Used",
	"Not Used", "Outhole", "Trough #1", "Trough #2", "Trough #3", "Shooter Lane", "Left EOS", "Right EOS",
	"Left Outlane", "Left Return", "Right Outlane", "Right Return", "Left Slingshot", "Right Slingshot", "Not Used", "Not Used",
	"1 Lane", "2 Lane", "3 Lane", "Left Ramp", "Center Ramp", "Right Ramp", "Left Rollover", "Right Rollover",
	"Left Bank1", "Left Bank2", "Left Bank3", "Wireform1", "Wireform2", "Wireform3", "Not Used", "Not Used",
	"Center Bank1", "Center Bank2", "Center Bank3", "Wireform4", "Super VUK", "Left Pop Bumper", "Center Pop Bumper", "Right Pop Bumper",
	"Right Bank1", "Right Bank2", "Right Bank3",
] + ["Not Used"] * 13

LAMPS = [
	'"S"tarwarp', 's"T"arwarp', 'st"A"rwarp', 'sta"R"warp', 'star"W"arp', 'starw"A"rp', 'starwa"R"p', 'starwar"P"',
	"Center Square", "Center Circle", "Center Triangle", "Left Ramp 1970", "Left Ramp 1960", "Left Ramp 1950", "5X", "4X",
	"Special", "3 Ball Jackpot", "Left Ramp E=MC²", "Left Mini Jackpot", "Center Mini Jackpot", "Right Mini Jackpot", "3X", "2X",
	"2X All Scores Cntr Plyfld", "Extra Ball Back Panel", "Bonus Hold Back Panel", "100K Back Panel", "50K Back Panel", "25K Back Panel",
	"Targets Light Special", "2X All Scores", "Left Triangle", "Left Circle", "Left Square", "Left Extra Ball", "Laser Kick", "Left Return",
	"Extra Ball Center Playfield", "Bonus Hold Center Plyfld", "Right Square", "Right Circle", "Right Triangle", "Right Hotdog", "Right Return",
	"Right Extra Ball", "Left Hotdog", "Starwarp Center Playfield", "Lane1", "Lane2", "Lane3", "Left Pop Bumper", "Center Pop Bumper",
	"Right Pop Bumper", "1980", "1970", "Top Right Arrow", "Right Ramp E=MC²", "Right Ramp 1950", "Right Ramp 1960", "Right Ramp 1970",
	"Engine", "1960", "1950",
]

SOLENOIDS = [
	"Klacker", "Chime 1", "Chime 2", "Chime 3", "Flash No.1", "Flash No.2", "Flash No.3", "Flash No.4", "Flash No.5",
	"Left/Right Coil Relay K1", "General Illumination Relay K1", "Flash No.6", "Flash No.7", "Flash No.8", "Flash No.9", "Laser Kick",
	"Right Pop Bumper (Coil Test table)", "Left Slingshot", "Left Pop Bumper", "Unused SP6 Driver", "Right Slingshot",
	"Center Pop Bumper (Coil Test table)", "Game On / Flipper and Special-Solenoid Enable", "Unused Solenoid 24", "Outhole", "Trough Eject",
	"Super Vertical Up Kicker", "Ball Lock Release", "Emulator-Published Mux State 29", "Emulator-Published Mux State 30",
	"Emulator-Published Mux State 31", "Emulator-Published Mux State 32",
] + [f"Inert Solenoid Address {number}" for number in range(33, 45)] + [
	"Synthetic Right Flipper Power", "Synthetic Right Flipper Hold", "Synthetic Left Flipper Power", "Synthetic Left Flipper Hold",
	"Simulation Ball Shooter", "Reserved Solenoid 50",
]

PRIOR_CONFLICT_IDS = {
	"conflict.left-flipper-eos-runtime", "conflict.right-flipper-eos-runtime", "conflict.mux-bank-output-typing",
	"conflict.special-solenoid-sp1-sp2-schematic-swap", "conflict.output-11-callback-overwrite",
	"conflict.switch-23-runtime-misroute", "conflict.switch-36-runtime-misroute", "conflict.lamp-24-runtime-omission",
}


def load_json(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as stream:
		for block in iter(lambda: stream.read(1024 * 1024), b""):
			digest.update(block)
	return digest.hexdigest()


class TimeMachineDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.inputs = {item["id"]: item for item in cls.definition["inputs"]}
		cls.outputs = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		cls.lamps = {item["binding"]["device"]: item for item in cls.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		cls.sources = {item["id"]: item for item in cls.definition["sources"]}

	def test_identity_parent_generation_and_exact_bounds(self) -> None:
		self.assertEqual(OWN_MACHINE, self.definition["machine"]["id"])
		self.assertEqual({"width":1000.0,"height":1910.0,"units":"vpx","provenance":{"status":"validated","source_refs":["vpx-table.time-machine-2.4.1"]}}, self.definition["machine"]["playfield"])
		self.assertEqual({"platform":"pinmame.dataeast","hardware_generation":"0x1000","inversion_applied_by_emulator":False}, self.definition["controller"])
		core = self.sources["pinmame.core.4ec52ff0ac13"]
		self.assertEqual("BSD-3-Clause",core["license"])
		self.assertIn("wpc.invSw zero-initialized",core["locator"])
		self.assertIn("core.c lines 2455-2456",core["locator"])
		for fragment in ("lines 714-715", "737-738", "746-747", "SP6, SP5, SP2, SP3, SP1, and SP4"):
			self.assertIn(fragment, core["locator"])
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(OWN_DRIVERS, set(drivers))
		self.assertNotIn("clone_of", drivers["tmac_a24"])
		self.assertEqual("tmac_a24", drivers["tmac_a18"]["clone_of"])
		self.assertEqual("tmac_a24", drivers["tmac_g18"]["clone_of"])
		self.assertEqual(["Time Machine (2.4)", "Time Machine (1.8)", "Time Machine (1.8 German)"], [driver["description"] for driver in self.definition["drivers"]])
		self.assertTrue(all(driver["year"] == "1988" and driver["manufacturer"] == "Data East" for driver in drivers.values()))
		self.assertIn("INITGAMES11(tmac, GEN_DE, de_dispAlpha2, FLIP1516, SNDBRD_DE1S, 0, 0)", self.sources["pinmame.core.4ec52ff0ac13"]["locator"])

	def test_complete_input_namespace_and_literal_manual_fitment(self) -> None:
		positive = {item["binding"]["device"]: item for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] > 0}
		self.assertEqual(set(range(1,65)), set(positive))
		self.assertEqual({-7,-6}, {item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] < 0})
		self.assertEqual([0], [item["binding"]["device"] for item in self.definition["inputs"] if item["binding"]["group"] == "pinmame.input.dip"])
		for number, printed in enumerate(SWITCHES, start=1):
			self.assertEqual(f"Unused Switch {number}" if printed == "Not Used" else printed, positive[number]["label"], number)
			self.assertEqual("unused" if printed == "Not Used" else "used", positive[number]["availability"], number)
		self.assertEqual("conflicted", positive[2]["provenance"]["status"])
		self.assertEqual("conflicted", positive[15]["provenance"]["status"])
		self.assertEqual("flipper.lower.left.button", positive[15]["roles"][0])
		self.assertEqual("180-5018-00", positive[16]["physical"]["part_number"])
		self.assertEqual({1,3,4,5,6,7,15,16}, {number for number,item in positive.items() if item.get("spatial",{}).get("reason") == "cabinet_or_service"})

	def test_lamps_are_exactly_1_through_64_and_lamp_25_fails_closed(self) -> None:
		self.assertEqual(set(range(1,65)), set(self.lamps))
		self.assertEqual(LAMPS, [self.lamps[number]["label"] for number in range(1,65)])
		self.assertTrue(all(self.lamps[number]["availability"] == "used" for number in self.lamps))
		self.assertEqual({1,2,3,4,5,6,7,8,26,27,28,29,30,62}, {number for number,item in self.lamps.items() if item.get("spatial",{}).get("reason") == "cabinet_or_service"})
		self.assertNotIn("spatial", self.lamps[25])
		self.assertEqual("conflicted", self.lamps[25]["provenance"]["status"])
		self.assertIn("is_backglass=true", self.lamps[25]["physical"]["notes"])
		located = [item for item in self.lamps.values() if item.get("spatial",{}).get("status") == "candidate"]
		self.assertEqual(49, len(located))

	def test_all_fifty_solenoids_have_machine_specific_dispositions(self) -> None:
		import curate_time_machine as curator
		self.assertEqual(set(range(1,51)), set(self.outputs))
		self.assertEqual(SOLENOIDS, [self.outputs[number]["label"] for number in range(1,51)])
		self.assertEqual("coil.game-on", self.outputs[23]["id"])
		self.assertEqual("relay", self.outputs[10]["kind"])
		self.assertEqual("gi", self.outputs[11]["kind"])
		self.assertTrue(all(self.outputs[number]["kind"] == "flasher" for number in [5,6,7,8,9,12,13,14,15,29,30,31,32]))
		self.assertEqual({20,24,*range(33,45),49,50}, {number for number,item in self.outputs.items() if item["availability"] == "unused"})
		self.assertTrue(all(self.outputs[number]["availability"] == "unknown" and self.outputs[number]["kind"] == "flasher" for number in range(29,33)))
		self.assertTrue(all("effective total of 23 regular coils" in self.outputs[number]["physical"]["notes"] for number in range(29,33)))
		self.assertTrue(all("device chart stops at SIDE R 04" in self.outputs[number]["physical"]["notes"] for number in range(29,33)))
		self.assertTrue(all("quantity" not in self.outputs[number].get("physical",{}) for number in range(29,33)))
		self.assertTrue(all("spatial" not in self.outputs[number] for number in range(29,33)))
		manual_aliases = {
			number: {alias["value"] for alias in output["aliases"] if alias["namespace"] == "manual.address"}
			for number, output in self.outputs.items()
		}
		expected_manual_aliases = {
			**{number: {f"SIDE L {number:02d}"} for number in range(1,9)},
			**{number: {str(number)} for number in range(9,17)},
			17: {"SP1"}, 18: {"SP3"}, 19: {"SP4"}, 20: {"SP6"}, 21: {"SP5"}, 22: {"SP2"},
			**{number: {f"SIDE R {number - 24:02d}"} for number in range(25,29)},
		}
		derived = {17 + curator.SPECIAL_DE_PERMUTATION[handler]: printed for handler, printed in curator.SPECIAL_PIA_HANDLER_TO_PRINTED.items()}
		self.assertEqual({17:1,18:3,19:4,20:6,21:5,22:2}, derived)
		self.assertEqual(derived, curator.SPECIAL_PUBLIC_TO_PRINTED)
		self.assertEqual(expected_manual_aliases, {number: values for number, values in manual_aliases.items() if values})
		for number in (10,11):
			self.assertEqual(1,self.outputs[number]["physical"]["quantity"],number)
			self.assertNotIn("bulbs",self.outputs[number]["physical"]["notes"].casefold(),number)
		self.assertEqual(("coil","unused","unused"),(self.outputs[20]["kind"],self.outputs[20]["availability"],self.outputs[20]["spatial"]["reason"]))
		self.assertEqual(("virtual","unused","virtual"),(self.outputs[24]["kind"],self.outputs[24]["availability"],self.outputs[24]["spatial"]["reason"]))
		self.assertTrue(all("quantity" not in self.outputs[number].get("physical",{}) for number in {20,24,*range(33,45),49,50}))
		self.assertTrue(all(self.outputs[number]["kind"] == "virtual" for number in range(33,51) if number not in {45,46,47,48}))
		self.assertTrue(all(self.outputs[number]["kind"] == "virtual" and self.outputs[number]["availability"] == "used" for number in {45,46,47,48}))
		self.assertTrue(all("quantity" not in self.outputs[number].get("physical",{}) and "part_number" not in self.outputs[number].get("physical",{}) for number in {45,46,47,48}))
		self.assertTrue(all(self.outputs[number]["spatial"]["status"] == "not_applicable" and self.outputs[number]["spatial"]["reason"] == "virtual" for number in {45,46,47,48}))
		self.assertTrue(all(self.outputs[number]["provenance"]["source_refs"] == ["manual.data-east.time-machine.1988","pinmame.core.4ec52ff0ac13"] for number in {20,24}))
		self.assertEqual({17:"Q8",18:"Q10",19:"Q11",20:"Q13",21:"Q12",22:"Q9"}, {number:self.outputs[number]["wiring"]["driver_transistor"] for number in range(17,23)})
		self.assertTrue(all(self.outputs[number]["provenance"]["source_refs"] == ["pinmame.core.4ec52ff0ac13"] for number in {*range(33,45),49,50}))
		self.assertTrue(all(self.outputs[number]["provenance"]["source_refs"] == ["pinmame.core.4ec52ff0ac13","vpx-script.time-machine-2.4.1"] for number in {45,46,47,48}))

	def test_mux_relationships_and_special_coil_conflict_are_not_inferred(self) -> None:
		relationships = self.definition["relationships"]
		self.assertEqual({f"coil.driver-{number}" for number in range(25,33)}, {item["destination"] for item in relationships})
		self.assertTrue(all(item["source"] == "coil.driver-10" and item["kind"] == "relay_gated" for item in relationships))
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual([], mechanisms["mechanism.center-pop"]["actuators"])
		self.assertEqual([], mechanisms["mechanism.right-pop"]["actuators"])
		self.assertEqual(["coil.driver-19"], mechanisms["mechanism.left-pop"]["actuators"])
		self.assertEqual(["coil.driver-18"], mechanisms["mechanism.left-slingshot"]["actuators"])
		self.assertEqual(["coil.driver-21"], mechanisms["mechanism.right-slingshot"]["actuators"])

	def test_display_array_and_mechanism_topology(self) -> None:
		self.assertEqual([(0,1,7),(1,9,7),(2,21,7),(3,29,7)], [(item["controller_index"],item["segment_start"],item["width"]) for item in self.definition["displays"]])
		self.assertTrue(all(item["spatial"]["status"] == "not_applicable" for item in self.definition["displays"]))
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		lock = mechanisms["mechanism.visible-lock"]
		self.assertEqual(["coil.driver-28"], lock["actuators"])
		self.assertEqual(["switch.matrix-36","switch.matrix-37","switch.matrix-38"], lock["sensors"])
		self.assertEqual(3, len(lock["positions"]))
		self.assertEqual("500-5104-00", lock["assembly_part_number"])
		vuk = mechanisms["mechanism.super-vuk"]
		self.assertEqual(["switch.matrix-44","switch.matrix-45"], vuk["sensors"])
		self.assertEqual("500-5116-00", vuk["assembly_part_number"])
		self.assertEqual({"mechanism.left-standups","mechanism.center-standups","mechanism.right-standups"}, {identifier for identifier in mechanisms if identifier.endswith("standups")})
		self.assertTrue(all(mechanisms[identifier]["kind"] == "other" and mechanisms[identifier]["actuators"] == [] for identifier in mechanisms if identifier.endswith("standups")))

	def test_coverage_and_source_conflicts_are_explicit(self) -> None:
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["controller_platform","output_semantics","mechanism_behavior","polarity","spatial_placement","unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("unknown", self.definition["coverage"]["dimensions"]["controller_platform"])
		conflict_ids = {item["id"] for item in self.definition["conflicts"]}
		self.assertEqual({
			"conflict.left-eos-vs-public-button-state", "conflict.right-eos-vs-public-button-state",
			"conflict.shared-port-position-2-vs-unfitted", "conflict.special-coil-right-center-location",
			"conflict.lamp-25-playfield-vs-table-backglass",
		}, conflict_ids)
		self.assertTrue(all(len(item["source_refs"]) >= 2 for item in self.definition["conflicts"]))

	def test_spatial_report_asserts_both_extents_and_concrete_blockers(self) -> None:
		report = load_json(REPORT_PATH)
		self.assertEqual({"left":0.0,"top":0.0,"right":1000.0,"bottom":1910.0}, report["coordinate_system"]["raw_bounds"])
		self.assertIn("width agreement alone is insufficient", report["method"][0])
		self.assertIn("l65", report["excluded_helpers"]["lamp_65"])
		self.assertEqual({"controller_platform","output_semantics","mechanism_behavior","polarity","spatial_placement","unresolved_conflicts"}, {item["dimension"] for item in report["blockers"]})
		placements = [placement for group in (self.definition["inputs"],self.definition["outputs"]) for item in group for placement in item.get("spatial",{}).get("placements",[])]
		self.assertTrue(placements)
		self.assertTrue(all(0 <= item["x"] <= 1 and 0 <= item["y"] <= 1 for item in placements))
		markdown = REPORT_MD_PATH.read_text(encoding="utf-8")
		self.assertIn("1000`, `bottom=1910", markdown)
		self.assertIn("Keep partial", markdown)

	def test_excerpt_hashes_and_literal_print_are_preserved(self) -> None:
		excerpts = self.sources["manual.data-east.time-machine.1988"]["excerpts"]
		self.assertEqual(4, len(excerpts))
		for excerpt in excerpts:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file())
			self.assertEqual(excerpt["sha256"], sha256(path), excerpt["id"])
			self.assertTrue(excerpt["reviewed"])
		switch = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
		lamp = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
		coil = (EXCERPT_ROOT / "coil-and-flipper.md").read_text(encoding="utf-8")
		construction = (EXCERPT_ROOT / "mechanism-construction.md").read_text(encoding="utf-8")
		self.assertIn("15 Left EOS", switch)
		self.assertIn("Left Flip. Instant Info.; Left EOS", switch)
		self.assertIn("Targets Lite Special", lamp)
		self.assertIn("Left EMC²SR", lamp)
		self.assertIn("Left Ramp E=MC²", lamp)
		self.assertIn("| SP1 | RIGHT POP BUMPER |", coil)
		self.assertIn("Control line (CPU to coil)", coil)
		self.assertIn("| SP5 | RIGHT SLINGSHOT | BLU-GRN / CPU CN19-8 | RED / PS CN3-6 | ORN-GRN / CPU CN18-8 | Q12 | 23-800 |", coil)
		self.assertIn("| SP6 | NOT USED | -- / CPU CN19-9 | -- / PS CN3-6 | -- / CPU CN18-9 | Q13 | -- |", coil)
		self.assertIn('"effectively provides 23 regular coils."', coil)
		self.assertIn("After SIDE R 04, the sheet shows no further right-side device rows", coil)
		self.assertIn("one `24-900` coil", construction)
		self.assertIn("red triangle, yellow circle, and blue square", construction)
		manual = self.sources["manual.data-east.time-machine.1988"]
		self.assertEqual("https://archive.org/download/Data_East_Time_Machine_Manual/Data_East_1988_Time_Machine_Manual.pdf", manual["uri"])
		self.assertEqual("Data_East_1988_Time_Machine_Manual.pdf", manual["original_filename"])
		self.assertEqual("Data_East_Time_Machine_Manual",manual["source_id"])
		self.assertEqual("NOASSERTION",manual["license"])
		self.assertEqual("NOASSERTION",manual["rights"])
		self.assertEqual("2026-08-09T12:41:47Z",manual["acquired_at"])
		self.assertIn("originally downloaded from IPDB",manual["locator"])
		for source in self.definition["sources"]:
			self.assertIn("acquired_at", source, source["id"])
			self.assertIn("license", source, source["id"])
			self.assertIn("attribution", source, source["id"])
		for source_id in ("vpx-table.time-machine-2.4.1", "vpx-script.time-machine-2.4.1", "vpx-extraction.time-machine-2.4.1"):
			source = self.sources[source_id]
			self.assertIn("source_id", source)
			self.assertIn("original_filename", source)
			self.assertIn("rights", source)
		self.assertTrue(all(item["uri"] == "https://github.com/vpinball/pinmame" for item in self.definition["sources"] if item["kind"] in {"pinmame_catalog","pinmame_core"}))
		self.assertTrue(all(item["uri"].startswith("external:pinmame-vpx-sources/") for item in self.definition["sources"] if item["kind"] in {"vpx_table","vpx_script"} and item["id"] != "vpx-extraction.time-machine-2.4.1"))
		self.assertTrue(all(not item["uri"].startswith(("source-checkouts/","vpx-sources/")) for item in self.definition["sources"]))
		self.assertEqual({
			"excerpt.time-machine.switch-matrix":"PDF pages 26-27, printed pages 22-23",
			"excerpt.time-machine.lamp-matrix":"PDF pages 28-29, printed pages 24-25",
			"excerpt.time-machine.coil-and-flipper":"PDF pages 30-31, printed pages 26-27",
			"excerpt.time-machine.mechanism-construction":"PDF page 67 (printed 47) and PDF pages 74, 76, 77 (printed 54, 56, 57)",
		}, {item["id"]:item["locator"] for item in excerpts})
		artifact_text = "\n".join(path.read_text(encoding="utf-8") for path in [DEFINITION_PATH, SEED_PATH, REPORT_PATH, REPORT_MD_PATH, KNOWLEDGE_PATH])
		self.assertNotIn("board_diagrams_are_in_color", artifact_text.casefold())
		self.assertNotIn("colour board diagrams", artifact_text.casefold())

	def test_manifest_canonical_digest_and_seed_identity(self) -> None:
		manifest = load_json(MANIFEST_PATH)
		self.assertEqual(3049, manifest["file_count"])
		self.assertEqual(313_925_219, manifest["total_bytes"])
		self.assertEqual(3049, len(manifest["files"]))
		algorithm = "SHA-256 of the UTF-8 JSON object after removing manifest_sha256 and serializing with sorted keys, compact separators, and ensure_ascii=False."
		self.assertEqual(algorithm, manifest["manifest_algorithm"])
		body = {key:value for key,value in manifest.items() if key != "manifest_sha256"}
		canonical = json.dumps(body,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
		self.assertEqual("91bb4c4b3be5b24ea9b77493e46d83810dd549ca10186ae47da4a1f8f9eaa185", hashlib.sha256(canonical).hexdigest())
		self.assertEqual(manifest["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
		extraction_source = self.sources["vpx-extraction.time-machine-2.4.1"]
		self.assertEqual("96ae681549e9284ccec0eddb0181decb07b0388651fcf9bfb22bd299dfb5a8b6", extraction_source["sha256"])
		self.assertIn(f"algorithm: {algorithm}", extraction_source["locator"])
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_catalog_reassigns_all_three_and_stub_is_deleted_normally(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		records = {item["id"]:item for item in catalog["drivers"]}
		for driver_id in OWN_DRIVERS:
			self.assertEqual(OWN_MACHINE, records[driver_id]["machine_id"])
			self.assertEqual("machines/partial/data-east/time-machine-1988.json", records[driver_id]["definition"])
		self.assertFalse((ROOT / "machines/stubs/tmac_a24.json").exists())
		self.assertFalse((ROOT / "knowledge/stubs/tmac_a24.md").exists())
		self.assertFalse(any(ROOT.rglob("*.disabled")))

	def test_catalog_derived_forbidden_identifier_guard(self) -> None:
		catalog = load_json(ROOT / "catalog/pinmame.json")
		paths = [DEFINITION_PATH,SEED_PATH,REPORT_PATH,REPORT_MD_PATH,KNOWLEDGE_PATH]
		artifact = "\n".join(path.read_text(encoding="utf-8") for path in paths)
		folded = artifact.casefold()
		identifier_tokens = set(re.findall(r"[a-z0-9]+(?:[._-][a-z0-9*]+)+", folded))
		other_machine_ids = {item["id"].casefold() for item in catalog["machines"] if item["id"] != OWN_MACHINE}
		other_driver_ids = {value.casefold() for item in catalog["drivers"] for value in (item.get("id"),item.get("root_driver")) if isinstance(value,str) and "_" in value and value not in OWN_DRIVERS}
		self.assertEqual(set(), identifier_tokens & (other_machine_ids | other_driver_ids))

		own_generations = set(re.findall(r"\bGEN_[A-Z0-9_]+\b", artifact))
		foreign_generations: set[str] = set()
		foreign_hardware: set[str] = set()
		foreign_table_builds: set[str] = set()
		own_hardware = self.definition["controller"]["hardware_generation"].casefold()
		own_tables = {value.casefold() for source in self.definition["sources"] if source.get("kind") == "vpx_table" for value in (source.get("id"),source.get("original_filename"),source.get("source_id"),source.get("sha256")) if isinstance(value,str)}
		for record in catalog["machines"]:
			if record["id"] == OWN_MACHINE: continue
			path = ROOT / record["definition"]
			if not path.is_file(): continue
			other = load_json(path)
			other_text = path.read_text(encoding="utf-8")
			foreign_generations.update(re.findall(r"\bGEN_[A-Z0-9_]+\b", other_text))
			hardware = other.get("controller",{}).get("hardware_generation")
			if isinstance(hardware,str) and hardware.casefold() != own_hardware: foreign_hardware.add(hardware.casefold())
			for source in other.get("sources",[]):
				if source.get("kind") != "vpx_table": continue
				for key in ("id","original_filename","source_id","sha256"):
					value = source.get(key)
					if isinstance(value,str) and value.casefold() not in own_tables: foreign_table_builds.add(value.casefold())
		self.assertEqual(set(), {value for value in foreign_generations - own_generations if value in artifact})
		self.assertEqual(set(), foreign_hardware & set(re.findall(r"\b0x[0-9a-f]+\b", folded)))
		self.assertEqual(set(), {value for value in foreign_table_builds if value in folded})

		conflict_ids = {item["id"].casefold() for item in self.definition["conflicts"]}
		self.assertEqual(set(), conflict_ids & {value.casefold() for value in PRIOR_CONFLICT_IDS})


class TimeMachineCuratorTests(unittest.TestCase):
	def test_curator_check_passes(self) -> None:
		environment = dict(os.environ)
		environment["PYTHONPATH"] = str(ROOT / "src")
		for _ in range(2):
			result = subprocess.run([sys.executable,str(ROOT / "tools/curate_time_machine.py"),"--check"],cwd=ROOT,env=environment,text=True,capture_output=True)
			self.assertEqual(0,result.returncode,result.stdout + result.stderr)

	def test_curator_check_fails_closed_for_configured_missing_evidence(self) -> None:
		with tempfile.TemporaryDirectory() as scratch:
			environment = dict(os.environ)
			environment["PYTHONPATH"] = str(ROOT / "src")
			environment["PINMAME_VPX_SOURCES_ROOT"] = scratch
			environment["PINMAME_MANUALS_ROOT"] = scratch
			result = subprocess.run([sys.executable,str(ROOT / "tools/curate_time_machine.py"),"--check"],cwd=ROOT,env=environment,text=True,capture_output=True)
			self.assertNotEqual(0,result.returncode)
			self.assertIn("evidence:",result.stdout + result.stderr)


class TimeMachineExternalEvidenceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.vpx_root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) if os.environ.get("PINMAME_VPX_SOURCES_ROOT") else None
		cls.manual_root = Path(os.environ["PINMAME_MANUALS_ROOT"]) if os.environ.get("PINMAME_MANUALS_ROOT") else None

	def test_retained_table_script_bounds_and_vpm_map_lights_idiom(self) -> None:
		if self.vpx_root is None: self.skipTest("retained VPX sources are not available")
		base = self.vpx_root / "data-east/time-machine-1988"
		extraction = base / "vpxtool-extract"
		table = base / "Time Machine (Data East 1988) v.2.4.1.vpx"
		self.assertEqual("b6c4b39bc7a672c1914b25e19192ec4cde8432aae00f9a5cd913c9b2f3c3c4f4", sha256(table))
		self.assertEqual("1ab7a5cfd7c6e55652a1fc4f9a28e05fd55e24b732b897355e0daec1a5602ee1", sha256(extraction / "script.vbs"))
		script = (extraction / "script.vbs").read_text(encoding="utf-8")
		active = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("'"))
		self.assertRegex(active, r'Const\s+cGameName\s*=\s*"tmac_a24"')
		self.assertRegex(active, r"(?i)\.HandleMechanics\s*=\s*0")
		self.assertRegex(active, r"(?i)vpmMapLights\s+AllLamps")
		self.assertNotRegex(active, r"(?i)Lampz\.MassAssign|\bSetLamp\b")
		self.assertNotRegex(active, r"(?i)(?:Sol|SolMod)Callback\((?:29|30|31|32)\)")
		gamedata = load_json(extraction / "gamedata.json")
		self.assertEqual((0.0,0.0,1000.0,1910.0), tuple(float(gamedata[key]) for key in ("left","top","right","bottom")))

		collections = load_json(extraction / "collections.json")
		all_lamps = next(item for item in collections if item["name"] == "AllLamps")
		self.assertEqual(134, len(all_lamps["items"]))
		items = {}
		for path in (extraction / "gameitems").glob("*.json"):
			kind,item = next(iter(load_json(path).items()))
			if isinstance(item.get("name"),str): items[item["name"]] = (kind,item)
		timers = {number:[] for number in range(1,66)}
		for name in all_lamps["items"]:
			kind,item = items[name]
			self.assertEqual("Light",kind)
			timers[int(item["timer_interval"])].append(name)
		self.assertTrue(all(timers[number] for number in range(1,65)))
		self.assertEqual(["l65"],timers[65])
		self.assertTrue(items["l65"][1]["is_backglass"])

	def test_extraction_manifest_recomputes_every_file(self) -> None:
		if self.vpx_root is None: self.skipTest("retained VPX sources are not available")
		extraction = self.vpx_root / "data-east/time-machine-1988/vpxtool-extract"
		manifest = load_json(MANIFEST_PATH)
		actual = [path.relative_to(extraction).as_posix() for path in sorted(path for path in extraction.rglob("*") if path.is_file())]
		self.assertEqual(actual,[item["path"] for item in manifest["files"]])
		for item in manifest["files"]:
			path = extraction / item["path"]
			self.assertEqual(item["bytes"],path.stat().st_size,item["path"])
			self.assertEqual(item["sha256"],sha256(path),item["path"])

	def test_retained_archive_manual_identity_hash_and_page_mapping(self) -> None:
		if self.manual_root is None: self.skipTest("retained manuals are not available")
		root = self.manual_root / "by-machine/data-east.time-machine.1988/archive-org"
		name = "Data_East_1988_Time_Machine_Manual.pdf"
		manual = root / name
		self.assertEqual(4_542_921,manual.stat().st_size)
		self.assertEqual("f232f8114ea31776a9d49e274b5ebed32cb3805acb4e719785fe48d43ddd719c",sha256(manual))
		metadata = load_json(root / "hashes.json")[name]
		self.assertEqual(78,metadata["page_count"])
		self.assertEqual(0,metadata["sampled_characters"])
		self.assertEqual("https://archive.org/download/Data_East_Time_Machine_Manual/Data_East_1988_Time_Machine_Manual.pdf",metadata["source_url"])
		self.assertEqual("https://archive.org/details/Data_East_Time_Machine_Manual",metadata["details_url"])
		self.assertEqual("Data_East_Time_Machine_Manual",metadata["source_id"])
		self.assertEqual("NOASSERTION",metadata["rights"])
		manifest = load_json(self.manual_root/"manifest.json")
		entries = [item for item in manifest["documents"] if item["machine_id"] == "data-east.time-machine.1988"]
		self.assertEqual(1,len(entries))
		entry = entries[0]
		self.assertEqual("archive.Data_East_Time_Machine_Manual.f232f8114ea3",entry["id"])
		self.assertEqual("f232f8114ea31776a9d49e274b5ebed32cb3805acb4e719785fe48d43ddd719c",entry["sha256"])
		self.assertEqual("https://archive.org/details/Data_East_Time_Machine_Manual",entry["source_url"])


if __name__ == "__main__":
	unittest.main()
