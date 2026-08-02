from __future__ import annotations

import json
import unittest
from pathlib import Path

from pinmame_game_defs.coverage import build_coverage_report, build_curation_queue


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class MachineClassificationTests(unittest.TestCase):
	def test_scotts_test_rom_is_explicitly_non_game(self) -> None:
		path = REPOSITORY_ROOT / "machines/partial/diagnostic/scotts-test-rom-v8.json"
		definition = json.loads(path.read_text(encoding="utf-8"))
		self.assertEqual("diagnostic_software", definition["machine"]["kind"])
		self.assertEqual(["scotest8"], [driver["id"] for driver in definition["drivers"]])

	def test_non_games_are_retained_but_excluded_from_game_coverage(self) -> None:
		catalog = json.loads((REPOSITORY_ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
		report = build_coverage_report(REPOSITORY_ROOT)
		self.assertEqual(len(catalog["machines"]), report["catalog_record_count"])
		self.assertEqual(catalog["summary"]["non_game_count"], report["non_game_record_count"])
		self.assertEqual(catalog["summary"]["game_count"], report["machine_count"])
		self.assertEqual(1, report["non_game_record_count"])

	def test_diagnostic_is_not_in_game_curation_queue(self) -> None:
		queue = build_curation_queue(REPOSITORY_ROOT)
		self.assertNotIn("diagnostic.scotts-test-rom-v8", {entry["machine_id"] for entry in queue["entries"]})


if __name__ == "__main__":
	unittest.main()
