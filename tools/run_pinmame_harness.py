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
from typing import Any


PINMAME_MAX_PATH = 512
PINMAME_FILE_TYPE_ROMS = 0
PINMAME_FILE_TYPE_NVRAM = 1
PINMAME_FILE_TYPE_SAMPLES = 2
PINMAME_FILE_TYPE_CONFIG = 3
PINMAME_FILE_TYPE_HIGHSCORE = 4
PINMAME_STATUS_OK = 0
SEGMENT_16_DISPLAY_TYPES = {0, 1, 16, 17}
MAX_DMD_EVENTS_PER_DISPLAY = 256

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
		self.display_frames: dict[int, list[int]] = {}
		self.dmd_change_counts: dict[int, int] = {}
		self.dmd_suppressed_counts: dict[int, int] = {}
		self.solenoid_states: dict[int, int] = {}
		self.lamp_states: dict[int, int] = {}
		self.gi_states: dict[int, int] = {}

	def record(self, event: str, **values: Any) -> None:
		with self.lock:
			self.events.append(
				{"time_s": round(time.monotonic() - self.started_at, 6), "event": event, **values}
			)

	def snapshot_displays(
		self,
		dmd_dir: Path | None = None,
		snapshot_index: int | None = None,
		snapshot_label: str | None = None,
	) -> list[dict[str, Any]]:
		with self.lock:
			displays = []
			for index, frame in sorted(self.display_frames.items()):
				layout = self.display_layouts.get(index, {})
				display: dict[str, Any] = {"index": index, "layout": layout}
				if (layout.get("type", -1) & 0x1F) == 14:
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
				else:
					display["segments"] = frame
				text = _decode_segment_frame(layout.get("type", -1), frame)
				if text is not None:
					display["text"] = text
				displays.append(display)
			return displays

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

	def snapshot_dmd_event_summary(self) -> dict[str, dict[str, int]]:
		with self.lock:
			return {
				str(index): {"changed_frames": count, "recorded_events": min(count, MAX_DMD_EVENTS_PER_DISPLAY), "suppressed_events": self.dmd_suppressed_counts.get(index, 0)}
				for index, count in sorted(self.dmd_change_counts.items())
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
	return switch, state


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


def _hold_switch(
	library: ctypes.CDLL, recorder: Recorder, switch: int, hold_seconds: float
) -> None:
	"""Keep a switch asserted even when a hardware driver refreshes its cabinet column."""
	deadline = time.monotonic() + hold_seconds
	while time.monotonic() < deadline:
		library.PinmameSetSwitch(switch, 1)
		_poll_outputs(library, recorder)
		time.sleep(min(0.01, max(deadline - time.monotonic(), 0)))
	library.PinmameSetSwitch(switch, 0)
	_poll_outputs(library, recorder)


def _output_snapshot(
	recorder: Recorder,
	label: str,
	dmd_dir: Path | None = None,
	snapshot_index: int | None = None,
) -> dict[str, Any]:
	return {
		"label": label,
		"time_s": round(time.monotonic() - recorder.started_at, 6),
		"active_solenoids": recorder.snapshot_active_solenoids(),
		"active_lamps": recorder.snapshot_active_lamps(),
		"active_gis": recorder.snapshot_active_gis(),
		"displays": recorder.snapshot_displays(dmd_dir, snapshot_index, label),
	}


def _path_bytes(path: Path) -> bytes:
	encoded = str(path).encode("utf-8")
	if len(encoded) >= PINMAME_MAX_PATH:
		raise ValueError(f"PinMAME path exceeds {PINMAME_MAX_PATH - 1} encoded bytes: {path}")
	return encoded


def run(args: argparse.Namespace) -> dict[str, Any]:
	dll_path = args.library.resolve(strict=True)
	rom_path = args.rom_path.resolve(strict=True)
	work_dir = args.work_dir.resolve()
	for child in ("nvram", "cfg", "hi"):
		(work_dir / child).mkdir(parents=True, exist_ok=True)

	library = ctypes.CDLL(str(dll_path))
	_configure_api(library)
	recorder = Recorder()

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
		if layout.length <= 0 or display_type == 15:
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
	def is_key_pressed(_keycode: int, _user_data: int) -> int:
		return 0

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
	library.PinmameSetHandleKeyboard(0)
	library.PinmameSetHandleMechanics(0)

	status = library.PinmameRun(args.game.encode("ascii"))
	if status != PINMAME_STATUS_OK:
		raise RuntimeError(f"PinmameRun returned status {status}")

	snapshots: list[dict[str, Any]] = []
	try:
		if not recorder.ready.wait(args.ready_timeout):
			raise TimeoutError("PinMAME did not report a ready state")
		for switch, state in args.initial_switch:
			library.PinmameSetSwitch(switch, state)
			recorder.record("switch", number=switch, state=state, initial=True)
		_wait_with_poll(library, recorder, args.boot_wait)
		snapshots.append(_output_snapshot(recorder, "booted", args.dmd_dir, len(snapshots)))
		for step, (switch, hold_ms, settle_s) in enumerate(args.pulse, start=1):
			recorder.record("switch", number=switch, state=1, step=step)
			_hold_switch(library, recorder, switch, hold_ms / 1000)
			recorder.record("switch", number=switch, state=0, step=step)
			_wait_with_poll(library, recorder, settle_s)
			snapshots.append(
				_output_snapshot(
					recorder,
					f"after pulse {step}: switch {switch}",
					args.dmd_dir,
					len(snapshots),
				)
			)
		if args.observe > 0:
			_wait_with_poll(library, recorder, args.observe)
			snapshots.append(
				_output_snapshot(
					recorder, "final observation", args.dmd_dir, len(snapshots)
				)
			)
	finally:
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
		"rom_path": str(rom_path),
		"work_dir": str(work_dir),
		"dmd_dir": str(args.dmd_dir.resolve()) if args.dmd_dir else None,
		"initial_switches": [
			{"switch": switch, "state": state} for switch, state in args.initial_switch
		],
		"pulses": [
			{"switch": switch, "hold_ms": hold_ms, "settle_s": settle_s}
			for switch, hold_ms, settle_s in args.pulse
		],
		"snapshots": snapshots,
		"events": recorder.events,
		"dmd_event_summary": recorder.snapshot_dmd_event_summary(),
	}


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--library", type=Path, required=True, help="libpinmame DLL/shared library")
	parser.add_argument("--game", required=True, help="PinMAME driver name")
	parser.add_argument("--rom-path", type=Path, required=True, help="read-only ROM archive directory")
	parser.add_argument("--work-dir", type=Path, required=True, help="isolated writable PinMAME state directory")
	parser.add_argument("--samples-path", type=Path, help="optional read-only sample archive directory")
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
		help="optional directory for grayscale PGM snapshots of DMD displays",
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
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
