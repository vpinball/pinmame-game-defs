"""Summarize the retained Class of 1812 harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/gottlieb.class-of-1812.1991/runtime/`` (written by ``tools/run_pinmame_harness.py`` with the pinned
library: the ``nvram-init`` run from an empty state directory, every other run from a new state directory holding only
that run's initialized NVRAM), checks that every run succeeded on the pinned emulator binary with an unchanged committed
scenario, reads the text of the two 20-character alphanumeric displays from each snapshot's recorded segments and writes
``evidence/runtime/gts3/class-of-1812-clas1812-service-tests.json``: the Lamp Matrix, Relay & Solenoid and Switch Matrix
tests, each step paired with the public address it drove or the host held, plus the Front Door Test, one scripted game
and two tilt probes of the trough switch 44 that differ only in whether the host opens 44 while the ball is out.

The ROM's font draws the digit 0 like the letter O and 5 like S, so the harness's segment table prints them as letters.
It marks a comma either as a cell of its own (segment 0x4000) or by lighting the comma segments 0x8080 beside a character;
``display_line`` reads the first as a comma and the second as the harness's character followed by a comma, and leaves any
other cell the harness does not name as ``?``. ``read_number`` folds the two-character index after ``=`` (with A and B for
the tens 10 and 11), and ``fold_name`` folds a name token made only of those glyphs, digits and commas when it holds a digit
or a comma, follows BONUS or ends in X.
A Lamp Matrix step pairs the displayed number with the one lamp that blinked during the step; a Relay & Solenoid step
pairs the displayed driver with the output its credit-button press fired; a Switch Matrix step reads the frame taken while
the host held the address at 1. A pairing that disagrees with the expected arithmetic stops the build. ``--check``
re-derives everything and refuses any drift.

    python tools/class_of_1812_runtime_evidence.py            # write
    python tools/class_of_1812_runtime_evidence.py --check    # re-derive and compare, write nothing
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)
_harness_spec = importlib.util.spec_from_file_location("run_pinmame_harness", TOOLS / "run_pinmame_harness.py")
harness = importlib.util.module_from_spec(_harness_spec)
assert _harness_spec.loader is not None
_harness_spec.loader.exec_module(harness)

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
MACHINE_ID = "gottlieb.class-of-1812.1991"
GAME = "clas1812"
ROM_ARCHIVE_SHA256 = "a924f9a05395a0f3014948f2adfbf0ae3357224c0c2019bee61e5e2aac8b6360"
SCENARIO_DIRECTORY = "tools/harness-scenarios/gts3"
RUNS = ("nvram-init", "lamp-matrix", "solenoids", "switch-matrix", "front-door", "gameplay", "tilt-trough-closed", "tilt-trough-open")
RUNTIME_RELATIVE = Path("gottlieb.class-of-1812.1991/runtime")
SOURCE_PATH = "external:pinmame-review-artifacts/gottlieb.class-of-1812.1991/runtime"
EVIDENCE_PATH = ROOT / "evidence/runtime/gts3/class-of-1812-clas1812-service-tests.json"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, every saved display frame, and every state-directory file including the inherited and "
	"written NVRAM) except manifest.json and manifest.sha256, sorted by POSIX relative path. "
	"tools/build_external_evidence_manifest.py writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game clas1812 --rom-path <vpinmame-roms> "
	"--work-dir <state-directory> --scenario tools/harness-scenarios/gts3/class-of-1812-<name>.json --dmd-dir <frames> "
	"--output <external-run.json>. The nvram-init run starts from an empty state directory (state-init-clas1812) and loads "
	"factory settings; every other run starts from a new state directory (states/clas1812-<name>) holding only that NVRAM. "
	"Every scenario sets switch_converter gts3, so the harness checks PINMAME_HARDWARE_GEN_GTS3 before touching a switch."
)
FLIPPER_SYNTHETIC = {45, 46, 47, 48}
# The comma as a cell of its own, and the comma segments this ROM lights beside a character.
COMMA_CELL = 0x4000
COMMA_SEGMENTS = 0x8080
SERVICE_LIMITATION = "A pulsed address is ROM activity, not proof that a load is fitted."
SWITCH_LIMITATION = (
	"The Switch Matrix Test names the switch the ROM sees closed, so a name shown while the host holds an address at 1 proves "
	"that the ROM scans that address under that name and reads 1 as closed; it does not show how the contact is built."
)
STATIC_LIMITATION = (
	"The host answers the ROM with fixed, scripted switch changes; it never moves a ball or a mechanism, so a pulse the ROM "
	"fires proves only that the address changed under these conditions."
)


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


def glyph(char: str, segments: int) -> str:
	if char != "?":
		return char
	if segments == COMMA_CELL:
		return ","
	base = harness.SEGMENT_16_CHARACTERS.get(segments & ~COMMA_SEGMENTS) if segments & COMMA_SEGMENTS == COMMA_SEGMENTS else None
	return base + "," if base else "?"


def display_line(display: dict[str, Any]) -> str:
	"""The harness's text for one alphanumeric display, with the comma cells it prints as ? read from their segments."""
	text = display["text"]
	if len(text) != len(display["segments"]):
		raise RuntimeError(f"display {display['index']}: text and segments differ in length")
	return "".join(glyph(char, segments) for char, segments in zip(text, display["segments"])).strip()


