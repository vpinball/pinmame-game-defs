#!/usr/bin/env python3
"""Render an evidence excerpt crop and emit its source-record fragment.

An excerpt has two halves. The transcription is written by hand, because reading a schematic is the
part that needs judgement and is exactly the step a curator must not skip. This tool does the other
half: it renders the region the transcription came from, so a reader can look at the page without
holding the document, and it prints the JSON fragment to paste into the source record.

Crops are for facts that are *drawings*. A printed table belongs in the transcription, where it is
diffable and greppable and costs a kilobyte; rendering it as an image costs forty times that and
cannot be searched. Reach for a crop when the fact is schematic wiring, a connector fan-out or an
insert map - something prose cannot carry faithfully.

The crop is deliberately not thresholded to 1-bit. Printed shading carries meaning on some machines
- the shaded opto rows of a Williams switch matrix are the obvious case - and flattening it would
destroy evidence. Grayscale is the compromise: it keeps shading while costing far less than colour.

Legibility matters more than bytes, but a crop is a reading aid and not an archive, so the tool
refuses anything over 100 kB by default. Scanned line art compresses badly whatever is done to it,
so the way back under the limit is normally a tighter crop - one block, not one page - rather than a
lower quality that makes the text unreadable.

Some pages genuinely need more. A colour playfield insert map or a lamp-location drawing can carry
meaning in the colours themselves, and downsampling it to a legible grayscale costs more than the
budget allows. Pass ``--color`` and raise ``--max-bytes`` for those, and say in the excerpt why the
exception was needed. It should stay an exception: a handful per project, not per machine.

Usage:

    python tools/make_excerpt.py \\
        --pdf <manual.pdf> --page 52 \\
        --box 0.185,0.455,0.335,0.720 \\
        --out evidence/excerpts/bally.kiss.1979/a5-connector-functions.webp \\
        --id excerpt.kiss.a5-connector-functions \\
        --locator "PDF page 52, LAMP DRIVER A5 connector block"

``--rotate`` rotates the rendered page counter-clockwise before cropping. ``--box`` is
left,top,right,bottom as fractions of that oriented page, which keeps the call readable and
independent of the render resolution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DPI = 300
DEFAULT_WIDTH = 1000
DEFAULT_QUALITY = 75
MAX_BYTES = 100_000


def find_pdftoppm() -> str:
	# Prefer a real executable over command-wrapper shims, which do not reliably preserve
	# quoted Windows paths when invoked through subprocess without a shell. The explicit legacy
	# path remains a fallback for contributors whose Poppler installation is not on PATH.
	for candidate in ("pdftoppm.exe", "pdftoppm", r"C:\Tools\poppler-23.05.0\Library\bin\pdftoppm.exe"):
		resolved = shutil.which(candidate) or (candidate if Path(candidate).is_file() else None)
		if not resolved:
			continue
		try:
			probe = subprocess.run([resolved, "-v"], check=False, capture_output=True, timeout=5)
		except (OSError, subprocess.TimeoutExpired):
			continue
		if probe.returncode == 0:
			return resolved
	raise SystemExit("no usable pdftoppm found; install Poppler or put a working executable on PATH")


def sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with open(path, "rb") as handle:
		for chunk in iter(lambda: handle.read(1 << 20), b""):
			digest.update(chunk)
	return digest.hexdigest()


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--pdf", required=True, type=Path)
	parser.add_argument("--page", required=True, type=int)
	parser.add_argument("--box", required=True, help="left,top,right,bottom as page fractions")
	parser.add_argument("--rotate", type=int, choices=(0, 90, 180, 270), default=0,
	                    help="counter-clockwise page rotation before cropping")
	parser.add_argument("--out", required=True, type=Path, help="repository-relative .webp path")
	parser.add_argument("--id", required=True)
	parser.add_argument("--locator", required=True)
	parser.add_argument("--transcription", type=Path, help="the .md transcription this crop accompanies")
	parser.add_argument("--dpi", type=int, default=DEFAULT_DPI)
	parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="output width in pixels")
	parser.add_argument("--quality", type=int, default=DEFAULT_QUALITY, help="WebP quality; use --lossless for shading-critical pages")
	parser.add_argument("--lossless", action="store_true", help="lossless WebP, for pages where subtle shading is the evidence")
	parser.add_argument("--color", action="store_true", help="keep colour; the exception, for pages where colour carries meaning such as an insert map")
	parser.add_argument("--max-bytes", type=int, default=MAX_BYTES, help=f"size ceiling, default {MAX_BYTES}; raise it only for a genuine colour exception")
	args = parser.parse_args()

	try:
		from PIL import Image
	except ImportError:
		raise SystemExit("Pillow is required: python -m pip install pillow")

	left, top, right, bottom = (float(v) for v in args.box.split(","))
	if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
		raise SystemExit("--box must be 0 <= left < right <= 1 and 0 <= top < bottom <= 1")

	with tempfile.TemporaryDirectory() as work:
		stem = Path(work) / "page"
		subprocess.run(
			[find_pdftoppm(), "-png", "-r", str(args.dpi), "-f", str(args.page), "-l", str(args.page),
			 str(args.pdf), str(stem)],
			check=True, capture_output=True,
		)
		rendered = sorted(Path(work).glob("page*.png"))
		if not rendered:
			raise SystemExit(f"pdftoppm produced no output for page {args.page}")
		# Copy out of the lazy file handle so the temporary directory can be removed on Windows.
		with Image.open(rendered[0]) as handle:
			page = handle.copy()
	if args.rotate:
		page = page.rotate(args.rotate, expand=True)

	width, height = page.size
	crop = page.crop((int(left * width), int(top * height), int(right * width), int(bottom * height)))
	scaled_height = max(1, round(crop.size[1] * args.width / crop.size[0]))
	crop = (crop if args.color else crop.convert("L")).resize((args.width, scaled_height), Image.LANCZOS)

	out = (ROOT / args.out) if not args.out.is_absolute() else args.out
	out.parent.mkdir(parents=True, exist_ok=True)
	if args.lossless:
		crop.save(out, "WEBP", lossless=True, method=6)
	else:
		crop.save(out, "WEBP", quality=args.quality, method=6)

	record: dict[str, object] = {
		"id": args.id,
		"locator": args.locator,
		"image": args.out.as_posix(),
		"image_sha256": sha256(out),
		"image_derivation": (
			f"{args.pdf.name} page {args.page}, crop box {args.box} of the page, rendered at "
			f"{args.dpi} dpi with pdftoppm"
			f"{f', rotated {args.rotate} degrees counter-clockwise' if args.rotate else ''}, "
			f"reduced to {args.width}px wide "
			f"{'colour' if args.color else 'grayscale'}, "
			f"{'lossless' if args.lossless else f'quality {args.quality}'} WebP"
		),
	}
	if args.transcription:
		record["path"] = args.transcription.as_posix()
		transcription = (ROOT / args.transcription) if not args.transcription.is_absolute() else args.transcription
		if transcription.is_file():
			record["sha256"] = sha256(transcription)

	size = out.stat().st_size
	if size > args.max_bytes:
		out.unlink()
		raise SystemExit(
			f"crop is {size} bytes, over the {args.max_bytes} byte limit. Tighten --box to the block "
			f"you actually cite, or lower --width; do not drop --quality far enough to blur the text. "
			f"If this is a colour page whose colours carry meaning, pass --color and raise "
			f"--max-bytes, and record why in the excerpt."
		)

	print(f"wrote {out.relative_to(ROOT).as_posix() if out.is_relative_to(ROOT) else out} "
	      f"({size} bytes, {crop.size[0]}x{crop.size[1]})", file=sys.stderr)
	print(json.dumps(record, indent=2))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
