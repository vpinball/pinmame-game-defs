#!/usr/bin/env python3
"""Run a PinMAME ROM in an isolated, scriptable evidence harness.

The harness never writes beside the supplied ROMs. PinMAME's mutable NVRAM,
configuration, and high-score paths are redirected below ``--work-dir``. Its
JSON output records injected switch pulses, output transitions, display
layouts, and state snapshots so a curation decision can cite a repeatable run.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator


PINMAME_MAX_PATH = 512
PINMAME_FILE_TYPE_ROMS = 0
PINMAME_FILE_TYPE_NVRAM = 1
PINMAME_FILE_TYPE_SAMPLES = 2
PINMAME_FILE_TYPE_CONFIG = 3
PINMAME_FILE_TYPE_HIGHSCORE = 4
PINMAME_STATUS_OK = 0
SEGMENT_16_DISPLAY_TYPES = {0, 1, 16, 17}
MAX_DMD_EVENTS_PER_DISPLAY = 256
SCENARIO_FORMAT = "pinmame-harness-scenario"
SCENARIO_VERSION = 1
SCENARIO_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "harness-scenario.schema.json"
# Behavior-changing P2K ball/switch-model inputs retained in run provenance.
# Debug logging, trap, forwarding, map-dump, and performance-only variables are intentionally excluded.
P2K_DEBUG_ENVIRONMENT_NAMES = (
	"P2K_BALLSAT",
	"P2K_DOORCLOSE",
	"P2K_DRAIN",
	"P2K_HANDPLUNGE",
	"P2K_HITLEN",
	"P2K_HITRATE",
	"P2K_LANEHOLD",
	"P2K_NAMES",
	"P2K_PLAY",
	"P2K_PLAYFIELD",
	"P2K_PLAYHOLD",
	"P2K_SWSWEEP",
	"P2K_SWSWEEPAT",
	"P2K_SWWATCH",
	"P2K_TROUGH",
)
# Values are pinned to src/libpinmame/libpinmame.h's PINMAME_KEYCODE enum.
# The Data East service bindings are corroborated by src/wpc/s11.h DE_COMPORTS:
# Green=KEYCODE_7, Black=KEYCODE_8; flippers come from src/wpc/core.h CORE_PORTS
# at the CORE_FLIPINPORT index. The Pinball 2000 bindings follow src/wpc/p2k.c's
# input_ports_rfm declaration and its measured diagnostic-button ordering.
KEY_ALIASES = {
	"balls_in_trough": 1,
	"service_escape": 26,
	"start": 27,
	"coin_1": 31,
	"service_green": 33,
	"service_enter": 33,
	"service_black": 34,
	"service_up": 34,
	"service_down": 35,
	"launch": 66,
	"coin_door": 78,
	"left_flipper": 93,
	"right_flipper": 94,
	"left_action": 95,
	"right_action": 96,
}
MIN_SAFE_PUBLIC_SWITCH = -7
MAX_SAFE_PUBLIC_SWITCH = 120

# PinMAME's regular 16-segment patterns (core_ascii2seg16). Some ROMs use
# bespoke animation glyphs; those remain visible as ``?`` while ordinary
# diagnostic text is made directly searchable in harness evidence.
SEGMENT_16_CHARACTERS = {
	0x0000: " ",
	0x0309: "!",
	0x0220: '"',
	0x2A4E: "#",
	0x2A6D: "$",
	0x6E65: "%",
	0x135D: "&",
	0x0400: "'",
	0x1400: "(",
	0x4100: ")",
	0x7F40: "*",
	0x2A40: "+",
	0x0080: ",",
	0x0840: "-",
	0x0008: ".",
	0x4400: "/",
	0x443F: "0",
	0x2200: "1",
	0x085B: "2",
	0x084F: "3",
	0x0866: "4",
	0x087D: "6",
	0x0007: "7",
	0x087F: "8",
	0x086F: "9",
	0x0009: ":",
	0x4001: ";",
	0x4408: "<",
	0x0848: "=",
	0x1108: ">",
	0x2803: "?",
	0x205F: "@",
	0x0877: "A",
	0x2A0F: "B",
	0x0039: "C",
	0x220F: "D",
	0x0079: "E",
	0x0071: "F",
	0x083D: "G",
	0x0876: "H",
	0x2209: "I",
	0x001E: "J",
	0x1470: "K",
	0x0038: "L",
	0x0536: "M",
	0x1136: "N",
	0x003F: "O",
	0x0873: "P",
	0x103F: "Q",
	0x1873: "R",
	0x086D: "S",  # Electrically identical to the digit 5.
	0x2201: "T",
	0x003E: "U",
	0x4430: "V",
	0x5036: "W",
	0x5500: "X",
	0x2500: "Y",
	0x4409: "Z",
	0x1100: "\\",
	0x000F: "]",
	0x5000: "^",
}


def _decode_segment_frame(display_type: int, frame: list[int]) -> str | None:
	if (display_type & 0x1F) not in SEGMENT_16_DISPLAY_TYPES:
		return None
	return "".join(SEGMENT_16_CHARACTERS.get(value, "?") for value in frame)


class PinmameDisplayLayout(ctypes.Structure):
	_fields_ = [
		("type", ctypes.c_int),
		("top", ctypes.c_int32),
		("left", ctypes.c_int32),
		("length", ctypes.c_int32),
		("width", ctypes.c_int32),
		("height", ctypes.c_int32),
		("depth", ctypes.c_int32),
	]


class PinmameAudioInfo(ctypes.Structure):
	_fields_ = [
		("format", ctypes.c_int),
		("channels", ctypes.c_int),
		("sampleRate", ctypes.c_double),
		("framesPerSecond", ctypes.c_double),
		("samplesPerFrame", ctypes.c_int),
		("bufferSize", ctypes.c_int),
	]


class PinmameSolenoidState(ctypes.Structure):
	_fields_ = [("solNo", ctypes.c_int), ("state", ctypes.c_int)]


class PinmameLampState(ctypes.Structure):
	_fields_ = [("lampNo", ctypes.c_int), ("state", ctypes.c_int)]


class PinmameGIState(ctypes.Structure):
	_fields_ = [("giNo", ctypes.c_int), ("state", ctypes.c_int)]


CallbackFactory = ctypes.WINFUNCTYPE if os.name == "nt" else ctypes.CFUNCTYPE
StateCallback = CallbackFactory(None, ctypes.c_int, ctypes.c_void_p)
DisplayAvailableCallback = CallbackFactory(
	None,
	ctypes.c_int,
	ctypes.c_int,
	ctypes.POINTER(PinmameDisplayLayout),
	ctypes.c_void_p,
)
DisplayUpdatedCallback = CallbackFactory(
	None,
	ctypes.c_int,
	ctypes.c_void_p,
	ctypes.POINTER(PinmameDisplayLayout),
	ctypes.c_void_p,
)
AudioAvailableCallback = CallbackFactory(
	ctypes.c_int,
	ctypes.POINTER(PinmameAudioInfo),
	ctypes.c_void_p,
)
AudioUpdatedCallback = CallbackFactory(
	ctypes.c_int,
	ctypes.c_void_p,
	ctypes.c_int,
	ctypes.c_void_p,
)
SolenoidUpdatedCallback = CallbackFactory(
	None,
	ctypes.POINTER(PinmameSolenoidState),
	ctypes.c_void_p,
)
KeyPressedCallback = CallbackFactory(ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
SoundCommandCallback = CallbackFactory(
	None,
	ctypes.c_int,
	ctypes.c_int,
	ctypes.c_void_p,
)


class PinmameConfig(ctypes.Structure):
	_fields_ = [
		("audioFormat", ctypes.c_int),
		("sampleRate", ctypes.c_int),
		("vpmPath", ctypes.c_char * PINMAME_MAX_PATH),
		("cb_OnStateUpdated", StateCallback),
		("cb_OnDisplayAvailable", DisplayAvailableCallback),
		("cb_OnDisplayUpdated", DisplayUpdatedCallback),
		("cb_OnAudioAvailable", AudioAvailableCallback),
		("cb_OnAudioUpdated", AudioUpdatedCallback),
		("cb_OnMechAvailable", ctypes.c_void_p),
		("cb_OnMechUpdated", ctypes.c_void_p),
		("cb_OnSolenoidUpdated", SolenoidUpdatedCallback),
		("cb_OnConsoleDataUpdated", ctypes.c_void_p),
		("fn_IsKeyPressed", KeyPressedCallback),
		("cb_OnLogMessage", ctypes.c_void_p),
		("cb_OnSoundCommand", SoundCommandCallback),
	]


class Recorder:
	def __init__(self) -> None:
		self.started_at = time.monotonic()
		self.ready = threading.Event()
		self.lock = threading.Lock()
		self.events: list[dict[str, Any]] = []
		self.display_layouts: dict[int, dict[str, int]] = {}
		self.display_frames: dict[int, list[int] | bytes] = {}
		self.dmd_change_counts: dict[int, int] = {}
		self.dmd_suppressed_counts: dict[int, int] = {}
		self.video_change_counts: dict[int, int] = {}
		self.video_suppressed_counts: dict[int, int] = {}
		self.video_frame_hashes: dict[int, str] = {}
		self.solenoid_states: dict[int, int] = {}
		self.lamp_states: dict[int, int] = {}
		self.gi_states: dict[int, int] = {}

	def record(self, event: str, **values: Any) -> None:
		with self.lock:
			self.events.append(
				{"time_s": round(time.monotonic() - self.started_at, 6), "event": event, **values}
			)

	def event_index(self) -> int:
		with self.lock:
			return len(self.events)

	def transition_summary(self, start_index: int) -> dict[str, list[dict[str, Any]]]:
		with self.lock:
			events = list(self.events[start_index:])
		summary: dict[str, list[dict[str, Any]]] = {}
		for event_name, output_key in (("solenoid", "solenoids"), ("lamp", "lamps"), ("gi", "gis")):
			states: dict[int, list[int]] = {}
			for event in events:
				if event.get("event") != event_name:
					continue
				states.setdefault(event["number"], []).append(event["state"])
			summary[output_key] = [
				{"number": number, "states": values}
				for number, values in sorted(states.items())
			]
		return summary

	def snapshot_displays(
		self,
		dmd_dir: Path | None = None,
		snapshot_index: int | None = None,
		snapshot_label: str | None = None,
	) -> list[dict[str, Any]]:
		with self.lock:
			frames = [
				(
					index,
					dict(self.display_layouts.get(index, {})),
					bytes(frame) if isinstance(frame, bytes) else list(frame),
				)
				for index, frame in sorted(self.display_frames.items())
			]
		displays = []
		for index, layout, frame in frames:
			display: dict[str, Any] = {"index": index, "layout": layout}
			display_type = layout.get("type", -1) & 0x1F
			if display_type == 14:
				pixels = bytes(frame)
				display["pixel_sha256"] = hashlib.sha256(pixels).hexdigest()
				display["nonzero_pixels"] = sum(pixel != 0 for pixel in pixels)
				if dmd_dir is not None and snapshot_index is not None:
					dmd_dir.mkdir(parents=True, exist_ok=True)
					slug = re.sub(r"[^a-z0-9]+", "-", (snapshot_label or "snapshot").lower()).strip("-")
					artifact = dmd_dir / f"{snapshot_index:03d}-{slug}-display-{index}.pgm"
					depth = max(int(layout.get("depth", 1)), 1)
					max_level = max((1 << depth) - 1, 1)
					grayscale = (
						bytes(round(pixel * 255 / max_level) for pixel in pixels)
						if max(pixels, default=0) <= max_level
						else pixels
					)
					header = f"P5\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
					artifact.write_bytes(header + grayscale)
					display["artifact"] = str(artifact)
			elif display_type == 15:
				pixels = bytes(frame)
				display["pixel_format"] = "rgb24"
				display["pixel_sha256"] = hashlib.sha256(pixels).hexdigest()
				display["nonblack_pixels"] = sum(
					any(pixels[offset : offset + 3]) for offset in range(0, len(pixels), 3)
				)
				if dmd_dir is not None and snapshot_index is not None:
					dmd_dir.mkdir(parents=True, exist_ok=True)
					slug = re.sub(r"[^a-z0-9]+", "-", (snapshot_label or "snapshot").lower()).strip("-")
					artifact = dmd_dir / f"{snapshot_index:03d}-{slug}-display-{index}.ppm"
					header = f"P6\n{layout['width']} {layout['height']}\n255\n".encode("ascii")
					artifact.write_bytes(header + pixels)
					display["artifact"] = str(artifact)
			else:
				display["segments"] = frame
			text = _decode_segment_frame(layout.get("type", -1), frame)
			if text is not None:
				display["text"] = text
			displays.append(display)
		return displays

	def current_display_text(self) -> str:
		"""Return normalized text from every currently decoded segment display."""
		with self.lock:
			frames = [
				(self.display_layouts.get(index, {}).get("type", -1), list(frame))
				for index, frame in sorted(self.display_frames.items())
				if (self.display_layouts.get(index, {}).get("type", -1) & 0x1F)
				in SEGMENT_16_DISPLAY_TYPES
			]
		texts = [
			text
			for display_type, frame in frames
			if (text := _decode_segment_frame(display_type, frame)) is not None
		]
		return " ".join(" ".join(texts).upper().split())

	def record_dmd_frame(self, index: int, frame: list[int]) -> None:
		with self.lock:
			if self.display_frames.get(index) == frame:
				return
			self.display_frames[index] = frame
			change_count = self.dmd_change_counts.get(index, 0) + 1
			self.dmd_change_counts[index] = change_count
			if change_count <= MAX_DMD_EVENTS_PER_DISPLAY:
				self.events.append({"time_s": round(time.monotonic() - self.started_at, 6), "event": "display", "index": index, "pixel_sha256": hashlib.sha256(bytes(frame)).hexdigest()})
			else:
				self.dmd_suppressed_counts[index] = self.dmd_suppressed_counts.get(index, 0) + 1

	def record_video_frame(self, index: int, frame: bytes) -> None:
		frame_sha256 = hashlib.sha256(frame).hexdigest()
		with self.lock:
			if self.video_frame_hashes.get(index) == frame_sha256:
				return
			self.display_frames[index] = frame
			self.video_frame_hashes[index] = frame_sha256
			change_count = self.video_change_counts.get(index, 0) + 1
			self.video_change_counts[index] = change_count
			if change_count <= MAX_DMD_EVENTS_PER_DISPLAY:
				self.events.append({"time_s": round(time.monotonic() - self.started_at, 6), "event": "video", "index": index, "pixel_sha256": frame_sha256})
			else:
				self.video_suppressed_counts[index] = self.video_suppressed_counts.get(index, 0) + 1

	def snapshot_dmd_event_summary(self) -> dict[str, dict[str, int]]:
		with self.lock:
			return {
				str(index): {"changed_frames": count, "recorded_events": min(count, MAX_DMD_EVENTS_PER_DISPLAY), "suppressed_events": self.dmd_suppressed_counts.get(index, 0)}
				for index, count in sorted(self.dmd_change_counts.items())
			}

	def snapshot_video_event_summary(self) -> dict[str, dict[str, int]]:
		with self.lock:
			return {
				str(index): {"changed_frames": count, "recorded_events": min(count, MAX_DMD_EVENTS_PER_DISPLAY), "suppressed_events": self.video_suppressed_counts.get(index, 0)}
				for index, count in sorted(self.video_change_counts.items())
			}

	def record_lamp(self, number: int, state: int) -> None:
		with self.lock:
			self.lamp_states[number] = state
			self.events.append(
				{
					"time_s": round(time.monotonic() - self.started_at, 6),
					"event": "lamp",
					"number": number,
					"state": state,
				}
			)

	def snapshot_active_lamps(self) -> list[int]:
		with self.lock:
			return sorted(number for number, state in self.lamp_states.items() if state)

	def record_solenoid(self, number: int, state: int) -> None:
		with self.lock:
			self.solenoid_states[number] = state
			self.events.append(
				{
					"time_s": round(time.monotonic() - self.started_at, 6),
					"event": "solenoid",
					"number": number,
					"state": state,
				}
			)

	def snapshot_active_solenoids(self) -> list[int]:
		with self.lock:
			return sorted(number for number, state in self.solenoid_states.items() if state)

	def record_gi(self, number: int, state: int) -> None:
		with self.lock:
			self.gi_states[number] = state
			self.events.append(
				{
					"time_s": round(time.monotonic() - self.started_at, 6),
					"event": "gi",
					"number": number,
					"state": state,
				}
			)

	def snapshot_active_gis(self) -> list[int]:
		with self.lock:
			return sorted(number for number, state in self.gi_states.items() if state)


def _parse_pulse(value: str) -> tuple[int, int, float]:
	parts = value.split(":")
	if len(parts) > 3:
		raise argparse.ArgumentTypeError("pulse must be SWITCH[:HOLD_MS[:SETTLE_S]]")
	try:
		switch = int(parts[0])
		hold_ms = int(parts[1]) if len(parts) >= 2 else 100
		settle_s = float(parts[2]) if len(parts) == 3 else 1.0
	except ValueError as exc:
		raise argparse.ArgumentTypeError("pulse values must be numeric") from exc
	if hold_ms <= 0 or settle_s < 0:
		raise argparse.ArgumentTypeError("pulse hold must be positive and settle non-negative")
	_validate_public_switch_address(switch, argparse.ArgumentTypeError)
	return switch, hold_ms, settle_s


def _parse_initial_switch(value: str) -> tuple[int, int]:
	parts = value.split(":")
	if len(parts) > 2:
		raise argparse.ArgumentTypeError("initial switch must be SWITCH[:STATE]")
	try:
		switch = int(parts[0])
		state = int(parts[1]) if len(parts) == 2 else 1
	except ValueError as exc:
		raise argparse.ArgumentTypeError("initial switch values must be integers") from exc
	if state not in (0, 1):
		raise argparse.ArgumentTypeError("initial switch state must be 0 or 1")
	_validate_public_switch_address(switch, argparse.ArgumentTypeError)
	return switch, state


def _parse_watch_switch(value: str) -> int:
	try:
		switch = int(value)
	except ValueError as exc:
		raise argparse.ArgumentTypeError("watched switch must be an integer") from exc
	_validate_public_switch_address(switch, argparse.ArgumentTypeError)
	return switch


def _validate_public_switch_address(
	switch: int,
	error_type: type[Exception] = ValueError,
) -> None:
	"""Reject addresses that can overrun an unchecked sequential PinMAME switch matrix.

	PinMAME's native core_getSw/core_setSw functions do not bounds-check the converted
	matrix index. Until LibPinMAME exposes a driver's converter, the harness uses the
	conservative range shared by sequential converters and refuses less-safe addresses.
	"""
	if not MIN_SAFE_PUBLIC_SWITCH <= switch <= MAX_SAFE_PUBLIC_SWITCH:
		raise error_type(
			f"public switch address must be between {MIN_SAFE_PUBLIC_SWITCH} and "
			f"{MAX_SAFE_PUBLIC_SWITCH}; got {switch}"
		)


def _load_scenario(path: Path, content: bytes | None = None) -> dict[str, Any]:
	data = json.loads((content if content is not None else path.read_bytes()).decode("utf-8"))
	schema = json.loads(SCENARIO_SCHEMA_PATH.read_text(encoding="utf-8"))
	errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda error: list(error.path))
	if errors:
		error = errors[0]
		location = ".".join(str(part) for part in error.path) or "<root>"
		raise ValueError(f"scenario schema validation failed at {location}: {error.message}")
	return data


def _configure_api(library: ctypes.CDLL) -> None:
	library.PinmameSetConfig.argtypes = [ctypes.POINTER(PinmameConfig)]
	library.PinmameSetConfig.restype = None
	library.PinmameSetPath.argtypes = [ctypes.c_int, ctypes.c_char_p]
	library.PinmameSetPath.restype = None
	library.PinmameSetHandleKeyboard.argtypes = [ctypes.c_int]
	library.PinmameSetHandleKeyboard.restype = None
	library.PinmameSetHandleMechanics.argtypes = [ctypes.c_int]
	library.PinmameSetHandleMechanics.restype = None
	library.PinmameRun.argtypes = [ctypes.c_char_p]
	library.PinmameRun.restype = ctypes.c_int
	library.PinmameIsRunning.argtypes = []
	library.PinmameIsRunning.restype = ctypes.c_int
	library.PinmameStop.argtypes = []
	library.PinmameStop.restype = None
	library.PinmameSetSwitch.argtypes = [ctypes.c_int, ctypes.c_int]
	library.PinmameSetSwitch.restype = None
	library.PinmameGetSwitch.argtypes = [ctypes.c_int]
	library.PinmameGetSwitch.restype = ctypes.c_int
	library.PinmameGetMaxSolenoids.argtypes = []
	library.PinmameGetMaxSolenoids.restype = ctypes.c_int
	library.PinmameGetSolenoid.argtypes = [ctypes.c_int]
	library.PinmameGetSolenoid.restype = ctypes.c_int
	library.PinmameGetMaxLamps.argtypes = []
	library.PinmameGetMaxLamps.restype = ctypes.c_int
	library.PinmameGetLamp.argtypes = [ctypes.c_int]
	library.PinmameGetLamp.restype = ctypes.c_int
	library.PinmameGetChangedLamps.argtypes = [ctypes.POINTER(PinmameLampState)]
	library.PinmameGetChangedLamps.restype = ctypes.c_int
	library.PinmameGetMaxGIs.argtypes = []
	library.PinmameGetMaxGIs.restype = ctypes.c_int
	library.PinmameGetGI.argtypes = [ctypes.c_int]
	library.PinmameGetGI.restype = ctypes.c_int
	library.PinmameGetChangedGIs.argtypes = [ctypes.POINTER(PinmameGIState)]
	library.PinmameGetChangedGIs.restype = ctypes.c_int


def _poll_outputs(library: ctypes.CDLL, recorder: Recorder) -> None:
	max_lamps = max(library.PinmameGetMaxLamps(), 1)
	lamp_states = (PinmameLampState * max_lamps)()
	for index in range(library.PinmameGetChangedLamps(lamp_states)):
		state = lamp_states[index]
		recorder.record_lamp(state.lampNo, state.state)

	max_gis = max(library.PinmameGetMaxGIs(), 1)
	gi_states = (PinmameGIState * max_gis)()
	for index in range(library.PinmameGetChangedGIs(gi_states)):
		state = gi_states[index]
		recorder.record_gi(state.giNo, state.state)


def _wait_with_poll(library: ctypes.CDLL, recorder: Recorder, seconds: float) -> None:
	deadline = time.monotonic() + seconds
	while time.monotonic() < deadline:
		_poll_outputs(library, recorder)
		time.sleep(min(0.01, max(deadline - time.monotonic(), 0)))
	_poll_outputs(library, recorder)


def _wait_for_display_match(
	library: ctypes.CDLL,
	recorder: Recorder,
	targets: list[str],
	seconds: float,
) -> tuple[str | None, str]:
	"""Poll through a settle window so short-lived diagnostic titles are not skipped."""
	deadline = time.monotonic() + seconds
	while True:
		_poll_outputs(library, recorder)
		display_text = recorder.current_display_text()
		matched = next((target for target in targets if target in display_text), None)
		if matched is not None or time.monotonic() >= deadline:
			return matched, display_text
		time.sleep(min(0.01, max(deadline - time.monotonic(), 0)))


def _hold_switch(
	library: ctypes.CDLL,
	recorder: Recorder,
	switch: int,
	hold_seconds: float,
	before_release: Callable[[], None] | None = None,
	*,
	active_state: int = 1,
) -> None:
	"""Keep a switch asserted even when a hardware driver refreshes its cabinet column."""
	rest_state = 1 - active_state
	deadline = time.monotonic() + hold_seconds
	while True:
		library.PinmameSetSwitch(switch, active_state)
		_poll_outputs(library, recorder)
		remaining = deadline - time.monotonic()
		if remaining <= 0:
			break
		time.sleep(min(0.01, remaining))
	if before_release is not None:
		before_release()
	library.PinmameSetSwitch(switch, rest_state)
	_poll_outputs(library, recorder)


def _output_snapshot(
	recorder: Recorder,
	label: str,
	dmd_dir: Path | None = None,
	snapshot_index: int | None = None,
	library: ctypes.CDLL | None = None,
	watch_switches: tuple[int, ...] = (),
) -> dict[str, Any]:
	snapshot = {
		"label": label,
		"time_s": round(time.monotonic() - recorder.started_at, 6),
		"active_solenoids": recorder.snapshot_active_solenoids(),
		"active_lamps": recorder.snapshot_active_lamps(),
		"active_gis": recorder.snapshot_active_gis(),
		"displays": recorder.snapshot_displays(dmd_dir, snapshot_index, label),
	}
	if library is not None and watch_switches:
		snapshot["watched_switches"] = [
			{"number": switch, "state": 1 if library.PinmameGetSwitch(switch) else 0}
			for switch in watch_switches
		]
	return snapshot


def _append_output_snapshot(
	snapshots: list[dict[str, Any]],
	recorder: Recorder,
	label: str,
	dmd_dir: Path | None,
	library: ctypes.CDLL | None = None,
	watch_switches: tuple[int, ...] = (),
) -> None:
	snapshots.append(
		_output_snapshot(
			recorder, label, dmd_dir, len(snapshots), library, watch_switches
		)
	)


def _path_bytes(path: Path) -> bytes:
	encoded = str(path).encode("utf-8")
	if len(encoded) >= PINMAME_MAX_PATH:
		raise ValueError(f"PinMAME path exceeds {PINMAME_MAX_PATH - 1} encoded bytes: {path}")
	return encoded


def run(args: argparse.Namespace) -> dict[str, Any]:
	dll_path = args.library.resolve(strict=True)
	rom_path = args.rom_path.resolve(strict=True)
	work_dir = args.work_dir.resolve()
	scenario_path = args.scenario.resolve(strict=True) if args.scenario else None
	scenario_bytes = scenario_path.read_bytes() if scenario_path else None
	scenario_sha256 = hashlib.sha256(scenario_bytes).hexdigest() if scenario_bytes else None
	scenario = _load_scenario(scenario_path, scenario_bytes) if scenario_path else None
	if scenario and scenario.get("game") and scenario["game"] != args.game:
		raise ValueError(
			f"scenario game {scenario['game']!r} does not match --game {args.game!r}"
		)
	if scenario and (args.initial_switch or args.pulse):
		raise ValueError("--scenario cannot be combined with --initial-switch or --pulse")
	initial_switches = (
		[(item["switch"], item["state"]) for item in scenario.get("initial_switches", [])]
		if scenario
		else list(args.initial_switch)
	)
	actions: list[dict[str, Any]] = (
		list(scenario.get("actions", []))
		if scenario
		else [
			{
				"type": "pulse",
				"switch": switch,
				"hold_ms": hold_ms,
				"settle_s": settle_s,
				"snapshot_while_held": args.snapshot_while_held,
			}
			for switch, hold_ms, settle_s in args.pulse
		]
	)
	watch_switch_set = set(args.watch_switch)
	if scenario:
		watch_switch_set.update(scenario.get("watch_switches", []))
	watch_switch_set.update(switch for switch, _state in initial_switches)
	watch_switch_set.update(
		action["switch"]
		for action in actions
		if action["type"] in ("pulse", "set_switch", "pulse_until_display", "pulse_until_output")
		and "switch" in action
	)
	watch_switches = tuple(sorted(watch_switch_set))
	for switch in watch_switches:
		_validate_public_switch_address(switch)
	use_keyboard = any(
		action["type"] in ("pulse_key", "set_key")
		or (action["type"] in ("pulse_until_display", "pulse_until_output") and "key" in action)
		for action in actions
	)
	for child in ("nvram", "cfg", "hi"):
		(work_dir / child).mkdir(parents=True, exist_ok=True)

	library = ctypes.CDLL(str(dll_path))
	_configure_api(library)
	recorder = Recorder()
	pressed_keys: set[int] = set()
	pressed_keys_lock = threading.Lock()

	@StateCallback
	def on_state_updated(state: int, _user_data: int) -> None:
		recorder.record("emulator_state", state=state)
		if state:
			recorder.ready.set()

	@DisplayAvailableCallback
	def on_display_available(
		index: int,
		display_count: int,
		layout_pointer: ctypes.POINTER(PinmameDisplayLayout),
		_user_data: int,
	) -> None:
		layout = layout_pointer.contents
		values = {
			"type": layout.type,
			"top": layout.top,
			"left": layout.left,
			"length": layout.length,
			"width": layout.width,
			"height": layout.height,
			"depth": layout.depth,
		}
		with recorder.lock:
			recorder.display_layouts[index] = values
		recorder.record("display_available", index=index, display_count=display_count, **values)

	@DisplayUpdatedCallback
	def on_display_updated(
		index: int,
		data: int,
		layout_pointer: ctypes.POINTER(PinmameDisplayLayout),
		_user_data: int,
	) -> None:
		layout = layout_pointer.contents
		if not data:
			return
		display_type = layout.type & 0x1F
		if display_type == 14:
			if layout.width <= 0 or layout.height <= 0:
				return
			frame = list(ctypes.string_at(data, layout.width * layout.height))
			recorder.record_dmd_frame(index, frame)
			return
		if display_type == 15:
			if layout.width <= 0 or layout.height <= 0:
				return
			frame = ctypes.string_at(data, layout.width * layout.height * 3)
			recorder.record_video_frame(index, frame)
			return
		if layout.length <= 0:
			return
		segments = ctypes.cast(data, ctypes.POINTER(ctypes.c_uint16))
		frame = [segments[offset] for offset in range(layout.length)]
		with recorder.lock:
			changed = recorder.display_frames.get(index) != frame
			recorder.display_frames[index] = frame
		if changed:
			values: dict[str, Any] = {"index": index, "segments": frame}
			text = _decode_segment_frame(layout.type, frame)
			if text is not None:
				values["text"] = text
			recorder.record("display", **values)

	@AudioAvailableCallback
	def on_audio_available(info_pointer: ctypes.POINTER(PinmameAudioInfo), _user_data: int) -> int:
		info = info_pointer.contents
		recorder.record(
			"audio_available",
			format=info.format,
			channels=info.channels,
			sample_rate=info.sampleRate,
			frames_per_second=info.framesPerSecond,
			samples_per_frame=info.samplesPerFrame,
			buffer_size=info.bufferSize,
		)
		return info.samplesPerFrame

	@AudioUpdatedCallback
	def on_audio_updated(_buffer: int, samples: int, _user_data: int) -> int:
		return samples

	@SolenoidUpdatedCallback
	def on_solenoid_updated(
		state_pointer: ctypes.POINTER(PinmameSolenoidState), _user_data: int
	) -> None:
		state = state_pointer.contents
		recorder.record_solenoid(state.solNo, state.state)

	@KeyPressedCallback
	def is_key_pressed(keycode: int, _user_data: int) -> int:
		with pressed_keys_lock:
			return 1 if keycode in pressed_keys else 0

	@SoundCommandCallback
	def on_sound_command(board: int, command: int, _user_data: int) -> None:
		recorder.record("sound_command", board=board, command=command)

	config = PinmameConfig(
		audioFormat=0,
		sampleRate=44100,
		vpmPath=_path_bytes(work_dir) + os.sep.encode("ascii"),
		cb_OnStateUpdated=on_state_updated,
		cb_OnDisplayAvailable=on_display_available,
		cb_OnDisplayUpdated=on_display_updated,
		cb_OnAudioAvailable=on_audio_available,
		cb_OnAudioUpdated=on_audio_updated,
		cb_OnMechAvailable=None,
		cb_OnMechUpdated=None,
		cb_OnSolenoidUpdated=on_solenoid_updated,
		cb_OnConsoleDataUpdated=None,
		fn_IsKeyPressed=is_key_pressed,
		cb_OnLogMessage=None,
		cb_OnSoundCommand=on_sound_command,
	)

	library.PinmameSetConfig(ctypes.byref(config))
	library.PinmameSetPath(PINMAME_FILE_TYPE_ROMS, _path_bytes(rom_path))
	library.PinmameSetPath(PINMAME_FILE_TYPE_NVRAM, _path_bytes(work_dir / "nvram"))
	library.PinmameSetPath(PINMAME_FILE_TYPE_CONFIG, _path_bytes(work_dir / "cfg"))
	library.PinmameSetPath(PINMAME_FILE_TYPE_HIGHSCORE, _path_bytes(work_dir / "hi"))
	if args.samples_path:
		library.PinmameSetPath(
			PINMAME_FILE_TYPE_SAMPLES, _path_bytes(args.samples_path.resolve(strict=True))
		)
	library.PinmameSetHandleKeyboard(1 if use_keyboard else 0)
	library.PinmameSetHandleMechanics(0)

	status = library.PinmameRun(args.game.encode("ascii"))
	if status != PINMAME_STATUS_OK:
		raise RuntimeError(f"PinmameRun returned status {status}")

	snapshots: list[dict[str, Any]] = []
	steps: list[dict[str, Any]] = []
	failure: dict[str, Any] | None = None
	current_step: int | None = None
	current_label: str | None = None
	try:
		if not recorder.ready.wait(args.ready_timeout):
			raise TimeoutError("PinMAME did not report a ready state")
		for switch, state in initial_switches:
			library.PinmameSetSwitch(switch, state)
			recorder.record(
				"switch",
				number=switch,
				state=state,
				observed_state=1 if library.PinmameGetSwitch(switch) else 0,
				initial=True,
			)
		_wait_with_poll(library, recorder, args.boot_wait)
		snapshots.append(
			_output_snapshot(
				recorder, "booted", args.dmd_dir, len(snapshots), library, watch_switches
			)
		)
		for step_number, action in enumerate(actions, start=1):
			current_step = step_number
			start_index = recorder.event_index()
			action_type = action["type"]
			label = action.get("label") or f"step {step_number}: {action_type}"
			current_label = label
			step_result: dict[str, Any] = {
				"step": step_number,
				"type": action_type,
				"label": label,
			}
			if action_type == "pulse":
				switch = action["switch"]
				hold_ms = action.get("hold_ms", 100)
				settle_s = action.get("settle_s", 1.0)
				active_state = action.get("active_state", 1)
				rest_state = 1 - active_state
				recorder.record("switch", number=switch, state=active_state, step=step_number)
				observed_while_held: list[int] = []

				def before_release() -> None:
					observed = 1 if library.PinmameGetSwitch(switch) else 0
					observed_while_held.append(observed)
					recorder.record(
						"switch_observed", number=switch, state=observed, phase="held", step=step_number
					)
					if action.get("snapshot_while_held", False):
						_append_output_snapshot(
							snapshots,
							recorder,
							f"{label} (held)",
							args.dmd_dir,
							library,
							watch_switches,
						)

				_hold_switch(
					library,
					recorder,
					switch,
					hold_ms / 1000,
					before_release,
					active_state=active_state,
				)
				released_state = 1 if library.PinmameGetSwitch(switch) else 0
				recorder.record(
					"switch", number=switch, state=rest_state, observed_state=released_state, step=step_number
				)
				_wait_with_poll(library, recorder, settle_s)
				step_result.update(
					{
						"switch": switch,
						"hold_ms": hold_ms,
						"settle_s": settle_s,
						"active_state": active_state,
						"rest_state": rest_state,
						"observed_while_held": observed_while_held[-1],
						"observed_after_release": 1 if library.PinmameGetSwitch(switch) else 0,
					}
				)
			elif action_type == "set_switch":
				switch = action["switch"]
				state = action["state"]
				settle_s = action.get("settle_s", 1.0)
				library.PinmameSetSwitch(switch, state)
				observed = 1 if library.PinmameGetSwitch(switch) else 0
				recorder.record(
					"switch", number=switch, state=state, observed_state=observed, step=step_number
				)
				_wait_with_poll(library, recorder, settle_s)
				step_result.update(
					{
						"switch": switch,
						"state": state,
						"settle_s": settle_s,
						"observed_state": 1 if library.PinmameGetSwitch(switch) else 0,
					}
				)
			elif action_type in ("pulse_key", "set_key"):
				key = action["key"]
				keycode = KEY_ALIASES[key]
				settle_s = action.get("settle_s", 1.0)
				if action_type == "pulse_key":
					hold_ms = action.get("hold_ms", 100)
					with pressed_keys_lock:
						pressed_keys.add(keycode)
					recorder.record("key", key=key, keycode=keycode, state=1, step=step_number)
					_wait_with_poll(library, recorder, hold_ms / 1000)
					if action.get("snapshot_while_held", False):
						_append_output_snapshot(
							snapshots,
							recorder,
							f"{label} (held)",
							args.dmd_dir,
							library,
							watch_switches,
						)
					with pressed_keys_lock:
						pressed_keys.discard(keycode)
					recorder.record("key", key=key, keycode=keycode, state=0, step=step_number)
					step_result["hold_ms"] = hold_ms
				else:
					state = action["state"]
					with pressed_keys_lock:
						if state:
							pressed_keys.add(keycode)
						else:
							pressed_keys.discard(keycode)
					recorder.record("key", key=key, keycode=keycode, state=state, step=step_number)
					step_result["state"] = state
				_wait_with_poll(library, recorder, settle_s)
				step_result.update({"key": key, "keycode": keycode, "settle_s": settle_s})
			elif action_type == "wait":
				seconds = action["seconds"]
				_wait_with_poll(library, recorder, seconds)
				step_result["seconds"] = seconds
			elif action_type == "wait_until_output":
				channel_key = {"solenoid": "solenoids", "lamp": "lamps", "gi": "gis"}[
					action["channel"]
				]
				addresses = set(action["addresses"])
				timeout_s = action["timeout_s"]
				active_only = action.get("active_only", False)
				deadline = time.monotonic() + timeout_s
				matched_outputs: list[dict[str, Any]] = []
				while True:
					_poll_outputs(library, recorder)
					matched_outputs = [
						transition
						for transition in recorder.transition_summary(start_index)[channel_key]
						if transition["number"] in addresses
						and (not active_only or any(state != 0 for state in transition["states"]))
					]
					if matched_outputs:
						break
					remaining = deadline - time.monotonic()
					if remaining <= 0:
						raise TimeoutError(
							f"{label}: no {action['channel']} transition at {sorted(addresses)} "
							f"within {timeout_s} seconds; display text was "
							f"{recorder.current_display_text()!r}"
						)
					time.sleep(min(0.01, remaining))
				step_result.update(
					{
						"channel": action["channel"],
						"addresses": action["addresses"],
						"timeout_s": timeout_s,
						"active_only": active_only,
						"matched_outputs": matched_outputs,
					}
				)
			elif action_type == "pulse_until_display":
				targets = [" ".join(text.upper().split()) for text in action["texts"]]
				hold_ms = action.get("hold_ms", 100)
				settle_s = action.get("settle_s", 1.0)
				max_pulses = action.get("max_pulses", 20)
				display_text = recorder.current_display_text()
				display_checks = [{"after_pulses": 0, "display_text": display_text}]
				matched_text = next((target for target in targets if target in display_text), None)
				pulses_performed = 0
				for pulse_number in range(1, max_pulses + 1):
					if matched_text is not None:
						break
					if "switch" in action:
						switch = action["switch"]
						active_state = action.get("active_state", 1)
						rest_state = 1 - active_state
						recorder.record(
							"switch", number=switch, state=active_state, step=step_number, repeat=pulse_number
						)
						_hold_switch(library, recorder, switch, hold_ms / 1000, active_state=active_state)
						recorder.record(
							"switch", number=switch, state=rest_state, step=step_number, repeat=pulse_number
						)
					else:
						key = action["key"]
						keycode = KEY_ALIASES[key]
						with pressed_keys_lock:
							pressed_keys.add(keycode)
						recorder.record(
							"key", key=key, keycode=keycode, state=1, step=step_number, repeat=pulse_number
						)
						_wait_with_poll(library, recorder, hold_ms / 1000)
						with pressed_keys_lock:
							pressed_keys.discard(keycode)
						recorder.record(
							"key", key=key, keycode=keycode, state=0, step=step_number, repeat=pulse_number
						)
					pulses_performed = pulse_number
					matched_text, display_text = _wait_for_display_match(
						library, recorder, targets, settle_s
					)
					display_checks.append(
						{"after_pulses": pulse_number, "display_text": display_text}
					)
				if matched_text is None:
					raise TimeoutError(
						f"{label}: none of {targets!r} appeared after {max_pulses} pulses; "
						f"last display text was {display_text!r}"
					)
				step_result.update(
					{
						"switch": action.get("switch"),
						"key": action.get("key"),
						"texts": action["texts"],
						"matched_text": matched_text,
						"pulses": pulses_performed,
						"hold_ms": hold_ms,
						"settle_s": settle_s,
						"active_state": action.get("active_state", 1) if "switch" in action else None,
						"display_checks": display_checks,
					}
				)
			elif action_type == "pulse_until_output":
				channel_key = {"solenoid": "solenoids", "lamp": "lamps", "gi": "gis"}[
					action["channel"]
				]
				addresses = set(action["addresses"])
				hold_ms = action.get("hold_ms", 100)
				settle_s = action.get("settle_s", 1.0)
				max_pulses = action.get("max_pulses", 20)
				pulse_checks: list[dict[str, Any]] = []
				matched_outputs: list[dict[str, Any]] = []
				for pulse_number in range(1, max_pulses + 1):
					pulse_start = recorder.event_index()
					if "switch" in action:
						switch = action["switch"]
						active_state = action.get("active_state", 1)
						rest_state = 1 - active_state
						recorder.record(
							"switch", number=switch, state=active_state, step=step_number, repeat=pulse_number
						)
						_hold_switch(library, recorder, switch, hold_ms / 1000, active_state=active_state)
						recorder.record(
							"switch", number=switch, state=rest_state, step=step_number, repeat=pulse_number
						)
					else:
						key = action["key"]
						keycode = KEY_ALIASES[key]
						with pressed_keys_lock:
							pressed_keys.add(keycode)
						recorder.record(
							"key", key=key, keycode=keycode, state=1, step=step_number, repeat=pulse_number
						)
						_wait_with_poll(library, recorder, hold_ms / 1000)
						with pressed_keys_lock:
							pressed_keys.discard(keycode)
						recorder.record(
							"key", key=key, keycode=keycode, state=0, step=step_number, repeat=pulse_number
						)
					_wait_with_poll(library, recorder, settle_s)
					pulse_summary = recorder.transition_summary(pulse_start)
					matched_outputs = [
						transition
						for transition in pulse_summary[channel_key]
						if transition["number"] in addresses
					]
					pulse_checks.append(
						{
							"after_pulses": pulse_number,
							"display_text": recorder.current_display_text(),
							"matched_outputs": matched_outputs,
						}
					)
					if matched_outputs:
						break
				else:
					raise TimeoutError(
						f"{label}: no {action['channel']} transition at {sorted(addresses)} "
						f"after {max_pulses} pulses; last display text was "
						f"{recorder.current_display_text()!r}"
					)
				step_result.update(
					{
						"switch": action.get("switch"),
						"key": action.get("key"),
						"channel": action["channel"],
						"addresses": action["addresses"],
						"matched_outputs": matched_outputs,
						"pulses": len(pulse_checks),
						"hold_ms": hold_ms,
						"settle_s": settle_s,
						"active_state": action.get("active_state", 1) if "switch" in action else None,
						"pulse_checks": pulse_checks,
					}
				)
			else:  # _load_scenario rejects this; keep run() defensive for constructed Namespaces.
				raise ValueError(f"unsupported action type: {action_type}")
			step_result["transitions"] = recorder.transition_summary(start_index)
			_append_output_snapshot(
				snapshots, recorder, label, args.dmd_dir, library, watch_switches
			)
			steps.append(step_result)
			current_step = None
			current_label = None
		if args.observe > 0:
			_wait_with_poll(library, recorder, args.observe)
			snapshots.append(
				_output_snapshot(
					recorder,
					"final observation",
					args.dmd_dir,
					len(snapshots),
					library,
					watch_switches,
				)
			)
	except Exception as exc:
		failure = {
			"type": type(exc).__name__,
			"message": str(exc),
			"step": current_step,
			"label": current_label,
		}
		recorder.record("failure", **failure)
		_append_output_snapshot(
			snapshots,
			recorder,
			f"failure: {current_label or type(exc).__name__}",
			args.dmd_dir,
			library,
			watch_switches,
		)
	finally:
		with pressed_keys_lock:
			pressed_keys.clear()
		if library.PinmameIsRunning():
			library.PinmameStop()
		for _ in range(100):
			if not library.PinmameIsRunning():
				break
			time.sleep(0.01)

	return {
		"format": "pinmame-harness-run",
		"version": 1,
		"game": args.game,
		"library": str(dll_path),
		"library_sha256": hashlib.sha256(dll_path.read_bytes()).hexdigest(),
		"p2k_debug_environment": {
			name: os.environ[name]
			for name in P2K_DEBUG_ENVIRONMENT_NAMES
			if name in os.environ
		},
		"rom_path": str(rom_path),
		"work_dir": str(work_dir),
		"dmd_dir": str(args.dmd_dir.resolve()) if args.dmd_dir else None,
		"scenario": (
			{
				"path": str(scenario_path),
				"sha256": scenario_sha256,
				"notes": scenario.get("notes"),
				"action_count": len(actions),
			}
			if scenario_path
			else None
		),
		"watch_switches": list(watch_switches),
		"initial_switches": [
			{"switch": switch, "state": state} for switch, state in initial_switches
		],
		"pulses": [
			{"switch": switch, "hold_ms": hold_ms, "settle_s": settle_s}
			for switch, hold_ms, settle_s in args.pulse
		],
		"snapshots": snapshots,
		"steps": steps,
		"failure": failure,
		"events": recorder.events,
		"dmd_event_summary": recorder.snapshot_dmd_event_summary(),
		"video_event_summary": recorder.snapshot_video_event_summary(),
	}


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--library", type=Path, required=True, help="libpinmame DLL/shared library")
	parser.add_argument("--game", required=True, help="PinMAME driver name")
	parser.add_argument("--rom-path", type=Path, required=True, help="read-only ROM archive directory")
	parser.add_argument("--work-dir", type=Path, required=True, help="isolated writable PinMAME state directory")
	parser.add_argument("--samples-path", type=Path, help="optional read-only sample archive directory")
	parser.add_argument(
		"--scenario",
		type=Path,
		help="optional structured JSON action sequence; cannot be combined with --initial-switch or --pulse",
	)
	parser.add_argument(
		"--watch-switch",
		type=_parse_watch_switch,
		action="append",
		default=[],
		metavar="SWITCH",
		help="include the observed public state of this switch in every snapshot; may be repeated",
	)
	parser.add_argument(
		"--initial-switch",
		type=_parse_initial_switch,
		action="append",
		default=[],
		metavar="SWITCH[:STATE]",
		help="set a persistent switch state immediately after starting the ROM; may be repeated",
	)
	parser.add_argument(
		"--pulse",
		type=_parse_pulse,
		action="append",
		default=[],
		metavar="SWITCH[:HOLD_MS[:SETTLE_S]]",
		help="inject a sequential switch pulse; may be repeated",
	)
	parser.add_argument("--ready-timeout", type=float, default=10.0)
	parser.add_argument("--boot-wait", type=float, default=2.0)
	parser.add_argument("--observe", type=float, default=0.0)
	parser.add_argument(
		"--dmd-dir",
		type=Path,
		help="optional directory for grayscale PGM DMD snapshots and RGB PPM video snapshots",
	)
	parser.add_argument(
		"--snapshot-while-held",
		action="store_true",
		help="capture an additional output/DMD snapshot immediately before each pulsed switch is released",
	)
	parser.add_argument("--output", type=Path, help="write JSON here instead of stdout")
	return parser


def main() -> int:
	args = build_parser().parse_args()
	try:
		result = run(args)
	except (OSError, RuntimeError, TimeoutError, ValueError) as exc:
		print(f"error: {exc}", file=sys.stderr)
		return 1
	serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
	if args.output:
		args.output.parent.mkdir(parents=True, exist_ok=True)
		args.output.write_text(serialized, encoding="utf-8")
	else:
		sys.stdout.write(serialized)
	return 1 if result["failure"] else 0


if __name__ == "__main__":
	raise SystemExit(main())
