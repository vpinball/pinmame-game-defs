"""Recompute Mary Shelley's Frankenstein's observed placements from its exact retained VPX extraction.

Only script-linked physical objects with a stored centre are selected: triggers, hit targets,
kickers, bumpers, spinners, the plunger, lights, and the drag-point means of the slingshot walls and
the diverter ramp. No primitive is used, so no mesh export is needed. Flasher sprites, reflection
helper lights, cabinet primitives and primitive origins are excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
TABLE_NAME = "Mary Shelley's Frankenstein (Sega 1995) v1.2.vpx"
TABLE_SHA = "6f254182c77934f6a62fb02f675578532a40d14b87902a2944d1ba56280c3d2c"
MANIFEST_SHA = "445c14af3a52b3f3039f59cc54fe617919e4654660a8a858781b080a52b499c2"
SCRIPT_SHA = "53f8c80ad721dd92916c0d318decf95b4c4434c94a3c0efa3648b87f332fe571"
WIDTH, HEIGHT = 952, 2080

SWITCH_OBJECTS = {
    15: "BallRelease", 41: "Bumper13", 42: "Bumper14", 43: "Bumper15", 44: "Bumper16",
    47: "LeftSlingshot", 48: "RightSlingshot",
    **{n: f"sw{n}" for n in (16, *range(17, 30), 31, 32, *range(33, 41), 45, 46, 53, 54, 55, 56)},
}
COIL_OBJECTS = {
    1: ["BallLockout"], 2: ["BallRelease"], 3: ["AutoPlunger"], 4: ["sw32"], 5: ["sw31"], 6: ["kIceCave"],
    7: ["kVUK"], 9: ["trUpperRampTrap1"], 12: ["trUpperRampTrap2"], 13: ["kFrankRightHand", "kFrankLeftHand"],
    14: ["rDiverter"], 16: ["Kickback"], 17: ["Bumper13"], 18: ["Bumper14"], 19: ["Bumper15"], 20: ["Bumper16"],
    21: ["LeftSlingshot"], 22: ["RightSlingshot"],
}
# Script flasher index (SolCallback(n) = "SolFlasher i, ") -> public output.
FLASHER_INDEX = {0: 15, 1: 25, 2: 26, 3: 27, 4: 28, 5: 29, 6: 30, 7: 31}
# Lamps the LampTimer drives through named objects rather than the InsertLights collection.
SPECIAL_LAMPS = {13: "lBumper13", 14: "lBumper14", 15: "lBumper15", 16: "lBumper16",
                 29: "lPlasticBulb29", 30: "lPlasticBulb30", 48: "lPlasticBulb48", 56: "lPlasticBulb56"}
# l40 is the lamp-40 socket beside l40a, but the table gives it TimerInterval 39 (see the curator).
MISBOUND = {"l40": 40}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def script_flashers(script: str) -> dict[int, list[str]]:
    """The aFlasherLight array, one list of light names per SolFlasher index."""
    body = script.split("Dim aFlasherLight", 1)[1].split("Dim aFlasherValue", 1)[0]
    groups = re.findall(r"Array\(((?:lFlasher\w+,?\s*)+)\)", body)
    if len(groups) != 8:
        raise ValueError("Frankenstein aFlasherLight array changed")
    return {i: [n.strip() for n in g.split(",")] for i, g in enumerate(groups)}


def build(vpx_root: Path) -> dict:
    base = vpx_root / "sega/mary-shelley-s-frankenstein-1995"
    extraction = base / "extracted-vpxtool"
    if sha(base / TABLE_NAME) != TABLE_SHA:
        raise ValueError("Frankenstein retained VPX differs from the admitted source")
    if check_manifest(extraction, "frankst") != MANIFEST_SHA or sha(extraction / "script.vbs") != SCRIPT_SHA:
        raise ValueError("Frankenstein extraction differs from the admitted source")
    objects = {}
    for path in (extraction / "gameitems").glob("*.json"):
        kind, data = next(iter(json.loads(path.read_text(encoding="utf-8")).items()))
        objects[data["name"]] = (kind, data, path)
    game = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
    if tuple(game[n] for n in ("left", "top", "right", "bottom")) != (0, 0, WIDTH, HEIGHT):
        raise ValueError("Frankenstein table bounds changed")
    collections = {c["name"]: c["items"] for c in json.loads((extraction / "collections.json").read_text(encoding="utf-8"))}
    script = (extraction / "script.vbs").read_text(encoding="utf-8", errors="replace")

    def point(name):
        kind, data, path = objects[name]
        if kind in ("Flasher", "Primitive") or data.get("is_backglass"):
            raise ValueError(f"not a physical playfield anchor: {name}")
        if kind in ("Wall", "Ramp"):
            points = data["drag_points"]
            x = sum(p["x"] for p in points) / len(points)
            y = sum(p["y"] for p in points) / len(points)
            method = f"mean of the {kind.lower()}'s drag points"
        else:
            centre = data.get("center") or data.get("position")
            if centre is None:
                raise ValueError(f"no exact centre for {name}")
            x, y = centre["x"], centre["y"]
            method = "stored physical object centre/pivot"
        if not (0 <= x <= WIDTH and 0 <= y <= HEIGHT):
            raise ValueError(f"out-of-bounds anchor: {name} ({x},{y})")
        return {"object": name, "type": kind, "path": path.relative_to(extraction).as_posix(), "sha256": sha(path),
                "raw_x": x, "raw_y": y, "method": method, "x": round(x / WIDTH, 6), "y": round(y / HEIGHT, 6)}

    placements = {}
    for n, name in SWITCH_OBJECTS.items():
        placements[f"switch.{n}"] = [point(name)]
    for n, names in COIL_OBJECTS.items():
        placements[f"solenoid.{n}"] = [point(name) for name in names]
    for index, names in script_flashers(script).items():
        # One placement per socket: the lights of one socket share a letter (Ab..Az, Ba, ...).
        sockets = {}
        for name in names:
            sockets.setdefault(re.fullmatch(r"lFlasher\d+([A-Z])[a-z]", name).group(1), name)
        placements[f"solenoid.{FLASHER_INDEX[index]}"] = [point(sockets[k]) for k in sorted(sockets)]
    lamps = {}
    for name in collections["InsertLights"]:
        kind, data, _ = objects[name]
        if kind != "Light" or name.endswith("a"):
            continue
        lamps.setdefault(MISBOUND.get(name, data["timer_interval"]), []).append(name)
    if any(len(v) != 1 for v in lamps.values()) or set(lamps) & set(SPECIAL_LAMPS):
        raise ValueError(f"Frankenstein insert lights are not one per lamp: {lamps}")
    for n, name in {**{k: v[0] for k, v in lamps.items()}, **SPECIAL_LAMPS}.items():
        placements[f"lamp.{n}"] = [point(name)]
    placements["solenoid.11"] = [point(name) for name in collections["GIBulbs"]]
    return {"table_bounds": {"left": 0, "top": 0, "right": WIDTH, "bottom": HEIGHT},
            "table_sha256": TABLE_SHA, "script_sha256": SCRIPT_SHA, "manifest_sha256": MANIFEST_SHA,
            "placements": dict(sorted(placements.items(), key=lambda kv: (kv[0].split(".")[0], int(kv[0].split(".")[1])))),
            "mechanical_anchors": {name: point(name) for name in ("LeftFlipper", "RightFlipper", "RightUpperFlipper", "Drain")},
            "omitted": ("Trough switches 9-14 have no table object: a cvpmBallStack (InitSw 0,14,13,12,11,10,9,0) "
                        "stands in for them. Lamps 31 and 32 are drawn only by the Flasher sprites fPlasticBulb31/32 "
                        "and share the light lPlasticBulb30, so no object stands for their sockets. The creature head "
                        "servo and the knocker have no playfield object; the head primitive is a render object."),
            "rejected": ["All VPX Flasher objects (fPlasticBulb* glow sprites and the flasher-dome sprites)",
                         "Reflection helper lights whose names end in 'a' (the script scales them with EnableReflectionsAtBall)",
                         "Repeated lights of one flasher socket (lFlasher<n><letter>b..z): one placement per socket letter",
                         "Primitives (flasher domes, bumper caps, the creature head, body and arms, trap doors, hammers) and their position fields",
                         "The sw31e/sw32e/sw31s/sw32s helper triggers that steer the scoop kick and sound"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vpx-root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = (json.dumps(build(args.vpx_root), indent=2, sort_keys=True) + "\n").encode()
    path = ROOT / "tools/frankenstein_places.json"
    if args.check:
        if path.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise ValueError("Frankenstein placements drifted")
    else:
        path.write_bytes(payload)


if __name__ == "__main__":
    main()
