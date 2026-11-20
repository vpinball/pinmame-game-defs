"""Reproduce the Mata Hari definition, recreation note and spatial report."""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import quote

from pinmame_game_defs.identifiers import slug
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes
from pinmame_game_defs.spatial import _round_point

import drawing_callouts


ROOT = Path(__file__).resolve().parents[1]
ID = "bally.mata-hari.1977"
SLUG = "mata-hari-1977"
SEEDS = ROOT / "tools/seeds/bally"
EXCERPTS = ROOT / "evidence/excerpts" / ID
DEFINITION = ROOT / f"machines/partial/bally/{SLUG}.json"
KNOWLEDGE = ROOT / f"knowledge/bally/{SLUG}.md"
REPORT = ROOT / f"reports/spatial/bally/{SLUG}"
CALLOUTS = SEEDS / f"{SLUG}-callouts.json"
PIN = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
IPDB = "https://www.ipdb.org/machine.cgi?id=4501"
CORE = "pinmame.core.by17.46e1a01a"
IDENTITY = "identity.mata-hari-1104-e"
MANUAL = "manual.mata-hari.fo579"
SCHEM = "manual.mata-hari.schematics"
LOCATIONS = "manual.mata-hari.factory-locations"
A5 = "manual.mata-hari.lamp-driver"
ROM = "rom.mata-hari.installation"
BULLETIN = "bulletin.mata-hari.mpu-service"
TOP = "photo.mata-hari.playfield"
UNDERSIDE = "photo.mata-hari.underside"
DETAIL = "photo.mata-hari.feature-inserts"
SCRIPT = "vpx-script.mata-hari-1978"
CORPUS = "vpx-script.mata-hari-2-0-0"
CORPUS_REVISION = "0c036bb61b4b4e8c778c37559f6795df8cd1521e"
CORPUS_SCRIPT = "Mata Hari (Bally 1978) v2.0.0.vbs"
CORPUS_SHA256 = "623a6d96c89590e65c509a6e533e9509ffe0939d8ac1f0604aadc83e2647a73b"
GEOMETRY = "vpx-table.mata-hari-1978"
GEOMETRY_1977 = "vpx-table.mata-hari-1977"
PLAY = "runtime.mata-hari.stock-gameplay"
AB_PLAY = "runtime.mata-hari.stock-ab-lamps"
AB_FOLDER = "native-ab-lamps-89e71fae5467"
AB_SHA256 = "10f98b319c8dad465986fae54f86c04f22bca5496e46028c17ddd171bee7a0c1"
AB_MANIFEST = "db88f85f45d30b59c4e12880fe02803209782d3c1ecfe566d74ff05fe9d5e2e5"
SERVICE = "runtime.mata-hari.stock-service"
V22 = "runtime.mata-hari.v22-display-layout"
REVIEW = f"external:pinmame-review-artifacts/{ID}/native-traces"
NATIVE_MANIFEST = "77b1e24392747e450a2cce02ec805cc1985e76024e9731206d3eb22494747f69"
VPX = f"external:pinmame-vpx-sources/bally/{SLUG}"

TABLES = {
    1977: {
        "sha256": "3684e0baac9f994bd141df4811e8e69974a3eb7bf27b7767dc969a84786d9742",
        "script_sha256": "1f01040daceead28be4f14c5981691f83d895353496793f1fc888cd3ba8a4044",
        "manifest_sha256": "95076d9a9231bf354394c3945834795ef76dff8833dafadd7e3ec15b3e41ad28",
        "vpx_size": 66654208,
        "file_count": 1039,
        "file_bytes": 77998348,
    },
    1978: {
        "sha256": "4af73b1882c164bf2a653a4191df67306365e682d0b90c0bb5aadd32cc2f7b87",
        "script_sha256": "e1c9628fdf32c53b99496500aa138067294691c8c0bf743b2af500dd9f5fd357",
        "manifest_sha256": "546a3fd9da7edc8b93023963b5fe800a69ad441ffd68d5e9026670d19c97bee6",
        "vpx_size": 24227840,
        "file_count": 886,
        "file_bytes": 35621248,
    },
}
FACTORY_FILES = {
    MANUAL: ("Bally_1977_Mata_Hari_Manual_Color.pdf", "ec3ec02a5928e061b534bfb031eaed085db5d85c0e6a6a7eebe723cc2d6fe3f0", "08:29:24"),
    SCHEM: ("Bally_1978_Mata_Hari_SS_Schematics.pdf", "05712810268a5bd832e50c33f9d149050d0724c951e48e4a163e7e22b610ddb0", "08:29:23"),
    A5: ("Bally_1978_Mata_Hari_Lamp_Driver_Schematic.jpg", "619389725b157ecc0c9cf0801845c69a3158956bbb811c8b59508ed59ddfd556", "08:29:23"),
}
PHOTOS = {
    TOP: ("ipdb-34391.jpg", "image-45.jpg", 34391, "dad87f0b8c52483f4bdd9d9ae19a2e60bd2f65f0eedf1d8277b9ed268cbf4615", "Overall player-side playfield"),
    UNDERSIDE: ("ipdb-34409.jpg", "image-D46.jpg", 34409, "fdfebb57fc9241c1328a5d12bfe53816a0934d84ef83d3b7bab0d212095eaf10", "Underside, from the apron end"),
}
BULLETIN_FILE = "Bally_Service_Bulletin_Book_1978.pdf"
BULLETIN_SHA256 = "4ddf43046733a60f5329ea84fecc5a4e85ed541567ca4b5a6caee1ae1846dcfc"
RUNTIME = {
    PLAY: ("native-stock-gameplay-20261120.json", "d30115b51d20431f066f9282ff249e319503e29e8490f75a40269c8cfe2112aa", "08:35:07", "Start, serve, both flippers, isolated thumpers and slings, saucer, both full banks and tilt."),
    SERVICE: ("native-stock-service-20261120.json", "b08a6111792a09ab664b44f6aac66608b56b7acd2faecf11e1b53c77b70dd663", "08:35:17", "Lamp/display/coil/switch tests, including two full coil sequences."),
    V22: ("native-v22-7-layout-20261120.json", "4f8ddf494cd4e1af4647e109ce78a2dbfcbf54e8ba221aba5656c3533809b6c1", "08:41:39", "Seven-digit player fields on matahard7 startup. Default DIP state."),
}

