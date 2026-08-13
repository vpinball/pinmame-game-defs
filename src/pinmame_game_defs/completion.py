from __future__ import annotations

from collections.abc import Iterable


# These are the authoring requirements represented by coverage.missing today.
# Keep this list stable and explicit: adding a requirement changes every partial
# machine's score and therefore requires a reviewed catalog migration.
AUTHOR_READY_REQUIREMENTS = frozenset(
	{
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
		"unresolved_conflicts",
	}
)


def completion_score(status: str, missing: Iterable[str]) -> int:
	"""Return deterministic progress toward author readiness as an integer percent.

	The lifecycle status remains authoritative. Stubs deliberately receive no
	credit and author-ready definitions are complete by definition. A partial's
	score is the share of the fixed authoring requirements absent from its
	``coverage.missing`` list.
	"""
	missing_list = list(missing)
	missing_set = set(missing_list)
	if len(missing_list) != len(missing_set):
		raise ValueError("coverage.missing must not contain duplicates")
	unknown = missing_set - AUTHOR_READY_REQUIREMENTS
	if unknown:
		raise ValueError(f"Unknown authoring requirements: {', '.join(sorted(unknown))}")
	if status == "stub":
		return 0
	if status == "author_ready":
		if missing_set:
			raise ValueError("author-ready definitions cannot have missing requirements")
		return 100
	if status != "partial":
		raise ValueError(f"Unknown coverage status: {status!r}")
	if not missing_set:
		raise ValueError("partial definitions must have missing requirements")
	completed = len(AUTHOR_READY_REQUIREMENTS - missing_set)
	total = len(AUTHOR_READY_REQUIREMENTS)
	return (completed * 100 + total // 2) // total
