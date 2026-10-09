"""Summarize the retained Diner harness runs into compact runtime evidence.

Reads the raw ``pinmame-harness-run`` records under the working root's
``review-artifacts/williams.diner.1990/runtime/runs/`` (written by ``tools/run_pinmame_harness.py``
with the pinned library, each from a new state directory that inherits only its set's retained
initialization run's NVRAM), checks that every run succeeded on the pinned emulator binary with an
unchanged committed scenario, and writes two files:

* ``evidence/runtime/system-11/diner-l4-service-and-mechanisms.json``: the diner_l4 service tests,
  power-up probes and gameplay run;
* ``evidence/runtime/system-11/diner-<set>-service-tests.json`` for each other local diner_* set: its
  Coil, Single Lamps and Switch Levels names, compared with diner_l4's.

Display text is decoded from the raw sixteen-segment values of the two alphanumeric rows: the low
fifteen bits are the glyph and bit 15 is the period; the ROM draws the numeral 1 as 0x0006 and uses
one glyph for 0 and O and one for 5 and S, which the decoder writes as O and S. A Coil Test step is
the text on the upper row when the step's output rises; a Single Lamps step is the upper-row text shown
longest between two Start presses; a Switch Levels step is the snapshot taken while the address is held.
Every number written is recomputed from the raw runs, and ``--check`` refuses any drift.

    python tools/diner_runtime_evidence.py            # write
    python tools/diner_runtime_evidence.py --check    # re-derive and compare, write nothing
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
MACHINE_ID = "williams.diner.1990"
GAME = "diner_l4"
VARIANT_GAMES = ("diner_l3", "diner_l2", "diner_l1", "diner_l4fr")
ROM_ARCHIVE_SHA256 = {
	"diner_l4": "dfbd37bb3e8b847d8f3fbf11e6091a41a9d52c88b2f55443caa110b4453511c0",
	"diner_l3": "602e6763ca6b80486c6072c6440228d3b6561faff89ef9ce93c5273639d6309e",
	"diner_l2": "4ef205b6e9aed3ef758002c81976ef2bde553517a7e7e83f89d357425196e9d3",
	"diner_l1": "11ecab1484e3c1be90aad07eeb63b67e70544729cbc719f26e35622ce1abfd6a",
	"diner_l4fr": "3ad6d2318b2688e00493fc6ec7824cb4a33e46227693ee51f60748c57e38fea6",
}
SCENARIO_DIRECTORY = "tools/harness-scenarios/system-11"
EVIDENCE_PATH = ROOT / "evidence/runtime/system-11/diner-l4-service-and-mechanisms.json"


def variant_evidence_path(game: str) -> Path:
	return ROOT / f"evidence/runtime/system-11/diner-{game.split('_', 1)[1]}-service-tests.json"

RUNTIME_RELATIVE = Path("williams.diner.1990/runtime")
SOURCE_PATH = "external:pinmame-review-artifacts/williams.diner.1990/runtime"
MANIFEST_ALGORITHM = (
	"source.sha256 is SHA-256 of manifest.json's exact bytes. manifest.json is compact canonical JSON with sorted keys, "
	"separators=(',', ':'), ensure_ascii=False, plus one LF, of {files: [{path, sha256, size}], format: "
	"'pinmame-external-evidence-manifest', game, version: 1}; files lists every file under source.path recursively (the raw "
	"run JSON and log of every run, and every state-directory file including the inherited and written NVRAM) except "
	"manifest.json and manifest.sha256, sorted by POSIX relative path. tools/build_external_evidence_manifest.py writes and "
	"re-checks it."
)
COMMAND_TEMPLATE = (
	"python -B tools/run_pinmame_harness.py --library <pinned-pinmame64.dll> --game <set> --rom-path <vpinmame-roms> "
	"--work-dir <new-state-directory> --scenario tools/harness-scenarios/system-11/diner-<name>.json --boot-wait 0 "
	"--output <external-run.json>. Each set's initialization run (diner-nvram-init.json) starts from an empty state "
	"directory and stops on FACTORY SETTING; every other run of that set starts from a new state directory holding only "
	"that run's NVRAM. Diagnostic scenarios wait 8 s, set Manual-Down (-6 = 0), pulse Advance (-7) to enter the tests, set "
	"Auto-Up (-6 = 1) and pulse Advance until the checkpoint text is displayed."
)
INIT_RUN = "nvram-init"
RUN_NAMES = (
	"nvram-init", "coil-test", "single-lamps", "switch-levels", "c-side-test", "wheel-test-59-0", "wheel-test-59-edge",
	"boot-baseline", "boot-outhole-9", "boot-trough-11-13", "boot-shooter-14", "boot-subway-15-16", "boot-subway-15",
	"boot-ejects-49-50", "boot-ramp-up-down-10", "boot-drops-center-22-24", "boot-drops-left-30-32", "boot-clock-59",
	"boot-cup-17", "gameplay",
)
VARIANT_RUN_NAMES = ("nvram-init", "coil-test", "single-lamps", "switch-levels")
STATIC_LIMITATION = (
	"Static host switches only; the harness never moves a ball or a mechanism, so repeated pulses are ROM retries against a "
	"host-held switch."
)
SCRIPTED_LIMITATION = (
	"The host answers the ROM's drives with fixed, scripted switch changes; a pulse the ROM fires proves only that the address "
	"changed under these conditions, not a mechanism's travel time or the physical device's identity."
)
ROM_GLYPHS = {0x0006: "1"}
# Background outputs left out of the per-run span notes: the attract-mode lamp-show flashers and relays repeat for as
# long as the game is idle and say nothing about the probed device.
ATTRACT_BACKGROUND = {9, 10, 11, 12, 13}


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
		text.append(("?" if value & 0x7FFF else " ") if glyph is None else glyph)
		if value & 0x8000:
			text.append(".")
	return "".join(text)


def normalized(text: str) -> str:
	return " ".join(text.split())


def glyph_folded(text: str) -> str:
	"""A name as this ROM's font draws it: 0 and O, and 5 and S, share a glyph."""
	return text.replace("0", "O").replace("5", "S")


