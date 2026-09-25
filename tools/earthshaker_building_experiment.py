"""Probe how an Earthshaker ROM drives the optional sinking Institute building.

Production Earthshakers ship with a static building, but the esha_la3 and esha_pa1 ROMs run here
still energize solenoid 9 (the building motor relay on the PA prototypes) when the game enters
Game-Over mode.
Held static, switches 25/26 (the prototype building-height optos) never stop that pulse, so the
ROM is waiting for them to change. This tool boots a ROM from a new, empty state directory,
reaches Game-Over mode through the Ad 70 exit the manual describes, and while solenoid 9 is on
moves a modelled building and rewrites switches 25/26 from it. It records when the ROM releases
solenoid 9 and which switch pattern the model presented at that moment.

The model is a host-side hypothesis, not physical evidence: the building travels between its two
limits at a fixed speed while solenoid 9 is on, reverses at each limit, and presents one switch
pattern per quarter of its travel. ``--pattern`` gives the four (25,26) states from the top limit
downwards, e.g. ``01,00,10,11`` (the retained VPW table's model). What the run shows is only which
presented pattern the ROM accepts as a stopping point.
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


def run(args: argparse.Namespace) -> dict[str, Any]:
	dll_path = args.library.resolve(strict=True)
	rom_path = args.rom_path.resolve(strict=True)
	work_dir = args.work_dir.resolve()
	if work_dir.exists() and any(work_dir.iterdir()):
		raise RuntimeError(f"work directory must be new and empty: {work_dir}")
	for child in ("nvram", "cfg", "hi"):
		(work_dir / child).mkdir(parents=True, exist_ok=True)
	pattern = [tuple(int(bit) for bit in item) for item in args.pattern.split(",")]
	if len(pattern) != 4 or any(len(item) != 2 for item in pattern):
		raise RuntimeError("--pattern needs four two-bit states, e.g. 01,00,10,11")
	library = ctypes.CDLL(str(dll_path))
	harness._configure_api(library)
	ready = threading.Event()
	lock = threading.Lock()
	events: list[dict[str, Any]] = []
	start = time.monotonic()
	motor = {"on": False}

	def record(kind: str, **values: Any) -> None:
		with lock:
			events.append({"t": round(time.monotonic() - start, 3), "kind": kind, **values})

	@harness.StateCallback
	def on_state(state: int, _user: int) -> None:
		if state:
			ready.set()

	@harness.DisplayAvailableCallback
	def on_display_available(_index: int, _count: int, _layout: Any, _user: int) -> None:
		return None

	@harness.DisplayUpdatedCallback
	def on_display(_index: int, _data: int, _layout: Any, _user: int) -> None:
		return None

	@harness.AudioAvailableCallback
	def on_audio_available(info_pointer: Any, _user: int) -> int:
		return info_pointer.contents.samplesPerFrame

	@harness.AudioUpdatedCallback
	def on_audio(_buffer: int, samples: int, _user: int) -> int:
		return samples

	@harness.SolenoidUpdatedCallback
	def on_solenoid(state_pointer: Any, _user: int) -> None:
		state = state_pointer.contents
		if state.solNo == 9:
			motor["on"] = bool(state.state)
		record("solenoid", number=state.solNo, state=state.state)

	@harness.KeyPressedCallback
	def is_key_pressed(_keycode: int, _user: int) -> int:
		return 0

	@harness.SoundCommandCallback
	def on_sound(_board: int, _command: int, _user: int) -> None:
		return None

	config = harness.PinmameConfig(
		audioFormat=0, sampleRate=44100, vpmPath=harness._path_bytes(work_dir) + os.sep.encode("ascii"),
		cb_OnStateUpdated=on_state, cb_OnDisplayAvailable=on_display_available, cb_OnDisplayUpdated=on_display,
		cb_OnAudioAvailable=on_audio_available, cb_OnAudioUpdated=on_audio, cb_OnMechAvailable=None, cb_OnMechUpdated=None,
		cb_OnSolenoidUpdated=on_solenoid, cb_OnConsoleDataUpdated=None, fn_IsKeyPressed=is_key_pressed,
		cb_OnLogMessage=None, cb_OnSoundCommand=on_sound,
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

	# Building position: 0.0 = top limit, 1.0 = bottom limit.
	model = {"position": args.initial_position, "direction": 1.0, "zone": None}

	def zone_of(position: float) -> int:
		return min(3, int(position * 4))

	def apply_zone() -> None:
		zone = zone_of(model["position"])
		if zone != model["zone"]:
			model["zone"] = zone
			library.PinmameSetSwitch(25, pattern[zone][0])
			library.PinmameSetSwitch(26, pattern[zone][1])
			record("building", position=round(model["position"], 3), zone=zone, sw25=pattern[zone][0], sw26=pattern[zone][1])

	for switch, state in ((-6, 0), (11, 1), (12, 1), (13, 1)):
		library.PinmameSetSwitch(switch, state)
	apply_zone()
	stop = threading.Event()

	def mover() -> None:
		last = time.monotonic()
		while not stop.is_set():
			now = time.monotonic()
			if motor["on"]:
				model["position"] += model["direction"] * (now - last) / args.travel_s
				if model["position"] >= 1.0:
					model["position"], model["direction"] = 1.0, -1.0
				elif model["position"] <= 0.0:
					model["position"], model["direction"] = 0.0, 1.0
				apply_zone()
			last = now
			time.sleep(0.005)

	thread = threading.Thread(target=mover, daemon=True)
	thread.start()

	def press(switch: int, settle: float) -> None:
		record("action", type="press", switch=switch)
		library.PinmameSetSwitch(switch, 1)
		time.sleep(0.15)
		library.PinmameSetSwitch(switch, 0)
		time.sleep(settle)

	time.sleep(args.boot_wait)
	record("checkpoint", name="boot_complete")
	press(-7, 2.0)
	press(-7, 2.0)
	library.PinmameSetSwitch(-6, 1)
	record("action", type="set", switch=-6, state=1)
	time.sleep(0.2)
	press(-7, args.attract_wait)
	record("checkpoint", name="game_over_observed")
	if args.start_game:
		press(4, 1.0)
		press(3, args.game_wait)
		record("checkpoint", name="game_observed")
	stop.set()
	thread.join()
	library.PinmameStop()
	time.sleep(0.5)
	return {
		"format": "earthshaker-building-experiment",
		"version": 1,
		"game": args.game,
		"library_sha256": hashlib.sha256(dll_path.read_bytes()).hexdigest(),
		"rom_archive_sha256": hashlib.sha256((rom_path / f"{args.game}.zip").read_bytes()).hexdigest(),
		"tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		"pattern_top_to_bottom": args.pattern,
		"travel_s": args.travel_s,
		"initial_position": args.initial_position,
		"boot_wait_s": args.boot_wait,
		"events": events,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--library", type=Path, required=True)
	parser.add_argument("--rom-path", type=Path, required=True)
	parser.add_argument("--work-dir", type=Path, required=True)
	parser.add_argument("--output", type=Path, required=True)
	parser.add_argument("--game", default="esha_la3")
	parser.add_argument("--pattern", default="01,00,10,11")
	parser.add_argument("--travel-s", type=float, default=3.0)
	parser.add_argument("--initial-position", type=float, default=0.5)
	parser.add_argument("--boot-wait", type=float, default=20.0)
	parser.add_argument("--attract-wait", type=float, default=15.0)
	parser.add_argument("--game-wait", type=float, default=15.0)
	parser.add_argument("--start-game", action="store_true")
	parser.add_argument("--ready-timeout", type=float, default=15.0)
	args = parser.parse_args()
	result = run(args)
	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8", newline="\n")
	print(f"wrote {args.output}")


if __name__ == "__main__":
	main()
