#!/usr/bin/env python3
"""Build the partial Embryon inventory from pinned, individually reviewed evidence.

High auxiliary selectors and physical lamp counts remain unresolved; an emulator
address's existence alone does not establish a physical lamp socket.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pinmame_game_defs.spatial import _round_point
from embryon_lamps import build_lamps, A5, A9, WIRING
OUTPUT = ROOT / "machines/partial/bally/embryon-1981.json"
PROMOTED = ROOT / "machines/author-ready/bally/embryon-1981.json"
EXCERPT = ROOT / "evidence/excerpts/bally.embryon.1981/manual-page-22.md"
EXCERPT_HASH = "c14ef79af27575a7ee6afb6294a572ce4e2d4a0196453efef549753d9b0af7e8"
DIP_EXCERPT = ROOT / "evidence/excerpts/bally.embryon.1981/manual-pages-10-12.md"
DIP_HASH = "fd7805687f001ed15fe41fd779db29e97a14986788232642019d3319c11a032c"
IDENTITY_EXCERPT = ROOT / "evidence/excerpts/bally.embryon.1981/ipdb-identity.md"
IDENTITY_HASH = "c141ea6d227a23f10bfb39af9471271a4fb2f489fec0f9316efc765d2911994b"
TEXT_SEEDS = {
    ROOT / "tools/seeds/bally/embryon-1981-harness.json":
        (ROOT / "evidence/runtime/by35/embryon-1981-harness.json", "973da065183f08e72af6e1be27a15f732fd697e58d422f964064d0d9518c104c"),
    ROOT / "tools/seeds/bally/embryon-1981-knowledge.md":
        (ROOT / "knowledge/bally/embryon-1981.md", "e9c92acb360054efaecf434c529fa298071632aa6a1f46c2ff01493d6c5eb2d1"),
    ROOT / "tools/seeds/bally/embryon-1981-spatial.md":
        (ROOT / "reports/spatial/bally/embryon-1981.md", "823c10ee58ff5ae7acd87d92d01426bb4bf4fc00b4925f373c2b6a4b093a07d9"),
}
MANUAL = "manual.embryon"
CORE = "pinmame.embryon"
SCRIPT = "vpx.embryon.local"
RUN = "runtime.embryon.solenoid"
GEOMETRY = "vpx.embryon.geometry"
SWITCH_SCHEMATIC = "schematic.embryon.switch"
SOLENOID_SCHEMATIC = "schematic.embryon.solenoid"
FLIP_RUN = "runtime.embryon.flippers"
CABINET_SCHEMATIC = "schematic.embryon.cabinet"
MPU_SCHEMATIC = "schematic.embryon.mpu"
SOUND_SCHEMATIC = "schematic.embryon.sound"
LIBRARY = "vpx.embryon.core-library"
MODERN = "vpx.embryon.modern"
MODERN_GEOMETRY = "vpx.embryon.modern-geometry"
RESET_RUN = "runtime.embryon.single-drop"
RESET_EVIDENCE = ROOT / "tools/seeds/bally/embryon-1981-single-drop.json"
RESET_HASH = "5647ec3ddf6aef15447f55613cd21b16946c55d8f25af86f2c0c448a8bc84f12"
BULB_SEED = ROOT / "tools/seeds/bally/embryon-1981-bulbs.json"
BULB_HASH = "0d51b6ea72f44fe2614c33bb7db8f5e411f0915c0e31b58f3b184b3b96deb759"
EXTRA_EVIDENCE = {
    "manual-page-22.md": EXCERPT_HASH,
    "main-lamp-map.md": "35f28f07e1ae6db44a1206345b0f01689e092d78b6c1b2a88e6db47d20e3752c",
    "schematic-connector-tables.md": "63848f470be5deef8cc3f0e8abb55c7498c158bea067922aa30083db9b560f12",
    "switch17-series.md": "6409bd5fdd46fda346bfa511b09235a37dd1313ee7ae93f7bb8af05c95688f86",
    "runtime-bindings.md": "ed6b8339306a10f15139087ab98b39603a23af9aa10e1d2bde494d90854728d8",
    "manual-rules.md": "bf7cbd4125535a83888cbb4bbe3006943453b80fb4c94ce5ca1ea8f58316ddaf",
    "manual-parts.md": "b4fe5355f52abdbb7705d9d68060b8530dd0c5080df539093565e46d105c3678",
    "modeled-bulbs.md": "e79dc4b1a549fd0be174bab6565cf48bb98c4880dd7ed974a337734a5faf282f",
    "solenoid-fitment.md": "6a33002c610a4eef78d384bff00927a28aea92aede636aecee37f9676eb5c36b",
    "switch-column-fitment.md": "d2d844b9fae76d459b96ca98aa286f38cab23276cfffc4ba8e31272f7c3d6d66",
    "service-polarity.md": "1be91e315ce7261a615a1d26d6c26861ac2ee193aa651ac7bbf6e351d141968a",
}
FLIP_EVIDENCE = ROOT / "tools/seeds/bally/embryon-1981-flipper-tilt.json"
FLIP_HASH = "25ec5e35da735039d290f55a77e86f292394d71e6cd6885bb66385395dee57aa"
SPATIAL_SEED = ROOT / "tools/seeds/bally/embryon-1981-spatial.json"
SPATIAL_HASH = "5a75c8017c9cc0d2cf5429dd60e6ace5ee63a258d4b003da94cdeb1039bc515c"
RUNTIME_EVIDENCE = ROOT / "tools/seeds/bally/embryon-1981-solenoid-self-test.json"
RUNTIME_HASH = "acf96625f0f544dd3c1fa7491c311f000e7159493b8cfb9be657c1ed49280b02"

SWITCHES = [
    "10 point rebound", "Rollover buttons", "Right flipper button", "Saucer",
    "Left and right of outhole", "Credit button", "Tilt", "Outhole",
    "Coin III right", "Coin I left", "Coin II middle", "A rollover",
    "B rollover", "Right outlane", "Left outlane", "Slam",
    "Single drop target and back target", "Spinner", "Top center rollover",
    "Top drop target upper", "Top drop target center", "Top drop target lower",
    "1 rollover", "2 rollover", "Left drop target upper", "Left drop target center",
    "Left drop target lower", "Left side captive ball target", "Center right upper target",
    "Center right lower target", "Center left lower target", "Center left upper target",
    "Right center inside target", "Left center inside target", "Right slingshot",
    "Left slingshot", "Right bottom thumper bumper", "Right top thumper bumper",
    "Left bottom thumper bumper", "Left top thumper bumper",
]
COILS = {
    1: (9, "Single drop target reset"), 2: (10, "Left three-bank reset"),
    3: (11, "Top three-bank reset"), 4: (12, "Saucer"), 5: (8, "Outhole kicker"),
    6: (7, "Knocker"), 10: (3, "Left top thumper bumper"),
    11: (4, "Left bottom thumper bumper"), 12: (5, "Right top thumper bumper"),
    13: (6, "Right bottom thumper bumper"), 14: (1, "Left slingshot"),
    15: (2, "Right slingshot"), 18: (13, "Coin lockout"),
    19: (14, "Flipper enable relay"), 20: (15, "Right outlane flipper"),
}
COIL_PARTS = {
    1: "AO-27-1300", 2: "NO26-1900", 3: "NO26-1900", 4: "AO-27-1300",
    5: "AO-27-1300", 6: "AR-26-1200", 10: "AN-26-1200", 11: "AN-26-1200",
    12: "AN-26-1200", 13: "AN-26-1200", 14: "AO-26-1200", 15: "AO-26-1200",
    18: "FO-36-7000", 20: "AO-27-1300", 46: "AQ-25-500/34-4500", 48: "AQ-25-500/34-4500",
}
DIP_LABELS = {
    6: "Top drop target feature adjustment", 7: "Bonus value memory",
    8: "Bonus multiplier memory", 14: "Top feature lane arrow memory",
    15: "Single drop target value memory", 16: "Left three-drop value memory",
    21: "Center outside target lights per hit", 22: "Center outside target memory",
    23: "1 and 2 lane memory", 24: "A and B lane memory",
    25: "Maximum credits bit 1", 26: "Maximum credits bit 2",
    27: "Credit display", 28: "Match feature", 29: "Replays per game",
    30: "Game-over attract voice", 31: "Balls per game bit 1", 32: "Balls per game bit 2",
}


def provenance(*refs: str, status: str = "candidate") -> dict:
    return {"status": status, "source_refs": list(refs)}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason,
            "provenance": provenance(*refs)}


def item(group: str, address: int, label: str, kind: str, availability: str,
         refs: tuple[str, ...]) -> dict:
    namespace = {"switch": "pinmame.switch", "dip": "pinmame.dip",
                 "solenoid": "pinmame.solenoid", "lamp": "pinmame.lamp"}[group]
    direction = "input" if group in ("switch", "dip") else "output"
    return {"id": f"{group}.{address if address >= 0 else 'minus-' + str(-address)}",
            "label": label, "kind": kind, "availability": availability,
            "binding": {"group": f"pinmame.{direction}.{group}", "device": address},
            "aliases": [{"namespace": namespace, "value": str(address)}],
            "provenance": provenance(*refs)}


def build() -> dict:
    for path, digest in [(BULB_SEED, BULB_HASH), (RESET_EVIDENCE, RESET_HASH)]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Pinned Embryon evidence changed: {path}")
    if not EXCERPT.is_file() or hashlib.sha256(EXCERPT.read_bytes()).hexdigest() != EXCERPT_HASH:
        raise ValueError("candidate manual excerpt missing or changed")
    if hashlib.sha256(IDENTITY_EXCERPT.read_bytes()).hexdigest() != IDENTITY_HASH:
        raise ValueError("IPDB identity excerpt changed")
    if hashlib.sha256(DIP_EXCERPT.read_bytes()).hexdigest() != DIP_HASH:
        raise ValueError("candidate DIP excerpt changed")
    if hashlib.sha256(SPATIAL_SEED.read_bytes()).hexdigest() != SPATIAL_HASH:
        raise ValueError("spatial source seed changed")
    if hashlib.sha256(RUNTIME_EVIDENCE.read_bytes()).hexdigest() != RUNTIME_HASH:
        raise ValueError("compact runtime evidence changed")
    if hashlib.sha256(FLIP_EVIDENCE.read_bytes()).hexdigest() != FLIP_HASH:
        raise ValueError("compact flipper evidence changed")
    for name, digest in EXTRA_EVIDENCE.items():
        if hashlib.sha256((EXCERPT.parent / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"excerpt missing or changed: {name}")
    geometry = json.loads(SPATIAL_SEED.read_text(encoding="utf-8"))
    inp = []
    for n, label in enumerate(SWITCHES, 1):
        d = item("switch", n, label, "switch", "used", (MANUAL, CORE, SWITCH_SCHEMATIC))
        d["provenance"] = provenance(MANUAL, CORE, SWITCH_SCHEMATIC, status="validated")
        d["aliases"] += [{"namespace": "vpe-legacy.switch", "value": v}
                         for v in dict.fromkeys((str(n), f"{n:02}", f"{n:03}"))]
        d["aliases"].append({"namespace": "manual.self-test", "value": f"{n:02}"})
        d["normally_closed"] = False
        if n in (1, 2, 5, 7, 16):
            d["physical"] = {"quantity": {1: 4, 2: 3, 5: 2, 7: 3, 16: 2}[n]}
        if n in (3, 6, 7, 9, 10, 11, 16):
            d["spatial"] = na("cabinet_or_service", MANUAL)
        if n == 3:
            d["physical"] = {"notes": "Assert this matrix input alongside synthetic right flipper button 82; FLIP_SW does not copy 82 to 3."}
        if n == 17:
            d["physical"] = {"quantity": 2, "notes": "Normally-open target-down contact in series with the normally-closed back-target contact. The composite matrix circuit rests open; the back target briefly breaks it when the drop is down."}
        inp.append(d)
    for n in range(41, 49):
        d = item("switch", n, f"Unwired switch column position {n}", "virtual", "unused", (CORE, MANUAL, SWITCH_SCHEMATIC, SOLENOID_SCHEMATIC))
        d["physical"] = {"notes": "Manual page 22 lists positions 1-40; Embryon's W-1192-29c fits only ST0-ST4. PinMAME can read a sixth column via PB7, but the machine uses that line for Flipsave output 20, with no sixth-column contacts fitted."}
        d["spatial"] = na("unused", MANUAL, SWITCH_SCHEMATIC)
        inp.append(d)
    for n, label in [(-7, "Self test"), (-6, "CPU diagnostic"), (-5, "Sound diagnostic")]:
        physical_source = {-7: CABINET_SCHEMATIC, -6: MPU_SCHEMATIC, -5: SOUND_SCHEMATIC}[n]
        d = item("switch", n, label, "switch", "used", (CORE, physical_source, "manual.embryon.color"))
        d["normally_closed"] = False
        d["spatial"] = na("cabinet_or_service", CORE, physical_source, "manual.embryon.color")
        inp.append(d)
    for n in range(81, 89):
        used = n in (82, 84)
        d = item("switch", n, {82: "Right flipper button", 84: "Left flipper button"}.get(n, f"Unused flipper column bit {n}"), "switch" if used else "virtual", "used" if used else "unused", (CORE, FLIP_RUN, "manual.embryon.color") if used else (CORE,))
        d["spatial"] = na("cabinet_or_service", CORE, "manual.embryon.color") if used else na("unused", CORE)
        if used:
            d["normally_closed"] = False
            d["physical"] = {"switch_type": "button", "notes": "Physical cabinet button, exposed in PinMAME's synthetic flipper input column."}
        inp.append(d)
    for n in range(1, 33):
        label = DIP_LABELS.get(n)
        if label is None:
            chute = 1 if n <= 5 else 3 if n <= 13 else 2
            label = f"Coin chute {chute} pricing bit {n}"
        d = item("dip", n, label, "dip_switch", "used", (CORE, MANUAL))
        d["physical"] = {"switch_type": "dip"}
        d["spatial"] = na("dip_switch", CORE)
        inp.append(d)
    out = []
    for n in list(range(1, 16)) + list(range(17, 21)):
        if n in COILS:
            test, label = COILS[n]
            d = item("solenoid", n, label, "relay" if n == 19 else "coil", "used", (MANUAL, RUN))
            d["provenance"] = provenance(MANUAL, RUN, SOLENOID_SCHEMATIC, status="validated")
            d["aliases"].append({"namespace": "manual.self-test", "value": f"{test:02}"})
            if n in (6, 18, 19):
                d["spatial"] = na("cabinet_or_service", MANUAL)
        else:
            d = item("solenoid", n, f"Unfitted output {n}", "virtual", "unused", (CORE, RUN, SOLENOID_SCHEMATIC))
            d["spatial"] = na("no_physical_device", CORE)
            if n == 17:
                d["provenance"] = provenance(CORE, RUN, FLIP_RUN, RESET_RUN + "-1", RESET_RUN + "-2", SOLENOID_SCHEMATIC, status="validated")
                d["physical"] = {"notes": "Embryon's solenoid sheet marks the PB4/CONT.2 load N/U. All four raw runs show a shared 17-20 boot pulse, each rising/falling callback set within 1 ms before scenario switch actions. Pinned by35.c:357-359 complements PIA1:B's high nibble (data ^= 0xf0) and maps the whole bank via (data & 0xf0)<<12; exact timestamps and source hash are in the compact solenoid seed. The no-load drawing plus explained public bank behavior supports unused 17. The precise firmware instruction and why the ROM initializes the bank are untraced; transitions do not establish physical fitment."}
        out.append(d)
    for n, label in [(45, "Right flipper duplicate"), (46, "Right flippers"),
                     (47, "Left flipper duplicate"), (48, "Left flipper")]:
        d = item("solenoid", n, label, "virtual" if n in (45, 47) else "coil", "used", (CORE, SCRIPT, FLIP_RUN))
        d["physical"] = {"notes": "The pair is synthetic and held together; it does not measure winding or EOS timing."}
        if n in (45, 47):
            d["spatial"] = na("virtual", CORE)
        else:
            d["physical"]["quantity"] = 2 if n == 46 else 1
        out.append(d)
    out.extend(build_lamps(item, na, provenance))
    for d in inp:
        d["provenance"]["status"] = "validated"
        if d["binding"]["group"] == "pinmame.input.switch" and d["binding"]["device"] in (82, 84):
            d["provenance"] = provenance(CORE, FLIP_RUN, SOLENOID_SCHEMATIC, CABINET_SCHEMATIC, "manual.embryon.color", status="validated")
    for d in out:
        if d["binding"]["group"] == "pinmame.output.solenoid" and d["binding"]["device"] in COIL_PARTS:
            d.setdefault("physical", {})["part_number"] = COIL_PARTS[d["binding"]["device"]]
            if MANUAL not in d["provenance"]["source_refs"]:
                d["provenance"]["source_refs"].append(MANUAL)
        if d["binding"]["group"] == "pinmame.output.solenoid" and d["binding"]["device"] in (18, 19):
            d.setdefault("physical", {})["notes"] = "The modern table uses this output as a GI visual proxy. The machine's wiring identifies coin lockout (18) or the flipper-enable relay (19); fixed GI has no public output here."
            d["provenance"]["source_refs"].append(MODERN)
    def place(device: dict, names: list[str], role: str) -> None:
        b = geometry["bounds"]
        placements = []
        for index, name in enumerate(names):
            x, y = geometry["objects"][name]
            x = (x - b["left"]) / (b["right"] - b["left"])
            y = (y - b["top"]) / (b["bottom"] - b["top"])
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError(f"out-of-bounds object {name}")
            placements.append({"id": f"placement.{device['id']}-{index + 1}", "role": role,
                               "space": "playfield", "x": _round_point(x), "y": _round_point(y),
                               "provenance": provenance(GEOMETRY, SCRIPT, MANUAL, status="observed")})
        device["spatial"] = {"status": "observed", "placements": placements}

    input_places = {2: ["Trigger.sw2a", "Trigger.sw2b", "Trigger.sw2c"],
                    4: ["Kicker.sw4"], 12: ["Trigger.sw12"], 13: ["Trigger.sw13"],
                    14: ["Trigger.sw14"], 15: ["Trigger.sw15"], 18: ["Spinner.sw18"],
                    19: ["Trigger.sw19"], 23: ["Trigger.sw23"], 24: ["Trigger.sw24"],
                    37: ["Bumper.Bumper4"], 38: ["Bumper.Bumper3"],
                    39: ["Bumper.Bumper2"], 40: ["Bumper.Bumper1"]}
    input_places.update({17: ["Wall.t17", "Wall.t17x"], 35: ["Wall.RightSlingshot"],
                         36: ["Wall.LeftSlingshot"]})
    input_places.update({n: [f"Wall.t{n}"] for n in (20, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34)})
    for device in inp:
        n = device["binding"]["device"]
        if device["binding"]["group"] == "pinmame.input.switch" and n in input_places:
            place(device, input_places[n], "sensor")
    output_places = {4: ["Kicker.sw4"], 10: ["Bumper.Bumper1"], 11: ["Bumper.Bumper2"],
                     12: ["Bumper.Bumper3"], 13: ["Bumper.Bumper4"],
                     20: ["Flipper.RightLFlipper"], 46: ["Flipper.RightFlipper", "Flipper.RightUFlipper"],
                     48: ["Flipper.LeftFlipper"]}
    output_places.update({1: ["Wall.t17"], 2: ["Wall.t26"], 3: ["Wall.t21"],
                          14: ["Wall.LeftSlingshot"], 15: ["Wall.RightSlingshot"]})
    for device in out:
        n = device["binding"]["device"]
        if device["binding"]["group"] == "pinmame.output.solenoid" and n in output_places:
            place(device, output_places[n], "effect")
    bulb_data = json.loads(BULB_SEED.read_bytes())
    lamps = {d["binding"]["device"]: d for d in out if d["binding"]["group"] == "pinmame.output.lamp"}
    for row in bulb_data["bulbs"]:
        d = lamps[row["output"]]
        if d["availability"] != "used" or ("spatial" in d and d["spatial"]["status"] == "not_applicable"):
            raise ValueError(f"Bulb conflicts with physical disposition: {row['object']}")
        x, y, _ = [(a + b) / 2 for a, b in zip(*row["bounds"])]
        if not 0 <= x <= 1257 or not 0 <= y <= 1974:
            raise ValueError(f"Bulb outside playfield: {row['object']}")
        spatial = d.setdefault("spatial", {"status": "observed", "placements": []})
        spatial["placements"].append({"id": f"placement.lamp-{row['output']}-{row['object'].lower().replace('_', '-')}",
            "role": "emitter", "space": "playfield", "x": _round_point(x / 1257), "y": _round_point(y / 1974),
            "provenance": provenance(MODERN_GEOMETRY, MODERN, A5 if row["output"] < 65 else A9, status="observed")})
    for d in lamps.values():
        if d.get("spatial", {}).get("placements"):
            d.setdefault("physical", {})["quantity"] = len(d["spatial"]["placements"])
            d["provenance"]["source_refs"].extend([MODERN, MODERN_GEOMETRY])
            d["provenance"]["status"] = "observed"
    for d in inp + out:
        d["provenance"]["source_refs"] = list(dict.fromkeys(d["provenance"]["source_refs"]))
        if d["id"] in ("switch.35", "switch.36", "solenoid.14", "solenoid.15"):
            d.setdefault("physical", {})["notes"] = "Spatial anchor projects this sling assembly to the midpoint of its active rubber edge; it does not enumerate individual switch leaves or measure the coil shaft."
    displays = []
    for index, (label, start, width) in enumerate([(f"Player {n}", 2 + (n-1)*8, 6) for n in range(1, 5)] + [("Credits", 35, 2), ("Match and ball in play", 38, 2)]):
        displays.append({"id": f"display.{index+1}", "label": label, "kind": "segment",
                         "controller_index": index, "segment_start": start, "width": width,
                         "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE, MANUAL),
                         "provenance": provenance(CORE, MANUAL)})
    driver_data = [("embryon", "Embryon", "1981", "Bally"), ("embryona", "Embryon (Free Play)", "2004", "Bally / Oliver"),
                   ("embryonb", "Embryon (7-digit conversion rev. 1)", "2002", "Bally / Oliver"),
                   ("embryonc", "Embryon (7-digit conversion rev. 8)", "2004", "Bally / Oliver"),
                   ("embryond", "Embryon (7-digit conversion rev. 9)", "2004", "Bally / Oliver"),
                   ("embryone", "Embryon (7-digit conversion rev. 92)", "2011", "Bally")]
    drivers = []
    for driver, description, year, manufacturer in driver_data:
        d = {"id": driver, "description": description, "year": year, "manufacturer": manufacturer,
             "flags": 0, "physical_compatibility": "identical" if driver == "embryon" else "compatible"}
        if driver != "embryon":
            d.update(clone_of="embryon", variant_notes="Seven-digit player displays replace the original six-digit layout.",
                     display_overrides=[{"target": f"display.{i+1}", "segment_start": 1+i*8, "width": 7,
                                         "provenance": provenance(CORE)} for i in range(4)])
        drivers.append(d)
    sources = [
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": "46e1a01a0f73dc5ce163d98db1ae435883ecc450", "locator": "src/wpc/by35games.c:1207-1259; by35.c:240-249 sixth-column read and 331-359 PIA1:B continuous-bank mapping (especially 357-359); by35.c SHA-256 91df5b0c8a8ba19c017fec5ea45b7a4e2b911f2a56b9a793de7ad1caddd6f6e2", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": "ipdb.embryon.783", "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=783", "sha256": "76abab82caebe21f3c28a9f6b2783e3eebd31140bd8826d579419df79b5aaff1", "locator": "Retained browser capture ipdb-machine-783.json; IPDB 783 identity, date and model", "source_id": "783", "acquired_at": "2026-11-06T18:15:39.880Z", "attribution": "Internet Pinball Database", "license": "NOASSERTION", "excerpts": [{"id": "ipdb-identity", "locator": "Identity and notable features", "path": IDENTITY_EXCERPT.relative_to(ROOT).as_posix(), "sha256": IDENTITY_HASH, "method": "mixed", "transcribed_by": "curator, visually verified", "reviewed": False}]},
        {"id": MANUAL, "kind": "manual", "uri": "https://arcarc.xmission.com/Pinball/PDF%20Pinball%20Manuals%20and%20Schematics/Embryon.pdf", "sha256": "bca8ac2a339d9b49631f579d90c516cae2713fec5cfe149c2024a7ed23eb03f2", "original_filename": "Embryon.pdf", "acquired_at": "2026-11-06T18:07:59.826928Z", "locator": "PDF pages 6, 8–12 and 22; retained as Embryon-arcarc.pdf", "license": "NOASSERTION", "attribution": "Bally Manufacturing; scan retained from arcarc", "excerpts": [{"id": "manual-page-22", "locator": "PDF page 22", "path": EXCERPT.relative_to(ROOT).as_posix(), "sha256": EXCERPT_HASH, "method": "mixed", "transcribed_by": "curator, visually verified", "reviewed": True}, {"id": "manual-pages-10-12", "locator": "PDF pages 10–12; dense pricing rows pending full cell review", "path": DIP_EXCERPT.relative_to(ROOT).as_posix(), "sha256": DIP_HASH, "method": "model", "transcribed_by": "curator, unreviewed transcription", "reviewed": False}]},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:vpx-sources/bally/embryon-1981/local-v1.4/extraction/script.vbs", "sha256": "60703a639ca2d19a2a4caf2501e2ae62c38c4e76c568f58aa64e9aa2661fde75", "locator": "Embedded script, callbacks and ball stacks; extraction manifest 77e7c44ae196fed770dc82cbf2adedd0f725a409ee5230e10818b02d5b9ccae9", "license": "NOASSERTION", "attribution": "ICPjuggla, OldSkoolGamer, Herweh and contributors", "known_working": True},
        {"id": GEOMETRY, "kind": "vpx_table", "uri": "external:vpx-sources/bally/embryon-1981/local-v1.4/Embryon(Bally 1980)VPXv1.4.vpx", "sha256": "a759546a3b9f2f9b8fa204ac1c81e25526462abd94c0d757a1063b9acc94a5c2", "locator": "Retained extraction, canonical manifest SHA-256 77e7c44ae196fed770dc82cbf2adedd0f725a409ee5230e10818b02d5b9ccae9; bounds 1257 by 1974; exact centers in tools/seeds/bally/embryon-1981-spatial.json", "license": "NOASSERTION", "attribution": "VPX table authors"},
        {"id": RUN, "kind": "runtime_scenario", "uri": "external:review-artifacts/embryon-1981/harness/solenoid-run-1.json", "sha256": "afdc30c3cd55e345e1b1bb53f158967599840bc5277945f75dbaa7ea96ada3ba", "locator": "Fresh ROM service-test display and public solenoid transitions; compact service mapping and all-four-run startup_continuous_bank summary in tools/seeds/bally/embryon-1981-solenoid-self-test.json SHA-256 " + RUNTIME_HASH},
    ]
    def excerpt(name: str, locator: str, reviewed: bool = False) -> dict:
        transcribed_by = "curator, visually verified" if reviewed else "curator, unreviewed transcription"
        return {"id": name[:-3], "locator": locator,
                "path": (EXCERPT.parent / name).relative_to(ROOT).as_posix(),
                "sha256": EXTRA_EVIDENCE[name], "method": "mixed",
                "transcribed_by": transcribed_by,
                "reviewed": reviewed}

    archive = "https://www.ipdb.org/files/783/embryon_schematics.zip"
    def sheet(source_id: str, filename: str, digest: str, locator: str, excerpts: list[dict]) -> dict:
        return {"id": source_id, "kind": "manual", "uri": f"external:manuals/by-machine/bally.embryon.1981/ipdb-schematics/{filename}", "source_id": "783",
                "sha256": digest, "original_filename": filename,
                "locator": f"IPDB 783 zip member {filename} from {archive}; archive SHA-256 c92a259d772ae57e6e99e3b62135307c76e71f281536ce0e7daa8fa01aa67029; {locator}",
                "license": "NOASSERTION", "attribution": "Bally Manufacturing; Internet Pinball Database", "excerpts": excerpts}
    sources.extend([
        sheet(A5, "lamp.tif", "7e618f66ec4844a71114e2af264aaa9f4d92b32342ee30789faf348ad320315f", "A5 decoder and connector branches", [excerpt("main-lamp-map.md", "A5 main decoder, loads and J4", True), excerpt("schematic-connector-tables.md", "A5 J1/J2/J3 connector labels")]),
        sheet(A9, "lampaux.tif", "21e883165297b2052e364249eac59d64a2b1aaad3cffdb30f0d6e8c7d34dc9f9", "A9 decoder and output labels", [excerpt("schematic-connector-tables.md", "A9 outputs")]),
        sheet(WIRING, "wiring1.tif", "470792c15ef8907ab1524634b99ce787472a10d3a0eed87125c518f3c18618f5", "W-1255 feature lamp harness", [excerpt("schematic-connector-tables.md", "W-1255 feature lamp harness")]),
        sheet(SWITCH_SCHEMATIC, "switch.tif", "cd75ab89604b39a2b755f46ae2c3d4682ac50f982ef78b028e0cff92c2d0383f", "W-1192-29c switch wiring", [excerpt("switch17-series.md", "Single-drop and back-target series circuit", True), excerpt("switch-column-fitment.md", "W-1192-29c: five ST0-ST4 branches on A4J2 pins 1-5; Flipsave coil circuit", True)]),
        sheet(SOLENOID_SCHEMATIC, "sol.tif", "cbda1f7f1c2f184f1ec339aa6ff0716ca40ae02684c8a06ceb5b5475dee7bd43", "Solenoid outputs and N/U positions", [excerpt("solenoid-fitment.md", "Decoder fitment", True)]),
        sheet(CABINET_SCHEMATIC, "switch1.tif", "8395c33a4cd59785f39b546e5dca73b35a6049e2463062606980997a0e041496", "W-1186-12c TEST SW and RIGHT/LEFT FLIPPER SWITCH contacts", [excerpt("service-polarity.md", "W-1186-12c cabinet contacts", True)]),
        sheet(MPU_SCHEMATIC, "mpu.tif", "edb79950e418341c862666e69eef28f8292bbd641a8eb8622fbaca9a485477f3", "W-1181-3c S33 ACTIVITY above U9", [excerpt("service-polarity.md", "W-1181-3c S33 contact", True)]),
        sheet(SOUND_SCHEMATIC, "sound.tif", "d364f4e7c2483f200d96e484c4ce3fd20c9799ac760fa71bd542fc0dd77410d8", "W-1230-1 SW1 TEST SW beside U1", [excerpt("service-polarity.md", "W-1230-1 SW1 contact", True)]),
        {"id": "manual.embryon.color", "kind": "manual", "uri": "https://www.ipdb.org/files/783/Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf", "source_id": "783", "sha256": "55c800db586661821e84300aaf57fa24d825a492e78a94d41130b5916dcbe07b", "original_filename": "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf", "acquired_at": "2026-11-06T18:12:29.351736Z", "locator": "IPDB game https://www.ipdb.org/machine.cgi?id=783; PDF 39 cabinet, 40 playfield, 51 solenoid, 47 main lamps, 50 auxiliary, 52 flasher; primary switch17 crop SHA-256 0f3c12798feb96f6450b63bf3a67259d6c7e72951830dc8a13dfe44740f62b0b", "license": "NOASSERTION", "attribution": "Bally Manufacturing; Internet Pinball Database", "excerpts": [excerpt("switch17-series.md", "PDF page 40 series circuit", True), excerpt("main-lamp-map.md", "PDF pages 40, 47 and 52 main and flasher wiring", True)]},
        {"id": LIBRARY, "kind": "vpx_script", "uri": "external:vpx-sources/bally/embryon-1981/libraries/core.vbs", "sha256": "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69", "locator": "vpmTimer.Update, PulseSw and cvpmDropTarget.SolDropUp; retained from user VPinMAME script library", "license": "NOASSERTION", "attribution": "VPinMAME core.vbs contributors", "excerpts": [excerpt("runtime-bindings.md", "Timer and switch 17 workaround")]},
        {"id": MODERN, "kind": "vpx_script", "uri": "external:vpx-sources/bally/embryon-1981/unclepaulie-2.0.2/extraction/script.vbs", "sha256": "7c4630d1d1805020b24b578013a5ad3255ee943495a6931c69ec2c7a427d503e", "acquired_at": "2026-11-06T18:23:53.543Z", "locator": "UpdateDTLamps and UpdateVRLamps; release https://vpuniverse.com/files/file/15595-embryon-bally-1981-w-vr-room/; source VPX SHA-256 b825e72293a452017a28f5ece39ed71b8fd6ab28edfdf6d0aef9addb14e5bb83; extraction manifest b54f92817455a7da1716c7929adafab4bf96acfe3a30093d87fa2649eede89d8", "license": "NOASSERTION", "attribution": "UnclePaulie and contributors", "excerpts": [excerpt("runtime-bindings.md", "Backbox callbacks and GI proxy")]},
        {"id": FLIP_RUN, "kind": "runtime_scenario", "uri": "external:review-artifacts/embryon-1981/harness/flipper-run-1.json", "sha256": "5edf495a5eab7262fcd3fb9d7d7ae3d7506f193bf705d2ac8c376e2c22e647b7", "locator": "Held button and tilt snapshots; compact tools/seeds/bally/embryon-1981-flipper-tilt.json SHA-256 " + FLIP_HASH + "; boot bank 17-20: tools/seeds/bally/embryon-1981-solenoid-self-test.json:startup_continuous_bank SHA-256 " + RUNTIME_HASH},
    ])
    next(s for s in sources if s["id"] == SCRIPT)["excerpts"] = [excerpt("runtime-bindings.md", "Ball stacks, callbacks and switch 17")]
    manual_source = next(s for s in sources if s["id"] == MANUAL)
    manual_source["excerpts"].extend([excerpt("manual-rules.md", "PDF pages 6, 8 and 9", True),
                                      excerpt("manual-parts.md", "PDF page 25 ASSEMBLY COILS region", True),
                                      excerpt("service-polarity.md", "PDF page 35, printed page 30, sound-module heading", True)])
    manual_source["locator"] = "PDF pages 6, 8–12, 22, 25 and 35; retained as Embryon-arcarc.pdf"
    dip_excerpt = next(e for e in manual_source["excerpts"] if e["id"] == "manual-pages-10-12")
    dip_excerpt.update(locator="PDF pages 10–12, all option and pricing tables", method="mixed",
                       transcribed_by="curator, visually verified cell by cell", reviewed=True)
    next(s for s in sources if s["id"] == "ipdb.embryon.783")["excerpts"][0]["reviewed"] = True
    for source_id in (A5, A9, WIRING):
        for e in next(s for s in sources if s["id"] == source_id)["excerpts"]:
            e.update(reviewed=True, transcribed_by="curator, visually verified")
    modern_source = next(s for s in sources if s["id"] == MODERN)
    modern_source["known_working"] = True
    next(s for s in sources if s["id"] == CORE)["excerpts"] = [excerpt("runtime-bindings.md", "by35.c:134–166, 261 and 277; lamp data capture and separate address latches", True), excerpt("solenoid-fitment.md", "by35.c:331-359, especially 357-359; PIA1:B continuous bank", True), excerpt("switch-column-fitment.md", "by35.c:240-249; sixth switch-column select via PB7", True), excerpt("service-polarity.md", "by35.h:229-231; by35.c:475-484; by35games.c:1207; by35snd.c:464-465,591-593; core.h:332,352-354; core.c:2209", True)]
    modern_source["excerpts"].append(excerpt("modeled-bulbs.md", "Lampz callbacks, FlInitBumper and GIMidLane", True))
    sources.append({"id": MODERN_GEOMETRY, "kind": "vpx_table",
        "uri": "external:vpx-sources/bally/embryon-1981/unclepaulie-2.0.2/download/Embryon (Bally 1981) w VR Room v2.0.2.vpx",
        "sha256": "b825e72293a452017a28f5ece39ed71b8fd6ab28edfdf6d0aef9addb14e5bb83",
        "attribution": "UnclePaulie and contributors", "license": "NOASSERTION",
        "locator": "VPX v2.0.2; vpxtool git:v0.33.3 export obj --units vpu; OBJ SHA-256 " + bulb_data["obj_sha256"] + "; canonical extraction manifest " + bulb_data["manifest_sha256"],
        "excerpts": [excerpt("modeled-bulbs.md", "Individual bulb meshes and independently positioned controls", True)]})
    reset_data = json.loads(RESET_EVIDENCE.read_bytes())
    for i, run in enumerate(reset_data["runs"], 1):
        sources.append({"id": RESET_RUN + f"-{i}", "kind": "runtime_scenario",
            "uri": "external:review-artifacts/embryon-1981/" + run["raw_path"], "sha256": run["raw_sha256"],
            "locator": "Fresh state, two physical switch-17 break/restoration sequences; compact tools/seeds/bally/embryon-1981-single-drop.json SHA-256 " + RESET_HASH + "; boot bank 17-20: tools/seeds/bally/embryon-1981-solenoid-self-test.json:startup_continuous_bank SHA-256 " + RUNTIME_HASH})
    color_source = next(s for s in sources if s["id"] == "manual.embryon.color")
    # Literal render_excerpt_image.py stdout; pinned-toolchain byte reproduction
    # is retained externally in crop-reproduction/.
    color_source["locator"] += "; PDF 39 cabinet service contacts, 45 sound SW1, 46 MPU S33; crop renderer: PyMuPDF 1.28.2, Pillow 12.3.0, libwebp 1.6.0"
    crops = [
        ("switch17-series.md", "switch17-series-p40.webp", "0f3c12798feb96f6450b63bf3a67259d6c7e72951830dc8a13dfe44740f62b0b", "40, crop box 0.05,0.66,0.38,0.91",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 40, crop box 0.05,0.66,0.38,0.91, scanned page rendered at its native resolution (embedded image xref 145, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 1276x1090 WebP quality 80"),
        ("main-lamp-map.md", "a10-flasher.webp", "b1a629d56b24fbe635293cb9ff6a1a03109cf65808de785277fc03f01d390e0f", "52, crop box 0.25,0.2,0.75,0.8",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 52, crop box 0.25,0.2,0.75,0.8, scanned page rendered at its native resolution (embedded image xref 182, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 3060x1651 WebP quality 80"),
        ("solenoid-fitment.md", "solenoid-unfitted.webp", "760cd88f3278d190dfdf520326ea0a15ddba4313481e39b86cb179dabf56a23b", "51, crop box 0.38,0.41,0.62,0.84",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 51, crop box 0.38,0.41,0.62,0.84, scanned page rendered at its native resolution (embedded image xref 180, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 2193x793 WebP quality 80"),
        ("solenoid-fitment.md", "solenoid-continuous.webp", "f4aa5846e7dc629d87408f7d451b332802e5693aa6bf1ec9dba5346096268411", "51, crop box 0.06,0.045,0.43,0.44",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 51, crop box 0.06,0.045,0.43,0.44, scanned page rendered at its native resolution (embedded image xref 180, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 2015x1222 WebP quality 80"),
        ("service-polarity.md", "service-cabinet-switches.webp", "c710ff968f18779a582d229af2e2d795c645ef7ccfcb39d3c40bc6789f221fcc", "39, crop box 0.56,0.43,0.82,0.96",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 39, crop box 0.56,0.43,0.82,0.96, scanned page rendered at its native resolution (embedded image xref 143, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 2703x859 WebP quality 80"),
        ("service-polarity.md", "cpu-diagnostic-contact.webp", "07900bc0aa7dc973eaacc18787e634a2a34869446c055ba6b14bed6d71c77e64", "46, crop box 0.15,0.66,0.41,0.745",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 46, crop box 0.15,0.66,0.41,0.745, scanned page rendered at its native resolution (embedded image xref 166, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 435x859 WebP quality 80"),
        ("service-polarity.md", "sound-diagnostic-contact.webp", "7f614255f0761b49c637b62652087894f11806c8b6695137299bbc4be36d27c5", "45, crop box 0.11,0.7,0.27,0.8",
         "Bally_1981_Embryon_English_Manual_in_color_with_paginated_schematics.pdf page 45, crop box 0.11,0.7,0.27,0.8, scanned page rendered at its native resolution (embedded image xref 159, 3328px across 11.10in), rendered at 300 dpi, grayscale, rotated 270 degrees counter-clockwise, 511x529 WebP quality 80"),
    ]
    color_source["excerpts"] = []
    for name, image_name, digest, region, derivation in crops:
        image_path = EXCERPT.parent / image_name
        if hashlib.sha256(image_path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Drawing crop missing or changed: {image_name}")
        e = excerpt(name, "PDF page " + region, True)
        e.update(id=image_name[:-5], image=image_path.relative_to(ROOT).as_posix(), image_sha256=digest,
                 image_derivation=derivation)
        color_source["excerpts"].append(e)
    single_drop = next(d for d in inp if d["id"] == "switch.17")
    single_drop["provenance"]["source_refs"].extend([RESET_RUN + "-1", RESET_RUN + "-2"])
    mechanisms = [
        {"id": "mechanism.trough", "label": "Two-ball trough and outhole", "kind": "other", "actuators": ["solenoid.5"], "sensors": ["switch.5", "switch.8"], "behavior": "The retained script initializes a two-ball stack with switches 8 and 5 and serves on output 5; switch 5 is shared by two physical contacts.", "provenance": provenance(SCRIPT, MANUAL)},
        {"id": "mechanism.saucer", "label": "Lock saucer", "kind": "kicker", "actuators": ["solenoid.4"], "sensors": ["switch.4"], "behavior": "Switch 4 senses the saucer; output 4 ejects the ball in the retained table.", "provenance": provenance(SCRIPT, MANUAL)},
        {"id": "mechanism.top-bank", "label": "Top three drop targets", "kind": "drop_target_bank", "actuators": ["solenoid.3"], "sensors": ["switch.20", "switch.21", "switch.22"], "behavior": "The retained table resets the three individually sensed targets together on output 3.", "provenance": provenance(SCRIPT, MANUAL)},
        {"id": "mechanism.left-bank", "label": "Left three drop targets", "kind": "drop_target_bank", "actuators": ["solenoid.2"], "sensors": ["switch.25", "switch.26", "switch.27"], "behavior": "The retained table resets the three individually sensed targets together on output 2.", "provenance": provenance(SCRIPT, MANUAL)},
        {"id": "mechanism.single-drop", "label": "Single drop and back target", "kind": "drop_target_bank", "actuators": ["solenoid.1"], "sensors": ["switch.17"], "behavior": "The target-down NO contact is in series with the NC back contact. A back hit breaks and restores switch 17 while the drop is down; both fresh native runs pulse reset output 1 on restoration. The raised target then clears switch 17. The table's TRUE/FALSE pulse and forced raise are a workaround.", "provenance": provenance(SCRIPT, MANUAL, SWITCH_SCHEMATIC, RESET_RUN + "-1", RESET_RUN + "-2", status="observed")},
        {"id": "mechanism.captive-balls", "label": "Captive and messenger balls", "kind": "other", "actuators": [], "sensors": ["switch.28", "switch.29", "switch.30", "switch.31", "switch.32", "switch.33", "switch.34"], "behavior": "Five captive balls accompany two free balls: one behind the left bank operates 28, one behind the single drop operates the back contact of 17, and a shared center ball transmits momentum to two inside balls at 33/34. Completing outside targets 29–32 enables letter awards on inside hits; simultaneous inside hits award two letters and a flash. Travel and animation timing remain table tuning.", "provenance": provenance(SCRIPT, MANUAL, "ipdb.embryon.783", status="observed")},
        {"id": "mechanism.flippers", "label": "Flippers and Flipsave", "kind": "other", "actuators": ["solenoid.19", "solenoid.20", "solenoid.46", "solenoid.48"], "sensors": ["switch.3", "switch.82", "switch.84"], "behavior": "Output 19 enables flippers; synthetic pairs follow buttons, while 20 separately drives the right outlane Flipsave flipper.", "provenance": provenance(CORE, SCRIPT, MANUAL)},
    ]
    return {"format": "pinmame-machine-definition", "schema_version": 2,
            "machine": {"id": "bally.embryon.1981", "name": "Embryon", "manufacturer": "Bally", "year": 1981, "kind": "physical_pinball", "model_number": "1222", "ipdb_id": 783, "opdb_id": "G4qk7-MNEjx", "playfield": {"width": 1257, "height": 1974, "units": "vpx", "provenance": provenance(GEOMETRY, status="observed")}},
            "coverage": {"status": "partial", "missing": ["output_semantics", "mechanism_behavior", "variant_differences", "provenance", "spatial_placement", "unresolved_conflicts"],
                         "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "conflicted", "mechanisms": "observed", "variant_coverage": "candidate", "recreation_knowledge": "observed", "spatial_placement": "observed"}},
            "controller": {"platform": "pinmame.by35", "hardware_generation": "0x400000", "inversion_applied_by_emulator": True}, "drivers": drivers, "inputs": inp, "outputs": out, "displays": displays, "mechanisms": mechanisms, "relationships": [], "sources": sources,
            "knowledge": {"path": "knowledge/bally/embryon-1981.md", "status": "partial"},
            "conflicts": [{"id": "conflict.captive-ball-lamp-counts", "path": "outputs.lamp.70-and-86.physical.quantity", "description": "The A9 schematic labels right/left captive-ball lamp counts 2/1, while W-1255 labels them 1/2. Existing photographs do not identify circuit membership. Resolution path: an owner should trace A9J2-6 and A9J2-13 to their bulbs and count each circuit's fitted sockets.", "source_refs": [A9, WIRING]}]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if PROMOTED.exists():
        raise SystemExit("Refusing to overwrite an author-ready definition")
    payload = (json.dumps(build(), indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    outputs = {OUTPUT: payload}
    for seed, (target, digest) in TEXT_SEEDS.items():
        data = seed.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise SystemExit(f"Pinned seed changed: {seed}")
        outputs[target] = data
    if args.check:
        for target, data in outputs.items():
            if not target.is_file() or target.read_bytes() != data:
                raise SystemExit(f"Embryon artifact drift: {target}")
        print("Embryon artifacts are current")
    else:
        for target, data in outputs.items():
            target.write_bytes(data)


if __name__ == "__main__":
    main()
