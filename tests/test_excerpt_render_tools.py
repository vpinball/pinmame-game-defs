from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf as fitz
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

	def test_a_finer_mask_sets_the_native_resolution_of_a_mixed_raster_page(self) -> None:
		"""A mixed-raster scan draws its line art through a mask finer than its background image."""
		import io

		from render_excerpt_image import analyze

		with tempfile.TemporaryDirectory() as directory:
			pdf = Path(directory) / "manual.pdf"

			def png(width: int, mode: str) -> bytes:
				buffer = io.BytesIO()
				Image.new(mode, (width, width), 128).save(buffer, format="PNG")
				return buffer.getvalue()

			document = fitz.open()
			page = document.new_page(width=144, height=144)
			# A 2 x 2 inch page: a 50 px background (25 dpi) drawn through a 200 px mask (100 dpi).
			page.insert_image(page.rect, stream=png(50, "RGB"), mask=png(200, "L"))
			document.save(pdf)
			document.close()
			with fitz.open(pdf) as reopened:
				result = analyze(reopened[0], reopened[0].rect, 11.0)
			self.assertEqual("raster", result.kind)
			self.assertAlmostEqual(100.0, result.dpi, places=3)
			self.assertIn("200px /SMask over a 50px background", result.detail)

	def test_a_placeholder_pixel_does_not_set_the_resolution_but_a_masked_one_does(self) -> None:
		"""A 1 px fill laid over a stencil scan is ignored; a 1 px background drawn through a fine mask is the scan."""
		import io

		from render_excerpt_image import analyze

		def png(width: int, mode: str) -> bytes:
			buffer = io.BytesIO()
			Image.new(mode, (width, width), 128).save(buffer, format="PNG")
			return buffer.getvalue()

		with tempfile.TemporaryDirectory() as directory:
			pdf = Path(directory) / "manual.pdf"
			document = fitz.open()
			page = document.new_page(width=152, height=152)
			# A 300 px scan placed 2 inches wide, under a 1 px placeholder stretched a little wider, so the
			# placeholder covers more of the crop (as on The Sopranos manual's location drawings).
			page.insert_image(fitz.Rect(4, 4, 148, 148), stream=png(300, "L"))
			page.insert_image(fitz.Rect(3, 3, 149, 149), stream=png(1, "L"))
			document.save(pdf)
			document.close()
			with fitz.open(pdf) as reopened:
				result = analyze(reopened[0], reopened[0].rect, 11.0)
			self.assertEqual("raster", result.kind)
			self.assertAlmostEqual(150.0, result.dpi, places=3)

			masked = Path(directory) / "masked.pdf"
			document = fitz.open()
			page = document.new_page(width=144, height=144)
			# A 1 px background drawn through a 600 px soft mask: the mask is a 300 dpi scan.
			page.insert_image(page.rect, stream=png(1, "RGB"), mask=png(600, "L"))
			document.save(masked)
			document.close()
			with fitz.open(masked) as reopened:
				result = analyze(reopened[0], reopened[0].rect, 11.0)
			self.assertEqual("raster", result.kind)
			self.assertAlmostEqual(300.0, result.dpi, places=3)

	def test_a_colour_key_mask_is_not_mistaken_for_a_raster(self) -> None:
		"""A /Mask can reference a colour-key array; it has no Width, so the image's own resolution stands."""
		import io

		from render_excerpt_image import analyze

		with tempfile.TemporaryDirectory() as directory:
			pdf = Path(directory) / "manual.pdf"
			buffer = io.BytesIO()
			Image.new("RGB", (50, 50), 128).save(buffer, format="PNG")
			document = fitz.open()
			page = document.new_page(width=144, height=144)
			page.insert_image(page.rect, stream=buffer.getvalue())
			image_xref = page.get_images(full=True)[0][0]
			key_xref = document.get_new_xref()
			document.update_object(key_xref, "[0 0 0 0 0 0]")
			document.xref_set_key(image_xref, "Mask", f"{key_xref} 0 R")
			document.save(pdf)
			document.close()
			with fitz.open(pdf) as reopened:
				result = analyze(reopened[0], reopened[0].rect, 11.0)
			self.assertAlmostEqual(25.0, result.dpi, places=3)
			self.assertNotIn("/Mask", result.detail)


if __name__ == "__main__":
	unittest.main()
