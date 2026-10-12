"""Derive the pinned Star Wars (Data East 1992) geometry table from the retained vpxtool extraction.

Reads the retained VPW v1.2.2 extraction (never a different table), takes the exact object each
placement names through the embedded script's own bindings, and writes tools/star_wars_geometry.json:
file, SHA-256, object type, method, raw and normalized position. Normalization is x = raw_x / right
and y = raw_y / bottom of the table bounds (x = 0 left, y = 0 rear). The three baked-mesh anchors
(DeathStar, DSDoor, R2Head) are located by the centre of their world-space mesh bounds in the
companion `vpxtool export obj --units vpu` export (obj x = playfield x, obj y = playfield depth,
obj z = height), never by a primitive position taken on trust.

    python tools/build_star_wars_geometry.py <extraction-dir> --obj <obj-export-dir>           # rewrite the JSON
    python tools/build_star_wars_geometry.py <extraction-dir> --obj <obj-export-dir> --check   # refuse drift
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "star_wars_geometry.json"
TABLE_SHA256 = "ea240a0193d6f3d829fdd0c416d18b8dbe733ce5ad4bbefcb4b17b481b9d11ca"
SCRIPT_SHA256 = "1d5252b9ef7d1d00646df732661a07b384d6d5cb14798ff86337a00de1c7d144"

# Switch address -> the object the embedded script's Hit/UnHit/Controller.Switch code binds.
# Cited line numbers are in the retained embedded script (script.vbs, sha256 above).
SWITCH_OBJECTS = {
    10: ("Kicker", "BallRelease"), 11: ("Kicker", "BallRelease"),
    12: ("Kicker", "BallRelease"), 13: ("Kicker", "BallRelease"),  # bsTrough InitSwitches/InitExit, 180-186
    14: ("Trigger", "sw14"),  # InitImpulseP sw14, 190-192
    17: ("Trigger", "sw17"),  # sw17_hit pulse, 819
    19: ("Gate", "sw19"),  # sw19_hit pulse, 820
    20: ("Gate", "sw20"),  # sw20_hit pulse + WireRampOn, 822
    21: ("Trigger", "sw21"), 22: ("Trigger", "sw22"), 23: ("Trigger", "sw23"), 24: ("Trigger", "Sw24"),  # 826-833
    25: ("HitTarget", "sw25"), 26: ("HitTarget", "sw26"), 27: ("HitTarget", "sw27"),
    28: ("HitTarget", "sw28"), 29: ("HitTarget", "sw29"),  # STHit, 839-843
    30: ("Wall", "sw30"), 31: ("Wall", "sw31"), 32: ("Wall", "sw32"),  # DTHit, 849-851
    33: ("Kicker", "sw33"),  # SolRightEject.InitSaucer sw33, 229-232
    34: ("Kicker", "deathstarIn"),  # deathstarIn_Hit pulses 34, 253-256
    35: ("Kicker", "r2In"),  # r2In_Hit pulses 35, 241-245
    36: ("Kicker", "sw36"),  # sw36_Hit + SolLeftPopper kicks sw36, 257-277
    37: ("Kicker", "sw37"),  # SolLeftEject.InitSaucer sw37, 235-238
    38: ("Trigger", "sw38"),  # 873-874
    39: ("Trigger", "sw39"),  # delayed ramp-exit pulse, 875
    40: ("HitTarget", "sw40"),  # door bar blocks sw40, 297-300
    41: ("Mesh", "DSDoor"), 42: ("Mesh", "DSDoor"),  # mechDeathStarDoor .AddSw 41, 42, 206-216
    43: ("Wall", "LeftSlingShot"), 44: ("Wall", "RightSlingShot"),  # slingshot handlers, 442-468
    45: ("Bumper", "Bumper1"), 46: ("Bumper", "Bumper2"), 47: ("Bumper", "Bumper3"), 48: ("Bumper", "Bumper4"),  # 885-916
}
# Coil effect anchors (the mechanism object the coil acts on, never a winding centre).
COIL_OBJECTS = {
    1: ("Kicker", "BallRelease"), 2: ("Kicker", "BallRelease"),  # bsTrough SolIn/SolOut, 481-482, 515-526
    3: ("Plunger", "Plunger"),  # SolAutoPlungerIM fires the shooter-lane plunger, 483, 541-546
    4: ("Kicker", "sw37"), 7: ("Kicker", "sw33"),  # SolCallback SolLeftEject/SolRightEject, 484, 487
    5: ("Kicker", "sw36"),  # SolLeftPopper kicks the Death Star VUK, 485, 267-277
    6: ("Wall", "sw31"),  # ResetDrops acts on the drop bank (wall sw30/sw31/sw32; sw31 is its middle target), 486
    9: ("Mesh", "R2Head"),  # SolR2 raises R2Head/R2Body, 488, 339-352
    12: ("Mesh", "DSDoor"),  # mechDeathStarDoor .Sol1 = 12, 206-216
    15: ("Mesh", "DeathStar"),  # mechDeathStar .Sol1 = 15 rotates the toy, 218-224
    16: ("Plunger", "KickBack"),  # SolKickback Fire/PullBack, 494, 528-534
    17: ("Bumper", "Bumper1"), 18: ("Bumper", "Bumper2"), 19: ("Bumper", "Bumper3"), 20: ("Bumper", "Bumper4"),  # 495-498
    21: ("Wall", "LeftSlingShot"), 22: ("Wall", "RightSlingShot"),  # 499-500
    46: ("Flipper", "RightFlipper"), 48: ("Flipper", "LeftFlipper"),  # SolCallback sLRFlipper/sLLFlipper, 511-512
}
# Lamp address -> the script-driven Light/Flasher objects that are the bulbs themselves
# (Lampz.MassAssign in InitLampsNF, 967-1160). Insert plastics named by Lampz.Callback
# (p1..p60, BumperCapN, pf4/pf8, JabbasInsert) are lighting targets, not bulbs.
LAMP_LIGHTS = {
    1: ("l1",), 2: ("l2",), 3: ("l3",), 4: ("l4",), 5: ("l5",), 6: ("l6",), 7: ("l7",), 8: ("l8",),
    9: ("l9",), 10: ("l10",), 11: ("l11",), 12: ("l12",), 13: ("l13",), 14: ("l14",), 15: ("l15",), 16: ("l16",),
    18: ("l18",), 19: ("l19",), 20: ("l20",), 21: ("l21",), 22: ("l22",), 23: ("l23",), 24: ("l24f",),
    26: ("l26",), 27: ("l27",), 28: ("l28",),
    31: ("l31",), 32: ("l32",), 33: ("l33",), 34: ("l34",), 35: ("l35",), 36: ("l36",), 37: ("l37",),
    38: ("l38",), 39: ("l39",), 40: ("l40",),
    41: ("l41",), 42: ("l42",), 43: ("l43",), 44: ("l44",),
    45: ("l45",), 46: ("l46",), 47: ("l47",),
    49: ("l49", "l49a"), 50: ("l50", "l50a"), 51: ("l51", "l51a"),
    52: ("l52",), 53: ("l53",), 54: ("l54",), 55: ("l55",), 56: ("l56",),
    57: ("l57",), 58: ("l58",), 59: ("l59",), 60: ("l60",),
    61: ("l61",), 62: ("l62",), 63: ("l63",), 64: ("l64",),
}
# The GI channel (Lampz.obj(111) = ColtoArray(GI), 1158) drives the GI collection's
# seventeen playfield bulb Lights (collections.json, collection "GI").
GI_LIGHTS = ("Light1", "Light2", "Light3", "Light4", "Light5", "Light6", "Light7", "Light8",
             "Light9", "Light10", "Light11", "Light001", "Light002", "Light003", "Light004",
             "Light005", "Light006")
# Flash-lamp bank (public solenoid 25-32, lamp channel 125-132) -> the Light/Flasher objects the
# script's SolCallback/MassAssign drives. Banks 5R (129) and 7R (131) have their MassAssign lines
# commented out in the retained script: the table models no bulbs for them.
FLASHER_LIGHTS = {
    25: ("f125a_u", "f125a_l", "f125b_u", "f125b_l", "f125c_u", "f125c_l", "f125d", "f125e"),
    26: ("f126a", "f126b", "f2r"),
    27: ("f3r_a", "f3r_b"),
    28: ("f128a", "f128b", "f128c", "f128d_u", "f128d_l", "f4r_a", "f4r_af", "f4r_b", "f4r_bf", "f4r_c", "f4r_cf"),
    30: ("f6r_a", "f6r_b"),
    32: ("F132a", "f132b", "F132c", "F132d_l", "F132d_u", "F132e_l", "F132e_u", "f8r_a", "f8r_b", "f8rf"),
}
# Objects whose stored position is not trusted: world-space mesh bounds decide them.
MESH_OBJECTS = ("DeathStar", "DSDoor", "R2Head")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def polygon_centroid(points: list[dict]) -> tuple[float, float]:
    """Signed shoelace area centroid of a wall's (or flasher's) drag points."""
    area = cx = cy = 0.0
    for a, b in zip(points, points[1:] + points[:1]):
        cross = a["x"] * b["y"] - b["x"] * a["y"]
        area += cross
        cx += (a["x"] + b["x"]) * cross
        cy += (a["y"] + b["y"]) * cross
    if abs(area) < 1e-9:
        raise ValueError("degenerate polygon")
    return cx / (3 * area), cy / (3 * area)


def mesh_centres(obj_dir: Path) -> dict[str, tuple[str, tuple[float, float]]]:
    """Centre of each named object's world-space bounds in the vpxtool obj export.

    The exporter writes playfield x to obj x, playfield depth to obj y and height to obj z.
    """
    (obj_file,) = [path for path in obj_dir.iterdir() if path.suffix == ".obj"]
    bounds: dict[str, list[float]] = {}
    group = "pre"
    for line in obj_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("o "):
            group = line[2:].strip()
        elif line.startswith("v ") and group in MESH_OBJECTS:
            x, y, z = (float(token) for token in line.split()[1:4])
            box = bounds.setdefault(group, [x, y, x, y])
            box[0], box[1] = min(box[0], x), min(box[1], y)
            box[2], box[3] = max(box[2], x), max(box[3], y)
    centres = {}
    for name, (x0, y0, x1, y1) in bounds.items():
        centres[name] = ("mesh_world_bounds", ((x0 + x1) / 2, (y0 + y1) / 2))
    missing = [name for name in MESH_OBJECTS if name not in centres]
    if missing:
        raise ValueError(f"mesh anchors absent from obj export: {missing}")
    return centres


def build(extraction: Path, obj_dir: Path) -> dict:
    items = extraction / "gameitems"
    bounds_source = load(extraction / "gamedata.json")
    left, top = bounds_source["left"], bounds_source["top"]
    right, bottom = bounds_source["right"], bounds_source["bottom"]
    objects: dict[str, dict] = {}
    mesh = mesh_centres(obj_dir)
    # The script names objects case-insensitively (VBScript); the extraction keeps the table's own case.
    actual = {path.name.lower(): path for path in items.iterdir()}

    def kind_of(name: str) -> str:
        for kind in ("Light", "Flasher"):
            if f"{kind}.{name}.json".lower() in actual:
                return kind
        raise KeyError(name)

    def find(kind: str, name: str) -> Path:
        return actual[f"{kind}.{name}.json".lower()]

    def take(kind: str, name: str) -> None:
        if name in objects:
            return
        if kind == "Mesh":
            method, (x, y) = mesh[name]
            objects[name] = {
                "file": f"obj-export/{obj_file_name(obj_dir)}", "sha256": obj_sha256(obj_dir),
                "type": "Primitive", "method": method, "raw_xy": [round(x, 5), round(y, 5)],
                "xy": [round((x - left) / (right - left), 6), round((y - top) / (bottom - top), 6)],
            }
            return
        path = find(kind, name)
        data = load(path)[kind]
        if kind in {"Wall", "Flasher"}:
            method, (x, y) = "polygon_area_centroid", polygon_centroid(data["drag_points"])
        elif kind == "HitTarget":
            method, (x, y) = "object_position", (data["position"]["x"], data["position"]["y"])
        else:
            method, (x, y) = "object_center", (data["center"]["x"], data["center"]["y"])
        objects[name] = {
            "file": f"gameitems/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "type": kind, "method": method, "raw_xy": [round(x, 5), round(y, 5)],
            "xy": [round((x - left) / (right - left), 6), round((y - top) / (bottom - top), 6)],
        }

    for table in (SWITCH_OBJECTS, COIL_OBJECTS):
        for kind, name in table.values():
            take(kind, name)
    for names in (*LAMP_LIGHTS.values(), *FLASHER_LIGHTS.values(), GI_LIGHTS):
        for name in names:
            take(kind_of(name), name)
    return {
        "bounds": [left, top, right, bottom],
        "table_sha256": TABLE_SHA256, "script_sha256": SCRIPT_SHA256,
        "switches": {str(n): f"{kind}.{name}" for n, (kind, name) in sorted(SWITCH_OBJECTS.items())},
        "coils": {str(n): f"{kind}.{name}" for n, (kind, name) in sorted(COIL_OBJECTS.items())},
        "lamps": {str(n): list(names) for n, names in sorted(LAMP_LIGHTS.items())},
        "gi": list(GI_LIGHTS),
        "flashers": {str(n): list(names) for n, names in sorted(FLASHER_LIGHTS.items())},
        "objects": dict(sorted(objects.items())),
    }


def obj_file_name(obj_dir: Path) -> str:
    return next(path.name for path in obj_dir.iterdir() if path.suffix == ".obj")


def obj_sha256(obj_dir: Path) -> str:
    return hashlib.sha256((obj_dir / obj_file_name(obj_dir)).read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraction", type=Path)
    parser.add_argument("--obj", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    script = args.extraction / "script.vbs"
    if hashlib.sha256(script.read_bytes()).hexdigest() != SCRIPT_SHA256:
        raise SystemExit("not the retained VPW v1.2.2 extraction")
    payload = (json.dumps(build(args.extraction, args.obj), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise SystemExit("geometry drift")
        print("geometry matches")
    else:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
