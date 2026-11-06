"""Run poto_a32 against an explicitly synthetic, unidirectional organ-crank model.

This adapter reuses the pinned harness's public API, polling, scenario validation and raw trace.
It does not measure physical cam widths or motor speed. Model feedback is recorded as host
stimulus and is never presented as a ROM-produced switch observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import run_pinmame_harness as harness


def scenario(phase: float) -> dict:
    return {
        "format": "pinmame-harness-scenario", "version": 1, "game": "poto_a32",
        "notes": "All-direct inputs, keyboard off, mechanics off. Synthetic host crank feedback at 52/53. Fresh state. Output14 powers one-way phase progression; no physical cam speed or width claimed.",
        "watch_switches": [11, 12, 13, 14, 52, 53, 82, 84],
        "initial_switches": [{"switch": n, "state": 1} for n in (11, 12, 13)] + [{"switch": 52, "state": 0}, {"switch": 53, "state": int(phase == 0)}],
        "actions": [
            {"type": "pulse", "switch": 6, "hold_ms": 120, "settle_s": .5, "label": "coin 1"},
            {"type": "pulse", "switch": 6, "hold_ms": 120, "settle_s": .5, "label": "coin 2"},
            {"type": "pulse", "switch": 3, "hold_ms": 120, "settle_s": 12, "label": "start from synthetic crank position"},
            {"type": "set_switch", "switch": 13, "state": 0, "settle_s": .25, "label": "model served ball leaves trough entry"},
            {"type": "pulse", "switch": 14, "hold_ms": 200, "settle_s": 1, "label": "ball crosses shooter lane"},
            *[{"type": "pulse", "switch": n, "hold_ms": 200, "settle_s": .8, "label": f"complete organ target {n}"} for n in (41, 42, 43)],
            {"type": "wait", "seconds": 15, "label": "observe target-triggered organ movement"},
            {"type": "set_switch", "switch": -6, "state": 1, "settle_s": .5, "label": "Green reverse diagnostics direction"},
            {"type": "pulse_until_display", "switch": -7, "texts": ["ORGAN TEST"], "max_pulses": 40, "hold_ms": 200, "settle_s": 1.0, "label": "find own Organ Test title"},
            {"type": "pulse", "switch": 3, "hold_ms": 12000, "settle_s": 3, "snapshot_while_held": True, "label": "hold Start in Organ Test with synthetic crank feedback"},
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--rom-path", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--phase", type=float, choices=(0.0, .25), required=True)
    parser.add_argument("--period", type=float, required=True)
    parser.add_argument("--half-width", type=float, required=True)
    parser.add_argument("--jammed", action="store_true")
    args = parser.parse_args()
    if args.directory.exists():
        raise ValueError("each probe requires a new evidence/state directory")
    args.directory.mkdir(parents=True)
    scene = args.directory / "scenario.json"
    scene.write_text(json.dumps(scenario(args.phase), indent=2) + "\n", encoding="utf-8")
    phase = args.phase
    previous_time = None
    previous_drive = None
    previous_contacts = None
    original_poll = harness._poll_outputs

    def model_poll(library, recorder):
        nonlocal phase, previous_time, previous_drive, previous_contacts
        original_poll(library, recorder)
        now = time.monotonic()
        drive = int(bool(library.PinmameGetSolenoid(14)))
        if previous_time is not None and drive and not args.jammed:
            phase = (phase + (now - previous_time) / args.period) % 1
        previous_time = now
        contacts = (int(abs(phase - .5) <= args.half_width), int(min(phase, 1 - phase) <= args.half_width))
        if args.jammed:
            contacts = (0, 0)
        for number, state in zip((52, 53), contacts):
            library.PinmameSetSwitch(number, state)
        if previous_contacts != contacts:
            recorder.record("organ_model_host_feedback", phase=phase, switch_52=contacts[0], switch_53=contacts[1], motor_14=drive)
            previous_contacts = contacts
        if previous_drive != drive:
            recorder.record("organ_model_motor_transition", phase=phase, motor_14=drive, switch_52=contacts[0], switch_53=contacts[1])
            previous_drive = drive

    harness._poll_outputs = model_poll
    parsed = harness.build_parser().parse_args([
        "--library", str(args.library), "--game", "poto_a32", "--rom-path", str(args.rom_path),
        "--work-dir", str(args.directory / "state"), "--scenario", str(scene), "--boot-wait", "15",
        "--output", str(args.directory / "run.json"),
    ])
    result = harness.run(parsed)
    result["organ_model"] = {
        "kind": "synthetic unidirectional crank, host stimulus", "initial_phase": args.phase,
        "period_while_powered_s": args.period, "limit_half_width_turns": args.half_width,
        "jammed_no_contacts": args.jammed,
        "rule": "phase advances while public14 is active; closed53 near0 turns and open52 near0.5 turns; no physical timing/mark claim",
        "adapter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (args.directory / "run.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"failure": result["failure"], "events": len(result["events"]), "model": result["organ_model"]}))
    return int(bool(result["failure"]))


if __name__ == "__main__":
    raise SystemExit(main())
