"""Recompute Grand Lizard spatial evidence from retained source artifacts."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from pinmame_game_defs.spatial import _item_point, _round_point

SEED = Path("tools/seeds/williams/grand-lizard-1986-spatial.json")
EXTRACTION = Path("williams/grand-lizard-1986/build-01-grand-lizard-williams-1986/extraction")
OBJ = Path("grand-lizard-1986/spatial/build-01-obj-vpu/Grand Lizard (Williams 1986).obj")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Grand Lizard spatial: {message}")


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _source(root: Path, relative: str, expected: str) -> Path:
    path = (root / relative).resolve()
    _require(path.is_relative_to(root.resolve()), f"path escapes source root: {relative}")
    _require(path.is_file() and _hash(path) == expected, f"source digest mismatch: {path}")
    return path


def _solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    rows = [r[:] + [v] for r, v in zip(matrix, vector)]
    for i in range(len(vector)):
        pivot = max(range(i, len(vector)), key=lambda j: abs(rows[j][i]))
        rows[i], rows[pivot] = rows[pivot], rows[i]
        value = rows[i][i]
        _require(abs(value) > 1e-10, "degenerate drawing controls")
        rows[i] = [v / value for v in rows[i]]
        for j in range(len(vector)):
            if j != i:
                value = rows[j][i]
                rows[j] = [x - value * y for x, y in zip(rows[j], rows[i])]
    return [rows[i][-1] for i in range(len(vector))]


def _affine(controls: list[dict]) -> list[list[float]]:
    _require(len(controls) == 4, "expected four independently read flipper controls")
    design = [[*c["pixel"], 1] for c in controls]
    matrix = [[sum(row[i] * row[j] for row in design) for j in range(3)] for i in range(3)]
    return [
        _solve(matrix, [sum(design[j][i] * controls[j]["vpu"][k] for j in range(4)) for i in range(3)])
        for k in (0, 1)
    ]


def _outside(point: list[float], controls: list[dict]) -> bool:
    polygon = [controls[i]["pixel"] for i in (2, 3, 1, 0)]
    cross = [(b[0] - a[0]) * (point[1] - a[1]) - (b[1] - a[1]) * (point[0] - a[0]) for a, b in zip(polygon, polygon[1:] + polygon[:1])]
    return any(v > 1e-9 for v in cross) and any(v < -1e-9 for v in cross)


def _point(kind: str, obj: dict) -> tuple[float, float, str]:
    x, y, method = _item_point(kind, obj.get(kind, obj))
    _require(x is not None and y is not None and method is not None, f"missing {kind} point")
    return x, y, method


def _placement(seed: dict, device_id: str, placement_id: str | None = None) -> dict:
    matches = seed["devices"][device_id]["spatial"]["placements"]
    if placement_id is not None:
        matches = [p for p in matches if p["id"] == placement_id]
    _require(len(matches) == 1, f"missing or ambiguous placement for {device_id}")
    return matches[0]


def _normalized(x: float, y: float, bounds: dict) -> tuple[float, float]:
    return (_round_point((x - bounds["left"]) / (bounds["right"] - bounds["left"])), _round_point((y - bounds["top"]) / (bounds["bottom"] - bounds["top"])))


def verify_spatial(root: Path, vpx_root: Path, manuals_root: Path, review_root: Path) -> None:
    """Fail closed when a source, calibration, mapping or normalized point drifts."""
    root, vpx_root, manuals_root, review_root = map(Path, (root, vpx_root, manuals_root, review_root))
    seed = json.loads((root / SEED).read_text(encoding="utf-8"))
    report = seed["report"]
    extraction = vpx_root / EXTRACTION
    gamedata = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
    bounds = {k: gamedata[k] for k in ("left", "top", "right", "bottom")}
    _require(bounds == report["bounds"] == {"left": 0, "top": 0, "right": 952, "bottom": 1974}, "table bounds drifted")
    ids: set[str] = set()
    for device in seed["devices"].values():
        _require(device["spatial"]["status"] == "observed", "unsupported assertion status")
        for placement in device["spatial"]["placements"]:
            _require(placement["id"] not in ids, "duplicate placement ID")
            ids.add(placement["id"])
    checked: set[str] = set()
    for obs in report["observations"]:
        points = []
        for component in obs.get("components", [obs]):
            path = _source(extraction, component["file"], component["sha256"])
            kind = path.name.split(".", 1)[0]
            x, y, method = _point(kind, json.loads(path.read_text(encoding="utf-8")))
            _require((x, y, method) == (component["raw_x"], component["raw_y"], component["method"]), f"raw geometry drifted: {path}")
            points.append((x, y))
        x, y = (sum(p[i] for p in points) / len(points) for i in (0, 1))
        _require((x, y) == (obs["raw_x"], obs["raw_y"]), "composite point drifted")
        if "components" in obs:
            method = "arithmetic_mean_of_component_points" if len(points) > 1 else obs["components"][0]["method"]
            _require(obs["method"] == method, "composite method drifted")
        placement = _placement(seed, obs["device_id"])
        _require(_normalized(x, y, bounds) == (obs["normalized_x"], obs["normalized_y"]) == (placement["x"], placement["y"]), f"normalized geometry drifted: {obs['device_id']}")
        checked.add(placement["id"])
    for name in ("manual49", "manual50"):
        drawing = report[name]
        _source(manuals_root, drawing["full_page_render"], drawing["full_page_sha256"])
        excerpt = drawing["excerpt"]
        _source(root, excerpt["image"], excerpt["image_sha256"])
        controls = drawing["control_points"]
        for c in controls:
            path = _source(extraction, c["file"], c["sha256"])
            x, y, _ = _point("Flipper", json.loads(path.read_text(encoding="utf-8")))
            _require([x, y] == c["vpu"], f"flipper control drifted: {path}")
        fit = _affine(controls)
        _require(all(math.isclose(fit[i][j], drawing["pixel_to_vpu_affine_rows"][i][j], rel_tol=1e-10, abs_tol=1e-8) for i in range(2) for j in range(3)), f"{name} affine fit drifted")
        _require(max(c["vpu"][1] for c in controls) - min(c["vpu"][1] for c in controls) >= (bounds["bottom"] - bounds["top"]) / 2, f"{name} control span insufficient")
        for c in controls:
            fitted = [sum(a * b for a, b in zip(coefficients, (*c["pixel"], 1))) for coefficients in fit]
            _require([round(fitted[i] - c["vpu"][i], 3) for i in (0, 1)] == c["residual_vpu"], f"{name} control residual drifted")
        for row in drawing["placements"]:
            px, py = row["page_pixel"]
            x, y = (sum(a * b for a, b in zip(coefficients, (px, py, 1))) for coefficients in fit)
            _require(all(math.isclose(actual, recorded, rel_tol=0, abs_tol=1e-6) for actual, recorded in zip((x, y), row["fit_vpu"])), f"drawing fit point drifted: {row['device_id']}")
            placement = _placement(seed, row["device_id"], row.get("placement_id"))
            _require(_normalized(x, y, bounds) == tuple(row["normalized"]) == (placement["x"], placement["y"]), f"drawing point drifted: {row['device_id']}")
            _require(row["extrapolated"] == _outside(row["page_pixel"], controls), f"drawing hull drifted: {row['device_id']}")
            checked.add(placement["id"])
    mesh = report["target_meshes"]
    obj = _source(review_root, OBJ.as_posix(), mesh["obj_sha256"])
    vertices: dict[str, list[list[float]]] = {}
    active = None
    with obj.open(encoding="utf-8") as source:
        for line in source:
            if line.startswith("o "):
                active = line[2:].strip()
            elif active in mesh["meshes"] and line.startswith("v "):
                vertices.setdefault(active, []).append([float(v) for v in line.split()[1:4]])
    for name, expected in mesh["meshes"].items():
        points = vertices.get(name, [])
        _require(len(points) == expected["vertices"], f"mesh vertex count drifted: {name}")
        low = [min(p[i] for p in points) for i in range(3)]
        high = [max(p[i] for p in points) for i in range(3)]
        _require(low == expected["bounds_min"] and high == expected["bounds_max"], f"mesh bounds drifted: {name}")
        _require([(a + b) / 2 for a, b in zip(low, high)] == expected["center"], f"mesh center drifted: {name}")
    for c in mesh["independent_table_controls"]:
        path = _source(extraction, "gameitems/" + c["collider"], c["collider_sha256"])
        x, y, _ = _point("HitTarget", json.loads(path.read_text(encoding="utf-8")))
        center = mesh["meshes"][c["primitive"]]["center"][:2]
        _require([x, y] == c["collider_vpu"] and center == c["mesh_center_vpu"] and math.isclose(math.hypot(center[0]-x, center[1]-y), c["distance_vpu"], abs_tol=1e-9), "mesh control drifted")
    for device_id, name in mesh["switches"].items():
        x, y, _ = mesh["meshes"][name]["center"]
        placement = _placement(seed, device_id)
        _require(_normalized(x, y, bounds) == (placement["x"], placement["y"]), f"mesh point drifted: {device_id}")
        checked.add(placement["id"])
    _require(checked == ids, "missing or unaccounted spatial placements")