def run_file(runs: Path, game: str, name: str) -> Path:
	return runs / f"{game}-{name}.json"


def load_run(runs: Path, game: str, name: str) -> dict[str, Any]:
	run = json.loads(run_file(runs, game, name).read_text(encoding="utf-8"))
	if run.get("failure") is not None or run.get("game") != game:
		raise RuntimeError(f"{game} {name}: not a successful run")
	if run.get("library_sha256") != LIBRARY_SHA256:
		raise RuntimeError(f"{game} {name}: not produced by the pinned library")
	scenario = ROOT / SCENARIO_DIRECTORY / f"diner-{name}.json"
	if run["scenario"]["sha256"] != sha256(scenario):
		raise RuntimeError(f"{game} {name}: scenario drift against {scenario}")
	return run


def upper_timeline(run: dict[str, Any]) -> list[tuple[float, str]]:
	timeline = []
	for event in run["events"]:
		if event["event"] == "display" and event.get("index") == 0 and isinstance(event.get("segments"), list):
			timeline.append((event["time_s"], normalized(decode_alpha(event["segments"]))))
	return timeline


def text_at(timeline: list[tuple[float, str]], time: float) -> str:
	current = ""
	for at, text in timeline:
		if at > time:
			break
		current = text
	return current


def longest_text(timeline: list[tuple[float, str]], start: float, end: float) -> str:
	durations: dict[str, float] = {}
	current = text_at(timeline, start)
	at = start
	for when, text in timeline:
		if when <= start:
			continue
		if when >= end:
			break
		durations[current] = durations.get(current, 0.0) + (when - at)
		current, at = text, when
	durations[current] = durations.get(current, 0.0) + (end - at)
	return max(sorted(durations), key=lambda text: durations[text])


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


