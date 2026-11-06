"""Recompute compact WWF observations from immutable, externally retained traces.

No emulator or network call is made. Each game has its own evidence envelope;
run names scope every observation. Counts and transitions come from raw data,
not from a manually entered summary. Host writes are never ROM switch evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.wwf-royal-rumble.1994"
SESSION = Path(KEY) / "session-20261106"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
RUNS = {
    "wwfr_106": ["106-switches-held", "106-focused", "106-lamps", "106-coils", "106-selector", "106-printer", "106-dip1-printer", "106-gameplay-v3"],
    "wwfr_103": ["103-switches-held", "103-focused", "103-lamps", "103-coils", "103-printer", "103-gameplay-v3"],
    "wwfr_103f": ["french-switches-held", "french-lamps", "french-coils", "french-gameplay-v3", "french-gameplay-v4"],
}
ROM_HASHES = {
    "wwfr_106": "a9a9334c59e938e59f351faab804b9c12b55a6bed28371350265bbea58e382b6",
    "wwfr_103": "9dfcdad2cb0a7c4aa84376e3cded19e8e0281bc4c0f51b96fb27ef07ce7e4250",
    "wwfr_103f": "efc2f45546e535d94e4e32aa550ef7196c2ad0f8cb87654efc3e0c3c5e679d58",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build(review_root, game):
    base = Path(review_root) / SESSION
    records, observations, readings = [], {}, []
    library_hash = None
    for name in RUNS[game]:
        path = base / "harness" / f"{name}.json"
        run = read(path)
        if run["game"] != game or run["failure"] is not None:
            raise ValueError(f"Wrong game or failed run: {path}")
        if library_hash is not None and library_hash != run["library_sha256"]:
            raise ValueError("Mixed native libraries")
        library_hash = run["library_sha256"]
        # Retained raw paths are immutable. Resolve the same filename below the
        # caller's evidence root so a relocated archive remains verifiable.
        scenario = base / Path(run["scenario"]["path"].replace("\\", "/")).name
        scenario_data = read(scenario)
        service_pulses = sum(step.get("pulses", 0) if step["type"] == "pulse_until_display" else 1
                             for step in run["steps"] if step.get("switch") == -7 and step["type"] in ("pulse", "pulse_until_display"))
        records.append({"name": name, "sha256": sha(path),
                        "retained_from": (SESSION / "harness" / path.name).as_posix(),
                        "scenario_path": (SESSION / scenario.name).as_posix(),
                        "scenario_sha256": sha(scenario), "action_count": len(scenario_data["actions"]),
                        "self_test_pulses": service_pulses, "snapshot_count": len(run["snapshots"]),
                        "initial_switches": run["initial_switches"],
                        "boot_wait_s": 15, "nvram_initialization": "Fresh isolated state directory; no inherited NVRAM."})
        sequence = [event["number"] for event in run["events"] if event["event"] == "solenoid" and event["state"]]
        item = {"solenoid_addresses_seen": sorted(set(sequence)),
                "diagnostic_checkpoints": [{"matched_text": step["matched_text"], "after_service_pulses": step["pulses"]}
                                           for step in run["steps"] if step.get("matched_text")],
                "ordered_solenoid_on_sequence": sequence,
                "note": "Counts include navigation. Host-written switch readback is not an emulator observation."}
        if "gameplay-v" in name:
            item["named_action_observations"] = []
            for step in run["steps"]:
                if not step.get("label", "").startswith("isolated-") or step.get("type") != "pulse":
                    continue
                numbers = sorted(t["number"] for t in step["transitions"]["solenoids"] if 1 in t["states"])
                item["named_action_observations"].append({"label": step["label"], "input_kind": "switch",
                    "input_address": step["switch"], "host_stimulus_switch_addresses": [step["switch"]],
                    "observed_switch_addresses": [], "transitioned_solenoid_addresses": numbers,
                    "result": "observed" if numbers else "no_matching_transition"})
        if "printer" in name:
            item["limitation"] = "Reached actual adjustment 53, pressed Start and waited. No 37–44 transition; absence does not prove unused. DIP=1 successor is a raw configuration stimulus without physical jumper identity."
        if "lamps" in name:
            item["note"] += " The immutable action label 'Forward lamp stepping' is mistaken: Green=0 steps downward, with wraparound. All 64 public lamp addresses are exercised."
        if name == "french-gameplay-v3":
            item["limitation"] = "Two coin pulses did not establish a credit with French defaults; attract screens persisted. This run proves no play-mode causal response. A ten-coin successor is retained separately."
        transcriptions = {}
        if name == "106-focused":
            transcriptions = {"focused-switch-40 (held)": "ACTIVE SWITCH TEST | START MODE (SCOOP) #40",
                              "focused-switch-41 (held)": "ACTIVE SWITCH TEST | LEFT RAMP ENTER #41",
                              "focused-switch-62 (held)": "ACTIVE SWITCH TEST | TAG BUTTON #62"}
        elif name == "106-selector":
            transcriptions = {f"selector-{index}-sample-3": f"COIL TEST | {label} #{number:02}"
                              for index, number, label in [(24,17,"LEFT TURBO"),(25,18,"BOTTOM TURBO"),
                                  (26,19,"RIGHT TURBO"),(27,20,"LEFT SLING"),(28,21,"RIGHT SLING"),(29,22,"EXIT DIVERTER")]}
        elif name in ("106-printer", "103-printer"):
            transcriptions = {"Find actual Adjustment53 printer title": "ADJUSTMENT 53 | PRINTER INTERFACE | PRESS START TO PRINT"}
        for label, text in transcriptions.items():
            snapshot = next(x for x in run["snapshots"] if x["label"] == label)
            display = snapshot["displays"][0]
            readings.append({"label": name + ": " + label, "display_index": display["index"],
                             "pixel_sha256": display["pixel_sha256"], "nonzero_pixels": display["nonzero_pixels"],
                             "interpreted_text": text, "active_solenoid_addresses": snapshot["active_solenoids"]})
        observations[name] = item
    return {"format": "pinmame-machine-evidence", "version": 1,
            "extractor": {"id": "tools/build_wwf_runtime_evidence.py", "version": 1},
            "source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
                       "revision": REVISION, "path": "tools/build_wwf_runtime_evidence.py",
                       "sha256": sha(Path(__file__)), "license": "MIT", "quality": "observed",
                       "attribution": "Project harness and project curator curator. ROMs and raw frames remain external."},
            "driver_ids": [game], "machine_ids": [KEY], "switches": [], "outputs": [], "states": [], "mechanisms": [],
            "recreation_notes": [],
            "runtime": {"game": game, "rom_archive_sha256": ROM_HASHES[game],
                        "emulator": {"binary": "pinmame64.dll", "sha256": library_hash, "built_from_revision": REVISION},
                        "raw_runs": records, "command_template": "python -B tools/wwf_harness.py --game <game> --library <pinned-dll> --rom-path <read-only-rom-root> --work-dir <fresh-isolated-state> --scenario <retained-scenario> --boot-wait 15 --dmd-dir <external-dmd-dir> --output <external-trace.json>. Exact title masks only; host supplies all ball transfers. Early adapter/scenario originals remain immutable externally; final adapter adds target/game guards without changing title masks.",
                        "observations": {"runs": observations, "diagnostic_snapshots": readings,
                                         "service_language": "French lamp/coil titles for wwfr_103f; Active Switch and Coil Select headers remain English. US variants use English."}}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for game in RUNS:
        path = ROOT / f"evidence/runtime/data-east/wwf-royal-rumble-{game}-service-tests.json"
        payload = (json.dumps(build(args.review_root, game), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
        if args.check:
            if not path.is_file() or path.read_bytes().replace(b"\r\n", b"\n") != payload:
                raise ValueError(f"WWF runtime evidence drift: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)


if __name__ == "__main__":
    main()
