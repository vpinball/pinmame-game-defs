from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATHS = {
	"premium": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-premium-limited-edition-luci-2012.json",
	"pro": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-pro-2012.json",
	"led_pro": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-led-pro-2014.json",
	"vault": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-vault-edition-2018.json",
	"american": ROOT / "machines" / "author-ready" / "virtual" / "american-country-2024.json",
}
PREMIUM_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "ac-dc-premium-boot-start.json"
PRO_EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "sam" / "ac-dc-pro-boot-start.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


class AcDcDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definitions = {name: load_json(path) for name, path in DEFINITION_PATHS.items()}
		cls.premium_evidence = load_json(PREMIUM_EVIDENCE_PATH)
		cls.pro_evidence = load_json(PRO_EVIDENCE_PATH)

	def test_all_five_products_are_author_ready(self) -> None:
		for definition in self.definitions.values():
			self.assertEqual("author_ready", definition["coverage"]["status"])
			self.assertEqual([], definition["coverage"]["missing"])
			self.assertTrue(all(value == "validated" for value in definition["coverage"]["dimensions"].values()))
			self.assertEqual("complete", definition["knowledge"]["status"])

	def test_driver_family_is_split_without_overlap_or_omission(self) -> None:
		expected = {
			"premium": {"acd_150h", "acd_152h", "acd_160h", "acd_161h", "acd_163h", "acd_165h", "acd_168h", "acd_168hc", "acd_170h", "acd_170hc"},
			"pro": {"acd_121", "acd_125", "acd_130", "acd_140", "acd_150", "acd_152", "acd_160", "acd_161", "acd_163", "acd_165"},
			"led_pro": {"acd_168", "acd_168c"},
			"vault": {"acd_170", "acd_170c"},
			"american": {"acd_170_ac"},
		}
		seen: set[str] = set()
		for name, definition in self.definitions.items():
			drivers = {driver["id"] for driver in definition["drivers"]}
			self.assertEqual(expected[name], drivers)
			self.assertFalse(seen & drivers)
			seen.update(drivers)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual({driver["id"] for driver in catalog["drivers"] if driver["id"].startswith("acd_")}, seen)

	def test_every_controller_address_space_is_explicit(self) -> None:
		for definition in self.definitions.values():
			switches = bindings(definition, "inputs", "pinmame.input.switch")
			self.assertEqual(set(range(1, 73)) | set(range(81, 89)) | set(range(-7, 1)), set(switches))
			self.assertEqual(set(range(1, 9)), set(bindings(definition, "inputs", "pinmame.input.dip")))
			self.assertEqual(96, len(definition["inputs"]))
			self.assertEqual(set(range(1, 81)), set(bindings(definition, "outputs", "pinmame.output.lamp")) & set(range(1, 81)))
			self.assertEqual({0}, set(bindings(definition, "outputs", "pinmame.output.gi")))

	def test_edition_specific_bell_and_lamp_deltas_are_locked(self) -> None:
		pro_switches = bindings(self.definitions["pro"], "inputs", "pinmame.input.switch")
		led_switches = bindings(self.definitions["led_pro"], "inputs", "pinmame.input.switch")
		vault_switches = bindings(self.definitions["vault"], "inputs", "pinmame.input.switch")
		premium_switches = bindings(self.definitions["premium"], "inputs", "pinmame.input.switch")
		self.assertEqual("Hell's Bell standup target", pro_switches[36]["label"])
		self.assertIn("Swinging Hell's Bell", led_switches[36]["label"])
		self.assertIn("Swinging Hell's Bell", vault_switches[36]["label"])
		self.assertEqual("Swinging bell score opto", premium_switches[47]["label"])
		for name in ("pro", "led_pro"):
			lamps = bindings(self.definitions[name], "outputs", "pinmame.output.lamp")
			self.assertTrue(all(lamps[address]["availability"] == "used" for address in (14, 15, 17)))
			self.assertTrue(all("VPX playfield insert" in lamps[address]["label"] for address in (14, 15, 17)))
		vault_lamps = bindings(self.definitions["vault"], "outputs", "pinmame.output.lamp")
		self.assertTrue(all(vault_lamps[address]["availability"] == "unused" for address in (14, 15, 17)))
		self.assertTrue(all("Removed Vault Edition insert" in vault_lamps[address]["label"] for address in (14, 15, 17)))

	def test_premium_auxiliary_board_uses_public_addresses_and_manual_aliases(self) -> None:
		solenoids = bindings(self.definitions["premium"], "outputs", "pinmame.output.solenoid")
		self.assertTrue(set(range(51, 59)).issubset(solenoids))
		for public, physical in zip(range(51, 59), range(41, 49)):
			manual_alias = next(alias["value"] for alias in solenoids[public]["aliases"] if alias["namespace"] == "manual.address")
			self.assertEqual(str(physical), manual_alias)
			self.assertEqual("Auxiliary 8-coil board", solenoids[public]["wiring"]["board"])
		self.assertEqual("Animated band members", solenoids[51]["label"])
		self.assertEqual("Cannon eject / fire", solenoids[53]["label"])
		self.assertEqual("Swinging-bell magnet", solenoids[54]["label"])
		self.assertEqual("Left-ramp crossover diverter", solenoids[57]["label"])

	def test_sam_game_on_and_physical_ticket_service_are_not_conflated(self) -> None:
		for definition in self.definitions.values():
			solenoids = bindings(definition, "outputs", "pinmame.output.solenoid")
			self.assertEqual("virtual", solenoids[33]["kind"])
			self.assertNotIn("wiring", solenoids[33])
			ticket = bindings(definition, "outputs", "physical.output.ticket")
			self.assertEqual({33, 34, 35}, set(ticket))
			self.assertTrue(all("wiring" not in output for output in ticket.values()))

	def test_premium_extended_lamps_follow_public_bgr_and_gi_contract(self) -> None:
		lamps = bindings(self.definitions["premium"], "outputs", "pinmame.output.lamp")
		self.assertEqual(set(range(1, 161)), set(lamps))
		self.assertEqual(["Face mouth RGB blue", "Face mouth RGB green", "Face mouth RGB red"], [lamps[address]["label"] for address in range(81, 84)])
		self.assertEqual(["Bell arrow (top) RGB blue", "Bell arrow (top) RGB green", "Bell arrow (top) RGB red"], [lamps[address]["label"] for address in range(84, 87)])
		self.assertTrue(all(lamps[address]["availability"] == "unused" for address in (114, 115, 116, 129)))
		self.assertEqual({130, 132, 134, 136}, {address for address, item in lamps.items() if 129 <= address <= 150 and item["kind"] == "gi"})
		self.assertEqual(set(range(151, 159)), {address for address, item in lamps.items() if "flame-tunnel" in item["label"]})
		self.assertFalse(set(range(177, 192)) & set(lamps))

	def test_custom_mechanisms_capture_sensors_actuators_and_passive_bell(self) -> None:
		premium = {mechanism["id"]: mechanism for mechanism in self.definitions["premium"]["mechanisms"]}
		pro = {mechanism["id"]: mechanism for mechanism in self.definitions["pro"]["mechanisms"]}
		led = {mechanism["id"]: mechanism for mechanism in self.definitions["led_pro"]["mechanisms"]}
		self.assertEqual(5, len(premium["mechanism.trough"]["sensors"]))
		self.assertEqual(3, len(premium["mechanism.cannon"]["sensors"]))
		self.assertEqual(2, len(premium["mechanism.cannon"]["actuators"]))
		self.assertEqual(1, len(premium["mechanism.swinging-bell"]["sensors"]))
		self.assertEqual(1, len(premium["mechanism.swinging-bell"]["actuators"]))
		self.assertIn("mechanism.lower-playfield-flippers", premium)
		self.assertIn("mechanism.acdc-drop-bank", premium)
		self.assertNotIn("mechanism.lower-playfield-flippers", pro)
		self.assertEqual([], pro["mechanism.bell"]["actuators"])
		self.assertEqual([], led["mechanism.bell"]["actuators"])
		self.assertIn("freely swinging", led["mechanism.bell"]["behavior"].casefold())

	def test_american_country_repeats_the_inherited_contract_with_retheme_labels(self) -> None:
		premium = self.definitions["premium"]
		american = self.definitions["american"]
		for collection in ("inputs", "outputs"):
			premium_contract = {(item["binding"]["group"], item["binding"]["device"]): (item["kind"], item["availability"]) for item in premium[collection]}
			american_contract = {(item["binding"]["group"], item["binding"]["device"]): (item["kind"], item["availability"]) for item in american[collection]}
			self.assertEqual(premium_contract, american_contract)
		american_outputs = bindings(american, "outputs", "pinmame.output.solenoid")
		american_lamps = bindings(american, "outputs", "pinmame.output.lamp")
		self.assertEqual("Pickup-truck flasher", american_outputs[17]["label"])
		self.assertEqual("Gun rotation motor", american_outputs[32]["label"])
		self.assertEqual("Liberty Bell magnet", american_outputs[54]["label"])
		self.assertTrue(all(american_lamps[address]["label"].startswith("Country Playlist tag") for address in range(65, 77)))
		self.assertEqual({mechanism["id"] for mechanism in premium["mechanisms"]}, {mechanism["id"] for mechanism in american["mechanisms"]})

	def test_exact_rom_runs_anchor_display_gi_and_source_hashes(self) -> None:
		for evidence, driver, rom_sha, raw_sha in (
			(self.premium_evidence, "acd_170h", "1ace847619af4864769b053f641d3e035a1c72d517ac750af7088600cdd291d4", "31d6c8a83091c62785ce5b23cb1417a12bfb229ed61b5366354451510e4940c0"),
			(self.pro_evidence, "acd_170", "e55c7386950272568dd639f3c8d70beff6fbd584ed49601d4196b46cb1e66ca5", "f3c237db82c4686bd58908a9b1935b21a483fe99b753bd6f25ab9b375c372511"),
		):
			runtime = evidence["runtime"]
			self.assertEqual(driver, runtime["game"])
			self.assertEqual(rom_sha, runtime["rom_archive_sha256"])
			self.assertEqual(raw_sha, runtime["raw_runs"][0]["sha256"])
			self.assertEqual([0], runtime["observations"]["gi_addresses_seen"])
			self.assertEqual([{"depth": 4, "height": 32, "type": 14, "width": 128}], runtime["observations"]["display_layouts_seen"])
		premium_sources = {source["id"]: source for source in self.definitions["premium"]["sources"]}
		pro_sources = {source["id"]: source for source in self.definitions["pro"]["sources"]}
		self.assertEqual("d3de500b504b165023e3858883067ca518543307387ec2460397b740ebe240b6", premium_sources["manual.acdc-premium-le"]["sha256"])
		self.assertEqual("b478b21272befd41908aa3ef4daf3a90d4838334346718cb4d5fde7f23bb2fc0", premium_sources["vpx.acdc-luci-premium-vpw-1.1.4"]["sha256"])
		self.assertEqual("987d42c68b586af1b0d66100b9f34d5215dfaf67574032849adb1c2f18c6cab5", pro_sources["manual.acdc-pro"]["sha256"])
		self.assertEqual("e0fdef84892ea8bce6eae179509ac8262f103bac0173c2e822a4fe10aafcf7fa", pro_sources["vpx.acdc-pro-1.0-lighting-fix"]["sha256"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "ac-dc-luci-premium-2013.json").exists())


if __name__ == "__main__":
	unittest.main()
