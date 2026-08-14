from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "bally" / "attack-from-mars-1995.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "attack-from-mars-1995.json"
PARTIAL_PATH = ROOT / "machines" / "partial" / "bally" / "attack-from-mars-1995.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "attack-from-mars-1995.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-95.json"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "wpc-95" / "attack-from-mars-boot-attract-and-ball-start.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "attack-from-mars-1995.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

DRIVER_IDS = {
	"afm_03", "afm_10", "afm_11", "afm_113", "afm_113b",
	"afm_11pfx", "afm_11u", "afm_f10", "afm_f20", "afm_f32",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
UNUSED_MATRIX_ADDRESSES = {12, 15, 23, 25, 28, 68} | {80 + row for row in range(1, 9)}
OPTO_ADDRESSES = {31, 32, 33, 34, 35, 36, 37}
SAUCER_LED_ADDRESSES = {91, 92, 93, 94, 95, 96, 97, 98, 101, 102, 103, 104, 105, 106, 107, 108}


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
	import curate_attack_from_mars as curator

	argv = sys.argv
	sys.argv = ["curate_attack_from_mars.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class AttackFromMarsDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	# --- identity and promotion ------------------------------------------------

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.attack-from-mars.1995", machine["id"])
		self.assertEqual("Attack From Mars", machine["name"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1995, machine["year"])
		self.assertEqual("physical_pinball", machine["kind"])

	def test_opdb_crosswalk_supplies_ipdb_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual(3781, machine["ipdb_id"])
		self.assertNotIn("model_number", machine)

	def test_promotion_state(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("author_ready", coverage["status"])
		self.assertEqual([], coverage["missing"])
		self.assertTrue(all(value == "validated" for value in coverage["dimensions"].values()))
		self.assertEqual([], self.definition["conflicts"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_controller_is_the_shared_wpc_95_profile(self) -> None:
		controller = self.definition["controller"]
		self.assertEqual("pinmame.wpc-95", controller["platform"])
		self.assertEqual("0x80", controller["hardware_generation"])
		self.assertTrue(controller["inversion_applied_by_emulator"])
		self.assertTrue(CONTROLLER_PATH.is_file())

	def test_stale_partial_is_gone(self) -> None:
		self.assertFalse(PARTIAL_PATH.exists())

	# --- drivers ---------------------------------------------------------------

	def test_every_driver_is_covered_with_a_compatibility_verdict(self) -> None:
		drivers = {driver["id"]: driver for driver in self.definition["drivers"]}
		self.assertEqual(DRIVER_IDS, set(drivers))
		for driver_id, driver in drivers.items():
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver_id)
			self.assertTrue(driver["variant_notes"].strip(), driver_id)
		# The three FreeWPC builds and the two re-releases are compatible rather than identical.
		for driver_id in ("afm_f10", "afm_f20", "afm_f32", "afm_11pfx", "afm_11u"):
			self.assertEqual("compatible", drivers[driver_id]["physical_compatibility"], driver_id)
		for driver_id in ("afm_03", "afm_10", "afm_11", "afm_113", "afm_113b"):
			self.assertEqual("identical", drivers[driver_id]["physical_compatibility"], driver_id)

	def test_catalog_maps_every_driver_to_this_definition(self) -> None:
		catalog = load_json(CATALOG_PATH)
		mapped = {
			record["id"]
			for record in catalog["drivers"]
			if record.get("machine_id") == "bally.attack-from-mars.1995"
		}
		self.assertEqual(DRIVER_IDS, mapped)
		for record in catalog["drivers"]:
			if record["id"] in DRIVER_IDS:
				self.assertEqual("author_ready", record["coverage_status"], record["id"])

	# --- switch enumeration ----------------------------------------------------

	def test_full_switch_enumeration(self) -> None:
		expected = set(range(1, 9)) | MATRIX_ADDRESSES | set(range(111, 119))
		self.assertEqual(expected, set(self.switches))
		self.assertEqual(set(range(1, 9)), set(self.dips))

	def test_unused_matrix_positions_are_declared_unused(self) -> None:
		for address in MATRIX_ADDRESSES:
			device = self.switches[address]
			if address in UNUSED_MATRIX_ADDRESSES:
				self.assertEqual("unused", device["availability"], address)
				self.assertEqual("not_applicable", device["spatial"]["status"], address)
				self.assertEqual("unused", device["spatial"]["reason"], address)
			else:
				self.assertEqual("used", device["availability"], address)

	def test_optos_are_exactly_column_three_rows_one_to_seven(self) -> None:
		normally_closed = {
			address
			for address, device in self.switches.items()
			if device.get("normally_closed") is True
		}
		# Column 3 rows 1-7 are the printed optos; the two lower flipper cabinet optos are also
		# normally closed but live on the Fliptronic addresses.
		self.assertEqual(OPTO_ADDRESSES | {112, 114}, normally_closed)
		for address in OPTO_ADDRESSES:
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
		# Switch 38 shares column 3 but is row 8 and is not an opto.
		self.assertNotEqual("opto", self.switches[38]["physical"]["switch_type"])
		self.assertIs(False, self.switches[38]["normally_closed"])

	def test_upper_flipper_switch_positions_are_unused(self) -> None:
		for address in (115, 116, 117, 118):
			device = self.switches[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("unused", device["spatial"]["reason"], address)
			self.assertIn("no upper flippers", device["physical"]["notes"], address)
			self.assertNotIn("wiring", device, address)
		for address in (111, 112, 113, 114):
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_martian_targets_spell_the_word_in_order(self) -> None:
		expected = {
			56: '"M"ARTIAN Target', 57: 'M"A"RTIAN Target', 58: 'MA"R"TIAN Target',
			43: 'MAR"T"IAN Target', 44: 'MART"I"AN Target',
			41: 'MARTI"A"N Target', 42: 'MARTIA"N" Target',
		}
		for address, label in expected.items():
			self.assertEqual(label, self.switches[address]["label"], address)

	def test_always_closed_switch_is_a_constant(self) -> None:
		device = self.switches[24]
		self.assertEqual("constant", device["kind"])
		self.assertTrue(device["constant_active"])
		self.assertTrue(device["initial_active"])
		self.assertEqual("constant", device["spatial"]["reason"])

	# --- output enumeration ----------------------------------------------------

	def test_full_solenoid_enumeration(self) -> None:
		expected = set(range(1, 51)) | {51, 52, 53}
		# PinMAME publishes no addresses at these positions for this generation.
		expected -= {54}
		self.assertEqual(expected & set(self.solenoids), set(self.solenoids))
		for address in (1, 2, 24, 33, 34, 35, 36, 37, 38, 39, 45, 46, 47, 48):
			self.assertIn(address, self.solenoids, address)

	def test_lpdc_mirrors_and_custom_solenoids_are_virtual_duplicates(self) -> None:
		for address in (41, 42, 43):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"], address)
			self.assertIn("internal.duplicate.lpdc-mirror", device["roles"], address)
			self.assertEqual("virtual", device["spatial"]["reason"], address)
		for address in (51, 52, 53):
			device = self.solenoids[address]
			self.assertEqual("virtual", device["kind"], address)
			self.assertIn("internal.duplicate.custom-solenoid", device["roles"], address)

	def test_strobe_light_is_39_and_the_script_binds_its_mirror_43(self) -> None:
		self.assertEqual("Strobe Light", self.solenoids[39]["label"])
		self.assertEqual("A-20718", self.solenoids[39]["physical"]["assembly_part_number"])
		self.assertIn("SolCallback(43)", self.solenoids[39]["physical"]["notes"])
		# The mirror must not be described as a second saucer-dome circuit.
		mirror_notes = self.solenoids[43]["physical"]["notes"]
		self.assertIn("mirror", mirror_notes)
		self.assertNotIn("saucer-dome", mirror_notes)

	def test_gate_naming_follows_the_manual_and_records_the_pinmame_disagreement(self) -> None:
		self.assertEqual("Right Gate", self.solenoids[33]["label"])
		self.assertEqual("Left Gate", self.solenoids[34]["label"])
		for address in (33, 34):
			notes = self.solenoids[address]["physical"]["notes"]
			self.assertIn("A-17797-2", notes, address)
			self.assertIn("A-17797-1", notes, address)
			# The disagreement must be recorded, not averaged away or claimed as agreement.
			self.assertIn("disagreement is recorded", notes, address)
			self.assertNotIn("Every available source agrees", notes, address)
		# The custom-solenoid duplicates follow the bit order wpc.c actually writes.
		self.assertIn("public solenoid 34", self.solenoids[51]["physical"]["notes"])
		self.assertIn("public solenoid 33", self.solenoids[52]["physical"]["notes"])

	def test_motor_bank_is_a_motor_not_a_flashlamp(self) -> None:
		device = self.solenoids[24]
		self.assertEqual("motor", device["kind"])
		self.assertEqual("14-8023", device["physical"]["part_number"])
		self.assertEqual("A-20572", device["physical"]["assembly_part_number"])
		self.assertIn("not a flashlamp", device["physical"]["notes"])

	def test_lower_flipper_addresses_keep_their_manual_aliases(self) -> None:
		for address, manual in ((45, "29"), (46, "30"), (47, "31"), (48, "32")):
			aliases = {alias["namespace"]: alias["value"] for alias in self.solenoids[address]["aliases"]}
			self.assertEqual(manual, aliases["manual.address"], address)
			self.assertEqual(str(address), aliases["pinmame.solenoid"], address)

	def test_two_bulb_flashers_declare_quantity_two_with_one_placement(self) -> None:
		for address in (17, 18, 19, 25, 26, 27):
			device = self.solenoids[address]
			self.assertEqual(2, device["physical"]["quantity"], address)
			self.assertEqual(1, len(device["spatial"]["placements"]), address)
		for address in (20, 21, 22, 23, 28):
			self.assertEqual(1, self.solenoids[address]["physical"]["quantity"], address)

	def test_right_side_high_flasher_is_placed_on_the_right(self) -> None:
		# The retained table's stored pos for this flasher is stale and points left; the drag-point
		# centroid, the wall glow and the manual all place it on the right.
		placement = self.solenoids[19]["spatial"]["placements"][0]
		self.assertGreater(placement["x"], 0.8)
		self.assertEqual("A-20549", self.solenoids[19]["physical"]["assembly_part_number"])
		# Its left-hand counterpart stays on the left.
		self.assertLess(self.solenoids[27]["spatial"]["placements"][0]["x"], 0.2)
		self.assertEqual("A-20546", self.solenoids[27]["physical"]["assembly_part_number"])

	# --- lamps -----------------------------------------------------------------

	def test_lamp_enumeration_covers_the_matrix_and_the_saucer_ring(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES | SAUCER_LED_ADDRESSES, set(self.lamps))

	def test_lamp_87_is_the_only_unused_matrix_lamp(self) -> None:
		unused = {address for address, device in self.lamps.items() if device["availability"] == "unused"}
		self.assertEqual({87}, unused)

	def test_lamp_15_drives_two_bulbs_at_two_placements(self) -> None:
		device = self.lamps[15]
		self.assertEqual("Return To Battle", device["label"])
		self.assertEqual(2, device["physical"]["quantity"])
		self.assertEqual(2, len(device["spatial"]["placements"]))

	def test_saucer_leds_are_enumerated_and_sourced_from_the_harness(self) -> None:
		for address in SAUCER_LED_ADDRESSES:
			device = self.lamps[address]
			self.assertEqual("used", device["availability"], address)
			self.assertEqual("A-20670", device["physical"]["assembly_part_number"], address)
			self.assertIn("91-98 and 101-108", device["physical"]["notes"], address)
			refs = device["provenance"]["source_refs"]
			self.assertIn("runtime.attack-from-mars.boot-attract-and-ball-start", refs, address)

	def test_cabinet_button_lamps_have_no_playfield_coordinate(self) -> None:
		for address in (86, 88):
			device = self.lamps[address]
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"], address)

	# --- general illumination --------------------------------------------------

	def test_five_gi_strings_with_three_placed_and_two_backbox(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))
		for address, count in ((0, 8), (1, 7), (2, 14)):
			device = self.gi[address]
			self.assertEqual("validated", device["spatial"]["status"], address)
			self.assertEqual(count, len(device["spatial"]["placements"]), address)
		# Strings 01 and 02 have an unambiguous emitter array, so their table-derived count stands.
		for address in (0, 1):
			self.assertEqual(
				len(self.gi[address]["spatial"]["placements"]),
				self.gi[address]["physical"]["quantity"],
				address,
			)
		for address in (3, 4):
			device = self.gi[address]
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"], address)
			# The manual publishes no count for the insert-panel strings, so none is asserted.
			self.assertNotIn("quantity", device["physical"], address)
			self.assertIn("not asserted", device["physical"]["notes"], address)

	def test_gi_string_three_asserts_no_socket_count(self) -> None:
		# The three jet-bumper bulb lights in the retained table are not proven decorative, so an
		# exact physical socket count for this string would be an unsupported assertion.
		device = self.gi[2]
		self.assertNotIn("quantity", device["physical"])
		notes = device["physical"]["notes"]
		self.assertIn("gi31", notes)
		self.assertIn("unresolved", notes)
		self.assertIn("not claimed to be exhaustive", notes)

	def test_open_gi_question_is_disclosed_in_the_spatial_report(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		unresolved = report["unresolved"]
		self.assertEqual(1, len(unresolved))
		entry = unresolved[0]
		self.assertEqual("pinmame.output.gi 2", entry["scope"])
		self.assertIn("jet-bumper", entry["question"])
		self.assertTrue(entry["why_not_blocking"].strip())
		# The exclusion list must not claim these are settled decoration.
		self.assertNotIn("gi31", " ".join(report["excluded_object_classes"]))

	def test_serial_control_outputs_are_not_light_emitters(self) -> None:
		# Solenoids 37 and 38 clock a shift register; the light they produce is the sixteen saucer
		# L.E.D.s. Giving them emitter placements would invent two physical emitters.
		for address in (37, 38):
			device = self.solenoids[address]
			# Not "relay" either: no relay exists on this circuit. control_signal is the kind for a
			# logic-level line that drives another board.
			self.assertEqual("control_signal", device["kind"], address)
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			self.assertEqual("internal_nonvisual", device["spatial"]["reason"], address)
			self.assertIn("internal.serial-control", device["roles"], address)
			self.assertIn("emits no light itself", device["physical"]["notes"], address)
		# The strobe on 39 is a genuine emitter and keeps its placement.
		self.assertEqual("flasher", self.solenoids[39]["kind"])
		self.assertEqual("validated", self.solenoids[39]["spatial"]["status"])

	def test_runtime_evidence_pins_the_emulator_and_initial_state(self) -> None:
		evidence = load_json(EVIDENCE_PATH)
		runtime = evidence["runtime"]
		emulator = runtime["emulator"]
		self.assertRegex(emulator["sha256"], r"^[0-9a-f]{64}$")
		self.assertEqual("4ec52ff0ac133ac251681518aed2249e19fe26eb", emulator["built_from_revision"])
		self.assertRegex(runtime["rom_archive_sha256"], r"^[0-9a-f]{64}$")
		self.assertEqual(2, len(runtime["raw_runs"]))
		for run in runtime["raw_runs"]:
			self.assertTrue(run["nvram_initialization"].strip(), run["name"])
			self.assertIn("initial_switches", run, run["name"])
			self.assertIn("pulses", run, run["name"])
			self.assertGreater(run["boot_wait_s"], 0, run["name"])
		# raw_runs must be in replay order, not alphabetical order: the run that creates the NVRAM
		# has to come before the run that inherits it, or the recorded replay is impossible.
		names = [run["name"] for run in runtime["raw_runs"]]
		self.assertEqual(["boot-and-service-v1", "attract-and-ball-start-v1"], names)
		self.assertIn("empty", runtime["raw_runs"][0]["nvram_initialization"])
		self.assertIn("inherited", runtime["raw_runs"][1]["nvram_initialization"])
		self.assertIn("replay order", runtime["command_template"])

	def test_curator_gate_covers_the_whole_promoted_bundle(self) -> None:
		import curate_attack_from_mars as curator

		# The knowledge note and the runtime evidence are not curator output, so they are pinned by
		# hash; a stale note or a substituted evidence file must fail the gate.
		curator.verify_promoted_bundle(ROOT)
		self.assertRegex(curator.KNOWLEDGE_SHA256, r"^[0-9a-f]{64}$")
		self.assertRegex(curator.EVIDENCE_SHA256, r"^[0-9a-f]{64}$")
		self.assertNotEqual("0" * 64, curator.KNOWLEDGE_SHA256)
		self.assertNotEqual("0" * 64, curator.EVIDENCE_SHA256)

	def test_knowledge_note_does_not_assert_unretained_sources_as_authority(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("IPDB 3781", text)
		self.assertIn("reports/opdb-identity.json", text)
		# The 176-page manual and the altsound package are contributor-held, not retained here.
		self.assertIn("contributor-held", text)
		self.assertNotIn("retained community altsound.csv", text)

	def test_knowledge_note_has_no_stale_partial_conclusions(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertNotIn("before this machine is promoted", text)
		self.assertNotIn("marks both entries\n`observed`", text)
		self.assertNotIn("has not been independently verified here", text)
		self.assertNotIn("should ultimately be marked unused", text)

	# --- displays and mechanisms ----------------------------------------------

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		display = displays[0]
		self.assertEqual("dmd", display["kind"])
		self.assertEqual((128, 32), (display["width"], display["height"]))
		self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_mechanism_inventory(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		for identifier in (
			"mechanism.trough", "mechanism.shooter-lane", "mechanism.motor-bank",
			"mechanism.drop-target", "mechanism.left-popper", "mechanism.right-popper",
			"mechanism.saucer", "mechanism.loop-gates", "mechanism.ramp-diverter",
			"mechanism.alien-left-low", "mechanism.alien-left-high",
			"mechanism.alien-right-high", "mechanism.alien-right-low",
			"mechanism.jet-bumpers", "mechanism.slingshots", "mechanism.flippers",
		):
			self.assertIn(identifier, mechanisms)
		self.assertEqual(16, len(mechanisms))

	def test_four_alien_mechanisms_cover_the_seven_martian_targets(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		groups = {
			"mechanism.alien-left-low": {"switch.matrix-56", "switch.matrix-57", "switch.matrix-58"},
			"mechanism.alien-left-high": {"switch.matrix-43"},
			"mechanism.alien-right-high": {"switch.matrix-44"},
			"mechanism.alien-right-low": {"switch.matrix-41", "switch.matrix-42"},
		}
		covered: set[str] = set()
		for identifier, sensors in groups.items():
			self.assertEqual(sensors, set(mechanisms[identifier]["sensors"]), identifier)
			self.assertFalse(covered & sensors, identifier)
			covered |= sensors
		self.assertEqual(7, len(covered))

	def test_motor_bank_records_both_end_positions_and_the_gating(self) -> None:
		mechanism = next(m for m in self.definition["mechanisms"] if m["id"] == "mechanism.motor-bank")
		positions = {position["id"]: position for position in mechanism["positions"]}
		self.assertEqual({"up", "down"}, set(positions))
		self.assertEqual(["switch.matrix-67"], positions["up"]["sensors"])
		self.assertEqual(["switch.matrix-66"], positions["down"]["sensors"])
		self.assertIn("only while 67 Motor Bank Up is closed", mechanism["behavior"])
		self.assertIn("66 Motor Bank Down is closed", mechanism["behavior"])

	def test_relationships_are_causal_not_positional(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual(
			{
				"relationship.trough-eject-opto",
				"relationship.drop-target-reset",
				"relationship.motor-bank-up",
				"relationship.motor-bank-down",
			},
			set(relationships),
		)
		self.assertEqual("inverted", relationships["relationship.drop-target-reset"]["kind"])
		for relationship in relationships.values():
			self.assertIn(relationship["kind"], {"direct", "normally_closed_series", "relay_gated", "inverted", "pulse"})

	# --- provenance and spatial audit ------------------------------------------

	def test_every_device_has_availability_and_a_spatial_record(self) -> None:
		for device in self.definition["inputs"] + self.definition["outputs"]:
			self.assertIn(device["availability"], {"used", "unused", "optional"}, device["id"])
			self.assertIn("spatial", device, device["id"])
			self.assertEqual("validated", device["provenance"]["status"], device["id"])
			self.assertTrue(device["provenance"]["source_refs"], device["id"])

	def test_every_source_ref_resolves(self) -> None:
		known = {source["id"] for source in self.definition["sources"]}
		for device in self.definition["inputs"] + self.definition["outputs"]:
			for ref in device["provenance"]["source_refs"]:
				self.assertIn(ref, known, device["id"])
			spatial = device["spatial"]
			for placement in spatial.get("placements", []):
				for ref in placement["provenance"]["source_refs"]:
					self.assertIn(ref, known, placement["id"])

	def test_placement_ids_are_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		for device in self.definition["inputs"] + self.definition["outputs"]:
			for placement in device["spatial"].get("placements", []):
				self.assertNotIn(placement["id"], seen)
				seen.add(placement["id"])
				for axis in ("x", "y"):
					value = placement[axis]
					self.assertGreaterEqual(value, 0.0, placement["id"])
					self.assertLessEqual(value, 1.0, placement["id"])
					decimals = str(value).split(".")[1] if "." in str(value) else ""
					self.assertLessEqual(len(decimals), 6, placement["id"])
		self.assertEqual(187, len(seen))

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("bally.attack-from-mars.1995", report["machine_id"])
		self.assertEqual("validated", report["status"])
		self.assertEqual(187, report["placement_count"])
		# One disclosed, non-blocking question remains; every entry must say why it does not block.
		for entry in report["unresolved"]:
			self.assertTrue(entry["why_not_blocking"].strip(), entry["scope"])
		self.assertEqual(745, report["extraction"]["file_count"])
		self.assertEqual(
			{"left": 0.0, "top": 0.0, "right": 964.0, "bottom": 2162.0},
			report["coordinate_convention"]["source_bounds"],
		)
		# Every projection must carry a concrete reason.
		for entry in report["projections"]:
			self.assertTrue(entry["reason"].strip(), entry)
		self.assertTrue(report["visual_review_cache"]["pages"])

	def test_render_helpers_are_declared_excluded(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		excluded = " ".join(report["excluded_object_classes"])
		self.assertIn("flw", excluded)
		self.assertIn("DivF", excluded)
		self.assertIn("BallShadow", excluded)
		# The raised flare quads are the only coordinate the table offers for six flashers, so they
		# are the documented placement anchor. Claiming them as excluded while using their position
		# would be self-contradictory, so the exclusion list must not name them.
		self.assertNotIn("flare_red", excluded)
		for address in (17, 18, 19, 25, 26, 27):
			reasons = [
				entry["reason"]
				for entry in report["projections"]
				if entry["group"] == "pinmame.output.solenoid" and entry["address"] == address
			]
			self.assertEqual(1, len(reasons), address)
			self.assertIn("f", reasons[0], address)

	def test_only_solenoid_19_uses_a_drag_point_centroid(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		centroid_users = [
			entry["address"]
			for entry in report["projections"]
			if entry["group"] == "pinmame.output.solenoid" and "centroid" in entry["reason"]
		]
		self.assertEqual([19], centroid_users)

	# --- runtime evidence ------------------------------------------------------

	def test_runtime_evidence_observed_every_saucer_led_address(self) -> None:
		evidence = load_json(EVIDENCE_PATH)
		self.assertEqual(["afm_113b"], evidence["driver_ids"])
		self.assertEqual(["bally.attack-from-mars.1995"], evidence["machine_ids"])
		observations = evidence["runtime"]["observations"]
		seen = set(observations["lamp_addresses_seen"])
		self.assertTrue(SAUCER_LED_ADDRESSES <= seen)
		self.assertEqual([0, 1, 2, 3, 4], observations["gi_addresses_seen"])
		# The clock, the data and both of their mirrors were observed.
		self.assertTrue({37, 38, 41, 42} <= set(observations["solenoid_addresses_seen"]))

	# --- knowledge -------------------------------------------------------------

	def test_knowledge_note_is_promoted_and_has_no_open_questions(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("author_ready", text)
		self.assertNotIn("## Unresolved questions", text)
		self.assertNotIn("not yet modeled", text)
		self.assertNotIn("not yet enumerated", text)
		self.assertIn("91-98 and 101-108", text)
		# The MARTIAN letters must be attributed to the right switches.
		self.assertIn('43 MAR"T"', text)
		self.assertIn('44 MART"I"', text)

	def test_knowledge_note_is_valid_utf8_prose(self) -> None:
		raw = KNOWLEDGE_PATH.read_bytes()
		self.assertEqual(raw.decode("utf-8"), KNOWLEDGE_PATH.read_text(encoding="utf-8"))

	# --- deterministic curator -------------------------------------------------

	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(SEED_PATH.read_bytes(), DEFINITION_PATH.read_bytes())

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_attack_from_mars as curator

		curator.check(ROOT)

	def test_curator_check_is_idempotent(self) -> None:
		import curate_attack_from_mars as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_rebuilds_the_definition_byte_for_byte(self) -> None:
		import curate_attack_from_mars as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		self.assertEqual(DEFINITION_PATH.read_bytes(), canonical_bytes(curator.build()))


class AttackFromMarsRetainedEvidenceTests(unittest.TestCase):
	"""Checks that only run when the external evidence roots are configured."""

	def setUp(self) -> None:
		self.sources_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not self.sources_root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")

	def test_retained_extraction_matches_its_pinned_manifest(self) -> None:
		import curate_attack_from_mars as curator

		root = Path(self.sources_root)
		if not (root / curator.EXTRACTION_RELATIVE_PATH).is_dir():
			self.skipTest("the retained Attack From Mars extraction is not present")
		curator.verify_extraction_manifest(root)

	def test_every_visual_review_page_matches_its_pinned_hash(self) -> None:
		import curate_attack_from_mars as curator

		manuals_root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not manuals_root:
			self.skipTest("PINMAME_MANUALS_ROOT is not configured")
		rendered = Path(manuals_root) / "rendered" / "bally.attack-from-mars.1995"
		if not rendered.is_dir():
			self.skipTest("the rendered Attack From Mars page cache is not present")
		for name, digest, _note in curator.VISUAL_REVIEW_CACHE:
			page = rendered / name
			self.assertTrue(page.is_file(), name)
			self.assertEqual(digest, curator._file_sha256(page), name)

	def test_retained_transcription_matches_its_pinned_hash(self) -> None:
		import curate_attack_from_mars as curator

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		path = Path(artifacts_root) / "attack-from-mars-1995" / "manual-transcription.md"
		if not path.is_file():
			self.skipTest("the retained transcription is not present")
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(path))

	def test_retained_harness_runs_match_the_evidence_record(self) -> None:
		import curate_attack_from_mars as curator

		artifacts_root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not artifacts_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		harness = Path(artifacts_root) / "attack-from-mars-1995" / "harness"
		if not harness.is_dir():
			self.skipTest("the retained harness runs are not present")
		evidence = load_json(EVIDENCE_PATH)
		names = {
			"boot-and-service-v1": "afm-boot-and-service.json",
			"attract-and-ball-start-v1": "afm-attract-and-ball-start.json",
		}
		for run in evidence["runtime"]["raw_runs"]:
			path = harness / names[run["name"]]
			self.assertTrue(path.is_file(), run["name"])
			self.assertEqual(run["sha256"], curator._file_sha256(path), run["name"])


if __name__ == "__main__":
	unittest.main()