SWITCHES = {
    6: "Start / credit button", 7: "Tilt contacts", 8: "Outhole ball switch",
    9: "Right coin chute III", 10: "Left coin chute I", 11: "Centre coin chute II",
    16: "Slam contacts",
    17: "Right drop target D", 18: "Right drop target C", 19: "Right drop target B", 20: "Right drop target A",
    21: "Left drop target D", 22: "Left drop target C", 23: "Left drop target B", 24: "Left drop target A",
    25: "Right flipper feeder lane", 26: "Left flipper feeder lane", 27: "Drop-target rebound contacts",
    28: "Right side B lane", 29: "Left side A lane", 30: "Top right B lane", 31: "Top left A lane",
    32: "Top saucer ball switch", 33: "Right outlane", 34: "Left outlane",
    35: "Right slingshot", 36: "Left slingshot", 37: "Bottom right thumper bumper",
    38: "Bottom left thumper bumper", 39: "Top right thumper bumper", 40: "Top left thumper bumper",
}
INPUT_OBJECTS = {
    8: ("Kicker.Drain",),
    17: ("HitTarget.Target9",), 18: ("HitTarget.Target8",),
    19: ("HitTarget.Target7",), 20: ("HitTarget.Target6",),
    21: ("HitTarget.Target1",), 22: ("HitTarget.Target2",),
    23: ("HitTarget.Target3",), 24: ("HitTarget.Target4",),
    27: ("Wall.ULeftSlingShot", "Wall.URightSlingshot"),
    32: ("Kicker.Kicker1",), 35: ("Wall.RightSlingShot",), 36: ("Wall.LeftSlingShot",),
    37: ("Bumper.Bumper4",), 38: ("Bumper.Bumper1",), 39: ("Bumper.Bumper3",), 40: ("Bumper.Bumper2",),
}
INPUT_OBJECTS.update({n: (f"Trigger.sw{n}",) for n in (25, 26, 28, 29, 30, 31, 33, 34)})
DIP_RANGES = {
    (1, 5): "Coin I credits per coin", (6, 7): "High game to date award", (8, 8): "Melody enable",
    (9, 13): "Coin III credits per coin", (16, 16): "Three or five balls",
    (17, 19): "Maximum credits", (20, 20): "Show credits", (21, 21): "Match enable",
    (23, 23): "Saucer multiplier schedule", (24, 24): "A/B scoring schedule",
    (25, 28): "Coin II credits per coin", (30, 31): "Special award mode", (32, 32): "High score award",
}
COILS = {
    1: (13, "Top saucer kicker", "AO-27-1300"),
    2: (3, "10-point chime", "CN-31-2000"), 3: (4, "100-point chime", "CN-31-2000"),
    4: (5, "1000-point chime", "CN-31-2000"), 5: (6, "Extra chime", "CN-31-2000"),
    6: (2, "Knocker", "AR-26-1200"), 7: (1, "Outhole kicker", "AN-26-1200"),
    8: (7, "Bottom left thumper coil", "AN-26-1200"), 9: (8, "Top left thumper coil", "AN-26-1200"),
    10: (9, "Top right thumper coil", "AN-26-1200"), 11: (10, "Bottom right thumper coil", "AN-26-1200"),
    12: (11, "Left slingshot coil", "AN-26-1200"), 13: (14, "Left drop bank reset", "NO-26-1900"),
    14: (12, "Right slingshot coil", "AN-26-1200"), 15: (15, "Right drop bank reset", "NO-26-1900"),
    18: (16, "Coin door lockout", "FO-36-7000"), 19: (17, "K1 flipper enable relay", None),
}
EFFECT_SENSORS = {1: 32, 7: 8, 8: 38, 9: 40, 10: 39, 11: 37, 12: 36, 14: 35}
COIL_OBJECTS = {coil: INPUT_OBJECTS[switch] for coil, switch in EFFECT_SENSORS.items()}
COIL_OBJECTS.update({46: ("Flipper.RightFlipper",), 48: ("Flipper.LeftFlipper",)})
BACKBOX_LAMPS = {
    11: "Backbox shoot again", 13: "Ball in play legend", 14: "Can play 1", 15: "Player up 1",
    27: "Match", 29: "High game to date", 30: "Can play 2", 31: "Player up 2",
    45: "Game over", 46: "Can play 3", 47: "Player up 3", 61: "Tilt legend",
    62: "Can play 4", 63: "Player up 4",
}
BONUS = (1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35)
AB_VALUE = (6, 22, 38, 54, 7)
LAMP_LABELS = {
    **{n: f"Bonus {value}K" for n, value in zip(BONUS, (*range(1, 11), 20), strict=True)},
    **{n: f"A/B value {value}K" for value, n in enumerate(AB_VALUE, 1)},
    **BACKBOX_LAMPS,
    23: "A/B value extra ball", 26: "Saucer 5X potential", 28: "5X bonus multiplier",
    36: "B lane lamps", 39: "A/B value special", 40: "Right outlane 50K",
    41: "Bottom right thumper lamp", 42: "Saucer 3X potential", 43: "Playfield shoot again",
    44: "3X bonus multiplier", 51: "Drop-target special", 52: "A lane lamps",
    56: "Left outlane 50K", 57: "Bottom left thumper lamp", 58: "Saucer 2X potential",
    59: "Apron credit indicator", 60: "2X bonus multiplier",
}
ROUND_INSERTS = (*BONUS, *AB_VALUE, 23, 39, 40, 51, 56)
LAMP_OBJECTS = {
    n: (f"Light.L{n}a",) for n in ROUND_INSERTS if n not in {2, 3, 51, 54, 56}
}
LAMP_OBJECTS.update({
    2: ("Light.L22",), 3: ("Light.L3",), 51: ("Light.L51",),
    54: ("Light.L54",), 56: ("Light.L56",), 59: ("Light.l59",),
    41: ("Light.BumpLight4",), 57: ("Light.BumpLight1",),
})
LAMP_GAPS = {
    26: "Two overlapping lights paint one 5X potential arrow. The socket center is unresolved.",
    28: "Two lights paint one 5X multiplier insert. The socket center is unresolved.",
    36: "A5/A6 specify two bulbs, one for each B indicator. L36a models the top insert. I36b and l36c overlap the side insert. Confirm both underside socket centers.",
    42: "Two overlapping lights paint one 3X potential arrow. The socket center is unresolved.",
    43: "Two lights paint one shoot-again insert. The socket center is unresolved.",
    44: "Two lights paint one 3X multiplier insert. The socket center is unresolved.",
    52: "A5/A6 specify two bulbs, one for each A indicator. L52a models the top insert. I52b and I52c overlap the side insert. Confirm both underside socket centers.",
    58: "Two overlapping lights paint one 2X potential arrow. The socket center is unresolved.",
    60: "Two lights paint one 2X multiplier insert. The socket center is unresolved.",
}
DRIVERS = {
    "matahari": ("Mata Hari", "1978", "Bally", "identical",
                 "Factory six-digit set, 2 KiB U2 and U6 images in the BY17 map."),
    "mataharb": ("Mata Hari (Free Play)", "2008", "Bally / Oliver", "compatible",
                 "Oliver's free-play set uses the two 4 KiB U2/U6 loader. The archive readme specifies 2732 hardware and S17–19 on for free play."),
    "mataharc": ("Mata Hari (Free Play+)", "2019", "Bally", "identical",
                 "Free Play+ with replacement 2 KiB 2716 images at U2 and U6 in the stock BY17 memory map. Variant-specific behavior has no retained native run."),
    "matahard": ("Mata Hari (Free Play and MODified rules)", "2025", "Bally / Quench", "compatible",
                 "Quench V22, two 4 KiB images in the BY35 address map on a suitably configured MPU. DIP 19 off retains six player digits and virtual millions."),
    "matahard7": ("Mata Hari (Free Play and MODified rules, 7-digit)", "2025", "Bally / Quench", "compatible",
                  "Same V22 ROM bytes and 4 KiB MPU addressing as matahard. DIP 19 on and a separate millions-digit strobe to all four aftermarket seven-digit player displays. Stock credits and match/ball fields remain two digits each."),
    "matatest": ("Mata Hari (New game rules MOD)", "2005", "Bally / Oliver", "compatible",
                 "Oliver revision 7 uses two 2732 program EPROMs, with new rules, a skill shot and DIP 25/26 free play."),
}


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"status": status, "source_refs": list(refs)}


