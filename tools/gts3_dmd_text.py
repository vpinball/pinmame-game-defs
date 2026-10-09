"""Read the text of a Gottlieb System 3 DMD frame that the runtime harness saved as a PGM.

The harness writes each 128x32 DMD snapshot as a binary PGM whose levels are the ROM's raw dot
intensities. Any lit dot is ink: the frame is binarized, split into text bands (runs of rows that hold
lit dots), each band into glyphs (runs of columns that hold lit dots), and each glyph is looked up by
its exact bit pattern in a committed glyph table. A gap of four or more blank columns in the 7-dot font,
or three in the 5-dot font, is a space; narrower gaps sit inside a word, around the narrow numeral 1.

Two folds follow the ROM's fonts rather than guess: each font draws 0 and O with one glyph, so the
number field after a colon (``SOLENOID:12``) and a glyph next to a digit read as 0; and a straight
double quote is drawn as two single ticks, which read as ``"``. The Lamp Matrix and Switch Edges tests
number 100-117 as A0-B7, which ``test_number`` converts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


GLYPH_TABLE_PATH = Path(__file__).resolve().parent / "seeds" / "gottlieb" / "stargate-1995-dmd-glyphs.json"


def load_glyphs(path: Path = GLYPH_TABLE_PATH) -> dict[str, str]:
	return json.loads(path.read_text(encoding="utf-8"))["glyphs"]


def read_pgm(data: bytes) -> tuple[int, int, bytes]:
	"""Parse a binary PGM: magic, width, height and maxval, then exactly one whitespace byte before the raster.

	The raster is raw levels, so a level of 9, 10, 13 or 32 is a pixel, not a separator.
	"""
	tokens: list[bytes] = []
	position = 0
	end = len(data)
	while len(tokens) < 4:
		while position < end and data[position:position + 1].isspace():
			position += 1
		start = position
		while position < end and not data[position:position + 1].isspace():
			position += 1
		if position >= end:
			raise ValueError("truncated PGM header")
		tokens.append(data[start:position])
	if tokens[0] != b"P5":
		raise ValueError("not a binary PGM")
	width, height = int(tokens[1]), int(tokens[2])
	raster = data[position + 1:position + 1 + width * height]
	if len(raster) != width * height:
		raise ValueError("truncated PGM raster")
	return width, height, raster


def binarize(data: bytes) -> list[list[int]]:
	width, height, pixels = read_pgm(data)
	return [[1 if pixels[y * width + x] else 0 for x in range(width)] for y in range(height)]


def _bands(grid: list[list[int]]) -> list[tuple[int, int]]:
	rows = [any(row) for row in grid]
	bands = []
	y = 0
	while y < len(rows):
		if rows[y]:
			start = y
			while y < len(rows) and rows[y]:
				y += 1
			bands.append((start, y))
		else:
			y += 1
	return bands


def glyph_key(grid: list[list[int]], y0: int, y1: int, x0: int, x1: int) -> str:
	bits = "".join(str(grid[y][x]) for y in range(y0, y1) for x in range(x0, x1))
	return f"{x1 - x0}x{y1 - y0}:{int(bits, 2):x}"


def segment(grid: list[list[int]]) -> list[list[str]]:
	"""Each text band as a list of glyph keys, with " " for a word gap."""
	lines = []
	width = len(grid[0]) if grid else 0
	for y0, y1 in _bands(grid):
		gap_limit = 4 if y1 - y0 >= 7 else 3
		columns = [any(grid[y][x] for y in range(y0, y1)) for x in range(width)]
		glyphs: list[str] = []
		x = 0
		last_end: int | None = None
		while x < width:
			if columns[x]:
				start = x
				while x < width and columns[x]:
					x += 1
				if last_end is not None and start - last_end >= gap_limit:
					glyphs.append(" ")
				glyphs.append(glyph_key(grid, y0, y1, start, x))
				last_end = x
			else:
				x += 1
		lines.append(glyphs)
	return lines


def _number_field(text: str) -> str:
	head, separator, tail = text.partition(":")
	if not separator or not tail.strip():
		return text
	folded = tail.replace(" ", "").replace("O", "0")
	if folded.isdigit() or re.fullmatch(r"[AB][0-7]", folded):
		return head + separator + folded
	return text


def _tidy(text: str) -> str:
	text = text.replace("''", '"')
	return re.sub(r"(?<=\d)O|O(?=\d)", "0", text)


def decode(data: bytes, glyphs: dict[str, str]) -> list[str]:
	"""The text lines of one frame, top to bottom; an unknown glyph reads as "?"."""
	lines = []
	for keys in segment(binarize(data)):
		text = "".join(key if key == " " else glyphs.get(key, "?") for key in keys)
		lines.append(_tidy(_number_field(text)))
	return lines


def test_number(field: str) -> int:
	"""A Lamp Matrix or Switch Edges number as the public address: A0-A7 are 100-107, B0-B7 are 110-117."""
	if field[:1] == "A":
		return 100 + int(field[1:])
	if field[:1] == "B":
		return 110 + int(field[1:])
	return int(field)


def labelled(lines: list[str], label: str) -> tuple[int, str] | None:
	"""Find ``LABEL:nn`` and return the number and the next line (the ROM's name for it)."""
	for index, line in enumerate(lines):
		if line.startswith(label + ":"):
			name = lines[index + 1] if index + 1 < len(lines) else ""
			return test_number(line.split(":", 1)[1]), name
	return None


def describe(data: bytes, glyphs: dict[str, Any] | None = None) -> str:
	return " / ".join(decode(data, glyphs if glyphs is not None else load_glyphs()))


if __name__ == "__main__":
	import sys

	table = load_glyphs()
	for argument in sys.argv[1:]:
		print(Path(argument).name, "|", describe(Path(argument).read_bytes(), table))
