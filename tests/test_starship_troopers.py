from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import curate_starship_troopers as curator  # noqa: E402
import starship_troopers_runtime_evidence as evidence_tool  # noqa: E402
import starship_troopers_spatial_seed as seed_tool  # noqa: E402

MACHINE_ID = "sega.starship-troopers.1997"
DEFINITION_PATH = ROOT / "machines" / "partial" / "sega" / "starship-troopers-1997.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "sega" / "starship-troopers-1997.json"
SEED_PATH = ROOT / "tools" / "seeds" / "sega" / "starship-troopers-1997-spatial.json"
EVIDENCE_201_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "starship-troopers-startrp-gameplay.json"
EVIDENCE_200_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "starship-troopers-startrp2-gameplay.json"
EXCERPT_DIRECTORY = ROOT / "evidence" / "excerpts" / MACHINE_ID
RUNS = ((EVIDENCE_201_PATH, "startrp-gameplay"), (EVIDENCE_200_PATH, "startrp2-gameplay"))

DRIVER_IDS = {"startrp", "startrp2"}
# The Switch Matrix Grid's NOT USED cells and page 21's "The following switches are not used" (excerpt switch-matrix.md).
NOT_USED_SWITCHES = {1, 8, 11, 36, 44, 63, 64}
# The European 4th coin slot and the two coin-door positions printed (Future Use).
OPTIONAL_SWITCHES = {2, 3, 7}
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def steps(path: Path, run: str) -> dict[str, dict]:
	prefix = f"{run} "
	return {item["label"].split(": ", 1)[1].split(";")[0]: item for item in load(path)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(prefix)}


def solenoid_states(item: dict) -> dict[int, list[int]]:
	"""The per-solenoid state sequences the extractor writes into a step's label, in recorded order."""
	match = re.search(r"; solenoid states during the step: (.*?)(?:; GI 0 states|$)", item["label"])
	if not match:
		return {}
	result = {}
	for part in match.group(1).split("; "):
		number, states = part.split(" = ")
		result[int(number)] = [int(state) for state in states.split(", ")]
	return result


class StarshipTroopersTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.by_binding = {(item["binding"]["group"], item["binding"]["device"]): item for item in cls.definition["inputs"] + cls.definition["outputs"]}

	def device(self, group: str, address: int) -> dict:
		return self.by_binding[(f"pinmame.{group}", address)]

	def test_identity_drivers_and_the_honest_gate(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, 4341, "G5we0-MDx6b", 1997, "59"), (machine["id"], machine["ipdb_id"], machine["opdb_id"], machine["year"], machine["model_number"]))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual({"startrp": "identical", "startrp2": "identical"}, {key: value["physical_compatibility"] for key, value in drivers.items()})
		self.assertEqual("startrp", drivers["startrp2"]["clone_of"])
		self.assertNotIn("clone_of", drivers["startrp"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertEqual([], self.definition["conflicts"])
		catalog = load(ROOT / "catalog/pinmame.json")
		claimed = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(DRIVER_IDS, claimed)

	def test_every_public_address_is_declared_exactly_once(self) -> None:
		def addresses(group: str) -> set[int]:
			return {item["binding"]["device"] for item in self.definition["inputs"] + self.definition["outputs"] if item["binding"]["group"] == group}
		self.assertEqual(set(range(-3, 1)) | set(range(1, 65)) | set(range(81, 89)), addresses("pinmame.input.switch"))
		self.assertEqual(set(range(1, 9)), addresses("pinmame.input.dip"))
		self.assertEqual(set(range(1, 51)), addresses("pinmame.output.solenoid"))
		self.assertEqual(set(range(1, 81)), addresses("pinmame.output.lamp"))
		self.assertEqual({0}, addresses("pinmame.output.gi"))
		keys = [(item["binding"]["group"], item["binding"]["device"]) for item in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(keys), len(set(keys)))

	def test_unused_and_optional_cells_follow_the_grids(self) -> None:
		unused = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "unused"}
		self.assertEqual(NOT_USED_SWITCHES, unused)
		optional = {address for address in range(1, 65) if self.device("input.switch", address)["availability"] == "optional"}
		self.assertEqual(OPTIONAL_SWITCHES, optional)
		self.assertEqual({33}, {address for address in range(1, 81) if self.device("output.lamp", address)["availability"] == "unused"})
		self.assertEqual({8, 24}, {address for address in range(1, 51) if self.device("output.solenoid", address)["availability"] == "optional"})
		# The coil chart's two NOT USED rows, and the remapped right flipper's empty public 16.
		self.assertEqual({16, 21, 22}, {address for address in range(1, 33) if self.device("output.solenoid", address)["availability"] == "unused"})
		self.assertEqual({85, 86, 87}, {address for address in range(81, 89) if self.device("input.switch", address)["availability"] == "unused"})
		mini = self.device("input.switch", 88)
		self.assertEqual(("used", ["flipper.mini.right.button"]), (mini["availability"], mini["roles"]))
		self.assertEqual({1, 2, 3, 4, 5}, {number for number in range(1, 9) if self.device("input.dip", number)["availability"] == "used"})

	def test_polarity_follows_the_read_path_and_the_wiring_diagrams(self) -> None:
		for address in range(1, 65):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertTrue(self.device("input.switch", 81)["normally_closed"])
		self.assertTrue(self.device("input.switch", 83)["normally_closed"])
		# The EOS contacts are N.C., but PinMAME rewrites 81 and 83 from the flipper outputs (FLIP_SOL includes FLIP_EOS):
		# nothing tells a host to drive or initialize them, and the buttons' notes describe the ROM driving the coils.
		for address in (81, 83):
			eos = self.device("input.switch", address)
			self.assertNotIn("initial_active", eos, address)
			self.assertIn("FLIP_SOL includes FLIP_EOS", eos["physical"]["notes"], address)
			self.assertIn("A host write is overwritten", eos["physical"]["notes"], address)
			self.assertNotIn("whatever the host writes", eos["physical"]["notes"], address)
		for address in (82, 84):
			notes = self.device("input.switch", address)["physical"]["notes"]
			self.assertIn("dedswitch_r and drives the", notes, address)
			self.assertNotIn("copies into the lower-flipper outputs", notes, address)
		knowledge = (ROOT / "knowledge" / "sega" / "starship-troopers-1997.md").read_text(encoding="utf-8")
		self.assertNotIn("81 and 83 at 1", knowledge)
		self.assertIn("Leave 81 and 83 alone", knowledge)
		for address in (82, 84, 88, -3, -2, -1, 0):
			self.assertFalse(self.device("input.switch", address)["normally_closed"], address)
		self.assertEqual({12, 13, 14, 15}, {address for address in range(1, 65) if self.device("input.switch", address).get("initial_active")})
		self.assertTrue(self.device("input.switch", -3)["initial_active"])
		self.assertEqual({15, 47, 48}, {address for address in range(1, 65) if self.device("input.switch", address).get("physical", {}).get("switch_type") == "opto"})
		# The warrior bug target rides the carriage on a stack switch, not the roller micro switch the shared cell repeats.
		target = self.device("input.switch", 35)["physical"]
		self.assertEqual(("leaf", "180-5133-00"), (target["switch_type"], target["part_number"]))
		self.assertEqual("unknown", self.device("input.switch", 16)["physical"]["switch_type"])

	def test_flipper_remap_and_synthetic_states(self) -> None:
		left = self.device("output.solenoid", 48)
		right = self.device("output.solenoid", 46)
		self.assertEqual(("device.q15-left-flipper", "coil"), (left["id"], left["kind"]))
		self.assertEqual(("device.q16-right-flipper", "coil"), (right["id"], right["kind"]))
		self.assertEqual(("device.q14-mini-flipper", "coil", "used"), (self.device("output.solenoid", 14)["id"], self.device("output.solenoid", 14)["kind"], self.device("output.solenoid", 14)["availability"]))
		for address in (15, 45, 47):
			self.assertEqual(("virtual", "used"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		for address in (16, *range(33, 45), 49, 50):
			self.assertEqual(("virtual", "unused"), (self.device("output.solenoid", address)["kind"], self.device("output.solenoid", address)["availability"]), address)
		kinds = {address: self.device("output.solenoid", address)["kind"] for address in range(1, 33) if address not in (15, 16)}
		self.assertEqual({23, 25, 26, 27, 28, 29, 30, 31, 32}, {address for address, kind in kinds.items() if kind == "flasher"})
		self.assertEqual({17, 18, 19, 20}, {address for address, kind in kinds.items() if kind == "motor"})
		self.assertEqual({5, 6}, {address for address, kind in kinds.items() if kind == "magnet"})

	def test_both_drivers_publish_the_game_on_state(self) -> None:
		# 15 rises once when the served ball reaches the shooter lane and falls once at the drain, in both runs.
		for path, run in RUNS:
			observed = steps(path, run)
			served = observed["the served ball rests on the shooter lane switch 16"]
			drained = observed["the ball drains: trough position 12 fills again"]
			self.assertEqual([1], solenoid_states(served)[15], run)
			self.assertEqual([0], solenoid_states(drained)[15], run)
			self.assertNotIn(15, drained["active_solenoid_addresses"], run)
			between = [item for label, item in observed.items() if item is not served and item is not drained and 15 in solenoid_states(item)]
			self.assertEqual([], between, run)
			boot = next(item for item in load(path)["runtime"]["observations"]["named_action_observations"] if item["label"].startswith(f"{run} step 1:"))
			self.assertEqual(("key", "wait with no host input"), (boot["input_kind"], boot["input_name"]), run)
			self.assertNotIn("input_address", boot, run)
			# Each step's host stimulus is only the switch that step writes.
			self.assertEqual([], boot["host_stimulus_switch_addresses"], run)
			self.assertEqual([16], served["host_stimulus_switch_addresses"], run)
			self.assertEqual([47], observed["left orbit opto (public 47) closed once"]["host_stimulus_switch_addresses"], run)
			for item in load(path)["runtime"]["observations"]["named_action_observations"]:
				expected = [item["input_address"]] if item["input_kind"] == "switch" else []
				self.assertEqual(expected, item["host_stimulus_switch_addresses"], item["label"])

	def test_each_orbit_opto_fires_the_right_magnet_twice(self) -> None:
		for path, run in RUNS:
			observed = steps(path, run)
			for label in ("left orbit opto (public 47) closed once", "right orbit opto (public 48) closed once"):
				self.assertEqual([1, 0, 1, 0], solenoid_states(observed[label])[6], (run, label))

	def test_wiring_comes_from_the_printed_tables(self) -> None:
		trough = self.device("output.solenoid", 1)["wiring"]
		self.assertEqual(("Q1", "BRN-BLK", "J8-P1", "YEL-VIO", "J10-P4/5", 50), (trough["driver_transistor"], trough["control_wire"], trough["control_connection"], trough["power_wire"], trough["power_connection"], trough["nominal_voltage_v"]))
		self.assertEqual("BRN-YEL", self.device("output.solenoid", 4)["wiring"]["control_wire"])
		self.assertIn("BRY-YEL", self.device("output.solenoid", 4)["physical"]["notes"])
		# DR. 6 overprints Q7's two power colours; the detailed wiring diagram (printed page 88) puts RED/WHT between the fuse and the coil.
		self.assertEqual(("VIO-YEL / RED-WHT", "J10-P3"), (self.device("output.solenoid", 7)["wiring"]["power_wire"], self.device("output.solenoid", 7)["wiring"]["power_connection"]))
		for address in (25, 26, 27, 28):
			self.assertEqual(("165-5004-00", 4), (self.device("output.solenoid", address)["physical"]["part_number"], self.device("output.solenoid", address)["physical"]["quantity"]), address)
		# F5 mixes three #906 and one #89, so it carries a quantity and no single bulb part.
		f5 = self.device("output.solenoid", 29)["physical"]
		self.assertEqual(4, f5["quantity"])
		self.assertNotIn("part_number", f5)
		self.assertIn("165-5000-89", f5["notes"])
		self.assertEqual(("ORG-GRY", "Q15"), (self.device("output.solenoid", 48)["wiring"]["control_wire"], self.device("output.solenoid", 48)["wiring"]["driver_transistor"]))
		self.assertEqual(("ORG-VIO", "Q16"), (self.device("output.solenoid", 46)["wiring"]["control_wire"], self.device("output.solenoid", 46)["wiring"]["driver_transistor"]))
		stepper = self.device("output.solenoid", 17)["wiring"]
		self.assertEqual(("VIO-BRN", "J7-P2", "GRY-RED", "J16-P3", 12), (stepper["control_wire"], stepper["control_connection"], stepper["power_wire"], stepper["power_connection"], stepper["nominal_voltage_v"]))
		self.assertEqual("J7-P10", self.device("output.solenoid", 24)["wiring"]["control_connection"])
		switch = self.device("input.switch", 54)["wiring"]
		self.assertEqual(("GRN-VIO", "CN5-P8", "WHT-BLU", "CN7-P3"), (switch["drive_wire"], switch["drive_connection"], switch["return_wire"], switch["return_connection"]))
		for address, wire, pin in ((1, "WHT-BRN", "CN7-P9"), (8, "WHT-GRY", "CN7-P1")):
			wiring = self.device("input.switch", address)["wiring"]
			self.assertEqual((wire, pin), (wiring["return_wire"], wiring["return_connection"]), address)
		self.assertEqual(("GRY-GRN", "CN6-P7"), (self.device("input.switch", 88)["wiring"]["drive_wire"], self.device("input.switch", 88)["wiring"]["drive_connection"]))
		lamp = self.device("output.lamp", 80)["wiring"]
		self.assertEqual(("YEL-GRY", "J13-P1", "RED", "J12-P11"), (lamp["drive_wire"], lamp["drive_connection"], lamp["return_wire"], lamp["return_connection"]))
		# Lamp row 7 (Q39, CN1 pin 15) is DISP1, the WARRIOR display, per the board schematic.
		segment = self.device("output.lamp", 49)
		self.assertEqual("Warrior 7-Segment A", segment["label"])
		self.assertTrue(segment["wiring"]["return_connection"].startswith("CN1-P15"))
		self.assertEqual("Tanker 7-Segment G", self.device("output.lamp", 79)["label"])

	def test_mechanisms_reference_declared_devices(self) -> None:
		ids = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(set(mechanism["actuators"] + mechanism["sensors"]) <= ids, mechanism["id"])
		by_id = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertTrue({"mechanism.trough", "mechanism.super-vuk", "mechanism.warrior-bug", "mechanism.brain-bug", "mechanism.magnets", "mechanism.mini-flipper"} <= set(by_id))
		bug = by_id["mechanism.warrior-bug"]
		self.assertEqual(["switch.33-stepper-motor-rear"], next(position["sensors"] for position in bug["positions"] if position["id"].endswith(".rear")))
		self.assertEqual(["switch.34-stepper-motor-front"], next(position["sensors"] for position in bug["positions"] if position["id"].endswith(".front")))
		actuators = [actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))

	def test_table_defects_stay_out_of_the_conflicts(self) -> None:
		self.assertIn("crossing is a defect of the retained table", self.device("input.switch", 59)["physical"]["notes"])
		self.assertIn("crossing is a defect of the retained table", self.device("input.switch", 62)["physical"]["notes"])
		self.assertIn("table defect", self.device("output.solenoid", 8)["physical"]["notes"])
		self.assertEqual("not_applicable", self.device("output.solenoid", 8)["spatial"]["status"])

	def test_every_excerpt_is_pinned_and_every_source_is_cited(self) -> None:
		cited = set()
		for item in self.definition["inputs"] + self.definition["outputs"] + self.definition["mechanisms"] + self.definition["displays"]:
			cited.update(item["provenance"]["source_refs"])
		declared = {source["id"] for source in self.definition["sources"]}
		self.assertTrue(cited <= declared, cited - declared)
		paths = set()
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], sha256(ROOT / excerpt["path"]), excerpt["id"])
				paths.add(Path(excerpt["path"]).name)
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], sha256(ROOT / excerpt["image"]), excerpt["id"])
					paths.add(Path(excerpt["image"]).name)
		self.assertEqual({path.name for path in EXCERPT_DIRECTORY.iterdir()}, paths)

	def test_committed_text_names_no_other_machine(self) -> None:
		catalog = load(ROOT / "catalog/pinmame.json")
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID and len(driver["id"]) >= 5}
		texts = [DEFINITION_PATH.read_text(encoding="utf-8"), (ROOT / "knowledge/sega/starship-troopers-1997.md").read_text(encoding="utf-8")]
		words = set(re.findall(r"[a-z0-9_]{5,}", "\n".join(texts)))
		self.assertEqual(set(), words & foreign)

	def test_placements_are_in_range_unique_and_from_the_seed(self) -> None:
		seed = load(SEED_PATH)
		self.assertEqual(curator.TABLE_SHA256, seed["table"]["sha256"])
		placement_ids = []
		for item in self.definition["inputs"] + self.definition["outputs"]:
			spatial = item.get("spatial")
			if not spatial or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("observed", spatial["status"], item["id"])
			for placement in spatial["placements"]:
				placement_ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
		self.assertEqual(len(placement_ids), len(set(placement_ids)))
		# Only the four flashers whose bulbs the table does not model are used without a placement.
		missing = {item["id"] for item in self.definition["inputs"] + self.definition["outputs"] if item.get("availability") in {"used", "optional"} and "spatial" not in item}
		self.assertEqual({curator.q_output_id(number) for number in (23, 30, 31, 32)}, missing)
		# Every seed entry lands on a device: the power-phase addresses 45 and 47 carry no placement of their own.
		self.assertFalse({"45", "47"} & set(seed["solenoid"]))
		for category, group in (("switch", "input.switch"), ("solenoid", "output.solenoid"), ("lamp", "output.lamp")):
			for address in seed[category]:
				self.assertEqual("observed", self.device(group, int(address))["spatial"]["status"], (category, address))
		gi = self.device("output.gi", 0)
		self.assertEqual(28, len(gi["spatial"]["placements"]))
		self.assertEqual(36, gi["physical"]["quantity"])
		self.assertEqual(2, self.device("output.lamp", 40)["physical"]["quantity"])
		self.assertEqual(2, len(self.device("output.lamp", 40)["spatial"]["placements"]))
		# Flashers are placed only on script-driven Lights that sit on a modelled dome, socket or bulb; the table's glow
		# sprites and the Lights over no modelled part place nothing.
		for address in seed["solenoid"]:
			self.assertNotIn("Flasher", {entry["type"] for entry in seed["solenoid"][address]}, address)
		placed = {address: len(self.device("output.solenoid", address).get("spatial", {}).get("placements", [])) for address in (23, 25, 26, 27, 28, 29, 30, 31, 32)}
		self.assertEqual({23: 0, 25: 4, 26: 4, 27: 4, 28: 4, 29: 2, 30: 0, 31: 0, 32: 0}, placed)
		self.assertEqual({"23": ["l123a", "l123b"], "30": ["l130b", "l130c", "l130d"], "31": ["l131b", "l131c", "l131d"], "32": ["l132"]}, seed["unplaced_solenoid_lights"])
		domes = {25: "CapsRed", 26: "CapsYellow", 27: "CapsGreen", 28: "CapsBlue"}
		for address in (25, 26, 27, 28, 29):
			expected = [domes[address], "KabeSockel"] if address in domes else ["WarriorBugAssembly006"]
			for entry, placement in zip(seed["solenoid"][str(address)], self.device("output.solenoid", address)["spatial"]["placements"]):
				self.assertEqual(expected, [mesh["object"] for mesh in entry["mesh"]], entry["object"])
				self.assertTrue(all(mesh["distance"] < 8 for mesh in entry["mesh"]), entry["object"])
				self.assertIn(curator.VPX_OBJ_SOURCE, placement["provenance"]["source_refs"])
		for address in (23, 30, 31, 32):
			self.assertNotIn("spatial", self.device("output.solenoid", address), address)
		# A projection, or a table-derived point checked against a drawing, cites the manual; a plain table object does not.
		for category, group in (("switch", "input.switch"), ("solenoid", "output.solenoid"), ("lamp", "output.lamp")):
			for address, entries in seed[category].items():
				placements = self.device(group, int(address))["spatial"]["placements"]
				for entry, placement in zip(entries, placements):
					self.assertEqual("projection" in entry or "drawing" in entry, curator.MANUAL_SOURCE in placement["provenance"]["source_refs"], (category, address))
		# The warrior bug's one motor sits at the rear end of its track, beside the plastic that carries lamp 34.
		for address in (17, 18, 19, 20):
			self.assertEqual(["BWall24"], [entry["object"] for entry in seed["solenoid"][str(address)]], address)
			self.assertIn("printed page 78", seed["solenoid"][str(address)][0]["projection"])
		# Each 7-segment segment is its texture's lit centroid on its own Flasher quad, in the A-G arrangement of the key.
		for first in (49, 57, 65, 73):
			points = {}
			for offset, letter in enumerate("ABCDEFG"):
				(entry,) = seed["lamp"][str(first + offset)]
				self.assertEqual(("Flasher", f"l{first + offset}"), (entry["type"], entry["object"]))
				self.assertEqual({"image", "u", "v"}, set(entry["segment"]))
				self.assertIn("A-G arrangement", entry["drawing"])
				points[letter] = (entry["x"], entry["y"])
			self.assertTrue(points["A"][1] < points["G"][1] < points["D"][1], first)
			self.assertTrue(points["F"][0] < points["A"][0] < points["B"][0] and points["E"][0] < points["D"][0] < points["C"][0], first)
			self.assertTrue(points["B"][1] < points["C"][1] and points["F"][1] < points["E"][1], first)
		# The lamps on bulbs the table models cite the mesh export; the Tanker Bug sign stands upright with 39's bulb lowest.
		bulbs = {28: "bulbs_red", 29: "bulbs_red", 30: "bulbs_red", 35: "bulbs_yellow", 36: "bulbs_red", 39: "bulbs_blue", 47: "bulbs_red", 48: "bulbs_red"}
		for address, entries in seed["lamp"].items():
			for entry, placement in zip(entries, self.device("output.lamp", int(address))["spatial"]["placements"]):
				meshes = [mesh["object"] for mesh in entry.get("mesh", [])]
				self.assertEqual([bulbs[int(address)]] if int(address) in bulbs else [], meshes, address)
				self.assertEqual(bool(meshes), curator.VPX_OBJ_SOURCE in placement["provenance"]["source_refs"], address)
				self.assertTrue(all(mesh["distance"] < 8 for mesh in entry.get("mesh", [])), address)
		sign = {address: seed["lamp"][str(address)][0]["mesh"][0] for address in (35, 36, 39)}
		self.assertLess(sign[39]["height"][1], min(sign[35]["height"][0], sign[36]["height"][0]))
		self.assertLessEqual(max(mesh["y"] for mesh in sign.values()) - min(mesh["y"] for mesh in sign.values()), 2.0)
		for address in (35, 36, 39):
			self.assertIn("Tanker Bug Sign", seed["lamp"][str(address)][0]["drawing"])
		# A lamp DR. 5 draws below the playfield lights an insert the table models no bulb under: it is a disclosed
		# projection onto its insert light, and no lamp is placed at a bare render light.
		inserts = {int(address) for address, entries in seed["lamp"].items() for entry in entries if entry["type"] == "Light" and "mesh" not in entry}
		self.assertEqual(set(range(1, 28)) | {31, 32, 37, 38, 40} | set(range(41, 47)) | {56, 64, 72, 80}, inserts)
		self.assertEqual(43, sum(len(seed["lamp"][str(address)]) for address in inserts))
		for address in inserts:
			for entry in seed["lamp"][str(address)]:
				self.assertIn("mounted below the playfield", entry["projection"], address)
				self.assertIn("not a measured socket", entry["projection"], address)
		self.assertEqual(sorted(inserts), curator.seed_tool_inserts())
		# An emitter on a modelled socket or bulb is placed at that piece's centre, not at its render Light.
		anchored = [entry for entries in list(seed["solenoid"].values()) + list(seed["lamp"].values()) for entry in entries if "mesh" in entry]
		self.assertEqual(26, len(anchored))
		for entry in anchored:
			(anchor,) = [mesh for mesh in entry["mesh"] if mesh["object"] == entry["anchor"]]
			self.assertIn(entry["anchor"], {"KabeSockel", "WarriorBugAssembly006", "bulbs_red", "bulbs_yellow", "bulbs_blue"}, entry["object"])
			self.assertEqual((round(anchor["x"] / 952.0, 6), round(anchor["y"] / 2133.17, 6)), (entry["x"], entry["y"]), entry["object"])
			self.assertNotEqual((entry["light"]["x"], entry["light"]["y"]), (entry["x"], entry["y"]), entry["object"])
		dmd = self.definition["displays"][0]
		self.assertIn(curator.MANUAL_SOURCE, dmd["spatial"]["provenance"]["source_refs"])

	def test_the_curator_reproduces_every_artifact(self) -> None:
		curator.check(ROOT)

	def test_the_seed_builder_refuses_an_unpinned_extraction(self) -> None:
		# The builder reads no coordinate from an extraction that is not, file for file, the pinned one.
		with tempfile.TemporaryDirectory() as directory:
			extraction = Path(directory) / "extracted"
			(extraction / "gameitems").mkdir(parents=True)
			(extraction / "gameitems" / "Trigger.sw16.json").write_bytes(b'{"Trigger": {"center": {"x": 838.0, "y": 1650.0}}}\n')
			with self.assertRaisesRegex(SystemExit, "not the pinned retained extraction"):
				seed_tool.build(extraction, Path(directory) / "table.vpx", Path(directory) / "table.obj")

	def test_scenarios_name_only_their_game_and_evidence_pins_its_runs(self) -> None:
		manifests = {}
		for path, game, rom in ((EVIDENCE_201_PATH, "startrp", curator.ROM_ARCHIVE_SHA256), (EVIDENCE_200_PATH, "startrp2", curator.ROM_200_ARCHIVE_SHA256)):
			document = load(path)
			self.assertEqual(LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(curator.RUNTIME_LIBRARY_SHA256, document["runtime"]["emulator"]["sha256"])
			self.assertEqual(rom, document["runtime"]["rom_archive_sha256"])
			self.assertEqual(curator.PINMAME_REVISION, document["source"]["revision"])
			relative = path.relative_to(ROOT).as_posix()
			self.assertEqual((game, rom), evidence_tool.DOCUMENTS[relative][:2])
			self.assertEqual(set(evidence_tool.DOCUMENTS[relative][2]), {run["name"] for run in document["runtime"]["raw_runs"]})
			manifests.update(evidence_tool.DOCUMENTS[relative][2])
			for run in document["runtime"]["raw_runs"]:
				scenario = ROOT / run["scenario_path"]
				self.assertEqual(run["scenario_sha256"], sha256(scenario), run["name"])
				self.assertEqual(game, load(scenario)["game"])
				self.assertNotIn(b"\r", scenario.read_bytes(), run["name"])
				# The coverage the sources state: every placed matrix switch but the ones the scenario never toggles, which it
				# either holds from boot (13-15 and 33 closed, 34 open) or never writes (37 and 39).
				toggled = {action["switch"] for action in load(scenario)["actions"] if "switch" in action}
				initial = {item["switch"]: item["state"] for item in load(scenario)["initial_switches"]}
				placed = {address for address in range(1, 65) if self.device("input.switch", address).get("spatial", {}).get("status") == "observed"}
				self.assertEqual(set(curator.UNTOGGLED_MATRIX_SWITCHES), placed - toggled, run["name"])
				self.assertEqual({13: 1, 14: 1, 15: 1, 33: 1, 34: 0}, {address: state for address, state in initial.items() if address in placed - toggled}, run["name"])
				self.assertFalse({81, 83} & (set(initial) | toggled), run["name"])
		for source in self.definition["sources"]:
			if source["kind"] == "runtime_scenario":
				self.assertIn(curator.HARNESS_COVERAGE, source["locator"], source["id"])
		self.assertEqual(manifests, curator.RUN_MANIFESTS)

	def test_gameplay_steps_support_the_switch_to_coil_claims(self) -> None:
		expected = {
			"left turbo bumper (public 49) closed once": {9}, "bottom turbo bumper (public 50) closed once": {10}, "right turbo bumper (public 51) closed once": {11},
			"left slingshot (public 59) closed once": {12}, "right slingshot (public 62) closed once": {13}, "Start button (public 54)": {1, 32},
			"coin 1 on the center coin slot (public 5)": {24, 25, 26, 27, 28}, "a ball enters the VUK (public 45) and stays": {3, 4, 27, 30, 32},
			"a ball enters the super VUK (public 46) and stays": {4, 32}, "left orbit opto (public 47) closed once": {6}, "right orbit opto (public 48) closed once": {6},
			"warrior bug target (stepper motor bug, public 35) closed once": {18, 29}, "under-trough bug hole (public 10) closed once": {19, 26, 27, 29},
			"left bottom stand-up, green (public 17) closed once": {27}, "left middle stand-up, yellow (public 18) closed once": {26},
			"right ramp stand-up, yellow (public 32) closed once": {25, 26, 27, 28, 32}, "right top lane (public 43) closed once": {32},
			"left outlane (public 57) closed once": {30}, "right outlane (public 60) closed once": {31},
			"mini flipper button (dedicated DS-5, public 88) held 1.5 s": {14},
			"left flipper button (public 84) held 1.5 s": {47, 48},
			"the ball drains: trough position 12 fills again": {1, 25, 26, 27, 28, 32},
		}
		quiet = (
			"left middle stand-up, red (public 19) closed once", "right bottom stand-up, red (public 21) closed once", "pop stand-up, blue (public 28) closed once",
			"VUK stand-up, green (public 30) closed once", "VUK stand-up, blue (public 31) closed once", "left ramp enter (public 25) closed once",
			"left ramp exit (public 26) closed once", "right ramp enter (public 52) closed once", "right ramp exit (public 53) closed once",
			"left top lane (public 41) closed once", "middle top lane (public 42) closed once", "left return lane (public 58) closed once",
			"right return lane (public 61) closed once", "brain bug hit (public 38) closed once", "under-trough skill shot (public 9) closed once",
			"under-trough pop exit hole (public 40) closed once",
			"one ball has left the trough: the left-most trough position 12 empties as the stack shifts toward the up-kicker",
		)
		for path, run in RUNS:
			observed = steps(path, run)
			for label, coils in expected.items():
				self.assertTrue(coils <= set(observed[label]["active_solenoid_addresses"]), (run, label))
			for label in quiet:
				self.assertEqual([], observed[label]["active_solenoid_addresses"], (run, label))
			# The right flipper step carries the ball search; the flipper pair is all the button itself explains.
			self.assertTrue({45, 46, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14} <= set(observed["right flipper button (public 82) held 1.5 s"]["active_solenoid_addresses"]), run)
			seen = set(load(path)["runtime"]["observations"]["solenoid_addresses_seen"])
			self.assertFalse(seen & {8, 21, 22, 23}, run)
			# A step counts as observed when a solenoid or the G.I. changed during it.
			for item in load(path)["runtime"]["observations"]["named_action_observations"]:
				result = "observed" if item["transitioned_solenoid_addresses"] or "GI 0 states" in item["label"] else "no_matching_transition"
				self.assertEqual(result, item["result"], item["label"])
			for label in ("left ramp exit (public 26) closed once", "right ramp exit (public 53) closed once", "under-trough pop exit hole (public 40) closed once"):
				self.assertEqual(([], "observed"), (observed[label]["transitioned_solenoid_addresses"], observed[label]["result"]), (run, label))
			# The brain bug hit was closed while Q7 was off: no coil, flasher or G.I. change answered it.
			brain = observed["brain bug hit (public 38) closed once"]
			self.assertEqual(([], "no_matching_transition"), (brain["active_solenoid_addresses"], brain["result"]), run)
			self.assertNotIn("GI 0", brain["label"], run)
			self.assertEqual(set(range(1, 81)), set(load(path)["runtime"]["observations"]["lamp_addresses_seen"]), run)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_compact_runtime_evidence_matches_the_retained_raw_runs(self) -> None:
		from pinmame_game_defs.jsonio import canonical_bytes

		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"])
		for relative, (game, rom, runs) in evidence_tool.DOCUMENTS.items():
			self.assertEqual(canonical_bytes(evidence_tool.build(root, game, rom, runs)), (ROOT / relative).read_bytes(), relative)
			# The source names the one retained file its digest covers: that run's manifest.
			source = load(ROOT / relative)["source"]
			prefix = "external:pinmame-review-artifacts/"
			self.assertTrue(source["path"].startswith(prefix) and source["path"].endswith("/manifest.json"), relative)
			self.assertEqual(source["sha256"], sha256(root / source["path"][len(prefix):]), relative)

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_raw_runs_show_the_game_on_edges_and_the_orbit_magnet_timing(self) -> None:
		for name in curator.RUN_MANIFESTS:
			events = load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")["events"]
			edges = [event["state"] for event in events if event["event"] == "solenoid" and event["number"] == 15]
			self.assertEqual([1, 0], edges, name)
			for address in (47, 48):
				written = next(event["time_s"] for event in events if event["event"] == "switch" and event["number"] == address and event["state"] == 1)
				released = next(event["time_s"] for event in events if event["event"] == "switch" and event["number"] == address and event["state"] == 0)
				rise = next(event["time_s"] for event in events if event["event"] == "solenoid" and event["number"] == 6 and event["state"] == 1 and event["time_s"] > written)
				# The ROM answers while the input is still 1: the notes' polarity proof for the orbit optos.
				self.assertLess(rise, released, (name, address))
				self.assertLessEqual(rise - written, 0.101, (name, address))

	@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review-artifacts root is not configured")
	def test_unfitted_lamp_33_carries_light_show_data(self) -> None:
		# The lamp-33 note says the ROM wrote the unfitted cell 100 times in each run, as often as its row neighbour 35.
		for name in curator.RUN_MANIFESTS:
			events = load(Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / evidence_tool.HARNESS_DIRECTORY / name / "run.json")["events"]
			counts = {number: sum(1 for event in events if event["event"] == "lamp" and event["number"] == number and not event.get("initial")) for number in (33, 35)}
			self.assertEqual({33: 100, 35: 100}, counts, name)

	@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
	def test_the_retained_extraction_script_and_seed_match(self) -> None:
		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"])
		curator.verify_extraction_manifest(root)
		table = root / curator.VPX_DIRECTORY / curator.TABLE_NAME
		self.assertEqual(curator.TABLE_SHA256, sha256(table))
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, sha256(script))
		built = seed_tool.canonical(seed_tool.build(root / curator.EXTRACTION_RELATIVE_PATH, table, root / curator.OBJ_EXPORT_RELATIVE_PATH))
		self.assertEqual(built.encode("utf-8"), SEED_PATH.read_bytes())
		code = "\n".join(line for line in script.read_text(encoding="latin-1").splitlines() if not line.strip().startswith("'"))
		self.assertIn('Const cGameName = "startrp2"', code)
		self.assertIn(".InitSw 0, 15, 14, 13, 12, 0, 0, 0", code)
		self.assertIn('SolCallBack(8)= "SolKnocker"', code)
		self.assertIn("Controller.Switch(88) = 1", code)
		# The claims behind the EOS and lamp-34 notes: no live write to 81 or 83, and no light bound to lamp 34.
		for address in (81, 83):
			self.assertIsNone(re.search(rf"(Switch\(\s*{address}\s*\)|PulseSw\s*\(?\s*{address}\b)", code, re.IGNORECASE), address)
		# Every lamp helper the script defines takes the lamp number first; collect them from the script itself, so a helper
		# added to the table is covered too, along with the state arrays it declares.
		helpers = sorted(set(re.findall(r"^\s*Sub\s+(\w+)\s*\(\s*nr\b", code, re.IGNORECASE | re.MULTILINE)), key=str.casefold)
		self.assertTrue({"Lamp", "Lampm", "Flash", "Flashm", "SetLamp", "SetModLamp", "LampMod", "FlashMod", "FadeObj", "FadeObjm", "NFadeObj", "NFadeObjm", "Text", "Textm"} <= set(helpers), helpers)
		arrays = re.search(r"^\s*Dim\s+(.*\bLampState\(.*)$", code, re.IGNORECASE | re.MULTILINE).group(1)
		arrays = sorted(re.findall(r"(\w+)\s*\(", arrays))
		self.assertEqual(["FadingState", "FlashLevel", "LampState"], arrays)
		guard = re.compile(rf"\b(?:{'|'.join(helpers)})\s*\(?\s*34\b|\b(?:{'|'.join(arrays)})\s*\(\s*34\s*\)", re.IGNORECASE)
		self.assertIsNone(guard.search(code))
		# The guard catches each binding form, and sees the helpers UpdateLamps uses for the neighbouring lamp 35.
		for sample in ("Lamp 34, l34", "FadeObj 34, P34, a, b, c, d", "NFadeObjm 34, P34, a, b", "FlashMod 34, f34", "Flashm 34, f34", "SetLamp 34, 1", "Text 34, t, m", "FlashLevel(34) = 1", "LampState(34)"):
			self.assertIsNotNone(guard.search(sample), sample)
		self.assertIsNone(guard.search("SetLamp 134, 1"))
		self.assertIsNotNone(re.search(rf"\b(?:{'|'.join(helpers)})\s*\(?\s*35\b", code, re.IGNORECASE))

	@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root is not configured")
	def test_the_retained_manual_matches_its_pin(self) -> None:
		root = Path(os.environ["PINMAME_MANUALS_ROOT"]) / "by-machine" / curator.MACHINE_ID / "ipdb"
		self.assertEqual(curator.MANUAL_SHA256, sha256(root / curator.MANUAL_NAME))


if __name__ == "__main__":
	unittest.main()
