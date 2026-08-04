from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATHS = {
	"premium": ROOT / "machines" / "partial" / "stern" / "ac-dc-premium-limited-edition-luci-2012.json",
	"pro": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-pro-2012.json",
	"led_pro": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-led-pro-2014.json",
	"vault": ROOT / "machines" / "author-ready" / "stern" / "ac-dc-vault-edition-2018.json",
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

	def test_led_pro_and_vault_are_author_ready_and_other_products_remain_fail_closed(self) -> None:
		for name, definition in self.definitions.items():
			self.assertEqual(2, definition["schema_version"])
			self.assertEqual("complete", definition["knowledge"]["status"])
			if name in {"pro", "led_pro", "vault"}:
				self.assertEqual("author_ready", definition["coverage"]["status"])
				self.assertEqual([], definition["coverage"]["missing"])
				self.assertEqual("validated", definition["coverage"]["dimensions"]["spatial_placement"])
				self.assertTrue(all("spatial" in device for device in [*definition["inputs"], *definition["outputs"]]))
			else:
				self.assertEqual("partial", definition["coverage"]["status"])
				self.assertIn("spatial_placement", definition["coverage"]["missing"])
				self.assertEqual("unknown", definition["coverage"]["dimensions"]["spatial_placement"])

	def test_driver_family_is_split_without_overlap_or_omission(self) -> None:
		expected = {
			"premium": {"acd_150h", "acd_152h", "acd_160h", "acd_161h", "acd_163h", "acd_165h", "acd_168h", "acd_168hc", "acd_170h", "acd_170hc"},
			"pro": {"acd_121", "acd_125", "acd_130", "acd_140", "acd_150", "acd_152", "acd_160", "acd_161", "acd_163", "acd_165"},
			"led_pro": {"acd_168", "acd_168c"},
			"vault": {"acd_170", "acd_170c"},
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
		self.assertIn("Right-loop", vault_lamps[28]["label"])
		self.assertIn("center", vault_switches[35]["label"].casefold())
		self.assertIn("right", vault_switches[42]["label"].casefold())

	def test_original_pro_excludes_premium_only_mechanisms_and_auxiliary_outputs(self) -> None:
		pro = self.definitions["pro"]
		mechanism_ids = {mechanism["id"] for mechanism in pro["mechanisms"]}
		self.assertIn("mechanism.cannon", mechanism_ids)
		self.assertNotIn("mechanism.lower-playfield-eject", mechanism_ids)
		self.assertNotIn("mechanism.lower-playfield-flippers", mechanism_ids)
		self.assertNotIn("mechanism.bell-eject", mechanism_ids)
		self.assertNotIn("mechanism.swinging-bell", mechanism_ids)
		self.assertNotIn("mechanism.detonator", mechanism_ids)
		self.assertNotIn("mechanism.band-members", mechanism_ids)
		self.assertNotIn("mechanism.left-ramp-diverter", mechanism_ids)
		solenoids = bindings(pro, "outputs", "pinmame.output.solenoid")
		self.assertEqual(set(range(1, 34)), set(solenoids))
		bell = next(mechanism for mechanism in pro["mechanisms"] if mechanism["id"] == "mechanism.bell")
		self.assertEqual([], bell["actuators"])

	def test_led_pro_spatial_layout_preserves_exact_deltas_and_na_counts(self) -> None:
		led = self.definitions["led_pro"]
		switches = bindings(led, "inputs", "pinmame.input.switch")
		solenoids = bindings(led, "outputs", "pinmame.output.solenoid")
		lamps = bindings(led, "outputs", "pinmame.output.lamp")
		gi = bindings(led, "outputs", "pinmame.output.gi")[0]
		self.assertEqual({"x": 0.399947, "y": 0.145745}, {key: switches[36]["spatial"]["placements"][0][key] for key in ("x", "y")})
		self.assertEqual(
			["vpx-table.acdc-pro-vault-1.0", "vpx.acdc-pro-vault-1.0-lighting-fix", "stern.acdc-led-pro-announcement"],
			switches[36]["spatial"]["placements"][0]["provenance"]["source_refs"],
		)
		self.assertEqual([], {mechanism["id"]: mechanism for mechanism in led["mechanisms"]}["mechanism.bell"]["actuators"])
		self.assertEqual("Under-apron four-ball trough assembly 500-6318-24-ND", switches[18]["physical"]["location"])
		self.assertEqual("Rotating cannon motor-and-switch assembly", switches[61]["physical"]["location"])
		self.assertEqual(3, len(solenoids[25]["spatial"]["placements"]))
		self.assertEqual(
			[(0.524113, 0.155556), (0.736963, 0.151240), (0.639000, 0.235974)],
			[(placement["x"], placement["y"]) for placement in solenoids[25]["spatial"]["placements"]],
		)
		self.assertEqual(3, solenoids[25]["physical"]["quantity"])
		for address, expected in {
			14: (0.387038, 0.534787), 15: (0.520102, 0.534166), 17: (0.452994, 0.604875),
		}.items():
			self.assertEqual("used", lamps[address]["availability"])
			self.assertEqual(expected, (lamps[address]["spatial"]["placements"][0]["x"], lamps[address]["spatial"]["placements"][0]["y"]))
			self.assertEqual(
				["vpx-table.acdc-pro-1.0", "vpx.acdc-pro-1.0-lighting-fix", "manual.acdc-pro"],
				lamps[address]["spatial"]["placements"][0]["provenance"]["source_refs"],
			)
		self.assertEqual("unused", lamps[16]["spatial"]["reason"])
		self.assertEqual(38, len(gi["spatial"]["placements"]))
		self.assertEqual(45, gi["physical"]["quantity"])
		self.assertIn("seven off-playfield back-panel bulbs", gi["physical"]["notes"])
		self.assertEqual(("not_applicable", "cabinet_or_service"), (solenoids[22]["spatial"]["status"], solenoids[22]["spatial"]["reason"]))
		self.assertEqual({"x": 0.833431, "y": 0.123162}, {key: gi["spatial"]["placements"][11][key] for key in ("x", "y")})
		self.assertEqual(
			["vpx-table.acdc-pro-1.0", "vpx.acdc-pro-1.0-lighting-fix", "manual.acdc-pro"],
			gi["spatial"]["placements"][11]["provenance"]["source_refs"],
		)
		located_inputs = sum(device["spatial"]["status"] == "validated" for device in led["inputs"])
		located_outputs = sum(device["spatial"]["status"] == "validated" for device in led["outputs"])
		placements = sum(len(device["spatial"].get("placements", [])) for device in [*led["inputs"], *led["outputs"]])
		self.assertEqual((48, 81, 168), (located_inputs, located_outputs, placements))
		na_counts = {
			(collection, reason): sum(device["spatial"].get("reason") == reason for device in led[collection])
			for collection in ("inputs", "outputs")
			for reason in ("cabinet_or_service", "dip_switch", "unused", "virtual", "internal_nonvisual")
		}
		self.assertEqual(17, na_counts[("inputs", "cabinet_or_service")])
		self.assertEqual(8, na_counts[("inputs", "dip_switch")])
		self.assertEqual(23, na_counts[("inputs", "unused")])
		self.assertEqual(21, na_counts[("outputs", "cabinet_or_service")])
		self.assertEqual(14, na_counts[("outputs", "unused")])
		self.assertEqual(1, na_counts[("outputs", "virtual")])
		self.assertEqual(0, na_counts[("outputs", "internal_nonvisual")])
		self.assertEqual(11, len(led["mechanisms"]))
		led_sources = {source["id"]: source for source in led["sources"]}
		self.assertEqual("vpx_table", led_sources["vpx-table.acdc-pro-1.0"]["kind"])
		self.assertEqual("local-evidence://vpx-table/acdc-pro-1.0", led_sources["vpx-table.acdc-pro-1.0"]["uri"])
		self.assertEqual("AC-DC Pro-1.0.vpx", led_sources["vpx-table.acdc-pro-1.0"]["original_filename"])
		self.assertEqual("44bf3d67f96968103ab71f26b8b12786e5590f62bd73589b85060983dc62d9e9", led_sources["vpx-table.acdc-pro-1.0"]["sha256"])
		self.assertIn("78,274,560 bytes", led_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("235 centered candidates", led_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("bounds 0,0-952,2115", led_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("cGameName=acd_170", led_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("AC/DC Pro (Stern 2012)", led_sources["vpx-table.acdc-pro-1.0"]["locator"])

	def test_original_pro_spatial_layout_uses_standup_bell_and_original_lamps(self) -> None:
		pro = self.definitions["pro"]
		switches = bindings(pro, "inputs", "pinmame.input.switch")
		solenoids = bindings(pro, "outputs", "pinmame.output.solenoid")
		lamps = bindings(pro, "outputs", "pinmame.output.lamp")
		gi = bindings(pro, "outputs", "pinmame.output.gi")[0]
		self.assertEqual({"x": 0.387677, "y": 0.092558}, {key: switches[36]["spatial"]["placements"][0][key] for key in ("x", "y")})
		self.assertEqual(
			["vpx-table.acdc-pro-1.0", "vpx.acdc-pro-1.0-lighting-fix", "manual.acdc-pro"],
			switches[36]["spatial"]["placements"][0]["provenance"]["source_refs"],
		)
		bell = {mechanism["id"]: mechanism for mechanism in pro["mechanisms"]}["mechanism.bell"]
		self.assertEqual("Hell's Bell standup target", bell["label"])
		self.assertEqual("other", bell["kind"])
		self.assertEqual([], bell["actuators"])
		for address, expected in {
			14: (0.387038, 0.534787), 15: (0.520102, 0.534166), 17: (0.452994, 0.604875),
		}.items():
			self.assertEqual(expected, (lamps[address]["spatial"]["placements"][0]["x"], lamps[address]["spatial"]["placements"][0]["y"]))
		self.assertEqual({"x": 0.833431, "y": 0.123162}, {key: gi["spatial"]["placements"][11][key] for key in ("x", "y")})
		located_inputs = sum(device["spatial"]["status"] == "validated" for device in pro["inputs"])
		located_outputs = sum(device["spatial"]["status"] == "validated" for device in pro["outputs"])
		placements = sum(len(device["spatial"].get("placements", [])) for device in [*pro["inputs"], *pro["outputs"]])
		self.assertEqual((48, 81, 168), (located_inputs, located_outputs, placements))
		self.assertEqual(38, len(gi["spatial"]["placements"]))
		self.assertEqual(45, gi["physical"]["quantity"])
		self.assertEqual(("not_applicable", "cabinet_or_service"), (solenoids[22]["spatial"]["status"], solenoids[22]["spatial"]["reason"]))
		pro_sources = {source["id"]: source for source in pro["sources"]}
		self.assertEqual("vpx_table", pro_sources["vpx-table.acdc-pro-1.0"]["kind"])
		self.assertEqual("44bf3d67f96968103ab71f26b8b12786e5590f62bd73589b85060983dc62d9e9", pro_sources["vpx-table.acdc-pro-1.0"]["sha256"])
		self.assertIn("78,274,560 bytes", pro_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("235 centered candidates", pro_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("bounds 0,0-952,2115", pro_sources["vpx-table.acdc-pro-1.0"]["locator"])
		self.assertIn("cGameName=acd_170", pro_sources["vpx-table.acdc-pro-1.0"]["locator"])

	def test_pro_derived_rear_panel_fixtures_keep_physical_records_without_playfield_coordinates(self) -> None:
		for variant in ("pro", "led_pro", "vault"):
			definition = self.definitions[variant]
			lamps = bindings(definition, "outputs", "pinmame.output.lamp")
			solenoids = bindings(definition, "outputs", "pinmame.output.solenoid")
			for address in (53, 54, 55, 56, 65, 66, 67, 68, 69, 70, 71, 72):
				self.assertEqual(("not_applicable", "cabinet_or_service"), (lamps[address]["spatial"]["status"], lamps[address]["spatial"]["reason"]))
				self.assertEqual(["cabinet.rear-panel"], lamps[address]["roles"])
				self.assertEqual(1, lamps[address]["physical"]["quantity"])
				self.assertIn("no playfield coordinate", lamps[address]["physical"]["notes"])
			self.assertEqual(["cabinet.rear-panel"], solenoids[22]["roles"])
			self.assertEqual(1, solenoids[22]["physical"]["quantity"])
			self.assertIn("no playfield coordinate", solenoids[22]["physical"]["notes"])

	def test_vault_spatial_layout_preserves_physical_multiplicity_and_cabinet_scope(self) -> None:
		vault = self.definitions["vault"]
		switches = bindings(vault, "inputs", "pinmame.input.switch")
		solenoids = bindings(vault, "outputs", "pinmame.output.solenoid")
		lamps = bindings(vault, "outputs", "pinmame.output.lamp")
		gi = bindings(vault, "outputs", "pinmame.output.gi")[0]
		self.assertEqual({"x": 0.220215, "y": 0.726524}, {key: switches[26]["spatial"]["placements"][0][key] for key in ("x", "y")})
		self.assertEqual({"x": 0.720277, "y": 0.695345}, {key: switches[61]["spatial"]["placements"][0][key] for key in ("x", "y")})
		self.assertEqual("cabinet_or_service", switches[64]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", lamps[1]["spatial"]["reason"])
		self.assertEqual(3, len(solenoids[25]["spatial"]["placements"]))
		self.assertEqual(3, solenoids[25]["physical"]["quantity"])
		self.assertEqual(38, len(gi["spatial"]["placements"]))
		self.assertEqual(45, gi["physical"]["quantity"])
		self.assertEqual(("not_applicable", "cabinet_or_service"), (solenoids[22]["spatial"]["status"], solenoids[22]["spatial"]["reason"]))
		self.assertEqual("not_applicable", lamps[14]["spatial"]["status"])
		self.assertEqual("unused", lamps[14]["spatial"]["reason"])
		self.assertEqual("cabinet_or_service", solenoids[8]["spatial"]["reason"])
		self.assertEqual(["cabinet.shaker"], solenoids[8]["roles"])
		self.assertEqual("cabinet_or_service", solenoids[24]["spatial"]["reason"])
		self.assertFalse(any(output["spatial"].get("reason") == "internal_nonvisual" for output in vault["outputs"]))
		self.assertEqual(11, len(vault["mechanisms"]))

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
		self.assertEqual("44bf3d67f96968103ab71f26b8b12786e5590f62bd73589b85060983dc62d9e9", pro_sources["vpx-table.acdc-pro-1.0"]["sha256"])
		self.assertIn("78,274,560 bytes", pro_sources["vpx-table.acdc-pro-1.0"]["locator"])
		vault_sources = {source["id"]: source for source in self.definitions["vault"]["sources"]}
		self.assertEqual("10a460c6b84fc1b8b372bf7b3d92b1904ee5eed9d5aad29fe384e7a6502fa328", vault_sources["vpx-table.acdc-pro-vault-1.0"]["sha256"])
		self.assertIn("79,429,632 bytes", vault_sources["vpx-table.acdc-pro-vault-1.0"]["locator"])
		self.assertFalse((ROOT / "machines" / "partial" / "stern" / "ac-dc-luci-premium-2013.json").exists())


if __name__ == "__main__":
	unittest.main()
