from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.errors import DefinitionError
from pinmame_game_defs.jsonio import file_sha256
from pinmame_game_defs.opdb import _override_is_redundant, catalog_root_names_agree, identity_disagreement, identity_disagreements, import_opdb, load_opdb_machine_identity_index, names_agree, record_name_agrees


ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, value: object) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(value), encoding="utf-8")


class OpdbImportTests(unittest.TestCase):
	def test_identity_disagreement_rejects_same_title_from_another_manufacturer(self) -> None:
		definition = {"machine": {"id": "game-plan.rio.1978", "name": "Rio", "manufacturer": "Game Plan", "year": 1978}}
		wrong_record = {
			"opdbId": "GRw9Z-MLbl4",
			"name": "Rio",
			"commonName": None,
			"manufacturer": {"name": "Playmatic", "fullName": "Playmatic"},
		}
		correct_record = {
			"opdbId": "GrJy1-MDEbO",
			"name": "Rio",
			"commonName": None,
			"manufacturer": {"name": "Game Plan", "fullName": "Game Plan, Inc."},
		}
		self.assertIn("manufacturer", identity_disagreement(definition, wrong_record) or "")
		self.assertIsNone(identity_disagreement(definition, correct_record))
		concatenated_name = dict(correct_record, name="GamePlanRio")
		self.assertIn("machine name", identity_disagreement(definition, concatenated_name) or "")
		compact_spelling = dict(correct_record, name="Blackbelt")
		compact_definition = {"machine": dict(definition["machine"], name="Black Belt")}
		self.assertIsNone(identity_disagreement(compact_definition, compact_spelling))

	def test_identity_agreement_rejects_substrings_and_single_shared_tokens(self) -> None:
		self.assertFalse(names_agree("Mary Shelley's Frankenstein", "Dealer's Choice"))
		self.assertFalse(names_agree("Star Trek", "Star Wars"))
		for edition in ("EM", "CE", "SE", "Remake", "Deluxe", "Special", "Classic", "1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P"):
			self.assertFalse(names_agree("Mata Hari", f"Mata Hari ({edition})"), edition)
		for qualifier in ("Prototype", "Signature", "75th Anniversary", "Motion Picture Trilogy", "Catwoman Signature Edition"):
			self.assertFalse(names_agree("Kiss", f"Kiss ({qualifier})"), qualifier)
		self.assertTrue(names_agree("AC/DC Pro (original)", "AC/DC (Pro)"))
		self.assertTrue(names_agree("TRON Legacy LE", "TRON Legacy Limited Edition"))
		for left, right in (
			("Whirlwind", "Whirlwind 2.0"),
			("Black Magic", "Black Magic 4"),
			("Cowboy Eight Ball", "Cowboy Eight Ball 2"),
			("A.G. Football", "U.S.A. Football"),
			("Challenger", "Challenger I"),
		):
			self.assertFalse(names_agree(left, right), (left, right))
		for machine_manufacturer, opdb_manufacturer in (("Sega", "Segasa"), ("LTD", "LTDA"), ("MM", "ManilaMatic")):
			definition = {"machine": {"id": "example", "name": "Same Title", "manufacturer": machine_manufacturer, "year": 1980}}
			record = {
				"opdbId": "GEXAMPLE-MEXAMPLE",
				"name": "Same Title",
				"commonName": None,
				"manufacturer": {"name": opdb_manufacturer, "fullName": opdb_manufacturer},
			}
			self.assertIn("manufacturer", identity_disagreement(definition, record) or "")

	def test_identity_disagreements_report_name_and_manufacturer_independently(self) -> None:
		definition = {"machine": {"id": "example", "name": "Space Ship Deluxe", "manufacturer": "Stargame", "year": 1986}}
		record = {
			"opdbId": "G5YVk-MDBvP",
			"name": "Space Ship",
			"commonName": None,
			"manufacturer": {"name": "Unidesa", "fullName": "Unidesa"},
		}
		self.assertEqual({"name", "manufacturer"}, set(identity_disagreements(definition, record)))

	def test_identity_agreement_uses_common_name_and_rejects_wrong_year(self) -> None:
		definition = {"machine": {"id": "example", "name": "Big Hurt", "manufacturer": "Gottlieb", "year": 1995}}
		record = {
			"opdbId": "G4kzN-MQpYx",
			"name": "Frank Thomas' Big Hurt",
			"commonName": "Big Hurt",
			"manufactureDate": "1995-06-01",
			"manufacturer": {"name": "Gottlieb", "fullName": "Gottlieb"},
		}
		self.assertTrue(record_name_agrees("Big Hurt (rev. 3)", record))
		self.assertNotIn("year", identity_disagreements(definition, record))
		record["manufactureDate"] = "2007-06-01"
		self.assertIn("year", identity_disagreements(definition, record))

	def test_common_name_cannot_erase_a_canonical_physical_qualifier(self) -> None:
		record = {"name": "Halloween (SE)", "commonName": "Halloween"}
		self.assertFalse(record_name_agrees("Halloween", record))
		self.assertTrue(record_name_agrees("Halloween SE", record))
		for product_class in ("Bingo", "Shuffle", "Bowler", "Redemption", "Coin Dropper", "Gun Game", "4 Players", "Pinball/Video Combo"):
			self.assertFalse(record_name_agrees(f"Game ({product_class})", {"name": "Game", "commonName": None}), product_class)

	def test_record_name_agreement_ignores_non_physical_record_parentheticals(self) -> None:
		self.assertTrue(record_name_agrees("Rio", {"name": "Rio (Free Play)", "commonName": None}))
		self.assertTrue(record_name_agrees("Rio", {"name": "Rio (rev. 3)", "commonName": None}))
		self.assertTrue(record_name_agrees("Rio", {"name": "Rio (V1.2)", "commonName": None}))

	def test_record_name_agreement_fails_closed_on_unclassified_record_parentheticals(self) -> None:
		self.assertFalse(record_name_agrees("Aztec", {"name": "Aztec (SS)", "commonName": None}))
		self.assertFalse(record_name_agrees("Fathom", {"name": "Fathom (Mermaid)", "commonName": None}))
		self.assertTrue(record_name_agrees("Fathom (Mermaid)", {"name": "Fathom (Mermaid)", "commonName": None}))

	def test_catalog_root_name_agreement_is_any_match_and_fail_closed(self) -> None:
		record = {"name": "Game", "commonName": None}
		catalog = {"wrong": {"description": "Other"}, "right": {"description": "Game"}}
		self.assertEqual(([], False), catalog_root_names_agree([], catalog, record))
		self.assertEqual(([], False), catalog_root_names_agree(["missing"], catalog, record))
		self.assertEqual((["Other", "Game"], True), catalog_root_names_agree(["wrong", "right"], catalog, record))

	def test_redundant_override_check_replays_existing_ipdb_selection(self) -> None:
		manufacturer = {"name": "Maker", "fullName": "Maker"}
		mapped = {"opdbId": "GGAME-MMAPPED", "ipdbId": 123, "name": "Game", "commonName": None, "manufactureDate": "1980-01-01", "manufacturer": manufacturer}
		existing = {"opdbId": "GGAME-MEXISTING", "ipdbId": 456, "name": "Other Title", "commonName": None, "manufactureDate": "1980-01-01", "manufacturer": manufacturer}
		definition = {"machine": {"id": "game", "ipdb_id": 456, "opdb_id": "GGAME-MMAPPED", "name": "Game", "manufacturer": "Maker", "year": 1980}}
		by_ipdb = {123: [mapped], 456: [existing]}
		self.assertTrue(_override_is_redundant(definition, mapped, [mapped], by_ipdb, {}, True))
		self.assertFalse(_override_is_redundant(definition, existing, [mapped, existing], by_ipdb, {}, True))

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
		reported = {
			record["machine_id"]: record
			for record in report["machines"]
			if record["resolution"] in {"override", "csv_with_reviewed_override"}
		}
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
				{
					"drivers": [{"description": "Game", "id": "game"}, {"description": "Unmapped", "id": "unmapped"}],
					"machines": [{"id": "stub.pinmame.game", "root_drivers": ["game"]}],
				},
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
			write_json(
				root / "config/opdb-overrides.json",
				{
					"format": "pinmame-opdb-overrides",
					"schema_version": 1,
					"machines": {"stub.pinmame.game": {"opdb_id": "GNEW-MNEW", "reason": "Redundant selection."}},
					"stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"},
				},
			)
			with self.assertRaisesRegex(DefinitionError, "OPDB override is redundant"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)
			write_json(
				root / "config/opdb-overrides.json",
				{"format": "pinmame-opdb-overrides", "schema_version": 1, "machines": {}, "stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"}},
			)
			write_json(root / "families/opdb/stale.json", family)
			with self.assertRaisesRegex(DefinitionError, "Unexpected stale OPDB family files"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)
			(root / "families/opdb/stale.json").unlink()
			catalog = json.loads((root / "catalog/pinmame.json").read_text(encoding="utf-8"))
			catalog["drivers"][0]["description"] = "Unrelated Root"
			write_json(root / "catalog/pinmame.json", catalog)
			with self.assertRaisesRegex(DefinitionError, "resolved identity disagrees with PinMAME root title"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)
			catalog["drivers"][0]["description"] = "Game"
			write_json(root / "catalog/pinmame.json", catalog)
			definition["machine"]["name"] = "Different Game"
			definition["machine"]["manufacturer"] = "Unrelated Works"
			definition["coverage"] = {"missing": []}
			write_json(root / "machines/stubs/game.json", definition)
			with self.assertRaisesRegex(DefinitionError, "resolved identity is incompatible"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z", check=True)
			write_json(
				root / "config/opdb-overrides.json",
				{
					"format": "pinmame-opdb-overrides",
					"schema_version": 1,
					"machines": {"stub.pinmame.game": {"opdb_id": "not-an-opdb-id", "reason": "Reviewed licensed production."}},
					"stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"},
				},
			)
			with self.assertRaisesRegex(DefinitionError, "OPDB override must contain"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z")
			write_json(
				root / "config/opdb-overrides.json",
				{
					"format": "pinmame-opdb-overrides",
					"schema_version": 1,
					"machines": {"stub.pinmame.game": {"opdb_id": "GNEW-MNEW", "reason": "Reviewed licensed production."}},
					"stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"},
				},
			)
			with self.assertRaisesRegex(DefinitionError, "cross-manufacturer OPDB override requires an evidence_url"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z")
			write_json(
				root / "config/opdb-overrides.json",
				{
					"format": "pinmame-opdb-overrides",
					"schema_version": 1,
					"machines": {
						"stub.pinmame.game": {
							"evidence_url": "https://",
							"opdb_id": "GNEW-MNEW",
							"reason": "Reviewed licensed production.",
						}
					},
					"stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"},
				},
			)
			with self.assertRaisesRegex(DefinitionError, "evidence_url must be an HTTPS URL"):
				import_opdb(root, snapshot, "2026-08-14T17:53:43Z")
			write_json(
				root / "config/opdb-overrides.json",
				{
					"format": "pinmame-opdb-overrides",
					"schema_version": 1,
					"machines": {
						"stub.pinmame.game": {
							"evidence_url": "https://example.test/licensed-production",
							"opdb_id": "GNEW-MNEW",
							"reason": "Reviewed licensed production.",
						}
					},
					"stale_opdb_ids": {"GOLD-MOLD": "GNEW-MNEW"},
				},
			)
			report = import_opdb(root, snapshot, "2026-08-14T17:53:43Z")
			self.assertEqual("csv_with_reviewed_override", report["machines"][0]["resolution"])


if __name__ == "__main__":
	unittest.main()
