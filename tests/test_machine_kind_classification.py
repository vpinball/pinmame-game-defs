from __future__ import annotations

import re
import unittest
from pathlib import Path

from pinmame_game_defs.coverage import build_coverage_report
from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
# Driver-description patterns that identify non-game records. The classification
# must be derivable from the pinned catalog, not a hand-listed path set.
DIAGNOSTIC_PATTERN = re.compile(r"test fixture|test chip|test rom|board tester|boot flash", re.IGNORECASE)
REDEMPTION_PATTERN = re.compile(r"redemption", re.IGNORECASE)


class MachineKindClassificationTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.catalog = load_json(ROOT / "catalog" / "pinmame.json")
		cls.driver_by_id = {record["id"]: record for record in cls.catalog["drivers"]}

	def test_every_test_fixture_driver_is_diagnostic_software(self) -> None:
		for machine in self.catalog["machines"]:
			definition = load_json(ROOT / machine["definition"])
			descriptions = [self.driver_by_id[driver_id]["description"] for driver_id in machine["root_drivers"]]
			if any(DIAGNOSTIC_PATTERN.search(description) for description in descriptions):
				self.assertEqual(
					"diagnostic_software",
					definition["machine"].get("kind"),
					(machine["id"], descriptions),
				)

	def test_redemption_drivers_are_classified_as_redemption_games(self) -> None:
		for machine in self.catalog["machines"]:
			definition = load_json(ROOT / machine["definition"])
			descriptions = [self.driver_by_id[driver_id]["description"] for driver_id in machine["root_drivers"]]
			if any(REDEMPTION_PATTERN.search(description) for description in descriptions):
				self.assertEqual(
					"redemption_game",
					definition["machine"].get("kind"),
					(machine["id"], descriptions),
				)

	def test_bingo_pinballs_are_physical_pinball(self) -> None:
		for machine in self.catalog["machines"]:
			if "bingo" not in machine["id"]:
				continue
			definition = load_json(ROOT / machine["definition"])
			self.assertEqual("physical_pinball", definition["machine"].get("kind"), machine["id"])

	def test_non_game_kinds_are_excluded_from_physical_coverage(self) -> None:
		report = build_coverage_report(ROOT)
		self.assertEqual(self.catalog["summary"]["game_count"], report["machine_count"])
		self.assertEqual(13, report["non_game_record_count"])
		self.assertEqual(13, sum(1 for machine in self.catalog["machines"] if machine["machine_kind"] == "diagnostic_software"))
		self.assertEqual(777, report["machine_count"])


if __name__ == "__main__":
	unittest.main()
