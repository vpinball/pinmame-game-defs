"""Build the committed Tales from the Crypt runtime evidence from the retained harness runs.

Reads the four retained raw runs of the US 3.03 service tests (``PINMAME_REVIEW_ARTIFACTS_ROOT``), pairs
the curator's visual DMD readings (``tftc_readings``) with each frame's pixel digest, derives the
switch-to-coil observations, and writes two committed files:

* ``evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json``, a
  ``pinmame-machine-evidence`` bundle, and
* ``tools/tales_from_the_crypt_runtime.json``, the compact facts the curator consumes.

The raw runs, DMD frames and isolated state directories stay external under the working root, covered by a
canonical manifest (``tools/build_external_evidence_manifest.py``).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import build_external_evidence_manifest as manifest
import tftc_manual
import tftc_readings as readings

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.tales-from-the-crypt.1993"
SESSION = "data-east.tales-from-the-crypt.1993/session-20261002/final/tftc_303"
EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json"
RUNTIME_PATH = ROOT / "tools/tales_from_the_crypt_runtime.json"
RUNS = ("active-switches", "lamp-test", "cycling-coils", "laser-tombstone", "printer-interface")
PINMAME_REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
ROM_ARCHIVE = Path("L:/Visual Pinball/VPinMAME/roms/tftc_303.zip")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_run(base: Path, name: str) -> dict:
    return json.loads((base / name / "run.json").read_text(encoding="utf-8"))


def snapshots_by_label(run: dict) -> dict[str, dict]:
    return {snapshot["label"]: snapshot for snapshot in run["snapshots"]}


def display(snapshot: dict) -> dict:
    (frame,) = [item for item in snapshot["displays"] if item.get("pixel_sha256")]
    return frame


def solenoid_on_events(run: dict, lower: float = 0.0, upper: float = 1e9) -> list[tuple[float, int]]:
    return [
        (event["time_s"], event["number"])
        for event in run["events"]
        if event["event"] == "solenoid" and event["state"] == 1 and lower <= event["time_s"] < upper
    ]


def build(base: Path, rom_archive: Path) -> tuple[dict, dict]:
    runs = {name: load_run(base, name) for name in RUNS}
    switch_chart = tftc_manual.switch_data()["chart"]
    lamp_chart = tftc_manual.lamp_data()["chart"]
    snapshots: list[dict] = []

    # --- Active Switch Test ------------------------------------------------------------------------------
    active = runs["active-switches"]
    by_label = snapshots_by_label(active)
    baseline = [s for s in active["snapshots"] if s["label"].startswith("advance with the Black")][0]
    switch_names: dict[str, dict] = {}
    for address in list(range(1, 65)):
        name, column_wire, row_wire = readings.SWITCH_READINGS[address]
        chart = switch_chart[address]
        if (column_wire, row_wire) != (chart["drive"]["wire"], chart["return"]["wire"]):
            raise SystemExit(f"switch {address}: ROM wires {column_wire} {row_wire} disagree with the manual chart")
        frame = display(by_label[f"hold public switch {address} (held)"])
        switch_names[str(address)] = {"name": name, "wires": f"{column_wire} {row_wire}", "pixel_sha256": frame["pixel_sha256"]}
        snapshots.append({
            "label": f"Active Switch Test, public switch {address} held 900 ms",
            "display_index": 0,
            "pixel_sha256": frame["pixel_sha256"],
            "nonzero_pixels": frame["nonzero_pixels"],
            "interpreted_text": f"-ACTIVE SWITCH TEST- | {name} | {column_wire} {row_wire} #{address:02d}",
            "active_solenoid_addresses": by_label[f"hold public switch {address} (held)"]["active_solenoids"],
        })
    for address, reading in readings.FLIPPER_COLUMN_READINGS.items():
        frame = display(by_label[f"hold public switch {address} (held)"])
        text = "-ACTIVE SWITCH TEST- | NONE" if reading is None else f"-ACTIVE SWITCH TEST- | {reading[1]} #{reading[0]}"
        snapshots.append({
            "label": f"Active Switch Test, flipper-column public switch {address} held 900 ms",
            "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
            "interpreted_text": text, "active_solenoid_addresses": by_label[f"hold public switch {address} (held)"]["active_solenoids"],
        })
    base_frame = display(baseline)
    snapshots.insert(0, {
        "label": "Active Switch Test baseline, every public switch at 0",
        "display_index": 0, "pixel_sha256": base_frame["pixel_sha256"], "nonzero_pixels": base_frame["nonzero_pixels"],
        "interpreted_text": "-ACTIVE SWITCH TEST- | NONE", "active_solenoid_addresses": baseline["active_solenoids"],
    })

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
        if (column_wire, row_wire) != (chart["drive"]["wire"], chart["return"]["wire"]):
            raise SystemExit(f"lamp {address}: ROM wires {column_wire} {row_wire} disagree with the manual chart")
        frame = display(snapshot)
        lamp_names[str(address)] = {"name": name, "wires": f"{column_wire} {row_wire}", "pixel_sha256": frame["pixel_sha256"]}
        snapshots.append({
            "label": f"Lamp Test, Start press {press}, lamp {address} lit",
            "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
            "interpreted_text": f"-LAMP TEST- | {name} | {column_wire} {row_wire} #{address:02d}",
            "active_solenoid_addresses": snapshot["active_solenoids"],
        })

    # --- Cycling Coils -----------------------------------------------------------------------------------
    coil_run = runs["cycling-coils"]
    ticks = [(s["time_s"], s) for s in coil_run["snapshots"] if s["label"].startswith("cycling coils tick")]
    ons = solenoid_on_events(coil_run)
    start = [t for t, n in ons if n == 1 and t > 40][0]
    cycle: list[tuple[float, int]] = []
    for time_s, number in ons:
        if time_s < start - 0.001:
            continue
        if number == 1 and cycle:
            break
        cycle.append((time_s, number))
    order = [n for _, n in cycle if n != 10]
    expected = list(range(1, 10)) + list(range(11, 23))
    coil_sequence = [n for n in order if n < 25]
    flash_sequence = [n for n in order if n >= 25]
    if coil_sequence != expected or flash_sequence != list(range(25, 33)):
        raise SystemExit(f"unexpected cycling order: {order}")
    fired = {number: time_s for time_s, number in cycle if number != 10}
    coil_names: dict[str, dict] = {}
    for number, text in {**readings.COIL_READINGS, **readings.FLASHER_READINGS}.items():
        later = [s for t, s in ticks if t >= fired[number] + 0.3]
        snapshot = later[0]
        frame = display(snapshot)
        title = "-CYCLING COILS-"
        coil_names[str(number)] = {"name": text, "pixel_sha256": frame["pixel_sha256"]}
        snapshots.append({
            "label": f"Cycling Coils, public solenoid {number} fired at {fired[number]:.2f} s",
            "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
            "interpreted_text": f"{title} | {text}", "active_solenoid_addresses": snapshot["active_solenoids"],
        })

    # --- Laser Kick and Tombstone tests --------------------------------------------------------------------
    laser = runs["laser-tombstone"]
    actions: list[dict] = []
    for step in laser["steps"]:
        label = step["label"]
        match = re.match(r"(Laser Kick Test|Tombstone Test): (close public switch (\d+) for (\d+) ms|hold Start 2.5 s|close public switch (\d+))", label)
        if not match:
            continue
        number = int(match.group(3) or match.group(5) or 3)
        begin = [e for e in laser["events"] if e["event"] == "switch" and e.get("step") == step["step"] and e["state"] == 1][0]["time_s"]
        end = [e for e in laser["events"] if e["event"] == "switch" and e.get("step") == step["step"] and e["state"] == 0][0]["time_s"]
        transitions = sorted({
            e["number"] for e in laser["events"]
            if e["event"] == "solenoid" and e["number"] != 23 and begin <= e["time_s"] <= end + 1.0
        })
        actions.append({
            "label": label,
            "input_kind": "switch",
            "input_address": number,
            "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": [number],
            "active_solenoid_addresses": [],
            "transitioned_solenoid_addresses": transitions,
            "result": "observed" if transitions else "no_matching_transition",
        })
        held = snapshots_by_label(laser).get(f"{label} (held)")
        if held is not None:
            frame = display(held)
            snapshots.append({
                "label": label + " (display at the end of the hold)",
                "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
                "interpreted_text": TOMBSTONE_READINGS.get(label, "-LASER KICK TEST- | >PUT BALL IN KICKER<"),
                "active_solenoid_addresses": held["active_solenoids"],
            })

    # --- Printer interface (Adjustment 61) ---------------------------------------------------------------------
    printer = runs["printer-interface"]
    printer_step = [step for step in printer["steps"] if step["label"] == "Adjustment 61: press Start to print"][0]
    begin = [e for e in printer["events"] if e["event"] == "switch" and e.get("step") == printer_step["step"] and e["state"] == 1][0]["time_s"]
    end = [e for e in printer["events"] if e["event"] == "switch" and e.get("step") == printer_step["step"] and e["state"] == 0][0]["time_s"]
    printer_transitions = sorted({
        e["number"] for e in printer["events"]
        if e["event"] == "solenoid" and e["number"] != 23 and begin <= e["time_s"] <= end + 12.0
    })
    printer_levels = sorted({(e["number"], e["state"]) for e in printer["events"] if e["event"] == "solenoid" and e["number"] >= 37 and begin <= e["time_s"]})
    printer_actions = [{
        "label": "Adjustment 61: press Start to print",
        "input_kind": "switch",
        "input_address": 3,
        "observed_switch_addresses": [],
        "host_stimulus_switch_addresses": [3],
        "active_solenoid_addresses": [number for number, state in printer_levels if state],
        "transitioned_solenoid_addresses": printer_transitions,
        "result": "observed" if printer_transitions else "no_matching_transition",
    }]
    printer_held = snapshots_by_label(printer)["Adjustment 61: press Start to print (held)"]
    frame = display(printer_held)
    snapshots.append({
        "label": "Adjustment 61 display while Start is held",
        "display_index": 0, "pixel_sha256": frame["pixel_sha256"], "nonzero_pixels": frame["nonzero_pixels"],
        "interpreted_text": "-ADJUSTMENT- | 61 | PRINTER INTERFACE | PRESS START TO PRINT",
        "active_solenoid_addresses": printer_held["active_solenoids"],
    })

    # --- Raw-run records ---------------------------------------------------------------------------------
    raw_runs = []
    per_run: dict[str, dict] = {}
    all_solenoids: set[int] = set()
    for name in RUNS:
        run = runs[name]
        scenario_path = ROOT / f"tools/harness-scenarios/data-east/tftc-303-{name}.json"
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
            "scenario_path": f"tools/harness-scenarios/data-east/tftc-303-{name}.json",
            "scenario_sha256": scenario_sha,
            "action_count": len(scenario["actions"]),
            "watch_switches": scenario["watch_switches"],
            "self_test_pulses": sum(item["after_service_pulses"] for item in checkpoints),
            "nvram_initialization": "new empty isolated state directory; no NVRAM inherited",
            "boot_wait_s": 8.0,
            "snapshot_count": len(run["snapshots"]),
        })
        per_run[name] = {
            "diagnostic_checkpoints": checkpoints,
            "solenoid_addresses_seen": solenoids,
        }
    per_run["cycling-coils"]["ordered_solenoid_on_sequence"] = [n for _, n in cycle]
    per_run["laser-tombstone"]["named_action_observations"] = actions
    per_run["printer-interface"]["named_action_observations"] = printer_actions

    external = base
    manifest_digest = manifest.write_manifest(external, "tftc_303")
    runtime_facts = {
        "format": "pinmame-tftc-runtime-facts",
        "version": 1,
        "source": "evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json",
        "rom_switch_names": switch_names,
        "rom_lamp_names": lamp_names,
        "rom_coil_names": coil_names,
        "printer_interface": {"transitioned_solenoids": printer_transitions, "label": "Adjustment 61: press Start to print"},
        "causal_pairs": [
            {"switch": action["input_address"], "coils": action["transitioned_solenoid_addresses"], "label": action["label"]}
            for action in actions
        ],
    }
    evidence = {
        "driver_ids": ["tftc_303"],
        "extractor": {"id": "tools/build_tftc_runtime_evidence.py", "version": 1},
        "format": "pinmame-machine-evidence",
        "machine_ids": [KEY],
        "mechanisms": [],
        "outputs": [],
        "recreation_notes": [],
        "runtime": {
            "game": "tftc_303",
            "rom_archive_sha256": sha256_file(rom_archive),
            "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA256, "built_from_revision": PINMAME_REVISION},
            "raw_runs": raw_runs,
            "command_template": (
                "python tools/tftc_harness.py --library <libpinmame> --game tftc_303 --rom-path <read-only-rom-root> --work-dir <new-isolated-state> "
                "--scenario tools/harness-scenarios/data-east/tftc-303-<run>.json --boot-wait 8 --dmd-dir <external-dmd-dir> --output <external-run.json>. "
                "No keyboard handling: every stimulus is a direct public switch write (the Black Advance button at -7, the Green input at -6, then "
                "playfield and cabinet addresses). tools/tftc_harness.py replaces only the display-title checkpoint with exact title-band matches of "
                "visually read retained frames (tools/tftc_header_templates.json). Each DMD reading in diagnostic_snapshots was read by a curator from "
                "the retained 128x32 frame whose pixel digest is recorded beside it."
            ),
            "observations": {
                "service_language": "US English 3.03",
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


TOMBSTONE_READINGS = {
    "Tombstone Test: hold Start 2.5 s": 'TOMBSTONE TEST | PRESS START BUTTON | "UP" SWITCH OFF | "DOWN" SWITCH OFF | TARGET SWITCH OFF',
    "Tombstone Test: close public switch 33": 'TOMBSTONE TEST | PRESS START BUTTON | "UP" SWITCH ON | "DOWN" SWITCH OFF | TARGET SWITCH OFF',
    "Tombstone Test: close public switch 36": 'TOMBSTONE TEST | PRESS START BUTTON | "UP" SWITCH OFF | "DOWN" SWITCH ON | TARGET SWITCH OFF',
    "Tombstone Test: close public switch 37": 'TOMBSTONE TEST | PRESS START BUTTON | "UP" SWITCH OFF | "DOWN" SWITCH OFF | TARGET SWITCH ON',
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-artifacts-root", type=Path, default=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"))
    parser.add_argument("--rom-archive", type=Path, default=ROM_ARCHIVE)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    base = Path(args.review_artifacts_root) / SESSION
    evidence, facts = build(base, args.rom_archive)
    if args.write:
        EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE_PATH.write_bytes((json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
        RUNTIME_PATH.write_bytes((json.dumps(facts, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
    print(f"{len(evidence['runtime']['observations']['diagnostic_snapshots'])} diagnostic snapshots; manifest {evidence['source']['sha256']}")


if __name__ == "__main__":
    main()