def not_applicable(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def excerpt(name: str, locator: str) -> dict:
    path = EXCERPTS / f"{name}.md"
    return {"id": f"excerpt.mata-hari.{name}", "locator": locator,
            "path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path),
            "method": "manual", "transcribed_by": "Mata Hari primary curator", "reviewed": True}


def sources() -> list[dict]:
    identity = excerpt("identity-and-roms", "IPDB and OPDB identity, pinned declarations, archive text and installation references")
    self_test = excerpt("self-test", "FO 579 PDF pages 22, 23 and 25–26")
    parts = excerpt("parts-and-options", "FO 579 PDF pages 8–11 and 13–15")
    locations = excerpt("factory-locations", "FO 579 printed page 18 (PDF page 23)")
    crop = EXCERPTS / "factory-locations.webp"
    locations.update(
        image=crop.relative_to(ROOT).as_posix(), image_sha256=file_sha256(crop),
        image_derivation="Bally_1977_Mata_Hari_Manual_Color.pdf page 23, crop box 0.07,0.036,0.636,0.919, scanned page rendered at its native resolution (embedded image xref 74, 3328px across 11.00in), rendered at 181 dpi, capped to 870px wide, grayscale, 871x1758 WebP quality 66",
    )
    lamps = excerpt("lamp-wiring", "W-1182-5c, W-1187-1c, W-1192-1c and W-1186-4c")
    source_excerpts = {
        MANUAL: [self_test, parts],
        LOCATIONS: [locations],
        SCHEM: [
            excerpt("switch-wiring", "W-1186-4c, W-1187-1c and W-1192-1c"),
            excerpt("solenoid-wiring", "W-1183-5c and W-1186-4c through W-1192-1c"),
            lamps,
        ],
        A5: [lamps],
    }
    result = [
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame",
         "revision": PIN, "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
         "locator": "src/wpc/by35games.c Mata Hari declarations and dispBy6/dispBy7, by35.c board I/O, by35.h ROM loaders, core.c flipper synthesis, and src/libpinmame/libpinmame.cpp native interface."},
        {"id": IDENTITY, "kind": "human_review", "uri": IPDB, "source_id": "4501",
         "locator": "Mata Hari solid-state project and manufacture dates. Pinside, IPSND, OPDB and EM identifiers listed in the excerpt.",
         "attribution": "Internet Pinball Database, Pinside, IPSND and Open Pinball Database",
         "acquired_at": "2026-11-20T08:29:00Z", "excerpts": [identity]},
        {"id": ROM, "kind": "human_review", "uri": "https://www.pinheadz.net/mata-hari-new-rules",
         "locator": "Quench V21 author page and retained V22 archive documentation, Oliver Kaegi PCK-Bally and the Bally service bulletin.",
         "attribution": "Quench, Oliver Kaegi, Bally Manufacturing and PinMAME contributors", "excerpts": [identity]},
        {"id": BULLETIN, "kind": "service_bulletin",
         "uri": "https://howtopinball.com/files/pinball/paperwork/bally-classic/service-bulletins/bally-service-bulletin-book-1978.pdf",
         "locator": "PDF pages 28–30, Bally MPU service bulletin revised August 12, 1978. Tables I and II and the F.O. 597 upgrade notes.",
         "sha256": BULLETIN_SHA256, "original_filename": BULLETIN_FILE,
         "license": "NOASSERTION", "attribution": "Bally Manufacturing Corporation, scan hosted by How To Pinball",
         "acquired_at": "2026-11-20T09:05:24Z",
         "excerpts": [excerpt("mpu-service-bulletin", "PDF pages 28–30, Mata Hari and referenced jumper cells")]},
    ]
    for key, (filename, digest, time) in (FACTORY_FILES | {LOCATIONS: FACTORY_FILES[MANUAL]}).items():
        result.append({"id": key, "kind": "manual", "uri": f"https://www.ipdb.org/files/4501/{filename}",
                       "sha256": digest, "original_filename": filename, "source_id": "4501",
                       "locator": f"{IPDB} | " + ", ".join(item["locator"] for item in source_excerpts[key]),
                       "license": "NOASSERTION", "rights": "Retained locally for research",
                       "attribution": "Bally Manufacturing Corporation, hosted by the Internet Pinball Database",
                       "acquired_at": f"2026-11-20T{time}Z", "excerpts": source_excerpts[key]})
    for key, (filename, resource, picno, digest, description) in PHOTOS.items():
        result.append({"id": key, "kind": "human_review", "uri": f"https://www.ipdb.org/images/4501/{resource}",
                       "sha256": digest, "original_filename": filename, "source_id": "4501",
                       "locator": f"{description} | https://www.ipdb.org/showpic.pl?id=4501&picno={picno}",
                       "attribution": "Vic Camp / Internet Pinball Database", "rights": "NOASSERTION",
                       "acquired_at": "2026-11-20T08:30:49Z"})
    result.append({"id": DETAIL, "kind": "human_review",
                   "uri": "https://pinside.com/pinball/machine/mata-hari/gallery/legacy",
                   "locator": "Legacy archive photo Mata-Playfield-05, close-up of the upper potential arrows and bumper caps.",
                   "original_filename": "pinside-pf_Mata-Playfield-05.jpg",
                   "sha256": "1e52771fb12c2eb800e38ac4c7ded51fa5c1fa1104ac3229ebc50bdaef3ffe76",
                   "attribution": "Pinside legacy gallery", "rights": "NOASSERTION",
                   "acquired_at": "2026-11-20T08:35:06Z"})
    script_excerpt = excerpt("vpx-bindings", "Embedded script and gameitems in the two retained extractions")
    for year, info in TABLES.items():
        result.extend([
            {"id": f"vpx-table.mata-hari-{year}", "kind": "vpx_table",
             "uri": f"{VPX}/Mata Hari (Bally {year}).vpx", "sha256": info["sha256"],
             "revision": "vpxtool git:v0.33.3", "locator": f"extracted-{year}/gamedata.json, collections.json and gameitems. Full manifest {info['manifest_sha256']}.",
             "license": "NOASSERTION", "attribution": "Allknowing2012, shared JPSalas VP9 lineage", "excerpts": [script_excerpt]},
            {"id": f"vpx-script.mata-hari-{year}", "kind": "vpx_script",
             "uri": f"{VPX}/extracted-{year}/script.vbs", "sha256": info["script_sha256"],
             "revision": "vpxtool git:v0.33.3", "locator": "Embedded script, cGameName, solenoid bindings, Table1_Init and switch handlers.",
             "license": "NOASSERTION", "attribution": "Allknowing2012, JPSalas and JimmyFingers credits in script", "excerpts": [script_excerpt]},
        ])
    result.append({
        "id": CORPUS, "kind": "vpx_script",
        "uri": f"https://github.com/sverrewl/vpxtable_scripts/blob/{CORPUS_REVISION}/{quote(CORPUS_SCRIPT)}",
        "revision": CORPUS_REVISION, "sha256": CORPUS_SHA256,
        "locator": f"{CORPUS_SCRIPT}:1210–1211 and 3737–3742",
        "license": "NOASSERTION", "attribution": "UnclePaulie and other contributors credited in the script",
        "known_working": True, "excerpts": [script_excerpt],
    })
    runtime_excerpt = excerpt("native-runs", "Fresh-state LibPinMAME observations and retained command lines")
    for key, (filename, digest, time, locator) in RUNTIME.items():
        result.append({"id": key, "kind": "runtime_scenario", "uri": f"{REVIEW}/{filename}", "sha256": digest,
                       "revision": PIN, "locator": locator, "acquired_at": f"2026-11-20T{time}Z",
                       "attribution": "Mata Hari primary curator", "excerpts": [runtime_excerpt]})
    result.append({
        "id": AB_PLAY, "kind": "runtime_scenario",
        "uri": f"external:pinmame-review-artifacts/{ID}/{AB_FOLDER}/trace.json",
        "sha256": AB_SHA256, "revision": PIN, "acquired_at": "2026-11-20T09:49:26Z",
        "locator": "Fresh stock three-ball A/B lane and bumper probe. First pair completes at switch 30, raising both 41 and 57.",
        "attribution": "Mata Hari primary curator", "excerpts": [runtime_excerpt],
    })
    return result


