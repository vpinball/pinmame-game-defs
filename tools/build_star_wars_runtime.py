"""Rebuild compact, visually transcribed stwr_103 diagnostic evidence.

Requires the exact retained raw runs. ROM names below were read from the DMD
contact sheets; code only selects and pins their frames and controller events.
It does not recognize arbitrary DMD text or infer physical fitment from activity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from build_external_evidence_manifest import build_manifest, canonical_bytes

ROOT = Path(__file__).resolve().parents[1]
FOLDER = "star-wars-1992-curation-2026-10-22"
TARGET = ROOT / "tools/star_wars_runtime.json"
EVIDENCE = ROOT / "evidence/runtime/data-east/star-wars-stwr_103-service-tests.json"
LIBRARY_SHA = "dfcd9f9407dcb4e107d6ea066ceaccdb07333b552cd30fc1bfc491a385a4dead"
SWITCH_NAMES = (
    "PLUMB TILT", "4TH COIN", "CREDIT BUTTON", "RIGHT COIN", "CENTER COIN", "LEFT COIN", "SLAM TILT", "NOT USED",
    "NOT USED", "OUTHOLE", "TROUGH #1 LEFT", "TROUGH #2 CENTER", "TROUGH #3 RIGHT", "SHOOTER LANE", "LEFT FLIPPER", "RIGHT FLIPPER",
    "RIGHT LOOP", "MIDDLE LOOP", "LEFT LOOP", "RAMP ENTRANCE", "RIGHT OUTLANE", "RIGHT RETURN", "LEFT RETURN", "LEFT OUTLANE",
    "X-WING 1", "X-WING 2", "X-WING 3", "X-WING 4", "X-WING 5", "DROP TARGET TOP", "DROP TARGET MIDDLE", "DROP TARGET BOTTOM",
    "RIGHT SCOOP", "DEATH STAR TROUGH", "OBI-WAN TROUGH", "VUK", "LEFT SCOOP", "R2D2 ENTRANCE", "RAMP EXIT", "BAR TARGET",
    "BAR MOTOR UP", "BAR MOTOR DOWN", "LEFT SLINGSHOT", "RIGHT SLINGSHOT", "TOP TURBO BUMPER", "LEFT TURBO BUMPER", "RIGHT TURBO BUMPER", "BOTTOM TURBO BUMPER",
    "NOT USED", "SHIFT BUTTON", "SHIFT DOWN", "SHIFT UP", *(["NOT USED"] * 12),
)
LAMP_NAMES = (
    "-S-", "-T-", "-A-", "-R-", "-W-", "-A-", "-R-", "-S-",
    *[f"D.S. MOON {n}" for n in range(1, 9)], "X MODE", "EXTRA BALL", "LITE C3PO EYES", "LITE THE FORCE", "YODA", "D.S. X-WING MULT.", "D.S. TIE FIGHTER", "DEATH STAR",
    "CABINET: START BUTTON", "C3PO LEFT EYE", "C3PO MOUTH", "C3PO RIGHT EYE", "D.S. SPHERE 1", "D.S. SPHERE 2", "SHOOTER LANE", "UPPER LEFT OUTLANE",
    *[f"X-WING {n}" for n in range(1, 6)], "DROP TARGET TOP", "DROP TARGET MIDDLE", "DROP TARGET BOTTOM",
    "10 MILLION LEFT", "10 MILLION CENTER", "LARGE TIE FIGHTER", "10 MILLION RIGHT", "R2D2 WHEN LIT", "LITE LASER KICK", "LEFT SCOOP", "RIGHT SCOOP",
    "RAMP HYPER SPACE", "RAMP JACKPOT", "RAMP EMPIRE", "LIGHT SABER", "RIGHT OUTLANE", "RIGHT RETURN LANE", "LEFT RETURN LANE", "LASER KICK",
    "R2D2 DOME LEFT", "R2D2 DOME RIGHT", "VICTORY", "SPECIAL", "TOP TURBO BUMPER", "LEFT TURBO BUMPER", "RIGHT TURBO BUMPER", "BOTTOM TURBO BUMPER",
)
COIL_NAMES = {
    1: "COIL: OUTHOLE", 2: "COIL: TROUGH EJECT", 3: "COIL: BALL LAUNCHER", 4: "COIL: LEFT SCOOP KICKER", 5: "COIL: VUK", 6: "COIL: DROP TARGET", 7: "COIL: RIGHT SCOOP KICKER", 8: "COIL: KNOCKER", 9: "COIL: R2D2 DANCE",
    11: "RELAY: G.I. RELAY", 12: "RELAY: BAR TARGET", 13: "COIL: NOT USED", 14: "COIL: NOT USED", 15: "RELAY: R2D2 & D. STAR", 16: "COIL: LASERKICK",
    17: "COIL: TOP BUMPER", 18: "COIL: LEFT BUMPER", 19: "COIL: RIGHT BUMPER", 20: "COIL: BOTTOM BUMPER", 21: "COIL: LEFT SLING", 22: "COIL: RIGHT SLING",
    25: "FLASH: 1-INSERT 3-PLFD", 26: "FLASH: 3-PANEL 1-PLFD", 27: "FLASH: 2-INSERT 2-PLFD", 28: "FLASH: 4-PLFD", 29: "FLASH: 2-INSERT 2-PLFD", 30: "FLASH: 2-INSERT 2-PLFD", 31: "FLASH: 2-INSERT 2-PLFD", 32: "FLASH: 4-PLFD",
}
SWITCH_COLORS = ("BRN", "RED", "ORN", "YEL", "BLK", "BLU", "VIO", "GRY")
LAMP_COLORS = ("BRN", "RED", "ORN", "BLK", "GRN", "BLU", "VIO", "GRY")
LAMP_ROWS = ("BRN", "BLK", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")
SWITCH_ROWS = ("BRN", "RED", "ORN", "YEL", "GRN", "BLU", "VIO", "GRY")


def canonical(value) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame(snapshot: dict, root: Path) -> dict:
    display = snapshot["displays"][0]
    # Raw traces retain their original Windows paths, even on another host.
    path = root / Path(display["artifact"].replace("\\", "/")).parent.name / Path(display["artifact"].replace("\\", "/")).name
    header, pixels = path.read_bytes().split(b"\n255\n", 1)
    layout = display["layout"]
    if header != f"P5\n{layout['width']} {layout['height']}".encode("ascii") or len(pixels) != layout['width'] * layout['height']:
        raise ValueError(f"unexpected DMD PGM layout: {path}")
    maximum = (1 << layout['depth']) - 1
    raw = bytes(round(value * maximum / 255) for value in pixels)
    if display["pixel_sha256"] not in {hashlib.sha256(raw).hexdigest(), hashlib.sha256(pixels).hexdigest()}:
        raise ValueError(f"DMD pixels do not match trace digest: {path}")
    return {"path": path.relative_to(root).as_posix(), "sha256": digest(path),
            "pixel_sha256": display["pixel_sha256"], "time_s": snapshot["time_s"]}


def build(root: Path) -> dict:
    assert len(SWITCH_NAMES) == len(LAMP_NAMES) == 64
    runs = {}
    for name in ("explore-01", "switches-02", "lamps-01", "coils-01"):
        path = root / f"{name}.json"
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw["failure"] or raw["game"] != "stwr_103" or raw["library_sha256"] != LIBRARY_SHA:
            raise ValueError(f"wrong or failed native run: {name}")
        runs[name] = raw
    switch_run = runs["switches-02"]
    switches = {}
    for snapshot in switch_run["snapshots"]:
        if "(held)" not in snapshot["label"]:
            continue
        number = int(snapshot["label"].split()[1])
        switches[str(number)] = {"name": SWITCH_NAMES[number - 1] if number <= 64 else "RIGHT FLIPPER" if number == 82 else "LEFT FLIPPER",
                                 "public_active": 1, "frame": frame(snapshot, root)}
        diagnostic = number if number <= 64 else 16 if number == 82 else 15
        switches[str(number)].update({"diagnostic_number": diagnostic,
            "drive_wire": "GRN-" + SWITCH_COLORS[(diagnostic - 1) // 8],
            "return_wire": "WHT-" + SWITCH_ROWS[(diagnostic - 1) % 8]})
    if set(map(int, switches)) != {*range(1, 65), 82, 84}:
        raise ValueError("incomplete ROM-named switch run")
    lamps = {}
    for snapshot in runs["lamps-01"]["snapshots"][4:68]:
        active = snapshot["active_lamps"]
        if len(active) != 1:
            raise ValueError("single-lamp test did not select exactly one address")
        number = active[0]
        if number in map(int, lamps):
            raise ValueError("lamp test repeated an address before completing the matrix")
        lamps[str(number)] = {"name": LAMP_NAMES[number - 1], "frame": frame(snapshot, root),
            "drive_wire": "YEL-" + LAMP_COLORS[(number - 1) // 8], "return_wire": "RED-" + LAMP_ROWS[(number - 1) % 8]}
    if set(map(int, lamps)) != set(range(1, 65)):
        raise ValueError("lamp test omitted an address")
    coils = {}
    raw = runs["coils-01"]
    for event in raw["events"]:
        number = event.get("number")
        if event["event"] != "solenoid" or not event["state"] or number not in COIL_NAMES or str(number) in coils or event["time_s"] <= raw["snapshots"][5]["time_s"]:
            continue
        snapshot = next(s for s in raw["snapshots"] if s["time_s"] >= event["time_s"] + .35)
        if snapshot["time_s"] - event["time_s"] >= .8:
            raise ValueError("coil frame is outside the visually reviewed diagnostic phase")
        coils[str(number)] = {"name": COIL_NAMES[number], "event_time_s": event["time_s"], "frame": frame(snapshot, root)}
    if set(map(int, coils)) != set(COIL_NAMES):
        raise ValueError("coil test omitted a transcribed diagnostic phase")
    artifact_paths = [root / f"{name}.json" for name in runs]
    artifact_paths += [path for name in runs for path in (root / f"{name}-dmd").glob("*.pgm")]
    artifacts = [{"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}
                 for path in sorted(artifact_paths, key=lambda path: path.relative_to(root).as_posix())]
    return {
        "format": "pinmame-diagnostic-observations", "version": 1, "game": "stwr_103",
        "pinmame_revision": "97aa922bf8e4b6970126192ec1ac1fb0305a4f62", "library_sha256": LIBRARY_SHA,
        "retained_root": f"external:pinmame-review-artifacts/{FOLDER}",
        "method": "Exact visually read diagnostic title checkpoints. Switches held 1.2s, released 0.65s; lamps stepped once through all 64 addresses; automatic coil events paired with DMD frames 0.35-0.8s later. Native build independently verified against pinned source.",
        "limitations": "Observations identify CPU 1.03 / display 1.05 semantics, not hardware fitment, quantities, real motion timing or physical ROM compatibility. Harness pulse reasserts every 10ms: forced matrix 15/16 holds can reach the ROM between core rewrites and do not establish a supported flipper interface; use 84/82. Host readback is not evidence of ROM processing. Factory-unused 18/52 and lamp 17 retain software names, not physical devices.",
        "switches": switches, "lamps": lamps, "solenoids": coils,
        "artifacts": artifacts,
        "artifact_manifest_sha256": hashlib.sha256(canonical(artifacts)).hexdigest(),
        "artifact_manifest_algorithm": "All four raw JSON traces and all their DMD PGM snapshots; case-sensitive relative POSIX path order; path, bytes, full-file SHA256; canonical sorted-key indented UTF-8 JSON plus LF, as canonical() in this builder.",
        "dmd_manifests": {name: {"sha256": hashlib.sha256(canonical_bytes(build_manifest(root / f"{name}-dmd", "stwr_103")) + b"\n").hexdigest(),
                                 "algorithm": "tools/build_external_evidence_manifest.py; canonical compact sorted-key UTF-8 JSON plus LF"} for name in runs},
    }


def envelope(facts: dict, root: Path, rom_root: Path) -> dict:
    runs = {name: json.loads((root / f"{name}.json").read_text(encoding="utf-8")) for name in ("explore-01", "switches-02", "lamps-01", "coils-01")}
    snapshots = []
    for category in ("switches", "lamps", "solenoids"):
        for number, observation in facts[category].items():
            f = observation["frame"]
            run = next(raw for raw in runs.values() if any(s["time_s"] == f["time_s"] and s["displays"][0]["pixel_sha256"] == f["pixel_sha256"] for s in raw["snapshots"]))
            snapshot = next(s for s in run["snapshots"] if s["time_s"] == f["time_s"])
            snapshots.append({"label": f"{category} public {number}; {f['path']}", "display_index": 0,
                              "pixel_sha256": f["pixel_sha256"], "interpreted_text": observation["name"] +
                                  (f" | {observation['drive_wire']} {observation['return_wire']} #{observation.get('diagnostic_number', int(number)):02}" if "drive_wire" in observation else ""),
                              "active_solenoid_addresses": snapshot["active_solenoids"]})
    archive = rom_root / "stwr_103.zip"
    # Hash authorized ROM data without extracting or modifying it.
    with zipfile.ZipFile(archive) as z:
        members = [{"name": n, "sha256": hashlib.sha256(z.read(n)).hexdigest(),
                    "sha1": hashlib.sha1(z.read(n)).hexdigest(), "crc32": f"{z.getinfo(n).CRC:08x}", "bytes": z.getinfo(n).file_size}
                   for n in sorted(z.namelist()) if not n.endswith("/")]
    facts["rom_archive"] = {"name": "stwr_103.zip", "sha256": digest(archive), "members": members}
    return {"format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/build_star_wars_runtime.py", "version": 1},
        "source": {"kind": "runtime_scenario", "repository": "https://github.com/vpinball/pinmame",
            "revision": facts["pinmame_revision"], "path": "tools/star_wars_runtime.json", "sha256": hashlib.sha256(canonical(facts)).hexdigest(),
            "license": "NOASSERTION", "attribution": "Curator's LibPinMAME runs on contributor-authorized ROM; no ROM bytes redistributed", "quality": "observed"},
        "driver_ids": ["stwr_103"], "machine_ids": ["data-east.star-wars.1992"],
        "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {"game": "stwr_103", "rom_archive_sha256": digest(archive),
            "emulator": {"binary": "pinmame64.dll", "sha256": LIBRARY_SHA, "built_from_revision": facts["pinmame_revision"]},
            "raw_runs": [{"name": name, "sha256": digest(root / f"{name}.json"),
                "self_test_pulses": sum(int(step.get("pulses", 0)) for step in raw["steps"] if step["type"] == "pulse_until_display"),
                "snapshot_count": len(raw["snapshots"]), "boot_wait_s": 10,
                "nvram_initialization": "new empty isolated work directory; no inherited NVRAM"} for name, raw in runs.items()],
            "command_template": "python -B tools/star_wars_harness.py --library <pinned-native-DLL> --game stwr_103 --rom-path <authorized-read-only-ROM-root> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/data-east/stwr-103-<switches|lamps|coils>.json --boot-wait 10 --dmd-dir <retained-DMD-folder> --output <retained-run.json>. Exploratory title discovery uses the retained count-based scenario only; final diagnostic runs require exact visually read title masks. See tools/star_wars_runtime.json for raw-file/frame pins and limitations.",
            "observations": {"diagnostic_snapshots": snapshots, "lamp_addresses_seen": sorted({e['number'] for raw in runs.values() for e in raw['events'] if e['event']=='lamp' and e['state']}),
                "solenoid_addresses_seen": sorted({e['number'] for raw in runs.values() for e in raw['events'] if e['event']=='solenoid' and e['state']}),
                "gi_addresses_seen": [], "display_indices_seen": [0], "service_language": "English"}}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--rom-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.review_root / FOLDER
    facts = build(root)
    evidence = envelope(facts, root, args.rom_root)
    for path, data in ((TARGET, canonical(facts)), (EVIDENCE, canonical(evidence))):
        if args.check:
            if path.read_bytes().replace(b"\r\n", b"\n") != data:
                raise SystemExit(f"runtime evidence drift: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
