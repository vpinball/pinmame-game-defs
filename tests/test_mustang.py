from __future__ import annotations

import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PREMIUM_PATH = REPOSITORY_ROOT / "machines" / "partial" / "stern" / "mustang-premium-limited-edition-boss-2014.json"
PRO_PATH = REPOSITORY_ROOT / "machines" / "partial" / "stern" / "mustang-pro-2014.json"


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

	def test_both_working_script_validated_editions_are_fail_closed_for_spatial_retrofit(self) -> None:
		self.assertEqual(2, self.premium["schema_version"])
		self.assertEqual("partial", self.premium["coverage"]["status"])
		self.assertIn("spatial_placement", self.premium["coverage"]["missing"])
		self.assertEqual(2, self.pro["schema_version"])
		self.assertEqual("partial", self.pro["coverage"]["status"])
		self.assertIn("spatial_placement", self.pro["coverage"]["missing"])
		self.assertEqual(6098, self.pro["machine"]["ipdb_id"])

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
		self.assertTrue(all(lamps[address]["availability"] == "unused" for address in (80, 98, 99, 100, 101)))

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
		self.assertIn("asserted both posts rise", mechanisms["mechanism.orbit-post"]["behavior"])
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
		pro_script = next(source for source in self.pro["sources"] if source["id"] == "vpx.mustang-pro-85vett-gtxjoe-1.0")
		pro_table = next(source for source in self.pro["sources"] if source["id"] == "vpx-table.mustang-pro-85vett-gtxjoe-1.0")
		pro_runtime = next(source for source in self.pro["sources"] if source["id"] == "runtime.mustang-pro.boot-start")
		self.assertEqual("4ddf63df5b96e20da501ae336948e877473d21a4eeaf118a58bb7fcba9105a00", pro_script["sha256"])
		self.assertEqual("3ff72f7f2c58064f96991f8284a16ac2da90c369c217e878cb8603660ffc1b3c", pro_table["sha256"])
		self.assertEqual("c5002a38d3a392aec6e0160e1cd7988917e38e6118e375ef8e7f03e8d9b7bfe2", pro_runtime["sha256"])
		self.assertTrue((REPOSITORY_ROOT / "evidence" / "runtime" / "sam" / "mustang-pro-boot-start.json").is_file())


if __name__ == "__main__":
	unittest.main()