def read_number(text: str) -> int:
	"""The index after '=': O reads 0, S reads 5, and a leading A or B is the tens digit 10 or 11."""
	text = text.replace("O", "0").replace("S", "5").replace(" ", "")
	if not re.fullmatch(r"[0-9AB]?[0-9]", text):
		raise RuntimeError(f"unreadable index {text!r}")
	tens = ({"A": 10, "B": 11}[text[0]] if text[0] in "AB" else int(text[0])) if len(text) == 2 else 0
	return tens * 10 + int(text[-1])


def fold_name(name: str) -> str:
	tokens = name.split()
	out = []
	for index, token in enumerate(tokens):
		if re.fullmatch(r"[0-9OS,]+X?", token) and (
			re.search(r"[0-9,]", token) or token.endswith("X") or (index and tokens[index - 1] == "BONUS")
		):
			token = token.replace("O", "0").replace("S", "5")
		out.append(token)
	return " ".join(out)


def labelled(lines: list[str], title: str) -> tuple[int, str] | None:
	"""(number, name) from a service-test screen whose first line is title and whose second reads 'NAME =nn'."""
	if len(lines) != 2 or lines[0] != title:
		return None
	match = re.fullmatch(r"(.*?)\s*=\s*([0-9OSAB ]{1,3})", lines[1])
	if not match:
		return None
	return read_number(match.group(2)), fold_name(match.group(1).strip())


class Run:
	def __init__(self, runtime: Path, name: str) -> None:
		self.name = name
		self.path = runtime / "runs" / f"{GAME}-{name}.json"
		self.data = json.loads(self.path.read_text(encoding="utf-8"))
		self.scenario_path = f"{SCENARIO_DIRECTORY}/class-of-1812-{name}.json"
		scenario_bytes = (ROOT / self.scenario_path).read_bytes()
		if self.data.get("failure"):
			raise RuntimeError(f"{self.path.name}: the run failed: {self.data['failure']}")
		if self.data.get("library_sha256") != LIBRARY_SHA256:
			raise RuntimeError(f"{self.path.name}: not recorded on the pinned library")
		if self.data.get("game") != GAME:
			raise RuntimeError(f"{self.path.name}: recorded for {self.data.get('game')!r}")
		if self.data["scenario"]["sha256"] != hashlib.sha256(scenario_bytes).hexdigest():
			raise RuntimeError(f"{self.path.name}: the committed scenario changed since the run")
		if self.data.get("switch_converter") != "gts3":
			raise RuntimeError(f"{self.path.name}: not run with the gts3 switch converter")
		snapshots = self.data["snapshots"]
		texts = []
		for index, snapshot in enumerate(snapshots):
			alpha = [display for display in snapshot.get("displays") or [] if "segments" in display]
			if [display["index"] for display in alpha] != [0, 1]:
				raise RuntimeError(f"{self.path.name}: snapshot {index} does not carry the two alphanumeric displays")
			texts.append([display_line(display) for display in alpha])
		# Snapshot 0 is the boot snapshot; step n's settle snapshot follows it, and a step with a held snapshot adds one
		# more just before. Pair them by label in order.
		self.boot_text = texts[0]
		self.step_text: dict[int, list[str]] = {}
		self.step_held_text: dict[int, list[str]] = {}
		cursor = 1
		for step in self.data["steps"]:
			if cursor < len(snapshots) and snapshots[cursor]["label"] == f"{step['label']} (held)":
				self.step_held_text[step["step"]] = texts[cursor]
				cursor += 1
			if cursor >= len(snapshots) or snapshots[cursor]["label"] != step["label"]:
				raise RuntimeError(f"{self.path.name}: no settle snapshot for step {step['step']} ({step['label']})")
			self.step_text[step["step"]] = texts[cursor]
			cursor += 1
		if cursor != len(snapshots):
			raise RuntimeError(f"{self.path.name}: {len(snapshots) - cursor} snapshots left unpaired")

	def raw_record(self, nvram_note: str) -> dict[str, Any]:
		scenario = json.loads((ROOT / self.scenario_path).read_text(encoding="utf-8"))
		record: dict[str, Any] = {
			"name": self.name,
			"sha256": sha256(self.path),
			"scenario_path": self.scenario_path,
			"scenario_sha256": self.data["scenario"]["sha256"],
			"action_count": len(scenario["actions"]),
			"self_test_pulses": sum(1 for action in scenario["actions"] if action.get("switch") == -8),
			"nvram_initialization": nvram_note,
			"snapshot_count": len(self.data["snapshots"]),
			"watch_switches": self.data["watch_switches"],
		}
		if self.data.get("initial_switches"):
			record["initial_switches"] = self.data["initial_switches"]
		return record

	def solenoid_events(self, numbers: set[int]) -> list[tuple[int, int, float]]:
		return [
			(event["number"], event["state"], event["time_s"]) for event in self.data["events"]
			if event.get("event") == "solenoid" and event["number"] in numbers
		]


