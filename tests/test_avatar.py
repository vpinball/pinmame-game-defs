from __future__ import annotations

import json
import importlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
PRO_PATH = ROOT / "machines" / "partial" / "stern" / "avatar-pro-2010.json"
PRO_KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "avatar-pro-2010.md"
LE_PATH = ROOT / "machines" / "partial" / "stern" / "avatar-limited-edition-2010.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avatar-pro-boot-start.json"
LE_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "avatar-limited-edition-boot-start.json"
LE_DIAGNOSTIC_PATHS = {
	"transporter-up-to-down": ROOT / "evidence" / "runtime" / "sam" / "avatar-limited-edition-transporter-up-to-down.json",
	"transporter-down-to-up": ROOT / "evidence" / "runtime" / "sam" / "avatar-limited-edition-transporter-down-to-up.json",
	"amp-suit-motor": ROOT / "evidence" / "runtime" / "sam" / "avatar-limited-edition-amp-suit-motor.json",
	"three-bank-motor": ROOT / "evidence" / "runtime" / "sam" / "avatar-limited-edition-three-bank-motor.json",
}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


class AvatarDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.pro = load_json(PRO_PATH)
		cls.le = load_json(LE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)
		cls.le_evidence = load_json(LE_EVIDENCE_PATH)
		cls.le_diagnostics = {name: load_json(path) for name, path in LE_DIAGNOSTIC_PATHS.items()}

	def test_both_editions_remain_fail_closed_for_spatial_retrofit(self) -> None:
		for definition in (self.pro, self.le):
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("partial", definition["coverage"]["status"])
			expected = ["spatial_placement"]
			if definition.get("conflicts"):
				expected.append("unresolved_conflicts")
			self.assertEqual(expected, definition["coverage"]["missing"])
			self.assertEqual("unknown", definition["coverage"]["dimensions"]["spatial_placement"])
			if definition is self.le:
				self.assertEqual("not_applicable", definition["displays"][0]["spatial"]["status"])
				self.assertEqual("cabinet_or_service", definition["displays"][0]["spatial"]["reason"])
				self.assertEqual(
					["pinmame.core.4ec52ff0ac13", "manual.avatar-pro-le.2010"],
					definition["displays"][0]["spatial"]["provenance"]["source_refs"],
				)
		self.assertEqual("complete", self.pro["knowledge"]["status"])
		self.assertEqual("complete", self.le["knowledge"]["status"])
		self.assertEqual(
			{"conflict.pro-le-target-and-sling-spatial", "conflict.pro-le-mechanism-spatial", "conflict.pro-le-flasher-quantity"},
			{conflict["id"] for conflict in self.pro["conflicts"]},
		)
		self.assertEqual([], self.le["conflicts"])
		self.assertFalse((ROOT / "machines" / "stubs" / "avr_120h.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "avr_120h.md").exists())

	def test_pro_spatial_inventory_retains_only_defensible_geometry_and_quantities(self) -> None:
		inputs = bindings(self.pro, "inputs", "pinmame.input.switch")
		outputs = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		devices = [*self.pro["inputs"], *self.pro["outputs"]]
		self.assertTrue(all(device.get("spatial", {}).get("status") in {None, "validated", "not_applicable"} for device in devices))
		self.assertEqual({"unused"}, {inputs[address]["spatial"].get("reason", "located") for address in (41, 47, 48, 72)})
		blocked_inputs = {18, 19, 20, 21, 45, 46, 57, 58}
		self.assertTrue(all("spatial" not in inputs[address] for address in blocked_inputs))
		self.assertTrue(all("intentionally withheld" in inputs[address]["physical"]["notes"] for address in blocked_inputs))
		self.assertEqual((0.848214, 0.871661), tuple(inputs[22]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		self.assertEqual((0.949580, 0.881560), tuple(inputs[23]["spatial"]["placements"][0][axis] for axis in ("x", "y")))
		for address in (7, 8, 26, 27):
			self.assertNotIn("spatial", inputs[address])
			self.assertIn("polygon-derived", inputs[address]["physical"]["notes"])
		blocked_flashers = {20, 21, 22, 23, 26}
		self.assertTrue(all("spatial" not in outputs[address] for address in blocked_flashers))
		self.assertEqual({20: 1, 21: 2, 22: 1, 23: 1, 26: 1}, {address: outputs[address]["physical"]["quantity"] for address in blocked_flashers})
		self.assertTrue(all("intentionally withheld" in outputs[address]["physical"]["notes"] for address in blocked_flashers))
		for address in (6, 7, 17, 18, 25, 30, 31):
			self.assertNotIn("spatial", outputs[address])
			self.assertIn("intentionally withheld", outputs[address]["physical"]["notes"])
		for address in (25, 30, 31):
			self.assertNotIn("quantity", outputs[address]["physical"])
			self.assertIn("conflict", outputs[address]["physical"]["notes"])
		self.assertIn("disagree", outputs[6]["physical"]["notes"])
		self.assertIn("disagree", outputs[7]["physical"]["notes"])
		for address in (5, 13, 19):
			self.assertEqual(("not_applicable", "internal_nonvisual"), (outputs[address]["spatial"]["status"], outputs[address]["spatial"]["reason"]))
			self.assertIn("internal mechanism load", outputs[address]["physical"]["notes"])
		self.assertEqual((2, 2), (outputs[28]["physical"]["quantity"], len(outputs[28]["spatial"]["placements"])))
		self.assertEqual((1, 1), (outputs[29]["physical"]["quantity"], len(outputs[29]["spatial"]["placements"])))
		self.assertEqual((1, 1), (outputs[32]["physical"]["quantity"], len(outputs[32]["spatial"]["placements"])))
		self.assertTrue(all(lamps[address]["physical"]["quantity"] == len(lamps[address]["spatial"]["placements"]) for address in lamps if lamps[address]["availability"] == "used" and address not in {1, 2}))
		gi = bindings(self.pro, "outputs", "pinmame.output.gi")[0]
		self.assertEqual(37, gi["physical"]["quantity"])
		self.assertNotIn("spatial", gi)
		self.assertIn("23 generic VPX GI render-pool objects", gi["physical"]["notes"])

	def test_pro_spatial_source_and_display_contract_are_pinned(self) -> None:
		sources = {source["id"]: source for source in self.pro["sources"]}
		archive = sources["vpx-table.avatar-pro.archive-080116a-geometry"]
		self.assertEqual("aaff981437470f8c4edf6b2902e7a6d78db19d826a04d9662e3bcb812dd9740d", archive["sha256"])
		self.assertFalse(archive["known_working"])
		self.assertNotIn("L:\\", archive["locator"])
		self.assertIn("byte-distinct", archive["locator"])
		self.assertFalse(sources["vpx-table.avatar-pro.vpuniverse-4755"]["known_working"])
		self.assertIn("byte-distinct", sources["vpx-table.avatar-pro.vpuniverse-4755"]["locator"])
		display = self.pro["displays"][0]
		self.assertEqual((128, 32, "dmd"), (display["width"], display["height"], display["kind"]))
		self.assertIn("runtime.avatar-pro.boot-start", display["provenance"]["source_refs"])
		self.assertEqual(("not_applicable", "cabinet_or_service"), (display["spatial"]["status"], display["spatial"]["reason"]))

	def test_pro_spatial_generator_matches_committed_artifacts(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		try:
			curator = importlib.import_module("curate_avatar_pro_spatial")
		finally:
			sys.path.pop(0)
		self.assertEqual(self.pro, curator.build_curated_definition())
		self.assertEqual(PRO_KNOWLEDGE_PATH.read_text(encoding="utf-8"), curator.SPATIAL_KNOWLEDGE)

	def test_le_spatial_retrofit_keeps_edition_specific_devices_out_of_pro_geometry(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		for address in (41, 47, 48, 72):
			self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", inputs[address]["provenance"]["source_refs"])
			self.assertNotIn("vpx-table.avatar-pro.local-archive-2020", inputs[address].get("spatial", {}).get("placements", [{}])[0].get("provenance", {}).get("source_refs", []))
		self.assertNotIn("spatial", inputs[41])
		self.assertIn("LeftRampStart", inputs[41]["physical"]["notes"])
		for address in (8, 18, 19, 20, 21, 22, 23, 26, 27, 41, 42, 43, 44, 45, 46, 47, 48, 57, 58, 72):
			self.assertNotIn("spatial", inputs[address])
			self.assertIn("Spatial blocker:", inputs[address]["physical"]["notes"])
		for address in (4, 5, 12, 13, 14, 17, 18, 19, 27):
			self.assertNotIn("spatial", outputs[address])
			self.assertIn("Spatial blocker:", outputs[address]["physical"]["notes"])
		self.assertEqual(2, outputs[27]["physical"]["quantity"])
		self.assertEqual(2, outputs[21]["physical"]["quantity"])
		self.assertEqual("not_applicable", outputs[21]["spatial"]["status"])
		self.assertNotIn("spatial", outputs[22])
		self.assertIn("fantasy placement", outputs[22]["physical"]["notes"])
		for address in (20, 22, 23, 25, 26, 28, 29, 30, 31, 32):
			self.assertNotIn("spatial", outputs[address])
		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		for address in (20, 44, 45, 46):
			self.assertNotIn("spatial", lamps[address])
			self.assertIn("Spatial blocker:", lamps[address]["physical"]["notes"])
		gi = next(item for item in self.le["outputs"] if item["binding"] == {"group": "pinmame.output.gi", "device": 0})
		self.assertNotIn("spatial", gi)
		self.assertNotIn("quantity", gi.get("physical", {}))
		self.assertIn("GIWhite", gi["physical"]["notes"])

	def test_le_only_mechanisms_and_generator_artifacts_are_fail_closed(self) -> None:
		mechanisms = {item["id"]: item for item in self.le["mechanisms"]}
		for mechanism_id in ("mechanism.transporter", "mechanism.amp-marching-legs", "mechanism.ceramic-ball"):
			self.assertIn(mechanism_id, mechanisms)
			self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", mechanisms[mechanism_id]["provenance"]["source_refs"])
		generator = (ROOT / "tools" / "curate_avatar_le_spatial.py").read_text(encoding="utf-8")
		self.assertNotIn("E:\\_vpe-2025", generator)
		self.assertIn("--artifact-root", generator)

	def test_le_spatial_curator_check_is_deterministic_and_non_mutating(self) -> None:
		paths = [LE_PATH, ROOT / "knowledge" / "stern" / "avatar-limited-edition-2010.md"]
		before = {path: path.read_bytes() for path in paths}
		with tempfile.TemporaryDirectory() as artifact_root:
			artifact_path = Path(artifact_root)
			result = subprocess.run(
				[sys.executable, str(ROOT / "tools" / "curate_avatar_le_spatial.py"), "--check", "--artifact-root", artifact_root],
				cwd=ROOT,
				capture_output=True,
				text=True,
				check=False,
			)
			self.assertEqual(0, result.returncode, result.stderr)
			self.assertIn("no files were written or deleted", result.stdout)
			self.assertFalse((artifact_path / "analysis").exists())
		self.assertEqual(before, {path: path.read_bytes() for path in paths})

	def test_le_spatial_curator_check_reports_mismatch_without_deleting_author_ready(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		try:
			curator = importlib.import_module("curate_avatar_le_spatial")
		finally:
			sys.path.pop(0)
		with tempfile.TemporaryDirectory() as root:
			temp_root = Path(root)
			partial_path = temp_root / "partial.json"
			knowledge_path = temp_root / "knowledge.md"
			author_ready_path = temp_root / "author-ready.json"
			partial_path.write_bytes(b"stale")
			knowledge_path.write_bytes(b"stale")
			author_ready_path.write_bytes(b"preserve this file")
			with patch.object(curator, "PARTIAL_PATH", partial_path), patch.object(curator, "KNOWLEDGE_PATH", knowledge_path), patch.object(curator, "AUTHOR_READY_PATH", author_ready_path):
				self.assertEqual(1, curator.check(temp_root / "external-artifacts"))
			self.assertEqual(b"preserve this file", author_ready_path.read_bytes())
			self.assertFalse((temp_root / "external-artifacts").exists())

	def test_le_spatial_curator_write_refuses_to_clobber_or_create_conflicting_partial(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		try:
			curator = importlib.import_module("curate_avatar_le_spatial")
		finally:
			sys.path.pop(0)
		with tempfile.TemporaryDirectory() as root:
			temp_root = Path(root)
			partial_path = temp_root / "partial.json"
			knowledge_path = temp_root / "knowledge.md"
			author_ready_path = temp_root / "author-ready.json"
			partial_path.write_bytes(b"existing partial")
			knowledge_path.write_bytes(b"existing knowledge")
			author_ready_path.write_bytes(b"canonical author-ready bytes")
			before = {path: path.read_bytes() for path in (partial_path, knowledge_path, author_ready_path)}
			with patch.object(curator, "PARTIAL_PATH", partial_path), patch.object(curator, "KNOWLEDGE_PATH", knowledge_path), patch.object(curator, "AUTHOR_READY_PATH", author_ready_path):
				with self.assertRaisesRegex(RuntimeError, "author-ready artifact exists"):
					curator.curate(temp_root / "external-artifacts")
			self.assertEqual(before, {path: path.read_bytes() for path in before})
			self.assertFalse((temp_root / "external-artifacts").exists())

	def test_regular_avatar_generator_fails_before_creating_partial_conflict(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		try:
			generator = importlib.import_module("curate_avatar")
		finally:
			sys.path.pop(0)
		with tempfile.TemporaryDirectory() as root:
			author_ready_path = Path(root) / "avatar-le-author-ready.json"
			author_ready_path.write_bytes(b"canonical author-ready bytes")
			paths = [LE_PATH, PRO_PATH, ROOT / "knowledge" / "stern" / "avatar-limited-edition-2010.md"]
			before = {path: path.read_bytes() for path in paths}
			with patch.object(generator, "AUTHOR_READY_PATH", author_ready_path):
				with self.assertRaisesRegex(RuntimeError, "author-ready artifact exists"):
					generator.main()
			self.assertEqual(before, {path: path.read_bytes() for path in paths})

	def test_regular_avatar_generator_preserves_curated_pro_artifacts(self) -> None:
		sys.path.insert(0, str(ROOT / "tools"))
		try:
			generator = importlib.import_module("curate_avatar")
			le_curator = importlib.import_module("curate_avatar_le_spatial")
		finally:
			sys.path.pop(0)
		with tempfile.TemporaryDirectory() as root:
			author_ready_path = Path(root) / "missing-author-ready.json"
			with patch.object(generator, "AUTHOR_READY_PATH", author_ready_path), patch.object(generator, "write_json") as write_json_mock, patch.object(generator, "write_text") as write_text_mock, patch.object(le_curator, "curate") as le_curate_mock:
				generator.main()
			self.assertFalse(any(call.args[0] == PRO_PATH for call in write_json_mock.call_args_list))
			self.assertFalse(any(call.args[0] == PRO_KNOWLEDGE_PATH for call in write_text_mock.call_args_list))
			le_curate_mock.assert_called_once_with()

	def test_le_cabinet_controls_quantities_and_spatial_provenance_are_audited(self) -> None:
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		cabinet_inputs = {15, 16, 65, 66, 67, 68, 69, 84, 82, -7, -6, -5, -3, -2, -1, 0}
		self.assertEqual(cabinet_inputs, {address for address, device in inputs.items() if device.get("spatial", {}).get("reason") == "cabinet_or_service"})
		self.assertTrue(all(any(role.startswith(("cabinet.", "service.", "flipper.")) for role in inputs[address].get("roles", [])) for address in cabinet_inputs))
		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		self.assertEqual("cabinet.shaker", outputs[8]["roles"][0])
		self.assertEqual("cabinet.backpanel-flasher", outputs[21]["roles"][0])
		self.assertEqual(2, outputs[21]["physical"]["quantity"])
		self.assertEqual("cabinet.coin-meter", outputs[24]["roles"][0])
		self.assertEqual({20: 1, 21: 2, 22: 1, 23: 1, 25: 1, 26: 1, 27: 2, 28: 2, 29: 1, 30: 1, 31: 1, 32: 1}, {address: outputs[address]["physical"]["quantity"] for address in (20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32)})
		pro_geometry = {"vpx.avatar-pro-lw-vpumod-1.12", "vpx-table.avatar-pro.local-archive-2020", "vpx-table.avatar-pro.local-primary-2020"}
		for address in (41, 47, 48, 72):
			spatial_refs = {
				ref
				for placement in inputs[address].get("spatial", {}).get("placements", [])
				for ref in placement["provenance"]["source_refs"]
			}
			self.assertFalse(pro_geometry & spatial_refs)
		for address in (4, 12, 14, 27):
			self.assertNotIn("spatial", outputs[address])

	def test_each_promoted_coordinate_cites_the_candidate_that_contains_its_named_object(self) -> None:
		archive = "vpx-table.avatar-pro.local-archive-2020"
		primary = "vpx-table.avatar-pro.local-primary-2020"
		manual = "manual.avatar-pro-le.2010"
		inputs = bindings(self.le, "inputs", "pinmame.input.switch")
		primary_inputs = {2, 3, 4, 5, 17, 36, 37, 38, 39}
		located_inputs = {address for address, device in inputs.items() if device.get("spatial", {}).get("placements")}
		for address in located_inputs:
			expected_geometry = primary if address in primary_inputs else archive
			for placement in inputs[address]["spatial"]["placements"]:
				self.assertEqual([manual, expected_geometry], placement["provenance"]["source_refs"])

		outputs = bindings(self.le, "outputs", "pinmame.output.solenoid")
		archive_solenoids = {2, 3, 6, 7, 11, 15, 16}
		located_solenoids = {address for address, device in outputs.items() if device.get("spatial", {}).get("placements")}
		for address in located_solenoids:
			expected_geometry = archive if address in archive_solenoids else primary
			for placement in outputs[address]["spatial"]["placements"]:
				self.assertEqual([manual, expected_geometry], placement["provenance"]["source_refs"])

		lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		for device in lamps.values():
			for placement in device.get("spatial", {}).get("placements", []):
				self.assertEqual([manual, archive], placement["provenance"]["source_refs"])

	def test_spatial_source_locators_and_rendered_knowledge_are_followable(self) -> None:
		sources = {source["id"]: source for source in self.le["sources"]}
		self.assertTrue(sources["vpx-table.avatar-pro.local-primary-2020"]["uri"].endswith("/avatar 080116a mod 1.19.vpx"))
		knowledge = (ROOT / "knowledge" / "stern" / "avatar-limited-edition-2010.md").read_text(encoding="utf-8")
		self.assertFalse(any(line.startswith("\t") for line in knowledge.splitlines()))

	def test_editions_exhaustively_split_the_mixed_pinmame_clone_tree(self) -> None:
		pro = {driver["id"] for driver in self.pro["drivers"]}
		limited_edition = {driver["id"] for driver in self.le["drivers"]}
		self.assertEqual({"avr_106", "avr_110", "avr_200"}, pro)
		self.assertEqual({"avr_101h", "avr_120h"}, limited_edition)
		self.assertFalse(pro & limited_edition)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("avr_")}, pro | limited_edition)
		self.assertEqual(2010, self.pro["machine"]["year"])
		self.assertEqual(5618, self.pro["machine"]["ipdb_id"])
		self.assertEqual(5653, self.le["machine"]["ipdb_id"])
		self.assertEqual("I-00B6", self.le["machine"]["model_number"])

	def test_complete_matrix_dedicated_and_dip_address_spaces_are_explicit(self) -> None:
		expected_switches = set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1))
		for definition in (self.pro, self.le):
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(expected_switches, set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertTrue(switches[39]["normally_closed"])
			self.assertTrue(switches[83]["normally_closed"])
			self.assertTrue(switches[81]["normally_closed"])
			self.assertEqual("unused", switches[6]["availability"])

	def test_pro_and_le_switch_boundaries_are_not_blended(self) -> None:
		pro = bindings(self.pro, "inputs", "pinmame.input.switch")
		limited_edition = bindings(self.le, "inputs", "pinmame.input.switch")
		for address in (41, 47, 48, 72):
			self.assertEqual("unused", pro[address]["availability"])
			self.assertEqual("used", limited_edition[address]["availability"])
		self.assertEqual("Left ramp entrance", limited_edition[41]["label"])
		self.assertEqual("Transporter down", limited_edition[47]["label"])
		self.assertEqual("Transporter up", limited_edition[48]["label"])
		self.assertEqual("Alternate shooter-lane metal detector", limited_edition[72]["label"])
		self.assertFalse(limited_edition[72]["normally_closed"])
		self.assertIn("steel ball bridges", limited_edition[72]["physical"]["notes"])
		for address in (41, 47, 48, 72):
			self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", limited_edition[address]["provenance"]["source_refs"])

	def test_main_solenoids_game_on_and_auxiliary_capacity_are_explicit(self) -> None:
		for definition in (self.pro, self.le):
			outputs = bindings(definition, "outputs", "pinmame.output.solenoid")
			self.assertEqual(set(range(1, 34)) | set(range(51, 67)), set(outputs))
			self.assertEqual("virtual", outputs[33]["kind"])
			self.assertNotIn("wiring", outputs[33])
			self.assertTrue(all(outputs[address]["kind"] == "virtual" and outputs[address]["availability"] == "unused" for address in range(51, 67)))
			self.assertEqual("J9-P1", outputs[9]["wiring"]["control_connection"])
			self.assertEqual("J7-P4", outputs[19]["wiring"]["control_connection"])
			self.assertEqual("J7-P1", outputs[17]["wiring"]["power_connection"])
			self.assertEqual(20, outputs[17]["wiring"]["nominal_voltage_v"])
		pro = bindings(self.pro, "outputs", "pinmame.output.solenoid")
		limited_edition = bindings(self.le, "outputs", "pinmame.output.solenoid")
		for address in (4, 12, 14, 27):
			self.assertEqual("unused", pro[address]["availability"])
			self.assertEqual("used", limited_edition[address]["availability"])
			self.assertNotIn("power_wire", pro[address]["wiring"])
			self.assertNotIn("power_wire", limited_edition[address]["wiring"])
			self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", limited_edition[address]["provenance"]["source_refs"])
		self.assertEqual("optional", pro[8]["availability"])
		self.assertEqual("used", limited_edition[8]["availability"])
		self.assertEqual("optional", pro[24]["availability"])

	def test_lamp_matrix_and_general_illumination_are_complete(self) -> None:
		pro_lamps = bindings(self.pro, "outputs", "pinmame.output.lamp")
		le_lamps = bindings(self.le, "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 81)), set(pro_lamps))
		self.assertEqual(set(range(1, 81)), set(le_lamps))
		self.assertEqual({20, 25, 44, 45, 46} | set(range(65, 81)), {address for address, lamp in pro_lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual({25} | set(range(65, 81)), {address for address, lamp in le_lamps.items() if lamp["availability"] == "unused"})
		self.assertEqual("1X", le_lamps[20]["label"])
		self.assertEqual("8X", le_lamps[46]["label"])
		self.assertEqual("J13-P9", le_lamps[1]["wiring"]["drive_connection"])
		self.assertEqual("J12-P11", le_lamps[80]["wiring"]["return_connection"])
		self.assertEqual({"board": "I/O Power Driver board lamp matrix", "drive_connection": "J13-P7", "drive_wire": "YEL-ORG", "return_connection": "J12-P6", "return_wire": "RED-BLU"}, le_lamps[43]["wiring"])
		for definition in (self.pro, self.le):
			self.assertEqual({0}, set(bindings(definition, "outputs", "pinmame.output.gi")))

	def test_common_amp_bank_suit_and_link_lock_are_recreatable(self) -> None:
		for definition in (self.pro, self.le):
			mechanisms = {item["id"]: item for item in definition["mechanisms"]}
			bank = mechanisms["mechanism.amp-three-bank"]
			self.assertEqual(5, len(bank["sensors"]))
			self.assertIn("Z 25 to -24 in 25 steps", bank["behavior"])
			self.assertEqual(2, len(bank["positions"]))
			suit = mechanisms["mechanism.amp-suit"]
			self.assertEqual(2, len(suit["actuators"]))
			self.assertEqual(2, len(suit["positions"]))
			self.assertIn("Switch 57 is the down endpoint and 58 the up endpoint", suit["behavior"])
			link = mechanisms["mechanism.link-lock"]
			self.assertEqual(2, len(link["actuators"]))
			self.assertIn("physical barriers", link["behavior"])
		pro_mechanisms = {item["id"]: item for item in self.pro["mechanisms"]}
		le_mechanisms = {item["id"]: item for item in self.le["mechanisms"]}
		self.assertNotIn("Exact LE service evidence", pro_mechanisms["mechanism.amp-three-bank"]["behavior"])
		self.assertNotIn("Exact LE service evidence", pro_mechanisms["mechanism.amp-suit"]["behavior"])
		self.assertIn("Exact LE service evidence", le_mechanisms["mechanism.amp-three-bank"]["behavior"])
		self.assertIn("Exact LE service evidence", le_mechanisms["mechanism.amp-suit"]["behavior"])

	def test_le_transporter_marching_legs_and_ceramic_ball_are_distinct_mechanisms(self) -> None:
		pro = {item["id"]: item for item in self.pro["mechanisms"]}
		limited_edition = {item["id"]: item for item in self.le["mechanisms"]}
		for mechanism_id in ("mechanism.transporter", "mechanism.amp-marching-legs", "mechanism.ceramic-ball"):
			self.assertNotIn(mechanism_id, pro)
			self.assertIn(mechanism_id, limited_edition)
		transporter = limited_edition["mechanism.transporter"]
		self.assertEqual(1, len(transporter["actuators"]))
		self.assertEqual(2, len(transporter["positions"]))
		self.assertIn("single motor is polarity-reversed", transporter["behavior"])
		self.assertIn("there is no second public motor output", transporter["behavior"])
		legs = limited_edition["mechanism.amp-marching-legs"]
		self.assertEqual(2, len(legs["actuators"]))
		self.assertIn("alternating leg movement", legs["behavior"])
		self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", legs["provenance"]["source_refs"])
		self.assertNotIn("vpx.avatar-pro-lw-vpumod-1.12", transporter["provenance"]["source_refs"])
		ceramic = limited_edition["mechanism.ceramic-ball"]
		self.assertIn("three steel balls and one ceramic", ceramic["behavior"])
		self.assertIn("Preserve per-ball material identity", ceramic["behavior"])

	def test_exact_manual_script_rom_and_runtime_hashes_are_pinned(self) -> None:
		for definition in (self.pro, self.le):
			sources = {source["id"]: source for source in definition["sources"]}
			self.assertEqual("afaed95b1b3406193a234a4afa579f15bc5bb3c4cd92859def4ad7b202fab04b", sources["manual.avatar-pro-le.2010"]["sha256"])
			self.assertEqual("8fc8cb6ce0c02af97feb69f3271dce02b5531c79ead4171f614a4bc02614db29", sources["vpx.avatar-pro-lw-vpumod-1.12"]["sha256"])
			self.assertEqual("8ddff84ad8f5c8c6f583153f058458ed17bdd6fbafe60304fa2621920872590e", sources["vpx-table.avatar-pro.vpuniverse-4755"]["sha256"])
		self.assertEqual("576f70929705761a78a0272a6fb72cd17656e0feb75cccb904a4080e7e5b9bd7", self.pro_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("d4d289134836b9e352b32aa8d75fc192b702d9d44580c9389fd38319137ca8e7", self.pro_evidence["runtime"]["raw_runs"][0]["sha256"])
		self.assertEqual("264a1ad74e2d247b212837951d9528910ee9b6a127a5eaaac51dcd6572344269", self.le_evidence["runtime"]["rom_archive_sha256"])
		self.assertEqual("6d00f26380ed4c71b7a921a38fe241bf3a675e472be884c742ee35ac4e8f99e8", self.le_evidence["runtime"]["raw_runs"][0]["sha256"])

	def test_corrected_runtime_snapshots_do_not_invent_sam_outputs_34_to_36(self) -> None:
		for evidence in (self.pro_evidence, self.le_evidence):
			observations = evidence["runtime"]["observations"]
			self.assertEqual([33], observations["solenoid_addresses_seen"])
			self.assertFalse({34, 35, 36} & set(observations["solenoid_addresses_seen"]))
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], observations["display_layouts_seen"])
			self.assertEqual({1} | set(range(3, 25)) | set(range(26, 65)), set(observations["lamp_addresses_seen"]))

	def test_le_mechanism_diagnostics_record_both_transporter_directions_and_amp_motion(self) -> None:
		expected = {
			"transporter-up-to-down": ("77ba0cab5d2cfa5c77b5e205d65a091dcdc9f5bdcddcd2886a75ff08dbb1c7dc", {14}),
			"transporter-down-to-up": ("761ba656664c40c8fe7f71c1203142c6b50a452a416bfa48dcf614edc546b628", {14}),
			"amp-suit-motor": ("0dc74feaa609f588691138a9907d5261615fccbb334ed8d77a724a240c126881", {13, 14, 19}),
			"three-bank-motor": ("b5e62835a39af924b757d9f2cac6f73312c149c668699f5882ca1ea932cf901a", {5, 14}),
		}
		self.assertEqual(set(expected), set(self.le_diagnostics))
		for name, evidence in self.le_diagnostics.items():
			run = evidence["runtime"]["raw_runs"][0]
			self.assertEqual(expected[name][0], run["sha256"])
			self.assertEqual(expected[name][0], evidence["source"]["sha256"])
			self.assertEqual(expected[name][1], set(evidence["runtime"]["observations"]["solenoid_addresses_seen"]))
			self.assertEqual("runtime_scenario", evidence["source"]["kind"])
			self.assertNotIn("<mechanism-endpoint-initial-switches>", evidence["runtime"]["command_template"])
			self.assertNotIn("<service-menu-pulses>", evidence["runtime"]["command_template"])
			snapshot = evidence["runtime"]["observations"]["diagnostic_snapshots"][0]
			self.assertEqual(64, len(snapshot["pixel_sha256"]))
			self.assertTrue(snapshot["interpreted_text"])
		self.assertEqual([], self.le_diagnostics["transporter-up-to-down"]["runtime"]["observations"]["diagnostic_snapshots"][0]["active_solenoid_addresses"])
		self.assertEqual([14], self.le_diagnostics["transporter-down-to-up"]["runtime"]["observations"]["diagnostic_snapshots"][0]["active_solenoid_addresses"])
		self.assertIn("MOVING TO SWITCH #57", self.le_diagnostics["amp-suit-motor"]["runtime"]["observations"]["diagnostic_snapshots"][0]["interpreted_text"])
		self.assertIn("MOVING TO SWITCH #45", self.le_diagnostics["three-bank-motor"]["runtime"]["observations"]["diagnostic_snapshots"][0]["interpreted_text"])

	def test_all_bindings_semantic_ids_and_mechanism_actuator_owners_are_unique(self) -> None:
		for definition in (self.pro, self.le):
			for collection in (definition["inputs"], definition["outputs"]):
				bindings_seen = [(item["binding"]["group"], item["binding"]["device"]) for item in collection]
				self.assertEqual(len(bindings_seen), len(set(bindings_seen)))
				ids = [item["id"] for item in collection]
				self.assertEqual(len(ids), len(set(ids)))
			actuators = [actuator for mechanism in definition["mechanisms"] for actuator in mechanism["actuators"]]
			self.assertEqual(len(actuators), len(set(actuators)))


if __name__ == "__main__":
	unittest.main()
