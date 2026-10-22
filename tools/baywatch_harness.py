"""Exact, visually verified 192x64 Portals checkpoints for Baywatch USA 4.00.

Masks come from retained exploratory PGM frames; unknown screens return no text. Menus use the
whole selected screen, live tests only their invariant title band. This is a bounded adapter to
the standard runner, not general DMD OCR. Raw evidence retains the original probe adapter too.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
import zlib

import run_pinmame_harness as harness

TEMPLATES=json.loads(Path(__file__).with_name("baywatch_header_templates.json").read_text(encoding="utf-8"))
MASKS={name:(tuple(t["box"]),zlib.decompress(base64.b64decode(t["mask_zlib"]))) for name,t in TEMPLATES.items()}


def match_titles(frame,width,height):
    if (width,height)!=(192,64) or len(frame)!=192*64:return []
    return [name for name,((x0,y0,x1,y1),mask) in MASKS.items()
            if bytes(bool(frame[y*192+x]) for y in range(y0,y1) for x in range(x0,x1))==mask]


def dmd_text(recorder):
    with recorder.lock:
        return " ".join(name for index,frame in recorder.display_frames.items()
                        for layout in [recorder.display_layouts.get(index,{})]
                        for name in match_titles(frame,layout.get("width"),layout.get("height")))


def check_targets(scenario):
    for action in scenario.get("actions",[]):
        if action["type"]!="pulse_until_display":continue
        for target in action["texts"]:
            if target not in MASKS or any(target in other for other in MASKS if other!=target):
                raise ValueError(f"not a unique verified Baywatch checkpoint: {target}")


def main():
    args=harness.build_parser().parse_args()
    if args.game!="baywatch":raise ValueError("These templates were verified only with Baywatch USA 4.00")
    if args.scenario:check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text=dmd_text
    return harness.main()


if __name__=="__main__":raise SystemExit(main())
