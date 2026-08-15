from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
RFM_PATH = ROOT / "machines" / "partial" / "bally" / "revenge-from-mars-1999.json"
SWEP1_PATH = ROOT / "machines" / "stubs" / "swep1_150.json"
TAF_PATH = ROOT / "machines" / "author-ready" / "bally" / "the-addams-family-1992.json"

RFM_DRIVERS = {
	"rfm_120", "rfm_140", "rfm_150", "rfm_160", "rfm_180", "rfm_190", "rfm_191", "rfm_195",
	"rfm_200", "rfm_210", "rfm_222", "rfm_223", "rfm_224", "rfm_250", "rfm_260",
}
SWEP1_DRIVERS = {"swep1_130", "swep1_140", "swep1_150", "swep1_200", "swep1_201", "swep1_210"}
STUB_MISSING = [
	"identity",
	"controller_platform",
	"input_enumeration",
	"input_semantics",
	"output_enumeration",
	"output_semantics",
	"display_inventory",
	"mechanism_inventory",
	"mechanism_behavior",
	"polarity",
	"variant_differences",
	"recreation_notes",
	"provenance",
]


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class Pinball2000CatalogTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.catalog = load_json(CATALOG_PATH)
		cls.catalog_drivers = {driver["id"]: driver for driver in cls.catalog["drivers"]}

	def test_catalog_baseline_counts(self) -> None:
		self.assertEqual(
			{
				"author_ready_count": 24,
				"driver_count": 2888,
				"game_count": 789,
				"machine_count": 790,
				"non_game_count": 1,
				"partial_count": 98,
				"root_driver_count": 774,
				"stub_count": 668,
			},
			self.catalog["summary"],
		)

	def test_pinball_2000_families_are_complete_and_grouped(self) -> None:
		for driver_ids, root_driver, definition, machine_id, coverage in (
			(RFM_DRIVERS, "rfm_160", "machines/partial/bally/revenge-from-mars-1999.json", "bally.revenge-from-mars.1999", "partial"),
			(SWEP1_DRIVERS, "swep1_150", "machines/stubs/swep1_150.json", "stub.pinmame.swep1_150", "stub"),
		):
			catalog_family = {driver_id for driver_id in self.catalog_drivers if driver_id.startswith(root_driver.split("_")[0] + "_")}
			self.assertEqual(driver_ids, catalog_family)
			for driver_id in driver_ids:
				row = self.catalog_drivers[driver_id]
				self.assertEqual(root_driver, row["root_driver"])
				self.assertEqual(definition, row["definition"])
				self.assertEqual(machine_id, row["machine_id"])
				self.assertEqual(coverage, row["coverage_status"])

	def test_swep1_remains_a_fail_closed_stub(self) -> None:
		definition = load_json(SWEP1_PATH)
		self.assertEqual("stub.pinmame.swep1_150", definition["machine"]["id"])
		self.assertNotIn("kind", definition["machine"])
		self.assertEqual(SWEP1_DRIVERS, {driver["id"] for driver in definition["drivers"]})
		self.assertEqual("stub", definition["coverage"]["status"])
		self.assertEqual(STUB_MISSING, definition["coverage"]["missing"])
		for collection in ("inputs", "outputs", "displays", "mechanisms", "relationships", "conflicts"):
			self.assertEqual([], definition[collection])
		self.assertEqual({PINMAME_REVISION}, {source["revision"] for source in definition["sources"]})
		self.assertEqual("knowledge/stubs/swep1_150.md", definition["knowledge"]["path"])
		self.assertTrue((ROOT / definition["knowledge"]["path"]).is_file())

	def test_rfm_is_promoted_to_an_honest_partial(self) -> None:
		definition = load_json(RFM_PATH)
		self.assertEqual("bally.revenge-from-mars.1999", definition["machine"]["id"])
		self.assertEqual(RFM_DRIVERS, {driver["id"] for driver in definition["drivers"]})
		self.assertEqual("partial", definition["coverage"]["status"])
		self.assertEqual(["mechanism_behavior", "polarity", "variant_differences"], definition["coverage"]["missing"])
		self.assertEqual("observed", definition["coverage"]["dimensions"]["spatial_placement"])
		self.assertFalse((ROOT / "machines/stubs/rfm_160.json").exists())
		self.assertFalse((ROOT / "knowledge/stubs/rfm_160.md").exists())

	def test_new_addams_family_variant_does_not_create_a_residual_stub(self) -> None:
		definition = load_json(TAF_PATH)
		taf_i4bs = next(driver for driver in definition["drivers"] if driver["id"] == "taf_i4bs")
		self.assertEqual("taf_l5", taf_i4bs["clone_of"])
		self.assertEqual("compatible", taf_i4bs["physical_compatibility"])
		self.assertIn("ball-saver", taf_i4bs["variant_notes"])
		catalog_row = self.catalog_drivers["taf_i4bs"]
		self.assertEqual("bally.the-addams-family.1992", catalog_row["machine_id"])
		self.assertEqual("author_ready", catalog_row["coverage_status"])
		self.assertFalse((ROOT / "machines" / "stubs" / "taf_l5.json").exists())


if __name__ == "__main__":
	unittest.main()
