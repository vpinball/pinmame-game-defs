from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "williams" / "medieval-madness-1997.json"
SEED_PATH = ROOT / "tools" / "seeds" / "williams" / "medieval-madness-1997.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "williams" / "medieval-madness-1997.json"
STUB_PATH = ROOT / "machines" / "stubs" / "mm_10.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "williams" / "medieval-madness-1997.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "wpc-95" / "medieval-madness-boot-start-and-service.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "williams" / "medieval-madness-1997.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

DRIVER_IDS = {"mm_05", "mm_10", "mm_109", "mm_109b", "mm_109c", "mm_10pfx", "mm_10u"}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {23, 42, 43, 76, 77, 78} | {80 + row for row in range(1, 9)}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37, 41}


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
	import curate_medieval_madness as curator
	import sys

	argv = sys.argv
	sys.argv = ["curate_medieval_madness.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class MedievalMadnessDefinitionTests(unittest.TestCase):
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
		self.assertEqual("williams.medieval-madness.1997", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(4032, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1997, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-95", self.definition["controller"]["platform"])
		self.assertEqual("0x80", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_the_stale_partial_and_generated_stub_are_gone(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())
		self.assertFalse(STUB_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertNotIn("partial", KNOWLEDGE_PATH.read_text(encoding="utf-8").splitlines()[2])

	def test_every_mm_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		catalog = load_json(CATALOG_PATH)
		catalog_drivers = {
			record["id"]
			for record in catalog["drivers"]
			if record["machine_id"] == "williams.medieval-madness.1997"
		}
		self.assertEqual(DRIVER_IDS, catalog_drivers)
		machine = next(record for record in catalog["machines"] if record["id"] == "williams.medieval-madness.1997")
		self.assertEqual("author_ready", machine["coverage_status"])
		self.assertEqual("machines/author-ready/williams/medieval-madness-1997.json", machine["definition"])
		self.assertEqual(["mm_10"], machine["root_drivers"])

	def test_the_virtual_only_ports_stay_compatible_rom_variants_not_separate_machines(self) -> None:
		by_id = {driver["id"]: driver for driver in self.definition["drivers"]}
		for driver_id in ("mm_10pfx", "mm_10u"):
			self.assertEqual("compatible", by_id[driver_id]["physical_compatibility"])
			self.assertIn("display text", by_id[driver_id]["variant_notes"])
		self.assertEqual("mm_10", by_id["mm_10pfx"]["clone_of"])
		self.assertEqual("mm_10", by_id["mm_10u"]["clone_of"])

	def test_the_full_wpc95_input_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119)), set(self.switches))
		self.assertEqual(set(range(1, 9)), set(bindings(self.definition, "inputs", "pinmame.input.dip")))
		self.assertEqual(88, len(self.definition["inputs"]))
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

	def test_coin_door_service_order_follows_the_manual_and_the_runtime_probe(self) -> None:
		self.assertEqual("Service Credits / Escape", self.switches[5]["label"])
		self.assertEqual("Volume Down / Down", self.switches[6]["label"])
		self.assertEqual("Volume Up / Up", self.switches[7]["label"])
		self.assertEqual("Begin Test / Enter", self.switches[8]["label"])
		self.assertEqual(["service.enter"], self.switches[8]["roles"])
		self.assertIn("runtime.medieval-madness.boot-start-and-service", self.switches[8]["provenance"]["source_refs"])
		for address in (6, 7):
			self.assertIn("runtime.medieval-madness.boot-start-and-service", self.switches[address]["provenance"]["source_refs"], address)
		evidence = load_json(EVIDENCE_PATH)
		texts = {snapshot["interpreted_text"] for snapshot in evidence["runtime"]["observations"]["diagnostic_snapshots"]}
		self.assertIn("TO RESET SCORES- HOLD ENTER----4", texts)
		# Switch 7 raised the ROM's own volume display and switch 6 lowered it, which pins the
		# direction of the pair rather than inferring it from the printed table alone.
		self.assertIn("VOLUME (15)", texts)
		self.assertIn("VOLUME (12)", texts)

	def test_upper_flipper_positions_are_explicitly_not_installed(self) -> None:
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)
		for address in (115, 116, 117, 118):
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("unused", self.switches[address]["spatial"]["reason"], address)
			self.assertNotIn("wiring", self.switches[address])
		self.assertTrue(self.switches[112]["normally_closed"])
		self.assertTrue(self.switches[114]["normally_closed"])
		self.assertFalse(self.switches[111]["normally_closed"])
		self.assertFalse(self.switches[113]["normally_closed"])

	def test_the_full_wpc95_output_space_is_enumerated_with_honest_kinds(self) -> None:
		self.assertEqual(set(range(1, 51)), set(self.solenoids))
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		self.assertEqual(set(range(0, 5)), set(self.gi))
		self.assertEqual(119, len(self.definition["outputs"]))
		for address in range(17, 26):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
			self.assertEqual(2, self.solenoids[address]["physical"]["quantity"], address)
		self.assertEqual("motor", self.solenoids[37]["kind"])
		for address in (29, 30, 31, 32, 38, 39, 40, 41, 42, 43, 44, 49, 50):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("virtual", self.solenoids[address]["spatial"]["reason"], address)

	def test_the_lpdc_mirror_is_one_motor_not_two(self) -> None:
		self.assertEqual("Drawbridge Motor", self.solenoids[37]["label"])
		self.assertEqual("used", self.solenoids[37]["availability"])
		self.assertEqual("Drawbridge Motor LPDC Mirror", self.solenoids[41]["label"])
		self.assertEqual("virtual", self.solenoids[41]["kind"])
		self.assertEqual("used", self.solenoids[41]["availability"])
		self.assertEqual(["internal.duplicate.lpdc-mirror"], self.solenoids[41]["roles"])
		self.assertNotIn("wiring", self.solenoids[41])
		manual_aliases = {alias["value"] for alias in self.solenoids[41]["aliases"] if alias["namespace"] == "manual.address"}
		self.assertEqual({"37"}, manual_aliases)

	def test_troll_circuits_keep_physical_kind_separate_from_fliptronic_transport(self) -> None:
		for address, label in ((33, "Left Troll Power"), (34, "Left Troll Hold"), (35, "Right Troll Power"), (36, "Right Troll Hold")):
			self.assertEqual(label, self.solenoids[address]["label"], address)
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
			self.assertEqual("FL-11753", self.solenoids[address]["physical"]["part_number"], address)
		for address, manual_address in ((45, "29"), (46, "30"), (47, "31"), (48, "32")):
			aliases = {alias["value"] for alias in self.solenoids[address]["aliases"] if alias["namespace"] == "manual.address"}
			self.assertEqual({manual_address}, aliases, address)

	def test_physical_solenoid_wiring_is_unique_and_manual_sourced(self) -> None:
		connections: dict[str, int] = {}
		for address, device in self.solenoids.items():
			if device["kind"] == "virtual" or "wiring" not in device:
				continue
			connection = device["wiring"]["control_connection"]
			self.assertNotIn(connection, connections, f"{address} duplicates {connections.get(connection)}")
			connections[connection] = address
		self.assertEqual("J116-1", self.solenoids[1]["wiring"]["control_connection"])
		self.assertEqual("Q72", self.solenoids[1]["wiring"]["driver_transistor"])
		self.assertEqual("J110-1", self.solenoids[37]["wiring"]["control_connection"])
		self.assertEqual("U3A and U3B", self.solenoids[37]["wiring"]["driver_transistor"])

	def test_gi_playfield_strings_are_located_and_insert_panel_strings_are_cabinet(self) -> None:
		for address in (0, 1, 2):
			self.assertEqual("validated", self.gi[address]["spatial"]["status"], address)
			placements = self.gi[address]["spatial"]["placements"]
			self.assertEqual(self.gi[address]["physical"]["quantity"], len(placements), address)
		self.assertEqual(10, len(self.gi[0]["spatial"]["placements"]))
		self.assertEqual(12, len(self.gi[1]["spatial"]["placements"]))
		self.assertEqual(11, len(self.gi[2]["spatial"]["placements"]))
		for address in (3, 4):
			self.assertEqual("not_applicable", self.gi[address]["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", self.gi[address]["spatial"]["reason"], address)
			self.assertEqual(["cabinet.insert-panel"], self.gi[address]["roles"], address)

	def test_lamp_quantities_and_cabinet_lamps_are_explicit(self) -> None:
		self.assertEqual(2, self.lamps[15]["physical"]["quantity"])
		self.assertEqual(1, len(self.lamps[15]["spatial"]["placements"]))
		self.assertEqual(2, self.lamps[78]["physical"]["quantity"])
		self.assertEqual(2, len(self.lamps[78]["spatial"]["placements"]))
		for address in (87, 88):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"], address)
		self.assertEqual("Magic Shield", self.lamps[72]["label"])
		self.assertIn("Ball Save", self.lamps[72]["physical"]["notes"])

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

	def test_mechanism_inventory_covers_every_custom_assembly(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.shooter-lane", "mechanism.drawbridge", "mechanism.castle-gate",
				"mechanism.exploding-castle", "mechanism.left-popper", "mechanism.tower", "mechanism.left-troll",
				"mechanism.right-troll", "mechanism.catapult", "mechanism.merlin-eject", "mechanism.loop-gates",
				"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.right-target-bank",
				"mechanism.lower-flippers",
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
		self.assertEqual([], mechanisms["mechanism.right-target-bank"]["actuators"])
		# Every used physical coil or motor is owned by exactly one mechanism except the backbox knocker.
		physical = {
			device["id"]
			for device in self.definition["outputs"]
			if device["kind"] in {"coil", "motor"} and device["availability"] == "used"
		}
		self.assertEqual({"device.knocker"}, physical - set(owners))
		self.assertEqual("motorized", mechanisms["mechanism.drawbridge"]["kind"])
		self.assertIn("500-step position counter", mechanisms["mechanism.drawbridge"]["behavior"])
		self.assertIn("Left Loop High (66)", mechanisms["mechanism.loop-gates"]["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual(
			{"relationship.trough-eject-opto", "relationship.left-troll-up", "relationship.right-troll-up"},
			set(relationships),
		)
		self.assertEqual("switch.matrix-31", relationships["relationship.trough-eject-opto"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-eject-opto"]["kind"])
		self.assertEqual("direct", relationships["relationship.left-troll-up"]["kind"])
		self.assertEqual("switch.matrix-74", relationships["relationship.left-troll-up"]["destination"])
		self.assertEqual("switch.matrix-75", relationships["relationship.right-troll-up"]["destination"])

	def test_july_1997_production_split_records_both_assemblies(self) -> None:
		import curate_medieval_madness as curator

		self.assertEqual(
			{"A-21712-5", "A-22027", "A-22034", "A-22033", "A-22036"},
			set(curator.PRODUCTION_SPLIT),
		)
		affected = []
		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			assembly = device.get("physical", {}).get("assembly_part_number")
			if assembly in curator.PRODUCTION_SPLIT:
				affected.append(device["id"])
				early = curator.PRODUCTION_SPLIT[assembly][0]
				notes = device["physical"]["notes"]
				self.assertIn("before July 21, 1997", notes, device["id"])
				self.assertIn(early, notes, device["id"])
		# Trolls, drawbridge gate/motor, drawbridge switches, left popper and tower lock post.
		self.assertGreaterEqual(len(affected), 9)

	def test_upper_flipper_template_disagreement_is_recorded(self) -> None:
		for address in (115, 116, 117, 118):
			notes = self.switches[address]["physical"]["notes"]
			self.assertIn("2-48", notes, address)
			self.assertIn("3-11", notes, address)
			self.assertIn("Basket", notes, address)

	def test_gi_insert_panel_strings_do_not_assert_an_unpublished_count(self) -> None:
		for address in (3, 4):
			physical = self.gi[address]["physical"]
			self.assertNotIn("quantity", physical, address)
			self.assertIn("6.3 V", physical["notes"], address)
			self.assertIn("up to 18 bulbs", physical["notes"], address)
			self.assertIn("not asserted", physical["notes"], address)

	def test_fast_flip_state_is_not_described_as_ball_in_play_only(self) -> None:
		notes = self.solenoids[31]["physical"]["notes"]
		self.assertIn("fast-flip flag", notes)
		self.assertNotIn("only while a ball was in play", notes)
		self.assertIn("attract", notes)
		knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertNotIn("channel 31 active only while a ball is in play", knowledge)

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
		self.assertIn("vpx-script.mm-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.mm-vpw-1-0"]["known_working"])
		self.assertEqual(
			"cdc5590888d810a44b772ec327789362cd27dd7a6c58870bc148b2d87a0f90f8",
			sources["vpx-script.mm-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"9a05a555d03aca3d48d73b3e6566220b27fde46aa5d2517a08faacdbc58bcab9",
			sources["vpx-table.mm-vpw-1-0"]["sha256"],
		)
		for source in self.definition["sources"]:
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

	def test_runtime_observations_only_reference_declared_addresses(self) -> None:
		evidence = load_json(EVIDENCE_PATH)
		observations = evidence["runtime"]["observations"]
		self.assertEqual(sorted(MATRIX_ADDRESSES), observations["lamp_addresses_seen"])
		self.assertEqual([0, 1, 2, 3, 4], observations["gi_addresses_seen"])
		self.assertTrue(set(observations["solenoid_addresses_seen"]) <= set(self.solenoids))
		self.assertEqual(["williams.medieval-madness.1997"], evidence["machine_ids"])
		self.assertEqual(["mm_10"], evidence["driver_ids"])


class MedievalMadnessCuratorTests(unittest.TestCase):
	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_medieval_madness as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_medieval_madness as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		# Regression: a bare invocation used to fall through to generate() and rewrite the
		# canonical artifacts. argparse must reject it instead.
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_medieval_madness as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Medieval Madness", b"Medieval Sadness", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_visual_review_cache_is_pinned_and_present_when_the_artifact_root_is_configured(self) -> None:
		import curate_medieval_madness as curator

		report = load_json(SPATIAL_REPORT_PATH)
		cache = report["visual_review_cache"]
		self.assertEqual(len(curator.VISUAL_REVIEW_CACHE), len(cache["pages"]))
		for page in cache["pages"]:
			self.assertRegex(page["sha256"], r"^[0-9a-f]{64}$")
			self.assertTrue(page["note"].strip())
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, cache["transcription"]["sha256"])
		sources = {source["id"]: source for source in load_json(DEFINITION_PATH)["sources"]}
		self.assertEqual(
			curator.MANUAL_TRANSCRIPTION_SHA256,
			sources["manual-support.williams.medieval-madness.1997"]["sha256"],
		)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_medieval_madness as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class MedievalMadnessRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_medieval_madness as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_rendered_manual_pages_and_transcription_match_their_pinned_hashes(self) -> None:
		import curate_medieval_madness as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		manuals = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root or not manuals:
			self.skipTest("manual and review-artifact roots are not configured")
		transcription = Path(root) / "medieval-madness-1997" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))
		rendered = Path(manuals) / "rendered" / "williams.medieval-madness.1997"
		for relative_path, digest, _note in curator.VISUAL_REVIEW_CACHE:
			page = rendered / relative_path
			self.assertTrue(page.is_file(), relative_path)
			self.assertEqual(digest, curator._file_sha256(page), relative_path)

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_medieval_madness as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "williams/medieval-madness-1997/source/Medieval Madness (Williams 1997) VPW v1.0.vpx"
		script = source_root / "williams/medieval-madness-1997/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))


if __name__ == "__main__":
	unittest.main()
