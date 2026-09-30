"""Deterministic, game-scoped curation of Data East Guns N' Roses (1994).

Factory tables are literal checked transcriptions in guns_n_roses_data.py.
Geometry is pinned to one retained complete extraction, never a different
script's object names. --check regenerates in memory and refuses all drift.
External verification is separate and explicit; bare CI needs no private files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships
from guns_n_roses_data import (
    ASSEMBLY_TABLES, COIL_CHART, FLIPPER_CHART, LAMP_COLUMNS, LAMP_NAMES,
    LAMP_ROWS, SWITCH_COLUMNS, SWITCH_NAMES, SWITCH_PARTS, SWITCH_ROWS,
)

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.guns-n-roses.1994"
STEM = "data-east/guns-n-roses-1994"
EXCERPTS = f"evidence/excerpts/{STEM}"
PIN = "pinmame.core.8371478a7640"
MANUAL = "manual.guns-n-roses.1994"
ADDENDUM = "manual-addendum.guns-n-roses.1994"
SCHEMATICS = "schematics.guns-n-roses.1994"
ASSEMBLY_MANUAL = "manual-upper-assembly.guns-n-roses.1994"
TABLE = "vpx-table.guns-n-roses.team-pp"
SCRIPT = "vpx-script.guns-n-roses.team-pp"
VPW = "vpx-script.guns-n-roses.vpw-1-2-1"
RUNTIME = "runtime.guns-n-roses.us-3-00"
ACTIVE_RUNTIME = "runtime.guns-n-roses.active-switches"
VBS = "vpm-library.guns-n-roses"
CORE_VBS = "vpm-core-library.guns-n-roses"
SB63 = "service-sb63.guns-n-roses.1994"
SB64 = "service-sb64.guns-n-roses.1994"
REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
PIN_FILES = (
    ("core.h", "9d2fa69f7fa6963adc793b272bb5cbfbf94e929c0d7f6b928b1b02a8ee15b2b3", "139-165,300-360; FLIP_SWNO and address bands"),
    ("core.c", "84aa5ccddc077b60c1331e32ee13d3d577fd5109d4e7a90001692f737a1c7963", "1700-1777,2182-2224,2591; button copies, synthetic outputs, no simData initialization"),
    ("s11.c", "cd1b989ac1eec8c95126e743829a8a3726e76a9b838a29339776d4025d75d2d4", "371-410,558-650,870-877,1188-1196; printer, mux, PIA and brightness models"),
    ("sim.c", "20579da60adf58538d5b8c93a0bf22bd8c6d4e3ea6657234cd371293bd05c405", "238; simulator-only output 49"),
)
PIN_REFS = (PIN, *(f"pinmame.{name.replace('.', '-')}.8371478a7640" for name, _, _ in PIN_FILES))
TABLE_SUBDIR = "data-east/guns-n-roses-1994/extractions/team-pp-2019-4e54ffbde40c"
MANUAL_FILENAME = "Data_East_1994_Guns_N_Roses_Manual.pdf"
MANUAL_SHA = "1afd9b93bc17a7b46841c00a23e6f6f02fd3c2e61e3cfe06ba9d88e31aaa7236"
GEOMETRY = load_json(ROOT / "tools/guns_n_roses_geometry.json")
MANUAL_ACQUISITIONS = load_json(ROOT / "tools/guns_n_roses_manual_provenance.json")["records"]


def prov(*refs: str, status: str = "validated") -> dict:
    # PIN names the controller contract; retain every exact file in its chain.
    expanded = [item for ref in refs for item in
                (PIN_REFS if ref == PIN else (VBS, CORE_VBS) if ref == VBS else (ref,))]
    return {"status": status, "source_refs": list(dict.fromkeys(expanded))}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def spatial(identifier: str, role: str, *objects: str) -> dict:
    return {
        "status": "observed",
        "placements": [
            {"id": f"{identifier}.{role}-{i}", "role": role, "space": "playfield",
             "x": GEOMETRY["objects"][obj]["xy"][0],
             "y": GEOMETRY["objects"][obj]["xy"][1],
             "provenance": prov(TABLE, SCRIPT, MANUAL, status="observed")}
            for i, obj in enumerate(objects, 1)
        ],
    }


def legacy(group: str, address: int, fallback: str) -> tuple[str, list]:
    if group == "pinmame.input.switch":
        old = GEOMETRY["legacy"]["inputs"].get(str(address))
    else:
        old = GEOMETRY["legacy"]["outputs"].get(f"{group}:{address}")
    namespace = {"pinmame.input.switch": "pinmame.switch",
                 "pinmame.output.lamp": "pinmame.lamp",
                 "pinmame.output.solenoid": "pinmame.solenoid"}.get(group)
    return (old["id"], old["aliases"]) if old else (
        fallback, [{"namespace": namespace, "value": str(address)}] if namespace else [])


def device(group: str, address: int, label: str, kind: str,
           availability: str, *refs: str) -> dict:
    identifier, aliases = legacy(group, address, f"{kind}.address-{address}".replace("--", "-minus-"))
    return {"id": identifier, "label": label, "kind": kind,
            "binding": {"group": group, "device": address}, "aliases": aliases,
            "availability": availability, "provenance": prov(*refs)}


SWITCH_OBJECTS = {
    **{n: f"sw{n}" for n in [16, 21, 22, 23, 24, 37, 38, 39, 40, 48, 49, 50, 51, 52,
                              53, 54, 55, 56, 58, 60]},
    **{n: f"SW{n}" for n in [17, 18, 19, 20, 33, 34, 35, 59]},
    36: "sw36", 57: "sw57", 25: "Bumper1", 26: "Bumper2", 27: "Bumper3",
    28: "RightSlingShot", 29: "LeftSlingShot", 30: "LeftSlingShotH",
}


def inputs() -> list:
    records = []
    for address, label in enumerate(SWITCH_NAMES, 1):
        unused = label == "Not Used"
        d = device("pinmame.input.switch", address, label, "switch",
                   "unused" if unused else "used", MANUAL, PIN, VPW)
        col, row = divmod(address - 1, 8)
        drive, drive_pin, transistor = SWITCH_COLUMNS[col]
        ret, ret_pin = SWITCH_ROWS[row]
        d["wiring"] = {"board": "CPU", "drive_wire": drive,
                       "drive_connection": drive_pin, "driver_transistor": transistor,
                       "return_wire": ret, "return_connection": ret_pin}
        d["physical"] = {"notes": f"Factory switch matrix column {col+1}, row {row+1}."}
        if unused:
            d["spatial"] = na("unused", MANUAL)
            d["physical"]["notes"] += " Factory explicitly marks Not Used; no contact fitted."
        else:
            d["normally_closed"] = False
            d["pulse"] = address in {17, 18, 19, 20, 25, 26, 27, 28, 29, 30}
            if address in range(9, 15):
                d["initial_active"] = True
            if SWITCH_PARTS[address-1] not in {"---", "See Cabinet"}:
                d["physical"]["part_number"] = SWITCH_PARTS[address-1]
            d["physical"]["notes"] += (
                " Public 1 is the active closure: GnR invSw is zero and Data East pia4a_r "
                "returns core_getSwCol without complementing. The exact scripts set 1 on "
                "Hit and 0 on UnHit (or hold drop state until reset). Do not reinvert.")
            if address in SWITCH_OBJECTS:
                d["spatial"] = spatial(d["id"], "sensor", SWITCH_OBJECTS[address])
                obj = SWITCH_OBJECTS[address]
                d["physical"]["notes"] += f" Geometry anchor: {obj}; sensor location on the named mechanism, not the coil winding."
            elif address <= 8 or address >= 62:
                d["spatial"] = na("cabinet_or_service", MANUAL, PIN)
            # Seven under-apron trough contacts have no separate local geometry.
        if address in {63, 64}:
            d["physical"]["notes"] += (
                f" ROM-readable copy only; direct writes are overwritten by core_updateSw. "
                f"A consumer drives host button {84 if address == 63 else 82}. "
                "The SSFB senses cabinet closure through Q7 (left) / Q5 (right); "
                "this matrix value is not a flipper EOS.")
            d["provenance"] = prov(MANUAL, PIN, VBS, RUNTIME)
        if address in {15,25,26,27,28,29,30,62,63,64}:
            d["provenance"] = prov(MANUAL,PIN,VPW,ACTIVE_RUNTIME)
        if address == 15:
            d["physical"]["notes"] += (
                " Real seventh/right trough miniature switch, not a software-only sensor. "
                "VPW models its occupancy around SolTrough/SolRelease; that surrogate is "
                "not evidence that the physical contact is absent.")
        if address in {28, 29}:
            d["physical"]["notes"] += (
                " Printed page 33 drawing transposes sling callouts 28/29. The full matrix, "
                "parts table and both scripts agree: 28 right, 29 left.")
        if address in {28, 29, 30}:
            d["physical"].update(quantity=2, switch_type="leaf")
            d["physical"]["notes"] += (
                " Factory PDF 58 lists two 180-5054-00 leaf contacts and two diodes per "
                "slingshot assembly, represented by this one matrix circuit. The VPX "
                "wall centroid is an impact-region proxy, not either contact's center. "
                "Individual physical contact positions remain unresolved.")
            d.pop("spatial", None)
        if address == 62:
            d["physical"]["switch_type"] = "microswitch"
            d["physical"]["notes"] += (
                " The gun assembly BOM instead lists 180-5143-00; both factory part "
                "numbers are retained, without asserting interchangeability.")
        records.append(d)
    for address, label in [(-7, "Black Advance"), (-6, "Green Up/Down Toggle")]:
        d = device("pinmame.input.switch", address, label, "switch", "used", PIN, MANUAL)
        d["spatial"] = na("cabinet_or_service", PIN, MANUAL)
        d["physical"] = {"switch_type": "button", "notes": (
            "DE_COMPORTS named keyboard port: Black is momentary; Green toggles service "
            "direction on a press edge. Use named keys; do not substitute persistent matrix writes.")}
        d["pulse"] = address == -7
        records.append(d)
    records.extend(flipper_column_inputs(
        flip_swno=(63, 64), flip_swno_text="FLIP6364 (FLIP_SWNO(63,64))",
        core_refs=PIN_REFS, button_refs=(VBS, CORE_VBS, VPW, RUNTIME, ACTIVE_RUNTIME),
        button_notes={
            "left": "Active Switch Test calls matrix 63 LEFT END OF STROKE; that ROM label does not change the host-button transport.",
            "right": "Active Switch Test calls matrix 64 RIGHT END OF STROKE; that ROM label does not change the host-button transport.",
        },
        unused_notes={88: "Upper staged control is a host cvpmFlips2 callback, not a ROM switch at 88 or EOS synthesis."},
        unused_note_refs=(VBS, CORE_VBS, VPW),
    ))
    records.append({
        "id": "dip.country-w7", "label": "Country jumper W7", "kind": "dip_switch",
        "availability": "used", "binding": {"group": "pinmame.input.dip", "device": 0},
        "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
        "spatial": na("dip_switch", PIN),
        "physical": {"switch_type": "dip", "notes": "pia2a_r reads core_getDip(0)<<7; game uses shared DE input ports."},
        "provenance": prov(PIN),
    })
    return records


def coil_wiring(row: tuple) -> dict:
    _, _, transistor, board, wire, pin, power, power_pin, volts, _ = row
    return {"board": board, "driver_transistor": transistor, "control_wire": wire,
            "control_connection": pin, "power_wire": power, "power_connection": power_pin,
            "nominal_voltage_v": 50 if "50" in volts else 32, "voltage_type": "dc"}


def outputs() -> list:
    records = []
    chart = {row[0]: row for row in COIL_CHART}
    anchors = {2: "BallRelease", 3: "sw16", 4: "sw37", 5: "sw39", 6: "sw38",
               7: "TrapDoor", 9: "SW35", 12: "SW34", 14: "sw24",
               17: "Bumper1", 18: "Bumper2", 19: "Bumper3",
               20: "LeftSlingShot", 21: "RightSlingShot", 22: "LeftSlingShotH"}
    for address in range(1, 65):
        row = chart.get(f"{address}L" if address <= 8 else f"{address:02d}")
        if row and row[1] != "Not Used":
            kind = "relay" if address in {10, 11} else "coil"
            d = device("pinmame.output.solenoid", address, row[1], kind, "used", MANUAL, PIN, VPW)
            d["wiring"] = coil_wiring(row)
            d["physical"] = {"part_number": row[-1], "quantity": 1,
                             "notes": "Full factory driver table is retained in coil-chart.md."}
            if address == 7:
                d["wiring"]["control_connection"] = "PPB J2-7"
                d["physical"]["notes"] += " Table prints J2-8; printed page 38 schematic proves J2-7 (J2-8 is knocker)."
            if address == 10:
                d["wiring"]["control_connection"] = "CPU CN12-2"
                d["physical"]["notes"] += " Table duplicates CN12-5 from driver 12; schematic proves CN12-2 for the relay."
            if address == 5:
                d["physical"]["part_number"] = "25-1240"
                d["physical"]["assembly_part_number"] = "500-5839-00"
                d["physical"]["notes"] += " Printed page 37 says 23-800; wiring diagram and VUK BOM item 7 both specify 25-1240."
            if address in anchors:
                d["spatial"] = spatial(d["id"], "effect", anchors[address])
                d["physical"]["notes"] += " Placement projects the coil's effect onto its mechanism, not a winding-center measurement."
            elif address in {8, 10, 11}:
                d["spatial"] = na("cabinet_or_service", MANUAL)
            if address == 11:
                d["physical"]["notes"] += (
                    " Physical relay on power supply; public state is modeled as reversed #44 "
                    "6.3VAC brightness by PinMAME. No separate GI channel. Asserted binary "
                    "11 switches GI off in the scripts; deasserted restores it. Actual PF "
                    "GI sockets must be mapped separately from this internal relay.")
        elif 25 <= address <= 32:
            row = chart[f"{address-24}R"]
            d = device("pinmame.output.solenoid", address, row[1], "flasher", "used", MANUAL, PIN, VPW)
            d["wiring"] = coil_wiring(row)
            pf = 1 if address in {29, 30} else 2
            other_region = "rear playfield back-panel" if address == 25 else "backbox insert"
            d["physical"] = {"part_number": "#89", "quantity": 4,
                             "location": "playfield and rear playfield back panel" if address == 25
                                         else "playfield and backbox insert",
                             "notes": f"Factory bank {address-24}R: {pf} playfield bulbs, {4-pf} {other_region} bulbs. "
                             "The stock list's aggregate count is not a bank socket map. "
                             "No glow, reflection, Flasher sprite, or shared visual proxy is promoted to a socket."}
            if address == 25:
                d["physical"]["notes"] += (
                    " PDF 41 / printed page 37 distinguishes Backpanel from Insert. "
                    "PDF 40 / printed page 36 places the two back-panel bulbs at the "
                    "rear playfield corners and lists only 2R-8R in the Backbox Flash Lamps drawing.")
            if address == 28:
                d["physical"]["notes"] += (
                    " Table calls this captive-ball flash; location drawing labels 4R Turbo "
                    "Bumpers X2. Preserve both names: an illuminated target is not necessarily "
                    "the bulb location. The diagram establishes bumper-area placement.")
        else:
            meaningful = address in {23, 37, 38, 39, 45, 46, 47, 48}
            names = {
                23: "Game-on / flipper enable", 24: "Unimplemented S11 bit 24",
                33: "Unimplemented upper-right power alias", 34: "Unimplemented upper-right hold alias",
                35: "Unimplemented upper-left power alias", 36: "Upper-left callback key (dead PinMAME output)",
                37: "Raw printer bit 0 / left magnet alias", 38: "Raw printer bit 1 / center magnet alias",
                39: "Raw printer bit 2 / right magnet alias",
                45: "Synthetic lower-right power state", 46: "Synthetic lower-right combined state",
                47: "Synthetic lower-left power state", 48: "Synthetic lower-left combined state",
                49: "Shared simulator shooter-release signal", 50: "Reserved pre-custom gap",
            }
            label = names.get(address, f"Unused output {address}")
            if 40 <= address <= 44:
                label = f"Unconnected printer bit {address-37}"
            d = device("pinmame.output.solenoid", address, label, "virtual",
                       "used" if meaningful else "unused", PIN)
            d["spatial"] = na("virtual", PIN)
            d["physical"] = {"notes": (
                "Public compatibility namespace, not a fitted winding. GnR publishes "
                "53 solenoids; custom 54-64 return zero. Shared core has no Data East "
                "upper 33-36 return; 50 is a gap. Matrix/PIA writers never set bit 24. "
                "Factory chart explicitly leaves 13,15,16 unfitted.")}
            if 40 <= address <= 44:
                d["physical"]["notes"] = (
                    f"Raw printer-line transport bit {address-37}; the magnet board has "
                    "only three output transistors. Addendum schematic grounds unused "
                    "latch inputs 4-8. This enumerated unused physical channel is not "
                    "a fourth magnet or a fitted coil; byte readback remains a transport detail.")
                d["provenance"] = prov(PIN, ADDENDUM)
            if 45 <= address <= 48:
                d["physical"]["notes"] = (
                    "core_updateSw fabricates button-derived lower-flipper states when 23 "
                    "enables the game; 46/48 combine power-or-hold. These have no "
                    "independent physical quantity and are not four fitted coils.")
                d["provenance"] = prov(PIN, RUNTIME)
            if address == 36:
                d["physical"]["notes"] = (
                    "Legacy ID retained, but not a live CPU coil. VPW assigns its upper "
                    "callback to 36; cvpmFlips2 captures it and directly calls it from "
                    "the staged cabinet key while 23 permits flippers. It need not "
                    "observe a nonexistent ROM output 36.")
                d["provenance"] = prov(PIN, VPW, VBS, MANUAL)
            if address == 49:
                d["physical"]["notes"] = (
                    "Shared core reserves simulated manual-shooter release at 49. GnR has "
                    "no simData and therefore never publishes meaningful shooter state "
                    "here in a fresh run. This unused compatibility alias is separate "
                    "from the physical rose plunger.")
            if address in {51, 52, 53}:
                side, obj, physical_number, out_pin, data_pin, wire = {
                    51: ("Left", "leftMagnet", 2, 4, 6, "BLU-GRY"),
                    52: ("Center", "CenterMagnet", 1, 3, 7, "BLU-VIO"),
                    53: ("Right", "RightMagnet", 3, 7, 8, "BLU-WHT"),
                }[address]
                d["kind"] = "magnet"; d["label"] = f"{side} playfield magnet"; d["availability"] = "used"
                d["provenance"] = prov(PIN, ADDENDUM, MANUAL, VPW, SCRIPT, RUNTIME)
                d["spatial"] = spatial(d["id"], "effect", obj)
                d["wiring"] = {
                    "board": "Magnet Board 520-5068-00", "control_wire": wire,
                    "control_connection": f"J2-{out_pin}",
                    "driver_transistor": f"Q{physical_number}",
                    "power_wire": "VIO-YEL", "power_connection": "J2-1 / PPB J7-3",
                    "nominal_voltage_v": 50, "voltage_type": "dc",
                }
                d["physical"] = {"quantity": 1, "notes": (
                    f"Addendum magnet {physical_number}, latch input J1-{data_pin}, "
                    f"public raw {address-14} mirrored by custom {address}. "
                    "The factory input permutation, not stale generic s11.c comments, "
                    "settles the board number; exact script settles left/center/right. "
                    "16 in cvpmMagnet is force-radius tuning, not physical coil radius.")}
        records.append(d)
    for address, label in enumerate(LAMP_NAMES, 1):
        d = device("pinmame.output.lamp", address, label, "lamp", "used", MANUAL, PIN, VPW)
        col, row = divmod(address - 1, 8)
        wire, pin, transistor = LAMP_COLUMNS[col]; ret, ret_pin, ret_q = LAMP_ROWS[row]
        d["wiring"] = {"board": "CPU", "drive_wire": wire, "drive_connection": pin,
                       "driver_transistor": transistor, "return_wire": ret,
                       "return_connection": ret_pin, "return_component": ret_q}
        d["physical"] = {"quantity": 2 if address == 55 else 1,
                         "notes": "Full factory matrix and bulb-location drawing determine name and fitment."}
        if address < 63:
            d["spatial"] = spatial(d["id"], "emitter", f"l{address}",
                                   *(["l55a"] if address == 55 else []))
            d["physical"]["notes"] += (
                " Named Light center is cross-checked against the factory insert/socket "
                "symbol. An insert overlay is not counted as an extra bulb.")
            if address in {2, 3}:
                d["physical"]["notes"] += (
                    " This older table incorrectly gives l2/l3 TimerInterval=18; their "
                    "ROCK insert positions are established by the factory drawing. "
                    "That local runtime bug does not redefine factory lamp 2 or 3.")
            if address == 55:
                d["physical"]["notes"] += " Factory shows two 55 locations (left shooter and left ramp); retained l55/l55a are distinct bulbs."
        else:
            d["spatial"] = na("cabinet_or_service", MANUAL)
        records.append(d)
    return records


def mechanisms(ins: list, outs: list) -> list:
    sw = {d["binding"]["device"]: d["id"] for d in ins if d["binding"]["group"] == "pinmame.input.switch"}
    sol = {d["binding"]["device"]: d["id"] for d in outs if d["binding"]["group"] == "pinmame.output.solenoid"}
    rows = [
        ("trough", "Six-ball trough and lockout", "kicker", [1, 2], list(range(9, 16)), "500-5683-01",
         "Six active balls rest on 9-14; 15 is the seventh/right staging contact. "
         "Lock-ball assembly 500-5684-01 and trough are separate cooperating assemblies. "
         "Driver 1 operates the 25-1240 lockout linkage; driver 2 ejects with 23-800 "
         "toward shooter 16. VPW initializes 9-14 active, shifts its six kicker objects "
         "on a 300 ms timer, asserts 15 after SolTrough and clears it after SolRelease. "
         "Those local kicks are a surrogate, not proof of physical coil timing. "
         "Unexpected occupancy invokes ball search / missing-ball diagnostics."),
        ("auto-launch", "Gun trigger and right auto launch", "kicker", [3], [15, 16, 62], "500-5477-03",
         "Spring-return 22-600 striker auto launches the right shooter lane when the gun "
         "microswitch 62 requests launch. Gun 500-5834-00 has a trigger spring and no "
         "separate solenoid. The rose plunger is physically separate. SB63 addresses "
         "electrical launch failures: failed climbs can accumulate balls and overheat "
         "the coil. It describes a 3.00 watchdog disabling auto launch on repeated "
         "shooter-switch closures. SB64 lowers the rear ramp mount approximately "
         "half an inch and advances its entrance in the routed slots."),
        ("rose-plunger", "Left rose handle manual shooter", "other", [], [24], "500-5836-01-02",
         "Manual long-shaft spring plunger returns from pulled to released, propelling "
         "the left shooter lane. No CPU coil drives the rose handle. VPW shares a host "
         "plunger key with gun trigger, and permits rose pull/fire only when no ball "
         "is in the right shooter; do not merge those two physical controls."),
        ("eject", "Upper-left ball eject", "kicker", [4], [37], "500-5664-01",
         "24-940 coil pulls a plunger/link and pivots an eject cam; spring restores it. "
         "Switch 37 reports an occupied cup. Driver 4 ejects, validated in the ROM kick "
         "test. Legacy upper-left VUK ID stays stable although the factory calls it Eject."),
        ("vuk", "Upper-right vertical up-kicker", "kicker", [5], [39], "500-5839-00",
         "25-1240 vertical striker lifts the captured ball into the upper wireform; "
         "39 detects occupancy. Spring restores the plunger. Driver 5 fires in ROM "
         "kick test. VPW destroys/creates a ball on the wireform as a simulation technique."),
        ("scoop", "Center power scoop and Kick Big", "kicker", [6], [38], "500-5809-00",
         "Power scoop and 500-5740-00 Kick Big are separate assemblies working together. "
         "38 is the scoop microswitch, driver 6 is a 50V 23-800 striker. VPW can retain "
         "up to three balls before kicking; destroy/create and timer logic implement "
         "a virtual stack, not additional sensors. ROM kick test confirms 38 to 6."),
        ("trap-door", "G-ramp trap door and snake-pit route", "diverter", [7], [40, 51, 52], "500-5830-00",
         "28-1050 plunger, linkage pin and flap control a hole in the G ramp. VPW starts "
         "SolTrapDoor 0 closed; assertion opens the drop route and release restores "
         "the ramp route. The ramp enter/exit and funnel switches detect balls, not "
         "door position. No home/limit sensor is fitted in the complete switch chart."),
        ("right-drop-bank", "Right three-drop bank", "drop_target_bank", [9], [36, 35, 57], "500-5621-03",
         "Each target latches down on impact and closes its own switch; one 23-800 "
         "reset lifts all three. Bottom/middle/top are 36/35/57, not numeric order. "
         "Script holds closure until bank reset; stock BOM on page 61 includes unused "
         "2/4-bank options that do not make this game a larger bank."),
        ("left-drop-bank", "Left three-drop bank", "drop_target_bank", [12], [33, 34, 59], "500-5621-03",
         "Each target latches down; one 23-800 reset lifts the whole bank. "
         "Bottom/middle/top 33/34/59. The exact scripts reset through driver 12."),
        ("laser-kick", "Left outlane Laser Kick", "kicker", [14], [54], "500-5838-00",
         "A 50V 23-800 striker returns a left-outlane ball to play; spring restores it. "
         "Outlane closure 54 fires 14 in the dedicated ROM test after game-on 23 "
         "enables outputs. It is distinct from manual shooter 24, though the retained "
         "table kicks its left-lane plunger for the effect."),
        ("captive-ball", "Captive DUFF ball and four standups", "toy", [], [17, 18, 19, 20], None,
         "One captive ball strikes four DUFF standups; six other balls circulate. "
         "D/U/F/F are four distinct contacts, not duplicates. The historical prototype "
         "rest-rollover, mini-loop sensor and extra Time To Rock standup were removed "
         "before production and are not silently populated into unused addresses."),
        ("magnets", "Three center-playfield electromagnets", "other", [51, 52, 53], [], "520-5068-00",
         "Three separately switched magnetic fields disturb rolling balls; no position "
         "marks, limit contacts or fourth magnet. Board Q1/Q2/Q3 map to center/left/right "
         "via the factory latch permutation and exact script. Hold Start in Magnet Test "
         "to cycle all three. They begin deenergized; GrabCenter=False means no scripted "
         "ball pinning. SB63 states that 3.00 turns the magnets off in multiball when "
         "a 50 V coil fires, reducing shared supply loading; the service-test traces "
         "do not independently exercise that gameplay condition. The 16 force radius "
         "is table tuning, not a factory measurement."),
        ("lower-left-flipper", "Lower-left flipper", "other", [48], [84, 63], "500-5755-02",
         "Cabinet-wired SSFB coil 22-1080: timed 50V actuation, 8VAC-derived holding "
         "power, spring return. Normally-closed physical EOS can retrigger power on "
         "knockback; it has no GnR ROM-readable address. Output 23 enables the host "
         "flipper controller; 47/48 are synthetic states, not additional physical coils."),
        ("lower-right-flipper", "Lower-right flipper", "other", [46], [82, 64], "500-5755-01",
         "Same SSFB timed power/hold topology with a right cabinet button. Host 82 "
         "copies to matrix 64 and fabricates 45/46 while 23 is enabled. Lower physical "
         "EOS belongs to the SSFB circuit and is not host 81."),
        ("upper-left-flipper", "Staged upper-left flipper", "other", [], [], "500-5694-02",
         "Third physical flipper, driven directly by a staged cabinet contact through "
         "SSFB channel C. No upper EOS in the factory flipper chart. VPW cvpmFlips2 "
         "captures the callback keyed by 36 and invokes it from the host staged input; "
         "core cannot publish 36. Factory chart 25-1100 conflicts with assembly 23-1100; "
         "retain that unresolved part difference and do not invent an active ROM coil."),
    ]
    result = []
    for key, label, kind, actuators, sensors, assembly, behavior in rows:
        m = {"id": f"mechanism.{key}", "label": label, "kind": kind,
             "actuators": [sol[n] for n in actuators], "sensors": [sw[n] for n in sensors],
             "behavior": behavior, "provenance": prov(MANUAL, PIN, VPW, SCRIPT)}
        if assembly: m["assembly_part_number"] = assembly
        if key in {"magnets", "laser-kick", "eject", "vuk", "scoop"}:
            m["provenance"] = prov(MANUAL, ADDENDUM, PIN, VPW, RUNTIME)
        if key == "magnets":
            m["provenance"]["source_refs"].append(SB63)
        if key == "auto-launch":
            m["provenance"] = prov(MANUAL, PIN, VPW, SCRIPT, SB63, SB64)
        if "flipper" in key: m["provenance"] = prov(MANUAL, SCHEMATICS, PIN, VPW, VBS)
        if "drop-bank" in key:
            m["positions"] = [
                {"id": f"{m['id']}.{position}", "label": position.title(), "sensors": [sw[n]]}
                for position, n in zip(["bottom", "middle", "top"], sensors)
            ]
        result.append(m)
    for label, sensor, actuator in [
        ("Left turbo bumper", 25, 17), ("Bottom turbo bumper", 26, 18),
        ("Right turbo bumper", 27, 19), ("Left slingshot", 29, 20),
        ("Right slingshot", 28, 21), ("Top slingshot", 30, 22),
    ]:
        result.append({"id": f"mechanism.special-{actuator}", "label": label, "kind": "kicker",
                       "actuators": [sol[actuator]], "sensors": [sw[sensor]],
                       "assembly_part_number": "500-5227-00" if actuator < 20 else
                                               "500-5226-01" if actuator == 22 else "500-5226-00",
                       "behavior": (
                           "Ball impact tilts the skirt and closes the leaf contact; the ROM "
                           "drives the 23-800 coil, pulling the plunger/yoke and rod/ring "
                           "down to repel the ball. The spring restores the resting ring. "
                           if actuator < 20 else
                           "Two leaf contacts detect rubber deflection through one matrix "
                           "circuit. The ROM drives the 23-800 coil; its plunger/link pivots "
                           "the arm and tip into the rubber to repel the ball, and the spring "
                           "restores the resting arm. The top assembly rotates the coil 90 degrees. "
                       ) + "GnR has no ssSw array; do not add host autofire bypasses.",
                       "provenance": prov(MANUAL, PIN, VPW)})
    result.append({"id": "mechanism.knocker", "label": "Cabinet knocker", "kind": "other",
                   "actuators": [sol[8]], "sensors": [], "assembly_part_number": "500-5081-00",
                   "behavior": "23-800 striker hits the cabinet stop and spring returns; "
                   "no position sensor or playfield emitter.",
                   "provenance": prov(MANUAL, VPW)})
    return result


def table_text(title: str, headers: list, rows: list) -> str:
    return (f"# {title}\n\nVisually checked against the factory PDF by primary Sol curator "
            "(2026-09-30). Literal full table region; zero-population and Not Used rows "
            "are retained. OCR was navigation only.\n\n"
            + "| " + " | ".join(headers) + " |\n"
            + "| " + " | ".join(["---"] * len(headers)) + " |\n"
            + "".join("| " + " | ".join(str(x) for x in row) + " |\n" for row in rows))


def transcriptions() -> dict[str, str]:
    switch_rows = []
    lamp_rows = []
    for n in range(1, 65):
        col, row = divmod(n-1, 8)
        switch_rows.append((n, SWITCH_NAMES[n-1], SWITCH_PARTS[n-1], col+1, row+1,
                            *SWITCH_COLUMNS[col], *SWITCH_ROWS[row]))
        lamp_rows.append((n, LAMP_NAMES[n-1], col+1, row+1,
                          *LAMP_COLUMNS[col], *LAMP_ROWS[row]))
    result = {
        "switch-chart.md": table_text(
            "Switch matrix and parts: printed pages 32-33 / PDF 36-37",
            ["Address", "Name", "Part", "Column", "Row", "Drive", "Drive pin", "Transistor",
             "Return", "Return pin"], switch_rows),
        "lamp-chart.md": table_text(
            "Lamp matrix: printed pages 34-35 / PDF 38-39",
            ["Address", "Name", "Column", "Row", "Drive", "Drive pin", "Transistor",
             "Return", "Return pin", "Return transistor"], lamp_rows),
        "coil-chart.md": table_text(
            "Full solenoid/flash table: printed page 37 / PDF 41",
            ["No", "Name", "D.T.", "Board", "Control wire", "Control connection",
             "Power wire", "Power connection", "Voltage", "Coil / bulb"], list(COIL_CHART))
        + "\n" + table_text(
            "Full flipper-solenoid table: printed page 37 / PDF 41",
            ["Flipper", "Coil", "Cabinet", "SW drive", "SW return", "EOS", "Ground",
             "Power input", "Holding input", "Outputs", "Coil wires"], list(FLIPPER_CHART)),
    }
    result["assembly-tables.md"] = (
        "# Complete checked stock and assembly regions\n\nSource: original main manual; "
        "PDF page number precedes each region. Visually checked by primary Sol "
        "curator, 2026-09-30. Repeated item numbers and generic alternate parts are "
        "retained; do not infer fitment from a generic BOM alone.\n\n"
        + "\n\n".join(f"## PDF {page} / printed {page-4}\n\n```text\n{text}\n```"
                      for page, text in sorted(ASSEMBLY_TABLES.items())) + "\n")
    result["factory-corrections.md"] = """# Factory diagrams and corrections

