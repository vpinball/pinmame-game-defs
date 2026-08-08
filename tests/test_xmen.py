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
PRO_SPATIAL_AUDIT_PATH = ROOT / "reports" / "spatial" / "stern" / "x-men-pro-2012.json"


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
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.pro["coverage"]["missing"])
		for definition in (self.le, self.pro):
			self.assertEqual("complete", definition["knowledge"]["status"])
		self.assertEqual([], self.le["conflicts"])
		self.assertEqual(["conflict.pro-lamp-59-script-versus-physical-inventory"], [conflict["id"] for conflict in self.pro["conflicts"]])
		self.assertEqual("outputs[pinmame.output.lamp:59]", self.pro["conflicts"][0]["path"])
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

	def test_changed_xmen_files_contain_no_developer_absolute_paths(self) -> None:
		for path in (
			ROOT / "knowledge" / "stern" / "x-men-limited-edition-2012.md",
			ROOT / "knowledge" / "stern" / "x-men-pro-2012.md",
			ROOT / "machines" / "partial" / "stern" / "x-men-limited-edition-2012.json",
			ROOT / "machines" / "partial" / "stern" / "x-men-pro-2012.json",
			PRO_SPATIAL_AUDIT_PATH,
			ROOT / "tests" / "test_xmen.py",
			ROOT / "tools" / "curate_xmen.py",
			ROOT / "tools" / "curate_xmen_le_spatial.py",
		):
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
		self.assertEqual("unknown", lamps[59]["availability"])
		self.assertEqual("observed", lamps[59]["provenance"]["status"])
		self.assertEqual("Wolverine feature reflection (script-only)", lamps[59]["label"])
		self.assertIn("f59b", lamps[59]["physical"]["notes"])
		self.assertNotIn("location", lamps[59]["physical"])
		self.assertIn("x=742.9, y=1130.5", lamps[49]["physical"]["location"])
		sources = {source["id"]: source for source in self.pro["sources"]}
		self.assertEqual("00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8", sources["vpx-table.x-men-pro-physmod5"]["sha256"])
		self.assertTrue(sources["vpx-table.x-men-pro-physmod5"]["known_working"])
		self.assertIn("inventory.json SHA-256 d197a15cccc29b18be6d5b9128b110b83fd2aa3b109a9c0df8d2ffff174303e8", sources["vpx-table.x-men-pro-physmod5"]["locator"])

	def test_pro_curator_output_is_honest_without_the_retrofit_transform(self) -> None:
		"""build_pro() must be self-consistent on its own, not only after the pending-set rewrite.

		fail_closed_spatial_partial() currently downgrades this machine to partial because it is
		listed in SPATIAL_RETROFIT_PENDING_MACHINE_IDS. Removing it from that tuple is the intended
		step once spatial placement is reconciled, so build_pro() must not rely on that rewrite to
		avoid claiming author_ready while it still lists missing requirements and an open conflict.
		"""
		import sys

		tools = str(ROOT / "tools")
		if tools not in sys.path:
			sys.path.insert(0, tools)
		import curate_xmen

		raw = curate_xmen.build_pro()
		coverage = raw["coverage"]
		if coverage["missing"] or raw["conflicts"]:
			self.assertNotEqual(
				"author_ready",
				coverage["status"],
				"build_pro() claims author_ready while still listing missing requirements or conflicts",
			)

	def test_pro_spatial_retrofit_fails_closed_on_unreconciled_sockets(self) -> None:
		inputs = bindings(self.pro, "inputs", "pinmame.input.switch")
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		self.assertTrue(all("spatial" not in device for device in self.pro["inputs"] + self.pro["outputs"]))
		for address in (17, 18, 22, 28, 29, 31):
			self.assertNotIn("quantity", outputs[address]["physical"])
		self.assertEqual("Pro output 17 flasher render group", outputs[17]["label"])
		self.assertEqual("Pro output 18 flasher render group", outputs[18]["label"])
		self.assertEqual("Pro output 22 flasher render group", outputs[22]["label"])
		self.assertEqual("Pro output 28 backpanel render group", outputs[28]["label"])
		self.assertEqual("Pro output 29 backpanel render group", outputs[29]["label"])
		self.assertNotIn("double", " ".join(outputs[address]["label"].lower() for address in (17, 18, 22, 28, 29)))
		self.assertNotIn("triple", " ".join(outputs[address]["label"].lower() for address in (17, 18, 22, 28, 29)))
		self.assertIn("f118 at x=805.5, y=1438.0", outputs[18]["physical"]["location"])
		self.assertIn("f118b at x=917.5, y=594.0", outputs[18]["physical"]["location"])
		self.assertIn("page 60 gives Q18 no X2 marker", outputs[18]["physical"]["notes"])
		self.assertIn("page 61 shows two 18 callouts", outputs[18]["physical"]["notes"])
		self.assertIn("f122 at x=503.5, y=288.0", outputs[22]["physical"]["location"])
		self.assertIn("non-canonical", outputs[22]["physical"]["location"])
		self.assertIn("lossy ad-hoc .NET extractor", outputs[22]["physical"]["notes"])
		self.assertIn("f129 at x=843.5, y=94.0", outputs[29]["physical"]["location"])
		self.assertIn("f129a at x=639.5, y=90.0", outputs[29]["physical"]["location"])
		self.assertEqual("Unresolved Pro output 31 flasher candidate", outputs[31]["label"])
		self.assertIn("f131 at x=527.5, y=472.0", outputs[31]["physical"]["location"])
		self.assertIn("LE-specific", outputs[31]["physical"]["notes"])
		self.assertIn("does not establish either Pro physical identity or multiplicity", outputs[31]["physical"]["notes"])
		self.assertIn("No second Pro Q31 socket is established", outputs[31]["physical"]["notes"])
		for address in (17, 18, 21, 22, 25, 27, 28, 29, 31):
			self.assertIn("Raw VPX candidate", outputs[address]["physical"]["location"])
			self.assertIn("canonical spatial placement", outputs[address]["physical"]["notes"])
		self.assertNotIn("spatial", bindings(self.pro, "outputs", "pinmame.output.gi")[0])
		for address in (3, 11, 38, 71):
			lamp = bindings(self.pro, "outputs", "pinmame.output.lamp")[address]
			self.assertIn("Raw VPX candidate position", lamp["physical"]["location"])
			self.assertIn("not a canonical spatial placement", lamp["physical"]["notes"])
		for address in (18, 19, 20, 21, 22):
			self.assertNotIn("spatial", inputs[address])
		knowledge = (ROOT / "knowledge" / "stern" / "x-men-pro-2012.md").read_text(encoding="utf-8")
		self.assertIn("x=0 left/x=1 right", knowledge)
		self.assertIn("retained only as raw VPX candidate locations", knowledge)
		self.assertIn("have not been promoted to schema-v2 `spatial` placements", knowledge)
		self.assertIn("GI output 0", knowledge)
		self.assertIn("Flasher output 18", knowledge)
		self.assertIn("output 22", knowledge)
		self.assertIn("output 29", knowledge)
		self.assertIn("Flasher output 31", knowledge)
		self.assertIn("Q31 Pro physical identity and multiplicity are both unresolved", knowledge)
		self.assertIn("no second Q31 socket is established", knowledge)
		self.assertIn("raw candidate `f122`", knowledge)
		self.assertIn("lamp state 59", knowledge)
		self.assertIn("right=959, bottom=2162", knowledge)
		self.assertIn("bsTrough.InitSw 0, 21, 20, 19, 18", knowledge)
		self.assertIn("page 57 groups `18-22`", knowledge)
		self.assertIn("## Author construction checklist", knowledge)
		self.assertIn("jam 22", knowledge)
		self.assertIn("keep the Pro definition `partial`", knowledge)
		self.assertIn("`unresolved_conflicts`", knowledge)
		self.assertIn("full `vpxtool extract`", knowledge)
		self.assertIn("exit 101", knowledge)
		self.assertIn("LE evidence is itself inconsistent for Q18", knowledge)
		self.assertIn("outputs 17, 18, 22, 28, 29, and 31", knowledge)

	def test_pro_spatial_audit_is_fail_closed_and_machine_specific(self) -> None:
		audit = load_json(PRO_SPATIAL_AUDIT_PATH)
		self.assertEqual("pinmame-spatial-blockers", audit["format"])
		self.assertEqual("stern.x-men-pro.2012", audit["machine_id"])
		self.assertEqual({"left": 0.0, "top": 0.0, "right": 959.0, "bottom": 2162.0}, audit["coordinate_convention"]["source_bounds"])
		self.assertEqual("attempted_failed_no_output", audit["extraction"]["vpxtool"]["coordinate_export_status"])
		self.assertIn("vpxtool extract --force", audit["extraction"]["vpxtool"]["coordinate_export_command"])
		self.assertEqual(101, audit["extraction"]["vpxtool"]["failure"]["exit_code"])
		self.assertIn("panics before VPXTool writes any extracted item files", audit["extraction"]["vpxtool"]["limitation"])
		raw_extractor = audit["extraction"]["raw_candidate_inventory"]
		self.assertEqual("unidentified_ad_hoc_dotnet_extractor_using_visualpinball_engine_vpt_records", raw_extractor["extractor_identity"])
		self.assertIn("tools/_xmen_vpt_extract.csproj", raw_extractor["command_project_clue"])
		self.assertIn("absent", raw_extractor["source_and_version"])
		self.assertEqual("lossy", raw_extractor["lossiness"]["status"])
		self.assertEqual(10556, raw_extractor["lossiness"]["unknown_tag_occurrences"])
		self.assertEqual(79, raw_extractor["lossiness"]["unique_unknown_tag_count"])
		self.assertIn("GRSZ", raw_extractor["lossiness"]["unique_unknown_tags"])
		self.assertIn("TRNS", raw_extractor["lossiness"]["unique_unknown_tags"])
		self.assertEqual({"observed_table_bounds", "normalization_withheld"}, {item["class"] for item in audit["transformations"]})
		self.assertEqual({"raw_candidate_only", "assembly_anchor_rejected", "edition_transfer_rejected"}, {item["class"] for item in audit["projection_classes"]})
		candidates = {(item["binding"]["group"], item["binding"]["address"]): item for item in audit["candidate_coordinates"]}
		self.assertEqual({("pinmame.output.solenoid", 17), ("pinmame.output.solenoid", 18), ("pinmame.output.solenoid", 22), ("pinmame.output.solenoid", 28), ("pinmame.output.solenoid", 29), ("pinmame.output.solenoid", 31), ("pinmame.output.lamp", 59)}, set(candidates))
		self.assertEqual([{"name": "f122", "x": 503.5, "y": 288.0}], candidates[("pinmame.output.solenoid", 22)]["objects"])
		self.assertIn("identity and multiplicity unresolved", candidates[("pinmame.output.solenoid", 31)]["disposition"])
		self.assertEqual([{"name": "f59b", "x": 201.5, "y": 1094.0}], candidates[("pinmame.output.lamp", 59)]["objects"])
		blockers = {item["id"]: item for item in audit["unresolved_blockers"]}
		self.assertEqual({"gi-0-pro-socket-geometry", "solenoid-17-pro-identity-and-multiplicity", "solenoid-18-pro-socket-identity", "solenoid-22-pro-socket-geometry", "solenoid-28-pro-identity-and-multiplicity", "solenoid-29-pro-socket-geometry", "solenoid-31-pro-identity-and-multiplicity", "lamp-59-script-versus-physical-inventory", "switches-18-through-22-trough-centers"}, set(blockers))
		self.assertEqual([18, 19, 20, 21, 22], blockers["switches-18-through-22-trough-centers"]["devices"]["inputs"])
		self.assertIn("no second socket is established", blockers["solenoid-31-pro-identity-and-multiplicity"]["blocker"])
		self.assertEqual([{"group": "pinmame.output.lamp", "address": 59}], blockers["lamp-59-script-versus-physical-inventory"]["devices"]["outputs"])
		self.assertEqual("reject_edition_mismatched_counts_and_positions", audit["manual_review"]["transfer_decision"])
		self.assertIn("page 61 visibly contains two 18 callouts", audit["manual_review"]["q18_internal_conflict"])
		self.assertEqual(["manual_page_renders", "manual_selected_page_ocr"], audit["manual_review"]["retained_review_evidence"])
		self.assertEqual("remain_partial", audit["promotion_decision"]["decision"])
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], audit["promotion_decision"]["coverage_missing"])

	def test_pro_external_vpx_and_spatial_audit_evidence_are_hash_locked(self) -> None:
		root = external_root("PINMAME_VPX_SOURCES_ROOT") / "stern" / "x-men-pro-2012"
		expected_files = {
			"source/XMen FS (physmod5).zip": (21499804, "6f5eae417c894af5947a819448f45616cb2348a1cfdca5cff544e6bdcda439fb"),
			"source/XMen FS (physmod5)/XMen FS  (physmod5).vpt": (25464832, "00784b76eb35991d4bb4b13939862f67506f06cb017426668d57a66ded8829d8"),
			"analysis/physmod5/inventory.json": (250396, "d197a15cccc29b18be6d5b9128b110b83fd2aa3b109a9c0df8d2ffff174303e8"),
			"analysis/physmod5/table-script.vbs": (42442, "90cd88f121798f7c91ba738713c2aae99784751637380beb864ee3e2bcde25cb"),
			"analysis/physmod5/textures/PF A.jpg": (448926, "5dc652f161f4494b8072fc08cb74a89e5bb6253a45fd16255e4383e6b0576ea6"),
			"extraction/vpxtool-0.33.3/gamedata.json": (5267, "da89862afc2d9433fbc730d3aa453af85c3c894fc5381c8bd5b99c26b40fc43f"),
			"extraction/vpxtool-0.33.3-full/failure.json": (1682, "1d66232147c795bcddac0b57cf8bd78f03554cf039f0e5d195773f0df513878d"),
			"extraction/vpxtool-0.33.3-full/extract.stdout.log": (107, "917c7ddf161ee611178a5376c23ecd8c8fdbd9762d7c7af260daf8c8e97e1b22"),
			"extraction/vpxtool-0.33.3-full/extract.stderr.log": (1154164, "101ea8bcfdfe4c6d5e0076bb5527121a53bfcbf54fbf3b49ab9a5ed403e91090"),
			"extraction/physmod5-vpt/loader.log": (718448, "da276598d764d4605698975ee66d6bf20e2063eaf5a4aa631c00d802716a92ac"),
		}
		for relative_path, (size, expected_hash) in expected_files.items():
			path = root / relative_path
			self.assertTrue(path.is_file(), path)
			self.assertEqual(size, path.stat().st_size, path)
			self.assertEqual(expected_hash, hashlib.sha256(path.read_bytes()).hexdigest(), path)
		audit = load_json(PRO_SPATIAL_AUDIT_PATH)
		gamedata = load_json(root / "extraction" / "vpxtool-0.33.3" / "gamedata.json")
		self.assertEqual(audit["coordinate_convention"]["source_bounds"], {key: gamedata[key] for key in ("left", "top", "right", "bottom")})
		self.assertEqual("git:v0.33.3", audit["extraction"]["vpxtool"]["version"])
		self.assertEqual(expected_files["extraction/vpxtool-0.33.3/gamedata.json"][1], audit["evidence_artifacts"]["vpxtool_gamedata"]["sha256"])
		self.assertEqual(expected_files["extraction/vpxtool-0.33.3-full/failure.json"][1], audit["evidence_artifacts"]["vpxtool_extraction_failure"]["sha256"])
		failure = load_json(root / "extraction" / "vpxtool-0.33.3-full" / "failure.json")
		self.assertEqual("pinmame-vpxtool-extraction-failure", failure["format"])
		self.assertEqual(101, failure["exit_code"])
		self.assertEqual("no_extracted_files_written", failure["output"]["status"])
		self.assertEqual(expected_files["source/XMen FS (physmod5)/XMen FS  (physmod5).vpt"][1], failure["input_adapter"]["renamed_copy_sha256"])
		self.assertIn("vpxtool extract chooses the parser", failure["input_adapter"]["reason"])
		self.assertIn("gamedata and gameitems can read the .vpt directly", failure["input_adapter"]["reason"])
		self.assertEqual(0, failure["output"]["file_count"])
		stderr = (root / "extraction" / "vpxtool-0.33.3-full" / "extract.stderr.log").read_text(encoding="utf-8")
		self.assertIn("range end index 39403 out of range for slice of length 39402", stderr)
		self.assertFalse(any((root / "extraction" / "vpxtool-0.33.3-full").rglob("gameitems/*.json")))
		self.assertEqual({"failure.json", "extract.stdout.log", "extract.stderr.log"}, {path.name for path in (root / "extraction" / "vpxtool-0.33.3-full").iterdir()})
		analysis_root = root / "analysis" / "physmod5"
		entries = []
		for path in sorted((path for path in analysis_root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(analysis_root).as_posix()):
			entries.append({"path": path.relative_to(analysis_root).as_posix(), "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
		manifest = audit["extraction"]["retained_analysis_manifest"]
		self.assertEqual(entries, manifest["entries"])
		self.assertEqual(sum(entry["size"] for entry in entries), manifest["total_bytes"])
		self.assertEqual(hashlib.sha256(json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(), manifest["sha256"])
		loader_text = (root / "extraction" / "physmod5-vpt" / "loader.log").read_text(encoding="utf-16")
		unknown_tags = sorted(set(re.findall(r"Unknown tag ([A-Z0-9]{4})", loader_text)))
		self.assertEqual(10556, len(re.findall(r"Unknown tag ([A-Z0-9]{4})", loader_text)))
		self.assertEqual(unknown_tags, audit["extraction"]["raw_candidate_inventory"]["lossiness"]["unique_unknown_tags"])
		inventory = load_json(analysis_root / "inventory.json")
		flashers = {item["Name"]: item for item in inventory["Flashers"]}
		self.assertEqual({"Name": "f122", "X": 503.5, "Y": 288, "Height": 100, "ImageA": "fcr", "ImageB": None, "IsVisible": True}, flashers["f122"])

	def test_pro_selected_manual_review_artifacts_are_hash_locked(self) -> None:
		root = external_root("PINMAME_MANUALS_ROOT") / "by-machine" / "stern.x-men-pro-limited-edition.2012" / "primetime-amusements" / "extracted"
		expected_renders = {
			"page-056.png": (493289, "4570d89f3d7fd35ab9957336e92270fc3888e55a12669d265233f633f5b7323c"),
			"page-057.png": (539057, "f7f970c003b56e048d3ea744b7a2b75fe7feeaea6aa655bd72586c503359a30f"),
			"page-058.png": (342231, "cf70a3b5455f6bf8f0eba84749ed000cf532e80d4b5a3219231a7cad6c2b49b5"),
			"page-059.png": (365760, "ecc488adf364b9447f9ef43fa9140c0e5def1de8d15db410b558217e3166f9b7"),
			"page-060.png": (290727, "15bb165e604bc9839a4cee9c6a66f0cb7b3a8c265311d4f40334bef98bc44f73"),
			"page-061.png": (481891, "45b714f85813592f5599da964f74421539106c2cd684cbec3365f2ec972c0580"),
			"page-062.png": (79570, "9a399dd617d684313adcb50786fb970d2509b496bbed9a757bed3e7e0857f3df"),
			"page-109.png": (278677, "1e086f5c459a3f0f10b3063aa132eb8ea1894f3003c328268dc13481dca12b38"),
			"page-110.png": (286150, "c58b6c0cb5ad52cffb13355f631688087c59cc4bb4eaeff8f9a73368f3b4a805"),
			"page-111.png": (273435, "38081cfe6492152210d0f7c0995843a900378de322ea7ce44cc0f3c8f4d9842e"),
		}
		for name, (size, expected_hash) in expected_renders.items():
			path = root / "rendered-pages" / name
			self.assertEqual(size, path.stat().st_size, path)
			self.assertEqual(expected_hash, hashlib.sha256(path.read_bytes()).hexdigest(), path)
		ocr_path = root / "ocr-selected" / "pages-056-062-109-111.md"
		self.assertEqual(3180, ocr_path.stat().st_size)
		self.assertEqual("1b194820180e5a7a90b573cebff45de2c48b8354d298557b8aa210c76d1ac755", hashlib.sha256(ocr_path.read_bytes()).hexdigest())
		audit = load_json(PRO_SPATIAL_AUDIT_PATH)
		self.assertEqual([56, 57, 58, 59, 60, 61, 62, 109, 110, 111], [item["page"] for item in audit["evidence_artifacts"]["manual_page_renders"]["files"]])
		self.assertEqual("1b194820180e5a7a90b573cebff45de2c48b8354d298557b8aa210c76d1ac755", audit["evidence_artifacts"]["manual_selected_page_ocr"]["sha256"])

	def test_sources_and_exact_rom_run_are_hash_locked(self) -> None:
		sources = {source["id"]: source for source in self.le["sources"]}
		self.assertEqual("0812b91d0950ff8c1b15c5bc17afc827029ca8aaaa0bbb78cc11ea606b629bf8", sources["manual.x-men-pro-le.2012"]["sha256"])
		self.assertIn("LE-only", sources["manual.x-men-pro-le.2012"]["locator"])
		self.assertEqual("d793836fefab6c0de53463943e36245c7ed800d5ca86675e3c2b2f46df693643", sources["manual.x-men-pro-le.2012.high-resolution"]["sha256"])
		self.assertIn("page 60 lacks a Q18 X2 marker", sources["manual.x-men-pro-le.2012.high-resolution"]["locator"])
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
			pro_paths = [root / "machines" / "partial" / "stern" / "x-men-pro-2012.json", root / "knowledge" / "stern" / "x-men-pro-2012.md", root / "reports" / "spatial" / "stern" / "x-men-pro-2012.json"]
			pro_first = [path.read_bytes() for path in pro_paths]
			self.assertEqual([PRO_PATH.read_bytes(), (ROOT / "knowledge" / "stern" / "x-men-pro-2012.md").read_bytes(), PRO_SPATIAL_AUDIT_PATH.read_bytes()], pro_first)
			base_module.main()
			self.assertEqual(spatial_first, [path.read_bytes() for path in paths])
			self.assertEqual(pro_first, [path.read_bytes() for path in pro_paths])
			self.assertFalse((root / "machines" / "author-ready" / "stern" / "x-men-limited-edition-2012.json").exists())


if __name__ == "__main__":
	unittest.main()
