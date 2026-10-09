"""Fail-closed tests for the Williams Black Knight (1980) definition.

The facts worth pinning are the ones a plausible guess gets wrong: PinMAME's simulator file names
solenoid 11 a knocker and 1 the outhole while the machine has a GI relay at 11 and an outhole kicker
called Ball Release at 1; the game-on enable is 25 on System 7, not 23; each Magna-Save button
fires its own side's relay although the wiring sheet prints the relay coils' sides swapped; the
special solenoids follow switches 21, 22 and 36; lamp 7 is printed but has no bulb; the rebound
standups 28, 32 and 40 are optional, not absent; the CPU-board DIP banks are never read; and the
player displays are not in index order. Geometric ordering assertions catch a reversed left/right
or top/bottom identity.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "black-knight-1980.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "black-knight-1980.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "black-knight-1980.json"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "system-7.json"
SCENARIO_DIR = ROOT / "tools" / "harness-scenarios" / "system-7"

SWITCH = "pinmame.input.switch"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
DIP = "pinmame.input.dip"

DRIVER_IDS = {"bk_l4", "bk_l3", "bk_l2", "bk_f4"}
UNUSED_SWITCHES = set(range(47, 65))
OPTIONAL_SWITCHES = {28, 32, 40}
# src/wpc/sims/s7/full/bk.c bkGameData: special solenoid 17+n is fired by switch ssSw[n].
SPECIAL_SWITCH = {17: 21, 18: 22, 19: 36}
BACKBOX_LAMPS = {1, 2, 3, 4, 5, 6, 8}
UNUSED_LAMPS = {7, 43, 44, 45, 46}
UNUSED_SOLENOIDS = {12, 13, 14, 20, 21, 22, 23, 24}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def point(device: dict, index: int = 0) -> tuple[float, float]:
	placement = device["spatial"]["placements"][index]
	return placement["x"], placement["y"]


class BlackKnightDefinitionTests(unittest.TestCase):
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

	def test_identity_and_platform(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("williams.black-knight.1980", "Black Knight", "Williams", 1980, "500", 310, "GrO7w-M9R03"), (machine["id"], machine["name"], machine["manufacturer"], machine["year"], machine["model_number"], machine["ipdb_id"], machine["opdb_id"]))
		self.assertEqual({"platform": "pinmame.system-7", "hardware_generation": "0x10000", "inversion_applied_by_emulator": True}, self.definition["controller"])
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		claimed = {record["id"]: record["machine_id"] for record in catalog["drivers"] if record["id"].startswith("bk_")}
		self.assertEqual({driver: "williams.black-knight.1980" for driver in DRIVER_IDS}, claimed)
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])

	def test_switch_enumeration_and_polarity(self) -> None:
		self.assertEqual(set(range(-7, -2)) | set(range(1, 65)) | set(range(81, 89)), set(self.switches))
		self.assertEqual(UNUSED_SWITCHES, {address for address in range(1, 65) if self.switches[address]["availability"] == "unused"})
		self.assertEqual(OPTIONAL_SWITCHES, {address for address in range(1, 65) if self.switches[address]["availability"] == "optional"})
		for address in range(1, 47):
			self.assertIs(False, self.switches[address]["normally_closed"], address)
		self.assertEqual({82, 84}, {address for address in range(81, 89) if self.switches[address]["availability"] == "used"})

	def test_magna_save_buttons_are_cabinet_switches_9_and_10(self) -> None:
		self.assertEqual(("Right Magnet Button", "Left Magnet Button"), (self.switches[9]["label"], self.switches[10]["label"]))
		for address in (9, 10):
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
			self.assertIn("7P1-20", self.switches[address]["wiring"]["drive_connection"])
		# The rest of matrix column 2 is on the playfield harness, not the cabinet.
		for address in range(11, 17):
			wiring = self.switches[address]["wiring"]
			self.assertEqual("2J2-8, 8P1-1", wiring["drive_connection"], address)
			self.assertIn(f"8SW{address}, diode 8D{address}", wiring["return_component"], address)
			self.assertNotIn("7P1", wiring["return_connection"], address)

	def test_solenoid_names_follow_the_manual_not_the_simulator_file(self) -> None:
		self.assertEqual("Ball Release", self.solenoids[1]["label"])
		self.assertEqual("Ball Ramp Thrower", self.solenoids[6]["label"])
		self.assertEqual("Multi-Ball Release", self.solenoids[7]["label"])
		self.assertEqual(("relay", "Special Relay (General Illumination)"), (self.solenoids[11]["kind"], self.solenoids[11]["label"]))
		self.assertNotIn("Knocker", json.dumps(self.solenoids[11]["label"]))
		self.assertEqual("Bell", self.solenoids[15]["label"])

	def test_magnet_relays_follow_their_sides(self) -> None:
		self.assertEqual(("relay.right-magnet-relay", "relay.left-magnet-relay"), (self.solenoids[9]["id"], self.solenoids[10]["id"]))
		self.assertIn("8L28", self.solenoids[9]["wiring"]["return_component"])
		self.assertIn("8L29", self.solenoids[10]["wiring"]["return_component"])
		self.assertIn("drafting error", self.solenoids[9]["physical"]["notes"])
		# The relay coils are fed from the flipper rails through 8R7/8R8, not from SOL. B+.
		self.assertEqual(("GRY", "BLU"), (self.solenoids[9]["wiring"]["power_wire"], self.solenoids[10]["wiring"]["power_wire"]))
		self.assertIn("8R7", self.solenoids[9]["wiring"]["power_connection"])
		self.assertIn("8R8", self.solenoids[10]["wiring"]["power_connection"])
		self.assertGreater(point(self.solenoids[9])[0], 0.5)
		self.assertLess(point(self.solenoids[10])[0], 0.5)

	def test_game_on_is_25_and_flippers_are_synthetic(self) -> None:
		self.assertEqual(set(range(1, 26)) | {45, 46, 47, 48}, set(self.solenoids))
		self.assertEqual("relay.game-on-flipper-enable", self.solenoids[25]["id"])
		self.assertEqual({45, 46, 47, 48}, {address for address, item in self.solenoids.items() if item["kind"] == "virtual"})
		self.assertEqual(UNUSED_SOLENOIDS, {address for address, item in self.solenoids.items() if item["availability"] == "unused"})

	def test_special_solenoids_follow_ss_sw(self) -> None:
		relationships = {(item["source"], item["destination"]) for item in self.definition["relationships"] if item["kind"] == "direct"}
		for coil, switch in SPECIAL_SWITCH.items():
			self.assertIn((self.switches[switch]["id"], self.solenoids[coil]["id"]), relationships, coil)
		self.assertEqual(len(SPECIAL_SWITCH), len(relationships))

	def test_lamps(self) -> None:
		self.assertEqual(set(range(1, 65)), set(self.lamps))
		self.assertEqual(UNUSED_LAMPS, {address for address, item in self.lamps.items() if item["availability"] == "unused"})
		for address in BACKBOX_LAMPS:
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual({1: 2}, {address: item["physical"]["quantity"] for address, item in self.lamps.items() if "quantity" in item.get("physical", {})})
		self.assertIn("N.C.", self.lamps[7]["physical"]["notes"])

	def test_no_gi_channel(self) -> None:
		self.assertFalse(any(item["binding"]["group"] == "pinmame.output.gi" for item in self.definition["outputs"]))

	def test_dips_are_sound_board_only(self) -> None:
		self.assertEqual({1, 2} | set(range(9, 25)), set(self.dips))
		self.assertEqual({1, 2}, {address for address, item in self.dips.items() if item["availability"] == "used"})
		for address in range(9, 25):
			self.assertIn("rom.black-knight.dip-port-reads", self.dips[address]["provenance"]["source_refs"], address)

	def test_displays_follow_the_observed_player_order(self) -> None:
		displays = {display["id"]: (display["controller_index"], display["segment_start"], display["width"]) for display in self.definition["displays"]}
		self.assertEqual(
			{
				"display.player-1-score": (2, 1, 7),
				"display.player-2-score": (3, 9, 7),
				"display.player-3-score": (0, 21, 7),
				"display.player-4-score": (1, 29, 7),
				"display.ball-in-play-tens": (4, 0, 1),
				"display.ball-in-play-units": (5, 8, 1),
				"display.credits-tens": (6, 20, 1),
				"display.credits-units": (7, 28, 1),
			},
			displays,
		)

	def test_geometric_order(self) -> None:
		# Outlanes outside inlanes, left on the left.
		self.assertLess(point(self.switches[11])[0], point(self.switches[16])[0])
		self.assertLess(point(self.switches[15])[0], point(self.switches[12])[0])
		self.assertLess(point(self.solenoids[17])[0], point(self.solenoids[18])[0])
		# Lower left bank: lower target nearest the player.
		ys = [point(self.switches[address])[1] for address in (25, 26, 27)]
		self.assertEqual(sorted(ys, reverse=True), ys)
		# Lower right bank: right, centre, left from right to left.
		xs = [point(self.switches[address])[0] for address in (29, 30, 31)]
		self.assertEqual(sorted(xs, reverse=True), xs)
		# Top banks on the upper playfield, behind the lower playfield's banks.
		for upper, lower in ((34, 26), (38, 30)):
			self.assertLess(point(self.switches[upper])[1], point(self.switches[lower])[1])
		# Ball ramp: left, centre, right from left to right, below the flippers; lockup bottom to top.
		xs = [point(self.switches[address])[0] for address in (19, 18, 17)]
		self.assertEqual(sorted(xs), xs)
		ys = [point(self.switches[address])[1] for address in (43, 42, 41)]
		self.assertEqual(sorted(ys), ys)
		# Bonus ladder "1" at the bottom climbing to "40".
		ys = [point(self.lamps[address])[1] for address in range(48, 61)]
		self.assertEqual(sorted(ys, reverse=True), ys)

	def test_excerpt_digests(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])

	def test_harness_scenarios_are_pinned(self) -> None:
		import curate_black_knight as curator

		for _run, (_run_sha, scenario, scenario_sha, _init_sha, game) in curator.HARNESS_RUNS.items():
			self.assertEqual(scenario_sha, hashlib.sha256((SCENARIO_DIR / scenario).read_bytes()).hexdigest(), scenario)
			self.assertEqual(game, load_json(SCENARIO_DIR / scenario)["game"], scenario)
		for game, (name, digest) in curator.HARNESS_BOOT.items():
			self.assertEqual(digest, hashlib.sha256((SCENARIO_DIR / name).read_bytes()).hexdigest(), name)
			self.assertEqual(game, load_json(SCENARIO_DIR / name)["game"], name)

	def test_gameplay_scenarios_use_direct_switch_writes_only(self) -> None:
		for path in SCENARIO_DIR.glob("black-knight-*.json"):
			for action in load_json(path)["actions"]:
				self.assertNotIn(action["type"], {"pulse_key", "set_key"}, path.name)

	def test_no_sibling_record_is_named(self) -> None:
		# The curator started from the Firepower curator; none of its or Black Knight 2000's identities may
		# leak in. The forbidden set comes from the catalog: each sibling's machine id, its driver ids and
		# the title its drivers carry, plus Firepower's System 6 generation and profile.
		import re

		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		siblings = {"williams.firepower.1980", "williams.black-knight-2000.1989"}
		self.assertEqual(siblings, {m["id"] for m in catalog["machines"] if m["id"] in siblings})
		forbidden = set(siblings) | {"GEN_S6", "pinmame.system-6"}
		for driver in catalog["drivers"]:
			if driver["machine_id"] in siblings:
				forbidden.add(driver["id"])
				forbidden.add(re.sub(r"\s*\(.*\)$", "", driver["description"]))
		self.assertTrue({"bk2k_l4", "frpwr_l6", "Black Knight 2000", "Firepower"} <= forbidden, forbidden)
		paths = [
			DEFINITION_PATH,
			SEED_PATH,
			ROOT / "knowledge" / "williams" / "black-knight-1980.md",
			ROOT / "reports" / "spatial" / "williams" / "black-knight-1980.json",
			ROOT / "reports" / "spatial" / "williams" / "black-knight-1980.md",
			*sorted((ROOT / "evidence" / "excerpts" / "williams.black-knight.1980").glob("*.md")),
		]
		for path in paths:
			text = path.read_text(encoding="utf-8").casefold()
			for token in forbidden:
				self.assertNotIn(token.casefold(), text, f"{path.name} names {token}")


class BlackKnightControllerProfileTests(unittest.TestCase):
	def test_profile_ranges(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.system-7", profile["id"])
		groups = {group["id"]: group["address_rules"] for group in profile["groups"]}
		self.assertEqual([{"minimum": -7, "maximum": -3}, {"minimum": 1, "maximum": 64}, {"minimum": 81, "maximum": 88}], groups[SWITCH])
		self.assertEqual([{"minimum": 1, "maximum": 25}, {"minimum": 45, "maximum": 48}, {"minimum": 51, "maximum": 60}], groups[SOLENOID])
		self.assertEqual([{"minimum": 1, "maximum": 96}], groups[LAMP])
		self.assertEqual([{"minimum": 1, "maximum": 2}, {"minimum": 9, "maximum": 24}], groups[DIP])
		self.assertNotIn("pinmame.output.gi", groups)

	def test_profile_states_the_special_solenoid_permutation(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		notes = {group["id"]: group.get("notes", "") for group in profile["groups"]}
		for handler, public in (("pia2cb2_w", "17"), ("pia2ca2_w", "18"), ("pia4cb2_w", "19"), ("pia4ca2_w", "20"), ("pia1ca2_w", "21"), ("pia3cb2_w", "22"), ("pia0cb2_w", "23"), ("pia0ca2_w", "24")):
			self.assertRegex(notes[SOLENOID], rf"`{handler}` \| \d \| `{public}`")
		self.assertIn("S7_GAMEONSOL", notes[SOLENOID])


class BlackKnightCuratorTests(unittest.TestCase):
	def test_curator_check(self) -> None:
		import curate_black_knight as curator

		curator.check(ROOT)

	def test_figure3_registration(self) -> None:
		"""The drawing-derived points are interpolated, reproduce the stated fit, and match the excerpt."""
		import curate_black_knight as curator

		controls = list(curator.FIGURE3_CONTROLS.values())
		fit = curator.affine_fit(controls)
		residuals = [((x - tx) ** 2 + (y - ty) ** 2) ** 0.5 for (pixel, (tx, ty)) in controls for x, y in [curator.apply_fit(fit, pixel)]]
		self.assertEqual(9.4, round((sum(r * r for r in residuals) / len(residuals)) ** 0.5, 1))
		leave_one_out = []
		for index, (pixel, (tx, ty)) in enumerate(controls):
			x, y = curator.apply_fit(curator.affine_fit(controls[:index] + controls[index + 1:]), pixel)
			leave_one_out.append(((x - tx) ** 2 + (y - ty) ** 2) ** 0.5)
		self.assertEqual(17.3, round(max(leave_one_out), 1))
		# Controls named after a table object carry that object's centre.
		for name, (_, table_point) in curator.FIGURE3_CONTROLS.items():
			if name in curator.TABLE_POINTS:
				for got, want in zip(table_point, curator.TABLE_POINTS[name]):
					self.assertAlmostEqual(want, got, delta=1e-3, msg=name)

		# Every reading lies strictly inside the controls' convex hull (no extrapolation).
		def cross(o: tuple, a: tuple, b: tuple) -> float:
			return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

		points = sorted({pixel for pixel, _ in controls})
		lower: list = []
		upper: list = []
		for p in points:
			while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
				lower.pop()
			lower.append(p)
		for p in reversed(points):
			while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
				upper.pop()
			upper.append(p)
		hull = lower[:-1] + upper[:-1]
		for name, pixel in curator.FIGURE3_READINGS.items():
			for a, b in zip(hull, hull[1:] + hull[:1]):
				self.assertGreater(cross(a, b, pixel), 0, f"{name} is outside the Figure 3 controls")

		# The excerpt's tables carry the same controls, readings and two-decimal results.
		excerpt = (ROOT / "evidence" / "excerpts" / "williams.black-knight.1980" / "switch-locations.md").read_text(encoding="utf-8")
		for (u, v), _ in controls:
			self.assertIn(f"| ({u}, {v}) |", excerpt)
		for name, (u, v) in curator.FIGURE3_READINGS.items():
			x, y = curator.DRAWING_POINTS[name]
			self.assertRegex(excerpt, rf"\| \({u}, {v}\)[^|]* \| \([0-9.]+, [0-9.]+\) \| \({x:.2f}, {y:.2f}\) \|", name)


class BlackKnightRetainedEvidenceTests(unittest.TestCase):
	"""Re-verify the retained table extraction and harness runs when the working root is present."""

	@classmethod
	def setUpClass(cls) -> None:
		sys.path.insert(0, str(ROOT / "src"))
		from pinmame_game_defs.workspace import resolve_working_root

		working_root = resolve_working_root(ROOT)
		cls.runtime_root = working_root / "runtime-evidence"
		cls.sources_root = working_root / "vpx-sources"
		# Skip only when no Black Knight evidence is retained at all; a partial bundle is a failure.
		parts = {
			"runtime manifest": cls.runtime_root / "black-knight-1980.manifest.json",
			"runtime directory": cls.runtime_root / "black-knight-1980",
			"table directory": cls.sources_root / "williams" / "black-knight-1980",
		}
		present = {name for name, path in parts.items() if path.exists()}
		if not present:
			raise unittest.SkipTest("retained Black Knight evidence is not present")
		if present != set(parts):
			raise AssertionError(f"incomplete retained Black Knight evidence: missing {sorted(set(parts) - present)}")

	def test_extraction_matches_its_manifest(self) -> None:
		import curate_black_knight as curator

		curator.verify_extraction_manifest(self.sources_root)
		root = self.sources_root / "williams" / "black-knight-1980"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "source" / "Black Knight (Williams 1980).vpx").read_bytes()).hexdigest())
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256((root / "extracted-vpxtool" / curator.EXTRACTION_DIRECTORY / "script.vbs").read_bytes()).hexdigest())

	def test_script_library_is_the_pinned_file(self) -> None:
		import curate_black_knight as curator

		library = (self.sources_root / "williams" / "black-knight-1980" / "vpinmame-scripts" / "s7.vbs").read_bytes()
		self.assertEqual(curator.VPM_LIBRARY_SHA256, hashlib.sha256(library).hexdigest())
		# The excerpt's constants are the library's own lines.
		text = library.decode("latin-1")
		for line in ("Const GameOnSolenoid = 25", "Const swLRFlip       = 82", "Const swLLFlip       = 84"):
			self.assertIn(line, text)

	def test_table_points_are_recomputed_from_gameitems(self) -> None:
		import curate_black_knight as curator

		gameitems = self.sources_root / "williams" / "black-knight-1980" / "extracted-vpxtool" / curator.EXTRACTION_DIRECTORY / "gameitems"
		files = {path.name.split(".", 1)[1].removesuffix(".json"): path for path in gameitems.glob("*.json")}
		for name, (x, y) in curator.TABLE_POINTS.items():
			item = next(iter(load_json(files[name]).values()))
			if "center" in item:
				expected = (item["center"]["x"], item["center"]["y"])
			else:
				points = item["drag_points"]
				expected = (sum(point["x"] for point in points) / len(points), sum(point["y"] for point in points) / len(points))
			self.assertAlmostEqual(expected[0], x, delta=1e-4, msg=name)
			self.assertAlmostEqual(expected[1], y, delta=1e-4, msg=name)
		# Every placed lamp's light carries that lamp's number as its TimerInterval, which InitLights binds.
		for address, (_label, name) in curator.LAMPS.items():
			self.assertEqual(address, next(iter(load_json(files[name]).values()))["timer_interval"], name)

	def test_table_script_defects_still_present(self) -> None:
		import curate_black_knight as curator

		script = (self.sources_root / "williams" / "black-knight-1980" / "extracted-vpxtool" / curator.EXTRACTION_DIRECTORY / "script.vbs").read_text(encoding="latin-1")
		self.assertIn('SolCallback(23) = "vpmNudge.SolGameOn"', script)
		self.assertIn(".Solenoid = 9", script)
		self.assertIn(".Solenoid = 10", script)

	def test_runtime_directory_matches_its_manifest(self) -> None:
		import curate_black_knight as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		manifest = load_json(self.runtime_root / "black-knight-1980.manifest.json")
		self.assertEqual(canonical_bytes(curator.build_runtime_manifest(self.runtime_root)), canonical_bytes(manifest))
		self.assertEqual(curator.RUNTIME_MANIFEST, curator.manifest_identity(manifest))
		for name, (run_sha, _scenario, scenario_sha, _init_sha, _game) in curator.HARNESS_RUNS.items():
			path = self.runtime_root / "black-knight-1980" / name
			run = load_json(path)
			self.assertEqual(run_sha, hashlib.sha256(path.read_bytes()).hexdigest(), name)
			self.assertEqual(scenario_sha, run["scenario"]["sha256"], name)
			self.assertEqual(curator.LIBRARY_SHA256, run["library_sha256"], name)
			self.assertIsNone(run["failure"], name)

	def _run(self, name: str) -> dict:
		return load_json(self.runtime_root / "black-knight-1980" / name)

	@staticmethod
	def _solenoids(step: dict) -> dict[int, list[int]]:
		return {item["number"]: item["states"] for item in step["transitions"]["solenoids"]}

	def test_solenoid_test_pairs_display_and_address(self) -> None:
		digits = {0x3F: 0, 0x06: 1, 0x5B: 2, 0x4F: 3, 0x66: 4, 0x6D: 5, 0x7D: 6, 0x07: 7, 0x7F: 8, 0x6F: 9}
		for name in ("run-sol.json", "run-sol-l3.json", "run-sol-f4.json"):
			run = self._run(name)
			# One snapshot at boot, then one at the end of every step.
			self.assertEqual(len(run["steps"]) + 1, len(run["snapshots"]), name)
			paired: dict[int, set[int]] = {}
			for step, snapshot in zip(run["steps"], run["snapshots"][1:]):
				if not step["label"].startswith(("Advance: next solenoid step", "Manual-Down: hold")):
					continue
				segments = {display["index"]: display["segments"][0] & 0x7F for display in snapshot["displays"] if "segments" in display}
				shown = digits[segments[4]] * 10 + digits[segments[5]]
				paired.setdefault(shown, set()).update(self._solenoids(step))
			# Every displayed step 1-25 pulses the address of its own number.
			self.assertEqual(set(range(1, 26)), set(paired), name)
			for number, changed in paired.items():
				self.assertIn(number, changed, (name, number))

	def test_switch_test_reports_1_to_46(self) -> None:
		run = self._run("run-sw.json")
		digits = {0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9", 0x00: " "}
		reported = set()
		for snapshot in run["snapshots"]:
			if not snapshot["label"].endswith("(held)"):
				continue
			address = int(snapshot["label"].split("switch ")[1].split(" ")[0])
			segments = {display["index"]: display["segments"][0] & 0x7F for display in snapshot["displays"] if "segments" in display}
			shown = (digits[segments[4]] + digits[segments[5]]).strip()
			if shown:
				self.assertEqual(address, int(shown), address)
				reported.add(address)
		self.assertEqual(set(range(1, 47)), reported)

	def test_gameplay_causality(self) -> None:
		steps = {step["label"]: step for step in self._run("run-play.json")["steps"]}
		self.assertEqual({17: [1, 0]}, self._solenoids(steps["left kicker scoring switch"]))
		self.assertEqual({18: [1, 0]}, self._solenoids(steps["right kicker scoring switch"]))
		self.assertEqual({19: [1, 0]}, self._solenoids(steps["jet bumper switch"]))
		self.assertEqual({45: [1, 0], 46: [1, 0]}, self._solenoids(steps["right flipper button (synthetic 82)"]))
		self.assertEqual({47: [1, 0], 48: [1, 0]}, self._solenoids(steps["left flipper button (synthetic 84)"]))
		for label, coil in (("lower left bank: target 27 down, bank complete", 2), ("lower right bank: target 31 down, bank complete", 3), ("top left bank: target 35 down, bank complete", 4), ("top right bank: target 39 down, bank complete", 5)):
			self.assertIn(coil, self._solenoids(steps[label]), label)
		self.assertEqual([1], self._solenoids(steps["left Magna-Save button"])[10])
		self.assertEqual([1], self._solenoids(steps["right Magna-Save button"])[9])
		self.assertEqual({8: [1, 0]}, self._solenoids(steps["ball in the lower playfield eject hole"]))
		self.assertIn(1, self._solenoids(steps["ball drains into the outhole"]))
		third = self._solenoids(steps["playfield tilt, third closure"])
		self.assertEqual(([1], [0]), (third[11], third[25]))

	def test_multiball_release_fires_with_the_balls_still_locked(self) -> None:
		steps = {step["label"]: step for step in self._run("run-mb.json")["steps"]}
		waited = self._solenoids(steps["with all three lockup switches still closed, wait for the Multi-Ball release (solenoid 7)"])
		self.assertEqual([1], waited[7])


if __name__ == "__main__":
	unittest.main()
