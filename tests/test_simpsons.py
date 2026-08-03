from __future__ import annotations

import json
import unittest
from pathlib import Path

from pinmame_game_defs.jsonio import content_sha256


ROOT = Path(__file__).resolve().parents[1]
LEGACY_PATH = ROOT / "games" / "simp.json"
DEFINITION_PATH = ROOT / "machines" / "partial" / "stern" / "the-simpsons-pinball-party-2003.json"
IRON_MAN_VAULT_PATH = ROOT / "machines" / "partial" / "stern" / "iron-man-vault-edition-2014.json"
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class SimpsonsIdentityTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.legacy = load_json(LEGACY_PATH)
		cls.definition = load_json(DEFINITION_PATH)
		cls.iron_man_vault = load_json(IRON_MAN_VAULT_PATH)
		cls.catalog = load_json(CATALOG_PATH)

	def test_tspp_uses_its_physical_ipdb_identity(self) -> None:
		self.assertEqual(4674, self.legacy["game"]["ipdb_id"])
		self.assertEqual(4674, self.definition["machine"]["ipdb_id"])
		source = next(source for source in self.definition["sources"] if source["id"] == "ipdb.the-simpsons-pinball-party.4674")
		self.assertEqual("https://www.ipdb.org/machine.cgi?id=4674", source["uri"])
		self.assertIn("IPDB 6154 link belongs to Iron Man Vault Edition", source["locator"])

	def test_catalog_hashes_resolve_to_the_corrected_definition(self) -> None:
		expected_hash = content_sha256(self.definition)
		machine = next(machine for machine in self.catalog["machines"] if machine["id"] == "stern.the-simpsons-pinball-party.2003")
		self.assertEqual(DEFINITION_PATH.relative_to(ROOT).as_posix(), machine["definition"])
		self.assertEqual(expected_hash, machine["definition_sha256"])
		drivers = [driver for driver in self.catalog["drivers"] if driver.get("machine_id") == machine["id"]]
		self.assertTrue(drivers)
		self.assertTrue(all(driver["definition_sha256"] == expected_hash for driver in drivers))

	def test_iron_man_vault_keeps_the_legitimate_6154_identity(self) -> None:
		self.assertEqual(6154, self.iron_man_vault["machine"]["ipdb_id"])


if __name__ == "__main__":
	unittest.main()
