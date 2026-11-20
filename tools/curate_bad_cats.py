"""Regenerate the Bad Cats definition and spatial audit from retained evidence."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json
from pinmame_game_defs.spatial import extract_spatial_candidates

from build_external_evidence_manifest import check_manifest
from pinmame_flipper_column import flipper_column_inputs, flipper_column_relationships

MACHINE = "williams.bad-cats.1989"
SLUG = "bad-cats-1989"
SWITCH = "pinmame.input.switch"
DIP = "pinmame.input.dip"
COIL = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
CORE = "pinmame.bcats.46e1a01a"
MANUAL = "manual.bcats.operations"
TABLE = "vpx.bcats.unclewilly"
SCRIPT = "vpx-script.bcats.unclewilly"
IPDB = "ipdb.bcats.127"
TCM = "home-rom.bcats.cats-meow"
RUNTIME = "runtime.bcats.l5-service"
STEPPER = "manual.bcats.stepper"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
SEED = ROOT / "tools/seeds/williams"
EXCERPTS = Path("evidence/excerpts") / MACHINE
DEFINITION = Path("machines/partial/williams") / f"{SLUG}.json"
KNOWLEDGE = Path("knowledge/williams") / f"{SLUG}.md"
REPORT = Path("reports/spatial/williams") / f"{SLUG}.md"
RUNTIME_PATH = Path("evidence/runtime/system-11/bcats_l5-service.json")
MANUAL_FILE = "operation-and-parts-nov-1989.pdf"
MANUAL_HASH = "79306ef2f40e5c67c6e8ea3693562525934a348fd0659858a8e1ef9bdd921274"
MANUAL_URL = "https://www.coinoperatorshop.com/media/products/manual/pinball/Williams_1989_Bad_Cats_Manual.pdf"
IPDB_HASH = "00184cf0e192fbed87cadab45aee8b64ea47617ecd4c81b41d96675a9f0f4157"
IPDB_URL = "https://www.ipdb.org/machine.cgi?id=127"
TCM_URL = "https://pinside.com/pinball/forum/topic/the-cat-s-meow-a-new-home-rom-for-bad-cats"

SWITCH_LABELS = {
    1: "Plumb Bob Tilt", 2: "C-Side Power A/C Relay Feedback", 3: "Credit Button",
    4: "Right Coin Chute", 5: "Center Coin Chute", 6: "Left Coin Chute",
    7: "Slam Tilt", 8: "High Score Reset", 9: "Playfield Tilt", 10: "Outhole",
    11: "T Rollover", 12: "O Rollover", 13: "Y Rollover", 14: "Ball Shooter Lane",
    16: "Enter Center Ramp", 19: "In-Line Fish Target", 22: "Doghouse Kickbig",
    23: "Enter Tiger Ramp", 24: "Fish Collect Eject Hole", 25: "Bird Target 1",
    26: "Bird Target 2", 27: "Bird Target 3", 28: "Bird Target 4",
    29: "Bird Target 5", 30: "Left Return Lane", 31: "Right Return Lane",
    33: "Rubber 1", 34: "Rubber 2", 35: "Left Outlane", 36: "Right Outlane",
    37: "Milk Target 1", 38: "Milk Target 2", 39: "Milk Target 3", 40: "Rubber 3",
    41: "Exit Tiger Ramp", 43: "Exit Center Ramp", 44: "Seafood Wheel Home",
    57: "Right Flipper Lane Change", 58: "Left Flipper Lane Change",
    60: "Left Jet Bumper", 61: "Right Jet Bumper", 62: "Lower Jet Bumper",
    63: "Left Slingshot", 64: "Right Slingshot",
}
SWITCH_ALIASES = {
    -7: "s_advance", -6: "s_up_down", -5: "s_cpu_diagnostics", -4: "s_sound_diagnostics",
    1: "s_tilt", 2: "s_ball_roll_tilt", 3: "s_start_button", 4: "s_coin_3",
    5: "s_coin_2", 6: "s_coin_1", 7: "s_slam_tilt", 8: "s_high_score_reset",
    81: "s_flipper_upper_right", 82: "s_flipper_lower_right",
    83: "s_flipper_upper_left", 84: "s_flipper_lower_left",
}
COIL_ALIASES = {
    23: "c_game_on", 34: "c_flipper_upper_right", 36: "c_flipper_upper_left",
    46: "c_flipper_lower_right", 48: "c_flipper_lower_left",
}
SOLENOID_LABELS = {
    1: "Outhole Kicker", 2: "Knocker", 3: "Doghouse Kickbig", 4: "Milk Bottle Bank Reset",
    5: "Garbage Can Eject", 6: "Bird Cage Bank Reset", 9: "Backbox Cat Motor",
    10: "Playfield General Illumination Relay", 11: "Backbox General Illumination Relay",
    12: "A/C Select Relay", 13: "Backbox Woman Motor", 14: "Backbox Bad Cats Flashers",
    15: "Seafood Wheel Winding 2", 16: "Seafood Wheel Winding 1",
    17: "Left Jet Bumper", 18: "Left Slingshot", 19: "Right Jet Bumper",
    20: "Right Slingshot", 21: "Lower Jet Bumper", 23: "Flipper and Special Solenoid Enable",
    25: "Fish and Trash Flashers", 26: "Tiger Flashers", 27: "Bird Bank Flashers",
    28: "Left Tiger Flashers", 29: "Jackpot Flashers", 30: "Seafood Flashers",
    31: "Doghouse Flashers", 32: "Barbecue Flashers", 45: "Right Flipper Power Mirror",
    46: "Right Flipper Hold Mirror", 47: "Left Flipper Power Mirror", 48: "Left Flipper Hold Mirror",
}
SWITCH_NOTES = {
    2: "S11_MUXSW2 overwrites the legacy Ball Roll Tilt address with the state of public solenoid 12.",
    5: "The switch matrix allocates a center coin chute. The US parts list specifies it as unfitted.",
    9: "The factory parts list calls out B-8306-1. The local VPX script does not implement this contact.",
    10: "The known-working script holds this switch closed with the single ball resting in the drain trough.",
    19: "A linear moving target operates an opto. The VPW script uses a virtual target to reproduce the opto response.",
    44: "In the uninverted matrix public 1 means closed, confirmed by Switch Levels. The factory Wheel Test displays H for an open matrix contact or interrupted opto. VPX simulates the sensor window at steps 0–99 of 200. The physical rest convention and flag width remain unmeasured.",
    57: "Factory parts list identifies a Backbox Interconnect Board optotransistor. PinMAME copies right flipper button 82 into switch 57 each update.",
    58: "Factory parts list identifies a Backbox Interconnect Board optotransistor. PinMAME copies left flipper button 84 into switch 58 each update.",
}
OUTPUT_NOTES = {
    10: "A playfield-mounted C-11998-1 relay switches the playfield illumination. System 11 has no separate public GI-string group.",
    11: "The second C-11998-1 relay is on the backbox insert board and switches backbox illumination.",
    12: "D-12247 carries this relay. It selects the C side and PinMAME reports its state back at switch 2.",
    14: "The wiring table prints four #89 backbox lamps. The abbreviated location list prints #906.",
    15: "Coil 2 of the shared stepper. The brown-violet feed reaches D-12046 J1-5 Input B.",
    16: "Coil 1 of the shared stepper. The brown-grey feed reaches D-12046 J1-4 Input A.",
    23: "PIA0 CB2 gates published special solenoids and the synthetic flipper mirrors. There is no distinct CPU coil driver for 23.",
    31: "The factory drawing calls out 7A at the right-side flasher. Its adjacent parts table and the test table agree on 7C for this device.",
    7: "The L-5 Coil Test pulses 07A under NOT USED. Williams specifies no fitted load.",
    8: "The L-5 Coil Test pulses 08A under NOT USED. Williams specifies no fitted load.",
    22: "The L-5 Coil Test pulses Special 6 under NOT USED. Williams specifies no fitted load.",
}
DRIVERS = {
    "bcats_f1": "Williams LF-1 French program and regional factory adjustments.",
    "bcats_g4": "Williams LG-4 German. PinMAME uses the L-5 U26 and a repaired German U27 image.",
    "bcats_l2": "Williams LA-2. Early production software handles the linear Fishbone-Us opto differently from L-5.",
    "bcats_l5": "Williams L-5 production program and the baseline for this definition.",
    "bcats_tcm": "The Cat's Meow home ROM by idealjoker. The replacement U26/U27 software adds rules and adjustments on the original board.",
    "bcats_tcm12": "The Cat's Meow 1.2 replacement U26/U27 program for the original machine.",
    "bcats_tcm13": "The Cat's Meow 1.3 replacement U26/U27 program for the original machine.",
}


def excerpt(name: str, locator: str) -> dict:
    path = EXCERPTS / f"{name}.md"
    return {
        "id": f"excerpt.bcats.{name}", "path": path.as_posix(), "locator": locator,
        "sha256": file_sha256(ROOT / path), "method": "manual",
        "transcribed_by": "curator", "reviewed": True,
    }


def source_records(seed: dict) -> list[dict]:
    return [
        {
            "id": CORE, "kind": "pinmame_core",
            "uri": "https://github.com/vpinball/pinmame",
            "revision": REVISION, "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
            "locator": "src/wpc/s11games.c:1042–1117; src/wpc/s11.c s11_dispS11b2, pia4a_r, setSSSol, updsol, SWITCH_UPDATE(s11), MACHINE_INIT(s11); src/wpc/core.c core_updateSw and core_getSol",
        },
        {
            "id": MANUAL, "kind": "manual", "uri": MANUAL_URL,
            "revision": "16-575-101 November 1989", "sha256": MANUAL_HASH,
            "license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.",
            "original_filename": "Williams_1989_Bad_Cats_Manual.pdf", "acquired_at": "2026-11-20T08:28:36Z",
            "locator": "Retained 47-page operations and parts scan. PDF 32, 33, 35–37, 40, 43–47.",
            "excerpts": [
                excerpt("switch-matrix", "PDF 35 (printed 32), sequential switch matrix"),
                excerpt("lamp-matrix", "PDF 32 (printed 29), sequential lamp matrix"),
                excerpt("solenoid-table", "PDF 33 (printed 30), A/C and special solenoid table; PDF 44 parts and flasher locations"),
                excerpt("location-lists", "PDF 45–46, complete switch part and lamp location lists"),
                excerpt("factory-mechanisms", "PDF 10, 36–37, 40, 43, 47, mechanism sections and drawings"),
            ],
        },
        {
            "id": TABLE, "kind": "vpx_table",
            "uri": f"external:pinmame-vpx-sources/williams/{SLUG}/{seed['table']}",
            "sha256": seed["table_sha256"], "attribution": "unclewilly, Clark Kent, Dark",
            "license": "NOASSERTION", "acquired_at": "2026-11-20T08:28:00Z",
            "locator": f"VPX 10.4 BadCats v1.0. Exact gamedata/gameitems extraction and manifest SHA-256 {seed['manifest_sha256']}.",
        },
        {
            "id": SCRIPT, "kind": "vpx_script",
            "uri": f"external:pinmame-vpx-sources/williams/{SLUG}/extracted/script.vbs",
            "sha256": seed["script_sha256"], "attribution": "unclewilly, Clark Kent, Dark",
            "license": "NOASSERTION", "acquired_at": "2026-11-20T08:28:00Z", "known_working": True,
            "locator": "Extracted with vpxtool git:v0.33.3. Table initialization, switch handlers, solenoid callbacks and LampTimer_timer.",
            "excerpts": [excerpt("vpx-bindings", "Embedded script initialization, switch and solenoid handlers, and matrix-lamp dispatch")],
        },
        {
            "id": IPDB, "kind": "human_review", "uri": IPDB_URL,
            "sha256": IPDB_HASH, "source_id": "127", "acquired_at": "2026-11-20T08:27:59Z",
            "locator": "Retained rendered page HTML ipdb-127.html, model, release, keyed image captions and factory downloads.",
            "license": "NOASSERTION", "attribution": "Internet Pinball Database",
            "excerpts": [excerpt("identity", "IPDB 127 model, production and physical features; Pinside home ROM announcement")],
        },
        {
            "id": TCM, "kind": "human_review", "uri": TCM_URL,
            "locator": "idealjoker's announcement, LA-2/L-5 linear-target behavior notes and installation instructions for replacement program chips.",
            "attribution": "idealjoker via Pinside",
        },
        {
            "id": STEPPER, "kind": "manual",
            "uri": "https://www.ipdb.org/files/127/Williams_1989_Bad_Cats_Seafood_Wheel_Stepper_Motor_Control_Board_Schematic.pdf",
            "sha256": "95abd83b4ca94f226ace714ee0e99638f665e1408bc75599dc504f1aeeb2bc0d",
            "source_id": "127", "acquired_at": "2026-11-20T08:42:30Z",
            "original_filename": "Williams_1989_Bad_Cats_Seafood_Wheel_Stepper_Motor_Control_Board_Schematic.pdf",
            "locator": f"IPDB machine page {IPDB_URL}; D-12046, sheet 1, opto and stepper connectors.",
            "license": "NOASSERTION", "attribution": "Williams Electronics Games, Inc.",
            "excerpts": [excerpt("stepper-wiring", "D-12046 sheet 1, J1 and P2 connections and Opto 1 circuit")],
        },
        {
            "id": RUNTIME, "kind": "service_diagnostic", "uri": RUNTIME_PATH.as_posix(),
            "sha256": file_sha256(ROOT / RUNTIME_PATH), "revision": REVISION,
            "locator": "Bad Cats L-5 Coil Test, Single Lamps and Switch Levels on pinned LibPinMAME.",
            "attribution": "pinmame-game-defs contributors",
        },
    ] + seed.get("extra_sources", [])


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"source_refs": list(refs), "status": status}


def not_applicable(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def ident(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def aliases(group: str, address: int, legacy: str | None = None) -> list[dict]:
    kind = {SWITCH: "switch", COIL: "coil", LAMP: "lamp", DIP: "dip"}[group]
    result = [{"namespace": f"pinmame.{kind}", "value": str(address)}]
    if group != DIP:
        values = dict.fromkeys((str(address), f"{address:02}", f"{address:03}")) if address >= 0 else {str(address): None}
        result.extend({"namespace": f"vpe-legacy.{kind}", "value": value} for value in values)
        if legacy:
            result.append({"namespace": f"vpe-legacy.{kind}", "value": legacy})
    return result


def device(group: str, address: int, kind: str, label: str, availability: str, *refs: str) -> dict:
    prefix = {SWITCH: "switch", COIL: "device", LAMP: "lamp", DIP: "dip"}[group]
    legacy = SWITCH_ALIASES.get(address) if group == SWITCH else COIL_ALIASES.get(address) if group == COIL else None
    return {
        "id": f"{prefix}.{ident(label)}", "label": label, "kind": kind,
        "binding": {"group": group, "device": address}, "availability": availability,
        "aliases": aliases(group, address, legacy),
        "provenance": provenance(*refs, status="candidate" if availability == "unknown" else "validated"),
    }


def table_rows(name: str) -> list[list[str]]:
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in (ROOT / EXCERPTS / f"{name}.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("|")
    ]


def matrix_rows(name: str) -> dict[int, tuple[str, dict]]:
    rows = table_rows(name)
    entries = {}
    for row in rows[2:]:
        ret_wire, ret_pin = row[0].split()[-2:]
        for heading, cell in zip(rows[0][1:], row[1:], strict=True):
            drive_wire, drive_pin = heading.split()[-2:]
            transistor = next(value for value in heading.split() if value.startswith("Q"))
            number, label = cell.split(maxsplit=1)
            wiring = {
                "board": "System 11B CPU board", "driver_transistor": transistor,
                "drive_wire": drive_wire, "drive_connection": drive_pin,
                "return_wire": ret_wire, "return_connection": ret_pin,
            }
            if name == "lamp-matrix":
                wiring["return_component"] = row[0].split()[0]
            entries[int(number)] = (label, wiring)
    if set(entries) != set(range(1, 65)):
        raise ValueError(f"Incomplete factory {name}")
    return entries


def inputs(seed: dict) -> list[dict]:
    result = []
    labels = {-7: "Advance", -6: "Auto-Up / Manual-Down", -5: "CPU Diagnostics", -4: "Sound Diagnostics"}
    for address, label in labels.items():
        item = device(SWITCH, address, "switch", label, "used", MANUAL, CORE)
        item.update(physical={"location": "coin-door service panel" if address in {-7, -6} else "backbox CPU board",
                              "switch_type": "button" if address != -6 else "other"},
                    spatial=not_applicable("cabinet_or_service", MANUAL, CORE))
        result.append(item)
    construction = {int(row[0]): row[1] for row in table_rows("location-lists") if len(row) == 3 and row[0].isdigit()}
    for address, (_, wiring) in sorted(matrix_rows("switch-matrix").items()):
        label = SWITCH_LABELS.get(address, f"Unused Switch {address}")
        availability = ("optional" if address == 5 else "used") if address in SWITCH_LABELS else "unused"
        refs = (MANUAL, CORE, STEPPER, RUNTIME) if address == 44 else (MANUAL, CORE)
        if address in seed["normally_open"]:
            refs += (SCRIPT,)
        item = device(SWITCH, address, "switch", label, availability, *refs)
        if availability == "unused":
            item["spatial"] = not_applicable("unused", MANUAL, CORE)
        else:
            location = "playfield"
            switch_type = "other"
            if address in {1, 3, 4, 5, 6, 7, 8}:
                location = "cabinet"
                switch_type = "button" if address in {3, 8} else "tilt" if address in {1, 7} else "other"
            elif address in {2, 57, 58}:
                location = "backbox"
                switch_type = "opto" if address in {57, 58} else "other"
            elif address in {19, 25, 26, 27, 28, 29, 37, 38, 39, 44}:
                switch_type = "opto"
            elif address in {9}:
                switch_type = "tilt"
            item["physical"] = {"location": location, "switch_type": switch_type}
            if construction[address].startswith("p/o "):
                item["physical"]["assembly_part_number"] = construction[address][4:]
            elif construction[address] not in {"-", "(See Figure 2)", "Not Used (USA)"}:
                item["physical"]["part_number"] = construction[address]
            if address in SWITCH_NOTES:
                item["physical"]["notes"] = SWITCH_NOTES[address]
            item["wiring"] = wiring
            # No per-game input inversion. Limit contact claims to proven entries.
            if address in seed["normally_open"]:
                item["normally_closed"] = False
            if address == 10:
                item["initial_active"] = True
            if location != "playfield":
                item["spatial"] = not_applicable("cabinet_or_service", MANUAL, CORE)
        result.append(item)

    buttons = flipper_column_inputs(
        flip_swno=(58, 57), flip_swno_text="FLIP_SWNO(58,57)", core_refs=(CORE,),
        button_refs=(MANUAL, SCRIPT), button_notes={
            side: "PDF 45 lists the separate SW-10A-48 cabinet button for each side."
            for side in ("right", "left")
        }, button_normally_closed=False,
    )
    for button in buttons:
        number = button["binding"]["device"]
        button["aliases"] = aliases(SWITCH, number, SWITCH_ALIASES.get(number))
    country = device(DIP, 0, "dip_switch", "Country Jumper", "used", CORE)
    country["physical"] = {"location": "CPU board", "switch_type": "dip", "notes": "PIA2 PA7 reads the USA/Germany country jumper."}
    country["spatial"] = not_applicable("dip_switch", CORE)
    return result + buttons + [country]


def solenoids() -> list[dict]:
    result = []
    rows = {}
    for number, _, _, color, cpu, field, transistor, part in table_rows("solenoid-table")[2:]:
        printed = number.rstrip("³")
        if printed == "-":
            continue
        address = int(printed.rstrip("AC")) + (24 if printed.endswith("C") else 0)
        rows[address] = printed, color, cpu, field, transistor, part
    for address in range(1, 51):
        if address in SOLENOID_LABELS:
            availability = "used"
        else:
            availability = "unused"
        label = SOLENOID_LABELS.get(address, f"Unused Solenoid {address}")
        if address in {23, 45, 46, 47, 48} or address not in rows:
            kind = "virtual"
        elif address in {9, 13, 15, 16}:
            kind = "motor"
        elif address in {10, 11, 12}:
            kind = "relay"
        elif address == 14 or 25 <= address <= 32:
            kind = "flasher"
        else:
            kind = "coil"
        refs = [CORE, MANUAL]
        if address in rows:
            refs.append(RUNTIME)
        if address in {15, 16}:
            refs.append(STEPPER)
        item = device(COIL, address, kind, label, availability, *refs)
        if address in rows:
            printed, color, cpu, field, transistor, part = rows[address]
            item["aliases"].append({"namespace": "manual.address", "value": printed})
            item["wiring"] = {
                "board": "Aux Power Driver Board", "driver_transistor": transistor, "drive_wire": color,
                "drive_connection": field,
            }
            if not cpu.startswith("("):
                item["wiring"]["control_connection"] = cpu
            else:
                item["wiring"]["control_wire"] = cpu.strip("()")
        if availability == "unused":
            item["spatial"] = not_applicable("unused", CORE, MANUAL)
            if address in OUTPUT_NOTES:
                item["physical"] = {"notes": OUTPUT_NOTES[address]}
        elif availability == "used":
            if kind == "virtual":
                side = "right" if address < 47 else "left"
                note = OUTPUT_NOTES.get(address, f"PinMAME synthesizes both {side} outputs from the cabinet button while 23 enables the flippers. The factory flipper has its own cabinet-wired power and hold circuit.")
                item["physical"] = {"notes": note}
                item["spatial"] = not_applicable("virtual", CORE)
            else:
                location = "playfield"
                if address in {2, 9, 11, 12, 13, 14}:
                    location = "backbox"
                if 25 <= address <= 32 and address != 30:
                    location = "playfield and backbox"
                item["physical"] = {"location": location}
                if kind == "flasher":
                    item["physical"]["quantity"] = 4 if address == 14 else 3 if address == 30 else 2
                    item["physical"]["part_number"] = "#89" if address == 14 else "#906" if address == 30 else "#906/#89"
                else:
                    item["physical"]["part_number"] = part.split(" p/n")[-1].split()[0]
                if address in OUTPUT_NOTES:
                    item["physical"]["notes"] = OUTPUT_NOTES[address]
                if location == "backbox":
                    item["spatial"] = not_applicable("cabinet_or_service", MANUAL)
        result.append(item)
    return result


def lamps() -> list[dict]:
    result = []
    overrides = {
        17: "T (Rear Playfield Panel)", 18: "O (Rear Playfield Panel)", 19: "Y (Rear Playfield Panel)",
        31: "Doghouse", 32: "Seafood Arrow 2 (Fitment Unconfirmed)", 55: "Barbecue (Backglass)",
        64: "8,000,000 JACKPOT (Backglass)",
    }
    notes = {
        31: "PDF 46 gives DOGHOUSE and points to its lamp assembly. The matrix calls this Seafood Arrow 1.",
        32: "The matrix names Seafood Arrow 2. The location list leaves 32 blank and the local VPX omits it. L-5 blinks the address under a blank name.",
        55: "The matrix calls this backglass lamp JACKPOT. The PDF 46 location list and L-5 Single Lamps diagnostic both identify Barbecue.",
    }
    for address, (label, wiring) in sorted(matrix_rows("lamp-matrix").items()):
        label = overrides.get(address, label)
        if address in range(33, 40):
            label = f"BAD CATS Letter {address - 32} ({label})"
        refs = (MANUAL, CORE, RUNTIME) if address in {31, 32, 55} else (MANUAL, CORE)
        item = device(LAMP, address, "lamp", label, "unknown" if address == 32 else "used", *refs)
        item["wiring"] = wiring
        location = "playfield"
        if address >= 54:
            location = "backbox"
        elif 17 <= address <= 19:
            location = "rear playfield panel"
        elif 9 <= address <= 13:
            location = "Tiger Ramp"
        item["physical"] = {"location": location} if address != 32 else {}
        if address in notes:
            item["physical"]["notes"] = notes[address]
        if location == "backbox":
            item["spatial"] = not_applicable("cabinet_or_service", MANUAL)
        result.append(item)
    return result


def displays() -> list[dict]:
    return [
        {
            "id": f"display.{position}-alphanumeric", "label": f"{position.title()} sixteen-character alphanumeric display",
            "kind": "segment", "controller_index": index, "segment_start": index * 20, "width": 16,
            "physical_location": "cabinet_or_service", "spatial": not_applicable("cabinet_or_service", CORE, MANUAL),
            "provenance": provenance(CORE, MANUAL, "pinside.bcats.backbox"),
        }
        for index, position in enumerate(("upper", "lower"))
    ]


def mechanisms(switches: dict[int, dict], coils: dict[int, dict]) -> list[dict]:
    items = [
        ("trough", "Outhole and Single-Ball Trough", "kicker", [1], [10, 14], "B-8039-2",
         "The drain feeds the under-apron runway. A settled ball closes 10. Output 1 kicks it to the manual shooter lane, which has its own switch 14."),
        ("doghouse", "Doghouse Kickbig", "kicker", [3], [22], "C-11987-1",
         "A ball settles in the molded Doghouse pocket and closes 22. The kick arm releases it back to the playfield when 3 pulses."),
        ("garbage-can", "Garbage Can Eject", "kicker", [5], [24], "B-9361-R-5",
         "A ball in the garbage-can eject hole closes Fish Collect 24. Coil 5 kicks the ball out toward the upper playfield."),
        ("bird-bank", "Five-Bird Drop Target Bank", "drop_target_bank", [6], list(range(25, 30)), "C-13116",
         "Five latching blades report their lowered states through C-13239. Reset coil 6 lifts the bank and clears the target states."),
        ("milk-bank", "Three-Milk-Bottle Drop Target Bank", "drop_target_bank", [4], [37, 38, 39], "C-11223-1",
         "Three latching blades report their lowered states through the C-12559 opto board. Reset coil 4 lifts the bank and clears the target states."),
        ("fish-target", "Fish Bone-Us Linear Target", "other", [], [19], "B-13016",
         "The ball moves a sprung target arm through a sensing region. The ROM counts the opto's transitions, and the VPX uses a moving stand-in."),
        ("wheel", "Seafood Wheel", "rotary", [15, 16], [44], "C-12036-2",
         "Two phases drive one stepper under an eight-position wheel. Test 08 reports a home opto and a nominal count of 1–200, and spins to the next counterclockwise position."),
        ("backbox", "Cat and Broom Animation", "toy", [9, 13], [], "C-13180",
         "The insert-board feature has separate motors for the cat and woman. Test 09 exercises them independently."),
        ("tiger-ramp", "Tiger Ramp Gates", "gate", [], [23, 41], None,
         "The ramp entrance and exit each have a switch. The ramp guides the ball around the rear of the playfield."),
        ("center-ramp", "Center Ramp Gates", "gate", [], [16, 43], None,
         "The Goldfish ramp has separate entrance and exit contacts. The ramp rises above the playfield and returns the ball on its wireform."),
        ("left-jet", "Left Jet Bumper", "kicker", [17], [60], "B-13123",
         "The skirt closes the bumper contact and its coil snaps the bumper ring down."),
        ("right-jet", "Right Jet Bumper", "kicker", [19], [61], "B-9414",
         "The skirt closes the bumper contact and its coil snaps the bumper ring down."),
        ("lower-jet", "Lower Jet Bumper", "kicker", [21], [62], "B-9414",
         "The skirt closes the bumper contact and its coil snaps the bumper ring down."),
        ("left-sling", "Left Slingshot", "kicker", [18], [63], "B-12665",
         "Rubber movement closes the paired switch assembly and the kick arm deforms the rubber outward."),
        ("right-sling", "Right Slingshot", "kicker", [20], [64], "B-12665",
         "Rubber movement closes the paired switch assembly and the kick arm deforms the rubber outward."),
        ("left-flipper", "Lower Left Flipper", "other", [], [58], "C-11626-L-1",
         "The cabinet button operates the power and hold coil circuit. Lane-change monitor 58 follows its actuation."),
        ("right-flipper", "Lower Right Flipper", "other", [], [57], "C-11626-R-1",
         "The cabinet button operates the power and hold coil circuit. Lane-change monitor 57 follows its actuation."),
    ]
    return [
        {
            "id": f"mechanism.{identifier}", "label": label, "kind": kind,
            "actuators": [coils[address]["id"] for address in actuators],
            "sensors": [switches[address]["id"] for address in sensors],
            "behavior": behavior, "provenance": provenance(MANUAL, SCRIPT, status="observed"),
            **({"assembly_part_number": assembly} if assembly else {}),
        }
        for identifier, label, kind, actuators, sensors, assembly, behavior in items
    ]


def build(seed: dict) -> dict:
    switch_list = inputs(seed)
    coil_list = solenoids()
    output_list = coil_list + lamps()
    devices = {(d["binding"]["group"], d["binding"]["device"]): d for d in switch_list + output_list}
    for coordinate in seed["placements"]:
        item = devices[coordinate["group"], coordinate["address"]]
        if item["availability"] != "used" or item.get("spatial", {}).get("status") == "not_applicable":
            raise ValueError(f"Cannot place {item['id']}")
        spatial = item.setdefault("spatial", {"status": "observed", "placements": []})
        spatial["placements"].append({
            "id": f"{item['id']}.placement-{len(spatial['placements']) + 1}",
            "space": "playfield", "role": coordinate["role"],
            "x": coordinate["x"], "y": coordinate["y"],
            "provenance": provenance(*coordinate["source_refs"], status="observed"),
        })
    switches = {d["binding"]["device"]: d for d in switch_list if d["binding"]["group"] == SWITCH}
    coils = {d["binding"]["device"]: d for d in coil_list}
    relays = [{
        "id": "relationship.mux-relay-feedback", "kind": "direct",
        "source": coils[12]["id"], "destination": switches[2]["id"], "provenance": provenance(CORE, MANUAL),
    }]
    flippers = flipper_column_relationships(
        flip_swno=(58, 57), matrix_ids={address: switches[address]["id"] for address in (57, 58)}, refs=(CORE,),
    )
    driver_index = {record["id"]: record for record in load_json(ROOT / "catalog/pinmame.json")["drivers"]}
    drivers = []
    for driver_id, note in DRIVERS.items():
        item = {key: driver_index[driver_id][key] for key in ("id", "description", "year", "manufacturer", "flags", "clone_of") if key in driver_index[driver_id]}
        item.update(physical_compatibility="identical", variant_notes=note)
        drivers.append(item)
    bounds = seed["bounds"]
    return {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {
            "id": MACHINE, "name": "Bad Cats", "manufacturer": "Williams", "year": 1989,
            "kind": "physical_pinball", "model_number": "575", "ipdb_id": 127, "opdb_id": "GrEBz-MBR3N",
            "playfield": {
                "width": bounds["right"] - bounds["left"], "height": bounds["bottom"] - bounds["top"],
                "units": "vpx", "provenance": provenance(TABLE),
            },
        },
        "coverage": {
            "status": "partial", "missing": seed["missing"],
            "dimensions": {
                "catalog_identity": "validated", "address_enumeration": "validated", "semantic_naming": "observed",
                "physical_wiring": "observed", "mechanisms": "observed", "variant_coverage": "validated",
                "recreation_knowledge": "observed", "spatial_placement": "observed",
            },
        },
        "controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
        "drivers": drivers, "inputs": switch_list, "outputs": output_list, "displays": displays(),
        "mechanisms": mechanisms(switches, coils), "relationships": relays + flippers,
        "sources": source_records(seed), "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"},
    }


def spatial_report(definition: dict, seed: dict) -> str:
    missing = [
        d for d in definition["inputs"] + definition["outputs"]
        if d["availability"] != "unused" and "spatial" not in d
    ]
    lines = [
        "# Bad Cats spatial audit", "", "Coverage is partial. Positions use x=0 at left and y=0 at the rear.",
        "", f"VPX `{seed['table']}` SHA-256 `{seed['table_sha256']}`.",
        f"Embedded script SHA-256 `{seed['script_sha256']}`.",
        f"Factory operations manual SHA-256 `{MANUAL_HASH}`.",
        f"vpxtool git:v0.33.3 extracted {seed['file_count']} files and {seed['total_bytes']} bytes.",
        f"Full manifest SHA-256 `{seed['manifest_sha256']}`. The manifest uses case-sensitive relative POSIX paths, file sizes and SHA-256, serialized as compact sorted-key JSON plus a final LF.",
        "", "VPX bounds are (0, 0) to (952, 2042). The normalization subtracts the left/top bounds and divides by width/height, rounded to six places.",
        "", *seed["spatial_notes"],
        "", f"## Observed placements ({len(seed['placements'])})", "",
        "| Group | Address | VPX item | Raw x, y | Normalized x, y | Evidence role |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| {p['group']} | {p['address']} | `{p['file']}` | {p['raw_x']}, {p['raw_y']} | {p['x']}, {p['y']} | {p['note']} |"
        for p in seed["placements"]
    )
    lines.extend(["", "## Used or unresolved addresses without a placement", ""])
    lines.extend(f"- {d['binding']['group']} {d['binding']['device']} · {d['label']}" for d in missing)
    return "\n".join(lines) + "\n"


def verify_retained(seed: dict) -> None:
    if directory := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        base = Path(directory) / "williams" / SLUG
        table = base / seed["table"]
        extraction = base / "extracted"
        if file_sha256(table) != seed["table_sha256"] or file_sha256(extraction / "script.vbs") != seed["script_sha256"]:
            raise ValueError("Retained Bad Cats VPX/script drift")
        if check_manifest(extraction, "bcats_l5") != seed["manifest_sha256"]:
            raise ValueError("Retained Bad Cats VPX manifest drift")
        entries = load_json(extraction / "manifest.json")["files"]
        if (len(entries), sum(row["size"] for row in entries)) != (seed["file_count"], seed["total_bytes"]):
            raise ValueError("Retained Bad Cats VPX extraction size drift")
        candidates = extract_spatial_candidates(extraction, table, "git:v0.33.3")
        if candidates["bounds"] != seed["bounds"]:
            raise ValueError("Retained Bad Cats VPX bounds drift")
        points = {(row["type"].lower(), row["name"].lower(), row["x"], row["y"]) for row in candidates["objects"]}
        for placement in seed["placements"]:
            identity = (placement["vpx_type"].lower(), placement["anchor"].lower(), placement["x"], placement["y"])
            if identity not in points or not (extraction / placement["file"]).is_file():
                raise ValueError(f"Retained Bad Cats object coordinate drift: {identity}")
    if directory := os.environ.get("PINMAME_MANUALS_ROOT"):
        base = Path(directory) / "by-machine" / MACHINE
        for name, digest in {
            MANUAL_FILE: MANUAL_HASH,
            "seafood-stepper-schematic.pdf": "95abd83b4ca94f226ace714ee0e99638f665e1408bc75599dc504f1aeeb2bc0d",
        }.items():
            if file_sha256(base / name) != digest:
                raise ValueError(f"Retained Bad Cats manual drift: {name}")
    if directory := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        base = Path(directory) / SLUG
        if file_sha256(base / "ipdb-127.html") != IPDB_HASH:
            raise ValueError("Retained Bad Cats identity capture drift")
        for relative, digest in seed["review_hashes"].items():
            if file_sha256(base / relative) != digest:
                raise ValueError(f"Retained Bad Cats review artifact drift: {relative}")
        for run in load_json(ROOT / RUNTIME_PATH)["runtime"]["raw_runs"]:
            if file_sha256(base / "runtime" / f"l5-{run['name']}-20261120.json") != run["sha256"]:
                raise ValueError(f"Retained Bad Cats diagnostic drift: {run['name']}")

    for run in load_json(ROOT / RUNTIME_PATH)["runtime"]["raw_runs"]:
        if file_sha256(ROOT / run["scenario_path"]) != run["scenario_sha256"]:
            raise ValueError(f"Bad Cats diagnostic scenario drift: {run['scenario_path']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if (ROOT / "machines/author-ready/williams" / DEFINITION.name).exists():
        raise ValueError("Refusing to overwrite author-ready Bad Cats")
    seed = load_json(SEED / f"{SLUG}-geometry.json")
    verify_retained(seed)
    definition = build(seed)
    outputs = {
        DEFINITION: canonical_bytes(definition),
        KNOWLEDGE: (SEED / f"{SLUG}-knowledge.md").read_bytes(),
        REPORT: spatial_report(definition, seed).encode("utf-8"),
    }
    for relative, payload in outputs.items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                raise ValueError(f"Bad Cats curator drift: {relative}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    print(f"{MACHINE}: partial, {len(seed['placements'])} observed placements")


if __name__ == "__main__":
    main()
