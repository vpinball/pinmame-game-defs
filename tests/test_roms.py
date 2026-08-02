from __future__ import annotations

import json
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from pinmame_game_defs.roms import index_rom_corpus


class RomCorpusIndexTests(unittest.TestCase):
	def test_indexes_hashes_without_extracting_roms(self) -> None:
		with TemporaryDirectory() as temporary:
			root = Path(temporary)
			rom_root = root / "roms"
			rom_root.mkdir()
			with zipfile.ZipFile(rom_root / "game1.zip", "w", zipfile.ZIP_DEFLATED) as archive:
				archive.writestr("cpu.bin", b"test-rom-bytes")
			catalog = root / "catalog.json"
			catalog.write_text(json.dumps({"source": {"pinmame_revision": "a" * 40}, "drivers": [{"id": "game1"}, {"id": "missing"}]}), encoding="utf-8")
			output = root / "index.json"
			index = index_rom_corpus(rom_root, catalog, output, content_hashes=True)
			self.assertEqual(1, index["summary"]["matched_driver_count"])
			self.assertEqual(["missing"], index["missing_driver_ids"])
			member = index["archives"][0]["members"][0]
			self.assertEqual("675e009b", member["crc32"])
			self.assertEqual("6b1f801a69c280ecae81d5a381df18b43a503cfb3036e9f43bdcfd6247aa4678", member["sha256"])
			self.assertFalse((rom_root / "cpu.bin").exists())

	def test_reuses_unchanged_archive_records(self) -> None:
		with TemporaryDirectory() as temporary:
			root = Path(temporary)
			rom_root = root / "roms"
			rom_root.mkdir()
			with zipfile.ZipFile(rom_root / "game1.zip", "w") as archive:
				archive.writestr("cpu.bin", b"abc")
			catalog = root / "catalog.json"
			catalog.write_text(json.dumps({"source": {"pinmame_revision": "b" * 40}, "drivers": [{"id": "game1"}]}), encoding="utf-8")
			output = root / "index.json"
			first = index_rom_corpus(rom_root, catalog, output)
			second = index_rom_corpus(rom_root, catalog, output)
			self.assertEqual(first, second)


if __name__ == "__main__":
	unittest.main()
