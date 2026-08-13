from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path

from pinmame_game_defs.completion import AUTHOR_READY_REQUIREMENTS, completion_score
from pinmame_game_defs.jsonio import load_json
from pinmame_game_defs.validation import validate_catalog

ROOT = Path(__file__).resolve().parents[1]


class CompletionScoreTests(unittest.TestCase):
	def test_status_endpoints_are_absolute(self) -> None:
		self.assertEqual(0, completion_score("stub", AUTHOR_READY_REQUIREMENTS))
		self.assertEqual(100, completion_score("author_ready", []))

	def test_partial_score_is_share_of_satisfied_requirements(self) -> None:
		self.assertEqual(94, completion_score("partial", ["spatial_placement"]))
		self.assertEqual(88, completion_score("partial", ["polarity", "unresolved_conflicts"]))
		self.assertEqual(75, completion_score("partial", ["polarity", "spatial_placement", "unresolved_conflicts", "variant_differences"]))
		self.assertEqual(13, completion_score("partial", sorted(AUTHOR_READY_REQUIREMENTS - {"identity", "controller_platform"})))

	def test_requirement_set_matches_machine_schema(self) -> None:
		schema = load_json(ROOT / "schemas" / "machine.schema.json")
		schema_requirements = schema["$defs"]["coverage"]["properties"]["missing"]["items"]["enum"]
		self.assertEqual(AUTHOR_READY_REQUIREMENTS, frozenset(schema_requirements))

	def test_invalid_inputs_fail_closed(self) -> None:
		with self.assertRaisesRegex(ValueError, "must have missing"):
			completion_score("partial", [])
		with self.assertRaisesRegex(ValueError, "cannot have missing"):
			completion_score("author_ready", ["spatial_placement"])
		with self.assertRaisesRegex(ValueError, "Unknown authoring requirements"):
			completion_score("partial", ["not-a-requirement"])
		with self.assertRaisesRegex(ValueError, "duplicates"):
			completion_score("partial", ["polarity", "polarity"])

	def test_catalog_scores_are_reproducible_from_machine_coverage(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		for machine in catalog["machines"]:
			definition = load_json(ROOT / machine["definition"])
			coverage = definition["coverage"]
			self.assertEqual(
				completion_score(coverage["status"], coverage["missing"]),
				machine["completion_score"],
				machine["id"],
			)

	def test_known_machine_scores_distinguish_near_complete_from_imported(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		by_id = {machine["id"]: machine for machine in catalog["machines"]}
		self.assertEqual(100, by_id["williams.medieval-madness.1997"]["completion_score"])
		self.assertEqual(94, by_id["williams.white-water.1993"]["completion_score"])
		self.assertEqual(88, by_id["williams.monster-bash.1998"]["completion_score"])
		self.assertEqual(75, by_id["stern.lord-of-the-rings.2003"]["completion_score"])
		self.assertEqual(19, by_id["data-east.guns-n-roses.1994"]["completion_score"])
		self.assertEqual(0, by_id["stub.pinmame.bbh_170"]["completion_score"])

	def test_repository_validation_rejects_a_hand_edited_score(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		mutated = deepcopy(catalog)
		machine = next(machine for machine in mutated["machines"] if machine["coverage_status"] == "partial")
		machine["completion_score"] -= 1
		errors = validate_catalog(mutated, ROOT)
		self.assertTrue(any("completion_score" in error and "from definition coverage" in error for error in errors), errors)

	def test_repository_validation_rejects_hand_edited_missing_requirements(self) -> None:
		catalog = load_json(ROOT / "catalog" / "pinmame.json")
		mutated = deepcopy(catalog)
		machine = next(machine for machine in mutated["machines"] if len(machine["missing"]) > 1)
		machine["missing"] = machine["missing"][:-1]
		errors = validate_catalog(mutated, ROOT)
		self.assertTrue(any(".missing: does not match definition" in error for error in errors), errors)


if __name__ == "__main__":
	unittest.main()
