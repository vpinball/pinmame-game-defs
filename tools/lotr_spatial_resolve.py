"""Resolve LOTR device coordinates from four retained recreations.

Three retained tables are readings of the factory playfield; independence between them is
unestablished. Treating them as three measurements rather than one authority corroborates a
position when all three agree and exposes outliers. A fourth Neo LED recreation is a derivative
JPSalas table and therefore contributes only a supplemental measurement of lamps 81-99. Every
lamp-81-99 coordinate is resolved through each script's own address-to-object binding; object names
are never assumed to equal public addresses.

Classification per device:
  validated  - all three factory-layout tables agree within AGREE (Neo may agree or disagree)
  observed   - fewer than all three factory-layout tables agree; usable but not fully corroborated
  conflicted - tables place it in genuinely different spots with no majority
  missing    - no table models it

Coordinates are normalized per table against that table's own playfield bounds, so
different table sizes are directly comparable.
"""
import argparse
import json
import os
import re
import statistics
from pathlib import Path


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--write",
    type=Path,
    required=True,
    metavar="PATH",
    help="Write the derived consensus to this explicit external evidence path.",
)
args = parser.parse_args()

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
LED_TABLES = {
    # This is a Neo LED derivative of the retained JPSalas table, not an independent factory-layout
    # authority. It contributes a supplemental l81-l99 measurement only.
    "neo-led-1-0-3": BASE / "source" / "vpxtool-extract",
}
ALL_TABLES = {**TABLES, **LED_TABLES}
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
REQUIRED_FACTORY_TABLES = frozenset(TABLES)

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

# Public flasher 25 drives three distinct bulbs. Each retained script binds all of its listed
# objects to that one output, so reducing a table to one arbitrary f25 object compares different
# bulbs and manufactures an outlier. Group every co-located rendering object by physical emitter;
# the resolver verifies both the script evidence and within-table co-location before consensus.
FLASHER_EMITTER_OBJECTS = {
    25: {
        "left": {
            "vpw-1-6": {
                "objects": ["Flasherbase1"],
                "script_evidence": ["SolModCallback(25)", "Lampz.Callback(125)", "sub ModFlash25", "UpdateCaps 1", 'Eval("Flasherbase" & nr)'],
            },
            "jpsalas-600": {
                "objects": ["f25a001", "f25c001"],
                "script_evidence": ["SolCallback(25)", "f25a001", "f25c001"],
            },
            "hanibal-4k": {
                "objects": ["f25b", "f25e"],
                "script_evidence": ["SolCallBack(25)", "Kombiflasher2 125, f25b", "NFadeLm 125, f25e"],
            },
        },
        "right": {
            "vpw-1-6": {
                "objects": ["Flasherbase3"],
                "script_evidence": ["SolModCallback(25)", "Lampz.Callback(125)", "sub ModFlash25", "UpdateCaps 3", 'Eval("Flasherbase" & nr)'],
            },
            "jpsalas-600": {
                "objects": ["f25a002", "f25c002"],
                "script_evidence": ["SolCallback(25)", "f25a002", "f25c002"],
            },
            "hanibal-4k": {
                "objects": ["f25a", "f25f"],
                "script_evidence": ["SolCallBack(25)", "Kombiflasher2 125, f25a", "NFadeLm 125, f25f"],
            },
        },
        "bottom": {
            "vpw-1-6": {
                "objects": ["Flasherbase2"],
                "script_evidence": ["SolModCallback(25)", "Lampz.Callback(125)", "sub ModFlash25", "UpdateCaps 2", 'Eval("Flasherbase" & nr)'],
            },
            "jpsalas-600": {
                "objects": ["f25a3", "f25c"],
                "script_evidence": ["SolCallback(25)", "f25a3", "f25c"],
            },
            "hanibal-4k": {
                "objects": ["f25c", "f25d"],
                "script_evidence": ["SolCallBack(25)", "Kombiflasher2 125, f25c", "NFadeLm 125, f25d"],
            },
        },
    },
}


