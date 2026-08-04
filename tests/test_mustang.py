from __future__ import annotations

import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = REPOSITORY_ROOT / "machines" / "author-ready" / "stern" / "mustang-premium-limited-edition-boss-2014.json"
PRO_PATH = REPOSITORY_ROOT / "machines" / "author-ready" / "stern" / "mustang-pro-2014.json"


def load_definition(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def manual_alias(item: dict[str, object]) -> str:
	return next(alias["value"] for alias in item["aliases"] if alias["namespace"] == "manual.address")


class MustangDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.premium = load_definition(PREMIUM_PATH)
		cls.pro = load_definition(PRO_PATH)

	def test_editions_split_the_complete_clone_family(self) -> None:
		premium_drivers = {driver["id"] for driver in self.premium["drivers"]}
		pro_drivers = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"mt_130h", "mt_140h", "mt_140hb", "mt_145h", "mt_145hb", "mt_145hc"}, premium_drivers)
		self.assertEqual({"mt_120", "mt_130", "mt_140", "mt_145", "mt_145c"}, pro_drivers)
		self.assertFalse(premium_drivers & pro_drivers)

	def test_both_physical_editions_are_author_ready(self) -> None:
		for definition in (self.premium, self.pro):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("physical_pinball", definition["machine"]["kind"])
			self.assertEqual("author_ready", definition["coverage"]["status"])
			self.assertEqual([], definition["coverage"]["missing"])
			self.assertEqual("validated", definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(6098, self.pro["machine"]["ipdb_id"])
		self.assertFalse((REPOSITORY_ROOT / "machines" / "partial" / "stern" / "mustang-pro-2014.json").exists())

	def test_physical_trough_inventory_keeps_six_positions_and_jam(self) -> None:
		by_address = {
			item["binding"]["device"]: item
			for item in self.premium["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		self.assertEqual(["microswitch"] * 5, [by_address[number]["physical"]["switch_type"] for number in range(17, 22)])
		self.assertEqual("opto", by_address[22]["physical"]["switch_type"])
		self.assertEqual("opto", by_address[23]["physical"]["switch_type"])
		trough = next(item for item in self.premium["mechanisms"] if item["id"] == "mechanism.trough")
		self.assertEqual(7, len(trough["sensors"]))
		self.assertIn("23,22,21,20,19,18", trough["behavior"])
		self.assertEqual(7, len({tuple(by_address[number]["spatial"]["placements"][0][axis] for axis in ("x", "y")) for number in range(17, 24)}))
		self.assertTrue(all(by_address[number]["spatial"]["placements"][0]["provenance"]["source_refs"] == ["manual.mustang-premium-boss-le"] for number in range(17, 24)))

	def test_auxiliary_board_manual_numbers_map_to_public_addresses(self) -> None:
		by_address = {
			item["binding"]["device"]: item
			for item in self.premium["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}
		self.assertEqual("41", manual_alias(by_address[59]))
		self.assertEqual("42", manual_alias(by_address[60]))
		self.assertEqual("Q41", by_address[59]["wiring"]["driver_transistor"])
		self.assertEqual("Q46", by_address[64]["wiring"]["driver_transistor"])
		self.assertEqual("unused", by_address[64]["availability"])
		self.assertEqual("unused", by_address[66]["availability"])

	def test_extended_lamps_keep_physical_and_runtime_addresses(self) -> None:
		by_manual = {
			manual_alias(item): item
			for item in self.premium["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp" and any(alias["namespace"] == "manual.address" for alias in item["aliases"])
		}
		self.assertEqual(103, by_manual["98"]["binding"]["device"])
		self.assertEqual(98, by_manual["109"]["binding"]["device"])
		self.assertEqual(119, by_manual["117"]["binding"]["device"])
		self.assertEqual(129, by_manual["141"]["binding"]["device"])
		self.assertEqual(144, by_manual["142"]["binding"]["device"])
		self.assertEqual("lamp", by_manual["81"]["kind"])
		self.assertEqual("rgb_lamp", by_manual["117"]["kind"])

	def test_premium_spatial_inventory_preserves_physical_multiplicity_and_scope(self) -> None:
		devices = [*self.premium["inputs"], *self.premium["outputs"]]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		inputs = {item["binding"]["device"]: item for item in self.premium["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		self.assertEqual((0.836685, 0.552217), tuple(inputs[1]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual(("not_applicable", "cabinet_or_service"), (inputs[71]["spatial"]["status"], inputs[71]["spatial"]["reason"]))
		self.assertEqual(inputs[52]["spatial"]["placements"][0]["x"], inputs[53]["spatial"]["placements"][0]["x"])
		outputs = {(item["binding"]["group"], item["binding"]["device"]): item for item in self.premium["outputs"]}
		for address in (31, 32, 61, 62, 63):
			self.assertEqual(("not_applicable", "cabinet_or_service"), (outputs[("pinmame.output.solenoid", address)]["spatial"]["status"], outputs[("pinmame.output.solenoid", address)]["spatial"]["reason"]))
		self.assertEqual((0.069490, 0.082959), tuple(outputs[("pinmame.output.solenoid", 21)]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.920713, 0.070765), tuple(outputs[("pinmame.output.solenoid", 23)]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (20, 21, 22, 23, 79, *range(102, 112)):
			lamp = outputs[("pinmame.output.lamp", address)]
			self.assertEqual((1, 1), (lamp["physical"]["quantity"], len(lamp["spatial"]["placements"])))
		for channels in ((117, 118, 119), (120, 121, 122), (123, 124, 125), (126, 127, 128), (130, 131, 132), (133, 134, 135), (136, 137, 138), (139, 140, 141)):
			points = {tuple(outputs[("pinmame.output.lamp", address)]["spatial"]["placements"][0][axis] for axis in ("x", "y")) for address in channels}
			self.assertEqual(1, len(points))

	def test_premium_gi_is_one_transport_channel_with_four_circuits_and_thirty_two_emitters(self) -> None:
		gi = next(item for item in self.premium["outputs"] if item["binding"]["group"] == "pinmame.output.gi")
		self.assertEqual(0, gi["binding"]["device"])
		self.assertEqual(32, gi["physical"]["quantity"])
		self.assertEqual(32, len(gi["spatial"]["placements"]))
		self.assertEqual(7, sum("rear-red.gi2" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(7, sum("wedge.gi3" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(8, sum("wedge.gi1" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(2, sum("spot-gi1" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(8, sum("bayonet.gi0" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertFalse(any(token in point["id"] for point in gi["spatial"]["placements"] for token in ("GI_ALL", "GIFlash", "field")))
		lamp_98 = next(item for item in self.premium["outputs"] if item["binding"] == {"group": "pinmame.output.lamp", "device": 98})
		self.assertEqual("Shot arrow #1 white", lamp_98["label"])

	def test_pro_extended_lamps_use_proven_runtime_shuffle(self) -> None:
		by_manual = {
			manual_alias(item): item
			for item in self.pro["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp" and any(alias["namespace"] == "manual.address" and alias["value"].isdigit() and int(alias["value"]) >= 81 for alias in item["aliases"])
		}
		self.assertEqual(81, by_manual["81"]["binding"]["device"])
		self.assertEqual(103, by_manual["98"]["binding"]["device"])
		self.assertEqual(102, by_manual["99"]["binding"]["device"])
		self.assertEqual(104, by_manual["100"]["binding"]["device"])
		self.assertEqual(112, by_manual["108"]["binding"]["device"])
		lamps = {item["binding"]["device"]: item for item in self.pro["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertTrue(all(lamps[address]["availability"] == "unused" for address in (3, 43, 44, 98, 99, 100, 101)))
		self.assertEqual("Shot arrow #5", lamps[45]["label"])
		self.assertEqual("Right 3-bank bottom", lamps[49]["label"])
		self.assertEqual("Right pop bumper", lamps[80]["label"])

	def test_pro_spatial_inventory_preserves_conflicts_and_physical_multiplicity(self) -> None:
		devices = [*self.pro["inputs"], *self.pro["outputs"]]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		inputs = {item["binding"]["device"]: item for item in self.pro["inputs"] if item["binding"]["group"] == "pinmame.input.switch"}
		self.assertEqual((0.836685, 0.552217), tuple(inputs[1]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (49, 50):
			self.assertEqual(("unused", "not_applicable"), (inputs[address]["availability"], inputs[address]["spatial"]["status"]))
			self.assertIn("electrical matrix table", inputs[address]["physical"]["notes"])
		self.assertEqual(7, len({tuple(inputs[number]["spatial"]["placements"][0][axis] for axis in ("x", "y")) for number in range(17, 24)}))
		outputs = {(item["binding"]["group"], item["binding"]["device"]): item for item in self.pro["outputs"]}
		orbit_post = outputs[("pinmame.output.solenoid", 31)]
		self.assertEqual((1, 1), (orbit_post["physical"]["quantity"], len(orbit_post["spatial"]["placements"])))
		self.assertIn("tangent UpPost2 collision wall", orbit_post["physical"]["notes"])
		self.assertEqual((0.069490, 0.082959), tuple(outputs[("pinmame.output.solenoid", 21)]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.920713, 0.070765), tuple(outputs[("pinmame.output.solenoid", 23)]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual(outputs[("pinmame.output.lamp", 20)]["spatial"]["placements"][0]["x"], outputs[("pinmame.output.lamp", 26)]["spatial"]["placements"][0]["x"])
		self.assertEqual(outputs[("pinmame.output.lamp", 34)]["spatial"]["placements"][0]["x"], outputs[("pinmame.output.lamp", 42)]["spatial"]["placements"][0]["x"])

	def test_pro_gi_has_thirty_two_physical_emitters_on_one_transport_channel(self) -> None:
		gi = next(item for item in self.pro["outputs"] if item["binding"]["group"] == "pinmame.output.gi")
		self.assertEqual((0, 32, 32), (gi["binding"]["device"], gi["physical"]["quantity"], len(gi["spatial"]["placements"])))
		self.assertEqual(7, sum("rear-red.gi2" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(7, sum("wedge.gi3" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(8, sum("wedge.gi1" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(2, sum("spot-gi1" in point["id"] for point in gi["spatial"]["placements"]))
		self.assertEqual(8, sum("bayonet.gi0" in point["id"] for point in gi["spatial"]["placements"]))

	def test_pro_gi_and_display_are_runtime_validated(self) -> None:
		gi = next(item for item in self.pro["outputs"] if item["binding"]["group"] == "pinmame.output.gi")
		self.assertEqual(0, gi["binding"]["device"])
		self.assertIn({"namespace": "pinmame.gi", "value": "0"}, gi["aliases"])
		self.assertEqual([128, 32], [self.pro["displays"][0]["width"], self.pro["displays"][0]["height"]])
		self.assertIn("runtime.mustang-pro.boot-start", self.pro["displays"][0]["provenance"]["source_refs"])

	def test_pro_mechanisms_capture_complete_recreation_behavior(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		self.assertEqual({"mechanism.trough", "mechanism.auto-launcher", "mechanism.right-scoop", "mechanism.captive-ball", "mechanism.center-drop-bank", "mechanism.mid-ramp", "mechanism.upper-ramp", "mechanism.orbit-post", "mechanism.bowl", "mechanism.pop-bumpers", "mechanism.slingshots", "mechanism.flippers", "mechanism.spinner"}, set(mechanisms))
		self.assertIn("23,22,21,20,19,18", mechanisms["mechanism.trough"]["behavior"])
		self.assertIn("185 degrees", mechanisms["mechanism.right-scoop"]["behavior"])
		self.assertIn("one physical UP POST assembly", mechanisms["mechanism.orbit-post"]["behavior"])
		self.assertTrue(all(item["provenance"]["status"] == "validated" for item in mechanisms.values()))

	def test_bindings_are_unique_within_each_controller_group(self) -> None:
		for definition in (self.premium, self.pro):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings), len(set(bindings)))

	def test_exact_rom_evidence_is_hash_anchored(self) -> None:
		rom = next(source for source in self.premium["sources"] if source["kind"] == "rom_static_analysis")
		self.assertEqual("4d26f0cca37435800ea84fa6687e0d6be006437194db36d9087e0e8bcdb9cf25", rom["sha256"])
		self.assertIn("CRC32 20ec78b3", rom["locator"])
		premium_table = next(source for source in self.premium["sources"] if source["id"] == "vpx-table.mustang-premium-le-vpw-1.27-geometry")
		self.assertEqual("f3f5e24665cf8bc0231f16e9cb28eed7c2cc1ff265d9c7e3cf93bf8589fe59e1", premium_table["sha256"])
		pro_script = next(source for source in self.pro["sources"] if source["id"] == "vpx.mustang-pro-85vett-gtxjoe-1.0")
		pro_table = next(source for source in self.pro["sources"] if source["id"] == "vpx-table.mustang-pro-85vett-gtxjoe-1.0")
		pro_runtime = next(source for source in self.pro["sources"] if source["id"] == "runtime.mustang-pro.boot-start")
		self.assertEqual("4ddf63df5b96e20da501ae336948e877473d21a4eeaf118a58bb7fcba9105a00", pro_script["sha256"])
		self.assertEqual("3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c", pro_table["sha256"])
		self.assertTrue(pro_table["known_working"])
		self.assertIn("All 5,311 GameItem streams and the embedded script are byte-identical", pro_table["locator"])
		self.assertEqual("c5002a38d3a392aec6e0160e1cd7988917e38e6118e375ef8e7f03e8d9b7bfe2", pro_runtime["sha256"])
		self.assertTrue((REPOSITORY_ROOT / "evidence" / "runtime" / "sam" / "mustang-pro-boot-start.json").is_file())

	def test_base_generator_has_no_import_time_writes(self) -> None:
		source = (REPOSITORY_ROOT / "tools" / "curate_mustang.py").read_text(encoding="utf-8")
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

	def test_base_generator_does_not_clobber_promoted_pro_artifacts(self) -> None:
		spec = importlib.util.spec_from_file_location("curate_mustang_no_clobber_test", REPOSITORY_ROOT / "tools" / "curate_mustang.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		with tempfile.TemporaryDirectory() as temporary:
			module.ROOT = Path(temporary)
			knowledge_path = module.ROOT / "knowledge" / "stern" / "mustang-pro-2014.md"
			knowledge_path.parent.mkdir(parents=True)
			knowledge_path.write_text("promoted spatial knowledge\n", encoding="utf-8")
			module.main()
			self.assertEqual("promoted spatial knowledge\n", knowledge_path.read_text(encoding="utf-8"))
			self.assertFalse((module.ROOT / "machines" / "partial" / "stern" / "mustang-pro-2014.json").exists())


if __name__ == "__main__":
	unittest.main()
