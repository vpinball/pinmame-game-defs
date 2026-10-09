"""Build the committed The Who's Tommy Pinball Wizard runtime evidence from the retained harness runs.

Reads the retained raw runs of the US 4.00 (``tomy_400``) service tests and a game start
(``PINMAME_REVIEW_ARTIFACTS_ROOT``), pairs the curator's visual DMD readings (``tools/tommy_readings.json``)
with each frame's pixel digest, derives the switch-to-coil and test-button observations, and writes two
committed files:

* ``evidence/runtime/data-east/the-who-s-tommy-pinball-wizard-tomy_400-service-tests.json``, a
  ``pinmame-machine-evidence`` bundle, and
* ``tools/tommy_runtime.json``, the compact facts the curator consumes.

The raw runs, DMD frames and isolated state directories stay external under the working root, covered by
a canonical manifest (``tools/build_external_evidence_manifest.py``). ``--check`` rebuilds both files and
refuses any difference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

import build_external_evidence_manifest as manifest
import tommy_manual

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.the-who-s-tommy-pinball-wizard.1994"
SESSION = f"{KEY}/session-20261009/final/tomy_400"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/the-who-s-tommy-pinball-wizard-tomy_400-service-tests.json"
RUNTIME_PATH = ROOT / "tools/tommy_runtime.json"
READINGS_PATH = ROOT / "tools/tommy_readings.json"
RUNS = ("active-switches", "lamp-test", "diagnostic-tour", "cycling-coils", "cycling-flashers", "coil-test-fire", "mirror-test", "arch-test", "printer-interface", "trough-serve")
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
LIBRARY_SHA256 = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
ROM_ARCHIVE_SHA256 = "6fa8d210ccd1c45c673bb970e24ea7996476fff289f5215b3fbb9b3424af5aa6"
ROM_ARCHIVE = Path("L:/Visual Pinball/VPinMAME/roms/tomy_400.zip")
# The ROM prints ORG where the manual prints ORN; nothing else differs in the wire abbreviations.
WIRE_SPELLING = {"ORG": "ORN"}
# Outputs the attract, intro and service screens drive on their own: the relay, G.I., game-on and flash lamps.
LIGHT_SHOW_OUTPUTS = {10, 11, 23, 15, *range(25, 33)}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_wires(text: str) -> str:
    return " ".join("-".join(WIRE_SPELLING.get(part, part) for part in token.split("-")) for token in text.split())


def load_run(base: Path, name: str) -> dict:
    """A retained run, refused unless it is a clean tomy_400 run on the pinned emulator build."""
    run = json.loads((base / name / "run.json").read_text(encoding="utf-8"))
    if run.get("game") != "tomy_400" or run.get("library_sha256") != LIBRARY_SHA256 or run.get("failure"):
        raise SystemExit(f"{name}: not a clean tomy_400 run on pinmame64.dll {LIBRARY_SHA256} (game {run.get('game')!r}, failure {run.get('failure')!r})")
    return run


def snapshot(run: dict, label: str) -> dict:
    matches = [item for item in run["snapshots"] if item["label"] == label]
    if len(matches) != 1:
        raise SystemExit(f"expected one snapshot labelled {label!r}, found {len(matches)}")
    return matches[0]


def frame(base: Path, run_name: str, item: dict) -> dict:
    """The snapshot's DMD frame, refused unless the retained PGM's pixels hash to the recorded digest."""
    (display,) = [entry for entry in item["displays"] if entry.get("pixel_sha256")]
    path = base / run_name / "dmd" / Path(display["artifact"].replace("\\", "/")).name
    header, payload = path.read_bytes().split(b"\n", 2)[:2], path.read_bytes().split(b"\n", 3)[3]
    max_level = (1 << max(int(display["layout"].get("depth", 1)), 1)) - 1
    scaled = {round(level * 255 / max_level) for level in range(max_level + 1)}
    candidates = [payload] + ([bytes(round(value * max_level / 255) for value in payload)] if set(payload) <= scaled else [])
    if header != [b"P5", f"{display['layout']['width']} {display['layout']['height']}".encode("ascii")] or display["pixel_sha256"] not in {
        hashlib.sha256(raw).hexdigest() for raw in candidates
    }:
        raise SystemExit(f"{path}: the retained frame's pixels do not hash to the recorded digest {display['pixel_sha256']}")
    return display


def step_transitions(run: dict, label: str) -> list[int]:
    (step,) = [item for item in run["steps"] if item["label"] == label]
    return sorted({item["number"] for item in step["transitions"]["solenoids"] if 1 in item["states"] and item["number"] not in (23, 45, 46, 47, 48)})


def build(base: Path, *, write_manifest: bool) -> tuple[dict, dict]:
    readings = json.loads(READINGS_PATH.read_text(encoding="utf-8"))
    runs = {name: load_run(base, name) for name in RUNS}
    switch_chart = tommy_manual.switch_data()["chart"]
    lamp_chart = tommy_manual.lamp_data()["chart"]
    snapshots: list[dict] = []

    def read(reading: dict, label: str, text: str) -> dict:
        item = snapshot(runs[reading["run"]], reading["snapshot"])
        display = frame(base, reading["run"], item)
        if display["pixel_sha256"] != reading["pixel_sha256"]:
            raise SystemExit(f"{label}: frame {display['pixel_sha256']} is not the frame that was read ({reading['pixel_sha256']}); read it again")
        snapshots.append({
            "label": label, "display_index": 0, "pixel_sha256": display["pixel_sha256"], "nonzero_pixels": display["nonzero_pixels"],
            "interpreted_text": text, "active_solenoid_addresses": item["active_solenoids"],
        })
        return item

    # --- Active Switch Test ----------------------------------------------------------------------------------
    read(readings["screens"]["active-switch-baseline"], "Active Switch Test baseline, every public switch at 0", readings["screens"]["active-switch-baseline"]["text"])
    switch_names = {}
    for address in range(1, 65):
        reading = readings["switches"][str(address)]
        chart = switch_chart[address]
        if normalize_wires(reading["wires"]) != f"{chart['drive']['wire']} {chart['return']['wire']}" or reading["number"] != address:
            raise SystemExit(f"switch {address}: ROM wires {reading['wires']} #{reading['number']} disagree with the manual chart")
        read(reading, f"Active Switch Test, public switch {address} held 900 ms", f"-ACTIVE SWITCH TEST- | {reading['name']} | {reading['wires']} #{address:02d}")
        switch_names[str(address)] = {"name": reading["name"], "wires": reading["wires"]}
    for key, reading in readings["flipper_column"].items():
        text = "-ACTIVE SWITCH TEST- | NONE" if reading["name"] is None else f"-ACTIVE SWITCH TEST- | {reading['name']} | {reading['wires']} #{reading['number']}"
        read(reading, f"Active Switch Test, flipper-column public switch {key} held 900 ms", text)
    if {key for key, reading in readings["flipper_column"].items() if reading["name"]} != {"82", "84"}:
        raise SystemExit("only 82 and 84 should reach the ROM from the flipper column")

    # --- Lamp tests -------------------------------------------------------------------------------------------
    lamp_names = {}
    for address in range(1, 65):
        reading = readings["lamps"][str(address)]
        if reading is None:
            continue
        chart = lamp_chart[address]
        if normalize_wires(reading["wires"]) != f"{chart['drive']['wire']} {chart['return']['wire']}" or reading["number"] != address:
            raise SystemExit(f"lamp {address}: ROM wires {reading['wires']} #{reading['number']} disagree with the manual chart")
        item = read(reading, f"Lamp Test, lamp {address} selected", f"-LAMP TEST- | {reading['name']} | {reading['wires']} #{address:02d}")
        if item["active_lamps"] != [address]:
            raise SystemExit(f"lamp test: {address} selected but lamps {item['active_lamps']} lit")
        lamp_names[str(address)] = {"name": reading["name"], "wires": reading["wires"]}
    skipped = sorted(int(key) for key, value in readings["lamps"].items() if value is None)
    row_column = {}
    for kind in ("row", "column"):
        for number, reading in readings[f"{kind}_lamps"].items():
            item = read(reading, f"{kind.title()} Lamps test, {kind} {number}", f"-{kind.upper()} LAMPS ON- | {reading['text']}")
            expected = [(int(number) - 1) * 8 + r for r in range(1, 9)] if kind == "column" else [c * 8 + int(number) for c in range(8)]
            if item["active_lamps"] != expected or item["active_lamps"] != reading["lamps"]:
                raise SystemExit(f"{kind} {number}: lamps {item['active_lamps']} are not the {kind}'s eight lamps")
            for address in item["active_lamps"]:
                row_column.setdefault(address, []).append(reading["text"])

    # --- Cycling coils and flashers -----------------------------------------------------------------------------
    cycling = runs["cycling-coils"]
    ons = [(event["time_s"], event["number"]) for event in cycling["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["number"] not in (10, 23, 44, 51)]
    entered = snapshot(cycling, "cycling coils tick 1")["time_s"]
    start = [time_s for time_s, number in ons if number == 1 and time_s >= entered][0]
    order: list[int] = []
    for time_s, number in ons:
        if time_s < start:
            continue
        if number == 1 and order:
            break
        order.append(number)
    expected = [n for drive in range(1, 9) for n in (drive, drive + 24)] + [9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]
    if order != expected:
        raise SystemExit(f"unexpected cycling order: {order}")
    coil_names = {}
    for key, reading in readings["cycling_coils"].items():
        read(reading, f"Cycling Coils, public solenoid {key} step", f"-CYCLING COILS- | {reading['name']}")
        coil_names[key] = reading["name"]
    flasher_ons = [event["number"] for event in runs["cycling-flashers"]["events"] if event["event"] == "solenoid" and event["state"] == 1 and event["number"] in {15, *range(25, 33)}]
    if flasher_ons[:9] != [25, 26, 27, 28, 29, 30, 31, 32, 15]:
        raise SystemExit(f"unexpected cycling-flashers order {flasher_ons[:9]}")

    # --- Coil Test (select with the flipper buttons, fire with Start) -------------------------------------------
    coil_test = []
    for reading in readings["coil_test"]:
        entry = reading["entry"]
        read(reading, f"Coil Test, entry {entry} {reading['number']}", f"-COIL TEST- | {reading['name']} | {reading['wires']} {reading['number']}")
        fired = step_transitions(runs["coil-test-fire"], f"entry {entry}: Start short press fires the selected entry")
        coil_test.append({"entry": entry, "number": reading["number"], "name": reading["name"], "wires": reading["wires"], "fired": fired})

    # --- Mirror and Arch tests ------------------------------------------------------------------------------------
    for key in ("mirror-baseline", "mirror-switch-28", "mirror-switch-31", "mirror-switch-32", "arch-baseline", "arch-start-held"):
        reading = readings["screens"][key]
        read(reading, f"{'Mirror' if key.startswith('mirror') else 'Arch'} test: {key}", reading["text"])
    actions = []
    for run_name in ("mirror-test", "arch-test"):
        run = runs[run_name]
        for label in ("Start short press 1", "Start short press 2", "Start long press 1"):
            fired = step_transitions(run, label)
            actions.append({
                "label": f"{run_name}: {label}", "input_kind": "switch", "input_address": 3, "observed_switch_addresses": [],
                "host_stimulus_switch_addresses": [3], "active_solenoid_addresses": snapshot(run, f"{label} (held)")["active_solenoids"],
                "transitioned_solenoid_addresses": fired, "result": "observed" if fired else "no_matching_transition",
            })
        for address in [*range(1, 65), *range(81, 89)]:
            label = f"hold public switch {address}"
            if address == 3 or not [step for step in run["steps"] if step["label"] == label]:
                continue
            fired = step_transitions(run, label)
            if fired:
                actions.append({
                    "label": f"{run_name}: {label}", "input_kind": "switch", "input_address": address, "observed_switch_addresses": [],
                    "host_stimulus_switch_addresses": [address], "active_solenoid_addresses": snapshot(run, f"{label} (held)")["active_solenoids"],
                    "transitioned_solenoid_addresses": fired, "result": "observed",
                })
    causal = {(action["label"].split(":")[0], action["input_address"]): action["transitioned_solenoid_addresses"] for action in actions if action["input_address"] != 3}
    expected_causal = {16: [3], 19: [4], 23: [5], 47: [6]}
    for run_name in ("mirror-test", "arch-test"):
        found = {address: fired for (name, address), fired in causal.items() if name == run_name}
        if found != expected_causal:
            raise SystemExit(f"{run_name}: switch-to-coil pairs {found} differ from {expected_causal}")
    start_fires = {action["label"].split(":")[0]: action["transitioned_solenoid_addresses"] for action in actions if action["input_address"] == 3}
    if start_fires != {"mirror-test": [14], "arch-test": [44, 51]}:
        raise SystemExit(f"unexpected Start responses {start_fires}")

    # --- Adjustment 56 PRINTER INTERFACE: Start prints nothing on this ROM -------------------------------------------
    printer_reading = readings["screens"]["printer-adjustment-56"]
    read(printer_reading, "Adjustment 56 display while Start is held", printer_reading["text"])
    printer_fired = step_transitions(runs["printer-interface"], "Adjustment 56: press Start to print")
    printer_actions = [{
        "label": "Adjustment 56: press Start to print", "input_kind": "switch", "input_address": 3, "observed_switch_addresses": [],
        "host_stimulus_switch_addresses": [3], "active_solenoid_addresses": snapshot(runs["printer-interface"], "Adjustment 56: press Start to print (held)")["active_solenoids"],
        "transitioned_solenoid_addresses": printer_fired, "result": "observed" if printer_fired else "no_matching_transition",
    }]
    if printer_fired:
        raise SystemExit(f"Adjustment 56 Start fired {printer_fired}; the readings expect nothing")

    # --- CN3 lines 37-44 and the custom solenoid 51 over every run ---------------------------------------------------
    cn3: dict[int, list] = {}
    for run_name, run in runs.items():
        for event in run["events"]:
            if event["event"] == "solenoid" and event["number"] in (*range(37, 45), 51):
                cn3.setdefault(event["number"], []).append((run_name, event["time_s"], event["state"]))
    def edges(address: int) -> list[tuple[str, float, int]]:
        return [(name, round(time_s, 2), state) for name, time_s, state in cn3[address]]

    # PinMAME reports the custom solenoid in the same update as line 44, within a frame of it.
    if set(cn3) != {44, 51} or len(cn3[44]) != len(cn3[51]) or any(
        a[0] != b[0] or a[2] != b[2] or abs(a[1] - b[1]) > 0.02 for a, b in zip(edges(44), edges(51))
    ):
        raise SystemExit(f"outputs 37-44 and 51: expected only 44 and 51, moving together; saw {sorted(cn3)}")
    boot_pulses = sorted({round(t2 - t1, 2) for (n1, t1, s1), (n2, t2, s2) in zip(cn3[44], cn3[44][1:]) if n1 == n2 and s1 == 1 and s2 == 0 and t1 < 9})

    # --- Game start (trough serve) ------------------------------------------------------------------------------------
    serve = runs["trough-serve"]
    events = [event for event in serve["events"] if event["event"] in ("solenoid", "switch")]
    start_press = [event["time_s"] for event in events if event["event"] == "switch" and event["number"] == 3 and event["state"] == 1][0]
    ball_on_15 = [event["time_s"] for event in events if event["event"] == "switch" and event["number"] == 15 and event["state"] == 1][0]
    ball_off_15 = [event["time_s"] for event in events if event["event"] == "switch" and event["number"] == 15 and event["state"] == 0][0]
    def ons_between(lower: float, upper: float) -> dict[int, int]:
        counts: dict[int, int] = {}
        for event in events:
            if event["event"] == "solenoid" and event["state"] == 1 and lower <= event["time_s"] < upper and event["number"] not in LIGHT_SHOW_OUTPUTS:
                counts[event["number"]] = counts.get(event["number"], 0) + 1
        return counts
    power_up = ons_between(0.0, 9.0)
    waiting = ons_between(start_press, ball_on_15)
    releasing = ons_between(ball_on_15, ball_off_15)
    mirror_on = [event["time_s"] for event in events if event["event"] == "solenoid" and event["number"] == 14]
    serve_facts = {
        "power_up_pulses": {str(key): value for key, value in sorted(power_up.items())},
        "start_to_15_closed": {str(key): value for key, value in sorted(waiting.items())},
        "while_15_closed": {str(key): value for key, value in sorted(releasing.items())},
        "start_press_s": round(start_press, 2), "ball_on_15_s": round(ball_on_15, 2), "ball_off_15_s": round(ball_off_15, 2),
        "mirror_motor_first_on_s": round(mirror_on[0], 2),
    }
    if waiting.get(1, 0) < 5 or releasing.get(2, 0) < 3:
        raise SystemExit(f"trough serve: unexpected pulses {serve_facts}")
    serve_actions = [{
        "label": "Game start: Start pressed with balls on 9-14 and 15 open, until a ball reaches 15",
        "input_kind": "switch", "input_address": 3, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [3],
        "active_solenoid_addresses": [], "transitioned_solenoid_addresses": sorted(waiting), "result": "observed",
    }, {
        "label": "Game start: a ball held on the release position 15",
        "input_kind": "switch", "input_address": 15, "observed_switch_addresses": [], "host_stimulus_switch_addresses": [15],
        "active_solenoid_addresses": [], "transitioned_solenoid_addresses": sorted(releasing), "result": "observed",
    }]

    # --- Raw-run records ---------------------------------------------------------------------------------------------
    raw_runs = []
    per_run: dict[str, dict] = {}
    all_solenoids: set[int] = set()
    for name in RUNS:
        run = runs[name]
        scenario_path = ROOT / f"tools/harness-scenarios/data-east/tomy-400-{name}.json"
        scenario_sha = sha256_file(scenario_path)
        if sha256_file(base / name / "scenario.json") != scenario_sha:
            raise SystemExit(f"{name}: retained scenario differs from the committed scenario")
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        checkpoints = [
            {"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
            for step in run["steps"] if step["type"] == "pulse_until_display"
        ]
        solenoids = sorted({event["number"] for event in run["events"] if event["event"] == "solenoid"})
        all_solenoids.update(solenoids)
        raw_runs.append({
            "name": name, "sha256": sha256_file(base / name / "run.json"),
            "scenario_path": f"tools/harness-scenarios/data-east/tomy-400-{name}.json", "scenario_sha256": scenario_sha,
            "action_count": len(scenario["actions"]), "watch_switches": scenario.get("watch_switches", []),
            "self_test_pulses": sum(item["after_service_pulses"] for item in checkpoints),
            "nvram_initialization": "new empty isolated state directory; no NVRAM inherited", "boot_wait_s": 8.0,
            "snapshot_count": len(run["snapshots"]),
        })
        per_run[name] = {"diagnostic_checkpoints": checkpoints, "solenoid_addresses_seen": solenoids}
    per_run["cycling-coils"]["ordered_solenoid_on_sequence"] = order
    per_run["cycling-flashers"]["ordered_solenoid_on_sequence"] = flasher_ons[:18]
    per_run["mirror-test"]["named_action_observations"] = [a for a in actions if a["label"].startswith("mirror-test")]
    per_run["arch-test"]["named_action_observations"] = [a for a in actions if a["label"].startswith("arch-test")]
    per_run["trough-serve"]["named_action_observations"] = serve_actions
    per_run["printer-interface"]["named_action_observations"] = printer_actions
    per_run["trough-serve"]["note"] = (
        "Counts exclude the outputs the attract, intro and lamp shows drive by themselves (10, 11, 15, 23 and 25-32). The host moved the balls: a ball "
        "reached 15 only when the host closed it, and left 15 only when the host opened it, so the pulse counts measure the ROM's retries, not travel times."
    )
    per_run["coil-test-fire"]["note"] = "Each entry is selected with the right flipper button (public 82) and fired with Start; the transitions per entry are in the curator facts."

    # Regeneration writes the external manifest; --check only verifies it and never touches the retained runs.
    try:
        manifest_digest = manifest.write_manifest(base, "tomy_400") if write_manifest else manifest.check_manifest(base, "tomy_400")
    except ValueError as error:
        raise SystemExit(f"retained runs: {error}") from error
    source_locator = (
        f"US 4.00 (tomy_400) in {len(RUNS)} fresh-state harness runs: the Active Switch Test of public 1-64 and 81-88, the discrete Lamp Test, the Row and Column "
        "lamp tests, Cycling Coils, Cycling Flashers, the Coil Test fired entry by entry, the Mirror and Arch tests, Adjustment 56 PRINTER INTERFACE, and a game start with the host serving a ball from "
        f"the trough; {len(snapshots)} visually read 128x32 frames paired with their pixel digests; the raw runs stay under the working root with a canonical manifest"
    )
    facts = {
        "format": "pinmame-tommy-runtime-facts",
        "version": 1,
        "source": EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "source_locator": source_locator,
        "rom_switch_names": switch_names,
        "rom_lamp_names": lamp_names,
        "lamps_skipped_by_lamp_test": skipped,
        "lamp_row_column": {str(address): texts for address, texts in sorted(row_column.items()) if address in skipped},
        "cycling_coils_order": order,
        "cycling_coil_names": coil_names,
        "coil_test": coil_test,
        "mirror_and_arch": {"start": start_fires, "switch_to_coil": {str(k): v for k, v in expected_causal.items()}},
        "cn3_lines": {"moving": [44, 51], "power_up_pulse_s": boot_pulses, "printer_start_fired": printer_fired},
        "trough_serve": serve_facts,
    }
    evidence = {
        "driver_ids": ["tomy_400"],
        "extractor": {"id": "tools/build_tommy_runtime_evidence.py", "version": 1},
        "format": "pinmame-machine-evidence",
        "machine_ids": [KEY],
        "mechanisms": [],
        "outputs": [],
        "recreation_notes": [],
        "runtime": {
            "game": "tomy_400",
            "rom_archive_sha256": ROM_ARCHIVE_SHA256,
            "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
            "raw_runs": raw_runs,
            "command_template": (
                "python tools/tommy_harness.py --library <libpinmame> --game tomy_400 --rom-path <read-only-rom-root> --work-dir <new-isolated-state> "
                "--scenario tools/harness-scenarios/data-east/tomy-400-<run>.json --boot-wait 8 --dmd-dir <external-dmd-dir> --output <external-run.json>. "
                "No keyboard handling: every stimulus is a direct public switch write (the Black Advance button at -7, the Green input at -6, then playfield and "
                "cabinet addresses). tools/tommy_harness.py replaces only the display-title checkpoint with exact title-band matches of visually read retained "
                "frames (tools/tommy_header_templates.json). Each DMD reading in diagnostic_snapshots was read by a curator from the retained 128x32 frame whose "
                "pixel digest is recorded beside it."
            ),
            "observations": {
                "service_language": "US English 4.00",
                "solenoid_addresses_seen": sorted(all_solenoids),
                "lamp_addresses_seen": list(range(1, 65)),
                "diagnostic_snapshots": snapshots,
                "runs": per_run,
            },
        },
        "source": {
            "attribution": "Generated locally from pinned PinMAME and the user-authorized ROM corpus; ROM bytes remain external.",
            "kind": "runtime_scenario",
            "license": "NOASSERTION",
            "manifest_algorithm": (
                "source.sha256 is SHA-256 of manifest.json's exact UTF-8 bytes. manifest.json is compact canonical JSON with sorted keys, separators=(',', ':'), "
                "ensure_ascii=False, plus one LF; it lists every file below source.path except manifest.json and manifest.sha256 as {path, sha256, size}, using "
                "sorted POSIX-relative paths."
            ),
            "path": f"external:pinmame-review-artifacts/{SESSION}",
            "quality": "observed",
            "repository": "https://github.com/vpinball/pinmame",
            "revision": PINMAME_REVISION,
            "sha256": manifest_digest,
        },
        "states": [],
        "switches": [],
        "version": 1,
    }
    return evidence, facts


def _bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Rebuild and refuse any difference from the committed files.")
    args = parser.parse_args()
    root = os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if not root:
        raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT must point at the working root's review-artifacts directory")
    if ROM_ARCHIVE.is_file() and sha256_file(ROM_ARCHIVE) != ROM_ARCHIVE_SHA256:
        raise SystemExit(f"{ROM_ARCHIVE} is not the ROM archive the runs used")
    evidence, facts = build(Path(root) / SESSION, write_manifest=not args.check)
    outputs = ((EVIDENCE_PATH, _bytes(evidence)), (RUNTIME_PATH, _bytes(facts)))
    if args.check:
        for path, payload in outputs:
            if path.read_bytes().replace(b"\r\n", b"\n") != payload:
                raise SystemExit(f"{path} differs from the retained runs")
        print("Tommy runtime evidence matches the retained runs.")
        return
    for path, payload in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    print(f"Wrote {EVIDENCE_PATH.relative_to(ROOT)} and {RUNTIME_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
