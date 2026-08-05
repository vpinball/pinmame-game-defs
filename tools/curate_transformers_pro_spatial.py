"""Record the evidence-backed, fail-closed Transformers Pro spatial disposition."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[1]
for import_root in (ROOT / "src", TOOLS):
	if str(import_root) not in sys.path:
		sys.path.insert(0, str(import_root))

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from pinmame_game_defs.spatial import SPATIAL_RETROFIT_PENDING_MACHINE_IDS
from curate_transformers import curated_pro_knowledge, curated_pro_partial
from transformers_pro_spatial_evidence import (
	CANDIDATE_REGISTER_RELATIVE_PATH,
	MACHINE_ID,
	build_candidate_register,
	load_candidate_register,
	spatial_review_disposition,
)


def promote(root: Path = ROOT) -> None:
	"""Write the deterministic partial while refusing an unsupported promotion."""
	if MACHINE_ID not in SPATIAL_RETROFIT_PENDING_MACHINE_IDS:
		raise RuntimeError(f"Refusing spatial disposition for a machine no longer pending: {MACHINE_ID}")
	author_ready_path = root / "machines/author-ready/stern/transformers-pro-2011.json"
	if author_ready_path.exists():
		raise RuntimeError(f"Refusing to overwrite author-ready definition: {author_ready_path}")
	spatial_review_disposition(root)
	definition = curated_pro_partial(root)
	knowledge = curated_pro_knowledge(root)
	write_json(root / "machines/partial/stern/transformers-pro-2011.json", definition)
	write_text(root / "knowledge/stern/transformers-pro-2011.md", knowledge)


def write_candidate_register(source_root: Path, root: Path = ROOT) -> None:
	"""Write the portable register from the retained exact table and VPXTool extraction."""
	write_json(root / CANDIDATE_REGISTER_RELATIVE_PATH, build_candidate_register(source_root))


def check(root: Path = ROOT) -> None:
	"""Refuse drift in the portable candidate record and its generated partial outputs."""
	load_candidate_register(root)
	spatial_review_disposition(root)
	definition_path = root / "machines/partial/stern/transformers-pro-2011.json"
	knowledge_path = root / "knowledge/stern/transformers-pro-2011.md"
	if not definition_path.is_file() or not knowledge_path.is_file():
		raise RuntimeError("Transformers Pro spatial outputs are missing")
	if canonical_bytes(load_json(definition_path)) != canonical_bytes(curated_pro_partial(root)):
		raise RuntimeError(f"Transformers Pro partial definition drifted: {definition_path}")
	if knowledge_path.read_text(encoding="utf-8") != curated_pro_knowledge(root):
		raise RuntimeError(f"Transformers Pro knowledge note drifted: {knowledge_path}")


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="verify the committed register and generated partial outputs")
	parser.add_argument("--write-candidate-register", action="store_true", help="rebuild the committed register from PINMAME_VPX_SOURCES_ROOT")
	args = parser.parse_args()
	if args.check and args.write_candidate_register:
		raise RuntimeError("--check and --write-candidate-register cannot be combined")
	if args.write_candidate_register:
		source_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
		if not source_root:
			raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to rebuild the Transformers Pro candidate register")
		write_candidate_register(Path(source_root))
		return
	if args.check:
		check()
		return
	promote()


if __name__ == "__main__":
	main()
