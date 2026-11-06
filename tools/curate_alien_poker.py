"""Build the partial Alien Poker records from pinned, game-specific evidence.

No external evidence is required to reproduce the records. When optional evidence roots are
configured, their pinned artifacts must match. Source roles and curation decisions are pinned explicitly;
this tool preserves the remaining physical-placement blockers and never promotes the record.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from functools import cache
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from tools.alien_poker_runtime import runtime_evidence

ROOT = Path(__file__).resolve().parents[1]
REV = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
MANUAL = "manual.alien-poker.booklet"
CORE = "pinmame.core.alien-poker"
SCRIPT = "vpx-script.alien-poker.jpsalas"
TABLE = "vpx-table.alien-poker.jpsalas"
EXCERPT = "evidence/excerpts/williams.alien-poker.1980/factory-tables.md"
OLIVER_EXCERPT = "evidence/excerpts/williams-oliver.alien-poker.1980/conversion.md"
OLIVER_EXCERPT_HASH = 'f3ac7d95e4a99984b1a4b06fb57371bca88f1124a805b5a676568a273a77eb2b'
OLIVER_HASH = "4122ff6b9fc5dc6a27cee66605e8a9dd49f893cf55392499225cddbfe5820278"
MANUAL_HASH = "e51781256a100cf9d502c1f94bb77755f36c0e2409bec82ad0293db1c35afb99"
TABLE_HASH = "0d3d61ba86415cd68b97e03bc6f52038a96906fae106bb3315f43f19577361e2"
SCRIPT_HASH = "808b4cd61e0d836a593cf733ae47c09a180e739954314cb55910db2ba4f6e9f7"
PRODUCTION = "machines/partial/williams/alien-poker-1980.json"
CONVERSION = "machines/partial/williams-oliver/alien-poker-1980.json"
SEED = "tools/seeds/williams/alien-poker-1980.json"
CONVERSION_SEED = "tools/seeds/williams-oliver/alien-poker-1980.json"

SWITCHES = [
    "Plumb Bob Tilt",
    "Ball Roll Tilt",
    "Credit Button",
    "Right Coin Switch",
    "Center Coin Switch",
    "Left Coin Switch",
    "Slam Tilt",
    "High Score Reset",
    "Outhole",
    "A Drop Target",
    "Left Special",
    "Left Inside Rollover",
    "Left Kicker",
    "Lower Left Joker Target",
    "Spade Ace Eject Hole",
    "Middle Left Joker Target",
    "Spinner",
    "K Drop Target",
    "Lower Top Standup",
    "Top Joker Target",
    "Top Standup",
    "Club Ace Eject Hole",
    "King of Hearts Rollover",
    "King of Clubs Rollover",
    "King of Diamonds Rollover",
    "Q Drop Target",
    "King of Spades Rollover",
    "Top Right Standup",
    "Heart Ace Eject Hole",
    "Right Joker Target",
    "Playfield Tilt",
    "Right Special",
    "Lower Right Standup",
    "J Drop Target",
    "Center Jet Bumper",
    "Left Jet Bumper",
    "Right Jet Bumper",
    "Bottom Jet Bumper",
    "Left Center Standup",
    "Right Center Standup",
    "5 Bank Standup",
    "10 Drop Target",
    "Right Flipper Lane Change Switch",
]
LAMPS = [
    "Same Player Shoots Again",
    "Left Special",
    "Right Special",
    "P",
    "O",
    "K",
    "E",
    "R",
    "2X",
    "3X",
    "4X",
    "5X",
    "Heart King",
    "Club King",
    "Diamond King",
    "King",
    "Royal Flush 2X",
    "Royal Flush 3X and Left Spin 1000",
    "Royal Flush 4X",
    "Royal Flush 20,000",
    "Royal Flush 40,000",
    "Royal Flush 60,000",
    "Royal Flush 80,000",
    "Royal Flush 100,000",
    "Ace of Hearts",
    "Ace of Spades",
    "Ace of Clubs",
    "Advance Royal Flush",
    "Left Jet Bumper",
    "Center Jet Bumper",
    "Bottom Jet Bumper",
    "Right Jet Bumper",
    "Lower Left Joker",
    "Middle Left Joker",
    "Top Left Joker",
    "Right Joker",
    "Extra Ball When Lit",
    "20,000 Bonus",
    "40,000 Bonus",
    "2,000 Bonus",
    "4,000 Bonus",
    "6,000 Bonus",
    "8,000 Bonus",
    "10,000 Bonus",
    "12,000 Bonus",
    "14,000 Bonus",
    "16,000 Bonus",
    "18,000 Bonus",
    "Not Used",
    "1 Can Play",
    "2 Can Play",
    "3 Can Play",
    "4 Can Play",
    "Match",
    "Ball in Play",
    "Credits (Playfield)",
    "Player 1 Up",
    "Player 2 Up",
    "Player 3 Up",
    "Player 4 Up",
    "Tilt",
    "Game Over",
    "Same Player Shoots (Backbox)",
    "High Score",
]
COILS = [
    "Ball Release", "Spade Ace Eject Hole", "Heart Ace Eject Hole", "10 Drop Target Reset", "J Drop Target Reset",
    "Q Drop Target Reset", "K Drop Target Reset", "A Drop Target Reset", "Sound 1", "Sound 2", "Sound 3", "Sound 4",
    "Sound 5", "Credit Knocker", "Club Ace Eject Hole", "Coin Lockout", "Center Jet Bumper", "Right Jet Bumper",
    "Left Jet Bumper", "Bottom Jet Bumper", "Drop Target Release", "Left Kicker", "Game On Enable"
]
# The shared spatial extractor computed these centres from the exact retained table. Only script-bound
# physical switches are included; no lamp render helpers are represented as physical bulbs.
MANIFEST_HASH = "c35dcc798caf34769c3f525d4a0a10bc2c554f7cfb1eb410e7b19703706b3c16"
BUNDLE_MANIFEST_HASH = "256a0d082e6b189e0968d0dad2d618452fc837c7f923651f4480bfcdf4c4d87a"
SW_COLUMNS = [("GRN-BRN", "2J2-9"), ("GRN-RED", "2J2-8"), ("GRN-ORN", "2J2-7"), ("GRN-YEL", "2J2-6"),
              ("GRN-BLK", "2J2-5"), ("GRN-BLU", "2J2-3"), ("GRN-VIO", "2J2-2"), ("GRN-GRY", "2J2-1")]
SW_ROWS = [("WHT-BRN", "2J3-9"), ("WHT-RED", "2J3-8"), ("WHT-ORN", "2J3-7"), ("WHT-YEL", "2J3-6"), ("WHT-GRN", "2J3-5"),
           ("WHT-BLU", "2J3-4"), ("WHT-VIO", "2J3-3"), ("WHT-GRY", "2J3-1")]
LAMP_COLUMNS = [("YEL-BRN", "2J5-8"), ("YEL-RED", "2J5-9"), ("YEL-ORN", "2J5-6"), ("YEL-BLK", "2J5-7"),
                ("YEL-GRN", "2J5-3"), ("YEL-BLU", "2J5-5"), ("YEL-VIO", "2J5-1"), ("YEL-GRY", "2J5-2")]
LAMP_ROWS = [("RED-BRN", "2J7-1"), ("RED-BLK", "2J7-2"), ("RED-ORN", "2J7-3"), ("RED-YEL", "2J7-4"),
             ("RED-GRN", "2J7-5"), ("RED-BLU", "2J7-6"), ("RED-VIO", "2J7-9"), ("RED-GRY", "2J7-8")]
COIL_WIRING = [("GRY-BRN", "2P11-4, 8P3-17", "Q15", "SA-23-850-DC"),
               ("GRY-RED", "2P11-5, 8P3-18", "Q17", "SG3-23-850-DC"),
               ("GRY-ORN", "2P11-7, 8P3-19", "Q19", "SG3-23-850-DC"),
               ("GRY-YEL", "2P11-8, 8P3-20", "Q21", "SA3-24-750-DC"),
               ("GRY-GRN", "2P11-9, 8P3-21", "Q23", "SA3-24-750-DC"),
               ("GRY-BLU", "2P11-3, 8P3-22", "Q25", "SA3-24-750-DC"),
               ("GRY-VIO", "2P11-2, 8P3-23", "Q27", "SA3-24-750-DC"),
               ("GRY-BLK", "2P11-1, 8P3-24", "Q29", "SA3-24-750-DC"), ("BRN-BLK", "2P9-9, 10P3-3", "Q31", None),
               ("BRN-RED", "2P9-7, 10P3-2", "Q33", None), ("BRN-ORN", "2P9-1, 10P3-5", "Q35", None),
               ("BRN-YEL", "2P9-2, 10P3-4", "Q37", None), ("BRN-GRN", "2P9-3, 10P3-7", "Q39", None),
               ("BRN-BLU", "2P9-4, 7P1-16", "Q41", "SA-23-850-DC"), ("BRN-VIO", "2P9-5, 8P3-1", "Q43", "SG-23-850-DC"),
               ("BRN-GRY", "2P9-6, 7P1-18, 7P2-4", "Q45", "SM-35-4000-DC"),
               ("BLU-BRN", "2P12-7, 8P3-11", "Q2", "SG-23-850-DC"), ("BLU-RED", "2P12-4, 8P3-12", "Q4", "SG-23-850-DC"),
               ("BLU-ORN", "2P12-3, 8P3-13", "Q6", "SG-23-850-DC"), ("BLU-YEL", "2P12-6, 8P3-14", "Q8", "SG-23-850-DC"),
               ("BLU-GRN", "2P12-8, 8P3-15", "Q10", "SA3-24-750-DC"),
               ("BLU-BLK", "2P12-9, 8P3-16", "Q12", "SG-23-800-DC")]
# The coil physically acts on the identified eject hole, target or bumper; this is a disclosed
# mechanism projection, not a claim that the table object marks the under-playfield coil centre.
COIL_PROJECTIONS = {2: 15, 3: 29, 4: 42, 5: 34, 6: 26, 7: 18, 8: 10, 15: 22, 17: 35, 18: 37, 19: 36, 20: 38}


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(refs)}


EXCERPT_HASHES = {'evidence/excerpts/williams.alien-poker.1980/factory-tables.md': 'd144f26bbb11a935ab9fcc32fe2445fb2d17c5d0a6fef05d8c6e1aab014493a1', 'evidence/excerpts/williams.alien-poker.1980/operation-and-diagnostics.md': '10cc08362f92abd4aca2191d3fc29a9b83d4999fafd9c3289677ad018b3b4446', 'evidence/excerpts/williams.alien-poker.1980/physical-observations.md': '96cfbd98fbdee5a79f9267153c02fdc9c49a8a7b5e2cbb94e7269d4853ce4389', 'evidence/excerpts/williams.alien-poker.1980/script-bindings.md': '261694dbf5152127adfe8f42feaac8fdc120ae16eb8e522fe709f7c03718eb46', 'evidence/excerpts/williams.alien-poker.1980/switch-locations.md': '5e1785261f4f84ed4dbf4ea5c7149d37d511b0040b9d80cfa6a04edf0c7e1378', 'evidence/excerpts/williams.alien-poker.1980/switch-locations.webp': 'b1110a7af26462033f52345a2d5dc1c443cd28aa2383948f92eca3ffdd96545f', 'evidence/excerpts/williams-oliver.alien-poker.1980/conversion.md': 'f3ac7d95e4a99984b1a4b06fb57371bca88f1124a805b5a676568a273a77eb2b'}
DATA_HASH = 'ff98b17d962db47638d898d9816e06845eb0d925a9e95316150904fe5b4b52af'
KNOWLEDGE = (ROOT / "tools/seeds/williams/alien-poker-1980-knowledge.md").read_text(encoding="utf8")
CONVERSION_KNOWLEDGE = (ROOT / "tools/seeds/williams-oliver/alien-poker-1980-knowledge.md").read_text(encoding="utf8")

DATA_PATH = "tools/seeds/williams/alien-poker-1980-evidence.json"
RUNTIME = "runtime.alien-poker.production"
PHOTOS = "human-review.alien-poker.physical"
LIBRARY = "vpx-script.alien-poker.libraries"
OLIVER = "human-review.oliver-alien-poker-conversion"
EXCERPT_DIR = "evidence/excerpts/williams.alien-poker.1980"
RUNTIME_PATH = "evidence/runtime/system-6/alien-poker-1980.json"


@cache
def data() -> dict:
    return load_json(ROOT / DATA_PATH)


def excerpt(name: str, locator: str, *, image: bool = False) -> dict:
    path = f"{EXCERPT_DIR}/{name}.md"
    record = {
        "id": name,
        "path": path,
        "sha256": EXCERPT_HASHES[path],
        "locator": locator,
        "method": "mixed",
        "transcribed_by": "Game-definition curators; visually checked and corrected against retained source renders",
        "reviewed": True
    }
    if image:
        record.update(
            image=f"{EXCERPT_DIR}/switch-locations.webp",
            image_sha256="b1110a7af26462033f52345a2d5dc1c443cd28aa2383948f92eca3ffdd96545f",
            image_derivation=
            "Alien_Poker_op.pdf page 10, crop box 0.025,0.085,0.56,0.71, scanned page rendered at its native resolution (embedded image xref 45, 2152px across 5.38in), rendered at 365 dpi, capped to 1050px wide, grayscale, 1051x2008 WebP quality 65"
        )
    return record


def sources() -> list[dict]:
    retained = data()
    return [
        {
            "id": CORE,
            "kind": "pinmame_core",
            "uri": f"https://github.com/vpinball/pinmame/tree/{REV}",
            "revision": REV,
            "locator": "src/wpc/s6games.c: INITGAMEFULL(alpok), all six production ROM blocks and free-play header; s6.c: s6_7digit_disp, s6_swrow_r, s6_dips_r, setSSSol, s6_vblank; s6.h: S6_COMPORTS; core.c: core_updateSw, core_swSeq2m/core_m2swSeq; wmssnd.c: sound DIP bits",
            "license": "BSD-3-Clause",
            "attribution": "PinMAME contributors"
        },
        {
            "id": MANUAL,
            "kind": "manual",
            "uri": "https://archive.org/download/arcademanual_Alien_Poker_op/Alien_Poker_op.pdf",
            "source_id": "arcademanual_Alien_Poker_op",
            "original_filename": "Alien_Poker_op.pdf",
            "rights": "No rights metadata supplied by Internet Archive; original retained locally only",
            "sha256": MANUAL_HASH,
            "acquired_at": retained["manual_acquired_at"],
            "locator": "https://archive.org/details/arcademanual_Alien_Poker_op; uploader manuallibrary@textfiles.com; Williams 16P-501-103, October 1980, PDF pages 1-12 = printed pages 1-12; identical original also verified through IPDB 48 https://www.ipdb.org/files/48/Williams_1980_Alien_Poker_Manual.pdf",
            "license": "NOASSERTION",
            "attribution": "Williams Electronics, Inc.; Internet Archive uploader manuallibrary@textfiles.com",
            "excerpts": [
                excerpt("factory-tables", "Figures 3,5,6 and Table 3; pp8,9,11,12"),
                excerpt("operation-and-diagnostics",
                        "pp1-3,7; board requirements, operation, diagnostics and Master Command"),
                excerpt("switch-locations", "Figure 4, p10, playfield drawing", image=True)
            ]
        },
        {
            "id": SCRIPT,
            "kind": "vpx_script",
            "uri": "external:pinmame-vpx-sources/williams/alien-poker-1980/extracted/script.vbs",
            "sha256": SCRIPT_HASH,
            "locator": "JPSalas v1.0.1, metadata 29.12.2017; alpok_l6; InitSw/InitDrop/InitSaucer, switch handlers, SolCallback and UpdateLamps; matching semantic signatures in pinned vpxtable_scripts sidecar",
            "license": "NOASSERTION",
            "attribution": "JPSalas; source pictures credited to Akiles5000 in table metadata",
            "known_working": True,
            "excerpts": [excerpt("script-bindings", "script.vbs runtime bindings; original file retained unchanged")]
        },
        {
            "id": TABLE,
            "kind": "vpx_table",
            "uri": "external:pinmame-vpx-sources/williams/alien-poker-1980/Alien Poker (Williams 1980).vpx",
            "sha256": TABLE_HASH,
            "locator": "Exact local JPSalas 1.0.1 table; vpxtool git:v0.33.3; extracted bounds(0,0)-(952,1974); complete extraction manifest and object register in spatial report",
            "license": "NOASSERTION",
            "attribution": "JPSalas; Akiles5000 source pictures"
        },
        {
            "id": LIBRARY,
            "kind": "vpx_script",
            "uri": "external:pinmame-vpx-sources/williams/alien-poker-1980/libraries/s6.vbs",
            "sha256": "51540940fc31d7afccbee636815c40369fa852b86116339c641073845a6ad24a",
            "locator": "Retained VPinMAME s6.vbs swLRFlip 82/swLLFlip 84 and vpmKeyDown/Up; accompanying core.vbs hash recorded in excerpt and evidence fixture",
            "license": "NOASSERTION",
            "attribution": "VPinMAME script-library contributors",
            "excerpts": [excerpt("script-bindings", "s6.vbs constants and key handlers; core.vbs helper contract")]
        },
        {
            "id": RUNTIME,
            "kind": "runtime_scenario",
            "uri": f"repository:{RUNTIME_PATH}",
            "sha256": retained["runtime_manifest"]["sha256"],
            "revision": REV,
            "locator": "Retained review-artifacts/williams.alien-poker.1980/runtime manifest: three fresh initialization boots plus production solenoid, switch and gameplay runs; digest is canonical directory manifest, not one raw run. Command/scenario/ROM/binary hashes in compact evidence.",
            "license": "MIT",
            "attribution": "PinMAME contributors and game-definition curators"
        },
        {
            "id": PHOTOS,
            "kind": "human_review",
            "uri": "https://www.ipdb.org/machine.cgi?id=48",
            "sha256": "6f044600e7b8d6148783471c1e32a0b0c1f69ed12e70485e2a3cb31a1b661bed",
            "acquired_at": "2026-11-06T08:42:46.764239+00:00",
            "locator": "Verified IPDB 48 capture https://web.archive.org/web/20250108064548id_/https://www.ipdb.org/machine.cgi?id=48; image 19 Jean-Pierre Renault, images 21/23/24 Mark Steinman; direct image URLs and immutable hashes in report. Pinside CUJO original bank post 1 and dated 2024-10-23 removed-PCB photographs, rebuild post 5. Generic factory D8362 drawing inspected and rejected as fitment evidence.",
            "license": "NOASSERTION",
            "attribution": "IPDB photographers Jean-Pierre Renault and Mark Steinman; Pinside CUJO and koen12344; Williams parts catalog",
            "excerpts": [
                excerpt(
                    "physical-observations",
                    "IPDB production photos; Pinside Alien Poker 5-Bank Drop Rebuild posts 1/5 and dated 2024-10-23 PCB photographs"
                )
            ]
        },
        *[{
            "id": resource["id"],
            "kind": "human_review",
            "uri": resource["url"],
            "sha256": resource["sha256"],
            "acquired_at": resource["acquired_at"],
            "source_id": "48",
            "original_filename": resource["url"].rsplit("/", 1)[1],
            "locator": "Verified IPDB 48 https://www.ipdb.org/machine.cgi?id=48; acquired through Wayback; " + resource["role"],
            "license": "NOASSERTION",
            "attribution": resource["attribution"],
        } for resource in retained["photo_resources"]],
    ]


def device(group: str, n: int, label: str, kind: str, refs: tuple[str, ...], availability: str) -> dict:
    prefix = {
        "pinmame.input.switch": "switch",
        "pinmame.input.dip": "dip",
        "pinmame.output.solenoid": "solenoid",
        "pinmame.output.lamp": "lamp"
    }[group]
    namespace = group.replace("input.", "").replace("output.", "")
    aliases = [str(n)]
    if group == "pinmame.input.switch" and n > 0:
        aliases = list(dict.fromkeys([str(n), f"{n:02d}", f"{n:03d}"]))
    return {
        "id": f"{prefix}.{f'n{-n}' if n < 0 else n}",
        "label": label,
        "kind": kind,
        "binding": {
            "group": group,
            "device": n
        },
        "aliases": [{
            "namespace": namespace,
            "value": value
        } for value in aliases],
        "availability": availability,
        "provenance": provenance(*refs)
    }


def not_applicable(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*(refs or (MANUAL, CORE)))}


def located(device_id: str, names: list[str], role: str, *refs: str) -> dict:
    objects = data()["objects"]
    return {
        "status": "observed",
        "placements": [{
            "id": f"{device_id}.{role}-{i+1}",
            "role": role,
            "space": "playfield",
            "x": objects[name]["x"],
            "y": objects[name]["y"],
            "provenance": provenance(TABLE, SCRIPT, MANUAL, *refs, status="observed")
        } for i, name in enumerate(names)]
    }


def drivers() -> list[dict]:
    descriptions = {
        "l2": "L-2",
        "l2ff": "L-2 Free Play Fix",
        "l6": "L-6",
        "l6ff": "L-6 Free Play Fix",
        "f6": "L-6, French Speech",
        "f6ff": "L-6, French Speech, Free Play Fix"
    }
    result = []
    for suffix, description in sorted(descriptions.items()):
        row = {
            "id": f"alpok_{suffix}",
            "description": f"Alien Poker ({description})",
            "year": "1980",
            "manufacturer": "Williams",
            "flags": 0,
            "physical_compatibility": "identical",
            "variant_notes": "Same GEN_S6, init, I/O and seven-digit display layout. " +
            ("French speech ROMs replace the English speech set. " if suffix.startswith("f") else "") +
            ("Patched green1fpfix.716 restores credit knocker in free play."
             if suffix.endswith("ff") else "Factory production program/speech configuration.")
        }
        if suffix != "l6": row["clone_of"] = "alpok_l6"
        result.append(row)
    return result


def build() -> dict:
    inputs = []
    for n, label in zip(
            range(-7, -2),
        ["Advance", "Auto-Up / Manual-Down", "CPU Diagnostic", "Sound Diagnostic", "Master Command Enter"]):
        item = device("pinmame.input.switch", n, label, "switch", (CORE, MANUAL), "used")
        item.update(physical={
            "location": "cabinet/service",
            "switch_type": "other" if n == -6 else "button"
        },
                    spatial=not_applicable("cabinet_or_service"))
        inputs.append(item)
    for n in range(1, 65):
        item = device("pinmame.input.switch", n, SWITCHES[n - 1] if n <= 43 else "Not Used",
                      "switch" if n <= 43 else "virtual", (MANUAL, CORE, RUNTIME), "used" if n <= 43 else "unused")
        col, row = SW_COLUMNS[(n - 1) // 8], SW_ROWS[(n - 1) % 8]
        item["wiring"] = {
            "drive_wire": col[0],
            "drive_connection": col[1],
            "return_wire": row[0],
            "return_connection": row[1]
        }
        if n > 43: item["spatial"] = not_applicable("unused")
        else:
            item["normally_closed"] = False
            item["physical"] = {
                "location": "cabinet/service" if n <= 8 else "playfield",
                "notes": "Unmasked System 6 row read and ROM Test 03 active 1 establish a normally-open matrix contact; no controller-wide inversion is reapplied."
            }
            if n in (10, 18, 26, 34, 42):
                item["physical"].update(
                    switch_type="other",
                    part_number="1B-2001-124-4",
                    notes=
                    "Original horseshoe PCB and mechanical slider; full-down contact closes and stays closed until this target rises. Factory table, original CUJO photos, raw read path and ROM Test 03 agree. Replacement magnetic/opto boards are not factory construction."
                )
                item["provenance"] = provenance(MANUAL, CORE, RUNTIME, PHOTOS, SCRIPT)
            if str(n) in data()["switch_objects"]:
                name = data()["switch_objects"][str(n)]
                item["spatial"] = located(item["id"], [name], "sensor", PHOTOS)
                if n == 13:
                    item["physical"][
                        "notes"] += " Position projects the scoring contact assembly onto its own LeftSlingshot rubber wall centroid; it is not a measured leaf-contact location."
            elif n <= 8:
                item["spatial"] = not_applicable("cabinet_or_service")
            else:
                item["physical"][
                    "notes"] += " Physical position unresolved; Drain/BallRelease or the factory remote dashed label must not be treated as the fitted device centre."
            if n == 43:
                item["kind"] = "virtual"
                item.pop("normally_closed")
                item["spatial"] = not_applicable("virtual", CORE, RUNTIME)
                item["physical"] = {
                    "notes": "The factory matrix prints 43 RIGHT FLIPPER LANE CHANGE SWITCH; Figure 4 draws it in a dashed circle beside the upper right flipper. The contact's mounting and construction are unresolved. In PinMAME core_updateSw copies public 82 into 43 every update. Drive 82; direct 43 is overwritten. The single-write button probe proves the emulator copy, not the factory contact's location or polarity. The script's redundant 43 write has no independent effect."
                }
        inputs.append(item)
    for n in range(81, 89):
        item = device("pinmame.input.switch", n, {
            82: "Right Flipper Button",
            84: "Left Flipper Button"
        }.get(n, "Unused Flipper Column Position"), "virtual", (CORE, LIBRARY, RUNTIME),
                      "used" if n in (82, 84) else "unused")
        item["spatial"] = not_applicable("cabinet_or_service" if n in (82, 84) else "unused")
        if n in (82, 84):
            item["physical"] = {
                "location": "cabinet",
                "notes": "Host input bit for the cabinet button. Right controls both right flippers; left controls one. Synthetic output pairs do not measure separate physical windings."
            }
        inputs.append(item)
    for n in [1, 2, *range(9, 25)]:
        used = n in (1, 2, 17, 18, 19)
        label = f"Sound Board Option DS1 Position {n}" if n <= 2 else ({
            17: "Master Command 8 - Zero Audits",
            18: "Master Command 7 - Restore Factory Settings",
            19: "Master Command 6 - Auto-Cycle"
        }.get(n, f"Unused CPU Function Position {n}"))
        item = device("pinmame.input.dip", n, label, "dip_switch", (CORE, MANUAL), "used" if used else "unused")
        item.update(spatial=not_applicable("dip_switch"),
                    physical={
                        "location": "sound board" if n <= 2 else "CPU board",
                        "switch_type": "dip"
                    })
        if n <= 2:
            item["physical"][
                "notes"] = "Two emulator sound-option bits are folded into command bits 5/6. No game-specific option name is inferred; the booklet identifies D8224 but does not name these positions."
        elif n >= 20:
            item["physical"][
                "notes"] = "No function assigned by the game's Master Command diagram; lower function bank explicitly NOT USED. No adjustment is invented from the transport bit."
        inputs.append(item)
    outputs = []
    for n, label in enumerate(COILS, 1):
        kind = "control_signal" if 9 <= n <= 13 else "relay" if n in (16, 23) else "coil"
        item = device("pinmame.output.solenoid", n, label, kind, (MANUAL, CORE, SCRIPT, RUNTIME), "used")
        if n <= 22:
            wire, connection, transistor, part = COIL_WIRING[n - 1]
            item["wiring"] = {"drive_wire": wire, "drive_connection": connection, "driver_transistor": transistor}
            if part: item["physical"] = {"part_number": part}
        item.setdefault("physical", {})["location"] = "cabinet/service" if n in (
            14, 16, 23) else "internal sound board" if 9 <= n <= 13 else "playfield"
        if n in COIL_PROJECTIONS or n == 22:
            switch = COIL_PROJECTIONS.get(n, 13)
            item["spatial"] = located(item["id"], [data()["switch_objects"][str(switch)]], "effect", PHOTOS)
            item["physical"][
                "notes"] = "Effect projection onto this mechanism's own bound target/saucer/bumper/sling object, not the under-playfield coil centre."
        elif n == 21:
            item["spatial"] = located(item["id"], ["sw26"], "effect", PHOTOS)
            item["physical"][
                "notes"] = "Common release effect projected onto middle Q target of this five-target assembly; physical coil is separate/perpendicular, as shown by original bank photos."
        elif n != 1:
            item["spatial"] = not_applicable("internal_nonvisual" if 9 <= n <= 13 else "cabinet_or_service")
        if n in (18, 19):
            item["physical"][
                "notes"] += " Figure 3 reverses 18/19; Table 3, the game-data slots and gameplay show 18 right/19 left."
        if n == 1:
            item["physical"][
                "notes"] = "Single production outhole coil; shooter-lane BallRelease is a scripted serve proxy and does not locate this coil."
        if n == 23:
            item["physical"][
                "notes"] = "PIA3 CB2 enables the driver-board flipper relay and special circuits; public 23 is game-on, not a playfield coil."
        if n == 16:
            item["physical"][
                "notes"] = "Factory coin-lockout coil. Energized in the retained attract run; no playfield coordinate."
        outputs.append(item)
    for n in range(45, 49):
        item = device("pinmame.output.solenoid", n, f"Synthetic {'Right' if n <= 46 else 'Left'} Flipper State {n}",
                      "virtual", (CORE, RUNTIME), "used")
        item.update(
            spatial=not_applicable("virtual"),
            physical={
                "notes": "Fabricated from enabled cabinet-button state. Both members of each pair rise together; no independent EOS or winding current is measured."
            })
        outputs.append(item)
    for n, label in enumerate(LAMPS, 1):
        item = device("pinmame.output.lamp", n, label, "virtual" if n == 49 else "lamp", (MANUAL, SCRIPT, PHOTOS),
                      "unused" if n == 49 else "used")
        col, row = LAMP_COLUMNS[(n - 1) // 8], LAMP_ROWS[(n - 1) % 8]
        item["wiring"] = {
            "drive_wire": col[0],
            "drive_connection": col[1],
            "return_wire": row[0],
            "return_connection": row[1]
        }
        if n == 49: item["spatial"] = not_applicable("unused")
        elif n >= 50 and n != 56:
            item.update(
                spatial=not_applicable("cabinet_or_service"),
                physical={
                    "location": "backbox",
                    "notes": "Cabinet/backglass legend per factory matrix and physical backglass; table proxies 50-53 do not locate playfield bulbs."
                })
        elif n == 56:
            item["physical"] = {
                "location": "playfield",
                "notes": "Factory matrix says CREDITS(PLAYFIELD). l56 is on bare wood outside the painted field; it is not accepted as a physical socket. The conversion author reuses this real circuit, corroborating fitment but not a production position."
            }
        else:
            names = [f"l{n}"]
            if n == 18: names.append("l18a")
            if n == 37: names.append("l37a")
            if 29 <= n <= 32:
                names = [{29: "Bumper1", 30: "Bumper2", 31: "Bumper4", 32: "Bumper3"}[n]]
            item["physical"] = {
                "location": "playfield",
                "quantity": len(names),
                "notes": "Observed insert/feature projection from actual runtime binding, checked for side/order against production photographs; socket centre beneath artwork/plastics is not independently measured."
            }
            if n == 18:
                item["physical"]["notes"] += " Royal Flush 3X and spinner are two distinct emitters sharing 18."
            if n == 37:
                item["physical"][
                    "notes"] += " Factory(X2): upper Club and right Heart extra-ball arrows share 37; l37b is only a glow."
            if 29 <= n <= 32:
                item["physical"].pop("quantity")
                item["physical"][
                    "notes"] += " Both Light layers are excluded as separate sockets; one effect is projected onto the corresponding physical bumper centre. Hidden bulb quantity is unverified."
            item["spatial"] = located(item["id"], names, "emitter", PHOTOS)
        outputs.append(item)
    displays = []
    specs = [(f"Player {i}", start, 7) for i, start in enumerate([1, 9, 21, 29], 1)] + [("Ball in Play Tens", 0, 1),
                                                                                       ("Ball in Play Units", 8, 1),
                                                                                       ("Credit Tens", 20, 1),
                                                                                       ("Credit Units", 28, 1)]
    for i, (label, start, width) in enumerate(specs):
        displays.append({
            "id": f"display.{i}",
            "label": label,
            "kind": "segment",
            "controller_index": i,
            "segment_start": start,
            "width": width,
            "physical_location": "cabinet_or_service",
            "spatial": not_applicable("cabinet_or_service"),
            "provenance": provenance(CORE, MANUAL, RUNTIME, PHOTOS)
        })
    return {
        "format": "pinmame-machine-definition",
        "schema_version": 2,
        "machine": {
            "id": "williams.alien-poker.1980",
            "name": "Alien Poker",
            "manufacturer": "Williams",
            "year": 1980,
            "kind": "physical_pinball",
            "model_number": "501",
            "ipdb_id": 48,
            "opdb_id": "G4yen-MD12Y",
            "playfield": {
                "width": 952,
                "height": 1974,
                "units": "vpx",
                "provenance": provenance(TABLE)
            }
        },
        "coverage": {
            "status": "partial",
            "missing": ["polarity", "spatial_placement"],
            "dimensions": {
                "catalog_identity": "validated",
                "address_enumeration": "validated",
                "semantic_naming": "validated",
                "physical_wiring": "observed",
                "mechanisms": "validated",
                "variant_coverage": "validated",
                "recreation_knowledge": "validated",
                "spatial_placement": "observed"
            }
        },
        "controller": {
            "platform": "pinmame.system-6",
            "hardware_generation": "0x20000",
            "inversion_applied_by_emulator": True
        },
        "drivers": drivers(),
        "inputs": inputs,
        "outputs": outputs,
        "displays": displays,
        "mechanisms": mechanisms(),
        "relationships": relationships(),
        "sources": sources(),
        "knowledge": {
            "path": "knowledge/williams/alien-poker-1980.md",
            "status": "partial"
        },
        "conflicts": []
    }


def mechanisms() -> list[dict]:
    result = []

    def add(key, label, kind, coils, switches, behavior):
        result.append({
            "id": f"mech.{key}",
            "label": label,
            "kind": kind,
            "actuators": [f"solenoid.{n}" for n in coils],
            "sensors": [f"switch.{n}" for n in switches],
            "behavior": behavior,
            "provenance": provenance(MANUAL, SCRIPT, RUNTIME, PHOTOS)
        })

    add(
        "outhole", "Single-ball outhole and manual shooter", "kicker", [1], [9],
        "One ball drains under the apron onto switch 9; output 1 kicks it into the feed path to the shooter lane. The manual plunger launches it. Startup game-on enables play; a held drain contact can cause repeated serve attempts. The table's BallRelease is the final shooter proxy, not an extra physical trough coil. No production multiball trough exists."
    )
    for name, coil, sw in [("spade", 2, 15), ("heart", 3, 29), ("club", 15, 22)]:
        add(
            f"{name}-eject", f"{name.title()} Ace saucer", "kicker", [coil], [sw],
            f"Ball enters the {name} saucer and holds switch {sw}; output {coil} ejects it to the open field, releasing the contact. P-O-K-E-R/rule lamps control awards, not an additional lock mechanism. A lingering contact can be retried; actual kick strength, trajectory and animation timing are table-owned."
        )
    add(
        "royal-flush", "Five individually reset diamond drop targets and common release", "drop_target_bank",
        [4, 5, 6, 7, 8, 21], [42, 34, 26, 18, 10],
        "Order 10,J,Q,K,A. Each target slides in guides, latches up and drops with spring bias when struck. Its original horseshoe PCB closes at full down and stays closed until raised. Outputs 4,5,6,7,8 individually raise 10,J,Q,K,A; output 21 operates the common release and drops all five. Out-of-order targets reset individually; held contacts after a reset can cause ROM retries. Original bank photos show five separate plungers and perpendicular release. A generic single-lift bank is incorrect. Guide/contact friction, worn PCB tracks or springs can cause sticking, failed registration or rebound. No numeric mechanical timing is asserted."
    )
    for coil, sw, label in [(17, 35, "Center Jet"), (18, 37, "Right Jet"), (19, 36, "Left Jet"), (20, 38, "Bottom Jet"),
                            (22, 13, "Left Kicker")]:
        add(
            f"special-{coil}", label, "other", [coil], [sw],
            f"Scoring contact {sw} and its dedicated special-trigger circuit operate the same {label.lower()} assembly. Game-on23 gates the response; PinMAME's switch-driven slot publishes {coil}. Coil movement strikes the ball and returns mechanically. Gameplay confirms the address pair; there is no motor/home-position model."
        )
    add(
        "flippers", "Three cabinet-wired flippers", "other", [23], [82, 84],
        "The left cabinet button operates one flipper, the right operates both right flippers. Hardware EOS switches reduce coil power locally; the CPU only enables their supply. Public 45-48 are synthetic paired states, not individual CPU coil drivers or EOS measurements. Right 82 also supplies ROM lane-change 43. Springs return bats at release; table geometry and tuning remain table-owned."
    )
    add(
        "spinner", "Left passive spinner", "other", [], [17],
        "A passing ball rotates the free spinner and pulses 17. Royal Flush 3X/spinner lamp 18 changes the award; no motor or actuator is fitted."
    )
    return result


def relationships() -> list[dict]:
    return [{
        "id": f"relationship.special-{coil}",
        "kind": "pulse",
        "source": f"switch.{sw}",
        "destination": f"solenoid.{coil}",
        "provenance": provenance(CORE, MANUAL, RUNTIME)
    } for coil, sw in [(17, 35), (18, 37), (19, 36), (20, 38), (22, 13)]]


def conversion() -> dict:
    # A separate fail-closed record: a shared ROM init does not erase changed physical hardware.
    result = {
        "format": "pinmame-machine-definition",
        "schema_version": 2,
        "machine": {
            "id": "williams-oliver.alien-poker.1980",
            "name": "Alien Poker Multiball Conversion",
            "manufacturer": "Williams / Oliver",
            "year": None,
            "kind": "physical_conversion"
        },
        "controller": {
            "platform": "pinmame.system-6",
            "hardware_generation": "0x20000",
            "inversion_applied_by_emulator": True
        },
        "drivers": [{
            "id": "alpok_b6",
            "clone_of": "alpok_l6",
            "description": "Alien Poker (L-6, Multiball conversion)",
            "year": "2006",
            "manufacturer": "Williams / Oliver",
            "flags": 0,
            "physical_compatibility": "unknown",
            "variant_notes": "Hardware conversion documented by its author. Catalog 2006 is a firmware year, not an established conversion manufacture date. Physical Firepower-style and proposed alternative trough installations must not be conflated."
        }],
        "inputs": [],
        "outputs": [],
        "displays": [],
        "mechanisms": [],
        "relationships": [],
        "conflicts": [],
        "sources": [
            sources()[0], {
                "id": OLIVER,
                "kind": "human_review",
                "uri": "https://www.pinball4you.ch/okaegi/pro_alienmulti.html",
                "sha256": OLIVER_HASH,
                "acquired_at": "2026-11-06T08:42:45.029813+00:00",
                "locator": "Oliver Kaegi hardware and game-ROM sections; retained manual-root/by-machine/williams.alien-poker.1980/oliver-multiball.html; full physical changes, original and converted photographs",
                "license": "NOASSERTION",
                "attribution": "Oliver Kaegi",
                "excerpts": [{
                    "id": "conversion",
                    "locator": "hardware and software sections",
                    "path": OLIVER_EXCERPT,
                    "sha256": OLIVER_EXCERPT_HASH,
                    "method": "manual",
                    "transcribed_by": "Game-definition curators; checked against the retained author page and original/converted photographs",
                    "reviewed": True
                }]
            }
        ],
        "knowledge": {
            "path": "knowledge/williams-oliver/alien-poker-1980.md",
            "status": "partial"
        }
    }
    result["coverage"] = {
        "status": "partial",
        "missing": [
            "identity", "input_enumeration", "input_semantics", "output_enumeration", "output_semantics",
            "display_inventory", "mechanism_inventory", "mechanism_behavior", "polarity", "variant_differences",
            "provenance", "spatial_placement"
        ],
        "dimensions": {
            "catalog_identity": "candidate",
            "address_enumeration": "unknown",
            "semantic_naming": "candidate",
            "physical_wiring": "candidate",
            "mechanisms": "candidate",
            "variant_coverage": "candidate",
            "recreation_knowledge": "observed",
            "spatial_placement": "unknown"
        }
    }
    return result


def report() -> dict:
    retained = data()
    definition = build()
    return {
        "format": "pinmame-spatial-blockers",
        "version": 1,
        "machine_id": "williams.alien-poker.1980",
        "promotion_decision": "Remain partial; observed feature projections and unresolved physical sockets do not meet author readiness.",
        "coordinate_convention": {
            "space": "playfield",
            "x": "left 0/right 1",
            "y": "back 0/front 1",
            "bounds": {
                "left": 0,
                "top": 0,
                "right": 952,
                "bottom": 1974
            },
            "formula": "(x-left)/(right-left), (y-top)/(bottom-top), shared extractor rounded to six decimals"
        },
        "evidence": {
            "table_sha256": TABLE_HASH,
            "script_sha256": SCRIPT_HASH,
            "manual_sha256": MANUAL_HASH,
            "inner_extraction": {
                "file_count": 748,
                "bytes": 21693281,
                "sha256": MANIFEST_HASH
            },
            "retained_source_bundle": {
                "file_count": 751,
                "bytes": 37898424,
                "sha256": BUNDLE_MANIFEST_HASH
            },
            "manifest_algorithm": "tools/build_external_evidence_manifest.py: every relative POSIX path/size/SHA256, case-sensitive path sort, compact UTF8 JSON sorted keys plus LF; exclude only root manifest.json and manifest.sha256. Inner root is extracted; outer root includes table, extracted files and two libraries.",
            "runtime": retained["runtime_manifest"],
            "external_artifacts": retained["external_artifacts"],
            "production_photographs": retained["photo_resources"],
            "original_bank_photographs": retained["bank_photo_resources"],
        },
        "objects": retained["objects"],
        "switch_object_bindings": retained["switch_objects"],
        "projections": {
            "coil_effects": {
                str(n): f"switch {sw} assembly object"
                for n, sw in {
                    **COIL_PROJECTIONS, 22: 13
                }.items()
            },
            "coil 21": "middle Q target of the same bank; physical release actuator is perpendicular",
            "lamp 29-32": "one emitter projection per physical bumper; light layers are rendering doubles",
            "insert_lamps": "script-bound insert/feature centres are observed projections, not measured underside sockets"
        },
        "rejected_objects": {
            "lamp 56": "l56 on bare wood outside painted field; cannot locate factory CREDITS(PLAYFIELD)",
            "lamp 50-53": "backbox proxies placed along table edge",
            "lamp 2a-3a-13a-16a-37b": "Flasher glow helpers",
            "GI": "local visual effects do not establish physical sockets/string wiring",
            "Drain/BallRelease": "ball-transfer proxies do not locate production switch 9/coil 1",
            "switch 31": "factory dashed annotation is remote; actual position unmeasured"
        },
        "unplaced": [item["id"] for item in definition["inputs"] + definition["outputs"] if "spatial" not in item],
        "unplaced_physical_counterparts": ["switch.43"],
        "blockers": [
            "Exact service-contact construction remains outside the game's retained booklet; matrix contacts 1-42 have independent read-path and ROM polarity evidence.",
            "Factory lane-change contact 43 has unresolved mounting and construction. Its virtual PinMAME copy from cabinet input 82 does not establish physical location or polarity.",
            "Physical playfield credit socket 56 and under-apron switch 9/coil 1/tilt 31 lack a defensible measured position.",
            "Observed insert, raised-plastic and mechanism projections have not been independently established as every physical socket/contact centre.",
            "Uncontrolled GI socket inventory/wiring is incomplete; no separate System 6 public GI group exists. Do not fabricate one."
        ],
        "factory_reconciliation": "The curator visually compared factory Figures 3/4 and original production photos with exact retained PF overlays for count/side/order. No calibrated factory affine fit is claimed; no manual balloon supplied coordinates.",
        "related_conversion": "Separate partial williams-oliver.alien-poker.1980; production geometry does not validate its relocated hardware."
    }


def report_markdown() -> str:
    return """# Alien Poker spatial evidence and remaining blockers

