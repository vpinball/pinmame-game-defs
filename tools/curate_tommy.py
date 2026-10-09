"""Curate the physical Data East The Who's Tommy Pinball Wizard (1994) machine definition.

Side-effect free and deterministic. The printed tables are parsed from the hand-transcribed excerpts
committed under ``evidence/excerpts/data-east.the-who-s-tommy-pinball-wizard.1994/`` (``tommy_manual``),
the semantic naming is in ``tommy_semantics``, the normalized coordinates resolved from the retained
recreation are in ``tools/tommy_places.json`` (``tools/build_tommy_places.py``), the ROM's own service-test
readings are in ``tools/tommy_runtime.json`` (``tools/build_tommy_runtime_evidence.py``), and the ROM
inventory is parsed from pinned PinMAME and embedded below. ``--regenerate`` reproduces the canonical
artifacts byte-for-byte without reading any external evidence root; ``--check`` refuses drift.

The definition, its pinned seed, the spatial report and the knowledge note are all generated here from
the same objects, so prose cannot outlive the data behind it. The comparison folds CRLF to LF first, so a
checkout Git rewrote under ``core.autocrlf=true`` still passes while every other byte difference fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from pinmame_game_defs.jsonio import load_json, write_json
from pinmame_flipper_column import (
    VPM_CORE_SHA256,
    VPM_DE_LIBRARY_SOURCE,
    VPM_DE_LIBRARY_URI,
    VPM_DE_SHA256,
    flipper_column_inputs,
    flipper_column_relationships,
    vpm_staged_flipper_notes,
)
import tommy_manual
import tommy_semantics as sem

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.the-who-s-tommy-pinball-wizard.1994"
SLUG = "the-who-s-tommy-pinball-wizard-1994"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
PLACES_PATH = ROOT / "tools/tommy_places.json"
RUNTIME_PATH = ROOT / "tools/tommy_runtime.json"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/the-who-s-tommy-pinball-wizard-tomy_400-service-tests.json"
KNOWLEDGE_TEMPLATE = ROOT / "tools/tommy_knowledge.md"
EXCERPT_DIR = ROOT / "evidence/excerpts" / KEY

REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
SHORT = REVISION[:12]
MANUAL = f"manual.{KEY}"
IPDB = f"ipdb.{KEY}"
CATALOG = f"pinmame.catalog.{SHORT}"
CORE = f"pinmame.core.{SHORT}"
CORE_H = f"pinmame.core-h.{SHORT}"
CORE_C = f"pinmame.core-c.{SHORT}"
S11_C = f"pinmame.s11-c.{SHORT}"
S11_H = f"pinmame.s11-h.{SHORT}"
TABLE = "vpx-table.the-who-s-tommy-pinball-wizard-vpw-mod-1-2-1"
SCRIPT_REF = "vpx-script.the-who-s-tommy-pinball-wizard-vpw-mod-1-2-1"
EXTRACTION = "vpx-extraction.the-who-s-tommy-pinball-wizard-vpw-mod-1-2-1"
LEGACY = "legacy.game.tommy"
RUNTIME_SRC = "runtime.the-who-s-tommy-pinball-wizard.tomy-400-service-tests"

MANUAL_NAME = "Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf"
MANUAL_SHA256 = "4d61131a75c9fca301ed878160b6f90448296b935f65fd62a8c9b13e390405fb"
MANUAL_URL = "https://web.archive.org/web/20240804185614id_/https://www.ipdb.org/files/2579/Data_East_1994_The_Who_s_Tommy_Pinball_Wizard_Manual.pdf"
IPDB_CAPTURE = "https://web.archive.org/web/20251218152159id_/https://www.ipdb.org/machine.cgi?id=2579"
IPDB_SHA256 = "950507b62368d55d81a748c2728e7b8736485d500c6d3adb5be94a04a44d6eec"
TABLE_NAME = "The Who's Tommy Pinball Wizard (Data East 1994) VPWMod 1.2.1.vpx"
TABLE_SHA256 = "65b781c4ce13f253dace8003b4c06fe55d447255d51eb9821732c64bad4c7d0b"
SCRIPT_SHA256 = "c6d74cb6fafd0aad6c12129272a3cd0a4f5086b2f75c7f6f8d00850e555717d1"
EXTRACTION_MANIFEST_SHA256 = "fc3f74ec1c6a35dac4a56050b394ef6e7c7ff0de36a61344bb2940a5d3e2696b"
EXTRACTION_FILE_COUNT = 2286
EXTRACTION_TOTAL_BYTES = 247222456
PIN_FILE_SHA256 = {
    "degames.c": "223623584396cc530c8baef577772d4b96d39784aa2624f04746871c8f89f5d8",
    "core.h": "2c233ae172aad639fc7a3636c7882ca65a8c4bfa99f086b4b90ef17cf8c41a12",
    "core.c": "ae94d4ae8078f684b3ba58fd35cac84bf58e181de1e6f25ecb95f03c66966dcc",
    "s11.c": "cd1b989ac1eec8c95126e743829a8a3726e76a9b838a29339776d4025d75d2d4",
    "s11.h": "743b0836cc84e41e793d65786a964a595fb403c4fdba29b2961e8a36a937f614",
}

# The seven PinMAME drivers, parsed from src/wpc/degames.c at the pinned revision (lines 1158-1242).
# Roles: CPU, display, then the five sound ROMs (U7, U17, U21, U36, U37). All seven share tommyGameData
# (degames.c lines 1165-1172) and every sound ROM.
ROLES = ("CPU", "display", "sound U7", "sound U17", "sound U21", "sound U36", "sound U37")
SOUND = ["tommysnd.u7", "tommysnd.u17", "tommysnd.u21", "tommysnd.u36", "tommysnd.u37"]
ROM_SETS = {
    "tomy_400": ["tomcpua.400", "tommydva.400", *SOUND],
    "tomy_500": ["tomcpua.500", "tommydva.500", *SOUND],
    "tomy_301g": ["tom_3.00_german_cpu_c5.bin", "tom_3.00_german_display_rom0.bin", *SOUND],
    "tomy_201d": ["Tommy_2.01_Dutch_cpu.bin", "Tommy_2.00_display.bin", *SOUND],
    "tomy_h30": ["tomcpuh.300", "tommydva.300", *SOUND],
    "tomy_102": ["tomcpua.102", "tommydva.300", *SOUND],
    "tomy_102be": ["tomcpub.102", "tommydvb.102", *SOUND],
}
ROOT_DRIVER = "tomy_400"
DRIVER_LABELS = {
    "tomy_400": "Tommy Pinball Wizard, The Who's (4.00)",
    "tomy_500": "Tommy Pinball Wizard, The Who's (5.00 unofficial MOD)",
    "tomy_301g": "Tommy Pinball Wizard, The Who's (3.01 German)",
    "tomy_201d": "Tommy Pinball Wizard, The Who's (2.01 Dutch)",
    "tomy_h30": "Tommy Pinball Wizard, The Who's (3.00 Dutch)",
    "tomy_102": "Tommy Pinball Wizard, The Who's (1.02)",
    "tomy_102be": "Tommy Pinball Wizard, The Who's (1.02 Belgian)",
}
DRIVER_YEARS = {driver: ("2016" if driver == "tomy_500" else "1994") for driver in ROM_SETS}

SW = tommy_manual.switch_data()
LAMP = tommy_manual.lamp_data()
COIL = tommy_manual.coil_data()
PARTS = tommy_manual.assembly_data()
LEGACY_GAME = load_json(ROOT / "games/tommy.json")
PLACES = load_json(PLACES_PATH) if PLACES_PATH.is_file() else {"table_bounds": None, "placements": {}, "unplaced": [], "rejected": []}
FACTS = load_json(RUNTIME_PATH)
ROM_SWITCH = FACTS["rom_switch_names"]
ROM_LAMP = FACTS["rom_lamp_names"]
COIL_TEST = FACTS["coil_test"]
CYCLE = FACTS["cycling_coils_order"]
SERVE = FACTS["trough_serve"]
ROW_COLUMN = FACTS["lamp_row_column"]


def prov(status: str, refs) -> dict:
    return {"status": status, "source_refs": list(refs)}


def not_applicable(reason: str, refs) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov("validated", refs)}


def legacy_numbers(n: int) -> list[str]:
    values = [str(n)]
    for width in (2, 3):
        padded = str(n).zfill(width)
        if padded not in values:
            values.append(padded)
    return values


LEGACY_SWITCHES = {int(item["id"]) for item in LEGACY_GAME["switches"]}
LEGACY_COILS = {int(item["id"]) for item in LEGACY_GAME["coils"]}
LEGACY_LAMPS = {int(item["id"]) for item in LEGACY_GAME["lamps"]}


def aliases(namespace: str, address: int, legacy_kind: str | None, legacy: set[int], *, extra=()) -> list[dict]:
    values = [{"namespace": namespace, "value": str(address)}]
    if legacy_kind and address in legacy:
        values += [{"namespace": f"vpe-legacy.{legacy_kind}", "value": value} for value in legacy_numbers(address)]
    values += [{"namespace": ns, "value": value} for ns, value in extra]
    return values


def spatial_for(device_id: str, role: str, key: str, refs) -> dict | None:
    hits = PLACES["placements"].get(key)
    if not hits:
        return None
    hits = sorted(hits, key=lambda hit: (hit["x"], hit["y"]))
    placements = []
    for index, hit in enumerate(hits, start=1):
        suffix = "" if len(hits) == 1 else f".{index}"
        placements.append({
            "id": f"{device_id}.{role}{suffix}", "role": role, "space": "playfield",
            "x": hit["x"], "y": hit["y"], "provenance": prov("observed", refs),
        })
    return {"status": "observed", "placements": placements}


PLACE_REFS = [TABLE, SCRIPT_REF, MANUAL]
inputs: list[dict] = []
outputs: list[dict] = []

# --- Inputs: the 8 x 8 switch matrix -----------------------------------------------------------------
FLIP_SWNO = (63, 64)
for address in range(1, 65):
    chart = SW["chart"][address]
    part = SW["parts"][address]
    unused = address in sem.UNUSED_SWITCHES
    suffix, label = ("unused-%d" % address, "Unused Switch %d" % address) if unused else sem.SWITCHES[address]
    device_id = f"switch.{suffix}"
    notes = [f"Printed switch-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}'."]
    if unused:
        notes.append("Printed Not Used in both the switch-matrix chart and the Switch Part Numbers table; the address is strobed but carries no device.")
    else:
        notes.append(f"The Switch Part Numbers table prints '{part['description']}'" + (f", part {part['part']}." if part["part"] else f", with the part cell printed '{part['part_printed']}'."))
    if part["marker"] == "*":
        notes.append("The table marks the address '*', which its legend reads 'Location - In Cabinet'.")
    if part["marker"] == "**":
        notes.append("The table marks the address '**', which its legend reads 'Locatoin - Under Playfield' (sic).")
    if address == 2:
        notes.append(
            "Dedicated cabinet column. Pinned PinMAME's shared DE_COMPORTS macro labels this position 'Ball Tilt', but that is a generic platform label: this "
            "machine's own chart and parts table print '4th Coin' (On Coin Door) with no part number. tommyGameData sets no S11_MUXSW2, so s11.c does not overwrite it with relay state."
        )
    if address == 3:
        notes.append(
            "DE_COMPORTS binds the cabinet Start button to this position; the manual's Game Diagnostics text calls it the 'Game Start push-button switch on the front of the "
            "cabinet', and the Cabinet Parts list names the 'Start Button Switch Ass'y (Touch Me)' 500-5728-01. The chart names the address Credit Button, so both names are kept."
        )
    if address == 8:
        notes.append(
            "Not declared by pinned PinMAME's DE_COMPORTS. The Cabinet Parts list names an 'Extra Ball Switch Ass'y (Orange)' 500-5779-07; the retained table sets the "
            "address from keycode 3 (Tommy_KeyDown/Tommy_KeyUp, script lines 147 and 212)."
        )
    if address in (28, 31):
        notes.append(
            "One of the two limit switches of the mirror motor mechanism ('Mirror Motor Up & Mirror Motor Down' in the Mirror Up & Down Test text), which the CPU reads to "
            "determine the motor's state; the text says each closes just prior to the limit of the mechanism and that both should never be closed together. The "
            "retained table has no object for it: its MirrorTimer synthesises the address from the height of the MirrorP primitive "
            + ("(MirrorP.Z >= 137 closes 28, script lines 842-846)." if address == 28 else "(MirrorP.Z <= 3 closes 31, script lines 847-851).")
        )
    if address == 32:
        notes.append(
            "The mirror itself: the Mirror Up & Down Test text calls the mechanism 'a Target Switch (Mirror)' that is lowered to allow a shot to the VUK. The retained table "
            "pulses it from sw32_Hit only above a ball speed of 4 (ShakeMirror, script lines 858-868)."
        )
    if address in (41, 42):
        notes.append(
            "The location drawing marks the entry with a circled 'ET' (Enter Trough (Mirror & Skill)). The retained table pulses it from the trigger "
            f"sw{address} (script lines {644 if address == 41 else 638}-{645 if address == 41 else 639})."
        )
    if address in (58, 62):
        notes.append("The location drawing puts the balloon at the rail beside the words 'ON WIRE RAMP'.")
    rom = ROM_SWITCH[str(address)]
    notes.append(
        f"ROM evidence (US 4.00 Active Switch Test): holding public {address} at 1 shows '{rom['name']}', wires {rom['wires']} and '#{address:02d}'; "
        "with every public switch at 0 the same screen shows no switch. The ROM therefore treats public 1 as the closed contact and no switch as closed at rest"
        + (", so the matrix contact rests open. The test also names the address NOT USED." if unused else ", so the matrix contact rests open.")
    )
    entry = {
        "id": device_id,
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": aliases("pinmame.switch", address, "switch", LEGACY_SWITCHES),
        "availability": "unused" if unused else "used",
        "provenance": prov("validated", [MANUAL, CORE_H, RUNTIME_SRC] + ([] if unused or address in (2,) else [SCRIPT_REF])),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": chart["drive"]["wire"],
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
        },
    }
    if not unused:
        entry["normally_closed"] = False
    if part["part"]:
        entry["physical"]["part_number"] = part["part"]
    if address in sem.SWITCH_TYPES:
        entry["physical"]["switch_type"] = sem.SWITCH_TYPES[address]
    if address in sem.CABINET_ROLES:
        entry["roles"] = [sem.CABINET_ROLES[address]]
    if address in FLIP_SWNO:
        side = "left" if address == 63 else "right"
        button = 84 if address == 63 else 82
        entry["physical"]["notes"] += (
            f" The parts table prints this address as the {side} flipper cabinet switch (part 180-5124-00, marked '*' In Cabinet). PinMAME declares "
            f"tommyGameData's flippers FLIP6364 = FLIP_SWNO(63,64) with no FLIP_SOL, and core.c's core_updateSw rewrites this switch on every update from PinMAME's "
            f"flipper column button bit {button} (the {side} cabinet button), so the ROM reads the button state exactly as the host wrote it there. A consumer drives {button}, "
            f"not {address}: a host write to {address} is overwritten on the next update. The retained table never writes this address (its flipper keys reach de.vbs, which writes 82/84)."
        )
        entry["roles"] = [f"flipper.lower.{side}.matrix-copy"]
    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address in sem.CABINET_ROLES or address in FLIP_SWNO:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, CORE_H] if address in FLIP_SWNO else [MANUAL])
    else:
        located = spatial_for(device_id, "sensor", f"switch.{address}", PLACE_REFS)
        if located:
            entry["spatial"] = located
            if address in (28, 31):
                entry["physical"]["notes"] += (
                    " The coordinate is a projection onto the retained table's mirror mechanism (MirrorP); the switch has no own geometry in the table."
                )
    inputs.append(entry)

for address, suffix, label, port_label in (
    (-7, "service-advance", "Advance (Black Button)", "Black Button"),
    (-6, "service-up-down", "Up/Down (Green Button)", "Green Button"),
):
    inputs.append({
        "id": f"switch.{suffix}",
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": [{"namespace": "pinmame.switch", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [S11_H, S11_C, MANUAL, RUNTIME_SRC]),
        "physical": {"notes": (
            f"Coin-door diagnostic button, named '{port_label}' by s11.h's DE_COMPORTS, placed in switch column 0 rather than the playfield matrix. "
            "Data East defines only these two (DE_SWADVANCE -7, DE_SWUPDN -6). The manual's Game Diagnostics page names them the STEP push-button and the "
            "FORWARD/REVERSE push-button inside the coin door; the Cabinet Parts list names the 'Interlock & Momentary Diagnostics Switch Set' 180-5012-00. "
            + (
                "The manual tells the operator to 'depress' it, and every retained service run pulses it at level 1 for 250 ms or less while the ROM advances one test per pulse "
                "and stays put at 0, so public 1 is the depressed button. s11.c hands the PIA the complement (pia_set_input_ca1(S11_PIA2, !core_getSw(DE_SWADVANCE))), the level "
                "a contact closing to ground presents. A momentary push-button that rests released therefore rests with its contact open."
                if address == -7 else
                "An alternate-action push-button with two maintained positions that the manual calls FORWARD (up) and REVERSE (down) and says must be REVERSE to enter "
                "diagnostics. The retained service runs hold it at 1 for the diagnostics walks, so public 1 is REVERSE. Unlike the Black button, s11.c hands the PIA the level "
                "uncomplemented (pia_set_input_cb1(S11_PIA2, core_getSw(DE_SWUPDN))), and no retained page draws the coin-door switch circuit, so which position closes the "
                "contact is not established; a two-position maintained switch also has no single rest position. Its contact polarity is left undeclared, which keeps the polarity requirement open."
            )
        )},
        **({"normally_closed": False} if address == -7 else {}),
        "spatial": not_applicable("cabinet_or_service", [S11_H, S11_C, MANUAL]),
    })

_LEFT_ROW = COIL["flippers"]["Left Flipper"]
_RIGHT_ROW = COIL["flippers"]["Right Fliper Lwr."]
_UPPER_ROW = COIL["flippers"]["Left Flipper Upr."]
_flipper_items = flipper_column_inputs(
    flip_swno=FLIP_SWNO, flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)",
    core_refs=(CORE, CORE_H, CORE_C, S11_C), button_refs=(SCRIPT_REF, VPM_DE_LIBRARY_SOURCE),
    button_notes={
        side: (
            f"The retained known-working script drives it: Tommy_KeyDown/Tommy_KeyUp hand the {side} flipper key to de.vbs vpmKeyDown/vpmKeyUp (script lines 207 and 264), "
            f"which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with {'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} "
            f"(excerpt vpm-script-library-flippers). The physical counterpart is the {side} cabinet flipper button"
            + ("; the left button works both left flippers, the lower and the upper left one (the Cabinet Parts list's 'Flipper Switch, Double, Left Top/Bottom' 180-5122-00)."
               if side == "left" else ".")
        )
        for side in ("left", "right")
    },
    unused_notes=vpm_staged_flipper_notes(library="DE.VBS"),
    unused_note_refs=(VPM_DE_LIBRARY_SOURCE,),
)
for _item in _flipper_items:
    _address = _item["binding"]["device"]
    if _address in (82, 84):
        _matrix = 64 if _address == 82 else 63
        _row = _LEFT_ROW if _address == 84 else _RIGHT_ROW
        _item["provenance"]["source_refs"] += [RUNTIME_SRC, MANUAL]
        _item["physical"]["notes"] += (
            f" ROM evidence (US 4.00 Active Switch Test): holding public {_address} at 1 shows '{ROM_SWITCH[str(_matrix)]['name']}', the wires "
            f"{ROM_SWITCH[str(_matrix)]['wires']} and '#{_matrix}', the matrix switch core_updateSw copies it into, while the other six flipper-column addresses "
            "(81, 83 and 85-88) show no switch, so the ROM cannot see them."
            f" Contact: the manual's Flipper Solenoids table routes the flipper ground '{_row['CPU to flipper switch']}' through the cabinet flipper switch to the Flipper PCB "
            f"('{_row['Flipper switch to Flip. PCB']}'). A switch in series with the flipper's ground energises the coil while it is closed, so the released button rests open; "
            "public 1 is the pressed button."
        )
        _item["normally_closed"] = False
    else:
        _item["provenance"]["source_refs"].append(RUNTIME_SRC)
        _item["physical"]["notes"] += " ROM evidence: holding this address at 1 in the US 4.00 Active Switch Test shows no switch."
inputs.extend(_flipper_items)

inputs.append({
    "id": "dip.jumper-w7",
    "label": "Jumper W7",
    "kind": "dip_switch",
    "binding": {"group": "pinmame.input.dip", "device": 0},
    "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
    "availability": "unknown",
    "provenance": prov("observed", [S11_C]),
    "physical": {"notes": (
        "s11.c declares MDRV_DIPS(1), commented '(actually a jumper)', and pia2a_r reads it as core_getDip(0) << 7 on PIA2 PA7, annotated 'PA7 (I) Jumper W7'. "
        "This machine's manual prints a CPU jumper table (PDF page 2) for the ROM and RAM jumpers of each game but does not describe W7, so the meaning of the bit is not "
        "stated by any retained source."
    )},
    "spatial": not_applicable("dip_switch", [S11_C]),
})

# --- Outputs: drives 1-8, the left (coil) half of the Left/Right relay pair ---------------------------
DRV = COIL["drivers"]
SCHEM = COIL["schematic"]


def _volts(text: str) -> tuple[int, str]:
    """'32v L' -> (32, 'dc'); '9v AC' -> (9, 'ac')."""
    number, _, rest = text.partition("v")
    return int(number), ("ac" if "AC" in rest else "dc")


LEFT_IDS = {
    1: ("coil", "coil.six-ball-lockout", "6-Ball Ass'y Lockout"),
    2: ("coil", "coil.ball-eject", "Ball Eject (Ball Release)"),
    3: ("coil", "coil.auto-ball-launch", "Auto Ball Launch"),
    4: ("coil", "coil.vuk", "VUK"),
    5: ("coil", "coil.left-scoop", "Left Scoop"),
    6: ("coil", "coil.eject", "Eject"),
    7: ("virtual", "coil.unused-driver-7", "Unfitted Left Driver 7"),
    8: ("coil", "coil.knocker", "Knocker"),
}
SCRIPT_BOUND_LEFT = {
    1: "SolCallback(1) = SolTrough, which kicks the ball held at sw14 toward sw15 and sets switch 15 (script lines 476 and 585-590)",
    2: "SolCallback(2) = SolRelease, which kicks sw15's ball into the shooter lane and clears switch 15 (script lines 477 and 592-598)",
    3: "SolCallback(3) = AutoLaunch, which fires the cvpmImpulseP plunger on swPlunger (script lines 478 and 616-623)",
    4: "SolCallback(4) = ExitVUK, which kicks sw19's ball up (script lines 479 and 659-669)",
    5: "SolCallback(5) = ExitScoop, which kicks sw23's ball out (script lines 480 and 693-704)",
    6: "SolCallback(6) = SolEject, which kicks sw47's ball (script lines 481 and 742-748)",
    8: "SolCallback(8) = vpmSolSound Knocker (script line 482)",
}

for address in range(1, 9):
    row = DRV[f"{address}L"]
    kind, device_id, label = LEFT_IDS[address]
    drawn = SCHEM[address]
    unfitted = address == 7
    notes = [
        f"Left half of the Left/Right relay pair on drive {address} (coil-table row {address}L, '{row['Description']}', Coil Test index '{COIL['index'][f'{address}L']}'); "
        f"the right half (row {address}R) is published at address {address + 24}. The coil chart schematic draws it as '{drawn['Coil as drawn']}'."
    ]
    if unfitted:
        notes.append(
            "The coil table prints every cell of the row 'Not Used' or dashes except the PPB J2-3 connector, and the schematic marks the wire 'N.C.' at a 'NO COIL AT THIS "
            "LOCATION' balloon: no load is fitted on this half of the drive."
        )
    else:
        notes.append(f"The retained table binds {SCRIPT_BOUND_LEFT[address]}.")
    if address == 2:
        notes.append("The coil table and index call it 'Ball Eject'; the schematic labels the coil 'BALL RELEASE'. It kicks the ball from the trough's release position into the shooter lane.")
    if address in (3, 4):
        notes.append(
            f"The coil returns to '{row['Power line']}' on '{row['Power connection']}', which the schematic draws as +50 VL through a TIP 36C booster transistor on the PPB "
            f"board (the coil table's power-description cell prints '{row['Power description']}'); the J8 control connection is the booster's output."
        )
    if address == 8:
        notes.append("The Cabinet Parts list places the Knocker (500-5081-00) in the cabinet, and the Major Assemblies list calls it 'Knocker Ass'y (In Cabinet Bottom, See Item 40, Pg. 37)'.")
    entry = {
        "id": device_id,
        "label": label,
        "kind": kind,
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "unused" if unfitted else "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([] if unfitted else [SCRIPT_REF])),
        "physical": {"notes": " ".join(notes)},
        "wiring": {"board": "CPU Board", "driver_transistor": row["Drive transistor"]},
    }
    if not unfitted:
        entry["physical"]["part_number"] = row["Coil or flash type"]
        volts, vtype = _volts(row["Power description"])
        entry["wiring"].update({
            "control_wire": row["Control line"], "control_connection": row["Control connect"],
            "power_wire": row["Power line"], "power_connection": row["Power connection"],
            "nominal_voltage_v": 50 if address in (3, 4) else volts, "voltage_type": vtype,
        })
    if unfitted:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address == 8:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        located = spatial_for(entry["id"], "effect", f"solenoid.{address}", PLACE_REFS)
        if located:
            entry["spatial"] = located
            entry["physical"]["notes"] += " The coordinate is the retained table's model of the mechanism this coil actuates, not a claimed winding centre."
    outputs.append(entry)

# --- Outputs: drives 9-16, direct on CN-12 ------------------------------------------------------------------
DIRECT = {
    9: ("motor", "motor.unfitted-shaker-9", "Shaker Motor Driver (Motor Not Fitted)", "unused"),
    10: ("relay", "relay.left-right-relay", "Left/Right Relay", "used"),
    11: ("gi", "gi.general-illumination", "G.I. Relay", "used"),
    12: ("coil", "coil.top-diverter", "Top Diverter", "used"),
    13: ("motor", "motor.airplane", "Airplane Motor", "used"),
    14: ("motor", "motor.mirror", "Mirror Motor Relay", "used"),
    15: ("flasher", "flasher.tommy", "Tommy Flash", "used"),
    16: ("virtual", "coil.unused-driver-16", "Unfitted Driver 16", "unused"),
}
DIRECT_NOTES = {
    9: (
        "The row is the PPB's Q1 TIP 36C shaker driver: the coil chart schematic and the Playfield Coil/Flashlamp Wiring Diagram draw drive 9 (CPU CN12-1, Q30, WHT/BRN) "
        "through Q1 to the Shaker Motor Board and a 'CABINET SHAKER MOTOR 12VDC'. The Cabinet Parts list prints 'Shaker Motor (Not Used in this Game)' 515-5893-00 while it "
        "lists the Shaker Motor P.C. Board 520-5065-00 (which also feeds the airplane motors). The driver circuit exists but no "
        "motor is fitted to it on this machine. The retained table leaves SolCallback(9) commented out (script line 483)."
    ),
    10: (
        "Energising it re-routes drives 1-8 from the coils (left set) to the flash lamps (right set); pinned PinMAME publishes the right set at 25-32 (s11.c updsol; "
        "tommyGameData's muxSol is 10). The coil table lists it as a '24v DC 10A OPDT' relay powered RED/WHT from PS CN3-5. The retained table leaves SolCallback(10) "
        "commented out (script line 484): its flash-lamp callbacks are bound to 25-32."
    ),
    11: (
        "There is no GI channel on this platform: the general illumination is solenoid 11, the G.I. relay on the power-supply board. s11.c types it "
        "CORE_MODOUT_BULB_44_6_3V_AC_REV (a reversed 6.3 VAC #44 bulb output) for Tommy (s11.c line 1243), so a consumer shows the GI lit while solenoid 11 is off; the "
        "retained table's GIRelay (SolCallback(11), script lines 485 and 2787-2835) turns its GI lights off while the solenoid is on. The bulb table lists 92 No. 44 and "
        "47 No. 555 bulbs without saying which are general illumination, and the lamp location page says G.I. lamps are not shown, so no quantity is claimed."
    ),
    12: (
        "The coil table prints the control wire 'BRY-YEL' (sic); the schematic and the wiring diagram draw it 'BRN/YEL' to the 'DIVERTER 27-1500'. The retained table binds "
        "SolCallback(12) = Diverter, which raises its TopDiverter wall while the solenoid is on and drops it when off (script lines 486 and 759-767)."
    ),
    13: (
        "The Playfield Coil/Flashlamp Wiring Diagram draws 'AIRPLANE MOTORS', two motor symbols in parallel on CPU CN12-6 (Q26, BLU/GRN), fed from the Shaker Motor Board "
        "J1-P4/5 (the coil table's power cell: 'SMB J3-P 1/3', '9v DC'). They turn the propellers of the Airplane Assembly (515-5949-00) above the playfield. The retained table "
        "binds SolCallback(13) = PropellerMove, which spins two propeller primitives while the solenoid is on (script lines 487 and 776-790)."
    ),
    14: (
        "The wiring diagram draws CPU CN12-7 (Q25, BRN/BLU) to the coil of a Relay Board 520-5010-00 whose normally open contact switches 28 VAC from BR2 to the mirror motor, "
        "so the motor runs while the solenoid is on. The Mirror Up & Down Test text names 'Q23 on the CPU' as the relay driver, where the coil table and both drawings print Q25 "
        "on drive 14 (Q23 is drive 16, unfitted); the sources agree on the device and its address and differ only on a transistor designator. The retained table binds "
        "SolCallback(14) = MirrorMove, which only picks a direction: when the solenoid turns on while the table's mirror rests at a limit it sets travel toward the other "
        "limit, and its always-running MirrorTimer then completes the whole stroke whether or not 14 stays on (script lines 488, 813-830 and 832-852). That is a "
        "completed-stroke approximation of a motor the manual runs only while the relay is energised."
    ),
    15: (
        "Flash lamp X1 'Tommy': the coil table's note 3 counts the X# lamps on the playfield and the rest of four in the insert, and the schematic and wiring diagram label the "
        "four bulbs '(1) PLFD (3) INSERT'. The Coil Test drawing places one '15' balloon at the mirror and three in the backbox flash-lamp drawing. s11.c types the output "
        "CORE_MODOUT_BULB_89_32V_DC_S11 for Tommy (line 1245). The retained table binds SolCallback(15) = FlashSol15 (Lampz 115, its mirror flasher; script lines 489, 1878 and 2583-2593)."
    ),
    16: "The coil table prints every cell of the row as dashes and the schematic draws Q23's '(BRN/GRY) N.C.' wire to 'NO COIL AT THIS LOCATION'. No load is fitted.",
}
for address in range(9, 17):
    row = DRV[f"{address:02d}"]
    kind, device_id, label, availability = DIRECT[address]
    notes = [f"Coil-table row {address:02d} prints '{row['Description']}'; the Coil Test index prints '{COIL['index'][f'{address:02d}']}'.", DIRECT_NOTES[address]]
    entry = {
        "id": device_id,
        "label": label,
        "kind": kind,
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": availability,
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([SCRIPT_REF] if address in (11, 12, 13, 14, 15) else [])),
        "physical": {"notes": " ".join(notes)},
    }
    if address != 16:
        entry["wiring"] = {
            "board": "PPB (Q1 TIP 36C), driven from CPU Q30" if address == 9 else "CPU Board",
            "driver_transistor": "Q30" if address == 9 else row["Drive transistor"],
            "control_wire": row["Control line"].replace("BRY-YEL", "BRN-YEL"),
            "control_connection": row["Control connect"],
            "power_wire": row["Power line"],
            "power_connection": row["Power connection"],
        }
        if address == 9:
            entry["wiring"]["control_wire"] = "WHT/BRN"
            entry["wiring"]["control_connection"] = "CPU CN12-1"
    if address in (12, 13):
        entry["physical"]["part_number" if address == 12 else "assembly_part_number"] = "27-1500" if address == 12 else "515-5949-00"
    if address == 14:
        entry["physical"]["assembly_part_number"] = "500-5742-01"
    if address == 15:
        entry["physical"]["part_number"] = "#89"
        entry["physical"]["quantity"] = 4
    if address == 11:
        entry["roles"] = ["playfield.general-illumination"]
    if address in (9, 16):
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address == 10:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        located = spatial_for(entry["id"], "emitter" if address in (11, 15) else "effect", f"solenoid.{address}", PLACE_REFS)
        if located:
            entry["spatial"] = located
            if address != 15:
                entry["physical"]["notes"] += " The coordinate is the retained table's model of the mechanism this output drives, not a claimed winding or motor centre."
    outputs.append(entry)

# --- Solenoids 17-22: the CPU-controlled auxiliary (switched) solenoids --------------------------------------
AUX_IDS = {
    17: ("coil.top-left-turbo-bumper", "Top Left Turbo Bumper", "SolBumper1"),
    18: ("coil.top-center-turbo-bumper", "Top Center Turbo Bumper", "SolBumper2"),
    19: ("coil.top-right-turbo-bumper", "Top Right Turbo Bumper", "SolBumper3"),
    20: ("coil.left-slingshot", "Left Slingshot", "SolLSling"),
    21: ("coil.right-slingshot", "Right Slingshot", "SolRSling"),
}
for address in range(17, 23):
    row = DRV[str(address)]
    if address == 22:
        outputs.append({
            "id": "coil.unused-driver-22",
            "label": "Unfitted Auxiliary Driver 22",
            "kind": "virtual",
            "binding": {"group": "pinmame.output.solenoid", "device": address},
            "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
            "availability": "unused",
            "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC]),
            "physical": {"notes": (
                "The sixth switched solenoid. The coil table prints 'Coil: Not Used' with dashes for transistor, board and control line, but keeps the generic cells "
                f"'{row['Control connect']}', '{row['Power connection']}', '{row['Power description']}' and '{row['Coil or flash type']}'; the Coil Test index prints 22 'NOT USED'. "
                "No device is fitted; the retained table binds nothing to 22."
            )},
            "spatial": not_applicable("unused", [MANUAL]),
        })
        continue
    device_id, label, callback = AUX_IDS[address]
    entry = {
        "id": device_id,
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"part_number": row["Coil or flash type"], "notes": (
            f"Coil-table row {address} prints '{row['Description']}'; the Coil Test index prints '{COIL['index'][str(address)]}'. One of the six switched solenoids: CORE_FIRSTSSSOL is 17 "
            "and Data East's PIA permutation publishes them at 17 + ssSolNo, which is not sequential, so the printed coil number and PinMAME's public address are different "
            "identities that only a ROM run can pair (see the ROM evidence below). Pinned PinMAME leaves sxx.ssSw empty, so none is publishable from a switch closure alone. "
            f"The retained table binds SolCallback({address}) = {callback} (script line {473 + address}), "
            + (
                "whose body is commented out (script lines 1164-1180): the table kicks the ball with the VPX bumper itself on contact and never consumes the solenoid."
                if address < 20 else
                "which raises the slingshot's threshold to 2500 while the solenoid is on and restores it when off (script lines 941-947 and 968-974): the table kicks the ball "
                "with the VPX slingshot on contact and uses the solenoid only to suppress a second kick."
            )
        )},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Drive transistor"],
            "control_wire": row["Control line"], "control_connection": row["Control connect"],
            "power_wire": row["Power line"], "power_connection": row["Power connection"],
            "nominal_voltage_v": 32, "voltage_type": "dc",
        },
    }
    located = spatial_for(entry["id"], "effect", f"solenoid.{address}", PLACE_REFS)
    if located:
        entry["spatial"] = located
    outputs.append(entry)

outputs.append({
    "id": "control.game-on",
    "label": "Game On / Switched Solenoid Enable",
    "kind": "control_signal",
    "binding": {"group": "pinmame.output.solenoid", "device": 23},
    "aliases": aliases("pinmame.solenoid", 23, "coil", LEGACY_COILS),
    "availability": "used",
    "provenance": prov("validated", [S11_C, S11_H, SCRIPT_REF]),
    "physical": {"notes": (
        "S11_GAMEONSOL is 23, driven by PIA0 CB2 (s11.c pia0cb2_w). It enables the switched solenoids and gates the flippers rather than driving a device of its own; "
        "core_updateSw passes it to the flipper synthesis as the enable. The retained table binds SolCallback(23) = SolEnableFlips, which lets its flippers move only while it "
        "is on (script lines 495 and 1494-1496)."
    )},
    "spatial": not_applicable("virtual", [S11_C]),
})
outputs.append({
    "id": "virtual.unused-24",
    "label": "Unused Solenoid 24",
    "kind": "virtual",
    "binding": {"group": "pinmame.output.solenoid", "device": 24},
    "aliases": [{"namespace": "pinmame.solenoid", "value": "24"}],
    "availability": "unused",
    "provenance": prov("validated", [S11_C]),
    "physical": {"notes": "Reserved slot between the switched solenoids and the muxed right set; s11.c publishes nothing here."},
    "spatial": not_applicable("unused", [S11_C]),
})

# --- Solenoids 25-32: the right half of the relay pair, all flash lamps ------------------------------------------
SCRIPT_FLASH = {
    25: "Setlamp 125 (Lampz 125, the six bottom-arch flasher objects F25A-F25R; script lines 496 and 1880-1885)",
    26: "Flash26 (Lampz 126 and flasher dome 1; script lines 497, 1886-1888 and 2343-2350)",
    27: "Flash27 (Lampz 127, the left-scoop flasher; script lines 498, 1889 and 2352-2359)",
    28: "FlashSol28 (Lampz 128; script lines 499, 1890-1891 and 2651-2661)",
    29: "Setlamp 129 (Lampz 129, the bumper flashers; script lines 500 and 1892-1894)",
    30: "Flash30 (flasher domes 3-6 on the back panel; script lines 501 and 2361-2368)",
    31: "FlashSol31 (Lampz 131; script lines 502, 1895-1899 and 2704-2714)",
    32: "Flash32 (Lampz 132; script lines 503, 1900-1903 and 2370-2377)",
}
for address in range(25, 33):
    drive = address - 24
    row = DRV[f"{drive}R"]
    drawn = SCHEM[drive]["Bulb note as drawn"]
    name = row["Description"].split(": ", 1)[1]
    on_playfield = int(name.split(" ", 1)[0].lstrip("X"))
    entry = {
        "id": f"flasher.{drive}r",
        "label": f"Flash Lamps {drive}R ({COIL['index'][f'{drive}R']})",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, SCRIPT_REF, RUNTIME_SRC]),
        "physical": {
            "part_number": "#89",
            "quantity": 4,
            "notes": (
                f"Right half of the Left/Right relay pair on drive {drive}; the left half is published at address {drive}. The coil table prints 'Flashlamp: {name}', and its note 3 "
                f"reads the X count as the flash lamps on the playfield, the remainder of four being in the insert: {on_playfield} outside the insert"
                + ("" if on_playfield == 4 else f" and {4 - on_playfield} in the backbox insert") + f". The coil chart schematic labels the four No. 89 bulbs '{drawn}'. "
                "PinMAME types the whole 25-32 block as eight No. 89 flashers (s11.c line 1244). "
                f"The retained table binds SolCallback({address}) = {SCRIPT_FLASH[address]}."
            ),
        },
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Drive transistor"],
            "control_wire": row["Control line"], "control_connection": row["Control connect"],
            "power_wire": row["Power line"], "power_connection": row["Power connection"],
            "nominal_voltage_v": 32, "voltage_type": "dc",
        },
    }
    if drive == 6:
        entry["physical"]["notes"] += " 'Back Panel' is the playfield's rear panel: all four bulbs are on it and none in the insert."
    if drive == 4:
        entry["label"] = "Flash Lamps 4R (Eject)"
        entry["physical"]["notes"] += (
            " The coil table and the schematic call the playfield pair 'Upper Right', but the Flash Lamp / Coil Tests location drawing on printed page 36 puts both 4R "
            "balloons at the upper left beside the eject, the ROM names the group 'INS X2 EJECT X2' (below), and the retained table's two lamps for 28 sit there too; the "
            "location follows the drawing and the ROM, and the table name is read as a misprint."
        )
    located = spatial_for(entry["id"], "emitter", f"solenoid.{address}", PLACE_REFS)
    if located:
        entry["spatial"] = located
        if len(located["placements"]) != on_playfield:
            entry["physical"]["notes"] += (
                f" The retained table models {len(located['placements'])} lit object(s) for this flasher where the manual counts {on_playfield} outside the insert; the placements "
                "are the table's modelled domes and lenses, not a socket survey."
            )
    outputs.append(entry)

# --- 33-36: inert on this generation ------------------------------------------------------------------------------
for address in range(33, 37):
    outputs.append({
        "id": f"virtual.inert-{address}",
        "label": f"Inert Solenoid Address {address}",
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": (
            "core_getSol serves 33-36 only for the WPC and SAM generations (driver-specific flipper and game-on remaps); tommyGameData is GEN_DEDMD32, so the address always reads 0."
        )},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- 37-44: PIA2 port B, the CN3 printer data lines, which carry the blinder servo signals on this machine --------
PRINTER_PINS = {0: 9, 1: 8, 2: 7, 7: 1}
BLINDER = {
    "lines": {
        "44": {"note": (
            "ROM evidence (US 4.00): this is the only one of 37-44 that ever changed in the retained runs. Holding Start in the Arch Test drives it for as long as Start is held "
            "and the screen's ARCH STATUS reads ON, releasing Start drops it, and at power-up the ROM drives it once for about 0.7 s, which matches the adjustment procedure's "
            "'TURN ON POWER TO TEST. THE BLINDER ASS'Y WILL CYCLE'. PinMAME copies it to custom solenoid 51 in the same update. The line is therefore the blinder's "
            "commanded position: 1 puts the blades out over the flippers. Pressing Start on Adjustment 56 PRINTER INTERFACE ('PRESS START TO PRINT') changed nothing from 37 to 44."
        )},
    },
    "unobserved_note": (
        "ROM evidence (US 4.00): the line never changed in any retained run - the service tests, the Arch Test, a game start, and Start pressed three times on Adjustment 56 "
        "PRINTER INTERFACE ('PRESS START TO PRINT', which the manual says lets the operator print by pressing Start) - while 44 moved with the blinder. The manual draws the "
        "servo board's CLEAR, DATA and CLOCK inputs, but the source pins of those wires are not legible on the retained scan, so which CN3 lines feed the board is not "
        "established, and failure to observe a change does not prove that the line is unused. Its availability stays unknown."
    ),
    "servo_note": (
        "ROM evidence (US 4.00): the Arch Test drives 51 together with 44 while Start is held, and the power-up drives both once for about 0.7 s; no switch in 1-64 or "
        "81-88 changes the Arch Test's ARCH STATUS, so the blinder has no sensor the ROM reads."
    ),
}
for index, address in enumerate(range(37, 45)):
    pin = PRINTER_PINS.get(index)
    pin_text = (
        f"CN3 pin {pin}" if pin is not None else
        "a CN3 pin the comment elides: it states pins 9, 8 and 7 for bits 0-2 and pin 1 for bit 7, so bits 3-6 occupy four of pins 2-6"
    )
    observed = BLINDER["lines"].get(str(address))
    notes = (
        f"tommyGameData sets gameSpecific1 = S11_PRINTERLINE, so s11.c's pia2b_w publishes PIA2 port B bit {index} here as the extSol bit that core_getSol reads at 37 + {index} "
        f"({pin_text}; the comment heads the list 'CN3 Printer Data Lines (Used by various games)' and names bit 7, CN3 pin 1, 'Blinder on Tommy'). On this machine the "
        "manual's coil chart schematic draws the Servo Motor Interface Board's seven-pin input P2 with CLEAR, DATA and CLOCK lines from the CPU board beside its supplies, and the "
        "Pinball Servo Controller text says the board latches the DATA level on a CLOCK transition into one flip-flop that sets the servo's pulse width, CLEAR resetting it. "
    )
    notes += observed["note"] if observed else BLINDER["unobserved_note"]
    outputs.append({
        "id": f"virtual.cn3-line-{address}",
        "label": f"CN3 Printer/Servo Data Line {index}" + (f" (CN3 pin {pin})" if pin is not None else ""),
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "used" if observed else "unknown",
        "provenance": prov("validated" if observed else "candidate", [CORE_C, S11_C, MANUAL, RUNTIME_SRC]),
        "physical": {"notes": notes},
        "spatial": not_applicable("virtual", [S11_C]),
    })

# --- 45-48: PinMAME's synthetic lower flipper outputs ---------------------------------------------------------------
FLIPPERS = {
    45: ("Synthetic Lower Right Flipper Power", "right"), 46: ("Synthetic Lower Right Flipper Hold", "right"),
    47: ("Synthetic Lower Left Flipper Power", "left"), 48: ("Synthetic Lower Left Flipper Hold", "left"),
}
for address, (label, side) in FLIPPERS.items():
    row = _LEFT_ROW if side == "left" else _RIGHT_ROW
    notes = (
        "Not a CPU-driven output on this machine. tommyGameData declares no FLIP_SOL, so core.c's core_updateSw synthesises these bits whenever the switched-solenoid enable "
        f"(public 23) is on and the corresponding cabinet button bit of PinMAME's flipper column is set: public {82 if side == 'right' else 84}, the same bit it copies into matrix "
        f"switch {64 if side == 'right' else 63}. Power and hold therefore assert and release together and are not independently controllable; a recreation must not model them as "
        "two coils. The physical coils are driven from the Solid State Flipper Board, whose printed Flipper Solenoids table lists a Left Flipper (22-1080), a Right Flipper Lower "
        "(22-1080) and a third row printed 'Left Flipper Upr.' (25-1800). That third row's label puts the upper flipper on the left, as the Major Assemblies list (item 5, Flipper "
        "Assembly Upper Left 500-5795-02) and the Cabinet Parts list (item 15, 'Flipper Switch, Double, Left Top/Bottom') do, yet its flipper-ground cell repeats the right "
        f"lower flipper's '{_RIGHT_ROW['CPU to flipper switch']}' while its power pins repeat the left flipper's '{_UPPER_ROW['Power line, Flip. PCB to coil']}'; the row's wires "
        "are internally inconsistent and are not used for the upper flipper. PinMAME synthesises nothing for the upper left flipper; it moves with the left button. "
    )
    if address in (46, 48):
        notes += (
            f"The retained table binds SolCallback({address}) = {'SolRFlipper' if address == 46 else 'SolLFlipper'} (script lines {504 if address == 46 else 506} and "
            f"{'1516-1532' if address == 46 else '1498-1514'}), firing its flipper only while SolEnableFlips has seen 23 on."
        )
    elif address == 47:
        notes += (
            "The retained table sets vpmFlips.FlipperSolNumber(2) = 47 (script line 279) and leaves SolCallback(47) = SolULFlipper commented out (line 505); with its "
            "StagedFlipper option 0 it moves its upper left flipper straight from the left flipper key (script lines 158-176 and 230-236)."
        )
    else:
        notes += "The retained table binds nothing to 45."
    outputs.append({
        "id": f"virtual.flipper-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, CORE_H] + ([SCRIPT_REF] if address != 45 else [])),
        "physical": {"part_number": row["Coil type"], "notes": notes},
        "wiring": {
            "board": "Solid State Flipper Board", "control_wire": row["CPU to flipper switch"].split(" ")[0],
            "control_connection": row["CPU to flipper switch"].split(" ", 1)[1],
            "power_wire": row["Power line, Flip. PCB to coil"].split(" ")[0],
            "power_connection": row["Power line, Flip. PCB to coil"].split(" ", 1)[1],
        },
        "spatial": not_applicable("virtual", [MANUAL, CORE_C]),
    })
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL (51)."),
):
    outputs.append({
        "id": f"virtual.reserved-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": note},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- 51: the blinder, PinMAME's one custom solenoid ------------------------------------------------------------------
_blinder = {
    "id": "servo.blinder",
    "label": "Blinder Servo",
    "kind": "servo",
    "binding": {"group": "pinmame.output.solenoid", "device": 51},
    "aliases": aliases("pinmame.solenoid", 51, "coil", LEGACY_COILS),
    "availability": "used",
    "provenance": prov("validated", [CORE, CORE_H, CORE_C, MANUAL, SCRIPT_REF, RUNTIME_SRC]),
    "physical": {
        "assembly_part_number": PARTS["assemblies"]["16"]["Part No."],
        "notes": (
            "tommyGameData declares one custom solenoid (custSol = 1) and a getSol handler, tommy_getSol, that returns core_getSol(44) > 0 for sBlinderMotor = "
            "CORE_CUSTSOLNO(1); core.h defines CORE_CUSTSOLNO(n) as CORE_FIRSTCUSTSOL - 1 + n with CORE_FIRSTCUSTSOL 51, so the public address is 51 (degames.c's "
            "comment beside the define says 33, which the pinned arithmetic does not produce). Address 51 is therefore PinMAME's copy of CN3 data line 7 (public 44), "
            "not a separate driver. The physical device is the Blinder Assembly (Major Assemblies item 16, 'Under Arch, Above Playfield'): a radio-control servo on the "
            "Pinball Servo Controller board, which the manual's Arch Motor Test describes as a feature that covers the lower flippers. The board holds one latched bit: DATA "
            "strobed in gives the minimum servo pulse width (set by pot R2, which the adjustment procedure uses for the 'open' alignment, the blades out over the flippers) and "
            "DATA cleared the maximum (pot R5, the 'closure' alignment, the blades folded in so they protrude no more than 3/16 inch beyond the arch wall). The blinder has two "
            "commanded positions and no position feedback switch. The retained table binds SolCallback(51) = BlinderMove, which swings its two blinder blades out over the "
            "flipper area, making them collidable, while the solenoid is on and folds them back under the arch when it turns off (script lines 507 and 895-922). "
            f"{BLINDER['servo_note']}"
        ),
    },
}
_located = spatial_for("servo.blinder", "effect", "solenoid.51", PLACE_REFS)
if _located:
    _blinder["spatial"] = _located
    _blinder["physical"]["notes"] += (
        " The coordinates are the mesh-bounds centres of the retained table's two blinder blades in their stored pose; the table models the blades hinged under the bottom arch "
        "and its mesh extends past the playfield's front edge, so the placement is approximate."
    )
outputs.append(_blinder)

# --- Lamps 1-64 ------------------------------------------------------------------------------------------------
for address in range(1, 65):
    chart = LAMP["chart"][address]
    location = LAMP["location"][address]
    suffix, label = sem.LAMPS[address]
    notes = [
        f"Printed lamp-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}' and the location table '{location['description']}'"
        + (f" (marked '{location['marker']}')." if location["marker"] else ".")
    ]
    if address == 42:
        notes.append("The chart prints the cell number 41 in this cell, a misprint: its column and row make it 42 and the location table lists 42 as '...O (Playfield)'.")
    if address == 22:
        notes.append("The chart prints 'RT. Ramp S-U Top' where the location table prints 'Left Ramp Stand-Up Top'; the ROM's own name for the lamp is below.")
    if address in sem.BACKBOX_LAMPS:
        notes.append(
            "A backbox insert lamp: the location table marks it '**' (Location - Backbox (Insert)) and 'Insert X2', and the Backbox Insert Locations drawing shows two balloons "
            "for it, so the address drives two bulbs behind the backglass's TOMMY letters. The retained table binds only virtual-reality backglass bulbs to it."
        )
    if address in sem.TWO_BULB_LAMPS:
        notes.append("The location table prints 'X2' and the location drawing places two balloons for it, one at each side of the playfield, so the address drives two playfield bulbs.")
    if address in (39, 40, 60, 61):
        notes.append("The location table refers this lamp to its note 1, 'RAMPS ARE NOT SHOWN': the bulb is on a ramp.")
    if address == 56:
        notes.append("The location table refers this lamp to its note 2, 'AIRPLANE IS NOT SHOWN': the bulb is on the airplane above the playfield.")
    if address in sem.CABINET_LAMPS:
        notes.append(
            "A cabinet lamp: the location table marks it '*' (Location - In Cabinet). "
            + ("It lights the Extra Ball button; the retained table reads Controller.Lamp(23) for its button primitive (script line 5048)."
               if address == 23 else "It lights the Start (Credit) button; the retained table reads Controller.Lamp(64) for its launch-button primitive (script line 5049).")
        )
    rom = ROM_LAMP.get(str(address))
    if rom:
        notes.append(
            f"ROM evidence (US 4.00 Lamp Test): the single-lamp test lights public lamp {address} under '{rom['name']}', wires {rom['wires']}, '#{address:02d}', and no other lamp."
        )
    else:
        notes.append(
            f"ROM evidence (US 4.00): the single-lamp Lamp Test steps over this address in both directions, so it prints no name for it, but the Row and Column lamp tests "
            f"light it with the rest of its row and column ({' and '.join(ROW_COLUMN[str(address)])}), so the ROM drives it."
        )
    entry = {
        "id": f"lamp.{suffix}",
        "label": label,
        "kind": "lamp",
        "binding": {"group": "pinmame.output.lamp", "device": address},
        "aliases": aliases("pinmame.lamp", address, "lamp", LEGACY_LAMPS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": chart["drive"]["wire"],
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
            "return_component": chart["return"]["transistor"],
        },
    }
    if address in sem.BACKBOX_LAMPS or address in sem.TWO_BULB_LAMPS:
        entry["physical"]["quantity"] = 2
    if address in sem.CABINET_LAMPS:
        entry["roles"] = [sem.CABINET_LAMPS[address]]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address in sem.BACKBOX_LAMPS:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        located = spatial_for(entry["id"], "emitter", f"lamp.{address}", PLACE_REFS)
        if located:
            entry["spatial"] = located
    outputs.append(entry)

# --- ROM evidence on the outputs ---------------------------------------------------------------------------------
_BY_ADDRESS: dict[int, list[dict]] = {}
for _entry in COIL_TEST:
    for _number in _entry["fired"]:
        if _number != 10 or _entry["number"] == "#10":
            _BY_ADDRESS.setdefault(_number, []).append(_entry)
_SILENT = {_entry["number"]: _entry for _entry in COIL_TEST if not _entry["fired"]}


def rom_output_note(address: int) -> str | None:
    """The ROM's own name and the Coil Test's response for one public solenoid address."""
    sentences = []
    for entry in _BY_ADDRESS.get(address, []):
        relay = " with the relay at 10 turned on first" if 10 in entry["fired"] and address != 10 else ""
        sentences.append(
            f"ROM evidence (US 4.00 Coil Test): entry {entry['number']} is named '{entry['name']}' with the wires '{entry['wires']}', and pressing Start on it fires public "
            f"{address}{relay} and nothing else."
        )
    if address in CYCLE:
        sentences.append(f"The automatic Cycling Coils test fires public {address} as step {CYCLE.index(address) + 1} of its {len(CYCLE)}-step cycle.")
    if address in (7, 9):
        sentences.append(
            "The ROM itself names the entry NOT USED: firing it is the test sweeping every driver, so the pulse does not make the address a fitted device."
        )
    if address in (16, 22):
        entry = _SILENT[f"#{address}"]
        sentences.append(
            f"ROM evidence (US 4.00 Coil Test): entry #{address} is named '{entry['name']}' ('{entry['wires']}'), and pressing Start on it fires nothing; Cycling Coils skips it."
        )
    if address == 10:
        sentences.append(
            "ROM evidence (US 4.00): the Coil Test has no entry #10; each R entry turns public 10 on before it fires its flash lamps, and Cycling Coils asserts 10 before each of 25-32."
        )
    return " ".join(sentences) or None


for entry in outputs:
    group, address = entry["binding"]["group"], entry["binding"]["device"]
    if group == "pinmame.output.solenoid":
        note = rom_output_note(address)
        if note:
            entry["physical"]["notes"] += " " + note
            if RUNTIME_SRC not in entry["provenance"]["source_refs"]:
                entry["provenance"]["source_refs"].append(RUNTIME_SRC)

# --- Displays ---------------------------------------------------------------------------------------------------
displays = [{
    "id": "display.dmd",
    "label": "128x32 Dot Matrix Display",
    "kind": "dmd",
    "controller_index": 0,
    "width": 128,
    "height": 32,
    "physical_location": "cabinet_or_service",
    "provenance": prov("validated", [CORE, MANUAL]),
    "spatial": not_applicable("cabinet_or_service", [CORE, MANUAL]),
}]

# --- Mechanisms --------------------------------------------------------------------------------------------------
ASM = PARTS["assemblies"]
MECH_REFS = [MANUAL, SCRIPT_REF]
mechanisms = [
    {
        "id": "mechanism.ball-trough",
        "label": "Six-Ball Trough, Lockout and Ball Eject",
        "kind": "kicker",
        "actuators": ["coil.six-ball-lockout", "coil.ball-eject"],
        "sensors": [f"switch.{sem.SWITCHES[a][0]}" for a in range(9, 16)],
        "assembly_part_number": ASM["1"]["Part No."],
        "behavior": (
            "Seven trough switches, Ball Trough #1 Left at 9 through #7 Right at 15, all part 180-5119-00 except 15 (180-5118-00), with the shooter lane switch 16 after them. "
            f"The Major Assemblies list names a 6-Ball Switch Assembly ({ASM['1']['Part No.']}, under the playfield), a Lock Ball Assembly ({ASM['2a']['Part No.']}, under the arch, "
            f"above the playfield) and a Deflector for the 6-Ball Ass'y ({ASM['2b']['Part No.']}, under the arch); the coil tables give drive 1 to the '6-Ball Ass'y Lockout' (25-1240) "
            "and drive 2 to the Ball Eject (23-800, drawn as BALL RELEASE). The retained table rests six balls on kickers 9-14, kicks the ball at 14 toward 15 and closes 15 when drive 1 "
            "fires (SolTrough), and kicks the ball at 15 into the shooter lane and opens 15 when drive 2 fires (SolRelease); its trough is a surrogate and the physical lockout's timing "
            "is not measured. The manual's Easy Trough Clear test lets the technician empty the trough with either flipper button."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.auto-ball-launch",
        "label": "Auto Ball Launch and Manual Shooter",
        "kind": "kicker",
        "actuators": ["coil.auto-ball-launch"],
        "sensors": ["switch.shooter-lane"],
        "assembly_part_number": ASM["8"]["Part No."],
        "behavior": (
            f"The Shooter/Kicker Assembly (Auto Ball Launch, {ASM['8']['Part No.']}) fires the Auto Ball Launch coil (drive 3, 22-600 through the +50 V booster) to send a ball "
            f"up the shooter lane, beside a conventional Shooter Assembly Long Shaft ({ASM['9']['Part No.']}) the player pulls. The shooter lane switch 16 senses a ball waiting. "
            "The instruction card's skill shot asks the player to plunge the ball into the secret hole behind the parachute. The retained table models both: a VPX plunger on the "
            "plunger key and a cvpmImpulseP auto-plunger on swPlunger fired by SolCallback(3)."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.vuk",
        "label": "Super VUK (Right)",
        "kind": "kicker",
        "actuators": ["coil.vuk"],
        "sensors": ["switch.vuk"],
        "assembly_part_number": ASM["11"]["Part No."],
        "behavior": (
            f"The Super VUK Assembly (Right, {ASM['11']['Part No.']}) holds a ball on the VUK Microswitch 19 (180-5064-00) until the VUK coil (drive 4, 23-800 through the +50 V "
            "booster) throws it up. The Mirror Up & Down Test text says the mirror is lowered 'to allow a shot to the Vertical Up Kicker (VUK) below the playfield'. In the retained "
            "table a ball entering the mirror trough (sw41) drops to the VUK kicker sw19 (sw41_Hit marks it as arriving through the subway, script lines 644-648), and ExitVUK on "
            "SolCallback(4) kicks it up."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.left-scoop",
        "label": "Left Scoop (Super VUK, Scoop Left)",
        "kind": "kicker",
        "actuators": ["coil.left-scoop"],
        "sensors": ["switch.left-scoop"],
        "assembly_part_number": ASM["12"]["Part No."],
        "behavior": (
            f"The Super VUK Assembly (Scoop Left, {ASM['12']['Part No.']}) holds a ball on the Left Scoop switch 23 (180-5116-00) until the Left Scoop coil (drive 5, 23-800) ejects it. "
            "The retained table kicks the ball out with ExitScoop on SolCallback(5) and offers its own option to send it toward the left or the right flipper (Scoop_kick), which is "
            "table tuning, not machine data."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.eject",
        "label": "Eject (Genius Hole)",
        "kind": "kicker",
        "actuators": ["coil.eject"],
        "sensors": ["switch.eject"],
        "behavior": (
            "The Eject switch 47 (Micro Switch, 180-5027-01) senses a ball in the eject hole at the upper left, and the Eject coil (drive 6, 24-940) kicks it out. The instruction card "
            "calls it the Genius Hole ('Shoot the \"eject\" to collect various Skill Level awards') and lights the Mystery award there from the right ramp. The retained table kicks the "
            "ball with SolEject on SolCallback(6)."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.mirror",
        "label": "Raising and Lowering Mirror",
        "kind": "motorized",
        "actuators": ["motor.mirror"],
        "sensors": ["switch.mirror-up", "switch.mirror-down", "switch.mirror-target", "switch.mirror-trough"],
        "assembly_part_number": ASM["14"]["Part No."],
        "behavior": (
            f"A Motor, Cam & Switch Assembly (Mirror, {ASM['14']['Part No.']}) with a Target Back Plate Assembly (Mirror, {ASM['15']['Part No.']}) raises and lowers the mirror, "
            "a target switch (Mirror Target 32, 180-5083-00). The motor runs on 28 VAC through a relay on Relay Board 520-5010-00 that drive 14 energises (the Mirror Motor Relay), "
            "and two limit switches, Mirror Up 28 and Mirror Down 31 (both 180-5052-00), tell the CPU where it is; the Mirror Up & Down Test says each limit switch closes just "
            "before the limit of travel and the two must never be closed together, and that holding Start energises the relay for as long as it is held, so the motor runs "
            "only while drive 14 is on and the ROM stops it on a limit switch. With the mirror lowered "
            "the ball can enter the Mirror Trough (41, under the playfield, entry marked ET) that leads to the VUK. The instruction card's multiball is 'Spell T-O-M-M-Y by shooting "
            "the mirror, then enter the mirror for 4-Ball Play'. IPDB lists a 'Raising/Lowering mirror' among the toys. The retained table approximates the motor with "
            "completed strokes: drive 14 turning on at a limit starts its MirrorP primitive toward the other limit, a timer finishes the stroke whether or not 14 stays on, "
            "28 and 31 close at the two ends and the target's collision drops when lowered. A recreation should instead move the mirror only while 14 is on. Travel speed "
            "is table tuning, not machine data."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.blinder",
        "label": "Flipper Blinder",
        "kind": "motorized",
        "actuators": ["servo.blinder"],
        "sensors": [],
        "assembly_part_number": ASM["16"]["Part No."],
        "behavior": (
            f"The Blinder Assembly ({ASM['16']['Part No.']}, under the arch, above the playfield) is a pair of blades, the manual's top and bottom blades, on a link arm driven by a "
            "radio-control servo; IPDB describes 'flipper blinders [that] extend from under metal apron to cover flipper area from player's view'. The Pinball Servo Controller board "
            "latches one CPU data bit (DATA clocked in by CLOCK, reset by CLEAR) and turns it into a free-running 18 ms servo pulse of a minimum or a maximum width, each set by a "
            "pot, so the blades have two commanded positions: out over the lower flippers (the procedure's 'open', pot R2) and folded in under the arch (its 'closure', pot R5). "
            "There is no position feedback. The manual's Arch Motor Test moves the blinder out while Start is held and back when it is released. PinMAME publishes the latched "
            "state's source line at 44 and copies it to custom solenoid 51; the retained table swings its blades out while 51 is on."
        ),
        "provenance": prov("candidate", MECH_REFS + [CORE]),
    },
    {
        "id": "mechanism.airplane",
        "label": "Captain Walker's Airplane",
        "kind": "toy",
        "actuators": ["motor.airplane"],
        "sensors": [],
        "assembly_part_number": ASM["17"]["Part No."],
        "behavior": (
            f"The Airplane (Bomber) Assembly ({ASM['17']['Part No.']}) spans the upper playfield; the wiring diagram draws two airplane motors in parallel on drive 13, powered "
            "from the Shaker Motor Board, which turn its propellers. Lamp 56 (Airplane) is on the airplane. IPDB lists 'Captain Walker's airplane' among the toys. The retained "
            "table spins two propeller primitives while drive 13 is on and lets them run down when it turns off."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.top-diverter",
        "label": "Top Diverter",
        "kind": "diverter",
        "actuators": ["coil.top-diverter"],
        "sensors": [],
        "behavior": (
            "The Top Diverter coil (drive 12, 27-1500) moves a diverter at the top of the playfield. No switch senses it. The retained table raises its TopDiverter wall while the "
            "solenoid is on and drops it when off, so the diverter is a held output rather than a pulse."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.turbo-bumpers",
        "label": "Turbo Bumpers",
        "kind": "other",
        "actuators": ["coil.top-left-turbo-bumper", "coil.top-center-turbo-bumper", "coil.top-right-turbo-bumper"],
        "sensors": ["switch.left-turbo-bumper", "switch.center-turbo-bumper", "switch.right-turbo-bumper"],
        "assembly_part_number": ASM["7"]["Part No."],
        "behavior": (
            f"Three pop bumpers (Turbo Bumper, X3, {ASM['7']['Part No.']}) sensed at 49-51 (part 180-5015-01) and fired by the Top Left, Top Center and Top Right Turbo Bumper coils "
            "(printed 17-19, 23-800). Pinned PinMAME's PIA permutation of the switched solenoids is not sequential, so the printed coil numbers alone do not give the public "
            "addresses; the ROM's own coil test pairs them."
        ),
        "positions": [
            {"id": "mechanism.turbo-bumpers.left", "label": "Left Turbo Bumper", "sensors": ["switch.left-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.center", "label": "Center Turbo Bumper", "sensors": ["switch.center-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.right", "label": "Right Turbo Bumper", "sensors": ["switch.right-turbo-bumper"]},
        ],
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.slingshots",
        "label": "Slingshots",
        "kind": "other",
        "actuators": ["coil.left-slingshot", "coil.right-slingshot"],
        "sensors": ["switch.left-slingshot", "switch.right-slingshot"],
        "assembly_part_number": ASM["6"]["Part No."],
        "behavior": (
            f"Two slingshot assemblies ({ASM['6']['Part No.']}) sensed at 17 and 18 (part 180-5023-00) and fired by the Left and Right Slingshot coils (printed 20 and 21, 23-800)."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.left-3-bank",
        "label": "Left 3-Bank Stand-Up Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.left-3-bank-bottom", "switch.left-3-bank-middle", "switch.left-3-bank-top"],
        "assembly_part_number": ASM["21a"]["Part No."],
        "behavior": (
            f"A bank of three round stand-up targets (3-Bank Target Round Ass'y Left, {ASM['21a']['Part No.']}) at 25-27, each with its own lamp (25-27). No reset coil: they are stand-ups."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.right-3-bank",
        "label": "Right 3-Bank Stand-Up Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.right-3-bank-top", "switch.right-3-bank-middle", "switch.right-3-bank-bottom"],
        "assembly_part_number": ASM["21b"]["Part No."],
        "behavior": (
            f"The mirror-image bank (3-Bank Target Round Ass'y Right, {ASM['21b']['Part No.']}) at 33-35, each with its own lamp (33-35). No reset coil."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.captive-ball",
        "label": "Captive Ball",
        "kind": "toy",
        "actuators": [],
        "sensors": ["switch.captive-ball-target"],
        "behavior": (
            "A captive ball whose target switch 43 (Captive Ball (Target Switch), 180-5114-08) scores when the captive ball is driven into it, on the right side of the playfield. "
            "The retained table creates the captive ball at its CaptiveBall kicker and releases it at start-up, and scores 43 from its target."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
]

_MECH_EVIDENCE = {
    "mechanism.ball-trough": {"status": "validated", "text": (
        f"ROM evidence (US 4.00 game start, host moving the balls): at power-up the ROM pulses drives 1-6 and the top diverter (12) once each. After Start with balls on 9-14 and 15 open it pulsed the "
        f"lockout (public 1) {SERVE['start_to_15_closed']['1']} times at about 1.2 s intervals, with occasional auto-launch (3) and ball-eject (2) pulses between them; once the host "
        f"closed 15 it stopped the lockout and pulsed the ball eject (2) {SERVE['while_15_closed']['2']} times until the host opened 15. So the lockout feeds a ball to the release "
        "position 15 and the eject kicks it from 15 into the shooter lane; the host moved the balls, so travel times are not measured. The Coil Test names public 1 'COIL: LOCK OUT' "
        "and 2 'COIL: BALL RELEASE'."
    )},
    "mechanism.auto-ball-launch": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Mirror and Arch tests): closing the shooter lane switch 16 fires public 3, which the Coil Test names 'COIL: AUTO LAUNCH 50V'. In the game start "
        "the ROM did not fire 3 while the served ball rested on 16; the player launches it."
    )},
    "mechanism.vuk": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Mirror and Arch tests): closing the VUK switch 19 fires public 4, which the Coil Test names 'COIL: VUK'."
    )},
    "mechanism.left-scoop": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Mirror and Arch tests): closing the Left Scoop switch 23 fires public 5, which the Coil Test names 'COIL: LEFT SCOOP'."
    )},
    "mechanism.eject": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Mirror and Arch tests): closing the Eject switch 47 fires public 6, which the Coil Test names 'COIL: EJECT'."
    )},
    "mechanism.mirror": {"status": "validated", "text": (
        f"ROM evidence (US 4.00 Mirror test): the screen shows MIRROR UP, MIRROR DOWN and MIRROR TARGET, each reading ON when public 28, 31 and 32 respectively is held at 1, and "
        "'START ACTIVATES MOTOR'; holding Start drives public 14 (the Coil Test's 'MOTOR: MIRROR') for as long as it is held. In the game start, with neither limit switch "
        f"simulated, the ROM switched 14 on {SERVE['mirror_motor_first_on_s']} s after power-up and left it on until Start was pressed, the behaviour of a motor run until it "
        "reaches a limit switch that never closes. The run does not show which limit the ROM seeks at power-up."
    )},
    "mechanism.blinder": {"status": "validated", "text": BLINDER["servo_note"]},
    "mechanism.airplane": {"status": "validated", "text": (
        "ROM evidence (US 4.00): the Coil Test names public 13 'MOTOR: AIRPLANE', and the game-start intro runs it for about 5.7 s."
    )},
    "mechanism.top-diverter": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Coil Test): entry #12 'COIL: TOP DIVERTER' turns public 12 on and leaves it on until the next entry is selected, so the ROM holds the diverter rather than pulsing it."
    )},
    "mechanism.turbo-bumpers": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Coil Test and Active Switch Test): the ROM names public 17, 18 and 19 'COIL: LEFT POP BUMPER', 'CENTER POP BUMPER' and 'RIGHT POP BUMPER' and "
        "switches 49, 50 and 51 'LEFT/CENTER/RIGHT POP BUMPER', so the coils and skirts pair left, center and right, and the printed coil numbers are the public addresses."
    )},
    "mechanism.slingshots": {"status": "validated", "text": (
        "ROM evidence (US 4.00 Coil Test and Active Switch Test): the ROM names public 20 and 21 'COIL: LEFT SLINGSHOT' and 'COIL: RIGHT SLINGSHOT' and switches 17 and 18 LEFT and "
        "RIGHT SLINGSHOT."
    )},
}
for _mechanism in mechanisms:
    _sentence = _MECH_EVIDENCE.get(_mechanism["id"])
    if _sentence:
        _mechanism["behavior"] += " " + _sentence["text"]
        _mechanism["provenance"]["source_refs"].append(RUNTIME_SRC)
        _mechanism["provenance"]["status"] = _sentence["status"]

relationships = [
    {
        "id": f"relationship.left-right-relay-{drive}",
        "kind": "relay_gated",
        "source": "relay.left-right-relay",
        "destination": f"flasher.{drive}r",
        "provenance": prov("validated", [MANUAL, CORE, S11_C]),
    }
    for drive in range(1, 9)
] + [
    {
        "id": "relationship.cn3-line-44-to-blinder",
        "kind": "direct",
        "source": "virtual.cn3-line-44",
        "destination": "servo.blinder",
        "provenance": prov("validated", [CORE, CORE_C]),
    },
] + flipper_column_relationships(
    flip_swno=FLIP_SWNO, matrix_ids={63: "switch.left-flipper-copy", 64: "switch.right-flipper-copy"}, refs=(CORE_C, CORE_H),
)

conflicts: list[dict] = []

# --- Drivers -------------------------------------------------------------------------------------------------------
_root = ROM_SETS[ROOT_DRIVER]
drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root and the last factory firmware (4.00, display ROM tommydva.400). Every tomy_* set shares one tommyGameData (GEN_DEDMD32, de_128x32DMD, "
            "FLIP6364, one custom solenoid with tommy_getSol, sound board DE2S, DMD board DEDMD32, S11_PRINTERLINE, muxSol 10) and one set of five sound ROMs, so all seven "
            "present identical playfield hardware and identical public addresses. The 5.00 set is a 2016 community MOD, not factory firmware; it runs on this same machine."
        )
    else:
        differing = [(role, mine) for role, mine, theirs in zip(ROLES, roms, _root) if mine != theirs]
        note = ("Differs from the root in " + ", ".join(f"the {role} ROM ({rom})" for role, rom in differing) + ".") if differing else "Byte-identical ROM set to the root."
        note += " The shared tommyGameData means the address model is unchanged."
        if driver_id in ("tomy_201d", "tomy_h30"):
            note += " Labelled Dutch: a language firmware for the same hardware."
        if driver_id == "tomy_301g":
            note += " Labelled German: a language firmware for the same hardware."
        if driver_id == "tomy_102be":
            note += " Labelled Belgian: a regional firmware for the same hardware."
        if driver_id == "tomy_102":
            note += " An early factory revision; it uses the 3.00 display ROM (tommydva.300)."
        if driver_id == "tomy_500":
            note += (
                " PinMAME dates this set 2016: later community software for the same physical machine, not a new game. The retained known-working table runs this ROM "
                "(cGameName = tomy_500, script line 130, with tomy_400 kept as a commented alternative), so its callbacks are evidence about the MOD, which keeps the factory address map."
            )
    drivers.append({
        "id": driver_id,
        "description": DRIVER_LABELS[driver_id],
        "year": DRIVER_YEARS[driver_id],
        "manufacturer": "Data East",
        "flags": 0,
        "physical_compatibility": "identical",
        "variant_notes": note,
        **({} if driver_id == ROOT_DRIVER else {"clone_of": ROOT_DRIVER}),
    })
for _driver in drivers:
    for _role, _mine, _theirs in zip(ROLES, ROM_SETS[_driver["id"]], _root):
        if _mine != _theirs and _mine not in _driver["variant_notes"]:
            raise SystemExit(f"{_driver['id']}: {_role} ROM {_mine} differs from the root but the note omits it")

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_record(name: str, locator: str, **extra) -> dict:
    record = {
        "id": f"excerpt.tommy.{name.rsplit('.', 1)[0]}",
        "locator": locator,
        "path": f"evidence/excerpts/{KEY}/{name}",
        "sha256": file_sha256(EXCERPT_DIR / name),
    }
    record.update(extra)
    return record


CHECKED = {"method": "manual", "transcribed_by": "curator, read from native-resolution renders of the image-only scan; OCR was used only to find pages", "reviewed": True}
EXCERPTS_MANUAL = [
    excerpt_record("switch-matrix.md", "printed pages 32-33 (PDF 36-37), Switch Matrix Chart and the complete Switch Part Numbers table", **CHECKED),
    excerpt_record("lamp-matrix.md", "printed pages 34-35 (PDF 38-39), Lamp Matrix Chart and Lamp Matrix Location and Descriptions", **CHECKED),
    excerpt_record("coil-drivers.md", "printed pages 36-38 (PDF 40-42), Flash Lamp / Coil Tests index, the coil and flash-lamp table, Flipper Solenoids and the coil chart schematic", **CHECKED),
    excerpt_record("bulbs-and-assemblies.md", "printed pages 40 and 45 (PDF 44 and 49), Playfield - Major Assemblies and Lamp Board Layouts & Lamp Bulb Part Numbers", **CHECKED),
    excerpt_record("cabinet-and-motor-wiring.md", "printed pages 39 and 64 (PDF 43 and 71), Cabinet Parts Illustration and the motor circuits of the Playfield Coil/Flashlamp Wiring Diagram", **CHECKED),
    excerpt_record(
        "diagnostics-and-blinder-text.md",
        "printed pages 5 and 29-31 (PDF 9 and 33-35), instruction card, Game Diagnostics, Mirror Up & Down and Arch Motor tests; PDF 113 and 115-116, Pinball Servo Controller theory and blinder adjustment",
        **{**CHECKED, "transcribed_by": "curator, drafted from an OCR pass over the renders and corrected sentence by sentence against the render"},
    ),
]


def pin_source(identifier: str, filename: str, locator: str) -> dict:
    return {
        "id": identifier, "kind": "pinmame_core",
        "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/{filename}",
        "revision": REVISION, "sha256": PIN_FILE_SHA256[filename], "locator": locator,
        "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
    }


sources = [
    {
        "id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REVISION,
        "locator": "PinmameGetGames; src/wpc/degames.c lines 1158-1242 (tomy_400 root, six clones)", "license": "BSD-3-Clause",
        "attribution": "PinMAME contributors",
    },
    pin_source(CORE, "degames.c", "lines 77-80 (INITGAMES11 layout), 87-91 (FLIP6364), 1158-1172 (tommyGameData, sBlinderMotor, tommy_getSol) and 1173-1242 (tomy drivers and ROM sets)"),
    pin_source(CORE_H, "core.h", "lines 159 (FLIP_SWNO), 298-332 (output bands, CORE_FIRSTCUSTSOL 51, CORE_CUSTSOLNO, CORE_FLIPPERSWCOL)"),
    pin_source(CORE_C, "core.c", "lines 1778-1860 (core_updateSw flipper copies and synthetic outputs) and 2251-2302 (core_getSol, including the hw.getSol branch above 50)"),
    pin_source(S11_C, "s11.c", "lines 392-410 (pia2b_w printer lines, 'Blinder on Tommy'), 537-650 (setSSSol, updsol, muxing, game-on), 1242-1246 (Tommy output typing)"),
    pin_source(S11_H, "s11.h", "lines 30-60 (DE_COMPORTS), 89-93 (S11_GAMEONSOL, DE_SWADVANCE, DE_SWUPDN)"),
    {
        "id": MANUAL, "kind": "manual",
        "uri": MANUAL_URL,
        "locator": f"{MANUAL_NAME}; printed pages 5-64 and the unnumbered blinder section (PDF 9-71 and 113-117); IPDB-hosted scan of Data East Pinball, Inc.'s 1994 manual, 117 pages, image-only",
        "sha256": MANUAL_SHA256, "original_filename": MANUAL_NAME,
        "acquired_at": "2026-10-09T15:41:00Z",
        "excerpts": EXCERPTS_MANUAL,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Data East Pinball, Inc.; hosted by the Internet Pinball Machine Database",
    },
    {
        "id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2579",
        "locator": (
            "IPDB machine #2579, 'The Who's Tommy Pinball Wizard' (Data East Pinball, Incorporated), date of manufacture January 08, 1994, model number 500-5528-01, MPU DataEast/Sega "
            "Version 3, 4,700 units (confirmed); notable features: three flippers, three pop bumpers, six-ball multiball, flipper blinders that extend from under the metal apron to "
            "cover the flipper area from the player's view, unlimited buy-in balls; toys: Captain Walker's airplane and a raising/lowering mirror. The notes describe ten "
            f"pre-production prototypes with six pop bumpers. Retained Wayback capture {IPDB_CAPTURE}. Identity cross-checked against the manual's title, the PinMAME driver "
            "description and the retained table's header ('IPDB No. 2579')."
        ),
        "sha256": IPDB_SHA256, "acquired_at": "2026-10-09T15:41:00Z",
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
    },
    {
        "id": RUNTIME_SRC, "kind": "runtime_scenario",
        "uri": "internal:" + RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "locator": FACTS["source_locator"],
        "revision": REVISION, "sha256": file_sha256(RUNTIME_EVIDENCE_PATH),
        "license": "NOASSERTION", "attribution": "Primary curator; legally supplied user ROMs",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": "external:vpx-sources/data-east/the-who-s-tommy-pinball-wizard/vpw-mod-1.2.1/The%20Who%27s%20Tommy%20Pinball%20Wizard%20%28Data%20East%201994%29%20VPWMod%201.2.1.vpx",
        "locator": f"retained known-working recreation, VPW Mod 1.2.1 of ninuzzu's VPX table; playfield 952 x 2162; runs cGameName tomy_500",
        "sha256": TABLE_SHA256, "known_working": True, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "ninuzzu (table recreation) and the VPW team credited in the script header",
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": "external:vpx-sources/data-east/the-who-s-tommy-pinball-wizard/vpw-mod-1.2.1/extracted/script.vbs",
        "locator": "table script; key handling (lines 145-264), SolCallback map (lines 476-507), switch handlers, mirror and blinder animation (lines 806-922), Lampz binding (lines 1680-1903)",
        "sha256": SCRIPT_SHA256, "known_working": True, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "ninuzzu and the VPW team credited in the script header",
    },
    {
        "id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI,
        "original_filename": "de.vbs", "sha256": VPM_DE_SHA256, "acquired_at": "2026-09-25T23:32:01Z",
        "locator": (
            "The VPinMAME script library the retained table loads at runtime (script.vbs line 105 LoadVPM \"02000000\", \"de.vbs\", 3.5; de.vbs executes core.vbs), retained from the "
            f"contributor's working installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). de.vbs defines swLRFlip = 82 and swLLFlip = 84 and sets them from the flipper "
            "keys in vpmKeyDown/vpmKeyUp, and names the staged upper flipper keys swURFlip/swULFlip at 86 and 88."
        ),
        "license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
        "excerpts": [excerpt_record("vpm-script-library-flippers.md", "de.vbs lines 21-36, 62-111; core.vbs lines 2090 and 2862-2865; script.vbs lines 34, 105, 129-130, 145-264, 279, 284-285, 495, 504-507", **{**CHECKED, "transcribed_by": "curator, read from the script files"})],
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": "external:vpx-sources/data-east/the-who-s-tommy-pinball-wizard/vpw-mod-1.2.1/extracted/manifest.json",
        "locator": (
            f"vpxtool extraction of the retained table, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, with the canonical external-evidence manifest "
            f"(manifest.json SHA-256 {EXTRACTION_MANIFEST_SHA256}, recomputable with tools/build_external_evidence_manifest.py --game tomy_500)"
        ),
        "sha256": EXTRACTION_MANIFEST_SHA256, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "ninuzzu and the VPW team credited in the script header",
    },
    {
        "id": LEGACY, "kind": "legacy_json", "uri": "https://github.com/vpinball/pinmame-game-defs", "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
        "locator": "games/tommy.json; origin=vbscript-parser", "attribution": "pinmame-game-defs contributors",
    },
]

# --- Coverage ---------------------------------------------------------------------------------------------------------
# Every requirement whose evidence is not complete, each with the device or record that keeps it open:
# input_semantics, the W7 jumper whose meaning no retained source states;
# output_semantics, CN3 data lines 37-43, which no retained run or legible page assigns;
# polarity, the Green FORWARD/REVERSE button (-6);
# spatial_placement, every placement observed from one recreation lineage; the GI emitters are not placed.
MISSING = ["input_semantics", "output_semantics", "polarity", "spatial_placement"]
DIMENSIONS = {
    "catalog_identity": "validated",
    "address_enumeration": "validated",
    "semantic_naming": "observed",
    "physical_wiring": "observed",
    "mechanisms": "validated",
    "variant_coverage": "validated",
    "recreation_knowledge": "validated",
    "runtime_observation": "observed",
    "causal_exercise": "observed",
    "spatial_placement": "observed" if PLACES["placements"] else "unknown",
}

definition = {
    "format": "pinmame-machine-definition",
    "schema_version": 2,
    "machine": {
        "id": KEY,
        "name": "The Who's Tommy Pinball Wizard",
        "manufacturer": "Data East",
        "year": 1994,
        "kind": "physical_pinball",
        "model_number": "500-5528-01",
        "ipdb_id": 2579,
        "opdb_id": "GR6do-MLBq4",
        **({"playfield": {
            "width": PLACES["table_bounds"]["width"], "height": PLACES["table_bounds"]["height"], "units": "vpx",
            "provenance": prov("observed", [TABLE]),
        }} if PLACES["table_bounds"] else {}),
    },
    "controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x4000", "inversion_applied_by_emulator": True},
    "coverage": {"status": "partial", "dimensions": DIMENSIONS, "missing": MISSING},
    "drivers": drivers,
    "inputs": inputs,
    "outputs": outputs,
    "displays": displays,
    "mechanisms": mechanisms,
    "relationships": relationships,
    "conflicts": conflicts,
    "sources": sources,
    "knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
}

# --- Spatial report ------------------------------------------------------------------------------------------------------
_placed = sum(len(d.get("spatial", {}).get("placements", [])) for d in inputs + outputs)
_no_spatial_key = sorted(d["id"] for d in inputs + outputs if "spatial" not in d and d["availability"] in ("used", "unknown"))
spatial_report = {
    "format": "pinmame-spatial-blockers",
    "version": 1,
    "machine_id": KEY,
    "status": "partial",
    "coordinate_convention": (
        "x = 0 is the left side and x = 1 the right side; y = 0 is the rear and y = 1 the apron end, normalized against the retained table's own playfield bounds "
        f"({PLACES['table_bounds']['width']:.0f} x {PLACES['table_bounds']['height']:.0f} VPX units, asserted rather than assumed)."
    ) if PLACES["table_bounds"] else "No coordinates are recorded yet.",
    "placement_count": _placed,
    "source": {"table": TABLE, "extraction": EXTRACTION, "extraction_file_count": EXTRACTION_FILE_COUNT, "extraction_manifest_sha256": EXTRACTION_MANIFEST_SHA256},
    "blockers": [
        {
            "id": "single-retained-recreation",
            "severity": "major",
            "detail": (
                "Exactly one known-working recreation is admitted as spatial evidence: the VPW Mod 1.2.1 of ninuzzu's table, which runs the tomy_500 MOD ROM. No second table "
                "from an independent lineage is retained, and no placement has been checked against the factory location drawings on printed pages 33, 35 and 36, so every "
                "placement stays `observed`."
            ),
        },
        {
            "id": "devices-without-a-retained-object",
            "severity": "major",
            "detail": "These used or unresolved devices have no honest coordinate in the retained recreation, so their spatial key is omitted rather than fabricated.",
            "omitted_spatial_key_devices": _no_spatial_key,
        },
        {
            "id": "projections-and-approximations",
            "severity": "major",
            "detail": (
                "The mirror limit switches 28 and 31 are projected onto the mirror primitive; the airplane propellers, the blinder blades and the flasher domes use the "
                "world-space mesh-bounds centre of the table's primitives (the back-panel domes of 30R are on the rear wall, projected onto the playfield plane); the flasher "
                "placements are the table's modelled lenses and domes, not a socket survey."
            ),
        },
    ],
    "unresolved": PLACES.get("unplaced", []),
}

# --- Knowledge note ------------------------------------------------------------------------------------------------------
KNOWLEDGE_TEXT = KNOWLEDGE_TEMPLATE.read_bytes().decode("utf-8") if KNOWLEDGE_TEMPLATE.is_file() else ""
knowledge_note = KNOWLEDGE_TEXT.replace("{driver_count}", str(len(drivers))).replace("{placed}", str(_placed))


def build() -> dict:
    """Return the canonical definition assembled from the embedded literals."""
    return definition


def _comparable(payload: bytes) -> bytes:
    """``payload`` with CRLF folded to LF, so the comparison ignores line endings and nothing else."""
    return payload.replace(b"\r\n", b"\n")


def _definition_bytes() -> bytes:
    with tempfile.TemporaryDirectory() as scratch:
        probe = Path(scratch) / "definition.json"
        write_json(probe, definition)
        return probe.read_bytes()


def _artifacts() -> tuple[tuple[Path, bytes], ...]:
    report_bytes = (json.dumps(spatial_report, indent="\t", sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    definition_bytes = _definition_bytes()
    return (
        (DEFINITION_PATH, definition_bytes),
        (SEED_PATH, definition_bytes),
        (SPATIAL_REPORT_PATH, report_bytes),
        (KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
    )


def _write(root: Path) -> None:
    existing = root / f"machines/author-ready/data-east/{SLUG}.json"
    if existing.is_file() and definition["coverage"]["status"] != "author_ready":
        raise RuntimeError(f"refusing to curate while an author-ready artifact exists (preserved): {existing}")
    if not KNOWLEDGE_TEXT:
        raise RuntimeError(f"the knowledge template is missing: {KNOWLEDGE_TEMPLATE}")
    for path, payload in _artifacts():
        target = root / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as stream:
            stream.write(payload)


def _check(root: Path) -> None:
    for path, expected in _artifacts():
        target = root / path.relative_to(ROOT)
        if not target.is_file():
            raise RuntimeError(f"Tommy artifact is missing: {target}")
        if _comparable(target.read_bytes()) != _comparable(expected):
            raise RuntimeError(f"Tommy artifact does not match the deterministic curator: {target}")
    report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
    expected_format = "pinmame-spatial-audit" if definition["coverage"]["status"] == "author_ready" else "pinmame-spatial-blockers"
    if report.get("format") != expected_format or report.get("machine_id") != KEY:
        raise RuntimeError(f"Tommy spatial report must be {expected_format} and name this machine")
    placements = sum(len(d.get("spatial", {}).get("placements", [])) for c in ("inputs", "outputs") for d in definition[c])
    if report.get("placement_count") != placements:
        raise RuntimeError(f"Tommy spatial report claims {report.get('placement_count')} placements but the definition carries {placements}")
    print("Tommy definition, seed, spatial report, and knowledge note match the deterministic curator.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts.")
    mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, spatial report and knowledge note.")
    parser.add_argument("--repository-root", type=Path, default=ROOT, help="Repository root to operate on.")
    args = parser.parse_args()
    root = args.repository_root.resolve()
    if args.regenerate:
        _write(root)
        print(f"Wrote {DEFINITION_PATH.relative_to(ROOT)}, {SEED_PATH.relative_to(ROOT)}, the spatial report and the knowledge note")
        return
    _check(root)


if __name__ == "__main__":
    main()
