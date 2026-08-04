"""Promote the original 2010 Iron Man with edition-safe shared-layout evidence."""

from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import file_sha256, write_json, write_text

from curate_iron_man import CANDIDATE_REGISTER_PATH, ORIGINAL_KNOWLEDGE, ORIGINAL_MANUAL_SOURCE, build
from curate_iron_man_vault_spatial import apply_spatial


ROOT = Path(__file__).resolve().parents[1]
PARTIAL_PATH = ROOT / "machines/partial/stern/iron-man-2010.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/iron-man-2010.json"
SHARED_LAYOUT_SOURCE = "human-review.iron-man-original-shared-layout.2026-08-04"


def promote() -> None:
	definition = build(False)
	definition["sources"].append({
		"id": SHARED_LAYOUT_SOURCE,
		"kind": "human_review",
		"uri": "evidence:vpx/source-candidate-register/stern/iron-man-2010.json",
		"sha256": file_sha256(CANDIDATE_REGISTER_PATH),
		"locator": "Edition-safe manual/VPX reconciliation: original manual PDF pages 25-26, Vault maps on pages 17/19/21, the reviewed exact VPW frame, and the 309/419/436-point original-product candidate reports with SHA-256 9ed49e4c58e18d6b0e1cbc18dbc489a3ea42d409cec53d9b85cc678c9f5e639b, 216e555ff20da69526fd08666d672bb690b54a1ab9a5e6df135a316a13b3e9df, and aa21d1e7ac6d0a0e59f4c7b090b737f329b2e27c44d441261f4fcb6b88648f21. Conflicting raw centers such as sw37 are never averaged. Licenses only normalized 2D shared-layout positions; original construction remains controlled by the 2010 parts book, and Z/heights, Vault-only hardware, and renderer helpers remain excluded.",
		"license": "NOASSERTION",
		"attribution": "Human review of official Stern manuals and user-authorized VPX evidence",
		"acquired_at": "2026-08-04T00:00:00Z",
	})
	definition["schema_version"] = 2
	definition["coverage"]["status"] = "author_ready"
	definition["coverage"]["missing"] = []
	definition["coverage"]["dimensions"]["spatial_placement"] = "validated"
	apply_spatial(
		definition,
		geometry_source=SHARED_LAYOUT_SOURCE,
		manual_source=ORIGINAL_MANUAL_SOURCE,
		projection_source=SHARED_LAYOUT_SOURCE,
		product_label="Iron Man 2010",
		preserve_existing_gi_construction=True,
	)
	write_json(AUTHOR_READY_PATH, definition)
	write_text(ROOT / "knowledge/stern/iron-man-2010.md", ORIGINAL_KNOWLEDGE)
	if PARTIAL_PATH.exists():
		PARTIAL_PATH.unlink()


if __name__ == "__main__":
	promote()
