from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "revenge-from-mars-1999.json"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "p2k.json"
EXCERPT_PATH = ROOT / "evidence" / "excerpts" / "bally.revenge-from-mars.1999" / "operations-manual-service-tables.md"
RFM_DRIVERS = {
	"rfm_120", "rfm_140", "rfm_150", "rfm_160", "rfm_180", "rfm_190", "rfm_191", "rfm_195",
	"rfm_200", "rfm_210", "rfm_222", "rfm_223", "rfm_224", "rfm_250", "rfm_260",
}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class RevengeFromMarsDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.controller = load_json(CONTROLLER_PATH)

	def test_identity_controller_and_driver_family(self) -> None:
		self.assertEqual(
			{"id": "bally.revenge-from-mars.1999", "name": "Revenge from Mars", "manufacturer": "Bally", "year": 1999, "kind": "physical_pinball", "model_number": "50070", "ipdb_id": 4446},
			self.definition["machine"],
		)
		self.assertEqual("pinmame.p2k", self.definition["controller"]["platform"])
		self.assertEqual("0x8000000000000", self.definition["controller"]["hardware_generation"])
		self.assertEqual(RFM_DRIVERS, {driver["id"] for driver in self.definition["drivers"]})

	def test_controller_exposes_only_the_p2k_public_ranges(self) -> None:
		groups = {group["id"]: group for group in self.controller["groups"]}
		self.assertEqual({"pinmame.input.switch", "pinmame.output.solenoid", "pinmame.output.lamp"}, set(groups))
		self.assertEqual([{"minimum": 0, "maximum": 127}], groups["pinmame.output.lamp"]["address_rules"])
		self.assertEqual(
			[{"minimum": 1, "maximum": 32}, {"minimum": 45, "maximum": 48}, {"minimum": 51, "maximum": 62}],
			groups["pinmame.output.solenoid"]["address_rules"],
		)

	def test_all_switch_driver_and_lamp_positions_are_explicit(self) -> None:
		inputs = {item["binding"]["device"]: item for item in self.definition["inputs"]}
		expected_inputs = {column * 10 + row for column in range(1, 9) for row in range(1, 9)} | set(range(91, 99)) | set(range(101, 109)) | set(range(111, 119))
		self.assertEqual(expected_inputs, set(inputs))
		self.assertEqual(88, len(inputs))
		self.assertEqual({53, 54, 55, 56}, {address for address, item in inputs.items() if item["availability"] == "optional"})
		self.assertEqual({41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56}, {address for address, item in inputs.items() if item.get("normally_closed")})
		self.assertTrue(all("normally_closed" not in item for address, item in inputs.items() if address not in {41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56}))

		solenoids = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.solenoid"}
		self.assertEqual(set(range(1, 33)) | set(range(45, 49)) | set(range(51, 63)), set(solenoids))
		self.assertEqual("Right Flipper Power", solenoids[45]["label"])
		self.assertEqual("Lock Diverter Power", solenoids[51]["label"])
		self.assertEqual("Ticket Dispenser (Optional)", solenoids[62]["label"])

		lamps = {item["binding"]["device"]: item for item in self.definition["outputs"] if item["binding"]["group"] == "pinmame.output.lamp"}
		self.assertEqual(set(range(128)), set(lamps))
		self.assertEqual("Start Button", lamps[2]["label"])
		self.assertEqual("Right Slingshot Spotlight", lamps[15]["label"])
		self.assertEqual("Left Slingshot Spotlight", lamps[31]["label"])
		self.assertEqual("11A", next(alias["value"] for alias in lamps[0]["aliases"] if alias["namespace"] == "manual.address"))
		self.assertEqual("88B", next(alias["value"] for alias in lamps[127]["aliases"] if alias["namespace"] == "manual.address"))

	def test_video_contract_preserves_the_line_doubled_export(self) -> None:
		self.assertEqual(
			[{"id": "display.pinball-2000-video", "label": "Pinball 2000 reflected playfield video", "kind": "video", "controller_index": 0, "width": 640, "height": 480, "spatial": {"status": "not_applicable", "reason": "cabinet_or_service", "provenance": {"status": "validated", "source_refs": ["pinmame.core.8371478a7640"]}}, "provenance": {"status": "validated", "source_refs": ["pinmame.core.8371478a7640"]}}],
			self.definition["displays"],
		)

	def test_manual_and_rejected_vpx_are_content_locked(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertEqual("6ba2c0728d26e379d1e1a0b2a2ff5eb40f61fce2d38c45e0e4f094166df0b9df", sources["manual.rfm.operations-1999"]["sha256"])
		self.assertEqual("9a5415a3b6b5a57b01749415789019fe7037a828e9ab691ce64cd1720b2294be", sources["vpx-table.attack-and-revenge-v600-rejected"]["sha256"])
		self.assertFalse(sources["vpx-table.attack-and-revenge-v600-rejected"]["known_working"])
		self.assertIn("cGameName=afm_113b", sources["vpx-table.attack-and-revenge-v600-rejected"]["locator"])
		self.assertEqual("e283b2b47f41ebe5c5464d2cda49df531d069dc57db8e91f29c12c9ef90c663b", hashlib.sha256(EXCERPT_PATH.read_bytes()).hexdigest())

	def test_only_resolved_manual_lamp_disagreement_is_retained(self) -> None:
		self.assertEqual(1, len(self.definition["conflicts"]))
		conflict = self.definition["conflicts"][0]
		self.assertEqual("ignored", conflict["status"])
		self.assertIn("18B", conflict["description"])
		self.assertIn("28B", conflict["description"])


if __name__ == "__main__":
	unittest.main()
