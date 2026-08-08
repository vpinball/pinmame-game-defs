"""Regression tests for the Bally Judge Dredd definition and the wpc-dcs profile it reuses.

Two regressions this file guards specifically:

* Judge Dredd is a **wide-body** table. Its retained playfield is 1093 units across, not the 952
  that standard-body WPC games use, and every normalized x here was divided by 1093. Indiana Jones
  established that using the standard divisor on a wide-body silently stretches every x coordinate
  by roughly 15%, which no schema check would catch because the results stay in range.
* This generation has **no LPDC board**, so public 37-44 is dead address space rather than the
  WPC-95 37-40/41-44 mirror pair. pinned core_getSol returns a constant 0 across that whole range
  here, so a reader importing the WPC-95 rule would invent eight outputs and a duplicate
  relationship between them, none of which exists on this machine.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

DEFINITION_PATH = ROOT / "machines" / "partial" / "bally" / "judge-dredd-1993.json"
SEED_PATH = ROOT / "tools" / "seeds" / "bally" / "judge-dredd-1993.json"
PROFILE_PATH = ROOT / "controllers" / "pinmame" / "wpc-dcs.json"
KNOWLEDGE_PATH = ROOT / "knowledge" / "bally" / "judge-dredd-1993.md"
SPATIAL_REPORT_PATH = ROOT / "reports" / "spatial" / "bally" / "judge-dredd-1993.json"


def load_json(path: Path) -> dict:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class JudgeDreddDefinitionTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.definition = load_json(DEFINITION_PATH)
		cls.switches = {
			int(d["binding"]["device"]) for d in cls.definition["inputs"]
			if d["binding"]["group"] == "pinmame.input.switch"
		}
		cls.solenoids = {
			int(d["binding"]["device"]) for d in cls.definition["outputs"]
			if d["binding"]["group"] == "pinmame.output.solenoid"
		}
		cls.gi = {
			int(d["binding"]["device"]) for d in cls.definition["outputs"]
			if d["binding"]["group"] == "pinmame.output.gi"
		}

	def test_identity_and_controller_platform(self) -> None:
		machine = self.definition["machine"]
		self.assertEqual("bally.judge-dredd.1993", machine["id"])
		self.assertEqual("Bally", machine["manufacturer"])
		self.assertEqual(1993, machine["year"])
		self.assertEqual("pinmame.wpc-dcs", self.definition["controller"]["platform"])
		self.assertEqual("0x10", self.definition["controller"]["hardware_generation"])
		self.assertTrue(self.definition["controller"]["inversion_applied_by_emulator"])

	def test_playfield_is_wide_body_and_matches_the_normalization_divisors(self) -> None:
		"""1093 wide, not 952. Every normalized x depends on this."""
		playfield = self.definition["machine"]["playfield"]
		self.assertEqual("vpx", playfield["units"])
		self.assertAlmostEqual(1093.0, playfield["width"], places=3)
		self.assertAlmostEqual(2162.0, playfield["height"], places=3)

	def test_driver_family_is_the_twelve_jd_drivers(self) -> None:
		self.assertEqual(
			{"jd_l1", "jd_d1", "jd_l1at", "jd_l1d", "jd_l4", "jd_d4",
			 "jd_l5", "jd_d5", "jd_l6", "jd_d6", "jd_l7", "jd_d7"},
			{driver["id"] for driver in self.definition["drivers"]},
		)

	# -------------------------------------------------------------- switches --

	def test_matrix_uses_column_times_ten_notation_with_eight_full_columns(self) -> None:
		expected = {column * 10 + row for column in range(1, 9) for row in range(1, 9)}
		self.assertTrue(expected <= self.switches, "a standard matrix position is missing")

	def test_no_switch_sits_on_a_row_zero_or_row_nine(self) -> None:
		"""Column-times-ten notation has no row 0 and no row 9; those would be decode errors."""
		for address in self.switches:
			if address >= 11:
				self.assertIn(address % 10, range(1, 9), f"switch {address} has an illegal row digit")

	def test_fliptronic_column_is_present_at_111_to_118(self) -> None:
		self.assertEqual(set(range(111, 119)), {a for a in self.switches if a >= 111})

	def test_dedicated_switches_occupy_1_to_8(self) -> None:
		self.assertEqual(set(range(1, 9)), {a for a in self.switches if a <= 8})

	# ------------------------------------------------------------- solenoids --

	def test_solenoid_range_is_contiguous_1_to_51(self) -> None:
		self.assertEqual(set(range(1, 52)), self.solenoids)

	def test_thirty_seven_to_forty_four_are_unused_space_not_an_lpdc_mirror_pair(self) -> None:
		"""WPC-DCS has no LPDC board, so 37-44 is dead address space -- not a duplicate pair.

		pinned core_getSol serves the 37-40/41-44 branch only for GEN_WPC95, GEN_WPC95DCS and
		GEN_ALLS11, returning a constant 0 here. The regression guarded is a reader importing the
		WPC-95 rule and treating 41-44 as mirrors of 37-40: on this generation neither half drives
		anything, and no device in this range may carry a playfield placement.
		"""
		by_address = {
			int(d["binding"]["device"]): d for d in self.definition["outputs"]
			if d["binding"]["group"] == "pinmame.output.solenoid"
		}
		for address in range(37, 45):
			device = by_address[address]
			self.assertEqual("unused", device["availability"], f"solenoid {address}")
			spatial = device.get("spatial") or {}
			self.assertEqual("not_applicable", spatial.get("status"), f"solenoid {address}")
			self.assertEqual("virtual", spatial.get("reason"), f"solenoid {address}")
			self.assertNotIn("placements", spatial, f"solenoid {address} must have no placement")
			self.assertIn(
				"no LPDC board", (device.get("physical") or {}).get("notes", ""),
				f"solenoid {address} must say why it is dead space",
			)

	def test_virtual_solenoid_availability_tracks_runtime_state_not_physical_fitment(self) -> None:
		by_address = {
			int(d["binding"]["device"]): d for d in self.definition["outputs"]
			if d["binding"]["group"] == "pinmame.output.solenoid" and d["kind"] == "virtual"
		}
		self.assertEqual({29, 30, 31, 51}, {address for address, device in by_address.items() if device["availability"] == "used"})
		self.assertEqual({12, 14, 32, *range(37, 45), 49, 50}, {address for address, device in by_address.items() if device["availability"] == "unused"})
		for address in (29, 30, 31):
			self.assertEqual(["internal.wpc-state"], by_address[address]["roles"], address)

	def test_five_general_illumination_addresses(self) -> None:
		self.assertEqual({0, 1, 2, 3, 4}, self.gi)

	# ------------------------------------------------------------- conflicts --

	def test_all_four_conflicts_are_present_and_the_record_stays_partial(self) -> None:
		self.assertEqual(
			{
				"conflict.column-6-7-optos-not-all-normalized",
				"conflict.judge-drop-targets-normalized-without-opto-evidence",
				"conflict.l1-era-switch-fitment",
				"conflict.gi-string-order-script-vs-manual",
			},
			{conflict["id"] for conflict in self.definition["conflicts"]},
		)
		self.assertEqual("partial", self.definition["coverage"]["status"])
		self.assertEqual(
			["polarity", "spatial_placement", "unresolved_conflicts"],
			self.definition["coverage"]["missing"],
		)


class JudgeDreddSpatialTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		definition = load_json(DEFINITION_PATH)
		cls.points = {}
		for group in ("inputs", "outputs"):
			for device in definition[group]:
				placements = (device.get("spatial") or {}).get("placements") or []
				if placements:
					cls.points[device["id"]] = (placements[0]["x"], placements[0]["y"])

	def test_every_placement_is_in_range_with_at_most_six_decimals(self) -> None:
		self.assertTrue(self.points, "no placements were found at all")
		for device_id, (x, y) in self.points.items():
			self.assertGreaterEqual(x, 0.0, device_id)
			self.assertLessEqual(x, 1.0, device_id)
			self.assertGreaterEqual(y, 0.0, device_id)
			self.assertLessEqual(y, 1.0, device_id)
			for axis, value in (("x", x), ("y", y)):
				self.assertEqual(round(value, 6), value, f"{device_id} {axis} has too many decimals")

	def test_placement_ids_are_unique(self) -> None:
		definition = load_json(DEFINITION_PATH)
		seen = set()
		for group in ("inputs", "outputs"):
			for device in definition[group]:
				for placement in (device.get("spatial") or {}).get("placements") or []:
					self.assertNotIn(placement["id"], seen, f"duplicate placement id {placement['id']}")
					seen.add(placement["id"])

	def test_left_named_devices_sit_left_of_their_right_named_partner(self) -> None:
		"""The cheap ordering check the Centaur post-mortem asked for.

		Pairs are discovered rather than hard-coded so that this keeps working as the definition
		grows: any two devices whose ids differ only by a left/right token must be sided correctly.
		A wide-body divisor mistake would not trip this, but a transposition would, and both
		Cactus Canyon and Ripley's shipped transpositions that it catches.
		"""
		checked = 0
		for device_id, (x, _) in self.points.items():
			if "left" not in device_id:
				continue
			partner = device_id.replace("left", "right")
			if partner not in self.points:
				continue
			# skip pairs where "left"/"right" names a ball path rather than a playfield side
			self.assertLess(x, self.points[partner][0], f"{device_id} must sit left of {partner}")
			checked += 1
		self.assertGreater(checked, 0, "no left/right pairs were compared")


class WpcDcsProfileTests(unittest.TestCase):
	def test_profile_is_unmodified_by_this_game(self) -> None:
		profile = load_json(PROFILE_PATH)
		self.assertEqual("pinmame.wpc-dcs", profile["id"])
		self.assertTrue(profile["inversion_applied_by_emulator"])


class JudgeDreddArtifactTests(unittest.TestCase):
	def test_seed_and_definition_are_byte_identical(self) -> None:
		self.assertEqual(DEFINITION_PATH.read_bytes(), SEED_PATH.read_bytes())

	def test_knowledge_note_exists_and_is_declared_complete(self) -> None:
		definition = load_json(DEFINITION_PATH)
		self.assertEqual("knowledge/bally/judge-dredd-1993.md", definition["knowledge"]["path"])
		self.assertEqual("complete", definition["knowledge"]["status"])
		self.assertTrue(KNOWLEDGE_PATH.is_file())

	def test_spatial_report_is_for_this_machine(self) -> None:
		self.assertEqual("bally.judge-dredd.1993", load_json(SPATIAL_REPORT_PATH)["machine_id"])


if __name__ == "__main__":
	unittest.main()
