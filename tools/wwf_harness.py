"""Exact, visually reviewed DMD checkpoints for the three production WWF ROMs.

Only title recognition changes. Unknown screens return no match. A direct host
switch write remains a stimulus, never an observation of a physical contact.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads(Path(__file__).with_name("wwf_header_templates.json").read_text(encoding="utf-8"))
MASKS = {title: (data["rows"], base64.b64decode(data["mask"])) for title, data in TEMPLATES.items()}
GAMES = {"wwfr_106", "wwfr_103", "wwfr_103f"}


def match_titles(frame, width, height):
    if (width, height) != (128, 32) or len(frame) != 4096:
        return []
    return [title for title, ((first, last), mask) in MASKS.items()
            if bytes(bool(frame[y * width + x]) for y in range(first, last + 1)
                     for x in range(width)) == mask]


def dmd_text(recorder):
    with recorder.lock:
        return " ".join(title for index, frame in recorder.display_frames.items()
                        if ((layout := recorder.display_layouts.get(index, {})).get("type", -1) & 31) == 14
                        for title in match_titles(frame, layout.get("width", 0), layout.get("height", 0)))


def check_targets(scenario):
    for action in scenario.get("actions", []):
        if action.get("type") != "pulse_until_display":
            continue
        for target in action.get("texts", []):
            if target not in MASKS or any(target in title for title in MASKS if title != target):
                raise ValueError(f"Ambiguous or unverified WWF display target: {target!r}")


def main():
    args = harness.build_parser().parse_args()
    if args.game not in GAMES:
        raise ValueError("These templates are verified only for the three production WWF drivers")
    if args.scenario:
        check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    raise SystemExit(main())
