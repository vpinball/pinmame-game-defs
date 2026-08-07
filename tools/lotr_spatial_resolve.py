"""Resolve LOTR device coordinates by consensus across the three retained recreations.

Each retained table is one author's reading of the same physical machine; independence between
them is unestablished. Treating them as three measurements rather than one authority does two
things a single-table pass cannot: it corroborates a position when all three agree, and it
exposes a placement one author got wrong instead of importing that error silently.

Classification per device:
  validated  - all three tables agree within AGREE (any disagreeing table is reported)
  observed   - fewer than three tables agree; usable but not fully corroborated
  conflicted - tables place it in genuinely different spots with no majority
  missing    - no table models it

Coordinates are normalized per table against that table's own playfield bounds, so
different table sizes are directly comparable.
"""
import json
import os
import re
import statistics
import sys
from pathlib import Path

def _evidence_root() -> Path:
    """Resolve the retained VPX sources root: PINMAME_VPX_SOURCES_ROOT, else the runbook's
    sibling working directory. Nothing here writes into the repository."""
    override = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if override:
        return Path(override) / "stern" / "lord-of-the-rings-2003"
    # Walk up until the runbook's sibling working directory is found, so this resolves the same
    # way from the main checkout and from a per-game worktree.
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "pinmame-game-defs-working-dir" / "vpx-sources"
        if candidate.is_dir():
            return candidate / "stern" / "lord-of-the-rings-2003"
    raise SystemExit(
        "Cannot locate the retained VPX sources. Set PINMAME_VPX_SOURCES_ROOT to the vpx-sources root."
    )


BASE = _evidence_root()
TABLES = {
    "vpw-1-6": BASE / "vpxtool-extract",
    "jpsalas-600": BASE / "alt-jpsalas-600" / "vpxtool-extract",
    "hanibal-4k": BASE / "alt-hanibal-4k" / "vpxtool-extract",
}
AGREE = 0.025  # normalized units; ~2.5% of playfield width/length

# Independence between the three retained recreations is UNESTABLISHED, so no grouping of them
# is asserted. Two facts are recorded and neither settles it:
#   - measured: JPSalas and Hanibal agree with each other to within 0.0155 on every lamp both
#     model, while either differs from VPW by up to 0.187.
#   - documented: VPW credits "EBIsLit - Baseline playfield scan" and JPSalas records its
#     playfield as "based on Ebislit's playfield". Hanibal states no ancestry at all.
# The measured clustering and the documented ancestry pair the tables DIFFERENTLY, so any lineage
# model would be a guess. Rather than invent one, corroboration is counted conservatively: a
# placement is validated only when all three retained tables agree on it, which is the strongest
# evidence available here and needs no ancestry claim. Anything less is observed.
REQUIRED_AGREEMENT = 3

# Objects a table may use for a device when it does not use the plain l<N>/sw<N>/f<N> name.
# Every entry here is a naming-convention lead that the consensus check then confirms or rejects.
ALIASES = {
    "switch": {
        49: ["Bumper1", "Bumper001", "bumper1"],
        50: ["Bumper2", "Bumper002", "bumper2"],
        51: ["Bumper3", "Bumper003", "bumper3"],
        59: ["Leftslingshot", "LeftSlingshot", "LSling", "sling1"],
        62: ["Rightslingshot", "RightSlingshot", "RSling", "sling2"],
    },
    "flasher": {},
}

