from __future__ import annotations

import json
import hashlib
import importlib.util
import os
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LE_PATH = ROOT / "machines" / "partial" / "stern" / "x-men-limited-edition-2012.json"
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "x-men-pro-2012.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "x-men-limited-edition-boot-start.json"


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


class XMenDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.le = load_json(LE_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_le_remains_fail_closed_while_pro_remains_partial(self) -> None:
		self.assertEqual(2, self.le["schema_version"])
		self.assertEqual("partial", self.le["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.le["coverage"]["missing"])
		self.assertEqual("unknown", self.le["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		for definition in (self.le, self.pro):
			self.assertEqual("complete", definition["knowledge"]["status"])
			self.assertEqual([], definition["conflicts"])
		self.assertTrue(LE_PATH.exists())
		self.assertFalse((ROOT / "machines" / "author-ready" / "stern" / "x-men-limited-edition-2012.json").exists())
		self.assertTrue(PRO_PATH.exists())

	def test_le_spatial_records_preserve_exact_table_geometry_and_manual_multiplicity(self) -> None:
		switches = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		unresolved_bindings = {
			("pinmame.input.switch", 22),
			("pinmame.output.solenoid", 19),
			("pinmame.output.solenoid", 20),
			("pinmame.output.solenoid", 30),
		}
		located_devices = [device for device in [*self.le["inputs"], *self.le["outputs"]] if (device["binding"]["group"], device["binding"]["device"]) not in unresolved_bindings]
		self.assertTrue(all("spatial" in device for device in located_devices))
		self.assertEqual("validated", switches[34]["spatial"]["status"])
		self.assertEqual((0.713607, 0.753937), (switches[34]["spatial"]["placements"][0]["x"], switches[34]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.926444, 0.376846), (switches[35]["spatial"]["placements"][0]["x"], switches[35]["spatial"]["placements"][0]["y"]))
		self.assertEqual("cabinet_or_service", switches[82]["spatial"]["reason"])
		self.assertEqual("internal_nonvisual", outputs[54]["spatial"]["reason"])
		self.assertEqual("virtual", outputs[33]["spatial"]["reason"])
		for address in (6, 7):
			self.assertEqual((0.526092, 0.204412), (outputs[address]["spatial"]["placements"][0]["x"], outputs[address]["spatial"]["placements"][0]["y"]))
			self.assertIn("Derived/shared assembly geometry", outputs[address]["physical"]["notes"])
			self.assertIn("Trigger.sw53.center", outputs[address]["physical"]["notes"])
			self.assertNotIn((0.526589, 0.204940), {(placement["x"], placement["y"]) for placement in outputs[address]["spatial"]["placements"]})
		self.assertEqual(31, self.le["outputs"][-1]["physical"]["quantity"])
		self.assertEqual(3, outputs[28]["physical"]["quantity"])
		self.assertEqual(3, outputs[29]["physical"]["quantity"])
		self.assertEqual(2, outputs[31]["physical"]["quantity"])
		self.assertEqual(2, outputs[17]["physical"]["quantity"])
		self.assertEqual(1, outputs[18]["physical"]["quantity"])
		self.assertEqual(2, outputs[19]["physical"]["quantity"])
		self.assertEqual(2, outputs[20]["physical"]["quantity"])
		flasher_outputs = {address: outputs[address] for address in (17, 18, 19, 20, 21, 22, 25, 28, 29, 30, 31, 32)}
		self.assertEqual(21, sum(device["physical"]["quantity"] for device in flasher_outputs.values()))
		self.assertEqual(16, sum(len(device.get("spatial", {}).get("placements", [])) for device in flasher_outputs.values()))
		for address in (19, 20, 30):
			self.assertNotIn("spatial", flasher_outputs[address])
		self.assertEqual(1, flasher_outputs[30]["physical"]["quantity"])
		self.assertIn("Cyclops spinner proxy", flasher_outputs[30]["physical"]["notes"])
		self.assertIn("No f130 emitter exists", flasher_outputs[30]["physical"]["notes"])
		self.assertEqual([(0.608390, 0.169829), (0.450827, 0.172193)], [(placement["x"], placement["y"]) for placement in flasher_outputs[22]["spatial"]["placements"]])
		self.assertEqual(["device.magneto-left-right-double-flasher.emitter.f122a", "device.magneto-left-right-double-flasher.emitter.f122b"], [placement["id"] for placement in flasher_outputs[22]["spatial"]["placements"]])
		self.assertTrue(all(placement["provenance"]["source_refs"] == ["vpx-table.x-men-le-v2.0.1"] for placement in flasher_outputs[22]["spatial"]["placements"]))
		self.assertIn("Primitive.Target_004_*/Target_001_*", flasher_outputs[22]["physical"]["notes"])
		self.assertEqual((0.951053, 0.309522), (flasher_outputs[18]["spatial"]["placements"][0]["x"], flasher_outputs[18]["spatial"]["placements"][0]["y"]))
		self.assertEqual(1, len(flasher_outputs[18]["spatial"]["placements"]))
		self.assertEqual((0.148958, 0.018409), (flasher_outputs[28]["spatial"]["placements"][0]["x"], flasher_outputs[28]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.837139, 0.018409), (flasher_outputs[29]["spatial"]["placements"][2]["x"], flasher_outputs[29]["spatial"]["placements"][2]["y"]))
		self.assertEqual((0.118833, 0.882520), (flasher_outputs[31]["spatial"]["placements"][0]["x"], flasher_outputs[31]["spatial"]["placements"][0]["y"]))
		self.assertNotIn((0.0, 1.0), {(placement["x"], placement["y"]) for placement in flasher_outputs[31]["spatial"]["placements"]})
		self.assertEqual("cabinet_or_service", lamps[39]["spatial"]["reason"])
		self.assertEqual(57, sum(1 for lamp in lamps.values() if lamp["spatial"]["status"] == "validated"))
		switches = bindings(self.le, "inputs", "pinmame.input.switch")
		self.assertEqual("Trough jam", switches[22]["label"])
		self.assertEqual("opto", switches[22]["physical"]["switch_type"])
		self.assertNotIn("spatial", switches[22])
		placements = [placement for device in [*self.le["inputs"], *self.le["outputs"]] for placement in device.get("spatial", {}).get("placements", [])]
		self.assertTrue(all(len(placement["provenance"]["source_refs"]) == 1 for placement in placements))
		self.assertNotIn((0.469952, 0.241956), {(placement["x"], placement["y"]) for placement in placements})
		self.assertNotIn((0.591291, 0.242244), {(placement["x"], placement["y"]) for placement in placements})
		self.assertNotIn((0.689153, 0.184374), {(placement["x"], placement["y"]) for placement in placements})
		self.assertEqual(["vpx-table.x-men-le-vpw-1.0"], switches[21]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual(["vpx-table.x-men-le-v2.0.1"], flasher_outputs[18]["spatial"]["placements"][0]["provenance"]["source_refs"])
		sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("vpx_table", sources["vpx-table.x-men-le-vpw-1.0"]["kind"])
		self.assertEqual("332c0a822024e7e0701e3939bdde0c0e0e4026479ef86414f93887681b3fa22e", sources["vpx-table.x-men-le-vpw-1.0"]["sha256"])
		self.assertEqual("5b78b36d07ed2f06c5aad360deb04c67d8f31fce9770843a178aac1bd624f5a7", sources["vpx-table.x-men-le-v2.0.1"]["sha256"])
		for source_id in ("vpx-table.x-men-le-vpw-1.0", "vpx-table.x-men-le-v2.0.1", "vpx-table.x-men-le-v2.2.7a-test"):
			self.assertTrue(sources[source_id]["uri"].startswith("external:pinmame-vpx-sources/stern/x-men-limited-edition-2012/source/"))
			self.assertNotIn("local-evidence://", json.dumps(sources[source_id]))
			self.assertNotRegex(json.dumps(sources[source_id]), r"L:[\\\\/]")
		self.assertNotIn("vpx-table.x-men-pro-physmod5", {ref for device in self.le["outputs"] for placement in device.get("spatial", {}).get("placements", []) for ref in placement.get("provenance", {}).get("source_refs", [])})
		knowledge = (ROOT / "knowledge" / "stern" / "x-men-limited-edition-2012.md").read_text(encoding="utf-8")
		self.assertIn("F30 exact emitter geometry is unresolved", knowledge)
		self.assertIn("F19/F20 per-socket geometry, F30 emitter geometry, and switch 22 exact geometry", knowledge)

	def test_le_vpx_cache_is_byte_identical_and_review_artifacts_are_retained(self) -> None:
		sources = {source["id"]: source for source in self.le["sources"]}
		source_root = external_root("PINMAME_VPX_SOURCES_ROOT") / "stern" / "x-men-limited-edition-2012" / "source"
		review_root = external_root("PINMAME_REVIEW_ARTIFACTS_ROOT") / "stern" / "x-men-limited-edition-2012"
		for source_id in ("vpx-table.x-men-le-vpw-1.0", "vpx-table.x-men-le-v2.0.1", "vpx-table.x-men-le-v2.2.7a-test"):
			path = source_root / sources[source_id]["original_filename"]
			self.assertTrue(path.is_file(), path)
			digest = hashlib.sha256()
			with path.open("rb") as stream:
				for chunk in iter(lambda: stream.read(1024 * 1024), b""):
					digest.update(chunk)
			self.assertEqual(sources[source_id]["sha256"], digest.hexdigest())
		self.assertTrue((review_root / "spatial-candidates-vpw-v1.0.json").is_file())
		self.assertTrue((source_root.parent / "extraction" / "VPW_v1.0").is_dir())

	def test_changed_xmen_prose_contains_no_developer_absolute_paths(self) -> None:
		for path in (ROOT / "docs" / "MACHINE_DEFINITIONS_PLAN.md", ROOT / "tests" / "test_xmen.py"):
			self.assertNotRegex(path.read_text(encoding="utf-8"), re.compile(r"(?i)\b[a-z]:[\\/]"), path)

	def test_editions_split_every_supported_xmen_driver(self) -> None:
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		pro = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"xmn_102", "xmn_120h", "xmn_121h", "xmn_122h", "xmn_123h", "xmn_124h", "xmn_130h", "xmn_150h", "xmn_151h", "xmn_151hc"}, limited_edition)
		self.assertEqual({"xmn_100", "xmn_104", "xmn_105", "xmn_130", "xmn_150", "xmn_151", "xmn_151c"}, pro)
		self.assertFalse(limited_edition & pro)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("xmn_")}, limited_edition | pro)

	def test_switch_inventory_is_complete_and_marks_le_only_hardware(self) -> None:
		for definition in (self.le, self.pro):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Iceman home", bindings(self.le, "inputs", "pinmame.input.switch")[34]["label"])
		self.assertEqual("Right Nightcrawler down", bindings(self.le, "inputs", "pinmame.input.switch")[56]["label"])
		pro_switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertTrue(all(pro_switches[address]["availability"] == "unused" for address in (12, 34, 35, 50, 51, 56)))

	def test_le_main_auxiliary_and_virtual_outputs_are_distinct(self) -> None:
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 59)), set(outputs))
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		self.assertEqual("Q41", outputs[51]["wiring"]["driver_transistor"])
		self.assertEqual("Q48", outputs[58]["wiring"]["driver_transistor"])
		self.assertEqual("ORG-BLU", outputs[56]["wiring"]["control_wire"])
		self.assertEqual("Iceman ramp motor", outputs[27]["label"])
		self.assertEqual("Disc motor power", outputs[23]["label"])

	def test_le_lamp_matrix_and_gi_are_complete(self) -> None:
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		expected_unused = set(range(1, 17)) | {40, 44, 61, 62, 63, 64}
		self.assertEqual(expected_unused, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("Dark Phoenix", lamps[45]["label"])
		self.assertEqual("Magneto green", lamps[65]["label"])
		self.assertEqual({0}, set(bindings(self.le, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_capture_sensor_and_actuator_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertEqual(["device.magneto-magnet", "device.disc-motor-power"], mechanisms["mechanism.magneto-disc"]["actuators"])
		self.assertIn("no index or home switch exists", mechanisms["mechanism.magneto-disc"]["behavior"])
		self.assertEqual(["switch.iceman-home", "switch.iceman-away"], mechanisms["mechanism.iceman-ramp"]["sensors"])
		self.assertEqual([["switch.iceman-home"], ["switch.iceman-away"]], [position["sensors"] for position in mechanisms["mechanism.iceman-ramp"]["positions"]])
		self.assertEqual([], mechanisms["mechanism.left-nightcrawler"]["positions"][1]["sensors"])
		self.assertIn("mechanically", mechanisms["mechanism.left-nightcrawler"]["behavior"])
		self.assertIn("255 minus the output value", mechanisms["mechanism.color-gi"]["behavior"])
		self.assertEqual(["switch.center-lock-1-bottom", "switch.center-lock-2", "switch.center-lock-3", "switch.center-lock-4-top"], mechanisms["mechanism.center-lock"]["sensors"])

	def test_pro_excludes_le_auxiliary_devices_and_preserves_known_difference(self) -> None:
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(outputs))
		self.assertEqual("virtual", outputs[33]["kind"])
		self.assertNotIn("wiring", outputs[33])
		self.assertEqual("Wolverine magnet", outputs[32]["label"])
		self.assertFalse(set(range(51, 59)) & set(outputs))
		mechanisms = {item["id"] for item in self.pro["mechanisms"]}
		self.assertFalse({"mechanism.iceman-ramp", "mechanism.left-nightcrawler", "mechanism.right-nightcrawler", "mechanism.magneto-disc", "mechanism.color-gi"} & mechanisms)

	def test_pro_lamp_matrix_is_complete_semantic_and_hash_locked(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		expected_used = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 60, 61, 62, 65, 66, 67, 68, 69, 70, 71}
		self.assertEqual(expected_used, {address for address, lamp in lamps.items() if lamp["availability"] == "used"})
		self.assertEqual("Left Nightcrawler feature insert", lamps[11]["label"])
		self.assertEqual("Magneto completion medallion right", lamps[49]["label"])
		self.assertEqual("Bottom pop bumper", lamps[62]["label"])
		self.assertIn("x=742.9, y=1130.5", lamps[49]["physical"]["location"])
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8", sources["vpx-table.x-men-pro-physmod5"]["sha256"])

	def test_sources_and_exact_rom_run_are_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("0812b91d0950ff8c1b15c5bc17afc827029ca8aaaa0bbb78cc11ea606b629bf8", sources["manual.x-men-pro-le.2012"]["sha256"])
		self.assertIn("page 60 was visually verified", sources["manual.x-men-pro-le.2012"]["locator"])
		self.assertEqual("d793836fefab6c0de53463943e36245c7ed800d5ca86675e3c2b2f46df693643", sources["manual.x-men-pro-le.2012.high-resolution"]["sha256"])
		self.assertEqual("6d445e52398640bd35a498553bb0ba32f1b9ce23e2964d0694c18ff2e9225650", sources["vpx.x-men-le-vpw-1.0.6"]["sha256"])
		runtime = self.evidence["runtime"]
		self.assertEqual("xmn_151h", runtime["game"])
		self.assertEqual("cc8069743e6a0f45c3b310c0804230241739b5cf8c51f0481d96810f9edab5be", runtime["rom_archive_sha256"])
		self.assertEqual("72730b25d7cec239eac1d8df6039f0c465e2c729070d49acebec8d22aa5cb61c", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])

	def test_bindings_are_unique_within_each_controller_group(self) -> None:
		for definition in (self.le, self.pro):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))

	def test_author_ready_conflict_is_non_destructive_for_both_curators(self) -> None:
		spec = importlib.util.spec_from_file_location("curate_xmen_regeneration_test", ROOT / "tools" / "curate_xmen.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		with tempfile.TemporaryDirectory() as temporary:
			module.ROOT = Path(temporary)
			definition_path = module.ROOT / "machines" / "author-ready" / "stern" / "x-men-limited-edition-2012.json"
			definition_path.parent.mkdir(parents=True)
			definition_path.write_bytes(b'{"coverage": {"status": "author_ready"}}\n')
			with self.assertRaisesRegex(RuntimeError, "author-ready canonical definition already exists"):
				module.main()
			self.assertTrue(definition_path.exists())
			self.assertFalse((module.ROOT / "machines" / "partial" / "stern" / "x-men-limited-edition-2012.json").exists())
			spatial_spec = importlib.util.spec_from_file_location("curate_xmen_le_spatial_conflict_test", ROOT / "tools" / "curate_xmen_le_spatial.py")
			self.assertIsNotNone(spatial_spec)
			self.assertIsNotNone(spatial_spec.loader)
			spatial_module = importlib.util.module_from_spec(spatial_spec)
			spatial_spec.loader.exec_module(spatial_module)
			with self.assertRaisesRegex(RuntimeError, "author-ready canonical definition already exists"):
				spatial_module.generate(root=module.ROOT)
			self.assertTrue(definition_path.exists())

	def test_base_and_spatial_curators_share_byte_stable_canonical_le_generation(self) -> None:
		base_spec = importlib.util.spec_from_file_location("curate_xmen_ordering_test", ROOT / "tools" / "curate_xmen.py")
		self.assertIsNotNone(base_spec)
		self.assertIsNotNone(base_spec.loader)
		base_module = importlib.util.module_from_spec(base_spec)
		base_spec.loader.exec_module(base_module)
		spec = importlib.util.spec_from_file_location("curate_xmen_le_spatial_regeneration_test", ROOT / "tools" / "curate_xmen_le_spatial.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		spatial_module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(spatial_module)

		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			spatial_module.generate(root=root)
			paths = [root / "machines" / "partial" / "stern" / "x-men-limited-edition-2012.json", root / "knowledge" / "stern" / "x-men-limited-edition-2012.md"]
			spatial_first = [path.read_bytes() for path in paths]
			spatial_module.generate(root=root)
			self.assertEqual(spatial_first, [path.read_bytes() for path in paths])

			base_module.ROOT = root
			base_module.main()
			self.assertEqual(spatial_first, [path.read_bytes() for path in paths])
			self.assertIn(b"F19/F20 per-socket geometry", spatial_first[1])
			self.assertFalse((root / "machines" / "author-ready" / "stern" / "x-men-limited-edition-2012.json").exists())


if __name__ == "__main__":
	unittest.main()
