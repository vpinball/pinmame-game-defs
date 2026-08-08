from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256
from pinmame_game_defs.spatial import fail_closed_spatial_partial

ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "tron-legacy-pro-2011.json"
LE_PATH = ROOT / "machines" / "author-ready" / "stern" / "tron-legacy-limited-edition-2011.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "tron-legacy-pro-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "tron-legacy-limited-edition-boot-start.json"
LE_SPATIAL_PATH = ROOT / "evidence" / "vpx" / "tron-legacy-limited-edition-2011-v11-spatial-candidates.json"
PRO_EXTRACTION_PATH = ROOT / "reports" / "spatial" / "stern" / "tron-legacy-pro-2011.json"
PRO_KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "tron-legacy-pro-2011.md"
TRON_CURATOR_PATH = ROOT / "tools" / "curate_tron.py"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def external_root(variable: str) -> Path:
	value = os.environ.get(variable)
	if not value:
		raise unittest.SkipTest(f"{variable} is not configured; external evidence verification skipped")
	return Path(value).expanduser()


class TronDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.le = load_json(LE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)
		cls.pro_extraction = load_json(PRO_EXTRACTION_PATH)
		cls.pro_knowledge = PRO_KNOWLEDGE_PATH.read_text(encoding="utf-8")
		cls.tron_curator = TRON_CURATOR_PATH.read_text(encoding="utf-8")

	def test_pro_remains_fail_closed_and_le_is_spatially_author_ready(self) -> None:
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		self.assertEqual(2, self.le["schema_version"])
		self.assertEqual("author_ready", self.le["coverage"]["status"])
		self.assertEqual([], self.le["coverage"]["missing"])
		self.assertEqual("validated", self.le["coverage"]["dimensions"]["spatial_placement"])
		for definition in (self.pro, self.le):
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertTrue((ROOT / "machines" / "author-ready" / "stern" / "tron-legacy-limited-edition-2011.json").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "tron-legacy-limited-edition-2011.json").exists())

	def test_le_spatial_inventory_keeps_exact_geometry_and_manual_multiplicity(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual("validated", inputs[31]["spatial"]["status"])
		self.assertEqual((0.812434, 0.370486), (inputs[31]["spatial"]["placements"][0]["x"], inputs[31]["spatial"]["placements"][0]["y"]))
		self.assertEqual(1, len(inputs[18]["spatial"]["placements"]))
		self.assertEqual({18, 19, 20, 21}, {address for address in (18, 19, 20, 21) if inputs[address]["spatial"]["status"] == "validated"})
		for address in (52, 53):
			self.assertEqual((0.471314, 0.208014), (inputs[address]["spatial"]["placements"][0]["x"], inputs[address]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.471314, 0.208014), (outputs[6]["spatial"]["placements"][0]["x"], outputs[6]["spatial"]["placements"][0]["y"]))
		self.assertEqual("cabinet_or_service", inputs[65]["spatial"]["reason"])
		self.assertEqual(2, len(outputs[19]["spatial"]["placements"]))
		self.assertEqual(["manual.tron-legacy-pro-le.2011"], outputs[20]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual(["manual.tron-legacy-pro-le.2011", "vpx.tron-legacy-le-vpm-1.1.4", "vpx-table.tron-legacy-le-v11"], outputs[21]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertIn("Lanelight", outputs[21]["physical"]["notes"])
		self.assertEqual(2, outputs[25]["physical"]["quantity"])
		self.assertEqual(35, outputs[0]["physical"]["quantity"] if 0 in outputs else bindings(self.le, "outputs", "pinmame.output.gi")[0]["physical"]["quantity"])
		self.assertEqual(62, sum(1 for address, lamp in lamps.items() if address <= 80 and lamp["availability"] == "used" and lamp["spatial"]["status"] == "validated"))
		self.assertEqual(23, lamps[104]["physical"]["quantity"])
		self.assertEqual(29, lamps[101]["physical"]["quantity"])
		self.assertEqual("vpx-table.tron-legacy-le-v11", next(source["id"] for source in self.le["sources"] if source["kind"] == "vpx_table"))
		self.assertEqual("56ad2f5318c33dbc12f3aa2515a41d819eb8b95b2ffcd94ebe1044cec4281ae5", next(source["sha256"] for source in self.le["sources"] if source["kind"] == "vpx_table"))

	def test_le_primitive_and_wall_centers_are_reported_and_bound_by_name(self) -> None:
		report = load_json(LE_SPATIAL_PATH)
		self.assertEqual(2, report["version"])
		self.assertEqual({"left": 0.0, "top": 0.0, "right": 952.0, "bottom": 2115.0}, report["bounds"])
		self.assertEqual("56ad2f5318c33dbc12f3aa2515a41d819eb8b95b2ffcd94ebe1044cec4281ae5", report["source"]["vpx_sha256"])
		self.assertEqual("vpxtool git:v0.33.3", report["source"]["vpxtool_version"])
		points = {(item["type"], item["name"]): (item["x"], item["y"]) for item in report["objects"]}
		for object_type, name in (
			("Primitive", "sw1p"), ("Primitive", "sw2p"), ("Primitive", "sw3p"), ("Primitive", "sw4p"),
			("Primitive", "sw7p"), ("Primitive", "sw8p"), ("Primitive", "sw13p"), ("Primitive", "sw48p"),
			("Primitive", "SW49P"), ("Primitive", "SW50P"), ("Primitive", "SW51P"), ("Primitive", "MotorBank"),
			("Primitive", "recognizer"), ("Primitive", "Disc1"), ("Wall", "LeftSlingShot"),
			("Wall", "RightSlingShot"), ("Wall", "UpPost"),
		):
			self.assertIn((object_type, name), points)
			item = next(item for item in report["objects"] if item["type"] == object_type and item["name"] == name)
			self.assertEqual("gameitems/" + object_type + "." + name + ".json", item["source_path"])
			self.assertIn(item["center_method"], {"position", "drag_point_centroid"})
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		input_sources = {1: "sw1p", 2: "sw2p", 3: "sw3p", 4: "sw4p", 7: "sw7p", 8: "sw8p", 13: "sw13p", 48: "sw48p", 49: "SW49P", 50: "SW50P", 51: "SW51P", 52: "MotorBank", 53: "MotorBank", 54: "recognizer", 55: "recognizer", 56: "recognizer"}
		for address, name in input_sources.items():
			self.assertEqual(points[("Primitive", name)], tuple(inputs[address]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address, object_type, name in ((26, "Wall", "LeftSlingShot"), (27, "Wall", "RightSlingShot")):
			self.assertEqual(points[(object_type, name)], tuple(inputs[address]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address, object_type, name in ((5, "Primitive", "Disc1"), (6, "Primitive", "MotorBank"), (7, "Wall", "UpPost"), (13, "Wall", "LeftSlingShot"), (14, "Wall", "RightSlingShot"), (22, "Primitive", "Disc1"), (23, "Primitive", "recognizer"), (30, "Primitive", "Disc1")):
			self.assertEqual(points[(object_type, name)], tuple(outputs[address]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		target_centers = [points[("Primitive", name)] for name in ("sw1p", "sw2p", "sw3p", "sw4p")]
		expected_reset = tuple(round(sum(point[index] for point in target_centers) / 4, 6) for index in (0, 1))
		self.assertEqual(expected_reset, tuple(outputs[3]["spatial"]["placements"][0][axis] for axis in ("x", "y")))

	def test_le_slingshot_provenance_and_rgb_channels_are_explicit(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		for address, source_name in ((26, "Wall.LeftSlingShot"), (27, "Wall.RightSlingShot")):
			placement = inputs[address]["spatial"]["placements"][0]
			self.assertEqual(["manual.tron-legacy-pro-le.2011", "vpx-table.tron-legacy-le-v11"], placement["provenance"]["source_refs"])
			self.assertIn(source_name, inputs[address]["physical"]["notes"])
		for address, source_name in ((13, "Wall.LeftSlingShot"), (14, "Wall.RightSlingShot")):
			placement = outputs[address]["spatial"]["placements"][0]
			self.assertEqual(["manual.tron-legacy-pro-le.2011", "vpx.tron-legacy-le-vpm-1.1.4", "vpx-table.tron-legacy-le-v11"], placement["provenance"]["source_refs"])
			self.assertIn(source_name, outputs[address]["physical"]["notes"])
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		for addresses, quantity, group in (((101, 102, 103), 29, "rgb.right-ramp"), ((104, 105, 106), 23, "rgb.left-ramp")):
			coordinate_sets = []
			for address in addresses:
				lamp = lamps[address]
				physical = lamp["physical"]
				self.assertEqual(group, physical["shared_emitter_group"])
				self.assertEqual(list(addresses), physical["co_located_addresses"])
				self.assertEqual(quantity, physical["quantity"])
				self.assertEqual(quantity, physical["shared_physical_quantity"])
				self.assertIn("independently controlled", physical["notes"])
				self.assertIn("one physical", physical["notes"])
				self.assertEqual(quantity, len(lamp["spatial"]["placements"]))
				coordinate_sets.append([(point["x"], point["y"]) for point in lamp["spatial"]["placements"]])
			self.assertEqual([coordinate_sets[0]] * 3, coordinate_sets)

	def test_pro_extraction_gate_records_rejected_le_sources(self) -> None:
		inventory = self.pro_extraction
		self.assertEqual("blocked_partial", inventory["status"])
		self.assertFalse(inventory["author_ready"])
		self.assertTrue(inventory["acquisition"]["exact_source_target_exists"])
		self.assertFalse(inventory["acquisition"]["exact_source_copied"])
		self.assertTrue(inventory["acquisition"]["rejected_candidate_retained"])
		self.assertTrue(inventory["acquisition"]["rejected_candidate_extraction_performed"])
		self.assertFalse(inventory["acquisition"]["exact_pro_extraction_performed"])
		self.assertEqual("partial", inventory["fail_closed_gates"]["canonical_status"])
		self.assertEqual(["local-table-library[0]", "local-table-library[1]", "authenticated-community-downloads"], inventory["acquisition"]["search_order"])
		self.assertEqual(5, len(inventory["candidates"]))
		self.assertTrue(all(not candidate["accepted"] for candidate in inventory["candidates"]))
		self.assertTrue(all(candidate["vpxtool"]["rom"] == "trn_174h" for candidate in inventory["candidates"]))

		candidate = next(candidate for candidate in inventory["candidates"] if candidate["sha256"] == "876b833bde197cabf2a37aa4b6f1bd4bcfeca4e6dfe5552a8316f0a60b2aacfb")
		self.assertEqual(64176128, candidate["bytes"])
		self.assertEqual("https://www.vpforums.org/index.php?app=downloads&showfile=15427", candidate["download_url"])
		self.assertEqual("limited_edition_rejected_negative_identity", candidate["classification"])
		self.assertTrue(candidate["retained_only_as_negative_identity_evidence"])
		self.assertFalse(candidate["pro_coordinates_eligible"])
		self.assertFalse(candidate["provenance_eligible"])
		self.assertIn("DTBank4.SolDropUp", candidate["rejection"])
		self.assertIn("D13/D14", candidate["rejection"])
		self.assertEqual("6d40356884812cf5a35f70fa78051f43697129b16ad86cf997354f29776fd42a", candidate["download_archive"]["sha256"])
		web_record = next(item for item in inventory["web_candidates"] if item["url"].endswith("showfile=15427"))
		self.assertEqual({"url", "result", "accepted", "candidate_sha256"}, set(web_record))
		self.assertEqual(candidate["sha256"], web_record["candidate_sha256"])

	def test_rejected_candidate_never_enters_pro_definition_or_provenance(self) -> None:
		self.assertIn("retained only as negative identity evidence", self.pro_knowledge)
		self.assertIn("must not supply Pro coordinates or provenance", self.pro_knowledge)
		self.assertIn("retained only as negative identity evidence", self.tron_curator)
		self.assertIn("must not supply Pro coordinates or provenance", self.tron_curator)
		self.assertIn("staged from `SolLFlipper` through `LeftFlipper1`", self.pro_knowledge)
		self.assertIn("dedicated `SolCallback(12)` hook commented out", self.pro_knowledge)
		self.assertFalse(any(source["kind"] == "vpx_table" for source in self.pro["sources"]))
		pro_json = json.dumps(self.pro, sort_keys=True)
		for forbidden in ("876b833bde197", "Bigus", "showfile=15427", "vpforums-showfile-15427"):
			self.assertNotIn(forbidden, pro_json)
		self.assertTrue(all("spatial" not in item for item in self.pro["inputs"] + self.pro["outputs"]))

	def test_changed_tron_pro_files_contain_no_developer_absolute_paths(self) -> None:
		for path in (
			ROOT / "machines" / "partial" / "stern" / "tron-legacy-pro-2011.json",
			PRO_KNOWLEDGE_PATH,
			PRO_EXTRACTION_PATH,
			TRON_CURATOR_PATH,
			ROOT / "tests" / "test_tron.py",
		):
			self.assertNotRegex(path.read_text(encoding="utf-8"), re.compile(r"(?i)\b[a-z]:[\\/]"), path)

	def test_rejected_candidate_cache_is_byte_identical_and_proves_le_identity(self) -> None:
		candidate = next(candidate for candidate in self.pro_extraction["candidates"] if candidate["sha256"] == "876b833bde197cabf2a37aa4b6f1bd4bcfeca4e6dfe5552a8316f0a60b2aacfb")
		candidate_root = external_root("PINMAME_VPX_SOURCES_ROOT") / "stern" / "tron-legacy-pro-2011" / "rejected" / "vpforums-showfile-15427"
		artifacts = (
			(candidate_root / "source" / "Tron Legacy (Stern 2011)_Bigus(MOD)4.0.vpx", candidate["sha256"]),
			(candidate_root / "download-archive" / "Tron Legacy (Stern 2011)_Bigus(MOD)4.0.vpx.zip", candidate["download_archive"]["sha256"]),
			(candidate_root / "analysis" / "script.vbs", candidate["vpxtool"]["analysis_script_sha256"]),
			(candidate_root / "extraction" / "script.vbs", candidate["vpxtool"]["extracted_script_sha256"]),
		)
		for path, expected_sha256 in artifacts:
			self.assertTrue(path.is_file(), path)
			self.assertEqual(expected_sha256, file_sha256(path))
		script = artifacts[3][0].read_text(encoding="utf-8", errors="replace")
		self.assertRegex(script, re.compile(r'cGameName\s*=\s*"trn_174h"', re.IGNORECASE))
		self.assertRegex(script, re.compile(r'SolCallback\(3\)\s*=\s*"DTBank4\.SolDropUp"', re.IGNORECASE))
		self.assertIn("LeftFlipper1.RotateToEnd", script)

	def test_pro_extraction_report_is_canonical_and_generated(self) -> None:
		tools_path = str(ROOT / "tools")
		if tools_path not in sys.path:
			sys.path.insert(0, tools_path)
		import curate_tron as curator

		self.assertEqual(curator.pro_extraction_report(), self.pro_extraction)
		self.assertEqual(canonical_bytes(self.pro_extraction), PRO_EXTRACTION_PATH.read_bytes())
		self.assertEqual(canonical_bytes(fail_closed_spatial_partial(curator.build(False))), PRO_PATH.read_bytes())
		runtime_source = next(source for source in self.pro["sources"] if source["id"] == "runtime.tron-legacy-pro.boot-start")
		report_runtime = self.pro_extraction["external_evidence"]["pro_runtime"]
		self.assertEqual(runtime_source["uri"], report_runtime["path"])
		self.assertEqual(runtime_source["sha256"], report_runtime["sha256"])

	def test_supported_driver_family_is_exhaustively_split_by_physical_model(self) -> None:
		pro = {driver["id"] for driver in self.pro["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"trn_110", "trn_120", "trn_140", "trn_150", "trn_160", "trn_170", "trn_174", "trn_17402"}, pro)
		self.assertEqual({"trn_100h", "trn_110h", "trn_130h", "trn_140h", "trn_174h"}, limited_edition)
		self.assertFalse(pro & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("trn_")}, pro | limited_edition)
		self.assertEqual(5682, self.pro["machine"]["ipdb_id"])
		self.assertEqual(5707, self.le["machine"]["ipdb_id"])
		self.assertEqual("I-00B9", self.pro["machine"]["model_number"])
		self.assertEqual("I-00C2", self.le["machine"]["model_number"])

	def test_complete_switch_and_dip_spaces_include_model_differences(self) -> None:
		for definition in (self.pro, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertEqual("unused", switches[33]["availability"])
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertTrue(all(pro[address]["availability"] == "unused" for address in (54, 55, 56)))
		self.assertTrue(all(limited_edition[address]["availability"] == "used" for address in (54, 55, 56)))
		self.assertEqual("used", pro[88]["availability"])
		self.assertEqual("used", pro[87]["availability"])
		self.assertTrue(pro[87]["normally_closed"])
		self.assertEqual("unused", limited_edition[88]["availability"])
		self.assertEqual("unused", limited_edition[87]["availability"])
		self.assertIn("stages the upper-left flipper from the left-flipper control", limited_edition[88]["physical"]["notes"])
		self.assertIn("PDF page 49, D-13", pro[88]["physical"]["notes"])
		self.assertIn("PDF page 55, D-13", limited_edition[88]["physical"]["notes"])
		for switches in (pro, limited_edition):
			self.assertTrue(switches[22]["pulse"])
			for address in (14, 25, 28):
				self.assertFalse(switches[address]["pulse"])
				self.assertEqual("leaf", switches[address]["physical"]["switch_type"])

	def test_main_outputs_are_complete_and_model_specific(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 35)), set(pro))
		self.assertEqual(set(range(1, 35)), set(limited_edition))
		self.assertEqual("Disc direction relay", pro[3]["label"])
		self.assertEqual("TRON four-bank drop-target reset", limited_edition[3]["label"])
		self.assertEqual("Lower left flasher", pro[22]["label"])
		self.assertEqual("Disc direction relay", limited_edition[22]["label"])
		self.assertEqual("Lower right flasher", pro[23]["label"])
		self.assertEqual("Recognizer motor relay", limited_edition[23]["label"])
		self.assertEqual("Left dome flashers x2", limited_edition[19]["label"])
		self.assertEqual("Right dome flashers x2", limited_edition[25]["label"])
		self.assertIn("source conflict", limited_edition[19]["physical"]["notes"].lower())
		self.assertIn("source conflict", limited_edition[25]["physical"]["notes"].lower())
		self.assertEqual("Upper-left flipper", limited_edition[12]["label"])
		self.assertEqual("optional", limited_edition[8]["availability"])
		self.assertEqual("optional", limited_edition[24]["availability"])
		self.assertEqual("virtual", limited_edition[33]["kind"])
		self.assertEqual("unused", limited_edition[34]["availability"])
		self.assertIn("commented-out SolCallback(34)", limited_edition[34]["physical"]["notes"])
		self.assertEqual("J8-P11", limited_edition[9]["wiring"]["control_connection"])
		self.assertNotIn("vpx.tron-legacy-le-vpm-1.1.4", pro[3]["provenance"]["source_refs"])

	def test_lamp_maps_and_tricolor_public_order_are_exact(self) -> None:
		pro = bindings(self.pro, "outputs", "pinmame.output.lamp")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.lamp")
		expected_addresses = set(range(1, 81)) | set(range(101, 107))
		self.assertEqual(expected_addresses, set(pro))
		self.assertEqual(expected_addresses, set(limited_edition))
		self.assertEqual(set(range(1, 36)) | set(range(37, 46)) | set(range(48, 54)) | set(range(55, 65)) | {66}, {address for address, lamp in pro.items() if lamp["availability"] == "used"})
		self.assertEqual(set(range(1, 41)) | {42, 43} | set(range(45, 67)) | set(range(101, 107)), {address for address, lamp in limited_edition.items() if lamp["availability"] == "used"})
		self.assertTrue(all(pro[address]["availability"] == "unused" for address in range(101, 107)))
		self.assertEqual(["Right ramp blue", "Right ramp green", "Right ramp red", "Left ramp blue", "Left ramp green", "Left ramp red"], [limited_edition[address]["label"] for address in range(101, 107)])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))
		self.assertNotIn("vpx.tron-legacy-le-vpm-1.1.4", pro[1]["provenance"]["source_refs"])

	def test_custom_mechanisms_are_recreatable_and_not_cross_contaminated(self) -> None:
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertIn("mechanism.tron-standups", pro)
		self.assertNotIn("mechanism.tron-drop-bank", pro)
		self.assertNotIn("mechanism.recognizer-toy", pro)
		self.assertIn("mechanism.tron-drop-bank", limited_edition)
		self.assertIn("mechanism.recognizer-toy", limited_edition)
		self.assertEqual(["device.tron-four-bank-drop-target-reset"], limited_edition["mechanism.tron-drop-bank"]["actuators"])
		self.assertEqual(3, len(limited_edition["mechanism.recognizer-toy"]["positions"]))
		self.assertIn("initializes down on switch 52", limited_edition["mechanism.recognizer-bank"]["behavior"])
		for definition in (pro, limited_edition):
			disc = definition["mechanism.disc"]
			self.assertEqual({"device.disc-motor-power", "device.disc-direction-relay", "device.disc-motor-relay"}, set(disc["actuators"]))
			self.assertIn("carry and throw balls", disc["behavior"])

	def test_manual_script_and_exact_rom_evidence_are_pinned(self) -> None:
		for definition in (self.pro, self.le):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("1212d9f1f5bdb33e9b248299d0e1693ad1103f82129234a1348f0aa8edd47e84", sources["manual.tron-legacy-pro-le.2011"]["sha256"])
			self.assertEqual("d257913fb05fa054bbf15a8605d4b9b3af2887514355784cbfbc5c92a36adfcc", sources["vpx.tron-legacy-le-vpm-1.1.4"]["sha256"])
			self.assertTrue(sources["vpx.tron-legacy-le-vpm-1.1.4"]["known_working"])
		self.assertEqual("610e8fc71fdd83a94748ebe8691aeaa5964986e2d236ce6b7c46ed13602ff772", self.pro_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("51af7aa06cbdd8286101a9dba0b8d2376f957d14a9ae6b0172ed6806683be490", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("7ae5392a3bf6f9a7d282bf3ca002eea00a84ffd8cf39ff9af2e77a75e0eac44b", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("92dee327b8700943e258f6ac6c0b7a2b8716b0070698069125cb2be5ed4b306f", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual({101, 102, 103, 104, 105, 106}, set(self.le_evidence["runtime"]["observations"]["lamp_addresses_seen"]) & set(range(101, 107)))
		self.assertFalse(set(self.pro_evidence["runtime"]["observations"]["lamp_addresses_seen"]) & set(range(101, 107)))
		self.assertIn("--initial-switch 52", self.pro_evidence["runtime"]["command_template"])

	def test_q19_q25_lampmod_mapping_uses_script_ground_truth_and_discloses_conflict(self) -> None:
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual("Left dome flashers x2", outputs[19]["label"])
		self.assertEqual("Right dome flashers x2", outputs[25]["label"])
		self.assertEqual([(0.048271, 0.121191), (0.048625, 0.595134)], [(point["x"], point["y"]) for point in outputs[19]["spatial"]["placements"]])
		self.assertEqual([(0.811384, 0.503503), (0.650501, 0.137223)], [(point["x"], point["y"]) for point in outputs[25]["spatial"]["placements"]])
		for address in (19, 25, 28, 31, 32):
			self.assertEqual(2, outputs[address]["physical"]["quantity"])
			self.assertIn("Multiplicity follows the official LE flasher chart", outputs[address]["physical"]["notes"])
		self.assertIn("LampMod 125", outputs[19]["physical"]["notes"])
		self.assertIn("LampMod 119", outputs[25]["physical"]["notes"])
		for address in (19, 25):
			notes = outputs[address]["physical"]["notes"]
			self.assertIn("official Stern manual", notes)
			self.assertIn("PDF page 57", notes)
			self.assertIn("Q19 to `FLASH: RIGHT DOMES (X2)`", notes)
			self.assertIn("Q25 to `FLASH: LEFT DOMES (X2)`", notes)
			self.assertIn("VPW Mod 0.24", notes)
			self.assertIn("ecea74df1775bd39cfd8838955adfefb544b5907d345223847369710fc4dac7d", notes)
			self.assertIn("ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4", notes)
			self.assertIn("source conflict", notes.lower())
		self.assertEqual({"manual.tron-legacy-pro-le.2011", "vpx.tron-legacy-le-vpm-1.1.4", "vpx-table.tron-legacy-le-v11"}, set(outputs[19]["spatial"]["placements"][0]["provenance"]["source_refs"]))
		self.assertEqual({"manual.tron-legacy-pro-le.2011", "vpx.tron-legacy-le-vpm-1.1.4", "vpx-table.tron-legacy-le-v11"}, set(outputs[25]["spatial"]["placements"][0]["provenance"]["source_refs"]))
		knowledge = (ROOT / "knowledge/stern/tron-legacy-limited-edition-2011.md").read_text(encoding="utf-8").lower()
		self.assertIn("source conflict", knowledge)
		self.assertIn("official stern manual (`manual.tron-legacy-pro-le.2011`, pdf page 57)", knowledge)
		self.assertIn("q19 to `flash: right domes (x2)`", knowledge)
		self.assertIn("q25 to `flash: left domes (x2)`", knowledge)
		self.assertIn("vpw mod 0.24", knowledge)
		self.assertIn("ecea74df1775bd39cfd8838955adfefb544b5907d345223847369710fc4dac7d", knowledge)
		self.assertIn("ce3a843e5747c1163fb9478ac65addc8b3dc89e44471d527768823b6d63b7ec4", knowledge)
		self.assertNotIn("concordant manual", knowledge)
		self.assertNotIn("systems\n\n\ntron", knowledge)

	def test_candidate_geometry_rejects_report_tampering_and_vpxtool_version_drift(self) -> None:
		tools_path = str(ROOT / "tools")
		if tools_path not in sys.path:
			sys.path.insert(0, tools_path)
		import curate_tron_le_spatial as curator

		report = load_json(LE_SPATIAL_PATH)
		with tempfile.TemporaryDirectory() as temporary:
			temporary_root = Path(temporary)
			modified_object = temporary_root / "modified-object.json"
			tampered = json.loads(json.dumps(report))
			tampered["objects"][0]["x"] += 0.001
			modified_object.write_text(json.dumps(tampered), encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "SHA-256"):
				curator.CandidateGeometry(modified_object)
			modified_content = temporary_root / "modified-content.json"
			modified_content.write_text(LE_SPATIAL_PATH.read_text(encoding="utf-8") + "\n", encoding="utf-8")
			with self.assertRaisesRegex(ValueError, "SHA-256"):
				curator.CandidateGeometry(modified_content)
			for version in (None, "vpxtool git:v0.33.2"):
				version_path = temporary_root / ("missing-version.json" if version is None else "wrong-version.json")
				version_tampered = json.loads(json.dumps(report))
				if version is None:
					del version_tampered["source"]["vpxtool_version"]
				else:
					version_tampered["source"]["vpxtool_version"] = version
				version_path.write_text(json.dumps(version_tampered), encoding="utf-8")
				with patch.object(curator, "SPATIAL_EVIDENCE_SHA256", file_sha256(version_path)):
					with self.assertRaisesRegex(ValueError, "vpxtool version"):
						curator.CandidateGeometry(version_path)

	def test_le_promote_is_idempotent_and_refuses_clobber_or_stale_partial(self) -> None:
		tools_path = str(ROOT / "tools")
		if tools_path not in sys.path:
			sys.path.insert(0, tools_path)
		import curate_tron_le_spatial as curator

		with tempfile.TemporaryDirectory() as temporary:
			temporary_root = Path(temporary)
			author_ready = temporary_root / "author-ready.json"
			knowledge = temporary_root / "knowledge.md"
			partial = temporary_root / "partial.json"
			with patch.object(curator, "AUTHOR_READY_PATH", author_ready), patch.object(curator, "KNOWLEDGE_PATH", knowledge), patch.object(curator, "PARTIAL_PATH", partial):
				curator.promote()
				first_author = author_ready.read_bytes()
				first_knowledge = knowledge.read_bytes()
				curator.promote()
				self.assertEqual(first_author, author_ready.read_bytes())
				self.assertEqual(first_knowledge, knowledge.read_bytes())
				author_ready.write_text("{\"unexpected\": true}\n", encoding="utf-8")
				with self.assertRaisesRegex(RuntimeError, r"verify the source inputs, remove this generated output, and rerun tools/curate_tron\.py"):
					curator.promote()
				self.assertEqual("{\"unexpected\": true}\n", author_ready.read_text(encoding="utf-8"))
				author_ready.write_bytes(first_author)
				knowledge.write_text("unexpected\n", encoding="utf-8")
				with self.assertRaisesRegex(RuntimeError, r"verify the source inputs, remove this generated output, and rerun tools/curate_tron\.py"):
					curator.promote()
				self.assertEqual("unexpected\n", knowledge.read_text(encoding="utf-8"))
				partial.write_text("{}\n", encoding="utf-8")
				with self.assertRaisesRegex(RuntimeError, "stale partial artifact"):
					curator.promote()

	def test_every_runtime_observation_resolves_to_a_declared_output(self) -> None:
		for definition, evidence in ((self.pro, self.pro_evidence), (self.le, self.le_evidence)):
			groups = {
				"solenoid_addresses_seen": bindings(definition, "outputs", "pinmame.output.solenoid"),
				"lamp_addresses_seen": bindings(definition, "outputs", "pinmame.output.lamp"),
				"gi_addresses_seen": bindings(definition, "outputs", "pinmame.output.gi"),
			}
			for observation, declared in groups.items():
				self.assertFalse(set(evidence["runtime"]["observations"][observation]) - set(declared), observation)

	def test_bindings_and_semantic_ids_are_unique(self) -> None:
		for definition in (self.pro, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
	unittest.main()
