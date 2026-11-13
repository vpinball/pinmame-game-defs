"""Deterministically curate Sega Mary Shelley's Frankenstein (1995), Data East 3b, from reviewed evidence.

The complete printed regions in evidence/excerpts are the tabular input; the ROM's own service-test
readings are pinned in tools/seeds and evidence/runtime; frankenstein_places.json holds recomputable
observed geometry. No external evidence is needed to regenerate. Optional evidence roots are verified
fail-closed when provided. A partial cannot overwrite an author-ready record.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_flipper_column import (
    flipper_column_inputs, flipper_column_relationships, vpm_staged_flipper_notes,
    VPM_DE_LIBRARY_SOURCE, VPM_DE_LIBRARY_URI, VPM_DE_SHA256,
)

ROOT = Path(__file__).resolve().parents[1]
KEY = "sega.mary-shelley-s-frankenstein.1995"
SLUG = "mary-shelley-s-frankenstein-1995"
REV = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
MANUAL = "manual.mary-shelley-s-frankenstein.production"
SCHEMATICS = "manual.mary-shelley-s-frankenstein.schematics"
CHART = "manual.mary-shelley-s-frankenstein.tech-chart"
CORE = "pinmame.mary-shelley-s-frankenstein.core"
SCRIPT = "vpx-script.mary-shelley-s-frankenstein.1-2"
TABLE = "vpx-table.mary-shelley-s-frankenstein.1-2"
EXTRACTION = "vpx-extraction.mary-shelley-s-frankenstein.1-2"
RUNTIME = "runtime.mary-shelley-s-frankenstein.frankst"
GEOMETRY = "geometry.mary-shelley-s-frankenstein.1-2"
DEFINITION_PATH = ROOT / f"machines/partial/sega/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/sega/{SLUG}.json"
READINGS_PATH = ROOT / f"tools/seeds/sega/{SLUG}-runtime-readings.json"
RUNTIME_PATH = ROOT / "evidence/runtime/data-east/mary-shelley-s-frankenstein-frankst-service-tests.json"
KNOWLEDGE_PATH = ROOT / f"knowledge/sega/{SLUG}.md"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/sega/{SLUG}.json"
PLACES_PATH = ROOT / "tools/frankenstein_places.json"
EXCERPTS = ROOT / "evidence/excerpts" / KEY
MISSING = ["input_semantics", "output_semantics", "mechanism_behavior", "spatial_placement"]
MANUAL_NAME = "Sega_1995_Mary_Shelley_s_Frankenstein_English_Manual_pages_1_66_which_excludes_schematics_OCR_searchable.pdf"
SCHEMATICS_NAME = "Sega_1995_Mary_Shelley_s_Frankenstein_English_Manual_pages_67_93_which_are_the_schematics_OCR_searchable.pdf"
CHART_NAME = "Sega_1995_Mary_Shelley_s_Frankenstein_Solenoid_Switch_and_Lamp_Matrix_Charts.pdf"
ACQUIRED = "2026-11-13T14:16:00Z"
MANUALS = {
    MANUAL_NAME: "2f752c431e3b2a4718180e52340c5394f36b41833a150464f04d52d442be8764",
    SCHEMATICS_NAME: "e4eeb409e321ea1eb3f9d30120e488db8b638a6d3d69f3c66c2c9ca7919bf883",
    CHART_NAME: "1aaf40f86466ad57b5e6c2dfc4d040dce2d8ddfe98a67855084815304129ed97",
}
UNUSED_SWITCHES = {30, 49, 50, 51, 52, 57, 58, 59, 60, 61}
CABINET_SWITCHES = {1, 2, 3, 4, 5, 6, 7, 8, 62, 63, 64}
UNUSED_LAMPS = {49, 50, 51, 52, 53, 54, 57, 58, 59, 60, 61, 62}
CABINET_LAMPS = {63, 64}
UNUSED_DRIVERS = {32}
SWITCH_LABELS = (
    "Plumb Bob Tilt|4th Coin Slot|Start Button|Right Coin Slot|Center Coin Slot|Left Coin Slot|Slam Tilt|"
    "Extra Ball Buy-in Button|Trough Ball 1 Left|Trough Ball 2|Trough Ball 3|Trough Ball 4|Trough Ball 5|"
    "Trough Ball 6 Right|Trough Up-Kicker Ball 7|Shooter Lane|Stand-up F Bottom 2-Bank Left|"
    "Stand-up R Bottom 2-Bank Right|Stand-up A Middle 3-Bank Bottom|Stand-up N Middle 3-Bank Middle|"
    "Stand-up K Middle 3-Bank Top|Stand-up E Top 3-Bank Left|Stand-up N Top 3-Bank Middle|Stand-up S Top 3-Bank Right|"
    "Move Jackpot Stand-up|Stand-up T Ramp Left|Stand-up E Ramp Right|Stand-up I Right 2-Bank Top|"
    "Stand-up N Right 2-Bank Bottom|Unused 30|Sarcophagus Upper Scoop|Geneva Lower Scoop|Left Orbit Bottom|"
    "Left Orbit Top|Right Orbit Top|Right Orbit Bottom|Left Outlane|Left Return Lane|Right Return Lane|Right Outlane|"
    "Top Turbo Bumper|Middle Left Turbo Bumper|Middle Right Turbo Bumper|Bottom Turbo Bumper|Ramp Entrance Gate|"
    "Ramp Exit Gate|Left Slingshot|Right Slingshot|Unused 49|Unused 50|Unused 51|Unused 52|North Pole VUK|"
    "Ingolstadt Right Orbit Spinner|Ice Cave Ball Eject|Mini-Orbit Rollover by Eject|Unused 57|Unused 58|Unused 59|"
    "Unused 60|Unused 61|The Switch Lever|Left Flipper Button Matrix Copy|Right Flipper Button Matrix Copy"
).split("|")
LAMP_LABELS = (
    "Letter F|Letter R|Letter A|Letter N 1|Letter K|Letter E 1|Letter N 2|Letter S|Letter T|Letter E 2|Letter I|"
    "Letter N 3|Top Turbo Bumper|Middle Left Turbo Bumper|Middle Right Turbo Bumper|Bottom Turbo Bumper|"
    "Frankenstein Millions Mode|Stoning Mode|Creature Feature Mode|Lynch Justine Mode|North Pole Mode|"
    "Lite Extra Ball Mode|Voltage Mode|Graveyard Mode|Ramp Jackpot|North Pole VUK Jackpot|Ice Cave Ball Eject Jackpot|"
    "Left Orbit Jackpot|Geneva Lower Scoop|Sarcophagus Upper Scoop|VUK Entrance Left|VUK Entrance Right|"
    "Left Outlane Alive Kick-Back|Left Outlane Special|Left Return Lane Lite Ingolstadt|Right Return Lane Lite Geneva|"
    "Right Outlane Double Bonus|Ice Cave Mode|Lite Lock 1|Lite Lock 2|Move Jackpot|Change Scene|"
    "Ingolstadt Spinner Mode|Jackpot Grows|Justine Mode|Extra Ball|Creature Mode|Shooter Lane|Unused Lamp 49|"
    "Unused Lamp 50|Unused Lamp 51|Unused Lamp 52|Unused Lamp 53|Unused Lamp 54|Live Again Shoot Again|"
    "VUK Entrance Middle|Unused Lamp 57|Unused Lamp 58|Unused Lamp 59|Unused Lamp 60|Unused Lamp 61|Unused Lamp 62|"
    "Extra Ball Buy-in Button|Start Button"
).split("|")
# Number, label and kind of every fitted driver; flashers 25-31 are the PPB's right-side loads 1R-7R.
COILS = {
    1: ("6-Ball Trough Lockout", "coil"), 2: ("Trough Up-Kicker", "coil"), 3: ("Autolaunch", "coil"),
    4: ("Geneva Lower Scoop Kick-Big", "coil"), 5: ("Sarcophagus Upper Scoop Kick-Big", "coil"),
    6: ("Ice Cave Ball Eject", "coil"), 7: ("North Pole VUK", "coil"), 8: ("Knocker", "coil"),
    9: ("Ramp Trap Door Right", "coil"), 10: ("Left Right A-B Relay", "relay"), 11: ("General Illumination Relay", "gi"),
    12: ("Ramp Trap Door Left", "coil"), 13: ("Creature Arms Throw", "coil"), 14: ("Right Orbit Ball Diverter", "coil"),
    15: ("Flasher Upper Right Playfield Around VUK", "flasher"), 16: ("Laser Kick Kickback", "coil"),
    17: ("Top Turbo Bumper", "coil"), 18: ("Middle Left Turbo Bumper", "coil"), 19: ("Middle Right Turbo Bumper", "coil"),
    20: ("Bottom Turbo Bumper", "coil"), 21: ("Left Slingshot", "coil"), 22: ("Right Slingshot", "coil"),
    25: ("Flasher 1R Above A-N-K", "flasher"), 26: ("Flasher 2R Above F-R", "flasher"), 27: ("Flasher 3R Above I-N", "flasher"),
    28: ("Flasher 4R Pop Bumpers", "flasher"), 29: ("Flasher 5R By Spinner", "flasher"),
    30: ("Flasher 6R Upper Left Corner", "flasher"), 31: ("Flasher 7R Around VUK", "flasher"),
}
DRIVER_ROWS = (
    ("frankst", "Frankenstein, Mary Shelley's", "1994"),
    ("frankstg", "Frankenstein, Mary Shelley's (German)", "1995"),
    ("franksti", "Frankenstein, Mary Shelley's (Italian)", "1995"),
)
MERGED = "[merged with row above]"
# Coils whose part number the driver table and the wiring sheets print differently: none is asserted.
DISPUTED_PARTS = {6, 7, 20}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def prov(*refs, status="validated"): return {"status": status, "source_refs": list(dict.fromkeys(refs))}
def na(reason, *refs): return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}
def slug(text): return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
def clause(text): return text.rstrip(".")
def aliases(group, n, manual=None):
    return [{"namespace": f"pinmame.{group}", "value": str(n)}] + ([] if manual is None else [{"namespace": "manual.address", "value": manual}])


def table(filename, header):
    """The rows of the one markdown table in an excerpt whose header line is exactly ``header``."""
    lines = (EXCERPTS / filename).read_text(encoding="utf-8").splitlines()
    if lines.count(header) != 1:
        raise ValueError(f"expected one table {header!r} in {filename}")
    start = lines.index(header) + 2
    result = []
    for line in lines[start:]:
        if not line.startswith("| "):
            break
        result.append([x.strip() for x in line.strip().strip("|").split("|")])
    width = header.count("|") - 1
    if any(len(r) != width for r in result):
        raise ValueError(f"ragged table {header!r} in {filename}")
    return result


def checked_excerpt(filename, locator):
    path = EXCERPTS / filename
    return {"id": slug(path.stem), "locator": locator, "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha(path), "method": "manual",
            "transcribed_by": "Curator; direct visual verification of retained native-resolution renders", "reviewed": True}


def readings():
    """The ROM's own ACTIVE SWITCH, SINGLE LAMP and COIL TEST texts, pinned to frame digests in the readings seed."""
    found = {}
    for item in load_json(READINGS_PATH)["readings"]:
        if item["group"] in ("switch", "lamp", "solenoid"):
            found.setdefault((item["group"], item["address"]), item)
    return found