# Flasher object names taken from each script's own callback bindings rather than guessed,
# because the three authors name flasher objects completely differently. VPW routes every
# flasher through Lampz.Callback -> ModFlashNN -> UpdateCaps <cap> -> Flasherbase<cap>;
# JPSalas binds objects directly in vpmFlasher; Hanibal maps them with Kombiflasher2/NFadeLm.
FLASHER_OBJECTS = {
    14: {"vpw-1-6": "Flasherbase4", "jpsalas-600": "f14", "hanibal-4k": "f14a"},
    23: {"vpw-1-6": "Flasherbase5", "jpsalas-600": "f23", "hanibal-4k": "f23a"},
    25: {"vpw-1-6": "Flasherbase2", "jpsalas-600": "f25c", "hanibal-4k": "f25b"},
    # JPSalas' f<N>l objects are non-positional helper Lights parked together at
    # (0.1366, 0.9018); only the Flasher props carry real coordinates. Using the
    # helper lights produced three fake conflicts.
    26: {"vpw-1-6": None, "jpsalas-600": "f26", "hanibal-4k": "F26"},
    27: {"vpw-1-6": "Flasherbase7", "jpsalas-600": "f27a", "hanibal-4k": "F27a"},
    29: {"vpw-1-6": "Flasherbase6", "jpsalas-600": "f29a", "hanibal-4k": "f29"},
    30: {"vpw-1-6": "f130", "jpsalas-600": "f30", "hanibal-4k": "f130"},
    31: {"vpw-1-6": None, "jpsalas-600": "f31", "hanibal-4k": None},
    32: {"vpw-1-6": "Lbalrogbloom", "jpsalas-600": "l132", "hanibal-4k": None},
}


def bounds(extract: Path):
    g = json.loads((extract / "gamedata.json").read_text(encoding="utf-8"))
    return float(g["left"]), float(g["right"]), float(g["top"]), float(g["bottom"])


BOUNDS = {label: bounds(path) for label, path in TABLES.items() if (path / "gamedata.json").exists()}
INDEX = {
    label: {p.name.split(".")[-2].lower(): p for p in (path / "gameitems").glob("*.json") if p.name.count(".") >= 2}
    for label, path in TABLES.items()
}


def locate(label: str, name: str):
    path = INDEX[label].get(name.lower())
    if path is None:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    variant, body = next(iter(payload.items()))
    c = body.get("center") or body.get("position")
    if not c:
        pts = body.get("drag_points") or []
        if not pts:
            return None
        c = {"x": sum(p["x"] for p in pts) / len(pts), "y": sum(p["y"] for p in pts) / len(pts)}
    left, right, top, bottom = BOUNDS[label]
    return {
        "table": label,
        "object": path.name.split(".")[-2],
        "item_type": variant,
        "x": (float(c["x"]) - left) / (right - left),
        "y": (float(c["y"]) - top) / (bottom - top),
    }


def candidates(kind: str, address: int, prefix: str):
    if kind == "flasher":
        # Explicit per-table objects only; a generic f<N> guess pairs different physical
        # devices across tables and manufactures conflicts that are not real.
        out = []
        for label, name in FLASHER_OBJECTS.get(address, {}).items():
            if not name:
                continue
            hit = locate(label, name)
            if hit:
                out.append(hit)
        return out
    names = [f"{prefix}{address}"] + ALIASES.get(kind, {}).get(address, [])
    if kind == "lamp":
        # VPW drives several inserts as p<N> primitives through Lampz.Callback rather than as
        # l<N> lights. Searching only l<N> reported those lamps as unmodelled when they are not.
        names.append(f"p{address}")
    out = []
    for label in TABLES:
        for name in names:
            hit = locate(label, name)
            if hit:
                out.append(hit)
                break
    return out


def consensus(hits: list[dict]):
    if not hits:
        return {"status": "missing", "candidates": []}
    if len(hits) == 1:
        h = hits[0]
        return {"status": "observed", "x": round(h["x"], 6), "y": round(h["y"], 6),
                "agreeing_tables": [h["table"]], "outliers": [], "candidates": hits}
    # Largest cluster whose members are all within AGREE of the cluster's first member.
    best: list[dict] = []
    for anchor in hits:
        cluster = [h for h in hits if abs(h["x"] - anchor["x"]) <= AGREE and abs(h["y"] - anchor["y"]) <= AGREE]
        if len(cluster) > len(best):
            best = cluster
    if len(best) < 2:
        return {"status": "conflicted", "candidates": hits}
    outliers = [h for h in hits if h not in best]
    return {
        "status": "validated",
        "x": round(statistics.median(h["x"] for h in best), 6),
        "y": round(statistics.median(h["y"] for h in best), 6),
        "spread": round(max(max(h["x"] for h in best) - min(h["x"] for h in best),
                            max(h["y"] for h in best) - min(h["y"] for h in best)), 6),
        "agreeing_tables": [h["table"] for h in best],
        "outliers": [{"table": h["table"], "x": round(h["x"], 6), "y": round(h["y"], 6)} for h in outliers],
        "candidates": hits,
    }


