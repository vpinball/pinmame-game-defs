"""Deterministically curate Stern World Poker Tour (2006).

The retained seed is a transcription of factory address tables. Spatial points
are exact VPX object centres, but remain observational until the physical
socket/sensor association is proved. This contribution stays partial.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, write_bytes

ROOT = Path(__file__).resolve().parents[1]
STEM = "world-poker-tour-2006"
MACHINE = "stern.world-poker-tour.2006"
SEED_PATH = ROOT / f"tools/seeds/stern/{STEM}.json"
SPATIAL_PATH = ROOT / f"tools/seeds/stern/{STEM}-spatial.json"
MANUAL_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-manual-tables.md"
MECH_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-mechanisms.md"
SOURCE_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-script-and-core.md"
DIAG_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-coil-diagnostic.md"
MINI_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-mini-displays.md"
SERVICE_EXCERPT = ROOT / f"evidence/excerpts/stern/{STEM}-service-bulletins.md"
DEST = ROOT / f"machines/partial/stern/{STEM}.json"
KNOWLEDGE = ROOT / f"knowledge/stern/{STEM}.md"
AUDIT = ROOT / f"reports/spatial/stern/{STEM}.json"

MANUAL = "manual.stern-wpt-2006"
MANUAL_ASSEMBLY = "manual.stern-wpt-2006-assembly"
CORE = "pinmame.core.8371478a7640"
CATALOG = "pinmame.catalog.8371478a7640"
SCRIPT = "vpx.script.wpt-known-working"
TABLE = "vpx.table.wpt-062018a"
TABLE_OLD = "vpx.table.wpt-archive"
RUNTIME = "runtime.wpt-140a-switch-test"
RUNTIME_COIL = "runtime.wpt-140a-coil-test"
SB = "bulletin.stern-wpt-165"
SB163 = "bulletin.stern-wpt-163"
SB164 = "bulletin.stern-wpt-164"
PINNED_LIBRARY_SHA256 = "ddee814f9dd321d03f7e6978f93096fe830e029e61d0399846e7e44428b7ce4e"
PINNED_SWITCH_TRACE_SHA256 = "b556e88286de5212d1cde8ae326f1436717251486103215fbbff4b82bd57f28f"
PINNED_COIL_TRACE_SHA256 = "1b31464a14146bdb93f0afa7999cd42e61a3ee725f8a72d260e1ca458489800a"

MATRIX_RETURNS = [
    ("WHT-BRN", "J6-P9"), ("WHT-RED", "J6-P8"), ("WHT-ORG", "J6-P7"), ("WHT-YEL", "J6-P6"),
    ("WHT-GRN", "J6-P5"), ("WHT-BLU", "J6-P3"), ("WHT-VIO", "J6-P2"), ("WHT-GRY", "J6-P1"),
    ("TAN-BLK", "J12-P9"), ("TAN-RED", "J12-P8"), ("TAN-ORG", "J12-P7"), ("TAN-YEL", "J12-P6"),
    ("TAN-GRN", "J12-P4"), ("TAN-BLU", "J12-P3"), ("TAN-VIO", "J12-P2"), ("TAN-WHT", "J12-P1"),
]
MATRIX_DRIVES = [("GRN-BRN", "J1-P1"), ("GRN-RED", "J1-P3"), ("GRN-ORG", "J1-P4"), ("GRN-YEL", "J1-P5")]
DEDICATED_DEVICES = [65, 66, 67, 68, 69, 70, 71, 72, 84, 83, 82, 81, 88, 87, 86, 85, -7, -6, -5, -4, -3, -2, -1, 0]
DEDICATED_WIRES = [
    ("PNK-BRN", "J2-P2"), ("PNK-RED", "J2-P3"), ("PNK-ORG", "J2-P4"), ("PNK-YEL", "J2-P6"),
    ("PNK-GRN", "J2-P7"), ("PNK-BLU", "J2-P8"), ("PNK-VIO", "J2-P9"), ("PNK-GRY", "J2-P10"),
    ("GRY-BRN", "J3-P1"), ("GRY-RED", "J3-P2"), ("GRY-ORG", "J3-P4"), ("GRY-YEL", "J3-P5"),
    ("GRY-GRN", "J3-P6"), ("GRY-BLU", "J3-P7"), ("GRY-VIO", "J3-P8"), ("GRY-BLK", "J3-P9"),
    ("LGN-BRN", "J13-P1"), ("LGN-RED", "J13-P3"), ("LGN-ORG", "J13-P4"), ("LGN-YEL", "J13-P5"),
    ("LGN-BLK", "J13-P6"), ("LGN-BLU", "J13-P7"), ("LGN-VIO", "J13-P8"), ("LGN-GRY", "J13-P9"),
]
COIL_CONTROL_WIRE = [
    "BRN-BLK", "BRN-RED", "BRN-ORG", "BRN-YEL", "BRN-GRN", "BRN-BLU", "BRN-VIO", "BRN-GRY",
    "BLU-BRN", "BLU-RED", "BLU-ORG", "BLU-YEL", "BLU-GRN", "BLU-BLK", "ORG-GRY", "ORG-VIO",
    "VIO-BRN", "VIO-RED", "VIO-ORG", "VIO-YEL", "VIO-GRN", "VIO-BLU", "VIO-BLK", "VIO-GRY",
    "BLK-BRN", "BLK-RED", "BLK-ORG", "BLK-YEL", "BLK-GRN", "BLK-BLU", "BLK-VIO", "BLK-GRY",
]
COIL_CONTROL_PIN = [
    "J8-P1", "J8-P3", "J8-P4", "J8-P5", "J8-P6", "J8-P7", "J8-P8", "J8-P9",
    "J9-P1", "J9-P2", "J9-P4", "J9-P5", "J9-P6", "J9-P7", "J9-P8", "J9-P9",
    "J7-P2", "J7-P3", "J7-P4", "J7-P6", "J7-P7", "J7-P8", "J7-P9", "J7-P10",
    "J6-P1", "J6-P2", "J6-P3", "J6-P4", "J6-P5", "J6-P6", "J6-P7", "J6-P8",
]
LAMP_COLUMN_WIRES = ["RED-BRN", "RED-BLK", "RED-ORG", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY", "RED-WHT", "RED"]
LAMP_COLUMN_PINS = ["J12-P1", "J12-P2", "J12-P3", "J12-P4", "J12-P5", "J12-P6", "J12-P7", "J12-P9", "J12-P10", "J12-P11"]
LAMP_RETURN_WIRES = ["YEL-BRN", "YEL-RED", "YEL-ORG", "YEL-BLK", "YEL-GRN", "YEL-BLU", "YEL-VIO", "YEL-GRY"]
LAMP_RETURN_PINS = ["J13-P9", "J13-P8", "J13-P7", "J13-P6", "J13-P5", "J13-P4", "J13-P3", "J13-P1"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "unused"


def alias(group: str, value: int | str) -> list[dict]:
    return [{"namespace": group, "value": str(value)}]


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def placed(name: str, role: str, objects: dict, *refs: str) -> dict | None:
    object_data = objects.get(name)
    if object_data is None:
        return None
    return {
        "status": "observed",
        "placements": [{
            "id": f"placement.{slug(name)}", "role": role, "space": "playfield",
            "x": object_data[0], "y": object_data[1],
            "provenance": prov(TABLE, *refs, status="observed"),
        }],
    }


def parse_manual_rows(text: str, heading: str, count: int) -> list[list[str]]:
    section = text.split(heading, 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if cells and cells[0].isdigit():
            n = int(cells[0])
            if 1 <= n <= count and n not in rows:
                rows[n] = cells
    if set(rows) != set(range(1, count + 1)):
        raise ValueError(f"{heading}: incomplete address table {sorted(set(range(1,count+1))-set(rows))}")
    return [rows[i] for i in range(1, count + 1)]


def switch_id(n: int, seed: dict) -> str:
    return f"switch.{n}-{slug(seed['switch_labels'][n-1])}"


def coil_id(n: int, seed: dict) -> str:
    return f"coil.{n}-{slug(seed['coil_labels'][n-1])}"


def input_records(seed: dict, spatial: dict, switch_rows: list[list[str]]) -> list[dict]:
    records = []
    for n, label in enumerate(seed["switch_labels"], 1):
        row = switch_rows[n - 1]
        used = n in seed["used_matrix_switches"]
        opto = n in seed["opto_matrix_switches"]
        cabinet = n in seed["cabinet_matrix_switches"]
        # The matrix chart names addresses and parts, but does not itself
        # establish a contact style for every listed part. Only assemblies
        # that actually name a micro or blade/leaf contact classify one.
        leaf = n in {14, 26, 27, 30, 31, 32, 41}
        micro = n in {3, 9, 44, 49, 50, 51, 53, 55}
        physical = {"switch_type": "opto" if opto else "button" if cabinet else "leaf" if leaf else "microswitch" if micro else "unknown", "quantity": 2 if n in {26, 27} else 1}
        if not used:
            physical = {"switch_type": "unknown", "notes": "Factory address table prints NOT USED; placeholder part numbers are not fitted hardware."}
        if used and row[3] != "— (printed blank)":
            physical["part_number"] = row[3].split(";")[0].strip()
        if used and row[4] != "— (printed blank)":
            physical["location"] = row[4]
        if used and physical["switch_type"] == "unknown":
            physical["notes"] = "Factory chart identifies the part and position but does not establish leaf versus microswitch contact construction; retain unknown pending an assembly-level contact drawing or installed-part inspection."
        if n == 15:
            physical["notes"] = "Factory switch-location drawing on PDF page 7 requires the optional Tournament Kit for this button."
        if n == 54:
            physical.pop("quantity", None)
            physical["notes"] = "Factory grid says LEFT RAMP MADE; two separate assembly drawings label an opto SW54, and the VPX script asserts 54 from both the left ramp and ScoopTrigger. Fitment remains conflicted."
        if n == 56:
            physical["notes"] = "Factory grid calls this an OPTO PAIR, while the printed SW56 footnote describes a cabinet hanger bracket and contact wire. Exact construction remains conflicted."
        drive = MATRIX_DRIVES[(n - 1) // 16]
        ret = MATRIX_RETURNS[(n - 1) % 16]
        item = {
            "id": switch_id(n, seed), "label": label, "kind": "switch",
            "binding": {"group": "pinmame.input.switch", "device": n},
            "aliases": alias("manual.switch", f"SW{n}"),
            "availability": "optional" if n == 15 else "used" if used else "unused", "physical": physical,
            "wiring": {"board": "SAM CPU/Sound switch matrix", "drive_wire": drive[0], "drive_connection": drive[1], "return_wire": ret[0], "return_connection": ret[1]},
            "provenance": prov(MANUAL, CORE, *([RUNTIME] if n in {3, 21, 63} else []), status="conflicted" if n in {54, 56} else "validated"),
        }
        if used and n not in {54, 56}:
            # The factory chart states the sensor class; controller-facing
            # polarity is only asserted for three ROM-tested controls.
            item["pulse"] = n in {8, 14, 26, 27, 30, 31, 32, 41, 42, 43, 45, 46, 47, 48, 60, 61, 62}
        if not used:
            item["spatial"] = na("unused", MANUAL, CORE)
        elif cabinet or n in {55, 57, 58, 59, 60, 61, 62, 63}:
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif n not in {54, 56}:
            name = f"sw{n}"
            candidate = placed(name, "sensor", spatial, MANUAL)
            if candidate:
                item["spatial"] = candidate
        records.append(item)
    for d, (device, label, wire) in enumerate(zip(DEDICATED_DEVICES, seed["dedicated_labels"], DEDICATED_WIRES), 1):
        availability = "unused" if d in {6, 20} else "optional" if d in {5, 7, 8, 18, 19} else "used"
        kind = "tilt" if d in {17, 18} else "leaf" if d in {10, 12, 14, 16} else "button"
        ground = ("BLK", "J2-P1/11 and J3-P1") if d <= 8 else ("BLK", "J3-P10") if d <= 16 else ("BLK", "J13-P10")
        dedicated = {
            "id": f"switch.d{d}-{slug(label)}", "label": label, "kind": "switch",
            "binding": {"group": "pinmame.input.switch", "device": device},
            "aliases": alias("manual.switch", f"D{d}"),
            "availability": availability,
            "physical": {"switch_type": "unknown", "notes": "Factory dedicated chart prints NOT USED."} if availability == "unused" else {"switch_type": kind, "location": "cabinet or backbox" if d >= 17 or d <= 9 else "flipper assembly", "quantity": 1},
            "wiring": {"board": "SAM CPU/Sound dedicated input", "drive_wire": wire[0], "drive_connection": wire[1], "return_wire": ground[0], "return_connection": ground[1]},
            "spatial": na("unused" if availability == "unused" else "cabinet_or_service", MANUAL),
            "provenance": prov(MANUAL, CORE),
        }
        if 9 <= d <= 16:
            dedicated["normally_closed"] = d in {10, 12, 14, 16}
        records.append(dedicated)
    for n in range(1, 9):
        records.append({
            "id": f"dip.{n}", "label": f"CPU/Sound DIP switch {n}", "kind": "dip_switch",
            "binding": {"group": "pinmame.input.dip", "device": n},
            "aliases": alias("manual.dip", f"SW1-{n}"), "availability": "used",
            "physical": {"switch_type": "dip", "location": "CPU/Sound board between J3 and J13"},
            "spatial": na("dip_switch", MANUAL), "provenance": prov(MANUAL, CORE),
        })
    return records


def coil_wiring(n: int) -> dict:
    value = {"board": "SAM I/O Power Driver", "driver_transistor": f"Q{n}", "control_wire": COIL_CONTROL_WIRE[n-1], "control_connection": COIL_CONTROL_PIN[n-1]}
    if n <= 12 or n == 21:
        value.update(power_wire="YEL-VIO", power_connection="J10-P9/10", nominal_voltage_v=50, voltage_type="dc")
    elif n <= 16:
        value.update(power_wire="GRY-YEL via flipper feed" if n % 2 else "BLU-YEL via flipper feed", power_connection="J10-P6/7", nominal_voltage_v=50, voltage_type="dc")
    elif n in {17, 18, 19, 20}:
        value.update(power_wire="BRN", power_connection="J7-P1", nominal_voltage_v=20, voltage_type="dc")
    elif n == 24:
        value.update(power_wire="RED", power_connection="J16-P4-8", nominal_voltage_v=5, voltage_type="dc")
    else:
        value.update(power_wire="ORG", power_connection="J6-P10", nominal_voltage_v=20, voltage_type="dc")
    return value


def output_records(seed: dict, spatial: dict, coil_rows: list[list[str]], lamp_rows: list[list[str]]) -> list[dict]:
    result = []
    for n, label in enumerate(seed["coil_labels"], 1):
        flash = n in seed["flasher_coils"]
        optional = n in seed["optional_coils"]
        on_backpanel = n in set(seed["backpanel_flashers"]) | {4, 12, 19, 32}
        physical = {"location": "backpanel" if on_backpanel else "playfield", "quantity": 1}
        if optional:
            physical = {"notes": "Factory chart calls Q24 an optional 5 V coil channel; no fitted device is established."}
        if coil_rows[n-1][-1] != "— (printed blank)":
            physical["part_number"] = coil_rows[n-1][-1]
        if n == 21:
            physical["notes"] = "Q21 uses the separate 50 V step-up board 520-5254-00; the standard low-side control connector remains J7-P7."
        if n == 32:
            physical.pop("part_number", None)
            physical["notes"] = "Assembly sheet p.118 names a 25-1240 coil / 090-5034-ND, but the coil chart p.10 and board diagram p.123 print 26-1200 / 090-5044-ND. Physical coil fitment is unresolved. Board p.123 and ROM diagnostic independently show orange 20 V feed; p.10's brown feed is a chart error."
        item = {
            "id": coil_id(n, seed), "label": label, "kind": "flasher" if flash else "coil",
            "binding": {"group": "pinmame.output.solenoid", "device": n},
            "aliases": alias("manual.coil", f"Q{n}"), "availability": "optional" if optional else "used",
            "physical": physical, "wiring": coil_wiring(n), "provenance": prov(MANUAL, CORE, *([RUNTIME_COIL] if n != 24 else []), *([MANUAL_ASSEMBLY] if n == 32 else []), status="conflicted" if n == 32 else "validated"),
        }
        if on_backpanel and not optional:
            item["spatial"] = na("cabinet_or_service", MANUAL)
        result.append(item)
    for n in range(33, 67):
        availability = "used" if n == 33 else "unused"
        result.append({
            "id": f"signal.solenoid-{n}", "label": "Synthetic game-on signal" if n == 33 else f"Unused SAM solenoid capacity {n}",
            "kind": "virtual",
            "binding": {"group": "pinmame.output.solenoid", "device": n},
            "aliases": alias("pinmame.solenoid", n), "availability": availability,
            "spatial": na("virtual", CORE), "provenance": prov(CORE),
        })
    for n, label in enumerate(seed["lamp_labels"], 1):
        row = lamp_rows[n-1]
        col = (n - 1) // 8
        ret = (n - 1) % 8
        used = n not in seed["unused_lamps"]
        kind = "cabinet_or_service" if n in seed["cabinet_lamps"] or n in seed["backpanel_lamps"] else None
        item = {
            "id": f"lamp.{n}-{slug(label)}", "label": label, "kind": "lamp",
            "binding": {"group": "pinmame.output.lamp", "device": n},
            "aliases": alias("manual.lamp", n), "availability": "used" if used else "unused",
            "physical": {"part_number": row[-1], "quantity": 1} if used else {"notes": "Factory table prints NOT USED."},
            "wiring": {"board": "SAM I/O Power Driver lamp matrix", "driver_transistor": f"Q{33+col}", "drive_wire": LAMP_COLUMN_WIRES[col], "drive_connection": LAMP_COLUMN_PINS[col], "return_wire": LAMP_RETURN_WIRES[ret], "return_connection": LAMP_RETURN_PINS[ret], "nominal_voltage_v": 18, "voltage_type": "dc"},
            "provenance": prov(MANUAL, CORE),
        }
        if not used or kind:
            item["spatial"] = na("unused" if not used else kind, MANUAL)
        else:
            candidate = placed(f"l{n}", "emitter", spatial, MANUAL)
            if candidate:
                item["spatial"] = candidate
        result.append(item)
    # The public controller profile reserves 1..339; this game selects only
    # the 80-column SAM lamp extension. Preserve the rest as explicit capacity.
    for n in range(81, 340):
        result.append({
            "id": f"lamp.capacity-{n}", "label": f"Unused SAM lamp capacity {n}", "kind": "virtual",
            "binding": {"group": "pinmame.output.lamp", "device": n},
            "aliases": alias("pinmame.lamp", n), "availability": "unused",
            "spatial": na("virtual", CORE), "provenance": prov(CORE),
        })
    result.append({
        "id": "gi.aggregate", "label": "Aggregate general illumination", "kind": "gi",
        "binding": {"group": "pinmame.output.gi", "device": 0}, "aliases": alias("pinmame.gi", 0),
        "availability": "used",
        "physical": {"notes": "Factory manual has four separately wired GI circuits and variable production bulb quantity; LibPinMAME exposes one aggregate address only."},
        "provenance": prov(MANUAL, CORE),
    })
    return result


def mechanism_records(seed: dict) -> list[dict]:
    groups = [
        ("four-ball-trough", "Four-ball trough and stacking opto", "other", [1], [18,19,20,21,22,23], "Four ordered ball seats feed Q1 to the shooter lane; SW21 and SW22 are paired optos. Occupied seats persist; Q1 pulses one ball into the shooter. Jam/stacking optical clearance gates additional feed. Initialise actual four-ball occupancy before boot and recover trapped balls through the trough, never by directly asserting an unrelated cabinet button."),
        ("shooter-and-vuk", "Shooter, auto-launch and shooter VUK", "kicker", [2,3], [3,23,51], "SW23 holds a staged shooter ball; player plunge or Q2 launches it. The routed ball may enter the shooter-lane vertical up-kicker, where SW3 senses capture and Q3 ejects into its wire ramp; SW51 senses its exit gate. A stuck SW3 with no Q3 discharge is a VUK jam."),
        ("left-vuk-transfer", "Left VUK and transfer trough", "kicker", [4], [55,56,59], "The backpanel left VUK lifts a ball from SW55 through a tube toward the upper playfield; SW56 watches the upper exit and SW59 the transfer tube's first/left position. Retain separate tube occupancy and avoid inventing a coil for gravity transfer. The SW56 construction is conflicted between grid and footnote."),
        ("left-eight-bank", "Eight-bank left drops", "drop_target_bank", [5,6], list(range(33,41)), "Eight latched targets each interrupt a slotted opto. The assembly has two four-target reset mechanisms driven by Q5 and Q6, so either half may reset independently. A raised target becomes down when struck, remains down until its half-bank reset lifts it, and can jam down if spring or lift bracket fails."),
        ("middle-four-bank", "Four-bank middle drops", "drop_target_bank", [7], list(range(10,14)), "Four slotted optos detect four latching drop blades. Q7 raises the bank through a common lift bracket and springs. Preserve individual down states and the simultaneous mechanical reset; a failed lift or opto leaves a false down target."),
        ("right-four-bank", "Four-bank right drops", "drop_target_bank", [8], list(range(4,8)), "Four slotted optos detect four latching drop blades, numbered bottom-to-top. Q8 raises the whole bank; each target remains down until reset. Keep Q8 separate from Q7 and respect partial-bank scores before reset."),
        ("three-pops", "Three pop bumpers", "other", [9,10,11], [30,31,32], "Each skirt switch fires its matching independent high-current bumper coil; the cap lamp is a separate matrix output. A lodged or bouncing skirt can repeat actuation and needs ordinary debounce."),
        ("jail-bars", "Ace-in-the-Hole jail bars and latch", "toy", [12,19], [57,58,63], "Q12 raises the jail-bar/mouse-trap assembly and Q19 operates its mini-coil latch. Optical transmitter/receiver pairs monitor bash and rest; SW63 is the raised-end slotted opto. A ball can strike the bars and change SW57 before the assembly returns to rest SW58. Recreate moving collision and latch state; never collapse all three sensors into a single animation flag."),
        ("left-ramp", "Reverse-O-Matic left ramp and up post", "diverter", [20], [54], "Q20 raises a post on the left steel ramp to affect ball routing. The left-ramp made opto is designated SW54 in the grid and ramp drawing, but a separate transfer-trough drawing and two script handlers also claim 54. The exact number and sensing point need physical continuity or ROM diagnostic/firmware proof before final wiring."),
        ("right-ramp", "Right ramp down post", "gate", [32], [9,52], "A ball enters past SW9 and clears the right-ramp made opto SW52. Q32 operates the down-post ball stop; the post must actually alter ball containment and return to its default state after the drive ends."),
        ("playfield-flippers", "Four independently driven flippers", "other", [13,14,15,16], [], "Upper left/right Q13/Q14 and lower left/right Q15/Q16 are distinct factory coil/EOS assemblies. The left and right cabinet buttons are double-stacked: half travel closes the lower N.O. button D9/D11, full press also closes the corresponding upper N.O. button D13/D15. D10/D12/D14/D16 are N.C. EOS contacts that open about 1/16 inch into the stroke. The factory CPU applies an initial 40 ms kick and then 1 ms pulses every 12 ms while held; a forced rebound closing EOS requests another kick. The older table deliberately comments Q13/Q14 callbacks for SAM fastflips and rotates upper flippers from its lower callbacks; the 2018 and pinned scripts use separate upper callbacks. Both implementations model four physical flippers."),
        ("slings-and-eject", "Slingshots and eject popper", "kicker", [17,18,21], [26,27,49], "Each slingshot has two physical leaf contacts feeding one matrix address and its own Q17/Q18 coil. The separate eject popper captures a ball on SW49 then fires Q21 through the step-up board; its high-side feed is 50 V, unlike neighboring low-power drivers."),
    ]
    result = []
    for ident, label, kind, qs, sws, behavior in groups:
        result.append({
            "id": f"mechanism.{ident}", "label": label, "kind": kind,
            "actuators": [coil_id(n, seed) for n in qs],
            "sensors": [switch_id(n, seed) for n in sws],
            "behavior": behavior, "provenance": prov(MANUAL, SCRIPT, status="conflicted" if ident in {"left-ramp","left-vuk-transfer"} else "observed"),
        })
    return result


def sources(seed: dict, spatial: dict) -> list[dict]:
    def excerpt(ident: str, path: Path, locator: str) -> dict:
        by = "GPT-6-Sol" if path in {SOURCE_EXCERPT, DIAG_EXCERPT, MINI_EXCERPT, SERVICE_EXCERPT} else "GPT Terra; GPT-6-Sol correction"
        reviewed = path in {SOURCE_EXCERPT, DIAG_EXCERPT, MINI_EXCERPT, SERVICE_EXCERPT}  # full manual tables/assemblies remain candidate
        return {"id": ident, "locator": locator, "path": path.relative_to(ROOT).as_posix(), "sha256": sha(path), "method": "mixed", "transcribed_by": by, "reviewed": reviewed}
    return [
        {"id": MANUAL, "kind": "manual", "uri": "https://sternpinball.com/wp-content/uploads/2018/11/World_Poker_Tour_Manual.pdf", "sha256": seed["manual_sha256"], "locator": "PDF pp. 6-11, 123, 125-126, 129, 166-167 and 179; printed DR.4-9 and Sec.5 Ch.1-4", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt("wpt-address-tables", MANUAL_EXCERPT, "PDF pp.6-7,8,10,125-126"), excerpt("wpt-wiring-reconciliation", DIAG_EXCERPT, "PDF pp.10,118,123,129,179"), excerpt("wpt-card-display-board", MINI_EXCERPT, "PDF pp.7,166-167")]},
        {"id": MANUAL_ASSEMBLY, "kind": "manual", "uri": "https://sternpinball.com/wp-content/uploads/2018/11/World_Poker_Tour_Manual.pdf", "sha256": seed["manual_sha256"], "locator": "PDF pp.98-119, printed Sec.4 Ch.2 pp.74-93", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt("wpt-mechanisms", MECH_EXCERPT, "PDF pp.98-119")]},
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": seed["pinmame_revision"], "locator": "src/wpc/sam.c WPT INITGAME, LED board and SAM I/O; src/wpc/core.c", "excerpts": [excerpt("wpt-core-topology", SOURCE_EXCERPT, "sam.c 923-1009, 1373-1398, 2361-2378, 2448; core.c 2117-2163"), excerpt("wpt-card-display-routing", MINI_EXCERPT, "sam.c 923-1009 and 2361-2378")]},
        {"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": seed["pinmame_revision"], "locator": "46 wpt_ drivers pinned native catalog"},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:source-checkouts/vpxtable_scripts/World Poker Tour (Stern 2006) v.2.3.1.vbs", "revision": "0c036bb61b4b4e8c778c37559f6795df8cd1521e", "sha256": "d44738c5fa4693a8b096f226399f3ea2f81c985a1e780c33d012acf7d2bc390a", "locator": "controller switch, solenoid and ball-routing callbacks", "known_working": True, "license": "NOASSERTION", "attribution": "VPX table script authors", "excerpts": [excerpt("wpt-script-routing", SOURCE_EXCERPT, "v2.3.1 lines 304-307, 539-574, 735-767, 910-911, 1094, 2649-2664")]},
        {"id": TABLE, "kind": "vpx_table", "uri": "external:vpx-sources/stern/world-poker-tour-2006/wpt-062018a/wpt 062018a.vpx", "sha256": spatial["table_sha256"], "locator": "vpxtool v0.33.3 extraction; 952x2250 VPU; object centres and extraction manifest " + spatial["table_manifest_sha256"], "license": "NOASSERTION", "attribution": "VPX table author", "excerpts": [{"id": "wpt-table-object-centres", "locator": "vpxtool gameitems named lN/swN/ScoopTrigger and Dn", "path": SPATIAL_PATH.relative_to(ROOT).as_posix(), "sha256": sha(SPATIAL_PATH), "method": "mixed", "transcribed_by": "GPT Luna; GPT-6-Sol review", "reviewed": False}, excerpt("wpt-card-display-centres", MINI_EXCERPT, "script.vbs lines 1318-1389; Light.D18 through Light.D473 centres")]},
        {"id": TABLE_OLD, "kind": "vpx_table", "uri": "external:vpx-sources/stern/world-poker-tour-2006/world-poker-tour-stern-2006/World Poker Tour (Stern 2006).vpx", "sha256": "92a9720af51c825c9603d9dc78acc2423b7f86c907e1c4a6e92393156a22d9b8", "locator": "Alternate 952x2250 VPX, wpt_140a, extraction manifest 368e8262d51e6db70f8f05a8919f008d8d0a92340d29b1527ff8e9c700ada9e6; embedded script ad1b9829 comments Q13/Q14 for SAM fastflips but its lower callbacks rotate the upper flippers", "license": "NOASSERTION", "attribution": "VPX table author", "excerpts": [excerpt("wpt-alternate-table", SOURCE_EXCERPT, "alternate table/script comparison")]},
        {"id": RUNTIME, "kind": "service_diagnostic", "uri": "external:review-artifacts/stern.world-poker-tour.2006/session-20260930/wpt-switch-test-pinned-frames-run.json", "revision": seed["pinmame_revision"], "sha256": PINNED_SWITCH_TRACE_SHA256, "locator": "Verified pinned native DLL SHA-256 " + PINNED_LIBRARY_SHA256 + "; fresh wpt_140a ROM Switch Test: SW3/21/63 public level 1 reports SHOOTER LANE VUK, TROUGH #1 (R), JAIL BARS UP; committed scenario SHA-256 84ebcccc31bb7942bbefac737d3b88fa0bc1f786ae6c3e501ec861954961ec5a"},
        {"id": RUNTIME_COIL, "kind": "service_diagnostic", "uri": "external:review-artifacts/stern.world-poker-tour.2006/session-20260930/wpt-coil-diagnostic-pinned-frames-run.json", "revision": seed["pinmame_revision"], "sha256": PINNED_COIL_TRACE_SHA256, "locator": "Verified pinned native DLL SHA-256 " + PINNED_LIBRARY_SHA256 + "; fresh wpt_140a Single Coil Test DMD sweep: displayed Q1-23 and Q25-32 labels, Q24 skipped; actions after Q24 are offset from host labels; Q32 ORG/BLK-GRY; next AUX1 selector is diagnostic #33, distinct from public synthetic game-on 33", "excerpts": [excerpt("wpt-coil-diagnostic", DIAG_EXCERPT, "V14.0 Single Coil Test DMD sweep")]},
        {"id": SB163, "kind": "service_bulletin", "uri": "external:manuals/by-machine/stern.world-poker-tour.2006/sb163.pdf", "sha256": "da0f791a94e0c02cac1ad7288d41dcbc4da916232be42c8e756e3e70b350ae49", "locator": "Stern Service Bulletin 163, July 24 2006, p.1: unstable CPU/Sound PCB flash can cause resets or endless multiball; replacement 520-5246-00", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt("wpt-sb163", SERVICE_EXCERPT, "Bulletin 163 p.1")]},
        {"id": SB164, "kind": "service_bulletin", "uri": "external:manuals/by-machine/stern.world-poker-tour.2006/sb164.pdf", "sha256": "b7d0f5274dd0477f727a8f4fa0d7388821f826f112b2267a3d7b2bfc3c5ecb28", "locator": "Stern Service Bulletin 164, August 22 2006, p.1-2: SAM game-code update and backup procedure with CPU/Sound DIP #8", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt("wpt-sb164", SERVICE_EXCERPT, "Bulletin 164 pp.1-2")]},
        {"id": SB, "kind": "service_bulletin", "uri": "external:manuals/by-machine/stern.world-poker-tour.2006/sb165.pdf", "sha256": "40cf83f3109c7adcdfffebebaa16022f18597da12ebcbcfcee3b7f601fbe042c", "locator": "Stern Service Bulletin 165, dated September 19 2006: pre-v1.11 drop-target serve auto-launch behavior vs v1.11+", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt("wpt-sb165", SERVICE_EXCERPT, "Bulletin 165 p.1")]},
    ]


def build(seed: dict, spatial: dict) -> dict:
    manual_text = MANUAL_EXCERPT.read_text(encoding="utf-8")
    switch_rows = parse_manual_rows(manual_text, "| # | Literal switch name", 64)
    lamp_rows = parse_manual_rows(manual_text, "| # | Printed bulb type", 80)
    coil_rows = parse_manual_rows(manual_text, "| # | Literal coil / flash lamp", 32)
    # No transcribed address may silently lose its manual identity.
    assert len(seed["switch_labels"]) == 64 and len(seed["dedicated_labels"]) == 24
    assert len(seed["lamp_labels"]) == 80 and len(seed["coil_labels"]) == 32
    assert all(spatial["bounds"][k] == v for k, v in {"left":0,"top":0,"right":952,"bottom":2250}.items())
    catalog_drivers = [d for d in json.loads((ROOT/"catalog/pinmame.json").read_text(encoding="utf-8"))["drivers"] if d["id"].startswith("wpt_")]
    assert len(catalog_drivers) == 46 and all(d["root_driver"] == "wpt_140a" for d in catalog_drivers)
    drivers = []
    for entry in catalog_drivers:
        driver = {k: entry[k] for k in ("id", "description", "year", "manufacturer", "flags")}
        if entry["id"] != "wpt_140a":
            driver["clone_of"] = "wpt_140a"
        driver["physical_compatibility"] = "identical"
        version_prefix = re.match(r"wpt_(\d{3})", entry["id"])
        assert version_prefix is not None
        serve_rule = ("Before v1.11: Bulletin 165 says three down drops during serve can trigger an immediate auto-launch."
                      if int(version_prefix.group(1)) < 111 else
                      "V1.11 or later: Bulletin 165 says three down drops during serve are spotted without auto-launch.")
        driver["variant_notes"] = "Same 2006 factory WPT hardware; description identifies firmware and language. " + serve_rule
        drivers.append(driver)
    assert [item["controller_index"] for item in spatial["mini_displays"]] == list(range(1, 15))
    displays = [{
        "id": "display.main-dmd", "label": "Backbox 128x32 dot-matrix display", "kind": "dmd", "controller_index": 0, "width": 128, "height": 32, "physical_location": "cabinet_or_service",
        "spatial": na("cabinet_or_service", MANUAL, CORE), "provenance": prov(MANUAL, CORE, RUNTIME),
    }]
    for n in range(1, 15):
        center = spatial["mini_displays"][n - 1]
        assert center["center_pixel"] == f"D{18+35*(n-1)}"
        displays.append({
            "id": f"display.card-{n}", "label": f"Playfield poker-card mini dot matrix block {n}", "kind": "dmd",
            "controller_index": n, "width": 5, "height": 7, "physical_location": "playfield",
            "spatial": {"status": "observed", "placements": [{
                "id": f"placement.card-{n}-display", "role": "display", "space": "playfield",
                "x": center["x"], "y": center["y"], "provenance": prov(MANUAL, CORE, TABLE, status="observed"),
            }]},
            "provenance": prov(MANUAL, CORE, TABLE, RUNTIME, status="observed"),
        })
    return {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {"id": MACHINE, "name": "World Poker Tour", "manufacturer": "Stern", "year": 2006, "kind": "physical_pinball", "ipdb_id": 5134, "opdb_id": "G5poe-MQrb5", "playfield": {"width": 952, "height": 2250, "units": "vpx", "provenance": prov(TABLE)}},
        "coverage": {"status": "partial", "missing": ["mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"], "dimensions": {
            "catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "observed", "physical_wiring": "conflicted",
            "mechanisms": "observed", "variant_coverage": "observed", "recreation_knowledge": "observed", "spatial_placement": "conflicted",
        }},
        "controller": {"platform": "pinmame.sam", "inversion_applied_by_emulator": True},
        "drivers": drivers,
        "inputs": input_records(seed, spatial["objects"], switch_rows),
        "outputs": output_records(seed, spatial["objects"], coil_rows, lamp_rows),
        "displays": displays, "mechanisms": mechanism_records(seed), "relationships": [],
        "sources": sources(seed, spatial), "knowledge": {"path": KNOWLEDGE.relative_to(ROOT).as_posix(), "status": "partial"},
        "conflicts": [
            {"id": "conflict.sw54-fitment", "path": "inputs.switch.54", "description": "Factory grid, switch wiring schematic and left ramp assembly identify SW54 as Left Ramp Made, while the separate transfer trough assembly also labels its paired transmitter/receiver beam SW54; two table handlers assert switch 54 for ramp and scoop. Each transmitter/receiver pair forms one beam, not two switches. Exact electrical sharing/fitment is unknown. Resolution path: inspect both installed opto harnesses and trace each signal to its switch-matrix return, then trigger each beam separately in the ROM Switch Test.", "source_refs": [MANUAL, SCRIPT, TABLE]},
            {"id": "conflict.sw56-construction", "path": "inputs.switch.56", "description": "Factory grid on PDF p.6 specifies SW56 OPTO PAIR above left VUK; the separate switch-location drawing's footnote on PDF p.7 describes SW56 as a cabinet hanger bracket and contact wire. Cannot specify factory contact construction until resolved. Resolution path: inspect the installed SW56 assembly and trace its wire/PCB number back to the matrix harness; a standalone emulator pulse cannot identify contact construction.", "source_refs": [MANUAL, SCRIPT]},
            {"id": "conflict.q32-coil", "path": "outputs.coil.32", "description": "Factory coil chart p.10 and board diagram p.123 print Q32 26-1200 / 090-5044-ND while the specific down-post assembly sheet p.118 prints 25-1240 / 090-5034-ND. The p.10 brown feed is separately resolved as a chart error by p.123 and the ROM's orange board feed. Physical coil fitment remains open. Resolution path: read the installed Q32 coil's sleeve marking or a revision-controlled Stern bill of materials for the down-post assembly.", "source_refs": [MANUAL, MANUAL_ASSEMBLY, RUNTIME_COIL]},
        ],
    }


def knowledge(seed: dict) -> str:
    return f"""# World Poker Tour (Stern, 2006)

