"""Which conflicts still count as outstanding work.

This lives in its own module, apart from `validation`, purely so it costs
nothing to import. The author-ready gate needs it, the coverage-consistency
rule needs it, `spatial.fail_closed_spatial_partial()` needs it when it
downgrades a definition to partial, and several curators need it when they
build their blocker reports. Importing it from `validation` drags in
`schema_validation` and therefore `jsonschema`, which made a curator that only
wanted to compute a coverage list fail outright in an environment without it.

There is exactly one implementation on purpose. The first draft had three
curators restating the predicate inline, and every copy fell behind the moment
the real rule started demanding a rationale.
"""

from __future__ import annotations

from typing import Any


def unresolved_conflicts(definition: dict[str, Any]) -> list[dict[str, Any]]:
	"""Conflicts that still need evidence.

	`status` is absent on every record written before the field existed, and
	absent means unresolved: a conflict has to be opted out of blocking
	deliberately, never by omission.

	A stated reason is part of what the state *is*, not a separate schema
	courtesy, so it is checked here rather than only in the schema. Otherwise
	`{"status": "ignored"}` alone lifts the author-ready gate wherever the
	validator runs without a schema pass in front of it, and the one sentence
	that justifies ignoring a real disagreement becomes optional.
	"""
	return [
		conflict
		for conflict in definition.get("conflicts") or []
		if not is_ignored(conflict)
	]


def is_ignored(conflict: Any) -> bool:
	"""A conflict is ignored only if it says so *and* says why.

	The reason has to contain an ASCII letter or digit. Three weaker rules were
	tried and each let a rationale through that renders as nothing: `minLength:
	1` accepts a single space; `.strip()` accepts U+200B ZERO WIDTH SPACE and
	every other invisible Unicode does not classify as whitespace; and
	`str.isalnum()` accepts default-ignorable *letters* such as U+115F HANGUL
	CHOSEONG FILLER, which is a letter to Unicode and zero ink on screen.

	ASCII is deliberate rather than lazy. The schema states the same rule as a
	`pattern`, JSON Schema specifies ECMA-262 regex semantics, and `\\w` is
	Unicode-aware in Python but ASCII-only in ECMAScript -- so a Unicode-class
	rule means two different things depending on which validator runs it. Every
	rationale in this catalog, and the runbook that governs them, is English.
	A rule that is identical in both engines is worth more here than one that
	would accept a rationale written entirely in another script.
	"""
	if not isinstance(conflict, dict) or conflict.get("status") != "ignored":
		return False
	rationale = conflict.get("rationale")
	return isinstance(rationale, str) and any(
		"a" <= character <= "z" or "A" <= character <= "Z" or "0" <= character <= "9"
		for character in rationale
	)
