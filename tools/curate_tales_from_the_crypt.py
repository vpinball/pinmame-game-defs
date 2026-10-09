"""Curate the physical Data East Tales from the Crypt (1993) machine definition.

Side-effect free and deterministic. The printed tables are parsed from the hand-transcribed excerpts
committed under ``evidence/excerpts/data-east.tales-from-the-crypt.1993/`` (``tftc_manual``), the
semantic naming is in ``tftc_semantics``, the normalized coordinates resolved from the retained
recreation are in ``tools/tales_from_the_crypt_places.json`` when present, and the ROM inventory is
parsed from pinned PinMAME and embedded below. ``--regenerate`` reproduces the canonical artifacts
byte-for-byte without reading any external evidence root; ``--check`` refuses drift.

The definition, its pinned seed, the spatial report and the knowledge note are all generated here
from the same objects, so prose cannot outlive the data behind it. The comparison folds CRLF to LF
first, so a checkout Git rewrote under ``core.autocrlf=true`` still passes while every other byte
difference still fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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
import drawing_callouts
import tftc_manual
import tftc_semantics as sem

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.tales-from-the-crypt.1993"
DEFINITION_PATH = ROOT / "machines/partial/data-east/tales-from-the-crypt-1993.json"
SEED_PATH = ROOT / "tools/seeds/data-east/tales-from-the-crypt-1993.json"
SPATIAL_REPORT_PATH = ROOT / "reports/spatial/data-east/tales-from-the-crypt-1993.json"
KNOWLEDGE_PATH = ROOT / "knowledge/data-east/tales-from-the-crypt-1993.md"
PLACES_PATH = ROOT / "tools/tales_from_the_crypt_places.json"
RUNTIME_PATH = ROOT / "tools/tales_from_the_crypt_runtime.json"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json"
EXCERPT_DIR = ROOT / "evidence/excerpts" / KEY

REVISION = "8371478a7640f1896dcdf565aed340dc5df989ba"
MANUAL = f"manual.{KEY}"
IPDB = f"ipdb.{KEY}"
CATALOG = "pinmame.catalog.8371478a7640"
CORE = "pinmame.core.8371478a7640"
CORE_H = "pinmame.core-h.8371478a7640"
CORE_C = "pinmame.core-c.8371478a7640"
S11_C = "pinmame.s11-c.8371478a7640"
S11_H = "pinmame.s11-h.8371478a7640"
PIN_REFS = (CORE, CORE_H, CORE_C, S11_C, S11_H)
TABLE = "vpx-table.tales-from-the-crypt-vpw-1-01"
SCRIPT_REF = "vpx-script.tales-from-the-crypt-vpw-1-01"
EXTRACTION = "vpx-extraction.tales-from-the-crypt-vpw-1-01"
LEGACY = "legacy.game.tftc"
RUNTIME_SRC = "runtime.tales-from-the-crypt.tftc-303-service-tests"
CALLOUTS = "drawing-callouts.tales-from-the-crypt.2026-10-09"
CALLOUT_SEED = ROOT / "tools/seeds/data-east/tales-from-the-crypt-1993-callouts.json"
CALLOUT_DATA = load_json(CALLOUT_SEED) if CALLOUT_SEED.is_file() else None

MANUAL_SHA256 = "e31a330891c519ba9bdd7a2328631d9163f4f130ab5fa356a1c33573abf63468"
TABLE_SHA256 = "9eed3ec6f6d4fefa9fb63a3c392fb6b59bd221a8c189b8473c844236bc3f38db"
SCRIPT_SHA256 = "8dbbd3239aea2ae67362842e14e776b4866257898041012cc166809b8085db61"
EXTRACTION_MANIFEST_SHA256 = "d4be453ab6ac1738915b445b1a8e07be23a7e27bb8c6e2c7c591372079d325c5"
EXTRACTION_FILE_COUNT = 1620
EXTRACTION_TOTAL_BYTES = 355081011
IPDB_SHA256 = "fda75b9d89947f85b08b6835e6e8b78c10363deeb5c06e761113d18142eeb10a"
PIN_FILE_SHA256 = {
    "degames.c": "4b0b026de796c07dcddd4753c47859c39c08092a1e87739f85a6b9e12a3af1c1",
    "core.h": "9d2fa69f7fa6963adc793b272bb5cbfbf94e929c0d7f6b928b1b02a8ee15b2b3",
    "core.c": "84aa5ccddc077b60c1331e32ee13d3d577fd5109d4e7a90001692f737a1c7963",
    "s11.c": "cd1b989ac1eec8c95126e743829a8a3726e76a9b838a29339776d4025d75d2d4",
    "s11.h": "743b0836cc84e41e793d65786a964a595fb403c4fdba29b2961e8a36a937f614",
}

# The six PinMAME drivers, parsed from src/wpc/degames.c at the pinned revision (lines 1096-1150).
# Roles: CPU, display, sound U7, sound U17, sound U21. All six share tftcGameData (INITGAMES11 at
# degames.c:1099) and every sound ROM.
ROM_SETS = {
    "tftc_303": {"macro": "DE_ROMSTARTx0", "roms": ["tftccpua.303", "tftcdspa.301", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
    "tftc_400": {"macro": "DE_ROMSTARTx0", "roms": ["tftccpua.400", "tftcdspa.400", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
    "tftc_302": {"macro": "DE_ROMSTARTx0", "roms": ["tftccpua.302", "tftcdspa.301", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
    "tftc_300": {"macro": "DE_ROMSTARTx0", "roms": ["tftccpua.300", "tftcdspa.300", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
    "tftc_200": {"macro": "DE_ROMSTARTx0", "roms": ["tftcgc5.a20", "tftcdot.a20", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
    "tftc_104": {"macro": "DE_ROMSTARTx0", "roms": ["tftccpua.104", "tftcdspl.103", "sndu7.dat", "sndu17.dat", "sndu21.dat"]},
}
ROOT_DRIVER = "tftc_303"
DRIVER_LABELS = {
    "tftc_303": "Tales from the Crypt (3.03)",
    "tftc_400": "Tales from the Crypt (4.00 unofficial MOD)",
    "tftc_302": "Tales from the Crypt (3.02 Dutch)",
    "tftc_300": "Tales from the Crypt (3.00)",
    "tftc_200": "Tales from the Crypt (2.00)",
    "tftc_104": "Tales from the Crypt (1.04 Spanish)",
}
DRIVER_YEARS = {"tftc_303": "1993", "tftc_400": "2015", "tftc_302": "1993", "tftc_300": "1993", "tftc_200": "1993", "tftc_104": "1993"}
ROLES = ("CPU", "display", "sound U7", "sound U17", "sound U21")

SW = tftc_manual.switch_data()
LAMP = tftc_manual.lamp_data()
COIL = tftc_manual.coil_data()
BULB = tftc_manual.bulb_data()
LEGACY_GAME = load_json(ROOT / "games/tftc.json")
PLACES = load_json(PLACES_PATH) if PLACES_PATH.is_file() else {"table_bounds": None, "placements": {}, "unplaced": []}
FACTS = load_json(RUNTIME_PATH)
ROM_SWITCH = FACTS["rom_switch_names"]
ROM_LAMP = FACTS["rom_lamp_names"]
ROM_COIL = FACTS["rom_coil_names"]


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


# --- Source ids shared by the devices --------------------------------------------------------------
def spatial_for(device_id: str, role: str, key: str, refs) -> dict | None:
    hits = PLACES["placements"].get(key)
    if not hits:
        return None
    if key in ("lamp.17", "lamp.26"):
        # The location table lists the two bulbs as A (left side) and B (right side); order them that way.
        hits = sorted(hits, key=lambda hit: hit["x"])
    placements = []
    for index, hit in enumerate(hits, start=1):
        suffix = "" if len(hits) == 1 else f".{index}"
        placements.append({
            "id": f"{device_id}.{role}{suffix}", "role": role, "space": "playfield",
            "x": hit["x"], "y": hit["y"], "provenance": prov("observed", refs),
        })
    return {"status": "observed", "placements": placements}


inputs: list[dict] = []
outputs: list[dict] = []

# --- Inputs ----------------------------------------------------------------------------------------
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
    if part["description"] != chart["printed"] and not unused:
        notes.append(f"The Switch Part Numbers table prints this address as '{part['description']}'.")
    if address == 2:
        notes.append(
            "Dedicated cabinet column. Pinned PinMAME's shared DE_COMPORTS macro labels this position 'Ball Tilt', "
            "but that is a generic platform label: this machine's own chart and parts table print '4th Coin' with no part number. "
            "tftcGameData sets no S11_MUXSW2, so s11.c does not overwrite it with relay state."
        )
    if address == 3:
        notes.append(
            "DE_COMPORTS binds the cabinet Start button to this position; the manual's switch tests and Game Diagnostics text call the "
            "front-of-cabinet button the 'Game Start push-button switch', and its parts list item 14 is 'Start Button Switch Ass'y (Red)'. "
            "The chart names the address Credit Button, so both names are kept."
        )
    if address == 8:
        notes.append("Not declared by pinned PinMAME's DE_COMPORTS (no key); the retained table pulses it from its 2 key as the buy-in button.")
    if address in (33, 36, 37):
        notes.append(
            "The Switch Part Numbers table asterisks this address, and its legend reads '* = Location is in the cabinet', yet the tombstone "
            "mechanism this switch belongs to is a playfield mechanism: the Motor, Cam & Switch Assembly (item 2) is listed on the Playfield - Major "
            "Assemblies page as a part below the playfield, and the Gravestone Up & Down Test describes limit switches of the gravestone motor mechanism. "
            "The asterisk is read as 'not shown on the playfield drawing'; the address has no callout on that drawing."
        )
    if address == 33:
        notes.append("Printed 'Up' (chart) / 'Up (Tomb)' (parts table); the Gravestone Up & Down Test calls it 'Gravestone Motor Up'. The retained table's cvpmMech maps position 160-180 to it (script line 1676).")
    if address == 36:
        notes.append("Printed 'Down' (chart) / 'Down (Tomb)' (parts table); the Gravestone Up & Down Test calls it 'Gravestone Motor Down'. The retained table's cvpmMech maps position 0-20 to it (script line 1677).")
    if address == 37:
        notes.append("Printed 'Grave-Stone' (chart) / 'Tombstone Score' (parts table), part 180-5083-00. It scores when the ball strikes the tombstone target.")
    if address == 57:
        notes.append("The chart cell reads 'Lamp Ramp Exit', an evident misprint of 'Left Ramp Exit', which the parts table and the left-ramp naming of 44, 45 and 62 support.")
    if address in sem.SCRIPT_NOTES and not unused:
        notes.append(f"Retained table: {sem.SCRIPT_NOTES[address]}")
    rom = ROM_SWITCH[str(address)]
    notes.append(
        f"ROM evidence (US 3.03 Active Switch Test): holding public {address} at 1 shows '{rom['name']}', wires {rom['wires']} and '#{address:02d}'; "
        "with every public switch at 0 the same screen shows NONE. The ROM therefore treats public 1 as the closed contact and no switch as closed at rest"
        + (", so the matrix contact rests open. The test also names the address NOT USED." if unused else ", so the matrix contact rests open.")
    )
    entry = {
        "id": device_id,
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": aliases("pinmame.switch", address, "switch", LEGACY_SWITCHES),
        "availability": "unused" if unused else "used",
        "provenance": prov("validated", [MANUAL, CORE_H, RUNTIME_SRC] + ([] if unused else [SCRIPT_REF])),
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
    if address in (63, 64):
        side = "left" if address == 63 else "right"
        button = 84 if address == 63 else 82
        entry["physical"]["notes"] += (
            f" The manual prints this address as a flipper end-of-stroke switch (part 180-5124-00, not marked as a cabinet switch), but PinMAME "
            f"declares tftcGameData FLIPPERS FLIP6364 = FLIP_SWNO(63,64) with no FLIP_SOL and core.c's core_updateSw rewrites it on every update from PinMAME's flipper "
            f"column button bit {button} (the {side} cabinet button), so the ROM reads the button state exactly as the host wrote it there. No end-of-stroke state is "
            f"modelled: with no FLIP_SOL no FLIP_EOS bit is ever set, so the EOS simulation never runs. A consumer drives {button}, not {address}: a host write to {address} "
            "is overwritten on the next update. The retained table never writes this address (its flipper keys reach de.vbs, which writes 82/84)."
        )
        entry["roles"] = [f"flipper.lower.{side}.matrix-copy"]
    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address in sem.CABINET_ROLES or address in (63, 64):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, CORE_H] if address in (63, 64) else [MANUAL])
    else:
        located = spatial_for(device_id, "sensor", f"switch.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if located:
            entry["spatial"] = located
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
            "FORWARD/REVERSE push-button inside the coin door. "
            + (
                "The manual tells the operator to 'depress' it, and every retained service run pulses it at level 1 for 250 ms or less while the ROM advances one test per pulse and "
                "stays put at 0, so public 1 is the depressed button. s11.c hands the PIA the complement (pia_set_input_ca1(S11_PIA2, !core_getSw(DE_SWADVANCE))), the level a "
                "contact closing to ground presents, and its debug readout prints 'B-Down' for 1. A momentary push-button that rests released therefore rests with its contact open."
                if address == -7 else
                "An alternate-action push-button with two maintained positions: the manual's audit and diagnostics text calls them FORWARD (up) and REVERSE (down). The retained service "
                "runs hold it at 1 for the diagnostics walks (the manual says the switch must be REVERSE to enter diagnostics) and drop it to 0 for the lamp test, and s11.c's debug "
                "readout prints 'G-Down' for 1, so public 1 is REVERSE. Unlike the Black button, s11.c hands the PIA the level uncomplemented "
                "(pia_set_input_cb1(S11_PIA2, core_getSw(DE_SWUPDN))), and no retained page draws the coin-door switch circuit, so which position closes the contact is not "
                "established; a two-position maintained switch also has no single rest position. Its contact polarity is left undeclared, which keeps the polarity requirement open."
            )
        )},
        **({"normally_closed": False} if address == -7 else {}),
        "spatial": not_applicable("cabinet_or_service", [S11_H, S11_C, MANUAL]),
    })

_flipper_items = flipper_column_inputs(
    flip_swno=FLIP_SWNO, flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)",
    core_refs=(CORE, CORE_H, CORE_C, S11_C), button_refs=(SCRIPT_REF, VPM_DE_LIBRARY_SOURCE),
    button_notes={
        side: (
            f"The retained known-working script drives it: Table1_KeyDown/Table1_KeyUp hand the {side} flipper key to de.vbs vpmKeyDown/vpmKeyUp through "
            f"KeyDownHandler/KeyUpHandler (script lines 1737 and 1811), which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with "
            f"{'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} (excerpt vpm-script-library-flippers). The physical counterpart is the "
            f"{side} cabinet flipper button; the machine has three flippers and the right button moves both the lower and the upper right flipper."
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
        _item["provenance"]["source_refs"] += [RUNTIME_SRC, MANUAL]
        _row = COIL["flippers"]["Left Flipper" if _address == 84 else "Right Fliper Lwr."]
        _item["physical"]["notes"] += (
            f" ROM evidence (US 3.03 Active Switch Test): holding public {_address} at 1 shows '{ROM_SWITCH[str(_matrix)]['name']}', the wires "
            f"{ROM_SWITCH[str(_matrix)]['wires']} and '#{_matrix}', the matrix switch core_updateSw copies it into, while the other six flipper-column addresses "
            "(81, 83 and 85-88) show NONE, so the ROM cannot see them."
            f" Contact: the manual's Flipper Solenoids table routes the flipper ground '{_row['CPU to flipper switch']}' through the cabinet flipper switch to the Flipper PCB "
            f"('{_row['Flipper switch to Flip. PCB']}'), and the parts list names the cabinet parts Flipper Switch (Left) 180-5048-01 and Flipper Switch, Double (Right) 180-5122-00. "
            "A switch in series with the flipper's ground energises the coil while it is closed, so the released button rests open; public 1 is the pressed button."
        )
        _item["normally_closed"] = False
    else:
        _item["provenance"]["source_refs"].append(RUNTIME_SRC)
        _item["physical"]["notes"] += " ROM evidence: holding this address at 1 in the US 3.03 Active Switch Test shows NONE."
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
        "This machine's manual prints a CPU jumper table (printed page 2) for the ROM and RAM jumpers but does not describe W7, so the meaning of the bit is not stated by any retained source."
    )},
    "spatial": not_applicable("dip_switch", [S11_C]),
})

# --- Outputs: solenoid drives 1-16 --------------------------------------------------------------------
# The coil's +VL side as drawn on the Special Coil Wiring Diagram: (wire, PPB pin, volts).
LEFT_POWER = {
    1: ("BRN", "PPB J6-3", 32), 2: ("BRN", "PPB J6-3", 32), 3: ("YEL-VIO", "PPB J7-8,9", 50), 4: ("BRN", "PPB J6-3", 32),
    5: ("BRN", "PPB J7-3", 32), 6: ("YEL-VIO", "PPB J7-8,9", 50), 7: ("BRN", "PPB J6-3", 32), 8: ("BRN", "PPB J7-8,9", 32),
}


def _wire_and_pin(cell: str) -> tuple[str, str]:
    """Split a transcribed cell such as 'VIO-BRN (J2-10)' into the wire and its PPB pin."""
    match = re.match(r"([A-Z]+[-/][A-Z]+) \((J\d+-\d+)\)", cell)
    if not match:
        raise ValueError(f"unexpected wire cell {cell!r}")
    return match.group(1), f"PPB {match.group(2)}"


def coil_wiring(row: dict, *, left: bool) -> dict:
    """Wiring of one half of a relay pair.

    Both halves share the transistor and its CPU-to-PPB wire (the drive). The PPB board then splits them: the left coil's
    own wire leaves on J2 and the right flash lamps' own wire returns on J9, and that per-load wire is the control.
    """
    drive = int(row["Drive"])
    wiring = {"board": "CPU Board", "driver_transistor": row["Transistor"]}
    wiring["drive_wire"] = row["CPU to PPB wire"]
    wiring["drive_connection"] = f"CN-11 pin {row['CN-11 pin']}"
    wiring["control_wire"], wiring["control_connection"] = _wire_and_pin(row["Coil wire (to coil)"] if left else row["Return wire"])
    if left:
        wiring["power_wire"], wiring["power_connection"], wiring["nominal_voltage_v"] = LEFT_POWER[drive]
    else:
        wiring["power_wire"], wiring["power_connection"], wiring["nominal_voltage_v"] = "ORG", "PPB J6-4,5", 32
    wiring["voltage_type"] = "dc"
    return wiring


DIRECT_IDS = {
    9: ("coil", "diverter", "coil", "Diverter"),
    10: ("relay", "left-right-coil-relay", "relay", "Left/Right Coil Relay"),
    11: ("gi", "general-illumination", "gi", "General Illumination Relay"),
    12: ("virtual", "unused-driver-12", "virtual", "Unfitted Driver 12"),
    13: ("virtual", "unused-driver-13", "virtual", "Unfitted Driver 13"),
    14: ("virtual", "unused-driver-14", "virtual", "Unfitted Driver 14"),
    15: ("motor", "tombstone-motor", "motor", "Tombstone (Gravestone) Motor Relay"),
    16: ("motor", "shaker-motor", "motor", "Shaker Motor"),
}
LEFT_IDS = {
    1: ("six-ball-lockout", "6 Ball Ass'y Lockout"),
    2: ("ball-release", "Ball Release"),
    3: ("ball-launch", "Ball Launch"),
    4: ("drop-target-reset", "Drop Target Reset"),
    5: ("scoop", "Scoop"),
    6: ("left-vuk", "Left VUK"),
    7: ("top-vuk", "Top VUK"),
    8: ("knocker", "Knocker"),
}
SCRIPT_BOUND_LEFT = {
    1: "SolCallback(1) = kisort, which kicks the ball held at sw14 toward sw15 (script lines 276 and 1958-1966)",
    2: "SolCallback(2) = KickBallToLane, which ejects sw15's ball into the shooter lane (script lines 277 and 1928-1945)",
    3: "SolCallback(3) = Auto_Plunger (script line 278)",
    4: "SolCallback(4) = ResetDrops, the drop-target bank reset (script line 279)",
    5: "SolCallback(5) = ScoopKick, which ejects the Power Scoop ball (script lines 280 and 2124-2131)",
    6: "SolCallback(6) = KickBallUp38, the VUK raise (script line 281)",
    7: "SolCallback(7) = KickBallUp52, the back VUK raise (script line 282)",
    8: "SolCallback(8) = vpmSolSound Knocker (script line 284)",
}

for address in range(1, 9):
    row = COIL["muxed"][address]
    suffix, label = LEFT_IDS[address]
    notes = [
        f"Left half of the Left/Right relay pair on printed drive {address}; the right half is published at address {address + 24}. "
        f"The Special Coil Wiring Diagram names the coil '{row['Left coil'].upper()} {row['Coil type']}'.",
        f"The retained table binds {SCRIPT_BOUND_LEFT[address]}.",
    ]
    if address == 1:
        notes.append(
            "The manual draws this coil as the '6 Ball Ass'y Lockout' (25-1240), and the Playfield - Major Assemblies page lists a 6-Ball Switch Assembly, a Lock Ball "
            "Assembly and a deflector for it; the retained table's callback is named kisort and kicks a ball along its model of the trough."
        )
    if address in (3, 6):
        notes.append(
            f"The coil returns to +50 VL through the Q{5 if address == 3 else 3} booster transistor on the PPB board, so it is a higher-voltage coil than the +32 V ones: "
            f"its J2 wire ({row['Coil wire (to coil)'].split(' (')[0]}) drives the booster, which drives the coil."
        )
    if address == 3:
        notes.append(
            "This is the autoplunger IPDB describes as shaped like a door handle with the head of the Crypt Keeper; the cabinet's Ball Launch Door Handle assembly "
            "(parts list items 1A and 1B) carries the launch-button switch 62. The manual's location drawing prints a '3L' box at the lower right of the shooter lane."
        )
    entry = {
        "id": f"coil.{suffix}",
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, SCRIPT_REF, RUNTIME_SRC]),
        "physical": {"part_number": row["Coil type"], "notes": " ".join(notes)},
        "wiring": coil_wiring(row, left=True),
    }
    located = spatial_for(entry["id"], "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
    if located:
        entry["spatial"] = located
        entry["physical"]["notes"] += " The coordinate is the retained table's model of the mechanism this coil actuates, not a claimed winding centre."
    outputs.append(entry)

for address in range(9, 17):
    row = COIL["direct"][address]
    kind, suffix, _, label = DIRECT_IDS[address]
    notes = [f"Direct CPU driver on CN-12 pin {row['CN-12 pin']}; not affected by the Left/Right relay. The Special Coil Wiring Diagram draws: {row['Device as drawn']}."]
    unfitted = address in (12, 13, 14)
    entry = {
        "id": f"{ {'coil': 'coil', 'relay': 'relay', 'gi': 'gi', 'virtual': 'coil', 'motor': 'motor'}[kind] }.{suffix}",
        "label": label,
        "kind": kind,
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "unused" if unfitted else "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([] if unfitted else [SCRIPT_REF])),
        "physical": {"notes": " ".join(notes)},
        "wiring": {"board": "CPU Board", "driver_transistor": row["Transistor"], "control_wire": row["Wire"].replace("(", "").replace(")", "").replace(" N.C.", ""), "control_connection": f"CN-12 pin {row['CN-12 pin']}"},
    }
    if address == 9:
        entry["physical"]["part_number"] = "27-1400"
        entry["physical"]["notes"] += " The retained table binds SolCallback(9) = SolDiv, its diverter (script line 283)."
    if address == 10:
        entry["physical"]["notes"] += (
            " Energising it re-routes drives 1-8 from the coils (left set) to the flash lamps (right set); pinned PinMAME publishes the right set at 25-32 "
            "(s11.c updsol; tftcGameData's muxSol is 10). The retained table never binds SolCallback(10): its Flash1R-Flash8R callbacks are bound to 25-32."
        )
    if address == 11:
        entry["roles"] = ["playfield.general-illumination"]
        entry["physical"]["notes"] += (
            " There is no GI channel on this platform: the general illumination is solenoid 11, the 'GENERAL ILLUM. RELAY' K-1 on the power-supply board. s11.c types it "
            "CORE_MODOUT_BULB_44_6_3V_AC_REV (a reversed 6.3 VAC #44 bulb output) for Tales from the Crypt, so a consumer shows the GI lit while solenoid 11 is off; the "
            "retained table's SetGI (SolCallback(11), script line 285) agrees. The legacy corpus's Lampz index 111 is the table's own GI channel."
        )
        entry["aliases"] = aliases("pinmame.coil", address, "coil", LEGACY_COILS, extra=[("vpe-legacy.lamp", "111"), ("vpe-legacy.lamp", "0111")] if 111 in LEGACY_LAMPS else [])
    if address in (12, 13, 14):
        entry["physical"]["notes"] += " The drawing's three stubs are marked 'NO COIL AT THIS LOCATION'."
        entry["spatial"] = not_applicable("unused", [MANUAL])
    if address == 15:
        entry["physical"]["notes"] += (
            " The retained table's cvpmMech tombstone is driven by Sol1 = 15 (script line 1671). The Gravestone Up & Down Test text names Q23 as the relay driver, which is "
            "the transistor the same manual's schematic draws on drive 16 (the shaker motor); drive 15's transistor is Q24 on the drawing. Both readings are kept: the two sources "
            "agree on the device and its public address (the script binds 15), and differ only on a driver transistor designator."
        )
    if address == 16:
        entry["physical"]["notes"] += " The retained table binds SolCallback(16) = SolShake, which nudges the table while on (script lines 286 and 1573-1587). Adj. 48 'SHAKER MOTOR' switches the feature ON or OFF."
    if address in (9, 15):
        located = spatial_for(entry["id"], "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if located:
            entry["spatial"] = located
            entry["physical"]["notes"] += " The coordinate is the retained table's model of the mechanism this output actuates, not a claimed winding centre."
    elif address == 11:
        located = spatial_for(entry["id"], "emitter", "solenoid.11", [TABLE, SCRIPT_REF, MANUAL])
        if located:
            entry["spatial"] = located
            entry["physical"]["notes"] += (
                " The retained table's GI collection holds 39 Light objects, none of which shows its own bulb mesh: wide lights (falloff 150-200 VPX units) that sit within 4 units of a "
                "piece of the table's modelled GI bulb mesh (Primitive.bulbs, 28 separate bulbs in its world-space OBJ export), and small glow helpers (falloff 30-50) up to 24 units "
                f"beside them. Each bulb-mesh piece that a GI light lies within 25 units of is one emitter, placed on the GI light nearest it, which gives {len(located['placements'])} "
                "emitters; the other four pieces have no GI light near them and are not counted. The table's grouping is not the machine's wiring, the manual's bulb table does not say how many of its 91 No. 44 and 34 No. 555 bulbs "
                "are general illumination, and the manual's own note says G.I. lamps are not shown on its lamp drawings, so no quantity is claimed."
            )
    elif address == 10:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address == 16:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    outputs.append(entry)

# --- Solenoids 17-22: the CPU Controlled Auxiliary Solenoids -----------------------------------------
AUX_IDS = {
    17: ("left-turbo-bumper", "Left Turbo Bumper"), 18: ("center-turbo-bumper", "Center Turbo Bumper"),
    19: ("right-turbo-bumper", "Right Turbo Bumper"), 20: ("left-slingshot", "Left Slingshot"),
    21: ("right-slingshot", "Right Slingshot"), 22: ("laser-kickback", "Laser Kickback"),
}
for address in range(17, 23):
    row = COIL["auxiliary"][address]
    suffix, label = AUX_IDS[address]
    notes = [
        "One of the six switched/special solenoids; CORE_FIRSTSSSOL is 17 and Data East's PIA permutation ssSolNo[1] = {3,4,5,1,0,2} publishes them at 17 + that index, "
        "so the printed coil number and PinMAME's public address are different identities, and only a ROM run can pair them: the US 3.03 Cycling Coils test fires public "
        "17-22 in order under the names LEFT TURBO, BOTTOM TURBO, RIGHT TURBO, LEFT SLING, RIGHT SLING and LASER KICK 50V, which are the manual's coils 17-22, so here the "
        "printed number is the public address. Pinned PinMAME's INITGAMES11 leaves sxx.ssSw empty, so none of these is publishable from a "
        "switch closure: the public output appears only when the ROM drives its PIA line.",
    ]
    if address == 22:
        notes.append(
            "Printed 'Laser Kickback (See Schematic)', control WHT-VIO, power VIO-YEL PPB J7-3 (a different power connection from 17-21, which take RED PS CN3-6). The Laser Kick "
            "Test text says rolling the ball over the left outlane switch should fire it. The retained table binds SolCallback(22) = Solkickback, which fires an auto-plunger at the left outlane (script lines 287 and 1603-1610)."
        )
    entry = {
        "id": f"coil.{suffix}",
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([SCRIPT_REF] if address == 22 else [])),
        "physical": {"part_number": row["Coil type"], "notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Drive transistor"],
            "control_wire": row["Control line (CPU to coil)"].split(" ")[0],
            "control_connection": row["Control line (CPU to coil)"].split(" ", 1)[1],
            "power_wire": row["Power line (PS to coil)"].split(" ")[0],
            "power_connection": row["Power line (PS to coil)"].split(" ", 1)[1],
        },
    }
    located = spatial_for(entry["id"], "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
    if located:
        entry["spatial"] = located
    outputs.append(entry)

outputs.append({
    "id": "control.game-on",
    "label": "Game On / Switched Solenoid Enable",
    "kind": "control_signal",
    "binding": {"group": "pinmame.output.solenoid", "device": 23},
    "aliases": [{"namespace": "pinmame.solenoid", "value": "23"}],
    "availability": "used",
    "provenance": prov("validated", [S11_C]),
    "physical": {"notes": (
        "S11_GAMEONSOL is 23, driven by PIA0 CB2 (s11.c pia0cb2_w). It enables the six switched solenoids 17-22 and gates the flippers rather than driving a device of its own; "
        "core_updateSw passes it to the flipper synthesis as the enable."
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

# --- Solenoids 25-32: the right half of the relay pair, all flash lamps ----------------------------------
for address in range(25, 33):
    drive = address - 24
    row = COIL["muxed"][drive]
    plfd, back, insert = sem.FLASHER_COMPOSITION[drive]
    assert row["Right set"] == f"({plfd}) PLFD" + (f" ({back}) BACK PANEL" if back else "") + (f" ({insert}) INSERT" if insert else "") + " (4) 89", row["Right set"]
    entry = {
        "id": f"flasher.{drive}r",
        "label": f"Flash Lamps {drive}R",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, SCRIPT_REF, RUNTIME_SRC]),
        "physical": {
            "quantity": 4,
            "notes": (
                f"Right half of the Left/Right relay pair on printed drive {drive}; the left half (the {row['Left coil']} coil) is published at address {drive}. The Special Coil Wiring "
                f"Diagram prints '{row['Right set']}': four No. 89 bulbs, {plfd} on the playfield"
                + (f", {back} on the back panel" if back else "") + (f", {insert} in the insert (backbox) panel" if insert else "")
                + ". PinMAME types the whole 25-32 block as eight No. 89 flashers. The manual's bulb table lists 31 No. 89 bulbs against these drawings' 32 (18 playfield sockets against 19 drawn): "
                "the one-bulb difference is not attributable to a drive, so per-drive quantities follow the drawings. "
                f"The retained table binds SolCallback({address}) = Sol{drive}R (script lines {287 + drive})."
            ),
        },
        "wiring": coil_wiring(row, left=False),
    }
    located = spatial_for(entry["id"], "effect", f"solenoid.{address}", [TABLE, SCRIPT_REF, MANUAL])
    if located:
        entry["spatial"] = located
        if len(located["placements"]) != 4:
            entry["physical"]["notes"] += (
                f" The retained table models {len(located['placements'])} lit objects for this flasher, not four bulb sockets; they are presentation effects and are not a socket survey."
            )
    outputs.append(entry)

# --- 33-44: inert and printer-line addresses ---------------------------------------------------------------
for address in range(33, 37):
    outputs.append({
        "id": f"virtual.inert-{address}",
        "label": f"Inert Solenoid Address {address}",
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": "core_getSol serves 33-36 only for the WPC and SAM generations (driver-specific flipper and game-on remaps); tftcGameData is GEN_DEDMD32, so the address always reads 0."},
        "spatial": not_applicable("virtual", [CORE_C]),
    })
# s11.c's pia2b_w comment states the CN3 pin of bits 0-2 (pins 9, 8, 7) and bit 7 (pin 1) and elides bits 3-6.
PRINTER_PINS = {0: 9, 1: 8, 2: 7, 7: 1}
for index, address in enumerate(range(37, 45)):
    pin = PRINTER_PINS.get(index)
    pin_text = (
        f"CN3 pin {pin}" if pin is not None else
        "a CN3 pin the comment elides: it states pins 9, 8 and 7 for bits 0-2 and pin 1 for bit 7, so bits 3-6 occupy four of pins 2-6"
    )
    outputs.append({
        "id": f"virtual.printer-line-{address}",
        "label": f"Printer Data Line {index}" + (f" (CN3 pin {pin})" if pin is not None else ""),
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [CORE_C, S11_C, MANUAL, RUNTIME_SRC]),
        "physical": {"notes": (
            f"tftcGameData sets gameSpecific1 = S11_PRINTERLINE, so s11.c's pia2b_w publishes PIA2 port B bit {index} here as the extSol bit that core_getSol reads at 37 + {index} "
            f"({pin_text}; the comment heads the list 'CN3 Printer Data Lines (Used by various games)'). This machine's Adj. 61 'PRINTER INTERFACE' lets the operator print an audit sheet with the Start button, so the "
            "port is a printer interface. ROM evidence (US 3.03): pressing Start on Adjustment 61 PRINTER INTERFACE ('PRESS START TO PRINT') asserted public 40, 42, 43 and 44 together (PIA2 port B bits 3, 5, 6 and 7) "
            "and no other address from 37 to 44; none of 37-44 moved in the Active Switch, Lamp, Cycling Coils, Laser Kick or Tombstone tests. The addresses carry the printer's data port, not a playfield device, "
            "and the manual's coil tables name none."
        )},
        "spatial": not_applicable("virtual", [S11_C]),
    })

FLIPPERS = {
    45: ("Synthetic Lower Right Flipper Power", "right"), 46: ("Synthetic Lower Right Flipper Hold", "right"),
    47: ("Synthetic Lower Left Flipper Power", "left"), 48: ("Synthetic Lower Left Flipper Hold", "left"),
}
for address, (label, side) in FLIPPERS.items():
    row = COIL["flippers"]["Left Flipper" if side == "left" else "Right Fliper Lwr."]
    outputs.append({
        "id": f"virtual.flipper-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": [{"namespace": "pinmame.solenoid", "value": str(address)}],
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, CORE_H]),
        "physical": {
            "part_number": row["Coil type"],
            "notes": (
                "Not a CPU-driven output on this machine. tftcGameData declares no FLIP_SOL, so core.c's core_updateSw synthesises these bits whenever the switched-solenoid enable (public 23) is on and "
                f"the corresponding cabinet button bit of PinMAME's flipper column is set: public {82 if side == 'right' else 84}, the same bit it copies into matrix switch {64 if side == 'right' else 63}. "
                "Power and hold therefore assert and release together and are not independently controllable; a recreation must not model them as two coils. The physical coils are driven from the "
                f"Flipper PCB, whose printed Flipper Solenoids table lists a Left Flipper ({COIL['flippers']['Left Flipper']['Assembly']}), a Right Flipper Lower ({COIL['flippers']['Right Fliper Lwr.']['Assembly']}) and a "
                f"Right Flipper Upper ({COIL['flippers']['Right Flipper Upr.']['Assembly']}); the upper right flipper's coil (25-1800) shares the lower right flipper's ORN-VIO CPU CN19-1 flipper-ground line and "
                "PinMAME synthesises nothing for it. This machine has three flippers."
            ),
        },
        "wiring": {
            "board": "Flipper PCB", "control_wire": row["CPU to flipper switch"].split(" ")[0],
            "control_connection": row["CPU to flipper switch"].split(" ", 1)[1],
            "power_wire": row["Power line, Flip. PCB to coil"].split(" ")[0],
            "power_connection": row["Power line, Flip. PCB to coil"].split(" ", 1)[1],
        },
        "spatial": not_applicable("virtual", [MANUAL, CORE_C]),
    })
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL; tftcGameData declares custSol = 0, so nothing is published from 51 upward."),
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

# --- Lamps 1-64 ------------------------------------------------------------------------------------------------
for address in range(1, 65):
    chart = LAMP["chart"][address]
    suffix, label = sem.LAMPS[address]
    location_keys = [key for key in LAMP["location"] if key.rstrip("AB") == f"{address:02d}"]
    notes = [f"Printed lamp-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}'."]
    notes.append("The location table prints: " + "; ".join(f"{key} {LAMP['location'][key]}" for key in location_keys) + ".")
    if address in sem.TWO_BULB_LAMPS:
        notes.append("The location table lists two bulbs on this one address, one at each side of the playfield, so the address drives two physical inserts.")
    if address in (14, 16):
        notes.append("The location drawing's callout sits below the playfield outline, beside the cabinet front: a cabinet lamp.")
    if address == 15:
        notes.append("The location drawing's callout sits in the shooter lane beside the plunger; the retained table calls its lamp object the 'Plunger LED' (script lines 3043-3044). It lights the launch cue for the door-handle autoplunger.")
    if address in (14, 16):
        notes.append("The retained table leaves its Lampz binding commented out (script lines 3042 and 3047).")
    entry = {
        "id": f"lamp.{suffix}",
        "label": label,
        "kind": "lamp",
        "binding": {"group": "pinmame.output.lamp", "device": address},
        "aliases": aliases("pinmame.lamp", address, "lamp", LEGACY_LAMPS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, S11_C, RUNTIME_SRC] + ([SCRIPT_REF] if address not in (14, 16) else [])),
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
    if address in sem.TWO_BULB_LAMPS:
        entry["physical"]["quantity"] = 2
    if address in sem.CABINET_LAMPS:
        entry["roles"] = [sem.CABINET_LAMPS[address]]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    else:
        located = spatial_for(entry["id"], "emitter", f"lamp.{address}", [TABLE, SCRIPT_REF, MANUAL])
        if located:
            entry["spatial"] = located
    outputs.append(entry)

# --- ROM evidence on the outputs ---------------------------------------------------------------------------------
for entry in outputs:
    group, address = entry["binding"]["group"], entry["binding"]["device"]
    if group == "pinmame.output.lamp":
        rom = ROM_LAMP[str(address)]
        entry["physical"]["notes"] += (
            f" ROM evidence (US 3.03 Lamp Test): Start steps one lamp at a time and lights public lamp {address} under '{rom['name']}', wires {rom['wires']}, '#{address:02d}'; "
            "the ROM names lamps by position where the manual names them by feature, and the wires match the manual's chart."
        )
    elif group == "pinmame.output.solenoid" and address == 10:
        entry["physical"]["notes"] += " ROM evidence (US 3.03 Cycling Coils): public 10 asserts together with each of the eight flash-lamp steps (25-32), once per step."
    elif group == "pinmame.output.solenoid" and str(address) in ROM_COIL:
        rom = ROM_COIL[str(address)]
        if address >= 25:
            entry["physical"]["notes"] += (
                f" ROM evidence (US 3.03 Cycling Coils): public {address} fires with the relay at 10 under the step '{rom['name']}', which gives the same bulb composition as the "
                "Special Coil Wiring Diagram (insert, playfield and back-panel counts)."
            )
        elif address in (12, 13, 14):
            entry["physical"]["notes"] += (
                f" ROM evidence (US 3.03 Cycling Coils): the test pulses public {address} in its drive order and names it '{rom['name']}'. The pulse is the test sweeping every driver, "
                "so it does not make the address a fitted device: the wiring diagram prints NO COIL AT THIS LOCATION and the ROM agrees."
            )
        else:
            entry["physical"]["notes"] += f" ROM evidence (US 3.03 Cycling Coils): public {address} fires in drive order under the step '{rom['name']}'."

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
MECH_REFS = [MANUAL, SCRIPT_REF]
mechanisms = [
    {
        "id": "mechanism.ball-trough",
        "label": "Six-Ball Trough, Lockout and Ball Release",
        "kind": "kicker",
        "actuators": ["coil.six-ball-lockout", "coil.ball-release"],
        "sensors": [f"switch.{sem.SWITCHES[a][0]}" for a in range(9, 17)],
        "assembly_part_number": "500-5683-01",
        "behavior": (
            "Seven trough switches run along a slanted rail at the bottom of the playfield: #1 Left at 9 (the drain end) through #6 at 14, and #7 Right at 15 (the release position), "
            "all printed with part 180-5119-00 except 15 (180-5118-00). The shooter lane switch 16 follows. The manual lists a 6-Ball Switch Assembly (500-5683-01), a Lock Ball "
            "Assembly (500-5684-01) and a Deflector (535-6606-01) for this region, and its drive table gives drive 1 to the '6 Ball Ass'y Lockout' (25-1240) and drive 2 to the Ball "
            "Release (23-800). The retained table models six balls resting on 9-14 on kickers that shuffle toward 15 after drive 1 fires (kisort), asserts 15 for the ball ready to release, and "
            "clears 15 and kicks the ball into the lane when drive 2 fires. The table's trough is a surrogate: the physical lockout linkage's timing is not measured. The manual's Easy Trough "
            "Clear message tells the operator to press a flipper button to clear balls from the trough."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.ball-launch",
        "label": "Door-Handle Autoplunger",
        "kind": "kicker",
        "actuators": ["coil.ball-launch"],
        "sensors": ["switch.launch-button", "switch.shooter-lane"],
        "assembly_part_number": "500-5477-01",
        "behavior": (
            "The Ball Launch Assembly (500-5477-01) fires the Ball Launch coil (drive 3, 23-800 through the +50 V booster) to send the ball up the right-hand lane. The player triggers it "
            "with the cabinet's Ball Launch Door Handle (items 1A/1B), whose switch is the matrix's Launch Button at 62. The manual's Kill Shot rule also uses the handle: 'Shoot the Lit Drop Target "
            "Bank with the door handle'. The retained table sets 62 from the plunger key and the lock-bar key and fires its auto plunger from SolCallback(3)."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.drop-target-bank",
        "label": "Guillotine Drop Target Bank",
        "kind": "drop_target_bank",
        "actuators": ["coil.drop-target-reset"],
        "sensors": ["switch.left-drop-target", "switch.middle-drop-target", "switch.right-drop-target"],
        "assembly_part_number": "500-5621-03",
        "behavior": (
            "Three drop targets, printed Left Drop, Middle Drop and Right Drop at 41-43 (part 180-5092-01), reset as one bank by the Drop Target coil (drive 4, 23-800). The lamp chart calls "
            "them the Guillotine Drop Targets and the rules say the targets 'drop into the display' with an increasing value (Super Guillotine). The retained table builds them as a cvpmDropTarget "
            "(dtBank.InitDrop Array(sw41, sw42, sw43), script line 1662) and binds SolCallback(4) = ResetDrops."
        ),
        "positions": [
            {"id": "mechanism.drop-target-bank.left", "label": "Left Drop Target", "sensors": ["switch.left-drop-target"]},
            {"id": "mechanism.drop-target-bank.middle", "label": "Middle Drop Target", "sensors": ["switch.middle-drop-target"]},
            {"id": "mechanism.drop-target-bank.right", "label": "Right Drop Target", "sensors": ["switch.right-drop-target"]},
        ],
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.left-vuk",
        "label": "Left VUK (Gravestone VUK)",
        "kind": "kicker",
        "actuators": ["coil.left-vuk"],
        "sensors": ["switch.left-vuk"],
        "assembly_part_number": "500-5306-03",
        "behavior": (
            "The Vertical Up Kicker assembly (500-5306-03) holds a ball at 38 (part 180-5064-00) until the Left VUK coil (drive 6, 23-800 through the +50 V booster) throws it up. The Gravestone Up & Down Test "
            "text says the tombstone lowers 'to allow a shot to the Vertical Up Kicker (VUK) below the playfield', and the audit text calls a ball shot there after the gravestone is lowered 'Robbing the Crypt'. "
            "The retained table raises the ball from the kicker with KickBallUp38 on SolCallback(6) and moves it to the upper left of the playfield."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.super-vuk",
        "label": "Super VUK and Subway Troughs",
        "kind": "kicker",
        "actuators": ["coil.top-vuk"],
        "sensors": ["switch.super-vuk-right", "switch.small-trough", "switch.large-trough"],
        "assembly_part_number": "500-5116-06",
        "behavior": (
            "The Super VUK assembly (500-5116-06) at the top right catches a ball at 52 (part 180-5064-01) and the Top VUK coil (drive 7, 23-800) throws it back onto the playfield. The Trough Assembly "
            "(500-5652-00) beside it carries the Small Trough (53) and Large Trough (54) switches (part 180-5093-00). The retained table calls the path the 'Subway': 53 and 54 are triggers on it and "
            "52 is its 'Back VUK - From Subway', raised by KickBallUp52 on SolCallback(7). Which shots feed the subway is a property of the retained table's ramp geometry and is not stated by the manual."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.power-scoop",
        "label": "Power Scoop",
        "kind": "kicker",
        "actuators": ["coil.scoop"],
        "sensors": ["switch.power-scoop"],
        "assembly_part_number": "500-5741-00",
        "behavior": (
            "The Power Scoop Assembly (500-5741-00) holds the ball at 55 (part 500-5057-00) until the Scoop coil (drive 5, 23-800) ejects it. The rules use the scoop to collect a lit Creature Feature, "
            "to start the Crypt Jam six-ball play once every creature feature is complete, and for the Electric Chair award. The retained table's ScoopKick ejects the ball and clears the switch."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.diverter",
        "label": "Diverter",
        "kind": "diverter",
        "actuators": ["coil.diverter"],
        "sensors": [],
        "assembly_part_number": "500-5654-00",
        "behavior": (
            "The Diverter Assembly (500-5654-00) with its Diverter Plunger & Crankarm Assembly (515-5453-00) is fired by drive 9 (27-1400). The rules audit counts the times the diverter was enabled ('Use Diverter', Audit 92). "
            "The retained table starts with the diverter dropped and animates it from SolCallback(9) = SolDiv (script lines 1542-1567). No switch senses it."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.tombstone",
        "label": "Rising and Lowering Tombstone (Gravestone)",
        "kind": "motorized",
        "actuators": ["motor.tombstone-motor"],
        "sensors": ["switch.tombstone-up-limit", "switch.tombstone-down-limit", "switch.tombstone-score"],
        "assembly_part_number": "500-5742-01",
        "behavior": (
            "A motor with a cam and two limit switches (Motor, Cam & Switch Assembly, 500-5742-01, drawn below the playfield) raises and lowers the tombstone target in front of the Left VUK. The "
            "Gravestone Up & Down Test says the CPU determines the motor's state from the two limit switches, that each limit switch should close 'just prior to the limit' of the mechanism, and that "
            "both should never be closed at the same time; holding Start pulses the relay repeatedly. The retained table models it as a cvpmMech (type one-solenoid reverse, Sol1 = 15, length 180, "
            "position 160-180 closing switch 33 and 0-20 closing switch 36) and pulses switch 37 when a ball strikes the target from below (script lines 1668-1681 and 2664-2735). The rules lower the "
            "tombstone when C-R-Y-P-T is spelled (Multi-Ball ready) and for the Monster Jackpot; IPDB lists 'Rising and lowering gravestone' as the machine's toy. "
            "Mechanism speed and travel are table-owned tuning, not machine data."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.laser-kickback",
        "label": "Laser Kickback and Knocker Assembly",
        "kind": "kicker",
        "actuators": ["coil.laser-kickback"],
        "sensors": ["switch.left-outlane"],
        "assembly_part_number": "500-5081-00",
        "behavior": (
            "The Kickback & Knocker Assembly (500-5081-00) sits at the lower left. The Laser Kick Test text states that rolling the ball over the left outlane switch should fire the Laser Kick, and that "
            "a late or early kick is corrected by adjusting the switch actuator. The rules' Crypt Kicker returns a ball from the left outlane when lit. The retained table fires a plunger at the outlane "
            "from SolCallback(22). The assembly also carries the Knocker (drive 8)."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.turbo-bumpers",
        "label": "Turbo Bumpers",
        "kind": "other",
        "actuators": ["coil.left-turbo-bumper", "coil.center-turbo-bumper", "coil.right-turbo-bumper"],
        "sensors": ["switch.left-turbo-bumper", "switch.bottom-turbo-bumper", "switch.right-turbo-bumper"],
        "assembly_part_number": "500-5227-00",
        "behavior": (
            "Three pop bumpers (Turbo Bumper Assemblies, 500-5227-00, part 180-5015-01 skirts at 49-51). The coil table names them Left, Center and Right Turbo Bumper (17, 18, 19) while the switch chart "
            "names them Left, Bottom and Right; the same bumper is meant by Center and Bottom. The rules' Psycho Pops and Chop Pops light them for 25 million and 1 million per hit. Pinned PinMAME's PIA "
            "permutation of the six switched solenoids is not sequential, so the printed coil numbers alone do not give the public addresses; the ROM's own coil test below pairs them."
        ),
        "positions": [
            {"id": "mechanism.turbo-bumpers.left", "label": "Left Turbo Bumper", "sensors": ["switch.left-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.bottom", "label": "Bottom (Center) Turbo Bumper", "sensors": ["switch.bottom-turbo-bumper"]},
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
        "assembly_part_number": "500-5226-00",
        "behavior": (
            "Two slingshot assemblies (500-5226-00) above the lower flippers, sensed at 19 and 27 (part 180-5023-00) and fired by the Left and Right Slingshot coils (20 and 21, 23-800). "
            "The printed pairing is left to left and right to right; the ROM's own coil test below confirms the public addresses 20 and 21."
        ),
        "provenance": prov("candidate", MECH_REFS),
    },
    {
        "id": "mechanism.left-3-bank",
        "label": "Left 3-Bank Eyeball Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.left-bottom-3-bank", "switch.left-middle-3-bank", "switch.left-top-3-bank"],
        "assembly_part_number": "500-5765-00",
        "behavior": (
            "A bank of three stand-up targets (3-Bank Stand-Up Target Assembly, 500-5765-00) at 20-22 (parts 180-5130-02, -01 and -00). IPDB counts six 'Eyeball targets'. The rules light the Mystery Door "
            "values (lamps 49-51) when the ball rolls through the left return lane, and a miss turns them off. The bank has no reset coil in the printed coil inventory."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.right-3-bank",
        "label": "Right 3-Bank Eyeball Targets",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.right-bottom-3-bank", "switch.right-middle-3-bank", "switch.right-top-3-bank"],
        "assembly_part_number": "500-5765-00",
        "behavior": (
            "The mirror-image bank of three stand-up targets at 28-30 (parts 180-5130-02, -01 and -02; the top target's printed part repeats the bottom's). It has no reset coil in the printed coil inventory."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.captive-ball",
        "label": "Captive Ball (Clone)",
        "kind": "toy",
        "actuators": [],
        "sensors": ["switch.captive-ball-target"],
        "behavior": (
            "A captive ball whose target switch at 39 (part 180-5114-08) scores the Clone award: 'Shooting the captive ball target will award the player 5mil and add 1mil for additional shots and award features'. "
            "The retained table pulses the switch from a HitTarget."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
    {
        "id": "mechanism.shaker",
        "label": "Cabinet Shaker Motor",
        "kind": "motorized",
        "actuators": ["motor.shaker-motor"],
        "sensors": [],
        "assembly_part_number": "515-5893-00",
        "behavior": (
            "The Shaker Motor (515-5893-00) with its Shaker Motor P.C. Board (520-5065-00) in the cabinet is switched from drive 16 through Q4 and R16 on the CPU board; the board is fed 9 VAC through three diodes and fuses. "
            "Adj. 48 turns the feature ON or OFF. The retained table enables a repeating nudge while the output is on."
        ),
        "provenance": prov("validated", MECH_REFS),
    },
]

_CAUSAL = {pair["switch"]: pair for pair in FACTS["causal_pairs"] if pair["coils"]}
assert _CAUSAL[17]["coils"] == [22] and _CAUSAL[38]["coils"] == [6] and _CAUSAL[52]["coils"] == [7] and _CAUSAL[55]["coils"] == [5]
_MECH_EVIDENCE = {
    "mechanism.laser-kickback": (
        "ROM evidence (US 3.03 Laser Kick Test): closing public 17, the left outlane, fires public 22 within 20 ms, for a 400 ms and for a 1500 ms closure alike, while closing 18, 25 or 26 fires nothing; "
        "the coil's ROM name is 'LASER KICK 50V'.", "validated"),
    "mechanism.left-vuk": (
        "ROM evidence (US 3.03 Laser Kick Test): closing public 38 fires public 6, about 0.3 s later; the coil's ROM name is 'LEFT VUK 50V' and the switch's 'CRYPT VUK (LEFT)'.", "validated"),
    "mechanism.super-vuk": (
        "ROM evidence (US 3.03 Laser Kick Test): closing public 52 fires public 7, about 0.3 s later; the coil's ROM name is 'TOP VUK 50V' and the switch's 'RIGHT SUPER VUK'.", "validated"),
    "mechanism.power-scoop": (
        "ROM evidence (US 3.03 Laser Kick Test): closing public 55 fires public 5, about 0.3 s later; the coil's ROM name is 'SCOOP' and the switch's 'POWER SCOOP'.", "validated"),
    "mechanism.tombstone": (
        "ROM evidence (US 3.03 Tombstone Test): holding Start drives public 15 for as long as it is held, the coil's ROM name is 'MOTOR UP/DWN', and the test's UP, DOWN and TARGET lines turn ON "
        "when public 33, 36 and 37 are closed (the ROM names the switches 'UP/DWN BAR - UP', 'UP/DWN BAR - DOWN' and 'TOMB STONE').", "validated"),
    "mechanism.turbo-bumpers": (
        "ROM evidence (US 3.03 Cycling Coils and Active Switch Test): the ROM names public 17, 18 and 19 'LEFT TURBO', 'BOTTOM TURBO' and 'RIGHT TURBO' and switches 49, 50 and 51 'LEFT/BOTTOM/RIGHT TURBO BUMPER', "
        "so the coils and skirts pair left, bottom and right.", "validated"),
    "mechanism.slingshots": (
        "ROM evidence (US 3.03 Cycling Coils and Active Switch Test): the ROM names public 20 and 21 'LEFT SLING' and 'RIGHT SLING' and switches 19 and 27 LEFT and RIGHT SLINGSHOT.", "validated"),
    "mechanism.drop-target-bank": (
        "ROM evidence (US 3.03 Cycling Coils): public 4 is named 'DROP TARGET' and public 41-43 DROP TARGET - LEFT, MIDDLE and RIGHT.", "validated"),
    "mechanism.diverter": ("ROM evidence (US 3.03 Cycling Coils): public 9 is named 'DIVERTER'.", "validated"),
    "mechanism.shaker": ("ROM evidence (US 3.03 Cycling Coils): public 16 is named 'SHAKER MOTOR'.", "validated"),
    "mechanism.ball-trough": (
        "ROM evidence (US 3.03 Cycling Coils and Active Switch Test): public 1 is named 'LOCK OUT', public 2 'BALL RELEASE', and the ROM names switches 9-15 TROUGH #1 LEFT through #7 RIGHT. "
        "A game-start run from a fresh state with balls on 9-14 and 15 empty shows the serve: nothing fires at power-up; after Start the ROM pulses the lockout (public 1, about 0.4 s) every "
        "two seconds while 15 stays open; once 15 closes it stops the lockout and pulses the ball release (public 2, about 0.1 s) within 0.1 s, repeating every 2.3 s while 15 stays closed. "
        "So the lockout feeds the next ball onto the release position 15 and the release kicks it from 15 into the shooter lane; the host moved the balls, so travel times are not measured.", "validated"),
    "mechanism.ball-launch": (
        "ROM evidence (US 3.03 Cycling Coils, Active Switch Test and a game-start run): public 3 is named 'AUTO LAUNCH 50V' and public 62 'LAUNCH BUTTON'. With the served ball resting on the "
        "shooter lane switch 16 nothing fired for six seconds; pressing 62 fired public 3 within 0.11 s.", "validated"),
}
for _mechanism in mechanisms:
    _sentence, _status = _MECH_EVIDENCE.get(_mechanism["id"], (None, None))
    if _sentence:
        _mechanism["behavior"] += " " + _sentence
        _mechanism["provenance"]["source_refs"].append(RUNTIME_SRC)
        if _status:
            _mechanism["provenance"]["status"] = _status

relationships = [
    {
        "id": f"relationship.left-right-relay-{drive}",
        "kind": "relay_gated",
        "source": "relay.left-right-coil-relay",
        "destination": f"flasher.{drive}r",
        "provenance": prov("validated", [MANUAL, CORE, S11_C]),
    }
    for drive in range(1, 9)
] + flipper_column_relationships(
    flip_swno=FLIP_SWNO, matrix_ids={63: "switch.left-flipper-copy", 64: "switch.right-flipper-copy"}, refs=(CORE_C, CORE_H),
)

conflicts: list[dict] = []

# --- Drivers -------------------------------------------------------------------------------------------------------
_root = ROM_SETS[ROOT_DRIVER]["roms"]
drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]["roms"]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root and the last factory firmware (3.03, with display ROM tftcdspa.301). Every tftc_* set shares one tftcGameData (INITGAMES11, "
            "GEN_DEDMD32, de_128x32DMD, FLIP6364, sound board DE2S, DMD board DEDMD32, S11_PRINTERLINE) and one set of sound ROMs, so all six present identical "
            "playfield hardware and identical public addresses. The 4.00 set is a 2015 community MOD, not factory firmware; it runs on this same machine."
        )
    else:
        differing = [(role, mine) for role, mine, theirs in zip(ROLES, roms, _root) if mine != theirs]
        note = ("Differs from the root in " + ", ".join(f"the {role} ROM ({rom})" for role, rom in differing) + ".") if differing else "Byte-identical ROM set to the root."
        note += " The shared tftcGameData means the address model is unchanged."
        if driver_id == "tftc_104":
            note += " The CPU and display ROM names mark it as the Spanish-language set; it is a language firmware for the same hardware."
        if driver_id == "tftc_302":
            note += " Labelled Dutch; the display ROM is the root's."
        if driver_id == "tftc_400":
            note += (" PinMAME dates this set 2015: it is later community software for the same physical machine, not a new game. The retained known-working table runs this ROM "
                     "(cGameName = tftc_400), so its callbacks are evidence about the MOD, which keeps the factory address map.")
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
    _roms = ROM_SETS[_driver["id"]]["roms"]
    for _role, _mine, _theirs in zip(ROLES, _roms, _root):
        if _mine != _theirs and _mine not in _driver["variant_notes"]:
            raise SystemExit(f"{_driver['id']}: {_role} ROM {_mine} differs from the root but the note omits it")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_record(name: str, locator: str, **extra) -> dict:
    record = {
        "id": f"excerpt.tales-from-the-crypt.{name.rsplit('.', 1)[0]}",
        "locator": locator,
        "path": f"evidence/excerpts/{KEY}/{name}",
        "sha256": file_sha256(EXCERPT_DIR / name),
    }
    for key, value in extra.items():
        record[key] = value
    return record


def image_fields(name: str, derivation: str) -> dict:
    return {
        "image": f"evidence/excerpts/{KEY}/{name}",
        "image_sha256": file_sha256(EXCERPT_DIR / name),
        "image_derivation": derivation,
    }


MANUAL_NAME = "Data_East_1993_Tales_from_the_Crypt_Manual.pdf"
CHECKED = {"method": "manual", "transcribed_by": "curator, read from native-resolution renders of the image-only scan; OCR was used only to find pages", "reviewed": True}
EXCERPTS_MANUAL = [
    excerpt_record(
        "switch-matrix.md", "printed pages 28-29 (PDF 32-33), Switch Matrix Chart and complete Switch Part Numbers table",
        **image_fields("switch-matrix.webp", f"{MANUAL_NAME} page 32, crop box 0.07,0.435,0.895,0.875, scanned page rendered at its native resolution (embedded image xref 155, 2552px across 8.51in), rendered at 121 dpi, capped to 850px wide, grayscale, 851x587 WebP quality 70"),
        **CHECKED),
    excerpt_record(
        "lamp-matrix.md", "printed pages 30-31 (PDF 34-35), Lamp Matrix Chart and Lamp Matrix Locations and Descriptions",
        **image_fields("lamp-matrix.webp", f"{MANUAL_NAME} page 34, crop box 0.07,0.435,0.895,0.905, scanned page rendered at its native resolution (embedded image xref 165, 2552px across 8.51in), rendered at 121 dpi, capped to 850px wide, grayscale, 851x627 WebP quality 70"),
        **CHECKED),
    excerpt_record(
        "coil-drivers.md", "printed pages 32-33 (PDF 36-37), coil and flash-lamp tests, the auxiliary and flipper solenoid tables and the Special Coil Wiring Diagram",
        **image_fields("coil-flash-location.webp", f"{MANUAL_NAME} page 36, crop box 0.09,0.385,0.42,0.92, scanned page rendered at its native resolution (embedded image xref 175, 2552px across 8.51in), rendered at 221 dpi, capped to 620px wide, grayscale, 621x1301 WebP quality 60"),
        **CHECKED),
    excerpt_record("bulbs-and-assemblies.md", "printed pages 36 and 39 (PDF 40 and 43), Playfield - Major Assemblies and Lamp Bulbs & Sockets", **CHECKED),
    excerpt_record("diagnostics-text.md", "printed page 27 (PDF 31), Laser Kick Test, Gravestone Up & Down Test and Digital Display Test", **CHECKED),
]

CAPTURE_URL = "https://web.archive.org/web/20250108060343id_/https://www.ipdb.org/machine.cgi?id=2493"


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
        "locator": "PinmameGetGames; src/wpc/degames.c lines 1096-1150 (tftc_303 root, five clones)", "license": "BSD-3-Clause",
        "attribution": "PinMAME contributors",
    },
    pin_source(CORE, "degames.c", "lines 77-89 (INITGAMES11, FLIP6364) and 1096-1150 (tftc drivers and ROM sets)"),
    pin_source(CORE_H, "core.h", "lines 139-165, 300-360; FLIP_SWNO and public address bands"),
    pin_source(CORE_C, "core.c", "lines 1700-1777 (core_updateSw flipper copies and synthetic outputs) and 2173-2224 (core_getSol)"),
    pin_source(S11_C, "s11.c", "lines 371-410 (pia2b_w printer lines), 536-650 (setSSSol, updsol, muxing, game-on), 1170-1196 (output typing)"),
    pin_source(S11_H, "s11.h", "lines 30-60 (DE_COMPORTS), 88-95 (S11_GAMEONSOL, DE_SWADVANCE, DE_SWUPDN), 220-230 (gameSpecific1 flags)"),
    {
        "id": MANUAL, "kind": "manual",
        "uri": f"external:manuals/by-machine/{KEY}/{MANUAL_NAME}",
        "locator": f"{MANUAL_NAME}; printed pages 27-39 (PDF 31-43); GameEx-hosted scan of Data East Pinball, Inc.'s 1993 manual, 122 pages, image-only",
        "sha256": MANUAL_SHA256, "original_filename": MANUAL_NAME,
        "acquired_at": "2026-09-30T10:25:47Z",
        "excerpts": EXCERPTS_MANUAL,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Data East Pinball, Inc.",
    },
    {
        "id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=2493",
        "locator": (
            f"IPDB machine #2493, 'Tales from the Crypt' (Data East Pinball, Incorporated), 4 players, November 4, 1993 (produced Nov-4-1993 to Jan-6-1994), model number 500-5518-01, MPU DataEast/Sega Version 3, "
            f"4,500 units; features include three flippers, three pop bumpers, two slingshots, three spinning targets, two vertical up-kickers, two ramps, two scoops, a 3-bank drop target, six eyeball targets, a captive ball, "
            f"3- and 6-ball multiball, a door-handle autoplunger, a shaker motor and a rising and lowering gravestone. Retained Wayback capture {CAPTURE_URL}. Identity cross-checked against the manual's title, the PinMAME "
            f"driver description and the retained table's name."
        ),
        "sha256": IPDB_SHA256, "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
    },
    {
        "id": RUNTIME_SRC, "kind": "runtime_scenario",
        "uri": "internal:evidence/runtime/data-east/tales-from-the-crypt-tftc_303-service-tests.json",
        "locator": (
            "US 3.03 (tftc_303) in six fresh-state harness runs: the service tests (Active Switch Test of public 1-64 and 81-88, discrete Lamp Test of lamps 64 down to 1, automatic Cycling Coils, "
            "Laser Kick and Tombstone Tests, and Adjustment 61 PRINTER INTERFACE) and a game start with the host serving a ball from the trough; 179 visually read 128x32 frames paired with their pixel digests; the raw runs stay under the working root with a canonical manifest"
        ),
        "revision": REVISION, "sha256": file_sha256(RUNTIME_EVIDENCE_PATH),
        "license": "NOASSERTION", "attribution": "Primary curator; legally supplied user ROMs",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": f"external:vpx-sources/data-east/tales-from-the-crypt/vpw-1.01/Tales%20from%20the%20Crypt%20%28Data%20East%201993%29_VPW_V1.01.vpx",
        "locator": "retained known-working recreation, VPW 1.01 (2021); playfield 952 x 2162; runs cGameName tftc_400",
        "sha256": TABLE_SHA256, "known_working": True, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "freneticamnesic (Future Pinball to VP conversion), 32assassin, and the VPW team credited in the script header",
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": "external:vpx-sources/data-east/tales-from-the-crypt/vpw-1.01/extracted/script.vbs",
        "locator": "table script; SolCallback map (lines 276-298), Controller.Switch handlers, cvpmMech tombstone (lines 1668-1681), Lampz.MassAssign lamp binding (lines 3000-3213)",
        "sha256": SCRIPT_SHA256, "known_working": True, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "freneticamnesic, 32assassin and the VPW team credited in the script header",
    },
    {
        "id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI,
        "original_filename": "de.vbs", "sha256": VPM_DE_SHA256, "acquired_at": "2026-09-25T23:32:01Z",
        "locator": (
            "The VPinMAME script library the retained table loads at runtime (script.vbs line 264 LoadVPM \"01120100\", \"de.vbs\", 3.02; de.vbs executes core.vbs), retained from the contributor's working "
            f"installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). de.vbs defines swLRFlip = 82 and swLLFlip = 84 and sets them from the flipper keys in vpmKeyDown/vpmKeyUp, and names the staged "
            "upper flipper keys swURFlip/swULFlip at 86 and 88."
        ),
        "license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
        "excerpts": [excerpt_record("vpm-script-library-flippers.md", "de.vbs lines 21-36, 62-111; core.vbs lines 2061-2062, 2090 and 2854; script.vbs lines 264, 297-298, 650-664, 1641-1642, 1708-1812", **CHECKED)],
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": "external:vpx-sources/data-east/tales-from-the-crypt/vpw-1.01/extracted/manifest.json",
        "locator": (
            f"vpxtool extraction of the retained table, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, with the canonical external-evidence manifest "
            f"(manifest.json SHA-256 {EXTRACTION_MANIFEST_SHA256}, recomputable with tools/build_external_evidence_manifest.py --game tftc_400)"
        ),
        "sha256": EXTRACTION_MANIFEST_SHA256, "license": "NOASSERTION", "rights": "NOASSERTION",
        "attribution": "freneticamnesic, 32assassin and the VPW team credited in the script header",
    },
    *([{
        "id": CALLOUTS, "kind": "human_review", "uri": "internal:" + CALLOUT_SEED.relative_to(ROOT).as_posix(),
        "sha256": file_sha256(CALLOUT_SEED),
        "locator": (
            "2026-10-09 factory location-drawing callout check of PDF 33, 35 and 36 (printed 29, 31 and 32: the switch, lamp and flash lamp / coil location drawings): "
            "every callout transcribed independently on 300 dpi renders of the scan without table data, curator corrections recorded with their reasons, per-page control "
            "and callout fits; a table placement whose own callout lands within 0.07 normalized under both fits is validated (tools/drawing_callouts.py). Reads, overlays "
            "and the generator are retained under review-artifacts with a pinned manifest."
        ),
        "attribution": "PinMAME game definitions contributors", "rights": "NOASSERTION", "license": "NOASSERTION",
    }] if CALLOUT_DATA else []),
    {
        "id": LEGACY, "kind": "legacy_json", "uri": "https://github.com/vpinball/pinmame-game-defs", "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
        "locator": "games/tftc.json; origin=vbscript-parser", "attribution": "pinmame-game-defs contributors",
    },
]

# --- Coverage ---------------------------------------------------------------------------------------------------------
# Every requirement whose evidence is not complete, each with the device or record that keeps it open:
# input_semantics, the W7 jumper whose meaning no retained source states; polarity, the Green FORWARD/REVERSE button (-6);
# spatial_placement, every placement observed from one recreation lineage.
MISSING = ["input_semantics", "polarity", "spatial_placement"]
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
        "name": "Tales from the Crypt",
        "manufacturer": "Data East",
        "year": 1993,
        "kind": "physical_pinball",
        "model_number": "500-5518-01",
        "ipdb_id": 2493,
        "opdb_id": "GR6wO-MDvzk",
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
    "knowledge": {"path": "knowledge/data-east/tales-from-the-crypt-1993.md", "status": "complete"},
}

# Factory location-drawing callouts promote the placements they confirm.
CALLOUT_DECISIONS = drawing_callouts.apply_to_definition(definition, CALLOUT_DATA, CALLOUTS) if CALLOUT_DATA else None

# --- Spatial report ------------------------------------------------------------------------------------------------------
_placed = sum(len(d.get("spatial", {}).get("placements", [])) for d in inputs + outputs)
_no_spatial_key = sorted(d["id"] for d in inputs + outputs if "spatial" not in d and d["availability"] in ("used", "unknown"))
if PLACES["table_bounds"]:
    _convention = (
        "x = 0 is the left side and x = 1 the right side; y = 0 is the rear and y = 1 the apron end, normalized against the retained table's own playfield bounds "
        f"({PLACES['table_bounds']['width']:.0f} x {PLACES['table_bounds']['height']:.0f} VPX units, asserted rather than assumed)."
    )
else:
    _convention = "No coordinates are recorded yet."
spatial_report = {
    "format": "pinmame-spatial-blockers",
    "version": 1,
    "machine_id": KEY,
    "status": "partial",
    "coordinate_convention": _convention,
    "placement_count": _placed,
    "source": {"table": TABLE, "extraction": EXTRACTION, "extraction_file_count": EXTRACTION_FILE_COUNT, "extraction_manifest_sha256": EXTRACTION_MANIFEST_SHA256},
    "blockers": [
        {
            "id": "single-retained-recreation",
            "severity": "major",
            "detail": (
                "Exactly one known-working recreation is admitted as spatial evidence: the VPW 1.01 table. A second retained table, Bigus MOD 1.3, credits the same freneticamnesic and 32assassin "
                "lineage and carries the author's own 'not verified yet' header, so it is one derivative chain, not independent geometry. The factory location drawings on manual pages 29, 31 and 32 "
                "validate the placements whose own callouts land within the limit (drawing_callout_check); every other placement stays `observed`. Those location drawings leave out the "
                "general illumination. The Lamp Bulbs & Sockets drawing on printed page 39 (PDF 43) marks every playfield bulb, G.I. included, but only by bulb type, not by circuit, "
                "so the G.I. emitters need a reproducible measurement of that drawing reconciled against the lamp and flash-lamp sockets, or an independent table."
            ),
        },
        {
            "id": "devices-without-a-retained-object",
            "severity": "major",
            "detail": "These used or unresolved devices have no honest coordinate in the retained recreation, so their spatial key is omitted rather than fabricated.",
            "omitted_spatial_key_devices": _no_spatial_key,
        },
        {
            "id": "flasher-effects-are-not-a-socket-survey",
            "severity": "major",
            "detail": (
                "The retained table binds visual Light effects, not surveyed physical bulb sockets, and the manual's own flash-lamp bulb counts disagree by one (32 drawn, 31 listed). "
                "Flasher placements are presentation effects, not a complete socket survey."
            ),
        },
    ],
    "unresolved": PLACES.get("unplaced", []),
}
if CALLOUT_DECISIONS:
    spatial_report["drawing_callout_check"] = drawing_callouts.summary(
        CALLOUT_DATA, CALLOUT_DECISIONS, CALLOUT_SEED.relative_to(ROOT).as_posix(), file_sha256(CALLOUT_SEED)
    )

# --- Knowledge note ------------------------------------------------------------------------------------------------------
_KNOWLEDGE_TEMPLATE = ROOT / "tools/tales_from_the_crypt_knowledge.md"
KNOWLEDGE_TEXT = _KNOWLEDGE_TEMPLATE.read_bytes().decode("utf-8") if _KNOWLEDGE_TEMPLATE.is_file() else ""
_validated = sum(1 for d in inputs + outputs for p in d.get("spatial", {}).get("placements", []) if p["provenance"]["status"] == "validated")
knowledge_note = KNOWLEDGE_TEXT.replace("{driver_count}", str(len(drivers))).replace("{placed}", str(_placed)).replace("{validated}", str(_validated))


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
    existing = root / "machines/author-ready/data-east/tales-from-the-crypt-1993.json"
    if existing.is_file() and definition["coverage"]["status"] != "author_ready":
        raise RuntimeError(f"refusing to curate while an author-ready artifact exists (preserved): {existing}")
    for path, payload in _artifacts():
        target = root / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as stream:
            stream.write(payload)


def _check(root: Path) -> None:
    for path, expected in _artifacts():
        target = root / path.relative_to(ROOT)
        if not target.is_file():
            raise RuntimeError(f"Tales from the Crypt artifact is missing: {target}")
        if _comparable(target.read_bytes()) != _comparable(expected):
            raise RuntimeError(f"Tales from the Crypt artifact does not match the deterministic curator: {target}")
    report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
    expected_format = "pinmame-spatial-audit" if definition["coverage"]["status"] == "author_ready" else "pinmame-spatial-blockers"
    if report.get("format") != expected_format or report.get("machine_id") != KEY:
        raise RuntimeError(f"Tales from the Crypt spatial report must be {expected_format} and name this machine")
    placements = sum(len(d.get("spatial", {}).get("placements", [])) for c in ("inputs", "outputs") for d in definition[c])
    if report.get("placement_count") != placements:
        raise RuntimeError(f"Tales from the Crypt spatial report claims {report.get('placement_count')} placements but the definition carries {placements}")
    print("Tales from the Crypt definition, seed, spatial report, and knowledge note match the deterministic curator.")


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
