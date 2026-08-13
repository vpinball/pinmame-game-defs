from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_external_evidence_manifest import build_manifest, check_manifest, write_manifest


class ExternalEvidenceManifestTests(unittest.TestCase):
	def test_manifest_is_canonical_complete_and_self_excluding(self) -> None:
		with tempfile.TemporaryDirectory() as temporary:
			root = Path(temporary)
			(root / "nested").mkdir()
			(root / "z.txt").write_bytes(b"z")
			(root / "nested" / "a.bin").write_bytes(b"a\x00")
			(root / "B.txt").write_bytes(b"B")
			(root / "a.txt").write_bytes(b"a")
			(root / "manifest.json").write_text("stale", encoding="utf-8")
			(root / "manifest.sha256").write_text("stale", encoding="ascii")

			manifest = build_manifest(root, "example_game")
			schema = json.loads((ROOT / "schemas" / "external-evidence-manifest.schema.json").read_text(encoding="utf-8"))
			Draft202012Validator.check_schema(schema)
			Draft202012Validator(schema).validate(manifest)
			self.assertEqual("pinmame-external-evidence-manifest", manifest["format"])
			self.assertEqual("example_game", manifest["game"])
			self.assertEqual(["B.txt", "a.txt", "nested/a.bin", "z.txt"], [item["path"] for item in manifest["files"]])

			digest = write_manifest(root, "example_game")
			manifest_bytes = (root / "manifest.json").read_bytes()
			self.assertTrue(manifest_bytes.endswith(b"\n"))
			self.assertEqual(digest, hashlib.sha256(manifest_bytes).hexdigest())
			self.assertEqual(digest + "\n", (root / "manifest.sha256").read_text(encoding="ascii"))
			self.assertEqual(manifest, json.loads(manifest_bytes))
			self.assertEqual(digest, check_manifest(root, "example_game"))

			(root / "z.txt").write_bytes(b"changed")
			with self.assertRaisesRegex(ValueError, "manifest content is stale"):
				check_manifest(root, "example_game")


if __name__ == "__main__":
	unittest.main()
