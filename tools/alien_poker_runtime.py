"""Reduce retained production ROM traces without treating host input readback as evidence."""
from __future__ import annotations

from pathlib import Path

from pinmame_game_defs.jsonio import load_json

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/seeds/williams/alien-poker-1980-runtime.json"
DATA = ROOT / "tools/seeds/williams/alien-poker-1980-evidence.json"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DIGITS = {0: " ", 63: "0", 6: "1", 91: "2", 79: "3", 102: "4", 109: "5", 125: "6", 7: "7", 127: "8", 111: "9"}


def display_text(snapshot: dict, indices: tuple[int, ...]) -> str:
    displays = {d["index"]: d for d in snapshot["displays"]}
    return "".join(DIGITS[v & 127] for index in indices for v in displays[index]["segments"])


def runtime_evidence(directory: Path | None = None) -> dict:
    if directory is None:
        return load_json(SEED)
    pinned = load_json(DATA)
    runs = {}
    raw_runs = []
    for name in ("solenoid", "switch", "gameplay"):
        for phase in ("init", "run"):
            filename = f"{name}-{phase}.json"
            raw = load_json(directory / filename)
            if raw["failure"] is not None:
                raise RuntimeError(f"Cannot use failed runtime trace: {filename}")
            scenario = "init-scenario.json" if phase == "init" else f"{name}-scenario.json"
            raw_runs.append({
                "name": filename,
                "sha256": pinned["runtime_files"][filename]["sha256"],
                "scenario_path": f"external:pinmame-review-artifacts/williams.alien-poker.1980/runtime/{scenario}",
                "scenario_sha256": pinned["runtime_files"][scenario]["sha256"],
                "self_test_pulses": sum(step.get("switch") == -7 and step["type"] == "pulse" for step in raw["steps"]),
                "action_count": len(raw["steps"]),
                "snapshot_count": len(raw["snapshots"]),
                "watch_switches": raw["watch_switches"],
                "nvram_initialization": "New isolated state, one 20-second empty-NVRAM boot." if phase == "init" else
                f"Only the state produced by retained {name}-init.json, SHA256 {pinned['runtime_files'][f'{name}-init.json']['sha256']}; no exploratory NVRAM."
            })
        runs[name] = raw
    solenoid = runs["solenoid"]
    selectors = []
    for snapshot in solenoid["snapshots"]:
        if snapshot["label"] == "Advance: Test 02, solenoid 01" or snapshot["label"] == "Advance: next solenoid":
            selectors.append(int(display_text(snapshot, (4, 5))))
            if display_text(snapshot, (6, 7)) != "02":
                raise RuntimeError("Coil-test credit display checkpoint differs")
    if selectors != list(range(1, 23)) + [1]:
        raise RuntimeError("ROM coil selectors no longer cover 01-22 and wrap")
    switch = runs["switch"]
    responses = []
    for snapshot in switch["snapshots"]:
        label = snapshot["label"]
        if "close public switch " not in label or not label.endswith("(held)"):
            continue
        number = int(label.split("close public switch ", 1)[1].split(" ", 1)[0])
        if number > 42:
            continue  # repeated host 43 pulses/stale 43 displays are not contact evidence
        if int(display_text(snapshot, (4, 5))) != number or display_text(snapshot, (6, 7)) != "03":
            raise RuntimeError(f"ROM switch-test response differs at {number}")
        responses.append({
            "label": f"Test 03 contact {number}",
            "input_kind": "switch",
            "input_address": number,
            "host_stimulus_switch_addresses": [number],
            "observed_switch_addresses": [],
            "result": "observed",
            "display_responses": [{
                "snapshot_label": label,
                "display_index": index,
                "segments": snapshot["displays"][index]["segments"],
                "decoded_segment_positions": [0],
                "interpreted_text": display_text(snapshot, (index, ))
            } for index in (4, 5, 6, 7)]
        })
    if [row["input_address"] for row in responses] != list(range(1, 43)):
        raise RuntimeError("Fitted switch-test response set is incomplete")
    gameplay = runs["gameplay"]
    actions = []
    labels = [f"isolated switch {n}"
              for n in (35, 37, 36, 38, 13, 15, 22, 29)] + [f"hold flipper button {n}" for n in (82, 84)]
    for label in labels:
        step = next(s for s in gameplay["steps"] if s.get("label") == label)
        number = step["switch"]
        snapshots = [s for s in gameplay["snapshots"] if s["label"] == label]
        snapshot = snapshots[-1]
        transitions = sorted(row["number"] for row in step["transitions"]["solenoids"] if any(row["states"]))
        actions.append({
            "label": label,
            "input_kind": "switch",
            "input_address": number,
            "host_stimulus_switch_addresses": [number],
            "observed_switch_addresses": [43] if number == 82 else [],
            "active_solenoid_addresses": snapshot["active_solenoids"],
            "transitioned_solenoid_addresses": transitions,
            "result": "observed"
        })
        if number == 82 and next(s["state"] for s in snapshot["watched_switches"] if s["number"] == 43) != 1:
            raise RuntimeError("Single-write right button no longer supplies copied 43")
    for number, output in [(35, 17), (37, 18), (36, 19), (38, 20), (13, 22), (15, 2), (22, 15), (29, 3)]:
        row = next(a for a in actions if a["input_address"] == number)
        if output not in row["transitioned_solenoid_addresses"]:
            raise RuntimeError(f"Missing gameplay response {number}->{output}")
    for number, outputs in [(82, {45, 46}), (84, {47, 48})]:
        if not outputs.issubset(next(a for a in actions if a["input_address"] == number)["active_solenoid_addresses"]):
            raise RuntimeError("Missing held synthetic flipper pair")
    snapshots = {s["label"]: s for s in gameplay["snapshots"]}
    if display_text(snapshots["right coin"],
                    (6, 7)) != "03" or display_text(snapshots["start"],
                                                    (6, 7)) != "02" or int(display_text(snapshots["start"],
                                                                                        (4, 5))) != 1:
        raise RuntimeError("Gameplay credit/ball display roles changed")
    return {
        "format": "pinmame-machine-evidence",
        "version": 1,
        "extractor": {
            "id": "tools/alien_poker_runtime.py",
            "version": 1
        },
        "source": {
            "kind": "runtime_scenario",
            "repository": "https://github.com/vpinball/pinmame",
            "revision": REVISION,
            "path": "external:pinmame-review-artifacts/williams.alien-poker.1980/runtime",
            "sha256": pinned["runtime_manifest"]["sha256"],
            "manifest_algorithm": "tools/build_external_evidence_manifest.py compact sorted-key UTF8 JSON plus LF; sorted relative POSIX paths, sizes and SHA256; root manifest files excluded",
            "license": "MIT",
            "attribution": "PinMAME contributors and game-definition curators",
            "quality": "observed"
        },
        "driver_ids": ["alpok_l6"],
        "machine_ids": ["williams.alien-poker.1980"],
        "switches": [],
        "outputs": [],
        "states": [],
        "mechanisms": [],
        "recreation_notes": [],
        "runtime": {
            "emulator": {
                "binary": "builds/pinmame-46e1a01a/Release/pinmame64.dll",
                "built_from_revision": REVISION,
                "sha256": "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
            },
            "game": "alpok_l6",
            "rom_archive_sha256": pinned["rom"]["archive_sha256"],
            "raw_runs": raw_runs,
            "command_template": "python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game alpok_l6 --rom-path <authorized-read-only-rom-root> --work-dir <review-root>/williams.alien-poker.1980/runtime/<name>-state --scenario <scenario.json> --output <run.json>",
            "observations": {
                "runs": {
                    "solenoid": {
                        "ordered_solenoid_on_sequence": selectors,
                        "note": "Displayed selectors at indices 4/5, Test 02 at 6/7. Pulses are retained in raw steps; display number alone is not physical fitment."
                    },
                    "switch": {
                        "named_action_observations": responses,
                        "limitation": "Host states excluded from observed switches. Repeated 43 host pulses and stale 43 for 44-64 do not establish driveability/fitment."
                    },
                    "gameplay": {
                        "named_action_observations": actions,
                        "note": "First bumper step overlaps startup resets; only the matching special response is attributed to its closure. Credits 6/7 increment on coin and decrement on Start; ball 4/5 becomes 1 with a blank tens digit."
                    }
                }
            }
        }
    }
