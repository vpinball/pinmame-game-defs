#!/usr/bin/env python3
"""Reproduce Bally Skateball's curated definition and recreation note.

Semantic decisions live in this file and the pinned source tables. Spatial
decisions are an independently reviewable seed. Generation never requires the
external evidence roots; --verify-extraction checks them explicitly.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "tools")]
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256
from pinmame_game_defs.conflicts import unresolved_conflicts
import build_external_evidence_manifest as external_manifest

MACHINE_ID = "bally.skateball.1980"
DEFINITION = ROOT / "machines/partial/bally/skateball-1980.json"
AUTHOR_READY = ROOT / "machines/author-ready/bally/skateball-1980.json"
KNOWLEDGE = ROOT / "knowledge/bally/skateball-1980.md"
SEEDS = ROOT / "tools/seeds/bally"
SOURCES = SEEDS / "skateball-1980-sources.json"
SPATIAL = SEEDS / "skateball-1980-spatial.json"
KNOWLEDGE_SEED = SEEDS / "skateball-1980-knowledge.md"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
CORE = "pinmame.core.46e1a01a0f73"
PROFILE = "controller-profile.pinmame-by35"
MANUAL = "manual.bally.skateball.1980"
SCHEMATIC = "schematic.bally.skateball.1980"
SCRIPT = "vpx-script.skateball.1-0-4"
TABLE = "vpx-table.skateball.1-0-4"
LIBRARY = "vpinmame-library.bally-vbs"
RUNTIME = "runtime.skateball.skatebll.switch-2-and-19-in-play"
SERVICE_RUNTIME = "runtime.skateball.service-tests"
LANE_PHOTO = "human-review.skateball.photo-026"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def prov(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def aliases(namespace: str, number: int) -> list[dict]:
    # Numeric compatibility aliases are deliberately preserved, including pads.
    return [{"namespace": namespace, "value": str(number)}] + [
        {"namespace": f"vpe-legacy.{namespace.split('.')[-1]}", "value": value}
        for value in dict.fromkeys((str(number), f"{number:02d}", f"{number:03d}"))
    ]


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


# Public matrix address -> (label, contact class, pulse, location, roles).
# Side names are those of the factory's player-view Figure V, never the legacy
# import's reversed middle-bank names.
SWITCHES = {
    2: ("Middle right drop target", "leaf", False, "Middle three-target bank, right", []),
    3: ("Middle center drop target", "leaf", False, "Middle three-target bank, center", []),
    4: ("Middle left drop target", "leaf", False, "Middle three-target bank, left", []),
    5: ("Saucer", "leaf", False, "Upper-right saucer", []),
    6: ("Credit button", "button", False, "Coin door", ["cabinet.credit-button"]),
    7: ("Tilt", "tilt", False, "Panel, plumb bob and ball tilt contacts", ["cabinet.tilt"]),
    8: ("Outhole", "leaf", False, "Outhole below the flippers", ["internal.trough"]),
    9: ("Coin III (right)", "leaf", True, "Coin door, right coin chute", ["cabinet.coin-door"]),
    10: ("Coin I (left)", "leaf", True, "Coin door, hinge-side coin chute", ["cabinet.coin-door"]),
    11: ("Coin II (middle)", "leaf", True, "Coin door, middle coin chute", ["cabinet.coin-door"]),
    13: ("Number 3 lane", "leaf", True, "Rear rollover lane #3", []),
    14: ("Number 2 lane", "leaf", True, "Rear rollover lane #2", []),
    15: ("Number 1 lane", "leaf", True, "Rear rollover lane #1", []),
    16: ("Slam tilt", "tilt", False, "Coin door and cabinet", ["cabinet.slam-tilt"]),
    17: ("Drop-target and rebound scoring contacts", "leaf", True, "Three drop-target hit contacts and four 30-point rebound contacts", []),
    18: ("B lane", "leaf", True, "Right side lane B", []),
    19: ("A lane", "leaf", True, "Right side lane A", []),
    20: ("E drop target", "leaf", False, "Five-target SKATE bank, E", []),
    21: ("T drop target", "leaf", False, "Five-target SKATE bank, T", []),
    22: ("A drop target", "leaf", False, "Five-target SKATE bank, A", []),
    23: ("K drop target", "leaf", False, "Five-target SKATE bank, K", []),
    24: ("S drop target", "leaf", False, "Five-target SKATE bank, S", []),
    26: ("Top right drop target", "leaf", False, "Top three-target bank, right", []),
    27: ("Top center drop target", "leaf", False, "Top three-target bank, center", []),
    28: ("Top left drop target", "leaf", False, "Top three-target bank, left", []),
    30: ("Lower rollover button", "leaf", True, "Lower star rollover button", []),
    31: ("Upper rollover button", "leaf", True, "Upper star rollover button", []),
    32: ("Right flipper lane-change contact", "button", False, "Right cabinet flipper button, matrix contact", ["flipper.button.right"]),
    33: ("Spinner", "leaf", True, "Spinner", []),
    34: ("Right outlane", "leaf", True, "Right outlane special", []),
    35: ("Left outlane", "leaf", True, "Left outlane special", []),
    36: ("Right slingshot", "leaf", True, "Right slingshot", []),
    37: ("Left slingshot", "leaf", True, "Left slingshot", []),
    38: ("Right thumper bumper", "leaf", True, "Right thumper bumper", []),
    39: ("Bottom thumper bumper", "leaf", True, "Bottom thumper bumper", []),
    40: ("Left thumper bumper", "leaf", True, "Left thumper bumper", []),
}
BLANK_SWITCHES = {1, 12, 25, 29}
CABINET = {6, 7, 9, 10, 11, 16, 32}


def matrix_switch(number: int, evidence: dict) -> dict:
    if number not in SWITCHES:
        note = (f"Factory self-test row {number:02d} is explicitly blank and the game wiring fits no contact there."
                if number in BLANK_SWITCHES else
                "The game's matrix wiring uses ST0-ST4 (five columns, 1-40); no sixth-column contact is fitted.")
        return {"id": f"switch.unused-{number}", "label": f"Unused matrix position {number}", "kind": "switch",
                "binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number),
                "availability": "unused", "physical": {"notes": note}, "provenance": prov(MANUAL, SCHEMATIC, CORE),
                "spatial": na("unused", MANUAL, SCHEMATIC)}
    label, contact, pulse, location, roles = SWITCHES[number]
    notes = ["The game's switch-identification table and its own matrix wiring establish this contact.",
             "The MPU reads the switch matrix without complementing it; the table writes state 1 for a closure at the bound public switch address. The physical contact rests open, separately from PinMAME's informational inversion flag."]
    if number == 2:
        notes += ["Legacy evidence mislabelled public 1 as tilt and public 2 as a ball-roll tilt. The factory table leaves 1 blank, puts all three tilts at 7, and names 2 MIDDLE RIGHT DROP TARGET. The retained gameplay trace closes 3 and 4 then 2 and the ROM resets the middle bank at output 10 without tilting."]
    if number == 17:
        notes += ["The printed table names '3 DROP TARGET & 4 30 POINT REBOUNDS': seven physical contacts share this address. The scoring contacts are separate from the eleven latched target-down switches; the VPX uses sw17a-sw17g as pulse triggers."]
    if number == 32:
        notes += ["This independently wired matrix contact rotates the 1-2-3 lane awards. A recreation must assert it with the right cabinet button as well as public 82, which supplies the synthetic right-flipper state. It is neither an EOS input nor a copied FLIP_SWNO address."]
    if number in (13, 15):
        notes += ["The manual's self-test table assigns public 13 to lane #3 and public 15 to lane #1 without specifying their sides. Figure V draws the rear rollover circles left-to-right 15, 14, 13, corroborating relative number order, but its differing upper-playfield geometry is not fitted to validate absolute placements or as-built artwork. The retained JPSalas table pairs switch 13 and lamp 24 at the left lane, and switch 15 and lamp 56 at the right. Its artwork and the physical replacement board in photo-026 instead label lane #1 left and #3 right. The observed placement follows that replacement-board orientation; original 1980 artwork orientation remains unverified. This is an observed layout mismatch, not a factory-proven table defect."]
    physical = {"switch_type": contact, "location": location, "notes": " ".join(notes)}
    if number in {7, 16, 17}:
        physical["quantity"] = {7: 3, 16: 2, 17: 7}[number]
    item = {"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
            "binding": {"group": "pinmame.input.switch", "device": number},
            "aliases": aliases("pinmame.switch", number) + [{"namespace": "manual.address", "value": f"{number:02d}"}],
            "normally_closed": False, "pulse": pulse, "availability": "used", "physical": physical,
            "provenance": prov(MANUAL, SCHEMATIC, SCRIPT, CORE, *([RUNTIME] if number == 2 else []))}
    if number == 8:
        item["initial_active"] = True
    if roles:
        item["roles"] = roles
    if number in CABINET:
        item["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC)
    wiring = evidence.get("switch_wiring", {}).get(str(number))
    if wiring:
        item["wiring"] = copy.deepcopy(wiring)
    return item


DIP_FUNCTIONS = {
    **{n: "Coin chute I (hinge side) credits/coin, one bit of S1-S5" for n in range(1, 6)},
    7: "Drop target bonus advance: ON advances bonus one step; OFF does not advance bonus",
    8: "Top drop targets spot-multiplier X lamp memory: ON retained for next ball; OFF not retained",
    **{n: "Coin chute III (right side) credits/coin, one bit of S9-S13" for n in range(9, 14)},
    14: "Middle drop target arrow lamp memory: ON retained for next ball; OFF not retained",
    15: "Top drop target arrow lamp memory: ON retained for next ball; OFF not retained",
    16: "50,000 and saucer extra ball: ON light together; OFF 50,000 then extra ball",
    **{n: "Coin chute II (center) credits/coin, one bit of S17-S20; all OFF follows chute I" for n in range(17, 21)},
    23: "Bonus multiplier lamp memory: ON retained for next ball; OFF not retained",
    24: "Saucer extra ball and right outlane special: ON light together; OFF extra ball then special",
    25: "Maximum credits with S26: S26/S25 OFF/OFF 10, OFF/ON 15, ON/OFF 25, ON/ON 40",
    26: "Maximum credits with S25: S26/S25 OFF/OFF 10, OFF/ON 15, ON/OFF 25, ON/ON 40",
    27: "Credit display: ON shown; OFF hidden", 28: "Match feature: ON enabled; OFF disabled",
    30: "Making A-B and S-K-A-T-E: ON lights saucer extra ball; OFF does not",
    31: "Balls per game with S32: S32/S31 OFF/ON 5, ON/OFF 4, OFF/OFF 3, ON/ON 2",
    32: "Balls per game with S31: S32/S31 OFF/ON 5, ON/OFF 4, OFF/OFF 3, ON/ON 2",
}


def all_inputs(evidence: dict) -> list[dict]:
    inputs = []
    for number, label, role, location in [(-7, "Self-test button", "service.self-test", "Inside coin door"),
                                        (-6, "CPU diagnostic button", "service.diagnostic", "MPU board, backbox"),
                                        (-5, "Sound diagnostic button", "service.diagnostic", "Sound board, backbox")]:
        inputs.append({"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
                       "binding": {"group": "pinmame.input.switch", "device": number}, "aliases": aliases("pinmame.switch", number),
                       "availability": "used", "normally_closed": False, "pulse": False, "roles": [role],
                       "physical": {"switch_type": "button", "location": location}, "provenance": prov(CORE, LIBRARY, MANUAL),
                       "spatial": na("cabinet_or_service", CORE, MANUAL)})
    inputs.extend(matrix_switch(n, evidence) for n in range(1, 49))
    for n in range(81, 89):
        used = n in (82, 84)
        side = "Right" if n == 82 else "Left"
        label = f"{side} flipper button" if used else f"Unused flipper-column position {n}"
        item = {"id": f"switch.{slug(label)}", "label": label, "kind": "switch",
                "binding": {"group": "pinmame.input.switch", "device": n}, "aliases": aliases("pinmame.switch", n),
                "availability": "used" if used else "unused", "provenance": prov(CORE, PROFILE, LIBRARY, SCHEMATIC),
                "spatial": na("cabinet_or_service" if used else "unused", CORE, SCHEMATIC),
                "physical": {"notes": "The driver declares FLIP_SW(FLIP_L) without FLIP_SWNO, FLIP_SOL, FLIP_EOS or upper bits. The ROM reads columns 1-6, never generic column 11. Only lower button bits 82/84 feed core_updateSw's synthetic output pairs; the other positions have no consumer on this driver."}}
        if used:
            item.update(normally_closed=False, pulse=False, roles=[f"flipper.button.{side.lower()}"])
            item["physical"].update(switch_type="button", location=f"{side} cabinet flipper button")
            item["physical"]["notes"] += " Each button operates two physical flipper assemblies on its side."
            if n == 82:
                item["physical"]["notes"] += " Also assert matrix 32 for the independent lane-change contact."
        inputs.append(item)
    for n in range(1, 33):
        known = n in DIP_FUNCTIONS
        notes = DIP_FUNCTIONS.get(n, "No function is assigned in the game's complete adjustment pages or the retained table's DIP dialog. Its physical bank exists, but no function or non-use is inferred.")
        notes += f" PinMAME's BY35 input-port default is {'ON' if n in (20, 21) else 'OFF'}."
        if n in (25, 26):
            notes += " On skatebla, S25 and S26 both ON enable free play instead, per its retained archive's info.txt."
        inputs.append({"id": f"dip.option-switch-{n}", "label": f"MPU option switch S{n}" if known else f"Undocumented MPU option switch S{n}",
                       "kind": "dip_switch", "binding": {"group": "pinmame.input.dip", "device": n},
                       "aliases": [{"namespace": "pinmame.dip", "value": str(n)}, {"namespace": "manual.address", "value": f"S{n}"}],
                       "availability": "used" if known else "unknown", "physical": {"switch_type": "dip", "location": "MPU A4, backbox", "notes": notes},
                       "provenance": prov(MANUAL, CORE, SCRIPT), "spatial": na("dip_switch", MANUAL)})
    return inputs


# public -> (label, factory self-test number, kind, part number, cabinet).
COILS = {
    2: ("Saucer kicker", 3, "coil", "AO-27-1300", False),
    6: ("Knocker", 2, "coil", "AR-26-1200", True),
    7: ("Outhole kicker", 1, "coil", "AN-26-1200", False),
    8: ("SKATE drop target reset", 9, "coil", "NO-26-1900", False),
    9: ("Top drop target reset", 10, "coil", "NO-26-1900", False),
    10: ("Middle drop target reset", 11, "coil", "NO-26-1900", False),
    11: ("Left thumper bumper", 6, "coil", "AN-26-1200", False),
    12: ("Bottom thumper bumper", 7, "coil", "AN-26-1200", False),
    13: ("Right thumper bumper", 8, "coil", "AN-26-1200", False),
    14: ("Left slingshot", 4, "coil", "AO-26-1200", False),
    15: ("Right slingshot", 5, "coil", "AO-26-1200", False),
    18: ("Coin lockout", 12, "coil", "FO-36-7000", True),
    19: ("K1 flipper-enable relay", 13, "relay", None, True),
}

# Each tuple is (physical label, connector pin, literal wire code). The public
# address follows U1-U4 output 0-14, not SCR number: the SCR order is irregular.
# N/U branches on the same nets remain in the retained complete transcription.
LAMPS = {
    1: ("1K bonus", "A5J1-18", "58"), 2: ("5K bonus", "A5J1-19", "60"),
    3: ("9K bonus", "A5J1-17", "57"), 4: ("E drop target", "A5J1-23", "12"),
    5: ("S drop target", "A5J1-14", "54"), 6: ("2X bonus", "A5J1-15", "13"),
    7: ("20K saucer", "A5J1-16", "90"), 8: ("Saucer collect bonus", "A5J1-28", "78"),
    9: ("1-2-3 special", "A5J1-24", "50"), 10: ("Top right drop target arrow", "A5J1-25", "75"),
    11: ("Shoot again (backbox)", "A5J2-21", "47"), 12: ("Right outlane special", "A5J1-27", "53"),
    13: ("Ball in play", "A5J2-22", "62"), 14: ("Left outlane special", "A5J2-16", "34"),
    15: ("Bonus special", "A5J2-14", "12"), 17: ("2K bonus", "A5J1-1", "41"),
    18: ("6K bonus", "A5J1-9", "43"), 19: ("10K bonus", "A5J1-8", "51"),
    20: ("T drop target", "A5J1-3", "45"), 21: ("B lane", "A5J1-2", "52"),
    22: ("3X bonus", "A5J1-10", "23"), 23: ("30K saucer", "A5J1-7", "34"),
    24: ("Number 3 lane", "A5J1-6", "25"), 25: ("Right thumper bumper", "A5J1-5", "48"),
    26: ("Top center drop target arrow", "A5J1-11", "65"), 27: ("Match", "A5J2-8", "70"),
    28: ("Lower rollover button", "A5J1-12", "61"), 29: ("High score to date", "A5J2-23", "97"),
    30: ("Middle drop targets 10K center", "A5J2-20", "98"), 31: ("Middle drop targets 20K right arrow", "A5J2-15", "23"),
    33: ("3K bonus", "A5J3-26", "43"), 34: ("7K bonus", "A5J3-25", "36"),
    35: ("20K bonus", "A5J3-19", "67"), 36: ("A drop target", "A5J3-17", "13"),
    37: ("A lane", "A5J3-16", "25"), 38: ("4X bonus", "A5J3-23", "98"),
    39: ("50K saucer", "A5J3-27", "40"), 40: ("Number 2 lane", "A5J1-13", "96"),
    41: ("Bottom thumper bumper", "A5J3-21", "30"), 42: ("Top left drop target arrow", "A5J3-20", "64"),
    43: ("Same player shoots again", "A5J3-22", "23"), 44: ("Upper rollover button", "A5J3-24", "72"),
    45: ("Game over", "A5J2-11", "95"), 46: ("Middle drop targets 100K", "A5J2-6", "85"),
    47: ("Middle drop targets 10K right", "A5J2-2", "20"), 49: ("4K bonus", "A5J3-1", "10"),
    50: ("8K bonus", "A5J3-12", "21"), 51: ("40K bonus", "A5J3-15", "53"),
    52: ("K drop target", "A5J3-11", "20"), 53: ("60K bonus", "A5J3-9", "15"),
    54: ("5X bonus", "A5J3-3", "81"), 55: ("Saucer extra ball", "A5J3-4", "14"),
    56: ("Number 1 lane", "A5J3-2", "95"), 57: ("Left thumper bumper", "A5J3-10", "91"),
    58: ("Spot multiplier", "A5J3-18", "56"), 59: ("Credit indicator", "A5J3-13", "35"),
    60: ("Spinner 1K", "A5J3-14", "84"), 61: ("Tilt", "A5J2-10", "35"),
    62: ("Middle drop targets 10K left", "A5J2-7", "91"), 63: ("Middle drop targets 20K left arrow", "A5J2-1", "60"),
}
SCRS = [
    [14, 12, 13, 8, 9, 10, 11, 4, 1, 2, 3, 7, 16, 5, 6],
    [29, 27, 28, 35, 34, 22, 26, 25, 24, 17, 23, 21, 15, 18, 19],
    [36, 38, 44, 49, 48, 37, 32, 20, 42, 41, 40, 39, 33, 30, 31],
    [57, 50, 51, 54, 55, 60, 59, 58, 56, 46, 52, 53, 47, 43, 45],
]
BACKBOX_LAMPS = {11, 13, 27, 29, 45, 61}


def lamp_output(number: int) -> dict:
    label, connector, wire = LAMPS[number]
    decoder, output = divmod(number - 1, 16)
    notes = [f"A5 U{decoder + 1} output {output} drives Q{SCRS[decoder][output]}, then {connector} (wire {wire}). Public address = 16 * lamp-data line + decoder selector + 1; selectors 15 are idle and have no address."]
    if number in BACKBOX_LAMPS:
        notes += ["The insert/backbox schematic names this load in the A1 insert, so its physical location is backbox."]
    elif connector.startswith("A5J2"):
        notes += ["Although the lamp board labels J2 TO BACK BOX, Table B routes this branch onward to the playfield and W-1192-23C draws the load on PLAYFIELD A6."]
    if number in (11, 12, 27, 28, 40, 43, 44, 57, 60):
        notes += ["The board also exposes this same SCR net on a connector pin marked N/U for that branch. The N/U branch does not make the populated load unused; all sixty decoded addresses have a fitted lamp."]
    if number in (25, 57):
        notes += ["The retained JPSalas table swaps its left and right bumper-lamp bindings: NFadeL 25 names left Bumper1L and NFadeL 57 names right Bumper2L. The physical schematic fixes 25 at the right bumper and 57 at the left; this is a table defect, and any assembly-center projection follows the physical identity. The supplemental VPW table binds the bumper lamps to their correct physical sides."]
    if number in (24, 56):
        notes += ["The lamp wiring table names public 24 lane #3 and public 56 lane #1 without assigning sides. The retained JPSalas script drives lamp 24 through Light.l24 on the left and lamp 56 through Light.l56 on the right, matching its switch 13/15 pairing. The table artwork and physical replacement board in photo-026 label #1 left and #3 right; the manual's Figure V corroborates the switches' relative number order but is not an absolute placement fit. This is an observed mismatch with that replacement/artwork; original 1980 artwork orientation remains unverified. No lamp socket position is adopted from these render lights."]
    if number in (7, 23, 39):
        notes += ["The factory wiring and physical insert artwork label the saucer awards 20K, 30K and 50K. The manual's feature prose instead says 50K and 100K on early SKATE completions; that stale rule wording does not rename the observed inserts."]
    item = {"id": f"lamp.{slug(label)}", "label": label, "kind": "lamp", "availability": "used",
            "physical": {"location": "Backbox" if number in BACKBOX_LAMPS else "Playfield apron credit window" if number == 59 else "Playfield", "notes": " ".join(notes)},
            "wiring": {"board": "Lamp driver A5 AS-2518-23", "driver_transistor": f"Q{SCRS[decoder][output]}",
                       "drive_connection": connector, "drive_wire": wire},
            "provenance": prov(SCHEMATIC, CORE, *([MANUAL, SCRIPT, TABLE, LANE_PHOTO] if number in (24, 56) else []))}
    if number in BACKBOX_LAMPS:
        item["spatial"] = na("cabinet_or_service", SCHEMATIC)
        item["roles"] = ["cabinet.backglass"]
    return item


def all_outputs(evidence: dict) -> list[dict]:
    outputs = []
    for n in [*range(1, 16), *range(17, 21)]:
        if n in COILS:
            label, test, kind, part, cabinet = COILS[n]
            physical = {"location": label, "notes": f"Factory solenoid self-test number {test:02d}; this is distinct from public address {n}. The game's own A3 schematic traces the decoder/continuous PIA line to this load."}
            if part:
                physical["part_number"] = part
            item = {"id": f"device.{slug(label)}", "label": label, "kind": kind,
                    "binding": {"group": "pinmame.output.solenoid", "device": n},
                    "aliases": aliases("pinmame.coil", n) + [{"namespace": "manual.self-test", "value": f"{test:02d}"}],
                    "availability": "used", "physical": physical, "provenance": prov(MANUAL, SCHEMATIC, CORE, SCRIPT, SERVICE_RUNTIME)}
            if cabinet:
                item["spatial"] = na("cabinet_or_service", MANUAL, SCHEMATIC)
            if n == 19:
                item["physical"]["notes"] += " The retained gameplay trace raises this at game start, holds it through all three balls and right-button presses, and drops it at game over. It enables all four flippers; it is not an upper-right flipper output."
                item["provenance"] = prov(MANUAL, SCHEMATIC, CORE, RUNTIME)
            if str(n) in evidence.get("coil_wiring", {}):
                item["wiring"] = copy.deepcopy(evidence["coil_wiring"][str(n)])
        else:
            item = {"id": f"device.unused-solenoid-{n}", "label": f"Unused solenoid output {n}", "kind": "coil",
                    "binding": {"group": "pinmame.output.solenoid", "device": n}, "aliases": aliases("pinmame.coil", n),
                    "availability": "unused", "physical": {"notes": "The game's A3 solenoid-driver drawing marks the corresponding load N/U; the connector and playfield wiring fit no coil. A power-up/test pulse is output state, not a physical load."},
                    "provenance": prov(SCHEMATIC, CORE, SERVICE_RUNTIME), "spatial": na("unused", SCHEMATIC)}
            if n in (17, 20):
                item.update(id=f"output.unfitted-continuous-{n}", label=f"Unfitted continuous output {n}", availability="unknown")
                item["physical"]["notes"] = (
                    f"The game's A3 drawing positively marks the physical load behind continuous output {n} N/U, and the connector/playfield wiring fits no load. "
                    "All three retained ROM runs publish a startup burst at outputs 17-20; the exact rising and falling edges remain recorded as observations. "
                    "The PIA writes or ROM initialization causing that burst have not been established. Inverted PIA transport and startup timing alone do not explain its cause, so availability remains unknown. "
                    "The not-applicable spatial record describes documented physical non-fitment; it does not resolve the published state."
                )
                item["provenance"] = prov(SCHEMATIC, CORE, SERVICE_RUNTIME, status="observed")
        outputs.append(item)
    for n, side, duplicate in [(45, "Right", True), (46, "Right", False), (47, "Left", True), (48, "Left", False)]:
        label = f"{side} synthetic flipper power state" if duplicate else f"{side} flipper pair"
        physical = {"notes": f"PinMAME fabricates outputs {45 if side == 'Right' else 47}/{46 if side == 'Right' else 48} together from button {82 if side == 'Right' else 84} while relay 19 is enabled. Both remain asserted for the held closure; neither measures EOS or individual winding timing."}
        if not duplicate:
            physical.update(quantity=2, part_number="AQ-25-500/34-4500", location=f"Upper and lower {side.lower()} flipper assemblies")
            physical["notes"] += " The manual counts four flippers. The retained table's lower-side callback moves both flippers on that side; no separate upper output exists on this driver."
        item = {"id": f"output.{slug(label)}" if duplicate else f"device.{slug(label)}", "label": label,
                "kind": "virtual" if duplicate else "coil", "binding": {"group": "pinmame.output.solenoid", "device": n},
                "aliases": aliases("pinmame.coil", n), "availability": "used", "physical": physical,
                "provenance": prov(CORE, PROFILE, MANUAL, SCHEMATIC, SCRIPT, SERVICE_RUNTIME)}
        if duplicate:
            item["spatial"] = na("virtual", CORE, PROFILE)
        outputs.append(item)
    for n in [*range(1, 16), *range(17, 32), *range(33, 48), *range(49, 64)]:
        data = lamp_output(n)
        data.update(binding={"group": "pinmame.output.lamp", "device": n}, aliases=aliases("pinmame.lamp", n))
        outputs.append(data)
    return outputs


def mechanisms(inputs: list[dict], outputs: list[dict]) -> tuple[list[dict], list[dict]]:
    ins = {d["binding"]["device"]: d["id"] for d in inputs if d["binding"]["group"] == "pinmame.input.switch"}
    outs = {d["binding"]["device"]: d["id"] for d in outputs if d["binding"]["group"] == "pinmame.output.solenoid"}
    items = []
    for slug_, label, coil, sensors in [("skate-bank", "Five-target SKATE bank", 8, [20, 21, 22, 23, 24]),
                                       ("top-bank", "Top three-target bank", 9, [26, 27, 28]),
                                       ("middle-bank", "Middle three-target bank", 10, [2, 3, 4])]:
        items.append({"id": f"mechanism.{slug_}", "label": label, "kind": "drop_target_bank",
                      "actuators": [outs[coil]], "sensors": [ins[n] for n in sensors],
                      "behavior": f"{len(sensors)} independently latched drop targets; each down contact remains closed until the shared reset coil at public {coil} raises the bank. The script maps the target-down addresses {', '.join(map(str, sensors))} individually and raises all together on that output. Start/reset actions come from the ROM; do not substitute an all-down software timer. The three extra hit-scoring contacts on shared switch 17 are separate from these latched contacts; see the recreation note for their fitment.",
                      "provenance": prov(MANUAL, SCHEMATIC, SCRIPT)})
    for slug_, label, coil, sensor, text in [
        ("outhole", "Single-ball outhole and serve", 7, 8, "One ball rests in the outhole at startup, closing 8. Output 7 kicks it toward the shooter lane and the switch opens as the ball leaves. The manual shooter then launches it; no shooter switch, multiball trough stack or ball lock is evidenced."),
        ("saucer", "Saucer kickout", 2, 5, "A ball entering the saucer closes 5 and remains captured while the ROM scores its award or bonus. Output 2 ejects it back onto the playfield; open 5 when the ball leaves. The retained embedded script aims about 195 degrees at force 20 VPX units; these are implementation tuning clues, not measured factory timing or force.")]:
        items.append({"id": f"mechanism.{slug_}", "label": label, "kind": "kicker", "actuators": [outs[coil]],
                      "sensors": [ins[sensor]], "behavior": text, "provenance": prov(MANUAL, SCHEMATIC, SCRIPT)})
    for slug_, label, coils, sensors, text in [
        ("thumper-bumpers", "Three thumper bumpers", [11, 12, 13], [40, 39, 38], "Each skirt closure requests its own thumper coil: left 40 to 11, bottom 39 to 12, right 38 to 13. The ball is repelled by the ring and the skirt contact opens again; no home-position sensor exists."),
        ("slingshots", "Two slingshots", [14, 15], [37, 36], "The left rebound contacts at 37 request coil 14; the right contacts at 36 request coil 15. A kick moves the rubber arm then springs back. The factory table explicitly says the sling and thumper coils energize when their switch is made."),
        ("flippers", "Four hard-wired flippers", [46, 48], [82, 84, 32], "Each cabinet button powers both flippers on that side through the K1 enable relay. Public 46 drives the right pair and 48 the left pair; 45/47 repeat the synthetic state. Matrix 32 is the separate right-button lane-change contact. Each assembly has a physical EOS contact for its dual-winding coil, but this driver publishes no independent EOS input or upper-flipper output.")]:
        items.append({"id": f"mechanism.{slug_}", "label": label, "kind": "other", "actuators": [outs[n] for n in coils],
                      "sensors": [ins[n] for n in sensors], "behavior": text, "provenance": prov(MANUAL, SCHEMATIC, SCRIPT, CORE)})
    relationships = [{"id": f"relationship.switch-{s}-coil-{c}", "kind": "pulse", "source": ins[s], "destination": outs[c],
                      "provenance": prov(MANUAL, SCHEMATIC)} for s, c in [(37, 14), (36, 15), (40, 11), (39, 12), (38, 13)]]
    relationships += [{"id": f"relationship.flipper-enable-{side}", "kind": "relay_gated", "source": outs[19], "destination": outs[n],
                       "provenance": prov(SCHEMATIC, CORE)} for side, n in [("right", 46), ("left", 48)]]
    return items, relationships


def build_definition() -> dict:
    evidence = load(SOURCES)
    spatial = load(SPATIAL)
    inputs, outputs = all_inputs(evidence), all_outputs(evidence)
    switch_aliases = {-7: "s_self_test", -6: "s_cpu_diagnose", -5: "s_sound_diagnose", 6: "s_start_button", 7: "s_tilt",
                      9: "s_coin_3", 10: "s_coin_2", 11: "s_coin_1", 16: "s_slam_tilt", 82: "s_flipper_lower_right", 84: "s_flipper_lower_left"}
    coil_aliases = {19: ["c_game_on"], 46: ["c_flipper_lower_right", "c_flipper_upper_right"], 48: ["c_flipper_lower_left", "c_flipper_upper_left"]}
    for item in inputs:
        if item["binding"]["group"] == "pinmame.input.switch" and item["binding"]["device"] in switch_aliases:
            item["aliases"].append({"namespace": "vpe-legacy.switch", "value": switch_aliases[item["binding"]["device"]]})
    for item in outputs:
        if item["binding"]["group"] == "pinmame.output.solenoid":
            for value in coil_aliases.get(item["binding"]["device"], []):
                item["aliases"].append({"namespace": "vpe-legacy.coil", "value": value})
            if item["binding"]["device"] in (46, 48):
                item["physical"]["notes"] += " Named legacy flipper aliases follow their physical side to this synthetic pair; their former numeric bindings at continuous outputs 17/18/19/20 were incorrect. Numeric aliases remain address-bound."
    mechs, relationships = mechanisms(inputs, outputs)
    devices = {f"{('switch' if d['binding']['group'] == 'pinmame.input.switch' else 'lamp' if d['binding']['group'] == 'pinmame.output.lamp' else 'solenoid')}:{d['binding']['device']}": d
               for d in inputs + outputs if d["binding"]["group"] != "pinmame.input.dip"}
    for key, value in spatial.get("device_spatial", {}).items():
        if key not in devices:
            raise ValueError(f"Spatial seed names an unenumerated device: {key}")
        devices[key]["spatial"] = copy.deepcopy(value)
    for key, value in spatial.get("device_physical", {}).items():
        if key not in devices:
            raise ValueError(f"Physical spatial seed names an unenumerated device: {key}")
        # Append the geometric rationale rather than dropping semantic evidence.
        patch = copy.deepcopy(value)
        notes = patch.pop("notes", None)
        devices[key].setdefault("physical", {}).update(patch)
        if notes:
            devices[key]["physical"]["notes"] = devices[key]["physical"].get("notes", "") + " " + notes
    sources = copy.deepcopy(evidence["sources"]) + copy.deepcopy(spatial.get("sources", []))
    if len({s["id"] for s in sources}) != len(sources):
        raise ValueError("Duplicate semantic/spatial source IDs")
    for source in sources:
        for excerpt in source.get("excerpts", []):
            for path_key, hash_key in [("path", "sha256"), ("image", "image_sha256")]:
                if path_key in excerpt and file_sha256(ROOT / excerpt[path_key]) != excerpt[hash_key]:
                    raise ValueError(f"Pinned evidence drift: {excerpt[path_key]}")
    displays = [{"id": f"display.player-{n}-score", "label": f"Player {n} score", "kind": "segment", "controller_index": n - 1,
                 "segment_start": start, "width": 7, "provenance": prov(CORE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)}
                for n, start in enumerate((1, 9, 17, 25), 1)]
    displays += [{"id": f"display.{slug(label)}", "label": label, "kind": "segment", "controller_index": index,
                  "segment_start": start, "width": 2, "provenance": prov(CORE, MANUAL), "spatial": na("cabinet_or_service", CORE, MANUAL)}
                 for label, index, start in [("Credits", 4, 35), ("Match and ball in play", 5, 38)]]
    missing = ["input_semantics", "output_semantics", *spatial.get("coverage_missing", ["spatial_placement"])]
    definition = {"format": "pinmame-machine-definition", "schema_version": 2,
                  "machine": {"id": MACHINE_ID, "name": "Skateball", "manufacturer": "Bally", "year": 1980,
                              "kind": "physical_pinball", "model_number": "1210", "ipdb_id": 2170, "opdb_id": "GrNpx-M2YZq"},
                  "controller": {"platform": "pinmame.by35", "hardware_generation": "0x400000", "inversion_applied_by_emulator": True},
                  "coverage": {"status": "partial", "missing": list(dict.fromkeys(missing)), "dimensions": {
                      "catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "candidate",
                      "physical_wiring": "validated", "mechanisms": "validated", "variant_coverage": "validated",
                      "recreation_knowledge": "validated", "display_inventory": "validated", "spatial_placement": "observed"}},
                  "drivers": copy.deepcopy(evidence["drivers"]), "inputs": inputs, "outputs": outputs, "displays": displays,
                  "mechanisms": mechs, "relationships": relationships, "sources": sources,
                  "knowledge": {"path": "knowledge/bally/skateball-1980.md", "status": "partial"}, "conflicts": []}
    if spatial.get("playfield"):
        definition["machine"]["playfield"] = copy.deepcopy(spatial["playfield"])
    if unresolved_conflicts(definition):
        raise ValueError("Unexpected unresolved conflict")
    return definition


def verify_extraction() -> str:
    value = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if not value:
        raise ValueError("PINMAME_VPX_SOURCES_ROOT must identify retained evidence")
    evidence = load(SOURCES)
    base = Path(value) / "bally/skateball-1980"
    extraction = base / evidence["extraction"]["relative_path"]
    actual = external_manifest.check_manifest(extraction, "skatebll")
    if actual != evidence["extraction"]["manifest_sha256"]:
        raise ValueError("Extraction manifest does not match the curated pin")
    if file_sha256(base / evidence["extraction"]["table_relative_path"]) != evidence["extraction"]["table_sha256"]:
        raise ValueError("Retained VPX bytes do not match the curated pin")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()
    try:
        if args.verify_extraction:
            print(verify_extraction())
            return 0
        definition = build_definition()
        artifacts = {DEFINITION: canonical_bytes(definition), KNOWLEDGE: KNOWLEDGE_SEED.read_bytes()}
        if AUTHOR_READY.exists():
            raise ValueError("Refusing to overwrite or demote an existing author-ready definition")
        if args.check:
            drift = [str(p.relative_to(ROOT)) for p, content in artifacts.items() if not p.exists() or p.read_bytes() != content]
            if drift:
                raise ValueError("Curated artifact drift: " + ", ".join(drift))
        else:
            for path, content in artifacts.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        print("Skateball curated artifacts match" if args.check else "Regenerated Skateball curated artifacts")
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
