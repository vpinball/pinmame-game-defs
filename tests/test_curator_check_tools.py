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

	def test_pinmame_attachment_dry_runs_execute(self) -> None:
		# Round-5 blocker: the tool's write path crashed on an unpack error that
		# --check never exercised. Both dry-run modes must execute cleanly.
		if not (PINMAME_CHECKOUT / "src" / "wpc").is_dir():
			self.skipTest("pinned PinMAME checkout is not available")
		attach = run_tool("attach_pinmame_io.py", "--dry-run")
		self.assertIn("attached:", attach)
		sanitized = run_tool("attach_pinmame_io.py", "--sanitize-defines", "--dry-run")
		self.assertIn("sanitized:", sanitized)

	def test_vpx_attachment_dry_run_executes(self) -> None:
		output = run_tool("attach_vpx_script_io.py", "--dry-run")
		self.assertIn("attached:", output)

	def test_vpx_attachment_sanitize_dry_run_reproduces_the_committed_counts(self) -> None:
		# The --sanitize mode produces the committed data; its dry run must
		# report exactly the totals recorded in the attachment tests.
		from test_vpx_script_io_attachment import EXPECTED_ATTACHED_DEVICES, EXPECTED_ATTACHED_MACHINES, EXPECTED_ATTACHED_SCRIPTS

		output = run_tool("attach_vpx_script_io.py", "--sanitize", "--dry-run")
		self.assertIn(f"{EXPECTED_ATTACHED_MACHINES} machines with devices", output)
		self.assertIn(f"{EXPECTED_ATTACHED_DEVICES} devices from {EXPECTED_ATTACHED_SCRIPTS} scripts", output)


if __name__ == "__main__":
	unittest.main()