# Where the tables do not form a clean cluster, the manual settles it. Consensus proposes,
# the manual disposes: each entry names the DR.7 or DR.4 reading that picked the winner, and
# the coordinate still comes from a retained table rather than from reading pixels off a scan.
MANUAL_RESOLUTIONS = {
    ("flasher", 25): {
        "pick": "centroid-of-bumpers",
        "x": 0.706166, "y": 0.257348,
        # The centroid is computed from the three pop-bumper bodies, not from any f25 object, so
        # the tables credited must be the ones that supplied those bumper positions.
        "derived_from": ["vpw-1-6"],
        "reason": "DR.7 prints '25' three times, once beside each of coils 9, 10 and 11, all marked Red. FLASH: POPS X3 is three physical bulbs at the three pop bumpers, so each table legitimately picked a different one. Placed at the centroid of the three bumper positions with physical.quantity 3.",
    },
    ("flasher", 27): {
        "pick": "median-of-three",
        "reason": "DR.7 states flashers 26 and 27 are on the Back Panel and prints 27 (Clear) at the top right. All three tables place it in that corner but spread x 0.888-0.932 and y 0.033-0.074, just outside the agreement threshold; the per-axis median is taken.",
    },
    ("flasher", 29): {
        "pick": "jpsalas-600",
        "reason": "DR.7 places 29 (Red) hard against the right playfield edge, level with and slightly above the right pop bumper. JPSalas x=0.9568 y=0.1893 matches; VPW's x=0.867 is too far inboard and Hanibal's y=0.282 sits below the bumper instead of above it.",
    },
    ("flasher", 30): {
        "pick": "median-of-three",
        "reason": "DR.7 places 30 (Clear) on the right rail immediately beside coil 21, Sword Lock Release. All three tables agree on that region within 0.053; the per-axis median is taken.",
    },
    ("flasher", 31): {
        "pick": "jpsalas-600",
        "reason": "DR.7 places 31 (Clear) at the Destroy The Ring insert. Only JPSalas models it as a positioned flasher; VPW references the same insert in a commented-out DisableLighting p19 call, corroborating the location.",
    },
    ("flasher", 32): {
        "pick": "vpw-1-6",
        "reason": "DR.7 places 32 (Clear) at the Balrog, directly above the motor marked 22. VPW's Lbalrogbloom is the only object bound to the Balrog flash in a positioned form.",
    },
    ("switch", 28): {
        "pick": "jpsalas-600",
        "reason": "DR.4 prints 28 Balrog Hit as an above-playfield switch on the Balrog itself. JPSalas x=0.5105 sits on the Balrog assembly, which VPW independently models at x=0.5078; Hanibal's x=0.4390 is off the toy.",
    },
    ("switch", 41): {
        "pick": "median-of-three",
        "reason": "All three tables agree on y within 0.008 but spread x from 0.182 to 0.266 for the Top VUK. DR.4 places 41 in the upper-left; the per-axis median is taken.",
    },
}

