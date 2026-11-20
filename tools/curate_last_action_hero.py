"""Curate the physical Data East Last Action Hero (1993) machine definition.

Side-effect free and deterministic. The printed tables are parsed from the hand-transcribed excerpts committed
under ``evidence/excerpts/data-east.last-action-hero.1993/`` (``lah_manual``), the semantic naming is in
``lah_semantics``, the normalized coordinates resolved from the retained recreation are in
``tools/last_action_hero_places.json`` (``tools/build_lah_places.py``), the ROM's own service-test readings are in
``tools/last_action_hero_runtime.json`` (``tools/build_lah_runtime_evidence.py``), and the ROM inventory is parsed
from pinned PinMAME and embedded below. ``--regenerate`` reproduces the canonical artifacts byte-for-byte without
reading any external evidence root; ``--check`` refuses drift. ``--write-extraction-manifest`` and
``--verify-extraction`` write and verify the canonical manifest of the retained vpxtool extraction under
PINMAME_VPX_SOURCES_ROOT.

The definition, its pinned seed, the spatial report and the knowledge note are all generated here from the same
objects, so prose cannot outlive the data behind it.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_bytes, write_json, write_text
from pinmame_flipper_column import (
    VPM_CORE_SHA256,
    VPM_DE_LIBRARY_SOURCE,
    VPM_DE_LIBRARY_URI,
    VPM_DE_SHA256,
    flipper_column_inputs,
    flipper_column_relationships,
    vpm_staged_flipper_notes,
)
import lah_manual
import lah_semantics as sem

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.last-action-hero.1993"
SLUG = "last-action-hero-1993"
DEFINITION_PATH = ROOT / f"machines/partial/data-east/{SLUG}.json"
AUTHOR_READY_PATH = ROOT / f"machines/author-ready/data-east/{SLUG}.json"
SEED_PATH = ROOT / f"tools/seeds/data-east/{SLUG}.json"
SPATIAL_REPORT_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.json"
SPATIAL_REPORT_MARKDOWN_PATH = ROOT / f"reports/spatial/data-east/{SLUG}.md"
KNOWLEDGE_PATH = ROOT / f"knowledge/data-east/{SLUG}.md"
PLACES_PATH = ROOT / "tools/last_action_hero_places.json"
RUNTIME_PATH = ROOT / "tools/last_action_hero_runtime.json"
RUNTIME_EVIDENCE_PATH = ROOT / "evidence/runtime/data-east/last-action-hero-lah_112-service-tests.json"
KNOWLEDGE_TEMPLATE = ROOT / "tools/last_action_hero_knowledge.md"
EXCERPT_DIR = ROOT / "evidence/excerpts" / KEY

REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SHORT = REVISION[:12]
MANUAL = f"manual.{KEY}"
SCHEMATICS = f"manual.{KEY}.schematics"
IPDB = f"ipdb.{KEY}"
CATALOG = f"pinmame.catalog.{SHORT}"
CORE = f"pinmame.core.{SHORT}"
CORE_H = f"pinmame.core-h.{SHORT}"
CORE_C = f"pinmame.core-c.{SHORT}"
S11_C = f"pinmame.s11-c.{SHORT}"
S11_H = f"pinmame.s11-h.{SHORT}"
TABLE = "vpx-table.last-action-hero-vpw-1-1"
SCRIPT_REF = "vpx-script.last-action-hero-vpw-1-1"
EXTRACTION = "vpx-extraction.last-action-hero-vpw-1-1"
RUNTIME_SRC = "runtime.last-action-hero.lah-112-service-tests"
LEGACY = "legacy.game.lah"

MANUAL_NAME = "Data_East_1993_Last_Action_Hero_Manual.pdf"
MANUAL_SHA256 = "546f0272d7d2a4334224843fc1498077c45896cb8c492daa569ac07d3161c61d"
MANUAL_URL = f"https://web.archive.org/web/20240804185608id_/https://www.ipdb.org/files/1416/{MANUAL_NAME}"
SCHEMATICS_NAME = "Data_East_1993_Last_Action_Hero_Schematics_BW.pdf"
SCHEMATICS_SHA256 = "7925654b30802ba7246efdddcebb90cba62cffd39ad36945124d005fec30d702"
SCHEMATICS_URL = f"https://web.archive.org/web/20240804185607id_/https://www.ipdb.org/files/1416/{SCHEMATICS_NAME}"
MANUAL_ACQUIRED = "2026-11-20T08:28:25Z"
IPDB_CAPTURE = "https://web.archive.org/web/20250125011738id_/https://www.ipdb.org/machine.cgi?id=1416"
IPDB_SHA256 = "7a82ff0f474af0f7a1e7758fea4b021e388e6dfce24fb8a65a14268e7c9eb672"
IPDB_ACQUIRED = "2026-11-20T08:28:25Z"
TABLE_NAME = "Last Action Hero (Data East 1993) VPW v1.1.vpx"
TABLE_SHA256 = "0a1e3fcfc652086003106fb22290ec54166dd5121f8d405f4a3cd2389d59b173"
TABLE_ACQUIRED = "2026-11-20T08:30:04Z"
SCRIPT_SHA256 = "1038027da4bdabe7a447d96df6eb79bb3830b2af18a17330d709feb4eaa139e5"
EXTRACTION_ACQUIRED = "2026-11-20T08:30:10Z"
TABLE_ATTRIBUTION = (
    "VPW Film Crew (Tomate, Apophis, Sixtoe, Flux, Leojreimroc), based on previous work by javier1515, ninuzzu, knorr and dark"
)

SOURCE_DIRECTORY = "data-east/last-action-hero-1993/vpw-1.1"
EXTRACTION_RELATIVE_PATH = Path(SOURCE_DIRECTORY) / "extracted-vpxtool"
EXTRACTION_MANIFEST_RELATIVE_PATH = Path(SOURCE_DIRECTORY) / "extracted-vpxtool.manifest.json"
EXTRACTION_MANIFEST_SHA256 = "0a3fcdbabc4d9b1076e9be0a1117c996b06b7a42421a6cd024fd2b27149faca8"
EXTRACTION_FILE_COUNT = 2652
EXTRACTION_TOTAL_BYTES = 1996442982
VPXTOOL_VERSION = "vpxtool git:v0.33.3"
# The world-space export the placement builder's MESH_BOUNDS come from (tools/build_lah_places.py --world-obj).
WORLD_OBJ_SHA256 = "3213fbabb085338dd19d06179a899baedd82be4c35228f7a6cf46cd938ffa6b7"
WORLD_OBJ_URI = f"external:pinmame-vpx-sources/{SOURCE_DIRECTORY}/world-obj/Last Action Hero (Data East 1993) VPW v1.1.obj"
PIN_FILE_SHA256 = {
    "degames.c": "223623584396cc530c8baef577772d4b96d39784aa2624f04746871c8f89f5d8",
    "core.h": "b6c03b20a09fbadff1ce16f9f1cfc9e5bace08857cb998b92d8f304695ec97c0",
    "core.c": "38a4418adba7f2ef408e8f92bfcf3e5ab950c45164cb69461460af3747386c00",
    "s11.c": "03784af9fe444b3da56f72192a5b04da1aa72938435f3d902d94ab47c0f8bd9e",
    "s11.h": "743b0836cc84e41e793d65786a964a595fb403c4fdba29b2961e8a36a937f614",
}

# The nine PinMAME drivers, parsed from src/wpc/degames.c at the pinned revision (lines 1027-1102). Roles: CPU,
# display, then the three sound ROMs (U7, U17, U21). All nine share lahGameData and every sound ROM.
ROLES = ("CPU", "display", "sound U7", "sound U17", "sound U21")
SOUND = ["lahsnd.u7", "lahsnd.u17", "lahsnd.u21"]
ROM_SETS = {
    "lah_112": ["lahcpua.112", "lahdispa.106", *SOUND],
    "lah_f104": ["lahcpua.104", "lahdispf.101", *SOUND],
    "lah_l104": ["lahcpua.104", "lahdispl.102", *SOUND],
    "lah_c106": ["lahcpuc.106", "lahdispa.104", *SOUND],
    "lah_107": ["lahcpua.107", "lahdispa.104", *SOUND],
    "lah_l108": ["lahcpua.108", "lahdispl.104", *SOUND],
    "lah_l108_105": ["lahcpua.108", "lahdispl.105", *SOUND],
    "lah_110": ["lahcpua.110", "lahdispa.106", *SOUND],
    "lah_113": ["lahcpua.113", "lahdispa.106", *SOUND],
}
ROOT_DRIVER = "lah_112"
DRIVER_LABELS = {
    "lah_112": "Last Action Hero (1.12)",
    "lah_f104": "Last Action Hero (1.04 French)",
    "lah_l104": "Last Action Hero (1.04 Spanish)",
    "lah_c106": "Last Action Hero (1.06 Canadian)",
    "lah_107": "Last Action Hero (1.07)",
    "lah_l108": "Last Action Hero (1.08 Spanish, Display 1.04)",
    "lah_l108_105": "Last Action Hero (1.08 Spanish, Display 1.05)",
    "lah_110": "Last Action Hero (1.10)",
    "lah_113": "Last Action Hero (1.13 unofficial MOD)",
}
DRIVER_YEARS = {driver: ("2014" if driver == "lah_113" else "1993") for driver in ROM_SETS}

SW = lah_manual.switch_data()
LAMP = lah_manual.lamp_data()
COIL = lah_manual.coil_data()
SCHEM = lah_manual.schematic_data()
PARTS = lah_manual.parts_data()
ASSEMBLIES = PARTS["assemblies"]
SHEET_ASM = SCHEM["assemblies"]
CABINET = PARTS["cabinet"]
PLACES = load_json(PLACES_PATH)
FACTS = load_json(RUNTIME_PATH)
EVIDENCE = load_json(RUNTIME_EVIDENCE_PATH)
RUNS = EVIDENCE["runtime"]["observations"]["runs"]
ROM_SWITCH = FACTS["rom_switch_names"]
ROM_LAMP = FACTS["rom_lamp_names"]
ROM_COIL = {int(address): entry["name"] for address, entry in FACTS["rom_coil_names"].items()}
CYCLE = RUNS["cycling-coils"]["ordered_solenoid_on_sequence"]
CYCLE_STEPS = [address for address in CYCLE if address != 10]
TEST = {entry["label"]: entry for entry in FACTS["test_actions"]}
SERVE = {entry["label"]: entry for entry in FACTS["trough_serve"]}
SERVE_ORDER = RUNS["trough-serve"]["ordered_solenoid_on_sequence"]
MAGNET_ORDER = FACTS["magnet_test_on_sequence"]
LEGACY_GAME_SHA256 = "bc32a20c97f2a769590b39bb51c8af45b9e6e0289a8b7557e5f4867e8872ce9e"
if hashlib.sha256((ROOT / "games/lah.json").read_bytes()).hexdigest() != LEGACY_GAME_SHA256:
    raise SystemExit("games/lah.json no longer matches the legacy bytes this record's compatibility aliases were generated from")
LEGACY_GAME = load_json(ROOT / "games/lah.json")

if PLACES.get("table_bounds") != {"width": 952.0, "height": 2162.0}:
    raise SystemExit(f"tools/last_action_hero_places.json must carry the retained table's 952 x 2162 bounds, not {PLACES.get('table_bounds')}")
if RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix() != FACTS["source"]:
    raise SystemExit("tools/last_action_hero_runtime.json must name the committed runtime evidence bundle")
if sorted(CYCLE_STEPS) != [*range(1, 10), *range(11, 23), *range(25, 33)] or len(CYCLE_STEPS) != 29:
    raise SystemExit(f"the Cycling Coils run must fire 1-9, 11-22 and 25-32 once each, not {CYCLE_STEPS}")
if MAGNET_ORDER[:3] != [38, 37, 39] or any(MAGNET_ORDER[i] != MAGNET_ORDER[i % 3] for i in range(len(MAGNET_ORDER))):
    raise SystemExit(f"the Magnet Test must cycle 38, 37, 39 in turn, not {MAGNET_ORDER}")
for _address in [*range(1, 10), *range(11, 23), *range(25, 33)]:
    if _address not in ROM_COIL:
        raise SystemExit(f"the Cycling Coils frames name nothing at public {_address}")


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
LEGACY_COIL_NAMES = {int(item["id"]): item["alias"] for item in LEGACY_GAME["aliases"] if item["type"] == "coil"}


def aliases(namespace: str, address: int, legacy_kind: str | None = None, legacy: set[int] = frozenset(), *, extra=()) -> list[dict]:
    values = [{"namespace": namespace, "value": str(address)}]
    if legacy_kind and address in legacy:
        values += [{"namespace": f"vpe-legacy.{legacy_kind}", "value": value} for value in legacy_numbers(address)]
    values += [{"namespace": ns, "value": value} for ns, value in extra]
    return values


def wire(text: str) -> str:
    """A printed wire colour pair in the record's spelling: hyphenated, with ORN for the print's ORG."""
    return text.replace("/", "-").replace("ORG", "ORN")


def wire_note(printed: str, what: str) -> str | None:
    if wire(printed) == printed:
        return None
    changes = [change for found, change in (("/", "hyphenated"), ("ORG", "ORN for the print's ORG")) if found in printed]
    return f"The print spells {what} '{printed}'; it is recorded as {wire(printed)} ({', '.join(changes)})."


PLACE_REFS = [TABLE, SCRIPT_REF, EXTRACTION]


def spatial_for(device_id: str, role: str, key: str, *, status: str = "observed", extra_refs=()) -> dict | None:
    hits = PLACES["placements"].get(key)
    if not hits:
        return None
    hits = sorted(hits, key=lambda hit: (hit["x"], hit["y"]))
    placements = []
    for index, hit in enumerate(hits, start=1):
        suffix = "" if len(hits) == 1 else f".{index}"
        placements.append({
            "id": f"{device_id}.{role}{suffix}", "role": role, "space": "playfield",
            "x": hit["x"], "y": hit["y"], "provenance": prov(status, PLACE_REFS + list(extra_refs)),
        })
    return {"status": status, "placements": placements}


ORIGIN_TEXT = {
    "measured-center": "",
    "computed-centroid": " at the centroid of its drag points",
    "mesh-bounds-center": " at its world-space mesh-bounds centre",
    "primitive-pivot": " at its rotation axis",
}


def placed_objects(key: str) -> str:
    hits = sorted(PLACES["placements"].get(key, []), key=lambda hit: (hit["x"], hit["y"]))
    return ", ".join(f"{hit['object_type']} {hit['object']}{ORIGIN_TEXT[hit['coordinate_origin']]}" for hit in hits)


def unplaced_reason(key: str) -> str:
    reasons = [entry["reason"] for entry in PLACES["unplaced"] if entry["key"] == key]
    if len(reasons) != 1:
        raise SystemExit(f"tools/last_action_hero_places.json must give exactly one unplaced reason for {key}")
    return reasons[0]


def counted(number: int, noun: str) -> str:
    words = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four"}
    return f"{words[number]} {noun}{'' if number == 1 or number == 0 else 's'}"


def asm(item: str) -> str:
    return ASSEMBLIES[item]["Part No."]


def counts(label: str, table: dict) -> dict[int, int]:
    entry = table[label]
    return {int(address): count for address, count in entry.get("on_counts", entry.get("solenoid_on_counts", {})).items()}


inputs: list[dict] = []
outputs: list[dict] = []

# --- Inputs: the 8 x 8 switch matrix -----------------------------------------------------------------------------
FLIP_SWNO = (63, 64)
PART_DISAGREEMENTS = {
    address for address in range(1, 65)
    if SCHEM["switches"][address]["Part No."] != SW["parts"][address]["part_printed"]
}
if PART_DISAGREEMENTS != {32, 40, 48, 56, 57, 60, 61, 62}:
    raise SystemExit(f"the switch part tables must disagree exactly where the excerpt says, not at {sorted(PART_DISAGREEMENTS)}")
_RIGHT_LEAF = CABINET["15a"]
if (CABINET["15"]["Part No."], _RIGHT_LEAF["Part No."]) != ("180-5048-01", "180-5122-00"):
    raise SystemExit("the cabinet parts list must print the left and right flipper leaf switches 180-5048-01 and 180-5122-00")
NO_PART = PART_DISAGREEMENTS | {64}


def trigger_lines(address: int, first: int) -> str:
    return f"The retained table sets and clears it from its Sw{address} trigger (script lines {first}-{first + 1})."


SCRIPT_SWITCH_NOTES = {
    1: "The retained table names it its nudge tilt switch (vpmNudge.TiltSwitch = 1, script line 170).",
    8: "The retained table writes it from the plunger key (Table1_KeyDown/Table1_KeyUp, script lines 341 and 357).",
    15: (
        "The retained table never writes it from its sw15 kicker's own events: SolTrough sets it when it kicks the ball from its sw14 kicker into sw15, and SolRelease "
        "clears it when it kicks sw15 into the shooter lane (script lines 1108-1121)."
    ),
    16: "The retained table sets and clears it from its sw16 trigger (script lines 994-995); its cvpmImpulseP plunger names the same switch (.Switch 16, line 1133).",
    22: "The retained table sets and clears it from its sw22 trigger (Sw22_Hit/Sw22_UnHit, script lines 554-565).",
    23: "The retained table sets and clears it from its sw23 trigger (Sw23_Hit/Sw23_UnHit, script lines 567-575).",
    31: "The retained table adds the ball to its bsRScoop saucer on the sw31 kicker (InitSaucer sw31, 31, script line 178; sw31_Hit, line 1021).",
    32: "The retained table reports it through STHit 32 from its Sw32 stand-up target (script line 1024).",
    33: "The retained table pulses it from its Bumper1, the left of the two upper bumpers (Bumper1_Hit, script lines 935-936).",
    34: "The retained table pulses it from its Bumper3, the lowest of the three bumpers (Bumper3_Hit, script lines 947-948).",
    35: "The retained table pulses it from its Bumper2, the right of the two upper bumpers (Bumper2_Hit, script lines 941-942).",
    36: "The retained table pulses it from its LeftSlingshot wall (LeftSlingShot_Slingshot, script lines 788-790).",
    37: "The retained table pulses it from its RightSlingshot wall (RightSlingShot_Slingshot, script lines 813-815).",
    40: "The retained table reports it through STHit 40 from its Sw40 stand-up target (script line 1032).",
    46: "The retained table sets and clears it from its Sw46 trigger at the low end of its left ramp (script lines 1046-1047).",
    47: "The retained table adds the ball to its bsVuk saucer on the Sw47 kicker (InitSaucer sw47, 47, script line 187; Sw47_hit, line 1050).",
    48: "The retained table pulses it from its Sw48 kicker (Sw48_Hit, script line 1052).",
    54: "The retained table pulses it from its sw54 target beside its drop-target bank (Sw54_Hit, script line 1055).",
    56: "The retained table reports it through STHit 56 from its Sw56 stand-up target (script line 1060).",
    57: "The retained table adds the ball to its bsMLScoop saucer on the Sw57 kicker (InitSaucer sw57, 57, script line 195; sw57_Hit, line 1062).",
    58: "The retained table pulses it from its sw58 trigger, which it comments as the centre right subway switch (Sw58_Hit, script lines 1065-1066).",
    59: "The retained table pulses it from its Sw59 spinner (Sw59_Spin, script line 1069).",
    60: (
        "The retained table has no object for the crane limit switches: its CraneTimer sets 60 in CraneIsLeft when the boom reaches the left end of its sweep and clears "
        "it everywhere else (script lines 653-717)."
    ),
    61: (
        "The retained table has no object for the crane limit switches: its CraneTimer sets 61 in CraneIsRight when the boom reaches the right end of its sweep and clears "
        "it everywhere else (script lines 653-717)."
    ),
    62: (
        "The retained table writes it from both its plunger key and its lock-bar key (script lines 342, 346, 355 and 358), so its plunger key also presses Smart Missile."
    ),
}
for _address in range(9, 15):
    _first = 1076 + 2 * (14 - _address)
    SCRIPT_SWITCH_NOTES[_address] = f"The retained table sets and clears it from its trough kicker sw{_address} (script lines {_first}-{_first + 1})."
for _address in range(17, 22):
    SCRIPT_SWITCH_NOTES[_address] = f"The retained table reports it through DTHit {_address} from its sw{_address} drop-target wall (script line {981 + _address})."
for _address, _first in ((24, 1007), (28, 1014), (29, 1016), (30, 1018), (38, 1027), (39, 1029), (41, 1034), (42, 1036), (43, 1038), (44, 1040), (45, 1043), (55, 1057)):
    SCRIPT_SWITCH_NOTES[_address] = trigger_lines(_address, _first)
for _address in (25, 26, 27):
    SCRIPT_SWITCH_NOTES[_address] = f"The retained table reports it through STHit {_address} from its Sw{_address} stand-up target (script line {985 + _address})."

SWITCH_EXTRA_NOTES = {
    2: "Pinned PinMAME's shared DE_COMPORTS labels this position 'Ball Tilt', a generic platform label; this machine's chart, parts table and ROM print '4th Coin'.",
    3: "DE_COMPORTS binds PinMAME's Start input (IPT_START1) to this position; the chart names it Credit Button.",
    8: (
        "The ROM names it LAUNCH BUTTON. The Cabinet Parts Illustration's item 1 is the Shooter Gun Assy. (500-5731-00) at the front of the cabinet's right side, beside "
        "item 11 (Side Armor-Right), and the Major Assemblies drawing puts the Ball Launch Assy at the foot of the right shooter lane; the switch table's part "
        "180-5111-00 is the trigger contact."
    ),
    15: "The parts table types the release position 180-5118-00 where it prints 180-5119-00 for trough positions 9-14.",
    17: "The ROM names it DROP TARGET C BOTTOM: C is the lowest target of the five-bank.",
    21: "The ROM names it DROP TARGET E TOP: E is the highest target of the five-bank.",
    34: (
        "The switch chart calls it the Bottom Turbo Bumper, the coil table calls its coil 18 the Center Turbo Bumper and the lamp chart calls its lamp 7 the Top Turbo Bumper; "
        "the ROM names all three BOTTOM. It is the third bumper, below the left (33) and right (35) ones."
    ),
    54: (
        "The parts table prints 'Drop Target Bar (2)' (part 180-5129-00) and the ROM DROP TARGET BAR X2. The manual's rule text (printed page 4) calls it the "
        "DANGER bar: 'hitting the DANGER bar behind the drop targets will reset the drop target bank'. No retained page draws the bar, and no retained run closed 54 "
        "in a game."
    ),
    62: (
        "The parts table's part 180-0028-00 is the Cabinet Parts Illustration's item 14 Push Button Switch, and IPDB lists a Smart Missile button that awards the current "
        "award when pressed. The ROM's Crane Test fired nothing when 62 closed."
    ),
}

for address in range(1, 65):
    chart = SW["chart"][address]
    part = SW["parts"][address]
    sheet = SCHEM["switches"][address]
    unused = address in sem.UNUSED_SWITCHES
    suffix, label = (f"unused-{address}", f"Unused Switch {address}") if unused else sem.SWITCHES[address]
    device_id = f"switch.{suffix}"
    notes = [f"Printed switch-matrix column {chart['column']}, row {chart['row']}; the chart prints '{chart['printed']}'."]
    if unused:
        notes.append(
            f"The Switch Part Numbers table prints '{part['description']}' with the part cell '{part['part_printed']}': the address is strobed but carries no device."
        )
    else:
        notes.append(
            f"The Switch Part Numbers table prints '{part['description']}'"
            + (f", part {part['part_printed']}." if part["part"] else f", with the part cell printed '{part['part_printed']}'.")
        )
    if sheet["Description"] != part["description"]:
        notes.append(f"The schematic book's Playfield Switch Wiring Diagram prints the name '{sheet['Description']}'.")
    if address in PART_DISAGREEMENTS:
        notes.append(
            f"The schematic book's Playfield Switch Wiring Diagram prints the part '{sheet['Part No.']}' where the operator manual's table prints '{part['part_printed']}'; "
            "nothing retained settles which is right, so no part number is recorded."
        )
    if part["cabinet"]:
        notes.append(
            "The table marks the address with an asterisk; it prints no legend, but the asterisk marks exactly 01-08 and the location drawing has no callout for any of them, "
            "which reads as the cabinet marking."
        )
    if address in SWITCH_EXTRA_NOTES:
        notes.append(SWITCH_EXTRA_NOTES[address])
    if address in SCRIPT_SWITCH_NOTES:
        notes.append(SCRIPT_SWITCH_NOTES[address])
    rom = ROM_SWITCH[str(address)]
    entry: dict[str, Any] = {
        "id": device_id,
        "label": label,
        "kind": "switch",
        "binding": {"group": "pinmame.input.switch", "device": address},
        "aliases": aliases("pinmame.switch", address, "switch", LEGACY_SWITCHES),
        "availability": "unused" if unused else "used",
        "provenance": prov(
            "validated",
            [MANUAL, SCHEMATICS, CORE_H, RUNTIME_SRC] + ([] if unused or address in (2, 3, 4, 5, 6, 7) or address in FLIP_SWNO else [SCRIPT_REF]),
        ),
        "physical": {"notes": ""},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": chart["drive"]["wire"],
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
        },
    }
    if address in FLIP_SWNO:
        side = "left" if address == 63 else "right"
        button = 84 if address == 63 else 82
        notes.append(
            f"Both names denote what PinMAME publishes here, the {side} cabinet "
            f"flipper button: the game data declares FLIP6364 = FLIP_SWNO(63,64) with no FLIP_SOL, so PinMAME models no end-of-stroke switch on this machine, and core.c's "
            f"core_updateSw rewrites this switch on every update from PinMAME's flipper-column button bit {button}. A consumer drives {button}, not {address}. The retained "
            f"table never writes {address}; it hands the {side} flipper key to de.vbs, which writes {button} (excerpt vpm-script-library-flippers)."
        )
        if address == 64:
            notes.append(
                f"The switch table and the schematic sheet print part 180-5048-01 for both flipper buttons, while the Cabinet Parts Illustration prints item 15 'Left Flipper "
                f"Leaf Switch' 180-5048-01 and item 15a '{_RIGHT_LEAF['Description'].rstrip(' *')}' {_RIGHT_LEAF['Part No.']} (asterisked, not shown in the drawing); the "
                "right button's part number is not settled, so none is recorded."
            )
        notes.append(
            f"ROM evidence (1.12 Active Switch Test): a host write of 1 to public {address} showed '{rom['name']}', wires {rom['wires']} and '#{address}' but fired no flipper "
            f"output, while holding {button} showed the same frame and fired {'47/48' if side == 'left' else '45/46'}; with every matrix and flipper input at 0, and "
            "the Green service input -6 held at 1 throughout the test, the screen shows NONE."
        )
        entry["roles"] = [f"flipper.lower.{side}.matrix-copy"]
    else:
        notes.append(
            f"ROM evidence (1.12 Active Switch Test): holding public {address} at 1 shows '{rom['name']}', wires {rom['wires']} and '#{address:02d}'; "
            "with every matrix and flipper input at 0, and the Green service input -6 held at 1 throughout the test, the same screen shows NONE, so the ROM treats "
            "public 1 as the closed contact"
            + (" and names the address NOT USED." if unused else ".")
        )
    if not unused:
        entry["normally_closed"] = False
        notes.append("Contact: the switch-matrix chart shades no cell and marks no opto or normally closed position, so the fitted contact rests open.")
    entry["physical"]["notes"] = " ".join(notes)
    if part["part"] and address not in NO_PART:
        entry["physical"]["part_number"] = part["part"]
    if address in sem.SWITCH_TYPES:
        entry["physical"]["switch_type"] = sem.SWITCH_TYPES[address]
    if address in sem.CABINET_ROLES:
        entry["roles"] = [sem.CABINET_ROLES[address]]
    if unused:
        entry["spatial"] = not_applicable("unused", [MANUAL])
    elif address in sem.CABINET_ROLES or address in FLIP_SWNO:
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, CORE_H] if address in FLIP_SWNO else [MANUAL])
    else:
        located = spatial_for(device_id, "sensor", f"switch.{address}")
        if address in (60, 61):
            if located:
                raise SystemExit(f"switch {address}: the crane limits have no script-bound object, so the placement builder must leave them unplaced")
            entry["physical"]["notes"] += f" Not placed: {unplaced_reason(f'switch.{address}').split(': ', 1)[1]}."
        else:
            if not located:
                raise SystemExit(f"switch {address} is a playfield switch with no retained placement")
            entry["spatial"] = located
            entry["physical"]["notes"] += f" Placed on the retained table's {placed_objects(f'switch.{address}')}."
    inputs.append(entry)

_GREEN_LAMP_TEST = "Lamp Test, Start press 2, lamp 63 lit"
# The Cabinet Wiring Diagram (manual printed page 46) draws the two coin-door switches on CPU connector CN14 with one common (CN14-2 WHT).
DOOR = PARTS["diagnostic_switches"]
DOOR_PINS = {-7: "3", -6: "4"}
if (DOOR["2"]["Wire"], DOOR["3"]["Drawn device"], DOOR["4"]["Drawn device"]) != ("WHT", "STEP", "FOR / REV"):
    raise SystemExit("the cabinet wiring diagram must draw STEP on CN14-3 and FOR / REV on CN14-4 with the WHT common on CN14-2")


def door_wiring(address: int) -> str:
    row = DOOR[DOOR_PINS[address]]
    return (
        f"The manual's Cabinet Wiring Diagram (printed page 46) draws the coin door's '{row['Drawn device']}' switch on CPU connector CN14 pin {DOOR_PINS[address]} "
        f"({row['Wire']}, through interconnect 1M/F pin {row['1M/F pin']} and the coin door's 1F/M4 pin {row['1F/M4 pin']}), closing to the WHT common on CN14 pin 2 "
        f"(1F/M4 pin {DOOR['2']['1F/M4 pin']}), which the memory lock switch on CN14 pin 1 shares."
    )


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
            f"Coin-door diagnostic button, named '{port_label}' by s11.h's DE_COMPORTS and placed in switch column 0 rather than the playfield matrix; Data East defines only "
            "these two (DE_SWADVANCE -7, DE_SWUPDN -6). "
            + (
                "The manual's diagnostics pages step through the tests with the STEP push-button. Every retained service run pulses it at level 1 (for 250 ms, 120 ms in the "
                "printer-interface run) while the ROM steps on each pulse and stays put at 0, so public 1 is the depressed button. s11.c hands its emulated PIA the "
                "complement (!core_getSw(DE_SWADVANCE)); the public level is the button state, and this record does not derive the level of the CPU board's input "
                "line from it. A momentary push-button rests released, with its contact open. "
                + door_wiring(address) + " The page draws the contact open."
                if address == -7 else
                "PinMAME's port declares it a toggle (COREPORT_BITTOG), and the manual's Single Lamp text calls it the FORWARD/REVERSE push-button: 'FORWARD (up)' selects "
                "higher-numbered lamps, 'REVERSE (down)' lower-numbered ones. The retained runs do not settle which public level is which position. With -6 at 1, the first Black "
                "press from attract entered the diagnostics and, in the printer-interface run, Black stepped backwards through the adjustments from 99 to 58; with -6 at 0, Black "
                "from attract walked towards the audits, yet the Lamp Test with -6 at 0 stepped from lamp 1 to 64, 63 and down, which the manual's text reads as REVERSE. s11.c "
                "hands the PIA the level uncomplemented (core_getSw(DE_SWUPDN)). " + door_wiring(address) + " It draws the contact open and prints 'CLOSE ??????' under "
                "the switch's label, so the page leaves open in which of the two positions the contact is closed. Which position closes the contact is therefore not "
                "established, and its contact polarity is left undeclared, which keeps the polarity requirement open."
            )
        )},
        **({"normally_closed": False} if address == -7 else {}),
        "spatial": not_applicable("cabinet_or_service", [S11_H, S11_C, MANUAL]),
    })

_FLIPPER_ROWS = {"left": COIL["flippers"]["Left Flipper"], "right": COIL["flippers"]["Right Flipper"]}
_flipper_items = flipper_column_inputs(
    flip_swno=FLIP_SWNO, flip_swno_text="FLIP6364 = FLIP_SWNO(63,64)",
    core_refs=(CORE, CORE_H, CORE_C, S11_C), button_refs=(SCRIPT_REF, VPM_DE_LIBRARY_SOURCE),
    button_notes={
        side: (
            f"The retained known-working script drives it: Table1_KeyDown/Table1_KeyUp hand the {side} flipper key to de.vbs vpmKeyDown/vpmKeyUp (script lines 349 and 364), "
            f"which set Controller.Switch({'swLLFlip' if side == 'left' else 'swLRFlip'}) with {'swLLFlip = 84' if side == 'left' else 'swLRFlip = 82'} "
            f"(excerpt vpm-script-library-flippers). The physical counterpart is the {side} cabinet flipper button."
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
        _row = _FLIPPER_ROWS["left" if _address == 84 else "right"]
        _item["provenance"]["source_refs"] += [RUNTIME_SRC, MANUAL]
        _item["physical"]["notes"] += (
            f" ROM evidence (1.12 Active Switch Test): holding public {_address} at 1 shows '{ROM_SWITCH[str(_matrix)]['name']}', the wires "
            f"{ROM_SWITCH[str(_matrix)]['wires']} and '#{_matrix}', the matrix switch core_updateSw copies it into, and fires {'47/48' if _address == 84 else '45/46'}, "
            "while the other six flipper-column addresses (81, 83 and 85-88) show NONE, so the ROM cannot see them."
            f" Contact: the manual's Flipper Solenoids table routes the flipper ground '{_row['CPU to flipper switch']}' through the cabinet flipper switch to the flipper "
            f"board ('{_row['Flipper switch to Flip. PCB']}'). A switch in series with the flipper's ground energises the coil while it is closed, so the released button rests "
            "open; public 1 is the pressed button."
        )
        _item["normally_closed"] = False
    else:
        _item["provenance"]["source_refs"].append(RUNTIME_SRC)
        _item["physical"]["notes"] += " ROM evidence: holding this address at 1 in the 1.12 Active Switch Test shows NONE."
inputs.extend(_flipper_items)

inputs.append({
    "id": "dip.jumper-w7",
    "label": "Jumper W7",
    "kind": "dip_switch",
    "binding": {"group": "pinmame.input.dip", "device": 0},
    "aliases": [{"namespace": "pinmame.dip", "value": "0"}],
    "availability": "unknown",
    "provenance": prov("observed", [S11_C, SCHEMATICS]),
    "physical": {"notes": (
        "s11.c declares MDRV_DIPS(1), commented '(actually a jumper)', and pia2a_r reads it as core_getDip(0) << 7 on PIA2 PA7, annotated 'PA7 (I) Jumper W7'. The "
        "factory name is J8: the CPU Board Logic Diagram (schematic book printed page 56) draws PA7, pin 9 of the 6821 at 11B (the PIA whose port B the same page "
        "takes to CN3, which PinMAME publishes as PIA2's), pulled up to +5 through RA19-9 (4.7K) and taken to ground through a link labelled J8, drawn as two "
        "terminals joined by a dashed line. No retained page says what the ROM does with the bit or how the link is fitted at the factory, so its meaning stays "
        "unknown."
    )},
    "spatial": not_applicable("dip_switch", [S11_C]),
})

# --- Output 23: the game-on boundaries pinned in the derived runtime evidence -------------------------------------------
_GO = FACTS["game_on_23"]
_go_entry = _GO["active-switches"]["test_entry_s"]
_go_before = [level for level in _GO["active-switches"]["levels"] if level["time_s"] < _go_entry]
_go_after = [level for level in _GO["active-switches"]["levels"] if level["time_s"] > _go_entry]
_go_games = [_GO[name] for name in ("trough-serve", "captive-lamps")]
if (
    not _go_before or _go_before[-1]["state"] != 0 or [level["state"] for level in _go_after] != [1]
    or any([level["state"] for level in game["levels"]] != [1] or game["levels"][0]["time_s"] <= game["shooter_lane_16_set_s"] for game in _go_games)
):
    raise SystemExit("the retained levels of output 23 no longer match the game-on note")
GAME_ON_NOTE = (
    f"ROM evidence (1.12), host times: in the Active Switch Test run 23 came on {sum(l['state'] for l in _go_before)} times and went off "
    f"{sum(1 - l['state'] for l in _go_before)} times while the run advanced through the diagnostics menus (first on at {_go_before[0]['time_s']:.2f} s, last off at "
    f"{_go_before[-1]['time_s']:.2f} s); it was off in the test's entry frame at {_go_entry:.2f} s, the baseline NONE frame, came on at "
    f"{_go_after[0]['time_s']:.2f} s and stayed on to the end of the run, so every later Active Switch Test snapshot shows it on. In the game-start and "
    f"captive-ball runs it came on once, {_go_games[0]['levels'][0]['time_s'] - _go_games[0]['shooter_lane_16_set_s']:.2f} s and "
    f"{_go_games[1]['levels'][0]['time_s'] - _go_games[1]['shooter_lane_16_set_s']:.2f} s after the run set the shooter-lane switch 16, and stayed on to the end. "
    "These transitions show when the ROM asserted the line in these runs, not what it gates it on."
)

# --- Outputs: drives 1-8, the left (coil) half of the Left/Right relay pair ------------------------------------------
MUXED = COIL["muxed"]
LEFT_IDS = {
    1: ("coil.trough-lockout", "Trough Lockout (6 Ball Assembly)"),
    2: ("coil.ball-release", "Ball Release"),
    3: ("coil.ball-launch", "Ball Launch (Auto Launch)"),
    4: ("coil.crane-lock", "Crane Lock"),
    5: ("coil.vuk", "VUK"),
    6: ("coil.right-scoop", "Right Scoop"),
    7: ("coil.ball-lock", "Ball Lock (Left Lock)"),
    8: ("coil.knocker", "Knocker"),
}
# Drives whose coil reaches the PPB board through a TIP 36C booster on J8, and the booster pin the coil wire leaves, as the schematic
# book's wiring sheet (printed page 50) draws them. The operator manual's coil-driver drawing prints the boosters of 3, 5 and 6 but not 8's.
BOOSTED = {3: ("Q5", "J8-2"), 5: ("Q4", "J8-4"), 6: ("Q3", "J8-7"), 8: ("Q2", "J8-10")}
SHEET_COILS = SCHEM["coil_sheet"]
PPB_INPUTS = SCHEM["ppb_inputs"]
SHEET_BOOSTERS = SCHEM["boosters"]
SUPPLY_50 = "+50VDCL PPB J7-8/9 YEL/VIO"
SUPPLY_32 = "+32VL PPB J6-2/1 BRN"
SCRIPT_BOUND_LEFT = {
    1: "SolCallback(1) = SolTrough, which kicks the ball from its sw14 kicker into its sw15 kicker and sets switch 15 (script lines 373 and 1108-1113)",
    2: "SolCallback(2) = SolRelease, which kicks its sw15 kicker into the shooter lane and clears switch 15 (script lines 374 and 1115-1121)",
    3: "SolCallback(3) = AutoLaunch, which fires its cvpmImpulseP plunger on the swPlunger trigger (script lines 375 and 1127-1143)",
    4: (
        "SolCallback(4) = SolCraneLock, which kicks the ball riding its crane boom off at the falling edge of the solenoid, and only while the left limit 60 is closed "
        "(script lines 376 and 739-747)"
    ),
    5: "SolCallback(5) = bsVuk.SolOut, which kicks its bsVuk saucer on the Sw47 kicker (script lines 377 and 184-190)",
    6: "SolCallback(6) = bsRScoop.SolOut, which kicks its bsRScoop saucer on the sw31 kicker (script lines 378 and 175-182)",
    7: (
        "SolCallback(7) = SolLockRelease, which drops its lock Post wall and sinks the blockPost primitive while a LockReleaseTimer runs, then restores both (script lines 379 "
        "and 535-547)"
    ),
    8: "SolCallback(8) = SolKnocker, which only plays a knocker sound (script lines 380 and 583-587)",
}
LEFT_ASSEMBLIES = {3: "5", 4: "16", 5: "11", 7: "17"}
LEFT_NOTES = {
    1: (
        "The six-ball trough's lockout: it kicks the ball at trough position 14 into the release position 15. Major Assemblies item 10 (6 Ball Switch Assy., 500-5683-01) "
        "is the trough, and item 23 (Lock Ball Assembly, 500-5684-00) is drawn beside it at the lower right. The schematic book's Trough Assembly page (printed page 75) "
        f"draws Lock Ball Assembly 500-5684-01 with this drive's coil, '{SHEET_ASM['lockout']['7']['Description']}' ({SHEET_ASM['lockout']['7']['Part No.']}), laid "
        "horizontally beside a lock-ball link and cam, above the 6 Ball Switch Assembly and that assembly's own 23-800 coil; its suffix is -01 where the Major Assemblies "
        "list prints -00."
    ),
    2: (
        "The schematic book's Trough Assembly page (printed page 75) draws the 6 Ball Switch Assembly 500-5683-01 (Major Assemblies item 10) with this coil, "
        f"'{SHEET_ASM['trough']['9']['Description']}' ({SHEET_ASM['trough']['9']['Part No.']}), standing under the low end of its row of trough switches."
    ),
    3: "The cabinet's Shooter Gun Assy. (Cabinet Parts item 1, 500-5731-00) carries the launch trigger 8; Major Assemblies item 5 is the Ball Launch Assy.",
    4: (
        "The Crane Assembly drawing (schematic book printed page 76) puts the 515-5889-00 COIL ASSY. under the boom at the cab end, so this coil rides the sweeping boom; the "
        "Crane Test text calls it 'the ball release coil on the crane mechanism'. The coil is part of the Crane Assy. (Major Assemblies item 16)."
    ),
    5: "Major Assemblies item 11 (VUK Assy.) is drawn hatched at the top right corner, beside item 26 (VUK Ramp, 500-5724-00).",
    6: (
        "Which scoop assembly in the Major Assemblies list is the right scoop is not printed: item 12 (New Scoop Assy., 500-5691-00) and item 19 (Double Scoop, "
        "515-5772-01) are the scoops it lists. The switch table types the scoop's switch 31 'Right Scoop Assembly' 500-5057-00."
    ),
    7: (
        "Major Assemblies item 17 (Lock Ball Assy., 500-5730-00) is drawn on the left side in the hatched lock area. The schematic book's Ball Lock Assembly drawing of the "
        f"same part number (printed page 73) lists its coil as '{SHEET_ASM['ball_lock']['11']['Description']}' ({SHEET_ASM['ball_lock']['11']['Part No.']}) where the "
        "coil-driver table and the wiring sheet both print 27-1400; the part number follows the two wiring sources, and no retained page settles which winding is fitted."
    ),
    8: (
        "The operator manual's coil-driver drawing prints this row differently from the wiring sheet: its coil wire is 'VIO-GRY (J2-2)' with no booster, and its supply "
        "wire BRN on J7-8,9. The wiring sheet routes the left-set connector's pin 2 (the manual's J2-2) on WHT/GRY into the booster Q2 at J8-9, takes the booster's "
        "VIO/GRY coil wire out of J8-10, and draws the coil on the YEL/VIO '+50VDCL PPB J7-8/9' bus with 3, 5 and 6, whose rows the manual also prints YEL-VIO on J7-8,9. "
        "The record follows the wiring sheet; the disagreement is a wiring detail, so no conflict is recorded. No retained page locates the knocker: the location drawing "
        "prints no 8L callout and the cabinet parts list has no knocker item."
    ),
}

for address in range(1, 9):
    row = MUXED[address]
    sheet = SHEET_COILS[f"{address}L"]
    device_id, label = LEFT_IDS[address]
    printed_coil = row["Coil wire (to coil)"]
    power_wire_printed, power_connection, _supply = row["Coil power"].split(" ", 2)
    if sheet["Coil type"] != row["Coil type"]:
        raise SystemExit(f"drive {address}: the wiring sheet's coil {sheet['Coil type']} differs from the coil table's {row['Coil type']}")
    if address in BOOSTED:
        booster, output = BOOSTED[address]
        drive_row = SHEET_BOOSTERS[booster]
        if (sheet["Coil-side end"], drive_row["Coil pin"]) != (output, output) or not sheet["Drawn label"].startswith(drive_row["Coil"]):
            raise SystemExit(f"drive {address}: the wiring sheet does not draw booster {booster} with its coil pin {output} on {sheet['Drawn label']!r}")
        if address == 8:
            coil_wire_printed = printed_coil.partition(" ")[0]
            if printed_coil != "VIO-GRY (J2-2)" or drive_row["Drive line comes from"] != "left-set connector pin 2":
                raise SystemExit(f"drive 8: expected the manual's 'VIO-GRY (J2-2)' and the sheet's pin-2 drive line, not {printed_coil!r}")
        else:
            coil_wire_printed = printed_coil.rsplit(", ", 1)[1]
            if f"{booster} TIP 36C {output}" not in printed_coil:
                raise SystemExit(f"drive {address}: the booster {booster} {output} is not in the printed coil cell {printed_coil!r}")
        if wire(coil_wire_printed) != wire(drive_row["Coil wire"]):
            raise SystemExit(f"drive {address}: the coil wire {coil_wire_printed} differs from the sheet's {drive_row['Coil wire']}")
        control_connection = f"PPB {output}"
    else:
        coil_wire_printed, _, pin = printed_coil.partition(" ")
        control_connection = f"PPB {pin.strip('()')}"
        if sheet["Coil-side end"] != f"left-set connector pin {pin.strip('()').removeprefix('J2-')}" or wire(sheet["Coil-side wire"]) != wire(coil_wire_printed):
            raise SystemExit(f"drive {address}: the wiring sheet ends the coil at {sheet['Coil-side end']!r} on {sheet['Coil-side wire']}, not {printed_coil!r}")
    supply = SUPPLY_50 if address in BOOSTED else SUPPLY_32
    if sheet["Supply bus"] != supply:
        raise SystemExit(f"drive {address}: the wiring sheet's supply is {sheet['Supply bus']!r}, expected {supply!r}")
    notes = [
        f"Left half of the Left/Right relay pair on drive {address} (CPU transistor {row['Transistor']}, CN-11 pin {row['CN-11 pin']}, '{row['CPU to PPB wire']}' into PPB "
        f"{row['PPB input']}); the right half, the flash-lamp set, is published at {address + 24}. The coil-driver schematic draws the coil '{row['Left coil']} "
        f"{row['Coil type']}' on '{printed_coil}' with power '{row['Coil power']}'. The schematic book's wiring sheet (printed page 50) draws it as '{sheet['Drawn label']} "
        f"{sheet['Coil type']} {sheet['Position']}' on the '{sheet['Supply bus']}' bus.",
        f"The retained table binds {SCRIPT_BOUND_LEFT[address]}.",
    ]
    for note in (wire_note(coil_wire_printed, "the coil wire"), wire_note(row["CPU to PPB wire"], "the CPU line")):
        if note:
            notes.append(note)
    board = PPB_INPUTS[f"J1-{address}"]
    game_pin = int(re.search(r"\(J2-(\d+)\)", printed_coil).group(1))
    if board["J9 pin"] != row["Return wire"].split(" ")[1].strip("()") or board["J2 pin"] != f"J2-{game_pin - 1}":
        raise SystemExit(f"drive {address}: the PPB-1 schematic's {board} does not pair with the coil-driver drawing's row")
    if row["PPB input"] != f"J1-{address}":
        notes.append(
            f"The coil-driver drawing prints the PPB input '{row['PPB input']}' where the other six left drives print J1. The wiring sheet (printed page 50) brings "
            f"all eight drive lines into one fifteen-pin PPB connector, pin {address} for this drive, and the PPB-1 board schematic (printed page 67) names that input "
            f"J1-{address}, so the record reads the drawing's J2 as the input header J1."
        )
    notes.append(
        f"The PPB-1 board schematic (printed page 67) draws this drive's left-set output from input J1-{address} on {board['J2 pin']}, one pin below the J2-{game_pin} "
        f"that the coil-driver drawing prints and the pin {game_pin} the wiring sheet prints on its unnamed left-set connector"
        + {10: "; the board schematic draws its own J2-10 on a short line that ends unconnected", 3: "; the board schematic draws no J2-3"}.get(game_pin, "")
        + ". The sources agree on the drive, its public address and its coil, so the pin numbering is a wiring detail: the record follows the game's two "
        "drawings, which agree, and records no conflict."
    )
    if address in BOOSTED:
        booster, output = BOOSTED[address]
        drive_row = SHEET_BOOSTERS[booster]
        notes.append(
            f"The drive reaches the coil through the TIP 36C booster {booster} on the PPB board: the wiring sheet brings the drive line in on {drive_row['Drive-line pin']} "
            f"({drive_row['Drive-line wire']}) and the coil wire out of {drive_row['Coil pin']}, the control connection recorded here. The sheet's supply is the 50 V bus"
            + (", and it prints '50V' under the coil's label" if "50V" in sheet["Drawn label"] else "")
            + f"; the ROM names the coil '{ROM_COIL[address]}'. The manual's coil-driver drawing boxes the same J7-8,9 supply '+ 32 VL' like the J6-3 rows; the record "
            "follows the wiring sheet's 50 V."
        )
    else:
        notes.append(
            "The wiring sheet takes the coil's BRN supply from '+32VL PPB J6-2/1' where the coil-driver table prints J6-3; both are 32 V, and the record keeps the table's pin."
        )
    if address in LEFT_NOTES:
        notes.append(LEFT_NOTES[address])
    entry = {
        "id": device_id,
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, SCHEMATICS, CORE, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"part_number": row["Coil type"], "notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": row["Transistor"],
            "control_wire": wire(coil_wire_printed),
            "control_connection": control_connection,
            "power_wire": "YEL-VIO" if address in BOOSTED else wire(power_wire_printed),
            "power_connection": f"PPB {power_connection}",
        },
    }
    if address in BOOSTED:
        if power_connection != "J7-8,9":
            raise SystemExit(f"drive {address}: expected the J7-8,9 supply, not {row['Coil power']!r}")
        entry["wiring"].update({"nominal_voltage_v": 50, "voltage_type": "dc"})
    else:
        if row["Coil power"] != "BRN J6-3 +32 VL":
            raise SystemExit(f"drive {address}: expected the BRN J6-3 +32 VL supply, not {row['Coil power']!r}")
        entry["wiring"].update({"nominal_voltage_v": 32, "voltage_type": "dc"})
    if address in LEFT_ASSEMBLIES:
        entry["physical"]["assembly_part_number"] = asm(LEFT_ASSEMBLIES[address])
    if address not in (4, 8):
        located = spatial_for(device_id, "effect", f"solenoid.{address}")
        if not located:
            raise SystemExit(f"solenoid {address} has no retained placement")
        entry["spatial"] = located
        entry["physical"]["notes"] += (
            f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}, the table's model of the mechanism this coil actuates, not a claimed winding centre."
        )
    else:
        entry["physical"]["notes"] += f" Not placed: {unplaced_reason(f'solenoid.{address}').split(': ', 1)[1]}."
    outputs.append(entry)

# --- Outputs: drives 9-16, direct on CPU CN12 -------------------------------------------------------------------------
DIRECT = COIL["direct"]
DIRECT_IDS = {
    9: ("flasher", "flasher.crane-and-insert", "Flash Lamps 9 (Crane and Insert)"),
    10: ("relay", "relay.left-right-relay", "Left/Right Relay"),
    11: ("gi", "gi.general-illumination", "G.I. Relay"),
    12: ("coil", "coil.ramp-diverter", "Ramp Diverter"),
    13: ("coil", "coil.drop-target-reset", "Drop Target Reset"),
    14: ("motor", "motor.crane", "Crane Motor"),
    15: ("coil", "coil.middle-scoop", "Middle Scoop"),
    16: ("motor", "motor.shaker", "Shaker Motor"),
}
# (power wire, power connection, volts, the text that must appear in the printed cell)
DIRECT_POWER = {
    9: (None, None, 32, "PS board CN3-6 `+32V`"),
    10: ("RED-WHT", "PS CN3-5", 32, "RED/WHT to PS board CN3-5 `+32V`"),
    11: (None, None, None, "GENERAL ILLUM. RELAY"),
    12: ("RED", "PS CN3-6,7,8", 32, "power wire RED"),
    13: ("RED", "PS CN3-6,7,8", 32, "power wire RED"),
    14: ("GRY-RED", "PS CN6-3", 12, "`GRY/RED` to PS board CN6 pin 3 `+12VDC`"),
    15: ("RED", "PS CN3-6,7,8", 32, "power wire RED"),
    16: (None, None, None, "CABINET SHAKER MOTOR 12VDC"),
}
# Drive 9 against relay 10 across every retained run: the conflict below rests on 10 being on at every rise of 9.
DRIVE_9 = FACTS["drive_9_relay_10"]
if not DRIVE_9["rises"] or DRIVE_9["with_10_on"] != DRIVE_9["rises"]:
    raise SystemExit(f"the retained runs turned 9 on with 10 off ({DRIVE_9}); the drive-9 supply conflict must be re-read")
DIRECT_NOTES = {
    9: (
        "Four No. 89 flash lamps: the schematic labels them '(2) CRANE (2) INSERT' and the ROM names the drive '" + ROM_COIL[9] + "'. The Crane Assembly drawing puts two "
        "165-5000-89 lamps in the crane's cab, the Flash Lamp / Coil Tests location drawing prints callout 9 twice at the crane, and the Backbox Flash Lamps drawing shows two "
        "9R sockets, so two ride the crane boom and two light the backbox insert. PinMAME types the output a No. 89 flasher (s11.c line 1224). The retained table binds "
        "SolCallback(9) = Lampz.SetLamp 109, commented '09 - Flash Crane(x2) + Backbox Inserts(x2)' (script line 381). The schematic book's wiring sheet (printed "
        "page 50) draws the same four lamps, '(2) CRANE (2) INSERT' '(4) NO.89', on the '+32 VDCR PPBJ6-4/5' ORG supply of the right-set flash groups, where the "
        "coil-driver drawing returns their common to PS board CN3-6. The two disagree on more than a pin: printed page 32 says the Left/Right relay 10 switches "
        "+32 volts between the left-set coils and the right-set flash lamps, so on the wiring sheet the four lamps light only while 10 is energised, and on the "
        f"coil-driver drawing they light whatever 10's state. In every retained run 10 was already on whenever 9 turned on ({DRIVE_9['rises']} times in "
        f"{DRIVE_9['runs']} runs), so the runs "
        "cannot tell the two apart. The record keeps the public binding at 9 and the 32 V both drawings print, records no power connection and no relationship to "
        "10, and records the relay dependency as a conflict."
    ),
    10: (
        "Energising it re-routes drives 1-8 from the coils (left set) to the flash lamps (right set): printed page 32 says the relay switches +32 volts between them and is "
        "located on the PPB board, and pinned PinMAME publishes the right set at 25-32 (s11.c updsol, muxSol 10). The schematic draws the L/R COIL RELAY on PPB pins 9 and 2. "
        "The retained table binds nothing to 10 (SolCallback(10) is commented out, script line 382): its flash-lamp callbacks are bound to 25-32."
    ),
    11: (
        "There is no GI channel on this platform: the general illumination is solenoid 11, the G.I. relay RY1 on the power-supply board. The Power Supply Board "
        "Schematic (schematic book printed page 59) draws RY1 (24VDC/10A) with its coil on CN7 pins 1 and 3 and its diode D1 (1N4001) with the cathode on pin 3, so the "
        "positive supply is on pin 3 and the drive on pin 1. The operator manual's coil-driver drawing agrees: drive 11's BRN-ORG line enters CN7 pin 1 of the 'K-1' "
        "box, and pin 3 joins the +32V line of PS board CN3 pins 6-8. The Coil/Flash Lamp sheet (printed page 50) prints the reverse, '+ 32V' on pin 1 and the BRN/ORG "
        "line from CPU CN12 pin 4 on pin 3, with its diode's cathode towards pin 1. The record follows the board's own schematic and the coil-driver drawing; the "
        "disagreement is a wiring detail, so no conflict is recorded. Both changeover contacts are "
        "drawn de-energised, their joined moving contacts resting on contacts 2 and 1, and they carry the feed from CN9 pins 1 and 3 to CN8 pins 1-4, which the board "
        "joins; contacts 4 and 3 are connected to nothing, and CN8 pins 6-9 take CN9 pins 2 and 4 straight through. The Coil/Flash Lamp sheet's General Illumination "
        "Lines draw the power-supply connector (CN8 by its nine pins and its unconnected pin 5) with pins 1-4 (BRN, YEL, GRN, VIO) as '6.3 VAC OUTPUT TO BULBS' and "
        "pins 6-9 to the PPB board's G.I. fuses F4, F3, "
        "F2 and F1 (WHT/BRN, WHT/YEL, WHT/GRN, WHT/VIO), whose fused sides return to the bulbs. The fuse drawing (operator manual printed page 2, Detail A) labels "
        "those fuses, 'All 5A S.B.', F1 'Playfield', F2 'Backbox Door & Speaker Panel', F3 'Playfield & Coin Door' and F4 'Backbox Door'. So energising 11 opens "
        "the common feed of every G.I. line, and the playfield, backbox door, speaker panel and coin door G.I. go dark together. s11.c types 11 "
        "CORE_MODOUT_BULB_44_6_3V_AC_REV for the lah_ games ('GI output', line 1225), and what a consumer reads at 11 depends on the read path. The binary solenoid "
        "state is the relay drive: 1 energises the relay and the G.I. is dark, 0 releases it and the G.I. is lit. With modulated or physical solenoid outputs "
        "enabled (CORE_MODOUT_ENABLE_MODSOL or CORE_MODOUT_ENABLE_PHYSOUT_SOLENOIDS), core_getSol(11) returns the integrated brightness of the G.I. bulbs instead "
        "(core.c line 2464): the bulb type sets isReversed (lines 3422-3429) and the bulb model applies it before integrating (line 3265), so that value is already "
        "the G.I. brightness and must not be inverted again. The retained table's SolGI (SolCallback(11), script lines 383 and 471-489) reads the binary state, as the "
        "script sets no UseModSol, and turns its G.I. off while the solenoid is on. The schematic book's lamp sheet draws only a "
        "'G.I. LAMPS' block of two bulb pairs on connector 4M/F6 pins 1-4 (YEL, WHT-YEL, VIO, WHT-VIO, 'TO G.I. FUSES'), the colours of the F3 and F1 lines. No "
        "retained page counts or locates the G.I. bulbs, so no quantity or coordinate is claimed. The legacy corpus's 'GI String' lamp 0 is this output; its "
        "aliases are kept here."
    ),
    12: (
        "Major Assemblies item 24 (Diverter, 515-5453-00) is drawn at the left ramp entry, and the location drawing's callout 12 sits centre-left at the diverter. The "
        "retained table binds SolCallback(12) = SolDiv, which swaps its DivOpen and DivClose walls and swings its DivFlipper while the solenoid is on and back when it turns "
        "off (script lines 384 and 517-527)."
    ),
    13: (
        "It resets the five-bank (Major Assemblies item 6, 5 Bank Drop Target). The retained table binds SolCallback(13) = SoLDrop, which raises all five of its targets when "
        "the solenoid turns on (script lines 385 and 501-511). The schematic book's 5-Bank Drop Target Assembly drawing of the bank's part number, 500-5621-05 (printed "
        f"page 74), lists '{SHEET_ASM['drop_targets']['11']['Description']}' ({SHEET_ASM['drop_targets']['11']['Part #']}) where the coil-driver drawing prints "
        "'DROP TARGET 23-800'; the part number follows this game's coil-driver drawing, and no retained page settles which winding is fitted."
    ),
    14: (
        "The supply is recorded as the 12 V DC the schematic prints. Major Assemblies item 1 is the Crane Motor (041-5027-00), the part the Crane Assembly drawing calls '041-5027-00 MOTOR (CRANE)': it hangs under the playfield on "
        "the motor bracket and turns the vertical shaft that carries the cab and boom, and the Crane Test text says it rotates in one direction while a cam sweeps the arm "
        "through 145 degrees and back. The retained table binds SolCallback(14) = SoLCraneMotor, which runs its CraneTimer to turn the boom while the solenoid is on "
        "(script lines 386, 620-628 and 653-696)."
    ),
    15: (
        "The retained table binds SolCallback(15) = bsMLScoop.SolOut, which kicks its bsMLScoop saucer on the Sw57 kicker (script lines 387 and 192-199)."
    ),
    16: (
        "The cabinet shaker. That Q4 is a transistor drawn beside the shaker circuit, not drive 5's PPB booster. The Cabinet Parts Illustration's item 34 is the Shaker Motor (515-5893-00), drawn inside the cabinet, and item 35 the "
        "Shaker Motor P.C. Board (520-5065-00). The supply is a board output rather than a printed supply wire, so no power wiring or voltage is recorded. The retained "
        "table leaves SolCallback(16) commented out (script line 388)."
    ),
}
DIRECT_PARTS = {12: "27-1400", 13: "23-800", 14: "041-5027-00", 15: "23-800", 16: CABINET["34"]["Part No."]}
DIRECT_ASSEMBLIES = {12: "24", 13: "6", 14: "16"}
if (ASSEMBLIES["1"]["Description"], ASSEMBLIES["1"]["Part No."]) != ("Crane Motor", "041-5027-00") or CABINET["34"]["Description"] != "Shaker Motor":
    raise SystemExit("the parts lists must print Major Assemblies item 1 Crane Motor 041-5027-00 and Cabinet Parts item 34 Shaker Motor")
for address in range(9, 17):
    row = DIRECT[address]
    kind, device_id, label = DIRECT_IDS[address]
    power_wire, power_connection, volts, printed = DIRECT_POWER[address]
    if printed not in row["Device as drawn"]:
        raise SystemExit(f"drive {address}: {printed!r} is not in the printed device cell {row['Device as drawn']!r}")
    if address in (12, 13, 15) and DIRECT_PARTS[address] not in row["Device as drawn"]:
        raise SystemExit(f"drive {address}: part {DIRECT_PARTS[address]} is not in the printed device cell")
    notes = [
        f"The coil-driver schematic draws drive {row['Drive']} (CPU transistor {row['Transistor']}, CN-12 pin {row['CN-12 pin']}, {row['Wire']}) to: "
        + row["Device as drawn"].replace("`", "'") + ".",
        DIRECT_NOTES[address],
    ]
    for note in (wire_note(row["Wire"], "the CPU line"),):
        if note:
            notes.append(note)
    if address == 14:
        notes.append("The schematic prints the supply 'GRY/RED'; it is recorded as GRY-RED.")
    if address == 10:
        notes.append("The schematic prints the supply 'RED/WHT'; it is recorded as RED-WHT.")
    entry = {
        "id": device_id,
        "label": label,
        "kind": kind,
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases(
            "pinmame.coil", address, "coil", LEGACY_COILS,
            extra=[("vpe-legacy.lamp", value) for value in legacy_numbers(0)] if address == 11 and 0 in LEGACY_LAMPS else (),
        ),
        "availability": "used",
        "provenance": prov(
            "conflicted" if address == 9 else "validated",
            [MANUAL, CORE, S11_C, RUNTIME_SRC] + ([] if address in (10, 16) else [SCRIPT_REF]) + ([SCHEMATICS] if address in (9, 11, 13, 14) else [])
            + ([CORE_C] if address == 11 else []),
        ),
        "physical": {"notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": row["Transistor"],
            "control_wire": wire(row["Wire"]),
            "control_connection": f"CPU CN12-{row['CN-12 pin']}",
        },
    }
    if power_wire:
        entry["wiring"]["power_wire"] = power_wire
    if power_connection:
        entry["wiring"]["power_connection"] = power_connection
    if volts:
        entry["wiring"].update({"nominal_voltage_v": volts, "voltage_type": "dc"})
    if address in DIRECT_PARTS:
        entry["physical"]["part_number"] = DIRECT_PARTS[address]
    if address in DIRECT_ASSEMBLIES:
        entry["physical"]["assembly_part_number"] = asm(DIRECT_ASSEMBLIES[address])
    if address == 9:
        entry["physical"].update({"part_number": "#89", "quantity": 4})
    if address == 11:
        entry["roles"] = ["playfield.general-illumination", "backbox.general-illumination", "cabinet.general-illumination"]
    if address in (10, 16):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL])
    elif address in (9, 11):
        entry["physical"]["notes"] += f" Not placed: {unplaced_reason(f'solenoid.{address}').split(': ', 1)[1]}."
    else:
        located = spatial_for(device_id, "effect", f"solenoid.{address}", extra_refs=[MANUAL, SCHEMATICS] if address in (13, 14) else ())
        if not located:
            raise SystemExit(f"solenoid {address} has no retained placement")
        entry["spatial"] = located
        entry["physical"]["notes"] += f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}" + {
            13: ", a projection: the table models no reset coil, so the coordinate is the bank's middle target, the one object that stands for the bank.",
            14: (
                ", a projection: the coordinate is the crane's rotation axis, which the table's three crane meshes share and which the Crane Assembly drawing puts the "
                "motor under; it is not a measured motor centre."
            ),
        }.get(address, ", the table's model of the mechanism this output drives, not a claimed winding centre.")
    outputs.append(entry)

# --- Solenoids 17-22: the CPU-controlled auxiliary (switched) solenoids ------------------------------------------------
AUXILIARY = COIL["auxiliary"]
AUX_IDS = {
    17: ("coil.left-turbo-bumper", "Left Turbo Bumper"),
    18: ("coil.center-turbo-bumper", "Center (Bottom) Turbo Bumper"),
    19: ("coil.right-turbo-bumper", "Right Turbo Bumper"),
    20: ("coil.left-slingshot", "Left Slingshot"),
    21: ("coil.right-slingshot", "Right Slingshot"),
    22: ("coil.ripper-kickback", "Ripper Kickback"),
}
AUX_SCRIPT = {
    17: "leaves SolCallback(17) commented out (script line 389): its VPX bumper Bumper1 kicks the ball on contact",
    18: "leaves SolCallback(18) commented out (script line 390): its VPX bumper Bumper3 kicks the ball on contact",
    19: "leaves SolCallback(19) commented out (script line 391): its VPX bumper Bumper2 kicks the ball on contact",
    20: "leaves SolCallback(20) commented out (script line 392): its LeftSlingshot wall kicks the ball on contact",
    21: "leaves SolCallback(21) commented out (script line 393): its RightSlingshot wall kicks the ball on contact",
    22: "binds SolCallback(22) = SolRipperKick, which kicks its Sw48 kicker out while the solenoid turns on (script lines 394 and 593-602)",
}
AUX_ASSEMBLIES = {17: "4", 18: "4", 19: "4", 20: "3", 21: "3", 22: "2"}
_RIPPER_400 = counts("Laser Kick Test: close public switch 48 for 400 ms", TEST)
_RIPPER_1500 = counts("Laser Kick Test: close public switch 48 for 1500 ms", TEST)
if _RIPPER_400 != {22: 1} or _RIPPER_1500 != {22: 1}:
    raise SystemExit("the Laser Kick Test must fire 22 once from switch 48")
for address in range(17, 23):
    row = AUXILIARY[address]
    device_id, label = AUX_IDS[address]
    control_wire, control_connection = row["Control line (CPU to coil)"].split(" ", 1)
    power_wire, power_connection = row["Power line (PS to coil)"].split(" ", 1)
    notes = [
        f"Printed page 32's CPU Controlled Auxiliary Solenoids table prints coil {address} '{row['Coil description']}', control '{row['Control line (CPU to coil)']}', "
        f"power '{row['Power line (PS to coil)']}', transistor {row['Drive transistor']} and type {row['Coil type']}. One of the six switched solenoids: CORE_FIRSTSSSOL "
        f"is 17 and Data East's PIA permutation publishes them at 17 + ssSolNo; the ROM's Cycling Coils test names public {address} '{ROM_COIL[address]}', which pairs the "
        "printed coil with the public address.",
        f"The retained table {AUX_SCRIPT[address]}.",
    ]
    if address in (17, 18, 19):
        notes.append(
            "The coil table calls 18 the Center Turbo Bumper, the switch chart calls its switch 34 the Bottom Turbo Bumper and the lamp chart calls its lamp 7 the Top Turbo "
            "Bumper; the ROM names all three BOTTOM. It is the third bumper, below the left and right ones."
            if address == 18 else
            f"The ROM names its switch {address + 16} and its lamp {address - 11} the {'LEFT' if address == 17 else 'RIGHT'} turbo bumper too."
        )
    if address == 22:
        ripper = SHEET_COILS["SOL 22"]
        booster = SHEET_BOOSTERS["Q1"]
        if (booster["Coil"], booster["Coil pin"], booster["Drive-line pin"], ripper["Coil-side end"]) != ("RIPPER KICKBACK", "J8-12", "J8-11", "J8-12"):
            raise SystemExit("the wiring sheet must draw the Ripper Kickback on booster Q1, J8-11 in and J8-12 out")
        if ripper["Supply bus"] != "+50V PPB J7-P3 VIO/YEL" or ripper["Coil type"] != row["Coil type"] or "CN19-P9 Q13" not in booster["Drive line comes from"]:
            raise SystemExit("the wiring sheet's Ripper Kickback supply, coil or CPU line differs from the coil table")
        control_wire, control_connection = wire(booster["Coil wire"]), f"PPB {booster['Coil pin']}"
        notes.append(
            f"The schematic book's wiring sheet (printed page 50) draws the coil '{ripper['Drawn label']} {ripper['Coil type']} {ripper['Position']}' behind a TIP 36C booster "
            f"on the PPB board: the CPU line {booster['Drive-line wire']} from CPU CN19-9 ({row['Drive transistor']}) enters Q1 on {booster['Drive-line pin']}, and the "
            f"coil wire {booster['Coil wire']} leaves on {booster['Coil pin']}, the control connection recorded here. The printed table's control line "
            f"'{row['Control line (CPU to coil)']}' is the CPU side of the booster. The sheet's supply is '{ripper['Supply bus']}', the table's '{row['Power line (PS to coil)']}', "
            "and the +50VDC the Magnet Control Board takes from the same pin (schematic book printed page 70); the ROM names the "
            f"coil '{ROM_COIL[22]}', so the nominal voltage is 50 V. Major Assemblies item 2 (Kick Back Assy) is drawn on the right wall at the upper right. ROM evidence (1.12 "
            "Laser Kick Test, the screen reading '>FEED BALL TO RIPPER<'): closing switch 48 fires public 22 once, whether the switch is held 400 ms or 1.5 s."
        )
        notes.append(wire_note(booster["Coil wire"], "the coil wire"))
    entry = {
        "id": device_id,
        "label": label,
        "kind": "coil",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC, SCRIPT_REF] + ([SCHEMATICS] if address == 22 else [])),
        "physical": {"part_number": row["Coil type"], "assembly_part_number": asm(AUX_ASSEMBLIES[address]), "notes": " ".join(notes)},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Drive transistor"],
            "control_wire": control_wire, "control_connection": control_connection,
            "power_wire": power_wire, "power_connection": power_connection,
            "nominal_voltage_v": 50 if address == 22 else 32, "voltage_type": "dc",
        },
    }
    located = spatial_for(device_id, "effect", f"solenoid.{address}")
    if not located:
        raise SystemExit(f"solenoid {address} has no retained placement")
    entry["spatial"] = located
    entry["physical"]["notes"] += f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}."
    outputs.append(entry)

outputs.append({
    "id": "control.game-on",
    "label": "Game On / Switched Solenoid Enable",
    "kind": "control_signal",
    "binding": {"group": "pinmame.output.solenoid", "device": 23},
    "aliases": aliases("pinmame.solenoid", 23),
    "availability": "used",
    "provenance": prov("validated", [S11_C, S11_H, RUNTIME_SRC]),
    "physical": {"notes": (
        "S11_GAMEONSOL is 23, driven by PIA0 CB2 (s11.c pia0cb2_w). It enables the switched solenoids and gates the flippers rather than driving a device of its own; "
        "core_updateSw passes it to the flipper synthesis as the enable. " + GAME_ON_NOTE + " The retained table binds nothing to 23."
    )},
    "spatial": not_applicable("virtual", [S11_C]),
})
outputs.append({
    "id": "virtual.unused-24",
    "label": "Unused Solenoid 24",
    "kind": "virtual",
    "binding": {"group": "pinmame.output.solenoid", "device": 24},
    "aliases": aliases("pinmame.solenoid", 24),
    "availability": "unused",
    "provenance": prov("validated", [S11_C, RUNTIME_SRC]),
    "physical": {"notes": "Reserved slot between the switched solenoids and the muxed right set; s11.c publishes nothing here, and no retained run moved it."},
    "spatial": not_applicable("unused", [S11_C]),
})

# --- Solenoids 25-32: the right half of the relay pair, all flash lamps ------------------------------------------------
FLASH_LABELS = {
    1: "Top Right Police Lights", 2: "Playfield Upper Left", 3: "Ramp", 4: "Playfield Upper Right",
    5: "Playfield Mid Right", 6: "Playfield Lower Right", 7: "Top Left Police Lights", 8: "Playfield Lower Left",
}
SCRIPT_FLASH_COMMENTS = {
    1: "1R - Flash Topper Right Police(x4)",
    2: "2R - Flash Playfield Upper Left(x3) + Backbox Insert",
    3: "3R - Flash Ramp(x2) + Backbox Insert(x2)",
    4: "4R - Flash Playfield Upper Right(x2) + Backbox Insert(x2)",
    5: "5R - Flash Playfield Mid Right(x3) + Backbox Insert",
    6: "6R - Flash Playfield Low Right(x4)",
    7: "7R - Flash Topper Left Police(x4)",
    8: "8R - Flash Playfield Low Left + Backbox Insert(x2)",
}
# Callouts on the Flash Lamp / Coil Tests location drawing (playfield) and the Backbox Flash Lamps drawing, per group.
DRAWN = {1: (0, 0), 2: (3, 1), 3: (2, 2), 4: (2, 2), 5: (2, 1), 6: (4, 0), 7: (0, 0), 8: (1, 2)}
FLASH_QUANTITY = {drive: (3 if drive == 8 else 4) for drive in range(1, 9)}
FLASH_NOTES = {
    1: (
        "A topper group: the coil-driver drawing's '(4) TOP RIGHT POLICE LIGHTS', the wiring sheet's '(4) TOP RIGHT BACK BOX' and the ROM's 'BIG RGT MARS' name four "
        "lamps at the top of the backbox, none on the playfield."
    ),
    7: (
        "A topper group: the coil-driver drawing's '(4) TOP LEFT POLICE LIGHTS', the wiring sheet's '(4) TOP LEFT BACKBOX' and the ROM's 'BIG LEFT MARS' name four "
        "lamps at the top of the backbox, none on the playfield."
    ),
    4: (
        "The schematic counts one upper-right playfield lamp, two inserts and one back-panel lamp, the ROM '2-INS 2-PLFD' and the location drawing two 4R callouts on the "
        "playfield; all three give four lamps, two of them in the backbox insert, and they differ only on whether the back-panel lamp counts as playfield."
    ),
    5: (
        "The quantity follows the two wiring drawings, which record the group positively: the coil-driver drawing's '(3) MID RIGHT PLFD (1) INSERT' and the "
        "schematic book's wiring sheet's '(3) MID RIGHT PLFD (1) INSERT' with its own bulb list '(3) NO. 906 (1) NO. 89'. The location drawing prints only two 5R "
        "callouts on the playfield; a missing callout is weaker evidence than those positive records, and no source describes two playfield lamps. The ROM's "
        "'1-INS 3-PLFD' agrees, but it is a diagnostic label, not a count, so it only corroborates. 8R differs: there the ROM's name and the retained script describe "
        "a single playfield lamp, joining the location drawing against the wiring drawings, so that count is a conflict."
    ),
    6: (
        "The wiring sheet's caption splits the four into '(2) LOWER RIGHT PLFD' and '(2) MAGNETS' where the coil-driver drawing prints '(4) PLFD-LOWER RIGHT'; both count "
        "four lamps on the playfield, and the ROM's '4-PLFD' agrees. No retained page draws where the two 'MAGNETS' lamps sit."
    ),
    8: (
        "The working quantity is three: the location drawing prints one 8R callout on the playfield and the backbox drawing two 8R sockets, the ROM names the drive "
        "'2-INS 1-TAR PIT' and the retained script comments it 'Flash Playfield Low Left + Backbox Insert(x2)'. Both wiring drawings count four: the coil-driver "
        "drawing's '(2) LOW LEFT PLFD (2) INSERT (4) 89' and the schematic book's wiring sheet's '(2) PLFD (2) INSERT (4) NO.89', which draws every group as one box "
        "of four sockets. The ROM's name and the script's comment describe the group but cannot count its bulbs, so the physical count stays unresolved and is "
        "recorded as a conflict."
    ),
}
# Groups whose bulb type the factory drawings disagree on: the coil-driver drawing prints four No. 89, the wiring sheet three No. 906 and one No. 89.
MIXED_BULB_GROUPS = {4, 5}
SHEET_FLASH = SCHEM["flash_groups"]
for address in range(25, 33):
    drive = address - 24
    row = MUXED[drive]
    return_printed, return_pin = row["Return wire"].split(" ")
    on_playfield, in_backbox = DRAWN[drive]
    notes = (
        f"Right half of the Left/Right relay pair on drive {drive}; the left half is published at {drive}. The coil-driver schematic draws the right set '{row['Right set']}' "
        f"returning through '{row['Return wire']}' from the PPB board and fed '+32 VR' through the ORG wire from PPB J6 pins 4,5; PinMAME types the whole 25-32 block as "
        f"No. 89 flashers ('8 muxed flasher outputs (K1 relay is solenoid #10)', s11.c line 1226). The ROM names the group '{ROM_COIL[address]}'. The Flash Lamp / Coil "
        f"Tests location drawing prints {counted(on_playfield, f'{drive}R callout')} on the playfield and the Backbox Flash Lamps drawing "
        f"{counted(in_backbox, f'{drive}R socket')}. The retained table binds SolCallBack({address}) = Lampz.SetLamp {100 + drive}, commented "
        f"'{SCRIPT_FLASH_COMMENTS[drive]}' (script line {395 + drive})."
    )
    sheet = SHEET_FLASH[f"{drive}R"]
    sheet_bulbs = sheet["Bulbs printed under the group"]
    if (sheet_bulbs == "(3) NO. 906 (1) NO. 89") != (drive in MIXED_BULB_GROUPS) or (drive not in MIXED_BULB_GROUPS and sheet_bulbs != "(4) NO.89"):
        raise SystemExit(f"flash group {drive}R: the wiring sheet prints {sheet_bulbs!r}")
    notes += (
        f" The schematic book's wiring sheet (printed page 50) captions the group '{sheet['Caption']}' with '{sheet_bulbs}' and draws the same '+ 32VDCR PPB J6-4/5' "
        "ORG supply."
    )
    if drive in MIXED_BULB_GROUPS:
        notes += (
            " The factory drawings disagree on the bulbs: the coil-driver drawing prints four No. 89, the wiring sheet three No. 906 and one No. 89, and the Lamp Bulb Part "
            "Numbers drawing (printed page 38) marks one #906 socket on the right side of the playfield. No retained page settles which bulbs are fitted, so no part number "
            "is recorded; PinMAME's No. 89 typing is the emulator's output model, not a bulb count. A look at a working machine would settle it."
        )
    if drive in FLASH_NOTES:
        notes += " " + FLASH_NOTES[drive]
    note = wire_note(return_printed, "the return wire")
    if note:
        notes += " " + note
    notes += " The schematic prints the supply wire 'ORG'; it is recorded as ORN."
    entry = {
        "id": f"flasher.{drive}r",
        "label": f"Flash Lamps {drive}R ({FLASH_LABELS[drive]})",
        "kind": "flasher",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("conflicted" if drive == 8 else "validated", [MANUAL, SCHEMATICS, CORE, S11_C, SCRIPT_REF, RUNTIME_SRC]),
        "physical": {**({} if drive in MIXED_BULB_GROUPS else {"part_number": "#89"}), "quantity": FLASH_QUANTITY[drive], "notes": notes},
        "wiring": {
            "board": "CPU Board", "driver_transistor": row["Transistor"],
            "control_wire": wire(return_printed), "control_connection": f"PPB {return_pin.strip('()')}",
            "power_wire": "ORN", "power_connection": "PPB J6-4,5",
            "nominal_voltage_v": 32, "voltage_type": "dc",
        },
    }
    if drive in (1, 7):
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, SCRIPT_REF])
    else:
        entry["physical"]["notes"] += f" Not placed: {unplaced_reason(f'solenoid.{address}').split(': ', 1)[1]}."
    outputs.append(entry)

# --- 33-36: inert on this generation --------------------------------------------------------------------------------
for address in range(33, 37):
    outputs.append({
        "id": f"virtual.inert-{address}",
        "label": f"Inert Solenoid Address {address}",
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": (
            "core_getSol serves 33-36 only for the WPC and SAM generations (driver-specific flipper and game-on remaps); the lah_ game data is GEN_DEDMD32, so the address always reads 0."
        )},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- 37-39: PIA2 port B bits 0-2 on CN3, the three magnets ------------------------------------------------------------
MAGNET_PINS = SCHEM["magnet_pins"]
LATCH = SCHEM["latch"]
# public address -> (CN3 pin, board input pin, board output pin, MOSFET, gate resistor, latch stage)
MAGNETS = {
    37: ("CN3-9", "J1-6", "J2-4", "Q2", "R12", "2D/2Q"),
    38: ("CN3-8", "J1-7", "J2-3", "Q1", "R11", "1D/1Q"),
    39: ("CN3-7", "J1-8", "J2-7", "Q3", "R13", "8D/8Q"),
}
TABLE_MAGNETS = {37: ("LMagnet", "left", 204), 38: ("CMagnet", "center", 218), 39: ("RMagnet", "right", 211)}
MAGNET_SUBS = {37: ("SolLeftMagnet", 405, "764-770"), 38: ("SolCenterMagnet", 406, "756-762"), 39: ("SolRightMagnet", 407, "772-778")}
_magnet_counts = counts("Magnet Test: hold Start 2.5 s", TEST)
if set(_magnet_counts) != {37, 38, 39}:
    raise SystemExit(f"the Magnet Test must cycle exactly 37-39, not {_magnet_counts}")
if (ASSEMBLIES["22"]["Description"], ASSEMBLIES["22"]["Part No."]) != ("Magnet Coil (3)", "090-5042-00"):
    raise SystemExit("Major Assemblies item 22 must be the three magnet coils 090-5042-00")
CN3 = SCHEM["cn3"]
CN3_PINS = {int(row["Port line"].removeprefix("PB")): int(pin) for pin, row in CN3.items() if row["Port line"].startswith("PB")}
if CN3_PINS != {0: 9, 1: 8, 2: 7, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}:
    raise SystemExit(f"the CPU board sheet must draw PB0-PB7 on CN3 pins 9, 8, 7, 5, 4, 3, 2, 1, not {CN3_PINS}")
for address, (cn3, board_in, board_out, mosfet, resistor, stage) in MAGNETS.items():
    bit = address - 37
    if cn3 != f"CN3-{CN3_PINS[bit]}":
        raise SystemExit(f"magnet {address}: PB{bit} is on CN3 pin {CN3_PINS[bit]}, not {cn3}")
    in_row, out_row = MAGNET_PINS[board_in], MAGNET_PINS[board_out]
    if in_row["Other end"] != f"CPU {cn3}" or not out_row["Other end"].startswith("MAGNET "):
        raise SystemExit(f"magnet {address}: the Magnet Control Board sheet does not wire {board_in} to CPU {cn3} and {board_out} to a magnet")
    number = out_row["Other end"].removeprefix("MAGNET ")
    if in_row["Signal"] != f"INPUT {number}" or out_row["Signal"] != f"OUTPUT {number}":
        raise SystemExit(f"magnet {address}: board input and output numbers disagree")
    obj, side, line = TABLE_MAGNETS[address]
    sub, callback_line, sub_lines = MAGNET_SUBS[address]
    notes = (
        f"The game data sets S11_PRINTERLINE, so s11.c's pia2b_w publishes PIA2 port B bit {bit} here as the extSol bit that core_getSol reads at 37 + {bit}; the handler's "
        f"comment puts the bit on {cn3.replace('-', ' pin ')} (s11.c lines 392-410). The schematic book's Magnet Control Board connections (520-5068-00, printed page 70) "
        f"take {in_row['Wire']} from CPU {cn3} into {board_in} '{in_row['Signal']}' and bring '{out_row['Signal']}' out on {board_out} {out_row['Wire']} to "
        f"'{out_row['Other end']}'. The board's schematic (printed page 71) latches the input in its 74HCT273 U1 ({stage}) on the CLK edge (J1-9, BRN-WHT from CPU CN1-7; "
        f"CLR on J1-5, GRY-BLK from CPU CN2-1) and drives the {mosfet} P20N10 MOSFET through {resistor} 39K, whose drain is {board_out}; each drain has a 1N4934 diode to "
        "J2-1 '+V', which the connections sheet labels '+ 50VDC' (VIO-YEL from PPB J7-3). The sheet does not draw the magnet's other terminal, so no power wiring or "
        f"voltage is recorded. The CPU Board Logic Diagram (printed page 56) draws {cn3.replace('-', ' pin ')} as PB{bit} of the 6821 at 11B. The schematic does not show "
        "when the CPU clocks or clears the latch. PinMAME models neither. On its binary path it publishes, once per vertical blank, the last port value written before "
        "the interval OR-ed with every write during it (s11.c pia2b_w and lines 215 and 220), so a bit set before the boundary survives a later clearing write; on its "
        "modulated path it publishes the output's PWM state (core.c line 2497). A public level is therefore neither the CPU's instantaneous data line nor the latched "
        "magnet state, and the physical latch timing stays unresolved. Major Assemblies item 22 is 'Magnet Coil "
        "(3)', 090-5042-00, drawn three times across the centre of the playfield. The retained table approximates the board by holding its magnet on while the public "
        f"output is on: it binds SolCallback({address}) = {sub} (script lines {callback_line} and {sub_lines}), which turns its cvpmMagnet on the {obj} trigger on while "
        f"the solenoid is on (InitMagnet {obj}, 9, script line {line}); it calls it the {side} magnet. The schematic numbers the magnets by board output only and no "
        "retained page locates them. "
        f"ROM evidence (1.12 Magnet Test, 'rapidly cycles the 3 magnets ... as long as the start button is operated'): holding Start for 2.5 s turned the public addresses 38, 37 and "
        f"39 on in turn, board outputs 1, 2 and 3 in order, {_magnet_counts[address]} times for this one; these are public address transitions, not measured magnet "
        "timing."
    )
    if wire_note(in_row["Wire"], "the CPU line"):
        notes += " " + wire_note(in_row["Wire"], "the CPU line")
    entry = {
        "id": f"magnet.magnet-{number}",
        "label": f"Magnet {number}",
        "kind": "magnet",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.coil", address, "coil", LEGACY_COILS),
        "availability": "used",
        "provenance": prov("validated", [SCHEMATICS, MANUAL, CORE_C, S11_C, RUNTIME_SRC, SCRIPT_REF]),
        "physical": {"part_number": asm("22"), "notes": notes},
        "wiring": {
            "board": "Magnet Control Board", "driver_transistor": mosfet,
            "control_wire": wire(out_row["Wire"]), "control_connection": f"Magnet Control Board {board_out}",
        },
    }
    located = spatial_for(entry["id"], "effect", f"solenoid.{address}")
    if not located:
        raise SystemExit(f"magnet {address} has no retained placement")
    entry["spatial"] = located
    entry["physical"]["notes"] += (
        f" Placed on the retained table's {placed_objects(f'solenoid.{address}')}, the table's magnet; its position is the table's reading of the centre-of-playfield magnets."
    )
    outputs.append(entry)

# --- 40-44: PIA2 port B bits 3-7 on CN3 pins 5-1, with nothing retained on them ------------------------------------------------
_printer = FACTS["printer_interface"]
if _printer["transitioned_solenoids"] or _printer["transitions_37_44"]:
    raise SystemExit("the printer-interface run must leave every output untouched")
for address in range(40, 45):
    index = address - 37
    pin = CN3_PINS[index]
    printed = CN3[str(pin)]["Printed label"]
    outputs.append({
        "id": f"control.cn3-pin-{pin}",
        "label": f"CN3 Pin {pin} (Port B Bit {index})",
        "kind": "control_signal",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unknown",
        "provenance": prov("candidate", [CORE_C, S11_C, SCHEMATICS, RUNTIME_SRC]),
        "physical": {"notes": (
            f"The game data sets S11_PRINTERLINE, so s11.c's pia2b_w publishes PIA2 port B bit {index} here as the extSol bit that core_getSol reads at 37 + {index}; the "
            "handler's comment heads its list 'CN3 Printer Data Lines (Used by various games)'. The CPU Board Logic Diagram (schematic book printed page 56) draws PB"
            f"{index} of the 6821 at 11B on CN3 pin {pin}, "
            + (f"labelled '{printed}'" if printed != "(blank)" else "with no label")
            + " under the heading 'CN3 TO CON. CN1 (MAS DIS. BD)', which names the display-board connector rather than this game's load. On this machine bits 0-2 of the "
            "same port leave CN3 pins 9, 8 and 7 for the Magnet Control Board (public 37-39). ROM evidence (1.12): the line never changed in any retained run - the service "
            "tests, the Magnet Test, Adjustment 58 PRINTER INTERFACE with Start pressed ('PRESS START TO PRINT'), a game start and a game in play. No retained page of this "
            f"machine's manual or schematic book shows anything connected to CN3 pin {pin}, and failure to observe a change does not prove the line unused, so its "
            f"availability stays unknown, and so does what, if anything, it drives. Not placed: {unplaced_reason(f'solenoid.{address}')}."
        )},
    })

# --- 45-48: PinMAME's synthetic lower flipper outputs ---------------------------------------------------------------------
FLIPPERS = {
    45: ("Synthetic Lower Right Flipper Power", "right"), 46: ("Synthetic Lower Right Flipper Hold", "right"),
    47: ("Synthetic Lower Left Flipper Power", "left"), 48: ("Synthetic Lower Left Flipper Hold", "left"),
}
for address, (label, side) in FLIPPERS.items():
    row = _FLIPPER_ROWS[side]
    control_wire, control_connection = row["CPU to flipper switch"].split(" ", 1)
    power_wire, power_connection = row["Power line, Flip. PCB to coil"].split(" ", 1)
    notes = (
        "Not a CPU-driven output on this machine. The game data declares no FLIP_SOL, so core.c's core_updateSw synthesises these bits whenever the switched-solenoid enable "
        f"(public 23) is on and the corresponding cabinet button bit of PinMAME's flipper column is set: public {82 if side == 'right' else 84}, the same bit it copies into matrix "
        f"switch {64 if side == 'right' else 63}. Power and hold therefore assert and release together and are not independently controllable; a recreation must not model them as "
        f"two coils. The physical coil ({row['Coil type']}; the Flipper Solenoids table prints the assembly {row['Assembly']}, and Major Assemblies item "
        f"{'13 Flipper Right' if side == 'right' else '14 Flipper Left'} is {asm('13' if side == 'right' else '14')}) is driven from the S.S. Flipper P.C.B. (Cabinet Parts "
        f"item 25, {CABINET['25']['Part No.']}): the manual's Flipper Solenoids table prints the flipper ground '{row['CPU to flipper switch']}', the switch line "
        f"'{row['Flipper switch to Flip. PCB']}', the power line '{row['Power line, Flip. PCB to coil']}' and the board's power input '{row['Power input to Flip. PCB']}'."
    )
    if address in (46, 48):
        notes += (
            f" The retained table binds SolCallback({'sLRFlipper' if address == 46 else 'sLLFlipper'}) = {'SolRFlipper' if address == 46 else 'SolLFlipper'} "
            f"(script line {413 if address == 46 else 414}; core.vbs defines sLRFlipper = 46 and sLLFlipper = 48), which fires its flipper while the output is on "
            f"(the sub starts at script line {436 if address == 46 else 418})."
        )
    else:
        notes += f" The retained table binds nothing to {address}."
    outputs.append({
        "id": f"virtual.flipper-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases(
            "pinmame.solenoid", address, "coil", LEGACY_COILS,
            extra=([("pinmame.coil", str(address))] if address in (46, 48) else [])
            + ([("vpe-legacy.coil", LEGACY_COIL_NAMES[address])] if address in LEGACY_COIL_NAMES else []),
        ),
        "availability": "used",
        "provenance": prov("validated", [MANUAL, CORE_C, CORE_H, RUNTIME_SRC] + ([SCRIPT_REF, VPM_DE_LIBRARY_SOURCE] if address in (46, 48) else [])),
        "physical": {
            "part_number": row["Coil type"],
            "assembly_part_number": asm("13" if side == "right" else "14"),
            "notes": notes,
        },
        "wiring": {
            "board": "Flipper Board", "control_wire": control_wire, "control_connection": control_connection,
            "power_wire": power_wire, "power_connection": power_connection,
        },
        "spatial": not_applicable("virtual", [MANUAL, CORE_C]),
    })
for address, label, note in (
    (49, "Simulation Ball Shooter", "CORE_FIRSTSIMSOL is 49; a simulator slot, not machine hardware."),
    (50, "Reserved Solenoid 50", "The last address below CORE_FIRSTCUSTSOL (51); the lah_ game data declares no custom solenoid."),
):
    outputs.append({
        "id": f"virtual.reserved-{address}",
        "label": label,
        "kind": "virtual",
        "binding": {"group": "pinmame.output.solenoid", "device": address},
        "aliases": aliases("pinmame.solenoid", address),
        "availability": "unused",
        "provenance": prov("validated", [CORE_C]),
        "physical": {"notes": note},
        "spatial": not_applicable("virtual", [CORE_C]),
    })

# --- Lamps 1-64 ---------------------------------------------------------------------------------------------------------
LAMP_EXTRA_NOTES = {
    7: (
        "The lamp chart and the description list call it the Top Turbo Bumper, but the switch chart calls the third bumper's switch 34 the Bottom Turbo Bumper, the coil "
        "table calls its coil 18 the Center Turbo Bumper and the ROM names all three BOTTOM; lamps 6 and 8 are the left and right bumpers, so this is the third, lowest one, "
        "and the label follows the ROM."
    ),
    17: "One of the five CRANE letter inserts, C to E for lamps 17 to 21.",
    40: (
        "The description list prints '(2 Bulbs)' and the chart 'X2', and the Lamp Locations drawing (printed page 31) prints 40 at the top of the left and of the right "
        "return lane, so the lamp drives two bulbs."
    ),
    43: (
        "The description list prints '(2 Bulbs)' and the chart 'X2', and the Lamp Locations drawing (printed page 31) prints 43 beside the left and the right outlane, so "
        "the lamp drives two bulbs."
    ),
    52: "Cells 52, 53, 54 and 56 print a bar of four boxes above 'Middle Scoop' with a dot in box 1, 2, 3 and 4: four positions of one row of inserts.",
    57: (
        "The Lamp Locations drawing (printed page 31) prints 57 once, without an insert outline, at the right side of the apron opposite the RIPPER letters 58-63 on "
        "its left side; IPDB says the Ripper and Smart Missile caps are on the card holder, and the retained table's Light L57 sits on its right apron too. The table also "
        "fades its cabinet Smart Missile button primitive PinCab_Smart with the lamp (Lampz.Callback(57), script line 3907); no retained page says whether the lamp also "
        "lights the button, and the socket's exact position on the apron is not measured. The ROM's "
        "lamp test names it SMART MISSILE X2 where the chart and the description list print no bulb count, so no quantity is recorded."
    ),
    58: "One of the six RIPPER letter inserts, lamps 58 to 63; IPDB puts the Ripper caps on the card holder, and the retained table's Lights sit on its left apron.",
    64: "A cabinet lamp: it lights the Credit (Start) button, and the retained table fades only its cabinet primitive PinCab_Start with it (Lampz.Callback(64), script line 3908).",
}
# Lamps 31 and 32: which address the right captive-ball insert is wired to. A game in play closed each captive-ball and return-lane switch in turn.
CAPTIVE_STEPS = FACTS["captive_lamps"]
if [step["switch"] for step in CAPTIVE_STEPS] != [41, 42, 40, 56, 39, 55] or any(
    step["lamp_31_changes"] < 1 or step["lamp_32_changes"] or 32 in step["lamps_changed"] for step in CAPTIVE_STEPS
):
    raise SystemExit("the captive-lamps run must change lamp 31 and never lamp 32 for each of switches 41, 42, 40, 56, 39 and 55")
_captive_counts = sorted(step["lamp_31_changes"] for step in CAPTIVE_STEPS)
CAPTIVE_ROM = (
    "ROM evidence (1.12, a game in play): closing the return lanes 41 and 42, the captive targets 40 and 56 and the captive rollovers 39 and 55 one at a time changed "
    f"public lamp 31 in every step ({_captive_counts[0]} to {_captive_counts[-1]} transitions) and never changed 32."
)
LAMP_EXTRA_NOTES[31] = (
    "The Lamp Locations drawing (manual printed page 31) prints 31 twice, in a box at the left captive-ball area beside 33 and 37 and in a box at the right one below 35, "
    "and the ROM's lamp test names it 'CAPTIVE BALLS X2'; the record follows them with two bulbs. The schematic book's Playfield Lamp Wiring Diagram (printed page 53) "
    "names 31 'Left Captive Ball' and 32 'Right Captive Ball' instead. The manual's rule text (printed page 4) says the left return lane lights the right captive ball "
    "and the right return lane the left one, each 'for a time period to score 2 captive ball hits'. " + CAPTIVE_ROM + " So this firmware drives the indication of both "
    "captive balls through 31. The retained table fades both captive-ball light-map sets, Inserts_l31 and Inserts_l31b, with live Lampz.Callback(31) lines (script lines "
    "4772-4786). Which address a production harness wires the right captive-ball insert to is recorded as a conflict."
)
LAMP_EXTRA_NOTES[32] = (
    "The schematic book's Playfield Lamp Wiring Diagram (printed page 53) names it 'Right Captive Ball', where the chart, the description list and the ROM's lamp test "
    "(TICKET) do not. The Lamp Locations drawing (manual printed page 31) prints 32 once, in the open centre of the playfield below 39, 41 and 42, with no insert outline "
    "around it, and the retained table's Light L32 sits there too (Lampz.MassAssign(32) = l32, script line 4787). " + CAPTIVE_ROM + " Which address a production harness "
    "wires the right captive-ball insert to is recorded as a conflict."
)
for _address in (18, 19, 20, 21):
    LAMP_EXTRA_NOTES[_address] = LAMP_EXTRA_NOTES[17]
for _address in (53, 54, 56):
    LAMP_EXTRA_NOTES[_address] = LAMP_EXTRA_NOTES[52]
for _address in (59, 60, 61, 62, 63):
    LAMP_EXTRA_NOTES[_address] = LAMP_EXTRA_NOTES[58]
CAPTIVE_LAMPS = (31, 32)
for address in range(1, 65):
    chart = LAMP["chart"][address]
    described = LAMP["descriptions"][address]
    sheet = SCHEM["lamps"][address]
    suffix, label = sem.LAMPS[address]
    rom = ROM_LAMP[str(address)]
    drive_wire = re.sub(r"-\s+", "-", chart["drive"]["wire"])
    notes = [
        f"Printed lamp-matrix column {chart['column']}, row {chart['row']}; "
        + (
            f"the chart and the Lamp Number / Description list print '{described}'" if chart["printed"] == described else
            f"the chart prints '{chart['printed']}' and the Lamp Number / Description list '{described}'"
        )
        + (f", and the schematic book's lamp sheet '{sheet}'." if sheet != described else ".")
    ]
    if address in LAMP_EXTRA_NOTES:
        notes.append(LAMP_EXTRA_NOTES[address])
    notes.append(
        f"ROM evidence (1.12 Lamp Test): the single-lamp test turns on public lamp address {address} alone, under '{rom['name']}', wires {rom['wires']} and "
        f"'#{address:02d}'; it cannot show how many bulbs the address drives."
    )
    entry = {
        "id": f"lamp.{suffix}",
        "label": label,
        "kind": "lamp",
        "binding": {"group": "pinmame.output.lamp", "device": address},
        "aliases": aliases("pinmame.lamp", address, "lamp", LEGACY_LAMPS),
        "availability": "used",
        "provenance": prov("conflicted" if address in CAPTIVE_LAMPS else "validated", [MANUAL, SCHEMATICS, CORE_C, S11_C, RUNTIME_SRC]),
        "physical": {"notes": ""},
        "wiring": {
            "board": "CPU Board",
            "driver_transistor": chart["drive"]["transistor"],
            "drive_wire": drive_wire,
            "drive_connection": chart["drive"]["connector"],
            "return_wire": chart["return"]["wire"],
            "return_connection": chart["return"]["connector"],
            "return_component": chart["return"]["transistor"],
        },
    }
    if address in sem.LAMP_BULBS:
        entry["physical"]["quantity"] = sem.LAMP_BULBS[address]
    if address in sem.CABINET_LAMPS:
        entry["roles"] = [sem.CABINET_LAMPS[address]]
        entry["spatial"] = not_applicable("cabinet_or_service", [MANUAL, SCRIPT_REF])
    else:
        if spatial_for(entry["id"], "emitter", f"lamp.{address}"):
            raise SystemExit(f"lamp {address}: the places file places a matrix lamp, which needs a physical anchor this curator does not describe")
        entry["provenance"]["source_refs"].append(SCRIPT_REF)
        notes.append(f"Not placed: {unplaced_reason(f'lamp.{address}')}.")
    entry["physical"]["notes"] = " ".join(notes)
    outputs.append(entry)

# --- ROM evidence on the outputs ------------------------------------------------------------------------------------------
ACTIONS_BY_OUTPUT: dict[int, list[str]] = {}
for _entry in FACTS["test_actions"]:
    for _number in _entry["outputs"]:
        ACTIONS_BY_OUTPUT.setdefault(_number, []).append(_entry["label"])


def rom_output_note(address: int) -> str | None:
    """The ROM's own name, the Cycling Coils step and the dedicated tests' response for one public solenoid address."""
    sentences = []
    if address in CYCLE_STEPS:
        relay = ", with the relay at 10 turned on just before it" if CYCLE[CYCLE.index(address) - 1] == 10 else ""
        sentences.append(
            f"ROM evidence (1.12 Cycling Coils): the automatic test names public {address} '{ROM_COIL[address]}' and fires it as step {CYCLE_STEPS.index(address) + 1} of its "
            f"{len(CYCLE_STEPS)}-step cycle{relay}."
        )
    if address == 10:
        _OVERLAP = FACTS["cycling_left_coil_relay_overlap"]
        sentences.append(
            "ROM evidence (1.12 Cycling Coils): the test has no step of its own for 10; it turns 10 on before each of 25-32 and off again as it fires each left "
            "coil 1-8. PinMAME picks the left or right set from the relay's state at the moment the CPU writes the drives (s11.c updsol, lines 558-573), while "
            "it publishes the binary outputs once per vertical blank, so the published stream can show a left coil and 10 on together. Of the run's "
            f"{_OVERLAP['left_coil_rises']} left-coil rises, {_OVERLAP['same_update']} published the fall of 10 in the same update and {_OVERLAP['trailing']} "
            f"one vertical blank later ({_OVERLAP['min_trail_ms']}-{_OVERLAP['max_trail_ms']} ms); at the rest 10 was already off."
        )
    for label in ACTIONS_BY_OUTPUT.get(address, []):
        if address in (22, 37, 38, 39):
            continue
        sentences.append(f"In the {label.split(': ', 1)[0]} ('{label.split(': ', 1)[1]}') the ROM fired public {address}.")
    return " ".join(sentences) or None


for entry in outputs:
    group, address = entry["binding"]["group"], entry["binding"]["device"]
    if group == "pinmame.output.solenoid":
        note = rom_output_note(address)
        if note:
            entry["physical"]["notes"] += " " + note
            if RUNTIME_SRC not in entry["provenance"]["source_refs"]:
                entry["provenance"]["source_refs"].append(RUNTIME_SRC)

# --- Displays -----------------------------------------------------------------------------------------------------------
displays = [{
    "id": "display.dmd",
    "label": "128x32 Dot Matrix Display",
    "kind": "dmd",
    "controller_index": 0,
    "width": 128,
    "height": 32,
    "physical_location": "cabinet_or_service",
    "provenance": prov("validated", [CORE, MANUAL, RUNTIME_SRC]),
    "spatial": not_applicable("cabinet_or_service", [CORE, MANUAL]),
}]

# --- Mechanisms -------------------------------------------------------------------------------------------------------------
MECH_REFS = [MANUAL, SCRIPT_REF]
_start = counts("Trough: press Start with 15 empty", SERVE)
_release = counts("Trough: a ball reaches the release position 15", SERVE)
_shooter = counts("Trough: the ball rests in the shooter lane 16", SERVE)
_launch = counts("Trough: pull the launch trigger 8 with the ball on 16", SERVE)
if _start.get(1) is None or _release.get(2) is None or _launch.get(3) != 1 or 3 in _shooter:
    raise SystemExit("the trough-serve run must pulse the lockout after Start, the release once a ball reaches 15 and the launcher only from the trigger")
if counts("Crane Test: close public switch 8 (launch trigger)", TEST) != {4: 1} or counts("Crane Test: hold Start 3 s", TEST) != {14: 1}:
    raise SystemExit("the Crane Test must run the motor from Start and fire the crane lock from the trigger")
_levels = FACTS["crane_motor_levels"]
_crane = FACTS["crane_motor_timing"]
mechanisms = [
    {
        "id": "mechanism.trough",
        "label": "Six-Ball Trough, Lockout and Ball Release",
        "kind": "kicker",
        "actuators": ["coil.trough-lockout", "coil.ball-release"],
        "sensors": [f"switch.{sem.SWITCHES[a][0]}" for a in range(9, 17)],
        "assembly_part_number": asm("10"),
        "behavior": (
            f"The 6 Ball Switch Assy. ({asm('10')}) holds up to six balls on trough switches 9 (left, the drain end) to 14; the lockout coil on drive 1 (25-1240, the "
            "schematic's '6 Ball Ass'y Lockout') moves the ball at 14 into the release position 15 (Trough #7, typed 180-5118-00 against 180-5119-00 for 9-14), and the Ball "
            "Release on drive 2 (23-800) kicks it from 15 into the shooter lane, where switch 16 senses it. ROM evidence (1.12 game start, the host moving the balls): with "
            f"balls on 9-14 and 15 empty, Start pulsed the lockout {_start[1]} times; once a ball reached 15 the ROM pulsed the release {_release[2]} times while 15 stayed "
            "closed. The host moved every ball, so the counts are the ROM's retries, not travel times. The schematic book's Trough Assembly page (printed page 75) draws the "
            "6 Ball Switch Assembly 500-5683-01 with six subminiature switches (180-5119-00; its parts table prints 12) in a row under the sloped outhole bracket and one "
            "miniature switch (180-5118-00) on its switch bracket beside the top of the release coil (23-800), which stands vertically under the low end of the row with its "
            "plunger and spring; above it the page draws the Lock Ball Assembly 500-5684-01, its 25-1240 coil laid horizontally with the plunger, spring and link at one end "
            "and a lock-ball cam below the link. The page does not say which way either plunger moves. The retained table rests its balls on trough kickers sw9-sw14 that "
            "roll them towards sw14 (UpdateTroughTimer, script lines 1089-1101), and its SolTrough and SolRelease kick sw14 into sw15 and sw15 into the shooter lane (lines "
            "1108-1121)."
        ),
        "provenance": prov("validated", MECH_REFS + [SCHEMATICS, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.auto-launch",
        "label": "Auto Launch (Shooter Gun)",
        "kind": "kicker",
        "actuators": ["coil.ball-launch"],
        "sensors": ["switch.shooter-lane", "switch.launch-trigger"],
        "assembly_part_number": asm("5"),
        "behavior": (
            f"The Ball Launch Assy ({asm('5')}) on drive 3, 23-800 through the PPB booster Q5 and named '{ROM_COIL[3]}' by the ROM, launches the ball resting on the shooter "
            f"lane switch 16. The cabinet's Shooter Gun Assy. (Cabinet Parts item 1, {CABINET['1']['Part No.']}) carries the launch trigger 8. ROM evidence (1.12 game start): "
            "with the ball on 16 the ROM did not fire 3 until the trigger 8 closed, then fired it once, about "
            f"{FACTS['launch_delay_s']} s later on the host clock; the Laser Kick Test also fires 3 when 16 closes. The retained table fires a cvpmImpulseP plunger on its "
            "swPlunger trigger (script lines 1127-1143)."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.crane",
        "label": "Crane",
        "kind": "motorized",
        "actuators": ["motor.crane", "coil.crane-lock"],
        "sensors": ["switch.crane-left-limit", "switch.crane-right-limit"],
        "assembly_part_number": asm("16"),
        "behavior": (
            f"The Crane Assy. ({asm('16')}, drawn at the upper left inside the arc of the left orbit with the Crane Motor {asm('1')}) carries a cab and boom on a vertical shaft "
            "turned by the motor under the playfield (schematic book printed page 76). The Crane Test text: the motor rotates in one direction only, a cam on it sweeps the "
            "crane arm through an arc of 145 degrees and back, the two limit switches 60 and 61 report the ends of the sweep, and the trigger switch pulses 'the ball release "
            "coil on the crane mechanism', the crane lock 4, whose coil assembly (515-5889-00) rides under the boom at the cab end. The cab carries two No. 89 lamps of flash "
            "drive 9. IPDB: a motorized crane target moves the ball from one ramp to another. ROM evidence (1.12 Crane Test): holding Start ran 14; the trigger 8 fired 4 once; "
            "the screen showed 'LEFT CRANE SW: ON' while 60 was held and 'RIGHT CRANE SW: ON' while 61 was held, and neither limit nor the Smart Missile button 62 fired "
            f"anything. At game start, with neither limit switch ever closed, the ROM ran 14 from {_levels[0]['time_s']} s, dropped it "
            f"{_crane['drop_after_start_s']:.2f} s after the Start press for {_crane['dropout_ms']} ms and ran it until {_crane['off_after_shooter_lane_s']:.2f} s "
            "after the ball left the shooter lane, so the run shows only that the "
            "ROM drives the motor for long stretches when no limit closes, not where it normally stops it. How a ball gets onto the boom and off it is known only from the "
            "retained table: at the right limit it enables a kicker at the end of one ramp that drops the ball into a kicker on the boom, the ball rides the boom, and its "
            "SolCraneLock kicks it off at the falling edge of 4 while the left limit 60 is closed (script lines 653-747). The table models a reversing motor that sweeps 130 "
            "degrees and waits at each end, not a cam, and whether the physical coil holds the ball while energised or releases it is not printed. No run closed a limit "
            "switch while 14 was on (in the Crane Test both limit pulses ended before Start ran the motor), so whether the ROM stops the motor at a limit is unobserved."
        ),
        "provenance": prov("candidate", MECH_REFS + [SCHEMATICS, IPDB, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.ripper-kickback",
        "label": "Ripper Kickback",
        "kind": "kicker",
        "actuators": ["coil.ripper-kickback"],
        "sensors": ["switch.ripper-kickback"],
        "assembly_part_number": asm("2"),
        "behavior": (
            f"The Kick Back Assy ({asm('2')}, drawn on the right wall at the upper right) on switched solenoid 22, 23-800 on the 50 V VIO-YEL supply and named "
            f"'{ROM_COIL[22]}' by the ROM, kicks the ball out of the Ripper pit sensed by switch 48. IPDB: the Ripper target returns the ball at fast speed when hit. ROM "
            "evidence (1.12 Laser Kick Test, '>FEED BALL TO RIPPER<'): closing 48 fires 22 once, whether 48 is held 400 ms or 1.5 s, and closing the left outlane 43 fires "
            "nothing (the manual's Laser Kick paragraph names a left-outlane kick that reads as text shared with other Data East manuals). The retained table kicks its Sw48 "
            "kicker on 22 (script lines 593-602)."
        ),
        "provenance": prov("validated", MECH_REFS + [IPDB, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.vuk",
        "label": "VUK (Top Right Corner)",
        "kind": "kicker",
        "actuators": ["coil.vuk"],
        "sensors": ["switch.vuk"],
        "assembly_part_number": asm("11"),
        "behavior": (
            f"The VUK Assy. ({asm('11')}, drawn hatched at the top right corner) on drive 5, 23-800 through the PPB booster Q4 and named '{ROM_COIL[5]}' by the ROM, raises the "
            f"ball from switch 47 onto the VUK Ramp ({asm('26')}). ROM evidence (1.12 Laser Kick Test): closing 47 fires 5. The retained table kicks its bsVuk saucer on the "
            "Sw47 kicker (script lines 184-190 and 1050)."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.right-scoop",
        "label": "Right Scoop",
        "kind": "kicker",
        "actuators": ["coil.right-scoop"],
        "sensors": ["switch.right-scoop"],
        "behavior": (
            "The Right Scoop Ass'y on drive 6, 23-800 through the PPB booster Q3, kicks the ball out of the right scoop sensed by switch 31 (Right Scoop Assembly, 500-5057-00). "
            "ROM evidence (1.12 Laser Kick Test): closing 31 fires 6. In the retained table the right wire ramp, entered over the Right Scoop Rollover 38, ends in the scoop; "
            "that routing is the table's model."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.middle-scoop",
        "label": "Middle Scoop",
        "kind": "kicker",
        "actuators": ["coil.middle-scoop"],
        "sensors": [f"switch.{sem.SWITCHES[57][0]}", f"switch.{sem.SWITCHES[58][0]}"],
        "behavior": (
            f"The middle scoop coil on drive 15 (23-800) kicks the ball out of the scoop sensed by switch 57 (Middle Scoop Left); the switch chart (printed page 29) names "
            "58 Middle Scoop Right, the scoop's second switch. Major Assemblies item 19 (Double Scoop, "
            f"{asm('19')}) is drawn above the centre between two scoop assemblies. ROM evidence (1.12 Laser Kick Test): closing 57 fires 15, while closing the Middle Scoop "
            "Right switch 58 fires nothing, so only 57 produced a transition on drive 15 there; the retained table pulses 58 from a subway switch that does not hold the ball. Four lamps 52-54 and 56 form one row of Middle "
            "Scoop inserts."
        ),
        "provenance": prov("validated", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.ball-lock",
        "label": "Left Ball Lock",
        "kind": "gate",
        "actuators": ["coil.ball-lock"],
        "sensors": ["switch.left-lock-top", "switch.left-lock-bottom"],
        "assembly_part_number": asm("17"),
        "behavior": (
            f"The Lock Ball Assy. ({asm('17')}, drawn on the left side in the hatched lock area) on drive 7 (27-1400 in the coil table and on the wiring sheet, named "
            f"'{ROM_COIL[7]}' by the ROM) releases balls held in the left lock, sensed at 22 (top) and 23 (bottom). The schematic book's Ball Lock Assembly drawing of the "
            f"same part number (printed page 73) shows a vertical coil ({SHEET_ASM['ball_lock']['11']['Description']}) whose lock-ball plunger stands up out of its top "
            "bracket with a spring around it, and two actuator switches (180-5128-00, the part the switch table types for 22 and 23) beside the plunger with their arms "
            "reaching over the top. It draws no ball and does not say which way the plunger moves when the coil is energised, so whether the energised coil withdraws the "
            "plunger to release the balls is not printed. ROM evidence (1.12): in the game-start run 7 was the first solenoid the ROM switched on "
            f"({SERVE_ORDER[0]} first) once the outputs the attract and game-start lamp shows drive by themselves (9, 10, 11, 23 and 25-32) are left out, as the run's note "
            "says; the G.I. relay 11 had already switched. The Laser Kick Test fires nothing from 22 or 23. The retained table drops a post wall when 7 turns on and restores "
            "it after a timer (SolLockRelease, LockReleaseTimer, script lines 535-547)."
        ),
        "provenance": prov("candidate", MECH_REFS + [SCHEMATICS, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.drop-targets",
        "label": "Five-Bank Drop Targets (CRANE)",
        "kind": "drop_target_bank",
        "actuators": ["coil.drop-target-reset"],
        "sensors": [f"switch.{sem.SWITCHES[a][0]}" for a in range(17, 22)] + [f"switch.{sem.SWITCHES[54][0]}"],
        "assembly_part_number": asm("6"),
        "behavior": (
            f"The 5 Bank Drop Target ({asm('6')}) on the left side of the playfield: targets C, R, A, N and E on switches 17 (bottom) to 21 (top), as the ROM names them, reset "
            "together by drive 13 (23-800 on the operator manual's coil-driver drawing, the only drive table that prints its winding; the wiring sheet labels it 'DROP "
            "TARGET' without one), with the CRANE letter lamps 17-21. The schematic book's 5-Bank Drop Target Assembly "
            f"drawing (printed page 74, part 500-5621-05, 'ADJUSTABLE') lists a '{SHEET_ASM['drop_targets']['11']['Description']}' "
            f"({SHEET_ASM['drop_targets']['11']['Part #']}), a plunger/link assembly, a target lift bracket, a target reset spring and a switch assembly "
            f"({SHEET_ASM['drop_targets']['20']['Part #']}), and prints '*QUANTITY IS DESIGNATED BY BANK SIZE' under its table. Switch 54, the Drop Target Bar (printed "
            "'(2)', the ROM's X2), is the DANGER bar behind the bank: the manual's rule text (printed page 4) warns that 'hitting the DANGER bar behind the drop targets "
            "will reset the drop target bank', so the game, not a linkage, resets the bank through drive 13 when 54 closes. No retained page draws the bar, and no "
            "retained run closed 54 or exercised a reset in a game. The retained table pulses 54 from its sw54 target beside the bank and raises all five targets on 13 "
            "(script lines 501-511)."
        ),
        "positions": [
            {"id": f"mechanism.drop-targets.{sem.SWITCHES[a][0].removeprefix('drop-target-')}", "label": sem.SWITCHES[a][1], "sensors": [f"switch.{sem.SWITCHES[a][0]}"]}
            for a in range(17, 22)
        ],
        "provenance": prov("observed", MECH_REFS + [SCHEMATICS, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.ramp-diverter",
        "label": "Ramp Diverter",
        "kind": "diverter",
        "actuators": ["coil.ramp-diverter"],
        "sensors": [],
        "assembly_part_number": asm("24"),
        "behavior": (
            f"The Diverter ({asm('24')}, drawn on the left ramp entry) on drive 12 (27-1400). No switch reports its position, and no retained run exercised it in a game. The "
            "retained table swings its diverter open while 12 is on and back when it turns off."
        ),
        "provenance": prov("observed", MECH_REFS),
    },
    {
        "id": "mechanism.magnets",
        "label": "Playfield Magnets",
        "kind": "other",
        "actuators": ["magnet.magnet-1", "magnet.magnet-2", "magnet.magnet-3"],
        "sensors": [],
        "behavior": (
            f"Three Magnet Coils ({asm('22')}) across the centre of the playfield on the 50 V supply. Hardware: the Magnet Control Board (520-5068-00, schematic book printed "
            "pages 70-71) takes the CPU's PIA2 port B lines PB0-PB2 from CN3 pins 9, 8 and 7 into a 74HCT273, which latches them on the clock edge from CPU CN1-7 and is "
            "cleared from CPU CN2-1; each latched output gates a P20N10 MOSFET that grounds one magnet. The schematic book does not show when the CPU clocks or clears the "
            "latch. Emulator: PinMAME models neither the clock nor the clear; once per vertical blank it publishes at 37-39 the last port B value written before the "
            "interval OR-ed with every write during it (or, on its modulated path, the PWM state), so a public level is neither the CPU's instantaneous data line nor "
            "the latched magnet state, and the physical latch timing stays unresolved. Table: the retained table approximates the board by holding each cvpmMagnet on "
            "while its public output is on; it puts 37 on the left, 38 in the centre below them and 39 on the right, and no retained page says where each magnet is. The "
            "Magnet Test 'rapidly cycles the 3 magnets ... as long as the start button is operated' and the manual warns not to run it more than a few seconds because of the "
            "high current; the 1.12 ROM turned the public addresses 38, 37 and 39 on in turn, which the board's wiring makes outputs 1, 2 and 3; "
            "those are public address transitions, not magnet timing."
        ),
        "provenance": prov("observed", [SCHEMATICS, MANUAL, S11_C, SCRIPT_REF, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.turbo-bumpers",
        "label": "Turbo Bumpers",
        "kind": "other",
        "actuators": ["coil.left-turbo-bumper", "coil.center-turbo-bumper", "coil.right-turbo-bumper"],
        "sensors": ["switch.left-turbo-bumper", "switch.bottom-turbo-bumper", "switch.right-turbo-bumper"],
        "assembly_part_number": asm("4"),
        "behavior": (
            f"Three Turbo Bumper Assys ({asm('4')}) in the upper right quarter, sensed at 33-35 (180-5015-01) and fired by switched solenoids 17-19 (23-800), with lamps 6-8. "
            "The third bumper sits below the left and right ones; the manual's tables call it Bottom (switch 34), Center (coil 18) and Top (lamp 7), and the ROM BOTTOM for all "
            "three. No retained run paired a bumper switch with its coil in a game; the retained table lets its VPX bumpers kick on contact."
        ),
        "positions": [
            {"id": "mechanism.turbo-bumpers.left", "label": "Left Turbo Bumper", "sensors": ["switch.left-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.bottom", "label": "Bottom (Center) Turbo Bumper", "sensors": ["switch.bottom-turbo-bumper"]},
            {"id": "mechanism.turbo-bumpers.right", "label": "Right Turbo Bumper", "sensors": ["switch.right-turbo-bumper"]},
        ],
        "provenance": prov("observed", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.slingshots",
        "label": "Slingshots",
        "kind": "other",
        "actuators": ["coil.left-slingshot", "coil.right-slingshot"],
        "sensors": ["switch.left-slingshot", "switch.right-slingshot"],
        "assembly_part_number": asm("3"),
        "behavior": (
            f"Two Slingshot Assys ({asm('3')}) sensed at 36 and 37 (180-5054-00) and fired by switched solenoids 20 and 21 (23-800). No retained run paired a slingshot switch "
            "with its coil in a game; the retained table lets its VPX slingshots kick on contact."
        ),
        "provenance": prov("observed", MECH_REFS + [RUNTIME_SRC]),
    },
    {
        "id": "mechanism.captive-balls",
        "label": "Captive Balls",
        "kind": "other",
        "actuators": [],
        "sensors": ["switch.left-captive-rollover", "switch.left-captive-target", "switch.right-captive-rollover", "switch.right-captive-target"],
        "behavior": (
            "Two captive-ball lanes, each with a rollover and a target: left (39, 40) and right (55, 56). Neither lane has a coil. The manual's rule text (printed page 4) "
            "says each captive-ball shot advances the M-BALL countdown by one, and that the left return lane lights the right captive ball and the right return lane the left "
            "one 'for a time period to score 2 captive ball hits'. " + CAPTIVE_ROM + " The Lamp Locations drawing prints 31 at both captive-ball inserts, while the "
            "schematic book's lamp sheet names lamps 31 and 32 Left and Right Captive Ball; that disagreement is recorded as a conflict on lamp 31."
        ),
        "provenance": prov("observed", [MANUAL, SCHEMATICS, SCRIPT_REF, RUNTIME_SRC]),
    },
    {
        "id": "mechanism.shaker",
        "label": "Cabinet Shaker Motor",
        "kind": "motorized",
        "actuators": ["motor.shaker"],
        "sensors": [],
        "behavior": (
            f"The Shaker Motor ({CABINET['34']['Part No.']}) inside the cabinet, run by its Shaker Motor P.C. Board ({CABINET['35']['Part No.']}) from drive 16. ROM evidence "
            f"(1.12 game start): the ROM switched 16 on {_start[16]} times after Start, {_release[16]} times as the ball reached the release position and {_shooter[16]} times "
            "while it rested in the shooter lane. The retained table does not model it."
        ),
        "provenance": prov("observed", [MANUAL, RUNTIME_SRC]),
    },
]
relationships = [
    {
        "id": f"relationship.left-right-relay-{drive}",
        "kind": "relay_gated",
        "source": "relay.left-right-relay",
        "destination": f"flasher.{drive}r",
        "provenance": prov("validated", [MANUAL, CORE, S11_C, RUNTIME_SRC]),
    }
    for drive in range(1, 9)
] + flipper_column_relationships(
    flip_swno=FLIP_SWNO, matrix_ids={63: "switch.left-flipper-copy", 64: "switch.right-flipper-copy"}, refs=(CORE_C, CORE_H),
)

conflicts: list[dict] = [
    {
        "id": "conflict.flash-lamps-8r-quantity",
        "path": "outputs.flasher.8r",
        "description": (
            "Both wiring drawings count four lamps on flash group 8R: the operator manual's coil-driver drawing (printed page 33) prints '(2) LOW LEFT PLFD (2) INSERT "
            "(4) 89' and the schematic book's wiring sheet (printed page 50) '(2) PLFD (2) INSERT (4) NO.89'. The operator manual's Flash Lamp / Coil Tests location "
            "drawing (printed page 32) prints one 8R callout on the playfield and its Backbox Flash Lamps drawing two 8R sockets, three in all. The 1.12 ROM names the "
            "drive '2-INS 1-TAR PIT' and the retained table comments it 'Flash Playfield Low Left + Backbox Insert(x2)', but a name and a comment describe the group "
            "without counting its bulbs. The record keeps three as the working quantity. Resolution path: on a production machine, select 8R in the Select Coil test "
            "and count the lamps that light on the lower left of the playfield and in the backbox insert, or count the 8R sockets on its harness; an owner of the "
            "machine could do it."
        ),
        "source_refs": [MANUAL, SCHEMATICS, RUNTIME_SRC, SCRIPT_REF],
        "status": "unresolved",
    },
    {
        "id": "conflict.right-captive-ball-lamp",
        "path": "outputs.lamp.captive-balls-x2",
        "description": (
            "The operator manual prints lamp 31 'Captive Ball X2' and lamp 32 'Ticket' in its Lamp Matrix Chart and description list, and its Lamp Locations drawing "
            "(printed pages 30-31) prints 31 at both captive-ball inserts and 32 alone in the open centre of the playfield; the schematic book's Playfield Lamp Wiring "
            "Diagram (printed page 53) names 31 'Left Captive Ball' and 32 'Right Captive Ball'. The 1.12 ROM names 31 'CAPTIVE BALLS X2' and 32 'TICKET', drives 31 "
            "and never 32 while the captive-ball and return-lane switches close in a game, and the retained table fades both captive-ball inserts with 31; the record "
            "follows them, but none of them shows a production harness. Resolution path: run the single-lamp test on lamp 32 of a production machine, or trace the right "
            "captive-ball insert's socket wires to their lamp-matrix row and column, and see whether that insert lights on 32 or on 31; an owner of the machine could do it."
        ),
        "source_refs": [MANUAL, SCHEMATICS, RUNTIME_SRC, SCRIPT_REF],
        "status": "unresolved",
    },
    {
        "id": "conflict.flash-drive-9-supply",
        "path": "outputs.flasher.crane-and-insert",
        "description": (
            "The operator manual's coil-driver drawing (printed page 33) returns the common of drive 9's four No. 89 lamps (two in the crane cab, two in the "
            "backbox insert) to power-supply connector CN3 pin 6, an unswitched +32 V. The schematic book's wiring sheet (printed page 50) draws the same four "
            "lamps on '+32 VDCR PPBJ6-4/5', the ORG supply of the right-set flash groups 25-32, which the Left/Right relay 10 switches on only while it is "
            "energised (printed page 32). On the first drawing 9 lights its lamps whatever 10's state; on the second only while 10 is on. The 1.12 ROM had 10 "
            f"on at every one of the {DRIVE_9['rises']} times 9 turned on in the {DRIVE_9['runs']} retained runs, so the runs cannot tell the two apart, and PinMAME publishes 9 "
            "whatever 10's state. The record keeps the public binding at 9 and records neither supply nor a relay relationship. Resolution path: with the "
            "power off, check whether the common wire of the crane-cab or backbox-insert drive-9 sockets is continuous with PPB connector J6 pins 4-5 or with "
            "power-supply connector CN3 pin 6, or fire 9 in the Select Coil test with the relay released and see whether the lamps light; an owner of a "
            "production machine could do it."
        ),
        "source_refs": [MANUAL, SCHEMATICS, RUNTIME_SRC, S11_C],
        "status": "unresolved",
    },
]

# --- Drivers --------------------------------------------------------------------------------------------------------------
_root = ROM_SETS[ROOT_DRIVER]
drivers = []
for driver_id in sorted(ROM_SETS):
    roms = ROM_SETS[driver_id]
    if driver_id == ROOT_DRIVER:
        note = (
            "Clone-tree root (1.12, display ROM lahdispa.106). Every lah_ set shares one game-data block (INITGAMES11(lah, GEN_DEDMD32, de_128x32DMD, FLIP6364, SNDBRD_DE2S, "
            "SNDBRD_DEDMD32, S11_PRINTERLINE), muxSol 10) and the three sound ROMs, so all nine present identical playfield hardware and identical public addresses. Every "
            "harness run used it; its service screens read US English 1.12."
        )
    else:
        differing = [(role, mine) for role, mine, theirs in zip(ROLES, roms, _root) if mine != theirs]
        note = ("Differs from the root in " + ", ".join(f"the {role} ROM ({rom})" for role, rom in differing) + ".") if differing else "Byte-identical ROM set to the root."
        note += " The shared game data means the address model is unchanged."
        if driver_id in ("lah_f104", "lah_l104", "lah_l108"):
            note += " A language firmware for the same hardware (" + DRIVER_LABELS[driver_id].split("(", 1)[1].rstrip(")") + ")."
        if driver_id == "lah_c106":
            note += " Labelled Canadian, with its own CPU ROM lahcpuc.106: a regional firmware for the same hardware."
        if driver_id in ("lah_107", "lah_110"):
            note += " An earlier factory revision."
        if driver_id == "lah_l108_105":
            note += (
                " PinMAME marks its CPU ROM NO_DUMP and comments that the Spanish display ROM 1.05 is parked here because it is not known where it belongs and displays "
                "nothing with any known CPU ROM, so the set does not run; it stays grouped with the machine it was dumped from, and its physical compatibility is "
                "unknown until a working pairing of that display ROM with a CPU ROM on this hardware is shown."
            )
        if driver_id == "lah_113":
            note += (
                " PinMAME's catalog labels it an unofficial 2014 modification of the CPU ROM, sharing the 1.12 display ROM; it runs on the unmodified 1993 hardware, so it "
                "stays a driver variant of this machine. The retained known-working table runs it (cGameName lah_113, script line 64)."
            )
    drivers.append({
        "id": driver_id,
        "description": DRIVER_LABELS[driver_id],
        "year": DRIVER_YEARS[driver_id],
        "manufacturer": "Data East",
        "flags": 0,
        "physical_compatibility": "unknown" if driver_id == "lah_l108_105" else "identical",
        "variant_notes": note,
        **({} if driver_id == ROOT_DRIVER else {"clone_of": ROOT_DRIVER}),
    })
for _driver in drivers:
    for _role, _mine, _theirs in zip(ROLES, ROM_SETS[_driver["id"]], _root):
        if _mine != _theirs and _mine not in _driver["variant_notes"]:
            raise SystemExit(f"{_driver['id']}: {_role} ROM {_mine} differs from the root but the note omits it")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def excerpt_record(name: str, locator: str, **extra) -> dict:
    record = {
        "id": f"excerpt.last-action-hero.{name.rsplit('.', 1)[0]}",
        "locator": locator,
        "path": f"evidence/excerpts/{KEY}/{name}",
        "sha256": file_sha256(EXCERPT_DIR / name),
    }
    record.update(extra)
    return record


CHECKED = {
    "method": "manual",
    "transcribed_by": "curator, read from native-resolution (300 dpi) renders of the image-only scan; OCR was used only to find pages",
    "reviewed": True,
}
EXCERPTS_MANUAL = [
    excerpt_record(
        "switch-matrix.md",
        "printed pages 28-29 (PDF 32-33), Switch Matrix Chart and the complete Switch Part Numbers table", **CHECKED,
    ),
    excerpt_record(
        "lamp-matrix.md",
        "printed pages 30-31 (PDF 34-35), Lamp Matrix Chart, the Lamp Number / Description list and the Lamp Locations drawing", **CHECKED,
    ),
    excerpt_record(
        "coil-drivers.md",
        "printed pages 32-33 (PDF 36-37), the coil text, the coil-driver schematic for drives 1-16, CPU Controlled Auxiliary Solenoids, Flipper Solenoids, the Flash Lamp / "
        "Coil Tests location drawing and the Backbox Flash Lamps drawing", **CHECKED,
    ),
    excerpt_record(
        "cabinet-and-assemblies.md",
        "printed pages 2, 34, 35, 38 and 46 (PDF 6, 38, 39, 42 and 50), the PPB board's G.I. fuses (Detail A), Cabinet Parts Illustration, Playfield - Major "
        "Assemblies, Lamp Bulb Part Numbers and the Cabinet Wiring Diagram's diagnostic switches", **CHECKED,
    ),
    excerpt_record(
        "game-features.md",
        "printed page 4 (PDF 8), Game Specific Features: the skill shot, the CRANE targets and lock with the DANGER bar warning, advancing to M-BALL and the "
        "jackpot", **CHECKED,
    ),
    excerpt_record(
        "diagnostics-text.md",
        "printed page 27 (PDF 31), Digital Display, Crane, Magnet and Laser Kick tests", **CHECKED,
    ),
]
EXCERPTS_SCHEMATICS = [
    excerpt_record(
        "schematic-book.md",
        "PDF pages 2, 4, 5, 8, 11, 19, 22, 23 and 25-28 (printed 50, 52, 53, 56, 59, 67, 70, 71 and 73-76), Coil/Flash Lamp wiring sheet with its General Illumination "
        "Lines and G.I. relay, Playfield Switch Wiring Diagram, Playfield Lamp Wiring Diagram, CPU Board Logic Diagram connector CN3 and jumper J8, Power Supply Board "
        "Schematic relay RY1, PPB-1 board drive inputs, Magnet Control Board connections, Magnet Controller Board schematic, Ball Lock, 5-Bank Drop Target, "
        "Lock Ball and 6 Ball Switch assemblies and Crane Assembly", **CHECKED,
    ),
]


# The pinned files that open with a '// license:BSD-3-Clause' line; the pinned root LICENSE keeps every other file under the old MAME licence.
BSD_MARKED = {"degames.c", "s11.c", "s11.h"}


def pin_source(identifier: str, filename: str, locator: str) -> dict:
    record = {
        "id": identifier, "kind": "pinmame_core",
        "uri": f"https://github.com/vpinball/pinmame/blob/{REVISION}/src/wpc/{filename}",
        "revision": REVISION, "sha256": PIN_FILE_SHA256[filename], "locator": locator,
        "attribution": "PinMAME contributors",
    }
    if filename in BSD_MARKED:
        record["license"] = "BSD-3-Clause"
    else:
        record["license"] = "NOASSERTION"
        record["rights"] = (
            f"src/wpc/{filename} carries no license marker, so the pinned root LICENSE keeps it under PinMAME's inherited 'old MAME' license"
        )
    return record


sources = [
    {
        "id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": REVISION,
        "locator": "PinmameGetGames; src/wpc/degames.c lines 1027-1102 (lah_112 root, eight clones)", "license": "BSD-3-Clause",
        "attribution": "PinMAME contributors",
    },
    pin_source(CORE, "degames.c", "lines 77-82 (INITGAMES11, muxSol 10, des11 input ports), 85-89 (FLIP6364) and 1027-1102 (lah block, input_ports_lah, nine drivers and ROM sets)"),
    pin_source(CORE_H, "core.h", "lines 159 (FLIP_SWNO) and 298-332 (output bands, CORE_FIRSTSSSOL 17, CORE_FIRSTSIMSOL 49, CORE_FIRSTCUSTSOL 51, CORE_FLIPPERSWCOL)"),
    pin_source(
        CORE_C, "core.c",
        "lines 1793-1870 (core_updateSw flipper copies and synthetic outputs), 2456-2530 (core_getSol), 3262-3265 (core_update_pwm_output_bulb applies isReversed) "
        "and 3422-3429 (CORE_MODOUT_BULB_44_6_3V_AC_REV sets isReversed)",
    ),
    pin_source(
        S11_C, "s11.c",
        "lines 205-220 (vertical-blank solenoid update: extSol published into solenoids2, then reset to the last write), 371-372 and 727 (Jumper W7 on PIA2 PA7), "
        "392-410 (pia2b_w CN3 lines), 537-650 (setSSSol, updsol, muxing, game-on), 875-883 (lamp and solenoid typing), "
        "1223-1227 (DataEast/Sega 3 output typing for lah_) and 1331 (MDRV_DIPS(1))",
    ),
    pin_source(S11_H, "s11.h", "lines 30-42 (DE_COMPORTS), 89-93 (S11_GAMEONSOL, DE_SWADVANCE, DE_SWUPDN) and 227 (S11_PRINTERLINE)"),
    {
        "id": MANUAL, "kind": "manual",
        "uri": MANUAL_URL,
        "locator": (
            f"{MANUAL_NAME}; printed pages 2, 4, 27-35, 38 and 46 (PDF 6, 8, 31-39, 42 and 50); IPDB-hosted scan of Data East Pinball's 1993 operator manual, 53 pages, image-only, retrieved "
            "through a Wayback capture of IPDB's file URL"
        ),
        "sha256": MANUAL_SHA256, "original_filename": MANUAL_NAME,
        "acquired_at": MANUAL_ACQUIRED,
        "excerpts": EXCERPTS_MANUAL,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Data East Pinball, Inc.; hosted by the Internet Pinball Machine Database",
    },
    {
        "id": SCHEMATICS, "kind": "manual",
        "uri": SCHEMATICS_URL,
        "locator": (
            f"{SCHEMATICS_NAME}; PDF pages 2, 4, 5, 8, 11, 19, 22, 23 and 25-28 (printed 50, 52, 53, 56, 59, 67, 70, 71 and 73-76); IPDB-hosted scan of the same manual's schematic section, 30 pages, "
            "image-only, retrieved through a Wayback capture of IPDB's file URL"
        ),
        "sha256": SCHEMATICS_SHA256, "original_filename": SCHEMATICS_NAME,
        "acquired_at": MANUAL_ACQUIRED,
        "excerpts": EXCERPTS_SCHEMATICS,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Data East Pinball, Inc.; hosted by the Internet Pinball Machine Database",
    },
    {
        "id": IPDB, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=1416",
        "locator": (
            "IPDB machine #1416, 'Last Action Hero' (Data East Pinball), date of manufacture August 09, 1993 (production August 9 to October 29, 1993), model number "
            "500-5527-01, MPU DataEast/Sega Version 3, 5,505 units; design Lyman F. Sheats Jr., Tim Seckel, Joe Kaminkow, Ed Cebula and John Borg, art Markus Rothkranz, "
            "dots Jack Liddon and Kurt Andersen, music Brian Schmidt, software Lonnie D. Ropp and John Carpenter; notable features include a motorized crane target that "
            "moves the ball from one ramp to another, a Ripper target that returns the ball at fast speed, a Smart Missile button that awards the current award, three "
            "electromagnets and 6-ball multiball, with the Ripper and Smart Missile caps on the card holder. Retained Wayback capture "
            f"{IPDB_CAPTURE}. Identity cross-checked against the manual's title, the PinMAME driver description and the retained script's header (ipdb.org machine id 1416)."
        ),
        "sha256": IPDB_SHA256, "acquired_at": IPDB_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": "Internet Pinball Database contributors",
    },
    {
        "id": RUNTIME_SRC, "kind": "runtime_scenario",
        "uri": "internal:" + RUNTIME_EVIDENCE_PATH.relative_to(ROOT).as_posix(),
        "locator": (
            "LibPinMAME harness runs of lah_112 (US English 1.12) from fresh state directories with direct public switch writes only: the Active Switch Test of every switch "
            "address and the flipper column, the single-lamp test, Cycling Coils, the Crane, Magnet and Laser Kick tests, Adjustment 58 Printer Interface, a game start "
            "serving one ball, and a game in play closing the return-lane and captive-ball switches one at a time, scenarios under tools/harness-scenarios/data-east/lah-112-*.json, every cited DMD frame read by a curator and pinned by its pixel digest; raw "
            "traces retained under the review-artifacts root"
        ),
        "revision": REVISION, "sha256": file_sha256(RUNTIME_EVIDENCE_PATH),
        "license": "NOASSERTION", "attribution": "Curator; user-authorized local ROM copies, ROM bytes are not redistributed",
    },
    {
        "id": TABLE, "kind": "vpx_table",
        "uri": f"external:pinmame-vpx-sources/{SOURCE_DIRECTORY}/source/{TABLE_NAME}",
        "original_filename": TABLE_NAME,
        "locator": (
            "Retained known-working recreation by the VPW Film Crew, v1.1 (479,010,816 bytes); playfield 952 x 2162; runs cGameName lah_113. A Visual Light Mapper build: its "
            "lamps drive bulb-mode light-map source Lights that draw no bulb, so no lamp is placed on them, and its raised flash lamps have no modelled bulb or dome. "
            "Geometry authority for named "
            "script-bound objects only; normalized coordinates are x/952 and y/2162. Primitives are placed at the centre of their world-space mesh bounds from a "
            f"{VPXTOOL_VERSION} 'export obj --units vpu' export (SHA-256 {WORLD_OBJ_SHA256}, retained beside the table), and the crane at the rotation axis its three "
            "meshes share."
        ),
        "sha256": TABLE_SHA256, "known_working": True, "acquired_at": TABLE_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": TABLE_ATTRIBUTION,
    },
    {
        "id": SCRIPT_REF, "kind": "vpx_script",
        "uri": f"external:pinmame-vpx-sources/{EXTRACTION_RELATIVE_PATH.as_posix()}/script.vbs",
        "original_filename": "script.vbs",
        "locator": (
            "Embedded script of the retained table (header 'Last Action Hero (Data East 1993)', ipdb.org machine id 1416, credits lines 7-19), Windows-1252 text with CRLF "
            "line ends: LoadVPM \"01000200\", \"DE.VBS\", 3.46 (line 58), cGameName = \"lah_113\" (line 64), HandleKeyboard 0 and HandleMechanics 0 (lines 120 and 124), "
            "vpmNudge.TiltSwitch 1 (line 170), saucers and magnets (lines 175-220), key handling (lines 325-365), SolCallback map (lines 373-414), mechanism subs (lines "
            "418-778), bumper, slingshot and switch handlers (lines 788-1069), trough and launch (lines 1076-1143) and the Lampz assignments (lines 3902-5179)."
        ),
        "sha256": SCRIPT_SHA256, "known_working": True, "acquired_at": EXTRACTION_ACQUIRED,
        "license": "NOASSERTION", "rights": "NOASSERTION", "attribution": TABLE_ATTRIBUTION,
    },
    {
        "id": VPM_DE_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_DE_LIBRARY_URI,
        "original_filename": "de.vbs", "sha256": VPM_DE_SHA256, "acquired_at": "2026-09-25T23:32:01Z",
        "locator": (
            "The VPinMAME script library the retained table loads at runtime (script.vbs line 58 LoadVPM \"01000200\", \"DE.VBS\", 3.46; de.vbs executes core.vbs), retained "
            f"from the contributor's working installation together with core.vbs (SHA-256 {VPM_CORE_SHA256}). de.vbs defines swLRFlip = 82 and swLLFlip = 84 and sets them "
            "from the flipper keys in vpmKeyDown/vpmKeyUp, and names the staged upper flipper keys swURFlip/swULFlip at 86 and 88."
        ),
        "license": "NOASSERTION", "attribution": "VPinMAME / Visual Pinball script-library maintainers", "rights": "NOASSERTION",
        "excerpts": [excerpt_record(
            "vpm-script-library-flippers.md",
            "de.vbs lines 21-36 and 62-111; core.vbs lines 2090, 2854-2855 and 2862-2865; script.vbs lines 58, 64, 120, 124, 340-349, 353-364, 413-414, 418 and 436",
            **{**CHECKED, "transcribed_by": "curator, read from the script files"},
        )],
    },
    {
        "id": EXTRACTION, "kind": "vpx_table",
        "uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
        "locator": (
            "Canonical manifest of every sorted relative POSIX path, byte size and SHA-256 under extracted-vpxtool; "
            f"manifest SHA-256 {EXTRACTION_MANIFEST_SHA256}; {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes, produced with {VPXTOOL_VERSION} from the "
            "retained table. Bounds are 952 x 2162."
        ),
        "sha256": EXTRACTION_MANIFEST_SHA256, "acquired_at": EXTRACTION_ACQUIRED,
        "license": "NOASSERTION", "attribution": "vpxtool extraction",
    },
    {
        "id": LEGACY, "kind": "legacy_json", "uri": "https://github.com/vpinball/pinmame-game-defs", "revision": "4ea106d080728648a693af3b4dcabb091eee0a02",
        "locator": "games/lah.json; origin=vbscript-parser", "sha256": LEGACY_GAME_SHA256,
        "license": "MIT", "attribution": "pinmame-game-defs contributors",
        "rights": (
            "The cited revision's tree carries no licence file. The same bytes are this repository's games/lah.json, which its MIT licence "
            "covers, and the curator refuses to run when that file no longer matches the pinned digest."
        ),
    },
]

# --- Coverage ---------------------------------------------------------------------------------------------------------------
# Every requirement whose evidence is not complete, each with the device or record that keeps it open:
# input_semantics, Jumper W7 whose meaning no retained source states;
# output_semantics, CN3 pins 5-1 (40-44), which no retained run or page connects to anything;
# mechanism_behavior, how the crane loads and releases a ball and which way the energised left-lock coil moves its plunger, known only from one recreation;
# polarity, the Green FORWARD/REVERSE button (-6), whose closing position the cabinet wiring diagram prints as 'CLOSE ??????';
# spatial_placement, every placement observed from one recreation lineage, with the matrix lamps, flash lamps, G.I., crane lock, knocker and CN3 pins unplaced;
# unresolved_conflicts, which address the right captive-ball insert is wired to (lamp 31 or 32), how many lamps flash group 8R drives, and whether flash drive 9's
# lamps hang on the Left/Right relay's switched supply.
MISSING = ["input_semantics", "output_semantics", "mechanism_behavior", "polarity", "spatial_placement", "unresolved_conflicts"]
DIMENSIONS = {
    "catalog_identity": "validated",
    "address_enumeration": "validated",
    "semantic_naming": "observed",
    "physical_wiring": "observed",
    "mechanisms": "observed",
    "variant_coverage": "validated",
    "recreation_knowledge": "validated",
    "runtime_observation": "observed",
    "causal_exercise": "observed",
    "spatial_placement": "observed",
}

definition = {
    "format": "pinmame-machine-definition",
    "schema_version": 2,
    "machine": {
        "id": KEY,
        "name": "Last Action Hero",
        "manufacturer": "Data East",
        "year": 1993,
        "kind": "physical_pinball",
        "model_number": "500-5527-01",
        "ipdb_id": 1416,
        "opdb_id": "GRwyq-MW9lN",
        "playfield": {
            "width": PLACES["table_bounds"]["width"], "height": PLACES["table_bounds"]["height"], "units": "vpx",
            "provenance": prov("observed", [TABLE]),
        },
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
_identifiers = [device["id"] for device in inputs + outputs]
_duplicates = sorted({identifier for identifier in _identifiers if _identifiers.count(identifier) > 1})
if _duplicates:
    raise SystemExit(f"device identifiers are not unique: {_duplicates}")
_known = set(_identifiers)
for _mechanism in mechanisms:
    for _ref in _mechanism["actuators"] + _mechanism["sensors"]:
        if _ref not in _known:
            raise SystemExit(f"{_mechanism['id']} names an unknown device {_ref}")

# --- Spatial report -----------------------------------------------------------------------------------------------------------
PROJECTIONS = {
    ("pinmame.output.solenoid", 13): "The drop-target reset coil is projected onto the middle drop target sw19; the retained table models no coil.",
    ("pinmame.output.solenoid", 14): (
        "The crane motor is projected onto the crane's rotation axis, which the Crane Assembly drawing puts the motor under; it is not a measured motor centre."
    ),
}


def unplaced_keys(document: dict[str, Any]) -> set[str]:
    """The placement-builder keys of every device the record leaves without any spatial record."""
    prefixes = {"pinmame.input.switch": "switch", "pinmame.output.solenoid": "solenoid", "pinmame.output.lamp": "lamp"}
    return {
        f"{prefixes[device['binding']['group']]}.{device['binding']['device']}"
        for device in document["inputs"] + document["outputs"] if "spatial" not in device
    }


def build_spatial_report(document: dict[str, Any]) -> dict[str, Any]:
    located_inputs: list[int] = []
    observed_inputs: list[int] = []
    unplaced_inputs: list[int] = []
    not_applicable_inputs: dict[str, list[int]] = {}
    placement_count = 0
    for device in document["inputs"]:
        spatial = device.get("spatial")
        address = int(device["binding"]["device"])
        if spatial is None:
            unplaced_inputs.append(address)
            continue
        if spatial["status"] == "not_applicable":
            not_applicable_inputs.setdefault(spatial["reason"], []).append(address)
            continue
        placement_count += len(spatial["placements"])
        (observed_inputs if spatial["status"] == "observed" else located_inputs).append(address)
    located_outputs: list[dict[str, Any]] = []
    observed_outputs: list[dict[str, Any]] = []
    unplaced_outputs: list[dict[str, Any]] = []
    not_applicable_outputs: dict[str, list[dict[str, Any]]] = {}
    for device in document["outputs"]:
        binding = {"group": device["binding"]["group"], "address": int(device["binding"]["device"])}
        spatial = device.get("spatial")
        if spatial is None:
            unplaced_outputs.append(binding)
            continue
        if spatial["status"] == "not_applicable":
            not_applicable_outputs.setdefault(spatial["reason"], []).append(binding)
            continue
        placement_count += len(spatial["placements"])
        (observed_outputs if spatial["status"] == "observed" else located_outputs).append(binding)
    order = lambda item: (item["group"], item["address"])  # noqa: E731
    return {
        "format": "pinmame-spatial-blockers",
        "version": 1,
        "machine_id": document["machine"]["id"],
        "status": "observed",
        "blockers": [
            "Every placement comes from one community table (the VPW Film Crew's v1.1) and none was checked against the manual's location drawings, so all of them stay "
            "observed. Promotion needs a callout check of the drawings or a second, independent table lineage.",
            "No matrix lamp has a coordinate. The table drives lamps 1-63 through bulb-mode light-map source Lights that draw no bulb and models no insert bulb, and a "
            "light that sits on no bulb makes no socket; the lamps need a reproducible measurement on the manual's Lamp Locations drawing (printed page 31). Lamps 31, "
            "40 and 43 have no bound Light at all: each lights two inserts, the script fades two light-map sets for each "
            "with live Lampz.Callback lines and leaves only its Lampz.MassAssign line commented out, and choosing between the table's Lights would rest on their names alone. "
            "Which address the right captive-ball insert is wired to is a recorded conflict.",
            "Flash lamps 2R-6R and 8R (26-30, 32) have no coordinate: the table drives them through light-map sources at playfield height and models no bulb or dome, and a "
            "raised flash-lamp socket is never placed on a light-map source. Their sockets are drawn on the manual's Flash Lamp / Coil Tests location drawing.",
            "Flash drive 9 has no coordinate: two of its lamps ride the crane boom and two light the backbox insert.",
            "The G.I. relay 11 has no coordinate: the table's G.I. Lights are light-map sources that draw no bulb, and no retained page counts or locates the G.I. bulbs.",
            "The crane lock 4 rides the sweeping boom and has no fixed location; the knocker 8 is located by no retained page.",
            "CN3 pins 5-1 (solenoid addresses 40-44) have no coordinate: no retained page shows anything connected to them.",
            "The crane motor 14 is a projection onto the crane's rotation axis, and the drop-target reset coil 13 a projection onto the middle drop target.",
            "The crane limit switches 60 and 61 have no coordinate: the table binds no object to them, and the manual's Switch Locations drawing (printed page 29) "
            "prints them at the two ends of the boom's sweep, 60 at the left ramp entrance and 61 at the top of the right orbit beside 47, not at the crane's axis.",
            "The three magnets 37-39 are placed on the table's magnet triggers; the manual says only that they are in the centre of the playfield.",
        ],
        "coordinate_convention": {
            "space": "playfield",
            "source_bounds": {"left": 0.0, "top": 0.0, "right": PLACES["table_bounds"]["width"], "bottom": PLACES["table_bounds"]["height"]},
            "x": "x/952; 0=left, 1=right",
            "y": "y/2162; 0=rear/backglass, 1=apron/player",
        },
        "extraction": {
            "fail_closed": True,
            "file_count": EXTRACTION_FILE_COUNT,
            "manifest_algorithm": "Canonical JSON containing format/version and every extracted file as sorted relative POSIX path, byte size, and SHA-256.",
            "manifest_sha256": EXTRACTION_MANIFEST_SHA256,
            "manifest_uri": f"external:pinmame-vpx-sources/{EXTRACTION_MANIFEST_RELATIVE_PATH.as_posix()}",
            "source_ref": EXTRACTION,
            "total_bytes": EXTRACTION_TOTAL_BYTES,
            "vpxtool_version": VPXTOOL_VERSION,
        },
        "source_hashes": {
            "embedded_script_sha256": SCRIPT_SHA256,
            "manual_sha256": MANUAL_SHA256,
            "schematics_sha256": SCHEMATICS_SHA256,
            "table_sha256": TABLE_SHA256,
            "world_obj_sha256": WORLD_OBJ_SHA256,
        },
        "world_space_export": {
            "command": "vpxtool export obj --units vpu <retained VPX>",
            "sha256": WORLD_OBJ_SHA256,
            "uri": WORLD_OBJ_URI,
            "use": "x/y mesh bounds of every placed primitive, embedded in tools/build_lah_places.py and re-derived by its --world-obj check",
        },
        "placement_count": placement_count,
        "resolved_input_addresses": sorted(located_inputs),
        "observed_input_addresses": sorted(observed_inputs),
        "unplaced_input_addresses": sorted(unplaced_inputs),
        "resolved_output_bindings": sorted(located_outputs, key=order),
        "observed_output_bindings": sorted(observed_outputs, key=order),
        "unplaced_output_bindings": sorted(unplaced_outputs, key=order),
        "not_applicable_inputs": {reason: sorted(addresses) for reason, addresses in sorted(not_applicable_inputs.items())},
        "not_applicable_outputs": {reason: sorted(bindings, key=order) for reason, bindings in sorted(not_applicable_outputs.items())},
        "projections": [{"group": group, "address": address, "reason": reason} for (group, address), reason in sorted(PROJECTIONS.items())],
        "coordinate_origins": {
            "computed_centroids": sorted(
                f"{hit['object_type']} {hit['object']} ({key.replace('.', ' ')})"
                for key, hits in PLACES["placements"].items() for hit in hits if hit["coordinate_origin"] == "computed-centroid"
            ),
            "mesh_bounds_centres": sorted(
                f"Primitive {hit['object']} ({key.replace('.', ' ')})"
                for key, hits in PLACES["placements"].items() for hit in hits if hit["coordinate_origin"] == "mesh-bounds-center"
            ),
            "primitive_pivots": sorted(
                f"Primitive {hit['object']} ({key.replace('.', ' ')})"
                for key, hits in PLACES["placements"].items() for hit in hits if hit["coordinate_origin"] == "primitive-pivot"
            ),
            "object_centers": "every other placement uses its retained object's own stored center (Light, Kicker, Bumper, Spinner) or position (HitTarget)",
        },
        "excluded_object_classes": [
            "Baked lightmap primitives (*_LM_*) faded by Lampz.Callback: they paint light, and are never sockets.",
            "Light-map source Lights bound to flash lamps (f2-f6) and the G.I. Lights gi001-gi025: they sit at playfield height and draw no bulb, so they are not raised sockets.",
            "Cabinet and topper primitives (PinCab_*), VR backglass sprites and Lights the script never binds, such as f7, f8, L31, L31B, L40, L40B, L43 and L43B.",
            "The manual's switch, lamp and flash-lamp location drawings: read and transcribed, but not used for any coordinate.",
        ],
        "unresolved": [entry for entry in PLACES["unplaced"] if entry["key"] in unplaced_keys(document)],
    }


def render_spatial_report(report: dict[str, Any]) -> str:
    lines = [
        "# Last Action Hero (Data East, 1993) spatial review",
        "",
        f"Status: {report['status']}. Every playfield switch but the crane limits, every coil the retained table models with a script-bound object and the three magnets are placed from "
        "that table; cabinet, backbox, topper, virtual and unused addresses carry a controlled `not_applicable` record. The matrix lamps, the flash lamps, flash "
        "drive 9, the G.I., the crane lock, the knocker and the crane limit switches have no coordinate. No placement was checked against the manual's location drawings, so "
        f"every placement stays `observed` and the record stays at `machines/partial/data-east/{SLUG}.json`.",
        "",
        f"The geometry source is the retained known-working `{TABLE_NAME}` (SHA-256 `{TABLE_SHA256}`); its embedded script (SHA-256 `{SCRIPT_SHA256}`) is the runtime binding "
        "authority. Exact playfield bounds are 952 x 2162; every table coordinate is x/952 and y/2162 rounded to six places.",
        "",
        "## Evidence decisions",
        "",
        "- The embedded script is the runtime authority; the 1993 manual and its schematic book are the physical inventory, construction and wiring authority; the 1.12 ROM's "
        "own service tests settle names and switch-to-coil pairs; pinned PinMAME owns controller topology; the retained table supplies geometry for script-bound objects only.",
        "- The table is a Visual Light Mapper build. `Lampz.MassAssign` binds each matrix lamp to a bulb-mode light-map source Light that draws no bulb, and the table "
        "models no insert bulb; a light that sits on no bulb makes no socket, so no matrix lamp is placed, and a raised socket (a flasher dome, a crane cab lamp, a "
        "back-panel lamp) is never placed on such a source either, so no flash lamp is placed.",
        f"- Primitives are placed at the centre of their world-space mesh bounds from the retained `vpxtool export obj --units vpu` export (SHA-256 `{WORLD_OBJ_SHA256}`); "
        "the crane is placed at the rotation axis its three meshes share, which the builder checks against the script's ball-on-the-boom formula.",
        "- Triggers and walls are placed at the centroid of their drag points, never at the editor pivot a Trigger stores.",
        "- The Left/Right relay 10, the shaker motor 16, the topper flash groups 1R and 7R, the credit-button lamp 64 and the cabinet switches are cabinet, backbox or "
        "topper devices.",
        "",
        "## Blockers",
        "",
    ]
    lines += [f"- {blocker}" for blocker in report["blockers"]]
    lines += ["", "## Explicit projections", ""]
    lines += [f"- {entry['group']} {entry['address']}: {entry['reason']}" for entry in report["projections"]]
    lines += [
        "",
        "## Counts",
        "",
        f"- Placements: {report['placement_count']}",
        f"- Validated input addresses: {len(report['resolved_input_addresses'])}",
        f"- Observed-only input addresses: {len(report['observed_input_addresses'])}",
        f"- Validated output bindings: {len(report['resolved_output_bindings'])}",
        f"- Observed-only output bindings: {len(report['observed_output_bindings'])}",
        f"- Output bindings with no coordinate: {len(report['unplaced_output_bindings'])}",
    ]
    lines += [f"- Inputs with a controlled `{reason}` record: {len(addresses)}" for reason, addresses in report["not_applicable_inputs"].items()]
    lines += [f"- Outputs with a controlled `{reason}` record: {len(bindings)}" for reason, bindings in report["not_applicable_outputs"].items()]
    lines += [
        "",
        "## Promotion decision",
        "",
        "Refused. `coverage.missing` lists `spatial_placement` because every coordinate rests on one community table without a drawing check and the matrix lamps, the "
        "flash lamps, the G.I., the crane lock and the knocker are not placed; the other open requirements keep the record partial as well.",
        "",
        "## Retained evidence",
        "",
        f"- Extraction manifest `{report['extraction']['manifest_uri']}`, SHA-256 `{EXTRACTION_MANIFEST_SHA256}`, {EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes.",
        f"- World-space export `{WORLD_OBJ_URI}`, SHA-256 `{WORLD_OBJ_SHA256}`.",
        f"- Manual SHA-256 `{MANUAL_SHA256}`; schematic book SHA-256 `{SCHEMATICS_SHA256}`.",
        "",
    ]
    return "\n".join(lines)


SPATIAL_REPORT = build_spatial_report(definition)

# --- Knowledge note -------------------------------------------------------------------------------------------------------------
KNOWLEDGE_TEXT = KNOWLEDGE_TEMPLATE.read_bytes().decode("utf-8")
knowledge_note = (
    KNOWLEDGE_TEXT.replace("{driver_count}", str(len(drivers))).replace("{placed}", str(SPATIAL_REPORT["placement_count"]))
    .replace("{crane_dropout_ms}", str(_crane["dropout_ms"])).replace("{crane_off_after_shooter_lane_s}", f"{_crane['off_after_shooter_lane_s']:.2f}")
)
if "{" in re.sub(r"`[^`]*`", "", knowledge_note):
    raise SystemExit("the knowledge template still carries an unfilled placeholder")


def build() -> dict:
    """Return the canonical definition assembled from the embedded literals."""
    return definition


# --- Retained extraction ---------------------------------------------------------------------------------------------------------
def build_extraction_manifest(extraction_root: Path) -> dict[str, Any]:
    if not extraction_root.is_dir():
        raise RuntimeError(f"The Last Action Hero retained extraction is missing: {extraction_root}")
    paths = sorted(
        (path for path in extraction_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(extraction_root).as_posix(),
    )
    return {
        "format": "pinmame-vpx-extraction-manifest",
        "version": 1,
        "files": [
            {"path": path.relative_to(extraction_root).as_posix(), "size": path.stat().st_size, "sha256": file_sha256(path)}
            for path in paths
        ],
    }


def configured_vpx_sources_root(*, required: bool) -> Path | None:
    value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if not value:
        if required:
            raise RuntimeError("PINMAME_VPX_SOURCES_ROOT is required to verify the retained Last Action Hero extraction")
        return None
    return Path(value).expanduser().resolve()


def verify_extraction_manifest(source_root: Path) -> dict[str, Any]:
    extraction_root = source_root / EXTRACTION_RELATIVE_PATH
    manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
    if not manifest_path.is_file():
        raise RuntimeError(f"The Last Action Hero extraction manifest is missing: {manifest_path}")
    if file_sha256(manifest_path) != EXTRACTION_MANIFEST_SHA256:
        raise RuntimeError(f"The Last Action Hero extraction manifest's bytes are not the cited ones: {manifest_path}")
    table = source_root / SOURCE_DIRECTORY / "source" / TABLE_NAME
    if not table.is_file() or file_sha256(table) != TABLE_SHA256:
        raise RuntimeError(f"The retained Last Action Hero table is missing or not the cited one: {table}")
    actual = load_json(manifest_path)
    expected = build_extraction_manifest(extraction_root)
    if canonical_bytes(actual) != canonical_bytes(expected):
        raise RuntimeError(f"The Last Action Hero extraction manifest does not match all files under {extraction_root}")
    files = actual["files"]
    identity = (len(files), sum(int(item["size"]) for item in files), hashlib.sha256(canonical_bytes(actual)).hexdigest())
    if identity != (EXTRACTION_FILE_COUNT, EXTRACTION_TOTAL_BYTES, EXTRACTION_MANIFEST_SHA256):
        raise RuntimeError(f"The Last Action Hero extraction identity mismatch: {identity}")
    script = extraction_root / "script.vbs"
    if file_sha256(script) != SCRIPT_SHA256:
        raise RuntimeError(f"The Last Action Hero embedded script is not the cited one: {script}")
    return actual


def write_extraction_manifest(source_root: Path) -> Path:
    manifest_path = source_root / EXTRACTION_MANIFEST_RELATIVE_PATH
    write_json(manifest_path, build_extraction_manifest(source_root / EXTRACTION_RELATIVE_PATH))
    return manifest_path


# --- Artifacts ---------------------------------------------------------------------------------------------------------------------
def _artifacts() -> tuple[tuple[Path, bytes], ...]:
    definition_bytes = canonical_bytes(definition)
    return (
        (DEFINITION_PATH, definition_bytes),
        (SEED_PATH, definition_bytes),
        (SPATIAL_REPORT_PATH, canonical_bytes(SPATIAL_REPORT)),
        (SPATIAL_REPORT_MARKDOWN_PATH, render_spatial_report(SPATIAL_REPORT).encode("utf-8")),
        (KNOWLEDGE_PATH, knowledge_note.encode("utf-8")),
    )


def generate(root: Path = ROOT) -> Path:
    stale = root / AUTHOR_READY_PATH.relative_to(ROOT)
    if stale.exists() and definition["coverage"]["status"] != "author_ready":
        raise RuntimeError(f"refusing to curate while an author-ready artifact exists (preserved): {stale}")
    for path, payload in _artifacts():
        target = root / path.relative_to(ROOT)
        if path.suffix == ".md":
            write_text(target, payload.decode("utf-8"))
        else:
            write_bytes(target, payload)
    return root / DEFINITION_PATH.relative_to(ROOT)


def check(root: Path = ROOT) -> None:
    if (root / AUTHOR_READY_PATH.relative_to(ROOT)).exists():
        raise RuntimeError("A stale Last Action Hero author-ready definition is present")
    for path, expected in _artifacts():
        target = root / path.relative_to(ROOT)
        if not target.is_file():
            raise RuntimeError(f"The Last Action Hero artifact is missing: {target}")
        if target.read_bytes() != expected:
            raise RuntimeError(f"The Last Action Hero artifact drifted from its deterministic curator: {target}")
    report = load_json(root / SPATIAL_REPORT_PATH.relative_to(ROOT))
    placements = sum(len(d.get("spatial", {}).get("placements", [])) for c in ("inputs", "outputs") for d in definition[c])
    if report.get("format") != "pinmame-spatial-blockers" or report.get("machine_id") != KEY or report.get("placement_count") != placements:
        raise RuntimeError("The Last Action Hero spatial report must be a blockers report naming this machine and its placement count")
    print("The Last Action Hero definition, seed, spatial report and knowledge note match the deterministic curator.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Refuse drift between the curator and the canonical artifacts")
    mode.add_argument("--regenerate", action="store_true", help="Write the canonical definition, pinned seed, spatial report and knowledge note")
    mode.add_argument("--write-extraction-manifest", action="store_true", help="Write the retained full-file VPX extraction manifest")
    mode.add_argument("--verify-extraction", action="store_true", help="Verify the retained extraction against its pinned manifest identity")
    args = parser.parse_args()
    if args.write_extraction_manifest:
        root = configured_vpx_sources_root(required=True)
        assert root is not None
        print(f"The Last Action Hero extraction manifest written: {write_extraction_manifest(root)}")
    elif args.verify_extraction:
        root = configured_vpx_sources_root(required=True)
        assert root is not None
        verify_extraction_manifest(root)
        print("The Last Action Hero retained extraction matches its pinned manifest identity.")
    elif args.check:
        check(ROOT)
    else:
        print(f"Wrote {generate(ROOT)}")


if __name__ == "__main__":
    main()
