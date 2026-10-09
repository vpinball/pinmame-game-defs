"""Exact 128x32 DMD title checkpoints for the Tales from the Crypt US 3.03 ROM.

The generic harness cannot read text from a dot-matrix display, so ``pulse_until_display`` would never
match. This bounded adapter compares the title band of each 128x32 frame against the title bands of
visually read, retained exploratory frames (``tools/tftc_header_templates.json``: the rows a title
occupies, the non-zero-pixel mask of those rows, and the SHA-256 of the source frame). A frame whose title
band matches no template returns empty text, so an unknown screen makes the ordinary harness time out
instead of being guessed at. Everything else about the harness, including isolated state and raw event
capture, is unchanged.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads((Path(__file__).with_name("tftc_header_templates.json")).read_text(encoding="utf-8"))
MASKS = {title: (data["rows"], base64.b64decode(data["mask"])) for title, data in TEMPLATES.items()}


def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
    if (width, height) != (128, 32) or len(frame) != width * height:
        return []
    matches = []
    for title, ((first, last), mask) in MASKS.items():
        band = bytes(1 if frame[y * width + x] else 0 for y in range(first, last + 1) for x in range(width))
        if band == mask:
            matches.append(title)
    return matches


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        titles = [
            title
            for index, frame in recorder.display_frames.items()
            if ((layout := recorder.display_layouts.get(index, {})).get("type", -1) & 31) == 14
            for title in match_titles(frame, layout.get("width", 0), layout.get("height", 0))
        ]
    return " ".join(titles)


def check_targets(scenario: dict) -> None:
    """Refuse a display target that is not exactly one template title, or that is part of another title.

    The generic harness matches a target as a substring of the display text, so a target such as
    ``SWITCH TEST`` would also be satisfied by the ``ACTIVE SWITCH TEST`` screen and checkpoint the wrong test.
    """
    for action in scenario.get("actions", []):
        for target in action.get("texts", []) if action.get("type") == "pulse_until_display" else []:
            if target not in MASKS:
                raise ValueError(f"display target {target!r} is not a verified title template")
            longer = [title for title in MASKS if title != target and target in title]
            if longer:
                raise ValueError(f"display target {target!r} is also part of {longer}, so a substring match could checkpoint the wrong screen")


def main() -> int:
    args = harness.build_parser().parse_args()
    if not args.game.startswith("tftc_"):
        raise ValueError("Header templates are only verified for the tftc_* Tales from the Crypt sets")
    if args.scenario:
        check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    sys.exit(main())
