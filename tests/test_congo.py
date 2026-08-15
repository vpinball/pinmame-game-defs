from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


from test_excerpts import DRAWING_LIMIT, IMAGE_LIMIT, PAGE_SCALE_DRAWINGS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "williams" / "congo-1995.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "congo-1995.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "williams" / "congo-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "congo-1995.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "congo-1995.json"

DRIVER_IDS = {"congo_21", "congo_20", "congo_20s10k", "congo_13", "congo_11"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 66, 81, 82, 83, 84, 85, 86, 87, 88}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 41, 42, 43}


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
	import curate_congo as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_congo.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class CongoDefinitionTests(unittest.TestCase):
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
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("williams.congo.1995", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(1995, self.definition["machine"]["year"])
		self.assertEqual("16-50050-101", self.definition["machine"]["model_number"])
		self.assertEqual(964.0, self.definition["machine"]["playfield"]["width"])
		self.assertEqual(2162.0, self.definition["machine"]["playfield"]["height"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertEqual([], self.definition["conflicts"])

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_every_congo_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual("congo_21", by_id["congo_20"]["clone_of"])
		self.assertEqual("congo_21", by_id["congo_20s10k"]["clone_of"])
		self.assertEqual("congo_21", by_id["congo_13"]["clone_of"])
		self.assertEqual("congo_21", by_id["congo_11"]["clone_of"])
		self.assertNotIn("clone_of", by_id["congo_21"])
		# congo_20s10k is the only driver using a genuinely different hardware-generation
		# constant (GEN_WPC95DCS instead of GEN_WPC95); it must be "compatible", not "identical".
		self.assertEqual("compatible", by_id["congo_20s10k"]["physical_compatibility"])
		for driver_id in ("congo_21", "congo_20", "congo_13", "congo_11"):
			self.assertEqual("identical", by_id[driver_id]["physical_compatibility"], driver_id)

	def test_the_full_wpc95_input_space_is_enumerated_except_column_eight(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		# Column 8 (81-88) is entirely unused on this machine.
		for address in range(81, 89):
			self.assertIn(address, UNUSED_MATRIX_ADDRESSES)
		for address in sorted(UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_printed_opto_polarity_matches_pinmames_mask_with_zero_disagreement(self) -> None:
		for address in sorted(MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES - {24}):
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)
		self.assertEqual("constant", self.switches[24]["kind"])
		self.assertTrue(self.switches[24]["constant_active"])
		self.assertTrue(self.switches[24]["initial_active"])
		self.assertEqual("constant", self.switches[24]["spatial"]["reason"])

	def test_the_inverted_switch_mask_normalizes_exactly_the_nine_opto_addresses(self) -> None:
		# congoGameData's inverted-switch mask: column 3 = 0x3f (rows 1-6 = 31-36),
		# column 4 = 0x07 (rows 1-3 = 41-43). Re-derive the bit positions in code rather than by
		# hand, per this project's established lesson about hand-computed bitmask errors.
		mask = (0x00, 0x00, 0x00, 0x3f, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)
		normalized = set()
		for column in (3, 4):
			for row in range(1, 9):
				if (mask[column] >> (row - 1)) & 1:
					normalized.add(column * 10 + row)
		self.assertEqual(OPTO_ADDRESSES, normalized)

	def test_flipper_positions_upper_right_unfitted_upper_left_fitted(self) -> None:
		for address in (111, 112, 113, 114, 117, 118):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertTrue(self.switches[118]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])
		self.assertFalse(self.switches[117]["normally_closed"])
		# 116 is unfitted but the wiring page still shades it as an opto template.
		self.assertTrue(self.switches[116]["normally_closed"])
		self.assertNotIn("normally_closed", self.switches[115])
		self.assertNotIn("wiring", self.switches[115])
		self.assertIn("wiring", self.switches[116])
		upper_left = self.switches[118]
		self.assertEqual("Upper Left Flipper Button", upper_left["label"])
		self.assertEqual("used", upper_left["availability"])

	def test_the_full_wpc95_output_space_is_enumerated_with_honest_kinds(self) -> None:
		expected_solenoids = set(range(1, 51))
		self.assertEqual(expected_solenoids, set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		for address in list(range(17, 22)) + list(range(25, 29)):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (29, 30, 32, 37, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)
		self.assertEqual("used", self.solenoids[31]["availability"])
		self.assertEqual("used", self.solenoids[29]["availability"])
		# Congo fits all 28 low-numbered solenoid positions -- no gaps.
		for address in range(1, 29):
			self.assertEqual("used", self.solenoids[address]["availability"], address)

	def test_flipper_manual_address_mapping(self) -> None:
		manual_aliases = {
			address: {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			for address in (45, 46, 47, 48, 33, 34, 35, 36)
		}
		self.assertEqual({"29"}, manual_aliases[45])
		self.assertEqual({"30"}, manual_aliases[46])
		self.assertEqual({"31"}, manual_aliases[47])
		self.assertEqual({"32"}, manual_aliases[48])
		# 33-36 already equal their printed circuit numbers -- no translation alias.
		for address in (33, 34, 35, 36):
			self.assertEqual({f"{address:02d}"}, manual_aliases[address])
		self.assertEqual("Upper Left Post", self.solenoids[33]["label"])
		self.assertEqual("Mystery Eject", self.solenoids[34]["label"])
		self.assertEqual("Upper Left Flipper Power", self.solenoids[35]["label"])
		self.assertEqual("Upper Left Flipper Hold", self.solenoids[36]["label"])
		self.assertEqual("coil", self.solenoids[33]["kind"])
		self.assertEqual("coil", self.solenoids[34]["kind"])

	def test_gorilla_left_right_naming_is_resolved_from_the_manual_self_contradiction(self) -> None:
		self.assertEqual("Gorilla Left", self.solenoids[15]["label"])
		self.assertEqual("Gorilla Right", self.solenoids[16]["label"])
		notes15 = self.solenoids[15]["physical"]["notes"]
		notes16 = self.solenoids[16]["physical"]["notes"]
		self.assertIn("manual self-contradiction", notes15.lower())
		self.assertIn("manual self-contradiction", notes16.lower())

	def test_map_and_gates_are_coils_not_flashers_despite_the_printed_driver_bank(self) -> None:
		for address, label in ((22, "Map Eject"), (23, "Left Gate"), (24, "Right Gate")):
			self.assertEqual(label, self.solenoids[address]["label"])
			self.assertEqual("coil", self.solenoids[address]["kind"])
			self.assertIn("driver-board circuit", self.solenoids[address]["physical"]["notes"])

	def test_no_solenoid_is_labelled_a_magnet(self) -> None:
		for device in self.solenoids.values():
			self.assertNotEqual("magnet", device["kind"])
			self.assertNotIn("magnet", device["label"].lower())

	def test_physical_solenoid_wiring_connections_are_unique(self) -> None:
		connections: dict[tuple[object, str], int] = {}
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

	def test_gi_playfield_strings_are_located_and_backbox_strings_are_cabinet(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(5, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(13, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(16, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_labels_and_com_typo_resolution(self) -> None:
		self.assertEqual("(C)ongo", self.lamps[11]["label"])
		self.assertEqual("Com", self.lamps[72]["label"])
		self.assertIn("Corn", self.lamps[72]["physical"]["notes"])
		self.assertEqual("Travi", self.lamps[71]["label"])
		self.assertEqual("Not Used Lamp Position 87", self.lamps[87]["label"])
		self.assertEqual("unused", self.lamps[87]["availability"])
		self.assertEqual("not_applicable", self.lamps[88]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", self.lamps[88]["spatial"]["reason"])

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
		self.assertEqual([25], report["unresolved_input_addresses"])
		self.assertEqual(located, report["placement_count"])

	def test_switch_25_has_no_invented_coordinate(self) -> None:
		self.assertNotIn("spatial", self.switches[25])
		self.assertIn("No VPX object supplies a reliable coordinate", self.switches[25]["physical"]["notes"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		# Left/right jet bumpers ascend left -> right; bottom sits further toward the player.
		self.assertLess(switch_pos[63][0], switch_pos[64][0])
		self.assertGreater(switch_pos[65][1], switch_pos[63][1])
		self.assertGreater(switch_pos[65][1], switch_pos[64][1])
		# Left bank top/center/bottom descend the playfield in that printed order (ascending y).
		self.assertLess(switch_pos[46][1], switch_pos[47][1])
		self.assertLess(switch_pos[47][1], switch_pos[48][1])
		# Slingshots: left is left of right.
		self.assertLess(switch_pos[61][0], switch_pos[62][0])
		# Ramp enter is closer to the player (larger y) than ramp exit, both ramps.
		self.assertGreater(switch_pos[57][1], switch_pos[58][1])
		self.assertGreater(switch_pos[67][1], switch_pos[68][1])
		# CONGO standup targets ascend left -> right in printed C-O-N-G-O order.
		self.assertLess(switch_pos[74][0], switch_pos[75][0])
		self.assertLess(switch_pos[75][0], switch_pos[76][0])
		self.assertLess(switch_pos[76][0], switch_pos[77][0])
		self.assertLess(switch_pos[77][0], switch_pos[78][0])
		# AMY rollovers ascend left -> right in printed A-M-Y order.
		self.assertLess(switch_pos[71][0], switch_pos[72][0])
		self.assertLess(switch_pos[72][0], switch_pos[73][0])
		# Gorilla Left/Right solenoids: left arm is left of right arm.
		gorilla_left = self.solenoids[15]["spatial"]["placements"][0]
		gorilla_right = self.solenoids[16]["spatial"]["placements"][0]
		self.assertLess(gorilla_left["x"], gorilla_right["x"])

	def test_mechanism_inventory_covers_every_used_coil_or_motor(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.kickback",
				"mechanism.two-way-popper", "mechanism.ramp-diverter", "mechanism.volcano",
				"mechanism.top-loop-post", "mechanism.mystery-saucer", "mechanism.map-saucer",
				"mechanism.gates", "mechanism.upper-left-post", "mechanism.gray-gorilla",
				"mechanism.slingshots", "mechanism.jet-bumpers", "mechanism.lower-flippers",
				"mechanism.upper-left-flipper",
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
		# The knocker is a standard cabinet-service coil, not a documented "mechanism" in the
		# schema sense (no topology/behavior worth a dedicated record); Medieval Madness
		# (author-ready) leaves its own knocker unowned by any mechanism for the same reason.
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
			and "cabinet.knocker" not in device.get("roles", [])
		}
		self.assertEqual(set(), physical - set(owners))
		self.assertIn("no magnet", mechanisms["mechanism.gray-gorilla"]["behavior"].lower())

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
		self.assertIn("vpx-script.congo-jpsalas-nfozzy", sources)
		self.assertTrue(sources["vpx-script.congo-jpsalas-nfozzy"]["known_working"])
		self.assertEqual(
			"19c19ea64bb120af66ef3ca309a2ec98c08b35ecf08e198bb26b3cd1611cd936",
			sources["vpx-script.congo-jpsalas-nfozzy"]["sha256"],
		)
		self.assertEqual(
			"45a6448efb586475a6886962c5bace44789be1d7cd3dde2c507169fdf085432c",
			sources["vpx-table.congo-jpsalas-nfozzy"]["sha256"],
		)
		self.assertEqual(
			"2770692875d10e7cc5bdd11a823ceb9ecfd2f374ed196207ca66631127b77f40",
			sources["manual.williams.congo.1995"]["sha256"],
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

	def test_manual_source_excerpts_exist_and_hash_match(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual = sources["manual.williams.congo.1995"]
		self.assertGreaterEqual(len(manual["excerpts"]), 6)
		for excerpt in manual["excerpts"]:
			path = ROOT / excerpt["path"]
			self.assertTrue(path.is_file(), excerpt["path"])
			import hashlib

			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			self.assertEqual(excerpt["sha256"], digest, excerpt["id"])
			self.assertTrue(excerpt["reviewed"], excerpt["id"])
			if "image" in excerpt:
				image_path = ROOT / excerpt["image"]
				self.assertTrue(image_path.is_file(), excerpt["image"])
				image_digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
				self.assertEqual(excerpt["image_sha256"], image_digest, excerpt["id"])
				# Defer to the shared budget rather than restate it: this machine's
				# switch-locations crop is a page-scale drawing, and a second copy of
				# the rule here would have to be kept in step with tests/test_excerpts.py.
				limit = DRAWING_LIMIT if excerpt["id"] in PAGE_SCALE_DRAWINGS else IMAGE_LIMIT
				self.assertLessEqual(image_path.stat().st_size, limit, excerpt["id"])

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


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class CongoCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_congo as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_congo as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_congo as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Congo", b"Kongo", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_congo as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class CongoRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_congo as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_congo as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/congo-1995/source/Congo (Williams 1995) 1.1.vpx"
		script = source_root / "williams/congo-1995/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))


if __name__ == "__main__":
	unittest.main()
