"""Delegate Spider-Man (Stern 2007) generation to the spatial curator.

The spatial curator owns the canonical artifact once the exact working table has
been reviewed.  Keeping this base entry point as a guarded delegate prevents a
later address-only regeneration from clobbering reviewed placements.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
AUTHOR_READY_PATH = ROOT / "machines/author-ready/stern/spider-man-2007.json"


def refuse_if_canonical_definition_exists(path: Path = AUTHOR_READY_PATH) -> None:
	if path.exists():
		raise RuntimeError(
			f"Refusing to regenerate {path}: author-ready canonical definition already exists; "
			"use the spatial promotion path only after resolving the existing artifact."
		)


def main() -> None:
	refuse_if_canonical_definition_exists()
	if str(TOOLS) not in sys.path:
		sys.path.insert(0, str(TOOLS))
	from curate_spiderman_spatial import promote

	promote()


if __name__ == "__main__":
	main()
