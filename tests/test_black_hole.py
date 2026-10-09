"""Fail-closed tests for the Gottlieb Black Hole (1981) definition and the System 80 profile.

The facts worth pinning are the ones a plausible guess gets wrong: the manual's own solenoid list misnumbers every
coil, most playfield mechanisms hang on lamp drivers rather than solenoid drivers, lamps 48-51 are the hardware
inverse of 44-47, the flipper outputs say nothing about which playfield's flippers move, the sound-only drivers are
the same machine, and System 80 switch numbers are strobe*10+return rather than sequential.
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
sys.path.insert(0, str(ROOT / "src"))

import curate_black_hole as curator  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

DEFINITION_PATH = ROOT / "machines" / "partial" / "gottlieb" / "black-hole-1981.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "gts80.json"
SCENARIO_DIR = ROOT / "tools" / "harness-scenarios" / "gts80"
DRIVER_IDS = {"blckhole", "blkhole2", "blkholea", "blkhole7", "blkhol7s"}

SWITCH = "pinmame.input.switch"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
DIP = "pinmame.input.dip"


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_point(device: dict) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


def allowed(address: int, rules: list[dict]) -> bool:
	return any(
		(address in rule["values"]) if "values" in rule else rule["minimum"] <= address <= rule["maximum"]
		for rule in rules
	)


class BlackHoleDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.groups = {group["id"]: group for group in cls.profile["groups"]}
		cls.switches = by_address(cls.definition, "inputs", SWITCH)
		cls.dips = by_address(cls.definition, "inputs", DIP)
		cls.solenoids = by_address(cls.definition, "outputs", SOLENOID)
		cls.lamps = by_address(cls.definition, "outputs", LAMP)

	def test_curator_reproduces_the_definition_seed_and_report(self) -> None:
		built = curator.build()
		self.assertEqual(canonical_bytes(built), DEFINITION_PATH.read_bytes())
		self.assertEqual(DEFINITION_PATH.read_bytes(), curator.SEED_PATH.read_bytes())
		report = curator.build_spatial_report(built)
		self.assertEqual(canonical_bytes(report), curator.SPATIAL_REPORT_PATH.read_bytes())
		self.assertEqual(curator.render_spatial_report(report), curator.SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))
		self.assertEqual(curator.KNOWLEDGE_SEED_PATH.read_bytes(), (ROOT / curator.KNOWLEDGE_PATH).read_bytes())

	def test_check_refuses_a_missing_or_changed_knowledge_note(self) -> None:
		import shutil
		import tempfile

		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			for path in (curator.DEFINITION_PATH, curator.SEED_PATH, curator.SPATIAL_REPORT_PATH, curator.SPATIAL_REPORT_MARKDOWN_PATH, ROOT / curator.KNOWLEDGE_PATH):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			note = root / curator.KNOWLEDGE_PATH
			note.write_bytes(note.read_bytes() + b"\n")
			with self.assertRaisesRegex(RuntimeError, "knowledge note"):
				curator.check(root)
			note.unlink()
			with self.assertRaisesRegex(RuntimeError, "knowledge note"):
				curator.check(root)

	def test_identity_and_status(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("gottlieb.black-hole.1981", 307, "668", 1981), (machine["id"], machine["ipdb_id"], machine["model_number"], machine["year"]))
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["input_semantics", "spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		conflicts = {item["id"]: item for item in self.definition["conflicts"]}
		self.assertEqual({"conflict.tilt-pop-bumper-lights"}, set(conflicts))
		conflict = conflicts["conflict.tilt-pop-bumper-lights"]
		self.assertEqual(("outputs.relay.tilt-t", "unresolved"), (conflict["path"], conflict["status"]))
		self.assertIn("Resolution path:", conflict["description"])
		self.assertEqual("pinmame.gts80", self.definition["controller"]["platform"])
		self.assertEqual("0x200000000", self.definition["controller"]["hardware_generation"])

	def test_all_five_drivers_belong_to_this_machine(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertEqual("compatible", drivers["blkholea"]["physical_compatibility"])
		self.assertEqual("gts80s", drivers["blkholea"]["clone_of"])
		self.assertEqual({"identical"}, {drivers[name]["physical_compatibility"] for name in ("blckhole", "blkhole2")})
		for name in ("blkhole7", "blkhol7s"):
			overrides = {item["target"]: (item["segment_start"], item["width"]) for item in drivers[name]["display_overrides"]}
			self.assertEqual({"display.player-1-score": (2, 7), "display.player-2-score": (9, 7), "display.player-3-score": (22, 7), "display.player-4-score": (29, 7)}, overrides)
		for retired in curator.RETIRED_ARTIFACTS:
			self.assertFalse(retired.exists(), retired)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		owners = {driver["id"]: driver["machine_id"] for driver in catalog["drivers"] if driver["id"] in DRIVER_IDS}
		self.assertEqual({name: "gottlieb.black-hole.1981" for name in DRIVER_IDS}, owners)

	def test_profile_rules_cover_exactly_the_enumerated_addresses(self) -> None:
		for group_id, devices in ((SWITCH, self.switches), (SOLENOID, self.solenoids), (LAMP, self.lamps), (DIP, self.dips)):
			rules = self.groups[group_id]["address_rules"]
			for address in devices:
				self.assertTrue(allowed(address, rules), (group_id, address))
		expected_switches = set(range(-8, 0)) | {10 * row + col for row in range(8) for col in range(8)} | set(range(111, 119))
		self.assertEqual(expected_switches, set(self.switches))
		self.assertEqual(set(range(1, 12)) | {45, 46, 47, 48}, set(self.solenoids))
		self.assertEqual(set(range(64)), set(self.lamps))
		self.assertEqual(set(range(1, 43)), set(self.dips))

	def test_switch_dispositions(self) -> None:
		availability = {address: device["availability"] for address, device in self.switches.items()}
		unused = {address for address, value in availability.items() if value == "unused"}
		self.assertEqual({-8, -7, -6, -5, -3, -2, 36, 44, 45, 46, 54, 55, 56, 63, 64, 65, 66, 73, 74, 75, 76, 111, 113, 115, 116, 117, 118}, unused)
		self.assertEqual({57, 67, 77}, {address for address, value in availability.items() if value == "unknown"})
		self.assertTrue(self.switches[-1]["normally_closed"])
		used = {address for address, value in availability.items() if value == "used"}
		self.assertEqual({-1}, {address for address in used if self.switches[address]["normally_closed"]})
		self.assertIn("Tilt Switch", self.switches[26]["label"])
		self.assertIn("Black Hole Rollover", self.switches[33]["label"])
		self.assertIn("Track Switch", self.switches[53]["label"])
		self.assertIn("Ball Tube", self.switches[43]["label"])
		self.assertEqual(4, len(self.switches[6]["spatial"]["placements"]))

	def test_solenoids_follow_the_schematics_not_note_a(self) -> None:
		expected = {
			1: ("coil.upper-hole-bank-reset", "used"), 2: ("coil.upper-black-bank-reset", "used"),
			3: ("coil.coin-counter-left-chute", "optional"), 4: ("coil.coin-counter-right-chute", "optional"),
			5: ("coil.lower-yellow-bank-reset", "used"), 6: ("coil.lower-white-bank-reset", "used"),
			7: ("coil.coin-counter-center-chute", "optional"), 8: ("coil.knocker", "used"), 9: ("coil.outhole-kicker", "used"),
			10: ("virtual.game-on", "used"), 11: ("virtual.tilt-relay-state", "used"),
		}
		self.assertEqual(expected, {address: (self.solenoids[address]["id"], self.solenoids[address]["availability"]) for address in range(1, 12)})
		self.assertIn("A3J4-7", self.solenoids[1]["wiring"]["drive_connection"])
		self.assertIn("A3J4-8", self.solenoids[9]["wiring"]["drive_connection"])

	def test_lamp_drivers_that_drive_coils_and_relays(self) -> None:
		kinds = {address: (self.lamps[address]["kind"], self.lamps[address]["id"]) for address in (0, 1, 2, 8, 9, 12, 13, 14, 15, 16, 17, 18)}
		self.assertEqual({
			0: ("relay", "relay.game-over-q"), 1: ("relay", "relay.tilt-t"), 2: ("coil", "coil.coin-lockout"),
			8: ("coil", "coil.lower-ball-gate"), 9: ("control_signal", "control.sound-16"), 12: ("coil", "coil.lower-hole-kicker"),
			13: ("coil", "coil.upper-hole-kicker"), 14: ("coil", "coil.ball-lift-kicker"), 15: ("coil", "coil.trough-ball-gate"),
			16: ("relay", "relay.upper-playfield-u"), 17: ("relay", "relay.lower-playfield-l"), 18: ("coil", "coil.reentry-wireform-gate"),
		}, kinds)
		self.assertEqual("lamp.high-game-to-date-lightbox", self.lamps[10]["id"])
		self.assertEqual("lamp.game-over-lightbox", self.lamps[11]["id"])
		# Z3 follows the latch order on the drawn transistor lines; only the printed L labels are swapped.
		for address, pin, transistor in ((10, "A3J2-7", "Q11 MPS-A13"), (11, "A3J2-8", "Q12 MPS-A13")):
			wiring = self.lamps[address]["wiring"]
			self.assertEqual((pin, transistor), (wiring["drive_connection"], wiring["driver_transistor"]), address)
			self.assertIn(f"on {pin}", self.lamps[address]["physical"]["notes"], address)
		self.assertEqual({"virtual"}, {self.lamps[address]["kind"] for address in range(52, 64)})
		self.assertEqual({"unused"}, {self.lamps[address]["availability"] for address in range(61, 64)})
		self.assertEqual(3, self.lamps[19]["physical"]["quantity"])
		self.assertEqual(3, self.lamps[20]["physical"]["quantity"])
		self.assertEqual(2, self.lamps[3]["physical"]["quantity"])

	def test_spot_target_lamps_are_the_inverse_of_44_to_47(self) -> None:
		relationships = {(item["source"], item["destination"]): item["kind"] for item in self.definition["relationships"]}
		for low, high in zip(range(44, 48), range(48, 52)):
			self.assertEqual("inverted", relationships[(self.lamps[low]["id"], self.lamps[high]["id"])])
		self.assertEqual("inverted", relationships[("relay.tilt-t", "virtual.game-on")])
		for identifier in ("right-flipper-power", "right-flipper-hold", "left-flipper-power", "left-flipper-hold"):
			self.assertEqual("relay_gated", relationships[("virtual.game-on", f"virtual.{identifier}-synthetic")])

	def test_flipper_mechanisms_name_both_playfield_relays(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for side in ("right", "left"):
			behavior = mechanisms[f"mech.{side}-flippers"]["behavior"]
			self.assertIn("U relay", behavior)
			self.assertIn("L relay", behavior)
		self.assertEqual(["relay.upper-playfield-u", "relay.lower-playfield-l"], mechanisms["mech.playfield-select-relays"]["actuators"])

	def test_geometry_orders_and_sides(self) -> None:
		black = [first_point(self.switches[address]) for address in (3, 13, 23, 4, 14)]
		self.assertEqual(black, sorted(black, key=lambda point: -point[1]), "B is the lowest and K the highest left-bank target")
		self.assertTrue(all(x < 0.5 for x, _ in black))
		hole = [first_point(self.switches[address]) for address in (2, 12, 22, 32)]
		self.assertEqual(hole, sorted(hole, key=lambda point: point[1]), "H is the highest and E the lowest right-bank target")
		self.assertTrue(all(x > 0.5 for x, _ in hole))
		tops = [first_point(self.switches[address]) for address in (0, 10, 20)]
		self.assertEqual(tops, sorted(tops))
		spots = [first_point(self.switches[address]) for address in (1, 11, 21, 31)]
		self.assertEqual(spots, sorted(spots, key=lambda point: point[1]))
		self.assertLess(first_point(self.switches[5])[0], 0.1)
		yellow = [first_point(self.switches[address]) for address in (40, 50, 60, 70)]
		self.assertEqual(yellow, sorted(yellow, key=lambda point: -point[1]), "40 is nearest the player")
		white = [first_point(self.switches[address]) for address in (41, 51, 61)]
		self.assertEqual(white, sorted(white, key=lambda point: -point[0]), "41 is the right end")
		self.assertGreater(first_point(self.lamps[48])[1], first_point(self.lamps[30])[1])
		for address, device in self.lamps.items():
			for placement in device.get("spatial", {}).get("placements", []):
				self.assertEqual("observed", placement["provenance"]["status"], address)

	def test_profile_notes_state_the_numbering_and_the_inverted_column(self) -> None:
		self.assertIn("strobe `n/10`, return `n%10`", self.groups[SWITCH]["notes"])
		self.assertIn("`lampMatrix[6] = data ^ 0x0f`", self.groups[LAMP]["notes"])
		self.assertIn("`10` | Synthetic", self.groups[SOLENOID]["notes"])
		self.assertEqual(curator.PINMAME_REVISION, self.profile["sources"][0]["revision"])

	def test_committed_scenarios_match_their_pinned_hashes(self) -> None:
		for name, (game, _run_sha, scenario, scenario_sha) in curator.HARNESS_RUNS.items():
			path = SCENARIO_DIR / scenario
			self.assertEqual(scenario_sha, hashlib.sha256(path.read_bytes()).hexdigest(), name)
			self.assertEqual(game, load_json(path)["game"], name)
		self.assertEqual({path.name for path in SCENARIO_DIR.glob("*.json")}, {item[2] for item in curator.HARNESS_RUNS.values()})


class BlackHoleRetainedTableTests(unittest.TestCase):
	def test_retained_extraction_matches_its_manifest(self) -> None:
		root = curator.configured_vpx_sources_root(required=False)
		if root is None or not (root / curator.EXTRACTION_MANIFEST_RELATIVE_PATH).is_file():
			self.skipTest("retained Black Hole extraction is not configured")
		curator.verify_extraction_manifest(root)
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())
		text = script.read_bytes().decode("windows-1252")
		for needle in ("vpmNudge.TiltSwitch=26", "' Upper Playfield Relay", "if Controller.Lamp(16) = 0 Then", "If Controller.Lamp(17) Then", "NFadeLm 2, BLight1b"):
			self.assertIn(needle, text)


class BlackHoleRuntimeEvidenceTests(unittest.TestCase):
	"""Re-derive the harness claims from the retained raw runs when the working root is present."""

	@classmethod
	def setUpClass(cls) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		cls.root = resolve_working_root(ROOT) / "runtime-evidence" / curator.RUNTIME_DIRECTORY
		if not (cls.root / "manifest.json").is_file():
			raise unittest.SkipTest("retained Black Hole runtime evidence is not present")

	def run_json(self, name: str) -> dict:
		return load_json(self.root / name / "run.json")

	def test_manifest_and_run_identities(self) -> None:
		manifest_bytes = (self.root / "manifest.json").read_bytes()
		manifest = json.loads(manifest_bytes)
		self.assertEqual(curator.RUNTIME_MANIFEST, (len(manifest["files"]), sum(item["size"] for item in manifest["files"]), hashlib.sha256(manifest_bytes).hexdigest()))
		for item in manifest["files"]:
			self.assertEqual(item["sha256"], hashlib.sha256((self.root / item["path"]).read_bytes()).hexdigest(), item["path"])
		for name, (game, run_sha, _scenario, scenario_sha) in curator.HARNESS_RUNS.items():
			run_path = self.root / name / "run.json"
			self.assertEqual(run_sha, hashlib.sha256(run_path.read_bytes()).hexdigest(), name)
			run = self.run_json(name)
			self.assertEqual((game, scenario_sha, curator.LIBRARY_SHA256), (run["game"], run["scenario"]["sha256"], run["library_sha256"]), name)
			self.assertIsNone(run["failure"], name)

	@staticmethod
	def displays(run: dict):
		state: dict[int, list[int]] = {}
		for event in run["events"]:
			if event["event"] == "display" and event.get("segments") is not None:
				state[event["index"]] = event["segments"]
			yield event, state

	def test_solenoid_test_numbers_match_public_addresses(self) -> None:
		run = self.run_json("solenoid-test")
		digits = {0x06: 1, 0x5b: 2, 0x6d: 5, 0x7d: 6, 0x7c: 6, 0x7f: 8, 0x6f: 9, 0x67: 9}
		fired = [event for event in run["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["time_s"] > 14.5]
		order = [event["number"] for event in fired]
		self.assertEqual([1, 2, 5, 6, 8, 9], order[:6])
		shown = []
		for solenoid in fired[:6]:
			# The status digit settles within 0.1 s of the pulse; take the last value written before then.
			values = [event["segments"][0] for event in run["events"] if event["event"] == "display" and event.get("index") == 7 and event.get("segments") and event["time_s"] <= solenoid["time_s"] + 0.1]
			shown.append(digits.get(values[-1] & 0x7f))
		self.assertEqual([1, 2, 5, 6, 8, 9], shown)

	def test_switch_test_reports_each_address(self) -> None:
		seg = {0x3f: "0", 0x06: "1", 0x5b: "2", 0x4f: "3", 0x66: "4", 0x6d: "5", 0x7d: "6", 0x7c: "6", 0x07: "7", 0x7f: "8", 0x6f: "9", 0x67: "9"}
		reported: set[int] = set()
		for part in "abcde":
			run = self.run_json(f"switch-test-{part}")
			held: dict[int, float] = {}
			status: dict[int, str] = {}
			timeline = []
			for event in run["events"]:
				if event["event"] == "display" and event.get("index") in (6, 7) and event.get("segments"):
					status[event["index"]] = seg.get(event["segments"][0] & 0x7f, "?")
					timeline.append((event["time_s"], status.get(6, "") + status.get(7, "")))
				elif event["event"] == "switch" and not event.get("initial"):
					if event["state"] == 1:
						held[event["number"]] = event["time_s"]
					elif event["number"] in held:
						start = held.pop(event["number"])
						if any(start < time <= event["time_s"] and text == f"{event['number']:02d}" for time, text in timeline):
							reported.add(event["number"])
		expected = {10 * row + col for row in range(8) for col in range(8)} - {7, 47, 57, 77}
		self.assertEqual(expected, reported)

	def test_high_game_to_date_lamp(self) -> None:
		run = self.run_json("high-game-to-date")
		on = [event["time_s"] for event in run["events"] if event["event"] == "lamp" and event["number"] == 10 and event["state"] == 1]
		seven, zero = 0x07, 0x3f
		found = False
		for event in run["events"]:
			if event["event"] == "display" and event.get("index") == 8 and event.get("segments") == [seven, seven, zero, zero, zero, zero]:
				found = found or any(abs(event["time_s"] - time) < 0.1 for time in on)
		self.assertTrue(found, "the lower playfield display shows 770000 as lamp 10 lights")

	def test_tilts_and_gameplay_causality(self) -> None:
		for name in ("tilt-26", "tilt-57"):
			step = self.run_json(name)["steps"][-1]["transitions"]
			self.assertIn({"number": 1, "states": [1]}, step["lamps"], name)
			self.assertEqual({10: [0], 11: [1]}, {item["number"]: item["states"] for item in step["solenoids"]}, name)
		steps = {step["label"]: step["transitions"] for step in self.run_json("gameplay-causality")["steps"]}
		for label, solenoid in (("coin through the left chute (17)", 3), ("coin through the right chute (27)", 4), ("coin through the center chute (37)", 7)):
			self.assertEqual({solenoid: [1, 0]}, {item["number"]: item["states"] for item in steps[label]["solenoids"]}, label)
		self.assertEqual([], steps["right flipper button before a game"]["solenoids"])
		self.assertEqual({45: [1, 0], 46: [1, 0]}, {item["number"]: item["states"] for item in steps["right flipper button, upper playfield in play"]["solenoids"]})
		black = steps["black hole rollover (33)"]["lamps"]
		self.assertEqual({16, 17}, {item["number"] for item in black if item["number"] < 19})
		self.assertEqual({8: [1, 0]}, {item["number"]: item["states"] for item in steps["ball on the lower track switch (53 closed)"]["lamps"] if item["number"] < 19 and item["number"] != 9})
		self.assertIn(2, {item["number"] for item in steps["black bank drop target K (14)"]["solenoids"]})
		self.assertIn(1, {item["number"] for item in steps["hole bank drop target E (32)"]["solenoids"]})
		# The white-bank reset is a short pulse during the ball-tube closure, not held for the closure.
		events = self.run_json("gameplay-causality")["events"]
		tube = [event["time_s"] for event in events if event["event"] == "switch" and event["number"] == 43 and not event.get("initial")]
		white = [(event["time_s"], event["state"]) for event in events if event["event"] == "solenoid" and event["number"] == 6 and tube[0] <= event["time_s"] <= tube[1]]
		self.assertEqual([1, 0], [state for _time, state in white])
		self.assertLess(white[1][0] - white[0][0], 0.3)
		self.assertGreater(tube[1] - tube[0], 3.0)


if __name__ == "__main__":
	unittest.main()
