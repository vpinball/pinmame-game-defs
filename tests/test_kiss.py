"""Fail-closed tests for the Bally Kiss (1979) definition.

Kiss is the project's second Bally MPU AS-2518-35 machine. Most of what is worth guarding here
is the lamp chain, because it is derived rather than read off a single page: the public address
decomposes through the lamp strobe, the decoder output reaches an SCR, the SCR reaches a connector
pin, and only then does a printed function appear. Each of those steps is asserted separately so a
regression names the step that broke.
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITION_PATH = ROOT / "machines" / "author-ready" / "bally" / "kiss-1979.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "kiss-1979.md"
EVIDENCE_PATH = ROOT / "evidence" / "runtime" / "by35" / "kiss-solenoid-self-test.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "by35.json"

# Printed Self Test # -> (public address, device id). The printed column is a test order, not an
# address; this mapping was read off the running ROM and must never be "tidied" into an identity.
SELF_TEST_TO_PUBLIC = {
	1: (7, "device.outhole-kicker"),
	2: (6, "device.knocker"),
	3: (14, "device.drop-target-reset"),
	4: (9, "device.left-thumper-bumper"),
	5: (10, "device.right-thumper-bumper"),
	6: (11, "device.bottom-thumper-bumper"),
	7: (8, "device.top-thumper-bumper"),
	8: (12, "device.left-slingshot"),
	9: (13, "device.right-slingshot"),
	10: (17, "device.right-bottom-gate"),
	11: (18, "device.coin-lockout"),
	12: (19, "device.k1-flipper-relay"),
}

# public -> (A9J2 pin, label). Board wiring is primary; the pin functions are the Bally Kiss lamp
# chart, disclosed as secondary in each device note.
AUXILIARY = {
	65: (7, "Back Box K1 & K2"), 66: (6, "Back Box K3 & K4"), 67: (5, "Back Box K5 & K6"),
	81: (1, "Back Box I1"), 82: (2, "Back Box I2"), 83: (3, "Back Box I3"),
	97: (18, "Back Box SA1 & SA2 (Left)"), 98: (19, "Back Box SA3 (Left)"),
	99: (20, "Back Box SA4 (Left)"),
	113: (11, "Back Box SB1 & SB2 (Right)"), 114: (12, "Back Box SB3 (Right)"),
	115: (17, "Back Box SB4 (Right)"),
}


def load(path: Path) -> dict:
	return json.loads(path.read_text(encoding="utf-8"))


class KissDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load(DEFINITION_PATH)
		cls.switches = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.switch"
		}
		cls.dips = {
			item["binding"]["device"]: item
			for item in cls.definition["inputs"]
			if item["binding"]["group"] == "pinmame.input.dip"
		}
		cls.solenoids = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.solenoid"
		}
		cls.lamps = {
			item["binding"]["device"]: item
			for item in cls.definition["outputs"]
			if item["binding"]["group"] == "pinmame.output.lamp"
		}

	# ------------------------------------------------------------- identity --
	def test_identity_matches_the_manual_and_ipdb(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.kiss.1979", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1979, machine["year"])
		self.assertEqual(1386, machine["ipdb_id"])

	def test_playfield_extent_matches_the_retained_table_bounds(self) -> None:
		"""The normalized coordinates were computed from these bounds, so they must agree."""
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual("vpx", playfield["units"])
		self.assertAlmostEqual(952.941, playfield["width"], places=3)
		self.assertAlmostEqual(1976.471, playfield["height"], places=3)

	def test_the_intel_prototypes_are_not_part_of_this_machine(self) -> None:
		"""kissp and kissp2 are a different physical machine and must stay out.

		PinMAME declares them clones of kiss, but that is emulator metadata. They live in
		kissproto.c on an Intel 8035, and IPDB records them as about eleven "New Technology"
		prototypes with blue vacuum-fluorescent displays, no speech and a three-board architecture -
		"a completely different design". Grouping them here would erase that.
		"""
		ids = {driver["id"] for driver in self.definition["drivers"]}
		self.assertEqual({"kiss", "kissb", "kissc", "kissd", "kisse", "kissf"}, ids)
		self.assertNotIn("kissp", ids)
		self.assertNotIn("kissp2", ids)

	def test_only_the_original_driver_publishes_the_auxiliary_board(self) -> None:
		"""lampCol = 8 on kiss alone is an emulator difference, not a hardware one."""
		note = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("Only `kiss` declares `lampCol = 8`", note)
		self.assertIn("A9 board is fitted to every Kiss", note)

	# ------------------------------------------------------------ solenoids --
	def test_self_test_numbers_are_not_public_addresses(self) -> None:
		for self_test, (public, device_id) in SELF_TEST_TO_PUBLIC.items():
			device = self.solenoids[public]
			self.assertEqual(device_id, device["id"], public)
			self.assertIn(
				{"namespace": "manual.self-test", "value": str(self_test)},
				device["aliases"],
				f"public {public} must carry its printed self-test number {self_test}",
			)
		# If the two ever coincided the mapping would be suspect rather than convenient.
		identity = [t for t, (p, _) in SELF_TEST_TO_PUBLIC.items() if t == p]
		self.assertEqual([], identity, "no printed number should equal its public address here")

	def test_mapping_matches_the_retained_evidence_record(self) -> None:
		observed = load(EVIDENCE_PATH)["runtime"]["observations"]["physical_service_solenoid_to_public"]
		expected = {str(t): p for t, (p, _) in SELF_TEST_TO_PUBLIC.items()}
		self.assertEqual(expected, observed)

	def test_continuous_output_twenty_is_unused(self) -> None:
		"""Three continuous devices are printed; the fourth output only pulses at power-on."""
		device = self.solenoids[20]
		self.assertEqual("unused", device["availability"])
		self.assertIn("power-on pulse", device["physical"]["notes"])

	def test_public_seventeen_is_a_coil_here_not_a_switch_strobe(self) -> None:
		"""The game-specific inventory and runtime leave this address free for the detour gate.

		A six-column BY35 game can spend one continuous output on the sixth column strobe. Kiss has
		forty listed switches and uses 17 to drive the right outlane detour gate instead.
		"""
		device = self.solenoids[17]
		self.assertEqual("used", device["availability"])
		self.assertEqual("device.right-bottom-gate", device["id"])
		self.assertIn("five-column", device["physical"]["notes"])

	def test_no_solenoid_address_sixteen(self) -> None:
		self.assertNotIn(16, self.solenoids)

	# -------------------------------------------------------------- switches --
	def test_five_column_matrix_stops_at_forty(self) -> None:
		"""The game-specific printed inventory ends at 40 and 41-48 are not populated."""
		for address in range(41, 49):
			device = self.switches[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertIn("five-column", device["physical"]["notes"], address)
		for address in (28, 29, 32):
			self.assertEqual("unused", self.switches[address]["availability"], address)

	def test_j2_correction_is_not_used_as_five_column_proof(self) -> None:
		"""The generic J2 block does not rule out an ST5 routed through another connector."""
		for address in range(41, 49):
			self.assertNotIn(
				"manual-omissions.bally.kiss.1979",
				self.switches[address]["provenance"]["source_refs"],
				address,
			)

	def test_flipper_buttons_are_not_matrix_switches(self) -> None:
		"""On this generation they are wired through the K1 relay, so 81-88 are emulator mirrors."""
		for address in (82, 84):
			device = self.switches[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertIn("K1 flipper-enable relay", device["physical"]["notes"], address)

	def test_parallel_contact_counts_match_their_placements(self) -> None:
		"""The printed table brackets a contact count against three addresses."""
		self.assertEqual(3, self.switches[7]["physical"]["quantity"])   # Tilt (3)
		self.assertEqual(2, self.switches[16]["physical"]["quantity"])  # Slam (2)
		self.assertEqual(3, self.switches[25]["physical"]["quantity"])  # Drop Target and 2 Rebs.
		self.assertEqual(3, len(self.switches[25]["spatial"]["placements"]))

	def test_top_rollovers_spell_the_title_left_to_right(self) -> None:
		"""24 K, 23 I, 22 inner S, 21 outer S must run left to right across the top.

		This is the cheap check that would have caught the reversed pair on Centaur.
		"""
		order = [24, 23, 22, 21]
		xs = [self.switches[a]["spatial"]["placements"][0]["x"] for a in order]
		self.assertEqual(sorted(xs), xs, "top rollovers must ascend in x as K, I, S, S")

	def test_thumper_bumpers_sit_where_the_manual_names_them(self) -> None:
		top = self.switches[38]["spatial"]["placements"][0]
		bottom = self.switches[37]["spatial"]["placements"][0]
		left = self.switches[40]["spatial"]["placements"][0]
		right = self.switches[39]["spatial"]["placements"][0]
		self.assertLess(top["y"], bottom["y"], "the top bumper must sit nearer the backglass")
		self.assertLess(left["x"], right["x"], "the left bumper must sit left of the right one")

	# ----------------------------------------------------------------- lamps --
	def test_lamp_inventory_splits_exactly(self) -> None:
		"""53 placed, 18 back box only, 5 dead = 76 = 60 main board + 16 auxiliary.

		The 53 placed addresses are 46 playfield-only plus the 7 that light a backglass socket and a
		playfield insert. The retained table models exactly 53 lamp objects, and that exact agreement
		is the check that the derivation is right. An earlier pass read only one connector endpoint
		per SCR, arrived at 45, and explained away the difference; the difference was real.
		"""
		playfield = backbox = unused = 0
		for device in self.lamps.values():
			spatial = device["spatial"]
			if spatial["status"] == "validated":
				playfield += 1
			elif spatial.get("reason") == "cabinet_or_service":
				backbox += 1
			else:
				unused += 1
		self.assertEqual(53, playfield)
		self.assertEqual(18, backbox)
		self.assertEqual(5, unused)
		self.assertEqual(76, len(self.lamps))

	def test_scr_fan_out_is_read_from_this_game_s_schematic(self) -> None:
		"""An SCR reaches more than one connector branch, so endpoints are game-specific.

		Public 43's SCR Q40 goes to both A5J2-9, marked N/U, and A5J3-22 "Same Player Shoots Again"
		on the block marked TO PLAYFIELD. Only the J2 branch is unused. Reusing another machine's
		single-endpoint table drops whichever branch that machine did not plug.
		"""
		device = self.lamps[43]
		self.assertEqual("used", device["availability"])
		self.assertEqual("Same Player Shoots Again", device["label"])
		self.assertEqual("validated", device["spatial"]["status"])
		self.assertIn("A5J3-22", device["physical"]["notes"])

	def test_mixed_backglass_and_playfield_lamps_are_placed(self) -> None:
		"""Table B routes seven A5J2 pins onward to playfield inserts through the panel plug."""
		for address in (15, 30, 31, 46, 47, 62, 63):
			device = self.lamps[address]
			self.assertEqual(2, device["physical"]["quantity"], address)
			self.assertEqual("validated", device["spatial"]["status"], address)
			self.assertEqual(1, len(device["spatial"]["placements"]), address)
			self.assertIn("panel-to-back-cab", device["physical"]["notes"], address)

	def test_hardware_switch_to_coil_pairings_are_recorded(self) -> None:
		"""The printed table says these coils energize when their switch makes."""
		pairs = {
			("switch.right-slingshot", "device.right-slingshot"),
			("switch.left-slingshot", "device.left-slingshot"),
			("switch.bottom-thumper-bumper", "device.bottom-thumper-bumper"),
			("switch.top-thumper-bumper", "device.top-thumper-bumper"),
			("switch.right-thumper-bumper", "device.right-thumper-bumper"),
			("switch.left-thumper-bumper", "device.left-thumper-bumper"),
		}
		recorded = {
			(rel["source"], rel["destination"])
			for rel in self.definition["relationships"] if rel["kind"] == "direct"
		}
		self.assertEqual(pairs, recorded)

	def test_unreachable_decoder_slots_have_no_address(self) -> None:
		"""lampadr 15 is skipped, so these are not lamps at all."""
		for address in (16, 32, 48, 64, 80, 96, 112, 128):
			self.assertNotIn(address, self.lamps, address)

	def test_letter_columns_read_left_to_right_as_kiss(self) -> None:
		"""K, I, S, S must ascend in x, and each letter's five lamps share one column."""
		letters = {
			"K": [1, 2, 3, 4, 6], "I": [17, 18, 19, 20, 22],
			"S-left": [33, 34, 35, 36, 38], "S-right": [49, 50, 51, 52, 54],
		}
		centres = []
		for name, addresses in letters.items():
			xs = [self.lamps[a]["spatial"]["placements"][0]["x"] for a in addresses]
			self.assertLess(max(xs) - min(xs), 0.02, f"{name} lamps must share a column")
			centres.append(sum(xs) / len(xs))
		self.assertEqual(sorted(centres), centres, "the letter columns must spell KISS left to right")

	def test_auxiliary_circuits_are_backglass_and_cite_their_wiring(self) -> None:
		for address, (pin, label) in AUXILIARY.items():
			device = self.lamps[address]
			self.assertEqual(label, device["label"], address)
			self.assertEqual("not_applicable", device["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", device["spatial"]["reason"], address)
			self.assertIn(f"A9J2-{pin}", device["physical"]["notes"], address)
			# The secondary source must be disclosed on every one of them, never silently relied on.
			self.assertIn("secondary source", device["physical"]["notes"], address)

	def test_unpopulated_auxiliary_positions_carry_no_lamp(self) -> None:
		"""Q3 is N/U on all four MC14555B halves, so latched address 3 reaches no bulb."""
		for address in (68, 84, 100, 116):
			device = self.lamps[address]
			self.assertEqual("unused", device["availability"], address)
			self.assertEqual("unused", device["spatial"]["reason"], address)
			self.assertIn("N/U", device["physical"]["notes"], address)

	def test_the_one_unwired_main_board_output_is_not_a_lamp(self) -> None:
		"""A5J2-16 is marked N/U, so public 14 drives nothing. Public 43 is NOT in this set."""
		device = self.lamps[14]
		self.assertEqual("unused", device["availability"])
		self.assertIn("N/U", device["physical"]["notes"])
		self.assertEqual("used", self.lamps[43]["availability"])

	def test_every_placed_lamp_has_as_many_placements_as_bulbs(self) -> None:
		"""Placements must equal the bulb count, and the only shortfall is declared.

		The seven mixed addresses drive two sockets - one on the backglass and one on the playfield -
		but only the playfield insert has a coordinate, so they carry one placement for a quantity of
		two. Nothing else may fall short.
		"""
		mixed = {15, 30, 31, 46, 47, 62, 63}
		for address, device in self.lamps.items():
			spatial = device["spatial"]
			if spatial["status"] != "validated":
				continue
			quantity = device["physical"]["quantity"]
			placed = len(spatial["placements"])
			if address in mixed:
				self.assertEqual(2, quantity, address)
				self.assertEqual(1, placed, address)
			else:
				self.assertEqual(quantity, placed, address)

	def test_no_two_placements_describe_the_same_point(self) -> None:
		"""A render primitive stacked on a device is not a second physical location."""
		for item in self.definition["inputs"] + self.definition["outputs"]:
			placements = (item.get("spatial") or {}).get("placements") or []
			for index, one in enumerate(placements):
				for other in placements[index + 1:]:
					self.assertFalse(
						abs(one["x"] - other["x"]) <= 0.01 and abs(one["y"] - other["y"]) <= 0.01,
						f"{item['id']}: {one['id']} and {other['id']} are the same location",
					)

	# ------------------------------------------------------------- coverage --
	def test_coverage_is_author_ready_with_nothing_missing(self) -> None:
		coverage = self.definition["coverage"]
		self.assertEqual("author_ready", coverage["status"])
		self.assertEqual([], coverage["missing"])
		self.assertTrue(all(v == "validated" for v in coverage["dimensions"].values()))
		self.assertEqual([], self.definition["conflicts"])

	def test_every_device_carries_a_spatial_record(self) -> None:
		for item in self.definition["inputs"] + self.definition["outputs"]:
			self.assertIn("spatial", item, item["id"])
		for display in self.definition["displays"]:
			self.assertIn("spatial", display, display["id"])

	def test_displays_match_the_six_digit_layout(self) -> None:
		displays = {d["controller_index"]: d for d in self.definition["displays"]}
		self.assertEqual(6, len(displays))
		for index, start in enumerate((2, 10, 18, 26)):
			self.assertEqual(6, displays[index]["width"], index)
			self.assertEqual(start, displays[index]["segment_start"], index)
		self.assertEqual(2, displays[4]["width"])
		self.assertEqual(2, displays[5]["width"])

	def test_dip_switches_are_kiss_specific(self) -> None:
		"""Centaur's assignments must not have been carried across."""
		self.assertEqual(32, len(self.dips))
		self.assertIn("chute #2", self.dips[25]["label"])
		self.assertIn("Credit display", self.dips[20]["label"])
		self.assertIn("Match feature", self.dips[21]["label"])
		self.assertIn("Balls per game", self.dips[16]["label"])


class KissEvidenceTests(unittest.TestCase):
	def test_retained_traces_are_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		import hashlib

		record = load(EVIDENCE_PATH)
		for run in record["runtime"]["raw_runs"]:
			name = "soltest.json" if "self-test" in run["name"] else "playtest.json"
			path = Path(root) / "kiss-1979" / "harness" / name
			self.assertTrue(path.is_file(), str(path))
			digest = hashlib.sha256(path.read_bytes()).hexdigest()
			self.assertEqual(run["sha256"], digest, str(path))

	def test_auxiliary_sources_are_reachable_when_configured(self) -> None:
		"""The two sources the auxiliary identities rest on must be fail-closed, not just cited.

		Both were added after a review round and neither was covered by an evidence-root check, so
		the suite would have passed if either disappeared or drifted.
		"""
		import hashlib

		artifacts = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
		manuals = os.environ.get("PINMAME_MANUALS_ROOT")
		if not artifacts or not manuals:
			self.skipTest("evidence roots are not configured")
		expected = {
			Path(artifacts) / "kiss-1979" / "pinwiki-bally-kiss.txt":
				"6b1560451d9c43668c23854fbf40f8b5e4567dda63231e5fa7c866e1e89c7fc7",
			Path(manuals) / "by-machine" / "bally.centaur.1981" / "projects-centaur"
			/ "Bally_1981_Centaur_Installation_and_General_Game_Operation_Instructions_with_schematics_OCR_searchable.pdf":
				"c5b151bfc2d2672fce7b405519bda07051bd54e115e9484f39fe05159d47bc23",
		}
		for path, digest in expected.items():
			self.assertTrue(path.is_file(), str(path))
			self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest(), str(path))

	def test_recorded_source_hashes_match_the_definition(self) -> None:
		"""Whatever the tests check must be what the definition actually cites."""
		sources = {s["id"]: s for s in load(DEFINITION_PATH)["sources"]}
		self.assertEqual(
			"6b1560451d9c43668c23854fbf40f8b5e4567dda63231e5fa7c866e1e89c7fc7",
			sources["lamp-chart.bally.kiss.1979"]["sha256"],
		)
		self.assertEqual(
			"c5b151bfc2d2672fce7b405519bda07051bd54e115e9484f39fe05159d47bc23",
			sources["schematic.as-2518-43-auxiliary-lamp-driver"]["sha256"],
		)
		self.assertEqual(
			"2f39bd677aeecd26605ac832a419d5b6d3922e3016a7e0c64a1dd19b2e2d9e3e",
			sources["manual-omissions.bally.kiss.1979"]["sha256"],
		)

	def test_manual_is_reachable_when_configured(self) -> None:
		root = os.environ.get("PINMAME_MANUALS_ROOT")
		if not root:
			self.skipTest("evidence roots are not configured")
		import hashlib

		for name, digest in {
			"Bally_1979_Kiss_Manual.pdf": "b9f7b1dfbc76267bce3e14544f9f576b07a08b9909acc13913f3e906464292d1",
			"Bally_1979_Kiss_Omissions_to_Schematic_Diagrams_user_submitted.pdf": "2f39bd677aeecd26605ac832a419d5b6d3922e3016a7e0c64a1dd19b2e2d9e3e",
		}.items():
			path = Path(root) / "by-machine" / "bally.kiss.1979" / name
			self.assertTrue(path.is_file(), str(path))
			self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest(), str(path))


if __name__ == "__main__":
	unittest.main()
