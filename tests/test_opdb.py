from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.errors import DefinitionError
from pinmame_game_defs.jsonio import file_sha256
from pinmame_game_defs.opdb import import_opdb, load_opdb_machine_identity_index


ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value), encoding="utf-8")


class OpdbImportTests(unittest.TestCase):
	def test_committed_mapping_matches_identity_report(self) -> None:
		mapping_path = ROOT / "machines/opdb_id.csv"
		report = json.loads((ROOT / "reports/opdb-identity.json").read_text(encoding="utf-8"))
		with mapping_path.open("r", encoding="utf-8-sig", newline="") as stream:
			row_count = sum(1 for _ in csv.DictReader(stream))
		self.assertEqual("machines/opdb_id.csv", report["mapping"]["path"])
		self.assertEqual(row_count, report["mapping"]["row_count"])
		self.assertEqual(file_sha256(mapping_path), report["mapping"]["sha256"])

	def test_committed_overrides_match_identity_report(self) -> None:
		overrides = json.loads((ROOT / "config/opdb-overrides.json").read_text(encoding="utf-8"))["machines"]
		report = json.loads((ROOT / "reports/opdb-identity.json").read_text(encoding="utf-8"))
		reported = {record["machine_id"]: record for record in report["machines"] if record["resolution"] == "override"}
		self.assertEqual(set(overrides), set(reported))
		for machine_id, override in overrides.items():
			self.assertEqual(override["opdb_id"], reported[machine_id]["opdb_id"], machine_id)

	def test_unsupported_opdb_identities_stay_unmapped(self) -> None:
		# See docs/CURRENT-STATE.md: the pinned snapshot has no record for either physical variant.
		# The 2026-08-29 identity promotion moved their residual stubs into named partial records
		# whose identity comes from the PinMAME catalog alone, still without any OPDB identity.
		with (ROOT / "machines/opdb_id.csv").open("r", encoding="utf-8-sig", newline="") as stream:
			mapped_romsets = {row["romset"] for row in csv.DictReader(stream)}
		for romset, definition_path in (
			("ebalchmb", ROOT / "machines/partial/maibesa/eight-ball-champ-maibesa-unknown.json"),
			("usafootr", ROOT / "machines/partial/alvin-g/u-s-a-football-redemption-p08-1994.json"),
		):
			self.assertNotIn(romset, mapped_romsets)
			machine = json.loads(definition_path.read_text(encoding="utf-8"))["machine"]
			self.assertNotIn("ipdb_id", machine, romset)
			self.assertNotIn("opdb_id", machine, romset)

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
