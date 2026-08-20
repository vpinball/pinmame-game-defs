from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from render_excerpt_image import render
from rerender_excerpt_images import _render_options


class ExcerptRenderToolTests(unittest.TestCase):
	def test_render_options_restore_rotation_and_grayscale(self) -> None:
		derivation = "Manual.pdf page 1, full page, rendered at 100 dpi, grayscale, rotated 270 degrees counter-clockwise, 500x800 WebP quality 55"
		self.assertEqual((270, False), _render_options(derivation))

	def test_legacy_render_options_preserve_colour(self) -> None:
		self.assertEqual((0, True), _render_options("Manual.pdf page 1, full page, rendered at 100 dpi"))

	def test_render_applies_rotation_and_grayscale(self) -> None:
		with tempfile.TemporaryDirectory() as directory:
			root = Path(directory)
			pdf = root / "manual.pdf"
			output = root / "excerpt.webp"
			document = fitz.open()
			page = document.new_page(width=200, height=100)
			page.draw_rect(page.rect, color=(1, 0, 0), fill=(1, 0, 0))
			document.save(pdf)
			document.close()

			derivation, _digest = render(pdf, 1, output, None, 11.0, 1000, 80, rotate=90, color=False)
			with Image.open(output) as image:
				self.assertLess(image.width, image.height)
			self.assertIn("grayscale", derivation)
			self.assertIn("rotated 90 degrees counter-clockwise", derivation)


if __name__ == "__main__":
	unittest.main()
