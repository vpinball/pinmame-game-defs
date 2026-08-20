"""Bring over-budget table crops back under the size limit.

`tests/test_excerpts.py` allows a page-scale drawing to exceed the ordinary
100 kB budget, because its evidence is spread across callouts that a tighter
crop would drop. Every other crop is a table, where the right answer is fewer
pixels rather than a lower quality that blurs the digits.

This narrows the pixel budget per file until the encoded image fits, keeping the
crop box exactly as chosen, then rewrites the `image_derivation` string wherever
a curator records it so the recorded provenance still describes the file on disk.
Hashes look after themselves: the curators compute `image_sha256` from the bytes.

    python tools/fit_excerpt_images.py            # report only
    python tools/fit_excerpt_images.py --write
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from render_excerpt_image import render
from rerender_excerpt_images import DERIVATION, _find_pdf, _manual_roots, _render_options

# Narrow in steps rather than a true bisection: each render costs a page
# rasterisation, and the first or second step almost always fits.
WIDTH_STEPS = (2200, 1800, 1500, 1200, 1000, 850, 700, 600, 500)


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--limit", type=int, default=100_000)
	parser.add_argument("--write", action="store_true")
	parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
	arguments = parser.parse_args()

	root = arguments.repository_root.resolve()
	import sys
	sys.path.insert(0, str(root / "tests"))
	from test_excerpts import PAGE_SCALE_DRAWINGS

	roots = _manual_roots(root)
	cache: dict[str, Path | None] = {}
	curators = sorted((root / "tools").glob("curate_*.py"))
	curator_text = {path: path.read_text(encoding="utf-8") for path in curators}

	fitted = failed = skipped = 0
	for definition_path in sorted(root.glob("machines/**/*.json")):
		document = json.loads(definition_path.read_text(encoding="utf-8"))
		for source in document.get("sources") or []:
			for excerpt in source.get("excerpts") or []:
				image, derivation = excerpt.get("image"), excerpt.get("image_derivation")
				if not image or not derivation:
					continue
				if excerpt.get("id") in PAGE_SCALE_DRAWINGS:
					continue
				target = root / image
				if not target.is_file() or target.stat().st_size <= arguments.limit:
					continue
				match = DERIVATION.match(derivation)
				pdf = _find_pdf(match.group("pdf"), roots, cache) if match else None
				if pdf is None:
					print(f"  cannot re-derive {excerpt['id']}"); skipped += 1; continue
				crop = None
				if match.group("crop"):
					parts = [float(v) for v in match.group("crop").split(",") if v.strip()]
					crop = tuple(parts) if len(parts) == 4 else None

				original = target.stat().st_size
				rotate, color = _render_options(derivation)
				for width in WIDTH_STEPS:
					new_derivation, _digest = render(
						pdf, int(match.group("page")), target, crop, 11.0, width, 80,
						rotate=rotate, color=color,
					)
					if target.stat().st_size <= arguments.limit:
						break
				size = target.stat().st_size
				if size > arguments.limit:
					print(f"  STILL OVER {excerpt['id']}: {size} bytes"); failed += 1
					continue
				fitted += 1
				print(f"  {original // 1024:4d} -> {size // 1024:3d} kB  {excerpt['id']}")
				for path in curators:
					if derivation in curator_text[path]:
						curator_text[path] = curator_text[path].replace(derivation, new_derivation)

	if arguments.write:
		for path, text in curator_text.items():
			if text != path.read_text(encoding="utf-8"):
				path.write_text(text, encoding="utf-8", newline="")
				print(f"  updated derivation in {path.name}")
	print(f"\n{fitted} fitted, {failed} still over, {skipped} unresolvable")
	if not arguments.write:
		print("images were rewritten; pass --write to also update curator derivation strings")


if __name__ == "__main__":
	main()
