from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "stern" / "ali-seven-digit-conversion-2023.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "stern" / "ali-service-diagnostics.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def manual_alias(device: dict[str, object]) -> str:
	return next(alias["value"] for alias in device["aliases"] if alias["namespace"] == "manual.address")


class AliConversionDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_both_conversion_roots_share_one_physical_definition(self) -> None:
		self.assertEqual("physical_conversion", self.definition["machine"]["kind"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual({"alib", "alic"}, {driver["id"] for driver in self.definition["drivers"]})
		self.assertTrue(all(driver["physical_compatibility"] == "identical" for driver in self.definition["drivers"]))

	def test_complete_switch_matrix_and_cabinet_inputs_are_explicit(self) -> None:
		public_switches = {
			item["binding"]["device"]: item
			for item in self.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		self.assertEqual(set(range(-7, -4)) | set(range(1, 41)) | set(range(81, 85)), set(public_switches))
		self.assertEqual("Top-left spinner", public_switches[9]["label"])
		self.assertEqual(2, public_switches[11]["physical"]["quantity"])
		self.assertEqual({4, 10, 17, 18, 40}, {address for address in range(1, 41) if public_switches[address]["availability"] == "unused"})
		self.assertEqual(32, sum(item["kind"] == "dip_switch" for item in self.definition["inputs"]))
		self.assertEqual(2, sum(item["binding"]["group"] == "physical.input.direct" for item in self.definition["inputs"]))

	def test_service_solenoid_numbers_map_to_public_callbacks(self) -> None:
		outputs = {
			manual_alias(item): item["binding"]["device"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid" and manual_alias(item).isdigit()
		}
		expected = {"1": 2, "2": 1, "3": 6, "4": 7, "5": 3, "6": 4, "7": 5, "8": 8, "9": 11, "10": 12, "11": 14, "12": 13, "13": 9, "14": 10, "15": 19, "16": 15, "17": 17, "18": 20, "19": 18}
		self.assertEqual(expected, outputs)
		public_addresses = {
			item["binding"]["device"]
			for item in self.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}
		self.assertNotIn(16, public_addresses)
		self.assertTrue({46, 48}.issubset(public_addresses))

	def test_all_sixty_discrete_lamp_scrs_are_mapped(self) -> None:
		lamps = [item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"]
		addresses = {item["binding"]["device"] for item in lamps}
		expected = set(range(1, 64)) - {16, 32, 48}
		self.assertEqual(expected, addresses)
		unused_q = {manual_alias(item) for item in lamps if item["availability"] == "unused"}
		self.assertEqual({"Q01", "Q20", "Q24", "Q25", "Q54", "Q58"}, unused_q)
		self.assertTrue(all("Lamp Driver module LDA-100" in item["wiring"]["board"] for item in lamps))

	def test_custom_ball_devices_capture_shared_and_passive_behavior(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		top = mechanisms["mechanism.top-three-saucers"]
		self.assertEqual(3, len(top["sensors"]))
		self.assertEqual(["device.top-three-saucer-eject"], top["actuators"])
		self.assertIn("200 ms", top["behavior"])
		self.assertEqual([], mechanisms["mechanism.middle-left-passive-saucer"]["actuators"])
		self.assertIn("one ball", mechanisms["mechanism.outhole"]["behavior"].lower())

	def test_display_conversion_is_not_merged_with_six_digit_parent(self) -> None:
		widths = [display["width"] for display in self.definition["displays"]]
		self.assertEqual([7, 7, 7, 7, 2, 2], widths)

	def test_runtime_evidence_keeps_external_rom_and_run_hashes(self) -> None:
		runtime = self.evidence["runtime"]
		self.assertEqual("bf0edc82cdfcfbcc354faff3b2cf668a11f0aac53e7affd915e44136e3325a4b", runtime["rom_archive_sha256"])
		self.assertEqual([16, 32, 48, 64], runtime["observations"]["lamp_decoder_holes_not_seen"])
		self.assertEqual(2, runtime["observations"]["physical_service_solenoid_to_public"]["1"])
		self.assertEqual(18, runtime["observations"]["physical_service_solenoid_to_public"]["19"])
		self.assertEqual(2, len(runtime["raw_runs"]))

	def test_manual_script_table_and_harness_are_hash_anchored(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual("455ea85f99eff031ffcca75489ab4dfea0a587a864522fb2fa30a4bfd160d78b", sources["manual.ali.tech-chart"]["sha256"])
		self.assertEqual("6dbde0131a367c643ae87fe511052d28d83ed0cb6b74b87ba731a900678f1849", sources["vpx.ali.jp-salas.1.0.1"]["sha256"])
		self.assertEqual("14137b288aee843e834f509b467dd288fcf0e3269afcbd397e2276d31c24533f", sources["vpx-table.ali.jp-salas.1.0.1"]["sha256"])
		self.assertEqual("cb14917ee85f7b86b1c4c61b4b9c147c8e7909a97e52e21f2dfe237ac35219bf", sources["runtime.ali.service-solenoid-test"]["sha256"])


if __name__ == "__main__":
	unittest.main()