Main manual PDF 40 / printed page 36: full coil/flash table and location drawing.
1L 6-Ball Ass'y Lockout; 1R Back Panel X2 LT/RT Crnr.
2L Ball Release (Eject); 2R Right Playfield.
3L Auto Ball Launch 50V; 3R Left Playfield.
4L Kicker Eject; 4R Turbo Bumpers X2.
5L VUK 50V; 5R "R" Ramp Enter.
6L Scoop/Kick Big 50V; 6R "G" Ramp.
7L Ramp Coil Trap Door; 7R Under "R" Ramp.
8L Knocker32V; 8R Under "G" Ramp.
09 Right3-Bank Drop Targets; 10 Left/Right(A/B)Relay; 11 G.I.Relay;
12 Left3-Bank Drop Targets; 13 NotUsed;14 LaserKick50V;15 NotUsed;16 NotUsed;
17 LeftTurboBumper;18 BottomTurboBumper;19 RightTurboBumper;
20 LeftSlingshot;21 RightSlingshot;22 TopSlingshot.
Shaded entries 10/11/13/15/16 are not drawn as playfield devices.

Main manual PDF 42 / printed page 38 diagram: 7L VIO-BLK PPB J2-7 (table misprints
J2-8); 8L VIO-GRY J2-8. Mux relay 10 BLK-RED CPU CN12-2 (table
misprints CN12-5, which belongs to 12). VUK coil is 25-1240 (table says 23-800);
PDF 63 / printed page 59 BOM independently confirms 25-1240, 090-5034-01.
Each of 1R-8R has four #89 bulbs. PDF 41 / printed page 37 specifies
two playfield bulbs and two back-panel bulbs for 1R. PDF 40 / printed page 36
places the back-panel pair at the rear playfield corners; its Backbox Flash Lamps
drawing contains only 2R-8R. The remaining playfield/backbox insert splits are:
2R 2/2; 3R 2/2; 4R 2/2; 5R 1/3; 6R 1/3; 7R 2/2; 8R 2/2.
The 32 bulbs total 14 playfield, 16 backbox insert and 2 rear playfield back-panel bulbs.
The backbox insert bulbs are not playfield sockets.