Coverage: **partial**. The full public address space and factory wiring are recorded and all fourteen playfield card-display blocks are located as observed. SW54/SW56 fitment, Q32's installed coil part, sensor contact construction/polarity, and several socket and mechanism placements still prevent author-ready status.

## Identity and source order

All 46 pinned `wpt_*` drivers represent firmware/language versions of the same 2006 SAM game. The factory manual is authoritative for device parts, wiring, and physical mechanisms; the pinned known-working VPX v2.3.1 script explains ball routes and controller causality; PinMAME defines the public namespace. A fresh Switch Test on the verified revision-8371478 native DLL independently confirms SW3, SW21 and SW63 labels and their active public level. ROM switching alone does not prove a factory sensor's normal contact state. Bulletin 165 identifies a rule change: before v1.11, three dropped targets during serve auto-launched the ball; v1.11 and later spot the targets without an automatic launch. Recreate that behavior by ROM revision, rather than adding hardware.

Stern Service Bulletin 163 (July 24 2006, p.1) identifies unstable flash on some CPU/Sound PCBs as a cause of game resets or indefinitely extended multiball; affected machines receive replacement board 520-5246-00. This is a service intervention on the same WPT hardware, not another playfield edition. Bulletin 164 (August 22 2006, pp.1–2) describes SAM code update and backup: CPU/Sound DIP #8 enables the update menu, then reset and the USB 1.1 port are used. Firmware and language changes remain driver variants, not new physical table editions.

