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

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "indianapolis-500-1995.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "indianapolis-500-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "indianapolis-500-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "indianapolis-500-1995.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "indianapolis-500-1995.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

DRIVER_IDS = {"i500_11r", "i500_11b", "i500_10r"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX = {12, 33, 67, 68, 71, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
# i500GameData's inverted-switch mask as printed in src/wpc/sims/wpc/prelim/i500.c.
INVERTED_MASK = (0x00, 0x00, 0x00, 0x00, 0x1F, 0xE0, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00)
PRINTED_SHADED = {41, 42, 43, 44, 45, 56, 57, 58, 61, 62, 63}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def by_address(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def first_xy(device: dict) -> tuple[float, float]:
	placement = device["spatial"]["placements"][0]
	return placement["x"], placement["y"]


def mask_addresses(mask: tuple[int, ...]) -> set[int]:
	return {column * 10 + bit + 1 for column, value in enumerate(mask) for bit in range(8) if value >> bit & 1}


class IndianapolisFiveHundredTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = by_address(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = by_address(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_address(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gis = by_address(cls.definition, "outputs", "pinmame.output.gi")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}

	def test_identity_and_honest_partial_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(("bally.indianapolis-500.1995", "Indianapolis 500", "Bally", 1995), (machine["id"], machine["name"], machine["manufacturer"], machine["year"]))
		self.assertEqual((2853, "Gr8l3-MDWr0", "physical_pinball"), (machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("validated", coverage["dimensions"]["physical_wiring"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_catalog_maps_exactly_the_three_drivers_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == "bally.indianapolis-500.1995"}
		self.assertEqual(DRIVER_IDS, mapped)
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.definition["drivers"]))

	def test_the_full_input_space_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119))
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		unused = {address for address, device in self.switches.items() if device["availability"] == "unused"}
		self.assertEqual(UNUSED_MATRIX | {117, 118}, unused)

	def test_opto_polarity_matches_the_re_derived_pinmame_mask(self) -> None:
		normalized = mask_addresses(INVERTED_MASK)
		self.assertEqual(PRINTED_SHADED | {66}, normalized)
		closed = {address for address, device in self.switches.items() if address in MATRIX_ADDRESSES and device.get("normally_closed")}
		self.assertEqual(normalized, closed)
		self.assertEqual(normalized, {address for address, device in self.switches.items() if device.get("physical", {}).get("switch_type") == "opto" and address < 100})

	def test_switch_66_is_an_opto_despite_the_unshaded_printed_cell(self) -> None:
		device = self.switches[66]
		self.assertEqual("A-20047", device["physical"]["part_number"])
		self.assertIn("manual.bally.indianapolis-500.1995.operations-manual", device["provenance"]["source_refs"])
		self.assertIn("Turbo Opto PCB Assembly", device["physical"]["notes"])
		self.assertIn("printing omission", device["physical"]["notes"])

	def test_fliptronic_inputs(self) -> None:
		for address in (112, 114, 116):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])
			self.assertFalse(self.switches[address]["normally_closed"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		for address in (111, 113, 115):
			self.assertEqual("leaf", self.switches[address]["physical"]["switch_type"])

	def test_always_closed_switch_and_the_table_defect_note(self) -> None:
		device = self.switches[24]
		self.assertEqual("constant", device["kind"])
		self.assertTrue(device["constant_active"])
		self.assertIn("defect in that table", device["physical"]["notes"])

	def test_the_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gis))
		kinds = {address: device["kind"] for address, device in self.solenoids.items()}
		self.assertEqual({17: "motor", 18: "motor"}, {address: kind for address, kind in kinds.items() if kind == "motor"})
		self.assertEqual({14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28}, {address for address, kind in kinds.items() if kind == "flasher"})
		self.assertEqual(set(range(29, 33)) | set(range(37, 45)) | {49, 50}, {address for address, kind in kinds.items() if kind == "virtual"})
		self.assertEqual({6, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {address for address, device in self.solenoids.items() if device["availability"] == "unused"})
		self.assertEqual({67, 68, 85}, {address for address, device in self.lamps.items() if device["availability"] == "unused"})

	def test_fliptronic_outputs_keep_printed_circuit_numbers_and_diverter_routing(self) -> None:
		printed = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
		for address, number in printed.items():
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(number, aliases["manual.address"], address)
		self.assertIn("Diverter", self.solenoids[35]["label"])
		self.assertIn("Diverter", self.solenoids[36]["label"])
		self.assertIn("A-19978", self.solenoids[36]["physical"]["assembly_part_number"])
		self.assertIn("power OR hold", self.solenoids[34]["physical"]["notes"])

	def test_lamps_18_and_27_follow_the_matrix_and_the_geometry(self) -> None:
		self.assertEqual("Turbo Wrench", self.lamps[18]["label"])
		self.assertEqual("Left Ramp Wrench", self.lamps[27]["label"])
		turbo_target = first_xy(self.switches[47])
		ramp_target = first_xy(self.switches[55])
		lamp18, lamp27 = first_xy(self.lamps[18]), first_xy(self.lamps[27])
		distance = lambda a, b: ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5  # noqa: E731
		self.assertLess(distance(lamp18, turbo_target), distance(lamp18, ramp_target))
		self.assertLess(distance(lamp27, ramp_target), distance(lamp27, turbo_target))

	def test_nothing_placed_on_an_observed_switch_stays_validated(self) -> None:
		observed = {first_xy(device) for address, device in self.switches.items() if device["spatial"]["status"] == "observed"}
		for device in self.definition["outputs"]:
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable" or device["kind"] == "gi":
				continue
			if first_xy(device) in observed:
				self.assertEqual("observed", spatial["status"], device["id"])

	def test_flipper_prose_describes_fliptronic_end_of_stroke(self) -> None:
		flippers = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.flippers")
		self.assertNotIn("opens the power path", flippers["behavior"])
		self.assertIn("end-of-stroke input", flippers["behavior"])
		turbo = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.turbo")
		self.assertNotIn("four balls in its quadrants", turbo["behavior"])
		self.assertNotIn("REV. 1.1", KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	def test_lightup_leds_are_projected_onto_their_target_faces(self) -> None:
		for lamps, target in (((71, 72, 73, 74), 56), ((75, 76, 77, 78), 57), ((81, 82, 83, 84), 58)):
			for address in lamps:
				self.assertEqual(first_xy(self.switches[target]), first_xy(self.lamps[address]))
				self.assertEqual("A-19823", self.lamps[address]["physical"]["assembly_part_number"])

	def test_geometric_ordering(self) -> None:
		xy = {address: first_xy(device) for address, device in self.switches.items() if device["spatial"]["status"] != "not_applicable"}
		self.assertLess(xy[72][0], xy[74][0])
		self.assertLess(xy[74][0], xy[73][0])
		self.assertGreater(xy[74][1], xy[72][1])
		self.assertLess(xy[51][0], xy[52][0])
		self.assertLess(xy[52][0], xy[53][0])
		self.assertLess(xy[28][1], xy[31][1])
		self.assertLess(xy[31][1], xy[32][1])
		self.assertLess(xy[15][0], xy[16][0])
		self.assertLess(xy[17][0], xy[18][0])
		self.assertLess(xy[26][0], xy[27][0])
		self.assertLess(first_xy(self.solenoids[47])[0], first_xy(self.solenoids[45])[0])
		self.assertGreater(first_xy(self.solenoids[33])[0], 0.85)
		upper, lower = (placement["y"] for placement in self.solenoids[27]["spatial"]["placements"])
		self.assertLess(upper, lower)

	def test_race_track_reflectors_belong_to_gi_string_2_without_a_bulb_count(self) -> None:
		gi = self.gis[1]
		self.assertEqual(len(gi["spatial"]["placements"]), gi["physical"]["quantity"])
		self.assertIn("ORG and ORG/WHT", gi["physical"]["notes"])
		self.assertIn("prints no bulb count", gi["physical"]["notes"])
		for address in (3, 4):
			self.assertIn("only an inference", self.gis[address]["physical"]["notes"])
			self.assertEqual(["cabinet.insert-panel"], self.gis[address]["roles"])
		self.assertEqual("B-9362-R-3", self.solenoids[12]["physical"]["assembly_part_number"])

	def test_only_general_illumination_and_the_drawing_disputed_switches_are_observed(self) -> None:
		statuses = {}
		ids = []
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable":
				continue
			statuses[(device["binding"]["group"], device["binding"]["device"])] = spatial["status"]
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				self.assertEqual(spatial["status"], placement["provenance"]["status"])
		self.assertEqual(len(ids), len(set(ids)))
		observed = {key for key, status in statuses.items() if status == "observed"}
		expected = {("pinmame.output.gi", 0), ("pinmame.output.gi", 1), ("pinmame.output.gi", 2)}
		expected |= {("pinmame.input.switch", 54), ("pinmame.input.switch", 75)}
		self.assertEqual(expected, observed)
		self.assertEqual({"cabinet_or_service"}, {self.gis[3]["spatial"]["reason"], self.gis[4]["spatial"]["reason"]})
		self.assertEqual((6, 12, 25), tuple(len(self.gis[address]["spatial"]["placements"]) for address in (0, 1, 2)))

	def test_every_used_actuator_belongs_to_a_mechanism(self) -> None:
		actuators = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		coils = {device["id"] for address, device in self.solenoids.items() if device["kind"] in {"coil", "motor"} and device["availability"] == "used"}
		self.assertEqual(set(), coils - actuators)
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertEqual(set(), set(mechanism["actuators"] + mechanism["sensors"]) - ids, mechanism["id"])

	def test_sources_carry_hashed_excerpts_without_local_paths(self) -> None:
		text = json.dumps(self.definition)
		self.assertNotIn("E:/", text)
		self.assertNotIn("C:\\", text)
		for source_id in ("manual.bally.indianapolis-500.1995.operators-handbook", "manual.bally.indianapolis-500.1995.operations-manual"):
			excerpts = self.sources[source_id]["excerpts"]
			self.assertTrue(excerpts)
			for excerpt in excerpts:
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest())
				self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest())
				self.assertTrue(excerpt["reviewed"])

	def test_no_catalog_or_other_machine_identifier_leaks_into_the_artifacts(self) -> None:
		# The curator was modelled on another WPC-Security curator; forbid every other machine's
		# driver ids so inherited prose cannot survive unnoticed.
		catalog = load_json(CATALOG_PATH)
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != "bally.indianapolis-500.1995"}
		artifacts = DEFINITION_PATH.read_text(encoding="utf-8") + KNOWLEDGE_PATH.read_text(encoding="utf-8") + SPATIAL_REPORT_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9]+_[a-z0-9]+", artifacts))
		self.assertEqual(set(), tokens & foreign)
		self.assertNotIn("wcsGameData", artifacts)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_indianapolis_500 as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curator.build())
		self.assertEqual(expected, canonical_bytes(curator.build()))
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())
		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_refuses_drift(self) -> None:
		import tempfile
		import shutil

		import curate_indianapolis_500 as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			drifted = root / DEFINITION_PATH.relative_to(ROOT)
			drifted.write_bytes(drifted.read_bytes().replace(b"Turbo Index", b"Turbo lndex", 1))
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_pinned_pinmame_declares_the_mask_and_flipper_hardware(self) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		candidates = [Path(checkout)] if checkout else []
		working_root = resolve_working_root(ROOT)
		if working_root is not None:
			candidates.append(working_root / "source-checkouts" / "pinmame")
		source = next((path / "src/wpc/sims/wpc/prelim/i500.c" for path in candidates if (path / "src/wpc/sims/wpc/prelim/i500.c").is_file()), None)
		if source is None:
			self.skipTest("pinned PinMAME checkout is not available")
		text = source.read_text(encoding="utf-8", errors="replace")
		self.assertIn("{ 0x00, 0x00, 0x00, 0x00, 0x1f, 0xe0, 0x27, 0x00, 0x00, 0x00, 0x00, 0x00}", text)
		self.assertIn("FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L | FLIP_UR)", text)
		self.assertIn("GEN_WPCSECURITY", text)
		self.assertNotIn("wpc_set_fastflip_addr", text)


class IndianapolisFiveHundredRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_indianapolis_500 as curator

		curator.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_retained_table_and_script_hashes(self) -> None:
		import curate_indianapolis_500 as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "bally" / "indianapolis-500-1995"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "source" / "Indianapolis_500_VPX_1.1_RTM.vpx").read_bytes()).hexdigest())
		script = (root / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script).hexdigest())
		text = script.decode("latin-1")
		# Claims the definition makes about the script, checked against the script itself.
		self.assertIn("Controller.Switch(24) = 0", text)
		self.assertIn('Const cGameName = "i500_11r"', text)
		self.assertIn("InitSwitches Array(42, 43, 44, 45)", text)
		self.assertIn('SolCallback(36) = "SolDiverterHold"', text)
		self.assertNotRegex(text, r"(?m)^\s*SolCallback\((35|17|33|34)\)")
		self.assertIn("RightFlipper.RotateToEnd:RightFlipper2.RotateToEnd", text)

	def test_retained_reconciliation_hashes(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)["manual_reconciliation"]
		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "indianapolis-500"
		self.assertEqual(report["artifact_sha256"], hashlib.sha256((root / "manual-reconciliation.md").read_bytes()).hexdigest())
		for uri, digest in report["overlay_images"].items():
			name = uri.rsplit("/", 1)[1]
			self.assertEqual(digest, hashlib.sha256((root / name).read_bytes()).hexdigest(), name)

	def test_retained_manual_hashes(self) -> None:
		import curate_indianapolis_500 as curator

		root = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / "bally.indianapolis-500.1995"
		self.assertEqual(curator.HANDBOOK_SHA256, hashlib.sha256((root / "Indianapolis_500_OPS.pdf").read_bytes()).hexdigest())
		self.assertEqual(curator.MANUAL_SHA256, hashlib.sha256((root / "ipdb-2853" / "indy500manualfull.original-scan.pdf").read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
