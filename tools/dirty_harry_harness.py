"""Fail-closed DMD title checkpoints for the Dirty Harry LX-2 service menus.

Every mask comes from a visually read retained exploratory frame. Only menu
title bands are decoded; no switch/device label is guessed by OCR.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import run_pinmame_harness as harness

HEADERS = Path(__file__).with_name("seeds") / "williams/dirty-harry-1995-dmd-headers.json"
TEMPLATES = json.loads(HEADERS.read_text(encoding="utf-8"))

def match_titles(frame: bytes | list[int], width: int, height: int) -> list[str]:
	if (width,height)!=(128,32) or len(frame)!=4096: return []
	matches=[]
	for title, data in TEMPLATES.items():
		first,last=data["rows"]
		mask=bytes(int(bool(v)) for v in frame[first*128:(last+1)*128])
		if mask==base64.b64decode(data["mask"]): matches.append(title)
	return matches

def dmd_text(recorder: harness.Recorder) -> str:
	with recorder.lock:
		return " ".join(title for index,frame in recorder.display_frames.items()
			if ((layout:=recorder.display_layouts.get(index,{})).get("type",-1)&31)==14
			for title in match_titles(frame,layout.get("width",0),layout.get("height",0)))

def main() -> int:
	args=harness.build_parser().parse_args()
	if args.game!="dh_lx2": raise ValueError("Dirty Harry header masks verified only against dh_lx2")
	if args.scenario:
		for action in json.loads(args.scenario.read_text(encoding="utf-8"))["actions"]:
			for target in action.get("texts",[]):
				if target not in TEMPLATES or any(target in other for other in TEMPLATES if other!=target):
					raise ValueError(f"Unverified or ambiguous Dirty Harry title target: {target}")
	harness.Recorder.current_display_text=dmd_text
	return harness.main()

if __name__=="__main__": raise SystemExit(main())
