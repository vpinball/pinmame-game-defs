"""Record a System 11 ROM's service-test displays alongside its outputs.

System 11 diagnostics are driven by the Advance (-7) and Auto-Up/Manual-Down (-6) buttons, and the
alphanumeric displays name each solenoid, lamp group, or switch as the test reaches it. This tool
boots a legal ROM through LibPinMAME from a new, empty state directory, performs a scripted list
of button actions, and records every decoded display change together with every solenoid, lamp,
and G.I. transition, all time-stamped. Pairing the display text with the output that pulsed at the
same moment is ROM evidence for a coil's name and address.

Actions (``--action``, repeatable, run in order):
  press:<switch>[:<hold_ms>[:<settle_s>]]  momentary press (1 then 0)
  set:<switch>:<state>                     hold a switch at a level
  wait:<seconds>                           observe without input

The output is a raw external run record; ROM bytes and NVRAM never leave the working root.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

HARNESS_PATH = Path(__file__).resolve().parent / "run_pinmame_harness.py"
_spec = importlib.util.spec_from_file_location("run_pinmame_harness", HARNESS_PATH)
harness = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(harness)


def decode_alpha(frame: list[int]) -> str:
	"""Decode sixteen-segment frames, keeping the period/comma bit (0x80) as a trailing '.'."""
	text = []
	for value in frame:
		character = harness.SEGMENT_16_CHARACTERS.get(value)
		if character is None and value & 0x80:
			base = harness.SEGMENT_16_CHARACTERS.get(value & ~0x80)
			character = f"{base}." if base is not None else None
		text.append(character if character is not None else "?")
	return "".join(text)


def parse_action(value: str) -> dict[str, Any]:
	parts = value.split(":")
	if parts[0] == "press":
		return {"type": "press", "switch": int(parts[1]), "hold_ms": float(parts[2]) if len(parts) > 2 else 150.0, "settle_s": float(parts[3]) if len(parts) > 3 else 1.0}
	if parts[0] == "set":
		return {"type": "set", "switch": int(parts[1]), "state": int(parts[2])}
	if parts[0] == "wait":
		return {"type": "wait", "seconds": float(parts[1])}
	raise argparse.ArgumentTypeError(f"unknown action {value!r}")


def run(args: argparse.Namespace) -> dict[str, Any]:
	dll_path = args.library.resolve(strict=True)
	rom_path = args.rom_path.resolve(strict=True)
	work_dir = args.work_dir.resolve()
	if work_dir.exists() and any(work_dir.iterdir()):
		raise RuntimeError(f"work directory must be new and empty: {work_dir}")
	for child in ("nvram", "cfg", "hi"):
		(work_dir / child).mkdir(parents=True, exist_ok=True)
	library = ctypes.CDLL(str(dll_path))
	harness._configure_api(library)
	ready = threading.Event()
	lock = threading.Lock()
	events: list[dict[str, Any]] = []
	layouts: dict[int, dict[str, int]] = {}
	start = time.monotonic()

	def record(kind: str, **values: Any) -> None:
		with lock:
			events.append({"t": round(time.monotonic() - start, 3), "kind": kind, **values})

	@harness.StateCallback
	def on_state(state: int, _user: int) -> None:
		if state:
			ready.set()

	@harness.DisplayAvailableCallback
	def on_display_available(index: int, count: int, layout_pointer: Any, _user: int) -> None:
		layout = layout_pointer.contents
		layouts[index] = {"type": layout.type, "length": layout.length}

	last_frames: dict[int, list[int]] = {}

	@harness.DisplayUpdatedCallback
	def on_display(index: int, data: int, layout_pointer: Any, _user: int) -> None:
		layout = layout_pointer.contents
		if not data or layout.length <= 0:
			return
		segments = ctypes.cast(data, ctypes.POINTER(ctypes.c_uint16))
		frame = [segments[offset] for offset in range(layout.length)]
		with lock:
			changed = last_frames.get(index) != frame
			last_frames[index] = frame
		if changed:
			record("display", index=index, text=decode_alpha(frame), segments=frame)

	@harness.AudioAvailableCallback
	def on_audio_available(info_pointer: Any, _user: int) -> int:
		return info_pointer.contents.samplesPerFrame

	@harness.AudioUpdatedCallback
	def on_audio(_buffer: int, samples: int, _user: int) -> int:
		return samples

	@harness.SolenoidUpdatedCallback
	def on_solenoid(state_pointer: Any, _user: int) -> None:
		state = state_pointer.contents
		record("solenoid", number=state.solNo, state=state.state)

	@harness.KeyPressedCallback
	def is_key_pressed(_keycode: int, _user: int) -> int:
		return 0

	@harness.SoundCommandCallback
	def on_sound(_board: int, _command: int, _user: int) -> None:
		return None

	config = harness.PinmameConfig(
		audioFormat=0,
		sampleRate=44100,
		vpmPath=harness._path_bytes(work_dir) + os.sep.encode("ascii"),
		cb_OnStateUpdated=on_state,
		cb_OnDisplayAvailable=on_display_available,
		cb_OnDisplayUpdated=on_display,
		cb_OnAudioAvailable=on_audio_available,
		cb_OnAudioUpdated=on_audio,
		cb_OnMechAvailable=None,
		cb_OnMechUpdated=None,
		cb_OnSolenoidUpdated=on_solenoid,
		cb_OnConsoleDataUpdated=None,
		fn_IsKeyPressed=is_key_pressed,
		cb_OnLogMessage=None,
		cb_OnSoundCommand=on_sound,
	)
	library.PinmameSetConfig(ctypes.byref(config))
	library.PinmameSetPath(harness.PINMAME_FILE_TYPE_ROMS, harness._path_bytes(rom_path))
	library.PinmameSetPath(harness.PINMAME_FILE_TYPE_NVRAM, harness._path_bytes(work_dir / "nvram"))
	library.PinmameSetPath(harness.PINMAME_FILE_TYPE_CONFIG, harness._path_bytes(work_dir / "cfg"))
	library.PinmameSetPath(harness.PINMAME_FILE_TYPE_HIGHSCORE, harness._path_bytes(work_dir / "hi"))
	library.PinmameSetHandleKeyboard(0)
	library.PinmameSetHandleMechanics(0)
	if library.PinmameRun(args.game.encode("ascii")) != harness.PINMAME_STATUS_OK:
		raise RuntimeError("PinmameRun failed")
	if not ready.wait(args.ready_timeout):
		raise RuntimeError("emulator never reported running")

	max_lamps = max(library.PinmameGetMaxLamps(), 1)
	lamp_states = (harness.PinmameLampState * max_lamps)()
	max_gis = max(library.PinmameGetMaxGIs(), 1)
	gi_states = (harness.PinmameGIState * max_gis)()
	stop = threading.Event()

	def poll() -> None:
		while not stop.is_set():
			for index in range(library.PinmameGetChangedLamps(lamp_states)):
				record("lamp", number=lamp_states[index].lampNo, state=lamp_states[index].state)
			for index in range(library.PinmameGetChangedGIs(gi_states)):
				record("gi", number=gi_states[index].giNo, state=gi_states[index].state)
			time.sleep(0.005)

	poller = threading.Thread(target=poll, daemon=True)
	poller.start()
	for item in args.initial_switch:
		switch, state = item.split(":")
		library.PinmameSetSwitch(int(switch), int(state))
	time.sleep(args.boot_wait)
	record("checkpoint", name="boot_complete")
	for index, action in enumerate(args.action):
		record("action", index=index, **action)
		if action["type"] == "press":
			library.PinmameSetSwitch(action["switch"], 1)
			time.sleep(action["hold_ms"] / 1000.0)
			library.PinmameSetSwitch(action["switch"], 0)
			time.sleep(action["settle_s"])
		elif action["type"] == "set":
			library.PinmameSetSwitch(action["switch"], action["state"])
			time.sleep(0.2)
		else:
			time.sleep(action["seconds"])
	stop.set()
	poller.join()
	library.PinmameStop()
	time.sleep(0.5)
	return {
		"format": "s11-service-display-probe",
		"version": 1,
		"game": args.game,
		"library_sha256": hashlib.sha256(dll_path.read_bytes()).hexdigest(),
		"rom_archive_sha256": hashlib.sha256((rom_path / f"{args.game}.zip").read_bytes()).hexdigest(),
		"tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		"initial_switches": list(args.initial_switch),
		"boot_wait_s": args.boot_wait,
		"actions": args.action,
		"display_layouts": layouts,
		"events": events,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--library", type=Path, required=True)
	parser.add_argument("--rom-path", type=Path, required=True)
	parser.add_argument("--work-dir", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--game", required=True)
	parser.add_argument("--initial-switch", action="append", default=[], metavar="SWITCH:STATE")
	parser.add_argument("--action", action="append", type=parse_action, default=[])
	parser.add_argument("--boot-wait", type=float, default=10.0)
	parser.add_argument("--ready-timeout", type=float, default=15.0)
	args = parser.parse_args()
	result = run(args)
	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8", newline="\n")
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
