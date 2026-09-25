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


class WpcCustomSwitchWatchTests(unittest.TestCase):
	def test_no_custom_column_is_watched_by_default(self) -> None:
		self.assertEqual([], harness.build_parser().parse_args(REQUIRED).watch_wpc_custom_switch)

	def test_the_whole_custom_column_is_accepted_and_repeatable(self) -> None:
		argv = list(REQUIRED)
		for address in range(121, 129):
			argv += ["--watch-wpc-custom-switch", str(address)]
		self.assertEqual(list(range(121, 129)), harness.build_parser().parse_args(argv).watch_wpc_custom_switch)

	def test_addresses_outside_the_custom_column_are_refused(self) -> None:
		# The ordinary -7..120 envelope stays behind --watch-switch; this option only opens 121-128.
		for value in ("120", "129", "0", "-1", "0x79", "abc"):
			with self.assertRaises(argparse.ArgumentTypeError, msg=value):
				harness._parse_wpc_custom_watch_switch(value)

	def test_non_wpc_generations_are_refused_at_start(self) -> None:
		# WPC-95 (0x80) and WPC-DCS (0x10) are accepted; Whitestar (0x0004000000000), S.A.M.
		# (0x0100000000000) and the first non-WPC bit (0x100) are not.
		harness._require_wpc_generation(0x80)
		harness._require_wpc_generation(0x10)
		for generation in (0, 0x100, 0x0004000000000, 0x0100000000000):
			with self.assertRaises(RuntimeError, msg=hex(generation)):
				harness._require_wpc_generation(generation)

	def test_custom_watches_join_the_list_only_after_the_generation_check(self) -> None:
		class FakeLibrary:
			def __init__(self, generation: int) -> None:
				self.generation = generation

			def PinmameGetHardwareGen(self) -> int:
				return self.generation

		base = (5, 22)
		self.assertEqual(base, harness._with_wpc_custom_watch(FakeLibrary(0), base, []))
		self.assertEqual((5, 22, 121, 123), harness._with_wpc_custom_watch(FakeLibrary(0x10), base, [123, 121]))
		# A refused generation raises instead of returning a list, so run() keeps its ordinary-only
		# watch list for the failure snapshot.
		with self.assertRaises(RuntimeError):
			harness._with_wpc_custom_watch(FakeLibrary(0x0004000000000), base, [121])


if __name__ == "__main__":
	unittest.main()