**Partial.** The adjacent JSON pins the exact original VPX, complete extraction, native booklet,
production photographs and raw runtime evidence. Coordinates use x=0 left/x=1 right, y=0 back/y=1 front,
table bounds 952x1974 and the shared extractor. All accepted positions remain observed.

Script-bound switches include direct centres and the seven scored-wall centroids. Coil positions
are disclosed effects projected onto their own target/saucer/bumper/sling assemblies; release 21
projects onto this bank's middle target. Insert positions are observed feature projections.
Two 18 emitters and two 37 emitters are retained. Bumper light doubles and Flash/GI helpers never
become extra sockets. The factory diagrams and physical photos reconcile count, side and order;
they do not constitute an affine measurement or independently prove hidden socket centres.

Unplaced: switch 9, tilt 31, outhole coil 1 and physical credit lamp 56. Drain/BallRelease are table
ball-routing proxies. The factory's dashed 31 annotation is remote. l56 is on bare wood outside
the painted field, so it is rejected as a physical location. Backbox lamps 50-55/57-64 and the
cabinet/service devices have controlled not-applicable records. Constant GI is not a published
System 6 output group; the physical socket inventory remains incomplete.

The physical counterpart of virtual public switch 43 also has unresolved mounting and construction.
Figure 4 draws it beside the upper right flipper; the dashed circle does not locate its contact assembly.
The emulator copies cabinet input 82 into 43, which proves neither a cabinet mounting nor polarity.
Its public spatial record is not-applicable for reason virtual; this does not clear the physical gap.