PDF 39 / printed page 35 explicitly excludes GI from the switched-lamp drawing.
It shows two 55 bulbs (left-shooter and left-ramp) and cabinet 63/64.
PDF 37 / printed page 33 draws 28/29 on opposite slings from its own table; the
matrix, parts rows and exact scripts establish 28 right and 29 left.
Upper flipper PDF 41 / printed page 37 says 25-1100; PDF 57 / printed page 53
assembly 500-5694-02 says 23-1100, 090-5030-00. This part conflict remains open.
Gun 62 parts row says 180-5093-00; gun assembly PDF 70 lists 180-5143-00.
PDF 58 gives two 180-5054-00 leaf switches per lower or upper slingshot;
one matrix number represents the assembly, not one fitted physical contact.
PDF 52-53 lamp/socket stock counts are retained in full, including shaded
zero rows and positive-quantity #906 rows. They do not assign every bulb to
a matrix address, GI feed or flasher bank; no GI count is derived by subtraction.

Factory Service Bulletin 63, October 4, 1994, PDF 1: failed auto launch can
accumulate balls, overheat the 22-600 coil and blow PPB F5 (5A slow-blow),
disabling the 50V loads including flippers. It specifies 090-5023-01, a
centered white nylon flat-tipped plunger and the improved chrome ramp.
The cabinet already provides the printed 6.5% pitch with leg levelers fully
inserted. Published 3.00 changes: repeated shooter-switch closures after
failed ramp climbs disable auto launch; multiball 50V coil firing turns
magnets off to reduce shared-supply load. This is an official firmware
description, not an independently exercised gameplay observation.
Factory Service Bulletin 64, November 1, 1994, PDF 1: lower the rear shooter
ramp mount about half an inch and advance its entrance in the routed slots
to reduce climb pitch. Its second page illustrates the modification; no
unmeasured geometry is transferred to normalized playfield positions.

