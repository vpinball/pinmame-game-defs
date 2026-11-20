"""Build the committed Last Action Hero runtime evidence from the retained harness runs.

Reads the seven retained raw runs of the US 1.12 service tests, the printer adjustment, a game start and a game in
play (``PINMAME_REVIEW_ARTIFACTS_ROOT``), pairs the curator's visual DMD readings (``lah_readings``) with each
frame's pixel digest, derives the switch-to-output observations, and writes two committed files:

* ``evidence/runtime/data-east/last-action-hero-lah_112-service-tests.json``, a
  ``pinmame-machine-evidence`` bundle, and
* ``tools/last_action_hero_runtime.json``, the compact facts the curator consumes.

The raw runs, DMD frames and isolated state directories stay external under the working root, covered by a
canonical manifest (``tools/build_external_evidence_manifest.py``). ``--write`` rebuilds both committed files and
rewrites that manifest; ``--check`` rebuilds both files, refuses any difference, and only verifies the manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import build_external_evidence_manifest as manifest
import lah_manual
import lah_readings as readings

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.last-action-hero.1993"
GAME = "lah_112"
SESSION = "data-east.last-action-hero.1993/session-20261120/final/lah_112"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/last-action-hero-lah_112-service-tests.json"
RUNTIME_PATH = ROOT / "tools/last_action_hero_runtime.json"
RUNS = ("active-switches", "lamp-test", "cycling-coils", "crane-magnet-laser", "printer-interface", "trough-serve", "captive-lamps")
# The captive-lamps run's stimuli, in order: the two return lanes, then each captive-ball target and rollover.
CAPTIVE_SWITCHES = [41, 42, 40, 56, 39, 55]
# Outputs the attract and game-start lamp shows drive on their own: the crane flash lamps (9), the relay, G.I., game-on
# and the flash-lamp groups.
LIGHT_SHOW_OUTPUTS = {9, 10, 11, 23, *range(25, 33)}
PINMAME_REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ROM_ARCHIVE = Path("L:/Visual Pinball/VPinMAME/roms/lah_112.zip")
# The user-authorized archive every retained run booted; checked whenever the archive is reachable.
ROM_ARCHIVE_SHA256 = "3143ec1d9ff49c0344da87a3c8e5a8202d59322c5edee7bb903e0bb7affb6363"
PRINTER_LABEL = "press Start on the adjustment shown"
PRINTER_TEXT = "-ADJUSTMENT- | 58 | PRINTER INTERFACE | PRESS START TO PRINT"
# The ROM prints the orange wire as ORG; the manual's charts print ORN.
ROM_WIRE_SPELLING = {"ORG": "ORN"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manual_spelling(wire: str) -> str:
    return "-".join(ROM_WIRE_SPELLING.get(part, part) for part in wire.split("-"))


def load_run(base: Path, name: str) -> dict:
    """A retained run, refused unless it is a clean lah_112 run on the pinned emulator build."""
    run = json.loads((base / name / "run.json").read_text(encoding="utf-8"))
    if run.get("game") != GAME or run.get("library_sha256") != LIBRARY_SHA256 or run.get("failure"):
        raise SystemExit(f"{name}: not a clean {GAME} run on pinmame64.dll {LIBRARY_SHA256} (game {run.get('game')!r}, failure {run.get('failure')!r})")
    return run


def snapshots_by_label(run: dict) -> dict[str, dict]:
    return {snapshot["label"]: snapshot for snapshot in run["snapshots"]}


FRAME_ROOT: Path | None = None  # the session directory the runs' DMD artifact paths are relative to


def display(snapshot: dict) -> dict:
    """The snapshot's DMD frame, refused unless the retained PGM's pixels hash to the recorded digest.

    The harness hashes the raw levels it received and writes the PGM from them.
    """
    (frame,) = [item for item in snapshot["displays"] if item.get("pixel_sha256")]
    path = FRAME_ROOT / frame["artifact"].replace("\\", "/")
    header, payload = path.read_bytes().split(b"\n255\n", 1)
    max_level = (1 << max(int(frame["layout"].get("depth", 1)), 1)) - 1
    scaled = {round(level * 255 / max_level) for level in range(max_level + 1)}
    # The harness writes raw levels unchanged when any exceeds the depth's maximum, and scales them otherwise.
    candidates = [payload] + ([bytes(round(value * max_level / 255) for value in payload)] if set(payload) <= scaled else [])
    expected_header = f"P5\n{frame['layout']['width']} {frame['layout']['height']}".encode("ascii")
    if header != expected_header or frame["pixel_sha256"] not in {hashlib.sha256(raw).hexdigest() for raw in candidates}:
        raise SystemExit(f"{path}: the retained frame's pixels do not hash to the recorded digest {frame['pixel_sha256']}")
    return frame


def frame_snapshot(label: str, snapshot: dict, text: str) -> dict:
    frame = display(snapshot)
    return {
        "label": label, "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
        "interpreted_text": text, "active_solenoid_addresses": snapshot["active_solenoids"],
    }


def solenoid_on_events(run: dict, lower: float = 0.0, upper: float = 1e9) -> list[tuple[float, int]]:
    return [
        (event["time_s"], event["number"])
        for event in run["events"]
        if event["event"] == "solenoid" and event["state"] == 1 and lower <= event["time_s"] < upper
    ]


def counts_text(counts: dict[str, int]) -> str:
    """Switch-on counts as compact prose: ``22 x1`` or ``none``."""
    return ", ".join(f"{number} x{counts[number]}" for number in sorted(counts, key=int)) or "none"


def step_window(run: dict, step: dict, tail: float) -> tuple[float, float]:
    """The interval from the step's switch closing to ``tail`` seconds after it opens, cut at the next switch write."""
    switch_events = [e for e in run["events"] if e["event"] == "switch" and e.get("step") == step["step"]]
    begin = [e for e in switch_events if e["state"] == 1][0]["time_s"]
    end = [e for e in switch_events if e["state"] == 0][0]["time_s"]
    later = [e["time_s"] for e in run["events"] if e["event"] == "switch" and e["time_s"] > end and e.get("step") != step["step"]]
    return begin, min([end + tail, *later])