def coil_test(run: dict[str, Any]) -> list[dict[str, Any]]:
	"""Each coil-test step: the address that rises and the upper-row text then, for two complete cycles."""
	timeline = upper_timeline(run)
	begin = next(at for at, text in timeline if text == "COIL TEST")
	steps = []
	for event in run["events"]:
		if event["event"] != "solenoid" or not event["state"] or event["time_s"] <= begin or event["number"] == 23:
			continue
		text = text_at(timeline, event["time_s"])
		# The A/C select relay (12) is energized ahead of every C-side step; it is a step of its own only where the ROM names it.
		if event["number"] == 12 and text != "A/C SELECT":
			continue
		steps.append({"address": event["number"], "display": text, "time_s": round(event["time_s"], 3)})
	period = next(index for index in range(1, len(steps)) if steps[index]["address"] == steps[0]["address"] and index > 2)
	first, second = steps[:period], steps[period:2 * period]
	if [step["address"] for step in first] != [step["address"] for step in second]:
		raise RuntimeError("coil test second cycle differs from the first")
	if [step["display"] for step in first] != [step["display"] for step in second]:
		raise RuntimeError("coil test second cycle names differ from the first")
	return [{"step": index, "address": step["address"], "display": step["display"]} for index, step in enumerate(first, start=1)]


def relay_held(run: dict[str, Any], steps: list[dict[str, Any]]) -> list[int]:
	"""Addresses whose coil-test pulse falls inside an energized span of the A/C relay (12)."""
	timeline = upper_timeline(run)
	begin = next(at for at, text in timeline if text == "COIL TEST")
	relay = solenoid_spans(run).get(12, [])
	held = []
	rises = [(event["time_s"], event["number"]) for event in run["events"] if event["event"] == "solenoid" and event["state"] and event["time_s"] > begin]
	for step in steps:
		time = next(t for t, n in rises if n == step["address"])
		if step["address"] != 12 and any(a <= time and (b is None or time < b) for a, b in relay):
			held.append(step["address"])
	if held != list(range(25, 33)):
		raise RuntimeError(f"the A/C relay was held for {held}, not exactly the C-side bank 25-32")
	if not any(step["address"] == 12 and step["display"] == "A/C SELECT" for step in steps):
		raise RuntimeError("the coil test has no A/C SELECT step of its own")
	return held


def single_lamps(run: dict[str, Any]) -> list[dict[str, Any]]:
	timeline = upper_timeline(run)
	presses = [event["time_s"] for event in run["events"] if event["event"] == "switch" and event.get("number") == 3 and event.get("state") == 1]
	steps = [step for step in run["steps"] if step.get("label", "").startswith(("Start: step to designator", "first lamp"))]
	title = next(at for at, text in timeline if text == "SINGLE LAMPS")
	# The first lamp's window starts when the test title gives way to the first lamp name.
	begin = next(at for at, text in timeline if at > title and text != "SINGLE LAMPS")
	bounds = [begin] + presses
	pairs = []
	for index, step in enumerate(steps):
		designator = 1 if step["label"].startswith("first lamp") else int(step["label"].rsplit(" ", 1)[1])
		changed = sorted({lamp["number"] for lamp in step["transitions"]["lamps"]})
		start, end = bounds[index] + 0.3, bounds[index + 1]
		blinked = sorted({event["number"] for event in run["events"] if event["event"] == "lamp" and start <= event["time_s"] < end})
		if blinked != [designator]:
			raise RuntimeError(f"single lamps designator {designator} blinked {blinked}")
		pairs.append({"designator": designator, "address": designator, "display": longest_text(timeline, start, end), "step_changed": changed})
	if [pair["designator"] for pair in pairs] != list(range(1, 65)):
		raise RuntimeError("single lamps did not step through designators 01-64")
	return pairs


def switch_levels(run: dict[str, Any]) -> list[dict[str, Any]]:
	results = []
	for step in run["steps"]:
		label = step.get("label", "")
		if not label.startswith("hold public switch"):
			continue
		address = int(label.rsplit(" ", 1)[1])
		snapshot = next(item for item in run["snapshots"] if item.get("label") == label + " (held)")
		rows = {display["index"]: normalized(decode_alpha(display["segments"])) for display in snapshot["displays"] if display["index"] in (0, 1)}
		results.append({"address": address, "upper": rows.get(0, ""), "lower": rows.get(1, "")})
	return results


def boot_note(run: dict[str, Any]) -> str:
	holds = ", ".join(f"{item['switch']}={item['state']}" for item in run["initial_switches"])
	return f"Power-up probe with switches {holds} held from emulator start. Solenoid on-spans: {describe_spans(solenoid_spans(run), end_time(run))}."


