#!/usr/bin/env python3
"""Recompute exact displayed-coil pairings from the three retained service runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256
from build_external_evidence_manifest import check_manifest

SUMMARY = ROOT / "evidence/runtime/by35/skateball-1980-solenoid-tests.json"
SCENARIO = ROOT / "tools/harness-scenarios/by35/skateball-solenoid-test.json"
READINGS = ROOT / "tools/seeds/bally/skateball-1980-display-readings.json"
READINGS_LABEL = "tools/seeds/bally/skateball-1980-display-readings.json"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA256 = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
EXPECTED = {7: 1, 6: 2, 2: 3, 14: 4, 15: 5, 11: 6, 12: 7, 13: 8, 8: 9, 9: 10, 10: 11, 18: 12, 19: 13}
DIGITS = {0: " ", 0x3F: "0", 0x06: "1", 0x5B: "2", 0x4F: "3", 0x66: "4", 0x6D: "5", 0x7D: "6", 0x07: "7", 0x7F: "8", 0x6F: "9"}


def decode(segments: list[int]) -> str:
    return "".join(DIGITS.get(value & 0x7F, "?") for value in segments).strip()


def derive_pairings(run: dict) -> list[dict]:
    """Use the first complete refresh within 150 ms of each coil rising edge.

    BY35 blanks its score display between test values. Sampling only at the
    rising-edge timestamp sees the blank; the following completed refresh is
    before its matching falling edge. Pin exact segment words, not merely a decoded
    number that could hide altered words behind the comma-bit mask.
    """
    pairings = {}
    frames = [e for e in run["events"] if e["event"] == "display" and e["index"] == 0 and "segments" in e]
    for event in run["events"]:
        if event["event"] != "solenoid" or not event["state"] or event["time_s"] < 31:
            continue
        number = event["number"]
        if number not in EXPECTED:
            raise ValueError(f"Unexpected service-test coil {number}")
        falling_edges = [e["time_s"] for e in run["events"] if e["event"] == "solenoid" and e["number"] == number and not e["state"] and e["time_s"] > event["time_s"]]
        if not falling_edges:
            raise ValueError(f"No matching falling edge for public {number}")
        fall_time = min(falling_edges)
        for frame in frames:
            if not 0 < frame["time_s"] - event["time_s"] < 0.15 or frame["time_s"] >= fall_time:
                continue
            reading = decode(frame["segments"])
            if len(reading) != 2 or not reading.isdigit():
                continue
            if int(reading) != EXPECTED[number]:
                raise ValueError(f"Public coil {number} displayed {reading}, expected {EXPECTED[number]:02d}")
            pairings.setdefault(number, {
                "public_address": number, "self_test_number": int(reading),
                "rising_edge_time_s": event["time_s"], "display_time_s": frame["time_s"],
                "display_index": 0, "segments": frame["segments"],
                "segments_sha256": hashlib.sha256(canonical_bytes(frame["segments"])).hexdigest(),
            })
            break
    if set(pairings) != set(EXPECTED):
        raise ValueError(f"Incomplete service test: missing {sorted(set(EXPECTED) - set(pairings))}")
    return sorted(pairings.values(), key=lambda value: value["self_test_number"])


def build(runs: Path, rom_root: Path, *, write_readings: bool = False) -> dict:
    digest = check_manifest(runs, "skatebll")
    if write_readings and READINGS.exists():
        raise ValueError("Refusing to overwrite the pinned display readings")
    rows, raw, observations, readings = [], [], {}, []
    for driver in ("skatebll", "skatebla", "skateblb"):
        path = runs / f"{driver}-coil-run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        if run["failure"] is not None or run["game"] != driver or run["library_sha256"] != LIBRARY_SHA256:
            raise ValueError(f"Wrong or failed retained run: {driver}")
        if run["scenario"]["sha256"] != file_sha256(SCENARIO) or run["initial_switches"]:
            raise ValueError(f"Wrong scenario or startup switches: {driver}")
        pulses = [e for e in run["events"] if e["event"] == "solenoid" and e["state"]]
        rows.append({"driver": driver, "retained_from": f"external:pinmame-review-artifacts/skateball-1980/harness/{path.name}",
                     "sha256": file_sha256(path), "rom_archive_sha256": file_sha256(rom_root / f"{driver}.zip"),
                     "pairings": derive_pairings(run), "solenoids_seen": sorted({e["number"] for e in pulses}),
                     "unfitted_continuous_pulses": [e for e in pulses if e["number"] in (17, 20)]})
        readings.append({"driver": driver, "pairings": rows[-1]["pairings"]})
        raw.append({"name": driver + "-solenoid-test", "sha256": file_sha256(path), "retained_from": rows[-1]["retained_from"],
                    "scenario_path": SCENARIO.relative_to(ROOT).as_posix(), "scenario_sha256": file_sha256(SCENARIO),
                    "self_test_pulses": sum(s.get("switch") == -7 for s in run["steps"]),
                    "nvram_initialization": "fresh isolated state", "initial_switches": run["initial_switches"]})
        observations[driver + "-solenoid-test"] = {
            "solenoid_addresses_seen": rows[-1]["solenoids_seen"],
            "note": f"ROM archive SHA-256 {rows[-1]['rom_archive_sha256']}. First complete player-1 refresh within 150 ms of each output rising edge and before its falling edge gives the thirteen service-number pairings pinned with exact segment words and event times in {READINGS_LABEL}. Continuous startup output pulses: {json.dumps(rows[-1]['unfitted_continuous_pulses'], sort_keys=True, separators=(',', ':'))}. The schematic marks those loads N/U; activity alone does not prove fitment."
        }
    flipper_path = runs / "skatebll-flippers-tilt-run.json"
    flipper = json.loads(flipper_path.read_text(encoding="utf-8"))
    flipper_scenario = ROOT / "tools/harness-scenarios/by35/skateball-flippers-and-tilt.json"
    if flipper["failure"] is not None or flipper["game"] != "skatebll" or flipper["library_sha256"] != LIBRARY_SHA256 or flipper["scenario"]["sha256"] != file_sha256(flipper_scenario):
        raise ValueError("Wrong or failed flipper/tilt run")
    expected = {"right button before tilt (held)": [18, 19, 45, 46], "left button before tilt (held)": [18, 19, 47, 48],
                "physical tilt7 drops enable (held)": [18], "right button after tilt (held)": [18], "left button after tilt (held)": [18]}
    snapshots = [{"label": s["label"], "time_s": s["time_s"], "active_solenoids": s["active_solenoids"]}
                 for s in flipper["snapshots"] if s["label"] in expected]
    if {s["label"]: s["active_solenoids"] for s in snapshots} != expected:
        raise ValueError("Flipper/tilt observations differ from pinned conclusion")
    seed = {"format": "pinmame-segment-display-readings", "machine_id": "bally.skateball.1980",
            "note": "Each driver's first complete player-1 refresh within 150 ms of a solenoid rising edge and before its falling edge. Segment words, hash and both event times are pinned; the builder recomputes every entry from the retained runs.",
            "runs": readings}
    if write_readings:
        READINGS.write_bytes(canonical_bytes(seed))
    elif not READINGS.exists() or READINGS.read_bytes() != canonical_bytes(seed):
        raise ValueError("Retained service display frames differ from the pinned readings")
    flipper_name = "skatebll-flippers-tilt"
    raw.append({"name": flipper_name, "retained_from": f"external:pinmame-review-artifacts/skateball-1980/harness/{flipper_path.name}",
                "sha256": file_sha256(flipper_path), "scenario_path": flipper_scenario.relative_to(ROOT).as_posix(),
                "scenario_sha256": file_sha256(flipper_scenario), "self_test_pulses": sum(s.get("switch") == -7 for s in flipper["steps"]),
                "nvram_initialization": "fresh isolated state", "initial_switches": flipper["initial_switches"]})
    addresses = {"right button before tilt (held)": 82, "left button before tilt (held)": 84,
                 "physical tilt7 drops enable (held)": 7, "right button after tilt (held)": 82, "left button after tilt (held)": 84}
    actions = [{"label": s["label"], "input_kind": "switch", "input_address": addresses[s["label"]],
                "observed_switch_addresses": [], "host_stimulus_switch_addresses": [addresses[s["label"]]],
                "active_solenoid_addresses": s["active_solenoids"], "result": "observed"} for s in snapshots]
    observations[flipper_name] = {"named_action_observations": actions,
        "note": "Held-snapshot times and exact states: " + json.dumps(snapshots, sort_keys=True, separators=(",", ":"))}
    return {"format": "pinmame-machine-evidence", "version": 1, "machine_ids": ["bally.skateball.1980"],
            "driver_ids": [r["driver"] for r in rows], "switches": [], "outputs": [], "mechanisms": [], "states": [], "recreation_notes": [],
            "extractor": {"id": "tools/skateball_runtime_summary.py", "version": 1},
            "source": {"kind": "runtime_scenario", "path": "external:pinmame-review-artifacts/skateball-1980/harness",
                       "repository": "https://github.com/vpinball/pinmame", "revision": REVISION, "quality": "validated",
                       "license": "NOASSERTION", "attribution": "Local LibPinMAME service tests using the user-authorized ROM corpus; ROM bytes remain external",
                       "sha256": digest, "manifest_algorithm": "Directory manifest from tools/build_external_evidence_manifest.py: sorted relative POSIX paths, sizes and SHA-256 values serialized as compact canonical JSON plus newline. Individual raw runs are pinned separately."},
            "runtime": {"game": "skatebll", "rom_archive_sha256": rows[0]["rom_archive_sha256"],
                        "emulator": {"binary": "pinmame64.dll", "built_from_revision": REVISION, "sha256": LIBRARY_SHA256},
                        "command_template": "python tools/run_pinmame_harness.py --library <libpinmame> --game <driver> --rom-path <roms> --work-dir <fresh-isolated-state> --scenario <scenario.json> --output <external-run.json>; keyboard handling off. Scenario and raw-run hashes are recorded per run.",
                        "raw_runs": raw, "observations": {"physical_service_solenoid_to_public": {str(v): k for k, v in EXPECTED.items()}, "runs": observations}}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path)
    parser.add_argument("--rom-root", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-readings", action="store_true", help="explicitly regenerate the display-frame seed from retained runs")
    args = parser.parse_args()
    runs = args.runs or Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "skateball-1980/harness"
    roms = args.rom_root or Path(os.environ["PINMAME_ROM_LIBRARY_ROOT"])
    if args.check and args.write_readings:
        parser.error("--check and --write-readings are mutually exclusive")
    content = canonical_bytes(build(runs, roms, write_readings=args.write_readings))
    if args.check:
        if SUMMARY.read_bytes() != content:
            raise SystemExit("Skateball runtime summary differs from retained runs")
    else:
        SUMMARY.write_bytes(content)
    print("Skateball runtime pairings match" if args.check else "Wrote Skateball runtime pairings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