## Ball transport and banked targets

Four ball seats SW18–SW21 are ordered left to right, with an extra stacking opto SW22. Q1 kicks one ball to shooter switch SW23. Player plunge or Q2 auto-launch sends it into play; a separate shooter-lane VUK has SW3/Q3 and exit gate SW51. The eject popper is SW49/Q21 and Q21 has its own 50 V step-up board. The left/backpanel VUK is SW55/Q4; SW56 and SW59 observe upper exit/transfer points, but SW56's printed construction conflicts with its chart entry. Maintain actual ball containment through both vertical tubes and the backpanel transfer. A sensor staying occupied after coil fire is a jam, not a successful transfer.

The right and middle four-banks have independent reset coils Q8 and Q7 and optical switches SW4–7 and SW10–13. The left eight-bank has individual optos SW33–40 and two reset coils Q5/Q6, one per four-target lift. Drops latch down until the matching lift raises them; keep each target's own hit state and collide with its raised blade. Weak springs, a bad lift bracket, or a blocked opto can strand a target down.

## Moving assemblies and routes

The Ace-in-the-Hole jail-bar/mouse-trap assembly uses Q12 to lift and Q19 to latch. SW57 reports bash, SW58 rest, and SW63 up. The bar and latch are physically distinct moving parts; move collision geometry with them and hold a sensed rest/up state at endpoints. Right ramp SW9 leads to SW52, with Q32 operating its down-post stop. Left ramp Q20 raises a ball-routing post. The factory left ramp made opto is labelled SW54, yet a distinct transfer-trough assembly and the VPX ScoopTrigger handler also claim SW54. Leave that circuit unresolved until a board-level continuity map or discriminating ROM trace establishes whether the labels are a drawing error or intentional shared line.