def slug(text: str) -> str:
	return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def raw_entry(runtime: Path, runs: Path, game: str, name: str, run: dict[str, Any]) -> dict[str, Any]:
	init_dir = "state-init" if game == GAME else f"state-init-{game}"
	init_nv = sha256(runtime / init_dir / "nvram" / f"{game}.nv")
	entry: dict[str, Any] = {
		"name": name,
		"sha256": sha256(run_file(runs, game, name)),
		"scenario_path": f"{SCENARIO_DIRECTORY}/diner-{name}.json",
		"scenario_sha256": run["scenario"]["sha256"],
		"action_count": run["scenario"]["action_count"],
		"watch_switches": run["watch_switches"],
		"self_test_pulses": service_pulses(run),
		"boot_wait_s": 0,
		"snapshot_count": len(run["snapshots"]),
		"nvram_initialization": (
			f"Fresh empty state directory; this is the one retained {game} initialization run (FACTORY SETTING), whose "
			f"nvram/{game}.nv is the only state any later {game} run inherits."
			if name == INIT_RUN
			else f"Fresh state directory holding only nvram/{game}.nv (SHA-256 {init_nv}) from the retained {game} initialization run."
		),
	}
	if run["initial_switches"]:
		entry["initial_switches"] = [{"switch": item["switch"], "state": item["state"]} for item in run["initial_switches"]]
	return entry


def service_observations(run: dict[str, Any], name: str) -> tuple[dict[str, Any], dict[str, int], list[Any]]:
	"""The observation for a Coil, Single Lamps or Switch Levels run, its named addresses and its raw pairing."""
	spans = solenoid_spans(run)
	observation: dict[str, Any] = {"solenoid_addresses_seen": sorted(spans), "diagnostic_checkpoints": checkpoints(run)}
	named: dict[str, int] = {}
	if name == "coil-test":
		steps = coil_test(run)
		held = relay_held(run, steps)
		for step in steps:
			named[f"coil-{step['step']:02d}-{slug(step['display'])}"] = step["address"]
		observation.update({
			"ordered_solenoid_on_sequence": [step["address"] for step in steps],
			"note": (
				f"Advance walk to COIL TEST (lower display 05), then two identical cycles of {len(steps)} named steps. "
				"Step:address = upper display: " + "; ".join(f"{s['step']}:{s['address']} = {s['display']}" for s in steps)
				+ f". The A/C select relay (12) is energized before and held through each step that pulses {', '.join(map(str, held))}, "
				"pulsed by itself in its own A/C SELECT step, and released for every other step."
			),
			"limitation": "A pulsed address is ROM activity, not proof that a load is fitted.",
		})
		return observation, named, steps
	if name == "single-lamps":
		pairs = single_lamps(run)
		for pair in pairs:
			named[f"lamp-{pair['designator']:02d}-{slug(pair['display'])}"] = pair["address"]
		observation.update({
			"note": (
				"Advance walk to SINGLE LAMPS (lower display 04); each Start press (public 3) steps the designator, and designator n "
				"blinks public lamp n alone for every n from 1 to 64. Designator = upper display: "
				+ "; ".join(f"{p['designator']} = {p['display']}" for p in pairs) + "."
			),
		})
		return observation, named, [{"address": p["address"], "display": p["display"]} for p in pairs]
	results = switch_levels(run)
	observation.update({
		"note": (
			"Advance walk to SWITCH LEVELS (lower display 06); each public address 1-64 and 81-88 held at 1 alone for 1.5 s. "
			"Address = upper display / lower display while held: " + "; ".join(f"{r['address']} = {r['upper']} / {r['lower']}" for r in results) + "."
		),
		"limitation": "Host-held levels written on every poll; a name shown while public n is held at 1 means the ROM reads that address as active at 1.",
	})
	return observation, named, results


def evidence_record(game: str, extractor: str, manifest_bytes: bytes, raw_runs: list[dict[str, Any]], observations: dict[str, Any]) -> dict[str, Any]:
	return {
		"format": "pinmame-machine-evidence",
		"version": 1,
		"extractor": {"id": extractor, "version": 1},
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
			"emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
			"raw_runs": raw_runs,
			"command_template": COMMAND_TEMPLATE,
			"observations": observations,
		},
	}


