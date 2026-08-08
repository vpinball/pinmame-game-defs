from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "white-water-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "white-water-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "white-water-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "white-water.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "white-water-1993.json"

DRIVER_IDS = {
	"ww_l5", "ww_d5", "ww_lh5", "ww_lh6", "ww_lh6c", "ww_l4", "ww_d4", "ww_l3", "ww_d3",
	"ww_l2", "ww_d2", "ww_p8", "ww_p9", "ww_p6",
	"ww_bfr01", "ww_bfr01b", "ww_bfr01c", "ww_bfr01d", "ww_bfr01e",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {11, 12, 67, 72, 81, 82, 83, 84, 85, 88}
OPTO_ADDRESSES = {61, 62, 63, 64, 65, 66, 68, 86, 87}
PINMAME_NORMALIZED_OPTO_ADDRESSES = {61, 62, 63, 64, 65, 67, 68, 86, 87}
AUX_LAMP_ADDRESSES = set(range(91, 99)) | set(range(101, 109))


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
	import curate_white_water as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_white_water.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class WhiteWaterDefinitionTests(unittest.TestCase):
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
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("candidate", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension == "spatial_placement":
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.white-water.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2768, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_opto_polarity_sweep_found_zero_disagreement(self) -> None:
		# Unlike Monster Bash's Dracula-position optos, every address White Water prints with opto/
		# proximity construction is also normalized by wwGameData's inverted-switch mask, so there is
		# no conflicts entry for switch polarity on this machine.
		self.assertEqual([], self.definition["conflicts"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_ww_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("ww_l5", by_id["ww_lh6"]["clone_of"])
		self.assertNotIn("clone_of", by_id["ww_l5"])

	def test_the_full_wpc_fliptronic_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_is_recorded_even_where_pinmame_does_not_normalize_it(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_column_6_and_8_opto_masks_cover_every_printed_opto_address(self) -> None:
		import curate_white_water as curator

		# Column 6's inverted-switch mask is 0xbf = 0b10111111: bits 0-5 and 7 set, covering rows
		# 1-6 and 8 (switches 61-66, 68). The only clear bit is bit 6 (row 7 = switch 67), which is
		# printed "Not Used" anyway. Column 8's mask is 0x60 = 0b01100000, covering rows 6-7
		# (switches 86, 87). Together these are exactly OPTO_SWITCHES -- a clean sweep.
		self.assertEqual(0xBF, 0b10111111)
		self.assertEqual(1, (0xBF >> 5) & 1)
		self.assertEqual(0, (0xBF >> 6) & 1)
		self.assertEqual(curator.OPTO_SWITCHES, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		self.assertEqual({61, 62, 63, 64, 65, 66, 68, 86, 87}, curator.OPTO_SWITCHES)

	def test_flipper_positions(self) -> None:
		for address in (111, 112, 113, 114, 115, 116):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertTrue(self.switches[116]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertFalse(self.switches[115]["normally_closed"])
		self.assertNotIn("normally_closed", self.switches[117])
		# F7/F8 are unfitted (no upper-left flipper), but the switch-matrix wiring page still prints
		# their generic column template, so both retain a wiring record despite being unused.
		self.assertIn("wiring", self.switches[117])
		self.assertIn("wiring", self.switches[118])

	def test_the_full_wpc_fliptronic_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES | AUX_LAMP_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in list(range(8, 10)) + list(range(15, 25)):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (25, 26):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in (27, 28):
			self.assertEqual("control_signal", self.solenoids[address]["kind"], address)
		for address in (29, 30):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		self.assertEqual("virtual", self.solenoids[31]["kind"])
		self.assertEqual("used", self.solenoids[31]["availability"])
		self.assertEqual(["internal.wpc-state"], self.solenoids[31]["roles"])
		self.assertEqual("virtual", self.solenoids[31]["spatial"]["reason"])
		self.assertIn("no physical Game-On solenoid", self.solenoids[31]["physical"]["notes"])
		self.assertIn('SolCallback(31)="TiltSol"', self.solenoids[31]["physical"]["notes"])
		self.assertEqual("virtual", self.solenoids[32]["kind"])
		self.assertEqual("unused", self.solenoids[32]["availability"])
		self.assertEqual(["internal.unused.wpc-output"], self.solenoids[32]["roles"])
		self.assertEqual("virtual", self.solenoids[32]["spatial"]["reason"])
		for address in range(37, 45):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
		for address in (49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)

	def test_only_three_flippers_are_fitted(self) -> None:
		for address in (33, 34, 45, 46, 47, 48):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		for address in (35, 36):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)
			self.assertEqual("unused", self.solenoids[address]["spatial"]["reason"], address)

	def test_every_standard_solenoid_is_fitted(self) -> None:
		# Unlike Monster Bash, White Water genuinely has a fitted knocker: solenoid 7 is printed
		# with a real drive/voltage connection and a coil part number, not a blank one.
		for address in range(1, 29):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		self.assertEqual("Knocker", self.solenoids[7]["label"])
		self.assertEqual("coil", self.solenoids[7]["kind"])

	def test_auxiliary_chase_lamps_are_backbox_devices(self) -> None:
		for address in sorted(AUX_LAMP_ADDRESSES):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"], address)
			self.assertEqual(["cabinet.chase-lamp"], lamp["roles"], address)

	def test_lamps_17_and_55_are_fitted_but_unpositioned(self) -> None:
		for address in (17, 55):
			lamp = self.lamps[address]
			self.assertEqual("used", lamp["availability"], address)
			self.assertNotIn("spatial", lamp, address)

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(29, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(21, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.backbox"], self.gi[address]["roles"], address)

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
		self.assertEqual("candidate", report["status"])
		self.assertEqual(2, len(report["unresolved"]))
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = _positions(self.switches)
		lamp_x = _positions(self.lamps)
		# River standup targets spell R-I-V-E-R reading rear-to-front (ascending y): 35=R1, 34=I, 33=V,
		# 32=E, 31=R2.
		self.assertLess(switch_x[35][1], switch_x[34][1])
		self.assertLess(switch_x[34][1], switch_x[33][1])
		self.assertLess(switch_x[33][1], switch_x[32][1])
		self.assertLess(switch_x[32][1], switch_x[31][1])
		# Left/right outlanes and flipper lanes ascend left -> right.
		self.assertLess(switch_x[25][0], switch_x[28][0])
		self.assertLess(switch_x[26][0], switch_x[27][0])
		self.assertLess(switch_x[51][0], switch_x[52][0])
		# Lockup lane: right kicker has a larger x than center, center larger than left.
		self.assertGreater(switch_x[63][0], switch_x[64][0])
		self.assertGreater(switch_x[64][0], switch_x[65][0])
		# Hot Foot upper sits behind (smaller y) Hot Foot lower.
		self.assertLess(switch_x[73][1], switch_x[74][1])
		# River lamps also spell R-I-V-E-R rear-to-front, in ascending address order this time
		# (21=R1, 22=I, 23=V, 24=E, 25=R2): the lamp matrix and switch matrix are independently
		# numbered, so there is no requirement the two share a reading direction.
		self.assertLess(lamp_x[21][1], lamp_x[22][1])
		self.assertLess(lamp_x[22][1], lamp_x[23][1])
		self.assertLess(lamp_x[23][1], lamp_x[24][1])
		self.assertLess(lamp_x[24][1], lamp_x[25][1])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.whirlpool", "mechanism.lockup",
				"mechanism.bigfoot-head", "mechanism.ramp-diverter", "mechanism.kickback",
				"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.lower-flippers",
				"mechanism.upper-right-flipper", "mechanism.chase-lamp-board", "mechanism.knocker",
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
		self.assertIn("96-step", mechanisms["mechanism.bigfoot-head"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.whirlpool-tunnel-exit"}, set(relationships))
		self.assertEqual("switch.matrix-62", relationships["relationship.whirlpool-tunnel-exit"]["destination"])
		self.assertEqual("pulse", relationships["relationship.whirlpool-tunnel-exit"]["kind"])

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
		self.assertIn("vpx-script.ww-flupper", sources)
		self.assertTrue(sources["vpx-script.ww-flupper"]["known_working"])
		self.assertEqual(
			"0676acb1e610bda8f42f94a915a70bb1b71b6e48462326dd43083a3ab4fa0096",
			sources["vpx-script.ww-flupper"]["sha256"],
		)
		self.assertEqual(
			"7c59095e9c6a7e100e79f80d7d83497b1c87817bc9daf939721f1a8727a781cd",
			sources["vpx-table.ww-flupper"]["sha256"],
		)
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
		self.assertEqual("pinmame.wpc-fliptronic", profile["id"])
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


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class WhiteWaterCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_white_water as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_white_water as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_white_water as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"White Water", b"White Wager", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_white_water as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class WhiteWaterRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_white_water as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_white_water as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/white-water-1993/source/Whitewater (Williams 1993).vpx"
		script = source_root / "williams/white-water-1993/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_white_water as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "white-water" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
