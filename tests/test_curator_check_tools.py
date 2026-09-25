from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from pinmame_game_defs.workspace import resolve_working_root

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TOOLS = ROOT / "tools"
WORKING_ROOT = resolve_working_root(ROOT)
PINMAME_CHECKOUT = WORKING_ROOT / "source-checkouts" / "pinmame"
OPDB_SNAPSHOT = WORKING_ROOT / "review-artifacts" / "opdb-import" / "latest-opdb.json"


def run_tool_process(script: str, *args: str, environment_overrides: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
	import sys

	import os

	environment = dict(os.environ)
	environment["PYTHONPATH"] = os.pathsep.join([str(SRC), environment.get("PYTHONPATH", "")])
	if environment_overrides:
		environment.update(environment_overrides)
	return subprocess.run(
		[sys.executable, "-B", str(TOOLS / script), *args],
		cwd=ROOT,
		capture_output=True,
		text=True,
		env=environment,
	)


def run_tool(script: str, *args: str) -> str:
	completed = run_tool_process(script, *args)
	if completed.returncode != 0:
		raise AssertionError(f"{script} {args} failed:\n{completed.stdout}\n{completed.stderr}")
	return completed.stdout.strip()


class DeterministicCuratorCheckTests(unittest.TestCase):
	def test_promotion_template_preserves_order_and_requires_a_controller_for_omission(self) -> None:
		import sys

		sys.path.insert(0, str(TOOLS))
		import promote_catalog_stubs as tool

		expected = tool.expected_missing(True)
		without_platform = [requirement for requirement in expected if requirement != "controller_platform"]
		self.assertTrue(tool.coverage_missing_matches(expected, resolved=True, has_controller=False))
		self.assertTrue(tool.coverage_missing_matches(without_platform, resolved=True, has_controller=True))
		self.assertFalse(tool.coverage_missing_matches(without_platform, resolved=True, has_controller=False))
		self.assertFalse(tool.coverage_missing_matches(list(reversed(expected)), resolved=True, has_controller=False))

	def test_override_aware_identity_note_does_not_claim_plain_agreement(self) -> None:
		import sys

		sys.path.insert(0, str(TOOLS))
		import promote_catalog_stubs as tool

		record = {"commonName": None, "ipdbId": 1, "manufactureDate": "1980-01-01", "manufacturer": {"name": "Other"}, "name": "Game"}
		note = tool.note_identity_line(True, None, "GGAME-MGAME", record, "Reviewed manufacturer exception.")
		self.assertIn("machine-specific exception", note)
		self.assertIn("Reviewed manufacturer exception.", note)
		self.assertNotIn("agreement of the PinMAME catalog", note)
		self.assertTrue(tool.has_exactly_one_identity_basis(note))
		self.assertFalse(tool.has_exactly_one_identity_basis(note + "\n  agreement of the PinMAME catalog and this reviewed mapping."))
		self.assertTrue(tool.has_exactly_one_identity_basis("catalog do not agree on identity, so identity is unresolved"))
		self.assertTrue(tool.has_exactly_one_identity_basis("identity is unresolved: OPDB record shared with another machine"))
		shared_note = tool.note_shared_identity_line("GGAME-MGAME", record, "maker.game.1980")
		self.assertIn("OPDB record shared with maker.game.1980", shared_note)
		self.assertTrue(tool.has_exactly_one_identity_basis(shared_note))

	def test_promotion_structural_check_passes_without_external_evidence(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			completed = run_tool_process(
				"promote_catalog_stubs.py",
				"--check-structure",
				environment_overrides={"PINMAME_WORKING_ROOT": temporary_directory},
			)
		self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
		output = completed.stdout.strip()
		self.assertIn("structural check OK:", output)
		# Kingpin and Elvira and the Party Monsters left the bulk-promoted set when they were curated on 2026-09-25, and Firepower took four records out of it
		# (its own partial and the three Oliver residuals).
		self.assertEqual(659, int(output.split("structural check OK: ")[1].split(" ")[0]))

	def test_promotion_identity_check_passes_with_the_retained_snapshot(self) -> None:
		if not OPDB_SNAPSHOT.is_file():
			self.skipTest("retained OPDB snapshot is not available")
		output = run_tool("promote_catalog_stubs.py", "--check")
		self.assertIn("check OK:", output)
		self.assertEqual(659, int(output.split("check OK: ")[1].split(" ")[0]))

	def test_promotion_check_fails_closed_without_the_retained_snapshot(self) -> None:
		with tempfile.TemporaryDirectory() as temporary_directory:
			completed = run_tool_process("promote_catalog_stubs.py", "--check", environment_overrides={"PINMAME_WORKING_ROOT": temporary_directory})
		self.assertNotEqual(0, completed.returncode)
		self.assertIn("Retained OPDB snapshot is missing", completed.stdout + completed.stderr)

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
