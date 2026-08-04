from __future__ import annotations

import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = ROOT / "machines" / "author-ready" / "stern" / "metallica-premium-limited-edition-2013.json"
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "metallica-pro-2013.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "metallica-premium-boot-start.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "metallica-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class MetallicaDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.premium = load_json(PREMIUM_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)

	def test_premium_is_author_ready_while_pro_remains_fail_closed(self) -> None:
		self.assertEqual(2, self.premium["schema_version"])
		self.assertEqual("physical_pinball", self.premium["machine"]["kind"])
		self.assertEqual("author_ready", self.premium["coverage"]["status"])
		self.assertEqual([], self.premium["coverage"]["missing"])
		self.assertEqual("validated", self.premium["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual("complete", self.premium["knowledge"]["status"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		self.assertEqual("complete", self.pro["knowledge"]["status"])
		self.assertTrue((ROOT / "machines" / "partial" / "stern" / "metallica-pro-2013.json").exists())
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "metallica-premium-limited-edition-2013.json").exists())

	def test_premium_spatial_inventory_disposes_every_device(self) -> None:
		devices = [*self.premium["inputs"], *self.premium["outputs"]]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		for device in devices:
			for placement in device["spatial"].get("placements", []):
				self.assertGreaterEqual(placement["x"], 0)
				self.assertLessEqual(placement["x"], 1)
				self.assertGreaterEqual(placement["y"], 0)
				self.assertLessEqual(placement["y"], 1)
		inputs = bindings(self.premium, "inputs", "pinmame.input.switch")
		self.assertEqual((0.282798, 0.720336), tuple(inputs[26]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.701945, 0.719894), tuple(inputs[27]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.551829, 0.309179), tuple(bindings(self.premium, "outputs", "pinmame.output.solenoid")[53]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (15, 16, 65, 66, 67, 68, 69, 82, 84):
			self.assertEqual(("not_applicable", "cabinet_or_service"), (inputs[address]["spatial"]["status"], inputs[address]["spatial"]["reason"]))
		self.assertEqual(["flipper.lower.left.eos"], inputs[83]["roles"])
		self.assertEqual(["flipper.lower.right.eos"], inputs[81]["roles"])

	def test_premium_spatial_lighting_preserves_physical_multiplicity(self) -> None:
		lamps = bindings(self.premium, "outputs", "pinmame.output.lamp")
		self.assertEqual((0.810352, 0.448962), tuple(lamps[17]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.143356, 0.571677), tuple(lamps[87]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (25, 53):
			self.assertEqual((2, 1), (lamps[address]["physical"]["quantity"], len(lamps[address]["spatial"]["placements"])))
			self.assertIn("one composite light anchor", lamps[address]["physical"]["notes"])
		self.assertEqual((11, 10), (lamps[130]["physical"]["quantity"], len(lamps[130]["spatial"]["placements"])))
		self.assertEqual((11, 11), (lamps[132]["physical"]["quantity"], len(lamps[132]["spatial"]["placements"])))
		self.assertEqual((11, 5), (lamps[134]["physical"]["quantity"], len(lamps[134]["spatial"]["placements"])))
		self.assertEqual((28, 22), (lamps[136]["physical"]["quantity"], len(lamps[136]["spatial"]["placements"])))
		self.assertTrue(all(lamps[address]["spatial"]["reason"] == "cabinet_or_service" for address in (72, 76)))
		aggregate = bindings(self.premium, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(("not_applicable", "internal_nonvisual"), (aggregate["spatial"]["status"], aggregate["spatial"]["reason"]))
		self.assertIn("not another physical GI circuit", aggregate["physical"]["notes"])

	def test_premium_spatial_flashers_keep_manual_quantities(self) -> None:
		solenoids = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		self.assertEqual((2, 2), (solenoids[26]["physical"]["quantity"], len(solenoids[26]["spatial"]["placements"])))
		self.assertEqual((2, 2), (solenoids[27]["physical"]["quantity"], len(solenoids[27]["spatial"]["placements"])))
		self.assertEqual((2, 2), (solenoids[28]["physical"]["quantity"], len(solenoids[28]["spatial"]["placements"])))
		self.assertEqual((2, 1), (solenoids[31]["physical"]["quantity"], len(solenoids[31]["spatial"]["placements"])))
		for address in (21, 22):
			self.assertEqual(3, solenoids[address]["physical"]["quantity"])
			self.assertEqual(("not_applicable", "cabinet_or_service"), (solenoids[address]["spatial"]["status"], solenoids[address]["spatial"]["reason"]))

	def test_driver_family_is_split_without_overlap_or_omission(self) -> None:
		expected_premium = {"mtl_113h", "mtl_116h", "mtl_120h", "mtl_122h", "mtl_150h", "mtl_151h", "mtl_160h", "mtl_163h", "mtl_164h", "mtl_164hc", "mtl_170h", "mtl_170hc", "mtl_180h", "mtl_180hc"}
		expected_pro = {"mtl_052", "mtl_103", "mtl_105", "mtl_106", "mtl_112", "mtl_113", "mtl_116", "mtl_120", "mtl_122", "mtl_150", "mtl_151", "mtl_160", "mtl_163", "mtl_163d", "mtl_164", "mtl_164c", "mtl_170", "mtl_170c", "mtl_180", "mtl_180c"}
		premium = {driver["id"] for driver in self.premium["drivers"]}
		pro = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual(expected_premium, premium)
		self.assertEqual(expected_pro, pro)
		self.assertFalse(premium & pro)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("mtl_")}, premium | pro)

	def test_every_premium_input_address_is_explicit_and_corrected(self) -> None:
		switches = bindings(self.premium, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.premium, "inputs", "pinmame.input.dip")))
		self.assertEqual(96, len(self.premium["inputs"]))
		self.assertEqual("Shooter lane jam", switches[22]["label"])
		self.assertEqual("Shooter lane", switches[23]["label"])
		self.assertEqual("Grave marker opto", switches[52]["label"])
		self.assertEqual("Electric chair opto", switches[53]["label"])
		self.assertEqual("Coffin magnet ball detect", switches[63]["label"])
		self.assertTrue(switches[83]["normally_closed"])
		self.assertTrue(switches[81]["normally_closed"])
		self.assertTrue(all(switches[number]["normally_closed"] for number in (60, 61, 62)))

	def test_pro_input_inventory_excludes_premium_only_switches(self) -> None:
		switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.pro, "inputs", "pinmame.input.dip")))
		self.assertEqual(96, len(self.pro["inputs"]))
		self.assertEqual("Shooter lane jam", switches[22]["label"])
		self.assertEqual("Shooter lane", switches[23]["label"])
		self.assertEqual("Grave marker opto", switches[52]["label"])
		self.assertEqual("Electric chair opto", switches[53]["label"])
		self.assertTrue(all(switches[number]["normally_closed"] for number in (60, 61, 62)))
		for number in (33, 34, 38, 39, 55, 56, 57, 58, 59, 63, 64):
			self.assertEqual("unused", switches[number]["availability"])

	def test_main_auxiliary_and_processor_outputs_are_complete(self) -> None:
		solenoids = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 59)), set(solenoids))
		self.assertEqual("virtual", solenoids[33]["kind"])
		self.assertNotIn("wiring", solenoids[33])
		self.assertEqual({33, 34, 35}, set(bindings(self.premium, "outputs", "physical.output.ticket")))
		self.assertEqual("unused", solenoids[7]["availability"])
		self.assertEqual("unused", solenoids[17]["availability"])
		self.assertEqual("optional", solenoids[8]["availability"])
		self.assertEqual("Coffin lock release", solenoids[51]["label"])
		self.assertEqual("Loop up post", solenoids[55]["label"])
		self.assertEqual("Coffin processor D0 mode bit", solenoids[57]["label"])
		self.assertEqual("Coffin processor D1 mode bit", solenoids[58]["label"])
		self.assertEqual("520-6801-00 coffin magnet processor board", solenoids[57]["wiring"]["board"])

	def test_pro_outputs_are_complete_without_premium_auxiliary_hardware(self) -> None:
		solenoids = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(solenoids))
		self.assertEqual("virtual", solenoids[33]["kind"])
		self.assertNotIn("wiring", solenoids[33])
		self.assertEqual({33, 34, 35}, set(bindings(self.pro, "outputs", "physical.output.ticket")))
		self.assertEqual("Loop up post diverter", solenoids[7]["label"])
		self.assertEqual("Drop targets reset", solenoids[12]["label"])
		self.assertEqual("Electric chair step-up driver", solenoids[18]["label"])
		self.assertEqual("unused", solenoids[17]["availability"])
		self.assertEqual("optional", solenoids[8]["availability"])
		self.assertEqual("optional", solenoids[24]["availability"])
		self.assertFalse(set(range(51, 59)) & set(solenoids))

	def test_standard_lamp_matrix_is_complete(self) -> None:
		lamps = bindings(self.premium, "outputs", "pinmame.output.lamp")
		self.assertTrue(set(range(1, 81)).issubset(lamps))
		expected_unused = set(range(1, 17)) | {20, 36, 52, 54}
		self.assertEqual(expected_unused, {address for address in range(1, 81) if lamps[address]["availability"] == "unused"})
		self.assertEqual("Right loop Electric Chair", lamps[17]["label"])
		self.assertEqual("Tournament start", lamps[76]["label"])

	def test_pro_lamp_matrix_and_ordinary_gi_are_complete(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		expected_unused = {3, 28, 39, 59, 66, 72, 74, 76, 77, 79, 80}
		self.assertEqual(expected_unused, {address for address in range(1, 81) if lamps[address]["availability"] == "unused"})
		self.assertEqual("Start button", lamps[1]["label"])
		self.assertEqual("Grave lane Grave Marker", lamps[40]["label"])
		self.assertEqual("Electric Chair 3 right", lamps[78]["label"])
		self.assertFalse(set(range(81, 137)) & set(lamps))
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))

	def test_rgb_and_gi_use_exact_public_table_bindings(self) -> None:
		lamps = bindings(self.premium, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(81, 129)), set(lamps) & set(range(81, 129)))
		used = {87, 88, 89, 90, 91, 92, 99, 100, 101, 102, 103, 104, 108, 109, 110, 126, 127, 128}
		self.assertEqual(used, {address for address in range(81, 129) if lamps[address]["availability"] == "used"})
		for base, connector in ((87, "CN4"), (90, "CN5"), (99, "CN9"), (102, "CN11"), (108, "CN13"), (126, "CN19")):
			self.assertEqual([f"{connector} RGB blue", f"{connector} RGB green", f"{connector} RGB red"], [lamps[address]["label"] for address in range(base, base + 3)])
		self.assertEqual({130, 132, 134, 136}, {address for address, item in lamps.items() if item["kind"] == "gi"})
		self.assertEqual({0}, set(bindings(self.premium, "outputs", "pinmame.output.gi")))

	def test_custom_mechanisms_preserve_authoring_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.premium["mechanisms"]}
		expected = {"mechanism.trough", "mechanism.auto-launcher", "mechanism.right-eject", "mechanism.grave-marker", "mechanism.electric-chair", "mechanism.captive-ball-hammer", "mechanism.drop-bank", "mechanism.loop-post", "mechanism.coffin-lock", "mechanism.coffin-magnet", "mechanism.snake", "mechanism.flippers", "mechanism.pop-bumpers", "mechanism.slingshots"}
		self.assertEqual(expected, set(mechanisms))
		self.assertEqual(5, len(mechanisms["mechanism.trough"]["sensors"]))
		self.assertEqual(3, len(mechanisms["mechanism.coffin-lock"]["sensors"]))
		self.assertIn("00 is off", mechanisms["mechanism.coffin-magnet"]["behavior"])
		self.assertIn("10 is detect/hold", mechanisms["mechanism.coffin-magnet"]["behavior"])
		self.assertIn("output 55", mechanisms["mechanism.loop-post"]["behavior"].casefold())
		self.assertEqual(["device.hammer"], mechanisms["mechanism.captive-ball-hammer"]["actuators"])

	def test_pro_mechanisms_preserve_edition_specific_causality(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		expected = {"mechanism.trough", "mechanism.auto-launcher", "mechanism.right-eject", "mechanism.grave-marker-magnet", "mechanism.electric-chair", "mechanism.captive-ball", "mechanism.drop-bank", "mechanism.loop-post", "mechanism.snake", "mechanism.flippers", "mechanism.pop-bumpers", "mechanism.slingshots", "mechanism.optional-shaker", "mechanism.optional-ticket-dispenser"}
		self.assertEqual(expected, set(mechanisms))
		self.assertEqual([], mechanisms["mechanism.captive-ball"]["actuators"])
		self.assertIn("no motorized jaw", mechanisms["mechanism.snake"]["behavior"])
		self.assertIn("output 7", mechanisms["mechanism.loop-post"]["behavior"].casefold())
		self.assertEqual(["switch.grave-marker-opto"], mechanisms["mechanism.grave-marker-magnet"]["sensors"])

	def test_exact_rom_run_and_content_hashes_are_locked(self) -> None:
		runtime = self.evidence["runtime"]
		self.assertEqual("mtl_180h", runtime["game"])
		self.assertEqual("141018225cdf51421b579b319b925b6dfd6a2fda98471e16998bd648abd86488", runtime["rom_archive_sha256"])
		self.assertEqual("a9a266a66859c8c4374a2e798f90100bb15c229275ea2b58cc9f653bd48d6510", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
		self.assertEqual([20], runtime["observations"]["solenoid_addresses_seen"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		sources = {source["id"]: source for source in self.premium["sources"]}
		self.assertEqual("f82ecc04bded7117d4c5e3b724dc85e60b5057768bbf7bf5e46c0d1e71a91090", sources["manual.metallica-pro-premium"]["sha256"])
		self.assertEqual("3be5af3f6b05c4f1445c391aab42713bf9e76af87d563bfb061e7bc5daedfd64", sources["vpx.metallica-premium-monsters-vpw-2.0.2"]["sha256"])
		self.assertEqual("afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f", sources["vpx-table.metallica-premium-monsters-vpw-2.0"]["sha256"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "metallica-premium-2013.json").exists())

	def test_pro_runtime_and_downloaded_evidence_hashes_are_locked(self) -> None:
		runtime = self.pro_evidence["runtime"]
		self.assertEqual("mtl_170", runtime["game"])
		self.assertEqual("2f11830ffb35f2a80258e47a5ea0abd17fc2350995bb1d1d1a165480be61f654", runtime["rom_archive_sha256"])
		self.assertEqual("65fa45916ba42165b334bdcee7dea1bae25d0e0feee44cc887102b167c70d49e", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
		self.assertEqual([24], runtime["observations"]["solenoid_addresses_seen"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("d5ea2810308e05daee22c2a75b3d80a4b19fbd3f89e67144a38f9c20bdb33307", sources["vpx.metallica-pro-jps-6.0.0"]["sha256"])
		self.assertEqual("837ee8d05e0f61e51136d397737d85e4ec14d41859abfb6e789785b82a60a118", sources["vpx-table.metallica-pro-jps-6.0.0"]["sha256"])

	def test_premium_spatial_sources_are_content_locked_and_known_working(self) -> None:
		sources = {source["id"]: source for source in self.premium["sources"]}
		table = sources["vpx-table.metallica-premium-monsters-vpw-2.0"]
		self.assertTrue(table["known_working"])
		self.assertEqual("afc1f1b300b2b2226db6edc5986007c05ac714db5ce69a582730e2a346ecb17f", table["sha256"])
		self.assertIn("952.941 by 2117.647", table["locator"])
		self.assertIn("PDF pages 45-50", sources["manual.metallica-pro-premium"]["locator"])
		inputs = bindings(self.premium, "inputs", "pinmame.input.switch")
		self.assertEqual(["manual.metallica-pro-premium"], inputs[22]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual(
			["manual.metallica-pro-premium", "vpx.metallica-premium-monsters-vpw-2.0.2", "vpx-table.metallica-premium-monsters-vpw-2.0"],
			inputs[23]["spatial"]["placements"][0]["provenance"]["source_refs"],
		)

	def test_base_generator_has_no_import_time_writes(self) -> None:
		source = (ROOT / "tools" / "curate_metallica.py").read_text(encoding="utf-8")
		tree = ast.parse(source)
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
				if name in {"write", "write_json", "write_text", "unlink"}:
					mutating_calls.append(name)
		self.assertEqual([], mutating_calls)

	def test_base_generator_does_not_clobber_promoted_premium_artifacts(self) -> None:
		spec = importlib.util.spec_from_file_location("curate_metallica_no_clobber_test", ROOT / "tools" / "curate_metallica.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		with tempfile.TemporaryDirectory() as temporary:
			module.ROOT = Path(temporary)
			definition_path = module.ROOT / "machines" / "author-ready" / "stern" / "metallica-premium-limited-edition-2013.json"
			definition_path.parent.mkdir(parents=True)
			definition_path.write_text('{"promoted": true}\n', encoding="utf-8")
			knowledge_path = module.ROOT / "knowledge" / "stern" / "metallica-premium-limited-edition-2013.md"
			knowledge_path.parent.mkdir(parents=True)
			knowledge_path.write_text("promoted spatial knowledge\n", encoding="utf-8")
			module.main()
			self.assertEqual('{"promoted": true}\n', definition_path.read_text(encoding="utf-8"))
			self.assertEqual("promoted spatial knowledge\n", knowledge_path.read_text(encoding="utf-8"))
			self.assertFalse((module.ROOT / "machines" / "partial" / "stern" / "metallica-premium-limited-edition-2013.json").exists())


if __name__ == "__main__":
	unittest.main()