def bounds(extract: Path):
    g = json.loads((extract / "gamedata.json").read_text(encoding="utf-8"))
    return float(g["left"]), float(g["right"]), float(g["top"]), float(g["bottom"])


BOUNDS = {label: bounds(path) for label, path in ALL_TABLES.items() if (path / "gamedata.json").exists()}
INDEX = {
    label: {p.name.split(".")[-2].lower(): p for p in (path / "gameitems").glob("*.json") if p.name.count(".") >= 2}
    for label, path in ALL_TABLES.items()
}


# The retained scripts use three different lamp APIs, and Hanibal deliberately binds public
# addresses 81-99 to differently numbered objects. Parse those calls instead of guessing l<N>.
# Multiple objects on one call address (usually the base light plus an "a" overlay) are one table
# measurement; the resolver verifies that their coordinates are co-located before publishing the
# first bound object as that table's point.
LED_BINDING_PATTERNS = (
    re.compile(r"\bLampz\.MassAssign\((8[1-9]|9[0-9])\)\s*=\s*([A-Za-z_][A-Za-z0-9_]*)", re.I),
    re.compile(r"\bLamp\s+(8[1-9]|9[0-9])\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", re.I),
    re.compile(r"\bNFadeLm?\s+(8[1-9]|9[0-9])\s*,\s*([A-Za-z_][A-Za-z0-9_]*)", re.I),
)


