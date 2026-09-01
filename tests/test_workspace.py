from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinmame_game_defs.errors import DefinitionError
from pinmame_game_defs.workspace import resolve_working_root


class WorkingRootTests(unittest.TestCase):
	def test_resolves_sibling_root_from_primary_checkout(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory, patch.dict(os.environ, {}, clear=True):
			parent = Path(temporary_directory)
			repository = parent / "pinmame-game-defs"
			working_root = parent / "pinmame-game-defs-working-dir"
			repository.mkdir()
			working_root.mkdir()
			self.assertEqual(working_root.resolve(), resolve_working_root(repository, required=True))

	def test_resolves_shared_root_from_nested_worktree(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory, patch.dict(os.environ, {}, clear=True):
			working_root = Path(temporary_directory) / "pinmame-game-defs-working-dir"
			repository = working_root / "worktrees" / "pinmame-game-defs-example"
			repository.mkdir(parents=True)
			self.assertEqual(working_root.resolve(), resolve_working_root(repository, required=True))

	def test_resolves_shared_root_from_deeply_nested_checkout(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory, patch.dict(os.environ, {}, clear=True):
			working_root = Path(temporary_directory) / "pinmame-game-defs-working-dir"
			repository = working_root / "worktrees" / "group" / "pinmame-game-defs-example"
			repository.mkdir(parents=True)
			self.assertEqual(working_root.resolve(), resolve_working_root(repository, required=True))

	def test_environment_override_takes_precedence(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			parent = Path(temporary_directory)
			repository = parent / "checkout"
			override = parent / "evidence"
			repository.mkdir()
			override.mkdir()
			with patch.dict(os.environ, {"PINMAME_WORKING_ROOT": str(override)}, clear=True):
				self.assertEqual(override.resolve(), resolve_working_root(repository, required=True))

	def test_required_root_fails_closed(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory, patch.dict(os.environ, {}, clear=True):
			repository = Path(temporary_directory) / "checkout"
			repository.mkdir()
			with self.assertRaisesRegex(DefinitionError, "Shared working root is missing"):
				resolve_working_root(repository, required=True)


if __name__ == "__main__":
	unittest.main()