GROUPS = [("lamp", "l", range(1, 81)), ("switch", "sw", range(1, 65)), ("flasher", "f", [14, 23, 25, 26, 27, 29, 30, 31, 32])]
result = {"agreement_threshold": AGREE, "tables": {k: {"bounds": BOUNDS[k]} for k in BOUNDS}, "devices": {}}
for kind, prefix, addresses in GROUPS:
    bucket = {}
    for address in addresses:
        hits = candidates(kind, address, prefix)
        entry = consensus(hits)
        override = MANUAL_RESOLUTIONS.get((kind, address))
        if override:
            pick = override["pick"]
            entry["coordinate_origin"] = "table"
            if pick == "median-of-three" and hits:
                entry["x"] = round(statistics.median(h["x"] for h in hits), 6)
                entry["y"] = round(statistics.median(h["y"] for h in hits), 6)
                # A per-axis median can take x from one table and y from another, producing a
                # point no table holds. Only call it table-sourced when a table actually holds it.
                if not any(abs(h["x"] - entry["x"]) < 1e-9 and abs(h["y"] - entry["y"]) < 1e-9 for h in hits):
                    entry["coordinate_origin"] = "computed"
                    entry["derived_from"] = [h["table"] for h in hits]
            elif "x" in override:
                # A coordinate no table holds. It is derived, and must not be attributed to one.
                entry["x"], entry["y"] = override["x"], override["y"]
                entry["coordinate_origin"] = "computed"
                entry["derived_from"] = override.get("derived_from", [h["table"] for h in hits])
            else:
                chosen = next((h for h in hits if h["table"] == pick), None)
                if chosen:
                    entry["x"], entry["y"] = round(chosen["x"], 6), round(chosen["y"], 6)
            entry["resolved_by"] = "manual"
            entry["resolution"] = override["reason"]
        # Recompute support and disagreement against the coordinate actually published, on every
        # path. Previously the manual path rewrote agreeing_tables to every candidate, which made
        # the outlier list empty by construction and erased the very disagreements a manual
        # tie-break exists to record.
        if "x" in entry:
            supporting, disagreeing = [], []
            for h in hits:
                near = abs(h["x"] - entry["x"]) <= AGREE and abs(h["y"] - entry["y"]) <= AGREE
                (supporting if near else disagreeing).append(h)
            entry["agreeing_tables"] = [h["table"] for h in supporting]
            entry["outliers"] = [
                {"table": h["table"], "x": round(h["x"], 6), "y": round(h["y"], 6)} for h in disagreeing
            ]
            entry.setdefault("coordinate_origin", "table")
            entry["status"] = "validated" if len(supporting) >= REQUIRED_AGREEMENT else "observed"
            # Recompute spread against the published coordinate so it can never describe a
            # cluster the record no longer claims.
            if supporting:
                entry["spread"] = round(max(max(abs(h["x"] - entry["x"]) for h in supporting),
                                            max(abs(h["y"] - entry["y"]) for h in supporting)), 6)
            else:
                entry.pop("spread", None)
        bucket[address] = entry
    result["devices"][kind] = bucket

serializable = json.loads(json.dumps(result))
for kind_bucket in serializable["devices"].values():
    for entry in kind_bucket.values():
        entry.pop("candidates", None)
Path(sys.argv[1]).write_text(json.dumps(serializable, indent=2), encoding="utf-8")

for kind, _, addresses in GROUPS:
    bucket = result["devices"][kind]
    counts: dict[str, int] = {}
    for c in bucket.values():
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    print(f"{kind:9} {counts}")
    for addr, c in bucket.items():
        if c["status"] == "conflicted":
            print(f"    CONFLICT {kind} {addr}: " + "; ".join(f"{h['table']} {h['x']:.4f},{h['y']:.4f}" for h in c["candidates"]))
        elif c.get("outliers"):
            o = c["outliers"][0]
            print(f"    OUTLIER  {kind} {addr}: consensus {c['x']:.4f},{c['y']:.4f} from {'+'.join(c['agreeing_tables'])}; {o['table']} says {o['x']:.4f},{o['y']:.4f}")
        elif c["status"] == "missing":
            print(f"    MISSING  {kind} {addr}")