def build(base: Path, *, write_manifest: bool) -> tuple[dict, dict]:
    global FRAME_ROOT
    FRAME_ROOT = base.parents[1]
    runs = {name: load_run(base, name) for name in RUNS}
    switch_chart = lah_manual.switch_data()["chart"]
    lamp_chart = lah_manual.lamp_data()["chart"]
    snapshots: list[dict] = []

    # --- Active Switch Test ------------------------------------------------------------------------------
    active = runs["active-switches"]
    by_label = snapshots_by_label(active)
    baseline = [s for s in active["snapshots"] if s["label"].startswith("advance with the Black")][0]
    snapshots.append(frame_snapshot("Active Switch Test baseline, matrix and flipper inputs at 0 with Green -6 held", baseline, "-ACTIVE SWITCH TEST- | NONE"))
    switch_names: dict[str, dict] = {}
    for address in range(1, 65):
        name, column_wire, row_wire = readings.SWITCH_READINGS[address]
        chart = switch_chart[address]
        if (manual_spelling(column_wire), manual_spelling(row_wire)) != (chart["drive"]["wire"], chart["return"]["wire"]):
            raise SystemExit(f"switch {address}: ROM wires {column_wire} {row_wire} disagree with the manual chart")
        item = frame_snapshot(
            f"Active Switch Test, public switch {address} held 900 ms", by_label[f"hold public switch {address} (held)"],
            f"-ACTIVE SWITCH TEST- | {name} | {column_wire} {row_wire} #{address:02d}",
        )
        switch_names[str(address)] = {"name": name, "wires": f"{column_wire} {row_wire}", "pixel_sha256": item["pixel_sha256"]}
        snapshots.append(item)
    for address, reading in readings.FLIPPER_COLUMN_READINGS.items():
        if reading is not None:
            matrix_chart = switch_chart[reading[0]]
            if (reading[2], reading[3]) != (matrix_chart["drive"]["wire"], matrix_chart["return"]["wire"]):
                raise SystemExit(f"flipper-column switch {address}: ROM wires {reading[2]} {reading[3]} disagree with the chart row of switch {reading[0]}")
        text = "-ACTIVE SWITCH TEST- | NONE" if reading is None else f"-ACTIVE SWITCH TEST- | {reading[1]} | {reading[2]} {reading[3]} #{reading[0]}"
        snapshots.append(frame_snapshot(
            f"Active Switch Test, flipper-column public switch {address} held 900 ms", by_label[f"hold public switch {address} (held)"], text,
        ))

    # --- Lamp Test ---------------------------------------------------------------------------------------
    lamp_run = runs["lamp-test"]
    lamp_labels = snapshots_by_label(lamp_run)
    lamp_names: dict[str, dict] = {}
    for press in range(1, 65):
        address = 65 - press
        snapshot = lamp_labels[f"Start press {press}"]
        if snapshot["active_lamps"] != [address]:
            raise SystemExit(f"lamp test press {press}: expected lamp {address} lit, saw {snapshot['active_lamps']}")
        name, column_wire, row_wire = readings.LAMP_READINGS[address]
        chart = lamp_chart[address]
        if (manual_spelling(column_wire), manual_spelling(row_wire)) != (chart["drive"]["wire"], chart["return"]["wire"]):
            raise SystemExit(f"lamp {address}: ROM wires {column_wire} {row_wire} disagree with the manual chart")
        item = frame_snapshot(f"Lamp Test, Start press {press}, lamp {address} lit", snapshot, f"-LAMP TEST- | {name} | {column_wire} {row_wire} #{address:02d}")
        lamp_names[str(address)] = {"name": name, "wires": f"{column_wire} {row_wire}", "pixel_sha256": item["pixel_sha256"]}
        snapshots.append(item)
    if lamp_labels["Start press 65"]["active_lamps"] or lamp_labels["Start press 66"]["active_lamps"] != [64]:
        raise SystemExit("lamp test: press 65 should light nothing and press 66 should return to lamp 64")

    # --- Cycling Coils -----------------------------------------------------------------------------------
    def relay_10_at_rises(run: dict, numbers) -> list[tuple[float, int, float | None]]:
        """(time, output, ms until 10's next fall) for each rise of the given outputs while the published 10 is on."""
        events = [e for e in run["events"] if e["event"] == "solenoid"]
        state: dict[int, int] = {}
        found = []
        for index, event in enumerate(events):
            before = state.get(event["number"], 0)
            state[event["number"]] = event["state"]
            if event["number"] in numbers and event["state"] and not before:
                fall = next((e["time_s"] for e in events[index + 1:] if e["number"] == 10 and e["state"] == 0), None)
                found.append((event["time_s"], event["number"], state.get(10, 0), None if fall is None else (fall - event["time_s"]) * 1000))
        return found

    drive_9 = [rise for name in RUNS for rise in relay_10_at_rises(runs[name], (9,))]
    drive_9_relay_10 = {"runs": len(RUNS), "rises": len(drive_9), "with_10_on": sum(1 for _, _, on, _ in drive_9 if on)}
    left_rises = relay_10_at_rises(runs["cycling-coils"], range(1, 9))
    # A fall of 10 within 1 ms of the coil's rise belongs to the same published update; a later one trails it by a vertical blank.
    same_update = [lag for _, _, on, lag in left_rises if on and lag is not None and lag < 1.0]
    trailing = [lag for _, _, on, lag in left_rises if on and lag is not None and lag >= 1.0]
    if not trailing:
        raise SystemExit("cycling-coils run: the readings say the published 10 trails some left-coil rises")
    relay_overlap = {
        "left_coil_rises": len(left_rises), "same_update": len(same_update), "trailing": len(trailing),
        "min_trail_ms": round(min(trailing), 1), "max_trail_ms": round(max(trailing), 1),
    }

    coil_run = runs["cycling-coils"]
    ticks = [(s["time_s"], s) for s in coil_run["snapshots"] if s["label"].startswith("cycling coils tick")]
    ons = solenoid_on_events(coil_run)
    start = [t for t, n in ons if n == 1 and t > 63][0]
    cycle: list[tuple[float, int]] = []
    for time_s, number in ons:
        if time_s < start - 0.001:
            continue
        if number == 1 and cycle:
            break
        cycle.append((time_s, number))
    order = [n for _, n in cycle if n != 10]
    coil_sequence = [n for n in order if n < 25]
    flash_sequence = [n for n in order if n >= 25]
    if coil_sequence != list(range(1, 10)) + list(range(11, 23)) or flash_sequence != list(range(25, 33)):
        raise SystemExit(f"unexpected cycling order: {order}")
    relay_steps = [n for (_, n), (_, following) in zip(cycle, cycle[1:]) if n == 10 and 25 <= following <= 32]
    if len(relay_steps) != 8 or [n for _, n in cycle].count(10) != 8:
        raise SystemExit("cycling coils: the Left/Right relay should fire once before each of the eight right-set steps")
    fired = {number: time_s for time_s, number in cycle if number != 10}
    coil_names: dict[str, dict] = {}
    for number, text in {**readings.COIL_READINGS, **readings.FLASHER_READINGS}.items():
        snapshot = [s for t, s in ticks if t >= fired[number] + 0.3][0]
        item = frame_snapshot(f"Cycling Coils, public solenoid {number} fired at {fired[number]:.2f} s", snapshot, f"-CYCLING COILS- | {text}")
        coil_names[str(number)] = {"name": text, "pixel_sha256": item["pixel_sha256"]}
        snapshots.append(item)

    # --- Crane, Magnet and Laser Kick tests --------------------------------------------------------------
    tests = runs["crane-magnet-laser"]
    test_labels = snapshots_by_label(tests)
    for label, text in readings.TEST_READINGS.items():
        snapshots.append(frame_snapshot(label, test_labels[label], text))
    actions: list[dict] = []
    for step in tests["steps"]:
        label = step["label"]
        match = re.match(r"(Crane Test|Magnet Test|Laser Kick Test): (close public switch (\d+)|hold Start)", label)
        if not match or step["type"] != "pulse":
            continue
        number = int(match.group(3) or 3)
        begin, end = step_window(tests, step, 1.0)
        transitions = sorted({
            e["number"] for e in tests["events"]
            if e["event"] == "solenoid" and e["number"] not in LIGHT_SHOW_OUTPUTS and begin <= e["time_s"] <= end
        })
        pulses: dict[str, int] = {}
        for event in tests["events"]:
            if event["event"] == "solenoid" and event["state"] == 1 and event["number"] in transitions and begin <= event["time_s"] <= end:
                pulses[str(event["number"])] = pulses.get(str(event["number"]), 0) + 1
        actions.append({
            "label": label,
            "input_kind": "switch",
            "input_address": number,
            "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": [number],
            "active_solenoid_addresses": [],
            "transitioned_solenoid_addresses": transitions,
            "solenoid_on_counts": pulses,
            "result": "observed" if transitions else "no_matching_transition",
        })
    expected_actions = {
        "Crane Test: close public switch 60": [], "Crane Test: close public switch 61": [],
        "Crane Test: hold Start 3 s": [14], "Crane Test: close public switch 8 (launch trigger)": [4],
        "Crane Test: close public switch 62": [], "Magnet Test: hold Start 2.5 s": [37, 38, 39],
        "Laser Kick Test: close public switch 48 for 400 ms": [22], "Laser Kick Test: close public switch 48 for 1500 ms": [22],
        "Laser Kick Test: close public switch 43 for 400 ms": [], "Laser Kick Test: close public switch 47 for 500 ms": [5],
        "Laser Kick Test: close public switch 31 for 500 ms": [6], "Laser Kick Test: close public switch 57 for 500 ms": [15],
        "Laser Kick Test: close public switch 58 for 500 ms": [], "Laser Kick Test: close public switch 22 for 500 ms": [],
        "Laser Kick Test: close public switch 23 for 500 ms": [], "Laser Kick Test: close public switch 16 for 500 ms": [3],
    }
    if {action["label"]: action["transitioned_solenoid_addresses"] for action in actions} != expected_actions:
        raise SystemExit(f"crane/magnet/laser run: transitions {[(a['label'], a['transitioned_solenoid_addresses']) for a in actions]} differ from the readings")
    magnet_order = [
        e["number"] for e in tests["events"]
        if e["event"] == "solenoid" and e["state"] == 1 and e["number"] in (37, 38, 39)
    ]

    # --- Printer interface (Adjustment 58) ----------------------------------------------------------------
    printer = runs["printer-interface"]
    printer_labels = snapshots_by_label(printer)
    printer_step = [step for step in printer["steps"] if step["label"] == PRINTER_LABEL][0]
    begin, _ = step_window(printer, printer_step, 0.0)
    printer_transitions = sorted({
        e["number"] for e in printer["events"]
        if e["event"] == "solenoid" and e["number"] not in LIGHT_SHOW_OUTPUTS and e["time_s"] >= begin
    })
    transitions_37_44 = sorted({e["number"] for e in printer["events"] if e["event"] == "solenoid" and 37 <= e["number"] <= 44})
    if printer_transitions or transitions_37_44:
        raise SystemExit(f"printer run: expected no output after Start and no transition on 37-44 at all, saw {printer_transitions} and {transitions_37_44}")
    printer_actions = [{
        "label": "Adjustment 58 PRINTER INTERFACE: press Start to print",
        "input_kind": "switch",
        "input_address": 3,
        "observed_switch_addresses": [],
        "host_stimulus_switch_addresses": [3],
        "active_solenoid_addresses": [],
        "transitioned_solenoid_addresses": printer_transitions,
        "result": "no_matching_transition",
    }]
    snapshots.append(frame_snapshot("Adjustment 58 display while Start is held", printer_labels[f"{PRINTER_LABEL} (held)"], PRINTER_TEXT))
    snapshots.append(frame_snapshot("Adjustment 58 display 12 s after Start", printer_labels[PRINTER_LABEL], PRINTER_TEXT))

    # --- Trough serve (game start) ------------------------------------------------------------------------
    trough = runs["trough-serve"]
    trough_snapshots = trough["snapshots"]
    trough_steps = {step["label"]: step for step in trough["steps"]}
    trough_actions: list[dict] = []
    trough_pulses: list[dict] = []
    for previous, snapshot in zip(trough_snapshots, trough_snapshots[1:]):
        step = trough_steps[snapshot["label"]]
        window = [
            e for e in trough["events"]
            if e["event"] == "solenoid" and previous["time_s"] < e["time_s"] <= snapshot["time_s"] and e["number"] not in LIGHT_SHOW_OUTPUTS
        ]
        on_counts: dict[str, int] = {}
        for event in window:
            if event["state"] == 1:
                on_counts[str(event["number"])] = on_counts.get(str(event["number"]), 0) + 1
        trough_pulses.append({"label": snapshot["label"], "solenoid_on_counts": on_counts, "transitioned_solenoids": sorted({e["number"] for e in window})})
        if "switch" in step:
            transitions = sorted({e["number"] for e in window})
            trough_actions.append({
                "label": snapshot["label"],
                "input_kind": "switch",
                "input_address": step["switch"],
                "observed_switch_addresses": [],
                "host_stimulus_switch_addresses": [step["switch"]],
                "active_solenoid_addresses": sorted(snapshot["active_solenoids"]),
                "transitioned_solenoid_addresses": transitions,
                "result": "observed" if transitions else "no_matching_transition",
            })
    expected_trough = {
        "Trough: idle after power-up with balls on 9-14 and 15 empty": {},
        "Trough: coin 1 on the left coin switch": {},
        "Trough: coin 2 on the left coin switch": {},
        "Trough: press Start with 15 empty": {"1": 3, "14": 1, "16": 7},
        "Trough: the position 14 next to the release empties": {},
        "Trough: a ball reaches the release position 15": {"2": 6, "16": 7},
        "Trough: the ball leaves 15": {},
        "Trough: the ball rests in the shooter lane 16": {"16": 6},
        "Trough: pull the launch trigger 8 with the ball on 16": {"3": 1, "16": 1},
        "Trough: the ball leaves the shooter lane": {},
    }
    if {item["label"]: item["solenoid_on_counts"] for item in trough_pulses} != expected_trough:
        raise SystemExit(f"trough run: {[(i['label'], i['solenoid_on_counts']) for i in trough_pulses]} differ from the readings")
    crane_events = [e for e in trough["events"] if e["event"] == "solenoid" and e["number"] == 14]
    crane_motor = [(round(e["time_s"], 2), e["state"]) for e in crane_events]

    def host_switch_time(label: str, number: int, state: int) -> float:
        step = trough_steps[label]["step"]
        (time_s,) = [e["time_s"] for e in trough["events"] if e["event"] == "switch" and e.get("step") == step and e["number"] == number and e["state"] == state]
        return time_s

    start_press = host_switch_time("Trough: press Start with 15 empty", 3, 1)
    shooter_clear = host_switch_time("Trough: the ball leaves the shooter lane", 16, 0)
    if [e["state"] for e in crane_events] != [1, 0, 1, 0] or not crane_events[0]["time_s"] < start_press < crane_events[1]["time_s"] or not shooter_clear < crane_events[3]["time_s"]:
        raise SystemExit(f"trough run: the crane motor levels {crane_motor} differ from the readings (on, off after Start, on, off after the shooter lane clears)")
    crane_timing = {
        "drop_after_start_s": round(crane_events[1]["time_s"] - start_press, 2),
        "dropout_ms": round((crane_events[2]["time_s"] - crane_events[1]["time_s"]) * 1000),
        "off_after_shooter_lane_s": round(crane_events[3]["time_s"] - shooter_clear, 2),
    }
    trigger_step = trough_steps["Trough: pull the launch trigger 8 with the ball on 16"]
    trigger_time = [e["time_s"] for e in trough["events"] if e["event"] == "switch" and e.get("step") == trigger_step["step"] and e["state"] == 1][0]
    launch = [t for t, n in solenoid_on_events(trough, trigger_time) if n == 3][0]

    # --- Captive-ball lamps (game in play) ------------------------------------------------------------------
    captive = runs["captive-lamps"]
    if [step["label"] for step in captive["steps"][:len(trough["steps"])]] != [step["label"] for step in trough["steps"]]:
        raise SystemExit("captive-lamps run: its game start must repeat the trough-serve steps")
    if any(e["event"] == "lamp" and e["number"] == 32 for e in captive["events"]):
        raise SystemExit("captive-lamps run: lamp 32 changed state; the readings say it never does")
    captive_steps = []
    for step in captive["steps"]:
        if not step["label"].startswith("Captive: close"):
            continue
        changed = {item["number"]: len(item["states"]) for item in step["transitions"]["lamps"]}
        captive_steps.append({
            "label": step["label"], "switch": step["switch"],
            "lamp_31_changes": changed.get(31, 0), "lamp_32_changes": changed.get(32, 0),
            "lamps_changed": sorted(changed),
        })
    if [item["switch"] for item in captive_steps] != CAPTIVE_SWITCHES or not all(item["lamp_31_changes"] for item in captive_steps):
        raise SystemExit(f"captive-lamps run: {[(i['switch'], i['lamp_31_changes']) for i in captive_steps]} differ from the readings")

    # Every reading belongs to the exact frame it was read from: refuse a run whose frames changed.
    pinned = readings.READ_FRAME_DIGESTS
    labels = [snapshot["label"] for snapshot in snapshots]
    if len(set(labels)) != len(labels) or set(labels) != set(pinned):
        raise SystemExit("the evidence snapshots and the pinned read frames name different labels")
    for snapshot in snapshots:
        if snapshot["pixel_sha256"] != pinned[snapshot["label"]]:
            raise SystemExit(f"{snapshot['label']}: frame {snapshot['pixel_sha256']} is not the frame that was read ({pinned[snapshot['label']]}); read it again")

    # --- Raw-run records ---------------------------------------------------------------------------------
    raw_runs = []
    per_run: dict[str, dict] = {}
    all_solenoids: set[int] = set()
    for name in RUNS:
        run = runs[name]
        scenario_path = ROOT / f"tools/harness-scenarios/data-east/lah-112-{name}.json"
        scenario_sha = sha256_file(scenario_path)
        retained = (base / name / "scenario.json").read_bytes()
        if hashlib.sha256(retained).hexdigest() != scenario_sha:
            raise SystemExit(f"{name}: retained scenario differs from the committed scenario")
        checkpoints = [
            {"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
            for step in run["steps"] if step["type"] == "pulse_until_display"
        ]
        solenoids = sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"})
        all_solenoids.update(solenoids)
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        raw_runs.append({
            "name": name,
            "sha256": sha256_file(base / name / "run.json"),
            "scenario_path": f"tools/harness-scenarios/data-east/lah-112-{name}.json",
            "scenario_sha256": scenario_sha,
            "action_count": len(scenario["actions"]),
            "watch_switches": scenario["watch_switches"],
            "self_test_pulses": sum(item["after_service_pulses"] for item in checkpoints),
            "nvram_initialization": "new empty isolated state directory; no NVRAM inherited",
            "boot_wait_s": 8.0,
            "snapshot_count": len(run["snapshots"]),
        })
        per_run[name] = {"diagnostic_checkpoints": checkpoints, "solenoid_addresses_seen": solenoids}
    per_run["cycling-coils"]["ordered_solenoid_on_sequence"] = [n for _, n in cycle]

    # Output 23 (game on): its levels where the record cites them, with the boundaries the note is measured from.
    def levels(run: dict, number: int) -> list[dict]:
        return [{"time_s": round(e["time_s"], 2), "state": e["state"]} for e in run["events"] if e["event"] == "solenoid" and e["number"] == number]

    game_on = {"active-switches": {"levels": levels(active, 23), "test_entry_s": round(baseline["time_s"], 2)}}
    if 23 in baseline["active_solenoids"]:
        raise SystemExit("active-switches: output 23 is on in the Active Switch Test entry frame")
    if [level["state"] for level in game_on["active-switches"]["levels"] if level["time_s"] > game_on["active-switches"]["test_entry_s"]] != [1]:
        raise SystemExit("active-switches: output 23 must come on once after the test entry frame and stay on")
    on_raw = [e["time_s"] for e in active["events"] if e["event"] == "solenoid" and e["number"] == 23 and e["state"] == 1 and e["time_s"] > baseline["time_s"]][0]
    if any(23 not in s["active_solenoids"] for s in active["snapshots"] if s["time_s"] > on_raw):
        raise SystemExit("active-switches: output 23 is off in a later Active Switch Test snapshot")
    for name in ("trough-serve", "captive-lamps"):
        lane = [e["time_s"] for e in runs[name]["events"] if e["event"] == "switch" and e["number"] == 16 and e["state"] == 1][0]
        game_on[name] = {"levels": levels(runs[name], 23), "shooter_lane_16_set_s": round(lane, 2)}
        if [level["state"] for level in game_on[name]["levels"]] != [1] or game_on[name]["levels"][0]["time_s"] <= lane:
            raise SystemExit(f"{name}: output 23 must come on once, after the shooter lane 16 is set, and stay on")
    def level_text(values: list[dict]) -> str:
        return ", ".join(f"{'on' if level['state'] else 'off'} at {level['time_s']:.2f} s" for level in values)

    game_on_text = {
        "active-switches": (
            f"Output 23 (game on) by host time: {level_text(game_on['active-switches']['levels'])}; the Active Switch Test entry frame, the baseline NONE "
            f"frame, is at {game_on['active-switches']['test_entry_s']:.2f} s, and every later snapshot shows 23 on."
        ),
        **{
            name: (
                f"Output 23 (game on) came on once, at {game_on[name]['levels'][0]['time_s']:.2f} s, after the run set the shooter-lane switch 16 at "
                f"{game_on[name]['shooter_lane_16_set_s']:.2f} s, and stayed on."
            )
            for name in ("trough-serve", "captive-lamps")
        },
    }
    per_run["crane-magnet-laser"]["named_action_observations"] = [
        {key: value for key, value in action.items() if key != "solenoid_on_counts"} for action in actions
    ]
    per_run["crane-magnet-laser"]["note"] = (
        "Each action's window runs from the stimulus switch closing to 1 s after it opens, cut at the next switch write, and excludes the outputs "
        "the lamp show drives by itself (9, 10, 11, 23 and 25-32). Outputs switched on per action: "
        + "; ".join(f"{action['label']}: {counts_text(action['solenoid_on_counts'])}" for action in actions)
        + ". During the Magnet Test the ROM switched the magnets on in the order " + ", ".join(str(number) for number in magnet_order) + "."
    )
    per_run["printer-interface"]["named_action_observations"] = printer_actions
    per_run["printer-interface"]["note"] = (
        "Fixed Black presses walk from attract into the audits and backwards past Adjustment 99 FACTORY RESTORE to Adjustment 58 PRINTER INTERFACE "
        "('PRESS START TO PRINT'). A 300 ms Start press there changed no output in the following 12 s, and no address from 37 to 44 moved at any time in the run."
    )
    per_run["captive-lamps"]["note"] = (
        "The game start repeats the trough-serve run's steps; then, with the ball in play, each stimulus closes for 60 ms and the run waits 4 s. "
        "Lamp 32 never changed state in the whole run, attract mode included. Lamp state changes per stimulus (lamp 31 count; every lamp that changed): "
        + "; ".join(f"{item['label']}: 31 changed {item['lamp_31_changes']} times; {', '.join(str(n) for n in item['lamps_changed'])}" for item in captive_steps)
        + "."
    )
    per_run["trough-serve"]["named_action_observations"] = trough_actions
    per_run["trough-serve"]["ordered_solenoid_on_sequence"] = [
        e["number"] for e in trough["events"] if e["event"] == "solenoid" and e["state"] == 1 and e["number"] not in LIGHT_SHOW_OUTPUTS
    ]
    per_run["trough-serve"]["note"] = (
        "Transitions exclude the outputs the attract and game-start lamp shows drive by themselves (9, 10, 11, 23 and 25-32). Neither crane limit switch "
        "(60, 61) was ever closed: the crane motor (14) came on during power-up, dropped "
        f"{crane_timing['drop_after_start_s']:.2f} s after the Start press for {crane_timing['dropout_ms']} ms, and ran again until "
        f"{crane_timing['off_after_shooter_lane_s']:.2f} s after the ball left the shooter lane (14 levels by host time: "
        + ", ".join(f"{'on' if state else 'off'} at {time:.2f} s" for time, state in crane_motor)
        + f"). The auto-launch coil (3) fired {launch - trigger_time:.2f} s after the launch trigger (8) closed. Outputs switched on between one "
        "action's snapshot and the next: "
        + "; ".join(f"{item['label']}: {counts_text(item['solenoid_on_counts'])}" for item in trough_pulses)
        + "."
    )
    for name, text in game_on_text.items():
        per_run[name]["note"] = f"{per_run[name]['note']} {text}" if "note" in per_run[name] else text

    # Regeneration writes the external manifest; --check only verifies it and never touches the retained runs.
    manifest_digest = manifest.write_manifest(base, GAME) if write_manifest else manifest.check_manifest(base, GAME)
    runtime_facts = {
        "format": "pinmame-lah-runtime-facts",
        "version": 1,
        "source": "evidence/runtime/data-east/last-action-hero-lah_112-service-tests.json",
        "rom_switch_names": switch_names,
        "rom_lamp_names": lamp_names,
        "rom_coil_names": coil_names,
        "test_actions": [
            {"label": a["label"], "switch": a["input_address"], "outputs": a["transitioned_solenoid_addresses"], "on_counts": a["solenoid_on_counts"]}
            for a in actions
        ],
        "magnet_test_on_sequence": magnet_order,
        "printer_interface": {"label": printer_actions[0]["label"], "transitioned_solenoids": printer_transitions, "transitions_37_44": transitions_37_44},
        "trough_serve": trough_pulses,
        "crane_motor_levels": [{"time_s": t, "state": s} for t, s in crane_motor],
        "crane_motor_timing": crane_timing,
        "drive_9_relay_10": drive_9_relay_10,
        "cycling_left_coil_relay_overlap": relay_overlap,
        "launch_delay_s": round(launch - trigger_time, 2),
        "game_on_23": game_on,
        "captive_lamps": captive_steps,
    }
    evidence = {
        "driver_ids": [GAME],
        "extractor": {"id": "tools/build_lah_runtime_evidence.py", "version": 1},
        "format": "pinmame-machine-evidence",
        "machine_ids": [KEY],
        "mechanisms": [],
        "outputs": [],
        "recreation_notes": [],
        "runtime": {
            "game": GAME,
            "rom_archive_sha256": ROM_ARCHIVE_SHA256,
            "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
            "raw_runs": raw_runs,
            "command_template": (
                f"python tools/lah_harness.py --library <libpinmame> --game {GAME} --rom-path <read-only-rom-root> --work-dir <new-isolated-state> "
                "--scenario tools/harness-scenarios/data-east/lah-112-<run>.json --boot-wait 8 --dmd-dir <external-dmd-dir> --output <external-run.json>. "
                "No keyboard handling: every stimulus is a direct public switch write (the Black Advance button at -7, the Green input at -6, then "
                "playfield and cabinet addresses). tools/lah_harness.py replaces only the display-title checkpoint with exact title-band matches of "
                "visually read retained frames (tools/lah_header_templates.json). Each DMD reading in diagnostic_snapshots was read by a curator from "
                "the retained 128x32 frame whose pixel digest is recorded beside it."
            ),
            "observations": {
                "service_language": "US English 1.12",
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
    return evidence, runtime_facts


def _bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-artifacts-root", type=Path, default=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"))
    parser.add_argument("--rom-archive", type=Path, default=ROM_ARCHIVE)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Rebuild both committed files and the external manifest from the retained runs.")
    mode.add_argument("--check", action="store_true", help="Rebuild and refuse any difference from the committed files; the external manifest is only verified.")
    args = parser.parse_args()
    if not args.review_artifacts_root:
        raise SystemExit("PINMAME_REVIEW_ARTIFACTS_ROOT must point at the working root's review-artifacts directory")
    if args.rom_archive.is_file() and sha256_file(args.rom_archive) != ROM_ARCHIVE_SHA256:
        raise SystemExit(f"{args.rom_archive} is not the ROM archive the runs used")
    base = Path(args.review_artifacts_root) / SESSION
    evidence, facts = build(base, write_manifest=args.write)
    outputs = ((EVIDENCE_PATH, _bytes(evidence)), (RUNTIME_PATH, _bytes(facts)))
    if args.check:
        for path, payload in outputs:
            if not path.is_file() or path.read_bytes() != payload:
                raise SystemExit(f"{path} differs from the retained runs")
        print("Last Action Hero runtime evidence matches the retained runs.")
        return
    for path, payload in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    print(f"{len(evidence['runtime']['observations']['diagnostic_snapshots'])} diagnostic snapshots; manifest {evidence['source']['sha256']}")


if __name__ == "__main__":
    main()
