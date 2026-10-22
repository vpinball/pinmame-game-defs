"""Recompute schema-conformant Baywatch evidence from immutable external runs.

The reading seed binds visually checked DMD frames to pixel digests. Raw traces, source
PGMs, NVRAM and ROMs stay external. Checks reject changed traces, scenarios, manifests,
frames and harness implementations; failed explorations never become causal evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import zipfile

from build_external_evidence_manifest import canonical_bytes, check_manifest

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tools/baywatch_runtime_readings.json"
OUTPUT = ROOT / "evidence/runtime/data-east/baywatch-usa-400-service-tests.json"
REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
KEY = "sega.baywatch.1995"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_rom(seed):
    """Only the explicitly supplied existing ROM root is read."""
    if not (rom_root := os.environ.get("PINMAME_ROM_LIBRARY_ROOT")):
        return
    archive = Path(rom_root) / "baywatch.zip"
    if digest(archive) != seed["rom_archive_sha256"]:
        raise ValueError("Baywatch ROM archive changed")
    with zipfile.ZipFile(archive) as zipped:
        members = []
        for item in zipped.infolist():
            if item.is_dir():
                continue
            data = zipped.read(item)
            members.append({
                "name": item.filename, "size": item.file_size,
                "crc32": f"{item.CRC:08x}", "sha1": hashlib.sha1(data).hexdigest(),
                "sha256": hashlib.sha256(data).hexdigest(),
            })
    if sorted(members, key=lambda x: x["name"]) != sorted(seed["rom_members"], key=lambda x: x["name"]):
        raise ValueError("Baywatch ROM member inventory changed")


def verified_runs(review_root):
    seed = read_json(SEED)
    base = review_root / KEY
    if (digest(base / "probe_harness.py") != seed["harness_script_sha256"]
            or digest(ROOT / "tools/run_pinmame_harness.py") != seed["base_harness_sha256"]):
        raise ValueError("Baywatch harness implementation changed")
    manifest = check_manifest(base / "harness", "baywatch")
    if manifest != seed["manifest_sha256"]:
        raise ValueError("Baywatch raw evidence manifest changed")
    runs = {}
    for name, pin in seed["runs"].items():
        path = base / "harness" / (name + ".json")
        if digest(path) != pin["sha256"]:
            raise ValueError(f"Baywatch raw run changed: {name}")
        run = read_json(path)
        if (run["failure"] or run["game"] != "baywatch" or run["handle_mechanics"] != 0
                or run["library_sha256"] != seed["library_sha256"]):
            raise ValueError(f"not a successful, pinned Baywatch run: {name}")
        scenario = base / PureWindowsPath(run["scenario"]["path"]).name
        if (digest(scenario) != run["scenario"]["sha256"]
                or read_json(ROOT / pin["scenario_path"]) != read_json(scenario)):
            raise ValueError(f"Baywatch scenario changed: {name}")
        runs[name] = run
    if len({run["work_dir"] for run in runs.values()}) != len(runs):
        raise ValueError("Baywatch runs must use distinct fresh state directories")
    verify_rom(seed)
    return seed, runs, manifest


def diagnostic_readings(review_root, seed, runs):
    from PIL import Image

    readings = []
    for reading in seed["readings"]:
        run = runs[reading["run"]]
        snapshot = next(s for s in run["snapshots"] if s["label"] == reading["label"])
        display = snapshot["displays"][0]
        frame = (review_root / KEY / "harness" / f"{reading['run']}-dmd"
                 / PureWindowsPath(display["artifact"]).name)
        with Image.open(frame) as pixels:
            valid = (pixels.size == (192, 64)
                     and hashlib.sha256(pixels.tobytes()).hexdigest() == reading["pixel_sha256"]
                     and display["pixel_sha256"] == reading["pixel_sha256"])
        if not valid:
            raise ValueError(f"Baywatch visually read DMD frame changed: {frame}")
        readings.append({
            "label": f"{reading['run']}: {reading['label']}",
            "display_index": 0, "pixel_sha256": reading["pixel_sha256"],
            "interpreted_text": reading["name"],
            "active_solenoid_addresses": snapshot["active_solenoids"],
        })
    return readings


def gameplay_observations(game):
    observations = []
    for index, step in enumerate(game["steps"]):
        if step["type"] not in ("wait_until_output", "pulse_until_output"):
            continue
        matches = {m["number"] for m in step["matched_outputs"] if 1 in m["states"]}
        if set(step["addresses"]) != matches:
            raise ValueError(f"Baywatch gameplay checkpoint did not fire: {step['label']}")
        # A wait observes the response to the immediately preceding host write.
        stimulus = step if "switch" in step else game["steps"][index - 1]
        observations.append({
            "label": step["label"], "input_kind": "switch",
            "input_address": stimulus["switch"], "observed_switch_addresses": [],
            "host_stimulus_switch_addresses": (
                [22, 23, 24] if step["label"] == "bank-reset" else [stimulus["switch"]]
            ),
            "active_solenoid_addresses": [],
            "transitioned_solenoid_addresses": sorted(matches), "result": "observed",
        })
    for label, addresses in (("left-button", {47, 48}), ("right-button", {45, 46})):
        step = next(s for s in game["steps"] if s.get("label") == label)
        states = [s for s in step["transitions"]["solenoids"] if s["number"] in addresses]
        if {s["number"] for s in states if s["states"] == [1, 0]} != addresses:
            raise ValueError(f"Baywatch paired button states changed: {label}")
        observations.append({
            "label": label + ": paired states asserted and released together",
            "input_kind": "switch", "input_address": step["switch"],
            "observed_switch_addresses": [], "host_stimulus_switch_addresses": [step["switch"]],
            "active_solenoid_addresses": [],
            "held_synthetic_solenoid_addresses": sorted(addresses),
            "transitioned_solenoid_addresses": sorted(addresses), "result": "observed",
        })
    return observations


def build(review_root):
    seed, runs, manifest = verified_runs(review_root)
    readings = diagnostic_readings(review_root, seed, runs)
    raw_runs = []
    attributed = {}
    run_notes = {
        "switch-sweep": "DMD transmission can retain an earlier address. The separate long-settle "
                        "confirmation supplies the VUK readings; host writes are stimulus, not ROM feedback.",
        "switch-confirm": "Long-settle frames distinguish trough opto 15, rear upper VUK 44, "
                          "under-arch Super VUK 46, unused 51 and the left cabinet-button matrix copy.",
        "lamp-sweep": "All 64 single-lamp addresses were exercised. Incomplete first-run frames "
                      "16/17 are replaced only by the corresponding stable successor readings.",
        "lamp-sweep-stable": "Same parsed sequence with longer settling; frames 16/17, 33 and 64 "
                             "were visually confirmed. No press-count-only semantic assignments.",
        "coil-cycle": "Names are readings of displayed slots; DMD transmission can lag electrical "
                      "edges. Snapshot active states are retained literally. Output 10 selects "
                      "the alternate 25-32 bank; the cycle also labels driver 15 NOT USED.",
        "printer-explore": "Adjustment 53 reached TRANSMITTING DATA then CHECK CONNECTIONS. "
                           "No 37-44 transition was seen; non-observation does not prove non-use.",
        "shark-service": "Adjustment 50 published output 13, but its delayed timing did not isolate "
                         "rollover 54 as the cause, separately from autonomous service/ball search.",
        "gameplay-other-mechanisms": "Fresh five-ball trough; same-run serve, lower launch, three "
                                    "capture/eject devices, Laser Kick, bumpers, slings and drop reset "
                                    "passed. Driver 15 also pulses during gameplay; its purpose remains "
                                    "unknown. Both cabinet buttons assert/release paired synthetic states.",
    }
    for name, run in runs.items():
        pin = seed["runs"][name]
        raw_runs.append({
            "name": name, "sha256": pin["sha256"], "self_test_pulses": 0,
            "scenario_path": pin["scenario_path"],
            "scenario_sha256": digest(ROOT / pin["scenario_path"]),
            "action_count": run["scenario"]["action_count"],
            "snapshot_count": len(run["snapshots"]), "watch_switches": run["watch_switches"],
            "initial_switches": run["initial_switches"],
            "nvram_initialization": "New empty run-specific state directory; no inherited NVRAM.",
            "boot_wait_s": 8 if name in ("shark-service", "gameplay-other-mechanisms") else 5,
        })
        canonical_scenario = hashlib.sha256(canonical_bytes(read_json(ROOT / pin["scenario_path"]))).hexdigest()
        attributed[name] = {
            "solenoid_addresses_seen": sorted({e["number"] for e in run["events"] if e["event"] == "solenoid"}),
            "ordered_solenoid_on_sequence": [
                e["number"] for e in run["events"] if e["event"] == "solenoid" and e["state"]
            ],
            "note": (run_notes[name] + " Raw scenario SHA256 " + run["scenario"]["sha256"]
                     + "; canonical parsed repository scenario SHA256 " + canonical_scenario
                     + ". Parsed JSON is equal; the original Windows line endings remain in the raw hash."),
        }
    attributed["gameplay-other-mechanisms"]["named_action_observations"] = gameplay_observations(runs["gameplay-other-mechanisms"])
    attributed["shark-service"]["limitation"] = "No causal 54-to-13 proof is asserted from this run."
    attributed["printer-explore"]["unobserved_watched_addresses"] = list(range(37, 45))
    attributed["printer-explore"]["limitation"] = "Only public output transitions are checked; no physical printer is attached."
    all_events = [e for run in runs.values() for e in run["events"]]
    return {
        "format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/build_baywatch_runtime.py", "version": 1},
        "source": {
            "kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
            "revision": REVISION, "path": "review-artifacts/" + KEY + "/harness",
            "sha256": manifest, "quality": "observed", "license": "NOASSERTION",
            "attribution": "Primary curator; user-authorized existing USA 4.00 ROM",
            "manifest_algorithm": "tools/build_external_evidence_manifest.py --game baywatch; "
                                  "case-sensitive relative POSIX sort, path/size/SHA256 per file, "
                                  "canonical JSON plus LF; manifest.json/manifest.sha256 excluded.",
        },
        "driver_ids": ["baywatch"], "machine_ids": [KEY],
        "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {
            "game": "baywatch", "rom_archive_sha256": seed["rom_archive_sha256"],
            "emulator": {"binary": "pinmame64.dll", "sha256": seed["library_sha256"],
                         "built_from_revision": REVISION},
            "raw_runs": raw_runs,
            "command_template": "python tools/baywatch_harness.py --library <pinned-pinmame64.dll> "
                                "--game baywatch --rom-path <authorized-existing-rom-root> "
                                "--work-dir <new-empty-state-directory> --boot-wait <raw_run.boot_wait_s> "
                                "--handle-mechanics 0 --scenario <raw_run.scenario_path> "
                                "--dmd-dir <external-run-dmd> --output <external-run.json>. "
                                "Keyboard handling off; binary solenoid mode. Original runs used the "
                                "retained probe_harness.py adapter; its SHA256, the base harness SHA256 "
                                "and exact ROM members are pinned in tools/baywatch_runtime_readings.json "
                                "(SHA256 " + digest(SEED) + "). The committed adapter has equivalent "
                                "verified masks. Failed explorations remain in the external manifest "
                                "and are excluded from successful raw_runs and causal observations.",
            "observations": {
                "service_language": "English, USA CPU 4.00 / display A4.00",
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
            raise ValueError("Baywatch runtime evidence drifted")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_bytes(payload)


if __name__ == "__main__":
    main()
