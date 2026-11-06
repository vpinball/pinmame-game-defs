"""Derive the organ contract from five successful, fresh-state synthetic probes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_external_evidence_manifest import check_manifest, write_manifest

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("evidence/runtime/data-east/phantom-of-the-opera-organ.json")
PIN = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
LIBRARY_SHA = "8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5"
ADAPTER_SHA = "4e05666177e56628209eab14dc5abdf7a21738b2fcb7efa76efcf5cdbcb64986"
ROM_SHA = "7e90f6a0547d1a83b6aff8492ba0f0e8767a0f87345b9c2b47095a78764bf4e7"
CASES = ("closed-narrow", "midway-narrow", "closed-wide", "midway-wide", "jammed-no-limits")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(directory: Path) -> dict:
    digest = check_manifest(directory, "poto_a32")
    raw_runs = []
    runs = {}
    for name in CASES:
        path = directory / name / "run.json"
        run = json.loads(path.read_text(encoding="utf-8"))
        if run["failure"] is not None or run["library_sha256"] != LIBRARY_SHA:
            raise ValueError(f"unsuccessful or wrong-emulator organ run: {name}")
        if run["organ_model"]["adapter_sha256"] != ADAPTER_SHA:
            raise ValueError(f"wrong reactive adapter: {name}")
        events = run["events"]
        if any(event["event"] == "key" for event in events):
            raise ValueError(f"keyboard-enabled organ run: {name}")
        start = next(event["time_s"] for event in events if event["event"] == "switch" and event.get("step") == 12 and event["state"] == 1)
        transitions = [event for event in events if event["event"] == "organ_model_motor_transition"]
        cycles = []
        active = None
        for event in transitions:
            if event["time_s"] >= start:
                break
            if event["motor_14"]:
                active = event
            elif active is not None:
                cycles.append({"on_s": active["time_s"], "off_s": event["time_s"], "powered_duration_s": round(event["time_s"] - active["time_s"], 6), "synthetic_stop_phase": round(event["phase"], 6), "host_52_at_stop": event["switch_52"], "host_53_at_stop": event["switch_53"]})
                active = None
        expected_count = 3 if name.startswith("midway") or name == "jammed-no-limits" else 2
        if len(cycles) != expected_count:
            raise ValueError(f"unexpected automatic organ cycle count: {name}")
        endpoints = [(cycle["host_52_at_stop"], cycle["host_53_at_stop"]) for cycle in cycles]
        if name == "jammed-no-limits":
            if endpoints != [(0, 0)] * 3 or not all(5.5 < cycle["powered_duration_s"] < 6.5 for cycle in cycles):
                raise ValueError("jammed run did not demonstrate three bounded attempts")
        elif endpoints != ([(0, 1)] if name.startswith("midway") else []) + [(1, 0), (0, 1)]:
            raise ValueError(f"automatic homing/open/close endpoints disagree: {name}")
        test = run["steps"][-1]
        drive = next(item["states"] for item in test["transitions"]["solenoids"] if item["number"] == 14)
        if drive.count(1) < 10:
            raise ValueError(f"Organ Test did not repeatedly pulse motor14: {name}")
        checkpoint = next(step for step in run["steps"] if step.get("matched_text") == "ORGAN TEST")
        summary = {"model": run["organ_model"], "automatic_cycles": cycles, "organ_test_motor_pulses": drive.count(1), "organ_test_host_hold_ms": test["hold_ms"]}
        runs[name] = {"diagnostic_checkpoints": [{"matched_text": "ORGAN TEST", "after_service_pulses": checkpoint["pulses"]}], "solenoid_addresses_seen": sorted({event["number"] for event in events if event["event"] == "solenoid" and event["state"]}), "note": json.dumps(summary, sort_keys=True, separators=(",", ":")), "limitation": "52/53 and phase are synthetic host feedback, never ROM-produced switch observations or physical cam/speed measurements. Event durations use the host clock. Four cam/initial-position probes agree on homing and endpoint behavior; the open-contact jam probe bounds retries."}
        scene = directory / name / "scenario.json"
        if sha(scene) != run["scenario"]["sha256"]:
            raise ValueError(f"scenario drift: {name}")
        raw_runs.append({"name": f"phantom-of-the-opera-1990/organ/{name}/run.json", "sha256": sha(path), "scenario_path": f"phantom-of-the-opera-1990/organ/{name}/scenario.json", "scenario_sha256": sha(scene), "action_count": len(run["steps"]), "self_test_pulses": checkpoint["pulses"], "boot_wait_s": 15, "nvram_initialization": "New empty per-run state directory; no NVRAM copied from another probe.", "snapshot_count": len(run["snapshots"]), "watch_switches": run["watch_switches"]})
    return {"format": "pinmame-machine-evidence", "version": 1, "extractor": {"id": "tools/build_phantom_organ_evidence.py", "version": 1}, "source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame", "revision": PIN, "path": "external:pinmame-review-artifacts/phantom-of-the-opera-1990/organ/manifest.json", "sha256": digest, "license": "NOASSERTION", "attribution": "Authorized local ROM; PinMAME contributors; synthetic host-model probe, no ROM/NVRAM redistribution", "quality": "observed", "manifest_algorithm": "build_external_evidence_manifest.py canonical_bytes(build_manifest(directory,poto_a32))+LF; sorted relative POSIX paths, sizes and SHA256; excludes manifest.json/manifest.sha256"}, "driver_ids": ["poto_a32"], "machine_ids": ["data-east.phantom-of-the-opera.1990"], "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [], "runtime": {"game": "poto_a32", "rom_archive_sha256": ROM_SHA, "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA, "built_from_revision": PIN}, "raw_runs": raw_runs, "command_template": "python -B tools/phantom_organ_probe.py --library <pinned-library> --rom-path <authorized-ROM-root> --directory <new-directory> --phase <0|0.25> --period <6|4> --half-width <0.025|0.08> [--jammed]; each exact argument set is retained in its model summary and scenario.", "observations": {"runs": runs}}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.directory, "poto_a32")
    text = json.dumps(build(args.directory), indent=2, sort_keys=True) + "\n"
    if args.check:
        if (ROOT / OUTPUT).read_text(encoding="utf-8").replace("\r\n", "\n") != text:
            raise ValueError("organ evidence drift")
    else:
        (ROOT / OUTPUT).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / OUTPUT).write_text(text, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
