"""Render the page region an excerpt was transcribed from.

A hand-transcribed excerpt is only checkable by someone holding the source
document. Most of these manuals are not publicly hosted, and at least one
retained PDF has already drifted from the SHA-256 its source record pins, so
its citations can no longer be verified by anyone. Committing the cropped
region the transcription came from closes that gap: the claim and the evidence
for it travel together.

**Resolution is derived, never assumed.** A scanned manual page is one embedded
raster at whatever DPI the scanner produced -- 150, 200, 400, 600, rarely a
round number and essentially never 300. Rendering at a fixed 300 dpi either
upsamples a 200 dpi scan, inventing pixels and tripling the byte cost for no
detail, or downsamples a 600 dpi scan and throws away the fine print this
catalog exists to read. So for a raster page this renders at the embedded
image's own native resolution and stops.

A born-digital page has no native resolution at all -- it is vector text -- so
"native" is meaningless and the question becomes legibility. There the DPI is
chosen from the smallest type actually present on the region being cropped, so
that the smallest glyph lands at a readable pixel height.

Usage:

    python tools/render_excerpt_image.py <pdf> <page> <out.webp> \\
        [--crop x0,y0,x1,y1] [--min-glyph-px N] [--max-width N] [--quality N]

`--crop` is a normalized box in page coordinates: 0,0 is the top-left of the
page and 1,1 the bottom-right. Omit it to render the whole page, which is
rarely what you want -- crop to the table or the drawing being cited.

Prints the `image_derivation` string and the SHA-256 to record on the excerpt.
"""

from __future__ import annotations

import argparse
import hashlib
import io
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image

POINTS_PER_INCH = 72.0
# Below roughly this cap height a scanned glyph stops being reliably readable on
# screen, and this corpus is full of 6pt connector tables that have to be read
# character by character.
DEFAULT_MIN_GLYPH_PIXELS = 11.0
# Past this the file grows faster than the legibility does.
DEFAULT_MAX_WIDTH = 2600


@dataclass(frozen=True)
class PageAnalysis:
	"""What kind of page this is, and therefore what resolution to render it at."""

	kind: str  # "raster" or "vector"
	dpi: float
	detail: str


