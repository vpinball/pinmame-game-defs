from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "lord-of-the-rings-2003.json"
SEED_PATH = ROOT / "tools" / "seeds" / "stern" / "lord-of-the-rings-2003.json"
AUTHOR_READY_PATH = ROOT / "machines" / "author-ready" / "stern" / "lord-of-the-rings-2003.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "stern" / "lord-of-the-rings-2003.md"
CONTROLLER_PATH = ROOT / "controllers" / "pinmame" / "whitestar.json"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "stern" / "lord-of-the-rings-2003.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"

MATRIX_ADDRESSES = set(range(1, 65))
UNUSED_MATRIX_ADDRESSES = {26, 27, 63, 64}
OPTO_ADDRESSES = {14, 15, 41, 47}
UK_ONLY_SWITCHES = {1, 8}
DEDICATED_ADDRESSES = {-3, -2, -1, 0, 81, 82, 83, 84}
FLIPPER_COLUMN_HOLES = {85, 86, 87, 88}
UNUSED_SOLENOIDS = {12, 28}
FLASHER_ADDRESSES = {14, 23, 25, 26, 27, 29, 30, 31, 32}
UK_AUX_SOLENOIDS = {33, 34, 35}
BACK_PANEL_MODE_LAMPS = {73, 74, 75, 76, 77, 78}


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def bindings(definition: dict, collection: str, group: str) -> dict[int, dict]:
	return {
		item["binding"]["device"]: item
		for item in definition[collection]
		if item["binding"]["group"] == group
	}


class LordOfTheRingsDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = bindings(cls.definition, "inputs", "pinmame.input.switch")
		cls.solenoids = bindings(cls.definition, "outputs", "pinmame.output.solenoid")
		cls.lamps = bindings(cls.definition, "outputs", "pinmame.output.lamp")

	def test_machine_identity(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("stern.lord-of-the-rings.2003", machine["id"])
		self.assertEqual("Stern", machine["manufacturer"])
		self.assertEqual(2003, machine["year"])

	def test_promotion_state_is_held_at_partial(self) -> None:
		"""Held at partial by polarity, spatial, and edition-compatibility gaps.

		The 520-5242-00 LED board is enumerated, but its positions are observed rather than
		corroborated. Switch 15's public opto polarity and the LE hardware remain unestablished.
		"""
		coverage = self.definition["coverage"]
		self.assertEqual("partial", coverage["status"])
		self.assertEqual(
			["polarity", "spatial_placement", "unresolved_conflicts", "variant_differences"],
			coverage["missing"],
		)
		self.assertEqual("validated", coverage["dimensions"]["address_enumeration"])
		self.assertEqual("observed", coverage["dimensions"]["spatial_placement"])
		self.assertEqual("conflicted", coverage["dimensions"]["physical_wiring"])
		self.assertEqual("observed", coverage["dimensions"]["variant_coverage"])
		self.assertEqual(2, self.definition["schema_version"])

	def test_optos_do_not_claim_an_inversion_pinmame_never_applies(self) -> None:
		"""Whitestar normalizes nothing, and only switch 15 is left unsettled by that.

		`lotrGameData` is a positional aggregate that stops after the `hw` struct, so the
		trailing `wpc` member -- and with it `wpc.invSw` -- is zero-initialized, and core.c
		copies those zeros into the live mask. An earlier pass of this definition said "PinMAME
		normalizes the public state", reaching the right instruction for a recreation through a
		mechanism that does not exist.

		The distinction this locks down is between the three optos a known-working recreation
		settles by observation and the one it does not. Asserting only the conflict would let a
		later pass quietly widen it to all four; asserting only the notes would let the conflict
		be dropped.
		"""
		optos = {address: device for address, device in self.switches.items()
		         if device.get("physical", {}).get("switch_type") == "opto"}
		self.assertEqual({14, 15, 41, 47}, set(optos))
		for address, device in optos.items():
			notes = device["physical"]["notes"]
			self.assertNotIn("PinMAME normalizes", notes, f"switch {address} claims an inversion PinMAME never applies")
			self.assertIn("zero-initialized", notes, f"switch {address} must say why no inversion is applied")
			self.assertTrue(device["normally_closed"], f"switch {address} is a printed opto")
		for address in (14, 41, 47):
			self.assertIn("known-working VPW 1.6 script asserts this address", optos[address]["physical"]["notes"])
		self.assertIn("No retained recreation binds this address", optos[15]["physical"]["notes"])

		conflict = next(c for c in self.definition["conflicts"] if c["id"] == "conflict.whitestar-invsw-never-populated")
		self.assertIn("binding.device=15", conflict["path"])
		for address in (14, 41, 47):
			self.assertNotIn(f"binding.device={address}", conflict["path"])

	def test_led_board_is_enumerated_without_inventing_allocation_slots(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		conflicted = {86, 87, 88, 89, 94}
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual(set(range(81, 100)), set(self.lamps) & set(range(81, 105)))
		self.assertFalse(set(range(100, 105)) & set(self.lamps))
		self.assertNotIn("led-board-520-5242-00-not-enumerated", {item["id"] for item in report["blockers"]})
		for address in range(81, 100):
			device = self.lamps[address]
			self.assertEqual("observed", device["provenance"]["status"], address)
			self.assertIn("No factory semantic name", device["physical"]["notes"], address)
			self.assertNotIn("official manual and pinmame identify", device["physical"]["notes"].lower(), address)
			self.assertNotIn("manual.stern.lord-of-the-rings.2003", device["provenance"]["source_refs"], address)
			if address in conflicted:
				self.assertNotIn("spatial", device, address)
			else:
				self.assertEqual("observed", device["spatial"]["status"], address)
				refs = device["spatial"]["placements"][0]["provenance"]["source_refs"]
				self.assertNotIn("manual.stern.lord-of-the-rings.2003", refs, address)
		self.assertEqual(conflicted, {row["address"] for row in report["conflicted_led_positions"]})
		blocker = next(item for item in report["blockers"] if item["id"] == "script-bound-led-positions-conflict")
		self.assertEqual(5, len(blocker["devices"]))
		self.assertTrue(report["unresolved"])

	def test_led_positions_follow_each_script_binding_not_object_suffixes(self) -> None:
		"""Hanibal maps public 81 to l98 and 98 to l81; guessing l<N> is a silent address swap."""
		root = _vpx_root()
		if root is None:
			self.skipTest("retained VPX evidence root is not available")
		consensus = load_json(root / "derived" / "spatial-consensus.json")
		for address in range(81, 100):
			measurements = {
				row["table"]: row for row in consensus["devices"]["lamp"][str(address)]["script_bound_measurements"]
			}
			self.assertEqual({"vpw-1-6", "jpsalas-600", "hanibal-4k", "neo-led-1-0-3"}, set(measurements))
		self.assertEqual("l98", {
			row["table"]: row for row in consensus["devices"]["lamp"]["81"]["script_bound_measurements"]
		}["hanibal-4k"]["object"])
		self.assertEqual("l81", {
			row["table"]: row for row in consensus["devices"]["lamp"]["98"]["script_bound_measurements"]
		}["hanibal-4k"]["object"])

	def test_switch_11_canonical_label_is_normalized_without_rewriting_the_manual(self) -> None:
		self.assertEqual("4-Ball Trough #1 (Left)", self.switches[11]["label"])
		self.assertEqual("4-Ball Trough #2", self.switches[12]["label"])
		self.assertEqual("4-Ball Trough #3", self.switches[13]["label"])

	def test_led_source_records_describe_the_real_transport_and_neo_lineage(self) -> None:
		sources = {source["id"]: source for source in self.definition["sources"]}
		core = sources["pinmame.core.4ec52ff0ac13"]["locator"]
		self.assertIn("same widened Whitestar lamp transport", core)
		self.assertNotIn("distinct Whitestar LED-board binding group", core)
		neo = sources["vpx-table.lotr-neo-led-mod-1-0-3"]["locator"]
		self.assertIn("JPSalas", neo)
		self.assertIn("derivative", neo)
		self.assertIn("Valinor is the VPW table", neo)

	def test_no_stale_author_ready_artifact(self) -> None:
		self.assertFalse(AUTHOR_READY_PATH.exists())

	def test_dip_bank_is_enumerated(self) -> None:
		dips = bindings(self.definition, "inputs", "pinmame.input.dip")
		self.assertEqual(set(range(1, 9)), set(dips))
		for position in range(1, 6):
			self.assertEqual("used", dips[position]["availability"], position)
		for position in range(6, 9):
			self.assertEqual("unused", dips[position]["availability"], position)
		for dip in dips.values():
			self.assertEqual("dip_switch", dip["spatial"]["reason"])

	def test_validated_placements_cite_all_three_retained_tables(self) -> None:
		"""Independence between the three recreations is unestablished, so corroboration
		requires all three. Reverting the resolver to counting files, or to a lineage
		grouping, must fail here rather than pass silently."""
		all_tables = {"vpx-table.lotr-vpw-1-6", "vpx-table.lotr-jpsalas-600", "vpx-table.lotr-hanibal-4k"}
		validated = 0
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				spatial = device.get("spatial", {})
				if spatial.get("status") != "validated" or "placements" not in spatial:
					continue
				for place in spatial["placements"]:
					cited = {ref for ref in place["provenance"]["source_refs"] if ref.startswith("vpx-table.")}
					self.assertEqual(all_tables, cited, f"{device['id']} is validated on {sorted(cited)}")
					validated += 1
		self.assertGreater(validated, 0)

	def test_projected_coil_placements_never_inherit_validated(self) -> None:
		"""A coil placed at a co-located device's coordinate is a projection, not a measurement."""
		report = load_json(SPATIAL_REPORT_PATH)
		projected = {item["device"] for item in report["projections"]}
		self.assertTrue(projected)
		devices = {device["id"]: device for device in self.definition["outputs"]}
		for device_id in projected:
			self.assertEqual("observed", devices[device_id]["spatial"]["status"], device_id)

	def test_computed_coordinates_are_declared_and_never_validated(self) -> None:
		"""A coordinate no table holds cannot be a corroborated measurement of one."""
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertTrue(report["computed_coordinates"])
		computed = {(entry["kind"], entry["address"]) for entry in report["computed_coordinates"]}
		for entry in report["computed_coordinates"]:
			self.assertTrue(entry["derived_from"], entry)
		for collection, group, kind in (("inputs", "pinmame.input.switch", "switch"),
										("outputs", "pinmame.output.lamp", "lamp")):
			for address, device in bindings(self.definition, collection, group).items():
				if (kind, address) in computed:
					self.assertNotEqual("validated", device["spatial"].get("status"), device["id"])

	def test_printed_but_unplaced_devices_are_not_called_not_applicable(self) -> None:
		"""not_applicable is for cabinet and service devices. A device the printed location
		drawing places, that no retained table models, has an unresolved position: it carries no
		spatial record and appears as a blocker."""
		report = load_json(SPATIAL_REPORT_PATH)
		unplaced = {row["device"] for row in report["unplaced_devices"]}
		self.assertTrue(unplaced)
		devices = {d["id"]: d for c in ("inputs", "outputs") for d in self.definition[c]}
		for device_id in unplaced:
			self.assertNotIn("spatial", devices[device_id], device_id)
		blocker = next(b for b in report["blockers"] if b["id"] == "devices-printed-but-unplaced")
		self.assertEqual(len(unplaced), len(blocker["devices"]))

	def test_observed_partition_is_disjoint_and_complete(self) -> None:
		"""The report describes the observed set by partition, not by a hand-typed sentence."""
		report = load_json(SPATIAL_REPORT_PATH)
		partition = report["observed_partition"]
		buckets = [set(ids) for ids in partition.values()]
		for index, first in enumerate(buckets):
			for second in buckets[index + 1:]:
				self.assertEqual(set(), first & second)
		observed = {d["id"] for c in ("inputs", "outputs") for d in self.definition[c]
					if d.get("spatial", {}).get("status") == "observed"}
		self.assertEqual(observed, set().union(*buckets))

	def test_every_published_coordinate_is_in_the_spatial_derivation(self) -> None:
		"""No coordinate may bypass the deterministic resolver as an unverified curator literal."""
		import curate_lord_of_the_rings as curator

		derived = {
			(round(float(position["x"]), 6), round(float(position["y"]), 6))
			for bucket in curator.consensus["devices"].values()
			for entry in bucket.values()
			for position in ([entry] if "x" in entry else entry.get("emitters", {}).values())
			if "x" in position and "y" in position
		}
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				for placement in device.get("spatial", {}).get("placements", []):
					coordinate = (round(float(placement["x"]), 6), round(float(placement["y"]), 6))
					self.assertIn(coordinate, derived, device["id"])

	def test_blocker_counts_agree_with_the_definition(self) -> None:
		"""The report's prose is computed from the artifact, not written beside it."""
		report = load_json(SPATIAL_REPORT_PATH)
		blocker = next(item for item in report["blockers"] if item["id"] == "placements-not-fully-corroborated")
		observed = [
			device["id"]
			for collection in ("inputs", "outputs")
			for device in self.definition[collection]
			if device.get("spatial", {}).get("status") == "observed"
		]
		self.assertEqual(len(observed), len(blocker["devices"]))
		self.assertIn(str(len(observed)), blocker["summary"])

	def test_printed_insert_names_keep_their_capitalisation(self) -> None:
		"""(K) EEP marks which letter the insert lights; re-casing it throws the name away."""
		expected = {1: "(K) EEP", 2: "K (E) EP", 3: "KE (E) P", 4: "KEE (P)",
					57: "(O) RC", 58: "O (R) C", 59: "OR (C)"}
		for address, label in expected.items():
			self.assertEqual(label, self.lamps[address]["label"])

	def test_controller_is_the_shared_whitestar_profile(self) -> None:
		self.assertEqual("pinmame.whitestar", self.definition["controller"]["platform"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])
		self.assertTrue(CONTROLLER_PATH.is_file())

	def test_uk_auxiliary_coils_record_their_own_driver_board(self) -> None:
		for address in UK_AUX_SOLENOIDS:
			self.assertEqual("UK 3X Transformer Driver Board", self.solenoids[address]["wiring"]["board"], address)

	def test_no_ball_path_is_asserted_as_causality(self) -> None:
		"""Coil 1 launches a ball that later rolls over switch 16; it does not actuate it."""
		links = {(item["source"], item["destination"]) for item in self.definition["relationships"]}
		self.assertNotIn(("device.trough-up-kicker", "switch.matrix-16"), links)

	def test_every_driver_carries_a_compatibility_verdict_and_notes(self) -> None:
		"""`physical_compatibility` is a claim about the machine, not about the driver routing.

		An earlier revision asserted `identical` for all 46 drivers on the strength of a shared
		`init_lotr`. That proves the emulated hardware matches; it says nothing about the cabinet.
		The 2008 Limited Edition is the one driver where that gap matters - a limited run is
		exactly where a manufacturer adds hardware such as a shaker motor - and nothing retained
		here documents that machine, so it is `unknown` rather than asserted either way.
		"""
		drivers = self.definition["drivers"]
		self.assertEqual(46, len(drivers))
		for driver in drivers:
			expected = "unknown" if driver["id"] == "lotr_le" else "identical"
			self.assertEqual(expected, driver["physical_compatibility"], driver["id"])
			self.assertTrue(driver["variant_notes"].strip())
		limited = next(driver for driver in drivers if driver["id"] == "lotr_le")
		self.assertIn("Limited Edition", limited["variant_notes"])
		self.assertIn("not established by anything retained here", limited["variant_notes"])

	def test_no_relationship_claims_the_balrog_limits_are_complementary(self) -> None:
		"""`inverted` would assert each limit switch is the logical complement of the other.

		Two end-of-travel switches can both be open while the drive is in transit. The retained
		script does keep exactly one of the pair asserted, but that is the recreation's two-state
		model rather than an observation of the machine, and nothing retained here watches the
		mechanism mid-travel.
		"""
		for relationship in self.definition["relationships"]:
			if relationship["kind"] != "inverted":
				continue
			self.assertNotIn(relationship["source"], {"switch.matrix-31", "switch.matrix-32"})
			self.assertNotIn(relationship["destination"], {"switch.matrix-31", "switch.matrix-32"})

	def test_catalog_maps_every_driver_to_this_definition(self) -> None:
		catalog = load_json(CATALOG_PATH)
		relative = DEFINITION_PATH.relative_to(ROOT).as_posix()
		mapped = {record["id"] for record in catalog["drivers"] if record.get("definition") == relative}
		self.assertEqual({driver["id"] for driver in self.definition["drivers"]}, mapped)
		machine = next(record for record in catalog["machines"] if record["id"] == "stern.lord-of-the-rings.2003")
		self.assertEqual("partial", machine["coverage_status"])
		self.assertEqual(relative, machine["definition"])

	def test_full_switch_enumeration(self) -> None:
		expected = MATRIX_ADDRESSES | DEDICATED_ADDRESSES | FLIPPER_COLUMN_HOLES
		self.assertEqual(expected, set(self.switches))

	def test_unused_matrix_positions_are_declared_unused(self) -> None:
		for address in UNUSED_MATRIX_ADDRESSES:
			switch = self.switches[address]
			self.assertEqual("unused", switch["availability"], address)
			self.assertEqual("unused", switch["spatial"]["reason"], address)

	def test_optos_rest_closed_and_everything_else_rests_open(self) -> None:
		for address in MATRIX_ADDRESSES - UNUSED_MATRIX_ADDRESSES:
			switch = self.switches[address]
			self.assertEqual(address in OPTO_ADDRESSES, switch["normally_closed"], address)
			if address in OPTO_ADDRESSES:
				self.assertEqual("opto", switch["physical"]["switch_type"], address)

	def test_dedicated_switches_use_the_profile_addresses_not_the_matrix(self) -> None:
		"""Whitestar publishes the printed DS-1..DS-8 outside the matrix, at -3..0 and 81-84."""
		self.assertEqual("Left Flipper Button", self.switches[84]["label"])
		self.assertEqual("Left Flipper End-of-Stroke", self.switches[83]["label"])
		self.assertEqual("Right Flipper Button", self.switches[82]["label"])
		self.assertEqual("Right Flipper End-of-Stroke", self.switches[81]["label"])
		self.assertEqual("Volume (Red Button)", self.switches[-2]["label"])
		self.assertEqual("Service Credit (Green Button)", self.switches[-1]["label"])
		self.assertEqual("Begin Test (Black Button)", self.switches[0]["label"])
		self.assertEqual("Memory Protect", self.switches[-3]["label"])
		for address in (81, 83):
			self.assertTrue(any(role.startswith("internal.") for role in self.switches[address]["roles"]))
			# The printed dedicated-switch table puts DS-2 and DS-4 below the playfield, so their
			# position is unresolved and they carry no spatial record. This test used to assert
			# `internal_nonvisual` here, which is how the false claim survived six rounds.
			self.assertNotIn("spatial", self.switches[address])

	def test_uk_only_cabinet_buttons_are_optional(self) -> None:
		for address in UK_ONLY_SWITCHES:
			switch = self.switches[address]
			self.assertEqual("optional", switch["availability"], address)
			self.assertIn("UK", switch["physical"]["notes"])

	def test_flipper_column_holes_are_unused(self) -> None:
		for address in FLIPPER_COLUMN_HOLES:
			self.assertEqual("unused", self.switches[address]["availability"], address)

	def test_flipper_coils_are_at_46_and_48_not_the_printed_15_and_16(self) -> None:
		"""Whitestar removes the physical flipper coils from public 15/16.

		The manual prints them as coils #15 and #16, but PinMAME exposes the right coil at
		power-phase 45 with canonical callback 46 and the left at power-phase 47 with callback
		48. VPM's core.vbs agrees with sLRFlipper = 46 and sLLFlipper = 48.
		"""
		right, left = self.solenoids[46], self.solenoids[48]
		self.assertEqual("device.right-flipper", right["id"])
		self.assertEqual("device.left-flipper", left["id"])
		self.assertEqual("coil", right["kind"])
		self.assertEqual("coil", left["kind"])
		manual_aliases = {
			alias["value"] for alias in right["aliases"] + left["aliases"] if alias["namespace"] == "manual.address"
		}
		self.assertEqual({"#15", "#16"}, manual_aliases)

	def test_flipper_power_phases_are_declared_not_duplicated(self) -> None:
		for address, target in ((45, "device.right-flipper"), (47, "device.left-flipper")):
			phase = self.solenoids[address]
			self.assertEqual("control_signal", phase["kind"])
			self.assertEqual("internal_nonvisual", phase["spatial"]["reason"])
		links = {
			(item["source"], item["destination"])
			for item in self.definition["relationships"]
			if item["kind"] == "direct"
		}
		self.assertIn(("device.right-flipper-power-phase", "device.right-flipper"), links)
		self.assertIn(("device.left-flipper-power-phase", "device.left-flipper"), links)

	def test_public_15_is_the_synthetic_fast_flip_state(self) -> None:
		state = self.solenoids[15]
		self.assertEqual("virtual", state["kind"])
		self.assertEqual("virtual", state["spatial"]["reason"])
		self.assertNotIn("wiring", state)

	def test_unused_solenoids_are_declared_unused(self) -> None:
		for address in UNUSED_SOLENOIDS:
			self.assertEqual("unused", self.solenoids[address]["availability"], address)

	def test_uk_auxiliary_posts_occupy_33_to_35_and_36_is_unused(self) -> None:
		for address in UK_AUX_SOLENOIDS:
			coil = self.solenoids[address]
			self.assertEqual("optional", coil["availability"], address)
			self.assertIn("UK", coil["label"])
		self.assertEqual("unused", self.solenoids[36]["availability"])

	def test_flashers_are_exactly_the_printed_set(self) -> None:
		flashers = {address for address, item in self.solenoids.items() if item["kind"] == "flasher"}
		self.assertEqual(FLASHER_ADDRESSES, flashers)

	def test_pop_bumper_flasher_has_one_placement_per_physical_bulb(self) -> None:
		flasher = self.solenoids[25]
		self.assertEqual(3, flasher["physical"]["quantity"])
		self.assertEqual("validated", flasher["spatial"]["status"])
		placements = flasher["spatial"]["placements"]
		self.assertEqual(3, len(placements))
		self.assertEqual(
			{"device.pop-bumper-flashers.left.emitter", "device.pop-bumper-flashers.right.emitter", "device.pop-bumper-flashers.bottom.emitter"},
			{placement["id"] for placement in placements},
		)
		by_id = {placement["id"]: placement for placement in placements}
		for side, switch_address in (("left", 49), ("right", 50), ("bottom", 51)):
			placement = by_id[f"device.pop-bumper-flashers.{side}.emitter"]
			switch = self.switches[switch_address]["spatial"]["placements"][0]
			self.assertLessEqual(abs(placement["x"] - switch["x"]), 0.01)
			self.assertLessEqual(abs(placement["y"] - switch["y"]), 0.01)
			self.assertEqual("validated", placement["provenance"]["status"])
			self.assertEqual(
				{"vpx-table.lotr-vpw-1-6", "vpx-table.lotr-jpsalas-600", "vpx-table.lotr-hanibal-4k"},
				{ref for ref in placement["provenance"]["source_refs"] if ref.startswith("vpx-table.")},
			)

	def test_ring_magnet_is_a_magnet_and_records_its_dedicated_fuse(self) -> None:
		magnet = self.solenoids[6]
		self.assertEqual("magnet", magnet["kind"])
		self.assertIn("F20", magnet["physical"]["notes"])

	def test_balrog_motor_and_relay_are_typed_and_gated(self) -> None:
		self.assertEqual("motor", self.solenoids[22]["kind"])
		self.assertEqual("relay", self.solenoids[20]["kind"])
		gated = {
			(item["source"], item["destination"])
			for item in self.definition["relationships"]
			if item["kind"] == "relay_gated"
		}
		self.assertIn(("device.balrog-motor-relay", "device.balrog-motor"), gated)

	def test_matrix_and_led_board_share_the_lamp_transport_without_inventing_slots(self) -> None:
		"""The printed matrix is public 1-80; board 520-5242-00 follows at 81-99."""
		self.assertEqual(set(range(1, 100)), set(self.lamps))
		profile = load_json(CONTROLLER_PATH)
		groups = {group["id"]: group for group in profile["groups"]}
		lamp_group = groups["pinmame.output.lamp"]
		self.assertEqual({"minimum": 1, "maximum": 336}, lamp_group["address_rules"][0])
		self.assertIn("64 + (lampCol * 8)", lamp_group["notes"])
		self.assertIn("coinGameData", lamp_group["notes"])
		self.assertIn("titanic", lamp_group["notes"])
		self.assertIn("monopred", lamp_group["notes"])
		self.assertNotIn("Lord of the Rings", lamp_group["notes"])
		self.assertNotIn("520-5242-00", lamp_group["notes"])
		profile_locator = profile["sources"][0]["locator"]
		self.assertIn("src/wpc/bowlgames.c", profile_locator)
		self.assertIn("coinGameData", profile_locator)
		definition_profile = next(source for source in self.definition["sources"]
		                          if source["id"] == "controller-profile.pinmame-whitestar")
		for token in ("src/wpc/bowlgames.c", "coinGameData", "titanic", "monopred"):
			self.assertIn(token, definition_profile["locator"])

	def test_cabinet_lamps_have_no_playfield_coordinate(self) -> None:
		for address in (79, 80):
			lamp = self.lamps[address]
			self.assertEqual("not_applicable", lamp["spatial"]["status"], address)
			self.assertEqual("cabinet_or_service", lamp["spatial"]["reason"], address)
		self.assertEqual("optional", self.lamps[79]["availability"])

	def test_back_panel_mode_lamps_are_placed_by_all_three_tables(self) -> None:
		"""All three recreations model lamps 73-78, VPW as p73-p78 primitives. No claim of
		independence is made here; the point is that none of the three is missing."""
		for address in BACK_PANEL_MODE_LAMPS:
			lamp = self.lamps[address]
			placements = lamp["spatial"]["placements"]
			self.assertEqual(1, len(placements), address)
			refs = {ref for ref in placements[0]["provenance"]["source_refs"] if ref.startswith("vpx-table.")}
			self.assertEqual(
				{"vpx-table.lotr-vpw-1-6", "vpx-table.lotr-jpsalas-600", "vpx-table.lotr-hanibal-4k"}, refs, address
			)

	def test_manual_typo_is_preserved_not_normalized(self) -> None:
		"""The manual prints LEGOLES for lamps 15 and 33; source anomalies are preserved as printed."""
		for address in (15, 33):
			self.assertIn("LEGOLES", self.lamps[address]["label"].upper(), address)

	def test_general_illumination_is_one_aggregate_channel(self) -> None:
		gi = bindings(self.definition, "outputs", "pinmame.output.gi")
		self.assertEqual({0}, set(gi))
		self.assertIn("four separately fused", gi[0]["physical"]["notes"])

	def test_display_inventory_is_the_backbox_dmd(self) -> None:
		displays = self.definition["displays"]
		self.assertEqual(1, len(displays))
		display = displays[0]
		self.assertEqual("dmd", display["kind"])
		self.assertEqual(128, display["width"])
		self.assertEqual(32, display["height"])
		self.assertEqual("not_applicable", display["spatial"]["status"])
		self.assertEqual("cabinet_or_service", display["spatial"]["reason"])

	def test_mechanism_inventory(self) -> None:
		mechanisms = {item["id"]: item for item in self.definition["mechanisms"]}
		self.assertEqual(
			{
				"mechanism.trough", "mechanism.balrog", "mechanism.sword-lock", "mechanism.ring-magnet",
				"mechanism.loop-diverter", "mechanism.up-kickers", "mechanism.mini-playfield",
				"mechanism.uk-up-down-posts",
			},
			set(mechanisms),
		)
		balrog = mechanisms["mechanism.balrog"]
		self.assertEqual({"open", "closed"}, {position["id"] for position in balrog["positions"]})
		self.assertIn("switch.matrix-28", balrog["sensors"])
		self.assertIn("wobble", balrog["behavior"])

	def test_trough_records_the_printed_numbering_direction(self) -> None:
		trough = next(item for item in self.definition["mechanisms"] if item["id"] == "mechanism.trough")
		self.assertIn("numbers the positions from the left", trough["behavior"])
		self.assertEqual(5, len(trough["positions"]))

	def test_every_device_has_availability_and_an_accounted_spatial_state(self) -> None:
		"""Every device either carries spatial evidence or is declared unresolved in the report."""
		report = load_json(SPATIAL_REPORT_PATH)
		unplaced = ({row["device"] for row in report["unplaced_devices"]}
		            | {row["device"] for row in report["conflicted_led_positions"]})
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				self.assertIn("availability", device, device["id"])
				if "spatial" not in device:
					self.assertIn(device["id"], unplaced, device["id"])

	def test_every_source_ref_resolves(self) -> None:
		known = {source["id"] for source in self.definition["sources"]}
		def walk(node) -> None:
			if isinstance(node, dict):
				if "source_refs" in node:
					for ref in node["source_refs"]:
						self.assertIn(ref, known)
				for value in node.values():
					walk(value)
			elif isinstance(node, list):
				for value in node:
					walk(value)
		walk(self.definition)

	def test_placement_ids_are_unique_and_in_range(self) -> None:
		seen: set[str] = set()
		for collection in ("inputs", "outputs"):
			for device in self.definition[collection]:
				for place in device.get("spatial", {}).get("placements", []):
					self.assertNotIn(place["id"], seen)
					seen.add(place["id"])
					self.assertEqual("playfield", place["space"])
					self.assertGreaterEqual(place["x"], 0.0)
					self.assertLessEqual(place["x"], 1.0)
					self.assertGreaterEqual(place["y"], 0.0)
					self.assertLessEqual(place["y"], 1.0)

	def test_spatial_report_matches_the_definition(self) -> None:
		report = load_json(SPATIAL_REPORT_PATH)
		self.assertEqual("pinmame-spatial-blockers", report["format"])
		self.assertEqual("stern.lord-of-the-rings.2003", report["machine_id"])
		placements = sum(
			len(device.get("spatial", {}).get("placements", []))
			for collection in ("inputs", "outputs")
			for device in self.definition[collection]
		)
		self.assertEqual(placements, report["placement_count"])
		located_devices = sum(
			bool(device.get("spatial", {}).get("placements"))
			for collection in ("inputs", "outputs")
			for device in self.definition[collection]
		)
		self.assertEqual(
			located_devices,
			report["counts"]["validated_devices"] + report["counts"]["observed_devices"],
		)

	def test_spatial_report_records_the_rejected_outliers(self) -> None:
		"""One retained table lays the Fellowship inserts out as a closed ring rather than the printed
		arc, being an original-artwork edition; those rejections must stay visible."""
		report = load_json(SPATIAL_REPORT_PATH)
		rejected = {(item["kind"], item["address"]) for item in report["rejected_measurements"]}
		for address in range(9, 18):
			self.assertIn(("lamp", address), rejected)

	def test_multi_emitter_flasher_is_resolved_per_emitter_from_every_script(self) -> None:
		import curate_lord_of_the_rings as curator

		report = load_json(SPATIAL_REPORT_PATH)
		rejected = {(item["kind"], item["address"]) for item in report["rejected_measurements"]}
		self.assertNotIn(("flasher", 25), rejected)
		self.assertNotIn("multi_emitter_measurement_exclusions", report)
		entry = curator.consensus["devices"]["flasher"]["25"]
		self.assertEqual("validated", entry["status"])
		self.assertEqual(3, entry["quantity"])
		expected_objects = {
			"left": {"Flasherbase1", "f25a001", "f25c001", "f25b", "f25e"},
			"right": {"Flasherbase3", "f25a002", "f25c002", "F25a", "f25f"},
			"bottom": {"Flasherbase2", "f25a3", "f25c", "f25d"},
		}
		for side, emitter in entry["emitters"].items():
			self.assertEqual("validated", emitter["status"], side)
			self.assertEqual(
				{"vpw-1-6", "jpsalas-600", "hanibal-4k"},
				{measurement["table"] for measurement in emitter["measurements"]},
			)
			bound = {name for measurement in emitter["measurements"] for name in measurement["bound_objects"]}
			self.assertEqual(expected_objects[side], bound, side)
			self.assertTrue(all(measurement["script_lines"] for measurement in emitter["measurements"]))

	def test_knowledge_note_is_promoted_and_has_no_stale_partial_banner(self) -> None:
		text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
		self.assertIn("partial", text.splitlines()[2])
		self.assertNotIn("requiring validation", text)
		self.assertNotIn("has not yet been normalized", text)


def _vpx_root() -> Path | None:
    override = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if override:
        return Path(override) / "stern" / "lord-of-the-rings-2003"
    for parent in ROOT.resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
        if candidate.is_dir():
            return candidate / "stern" / "lord-of-the-rings-2003"
    return None


def _manuals_root() -> Path | None:
    override = os.environ.get("PINMAME_MANUALS_ROOT")
    if override:
        return Path(override) / "by-machine" / "stern.lord-of-the-rings.2003"
    for parent in ROOT.resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "manuals" / "by-machine"
        if candidate.is_dir():
            return candidate / "stern.lord-of-the-rings.2003"
    return None


_EXTERNAL_ROOTS = {
	"pinmame-vpx-sources": ("PINMAME_VPX_SOURCES_ROOT", "vpx-sources"),
	"pinmame-manuals": ("PINMAME_MANUALS_ROOT", "manuals"),
	"pinmame-review-artifacts": ("PINMAME_REVIEW_ARTIFACTS_ROOT", "review-artifacts"),
}


def _resolve_external(uri: str) -> Path | None:
	"""Turn an `external:<root>/<tail>` locator into the path it names.

	Returns None only when that evidence root is genuinely unavailable, so a caller can skip
	on a missing root while still failing on a locator that points at nothing.
	"""
	root_name, _, tail = uri[len("external:"):].partition("/")
	if root_name not in _EXTERNAL_ROOTS:
		raise AssertionError(f"unknown external root in locator: {uri}")
	variable, folder = _EXTERNAL_ROOTS[root_name]
	override = os.environ.get(variable)
	if override:
		base = Path(override)
	else:
		base = None
		for parent in ROOT.resolve().parents:
			candidate = parent / "pinmame-game-defs-working-dir" / folder
			if candidate.is_dir():
				base = candidate
				break
	if base is None or not base.is_dir():
		return None
	return base / unquote(tail)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class LordOfTheRingsRetainedEvidenceTests(unittest.TestCase):
    """Prove the recorded hashes describe the artifacts actually retained.

    These skip cleanly when the external evidence roots are absent, so the no-evidence run
    stays green without silently weakening the canonical checks.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.definition = load_json(DEFINITION_PATH)
        cls.sources = {source["id"]: source for source in cls.definition["sources"]}

    def test_every_external_locator_names_a_file_that_is_there(self) -> None:
        """A locator nobody reads is a locator nobody checks.

        Round six shipped four `uri` values that dropped the `alt-<table>/` path segment while
        carrying the correct SHA-256 of the file at the real path. Every gate stayed green
        because no gate read `uri` at all: the hash tests below carried their own hard-coded,
        and correct, path list. They now resolve through the locator, so a wrong locator can
        no longer hide behind a right hash.
        """
        checked = 0
        for source in self.definition["sources"]:
            uri = source.get("uri", "")
            if not uri.startswith("external:"):
                continue
            path = _resolve_external(uri)
            if path is None:
                self.skipTest(f"the evidence root named by {uri} is not available")
            self.assertTrue(path.is_file(), f"{source['id']} locator resolves to nothing: {uri} -> {path}")
            checked += 1
        self.assertEqual(14, checked, "every retained artifact must carry an external locator")

    def test_retained_tables_and_scripts_match_their_recorded_hashes(self) -> None:
        expected = {
            "vpx-table.lotr-vpw-1-6", "vpx-script.lotr-vpw-1-6",
            "vpx-table.lotr-jpsalas-600", "vpx-script.lotr-jpsalas-600",
            "vpx-table.lotr-hanibal-4k", "vpx-script.lotr-hanibal-4k",
			"vpx-table.lotr-neo-led-mod-1-0-3",
        }
        self.assertEqual(expected, {
            source["id"] for source in self.definition["sources"]
            if source["kind"] in ("vpx_table", "vpx_script") and not source["id"].startswith("vpx-extraction.")
        })
        for source_id in sorted(expected):
            path = _resolve_external(self.sources[source_id]["uri"])
            if path is None:
                self.skipTest("retained VPX sources are not available")
            self.assertTrue(path.is_file(), f"{source_id} locator resolves to nothing: {path}")
            self.assertEqual(self.sources[source_id]["sha256"], file_sha256(path), source_id)

    def test_retained_manual_and_transcription_match_their_recorded_hashes(self) -> None:
        for source_id in (
            "manual.stern.lord-of-the-rings.2003",
            "manual-support.stern.lord-of-the-rings.2003",
        ):
            path = _resolve_external(self.sources[source_id]["uri"])
            if path is None:
                self.skipTest("retained manuals are not available")
            self.assertTrue(path.is_file(), f"{source_id} locator resolves to nothing: {path}")
            self.assertEqual(self.sources[source_id]["sha256"], file_sha256(path), source_id)
        manual = self.sources["manual.stern.lord-of-the-rings.2003"]
        transcription_path = _resolve_external(self.sources["manual-support.stern.lord-of-the-rings.2003"]["uri"])
        transcription = json.loads(transcription_path.read_text(encoding="utf-8"))
        self.assertEqual(manual["sha256"], transcription["source"]["sha256"])
        self.assertEqual(manual["original_filename"], transcription["source"]["document"])

    def test_committed_manual_excerpts_match_their_recorded_digests(self) -> None:
        manual = self.sources["manual.stern.lord-of-the-rings.2003"]
        self.assertEqual(4, len(manual["excerpts"]))
        for excerpt in manual["excerpts"]:
            path = ROOT / excerpt["path"]
            self.assertTrue(path.is_file(), excerpt["path"])
            self.assertEqual(excerpt["sha256"], file_sha256(path), excerpt["id"])
            self.assertTrue(excerpt["reviewed"], excerpt["id"])
            if "image" in excerpt:
                image = ROOT / excerpt["image"]
                self.assertTrue(image.is_file(), excerpt["image"])
                self.assertEqual(excerpt["image_sha256"], file_sha256(image), excerpt["id"])
        locations = (ROOT / "evidence/excerpts/stern.lord-of-the-rings.2003/coil-flash-lamp-locations.md").read_text(encoding="utf-8")
        self.assertIn("flashers 14 and 23 yellow", locations)
        self.assertIn("all three flasher-25 bulbs and flasher 29 red", locations)

    def test_spatial_consensus_matches_its_recorded_hash(self) -> None:
        import curate_lord_of_the_rings as curator

        root = _vpx_root()
        if root is None or not (root / "derived" / "spatial-consensus.json").is_file():
            self.skipTest("retained spatial consensus is not available")
        recorded = self.sources["spatial-consensus.stern.lord-of-the-rings.2003"]["sha256"]
        self.assertEqual(recorded, file_sha256(root / "derived" / "spatial-consensus.json"))
        self.assertEqual(curator.consensus, load_json(root / "derived" / "spatial-consensus.json"))

    def test_spatial_consensus_recomputes_from_the_retained_extractions(self) -> None:
        import tempfile

        root = _vpx_root()
        if root is None or not root.is_dir():
            self.skipTest("retained extractions are not available")
        with tempfile.TemporaryDirectory() as scratch:
            regenerated = Path(scratch) / "spatial-consensus.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "tools" / "lotr_spatial_resolve.py"),
                    "--write",
                    str(regenerated),
                ],
                capture_output=True,
                text=True,
                cwd=str(ROOT),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual((root / "derived" / "spatial-consensus.json").read_bytes(), regenerated.read_bytes())

    def test_extraction_manifests_recompute(self) -> None:
        root = _vpx_root()
        if root is None or not root.is_dir():
            self.skipTest("retained extractions are not available")
        script = ROOT / "tools" / "lotr_extraction_manifest.py"
        result = subprocess.run(
            [sys.executable, "-B", str(script), "--verify"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        # Two distinct digests. `sources[].sha256` hashes the manifest FILE, uniformly with every
        # other source; the extraction-TREE digest lives in that file's own `manifest_sha256`
        # field and is what the tool recomputes. They used to be conflated, so `sha256` meant one
        # thing for three records and another for the rest, and a consumer hashing the named file
        # got a mismatch.
        for source_id in (
            "vpx-extraction.lotr-vpw-1-6", "vpx-extraction.lotr-jpsalas-600",
            "vpx-extraction.lotr-hanibal-4k", "vpx-extraction.lotr-neo-led-mod-1-0-3",
        ):
            path = _resolve_external(self.sources[source_id]["uri"])
            self.assertTrue(path.is_file(), f"{source_id} locator resolves to nothing: {path}")
            self.assertIn(json.loads(path.read_text(encoding="utf-8"))["manifest_sha256"], result.stdout, source_id)

    def test_every_driver_note_names_every_rom_that_differs(self) -> None:
        """The ROM-composition rule, checked as data rather than trusted to the builder's guard.

        Round six asserted "only the CPU game ROM differs" for all 45 clones. Round seven fixed
        the eight Spanish drivers and left the other 36 wrong. Round eight derived the prose and
        added a builder-side guard - and then exempted the Spanish drivers from it, i.e. exempted
        the one class the guard existed for; a cross-provider review made lotr_sp9 claim "No
        driver ROM changes" and generation still succeeded.

        This checks the invariant in the repository, against the ROM inventory embedded in the
        curator, so it holds whether or not the builder's guard is present or correct.
        """
        tree = ast.parse((ROOT / "tools" / "curate_lord_of_the_rings.py").read_text(encoding="utf-8"))
        rom_sets = None
        for node in tree.body:
            if (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "ROM_SETS" and isinstance(node.value, ast.Call)
                    and node.value.args and isinstance(node.value.args[0], ast.Constant)):
                rom_sets = json.loads(node.value.args[0].value)
        self.assertIsNotNone(rom_sets, "the curator must embed the parsed ROM inventory")
        notes = {driver["id"]: driver["variant_notes"] for driver in self.definition["drivers"]}
        self.assertEqual(set(notes), set(rom_sets), "every driver must have a parsed ROM set")
        root_cpu, root_display, root_sound = rom_sets["lotr"]
        for driver_id, (cpu, display, sound) in sorted(rom_sets.items()):
            if driver_id == "lotr":
                continue
            note = notes[driver_id]
            for rom, same, label in ((cpu, cpu == root_cpu, "CPU"),
                                     (display, display == root_display, "display"),
                                     (sound, sound == root_sound, "sound")):
                if not same:
                    self.assertIn(rom, note, f"{driver_id}: {label} ROM {rom} differs but the note omits it")

    def test_every_external_source_sha256_hashes_the_file_it_names(self) -> None:
        """One field, one meaning, across the whole `sources` array."""
        checked = 0
        for source in self.definition["sources"]:
            uri = source.get("uri", "")
            if not uri.startswith("external:"):
                continue
            path = _resolve_external(uri)
            if path is None:
                self.skipTest(f"the evidence root named by {uri} is not available")
            self.assertTrue(path.is_file(), f"{source['id']} locator resolves to nothing: {path}")
            self.assertEqual(source["sha256"], file_sha256(path), source["id"])
            checked += 1
        self.assertEqual(14, checked)


class LordOfTheRingsCuratorTests(unittest.TestCase):
	def test_seed_is_byte_identical_to_the_promoted_definition(self) -> None:
		self.assertEqual(SEED_PATH.read_bytes(), DEFINITION_PATH.read_bytes())

	def test_curator_check_is_idempotent(self) -> None:
		import curate_lord_of_the_rings as curator

		curator._check(ROOT)
		curator._check(ROOT)

	def test_curator_check_rejects_edited_artifacts(self) -> None:
		"""Every artifact the curator owns is byte-compared, including the canonical definition.

		Comparing canonical JSON would accept a reformatted definition; comparing a pinned digest
		would accept hand-written prose. Both were real gaps, so both directions are tested here
		against a throwaway copy of the tree rather than the working tree itself.
		"""
		import shutil
		import tempfile

		import curate_lord_of_the_rings as curator

		owned = [path.relative_to(ROOT) for path, _ in curator._artifacts()]
		self.assertGreaterEqual(len(owned), 4)
		with tempfile.TemporaryDirectory() as scratch:
			root = Path(scratch)
			for relative in set(owned):
				target = root / relative
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(ROOT / relative, target)
			curator._check(root)
			for relative in set(owned):
				target = root / relative
				original = target.read_bytes()
				target.write_bytes(original + b"\n")
				with self.assertRaises(RuntimeError, msg=f"editing {relative} was not detected"):
					curator._check(root)
				target.write_bytes(original)
			curator._check(root)

	def test_curator_check_survives_a_crlf_checkout_but_still_refuses_a_reformat(self) -> None:
		"""The gate forgives line endings, and nothing else.

		Git's Windows default `core.autocrlf=true` rewrites every LF in the working tree to CRLF,
		so a clone nobody had touched failed `--check` for a reason that has nothing to do with
		curation. Pinning the paths in a `.gitattributes` would have fixed that by changing
		repository-wide policy for one contribution's benefit; folding CRLF to LF inside the
		comparison fixes it where the problem actually is.

		Both halves are asserted here, because a normalisation loose enough to also forgive
		reformatting would quietly undo the byte-exactness this gate exists for - which is the
		gap that put the byte comparison here in the first place.
		"""
		import shutil
		import tempfile

		import curate_lord_of_the_rings as curator

		owned = {path.relative_to(ROOT) for path, _ in curator._artifacts()}
		with tempfile.TemporaryDirectory() as scratch:
			root = Path(scratch)
			for relative in owned:
				target = root / relative
				target.parent.mkdir(parents=True, exist_ok=True)
				shutil.copy2(ROOT / relative, target)
				# Exactly what a fresh `core.autocrlf=true` clone puts on disk.
				target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
			curator._check(root)
			definition = root / DEFINITION_PATH.relative_to(ROOT)
			same_data_other_bytes = (json.dumps(load_json(definition), indent=4, sort_keys=True) + "\n").encode("utf-8")
			definition.write_bytes(same_data_other_bytes)
			with self.assertRaises(RuntimeError, msg="a reformatted definition must still be refused"):
				curator._check(root)

	def test_curator_requires_an_explicit_mode(self) -> None:
		import curate_lord_of_the_rings as curator

		argv = sys.argv
		sys.argv = ["curate_lord_of_the_rings.py"]
		try:
			with self.assertRaises(SystemExit):
				curator.main()
		finally:
			sys.argv = argv

	def test_curator_exports_the_pinned_manual_transcription(self) -> None:
		import tempfile

		import curate_lord_of_the_rings as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		with tempfile.TemporaryDirectory() as scratch:
			path = Path(scratch) / "nested" / "transcription.json"
			argv = sys.argv
			sys.argv = ["curate_lord_of_the_rings.py", "--export-transcription", str(path)]
			try:
				curator.main()
			finally:
				sys.argv = argv
			self.assertEqual(canonical_bytes(curator.transcription), path.read_bytes())
			support = next(source for source in curator.SOURCES if source["id"] == curator.SUPPORT)
			self.assertEqual(support["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

	def test_curator_rebuilds_the_definition_byte_for_byte(self) -> None:
		import curate_lord_of_the_rings as curator
		from pinmame_game_defs.jsonio import canonical_bytes

		self.assertEqual(canonical_bytes(load_json(DEFINITION_PATH)), canonical_bytes(curator.build()))


if __name__ == "__main__":
	unittest.main()
