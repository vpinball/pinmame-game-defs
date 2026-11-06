"""Game-neutral readers for retained System 11 alphanumeric harness traces.

The shared segment glyphs use O/0 and S/5 for identical patterns.  Bit 15 is
the period; the ROM's narrow numeral 1 is 0x0006.  These functions interpret
display evidence and never infer physical fitment from an output transition.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from run_pinmame_harness import SEGMENT_16_CHARACTERS


def decode_alpha(values: list[int]) -> str:
	text = []
	for value in values:
		glyph = "1" if value & 0x7FFF == 0x0006 else SEGMENT_16_CHARACTERS.get(value & 0x7FFF)
		text.append(("?" if value & 0x7FFF else " ") if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def frame_digest(*rows: list[int]) -> str:
	return hashlib.sha256(json.dumps([list(row) for row in rows], separators=(",", ":")).encode("ascii")).hexdigest()


def row_timeline(run: dict[str, Any], index: int) -> list[tuple[float, list[int]]]:
	return [(event["time_s"], event["segments"]) for event in run["events"]
			if event["event"] == "display" and event.get("index") == index and isinstance(event.get("segments"), list)]


def frame_at(timeline: list[tuple[float, list[int]]], time: float) -> list[int]:
	current: list[int] = []
	for at, segments in timeline:
		if at > time:
			break
		current = segments
	return current


def longest_frame(timeline: list[tuple[float, list[int]]], start: float, end: float) -> list[int]:
	"""Pick the longest-displayed frame in [start,end); ties keep the earliest."""
	durations: dict[str, float] = {}
	frames: dict[str, list[int]] = {}

	def add(segments: list[int], seconds: float) -> None:
		key = json.dumps(segments)
		frames.setdefault(key, segments)
		durations[key] = durations.get(key, 0.0) + seconds

	current, at = frame_at(timeline, start), start
	for when, segments in timeline:
		if when <= start:
			continue
		if when >= end:
			break
		add(current, when - at)
		current, at = segments, when
	add(current, end - at)
	return frames[max(durations, key=durations.__getitem__)]


def service_pulses(run: dict[str, Any]) -> int:
	return sum(1 if step.get("type") == "pulse" else step.get("pulses", 0)
			   for step in run["steps"] if step.get("switch") == -7 and step.get("type") in ("pulse", "pulse_until_display"))


def checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
			for step in run["steps"] if step.get("type") == "pulse_until_display"]
