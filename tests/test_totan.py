from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "tales-of-the-arabian-nights-1996.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "tales-of-the-arabian-nights-1996.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "tales-of-the-arabian-nights-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "tales-of-the-arabian-nights-1996.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "tales-of-the-arabian-nights-1996.json"

DRIVER_IDS = {"totan_04", "totan_12", "totan_13", "totan_14", "totan_15c"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37}


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
	import curate_totan as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_totan.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class TotanDefinitionTests(unittest.TestCase):
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
		self.assertEqual(["spatial_placement", "unresolved_conflicts"], self.definition["coverage"]["missing"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["physical_wiring"])
		self.assertEqual("conflicted", self.definition["coverage"]["dimensions"]["spatial_placement"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"physical_wiring", "spatial_placement"}:
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.tales-of-the-arabian-nights.1996", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(3824, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1996, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_gi_string_3_conflict_is_recorded_and_unresolved(self) -> None:
		conflicts = {conflict["id"]: conflict for conflict in self.definition["conflicts"]}
		self.assertEqual({"conflict.gi-string-3-playfield-binding"}, set(conflicts))
		conflict = conflicts["conflict.gi-string-3-playfield-binding"]
		self.assertGreaterEqual(len(conflict["source_refs"]), 2)
		description = conflict["description"].lower()
		self.assertIn("unresolved", description)
		self.assertIn("harness", description)
		self.assertIn("2", conflict["path"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_totan_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("totan_14", by_id["totan_04"]["clone_of"])
		self.assertEqual("totan_14", by_id["totan_12"]["clone_of"])
		self.assertEqual("totan_14", by_id["totan_13"]["clone_of"])
		self.assertEqual("totan_14", by_id["totan_15c"]["clone_of"])
		self.assertNotIn("clone_of", by_id["totan_14"])
		self.assertEqual("compatible", by_id["totan_15c"]["physical_compatibility"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_pinmame_with_zero_disagreement(self) -> None:
		import curate_totan as curator

		# Column index 3 (0-based) is 0x7f: rows 1-7 (addresses 31-37) are the only opto column, and
		# PinMAME normalizes exactly that set -- zero polarity conflicts on this game, unlike Monster
		# Bash's Dracula-position asymmetry.
		mask = (0x00, 0x00, 0x00, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		self.assertEqual(0x7f, mask[3])
		self.assertEqual(curator.OPTO_SWITCHES, curator.PINMAME_NORMALIZED_OPTO_SWITCHES)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_flipper_positions_no_repurposed_fliptronic_switch(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		# 116/118 are unfitted but the wiring page still shades them as optos; the printed construction
		# is preserved even though the position is unused. 115/117 are plain unfitted leaf templates.
		self.assertTrue(self.switches[116]["normally_closed"])
		self.assertTrue(self.switches[118]["normally_closed"])
		self.assertNotIn("normally_closed", self.switches[115])
		self.assertNotIn("normally_closed", self.switches[117])

	def test_the_full_wpc95_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 65))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in list(range(17, 21)) + list(range(22, 29)):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		self.assertEqual("motor", self.solenoids[21]["kind"])
		for address in (29, 30, 31, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		for address in range(51, 65):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_no_unfitted_solenoid_positions_between_1_and_36(self) -> None:
		# Unlike Monster Bash (4, 7, and unfitted 33-36), every printed position 1-36 on this game is
		# physically fitted; there is a real knocker on address 7.
		for address in list(range(1, 29)) + [33, 34, 35, 36]:
			self.assertEqual("used", self.solenoids[address]["availability"], address)
		self.assertIn("knocker", self.solenoids[7]["label"].lower())
		self.assertEqual("not_applicable", self.solenoids[7]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.solenoids[7]["spatial"]["reason"])

	def test_flipper_manual_address_mapping_no_upper_flipper_translation(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48, 33, 34, 35, 36)
		}
		self.assertEqual({"29"}, manual_aliases[45])
		self.assertEqual({"30"}, manual_aliases[46])
		self.assertEqual({"31"}, manual_aliases[47])
		self.assertEqual({"32"}, manual_aliases[48])
		# Printed 33-36 are NOT translated (contrast Monster Bash's 37/38 -> 41/42 LPDC mirror): this
		# game declares no FLIP_SOL(FLIP_UR)/FLIP_SOL(FLIP_UL) bit, so core_getSol serves them as plain
		# driver-board bits at their own printed address.
		self.assertEqual({"33"}, manual_aliases[33])
		self.assertEqual({"34"}, manual_aliases[34])
		self.assertEqual({"35"}, manual_aliases[35])
		self.assertEqual({"36"}, manual_aliases[36])
		self.assertEqual("Left Diverter Power", self.solenoids[33]["label"])
		self.assertEqual("Left Diverter Hold", self.solenoids[34]["label"])
		self.assertEqual("Vanish Magnet", self.solenoids[35]["label"])
		self.assertEqual("Loop Post Diverter", self.solenoids[36]["label"])
		for address in (33, 34, 35, 36):
			self.assertEqual("used", self.solenoids[address]["availability"], address)
			self.assertNotIn("flipper", self.solenoids[address]["label"].lower())

	def test_physical_solenoid_wiring_connections_are_unique(self) -> None:
		connections: dict[tuple[object, object], int] = {}
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

	def test_gi_backbox_strings_are_not_applicable_and_playfield_strings_are_unresolved(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)
		for address in (3, 4):
			self.assertNotIn("spatial", self.gi[address], address)
			self.assertEqual("used", self.gi[address]["availability"], address)

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		self.assertEqual(2, self.lamps[28]["physical"]["quantity"])
		self.assertEqual(2, len(self.lamps[28]["spatial"]["placements"]))
		for address in sorted(MATRIX_ADDRESSES - {28, 88}):
			self.assertEqual(1, self.lamps[address]["physical"]["quantity"], address)
			self.assertEqual(1, len(self.lamps[address]["spatial"]["placements"]), address)
			self.assertEqual("used", self.lamps[address]["availability"], address)
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])
		self.assertEqual(["cabinet.start"], self.lamps[88]["roles"])
		self.assertEqual("Magic Carpet", self.lamps[31]["label"])
		self.assertEqual("Outlane Special", self.lamps[28]["label"])
		self.assertEqual("Start Button", self.lamps[88]["label"])

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
		self.assertEqual("conflicted", report["status"])
		self.assertEqual(
			[
				{"group": "pinmame.output.gi", "address": 3, "reason": "no VPX object bound to this playfield GI address in the retained extraction"},
				{"group": "pinmame.output.gi", "address": 4, "reason": "no VPX object bound to this playfield GI address in the retained extraction"},
			],
			report["unresolved"],
		)
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_x = {addr: pos[0] for addr, pos in _switch_positions(self.switches).items()}
		switch_y = {addr: pos[1] for addr, pos in _switch_positions(self.switches).items()}
		lamp_x = {addr: pos[0] for addr, pos in _emitter_positions(self.lamps).items()}
		# Left/right standup banks: three distinct, monotonically-ordered target positions each.
		left_bank_y = [p["y"] for p in self.switches[61]["spatial"]["placements"]]
		right_bank_y = [p["y"] for p in self.switches[62]["spatial"]["placements"]]
		self.assertEqual(3, len(set(left_bank_y)))
		self.assertEqual(3, len(set(right_bank_y)))
		self.assertEqual(sorted(left_bank_y, reverse=True), left_bank_y)
		self.assertEqual(sorted(right_bank_y, reverse=True), right_bank_y)
		# Left jet bumper sits left of right jet bumper.
		self.assertLess(switch_x[53], switch_x[54])
		# Left cage opto sits left of right cage opto (mirrored inlanes).
		self.assertLess(switch_x[36], switch_x[37])
		# Outlane is outboard of inlane on both sides.
		self.assertLess(switch_x[16], switch_x[26])
		self.assertGreater(switch_x[27], switch_x[17])
		# Left slingshot sits left of right slingshot; lamp inserts agree.
		self.assertLess(switch_x[51], switch_x[52])
		self.assertLess(lamp_x[48], lamp_x[47])
		self.assertLess(lamp_x[47], lamp_x[46])
		# Lower-left flipper coil anchor sits left of lower-right flipper coil anchor.
		left_flip = self.solenoids[47]["spatial"]["placements"][0]
		right_flip = self.solenoids[45]["spatial"]["placements"][0]
		self.assertLess(left_flip["x"], right_flip["x"])
		# Outlane-special lamp pair: right-side placement has the larger x.
		outlane_positions = sorted(p["x"] for p in self.lamps[28]["spatial"]["placements"])
		self.assertLess(outlane_positions[0], 0.1)
		self.assertGreater(outlane_positions[1], 0.8)

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.knocker",
				"mechanism.trough", "mechanism.cages", "mechanism.vanishing-ball", "mechanism.lock",
				"mechanism.bazaar-scoop", "mechanism.ramp-magnet", "mechanism.ramp-diverter",
				"mechanism.playfield-diverter", "mechanism.loop-post-diverter",
				"mechanism.spinning-lamp-unit", "mechanism.genie", "mechanism.slingshots",
				"mechanism.jet-bumpers", "mechanism.lower-flippers", "mechanism.left-kicker",
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
		self.assertIn("no PinMAME mech table", mechanisms["mechanism.spinning-lamp-unit"]["behavior"])
		self.assertIn("rock angle", mechanisms["mechanism.genie"]["behavior"])

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
		self.assertIn("vpx-script.totan-jpsalas-flupper-1-0", sources)
		self.assertTrue(sources["vpx-script.totan-jpsalas-flupper-1-0"]["known_working"])
		self.assertEqual(
			"c4a742f2188c9e3dcba70a7717d5b8985bbd1d913cc05c17df3b2f9d341b876b",
			sources["vpx-script.totan-jpsalas-flupper-1-0"]["sha256"],
		)
		self.assertEqual(
			"487375925e6f44998cd416b6d28983f08144d2bfe7a1432ac9ad16af7b23fec0",
			sources["vpx-table.totan-jpsalas-flupper-1-0"]["sha256"],
		)
		self.assertNotIn("runtime.totan", sources)
		self.assertNotIn("rom.totan", sources)
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


class TotanCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_totan as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_totan as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_totan as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Tales of the Arabian Nights", b"Tales of the Arabian Days", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_totan as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class TotanRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_totan as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_totan as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/tales-of-the-arabian-nights-1996/source/Tales of the Arabian Nights (Williams 1996).vpx"
		script = source_root / "williams/tales-of-the-arabian-nights-1996/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_totan as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "tales-of-the-arabian-nights-1996" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))


if __name__ == "__main__":
	unittest.main()
