from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.coverage import build_coverage_report, build_curation_queue
from pinmame_game_defs.scope import OUT_OF_SCOPE_DRIVER_IDS, is_in_scope_driver
from pinmame_game_defs.vpx_source import extract_vpx_corpora


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
		self.assertEqual(list(range(1, len(queue["entries"]) + 1)), [entry["order"] for entry in queue["entries"]])
		self.assertTrue(all(0 <= entry["completion_score"] <= 100 for entry in queue["entries"]))

	def test_catalog_contains_only_physical_machine_scope(self) -> None:
		self.assertEqual({"acd_170_ac", "beachbms", "beav_butt", "bubba", "che_cho", "rambo", "tomjerry"}, OUT_OF_SCOPE_DRIVER_IDS)
		catalog = json.loads((REPOSITORY_ROOT / "catalog/pinmame.json").read_text(encoding="utf-8"))
		self.assertTrue(all(machine.get("machine_kind") != "virtual_pinball" for machine in catalog["machines"]))
		self.assertFalse(OUT_OF_SCOPE_DRIVER_IDS & {driver["id"] for driver in catalog["drivers"]})
		self.assertTrue(all(is_in_scope_driver(driver["id"]) for driver in catalog["drivers"]))

	def test_virtual_only_artifacts_are_absent(self) -> None:
		for relative_path in (
			"machines/author-ready/virtual/american-country-2024.json",
			"machines/author-ready/watacaractr/cheech-chong-road-trippin-2021.json",
			"knowledge/virtual/american-country-2024.md",
			"knowledge/watacaractr/cheech-chong-road-trippin-2021.md",
			"evidence/runtime/wpc/che-cho-gameplay.json",
			"evidence/vpx/vpxtable-scripts/che_cho/1893c13b913b9879.json",
			"evidence/vpx/vpxtable-scripts/beachbms/382b2f1d4b199b79.json",
			"evidence/vpx/vpxtable-scripts/beav_butt/d5672f8734a204d1.json",
			"evidence/vpx/vpx-standalone-scripts/beav_butt/793f82c0a81cd645.json",
			"evidence/vpx/vpxtable-scripts/bubba/c2ed40c7968006a6.json",
			"evidence/vpx/vpxtable-scripts/tomjerry/51b67b85a63f4a7e.json",
			"evidence/vpx/vpxtable-scripts/tomjerry/98e84d31b1e901b4.json",
			"tools/curate_che_cho.py",
		):
			self.assertFalse((REPOSITORY_ROOT / relative_path).exists(), relative_path)

	def test_evidence_does_not_reference_excluded_drivers(self) -> None:
		for path in (REPOSITORY_ROOT / "evidence").glob("**/*.json"):
			evidence = json.loads(path.read_text(encoding="utf-8"))
			self.assertFalse(OUT_OF_SCOPE_DRIVER_IDS & set(evidence.get("driver_ids", [])), path)

	def test_vpx_extraction_skips_virtual_only_scripts(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			repository = root / "repository"
			corpus = root / "corpus"
			(repository / "catalog").mkdir(parents=True)
			corpus.mkdir()
			(repository / "catalog/pinmame.json").write_text(json.dumps({"drivers": [], "machines": []}), encoding="utf-8")
			(corpus / "virtual.vbs").write_text('Const cGameName = "Che_Cho"\n', encoding="utf-8")
			with patch("pinmame_game_defs.vpx_source._revision", return_value="0" * 40):
				report = extract_vpx_corpora([("fixture", corpus, "https://example.invalid")], repository)
			self.assertEqual(0, report["script_count"])
			self.assertFalse((repository / "evidence/vpx/fixture").exists())


if __name__ == "__main__":
	unittest.main()
