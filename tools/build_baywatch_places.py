"""Recompute Baywatch's observed placements from its exact retained VPX extraction.

Only curated, script-linked physical objects are selected. Flasher sprites, backglass objects,
drop-target glow helpers and primitive origins are excluded. Bulb/dome primitives use world-space
OBJ mesh bounds from vpxtool export obj --units vpu; the export remains outside Git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
TABLE_SHA = "50458a3ec79586a307a2cd576efc5d176cb0f3f540ab28f2a197006c32cf6f27"
MANIFEST_SHA = "6716fdbf9c5f594fb3183a4f4bd44529e8e33a8c77d6593f85a5af4c92301090"
SCRIPT_SHA = "a4206e78394fa2405493a1f26c694e7f934d33a4701e75013894c2242af0181e"

SWITCH_OBJECTS = {
    9: "sw9", 15: "BallRelease", 16: "sw16", 25: "Gate25", 28: "Gate28",
    41: "Bumper1", 42: "Bumper2", 43: "Bumper3", 44: "sw44", 46: "sw46",
    52: "sw52", 56: "sw56", 61: "SlingFSx1", 62: "SlingFDx1",
    **{n: f"sw{n}" for n in (*range(17,25),26,30,31,32,33,36,37,38,39,40,45,47,48,49,53,54,55,57,58,59,60)},
}
COIL_OBJECTS = {
    2: ["BallRelease"], 3: ["Plunger1"], 4: ["UpBLaunch"], 5: ["sw44"],
    6: ["sw46"], 7: ["sw56"], 9: ["UpperGate"], 12: ["Botola"],
    13: ["LeftFlipper1", "RightFlipper1"], 14: ["LowerGate"], 16: ["sw23"],
    17: ["Bumper1"], 18: ["Bumper2"], 19: ["Bumper3"],
    20: ["SlingFSx1"], 21: ["SlingFDx1"], 22: ["LaserKick"],
    25: ["DomeBW191", "DomeBW191a"], 26: ["l192", "l192b"],
    27: ["l193a", "DomeBW193"], 28: ["l194", "DomeBW194", "DomeBW194a"],
    30: ["DomeBW196"], 31: ["l197a", "l197b", "l197c"],
    32: ["l198", "DomeBW198"],
}
LAMP_OBJECTS = {
    **{n: [f"l{n}"] for n in (*range(1,6),9,10,*range(14,25),*range(26,33),*range(36,64))},
    **{n: [f"BulboF{n}"] for n in (6,11,12,13,33,34,35)},
    25: ["lL25", "lR25"],
}
GI_OBJECTS = [f"GIBulb{n}g" if n != 14 else "GIBulb14" for n in range(1,32)] + ["GIBulb32a", "GIBulb33a", "GIBumb2", "GIBumb3"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_bounds(path: Path) -> dict:
    groups: dict[str, list[list[float]]] = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("o "):
            current = line[2:]
        elif current is not None and line.startswith("v "):
            groups.setdefault(current, []).append(list(map(float,line.split()[1:4])))
    return {name: {"minimum": [min(v[i] for v in vertices) for i in range(3)],
                   "maximum": [max(v[i] for v in vertices) for i in range(3)]}
            for name,vertices in groups.items()}


def build(vpx_root: Path, obj: Path) -> dict:
    base = vpx_root / "sega/baywatch-1995"
    extraction = base / "extracted-vpxtool"
    if sha(base / "Baywatch (Sega) 1.0.5.vpx") != TABLE_SHA:
        raise ValueError("Baywatch retained VPX differs from the admitted source")
    if check_manifest(extraction, "baywatch") != MANIFEST_SHA or sha(extraction / "script.vbs") != SCRIPT_SHA:
        raise ValueError("Baywatch extraction differs from the admitted source")
    objects = {}
    for path in (extraction / "gameitems").glob("*.json"):
        kind,data = next(iter(json.loads(path.read_text(encoding="utf-8")).items()))
        objects[data["name"]] = (kind,data,path)
    game = json.loads((extraction / "gamedata.json").read_text(encoding="utf-8"))
    if tuple(game[n] for n in ("left","top","right","bottom")) != (0,0,952,2162):
        raise ValueError("Baywatch table bounds changed")
    bounds = mesh_bounds(obj)

    def point(name):
        kind,data,path = objects[name]
        if kind == "Flasher" or data.get("is_backglass"):
            raise ValueError(f"not a physical playfield anchor: {name}")
        if kind == "Primitive":
            box=bounds[name]
            x,y=((box["minimum"][i]+box["maximum"][i])/2 for i in range(2))
            method="world-space OBJ mesh-bounds centre"
        else:
            centre=data.get("center") or data.get("position")
            if centre is None:
                raise ValueError(f"no exact centre for {name}")
            x,y=centre["x"],centre["y"]
            method="stored physical object centre/pivot"
        if not (0 <= x <= 952 and 0 <= y <= 2162):
            raise ValueError(f"out-of-bounds anchor: {name} ({x},{y})")
        return {"object":name,"type":kind,"path":path.relative_to(extraction).as_posix(),
                "sha256":sha(path),"raw_x":x,"raw_y":y,"method":method,
                "x":round(x/952,6),"y":round(y/2162,6),
                **({"world_mesh_bounds":bounds[name]} if kind == "Primitive" else {})}

    placements={}
    for n,name in SWITCH_OBJECTS.items(): placements[f"switch.{n}"]=[point(name)]
    for n,names in COIL_OBJECTS.items(): placements[f"solenoid.{n}"]=[point(name) for name in names]
    for n,names in LAMP_OBJECTS.items(): placements[f"lamp.{n}"]=[point(name) for name in names]
    placements["solenoid.11"]=[point(name) for name in GI_OBJECTS]
    # Mesh-export sanity checks against independently positioned bumper objects. This checks the
    # export's coordinate convention; it does not grant independent physical validation.
    controls=[]
    for mesh,anchor in (("Bumper1Base","Bumper1"),("Bumper2Base","Bumper2"),("Bumper3Base","Bumper3")):
        box=bounds[mesh]; b=point(anchor)
        x,y=((box["minimum"][i]+box["maximum"][i])/2 for i in range(2))
        if abs(x-b["raw_x"])>2 or abs(y-b["raw_y"])>2:
            raise ValueError(f"OBJ coordinate control failed: {mesh} / {anchor}")
        controls.append({"mesh":mesh,"anchor":anchor,"dx":round(x-b["raw_x"],5),"dy":round(y-b["raw_y"],5)})
    return {"table_bounds":{"left":0,"top":0,"right":952,"bottom":2162},
            "table_sha256":TABLE_SHA,"script_sha256":SCRIPT_SHA,"manifest_sha256":MANIFEST_SHA,
            "obj_sha256":sha(obj),"export_command":"vpxtool export obj --units vpu <retained VPX>",
            "tool":"vpxtool git:v0.33.3","placements":placements,"mesh_controls":controls,
            "mechanical_anchors":{name:point(name) for name in ("LeftFlipper","RightFlipper","LeftFlipper1","RightFlipper1")},
            "omitted":"Trough lock coil 1 and five individual trough-switch geometries are absent. Flasher 29 has no admitted socket object; flasher 30 has only one of its two playfield bulbs. Backbox and cabinet coordinates are outside this space.",
            "rejected":["All VPX Flasher objects (reflection/glow sprites)","GIBulb13gt22/23/24 (three target glows at one point)","lgi1/lgi2 and the unselected member of each GIBulb render pair", "Backglass fbb1-fbb33", "Primitive position fields"]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vpx-root",type=Path,required=True)
    parser.add_argument("--world-obj",type=Path,required=True)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    payload=(json.dumps(build(args.vpx_root,args.world_obj),indent=2,sort_keys=True)+"\n").encode()
    path=ROOT/"tools/baywatch_places.json"
    if args.check:
        if path.read_bytes().replace(b"\r\n",b"\n") != payload: raise ValueError("Baywatch placements drifted")
    else:
        path.write_bytes(payload)


if __name__ == "__main__": main()
