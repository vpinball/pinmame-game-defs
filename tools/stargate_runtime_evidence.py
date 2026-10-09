"""Summarize the retained Stargate harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/gottlieb.stargate.1995/runtime/`` (written by ``tools/run_pinmame_harness.py`` with the
pinned library: each set's ``nvram-init`` run from an empty state directory, every other run from a new
state directory holding only that set's initialized NVRAM), checks that every run succeeded on the pinned
emulator binary with an unchanged committed scenario, reads the DMD text of every snapshot with
``tools/gts3_dmd_text.py`` and writes one bundle per ROM set:

* ``evidence/runtime/gts3/stargate-<set>-service-tests.json``: the set's Lamp Matrix, Relay & Solenoid,
  Aux Driver and Switch Edges tests, each step paired with the public address it drove or the host held;
  for ``stargat5`` also the Front Door Test, the tournament/coin-door probe, a gameplay run and a
  mechanism-sensor run. Every other set's names are compared with ``stargat5``'s.

A Lamp Matrix step pairs the displayed ``LAMP:nn`` with the one lamp that blinked during the step; a
Relay & Solenoid or Aux Driver step pairs the displayed driver with the output its credit-button press
fired; a Switch Edges step reads the frame taken while the host held the address at 1. A pairing that
disagrees with the expected arithmetic stops the build. ``--check`` re-derives everything and refuses any
drift.

    python tools/stargate_runtime_evidence.py            # write
    python tools/stargate_runtime_evidence.py --check    # re-derive and compare, write nothing
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
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(ROOT / "src"))

import gts3_dmd_text  # noqa: E402
from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
MACHINE_ID = "gottlieb.stargate.1995"
PRIMARY = "stargat5"
SETS = ("stargat5", "stargate", "stargat4", "stargat3", "stargat2", "stargat1")
ROM_ARCHIVE_SHA256 = {
	"stargat5": "b7148ab6a75e451ea78aa2a7b76a5c246b3c758b3aaee061db1f9628b616073c",
	"stargate": "00d69489c5ebe9529a88ad9950e8f5cabc013dd97d5b1e865d7994ae7826aee0",
	"stargat4": "455b0b7c3dede0f146214e0637ffe1c14b72b0e422c799973d03858c9a8aacec",
	"stargat3": "f2f35b651cc8af19e5708fb221ee5a25c08d6135a6265d6b845653b7974cf091",
	"stargat2": "9674174f17999408b98b5a73611dfbf02f47ae708a76fe9f5d7f1487a3d3ec6f",
	"stargat1": "114215235bbca64739f19fbca3a878c6497f4e60e2d2258a39e8280ce0036f42",
}
SCENARIO_DIRECTORY = "tools/harness-scenarios/gts3"
# The power-up frame's third line, read from the retained frames by eye; the builder pins each frame's pixel digest.
BOOT_SCREENS = {
	"stargat5": "STARGATE / (Install 4 Balls) / Game #742/5, ID #000000",
	"stargate": "STARGATE / (Install 4 Balls) / Game #742, ID #000000",
	"stargat4": "STARGATE / (Install 4 Balls) / Game #742/4, ID #000000",
	"stargat3": "STARGATE / (Install 4 Balls) / Game #742/3, ID #000000",
	"stargat2": "STARGATE / (Install 4 Balls) / Game #742/2, ID #000000",
	"stargat1": "STARGATE / (Install 4 Balls) / Game #742/1, ID #000000",
}
SERVICE_RUNS = ("nvram-init", "lamp-matrix", "solenoids", "aux-drivers", "switch-edges")
PRIMARY_RUNS = SERVICE_RUNS + ("front-door", "tournament-door", "gameplay", "mechanism-sensors")
RUNTIME_RELATIVE = Path("gottlieb.stargate.1995/runtime")
SOURCE_PATH = "external:pinmame-review-artifacts/gottlieb.stargate.1995/runtime"
# The game field tools/build_external_evidence_manifest.py --game records for this six-set directory.
MANIFEST_GAME = "stargate"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, every saved DMD frame, and every state-directory file including the inherited and written "
	"NVRAM) except manifest.json and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py "
	"writes and re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <set> --rom-path <vpinmame-roms> "
	"--work-dir <state-directory> --scenario tools/harness-scenarios/gts3/stargate-<name>.json --dmd-dir <frames> "
	"--output <external-run.json>. Each set's nvram-init run starts from an empty state directory (state-init-<set>) and "
	"loads factory settings; every other run of that set starts from a new state directory (states/<set>-<name>) holding "
	"only that run's NVRAM. Every scenario sets switch_converter gts3, so the harness checks PINMAME_HARDWARE_GEN_GTS3 "
	"before touching a switch."
)
FLIPPER_SYNTHETIC = {45, 46, 47, 48}
SERVICE_LIMITATION = "A pulsed address is ROM activity, not proof that a load is fitted."
SWITCH_LIMITATION = (
	"The Switch Edges Test keeps showing the last switch whose level changed, so a name shown while the host holds an "
	"address at 1 proves that the ROM scans that address under that name, not by itself which level is active."
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


def evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/gts3/stargate-{game}-service-tests.json"


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.casefold()).strip("-")


class Run:
	def __init__(self, runtime: Path, game: str, name: str, glyphs: dict[str, str]) -> None:
		self.game, self.name = game, name
		self.path = runtime / "runs" / f"{game}-{name}.json"
		self.data = json.loads(self.path.read_text(encoding="utf-8"))
		self.scenario_path = f"{SCENARIO_DIRECTORY}/stargate-{name}.json"
		scenario_bytes = (ROOT / self.scenario_path).read_bytes()
		if self.data.get("failure"):
			raise RuntimeError(f"{self.path.name}: the run failed: {self.data['failure']}")
		if self.data.get("library_sha256") != LIBRARY_SHA256:
			raise RuntimeError(f"{self.path.name}: not recorded on the pinned library")
		if self.data.get("game") != game:
			raise RuntimeError(f"{self.path.name}: recorded for {self.data.get('game')!r}")
		if self.data["scenario"]["sha256"] != hashlib.sha256(scenario_bytes).hexdigest():
			raise RuntimeError(f"{self.path.name}: the committed scenario changed since the run")
		if self.data.get("switch_converter") != "gts3":
			raise RuntimeError(f"{self.path.name}: not run with the gts3 switch converter")
		self.frames = runtime / "dmd" / f"{game}-{name}"
		self.text: dict[int, list[str]] = {}
		self.held_text: dict[int, list[str]] = {}
		for index, snapshot in enumerate(self.data["snapshots"]):
			displays = snapshot.get("displays") or []
			if len(displays) != 1:
				raise RuntimeError(f"{self.path.name}: snapshot {index} has {len(displays)} displays")
			frame = self.frames / Path(displays[0]["artifact"]).name
			if not frame.is_file():
				raise RuntimeError(f"{self.path.name}: retained frame missing: {frame}")
			lines = gts3_dmd_text.decode(frame.read_bytes(), glyphs)
			label = snapshot["label"]
			if label.endswith(" (held)"):
				self.held_text[index] = lines
			else:
				self.text[index] = lines
		# Snapshot 0 is the boot snapshot; step n's settle snapshot follows it, and a step with a
		# held snapshot adds one more just before. Pair them by label in order.
		self.step_text: dict[int, list[str]] = {}
		self.step_held_text: dict[int, list[str]] = {}
		snapshots = self.data["snapshots"]
		cursor = 1
		for step in self.data["steps"]:
			if cursor < len(snapshots) and snapshots[cursor]["label"] == f"{step['label']} (held)":
				self.step_held_text[step["step"]] = self.held_text[cursor]
				cursor += 1
			if cursor >= len(snapshots) or snapshots[cursor]["label"] != step["label"]:
				raise RuntimeError(f"{self.path.name}: no settle snapshot for step {step['step']} ({step['label']})")
			self.step_text[step["step"]] = self.text[cursor]
			cursor += 1

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


def solenoids_on(step: dict[str, Any]) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["solenoids"] if 1 in item["states"])


def blinking_lamps(step: dict[str, Any], minimum: int = 3) -> list[int]:
	return sorted(item["number"] for item in step["transitions"]["lamps"] if len(item["states"]) >= minimum)


def title(lines: list[str]) -> str:
	return " / ".join(lines[:2])


def lamp_matrix(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	for step in run.data["steps"]:
		if not step["label"].startswith("right flipper: lamp step") and step["label"] != "lamp 00 settle":
			continue
		found = gts3_dmd_text.labelled(run.step_text[step["step"]], "LAMP")
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no LAMP number")
		number, name = found
		blinking = blinking_lamps(step)
		if blinking != [number]:
			raise RuntimeError(f"{run.path.name}: LAMP:{number} blinked {blinking}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: LAMP:{number} named {names[number]!r} and {name!r}")
		names[number] = name
	expected = [column * 10 + row for column in range(12) for row in range(8)]
	if sorted(names) != expected:
		raise RuntimeError(f"{run.path.name}: the walk did not cover every lamp: {sorted(set(expected) - set(names))}")
	observation = {
		"diagnostic_checkpoints": [{"after_service_pulses": 4, "matched_text": "LAMP MATRIX TEST"}],
		"limitation": SERVICE_LIMITATION,
		"note": (
			"Self-test 3 stepped forward with the right flipper. In every step exactly one public lamp blinked (three or more "
			"state changes) and it was the displayed LAMP number, A0-B7 meaning 100-117. Address = name: "
			+ "; ".join(f"{number} = {names[number]}" for number in expected)
			+ "."
		),
	}
	return names, observation


def driver_test(run: Run, label: str, prefix: str, offset: int, channel: str, count: int) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	addresses: dict[int, int] = {}
	extras: dict[int, list[int]] = {}
	sequence: list[int] = []
	for step in run.data["steps"]:
		if not step["label"].startswith(f"start: fire {label}"):
			continue
		found = gts3_dmd_text.labelled(run.step_text[step["step"]], prefix)
		if found is None:
			raise RuntimeError(f"{run.path.name}: step {step['step']} shows no {prefix} number")
		number, name = found
		if channel == "solenoid":
			fired = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		else:
			fired = blinking_lamps(step, minimum=2)
		target = number + offset
		if target not in fired:
			raise RuntimeError(f"{run.path.name}: {prefix}:{number} fired {fired}, not {target}")
		if number in names and names[number] != name:
			raise RuntimeError(f"{run.path.name}: {prefix}:{number} named {names[number]!r} and {name!r}")
		names[number] = name
		addresses[number] = target
		others = [address for address in fired if address != target]
		if others:
			extras[number] = others
		sequence.append(target)
	if sorted(names) != list(range(count)):
		raise RuntimeError(f"{run.path.name}: the walk did not cover drivers 0-{count - 1}")
	note = (
		f"The right flipper steps the displayed {prefix} number and the credit button fires it; the {channel} that rose on each "
		f"press is the displayed number plus {offset}. {prefix.title()} = public {channel}: name: "
		+ "; ".join(f"{number} = {addresses[number]}: {names[number]}" for number in sorted(names))
		+ "."
	)
	if extras:
		note += " Also rising during the press: " + "; ".join(
			f"{prefix.title()} {number}: {', '.join(str(address) for address in others)}" for number, others in sorted(extras.items())
		) + "."
	observation: dict[str, Any] = {"limitation": SERVICE_LIMITATION, "note": note}
	if channel == "solenoid":
		observation["ordered_solenoid_on_sequence"] = sequence
		observation["solenoid_addresses_seen"] = sorted(set(sequence) | {address for others in extras.values() for address in others})
	return {number: names[number] for number in names}, observation


def switch_edges(run: Run) -> tuple[dict[int, str], dict[str, Any]]:
	names: dict[int, str] = {}
	silent: list[int] = []
	texts: dict[int, list[str]] = {}
	for step in run.data["steps"]:
		match = re.fullmatch(r"close switch (-?\d+)(?: through flipper button (141|143))?", step["label"])
		if not match:
			continue
		address = int(match.group(1))
		texts[address] = [line for line in run.step_held_text[step["step"]] if "?" not in line]
		found = gts3_dmd_text.labelled(run.step_held_text[step["step"]], "SWITCH")
		if found is None:
			silent.append(address)
			continue
		number, name = found
		if number != address:
			if address >= 0:
				raise RuntimeError(f"{run.path.name}: holding {address} showed SWITCH:{number}")
			silent.append(address)
			continue
		names[address] = name
	note = (
		"Self-test 6 with each address held at 1 alone for 400 ms (81 and 82 through the flipper buttons 143 and 141 that "
		"core_updateSw copies into them); the frame taken while held shows SWITCH:nn (A0-B7 meaning 100-117) and the ROM's "
		"name, and nn was the held address every time. Address = name: "
		+ "; ".join(f"{address} = {names[address]}" for address in sorted(names))
		+ "."
	)
	if silent:
		note += (
			" No SWITCH line of its own while held (the display kept the previous one or left the test): "
			+ ", ".join(f"{address} (\"{' / '.join(texts[address])}\")" for address in silent) + "."
		)
	return names, {"limitation": SWITCH_LIMITATION, "note": note, "switch_addresses_observed_while_held": sorted(names)}


def step_notes(run: Run) -> list[str]:
	notes = []
	for step in run.data["steps"]:
		on = [address for address in solenoids_on(step) if address not in FLIPPER_SYNTHETIC]
		synthetic = [address for address in solenoids_on(step) if address in FLIPPER_SYNTHETIC]
		text = " / ".join(line for line in run.step_text[step["step"]] if "?" not in line)
		part = f"{step['step']} {step['label']}: solenoids rising {on or 'none'}"
		if synthetic:
			part += f", synthetic flipper outputs {synthetic}"
		if text:
			part += f"; display \"{text}\""
		notes.append(part)
	return notes


def scripted(run: Run, summary: str) -> dict[str, Any]:
	seen = sorted({address for step in run.data["steps"] for address in solenoids_on(step)})
	return {"limitation": STATIC_LIMITATION, "note": summary + " Steps: " + "; ".join(step_notes(run)) + ".", "solenoid_addresses_seen": seen}


def front_door(run: Run) -> dict[str, Any]:
	counts = []
	for step in run.data["steps"]:
		lines = run.step_held_text.get(step["step"]) or run.step_text[step["step"]]
		counts.append(f"{step['label']}: \"{' / '.join(lines)}\"")
	return {"limitation": STATIC_LIMITATION, "note": "Self-test 9; display after each step (while held where taken): " + "; ".join(counts) + "."}


def build(root: Path) -> dict[str, dict[str, Any]]:
	runtime = root / RUNTIME_RELATIVE
	glyphs = gts3_dmd_text.load_glyphs()
	manifest_sha = manifests.check_manifest(runtime, MANIFEST_GAME)
	if manifest_sha != sha256(runtime / "manifest.json"):
		raise RuntimeError("the retained manifest digest does not match manifest.json")
	bundles: dict[str, dict[str, Any]] = {}
	reference: dict[str, dict[int, str]] = {}
	for game in SETS:
		names = PRIMARY_RUNS if game == PRIMARY else SERVICE_RUNS
		runs = {name: Run(runtime, game, name, glyphs) for name in names}
		init_nv = runtime / f"state-init-{game}" / "nvram" / f"{game}.nv"
		init_note = f"Fresh state directory holding only nvram/{game}.nv (SHA-256 {sha256(init_nv)}) from this set's nvram-init run."
		raw = [runs["nvram-init"].raw_record("Empty state directory state-init-" + game + "; this run loads factory settings and its NVRAM is the only state any later run of the set inherits.")]
		raw += [runs[name].raw_record(init_note) for name in names[1:]]
		observations: dict[str, Any] = {}
		init_texts = [" / ".join(line for line in run_text if "?" not in line) for run_text in runs["nvram-init"].step_text.values()]
		init_texts = [text for text in init_texts if text]
		observations["nvram-init"] = {
			"limitation": STATIC_LIMITATION,
			"note": (
				f"The power-up frame (pixel SHA-256 {runs['nvram-init'].data['snapshots'][0]['displays'][0]['pixel_sha256']}) "
				f"reads {BOOT_SCREENS[game]}, in a font the glyph table does not cover. Displays after each step: "
				+ "; ".join(f"\"{text}\"" for text in init_texts) + "."
			),
		}
		lamp_names, observations["lamp-matrix"] = lamp_matrix(runs["lamp-matrix"])
		sol_names, observations["solenoids"] = driver_test(runs["solenoids"], "solenoid", "SOLENOID", 1, "solenoid", 32)
		aux_names, observations["aux-drivers"] = driver_test(runs["aux-drivers"], "aux driver", "DRIVER", 120, "lamp", 8)
		switch_names, observations["switch-edges"] = switch_edges(runs["switch-edges"])
		tables = {"lamps": lamp_names, "solenoids": sol_names, "aux": aux_names, "switches": switch_names}
		if game == PRIMARY:
			reference = tables
			observations["front-door"] = front_door(runs["front-door"])
			observations["tournament-door"] = scripted(runs["tournament-door"], "Attract mode, coin door and tournament switches.")
			observations["gameplay"] = scripted(runs["gameplay"], "One game started with two coins on chute 1.")
			observations["mechanism-sensors"] = scripted(runs["mechanism-sensors"], "Attract mode with each mechanism sensor held at 1, then released.")
		else:
			differences = []
			for key, table in tables.items():
				for number in sorted(set(table) | set(reference[key])):
					if table.get(number) != reference[key].get(number):
						differences.append(f"{key} {number}: {table.get(number)!r} here, {reference[key].get(number)!r} on {PRIMARY}")
			observations["comparison"] = {
				"note": (
					f"Every lamp, solenoid, aux driver and switch name this set's tests display is identical to {PRIMARY}'s at the same address."
					if not differences else
					f"Names that differ from {PRIMARY}'s: " + "; ".join(differences) + "."
				),
			}
		named = {}
		for number, name in sorted(lamp_names.items()):
			named[f"lamp-{number:03d}-{slug(name) or 'unnamed'}"] = number
		for number, name in sorted(sol_names.items()):
			named[f"solenoid-{number:02d}-{slug(name)}"] = number + 1
		for number, name in sorted(aux_names.items()):
			named[f"aux-{number}-{slug(name)}"] = 120 + number
		bundles[game] = {
			"format": "pinmame-machine-evidence",
			"version": 1,
			"extractor": {"id": "stargate-harness-runs", "version": 1},
			"source": {
				"kind": "runtime_scenario",
				"repository": "https://github.com/vpinball/pinmame",
				"revision": REVISION,
				"path": SOURCE_PATH,
				"sha256": manifest_sha,
				"license": "NOASSERTION",
				"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes, NVRAM and DMD frames remain external.",
				"quality": "observed",
				"manifest_algorithm": MANIFEST_ALGORITHM,
			},
			"driver_ids": [game],
			"machine_ids": [MACHINE_ID],
			"switches": [],
			"outputs": [],
			"states": [],
			"mechanisms": [],
			"recreation_notes": [],
			"runtime": {
				"game": game,
				"rom_archive_sha256": ROM_ARCHIVE_SHA256[game],
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
	return bundles


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--check", action="store_true", help="re-derive the bundles and refuse drift, writing nothing")
	args = parser.parse_args()
	bundles = build(working_root())
	failures = []
	for game, bundle in bundles.items():
		path = evidence_path(game)
		expected = canonical_bytes(bundle)
		if args.check:
			if not path.is_file() or path.read_bytes() != expected:
				failures.append(path.relative_to(ROOT).as_posix())
		else:
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_bytes(expected)
			print(f"wrote {path.relative_to(ROOT).as_posix()}")
	if failures:
		print("drift: " + ", ".join(failures))
		return 1
	if args.check:
		print("Stargate runtime evidence matches the retained runs.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