def spatial(key, identifier, role, places, *refs):
    hits = places["placements"].get(key, [])
    if not hits:
        return None
    sources = refs or (TABLE, SCRIPT, GEOMETRY)
    return {"status": "observed", "placements": [
        {"id": f"{identifier}.{role}.{i}", "role": role, "space": "playfield", "x": h["x"], "y": h["y"],
         "provenance": prov(*sources, status="observed")} for i, h in enumerate(hits, 1)]}


def switch_type(n):
    return "tilt" if n in (1, 7) else "button" if n in (3, 8) else "other"


def coil_rows():
    rows = table("coils.md", "| Coil No. | Coil or Flashlamp Description | Drive Transistor (D.T.) | On Which Board? | D.T. Control Line | D.T. Control Line Connect | Power Line | Power Line Connection | Power Description | Coil or Flash Type |")
    resolved, previous = {}, None
    for row in rows:
        row = [previous[i] if cell == MERGED else cell for i, cell in enumerate(row)]
        resolved[row[0]] = previous = row
    return resolved


def build():
    switch_list = {int(r[0]): r for r in table("switches.md", "| Number | Description as printed | Part No. |")}
    switch_chart = {int(r[0]): r[3] for r in table("switches.md", "| Cell | Column | Row | Cell text as printed |")}
    lamp_chart = {int(r[0]): r[3] for r in table("lamps.md", "| Number | Column | Row | Cell text as printed |")}
    lamp_list = {int(r[0]): r[1] for r in table("lamps.md", "| Number | Description as printed |")}
    coils = coil_rows()
    sw_drive = [tuple(r[1:]) for r in table("switches.md", "| Column (Drive) | Transistor | Wire | Connector |")]
    sw_return = [tuple(r[1:]) for r in table("switches.md", "| Row (Return) | Wire | Connector |")]
    lamp_drive = [tuple(r[1:]) for r in table("lamps.md", "| Column | Transistor | Wire | Connector |")]
    lamp_return = [tuple(r[1:]) for r in table("lamps.md", "| Row | Transistor | Wire | Connector |")]
    if any(len(x) != 8 for x in (sw_drive, sw_return, lamp_drive, lamp_return)):
        raise ValueError("incomplete Frankenstein printed matrix headings")
    for name, grid in (("switch list", switch_list), ("switch chart", switch_chart), ("lamp chart", lamp_chart), ("lamp list", lamp_list)):
        if set(grid) != set(range(1, 65)):
            raise ValueError(f"incomplete Frankenstein printed {name}")
    if set(coils) != {f"{n}{s}" for n in range(1, 9) for s in "LR"} | {f"{n:02d}" for n in range(9, 23)}:
        raise ValueError("incomplete Frankenstein printed driver table")
    if len(SWITCH_LABELS) != 64 or len(LAMP_LABELS) != 64:
        raise ValueError("incomplete Frankenstein semantic inventory")
    rom = readings()
    places = load_json(PLACES_PATH)
    inputs, outputs = [], []

    for n in range(1, 65):
        number, description, part_cell = switch_list[n]
        label = SWITCH_LABELS[n - 1]
        identifier = "switch." + slug(label)
        col, row = (n - 1) // 8, (n - 1) % 8
        unused = n in UNUSED_SWITCHES
        part = part_cell if re.fullmatch(r"\d{3}-\d{4}-\d{2}", part_cell) else None
        reading = rom.get(("switch", n))
        notes = f"Switch matrix chart: {clause(switch_chart[n])}. Switch list: {clause(description)}; part {part_cell}."
        if reading:
            notes += f" The ROM's ACTIVE SWITCH TEST prints {reading['name']}, {reading['drive_wire']} {reading['return_wire']} {reading['number']}."
        notes += {
            15: " The up-kicker position at the right end of the 6-ball trough, part 180-5118-00 where positions 9-14 carry 180-5119-00. The ROM calls it 6-BALL TROUGH #7 (VUK); the table's BallRelease kicker sets it.",
            16: " The table also places a plastic bulb for lamp 48 beside this rollover.",
            25: " The move-jackpot stand-up between the two FRANKENSTEIN banks; the chart prints \" Move Jackpot \" in quotes.",
            31: " The scoop behind the upper scoop entrance (\"ENTRANCE TO UPPER SCOOP (WITH KICK-BIG)\"); output 5 kicks it out.",
            32: " The scoop behind the lower scoop entrance (\"ENTRANCE TO LOWER SCOOP (WITH KICK-BIG)\"); output 4 kicks it out.",
            37: " The left outlane rollover in front of the Kick Back under the arch; with Alive lit it fires output 16.",
            42: " The ROM names it LEFT TURBO BUMPER.", 43: " The ROM names it RIGHT TURBO BUMPER.",
            45: " The gate at the large ramp entrance; in the harness each closure flashed output 15.",
            46: " The overview's LARGE RAMP EXIT GATE at the upper left.",
            53: " The North Pole vertical up-kicker saucer at the upper right; output 7 lifts the ball to the upper level ramp.",
            54: " The Ingolstadt spinner in the right orbit; in the harness a spin fired the right orbit diverter 14.",
            55: " The Ice Cave saucer at the upper left behind the 1-way gate; output 6 ejects the ball.",
            62: " \"The Switch\", the cabinet lever assembly connected with the Ball Auto Launch; the ROM's AUTOLAUNCH LEVER. The table writes it from the plunger key.",
        }.get(n, "")
        if 9 <= n <= 14:
            notes += " A position in the 6-ball trough under the metal arch; balls rest from 9 (left) to 14 (right), where lock-out 1 releases them toward 15. The table models the trough as a ball stack with no switch object."
        if n in (63, 64):
            notes += f" FLIP6364 copies {'84' if n == 63 else '82'} into this matrix address on every update, so drive that flipper-column button, not {n}; the table's direct writes to {n} are commented out. A direct write to {n} reads back 0 and the ROM shows NONE."
            notes += " The switch list routes the right cabinet button through the 3-flipper board to both the lower and the upper right flipper." if n == 64 else ""
        if n in (2, 4, 5, 6):
            notes += " A coin-door switch not drawn on the playfield."
        item = {"id": identifier, "label": label, "kind": "switch", "binding": {"group": "pinmame.input.switch", "device": n},
                "aliases": aliases("switch", n, str(n)), "availability": "unused" if unused else "used",
                "provenance": prov(MANUAL, CHART, SCHEMATICS, CORE, RUNTIME, *([] if unused or n in CABINET_SWITCHES - {1, 62} or 9 <= n <= 14 else [SCRIPT])),
                "physical": {"notes": notes},
                "wiring": {"board": "CPU", "driver_transistor": sw_drive[col][0], "drive_wire": sw_drive[col][1],
                           "drive_connection": sw_drive[col][2], "return_wire": sw_return[row][0], "return_connection": sw_return[row][1]}}
        if not unused:
            item["normally_closed"] = False
            item["physical"]["switch_type"] = switch_type(n)
            if part:
                item["physical"]["part_number"] = part
        if n in (63, 64):
            item["roles"] = [f"flipper.lower.{'left' if n == 63 else 'right'}.matrix-copy"]
        if unused:
            item["spatial"] = na("unused", MANUAL, RUNTIME)
        elif n in CABINET_SWITCHES:
            item["spatial"] = na("cabinet_or_service", MANUAL, CORE)
        elif (s := spatial(f"switch.{n}", identifier, "sensor", places)):
            item["spatial"] = s
        inputs.append(item)

    for n, label in ((-7, "Black Begin Test / Step Button"), (-6, "Green Forward/Reverse Button")):
        inputs.append({
            "id": f"switch.service-{'enter' if n == -7 else 'select'}", "label": label, "kind": "switch",
            "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": aliases("switch", n),
            "availability": "used", "pulse": n == -7, "normally_closed": False,
            "physical": {"switch_type": "button", "location": "inside coin door",
                         "notes": ("The manual's diagnostics steps tests with the STEP push-button switch; Black is DE_SWADVANCE -7. In the harness each Black press stepped to the next test title." if n == -7 else
                                   "The manual's FORWARD/REVERSE push-button switch (up = forward). des11 uses DE_COMPORTS, whose Green input toggles (COREPORT_BITTOG), and the pinned s11.h notes that games after Frankenstein used a non-toggling switch; de.vbs also toggles -6 on each key press. The harness held -6 at 1 so Black and Start stepped forward.")},
            "provenance": prov(MANUAL, CORE, RUNTIME, VPM_DE_LIBRARY_SOURCE),
            "spatial": na("cabinet_or_service", MANUAL),
        })
    inputs.extend(flipper_column_inputs(
        flip_swno=(63, 64), flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)", core_refs=(CORE,),
        button_refs=(SCRIPT, VPM_DE_LIBRARY_SOURCE, RUNTIME),
        button_notes={side: f"The table's key handler leaves its direct write to {63 if side == 'left' else 64} commented out and calls de.vbs vpmKeyDown, whose swL{'L' if side == 'left' else 'R'}Flip is {84 if side == 'left' else 82}; the harness read back {63 if side == 'left' else 64} = 1 only while {84 if side == 'left' else 82} was held, and the ROM's ACTIVE SWITCH TEST then names {'LEFT' if side == 'left' else 'RIGHT'} END OF STROKE #{63 if side == 'left' else 64}, the manual's {'Lower Left Flipper Cabinet' if side == 'left' else 'Lower & Upper Right Flipper Cabinet'} switch. " + ("The left cabinet button switches the lower left flipper on the 3-flipper board." if side == "left" else "The right cabinet button switches both the lower right and the upper right flipper on the 3-flipper board.") for side in ("left", "right")},
        unused_notes=vpm_staged_flipper_notes(library="DE.VBS"), unused_note_refs=(VPM_DE_LIBRARY_SOURCE,)))
    for item in inputs:
        if item["binding"]["device"] in (82, 84):
            item["normally_closed"] = False
            item["provenance"]["source_refs"].append(MANUAL)
            item["physical"]["notes"] += " The Flipper Solenoids table (PDF 40) wires each cabinet switch from the matrix drive GRN-GRY to the 3-flipper board as an ordinary switch input."
    inputs.append({"id": "dip.country-jumper-w7", "label": "Country Jumper W7", "kind": "dip_switch",
                   "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [], "availability": "unknown",
                   "physical": {"notes": "s11.c pia2a_r reads core_getDip(0)<<7 under the comment Jumper W7. No retained Frankenstein evidence assigns its two values to a country or a fitted jumper position."},
                   "provenance": prov(CORE, status="observed"), "spatial": na("dip_switch", CORE)})

    for n in range(1, 65):
        manual_number = f"{n}L" if n <= 8 else f"{n - 24}R" if 25 <= n <= 32 else f"{n:02d}"
        printed = coils.get(manual_number)
        reading = rom.get(("solenoid", n))
        if n in COILS:
            label, kind = COILS[n]
            identifier = f"{kind}." + slug(label)
            notes = f"Driver table {manual_number}: {clause(printed[1])}; {printed[8]}, {printed[9]}."
            if reading:
                notes += f" The ROM's COIL TEST prints {reading['number']} {reading['name']} with the wires {reading['power_wire']} {reading['control_wire']} and fires this address alone."
            physical = {"notes": notes}
            if kind == "coil" and n not in DISPUTED_PARTS and re.fullmatch(r"\d{2}-\d{3,4}", printed[9]):
                physical["part_number"] = printed[9]
                physical["quantity"] = 1
            if kind == "flasher":
                physical["quantity"] = 4
                physical["part_number"] = "Bulb #89; Bulb #906" if n == 30 else "Bulb #89"
            physical["notes"] += {
                1: " The 6-ball trough lock-out releases the ball at position 14 toward the up-kicker position 15. In the harness the ROM fired 1 after Start and again to serve each replacement ball.",
                2: " The Trough Up-Kicker (TRUK) lifts the ball at 15 into shooter lane 16; the location legend calls 2L \"Ball Eject to Shooter Lane\". In the harness it fired once 15 closed.",
                3: " Ball Auto Launch under the butyrate at the shooter lane, connected with the cabinet lever \"The Switch\" (62). In the harness the first pull of 62 with a ball at 16 fired 3. Supply 50v L (PPB J 7-8) through the PPB helper transistor Q5.",
                4: " The Geneva (lower) scoop kick-big. The location legend prints \"Bot. Scoop Kick-Big 50v\"; the driver table and the wiring diagram put it on the +32VL BRN bus.",
                5: " The Sarcophagus (upper) scoop kick-big, 50v L with the PPB helper transistor Q2. The driver table and the Tech Chart print board CPU on this row and CPU/PPB on its flasher row 5R, which uses Q42 alone; the cells are kept as printed.",
                6: " The Ice Cave playfield ball eject at the upper left. The driver table and the Tech Chart print board PPB on this row and CPU on its flasher row 6R, which share the CPU drive transistor Q41; the cells are kept as printed. The driver table and Tech Chart print coil 24-940; the coil wiring diagram (schematics PDF 6) and the coil chart page (PDF 41) print EJECT 26-1200, so no coil part number is asserted.",
                7: " The North Pole vertical up-kicker lifts the ball from 53 to the upper level ramp, which carries the trap doors to the creature and continues as the wire ramp to the right return lane. The driver table and Tech Chart print coil 24-940; the coil wiring diagram prints RIGHT VUK 24-1240 and the coil chart page 25-1240, so no coil part number is asserted.",
                8: " Knocker 32v in the cabinet. Adjustment 44 External Replay Knocker lets the operator use it to drive an external device.",
                9: " Opens the right trap door in the upper level ramp; the overview labels the trap doors \"TO LEFT (LONG TROUGH) & RIGHT (SHORT TROUGH) CREATURE HANDS\". The table names this callback SolTrapLeftHand after the creature's left hand, which is on the player's right.",
                10: " K1 A/B relay on the PPB in the backbox selects the 1L-8L coil loads (off) or the 1R-8R flasher loads (on) on drives 1-8. The COIL TEST selects it before every R entry and has no entry of its own.",
                11: " A 24v DC relay on the power supply board switches the G.I. supply. The table lights its G.I. while the relay is off. Placements are the table's 22 G.I. bulb lights; the manual gives no complete G.I. socket list.",
                12: " Opens the left trap door in the upper level ramp, dropping the ball into the creature's right hand on the player's left.",
                13: " Swings both creature arms to throw the balls held in the creature's hands (\"WHICH CAN HOLD 1 BALL IN EACH HAND TO THROW\"); the ROM calls it CREATURE THROW. Adjustment 51 Enable Creature Throw set to NO disables the arms and the trap doors, and Adjustment 52 sets the throw pulse. The five service-test runs, booted with an empty trough, saw the ROM pulse 13 once about 3.8 s after power-up; the gameplay run, booted with six balls in the trough, did not. The Tech Chart prints Monster Arms 50v with Q26/Q3 on PPB J 8-7 (VIO-YEL, PPB J 7-3); the manual's driver table, the coil wiring diagram (MONSTER ARMS 23-800 on CPU CN12-6) and the ROM's RED power wire agree on 32v from the power supply, which this record follows.",
                14: " The right orbit ball diverter (\"DIVERTER ASSEMBLY (UNDER THE RAMPS)\"). In the harness a spin of the Ingolstadt spinner 54 fired it. The ROM's other entries print the power wire first and the control wire second; here it prints BRN-BLU VIO-YEL, where the driver table prints power RED and control BRN-BLU, which this record follows.",
                15: " The driver table prints type 27-1500 for this flashlamp; the coil wiring diagram draws it as \"(4) UPPER RIGHT PLAYFIELD\" with four No. 89 bulbs on BRN/VIO \"(TO Q24)\", which this record follows. In the harness each ramp entrance closure flashed it. The driver table prints power RED from PS CN 3-6,7, but the coil wiring diagram feeds this group with ORG 15 from \"+32VDCR PPBJ6-4/5\", the flasher bus the driver table prints ORN on PPB J 6-4, 5 for 1R-7R, and the ROM's COIL TEST also prints ORG. The record follows the diagram and the ROM, in the driver table's spelling for that bus.",
                16: " The Laser Kick, the kick back under the arch at the left outlane: with Alive lit, left outlane switch 37 fires it (observed in the harness gameplay run). The platform's cabinet wiring sheet shows a SHAKER MOTOR BD on PPB J8-12 \"SOLENOID DRIVE 16\"; this game's driver table, the ROM and the table bind 16 to the kickback. The driver table and the cabinet sheet print the control line on PPB J8-12; the playfield coil diagram (schematics PDF 6) draws the Laser Kick's BRN/GRY line to J8 pin 10. The record follows the two that agree. Adjustment 46 Laser Kick Present allows a game without the coil: with it set to NO, a lit Alive returns a left-outlane drain to the shooter lane instead.",
                20: " The driver table and the Tech Chart print 23-800 where the other three turbo bumpers print 23-700; the special coil diagram (schematics PDF 7) prints BOTTOM TURBO BUMPER 23-700 like the others, so no coil part number is asserted.",
                22: " The ROM prints RED VIO-YEL, a VIO-YEL control wire; the driver table and the special coil diagram print BLU-BLK and BLU/BLK, which this record follows. The Tech Chart's transistor cell is smudged; the manual prints Q13.",
            }.get(n, "")
            if kind == "flasher" and n != 15:
                physical["notes"] += (" Three No. 89 sockets and one No. 906 on this branch per the coil wiring diagram, where the driver table prints Bulb #89" if n == 30 else " Four No. 89 sockets on this branch per the coil wiring diagram") + "; the driver table's P/F and Insert counts split them between the playfield and the backbox insert, whose sockets are not in playfield space."
            item = {"id": identifier, "label": label, "kind": kind, "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n, manual_number), "availability": "used", "physical": physical,
                    "provenance": prov(MANUAL, CHART, SCHEMATICS, CORE, RUNTIME, *([] if n == 10 else [SCRIPT]))}
            item["wiring"] = {"board": printed[3], "driver_transistor": printed[2],
                              "control_wire": printed[4], "control_connection": printed[5],
                              "power_wire": printed[6], "power_connection": printed[7]}
            if n == 15:
                item["wiring"].update(power_wire=coils["1R"][6], power_connection=coils["1R"][7])
            if n in (8, 10):
                item["spatial"] = na("cabinet_or_service", MANUAL)
            elif (s := spatial(f"solenoid.{n}", identifier, "emitter" if kind in ("gi", "flasher") else "effect", places)):
                item["spatial"] = s
        elif n in UNUSED_DRIVERS:
            label = f"Unused Driver {manual_number}"
            identifier = "virtual." + slug(label)
            item = {"id": identifier, "label": label, "kind": "virtual", "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n, manual_number), "availability": "unused",
                    "physical": {"notes": ("Driver table row 8R prints \"Flashlamp: X0 P/F, Insert X0 Not Used in this Game.\" with dash placeholders in every wiring cell; the location legend shades 8R Not Used and the coil wiring diagram prints \"(4) NOT USED\" on the BLK/GRY branch, with a handwritten NOT USED. "
                                           "The ROM's own diagnostics publish state here: the COIL TEST shows #8R FLASH:NOT USED and fires it behind relay 10, and CYCLING FLASHERS and CYCLING COILS walk it with the other R loads. No gameplay or attract run published it. The diagnostics walk every driver slot, so this state drives no load. "
                                           "The pinned s11.c PWM branch types only 25-31 as #89 flashers.")},
                    "provenance": prov(MANUAL, CHART, SCHEMATICS, CORE, RUNTIME), "spatial": na("unused", MANUAL, RUNTIME),
                    "wiring": {"board": printed[3], "driver_transistor": printed[2]}}
        else:
            is_aux, is_flip = 37 <= n <= 44, 45 <= n <= 48
            label = (f"CN3 Printer Data Bit {n - 37}" if is_aux else
                     f"Synthetic Lower {'Right' if n <= 46 else 'Left'} Flipper {'Power' if n % 2 else 'Hold'}" if is_flip else
                     f"Unused Solenoid Address {n}")
            identifier = f"virtual.{slug(label)}"
            printer_pin = {37: 9, 38: 8, 39: 7, 44: 1}.get(n)
            note = ("S11_PRINTERLINE publishes PIA2:B bit " + str(n - 37) + " here. "
                    + (f"The pinned pia2b_w comment names CN3 pin {printer_pin}, which the backbox wiring sheet labels DATA LINE TO PRINTER. " if printer_pin is not None else "The pinned pia2b_w comment elides bits 3-6, so no connector pin is asserted. ") + "The manual's adjustments 58-61 describe an audit print-out, Reset Printer? and a Printer Interface that prints on Start, so a printer is an option on this machine. "
                    + ("The ROM drives this bit, so PinMAME publishes meaningful state here: in every run it toggles at power-up, and in the SERVO TEST it toggles around every creature head command, where 44 rises and falls while 37 and 38 toggle. The servo board takes a clock, data and an active-high enable from the CPU (its CN1-2, CN1-3, CN1-4), but no retained drawing connects it to CPU CN3, and CPU CN1-9 is printed SERVO ENABLE; which line carries which servo signal is not settled."
                       if n in (37, 38, 44) else "No run saw a transition here, and non-observation is not proof of non-use.")
                    if is_aux else
                    "core_updateSw fabricates the paired power/hold states together from cabinet button " + str(82 if n <= 46 else 84) + " while 23 enables flippers; they are not independently wired CPU coils. The table's sLRFlipper callback (46) moves both the lower right and the upper right flipper, matching the shared right button; sLLFlipper (48) moves the lower left flipper."
                    if is_flip else
                    "No Frankenstein load or producer is present at this address: 24 has no Data East state producer, 33-36 have no core_getSol path, 49 is a simulator slot with no Frankenstein simulator, 50 is reserved, and 51-64 would need a custom solenoid count or getSol, which INITGAMES11 does not declare.")
            item = {"id": identifier, "label": label, "kind": "virtual", "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("solenoid", n), "availability": "used" if is_flip or n in (23, 37, 38, 44) else "unknown" if is_aux else "unused",
                    "provenance": prov(CORE, *([RUNTIME, SCRIPT] if is_flip else [RUNTIME, SCHEMATICS] if n in (37, 38, 44) else []), status="observed" if is_aux else "validated"),
                    "physical": {"notes": note}, "spatial": na("virtual" if is_aux or is_flip or n == 23 else "unused", CORE)}
            if n == 23:
                item["id"] = "virtual.game-on-enable"
                item["label"] = "Game On / Switched Solenoid Enable"
                item["physical"]["notes"] = "S11_GAMEONSOL = 23 is the PIA0 CB2 switched-solenoid enable and gates the synthetic flipper states; the ROM raises it during play and its coil tests. No physical coil is fitted at this public address."
                item["provenance"]["source_refs"].append(RUNTIME)
        outputs.append(item)

    for n in range(1, 65):
        label = LAMP_LABELS[n - 1]
        identifier = "lamp." + slug(label)
        col, row = (n - 1) // 8, (n - 1) % 8
        reading = rom.get(("lamp", n))
        unused = n in UNUSED_LAMPS
        note = f"Lamp matrix chart: {clause(lamp_chart[n])}. Location list: {clause(lamp_list[n])}."
        if reading:
            note += f" The ROM's SINGLE LAMP TEST prints {reading['name']}, {reading['drive_wire']} {reading['return_wire']} {reading['number']} and lights this address alone."
        physical = {"notes": note}
        if unused:
            physical["notes"] += " The chart and the location list print it Not Used and the ROM prints NOT USED; the lamp test's walk of every address explains its published state."
        else:
            physical["quantity"] = 1
            physical["notes"] += {
                13: " The lamp in the top turbo bumper cap.", 14: " The lamp in the middle left turbo bumper cap.",
                15: " The lamp in the middle right turbo bumper cap.", 16: " The lamp in the bottom turbo bumper cap.",
                29: " A bulb on the plastic at the Geneva (lower) scoop; the table draws it as a plastic bulb.",
                30: " A bulb on the plastic at the Sarcophagus (upper) scoop.",
                31: " One of three VUK entrance bulbs; the table draws it only as a Flasher sprite sharing another lamp's light, so no placement is recorded.",
                32: " One of three VUK entrance bulbs; the table draws it only as a Flasher sprite sharing another lamp's light, so no placement is recorded.",
                33: " The Alive lamp of the Kick Back: lit, a drain into the left outlane returns to play.",
                39: " The table also binds its lamp-40 insert l40 to this number (TimerInterval 39); only l39 is placed here.",
                40: " The table's insert l40 at this lamp's position carries TimerInterval 39, a table defect, so the table never lights it from 40. Its position is retained as this lamp's insert, not as a script binding.",
                48: " A bulb at the shooter lane.", 56: " The middle of the three VUK entrance bulbs.",
            }.get(n, "")
        item = {"id": identifier, "label": label, "kind": "lamp", "binding": {"group": "pinmame.output.lamp", "device": n},
                "aliases": aliases("lamp", n, f"{n:02d}"), "availability": "unused" if unused else "used", "physical": physical,
                "provenance": prov(MANUAL, CHART, SCHEMATICS, CORE, RUNTIME, *([] if unused or n in CABINET_LAMPS or n == 40 else [SCRIPT]))}
        if not unused:
            item["wiring"] = {"board": "CPU", "driver_transistor": lamp_drive[col][0], "drive_wire": lamp_drive[col][1],
                              "drive_connection": lamp_drive[col][2], "return_wire": lamp_return[row][1],
                              "return_connection": lamp_return[row][2], "return_component": lamp_return[row][0]}
        if unused:
            item["spatial"] = na("unused", MANUAL, RUNTIME)
        elif n in CABINET_LAMPS:
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif n == 40:
            item["spatial"] = spatial("lamp.40", identifier, "emitter", places, TABLE, GEOMETRY, MANUAL)
        elif (s := spatial(f"lamp.{n}", identifier, "emitter", places)):
            item["spatial"] = s
        outputs.append(item)

    sw = {x["binding"]["device"]: x["id"] for x in inputs if x["binding"]["group"] == "pinmame.input.switch"}
    sol = {x["binding"]["device"]: x["id"] for x in outputs if x["binding"]["group"] == "pinmame.output.solenoid"}
    mechanisms = []

    def mech(key, label, kind, act, sensors, behavior, refs=(MANUAL, SCRIPT, CORE, RUNTIME)):
        mechanisms.append({"id": "mech." + key, "label": label, "kind": kind, "actuators": [sol[n] for n in act],
                           "sensors": [sw[n] for n in sensors], "behavior": behavior, "provenance": prov(*refs)})

    mech("trough", "Six-ball trough and up-kicker", "kicker", [1, 2], [9, 10, 11, 12, 13, 14, 15],
         "Six balls rest on 9 (left) to 14 (right) in the trough under the metal arch. Output 1, the lock-out, releases the ball at 14 toward the up-kicker position 15 (the ROM's 6-BALL TROUGH #7 (VUK)); output 2, the Trough Up-Kicker, lifts it into shooter lane 16. In the harness the ROM fired 1 after Start, then 2 once 15 closed. The table models the trough as a cvpmBallStack (InitSw 0,14,13,12,11,10,9,0) kicked by BallLockout and a separate BallRelease kicker at 15.")
    mech("autolaunch", "Lever autolaunch (\"The Switch\")", "kicker", [3], [16, 62],
         "Shooter lane 16 feeds the Ball Auto Launch under the butyrate (output 3). The cabinet lever assembly \"The Switch\" (62) is connected with it: the skill shot is \"Throw The Switch to collect value highlighted in display\". In the harness the first pull of 62 with a ball at 16 fired 3; in the LASER KICK TEST a ball at 16 fired 3 without the lever.")
    mech("upper-scoop", "Sarcophagus upper scoop", "kicker", [5], [31],
         "A ball entering the upper scoop (with kick-big) closes 31 and output 5 kicks it out (observed in the harness gameplay run and the LASER KICK TEST).")
    mech("lower-scoop", "Geneva lower scoop", "kicker", [4], [32],
         "A ball entering the lower scoop (with kick-big) closes 32 and output 4 kicks it out (observed in the harness gameplay run and the LASER KICK TEST).")
    mech("ice-cave", "Ice Cave ball eject", "kicker", [6], [55],
         "The Ice Cave saucer at the upper left behind a 1-way gate: a ball closes 55 and output 6 ejects it (observed in the harness). The Ice Cave relights Alive.")
    mech("north-pole", "North Pole VUK and creature lock", "kicker", [7, 9, 12, 13], [53, 45, 46],
         "A ball at the North Pole closes 53 and output 7 lifts it to the upper level ramp, which carries trap doors to the creature's hands and continues as the wire ramp to the right return lane. Shooting the large ramp (45 entrance, 46 exit) lights lock; locks are made at the North Pole, and the creature \"CAN HOLD 1 BALL IN EACH HAND TO THROW\". Outputs 9 (right trap door) and 12 (left trap door) open the doors so a ball drops into a hand, and 13 swings both arms to throw the held balls. In the harness the ROM answered every 53 closure with 7; three ramp shots and VUK closures did not reach a lock, so the ROM's trap-door and throw sequence was not observed. The table opens trap 9 into the creature's left hand (player's right) and 12 into the right hand, and 13 throws both and closes the doors. Adjustment 51 set to NO disables the arms and the trap doors; Adjustment 52 sets the throw pulse.",
         refs=(MANUAL, SCHEMATICS, SCRIPT, CORE, RUNTIME))
    mech("diverter", "Right orbit ball diverter", "diverter", [14], [54, 35, 36],
         "Output 14 moves the diverter under the ramps at the right orbit. In the harness one spin of the Ingolstadt spinner 54 fired 14. The table makes its diverter ramp collidable while 14 is on.")
    mech("laser-kick", "Left outlane Laser Kick", "kicker", [16], [37],
         "When Alive is lit (lamp 33), left outlane switch 37 fires output 16, the kick back under the arch, returning the ball to play (observed in the harness gameplay run). The Ice Cave relights it. The LASER KICK TEST does not fire 16 for a closed 37 alone. Adjustment 47 starts each ball with Alive lit (MODERATE), carries it over (HARD) or starts it off (EXHARD); Adjustment 46 set to NO serves a machine without the coil, returning a lit-Alive drain to the shooter lane.")
    mech("bumpers", "Four turbo bumpers", "other", [17, 18, 19, 20], [41, 42, 43, 44],
         "Top, middle left, middle right and bottom switches 41-44 fire special-solenoid outputs 17-20 within milliseconds in the harness.")
    mech("slings", "Left and right slingshots", "other", [21, 22], [47, 48],
         "Left 47 and right 48 fire outputs 21 and 22 within milliseconds in the harness.")
    mech("player-flippers", "Cabinet-controlled flippers", "other", [45, 46, 47, 48], [82, 84],
         "Three flippers on the solid state 3-flipper board, all 23-1100: lower left, lower right and upper right. The left cabinet button enables the lower left flipper; the right button enables both right flippers. Only the lower flippers have E.O.S. switches; the upper flipper's is printed Not Used. PinMAME copies 82/84 to matrix 64/63 and fabricates 45/46 and 47/48 in pairs, so use one state per side. No CPU driver reaches the flipper board.")
    mech("knocker", "Cabinet knocker", "other", [8], [], "Output 8 pulses the knocker in the cabinet; it has no playfield sensor or placement.")
    mech("lighting-control", "PPB bank selection and G.I. control", "other", [10, 11], [],
         "Relay 10 on the PPB switches drives 1-8 between the coil loads 1L-8L and the flasher loads 1R-8R (25-32). Relay 11 on the power supply board switches the G.I. supply; the table's G.I. is lit while 11 is off.")
    mech("creature-head", "Creature head servo", "motorized", [], [],
         "A servo motor turns the creature's head. It hangs off the Monster Head Motion Board (PN. 520-5113-00), of whose four servo outputs only #1 is used. "
         "The CPU clocks 8-bit command words to that board serially at 125 BPS with a transition-sensitive clock (four clock pulses per word) and an active-high enable, on the board's CN1-2, CN1-3 and CN1-4; "
         "each word triggers a pre-recorded routine stored in the board's micro-controller, so the CPU never positions the head itself. "
         "The servo pulse lasts 0.3 to 1.7 ms, repeats every 16.3 ms and centres the head at 1 ms. At power-up the board blinks its LED a few times and holds the servo centred until it receives a command code. "
         "The Creature Head Motion Test sends the routines from the service menu, and the manual says the motion should be the same as in game play. "
         "In the harness, public outputs 37, 38 and 44 toggled at power-up in every run and around every command of that test, 44 rising before and falling after each burst while 37 and 38 toggled. "
         "That pattern fits an enable with a clock and data pair, but no retained drawing connects the servo board to the CPU lines PinMAME publishes there, so the mechanism names no actuator. "
         "The command codes and the routine each one plays are not documented, so PinMAME's state cannot yet be mapped to a head movement. No switch reports the head's position. "
         "The retained table animates the head from its own timers (AnimateFranksHead), not from any PinMAME output.",
         refs=(MANUAL, SCHEMATICS, SCRIPT, CORE, RUNTIME))
    relationships = flipper_column_relationships(flip_swno=(63, 64), matrix_ids={63: sw[63], 64: sw[64]}, refs=(CORE, RUNTIME))
    for n in range(25, 33):
        relationships.append({"id": f"relationship.mux-{n}", "kind": "relay_gated", "source": sol[10], "destination": sol[n], "provenance": prov(MANUAL, CORE, RUNTIME)})
    for s, o in ((41, 17), (42, 18), (43, 19), (44, 20), (47, 21), (48, 22)):
        relationships.append({"id": f"relationship.switch-{s}-coil-{o}", "kind": "pulse", "source": sw[s], "destination": sol[o], "provenance": prov(MANUAL, CORE, RUNTIME)})
    conflicts = []
    definition = {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {"id": KEY, "name": "Mary Shelley's Frankenstein", "manufacturer": "Sega", "year": 1995, "kind": "physical_pinball",
                    "model_number": "36", "ipdb_id": 947, "opdb_id": "GRB7E-MP3rR",
                    "playfield": {"width": 952, "height": 2080, "units": "vpx", "provenance": prov(TABLE, status="observed")}},
        "controller": {"platform": "pinmame.dataeast", "hardware_generation": "0x8000", "inversion_applied_by_emulator": True},
        "coverage": {"status": "partial", "missing": MISSING + (["unresolved_conflicts"] if unresolved_conflicts({"conflicts": conflicts}) else []),
                     "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "validated",
                                    "physical_wiring": "validated", "mechanisms": "observed", "variant_coverage": "validated",
                                    "recreation_knowledge": "validated", "runtime_observation": "observed", "causal_exercise": "observed",
                                    "spatial_placement": "observed"}},
        "drivers": [{"id": n, "description": label, "year": year, "manufacturer": "Sega", "flags": 0,
                     **({"clone_of": "frankst"} if n != "frankst" else {}), "physical_compatibility": "identical",
                     "variant_notes": "All three drivers use init_frankst / GEN_DEDMD64 / de_192x64DMD / FLIP6364 / SNDBRD_DE2S / S11_PRINTERLINE, the same CPU ROM franka.103 and the same sound ROMs; only the display ROMs differ (USA A1.03, German 1.01, Italian 1.03). The root's catalog year 1994 is the driver's date; the IPDB machine is dated 1995."}
                    for n, label, year in DRIVER_ROWS],
        "inputs": inputs, "outputs": outputs,
        "displays": [{"id": "display.main-dmd", "label": "Backbox 192 x 64 DMD", "kind": "dmd", "controller_index": 0, "width": 192, "height": 64,
                      "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", CORE, MANUAL), "provenance": prov(CORE, MANUAL, RUNTIME)}],
        "mechanisms": mechanisms, "relationships": relationships, "sources": build_sources(),
        "conflicts": conflicts, "knowledge": {"path": KNOWLEDGE_PATH.relative_to(ROOT).as_posix(), "status": "complete"},
    }
    return definition


