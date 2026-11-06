from __future__ import annotations

import copy
import hashlib
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.jsonio import canonical_bytes, load_json
from tools import build_external_evidence_manifest as manifest
from tools import curate_xenon as curator


class XenonCuratorTests(unittest.TestCase):
	def setUp(self):
		self.tmp = tempfile.TemporaryDirectory(dir=os.environ.get("PINMAME_XENON_TEST_TMP"))
		self.addCleanup(self.tmp.cleanup)
		self.root = Path(self.tmp.name) / "repo"
		self.root.mkdir()
		self.manuals = Path(self.tmp.name) / "manuals"
		self.vpx = Path(self.tmp.name) / "vpx"
		self.manuals.mkdir()
		self.vpx.mkdir()
		self.extraction = self.vpx / "bally/xenon-1980/extracted-v2.5.2"
		self.extraction.mkdir(parents=True)
		(self.extraction / "script.vbs").write_bytes(b"fixture script\n")
		(self.extraction / "A.txt").write_bytes(b"A")
		digest = manifest.write_manifest(self.extraction, "xenon")
		manual = self.manuals / "manual.pdf"
		manual.write_bytes(b"fixture manual")
		excerpt = self.root / "evidence/excerpts/bally.xenon.1980/test.md"
		excerpt.parent.mkdir(parents=True)
		excerpt.write_bytes(b"transcription\n")
		definition = load_json(curator.ROOT / "machines/partial/bally/xenon-1980.json")
		# This fixture tests the curator's guards, independently of the real game's
		# expanding evidence bundle. The actual bundle has separate evidence tests.
		for source in definition["sources"]:
			source.pop("excerpts", None)
			source["uri"] = "https://example.test/fixture/" + source["id"]
		definition["sources"].append({
			"id": "manual.fixture", "kind": "manual", "uri": "external:pinmame-manuals/manual.pdf",
			"locator": "fixture", "license": "NOASSERTION", "attribution": "fixture",
			"sha256": hashlib.sha256(manual.read_bytes()).hexdigest(),
			"excerpts": [{"id": "excerpt.fixture", "locator": "page 1", "path": excerpt.relative_to(self.root).as_posix(), "sha256": hashlib.sha256(excerpt.read_bytes()).hexdigest()}],
		})
		self.seed = {
			"definition": definition, "knowledge_note": "Fixture knowledge.\n",
			"spatial_report": {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": curator.MACHINE_ID},
			"spatial_markdown": "# Fixture report\n",
			"external_files": [{"root": "manuals", "path": "manual.pdf", "sha256": hashlib.sha256(manual.read_bytes()).hexdigest()}],
			"extraction": {"root": "vpx-sources", "path": "bally/xenon-1980/extracted-v2.5.2", "game": "xenon", "manifest_sha256": digest, "file_count": 2, "total_bytes": len(b"fixture script\n") + 1},
		}
		self.env = patch.dict(os.environ, {name: "" for name in curator.ROOT_ENV.values()})
		self.env.start()
		self.addCleanup(self.env.stop)

	def write_seed(self):
		path = self.root / curator.SEED_PATH
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(canonical_bytes(self.seed))

	def test_missing_seed_and_missing_keys_fail(self):
		with self.assertRaisesRegex(ValueError, "missing seed"):
			curator.run(self.root, "check")
		for key in self.seed:
			bad = copy.deepcopy(self.seed)
			del bad[key]
			with self.subTest(key=key), self.assertRaisesRegex(ValueError, "missing seed keys"):
				curator.validate_seed(bad, self.root)

	def test_cli_modes_are_exclusive_and_check_is_read_only(self):
		self.write_seed()
		curator.run(self.root, "regenerate")
		with patch.object(curator, "ROOT", self.root), patch.object(sys, "argv", ["curate_xenon.py", "--check"]), redirect_stdout(io.StringIO()):
			# Schema files belong to the installed repository, so keep schema root
			# intact while exercising argument parsing and dispatch separately.
			with patch.object(curator, "run") as run:
				self.assertEqual(curator.main(), 0)
				run.assert_called_once_with(self.root, "check")
		with patch.object(sys, "argv", ["curate_xenon.py", "--check", "--regenerate"]), redirect_stderr(io.StringIO()):
			with self.assertRaises(SystemExit) as exc:
				curator.main()
			self.assertEqual(exc.exception.code, 2)

	def test_deterministic_artifacts_and_check_never_mutates(self):
		self.write_seed()
		curator.run(self.root, "regenerate")
		paths = list(curator.artifacts(self.seed, self.root))
		before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
		curator.run(self.root, "check")
		curator.run(self.root, "regenerate")
		self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths})
		paths[1].write_bytes(b"drift")
		drift = {p: p.read_bytes() for p in paths}
		with self.assertRaisesRegex(ValueError, "drifted"):
			curator.run(self.root, "check")
		self.assertEqual(drift, {p: p.read_bytes() for p in paths})
		self.seed["knowledge_note"] += "Changed.\n"
		self.write_seed()
		with self.assertRaisesRegex(ValueError, "drifted"):
			curator.run(self.root, "check")

	def test_excerpt_tamper_and_missing_are_rejected(self):
		excerpt = self.root / self.seed["definition"]["sources"][-1]["excerpts"][0]["path"]
		for content in (b"tampered", None):
			if content is None:
				excerpt.unlink()
			else:
				excerpt.write_bytes(content)
			with self.subTest(content=content), self.assertRaisesRegex(ValueError, "excerpt|digest"):
				curator.validate_seed(self.seed, self.root)

	def test_library_excerpt_is_literal_including_ranges_and_both_handlers(self):
		source = self.vpx / "Bally.vbs"
		lines = [f"source line {n}" for n in range(1,140)]
		source.write_text("\n".join(lines) + "\n", encoding="utf-8")
		excerpt = self.root / "bally.md"
		text = "\n\n".join(f"Lines {start}-{end}: literal block\n\n```vb\n" + "\n".join(lines[start-1:end]) + "\n```" for start,end in [(20,47),(72,139)])
		excerpt.write_text(text, encoding="utf-8")
		curator.verify_bally_excerpt(source, excerpt)
		for bad in [text.replace("source line 73", "End Function"), text.replace("20-47", "21-47"), text.split("Lines 72")[0]]:
			excerpt.write_text(bad, encoding="utf-8")
			with self.subTest(bad=bad[:70]), self.assertRaisesRegex(ValueError, "Bally excerpt"):
				curator.verify_bally_excerpt(source, excerpt)

	def test_explicit_roots_fail_closed_and_configured_roots_are_checked(self):
		curator.run(self.root, "regenerate", self.seed)
		with self.assertRaisesRegex(ValueError, "required"):
			curator.run(self.root, "verify-evidence", self.seed)
		with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": str(self.manuals), "PINMAME_VPX_SOURCES_ROOT": str(self.vpx)}):
			curator.run(self.root, "verify-evidence", self.seed)
			(self.manuals / "manual.pdf").write_bytes(b"tampered")
			with self.assertRaisesRegex(ValueError, "external file"):
				curator.run(self.root, "check", self.seed)
		with patch.dict(os.environ, {"PINMAME_MANUALS_ROOT": str(self.root / "missing")}):
			with self.assertRaisesRegex(ValueError, "configured evidence root"):
				curator.run(self.root, "check", self.seed)

	def test_extraction_tamper_and_added_file(self):
		with patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": str(self.vpx)}):
			curator.run(self.root, "regenerate", self.seed)
			original = (self.extraction / "A.txt").read_bytes()
			(self.extraction / "A.txt").write_bytes(b"B")
			with self.assertRaisesRegex(ValueError, "extraction identity"):
				curator.run(self.root, "check", self.seed)
			(self.extraction / "A.txt").write_bytes(original)
			(self.extraction / "new.txt").write_bytes(b"new")
			with self.assertRaisesRegex(ValueError, "extraction identity"):
				curator.run(self.root, "check", self.seed)

	def test_stale_author_ready_is_preserved_before_any_write(self):
		path = self.root / "machines/author-ready/bally/xenon-1980.json"
		path.parent.mkdir(parents=True)
		path.write_bytes(b"valuable artifact")
		with self.assertRaisesRegex(ValueError, "author-ready"):
			curator.run(self.root, "regenerate", self.seed)
		self.assertEqual(path.read_bytes(), b"valuable artifact")
		self.assertFalse((self.root / curator.KNOWLEDGE_PATH).exists())
	def test_secondary_extraction_is_also_recomputed(self):
		secondary = self.vpx / "bally/xenon-1980/extracted-v600"
		secondary.mkdir(parents=True)
		(secondary / "script.vbs").write_bytes(b"secondary")
		digest = manifest.write_manifest(secondary, "xenon")
		self.seed["secondary_extractions"] = [{"root":"vpx-sources", "path":"bally/xenon-1980/extracted-v600", "game":"xenon", "manifest_sha256":digest, "file_count":1, "total_bytes":9}]
		with patch.dict(os.environ, {"PINMAME_VPX_SOURCES_ROOT": str(self.vpx)}):
			curator.run(self.root, "regenerate", self.seed)
			(secondary / "script.vbs").write_bytes(b"tampered")
			with self.assertRaisesRegex(ValueError, "extraction identity"):
				curator.run(self.root, "check", self.seed)

	def test_internal_repository_source_hash_is_enforced(self):
		path = self.root / "evidence/fixture.json"
		path.write_bytes(b"derived facts")
		source = self.seed["definition"]["sources"][-1]
		source.update(uri="internal:evidence/fixture.json", sha256=hashlib.sha256(path.read_bytes()).hexdigest())
		curator.validate_seed(self.seed, self.root)
		path.write_bytes(b"changed")
		with self.assertRaisesRegex(ValueError, "repository source"):
			curator.validate_seed(self.seed, self.root)

	def test_author_ready_identical_is_noop_and_changed_is_refused(self):
		# Isolate the overwrite guard; a real author-ready seed must also pass all
		# schema and completeness validation before this branch is reached.
		seed = copy.deepcopy(self.seed)
		seed["definition"]["coverage"]["status"] = "author_ready"
		with patch.object(curator, "validate_seed"):
			curator.run(self.root, "regenerate", seed)
			path = self.root / "machines/author-ready/bally/xenon-1980.json"
			before = path.read_bytes(), path.stat().st_mtime_ns
			curator.run(self.root, "regenerate", seed)
			self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))
			seed["definition"]["machine"]["name"] = "changed"
			with self.assertRaisesRegex(ValueError, "author-ready"):
				curator.run(self.root, "regenerate", seed)
			self.assertEqual(before, (path.read_bytes(), path.stat().st_mtime_ns))

	def test_invalid_definition_report_and_external_assertions(self):
		mutations = [
			lambda s: s["definition"]["machine"].update(id="wrong.machine"),
			lambda s: s["definition"]["drivers"].append(copy.deepcopy(s["definition"]["drivers"][0])),
			lambda s: s["definition"]["inputs"].append({**copy.deepcopy(s["definition"]["inputs"][0]), "binding": {"group": "pinmame.input.switch", "device": 999}}),
			lambda s: s["definition"]["inputs"][0]["provenance"].update(source_refs=["missing.source"]),
			lambda s: s["definition"].update(format="wrong"),
			lambda s: s["spatial_report"].update(format="pinmame-spatial-audit"),
			lambda s: s["spatial_report"].update(version=0),
			lambda s: s["external_files"][0].update(sha256="0" * 64),
			lambda s: s["definition"]["sources"][-1].pop("sha256"),
			lambda s: s["definition"]["sources"][-1].update(uri="external:pinmame-manuals/missing.pdf"),
			lambda s: s["external_files"].clear(),
			lambda s: s["external_files"][0].update(path="../manual.pdf"),
		]
		for mutate in mutations:
			bad = copy.deepcopy(self.seed)
			mutate(bad)
			with self.subTest(mutation=mutate), self.assertRaises(ValueError):
				curator.validate_seed(bad, self.root)


if __name__ == "__main__":
	unittest.main()
