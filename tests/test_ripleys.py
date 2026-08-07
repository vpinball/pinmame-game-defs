from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "ripley-s-believe-it-or-not-2004.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "whitestar" / "ripleys-boot-start-and-gameplay.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "ripley-s-believe-it-or-not-2004.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "whitestar.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "ripley-s-believe-it-or-not-2004.md"
VPX_EVIDENCE_PATH = ROOT / "evidence" / "vpx" / "ripleys-exact-table-1.0.3.json"
SPATIAL_GENERATOR_PATH = ROOT / "tools" / "curate_ripleys_spatial.py"

_generator_spec = importlib.util.spec_from_file_location("curate_ripleys_spatial_test", SPATIAL_GENERATOR_PATH)
assert _generator_spec is not None and _generator_spec.loader is not None
SPATIAL_GENERATOR = importlib.util.module_from_spec(_generator_spec)
_generator_spec.loader.exec_module(SPATIAL_GENERATOR)


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def external_script_path() -> Path:
	root_value = os.environ.get(SPATIAL_GENERATOR.SCRIPT_ENV_VAR)
	if not root_value:
		raise unittest.SkipTest(f"{SPATIAL_GENERATOR.SCRIPT_ENV_VAR} is unset; retained-script integration tests skipped")
	path = Path(root_value).expanduser() / SPATIAL_GENERATOR.SCRIPT_RELATIVE_PATH
	if not path.is_file():
		raise unittest.SkipTest(f"retained Ripley's script unavailable at {path}; integration tests skipped")
	return path


def external_extraction_path() -> Path:
	root_value = os.environ.get(SPATIAL_GENERATOR.SCRIPT_ENV_VAR)
	if not root_value:
		raise unittest.SkipTest(f"{SPATIAL_GENERATOR.SCRIPT_ENV_VAR} is unset; retained-extraction integration tests skipped")
	path = Path(root_value).expanduser() / SPATIAL_GENERATOR.EXTRACTION_RELATIVE_PATH
	if not path.is_dir():
		raise unittest.SkipTest(f"retained Ripley's extraction unavailable at {path}; integration tests skipped")
	return path