July 18, 1994 Addendum No. 2, 780-5029-51, PDF 1: hold Start in Magnet Test
to rapidly cycle three center-playfield magnets. Laser Kick Test responds
to left-outlane ball placement and also supports eject and VUK tests.
Addendum PDF 2 complete connector block (KEY means no conductor):

| Magnet board520-5068-00 | Net / wire | Other endpoint |
| --- | --- | --- |
| J1-9 | CLOCK BRN-WHT | CPU CN1-7 |
| J1-8 | INPUT3 ORG-BLK | CPU CN3-7 |
| J1-7 | INPUT1 ORG-RED | CPU CN3-8 |
| J1-6 | INPUT2 ORG-BRN | CPU CN3-9 |
| J1-5 | CLR GRY-BLK | CPU CN2-1 |
| J1-4 | +5V GRY | PS CN6-7 |
| J1-3 | KEY | none |
| J1-2 | GND BLK | PS CN4 |
| J1-1 | GND BLK | PS CN4 |
| J2-1 | +50V VIO-YEL | PPB J7-3 |
| J2-2 | KEY | none |
| J2-3 | OUTPUT1 BLU-VIO | MAGNET1 |
| J2-4 | OUTPUT2 BLU-GRY | MAGNET2 |
| J2-5 | GND BLK | PS CN4 |
| J2-6 | GND BLK | PS CN4 |
| J2-7 | OUTPUT3 BLU-WHT | MAGNET3 |

Addendum PDF 3: 74HCT273 latch drives Q1/Q2/Q3 P20N10 and diode D1/D2/D3
1N4934; unused latch inputs 4-8 are grounded. Combining the explicit CPU
pin permutation with s11.c pia2b_w: raw 37=Magnet2, 38=Magnet1, 39=Magnet3.
Both exact scripts identify public 51/52/53 left/center/right. Generic source
comments' Magnet3/2/1 nomenclature is not the factory board numbering.

