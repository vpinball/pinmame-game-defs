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
# A page-scale drawing is the one case the budget above cannot serve. A location
# diagram, schematic sheet or wiring drawing carries its evidence in callouts
# spread across the whole page, so cropping it tighter drops the very thing being
# cited, and a scanned drawing at its own native resolution simply does not fit in
# 100 kB. These are listed rather than detected so the exception stays deliberate:
# adding one is an edit a reviewer sees, and the ordinary limit still applies to
# every table crop, which is where tightening the crop is the right answer.
DRAWING_LIMIT = 1_500_000
PAGE_SCALE_DRAWINGS = {
	"excerpt.addams-family.flipper-controller-wiring",
	"excerpt.addams-family.switch-locations",
	"excerpt.big-bang-bar.lamp-locations",
	"excerpt.big-bang-bar.solenoid-locations",
	"excerpt.big-bang-bar.switch-locations",
	"excerpt.cactus-canyon.lamp-locations",
	"excerpt.cactus-canyon.opto-board-assemblies",
	"excerpt.cactus-canyon.solenoid-flasher-locations",
	"excerpt.cactus-canyon.solenoid-flasher-wiring",
	"excerpt.cactus-canyon.switch-locations",
	"excerpt.cirqus-voltaire.lamp-locations",
	"excerpt.cirqus-voltaire.solenoid-flashlamp-locations",
	"excerpt.cirqus-voltaire.switch-locations",
	"excerpt.congo.lamp-locations",
	"excerpt.congo.solenoid-flashlamp-locations",
	"excerpt.congo.switch-locations",
	"excerpt.creature.lamp-locations",
	"excerpt.creature.solenoid-flasher-locations",
	"excerpt.creature.solenoid-flasher-wiring",
	"excerpt.creature.switch-locations",
	"excerpt.dracula.lamp-matrix-and-locations",
	"excerpt.dracula.solenoid-flasher-locations",
	"excerpt.dracula.solenoid-flasher-wiring",
	"excerpt.dracula.switch-locations",
	"excerpt.fathom.playfield-wiring",
	"excerpt.fish-tales.lamp-locations",
	"excerpt.fish-tales.solenoid-flasher-wiring",
	"excerpt.fish-tales.switch-locations",
	"excerpt.flash-gordon.parts-list-coils",
	"excerpt.funhouse.general-illumination-flipper-circuits",
	"excerpt.funhouse.lamp-locations",
	"excerpt.funhouse.rudy-mechanism-parts",
	"excerpt.funhouse.solenoid-locations",
	"excerpt.funhouse.switch-lamp-solenoid-circuits",
	"excerpt.funhouse.switch-locations",
	"excerpt.high-speed.lamp-locations",
	"excerpt.high-speed.solenoid-flasher-locations",
	"excerpt.high-speed.switch-locations",
	"excerpt.indiana-jones.board-assemblies",
	"excerpt.indiana-jones.lamp-matrix-and-locations",
	"excerpt.indiana-jones.solenoid-flasher-wiring",
	"excerpt.indiana-jones.switch-locations",
	"excerpt.judge-dredd.lamp-locations",
	"excerpt.judge-dredd.solenoid-flasher-locations",
	"excerpt.monster-bash.boards-and-assemblies",
	"excerpt.monster-bash.lamp-locations",
	"excerpt.monster-bash.solenoid-flasher-locations",
	"excerpt.monster-bash.solenoid-flasher-wiring",
	"excerpt.monster-bash.switch-locations",
	"excerpt.ngg.auxiliary-8-driver-board",
	"excerpt.ngg.flipper-circuits",
	"excerpt.ngg.lamp-locations",
	"excerpt.ngg.solenoid-locations",
	"excerpt.ngg.solenoid-wiring",
	"excerpt.ngg.switch-locations",
	"excerpt.rfm.lamp-locations-matrix-a",
	"excerpt.rfm.lamp-locations-matrix-b",
	"excerpt.rfm.playfield-switch-locations",
	"excerpt.rfm.solenoid-flasher-locations",
	"excerpt.scared-stiff.solenoid-flasher-wiring",
	"excerpt.scared-stiff.switch-locations-opto-sweep",
	"excerpt.sttng.gun-assembly",
	"excerpt.sttng.lamp-matrix-and-locations",
	"excerpt.sttng.solenoid-flasher-locations",
	"excerpt.sttng.solenoid-flasher-wiring",
	"excerpt.sttng.switch-locations",
	"excerpt.theatre-of-magic.lamp-locations",
	"excerpt.theatre-of-magic.solenoid-flasher-wiring",
	"excerpt.theatre-of-magic.solenoid-flashlamp-locations",
	"excerpt.theatre-of-magic.switch-locations",
	"excerpt.totan.lamp-matrix-and-locations",
	"excerpt.totan.solenoid-flasher-wiring",
	"excerpt.totan.solenoid-flashlamp-locations",
	"excerpt.totan.switch-locations",
	"excerpt.twilight-zone.lamp-locations",
	"excerpt.twilight-zone.solenoid-flasher-locations",
	"excerpt.twilight-zone.switch-locations-continued",
	"excerpt.white-water.chase-lamp-board",
	"excerpt.white-water.lamp-locations",
	"excerpt.white-water.solenoid-flasher-locations",
	"excerpt.white-water.solenoid-flasher-wiring",
	"excerpt.white-water.switch-locations",
	"excerpt.world-cup-soccer.lamp-locations",
	"excerpt.world-cup-soccer.solenoid-flasher-locations",
	"excerpt.world-cup-soccer.solenoid-flasher-wiring",
	"excerpt.world-cup-soccer.switch-locations",
}


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
		than a quality low enough to blur the text. A page-scale drawing is the deliberate
		exception, and it has to be named in PAGE_SCALE_DRAWINGS rather than detected, so that
		granting one is a visible edit instead of a side effect of how a file happened to render.
		"""
		for _, _, excerpt in sources_with_excerpts():
			image = excerpt.get("image")
			if not image:
				continue
			size = (ROOT / image).stat().st_size
			limit = DRAWING_LIMIT if excerpt.get("id") in PAGE_SCALE_DRAWINGS else IMAGE_LIMIT
			self.assertLessEqual(size, limit, f"{image} is {size} bytes (limit {limit})")

	def test_every_named_drawing_exception_is_used_and_needed(self) -> None:
		"""An exception list decays into a rubber stamp unless it is kept honest.

		An id that no longer exists, or one whose crop now fits the ordinary budget, must leave
		the list rather than sit there pre-authorising a future oversize file.
		"""
		sizes = {
			excerpt["id"]: (ROOT / excerpt["image"]).stat().st_size
			for _, _, excerpt in sources_with_excerpts()
			if excerpt.get("image")
		}
		self.assertEqual(set(), PAGE_SCALE_DRAWINGS - set(sizes), "named exceptions that cite no excerpt")
		unnecessary = {name for name in PAGE_SCALE_DRAWINGS if sizes[name] <= IMAGE_LIMIT}
		self.assertEqual(set(), unnecessary, "exceptions whose crop now fits the ordinary budget")

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
