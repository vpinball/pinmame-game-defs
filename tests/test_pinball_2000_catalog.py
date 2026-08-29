from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "pinmame.json"
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
RFM_PATH = ROOT / "machines" / "partial" / "bally" / "revenge-from-mars-1999.json"
SWEP1_PATH = ROOT / "machines" / "partial" / "midway" / "pinball-2000-star-wars-episode-i-1-50-2003.json"
TAF_PATH = ROOT / "machines" / "author-ready" / "bally" / "the-addams-family-1992.json"

RFM_DRIVERS = {
	"rfm_120", "rfm_140", "rfm_150", "rfm_160", "rfm_180", "rfm_190", "rfm_191", "rfm_195",
	"rfm_200", "rfm_210", "rfm_222", "rfm_223", "rfm_224", "rfm_250", "rfm_260",
}
SWEP1_DRIVERS = {"swep1_130", "swep1_140", "swep1_150", "swep1_200", "swep1_201", "swep1_210"}
IDENTITY_PARTIAL_MISSING = [
	"identity",
	"driver_mapping",
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
	"spatial_placement",
]
# The 2026-08-29 PinMAME I/O attachment declares the Pinball 2000 controller
# platform from the driver's own CORE_GAMEDEF module, so controller_platform
# leaves the missing list for Episode I.
SWEP1_PARTIAL_MISSING = [item for item in IDENTITY_PARTIAL_MISSING if item != "controller_platform"]


def load_json(path: Path) -> dict[str, object]:
	with path.open("r", encoding="utf-8") as stream:
		return json.load(stream)


class Pinball2000CatalogTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.catalog = load_json(CATALOG_PATH)
		cls.catalog_drivers = {driver["id"]: driver for driver in cls.catalog["drivers"]}

	def test_catalog_baseline_counts(self) -> None:
		# The 2026-08-29 catalog-wide identity promotion converted every residual
		# stub into an identity-resolved partial, so no generated stubs remain.
		self.assertEqual(
			{
				"author_ready_count": 26,
				"driver_count": 2888,
				"game_count": 779,
				"machine_count": 790,
				"non_game_count": 11,
				"partial_count": 764,
				"root_driver_count": 774,
				"stub_count": 0,
			},
			self.catalog["summary"],
		)

	def test_pinball_2000_families_are_complete_and_grouped(self) -> None:
		for driver_ids, root_driver, definition, machine_id, coverage in (
			(RFM_DRIVERS, "rfm_160", "machines/partial/bally/revenge-from-mars-1999.json", "bally.revenge-from-mars.1999", "partial"),
			(SWEP1_DRIVERS, "swep1_150", "machines/partial/midway/pinball-2000-star-wars-episode-i-1-50-2003.json", "midway.pinball-2000-star-wars-episode-i-1-50.2003", "partial"),
		):
			catalog_family = {driver_id for driver_id in self.catalog_drivers if driver_id.startswith(root_driver.split("_")[0] + "_")}
			self.assertEqual(driver_ids, catalog_family)
			for driver_id in driver_ids:
				row = self.catalog_drivers[driver_id]
				self.assertEqual(root_driver, row["root_driver"])
				self.assertEqual(definition, row["definition"])
				self.assertEqual(machine_id, row["machine_id"])
				self.assertEqual(coverage, row["coverage_status"])

	def test_swep1_is_an_identity_only_partial(self) -> None:
		definition = load_json(SWEP1_PATH)
		self.assertEqual("midway.pinball-2000-star-wars-episode-i-1-50.2003", definition["machine"]["id"])
		self.assertEqual({"inversion_applied_by_emulator": True, "platform": "pinmame.p2k"}, definition["controller"])
		self.assertNotIn("kind", definition["machine"])
		self.assertNotIn("ipdb_id", definition["machine"])
		self.assertNotIn("opdb_id", definition["machine"])
		self.assertEqual(SWEP1_DRIVERS, {driver["id"] for driver in definition["drivers"]})
		self.assertEqual("partial", definition["coverage"]["status"])
		self.assertEqual(SWEP1_PARTIAL_MISSING, definition["coverage"]["missing"])
		for collection in ("inputs", "outputs", "displays", "mechanisms", "relationships", "conflicts"):
			self.assertEqual([], definition[collection])
		self.assertEqual({PINMAME_REVISION}, {source["revision"] for source in definition["sources"]})
		core_sources = [source for source in definition["sources"] if source["id"].startswith("pinmame.core.")]
		self.assertEqual(1, len(core_sources))
		self.assertIn("machine module p2k", core_sources[0]["locator"])
		self.assertEqual("knowledge/midway/pinball-2000-star-wars-episode-i-1-50-2003.md", definition["knowledge"]["path"])
		self.assertTrue((ROOT / definition["knowledge"]["path"]).is_file())

	def test_rfm_keeps_only_the_authenticated_factory_variant_blocker(self) -> None:
		definition = load_json(RFM_PATH)
		self.assertEqual("bally.revenge-from-mars.1999", definition["machine"]["id"])
		self.assertEqual(RFM_DRIVERS, {driver["id"] for driver in definition["drivers"]})
		self.assertEqual("partial", definition["coverage"]["status"])
		self.assertEqual(["variant_differences"], definition["coverage"]["missing"])
		self.assertEqual("validated", definition["coverage"]["dimensions"]["mechanisms"])
		self.assertEqual("validated", definition["coverage"]["dimensions"]["spatial_placement"])
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