Paginated schematics PDF 43, theory of operation: the SSFB uses a timed
50 V actuation stage and an 8 V holding stage. The normally-closed EOS is
an optional knockback retrigger, not required for ordinary operation.
PDF 44-45 connector labels: CN1-12 Flipper SwitchC;CN1-11 SwitchB;
CN1-10 ReturnC;CN1-9 EOSB;CN1-8 +5V;CN1-7 SwitchA;CN1-6 GND;
CN1-5 ReturnB;CN1-4 SwitchDrive;CN1-3 ReturnA;CN1-2 KEY;CN1-1 EOSA.
CN2-1/2 CoilC;CN2-3 unused;CN2-4/5 CoilB;CN2-6 KEY;
CN2-7/8 CoilA;CN2-9/10 8VAC;CN2-11/12 +50VDC.
The printed flipper table's power connector cells disagree with these
schematic labels; no unverified power-pin cell is promoted onto a virtual alias.

Transcription method: visually checked native-DPI full-page PDF renders,
primary Sol curator, 2026-09-30; candidate OCR used only to find regions.
"""
    result["transport-and-runtime.md"] = """# Exact runtime and transport contract

Pinned PinMAME 8371478a7640f1896dcdf565aed340dc5df989ba:
degames.c lines 1269-1320 declares three GnR 3.00 drivers, shared gnrGameData,
GEN_DEDMD32, de_128x32DMD, FLIP6364, three custom solenoids,
zero extra switch/lamp columns, zero inverse array, S11_PRINTERLINE, mux 10.
core.h lines 300-330: extension 37, custom 51; gnr_getSol 51/52/53 returns 37/38/39.
s11.c lines 392-410: printer byte is noninverted; lines 205-220 publish it.
s11.c lines 558-584: mux 10 routes 1-8 to 25-32.
s11.c lines 618-625: Data East special order:
pia1ca2->20, pia1cb2->21, pia3ca2->22, pia3cb2->18, pia4ca2->17, pia4cb2->19.
s11.c lines 628-650: eight-bit switch strobe, uncomplemented core_getSwCol.
s11.c lines 1188-1196: 11 reversed #44 6.3 VAC; 25-32 #89 32 VDC.
core.c lines 1700-1753: 82->64, 84->63; game-on 23 gates synthetic 45-48.
core.c lines 2182-2224: 33-36 dead for Data East, 37-44 raw extension, 49 simulator,
50 gap, 51-53 custom; greater custom returns 0. No upper ROM coil 36.

Exact retained Team PP embedded script sha256
d42debb0e6c30e4498e6ed77ac475a04141a799448c7fcbfff26f3a247b376a9:
script.vbs line 95 cGameName=gnr_300; lines 170-250 trough/scoop/eject/VUK/magnets;
269 vpmMapLights AllLamps; 436-438 and 585-587 drop switches;
770-845 slings 28 right, 29 left, 30 top; 914-1020 matrix Hit/UnHit;
1044-1093 kickers; 1264-1334 solenoid callbacks/trap;
1346-1499 glow/flasher routines; 1505-1545 reversed GI.
Not exact-match to any pinned corpus script. Three Flipper objects exist;
LeftFlipper1 is the upper-left pivot and the old script moves it with the lower-left.

Pinned VPW 1.2.1 sha256
a0b37bbd036726345d89483c76e2afebec994abcc395d646b85ac79770eefe1e:
vpxtable_scripts revision 0c036bb61b4b4e8c778c37559f6795df8cd1521e;
script lines 39-40 ROM; 514-586 initialization with six trough balls, captive seventh,
magnets 51 left, 52 center, 53 right; 663-715 callbacks; 722-767 trough;
1263-1407 kickers/trap; staged cabinet flipper callbacks.
de.vbs and core.vbs cvpmFlips2.Init, lines 2094-2150, capture callbacks;
Flip/FlipUL call upper code directly while TiltSol/game-on 23 enables it.
de.vbs sha256 8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04;
core.vbs sha256 a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69.

