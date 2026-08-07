"""Fail-closed tests for source excerpts.

A recorded SHA-256 detects local drift but says nothing about what a source contained, so a reader
cannot tell what an assertion was actually read out of. Excerpts close that gap by storing the
transcribed region beside the definition. They only close it while they stay present, stay attached
to the bytes they claim, and stay honest about how they were produced, so all three fail closed.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCERPT_ROOT = ROOT / "evidence" / "excerpts"
IMAGE_LIMIT = 100_000


def definitions() -> list[Path]:
	return sorted((ROOT / "machines").rglob("*.json"))


def sources_with_excerpts():
	for path in definitions():
		document = json.loads(path.read_text(encoding="utf-8"))
		for source in document.get("sources", []):
			for excerpt in source.get("excerpts", []) or []:
				yield path, source, excerpt


class ExcerptTests(unittest.TestCase):
	def test_every_excerpt_file_exists_and_matches_its_digest(self) -> None:
		seen = 0
		for definition, source, excerpt in sources_with_excerpts():
			seen += 1
			for field, digest_field in (("path", "sha256"), ("image", "image_sha256")):
				relative = excerpt.get(field)
				if not relative:
					continue
				resolved = ROOT / relative
				self.assertTrue(resolved.is_file(), f"{definition.name} -> missing {relative}")
				recorded = excerpt.get(digest_field)
				self.assertIsInstance(recorded, str, f"{relative}: {digest_field} is required")
				self.assertEqual(
					recorded,
					hashlib.sha256(resolved.read_bytes()).hexdigest(),
					f"{relative} no longer matches its recorded digest",
				)
		self.assertGreater(seen, 0, "no excerpts found; this suite would pass vacuously")

	def test_excerpt_crops_stay_within_the_size_budget(self) -> None:
		"""A crop is a reading aid, not an archive.

		Scanned line art compresses badly, so the way back under the limit is a tighter crop rather
		than a quality low enough to blur the text. A colour insert map may legitimately need more,
		but it has to be a deliberate exception rather than the norm.
		"""
		for _, _, excerpt in sources_with_excerpts():
			image = excerpt.get("image")
			if not image:
				continue
			size = (ROOT / image).stat().st_size
			self.assertLessEqual(size, IMAGE_LIMIT, f"{image} is {size} bytes")

	def test_excerpts_declare_how_they_were_transcribed(self) -> None:
		"""An excerpt is itself an assertion, so an OCR pass and a checked read must differ."""
		for definition, _, excerpt in sources_with_excerpts():
			self.assertIn(
				excerpt.get("method"),
				{"manual", "ocr", "model", "mixed"},
				f"{definition.name} -> {excerpt.get('id')} must record how it was transcribed",
			)

	def test_crops_record_how_they_were_derived(self) -> None:
		"""Without a derivation the crop is an opaque blob that cannot be reproduced."""
		for _, _, excerpt in sources_with_excerpts():
			if excerpt.get("image"):
				self.assertTrue(
					excerpt.get("image_derivation"),
					f"{excerpt.get('id')}: a crop must say which page and box it came from",
				)

	def test_no_orphaned_excerpt_files(self) -> None:
		"""Every file under evidence/excerpts must be cited by some definition."""
		if not EXCERPT_ROOT.is_dir():
			self.skipTest("no excerpts directory")
		cited = set()
		for _, _, excerpt in sources_with_excerpts():
			for field in ("path", "image"):
				if excerpt.get(field):
					cited.add((ROOT / excerpt[field]).resolve())
		on_disk = {p.resolve() for p in EXCERPT_ROOT.rglob("*") if p.is_file()}
		self.assertEqual(set(), on_disk - cited, "excerpt files that nothing cites")

	def test_shared_excerpts_are_stored_once(self) -> None:
		"""The AS-2518-43 sheet is cited by two machines; it must not be duplicated per machine.

		Storing a transcription inline in each definition would let the copies diverge, which is the
		drift problem this mechanism exists to solve, one level up.
		"""
		by_path: dict[str, set[str]] = {}
		for definition, _, excerpt in sources_with_excerpts():
			by_path.setdefault(excerpt["path"], set()).add(definition.name)
		shared = {path: names for path, names in by_path.items() if len(names) > 1}
		for path in shared:
			self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
	unittest.main()
