"""Reproduce the evidence-bounded SlugFest first-model definition and spatial report.

No external source is needed for ordinary regeneration. Optional evidence roots verify
the retained bytes and every spatial seed against the extraction, rather than silently
substituting another table. Candidate positions and unresolved hardware remain partial.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text
from build_external_evidence_manifest import check_manifest

ROOT = Path(__file__).resolve().parents[1]
MACHINE_ID = "williams.slugfest-l-1.1991"
SLUG = "slugfest-l-1-1991"
MACHINE_PATH = ROOT / "machines/partial/williams" / f"{SLUG}.json"
AUTHOR_READY_PATH = ROOT / "machines/author-ready/williams" / f"{SLUG}.json"
KNOWLEDGE_PATH = ROOT / "knowledge/williams" / f"{SLUG}.md"
KNOWLEDGE_SEED_PATH = ROOT / "tools/seeds/williams" / f"{SLUG}-knowledge.md"
SPATIAL_SEED_PATH = ROOT / "tools/seeds/williams" / f"{SLUG}-spatial.json"
REPORT_PATH = ROOT / "reports/spatial/williams" / f"{SLUG}.json"
REPORT_MARKDOWN_PATH = ROOT / "reports/spatial/williams" / f"{SLUG}.md"
EXCERPT_ROOT = ROOT / "evidence/excerpts" / MACHINE_ID
PINMAME_REVISION = "97aa922bf8e4b6970126192ec1ac1fb0305a4f62"
TABLE_SHA256 = "c75825c0c39fcd89cc9d6c7c60d18fe3257e2c0a07a6321f43306c6d8e244424"
SCRIPT_SHA256 = "162f1067a1c0c1f72509b69cde2dc9381f26ccb425f56830e1c8792041fa1f25"
MANUAL_SHA256 = "94d1bce9eaca3dd1b8df72d66050edba3310afdffd86a2a8927ceffb86b9820a"
SUPPLEMENT_SHA256 = "64dbb47a7ce3eb7c0eb1443b4f0b9961aa40bb702c7cbb89889c514990877317"
AMENDMENTS_SHA256 = "7e5b90120972347269668f4f0aa70c1888e626ce00a329e76c25724565fd82b5"
COMPONENT_PAGE_SHA256 = "e11140e99bfface48af380fadfbbbf1de48c08661a4f8c375962493b2d533cdb"
EXTRACTION_MANIFEST_SHA256 = "3e31614714de9b6d84f5817b5188c73ae1536f4165015f98329f12eda0c91730"
EXTRACTION_FILE_COUNT = 3636
EXTRACTION_TOTAL_BYTES = 741886310
TABLE_NAME = "SlugFest (Williams 1991) v1.2.vpx"
MANUAL_NAME = "Williams_1991_SlugFest_First_Model_Operations_Manual_April_1991_with_paginated_schematics.pdf"
SUPPLEMENT_NAME = "Williams_1991_SlugFest_First_Model_Parts_Catalog_Supplement_16_9190_B_selected_pages.pdf"
AMENDMENTS_NAME = "Williams_1991_SlugFest_Manual_Amendments_1_through_4_undated.pdf"
SWITCH = "pinmame.input.switch"
DIP = "pinmame.input.dip"
SOLENOID = "pinmame.output.solenoid"
LAMP = "pinmame.output.lamp"
GI = "pinmame.output.gi"
CATALOG = "pinmame.catalog.97aa922bf8e4"
CORE = "pinmame.core.97aa922bf8e4"
MANUAL = "manual.williams.slugfest.1991"
SUPPLEMENT = "manual.williams.slugfest.parts-supplement"
AMENDMENTS = "bulletin.williams.slugfest.amendments"
COMPONENTS = "manual.williams.red-parts.microswitches"
IDENTITY = "identity.williams.slugfest.first-model"
VPX_SCRIPT = "vpx-script.slugfest-v1-2"
VPX_TABLE = "vpx-table.slugfest-v1-2"
EXTRACTION = "vpx-extraction.slugfest-v1-2"
RUNTIME = "runtime.slugfest.sf-l1.switch-edges"
RUNTIME_PATH = ROOT / "evidence/runtime/wpc-alpha/slugfest-switch-edges.json"
ACQUIRED_AT = "2026-10-21T20:56:49Z"
DRAWING_CROPS = {
    "pitcher-topology": (79, "0.31,0.08,0.94,0.9", "embedded image xref 549, 1275px across 8.50in", 150, "grayscale, rotated 270 degrees counter-clockwise, 1353x804 WebP quality 75"),
    "ramp-cam": (80, "0.09,0.11,0.91,0.45", "embedded image xref 556, 1275px across 8.50in", 150, "grayscale, 1047x562 WebP quality 80"),
    "bat-linkage": (81, "0.19,0.13,0.91,0.54", "embedded image xref 566, 1960px across 6.53in", 300, "grayscale, 1837x1353 WebP quality 80"),
    "pitch-speed-routing": (106, "0.38,0.06,0.91,0.92", "embedded image xref 753, 1275px across 8.50in", 150, "grayscale, rotated 270 degrees counter-clockwise, 1419x677 WebP quality 80"),
    "game-enable-relay": (118, "0.55,0.53,0.95,0.69", "embedded image xref 802, 8800px across 22.00in", 400, "grayscale, 3520x1091 WebP quality 80"),
}
MATRIX = tuple(column * 10 + row for column in range(1, 9) for row in range(1, 9))
MASKED_SWITCHES = frozenset((54, 55, 61, 62, 63))

# The center/right-of-center transposition in the locations list is settled by
# its own drawing, the matrix and the actual seven script handlers.
SWITCHES = {
    21: ("Slam Tilt", "27-1066", "tilt"),
    22: ("Coin Door Closed", "A-8630", "leaf"),
    23: ("Dispenser Prize", "A-14316", "opto"),
    24: ("Always Closed", "A-8630", "other"),
    25: ("Steal Base / Run", "20-9663-C-2", "button"),
    26: ("Bat Button", "20-9663-B-1", "button"),
    27: ("Dispenser Low", "5647-12693-01", "microswitch"),
    28: ("Dispenser Unjammed Button", "5641-09312-00", "button"),
    31: ("Pinch Hit", "20-9663-C-1", "button"),
    32: ("Fast Ball Pitch", "20-9663-A-6", "button"),
    33: ("Changeup Pitch", "20-9663-A-4", "button"),
    34: ("Curve Pitch", "20-9663-A-5", "button"),
    35: ("Screw Ball Pitch", "20-9663-A-3", "button"),
    36: ("Throw Out Runner / Boo", "20-9663-C-3", "button"),
    37: ("Start Player 1", "20-9663-A-1", "button"),
    38: ("Start Player 2", "20-9663-A-2", "button"),
    41: ("Left Target Panel", "A-14697", "leaf"),
    42: ("Target Panel 2 Left", "A-14697", "leaf"),
    43: ("Target Panel 3 Left", "A-14697", "leaf"),
    44: ("Center Target Panel", "A-14697", "leaf"),
    45: ("Target Panel 3 Right", "A-14697", "leaf"),
    46: ("Target Panel 2 Right", "A-14697", "leaf"),
    47: ("Right Target Panel", "A-14697", "leaf"),
    51: ("Back Row Trough", "5647-12133-08", "microswitch"),
    52: ("Strike Trough", "5647-12133-08", "microswitch"),
    54: ("Pitch Home", "14-7959", "opto"),
    55: ("Ramp Timing Opto", "A-14693", "opto"),
    56: ("Playfield Tilt 1", "SW-1A-117", "tilt"),
    57: ("Playfield Tilt 2", "SW-1A-117", "tilt"),
    61: ("Left Grandstand Return", "A-14447", "opto"),
    62: ("Middle Grandstand Return", "A-14447", "opto"),
    63: ("Right Grandstand Return", "A-14447", "opto"),
}
CABINET_SWITCHES = frozenset((21, 22, 23, 25, 26, 27, 28, *range(31, 39)))
LAMP_NAMES = {
    11: "Left Bleacher Home Run", 21: "Middle Bleacher Home Run", 31: "Right Bleacher Home Run",
    12: "Out Top Left", 13: "Out Top 2 Left", 14: "Out Top 3 Left", 15: "Out Top Center",
    16: "Out Top 3 Right", 17: "Out Top 2 Right", 18: "Out Top Right",
    22: "Single Middle Left", 23: "Double Middle 2 Left", 24: "Single Middle 3 Left", 25: "Sacrifice Middle Center",
    26: "Single Middle 2 Right", 27: "Double Middle 1 Right", 28: "Single Middle Right",
    32: "Double Bottom Left", 33: "Single Bottom 2 Left", 34: "Triple Bottom 3 Left", 35: "Home Run Bottom Center",
    36: "Triple Bottom 2 Right", 37: "Single Bottom 1 Right", 38: "Double Bottom Right",
    81: "Pinch Hit", 82: "Bat Ready", 83: "Steal Base", 84: "Throw Out Runner", 85: "Player 1 Start", 86: "Player 2 Start",
}
for _column, _first in ((4, 32), (5, 24), (6, 16), (7, 8)):
    for _row in range(1, 9):
        # The four bases are runner #25 (48), #17 (58), #1 (68), #9 (78).
        LAMP_NAMES[_column * 10 + _row] = f"Runner #{_first - _row + 1}"
LAMP_NAMES[68] = "Runner #1 (Home)"
LAMP_NAMES[78] = "Runner #9 (First Base)"
LAMP_NAMES[48] = "Runner #25 (Third Base)"
LAMP_NAMES[58] = "Runner #17 (Second Base)"

# function, physical kind, drive wire, power wire, connector, transistor, part.
SOLENOIDS = {
    1: ("Baseball Bat", "coil", "VIO-BRN", "VIO-YEL", "J130-1", "Q82", "A-14499"),
    2: ("Pitch Magnet", "magnet", "VIO-RED", "VIO-YEL", "J130-2", "Q80", "B-20-9608"),
    7: ("Knocker", "coil", "VIO-BLK", "VIO-YEL", "J130-8", "Q68", "AE-23-800"),
    17: ("Left Bleacher Home Run Flasher", "flasher", "BLK-BRN", "RED-WHT", "J125-1", "Q42", "806"),
    18: ("Center Bleacher Home Run Flasher", "flasher", "BLK-RED", "RED-WHT", "J126-2", "Q40", "806"),
    19: ("Right Bleacher Home Run Flasher", "flasher", "BLK-ORN", "RED-WHT", "J126-3", "Q38", "806"),
    20: ("Left Ramp Flasher", "flasher", "BLK-YEL", "RED-WHT", "J126-4", "Q36", "912"),
    21: ("Center Ramp Motor", "motor", "BLU-GRN", "VIO-ORN", "J126-6", "Q28", "14-7960"),
    22: ("Pitch Motor Fast Drive", "motor", "BLU-BLK", "VIO-ORN", "J126-7", "Q30", "14-7959"),
    23: ("Pitch Motor Medium Drive", "motor", "BLU-VIO", "VIO-ORN", "J126-8", "Q34", "14-7959"),
    24: ("Pitch Motor Slow Drive", "motor", "BLU-GRY", "VIO-ORN", "J126-9", "Q32", "14-7959"),
    25: ("Center Ramp Flasher", "flasher", "BLU-BRN", "RED-WHT", "J122-1", "Q26", "912"),
    26: ("Right Ramp Flasher", "flasher", "BLU-RED", "RED-WHT", "J122-2", "Q24", "912"),
    27: ("Card Dispenser Motor", "motor", "BLU-ORN", "VIO-ORN", "J122-3", "Q22", "14-7962"),
    28: ("Dispenser Low Lamp", "lamp", "BLU-YEL", "VIO-ORN", "J122-4", "Q20", "20-9679"),
}
UNUSED_SOLENOID_WIRING = {
    3: ("VIO-ORN", "J130-4", "Q78"), 4: ("VIO-YEL", "J130-5", "Q76"),
    5: ("VIO-GRN", "J130-6", "Q64"), 6: ("VIO-BLU", "J130-7", "Q66"),
    8: ("VIO-GRY", "J130-9", "Q70"), 9: ("BRN-BLK", "J127-1", "Q58"),
    10: ("BRN-RED", "J127-3", "Q56"), 11: ("BRN-ORN", "J127-4", "Q54"),
    12: ("BRN-YEL", "J127-5", "Q52"), 13: ("BRN-GRN", "J127-6", "Q50"),
    14: ("BRN-BLU", "J127-7", "Q48"), 15: ("BRN-VIO", "J127-8", "Q46"),
    16: ("BRN-GRY", "J127-9", "Q44"),
}
GI_DATA = (
    ("Infield Top", "WHT-BRN", "BRN", "J121-7", "Q18"),
    ("Backbox", "WHT-ORN", "ORN", "J120-8", "Q10"),
    ("Pitch Lamps", "WHT-YEL", "YEL", "J120-9", "Q14"),
    ("Outfield", "WHT-GRN", "GRN", "J121-11", "Q16"),
    ("Infield Bottom", "WHT-VIO", "VIO", "J120-11", "Q12"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def provenance(*sources: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(sources)}


def na(reason: str, *sources: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*sources)}


def device_id(group: str, address: int) -> str:
    return f"{group.rsplit('.', 1)[-1]}.{address}"


def aliases(address: int) -> list[dict]:
    return [{"namespace": "pinmame.numeric", "value": str(address)},
            {"namespace": "manual.address", "value": str(address)}]


def seed() -> dict:
    value = load_json(SPATIAL_SEED_PATH)
    if (value["table_sha256"], value["script_sha256"], value["manifest_sha256"]) != (
        TABLE_SHA256, SCRIPT_SHA256, EXTRACTION_MANIFEST_SHA256
    ):
        raise ValueError("spatial seed does not identify the pinned table extraction")
    if value["bounds"] != {"left": 0, "top": 0, "right": 1100, "bottom": 2000}:
        raise ValueError("spatial bounds drift")
    expected = {(LAMP, n) for n in LAMP_NAMES if n < 80 and n not in (11, 21, 31)}
    expected |= {(SWITCH, n) for n in range(41, 48)} | {(SOLENOID, n) for n in (20, 25, 26)}
    actual = {(row["group"], row["address"]) for row in value["placements"]}
    if actual != expected or len(actual) != len(value["placements"]):
        raise ValueError("spatial seed has missing, duplicate or unexpected device bindings")
    for row in value["placements"]:
        if (row["x"], row["y"]) != (round(row["raw_x"] / 1100, 6), round(row["raw_y"] / 2000, 6)):
            raise ValueError("spatial normalization drift")
        if not 0 <= row["x"] <= 1 or not 0 <= row["y"] <= 1:
            raise ValueError("spatial seed contains an out-of-range placement")
    return value


def located(row: dict) -> dict:
    status = "candidate" if row["group"] == SOLENOID else "observed"
    return {"status": status, "placements": [{
        "id": f"placement.{row['object'].lower()}",
        "role": "sensor" if row["group"] == SWITCH else "emitter",
        "space": "playfield", "x": row["x"], "y": row["y"],
        "provenance": provenance(VPX_TABLE, VPX_SCRIPT, MANUAL, status=status),
    }]}


def excerpt(name: str, locator: str, *, image: str | None = None, derivation: str | None = None) -> dict:
    path = EXCERPT_ROOT / name
    value = {"id": f"excerpt.slugfest.{path.stem}", "locator": locator,
             "path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path),
             "method": "mixed", "transcribed_by": "Curator; rendered source visually checked", "reviewed": True}
    if image:
        image_path = EXCERPT_ROOT / image
        value.update(image=image_path.relative_to(ROOT).as_posix(), image_sha256=sha256(image_path), image_derivation=derivation)
    return value


def sources() -> list[dict]:
    copyright_notice = "Copyright Williams Electronics Games, Inc.; NOASSERTION (research copy; original PDF not redistributed)"
    manual_common = {"kind": "manual", "license": copyright_notice, "attribution": "Williams Electronics Games, Inc.; original scan hosted by IPDB"}
    common_excerpt = excerpt("runtime-and-source.md", "bowlgames.c:477-502; wpc.c; core.c; retained script exact line ranges in transcription")
    result = [
        {"id": CATALOG, "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame", "revision": PINMAME_REVISION,
         "locator": "PinmameGetGames: sf_l1 and sf_d1; src/wpc/driver.c", "license": "BSD-3-Clause", "attribution": "PinMAME contributors"},
        {"id": CORE, "kind": "pinmame_core", "uri": f"https://github.com/vpinball/pinmame/blob/{PINMAME_REVISION}/src/wpc/bowlgames.c",
         "revision": PINMAME_REVISION, "sha256": "ca2339f2806c95061b22a5be44314ded4874f78f54e9e129064c0f851d17ef9f",
         "locator": "bowlgames.c:477-502 sfGameData, ROMs and driver declarations; wpc.c:97-99,506-530,642-660; core.c:1778-1855,2249-2350",
         "license": "BSD-3-Clause", "attribution": "PinMAME contributors", "excerpts": [common_excerpt]},
        {**manual_common, "id": MANUAL, "uri": f"https://www.ipdb.org/files/3281/{MANUAL_NAME}", "sha256": MANUAL_SHA256,
         "original_filename": MANUAL_NAME, "source_id": "ipdb:3281", "acquired_at": "2026-10-21T20:56:16.025333Z", "revision": "April 1991 / manual 16-60001-101", "locator": "Verified machine page https://www.ipdb.org/machine.cgi?id=3281; exact PDF and printed page locators in excerpts",
         "excerpts": [excerpt("manual-io.md", "PDF 96-101 / printed 2-36-2-41, complete matrix/location/driver regions"),
                      excerpt("power-driver-assembly.md", "PDF 12 / printed 1-2 board fitment; PDF 72 / printed 2-12 complete A-12697-1 parts table"),
                      excerpt("manual-mechanisms.md", "PDF 7,14-16,19-20,47-48,56-58,79-90; printed A,1-4-1-10,1-37-1-38,1-46-1-48,2-19-2-30")]},
        {**manual_common, "id": SUPPLEMENT, "uri": f"https://www.ipdb.org/files/3281/{SUPPLEMENT_NAME}", "sha256": SUPPLEMENT_SHA256,
         "original_filename": SUPPLEMENT_NAME, "source_id": "ipdb:3281", "acquired_at": "2026-10-21T20:56:15.779878Z", "revision": "16-9190-B selected pages", "locator": "https://www.ipdb.org/machine.cgi?id=3281; PDF 7,11-15 / printed 11-1,11-17,11-22-11-23b",
         "excerpts": [excerpt("identity-and-amendments.md", "Supplement PDF 7,11-15; physical models and dispenser changes")]},
        {**manual_common, "id": AMENDMENTS, "kind": "service_bulletin", "uri": f"https://www.ipdb.org/files/3281/{AMENDMENTS_NAME}", "sha256": AMENDMENTS_SHA256,
         "original_filename": AMENDMENTS_NAME, "source_id": "ipdb:3281", "acquired_at": "2026-10-21T20:56:15.438897Z", "revision": "16-60001-AMD through AMD-4, undated", "locator": "https://www.ipdb.org/machine.cgi?id=3281; PDF 1,3-5,7",
         "excerpts": [excerpt("identity-and-amendments.md", "Amendments 1-4, all nonblank pages")]},
        {"id": COMPONENTS, "kind": "manual", "uri": "https://www.planetarypinball.com/reference/partsmanuals/WMS_Parts_Red_16-9190-B/files/assets/mobile/page0564_i2.jpg",
         "sha256": COMPONENT_PAGE_SHA256, "original_filename": "page0564_i2.jpg", "revision": "Williams Red Parts Catalog 16-9190-B",
         "acquired_at": "2026-10-21T21:36:46.275851Z", "locator": "Printed 6-12 / digital page 564; publisher's original page image. Component construction only; SlugFest fitment from its own operations manual PDF 99.",
         "license": "Copyright Williams Electronics Games, Inc.; NOASSERTION (research copy; original page image not redistributed)",
         "attribution": "Williams Electronics Games, Inc.; digital catalog hosted by Planetary Pinball",
         "excerpts": [excerpt("component-microswitches.md", "Printed 6-12, complete two Micro Switches and Associated Assemblies tables")]},
        {"id": IDENTITY, "kind": "human_review", "uri": "https://www.ipdb.org/machine.cgi?id=3281", "revision": "2026-10-21",
         "sha256": "8a1ea904996d3a93a6a9752d7d2780316bfb6cbb2dbc9732d73d7dc68efc3004", "source_id": "ipdb:3281",
         "locator": "Verified first-model page; SHA256 identifies retained DOM snapshot ipdb-3281-page.json; related snapshots 5949=59d6444e631fa66aa6c2efe62fca8229a835b108eed348f4a4a76fdb5605a3b5 and 6023=771c28d47d1a80a122d44ff9d00a1a9d722da707885c4472be345d04eba9c1cc; browser-page-manifest.json records exact URLs/times under review-artifacts/williams.slugfest-l-1.1991",
         "license": "NOASSERTION; IPDB content and photographers retain rights", "attribution": "Internet Pinball Database; Christopher Wolf upper-playfield photo; factory manual cross-check",
         "acquired_at": "2026-10-21T20:56:31.984771Z", "excerpts": [excerpt("identity-and-amendments.md", "IPDB 3281 physical identity; cross-check against original manual and supplement")]},
        {"id": VPX_SCRIPT, "kind": "vpx_script", "uri": f"external://vpx-sources/williams/{SLUG}/extracted-vpxtool/script.vbs", "sha256": SCRIPT_SHA256,
         "revision": "SlugFest 1.2 / October 18 2026", "locator": "Embedded script extracted from exact retained VPX; line ranges in excerpt; cGameName sf_l1", "known_working": True,
         "license": "NOASSERTION; community table retained locally, not redistributed", "attribution": "DancingCan; Roccodimarco, Tab, Destruk; VPW, nFozzy, Rothbauerw, iaakki, wrd1972, apophis, Fleep (embedded credits)",
         "acquired_at": ACQUIRED_AT, "excerpts": [common_excerpt]},
        {"id": VPX_TABLE, "kind": "vpx_table", "uri": f"external://vpx-sources/williams/{SLUG}/{TABLE_NAME}", "sha256": TABLE_SHA256,
         "revision": "SlugFest 1.2", "locator": "vpxtool git:v0.33.3; bounds 0,0,1100,2000; exact per-object center values pinned in spatial seed",
         "license": "NOASSERTION; community table retained locally, not redistributed", "attribution": "DancingCan and embedded table credits", "acquired_at": ACQUIRED_AT,
         "excerpts": [common_excerpt]},
        {"id": EXTRACTION, "kind": "vpx_table", "uri": f"external://vpx-sources/williams/{SLUG}/extracted-vpxtool/manifest.json", "sha256": EXTRACTION_MANIFEST_SHA256,
         "revision": "vpxtool git:v0.33.3", "locator": "3636 files /741886310 bytes; tools/build_external_evidence_manifest.py: sorted case-sensitive POSIX path,size,SHA256; compact ensure_ascii=False sort_keys JSON plus LF; excludes manifest.json and manifest.sha256 only",
         "license": "NOASSERTION; extracted source artifacts retained locally", "attribution": "Original table contributors; vpxtool extractor; canonical manifest helper", "acquired_at": ACQUIRED_AT},
    ]
    result.append({"id": RUNTIME, "kind": "service_diagnostic", "uri": RUNTIME_PATH.relative_to(ROOT).as_posix(),
                   "sha256": sha256(RUNTIME_PATH), "revision": PINMAME_REVISION,
                   "locator": "Fresh sf_l1 T.1 Switch Edges; exact original ROM/DLL, raw JSON, scenario and interpreted frame hashes in compact evidence; retained review-artifacts/williams.slugfest-l-1.1991/harness/switch-edges-2.json",
                   "license": "BSD-3-Clause (harness/emulator); ROM bytes and full trace not redistributed", "attribution": "Williams diagnostic firmware; PinMAME contributors; curator visual frame review",
                   "excerpts": [excerpt("native-switch-edges.md", "Actual T.1 top-line active names; public 0/1/release; generic 112/114 synthetic outputs")]})
    manual_record = next(source for source in result if source["id"] == MANUAL)
    for name, (page, crop, basis, dpi, details) in DRAWING_CROPS.items():
        derivation = f"{MANUAL_NAME} page {page}, crop box {crop}, scanned page rendered at its native resolution ({basis}), rendered at {dpi} dpi, {details}"
        manual_record["excerpts"].append(excerpt(f"{name}.md", f"PDF{page}, drawing crop; exact region in image_derivation", image=f"{name}.webp", derivation=derivation))
    return result


def build_machine() -> dict:
    placements = {(row["group"], row["address"]): row for row in seed()["placements"]}
    inputs, outputs = [], []
    coin_names = ("Left Coin Chute", "Center Coin Chute", "Right Coin Chute", "Fourth Coin Chute", "Service Credit / Escape", "Volume Down / Down", "Volume Up / Up", "Begin Test / Enter")
    for address, label in enumerate(coin_names, 1):
        inputs.append({"id": device_id(SWITCH, address), "label": label, "kind": "switch", "binding": {"group": SWITCH, "device": address},
                       "aliases": aliases(address) + [{"namespace": "manual.dedicated", "value": f"D{address}"}], "availability": "used", "normally_closed": False,
                       "physical": {"location": "Coin door", "switch_type": "button" if address > 4 else "leaf", "quantity": 1},
                       "spatial": na("cabinet_or_service", MANUAL, CORE), "provenance": provenance(MANUAL, CORE, VPX_SCRIPT)})
    for address in MATRIX:
        found = SWITCHES.get(address)
        value = {"id": device_id(SWITCH, address), "label": found[0] if found else f"Unused Matrix {address}", "kind": "constant" if address == 24 else "switch",
                 "binding": {"group": SWITCH, "device": address}, "aliases": aliases(address), "availability": "used" if found else "unused",
                 "provenance": provenance(MANUAL, CORE, *( [VPX_SCRIPT] if found else [] ))}
        column, row = divmod(address, 10)
        value["wiring"] = {"board": "WPC CPU", "drive_wire": ("GRN-BRN", "GRN-RED", "GRN-ORN", "GRN-YEL", "GRN-BLK", "GRN-BLU", "GRN-VIO", "GRN-GRY")[column-1],
                           "return_wire": ("WHT-BRN", "WHT-RED", "WHT-ORN", "WHT-YEL", "WHT-GRN", "WHT-BLU", "WHT-VIO", "WHT-GRY")[row-1],
                           "return_connection": f"J208-{row}"}
        if not found:
            value["physical"] = {"notes": "Explicit Not Used cell in this game's full switch matrix. No fitted contact or invented placement."}
            value["spatial"] = na("unused", MANUAL)
        else:
            notes = "Public state is consumed as published. The WPC CPU reads the matrix directly; masked active-high optos are inverted by PinMAME."
            value["physical"] = {"part_number": found[1], "switch_type": found[2], "quantity": 1,
                                 "location": "Cabinet/control panel/dispenser" if address in CABINET_SWITCHES else "Playfield", "notes": notes}
            if address == 24:
                value.update(constant_active=True, initial_active=True)
                value["physical"]["notes"] = "Factory always-closed reference, not a ball sensor; wpc.c also initializes its raw matrix bit. Retained script explicitly holds 24 active."
                value["spatial"] = na("constant", MANUAL, CORE, VPX_SCRIPT)
            else:
                value["normally_closed"] = address in MASKED_SWITCHES
                if address in CABINET_SWITCHES:
                    value["spatial"] = na("cabinet_or_service", MANUAL, VPX_SCRIPT)
                elif (SWITCH, address) in placements:
                    value["spatial"] = located(placements[(SWITCH, address)])
                    value["physical"]["notes"] += " Observed projection onto the script-bound card-face contact, not a measured rear switch-wire position."
                if address == 22:
                    value["initial_active"] = True
                if address == 28:
                    value["physical"]["notes"] += " Factory 1-9/1-10 identifies an operator pushbutton: press after clearing jam/empty to resume accumulated awards. The retained script incorrectly holds it at 1 as healthy feed feedback; that table simplification is not the hardware rest state and is not a canonical startup requirement."
                if address in (44, 45):
                    value["physical"]["notes"] += " PDF 99 locations list reverses center/3R labels on 44/45; its drawing, matrix and seven left-to-right script bindings agree on this identity."
                if address == 54:
                    value["physical"].pop("part_number")
                    value["physical"]["notes"] += " Location table part 14-7959 is the motor; PDF 79 shows its separate cam/opto bracket. Normally-closed matrix construction follows mask 54 and the script's blocked/cycle feedback, not the beam's visual rest state."
                if address in (51, 52):
                    value["physical"]["notes"] += " Game-specific fitment is from PDF 99. Williams parts catalog 16-9190-B printed 6-12 identifies exact part 5647-12133-08 under Micro Switches and Associated Assemblies; the shared catalog establishes construction only."
                    value["provenance"]["source_refs"].append(COMPONENTS)
                if address in (23, 27, 28):
                    value["physical"]["notes"] += " Original A-14471 dispenser only; ticket or revised dispenser feedback is not silently substituted."
        inputs.append(value)
    for address in range(111, 119):
        inputs.append({"id": device_id(SWITCH, address), "label": f"Generic Emulator Flipper Column {address}", "kind": "virtual", "binding": {"group": SWITCH, "device": address},
                       "aliases": [{"namespace": "pinmame.numeric", "value": str(address)}], "availability": "used" if address in (112,114) else "unknown", "spatial": na("virtual", CORE),
                       "physical": {"notes": "No physical flippers or EOS are declared by sfGameData. 112/114 are generic host buttons; the retained script also writes 112 alongside real Bat 26. Other column bits are not synthesized, but wpc_r can read the column. No untried absence claim or invented hardware is made."},
                       "provenance": provenance(CORE, VPX_SCRIPT, RUNTIME, status="validated" if address in (112,114) else "observed")})
    for address in range(1, 9):
        inputs.append({"id": f"dip.{address}", "label": f"CPU Option / Country Bit {address}", "kind": "dip_switch", "binding": {"group": DIP, "device": address}, "aliases": [],
                       "availability": "used", "spatial": na("dip_switch", CORE), "provenance": provenance(CORE)})
    for address in range(1, 51):
        data = SOLENOIDS.get(address)
        value = {"id": device_id(SOLENOID, address), "label": data[0] if data else f"Unused Solenoid {address}", "kind": data[1] if data else "virtual",
                 "binding": {"group": SOLENOID, "device": address}, "aliases": aliases(address) if address <= 28 else [],
                 "availability": "used" if data else "unused", "provenance": provenance(CORE, *( [MANUAL, VPX_SCRIPT] if address <= 28 else [] ))}
        if data:
            value["physical"] = {"part_number": data[6], "location": "Cabinet/rear upright Bleachers Assembly" if address in (7,17,18,19,27,28) else "Playfield", "quantity": 1}
            value["wiring"] = {"board": "WPC Power Driver", "drive_wire": data[2], "power_wire": data[3], "drive_connection": data[4], "driver_transistor": data[5]}
            if address in (7,17,18,19,27,28):
                value["spatial"] = na("cabinet_or_service", MANUAL, VPX_SCRIPT)
            elif (SOLENOID, address) in placements:
                value["physical"]["notes"] = "Script-bound Light center is a candidate only: physical #912 socket center has not been reconciled against the factory ramp drawing. No VPX Flasher sprite or lightmap receiver is used."
            if address in (22,23,24):
                value["physical"].pop("quantity")
                value["physical"]["notes"] = "One shared 14-7959 pitch motor, three speed-select drive branches. PDF 106/3-4 A-14381 regulator joins Fast 22/Medium 23/Slow 24 through its separate resistor paths to that motor. Do not create three physical motors or add their quantities."
            if address == 1:
                value["physical"]["notes"] = "Factory bat coil A-14499, A-14464 linkage; assembly list says bat coil assembly A-14789. Retained table's direct bat fallback animates from the player button and only observes output 1, so its motion/timing is not proof of coil-driven factory behavior."
            if address == 17:
                value["physical"]["notes"] = "Table prints J125-1 while adjacent bleacher flasher rows print J126; preserved as a wiring-detail reading. Rear upright assembly is cabinet/rear-panel, not a playfield proxy coordinate."
            if address == 28:
                value["physical"]["notes"] = "Physical low-card lamp 20-9679 is carried by solenoid callback 28; it is a lamp, not a motor or flasher."
        elif address <= 28:
            wire, connector, transistor = UNUSED_SOLENOID_WIRING[address]
            value["kind"] = "coil"
            value["wiring"] = {"board": "WPC Power Driver", "drive_wire": wire, "drive_connection": connector, "driver_transistor": transistor}
            value["physical"] = {"notes": "Factory solenoid table explicitly Not Used / NU; power cell blank, no fitted load. Any service sweep state does not establish a physical coil."}
            value["spatial"] = na("unused", MANUAL, CORE)
        else:
            value["spatial"] = na("virtual" if address in (29,30,31,45,46,47,48) else "unused", CORE)
            if address in (29,30):
                value.update(label=f"J111 GPIO State {address-29+5}", availability="used", roles=["internal.wpc-state"])
                value["physical"] = {"notes": f"Virtual public mirror of WPC_GILAMPS bit {address-29+5}, unconditionally exported by wpc.c. This defines register-state meaning independently of whether this ROM toggles it. Any attached J111 load and game-specific physical function remain unproven; no physical load or quantity is claimed."}
            elif address == 31:
                value.update(label="Power Driver Game Enable Relay", kind="relay", availability="used", roles=["internal.wpc-state"])
                value["physical"] = {"part_number": "5580-08994-01", "quantity": 1, "location": "Rear cabinet WPC Power Driver Assembly A-12697-1",
                                     "notes": "Factory PDF 12 fits A-12697-1; PDF 72 item 51 lists RLY1, part 5580-08994-01, as Relay 4PDT 6VDC5A VS. PDF 118 draws T7 through R208/Q99 to a RELAY DPDT symbol and R/L FLIP RETURN contacts. Preserve the BOM 4PDT versus drawn DPDT readings without inferring additional contacts or fitted flipper loads. wpc.c maps WPC_GILAMPS bit 7 to public 31; native service navigation observes that state. No physical flippers or game-on output 19 are claimed."}
                value["spatial"] = na("cabinet_or_service", MANUAL, CORE)
                value["wiring"] = {"board": "WPC Power Driver A-12697-1", "driver_transistor": "Q99"}
                value["provenance"] = provenance(MANUAL, CORE)
            elif address == 32:
                value.update(label="Constant Zero WPC State", roles=["internal.unused.wpc-output"])
                value["physical"] = {"notes": "Constant zero public WPC state channel: core_getSol remaps only the three WPC_GILAMPS state bits to 29-31. No fourth state bit or fitted physical load exists at public 32."}
                value["spatial"] = na("virtual", CORE)
            elif address in (45,46,47,48):
                value.update(label=f"Synthetic {'Right' if address < 47 else 'Left'} Flipper {'Power' if address % 2 else 'Hold'} State", availability="used")
                value["physical"] = {"notes": "core_updateSw fabricates this pair from generic 112/114 while game enable is high. sfGameData declares no physical flippers. Both pair members describe virtual runtime state, never actual bat windings."}
        outputs.append(value)
    for address in MATRIX:
        used = address in LAMP_NAMES
        value = {"id": device_id(LAMP, address), "label": LAMP_NAMES.get(address, f"Unfitted Lamp Matrix {address}"), "kind": "lamp",
                 "binding": {"group": LAMP, "device": address}, "aliases": aliases(address), "availability": "used" if used else "unused", "provenance": provenance(MANUAL, CORE, *( [VPX_SCRIPT] if used else [] ))}
        col, row = divmod(address,10)
        value["wiring"] = {"board": "WPC Power Driver", "drive_wire": ("YEL-BRN","YEL-RED","YEL-ORN","YEL-BLK","YEL-GRN","YEL-BLU","YEL-VIO","YEL-GRY")[col-1],
                           "drive_connection": f"J137-{col}", "return_wire": ("RED-BRN","RED-BLK","RED-ORN","RED-YEL","RED-GRN","RED-BLU","RED-VIO","RED-GRY")[row-1],
                           "return_connection": f"J133-{(1,2,4,5,6,7,8,9)[row-1]}"}
        if not used:
            value["spatial"] = na("unused", MANUAL)
            value["physical"] = {"notes": "Blank factory matrix cell and no row in the complete lamp locations inventory; no emitter fitted. Blank is preserved separately from an explicit Not Used label in the excerpt."}
        else:
            value["physical"] = {"part_number": "555", "quantity": 1, "location": "Rear upright Bleachers Assembly" if address in (11,21,31) else ("Control panel" if address >= 80 else "Playfield insert")}
            if address in (11,21,31) or address >= 80:
                value["spatial"] = na("cabinet_or_service", MANUAL)
                if address in (11,21,31):
                    value["physical"]["notes"] = "Independent #555 controlled lamp in rear upright Bleachers Assembly, distinct from the #806 flasher on 17/18/19. Omitted from the retained AllLamps collection; do not delete it or place a helper at a fabricated playfield socket."
            else:
                value["physical"]["notes"] = "The report retains its script-bound insert Light center as a candidate reference only. That invisible non-bulb Light covers the insert, not an observed socket. Manual establishes one #555 bulb per insert; no canonical emitter coordinate is asserted before a factory-drawing/physical reconciliation."
        outputs.append(value)
    for address, data in enumerate(GI_DATA):
        label, drive, power, connector, transistor = data
        value = {"id": device_id(GI,address), "label": f"GI {label}", "kind": "gi", "binding": {"group": GI,"device": address},
                 "aliases": [{"namespace": "manual.address", "value": str(address+1)}], "availability": "used", "provenance": provenance(MANUAL, CORE, VPX_SCRIPT),
                 "physical": {"part_number": "555", "location": "Backbox" if address==1 else ("Control panel" if address==2 else "Playfield"),
                              "notes": "Five factory strings use callback indices 0-4. Script cohorts are visual proxies and regional/provisional assignments, not a physical socket inventory. No quantity inferred from helpers."},
                 "wiring": {"board": "WPC Power Driver", "drive_wire": drive,"power_wire":power,"drive_connection":connector,"driver_transistor":transistor}}
        if address in (1,2):
            value["spatial"] = na("cabinet_or_service", MANUAL)
        if address==2:
            value["physical"]["quantity"] = 4
            value["physical"]["notes"] += " PDF 97/2-37 separately lists four #555 pitch-control GI lamps A-D."
        outputs.append(value)
    mechanism_specs = [
        ("bat", "Baseball Bat", "other", [1], [26], "A-14464", "Coil 1/plunger and roller linkage swing the bat; extension spring returns it against the adjustable stop. Button 26 is a cabinet command, not bat EOS. The retained table moves directly from BatPress/BatRelease while observing 1; its fallback does not prove physical coil timing."),
        ("pitcher", "Three-speed Pitcher", "motorized", [22,23,24], [54], "A-14356", "One 14-7959 motor receives three speed branches through A-14381 regulator. It rotates clockwise viewed from left, drives pitch plate through one ball from the six-ball return queue and reports a timing-cam opto 54. Home is arm toward front/beam clear. Slow/medium/fast are branches of one motor, not three mechanisms; ROM errors can follow absent home feedback. Table delays are tuning, not measured cam widths."),
        ("pitch-magnet", "Pitch-path Magnet", "other", [2], [], "A-14696", "One under-playfield B-20-9608 magnet deflects slower pitches; fast pitches are little affected. No dedicated position or ball sensor belongs to the magnet. The retained table substitutes lateral force profiles and uses 2 as an acknowledgement, so its force/timing is not a physical calibration."),
        ("center-ramp", "Center Up/Down Ramp", "motorized", [21], [55], "A-14290", "One counter-clockwise motor (viewed from left) and cam raise/lower the center ramp, with timing opto 55. T.12 normally stops with beam clear and reports MOVING/ERROR. Both up/down endpoint semantics require the cam phase/history; clear alone is not proof of which height. Retained model initializes down and supplies modeled cam occlusion; phase windows and timing remain table tuning."),
        ("target-panels", "Seven Rotating Target Panels", "other", [], list(range(41,48)), "A-14150", "Seven independent A-14452-1..-7 rotating panels actuate their own A-14697 switch wire 41..47 from left to right. Results belong to the lit inserts and ROM. Rear deflector/guide sends the ball into the return trough. No reset solenoid or drop-target latch is fitted; the table's face triggers are contact proxies."),
        ("grandstand-returns", "Three Grandstand / Home Run Returns", "other", [], [61,62,63], "A-14446", "Left/middle/right shaped ramps behind the target row lead through three separate A-14315/A-14316 optical paths 61/62/63 into gravity returns. These report ball passage, not center-ramp position. Preserve the selected route until the ball clears its beam and joins the return; do not pulse all three for one ball."),
        ("six-ball-return", "Six-ball Gravity Return", "other", [], [51,52], "A-14621", "Rear/back-row return 51 and front strike trough 52 join adjustable passive ramps and the lowest trough feeding the single pitcher. Six balls are physical inventory; conserve them rather than create/destroy on every pitch. Height mismatch, guide pressure or a blocked trough can prevent a serve after a command. Sensor locations and exact handoff time remain unmeasured."),
        ("card-dispenser", "Original Card Dispenser", "motorized", [27], [23,27,28], "A-14471", "Motor 27 drives the original cable/pulley, piston and guide-rod feed under the card magazine, with extension-spring return; optical prize 23 confirms passage and low 27 senses stock. Unjammed 28 is an operator acknowledgement button after clearing a fault, not a healthy-state sensor. Low lamp 28 is normally off, on when low and blinks jam/empty; A.6.06 chooses stop or ignore dispenser errors. One-card gap and chute adjustment prevent double feed/hung cards. The table substitutes held 28=1, pulses 23 on confirmed advancement and models stock; its 15-card capacity and ms windows are tuning, not the factory 1030-card magazine. Revised A-14471-1 and ticket conversion are separate options, not simultaneously fitted hardware."),
        ("knocker", "Cabinet Knocker", "kicker", [7], [], "B-10686-1", "Cabinet AE-23-800 coil 7 strikes its mechanical stop and returns; no playfield ball path or sensor belongs to it."),
    ]
    mechanisms=[]
    for ident,label,kind,actuators,sensors,assembly,behavior in mechanism_specs:
        mechanisms.append({"id":f"mechanism.{ident}","label":label,"kind":kind,"actuators":[device_id(SOLENOID,n) for n in actuators],
                           "sensors":[device_id(SWITCH,n) for n in sensors],"assembly_part_number":assembly,"behavior":behavior,
                           "provenance":provenance(MANUAL,VPX_SCRIPT, status="observed" if ident in ("bat","center-ramp","pitcher","card-dispenser") else "validated")})
    for device in inputs + outputs:
        group,address = device["binding"]["group"],device["binding"]["device"]
        if (group == SWITCH and address in (*MASKED_SWITCHES,23,41)) or (group == SOLENOID and address in (31,45,46,47,48)):
            device["provenance"]["source_refs"].append(RUNTIME)
    return {"format":"pinmame-machine-definition","schema_version":2,
            "machine":{"id":MACHINE_ID,"name":"SlugFest (First Model)","manufacturer":"Williams","year":1991,"kind":"redemption_game","model_number":"60001","ipdb_id":3281,
                       "playfield":{"width":1100,"height":2000,"units":"vpx","provenance":provenance(VPX_TABLE,status="observed")}},
            "controller":{"platform":"pinmame.wpc-alpha","hardware_generation":"0x4","inversion_applied_by_emulator":True},
            "drivers":[{"id":"sf_d1","clone_of":"sf_l1","description":"Slugfest (D-1 LED Ghost Fix)","year":"1991","manufacturer":"Williams","flags":0,"physical_compatibility":"identical","variant_notes":"LED Ghost Fix of L-1 on the same sfGameData, wpc_mDMDS and sound-ROM set. No new physical game, lamp or device address is declared."},
                       {"id":"sf_l1","description":"Slugfest (L-1)","year":"1991","manufacturer":"Williams","flags":0,"physical_compatibility":"identical","variant_notes":"Original L-1 firmware for model 60001; retained known-working table binds it and native service run identifies 60001 REV L-1. Later physical models are not silently asserted identical."}],
            "inputs":inputs,"outputs":outputs,"displays":[{"id":"display.dmd","label":"Upright 128x32 Dot Matrix Display","kind":"dmd","width":128,"height":32,"controller_index":0,"physical_location":"cabinet_or_service","spatial":na("cabinet_or_service",MANUAL,CORE),"provenance":provenance(MANUAL,CORE)}],
            "mechanisms":mechanisms,"relationships":[],"sources":sources(),"conflicts":[],
            "knowledge":{"path":KNOWLEDGE_PATH.relative_to(ROOT).as_posix(),"status":"partial"},
            "coverage":{"status":"partial","missing":["input_semantics","output_semantics","mechanism_behavior","variant_differences","spatial_placement"],
                        "dimensions":{"catalog_identity":"validated","address_enumeration":"validated","semantic_naming":"observed","physical_wiring":"observed","mechanisms":"observed","variant_coverage":"observed","recreation_knowledge":"validated","spatial_placement":"observed"}}}


def build_report(machine: dict | None = None) -> dict:
    machine = machine or build_machine()
    devices = machine["inputs"] + machine["outputs"]
    located_devices = [value for value in devices if value.get("spatial",{}).get("placements")]
    return {"format":"pinmame-spatial-blockers","version":1,"machine_id":MACHINE_ID,
            "decision":"partial: no physical socket, hidden-sensor or cam measurement is invented",
            "table_sha256":TABLE_SHA256,"script_sha256":SCRIPT_SHA256,"manual_sha256":MANUAL_SHA256,
            "extraction":{"manifest_sha256":EXTRACTION_MANIFEST_SHA256,"file_count":EXTRACTION_FILE_COUNT,"total_bytes":EXTRACTION_TOTAL_BYTES,
                          "algorithm":"tools/build_external_evidence_manifest.py: case-sensitive POSIX paths sorted; each path,size,SHA256; compact sorted-key UTF-8 JSON plus LF; manifest pair excluded"},
            "transform":{"x":"raw_x /1100","y":"raw_y /2000","rounding_decimal_places":6,"convention":"x left 0/right 1; y rear 0/front 1"},
            "reference_candidates":seed()["placements"],"located_device_count":len(located_devices),
            "research_artifacts":[{"url":"https://www.ipdb.org/images/3281/image-13.jpg","page":"https://www.ipdb.org/showpic.pl?id=3281&picno=27257","sha256":"d2e4b6ac43537a3b15ac759035f22b74138d33f0cf2045a292b388018a5b5b6f","attribution":"John Gray","role":"Inspected cabinet/return-path overview; no measured coordinate derived."},
                                  {"url":"https://www.ipdb.org/images/3281/image-4.jpg","page":"https://www.ipdb.org/showpic.pl?id=3281&picno=9832","sha256":"d200b0a6648ce113a2c2fe5552981ed6a807ff38cfa750b2bbec916b7c98d805","attribution":"Christopher Wolf","role":"Independent primary-session cross-check of upright Bleachers Assembly; no coordinate derived."},
                                  {"path":"review-artifacts/williams.slugfest-l-1.1991/photos/pinside-manifest.json","role":"Primary-session gallery/contact inspection only; uploader unknown, no canonical coordinate or quantity asserted."}],
            "projection_classes":["Seven target contacts projected onto script-bound CardFaceContact trigger centers; actual rear switch-wire positions remain unmeasured."],
            "unresolved":[{"id":v["id"],"label":v["label"],"reason":"Physical playfield device has no defensible exact retained socket/sensor/actuator coordinate."} for v in devices if v.get("availability")=="used" and "spatial" not in v],
            "limitations":["53 insert Light centers are report-only reference candidates. They are invisible non-bulb insert overlays; no canonical emitter placement is asserted without physical socket reconciliation.",
                           "Three ramp-flasher Light centers are report-only candidates; canonical physical #912 socket positions are omitted until reconciled.",
                           "GI strings 0/3/4 have no physical bulb inventory or coordinates. Backbox/control-panel devices use not_applicable; no clamping of out-of-range cabinet Light coordinates.",
                           "No registration anchor, baked-mesh primitive origin, Flasher sprite or lightmap receiver is used as a physical placement.",
                           "Model 60001 original dispenser is the physical baseline; later dispenser/cosmetic models and ticket conversion are documented but not fully recreated."]}


def report_markdown(report: dict) -> str:
    lines=["# SlugFest first-model spatial blockers", "", "Status: **partial**. Coordinates use x left 0/right 1 and y rear 0/front 1.", "",
           f"Exact retained VPX SHA-256: `{TABLE_SHA256}`. Embedded script: `{SCRIPT_SHA256}`.",
           f"Factory operations manual: `{MANUAL_SHA256}`. Extraction manifest: `{EXTRACTION_MANIFEST_SHA256}` ({EXTRACTION_FILE_COUNT} files, {EXTRACTION_TOTAL_BYTES} bytes).", "",
           "The manifest is reproducible with tools/build_external_evidence_manifest.py. It sorts every POSIX relative filename case-sensitively, records byte size and SHA-256, and hashes compact sorted-key UTF-8 JSON with a final LF. Only its own manifest pair is excluded.", "",
           "Normalization is x=raw_x/1100, y=raw_y/2000, rounded to six places. The committed spatial seed names every exact object and raw point. Cabinet/backbox objects outside the rectangle are classified from the factory physical evidence; they are never clamped into the playfield.", ""]
    lines += [f"- {line}" for line in report["limitations"]]
    lines += ["", "| Device | Object | Raw x,y | Normalized x,y | Evidence role |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {row['group']} {row['address']} | {row['object']} | {row['raw_x']},{row['raw_y']} | {row['x']},{row['y']} | {row['classification']} |" for row in report["reference_candidates"]]
    lines += ["", "The seven target contacts are explicit target-face projections, not surveyed switch-wire coordinates. The insert positions follow script bindings (AllLamps plus TimerInterval), not names alone. Flasher candidates use script-driven Light centers; their physical #912 socket positions still require reconciliation.", "", "## Physical devices without placements", ""]
    lines += [f"- {row['id']}: {row['label']}. {row['reason']}" for row in report["unresolved"]]
    return "\n".join(lines)+"\n"


def verify_external_sources() -> None:
    vpx_root=os.environ.get("PINMAME_VPX_SOURCES_ROOT")
    if vpx_root:
        base=Path(vpx_root)/"williams"/SLUG
        extraction=base/"extracted-vpxtool"
        if sha256(base/TABLE_NAME)!=TABLE_SHA256 or sha256(extraction/"script.vbs")!=SCRIPT_SHA256:
            raise ValueError("retained SlugFest VPX/script hash drift")
        if check_manifest(extraction,"sf_l1")!=EXTRACTION_MANIFEST_SHA256:
            raise ValueError("retained extraction manifest identity drift")
        manifest=load_json(extraction/"manifest.json")
        if len(manifest["files"])!=EXTRACTION_FILE_COUNT or sum(f["size"] for f in manifest["files"])!=EXTRACTION_TOTAL_BYTES:
            raise ValueError("retained extraction count/size drift")
        game=load_json(extraction/"gamedata.json")
        if any(game[key]!=value for key,value in seed()["bounds"].items()):
            raise ValueError("retained table bounds drift")
        collection=next(c["items"] for c in load_json(extraction/"collections.json") if c["name"]=="AllLamps")
        for row in seed()["placements"]:
            kind,obj=next(iter(load_json(extraction/row["file"]).items()))
            if kind!=row["type"] or obj["center"]!={"x":row["raw_x"],"y":row["raw_y"]}:
                raise ValueError(f"retained object center drift: {row['object']}")
            if row["group"]==LAMP and (row["object"] not in collection or obj["timer_interval"]!=row["address"]):
                raise ValueError(f"retained lamp binding drift: {row['object']}")
    manuals_root=os.environ.get("PINMAME_MANUALS_ROOT")
    if manuals_root:
        base=Path(manuals_root)/"by-machine"/MACHINE_ID
        for name,digest in ((MANUAL_NAME,MANUAL_SHA256),(SUPPLEMENT_NAME,SUPPLEMENT_SHA256),(AMENDMENTS_NAME,AMENDMENTS_SHA256)):
            if sha256(base/name)!=digest:
                raise ValueError(f"retained factory PDF hash drift: {name}")
    review_root=os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT")
    if review_root:
        base=Path(review_root)/MACHINE_ID
        if sha256(base/"parts-catalog-page0564_i2.jpg")!=COMPONENT_PAGE_SHA256:
            raise ValueError("retained component construction page hash drift")
        if sha256(base/"ipdb-3281-page.json")!="8a1ea904996d3a93a6a9752d7d2780316bfb6cbb2dbc9732d73d7dc68efc3004":
            raise ValueError("retained identity snapshot hash drift")
        evidence=load_json(RUNTIME_PATH)
        run=evidence["runtime"]["raw_runs"][0]
        if sha256(base/"harness"/f"{run['name']}.json")!=run["sha256"]:
            raise ValueError("retained native run hash drift")
        if sha256(ROOT/run["scenario_path"])!=run["scenario_sha256"]:
            raise ValueError("native scenario hash drift")


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check",action="store_true")
    mode.add_argument("--regenerate",action="store_true")
    args=parser.parse_args()
    if AUTHOR_READY_PATH.exists():
        raise ValueError("refusing to overwrite an existing author-ready definition")
    verify_external_sources()
    machine=build_machine(); report=build_report(machine)
    knowledge=KNOWLEDGE_SEED_PATH.read_text(encoding="utf-8")
    expected={MACHINE_PATH:canonical_bytes(machine),REPORT_PATH:canonical_bytes(report),KNOWLEDGE_PATH:knowledge.encode("utf-8"),REPORT_MARKDOWN_PATH:report_markdown(report).encode("utf-8")}
    if args.check:
        for path,payload in expected.items():
            if not path.is_file() or path.read_bytes()!=payload:
                raise ValueError(f"curator drift: {path.relative_to(ROOT)}")
    else:
        write_json(MACHINE_PATH,machine);write_json(REPORT_PATH,report)
        write_text(KNOWLEDGE_PATH,knowledge);write_text(REPORT_MARKDOWN_PATH,report_markdown(report))
    print(f"{MACHINE_ID}: partial; {len(machine['inputs'])} inputs / {len(machine['outputs'])} outputs; {report['located_device_count']} observed/candidate positions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