Four independent flippers use Q13–Q16 and dedicated D9–D16 button/EOS contacts. The two side buttons are double-stacked: halfway press closes lower normally-open D9/D11, full press additionally closes upper normally-open D13/D15. All four EOS D10/D12/D14/D16 are normally closed and open about 1/16 inch into travel. Factory p.129 specifies a 40 ms kick then 1 ms hold pulses every 12 ms, with a fresh kick on high-velocity forced rebound. The older table deliberately comments Q13/Q14 callbacks for SAM fastflips but rotates both upper flippers from its lower callbacks; the 2018 and pinned scripts enable separate upper callbacks. Both reproduce four physical flippers. Each lower slingshot Q17/Q18 is fed by two leaf contacts sharing SW26/SW27. Pop bumper skirt/coil pairs are SW30/Q9, SW31/Q10 and SW32/Q11. The remaining orbit, spinner, target and lane switches are individually enumerated in JSON; contact style stays unknown where the factory chart names only a part number.

## Lighting and display

The factory chart enumerates Q22/Q23 and Q25–Q31 as nine flashers, five on the backpanel. Lamp matrix 1–80 has explicit unused 77; 1/2 are cabinet buttons, 3 is apron, and 67/68/75/76 are backpanel stand-up lamps. GI has four factory circuits on J15: upper playfield six bulbs, left edge/lower-right twelve, backpanel/coin door a production-dependent nine*, and lower-right six. LibPinMAME exposes only aggregate GI 0; circuit-to-output address assignment cannot be invented. The backbox DMD is 128×32. The physical 520-5250-14 LED board has fourteen 5×7 playfield card-display blocks in two rows of seven. Pinned `sam.c` publishes fourteen mini DMD callbacks after the main screen; the table's exact central pixel objects D18 through D473 place the fourteen blocks at observed normalized playfield positions, with the native compatibility mapping preserving their order. Do not flatten their pixels into ordinary matrix lamps.

