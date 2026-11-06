"""Extract diagnostic observations from the retained Embryon harness run.

This is deliberately read-only: the raw trace stays in the external evidence root.
The service display and coil events are compared by timestamp, not host readback.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

TRACE_SHA256 = "afdc30c3cd55e345e1b1bb53f158967599840bc5277945f75dbaa7ea96ada3ba"
EXPECTED = {1: 14, 2: 15, 3: 10, 4: 11, 5: 12, 6: 13, 7: 6,
            8: 5, 9: 1, 10: 2, 11: 3, 12: 4, 13: 18, 14: 19, 15: 20}
SEGMENTS = {63: 0, 6: 1, 91: 2, 79: 3, 102: 4, 109: 5,
            125: 6, 7: 7, 127: 8, 111: 9}


def verify_trace(path: Path) -> dict[int, int]:
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != TRACE_SHA256:
        raise ValueError("unexpected raw harness trace digest")
    trace = json.loads(payload)
    if trace["failure"] is not None or trace["game"] != "embryon":
        raise ValueError("not a successful Embryon run")
    # The service test was entered by step 4. Match a rising edge to the
    # nearest nonblank player-one display update, within 150 ms. The display
    # sometimes follows the edge; snapshots alone can straddle adjacent coils.
    samples = [s for s in trace["snapshots"] if s["label"].startswith("coil cycle sample")]
    observations: dict[int, set[int]] = {}
    displays = []
    for event in trace["events"]:
        if event.get("event") != "display" or event.get("index") != 0:
            continue
        digits = event.get("segments", [])[-2:]
        if len(digits) != 2 or any(n not in SEGMENTS for n in digits):
            continue
        number = SEGMENTS[digits[0]] * 10 + SEGMENTS[digits[1]]
        if 1 <= number <= 15:
            displays.append((event["time_s"], number))
    if not samples:
        raise ValueError("missing service-test samples")
    start = next(s["time_s"] for s in trace["snapshots"] if s["label"] == "cycling solenoid test") - 0.5
    end = samples[-1]["time_s"]
    for event in trace["events"]:
        if (event.get("event") != "solenoid" or event.get("state") != 1
                or not start <= event["time_s"] <= end):
            continue
        matches = [(abs(time - event["time_s"]), n) for time, n in displays
                   if abs(time - event["time_s"]) <= 0.15]
        if matches:
            _, number = min(matches)
            observations.setdefault(number, set()).add(event["number"])
    actual = {number: next(iter(addresses)) for number, addresses in observations.items()
              if len(addresses) == 1}
    if actual != EXPECTED:
        raise ValueError(f"unexpected or incomplete service mapping: {observations}")
    return actual


def verify_single_drop(trace: dict) -> list[dict]:
    """Check the repeatable break/restore/reset causality, without inferring mechanics."""
    if trace["failure"] is not None or trace["game"] != "embryon":
        raise ValueError("not a successful Embryon run")
    phases = [s for s in trace["steps"] if s["type"] == "set_switch" and s.get("switch") == 17]
    if [s["state"] for s in phases] != [1, 0, 1, 0, 1, 0, 1]:
        raise ValueError("incomplete switch-17 sequence")
    for i, phase in enumerate(phases):
        coils = phase["transitions"]["solenoids"]
        expected = [{"number": 1, "states": [1, 0]}] if i in (2, 6) else []
        if coils != expected or phase["observed_state"] != phase["state"]:
            raise ValueError(f"unexpected switch-17 reset phase: {phase['label']}")
    return [{k: s[k] for k in ("label", "switch", "state", "observed_state")} |
            {"solenoids": s["transitions"]["solenoids"]} for s in phases]
