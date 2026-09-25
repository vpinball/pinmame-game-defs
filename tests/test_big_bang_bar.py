from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "author-ready" / "capcom" / "big-bang-bar-1996.json"
SUPERSEDED_PARTIAL_PATH = ROOT / "machines" / "partial" / "capcom" / "big-bang-bar-1996.json"
SEED_PATH = ROOT / "tools" / "seeds" / "capcom" / "big-bang-bar-1996.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "capcom" / "big-bang-bar-1996.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "capcom.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "capcom" / "big-bang-bar-1996.json"

DRIVER_IDS = {"bbb108", "bbb109"}


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
	import curate_big_bang_bar as curator

	argv = sys.argv
	sys.argv = ["curate_big_bang_bar.py"]
	try:
		curator.main()
	finally:
		sys.argv = argv


def _positions(devices: dict[int, dict[str, object]]) -> dict[int, tuple[float, float]]:
	result: dict[int, tuple[float, float]] = {}
	for address, device in devices.items():
		spatial = device.get("spatial")
		if spatial is None or spatial["status"] == "not_applicable":
			continue
		placement = spatial["placements"][0]
		result[address] = (placement["x"], placement["y"])
	return result


class BigBangBarDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_author_ready_identity_and_coverage(self) -> None:
		self.assertEqual(2, self.definition["schema_version"])
		self.assertEqual("author_ready", self.definition["coverage"]["status"])
		self.assertEqual([], self.definition["coverage"]["missing"])
		dimensions = self.definition["coverage"]["dimensions"]
		self.assertEqual(
			{
				"catalog_identity": "validated",
				"address_enumeration": "validated",
				"semantic_naming": "validated",
				"physical_wiring": "validated",
				"mechanisms": "validated",
				"variant_coverage": "validated",
				"recreation_knowledge": "validated",
				"spatial_placement": "validated",
			},
			dimensions,
		)
		self.assertEqual("capcom.big-bang-bar.1996", self.definition["machine"]["id"])
		self.assertEqual("physical_pinball", self.definition["machine"]["kind"])
		self.assertEqual("Capcom", self.definition["machine"]["manufacturer"])
		self.assertEqual(1996, self.definition["machine"]["year"])
		self.assertEqual("pinmame.capcom", self.definition["controller"]["platform"])
		self.assertEqual("0x0", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertEqual("complete", self.definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())
		self.assertEqual([], self.definition["conflicts"])
		self.assertFalse(SUPERSEDED_PARTIAL_PATH.exists(), "the superseded partial record must not remain")

	def test_no_hardware_generation_bit_exists_for_capcom(self) -> None:
		# Distinct from every WPC/System-11/Whitestar/SAM game curated so far: capcom.c's own
		# core_tGameData literal is {0, disp, ...} -- gen is the literal zero, not a bitmask.
		self.assertEqual("0x0", self.definition["controller"]["hardware_generation"])

	def test_every_bbb_driver_is_claimed_exactly_once_and_is_physically_compatible(self) -> None:
		self.assertEqual(DRIVER_IDS, {driver["id"] for driver in self.definition["drivers"]})
		for driver in self.definition["drivers"]:
			self.assertEqual("identical", driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip(), driver["id"])
		bbb109 = next(driver for driver in self.definition["drivers"] if driver["id"] == "bbb109")
		bbb108 = next(driver for driver in self.definition["drivers"] if driver["id"] == "bbb108")
		self.assertNotIn("clone_of", bbb109)
		self.assertEqual("bbb109", bbb108["clone_of"])

	def test_cabinet_and_matrix_switch_space_is_enumerated(self) -> None:
		self.assertEqual(set(range(1, 17)) | set(range(17, 81)) | {81, 82, 84, 89}, set(self.switches))
		# Cabinet dedicated switches (1-16): the fitted ones are cabinet/service; the four
		# genuinely unfitted positions (11-14) are constants.
		for address in range(1, 17):
			self.assertEqual("not_applicable", self.switches[address]["spatial"]["status"], address)
			expected_reason = "constant" if address in (11, 12, 13, 14) else "cabinet_or_service"
			self.assertEqual(expected_reason, self.switches[address]["spatial"]["reason"], address)
		# 11-14 genuinely unfitted per the manual; 15/16 are this game's Token/Ticket dispense.
		for address in (11, 12, 13, 14):
			self.assertEqual("unused", self.switches[address]["availability"], address)
		for address in (15, 16):
			self.assertEqual("used", self.switches[address]["availability"], address)
		self.assertEqual("Tilt Bob", self.switches[10]["label"])
		self.assertEqual("Left Flipper Button", self.switches[5]["label"])

	def test_pinmame_normalized_opto_switches_match_capinvsw10_with_zero_disagreement(self) -> None:
		# capInvSw10 = {0, 0x00, 0x01, 0x78, 0x00, 0x00, 0x01} (src/wpc/capgames.c), re-derived
		# in code rather than by hand: col2 bit0->25, col3 bits3-6->36/37/38/39, col6 bit0->57.
		mask = [0, 0x00, 0x01, 0x78, 0x00, 0x00, 0x01]
		normalized: set[int] = set()
		for column, byte in enumerate(mask):
			for bit in range(8):
				if byte & (1 << bit):
					normalized.add(9 + bit + column * 8)
		self.assertEqual({25, 36, 37, 38, 39, 57}, normalized)
		for address in normalized:
			self.assertEqual("opto", self.switches[address]["physical"]["switch_type"], address)
			self.assertEqual("validated", self.switches[address]["provenance"]["status"], address)

	def test_all_six_normalized_optos_carry_positive_construction_evidence(self) -> None:
		# 36-39: opto receiver/transmitter part numbers on the switch-locations page.
		for address in (36, 37, 38, 39):
			physical = self.switches[address]["physical"]
			self.assertIn("A0015604-4R", physical["notes"], address)
			self.assertIn("A0015702-4R", physical["notes"], address)
		# 25: the game-rules page's own "the opto spinner" construction statement.
		self.assertIn("the opto spinner", self.switches[25]["physical"]["notes"])
		# 57: the alien mechanism's encoder disc + A0020000 slotted-opto PCB and the
		# C2-02 diagnostic's "the opto (which reads the encoder wheel)".
		self.assertIn("MT00501", self.switches[57]["physical"]["notes"])
		self.assertIn("A0020000", self.switches[57]["physical"]["notes"])
		self.assertIn("which reads the encoder wheel", self.switches[57]["physical"]["notes"])
		# The superseded "illegible-only" hedging must not survive promotion.
		for address in (25, 36, 37, 38, 39, 57):
			self.assertNotIn("coverage.missing", self.switches[address]["physical"]["notes"], address)

	def test_synthetic_flipper_column_and_platform_gap_are_virtual(self) -> None:
		self.assertEqual("virtual", self.switches[81]["kind"])
		self.assertEqual("not_applicable", self.switches[81]["spatial"]["status"])
		self.assertEqual("virtual", self.switches[81]["spatial"]["reason"])
		self.assertEqual("virtual", self.switches[89]["kind"])
		self.assertEqual("unused", self.switches[81]["availability"])
		self.assertNotIn("never exposed to a table script", self.switches[81]["physical"]["notes"])

	def test_flipper_buttons_are_host_driven_through_the_flipper_column(self) -> None:
		# FLIP_SWNO(5,6): core_updateSw copies the flipper column's lower button bits into
		# the ROM-read switches 5/6 every frame, so a host presses the buttons at 84/82.
		for rom_address, host, side in ((5, 84, "left"), (6, 82, "right")):
			with self.subTest(host=host):
				record = self.switches[host]
				self.assertEqual(f"switch.flipper-column-{host}", record["id"])
				self.assertEqual("virtual", record["kind"])
				self.assertEqual("used", record["availability"])
				self.assertEqual("validated", record["provenance"]["status"])
				self.assertIn("vpm-script-library.core-vbs", record["provenance"]["source_refs"])
				self.assertEqual("virtual", record["spatial"]["reason"])
				notes = record["physical"]["notes"]
				self.assertIn(f"writes it into matrix switch {rom_address} every frame", notes)
				self.assertIn(f"{side} flipper button", notes)
				rom_notes = self.switches[rom_address]["physical"]["notes"]
				self.assertIn(f"a host must drive public {host} instead", rom_notes)
				self.assertEqual(f"flipper.lower.{side}.button", self.switches[rom_address]["roles"][0])

	def test_solenoid_space_is_enumerated_with_honest_kinds(self) -> None:
		expected = set(range(1, 33)) | {33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51}
		self.assertEqual(expected, set(self.solenoids))
		for address in range(21, 27):
			self.assertEqual("flasher", self.solenoids[address]["kind"], address)
		for address in (30, 31, 32):
			self.assertEqual("motor", self.solenoids[address]["kind"], address)
		for address in range(1, 21):
			if address in (21, 22, 23, 24, 25, 26):
				continue
			self.assertEqual("coil", self.solenoids[address]["kind"], address)
		self.assertEqual("Left Flipper", self.solenoids[9]["label"])
		self.assertEqual("Right Flipper", self.solenoids[10]["label"])
		self.assertEqual("Upper Right Flipper", self.solenoids[11]["label"])

	def test_flipper_mirror_addresses_bind_to_physical_correspondence(self) -> None:
		# Address 45 (sLRFlipPow) mirrors physical 9 (Left Flipper); 47 (sLLFlipPow) mirrors
		# physical 10 (Right Flipper) -- the opposite left/right sense from PinMAME's own
		# constant names, per capcom.c's own admitted mirror-naming defect.
		self.assertIn("Left Flipper", self.solenoids[45]["label"])
		self.assertIn("Right Flipper", self.solenoids[47]["label"])
		self.assertEqual("used", self.solenoids[45]["availability"])
		self.assertEqual("used", self.solenoids[47]["availability"])
		for address in (34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48, 49, 50):
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_flipper_mirror_notes_record_the_resolved_script_library_constants(self) -> None:
		# The former conflict's open question (the numeric sLRFlipper/sLLFlipper values) is
		# resolved: the installed VPinMAME core.vbs defines them as the hold-side addresses
		# 46/48, which capcom.c never writes, so the retained table's flipper callbacks are
		# dead bindings under that library -- a consumed-table defect, not a machine fact.
		for address, hold_address in ((45, 46), (47, 48)):
			notes = self.solenoids[address]["physical"]["notes"]
			self.assertIn("core.vbs", notes, address)
			self.assertIn(f"hold address {hold_address}", notes, address)
			self.assertNotIn("conflict.", notes, address)

	def test_solenoid_35_is_a_live_eject_hole_mirror(self) -> None:
		device = self.solenoids[35]
		self.assertEqual("virtual", device["kind"])
		self.assertEqual("used", device["availability"], "the mirror carries physical 12's live state, so it is a meaningful channel")
		self.assertIn("Eject Hole", device["label"])
		notes = device["physical"]["notes"]
		self.assertIn("(soldata>>11)", notes)
		self.assertIn("admitted defect", notes)
		self.assertNotIn("conflict.", notes)

	def test_mechanism_coils_disclose_their_projections(self) -> None:
		# The shared reset coils and the reversible alien motor are placed onto the mechanism
		# members their own switches identify; the disclosure must travel with the placement.
		report = load_json(SPATIAL_REPORT_PATH)
		projected = {
			entry["address"]
			for entry in report["projections"]
			if entry["group"] == "pinmame.output.solenoid"
		}
		for address in (7, 17, 31, 32):
			device = self.solenoids[address]
			self.assertEqual("validated", device["spatial"]["status"], address)
			self.assertIn("Projected onto", device["physical"]["notes"], address)
			self.assertIn(address, projected, address)
		# The reset-coil placement sets are their banks' own target positions.
		self.assertEqual(
			[(0.106602, 0.611911), (0.115986, 0.585663), (0.125458, 0.559367), (0.134723, 0.532262)],
			[(p["x"], p["y"]) for p in self.solenoids[7]["spatial"]["placements"]],
		)
		self.assertEqual(
			[(0.444456, 0.336556), (0.497771, 0.327576), (0.550396, 0.318153)],
			[(p["x"], p["y"]) for p in self.solenoids[17]["spatial"]["placements"]],
		)
		self.assertEqual(
			[(0.71318, 0.067239), (0.782786, 0.11226)],
			[(p["x"], p["y"]) for p in self.solenoids[31]["spatial"]["placements"]],
		)
		self.assertEqual(
			[(p["x"], p["y"]) for p in self.solenoids[31]["spatial"]["placements"]],
			[(p["x"], p["y"]) for p in self.solenoids[32]["spatial"]["placements"]],
		)

	def test_solenoid_22_is_flasher_only_with_the_parts_list_resolution(self) -> None:
		device = self.solenoids[22]
		self.assertEqual("flasher", device["kind"])
		# The rejected coil part number must not survive in structured data.
		self.assertEqual("LP00101", device["physical"]["part_number"])
		notes = device["physical"]["notes"]
		self.assertIn("SM00221", notes)
		self.assertIn("COUPLING, SHAFT", notes)
		self.assertIn("MR00108", notes)
		self.assertIn("NO coil", notes)
		self.assertIn("manual-internal error", notes)
		self.assertIn("backbox-right flasher", notes)
		self.assertNotIn("conflict.", notes)

	def test_backbox_flasher_21_is_not_playfield_classified(self) -> None:
		device = self.solenoids[21]
		self.assertEqual("flasher", device["kind"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("cabinet_or_service", device["spatial"]["reason"])
		self.assertIn("cabinet.backbox", device["roles"])
		self.assertIn("callout 21 in the backbox box", device["physical"]["notes"])
		self.assertIn("render proxy", device["physical"]["notes"])

	def test_star_bumper_solenoid_identity_is_manual_diagram_validated(self) -> None:
		self.assertEqual((0.380918, 0.20046), self._placement(18))
		self.assertEqual((0.526188, 0.267465), self._placement(19))
		self.assertEqual((0.585404, 0.178991), self._placement(20))
		for address in (18, 19, 20):
			notes = self.solenoids[address]["physical"]["notes"]
			self.assertIn("playfield diagram", notes, address)
			self.assertNotIn("inferred only from the order", notes, address)

	def _placement(self, address: int) -> tuple[float, float]:
		placement = self.solenoids[address]["spatial"]["placements"][0]
		return (placement["x"], placement["y"])

	def test_sling_and_flipper_coils_carry_documented_projection_placements(self) -> None:
		expected = {
			4: (0.229376, 0.735796),
			5: (0.674001, 0.733646),
			9: (0.285743, 0.848334),
			10: (0.618202, 0.84836),
			11: (0.827363, 0.457798),
		}
		for address, (x, y) in expected.items():
			device = self.solenoids[address]
			self.assertEqual("coil", device["kind"], address)
			placement = device["spatial"]["placements"][0]
			self.assertEqual((x, y), (placement["x"], placement["y"]), address)
			self.assertEqual("validated", device["spatial"]["status"], address)
			self.assertIn("Projected onto", device["physical"]["notes"], address)
			self.assertIn("playfield diagram", device["physical"]["notes"], address)

	def test_diverter_solenoids_carry_validated_wall_placements(self) -> None:
		# Solenoid 14: the retained table's two drop-wall panels.
		sp14 = self.solenoids[14]["spatial"]["placements"]
		self.assertEqual(
			[(0.111295, 0.113743), (0.129284, 0.099031)],
			[(placement["x"], placement["y"]) for placement in sp14],
		)
		# Solenoid 15: the earlier recreation's wall, corroborated by the manual callout,
		# with the VPW v1.0 same-named wall's divergence disclosed.
		sp15 = self.solenoids[15]["spatial"]["placements"]
		self.assertEqual([(0.291495, 0.023552)], [(placement["x"], placement["y"]) for placement in sp15])
		notes = self.solenoids[15]["physical"]["notes"]
		self.assertIn("(0.433, 0.032)", notes)
		self.assertIn("divergent retained geometry", notes)
		for address in (14, 15):
			self.assertIn("is_visible=false", self.solenoids[address]["physical"]["notes"], address)
			self.assertNotIn("conflict.", self.solenoids[address]["physical"]["notes"], address)

	def test_knocker_is_a_backbox_device(self) -> None:
		device = self.solenoids[3]
		self.assertEqual("coil", device["kind"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("cabinet_or_service", device["spatial"]["reason"])
		self.assertIn("backbox", device["physical"]["notes"])

	def test_fast_flips_solenoid_51_is_diagnostic_only(self) -> None:
		device = self.solenoids[51]
		self.assertEqual("virtual", device["kind"])
		self.assertEqual("not_applicable", device["spatial"]["status"])
		self.assertEqual("virtual", device["spatial"]["reason"])

	def test_no_gi_output_group_exists_for_capcom(self) -> None:
		groups = {device["binding"]["group"] for device in self.definition["outputs"]}
		self.assertNotIn("pinmame.output.gi", groups)
		for device in self.definition["outputs"]:
			self.assertNotEqual("gi", device["kind"], device["id"])

	def test_lamp_matrix_is_fully_enumerated_across_both_banks(self) -> None:
		self.assertEqual(set(range(1, 129)) | {129, 130} | set(range(131, 137)), set(self.lamps))
		unused = {address for address, device in self.lamps.items() if device["availability"] == "unused" and address <= 128}
		self.assertEqual(18, len(unused))
		used = {address for address in range(1, 129) if address not in unused}
		self.assertEqual(110, len(used))

	def test_cabinet_lamps_carry_controlled_records(self) -> None:
		# 1/2: coin-door lamp pairs (X2 per the matrix-A schematic sheet); 3: the START lamp
		# illuminates the cabinet start button (the retained script binds Lampz.Callback(03)
		# to PinCab_Start_Button; no playfield START insert exists in any retained source).
		for address in (1, 2, 3):
			device = self.lamps[address]
			self.assertEqual("used", device["availability"], address)
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"], address)
		self.assertIn("PinCab_Start_Button", self.lamps[3]["physical"]["notes"])
		self.assertIn("X2", self.lamps[1]["physical"]["notes"])
		self.assertIn("X2", self.lamps[2]["physical"]["notes"])

	def test_lamps_38_and_125_carry_corroboration_table_placements(self) -> None:
		self.assertEqual((0.863445, 0.018851), self._lamp_placement(38))
		self.assertEqual((0.502167, 0.213736), self._lamp_placement(125))
		for address in (38, 125):
			notes = self.lamps[address]["physical"]["notes"]
			self.assertIn("earlier retained recreation", notes, address)
			self.assertEqual("validated", self.lamps[address]["spatial"]["status"], address)

	def _lamp_placement(self, address: int) -> tuple[float, float]:
		placement = self.lamps[address]["spatial"]["placements"][0]
		return (placement["x"], placement["y"])

	def test_x2_bulb_quantities_are_recorded(self) -> None:
		# The schematic's matrix sheets mark exactly four addresses X2 (two parallel bulbs):
		# matrix-A coin-door lamps 1/2 and matrix-B lamps 87/125. Kiss sets the repository
		# precedent for multi-socket addresses: the socket with a retained coordinate carries
		# the placement and the multi-socket fact is disclosed on the device.
		for address in (1, 2, 87, 125):
			device = self.lamps[address]
			self.assertEqual(2, device["physical"]["quantity"], address)
			self.assertIn("X2", device["physical"]["notes"], address)
		# No other used lamp claims a doubled quantity.
		for address, device in self.lamps.items():
			if address <= 128 and device["availability"] == "used" and address not in (1, 2, 87, 125):
				self.assertNotIn("quantity", device["physical"], address)
				self.assertNotIn("X2", device["physical"]["notes"], address)

	def test_electro_black_light_is_a_documented_feature_projection(self) -> None:
		device = self.lamps[62]
		self.assertEqual("used", device["availability"])
		placement = device["spatial"]["placements"][0]
		self.assertEqual((0.880954, 0.081206), (placement["x"], placement["y"]))
		self.assertIn("Documented projection", device["physical"]["notes"])
		self.assertIn("not surveyed", device["physical"]["notes"])

	def test_diagnostic_lamp_column_is_cabinet_hardware(self) -> None:
		for address in (129, 130):
			self.assertEqual("not_applicable", self.lamps[address]["spatial"]["status"])
			self.assertEqual("cabinet_or_service", self.lamps[address]["spatial"]["reason"])
		for address in range(131, 137):
			self.assertEqual("unused", self.lamps[address]["availability"], address)

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
		self.assertEqual([], report["unresolved"])
		self.assertEqual([], report["blockers"])
		self.assertEqual(located, report["placement_count"])

	def test_geometric_ordering_regression_assertions(self) -> None:
		switch_pos = _positions(self.switches)
		# Left flipper sits left of right flipper.
		self.assertLess(switch_pos[33][0], switch_pos[34][0])
		# 4-Bank targets 17-20 are laid out in ascending y (nearer the rear as index rises).
		self.assertLess(switch_pos[20][1], switch_pos[19][1])
		self.assertLess(switch_pos[19][1], switch_pos[18][1])
		self.assertLess(switch_pos[18][1], switch_pos[17][1])
		# Trough balls 1-4 (36-39): 36 is nearest the SolRelease exit point (kicked out to the
		# shooter lane), 39 is nearest the Outhole/drain entry (largest y, closest to the apron).
		self.assertLess(switch_pos[36][1], switch_pos[37][1])
		self.assertLess(switch_pos[37][1], switch_pos[38][1])
		self.assertLess(switch_pos[38][1], switch_pos[39][1])
		self.assertLess(switch_pos[39][1], switch_pos[35][1])
		# Left slingshot sits left of right slingshot.
		self.assertLess(switch_pos[41][0], switch_pos[42][0])
		sol_pos = _positions(self.solenoids)
		# Left sling coil sits left of right sling coil; left flipper coil left of right.
		self.assertLess(sol_pos[4][0], sol_pos[5][0])
		self.assertLess(sol_pos[9][0], sol_pos[10][0])
		# Star bumpers: 18 leftmost, 20 rightmost, 19 between them and lowest.
		self.assertLess(sol_pos[18][0], sol_pos[19][0])
		self.assertLess(sol_pos[19][0], sol_pos[20][0])
		self.assertGreater(sol_pos[19][1], sol_pos[18][1])
		self.assertGreater(sol_pos[19][1], sol_pos[20][1])
		# Both ramp diverters sit at the playfield's rear (manual callouts 14/15).
		self.assertLess(sol_pos[14][1], 0.2)
		self.assertLess(sol_pos[15][1], 0.1)

	def test_mechanism_inventory_covers_every_used_coil_or_motor_with_a_geometry_home(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.4-bank-drop-targets", "mechanism.3-bank-drop-targets",
				"mechanism.1-bank-drop-target", "mechanism.alien-mechanism", "mechanism.tube-dancer",
				"mechanism.orbit-gates", "mechanism.island-and-ramp-diverters",
			},
			set(mechanisms),
		)
		device_ids = {device["id"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		for mechanism in self.definition["mechanisms"]:
			self.assertTrue(mechanism["behavior"].strip(), mechanism["id"])
			self.assertEqual("validated", mechanism["provenance"]["status"], mechanism["id"])
			for reference in list(mechanism["actuators"]) + list(mechanism["sensors"]):
				self.assertIn(reference, device_ids, reference)

	def test_tube_dancer_mechanism_is_motorized_with_no_coil(self) -> None:
		mechanism = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.tube-dancer")
		self.assertEqual("motorized", mechanism["kind"])
		self.assertIn("SM00221", mechanism["behavior"])
		self.assertIn("no coil", mechanism["behavior"])
		self.assertIn("MR00108", mechanism["behavior"])

	def test_relationships_use_proven_causality_only(self) -> None:
		relationships = {item["id"]: item for item in self.definition["relationships"]}
		self.assertEqual({"relationship.trough-release-to-shooter-lane"}, set(relationships))
		self.assertEqual("switch.matrix-43", relationships["relationship.trough-release-to-shooter-lane"]["destination"])
		self.assertEqual("pulse", relationships["relationship.trough-release-to-shooter-lane"]["kind"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		self.assertEqual("dmd", displays[0]["kind"])
		self.assertEqual(128, displays[0]["width"])
		self.assertEqual(32, displays[0]["height"])
		self.assertEqual("not_applicable", displays[0]["spatial"]["status"])
		self.assertEqual("cabinet_or_service", displays[0]["spatial"]["reason"])

	def test_conflicts_are_empty_with_resolutions_documented(self) -> None:
		self.assertEqual([], self.definition["conflicts"])
		# The four former conflicts' resolutions stay discoverable in the curator.
		import curate_big_bang_bar as curator

		docstring = curator.conflicts.__doc__ or ""
		for resolved in (
			"flipper-mirror-address-left-right-naming",
			"solenoid-35-eject-hole-mirror-mislabeled",
			"solenoid-22-shared-device-construction",
			"ramp-diverter-geometry-inconsistent",
		):
			self.assertIn(resolved, docstring)

	def test_sources_are_hashed_licensed_and_free_of_local_paths(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		self.assertIn("vpx-script.bbb-vpw-1-0", sources)
		self.assertTrue(sources["vpx-script.bbb-vpw-1-0"]["known_working"])
		self.assertEqual(
			"db632ce7611ad625053c1bfcc6f035b95338c49449b5e78fa5fe2a4f38cfabf7",
			sources["vpx-script.bbb-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"7fd6c3a4ada4ae9c8b253a2123e64c8b546ced4e9c4211edff29f01e6647f3d5",
			sources["vpx-table.bbb-vpw-1-0"]["sha256"],
		)
		self.assertEqual(
			"5fc11391e3092298e31775fdff5944554fc78db2bdb9240aa39fa9eab5dabca5",
			sources["manual.capcom.big-bang-bar.1996"]["sha256"],
		)
		self.assertEqual(
			"fab546ea34874af8d721e8a9bc514a6ab64fa6835001dc4401d3c741b948d603",
			sources["manual-schematic.capcom.big-bang-bar.1996"]["sha256"],
		)
		self.assertEqual(
			"ba5d1384397b8a1a9115b089e4a281634acb9bfb760fe096a320774a8fa2ba46",
			sources["vpx-table.bbb-archive-2013"]["sha256"],
		)
		self.assertEqual(
			"d380c476c555cdcc4c13e160841211a6aefb5bcb271d807fc04ec42a6945bd72",
			sources["vpm-script-library.core-vbs"]["sha256"],
		)
		for photo in ("ipdb-photo.capcom.big-bang-bar.1996.tube-lady", "ipdb-photo.capcom.big-bang-bar.1996.overhead"):
			self.assertIn(photo, sources)
			self.assertTrue(sources[photo]["sha256"])
		for source in self.definition["sources"]:
			self.assertNotEqual("runtime_scenario", source["kind"])
			self.assertNotEqual("rom_static_analysis", source["kind"])
			if source["kind"] in {"vpx_script", "manual", "service_bulletin"}:
				self.assertTrue(source.get("license"), source["id"])
				self.assertTrue(source.get("attribution"), source["id"])
			for value in source.values():
				if isinstance(value, str):
					self.assertNotIn("e:\\", value.lower())
					self.assertNotIn("e:/", value.lower())

	def test_new_excerpts_are_recorded_against_their_sources(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		manual_excerpt_ids = {excerpt["id"] for excerpt in sources["manual.capcom.big-bang-bar.1996"]["excerpts"]}
		self.assertIn("excerpt.big-bang-bar.solenoid-location-diagram", manual_excerpt_ids)
		self.assertIn("excerpt.big-bang-bar.game-rules-spinner-opto", manual_excerpt_ids)
		self.assertIn("excerpt.big-bang-bar.alien-mech-parts-list", manual_excerpt_ids)
		self.assertIn("excerpt.big-bang-bar.alien-motor-diagnostic-opto", manual_excerpt_ids)
		self.assertIn("excerpt.big-bang-bar.tube-lady-parts-list", manual_excerpt_ids)
		alien_excerpt = next(
			excerpt for excerpt in sources["manual.capcom.big-bang-bar.1996"]["excerpts"]
			if excerpt["id"] == "excerpt.big-bang-bar.alien-mech-parts-list"
		)
		self.assertIn("printed page 105", alien_excerpt["locator"])
		schematic_excerpt_ids = {excerpt["id"] for excerpt in sources["manual-schematic.capcom.big-bang-bar.1996"]["excerpts"]}
		self.assertIn("excerpt.big-bang-bar.lamp-matrix-b-x2-quantities", schematic_excerpt_ids)
		self.assertIn("excerpt.big-bang-bar.lamp-matrix-a-x2-quantities", schematic_excerpt_ids)
		library_excerpt_ids = {excerpt["id"] for excerpt in sources["vpm-script-library.core-vbs"]["excerpts"]} if "excerpts" in sources["vpm-script-library.core-vbs"] else set()
		self.assertNotIn("excerpt.big-bang-bar.switch-locations", library_excerpt_ids)

	def test_controller_profile_declares_every_used_binding_group(self) -> None:
		profile = load_json(CONTROLLER_PATH)
		self.assertEqual("pinmame.capcom", profile["id"])
		self.assertEqual("Capcom CC", profile["hardware_family"])
		self.assertTrue(profile["inversion_applied_by_emulator"])
		groups = {group["id"]: group for group in profile["groups"]}
		used = {device["binding"]["group"] for device in list(self.definition["inputs"]) + list(self.definition["outputs"])}
		self.assertTrue(used <= set(groups))
		lamp_group = groups["pinmame.output.lamp"]
		self.assertEqual([{"minimum": 1, "maximum": 136}], lamp_group["address_rules"])
		self.assertIn("Breakshot is a supported hardware mode", lamp_group["notes"])

		def allowed(group_id: str, address: int) -> bool:
			for rule in groups[group_id]["address_rules"]:
				if "values" in rule and address in rule["values"]:
					return True
				if "minimum" in rule and rule["minimum"] <= address <= rule["maximum"]:
					return True
			return False

		for device in list(self.definition["inputs"]) + list(self.definition["outputs"]):
			self.assertTrue(allowed(device["binding"]["group"], device["binding"]["device"]), device["id"])

	def test_curator_is_deterministic_and_the_seed_is_byte_identical(self) -> None:
		import curate_big_bang_bar as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		first = canonical_bytes(curator.build())
		second = canonical_bytes(curator.build())
		self.assertEqual(first, second)
		self.assertEqual(first, DEFINITION_PATH.read_bytes())
		self.assertEqual(first, SEED_PATH.read_bytes())

	def test_curator_check_mode_passes_twice_on_the_committed_tree(self) -> None:
		import curate_big_bang_bar as curator

		curator.check(ROOT)
		curator.check(ROOT)

	def test_curator_requires_an_explicit_mode(self) -> None:
		with self.assertRaises(SystemExit):
			_run_curator_without_mode()

	def test_curator_check_mode_refuses_drift(self) -> None:
		import curate_big_bang_bar as curator

		original = DEFINITION_PATH.read_bytes()
		try:
			DEFINITION_PATH.write_bytes(original.replace(b"Big Bang Bar", b"Big Bang Car", 1))
			with self.assertRaises(RuntimeError):
				curator.check(ROOT)
		finally:
			DEFINITION_PATH.write_bytes(original)
		curator.check(ROOT)

	def test_spatial_report_is_regenerated_from_the_definition(self) -> None:
		import curate_big_bang_bar as curator

		from pinmame_game_defs.jsonio import canonical_bytes

		report = curator.build_spatial_report(curator.build())
		self.assertEqual(canonical_bytes(report), SPATIAL_REPORT_PATH.read_bytes())


@unittest.skipUnless(os.environ.get("PINMAME_VPX_SOURCES_ROOT"), "retained VPX evidence root is not configured")
class BigBangBarRetainedEvidenceTests(unittest.TestCase):
	def test_retained_extraction_matches_its_pinned_manifest_identity(self) -> None:
		import curate_big_bang_bar as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		manifest = curator.verify_extraction_manifest(source_root)
		self.assertEqual(curator.EXTRACTION_FILE_COUNT, len(manifest["files"]))

	def test_retained_table_and_script_hashes_match_the_definition(self) -> None:
		import curate_big_bang_bar as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "capcom/big-bang-bar-1996/source/Big Bang Bar (Capcom 1996) VPW v1.0.vpx"
		script = source_root / "capcom/big-bang-bar-1996/extracted-vpxtool/script.vbs"
		self.assertEqual(curator.TABLE_SHA256, curator._file_sha256(table))
		self.assertEqual(curator.SCRIPT_SHA256, curator._file_sha256(script))

	def test_corroboration_table_and_its_cited_files_match_the_definition(self) -> None:
		import curate_big_bang_bar as curator

		source_root = curator.configured_vpx_sources_root(required=True)
		assert source_root is not None
		table = source_root / "capcom/big-bang-bar-1996/corroboration/source/Big Bang Bar  (Capcom 1996).vpx"
		self.assertEqual(curator.CORROBORATION_TABLE_SHA256, curator._file_sha256(table))
		cited_root = source_root / "capcom/big-bang-bar-1996/corroboration/extracted-Big-Bang-Bar-(Capcom-1996)/gameitems"
		for name, digest in curator.CORROBORATION_CITED_FILES.items():
			self.assertEqual(digest, curator._file_sha256(cited_root / name), name)

	def test_manual_transcription_matches_its_pinned_hash(self) -> None:
		import curate_big_bang_bar as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		transcription = Path(root) / "big-bang-bar" / "manual-transcription.md"
		self.assertEqual(curator.MANUAL_TRANSCRIPTION_SHA256, curator._file_sha256(transcription))

	def test_vpm_script_libraries_match_their_pinned_hashes(self) -> None:
		import curate_big_bang_bar as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		libs = Path(root) / "big-bang-bar" / "vpm-script-libs"
		self.assertEqual(curator.VPM_CORE_LIBRARY_SHA256, curator._file_sha256(libs / "core.vbs"))
		self.assertEqual(curator.VPM_CAPCOM_LIBRARY_SHA256, curator._file_sha256(libs / "capcom.vbs"))

	def test_retained_ipdb_photos_match_their_pinned_hashes(self) -> None:
		import curate_big_bang_bar as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		photos = Path(root) / "big-bang-bar" / "ipdb-photos"
		self.assertEqual(curator.IPDB_TUBE_LADY_PHOTO_SHA256, curator._file_sha256(photos / "ipdb-4001-image-13-tube-lady-playfield.jpg"))
		self.assertEqual(curator.IPDB_OVERHEAD_PHOTO_SHA256, curator._file_sha256(photos / "ipdb-4001-image-6-playfield-overhead.jpg"))

	def test_installed_core_vbs_constants_still_name_the_hold_side_addresses(self) -> None:
		# The flipper-mirror resolution depends on the contributor's installed library; if the
		# library changes its constants, the resolution text on outputs 45/47 must be revisited.
		import curate_big_bang_bar as curator

		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("review-artifacts root is not configured")
		text = (Path(root) / "big-bang-bar" / "vpm-script-libs" / "core.vbs").read_text(encoding="utf-8", errors="replace")
		self.assertIn("Const sLRFlipper = 46", text)
		self.assertIn("Const sLLFlipper = 48", text)
		self.assertEqual(curator.VPM_CORE_LIBRARY_SHA256, curator._file_sha256(Path(root) / "big-bang-bar" / "vpm-script-libs" / "core.vbs"))


if __name__ == "__main__":
	unittest.main()
