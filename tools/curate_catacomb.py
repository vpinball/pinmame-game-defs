"""Deterministically curate Stern Catacomb from pinned, reviewed evidence.

Generation never reads a user's table, ROM, or manual. The optional verifier
checks those retained originals separately. Unknown loads and incomplete socket
evidence deliberately keep this record partial.
"""
from __future__ import annotations

import argparse
import copy
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catacomb_data as data
from pinmame_game_defs.jsonio import canonical_bytes, load_json

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "stern.catacomb.1981"
DEFINITION = Path("machines/partial/stern/catacomb-1981.json")
SEED = Path("tools/seeds/stern/catacomb-1981.json")
FACTS = Path("tools/seeds/stern/catacomb-1981-facts.json")
NOTE = Path("knowledge/stern/catacomb-1981.md")
NOTE_SEED = Path("tools/seeds/stern/catacomb-1981-knowledge.md")
REPORT = Path("reports/spatial/stern/catacomb-1981.json")
REPORT_MD = REPORT.with_suffix(".md")
RUNTIME = Path("evidence/runtime/stern/catacomb-1981.json")
MISSING = ["output_semantics", "mechanism_behavior", "spatial_placement"]
PHYSICAL_TO_PUBLIC = dict(enumerate((2, 1, 6, 7, 3, 4, 5, 8, 11, 12, 14, 13, 9, 10, 19, 15, 17, 20, 18), 1))
BANKS = {"a": (14, 15, 16), "b": (22, 23, 24), "c": (30, 31, 32), "d": (38, 39, 40)}
SWITCH_OBJECTS = {4: "sw4", 5: "sw5", 9: "Bumper1", 10: "Bumper2", 11: "UpperSlingshot",
                  12: "LeftSlingshot", 13: "RightSlingshot", 17: "Drain", 27: "sw27",
                  33: "BallRelease", 34: "Slot1", 35: "Slot2", 36: "sw36", 37: "sw37"}
SWITCH_OBJECTS.update({n: f"sw{n}" for n in (14,15,16,18,19,20,21,22,23,24,25,26,28,29,30,31,32,38,39,40)})
COIL_NAMES = {1: "Top thumper bumper", 2: "Bottom thumper bumper", 3: "Top slingshot",
              4: "Left slingshot", 5: "Right slingshot", 6: "Knocker", 7: "Left kickout hole",
              8: "Right kickout hole", 9: "Outhole reflex", 10: "Outhole turnstyle",
              11: "Drop bank A reset", 12: "Drop bank B reset", 13: "Drop bank C reset", 14: "Drop bank D reset",
              15: "Unused Q16 driver", 17: "Unused Q17 driver", 18: "Unused Q19 driver",
              19: "Main flipper enable relay", 20: "Backbox playfield enable"}
COIL_OBJECTS = {1: "Bumper1", 2: "Bumper2", 3: "UpperSlingshot", 4: "LeftSlingshot",
                5: "RightSlingshot", 7: "sw36", 8: "sw37", 9: "Drain", 10: "BallRelease"}


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(refs)}


