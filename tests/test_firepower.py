"""Fail-closed tests for the Williams Firepower (1980) definition.

The facts worth pinning are the ones a plausible guess gets wrong: the flipper macro copies a
synthetic button into switch 45 rather than naming two matrix buttons, the special solenoids map to
their switches with no permutation, solenoid 20 is the bottom *right* bumper although the booklet
prints Left twice, solenoids 2 and 3 are fitted drivers with no load, the Oliver System 7 drivers
live in their own conversion record because they run on a different CPU board, and both retained
tables bind every standup to switch 48.
The geometric ordering assertions catch a reversed left/right or top/bottom identity.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "firepower-1980.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "firepower-1980.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "firepower-1980.json"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-6.json"
EXCERPT_DIR = ROOT / "evidence" / "excerpts" / "williams.firepower.1980"
SCENARIO_DIR = ROOT / "tools" / "harness-scenarios" / "system-6"

SWITCH = "pinmame.input.switch"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
DIP = "pinmame.input.dip"

DRIVER_IDS = {
	"frpwr_l6", "frpwr_l2", "frpwr_l6ff", "frpwr_l2ff", "frpwr_t6", "frpwr_t6ff",
	"frpwr_a6", "frpwr_d6", "frpwr_b6", "frpwr_c6",
}
SYSTEM_7_DRIVERS = {"frpwr_a7", "frpwr_e7", "frpwr_b7", "frpwr_c7", "frpwr_d7"}
SEVEN_DIGIT_DRIVERS = {"frpwr_b6", "frpwr_c6"}
CONVERSION_PATH = ROOT / "machines" / "partial" / "williams-oliver" / "firepower-1980.json"
UNUSED_SWITCHES = {20, 24, 52, 55, 56, 59, 60, 61, 62, 63, 64}
# src/wpc/s6games.c INITGAMEFULL(frpwr_l6, ..., 26, 25, 27, 28, 42, 12): special solenoid 17+n is
# fired by switch ssSw[n].
SPECIAL_SWITCH = {17: 26, 18: 25, 19: 27, 20: 28, 21: 42, 22: 12}
BACKBOX_LAMPS = {50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def point(device: dict, index: int = 0) -> tuple[float, float]:
	placement = device["spatial"]["placements"][index]
	return placement["x"], placement["y"]


class FirepowerDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", SWITCH)
		cls.dips = by_address(cls.definition, "inputs", DIP)
		cls.solenoids = by_address(cls.definition, "outputs", SOLENOID)
		cls.lamps = by_address(cls.definition, "outputs", LAMP)

	def test_record_is_author_ready_in_the_right_directory(self) -> None:
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("williams.firepower.1980", "Firepower", "Williams", 1980, "497", 856), (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["model_number"], machine["ipdb_id"]))
		self.assertEqual((952.0, 1974.0), (machine["playfield"]["width"], machine["playfield"]["height"]))

	def test_system_6_drivers_belong_here_and_system_7_drivers_to_the_conversion(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		claimed = {record["id"]: record["machine_id"] for record in catalog["drivers"] if record["id"].startswith("frpwr_")}
		expected = {driver: "williams.firepower.1980" for driver in DRIVER_IDS}
		expected.update({driver: "williams-oliver.firepower.1980" for driver in SYSTEM_7_DRIVERS})
		self.assertEqual(expected, claimed)
		# The old frpwr_d7/frpwr_e7 residual records merged into the one conversion record.
		self.assertEqual([CONVERSION_PATH], sorted((ROOT / "machines" / "partial" / "williams-oliver").glob("firepower-*.json")))

	def test_no_system_6_driver_overrides_a_binding(self) -> None:
		for driver in self.definition["drivers"]:
			self.assertNotIn("overrides", driver, driver["id"])
		self.assertEqual("relay.game-on-flipper-enable", self.solenoids[23]["id"])

	def test_system_7_conversion_is_an_honest_partial(self) -> None:
		conversion = load_json(CONVERSION_PATH)
		machine = conversion["machine"]
		self.assertEqual(("williams-oliver.firepower.1980", "physical_conversion", 856), (machine["id"], machine["kind"], machine["ipdb_id"]))
		self.assertEqual(SYSTEM_7_DRIVERS, {driver["id"] for driver in conversion["drivers"]})
		self.assertEqual("partial", conversion["coverage"]["status"])
		self.assertIn("identity", conversion["coverage"]["missing"])
		self.assertIn("controller_platform", conversion["coverage"]["missing"])
		self.assertNotIn("controller", conversion)
		self.assertEqual(([], [], []), (conversion["inputs"], conversion["outputs"], conversion["displays"]))
		for driver in conversion["drivers"]:
			self.assertNotIn("overrides", driver)
			self.assertNotIn("physical_compatibility", driver)

	def test_seven_digit_drivers_override_every_display(self) -> None:
		displays = {display["id"]: display for display in self.definition["displays"]}
		for driver in self.definition["drivers"]:
			overrides = {override["target"]: (override["segment_start"], override["width"]) for override in driver.get("display_overrides", [])}
			if driver["id"] in SEVEN_DIGIT_DRIVERS:
				self.assertEqual({"display.player-1-score": (0, 7), "display.player-2-score": (7, 7), "display.player-3-score": (20, 7), "display.player-4-score": (27, 7), "display.credits": (34, 2), "display.ball-in-play": (14, 2)}, overrides, driver["id"])
				# Each seven-digit driver's credit/ball-in-play roles are observed on that driver.
				run = "runtime.firepower.seven-digit-" + driver["id"].split("_")[1]
				for override in driver["display_overrides"]:
					self.assertIn(run, override["provenance"]["source_refs"], driver["id"])
			else:
				self.assertEqual({}, overrides, driver["id"])
		self.assertEqual((4, 14, 2), (displays["display.credits"]["controller_index"], displays["display.credits"]["segment_start"], displays["display.credits"]["width"]))
		self.assertEqual((5, 6, 2), (displays["display.ball-in-play"]["controller_index"], displays["display.ball-in-play"]["segment_start"], displays["display.ball-in-play"]["width"]))

	def test_switch_enumeration(self) -> None:
		self.assertEqual(set(range(-7, -2)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(UNUSED_SWITCHES, {address for address in range(1, 65) if self.switches[address]["availability"] == "unused"})
		for address in range(1, 65):
			if address not in UNUSED_SWITCHES:
				self.assertIs(False, self.switches[address]["normally_closed"], address)
		self.assertEqual({82, 84}, {address for address in range(81, 89) if self.switches[address]["availability"] == "used"})

	def test_lane_change_switch_is_fed_by_the_synthetic_right_button(self) -> None:
		self.assertEqual("switch.right-flipper-lane-change-switch", self.switches[45]["id"])
		relationship = {item["id"]: item for item in self.definition["relationships"]}["relationship.right-flipper-button-drives-lane-change-switch"]
		self.assertEqual(("switch.right-flipper-button", "switch.right-flipper-lane-change-switch"), (relationship["source"], relationship["destination"]))

	def test_special_solenoids_follow_ss_sw_without_permutation(self) -> None:
		relationships = {(item["source"], item["destination"]) for item in self.definition["relationships"] if item["kind"] == "direct"}
		for coil, switch in SPECIAL_SWITCH.items():
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), relationships, coil)

	def test_solenoid_20_is_the_bottom_right_bumper(self) -> None:
		self.assertEqual("Bottom Right Jet Bumper", self.solenoids[20]["label"])
		self.assertIn("typing error", self.solenoids[20]["physical"]["notes"])
		self.assertGreater(point(self.solenoids[20])[0], point(self.solenoids[18])[0])

	def test_output_enumeration_and_kinds(self) -> None:
		self.assertEqual(set(range(1, 24)) | {45, 46, 47, 48}, set(self.solenoids))
		self.assertEqual({2, 3}, {address for address, item in self.solenoids.items() if item["availability"] == "unused"})
		self.assertEqual({9, 10, 11, 12, 13}, {address for address, item in self.solenoids.items() if item["kind"] == "control_signal"})
		self.assertEqual("flasher", self.solenoids[15]["kind"])
		self.assertEqual(2, len(self.solenoids[15]["spatial"]["placements"]))
		self.assertEqual({45, 46, 47, 48}, {address for address, item in self.solenoids.items() if item["kind"] == "virtual"})
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual({23}, {address for address, item in self.lamps.items() if item["availability"] == "unused"})

	def test_no_gi_channel(self) -> None:
		self.assertFalse(any(item["binding"]["group"] == "pinmame.output.gi" for item in self.definition["outputs"]))

	def test_backbox_lamps_have_no_playfield_coordinate(self) -> None:
		for address in BACKBOX_LAMPS:
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual({3: 2, 4: 2, 62: 2, 63: 2, 64: 2}, {address: item["physical"]["quantity"] for address, item in self.lamps.items() if "quantity" in item.get("physical", {})})
		self.assertEqual("apron", self.lamps[56]["physical"]["location"])

	def test_dips(self) -> None:
		self.assertEqual({1, 2} | set(range(9, 25)), set(self.dips))
		self.assertEqual({1, 2, 17, 18, 19}, {address for address, item in self.dips.items() if item["availability"] == "used"})
		self.assertIn("Zero Audit Totals", self.dips[17]["label"])
		self.assertIn("Auto-Cycle", self.dips[19]["label"])

	def test_geometric_order(self) -> None:
		# F-I-R-E lanes run left to right across the top.
		xs = [point(self.switches[address])[0] for address in (32, 33, 34, 35)]
		self.assertEqual(sorted(xs), xs)
		# Targets 1-3 left bank, 4-6 right bank, each left to right.
		xs = [point(self.switches[address])[0] for address in (17, 18, 19, 21, 22, 23)]
		self.assertEqual(sorted(xs), xs)
		# POWER targets top to bottom.
		ys = [point(self.switches[address])[1] for address in (39, 40, 41)]
		self.assertEqual(sorted(ys), ys)
		# Left-rail standups top to bottom, and the ball-ramp rest positions left to right.
		ys = [point(self.switches[address])[1] for address in (14, 49, 50)]
		self.assertEqual(sorted(ys), ys)
		xs = [point(self.switches[address])[0] for address in (51, 58, 57)]
		self.assertEqual(sorted(xs), xs)
		# Left devices left of right devices.
		for left, right in ((10, 44), (11, 43), (12, 42), (26, 27), (25, 28), (53, 54)):
			self.assertLess(point(self.switches[left])[0], point(self.switches[right])[0], (left, right))
		self.assertLess(point(self.switches[26])[1], point(self.switches[25])[1])
		self.assertLess(point(self.solenoids[22])[0], point(self.solenoids[21])[0])
		# Bonus ladder 1,000 at the bottom climbing to 20,000.
		ys = [point(self.lamps[address])[1] for address in (14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25)]
		self.assertEqual(sorted(ys, reverse=True), ys)

	def test_standups_are_identified_from_the_drawing_not_the_script(self) -> None:
		expected = {16: (0.219253, 0.13404), 31: (0.710496, 0.157521), 37: (0.748209, 0.213825), 14: (0.077564, 0.311903), 48: (0.870159, 0.579029), 50: (0.13632, 0.422896), 38: (0.864343, 0.414092)}
		for address, coordinates in expected.items():
			self.assertEqual(coordinates, point(self.switches[address]), address)
		self.assertEqual((0.12, 0.37), point(self.switches[49]))

	def test_excerpt_digests(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["image"])

	def test_harness_scenarios_are_pinned(self) -> None:
		import curate_firepower as curator

		for _run, (_run_sha, scenario, scenario_sha, _init_sha) in curator.HARNESS_RUNS.items():
			self.assertEqual(scenario_sha, hashlib.sha256((SCENARIO_DIR / scenario).read_bytes()).hexdigest(), scenario)
		init_scenarios = {
			"frpwr_l6": "firepower-nvram-init-boot.json",
			"frpwr_b6": "firepower-b6-nvram-init-boot.json",
			"frpwr_c6": "firepower-c6-nvram-init-boot.json",
			"frpwr_b7": "firepower-sys7-nvram-init-boot.json",
		}
		self.assertEqual(set(init_scenarios), set(curator.HARNESS_BOOT))
		for game, name in init_scenarios.items():
			self.assertEqual(curator.HARNESS_BOOT[game][0], hashlib.sha256((SCENARIO_DIR / name).read_bytes()).hexdigest(), name)
			self.assertEqual(game, load_json(SCENARIO_DIR / name)["game"], name)

	def test_flipper_button_scenario_never_writes_switch_45(self) -> None:
		scenario = load_json(SCENARIO_DIR / "firepower-flipper-button-copy.json")
		written = {action["switch"] for action in scenario["actions"] if "switch" in action} | {item["switch"] for item in scenario["initial_switches"]}
		self.assertNotIn(45, written)
		self.assertIn(82, written)


class FirepowerControllerProfileTests(unittest.TestCase):
	def test_profile_ranges(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		groups = {group["id"]: group["address_rules"] for group in profile["groups"]}
		self.assertEqual([{"minimum": -7, "maximum": -3}, {"minimum": 1, "maximum": 64}, {"minimum": 81, "maximum": 88}], groups[SWITCH])
		self.assertEqual([{"minimum": 1, "maximum": 23}, {"minimum": 45, "maximum": 48}], groups[SOLENOID])
		self.assertEqual([{"minimum": 1, "maximum": 64}], groups[LAMP])
		self.assertEqual([{"minimum": 1, "maximum": 2}, {"minimum": 9, "maximum": 24}], groups[DIP])
		self.assertNotIn("pinmame.output.gi", groups)


class FirepowerCuratorTests(unittest.TestCase):
	def test_curator_check(self) -> None:
		import curate_firepower as curator

		curator.check(ROOT)


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "PINMAME_VPX_SOURCES_ROOT is not set")
class FirepowerRetainedEvidenceTests(unittest.TestCase):
	def test_extractions_match_their_manifests(self) -> None:
		import curate_firepower as curator

		curator.verify_extraction_manifests(Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]))

	def test_script_hashes(self) -> None:
		import curate_firepower as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams" / "firepower-1980"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "source" / "Firepower (Williams 1980).vpx").read_bytes()).hexdigest())
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256((root / "extracted-vpxtool" / "firepower-williams-1980-v1.0" / "script.vbs").read_bytes()).hexdigest())
		self.assertEqual(curator.AI_SCRIPT_SHA256, hashlib.sha256((root / "extracted-vpxtool" / "firepower-vs-ai-v3.4.2" / "script.vbs").read_bytes()).hexdigest())

	def test_every_standup_wall_pulses_48_in_the_retained_script(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams" / "firepower-1980"
		script = (root / "extracted-vpxtool" / "firepower-williams-1980-v1.0" / "script.vbs").read_text(encoding="latin-1")
		for index in range(1, 9):
			self.assertIn(f"Sub StandupTarget{index}_hit:vpmtimer.pulsesw cLowerRightStandupSW", script)

	def test_only_the_vs_ai_revision_models_standup_49(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams" / "firepower-1980" / "extracted-vpxtool"
		base = {path.name for path in (root / "firepower-williams-1980-v1.0" / "gameitems").glob("Wall.StandupTarget*.json")}
		self.assertEqual({f"Wall.StandupTarget{index}.json" for index in range(1, 8)}, base)
		wall = load_json(root / "firepower-vs-ai-v3.4.2" / "gameitems" / "Wall.StandupTarget8.json")["Wall"]
		points = [(item["x"], item["y"]) for item in wall["drag_points"]]
		centre = (sum(x for x, _ in points) / len(points) / 952.0, sum(y for _, y in points) / len(points) / 1974.0)
		self.assertAlmostEqual(0.12, centre[0], delta=0.01)
		self.assertAlmostEqual(0.37, centre[1], delta=0.01)


class FirepowerRuntimeEvidenceTests(unittest.TestCase):
	"""Re-verify the retained harness runs when the shared working root is present."""

	@classmethod
	def setUpClass(cls) -> None:
		sys.path.insert(0, str(ROOT / "src"))
		from pinmame_game_defs.workspace import resolve_working_root

		cls.runtime_root = resolve_working_root(ROOT) / "runtime-evidence"
		if not (cls.runtime_root / "firepower-1980.manifest.json").is_file():
			raise unittest.SkipTest("retained Firepower runtime evidence is not present")

	def test_runtime_directory_matches_its_manifest(self) -> None:
		import curate_firepower as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		manifest = load_json(self.runtime_root / "firepower-1980.manifest.json")
		rebuilt = curator.build_extraction_manifest(self.runtime_root / "firepower-1980")
		rebuilt["format"] = "pinmame-runtime-evidence-manifest"
		self.assertEqual(canonical_bytes(rebuilt), canonical_bytes(manifest))
		identity = (len(manifest["files"]), sum(item["size"] for item in manifest["files"]), hashlib.sha256(canonical_bytes(manifest)).hexdigest())
		self.assertEqual(curator.RUNTIME_MANIFEST, identity)
		for name, (run_sha, _scenario, scenario_sha, _init_sha) in curator.HARNESS_RUNS.items():
			run = load_json(self.runtime_root / "firepower-1980" / name)
			self.assertEqual(run_sha, hashlib.sha256((self.runtime_root / "firepower-1980" / name).read_bytes()).hexdigest(), name)
			self.assertEqual(scenario_sha, run["scenario"]["sha256"], name)
			self.assertEqual(curator.LIBRARY_SHA256, run["library_sha256"], name)
			self.assertIsNone(run["failure"], name)

	def _steps(self, name: str) -> list[dict]:
		return load_json(self.runtime_root / "firepower-1980" / name)["steps"]

	@staticmethod
	def _changed(step: dict, kind: str, ignore: frozenset[int] = frozenset()) -> dict[int, list[int]]:
		return {item["number"]: item["states"] for item in step["transitions"][kind] if item["number"] not in ignore}

	def test_right_flipper_button_reaches_the_lane_change_switch(self) -> None:
		steps = {step["label"]: step for step in self._steps("run-flip.json")}
		right = steps["press and release the right cabinet flipper button (synthetic 82); public 45 is never written by the scenario"]
		self.assertEqual({45: [1, 0], 46: [1, 0]}, self._changed(right, "solenoids"))
		# Target-arrow lamps 26-31 flash throughout play and are not part of the lane change.
		arrows = frozenset(range(26, 32))
		self.assertEqual({5: [0], 6: [1]}, self._changed(right, "lamps", arrows))
		left = steps["press and release the left cabinet flipper button (synthetic 84)"]
		self.assertEqual({47: [1, 0], 48: [1, 0]}, self._changed(left, "solenoids"))
		self.assertEqual({}, self._changed(left, "lamps", arrows))

	def test_seven_digit_system_6_display_roles(self) -> None:
		for name in ("run-b6.json", "run-c6.json"):
			snapshots = {snapshot["label"]: {display["index"]: display["segments"] for display in snapshot["displays"] if "segments" in display} for snapshot in load_json(self.runtime_root / "firepower-1980" / name)["snapshots"]}
			coin = snapshots["insert a coin on the right coin switch (public 4)"]
			start = snapshots["press the credit button (public 3) to start a game"]
			# 0x3f is the digit 0, 0x06 the digit 1, 0 a blank digit.
			self.assertEqual(([0x3f, 0x06], [0x3f, 0x3f]), (coin[4], coin[5]), name)
			self.assertEqual(([0x3f, 0x3f], [0x00, 0x06]), (start[4], start[5]), name)


if __name__ == "__main__":
	unittest.main()