def table_rows(excerpt_name: str, heading: str) -> list[list[str]]:
    lines = (EXCERPTS / f"{excerpt_name}.md").read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(heading))
    rows = []
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    if not rows:
        raise ValueError(f"Empty evidence table {excerpt_name}: {heading}")
    return rows


def wire(code: str) -> str:
    colors = {"1": "RED", "2": "BLU", "3": "YEL", "4": "GRN", "5": "WHT",
              "6": "BRN", "7": "ORN", "8": "BLK", "9": "GRY"}
    return "-".join(colors[mark] for mark in code.split("-", 1)[0] if mark != "0")


def item(prefix: str, group: str, number: int, label: str, kind: str, *refs: str,
         availability: str = "used", status: str = "validated") -> dict:
    return {"id": f"{prefix}.{slug(label)}", "label": label, "kind": kind,
            "binding": {"group": f"pinmame.{group}", "device": number}, "aliases": [],
            "availability": availability, "provenance": provenance(*refs, status=status)}


def normalize(geometry: dict, name: str) -> tuple[float, float]:
    bounds = geometry["bounds"]
    x, y = geometry["objects"][name][:2]
    nx = (x - bounds["left"]) / (bounds["right"] - bounds["left"])
    ny = (y - bounds["top"]) / (bounds["bottom"] - bounds["top"])
    if not (0 <= nx <= 1 and 0 <= ny <= 1):
        raise ValueError(f"Object {name} is off the playfield")
    return _round_point(nx), _round_point(ny)


