from __future__ import annotations

import ast
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = ROOT / "machines" / "author-ready" / "stern" / "star-trek-premium-limited-edition-2013.json"
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "star-trek-pro-2013.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "star-trek-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class StarTrekDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.premium = load_json(PREMIUM_PATH)
		cls.pro = load_json(PRO_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_premium_is_author_ready_while_pro_remains_fail_closed(self) -> None:
		self.assertEqual(2, self.premium["schema_version"])
		self.assertEqual("physical_pinball", self.premium["machine"]["kind"])
		self.assertEqual("author_ready", self.premium["coverage"]["status"])
		self.assertEqual([], self.premium["coverage"]["missing"])
		self.assertEqual("validated", self.premium["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		self.assertEqual("complete", self.pro["knowledge"]["status"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "star-trek-premium-limited-edition-2013.json").exists())
		self.assertTrue((ROOT / "machines" / "partial" / "stern" / "star-trek-pro-2013.json").exists())

	def test_editions_split_the_complete_driver_family(self) -> None:
		premium = {driver["id"] for driver in self.premium["drivers"]}
		pro = {driver["id"] for driver in self.pro["drivers"]}
		self.assertEqual({"st_140h", "st_141h", "st_142h", "st_150h", "st_160h", "st_161h", "st_161hc", "st_162h", "st_162hc"}, premium)
		self.assertEqual({"st_120", "st_130", "st_140", "st_150", "st_160", "st_161", "st_161c", "st_162", "st_162c"}, pro)
		self.assertFalse(premium & pro)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("st_")}, premium | pro)
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.premium["drivers"]))
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.pro["drivers"]))

	def test_switch_matrix_names_and_dedicated_bindings_match_the_physical_machine(self) -> None:
		for definition in (self.premium, self.pro):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertEqual("Left pop bumper", switches[30]["label"])
			self.assertEqual("Bottom pop bumper", switches[32]["label"])
			self.assertEqual("Center 3-bank top", switches[39]["label"])
			self.assertEqual("Center 3-bank bottom", switches[41]["label"])
			self.assertEqual("Left 2-bank top", switches[42]["label"])
			self.assertEqual("Left 2-bank bottom", switches[43]["label"])
			self.assertEqual("Upper-right flipper button", switches[86]["label"])
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
		pro_switches = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual("unused", pro_switches[53]["availability"])
		self.assertEqual("Vengeance crash opto", bindings(self.premium, "inputs", "pinmame.input.switch")[53]["label"])

	def test_trough_has_four_positions_and_a_downstream_jam_opto(self) -> None:
		by_address = bindings(self.pro, "inputs", "pinmame.input.switch")
		self.assertEqual(["microswitch"] * 4, [by_address[number]["physical"]["switch_type"] for number in range(18, 22)])
		self.assertEqual("opto", by_address[22]["physical"]["switch_type"])
		trough = next(item for item in self.pro["mechanisms"] if item["id"] == "mechanism.trough")
		self.assertEqual(5, len(trough["sensors"]))
		self.assertIn("18-21", trough["behavior"])

	def test_pro_has_only_the_32_main_outputs(self) -> None:
		solenoids = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(solenoids))
		self.assertEqual("virtual", solenoids[33]["kind"])
		self.assertNotIn("wiring", solenoids[33])
		self.assertEqual("Center lock magnet", solenoids[3]["label"])
		self.assertEqual("Upper-right flipper", solenoids[12]["label"])
		self.assertEqual("optional", solenoids[8]["availability"])
		self.assertEqual("optional", solenoids[24]["availability"])
		self.assertFalse(set(range(51, 67)) & set(solenoids))

	def test_premium_auxiliary_board_uses_pinmame_public_compatibility_addresses(self) -> None:
		by_address = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		self.assertEqual("Q51", by_address[51]["wiring"]["driver_transistor"])
		self.assertEqual("Q41", by_address[59]["wiring"]["driver_transistor"])
		self.assertEqual("YEL-ORG", by_address[53]["wiring"]["control_wire"])
		self.assertEqual("unused", by_address[57]["availability"])
		self.assertEqual("unused", by_address[66]["availability"])

	def test_pro_standard_lamp_matrix_is_complete_and_physical(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual({1, 2, 6, 31, 39, 47, 58, 77, 78, 79}, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("Fire button", lamps[3]["label"])
		self.assertEqual("Black hole arrow", lamps[61]["label"])
		self.assertEqual("Right-side blue playfield spotlight", lamps[80]["label"])
		self.assertEqual({0}, set(bindings(self.pro, "outputs", "pinmame.output.gi")))

	def test_pro_rgb_insert_channels_preserve_color_and_position(self) -> None:
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		expected = {
			25: "Left orbit emblem red", 33: "Left orbit emblem green", 41: "Left orbit emblem blue",
			26: "Left ramp emblem red", 34: "Left ramp emblem green", 42: "Left ramp emblem blue",
			29: "Left eject emblem red", 37: "Left eject emblem green", 45: "Left eject emblem blue",
			30: "Center lane emblem red", 38: "Center lane emblem green", 46: "Center lane emblem blue",
			28: "Right ramp emblem red", 36: "Right ramp emblem green", 44: "Right ramp emblem blue",
			27: "Right orbit emblem red", 35: "Right orbit emblem green", 43: "Right orbit emblem blue",
		}
		self.assertEqual(expected, {address: lamps[address]["label"] for address in expected})
		self.assertTrue(all(lamps[address]["kind"] == "rgb_lamp" for address in expected))
		self.assertIn("x=200.0, y=1502.0", lamps[25]["physical"]["location"])

	def test_pro_mechanisms_are_complete_and_exclude_premium_hardware(self) -> None:
		mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		expected = {"mechanism.trough", "mechanism.auto-launcher", "mechanism.left-eject", "mechanism.center-drop-target", "mechanism.center-lock", "mechanism.vengeance", "mechanism.flippers", "mechanism.pop-bumpers", "mechanism.slingshots", "mechanism.spinner", "mechanism.beam-target-bank", "mechanism.trek-target-bank", "mechanism.right-target-bank", "mechanism.center-target-bank", "mechanism.left-target-bank", "mechanism.red-targets", "mechanism.ramps-and-orbits", "mechanism.laser", "mechanism.optional-shaker"}
		self.assertEqual(expected, set(mechanisms))
		self.assertEqual(["device.vengeance-super-speed-kickback"], mechanisms["mechanism.vengeance"]["actuators"])
		self.assertIn("passive bash", mechanisms["mechanism.vengeance"]["behavior"])
		self.assertIn("switch 90", mechanisms["mechanism.flippers"]["behavior"])
		all_actuators = {actuator for item in mechanisms.values() for actuator in item["actuators"]}
		self.assertFalse({"device.vengeance-ship-actuator", "device.vengeance-ship-latch", "device.rotating-vuk", "device.bottom-drain-kickback"} & all_actuators)

	def test_premium_custom_mechanisms_use_corrected_switch_names(self) -> None:
		by_id = {item["id"]: item for item in self.premium["mechanisms"]}
		self.assertEqual(["switch.center-lock-bottom", "switch.center-lock-top"], by_id["mechanism.center-lock"]["sensors"])
		self.assertIn("device.rotating-vuk", by_id["mechanism.left-eject"]["actuators"])
		self.assertIn("100 Hz", by_id["mechanism.vengeance"]["behavior"])

	def test_premium_spatial_inventory_is_complete_and_keeps_nonplayfield_devices_outside_playfield_space(self) -> None:
		devices = [*self.premium["inputs"], *self.premium["outputs"]]
		self.assertTrue(all(device["spatial"]["status"] in {"validated", "not_applicable"} for device in devices))
		inputs = bindings(self.premium, "inputs", "pinmame.input.switch")
		self.assertEqual((0.578782, 0.138478), tuple(inputs[1]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.516282, 0.312283), tuple(inputs[11]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.242986, 0.774518), tuple(inputs[26]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.682742, 0.775298), tuple(inputs[27]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.500865, 0.237365), tuple(inputs[53]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (15, 16, 65, 66, 67, 68, 71, 82, 84, 86):
			self.assertEqual(("not_applicable", "cabinet_or_service"), (inputs[address]["spatial"]["status"], inputs[address]["spatial"]["reason"]))
		solenoids = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		for address, expected in {1: (0.849790, 0.906658), 2: (0.938813, 0.911467), 3: (0.498950, 0.261848), 13: (0.242986, 0.774518), 14: (0.682742, 0.775298), 19: (0.033892, 0.112326), 20: (0.756171, 0.117120), 31: (0.502101, 0.247048), 54: (0.074562, 0.880015), 55: (0.103108, 0.480360)}.items():
			self.assertEqual(expected, tuple(solenoids[address]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.500865, 0.237365), tuple(solenoids[53]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.500865, 0.237365), tuple(solenoids[56]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address, quantity in {60: 2, 61: 2, 62: 1, 63: 1, 64: 1}.items():
			self.assertEqual(quantity, solenoids[address]["physical"]["quantity"])
			self.assertEqual(("not_applicable", "cabinet_or_service"), (solenoids[address]["spatial"]["status"], solenoids[address]["spatial"]["reason"]))

	def test_premium_lamp_geometry_preserves_physical_multiplicity_and_rgb_colocation(self) -> None:
		lamps = [item for item in self.premium["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"]
		by_physical: dict[int, list[dict[str, object]]] = {}
		for lamp in lamps:
			manual_addresses = [alias["value"] for alias in lamp["aliases"] if alias["namespace"] == "manual.address"]
			if not manual_addresses:
				continue
			physical_number = int(manual_addresses[0])
			by_physical.setdefault(physical_number, []).append(lamp)
		for physical_number in range(1, 65):
			placement_sets = {
				tuple((placement["x"], placement["y"]) for placement in lamp["spatial"]["placements"])
				for lamp in by_physical[physical_number]
			}
			self.assertEqual(1, len(placement_sets))
		for physical_number in (51, 57, 63, 64, 78, *range(79, 101)):
			self.assertTrue(all(lamp["physical"]["quantity"] == 2 for lamp in by_physical[physical_number]))
		for physical_number in (51, 63, 64):
			self.assertTrue(all(len(lamp["spatial"]["placements"]) == 1 for lamp in by_physical[physical_number]))
		self.assertTrue(all(len(lamp["spatial"]["placements"]) == 2 for lamp in by_physical[57]))
		for physical_number in range(70, 78):
			self.assertTrue(all(lamp["physical"]["quantity"] == 1 and len(lamp["spatial"]["placements"]) == 1 for lamp in by_physical[physical_number]))
		self.assertTrue(all(tuple(lamp["spatial"]["placements"][0][axis] for axis in ("x", "y")) == (0.104114, 0.296557) for lamp in by_physical[70]))
		for physical_number in (65, 66, 67, 68, 69, 78, *range(79, 101)):
			self.assertTrue(all(lamp["spatial"]["status"] == "not_applicable" and lamp["spatial"]["reason"] == "cabinet_or_service" for lamp in by_physical[physical_number]))

	def test_premium_gi_has_all_physical_emitters_without_putting_backbox_fixtures_in_playfield_space(self) -> None:
		gi = next(item for item in self.premium["outputs"] if item["binding"] == {"group": "pinmame.output.gi", "device": 0})
		placements = gi["spatial"]["placements"]
		self.assertEqual((41, 34), (gi["physical"]["quantity"], len(placements)))
		self.assertEqual(31, sum(".socket-" in placement["id"] for placement in placements))
		self.assertEqual(3, sum(".pop." in placement["id"] for placement in placements))
		self.assertFalse(any(".gi0" in placement["id"] or ".gi1" in placement["id"] or ".gi3" in placement["id"] for placement in placements))
		self.assertFalse(any(".backbox-" in placement["id"] for placement in placements))
		self.assertIn("27 wedge-base sockets, four bayonet sockets, and three illuminated pop-bumper assemblies", gi["physical"]["notes"])
		self.assertIn("seven backbox fixtures are inventoried here but intentionally have no playfield-space placement", gi["physical"]["notes"])
		self.assertFalse(any(token in placement["id"] for placement in placements for token in ("Laser", "ambient", "bloom")))

	def test_premium_spatial_provenance_and_registered_geometry_use_one_canonical_frame(self) -> None:
		manual = "manual.star-trek-premium-le"
		script = "vpx.star-trek-le-1.10"
		neo = "vpx-table.star-trek-le-neo-real-1.0.2-geometry"
		enterprise = "vpx-table.star-trek-enterprise-le-geometry"
		inputs = bindings(self.premium, "inputs", "pinmame.input.switch")
		self.assertEqual([manual, script, neo], inputs[23]["spatial"]["placements"][0]["provenance"]["source_refs"])
		for address in range(18, 22):
			self.assertEqual([manual, script, neo, enterprise], inputs[address]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual([manual, script, neo], inputs[22]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual((0.849790, 0.906658), tuple(inputs[22]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		solenoids = bindings(self.premium, "outputs", "pinmame.output.solenoid")
		self.assertEqual([manual], solenoids[22]["spatial"]["placements"][0]["provenance"]["source_refs"])
		self.assertEqual([manual, script, neo], solenoids[31]["spatial"]["placements"][0]["provenance"]["source_refs"])
		lamps = [item for item in self.premium["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"]
		by_number: dict[int, list[dict[str, object]]] = {}
		for lamp in lamps:
			for alias in lamp["aliases"]:
				if alias["namespace"] == "manual.address":
					by_number.setdefault(int(alias["value"]), []).append(lamp)
		for physical_number in (51, 56, 57):
			self.assertTrue(all(placement["provenance"]["source_refs"] == [manual, script, neo, enterprise] for lamp in by_number[physical_number] for placement in lamp["spatial"]["placements"]))
		expected_direct_points = {7: (0.589023, 0.393655), 21: (0.205095, 0.592894), 23: (0.142069, 0.652133), 37: (0.464548, 0.821889), 39: (0.517069, 0.779280), 41: (0.407826, 0.779280), 50: (0.172320, 0.182543), 52: (0.137099, 0.162618), 63: (0.143749, 0.888266), 64: (0.771201, 0.888266), 70: (0.104114, 0.296557), 77: (0.125825, 0.125684)}
		for physical_number, expected in expected_direct_points.items():
			self.assertTrue(all(placement["provenance"]["source_refs"] == [manual, script, neo] for lamp in by_number[physical_number] for placement in lamp["spatial"]["placements"]))
			self.assertTrue(all(tuple(lamp["spatial"]["placements"][0][axis] for axis in ("x", "y")) == expected for lamp in by_number[physical_number]))
		self.assertTrue(all(tuple(lamp["spatial"]["placements"][0][axis] for axis in ("x", "y")) == (0.897124, 0.517279) for lamp in by_number[51]))

	def test_premium_exact_geometry_sources_are_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.premium["sources"]}
		self.assertEqual("f7edee3cbcebff1a078496b7ef7dcef7368158a61b48934f2241792a70bc233c", sources["vpx-table.star-trek-le-neo-real-1.0.2-geometry"]["sha256"])
		self.assertEqual("46e4642ebcfcbedc59c3cf950b92ccc0dcc68818752110004c4164cb1d54cc8e", sources["vpx-table.star-trek-enterprise-le-geometry"]["sha256"])
		self.assertIn("exact st_161h table", sources["vpx-table.star-trek-le-neo-real-1.0.2-geometry"]["locator"])
		self.assertIn("exact st_161hc table", sources["vpx-table.star-trek-enterprise-le-geometry"]["locator"])

	def test_bindings_are_unique_within_each_controller_group(self) -> None:
		for definition in (self.premium, self.pro):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))

	def test_pro_sources_and_exact_rom_run_are_content_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("23cb9e6683d7b357ada48678a8e157a8b64102ea012821c350a3f033fae66b28", sources["manual.star-trek-pro"]["sha256"])
		self.assertEqual("abc5dbb6ead12f16886143a50cfd2534c9baf855b070924dd7d82e404b4d69bf", sources["vpx.star-trek-pro-fss"]["sha256"])
		self.assertEqual("2976e3313a6fa1ee6f26709d515661b81ade8f01894a847b907a5e608e5bb9e7", sources["vpx-table.star-trek-pro-fss"]["sha256"])
		runtime = self.evidence["runtime"]
		self.assertEqual("st_161c", runtime["game"])
		self.assertEqual("f42dc29347fa2d8f9e2abff7b1ec958507d73e4c658a946c2fd5f3d290b557c0", runtime["rom_archive_sha256"])
		self.assertEqual("a8404eca7535f40ade66f652a94b3923d3d46c7c23315a38d554e475170656e7", runtime["raw_runs"][0]["sha256"])
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])

	def test_base_generator_has_no_import_time_writes(self) -> None:
		source = (ROOT / "tools" / "curate_star_trek.py").read_text(encoding="utf-8")
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
		spec = importlib.util.spec_from_file_location("curate_star_trek_no_clobber_test", ROOT / "tools" / "curate_star_trek.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		with tempfile.TemporaryDirectory() as temporary:
			module.ROOT = Path(temporary)
			definition_path = module.ROOT / "machines" / "author-ready" / "stern" / "star-trek-premium-limited-edition-2013.json"
			definition_path.parent.mkdir(parents=True)
			definition_path.write_text('{"promoted": true}\n', encoding="utf-8")
			knowledge_path = module.ROOT / "knowledge" / "stern" / "star-trek-premium-limited-edition-2013.md"
			knowledge_path.parent.mkdir(parents=True)
			knowledge_path.write_text("promoted spatial knowledge\n", encoding="utf-8")
			module.main()
			self.assertEqual('{"promoted": true}\n', definition_path.read_text(encoding="utf-8"))
			self.assertEqual("promoted spatial knowledge\n", knowledge_path.read_text(encoding="utf-8"))
			self.assertFalse((module.ROOT / "machines" / "partial" / "stern" / "star-trek-premium-limited-edition-2013.json").exists())


if __name__ == "__main__":
	unittest.main()