def _crop_rect(page: fitz.Page, crop: tuple[float, float, float, float] | None) -> fitz.Rect:
	rect = page.rect
	if crop is None:
		return rect
	x0, y0, x1, y1 = crop
	if not (0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
		raise SystemExit(f"crop box must be normalized and ordered, got {crop}")
	return fitz.Rect(
		rect.x0 + x0 * rect.width,
		rect.y0 + y0 * rect.height,
		rect.x0 + x1 * rect.width,
		rect.y0 + y1 * rect.height,
	)


def _native_raster_dpi(page: fitz.Page, region: fitz.Rect) -> tuple[float, str] | None:
	"""The DPI of the embedded scan, or None when the page is not a scan.

	A page can carry several images -- a scan plus a logo, or a figure inside
	otherwise-digital text. The one that matters is whichever actually covers
	the region being cropped, so images are ranked by how much of the region
	they cover and anything covering almost none of it is ignored.
	"""
	best: tuple[float, float, str] | None = None
	for image in page.get_images(full=True):
		xref = image[0]
		try:
			rects = page.get_image_rects(xref)
		except Exception:
			continue
		info = page.parent.extract_image(xref)
		pixel_width = info.get("width") or 0
		if not pixel_width:
			continue
		for rect in rects:
			overlap = rect & region
			if overlap.is_empty:
				continue
			covered = (overlap.width * overlap.height) / max(region.width * region.height, 1e-9)
			if covered < 0.5:
				continue
			# The placed width in points is what maps pixels onto the page.
			dpi = pixel_width / (rect.width / POINTS_PER_INCH)
			detail = f"embedded image xref {xref}, {pixel_width}px across {rect.width / POINTS_PER_INCH:.2f}in"
			if best is None or covered > best[1]:
				best = (dpi, covered, detail)
	if best is None:
		return None
	return best[0], best[2]


def _legible_vector_dpi(page: fitz.Page, region: fitz.Rect, min_glyph_pixels: float) -> tuple[float, str]:
	"""Pick a DPI from the smallest type actually inside the region."""
	sizes: list[float] = []
	for block in page.get_text("dict", clip=region).get("blocks", []):
		for line in block.get("lines", []):
			for span in line.get("spans", []):
				size = float(span.get("size") or 0)
				if size > 0 and (span.get("text") or "").strip():
					sizes.append(size)
	if not sizes:
		# Vector line art with no type: 200 dpi resolves the thinnest rules
		# these schematics use without inflating the file.
		return 200.0, "vector line art, no type in region"
	smallest = min(sizes)
	dpi = min_glyph_pixels * POINTS_PER_INCH / smallest
	return dpi, f"smallest type in region {smallest:.1f}pt, targeting {min_glyph_pixels:.0f}px glyphs"


def analyze(page: fitz.Page, region: fitz.Rect, min_glyph_pixels: float) -> PageAnalysis:
	raster = _native_raster_dpi(page, region)
	if raster is not None:
		dpi, detail = raster
		return PageAnalysis("raster", dpi, f"scanned page rendered at its native resolution ({detail})")
	dpi, detail = _legible_vector_dpi(page, region, min_glyph_pixels)
	return PageAnalysis("vector", dpi, f"born-digital page rendered for legibility ({detail})")


def render(
	pdf_path: Path,
	page_number: int,
	output: Path,
	crop: tuple[float, float, float, float] | None,
	min_glyph_pixels: float,
	max_width: int,
	quality: int,
) -> tuple[str, str]:
	with fitz.open(pdf_path) as document:
		if not 1 <= page_number <= document.page_count:
			raise SystemExit(f"{pdf_path.name} has {document.page_count} pages; asked for {page_number}")
		page = document[page_number - 1]
		region = _crop_rect(page, crop)
		analysis = analyze(page, region, min_glyph_pixels)

		dpi = analysis.dpi
		scale = dpi / POINTS_PER_INCH
		capped = ""
		if region.width * scale > max_width:
			scale = max_width / region.width
			capped = f", capped to {max_width}px wide"
			dpi = scale * POINTS_PER_INCH
		pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=region, alpha=False)
		image = Image.open(io.BytesIO(pixmap.tobytes("png")))

	buffer = io.BytesIO()
	image.save(buffer, format="WEBP", quality=quality, method=6)
	payload = buffer.getvalue()
	output.parent.mkdir(parents=True, exist_ok=True)
	output.write_bytes(payload)

	box = "full page" if crop is None else "crop box " + ",".join(f"{value:g}" for value in crop)
	derivation = (
		f"{pdf_path.name} page {page_number}, {box}, {analysis.detail}, "
		f"rendered at {dpi:.0f} dpi{capped}, {image.width}x{image.height} WebP quality {quality}"
	)
	return derivation, hashlib.sha256(payload).hexdigest()


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("pdf", type=Path)
	parser.add_argument("page", type=int, help="1-based PDF page number")
	parser.add_argument("output", type=Path)
	parser.add_argument("--crop", help="normalized x0,y0,x1,y1 of the page")
	parser.add_argument("--min-glyph-px", type=float, default=DEFAULT_MIN_GLYPH_PIXELS)
	parser.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH)
	parser.add_argument("--quality", type=int, default=80)
	arguments = parser.parse_args()

	crop = None
	if arguments.crop:
		parts = [float(value) for value in arguments.crop.split(",")]
		if len(parts) != 4:
			raise SystemExit("--crop needs four comma-separated numbers")
		crop = (parts[0], parts[1], parts[2], parts[3])

	derivation, digest = render(
		arguments.pdf, arguments.page, arguments.output, crop,
		arguments.min_glyph_px, arguments.max_width, arguments.quality,
	)
	print(f"image            {arguments.output.as_posix()}")
	print(f"image_sha256     {digest}")
	print(f"image_derivation {derivation}")
	print(f"bytes            {arguments.output.stat().st_size:,}")


if __name__ == "__main__":
	main()
