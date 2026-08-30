from __future__ import annotations

import unittest

from pinmame_game_defs.vpx_source import extract_vpx_file, strip_trailing_comment


class StripTrailingCommentTests(unittest.TestCase):
	def test_live_lines_keep_their_code(self) -> None:
		self.assertEqual("NFadeL 14, l14", strip_trailing_comment("  NFadeL 14, l14 'check balltrough").lstrip())
		self.assertEqual('Sub SW12_Hit:Controller.Switch(12)=1 : playsoundAtVol"rollover" , ActiveBall, 1: End Sub', strip_trailing_comment('Sub SW12_Hit:Controller.Switch(12)=1 : playsoundAtVol"rollover" , ActiveBall, 1: End Sub'))
		self.assertEqual("x = 1", strip_trailing_comment("x = 1"))

	def test_quotes_protect_comment_characters(self) -> None:
		# The apostrophe inside the quoted string is real (not collapsed by
		# adjacent-string concatenation), so a naive split-on-quote would
		# truncate the live code; the quote-aware stripper must not.
		line = 'x = "it' + chr(39) + 's live" ' + chr(39) + ' dead comment'
		stripped = strip_trailing_comment(line)
		self.assertEqual('x = "it' + chr(39) + 's live"', stripped)
		self.assertNotEqual(line.split("'")[0].rstrip(), stripped)

	def test_the_whole_line_can_be_a_comment(self) -> None:
		self.assertEqual("", strip_trailing_comment("  ' SetLamp 106, Controller.Lamp(6)"))
		self.assertEqual("", strip_trailing_comment("':vpmTimer.PulseSw 62 no idea"))


class CommentLineExtractionTests(unittest.TestCase):
	def _catalog(self) -> dict[str, dict[str, object]]:
		return {"drivers": [{"id": "test_10", "machine_id": "m"}]}

	def _extract(self, text: str) -> dict[str, object]:
		import tempfile
		from pathlib import Path

		with tempfile.NamedTemporaryFile("w", suffix=".vbs", delete=False, encoding="utf-8") as stream:
			stream.write(text)
			path = Path(stream.name)
		try:
			return extract_vpx_file(path, path.parent, "rev", "https://example.test", self._catalog(), (text, "utf-8"))
		finally:
			path.unlink(missing_ok=True)

	def test_trailing_comments_never_become_candidates(self) -> None:
		text = "\n".join(
			[
				"Sub Table1_Init",
				"  NFadeL 14, l14 'check balltrough",
				"End Sub",
				"Sub Table1_KeyDown",
				"  'in this sub you may add a switch, for example Controller.Switch(14) = 1",
				"End Sub",
				"Sub Table1_Exit",
				"  ':vpmTimer.PulseSw 62 no idea",
				"End Sub",
			]
		)
		evidence = self._extract(text)
		addresses = {(candidate["group"], candidate["address"]) for candidate in evidence["switches"]}
		self.assertNotIn(("pinmame.input.switch", 14), addresses)
		self.assertNotIn(("pinmame.input.switch", 62), addresses)
		lamps = [candidate for candidate in evidence["outputs"] if candidate["address"] == 14]
		self.assertEqual(1, len(lamps))

	def test_quoted_comment_characters_stay_live(self) -> None:
		text = 'Sub Table1_Init\n  SolCallback(1) = "vpmSolSound ""Jet3""", \'Sol1\nEnd Sub\n'
		evidence = self._extract(text)
		self.assertEqual(1, len(evidence["outputs"]))


	def test_mid_identifier_slicing_never_produces_candidates(self) -> None:
		# Round-13 blocker: CONST_ASSIGNMENT_PATTERN without an anchor sliced
		# `SssVol` into `sVol`. The lookbehind must keep the whole identifier.
		text = "Const SssVol = 1\n"
		evidence = self._extract(text)
		symbols = [candidate["symbol"] for candidate in evidence["outputs"]]
		self.assertNotIn("sVol", symbols)
		self.assertNotIn("SssVol", symbols)  # lowercase `s`+lowercase is not Hungarian
		self.assertEqual([], evidence["outputs"])


if __name__ == "__main__":
	unittest.main()