class RipleyScriptResolverTests(unittest.TestCase):
	def test_resolver_requires_environment_fallback_when_path_is_omitted(self) -> None:
		with patch.dict(os.environ, {}, clear=False):
			os.environ.pop(SPATIAL_GENERATOR.SCRIPT_ENV_VAR, None)
			with self.assertRaisesRegex(RuntimeError, f"{SPATIAL_GENERATOR.SCRIPT_ENV_VAR} is unset"):
				SPATIAL_GENERATOR._resolve_script_path()

	def test_explicit_path_takes_precedence_over_environment_fallback(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			explicit_path = Path(temporary_directory) / "script.vbs"
			explicit_path.write_bytes(b"unit-test placeholder")
			with patch.dict(os.environ, {SPATIAL_GENERATOR.SCRIPT_ENV_VAR: str(Path(temporary_directory) / "missing")}, clear=False):
				self.assertEqual(explicit_path.resolve(), SPATIAL_GENERATOR._resolve_script_path(explicit_path))

	def test_resolver_reports_missing_and_wrong_type_paths(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			missing_path = Path(temporary_directory) / "missing-script.vbs"
			with self.assertRaisesRegex(FileNotFoundError, "does not exist"):
				SPATIAL_GENERATOR._resolve_script_path(missing_path)
			with self.assertRaisesRegex(ValueError, "regular file"):
				SPATIAL_GENERATOR._resolve_script_path(Path(temporary_directory))


class RipleysDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)
		cls.profile = load_json(PROFILE_PATH)
		cls.knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")

	def test_identity_driver_family_and_fail_closed_spatial_gate(self) -> None:
		self.assertEqual(
			{"id": "stern.ripley-s-believe-it-or-not.2004", "ipdb_id": 4917, "kind": "physical_pinball", "manufacturer": "Stern", "name": "Ripley's Believe It or Not!", "year": 2004},
			self.definition["machine"],
		)
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])
		self.assertEqual("unknown", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual({"conflict.ripleys.uk-table-scope", "conflict.ripleys-q24-script-revision"}, {conflict["id"] for conflict in self.definition["conflicts"]})
		expected = {f"rip{version}{language}" for version in ("300", "301", "302", "310") for language in ("", "f", "g", "i", "l")} | {f"ripleys{language}" for language in ("", "f", "g", "i", "l")}
		self.assertEqual(expected, {driver["id"] for driver in self.definition["drivers"]})
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(expected, {driver["id"] for driver in catalog["drivers"] if driver["root_driver"] == "ripleys"})
		self.assertTrue((ROOT / "machines" / "partial" / "stern" / "ripley-s-believe-it-or-not-2004.json").exists())

	def test_whitestar_profile_and_complete_input_spaces(self) -> None:
		self.assertEqual("pinmame.whitestar", self.profile["id"])
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		self.assertEqual(set(range(1, 65)) | set(range(-3, 1)) | set(range(81, 89)), set(switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual({10, 37, 63, 64, 85, 86, 87}, {address for address, switch in switches.items() if switch["availability"] == "unused"})
		self.assertTrue(switches[83]["normally_closed"])
		self.assertTrue(switches[81]["normally_closed"])
		self.assertEqual("Upper-right flipper button", switches[88]["label"])
		self.assertEqual("Coin-door memory protect", switches[-3]["label"])
		self.assertEqual(("180-5000-01", "500-5808-00", "CN6-P12"), (switches[-3]["physical"]["part_number"], switches[-3]["physical"]["assembly_part_number"], switches[-3]["wiring"]["drive_connection"]))
		self.assertEqual(["180-5192-02", "180-5192-04", "180-5192-00"], [switches[address]["physical"]["part_number"] for address in (-2, -1, 0)])
		self.assertTrue(all(not switches[address]["pulse"] for address in (-3, -2, -1, 0)))

	def test_switch_semantics_and_proven_script_contact_behavior(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		expected_pulses = {2, 3, 4, 5, 6, 7, 9, 15, 17, 19, 20, 21, 22, 25, 26, 27, 32, 49, 50, 51, 59, 62}
		self.assertEqual(expected_pulses, {address for address in range(1, 65) if switches[address]["availability"] != "unused" and switches[address]["pulse"]})
		self.assertEqual(["Four-ball trough 1 (left)", "Four-ball trough 2", "Four-ball trough 3", "Four-ball trough 4 / VUK opto", "Four-ball stacking opto"], [switches[address]["label"] for address in range(11, 16)])
		self.assertEqual(["Vari-target opto 1", "Vari-target opto 2", "Vari-target opto 3"], [switches[address]["label"] for address in range(41, 44)])
		self.assertEqual({-3, 11, 12, 13, 14, 42, 43}, {address for address, switch in switches.items() if switch.get("initial_active")})
		self.assertEqual("180-5190-28", switches[31]["physical"]["part_number"])
		self.assertNotIn("assembly_part_number", switches[31]["physical"])
		self.assertEqual("500-5190-28", switches[53]["physical"]["assembly_part_number"])
		self.assertNotIn("part_number", switches[53]["physical"])
		for address, expected in {
			1: ("GRN-BRN", "CN5-P1", "WHT-BRN", "CN7-P9"),
			8: ("GRN-BRN", "CN5-P1", "WHT-GRY", "CN7-P1"),
			9: ("GRN-RED", "CN5-P3", "WHT-BRN", "CN7-P9"),
			64: ("GRN-GRY", "CN5-P9", "WHT-GRY", "CN7-P1"),
		}.items():
			wiring = switches[address]["wiring"]
			self.assertEqual(expected, (wiring["drive_wire"], wiring["drive_connection"], wiring["return_wire"], wiring["return_connection"]))

	def test_physical_q_outputs_and_public_whitestar_remap_are_explicit(self) -> None:
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 51)), set(outputs))
		for address in list(range(1, 15)) + list(range(17, 33)):
			self.assertIn({"namespace": "manual.address", "value": f"Q{address}"}, outputs[address]["aliases"])
		self.assertEqual(("device.q14-upper-right-flipper", "Q14"), (outputs[14]["id"], outputs[14]["wiring"]["driver_transistor"]))
		self.assertEqual(("virtual", "used"), (outputs[15]["kind"], outputs[15]["availability"]))
		self.assertEqual(("virtual", "unused"), (outputs[16]["kind"], outputs[16]["availability"]))
		self.assertEqual(("device.q16-right-flipper", "Q16"), (outputs[46]["id"], outputs[46]["wiring"]["driver_transistor"]))
		self.assertEqual(("device.q15-left-flipper", "Q15"), (outputs[48]["id"], outputs[48]["wiring"]["driver_transistor"]))
		self.assertEqual({45, 47}, {address for address in (45, 46, 47, 48) if outputs[address]["kind"] == "virtual"})
		self.assertIn("power-phase compatibility", outputs[45]["label"])
		self.assertIn("power-phase compatibility", outputs[47]["label"])
		self.assertEqual({33, 34, 35}, {address for address, output in outputs.items() if output["availability"] == "optional" and address >= 33})
		self.assertEqual(set(range(36, 45)) | {49, 50}, {address for address, output in outputs.items() if address >= 33 and output["availability"] == "unused"})
		self.assertEqual("optional", outputs[24]["availability"])
		self.assertIn("deliberately comments out", outputs[24]["physical"]["notes"])

	def test_exact_uk_table_spatial_overlay_is_partial_and_multiplicity_safe(self) -> None:
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual("vpx-table.ripleys-jpsalas-1.0.3-uk", self.definition["sources"][2]["id"])
		self.assertEqual("6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48", self.definition["sources"][2]["sha256"])
		self.assertEqual(2, len(switches[32]["spatial"]["placements"]))
		self.assertEqual([(0.622044, 0.247893), (0.622044, 0.248008), (0.622044, 0.247893)], [(switches[address]["spatial"]["placements"][0]["x"], switches[address]["spatial"]["placements"][0]["y"]) for address in (41, 42, 43)])
		self.assertEqual(1, len(outputs[25]["spatial"]["placements"]))
		self.assertEqual(1, len(outputs[28]["spatial"]["placements"]))
		self.assertEqual(1, len(outputs[30]["spatial"]["placements"]))
		self.assertEqual(39, len(gi[0]["spatial"]["placements"]))
		self.assertNotIn("spatial", switches[11])
		self.assertNotIn("spatial", switches[44])
		self.assertNotIn("spatial", outputs[21])
		self.assertNotIn("spatial", outputs[33])
		self.assertNotIn("spatial", lamps[76])
		self.assertEqual("no_physical_device", outputs[24]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", lamps[80]["spatial"]["reason"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("UK model / All-Skill extra-post configuration", report["selected_source"]["edition"])
		self.assertGreaterEqual(len(report["unresolved_blockers"]), 7)
		self.assertEqual(self.definition["conflicts"], report["conflicts"])

	def test_spatial_placements_emit_exact_canonical_coordinates_without_generator_metadata(self) -> None:
		outputs = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		switches = bindings(self.definition, "inputs", "pinmame.input.switch")
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		for device in [*self.definition["inputs"], *self.definition["outputs"]]:
			for placement in device.get("spatial", {}).get("placements", []):
				self.assertNotIn("source_object", placement)
		self.assertEqual((0.371736, 0.156804), (switches[23]["spatial"]["placements"][0]["x"], switches[23]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.107415, 0.581115), (switches[24]["spatial"]["placements"][0]["x"], switches[24]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.193871, 0.443975), (outputs[25]["spatial"]["placements"][0]["x"], outputs[25]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.371927, 0.160119), (outputs[28]["spatial"]["placements"][0]["x"], outputs[28]["spatial"]["placements"][0]["y"]))
		self.assertEqual((0.765534, 0.164089), (outputs[30]["spatial"]["placements"][0]["x"], outputs[30]["spatial"]["placements"][0]["y"]))
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(SPATIAL_GENERATOR.EXTRACTION_MANIFEST_SHA256, report["selected_source"]["extraction_manifest_sha256"])
		audit = {(record.get("device_id"), record["name"]): record for record in report["object_audit"]}
		self.assertEqual("validated", audit[(switches[23]["id"], "SMagnet")]["status"])
		self.assertEqual("validated", audit[(switches[24]["id"], "IMagnet")]["status"])
		self.assertEqual("Light", audit[(outputs[28]["id"], "f28a")]["kind"])
		self.assertIn("graphical render helper", audit[(outputs[26]["id"], "f26")]["reason"])
		self.assertIn("graphical render helper", audit[(lamps[16]["id"], "l16")]["reason"])
		self.assertEqual({"f25b", "f26", "f27", "f28", "f29", "f30b", "f31", "f32", "l16"}, {record["name"] for record in report["object_audit"] if record["status"] == "unresolved" and record["kind"] == "Flasher"})
		for address in (26, 27, 29, 31, 32):
			self.assertNotIn("spatial", outputs[address])
		self.assertNotIn("spatial", lamps[16])

	def test_lamps_flashers_gi_and_native_displays_are_complete(self) -> None:
		lamps = bindings(self.definition, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(lamps))
		self.assertTrue(all(lamp["availability"] == "used" for lamp in lamps.values()))
		self.assertEqual({11, 16, 50, 51, 52, 63, 65, 76, 77, 78}, {address for address, lamp in lamps.items() if lamp["physical"]["part_number"] == "165-5000-44"})
		for address, expected in {
			1: ("YEL-BRN", "J13-P9", "RED-BRN", "J12-P1"),
			8: ("YEL-GRY", "J13-P1", "RED-BRN", "J12-P1"),
			9: ("YEL-BRN", "J13-P9", "RED-BLK", "J12-P2"),
			80: ("YEL-GRY", "J13-P1", "RED", "J12-P11"),
		}.items():
			wiring = lamps[address]["wiring"]
			self.assertEqual(expected, (wiring["drive_wire"], wiring["drive_connection"], wiring["return_wire"], wiring["return_connection"]))
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual({0}, set(gi))
		self.assertIn("four separately fused physical strings", gi[0]["physical"]["notes"])
		solenoids = bindings(self.definition, "outputs", "pinmame.output.solenoid")
		self.assertEqual({25, 26, 27, 28, 29, 30, 31, 32}, {address for address, output in solenoids.items() if output["kind"] == "flasher"})
		self.assertEqual((2, 2), (solenoids[25]["physical"]["quantity"], solenoids[30]["physical"]["quantity"]))
		self.assertIn("one #89", solenoids[30]["physical"]["notes"])
		self.assertIn("one #906", solenoids[30]["physical"]["notes"])
		self.assertEqual([(128, 32), (5, 7), (5, 7), (5, 7)], [(display["width"], display["height"]) for display in self.definition["displays"]])
		self.assertEqual([0, 1, 2, 3], [display["controller_index"] for display in self.definition["displays"]])

	def test_custom_mechanisms_capture_authoring_causality(self) -> None:
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		vari = mechanisms["mechanism.vari-target"]
		self.assertEqual(["switch.41-vari-target-opto-1", "switch.42-vari-target-opto-2", "switch.43-vari-target-opto-3"], vari["sensors"])
		for fragment in ("seven mechanical stops", "267-unit lever", "spring factor 0.3", "return speed 600", "path length 1/6", "1/2", "3/4", "closes 42 and 43"):
			self.assertIn(fragment, vari["behavior"])
		self.assertIn("100 ms", mechanisms["mechanism.trough"]["behavior"])
		self.assertEqual(["device.q19-idol-magnet", "device.q22-idol-opto-led"], mechanisms["mechanism.idol-magnet"]["actuators"])
		for fragment in ("150 ms", "tick 3", "tick 4", "tick 12"):
			self.assertIn(fragment, mechanisms["mechanism.shrunken-head-magnet"]["behavior"])
		self.assertEqual(["device.q15-left-flipper", "device.q16-right-flipper"], mechanisms["mechanism.lower-flippers"]["actuators"])
		for fragment in ("TempleDiv", "LockDiverter", "end position", "lock seats 44-46"):
			self.assertIn(fragment, mechanisms["mechanism.ramp-diverters"]["behavior"])
		self.assertIn("Q5's proven LockDiverter", mechanisms["mechanism.three-ball-lock"]["behavior"])
		self.assertEqual(["switch.1-left-cabinet-button-uk-only", "switch.8-right-cabinet-button-uk-only"], mechanisms["mechanism.optional-uk-controls"]["sensors"])
		self.assertIn("must not invent", mechanisms["mechanism.optional-q24-output"]["behavior"])

	def test_every_reference_binding_and_mechanism_endpoint_resolves_uniquely(self) -> None:
		items = [*self.definition["inputs"], *self.definition["outputs"]]
		self.assertEqual(len(items), len({item["id"] for item in items}))
		self.assertEqual(len(items), len({(item["binding"]["group"], item["binding"]["device"]) for item in items}))
		item_ids = {item["id"] for item in items}
		actuators: list[str] = []
		for mechanism in self.definition["mechanisms"]:
			self.assertLessEqual(set(mechanism["actuators"] + mechanism["sensors"]), item_ids)
			actuators.extend(mechanism["actuators"])
		self.assertEqual(len(actuators), len(set(actuators)))
		source_ids = {source["id"] for source in self.definition["sources"]}
		for item in [*items, *self.definition["displays"], *self.definition["mechanisms"]]:
			self.assertLessEqual(set(item["provenance"]["source_refs"]), source_ids)

	def test_exact_artifact_and_runtime_hashes_are_pinned_with_evidence_limits(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual("94a94aef7437fa5f78cadddd66801e96224cfe6a5b8ff643c4c6b09d979fad9e", sources["manual.stern-ripleys.2004"]["sha256"])
		self.assertEqual("3ba739ba81a3f1cad3b1a2b3a7cf7ea8db76eaf1baf4998c920f5a3d361c5ef7", sources["vpx.ripleys-vpwmod-1.3"]["sha256"])
		self.assertEqual("6c66b8cc355039ae9a4d615608802a92cd087782b16429569c87123894aadc48", sources["vpx-table.ripleys-jpsalas-1.0.3-uk"]["sha256"])
		self.assertEqual("092aab171d90eda62411496b387a90de5ca4a3273997ffb64de10c322cf366d3", sources["rom.stern-ripleys.3.20"]["sha256"])
		self.assertEqual(
			["1ef3c8baa88ace776fdf3ddbc59137afca0e7e9a6803339627985378a818270e", "e98f6058ba3d4cbd4e772606f1bc8f03039d334cde8d6045ec18d15444bf8ecc", "d389ced56f57bccd2704758cdac167b56d0a6f1621f306033adcc74d22fd57c7"],
			[run["sha256"] for run in self.evidence["runtime"]["raw_runs"]],
		)
		self.assertEqual([{"depth": 2, "height": 32, "type": 14, "width": 128}, {"depth": 2, "height": 7, "type": 526, "width": 5}], self.evidence["runtime"]["observations"]["display_layouts_seen"])
		self.assertEqual([0, 1, 2, 3], self.evidence["runtime"]["observations"]["display_indices_seen"])
		self.assertNotIn("physical_service_solenoid_to_public", self.evidence["runtime"]["observations"])
		self.assertIn("front-inserted PDF page 8", sources["manual.stern-ripleys.2004"]["locator"])
		self.assertIn("appended PDF page 190", sources["manual.stern-ripleys.2004"]["locator"])
		self.assertIn("pixel-frame callbacks only for the main DMD", self.knowledge)
		self.assertIn("must not invent either a physical or audible knocker", self.knowledge)

	def test_vpx_evidence_uses_exact_callbacks_and_source_lines(self) -> None:
		script_path = external_script_path()
		evidence = load_json(VPX_EVIDENCE_PATH)
		script_lines = script_path.read_bytes().decode(SPATIAL_GENERATOR.SCRIPT_ENCODING).splitlines()
		self.assertEqual(SPATIAL_GENERATOR.SCRIPT_SHA256, evidence["source"]["sha256"])
		self.assertEqual(3, evidence["extractor"]["version"])

		def assert_locations(value: object) -> None:
			if isinstance(value, dict):
				if "line" in value and ("source_text" in value or "raw" in value):
					self.assertEqual(value.get("source_text", value.get("raw")), script_lines[value["line"] - 1])
				if "line_start" in value:
					self.assertEqual(value["line_start"], value["line_end"])
					self.assertEqual(value["text"], script_lines[value["line_start"] - 1])
				for child in value.values():
					assert_locations(child)
			elif isinstance(value, list):
				for child in value:
					assert_locations(child)

		assert_locations(evidence)
		switches = evidence["switches"]
		switch9 = next(switch for switch in switches if switch["address"] == 9)
		switch25 = next(switch for switch in switches if switch["address"] == 25)
		self.assertEqual(("sw9_Hit", 291), (switch9["symbol"], switch9["line"]))
		self.assertEqual(("Bumper4_Hit", 304), (switch25["symbol"], switch25["line"]))
		self.assertEqual({("SMagnet_Hit", 263), ("Controller.Switch(23)", 264)}, {(switch["symbol"], switch["line"]) for switch in switches if switch["address"] == 23})
		self.assertEqual({("IMagnet_Hit", 300)}, {(switch["symbol"], switch["line"]) for switch in switches if switch["address"] == 24})
		self.assertNotIn("sw25", {switch["symbol"] for switch in switches if switch["address"] == 25})
		self.assertNotIn(320, {switch["line"] for switch in switches})

		outputs = evidence["outputs"]
		q24 = next(output for output in outputs if output["group"] == "pinmame.output.solenoid" and output["address"] == 24)
		self.assertEqual("SolCallBack(24)", q24["symbol"])
		self.assertEqual(181, q24["line"])
		lamp_addresses = {output["address"] for output in outputs if output["group"] == "pinmame.output.lamp"}
		self.assertEqual(set(range(1, 79)), lamp_addresses)
		self.assertNotIn(79, lamp_addresses)
		self.assertNotIn(80, lamp_addresses)
		self.assertEqual(540, next(output for output in outputs if output["group"] == "pinmame.output.lamp" and output["address"] == 1)["line"])
		gi_lines = [output["line"] for output in outputs if output["group"] == "pinmame.output.gi"]
		self.assertEqual([1004, 1006, 1007, 1008], gi_lines)
		self.assertNotIn("spatial_audit", evidence)
		self.assertIn(SPATIAL_GENERATOR.EXTRACTION_MANIFEST_SHA256, evidence["source"]["attribution"])

	def test_vpx_evidence_refuses_script_tamper_and_line_drift(self) -> None:
		definition = {"machine": {"id": "stern.ripley-s-believe-it-or-not.2004"}}
		original = external_script_path().read_bytes()
		with tempfile.TemporaryDirectory() as temporary_directory:
			tampered_path = Path(temporary_directory) / "tampered-script.vbs"
			tampered_path.write_bytes(original.replace(b"Sub sw9_Hit:", b"Sub sw9_Hit: ' tampered", 1))
			with self.assertRaisesRegex(ValueError, "hash mismatch"):
				SPATIAL_GENERATOR._vpx_script_evidence(definition, tampered_path)

		with tempfile.TemporaryDirectory() as temporary_directory:
			drifted_path = Path(temporary_directory) / "line-drifted-script.vbs"
			drifted_path.write_bytes(original.replace(b"Sub sw9_Hit:", b"' inserted line\r\nSub sw9_Hit:", 1))
			with self.assertRaisesRegex(ValueError, "hash mismatch"):
				SPATIAL_GENERATOR._vpx_script_evidence(definition, drifted_path)

	def test_extraction_manifest_refuses_tampered_selected_physical_object_and_snapshot_drift(self) -> None:
		source = external_extraction_path()
		with tempfile.TemporaryDirectory() as temporary_directory:
			copy = Path(temporary_directory) / "extracted-vpxtool"
			shutil.copytree(source, copy)
			physical_object = copy / "gameitems" / "Light.f28a.json"
			original_physical = physical_object.read_bytes()
			physical_object.write_bytes(original_physical.replace(b"354.07407", b"354.07408", 1))
			with self.assertRaisesRegex(ValueError, "manifest mismatch"):
				SPATIAL_GENERATOR._VPXExtraction(copy)
			physical_object.write_bytes(original_physical)

			missing_object = copy / "gameitems" / "Light.f28a.json"
			missing_object.unlink()
			with self.assertRaisesRegex(ValueError, "manifest mismatch"):
				SPATIAL_GENERATOR._VPXExtraction(copy)
			missing_object.write_bytes(original_physical)

			(copy / "gameitems" / "Added.unreviewed.json").write_bytes(b"{}\n")
			with self.assertRaisesRegex(ValueError, "manifest mismatch"):
				SPATIAL_GENERATOR._VPXExtraction(copy)
			(copy / "gameitems" / "Added.unreviewed.json").unlink()

			gamedata = copy / "gamedata.json"
			original_gamedata = gamedata.read_bytes()
			gamedata.write_bytes(original_gamedata.replace(b'"right": 952.0', b'"right": 953.0', 1))
			with self.assertRaisesRegex(ValueError, "manifest mismatch"):
				SPATIAL_GENERATOR._VPXExtraction(copy)


class RipleysPopBumperGeometryTests(unittest.TestCase):
	"""Guards the eight reversed placements this record shipped before 2026-08-07.

	The retained known-working table is internally inconsistent about its own pop bumpers: its
	*_Hit switch handlers and its lamp handling assign "right" and "bottom" to opposite bodies.
	An earlier revision of the spatial curator followed the switch half and produced eight
	`validated` placements in which the right and bottom members of both clusters were swapped.
	The manual's Coil & Flash Lamp Locations and Switch Matrix Grid Locations drawings both settle
	it the other way, and the script's own lamp half agrees with them.

	Three independent invariants are asserted. Only the co-location and bottom-y checks would each
	have caught the whole defect on their own: the x-ordering check catches the lower cluster but
	not the upper one, because the reversed upper pair happened to keep an ascending x (the body
	wrongly named "right" sat at 0.810 against "left" at 0.655). That is exactly why more than one
	invariant is asserted here.
	"""

	@classmethod
	def setUpClass(cls) -> None:
		definition = load_json(DEFINITION_PATH)
		cls.points = {}
		for group in ("inputs", "outputs"):
			for device in definition[group]:
				spatial = device.get("spatial") or {}
				placements = spatial.get("placements") or []
				if placements:
					cls.points[device["id"]] = (placements[0]["x"], placements[0]["y"])

	# switch id, coil id, lamp id for each of the six physical bumpers
	CLUSTERS = {
		"lower": [
			("left", "switch.25-lower-left-pop-bumper", "device.q6-lower-left-pop-bumper", "lamp.33-lower-left-pop-bumper"),
			("right", "switch.26-lower-right-pop-bumper", "device.q7-lower-right-pop-bumper", "lamp.34-lower-right-pop-bumper"),
			("bottom", "switch.27-lower-bottom-pop-bumper", "device.q8-lower-bottom-pop-bumper", "lamp.35-lower-bottom-pop-bumper"),
		],
		"upper": [
			("left", "switch.49-upper-left-pop-bumper", "device.q9-upper-left-pop-bumper", "lamp.60-upper-left-pop-bumper"),
			("right", "switch.50-upper-right-pop-bumper", "device.q10-upper-right-pop-bumper", "lamp.61-upper-right-pop-bumper"),
			("bottom", "switch.51-upper-bottom-pop-bumper", "device.q11-upper-bottom-pop-bumper", "lamp.62-upper-bottom-pop-bumper"),
		],
	}

	def test_switch_coil_and_lamp_of_one_bumper_are_co_located(self) -> None:
		"""All three devices sit on one physical bumper, so they must share a position.

		The lamp is allowed a small offset because its BumperLight object is nudged off the body
		centre for the glow, but nothing here may land on a different bumper -- the bumpers are
		more than 0.06 apart, so a 0.02 tolerance cannot mask a swap.
		"""
		for cluster, members in self.CLUSTERS.items():
			for position, switch_id, coil_id, lamp_id in members:
				switch = self.points[switch_id]
				coil = self.points[coil_id]
				lamp = self.points[lamp_id]
				self.assertEqual(switch, coil, f"{cluster} {position}: switch and coil must be identical")
				for axis, index in (("x", 0), ("y", 1)):
					self.assertAlmostEqual(
						switch[index], lamp[index], delta=0.02,
						msg=f"{cluster} {position}: lamp {axis} is on a different bumper than the switch",
					)

	def test_right_member_is_further_right_than_the_left_member(self) -> None:
		for cluster, members in self.CLUSTERS.items():
			by_position = {position: self.points[switch_id] for position, switch_id, _, _ in members}
			self.assertLess(
				by_position["left"][0], by_position["right"][0],
				f"{cluster} cluster: the member named 'right' must have the greater x",
			)

	def test_bottom_member_is_nearest_the_player(self) -> None:
		"""y = 1 is the apron end, so "bottom" must carry the greatest y in its cluster."""
		for cluster, members in self.CLUSTERS.items():
			by_position = {position: self.points[switch_id] for position, switch_id, _, _ in members}
			bottom_y = by_position["bottom"][1]
			for position in ("left", "right"):
				self.assertGreater(
					bottom_y, by_position[position][1],
					f"{cluster} cluster: 'bottom' must be nearer the player than '{position}'",
				)


if __name__ == "__main__":
	unittest.main()