## Spatial and authority limits

The 952×2250 VPX table gives exact stored object centres and six-place normalized coordinates. Each retained `lN` light and `swN` trigger/wall point is recorded only where its name and factory placement agree in broad region. The fourteen card-display placements use actual central pixel objects whose 5×7 groups and 2×7 board topology were checked against native mapping and the factory diagram. A rendered glow, lightmap helper, or primitive stored offset is not proof of a physical bulb or sensor seat. Missing points include the apron Deal Again lamp 3, GI bulbs, flasher sockets, trough sensors and part of the ball mechanism; no guessed coordinates were filled. Five backpanel flashers and four backpanel matrix lamps are marked outside playfield space.

## Concrete blockers

- SW54 has two physically separate manual assemblies and two VPX assertions; SW56's grid and footnote disagree. Q32's chart/schematic and its specific assembly drawing name different coils. ROM and board schematic settle Q32's orange J6-P10 supply against the chart's brown error, but an installed-coil inspection must settle its part. Confirm factory wiring or inspect installed assemblies.
- Most switch factory contact polarity, especially optos, is not established by the sampled active-high ROM test; a wiring/ROM inversion trace must settle physical normally-closed claims.
- The fourteen playfield card-display centres are now recorded as observed, with manual, PinMAME and VPX source roles separated. Original-machine mounting measurements would improve dimensional accuracy but do not make these modelled centres cabinet displays.
- VPX light/trigger coordinates are modelled centres, not all bulb sockets or sensor contacts. GI, flashers, trough, and complex assemblies require further measured placements before author readiness.

