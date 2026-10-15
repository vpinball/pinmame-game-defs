#!/usr/bin/env python3
"""Reproduce Mystery Castle's physical contract from reviewed, pinned evidence.

The facts file holds exact retained-object coordinates and artifact identities; the
tables below are the curator's complete, visually checked manual transcriptions.
Regeneration needs no external archive. Optional evidence roots are verified by the
focused tests, and --check refuses changed transcriptions as well as output drift.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pinmame_game_defs.conflicts import unresolved_conflicts
from build_external_evidence_manifest import canonical_bytes
import drawing_callouts

MACHINE_ID = "alvin-g.mystery-castle.1993"
SLUG = "mystery-castle-1993"
PIN = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
MANUAL = "manual.mystery-castle.9fa91108ba60"
SCRIPT = "vpx-script.mystery-castle-210"
TABLE = "vpx-table.mystery-castle-210"
CORE = "pinmame.alvg.97aa922bf8e4"
LIBRARY = "vpm.alving.63a758ecb79e"
EXCERPTS = f"evidence/excerpts/{MACHINE_ID}"
CALLOUTS = f"tools/seeds/alvin-g/{SLUG}-callouts.json"
DRAWING = "drawing.mystery-castle-lamps"

# Empty entries are literally blank cells, not an extrapolation from a sibling.
SWITCH_LABELS = [
    "LEFT COIN CHUTE", "RIGHT COIN CHUTE", "CENTER COIN CHUTE", "EXTRA COIN CHUTE", "SLAM", "", "L FLIPPER BUTTON", "R. FLIPPER BUTTON",
    "GAME START", "TILT", "", "", "", "SHOOTER BUTTON", "TEST PLUS", "TEST MINUS",
    "OUTHOLE", "BALL TROUGH", "", "", "SHOOTER LANE", "", "TUNNEL", "MEGAMODE",
    "BUMPER LEFT", "BUMPER RIGHT", "SLING LEFT", "SLING RIGHT", "CATWALK ENTER", "CATWALK EXIT", "TOWER ENTER", "TOWER EXIT",
    "CASTLE C", "CASTLE A", "CASTLE S", "CASTLE T", "CASTLE L", "CASTLE E", "BRIDGE", "",
    "TRAP T", "TRAP R", "TRAP A", "TRAP P", "LEFT RETURN", "LEFT OUTLANE", "RIGHT RETURN", "RIGHT OUTLANE",
    "STATUE TOP", "STATUE MIDDLE", "STATUE BOTTOM", "CHANGE ITEM", "DUNGEON", "BALLROOM", "SECRET DOOR", "",
] + [""] * 40

LAMP_LABELS = [
    "HUNT AGAIN", "SCEPTER", "CRYSTAL BALL", "BELL", "GOBLET", "POTION", "CANDELABRUM", "PANDORA'S BOX",
    "GOLD COINS", "JESTER'S HAT", "COAT OF ARMS", "MIRROR", "DRAGON IDOL", "SKULL", "PAINTING", "CROWN",
    "STATUE TOP", "STATUE MIDDLE", "STATUE BOTTOM", "MEGAMODE BOTTOM", "? BOTTOM", "CATAPULT", "LEFT RETURN", "LEFT OUTLANE",
    "CASTLE C", "CASTLE A", "CASTLE S", "CASTLE T", "CASTLE L", "CASTLE E", "RIGHT RETURN", "RIGHT OUTLANE",
    "TRAP T", "TRAP R", "TRAP A", "TRAP P", "MEGAMODE TUNNEL", "? TUNNEL", "BUMPER LEFT", "BUMPER RIGHT",
    "JACKPOT BRIDGE", "JACKPOT DUNGEON", "JACKPOT TOWER", "JACKPOT BALLROOM", "JACKPOT CATWALK", "SPECIAL", "GAME START", "SHOOTER BUTTON",
    "ITEM BRIDGE", "ITEM DUNGEON", "ITEM TOWER", "ITEM BALLROOM", "ITEM CATWALK", "EXTRA BALL", "SECRET DOOR", "CHANGE ITEM",
    "BBOARD BRIDGE", "BBOARD DUNGEON", "BBOARD TOWER", "BBOARD BALLROOM", "BBOARD CATWALK", "", "", "",
] + [""] * 32

# No. | fuse | literal description | power | return | connector | part.
# Q21..Q52 are printed even on the four otherwise blank rows.
COIL_ROWS = """1|F13|SECRET DOOR|VIO/BLU|VIO/GRY|H6-9|CLL-004
2|F14|BUMPER LEFT|VIO/GRN|VIO/RED|H6-8|CLL-006
3|F14|BUMPER RIGHT|VIO/GRN|VIO/ORG|H6-7|CLL-006
4|F15|SLING LEFT|VIO/BLK|VIO/YEL|H6-5|CLL-007
5|F15|SLING RIGHT|VIO/BLK|VIO/GRN|H6-4|CLL-007
6|F16|MEGAMODE|VIO/YEL|VIO/BLU|H6-3|CLL-007
7||||||
8||||||
9|F17|PLUNGER|VIO/ORG|BRN/BLK|H6-17|CLL-009
10|F14|CATAPULT|VIO/GRN|BRN/RED|H6-16|CLL-006
11|F13|DTS C-A-S|VIO/BLU|BRN/ORG|H6-15|CLL-004
12|F13|DTS T-L-E|VIO/BLU|BRN/YEL|H6-14|CLL-004
13|F14|OUTHOLE|VIO/GRN|BRN/GRN|H6-13|CLL-006
14|F15|KNOCKER|VIO/BLK|BRN/BLU|H6-12|CLL-007
15|F19|FLASHER RELAY|RED/VIO|BRN/VIO|H6-11|
16|F18|FIELD RELAY BOT|RED/GRN|BRN/GRY|H6-10|
17|F19|FLASHER DUNGEON|VIO/WHT|BLK/BRN|H7-8|
18|F19|FLASHER BRIDGE|VIO/WHT|BLK/RED|H7-7|
19|F19|FLASHER TOWER|VIO/WHT|BLK/ORG|H7-6|
20|F19|FLASHER BALLROOM|VIO/WHT|BLK/YEL|H7-5|
21|F19|FLASHER SECRET|VIO/WHT|BLK/GRN|H7-4|
22|F19|FLASHER CATWALK|VIO/WHT|BLK/BLU|H7-3|
23|F19|FLASHER PIT|VIO/WHT|BLK/VIO|H7-2|
24|F19|FLASHER BACKBOX|VIO/WHT|BLK/GRY|H7-1|
25||||||
26|F18|FIELD RELAY TOP|RED/GRN|BLU/BLK|H7-16|
27|F18|FLIPPER RELAY|RED/GRN|BLU/VIO|H7-15|
28||||||
29|F18|BOX RELAY NORM|RED/GRN|BLU/BRN|H7-12|
30|F26|EJECT 2 PLAYFIELD|RED/GRN|BLU/RED|H7-11|CLL-004
31|F18|BACK RELAY DOOM|RED/GRN|BLU/ORG|H7-10|
32|F18|GATE|RED/GRN|BLU/YEL|H7-09|CLL-006"""

SWITCH_PARTS = {
    5: "SLM-001", 7: "LSW-001", 8: "LSW-001", 9: "CBB-001", 10: "PLM-001", 14: "SHB-001", 15: "TSW-001", 16: "TSW-001",
    17: "MSW-011", 18: "MSW-013", 21: "SBA-001", 23: "MSW-009", 24: "MSA-009", 25: "CBB-001", 26: "CBB-001", 27: "DTR-001", 28: "DTR-001",
    **{n: "MSW-009" for n in (29, 30, 31, 32, 39)}, **{n: "DTS-001" for n in range(33, 39)},
    **{n: "STS-002" for n in range(41, 45)}, **{n: "SBA-001" for n in range(45, 49)},
    **{n: "STS-001" for n in (49, 50, 51)}, 52: "STR-004", **{n: "SBA-001" for n in (53, 54, 55)},
}
ASSEMBLIES = {1: "AKN-001", 2: "ABM-004", 3: "ABM-004", 4: "ABK-008", 5: "ABK-008", 6: "AVK-001", 9: "CKA-002", 10: "AKN-001", 11: "ADT-006", 12: "ADT-007", 13: "ABR-001", 14: "AKN-001", 30: "ABR-002", 32: "ADV-001"}
FLASHER_QUANTITIES = {17: 2, 18: 2, 19: 2, 20: 1, 21: 1, 22: 2, 23: 1, 24: 4}
CABINET_SWITCHES = set(range(1, 11)) | {14, 15, 16}
CABINET_LAMPS = {47, 48}
LAMP_555 = set(range(2, 20)) | set(range(25, 31)) | {39, 40, 47, 48}
SWITCH_STROBES = [("HP4-1", "WHT/BRN"), ("HP4-2", "WHT/RED"), ("HP4-3", "WHT/ORG"), ("HP4-4", "WHT/YEL"), ("HP4-5", "WHT/GRN"), ("HP4-6", "WHT/BLU"), ("HP4-7", "WHT/VIO"), ("HP4-8", "WHT/GRY"), ("HP4-9", "ORG/RED"), ("HP4-10", "ORG/BLK"), ("HP4-13", "ORG/YEL"), ("HP4-14", "ORG/GRN")]
SWITCH_RETURNS = [("HP5-9", "GRN/BRN"), ("HP5-7", "GRN/RED"), ("HP5-6", "GRN/ORG"), ("HP5-5", "GRN/YEL"), ("HP5-4", "GRN/YEL"), ("HP5-3", "GRN/BLU"), ("HP5-2", "GRN/VIO"), ("HP5-1", "GRN/GRY")]
LAMP_STROBES = [(f"HP9-{pin}", wire) for pin, wire in zip((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), ("RED/BRN", "RED/BLK", "RED/ORG", "RED/YEL", "RED/GRN", "RED/BLU", "RED/VIO", "RED/GRY", "GRY/RED", "GRY/BLK", "GRY/YEL", "GRY/GRN"))]
LAMP_RETURNS = [(f"HP2-{pin}", wire) for pin, wire in zip((1, 2, 3, 4, 5, 6, 8, 9), ("YEL/BRN", "YEL/RED", "YEL/ORG", "YEL/BLK", "YEL/GRN", "YEL/BLU", "YEL/VIO", "YEL/GRY"))]


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def prov(*refs, status="validated"):
    return {"source_refs": list(dict.fromkeys(refs)), "status": status}


def na(reason, *refs):
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def alias(namespace, value):
    return {"namespace": namespace, "value": str(value)}


def matrix_wiring(address, strobes, returns, lamp=False):
    strobe, row_wire = strobes[(address - 1) // 8]
    ret, col_wire = returns[(address - 1) % 8]
    # Schematics DOC-003 / DOC-004 settle the printed matrix's header errors.
    if not lamp:
        if (address - 1) % 8 == 4:
            col_wire = "GRN/BLK"
        if (address - 1) // 8 == 10:
            strobe = "HP4-11"
        if (address - 1) // 8 == 11:
            strobe = "HP4-12"
    row = {"board": "PCA-009 CPU/COMB #2", "drive_connection": strobe, "drive_wire": row_wire.replace("/", "-"), "return_connection": ret, "return_wire": col_wire.replace("/", "-")}
    if lamp:
        row["driver_transistor"] = f"Q{12 - (address - 1) // 8}/Q{13 + (address - 1) % 8}"
    return row


def excerpts():
    region = "Visually transcribed from native-resolution renders of the retained scan. Blank cells are `[blank]`; line breaks within cells are flattened; slash-separated source wire spelling is preserved. Matrix headings are literal, even where the schematic corrects them.\n\n"
    sw = ["# Switch matrix and location list", "", "PDF 30, printed 3-6: complete 96-cell matrix; PDF 31, printed 3-7: complete location/part list (01-55).", "", region,
          "| Return column | Printed header | Wire |", "| --- | --- | --- |"]
    sw += [f"| {i + 1} | {conn} | {wire} |" for i, (conn, wire) in enumerate(SWITCH_RETURNS)]
    sw += ["", "| Strobe row | Printed header | Wire |", "| --- | --- | --- |"]
    sw += [f"| {i + 1} | {conn} | {wire} |" for i, (conn, wire) in enumerate(SWITCH_STROBES)]
    sw += ["", "| No. | Matrix description | Location-list description | Part no. |", "| --- | --- | --- | --- |"]
    for n, label in enumerate(SWITCH_LABELS, 1):
        location = label
        if n == 15:
            location = "TEST MINUS"
        elif n == 24:
            location = "MEGAMODE EJECT"
        elif n in (50, 51):
            location = "STATUE MID" if n == 50 else "STATUE BOT"
        sw.append(f"| {n:02} | {label or '[blank]'} | {location or '[blank]' if n <= 55 else '[not listed]'} | {SWITCH_PARTS.get(n, '[blank]') if n <= 55 else '[not listed]'} |")
    sw += ["", "Printed matrix row 36 is damaged at CASTLE T; the following location list and DOC-003 schematic both print CASTLE T. Matrix HP5-4 repeats GRN/YEL, while DOC-003 and the cabinet schematic print GRN/BLK. Matrix HP4-13/-14 for strobes 11/12 disagree with DOC-003 and the board connector HP4-11/-12. Structured wiring follows the agreeing schematics. The location list prints TEST MINUS twice (15 and 16); matrix 15, schematic 15 and the coin-door controls establish 15 is Plus. These are settled printing defects, not open machine conflicts.", ""]
    lamps = ["# Lamp matrix and lamp-location list", "", "PDF 28, printed 3-4: complete 96-cell matrix; PDF 29, printed 3-5: complete 61-entry lamp/socket list.", "", region,
             "| Return column | Transistor | Connector | Wire |", "| --- | --- | --- | --- |"]
    lamps += [f"| {i + 1} | Q{i + 13} | {conn} | {wire} |" for i, (conn, wire) in enumerate(LAMP_RETURNS)]
    lamps += ["", "| Strobe row | Transistor | Connector | Wire |", "| --- | --- | --- | --- |"]
    lamps += [f"| {i + 1} | Q{12 - i} | {conn} | {wire} |" for i, (conn, wire) in enumerate(LAMP_STROBES)]
    lamps += ["", "| No. | Matrix description | Location-list description | Lamp no. | Socket part no. |", "| --- | --- | --- | --- | --- |"]
    for n, label in enumerate(LAMP_LABELS, 1):
        location = label.replace("JESTER'S HAT", "JESTER").replace("STATUE MIDDLE", "STATUE MID").replace("STATUE BOTTOM", "STATUE BOT").replace("BBOARD", "BB")
        socket = "LBK-011" if n in LAMP_555 else "LBK-010"
        if n in {1, 42, 55}:
            socket = "LBK-004"
        if n in {57, 58, 59, 60, 61}:
            socket = "LBK-005"
        if n in {39, 40, 47, 48}:
            socket = "[blank]"
        lamps.append(f"| {n:02} | {label or '[blank]'} | {location or '[blank]' if n <= 61 else '[not listed]'} | {'#555' if n in LAMP_555 else '#44' if label else '[not listed]'} | {socket if n <= 61 else '[not listed]'} |")
    lamps += ["", "Location-list footer: #44 LAMP, BAYONET BASE — LMP-002; #555 LAMP, WEDGE BASE — LMP-003. BB/BBOARD denotes the five playfield billboard lamps, named BILLBOARD in DOC-004 and drawn at the playfield signs. The drawing places 47 and 48 beyond the front playfield frame at the Start and Shooter buttons. Matrix cells 62-96 are blank. No printed quantity greater than one is claimed for these controlled lamps.", ""]
    coils = ["# Coil table and assembly-location list", "", "PDF 32, printed 3-8: entire Coil Table. PDF 33, printed 3-9: all assembly numbers accompanying the same 32 descriptions.", "", region,
             "| Fuse | Coil no. | Description | Transistor | Power | Return | Connector | Part no. | Assembly part no. (3-9) |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for line in COIL_ROWS.splitlines():
        number, fuse, label, power, ret, conn, part = line.split("|")
        n = int(number)
        coils.append("| " + " | ".join((fuse or "[blank]", number, label or "[blank]", f"Q{n + 20}", power or "[blank]", ret or "[blank]", conn or "[blank]", part or "[blank]", ASSEMBLIES.get(n, "[blank]"))) + " |")
    coils += ["", "The location list calls 29 BACK RELAY NORM (table: BOX RELAY NORM). The schematic DOC-002 labels 16 Top and 26 Bottom, opposite FIELD RELAY BOT/TOP in this table. The physical top/bottom assignment is unresolved; its literal branch counts are transcribed separately without assigning validated per-address quantities. Coil 6's generic AVK-001 assembly page (PDF 42/5-3) lists CLL-004 while the machine-specific coil table prints CLL-007; both readings are retained and the fitted machine-specific coil-table number is used. Table fuse F26 for 30 is a second protection stage: DOC-002 feeds the coil from F18 through F26. Blank coils 7,8,25,28 have no fitted load in the machine wiring.", ""]
    return {"switches.md": "\n".join(sw), "lamps.md": "\n".join(lamps), "coils.md": "\n".join(coils)}


def located(identifier, records):
    if not records:
        return None
    state = "candidate" if any(record["status"] == "candidate" for record in records) else "observed"
    return {"status": state, "placements": [{"id": f"{identifier}.p{i}", "role": record["role"], "space": "playfield", "x": record["x"], "y": record["y"], "provenance": prov(TABLE, SCRIPT, status=record["status"])} for i, record in enumerate(records, 1)]}


def build_definition(root, facts):
    inputs, outputs, mechanisms, relationships = [], [], [], []
    for n, raw in enumerate(SWITCH_LABELS, 1):
        used = bool(raw)
        identifier = f"switch.{n:02}"
        label = raw.title() if used else f"Unused Switch {n}"
        row = {"id": identifier, "label": label, "kind": "switch" if used else "virtual", "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": [alias("pinmame.switch", n), alias("manual.address", f"{n:02}")], "availability": "used" if used else "unused", "provenance": prov(MANUAL, CORE, SCRIPT) if used else prov(MANUAL, CORE), "wiring": matrix_wiring(n, SWITCH_STROBES, SWITCH_RETURNS)}
        if used:
            row["normally_closed"] = False
            row["physical"] = {"location": "cabinet or coin door" if n in CABINET_SWITCHES else "playfield", "quantity": 1, "switch_type": "button" if n in {7, 8, 9, 14, 15, 16} else "tilt" if n in {5, 10} else "microswitch" if n in {17, 18, 23, 24, 29, 30, 31, 32, 39} else "leaf", "notes": "DOC-003 draws the fitted matrix contact normally open. The driver reads the matrix complemented and declares no inverted-switch mask; public 1 is the closed contact."}
            if n in SWITCH_PARTS:
                row["physical"]["part_number"] = SWITCH_PARTS[n]
            if n in {7, 8}:
                row["physical"]["notes"] += f" PinMAME overwrites this matrix copy from cabinet-button address {116 if n == 7 else 114} every update. Drive that flipper-column address, never this copy. This is a button contact, not an EOS input."
            if n == 15:
                row["physical"]["notes"] += " The location list's repeated TEST MINUS at 15 is corrected by the matrix, wiring schematic and coin-door controls: 15 is Volume/Test Plus."
            if n in CABINET_SWITCHES:
                row["roles"] = ["cabinet" if n not in {15, 16} else "service"]
                row["spatial"] = na("cabinet_or_service", MANUAL, CORE)
            else:
                position = located(identifier, facts["switches"].get(str(n), []))
                if position:
                    row["spatial"] = position
                if n in {17, 18}:
                    row["physical"]["notes"] += " Position is a projection onto the retained trough/outhole model; it does not locate the under-apron switch bracket."
        else:
            row["physical"] = {"notes": "Blank matrix cell; DOC-003 labels this circuit N.U.; no physical switch is fitted."}
            row["spatial"] = na("unused", MANUAL, CORE)
        inputs.append(row)

    for n, label in ((-7, "Enter / Begin Test"), (-6, "Exit / Service Credits"), (-5, "Flasher/Ticket Sense Host Override")):
        row = {"id": f"switch.direct-{abs(n)}", "label": label, "kind": "virtual" if n == -5 else "switch", "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": [alias("pinmame.switch", n)], "availability": "optional" if n == -5 else "used", "roles": ["service"], "physical": {"notes": "The active CoinDoorSwitches_Read implementation, rather than its disabled manual-order block, is the public contract."}, "spatial": na("virtual" if n == -5 else "cabinet_or_service", CORE, LIBRARY, MANUAL), "provenance": prov(CORE, LIBRARY, MANUAL)}
        if n != -5:
            row["normally_closed"] = False
            row["physical"].update({"switch_type": "button", "location": "coin door", "quantity": 1})
            row["provenance"]["source_refs"].append("runtime.mystcasa-service-buttons")
        else:
            row["physical"]["notes"] += " No physical ticket switch is fitted. The host's -5 latch is ORed with swAvail1 (any active 17-24 flasher byte) at CPU PB5; the emulator also feeds solenoid 15 into PB3. This optional diagnostic override is not a ball sensor or a cabinet button."
        inputs.append(row)

    for n in range(113, 121):
        fitted = n in {114, 116}
        side = "Right" if n == 114 else "Left"
        row = {"id": f"switch.flipper-column-{n}", "label": f"{side} Flipper Button" if fitted else f"Unused Flipper Column Position {n}", "kind": "switch" if fitted else "virtual", "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": [alias("pinmame.switch", n)], "availability": "used" if fitted else "unused", "spatial": na("cabinet_or_service" if fitted else "unused", CORE, LIBRARY, MANUAL), "provenance": prov(CORE, LIBRARY, MANUAL), "physical": {"notes": "Internal column 15, published as 15*8+row-7. Only lower button bits 1 and 3 participate in this game's FLIP_SWNO(7,8); no EOS simulation or independent upper button is declared."}}
        if fitted:
            row.update({"normally_closed": False, "roles": ["cabinet", "flipper_button"], "physical": {"quantity": 1, "location": f"{side.lower()} cabinet flipper button", "switch_type": "button", "part_number": "LSW-001", "notes": f"Consumer-drive address. core_updateSw copies it into matrix switch {8 if n == 114 else 7}; do not drive the copy. The left button supplies a shared return for the lower-left flipper and, through the lower flipper's normally-open activator contact, the upper-left flipper. There is no independent upper-left button."}})
        inputs.append(row)

    for n, raw in enumerate(LAMP_LABELS, 1):
        used = bool(raw)
        identifier = f"lamp.{n:02}"
        row = {"id": identifier, "label": raw.title() if used else f"Unused Lamp {n}", "kind": "lamp" if used else "virtual", "binding": {"group": "pinmame.output.lamp", "device": n}, "aliases": [alias("pinmame.lamp", n), alias("manual.address", f"{n:02}")], "availability": "used" if used else "unused", "wiring": matrix_wiring(n, LAMP_STROBES, LAMP_RETURNS, lamp=True), "provenance": prov(MANUAL, CORE, SCRIPT) if used else prov(MANUAL, CORE)}
        if used:
            row["physical"] = {"location": "cabinet button" if n in {47, 48} else "playfield", "quantity": 1, "part_number": "LMP-003" if n in LAMP_555 else "LMP-002", "notes": f"The lamp-location list specifies {'#555 wedge-base' if n in LAMP_555 else '#44 bayonet-base'}. Runtime binding is vpmMapLights AllLights using each member's TimerInterval, not its name."}
            if n >= 57:
                row["label"] = raw.replace("BBOARD", "BILLBOARD").title()
                row["physical"]["notes"] += " BB/BBOARD is BILLBOARD on DOC-004: this bulb illuminates a playfield sign, as the location drawing shows."
            if n in CABINET_LAMPS:
                row["roles"] = ["cabinet"]
                row["spatial"] = na("cabinet_or_service", MANUAL, SCRIPT)
            else:
                position = located(identifier, facts["lamps"].get(str(n), []))
                if position:
                    row["spatial"] = position
                row["physical"]["notes"] += " Insert-light anchors identify illuminated inserts, not surveyed under-playfield sockets. Factory drawing callouts check the corresponding feature locations separately."
        else:
            row["spatial"] = na("unused", MANUAL, CORE)
            row["physical"] = {"notes": "Blank matrix cell and N.U. lamp branch on DOC-004; service activity cannot establish fitment."}
        outputs.append(row)

    for line in COIL_ROWS.splitlines():
        number, fuse, raw, power, ret, conn, part = line.split("|")
        n = int(number)
        used = bool(raw)
        kind = "flasher" if 17 <= n <= 24 else "gi" if n in {16, 26, 29, 31} else "relay" if n in {15, 27} else "coil" if used else "virtual"
        identifier = f"solenoid.{n:02}"
        label = raw.title() if used else f"Unused Solenoid {n}"
        if n == 16:
            label = "GI Relay 16 (Region Unresolved)"
        elif n == 26:
            label = "GI Relay 26 (Region Unresolved)"
        row = {"id": identifier, "label": label, "kind": kind, "binding": {"group": "pinmame.output.solenoid", "device": n}, "aliases": [alias("pinmame.solenoid", n), alias("manual.address", f"{n:02}")], "availability": "used" if used else "unused", "provenance": prov(MANUAL, CORE, SCRIPT) if used else prov(MANUAL, CORE), "physical": {"notes": f"Coil table transistor Q{20 + n}. " + (f"Printed fuse {fuse}. " if fuse else "")}, "wiring": {"board": "PCA-009 CPU/COMB #2", "driver_transistor": f"Q{20 + n}"}}
        if used:
            row["provenance"]["source_refs"].append("runtime.mystcasa-coil-service")
            row["wiring"].update({"power_wire": power.replace("/", "-"), "return_wire": ret.replace("/", "-"), "return_connection": conn})
            if part:
                row["physical"]["part_number"] = part
            if n in ASSEMBLIES:
                row["physical"]["assembly_part_number"] = ASSEMBLIES[n]
            if n in FLASHER_QUANTITIES:
                row["physical"].update({"quantity": FLASHER_QUANTITIES[n], "location": "backbox" if n == 24 else "playfield", "part_number": "#47"})
                row["physical"]["notes"] += "DOC-002 specifies #47 playfield flash lamps and #906 insert flash lamps; quantity is the number of drawn bulb symbols."
                if n == 24:
                    row["physical"]["part_number"] = "#906"
            elif kind == "coil":
                row["physical"].update({"quantity": 1, "location": "cabinet" if n == 14 else "playfield"})
            if n in {14, 15, 27, 29, 31, 24}:
                row["roles"] = ["cabinet"]
                row["spatial"] = na("cabinet_or_service", MANUAL, CORE)
            elif n in {16, 26}:
                row["provenance"]["status"] = "conflicted"
                row["physical"]["location"] = "playfield region unresolved"
                row["physical"]["notes"] += "DOC-002 labels 16 Top and 26 Bottom; its candidate controlled branches are 13 clear plus 13 red top-playfield bulbs at 16 and 12 bottom-playfield bulbs at 26. A further 2-4 coin-door bulbs share the F21 supply before the drawn relay-26 contact and are unswitched supply context, not a relay-controlled cabinet load. The coil table, observed ROM service labels and retained table's LowerGILights/UpperGILights callbacks instead assign 16 Bottom and 26 Top. These incompatible physical-region claims remain unresolved. Neither a per-address bulb quantity nor a top/bottom region is validated; no socket grouping is inferred from proximity. The public callbacks and fitted relay presence remain used."
            else:
                position = located(identifier, facts["solenoids"].get(str(n), []))
                if position:
                    row["spatial"] = position
                if kind == "coil":
                    row["physical"]["notes"] += "Actuator position is projected onto its own mechanism's fixed playfield object; it is not the measured under-playfield coil centre."
            if n in {29, 31}:
                row["physical"]["location"] = "backbox"
                if n == 29:
                    row["physical"]["notes"] += "DOC-002 normal backbox relay 29 feeds two separately fused branches of 12 bulbs each; their BLU/BLU returns go to PP1-11 and PP2-10 respectively."
                    row["physical"]["quantity"] = 24
                else:
                    row["provenance"]["status"] = "candidate"
                    row["physical"]["notes"] += "DOC-002 special backbox relay 31 supplies a dashed group labelled [4/6] BULBS (printed count digit uncertain) returning to PP1-11 and a separate parallel branch drawn with two unlabelled bulb symbols returning to PP2-10. The degraded count digit and the annotation's scope do not establish a total or whether it includes the separate pair, so no quantity is promoted. Both returns are BLU/BLU and are shared with different normal-insert branches; the footer voltage digit is also uncertain between 5 and 6 VAC, with no typed voltage promoted."
            if n == 6:
                row["physical"]["notes"] += "Generic AVK-001 parts list prints CLL-004; the machine-specific table prints CLL-007 and is retained here."
            if n in {2, 3, 4, 5}:
                row["physical"]["notes"] += "The table's corresponding SolCallback is commented out; its native bumper/slingshot physics still reports the switch. This does not make the fitted coil unused."
            if n == 23:
                row["physical"]["notes"] += "The schematic calls the same device Flasher Lock; the matrix/coil table calls it Pit."
        else:
            row["physical"]["notes"] += "No fitted load: blank coil-table row, absent from DOC-002's complete load wiring; this is not inferred from a missing table callback."
            row["spatial"] = na("unused", MANUAL, CORE)
        outputs.append(row)

    for n in range(33, 51):
        live = n in {45, 46, 47, 48}
        right = n in {45, 46}
        assembly = n in {46, 48}
        label = ("Right" if right else "Left / Upper Left") + (" Flipper Assembly Callback" if assembly else " Flipper Paired Synthetic State") if live else f"Unused Solenoid {n}"
        row = {"id": f"solenoid.{n:02}", "label": label, "kind": "coil" if assembly else "virtual", "binding": {"group": "pinmame.output.solenoid", "device": n}, "aliases": [alias("pinmame.solenoid", n)], "availability": "used" if live else "unused", "provenance": prov(CORE, MANUAL, SCRIPT), "physical": {"notes": "core_updateSw fabricates 45/46 together from button 114 and 47/48 together from 116 while relay 27 enables play. They are assembly-drive signals; no independent power/hold-winding timing is published. The table consumes 46/48. Do not interpret the two simultaneous bits as separately measured winding currents." if live else "No ALVG CPU output, extension handler or configured simulator supplies this address; custSol=0 and only 32 CPU driver bits exist."}}
        if assembly:
            row["physical"].update({"quantity": 1 if right else 2, "location": "right lower playfield" if right else "lower and upper left playfield"})
            if right:
                row["physical"]["part_number"] = "CLL-015"
            else:
                row["physical"]["notes"] += " Lower-left coil is CLL-015; upper-left coil is CLL-003. The physical normally-open Upper Flipper Activator on the lower assembly closes the upper branch after lower-flipper motion; the retained table approximates both as simultaneous callbacks."
            row["spatial"] = located(row["id"], facts["solenoids"][str(n)])
        else:
            row["spatial"] = na("virtual" if live else "unused", CORE)
        outputs.append(row)

    def mechanism(identifier, label, kind, actuators, sensors, behavior, assembly=None):
        row = {"id": identifier, "label": label, "kind": kind, "actuators": [f"solenoid.{n:02}" for n in actuators], "sensors": [f"switch.{n:02}" for n in sensors], "behavior": behavior, "provenance": prov(MANUAL, SCRIPT, CORE)}
        if assembly:
            row["assembly_part_number"] = assembly
        mechanisms.append(row)

    mechanism("mech.trough", "Outhole, two-ball trough and shooter feeder", "kicker", [13, 30], [17, 18, 21], "Two balls are supplied and installed (manual 1-3), agreeing with bsTrough.Balls=2; the driver macro's 3/*?*/ simulator parameter is not physical ball count. InitSw(17,18,0,...) puts the outhole before one monitored trough position. A drain enters the stack, 13 transfers it into the trough, and 30 ejects toward the shooter lane (21). The two coils do not directly actuate the sensors; ball movement does. Check outhole and trough jams before forcing another feed.")
    mechanism("mech.shooter", "Automatic shooter", "kicker", [9], [21], "Cabinet shooter button 14 is held by the plunger key; output 9 fires AutoPlunger through vpmSolAutoPlungeS. The modeled plunger is pulled back at initialization. The physical shooter coil is CLL-009 on CKA-002; exact pulse and travel tuning remains recreation-owned.", "CKA-002")
    mechanism("mech.catapult", "Left-outlane catapult / kickback", "kicker", [10], [46], "Output 10 fires CatapultPlunger, which is pulled back at initialization. It returns a ball from the lower-left outlane when the ROM awards the feature; the outlane switch reports the ball independently. The script's solenoid-sound helper parameter is not a measured real-machine pulse width.", "AKN-001")
    mechanism("mech.secret-door", "Secret-door kicker", "kicker", [1], [55], "A ball travels through the secret-door lane (55); output 1 releases the preloaded SecretDoorPlunger. Script plunger objects implement the physical linear kicker, not a motorized door or position sensor. No door-home input exists in the printed inventory.", "AKN-001")
    mechanism("mech.megamode", "Tunnel/subway to Megamode vertical eject", "kicker", [6], [23, 24], "Tunnel entry pulses 23. sw23 then destroys/transfers the ball into sw24 through a modeled subway; the Megamode stack asserts 24 while occupied and output 6 ejects from sw24 at script angle170/strength18. Those values are table tuning, not hardware measurements. Check the subway and eject cup for trapped balls.", "AVK-001")
    for first, last, coil, letters, assembly in ((33, 35, 11, "C-A-S", "ADT-006"), (36, 38, 12, "T-L-E", "ADT-007")):
        mechanism(f"mech.castle-{letters.lower()}", f"CASTLE {letters} three-drop bank", "drop_target_bank", [coil], list(range(first, last + 1)), "Three separate drop targets latch down and report their own switches. The bank's reset coil raises all three together through SolDropUp; no extra bank-down or home sensor is printed. Begin with raised targets; ROM reset coils restore them during startup/play. The retained table header reports that R03 counts four and R02 five drops toward the multiplier, but that header is an unverified ROM-behavior observation, not evidence for fitting fewer than six physical targets.", assembly)
    for sensor, coil, label in ((25, 2, "left pop bumper"), (26, 3, "right pop bumper"), (27, 4, "left slingshot"), (28, 5, "right slingshot")):
        mechanism(f"mech.{label.replace(' ', '-')}", label.title(), "kicker", [coil], [sensor], "Ball impact closes the normally-open scoring switch. The ROM controls the numbered coil; the retained table uses native VPX bumper/slingshot physics and pulses the switch, with its solenoid sound callback commented out. No mechanism home input or moving-position mark is fitted.", ASSEMBLIES[coil])
    mechanism("mech.gate", "Rear catwalk/tower diverter gate", "diverter", [32], [29, 30, 31, 32, 39], "Output 32 rotates Flipperdiverter away from its rest position; the retained timer returns it after 600ms. The flipper gameitem is a modeling choice for the physical ADV-001 gate. Catwalk, tower and bridge switches report ball passages, not gate position; there is no gate-home sensor. The timer is a recreation timing clue rather than a manufacturer dwell specification.", "ADV-001")
    mechanism("mech.right-flipper", "Lower right flipper", "other", [46], [], "One dual-winding CLL-015 flipper is operated by the right cabinet button. DOC-002 draws its normally-closed local EOS contact; that high-current contact is not a matrix input. Public 45/46 are fabricated together for the whole button closure when 27 is on, and the table consumes 46 for the assembly. They do not expose independent winding currents or EOS timing.")
    mechanism("mech.left-flippers", "Lower and upper left flippers", "other", [48], [], "DOC-002 gives the lower-left CLL-015 and upper-left CLL-003 separate coil branches with a shared left cabinet-button return. The lower-left assembly's normally-open Upper Flipper Activator (PDF44 item22, FLS-002) closes the upper branch when the lower assembly moves. Each coil has its own local normally-closed EOS contact (item24); neither contact is a matrix input. The table's SolLeftFlipper approximates this sequence by moving LeftFlipper and invisible LeftFlipper1 together. Public 47/48 are simultaneous assembly signals, not independently timed winding or upper-flipper states. To reproduce physical sequencing, model the normally-open activator from lower-flipper motion rather than inventing another controller callback.")
    for source, destination in (("switch.flipper-column-114", "switch.08"), ("switch.flipper-column-116", "switch.07"), ("solenoid.45", "solenoid.46"), ("solenoid.47", "solenoid.48")):
        relationships.append({"id": f"relation.{source}.{destination}", "kind": "direct", "source": source, "destination": destination, "provenance": prov(CORE)})
    for number in (*range(17, 25),):
        relationships.append({"id": f"relation.flasher-enable-{number}", "kind": "relay_gated", "source": "solenoid.15", "destination": f"solenoid.{number:02}", "provenance": prov(MANUAL)})
    for n in (46, 48):
        relationships.append({"id": f"relation.flipper-enable-{n}", "kind": "relay_gated", "source": "solenoid.27", "destination": f"solenoid.{n:02}", "provenance": prov(MANUAL, CORE)})

    sources = facts["sources"] + [{"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame", "revision": PIN, "license": "LicenseRef-PinMAME-legacy", "attribution": "PinMAME development team and contributors; Alvin G driver by Steve Ellenoff and Gerrit", "locator": "src/wpc/alvggames.c INITGAME2, mystcast/mystcasa ROM definitions and alvg_dispDMD; src/wpc/alvg.c xvia_0_a_r, CoinDoorSwitches_Read, SWITCH_UPDATE(alvg), alvg_sw2m/alvg_m2sw, u13/u14 handlers, solenoid_w, init_common; src/wpc/alvg.h cabinet constants; src/wpc/core.c core_updateSw/core_getSol; src/wpc/gen.h GEN_ALVG_DMD2. Licensing: pinned LICENSE 12–18 and section VI 73–84; these files lack the first-line BSD marker and retain inherited old-MAME terms; information reuse is expressly permitted separately from source-code reuse.", "excerpts": [{"id": "alvg-read-path", "locator": "Pinned source functions and complete title driver blocks", "path": f"{EXCERPTS}/pinmame.md", "sha256": digest((root / EXCERPTS / "pinmame.md").read_bytes()), "method": "manual", "transcribed_by": "curator from exact pinned source", "reviewed": True}]}]
    manual_source = next(source for source in sources if source["id"] == MANUAL)
    manual_source["excerpts"] = []
    for filename, payload in excerpts().items():
        manual_source["excerpts"].append({"id": filename[:-3], "locator": payload.splitlines()[2], "path": f"{EXCERPTS}/{filename}", "sha256": digest(payload.encode()), "method": "manual", "transcribed_by": "curator; entire regions checked visually against native-resolution scan", "reviewed": True})
    for record in facts["manual_drawing_excerpts"]:
        manual_source["excerpts"].append(record)
    definition = {"format": "pinmame-machine-definition", "schema_version": 2, "machine": {"id": MACHINE_ID, "name": "Mystery Castle", "manufacturer": "Alvin G", "year": 1993, "kind": "physical_pinball", "model_number": "AG08", "ipdb_id": 1647, "opdb_id": "G5vZZ-MQNNo", "playfield": {"width": 952.0, "height": 2162.0, "units": "vpx", "provenance": prov(TABLE)}}, "controller": {"platform": "pinmame.alvin-g", "hardware_generation": "0x400000000000", "inversion_applied_by_emulator": True}, "coverage": {"status": "partial", "missing": ["output_semantics", "spatial_placement", "unresolved_conflicts"], "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "conflicted", "physical_wiring": "conflicted", "output_semantics": "conflicted", "unresolved_conflicts": "conflicted", "mechanisms": "validated", "variant_coverage": "validated", "recreation_knowledge": "validated", "spatial_placement": "candidate"}}, "drivers": [{"id": "mystcast", "description": "Mystery Castle (R02)", "year": "1993", "manufacturer": "Alvin G", "flags": 0, "physical_compatibility": "identical", "variant_notes": "R02 CPU/sound/DMD firmware for the same AG08 cabinet, matrices, mechanisms and 128x32 DMD; alvg_dispDMD, FLIP78 and INITGAME2 fields are identical to R03."}, {"id": "mystcasa", "clone_of": "mystcast", "description": "Mystery Castle (R03)", "year": "199?", "manufacturer": "Alvin G", "flags": 0, "physical_compatibility": "identical", "variant_notes": "R03 (EPC081) changes CPU, sound-program and DMD ROM images, including DMD ROM packaging; it uses exactly the same GEN_ALVG_DMD2 layout and game-data hardware fields. The unknown firmware year does not create a second physical game."}], "inputs": inputs, "outputs": outputs, "displays": [{"id": "display.main", "label": "Backbox Dot Matrix Display", "kind": "dmd", "width": 128, "height": 32, "controller_index": 0, "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", MANUAL, CORE), "provenance": prov(MANUAL, CORE)}], "mechanisms": mechanisms, "relationships": relationships, "knowledge": {"path": f"knowledge/alvin-g/{SLUG}.md", "status": "complete"}, "sources": sources, "conflicts": []}
    definition["conflicts"] = [{
        "id": "gi-region-16-26", "path": "outputs/solenoid.16,solenoid.26/physical",
        "status": "unresolved", "source_refs": [MANUAL, SCRIPT, "runtime.mystcasa-coil-service"],
        "description": "DOC-002's load drawing connects relay 16 to top-playfield GI (13 clear plus 13 red bulbs) and relay 26 to bottom-playfield GI (12 bulbs). Another 2-4 coin-door bulbs tap the shared F21 supply before the relay-26 contact; those unswitched cabinet lamps are supply context, not a controlled relay load. The same manual's coil table labels 16 FIELD RELAY BOT and 26 FIELD RELAY TOP; the observed R03 service labels and retained VPX LowerGILights/UpperGILights assignments agree with that table. The public trace confirms addresses and labels, not the physical region or wired bulb grouping. This is an unresolved difference a recreation consumes; neither region nor per-address quantity is promoted. Resolution path: an original-machine wired socket survey, or a physical-machine service video showing selectors 16/26 together with every bulb they illuminate, supplied by an owner or technician, must link each public address to its actual controlled playfield branch."
    }]
    if {row["id"] for row in unresolved_conflicts(definition)} != {"gi-region-16-26"}:
        raise ValueError("reviewed GI conflict inventory changed")
    next(source for source in sources if source["id"] == CORE)["excerpts"].append({
        "id": "pinmame-license-scope", "locator": "Pinned LICENSE 12–18 and section VI 73–84; cited files' first lines and hashes",
        "path": f"{EXCERPTS}/pinmame-license.md", "sha256": facts["evidence"]["pinmame_license_excerpt_sha256"],
        "method": "manual", "transcribed_by": "curator checked the pinned license and each cited source header", "reviewed": True})
    seed = json.loads((root / CALLOUTS).read_text(encoding="utf-8"))
    definition["sources"].append({"id": DRAWING, "kind": "human_review", "uri": CALLOUTS,
        "sha256": digest((root / CALLOUTS).read_bytes()), "license": "NOASSERTION",
        "attribution": "Alvin G & Co factory drawing; independent source-only reader transcription, curator native-page verification and corrections",
        "locator": "Manual PDF29 / printed3-5 Lamp Locations. Four source-only bumper/rounded-flipper-heel controls; native2142x3055 render; 57 checks, excluding the two bumper lamps used as controls. Printed labels beside parts identify diagram features, not surveyed socket centers. Exact uncertainty, original reads, corrections and retained manifest are in the seed. Generated 2026-10-15 by tools/drawing_callouts.py version1."})
    drawing_callouts.apply_to_definition(definition, seed, DRAWING)
    return definition


def verify_inputs(root, facts):
    """Refuse incomplete, modified or internally inconsistent portable evidence."""
    if facts.get("machine_id") != MACHINE_ID or facts.get("version") != 1:
        raise ValueError("wrong Mystery Castle facts identity/version")
    if digest((root / CALLOUTS).read_bytes()) != facts["evidence"]["drawing_callouts_seed_sha256"]:
        raise ValueError("missing or changed drawing callout seed")
    if digest((root / EXCERPTS / "pinmame-license.md").read_bytes()) != facts["evidence"]["pinmame_license_excerpt_sha256"]:
        raise ValueError("missing or changed PinMAME license scope excerpt")
    if len(SWITCH_LABELS) != 96 or len(LAMP_LABELS) != 96 or len(COIL_ROWS.splitlines()) != 32:
        raise ValueError("incomplete factory address transcription")
    manifest = json.loads((root / f"tools/seeds/alvin-g/{SLUG}-extraction-manifest.json").read_text(encoding="utf-8"))
    if digest(canonical_bytes(manifest) + b"\n") != facts["evidence"]["extraction_manifest_sha256"]:
        raise ValueError("retained extraction manifest digest mismatch")
    if manifest["game"] != "mystcast" or len(manifest["files"]) != facts["evidence"]["extraction_file_count"] or sum(row["size"] for row in manifest["files"]) != facts["evidence"]["extraction_byte_count"]:
        raise ValueError("retained extraction manifest identity/count mismatch")
    for source in facts["sources"]:
        for excerpt in source.get("excerpts", []):
            path = root / excerpt["path"]
            if not path.is_file() or digest(path.read_bytes()) != excerpt["sha256"]:
                raise ValueError(f"missing or changed source excerpt: {path}")
    for excerpt in facts["manual_drawing_excerpts"]:
        for key, hash_key in (("path", "sha256"), ("image", "image_sha256")):
            path = root / excerpt[key]
            if not path.is_file() or digest(path.read_bytes()) != excerpt[hash_key]:
                raise ValueError(f"missing or changed physical drawing excerpt: {path}")
    for group in ("switches", "lamps", "solenoids"):
        for records in facts[group].values():
            for record in records:
                expected = (round(record["raw"]["x"] / 952, 6), round(record["raw"]["y"] / 2162, 6))
                if (record["x"], record["y"]) != expected or any(not 0 <= value <= 1 for value in expected):
                    raise ValueError(f"invalid source coordinate: {record['object']}")


def runtime_evidence(root, facts):
    """Wrap the exact portable visual-read summary in the shared evidence schema."""
    text = (root / EXCERPTS / "coil-service-summary.md").read_text(encoding="utf-8")
    summary = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
    source_path = f"external:pinmame-review-artifacts/{MACHINE_ID}/harness/coil-service/run.json"
    snapshots = [{"label": entry["step_label"], "display_index": 0,
                  "pixel_sha256": entry["pixel_sha256"],
                  "interpreted_text": f"SINGLE COILS {entry['displayed_number']:02} {entry['visually_read_name']}",
                  "active_solenoid_addresses": facts["runtime_snapshot_active_solenoids"][entry["step_label"]]} for entry in summary["entries"]]
    return {
        "format": "pinmame-machine-evidence", "version": 1,
        "extractor": {"id": "tools/curate_mystery_castle.py", "version": 1},
        "source": {"kind": "service_diagnostic", "repository": "https://github.com/vpinball/pinmame",
                   "revision": PIN, "path": source_path, "sha256": summary["source_run_sha256"],
                   "license": "NOASSERTION", "quality": "validated",
                   "attribution": "Runtime reviewer visually read every retained DMD frame; contribution curator reconciled names with factory wiring and checked every same-step public transition. Snapshot active states are preserved separately from pulse transitions; exact transition and snapshot/file hashes are in the portable coil-service-summary.md excerpt. No negative observation establishes physical non-fitment."},
        "driver_ids": ["mystcasa"], "machine_ids": [MACHINE_ID],
        "switches": [], "outputs": [], "states": [], "mechanisms": [], "recreation_notes": [],
        "runtime": {"game": "mystcasa", "rom_archive_sha256": summary["rom_archive_sha256"],
                    "emulator": {"binary": "pinmame64.dll", "sha256": summary["library_sha256"], "built_from_revision": PIN},
                    "raw_runs": [{"name": "R03 single-coil selector", "sha256": summary["source_run_sha256"],
                                  "retained_from": source_path, "self_test_pulses": len(summary["entries"]),
                                  "scenario_path": f"external:pinmame-review-artifacts/{MACHINE_ID}/coil-settled-checkpoints-scenario.json",
                                  "scenario_sha256": summary["scenario_sha256"], "boot_wait_s": 15,
                                  "nvram_initialization": "New isolated state directory; no state inherited from exploratory attempts."}],
                    "command_template": "python <retained alvg_harness.py> --library <pinned pinmame64.dll> --game mystcasa --rom-path <authorized read-only ROM root> --work-dir <new state> --handle-mechanics 0 --scenario <coil-settled-checkpoints-scenario.json> --output <external run.json>. Direct service writes keep keyboard handling off. T TESTS and SINGLE COILS title checkpoints each settle two seconds before the next action.",
                    "observations": {"service_language": "English", "display_indices_seen": [0],
                                     "solenoid_addresses_seen": sorted({v["number"] for entry in summary["entries"] for v in entry["observed_transitions"]}),
                                     "physical_service_solenoid_to_public": {str(entry["displayed_number"]): entry["public_solenoid"] for entry in summary["entries"]},
                                     "diagnostic_snapshots": snapshots}}
    }



def promotion_decision(drawing_summary, callouts):
    """Describe the computed fit without duplicating its counts or failure inventory."""
    excluded = ", ".join("lamp." + label.zfill(2) for label in sorted(callouts.get("excluded_checks", {}))) or "none"
    failed = ", ".join(sorted(drawing_summary["not_validated"])) or "none"
    return (f"Partial. The factory lamp-location drawing independently validates {drawing_summary['validated']} "
            f"of {drawing_summary['checked']} checked feature anchors; excluded lamp controls: {excluded}; "
            f"failed fit placements: {failed}. GI physical-region assignment, wired socket grouping and missing "
            "flasher emitters remain unresolved. Validated feature anchors do not assert measured socket centers.")


def artifacts(root):
    facts = json.loads((root / f"tools/seeds/alvin-g/{SLUG}-facts.json").read_text(encoding="utf-8"))
    verify_inputs(root, facts)
    definition = build_definition(root, facts)
    callouts = json.loads((root / CALLOUTS).read_text(encoding="utf-8"))
    decisions = drawing_callouts.evaluate(callouts, drawing_callouts.placements_of(definition))
    drawing_summary = drawing_callouts.summary(callouts, decisions, CALLOUTS, facts["evidence"]["drawing_callouts_seed_sha256"])
    payload = json_bytes(definition)
    positions = []
    for collection in ("inputs", "outputs"):
        for device in definition[collection]:
            spatial = device.get("spatial", {})
            if "placements" in spatial:
                positions.append({"device": device["id"], "status": spatial["status"], "placements": spatial["placements"]})
    report = {"format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID, "coordinate_convention": "x=0 left,1 right; y=0 rear/backglass,1 front/apron; one playfield space", "transformation": {"x": "raw_x/952", "y": "raw_y/2162", "rounding": "repository extract_spatial_candidates, six decimals", "bounds": {"left": 0, "top": 0, "right": 952, "bottom": 2162}}, "evidence": facts["evidence"], "resolved": positions, "projection_classes": facts["projection_classes"], "excluded_helpers": facts["excluded_helpers"], "blockers": facts["blockers"], "conflicts": definition["conflicts"]}
    report["drawing_callouts"] = drawing_summary
    report["promotion_decision"] = promotion_decision(drawing_summary, callouts)
    lines = ["# Mystery Castle spatial audit and blockers", "", "Coverage: **partial**", "", report["promotion_decision"], "", "## Factory drawing check", "", "Four independent source-only controls use two bumper circles and two lower flipper rounded heels. The heels are verified pivot estimates with 15px uncertainty; shaft dots are not drawn. Bumper centers have 10px uncertainty. The controls span the field; both control and callout leave-one-out fits are checked by the official helper. Source-only read corrections and all original ambiguities remain retained. Labels beside parts establish diagram feature locations, not exact sockets.", "", "```json", json.dumps(drawing_summary, indent=2, sort_keys=True), "```", "", "## Evidence and transform", "", "`x=raw_x/952`, `y=raw_y/2162`; x left-to-right, y rear-to-front; six decimals through the repository extractor.", "", "```json", json.dumps(facts["evidence"], indent=2, sort_keys=True), "```", "", "## Projection classes", ""]
    for item in facts["projection_classes"]:
        lines.append(f"- {item['class']}: {item['reason']}")
    lines += ["", "## Excluded helpers and proxies", ""] + [f"- {name}: {reason}" for name, reason in facts["excluded_helpers"].items()]
    lines += ["", "## Device placements", "", "| Device | State | Placements (x,y) |", "| --- | --- | --- |"]
    lines += [f"| {row['device']} | {row['status']} | " + "; ".join(f"{p['x']},{p['y']}" for p in row["placements"]) + " |" for row in positions]
    lines += ["", "## Concrete remaining evidence", ""] + [f"- {item['reason']} Resolution: {item['would_resolve']}" for item in facts["blockers"]] + [""]
    result = {f"machines/partial/alvin-g/{SLUG}.json": payload, f"tools/seeds/alvin-g/{SLUG}.json": payload, f"reports/spatial/alvin-g/{SLUG}.json": json_bytes(report), f"reports/spatial/alvin-g/{SLUG}.md": "\n".join(lines).encode(), f"knowledge/alvin-g/{SLUG}.md": (root / f"tools/seeds/alvin-g/{SLUG}-knowledge.md").read_bytes()}
    result.update({f"{EXCERPTS}/{name}": value.encode() for name, value in excerpts().items()})
    result["evidence/runtime/alvin-g/mystcasa-coil-service.json"] = json_bytes(runtime_evidence(root, facts))
    return result


def run(root, check):
    if (root / f"machines/author-ready/alvin-g/{SLUG}.json").exists():
        raise ValueError("refusing to overwrite or accept an existing author-ready artifact")
    expected = artifacts(root)
    errors = []
    for relative, payload in expected.items():
        path = root / relative
        if check:
            if not path.is_file() or path.read_bytes().replace(b"\r\n", b"\n") != payload.replace(b"\r\n", b"\n"):
                errors.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    if check and errors:
        raise ValueError("Mystery Castle curator drift: " + ", ".join(errors))
    print(f"Mystery Castle curator {'check' if check else 'regeneration'}: OK ({len(expected)} artifacts)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    parser.add_argument("--repository-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    run(args.repository_root.resolve(), args.check)


if __name__ == "__main__":
    main()