def build(review_root: Path) -> tuple[bytes, dict[str, Any], dict[str, dict[str, Any]]]:
	runtime = review_root / RUNTIME_RELATIVE
	runs_dir = runtime / "runs"
	manifest_bytes = (json.dumps(manifests.build_manifest(runtime, GAME), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
	raw_runs, observations = [], {}
	seen: set[int] = set()
	named: dict[str, int] = {}
	reference: dict[str, list[Any]] = {}
	for name in RUN_NAMES:
		run = load_run(runs_dir, GAME, name)
		raw_runs.append(raw_entry(runtime, runs_dir, GAME, name, run))
		spans = solenoid_spans(run)
		seen.update(spans)
		if name in ("coil-test", "single-lamps", "switch-levels"):
			observation, run_named, reference[name] = service_observations(run, name)
			named.update(run_named)
		elif name == INIT_RUN:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"note": "Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later diner_l4 runs inherit.",
			}
		elif name.startswith("boot-"):
			observation = {"solenoid_addresses_seen": sorted(spans), "note": boot_note(run), "limitation": STATIC_LIMITATION}
		else:
			observation = {
				"solenoid_addresses_seen": sorted(spans),
				"diagnostic_checkpoints": checkpoints(run),
				"note": f"Scripted scenario ({run['scenario']['action_count']} actions, see the scenario notes). Solenoid on-spans: {describe_spans(spans, end_time(run))}.",
				"limitation": SCRIPTED_LIMITATION if name == "gameplay" else STATIC_LIMITATION,
			}
		observations[name] = observation
	evidence = evidence_record(GAME, "diner-harness-runs", manifest_bytes, raw_runs, {
		"service_language": "English",
		"solenoid_addresses_seen": sorted(seen),
		"named_output_addresses": named,
		"runs": observations,
	})
	variants = {}
	for game in VARIANT_GAMES:
		game_runs, game_observations, game_named = [], {}, {}
		matches = []
		for name in VARIANT_RUN_NAMES:
			run = load_run(runs_dir, game, name)
			game_runs.append(raw_entry(runtime, runs_dir, game, name, run))
			if name == INIT_RUN:
				game_observations[name] = {
					"solenoid_addresses_seen": sorted(solenoid_spans(run)),
					"note": f"Boot to FACTORY SETTING from an empty state directory; the NVRAM written on stop is the only state later {game} runs inherit.",
				}
				continue
			observation, run_named, pairing = service_observations(run, name)
			game_named.update(run_named)
			same = pairing == reference[name]
			matches.append(f"{name}: {'identical to' if same else 'DIFFERENT from'} diner_l4")
			observation["note"] += f" Every pairing and displayed name is {'identical to' if same else 'DIFFERENT from'} the diner_l4 run of the same test."
			game_observations[name] = observation
		variants[game] = evidence_record(game, "diner-variant-harness-runs", manifest_bytes, game_runs, {
			"service_language": "English",
			"named_output_addresses": game_named,
			"runs": game_observations,
		})
	return manifest_bytes, evidence, variants


def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	args = parser.parse_args()
	review_root = working_root()
	runtime = review_root / RUNTIME_RELATIVE
	manifest_bytes, evidence, variants = build(review_root)
	if args.check:
		if (runtime / "manifest.json").read_bytes() != manifest_bytes:
			raise SystemExit(f"{runtime / 'manifest.json'} does not match the files beside it")
		manifests.check_manifest(runtime, GAME)
		if EVIDENCE_PATH.read_bytes() != canonical_bytes(evidence):
			raise SystemExit(f"{EVIDENCE_PATH} is not the summary of the raw runs in {runtime}")
		for game, record in variants.items():
			if variant_evidence_path(game).read_bytes() != canonical_bytes(record):
				raise SystemExit(f"{variant_evidence_path(game)} is not the summary of the raw runs in {runtime}")
		print("Diner runtime evidence and manifest match the raw runs.")
		return
	manifests.write_manifest(runtime, GAME)
	EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
	EVIDENCE_PATH.write_bytes(canonical_bytes(evidence))
	for game, record in variants.items():
		variant_evidence_path(game).write_bytes(canonical_bytes(record))
	print(f"wrote {EVIDENCE_PATH} and {len(variants)} variant files")


if __name__ == "__main__":
	main()
