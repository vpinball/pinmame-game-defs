from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "earthshaker-1989.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "earthshaker-1989.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "earthshaker-1989.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "earthshaker-1989.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-11.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "earthshaker-1989.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "earthshaker-1989.md"
LA3_RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "earthshaker-la3-service-and-mechanisms.json"
PA1_RUNTIME_PATH = ROOT / "evidence" / "runtime" / "system-11" / "earthshaker-pa1-prototype-service.json"

DRIVER_IDS = {"esha_la3", "esha_l4c", "esha_ma3", "esha_pr4", "esha_lg1", "esha_lg2", "esha_la1", "esha_pa4", "esha_pa1"}
UNUSED_SWITCHES = {47, 48, 49, 51, 59, 60, 61, 62, 63, 64}
# The pinned LibPinMAME build (revision 8371478a) and the ROM archives the runtime evidence was produced from.
PINNED_LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
ROM_ARCHIVE_SHA256 = {
	"esha_la3": "8340ada861b121e4426d53f9b6835ccdd091b5af9e6bc39631317d637ca251d4",
	"esha_pa1": "695d4113ae93d7e14da04d4111850f30edc60351df84a2fd8da6925c595461a8",
}
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


class EarthshakerDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(PARTIAL_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_identity_and_honest_partial_status(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.earthshaker.1989", machine["id"])
		self.assertEqual((1989, 753, "GRw0r-Mp42p", "physical_pinball"), (machine["year"], machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement", "variant_differences"], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.system-11", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("esha_")})
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertNotIn("clone_of", drivers["esha_la3"])
		self.assertEqual({"compatible"}, {drivers[driver_id]["physical_compatibility"] for driver_id in ("esha_pa1", "esha_pa4")})
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver_id, driver in drivers.items() if driver_id not in ("esha_pa1", "esha_pa4")})
		self.assertIn("BUILDING MOTOR", drivers["esha_pa1"]["variant_notes"])
		machine = next(record for record in catalog["machines"] if record["id"] == "williams.earthshaker.1989")
		self.assertEqual("machines/partial/williams/earthshaker-1989.json", machine["definition"])

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
			self.assertIn("this table never writes the address", self.switches[address]["physical"]["notes"])
		self.assertEqual({5, 25, 26}, {address for address, switch in self.switches.items() if switch["availability"] == "optional"})
		for address in range(1, 59):
			self.assertIn("esha_la3 switch table names it", self.switches[address]["physical"]["notes"], address)
		self.assertIn("BLDNG. 1 UNUSED", self.switches[25]["physical"]["notes"])
		self.assertEqual(["internal.ac-relay-feedback"], self.switches[2]["roles"])
		self.assertFalse(any(switch.get("normally_closed") for switch in self.switches.values()))
		self.assertEqual(("Right Coin Chute", "Left Coin Chute"), (self.switches[4]["label"], self.switches[6]["label"]))

	def test_drop_target_optos_follow_rom_polarity(self) -> None:
		for address in (27, 28, 29):
			switch = self.switches[address]
			self.assertEqual("opto", switch["physical"]["switch_type"])
			self.assertFalse(switch["normally_closed"])
			self.assertIn("seven times", switch["physical"]["notes"])
		left, center, right = (_point(self.switches[address]) for address in (27, 28, 29))
		self.assertLess(left[0], center[0])
		self.assertLess(center[0], right[0])

	def test_jet_bumpers_follow_manual_not_script(self) -> None:
		top, right, left = (_point(self.switches[address]) for address in (54, 53, 52))
		self.assertLess(top[1], right[1])
		self.assertLess(top[1], left[1])
		self.assertLess(left[0], right[0])
		self.assertEqual(_point(self.switches[54]), _point(self.solenoids[21]))
		self.assertEqual(_point(self.switches[53]), _point(self.solenoids[19]))
		self.assertEqual(_point(self.switches[52]), _point(self.solenoids[17]))
		lamp_top, lamp_left, lamp_right = (_point(self.lamps[address]) for address in (41, 42, 43))
		self.assertLess(lamp_top[1], lamp_left[1])
		self.assertLess(lamp_left[0], lamp_right[0])
		self.assertIn("swaps 52 and 54", self.switches[52]["physical"]["notes"])

	def test_public_solenoid_contract(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual({"flasher"}, {self.solenoids[address]["kind"] for address in range(25, 33)})
		self.assertEqual({"gi"}, {self.solenoids[address]["kind"] for address in (10, 11, 15)})
		self.assertEqual("relay", self.solenoids[12]["kind"])
		self.assertEqual("motor", self.solenoids[22]["kind"])
		self.assertEqual(["cabinet.shaker"], self.solenoids[22]["roles"])
		self.assertEqual("unused", self.solenoids[8]["availability"])
		self.assertEqual(("relay", "optional"), (self.solenoids[9]["kind"], self.solenoids[9]["availability"]))
		self.assertEqual(("not_applicable", "internal_nonvisual"), (self.solenoids[9]["spatial"]["status"], self.solenoids[9]["spatial"]["reason"]))
		self.assertEqual({"virtual"}, {self.solenoids[address]["kind"] for address in [23, 24, *range(33, 51)]})
		self.assertEqual("used", self.solenoids[23]["availability"])
		self.assertEqual({"used"}, {self.solenoids[address]["availability"] for address in range(45, 49)})
		self.assertEqual({2}, {self.solenoids[address]["physical"]["quantity"] for address in (14, 16, 26, 27, 32)})
		self.assertEqual({1}, {self.solenoids[address]["physical"]["quantity"] for address in (25, 28, 29, 30, 31)})
		self.assertEqual(2, len(self.solenoids[32]["spatial"]["placements"]))
		for address in (14, 16, 26, 27):
			self.assertEqual(1, len(self.solenoids[address]["spatial"]["placements"]), address)
		self.assertEqual(
			["relationship.ac-relay-switch-2", "relationship.flipper-column-82-to-matrix-57", "relationship.flipper-column-84-to-matrix-58"],
			[relationship["id"] for relationship in self.definition["relationships"]],
		)

	def test_right_ramp_flashers_follow_the_coil_drawing(self) -> None:
		upper, lower = sorted((placement["y"], placement["x"]) for placement in self.solenoids[32]["spatial"]["placements"])
		ramp_2, ramp_1 = _point(self.solenoids[31]), _point(self.solenoids[30])
		self.assertLess(upper[0], lower[0])
		self.assertLess(lower[0], ramp_2[1])
		self.assertLess(ramp_2[1], ramp_1[1])

	def test_general_illumination_placements(self) -> None:
		self.assertEqual(13, len(self.solenoids[10]["spatial"]["placements"]))
		self.assertEqual(18, len(self.solenoids[15]["spatial"]["placements"]))
		self.assertEqual(("not_applicable", "cabinet_or_service"), (self.solenoids[11]["spatial"]["status"], self.solenoids[11]["spatial"]["reason"]))

	def test_lamps(self) -> None:
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		for address in range(58, 65):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		# Windows share one point per column (rows differ only in height), and the columns run left to right.
		columns = [{_point(self.lamps[address]) for address in column} for column in ((17, 20, 23), (18, 21, 24), (19, 22, 25))]
		self.assertEqual([1, 1, 1], [len(column) for column in columns])
		left, centre, right = (next(iter(column)) for column in columns)
		self.assertLess(left[0], centre[0])
		self.assertLess(centre[0], right[0])
		# The shared point is the window primitives' origin, not a socket, so it must not claim validation.
		for address in range(17, 26):
			spatial = self.lamps[address]["spatial"]
			self.assertEqual("observed", spatial["status"], address)
			self.assertEqual({"observed"}, {placement["provenance"]["status"] for placement in spatial["placements"]}, address)
		for address in (25, 26):
			self.assertEqual("observed", self.switches[address]["spatial"]["status"], address)
			self.assertNotIn("normally_closed", self.switches[address], address)
		for address in (49, 57):
			self.assertIn("bulb-cover", self.lamps[address]["physical"]["notes"], address)
		self.assertIn("zone-8 marker", self.lamps[16]["physical"]["notes"])
		self.assertEqual("Building Window 1", self.lamps[23]["label"])
		self.assertEqual("Building Window 9", self.lamps[19]["label"])
		captive = [_point(self.lamps[address]) for address in range(1, 6)]
		self.assertTrue(all(captive[index][1] > captive[index + 1][1] for index in range(4)))

	def test_flipper_inputs_point_consumers_at_82_and_84(self) -> None:
		self.assertIn("through public 82", self.switches[57]["physical"]["notes"])
		self.assertIn("through public 84", self.switches[58]["physical"]["notes"])
		flippers = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.flippers")
		self.assertIn("82 (right) and 84 (left)", json.dumps(flippers))

	def test_game_on_enable_follows_the_harness_order(self) -> None:
		# The note's on/off/on order must match the committed summaries of the game-start runs.
		note = self.solenoids[23]["physical"]["notes"]
		self.assertLess(note.index("already on"), note.index("goes off"))
		self.assertLess(note.index("goes off"), note.index("comes back on"))
		runs = load_json(LA3_RUNTIME_PATH)["runtime"]["observations"]["runs"]
		for name in ("drop-targets-down", "drop-targets-up"):
			summary = runs[name]["note"]
			game_over = float(summary.split("Game-Over mode entered ")[1].split("s")[0])
			started = float(summary.split("Start pressed by ")[1].split("s")[0])
			first_sample = float(summary.split("first solenoid sample ")[1].split("s")[0])
			spans = summary.split("Game-on enable (23) on-spans: ")[1].split(" (first")[0].split(", ")
			self.assertEqual(2, len(spans), name)
			first_on, first_off = (float(value) for value in spans[0].rstrip("s").split("-"))
			self.assertEqual(first_sample, first_on, name)
			self.assertLess(first_on, game_over, name)
			self.assertGreater(first_off, game_over, name)
			self.assertLess(first_off - game_over, 2.0, name)
			self.assertTrue(spans[1].endswith("s-end"), name)
			self.assertGreater(float(spans[1].split("s-end")[0]), started, name)

	def test_every_device_is_spatially_recorded(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			self.assertIn("spatial", device, device["id"])

	def test_seed_and_curator_are_deterministic(self) -> None:
		self.assertEqual(PARTIAL_PATH.read_bytes(), SEED_PATH.read_bytes())
		import curate_earthshaker as curator

		curator.check(ROOT)

	def test_spatial_blockers_match_curator(self) -> None:
		import curate_earthshaker as curator

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual([14, 16, 26, 27], [entry["address"] for entry in report["partly_placed"]])
		self.assertEqual([[25, 26], list(range(17, 26))], [entry["addresses"] for entry in report["observed_only"]])
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_committed_excerpts_exist_hash_match_and_fit_budget(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["kind"] == "manual")
		self.assertEqual(9, len(manual["excerpts"]))
		self.assertIn("excerpt.earthshaker.game-play", {excerpt["id"] for excerpt in manual["excerpts"]})
		rom = next(source for source in self.definition["sources"] if source["kind"] == "rom_static_analysis")
		for excerpt in manual["excerpts"] + rom["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
			self.assertTrue(excerpt["reviewed"])
			if "image" in excerpt:
				image = ROOT / excerpt["image"]
				self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image.read_bytes()).hexdigest(), excerpt["image"])
				self.assertLessEqual(image.stat().st_size, 100_000, excerpt["image"])

	def test_rom_name_table_excerpt_matches_definition(self) -> None:
		import curate_earthshaker as curator

		text = (ROOT / "evidence" / "excerpts" / "williams.earthshaker.1989" / "rom-name-tables.md").read_text(encoding="utf-8")
		for address, name in curator.ROM_SWITCH_NAMES.items():
			self.assertIn(f"| {address} | {name} |", text, address)
		for address, name in curator.ROM_COIL_NAMES.items():
			self.assertIn(f"| {name} | {address} |", text, address)
		self.assertIn("| esha_pa1 | coil | 17 | UNUSED | BUILDING MOTOR |", text)

	def test_runtime_evidence_records_coil_test_and_drop_targets(self) -> None:
		la3 = load_json(LA3_RUNTIME_PATH)
		self.assertEqual(["williams.earthshaker.1989"], la3["machine_ids"])
		runtime = la3["runtime"]
		self.assertEqual("esha_la3", runtime["game"])
		self.assertEqual("8371478a7640f1896dcdf565aed340dc5df989ba", runtime["emulator"]["built_from_revision"])
		runs = runtime["observations"]["runs"]
		self.assertEqual(COIL_TEST_ORDER, runs["burnin-coil-test"]["ordered_solenoid_on_sequence"])
		self.assertIn("22=QUAKE MOTOR", runs["burnin-coil-test"]["note"])
		self.assertIn("9=UNUSED", runs["burnin-coil-test"]["note"])
		self.assertIn("fired 7 time(s) between Game-Over entry and Start and 7 time(s) after Start", runs["drop-targets-down"]["note"])
		self.assertIn("fired 1 time(s) between Game-Over entry and Start and 1 time(s) after Start", runs["drop-targets-up"]["note"])
		self.assertEqual(15, len(runtime["raw_runs"]))
		self.assertEqual(PINNED_LIBRARY_SHA256, runtime["emulator"]["sha256"])
		self.assertEqual(ROM_ARCHIVE_SHA256["esha_la3"], runtime["rom_archive_sha256"])
		pa1 = load_json(PA1_RUNTIME_PATH)
		pa1_runs = pa1["runtime"]["observations"]["runs"]
		self.assertEqual(PINNED_LIBRARY_SHA256, pa1["runtime"]["emulator"]["sha256"])
		self.assertEqual(ROM_ARCHIVE_SHA256["esha_pa1"], pa1["runtime"]["rom_archive_sha256"])
		self.assertEqual(COIL_TEST_ORDER, pa1_runs["burnin-coil-test"]["ordered_solenoid_on_sequence"])
		self.assertIn("17:9=BUILDING MOTOR", pa1_runs["burnin-coil-test"]["note"])

	def test_building_model_runs_ignore_the_first_change_then_stop_on_25_fall_or_26_rise(self) -> None:
		runs = load_json(LA3_RUNTIME_PATH)["runtime"]["observations"]["runs"]
		models = {name: run["note"] for name, run in runs.items() if name.startswith("building-model")}
		self.assertEqual(9, len(models))
		accepted: list[tuple[float, bool]] = []
		ignored_first_stop_edges: list[float] = []
		for name, note in models.items():
			released = float(note.split("released ")[1].split("s later")[0])
			presented = note.split("while it ran (time after 9 on, (25,26) before->after): ")[1].rstrip(".").split(", ")
			changes = []
			for change in presented:
				elapsed = float(change.split("s ")[0])
				before, after = change.split("(")[1].rstrip(")").split("->")
				if before != after:
					changes.append((elapsed, (before[0] == "1" and after[0] == "0") or (before[1] == "0" and after[1] == "1")))
			self.assertGreaterEqual(len(changes), 2, name)
			# The first change never stops the motor, whatever it is.
			self.assertGreaterEqual(released - changes[0][0], 0.15, name)
			if changes[0][1]:
				ignored_first_stop_edges.append(changes[0][0])
			# After it, the motor stops within about 0.1 s of the first 25 fall or 26 rise, and on nothing else.
			stop = next(change for change in changes[1:] if change[1])
			self.assertLess(released - stop[0], 0.12, name)
			self.assertEqual(stop, changes[-1], name)
			accepted.append((stop[0], changes[0][1]))
		# The two runs that separate this rule from a run-time threshold.
		self.assertLess(min(elapsed for elapsed, _ in accepted), 1.0)
		self.assertGreater(max(ignored_first_stop_edges), 2.0)


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root not configured")
class EarthshakerRetainedTableTests(unittest.TestCase):
	def test_retained_extraction_matches_manifest(self) -> None:
		import curate_earthshaker as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve()
		curator.verify_extraction_manifest(root)
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())

	def test_retained_script_still_swaps_top_and_left_bumper_switches(self) -> None:
		import curate_earthshaker as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve()
		text = (root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs").read_text(encoding="latin-1")
		self.assertIn("Sub Bumper1_Hit : vpmTimer.PulseSw(52)", text)
		self.assertIn("Sub Bumper3_Hit : vpmTimer.PulseSw(54)", text)
		self.assertIn('Const cGameName="esha_la3"', text)


@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
class EarthshakerRetainedManualTests(unittest.TestCase):
	def test_retained_manual_hash(self) -> None:
		import curate_earthshaker as curator

		path = Path(os.environ["PINMAME_MANUALS_ROOT"]).resolve() / "by-machine" / curator.MACHINE_ID / "earthshaker.pdf"
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256(path.read_bytes()).hexdigest())


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts root not configured")
class EarthshakerRetainedRuntimeTests(unittest.TestCase):
	def test_retained_raw_runs_match_evidence_hashes(self) -> None:
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "earthshaker"
		for evidence_path, directory, game in ((LA3_RUNTIME_PATH, "harness-runs-la3", "esha_la3"), (PA1_RUNTIME_PATH, "harness-runs-pa1", "esha_pa1")):
			evidence = load_json(evidence_path)
			manifest = root / directory / "manifest.json"
			self.assertEqual(evidence["source"]["sha256"], hashlib.sha256(manifest.read_bytes()).hexdigest())
			for run in evidence["runtime"]["raw_runs"]:
				path = root / directory / f"{game}-{run['name']}.json"
				self.assertEqual(run["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run["name"])

	def test_pinned_library_build_matches_runtime_evidence(self) -> None:
		library = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve().parent / "builds" / "pinmame-8371478" / "Release" / "pinmame64.dll"
		if not library.is_file():
			self.skipTest(f"pinned library build not present: {library}")
		self.assertEqual(PINNED_LIBRARY_SHA256, hashlib.sha256(library.read_bytes()).hexdigest())

	def test_committed_runtime_evidence_rederives_from_raw_runs(self) -> None:
		import earthshaker_summarize_runtime_evidence as summarizer

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "earthshaker"
		for evidence_path, directory, game in ((LA3_RUNTIME_PATH, "harness-runs-la3", "esha_la3"), (PA1_RUNTIME_PATH, "harness-runs-pa1", "esha_pa1")):
			summarizer.check(root / directory, game, root / "rom-name-tables" / f"{game}.json", evidence_path)

	def test_retained_rom_name_tables_match_curator(self) -> None:
		import curate_earthshaker as curator

		tables = load_json(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "earthshaker" / "rom-name-tables" / "esha_la3.json")
		self.assertEqual(curator.ROM_SWITCH_NAMES, {entry["index"]: entry["text"] for entry in tables["switch_table"]["entries"]})
		self.assertEqual([curator.ROM_COIL_NAMES[address] for address in COIL_TEST_ORDER], [entry["text"] for entry in tables["coil_table"]["entries"]])


if __name__ == "__main__":
	unittest.main()
