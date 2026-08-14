from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.errors import DefinitionError
from pinmame_game_defs.opdb import import_opdb, load_opdb_machine_identity_index


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value), encoding="utf-8")


class OpdbImportTests(unittest.TestCase):
	def test_import_updates_identity_family_provenance_and_incoherences(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			write_json(
				root / "catalog/pinmame.json",
				{"drivers": [{"id": "game"}, {"id": "unmapped"}]},
			)
			write_json(
				root / "machines/stubs/game.json",
				{
					"format": "pinmame-machine-definition",
					"machine": {"id": "stub.pinmame.game", "name": "STUB - Game", "manufacturer": "Maker", "year": 1980},
					"drivers": [{"id": "game"}],
				},
			)
			(root / "machines/opdb_id.csv").write_text("romset,opdb_id\ngame,GOLD-MOLD\nextra,GNEW-MNEW\n", encoding="utf-8")
			write_json(
				root / "config/opdb-overrides.json",
				{"format": "pinmame-opdb-overrides", "schema_version": 1, "machines": {}, "stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"}},
			)
			snapshot = root / "latest-opdb.json"
			write_json(
				snapshot,
				{
					"machineGroups": [{"opdbId": "GNEW", "name": "Game"}],
					"machines": [
						{
							"opdbId": "GNEW-MNEW",
							"name": "Game",
							"commonName": None,
							"ipdbId": 123,
							"manufactureDate": "1980-01-01",
							"manufacturer": {"name": "Maker", "fullName": "Maker, Inc."},
						}
					],
					"aliases": [],
				},
			)
			report = import_opdb(root, snapshot, "2026-08-14T17:53:43Z")
			definition = json.loads((root / "machines/stubs/game.json").read_text(encoding="utf-8"))
			family_path = root / "families/opdb/gnew.json"
			family = json.loads(family_path.read_text(encoding="utf-8"))
			self.assertEqual(123, definition["machine"]["ipdb_id"])
			self.assertEqual("GNEW-MNEW", definition["machine"]["opdb_id"])
			self.assertEqual("stale_id_rewrite", report["machines"][0]["resolution"])
			self.assertEqual(["unmapped"], report["incoherences"]["catalog_drivers_without_csv_mapping"])
			self.assertEqual([{"romset": "extra", "opdb_id": "GNEW-MNEW"}], report["incoherences"]["csv_romsets_not_in_catalog"])
			self.assertEqual("GNEW", family["family"]["opdb_id"])
			self.assertEqual({"stub.pinmame.game": {"ipdb_id": 123, "opdb_id": "GNEW-MNEW"}}, load_opdb_machine_identity_index(root))
			import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)
			write_json(root / "families/opdb/stale.json", family)
			with self.assertRaisesRegex(DefinitionError, "Unexpected stale OPDB family files"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)


if __name__ == "__main__":
	unittest.main()
