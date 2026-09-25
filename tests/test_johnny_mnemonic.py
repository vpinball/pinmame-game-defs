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

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "johnny-mnemonic-1995.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "johnny-mnemonic-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "johnny-mnemonic-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "johnny-mnemonic-1995.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "johnny-mnemonic-1995.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
MACHINE_ID = "williams.johnny-mnemonic.1995"

DRIVER_IDS = {"jm_12r", "jm_12b", "jm_05r"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# jmGameData's inverted-switch mask as printed in src/wpc/sims/wpc/prelim/jm.c.
INVERTED_MASK = (0x00, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00)
PRINTED_SHADED = {31, 32, 33, 34, 35, 36, 74, 75, 76, 77}


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


class JohnnyMnemonicTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = by_address(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = by_address(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = by_address(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = by_address(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gis = by_address(cls.definition, "outputs", "pinmame.output.gi")
		cls.sources = {source["id"]: source for source in cls.definition["sources"]}
		cls.mechanisms = {mechanism["id"]: mechanism for mechanism in cls.definition["mechanisms"]}

	def test_identity_and_honest_partial_coverage(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual((MACHINE_ID, "Johnny Mnemonic", "Williams", 1995), (machine["id"], machine["name"], machine["manufacturer"], machine["year"]))
		self.assertEqual((3683, "GR6W8-Mb55B", "physical_pinball"), (machine["ipdb_id"], machine["opdb_id"], machine["kind"]))
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(["spatial_placement"], coverage["missing"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("pinmame.wpc-security", self.definition["controller"]["platform"])
		self.assertEqual({"path": "knowledge/williams/johnny-mnemonic-1995.md", "status": "complete"}, self.definition["knowledge"])
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_catalog_maps_exactly_the_three_drivers_here(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] == MACHINE_ID}
		self.assertEqual(DRIVER_IDS, mapped)
		compatibility = {driver["id"]: driver["physical_compatibility"] for driver in self.definition["drivers"]}
		self.assertEqual({"jm_12r": "identical", "jm_12b": "identical", "jm_05r": "compatible"}, compatibility)

	def test_the_full_input_space_is_enumerated(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119))
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))
		unused = {address for address, device in self.switches.items() if device["availability"] == "unused"}
		self.assertEqual(set(range(81, 89)) | {117}, unused)
		self.assertEqual({116, 118}, {address for address, device in self.switches.items() if device["availability"] == "optional" and address > 100})

	def test_opto_polarity_matches_the_re_derived_pinmame_mask(self) -> None:
		normalized = mask_addresses(INVERTED_MASK)
		self.assertEqual(PRINTED_SHADED, normalized)
		closed = {address for address, device in self.switches.items() if address in MATRIX_ADDRESSES and device.get("normally_closed")}
		self.assertEqual(normalized, closed)
		optos = {address for address, device in self.switches.items() if device.get("physical", {}).get("switch_type") == "opto" and address < 100}
		self.assertEqual(normalized, optos)

	def test_fliptronic_column(self) -> None:
		for address in (112, 114):
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		for address in (111, 113):
			self.assertEqual("leaf", self.switches[address]["physical"]["switch_type"])
			self.assertIn("must not drive it", self.switches[address]["physical"]["notes"])
		ball_in_hand = self.switches[115]
		self.assertEqual(("Ball In Hand", "used", "leaf"), (ball_in_hand["label"], ball_in_hand["availability"], ball_in_hand["physical"]["switch_type"]))
		self.assertIn("service-bulletin.williams.johnny-mnemonic.sb85", ball_in_hand["provenance"]["source_refs"])

	def test_hand_controls_are_matrix_buttons_and_the_mechanics_copy_is_disclosed(self) -> None:
		for address, source in ((67, 116), (68, 118)):
			device = self.switches[address]
			self.assertEqual("button", device["physical"]["switch_type"])
			self.assertIn(f"copies public {source} into this address", device["physical"]["notes"])
			self.assertIn(f"switch {address}", self.switches[source]["physical"]["notes"])

	def test_hand_sensors_ride_the_hand(self) -> None:
		for address in (12, 37, 74, 75, 76, 77):
			self.assertEqual("internal_nonvisual", self.switches[address]["spatial"]["reason"])
		self.assertEqual("internal_nonvisual", self.switches[115]["spatial"]["reason"])
		self.assertEqual({"A-20533.1"}, {self.switches[address]["physical"]["part_number"] for address in (74, 75, 76, 77)})
		self.assertEqual({"5647-12693-06"}, {self.switches[address]["physical"]["part_number"] for address in (12, 37)})

	def test_always_closed_switch(self) -> None:
		device = self.switches[24]
		self.assertEqual("constant", device["kind"])
		self.assertTrue(device["constant_active"])

	def test_the_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(5)), set(self.gis))
		kinds = {address: device["kind"] for address, device in self.solenoids.items()}
		self.assertEqual({21, 22, 23, 24}, {address for address, kind in kinds.items() if kind == "control_signal"})
		self.assertEqual({17, 18, 19, 20, 25, 26, 27, 28}, {address for address, kind in kinds.items() if kind == "flasher"})
		self.assertEqual("magnet", kinds[6])
		self.assertEqual(set(range(29, 33)) | set(range(37, 45)) | {49, 50}, {address for address, kind in kinds.items() if kind == "virtual"})
		self.assertEqual({4, 8, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50}, {address for address, device in self.solenoids.items() if device["availability"] == "unused"})
		self.assertEqual({37}, {address for address, device in self.lamps.items() if device["availability"] == "unused"})

	def test_diverters_keep_their_crossed_fliptronic_circuits(self) -> None:
		printed = {45: "29", 46: "30", 47: "31", 48: "32", 33: "33", 34: "34", 35: "35", 36: "36"}
		for address, number in printed.items():
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(number, aliases["manual.address"], address)
		self.assertTrue(self.solenoids[33]["label"].startswith("Left Diverter"))
		self.assertTrue(self.solenoids[35]["label"].startswith("Right Diverter"))
		self.assertIn("Upper Right flipper circuit", self.solenoids[34]["physical"]["notes"])
		self.assertIn("Upper Left flipper circuit", self.solenoids[36]["physical"]["notes"])

	def test_cyber_matrix_lamps_pair_with_holes_by_label(self) -> None:
		for lamp, switch in {51: 71, 52: 72, 53: 73, 61: 61, 62: 62, 63: 63, 71: 51, 72: 52, 73: 53}.items():
			self.assertEqual(self.lamps[lamp]["label"][-2:], self.switches[switch]["label"][-2:])
			lamp_xy, switch_xy = first_xy(self.lamps[lamp]), first_xy(self.switches[switch])
			self.assertLess(abs(lamp_xy[0] - switch_xy[0]) + abs(lamp_xy[1] - switch_xy[1]), 0.01, lamp)

	def test_geometric_ordering(self) -> None:
		xy = {address: first_xy(device) for address, device in self.switches.items() if device["spatial"]["status"] != "not_applicable"}
		# Matrix: 51/52/53 rear row left to right, 71/72/73 front row.
		self.assertLess(xy[51][0], xy[52][0])
		self.assertLess(xy[52][0], xy[53][0])
		self.assertLess(xy[51][1], xy[61][1])
		self.assertLess(xy[61][1], xy[71][1])
		# Jets: left upper-left, bottom lowest, right to the right.
		self.assertLess(xy[44][0], xy[46][0])
		self.assertGreater(xy[45][1], xy[44][1])
		self.assertGreater(xy[45][1], xy[46][1])
		self.assertLess(xy[64][0], xy[65][0])
		self.assertLess(xy[65][0], xy[66][0])
		self.assertLess(xy[15][0], xy[16][0])
		self.assertLess(xy[17][0], xy[18][0])
		self.assertLess(xy[25][0], xy[26][0])
		self.assertLess(xy[27][0], xy[28][0])
		self.assertGreater(xy[32][0], xy[35][0])
		self.assertLess(first_xy(self.solenoids[47])[0], first_xy(self.solenoids[45])[0])
		self.assertLess(first_xy(self.solenoids[19])[0], first_xy(self.solenoids[20])[0])

	def test_observed_and_unplaced_records_are_exactly_the_disclosed_ones(self) -> None:
		observed = set()
		unplaced = set()
		ids = []
		for device in self.definition["inputs"] + self.definition["outputs"]:
			key = (device["binding"]["group"], device["binding"]["device"])
			spatial = device.get("spatial")
			if spatial is None:
				unplaced.add(key)
				continue
			if spatial["status"] == "not_applicable":
				continue
			if spatial["status"] == "observed":
				observed.add(key)
			for placement in spatial["placements"]:
				ids.append(placement["id"])
				self.assertTrue(0 <= placement["x"] <= 1 and 0 <= placement["y"] <= 1, placement["id"])
				self.assertEqual(spatial["status"], placement["provenance"]["status"])
		self.assertEqual(len(ids), len(set(ids)))
		expected = {("pinmame.output.gi", 0), ("pinmame.output.gi", 1), ("pinmame.output.gi", 2), ("pinmame.input.switch", 31)}
		expected |= {("pinmame.output.solenoid", address) for address in (5, 17, 18, 19, 20, 25, 26, 27, 28)}
		self.assertEqual(expected, observed)
		self.assertEqual({("pinmame.output.gi", 3)}, unplaced)
		self.assertEqual((10, 11, 12), tuple(len(self.gis[address]["spatial"]["placements"]) for address in (0, 1, 2)))
		self.assertEqual("cabinet_or_service", self.gis[4]["spatial"]["reason"])

	def test_clear_matrix_coil_follows_its_drawing_callout(self) -> None:
		device = self.solenoids[5]
		self.assertEqual("observed", device["spatial"]["status"])
		self.assertEqual((0.828, 0.038), first_xy(device))
		self.assertNotEqual(first_xy(self.switches[62]), first_xy(device))

	def test_connector_list_readings_are_disclosed(self) -> None:
		self.assertIn("read as the device's name", self.solenoids[28]["physical"]["notes"])
		self.assertEqual(1, self.solenoids[28]["physical"]["quantity"])
		self.assertIn("read as a misprint", self.gis[3]["physical"]["notes"])
		self.assertIn("'solenoid 21'", self.solenoids[20]["physical"]["notes"])
		self.assertIn("J134", self.lamps[11]["physical"]["notes"])
		self.assertNotIn("quantity", self.lamps[88]["physical"])

	def test_drawing_measured_flashers_cite_the_fit(self) -> None:
		for address in (5, 17, 18, 19, 20, 25, 26, 27, 28):
			refs = self.solenoids[address]["spatial"]["placements"][0]["provenance"]["source_refs"]
			self.assertIn("human-review.johnny-mnemonic.solenoid-drawing-fit", refs)
			for value in first_xy(self.solenoids[address]):
				self.assertEqual(value, round(value, 3))

	def test_every_used_actuator_belongs_to_a_mechanism(self) -> None:
		actuators = {actuator for mechanism in self.definition["mechanisms"] for actuator in mechanism["actuators"]}
		driven = {device["id"] for address, device in self.solenoids.items() if device["kind"] in {"coil", "magnet", "control_signal"} and device["availability"] == "used"}
		self.assertEqual(set(), driven - actuators)
		ids = {device["id"] for device in self.definition["inputs"] + self.definition["outputs"]}
		for mechanism in self.definition["mechanisms"]:
			self.assertEqual(set(), set(mechanism["actuators"] + mechanism["sensors"]) - ids, mechanism["id"])
		glove = self.mechanisms["mechanism.data-glove"]
		self.assertEqual({"switch.matrix-12", "switch.matrix-37", "switch.matrix-74", "switch.matrix-75", "switch.matrix-76", "switch.matrix-77", "switch.generic-115", "switch.matrix-67", "switch.matrix-68"}, set(glove["sensors"]))

	def test_sources_carry_hashed_excerpts_without_local_paths(self) -> None:
		text = json.dumps(self.definition)
		self.assertNotIn("E:/", text)
		self.assertNotIn("C:\\", text)
		for source in self.sources.values():
			for excerpt in source.get("excerpts", []):
				self.assertEqual(excerpt["sha256"], hashlib.sha256((ROOT / excerpt["path"]).read_bytes()).hexdigest(), excerpt["id"])
				if "image" in excerpt:
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256((ROOT / excerpt["image"]).read_bytes()).hexdigest(), excerpt["id"])
				self.assertTrue(excerpt["reviewed"])
		self.assertTrue(self.sources["manual.williams.johnny-mnemonic.1995.operations-manual"]["uri"].startswith("https://web.archive.org/web/"))

	def test_no_catalog_or_other_machine_identifier_leaks_into_the_artifacts(self) -> None:
		# The curator was modelled on another WPC-Security curator; forbid every other machine's
		# driver ids so inherited prose cannot survive unnoticed.
		catalog = load_json(CATALOG_PATH)
		foreign = {driver["id"] for driver in catalog["drivers"] if driver["machine_id"] != MACHINE_ID}
		artifacts = DEFINITION_PATH.read_text(encoding="utf-8") + KNOWLEDGE_PATH.read_text(encoding="utf-8") + SPATIAL_REPORT_PATH.read_text(encoding="utf-8")
		tokens = set(re.findall(r"[a-z0-9]+_[a-z0-9]+", artifacts))
		self.assertEqual(set(), tokens & foreign)
		for word in ("i500", "Indianapolis", "Turbo", "Race Track"):
			self.assertNotIn(word, artifacts)

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_johnny_mnemonic as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		expected = canonical_bytes(curator.build())
		self.assertEqual(expected, canonical_bytes(curator.build()))
		self.assertEqual(expected, DEFINITION_PATH.read_bytes())
		self.assertEqual(expected, SEED_PATH.read_bytes())
		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_refuses_drift(self) -> None:
		import shutil
		import tempfile

		import curate_johnny_mnemonic as curator

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			for path in (DEFINITION_PATH, SEED_PATH, SPATIAL_REPORT_PATH, SPATIAL_REPORT_PATH.with_suffix(".md")):
				target = root / path.relative_to(ROOT)
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copyfile(path, target)
			curator.check(root)
			drifted = root / DEFINITION_PATH.relative_to(ROOT)
			drifted.write_bytes(drifted.read_bytes().replace(b"Ball In Hand", b"Ball ln Hand", 1))
			with self.assertRaises(RuntimeError):
				curator.check(root)

	def test_pinned_pinmame_declares_the_mask_flippers_and_hand(self) -> None:
		from pinmame_game_defs.workspace import resolve_working_root

		checkout = os.environ.get("PINMAME_SOURCE_ROOT")
		candidates = [Path(checkout)] if checkout else []
		working_root = resolve_working_root(ROOT)
		if working_root is not None:
			candidates.append(working_root / "source-checkouts" / "pinmame")
		source = next((path / "src/wpc/sims/wpc/prelim/jm.c" for path in candidates if (path / "src/wpc/sims/wpc/prelim/jm.c").is_file()), None)
		if source is None:
			self.skipTest("pinned PinMAME checkout is not available")
		text = source.read_text(encoding="utf-8", errors="replace")
		self.assertIn("{ 0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x78, 0x00, 0x00, 0x00, 0x00}", text)
		self.assertIn("FLIP_SW(FLIP_L | FLIP_U) | FLIP_SOL(FLIP_L) | FLIP_BUT(FLIP_L | FLIP_U)", text)
		self.assertIn("GEN_WPCSECURITY", text)
		self.assertNotIn("wpc_set_fastflip_addr", text)
		self.assertIn("core_setSw(68, core_getSw(118));", text)
		self.assertIn("core_setSw(67, core_getSw(116));", text)
		self.assertIn("wpc_data[WPC_SOLENOID3] >> 4", text)
		self.assertIn("core_setSw(12, locals.xPos < 1 ? 1 : 0);", text)
		self.assertIn("core_setSw(37, locals.yPos < 1 ? 1 : 0);", text)


class JohnnyMnemonicRetainedEvidenceTests(unittest.TestCase):
	def _root(self, name: str) -> Path:
		value = os.environ.get(name)
		if not value:
			self.skipTest(f"{name} is not set")
		return Path(value)

	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_johnny_mnemonic as curator

		curator.verify_extraction_manifest(self._root("PINMAME_VPX_SOURCES_ROOT"))

	def test_retained_table_and_script_hashes_and_claims(self) -> None:
		import curate_johnny_mnemonic as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "williams" / "johnny-mnemonic-1995"
		self.assertEqual(curator.TABLE_SHA256, hashlib.sha256((root / "Johnny Mnemonic (Williams 1995) VPW v1.2.2.vpx").read_bytes()).hexdigest())
		script = (root / "extracted-vpxtool" / "script.vbs").read_bytes()
		self.assertEqual(curator.SCRIPT_SHA256, hashlib.sha256(script).hexdigest())
		text = script.decode("latin-1")
		# Claims the definition makes about the script, checked against the script itself.
		self.assertIn('Const cGameName = "jm_12r"', text)
		self.assertIn(".HandleMechanics = 0", text)
		self.assertIn("Controller.Switch(24) = 1", text)
		self.assertIn("If KeyCode = rightmagnasave Then Controller.Switch(67)=1", text)
		self.assertIn("If KeyCode = leftmagnasave Then Controller.Switch(68)=1", text)
		self.assertIn(".Sol1=22", text)
		self.assertIn(".Sol2=-21", text)
		self.assertIn(".Sol1=24", text)
		self.assertIn(".Sol2=-23", text)
		self.assertIn("vpmTimer.PulseSw 31", text)
		self.assertIn('SolCallBack(34)\t= "SolLeftDiverterHold"', text)
		self.assertIn('SolCallBack(36)\t= "SolRightDiverterHold"', text)
		self.assertNotRegex(text, r"(?m)^\s*SolCallback\((33|35)\)")
		self.assertIn("Case 3 : l143a.State = level", text)

	def test_retained_manual_and_bulletin_hashes(self) -> None:
		import curate_johnny_mnemonic as curator

		root = self._root("PINMAME_MANUALS_ROOT") / "by-machine" / MACHINE_ID
		for name, digest in (
			("Williams_1995_Johnny_Mnemonic_English_Manual.pdf", curator.MANUAL_SHA256),
			("Williams_1995_Johnny_Mnemonic_Service_Bulletin_85.pdf", curator.SB85_SHA256),
			("Williams_1995_Johnny_Mnemonic_Service_Bulletin_87.pdf", curator.SB87_SHA256),
			("Williams_1995_Johnny_Mnemonic_Manual_Addendum_1.pdf", curator.ADDENDUM1_SHA256),
			("Williams_1995_Johnny_Mnemonic_Manual_Addendum_2.pdf", curator.ADDENDUM2_SHA256),
		):
			self.assertEqual(digest, hashlib.sha256((root / name).read_bytes()).hexdigest(), name)

	def test_drawing_measured_placements_equal_the_fit_output(self) -> None:
		import curate_johnny_mnemonic as curator

		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "johnny-mnemonic"
		output = (root / "fit_solenoid_drawing.out.txt").read_text(encoding="utf-8")
		measured = {int(number): (float(x), float(y)) for number, x, y in re.findall(r"(?m)^  (\d+): px \(\d+,\d+\) -> table \([^)]*\) normalized \(([\d.]+), ([\d.]+)\)", output)}
		expected = {**{address: xy for address, (xy, _) in curator.DRAWING_FLASHER_POSITIONS.items()}, **{address: xy for address, (xy, _) in curator.DRAWING_COIL_POSITIONS.items()}}
		self.assertEqual(expected, {address: measured[address] for address in expected})

	def test_retained_archive_table_hashes(self) -> None:
		import curate_johnny_mnemonic as curator

		root = self._root("PINMAME_VPX_SOURCES_ROOT") / "williams" / "johnny-mnemonic-1995" / "archive-2020"
		self.assertEqual(curator.ARCHIVE_TABLE_SHA256, hashlib.sha256((root / "Johnny Mnemonic (Williams 1995).vpx").read_bytes()).hexdigest())
		self.assertEqual(curator.ARCHIVE_SCRIPT_SHA256, hashlib.sha256((root / "Johnny Mnemonic (Williams 1995)" / "script.vbs").read_bytes()).hexdigest())
		from pinmame_game_defs.jsonio import canonical_bytes, load_json

		manifest = load_json(root / "extracted-vpxtool.manifest.json")
		self.assertEqual(canonical_bytes(curator.build_extraction_manifest(root / "Johnny Mnemonic (Williams 1995)")), canonical_bytes(manifest))
		self.assertEqual(curator.ARCHIVE_MANIFEST_SHA256, hashlib.sha256(canonical_bytes(manifest)).hexdigest())

	def test_retained_drawing_fit_hashes(self) -> None:
		import curate_johnny_mnemonic as curator

		root = self._root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "johnny-mnemonic"
		self.assertEqual(curator.DRAWING_FIT_SHA256, hashlib.sha256((root / "fit_solenoid_drawing.py").read_bytes()).hexdigest())
		self.assertEqual(curator.DRAWING_FIT_OUTPUT_SHA256, hashlib.sha256((root / "fit_solenoid_drawing.out.txt").read_bytes()).hexdigest())


if __name__ == "__main__":
	unittest.main()
