from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "twilight-zone-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "twilight-zone-1993.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "bally" / "twilight-zone-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "twilight-zone-1993.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "wpc-fliptronic.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "twilight-zone-1993.json"

DRIVER_IDS = {
	"tz_92", "tz_93", "tz_94ch", "tz_94h", "tz_d1", "tz_d2", "tz_d3", "tz_d4",
	"tz_f10", "tz_f100", "tz_f19", "tz_f50", "tz_f86", "tz_f97", "tz_h7", "tz_h8",
	"tz_i7", "tz_i8", "tz_ifpa", "tz_ifpa2", "tz_l1", "tz_l2", "tz_l3", "tz_l4",
	"tz_l5", "tz_la9", "tz_p3", "tz_p3d", "tz_p4", "tz_p5", "tz_pa1", "tz_pa2",
}
MATRIX_ADDRESSES = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
# The clock optos: printed as a "9th column" 91-98, published by PinMAME at CORE_CUSTSWNO(1,1..8) = 121-128.
CUSTOM_COLUMN_ADDRESSES = set(range(121, 129))
PRINTED_CLOCK_OPTO_ADDRESSES = set(range(91, 99))
UNUSED_MATRIX_ADDRESSES = {71, 82, 86}
OPTO_ADDRESSES = {72, 73, 74, 75, 76, 81, 83, 84, 85, 87} | CUSTOM_COLUMN_ADDRESSES
FLIPPER_ADDRESSES = set(range(111, 119))


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
	import curate_twilight_zone as curator

	argv = sys.argv
	sys.argv = ["curate_twilight_zone.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


class TwilightZoneDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.dips = bindings(cls.definition, "inputs", "pinmame.input.dip")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")
		cls.gi = bindings(cls.definition, "outputs", "pinmame.output.gi")

	def test_partial_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("partial", self.definition["coverage"]["status"])
		# G.I. string 02 is the only device without a placement, and no conflict remains.
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		self.assertEqual("validated", self.definition["coverage"]["dimensions"]["semantic_naming"])
		for dimension, state in self.definition["coverage"]["dimensions"].items():
			if dimension in {"spatial_placement", "physical_wiring"}:
				continue
			self.assertIn(state, {"validated", "not_applicable"}, dimension)
		self.assertEqual("bally.twilight-zone.1993", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual(2684, self.definition["machine"]["ipdb_id"])
		self.assertEqual(1993, self.definition["machine"]["year"])
		self.assertEqual("pinmame.wpc-fliptronic", self.definition["controller"]["platform"])
		self.assertEqual("0x8", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])

	def test_clock_drives_follow_the_manual_and_the_rom_clock_test(self) -> None:
		# The manual's clock test text (1-18), its solenoid tables (2-52/2-53), the retained script's cross-reference and
		# the ROM's own clock test all make public 56 Clock Reverse and 57 Clock Forward. Pinned tz.c's #define names
		# read backwards, but its live mechClock model (tz.c:601-624) takes sol1 = sClockRev = 57 as forward through
		# mech.c:140-145, so only the names are swapped and the former naming conflict is withdrawn, not carried.
		self.assertEqual([], self.definition["conflicts"])
		reverse, forward = self.solenoids[56], self.solenoids[57]
		self.assertEqual(("Clock Reverse", "device.clock-reverse"), (reverse["label"], reverse["id"]))
		self.assertEqual(("Clock Forward", "device.clock-forward"), (forward["label"], forward["id"]))
		for device, drive in ((reverse, "42"), (forward, "43")):
			notes = device["physical"]["notes"]
			self.assertIn("With only drive 43 turned ON, the clock moves forward.", notes)
			self.assertIn("sClockFwd", notes)
			self.assertIn("naming defect", notes)
			for phrase in ("tz.c:601-616", "mech_add(0,&mechClock)", "tz.c:638-661", "mech.c:140-145", "dir = (sol==1)-(sol==2)"):
				self.assertIn(phrase, notes)
			for stale in ("unused at runtime", "inert"):
				self.assertNotIn(stale, notes)
			self.assertIn("runtime.twilight-zone.clock-test", device["provenance"]["source_refs"])
			self.assertIn("runtime.twilight-zone.clock-test-mech", device["provenance"]["source_refs"])
			self.assertIn("manual.bally.twilight-zone.1993.ipdb-2684", device["provenance"]["source_refs"])
			self.assertEqual({drive}, {a["value"] for a in device["aliases"] if a["namespace"] == "manual.address"})
		clock = {item["id"]: item for item in self.definition["mechanisms"]}["mechanism.clock"]
		self.assertEqual(["device.clock-reverse", "device.clock-forward"], clock["actuators"])
		self.assertIn("runtime.twilight-zone.clock-test", clock["provenance"]["source_refs"])
		self.assertIn("runtime.twilight-zone.clock-test-mech", clock["provenance"]["source_refs"])
		self.assertNotIn("conflict.", clock["behavior"])
		for stale in ("does not expose", "unused at runtime", "inert"):
			self.assertNotIn(stale, clock["behavior"])
		self.assertIn("GetMech(0)", clock["behavior"])
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		for stale in ("does not expose the clock", "unused at runtime", "currently inert"):
			self.assertNotIn(stale, note)
		text = json.dumps(self.definition)
		self.assertNotIn("Clock Motor Drive", text)
		self.assertNotIn("clock-motor-direction-naming\"", text)

	def test_clock_test_runtime_evidence_pins_each_named_operation(self) -> None:
		import hashlib
		import re
		import curate_twilight_zone as curator

		evidence = load_json(ROOT / curator.RUNTIME_CLOCK_PATH)
		runtime = evidence["runtime"]
		self.assertEqual("tz_92", runtime["game"])
		self.assertEqual("69fc1b83de3be491c1fc5b113437ee4e7ab11b87d65f8c675989144a9b55aece", runtime["rom_archive_sha256"])
		self.assertEqual("deb2c99f44af3ae669a716943e737aca4b6b5126d5a786544206d0e7bd77e83c", runtime["emulator"]["sha256"])
		self.assertEqual(curator.RUNTIME_LIBRARY_REVISION, runtime["emulator"]["built_from_revision"])
		self.assertIn("--handle-mechanics 0", runtime["command_template"])
		(raw,) = runtime["raw_runs"]
		self.assertEqual("00742c62ca76b02a402162a609566ae2ed40bb419c74d50b27246d6d54dee92e", raw["sha256"])
		# source.sha256 pins the run folder's canonical manifest; the move of the folder after the run is recorded.
		self.assertEqual("04e3f8e39c95603787528497e77f71ea580beeb12dfbc8859f58a45eeb220a9c", evidence["source"]["sha256"])
		self.assertIn("manifest.json", evidence["source"]["manifest_algorithm"])
		self.assertIn("review-artifacts/twilight-zone/clock-test-run2", runtime["command_template"])
		self.assertIn("moved", runtime["command_template"])
		scenario = ROOT / raw["scenario_path"]
		self.assertEqual("18458c0d6a6b402e9b550890ce6090ad5195a3b6ed27fb46b7a841e51b805d46", raw["scenario_sha256"])
		self.assertEqual(raw["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest())
		observations = runtime["observations"]
		pattern = re.compile(
			r"starts (CLOCK (?:FWD|REV)\. (?:SLOW|FAST)) .* from the snapshot before the start press to the snapshot after "
			r"the stop press public (5[67]) stays on throughout while public (5[67]) drops "
			r"(\d+) times: 5[67] alone ([\d.]+) s, 5[67] alone ([\d.]+) s, both ([\d.]+) s, neither ([\d.]+) s"
		)
		operations = {}
		for item in observations["named_action_observations"]:
			match = pattern.search(item["label"])
			if match:
				operations[match.group(1)] = match.groups()[1:]
				self.assertEqual([int(match.group(3))], item["transitioned_solenoid_addresses"], item["label"])
		# Forward keeps 57 (drive 43) on and drops 56; reverse keeps 56 (drive 42) on and drops 57.
		self.assertEqual({"CLOCK FWD. SLOW", "CLOCK FWD. FAST", "CLOCK REV. SLOW", "CLOCK REV. FAST"}, set(operations))
		for name, (held, dropped, drops, alone, other, both, neither) in operations.items():
			self.assertEqual(("57", "56") if "FWD" in name else ("56", "57"), (held, dropped), name)
			self.assertGreater(int(drops), 0, name)
			self.assertGreater(float(alone), 0.0, name)
			self.assertEqual((0.0, 0.0), (float(other), float(neither)), name)
		stopped = [item for item in observations["named_action_observations"] if item["label"].startswith("CLOCK STOPPED")]
		self.assertEqual(5, len(stopped))
		for item in stopped:
			self.assertIn("both on for 1.000 s", item["label"])
			self.assertEqual([], item["transitioned_solenoid_addresses"])
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		sys.path.insert(0, str(ROOT / "tools"))
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(evidence["source"]["sha256"], check_manifest(path.parent, "tz_92"))
		run = load_json(path)
		# Recompute every figure in the labels from the raw run, so a label can only state what the run shows.
		recomputed, recomputed_stopped = curator.clock_test_windows(run)
		for name, op in recomputed.items():
			held, dropped, drops, alone, other, both, neither = operations[name]
			window = op["window"]
			self.assertEqual(int(drops), op["drops"][int(dropped)], name)
			self.assertEqual(0, op["drops"][int(held)], name)
			self.assertAlmostEqual(float(alone), window[f"{held} only"], places=3, msg=name)
			self.assertAlmostEqual(float(both), window["both"], places=3, msg=name)
			self.assertEqual(0.0, window[f"{dropped} only"], name)
			self.assertEqual(0.0, window["neither"], name)
		for window in recomputed_stopped.values():
			self.assertEqual({"56 only": 0.0, "57 only": 0.0, "both": 1.0, "neither": 0.0}, window["window"])
		# Each pinned DMD frame is a frame the run showed.
		frames = {snapshot["displays"][0]["pixel_sha256"] for snapshot in run["snapshots"] if snapshot["displays"]}
		for item in observations["diagnostic_snapshots"]:
			self.assertIn(item["pixel_sha256"], frames, item["label"])

	def test_model_on_clock_test_shows_the_clock_moving_the_named_way(self) -> None:
		import hashlib
		import curate_twilight_zone as curator

		evidence = load_json(ROOT / curator.RUNTIME_CLOCK_MECH_PATH)
		runtime = evidence["runtime"]
		self.assertIn("--handle-mechanics 1", runtime["command_template"])
		(raw,) = runtime["raw_runs"]
		scenario = ROOT / raw["scenario_path"]
		self.assertEqual("tools/harness-scenarios/wpc-fliptronic/tz-clock-test-mech.json", raw["scenario_path"])
		self.assertEqual(raw["scenario_sha256"], hashlib.sha256(scenario.read_bytes()).hexdigest())
		self.assertEqual("0abb5b248b460924c14c0b31f70340b0659d4784cf9762f7d40cde11d66903c9", evidence["source"]["sha256"])
		texts = [item["interpreted_text"] for item in runtime["observations"]["diagnostic_snapshots"]]
		times = [text.split(" / ")[2] for text in texts]
		self.assertEqual(["0:00", "0:15", "0:15", "0:30", "1:00", "1:00", "12:45", "12:15", "12:00"], times)
		self.assertTrue(texts[1].startswith("CLOCK FWD. SLOW") and texts[4].startswith("CLOCK FWD. FAST"))
		self.assertTrue(texts[6].startswith("CLOCK REV. FAST") and texts[8].startswith("CLOCK REV. FAST"))
		# The ROM holds the same outputs as with the model off.
		for item in runtime["observations"]["named_action_observations"]:
			if "FWD" in item["label"]:
				self.assertEqual([56], item["transitioned_solenoid_addresses"])
			elif "REV" in item["label"]:
				self.assertEqual([57], item["transitioned_solenoid_addresses"])
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			return
		path = Path(root) / raw["retained_from"][len("external:pinmame-review-artifacts/"):]
		self.assertEqual(raw["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
		run = load_json(path)
		self.assertEqual(1, run["handle_mechanics"])
		frames = {snapshot["displays"][0]["pixel_sha256"] for snapshot in run["snapshots"] if snapshot["displays"]}
		for item in runtime["observations"]["diagnostic_snapshots"]:
			self.assertIn(item["pixel_sha256"], frames, item["label"])
		sys.path.insert(0, str(ROOT / "tools"))
		from build_external_evidence_manifest import check_manifest

		self.assertEqual(evidence["source"]["sha256"], check_manifest(path.parent, "tz_92"))

	def test_the_stale_author_ready_artifact_is_gone(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())
		self.assertTrue(DEFINITION_PATH.is_file())
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertTrue(CONTROLLER_PATH.is_file())

	def test_unconfigured_fast_flip_channel_uses_gilamps_state(self) -> None:
		self.assertIn("WPC_GILAMPS bit 7", self.solenoids[31]["physical"]["notes"])
		self.assertNotIn("fast-flip flag", self.solenoids[31]["physical"]["notes"])

	def test_every_tz_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertIn(driver["physical_compatibility"], {"identical", "compatible"}, driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])

	def test_full_switch_matrix_is_enumerated_with_no_gaps(self) -> None:
		expected = MATRIX_ADDRESSES | CUSTOM_COLUMN_ADDRESSES
		matrix_and_custom = {a for a in self.switches if a in expected}
		self.assertEqual(expected, matrix_and_custom)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("unused", self.switches[address]["availability"], address)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
		for address in (MATRIX_ADDRESSES | CUSTOM_COLUMN_ADDRESSES) - UNUSED_MATRIX_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)

	def test_dedicated_and_flipper_switches_are_present(self) -> None:
		for address in range(1, 9):
			self.assertIn(address, self.switches)
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.switches[address]["spatial"]["reason"])
		self.assertEqual(FLIPPER_ADDRESSES, {a for a in self.switches if 111 <= a <= 118})
		for address in FLIPPER_ADDRESSES:
			self.assertEqual("used", self.switches[address]["availability"], address)
			self.assertFalse(self.switches[address]["normally_closed"], address)
		self.assertEqual(set(range(1, 9)), set(self.dips))

	def test_four_flippers_are_fitted_not_repurposed(self) -> None:
		# Unlike Monster Bash, Twilight Zone genuinely has upper flippers.
		for address, expected in {
			111: "eos", 112: "button", 113: "eos", 114: "button",
			115: "eos", 116: "button", 117: "eos", 118: "button",
		}.items():
			label = self.switches[address]["label"].lower()
			self.assertIn(expected if expected != "eos" else "eos", label, address)

	def test_slingshot_labels_match_pinmame_source_not_the_superseded_legacy_stub(self) -> None:
		# tz.c: #define swLSling 34, #define swRSling 35. The legacy migrated stub this
		# definition replaces had these reversed; regression-guard the correction.
		self.assertIn("left", self.switches[34]["label"].lower())
		self.assertIn("right", self.switches[35]["label"].lower())
		left_x = self.switches[34]["spatial"]["placements"][0]["x"]
		right_x = self.switches[35]["spatial"]["placements"][0]["x"]
		self.assertLess(left_x, 0.5)
		self.assertGreater(right_x, 0.5)

	def test_opto_switches_match_the_pinmame_inverted_switch_mask(self) -> None:
		for address in OPTO_ADDRESSES:
			self.assertTrue(self.switches[address].get("normally_closed"), address)
			self.assertEqual("opto", self.switches[address]["physical"].get("switch_type"), address)
		non_opto_used = {a for a in self.switches if a in MATRIX_ADDRESSES and a not in UNUSED_MATRIX_ADDRESSES and a not in OPTO_ADDRESSES}
		for address in non_opto_used:
			self.assertFalse(self.switches[address].get("normally_closed", False), address)

	def test_switch_24_is_the_always_closed_reference_contact(self) -> None:
		# Page 2-50 of the complete IPDB manual prints matrix position 24 "Always Closed"
		# (switch list part "----"); pinned wpc.c closes it at machine init.
		switch = self.switches[24]
		self.assertEqual("Always Closed", switch["label"])
		self.assertEqual("constant", switch["kind"])
		self.assertEqual("used", switch["availability"])
		self.assertTrue(switch["constant_active"])
		self.assertTrue(switch["initial_active"])
		self.assertNotIn("part_number", switch["physical"])
		self.assertEqual("other", switch["physical"]["switch_type"])
		self.assertEqual({"status": "not_applicable", "reason": "constant"}, {k: switch["spatial"][k] for k in ("status", "reason")})
		self.assertEqual("validated", switch["spatial"]["provenance"]["status"])
		self.assertEqual(["manual.bally.twilight-zone.1993.ipdb-2684"], switch["spatial"]["provenance"]["source_refs"])
		self.assertIn("manual.bally.twilight-zone.1993.ipdb-2684", switch["provenance"]["source_refs"])
		self.assertEqual("validated", switch["provenance"]["status"])
		self.assertEqual(("J206-2", "J208-4"), (switch["wiring"]["drive_connection"], switch["wiring"]["return_connection"]))
		excerpt = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/switch-matrix.md").read_text(encoding="utf-8")
		self.assertIn("24 Always Closed", excerpt)
		self.assertIn("| 24 | ---- | Always Closed |", excerpt)

	def test_switches_11_to_33_carry_the_page_2_50_parts_and_every_matrix_switch_its_wiring(self) -> None:
		import curate_twilight_zone as curator

		excerpt = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/switch-matrix.md").read_text(encoding="utf-8")
		for address, (part, printed) in curator.SWITCH_PARTS_2_50.items():
			switch = self.switches[address]
			self.assertEqual(part, switch["physical"]["part_number"], address)
			self.assertIn(f"| {address} | {part} | {printed} |", excerpt)
			self.assertIn("manual.bally.twilight-zone.1993.ipdb-2684", switch["provenance"]["source_refs"], address)
			self.assertNotIn("not yet", switch["physical"]["notes"], address)
		self.assertEqual("Ball Shooter", self.switches[27]["label"])
		self.assertIn({"namespace": "vpx-script.label", "value": "Shooter Lane"}, self.switches[27]["aliases"])
		for address in (26,):
			self.assertIn("underside of the playfield", self.switches[address]["physical"]["notes"])
		for address in (14, 21, 22):
			self.assertIn("Not shown on the printed switch-locations diagram", self.switches[address]["physical"]["notes"])
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			column, row = divmod(address, 10)
			wiring = self.switches[address]["wiring"]
			self.assertEqual(curator.MATRIX_COLUMN_WIRING[column][1], wiring["drive_connection"], address)
			self.assertEqual(curator.MATRIX_ROW_WIRING[row][1], wiring["return_connection"], address)
		for column, (wire, connector, driver) in curator.MATRIX_COLUMN_WIRING.items():
			self.assertIn(f"| {column} | {wire} | {connector} | {driver} |", excerpt)
		for row, (wire, connector, receiver) in curator.MATRIX_ROW_WIRING.items():
			self.assertIn(f"| {row} | {wire} | {connector} | {receiver} |", excerpt)
		for address in UNUSED_MATRIX_ADDRESSES:
			self.assertNotIn("wiring", self.switches[address])

	def test_not_fitted_devices_have_no_part_number_and_no_placement(self) -> None:
		for address in (71, 82, 86):
			physical = self.switches[address]["physical"]
			self.assertNotIn("part_number", physical)
			self.assertNotIn("assembly_part_number", physical)
		magnet = self.solenoids[22]
		self.assertEqual("unused", magnet["availability"])
		self.assertNotIn("part_number", magnet["physical"])
		self.assertNotIn("assembly_part_number", magnet["physical"])

	def test_geometric_ordering_left_center_right_and_rear_front(self) -> None:
		# Left/right slingshots (already covered above); trough eject-to-drain should
		# increase in y (rear-to-front direction is not meaningful for a trough since it
		# runs along one edge, so assert against the shooter-lane/apron distance instead).
		shooter_y = self.switches[72]["spatial"]["placements"][0]["y"]
		start_button_role_devices = [d for d in self.definition["inputs"] if d["binding"]["device"] == 13]
		self.assertTrue(start_button_role_devices)
		self.assertGreater(shooter_y, 0.9)  # shooter lane sits near the apron (y close to 1)

	def test_auxiliary_board_solenoids_use_manual_address_alias_not_public_address(self) -> None:
		aliases = {
			alias["value"]
			for alias in self.solenoids[56]["aliases"]
			if alias["namespace"] == "manual.address"
		}
		self.assertEqual({"42"}, aliases)
		aliases51 = {
			alias["value"]
			for alias in self.solenoids[51]["aliases"]
			if alias["namespace"] == "manual.address"
		}
		self.assertEqual({"37"}, aliases51)

	def test_solenoids_37_through_44_are_declared_virtual_unused(self) -> None:
		for address in range(37, 45):
			self.assertEqual("virtual", self.solenoids[address]["kind"], address)
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_lamp_matrix_is_a_complete_8x8_grid(self) -> None:
		self.assertEqual(MATRIX_ADDRESSES, set(self.lamps))
		for address, lamp in self.lamps.items():
			self.assertEqual("used", lamp["availability"], address)

	def test_gi_strings_follow_the_complete_manual(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, set(self.gi))
		# G.I. string 02 (public 1) is mixed playfield + insert with no bulb list: physical, but unplaced.
		mini = self.gi[1]
		self.assertNotIn("spatial", mini)
		self.assertNotIn("quantity", mini["physical"])
		notes = mini["physical"]["notes"]
		for phrase in ("No spatial placement", "A-16806", "Light20", "Light43", "continuity or bulb survey of G.I. string 02"):
			self.assertIn(phrase, notes)
		# G.I. string 03 (public 2): the clock assembly's two sockets, co-located on the clock axis.
		clock = self.gi[2]
		self.assertEqual(2, clock["physical"]["quantity"])
		# Projected onto the clock axis, which is not a bulb object, so the two placements are observed.
		self.assertEqual("observed", clock["spatial"]["status"])
		self.assertEqual({"observed"}, {p["provenance"]["status"] for p in clock["spatial"]["placements"]})
		self.assertEqual(["spatial_placement"], self.definition["coverage"]["missing"])
		points = {(p["x"], p["y"]) for p in clock["spatial"]["placements"]}
		self.assertEqual(2, len(clock["spatial"]["placements"]))
		self.assertEqual({(self.solenoids[56]["spatial"]["placements"][0]["x"], self.solenoids[56]["spatial"]["placements"][0]["y"])}, points)
		for phrase in ("A-16124", "Light Bulb Sleeve - Red", "Light Bulb Sleeve - Yellow", "GIClock", "not socket positions", "The projection hides an offset", "about an inch apart"):
			self.assertIn(phrase, clock["physical"]["notes"])
		# G.I. string 04 (public 3) "Insert Main" is backbox-only by the 2-52 columns and the 3-33 connector list.
		self.assertEqual(("not_applicable", "cabinet_or_service"), (self.gi[3]["spatial"]["status"], self.gi[3]["spatial"]["reason"]))
		self.assertIn("Return G.I. to insert", self.gi[3]["physical"]["notes"])
		self.assertEqual("validated", self.gi[0]["spatial"]["status"])
		self.assertGreater(len(self.gi[0]["spatial"]["placements"]), 1)

	def test_the_knocker_is_backbox_hardware(self) -> None:
		knocker = self.solenoids[7]
		self.assertEqual(("not_applicable", "cabinet_or_service"), (knocker["spatial"]["status"], knocker["spatial"]["reason"]))
		self.assertEqual(["cabinet.knocker"], knocker["roles"])
		self.assertIn("manual.bally.twilight-zone.1993.ipdb-2684", knocker["spatial"]["provenance"]["source_refs"])
		for phrase in ("J130-8", "Backbox columns", "B-10686-1 Knocker & Bracket Assy.", "Sol 7 to playfield coil", "every coil row 01-28", "J130, J127, J125 or J124", "J107 or J109 supply pin", "knocker's drive connection"):
			self.assertIn(phrase, knocker["physical"]["notes"])
		self.assertNotIn("voltage connection J130-8", knocker["physical"]["notes"])
		self.assertNotIn("for this row", knocker["physical"]["notes"])
		excerpt = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-table.md").read_text(encoding="utf-8")
		self.assertIn("In every fitted coil row 01-28", excerpt)
		self.assertIn("J107 or J109 supply pin", excerpt)

	def test_two_socket_flashers_place_both_sockets(self) -> None:
		expected = {
			18: ((0.864045, 0.403193), (0.638022, 0.334415), "Light.f18c"),
			19: ((0.173298, 0.349009), (0.08989, 0.291975), "Light.f19a"),
			20: ((0.404644, 0.037562), (0.449201, 0.579049), "Light.f20c"),
			55: ((0.947625, 0.052201), (0.517859, 0.579395), "Light.f41c"),
		}
		for address, (first, second, second_object) in expected.items():
			flasher = self.solenoids[address]
			placements = flasher["spatial"]["placements"]
			self.assertEqual(2, flasher["physical"]["quantity"], address)
			self.assertEqual("validated", flasher["spatial"]["status"], address)
			self.assertEqual([first, second], [(p["x"], p["y"]) for p in placements], address)
			self.assertIn("vpx-table.tz-2-4-5", placements[0]["provenance"]["source_refs"], address)
			self.assertIn("vpx-table.tz-ninuzzu-2020", placements[1]["provenance"]["source_refs"], address)
			self.assertNotIn("vpx-table.tz-ninuzzu-2020", placements[0]["provenance"]["source_refs"], address)
			notes = flasher["physical"]["notes"]
			self.assertIn(second_object, notes, address)
			self.assertIn("smaller falloff" if address != 19 else "only Light at that spot", notes, address)
			self.assertNotIn("would misstate the quantity", notes, address)
		self.assertIn("leave-one-out RMS 0.034", self.solenoids[19]["physical"]["notes"])
		self.assertNotIn("leave-one-out error up to", self.solenoids[19]["physical"]["notes"])
		# The unsourced "removed to reduce cost" script comment stays disclosed for the door-panel sockets.
		for address in (20, 55):
			self.assertIn("reduce cost", self.solenoids[address]["physical"]["notes"], address)

	def test_mini_playfield_switches_carry_two_contacts_each(self) -> None:
		for address, walls in ((45, ("Wall.sw45", "Wall.sw45a")), (46, ("Wall.sw46", "Wall.sw46a"))):
			switch = self.switches[address]
			placements = switch["spatial"]["placements"]
			self.assertEqual(2, len(placements), address)
			self.assertEqual("validated", switch["spatial"]["status"], address)
			notes = switch["physical"]["notes"]
			for phrase in (*walls, "(2)", "MINI-PLAYFIELD, TOP AND BOTTOM RAMP SWITCH LOCATIONS", "remote callout balloons", "leave-one-out RMS 0.066", "coordinates come from the table"):
				self.assertIn(phrase, notes, address)
			# The largest leave-one-out error (0.112) may be named only as the outlier that makes the 0.07 cap decide.
			self.assertNotIn("leave-one-out error up to", notes, address)
			self.assertIn("0.07 cap", notes, address)
			for placement in placements:
				self.assertIn("vpx-table.tz-ninuzzu-2020", placement["provenance"]["source_refs"], address)
		# Left before right, side rail before bottom rail.
		left = [(p["x"], p["y"]) for p in self.switches[45]["spatial"]["placements"]]
		right = [(p["x"], p["y"]) for p in self.switches[46]["spatial"]["placements"]]
		self.assertTrue(all(l[0] < r[0] for l, r in zip(left, right)))
		self.assertTrue(left[0][1] < left[1][1] and right[0][1] < right[1][1])

	def test_no_used_physical_device_is_internal_nonvisual_for_lack_of_geometry(self) -> None:
		# validation.py pairs internal_nonvisual with internal.* roles. Only the four flipper
		# end-of-stroke contacts and the clock strobe line may use it; every other used physical device
		# must either be placed or omit its spatial key. The exemption is by address, not by role, so
		# adding an internal.* role to another device cannot hide a missing placement.
		exempt = {("pinmame.input.switch", address) for address in (111, 113, 115, 117)} | {("pinmame.output.solenoid", 58)}
		physical_kinds = {"switch", "coil", "flasher", "lamp", "gi", "motor", "magnet", "relay", "control_signal"}
		offenders = []
		internal_nonvisual = set()
		for device in self.definition["inputs"] + self.definition["outputs"]:
			spatial = device.get("spatial")
			key = (device["binding"]["group"], device["binding"]["device"])
			if spatial is not None and spatial["status"] == "not_applicable" and spatial["reason"] == "internal_nonvisual":
				internal_nonvisual.add(key)
			if device["kind"] not in physical_kinds or device["availability"] != "used" or spatial is None:
				continue
			if key in exempt:
				continue
			if spatial["status"] == "not_applicable" and spatial["reason"] == "internal_nonvisual":
				offenders.append(device["id"])
			self.assertNotIn("No VPX geometry evidence", device.get("physical", {}).get("notes", ""), device["id"])
		self.assertEqual([], offenders)
		self.assertTrue(exempt <= internal_nonvisual)
		strobe = self.solenoids[58]
		self.assertEqual("control_signal", strobe["kind"])
		self.assertEqual("internal_nonvisual", strobe["spatial"]["reason"])
		self.assertEqual(["internal.clock-opto-strobe"], strobe["roles"])

	def test_unplaced_physical_devices_omit_spatial_and_say_why(self) -> None:
		unplaced = {
			(device["binding"]["group"], device["binding"]["device"])
			for device in self.definition["inputs"] + self.definition["outputs"]
			if "spatial" not in device
		}
		self.assertEqual({("pinmame.output.gi", 1)}, unplaced)
		for group, address in unplaced:
			device = {"pinmame.input.switch": self.switches, "pinmame.output.solenoid": self.solenoids, "pinmame.output.gi": self.gi}[group][address]
			self.assertEqual("used", device["availability"], (group, address))
			self.assertIn("No spatial placement", device["physical"]["notes"], (group, address))
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual(unplaced, {(entry["group"], entry["address"]) for entry in report["unresolved"]})
		self.assertIn("spatial_placement", self.definition["coverage"]["missing"])

	def test_door_panel_lamps_are_playfield_inserts_and_buttons_are_cabinet(self) -> None:
		for address in list(range(11, 19)) + list(range(21, 29)):
			lamp = self.lamps[address]
			placement = lamp["spatial"]["placements"][0]
			self.assertEqual("validated", lamp["spatial"]["status"], address)
			self.assertNotIn("roles", lamp, address)
			self.assertTrue(0.35 < placement["x"] < 0.62 and 0.5 < placement["y"] < 0.75, address)
		for address in (87, 88):
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])

	def test_jet_bumper_switches_and_coils_follow_the_manual_drawings(self) -> None:
		self.assertEqual("Left Jet Bumper", self.switches[31]["label"])
		self.assertEqual("Right Jet Bumper", self.switches[32]["label"])
		self.assertEqual("Lower Jet Bumper", self.switches[33]["label"])
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		left, right, lower = point(self.switches[31]), point(self.switches[32]), point(self.switches[33])
		self.assertLess(left[0], right[0])
		self.assertGreater(lower[1], left[1])
		self.assertGreater(lower[1], right[1])
		# Coils by the page 2-53 drawing: 13 left, 14 upper right, 12 lower.
		self.assertEqual(left, point(self.solenoids[13]))
		self.assertEqual(right, point(self.solenoids[14]))
		self.assertEqual(lower, point(self.solenoids[12]))

	def test_flipper_coils_sit_on_their_own_flipper(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		lower_right, lower_left = point(self.solenoids[45]), point(self.solenoids[47])
		upper_right, upper_left = point(self.solenoids[33]), point(self.solenoids[35])
		self.assertGreater(lower_right[0], 0.5)
		self.assertLess(lower_left[0], 0.5)
		self.assertGreater(upper_right[0], upper_left[0])
		self.assertEqual(lower_right, point(self.solenoids[46]))
		self.assertEqual(lower_left, point(self.solenoids[48]))
		self.assertEqual(upper_right, point(self.solenoids[34]))
		self.assertEqual(upper_left, point(self.solenoids[36]))
		# End-of-stroke contacts follow the repository convention: internal to the flipper assembly.
		for eos in (111, 113, 115, 117):
			spatial = self.switches[eos]["spatial"]
			self.assertEqual(("not_applicable", "internal_nonvisual"), (spatial["status"], spatial["reason"]), eos)
			self.assertTrue(self.switches[eos]["roles"][0].startswith("internal."), eos)
		for button in (112, 114, 116, 118):
			self.assertEqual("cabinet_or_service", self.switches[button]["spatial"]["reason"])

	def test_clock_optos_and_motor_share_the_clock_axis(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		axis = point(self.switches[121])
		self.assertTrue(axis[0] > 0.7 and axis[1] < 0.3)
		for address in range(122, 129):
			self.assertEqual(axis, point(self.switches[address]), address)
		self.assertEqual(axis, point(self.solenoids[56]))
		self.assertEqual(axis, point(self.solenoids[57]))

	def test_clock_optos_are_bound_at_the_core_custswno_addresses(self) -> None:
		import curate_twilight_zone as curator

		# core.h:347: CORE_CUSTSWNO(c,r) = ((CORE_CUSTSWCOL-1+c)*10+r), CORE_CUSTSWCOL = CORE_STDSWCOLS = 12.
		# tz.c:175-182 defines swClockM15..swClockH4 as CORE_CUSTSWNO(1,1..8).
		core_custswcol = 12
		derived = {90 + row: (core_custswcol - 1 + 1) * 10 + row for row in range(1, 9)}
		self.assertEqual(dict(zip(range(91, 99), range(121, 129))), derived)
		self.assertEqual(derived, curator.CLOCK_OPTO_PUBLIC)
		self.assertEqual({row: curator.core_custswno(1, row) for row in range(1, 9)}, {row: 120 + row for row in range(1, 9)})
		labels = {
			121: "Clock 15 Minutes", 122: "Clock 0 Minutes", 123: "Clock 45 Minutes", 124: "Clock 30 Minutes",
			125: "Clock Hour 1", 126: "Clock Hour 2", 127: "Clock Hour 3", 128: "Clock Hour 4",
		}
		for printed, public in derived.items():
			switch = self.switches[public]
			self.assertEqual(f"switch.custom-{public}", switch["id"])
			self.assertEqual(labels[public], switch["label"])
			self.assertIn({"namespace": "pinmame.switch", "value": str(public)}, switch["aliases"])
			self.assertIn({"namespace": "manual.address", "value": str(printed)}, switch["aliases"])
			self.assertEqual("opto", switch["physical"]["switch_type"])
			self.assertTrue(switch["normally_closed"])
			self.assertEqual("8-Driver PCB A-16100 J5-1", switch["wiring"]["drive_connection"])
			self.assertEqual("Gray-White", switch["wiring"]["drive_wire"])
			self.assertEqual(curator.MATRIX_ROW_WIRING[printed - 90][1], switch["wiring"]["return_connection"])
			self.assertIn("Q1 and Q12", switch["wiring"]["return_component"])
			self.assertIn(f"CORE_CUSTSWNO(1,{printed - 90})", switch["physical"]["notes"])
			self.assertIn("internal column 12", switch["physical"]["notes"])
			self.assertIn("manual.bally.twilight-zone.1993.ipdb-2684", switch["provenance"]["source_refs"])
		# Nothing is bound at the printed numbers any more.
		self.assertFalse(PRINTED_CLOCK_OPTO_ADDRESSES & set(self.switches))
		clock = {item["id"]: item for item in self.definition["mechanisms"]}["mechanism.clock"]
		self.assertEqual([f"switch.custom-{public}" for public in range(121, 129)], clock["sensors"])
		# The wiring comes from page 2-50's column 9 heading and page 1-18's clock test text.
		matrix = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/switch-matrix.md").read_text(encoding="utf-8")
		self.assertIn("| 9 | Gray-White | *J5-1 | (blank) |", matrix)
		self.assertIn("* Located on 8 Driver P.C.B.,", matrix)
		clock_test = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/clock-test.md").read_text(encoding="utf-8")
		self.assertIn("driven by Q1 and Q12 of the 8-Driver Board", clock_test)

	def test_switch_61_carries_the_amended_part(self) -> None:
		switch = self.switches[61]
		self.assertEqual("5647-12693-57", switch["physical"]["part_number"])
		self.assertIn("5647-12693-32", switch["physical"]["notes"])
		self.assertIn("16-50020-AMD-1", switch["physical"]["notes"])
		self.assertIn("manual-amendment.bally.twilight-zone.1993", switch["provenance"]["source_refs"])
		excerpt = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/manual-amendment-clock-assembly.md").read_text(encoding="utf-8")
		self.assertIn("> Switch 61 changed to **5647-12693-57**.", excerpt)
		self.assertIn("> Page 2-51 Switch Locations", excerpt)

	def test_other_amendment_entries_are_applied_or_scoped(self) -> None:
		excerpt = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/manual-amendment-clock-assembly.md").read_text(encoding="utf-8")
		for line in (
			"> Item 2 has been changed to **SW-1A-194** Switch Assembly and,",
			"> Item 14 was changed to **A-16909** Opto Photo Transistor Assembly and,",
			"> Item 15 was changed to **A-16908** Opto LED Assembly.",
			"> Item 12a was added: **A-16535** Ramp Prox Opto sensor Assembly,",
		):
			self.assertIn(line, excerpt)
		self.assertIn("changes nothing recorded", excerpt)
		# Switch 74 (Gumball Popper): the Ball Popper Assembly's optos, amended on page 2-25.
		popper = self.switches[74]
		self.assertEqual("A-16908 (LED) / A-16909 (Trans)", popper["physical"]["assembly_part_number"])
		self.assertIn("A-14231 (LED) / A-14232 (Trans)", popper["physical"]["notes"])
		self.assertIn("manual-amendment.bally.twilight-zone.1993", popper["provenance"]["source_refs"])
		# Switch 57 (Slot Proximity): a proximity sensor assembly, not a plain switch.
		slot = self.switches[57]
		self.assertEqual("other", slot["physical"]["switch_type"])
		self.assertEqual("A-16535", slot["physical"]["part_number"])
		self.assertFalse(slot["normally_closed"])
		for phrase in ("Ramp Prox Opto sensor Assembly", "underside of the playfield", "item 12a"):
			self.assertIn(phrase, slot["physical"]["notes"])
		self.assertNotIn("plain mechanical switch", slot["physical"]["notes"])
		self.assertIn("manual-amendment.bally.twilight-zone.1993", slot["provenance"]["source_refs"])
		# No flipper end-of-stroke switch records a part the 2-20 entry would change.
		for address in (111, 113, 115, 117):
			self.assertNotIn("part_number", self.switches[address]["physical"])

	def test_clock_opto_board_names_match_the_printed_parts(self) -> None:
		for address in range(121, 125):
			self.assertIn("A-16220, the Minute Opto P.C.B.; the Hour board is A-16219", self.switches[address]["physical"]["notes"])
		for address in range(125, 129):
			self.assertIn("A-16219, the Hour Opto P.C.B.; the Minute board is A-16220", self.switches[address]["physical"]["notes"])

	def test_core_source_locator_names_the_live_and_disabled_clock_code(self) -> None:
		source = {s["id"]: s for s in self.definition["sources"]}
		locator = next(s for s in source.values() if s["kind"] == "pinmame_core")["locator"]
		for phrase in ("tz_swRowRead (tz.c:586-589", "tz.c:601-624", "tz.c:638-661", "disabled by #if 0", "mech.c:140-145", "wpc.c:1545"):
			self.assertIn(phrase, locator)
		self.assertNotIn("synthetic swGeneva/clock-opto derivation", locator)

	def test_fit_notes_name_the_deciding_cap(self) -> None:
		for device in (self.switches[45], self.switches[46], self.solenoids[19]):
			self.assertIn("0.07 cap", device["physical"]["notes"])
		self.assertIn("balloon 53", self.switches[46]["physical"]["notes"])
		self.assertIn("callout 18", self.solenoids[19]["physical"]["notes"])
		report = SPATIAL_REPORT_PATH.with_suffix(".md").read_text(encoding="utf-8")
		self.assertIn("so the 0.07 cap decides", report)

	def test_corrected_placements_do_not_regress(self) -> None:
		point = lambda device: (device["spatial"]["placements"][0]["x"], device["spatial"]["placements"][0]["y"])
		self.assertNotEqual(point(self.switches[47]), point(self.switches[52]))
		self.assertNotEqual(point(self.switches[74]), point(self.switches[51]))
		self.assertEqual(point(self.switches[26]), point(self.switches[15]))
		self.assertEqual(point(self.solenoids[15]), point(self.switches[88]))
		self.assertNotEqual(point(self.solenoids[24]), point(self.solenoids[6]))
		self.assertEqual(point(self.solenoids[24]), point(self.switches[55]))
		flasher = self.solenoids[17]
		self.assertEqual(2, flasher["physical"]["quantity"])
		self.assertEqual(2, len(flasher["spatial"]["placements"]))
		for address in (18, 19, 20, 55):
			self.assertEqual(2, self.solenoids[address]["physical"]["quantity"], address)
			self.assertEqual(2, len(self.solenoids[address]["spatial"]["placements"]), address)
		# Solenoid 5 sits on the diverter blade primitive (BM_RDiv pivot), not on the invisible DivTrig/DivWall helpers.
		self.assertEqual((0.279253, 0.21377), point(self.solenoids[5]))
		self.assertIn("Primitive.BM_RDiv", self.solenoids[5]["physical"]["notes"])
		for address in (51, 52, 53, 54, 55, 56, 57, 58):
			self.assertTrue(self.solenoids[address]["physical"]["notes"].startswith(
				f"Printed solenoid/flasher-locations item {address - 14}, "
			), address)

	def test_spatial_report_separates_projections_from_direct_placements(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertTrue(report["projections"])
		self.assertTrue(report["direct_placements"])
		for entry in report["projections"]:
			self.assertTrue(entry["reason"].startswith("Projected onto"), entry)
		for entry in report["direct_placements"]:
			self.assertFalse(entry["reason"].startswith("Projected onto"), entry)
		direct = {(entry["group"], entry["address"]) for entry in report["direct_placements"]}
		self.assertIn(("pinmame.input.switch", 31), direct)
		self.assertIn(("pinmame.input.switch", 52), direct)
		self.assertIn(("pinmame.output.solenoid", 5), direct)
		self.assertIn(("pinmame.input.switch", 45), direct)
		self.assertIn(("pinmame.output.solenoid", 18), direct)
		projected = {(entry["group"], entry["address"]) for entry in report["projections"]}
		self.assertIn(("pinmame.output.gi", 2), projected)
		self.assertEqual(1, len(report["unresolved"]))

	def test_device_identifiers_are_unique(self) -> None:
		identifiers = [d["id"] for d in self.definition["inputs"] + self.definition["outputs"]]
		self.assertEqual(len(identifiers), len(set(identifiers)))

	def test_curator_cli_requires_a_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()


class TwilightZoneControllerProfileTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.profile = load_json(CONTROLLER_PATH)

	def test_identity(self) -> None:
		self.assertEqual("pinmame.wpc-fliptronic", self.profile["id"])
		self.assertTrue(self.profile["inversion_applied_by_emulator"])

	def test_switch_group_covers_the_custom_column_and_flipper_range(self) -> None:
		switch_group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.input.switch")
		ranges = {(r["minimum"], r["maximum"]) for r in switch_group["address_rules"]}
		self.assertIn((121, 168), ranges)
		self.assertIn((111, 118), ranges)
		# Column 9 (91-98) is not a custom-switch address on this generation; the printed "9th column" is an alias.
		for minimum, maximum in ranges:
			self.assertFalse(minimum <= 91 <= maximum or minimum <= 98 <= maximum, (minimum, maximum))
		notes = switch_group["notes"]
		for phrase in ("`121-128`", "`CORE_CUSTSWCOL = CORE_STDSWCOLS = 12`", "`manual.address` alias"):
			self.assertIn(phrase, notes)
		self.assertNotIn("reports publicly at `91-98`", notes)
		lamp_group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.lamp")
		lamp_ranges = {(r["minimum"], r["maximum"]) for r in lamp_group["address_rules"]}
		self.assertIn((91, 98), lamp_ranges)

	def test_notes_document_the_wpc95_contrast(self) -> None:
		solenoid_group = next(g for g in self.profile["groups"] if g["id"] == "pinmame.output.solenoid")
		notes = solenoid_group["notes"].lower()
		self.assertIn("wpc-95", notes)
		self.assertIn("37-44", notes)


class TwilightZoneCuratorDeterminismTests(unittest.TestCase):
	def test_check_mode_passes_twice_in_a_row(self) -> None:
		import curate_twilight_zone as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_spatial_report_is_reproducible(self) -> None:
		import curate_twilight_zone as curator

		definition = curator.build()
		report = curator.build_spatial_report(definition)
		self.assertEqual(report, json.loads(SPATIAL_REPORT_PATH.read_text(encoding="utf-8")))


# Each pinned geometry file with the table its rows come from: "2.4.5" (normalized by that table's 1082.353 x
# 2164.706 bounds) or "2020" (the ninuzzu table, 1093 x 2162).
GEOMETRY_FILES = {
	"vpx-geometry.txt": "2.4.5",
	"vpx-geometry-2026-09-25.txt": "2.4.5",
	"vpx-geometry-2026-09-25-round3.txt": "2.4.5",
	"vpx-geometry-2026-09-26.txt": "2020",
}


def _table_bounds(table: str) -> tuple[float, float]:
	import curate_twilight_zone as curator

	return (curator.BOUNDS_X, curator.BOUNDS_Y) if table == "2.4.5" else (curator.BOUNDS_2020_X, curator.BOUNDS_2020_Y)


def _table_extraction(table: str) -> Path:
	import curate_twilight_zone as curator

	return curator.EXTRACTION_RELATIVE_PATH if table == "2.4.5" else curator.EXTRACTION_2020_RELATIVE_PATH


def _geometry_rows(text: str, table: str = "2.4.5") -> list[tuple[str, str, float, float, float, float, str]]:
	"""Parse the object rows of a pinned geometry file: (vpx_type, vpx_name, raw_x, raw_y, norm_x, norm_y, table)."""
	rows = []
	for line in text.splitlines():
		fields = line.split("\t")
		if len(fields) < 7:
			continue
		try:
			numbers = [float(value) for value in fields[3:7]]
		except ValueError:
			continue
		rows.append((fields[1], fields[2], *numbers, table))
	return rows


def _hard_coded_coordinates() -> list[tuple[str, float, float]]:
	"""Every normalized coordinate the curator hard-codes, including the _norm() anchors."""
	import curate_twilight_zone as curator

	coordinates = []
	for table_name, table in (
		("SWITCH_POSITIONS", curator.SWITCH_POSITIONS),
		("SOLENOID_POSITIONS", curator.SOLENOID_POSITIONS),
		("LAMP_POSITIONS", curator.LAMP_POSITIONS),
		("GI_POSITIONS", curator.GI_POSITIONS),
		("GI_CLOCK_POSITIONS", {2: curator.GI_CLOCK_POSITIONS}),
	):
		for address, points in table.items():
			for x, y in points:
				coordinates.append((f"{table_name}[{address}]", x, y))
	return coordinates


class TwilightZoneRetainedGeometryTests(unittest.TestCase):
	"""Tie every hard-coded coordinate to the pinned geometry files, and those files to the retained extraction.

	Every coordinate in SWITCH_POSITIONS, SOLENOID_POSITIONS, LAMP_POSITIONS and GI_POSITIONS (the TABLE_OBJECTS
	anchors included, since they reach the definition through those tables) must equal the normalized columns of
	a row in one of the three hash-pinned geometry files; with the extraction configured, every such row and every
	TABLE_OBJECTS anchor must also be recomputable from gameitems.
	"""

	@staticmethod
	def _object_point(item_type: str, item: dict[str, object]) -> tuple[float, float]:
		if item_type == "Flasher":
			return (item["pos_x"], item["pos_y"])
		if item_type in {"HitTarget", "Primitive"}:
			return (item["position"]["x"], item["position"]["y"])
		if item.get("center") is not None:
			return (item["center"]["x"], item["center"]["y"])
		if item_type == "Wall":
			points = item["drag_points"]
			return (sum(p["x"] for p in points) / len(points), sum(p["y"] for p in points) / len(points))
		raise AssertionError(f"unexpected anchor type {item_type}")

	@staticmethod
	def _review_folder() -> Path | None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		return Path(root).expanduser().resolve() / "twilight-zone-1993" if root else None

	def _used_rows(self, folder: Path) -> list[tuple[str, str, float, float, float, float, str]]:
		rows = [
			row
			for name, table in GEOMETRY_FILES.items()
			for row in _geometry_rows((folder / name).read_text(encoding="utf-8"), table)
		]
		used = []
		for label, x, y in _hard_coded_coordinates():
			matches = [row for row in rows if abs(row[4] - x) < 5e-7 and abs(row[5] - y) < 5e-7]
			self.assertTrue(matches, f"{label} ({x}, {y}) matches no row of the pinned geometry files")
			used.extend(matches)
		return used

	def test_table_object_anchors_match_the_retained_extraction(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		gameitems = Path(root).expanduser().resolve() / curator.EXTRACTION_RELATIVE_PATH / "gameitems"
		for name, (x, y) in curator.TABLE_OBJECTS.items():
			item_type, _ = name.split(".", 1)
			path = gameitems / f"{name}.json"
			self.assertTrue(path.is_file(), path)
			item = load_json(path)[item_type]
			actual = self._object_point(item_type, item)
			self.assertAlmostEqual(x, actual[0], places=4, msg=name)
			self.assertAlmostEqual(y, actual[1], places=4, msg=name)

	def test_2020_table_object_anchors_match_its_retained_extraction(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		gameitems = Path(root).expanduser().resolve() / curator.EXTRACTION_2020_RELATIVE_PATH / "gameitems"
		for name, (x, y) in curator.TABLE_2020_OBJECTS.items():
			item_type, _ = name.split(".", 1)
			path = gameitems / f"{name}.json"
			self.assertTrue(path.is_file(), path)
			actual = self._object_point(item_type, load_json(path)[item_type])
			self.assertAlmostEqual(x, actual[0], places=4, msg=name)
			self.assertAlmostEqual(y, actual[1], places=4, msg=name)
		# The 2020 table's own bounds, which its placements are normalized by.
		gamedata = load_json(Path(root).expanduser().resolve() / curator.EXTRACTION_2020_RELATIVE_PATH / "gamedata.json")
		self.assertEqual((curator.BOUNDS_2020_X, curator.BOUNDS_2020_Y), (gamedata["right"], gamedata["bottom"]))

	def test_review_artifacts_match_their_pinned_hashes(self) -> None:
		folder = self._review_folder()
		if folder is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import hashlib
		import curate_twilight_zone as curator

		expected = {
			"vpx-geometry.txt": curator.VPX_GEOMETRY_SHA256,
			"vpx-geometry-2026-09-25.txt": curator.VPX_GEOMETRY_SUPPLEMENT_SHA256,
			"vpx-geometry-2026-09-25-round3.txt": curator.VPX_GEOMETRY_SUPPLEMENT_2_SHA256,
			"vpx-geometry-2026-09-26.txt": curator.VPX_GEOMETRY_SUPPLEMENT_3_SHA256,
			"manual-transcription.md": curator.MANUAL_TRANSCRIPTION_SHA256,
		}
		for name, digest in expected.items():
			self.assertEqual(digest, hashlib.sha256((folder / name).read_bytes()).hexdigest(), name)
		geometry = "\n".join((folder / name).read_text(encoding="utf-8") for name in GEOMETRY_FILES)
		# Every anchor the curator names must be listed in one of the pinned geometry files.
		for name in [*curator.TABLE_OBJECTS, *curator.TABLE_2020_OBJECTS]:
			item_type, object_name = name.split(".", 1)
			self.assertIn(f"{item_type}\t{object_name}\t", geometry, name)
		# The third supplement records every fit that reconciled a new placement, and each one passed.
		supplement = (folder / "vpx-geometry-2026-09-26.txt").read_text(encoding="utf-8")
		tests = [line for line in supplement.splitlines() if line.strip().startswith("TEST ")]
		self.assertEqual(9, len(tests))
		self.assertTrue(all(line.endswith("PASS") for line in tests), tests)

	def test_every_hard_coded_coordinate_matches_a_pinned_geometry_row(self) -> None:
		folder = self._review_folder()
		if folder is None:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT is not configured")
		import curate_twilight_zone as curator

		used = self._used_rows(folder)
		self.assertGreater(len(used), 150)
		# Each matched row must itself follow its file's stated normalization (the 2020 table has its own bounds).
		for item_type, name, raw_x, raw_y, x, y, table in used:
			bound_x, bound_y = _table_bounds(table)
			self.assertAlmostEqual(x, round(raw_x / bound_x, 6), places=6, msg=f"{item_type}.{name}")
			self.assertAlmostEqual(y, round(raw_y / bound_y, 6), places=6, msg=f"{item_type}.{name}")
		self.assertTrue(any(row[6] == "2020" for row in used))

	def test_every_matched_geometry_row_is_recomputable_from_gameitems(self) -> None:
		folder = self._review_folder()
		vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if folder is None or not vpx_root:
			self.skipTest("PINMAME_REVIEW_ARTIFACTS_ROOT and PINMAME_VPX_SOURCES_ROOT are both required")
		import curate_twilight_zone as curator

		for item_type, name, raw_x, raw_y, _, _, table in set(self._used_rows(folder)):
			gameitems = Path(vpx_root).expanduser().resolve() / _table_extraction(table) / "gameitems"
			path = gameitems / f"{item_type}.{name}.json"
			self.assertTrue(path.is_file(), path)
			actual = self._object_point(item_type, load_json(path)[item_type])
			self.assertAlmostEqual(raw_x, actual[0], places=3, msg=f"{item_type}.{name}")
			self.assertAlmostEqual(raw_y, actual[1], places=3, msg=f"{item_type}.{name}")


class TwilightZoneExtractionManifestTests(unittest.TestCase):
	def test_manifest_matches_the_retained_extraction_when_evidence_root_is_configured(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import curate_twilight_zone as curator

		curator.verify_extraction_manifest(Path(root).expanduser().resolve())

	def test_2020_table_manifest_matches_its_retained_extraction(self) -> None:
		root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not root:
			self.skipTest("PINMAME_VPX_SOURCES_ROOT is not configured")
		import hashlib
		import curate_twilight_zone as curator

		source_root = Path(root).expanduser().resolve()
		curator.verify_2020_extraction_manifest(source_root)
		table = source_root / curator.EXTRACTION_2020_RELATIVE_PATH.parent / "Twilight Zone (Bally 1993).vpx"
		self.assertEqual(curator.TABLE_2020_SHA256, hashlib.sha256(table.read_bytes()).hexdigest())
		script = source_root / curator.EXTRACTION_2020_RELATIVE_PATH / "script.vbs"
		self.assertEqual(curator.SCRIPT_2020_SHA256, hashlib.sha256(script.read_bytes()).hexdigest())


class TwilightZoneSourceTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.sources = {source["id"]: source for source in load_json(DEFINITION_PATH)["sources"]}

	def test_new_sources_are_pinned(self) -> None:
		import curate_twilight_zone as curator

		expected = {
			"manual.bally.twilight-zone.1993.ipdb-2684": "b026feca0fe20a709a7224b49cdb7330586b041798f1a02193c53a00738fa105",
			"manual-amendment.bally.twilight-zone.1993": "36b83c898727d4215ec9157f1236a2a074374187a39f665d82efa8f39e95a856",
			"vpx-table.tz-ninuzzu-2020": "cd98f8a152065b1fdbd6c79d7d5f5301e165a37963991b1ee9104f7db3e435ca",
			"vpx-script.tz-ninuzzu-2020": curator.SCRIPT_2020_SHA256,
		}
		for identifier, digest in expected.items():
			source = self.sources[identifier]
			self.assertEqual(digest, source["sha256"], identifier)
			self.assertTrue(source.get("license") and source.get("attribution"), identifier)
		manual = self.sources["manual.bally.twilight-zone.1993.ipdb-2684"]
		self.assertIn("ipdb.org/files/2684/", manual["uri"])
		self.assertIn("machine.cgi?id=2684", manual["locator"])
		excerpts = {excerpt["id"] for excerpt in manual["excerpts"]}
		self.assertEqual(
			{
				"excerpt.twilight-zone.solenoid-flasher-table", "excerpt.twilight-zone.clock-test",
				"excerpt.twilight-zone.backbox-assembly", "excerpt.twilight-zone.clock-assembly",
				"excerpt.twilight-zone.mini-playfield-assembly", "excerpt.twilight-zone.power-driver-connectors",
				"excerpt.twilight-zone.mini-playfield-switch-drawing", "excerpt.twilight-zone.switch-matrix",
			},
			excerpts,
		)
		self.assertTrue(all(excerpt.get("reviewed") for excerpt in manual["excerpts"]))
		self.assertIn(curator.EXTRACTION_2020_MANIFEST_SHA256, self.sources["vpx-extraction.tz-ninuzzu-2020"]["locator"])
		self.assertEqual("runtime_scenario", self.sources["runtime.twilight-zone.clock-test"]["kind"])
		self.assertIn("IPDB copy", self.sources["manual.bally.twilight-zone.1993"]["locator"])

	def test_retained_manuals_match_their_pinned_hashes(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("PINMAME_MANUALS_ROOT is not configured")
		import hashlib

		folder = Path(root).expanduser().resolve() / "by-machine" / "bally.twilight-zone.1993" / "ipdb-2684"
		for identifier in ("manual.bally.twilight-zone.1993.ipdb-2684", "manual-amendment.bally.twilight-zone.1993"):
			source = self.sources[identifier]
			path = folder / source["original_filename"]
			self.assertEqual(source["sha256"], hashlib.sha256(path.read_bytes()).hexdigest(), identifier)

	def test_the_complete_manual_prints_what_the_definition_cites(self) -> None:
		table = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/solenoid-flasher-table.md").read_text(encoding="utf-8")
		self.assertIn("| 07 | Knocker | High Power | (blank) | J130-8 | (blank) | Q68 | (blank) | J107-3 |", table)
		self.assertIn("| 42 | Clock Reverse |", table)
		self.assertIn("| 43 | Clock Forward |", table)
		self.assertIn("| 04 | Insert Main | G.I. | (blank) | J-120-5 |", table)
		clock_test = (ROOT / "evidence/excerpts/bally.twilight-zone.1993/clock-test.md").read_text(encoding="utf-8")
		self.assertIn("With only drive 43 turned ON, the clock moves", clock_test)
		self.assertIn("With only drive 42 turned ON, the clock moves in reverse.", clock_test)


if __name__ == "__main__":
	unittest.main()