def place(device: dict, objects: tuple[str, ...], role: str, geometry: dict, *refs: str) -> dict:
    placements = []
    for index, name in enumerate(objects, 1):
        nx, ny = normalize(geometry, name)
        placements.append({"id": f"placement.{device['id']}-{index}", "role": role, "space": "playfield",
                           "x": nx, "y": ny,
                           "provenance": provenance(GEOMETRY, *refs, status="observed")})
    return {"status": "observed", "placements": placements}


def build_inputs(geometry: dict) -> dict[int, dict]:
    inputs = {}
    cabinet = {6: ("13", "2", "23", "14"), 9: ("14", "3", "15", "9"),
               10: ("14", "3", "65", "10"), 11: ("14", "3", "20", "11"),
               16: ("14", "3", "50", "16")}
    for number in range(1, 49):
        fit = "optional" if number == 11 else "used" if number in SWITCHES else "unused"
        switch = item("switch", "input.switch", number, SWITCHES.get(number, f"Unfitted matrix position {number}"),
                      "switch" if number in SWITCHES else "virtual", CORE, MANUAL, SCHEM, availability=fit)
        switch["aliases"] = [{"namespace": "pinmame.switch", "value": str(number)},
                             {"namespace": "pinmame.switch", "value": f"{number:02d}"}] if number < 10 else [
                                 {"namespace": "pinmame.switch", "value": str(number)}]
        if fit == "unused":
            switch["spatial"] = not_applicable("unused", CORE, SCHEM)
            inputs[number] = switch
            continue
        switch["aliases"].append({"namespace": "manual.self-test", "value": f"{number:02d}"})
        switch["normally_closed"] = False
        if number in cabinet:
            strobe, strobe_pin, ret, ret_pin = cabinet[number]
            jack = "A4J3"
            switch["spatial"] = not_applicable("cabinet_or_service", MANUAL, SCHEM)
        else:
            col, row = divmod(number - 1, 8)
            strobe, strobe_pin = ("51", "93", "52", "53", "31")[col], str(col + 1)
            ret, ret_pin = ("54", "56", "57", "58", "60", "63", "65", "70")[row], str(row + 8)
            jack = "A4J2"
        switch["wiring"] = {"board": "A4", "drive_wire": wire(strobe), "drive_connection": f"{jack}-{strobe_pin}",
                            "return_wire": wire(ret), "return_connection": f"{jack}-{ret_pin}"}
        if number == 7:
            switch["physical"] = {"quantity": 3, "switch_type": "tilt", "location": "Cabinet and playfield underside",
                                  "notes": "Cabinet plumb bob and roll cage (A4J3-2/-15) parallel the playfield tilt contact at the listed A4J2 pair. Its precise under-playfield location is unresolved."}
        elif number == 16:
            switch["physical"] = {"switch_type": "tilt", "location": "Coin door and cabinet",
                                  "notes": "Two parallel contacts are drawn. Manual page 2 identifies one factory door contact and optional extra cabinet contacts. Page 17 prints SLAM (2)."}
        elif number == 27:
            switch["physical"] = {"quantity": 2, "switch_type": "leaf", "location": "Behind drop banks",
                                  "notes": "Two normally-open contacts in parallel. These are scoring rebounds without a coil."}
        elif number in cabinet:
            switch["physical"] = {"location": "Coin door", "switch_type": "button" if number == 6 else "other"}
        elif number in INPUT_OBJECTS:
            switch["physical"] = {"location": "Playfield", "switch_type": "leaf"}
        if 17 <= number <= 20:
            switch["physical"]["notes"] = (
                f"The factory callout locates this switch at {INPUT_OBJECTS[number][0]}. "
                f"Both VPX versions assign {number} to HitTarget.Target{number - 11}, reversing the bank."
            )
        if number == 8:
            switch["initial_active"] = True
            switch["physical"]["part_number"] = "AS-2806-21"
        if number in INPUT_OBJECTS:
            switch["spatial"] = place(switch, INPUT_OBJECTS[number], "sensor", geometry, SCRIPT, MANUAL)
        inputs[number] = switch

    for number, label in {-7: "Coin door self-test", -6: "MPU S33 diagnostic", -5: "Unfitted sound diagnostic"}.items():
        fit = "unused" if number == -5 else "used"
        switch = item("switch", "input.switch", number, label, "virtual" if number == -5 else "switch",
                      CORE, MANUAL, SCHEM, availability=fit)
        switch["spatial"] = not_applicable("unused" if number == -5 else "cabinet_or_service", CORE, MANUAL)
        if number != -5:
            switch["normally_closed"] = False
        if number == -7:
            switch["wiring"] = {"board": "A4/A3", "drive_connection": "A4J3-1", "drive_wire": "RED",
                                "return_connection": "A3J2-7", "return_wire": "YEL-RED"}
        inputs[number] = switch

    for number in range(81, 89):
        side = {82: "Right", 84: "Left"}.get(number)
        label = f"{side} cabinet flipper button" if side else f"Unused core flipper-column position {number}"
        switch = item("switch", "input.switch", number, label, "switch" if side else "virtual",
                      CORE, SCHEM, availability="used" if side else "unused")
        switch["spatial"] = not_applicable("cabinet_or_service" if side else "unused", CORE, SCHEM)
        if side:
            switch["normally_closed"] = False
            switch["physical"] = {"location": f"{side} cabinet wall", "switch_type": "leaf",
                                  "notes": "Cabinet-wired contact. PinMAME reads the core button bit for synthetic flippers. The production MPU switch matrix does not receive this contact."}
            switch["wiring"] = {"board": "A3/A2", "drive_connection": f"A3J2-{1 if number == 82 else 2}",
                                "drive_wire": "RED" if number == 82 else "BLU", "return_connection": "A2J2-9", "return_wire": "ORN"}
        inputs[number] = switch
    return inputs


def build_dips() -> list[dict]:
    labels = {n: label for (start, end), label in DIP_RANGES.items() for n in range(start, end + 1)}
    return [
        item("dip", "input.dip", n, f"S{n} {labels.get(n, 'unverified option')}", "dip_switch",
             CORE, MANUAL, availability="used" if n in labels else "unknown",
             status="validated" if n in labels else "candidate")
        | {"spatial": not_applicable("dip_switch", MANUAL, CORE),
           "physical": {"location": "A4 MPU in backbox", "switch_type": "dip"}}
        for n in range(1, 33)
    ]