The committed scenario and bounded DMD-header adapter use named service
keys and exact retained top-ten-row templates. After the transient test
header, wait_until_output for 23 proves readiness before switch stimulus.
Fresh run magnet-laser-v2-state: US 3.00, boot 8 seconds, empty CMOS.
Expected causal results: holding Start cycles 37=51, 38=52, 39=53;
54 pulse->14, 37->4, 39->5, 38->6. Host left/right buttons produce 47/48 and 45/46.
Complete raw run, snapshots, ROM archive hashes, DLL identity and manifest
remain external. Compact checked observations are in runtime-summary.md.
Host switch readback alone is not evidence of ROM behavior.
"""
    result["geometry.md"] = (
        "# Exact retained geometry\n\nSelected Team PP original sha256 "
        "4e54ffbde40cc949256252244745c92e75ef00c6a498150b3d4eecb4fb52d71b. "
        "Full vpxtool git:v0.33.3 extraction: 1204 files, 117209740 bytes. "
        "Canonical manifest: 57014dfc9904bf08aa9e9e33a9e4bffd6b2d38983efe302519f753bb24e22eaa. "
        "Manifest algorithm: every relative POSIX path sorted, byte size and full-file "
        "SHA256; UTF8 compact JSON array sorted keys, no final newline.\n\n"
        "Bounds left 0, top 0, right 1000, bottom 1902. "
        "x=raw_x/1000; y=raw_y/1902; six-decimal rounding. Wall contact regions use "
        "signed shoelace area centroid, not the enclosing decoration. Exact "
        "JSON paths, item ordinals, raw coordinates, methods and hashes are in "
        "tools/guns_n_roses_geometry.json. No primitive or Flasher sprite is eligible.\n\n"
        "Manual control points: bumper 25 left/Bumper1, 26 bottom/Bumper2, 27 right/Bumper3; "
        "lamps 57/58/59 over JAM, central GUNS/ROSES insert rings, 55 left shooter and "
        "55 upper ramp; switches 37/39 left/right rear cups. Manual callout leaders "
        "are identity cross-checks, not pixel socket measurements. Three Flipper "
        "objects exist; LeftFlipper1 (120.20107, 797.88635) is the upper-left pivot. "
        "The older script ties it to the lower-left; VPW supplies staged semantics. "
        "Four unique local candidates are retained; selected manifest remains exact.\n")
    result["transport-and-runtime.md"] += "\nExact pinned transport files (full-file SHA256):\n\n"
    for name, digest, locator in PIN_FILES:
        result["transport-and-runtime.md"] += f"- src/wpc/{name}: `{digest}`; lines {locator}.\n"
    for stem, title, filename in [
        ("runtime-summary", "Checked runtime transitions", "guns_n_roses_runtime.json"),
        ("active-switches", "Visually checked Active Switch Test screenshots", "guns_n_roses_active_switches.json"),
        ("runtime-provenance", "Exact runtime provenance and external manifest", "guns_n_roses_runtime_provenance.json"),
        ("manual-provenance", "Retained document identities and acquisition URLs", "guns_n_roses_manual_provenance.json"),
    ]:
        payload = canonical_bytes(load_json(ROOT / "tools" / filename)).decode()
        result[f"{stem}.md"] = f"# {title}\n\n```json\n{payload}```\n"
    return result


def excerpt(name: str, locator: str, text: str) -> dict:
    return {"id": "excerpt.guns-n-roses."+name.removesuffix(".md"), "locator": locator,
            "path": f"{EXCERPTS}/{name}", "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "method": "manual",
            "transcribed_by": "primary Sol curator, 2026-09-30", "reviewed": True}


IMAGES = {
    "switch-chart.md": ("switch-locations", "138e8b746068f233275630be61b6405ecf6a2be57e07aa774c6d16416c549ba2",
        "Data_East_1994_Guns_N_Roses_Manual.pdf page 37, crop box 0.11,0.28,0.5,0.88, scanned page rendered at its native resolution (embedded image xref 252, 1700px across 8.50in), rendered at 200 dpi, grayscale, 663x1320 WebP quality 80"),
    "lamp-chart.md": ("lamp-locations", "7d7b8aad1bc249b24f278dc6994939e49b7e1c6bfb646bae0e0a58c9ac573dfe",
        "Data_East_1994_Guns_N_Roses_Manual.pdf page 39, crop box 0.05,0.38,0.83,0.95, scanned page rendered at its native resolution (embedded image xref 266, 1700px across 8.50in), rendered at 196 dpi, capped to 1300px wide, grayscale, 1301x1231 WebP quality 80"),
    "coil-chart.md": ("coil-locations", "f5975deb95facd28e8696554179bb5e4262be4f5d2244499aa8e53faaf79573e",
        "Data_East_1994_Guns_N_Roses_Manual.pdf page 40, crop box 0.52,0.31,0.9,0.93, scanned page rendered at its native resolution (embedded image xref 273, 1700px across 8.50in), rendered at 200 dpi, grayscale, 646x1364 WebP quality 80"),
}


def sources(texts: dict) -> list:
    def ex(name: str, locator: str) -> dict:
        e = excerpt(name, locator, texts[name])
        if name in IMAGES:
            stem, digest, derivation = IMAGES[name]
            e.update(image=f"{EXCERPTS}/{stem}.webp", image_sha256=digest,
                     image_derivation=derivation)
        return e
    def source(identifier: str, kind: str, uri: str, digest: str, locator: str,
               excerpts: list, attribution: str, **extra) -> dict:
        acquisition = next((r for r in MANUAL_ACQUISITIONS if r["sha256"] == digest), None)
        if acquisition:
            extra.update({k:acquisition[k] for k in ("source_id", "original_filename", "acquired_at")})
            excerpts = [*excerpts, ex("manual-provenance.md", "Verified IPDB 1100 machine page, original download URL, acquisition timestamp and digest")]
        return {"id": identifier, "kind": kind, "uri": uri, "sha256": digest,
                "locator": locator, "excerpts": excerpts, "attribution": attribution,
                "rights": "NOASSERTION", "license": "NOASSERTION", **extra}
    result = [
        source(MANUAL, "manual", "external:manuals/by-machine/data-east.guns-n-roses.1994/ipdb/"+MANUAL_FILENAME,
               MANUAL_SHA, "PDF 36-42 / printed pages 32-38; PDF 52-53 stock; PDF 55-70 / printed pages 51-66",
               [ex("switch-chart.md", "PDF 36-37 complete matrix and parts table"),
                ex("lamp-chart.md", "PDF 38-39 complete lamp matrix and locations"),
                ex("coil-chart.md", "PDF 41 complete coil/flasher/flipper tables; PDF 40 drawing"),
                ex("assembly-tables.md", "PDF 52-53 stock tables; PDF 55-63,65,67,70 full relevant BOM regions"),
                ex("factory-corrections.md", "PDF 37,39-42,57,63,70 crosschecks")],
               "Data East Pinball, Inc.", original_filename=MANUAL_FILENAME,
               source_id="IPDB1100", acquired_at="2026-09-30T10:26:56+00:00"),
        source(ASSEMBLY_MANUAL, "manual",
               "external:manuals/by-machine/data-east.guns-n-roses.1994/ipdb/"+MANUAL_FILENAME,
               MANUAL_SHA, "PDF 57 / printed page 53 upper flipper assembly; same document, different claim region",
               [ex("assembly-tables.md", "PDF 57 full upper flipper BOM, item 12 Coil 23-1100")],
               "Data East Pinball, Inc.", source_id="IPDB1100"),
        source(ADDENDUM, "manual",
               "external:manuals/by-machine/data-east.guns-n-roses.1994/ipdb/Data_East_1994_Guns_N_Roses_English_Manual_Addendum_and_Revised_Page_31.pdf",
               "c2295f482dbdcb6d2a1e12fb42b6eb6fd2c5af9becd5e643a596b76e20dc1274",
               "PDF 1-3; July 18, 1994 No. 2, 780-5029-51",
               [ex("factory-corrections.md", "PDF 1 diagnostic revisions; PDF 2 full connector block; PDF 3 magnet schematic")],
               "Data East Pinball, Inc.", source_id="IPDB1100"),
        source(SCHEMATICS, "manual",
               "external:manuals/by-machine/data-east.guns-n-roses.1994/ipdb/Data_East_1994_Guns_N_Roses_Schematics_paginated.pdf",
               "5cc6567b0d56ff1ceb970fab346b4f6f49f22315c59d007eefea35ee6d63b8dd",
               "PDF 43-45 SSFB theory and two halves of connector schematic",
               [ex("factory-corrections.md", "PDF 43-45 SSFB timing/EOS/connector labels")],
               "Data East Pinball, Inc.", source_id="IPDB1100"),
        source(PIN, "pinmame_core",
               "https://github.com/vpinball/pinmame/blob/"+REVISION+"/src/wpc/degames.c",
               "4b0b026de796c07dcddd4753c47859c39c08092a1e87739f85a6b9e12a3af1c1",
               "degames.c lines 1269-1320; GnR driver/game-data declarations and custom mirrors",
               [ex("transport-and-runtime.md", "Pinned source chain, every GnR address band")],
               "PinMAME contributors", revision=REVISION),
        *[source(identifier, "pinmame_core",
                 f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/{name}",
                 digest, f"src/wpc/{name} lines {locator}",
                 [ex("transport-and-runtime.md", f"Exact {name} controller-contract region")],
                 "PinMAME contributors", revision=REVISION)
          for identifier, (name, digest, locator) in zip(PIN_REFS[1:], PIN_FILES)],
        source(TABLE, "vpx_table",
               "external:vpx-sources/data-east/guns-n-roses-1994/tables/team-pp-2019-4e54ffbde40c/Guns and Roses (Data East 1994) Team PP 180 Final 1.08 MB.vpx",
               "4e54ffbde40cc949256252244745c92e75ef00c6a498150b3d4eecb4fb52d71b",
               "complete vpxtool extraction; gamedata.json bounds; gameitems per geometry.json",
               [ex("geometry.md", "Exact extraction manifest and source JSON locators")],
               "Team PP (retained table metadata and embedded script credits)", known_working=True,
               original_filename="Guns and Roses (Data East 1994) Team PP 180 Final 1.08 MB.vpx"),
        source(SCRIPT, "vpx_script", "external:vpx-sources/"+TABLE_SUBDIR+"/script.vbs",
               "d42debb0e6c30e4498e6ed77ac475a04141a799448c7fcbfff26f3a247b376a9",
               "script.vbs lines 95,170-269,436-438,585-587,770-1093,1264-1545",
               [ex("transport-and-runtime.md", "Exact embedded script callbacks/switches, not corpus sidecar")],
               "Team PP; embedded header credits", known_working=True),
        source(VPW, "vpx_script",
               "https://github.com/vpinball/vpxtable_scripts/blob/0c036bb61b4b4e8c778c37559f6795df8cd1521e/Guns%20N%20Roses%20(Data%20East%201994)%20VPW%201.2.1.vbs",
               "a0b37bbd036726345d89483c76e2afebec994abcc395d646b85ac79770eefe1e",
               "lines 39-40,514-586,663-767,1263-1407; staged flipper callbacks",
               [ex("transport-and-runtime.md", "Exact pinned VPW runtime semantics")],
               "VPinWorkshop; Niwak,Sixtoe,HiRez00,iaakki,leojreimroc,TastyWasps,Primetime5k,Hauntfreaks,Apophis,Flupper",
               revision="0c036bb61b4b4e8c778c37559f6795df8cd1521e", known_working=True),
        source(VBS, "vpx_script", "external:pinmame-review-artifacts/vpm-script-libs/de.vbs",
               "8858b4509a600f77a8a5844f138ed1c71f19b023550660efd62e308588e84d04",
               "de.vbs vpmKeyDown/vpmKeyUp and shared input mapping",
               [ex("transport-and-runtime.md", "DE library key transport")],
               "VPinMAME scripting library contributors"),
        source(CORE_VBS, "vpx_script", "external:pinmame-review-artifacts/vpm-script-libs/core.vbs",
               "a228644ec9714e32c5c6764254b151dc3ec9df2c438dd5a7ce9e9f324cc56f69",
               "cvpmFlips2.Init lines 2094-2150, Flip/FlipUL/TiltSol; captured upper callback",
               [ex("transport-and-runtime.md", "Core library staged-flipper control")],
               "VPinMAME scripting library contributors"),
        source(RUNTIME, "runtime_scenario",
               "external:pinmame-review-artifacts/data-east.guns-n-roses.1994/session-20260930/runtime/magnet-laser-v2-run.json",
               "3580db58380b3921102cebca406e924cf2d9dc210dc4f5988ac1cf3394939d0f",
               "complete fresh-state trace; scenario 796cf62b4f327ba351ffc9f40ef785f186ea18567a00b4f7e5760852144505cf",
               [ex("transport-and-runtime.md", "Causal expectations and retained raw-run identity"),
                ex("runtime-summary.md", "Checked complete-run metadata and per-step transitions"),
                ex("runtime-provenance.md", "ROM/DLL/harness/scenario/raw hashes, fresh-state setup, language, command and complete directory manifest")],
               "Primary curator; legally supplied user ROMs", revision=REVISION),
        source(ACTIVE_RUNTIME, "runtime_scenario",
               "external:pinmame-review-artifacts/data-east.guns-n-roses.1994/session-20260930/runtime/active-switch-run.json",
               "1ebefdf46827518e10ae6d098c99c6184877aa336a3c3bb531cae4d7a03d7cd9",
               "Fresh US 3.00 Active Switch Test; distinct header and output 23 readiness; ten held screenshots visually read",
               [ex("active-switches.md", "Raw run and scenario hashes; every held screenshot pixel/PGM hash and displayed label")],
               "Primary curator; legally supplied user ROMs", revision=REVISION),
    ]
    for identifier, needle in [(SB63, "Bulletin_63"), (SB64, "Bulletin_64")]:
        record = next(r for r in MANUAL_ACQUISITIONS if needle in r["original_filename"])
        result.append(source(identifier, "service_bulletin", "external:manuals/"+record["relative_path"],
                             record["sha256"], "PDF 1; factory failure mode, firmware or mounting correction",
                             [ex("factory-corrections.md", "Visually checked factory bulletin factual summary")],
                             record["attribution"]))
    return result


def build() -> dict:
    texts = transcriptions()
    ins = inputs(); outs = outputs()
    sw = {d["binding"]["device"]: d["id"] for d in ins if d["binding"]["group"] == "pinmame.input.switch"}
    sol = {d["binding"]["device"]: d["id"] for d in outs if d["binding"]["group"] == "pinmame.output.solenoid"}
    relationships = [
        {"id": f"relationship.mux-{n}", "kind": "relay_gated",
         "source": sol[10], "destination": sol[n], "provenance": prov(MANUAL, PIN)}
        for n in range(25, 33)
    ]
    relationships.extend(
        {"id": f"relationship.raw-magnet-{n}", "kind": "direct",
         "source": sol[n-14], "destination": sol[n], "provenance": prov(PIN, ADDENDUM, RUNTIME)}
        for n in range(51, 54)
    )
    relationships.extend(flipper_column_relationships(
        flip_swno=(63, 64), matrix_ids=sw, refs=(*PIN_REFS, RUNTIME, ACTIVE_RUNTIME),
    ))
    return {
        "format": "pinmame-machine-definition", "schema_version": 1,
        "machine": {"id": KEY, "name": "Guns N' Roses", "manufacturer": "Data East",
                    "year": 1994, "kind": "physical_pinball", "ipdb_id": 1100,
                    "opdb_id": "GrPKV-MyNoP", "model_number": "500-5529-01",
                    "playfield": {"width":1000,"height":1902,"units":"vpx",
                                  "provenance":prov(TABLE, status="observed")}},
        "controller": {"platform":"pinmame.dataeast","hardware_generation":"0x4000",
                       "inversion_applied_by_emulator":True},
        "drivers": [
            {"id":name,"description":description,"year":"1994","manufacturer":"Data East",
             "flags":0,"physical_compatibility":"identical",
             "variant_notes":notes, **({"clone_of":"gnr_300"} if name!="gnr_300" else {})}
            for name,description,notes in [
                ("gnr_300","Guns N' Roses (3.00)","US 3.00 CPU/DMD; all three variants share gnrGameData, controller transport and production wiring."),
                ("gnr_300f","Guns N' Roses (3.00 French)","French CPU and DMD images differ; sounds, display topology and I/O map match parent. US header templates must not be used to navigate this localized firmware."),
                ("gnr_300d","Guns N' Roses (3.00 Dutch)","Dutch CPU differs; DMD contents SHA1 match US under another filename; shared sounds and physical I/O. Local archive is merged and needs parent.")]],
        "inputs":ins,"outputs":outs,
        "displays":[{"id":"display.dmd","label":"128x32 dot matrix","kind":"dmd",
                     "controller_index":0,"width":128,"height":32,
                     "spatial":na("cabinet_or_service",PIN,MANUAL),
                     "provenance":prov(PIN,MANUAL,RUNTIME)}],
        "mechanisms":mechanisms(ins,outs),"relationships":relationships,
        "sources":sources(texts),
        "knowledge":{"path":f"knowledge/{STEM}.md","status":"complete"},
        "coverage":{"status":"partial",
                    "missing":["spatial_placement","unresolved_conflicts","output_semantics"],
                    "dimensions":{"catalog_identity":"validated","address_enumeration":"validated",
                                  "semantic_naming":"validated","physical_wiring":"observed",
                                  "mechanisms":"validated","variant_coverage":"validated",
                                  "recreation_knowledge":"validated","spatial_placement":"observed",
                                  "runtime_observation":"observed","causal_exercise":"observed"}},
        "conflicts":[{
            "id":"conflict.upper-flipper-coil",
            "path":"mechanisms.mechanism.upper-left-flipper",
            "description":"Factory coil chart specifies 25-1100 while its own upper "
            "assembly drawing and BOM specify 23-1100, 090-5030-00. "
            "Resolution path: check a production serial-numbered assembly or an "
            "attributable factory correction before selecting the upper coil part.",
            "source_refs":[MANUAL,ASSEMBLY_MANUAL],"status":"unresolved"}],
    }


def report(machine: dict) -> dict:
    missing_spatial = [d["id"] for d in machine["inputs"]+machine["outputs"] if "spatial" not in d]
    return {
        "format":"pinmame-spatial-blockers","version":1,"machine_id":KEY,
        "decision":"partial; independent cross-provider review belongs to coordinator",
        "coordinate_convention":"x=0 left, 1 right; y=0 rear, 1 front",
        "bounds":GEOMETRY["bounds"],
        "transform":"x=raw_x/1000; y=raw_y/1902; round to 6 decimals. Wall polygons use signed area centroid.",
        "selected_extraction":{"root":"external:vpx-sources/"+TABLE_SUBDIR,
                               "files":1204,"bytes":117209740,
                               "manifest_sha256":"57014dfc9904bf08aa9e9e33a9e4bffd6b2d38983efe302519f753bb24e22eaa",
                               "algorithm":"Sorted POSIX paths, sizes and full SHA256; compact sorted-key UTF8 JSON array, no newline."},
        "object_evidence":GEOMETRY["objects"],
        "physical_flipper_anchors": [
            {"mechanism": f"mechanism.{key}", "object":obj,
             "role":"effect","space":"playfield",
             "x":GEOMETRY["objects"][obj]["xy"][0],
             "y":GEOMETRY["objects"][obj]["xy"][1],
             "provenance":prov(TABLE,SCRIPT,MANUAL,VPW,status="observed")}
            for key,obj in [("lower-left-flipper","LeftFlipper"),
                            ("lower-right-flipper","RightFlipper"),
                            ("upper-left-flipper","LeftFlipper1")]],
        "manual_crosschecks":["PDF 37 bumper/switch/drop/cup identities","PDF 39 all 62 playfield lamp addresses including two 55 bulbs",
                              "PDF 40-41 physical coils and playfield/backbox insert/back-panel flasher split",
                              "PDF 55 trough/lock separate assemblies","PDF 56-57 three flippers",
                              "Addendum PDF 2-3 magnet input permutation"],
        "projections":{"wall_sensor":"Exact collidable contact-region polygon area centroid.",
                       "coil_effect":"Bumper/sling/drop/kicker mechanism, not winding center.",
                       "insert_bulb":"Named Light center reconciled to factory location symbol; no overlay duplication.",
                       "magnet_effect":"Exact cvpmMagnet event Trigger center; force radius not construction size."},
        "unplaced_records":missing_spatial,
        "blockers":[
            {"dimension":"spatial_placement","records":missing_spatial,
             "reason":"Seven individual trough contacts and lockout have no separate object in the older exact table; "
             "each slingshot has two physical leaf contacts but only a combined VPX wall impact region. "
             "Factory diagram balloons do not prove socket/contact offsets. Flash banks contain 14 playfield, "
             "16 backbox insert and 2 rear playfield back-panel bulbs; 1R's back-panel pair belongs to the playfield. "
             "The script reuses glow/reflection lights, and factory leaders do not identify every playfield socket. "
             "No safe substitute coordinates are emitted.",
             "resolution":"Acquire exact VPW geometry or measured production photos; fit factory frame/control points "
             "and retain per-socket measurements. Request recorded in external session/status.md."},
            {"dimension":"output_semantics","records":[sol["id"] for sol in machine["outputs"] if sol["binding"]=={"group":"pinmame.output.solenoid","device":11}],
             "reason":"GI relay identity, wiring and inverse runtime sense are settled; complete fitted GI socket inventory, "
             "playfield/backbox/cabinet split and individual playfield positions are not settled by aggregate stock counts.",
             "resolution":"Reconcile power-supply schematic GI feeds with socket photos/exact table; exclude apron and glow helpers."},
            {"dimension":"unresolved_conflicts","records":["conflict.upper-flipper-coil"],
             "reason":"Factory 25-1100 versus assembly 23-1100.",
             "resolution":"Production assembly or factory service correction."},
        ],
        "promotion":{"allowed":False,"missing":machine["coverage"]["missing"]},
        "evidence_paths":{"manual":"external:manuals/by-machine/"+KEY,
                          "vpx":"external:vpx-sources/data-east/guns-n-roses-1994/inventory",
                          "runtime":"external:pinmame-review-artifacts/"+KEY+"/session-20260930/runtime"},
    }


def knowledge(machine: dict) -> str:
    text = """# Guns N' Roses (Data East, 1994)

