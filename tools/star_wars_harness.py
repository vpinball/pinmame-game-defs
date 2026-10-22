"""Exact DMD title checkpoints visually read on Star Wars CPU 1.03 / display 1.05.

Each template pins a retained frame and a literal nonzero-pixel mask. Unknown
frames return no title; navigation fails rather than guessing a page number.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads(Path(__file__).with_name("star_wars_header_templates.json").read_text(encoding="utf-8"))


def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
    if (width, height) != (128, 32) or len(frame) != 4096:
        return []
    matches = []
    for title, data in TEMPLATES.items():
        first, last = data["rows"]
        left, right = data.get("cols", [0, 127])
        band = bytes(bool(frame[y * width + x]) for y in range(first, last + 1)
                     for x in range(left, right + 1))
        if band == base64.b64decode(data["mask"]):
            matches.append(title)
    return matches


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        titles = []
        for index, frame in recorder.display_frames.items():
            layout = recorder.display_layouts.get(index, {})
            if layout.get("type", -1) & 31 == 14:
                titles.extend(match_titles(frame, layout.get("width", 0), layout.get("height", 0)))
    return " ".join(titles)


def check_targets(scenario: dict) -> None:
    for action in scenario.get("actions", []):
        if action.get("type") != "pulse_until_display":
            continue
        for target in action.get("texts", []):
            if target not in TEMPLATES or any(target in t for t in TEMPLATES if t != target):
                raise ValueError(f"not an unambiguous, visually verified title: {target!r}")


def main() -> int:
    args = harness.build_parser().parse_args()
    if args.game != "stwr_103":
        raise ValueError("Title templates are only verified on stwr_103 CPU 1.03 / display 1.05")
    if args.scenario:
        check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    raise SystemExit(main())
