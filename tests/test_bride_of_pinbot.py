from __future__ import annotations

import hashlib
import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "the-machine-bride-of-pinbot-1991.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "the-machine-bride-of-pinbot-1991.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "the-machine-bride-of-pinbot-1991.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "the-machine-bride-of-pinbot-1991.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-alpha.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "the-machine-bride-of-pinbot-1991.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "the-machine-bride-of-pinbot-1991.md"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "wpc-alpha" / "bride-of-pinbot-head-helmet-and-service-names.json"

DRIVER_IDS = {
	"bop_l7", "bop_d7", "bop_l8", "bop_d8", "bop_l6", "bop_d6", "bop_l5", "bop_d5",
	"bop_l4", "bop_d4", "bop_l3", "bop_d3", "bop_l2", "bop_d2",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_SWITCHES = {23, 42, 48, 61, 62, 66, 68, 78, 81, 82, 83, 84, 85, 86, 87, 88}
HELMET_ADDRESSES = set(range(91, 99)) | set(range(101, 109))
HELMET_CLOCKWISE = [108, 107, 106, 105, 104, 103, 102, 101, 98, 97, 96, 95, 94, 93, 92, 91]
BACKBOX_LAMPS = set(range(71, 79)) | set(range(81, 86))


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _address_allowed(address: int, rules: list[dict[str, int]]) -> bool:
	return any(rule["minimum"] <= address <= rule["maximum"] for rule in rules)


def _point(device: dict[str, object]) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


class BrideOfPinbotDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(AUTHOR_READY_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_author_ready_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("williams.the-machine-bride-of-pinbot.1991", machine["id"])
		self.assertEqual((1991, 1502, "GRpee-MePdR", "physical_pinball"), (machine["year"], machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual({"validated"}, set(self.definition["coverage"]["dimensions"].values()))
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.wpc-alpha", self.definition["controller"]["platform"])
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		catalog_drivers = {driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("bop_")}
		self.assertEqual(DRIVER_IDS, catalog_drivers)
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		self.assertNotIn("clone_of", drivers["bop_l7"])
		self.assertEqual({"bop_l7"}, {driver["clone_of"] for driver in drivers.values() if "clone_of" in driver})
		self.assertEqual({"identical"}, {driver["physical_compatibility"] for driver in drivers.values()})
		self.assertIn("wpc_ram[0x1fc9]", drivers["bop_l7"]["variant_notes"])
		machine = next(record for record in catalog["machines"] if record["id"] == "williams.the-machine-bride-of-pinbot.1991")
		self.assertEqual("machines/author-ready/williams/the-machine-bride-of-pinbot-1991.json", machine["definition"])

	def test_controller_profile_admits_every_binding(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		groups = {group["id"]: group for group in profile["groups"]}
		lamp_rules = groups["pinmame.output.lamp"]["address_rules"]
		for address in HELMET_ADDRESSES:
			self.assertTrue(_address_allowed(address, lamp_rules), address)
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				group = groups[device["binding"]["group"]]
				self.assertTrue(_address_allowed(device["binding"]["device"], group["address_rules"]), device["id"])

	def test_switch_and_dip_enumeration(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		unused = {address for address, switch in self.switches.items() if address in MATRIX_ADDRESSES and switch["availability"] == "unused"}
		self.assertEqual(UNUSED_SWITCHES, unused)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertEqual({112, 114}, {address for address in range(111, 119) if self.switches[address]["availability"] == "used"})
		self.assertEqual("Face Position", self.switches[67]["label"])
		self.assertFalse(any(switch.get("normally_closed") for switch in self.switches.values()))

	def test_jet_bumper_switches_follow_manual_and_rom(self) -> None:
		upper_right, upper_left, lower = (_point(self.switches[address]) for address in (53, 54, 55))
		self.assertLess(upper_left[0], upper_right[0])
		self.assertGreater(lower[1], upper_left[1])
		self.assertGreater(lower[1], upper_right[1])
		self.assertEqual(_point(self.switches[54]), _point(self.solenoids[9]))
		self.assertEqual(_point(self.switches[53]), _point(self.solenoids[11]))
		self.assertEqual(_point(self.switches[55]), _point(self.solenoids[13]))
		self.assertIn("U.R. JET BUMPER", self.switches[53]["physical"]["notes"])

	def test_head_switches_and_kickers(self) -> None:
		left_eye, right_eye, mouth = (_point(self.switches[address]) for address in (63, 64, 65))
		self.assertLess(left_eye[0], right_eye[0])
		self.assertGreater(mouth[1], left_eye[1])
		self.assertEqual("motor", self.solenoids[28]["kind"])
		self.assertEqual("relay", self.solenoids[27]["kind"])
		self.assertEqual({"control_signal"}, {self.solenoids[address]["kind"] for address in (25, 26)})
		self.assertEqual([], self.definition["relationships"])
		head = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.head")
		self.assertEqual(["switch.matrix-67"], head["sensors"])
		self.assertEqual({self.solenoids[27]["id"], self.solenoids[28]["id"]}, set(head["actuators"]))
		self.assertEqual(["face-1", "face-2", "face-3", "face-4"], [position["id"] for position in head["positions"]])

	def test_public_solenoid_contract(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual({"flasher"}, {self.solenoids[address]["kind"] for address in range(17, 25)})
		self.assertEqual({2}, {self.solenoids[address]["physical"]["quantity"] for address in (18, 19, 21, 22, 23, 24)})
		self.assertEqual({1}, {self.solenoids[address]["physical"]["quantity"] for address in (17, 20)})
		self.assertEqual("relay", self.solenoids[31]["kind"])
		self.assertEqual({"unused"}, {self.solenoids[address]["availability"] for address in [32, *range(33, 45), 50]})
		self.assertEqual({"virtual"}, {self.solenoids[address]["kind"] for address in range(45, 50)})
		self.assertEqual(["cabinet.knocker"], self.solenoids[7]["roles"])

	def test_lamp_matrix_labels_and_backbox_lamps(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES | HELMET_ADDRESSES, set(self.lamps))
		self.assertEqual("Circle 50K", self.lamps[25]["label"])
		self.assertEqual(("Right Ramp Million", "Right Ramp 100K"), (self.lamps[61]["label"], self.lamps[63]["label"]))
		self.assertIn("swapped", self.lamps[61]["physical"]["notes"])
		self.assertIn("swapped", self.lamps[63]["physical"]["notes"])
		self.assertIn("CIRCLE SOK", self.lamps[25]["physical"]["notes"])
		for address in BACKBOX_LAMPS:
			self.assertEqual(("not_applicable", "cabinet_or_service"), (self.lamps[address]["spatial"]["status"], self.lamps[address]["spatial"]["reason"]), address)
		mini = [_point(self.lamps[address]) for address in (86, 87, 88)]
		self.assertEqual(sorted(mini), mini)

	def test_helmet_lamps_follow_manual_and_rom_order(self) -> None:
		points = [_point(self.lamps[address]) for address in HELMET_CLOCKWISE]
		lower_left, lower_right = points[0], points[-1]
		self.assertLess(lower_left[0], lower_right[0])
		self.assertEqual("Helmet Light 1", self.lamps[108]["label"])
		self.assertEqual("Helmet Light 16", self.lamps[91]["label"])
		self.assertTrue(all(points[index][1] >= points[index + 1][1] for index in range(0, 7)))
		self.assertTrue(all(points[index][1] <= points[index + 1][1] for index in range(8, 15)))
		helmet_gi = self.gi[1]
		self.assertEqual(16, helmet_gi["physical"]["quantity"])
		self.assertEqual(sorted(points), sorted((placement["x"], placement["y"]) for placement in helmet_gi["spatial"]["placements"]))

	def test_general_illumination(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))
		self.assertEqual({"cabinet_or_service"}, {self.gi[address]["spatial"]["reason"] for address in (0, 3)})
		self.assertEqual((9, 9), (self.gi[2]["physical"]["quantity"], self.gi[4]["physical"]["quantity"]))

	def test_every_used_device_is_spatially_resolved(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"] + self.definition["displays"]:
			self.assertIn("spatial", device, device["id"])
			self.assertEqual("validated" if device["spatial"]["status"] != "not_applicable" else "not_applicable", device["spatial"]["status"], device["id"])

	def test_seed_and_curator_are_deterministic(self) -> None:
		self.assertEqual(AUTHOR_READY_PATH.read_bytes(), SEED_PATH.read_bytes())
		import curate_bride_of_pinbot as curator

		curator.check(ROOT)

	def test_spatial_audit_matches_curator(self) -> None:
		import curate_bride_of_pinbot as curator

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual("pinmame-spatial-audit", report["format"])
		self.assertEqual([], report["unresolved"])
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_committed_excerpts_exist_hash_match_and_fit_budget(self) -> None:
		manual = next(source for source in self.definition["sources"] if source["kind"] == "manual")
		self.assertEqual(8, len(manual["excerpts"]))
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			image = ROOT / excerpt["image"]
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
			self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image.read_bytes()).hexdigest(), excerpt["image"])
			self.assertLessEqual(image.stat().st_size, 100_000, excerpt["image"])
			self.assertTrue(excerpt["reviewed"])

	def test_runtime_evidence_records_head_and_helmet_contract(self) -> None:
		evidence = load_json(RUNTIME_EVIDENCE_PATH)
		self.assertEqual(["williams.the-machine-bride-of-pinbot.1991"], evidence["machine_ids"])
		runtime = evidence["runtime"]
		self.assertEqual("bop_l7", runtime["game"])
		self.assertEqual("8371478a7640f1896dcdf565aed340dc5df989ba", runtime["emulator"]["built_from_revision"])
		runs = runtime["observations"]["runs"]
		self.assertIn("only public lamp(s) 108 stayed lit", runs["helmet-single-lamp"]["note"])
		self.assertIn("lit 107, 106, 105, 104, 103, 102, 101, 98, 97, 96, 95, 94, 93, 92, 91, 108", runs["helmet-single-lamp"]["note"])
		for start in (0, 90, 180, 270):
			self.assertEqual([8, 15, 16, 8], runs[f"head-coils-vpw-start-{start}"]["ordered_solenoid_on_sequence"])
		face_one: list[float] = []
		for start in (0, 90, 180, 270):
			note = runs[f"head-coils-vpw-start-{start}"]["note"]
			first_kick = note.split("head kickers first fired at angles ")[1].split(",")[0]
			self.assertTrue(first_kick.startswith("8@"), note)
			angle = float(first_kick[2:])
			if all(min(abs(angle - other), 360.0 - abs(angle - other)) > 5.0 for other in face_one):
				face_one.append(angle)
		self.assertEqual(3, len(face_one))
		self.assertIn("CIRCLE SOK / T.8 ?3 LAMP 2S", runs["lamp-names"]["note"])
		self.assertIn("RIGHT RAMP MILL / T.8 4? LAMP 6?", runs["lamp-names"]["note"])
		self.assertIn("RIGHT RAMP ?OOK / T.8 43 LAMP 63", runs["lamp-names"]["note"])
		self.assertIn("LEFT LOOP SOOK", runs["lamp-names"]["note"])
		self.assertIn("U.R. JET BUMPER", runs["switch-names"]["note"])
		self.assertIn("U.L. JET BUMPER", runs["switch-names"]["note"])
		self.assertEqual(12, len(runtime["raw_runs"]))


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root not configured")
class BrideOfPinbotRetainedTableTests(unittest.TestCase):
	def test_retained_extraction_matches_manifest(self) -> None:
		import curate_bride_of_pinbot as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve()
		curator.verify_extraction_manifest(root)
		script = root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())

	def test_retained_script_still_permutes_bumper_switches(self) -> None:
		import curate_bride_of_pinbot as curator

		root = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]).resolve()
		text = (root / curator.EXTRACTION_RELATIVE_PATH / "script.vbs").read_text(encoding="latin-1")
		self.assertIn("Sub Bumper1_Hit:vpmTimer.PulseSw 53", text)
		self.assertIn("Sub Bumper2_Hit:vpmTimer.PulseSw 55", text)
		self.assertIn("Sub Bumper3_Hit:vpmTimer.PulseSw 54", text)


@unittest.skipUnless(os.environ.get("PINMAME_MANUALS_ROOT"), "retained manual root not configured")
class BrideOfPinbotRetainedManualTests(unittest.TestCase):
	def test_retained_manual_hash(self) -> None:
		import curate_bride_of_pinbot as curator

		path = Path(os.environ["PINMAME_MANUALS_ROOT"]).resolve() / "by-machine" / curator.MACHINE_ID / "the_machine_operations_manual.pdf"
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256(path.read_bytes()).hexdigest())


@unittest.skipUnless(os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"), "retained review artifacts root not configured")
class BrideOfPinbotRetainedRuntimeTests(unittest.TestCase):
	def test_relay_released_forward_and_energized_reverse(self) -> None:
		# The head-coil test steps from the mouth face to the eyes face (forward) and back to the
		# mouth (reverse). The ROM's own relay state during those moves is the direction evidence.
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "bride-of-pinbot" / "harness-runs"
		for start in (0, 90, 180, 270):
			run = load_json(root / f"head-coils-vpw-start-{start}.json")
			kicks = [edge for edge in run["kicker_edges"] if edge["state"]]
			mouth = next(edge["t"] for edge in kicks if edge["solenoid"] == 8)
			eyes = next(edge["t"] for edge in kicks if edge["solenoid"] == 15)
			back = next(edge["t"] for edge in kicks if edge["solenoid"] == 8 and edge["t"] > eyes)
			forward = [edge["relay"] for edge in run["motor_edges"] if edge["motor"] and mouth < edge["t"] < eyes]
			reverse = [edge["relay"] for edge in run["motor_edges"] if edge["motor"] and eyes < edge["t"] < back]
			self.assertTrue(forward and set(forward) == {0}, (start, forward))
			self.assertTrue(reverse and set(reverse) == {1}, (start, reverse))

	def test_retained_raw_runs_match_evidence_hashes(self) -> None:
		evidence = load_json(RUNTIME_EVIDENCE_PATH)
		root = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]).resolve() / "bride-of-pinbot" / "harness-runs"
		for run in evidence["runtime"]["raw_runs"]:
			path = root / f"{run['name']}.json"
			self.assertEqual(run["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), run["name"])


if __name__ == "__main__":
	unittest.main()
