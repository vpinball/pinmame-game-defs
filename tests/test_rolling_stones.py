from __future__ import annotations

import ast
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-rolling-stones-standard-2011.json"
LE_PATH = ROOT / "machines" / "author-ready" / "stern" / "the-rolling-stones-limited-edition-2011.json"
STANDARD_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "rolling-stones-standard-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "rolling-stones-limited-edition-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class RollingStonesDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.standard = load_json(STANDARD_PATH)
		cls.le = load_json(LE_PATH)
		cls.standard_evidence = load_json(STANDARD_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)

	def test_both_physical_editions_are_spatially_ready(self) -> None:
		self.assertEqual(2, self.standard["schema_version"])
		self.assertEqual("author_ready", self.standard["coverage"]["status"])
		self.assertEqual([], self.standard["coverage"]["missing"])
		self.assertEqual("validated", self.standard["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(2, self.le["schema_version"])
		self.assertEqual("author_ready", self.le["coverage"]["status"])
		self.assertEqual([], self.le["coverage"]["missing"])
		self.assertEqual("validated", self.le["coverage"]["dimensions"]["spatial_placement"])
		for definition in (self.standard, self.le):
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "rsn_110h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "rsn_110h.md").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "the-rolling-stones-limited-edition-2011.json").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "the-rolling-stones-standard-2011.json").exists())

	def test_le_spatial_inventory_is_explicit_and_individual(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual("cabinet_or_service", inputs[84]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", inputs[82]["spatial"]["reason"])
		self.assertEqual(["manual.rolling-stones-standard-le.2011"], inputs[84]["spatial"]["provenance"]["source_refs"])
		self.assertEqual(["manual.rolling-stones-standard-le.2011"], inputs[82]["spatial"]["provenance"]["source_refs"])
		self.assertEqual("validated", inputs[83]["spatial"]["status"])
		self.assertEqual("validated", inputs[81]["spatial"]["status"])
		self.assertEqual((0.3075, 0.8415), (inputs[83]["spatial"]["placements"][0]["x"], inputs[83]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.6175, 0.8415), (inputs[81]["spatial"]["placements"][0]["x"], inputs[81]["spatial"]["placements"][0]["y"]))
		self.assertEqual(7, len(inputs[72]["spatial"]["placements"]))
		gi = bindings(self.le, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(40, len(gi["spatial"]["placements"]))
		self.assertEqual(40, gi["physical"]["quantity"])
		lamp20 = lamps[20]["spatial"]["placements"][0]
		self.assertNotIn((lamp20["x"], lamp20["y"]), {(point["x"], point["y"]) for point in gi["spatial"]["placements"]})
		self.assertEqual(2, len(outputs[29]["spatial"]["placements"]))
		self.assertEqual(2, outputs[29]["physical"]["quantity"])
		for address in (25, 27, 28):
			self.assertEqual(1, len(outputs[address]["spatial"]["placements"]))
			self.assertEqual(1, outputs[address]["physical"]["quantity"])
		self.assertEqual({"cabinet_or_service"}, {outputs[address]["spatial"]["reason"] for address in (20, 21)})
		self.assertEqual("internal_nonvisual", inputs[71]["spatial"]["reason"])
		self.assertTrue(all(0 <= placement[axis] <= 1 for collection in (self.le["inputs"], self.le["outputs"]) for device in collection for placement in device.get("spatial", {}).get("placements", []) for axis in ("x", "y")))

	def test_le_sw22_reuses_only_the_standard_manual_ordered_projection(self) -> None:
		sw22 = bindings(self.le, "inputs", "pinmame.input.switch")[22]
		self.assertIn("internal.trough-jam-opto", sw22["roles"])
		self.assertIn("internal.trough", sw22["roles"])
		self.assertEqual("Downstream trough-jam opto at the five-ball trough/eject corridor.", sw22["physical"]["location"])
		self.assertEqual("validated", sw22["spatial"]["status"])
		self.assertEqual((0.727167, 0.982), (sw22["spatial"]["placements"][0]["x"], sw22["spatial"]["placements"][0]["y"]))
		self.assertEqual(
			["vpx-table.rolling-stones-le-archive-2020", "manual.rolling-stones-standard-le.2011"],
			sw22["spatial"]["placements"][0]["provenance"]["source_refs"],
		)
		notes = sw22["physical"]["notes"]
		self.assertIn("Standard sibling's manual-ordered trough-region projection", notes)
		self.assertIn("not an exact VPX coordinate", notes)
		self.assertIn("uncertainty", notes)
		self.assertIn("no dedicated SW22 object", notes)
		self.assertNotEqual(sw22["spatial"]["placements"], bindings(self.le, "inputs", "pinmame.input.switch")[21]["spatial"].get("placements"))

	def test_le_cabinet_service_controls_and_physical_multiplicities_are_reconciled(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		cabinet_input_addresses = {15, 16, 65, 66, 67, 68, 69, 82, 84, 86, 88, -7, -6, -5, -3, -2, -1, 0}
		self.assertEqual({"cabinet_or_service"}, {inputs[address]["spatial"]["reason"] for address in cabinet_input_addresses})
		self.assertTrue(all(not inputs[address]["spatial"].get("placements") for address in cabinet_input_addresses))
		self.assertEqual({"cabinet_or_service"}, {outputs[address]["spatial"]["reason"] for address in (8, 20, 21, 24)})
		self.assertEqual({"cabinet_or_service"}, {lamps[address]["spatial"]["reason"] for address in (1, 2)})
		self.assertTrue(all(not outputs[address]["spatial"].get("placements") for address in (8, 20, 21, 24)))
		self.assertTrue(all(not lamps[address]["spatial"].get("placements") for address in (1, 2)))
		self.assertEqual({8: 1, 20: 1, 21: 1, 24: 1}, {address: outputs[address].get("physical", {}).get("quantity", 1) for address in (8, 20, 21, 24)})
		self.assertEqual({address: quantity for address, quantity in ((22, 1), (23, 1), (25, 1), (26, 1), (27, 1), (28, 1), (29, 2), (31, 1))}, {address: outputs[address]["physical"]["quantity"] for address in (22, 23, 25, 26, 27, 28, 29, 31)})
		self.assertEqual(40, bindings(self.le, "outputs", "pinmame.output.gi")[0]["physical"]["quantity"])
		self.assertTrue(all(lamps[address]["physical"]["quantity"] == 1 for address in set(range(3, 54)) | {58, 60, 61, 62}))

	def test_standard_spatial_inventory_is_complete_and_excludes_le_only_hardware(self) -> None:
		for collection in (self.standard["inputs"], self.standard["outputs"]):
			self.assertTrue(all("spatial" in device for device in collection))
			self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in collection))
		self.assertEqual("not_applicable", self.standard["displays"][0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.standard["displays"][0]["spatial"]["reason"])
		outputs = bindings(self.standard, "outputs", "pinmame.output.solenoid")
		switches = bindings(self.standard, "inputs", "pinmame.input.switch")
		self.assertEqual((0.4745, 0.9745), (switches[18]["spatial"]["placements"][0]["x"], switches[18]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.5385, 0.9775), (switches[19]["spatial"]["placements"][0]["x"], switches[19]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.727167, 0.982), (switches[22]["spatial"]["placements"][0]["x"], switches[22]["spatial"]["placements"][0]["y"]))
		self.assertNotEqual((0.664, 0.979), (switches[22]["spatial"]["placements"][0]["x"], switches[22]["spatial"]["placements"][0]["y"]))
		self.assertIn("disclosed", switches[22]["physical"]["notes"])
		self.assertEqual("not_applicable", switches[82]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[82]["spatial"]["reason"])
		self.assertEqual("not_applicable", switches[84]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", switches[84]["spatial"]["reason"])
		for address in (81, 83):
			self.assertEqual("validated", switches[address]["spatial"]["status"])
			self.assertIn("hidden-switch convention", switches[address]["physical"]["notes"])
			self.assertEqual(1, len(switches[address]["spatial"]["placements"]))
		self.assertEqual((0.664, 0.979), (outputs[1]["spatial"]["placements"][0]["x"], outputs[1]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.916, 0.92625), (outputs[2]["spatial"]["placements"][0]["x"], outputs[2]["spatial"]["placements"][0]["y"]))
		self.assertTrue(all(outputs[address]["spatial"]["reason"] == "cabinet_or_service" for address in (20, 21)))
		for address in (5, 7, 17, 29, 30, 32):
			self.assertEqual("unused", outputs[address]["spatial"]["reason"])
		self.assertEqual(7, len(bindings(self.standard, "inputs", "pinmame.input.switch")[72]["spatial"]["placements"]))
		for address in (25, 27, 28):
			self.assertEqual(1, outputs[address]["physical"]["quantity"])
			self.assertEqual(1, len(outputs[address]["spatial"]["placements"]))
			self.assertIn("synchronized LE render layers", outputs[address]["physical"]["notes"])
		gi = bindings(self.standard, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(40, len(gi["spatial"]["placements"]))
		self.assertEqual(40, gi["physical"]["quantity"])
		lamp20 = bindings(self.standard, "outputs", "pinmame.output.lamp")[20]["spatial"]["placements"][0]
		self.assertNotIn((lamp20["x"], lamp20["y"]), {(point["x"], point["y"]) for point in gi["spatial"]["placements"]})
		sources = {source["id"]: source for source in self.standard["sources"]}
		self.assertEqual("vpx_table", sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["kind"])
		self.assertFalse(sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["known_working"])
		self.assertIn("LE-only", sources["vpx-table.rolling-stones-le-bound-shared-geometry"]["locator"])
		self.assertIn("rsn_110h", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertIn("disqualified", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertNotIn("exact-looking", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])
		self.assertNotIn("inaccessible", sources["vpuniverse.rolling-stones-balutito-mod-2-0-24384"]["locator"])

	def test_editions_exhaustively_split_the_supported_driver_family(self) -> None:
		standard = {driver["id"] for driver in self.standard["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"rsn_103", "rsn_105", "rsn_110"}, standard)
		self.assertEqual({"rsn_100h", "rsn_110h"}, limited_edition)
		self.assertFalse(standard & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("rsn_")}, standard | limited_edition)
		self.assertEqual(5668, self.standard["machine"]["ipdb_id"])
		self.assertEqual(5708, self.le["machine"]["ipdb_id"])

	def test_complete_switch_and_dip_address_space_is_explicit(self) -> None:
		for definition in (self.standard, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertEqual("Moving Mick target hit", switches[72]["label"])
			self.assertTrue(switches[72]["pulse"])
		standard = bindings(self.standard, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertEqual("unused", standard[17]["availability"])
		self.assertEqual("used", limited_edition[17]["availability"])
		self.assertEqual("unused", standard[50]["availability"])
		self.assertEqual("used", limited_edition[50]["availability"])
		self.assertEqual("Magnetic ball detector", limited_edition[71]["label"])
		self.assertTrue(limited_edition[71]["normally_closed"])
		self.assertEqual("unused", standard[71]["availability"])
		self.assertIn("must not build a second start switch", standard[14]["physical"]["notes"])
		self.assertIn("vpx.rolling-stones-le-1.0.6i", standard[14]["provenance"]["source_refs"])

	def test_premium_real_and_virtual_cabinet_inputs_are_distinguished(self) -> None:
		standard = bindings(self.standard, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertTrue(all(standard[address]["availability"] == "unused" for address in (85, 86, 87, 88)))
		self.assertEqual("switch", limited_edition[88]["kind"])
		self.assertEqual("switch", limited_edition[86]["kind"])
		self.assertEqual("virtual", limited_edition[87]["kind"])
		self.assertEqual("virtual", limited_edition[85]["kind"])
		self.assertNotIn("switch_type", limited_edition[87]["physical"])
		self.assertNotIn("switch_type", limited_edition[85]["physical"])
		self.assertIn("must not build", limited_edition[87]["physical"]["notes"])
		self.assertIn("must not build", limited_edition[85]["physical"]["notes"])

	def test_main_outputs_are_complete_and_edition_specific(self) -> None:
		standard = bindings(self.standard, "outputs", "pinmame.output.solenoid")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(standard))
		self.assertEqual(set(range(1, 34)), set(limited_edition))
		edition_only = {5, 7, 17, 29, 30, 32}
		self.assertTrue(all(standard[address]["availability"] == "unused" for address in edition_only))
		self.assertTrue(all(limited_edition[address]["availability"] == "used" for address in edition_only))
		self.assertEqual("magnet", limited_edition[5]["kind"])
		self.assertEqual("magnet", limited_edition[7]["kind"])
		self.assertEqual("unused", standard[12]["availability"])
		self.assertEqual("optional", standard[8]["availability"])
		self.assertEqual("optional", standard[24]["availability"])
		self.assertEqual(5, standard[24]["wiring"]["nominal_voltage_v"])
		self.assertEqual("virtual", standard[33]["kind"])
		self.assertNotIn("wiring", standard[33])
		self.assertEqual("J8-P11", standard[9]["wiring"]["control_connection"])

	def test_lamp_matrix_and_general_illumination_are_complete(self) -> None:
		used = set(range(1, 54)) | {58, 60, 61, 62}
		for definition in (self.standard, self.le):
			lamps = bindings(definition, "outputs", "pinmame.output.lamp")
			self.assertEqual(set(range(1, 81)), set(lamps))
			self.assertEqual(used, {address for address, lamp in lamps.items() if lamp["availability"] == "used"})
			self.assertEqual("Mick position 1 home", lamps[53]["label"])
			self.assertEqual("unused", lamps[54]["availability"])
			self.assertIn("no Mick-position-5", lamps[54]["physical"]["notes"])
			self.assertEqual({0}, set(bindings(definition, "outputs", "pinmame.output.gi")))

	def test_moving_mick_causality_is_complete(self) -> None:
		for definition in (self.standard, self.le):
			mechanisms = {item["id"]: item for item in definition["mechanisms"]}
			mick = mechanisms["mechanism.moving-mick"]
			self.assertEqual(["device.mick-motor-relay-left", "device.mick-motor-relay-right"], mick["actuators"])
			self.assertEqual(8, len(mick["sensors"]))
			self.assertEqual(7, len(mick["positions"]))
			self.assertIn("share dedicated hit switch 72", mick["behavior"])
			self.assertIn("-27..+36 degrees", mick["behavior"])
			self.assertEqual(["switch.mick-position-5-park"], mick["positions"][4]["sensors"])

	def test_le_ceramic_ball_and_magnetized_diverter_are_recreatable(self) -> None:
		standard = {item["id"]: item for item in self.standard["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertNotIn("mechanism.magnetic-ball-diverter", standard)
		self.assertNotIn("mechanism.ceramic-ball", standard)
		diverter = limited_edition["mechanism.magnetic-ball-diverter"]
		self.assertEqual({"device.left-magnet", "device.right-magnet", "device.left-up-down-post", "device.center-up-down-post", "device.right-up-down-post"}, set(diverter["actuators"]))
		self.assertIn("Public 87/85", diverter["behavior"])
		ceramic = limited_edition["mechanism.ceramic-ball"]
		self.assertIn("preserves its identity", ceramic["behavior"])
		self.assertIn("restores it after shooter switch 23 clears", ceramic["behavior"])

	def test_source_and_exact_rom_hash_constants_are_pinned(self) -> None:
		for definition in (self.standard, self.le):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("1c9dd7f3085ccb159ec2ef976c29602b704c979e7ffcbbfe6bad987916bd22bf", sources["manual.rolling-stones-standard-le.2011"]["sha256"])
			self.assertEqual("969b5a547874f611e55a2cf09dfabcc02f63a816b27e6d459b65f7f6f5298033", sources["vpx.rolling-stones-le-1.0.6i"]["sha256"])
		self.assertNotIn("vpx-table.rolling-stones-le-archive-2020", {source["id"] for source in self.standard["sources"]})
		exact_table = next(source for source in self.le["sources"] if source["id"] == "vpx-table.rolling-stones-le-archive-2020")
		self.assertTrue(exact_table["known_working"])
		self.assertEqual("da987677bdad1cdf07ff4a6f65e7bbbd056619fb4490e3d926147503fd90cf10", exact_table["sha256"])
		self.assertIn("Tables Archive", exact_table["locator"])
		vpu_table = next(source for source in self.le["sources"] if source["id"] == "vpuniverse.rolling-stones-balutito-mod-2-0-24384")
		self.assertEqual("https://vpuniverse.com/files/file/24384-rolling-stones-the-stern-2011-balutitomod-20/", vpu_table["uri"])
		self.assertEqual("human_review", vpu_table["kind"])
		self.assertIn("ROM Name rsn_110h", vpu_table["locator"])
		self.assertIn("no table artifact was downloaded or hashed", vpu_table["locator"])
		self.assertNotIn("sha256", vpu_table)
		self.assertNotIn("known_working", vpu_table)
		standard_vpu_identity = next(source for source in self.standard["sources"] if source["id"] == "vpuniverse.rolling-stones-balutito-mod-2-0-24384")
		self.assertIn("disqualified", standard_vpu_identity["locator"])
		self.assertEqual("1d17d6faf937bfa583e7c8f0a822bc9db0aee74b205f043f9068fbcff58bb563", self.standard_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("56292ef32243878eb6347fbb64dc8e0684ae2b49e0c33f75593a2de133329c59", self.standard_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("cd01ff42364505034e9bdaabf211852a8ecc6ae499371840687e8297abfcaadf", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("81e0780965d9af7f37fffe036da6e6d6bee76905f14b594fbc744534f57bc72c", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])
		for evidence in (self.standard_evidence, self.le_evidence):
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], evidence["runtime"]["observations"]["display_layouts_seen"])
			self.assertEqual({1} | set(range(3, 54)) | {58, 60, 61, 62}, set(evidence["runtime"]["observations"]["lamp_addresses_seen"]))
		self.assertIn("<external-json>", self.standard_evidence["runtime"]["command_template"])
		self.assertNotIn("E:\\", self.standard_evidence["runtime"]["command_template"])
		self.assertNotIn("L:\\", self.standard_evidence["runtime"]["command_template"])

	def test_every_runtime_observation_resolves_to_a_declared_output(self) -> None:
		for definition, evidence in ((self.standard, self.standard_evidence), (self.le, self.le_evidence)):
			groups = {
				"solenoid_addresses_seen": bindings(definition, "outputs", "pinmame.output.solenoid"),
				"lamp_addresses_seen": bindings(definition, "outputs", "pinmame.output.lamp"),
				"gi_addresses_seen": bindings(definition, "outputs", "pinmame.output.gi"),
			}
			for observation, declared in groups.items():
				self.assertFalse(set(evidence["runtime"]["observations"][observation]) - set(declared), observation)

	def test_bindings_and_semantic_ids_are_unique(self) -> None:
		for definition in (self.standard, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))

	def test_curators_are_import_pure(self) -> None:
		for relative_path in ("tools/curate_rolling_stones.py", "tools/curate_rolling_stones_le_spatial.py"):
			tree = ast.parse((ROOT / relative_path).read_text(encoding="utf-8"), filename=relative_path)
			mutating_calls = []
			for statement in tree.body:
				if isinstance(statement, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
					continue
				if isinstance(statement, ast.If) and isinstance(statement.test, ast.Compare) and isinstance(statement.test.left, ast.Name) and statement.test.left.id == "__name__":
					continue
				for node in ast.walk(statement):
					if not isinstance(node, ast.Call):
						continue
					name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
					if name in {"write", "write_json", "write_text", "unlink", "remove"}:
						mutating_calls.append(name)
			self.assertEqual([], mutating_calls, relative_path)

	def test_base_main_repairs_missing_le_promotion_without_clobber_or_order_dependency(self) -> None:
		base_name = "curate_rolling_stones_main_lifecycle_test"
		spatial_name = "curate_rolling_stones_le_spatial_lifecycle_test"
		base_spec = importlib.util.spec_from_file_location(base_name, ROOT / "tools" / "curate_rolling_stones.py")
		self.assertIsNotNone(base_spec)
		self.assertIsNotNone(base_spec.loader)
		base = importlib.util.module_from_spec(base_spec)
		spatial_spec = importlib.util.spec_from_file_location(spatial_name, ROOT / "tools" / "curate_rolling_stones_le_spatial.py")
		self.assertIsNotNone(spatial_spec)
		self.assertIsNotNone(spatial_spec.loader)
		spatial = importlib.util.module_from_spec(spatial_spec)
		previous_base = sys.modules.get("curate_rolling_stones")
		previous_spatial = sys.modules.get("curate_rolling_stones_le_spatial")
		src_path = str(ROOT / "src")
		path_was_present = src_path in sys.path
		if not path_was_present:
			sys.path.insert(0, src_path)
		sys.modules["curate_rolling_stones"] = base
		sys.modules["curate_rolling_stones_le_spatial"] = spatial
		try:
			base_spec.loader.exec_module(base)
			spatial_spec.loader.exec_module(spatial)
			with tempfile.TemporaryDirectory() as temporary:
				root = Path(temporary)
				base.ROOT = root
				spatial.ROOT = root
				spatial.PARTIAL_PATH = root / "machines/partial/stern/the-rolling-stones-limited-edition-2011.json"
				spatial.AUTHOR_READY_PATH = root / "machines/author-ready/stern/the-rolling-stones-limited-edition-2011.json"
				spatial.KNOWLEDGE_PATH = root / "knowledge/stern/the-rolling-stones-limited-edition-2011.md"
				spatial.PARTIAL_PATH.parent.mkdir(parents=True)
				spatial.PARTIAL_PATH.write_text("fail-closed partial\n", encoding="utf-8")
				base.main()
				self.assertTrue(spatial.AUTHOR_READY_PATH.is_file())
				self.assertFalse(spatial.PARTIAL_PATH.exists())
				self.assertEqual("author_ready", load_json(spatial.AUTHOR_READY_PATH)["coverage"]["status"])

			with tempfile.TemporaryDirectory() as temporary:
				root = Path(temporary)
				base.ROOT = root
				spatial.ROOT = root
				spatial.PARTIAL_PATH = root / "machines/partial/stern/the-rolling-stones-limited-edition-2011.json"
				spatial.AUTHOR_READY_PATH = root / "machines/author-ready/stern/the-rolling-stones-limited-edition-2011.json"
				spatial.KNOWLEDGE_PATH = root / "knowledge/stern/the-rolling-stones-limited-edition-2011.md"
				spatial.promote()
				promoted_bytes = spatial.AUTHOR_READY_PATH.read_bytes()
				base.main()
				self.assertEqual(promoted_bytes, spatial.AUTHOR_READY_PATH.read_bytes())
				self.assertFalse(spatial.PARTIAL_PATH.exists())

			with tempfile.TemporaryDirectory() as temporary:
				root = Path(temporary)
				base.ROOT = root
				le_path = root / "machines/author-ready/stern/the-rolling-stones-limited-edition-2011.json"
				le_path.parent.mkdir(parents=True)
				le_path.write_text("{\"promoted\":true}\n", encoding="utf-8")
				base.main()
				self.assertEqual("{\"promoted\":true}\n", le_path.read_text(encoding="utf-8"))
				self.assertFalse((root / "machines/partial/stern/the-rolling-stones-limited-edition-2011.json").exists())
		finally:
			if previous_base is None:
				sys.modules.pop("curate_rolling_stones", None)
			else:
				sys.modules["curate_rolling_stones"] = previous_base
			if previous_spatial is None:
				sys.modules.pop("curate_rolling_stones_le_spatial", None)
			else:
				sys.modules["curate_rolling_stones_le_spatial"] = previous_spatial
			if not path_was_present:
				sys.path.remove(src_path)


if __name__ == "__main__":
	unittest.main()