def build_sources():
    places = load_json(PLACES_PATH)
    base = {"license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Sega Pinball, Inc.; hosted by IPDB"}
    machine = "Verified IPDB machine https://www.ipdb.org/machine.cgi?id=947 (Sega 'Mary Shelley's Frankenstein', model 36, January 1995, DataEast/Sega Version 3b). External manuals/by-machine/" + KEY + "."

    def ipdb(name):
        return {"kind": "manual", "uri": f"https://www.ipdb.org/files/947/{name}", "original_filename": name, "source_id": "IPDB 947",
                "sha256": MANUALS[name], "acquired_at": ACQUIRED}

    return [
        {"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{REV}/src/wpc/degames.c", "revision": REV,
         "locator": "degames.c 77-89 INITGAMES11/des11/FLIP6364 and Frankenstein block 1400-1437; s11.c pia2a_r 372, pia2b_w 392-412, setSSSol 537, updsol 558, pia0cb2_w 611, pia4b_w/pia4a_r 628/644 and the DataEast/Sega 3b PWM branch 1259-1269; s11.h DE_COMPORTS 30-44 and S11_GAMEONSOL 89; core.c core_updateSw 1793 and core_getSol 2456-2499; gen.h GEN_DEDMD64.",
         "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [checked_excerpt("controller.md", "pinned sources, exact symbols and public arithmetic")]},
        {"id": "pinmame.mary-shelley-s-frankenstein.catalog", "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REV,
         "locator": "PinmameGetGames and degames.c frankst root plus clones frankstg and franksti", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": MANUAL, **ipdb(MANUAL_NAME),
         "locator": machine + " Manual pages 1-66; PDF 10 playfield overview and instruction card (printed 6), PDF 30 game adjustments (printed 26), PDF 33 head motion and laser kick tests (printed 29), PDF 34-41 switch, lamp and coil tables, drawings and tests (printed 30-37).",
         **base, "excerpts": [
             checked_excerpt("switches.md", "PDF 34-35, printed 30-31, switch matrix chart and complete switch list"),
             checked_excerpt("lamps.md", "PDF 36-38, printed 32-34, lamp matrix chart, location list and lamp-test text"),
             checked_excerpt("coils.md", "PDF 38-41, printed 34-37, driver and flipper tables, location legend; schematics PDF 6-7 coil wiring"),
             checked_excerpt("mechanisms.md", "PDF 10, printed 6, playfield overview callouts and instruction card; PDF 30, printed 26, game adjustments 43-99; PDF 33, printed 29, head motion and laser kick tests")]},
        {"id": SCHEMATICS, **ipdb(SCHEMATICS_NAME),
         "locator": machine + " Schematics pages 67-93; PDF 4-9 cabinet, backbox, coil, special coil, switch and lamp wiring (printed 70-75), PDF 27 creature head servo board (printed 93).",
         **base, "excerpts": [
             checked_excerpt("matrix-sheets.md", "PDF 8-9, printed 74-75, switch and lamp wiring tables and connectors"),
             checked_excerpt("servo.md", "PDF 5 CPU CN1-CN3, PDF 27 servo board theory, PDF 4 shaker line"),
             checked_excerpt("coils.md", "PDF 6-7, printed 72-73, coil and flashlamp wiring and special coil diagram")]},
        {"id": CHART, **ipdb(CHART_NAME),
         "locator": "One-page Tech Chart 820-6104-06 (driver table, switch and lamp matrix charts, fuse lists); " + machine,
         **base, "excerpts": [checked_excerpt("tech-chart.md", "the whole chart, every cell")]},
        {"id": TABLE, "kind": "vpx_table", "uri": "external:vpx-sources/sega/mary-shelley-s-frankenstein-1995/Mary%20Shelley%27s%20Frankenstein%20%28Sega%201995%29%20v1.2.vpx",
         "sha256": places["table_sha256"], "known_working": True,
         "locator": "Mary Shelley's Frankenstein (Sega 1995) v1.2 by Schreibi34 and Herweh (table info version 1.0.2); 952 x 2080 VPX units; cGameName frankst; retained from the authorized local table library",
         "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Schreibi34 and Herweh", "acquired_at": "2026-11-13T14:18:00Z"},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:vpx-sources/sega/mary-shelley-s-frankenstein-1995/extracted-vpxtool/script.vbs",
         "sha256": places["script_sha256"], "known_working": True,
         "locator": "lines 158-232 library, controller and trough; 248-285 keys; 293-320 solenoid callbacks; 334-700 trough, flippers, slings, bumpers, switches, saucers and trap doors; 776-1070 creature arms, diverter, autolaunch and kickback; 1112-1203 lamps, G.I. and flashers",
         "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Schreibi34 and Herweh",
         "excerpts": [checked_excerpt("script-bindings.md", "machine-specific I/O bindings, mechanisms and table defects, summarized factually")]},
        {"id": EXTRACTION, "kind": "vpx_table", "uri": "external:vpx-sources/sega/mary-shelley-s-frankenstein-1995/extracted-vpxtool/manifest.json",
         "sha256": places["manifest_sha256"],
         "locator": "vpxtool git:v0.33.3; 888 payload files / 179,073,322 bytes; tools/build_external_evidence_manifest.py --game frankst sorts relative POSIX paths, records size/SHA256, canonical JSON plus LF; manifest files excluded from their own payload",
         "license": "NOASSERTION", "attribution": "Schreibi34 and Herweh; extraction by project contributors"},
        {"id": GEOMETRY, "kind": "human_review", "uri": "internal:tools/frankenstein_places.json", "sha256": sha(PLACES_PATH),
         "locator": "build_frankenstein_places.py: script-linked object selection, stored centres and wall/ramp drag-point means; one recreation lineage, all positions observed; rejected helpers and omitted devices are listed.",
         "license": "NOASSERTION", "attribution": "Primary curator; table geometry by the retained table's authors"},
        {"id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI, "sha256": VPM_DE_SHA256,
         "locator": "de.vbs lines 20-36 and vpmKeyDown/vpmKeyUp 66-114; retained machine-neutral library loaded by LoadVPM at script line 171",
         "license": "NOASSERTION", "attribution": "VPinMAME script-library maintainers", "excerpts": [checked_excerpt("controller.md", "de.vbs constants and key handlers")]},
        {"id": RUNTIME, "kind": "runtime_scenario", "uri": "internal:" + RUNTIME_PATH.relative_to(ROOT).as_posix(), "sha256": sha(RUNTIME_PATH), "revision": REV,
         "locator": "Fresh-state frankst (USA CPU 1.03, display A1.03) ACTIVE SWITCH, SINGLE LAMP, COIL, CYCLING, SERVO and LASER KICK tests and a gameplay run; visually read DMD frames pinned to pixel digests in tools/seeds/sega/mary-shelley-s-frankenstein-1995-runtime-readings.json; raw runs, frames and NVRAM external under review-artifacts/" + KEY + "/final.",
         "license": "NOASSERTION", "attribution": "Primary curator; user-authorized existing ROM"},
    ]


