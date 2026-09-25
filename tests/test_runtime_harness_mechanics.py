from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_pinmame_harness as harness  # noqa: E402


REQUIRED = ["--library", "x.dll", "--game", "mb_10", "--rom-path", "roms", "--work-dir", "state"]


class HandleMechanicsOptionTests(unittest.TestCase):
	def test_built_in_mechs_stay_disabled_by_default(self) -> None:
		args = harness.build_parser().parse_args(REQUIRED)
		self.assertEqual(0, args.handle_mechanics)

	def test_the_mask_accepts_decimal_and_hex_like_a_vpx_script(self) -> None:
		parser = harness.build_parser()
		self.assertEqual(4, parser.parse_args(REQUIRED + ["--handle-mechanics", "4"]).handle_mechanics)
		self.assertEqual(7, parser.parse_args(REQUIRED + ["--handle-mechanics", "0x7"]).handle_mechanics)

	def test_masks_outside_the_five_built_in_mechs_are_refused(self) -> None:
		for value in ("-1", "32", "0x20", "256"):
			with self.assertRaises(argparse.ArgumentTypeError, msg=value):
				harness._mechanics_mask(value)
		self.assertEqual(0x1F, harness._mechanics_mask("0x1f"))


if __name__ == "__main__":
	unittest.main()