def build_coils(geometry: dict) -> dict[int, dict]:
    momentary = [row for row in table_rows("solenoid-wiring", "| Selector") if row[-1].isdigit()]
    continuous = table_rows("solenoid-wiring", "| PIA bit")
    drivers = {int(row[-1]): row[2] for row in momentary + continuous}
    main_jacks = {int(row[-1]): row[3].split(" / ", 1)[0] for row in momentary}
    main_jacks.update({18: "J2-8", 19: "J3-5"})
    wire_at_jack = {connector: code for _, code, connector in table_rows("solenoid-wiring", "| Load destination")}
    result = {}
    for number, (self_test, label, part) in COILS.items():
        slot = "coil" if number != 19 else "relay"
        device = item("device", "output.solenoid", number, label, slot, CORE, MANUAL, SCHEM, SERVICE)
        device["aliases"] = [{"namespace": "manual.self-test", "value": f"{self_test:02d}"}]
        connector = main_jacks[number]
        wire_code = wire_at_jack[connector]
        device["wiring"] = {"board": "AS-2518-22", "driver_transistor": drivers[number],
                            "nominal_voltage_v": 43, "voltage_type": "dc"}
        if number == 19:
            device["wiring"].update(power_connection="A3J3-5 to A2J3-9", power_wire=wire(wire_code),
                                    control_connection="A3J3-8")
        else:
            device["wiring"].update(drive_connection=f"A3{connector}", drive_wire=wire(wire_code))
        if part:
            device["physical"] = {"part_number": part}
        if number in COIL_OBJECTS:
            device["spatial"] = place(device, COIL_OBJECTS[number], "effect", geometry, MANUAL, SCHEM, PLAY)
        elif number in (13, 15):
            device["physical"]["notes"] = "Assembly drive. A6 shows two parallel coil symbols on this line. The parts list and retained underside view do not establish two fitted coils per bank."
        else:
            device["spatial"] = not_applicable("cabinet_or_service", MANUAL, SCHEM)
        result[number] = device
    for number, bit, pin in ((17, "PB4", "A3J5-7"), (20, "PB7", "A3J2-15 / A3J5-3")):
        device = item("device", "output.solenoid", number, f"Unfitted continuous line {bit}", "virtual",
                      CORE, SCHEM, PLAY, availability="unknown", status="observed")
        device["wiring"] = {"board": "AS-2518-22", "driver_transistor": drivers[number], "drive_connection": pin}
        device["physical"] = {"notes": "No factory load on this line. A pulse is observed during fresh boot and its ROM purpose is unverified."}
        device["spatial"] = not_applicable("no_physical_device", CORE, SCHEM)
        result[number] = device
    for number, side in ((45, "right"), (47, "left")):
        device = item("device", "output.solenoid", number, f"Synthetic {side} flipper pair mirror", "virtual",
                      CORE, PLAY)
        device["spatial"] = not_applicable("virtual", CORE, PLAY)
        device["physical"] = {"notes": "Core mirror of the same enabled button held state. It does not measure a second actuator or winding."}
        result[number] = device
    for number, side, drive, button, code in ((46, "Right", "9", "1", "70"), (48, "Left", "8", "2", "40")):
        device = item("device", "output.solenoid", number, f"{side} flipper coil assembly", "coil", CORE, MANUAL, SCHEM, PLAY)
        device["physical"] = {"part_number": "AQ-25-500/34-5050", "assembly_part_number": "AS-2214-24",
                              "notes": "PinMAME's synthesized active state represents the flipper assembly. K1 enables the physical button circuit. A local EOS contact switches the winding circuit."}
        device["wiring"] = {"board": "AS-2518-22", "drive_connection": f"A3J1-{drive}", "drive_wire": wire(code),
                            "control_connection": f"K1 via A3J2-{button}", "power_connection": "A2J1-6",
                            "power_wire": "BRN", "nominal_voltage_v": 43, "voltage_type": "dc"}
        device["spatial"] = place(device, COIL_OBJECTS[number], "effect", geometry, MANUAL, SCHEM, PLAY)
        result[number] = device
    return result