This definition describes the production machine and all three pinned 3.00 ROM
variants. It remains partial for the explicit socket/geometry and upper-coil
blockers in the spatial report; address enumeration is complete.

Six balls circulate and one remains captive. Initialize trough switches 9-14
active before starting the controller. Switch 15 is a real seventh/right trough
sensor; VPW's virtual
staging is an implementation convenience. Boot/missing-ball diagnostics must
not be confused with a phantom contact. Gun switch 62, right shooter switch 16
and auto-launch coil 3 are separate from the rose-handle spring plunger and left
shooter switch 24.

The two three-drop banks latch independently; reset coil 12 clears switches
33/34/59 and reset coil 9 clears 36/35/57. Four captive DUFF standups 17-20 and
JAM lanes 21-23 are distinct. Special drivers 17-22 are CPU/PIA-driven; GnR has
no ssSw host autofire mapping. All 64 matrix lamps are fitted, including cabinet
lamp 63 Extra-Ball and 64 Credit; 55 has two playfield bulbs. Three center-playfield
magnets 51-53 mirror 37-39 and use the
factory latch permutation. Do not add three duplicate magnets at raw addresses.

Flippers use the SSFB, with timed 50 V power and lower 8 V holding circuits.
Physical EOS contacts are normally closed knockback retriggers outside the ROM
matrix. Consumer buttons 82 (right) and 84 (left) are copied to matrix 64/63;
direct writes to 63/64 cannot operate them. Active Switch Test calls those matrix
addresses RIGHT/LEFT END OF STROKE, but the pinned core proves they receive the
button copies. Public outputs 45-48 are synthetic controller states. Public 36
never drives a GnR coil. The upper staged flipper works through de.vbs/core.vbs
cvpmFlips2 direct callback capture while 23 enables flippers. A recreation must
provide the third physical flipper and staged host control without inventing
a CPU coil 36 or ROM switch 88. Upper coil factory chart 25-1100 versus BOM 23-1100
is recorded honestly.

Output 10 selects the PPB left/right mux: 1-8 are mechanical left loads and 25-32
are right flasher banks. Output 11 is a physical GI relay, despite PinMAME's
reversed #44 brightness model. Asserted binary 11 cuts GI; release restores it.
No separate Data East GI output namespace exists. Each flasher bank has four
bulbs: 14 playfield, 16 backbox insert and 2 rear playfield back-panel bulbs
in total. Bank 1R (public 25) has two playfield bulbs and two back-panel bulbs
at the rear playfield corners. PDF 41 / printed page 37 distinguishes Backpanel
from Insert; the PDF 40 / printed page 36 Backbox Flash Lamps drawing includes
only 2R-8R. Individual physical socket positions remain unresolved.
The older Team PP script shares glow objects, reverses output 31
and has bad l2/l3 timer bindings.
Those implementation defects stay in notes; they do not change factory wiring.

The exact retained geometry has bounds 1000x1902. Positions use player view,
x left-to-right and y rear-to-front. Collidable walls use polygon area centroid;
coil effects project to their actual mechanism. Factory drawing leaders check
identity, not exact socket offsets. Primitive origins, Flasher sprites,
lightmaps, blooms and reflections are excluded. The local old tables contain
three flipper pivots. The upper-left is LeftFlipper1; the older embedded script
moves it with the lower-left, while VPW supplies staged control. No per-contact
trough geometry is present. Each sling has two physical leaf contacts; one VPX
impact-region wall cannot locate both. The retained visual helpers cannot establish
every fitted GI/flasher socket.

