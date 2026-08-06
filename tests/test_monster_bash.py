from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "monster-bash-1998.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "monster-bash-1998.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "monster-bash-1998.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "monster-bash-1998.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "monster-bash-1998.json"

DRIVER_IDS = {"mb_05", "mb_10", "mb_106", "mb_106b"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {37, 38, 41, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 42, 43}


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
	import curate_monster_bash as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_monster_bash.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class MonsterBashDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_promoted_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		self.assertEqual([], self.definition["conflicts"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.monster-bash.1998", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(4441, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1998, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_stale_partial_is_gone(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_mb_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("mb_10", by_id["mb_05"]["clone_of"])
		self.assertEqual("mb_10", by_id["mb_106"]["clone_of"])
		self.assertEqual("mb_10", by_id["mb_106b"]["clone_of"])
		self.assertNotIn("clone_of", by_id["mb_10"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_the_pinmame_inversion_mask(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_flipper_positions_and_center_spinner(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		# 116 and 118 are unfitted but the wiring page still shades them as optos; that printed
		# construction is preserved even though the position is unused.
		self.assertTrue(self.switches[116]["normally_closed"])
		self.assertTrue(self.switches[118]["normally_closed"])
		self.assertNotIn("normally_closed", self.switches[115])
		self.assertNotIn("wiring", self.switches[115])
		self.assertIn("wiring", self.switches[116])
		self.assertIn("wiring", self.switches[118])
		spinner = self.switches[117]
		self.assertEqual("Center Spinner", spinner["label"])
		self.assertEqual("used", spinner["availability"])
		self.assertFalse(spinner["normally_closed"])
		self.assertEqual("validated", spinner["spatial"]["status"])

	def test_the_full_wpc95_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in range(17, 27):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (27, 28, 37, 38):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (29, 30, 31, 32, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_flipper_manual_address_mapping_and_lpdc_mirror(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48, 41, 42)
		}
		self.assertEqual({"29"}, manual_aliases[45])
		self.assertEqual({"30"}, manual_aliases[46])
		self.assertEqual({"31"}, manual_aliases[47])
		self.assertEqual({"32"}, manual_aliases[48])
		self.assertEqual({"37"}, manual_aliases[41])
		self.assertEqual({"38"}, manual_aliases[42])
		self.assertEqual("Dracula Motor Forward", self.solenoids[37]["label"])
		self.assertEqual("motor", self.solenoids[37]["kind"])
		self.assertEqual("used", self.solenoids[37]["availability"])
		self.assertEqual("Dracula Motor Backward", self.solenoids[38]["label"])
		self.assertEqual("Dracula Motor Forward LPDC Mirror", self.solenoids[41]["label"])
		self.assertEqual("virtual", self.solenoids[41]["kind"])
		self.assertEqual("used", self.solenoids[41]["availability"])
		self.assertEqual(["internal.duplicate.lpdc-mirror"], self.solenoids[41]["roles"])
		self.assertNotIn("wiring", self.solenoids[41])
		self.assertEqual("Dracula Motor Backward LPDC Mirror", self.solenoids[42]["label"])
		self.assertEqual("virtual", self.solenoids[42]["kind"])
		self.assertEqual("used", self.solenoids[42]["availability"])

	def test_unfitted_solenoids_are_enumerated_and_none_is_labelled_knocker(self) -> None:
		for address in (4, 7, 33, 34, 35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)
		for device in self.solenoids.values():
			self.assertNotIn("knocker", device["label"].lower())
		self.assertIn("sKnocker", self.solenoids[7]["physical"]["notes"])
		self.assertIn("solKnocker", self.solenoids[7]["physical"]["notes"])
		self.assertIn("no knocker coil", self.solenoids[7]["physical"]["notes"])

	def test_physical_solenoid_wiring_connections_are_unique(self) -> None:
		connections: dict[str, int] = {}
		for address, device in self.solenoids.items():
			if device["kind"] == "virtual" or device["availability"] != "used":
				continue
			wiring = device.get("wiring", {})
			connection = wiring.get("control_connection")
			if not connection:
				continue
			key = (wiring.get("board"), connection)
			self.assertNotIn(key, connections, f"{address} duplicates {connections.get(key)}")
			connections[key] = address
		self.assertEqual("J116-1", self.solenoids[1]["wiring"]["control_connection"])
		self.assertEqual("Q72", self.solenoids[1]["wiring"]["driver_transistor"])
		self.assertEqual("J110-1", self.solenoids[37]["wiring"]["control_connection"])
		self.assertEqual("J110-3", self.solenoids[38]["wiring"]["control_connection"])

	def test_gi_playfield_strings_are_located_and_insert_panel_strings_are_cabinet(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(34, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(39, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(15, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		for address in (12, 24, 31, 43):
			self.assertEqual(2, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.lamps[address]["spatial"]["placements"]), address)
		for address in sorted(MATRIX_ADDRESSES - {12, 24, 31, 43, 78, 87, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
		self.assertEqual("unused", self.lamps[78]["availability"])
		self.assertEqual("unused", self.lamps[78]["spatial"]["reason"])
		for address in (87, 88):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual("Drac-Attack", self.lamps[14]["label"])
		self.assertEqual("Quarter Moon", self.lamps[31]["label"])
		self.assertEqual("Three-Quarter Moon", self.lamps[43]["label"])
		self.assertEqual("Left Gargle", self.lamps[48]["label"])

	def test_every_spatial_placement_is_validated_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		located = 0
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			spatial = device["spatial"]
			if spatial["status"] == "not_applicable":
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
		self.assertEqual([], report["unresolved"])
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		# Top lanes ascend left -> center -> right for both switches and lamps.
		self.assertLess(switch_x[56], switch_x[57])
		self.assertLess(switch_x[57], switch_x[58])
		self.assertLess(lamp_x[37], lamp_x[36])
		self.assertLess(lamp_x[36], lamp_x[35])
		# Blue targets ascend left -> center -> right for both switches and lamps.
		self.assertLess(switch_x[44], switch_x[45])
		self.assertLess(switch_x[45], switch_x[46])
		self.assertLess(lamp_x[32], lamp_x[58])
		self.assertLess(lamp_x[58], lamp_x[44])
		# Outlane is outboard of return lane on both sides.
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		self.assertLess(switch_x[16], switch_x[26])
		self.assertGreater(switch_x[27], switch_x[17])
		# Jet bumpers: left is left of right, and bottom has the largest y.
		self.assertLess(switch_x[53], switch_x[54])
		self.assertGreater(switch_y[55], switch_y[53])
		self.assertGreater(switch_y[55], switch_y[54])
		# Dracula standups: top (12) behind bottom (15); lamps 34/38 keep the same order.
		self.assertLess(switch_y[12], switch_y[15])
		lamp_y = {addr: pos[1] for addr, pos in _emitter_positions(self.lamps).items()}
		self.assertLess(lamp_y[34], lamp_y[38])
		# Frankenstein body: head (74) has the smallest y and sits behind torso (73); left
		# arm/leg are left of right leg/arm.
		self.assertLess(lamp_y[74], lamp_y[73])
		self.assertLess(lamp_x[71], lamp_x[75])
		self.assertLess(lamp_x[72], lamp_x[75])
		self.assertLess(lamp_x[71], lamp_x[76])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.dracula",
				"mechanism.frankenstein-table", "mechanism.up-down-bank", "mechanism.mummy-coffin",
				"mechanism.bride-post", "mechanism.ramp-lock-post", "mechanism.ball-gates",
				"mechanism.left-eject", "mechanism.right-popper", "mechanism.slingshots",
				"mechanism.jet-bumpers", "mechanism.lower-flippers", "mechanism.center-spinner",
				"mechanism.flipper-proximity-sensors",
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
			for actuator in mechanism["actuators"]:
				self.assertNotIn(actuator, owners, actuator)
				owners[actuator] = mechanism["id"]
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("H-bridge", mechanisms["mechanism.dracula"]["behavior"])
		self.assertIn("90-step", mechanisms["mechanism.dracula"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-eject-opto"}, set(relationships))
		self.assertEqual("switch.matrix-31", relationships["relationship.trough-eject-opto"]["destination"])
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
		self.assertIn("vpx-script.mb-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.mb-vpw-1-0"]["known_working"])
		self.assertEqual(
			"b043d07c74693ce5c713a9edc1529413f3c2ec4420b63488085cd45e4fe413e8",
			sources["vpx-script.mb-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"bef48b75b072c3fc8b4803639cc65f54144db6ff7e9476f6ea6b1fc23bc68c8d",
			sources["vpx-table.mb-vpw-1-0"]["sha256"],
		)
		self.assertNotIn("runtime.monster-bash", sources)
		self.assertNotIn("rom.mb", sources)
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
		self.assertEqual("pinmame.wpc-95", profile["id"])
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


def _switch_positions(switches: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in switches.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


def _emitter_positions(lamps: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in lamps.items():
		spatial = device["spatial"]
		if spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class MonsterBashCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_monster_bash as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_monster_bash as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_monster_bash as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Monster Bash", b"Monster Sash", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_monster_bash as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class MonsterBashRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_monster_bash as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_monster_bash as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/monster-bash-1998/source/Monster Bash (Williams 1998) VPWmod v1.0.vpx"
		script = source_root / "williams/monster-bash-1998/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_monster_bash as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "monster-bash-1998" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
