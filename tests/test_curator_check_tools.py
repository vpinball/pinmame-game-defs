from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TOOLS = ROOT / "tools"
WORKING_ROOT = ROOT.parent / "pinmame-game-defs-working-dir"
PINMAME_CHECKOUT = WORKING_ROOT / "source-checkouts" / "pinmame"


def run_tool(script: str, *args: str) -> str:
	import sys

	import os

	environment = dict(os.environ)
	environment["PYTHONPATH"] = os.pathsep.join([str(SRC), environment.get("PYTHONPATH", "")])
	completed = subprocess.run(
		[sys.executable, "-B", str(TOOLS / script), *args],
		cwd=ROOT,
		capture_output=True,
		text=True,
		env=environment,
	)
	if completed.returncode != 0:
		raise AssertionError(f"{script} {args} failed:\n{completed.stdout}\n{completed.stderr}")
	return completed.stdout.strip()


class DeterministicCuratorCheckTests(unittest.TestCase):
	def test_promotion_check_passes_on_the_committed_tree(self) -> None:
		output = run_tool("promote_catalog_stubs.py", "--check")
		self.assertIn("check OK:", output)
		self.assertGreaterEqual(int(output.split("check OK: ")[1].split(" ")[0]), 500)

	def test_pinmame_attachment_check_passes_on_the_committed_tree(self) -> None:
		if not (PINMAME_CHECKOUT / "src" / "wpc").is_dir():
			self.skipTest("pinned PinMAME checkout is not available")
		output = run_tool("attach_pinmame_io.py", "--check")
		self.assertIn("check OK:", output)
		self.assertGreaterEqual(int(output.split("check OK: ")[1].split(" ")[0]), 100)


if __name__ == "__main__":
	unittest.main()
