"""Every report under reports/spatial must declare its purpose and agree with its machine.

Before this module the repository carried eight spatial reports in seven different shapes under
three format identifiers, two of them with files that omitted `version` entirely, and nothing
validated any of them. `pinmame-spatial-audit` meant both "here is why this machine was promoted"
and "here is why this machine cannot be promoted", which are opposite claims.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.validation import (  # noqa: E402
	SPATIAL_AUDIT_FORMAT,
	SPATIAL_BLOCKERS_FORMAT,
	_validate_spatial_reports,
)

SPATIAL_ROOT = ROOT / "reports" / "spatial"
SCHEMA_PATH = ROOT / "schemas" / "spatial-report.schema.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


def definitions_by_machine() -> dict[str, dict[str, object]]:
	result: dict[str, dict[str, object]] = {}
	for path in (ROOT / "machines").rglob("*.json"):
		definition = load_json(path)
		result[definition["machine"]["id"]] = definition
	return result


class SpatialReportEnvelopeTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.reports = {path: load_json(path) for path in sorted(SPATIAL_ROOT.rglob("*.json"))}
		cls.definitions = definitions_by_machine()

	def test_there_are_reports_to_check(self) -> None:
		self.assertGreaterEqual(len(self.reports), 8)

	def test_every_report_declares_a_known_purpose_and_version(self) -> None:
		for path, report in self.reports.items():
			name = path.relative_to(ROOT).as_posix()
			self.assertIn(report.get("format"), {SPATIAL_AUDIT_FORMAT, SPATIAL_BLOCKERS_FORMAT}, name)
			self.assertIsInstance(report.get("version"), int, name)
			self.assertGreaterEqual(report["version"], 1, name)
			self.assertIsInstance(report.get("machine_id"), str, name)

	def test_every_report_resolves_to_a_machine(self) -> None:
		for path, report in self.reports.items():
			self.assertIn(report["machine_id"], self.definitions, path.relative_to(ROOT).as_posix())

	def test_report_purpose_matches_machine_coverage(self) -> None:
		for path, report in self.reports.items():
			name = path.relative_to(ROOT).as_posix()
			status = self.definitions[report["machine_id"]]["coverage"]["status"]
			if report["format"] == SPATIAL_AUDIT_FORMAT:
				self.assertEqual("author_ready", status, f"{name} audits a machine that is {status}")
			else:
				self.assertNotEqual("author_ready", status, f"{name} blocks an author-ready machine")

	def test_reports_live_under_a_manufacturer_directory(self) -> None:
		for path in self.reports:
			relative = path.relative_to(SPATIAL_ROOT)
			self.assertEqual(2, len(relative.parts), f"{relative.as_posix()} must be <manufacturer>/<machine>.json")

	def test_one_format_identifier_means_one_purpose(self) -> None:
		"""No format may be used for both a promoted and an unpromotable machine."""
		purposes: dict[str, set[str]] = {}
		for report in self.reports.values():
			status = self.definitions[report["machine_id"]]["coverage"]["status"]
			purposes.setdefault(report["format"], set()).add(status == "author_ready")
		for fmt, seen in purposes.items():
			self.assertEqual(1, len(seen), f"{fmt} is used for both promoted and unpromotable machines")


class SpatialReportValidationTests(unittest.TestCase):
	"""The rule has to actually reject the mistakes it exists to prevent."""

	def setUp(self) -> None:
		self.definitions = definitions_by_machine()
		self._tmp = tempfile.TemporaryDirectory()
		self.root = Path(self._tmp.name)
		(self.root / "reports" / "spatial" / "stern").mkdir(parents=True)
		(self.root / "schemas").mkdir()
		shutil.copy(SCHEMA_PATH, self.root / "schemas" / "spatial-report.schema.json")

	def tearDown(self) -> None:
		self._tmp.cleanup()

	def _check(self, report: dict[str, object], relative_path: str | None = None) -> list[str]:
		machine_id = str(report.get("machine_id", "unknown.machine.0000"))
		parts = machine_id.split(".")
		canonical_path = f"{parts[0]}/{'-'.join(parts[1:])}.json"
		path = self.root / "reports" / "spatial" / (relative_path or canonical_path)
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(json.dumps(report), encoding="utf-8")
		errors: list[str] = []
		_validate_spatial_reports(self.root, self.definitions, errors)
		return errors

	def test_audit_for_a_partial_machine_is_rejected(self) -> None:
		errors = self._check({"format": SPATIAL_AUDIT_FORMAT, "version": 1, "machine_id": "stern.x-men-pro.2012"})
		self.assertTrue(any("$.format" in e for e in errors), errors)

	def test_blocker_report_for_an_author_ready_machine_is_rejected(self) -> None:
		errors = self._check({"format": SPATIAL_BLOCKERS_FORMAT, "version": 1, "machine_id": "bally.attack-from-mars.1995"})
		self.assertTrue(any("$.format" in e for e in errors), errors)

	def test_unknown_machine_is_rejected(self) -> None:
		errors = self._check({"format": SPATIAL_AUDIT_FORMAT, "version": 1, "machine_id": "stern.not-a-real-machine.1999"})
		self.assertTrue(any("does not resolve" in e for e in errors), errors)

	def test_missing_version_is_rejected(self) -> None:
		errors = self._check({"format": SPATIAL_AUDIT_FORMAT, "machine_id": "bally.attack-from-mars.1995"})
		self.assertTrue(any("version" in e for e in errors), errors)

	def test_unknown_format_is_rejected(self) -> None:
		errors = self._check({"format": "pinmame-spatial-review", "version": 1, "machine_id": "bally.attack-from-mars.1995"})
		self.assertTrue(any("$.format" in e for e in errors), errors)

	def test_a_correct_report_passes(self) -> None:
		errors = self._check({"format": SPATIAL_AUDIT_FORMAT, "version": 1, "machine_id": "bally.attack-from-mars.1995"})
		self.assertEqual([], errors)

	def test_noncanonical_report_filename_is_rejected(self) -> None:
		errors = self._check({"format": SPATIAL_AUDIT_FORMAT, "version": 1, "machine_id": "bally.attack-from-mars.1995"}, "bally/attack-from-mars-1995-extraction.json")
		self.assertTrue(any("expected canonical report path" in error for error in errors), errors)


if __name__ == "__main__":
	unittest.main()
