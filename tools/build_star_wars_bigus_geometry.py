"""Derive the pinned Star Wars (Data East 1992) geometry of the retained Bigus 3.0 mod table.

The Bigus 3.0 table is a second, scriptwise-independent factory-layout table: its embedded
script is the JPSalas lineage (header lines 1-8, sha256 below), not the retained VPW v1.2.2
script, and its own bounds (0,0,1024,2102) normalize its coordinates. This builder reads the
retained Bigus extraction (never a different table), takes the exact object each placement
names through the Bigus script's own bindings, and writes tools/star_wars_bigus_geometry.json:
file, SHA-256, object type, method, raw and normalized position. Normalization is
x = (raw_x - left) / (right - left) and y = (raw_y - top) / (bottom - top) of the Bigus bounds.

Addresses the Bigus script does not bind are listed, not guessed: sw40 has a handler whose
object is absent from the table (345); coil 12 has a defined BarUpdate sub no callback wires
(434-436); lamps 48-51 name lights the table does not contain (601-604); lamp 57 is driven as
the R2-head plastic's image swap (FadePR2, 648-660), which is a lighting target, not a bulb.

    python tools/build_star_wars_bigus_geometry.py <extraction-dir> --primary tools/star_wars_geometry.json          # rewrite the JSON
    python tools/build_star_wars_bigus_geometry.py <extraction-dir> --primary tools/star_wars_geometry.json --check   # refuse drift
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "star_wars_bigus_geometry.json"
TABLE_SHA256 = "5057ffe49defd5821c6c5be6b3f5823f9c7cc246572d87ef249c224bf81d832c"
SCRIPT_SHA256 = "8ca2f5fad6d7337114c61f2023478104d7999d653356fe6b9eb0d1ab35d48809"

# Switch address -> the object the Bigus embedded script binds (script.vbs, sha256 above).
SWITCH_OBJECTS = {
    10: ("Kicker", "Ballrelease"), 11: ("Kicker", "Ballrelease"),
    12: ("Kicker", "Ballrelease"), 13: ("Kicker", "Ballrelease"),  # bsTrough InitSw/InitKick Ballrelease, 79-80
    14: ("Trigger", "sw14"),  # sw14_Hit/UnHit, 313-314
    17: ("Trigger", "sw17"),  # 316-317
    19: ("Trigger", "sw19"), 20: ("Trigger", "sw20"),  # 319-323
    21: ("Trigger", "sw21"), 22: ("Trigger", "sw22"), 23: ("Trigger", "sw23"), 24: ("Trigger", "sw24"),  # 304-314
    25: ("HitTarget", "sw25"), 26: ("HitTarget", "sw26"), 27: ("HitTarget", "sw27"),
    28: ("HitTarget", "sw28"), 29: ("HitTarget", "sw29"),  # sw25..29_Hit PulseSw, 340-344
    30: ("Wall", "sw30"), 31: ("Wall", "sw31"), 32: ("Wall", "sw32"),  # dtbank.initdrop array(sw32,sw31,sw30), 118; sw30..32_Hit, 335-337
    33: ("Kicker", "sw33"),  # bsR InitSw 33/InitKick sw33, 101-107; sw33_Hit, 285
    34: ("Kicker", "sw34"),  # sw34_Hit PulseSwitch 34, 253
    35: ("Kicker", "sw35"),  # sw35_Hit PulseSwitch 35, 255
    36: ("Kicker", "sw36"),  # bsVUK InitSw 36/InitKick sw36, 113-117; sw36a popper kick, 257
    37: ("Kicker", "sw37"),  # bsL InitSw 37/InitKick sw37, 89-95; sw37_Hit, 267
    38: ("Trigger", "sw38"), 39: ("Trigger", "sw39"),  # 326-332
    41: ("Primitive", "PrBar"), 42: ("Primitive", "PrBar"),  # bar13_Timer drives Controller.Switch(41/42) from PrBar.z, 444-457
    43: ("Wall", "LeftSlingshot"), 44: ("Wall", "RightSlingshot"),  # slingshot handlers PulseSw 43/44, 214-228
    45: ("Bumper", "Bumper1"), 46: ("Bumper", "Bumper2"), 47: ("Bumper", "Bumper3"), 48: ("Bumper", "Bumper4"),  # BumperN_Hit PulseSw 45-48, 242-245
}
# Coil effect anchors (the mechanism object the coil acts on, never a winding centre).
COIL_OBJECTS = {
    1: ("Kicker", "Ballrelease"), 2: ("Kicker", "Ballrelease"),  # bsTrough SolIn/SolOut, 354-355
    3: ("Plunger", "Plunger"),  # vpmSolAutoPlunger Plunger, 356
    4: ("Kicker", "sw37"),  # bsL.SolOut, 357
    5: ("Kicker", "sw36"),  # bsVUK.SolOut, 358
    6: ("Wall", "sw31"),  # dtBank.SolDropUp acts on the drop bank (sw30/sw31/sw32; sw31 is its middle target), 359
    7: ("Kicker", "sw33"),  # bsR.SolOut, 360
    9: ("Primitive", "PrR2D2Head"),  # SolR2D2 moves PrR2D2/PrR2D2Head, 362, 379-385
    15: ("Primitive", "PrDS"),  # the Death Star spin timer rotates PrDS (TiR2Head_Timer body), 404-410
    16: ("Plunger", "KickBack"),  # vpmSolAutoPlunger Kickback, 367
    17: ("Bumper", "Bumper1"), 18: ("Bumper", "Bumper2"), 19: ("Bumper", "Bumper3"), 20: ("Bumper", "Bumper4"),  # jet rings driven with the bumper objects (BumperN_Hit, 242-245)
    21: ("Wall", "LeftSlingshot"), 22: ("Wall", "RightSlingshot"),  # slingshot handlers, 214-228
    46: ("Flipper", "RightFlipper"), 48: ("Flipper", "LeftFlipper"),  # SolCallback sLRFlipper/sLLFlipper, 464-465
}
# Lamp address -> the script-driven Light object the UpdateLamps fades (script.vbs 519-612).
# lNa members are render doubles collapsed to the member UpdateLamps fades first.
# 57 names the R2-head plastic image swap (FadePR2), not a bulb: unbound, see module docstring.
LAMP_LIGHTS = {
    1: ("l1",), 2: ("l2",), 3: ("l3",), 4: ("l4",), 5: ("l5",), 6: ("l6",), 7: ("l7",), 8: ("l8",),
    9: ("l9",), 10: ("l10",), 11: ("l11",), 12: ("l12",), 13: ("l13",), 14: ("l14",), 15: ("l15",), 16: ("l16",),
    18: ("l18",), 19: ("l19",), 20: ("l20",), 21: ("l21",), 22: ("l22",), 23: ("l23",), 24: ("l24",),
    26: ("l26",), 27: ("l27",), 28: ("l28",),
    31: ("L31",), 32: ("l32",), 33: ("l33",), 34: ("l34",), 35: ("l35",), 36: ("l36",), 37: ("l37",),
    41: ("l41",), 42: ("l42",), 43: ("l43",), 44: ("l44",),
    45: ("l45",), 46: ("l46",), 47: ("l47c",),
    52: ("l52",), 53: ("l53",), 54: ("l54",), 55: ("l55",), 56: ("l56",),
    58: ("l58",), 59: ("l59",), 60: ("l60",),
    61: ("BL1",), 62: ("BL2",), 63: ("BL3",), 64: ("BL4",),
}
# GI: `for each xx in GI` drives the GI collection's sixteen bulb Lights (610-624;
# collections.json collection "GI"). Sixteen against the VPW table's seventeen: disclosed.
GI_LIGHTS = tuple(f"Light{i:03d}" for i in range(1, 17))
# Flash-lamp bank (public solenoid 25-32, lamp channel 125-132) -> the Light the UpdateLamps
# flash block drives as flasher N = channel - 124 = JP FlashState number - 65 (519-543):
# 66->f1, 67->f2a, 68->l24, 69->f4a, 70->l29, 71->f6a, 72->l58, 73->f8a.
# Channels 129 (bank 29) and 131 (bank 31) ARE bound here, on l29 and l58 - the VPW table
# comments its MassAssign lines for those two banks out.
FLASHER_LIGHTS = {
    25: ("f1",), 26: ("f2a",), 27: ("l24",), 28: ("f4a",),
    29: ("L29",), 30: ("f6a",), 31: ("L58",), 32: ("f8a",),
}

UNBOUND = {
    "switch_40": "handler Sub sw40_Hit (345) names an object the table does not contain",
    "coil_12": "BarUpdate sub (434-436) is defined; no SolCallback wires it",
    "lamps_38_40": "UpdateLamps fades 38/39/40 via FadeDisableLighting l38/l39/l40 (579-581): insert-plastic lighting targets, no bulb objects",
    "lamps_48_51": "UpdateLamps names l48/l49/l50/l51 (590-593); the table contains none of them",
    "lamp_57": "FadePR2 57 (599, sub 648-660) drives the PrR2D2Head plastic's image: a lighting target, not a bulb",
}

# Frame fit: the two tables normalize against their own bounds, and bounds include shooter lane
# and furniture, so raw normalized coordinates are not comparable. Fit an affine mapping the
# Bigus-normalized space onto the VPW-normalized space from script-bound mechanism objects only
# (kickers, triggers, hit targets, drop walls, slingshot walls, bumpers, plunger, kickback,
# flippers; the conversion-kit toys PrBar/PrDS/PrR2D2Head are excluded), least squares with
# iterative rejection of controls above 0.04 residual. Lamps and flashers are never controls:
# they are the held-out validation of the fit (a fit checked on its own controls is circular).
FRAME_MAX_CONTROL_RESIDUAL = 0.04
FRAME_EXCLUDE = ("deathstar", "r2", "dsdoor", "pr", "bar")


def _solve_affine(pts: list[tuple[list[float], list[float]]]) -> list[float]:
    rows: list[list[float]] = []
    rhs: list[float] = []
    for (bx, by), (vx, vy) in pts:
        rows.append([bx, by, 1, 0, 0, 0]); rhs.append(vx)
        rows.append([0, 0, 0, bx, by, 1]); rhs.append(vy)
    size = 6
    normal = [[0.0] * size for _ in range(size)]
    base = [0.0] * size
    for row, value in zip(rows, rhs):
        for i in range(size):
            base[i] += row[i] * value
            for j in range(size):
                normal[i][j] += row[i] * row[j]
    for i in range(size):
        pivot = max(range(i, size), key=lambda r: abs(normal[r][i]))
        normal[i], normal[pivot] = normal[pivot], normal[i]
        base[i], base[pivot] = base[pivot], base[i]
        for r in range(size):
            if r != i and normal[i][i]:
                factor = normal[r][i] / normal[i][i]
                for c in range(size):
                    normal[r][c] -= factor * normal[i][c]
                base[r] -= factor * base[i]
    return [base[i] / normal[i][i] for i in range(size)]


def frame_fit(primary_objects: dict, bigus_objects: dict,
             switches: dict, coils: dict) -> dict:
    import math

    def nm(value: str) -> str:
        return value.split(".", 1)[1] if "." in value else value

    controls: list[tuple[str, str, list[float], list[float]]] = []
    seen: set[tuple[float, float]] = set()
    for section in (switches, coils):
        for address, value in section.items():
            name = nm(value)
            primary = primary_objects.get(name)
            if primary is None or name not in bigus_objects:
                continue
            if any(token in name.lower() for token in FRAME_EXCLUDE):
                continue
            key = (bigus_objects[name]["xy"][0], bigus_objects[name]["xy"][1])
            if key in seen:
                continue
            seen.add(key)
            controls.append((address, name, bigus_objects[name]["xy"], primary["xy"]))
    kept = controls[:]
    dropped: list[dict] = []
    for _ in range(6):
        affine = _solve_affine([(p, v) for _, _, p, v in kept])
        residuals = [math.dist([affine[0] * p[0] + affine[1] * p[1] + affine[2],
                                affine[3] * p[0] + affine[4] * p[1] + affine[5]], v)
                     for _, _, p, v in kept]
        rejects = [i for i, r in enumerate(residuals) if r > FRAME_MAX_CONTROL_RESIDUAL]
        if not rejects:
            break
        for i in rejects:
            dropped.append({"address": kept[i][0], "object": kept[i][1], "residual": round(residuals[i], 4)})
        kept = [c for i, c in enumerate(kept) if i not in set(rejects)]
    affine = [round(value, 6) for value in _solve_affine([(p, v) for _, _, p, v in kept])]
    residuals = [math.dist([affine[0] * p[0] + affine[1] * p[1] + affine[2],
                            affine[3] * p[0] + affine[4] * p[1] + affine[5]], v)
                 for _, _, p, v in kept]
    return {
        "affine": affine,
        "control_extent": [min(p[0] for _, _, p, _ in kept), max(p[0] for _, _, p, _ in kept),
                           min(p[1] for _, _, p, _ in kept), max(p[1] for _, _, p, _ in kept)],
        "controls": {address: {"object": name, "residual": round(r, 4)}
                     for (address, name, _, _), r in zip(kept, residuals)},
        "dropped": sorted(dropped, key=lambda d: int(d["address"])),
        "method": "least-squares affine (Bigus-normalized -> VPW-normalized) on script-bound "
                  "mechanism objects, iterative rejection above 0.04; lamps and flashers are "
                  "held out of the fit and validate it",
        "residual_max": round(max(residuals), 4),
        "residual_mean": round(sum(residuals) / len(residuals), 4),
    }


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def polygon_centroid(points: list[dict]) -> tuple[float, float]:
    area = cx = cy = 0.0
    for a, b in zip(points, points[1:] + points[:1]):
        cross = a["x"] * b["y"] - b["x"] * a["y"]
        area += cross
        cx += (a["x"] + b["x"]) * cross
        cy += (a["y"] + b["y"]) * cross
    if abs(area) < 1e-9:
        raise ValueError("degenerate polygon")
    return cx / (3 * area), cy / (3 * area)


def build(extraction: Path, primary_geometry: Path) -> dict:
    primary_objects = json.loads(primary_geometry.read_text(encoding="utf-8"))["objects"]
    items = extraction / "gameitems"
    bounds_source = load(extraction / "gamedata.json")
    left, top = bounds_source["left"], bounds_source["top"]
    right, bottom = bounds_source["right"], bounds_source["bottom"]
    # VBScript names objects case-insensitively; the extraction keeps the table's own case.
    actual = {path.name.lower(): path for path in items.iterdir()}
    objects: dict[str, dict] = {}

    def find(kind: str, name: str) -> Path:
        key = f"{kind}.{name}.json".lower()
        if key not in actual:
            raise KeyError(f"{kind}.{name} absent from the Bigus extraction")
        return actual[key]

    def take(kind: str, name: str) -> None:
        if name in objects:
            return
        path = find(kind, name)
        data = load(path)[kind]
        if kind in {"Wall", "Flasher"}:
            method, (x, y) = "polygon_area_centroid", polygon_centroid(data["drag_points"])
        elif kind in {"HitTarget", "Primitive", "Rubber"}:
            method, (x, y) = "object_position", (data["position"]["x"], data["position"]["y"])
        else:
            method, (x, y) = "object_center", (data["center"]["x"], data["center"]["y"])
        objects[name] = {
            "file": f"gameitems/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "type": kind, "method": method, "raw_xy": [round(x, 5), round(y, 5)],
            "xy": [round((x - left) / (right - left), 6), round((y - top) / (bottom - top), 6)],
        }

    def take_light(name: str) -> None:
        for kind in ("Light", "Flasher"):
            if f"{kind}.{name}.json".lower() in actual:
                take(kind, name)
                return
        raise KeyError(f"lamp light {name} absent from the Bigus extraction")

    for kind, name in (*SWITCH_OBJECTS.values(), *COIL_OBJECTS.values()):
        take(kind, name)
    for names in (*LAMP_LIGHTS.values(), *FLASHER_LIGHTS.values(), GI_LIGHTS):
        for name in names:
            take_light(name)
    switches = {str(n): f"{kind}.{name}" for n, (kind, name) in sorted(SWITCH_OBJECTS.items())}
    coils = {str(n): f"{kind}.{name}" for n, (kind, name) in sorted(COIL_OBJECTS.items())}
    return {
        "bounds": [left, top, right, bottom],
        "table_sha256": TABLE_SHA256, "script_sha256": SCRIPT_SHA256,
        "switches": switches,
        "coils": coils,
        "lamps": {str(n): list(names) for n, names in sorted(LAMP_LIGHTS.items())},
        "gi": list(GI_LIGHTS),
        "flashers": {str(n): list(names) for n, names in sorted(FLASHER_LIGHTS.items())},
        "unbound": dict(sorted(UNBOUND.items())),
        "frame": frame_fit(primary_objects, objects, switches, coils),
        "objects": dict(sorted(objects.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extraction", type=Path)
    parser.add_argument("--primary", type=Path, required=True,
                        help="the pinned VPW geometry JSON the frame fit maps onto")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    script = args.extraction / "script.vbs"
    if hashlib.sha256(script.read_bytes()).hexdigest() != SCRIPT_SHA256:
        raise SystemExit("not the retained Bigus 3.0 extraction")
    payload = (json.dumps(build(args.extraction, args.primary), indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
    if args.check:
        if OUTPUT.read_bytes().replace(b"\r\n", b"\n") != payload:
            raise SystemExit("geometry drift")
        print("bigus geometry matches")
    else:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
