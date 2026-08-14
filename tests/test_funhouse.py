from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "funhouse-1990.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "funhouse-1990.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "funhouse-1990.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "funhouse-1990.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-alpha.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / "reports" / "spatial" / "williams" / "funhouse-1990.md"

DRIVER_IDS = {
	"fh_l9", "fh_d9", "fh_l9b", "fh_d9b", "fh_905h", "fh_906h", "fh_907h", "fh_pa1",
	"fh_l2", "fh_l3", "fh_d3", "fh_l4", "fh_d4", "fh_l5", "fh_d5", "fh_f91",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {51, 55}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {item["binding"]["device"]: item for item in definition[collection] if item["binding"]["group"] == group}


def _run_curator_without_mode() -> None:
	import curate_funhouse as curator

	argv = sys.argv
	sys.argv = ["curate_funhouse.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class FunHouseDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_single_spatial_blocker(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("unknown", self.definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertEqual({"validated"}, {value for key, value in self.definition["coverage"]["dimensions"].items() if key != "spatial_placement"})
		self.assertEqual("williams.funhouse.1990", self.definition["machine"]["id"])
		self.assertEqual("Williams", self.definition["machine"]["manufacturer"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1990, self.definition["machine"]["year"])
		self.assertEqual(966, self.definition["machine"]["ipdb_id"])
		self.assertEqual("pinmame.wpc-alpha", self.definition["controller"]["platform"])
		self.assertEqual("0x2", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_driver_tree_matches_pinned_catalog(self) -> None:
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(by_id))
		self.assertNotIn("clone_of", by_id["fh_l9"])
		for driver_id in DRIVER_IDS - {"fh_l9"}:
			self.assertEqual("fh_l9", by_id[driver_id]["clone_of"], driver_id)
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"})
			self.assertGreater(len(driver["variant_notes"]), 0)
		self.assertEqual("compatible", by_id["fh_pa1"]["physical_compatibility"])
		self.assertIn("GEN_WPCALPHA_1", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("gameSpecific1=1", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("WPC_CFTBL", by_id["fh_pa1"]["variant_notes"])
		self.assertIn("internal PWM lamp slots 65-72", by_id["fh_pa1"]["variant_notes"])

	def test_retained_source_identity_and_tool_version_are_pinned(self) -> None:
		by_id = {source["id"]: source for source in self.definition["sources"]}
		manual = by_id["manual.williams.funhouse.1990"]
		self.assertEqual("arcademanual_Funhouse_OPS", manual["source_id"])
		self.assertEqual("https://archive.org/details/arcademanual_Funhouse_OPS", manual["uri"])
		self.assertEqual("2026-08-07T00:18:16Z", manual["acquired_at"])
		self.assertIn("manuallibrary@textfiles.com", manual["locator"])
		self.assertEqual("2026-08-14T17:36:41Z", by_id["manual.williams.funhouse.1990.operator-handbook"]["acquired_at"])
		self.assertEqual("2026-08-14T17:37:39Z", by_id["photo.williams.funhouse.1990.a13"]["acquired_at"])
		self.assertEqual("2026-08-07T15:17:32Z", by_id["vpx-table.fh-1-3"]["acquired_at"])
		self.assertEqual("2026-08-07T15:17:33Z", by_id["vpx-script.fh-1-3"]["acquired_at"])
		self.assertIn("vpxtool git:v0.33.3", by_id["vpx-extraction.fh-1-3"]["locator"])

	def test_controller_profile_reused_unchanged(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-alpha", profile["id"])
		self.assertEqual({"pinmame.input.switch", "pinmame.input.dip", "pinmame.output.solenoid", "pinmame.output.lamp", "pinmame.output.gi"}, {group["id"] for group in profile["groups"]})

	def test_switch_and_dip_enumeration(self) -> None:
		matrix_switches = {address: switch for address, switch in self.switches.items() if address in MATRIX_ADDRESSES}
		self.assertEqual(MATRIX_ADDRESSES, set(matrix_switches))
		for address, switch in matrix_switches.items():
			if address in UNUSED_MATRIX_ADDRESSES:
				self.assertEqual("unused", switch["availability"], address)
				self.assertEqual("unused", switch["spatial"]["reason"], address)
			else:
				self.assertEqual("used", switch["availability"], address)
		for address in range(1, 9):
			self.assertEqual(f"switch.cabinet-{address}", self.switches[address]["id"])
		self.assertEqual(set(range(111, 119)), {address for address in self.switches if 111 <= address <= 118})
		for address in {112, 114}:
			self.assertEqual("used", self.switches[address]["availability"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		for address in {111, 113, 115, 116, 117, 118}:
			self.assertEqual("unused", self.switches[address]["availability"])
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"])
		for address in {11, 12}:
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
			self.assertIn("matrix state is copied", self.switches[address]["physical"]["notes"])
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))

	def test_optos_and_constant_switch_are_normalized(self) -> None:
		for address, switch in self.switches.items():
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"].get("switch_type"), address)
				self.assertTrue(switch["normally_closed"], address)
			elif address in MATRIX_ADDRESSES and address not in UNUSED_MATRIX_ADDRESSES and address != 24:
				self.assertNotEqual("opto", switch["physical"].get("switch_type"), address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])

	def test_right_trough_switch_is_resolved_on_ballrelease(self) -> None:
		switch = self.switches[63]
		self.assertEqual("Right Trough", switch["label"])
		self.assertEqual("validated", switch["spatial"]["status"])
		placement = switch["spatial"]["placements"][0]
		self.assertAlmostEqual(0.877269, placement["x"], places=6)
		self.assertAlmostEqual(0.863859, placement["y"], places=6)
		self.assertIn("manual.williams.funhouse.1990.operator-handbook", placement["provenance"]["source_refs"])

	def test_public_solenoid_contract_is_complete(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		for address in {17, 18, 19, 20, 23, 24}:
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
			self.assertEqual(self.solenoids[address]["physical"]["quantity"], len(self.solenoids[address]["spatial"]["placements"]), address)
		self.assertEqual(2, len({(placement["x"], placement["y"]) for placement in self.solenoids[20]["spatial"]["placements"]}))
		self.assertEqual(
			[(0.446452, 0.46247), (0.460268, 0.512137)],
			[(placement["x"], placement["y"]) for placement in self.solenoids[20]["spatial"]["placements"]],
		)
		self.assertIn("vpx-script.funhouse-community-current", self.solenoids[20]["provenance"]["source_refs"])
		self.assertEqual("motor", self.solenoids[21]["kind"])
		self.assertEqual("motor", self.solenoids[22]["kind"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])

	def test_wpc_state_and_virtual_output_dispositions(self) -> None:
		for address in (29, 30):
			self.assertEqual("virtual", self.solenoids[address]["kind"])
			self.assertEqual("used", self.solenoids[address]["availability"])
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"])
		self.assertEqual("relay", self.solenoids[31]["kind"])
		self.assertEqual("used", self.solenoids[31]["availability"])
		self.assertEqual(["internal.wpc-state", "cabinet.game-on-relay"], self.solenoids[31]["roles"])
		self.assertEqual("cabinet_or_service", self.solenoids[31]["spatial"]["reason"])
		for address in {32, *range(33, 45), 50}:
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		self.assertEqual("virtual", self.solenoids[49]["kind"])
		self.assertEqual("used", self.solenoids[49]["availability"])
		self.assertEqual(["internal.simulator-ball-shooter"], self.solenoids[49]["roles"])
		self.assertIn("sShooterRel", self.solenoids[49]["physical"]["notes"])

	def test_synthetic_flipper_states_are_not_physical_coils(self) -> None:
		for address in range(45, 49):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		flippers = next(mechanism for mechanism in self.definition["mechanisms"] if mechanism["id"] == "mechanism.flippers")
		self.assertEqual(["device.synthetic-lower-right-flipper", "device.synthetic-left-flipper"], flippers["actuators"])
		self.assertEqual({"lower-right", "lower-left", "upper-left"}, {position["id"] for position in flippers["positions"]})
		self.assertIn("FL-11753", flippers["behavior"])
		self.assertIn("both LeftFlipper and LeftFlipper1", flippers["behavior"])
		self.assertIn("must not", flippers["behavior"])

	def test_lamp_matrix_and_multi_bulb_quantities(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertTrue(all(lamp["availability"] == "used" for lamp in self.lamps.values()))
		for address in (53, 61, 82):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (51, 52, 72):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)

	def test_steps_lamps_use_one_hotspot_each_in_vertical_order(self) -> None:
		for address in (54, 55, 56):
			self.assertEqual("validated", self.lamps[address]["spatial"]["status"])
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"])
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]))
			self.assertIn("_finger_1", self.lamps[address]["physical"]["notes"])
		y = {address: self.lamps[address]["spatial"]["placements"][0]["y"] for address in (54, 55, 56)}
		self.assertLess(y[56], y[55])
		self.assertLess(y[55], y[54])

	def test_gangway_typo_is_resolved_and_no_conflicts_remain(self) -> None:
		self.assertEqual("Gangway 100,000", self.lamps[12]["label"])
		self.assertIn("resolved one-digit typo", self.lamps[12]["physical"]["notes"])
		refs = set(self.lamps[12]["provenance"]["source_refs"])
		self.assertIn("manual.williams.funhouse.1990.operator-handbook", refs)
		self.assertIn("photo.williams.funhouse.1990.a13", refs)
		self.assertEqual([], self.definition["conflicts"])

	def test_gi_enumeration_and_physical_hotspots(self) -> None:
		self.assertEqual(set(range(5)), set(self.gi))
		self.assertEqual("not_applicable", self.gi[0]["spatial"]["status"])
		self.assertNotIn("spatial", self.gi[3])
		self.assertEqual("Q18", self.gi[0]["wiring"]["driver_transistor"])
		self.assertEqual("Q10", self.gi[1]["wiring"]["driver_transistor"])
		self.assertEqual("Q14", self.gi[2]["wiring"]["driver_transistor"])
		self.assertEqual("Q16", self.gi[3]["wiring"]["driver_transistor"])
		self.assertEqual("Q12", self.gi[4]["wiring"]["driver_transistor"])
		for address, quantity in ((1, 3), (2, 15), (4, 14)):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"])
			self.assertEqual(quantity, self.gi[address]["physical"]["quantity"])
			self.assertEqual(quantity, len(self.gi[address]["spatial"]["placements"]))
		self.assertEqual("Rudy G.I.", self.gi[1]["label"])
		self.assertEqual("Upper/Rear Playfield G.I.", self.gi[2]["label"])
		self.assertEqual("Lower Playfield G.I.", self.gi[4]["label"])

	def test_displays_and_mechanisms_are_complete(self) -> None:
		self.assertEqual(2, len(self.definition["displays"]))
		for display in self.definition["displays"]:
			self.assertEqual("segment", display["kind"])
			self.assertEqual(16, display["width"])
			self.assertEqual("not_applicable", display["spatial"]["status"])
		self.assertEqual({0, 1}, {display["controller_index"] for display in self.definition["displays"]})
		self.assertEqual({"mechanism.rudy-jaw", "mechanism.rudy-eyes", "mechanism.trap-door", "mechanism.step-gate", "mechanism.ramp-diverter", "mechanism.trough-and-shooters", "mechanism.tunnel-kickout", "mechanism.rudys-hideout", "mechanism.dummy-eject-hole", "mechanism.multiball-lock", "mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.flippers"}, {mechanism["id"] for mechanism in self.definition["mechanisms"]})

	def test_spatial_positions_are_normalized_and_only_gi_3_is_missing(self) -> None:
		missing = []
		for collection in (self.switches, self.solenoids, self.lamps, self.gi):
			for device in collection.values():
				spatial = device.get("spatial")
				if spatial is None:
					missing.append((device["binding"]["group"], device["binding"]["device"]))
					continue
				if spatial["status"] != "validated":
					continue
				for placement in spatial["placements"]:
					for axis in ("x", "y"):
						self.assertGreaterEqual(placement[axis], 0.0)
						self.assertLessEqual(placement[axis], 1.0)
						self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)
		self.assertEqual([("pinmame.output.gi", 3)], missing)

	def test_geometric_ordering_regressions(self) -> None:
		switch_x = {address: switch["spatial"]["placements"][0]["x"] for address, switch in self.switches.items() if switch.get("spatial") and switch["spatial"]["status"] == "validated"}
		switch_y = {address: switch["spatial"]["placements"][0]["y"] for address, switch in self.switches.items() if switch.get("spatial") and switch["spatial"]["status"] == "validated"}
		lamp_x = {address: lamp["spatial"]["placements"][0]["x"] for address, lamp in self.lamps.items() if lamp.get("spatial") and lamp["spatial"]["status"] == "validated"}
		self.assertLess(switch_x[41], switch_x[53])
		self.assertLess(switch_x[43], switch_x[52])
		self.assertLess(switch_x[18], switch_x[68])
		self.assertLess(switch_x[68], switch_x[77])
		self.assertLess(switch_x[47], switch_x[62])
		for left, right in zip(range(11, 16), range(12, 17)):
			self.assertLess(lamp_x[left], lamp_x[right])
		self.assertLess(self.lamps[61]["spatial"]["placements"][0]["x"], self.lamps[61]["spatial"]["placements"][1]["x"])
		self.assertLess(self.lamps[82]["spatial"]["placements"][0]["x"], self.lamps[82]["spatial"]["placements"][1]["x"])
		self.assertAlmostEqual(self.lamps[51]["spatial"]["placements"][0]["x"], self.switches[68]["spatial"]["placements"][0]["x"], delta=0.01)

	def test_seed_and_curator_are_deterministic(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())
		self.assertFalse(AUTHOR_READY_PATH.exists())
		import curate_funhouse as curator

		curator.check(ROOT)

	def test_curator_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_spatial_audit_matches_curator_and_names_gi_blocker(self) -> None:
		import curate_funhouse as curator

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(report, load_json(SPATIAL_REPORT_PATH))
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual("partial", report["status"])
		self.assertEqual(1, len(report["blockers"]))
		self.assertIn("socket-level", report["blockers"][0])
		self.assertEqual([{"group": "pinmame.output.gi", "address": 3}], report["unresolved"])
		self.assertEqual("vpxtool git:v0.33.3", report["extraction"]["vpxtool_version"])
		self.assertEqual(curator.render_spatial_report(report), SPATIAL_REPORT_MARKDOWN_PATH.read_text(encoding="utf-8"))

	def test_device_identifiers_are_unique(self) -> None:
		identifiers = [device["id"] for device in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_all_committed_excerpts_exist_and_hash_match(self) -> None:
		for source in self.definition["sources"]:
			for excerpt in source.get("excerpts", []):
				path = ROOT / excerpt["path"]
				self.assertTrue(path.is_file(), excerpt["path"])
				self.assertEqual(excerpt["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), excerpt["path"])
				if "image" in excerpt:
					image_path = ROOT / excerpt["image"]
					self.assertTrue(image_path.is_file(), excerpt["image"])
					self.assertEqual(excerpt["image_sha256"], hashlib.sha256(image_path.read_bytes()).hexdigest(), excerpt["image"])


if __name__ == "__main__":
	unittest.main()
