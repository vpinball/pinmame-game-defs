from __future__ import annotations

import os
from pathlib import Path

from .errors import DefinitionError


WORKING_ROOT_ENVIRONMENT_VARIABLE = "PINMAME_WORKING_ROOT"
WORKING_ROOT_DIRECTORY_NAME = "pinmame-game-defs-working-dir"


def resolve_working_root(repository_root: Path, *, required: bool = False) -> Path:
	"""Resolve the shared evidence root from a checkout or nested git worktree."""
	override = os.environ.get(WORKING_ROOT_ENVIRONMENT_VARIABLE, "").strip()
	if override:
		working_root = Path(override).expanduser().resolve()
	else:
		repository_root = repository_root.resolve()
		working_root = repository_root.parent / WORKING_ROOT_DIRECTORY_NAME
		for ancestor in (repository_root, *repository_root.parents):
			if ancestor.name == WORKING_ROOT_DIRECTORY_NAME and ancestor.is_dir():
				working_root = ancestor
				break
			candidate = ancestor / WORKING_ROOT_DIRECTORY_NAME
			if candidate.is_dir():
				working_root = candidate
				break
	if required and not working_root.is_dir():
		raise DefinitionError(
			f"Shared working root is missing: {working_root}. "
			f"Set {WORKING_ROOT_ENVIRONMENT_VARIABLE} to its absolute path."
		)
	return working_root
