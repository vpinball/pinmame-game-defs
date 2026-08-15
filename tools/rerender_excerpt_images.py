"""Re-render every committed excerpt crop at a different pixel budget.

The crop box is the expensive part: choosing it means opening the page, finding
the table, and checking the result is legible. The *resolution* is cheap and
mechanical, and `image_derivation` already records the page number and the crop
box for every committed image. So a decision about repository size is fully
reversible: point this at a new `--max-width` and every crop is regenerated
from its own recorded provenance, with no judgement re-exercised.

It only reports by default. Pass `--write` to replace the files, then run each
affected curator's `--regenerate` so the recorded `image_sha256` follows.

    python tools/rerender_excerpt_images.py --max-width 1600
    python tools/rerender_excerpt_images.py --max-width 1600 --write
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from render_excerpt_image import render

DERIVATION = re.compile(
	r"^(?P<pdf>.+?\.pdf) page (?P<page>\d+), "
	r"(?:crop box (?P<crop>[\d.,]+)|full page)"
)


def _manual_roots(repository_root: Path) -> list[Path]:
	working = repository_root.parent / "pinmame-game-defs-working-dir" / "manuals" / "by-machine"
	return [working] if working.is_dir() else []


def _find_pdf(name: str, roots: list[Path], cache: dict[str, Path | None]) -> Path | None:
	if name in cache:
		return cache[name]
	for root in roots:
		for candidate in root.rglob(name):
			cache[name] = candidate
			return candidate
	cache[name] = None
	return None


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--max-width", type=int, required=True)
	parser.add_argument("--quality", type=int, default=80)
	parser.add_argument("--write", action="store_true", help="replace the committed images")
	parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
	arguments = parser.parse_args()

	root = arguments.repository_root.resolve()
	roots = _manual_roots(root)
	if not roots:
		raise SystemExit("no retained manuals directory found; nothing to re-render from")

	cache: dict[str, Path | None] = {}
	before = after = 0
	rendered = skipped = 0
	for definition_path in sorted(root.glob("machines/**/*.json")):
		document = json.loads(definition_path.read_text(encoding="utf-8"))
		for source in document.get("sources") or []:
			for excerpt in source.get("excerpts") or []:
				image = excerpt.get("image")
				derivation = excerpt.get("image_derivation")
				if not image or not derivation:
					continue
				match = DERIVATION.match(derivation)
				target = root / image
				if not match or not target.is_file():
					skipped += 1
					continue
				pdf = _find_pdf(match.group("pdf"), roots, cache)
				if pdf is None:
					print(f"  no PDF for {excerpt['id']}: {match.group('pdf')}")
					skipped += 1
					continue
				crop = None
				if match.group("crop"):
					# The derivation writes "crop box a,b,c,d, scanned page ...",
					# so the captured run keeps a trailing separator.
					parts = [float(value) for value in match.group("crop").split(",") if value.strip()]
					if len(parts) != 4:
						print(f"  unparsable crop box for {excerpt['id']}: {match.group('crop')!r}")
						skipped += 1
						continue
					crop = (parts[0], parts[1], parts[2], parts[3])
				original = target.stat().st_size
				before += original
				destination = target if arguments.write else target.with_suffix(".rerender.tmp")
				new_derivation, digest = render(
					pdf, int(match.group("page")), destination, crop,
					11.0, arguments.max_width, arguments.quality,
				)
				size = destination.stat().st_size
				after += size
				rendered += 1
				if not arguments.write:
					destination.unlink()
				else:
					print(f"  {excerpt['id']}\n    {new_derivation}\n    sha256 {digest}")

	print(f"\n{rendered} re-rendered, {skipped} skipped")
	if rendered:
		print(f"before {before / 1048576:.1f} MB -> after {after / 1048576:.1f} MB "
		      f"({after / max(before, 1) * 100:.0f}%)")
	if not arguments.write:
		print("dry run; pass --write to replace, then re-run each affected curator's --regenerate")


if __name__ == "__main__":
	main()
