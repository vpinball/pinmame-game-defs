from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("make_excerpt", ROOT / "tools" / "make_excerpt.py")
MAKE_EXCERPT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MAKE_EXCERPT)


class MakeExcerptToolTests(unittest.TestCase):
	def test_resolver_skips_broken_path_shim(self) -> None:
		def which(candidate: str) -> str | None:
			return {"pdftoppm.exe": None, "pdftoppm": "broken.cmd"}.get(candidate)

		def run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[bytes]:
			if command[0] == "broken.cmd":
				raise OSError("wrapper target is missing")
			return subprocess.CompletedProcess(command, 0)

		with mock.patch.object(MAKE_EXCERPT.shutil, "which", side_effect=which), \
			 mock.patch.object(MAKE_EXCERPT.Path, "is_file", autospec=True, side_effect=lambda path: str(path) == r"C:\Tools\poppler-23.05.0\Library\bin\pdftoppm.exe"), \
			 mock.patch.object(MAKE_EXCERPT.subprocess, "run", side_effect=run):
			self.assertEqual(r"C:\Tools\poppler-23.05.0\Library\bin\pdftoppm.exe", MAKE_EXCERPT.find_pdftoppm())

	def test_resolver_rejects_every_unusable_candidate(self) -> None:
		with mock.patch.object(MAKE_EXCERPT.shutil, "which", return_value="broken.cmd"), \
			 mock.patch.object(MAKE_EXCERPT.subprocess, "run", side_effect=subprocess.TimeoutExpired("pdftoppm", 5)):
			with self.assertRaisesRegex(SystemExit, "no usable pdftoppm"):
				MAKE_EXCERPT.find_pdftoppm()


if __name__ == "__main__":
	unittest.main()
