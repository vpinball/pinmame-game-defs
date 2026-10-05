from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "black-knight-2000-1989.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "black-knight-2000-1989.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "black-knight-2000-1989.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "black-knight-2000-1989.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "black-knight-2000-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "black-knight-2000-1989.md"
EXCERPT_ROOT = ROOT / "evidence" / "excerpts" / "williams.black-knight-2000.1989"
RUNTIME_ROOT = ROOT / "evidence" / "runtime" / "system-11"
L4_RUNTIME_PATH = RUNTIME_ROOT / "black-knight-2000-l4-service-and-mechanisms.json"
SET_RUNTIME_PATHS = {game: RUNTIME_ROOT / f"black-knight-2000-{game.removeprefix('bk2k_')}-coil-test.json" for game in ("bk2k_la2", "bk2k_lg3", "bk2k_pa5", "bk2k_pa7", "bk2k_pu1")}
SCENARIO_ROOT = ROOT / "tools" / "harness-scenarios" / "system-11"
PINNED_LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
S11_GAMES_PATH = "src/wpc/s11games.c"

DRIVER_IDS = {"bk2k_l4", "bk2k_la2", "bk2k_lg1", "bk2k_lg3", "bk2k_pa5", "bk2k_pa7", "bk2k_pf1", "bk2k_pu1"}
UNUSED_SWITCHES = {14, 15, 56, 60, 61, 62, 63, 64}
COIL_TEST_ORDER = [1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _address_allowed(address: int, rules: list[dict[str, int]]) -> bool:
	return any(("values" in rule and address in rule["values"]) or (rule.get("minimum", address + 1) <= address <= rule.get("maximum", address - 1)) for rule in rules)


def _point(device: dict[str, object]) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


class BlackKnight2000DefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(PARTIAL_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_identity_and_honest_partial_status(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.black-knight-2000.1989", machine["id"])
		self.assertEqual((1989, 311, "GrxPP-Ml91r", "physical_pinball"), (machine["year"], machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual(["conflict.upper-flipper-button"], [conflict["id"] for conflict in self.definition["conflicts"]])
		self.assertTrue(all("Resolution path:" in conflict["description"] for conflict in self.definition["conflicts"]))
		self.assertEqual("pinmame.system-11", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("bk2k_")})
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertNotIn("clone_of", drivers["bk2k_l4"])
		self.assertEqual({"identical"}, {drivers[driver_id]["physical_compatibility"] for driver_id in ("bk2k_l4", "bk2k_la2", "bk2k_lg1", "bk2k_lg3")})
		self.assertEqual({"compatible"}, {drivers[driver_id]["physical_compatibility"] for driver_id in ("bk2k_pa5", "bk2k_pa7", "bk2k_pf1", "bk2k_pu1")})
		machine = next(record for record in catalog["machines"] if record["id"] == "williams.black-knight-2000.1989")
		self.assertEqual("machines/partial/williams/black-knight-2000-1989.json", machine["definition"])

	def test_controller_profile_admits_every_binding(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		groups = {group["id"]: group for group in profile["groups"]}
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				group = groups[device["binding"]["group"]]
				self.assertTrue(_address_allowed(device["binding"]["device"], group["address_rules"]), device["id"])

	def test_switch_enumeration_and_rom_names(self) -> None:
		self.assertEqual({-7, -6, -5, -4} | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual({0}, set(self.dips))
		self.assertEqual(UNUSED_SWITCHES, {address for address, switch in self.switches.items() if switch["availability"] == "unused" and address <= 64})
		# FLIP_SWNO(58,57): public 82 is copied into 57 and 84 into 58; the rest of the flipper column is never read.
		self.assertEqual({82, 84}, {address for address in range(81, 89) if self.switches[address]["availability"] == "used"})
		self.assertIn("matrix switch 57", self.switches[82]["physical"]["notes"])
		self.assertIn("matrix switch 58", self.switches[84]["physical"]["notes"])
		for address in (81, 83):
			self.assertIn("does write this address when a staged flipper key is pressed", self.switches[address]["physical"]["notes"])
		self.assertEqual({5}, {address for address, switch in self.switches.items() if switch["availability"] == "optional"})
		for address in set(range(1, 60)) - {2, 14, 15, 56}:
			self.assertIn("The bk2k_l4 switch table names it", self.switches[address]["physical"]["notes"], address)
		self.assertEqual(["internal.ac-relay-feedback"], self.switches[2]["roles"])
		self.assertEqual(("Right Coin Chute", "Left Coin Chute"), (self.switches[4]["label"], self.switches[6]["label"]))
		self.assertEqual("Magna Save Button", self.switches[59]["label"])

	def test_script_start_up_writes_to_22_and_24_are_a_table_defect_not_a_conflict(self) -> None:
		for address in (22, 24):
			notes = self.switches[address]["physical"]["notes"]
			self.assertIn("close coin door", notes, address)
			self.assertIn("defect of the retained table", notes, address)
		self.assertNotIn("conflict.switch-22", {conflict["id"] for conflict in self.definition["conflicts"]})

	def test_manual_names_and_orders_agree_with_table_geometry(self) -> None:
		# Left-to-right and top-to-bottom orders the manual's matrix prints, checked against the retained table's objects.
		right_bank = [_point(self.switches[address]) for address in (41, 42, 43)]
		self.assertTrue(right_bank[0][0] < right_bank[1][0] < right_bank[2][0])
		left_bank = [_point(self.switches[address]) for address in (46, 45, 44)]
		self.assertTrue(left_bank[0][1] < left_bank[1][1] < left_bank[2][1])
		win = [_point(self.switches[address]) for address in (25, 26, 27)]
		self.assertTrue(win[0][0] < win[1][0] < win[2][0])
		war = [_point(self.switches[address]) for address in (28, 29, 30)]
		self.assertTrue(war[0][0] < war[1][0] < war[2][0])
		bonus = [_point(self.lamps[address]) for address in (36, 37, 38, 39, 40)]
		self.assertTrue(all(bonus[index][0] < bonus[index + 1][0] for index in range(4)))
		black = [_point(self.lamps[address]) for address in (12, 13, 14, 15, 16)]
		self.assertTrue(all(black[index][0] < black[index + 1][0] for index in range(4)))
		self.assertLess(_point(self.switches[39])[0], _point(self.switches[48])[0])
		self.assertLess(_point(self.switches[17])[0], _point(self.switches[19])[0])
		self.assertEqual(_point(self.switches[17]), _point(self.solenoids[17]))
		self.assertEqual(_point(self.switches[19]), _point(self.solenoids[19]))
		self.assertEqual(_point(self.switches[21]), _point(self.solenoids[21]))

	def test_public_solenoid_contract(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual({"flasher"}, {self.solenoids[address]["kind"] for address in range(25, 33)})
		self.assertEqual({"gi"}, {self.solenoids[address]["kind"] for address in (9, 10, 11)})
		self.assertEqual({"relay"}, {self.solenoids[address]["kind"] for address in (12, 16)})
		self.assertEqual("magnet", self.solenoids[15]["kind"])
		self.assertEqual({"unused"}, {self.solenoids[address]["availability"] for address in (5, 22)})
		self.assertEqual({"virtual"}, {self.solenoids[address]["kind"] for address in [23, 24, *range(33, 51)]})
		self.assertEqual("used", self.solenoids[23]["availability"])
		self.assertEqual({"used"}, {self.solenoids[address]["availability"] for address in range(45, 49)})
		self.assertEqual({"unused"}, {self.solenoids[address]["availability"] for address in [24, *range(33, 45), 49, 50]})
		self.assertEqual("cabinet.knocker", self.solenoids[14]["roles"][0])
		self.assertEqual(
			["relationship.ac-relay-switch-2", "relationship.flipper-column-82-to-matrix-57", "relationship.flipper-column-84-to-matrix-58"],
			[relationship["id"] for relationship in self.definition["relationships"]],
		)

	def test_flasher_bulb_counts_follow_the_printed_p_and_i_columns(self) -> None:
		printed = {25: (2, 2), 26: (2, 2), 27: (2, 2), 28: (2, 2), 29: (1, 2), 30: (2, 2), 31: (1, 2), 32: (1, 2)}
		playfield = 0
		insert = 0
		for address, (p, i) in printed.items():
			self.assertEqual(p + i, self.solenoids[address]["physical"]["quantity"], address)
			playfield += p
			insert += i
		# IPDB: 16 flash lamps in the backbox insert, in sync with the playfield flashers.
		self.assertEqual(16, insert)
		self.assertEqual(13, playfield)
		for address in (25, 26, 27, 30):
			self.assertEqual(1, len(self.solenoids[address]["spatial"]["placements"]), address)
		self.assertEqual(2, len(self.solenoids[28]["spatial"]["placements"]))

	def test_general_illumination_placements(self) -> None:
		self.assertEqual(23, len(self.solenoids[10]["spatial"]["placements"]))
		self.assertEqual(10, len(self.solenoids[11]["spatial"]["placements"]))
		self.assertEqual(("not_applicable", "cabinet_or_service"), (self.solenoids[9]["spatial"]["status"], self.solenoids[9]["spatial"]["reason"]))

	def test_lamps(self) -> None:
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		for address in (1, 2, 3, 4, 6, 7):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		for address in set(range(1, 65)) - {1, 2, 3, 4, 6, 7}:
			self.assertEqual("observed", self.lamps[address]["spatial"]["status"], address)
		# The bolt circle (lamps 49-64) goes around lamp 5, the center: every ring lamp lies within 200 table units of it (the ring's radius is about 150).
		center = _point(self.lamps[5])
		for address in range(49, 65):
			x, y = _point(self.lamps[address])
			self.assertLess((((x - center[0]) * 954.0) ** 2 + ((y - center[1]) * 2052.0) ** 2) ** 0.5, 200.0, address)

	def test_lightning_wheel_order_matches_the_operator_message(self) -> None:
		order = [
			("EXTRA BALL", 49), ("50,000", 50), ("MAGNA SAVE", 51), ("10,000", 52), ("MULTI-BALL", 53), ("100,000", 54), ("RANSOM", 55),
			("200,000", 56), ("SPECIAL", 57), ("20,000", 58), ("KICKBACK", 59), ("150,000", 60), ("Drawbridge", 61), ("75,000", 62),
			("HURRY-UP", 63), ("250,000", 64),
		]
		for text, address in order:
			self.assertIn(text, self.lamps[address]["physical"]["notes"], address)
		message = " ".join((EXCERPT_ROOT / "operator-message.md").read_text(encoding="utf-8").split())
		positions = [message.index(text) for text in ("award EXTRA BALL", "50,000 points, light MAGNA-SAVE", "10,000 points, MULTI-BALL", "100,000 points", "R-A-N-S-O-M letter advance", "200,000 points, SPECIAL", "20,000 points", "KICKBACK (if", "150,000 points", "DRAWBRIDGE down", "75,000", "lights HURRY UP", "250,000")]
		self.assertEqual(sorted(positions), positions)

	def test_upper_flipper_conflict_names_every_source_and_resolution(self) -> None:
		conflict = self.definition["conflicts"][0]
		for text in ("2J10-4", "2J8-12", "Upr Left Flipper Button", "No Connection", "SW-1A-183", "SolRFlipper", "Resolution path:"):
			self.assertIn(text, conflict["description"], text)
		excerpt = (EXCERPT_ROOT / "flipper-wiring.md").read_text(encoding="utf-8")
		for text in ("| 2J8-12 | --- | No Connection |", "| 2J10-4 | --- | No Connection |", "| 26 | SW-1A-183 | Flipper Switch |", "Upr Left Flipper Button"):
			self.assertIn(text, excerpt, text)

	def test_every_device_is_spatially_recorded(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			if device["id"] in {"switch.matrix-11", "switch.matrix-12", "switch.matrix-13"}:
				self.assertNotIn("spatial", device)
				continue
			self.assertIn("spatial", device, device["id"])

	def test_seed_and_curator_are_deterministic(self) -> None:
		self.assertEqual(PARTIAL_PATH.read_bytes(), SEED_PATH.read_bytes())
		import curate_black_knight_2000 as curator

		curator.check(ROOT)

	def test_spatial_blockers_match_curator(self) -> None:
		import curate_black_knight_2000 as curator

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual([{"group": "pinmame.input.switch", "address": address} for address in (11, 12, 13)], report["unresolved"])
		self.assertEqual([25, 26, 27, 30], [entry["address"] for entry in report["partly_placed"]])
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_committed_excerpts_exist_hash_match_and_fit_budget(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["id"] == "manual.williams.black-knight-2000.operations")
		self.assertEqual(9, len(manual["excerpts"]))
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				self.assertTrue(excerpt["reviewed"])
				if "image" in excerpt:
					image = ROOT / excerpt["image"]
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image.read_bytes()).hexdigest(), excerpt["image"])

	def test_switch_matrix_and_lamp_matrix_excerpts_match_definition_labels(self) -> None:
		switch_text = (EXCERPT_ROOT / "switch-matrix.md").read_text(encoding="utf-8")
		for address in (16, 24, 31, 32, 40, 47, 59):
			self.assertIn(f" {address} |", switch_text, address)
		lamp_text = (EXCERPT_ROOT / "lamp-matrix.md").read_text(encoding="utf-8")
		for address in (19, 47, 48, 61, 63, 64):
			self.assertIn(f" {address} |", lamp_text, address)

	def test_playfield_dimensions_follow_the_retained_table_bounds(self) -> None:
		self.assertEqual({"width": 954.0, "height": 2052.0, "units": "vpx"}, self.definition["machine"]["playfield"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual({"left": 0.0, "top": 0.0, "right": 954.0, "bottom": 2052.0}, report["coordinate_convention"]["source_bounds"])
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			if spatial and spatial["status"] != "not_applicable":
				for placement in spatial["placements"]:
					self.assertTrue(0.0 <= placement["x"] <= 1.0 and 0.0 <= placement["y"] <= 1.0, device["id"])

	def test_knowledge_note_is_reproduced_by_the_curator(self) -> None:
		import curate_black_knight_2000 as curator

		self.assertEqual(curator.KNOWLEDGE_TEXT, KNOWLEDGE_PATH.read_text(encoding="utf-8"))
		self.assertIn("Coverage: **partial**", curator.KNOWLEDGE_TEXT)
		self.assertNotIn("also lights lamps 19 and 51", curator.KNOWLEDGE_TEXT)

	def test_rom_name_table_excerpt_matches_curator(self) -> None:
		import curate_black_knight_2000 as curator

		text = (EXCERPT_ROOT / "rom-name-tables.md").read_text(encoding="utf-8")
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f"| {address} | {name.replace(chr(34), 'z')} |", text, address)
		for address in (2, 14, 15, 56):
			self.assertIn(f"| {address} | (blank) |", text, address)
			self.assertNotIn(address, curator.ROM_SWITCH_NAMES)
		for entry, address in enumerate(COIL_TEST_ORDER, start=1):
			self.assertIn(f"| {entry} | {curator.ROM_COIL_NAMES[address]} | {address} |", text, address)
		self.assertEqual(set(COIL_TEST_ORDER), set(curator.ROM_COIL_NAMES))
		self.assertIn("| bk2k_lg3 | switch | 41 | RIGHT 3-BANK 1 | G |", text)
		self.assertIn("| bk2k_la2 | both | - | (no difference) | (no difference) |", text)

	def test_switches_the_rom_names_are_normally_open_and_others_say_nothing(self) -> None:
		import curate_black_knight_2000 as curator

		for address, device in self.switches.items():
			if address < 0:
				continue
			if address in curator.ROM_SWITCH_NAMES:
				self.assertIs(False, device["normally_closed"], address)
				self.assertIn("l4-switch-levels", device["physical"]["notes"], address)
			else:
				self.assertNotIn("normally_closed", device, address)
		for address in (41, 42, 43, 44, 45, 46):
			self.assertIn("Drop-target polarity", self.switches[address]["physical"]["notes"], address)
		for address in (14, 15, 56):
			self.assertIn("no name", self.switches[address]["physical"]["notes"], address)
		for address in (60, 61, 62, 63, 64):
			self.assertIn("does not read this position", self.switches[address]["physical"]["notes"], address)

	def test_lamp_notes_cite_the_roms_single_lamp_names(self) -> None:
		import curate_black_knight_2000 as curator

		self.assertEqual(set(range(1, 65)), set(curator.ROM_LAMP_NAMES))
		for address, device in self.lamps.items():
			self.assertIn(f"'{curator.ROM_LAMP_NAMES[address]}'", device["physical"]["notes"], address)
			self.assertIn("runtime.black-knight-2000.l4-service-and-mechanisms", device["provenance"]["source_refs"], address)

	def test_runtime_evidence_pins_the_coil_test_and_the_power_up_and_drop_target_runs(self) -> None:
		evidence = load_json(L4_RUNTIME_PATH)
		self.assertEqual(["williams.black-knight-2000.1989"], evidence["machine_ids"])
		runtime = evidence["runtime"]
		self.assertEqual("bk2k_l4", runtime["game"])
		self.assertEqual(PINMAME_REVISION, runtime["emulator"]["built_from_revision"])
		self.assertEqual(PINNED_LIBRARY_SHA256, runtime["emulator"]["sha256"])
		observations = runtime["observations"]
		self.assertEqual(COIL_TEST_ORDER, observations["ordered_solenoid_on_sequence"])
		self.assertEqual(28, len(runtime["raw_runs"]))
		for run in runtime["raw_runs"]:
			scenario = ROOT / run["scenario_path"]
			self.assertEqual(SCENARIO_ROOT, scenario.parent)
			self.assertEqual(run["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest(), run["name"])
		runs = observations["runs"]
		self.assertIn("Attract mode (Game Over mode) observed 12 s: solenoids 3 and 4 fired 0 and 0 time(s)", runs["l4-droptargets-left-bank-1"]["note"])
		self.assertIn("pulsed at [0.17, 1.34, 2.32] s and the right 3-bank reset (4) never", runs["l4-droptargets-left-bank-1"]["note"])
		self.assertIn("the left 3-bank reset (3) pulsed never and the right 3-bank reset (4) at [0.16, 1.31, 2.31] s", runs["l4-droptargets-right-bank-1"]["note"])
		for name in ("l4-boot-outhole-10", "l4-boot-popper-47", "l4-boot-right-eject-40", "l4-boot-upf-lock-36-38"):
			self.assertIn("one pulse", runs[name]["note"], name)
		for other in SET_RUNTIME_PATHS.values():
			other_evidence = load_json(other)
			self.assertEqual(COIL_TEST_ORDER, other_evidence["runtime"]["observations"]["ordered_solenoid_on_sequence"], other.name)
			self.assertEqual(PINNED_LIBRARY_SHA256, other_evidence["runtime"]["emulator"]["sha256"], other.name)
			self.assertEqual(2, len(other_evidence["runtime"]["raw_runs"]), other.name)

	def test_runtime_evidence_records_the_roms_lamp_names_and_flipper_synthetic_outputs(self) -> None:
		import curate_black_knight_2000 as curator

		observations = load_json(L4_RUNTIME_PATH)["runtime"]["observations"]
		note = observations["runs"]["l4-single-lamps"]["note"]
		for address, name in curator.ROM_LAMP_NAMES.items():
			self.assertIn(f"{address}={name}", note, address)
		self.assertEqual(list(range(1, 65)), observations["lamp_addresses_seen"])
		for address in (45, 46, 47, 48):
			self.assertIn(address, observations["solenoid_addresses_seen"])
		for address in (24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertNotIn(address, observations["solenoid_addresses_seen"])
		for address in (45, 47):
			self.assertIn("raised", self.solenoids[address]["physical"]["notes"], address)

	def test_motor_bank_note_does_not_claim_a_physical_direction(self) -> None:
		import curate_black_knight_2000 as curator

		self.assertIn("do not establish which physical end each switch marks", curator.DRAWBRIDGE_BEHAVIOR)
		mechanism = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.drawbridge-targets")
		self.assertIn("MOTOR BANK TEST", mechanism["behavior"])
		self.assertIn("do not establish which physical end each switch marks", mechanism["behavior"])
		for identifier in ("mechanism.left-drop-targets", "mechanism.right-drop-targets"):
			bank = next(item for item in self.definition["mechanisms"] if item["id"] == identifier)
			self.assertIn("three times", bank["behavior"], identifier)


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root not configured")
class BlackKnight2000RetainedTableTests(unittest.TestCase):
	def pinned_extraction_hashes(self) -> dict[str, str]:
		"""Map each extracted file to its SHA-256, read from the manifest only once its pinned digest matches.

		The tests that read extracted files check each one against this map first, so a stale or partial
		local extraction fails as a named hash mismatch instead of surfacing as a KeyError or a missing
		gameitem. test_retained_extraction_matches_manifest is what proves the whole tree.
		"""
		import curate_black_knight_2000 as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		manifest = load_json(Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve() / curator.EXTRACTION_MANIFEST_RELATIVE_PATH)
		self.assertEqual(curator.EXTRACTION_MANIFEST_SHA256, hashlib.sha256(canonical_bytes(manifest)).hexdigest(), "retained extraction manifest is not the pinned one")
		return {item["path"]: item["sha256"] for item in manifest["files"]}

	def read_retained(self, hashes: dict[str, str], relative_path: str) -> bytes:
		import curate_black_knight_2000 as curator

		self.assertTrue(relative_path in hashes, f"the pinned extraction manifest has no {relative_path}")
		data = (Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve() / curator.EXTRACTION_RELATIVE_PATH / relative_path).read_bytes()
		self.assertEqual(hashes[relative_path], hashlib.sha256(data).hexdigest(), f"retained {relative_path} does not match its SHA-256 in the pinned extraction manifest")
		return data

	def test_retained_extraction_matches_manifest(self) -> None:
		import curate_black_knight_2000 as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve()
		curator.verify_extraction_manifest(root)
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())

	def test_retained_script_start_up_block_and_flipper_hooks(self) -> None:
		text = self.read_retained(self.pinned_extraction_hashes(), "script.vbs").decode("latin-1")
		self.assertIn("Const cGameName = \"bk2k_l4\"", text)
		self.assertIn(".Switch(22) = 1 'close coin door", text)
		self.assertIn(".Switch(24) = 1 'and keep it close", text)
		self.assertIn("SolCallback(sLRFlipper) = \"SolRFlipper\"", text)
		self.assertIn("URightFlipper.RotateToEnd", text)
		for absent in ("NoUpperLeftFlipper", "NoUpperRightFlipper", "cSingleLFlip", "cSingleRFlip"):
			self.assertNotIn(absent, text)

	def test_retained_table_object_positions_match_the_curator(self) -> None:
		import curate_black_knight_2000 as curator

		hashes = self.pinned_extraction_hashes()
		for address, (name, x, y) in curator.SWITCH_POSITIONS.items():
			kind, _, object_name = name.partition(".")
			if kind not in ("Trigger", "Kicker", "Bumper", "HitTarget"):
				continue
			body = json.loads(self.read_retained(hashes, f"gameitems/{kind}.{object_name}.json"))[kind]
			raw_x, raw_y = (body["position"]["x"], body["position"]["y"]) if kind == "HitTarget" else (body["center"]["x"], body["center"]["y"])
			self.assertAlmostEqual(raw_x / curator.TABLE_WIDTH, x, places=6, msg=str(address))
			self.assertAlmostEqual(raw_y / curator.TABLE_HEIGHT, y, places=6, msg=str(address))
		for address, (name, x, y) in curator.LAMP_POSITIONS.items():
			body = json.loads(self.read_retained(hashes, f"gameitems/Light.{name}.json"))["Light"]
			self.assertAlmostEqual(body["center"]["x"] / curator.TABLE_WIDTH, x, places=6, msg=str(address))
			self.assertAlmostEqual(body["center"]["y"] / curator.TABLE_HEIGHT, y, places=6, msg=str(address))
		bounds = json.loads(self.read_retained(hashes, "gamedata.json"))
		self.assertEqual((0.0, 0.0, curator.TABLE_WIDTH, curator.TABLE_HEIGHT), (bounds["left"], bounds["top"], bounds["right"], bounds["bottom"]))


@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
class BlackKnight2000RetainedManualTests(unittest.TestCase):
	def test_retained_manual_hashes(self) -> None:
		import curate_black_knight_2000 as curator

		root = Path(os.environ["PINMAME_MANUALS_ROOT"]).resolve() / "by-machine" / curator.MACHINE_ID / "ipdb-311"
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256((root / "Williams_1989_Black_Knight_2000_Operations_Manual.pdf").read_bytes()).hexdigest())
		self.assertEqual(curator.MANUAL_APRIL_SHA256, hashlib.sha256((root / "Williams_1989_Black_Knight_2000_Manual.pdf").read_bytes()).hexdigest())
		self.assertEqual(curator.OPERATOR_SHA256, hashlib.sha256((root / "Williams_1989_Black_Knight_2000_An_Important_Message_To_Operators.pdf").read_bytes()).hexdigest())


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts root not configured")
class BlackKnight2000RetainedRuntimeTests(unittest.TestCase):
	@staticmethod
	def stage() -> Path:
		return Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "williams.black-knight-2000.1989" / "runtime-stage"

	def test_retained_raw_runs_match_evidence_hashes(self) -> None:
		stage = self.stage()
		for game, evidence_path in {"bk2k_l4": L4_RUNTIME_PATH, **SET_RUNTIME_PATHS}.items():
			evidence = load_json(evidence_path)
			directory = stage / "raw-runs" / game
			self.assertEqual(evidence["source"]["sha256"], hashlib.sha256((directory / "manifest.json").read_bytes()).hexdigest(), game)
			for run in evidence["runtime"]["raw_runs"]:
				self.assertEqual(run["sha256"], hashlib.sha256((directory / f"{run['name']}.json").read_bytes()).hexdigest(), run["name"])

	def test_committed_runtime_evidence_rederives_from_raw_runs(self) -> None:
		import bk2k_summarize_runtime_evidence as summarizer
		from pinmame_game_defs.jsonio import canonical_bytes

		for game, evidence_path in {"bk2k_l4": L4_RUNTIME_PATH, **SET_RUNTIME_PATHS}.items():
			_, evidence, _ = summarizer.build_driver_evidence(game)
			self.assertEqual(evidence_path.read_bytes(), canonical_bytes(evidence), game)

	def test_retained_rom_name_tables_match_curator(self) -> None:
		import curate_black_knight_2000 as curator

		tables = load_json(self.stage() / "rom-name-tables" / "bk2k_l4.json")
		self.assertEqual(curator.ROM_SWITCH_NAMES, {entry["index"]: entry["text"].replace("z", chr(34)) if entry["index"] in range(25, 31) else entry["text"] for entry in tables["switch_table"]["entries"][:59] if entry["text"]})
		self.assertEqual([curator.ROM_COIL_NAMES[address] for address in COIL_TEST_ORDER], [entry["text"] for entry in tables["coil_table"]["entries"][:30]])

	def test_pinned_library_build_matches_runtime_evidence(self) -> None:
		library = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve().parent / "builds" / "pinmame-8371478" / "Release" / "pinmame64.dll"
		if not library.is_file():
			self.skipTest(f"pinned library build not present: {library}")
		self.assertEqual(PINNED_LIBRARY_SHA256, hashlib.sha256(library.read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
