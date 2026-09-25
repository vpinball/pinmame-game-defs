"""Drive The Machine: Bride of Pinbot's head position switch from a reactive model.

The rotating head's only feedback is matrix switch 67 (Face Position). The sources that describe
what the switch reports disagree: the retained known-working VPW script closes it only while the
head dwells at faces 1-3, pinned PinMAME's built-in ``bop_handleMech`` simulation closes it around
face 1 and opens it just before faces 2-4, and the operations manual only says the switch is open
over a cam indentation and closed off one. This tool boots a legal ``bop_*`` ROM through
LibPinMAME, integrates a head angle from public solenoid 28 (Head Motor) and 27 (Motor Relay,
direction), and writes switch 67 from the selected model every few milliseconds. It then walks the
service menu into one of the head tests (motor/switch, coils, cycle) or the helmet-light test and
records every display change, the motor/relay edges with the modelled angle at which the ROM
stopped the motor, the head-kicker pulses (solenoids 8, 15, 16) with their angle, and every
helmet lamp change (public lamps 91-108).

Face k is modelled at angle 90*(k-1) degrees and relay-off motion increases the angle. The
models are synthetic probes of what the ROM accepts, not measurements of the physical cam.
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

FACE_ANGLES = (0.0, 90.0, 180.0, 270.0)
SWITCH_HEAD = 67
SOLENOID_RELAY = 27
SOLENOID_MOTOR = 28
SERVICE_ESCAPE, SERVICE_DOWN, SERVICE_UP, SERVICE_ENTER = 5, 6, 7, 8
COIN_DOOR_CLOSED = 22
TEST_TITLES = {
	"motor-switch": "HEAD MTR",
	"coils": "HEAD COIL",
	"cycle": "HEAD CYCLE",
	"helmet": "HELMET",
	"lamp-names": "SINGLE LAMP",
	"solenoid-names": "SOLENOID TEST",
	"switch-names": "SWITCH EDGES",
	"flasher-names": "FLASHER TEST",
}


def decode_alpha(frame: list[int]) -> str:
	"""Decode WPC alphanumeric segments, keeping the period/comma bit (0x80) as a trailing '.'."""
	text = []
	for value in frame:
		character = harness.SEGMENT_16_CHARACTERS.get(value)
		if character is None and value & 0x80:
			base = harness.SEGMENT_16_CHARACTERS.get(value & ~0x80)
			character = f"{base}." if base is not None else None
		text.append(character if character is not None else "?")
	return "".join(text)


def _angular_distance(a: float, b: float) -> float:
	delta = abs((a - b) % 360.0)
	return min(delta, 360.0 - delta)


def switch_state(model: str, angle: float, window: float) -> int:
	"""Return the public state of switch 67 (1 = closed) at a head angle; face 1 is angle 0."""
	angle %= 360.0
	near = [_angular_distance(angle, face) <= window for face in FACE_ANGLES]
	if model == "faces-open":
		# Contrast model: open within the window around every face, closed everywhere else.
		return 0 if any(near) else 1
	if model == "vpw":
		# VPW 1.0.3 HeadMechCallback: Controller.Switch(67) = currentFace in 1..3.
		return 1 if any(near[:3]) else 0
	if model == "pinned":
		# Position form of bop.c's bop_handleMech tick counters (forward transitions).
		if angle < 60.0 or angle >= 323.0:
			return 1
		if angle <= 90.0:
			return 0
		if angle < 150.0:
			return 1
		if angle <= 180.0:
			return 0
		if angle < 255.0:
			return 1
		return 0
	raise ValueError(model)


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
	texts: dict[int, str] = {}
	solenoids: dict[int, int] = {}
	start = time.monotonic()

	def record(kind: str, **values: Any) -> None:
		with lock:
			events.append({"t": round(time.monotonic() - start, 3), "kind": kind, **values})

	@harness.StateCallback
	def on_state(state: int, _user: int) -> None:
		if state:
			ready.set()

	@harness.DisplayAvailableCallback
	def on_display_available(index: int, count: int, layout: Any, _user: int) -> None:
		return None

	@harness.DisplayUpdatedCallback
	def on_display(index: int, data: int, layout_pointer: Any, _user: int) -> None:
		layout = layout_pointer.contents
		if not data or layout.length <= 0:
			return
		segments = ctypes.cast(data, ctypes.POINTER(ctypes.c_uint16))
		frame = [segments[offset] for offset in range(layout.length)]
		text = decode_alpha(frame)
		with lock:
			changed = texts.get(index) != text
			texts[index] = text
		if changed:
			record("display", index=index, text=text, segments=frame)

	@harness.AudioAvailableCallback
	def on_audio_available(info_pointer: Any, _user: int) -> int:
		return info_pointer.contents.samplesPerFrame

	@harness.AudioUpdatedCallback
	def on_audio(_buffer: int, samples: int, _user: int) -> int:
		return samples

	@harness.SolenoidUpdatedCallback
	def on_solenoid(state_pointer: Any, _user: int) -> None:
		state = state_pointer.contents
		with lock:
			solenoids[state.solNo] = state.state
		if state.solNo in (SOLENOID_RELAY, SOLENOID_MOTOR, 8, 15, 16):
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

	angle = args.initial_angle
	stop = threading.Event()
	motor_log: list[dict[str, Any]] = []
	kicker_log: list[dict[str, Any]] = []
	lamp_log: list[dict[str, Any]] = []
	max_lamps = max(library.PinmameGetMaxLamps(), 1)
	lamp_states = (harness.PinmameLampState * max_lamps)()

	def mech_loop() -> None:
		nonlocal angle
		last = time.monotonic()
		last_switch = None
		last_motor = 0
		last_kickers = {8: 0, 15: 0, 16: 0}
		while not stop.is_set():
			now = time.monotonic()
			dt = now - last
			last = now
			with lock:
				motor = solenoids.get(SOLENOID_MOTOR, 0)
				relay = solenoids.get(SOLENOID_RELAY, 0)
				kickers = {number: solenoids.get(number, 0) for number in last_kickers}
			if motor:
				angle = (angle + (-1.0 if relay else 1.0) * args.speed * dt) % 360.0
			state = switch_state(args.model, angle, args.window)
			if state != last_switch:
				library.PinmameSetSwitch(SWITCH_HEAD, state)
				last_switch = state
			for number, value in kickers.items():
				if value != last_kickers[number]:
					kicker_log.append({"t": round(now - start, 3), "solenoid": number, "state": value, "angle": round(angle, 2), "switch_67": state})
					last_kickers[number] = value
			for index in range(library.PinmameGetChangedLamps(lamp_states)):
				lamp = lamp_states[index]
				if lamp.lampNo >= 91:
					lamp_log.append({"t": round(now - start, 3), "lamp": lamp.lampNo, "state": lamp.state})
			if motor != last_motor:
				motor_log.append({"t": round(now - start, 3), "motor": motor, "relay": relay, "angle": round(angle, 2)})
				last_motor = motor
			time.sleep(0.002)

	thread = threading.Thread(target=mech_loop, daemon=True)
	thread.start()

	def pulse(switch: int, settle: float = 1.2) -> None:
		record("pulse", switch=switch)
		library.PinmameSetSwitch(switch, 1)
		time.sleep(0.15)
		library.PinmameSetSwitch(switch, 0)
		time.sleep(settle)

	def screen() -> str:
		with lock:
			top = "".join(texts.get(i, "") for i in (0, 1, 2))
			bottom = "".join(texts.get(i, "") for i in (3, 4, 5))
		return f"{top} / {bottom}"

	library.PinmameSetSwitch(COIN_DOOR_CLOSED, 1)
	time.sleep(args.boot_wait)
	record("checkpoint", name="boot_complete", screen=screen())
	library.PinmameSetSwitch(COIN_DOOR_CLOSED, 0)
	pulse(SERVICE_ENTER)  # Begin Test -> Game I.D.
	pulse(SERVICE_ENTER)  # Main menu
	for _ in range(8):
		if "TESTS" in screen().upper():
			break
		pulse(SERVICE_UP)
	record("checkpoint", name="main_menu", screen=screen())
	pulse(SERVICE_ENTER)  # enter test menu
	target = TEST_TITLES[args.test]
	for _ in range(20):
		if target in screen().upper():
			break
		pulse(SERVICE_UP, 0.8)
	record("checkpoint", name="head_test_selected", screen=screen())
	pulse(SERVICE_ENTER, args.settle)
	record("checkpoint", name="head_test_entered", screen=screen())
	if args.test == "helmet":
		pulse(SERVICE_ENTER, args.settle)  # ALL LAMPS -> SINGLE LAMP
		record("checkpoint", name="helmet_single_lamp", screen=screen())
	if args.test == "switch-names":
		for address in [column * 10 + row for column in range(1, 9) for row in range(1, 9)]:
			if address in (SWITCH_HEAD, COIN_DOOR_CLOSED):
				continue
			library.PinmameSetSwitch(address, 1)
			time.sleep(args.settle)
			record("checkpoint", name=f"switch_{address}_closed", screen=screen())
			library.PinmameSetSwitch(address, 0)
			time.sleep(args.settle)
	else:
		for step in range(args.steps):
			pulse(SERVICE_UP, args.settle)
			record("checkpoint", name=f"after_up_{step + 1}", screen=screen(), angle=round(angle, 2))
	stop.set()
	thread.join()
	library.PinmameStop()
	time.sleep(0.5)
	return {
		"format": "bop-head-mech-experiment",
		"version": 1,
		"game": args.game,
		"model": args.model,
		"window_degrees": args.window,
		"speed_degrees_per_second": args.speed,
		"initial_angle": args.initial_angle,
		"library_sha256": hashlib.sha256(dll_path.read_bytes()).hexdigest(),
		"rom_archive_sha256": hashlib.sha256((rom_path / f"{args.game}.zip").read_bytes()).hexdigest(),
		"tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		"test": args.test,
		"motor_edges": motor_log,
		"kicker_edges": kicker_log,
		"helmet_lamp_changes": lamp_log,
		"events": events,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--library", type=Path, required=True)
	parser.add_argument("--rom-path", type=Path, required=True)
	parser.add_argument("--work-dir", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--game", default="bop_l7")
	parser.add_argument("--model", choices=("faces-open", "vpw", "pinned"), required=True)
	parser.add_argument("--window", type=float, default=10.0, help="half-width in degrees of a face indentation")
	parser.add_argument("--speed", type=float, default=30.0, help="modelled head speed in degrees per second")
	parser.add_argument("--initial-angle", type=float, default=0.0)
	parser.add_argument("--boot-wait", type=float, default=45.0)
	parser.add_argument("--settle", type=float, default=12.0)
	parser.add_argument("--steps", type=int, default=5)
	parser.add_argument("--test", choices=tuple(TEST_TITLES), default="motor-switch")
	parser.add_argument("--ready-timeout", type=float, default=15.0)
	args = parser.parse_args()
	result = run(args)
	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