def script_led_bindings(label: str, extract: Path) -> dict[int, list[dict]]:
    script = extract / "script.vbs"
    bindings: dict[int, list[dict]] = {}
    for line_no, line in enumerate(script.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        code = line.split("'", 1)[0]
        match = None
        for pattern in LED_BINDING_PATTERNS:
            match = pattern.search(code)
            if match is not None:
                break
        if match is None:
            continue
        address, name = int(match.group(1)), match.group(2)
        rows = bindings.setdefault(address, [])
        if not any(row["object"].lower() == name.lower() for row in rows):
            rows.append({"object": name, "script_line": line_no})
    missing = sorted(set(range(81, 100)) - set(bindings))
    if missing:
        raise SystemExit(f"{label} script has no explicit lamp binding for public addresses {missing}")
    return bindings


LED_BINDINGS = {label: script_led_bindings(label, path) for label, path in ALL_TABLES.items()}


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


def _script_evidence_lines(label: str, patterns: list[str]) -> list[int]:
    lines = (ALL_TABLES[label] / "script.vbs").read_text(encoding="utf-8", errors="replace").splitlines()
    found = []
    for pattern in patterns:
        matches = [line_no for line_no, line in enumerate(lines, 1) if pattern.lower() in line.lower()]
        if not matches:
            raise SystemExit(f"{label} flasher binding evidence is missing script text {pattern!r}")
        found.append(matches[0])
    return sorted(set(found))


def flasher_emitter_candidates(address: int, emitter: str) -> list[dict]:
    out = []
    for label, binding in FLASHER_EMITTER_OBJECTS[address][emitter].items():
        hits = [locate(label, name) for name in binding["objects"]]
        if any(hit is None for hit in hits):
            missing = [name for name, hit in zip(binding["objects"], hits) if hit is None]
            raise SystemExit(f"{label} flasher {address} {emitter} has no positioned objects {missing}")
        positioned = [hit for hit in hits if hit is not None]
        primary = positioned[0]
        for hit in positioned[1:]:
            if abs(hit["x"] - primary["x"]) > 0.005 or abs(hit["y"] - primary["y"]) > 0.005:
                raise SystemExit(
                    f"{label} flasher {address} {emitter} binds non-co-located objects "
                    f"{primary['object']} and {hit['object']}; one emitter cannot be reduced to one measurement"
                )
        primary["bound_objects"] = [hit["object"] for hit in positioned]
        primary["script_lines"] = _script_evidence_lines(label, binding["script_evidence"])
        out.append(primary)
    return out


def candidates(kind: str, address: int, prefix: str, labels=TABLES):
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
    for label in labels:
        for name in names:
            hit = locate(label, name)
            if hit:
                out.append(hit)
                break
    return out


def led_candidates(address: int):
    out = []
    for label in ALL_TABLES:
        bindings = LED_BINDINGS[label][address]
        hits = [(binding, locate(label, binding["object"])) for binding in bindings]
        hits = [(binding, hit) for binding, hit in hits if hit is not None]
        if not hits:
            raise SystemExit(f"{label} script binds lamp {address}, but none of its bound objects is positioned")
        primary = hits[0][1]
        for binding, hit in hits[1:]:
            if abs(hit["x"] - primary["x"]) > 0.005 or abs(hit["y"] - primary["y"]) > 0.005:
                raise SystemExit(
                    f"{label} lamp {address} binds non-co-located objects "
                    f"{primary['object']} and {binding['object']}; one table cannot be reduced to one measurement"
                )
        primary["bound_objects"] = [binding["object"] for binding, _ in hits]
        primary["script_lines"] = [binding["script_line"] for binding, _ in hits]
        out.append(primary)
    return out


def consensus(hits: list[dict]):
    if not hits:
        return {"status": "missing", "candidates": []}
    if len(hits) == 1:
        h = hits[0]
        return {"status": "observed", "x": round(h["x"], 6), "y": round(h["y"], 6),
                "agreeing_tables": [h["table"]], "outliers": [], "candidates": hits}
    # Largest cluster whose members are all within AGREE of the cluster's first member. Preserve
    # every distinct largest membership set so a 2-2 tie is reported as conflicted instead of
    # being silently decided by table iteration order.
    clusters: list[tuple[int, ...]] = []
    for anchor in hits:
        cluster = tuple(
            index for index, hit in enumerate(hits)
            if abs(hit["x"] - anchor["x"]) <= AGREE and abs(hit["y"] - anchor["y"]) <= AGREE
        )
        if cluster not in clusters:
            clusters.append(cluster)
    largest = max(len(cluster) for cluster in clusters)
    best_clusters = [cluster for cluster in clusters if len(cluster) == largest]
    if largest < 2 or len(best_clusters) != 1:
        return {"status": "conflicted", "candidates": hits}
    best = [hits[index] for index in best_clusters[0]]
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


def verify_consensus_tie_policy() -> None:
    def hit(table: str, x: float, y: float) -> dict:
        return {"table": table, "object": table, "x": x, "y": y}

    tied = consensus([
        hit("a", 0.0, 0.0), hit("b", 0.01, 0.0),
        hit("c", 0.5, 0.5), hit("d", 0.51, 0.5),
    ])
    if tied["status"] != "conflicted":
        raise RuntimeError("consensus must not decide a 2-2 cluster tie by iteration order")
    majority = consensus([
        hit("a", 0.0, 0.0), hit("b", 0.01, 0.0), hit("c", 0.0, 0.01), hit("d", 0.5, 0.5),
    ])
    if majority["status"] != "validated" or set(majority["agreeing_tables"]) != {"a", "b", "c"}:
        raise RuntimeError("consensus must retain an unambiguous three-table cluster")


verify_consensus_tie_policy()


# Where the tables do not form a clean cluster, the manual settles it. Consensus proposes,
# the manual disposes: each entry names the DR.7 or DR.4 reading that picked the winner, and
# the coordinate still comes from a retained table rather than from reading pixels off a scan.
MANUAL_RESOLUTIONS = {
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
        "reason": "DR.4 prints 28 Balrog Hit as an above-playfield switch on the Balrog itself. JPSalas x=0.5105 sits on the Balrog assembly shown in the printed location drawing; Hanibal's x=0.4390 is off the toy. VPW has no bound sw28 object and contributes no switch-28 measurement.",
    },
    ("switch", 41): {
        "pick": "median-of-three",
        "reason": "All three tables agree on y within 0.008 but spread x from 0.182 to 0.266 for the Top VUK. DR.4 places 41 in the upper-left; the per-axis median is taken.",
    },
}

