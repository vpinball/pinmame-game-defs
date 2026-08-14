"""Guards the `ignored` conflict state.

An ignored conflict is a real disagreement that cannot reach a recreation. It
stays in the record so a reader can account for the `conflicted` provenance it
explains, and it does not gate author readiness. Two properties matter and both
are easy to lose:

- **Absent means unresolved.** A conflict must be opted out of blocking
  deliberately, never by a missing field, or every record written before the
  state existed silently stops counting.
- **An ignored conflict needs a stated reason.** Without one the state is just a
  way to make a blocker disappear.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from pinmame_game_defs.validation import validate_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _conflict(**overrides):
	base = {
		"id": "conflict.example",
		"path": "/inputs/switch.matrix-15",
		"description": "Two sources disagree about this address.",
		"source_refs": ["manual.example", "pinmame.core.example"],
	}
	base.update(overrides)
	return base


class IgnoredConflictStateTests(unittest.TestCase):
	def test_absent_status_is_unresolved(self) -> None:
		from pinmame_game_defs.validation import _unresolved_conflicts

		definition = {"conflicts": [_conflict()]}
		self.assertEqual(1, len(_unresolved_conflicts(definition)))

	def test_ignored_is_not_unresolved(self) -> None:
		from pinmame_game_defs.validation import _unresolved_conflicts

		definition = {"conflicts": [_conflict(status="ignored", rationale="Cannot reach a recreation.")]}
		self.assertEqual([], _unresolved_conflicts(definition))

	def test_explicit_unresolved_still_counts(self) -> None:
		from pinmame_game_defs.validation import _unresolved_conflicts

		definition = {"conflicts": [_conflict(status="unresolved")]}
		self.assertEqual(1, len(_unresolved_conflicts(definition)))

	def test_ignored_without_a_usable_reason_still_counts(self) -> None:
		"""The reason is what the state *is*; without one, nothing is opted out.

		The schema's conditional covers a missing key, but the validator also
		runs where no schema pass precedes it, and `minLength: 1` accepts a
		single space. Each of these would otherwise lift the author-ready gate
		on an assertion nobody justified.
		"""
		from pinmame_game_defs.validation import _unresolved_conflicts

		# U+200B and U+FEFF are not whitespace to Unicode, so `.strip()` keeps
		# them and the reason renders as nothing.
		for rationale in (None, "", " ", "\n\t ", "\u200b", "\u200b \ufeff", 42, [], {"why": "because"}):
			with self.subTest(rationale=rationale):
				conflict = _conflict(status="ignored")
				if rationale is not None:
					conflict["rationale"] = rationale
				definition = {"conflicts": [conflict]}
				self.assertEqual(
					1,
					len(_unresolved_conflicts(definition)),
					"an ignored conflict with no stated reason must keep counting as unresolved",
				)


class CommittedRecordTests(unittest.TestCase):
	"""The state as it is actually used across the catalog."""

	@classmethod
	def setUpClass(cls) -> None:
		cls.conflicts = []
		for path in sorted(REPOSITORY_ROOT.glob("machines/**/*.json")):
			document = json.loads(path.read_text(encoding="utf-8"))
			for conflict in document.get("conflicts") or []:
				cls.conflicts.append((path, document, conflict))

	def test_every_ignored_conflict_states_a_reason(self) -> None:
		for path, _document, conflict in self.conflicts:
			if conflict.get("status") == "ignored":
				with self.subTest(path=path.name, conflict=conflict["id"]):
					self.assertTrue(
						(conflict.get("rationale") or "").strip(),
						"an ignored conflict must say why the answer cannot reach a recreation",
					)

	def test_status_is_only_ever_a_known_value(self) -> None:
		for path, _document, conflict in self.conflicts:
			if "status" in conflict:
				with self.subTest(path=path.name, conflict=conflict["id"]):
					self.assertIn(conflict["status"], {"unresolved", "ignored"})

	def test_no_definition_claims_a_blocker_it_does_not_have(self) -> None:
		"""`unresolved_conflicts` costs real completion score; it must be earned.

		This asks the validator's own function rather than restating the rule.
		A second copy drifts: it would have gone on accepting a bare
		`status: "ignored"` after the real one started demanding a rationale.
		"""
		from pinmame_game_defs.validation import _unresolved_conflicts

		for path in sorted(REPOSITORY_ROOT.glob("machines/**/*.json")):
			document = json.loads(path.read_text(encoding="utf-8"))
			missing = document.get("coverage", {}).get("missing") or []
			if "unresolved_conflicts" not in missing:
				continue
			with self.subTest(path=path.name):
				self.assertTrue(
					_unresolved_conflicts(document),
					"lists unresolved_conflicts but every conflict is ignored or absent",
				)


class ValidatorGateTests(unittest.TestCase):
	"""The gate itself, exercised through the real validator."""

	def _author_ready_definition(self):
		for path in sorted(REPOSITORY_ROOT.glob("machines/author-ready/**/*.json")):
			return path, json.loads(path.read_text(encoding="utf-8"))
		self.skipTest("no author-ready definition available")

	def test_an_unresolved_conflict_blocks_author_ready(self) -> None:
		from pinmame_game_defs.validation import validate_machine

		_path, definition = self._author_ready_definition()
		candidate = copy.deepcopy(definition)
		candidate["conflicts"] = [_conflict()]
		errors = validate_machine(candidate)
		self.assertTrue(
			any("unresolved conflicts" in str(error) for error in errors),
			"an unresolved conflict must keep a definition out of author-ready",
		)

	def test_an_ignored_conflict_does_not_block_author_ready(self) -> None:
		from pinmame_game_defs.validation import validate_machine

		_path, definition = self._author_ready_definition()
		candidate = copy.deepcopy(definition)
		candidate["conflicts"] = [_conflict(status="ignored", rationale="Cannot reach a recreation.")]
		errors = validate_machine(candidate)
		self.assertFalse(
			any("unresolved conflicts" in str(error) for error in errors),
			"an ignored conflict must not gate author readiness",
		)

	def test_a_bare_ignored_status_does_not_open_the_gate(self) -> None:
		"""`validate_machine` runs with no schema pass in front of it here."""
		from pinmame_game_defs.validation import validate_machine

		_path, definition = self._author_ready_definition()
		for rationale in (None, "   "):
			with self.subTest(rationale=rationale):
				candidate = copy.deepcopy(definition)
				conflict = _conflict(status="ignored")
				if rationale is not None:
					conflict["rationale"] = rationale
				candidate["conflicts"] = [conflict]
				errors = validate_machine(candidate)
				self.assertTrue(
					any("unresolved conflicts" in str(error) for error in errors),
					"ignoring without a stated reason must not lift the author-ready gate",
				)

	def test_claiming_a_blocker_every_conflict_has_opted_out_of_is_rejected(self) -> None:
		"""Exercises the validator rule, not just today's corpus.

		The committed-record audit above passes whether or not this rule
		exists — deleting the rule leaves every current file consistent — so
		without this the guard could be removed and nothing would notice.
		"""
		from pinmame_game_defs.validation import validate_machine

		_path, definition = self._author_ready_definition()
		candidate = copy.deepcopy(definition)
		candidate["coverage"]["status"] = "partial"
		candidate["coverage"]["missing"] = ["unresolved_conflicts"]
		candidate["conflicts"] = [_conflict(status="ignored", rationale="Cannot reach a recreation.")]
		errors = validate_machine(candidate)
		self.assertTrue(
			any("every conflict is ignored" in str(error) for error in errors),
			"claiming unresolved_conflicts while every conflict is ignored must be rejected",
		)

		# The same definition with a real conflict is the state the rule allows.
		candidate["conflicts"].append(_conflict(id="conflict.second"))
		self.assertFalse(
			any("every conflict is ignored" in str(error) for error in validate_machine(candidate)),
			"one unresolved conflict is enough to earn the claim",
		)

	def test_the_schema_rejects_a_rationale_that_says_nothing(self) -> None:
		"""The other half of the same rule, at the schema layer."""
		from jsonschema import Draft202012Validator

		schema = json.loads((REPOSITORY_ROOT / "schemas" / "machine.schema.json").read_text(encoding="utf-8"))
		conflict_schema = dict(schema["$defs"]["conflict"])
		conflict_schema["$defs"] = schema["$defs"]
		validator = Draft202012Validator(conflict_schema)

		self.assertTrue(
			list(validator.iter_errors(_conflict(status="ignored"))),
			"an ignored conflict with no rationale must fail the schema",
		)
		for rationale in ("", " ", "\n\t ", "\u200b", "\u200b \ufeff"):
			with self.subTest(rationale=rationale):
				self.assertTrue(
					list(validator.iter_errors(_conflict(status="ignored", rationale=rationale))),
					"a blank rationale must fail the schema",
				)
		self.assertEqual(
			[],
			list(validator.iter_errors(_conflict(status="ignored", rationale="Cannot reach a recreation."))),
			"a real rationale must pass",
		)

	def test_repository_validates(self) -> None:
		self.assertEqual([], validate_repository(REPOSITORY_ROOT))


if __name__ == "__main__":
	unittest.main()