def build_lamps(geometry: dict) -> list[dict]:
    connector_rows = table_rows("lamp-wiring", "| Pin |")
    connector_codes = {f"J{jack}-{number}": cell.split()[0] for number, *cells in connector_rows
                       for jack, cell in enumerate(cells, 1)}
    result = []
    rows = table_rows("lamp-wiring", "| Public |")
    if [int(row[0]) for row in rows] != list(range(1, 65)):
        raise ValueError("Four complete A5 decoder banks are required")
    for raw_number, transistor, pins, _caption in rows:
        number = int(raw_number)
        if number % 16 == 0:
            continue
        main_pin = pins.split(" / ", 1)[0]
        used = number in LAMP_LABELS
        fit = "used" if used else "unknown" if number in {4, 20} else "unused"
        device = item("lamp", "output.lamp", number, LAMP_LABELS.get(number, f"Unfitted A5 lamp driver {number}"),
                      "lamp", CORE, A5, SCHEM, SERVICE, availability=fit,
                      status="observed" if fit == "unknown" else "validated")
        device["wiring"] = {"board": "AS-2518-23", "driver_transistor": transistor,
                            "drive_connection": f"A5{main_pin}", "drive_wire": wire(connector_codes[main_pin])}
        if not used:
            device["spatial"] = not_applicable("no_physical_device" if fit == "unknown" else "unused", A5, SCHEM)
            if fit == "unknown":
                device["provenance"]["source_refs"].append(PLAY)
                device["physical"] = {"notes": "The factory harness marks this branch N/U. The stock ROM blinks public lamps 4 and 20 together in attract, with about a second between edges, then holds both on throughout the recorded gameplay. Firmware purpose is unresolved."}
            result.append(device)
            continue
        device["physical"] = {"part_number": "E-125-22", "location": "Backbox" if number in BACKBOX_LAMPS else "Playfield",
                              "quantity": 2 if number in (36, 52) else 1}
        device["wiring"].update(nominal_voltage_v=5.4, voltage_type="dc")
        if number in BACKBOX_LAMPS:
            device["spatial"] = not_applicable("cabinet_or_service", MANUAL, SCHEM)
            device["wiring"]["power_connection"] = "A2J3-6"
        else:
            device["wiring"]["power_connection"] = "A2J1-7"
        if number in LAMP_OBJECTS:
            refs = (A5, TOP, GEOMETRY_1977) if number in (41, 57) else (A5, SCRIPT, TOP)
            device["spatial"] = place(device, LAMP_OBJECTS[number], "emitter", geometry, *refs)
        if number in LAMP_GAPS:
            device["physical"]["notes"] = LAMP_GAPS[number]
        elif number == 41:
            device["provenance"]["source_refs"].extend((AB_PLAY, SCRIPT, CORPUS))
            device["physical"]["notes"] = "Factory right lower cap. The stock three-ball probe published 41 and 57 together on the first A/B completion. Drive the right cap from 41. The retained VPX builds and the corpus v2.0.0 drive both caps from 41."
        elif number == 57:
            device["provenance"]["source_refs"].extend((AB_PLAY, SCRIPT, CORPUS))
            device["physical"]["notes"] = "Factory left lower cap. The stock three-ball probe published 57 alongside 41 on the first A/B completion. Drive the left cap from 57. The retained BumpLight1 follows 41, as does the left cap in corpus v2.0.0. Upper-right BumpLight3 belongs to VPX GI."
        elif number == 59:
            device["physical"].update(location="Left apron", notes="A6 labels J3-13 CREDIT INDICATOR. The mounted apron lens is on the playfield assembly.")
        elif number == 49:
            device["physical"]["notes"] = "A6 misprints A5J1-1. The A5 decoder and A5 connector list agree on J3-1."
        result.append(device)
    if set(LAMP_LABELS) != {d["binding"]["device"] for d in result if d["availability"] == "used"}:
        raise ValueError("Named lamp inventory does not match the decoder rows")
    return result


def displays_and_drivers() -> tuple[list[dict], list[dict]]:
    display_specs = [(f"player-{n}-score", f"Player {n} score", 2 + (n - 1) * 8, 6) for n in range(1, 5)]
    display_specs += [("credits", "Credits", 35, 2), ("match-ball-in-play", "Match / ball in play", 38, 2)]
    displays = [
        {"id": f"display.{name}", "label": label, "controller_index": i, "kind": "segment",
         "segment_start": start, "width": width, "physical_location": "cabinet_or_service",
         "spatial": not_applicable("cabinet_or_service", MANUAL, SCHEM, CORE),
         "provenance": provenance(MANUAL, SCHEM, CORE, SERVICE)}
        for i, (name, label, start, width) in enumerate(display_specs)
    ]
    drivers = []
    for key, (description, year, manufacturer, compatibility, notes) in sorted(DRIVERS.items()):
        driver = {"id": key, "description": description, "year": year, "manufacturer": manufacturer, "flags": 0,
                  "physical_compatibility": compatibility, "variant_notes": notes}
        if key != "matahari":
            driver["clone_of"] = "matahari"
        if key == "matahard7":
            driver["display_overrides"] = [
                {"target": display["id"], "controller_index": display["controller_index"],
                 "segment_start": display["segment_start"] - 1, "width": 7,
                 "provenance": provenance(CORE, ROM, V22)}
                for display in displays[:4]
            ]
        drivers.append(driver)
    return displays, drivers


def mechanisms_and_relationships(inputs: dict, coils: dict) -> tuple[list[dict], list[dict]]:
    mechanisms = []

    def add(label, kind, outs, switches, behavior, part=None):
        entry = {"id": f"mech.{slug(label)}", "label": label, "kind": kind,
                 "actuators": [coils[n]["id"] for n in outs], "sensors": [inputs[n]["id"] for n in switches],
                 "behavior": behavior, "provenance": provenance(MANUAL, SCHEM, PLAY, SCRIPT)}
        if part:
            entry["assembly_part_number"] = part
        mechanisms.append(entry)

    add("Outhole and shooter feed", "kicker", [7], [8],
        "One ball rests on the outhole wire below the flippers. The ROM counts and serves it to the right shooter alley. Release the switch when the ball clears the contact. The plunger is manual.")
    add("Top-centre saucer", "kicker", [1], [32],
        "The cup holds one ball and the closed contact signals occupancy. The ROM awards saucer scoring and fires the kicker. Release the contact when the ball actually exits.")
    for side, switch, coil, part in (("left", 21, 13, "AS-2795-45"), ("right", 17, 15, "AS-2795-44")):
        add(f"{side.title()} four-drop bank", "drop_target_bank", [coil], range(switch, switch + 4),
            "Four individual D, C, B, A switches bottom to top. Contacts hold closed as their targets latch down. A shared reset drive returns all four targets up and opens those contacts. The stock probe reset both banks after all eight targets fell.", part)
    add("Upper target-area rebound contacts", "other", [], [27],
        "Two parallel 10-point rebound contacts behind the banks. Either momentary closure gives the same matrix address. The upper VPX sling events represent the contacts.")
    for coil, switch in EFFECT_SENSORS.items():
        if coil in (1, 7):
            continue
        add(inputs[switch]["label"], "other", [coil], [switch],
            "The ball briefly closes the contact. With play enabled the ROM pulses this assembly's coil. The conversion uses native simulated rebound geometry.")
    for side, button, coil in (("right", 82, 46), ("left", 84, 48)):
        add(f"{side.title()} flipper", "other", [coil], [button],
            "Cabinet button and K1 contact energize the dual-winding assembly. Local EOS opens at end of stroke and the return spring lowers the flipper at release. PinMAME publishes one held enabled-button pair for the assembly.", "AS-2214-24")
    add("K1 flipper enable", "other", [19], [],
        "One backbox relay has two contacts, one for each local flipper circuit. The ROM asserts its driver when play is enabled and drops it on tilt.")
    add("Shooter lane ball gate", "gate", [], [],
        "Passive ball gate in the upper right shooter arch. It lets a launched ball enter the upper playfield and restricts return to the shooter alley.", "A-1475-9")
    add("Cabinet chime assembly", "other", [2, 3, 4, 5], [],
        "Four switched chime coils provide scoring and tunes. The driver declares no sound board.")
    add("Replay knocker", "other", [6], [],
        "The backbox knocker is a momentary coil with a physical strike. It is separate from the four chimes.")
    add("Coin door lockout", "other", [18], [9, 10, 11],
        "One continuous lockout coil serves the coin door, which carries right and left chutes and a provision for a centre chute. The chute contacts report accepted coins independently.")
    links = [
        {"id": f"relationship.switch-{switch}-pulses-coil-{coil}", "kind": "pulse",
         "source": inputs[switch]["id"], "destination": coils[coil]["id"], "provenance": provenance(SCHEM, PLAY)}
        for coil, switch in EFFECT_SENSORS.items() if coil not in (1, 7)
    ]
    links.extend(
        {"id": f"relationship.flipper-enable-{side}", "kind": "relay_gated",
         "source": coils[19]["id"], "destination": coils[coil]["id"], "provenance": provenance(SCHEM, CORE, PLAY)}
        for side, coil in (("right", 46), ("left", 48))
    )
    return mechanisms, links


