from __future__ import annotations

import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]


class MachineKindClassificationTests(unittest.TestCase):
	def test_test_fixtures_are_diagnostic_software(self) -> None:
		for relative in (
			"machines/partial/bally/wpc-test-fixture-dmd-l-3-1991.json",
			"machines/partial/bally/wpc-test-fixture-security-1-2-1994.json",
			"machines/partial/bally/wpc-test-fixture-wpc-95-1-2-1996.json",
			"machines/partial/bally/wpc-test-fixture-alphanumeric-l-3-1990.json",
			"machines/partial/gottlieb/system-80-test-fixture-1981.json",
			"machines/partial/gottlieb/system-80b-test-fixture-unknown.json",
			"machines/partial/gottlieb/system-1-t-test-fixture-unknown.json",
			"machines/partial/taito/taito-test-fixture-unknown.json",
			"machines/partial/data-east/data-east-test-chip-1998.json",
			"machines/partial/leon/data-east-leon-test-chip-version-4-unknown.json",
		):
			definition = load_json(ROOT / relative)
			self.assertEqual("diagnostic_software", definition["machine"].get("kind"), relative)

	def test_bingo_pinballs_and_the_gun_game_are_classified(self) -> None:
		bingo = load_json(ROOT / "machines/partial/sirmo-belgium/domino-ii-bingo-unknown.json")
		self.assertEqual("physical_pinball", bingo["machine"].get("kind"))
		gun_game = load_json(ROOT / "machines/partial/bally-midway/midnight-marauders-gun-game-1984.json")
		self.assertEqual("redemption_game", gun_game["machine"].get("kind"))

	def test_non_game_kinds_are_excluded_from_physical_coverage(self) -> None:
		from pinmame_game_defs.coverage import build_coverage_report

		report = build_coverage_report(ROOT)
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		self.assertEqual(catalog["summary"]["game_count"], report["machine_count"])
		self.assertEqual(11, report["non_game_record_count"])
		# The retained diagnostic plus the ten test-fixture/test-chip records this
		# classification covers.
		self.assertEqual(11, sum(1 for machine in catalog["machines"] if machine["machine_kind"] == "diagnostic_software"))


if __name__ == "__main__":
	unittest.main()
