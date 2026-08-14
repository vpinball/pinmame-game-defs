from __future__ import annotations

import json
import ast
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "twenty-four-2009.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "twenty-four-boot-start-and-diagnostics.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class TwentyFourDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_identity_and_coverage_remain_conspicuous_partial(self) -> None:
		self.assertEqual({"id": "stern.twenty-four.2009", "ipdb_id": 5419, "kind": "physical_pinball", "manufacturer": "Stern", "name": "24", "opdb_id": "GrEkZ-ML13O", "year": 2009}, self.definition["machine"])
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual({"input_semantics", "output_semantics", "mechanism_behavior", "recreation_notes", "spatial_placement", "unresolved_conflicts"}, set(self.definition["coverage"]["missing"]))
		self.assertEqual("observed", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual("partial", self.definition["knowledge"]["status"])
		self.assertEqual({"conflict.suitcase-stepper-phase-order", "conflict.playfield-contact-construction", "conflict.hidden-trough-seats", "conflict.lamp-face-and-q27-naming"}, {conflict["id"] for conflict in self.definition["conflicts"]})
		self.assertFalse((ROOT / "machines" / "author-ready" / "stern" / "twenty-four-2009.json").exists())
		self.assertFalse((ROOT / "machines" / "stubs" / "twenty4_150.json").exists())

	def test_partial_status_names_every_authoring_blocker_without_author_ready_claim(self) -> None:
		knowledge = (ROOT / "knowledge" / "stern" / "twenty-four-2009.md").read_text(encoding="utf-8")
		self.assertIn("Coverage: **partial -", knowledge)
		self.assertNotIn("Coverage: **author-ready", knowledge)
		for phrase in ("phase causality is incomplete", "Contact construction and normal-state coverage is incomplete", "ordered shared-assembly projection", "Lamp addresses 72-78"):
			self.assertIn(phrase, knowledge)
		for conflict in self.definition["conflicts"]:
			self.assertGreaterEqual(len(conflict["source_refs"]), 2)

	def test_driver_family_is_exhaustive_and_one_physical_product(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual({"twenty4_130", "twenty4_140", "twenty4_144", "twenty4_150"}, set(drivers))
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in drivers.values()))
		self.assertTrue(all("February 2009 physical product" in driver["variant_notes"] for driver in drivers.values()))
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(set(drivers), {driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("twenty4_")})

	def test_complete_matrix_dedicated_and_dip_spaces_are_explicit(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		expected = set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1))
		self.assertEqual(expected, set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in (12, 17, 35, 36, 37, 38, 42, 47, 49, 50, 51, 52, 53, 59, 63, 64):
			self.assertEqual("unused", switches[address]["availability"])
		self.assertEqual("Tournament Start", switches[15]["label"])
		self.assertIn("never create a trough sensor", switches[15]["physical"]["notes"])
		self.assertTrue(switches[83]["normally_closed"])
		self.assertTrue(switches[81]["normally_closed"])
		self.assertTrue(switches[-6]["normally_closed"])
		for address in set(range(1, 65)) - {15, 16}:
			self.assertEqual("unknown", switches[address]["physical"]["switch_type"])
			if switches[address]["availability"] == "used":
				self.assertIn("exact factory contact construction is not established", switches[address]["physical"]["notes"])

	def test_switch_semantics_and_pulse_state_match_proven_script(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		expected_labels = {3: "Safe House eject", 10: "Left-loop spinner", 14: "Left control gate", 18: "Trough 4 left", 23: "Shooter lane", 43: "Suitcase lock bottom", 48: "Suitcase home", 54: "Right orbit", 58: "Right ramp entrance", 60: "Single drop target left", 61: "Single drop target right", 62: "Sniper target"}
		for address, label in expected_labels.items():
			self.assertEqual(label, switches[address]["label"])
		for address in (1, 2, 4, 5, 6, 7, 8, 9, 10, 26, 27, 30, 31, 32, 33, 34, 39, 40, 41, 54, 58, 62):
			self.assertTrue(switches[address]["pulse"], f"switch {address} is a proven pulse trigger")
		for address in (3, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 43, 44, 45, 46, 48, 55, 56, 57, 60, 61):
			self.assertFalse(switches[address]["pulse"], f"switch {address} must retain sustained state")

	def test_q_outputs_game_on_and_no_aux_capacity_are_complete(self) -> None:
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(outputs))
		self.assertEqual(("virtual", "used"), (outputs[33]["kind"], outputs[33]["availability"]))
		for address in range(51, 67):
			self.assertEqual(("virtual", "unused"), (outputs[address]["kind"], outputs[address]["availability"]))
		self.assertEqual("optional", outputs[8]["availability"])
		self.assertEqual((16, "ac"), (outputs[8]["wiring"]["nominal_voltage_v"], outputs[8]["wiring"]["voltage_type"]))
		self.assertEqual("optional", outputs[24]["availability"])
		for address in (21, 23, 25, 30):
			self.assertEqual(f"Suitcase stepper drive Q{address}", outputs[address]["label"])
			self.assertEqual((24, "dc"), (outputs[address]["wiring"]["nominal_voltage_v"], outputs[address]["wiring"]["voltage_type"]))
			self.assertEqual("511-5072-00", outputs[address]["physical"]["part_number"])
			self.assertNotIn("power_wire", outputs[address]["wiring"])
			self.assertIn("without assigning A/B/C/D", outputs[address]["physical"]["notes"])
		for address in (17, 18, 22, 29):
			self.assertEqual(("BRN", "J7-P1"), (outputs[address]["wiring"]["power_wire"], outputs[address]["wiring"]["power_connection"]))
		for address in (19, 20, 26, 27, 28, 31, 32):
			self.assertEqual(("ORG", "J6-P10"), (outputs[address]["wiring"]["power_wire"], outputs[address]["wiring"]["power_connection"]))

	def test_lamp_matrix_gi_and_display_are_exhaustive(self) -> None:
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertEqual({9}, {address for address, lamp in lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("Not used", lamps[9]["label"])
		self.assertNotIn("location", lamps[9]["physical"])
		self.assertNotIn("incandescent", lamps[9]["physical"]["notes"])
		self.assertEqual("J13-P9", lamps[1]["wiring"]["drive_connection"])
		self.assertEqual("J12-P11", lamps[80]["wiring"]["return_connection"])
		self.assertIn("without claiming an unverified face order", lamps[72]["physical"]["notes"])
		self.assertIn("without claiming an unverified face order", lamps[76]["physical"]["notes"])
		self.assertEqual({0}, set(bindings(self.definition, "outputs", "pinmame.output.gi")))
		self.assertEqual([{"height": 32, "id": "display.dmd", "kind": "dmd", "label": "Dot-matrix display", "provenance": self.definition["displays"][0]["provenance"], "spatial": self.definition["displays"][0]["spatial"], "width": 128}], self.definition["displays"])

	def test_spatial_inventory_is_explicit_and_preserves_derived_geometry(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			self.assertIn("spatial", device)
			self.assertIn(device["spatial"]["status"], {"candidate", "observed", "validated", "not_applicable"})
		inputs = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertEqual("observed", inputs[48]["spatial"]["status"])
		self.assertIn("shared-assembly projection", inputs[48]["physical"]["notes"])
		self.assertEqual(1, len(inputs[18]["spatial"]["placements"]))
		self.assertEqual(5, len({inputs[address]["spatial"]["placements"][0]["x"] for address in range(18, 23)}))
		self.assertIn("trough-region projection", inputs[22]["physical"]["notes"])
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual(3, outputs[19]["physical"]["quantity"])
		self.assertEqual(2, outputs[31]["physical"]["quantity"])
		self.assertEqual(outputs[21]["spatial"]["placements"][0]["x"], outputs[30]["spatial"]["placements"][0]["x"])
		self.assertEqual(22, bindings(self.definition, "outputs", "pinmame.output.gi")[0]["physical"]["quantity"])
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertEqual("not_applicable", lamps[1]["spatial"]["status"])
		self.assertEqual("not_applicable", lamps[9]["spatial"]["status"])
		self.assertEqual("validated", lamps[80]["spatial"]["status"])

	def test_custom_mechanisms_capture_physical_causality(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertIn("physical Tournament Start switch 15", mechanisms["mechanism.trough"]["behavior"])
		suitcase = mechanisms["mechanism.suitcase"]
		self.assertEqual(["device.21-suitcase-stepper-drive-q21", "device.23-suitcase-stepper-drive-q23", "device.25-suitcase-stepper-drive-q25", "device.30-suitcase-stepper-drive-q30", "device.28-suitcase-lock-and-release-post"], suitcase["actuators"])
		self.assertEqual(4, len(suitcase["sensors"]))
		self.assertEqual("511-5092-00", suitcase["assembly_part_number"])
		self.assertIn("bottom physical 43 to ROM 45", suitcase["behavior"])
		self.assertIn("Q21 alone as the logical VPX animation trigger", suitcase["behavior"])
		self.assertIn("A/B/C/D electrical order is not established", suitcase["behavior"])
		self.assertIn("moving collision geometry", mechanisms["mechanism.safe-house"]["behavior"])
		self.assertIn("waggles", mechanisms["mechanism.sniper-house"]["behavior"])
		self.assertIn("latch down", mechanisms["mechanism.single-drop-targets"]["behavior"])
		actuators = [actuator for mechanism in mechanisms.values() for actuator in mechanism["actuators"]]
		self.assertEqual(len(actuators), len(set(actuators)))

	def test_sources_pin_exact_manual_script_rom_and_runtime_evidence(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual("c547202e54b3ffbe53ba955db9eed8d52a6fef4b4807416de2f31ccf18aaf71f", sources["manual.stern-24-parts.2009"]["sha256"])
		self.assertIn("not a complete service I/O chart", sources["manual.stern-24-parts.2009"]["locator"])
		self.assertEqual("20f04adaba96926b74aa91dba7f88024a70012eb601242d18dfb15ed3da1f990", sources["manual.stern-sam-io-reference.2014"]["sha256"])
		self.assertIn("not evidence for any 24 game semantic", sources["manual.stern-sam-io-reference.2014"]["locator"])
		self.assertEqual("7bf550806bd87c17417a974ed75b1700885da883e0dce5ce31d7dc7ba6cc094f", sources["vpx.stern-24-2.3.1"]["sha256"])
		self.assertEqual("7e8bf294f3b3dd4bfe53e2727957d000568bc9d079caeed60038ceeb8d1b89f5", sources["vpx-table.stern-24-2009-local"]["sha256"])
		self.assertEqual("be3a0e0e96df6d232fa1fa99110e63781abdca5484a1b97de75de0fd1760135a", sources["vpx.stern-24-embedded-2.0.1"]["sha256"])
		self.assertNotIn("L:\\Visual Pinball\\Tables", sources["vpx-table.stern-24-2009-local"]["locator"])
		self.assertEqual("f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4", sources["rom.stern-24.twenty4-150"]["sha256"])
		self.assertIn("6678046c447b92a5965747a40035a13e312cc5f436ab13f0585267f65635ae17", sources["rom.stern-24.twenty4-150"]["locator"])
		self.assertEqual("a1fca511fbebd25e045af4e22e08505820e633c9be493808572b7245c85886db", sources["runtime.stern-24.boot-start"]["sha256"])
		self.assertEqual("d771050fab8d52590383899ca8f11ab8c59886730de25e1be07021ad76261b14", sources["runtime.stern-24-switch-diagnostic-1-17"]["sha256"])
		self.assertEqual("7f51c62f83f6933de08379fc7c65ed8bd6193c8ae474a972bdaf588fb282ad0d", sources["runtime.stern-24-switch-diagnostic-22-64"]["sha256"])
		self.assertEqual("b37e8977dd1fb91cc27cae31ce995ff3cd825a7dfb9ceca9a5589f93be3fdcf0", sources["runtime.stern-24-coil-diagnostic"]["sha256"])
		self.assertIn("High-side feed color is machine-harness evidence", sources["runtime.stern-24-coil-diagnostic"]["locator"])
		self.assertEqual("a3a6d5277e56c833445a3fc3a69d774f3b1d494f4df6aea99bc858670a25f286", sources["runtime.stern-24-lamp-diagnostic"]["sha256"])
		self.assertEqual("6d48aa7e63bd39eb339732888669768b1dcf584a1d51821b6d7a346ca809ea9b", sources["runtime.stern-24-suitcase-motor-menu"]["sha256"])
		self.assertIn("validates the separate test's existence only", sources["runtime.stern-24-suitcase-motor-menu"]["locator"])
		self.assertIn("registers only SolCallback(21)", sources["vpx.stern-24-2.3.1"]["locator"])

	def test_runtime_evidence_records_boot_diagnostics_and_held_capture(self) -> None:
		self.assertEqual(["stern.twenty-four.2009"], self.evidence["machine_ids"])
		self.assertEqual(["twenty4_150"], self.evidence["driver_ids"])
		runtime = self.evidence["runtime"]
		self.assertEqual("f6ea60175911fe259f45d7d10bc792c2f3e6f2b06583b5311d62cccb76f5a1b4", runtime["rom_archive_sha256"])
		self.assertIn("--snapshot-while-held", runtime["command_template"])
		self.assertEqual([21, 23, 25, 30], runtime["observations"]["public_solenoid_decoder_holes_not_seen"])
		self.assertNotIn("named_output_addresses", runtime["observations"])
		self.assertEqual(set(range(1, 81)), set(runtime["observations"]["lamp_addresses_seen"]))
		self.assertEqual(6, runtime["command_template"].count("--pulse 65:300"))
		self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])

	def test_ids_and_bindings_are_unique(self) -> None:
		for collection in (self.definition["inputs"], self.definition["outputs"]):
			ids = [item["id"] for item in collection]
			self.assertEqual(len(ids), len(set(ids)))
			controller_bindings = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
			self.assertEqual(len(controller_bindings), len(set(controller_bindings)))

	def test_curators_are_import_pure_and_base_preserves_reviewed_partial(self) -> None:
		for filename in ("curate_twenty_four.py", "curate_twenty_four_spatial.py"):
			tree = ast.parse((ROOT / "tools" / filename).read_text(encoding="utf-8"))
			mutating_calls = []
			for statement in tree.body:
				if isinstance(statement, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
					continue
				if isinstance(statement, ast.If) and isinstance(statement.test, ast.Compare) and isinstance(statement.test.left, ast.Name) and statement.test.left.id == "__name__":
					continue
				for node in ast.walk(statement):
					if isinstance(node, ast.Call):
						name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
						if name in {"write", "write_json", "write_text", "unlink"}:
							mutating_calls.append(name)
			self.assertEqual([], mutating_calls, filename)
		spec = importlib.util.spec_from_file_location("curate_twenty_four_no_clobber_test", ROOT / "tools" / "curate_twenty_four.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		sys.modules["curate_twenty_four"] = module
		with tempfile.TemporaryDirectory() as temporary:
			module.ROOT = Path(temporary)
			definition_path = module.ROOT / "machines" / "partial" / "stern" / "twenty-four-2009.json"
			definition_path.parent.mkdir(parents=True)
			definition_path.write_text('{"reviewed": true}\n', encoding="utf-8")
			module.main()
			self.assertEqual('{"reviewed": true}\n', definition_path.read_text(encoding="utf-8"))
			self.assertFalse((module.ROOT / "machines" / "author-ready" / "stern" / "twenty-four-2009.json").exists())
			evidence_path = module.ROOT / "evidence" / "runtime" / "sam" / "twenty-four-boot-start-and-diagnostics.json"
			first_evidence = evidence_path.read_bytes()
			module.main()
			self.assertEqual(first_evidence, evidence_path.read_bytes())

		spec = importlib.util.spec_from_file_location("curate_twenty_four_spatial_determinism_test", ROOT / "tools" / "curate_twenty_four_spatial.py")
		self.assertIsNotNone(spec)
		self.assertIsNotNone(spec.loader)
		spatial_module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(spatial_module)
		with tempfile.TemporaryDirectory() as temporary:
			spatial_module.ROOT = Path(temporary)
			spatial_module.PARTIAL_PATH = spatial_module.ROOT / "machines" / "partial" / "stern" / "twenty-four-2009.json"
			spatial_module.AUTHOR_READY_PATH = spatial_module.ROOT / "machines" / "author-ready" / "stern" / "twenty-four-2009.json"
			spatial_module.KNOWLEDGE_PATH = spatial_module.ROOT / "knowledge" / "stern" / "twenty-four-2009.md"
			spatial_module.demote()
			first_definition = spatial_module.PARTIAL_PATH.read_bytes()
			spatial_module.demote()
			self.assertEqual(first_definition, spatial_module.PARTIAL_PATH.read_bytes())
			self.assertFalse(spatial_module.AUTHOR_READY_PATH.exists())

		with tempfile.TemporaryDirectory() as temporary:
			spatial_module.ROOT = Path(temporary)
			spatial_module.PARTIAL_PATH = spatial_module.ROOT / "machines" / "partial" / "stern" / "twenty-four-2009.json"
			spatial_module.AUTHOR_READY_PATH = spatial_module.ROOT / "machines" / "author-ready" / "stern" / "twenty-four-2009.json"
			spatial_module.KNOWLEDGE_PATH = spatial_module.ROOT / "knowledge" / "stern" / "twenty-four-2009.md"
			spatial_module.PARTIAL_PATH.parent.mkdir(parents=True)
			spatial_module.PARTIAL_PATH.write_bytes(b"reviewed partial\n")
			with self.assertRaisesRegex(FileExistsError, "reviewed partial"):
				spatial_module.demote()
			self.assertEqual(b"reviewed partial\n", spatial_module.PARTIAL_PATH.read_bytes())
			self.assertFalse(spatial_module.KNOWLEDGE_PATH.exists())

		with tempfile.TemporaryDirectory() as temporary:
			spatial_module.ROOT = Path(temporary)
			spatial_module.PARTIAL_PATH = spatial_module.ROOT / "machines" / "partial" / "stern" / "twenty-four-2009.json"
			spatial_module.AUTHOR_READY_PATH = spatial_module.ROOT / "machines" / "author-ready" / "stern" / "twenty-four-2009.json"
			spatial_module.KNOWLEDGE_PATH = spatial_module.ROOT / "knowledge" / "stern" / "twenty-four-2009.md"
			spatial_module.AUTHOR_READY_PATH.parent.mkdir(parents=True)
			spatial_module.AUTHOR_READY_PATH.write_bytes(b"reviewed author-ready\n")
			with self.assertRaisesRegex(FileExistsError, "author-ready"):
				spatial_module.demote()
			self.assertEqual(b"reviewed author-ready\n", spatial_module.AUTHOR_READY_PATH.read_bytes())
			self.assertFalse(spatial_module.PARTIAL_PATH.exists())
			self.assertFalse(spatial_module.KNOWLEDGE_PATH.exists())


if __name__ == "__main__":
	unittest.main()