def build() -> tuple[dict, dict]:
    geometry = load_json(SEEDS / f"{SLUG}-geometry.json")
    primary = geometry["1978"]
    inputs = build_inputs(primary)
    coils = build_coils(primary)
    outputs = [coils[n] for n in sorted(coils)] + build_lamps(primary)
    displays, drivers = displays_and_drivers()
    mechanisms, links = mechanisms_and_relationships(inputs, coils)
    source_records = sources()
    definition = {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {"id": ID, "name": "Mata Hari", "manufacturer": "Bally", "year": 1978,
                    "kind": "physical_pinball", "model_number": "1104-E", "ipdb_id": 4501, "opdb_id": "G417e-MDvXz"},
        "controller": {"platform": "pinmame.by17", "hardware_generation": "0x200000", "inversion_applied_by_emulator": True},
        "drivers": drivers, "inputs": [inputs[n] for n in sorted(inputs)] + build_dips(),
        "outputs": outputs, "displays": displays, "mechanisms": mechanisms, "relationships": links,
        "coverage": {
            "status": "partial",
            "missing": ["input_semantics", "output_semantics", "mechanism_behavior", "variant_differences", "spatial_placement"],
            "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated",
                           "semantic_naming": "observed", "physical_wiring": "observed", "mechanisms": "observed",
                           "variant_coverage": "observed", "recreation_knowledge": "validated",
                           "spatial_placement": "observed", "runtime_observation": "observed",
                           "causal_exercise": "observed"},
        },
        "conflicts": [],
        "sources": source_records,
        "knowledge": {"path": KNOWLEDGE.relative_to(ROOT).as_posix(), "status": "partial"},
    }
    callouts = load_json(CALLOUTS)
    callouts["checks"] = {}
    for key, page in callouts["pages"].items():
        for control in page["controls"]:
            control["xy"] = normalize(primary, control["object"])
        for read in page["reads"]:
            placement = inputs[int(read["label"])]["spatial"]["placements"][0]
            callouts["checks"][placement["id"]] = {"page": key, "label": read["label"]}
    decisions = drawing_callouts.apply_to_definition(definition, callouts, LOCATIONS)
    anchors = {}
    for devices, locations in ((inputs, INPUT_OBJECTS), (coils, COIL_OBJECTS)):
        for n, point_objects in locations.items():
            anchors[devices[n]["id"]] = list(point_objects)
    for output in outputs:
        n = output["binding"]["device"]
        if output["kind"] == "lamp" and n in LAMP_OBJECTS:
            anchors[output["id"]] = list(LAMP_OBJECTS[n])
    report = {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": ID,
        "decision": "partial",
        "vpxtool_version": "git:v0.33.3",
        "table_builds": {str(year): info | {"extraction": f"extracted-{year}", "bounds": geometry[str(year)]["bounds"]}
                         for year, info in TABLES.items()},
        "manifest_algorithm": "tools/build_external_evidence_manifest.py, full case-sensitive POSIX-relative path/size/SHA-256 list, compact sorted-key UTF-8 JSON plus LF.",
        "transform": "Player view x = raw x / 952, y = raw y / 1927. Repository coordinate rounding to six decimals.",
        "placement_objects": anchors,
        "factory_callouts": drawing_callouts.summary(
            callouts, decisions, CALLOUTS.relative_to(ROOT).as_posix(), file_sha256(CALLOUTS)
        ),
        "fixture_gaps": {str(n): note for n, note in LAMP_GAPS.items()},
        "unplaced_switches": [7],
        "unplaced_solenoid_drives": [13, 15],
        "gi_candidate_objects_only": {
            year: [f"Light.{name}" for name in data["gi_lights"]
                   if data["objects"][f"Light.{name}"][3]]
            for year, data in geometry.items()
        },
        "excluded_gi": ["Out-of-frame Light4 and Light5", "Bumper-cap visual lights without separate GI socket proof",
                        "Close or duplicated bulb objects without a harness or photo match"],
        "photo_and_manual_sources": [record for record in source_records if record["id"] in {TOP, UNDERSIDE, DETAIL, MANUAL, LOCATIONS, SCHEM, A5}],
    }
    return definition, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if (ROOT / f"machines/author-ready/bally/{SLUG}.json").exists():
        raise SystemExit("Refusing to overwrite a game with an author-ready artifact")
    definition, report = build()
    artifacts = {
        DEFINITION: canonical_bytes(definition),
        KNOWLEDGE: (SEEDS / f"{SLUG}-knowledge.md").read_bytes(),
        REPORT.with_suffix(".json"): canonical_bytes(report),
        REPORT.with_suffix(".md"): (SEEDS / f"{SLUG}-spatial.md").read_bytes(),
    }
    for path, data in artifacts.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"Mata Hari artifact drift: {path.relative_to(ROOT)}")
        else:
            write_bytes(path, data)
    if args.check:
        print("Mata Hari artifacts are current")


if __name__ == "__main__":
    main()
