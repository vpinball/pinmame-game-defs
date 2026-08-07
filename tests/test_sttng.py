from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "star-trek-the-next-generation-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "star-trek-the-next-generation-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "star-trek-the-next-generation-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "star-trek-the-next-generation-1993.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-dcs.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "star-trek-the-next-generation-1993.json"

DRIVER_IDS = {
	"sttng_l7", "sttng_d1", "sttng_d2", "sttng_d7", "sttng_dx", "sttng_g7", "sttng_h7",
	"sttng_l1", "sttng_l2", "sttng_l3", "sttng_l5", "sttng_l7c", "sttng_p4", "sttng_p5",
	"sttng_p6", "sttng_p8", "sttng_x7", "sttng_x8", "sttng_x9",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 61, 62, 63, 64, 65, 66, 67}
CUSTOM_SWITCH_ADDRESSES = {121, 122, 123, 124, 125, 126, 127, 128}
CUSTOM_SWITCH_USED = {122, 125, 126, 127}
CUSTOM_SOLENOID_ADDRESSES = {51, 52, 53, 54, 55, 56}


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict[str, object], collection: str, group: str) -> dict[int, dict[str, object]]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


def _run_curator_without_mode() -> None:
	"""Invoke the curator's CLI with no mode so argparse rejects it instead of writing files."""
	import curate_sttng as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_sttng.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class SttngDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "spatial_placement":
				continue
			self.assertEqual("validated", state, dimension)
		self.assertEqual("williams.star-trek-the-next-generation.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2357, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual({"width": 1093, "height": 2162, "units": "vpx"}, self.definition["machine"]["playfield"])
		self.assertEqual("pinmame.wpc-dcs", self.definition["controller"]["platform"])
		self.assertEqual("0x10", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_sttng_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertNotIn("clone_of", by_id["sttng_l7"])
		for driver_id in DRIVER_IDS - {"sttng_l7"}:
			self.assertEqual("sttng_l7", by_id[driver_id]["clone_of"], driver_id)

	def test_the_full_wpc_dcs_input_space_is_enumerated(self) -> None:
		expected = (
			set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)) | CUSTOM_SWITCH_ADDRESSES
		)
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		# Unlike Monster Bash/Indiana Jones, no standard matrix position (11-88) is printed Not Used.
		for address in sorted(MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in sorted(CUSTOM_SWITCH_ADDRESSES - CUSTOM_SWITCH_USED):
			self.assertEqual("unused", self.switches[address]["availability"], address)
		for address in sorted(CUSTOM_SWITCH_USED):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_pinmame_normalization_exactly(self) -> None:
		# Every printed opto (columns 3, 4, and 6 rows 1-7) is normalized by PinMAME; every
		# non-opto matrix position is not. There is zero disagreement anywhere -- conflicts is
		# empty for this machine, unlike Monster Bash or Indiana Jones.
		for address in sorted(MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])
		# The custom switch column (121-128) is not opto and is not inverted either -- also no
		# conflict, confirmed across the switch matrix shading, the parts list, and the Gun
		# Circuit Diagram's plain switch-contact symbol.
		for address in sorted(CUSTOM_SWITCH_USED):
			self.assertFalse(self.switches[address]["normally_closed"], address)

	def test_custom_switch_column_uses_the_core_custswcol_arithmetic_not_the_printed_silkscreen(self) -> None:
		import curate_sttng as curator

		# CORE_CUSTSWCOL = CORE_STDSWCOLS = 12; hw.swCol = 1 -> internal column 12 -> public 120+r.
		for address, manual in curator.CUSTOM_SWITCH_MANUAL_ALIAS.items():
			self.assertEqual(str(address - 30), manual, address)
			aliases = {a["value"] for a in self.switches[address]["aliases"] if a["namespace"] == "manual.address"}
			self.assertEqual({manual}, aliases, address)
		self.assertEqual("Left Gun Mark", self.switches[122]["label"])
		self.assertEqual("Left Gun Home", self.switches[127]["label"])
		self.assertEqual("Right Gun Home", self.switches[125]["label"])
		self.assertEqual("Right Gun Mark", self.switches[126]["label"])

	def test_custom_solenoid_board_uses_core_firstcustsol_arithmetic_not_the_printed_silkscreen(self) -> None:
		import curate_sttng as curator

		for address, manual in curator.CUSTOM_SOLENOID_MANUAL_ALIAS.items():
			self.assertEqual(str(address - 14), manual, address)
			aliases = {a["value"] for a in self.solenoids[address]["aliases"] if a["namespace"] == "manual.address"}
			self.assertEqual({manual}, aliases, address)
		self.assertEqual("Under Divertor Top", self.solenoids[51]["label"])
		self.assertEqual("Under Divertor Bottom", self.solenoids[52]["label"])
		self.assertEqual("Top Drop Up", self.solenoids[53]["label"])
		self.assertEqual("Top Drop Down", self.solenoids[54]["label"])
		self.assertEqual("Romulan Flashers", self.solenoids[55]["label"])
		self.assertEqual("Right Ramp Flashers", self.solenoids[56]["label"])
		# All six custom solenoids are only reachable through core_getSol's solNo>50 dispatch to
		# hw.getSol; the manual's own "37-42" board silkscreen is captured only as an alias, never
		# as the binding.device itself.
		for address in CUSTOM_SOLENOID_ADDRESSES:
			self.assertEqual(address, self.solenoids[address]["binding"]["device"])

	def test_eddy_current_return_lanes_are_not_opto(self) -> None:
		for address in (16, 17):
			switch = self.switches[address]
			self.assertEqual("other", switch["physical"]["switch_type"], address)
			self.assertFalse(switch["normally_closed"], address)
			self.assertIn("eddy", switch["physical"]["notes"].lower())
			self.assertIn("A-16922", switch["physical"]["notes"])

	def test_upper_left_flipper_is_absent_and_upper_right_is_fitted(self) -> None:
		for address in (111, 112, 113, 114, 115, 116):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("unused", self.switches[118]["availability"])
		self.assertEqual("unused", self.switches[118]["spatial"]["reason"])
		for address in (33, 34):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		for address in (35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		spinner = self.switches[117]
		self.assertEqual("Spinner", spinner["label"])
		self.assertEqual("used", spinner["availability"])
		self.assertFalse(spinner["normally_closed"])
		self.assertIn("spatial", spinner)
		self.assertEqual("validated", spinner["spatial"]["status"])

	def test_the_full_wpc_dcs_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 57))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(20, 29):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (17, 18):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("not_applicable", self.solenoids[address]["spatial"]["status"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_kickback_and_bonus_left_outlane_causality(self) -> None:
		self.assertEqual("Kickback", self.solenoids[8]["label"])
		self.assertEqual("used", self.solenoids[8]["availability"])
		self.assertIn("KickBack", self.solenoids[8]["physical"]["notes"])
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertIn("switch.matrix-15", mechanisms["mechanism.kickback"]["sensors"])
		self.assertIn("15", mechanisms["mechanism.kickback"]["behavior"])

	def test_knocker_is_backbox_and_no_device_double_counts_it(self) -> None:
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])
		self.assertEqual(["cabinet.backbox"], self.solenoids[7]["roles"])

	def test_gi_playfield_circuits_are_located_and_insert_panel_circuits_are_cabinet(self) -> None:
		for address in (0, 3, 4):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(6, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(18, len(self.gi[3]["spatial"]["placements"]))
		self.assertEqual(16, len(self.gi[4]["spatial"]["placements"]))
		for address in (1, 2):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)
			self.assertEqual("Insert G.I.", self.gi[address]["label"])

	def test_lamp_quantities_and_the_three_spatially_unresolved_lamps(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - {53, 78, 85, 86, 87, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertIn("spatial", self.lamps[address], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in (53, 85, 86):
			self.assertNotIn("spatial", self.lamps[address], address)
			self.assertEqual("used", self.lamps[address]["availability"], address)
		self.assertEqual("Advance in Rank", self.lamps[53]["label"])
		self.assertEqual("Borg Lock", self.lamps[85]["label"])
		self.assertEqual("Borg Jackpot", self.lamps[86]["label"])
		# Lamp 78 (Borg Ship) is one manual bulb rendered as a five-point animation; one placement.
		self.assertEqual("Borg Ship", self.lamps[78]["label"])
		self.assertEqual(1, len(self.lamps[78]["spatial"]["placements"]))
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device.get("spatial")
			if spatial is None or spatial["status"] == "not_applicable":
				continue
			self.assertEqual("validated", spatial["status"], device["id"])
			for placement in spatial["placements"]:
				located += 1
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				self.assertEqual("playfield", placement["space"])
				for axis in ("x", "y"):
					self.assertGreaterEqual(placement[axis], 0.0)
					self.assertLessEqual(placement[axis], 1.0)
					self.assertLessEqual(len(str(placement[axis]).partition(".")[2]), 6)
				self.assertEqual("validated", placement["provenance"]["status"])
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("validated", report["status"])
		self.assertEqual(1, len(report["blockers"]))
		for address in (53, 85, 86):
			self.assertIn(str(address), report["blockers"][0])
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _placement_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _placement_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _placement_positions(self.lamps).items()}
		# Left gun (custom 122/127) sits left of right gun (custom 125/126).
		self.assertLess(switch_x[122], switch_x[125])
		self.assertLess(switch_x[127], switch_x[126])
		# Left/right jet bumpers and the return lanes keep left < right ordering.
		self.assertLess(switch_x[16], switch_x[17])
		self.assertLess(switch_x[71], switch_x[72])
		# Left 45-degree target (26) is left of center (27), which is left of right (28).
		self.assertLess(switch_x[26], switch_x[27])
		self.assertLess(switch_x[27], switch_x[28])
		# Left slingshot wall sits left of right slingshot wall (solenoid geometry, switch 75/74).
		self.assertLess(switch_x[75], switch_x[74])
		# Trough/shooter sit toward the front (large y) of the playfield.
		self.assertGreater(switch_y[61], 0.5)
		self.assertGreater(switch_y[68], 0.5)
		# Left bank targets (51-53) sit left of right bank targets (54-56).
		self.assertLess(switch_x[51], switch_x[54])
		self.assertLess(switch_x[52], switch_x[55])
		self.assertLess(switch_x[53], switch_x[56])
		# Lamp columns mirror the same left/right split for the gun-mark lamp area proxies.
		self.assertLess(lamp_x[11], lamp_x[18])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.left-gun", "mechanism.right-gun", "mechanism.left-lock-queue",
				"mechanism.borg-lock", "mechanism.underplayfield-diverters", "mechanism.top-drop-target",
				"mechanism.bank-standups", "mechanism.trough", "mechanism.shooter-lane",
				"mechanism.kickback", "mechanism.jet-bumpers", "mechanism.slingshots",
				"mechanism.flippers", "mechanism.eddy-return-lanes", "mechanism.spinner",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		owners: dict[str, str] = {}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)
			for position in mechanism.get("positions", []):
				self.assertTrue(position["description"].strip(), (mechanism["id"], position["id"]))
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"}
			and device["availability"] == "used"
			and "cabinet.backbox" not in device.get("roles", [])
		}
		self.assertEqual(set(), physical - set(owners))
		# The backbox knocker is a simple cabinet device with no playfield mechanism of its own.
		self.assertNotIn("device.knocker", owners)
		# The gun motor never actuates its own Home/Mark switch directly -- it drives continuous
		# rotation and the switches sense the resulting angle. This must read explicitly.
		self.assertIn("does not itself actuate", mechanisms["mechanism.left-gun"]["behavior"])
		self.assertIn("never directly actuates", mechanisms["mechanism.right-gun"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-eject-opto"}, set(relationships))
		self.assertEqual("switch.matrix-67", relationships["relationship.trough-eject-opto"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-eject-opto"]["kind"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.sttng-vpw-mod-1-0", sources)
		self.assertTrue(sources["vpx-script.sttng-vpw-mod-1-0"]["known_working"])
		self.assertEqual(
			"073d9971157e822a246b2baf1e8f8033304d1b5272ffb2e9bd9581caf448cd24",
			sources["vpx-script.sttng-vpw-mod-1-0"]["sha256"],
		)
		self.assertEqual(
			"bd00efe46f3ab2392f8c471e65177b348da8e9fcb5829e9f073ab23f69714d8c",
			sources["vpx-table.sttng-vpw-mod-1-0"]["sha256"],
		)
		self.assertEqual(
			"7f626bce89556b2af4c80bf9eb1a5f74c72cbffe83a85b5142f17140bc820d86",
			sources["manual.williams.star-trek-the-next-generation.1993"]["sha256"],
		)
		self.assertNotIn("runtime.star-trek-the-next-generation", sources)
		self.assertNotIn("rom.sttng", sources)
		for source in self.definition["sources"]:
			self.assertNotEqual("runtime_scenario", source["kind"])
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("l:\\", value.lower())
					self.assertNotIn("l:/", value.lower())

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.wpc-dcs", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])
		groups = {group["id"]: group for group in profile["groups"]}
		used = {device["binding"]["group"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		self.assertTrue(used <= set(groups))

		def allowed(group_id: str, address: int) -> bool:
			for rule in groups[group_id]["address_rules"]:
				if "values" in rule and address in rule["values"]:
					return True
				if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
					return True
			return False

		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			self.assertTrue(allowed(device["binding"]["group"], device["binding"]["device"]), device["id"])


def _placement_positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class SttngCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_sttng as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_sttng as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_sttng as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Star Trek", b"Star Wars", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_sttng as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class SttngRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_sttng as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_sttng as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/star-trek-the-next-generation-1993/source/Star_Trek_The_Next_Generation_Williams_1993_VPW_Mod_v1.0.vpx"
		script = source_root / "williams/star-trek-the-next-generation-1993/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_sttng as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "star-trek-the-next-generation-1993" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
