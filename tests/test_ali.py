from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "ali-1980.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "stern" / "ali-service-diagnostics.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def manual_alias(device: dict[str, object]) -> str:
	return next(alias["value"] for alias in device["aliases"] if alias["namespace"] == "manual.address")


class AliDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)

	def test_physical_family_contains_stock_clone_and_conversion_roots(self) -> None:
		self.assertEqual({"id": "stern.ali.1980", "name": "Ali", "manufacturer": "Stern", "year": 1980, "kind": "physical_pinball", "ipdb_id": 43, "opdb_id": "G43kO-MQ50p"}, self.definition["machine"])
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("unknown", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertTrue(all(state == "validated" for dimension, state in self.definition["coverage"]["dimensions"].items() if dimension != "spatial_placement"))
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual({"ali", "alifp", "alib", "alic"}, set(drivers))
		self.assertNotIn("clone_of", drivers["ali"])
		self.assertEqual("ali", drivers["alifp"]["clone_of"])
		self.assertNotIn("clone_of", drivers["alib"])
		self.assertNotIn("clone_of", drivers["alic"])
		self.assertEqual(("1980", "Stern", "identical"), tuple(drivers["ali"][key] for key in ("year", "manufacturer", "physical_compatibility")))
		self.assertEqual(("1980", "Stern", "identical"), tuple(drivers["alifp"][key] for key in ("year", "manufacturer", "physical_compatibility")))
		self.assertEqual(("2023", "Stern / Idleman", "compatible"), tuple(drivers["alib"][key] for key in ("year", "manufacturer", "physical_compatibility")))
		self.assertEqual(("2023", "Stern / slochar", "compatible"), tuple(drivers["alic"][key] for key in ("year", "manufacturer", "physical_compatibility")))
		self.assertIn("not a separately manufactured game", drivers["alib"]["variant_notes"])

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

	def test_stock_display_inventory_has_explicit_conversion_overrides(self) -> None:
		displays = {display["id"]: display for display in self.definition["displays"]}
		self.assertEqual(
			{
				"display.player-1": (0, 2, 6),
				"display.player-2": (1, 10, 6),
				"display.player-3": (2, 18, 6),
				"display.player-4": (3, 26, 6),
				"display.credits": (4, 35, 2),
				"display.ball-match": (5, 38, 2),
			},
			{display_id: (display["controller_index"], display["segment_start"], display["width"]) for display_id, display in displays.items()},
		)
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("display_overrides", drivers["ali"])
		self.assertNotIn("display_overrides", drivers["alifp"])
		for driver_id in ("alib", "alic"):
			overrides = {override["target"]: override for override in drivers[driver_id]["display_overrides"]}
			self.assertEqual(
				{
					"display.player-1": (1, 7),
					"display.player-2": (9, 7),
					"display.player-3": (17, 7),
					"display.player-4": (25, 7),
				},
				{target: (override["segment_start"], override["width"]) for target, override in overrides.items()},
			)
			self.assertTrue(all("controller_index" not in override for override in overrides.values()))
			self.assertTrue(all(override["provenance"]["source_refs"] == ["pinmame.core.4ec52ff0ac13"] for override in overrides.values()))

	def test_runtime_evidence_keeps_external_rom_and_run_hashes(self) -> None:
		self.assertEqual(["ali"], self.evidence["driver_ids"])
		self.assertEqual(["stern.ali.1980"], self.evidence["machine_ids"])
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
		manual = sources["manual.ali.tech-chart"]
		self.assertEqual(3, len(manual["excerpts"]))
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), path)
			self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["id"])
			self.assertTrue((ROOT / excerpt["image"]).is_file(), excerpt["id"])
			self.assertTrue(excerpt["reviewed"])


if __name__ == "__main__":
	unittest.main()