ROM evidence uses the verified pinned DLL and US 3.00 in new empty state.
The bounded DMD adapter matches exact header pixels and waits for game-on 23
after transient service titles. Holding Start cycles all three magnets; in Laser
Kick Test, switch 54 fires 14, 37 fires 4, 39 fires 5 and 38 fires 6. Host left/right
buttons generate 47/48 and 45/46. Active Switch Test screenshots display bumper,
sling, trough and trigger names; public readback alone is never counted as proof.

French CPU/DMD and Dutch CPU differ; Dutch DMD contents match US under a
different filename. Sound images, controller transport and physical I/O are
shared. US DMD header templates are not verified for localized firmware.
Prototype extra standup/insert, captive rest-rollover and mini-loop contact are
not production fitment; historical unbuilt stage-lock ideas are not mechanisms.
Optional factory headphone jacks do not add PinMAME I/O.

Factory SB63 (October 4, 1994) addresses auto-launch failures; SB64 (November 1, 1994)
changes shooter-ramp mounting. Retained primary documents and secondary
prototype description stay external, hashed and attributable. No physical
ball-path force, animation timer or magnet radius is inferred from VPX tuning.

"""
    for mechanism in machine["mechanisms"]:
        text += f"## {mechanism['label']}\n\n{mechanism['behavior']}\n\n"
    text += (
        "## Evidence and remaining work\n\n"
        f"Factory transcriptions: {EXCERPTS}/. Exact object locators/hashes: "
        "tools/guns_n_roses_geometry.json. Runtime hashes and expected transitions: "
        "tools/guns_n_roses_runtime.json and reusable tools/harness-scenarios/"
        "gnr-300-magnet-laser.json. Complete originals, extraction manifests, ROM "
        "inventory, fresh-state traces and native renders remain under the external "
        "working root.\n")
    return text


def artifacts() -> dict[Path, bytes]:
    machine = build()
    payload = canonical_bytes(machine)
    result = {
        Path(f"machines/partial/{STEM}.json"):payload,
        Path(f"tools/seeds/{STEM}.json"):payload,
        Path(f"knowledge/{STEM}.md"):knowledge(machine).encode(),
        Path(f"reports/spatial/{STEM}.json"):canonical_bytes(report(machine)),
    }
    result.update({Path(f"{EXCERPTS}/{name}"):text.encode()
                   for name,text in transcriptions().items()})
    return result


def verify_runtime(raw: dict) -> None:
    if raw.get("failure") or raw.get("game") != "gnr_300":
        raise ValueError("Wrong game or failed runtime trace")
    if raw.get("library_sha256") != "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e":
        raise ValueError("Wrong pinned DLL")
    expected = load_json(ROOT / "tools/guns_n_roses_runtime.json")
    if raw.get("scenario",{}).get("sha256") != expected["scenario_sha256"]:
        raise ValueError("Wrong scenario")
    steps = {s["label"]:s for s in raw["steps"]}
    for label,title in [("Find ROM Magnet Test header","MAGNET TEST"),
                        ("Find ROM Laser Kick Test header","LASER KICK TEST"),
                        ("Find ROM Switch Test","SWITCH TEST")]:
        if steps.get(label,{}).get("matched_text") != title:
            raise ValueError(f"Missing ROM display checkpoint: {title}")
    for label in ["Wait for Laser Kick Test to enable outputs",
                  "Wait for Switch Test to enable outputs"]:
        if not any(o.get("number")==23 and 1 in o.get("states",[])
                   for o in steps.get(label,{}).get("matched_outputs",[])):
            raise ValueError("Service test idle/enable state not verified")
    def states(label: str) -> dict:
        return {s["number"]:s["states"] for s in steps[label]["transitions"]["solenoids"]}
    m = states("Hold Start and cycle all three magnets")
    for a,b in [(37,51),(38,52),(39,53)]:
        if not m.get(a) or m[a] != m.get(b) or 1 not in m[a] or 0 not in m[a]:
            raise ValueError(f"Magnet mirror {a}/{b} not exercised")
    for label, output in [("Left outlane closure tests Laser Kick",14),
                          ("Eject occupied in kick test",4),
                          ("VUK occupied in kick test",5),
                          ("Scoop occupied in kick test",6)]:
        if states(label).get(output) != [1,0]:
            raise ValueError(f"{label}: expected output{output} pulse")
    for label, pair in [("Host left button reaches matrix 63",(47,48)),
                        ("Host right button reaches matrix 64",(45,46))]:
        if any(states(label).get(n) != [1,0] for n in pair):
            raise ValueError(f"{label}: synthetic flipper states missing")


def verify_external(working: Path) -> None:
    x = working / "vpx-sources" / TABLE_SUBDIR
    files = [{"path":p.relative_to(x).as_posix(),"size_bytes":p.stat().st_size,
              "sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(x.rglob("*"),key=lambda p:p.relative_to(x).as_posix()) if p.is_file()]
    digest = hashlib.sha256(json.dumps(files,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    if digest != "57014dfc9904bf08aa9e9e33a9e4bffd6b2d38983efe302519f753bb24e22eaa":
        raise ValueError("Complete VPX extraction manifest drift")
    for record in GEOMETRY["objects"].values():
        if hashlib.sha256((x/record["file"]).read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError("Geometry source file drift")
    manual = working/"manuals/by-machine"/KEY/"ipdb"/MANUAL_FILENAME
    if hashlib.sha256(manual.read_bytes()).hexdigest() != MANUAL_SHA:
        raise ValueError("Factory manual drift")
    raw_path = working/"review-artifacts"/KEY/"session-20260930/runtime/magnet-laser-v2-run.json"
    if hashlib.sha256(raw_path.read_bytes()).hexdigest() != load_json(ROOT/"tools/guns_n_roses_runtime.json")["runtime"]:
        raise ValueError("Raw runtime trace drift")
    verify_runtime(load_json(raw_path))
    # Reconcile every source artifact independently; a correct main PDF does
    # not establish the identity of an addendum, library or script.
    for source in sources(transcriptions()):
        uri = source["uri"]
        if uri.startswith("external:"):
            relative = uri.removeprefix("external:")
            relative = relative.replace("pinmame-review-artifacts/","review-artifacts/",1)
            path = working/relative
        elif source["id"] == PIN:
            path = working/"source-checkouts/pinmame/src/wpc/degames.c"
        elif source["id"] in PIN_REFS[1:]:
            name = PIN_FILES[PIN_REFS[1:].index(source["id"])][0]
            path = working/"source-checkouts/pinmame/src/wpc"/name
        elif source["id"] == VPW:
            path = working/"source-checkouts/vpxtable_scripts/Guns N Roses (Data East 1994) VPW 1.2.1.vbs"
        else:continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Retained source drift:{source['id']}")
    for record in MANUAL_ACQUISITIONS:
        path = working/"manuals"/record["relative_path"]
        if path.stat().st_size != record["bytes"] or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError(f"Retained document acquisition drift:{record['original_filename']}")
    active = load_json(ROOT/"tools/guns_n_roses_active_switches.json")
    runtime_dir = raw_path.parent
    active_raw = load_json(runtime_dir/active["raw_file"])
    if active_raw.get("failure") or active_raw.get("scenario",{}).get("sha256") != active["scenario_sha256"]:
        raise ValueError("Wrong Active Switch run")
    steps = {s["label"]:s for s in active_raw["steps"]}
    if steps.get("Find Active Switch Test",{}).get("matched_text") != "ACTIVE SWITCH TEST":
        raise ValueError("Active Switch display checkpoint missing")
    snapshots = {s["label"]:s for s in active_raw["snapshots"]}
    if len(active["records"]) != 10:
        raise ValueError("Active Switch screenshots are incomplete")
    for record in active["records"]:
        frame = snapshots[record["snapshot_label"]]["displays"][0]
        if frame["pixel_sha256"] != record["pixel_sha256"]:
            raise ValueError("Active Switch display pixels changed")
        pgm = runtime_dir/"active-switch-dmd"/record["pgm_file"]
        if hashlib.sha256(pgm.read_bytes()).hexdigest() != record["pgm_sha256"]:
            raise ValueError("Active Switch screenshot changed")
    from build_external_evidence_manifest import check_manifest
    provenance = load_json(ROOT/"tools/guns_n_roses_runtime_provenance.json")
    library = working/"builds/pinmame-8371478/Release/pinmame64.dll"
    if hashlib.sha256(library.read_bytes()).hexdigest() != provenance["library_sha256"]:
        raise ValueError("Retained pinned DLL drift")
    if check_manifest(runtime_dir,"gnr_300") != provenance["manifest"]["sha256"]:
        raise ValueError("Runtime directory manifest drift")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--regenerate",action="store_true")
    parser.add_argument("--repository-root",type=Path,default=ROOT)
    parser.add_argument("--evidence-root",type=Path)
    args = parser.parse_args()
    if (args.repository_root/f"machines/author-ready/{STEM}.json").exists():
        raise ValueError("Refusing to overwrite an existing author-ready artifact")
    for path,payload in artifacts().items():
        target = args.repository_root/path
        if args.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n",b"\n") != payload:
                raise ValueError(f"Curator drift: {path}")
        else:
            write_bytes(target,payload)
    for stem,digest,_ in IMAGES.values():
        if hashlib.sha256((args.repository_root/f"{EXCERPTS}/{stem}.webp").read_bytes()).hexdigest() != digest:
            raise ValueError(f"Factory diagram crop drift: {stem}")
    if args.evidence_root:
        verify_external(args.evidence_root)
    print("Guns N' Roses artifacts match; partial blockers remain explicit.")


if __name__ == "__main__":
    main()