## Evidence

- Factory PDF SHA-256 `{seed['manual_sha256']}`, pp. 6–11, 98–119, 125–126, 166–167; corrected, hashed excerpt files are in `evidence/excerpts/stern/`.
- Pinned known-working script SHA-256 `d44738c5fa4693a8b096f226399f3ea2f81c985a1e780c33d012acf7d2bc390a`; retained 2018 VPX SHA-256 `baa4e6e2ec618ed667afc397dea2ee6cdc5c444f811395b42dd537cfec98c443`.
- Verified pinned native DLL SHA-256 `{PINNED_LIBRARY_SHA256}`; fresh wpt_140a Switch Test trace SHA-256 `{PINNED_SWITCH_TRACE_SHA256}` and Single Coil Test trace SHA-256 `{PINNED_COIL_TRACE_SHA256}`. Their raw trace fields record the library hash, exact committed scenario hash, and null failure. The older `ca33d8fd` traces are retained as diagnostics from a stale build, not revision-8371478 evidence. ROM archive SHA-256 `b4f98abae8cecb80a603285357c39688182b90ef376c46c80de5facb4e302463`.
- Stern service bulletins 163, 164 and 165 SHA-256 `da0f791a94e0c02cac1ad7288d41dcbc4da916232be42c8e756e3e70b350ae49`, `b7d0f5274dd0477f727a8f4fa0d7388821f826f112b2267a3d7b2bfc3c5ecb28`, and `40cf83f3109c7adcdfffebebaa16022f18597da12ebcbcfcee3b7f601fbe042c` respectively; official page and download URLs are retained in the external manual manifest.
"""


def audit(definition: dict, spatial: dict) -> dict:
    unresolved = [x["id"] for x in definition["conflicts"]]
    missing = [x["id"] for group in ("inputs", "outputs", "displays") for x in definition[group] if x.get("availability", "used") in {"used","optional"} and "spatial" not in x]
    return {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE, "promotion": "partial",
        "table_sha256": spatial["table_sha256"], "extraction_manifest_sha256": spatial["table_manifest_sha256"],
        "coordinates": "x=(raw_x-0)/952, y=(raw_y-0)/2250; six-decimal repository helper values; player view, y rear to apron",
        "source_seed_sha256": sha(SPATIAL_PATH), "manual_sha256": definition["sources"][0]["sha256"],
        "located_observations": sum("placements" in x.get("spatial", {}) for group in ("inputs","outputs","displays") for x in definition[group]),
        "missing_spatial_ids": missing, "unresolved_conflict_ids": unresolved,
        "projection_classes": {"exact_named_vpx_object_center": "observed only", "manual_drawing_projection": "not used", "cabinet_or_service": "not applicable", "virtual_or_unused": "not applicable"},
        "reason": "Unresolved SW54/SW56 and Q32 fitment, GI/flasher/socket and mechanism geometry; fourteen card-display block centres are located as observed.",
    }


def verify_runtime_content(trace: dict, scenario: Path, snapshots: int) -> None:
    """Reject a trace whose raw run fields do not prove the pinned replay."""
    if (trace.get("failure") is not None or trace.get("library_sha256") != PINNED_LIBRARY_SHA256
            or trace.get("game") != "wpt_140a" or trace.get("scenario", {}).get("sha256") != sha(scenario)
            or len(trace.get("snapshots", [])) != snapshots):
        raise ValueError("untrusted pinned native/scenario runtime provenance")


def verify_external(seed: dict, spatial: dict) -> None:
    roots = {
        "PINMAME_MANUALS_ROOT": ("by-machine/stern.world-poker-tour.2006/World_Poker_Tour_Manual.pdf", seed["manual_sha256"]),
        "PINMAME_VPX_SOURCES_ROOT": ("stern/world-poker-tour-2006/wpt-062018a/wpt 062018a.vpx", spatial["table_sha256"]),
        "PINMAME_REVIEW_ARTIFACTS_ROOT": ("stern.world-poker-tour.2006/session-20260930/wpt-switch-test-pinned-frames-run.json", PINNED_SWITCH_TRACE_SHA256),
    }
    for env, (relative, expected) in roots.items():
        if value := os.environ.get(env):
            target = Path(value) / relative
            if not target.is_file() or sha(target) != expected:
                raise ValueError(f"{env}: missing or wrong retained artifact {target}")
    if value := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        alternate = Path(value) / "stern/world-poker-tour-2006/world-poker-tour-stern-2006/World Poker Tour (Stern 2006).vpx"
        if not alternate.is_file() or sha(alternate) != "92a9720af51c825c9603d9dc78acc2423b7f86c907e1c4a6e92393156a22d9b8":
            raise ValueError(f"PINMAME_VPX_SOURCES_ROOT: missing or wrong retained artifact {alternate}")
    if value := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        session = Path(value) / "stern.world-poker-tour.2006/session-20260930"
        for filename, expected, scenario_name, snapshots in (
            ("wpt-switch-test-pinned-frames-run.json", PINNED_SWITCH_TRACE_SHA256, f"{STEM}-switch-test.json", 14),
            ("wpt-coil-diagnostic-pinned-frames-run.json", PINNED_COIL_TRACE_SHA256, f"{STEM}-coil-sweep.json", 40),
        ):
            target = session / filename
            if not target.is_file() or sha(target) != expected:
                raise ValueError(f"PINMAME_REVIEW_ARTIFACTS_ROOT: missing or wrong retained artifact {target}")
            trace = json.loads(target.read_text(encoding="utf-8"))
            scenario = ROOT / "tools/harness-scenarios/stern" / scenario_name
            try:
                verify_runtime_content(trace, scenario, snapshots)
            except ValueError as exc:
                raise ValueError(f"PINMAME_REVIEW_ARTIFACTS_ROOT: {target}: {exc}") from exc
        native = Path(value).resolve().parent / "builds/pinmame-8371478/Release/pinmame64.dll"
        if not native.is_file() or sha(native) != PINNED_LIBRARY_SHA256:
            raise ValueError(f"PINMAME_REVIEW_ARTIFACTS_ROOT: missing or wrong verified pinned native library {native}")
    if value := os.environ.get("PINMAME_SOURCE_ROOT"):
        checkout = Path(value)
        actual = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, capture_output=True, text=True, check=True).stdout.strip()
        if actual != seed["pinmame_revision"]:
            raise ValueError(f"PINMAME_SOURCE_ROOT: expected {seed['pinmame_revision']}, got {actual}")
    if value := os.environ.get("PINMAME_SCRIPTS_ROOT"):
        target = Path(value) / "World Poker Tour (Stern 2006) v.2.3.1.vbs"
        if not target.is_file() or sha(target) != "d44738c5fa4693a8b096f226399f3ea2f81c985a1e780c33d012acf7d2bc390a":
            raise ValueError(f"PINMAME_SCRIPTS_ROOT: missing or wrong retained artifact {target}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    spatial = json.loads(SPATIAL_PATH.read_text(encoding="utf-8"))
    verify_external(seed, spatial)
    definition = build(seed, spatial)
    artifacts = {
        DEST: canonical_bytes(definition),
        KNOWLEDGE: knowledge(seed).encode("utf-8"),
        AUDIT: canonical_bytes(audit(definition, spatial)),
    }
    for path, wanted in artifacts.items():
        if args.check:
            if not path.exists() or path.read_bytes() != wanted:
                raise SystemExit(f"drift or missing artifact: {path}")
        else:
            if DEST.parent.name == "author-ready" or (ROOT / f"machines/author-ready/stern/{STEM}.json").exists():
                raise SystemExit("refusing to overwrite author-ready artifact")
            write_bytes(path, wanted)
    print(f"{MACHINE}: {'checked' if args.check else 'wrote'} partial definition and audit")


if __name__ == "__main__":
    main()
