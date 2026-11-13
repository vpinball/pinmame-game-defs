"""Recompute schema-conformant Mary Shelley's Frankenstein runtime evidence from immutable external runs.

The reading seed binds visually read DMD frames to pixel digests. Raw traces, source PGMs, NVRAM and
ROMs stay external. The builder refuses changed traces, scenarios, manifests, frames, libraries, the
title adapter and its templates, and the harness implementation, and checks every step a claim rests
on. Exploratory runs live beside the final runs under harness/ and are never read here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import zipfile

from build_external_evidence_manifest import canonical_bytes, check_manifest
from recorded_repository_source import verify_recorded_source

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/seeds/sega/mary-shelley-s-frankenstein-1995-runtime-readings.json"
OUTPUT = ROOT / "evidence/runtime/data-east/mary-shelley-s-frankenstein-frankst-service-tests.json"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
# Repository revision whose runner bytes were recorded in the runtime seed.
HARNESS_REVISION = "91d1a18cc5dbc71b6dd17b521183a32a185033d4"
KEY = "sega.mary-shelley-s-frankenstein.1995"
MANIFEST_SHA = "7c79c5f6b28bb089aec860159dbde81eb32b36e4c2dae45d8b74b12b62482e4b"
# Same-run checkpoint label -> the public output the ROM fired in answer to the host write before it.
GAMEPLAY = {
    "trough-lockout": 1, "trough-upkick": 2, "lever-autolaunch": 3, "upper-scoop-kick": 5,
    "lower-scoop-kick": 4, "north-pole-vuk-kick": 7, "ice-cave-eject-kick": 6,
    "output-17": 17, "output-18": 18, "output-19": 19, "output-20": 20, "output-21": 21, "output-22": 22,
    "laser-kick": 16, "spinner-diverter": 14,
}
# The host write each checkpoint answers when it is not the step just before it.
STIMULUS = {"trough-lockout": [3, 4], "trough-upkick": [14, 15]}
# COIL TEST entry -> public address; entries 2-16 even switch relay 10 first, 30 and 31 wrap to 1 and 25.
COIL_ENTRIES = dict(zip(range(1, 32), [1, 25, 2, 26, 3, 27, 4, 28, 5, 29, 6, 30, 7, 31, 8, 32,
                                       9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 1, 25]))
# LASER KICK TEST: each ball-holding switch closed in the test fires its own kicker.
KICK_TEST = {"north-pole-vuk-53-closed": 7, "ice-cave-eject-55-closed": 6, "upper-scoop-31-closed": 5,
             "lower-scoop-32-closed": 4, "shooter-lane-16-closed": 3}
PRINTER_LINES = range(37, 45)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_rom(seed):
    """Only the explicitly supplied existing ROM root is read."""
    if not (rom_root := os.environ.get("PINMAME_ROM_LIBRARY_ROOT")):
        return
    archive = Path(rom_root) / "frankst.zip"
    if digest(archive) != seed["rom_archive_sha256"]:
        raise ValueError("Frankenstein ROM archive changed")
    with zipfile.ZipFile(archive) as zipped:
        members = []
        for item in zipped.infolist():
            data = zipped.read(item)
            members.append({"name": item.filename, "size": item.file_size, "crc32": f"{item.CRC:08x}",
                            "sha1": hashlib.sha1(data).hexdigest(), "sha256": hashlib.sha256(data).hexdigest()})
    if sorted(members, key=lambda m: m["name"]) != seed["rom_members"]:
        raise ValueError("Frankenstein ROM member inventory changed")


def verified_runs(review_root):
    seed = read_json(SEED)
    base = review_root / KEY / "final"
    verify_recorded_source(ROOT, HARNESS_REVISION, "tools/run_pinmame_harness.py", seed["base_harness_sha256"])
    if digest(ROOT / "tools/frankenstein_harness.py") != seed["adapter_sha256"]:
        raise ValueError("Frankenstein title adapter changed")
    if digest(ROOT / "tools/frankenstein_header_templates.json") != seed["templates_sha256"]:
        raise ValueError("Frankenstein title templates changed")
    if check_manifest(base, "frankst") != MANIFEST_SHA:
        raise ValueError("Frankenstein raw evidence manifest changed")
    runs = {}
    for name, pin in seed["runs"].items():
        path = base / name / "run.json"
        if digest(path) != pin["sha256"]:
            raise ValueError(f"Frankenstein raw run changed: {name}")
        run = read_json(path)
        if (run["failure"] or run["game"] != "frankst" or run["handle_mechanics"] != 0
                or run["library_sha256"] != seed["library_sha256"]):
            raise ValueError(f"not a successful, pinned Frankenstein run: {name}")
        scenario = base / name / PureWindowsPath(run["scenario"]["path"]).name
        if digest(scenario) != run["scenario"]["sha256"] or read_json(ROOT / pin["scenario_path"]) != read_json(scenario):
            raise ValueError(f"Frankenstein scenario changed: {name}")
        runs[name] = run
    if len({run["work_dir"] for run in runs.values()}) != len(runs):
        raise ValueError("Frankenstein runs must use distinct fresh state directories")
    verify_rom(seed)
    return seed, runs


def snapshot(run, label):
    matches = [s for s in run["snapshots"] if s["label"] == label]
    if len(matches) != 1:
        raise ValueError(f"expected one snapshot {label}")
    return matches[0]


def step(run, label):
    matches = [s for s in run["steps"] if s["label"] == label]
    if len(matches) != 1:
        raise ValueError(f"expected one step {label}")
    return matches[0]


def watched(snap):
    return {w["number"]: w["state"] for w in snap["watched_switches"]}


def transitions(run, label):
    return {t["number"]: t["states"] for t in step(run, label)["transitions"]["solenoids"]}


def diagnostic_readings(review_root, seed, runs):
    from PIL import Image

    readings = []
    for reading in seed["readings"]:
        run = runs[reading["run"]]
        snap = snapshot(run, reading["label"])
        display = snap["displays"][0]
        frame = review_root / KEY / "final" / reading["run"] / "dmd" / PureWindowsPath(display["artifact"]).name
        with Image.open(frame) as pixels:
            valid = (pixels.size == (192, 64)
                     and hashlib.sha256(pixels.tobytes()).hexdigest() == reading["pixel_sha256"]
                     and display["pixel_sha256"] == reading["pixel_sha256"])
        if not valid:
            raise ValueError(f"Frankenstein visually read DMD frame changed: {frame}")
        group, address = reading["group"], reading.get("address")
        levels = {n: s for n, s in watched(snap).items() if n != -6}
        if group == "switch":
            # The read address closed and every other address open; the cabinet buttons also raise
            # their flipper-column copy (82 -> 64, 84 -> 63), which the ROM reports as 64 and 63.
            expected = {82: {82: 1, 64: 1}, 84: {84: 1, 63: 1}}.get(address, {address: 1})
            others = {n: s for n, s in levels.items() if n not in expected}
            if any(levels.get(n) != s for n, s in expected.items()) or any(others.values()):
                raise ValueError(f"switch reading without its public level: {reading['label']}")
            if reading["number"] != f"#{ {82: 64, 84: 63}.get(address, address):02d}":
                raise ValueError(f"switch reading with a different printed number: {reading['label']}")
        elif group == "lamp" and snap["active_lamps"] != [address]:
            raise ValueError(f"lamp reading without its lamp: {reading['label']}")
        elif group == "solenoid":
            entry = int(reading["label"].split("-")[1])
            fired = transitions(run, f"entry-{entry}-fired")
            if COIL_ENTRIES[entry] != address or {n for n, s in fired.items() if 1 in s} - {10} != {address}:
                raise ValueError(f"coil reading without its output: {reading['label']}")
        elif group == "screen":
            # A NONE screen in the switch test holds only the address the host wrote, which the ROM
            # does not report (63/64 are overwritten, 81, 83 and 85-88 are not wired).
            held = {int(reading["label"].split("-")[1])} if reading["run"] == "switch-test" and "-closed" in reading["label"] else set()
            if {n for n, s in levels.items() if s} - held or snap["active_lamps"]:
                raise ValueError(f"rest screen with an active input or lamp: {reading['label']}")
        readings.append({
            "label": f"{reading['run']}: {reading['label']}", "display_index": 0,
            "pixel_sha256": reading["pixel_sha256"], "interpreted_text": interpreted(reading),
            "active_solenoid_addresses": snap["active_solenoids"],
        })
    return readings


def interpreted(reading):
    group = reading["group"]
    if group in ("switch", "lamp"):
        return f"{reading['name']}; DRIVE {reading['drive_wire']}; RETURN {reading['return_wire']}; {reading['number']}"
    if group == "solenoid":
        return f"{reading['number']} {reading['name']}; POWER {reading['power_wire']}; CONTROL {reading['control_wire']}"
    return reading["name"]


def coil_test_observations(run):
    observations = []
    for entry, address in COIL_ENTRIES.items():
        fired = transitions(run, f"entry-{entry}-fired")
        if {n for n, s in fired.items() if 1 in s} - {10} != {address}:
            raise ValueError(f"COIL TEST entry {entry} no longer fires only {address}")
        observations.append({
            "label": f"entry-{entry}-fired", "input_kind": "switch", "input_address": 3,
            "observed_switch_addresses": [], "host_stimulus_switch_addresses": [3],
            "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [address], "result": "observed",
        })
        if address >= 25 and 32 >= address and fired.get(10) != [1]:
            raise ValueError(f"COIL TEST entry {entry} no longer selects relay 10 first")
    return observations


def kick_test_observations(run):
    observations = []
    for label, address in KICK_TEST.items():
        fired = transitions(run, label)
        if {n for n, s in fired.items() if 1 in s and n not in PRINTER_LINES and n != 23} != {address}:
            raise ValueError(f"LASER KICK TEST step {label} no longer fires only {address}")
        observations.append({
            "label": label, "input_kind": "switch", "input_address": step(run, label)["switch"],
            "observed_switch_addresses": [], "host_stimulus_switch_addresses": [step(run, label)["switch"]],
            "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [address], "result": "observed",
        })
    if any(1 in s for n, s in transitions(run, "left-outlane-37-closed").items() if n != 23):
        raise ValueError("LASER KICK TEST now answers a closed left outlane with an output")
    return observations


def gameplay_observations(run):
    observations = []
    steps = run["steps"]
    for index, item in enumerate(steps):
        if item["label"] not in GAMEPLAY:
            continue
        address = GAMEPLAY[item["label"]]
        if address not in {m["number"] for m in item["matched_outputs"] if 1 in m["states"]}:
            raise ValueError(f"Frankenstein gameplay checkpoint did not fire: {item['label']}")
        stimulus = item if "switch" in item else steps[index - 1]
        observations.append({
            "label": item["label"], "input_kind": "switch", "input_address": stimulus["switch"],
            "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": STIMULUS.get(item["label"], [stimulus["switch"]]),
            "active_solenoid_addresses": [], "transitioned_solenoid_addresses": [address], "result": "observed",
        })
    for label, addresses in (("left-button", {47, 48}), ("right-button", {45, 46})):
        states = transitions(run, label)
        if {n for n, s in states.items() if s == [1, 0]} != addresses:
            raise ValueError(f"Frankenstein paired button states changed: {label}")
        observations.append({
            "label": label + ": paired states asserted and released together", "input_kind": "switch",
            "input_address": step(run, label)["switch"], "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": [step(run, label)["switch"]], "active_solenoid_addresses": [],
            "held_synthetic_solenoid_addresses": sorted(addresses),
            "transitioned_solenoid_addresses": sorted(addresses), "result": "observed",
        })
    tail = [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"]]
    if {9, 12, 13} & set(tail):
        raise ValueError("a trap door or creature output appeared in gameplay; revisit the mechanism notes")
    return observations


def build(review_root):
    seed, runs = verified_runs(review_root)
    readings = diagnostic_readings(review_root, seed, runs)
    switch_run = runs["switch-test"]
    for button, matrix in {82: 64, 84: 63}.items():
        if watched(snapshot(switch_run, f"switch-{button}-closed")).get(matrix) != 1:
            raise ValueError(f"flipper column copy {button}->{matrix} not observed")
    if any(watched(snapshot(switch_run, f"switch-{n}-closed")).get(n) != 0 for n in (63, 64)):
        raise ValueError("a direct matrix write to 63/64 was not overwritten")
    cycle = [e["number"] for e in runs["cycling"]["events"] if e["event"] == "solenoid" and e["state"]]
    if not set(range(1, 23)) | set(range(25, 33)) <= set(cycle):
        raise ValueError("cycling tests no longer publish every driver 1-22 and 25-32")
    for name, run in runs.items():
        if {e["number"] for e in run["events"] if e["event"] == "solenoid" and e["number"] in PRINTER_LINES} - {37, 38, 44}:
            raise ValueError(f"a printer line other than 37, 38 or 44 changed in {name}")
    servo = runs["servo-laser-kick"]
    if any(transitions(servo, f"servo-start-{n}").get(44) != [1, 0] for n in (2, 3, 4)):
        raise ValueError("SERVO TEST no longer raises and drops 44 around each head command")
    run_notes = {
        "switch-test": "ACTIVE SWITCH TEST: every public address 1-64 and 81-88 held 2.0 s, released 1.4 s. "
                       "The green forward/reverse button (-6) is held throughout to make Black step forward. "
                       "Each closed public address appears alone with its name, drive and return wire colours "
                       "and number. Direct writes to 63/64 read back 0 and show NONE (the flipper column "
                       "overwrites them); 82 and 84 read back as 64 and 63 and are named RIGHT and LEFT END OF "
                       "STROKE; 81, 83 and 85-88 show NONE.",
        "lamp-test": "SINGLE LAMP TEST: step 1 shows NONE, each later Start press lit exactly lamp n-1 with its "
                     "name, drive and return wire colours, and step 66 wraps to lamp 1.",
        "coil-test": "COIL TEST: the right flipper button shows the next entry with its name, power and control "
                     "wire colours and number, and Start fires it. Each entry fired only its own public address; "
                     "the R entries select relay 10 first and the L entries release it. Relay 10 has no entry of "
                     "its own and #8R is printed FLASH:NOT USED.",
        "cycling": "CYCLING FLASHERS pulses 25-32 behind relay 10 and 15; CYCLING COILS walks 1-9 with each muxed "
                   "25-32 behind relay 10, then 11-22. Boot pulses 13 once and toggles 37, 38 and 44.",
        "servo-laser-kick": "SERVO TEST: each Start press toggles the creature head routine; 44 rises and falls "
                            "around each command while 37 and 38 toggle, and no other driver changes. LASER KICK "
                            "TEST: the closed left outlane alone fires nothing (the test waits for a ball), while "
                            "the VUK, eject, both scoops and the shooter lane each fire their own kicker.",
        "gameplay": "Fresh six-ball trough; two coins and Start, then the host moves balls only after the ROM's own "
                    "output. Same-run checkpoints: trough lockout, up-kicker, lever autolaunch, upper and lower "
                    "scoops, North Pole VUK, Ice Cave eject, four bumpers, two slings, the left outlane Laser Kick "
                    "and the spinner-fired right orbit diverter; both cabinet buttons assert and release their paired "
                    "synthetic states. An unchecked tail of three ramp shots and VUK closures fired no trap door "
                    "(9, 12) or creature output (13).",
    }
    raw_runs, attributed = [], {}
    for name, run in runs.items():
        pin = seed["runs"][name]
        raw_runs.append({
            "name": name, "sha256": pin["sha256"], "self_test_pulses": 0,
            "scenario_path": pin["scenario_path"], "scenario_sha256": digest(ROOT / pin["scenario_path"]),
            "action_count": run["scenario"]["action_count"], "snapshot_count": len(run["snapshots"]),
            "watch_switches": run["watch_switches"], "initial_switches": run["initial_switches"],
            "nvram_initialization": "New empty run-specific state directory; no inherited NVRAM.",
            "boot_wait_s": 2,
        })
        canonical_scenario = hashlib.sha256(canonical_bytes(read_json(ROOT / pin["scenario_path"]))).hexdigest()
        attributed[name] = {
            "solenoid_addresses_seen": sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"}),
            "ordered_solenoid_on_sequence": [e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"]],
            "note": run_notes[name] + " Raw scenario SHA256 " + run["scenario"]["sha256"]
                    + "; canonical parsed repository scenario SHA256 " + canonical_scenario + ".",
        }
    attributed["coil-test"]["named_action_observations"] = coil_test_observations(runs["coil-test"])
    attributed["servo-laser-kick"]["named_action_observations"] = kick_test_observations(servo)
    attributed["gameplay"]["named_action_observations"] = gameplay_observations(runs["gameplay"])
    all_events = [e for run in runs.values() for e in run["events"]]
    return {
        "format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/build_frankenstein_runtime.py", "version": 1},
        "source": {
            "kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
            "revision": REVISION, "path": "review-artifacts/" + KEY + "/final",
            "sha256": MANIFEST_SHA, "quality": "observed", "license": "NOASSERTION",
            "attribution": "Primary curator; user-authorized existing frankst (USA CPU 1.03) ROM",
            "manifest_algorithm": "tools/build_external_evidence_manifest.py --game frankst; case-sensitive "
                                  "relative POSIX sort, path/size/SHA256 per file, canonical JSON plus LF; "
                                  "manifest.json/manifest.sha256 excluded.",
        },
        "driver_ids": ["frankst"], "machine_ids": [KEY],
        "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {
            "game": "frankst", "rom_archive_sha256": seed["rom_archive_sha256"],
            "emulator": {"binary": "pinmame64.dll", "sha256": seed["library_sha256"], "built_from_revision": REVISION},
            "raw_runs": raw_runs,
            "command_template": "python tools/frankenstein_harness.py --library <pinned-pinmame64.dll> --game frankst "
                                "--rom-path <authorized-existing-rom-root> --work-dir <new-empty-state-directory> "
                                "--scenario <raw_run.scenario_path> --dmd-dir <external-run-dmd> --output "
                                "<external-run.json>. Keyboard handling off, mechanisms off, binary solenoid "
                                "mode, default 2 s boot wait. Service screens are reached by stepping Black until "
                                "the title band matches a verified template (tools/frankenstein_header_templates.json); "
                                "the frame readings are pinned to pixel digests in "
                                "tools/seeds/sega/mary-shelley-s-frankenstein-1995-runtime-readings.json (SHA256 "
                                + digest(SEED) + "), with the ROM members, library, adapter, template and harness digests.",
            "observations": {
                "service_language": "English, USA CPU 1.03 (FEB.01, 1995) / display A1.03 (JANUARY 30, 1995)",
                "lamp_addresses_seen": sorted({e["number"] for e in all_events if e["event"] == "lamp"}),
                "solenoid_addresses_seen": sorted({e["number"] for e in all_events if e["event"] == "solenoid"}),
                "diagnostic_snapshots": readings, "runs": attributed,
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.review_root), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise ValueError("Frankenstein runtime evidence drifted")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)


if __name__ == "__main__":
    main()
