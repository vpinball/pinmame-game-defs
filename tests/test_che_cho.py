from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "watacaractr" / "cheech-chong-road-trippin-2021.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "wpc" / "che-cho-gameplay.json"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-alpha.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class CheechChongDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.evidence = load_json(EVIDENCE_PATH)
		cls.controller = load_json(CONTROLLER_PATH)

	def test_virtual_original_is_author_ready_without_physical_wiring(self) -> None:
		self.assertEqual("virtual_pinball", self.definition["machine"]["kind"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual("not_applicable", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual(["che_cho"], [driver["id"] for driver in self.definition["drivers"]])

	def test_complete_public_input_spaces_are_explicit(self) -> None:
		inputs = self.definition["inputs"]
		switches = {
			item["binding"]["device"]: item
			for item in inputs
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		expected_matrix = {row * 10 + column for row in range(1, 9) for column in range(1, 9)}
		self.assertEqual(set(range(1, 9)) | expected_matrix | set(range(111, 119)), set(switches))
		self.assertEqual(8, sum(item["binding"]["group"] == "pinmame.input.dip" for item in inputs))
		self.assertEqual("Start button", switches[13]["label"])
		self.assertEqual("Shooter lane", switches[75]["label"])
		self.assertEqual("unused", switches[23]["availability"])
		self.assertEqual("unused", switches[118]["availability"])

	def test_all_controller_outputs_are_explicit(self) -> None:
		outputs = self.definition["outputs"]
		by_group = {
			group: {item["binding"]["device"]: item for item in outputs if item["binding"]["group"] == group}
			for group in ("pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi")
		}
		self.assertEqual(set(range(1, 51)), set(by_group["pinmame.output.solenoid"]))
		self.assertEqual({row * 10 + column for row in range(1, 9) for column in range(1, 9)}, set(by_group["pinmame.output.lamp"]))
		self.assertEqual(set(range(5)), set(by_group["pinmame.output.gi"]))
		self.assertEqual({17, 18, 21, 22, 83, 84}, {address for address, item in by_group["pinmame.output.lamp"].items() if item["availability"] == "unused"})
		self.assertEqual("Game-on state and flipper-enable relay", by_group["pinmame.output.solenoid"][31]["label"])
		self.assertEqual("Lower-right flipper coil callback", by_group["pinmame.output.solenoid"][46]["label"])
		self.assertEqual("Lower-left and upper-left flipper coil callback", by_group["pinmame.output.solenoid"][48]["label"])

	def test_target_and_rollover_lamp_relationships_match_runtime_proof(self) -> None:
		observations = self.evidence["runtime"]["observations"]
		expected = {str(switch): lamp for switch, lamp in zip((31, 32, 33, 34, 41, 42, 43), (41, 42, 43, 44, 56, 57, 58))}
		expected |= {str(switch): lamp for switch, lamp in zip((51, 52, 53, 54, 55, 56), (23, 24, 25, 26, 27, 28))}
		expected |= {str(switch): lamp for switch, lamp in zip((57, 58, 61, 62, 63, 64, 65, 66), (31, 32, 33, 34, 35, 36, 37, 38))}
		self.assertEqual(expected, observations["switch_to_lamp"])
		lamps = {item["binding"]["device"]: item["label"] for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual(["A", "N", "D", "T", "H", "E"], [lamps[address][-1] for address in range(23, 29)])
		self.assertEqual(["P", "E", "D", "R", "O", "M", "A", "N"], [lamps[address][-1] for address in range(31, 39)])

	def test_displays_and_recreation_mechanisms_are_complete(self) -> None:
		self.assertEqual([(16, "segment"), (16, "segment")], [(display["width"], display["kind"]) for display in self.definition["displays"]])
		mechanisms = {mechanism["id"]: mechanism for mechanism in self.definition["mechanisms"]}
		self.assertTrue({
			"mechanism.trough",
			"mechanism.and-drop-bank",
			"mechanism.the-drop-bank",
			"mechanism.road-closed",
			"mechanism.motorcycle-cop",
			"mechanism.van-transfer",
			"mechanism.flippers",
		}.issubset(mechanisms))
		self.assertEqual([], mechanisms["mechanism.road-closed"]["actuators"])
		self.assertEqual([], mechanisms["mechanism.motorcycle-cop"]["actuators"])
		self.assertEqual([], mechanisms["mechanism.van-transfer"]["sensors"])
		self.assertEqual([], mechanisms["mechanism.van-transfer"]["actuators"])

	def test_runtime_evidence_is_hash_anchored_and_keeps_rom_external(self) -> None:
		runtime = self.evidence["runtime"]
		self.assertEqual("34d1f6a3fc31b988fe4c0a38904df2d533e3cb0735995134d113dcb7f96157c2", runtime["rom_archive_sha256"])
		self.assertNotIn("rom_bytes", runtime)
		self.assertEqual(5, len(runtime["observations"]["gi_addresses_seen"]))
		self.assertEqual(21, len(runtime["observations"]["switch_to_lamp"]))
		self.assertEqual({"game_on": 31, "trough_eject": 2}, runtime["observations"]["named_output_addresses"])

	def test_controller_profile_exposes_wpc_alpha_public_ranges(self) -> None:
		groups = {group["id"]: group for group in self.controller["groups"]}
		def ranges(group: dict[str, object]) -> list[list[int]]:
			return [[rule["minimum"], rule["maximum"]] for rule in group["address_rules"]]

		self.assertEqual([[1, 8], [11, 18], [21, 28], [31, 38], [41, 48], [51, 58], [61, 68], [71, 78], [81, 88], [111, 118]], ranges(groups["pinmame.input.switch"]))
		self.assertEqual([[1, 50]], ranges(groups["pinmame.output.solenoid"]))
		self.assertEqual([[0, 4]], ranges(groups["pinmame.output.gi"]))

	def test_stub_was_replaced_by_the_curated_definition(self) -> None:
		self.assertFalse((ROOT / "machines" / "stubs" / "che_cho.json").exists())
		self.assertFalse((ROOT / "knowledge" / "stubs" / "che_cho.md").exists())


if __name__ == "__main__":
	unittest.main()