The inner extraction manifest covers 748 files/21693281 bytes; the outer retained-source bundle
covers 751 files/37898424 bytes, adding the original table and two script libraries. These are
different roots with separate reproducible hashes, not competing extraction identities.
No whole manual, table, photograph, ROM or mutable NVRAM enters Git.
"""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_inputs(root: Path) -> None:
    for relative, expected in EXCERPT_HASHES.items():
        path = root / relative
        if not path.is_file() or digest(path) != expected:
            raise RuntimeError(f"Missing or changed excerpt: {relative}")
    if not (root / DATA_PATH).is_file() or digest(root / DATA_PATH) != DATA_HASH:
        raise RuntimeError("Missing or changed curation evidence seed")
    for manufacturer in ("williams", "williams-oliver"):
        if (root / f"machines/author-ready/{manufacturer}/alien-poker-1980.json").exists():
            raise RuntimeError("Refusing to overwrite an author-ready Alien Poker artifact")
    retained = load_json(root / DATA_PATH)
    for key, env in [("manuals", "PINMAME_MANUALS_ROOT"), ("vpx", "PINMAME_VPX_SOURCES_ROOT"),
                     ("review", "PINMAME_REVIEW_ARTIFACTS_ROOT")]:
        if not os.environ.get(env): continue
        base = Path(os.environ[env])
        for relative, record in retained["external_artifacts"][key].items():
            path = base / relative
            if not path.is_file() or path.stat().st_size != record["size"] or digest(path) != record["sha256"]:
                raise RuntimeError(f"Missing or changed retained artifact: {path}")
    if os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        from tools.build_external_evidence_manifest import build_manifest, canonical_bytes as manifest_bytes
        from pinmame_game_defs.spatial import extract_spatial_candidates
        base = Path(os.environ["PINMAME_VPX_SOURCES_ROOT"]) / "williams/alien-poker-1980"
        for directory, expected in [(base / "extracted", MANIFEST_HASH),
                                    (base, BUNDLE_MANIFEST_HASH)]:
            if hashlib.sha256(manifest_bytes(build_manifest(directory, "alpok_l6")) + b"\n").hexdigest() != expected:
                raise RuntimeError(f"Extraction manifest drift: {directory}")
        actual = {
            o["name"]: o
            for o in extract_spatial_candidates(base / "extracted", base /
                                                "Alien Poker (Williams 1980).vpx", "git:v0.33.3")["objects"]
        }
        if any(actual.get(name) != value for name, value in retained["objects"].items()):
            raise RuntimeError("Retained object centre or derivation drift")
    if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        from tools.build_external_evidence_manifest import build_manifest, canonical_bytes as manifest_bytes
        directory = Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) / "williams.alien-poker.1980/runtime"
        actual = build_manifest(directory, "alpok_l6")
        if hashlib.sha256(manifest_bytes(actual) + b"\n").hexdigest() != retained["runtime_manifest"]["sha256"]:
            raise RuntimeError("Raw runtime evidence manifest drift")
        if runtime_evidence(directory) != runtime_evidence():
            raise RuntimeError("Runtime observations differ from pinned compact evidence")


def artifacts() -> dict[str, object]:
    production, converted = build(), conversion()
    return {
        PRODUCTION: production,
        SEED: production,
        CONVERSION: converted,
        CONVERSION_SEED: converted,
        "knowledge/williams/alien-poker-1980.md": KNOWLEDGE,
        "knowledge/williams-oliver/alien-poker-1980.md": CONVERSION_KNOWLEDGE,
        "reports/spatial/williams/alien-poker-1980.json": report(),
        "reports/spatial/williams/alien-poker-1980.md": report_markdown(),
        RUNTIME_PATH: runtime_evidence()
    }


def check(root: Path = ROOT) -> None:
    verify_inputs(root)
    for name, value in artifacts().items():
        expected = canonical_bytes(value) if isinstance(value, dict) else value.encode("utf8")
        if not (root / name).is_file() or (root / name).read_bytes() != expected:
            raise RuntimeError(f"Missing or drifted artifact: {name}")


def generate(root: Path = ROOT) -> None:
    verify_inputs(root)
    for name, value in artifacts().items():
        if isinstance(value, dict): write_json(root / name, value)
        else: write_text(root / name, value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        print("Alien Poker artifacts match the curator.")
    else:
        generate()
        print("Generated partial Alien Poker contribution.")


if __name__ == "__main__": main()