GROUPS = [
    ("lamp", "l", range(1, 81), TABLES),
    ("switch", "sw", range(1, 65), TABLES),
    ("flasher", "f", [14, 23, 25, 26, 27, 29, 30, 31, 32], TABLES),
    ("lamp", "l", range(81, 100), ALL_TABLES),
]
result = {
    "agreement_threshold": AGREE,
    "tables": {
        k: {
            "bounds": BOUNDS[k],
            "role": "supplemental-derivative-led-measurement" if k in LED_TABLES else "factory-playfield-consensus",
        }
        for k in BOUNDS
    },
    "devices": {},
}
for kind, prefix, addresses, labels in GROUPS:
    bucket = {}
    for address in addresses:
        if kind == "flasher" and address in FLASHER_EMITTER_OBJECTS:
            emitters = {}
            for emitter in ("left", "right", "bottom"):
                emitter_hits = flasher_emitter_candidates(address, emitter)
                emitter_entry = consensus(emitter_hits)
                supporting = set(emitter_entry.get("agreeing_tables", ()))
                if emitter_entry.get("status") != "validated" or not REQUIRED_FACTORY_TABLES <= supporting:
                    raise SystemExit(
                        f"flasher {address} {emitter} is not corroborated by all factory tables: "
                        f"{sorted(supporting)}"
                    )
                emitter_entry["measurements"] = [
                    {
                        "table": hit["table"], "object": hit["object"],
                        "bound_objects": hit["bound_objects"], "script_lines": hit["script_lines"],
                        "x": round(hit["x"], 6), "y": round(hit["y"], 6),
                    }
                    for hit in emitter_hits
                ]
                emitter_entry.pop("candidates", None)
                emitters[emitter] = emitter_entry
            bucket[address] = {
                "status": "validated",
                "quantity": len(emitters),
                "emitters": emitters,
                "resolution": (
                    "The public output drives three physical bulbs. Every retained factory-layout script binds all "
                    "three, grouped here by co-located left, right and bottom emitter objects before consensus."
                ),
            }
            continue
        hits = led_candidates(address) if kind == "lamp" and address >= 81 else candidates(kind, address, prefix, labels)
        entry = consensus(hits)
        if kind == "lamp" and address >= 81:
            entry["script_bound_measurements"] = [
                {
                    "table": hit["table"], "object": hit["object"],
                    "bound_objects": hit["bound_objects"], "script_lines": hit["script_lines"],
                    "x": round(hit["x"], 6), "y": round(hit["y"], 6),
                }
                for hit in hits
            ]
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
            supporting_labels = {h["table"] for h in supporting}
            entry["status"] = "validated" if REQUIRED_FACTORY_TABLES <= supporting_labels else "observed"
            # Recompute spread against the published coordinate so it can never describe a
            # cluster the record no longer claims.
            if supporting:
                entry["spread"] = round(max(max(abs(h["x"] - entry["x"]) for h in supporting),
                                            max(abs(h["y"] - entry["y"]) for h in supporting)), 6)
            else:
                entry.pop("spread", None)
        bucket[address] = entry
    result["devices"].setdefault(kind, {}).update(bucket)

serializable = json.loads(json.dumps(result))
for kind_bucket in serializable["devices"].values():
    for entry in kind_bucket.values():
        if (entry.get("status") == "conflicted" and entry.get("candidates")
                and not entry.get("script_bound_measurements")):
            entry["measurements"] = [
                {"table": hit["table"], "object": hit["object"],
                 "x": round(hit["x"], 6), "y": round(hit["y"], 6)}
                for hit in entry["candidates"]
            ]
        entry.pop("candidates", None)
args.write.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

for kind in result["devices"]:
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