def slug(text: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def point(raw: dict, name: str) -> tuple[float, float]:
    row = next(x for x in raw["objects"] if x["object"].casefold() == name.casefold())
    # Match the repository helper: wall drag-point centroid, otherwise center/position.
    if row["type"] == "Wall":
        pts = row["drag_points"]
        return tuple(sum(x[k] for x in pts) / len(pts) for k in ("x", "y"))
    p = row.get("center", row.get("position"))
    return p["x"], p["y"]


def mesh_point(raw: dict, name: str) -> tuple[float, float]:
    return data.mesh_center(next(x for x in raw["meshes"] if x["object"] == name))


def located(raw: dict, identifier: str, role: str, points: list[tuple[str, tuple[float, float]]]) -> dict:
    return {"status": "observed", "placements": [
        {"id": f"{identifier}.{role}.{slug(name)}", "role": role, "space": "playfield",
         "x": data.normalize(raw, *xy)[0], "y": data.normalize(raw, *xy)[1],
         "provenance": prov("table.catacomb", "extraction.catacomb", "script.catacomb", status="observed")}
        for name, xy in points]}


def aliases(group: str, number: int, legacy: bool = False) -> list[dict]:
    result = [{"namespace": f"pinmame.{group}", "value": str(number)}]
    if legacy:
        result += [{"namespace": "vpe-legacy.switch", "value": value}
                   for value in dict.fromkeys((str(number), f"{number:02}", f"{number:03}"))]
    return result


def inputs(raw: dict) -> list[dict]:
    result = []
    for number, label, used in ((-7, "Self test", True), (-6, "MPU S33 / CPU diagnostic NMI", True), (-5, "Unfitted sound diagnostic", False)):
        physical = number in (-7, -6)
        result.append({"id": f"switch.{slug(label)}", "label": label, "kind": "switch" if physical else "virtual",
                       "binding": {"group": "pinmame.input.switch", "device": number},
                       "aliases": aliases("switch", number), "availability": "used" if used else "unused",
                       "normally_closed": False, "pulse": True,
                       "physical": {"location": "Inside coin door" if number == -7 else "MPU board in backbox" if number == -6 else "Emulator diagnostics",
                                    "notes": "Normally-open coin-door self-test button." if number == -7 else "On-board S33 MEMORY CLEAR is a normally-open pushbutton to ground on U9 pin 6 (NMI). PinMAME public -6 asserts this NMI. The separate door memory-clear contact is physical direct input 3 at A4J3-5; no shared electrical path or firmware clearing outcome is inferred." if number == -6 else "ST300V has no diagnostic callback for -5."},
                       "provenance": prov("core.catacomb", "manual.catacomb", "schematic.catacomb"),
                       "spatial": na("cabinet_or_service" if physical else "virtual", "core.catacomb", "manual.catacomb", "schematic.catacomb")})
        if physical:
            result[-1]["physical"]["switch_type"] = "button"
        if number == -6:
            result[-1]["id"] = "switch.mpu-diagnostic-s33"
            result[-1]["wiring"] = {"board": "MPU-200 A4", "control_connection": "U9-6 (NMI)", "return_connection": "Ground"}
    for row in raw["manual"]["pdf_18_switch_identification"]:
        n = int(row["switch_no"])
        label = row["description"].replace('"', '').title()
        notes = "Printed switch numbers are public matrix addresses, independently observed in the ROM's switch test."
        physical = {"location": "Cabinet" if n in (1,2,3,6,7,8) else "Main playfield", "switch_type": "leaf"}
        if n in (1,2,3): physical["switch_type"] = "microswitch"
        if n in (6,8): physical["switch_type"] = "button"
        if n == 7: physical["switch_type"] = "tilt"
        if n == 8:
            notes += " Manual p12 identifies the left cabinet button stopping bank lights. The modern 2.0.1 script asserts and clears matrix input 8 from LeftFlipperKey, agreeing with the manual. Only the older archive table uses RightFlipperKey for matrix input 8; that older table defect does not change physical identity."
        if n in {x for bank in BANKS.values() for x in bank}:
            bank = next(b for b, ns in BANKS.items() if n in ns)
            position = ("top", "middle", "bottom")[BANKS[bank].index(n)]
            label += f" / Backbox {bank.upper()} {position} rollover"
            physical["quantity"] = 2
            physical["location"] = "Playfield drop target and parallel backbox rollover"
            notes += " Two normally-open physical contacts share one matrix input; only the target is placed in playfield space. The backbox contact carries a .05 capacitor."
        if n in (33,34,35):
            notes += " Ball-count contact in the three-ball runway; initial occupied state follows the retained table."
        if n in (11,12,13):
            notes += " Sling leaf-contact quantity is not inferred from one modeled wall."
        bus = row["drawn_common_bus"]
        wire, connection = bus.split(" (")
        wiring = {"board": "MPU-200 A4", "control_wire": wire, "control_connection": "A4" + connection.rstrip(")"),
                  "return_connection": "A4" + row["jack_no"]}
        if row["wire_color"]:
            wiring["return_wire"] = row["wire_color"]
        else:
            notes += " The manual switch10 wire-color cell is genuinely blank; no pattern is used to fill it."
        physical["notes"] = notes
        item = {"id": f"switch.matrix-{n:02}", "label": label, "kind": "switch",
                "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": aliases("switch", n, True),
                "availability": "used", "normally_closed": False, "pulse": n in (4,9,10,11,12,13,27,28),
                "physical": physical, "wiring": wiring, "provenance": prov("manual.catacomb", "schematic.catacomb", "runtime.catacomb")}
        if n == 8:
            item["provenance"]["source_refs"] += ["script.catacomb", "archive-table.catacomb"]
        if n in SWITCH_OBJECTS:
            obj = SWITCH_OBJECTS[n]
            item["spatial"] = located(raw, item["id"], "sensor", [(obj, point(raw, obj))])
        else:
            item["spatial"] = na("cabinet_or_service", "manual.catacomb")
        if n in (33,34,35): item["initial_active"] = True
        result.append(item)
    for n in (81,82,83,84):
        used = n in (82,84)
        label = {81:"Unfitted upper right flipper",82:"Right cabinet flipper button",83:"Unfitted upper left flipper",84:"Left cabinet flipper button"}[n]
        result.append({"id": f"switch.flipper-{n}", "label": label, "kind": "switch" if used else "virtual",
                       "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": aliases("switch", n),
                       "availability": "used" if used else "unused", "normally_closed": False, "pulse": False,
                       "physical": {"location": "Cabinet", "notes": "Generic flipper-column positions; the MPU matrix read cannot select this synthetic column. Lower button bits drive paired synthetic outputs."},
                       "spatial": na("cabinet_or_service" if used else "unused", "core.catacomb", "manual.catacomb"),
                       "provenance": prov("core.catacomb", "manual.catacomb", "runtime.catacomb")})
    dip_rows = raw["manual"]["pdf_9_switch_assignments"]
    for n in range(1,33):
        row = next(r for r in dip_rows if str(n) in r["mpu_switch_numbers"].split(","))
        unused = row["label"] == "NOT USED"
        result.append({"id": f"dip.option-{n:02}", "label": f"MPU option {n}: {row['label']}", "kind": "dip_switch",
                       "binding": {"group": "pinmame.input.dip", "device": n}, "aliases": [],
                       "availability": "unused" if unused else "used",
                       "physical": {"switch_type": "dip", "location": "MPU-200 option banks S1-S32", "notes": "See the complete source tables, preserving each chart's bit order; no default DIP state is imposed."},
                       "spatial": na("dip_switch", "manual.catacomb"), "provenance": prov("manual.catacomb", "core.catacomb")})
    for n, label, obj in ((1,"Left main flipper EOS","LeftFlipper"),(2,"Right main flipper EOS","RightFlipper"),
                           (3,"Door memory-clear contact",None),(4,"Backbox flipper EOS",None),
                           (5,"Front-door slam contact",None)):
        item = {"id": f"switch.direct-{n}", "label": label, "kind": "switch", "availability": "used",
                "binding": {"group": "physical.input.direct", "device": n}, "aliases": [], "normally_closed": n in (1,2,4),
                "physical": {"location": "Main flipper assembly" if obj else "Backbox / cabinet", "switch_type": "button" if n == 3 else "leaf",
                             "notes": "Physical contact outside the public switch API. EOS placement projects onto its own flipper assembly; the controller does not model EOS current or timing."},
                "provenance": prov("manual.catacomb", "schematic.catacomb")}
        if n == 3:
            item["physical"] = {"location":"Inside coin door", "switch_type":"button",
                                "notes":"Separate normally-open door MEMORY CLEAR contact, also called S33 in the assembly drawing. The cabinet sheet routes A4J3-5 (W) through it to A3J2-7 (Y-R). This remote contact is distinct from the MPU's on-board S33 NMI button at public -6; no PinMAME transport is inferred for the door contact."}
            item["wiring"] = {"board":"MPU-200 A4 / SDU A3", "control_connection":"A4J3-5", "control_wire":"W", "return_connection":"A3J2-7", "return_wire":"Y-R"}
        if n == 5:
            item["physical"] = {"location":"Front coin door", "switch_type":"tilt",
                                "notes":"Separate normally-open slam contact: factory manual PDF18 routes MPU J4-13 B-O through this contact to SDU J2-7 Y-R. The cabinet drawing PDF2 shows its open rest position. Generic stern.vbs calls matrix8 slam, but Catacomb uses matrix8 for the left button; no public binding is inferred for this hard-wired contact."}
            item["wiring"] = {"board":"MPU-200 A4 / SDU A3", "control_connection":"A4J4-13", "control_wire":"B-O", "return_connection":"A3J2-7", "return_wire":"Y-R"}
        item["spatial"] = located(raw, item["id"], "sensor", [(obj, point(raw,obj))]) if obj else na("cabinet_or_service", "manual.catacomb")
        result.append(item)
    return result


def outputs(raw: dict) -> list[dict]:
    result = []
    physical_rows = {int(r["id_number"]):r for r in raw["manual"]["pdf_21_solenoid_identification"] if r["id_number"]}
    for physical, n in PHYSICAL_TO_PUBLIC.items():
        row = physical_rows[physical]
        unused = n in (15,17,18)
        identifier = f"device.{slug(COIL_NAMES[n])}"
        item = {"id": identifier, "label": COIL_NAMES[n], "kind": "relay" if n in (17,18,19,20) else "coil",
                "binding": {"group": "pinmame.output.solenoid", "device": n},
                "aliases": aliases("solenoid", n) + [{"namespace":"manual.self-test","value":str(physical)}],
                "availability": "unused" if unused else "used", "provenance": prov("manual.catacomb", "schematic.catacomb", "runtime.catacomb")}
        notes = f"Factory driver {row['trans_number']}; test number {physical} is distinct from public {n}."
        if unused:
            notes += " This machine's table prints N/U. The ROM pulses it during its diagnostic sweep; that pulse does not prove a fitted load."
            item["spatial"] = na("unused", "manual.catacomb", "runtime.catacomb")
        elif n in (6,19,20):
            item["spatial"] = na("cabinet_or_service", "manual.catacomb", "schematic.catacomb")
        elif n in COIL_OBJECTS:
            obj = COIL_OBJECTS[n]
            item["spatial"] = located(raw, identifier, "effect", [(obj, point(raw,obj))])
            notes += f" Projected onto its own {obj} mechanism; this is not a measured under-playfield coil center."
        else:
            bank = "abcd"[n-11]
            pts = [point(raw,f"sw{x}") for x in BANKS[bank]]
            xy = tuple(sum(p[i] for p in pts)/len(pts) for i in (0,1))
            item["spatial"] = located(raw,identifier,"effect",[(f"bank-{bank}-projection",xy)])
            notes += f" Reset actuator projected onto the mean of this bank's three actual target-wall centroids, {BANKS[bank]}; not a physical coil measurement."
        item["physical"] = {"location": "Cabinet/backbox" if n in (6,19,20) else "Playfield / under playfield", "notes": notes}
        if not unused:
            item["wiring"] = {"board": "SDU-100 A3", "driver_transistor": row["trans_number"],
                              "control_connection": "A3" + row["jack"], "control_wire": row["wire_color"]}
            part = "B-27-2300" if n in (11,12,13,14) else "J-26-1500" if n in (3,4,5) else "J-26-1200" if n in (1,2) else "N-26-1200" if n == 6 else "J-28-2300" if n in (7,8,9,10) else None
            if part: item["physical"]["part_number"] = part
        if n == 6: item["physical"]["notes"] += " Cabinet sheet p2 prints B-Y; the machine's coil table and SDU sheet print G-B at J2-5. Structured wiring follows the agreeing latter sources."
        if n == 19:
            # The table's J1-8/9 entries are switched contact leads, not the relay-coil drive.
            item["wiring"] = {"board":"SDU-100 A3", "driver_transistor":"Q15"}
            item["physical"]["notes"] += " Q15 drives the on-board K1 enable relay; the manual J1-8/G and J1-9/O continuation describes its main-flipper contact leads. No external relay-coil connector is asserted."
        if n == 20:
            item["provenance"]["status"] = "observed"
            item["physical"]["notes"] += " Runtime20 is sustained backbox enable; p23 shows a relay contact gating the separately wired whip coil. Q18-to-relay-coil harness identification is not fully traced. No relay_gated relationship to the whip is asserted."
        result.append(item)
    for n, obj, side in ((46,"RightFlipper","right"),(48,"LeftFlipper","left")):
        item = {"id": f"device.{side}-flipper", "label": f"{side.title()} main flipper", "kind": "coil", "availability": "used",
                "binding": {"group":"pinmame.output.solenoid","device":n},"aliases":aliases("solenoid",n),
                "physical":{"location":"Playfield", "quantity":1, "part_number":"J-25-475/34-4500",
                            "notes":"One dual-winding assembly. The paired synthetic power/held outputs rise together for the full enabled button closure; they do not measure winding current or EOS timing."},
                "spatial":located(raw,f"device.{side}-flipper","effect",[(obj,point(raw,obj))]),
                "provenance":prov("manual.catacomb","core.catacomb","runtime.catacomb")}
        result.append(item)
        result.append({"id":f"signal.{side}-flipper-power-mirror","label":f"{side.title()} synthetic flipper power mirror","kind":"virtual","availability":"used",
                       "binding":{"group":"pinmame.output.solenoid","device":n-1},"aliases":aliases("solenoid",n-1),
                       "physical":{"notes":"Synthetic paired state of the same flipper assembly, not another physical coil."},
                       "spatial":na("virtual","core.catacomb"),"provenance":prov("core.catacomb","runtime.catacomb")})
    result.append({"id":"device.backbox-whip-coil","label":"Hard-wired backbox flipper coil","kind":"coil","availability":"used",
                   "binding":{"group":"physical.output.direct","device":1},"aliases":[],
                   "physical":{"location":"Backbox","part_number":"J-25-600/34-4500","quantity":1,"notes":"Right-button-driven dual-winding coil behind the factory relay contact. No separate MPU pulse callback is asserted."},
                   "spatial":na("cabinet_or_service","manual.catacomb"),"provenance":prov("manual.catacomb","photos.catacomb")})
    for key, row in raw["lamp_rows"].items():
        n = int(key); printed = row["printed_table_row"]; unknown = printed is None
        label = printed["description"].replace('"','').title() if printed else f"Unnamed lamp-driver {row['diagram']['transistor']} load"
        identifier = f"lamp.scr-{row['diagram']['transistor'].lower()}"
        item = {"id":identifier,"label":label,"kind":"lamp","availability":"unknown" if unknown else "used",
                "binding":{"group":"pinmame.output.lamp","device":n},"aliases":aliases("lamp",n),
                "wiring":{"board":"LDA-100 A5","driver_transistor":row["diagram"]["transistor"]},
                "provenance":prov("schematic.catacomb","script.catacomb",status="observed" if unknown else "validated")}
        if unknown:
            endpoint = {2:"J1-19",29:"J2-23"}[n]
            item["wiring"]["control_connection"] = "A5"+endpoint
            item["physical"] = {"notes":f"Table row omitted, not printed blank or N/U. Drawing reaches {endpoint}; fitment/meaning unresolved. Render proxies and missing script activity cannot prove a load or non-fitment. Physical harness/socket inspection is required."}
        else:
            item["wiring"].update(control_connection="A5"+printed["jack_lda"]+"-"+printed["jack_pin_no"],control_wire=printed["wire_color"])
            item["physical"] = {"location":"Backbox" if n in (13,45,61,63) else "Playfield", "part_number":"8A-101 (#44)",
                                "notes":f"Factory IC/code {printed['ic']}/{printed['code']}, pin{printed['ic_pin_no']}; one named circuit, not a render-object count."}
            if n in (13,45,61,63):
                item["spatial"] = na("cabinet_or_service","schematic.catacomb","photos.catacomb")
            else:
                matches = data.mapped_lights(raw,n)
                if not matches: raise ValueError(f"named playfield lamp has no mapped light: {n}")
                bulb = f"bulb{n}"
                item["spatial"] = located(raw,identifier,"emitter",[(bulb,mesh_point(raw,bulb))])
                item["physical"]["quantity"] = 1
            if n == 11:
                item["physical"].update(quantity=2,location="Playfield insert and backbox legend")
                item["physical"]["notes"] += " Two endpoints J1-26 and J2-21; one playfield placement, one backbox emitter outside this space."
            if printed["jack_lda"] == "J2" and n not in (13,45,61,63,11):
                item["physical"]["notes"] += " Connector block says TO BACK BOX, but the named insert and physical photographs put this load on the playfield; connector routing is not physical-location authority."
        result.append(item)
    gi_points = [(name,mesh_point(raw,name)) for name in raw["collections"]["GIBulbPrims"]]
    gi_points += [(name,mesh_point(raw,name)) for name in ("bumperbulb1","bumperbulb2")]
    result.append({"id":"gi.transformer-illumination","label":"Transformer-fed general illumination","kind":"gi","availability":"used",
                   "binding":{"group":"physical.output.gi","device":1},"aliases":[],
                   "physical":{"location":"Playfield, backbox and coin door","notes":"23 actual modeled playfield bulb meshes are retained as observations. This is not the factory total: star/button and lower-post illumination plus hidden/apron, backbox and coin-door sockets are not fully inventoried. No total quantity is asserted."},
                   "wiring":{"power_connection":"A2J1-8","power_wire":"W","return_connection":"A2J1-1","return_wire":"R","nominal_voltage_v":6,"voltage_type":"ac"},
                   "spatial":located(raw,"gi.transformer-illumination","emitter",gi_points),"provenance":prov("schematic.catacomb","photos.catacomb")})
    return result


def mechanisms() -> list[dict]:
    rows = []
    def add(identifier,label,kind,actuators,sensors,behavior,status="validated"):
        rows.append({"id":"mechanism."+identifier,"label":label,"kind":kind,"actuators":actuators,"sensors":sensors,
                     "behavior":behavior,"provenance":prov("manual.catacomb","script.catacomb","runtime.catacomb",status=status)})
    for i,(bank,ns) in enumerate(BANKS.items(),11):
        add("bank-"+bank,"Three-target bank "+bank.upper(),"drop_target_bank",["device.drop-bank-"+bank+"-reset"],
            [f"switch.matrix-{n:02}" for n in ns],
            "Three targets latch down independently; the bank reset lifts all three and opens their contacts. All down spots the rotating color/number. Startup resets every bank. Each contact is paralleled with its own backbox rollover. A jammed target can hold that shared input and mask the rollover; keep contacts closed until reset. No physical speed or pulse duration is inferred from animation.")
    add("ball-feed","Three-ball runway and outhole reflex","kicker",["device.outhole-reflex","device.outhole-turnstyle"],
        [f"switch.matrix-{n:02}" for n in (17,33,34,35)],
        "A drained ball closes17; output9 advances it into the three-position runway.33 is the serve end, then34/35. Output10 releases a ball to the shooter lane. Start expects three balls and resets banks; the table starts33-35 occupied. Move switches with the ball: a coil does not directly actuate a remote runway sensor. A missing ball or a held drain contact can prevent a normal serve. The hand plunger is passive.")
    for side,n in (("left",36),("right",37)):
        add(side+"-captive-hole",side.title()+" captive-ball hole","kicker",["device."+side+"-kickout-hole"],[f"switch.matrix-{n:02}"],
            "A ball stays on the hole switch while captive; another ball can be served. Completing a color releases captive balls, or defers release to the next turn when completed in the backbox. An isolated switch closure need not eject immediately. The kick clears the local switch only as the ball leaves; a jam can leave it held.")
    for side,n,direct in (("right",82,2),("left",84,1)):
        add(side+"-flipper",side.title()+" main flipper","other",[f"device.{side}-flipper"],
            [f"switch.flipper-{n}",f"switch.direct-{direct}"],
            "Cabinet button energizes a dual-winding coil through K1. A normally-closed hard-wired EOS changes the winding circuit near full travel; spring return restores rest after release. Output19 enables main flippers and drops at end-of-ball/backbox phase. Synthetic paired outputs do not measure winding or EOS state. A failed EOS/contact/relay can change travel or cause heating; no virtual timing calibration is claimed.")
    add("main-flipper-enable","Shared main-flipper enable circuit","other",["device.main-flipper-enable-relay"],[],
        "One K1 relay enables both main-flipper circuits. It is owned once here and relates to both coils through explicit relay_gated relationships. The ROM raises public19 at Start and drops it before the backbox feature; these are enable states, not flipper strokes.")
    add("backbox-bagatelle","Retained-ball backbox bagatelle","other",["device.backbox-whip-coil","device.backbox-playfield-enable"],
        ["switch.direct-4","switch.matrix-08"]+[f"switch.matrix-{n:02}" for bank in BANKS.values() for n in bank],
        "One retained yellow ball returns to the bottom whip arm. A right-button-driven dual-winding flipper throws it around the right guide, through the passive upper wireform gate and into four columns of three rollovers, then back to rest. Courtesy and earned shots follow bonus. The left button stops bank lamps using matrix input 8; the modern 2.0.1 script agrees, while only the older archive table incorrectly writes switch 8 from RightFlipperKey. Public output 20 remains enabled through strokes while main-flipper enable 19 is off. Factory p23 shows a relay contact in series with the whip, but the Q18-to-relay-coil harness path remains untraced; no direct relay relationship is asserted. A stuck rollover or retained target contact can mask a score; a displaced passive gate can misroute or trap the ball. Physical timing and stroke strength remain table-owned.","observed")
    rows[-1]["provenance"]["source_refs"].append("archive-table.catacomb")
    add("spinner-and-gate","Spinner lane and passive gate","gate",[],["switch.matrix-04","switch.matrix-05"],
        "Ball rotation pulses spinner4 repeatedly; lane gate5 records traversal and passively returns. It scores/collects the lit award. Neither has a controller-driven actuator; the star-button and stand-up targets likewise return mechanically, not through a solenoid callback.")
    for n,sw in ((1,9),(2,10),(3,11),(4,12),(5,13)):
        add("reflex-"+str(sw),COIL_NAMES[n],"other",["device."+slug(COIL_NAMES[n])],[f"switch.matrix-{sw:02}"],
            "Ball closure of the local normally-open switch causes the ROM to pulse this mechanism's own coil, confirmed in isolation. Spring return restores the assembly. A coil pulse is not a measured sensor actuation or a calibrated physical force.")
    return rows


def source_records(facts: dict) -> list[dict]:
    revision = facts["pinmame_revision"]; a = facts["artifacts"]
    def excerpt(name,locator,image=None,derivation=None):
        e={"id":"excerpt.catacomb."+slug(name.removesuffix(".md")),"path":facts["excerpts"][name]["path"],
           "sha256":facts["excerpts"][name]["sha256"],"locator":locator,"method":"mixed","transcribed_by":"Curator transcription, checked against retained source text and rendered drawings","reviewed":True}
        if image: e.update(image=facts["excerpts"][image]["path"],image_sha256=facts["excerpts"][image]["sha256"],image_derivation=derivation)
        return e
    common={"license":"NOASSERTION; retained for local research, originals not redistributed","attribution":"Stern Electronics, Inc.; hosted by IPDB; retrieved through Internet Archive Wayback Machine","source_id":"469"}
    manual={"id":"manual.catacomb","kind":"manual","uri":"https://web.archive.org/web/20250119091324id_/https://www.ipdb.org/files/469/Stern_1981_Catacomb_Manual.pdf",
            "locator":"Verified IPDB469 Catacomb, model147, https://www.ipdb.org/machine.cgi?id=469 ; original https://www.ipdb.org/files/469/Stern_1981_Catacomb_Manual.pdf ; PDF pages4,6-23. "+a["manual"]["path"],
            "sha256":a["manual"]["sha256"],"original_filename":"Stern_1981_Catacomb_Manual.pdf","acquired_at":a["manual"]["acquired_at"],**common,
            "excerpts":[excerpt("manual-tables.md","PDF pages7,9-21; entire cited tables"),excerpt("backbox-flipper-wiring.md","PDF23 / printed22, Figure8-4","backbox-flipper-wiring.webp","Stern_1981_Catacomb_Manual.pdf page 23, crop box 0.65,0.22,1,0.95, scanned page rendered at its native resolution (embedded image xref 110, 606px across 8.42in), rendered at 72 dpi, grayscale, 213x578 WebP quality 80"),
                        excerpt("service-locations.md","PDF4 / printed3, separate MPU and coin-door MEMORY CLEAR callouts","service-locations.webp","Stern_1981_Catacomb_Manual.pdf page 4, crop box 0.01,0.06,0.92,0.64, scanned page rendered at its native resolution (embedded image xref 15, 606px across 8.42in), rendered at 72 dpi, grayscale, 552x456 WebP quality 80")]}
    schematic={"id":"schematic.catacomb","kind":"manual","uri":"https://web.archive.org/web/20250119091418id_/https://www.ipdb.org/files/469/Stern_1981_Catacomb_Schematics.pdf",
               "locator":"IPDB469 https://www.ipdb.org/machine.cgi?id=469 ; original https://www.ipdb.org/files/469/Stern_1981_Catacomb_Schematics.pdf ; native Catacomb playfield p3, LDA p6, MPU p7, SDU p9 and common sheets1/2/10. "+a["schematic"]["path"],
               "sha256":a["schematic"]["sha256"],"original_filename":"Stern_1981_Catacomb_Schematics.pdf","acquired_at":a["schematic"]["acquired_at"],**common,
               "excerpts":[excerpt("lamp-driver.md","PDF6 full printed table and drawn decoder/connector lines; rotated source raster derives155dpi, not fixed200","lamp-connectors.webp","Stern_1981_Catacomb_Schematics.pdf page 6, crop box 0.53,0.17,0.66,0.77 of the page, rendered at 155 dpi with pdftoppm, reduced to 333px wide grayscale, quality 75 WebP"),
                           excerpt("schematics.md","PDF3 physical GI branch; raster-derived159dpi","playfield-gi-wiring.webp","Stern_1981_Catacomb_Schematics.pdf page 3, crop box 0.17,0.66,0.36,0.85 of the page, rendered at 159 dpi with pdftoppm, reduced to 500px wide grayscale, quality 75 WebP"),
                           excerpt("mpu-nmi.md","PDF7, MPU-200 drawing340-602-S, on-board S33 to U9-6 NMI","mpu-nmi.webp","Stern_1981_Catacomb_Schematics.pdf page 7, crop box 0.22,0.26,0.43,0.51, scanned page rendered at its native resolution (embedded image xref 50, 2628px across 10.69in), rendered at 246 dpi, grayscale, 855x720 WebP quality 80"),
                           excerpt("door-service.md","PDF2, CABINET AND FRONT DOOR WIRING, service contacts","door-service.webp","Stern_1981_Catacomb_Schematics.pdf page 2, crop box 0.035,0.007,0.31,0.105, scanned page rendered at its native resolution (embedded image xref 20, 2520px across 10.91in), rendered at 231 dpi, grayscale, 1052x266 WebP quality 80")]}
    table_common={"license":"NOASSERTION; community table retained locally, not redistributed","attribution":"UnclePaulie; Hauntfreaks scan; Redbone graphics; VPW testing; prior HSM/lander code","acquired_at":a["table"]["acquired_at"]}
    return [manual,schematic,
        {"id":"identity.catacomb","kind":"human_review","uri":"https://web.archive.org/web/20250119091248id_/https://www.ipdb.org/machine.cgi?id=469","sha256":a["ipdb_page"]["sha256"],"source_id":"469","acquired_at":a["ipdb_page"]["acquired_at"],"license":"NOASSERTION","attribution":"Internet Pinball Database contributors","locator":"Verified Catacomb, Stern Electronics, October1981, model147, MPU200; original machine page https://www.ipdb.org/machine.cgi?id=469 ; retained "+a["ipdb_page"]["path"]},
        {"id":"archive-table.catacomb","kind":"vpx_table","uri":"retained:stern/catacomb-1981/Catacomb (Stern 1981).vpx","sha256":a["archive_table"]["sha256"],"revision":"0.9","known_working":False,"license":"NOASSERTION; local table retained, not redistributed","attribution":"32assassin; embedded metadata credits mfuegemann's VP9 version","locator":a["archive_table"]["path"]+"; retained extraction "+a["archive_extraction"]["sha256"]+"; duplicate sw2_Dropped handlers are a table defect; modern2.0.1 takes precedence","excerpts":[excerpt("vpx-runtime.md","Supplemental local table and rejected binding defects")]},
        {"id":"table.catacomb","kind":"vpx_table","uri":"https://vpuniverse.com/files/file/21750-catacomb-stern-1981/","revision":"2.0.1, 2024-09-27","sha256":a["table"]["sha256"],"locator":a["table"]["path"]+"; geometry observed, physical fitment reconciled only where stated",**table_common,"excerpts":[excerpt("vpx-runtime.md","Exact retained bounds, bindings, modeled bulbs and limitations")]},
        {"id":"script.catacomb","kind":"vpx_script","uri":"https://vpuniverse.com/files/file/21750-catacomb-stern-1981/","revision":"2.0.1","sha256":"177b7d10a092f82b8b8f00faee2c495eed5cb1353f01bccb20a529ef344055c5","locator":"extracted/script.vbs:270 vpmMapLights AllLamps; 727-741 callbacks; 747-870 ball/feed/backbox; 1138-1456 switches/targets; 5007-5071 legend handlers",**table_common,"excerpts":[excerpt("vpx-runtime.md","Runtime bindings and exact physical-versus-render boundary")]},
        {"id":"core.catacomb","kind":"pinmame_core","uri":"https://github.com/vpinball/pinmame/tree/"+revision,"revision":revision,"license":"GPL-2.0-or-later","attribution":"PinMAME contributors","locator":"src/wpc/stgames.c:1145-1177, INITGAME, dispst7; by35.c by35_lampStrobe, pia1b_w, SWITCH_UPDATE; by35.h BY35_SWCPUDIAG; core.c core_updateSw; core.h FLIP_SW; gen.h GEN_STMPU200; src/libpinmame/libpinmame.cpp:875-955 segment-derived DMD", "excerpts":[excerpt("core-runtime.md","by35.h:230; by35.c:475-481; libpinmame.cpp:875-955")]},
        *[{"id":"library."+name+".catacomb","kind":"vpx_script","uri":"retained:"+a[name+"_vbs"]["path"],"sha256":a[name+"_vbs"]["sha256"],"acquired_at":a[name+"_vbs"]["acquired_at"],"revision":"VBS v3.61 header","license":"NOASSERTION; retained local library, not redistributed","attribution":"VPinMAME script contributors","locator":a[name+"_vbs"]["path"],"excerpts":[excerpt("libraries.md","Actual retained core.vbs and stern.vbs key handlers, constants and game-specific limits")]} for name in ("core","stern")],
        {"id":"extraction.catacomb","kind":"vpx_table","uri":"retained:stern/catacomb-1981/vpu-2.0.1/extracted/manifest.json","sha256":a["extraction"]["sha256"],"revision":"vpxtool git:v0.33.3","locator":"Official build_external_evidence_manifest: case-sensitive sorted POSIX paths with byte size and SHA256; canonical compact sorted JSON plus LF; "+str(a["extraction"]["file_count"])+" files, "+str(a["extraction"]["total_bytes"])+" bytes; world OBJ "+a["world_obj"]["sha256"],**table_common},
        {"id":"runtime.catacomb","kind":"runtime_scenario","uri":"retained:catacomb-1981/harness/manifest.json","sha256":a["runtime"]["sha256"],"revision":revision,"locator":a["runtime"]["path"]+"; compact observations "+RUNTIME.as_posix()+"; five fresh-state runs; library "+facts["library_sha256"]+"; ROM "+facts["rom_archive_sha256"],"license":"MIT tooling; original ROM rights retained, no ROM bytes redistributed","attribution":"PinMAME contributors; Stern Electronics; local authorized ROM corpus","excerpts":[excerpt("vpx-runtime.md","ROM-output and displayed-number observations, excluding host readback")]},
        {"id":"photos.catacomb","kind":"human_review","uri":"https://pinside.com/pinball/forum/topic/catacomb-1","sha256":a["photo_manifest"]["sha256"],"acquired_at":a["photo_manifest"]["acquired_at"],"license":"NOASSERTION; photographs retained locally only","attribution":"Chicanelane and Pinside gallery contributors; IPDB photograph credited on retained source page","locator":a["photo_manifest"]["path"]+" gives original image URLs/times/hashes; ad168655 photos0/1/7/8/11; IPDB469 image49161; actual primary visual inspection, not a complete socket survey","excerpts":[excerpt("photos.md","Reviewed physical photographs and exact limitations")]}]


def build(root: Path = ROOT) -> dict[Path, bytes]:
    raw=data.load_raw(root/"tools/seeds/stern/catacomb-1981-raw.json"); facts=load_json(root/FACTS)
    for record in facts["excerpts"].values():
        p=root/record["path"]
        if data.sha256(p)!=record["sha256"]: raise ValueError(f"excerpt digest mismatch: {p}")
    machine=copy.deepcopy(facts["machine"]);machine.update(kind="physical_pinball",model_number="147",playfield={"width":952.941,"height":1976.471,"units":"vpx","provenance":prov("table.catacomb")})
    drivers=copy.deepcopy(facts["drivers"])
    for d in drivers:
        d["physical_compatibility"]="identical"
        d["variant_notes"]="Same GEN_STMPU200, dispst7 and ST300V hardware contract. "+({"catacomb":"Production firmware.","catacofp":"Free-play program changes U5 only; no hardware revision.","cataconb":"2021 tournament firmware suppresses the after-ball bagatelle, described upstream as a quick unpolished hack; it does not remove fitted hardware or create a 2021 physical edition."}[d["id"]])
    ins=inputs(raw); outs=outputs(raw)
    displays=[]
    for i,start,width,label in ((0,1,7,"Player1 score"),(1,9,7,"Player2 score"),(2,17,7,"Player3 score"),(3,25,7,"Player4 score"),(4,35,2,"Credits"),(5,38,2,"Ball in play / match")):
        displays.append({"id":f"display.{i}","label":label,"kind":"segment","controller_index":i,"segment_start":start,"width":width,"height":1,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service","manual.catacomb","core.catacomb"),"provenance":prov("manual.catacomb","core.catacomb","photos.catacomb")})
    relationships=[{"id":f"relationship.main-enable-{side}","kind":"relay_gated","source":"device.main-flipper-enable-relay","destination":f"device.{side}-flipper","provenance":prov("manual.catacomb","schematic.catacomb")} for side in ("left","right")]
    definition={"format":"pinmame-machine-definition","schema_version":2,"machine":machine,
                "coverage":{"status":"partial","missing":MISSING,"dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"observed","physical_wiring":"observed","mechanisms":"observed","variant_coverage":"validated","recreation_knowledge":"validated","spatial_placement":"observed"}},
                "controller":{"platform":"pinmame.stern-mpu200","hardware_generation":"0x1000000","inversion_applied_by_emulator":True},
                "drivers":drivers,"inputs":ins,"outputs":outs,"displays":displays,"mechanisms":mechanisms(),"relationships":relationships,
                "sources":source_records(facts),"knowledge":{"path":NOTE.as_posix(),"status":"partial"},"conflicts":[]}
    spatial={"format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,"coverage_status":"partial",
             "coordinate_convention":"Player view: x0 left/x1 right; y0 rear/y1 apron.",
             "bounds":raw["table_bounds"],"transformation":"(x-left)/(right-left), (y-top)/(bottom-top), rounded to6decimals; same arithmetic as extract_spatial_candidates",
             "artifacts":facts["artifacts"],"extraction_manifest_algorithm":"tools/build_external_evidence_manifest.py; case-sensitive POSIX paths sorted, each size/SHA256; sorted compact UTF8 JSON plus LF",
             "world_obj_units":"vpu","placements":[{"device_id":x["id"],**p} for x in ins+outs for p in x.get("spatial",{}).get("placements",[])],
             "raw_objects":raw["objects"],"raw_mesh_bounds":raw["meshes"],
             "projections":["Bank reset coils: mean of three target-wall drag-point centroids","Bumper/sling effects and outhole/turnstyle: own assembly anchor, not measured coil center","Main EOS contacts: corresponding flipper pivot"],
             "excluded_helpers":["lN/lNa doubles","GI top/lane light maps","Backbox TriggerB surfaces and VR mirrors","Lamp2 proxy with no proven socket","Star-button GI light without a separately modeled socket"],
             "blockers":["Q12/public2/J1-19 and Q15/public29/J2-23 loads unidentified; physical harness/socket inspection needed","GI socket total and hidden/apron, backbox and cabinet emitters incomplete; 23 mesh locations do not prove factory quantity","No factory drawing/control fit independently validates all retained placements","Q18 enable-to-backbox-relay coil path not traced; p23 proves contact/coil topology, runtime20 proves feature state"],
             "promotion_decision":"Remain partial; no readiness credit from observed mesh centers or unavailable load names."}
    runtime={"format":"pinmame-machine-evidence","version":1,
             "extractor":{"id":"tools/curate_catacomb.py","version":1},
             "source":{"kind":"runtime_scenario","repository":"https://github.com/vpinball/pinmame",
                       "revision":facts["pinmame_revision"],"path":"catacomb-1981/harness/manifest.json",
                       "sha256":facts["artifacts"]["runtime"]["sha256"],"license":"MIT tooling; original ROM rights retained",
                       "attribution":"PinMAME contributors; Stern Electronics; authorized local ROM corpus","quality":"observed"},
             "driver_ids":["catacomb"],"machine_ids":[MACHINE_ID],"switches":[],"outputs":[],"states":[],"mechanisms":[],"recreation_notes":[],
             "runtime":{"game":"catacomb","rom_archive_sha256":facts["rom_archive_sha256"],
                        "emulator":{"binary":"builds/pinmame-46e1a01a/Release/pinmame64.dll","sha256":facts["library_sha256"],"built_from_revision":facts["pinmame_revision"]},
                        "raw_runs":[{"name":r["path"],"sha256":r["sha256"],"scenario_path":r["retained_scenario_path"],"scenario_sha256":r["scenario_sha256"],
                                     "action_count":r["action_count"],"self_test_pulses":{"self-test":1,"coil-test":4,"switch-test":5}.get(name,0),
                                     "nvram_initialization":"New isolated state directory; no NVRAM or switch state inherited from another run."} for name,r in facts["runtime"].items()],
                        "command_template":"python -B tools/run_pinmame_harness.py --library <working-root>/builds/pinmame-46e1a01a/Release/pinmame64.dll --game catacomb --rom-path <authorized-read-only-ROM-root> --work-dir <new-isolated-state> --scenario tools/harness-scenarios/stern/catacomb-<name>.json --output <review-root>/catacomb-1981/harness/<name>.json",
                        "observations":{"lamp_addresses_seen":sorted({n for r in facts["runtime"].values() for n in r["lamp_addresses"]}),
                                        "solenoid_addresses_seen":sorted({n for r in facts["runtime"].values() for n in r["solenoid_addresses"]}),
                                        "gi_addresses_seen":[],"service_language":"numeric seven-segment diagnostics",
                                        "physical_service_solenoid_to_public":{str(k):v for k,v in PHYSICAL_TO_PUBLIC.items()},
                                        "named_action_observations":[{"label":f"Isolated playfield switch {sw}","input_kind":"switch","input_address":sw,
                                                                      "observed_switch_addresses":[],"active_solenoid_addresses":[],"transitioned_solenoid_addresses":[sol],
                                                                      "result":"observed"} for sw,sol in ((9,1),(10,2),(11,3),(12,4),(13,5),(17,9))]}}}
    note=(root/NOTE_SEED).read_bytes()
    report_md="# Catacomb spatial blockers\n\nCoverage remains **partial**. Coordinates are retained table observations in player view, x0left/x1right and y0rear/y1apron.\n\n"+"\n".join("- "+x for x in spatial["blockers"])+"\n\nThe JSON report retains the exact source hashes, complete extraction counts, world-mesh bounds, object coordinates, normalization and every canonical placement. Bank/EOS/coil projections are explicit; no backbox proxy is projected onto the playfield.\n"
    return {DEFINITION:canonical_bytes(definition),SEED:canonical_bytes(definition),NOTE:note,REPORT:canonical_bytes(spatial),REPORT_MD:report_md.encode(),RUNTIME:canonical_bytes(runtime)}


def check(root: Path = ROOT) -> None:
    if (root/"machines/author-ready/stern/catacomb-1981.json").exists(): raise ValueError("refuse to overwrite an author-ready Catacomb artifact")
    for path,expected in build(root).items():
        actual=root/path
        if not actual.is_file() or actual.read_bytes()!=expected: raise ValueError(f"curator drift: {path}")


def verify_external(root: Path = ROOT) -> None:
    """Fail on any supplied bad root; skip only roots not supplied."""
    raw=data.load_raw(root/"tools/seeds/stern/catacomb-1981-raw.json");facts=load_json(root/FACTS)
    roots={k:Path(os.environ[e]) if os.environ.get(e) else None for k,e in (("vpx-sources","PINMAME_VPX_SOURCES_ROOT"),("manuals","PINMAME_MANUALS_ROOT"),("review-artifacts","PINMAME_REVIEW_ARTIFACTS_ROOT"))}
    for p in roots.values():
        if p is not None and not p.is_dir():raise ValueError(f"invalid evidence root: {p}")
    if roots["vpx-sources"] or roots["review-artifacts"]:
        data.verify_sources(raw,vpx_root=roots["vpx-sources"],review_root=roots["review-artifacts"])
    for key,record in facts["artifacts"].items():
        rel=Path(record["path"]);external=roots.get(rel.parts[0])
        if external is not None and data.sha256(external.joinpath(*rel.parts[1:]))!=record["sha256"]:raise ValueError(f"artifact digest mismatch: {key}")
    from build_external_evidence_manifest import check_manifest,build_manifest
    for key in ("extraction","archive_extraction","runtime"):
        record=facts["artifacts"][key];rel=Path(record["path"]);external=roots.get(rel.parts[0])
        if external is None:continue
        directory=external.joinpath(*rel.parts[1:]).parent
        if check_manifest(directory,"catacomb")!=record["sha256"]:raise ValueError(f"manifest digest mismatch: {key}")
        m=build_manifest(directory,"catacomb")
        if (len(m["files"]),sum(x["size"] for x in m["files"]))!=(record["file_count"],record["total_bytes"]):raise ValueError(f"manifest counts mismatch: {key}")
    review=roots["review-artifacts"]
    if review is not None:
        for name,record in facts["runtime"].items():
            run=review/record["path"]
            if data.sha256(run)!=record["sha256"]:raise ValueError(f"runtime mismatch: {name}")
            trace=load_json(run)
            if trace["failure"] is not None or trace["library_sha256"]!=facts["library_sha256"]:raise ValueError(f"invalid runtime: {name}")
        photo_manifest=review/"catacomb-1981/photo-research/parts-ad-manifest.json"
        for record in load_json(photo_manifest):
            photograph=photo_manifest.parent/record["file"]
            if photograph.stat().st_size!=record["bytes"] or data.sha256(photograph)!=record["sha256"]:
                raise ValueError(f"photo resource mismatch: {photograph}")
    for name,record in facts["runtime"].items():
        scenario=root/record["scenario_path"]
        if data.sha256(scenario)!=record["repository_scenario_sha256"]:raise ValueError(f"repository scenario mismatch: {name}")
        if review is not None:
            original=review/record["retained_scenario_path"]
            if data.sha256(original)!=record["scenario_sha256"] or load_json(original)!=load_json(scenario):
                raise ValueError(f"retained scenario mismatch: {name}")


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true");parser.add_argument("--regenerate",action="store_true");parser.add_argument("--verify-evidence",action="store_true")
    args=parser.parse_args()
    if args.verify_evidence:verify_external()
    if args.regenerate:
        if (ROOT/"machines/author-ready/stern/catacomb-1981.json").exists():raise ValueError("author-ready artifact exists")
        for path,payload in build().items():
            target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(payload)
    else:check()
    print("Catacomb: deterministic partial definition verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
