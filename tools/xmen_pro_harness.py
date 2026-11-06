"""Exact, fail-closed X-Men Pro V1.51 DMD service-title checkpoints."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads((Path(__file__).parent / "seeds/stern/x-men-pro-2012-dmd-headers.json").read_text(encoding="utf-8"))


def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
    if (width, height) != (128, 32) or len(frame) != 4096:
        return []
    matches = []
    for title, record in TEMPLATES.items():
        first, last = record["rows"]
        left, right = record["columns"]
        mask = bytes(bool(frame[y * width + x]) for y in range(first, last + 1) for x in range(left, right))
        if mask == base64.b64decode(record["mask"]):
            matches.append(title)
    return matches


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        return " ".join(
            title
            for index, frame in recorder.display_frames.items()
            if ((layout := recorder.display_layouts.get(index, {})).get("type", -1) & 31) == 14
            for title in match_titles(frame, layout.get("width", 0), layout.get("height", 0))
        )


def check_targets(scenario: dict) -> None:
    for action in scenario.get("actions", []):
        if action.get("type") != "pulse_until_display":
            continue
        for target in action["texts"]:
            if target not in TEMPLATES or any(target in title for title in TEMPLATES if title != target):
                raise ValueError(f"unverified or ambiguous display checkpoint {target!r}")


def main() -> int:
    args = harness.build_parser().parse_args()
    if args.game != "xmn_151":
        raise ValueError("title masks are verified only for exact Pro xmn_151 V1.51")
    if args.scenario:
        check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text = dmd_text
    return harness.main()


if __name__ == "__main__":
    sys.exit(main())