def verify_external():
    if manual_root := os.environ.get("PINMAME_MANUALS_ROOT"):
        for filename, digest in MANUALS.items():
            path = Path(manual_root) / "by-machine" / KEY / filename
            if not path.is_file() or sha(path) != digest:
                raise ValueError(f"Frankenstein retained manual missing or changed: {path}")
    vpx_root = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if review_root := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        from build_frankenstein_runtime import build as build_runtime

        if build_runtime(Path(review_root)) != load_json(RUNTIME_PATH):
            raise ValueError("Frankenstein runtime evidence differs from the retained runs")
    if vpx_root:
        from build_frankenstein_places import build as build_places

        # This builder verifies the VPX/script identities and extraction manifest itself.
        if build_places(Path(vpx_root)) != load_json(PLACES_PATH):
            raise ValueError("Frankenstein placements differ from the retained extraction")


def artifacts():
    definition = build()
    places = load_json(PLACES_PATH)
    count = sum(len(d.get("spatial", {}).get("placements", [])) for group in ("inputs", "outputs") for d in definition[group])
    absent = [d["id"] for group in ("inputs", "outputs") for d in definition[group] if d.get("availability") in ("used", "unknown") and "spatial" not in d]
    report = {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": KEY, "status": "partial",
        "coordinate_convention": "x=0 left, x=1 right; y=0 rear, y=1 apron; x=raw_x/952, y=raw_y/2080. Six decimal places preserve deterministic table precision, not survey accuracy.",
        "placement_count": count,
        "source": {"table_sha256": places["table_sha256"], "extraction_manifest_sha256": places["manifest_sha256"]},
        "placements": places["placements"], "omitted_spatial_key_devices": absent,
        "blockers": [
            {"id": "single-recreation-lineage", "severity": "major", "detail": "All table coordinates come from one recreation (Schreibi34 and Herweh's v1.2). No factory location drawing has been checked against them: the manual's coil, flash lamp and lamp location drawings exist but were not measured, so every placement stays observed."},
            {"id": "missing-trough-and-vuk-entrance-geometry", "severity": "major", "detail": places["omitted"]},
            {"id": "gi-socket-survey", "severity": "major", "detail": "The table supplies 22 G.I. lights under output 11, but the manual gives no complete G.I. socket list or string allocation; the physical G.I. total is not asserted."},
            {"id": "flasher-insert-sockets", "severity": "minor", "detail": "Flasher placements are the table's playfield flash-lamp lights, one per socket; the driver table's backbox insert sockets have no playfield position."},
        ],
        "projection_notes": {
            "solenoid.13": "The two creature-hand kickers stand for the arms the coil swings, not for the coil under the creature.",
            "solenoid.14": "Mean of the diverter ramp's drag points: the diverter the coil moves, not the coil under the ramps.",
            "solenoid.9": "The trap-door trigger in the upper level ramp, not the coil.",
            "solenoid.12": "The trap-door trigger in the upper level ramp, not the coil.",
            "lamp.40": "l40 sits at lamp 40's insert; the table binds it to 39 by TimerInterval.",
        },
        "rejected": places["rejected"],
        "mechanical_anchors": places["mechanical_anchors"],
    }
    knowledge = (ROOT / "tools/frankenstein_knowledge.md").read_bytes()
    return [(DEFINITION_PATH, canonical_bytes(definition)), (SEED_PATH, canonical_bytes(definition)),
            (KNOWLEDGE_PATH, knowledge), (SPATIAL_REPORT_PATH, canonical_bytes(report))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--regenerate", action="store_true")
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    verify_external()
    existing = root / f"machines/author-ready/sega/{SLUG}.json"
    if existing.exists():
        raise ValueError(f"refusing to overwrite an existing author-ready Frankenstein artifact: {existing}")
    for path, payload in artifacts():
        target = root / path.relative_to(ROOT)
        if args.check:
            if not target.is_file() or target.read_bytes().replace(b"\r\n", b"\n") != payload.replace(b"\r\n", b"\n"):
                raise ValueError(f"Frankenstein artifact missing or drifted: {target}")
        else:
            write_bytes(target, payload)
    print("Frankenstein definition, seed, knowledge and spatial report match the curator." if args.check else "Regenerated Frankenstein definition, seed, knowledge and spatial report.")


if __name__ == "__main__":
    main()