def solenoids_on(step: dict[str, Any]) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["solenoids"] if 1 in item["states"])


def blinking_lamps(step: dict[str, Any], minimum: int = 3) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["lamps"] if len(item["states"]) >= minimum)


MATRIX = [column * 10 + row for column in range(12) for row in range(8)]


def lamp_matrix(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	for step in run.data["steps"]:
		if not step["label"].startswith("advance: lamp step") and step["label"] != "lamp 00 settle":
			continue
		found = labelled(run.step_text[step["step"]], "LAMP MATRIX TEST")
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no lamp number")
		number, name = found
		blinking = blinking_lamps(step)
		if blinking != [number]:
			raise RuntimeError(f"{run.path.name}: lamp {number} blinked {blinking}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: lamp {number} named {names[number]!r} and {name!r}")
		names[number] = name
	if sorted(names) != MATRIX:
		raise RuntimeError(f"{run.path.name}: the walk did not cover every lamp: {sorted(set(MATRIX) - set(names))}")
	observation = {
		"diagnostic_checkpoints": [{"after_service_pulses": 4, "matched_text": "LAMP MATRIX TEST"}],
		"limitation": SERVICE_LIMITATION,
		"note": (
			"Self-test 4 stepped forward with public 5; after =B7 the walk wraps to =00. In every step exactly one public lamp "
			"blinked (three or more state changes) and it was the displayed number, A0-B7 meaning 100-117. Address = name: "
			+ "; ".join(f"{number} = {names[number]}" for number in MATRIX) + "."
		),
	}
	return names, observation


def solenoid_test(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	addresses: dict[int, int] = {}
	extras: dict[int, list[int]] = {}
	sequence: list[int] = []
	for step in run.data["steps"]:
		if not step["label"].startswith("credit button: fire solenoid"):
			continue
		found = labelled(run.step_text[step["step"]], "RELAY+SOLENOID TEST")
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no driver number")
		number, name = found
		fired = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		target = number + 1
		if target not in fired:
			raise RuntimeError(f"{run.path.name}: driver {number} fired {fired}, not {target}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: driver {number} named {names[number]!r} and {name!r}")
		names[number] = name
		addresses[number] = target
		others = [address for address in fired if address != target]
		if others:
			extras[number] = others
		sequence.append(target)
	if sorted(names) != list(range(32)):
		raise RuntimeError(f"{run.path.name}: the walk did not cover drivers 0-31")
	note = (
		"Self-test 5: public 5 steps the displayed driver number and public 3 (the credit button) fires it; the solenoid that "
		"rose on each press is the displayed number plus 1. Driver = public solenoid: name: "
		+ "; ".join(f"{number} = {addresses[number]}: {names[number]}" for number in sorted(names))
		+ "."
	)
	if extras:
		note += " Also rising during the press: " + "; ".join(
			f"driver {number}: {', '.join(str(address) for address in others)}" for number, others in sorted(extras.items())
		) + "."
	observation: dict[str, Any] = {
		"limitation": SERVICE_LIMITATION,
		"note": note,
		"ordered_solenoid_on_sequence": sequence,
		"solenoid_addresses_seen": sorted(set(sequence) | {address for others in extras.values() for address in others}),
	}
	return names, observation


def switch_matrix(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	silent: list[int] = []
	texts: dict[int, list[str]] = {}
	idle = None
	for step in run.data["steps"]:
		if step["label"] == "switch matrix test idle":
			idle = " / ".join(run.step_text[step["step"]])
		match = re.fullmatch(r"close switch (-?\d+)(?: through flipper button (141|143))?", step["label"])
		if not match:
			continue
		address = int(match.group(1))
		held = run.step_held_text[step["step"]]
		texts[address] = held
		found = labelled(held, "SWITCH MATRIX TEST")
		if found is None:
			silent.append(address)
			continue
		number, name = found
		if number != address:
			if address >= 0 and address != 3:
				raise RuntimeError(f"{run.path.name}: holding {address} showed switch {number}")
			silent.append(address)
			continue
		names[address] = name
	if idle != "SWITCH MATRIX TEST / ALL SWITCHES OPEN":
		raise RuntimeError(f"{run.path.name}: the Switch Matrix Test was not idle before the walk: {idle!r}")
	note = (
		"Self-test 6 shows SWITCH MATRIX TEST / ALL SWITCHES OPEN before the walk. With each address held at 1 alone for "
		"400 ms (6 and 7 through the flipper buttons 143 and 141 that core_updateSw copies into them), the frame taken while "
		"held shows the ROM's name and =nn (A0-B7 meaning 100-117), and nn was the held address every time. Address = name: "
		+ "; ".join(f"{address} = {names[address]}" for address in sorted(names))
		+ "."
	)
	if silent:
		note += (
			" No line of its own while held: "
			+ ", ".join(f"{address} (\"{' / '.join(texts[address])}\")" for address in silent) + "."
		)
	return names, {"limitation": SWITCH_LIMITATION, "note": note, "switch_addresses_observed_while_held": sorted(names)}


def step_notes(run: Run) -> list[str]:
	notes = []
	for step in run.data["steps"]:
		on = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		synthetic = [address for address in solenoids_on(step) if address in FLIPPER_SYNTHETIC]
		text = " / ".join(line for line in run.step_text[step["step"]] if line)
		part = f"{step['step']} {step['label']}: solenoids rising {on or 'none'}"
		if synthetic:
			part += f", synthetic flipper outputs {synthetic}"
		if text:
			part += f"; display \"{text}\""
		notes.append(part)
	return notes


def scripted(run: Run, summary: str, timed: set[int] | None = None) -> dict[str, Any]:
	seen = sorted({address for step in run.data["steps"] for address in solenoids_on(step)})
	observation = {"limitation": STATIC_LIMITATION, "note": summary + " Steps: " + "; ".join(step_notes(run)) + ".", "solenoid_addresses_seen": seen}
	if timed:
		events = ", ".join(f"{number} {'on' if state else 'off'} at {time} s" for number, state, time in run.solenoid_events(timed))
		observation["note"] += f" Solenoid edges of {sorted(timed)}, timed from the start of the run: {events}."
	return observation


FRONT_DOOR_COUNTERS = re.compile(r"L- ?([\dO]+) +C- ?([\dO]+) +R- ?([\dO]+)")
# Which counter each coin switch advances in the Front Door Test: 0 the left, 1 the right and 2 the center chute.
FRONT_DOOR_CHUTES = {0: 0, 1: 2, 2: 1}


# The coin switches the Front Door Test run presses, in order.
FRONT_DOOR_COIN_PRESSES = [0, 1, 2, 0]


def front_door(run: Run) -> dict[str, Any]:
	"""Self-test 9. Fails closed unless every frame from the test's entry on reads FRONT DOOR TEST, the run presses coin
	switches 0, 1, 2 and 0, and each press advances only its own chute's counter in the held and the settled frame."""
	counts = []
	previous: list[int] | None = None
	presses: list[int] = []
	in_test = False
	for step in run.data["steps"]:
		number = step["step"]
		frames = [frame for frame in (run.step_held_text.get(number), run.step_text.get(number)) if frame]
		lines = frames[0] if frames else []
		counts.append(f"{step['label']}: \"{' / '.join(line for line in lines if line)}\"")
		in_test = in_test or step["label"].startswith("test button: self-test 9")
		if not in_test or step.get("switch") == -6:
			continue
		coin = step.get("switch") if step.get("switch") in FRONT_DOOR_CHUTES else None
		expected = None
		if coin is not None:
			presses.append(coin)
			expected = list(previous or [0, 0, 0])
			expected[FRONT_DOOR_CHUTES[coin]] += 1
		if not frames:
			raise RuntimeError(f"front-door step {number} ({step['label']}) has no display frame")
		if coin is not None and len(frames) != 2:
			raise RuntimeError(f"front-door step {number} ({step['label']}) lacks its held or its settled frame")
		readings = []
		for frame in frames:
			if frame[0].strip() != "FRONT DOOR TEST":
				raise RuntimeError(f"front-door step {number} ({step['label']}) does not show the FRONT DOOR TEST page: {frame}")
			match = FRONT_DOOR_COUNTERS.search(frame[1] if len(frame) > 1 else "")
			if not match:
				raise RuntimeError(f"front-door step {number} shows no L/C/R counters: {frame}")
			readings.append([int(value.replace("O", "0")) for value in match.groups()])
		current = readings[-1]
		if any(reading != current for reading in readings):
			raise RuntimeError(f"front-door step {number} ({step['label']}) shows different counters in its frames: {readings}")
		if expected is not None and current != expected:
			raise RuntimeError(f"front-door step {number} ({step['label']}) moved the counters to {current}, expected {expected}")
		if expected is None and previous is not None and current != previous:
			raise RuntimeError(f"front-door step {number} ({step['label']}) changed the counters without a coin: {current}")
		previous = current
	if previous is None:
		raise RuntimeError("the front-door run never reached the FRONT DOOR TEST page")
	if presses != FRONT_DOOR_COIN_PRESSES:
		raise RuntimeError(f"the front-door run pressed coin switches {presses}, expected {FRONT_DOOR_COIN_PRESSES}")
	return {"limitation": STATIC_LIMITATION, "note": "Self-test 9; display after each step: " + "; ".join(counts) + "."}


TROUGH_TIMED = {8, 9, 28, 29, 32}


def trough_probe(run: Run, summary: str) -> tuple[dict[str, Any], list[str]]:
	"""A tilt probe: which tilt pulse the ROM tilted on, and the steps on which it served a ball (28) or kicked the outhole (29).

	Returns the observation and the labels of the steps on which 28 rose; the step numbers live in the note, because the
	evidence schema admits no other field for them.
	"""
	served = [step["step"] for step in run.data["steps"] if 28 in solenoids_on(step)]
	kicked = [step["step"] for step in run.data["steps"] if 29 in solenoids_on(step)]
	tilted = [step["step"] for step in run.data["steps"] if step["label"].startswith("tilt switch") and 26 in solenoids_on(step)]
	observation = scripted(run, summary + f" Ball release 28 rose on steps {served}, outhole 29 on steps {kicked}, and the tilt relays 26/31 on tilt steps {tilted}.", TROUGH_TIMED)
	labels = {step["step"]: step["label"] for step in run.data["steps"]}
	return observation, [labels[number] for number in served]


def build(root: Path) -> dict[str, Any]:
	runtime = root / RUNTIME_RELATIVE
	manifest_sha = manifests.check_manifest(runtime, GAME)
	if manifest_sha != sha256(runtime / "manifest.json"):
		raise RuntimeError("the retained manifest digest does not match manifest.json")
	runs = {name: Run(runtime, name) for name in RUNS}
	init_nv = runtime / f"state-init-{GAME}" / "nvram" / f"{GAME}.nv"
	init_note = f"Fresh state directory holding only nvram/{GAME}.nv (SHA-256 {sha256(init_nv)}) from the nvram-init run."
	raw = [runs["nvram-init"].raw_record(f"Empty state directory state-init-{GAME}; this run loads factory settings and its NVRAM is the only state any later run inherits.")]
	raw += [runs[name].raw_record(init_note) for name in RUNS[1:]]
	observations: dict[str, Any] = {}
	boot = " / ".join(runs["nvram-init"].boot_text)
	if re.sub(r"\s+", " ", boot) != "CLASS OF 1812 / 73O 88FB":
		raise RuntimeError(f"unexpected power-up screen: {boot!r}")
	observations["nvram-init"] = {
		"limitation": STATIC_LIMITATION,
		"note": (
			f"The power-up screen reads \"{boot}\", the game number 730 (the font's 0 is drawn like O) and the ROM checksum "
			"88FB. Displays after each step: "
			+ "; ".join(f"\"{' / '.join(line for line in text if line)}\"" for text in runs["nvram-init"].step_text.values()) + "."
		),
	}
	lamp_names, observations["lamp-matrix"] = lamp_matrix(runs["lamp-matrix"])
	sol_names, observations["solenoids"] = solenoid_test(runs["solenoids"])
	_, observations["switch-matrix"] = switch_matrix(runs["switch-matrix"])
	observations["front-door"] = front_door(runs["front-door"])
	observations["gameplay"] = scripted(
		runs["gameplay"], (
			"One game started with two coins on public 1 and the trough switch (44) closed. The scenario's step labels predate "
			"the trough probes: 'ball at the trough release' and 'ball back at the trough release' name the host closing 44, "
			"which the probes show the ROM reads as both balls home, and 'outhole kicked' names the host opening 54, not a "
			"coil; the ROM fired the outhole coil 29 only after the host had closed 44 again (step 71)."
		),
		{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 28, 29, 32},
	)
	observations["tilt-trough-closed"], closed_served = trough_probe(
		runs["tilt-trough-closed"], "One game with the trough switch 44 held closed throughout; the tilt switch -7 is pulsed six times before the ball drains.",
	)
	observations["tilt-trough-open"], open_served = trough_probe(
		runs["tilt-trough-open"], (
			"The same sequence with two extra writes, each followed by a 0.5 s settle: 44 opened once the ball was released "
			"and closed again only after the drained ball left the outhole 54."
		),
	)
	closed_expected = ["start", "tilt switch -7 pulse 3", "tilt switch -7 pulse 6", "ball on the outhole switch 54"]
	if closed_served != closed_expected or open_served != ["start", "idle after the drain 1"]:
		raise RuntimeError(f"the trough probes no longer show the tilt behaviour they were recorded for: {closed_served}, {open_served}")
	named = {}
	for number, name in sorted(lamp_names.items()):
		named[f"lamp-{number:03d}-{slug(name) or 'unnamed'}"] = number
	for number, name in sorted(sol_names.items()):
		named[f"solenoid-{number:02d}-{slug(name)}"] = number + 1
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "class-of-1812-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": SOURCE_PATH,
			"sha256": manifest_sha,
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes, NVRAM and display frames remain external.",
			"quality": "observed",
			"manifest_algorithm": MANIFEST_ALGORITHM,
		},
		"driver_ids": [GAME],
		"machine_ids": [MACHINE_ID],
		"switches": [],
		"outputs": [],
		"states": [],
		"mechanisms": [],
		"recreation_notes": [],
		"runtime": {
			"game": GAME,
			"rom_archive_sha256": ROM_ARCHIVE_SHA256,
			"emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": REVISION},
			"raw_runs": raw,
			"command_template": COMMAND_TEMPLATE,
			"observations": {
				"service_language": "English",
				"named_output_addresses": named,
				"solenoid_addresses_seen": sorted({address for step in runs["solenoids"].data["steps"] for address in solenoids_on(step)}),
				"runs": observations,
			},
		},
	}


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="re-derive the bundle and refuse drift, writing nothing")
	args = parser.parse_args()
	expected = canonical_bytes(build(working_root()))
	if args.check:
		if not EVIDENCE_PATH.is_file() or EVIDENCE_PATH.read_bytes() != expected:
			print("drift: " + EVIDENCE_PATH.relative_to(ROOT).as_posix())
			return 1
		print("Class of 1812 runtime evidence matches the retained runs.")
		return 0
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(expected)
	print(f"wrote {EVIDENCE_PATH.relative_to(ROOT).as_posix()}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
