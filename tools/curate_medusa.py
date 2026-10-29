"""Reproduce the evidence-led, deliberately partial Bally Medusa definition.

The literal electrical tables are Medusa's own, not a sibling's. Geometry is
candidate data produced by the repository VPX extractor. No render helper is
promoted to a measured socket. --check never writes, including on bad inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "bally.medusa.1981"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
DEFINITION_PATH = ROOT / "machines/partial/bally/medusa-1981.json"
SEED_PATH = ROOT / "tools/seeds/bally/medusa-1981.json"
NOTE_PATH = ROOT / "knowledge/bally/medusa-1981.md"
NOTE_SEED = ROOT / "tools/seeds/bally/medusa-1981-knowledge.md"
GEOMETRY_PATH = ROOT / "evidence/spatial/bally.medusa.1981.json"
MANUAL_GEOMETRY_PATH = ROOT / "tools/seeds/bally/medusa-1981-manual-geometry.json"
BULBS_PATH = ROOT / "tools/seeds/bally/medusa-1981-bulbs.json"
REPORT_PATH = ROOT / "reports/spatial/bally/medusa-1981.json"
REPORT_MD_PATH = ROOT / "reports/spatial/bally/medusa-1981.md"
EXCERPTS = ROOT / "evidence/excerpts" / MACHINE_ID
TABLE_HASH = "35598302510b003baf68b5f9a274010b7325e639206c33203ff802f758eb7c3f"
SCRIPT_HASH = "53cb05307a911b62104a18d0b8bbda667775071712de4a51bffec78ef60b148d"
MANIFEST_HASH = "9754b28148f1c2661fbcd795e97b5e45bb514eadfd6715febd0ecc7c8c26021c"
MANUAL_HASH = "6137807222d614505ac923df7acd24c091449cf45f1d4d383ab82939d0df6a7b"
SCHEMATIC_HASH = "a4a8d3c6717cde7afc8015e556400ddec19c420bc1f3990977c8514a872b93b6"
PARTS_HASH = "87272502a90b90b6ee77732e230c61f4281af950f4dc1d2a8da07f0bb9cad295"
CORE = "pinmame.medusa"
MANUAL = "manual.medusa"
SCHEMATIC = "schematics.medusa"
PARTS = "parts.medusa"
SCRIPT = "vpx-script.medusa"
TABLE = "vpx-table.medusa"
RUNTIME = "runtime.medusa"
LIBRARY = "vbs.medusa"
PHOTOS = "photos.medusa"
MESH = "vpx-mesh.medusa"

SWITCH_LABELS = {
    1: "4 Drop Target D (Bottom)", 2: "4 Drop Target C", 3: "4 Drop Target B", 4: "4 Drop Target A (Top)",
    6: "Credit Button", 8: "Outhole", 9: "Coin III (Right)", 10: "Coin I (Left)", 11: "Coin II (Middle)",
    12: "Left Side Top Target", 13: "Left Side Middle Target", 14: "Left Side Bottom Target",
    15: "Tilt", 16: "Slam Tilt", 17: "Cabinet Post Button", 18: "Two 10 Point Rubbers and 4 Drop Target Rebound",
    19: "Saucer", 20: "#1 Shooter Lane Rollover Button", 21: "#2 Shooter Lane Rollover Button",
    22: "#3 Shooter Lane Rollover Button", 23: "#4 Shooter Lane Rollover Button", 24: "#5 Shooter Lane Rollover Button",
    25: "Right and Left Lower Gate", 26: "Right Top Gate", 27: "Top Right Back Target", 28: "Left Top Gate",
    29: "Top Left Back Target", 30: "Top Middle Back Target", 31: "Left and Right Outlane Rollover Button",
    32: "Left and Right Outlane", 33: "Spinner", 34: "Top Right Slingshot", 35: "Bottom Right Slingshot",
    36: "Left Slingshot", 37: "Right Top Thumper Bumper", 38: "Left Top Thumper Bumper",
    39: "Right Bottom Thumper Bumper", 40: "Left Bottom Thumper Bumper", 41: "Movable Flipper Open Limit",
    42: "#7 Top Drop Target (Right)", 43: "#6 Top Drop Target", 44: "#5 Top Drop Target",
    45: "#4 Top Drop Target", 46: "#3 Top Drop Target", 47: "#2 Top Drop Target", 48: "#1 Top Drop Target (Left)",
}
CABINET_SWITCHES = {6, 9, 10, 11, 15, 16, 17}
SWITCH_OBJECTS = {i: [f"sw{i}"] for i in SWITCH_LABELS if i not in CABINET_SWITCHES}
SWITCH_OBJECTS.update({8: ["BallRelease"], 18: ["sw18", "sw18a", "sw18b"], 25: ["sw25", "sw25a"],
                       31: ["sw31", "sw31a"], 32: ["sw32", "sw32a"], 34: ["sw34"],
                       35: ["RightSlingShot"], 36: ["LeftSlingShot"], 37: ["Bumper4"],
                       38: ["Bumper1"], 39: ["Bumper3"], 40: ["Bumper2"], 41: ["sw33"]})
ROW_WIRES = [("54", 8), ("63", 9), ("57", 10), ("78", 11), ("60", 12), ("56", 13), ("65", 14), ("52", 15)]
COLUMN_WIRES = [("51", "A4J2-1"), ("70", "A4J2-2"), ("93", "A4J2-3"), ("53", "A4J2-4"), ("31", "A4J2-5"), ("72", "A4J4-8")]

# Public address: label, transistor, physical connector, effect anchors. A paired
# label means two relay-selected loads; it does not create another public address.
SOLENOIDS = {
    1: ("Knocker / Open Movable Flipper", "Q2", "A3J1-3", ["sw33"]),
    2: ("4 Drop Target Reset / Close Movable Flipper", "Q1", "A3J1-2", ["sw2", "sw33"]),
    3: ("7 Drop Target Reset / #1 Top Drop Target", "Q5", "A3J2-10", ["sw45", "sw48"]),
    4: ("#2 / #3 Top Drop Target Knockdown", "Q6", "A3J2-11", ["sw47", "sw46"]),
    5: ("#4 / #5 Top Drop Target Knockdown", "Q7", "A3J2-12", ["sw45", "sw44"]),
    6: ("#6 / #7 Top Drop Target Knockdown", "Q3", "A3J2-5", ["sw43", "sw42"]),
    7: ("Shield of the Gods Post", "Q4", "A3J1-5", ["Post"]),
    8: ("Outhole / Saucer Kicker", "Q8", "A3J5-10", ["BallRelease", "sw19"]),
    9: ("Bottom Left Thumper Bumper", "Q13", "A3J5-12", ["Bumper2"]),
    10: ("Bottom Right Thumper Bumper", "Q14", "A3J5-11", ["Bumper3"]),
    11: ("Top Left Thumper Bumper", "Q9", "A3J5-9", ["Bumper1"]),
    12: ("Top Right Thumper Bumper", "Q10", "A3J5-15", ["Bumper4"]),
    13: ("Left Slingshot", "Q12", "A3J5-13", ["LeftSlingShot"]),
    14: ("Bottom Right Slingshot", "Q11", "A3J5-14", ["RightSlingShot"]),
    15: ("Top Right Slingshot", "Q16", "A3J5-8", ["sw34"]),
}
PAIRED = {1, 2, 3, 4, 5, 6, 8}
SOLENOID_IDS = {i: "coil." + re.sub(r"[^a-z0-9]+", "-", s[0].lower()).strip("-") for i, s in SOLENOIDS.items()}

# Complete A5 channel table: address | SCR | connector | literal function.
MAIN_LAMPS = """1|Q14|J1-18|10K Right Gate Lane
2|Q12|J1-19|50K Right Gate Lane
3|Q13|J1-17|50K Saucer
4|Q8|J1-23|Left and Right Gate Lane Arrow
5|Q9|J1-14|2X Left Gate Lane
6|Q10|J1-15|1K Medusa Bonus
7|Q11|J1-16|5K Medusa Bonus
8|Q4|J1-28|9K Medusa Bonus
9|Q1|J1-24|Special Saucer
10|Q2|J1-25|Top B Arrow
11|Q3|J2-21|Shoot Again (Backbox)
12|Q7|J1-27|#1 Target Arrow
13|Q16|J2-22|Ball in Play
14|Q5|J2-16|30K Colossus Bonus
15|Q6|J2-14|150K Colossus Bonus
17|Q29|J1-1|20K Right Gate Lane
18|Q27|J1-9|Special Right Gate Lane
19|Q28|J1-8|100K Saucer
20|Q35|J1-3|3 Advance Olympus
21|Q34|J1-2|3X Left Gate Lane / 2X Bonus
22|Q22|J1-10|2K Medusa Bonus
23|Q26|J1-7|6K Medusa Bonus
24|Q25|J1-6|10K Medusa Bonus
25|Q24|J1-5|Saucer Bonus Arrow
26|Q17|J1-11|Top A Arrow
27|Q23|J2-8|Match
28|Q21|J1-12|#2 Target Arrow
29|Q15|J2-23|High Score to Date
30|Q18|J2-20|60K Colossus Bonus
31|Q19|J2-15|Colossus Special
33|Q36|J3-26|30K Right Gate Lane
34|Q38|J3-25|Solenoid Expander Relay
35|Q44|J3-19|150K Saucer
36|Q49|J3-17|2 Advance Olympus
37|Q48|J3-16|5X Left Gate Lane / 3X Bonus
38|Q37|J3-23|3K Medusa Bonus
39|Q32|J3-27|7K Medusa Bonus
40|Q20|J1-13|20K Medusa Bonus
41|Q42|J3-21|Last Ball Extended Play
42|Q41|J3-20|60K Medusa Bonus
43|Q40|J3-22|Same Player Shoot Again (Playfield)
44|Q39|J3-24|#3 Target Arrow
45|Q33|J2-11|Game Over
46|Q30|J2-6|90K Colossus Bonus
47|Q31|J2-2|Top Middle Back Target
49|Q57|J3-1|40K Right Gate Lane
50|Q50|J3-12|Not Used Main Lamp Channel
51|Q51|J3-15|200K Saucer
52|Q54|J3-11|1 Advance Olympus
53|Q55|J3-9|50K Left Gate Lane / 5X Bonus
54|Q60|J3-3|4K Medusa Bonus
55|Q59|J3-4|8K Medusa Bonus
56|Q58|J3-2|40K Medusa Bonus
57|Q56|J3-10|Saucer Extended Play Arrow
58|Q46|J3-18|80K Medusa Bonus
59|Q52|J3-13|Credit Indicator
60|Q53|J3-14|#21 Top of Panel (Right)
61|Q47|J2-10|Tilt
62|Q43|J2-7|120K Colossus Bonus
63|Q45|J2-1|Special Medusa"""

# A9 wiring is read independently from W-1207-10 and W-1255-1.
AUX_PINS = [("J2-7", "10"), ("J2-4", "15"), ("J2-8", "51"), ("J2-10", "80"), ("J2-9", "54"), ("J2-6", "45"), ("J2-5", "60"),
            ("J2-14", "12"), ("J2-11", "18"), ("J2-15", "52"), ("J2-18", "57"), ("J2-17", "43"), ("J2-13", "40"), ("J2-12", "62"),
            ("J3-8", "13"), ("J3-3", "20"), ("J3-9", "53"), ("J3-11", "70"), ("J3-10", "25"), ("J3-7", "82"), ("J3-4", "95"),
            ("J3-15", "14"), ("J3-12", "21"), ("J3-16", "56"), ("J3-18", "72"), ("J3-17", "23"), ("J3-14", "27"), ("J3-13", "96")]
DIP_LABELS = {6: "Top Center Back Target Subtract Bonus", 7: "Colossus Bonus Memory", 8: "Movable Flipper Timer",
              14: "High Score Feature", 15: "Left Side Target Arrow Memory", 16: "Medusa Special Threshold",
              21: "Olympus Threshold Selector S21", 22: "Olympus Threshold Selector S22", 23: "Extra Ball Number Memory",
              24: "Medusa Bonus Memory", 25: "Maximum Credits Selector S25", 26: "Maximum Credits Selector S26",
              27: "Credit Display", 28: "Match Feature", 29: "Replays Per Game", 30: "Saucer Olympus Arrow Memory",
              31: "Balls Per Game Selector S31", 32: "Balls Per Game Selector S32"}
for _range, _chute in [(range(1, 6), "I (Left)"), (range(9, 14), "III (Right)"), (range(17, 21), "II (Center)")]:
    DIP_LABELS.update({i: f"Coin {_chute} Pricing S{i}" for i in _range})


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(refs)}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def placements(identifier: str, role: str, names: list[str]) -> dict:
    objects = {o["name"].casefold(): o for o in load_json(GEOMETRY_PATH)["objects"]}
    result = []
    for name in names:
        obj = objects[name.casefold()]
        result.append({"id": f"{identifier}.{name.lower()}", "space": "playfield", "role": role,
                       "x": obj["x"], "y": obj["y"], "provenance": provenance(TABLE, SCRIPT, SCHEMATIC, status="observed")})
    return {"status": "observed", "placements": result}


def outhole_projection(identifier: str, role: str) -> dict:
    from drawing_callouts import apply, fit
    objects = {o["name"].casefold(): o for o in load_json(GEOMETRY_PATH)["objects"]}
    seed = load_json(MANUAL_GEOMETRY_PATH)
    pairs = [(c["pixel"], (objects[c["object"].casefold()]["x"], objects[c["object"].casefold()]["y"])) for c in seed["controls"]]
    x, y = apply(fit(pairs), seed["measurements"]["outhole"]["pixel"])
    return {"status": "observed", "placements": [{"id": identifier + ".manual-outhole", "space": "playfield", "role": role, "x": round(x, 6), "y": round(y, 6), "provenance": provenance(MANUAL, TABLE, status="observed")}]}


def display_projection(identifier: str, first_digit: int) -> dict:
    objects = {o["name"]: o for o in load_json(GEOMETRY_PATH)["objects"]}
    names = [f"a{digit}{segment}" for digit in [first_digit, first_digit + 1] for segment in range(7)]
    # One physical two-digit region, assembled from fourteen segment components.
    # Unlike lamps, the segments are parts of one display region, not emitters
    # being counted or averaged into a socket.
    return {"status": "observed", "placements": [{"id": identifier + ".segment-region", "space": "playfield", "role": "display", "x": round(sum(objects[n]["x"] for n in names) / len(names), 6), "y": round(sum(objects[n]["y"] for n in names) / len(names), 6), "provenance": provenance(CORE, MANUAL, TABLE, SCRIPT, status="observed")}]}


def bulb_placement(identifier: str, address: int) -> dict:
    """Use the modelled bulb body, independently of its forward glow helper."""
    bulb = next(b for b in load_json(BULBS_PATH)["bulbs"] if b["address"] == address)
    state = "candidate" if address == 100 else "observed"
    return {"status": state, "placements": [{
        "id": identifier + "." + bulb["primitive"].lower(),
        "space": "playfield", "role": "emitter", "x": bulb["x"], "y": bulb["y"],
        "provenance": provenance(TABLE, MESH, SCRIPT, SCHEMATIC, PHOTOS, status=state),
    }]}


def device(identifier: str, label: str, kind: str, group: str, address: int, refs: tuple[str, ...], *, availability: str = "used", status: str = "validated", **extra) -> dict:
    ns = {"switch": "switch", "dip": "dip", "solenoid": "solenoid", "lamp": "lamp"}[group]
    aliases = [{"namespace": f"pinmame.{ns}", "value": str(address)}]
    if group in {"switch", "solenoid", "lamp"} and address >= 0:
        aliases.extend({"namespace": f"vpe-legacy.{ns}", "value": a} for a in dict.fromkeys([str(address), f"{address:02}", f"{address:03}"]))
    return {"id": identifier, "label": label, "kind": kind, "binding": {"group": f"pinmame.{'input' if group in {'switch', 'dip'} else 'output'}.{group}", "device": address},
            "aliases": aliases, "availability": availability, "provenance": provenance(*refs, status=status), **extra}


def build_inputs() -> list[dict]:
    result = []
    for address, label in [(-7, "Self Test"), (-6, "CPU Diagnostic"), (-5, "Sound Diagnostic")]:
        result.append(device(f"switch.diagnostic-{abs(address)}", label, "switch", "switch", address, (CORE, SCHEMATIC),
                             normally_closed=False, physical={"location": "coin door" if address == -7 else "backbox", "notes": "Direct diagnostic namespace; not a numbered matrix position."}, spatial=na("cabinet_or_service", CORE, SCHEMATIC)))
    for address in range(1, 49):
        identifier = f"switch.matrix-{address}"
        row, col = (address - 1) % 8, (address - 1) // 8
        wire, pin = ROW_WIRES[row]
        notes = "The own-game matrix draws a normally open contact; public sequential address = 8 * strobe + return + 1."
        if address in {5, 7}:
            result.append(device(identifier, f"Not Used Matrix Position {address}", "virtual", "switch", address, (MANUAL, SCHEMATIC), availability="unused", physical={"notes": "Blank identification row and starred NOT USED matrix position; no load inferred from the generic Bally keyboard port."}, spatial=na("unused", MANUAL, SCHEMATIC)))
            continue
        extra = {"normally_closed": False, "wiring": {"board": "MPU A4", "drive_wire": COLUMN_WIRES[col][0], "drive_connection": COLUMN_WIRES[col][1], "return_wire": wire, "return_connection": f"A4J2-{pin}"}}
        if address in CABINET_SWITCHES:
            extra["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC)
        else:
            extra["spatial"] = placements(identifier, "sensor", SWITCH_OBJECTS[address])
            notes += " Coordinates are observed projections onto the named table sensor or mechanism, with quantity and exact contact centers unpromoted."
        if address in {37, 38, 40}:
            notes += " The retained script assigns this number to another bumper. Figure V and the ROM's isolated gameplay response settle the physical pairing; that table handler is a defect."
        if address == 8:
            extra.pop("spatial")
            notes += " BallRelease is an off-center serve anchor and Drain a routing catcher. The coarse Figure V fit places the mouth above the table's Shield post, contradicting their physical order; that failed reconciliation is retained in the spatial report, not emitted as a contact coordinate."
        if address == 12:
            notes += " Identification table says KICKER; matrix and the own-game parts catalog identify a standup target, with no separate coil."
        if address == 41:
            notes += " CLOSED WHEN MOVABLE FLIPPERS ARE OPEN is the schematic's explicit position annotation. The printed name is MOVABLE FLIPPER END OF STROKE; the script uses it as open-position feedback, setting1 on open and0 on close. The retained evidence does not identify which assembly leaf stack supplies it, so no extra physical contact is invented. Its coordinate is a coarse projection onto the central zipper linkage at sw33, not the spinner's contact."
        if address in {18, 25, 31, 32}:
            notes += " Multiple physical contacts share this address. Every retained table location is recorded separately; no contact is made from a name alone."
        extra["physical"] = {"notes": notes}
        item = device(identifier, SWITCH_LABELS[address], "switch", "switch", address, (MANUAL, SCHEMATIC, PARTS, CORE, SCRIPT, RUNTIME), **extra)
        item["aliases"].append({"namespace": "manual.self-test", "value": f"{address:02}"})
        result.append(item)
    for address in range(81, 89):
        used = address in {82, 84}
        label = ("Right" if address == 82 else "Left") + " Flipper Button" if used else f"Unused Synthetic Flipper Column Position {address}"
        result.append(device(f"switch.flipper-column-{address}", label, "switch" if used else "virtual", "switch", address, (CORE, LIBRARY, SCHEMATIC), availability="used" if used else "unused",
                             **({"normally_closed": False} if used else {}), spatial=na("cabinet_or_service" if used else "unused", CORE, SCHEMATIC),
                             physical={"notes": "FLIP_SW(FLIP_L) has no FLIP_SWNO matrix copy. The ROM scans six matrix columns, never this column. Bally.vbs writes82/84 and core_updateSw synthesizes the enabled right45/46 and left47/48 pairs. Other bits produce no fitted additional control."}))
    for address in range(1, 33):
        result.append(device(f"dip.s{address}", DIP_LABELS[address], "dip_switch", "dip", address, (MANUAL, CORE), spatial=na("dip_switch", MANUAL), physical={"location": "MPU A4, backbox", "notes": f"Physical option switch S{address}; one of four eight-position banks S1-8, S9-16, S17-24, S25-32. Exact setting tables and adjustments are in the retained manual, PDF8-10."}))
    return result


def build_outputs() -> list[dict]:
    result = []
    for address, (label, q, pin, anchors) in SOLENOIDS.items():
        identifier = SOLENOID_IDS[address]
        notes = "Own-game A3 decoder output index +1 equals this public address; the ROM's self-test display independently pairs the printed number. The effect location is projected onto its mechanism, not a measured winding center."
        if address in PAIRED:
            notes += " Lamp34=0 selects the first named load; Lamp34=1 selects the second. Callback numbers25-30/32 are table-local dispatch labels and are not public outputs. Wiring and part numbers for each alternative are retained in the excerpts."
        if address == 1:
            notes += " Knocker is in the cabinet; only the zipper effect is placed."
        spatial = placements(identifier, "effect", anchors)
        if address == 8:
            spatial["placements"].pop(0)
            notes += " Only the saucer effect is placed. BallRelease is a serve anchor; the attempted manual outhole fit fails physical-order reconciliation and is not accepted."
        if address in {3, 4, 5, 6}:
            notes += " The retained script reverses its seven-target SolHit indices against the factory identification and A3 wiring. Physical effect anchors follow the own-game drawing and ROM self-test mapping; the callback reversal is a table defect."
        item = device(identifier, label, "coil", "solenoid", address, (MANUAL, SCHEMATIC, PARTS, CORE, SCRIPT, RUNTIME),
                      physical={"notes": notes}, wiring={"board": "Solenoid Driver A3 AS-2518-22", "driver_transistor": q, "control_connection": pin}, spatial=spatial)
        tests = [address]
        if address in PAIRED:
            tests.append(dict(zip([1, 2, 3, 4, 5, 6, 8], range(16, 23)))[address])
        item["aliases"].extend({"namespace": "manual.solenoid-self-test", "value": f"{n:02}"} for n in tests)
        result.append(item)
    for address, label, kind, availability, note in [
        (17, "Playfield Display Data Strobe PB4", "control_signal", "used", "The own-game W-1255-1 panel feature display connector6A1J1-15 reaches A4J4-5 on wire36. INITGAME2's final0x10 argument is hw.display, not gameSpecific1: by35.c pia1b_w latches bcd[5] and calls by35_dispStrobe(0x20) on a PB4 rising edge. The same PB4 bit is published, inverted, at continuous17. A3 Q17's N/U load pin does not make this meaningful display strobe unused. LISY's Medusa case independently declares J4-5 a strobe."),
        (18, "Coin Lockout Door", "coil", "used", "A3 Q19/J2-8, PB5, physical FO-36-7000 coin lockout. Printed Self Test23."),
        (19, "K1 Flipper Enable Relay", "relay", "used", "A3 Q15/K1 PB6. Printed Self Test24. The relay enables four cabinet-wired flipper coils. The retained table also uses it to toggle GI helpers; that is not the physical GI wiring."),
        (20, "Sixth Switch Column Strobe ST5", "control_signal", "used", "A4J4-8 supplies ST5 on the own-game matrix. by35.c reads PB7 for column6; its public continuous mirror20 is a strobe, not an extra coil. A3 Q18's load pins are N/U."),
    ]:
        item = device(f"solenoid.continuous-{address}", label, kind, "solenoid", address, (CORE, SCHEMATIC, RUNTIME), availability=availability, status="candidate" if availability == "unknown" else "validated", physical={"notes": note}, spatial=na("cabinet_or_service" if address in {18, 19} else "internal_nonvisual", CORE, SCHEMATIC))
        if address in {18, 19}:
            item["aliases"].append({"namespace": "manual.solenoid-self-test", "value": str(address + 5)})
        result.append(item)
    for address in [45, 46, 47, 48]:
        side = "Right" if address < 47 else "Left"
        virtual = address in {45, 47}
        identifier = f"flipper.{side.lower()}-{address}"
        extra = {"physical": {"notes": "Synthetic enabled button state; both members of the pair rise together, with no physical winding/EOS timing measurement. One cabinet button operates the upper and lower flipper on that side. Duplicate state does not create another coil."}}
        extra["spatial"] = na("virtual", CORE) if virtual else placements(identifier, "effect", [f"{side}Flipper", f"{side}Flipper2"])
        result.append(device(identifier, f"{side} Flipper {'State Mirror' if virtual else 'Pair'}", "virtual" if virtual else "coil", "solenoid", address, (CORE, LIBRARY, SCHEMATIC, PARTS), **extra))
    for line in MAIN_LAMPS.splitlines():
        address, q, pin, label = line.split("|")
        address = int(address)
        identifier = f"lamp.main-{address}"
        notes = f"A5 MC14514 decoder U{(address - 1) // 16 + 1}, S{(address - 1) % 16}, {q}. All connector branches, including N/U branches, are preserved in the excerpt. No bulb count is inferred from an electrical circuit symbol or VPX helper."
        extra = {"wiring": {"board": "Lamp Driver A5 AS-2518-23", "driver_transistor": q, "control_connection": f"A5{pin}"}}
        kind, availability = "lamp", "used"
        if address == 34:
            kind = "relay"
            extra["roles"] = ["internal.solenoid-expander-gate"]
            extra["spatial"] = na("internal_nonvisual", SCHEMATIC)
            notes += " Reaches A15 J1-2 SCR ANODE LAMP DRIVER and the solenoid-expander indicator light. Treat as an internal relay assembly, not a playfield insert."
        elif address == 50:
            availability = "unused"
            extra["spatial"] = na("unused", SCHEMATIC)
            notes += " The sole output branch is explicitly N/U. ROM lamp-test matrix activity does not fit a bulb."
        elif address in {11, 13, 27, 29, 45, 61}:
            extra["spatial"] = na("cabinet_or_service", SCHEMATIC)
        elif address == 59:
            # Board label alone does not settle where its fitted indicator is.
            notes += " The table's l59 is on its apron. That proxy is not accepted as a physical credit-indicator socket location. No spatial assertion."
        else:
            anchors = [f"l{address}"]
            if address in {4, 21, 37, 53}:
                anchors.append(f"l{address}_1")
            if address == 47:
                anchors = ["l47", "l47b", "l47d"]
                notes += " Table drives three top-target visual sites, each doubled in its fade list. The schematic labels only TOP MIDDLE BACK TARGET; fitted bulb count and which targets share this circuit are not settled, so these remain candidates."
            extra["spatial"] = placements(identifier, "emitter", anchors)
            if address == 47:
                extra["spatial"]["status"] = "candidate"
                for placement in extra["spatial"]["placements"]:
                    placement["provenance"]["status"] = "candidate"
            notes += " Locations are observed insert/target projections. All retained lights have show_bulb_mesh=false; these are not validated physical socket centers."
            # Insert and target glows are retained as extraction candidates only.
            # A known visual location does not establish a physical emitter.
            extra.pop("spatial")
            notes += " Those render candidates remain in evidence/spatial, not canonical emitter placements."
            if address == 60:
                extra["spatial"] = bulb_placement(identifier, address)
                notes += " The rear Olympus bar has an independently modelled bulb body for this channel; its world-space bounds supply the observed placement."
        extra["physical"] = {"notes": notes}
        result.append(device(identifier, label, kind, "lamp", address, (SCHEMATIC, CORE, SCRIPT), availability=availability, **extra))
    for data_line in range(4):
        for selector in range(15):
            address = 65 + 16 * data_line + selector
            identifier = f"lamp.aux-{address}"
            if selector >= 7:
                unloaded = selector == 7
                note = "A9 has only AD0-AD2 latched and seven SCRs per data line. "
                note += "S7 is explicitly N/U. This is an unloaded decoder position; the ROM can nevertheless write the matrix bit during diagnostics." if unloaded else "This exported emulator slot has no independent physical SCR. The real three-bit board aliases high selector values, whereas PinMAME exports a separate bit. Meaningful normal-operation state is not established; do not add a bulb or call it dead from trace absence."
                result.append(device(identifier, f"{'Unloaded A9 S7' if unloaded else 'Unresolved A9 High Selector'} Channel {address}", "virtual", "lamp", address, (SCHEMATIC, CORE, RUNTIME), availability="unused" if unloaded else "unknown", status="validated" if unloaded else "candidate", physical={"notes": note}, spatial=na("no_physical_device", SCHEMATIC, CORE)))
                continue
            pin, wire = AUX_PINS[data_line * 7 + selector]
            if selector < 5:
                n = selector * 4 + data_line + 1
                label = f"Olympus Top Panel #{n}"
                notes = "Own-game auxiliary decoder/SCR/connector trace; table provides a runtime coordinate, not an independently measured socket."
                status = "validated"
                if address == 84:
                    notes += " A9 board sheet prints #4, but the game's playfield harness sheet explicitly prints #14 on this connector. Keep the board typo in the excerpt."
                if address == 100:
                    label = "Olympus Bar, Runtime Position 15 (Printed #3 Duplicate)"
                    notes += " Both physical sheets duplicate #3 at A9J3-11; script position15 remains a candidate physical identity until a harness/socket trace settles it."
                    status = "candidate"
                anchors = [f"l{address}"]
            elif selector == 5 or address == 71:
                n = {70: 1, 86: 2, 102: 3, 118: 4, 71: 5}[address]
                label = f"#{n} Shooter Lane Rollover Button and Gorgon Bonus"
                notes = "The playfield harness draws two lamp symbols for this shared circuit, matching separate shooter-lane and Gorgon inserts. Their table coordinates remain observed projections, not bulb centers."
                anchors, status = [f"l{address}", f"l{address}_1"], "validated"
            else:
                label = {87: "Ready Shooter Lane", 103: "Aim Shooter Lane", 119: "Fire Shooter Lane"}[address]
                notes, anchors, status = "Own-game A9 circuit; observed insert projection, no guessed socket quantity.", [f"l{address}"], "validated"
            extra = {}
            if selector < 5:
                extra["spatial"] = bulb_placement(identifier, address)
                notes += " The observed coordinate is the world-space center of its modelled rear-bar bulb body, not the Light glow."
            else:
                notes += " Insert glows remain extraction candidates only; no canonical emitter placement is asserted."
            result.append(device(identifier, label, "lamp", "lamp", address, (SCHEMATIC, CORE, SCRIPT), status=status,
                                 physical={"notes": notes}, wiring={"board": "Auxiliary Lamp Driver A9 AS-2518-52", "driver_transistor": f"Q{data_line * 7 + selector + 1}", "control_connection": f"A9{pin}", "drive_wire": wire}, **extra))
    return result


def build_displays() -> list[dict]:
    result = []
    for i, start in enumerate([1, 9, 17, 25, 35, 38, 42, 44, 46]):
        label = f"Player {i + 1} Score" if i < 4 else ["Credits", "Ball in Play / Match", "Extended Play Time Units", "Like Numbers", "Shield of the Gods Bonus"][i - 4]
        identifier = f"display.{i}"
        item = {"id": identifier, "label": label, "kind": "segment", "controller_index": i, "segment_start": start, "width": 7 if i < 4 else 2, "height": 1,
                "physical_location": "cabinet_or_service" if i < 6 else "playfield", "provenance": provenance(CORE, MANUAL, SCHEMATIC, PARTS)}
        item["spatial"] = na("cabinet_or_service", CORE, MANUAL) if i < 6 else display_projection(identifier, 2 * (i - 6))
        result.append(item)
    return result


def build_mechanisms() -> list[dict]:
    specs = [
        ("outhole", "Outhole and Manual Shooter", "kicker", [SOLENOID_IDS[8]], ["switch.matrix-8"], "One-ball outhole returns a drained ball to the manual shooter. Public8 with lamp34=0 ejects it; the same public address with lamp34=1 ejects the saucer. The ball stack is table routing, not a measured extra trough assembly. Drain collection does not directly actuate the outhole contact.", None),
        ("saucer", "Neptune's Cove Saucer", "kicker", [SOLENOID_IDS[8]], ["switch.matrix-19"], "Upper-left saucer retains the ball on switch19 until public8 with lamp34=1 kicks it to play. The script uses InitSaucer sw19,19,155,8; angle155 and speed8 are table tuning, not factory geometry or physical timing.", "ASE-482-53"),
        ("right-targets", "Right Four Drop Target Bank", "drop_target_bank", [SOLENOID_IDS[2]], [f"switch.matrix-{n}" for n in range(1, 5)], "Four mechanically latching targets A(top) through D(bottom), switches4 through1. Public2 with lamp34=0 raises the bank. Targets remain down until reset; their make contacts follow target state. Completing all four collects Colossus, adds extended-play units and stops the right like-number digit.", "ASE-2795-73"),
        ("memory-targets", "Seven Olympus Memory Drop Targets", "drop_target_bank", [SOLENOID_IDS[n] for n in [3, 4, 5, 6]], [f"switch.matrix-{n}" for n in range(42, 49)], "Seven targets ordered left-to-right48..42. Public3 lamp34=0 resets the bank; individual knockdowns are target1=public3 gated,2=public4 ungated,3=public4 gated,4=public5 ungated,5=public5 gated,6=public6 ungated,7=public6 gated. Preserve target memory and ROM-directed knockdown; a plain reset-only bank loses the feature. Held contacts must be released when the physical reset succeeds, otherwise the ROM retries. The generic parts drawing illustrates a four-target memory unit; it does not prove the coil count of this seven-target variant.", "ASE-3038-4"),
        ("zipper", "Time Locked Zipper Flippers", "other", [SOLENOID_IDS[1], SOLENOID_IDS[2], "flipper.left-48", "flipper.right-46"], ["switch.matrix-41"], "The two upper flippers rotate normally and translate inward/outward as one latched linkage. Public1 with lamp34=1 opens the linkage; public2 gated closes it. Switch41 closes at the open position. The retained script substitutes alternate flipper objects and writes41 itself; that is a routing model, not two extra fitted flippers. Top target hits close the zipper. It reopens on timer expiry or when the ball leaves the upper area. DIP8 chooses accumulated10-second extensions versus a reset10-second interval. The parts drawing separately identifies the NB-24-1500 reset coil, GT-30-1300 latch coil, springs/linkage and both flipper assemblies; do not confuse winding EOS switches with matrix41.", "ASE-2397-4"),
        ("shield", "Shield of the Gods Post", "other", [SOLENOID_IDS[7]], ["switch.matrix-17"], "Cabinet action button17 requests the ROM-controlled post pulse7. A rubbered post between the lower flippers returns a ball toward play. It starts with five credits, lane shots add credits, unused credits score10000 each at bonus. The table models its impulse with a plunger and two alternate walls; those are one mechanism, not three physical posts. Post returns when drive releases; do not hold the table impulse from a button directly.", "ASE-2593-7"),
        ("flippers", "Four Cabinet-Wired Flippers", "other", ["flipper.left-48", "flipper.right-46", "solenoid.continuous-19"], ["switch.flipper-column-82", "switch.flipper-column-84"], "K1 enables four physical dual-winding flipper coils, two per cabinet button. Upper flippers are part of the zipper. Public45/46 and47/48 are synthetic pairs, not independent power/hold observations. Physical winding EOS contacts and lower-flipper illumination contacts are documented in the wiring and zipper assembly, separate from matrix41.", None),
        ("reflexes", "Four Bumpers and Three Slingshots", "other", [SOLENOID_IDS[n] for n in range(9, 16)], [f"switch.matrix-{n}" for n in range(34, 41)], "ROM causality confirmed separately:37->12,38->11,39->10,40->9,34->15,35->14,36->13. Each switch is stimulated separately in the retained gameplay trace. Physical locations follow Figure V; the table's first, second and fourth bumper handlers are rotated against those labels.", None),
        ("expander", "AS-2518-66 Solenoid Expander", "other", ["lamp.main-34"], [], "Lamp34 drives the expander optocoupler/relay and its internal indicator. Relay contacts select alternative loads for public1..6 and8. Use the lamp state at the output transition, as the retained script does. There is no public solenoid25..32 bank. The board is not a playfield lamp circuit merely because its gate uses the lamp callback.", "AS-2518-66"),
        ("gi", "General Illumination and Flipper Lamps", "other", [], [], "Own-game playfield schematic supplies general illumination from5.9VAC A2J1-4 (10) and -1 (70), with returns A2J1-6 (40) and -3 (50). Upper-flipper NC contacts switch the translucent lower-flipper lighting. PinMAME exposes no independent GI group for this driver. The script's29 GI objects and8 flipperlight helpers are a visual approximation; they do not establish sockets, quantities or string membership. A physical socket/harness survey remains required.", None),
    ]
    result = []
    for name, label, kind, acts, sensors, behavior, part in specs:
        if name in {"outhole", "saucer", "right-targets", "memory-targets", "zipper"}:
            acts = []
            behavior += " Shared public-driver ownership is recorded once under mechanism.expander; the exact selected loads are stated here and in its relay relationships."
        if name == "expander":
            acts = ["lamp.main-34"] + [SOLENOID_IDS[n] for n in sorted(PAIRED)]
        item = {"id": f"mechanism.{name}", "label": label, "kind": kind, "actuators": acts, "sensors": sensors, "behavior": behavior, "provenance": provenance(MANUAL, SCHEMATIC, PARTS, SCRIPT, CORE, RUNTIME)}
        if name in {"zipper", "gi"}:
            item["provenance"]["source_refs"].append(PHOTOS)
        if part:
            item["assembly_part_number"] = part
        result.append(item)
    return result


def excerpt(name: str, locator: str, *, reviewed: bool = True) -> dict:
    path = EXCERPTS / name
    if not path.is_file():
        raise ValueError(f"Missing required Medusa excerpt: {path}")
    item = {"id": "excerpt.medusa." + path.stem, "path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "locator": locator, "method": "mixed", "transcribed_by": "GPT Sol; bounded extraction by GPT Terra and GPT Luna, independently inspected as stated in each excerpt", "reviewed": reviewed}
    if name == "manual-geometry.md":
        item.update({"image": (EXCERPTS / "manual-figure-v.webp").relative_to(ROOT).as_posix(), "image_sha256": "ddafa8955456e383b65c3e4ec73161db51d39b6fabf967d9d32620a3fc1e3387", "image_derivation": "Bally_1981_Medusa_Manual.pdf page 18, crop box 0.025,0.06,0.6,0.9, scanned page rendered at its native resolution (embedded image xref 119, 2388px across 33.17in), rendered at 72 dpi, grayscale, 1374x2654 WebP quality 70"})
    return item


def build_sources() -> list[dict]:
    common = {"license": "Copyright Bally Manufacturing Corporation; factual excerpts only, original retained locally", "attribution": "Bally Manufacturing Corporation,1981; scans hosted by IPDB and PinWiki"}
    sources = [
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": REVISION, "sha256": "1c00fca170c7549a399a89fb0f76d4318fce08a6620becd4558fe8cb803bf00d", "locator": "src/wpc/by35games.c:23-40,1292-1332 medusaDisp, INITGAME2 and medusaa init alias; by35.c pia0b_r,pia1b_w,by35_lampStrobe; core.c core_updateSw; core.h flipper bits; lisy/lisy35.c case4 Medusa", "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [excerpt("pinmame.md", "Pinned source paths and hashes, exact macro argument roles")]},
        {"id": MANUAL, "kind": "manual", "uri": "https://www.ipdb.org/files/1565/Bally_1981_Medusa_Manual.pdf", "source_id": "1565", "revision": "Bally game1245 FO713,1981", "sha256": MANUAL_HASH, "original_filename": "Bally_1981_Medusa_Manual.pdf", "acquired_at": "2026-10-29T11:31:06.809390Z", "locator": "IPDB machine https://www.ipdb.org/machine.cgi?id=1565; PDF6-10 rules/options,16 service,17 identification,18 FigureV,19 parts; Windows.Media.Ocr plus native visual check", "excerpts": [excerpt("manual-io.md", "PDF17-18"), excerpt("rules-parts.md", "PDF6-10,16,19 and parts-catalog Medusa section")], **common},
        {"id": SCHEMATIC, "kind": "manual", "uri": "https://www.ipdb.org/files/1565/Bally_1981_Medusa_Schematics_paginated.pdf", "source_id": "1565", "revision": "Bally game1245 schematics", "sha256": SCHEMATIC_HASH, "original_filename": "Bally_1981_Medusa_Schematics_paginated.pdf", "acquired_at": "2026-10-29T11:31:08.137354Z", "locator": "IPDB machine1565; PDF1 cabinet,2-3 playfield W-1187-31/W-1255-1,4 backbox,5 A5,6 A3,7 A9,11 expander; Windows.Media.Ocr and native images", "excerpts": [excerpt("manual-io.md", "PDF2 matrix"), excerpt("schematic-a5-a3.md", "PDF5-6 full output/connector regions", reviewed=False), excerpt("schematic-a9.md", "PDF3,7 complete auxiliary rows"), excerpt("rules-parts.md", "PDF2,11 GI/expander")], **common},
        {"id": PARTS, "kind": "manual", "uri": "https://www.pinwiki.com/wiki/images/d/d6/Bally-Parts-Catalog-1981.pdf", "revision": "Bally1981 parts catalog", "sha256": PARTS_HASH, "original_filename": "Bally-Parts-Catalog-1981.pdf", "locator": "PDF25-26 printed46-49 Medusa; PDF42-43 printed80-82 memory and zipper assemblies; PDF39 shield post; native embedded scans rotated270degrees for Windows.Media.Ocr and visual inspection", "excerpts": [excerpt("rules-parts.md", "Rules and construction roles"), excerpt("catalog-parts.md", "Complete switch, coil, bottom-assembly and zipper parts tables")], **common},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/medusa-1981/extracted-vpxtool/script.vbs", "revision": "JPSalas Medusa1.0.4", "sha256": SCRIPT_HASH, "known_working": True, "license": "NOASSERTION; retained user-owned community table, not redistributed", "attribution": "JPSalas2017; credits Joe Entropy, RipleYYY and Pacdude for light numbering", "locator": "User-selected known-working Tables Archive source; extracted by vpxtool git:v0.33.3; init79-124,handlers133-277,expander283-312,zipper314-334,lamps487-608,display944-969", "excerpts": [excerpt("runtime-vpx.md", "Complete active switch/lamp binding and callback regions, derived facts")]},
        {"id": TABLE, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/medusa-1981/Medusa (Bally 1981).vpx", "revision": "JPSalas1.0.4; vpxtool git:v0.33.3", "sha256": TABLE_HASH, "locator": "bounds0,0,952,1974; full extraction836files10173989bytes; manifest9754b28148f1c2661fbcd795e97b5e45bb514eadfd6715febd0ecc7c8c26021c; evidence/spatial/bally.medusa.1981.json contains extractor candidates, not validated sockets", "license": "NOASSERTION; community table retained outside Git", "attribution": "JPSalas and credited contributors", "excerpts": [excerpt("runtime-vpx.md", "Named object coordinate roles and exclusions")]},
        {"id": LIBRARY, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/medusa-1981/Bally.vbs", "revision": "Bally.vbs3.61", "sha256": "d3ff448412b07a97722f7c34ad36e4364955d09595c381133eb24eabfaf7c18c", "known_working": True, "locator": "Local table's LoadVPM Bally.vbs dependency; cabinet key writes82/84, diagnostics-7..-5, synthetic callbacks from core.vbs; other retained library hashes in excerpt", "license": "NOASSERTION; local VPinMAME script library", "attribution": "VPinMAME script authors", "excerpts": [excerpt("runtime-vpx.md", "Bally.vbs/core.vbs key and callback constants")]},
        {"id": RUNTIME, "kind": "runtime_scenario", "uri": "external:pinmame-review-artifacts/bally.medusa.1981/harness", "revision": REVISION, "locator": "Fresh isolated-state runs explore-solenoid-run.json33ac9471b831c8e938139652d467d2c4d3b43fab2ddc2b3a83f9d88e1f0097f9 and explore-gameplay-run.jsonc8b776f3720ff1e6e4f4ab08b5f35f869b707cf9caa45258cdd02b3829da1f1c; pinned DLL8044e4dfbcd66dd2d686075f2b942d8c60c4a04899c603d2d67a9b2ff6103cd5; ROM hash/member provenance and limitations in excerpt", "license": "Derived factual observations; no ROM/NVRAM redistributed", "attribution": "Local LibPinMAME harness; legal user-supplied medusa.zip", "excerpts": [excerpt("runtime-vpx.md", "Service numbers, relay-gate state, isolated responses and trace hashes")]},
    ]
    by_id = {source["id"]: source for source in sources}
    by_id[MANUAL]["excerpts"].append(excerpt("manual-geometry.md", "PDF18 Figure V, coarse recorded measurement and affine controls"))
    by_id[SCHEMATIC]["excerpts"][1]["reviewed"] = True
    by_id[PARTS]["acquired_at"] = "2026-10-29T11:44:44.245434Z"
    for identifier in [SCRIPT, TABLE]:
        by_id[identifier]["acquired_at"] = "2026-10-29T11:29:07.000405Z"
    sources.append({
        "id": PHOTOS, "kind": "human_review",
        "uri": "external:pinmame-review-artifacts/bally.medusa.1981/photos",
        "revision": "IPDB1565 and Pinside Medusa gallery inspection, 2026-10-29",
        "sha256": "d4ac7a2c9a1fa9406bd2bc8b2633a287f14ec6fc2ef6b5b53047569955843ddd",
        "acquired_at": "2026-10-29T11:34:24Z",
        "locator": "Manifest of nine IPDB originals, 42 Pinside thumbnails, four full Pinside views and two derived contact sheets; direct photo pages, resource paths, hashes and limitations in excerpt",
        "license": "Photographer copyrights; originals and contact sheets retained outside Git",
        "attribution": "IPDB: Frank Ersfeld, Philippe Thibault, Mark Steinman, Mike Mahaffey; Pinside member gallery contributors",
        "excerpts": [excerpt("photos.md", "Verified machine1565; physical zipper/display/flipper observations and socket-survey limits")],
    })
    sources.extend([
        {
            "id": MESH, "kind": "vpx_table",
            "uri": "external:pinmame-review-artifacts/bally.medusa.1981/world-obj/Medusa (Bally 1981).obj",
            "revision": "vpxtool git:v0.33.3 export obj --units vpu",
            "sha256": "aa38d3de5c283f8dbc02800c07c5817c201ca982aeaf1d58955eda5dfb36981e",
            "acquired_at": "2026-10-29T12:23:30Z",
            "locator": "Exact retained VPX world export, 11210362 bytes; 21 Bulb-Wedge-Small bodies and four independently positioned bumper-cap controls; all bounds in committed bulb seed",
            "license": "NOASSERTION; derived community-table mesh retained outside Git",
            "attribution": "JPSalas and credited table/model contributors; vpxtool exporter",
            "excerpts": [excerpt("mesh-bulbs.md", "Complete rear-bar bulb inventory, coordinate derivation and controls")],
        },
        {
            "id": "manual-lamps.medusa", "kind": "manual",
            "uri": "https://www.ipdb.org/files/1565/Bally_1981_Medusa_Lamps_Schematic.pdf",
            "source_id": "1565", "revision": "W-1182-35 Medusa A5 lamp driver",
            "sha256": "68f4c9fea27200b80457a4eee164026d725bbf9f719df258c29728064805dd1b",
            "original_filename": "Bally_1981_Medusa_Lamps_Schematic.pdf",
            "acquired_at": "2026-10-29T11:31:07.276801Z",
            "locator": "Single-sheet copy of the A5 lamp drawing, same factual rows as paginated schematic PDF5; rendered/OCR retained; duplicate scan, not independent authority",
            "excerpts": [excerpt("schematic-a5-a3.md", "A5 portion, all four decoder channels and connector branches")],
            **common,
        },
    ])
    return sources


def build_definition() -> dict:
    outputs = build_outputs()
    relationships = [{"id": f"relationship.expander-{n}", "kind": "relay_gated", "source": "lamp.main-34", "destination": SOLENOID_IDS[n], "provenance": provenance(SCHEMATIC, SCRIPT, RUNTIME)} for n in sorted(PAIRED)]
    for n in [46, 48]:
        relationships.append({"id": f"relationship.enable-{n}", "kind": "relay_gated", "source": "solenoid.continuous-19", "destination": f"flipper.{'right' if n == 46 else 'left'}-{n}", "provenance": provenance(CORE, SCHEMATIC)})
    return {"format": "pinmame-machine-definition", "schema_version": 2,
            "machine": {"id": MACHINE_ID, "name": "Medusa", "manufacturer": "Bally", "year": 1981, "kind": "physical_pinball", "model_number": "1245", "ipdb_id": 1565, "opdb_id": "G4xXQ-MDWW1", "playfield": {"width": 952, "height": 1974, "units": "vpx", "provenance": provenance(TABLE)}},
            "controller": {"platform": "pinmame.by35", "hardware_generation": "0x0000000400000", "inversion_applied_by_emulator": True},
            "coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate", "physical_wiring": "candidate", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "observed"}},
            "drivers": [{"id": "medusa", "description": "Medusa", "manufacturer": "Bally", "year": "1981", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Production Bally game1245."}, {"id": "medusaa", "clone_of": "medusa", "description": "Medusa (Free Play)", "manufacturer": "Bally / Oliver", "year": "2004", "flags": 0, "physical_compatibility": "identical", "variant_notes": "Oliver free-play firmware uses init_medusa, identical controller, display and sound ROMs; its2004 firmware date is not a physical edition. Debug-only medusaf is absent from the pinned public catalog and is not added."}],
            "inputs": build_inputs(), "outputs": sorted(outputs, key=lambda o: (o["binding"]["group"], o["binding"]["device"])), "displays": build_displays(), "mechanisms": build_mechanisms(), "relationships": relationships,
            "sources": build_sources(), "conflicts": [], "knowledge": {"path": NOTE_PATH.relative_to(ROOT).as_posix(), "status": "complete"}}


def build_report(definition: dict) -> dict:
    all_devices = definition["inputs"] + definition["outputs"] + definition["displays"]
    return {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
            "decision": "partial; no physical-socket validation or author-ready claim", "coordinate_convention": "x0left,x1right,y0rear/backglass,y1front/apron, normalized playfield, at most6decimals",
            "table_sha256": TABLE_HASH, "script_sha256": SCRIPT_HASH, "extraction_manifest_sha256": MANIFEST_HASH, "extraction_file_count": 836, "extraction_total_bytes": 10173989,
            "transformation": {"bounds": [0, 0, 952, 1974], "x": "raw_x/952", "y": "raw_y/1974", "tool": "pinmame_game_defs.spatial.extract_spatial_candidates; six-place rounding; wall drag-point mean"},
            "located_devices": [x["id"] for x in all_devices if "placements" in x.get("spatial", {})],
            "without_spatial": [x["id"] for x in all_devices if "spatial" not in x],
            "unknown_outputs": [x["id"] for x in definition["outputs"] if x["availability"] == "unknown"],
            "projection_classes": ["coil/reflex effects onto mechanism anchors", "zipper limit and motion onto central linkage near sw33", "21 rear-bar bulb bodies from world-space mesh bounds; duplicate-label position remains candidate", "playfield two-digit display region projected onto its fourteen segment components"],
            "rejected_measurements": [{"device": "switch.matrix-8", "candidate": outhole_projection("switch.matrix-8", "sensor"), "reason": "Extrapolated Figure V fit puts the outhole above the table's Shield post; inconsistent physical order, coordinate withheld"}],
            "unpromoted_candidates": "All insert/target glow and GI/flipperlight coordinates remain in evidence/spatial; they do not establish physical emitters",
            "blockers": ["Twenty-eight auxiliary high-selector emulator slots have no independent SCR and no settled normal runtime semantics", "A9J3-11 duplicates physical #3 while script calls it bar position15", "Main lamp47 target bulb count/fitment and credit indicator59 physical location", "Insert lamps, GI and lower-flipper illumination sockets/string membership not surveyed", "Outhole fit fails physical-order reconciliation; observed mechanism/display projections need physical-center reconciliation"],
            "evidence": [s["uri"] for s in definition["sources"]]}


def report_markdown(report: dict) -> str:
    return "# Medusa spatial evidence and blockers\n\nCoverage: **partial**. No author-ready promotion.\n\n" + "\n".join(f"- {x}" for x in report["blockers"]) + "\n\nAll placements use x=0 left, x=1 right, y=0 rear/backglass, y=1 front/apron.\nThe exact 836-file extraction manifest, source hashes, formula, named projection classes,\nlocated devices, rejected outhole fit and unresolved outputs are recorded in `medusa-1981.json`.\nOnly the 21 modelled rear-bar bulb bodies supply lamp placements. Insert/target glows,\nGI helpers and flipperlight objects remain external extraction candidates, not sockets.\n"


def verify_retained_evidence() -> None:
    """An explicitly supplied root must be complete; no-root use stays portable."""
    checks = {
        "PINMAME_VPX_SOURCES_ROOT": {"bally/medusa-1981/Medusa (Bally 1981).vpx": TABLE_HASH, "bally/medusa-1981/extracted-vpxtool/script.vbs": SCRIPT_HASH, "bally/medusa-1981/extracted-vpxtool/manifest.json": MANIFEST_HASH},
        "PINMAME_MANUALS_ROOT": {"by-machine/bally.medusa.1981/Bally_1981_Medusa_Manual.pdf": MANUAL_HASH, "by-machine/bally.medusa.1981/Bally_1981_Medusa_Schematics_paginated.pdf": SCHEMATIC_HASH, "by-machine/bally.medusa.1981/Bally-Parts-Catalog-1981.pdf": PARTS_HASH},
        "PINMAME_REVIEW_ARTIFACTS_ROOT": {"bally.medusa.1981/harness/explore-solenoid-run.json": "33ac9471b831c8e938139652d467d2c4d3b43fab2ddc2b3a83f9d88e1f0097f9", "bally.medusa.1981/harness/explore-gameplay-run.json": "c8b776f3720ff1e6e4f4ab08b5f35f869b707cf9caa45258cdd02b3829da1f1c"},
    }
    for env, files in checks.items():
        if root := os.environ.get(env):
            for relative, expected in files.items():
                path = Path(root) / relative
                if not path.is_file() or digest(path) != expected:
                    raise ValueError(f"Missing or changed retained Medusa evidence: {path}")
    if root := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        from build_external_evidence_manifest import check_manifest
        check_manifest(Path(root) / "bally/medusa-1981/extracted-vpxtool", "medusa")
    if root := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        from build_external_evidence_manifest import check_manifest
        check_manifest(Path(root) / "bally.medusa.1981/photos", "medusa")
        obj = Path(root) / load_json(BULBS_PATH)["relative_path"]
        if not obj.is_file() or digest(obj) != load_json(BULBS_PATH)["source_sha256"]:
            raise ValueError(f"Missing or changed retained Medusa mesh: {obj}")


def validate_definition(definition: dict) -> None:
    """Reject incomplete electrical tables before any generated file is written."""
    from pinmame_game_defs.schema_validation import validate_against_schema
    from pinmame_game_defs.validation import validate_machine

    expected = {
        "pinmame.input.switch": {-7, -6, -5} | set(range(1, 49)) | set(range(81, 89)),
        "pinmame.input.dip": set(range(1, 33)),
        "pinmame.output.solenoid": set(range(1, 16)) | {17, 18, 19, 20, 45, 46, 47, 48},
        "pinmame.output.lamp": {n for n in range(1, 129) if n % 16},
    }
    devices = definition["inputs"] + definition["outputs"]
    for group, addresses in expected.items():
        actual = [d["binding"]["device"] for d in devices if d["binding"]["group"] == group]
        if len(actual) != len(addresses) or set(actual) != addresses:
            raise ValueError(f"Incomplete or duplicate Medusa address table: {group}")
    errors = validate_against_schema(definition, ROOT / "schemas/machine.schema.json", MACHINE_ID)
    errors += validate_against_schema(load_json(GEOMETRY_PATH), ROOT / "schemas/vpx-spatial-candidates.schema.json", "Medusa geometry")
    errors += validate_machine(definition, ROOT)
    if errors:
        raise ValueError("Invalid Medusa curator inputs: " + "; ".join(str(e) for e in errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    try:
        if (ROOT / "machines/author-ready/bally/medusa-1981.json").exists():
            raise ValueError("Refusing to overwrite an existing author-ready Medusa artifact")
        verify_retained_evidence()
        definition = build_definition()
        validate_definition(definition)
        report = build_report(definition)
        expected = {DEFINITION_PATH: canonical_bytes(definition), SEED_PATH: canonical_bytes(definition), NOTE_PATH: NOTE_SEED.read_bytes(), REPORT_PATH: canonical_bytes(report), REPORT_MD_PATH: report_markdown(report).encode("utf-8")}
        if args.check:
            for path, payload in expected.items():
                if not path.is_file() or path.read_bytes() != payload:
                    raise ValueError(f"Medusa curator drift: {path.relative_to(ROOT)}")
        else:
            for path, payload in expected.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(payload)
        print("Medusa artifacts match deterministic curator" if args.check else "Regenerated Medusa artifacts (partial)")
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
