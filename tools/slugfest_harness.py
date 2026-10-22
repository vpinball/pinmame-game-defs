"""Exact, fail-closed service-menu checkpoints read from retained sf_l1 frames.

Only four visually checked menu screens are recognized; no arbitrary DMD OCR,
guessed page counts or inferred switch names are supplied to the harness.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import run_pinmame_harness as harness

TEMPLATES = json.loads((Path(__file__).parent / "seeds/williams/slugfest-l-1-1991-dmd-templates.json").read_text(encoding="utf-8"))


def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
    if (width,height)!=(128,32) or len(frame)!=4096:
        return []
    result=[]
    for title,data in TEMPLATES.items():
        first,last=data["rows"]
        band=bytes(bool(frame[y*width+x]) for y in range(first,last+1) for x in range(width))
        if band==base64.b64decode(data["mask"]):
            result.append(title)
    return result


def dmd_text(recorder: harness.Recorder) -> str:
    with recorder.lock:
        return " ".join(title for index,frame in recorder.display_frames.items()
                        if ((layout:=recorder.display_layouts.get(index,{})).get("type",-1)&31)==14
                        for title in match_titles(frame,layout.get("width",0),layout.get("height",0)))


def check_targets(scenario: dict) -> None:
    for action in scenario.get("actions",[]):
        for target in action.get("texts",[]) if action.get("type")=="pulse_until_display" else []:
            if target not in TEMPLATES or any(target in title for title in TEMPLATES if title!=target):
                raise ValueError(f"unverified or ambiguous SlugFest display target: {target}")


def main() -> int:
    args=harness.build_parser().parse_args()
    if args.game!="sf_l1":
        raise ValueError("templates were verified only against sf_l1")
    if args.scenario:
        check_targets(json.loads(args.scenario.read_text(encoding="utf-8")))
    harness.Recorder.current_display_text=dmd_text
    return harness.main()


if __name__=="__main__":
    raise SystemExit(main())
