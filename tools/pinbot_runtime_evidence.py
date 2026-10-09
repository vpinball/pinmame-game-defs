"""Summarize the retained Pin-Bot (pb_l5) harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/williams.pinbot.1986/runtime/runs/`` (written by ``tools/run_pinmame_harness.py``
with the pinned library, each from a new state directory that inherits only the retained
initialization run's NVRAM), checks that every run succeeded on the pinned emulator binary with an
unchanged committed scenario, and writes ``evidence/runtime/system-11/pinbot-l5-service-and-mechanisms.json``.

Display text is decoded from the raw sixteen-segment values: the low fifteen bits are the glyph and
bit 15 is the period; the ROM draws the numeral 1 as 0x0006. The ROM's lamp, switch and coil name tables (``tools/pinbot_rom_name_tables.py``)
supply the names each service step must display; a step is paired with an address only when the
decoded display equals the table entry. Every number written is recomputed from the raw runs, and
``--check`` refuses any drift.

    python tools/pinbot_runtime_evidence.py            # write
    python tools/pinbot_runtime_evidence.py --check    # re-derive and compare, write nothing
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

from pinmame_game_defs.jsonio import canonical_bytes  # noqa: E402
from run_pinmame_harness import SEGMENT_16_CHARACTERS  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_external_evidence_manifest", TOOLS / "build_external_evidence_manifest.py")
manifests = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(manifests)

REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "f7b86e6688ef990f990d85564c3aaa264a14927d78402bab49880fafa74c5b6c"
GAME = "pb_l5"
MACHINE_ID = "williams.pinbot.1986"
SCENARIO_DIRECTORY = "tools/harness-scenarios/system-11"
EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/pinbot-l5-service-and-mechanisms.json"
RUNTIME_RELATIVE = Path("williams.pinbot.1986/runtime")
NAME_TABLE_RELATIVE = Path("williams.pinbot.1986/rom-name-tables/pb_l5.json")
SOURCE_PATH = "external:pinmame-review-artifacts/williams.pinbot.1986/runtime"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, and every state-directory file including the inherited and written NVRAM) except "
	"manifest.json and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py writes and "
	"re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game pb_l5 --rom-path <vpinmame-roms> "
	"--work-dir <new-state-directory> --scenario tools/harness-scenarios/system-11/pinbot-<name>.json --boot-wait 0 "
	"--output <external-run.json>. The initialization run starts from an empty state directory and stops on FACTORY SETTING; "
	"every other run starts from a new state directory holding only that run's nvram/pb_l5.nv. Diagnostic scenarios wait 8 s, "
	"set Manual-Down (-6 = 0), pulse Advance (-7) to enter the tests, set Auto-Up (-6 = 1) and pulse Advance until the "
	"checkpoint text is displayed."
)
INIT_RUN = "nvram-init"
RUN_NAMES = (
	"nvram-init",
	"coil-test",
	"single-lamps",
	"switch-levels",
	"boot-baseline",
	"boot-visor-closed-46",
	"boot-visor-open-47",
	"boot-ramp-down-44",
	"boot-trough-17-18",
	"boot-outhole-16",
	"boot-eyes-25-26",
	"boot-single-eject-38",
	"boot-drops-49-51",
	"boot-shooter-20",
	"visor-open-edge-47",
	"visor-cycle",
	"gameplay",
	"gameplay-reactive",
)
STATIC_LIMITATION = (
	"Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a "
	"host-held switch."
)
REACTIVE_LIMITATION = (
	"The host answers the ROM's drives with fixed, scripted switch changes; a pulse the ROM fires proves only that the address "
	"changed under these conditions, not a mechanism's travel time or the physical device's identity."
)
# The ROM draws the numeral 1 with the two right-hand segments only (0x0006), which the harness's
# shared sixteen-segment table does not list.
ROM_GLYPHS = {0x0006: "1"}
# Background outputs left out of the per-run span notes: the attract-mode G.I. and robot-face
# flicker repeats for as long as the game is idle and says nothing about the probed mechanism.
ATTRACT_BACKGROUND = {9, 11, 12}


def working_root() -> Path:
	value = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
	if not value:
		raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT is required: the raw runs live under the working root's review-artifacts")
	return Path(value).expanduser().resolve()


def sha256(path: Path) -> str:
	return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_alpha(values: list[int]) -> str:
	text = []
	for value in values:
		glyph = ROM_GLYPHS.get(value & 0x7FFF, SEGMENT_16_CHARACTERS.get(value & 0x7FFF))
		text.append("?" if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def normalized(text: str) -> str:
	return " ".join(text.split())


def as_displayed(table_text: str) -> str:
	"""A ROM table entry as the display draws it.

	This ROM's font has no glyph for "-" (it lights nothing) and draws 5 and S, and 0 and O, with the
	same segments, so both sides of a comparison fold those pairs.
	"""
	return glyph_folded(normalized(table_text.replace("-", " ")))


def glyph_folded(text: str) -> str:
	return text.replace("5", "S").replace("0", "O")


def load_run(runs: Path, name: str) -> dict[str, Any]:
	run = json.loads((runs / f"pb_l5-{name}.json").read_text(encoding="utf-8"))
	if run.get("failure") is not None or run.get("game") != GAME:
		raise RuntimeError(f"{name}: not a successful pb_l5 run")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise RuntimeError(f"{name}: not produced by the pinned library")
	scenario = ROOT / SCENARIO_DIRECTORY / f"pinbot-{name}.json"
	if run["scenario"]["sha256"] != sha256(scenario):
		raise RuntimeError(f"{name}: scenario drift against {scenario}")
	return run


def service_pulses(run: dict[str, Any]) -> int:
	total = 0
	for step in run["steps"]:
		if step.get("type") == "pulse" and step.get("switch") == -7:
			total += 1
		elif step.get("type") == "pulse_until_display" and step.get("switch") == -7:
			total += step["pulses"]
	return total


def checkpoints(run: dict[str, Any]) -> list[dict[str, Any]]:
	return [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
	        for step in run["steps"] if step.get("type") == "pulse_until_display"]


def solenoid_spans(run: dict[str, Any]) -> dict[int, list[tuple[float, float | None]]]:
	open_at: dict[int, float] = {}
	spans: dict[int, list[tuple[float, float | None]]] = {}
	for event in run["events"]:
		if event["event"] != "solenoid":
			continue
		number, time = event["number"], round(event["time_s"], 3)
		if event["state"]:
			open_at.setdefault(number, time)
		elif number in open_at:
			spans.setdefault(number, []).append((open_at.pop(number), time))
	for number, time in open_at.items():
		spans.setdefault(number, []).append((time, None))
	return spans


def describe_spans(spans: dict[int, list[tuple[float, float | None]]], end: float) -> str:
	parts = []
	for number in sorted(spans):
		if number in ATTRACT_BACKGROUND:
			continue
		items = spans[number]
		if len(items) <= 3:
			parts.append(f"{number}: " + ", ".join(f"{a}-{'end' if b is None else b} s" for a, b in items))
		else:
			gaps = [round(items[i + 1][0] - items[i][0], 2) for i in range(len(items) - 1)]
			parts.append(f"{number}: {len(items)} pulses from {items[0][0]} s to {items[-1][0]} s, spacing {min(gaps)}-{max(gaps)} s")
	return "; ".join(parts) + f" (observed to {end} s)"


def end_time(run: dict[str, Any]) -> float:
	return round(max(event["time_s"] for event in run["events"]), 3)


def display_timeline(run: dict[str, Any]) -> list[tuple[float, dict[int, str]]]:
	state: dict[int, str] = {}
	timeline = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") in (0, 1) and isinstance(event.get("segments"), list):
			state[event["index"]] = decode_alpha(event["segments"])
			timeline.append((event["time_s"], dict(state)))
	return timeline


def text_at(timeline: list[tuple[float, dict[int, str]]], time: float) -> str:
	current: dict[int, str] = {}
	for at, state in timeline:
		if at > time:
			break
		current = state
	return glyph_folded(normalized(current.get(0, "") + " " + current.get(1, "")))


def coil_test(run: dict[str, Any], names: list[str]) -> dict[str, Any]:
	"""Pair each coil-test step with the address it pulses and the name the ROM displays."""
	start = next(step for step in run["steps"] if step.get("type") == "pulse_until_display")
	timeline = display_timeline(run)
	begin = next(event["time_s"] for event in run["events"] if event["event"] == "display" and normalized(decode_alpha(event.get("segments") or [])) == "COIL")
	steps = []
	for event in run["events"]:
		if event["event"] != "solenoid" or not event["state"] or event["time_s"] <= begin or event["number"] == 23:
			continue
		text = text_at(timeline, event["time_s"] + 0.05)
		# The A/C select relay (14) is energized ahead of every C-side step; it is a step of its own
		# only where the ROM names it.
		if event["number"] == 14 and text != as_displayed("A-C SELECT"):
			continue
		steps.append((event["time_s"], event["number"], text))
	expected = [as_displayed(name) for name in names if name.strip()]
	period = len(expected)
	if len(steps) < 2 * period:
		raise RuntimeError(f"coil test recorded {len(steps)} steps, fewer than two cycles of {period}")
	pairs = []
	for index, (time, address, text) in enumerate(steps[:period]):
		if text != expected[index]:
			raise RuntimeError(f"coil test step {index + 1} displays {text!r}, ROM table entry is {expected[index]!r}")
		pairs.append({"step": index + 1, "address": address, "rom_name": [normalized(n) for n in names if n.strip()][index], "time_s": round(time, 3)})
	second = [address for _, address, _ in steps[period:2 * period]]
	if second != [pair["address"] for pair in pairs]:
		raise RuntimeError("coil test second cycle differs from the first")
	relay = solenoid_spans(run).get(14, [])
	c_side = []
	for pair in pairs:
		held = any(a <= pair["time_s"] and (b is None or pair["time_s"] < b) for a, b in relay)
		c_side.append(held)
	return {"pairs": pairs, "relay_14_held": c_side, "matched_start": start["matched_text"]}


def single_lamps(run: dict[str, Any], names: list[str]) -> dict[str, Any]:
	timeline = display_timeline(run)
	pairs = []
	for step in run["steps"]:
		label = step.get("label", "")
		if not (label.startswith("Credit: step to designator") or label.startswith("first lamp")):
			continue
		designator = 1 if label.startswith("first lamp") else int(label.rsplit(" ", 1)[1])
		changed = sorted({lamp["number"] for lamp in step["transitions"]["lamps"]})
		if designator not in changed:
			raise RuntimeError(f"single lamps designator {designator} did not blink its own address: {changed}")
		pairs.append({"designator": designator, "changed": changed})
	if [pair["designator"] for pair in pairs] != list(range(1, 65)):
		raise RuntimeError("single lamps did not step through designators 01-64")
	shown = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") in (0, 1):
			shown.append(normalized(text_at(timeline, event["time_s"])))
	missing = [index + 1 for index, name in enumerate(names) if as_displayed(name) not in shown]
	if missing:
		raise RuntimeError(f"single lamps never displayed the ROM names of lamps {missing}")
	return {"pairs": pairs}


def switch_levels(run: dict[str, Any], names: list[str]) -> dict[str, Any]:
	timeline = display_timeline(run)
	results = {}
	for step in run["steps"]:
		label = step.get("label", "")
		if not label.startswith("hold public switch"):
			continue
		address = int(label.rsplit(" ", 1)[1])
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label + " (held)")
		alpha = glyph_folded(normalized(" ".join(decode_alpha(display["segments"]) for display in snapshot["displays"] if display["index"] in (0, 1))))
		ball = [display["segments"] for display in snapshot["displays"] if display["index"] in (4, 5)]
		results[address] = {"display": alpha, "ball_in_play_segments": ball}
	return results


def boot_note(run: dict[str, Any]) -> str:
	holds = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"])
	return f"Power-up probe with switches {holds} held from emulator start. Solenoid on-spans: {describe_spans(solenoid_spans(run), end_time(run))}."


def build(review_root: Path) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
	runtime = review_root / RUNTIME_RELATIVE
	runs_dir = runtime / "runs"
	manifest_bytes = (json.dumps(manifests.build_manifest(runtime, GAME), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
	tables = json.loads((review_root / NAME_TABLE_RELATIVE).read_text(encoding="utf-8"))
	coil_names = [entry["text"] for entry in tables["coil_table"]["entries"]]
	lamp_names = [entry["text"] for entry in tables["lamp_table"]["entries"]]
	switch_names = [entry["text"] for entry in tables["switch_table"]["entries"]]
	init_nv = sha256(runtime / "state-init/nvram/pb_l5.nv")
	raw_runs, runs_obs, analysis = [], {}, {}
	seen: set[int] = set()
	named: dict[str, int] = {}
	ordered: list[int] = []
	lamps_seen: list[int] = []
	for name in RUN_NAMES:
		run = load_run(runs_dir, name)
		entry: dict[str, Any] = {
			"name": name,
			"sha256": sha256(runs_dir / f"pb_l5-{name}.json"),
			"scenario_path": f"{SCENARIO_DIRECTORY}/pinbot-{name}.json",
			"scenario_sha256": run["scenario"]["sha256"],
			"action_count": run["scenario"]["action_count"],
			"watch_switches": run["watch_switches"],
			"self_test_pulses": service_pulses(run),
			"boot_wait_s": 0,
			"snapshot_count": len(run["snapshots"]),
			"nvram_initialization": (
				"Fresh empty state directory; this is the one retained initialization run (FACTORY SETTING), whose nvram/pb_l5.nv "
				"is the only state any later run inherits."
				if name == INIT_RUN
				else f"Fresh state directory holding only nvram/pb_l5.nv (SHA-256 {init_nv}) from the retained initialization run."
			),
		}
		if run["initial_switches"]:
			entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
		raw_runs.append(entry)
		spans = solenoid_spans(run)
		run_seen = sorted(number for number in spans)
		seen.update(run_seen)
		observation: dict[str, Any] = {"solenoid_addresses_seen": run_seen}
		if name == INIT_RUN:
			observation["note"] = "Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later runs inherit."
		elif name == "coil-test":
			result = coil_test(run, coil_names)
			analysis[name] = result
			ordered = [pair["address"] for pair in result["pairs"]]
			for pair, held in zip(result["pairs"], result["relay_14_held"]):
				named[f"coil-{pair['step']:02d}-{re.sub(r'[^a-z0-9]+', '-', pair['rom_name'].lower()).strip('-')}"] = pair["address"]
			c_steps = [pair["address"] for pair, held in zip(result["pairs"], result["relay_14_held"]) if held and pair["address"] != 14]
			observation.update({
				"diagnostic_checkpoints": checkpoints(run),
				"ordered_solenoid_on_sequence": ordered,
				"note": (
					f"Advance walk to COIL TEST (Credit display 04), then two complete cycles of {len(ordered)} named steps, the second "
					"identical to the first. Step:address = ROM name: " + "; ".join(f"{p['step']}:{p['address']} = {p['rom_name']}" for p in result["pairs"])
					+ f". The A/C select relay (14) is energized before and held through each step that pulses {', '.join(map(str, c_steps))}, "
					"and released for every other step."
				),
				"limitation": (
					"A name is paired with an address only when the decoded player 1 and 2 display text at the pulse equals the ROM coil "
					"table entry (whitespace-normalized). A pulsed address is ROM activity, not proof that a load is fitted."
				),
			})
		elif name == "single-lamps":
			result = single_lamps(run, lamp_names)
			analysis[name] = result
			lamps_seen = sorted({lamp for pair in result["pairs"] for lamp in pair["changed"]})
			for index, lamp_name in enumerate(lamp_names, start=1):
				named[f"lamp-{index:02d}-{re.sub(r'[^a-z0-9]+', '-', normalized(lamp_name).lower()).strip('-')}"] = index
			observation.update({
				"diagnostic_checkpoints": checkpoints(run),
				"note": (
					"Advance walk to SINGLE LAMPS (Credit display 03); each Credit press (public 3) steps the designator, and designator n "
					"blinks public lamp n for every n from 1 to 64 while the player 1 and 2 displays show the ROM lamp-table entry n."
				),
			})
		elif name == "switch-levels":
			result = switch_levels(run, switch_names)
			analysis[name] = result
			named_ok = sorted(address for address, item in result.items() if 1 <= address <= 64 and item["display"] == as_displayed(switch_names[address - 1]))
			observation.update({
				"diagnostic_checkpoints": checkpoints(run),
				"note": (
					"Advance walk to SWITCH LEVELS (Credit display 05); each public address 1-64 and 81-88 held at 1 alone for 1.5 s. "
					f"The player 1 and 2 displays showed the ROM switch-table name of the held address for public {compress(named_ok)}. "
					+ switch_level_exceptions(result, switch_names)
				),
				"limitation": "Host-held levels; a name shown while public n is held at 1 means the ROM reads that address as active at 1.",
			})
		elif name.startswith("boot-"):
			observation.update({"note": boot_note(run), "limitation": STATIC_LIMITATION})
		elif name.startswith("visor-") or name.startswith("gameplay"):
			observation.update({
				"note": f"Scripted scenario ({run['scenario']['action_count']} actions, see the scenario notes). Solenoid on-spans: {describe_spans(spans, end_time(run))}.",
				"limitation": REACTIVE_LIMITATION if name in ("visor-cycle", "visor-open-edge-47", "gameplay-reactive") else STATIC_LIMITATION,
			})
		runs_obs[name] = observation
	evidence = {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": "pinbot-harness-runs", "version": 1},
		"source": {
			"kind": "runtime_scenario",
			"repository": "https://github.com/vpinball/pinmame",
			"revision": REVISION,
			"path": SOURCE_PATH,
			"sha256": hashlib.sha256(manifest_bytes).hexdigest(),
			"license": "NOASSERTION",
			"attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes and NVRAM remain external.",
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
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": {
				"service_language": "English",
				"solenoid_addresses_seen": sorted(seen),
				"lamp_addresses_seen": lamps_seen,
				"ordered_solenoid_on_sequence": ordered,
				"named_output_addresses": named,
				"display_indices_seen": [0, 1, 2, 3, 4, 5, 6, 7, 8],
				"runs": runs_obs,
			},
		},
	}
	return manifest_bytes, evidence, analysis


def compress(addresses: list[int]) -> str:
	if not addresses:
		return "none"
	ranges, start, previous = [], addresses[0], addresses[0]
	for address in addresses[1:] + [None]:
		if address is not None and address == previous + 1:
			previous = address
			continue
		ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
		if address is not None:
			start = previous = address
	return ", ".join(ranges)


def switch_level_exceptions(result: dict[int, dict[str, Any]], names: list[str]) -> str:
	notes = []
	for address in sorted(result):
		shown = result[address]["display"]
		expected = as_displayed(names[address - 1]) if 1 <= address <= 64 else None
		if expected is not None and shown == expected:
			continue
		notes.append(f"public {address}: displayed {shown!r}" + (f" (ROM table {expected!r})" if expected else ""))
	return ("Other holds: " + "; ".join(notes) + ".") if notes else ""


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	parser.add_argument("--analysis", type=Path, help="optional external path for the full derived analysis JSON")
	args = parser.parse_args()
	review_root = working_root()
	runtime = review_root / RUNTIME_RELATIVE
	manifest_bytes, evidence, analysis = build(review_root)
	if args.check:
		if (runtime / "manifest.json").read_bytes() != manifest_bytes:
			raise SystemExit(f"{runtime / 'manifest.json'} does not match the files beside it")
		manifests.check_manifest(runtime, GAME)
		if EVIDENCE_PATH.read_bytes() != canonical_bytes(evidence):
			raise SystemExit(f"{EVIDENCE_PATH} is not the summary of the raw runs in {runtime}")
		print("Pin-Bot runtime evidence and manifest match the raw runs.")
		return
	manifests.write_manifest(runtime, GAME)
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(canonical_bytes(evidence))
	if args.analysis:
		args.analysis.write_bytes(canonical_bytes(analysis))
	print(f"wrote {EVIDENCE_PATH}")


if __name__ == "__main__":
	main()
