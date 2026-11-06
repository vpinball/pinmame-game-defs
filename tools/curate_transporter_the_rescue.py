"""Build the partial Transporter the Rescue definition from pinned, reviewable facts.

The manual supplies physical labels and wiring, the retained script supplies runtime bindings,
and the exact VPX extraction supplies observed geometry. No image or ROM is redistributed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path

import drawing_callouts
from build_external_evidence_manifest import build_manifest, canonical_bytes as manifest_bytes
from pinmame_flipper_column import (
    VPM_CORE_SHA256, VPM_S11_SHA256, VPM_LIBRARY_SOURCE, VPM_LIBRARY_URI,
    flipper_column_inputs, flipper_column_relationships,
)
from pinmame_game_defs.jsonio import canonical_bytes, load_json, write_json, write_text

ROOT = Path(__file__).resolve().parents[1]
ID = "bally.transporter-the-rescue.1989"
FACTS = Path("tools/seeds/bally/transporter-the-rescue-1989-facts.json")
SPATIAL_FACTS = Path("tools/seeds/bally/transporter-the-rescue-1989-spatial.json")
SEED = Path("tools/seeds/bally/transporter-the-rescue-1989.json")
DEFINITION = Path("machines/partial/bally/transporter-the-rescue-1989.json")
AUTHOR = Path("machines/author-ready/bally/transporter-the-rescue-1989.json")
KNOWLEDGE = Path("knowledge/bally/transporter-the-rescue-1989.md")
REPORT = Path("reports/spatial/bally/transporter-the-rescue-1989.json")
REPORT_MD = Path("reports/spatial/bally/transporter-the-rescue-1989.md")
MANUAL = "manual.bally.transporter-the-rescue.1989"
CORE = "pinmame.core.46e1a01a0f73"
VPX = "vpx-table.transporter-vpw-105"
SCRIPT = "vpx-script.transporter-vpw-105"
EXTRACTION = "vpx-extraction.transporter-vpw-105"
CALLOUT_SOURCE = "drawing-callouts.transporter.1989"
CALLOUT_PATH = Path("tools/seeds/bally/transporter-the-rescue-1989-callouts.json")
PHOTO_PATH = Path("tools/seeds/bally/transporter-the-rescue-1989-photo-sockets.json")
PHOTO_SOURCE = "photo.transporter.underplayfield"
BULLETIN = "service-bulletin.transporter.1989"
RUNTIME = "runtime.transporter.l3-service"
RUNTIME_PATH = Path("evidence/runtime/system-11/transporter-l3-service.json")
RUNTIME_SHA = "099a26aed5154f060649b747d21a677fd997744ff6bda79cc9f37872e3e1b982"
LAMP_RUNTIME_PATH = Path("evidence/runtime/system-11/transporter-l3-single-lamps.json")
LAMP_RUNTIME_SHA = "d98720799973b5792d72b4a0ee3a6b86dccfd549393966ffd86b060086a6d47f"
REVISION = "46e1a01a0f73dc5ce163d98db1ae435883ecc450"
MANIFEST_SHA = "adbdad05e280be0e58c2364cf9d0992b20624da4ad280ce1ee5001e839818165"
EXTRACTION_PATH = Path("bally/transporter-the-rescue-1989/extracted-vpxtool")
VPX_ORIGIN = "https://vpuniverse.com/files/file/7899-transporter-the-rescue-bally-1989-vpw/"
VPX_ACQUIRED_AT = "2026-11-06T08:58:54.988127+00:00"
VPX_ACQUISITION = f"Origin {VPX_ORIGIN}; extractor vpxtool git:v0.33.3; acquired_at records the source archive acquisition from its retained mtime"
WIDTH, HEIGHT = 952.965, 1976.52
DRAWINGS = {
    "switch-locations": (54, "0.235,0.145,0.695,0.86", 265, "1172x2348"),
    "lamp-locations": (56, "0.21,0.14,0.69,0.865", 275, "1222x2380"),
    "solenoid-locations": (58, "0.22,0.15,0.745,0.88", 285, "1337x2397"),
    "drop-target-circuit": (61, "0.07,0.43,0.9,0.925", 300, "2112x1625"),
}
UNUSED_SWITCH = {18, 28, 29, 32, 36, 38, *range(41, 57)}
SWITCH_OBJECTS = {
    10: "Drain", 11: "BallRelease", 12: "Trough2", 13: "Trough3",
    **{i: f"SW{i}" for i in (14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 30, 31, 33, 34, 35, 37, 39, 40, 59)},
    60: "Bumper1", 61: "Bumper2", 62: "Bumper3", 63: "LeftSlingShot", 64: "RightSlingShot",
}
COIL_OBJECTS = {
    1: "Drain", 2: "BallRelease", 3: "SW20", 4: "SW23", 5: "LockLSol",
    6: "SW15", 8: "LockRSol", 10: "GateSol10", 14: "KickBack",
    17: "Bumper1", 18: "LeftSlingShot", 19: "Bumper2",
    20: "RightSlingShot", 21: "Bumper3",
}


def prov(*refs: str, status: str = "validated") -> dict:
    return {"source_refs": list(refs), "status": status}


def na(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": prov(*refs)}


def located(item_id: str, role: str, objects: list[str], facts: dict, status: str = "observed") -> dict:
    placements = []
    for i, name in enumerate(objects, 1):
        obj = facts["objects"][name]
        x, y = round(obj["x"] / WIDTH, 6), round(obj["y"] / HEIGHT, 6)
        if name in ("Flasherbase1", "Flasherbase2"):
            # The factory calls these playfield flashers; they sit on the rear rail. This is
            # an explicit projection onto that rail, not a silent clamp of arbitrary objects.
            y = 0.0
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise ValueError(f"out-of-bounds table object: {name}")
        placements.append({
            "id": f"{item_id}.{role}.{i}", "role": role, "space": "playfield",
            "x": x, "y": y, "provenance": prov(VPX, SCRIPT, MANUAL, status=status),
        })
    return {"status": status, "placements": placements}


def aliases(facts: dict, section: str, group: str, address: int, manual: str | None = None) -> list[dict]:
    prior = next((x for x in facts["legacy"][section] if x["binding"] == {"group": group, "device": address}), None)
    result = list(prior["aliases"]) if prior else []
    namespace = {"pinmame.input.switch": "pinmame.switch", "pinmame.output.lamp": "pinmame.lamp",
                 "pinmame.output.solenoid": "pinmame.solenoid"}.get(group)
    for alias in ([{"namespace": namespace, "value": str(address)}] if namespace else []) + (
        [{"namespace": "manual.address", "value": manual}] if manual else []
    ):
        if alias not in result:
            result.append(alias)
    return result


def legacy_id(facts: dict, section: str, group: str, address: int, default: str) -> str:
    prior = next((x for x in facts["legacy"][section] if x["binding"] == {"group": group, "device": address}), None)
    return prior["id"] if prior else default


def source_records(facts: dict, root: Path) -> list[dict]:
    excerpts = []
    for name, locator in (
        ("lamp-matrix", "PDF 39 (1-36), repeated PDF 55 (2-6)"),
        ("switch-matrix", "PDF 42 (1-39)"), ("switch-parts", "PDF 53 (2-4)"),
        ("solenoid-table", "PDF 40 (1-37)"), ("solenoid-parts", "PDF 57 (2-8)"),
        ("assemblies-and-circuits", "PDF 6, 7, 51, 61 and 78"),
    ):
        path = Path(f"evidence/excerpts/{ID}/{name}.md")
        excerpts.append({
            "id": f"excerpt.transporter.{name}", "path": path.as_posix(), "locator": locator,
            "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
            "method": "mixed", "transcribed_by": "Initial transcription, independently visually verified by the primary curator",
            "reviewed": True,
        })
    bulletin_path = Path(f"evidence/excerpts/{ID}/service-bulletins.md")
    runtime_path = root / RUNTIME_PATH
    if hashlib.sha256(runtime_path.read_bytes()).hexdigest() != RUNTIME_SHA:
        raise ValueError("compact runtime evidence differs from its pinned hash")
    if hashlib.sha256((root / LAMP_RUNTIME_PATH).read_bytes()).hexdigest() != LAMP_RUNTIME_SHA:
        raise ValueError("compact lamp evidence differs from its pinned hash")
    for name, (page, crop, xref, pixels) in DRAWINGS.items():
        excerpt = file_excerpt(root, name, name + ".md", f"PDF {page}, factory drawing")
        image = Path(f"evidence/excerpts/{ID}/{name}.webp")
        excerpt.update(image=image.as_posix(), image_sha256=hashlib.sha256((root / image).read_bytes()).hexdigest(),
                       image_derivation=f"Bally_1989_Transporter_the_Rescue_English_Manual.pdf page {page}, crop box {crop}, scanned page rendered at its native resolution (embedded image xref {xref}, 2544px across 8.48in), rendered at 300 dpi, grayscale, {pixels} WebP quality 60")
        excerpts.append(excerpt)
    return facts["legacy_sources"] + [
        {"id": CORE, "kind": "pinmame_core", "uri": "https://github.com/vpinball/pinmame",
         "revision": REVISION, "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
         "locator": "src/wpc/s11games.c tsptrGameData; s11.c switch and solenoid paths; core.c flipper synthesis"},
        {"id": "pinmame.catalog.46e1a01a0f73", "kind": "pinmame_catalog", "uri": "https://github.com/vpinball/pinmame",
         "revision": REVISION, "license": "BSD-3-Clause", "attribution": "PinMAME contributors",
         "locator": "PinmameGetGames six-driver tsptr_l3 clone tree, reconciled against src/wpc/s11games.c lines 975-1038"},
        {"id": MANUAL, "kind": "manual",
         "uri": "https://www.ipdb.org/files/2630/Bally_1989_Transporter_the_Rescue_English_Manual.pdf",
         "sha256": "d1e29962c3bc53733ba61a62d8d814d2a1adbf508f78dfe10c01cd4fb95f2ce9",
         "locator": "IPDB machine page https://www.ipdb.org/machine.cgi?id=2630; switch, lamp and solenoid matrices, parts lists and location diagrams",
         "source_id": "2630", "original_filename": "Bally_1989_Transporter_the_Rescue_English_Manual.pdf",
         "attribution": "Bally/Midway Manufacturing Company and Williams; hosted by IPDB", "license": "NOASSERTION",
         "acquired_at": "2026-11-06T09:00:00Z", "excerpts": excerpts},
        {"id": BULLETIN, "kind": "service_bulletin",
         "uri": "https://www.ipdb.org/files/2630/Bally_1989_Transporter_the_Rescue_Service_Bulletin_Book_1989_includes_Transporter_SB11_SB13.pdf",
         "sha256": "c12614faa3efee725c0c6ff0e586087987eead49fa024fe1107e61654ea1599c",
         "locator": "Service bulletin book PDF 29 and 34, SB11 and SB13",
         "source_id": "2630", "original_filename": "Bally_1989_Transporter_the_Rescue_Service_Bulletin_Book_1989_includes_Transporter_SB11_SB13.pdf",
         "attribution": "Bally/Midway Manufacturing Company and Williams; hosted by IPDB", "license": "NOASSERTION",
         "acquired_at": "2026-11-06T09:00:00Z",
         "excerpts": [{"id": "excerpt.transporter.service-bulletins", "path": bulletin_path.as_posix(),
                       "locator": "PDF 29 and 34, SB11 and SB13",
                       "sha256": hashlib.sha256((root / bulletin_path).read_bytes()).hexdigest(),
                       "method": "manual", "transcribed_by": "primary curator", "reviewed": True}]},
        {"id": RUNTIME, "kind": "runtime_scenario", "uri": "internal:evidence/runtime/system-11/transporter-l3-service.json",
         "sha256": RUNTIME_SHA, "revision": REVISION, "attribution": "pinmame-game-defs curation",
         "locator": "LibPinMAME tsptr_l3 coil and switch service tests; static U27 switch names for l3/lx4/lx4b"},
        {"id": "runtime.transporter.l3-single-lamps", "kind": "runtime_scenario", "uri": "internal:" + LAMP_RUNTIME_PATH.as_posix(),
         "sha256": LAMP_RUNTIME_SHA, "revision": REVISION, "attribution": "pinmame-game-defs curation",
         "locator": "ROM Single Lamps steps 1-64 pair display numbers and public lamp transitions; 18/56 display NOT USED while the diagnostic sweep pulses them"},
        {"id": VPX, "kind": "vpx_table", "uri": "external:pinmame-vpx-sources/bally/transporter-the-rescue-1989/Transporter%20the%20Rescue%20%28Midway%201989%29%20VPW%20v1.05.vpx",
         "sha256": "4cd27942999d39e6f1e23e6a2d65f24b61dc176f7eb5ede9c720a981c05718ff",
         "locator": "Retained VPW v1.05 table; bounds left/top 0/0, right/bottom 952.965/1976.52; " + VPX_ACQUISITION,
         "acquired_at": VPX_ACQUIRED_AT,
         "original_filename": "Transporter the Rescue (Midway 1989) VPW v1.05.vpx",
         "attribution": "VPW table authors and contributors", "license": "NOASSERTION"},
        {"id": SCRIPT, "kind": "vpx_script", "uri": "external:pinmame-vpx-sources/bally/transporter-the-rescue-1989/extracted-vpxtool/script.vbs",
         "sha256": "ac708574ef0cdd488f1ff4c63da2888d622e609fcf88b818448fd03a214756de",
         "locator": "Embedded script, Windows-1252: switch handlers, solenoid callbacks and Lampz assignments; " + VPX_ACQUISITION,
         "acquired_at": VPX_ACQUIRED_AT,
         "original_filename": "script.vbs", "known_working": True,
         "attribution": "VPin Workshop: agenteightysix, iaakki, Flupper, Shannon, eMBee, Benji, Sixtoe, Apophis, Wylte, bord, tomate, cyberpez and contributors; original WIP Sliderpoint", "license": "NOASSERTION",
         "excerpts": [file_excerpt(root, "embedded-script-bindings", "embedded-script-bindings.md", "Embedded VPW v1.05 script: SolCallback and switch-handler regions, trough initialization, Lampz.MassAssign and GI") ]},
        {"id": VPM_LIBRARY_SOURCE, "kind": "vpx_script", "uri": VPM_LIBRARY_URI,
         "sha256": VPM_S11_SHA256, "license": "NOASSERTION", "attribution": "VPinMAME script-library contributors",
         "locator": f"Retained s11.vbs constants and vpmKeyDown/vpmKeyUp; retained core.vbs SHA-256 {VPM_CORE_SHA256}, cvpmFlips2 and game-on dispatch",
         "excerpts": [file_excerpt(root, "vpm-script-library-flippers", "vpm-script-library-flippers.md", "s11.vbs lines 22-40 and 69-130; core.vbs cvpmFlips2, vpmInit and output dispatch")]},
        {"id": CALLOUT_SOURCE, "kind": "human_review", "uri": "internal:" + CALLOUT_PATH.as_posix(),
         "sha256": hashlib.sha256((root / CALLOUT_PATH).read_bytes()).hexdigest(),
         "locator": "Independently read native factory drawing pixels, exact table controls, curator verification and excluded checks; drawing_callouts.py affine and leave-one-out evaluation",
         "attribution": "Independent pixel reader; primary curator visual verification"},
        {"id": PHOTO_SOURCE, "kind": "human_review", "uri": "https://www.ipdb.org/images/2630/image-23.jpg",
         "sha256": "c589fb8e79673a894ea551d80e70303d6ac4b5df56caac97387254613f4d2696", "source_id": "ipdb.2630.photo-55768",
         "original_filename": "image-23.jpg", "acquired_at": "2026-11-06T09:03:00Z", "license": "NOASSERTION",
         "attribution": "Oliver Paust, hosted by IPDB; retained original outside Git",
         "locator": "Verified Transporter machine 2630, https://www.ipdb.org/machine.cgi?id=2630; photograph page https://www.ipdb.org/showpic.pl?id=2630&picno=55768; six-socket playfield board, 1200x1805 original pixels; portable control/socket seed " + PHOTO_PATH.as_posix(),
         "excerpts": [file_excerpt(root, "photograph-sockets", "photograph-sockets.md", "IPDB photo 55768, six-socket board and six affine controls")]},
        {"id": EXTRACTION, "kind": "vpx_table",
         "uri": "external:pinmame-vpx-sources/bally/transporter-the-rescue-1989/extracted-vpxtool/manifest.json",
         "sha256": MANIFEST_SHA, "locator": "Official sorted full-file SHA-256 manifest, 2104 files, 196647547 bytes; " + VPX_ACQUISITION,
         "acquired_at": VPX_ACQUIRED_AT,
         "attribution": "vpxtool extraction", "license": "NOASSERTION"},
    ]


def file_excerpt(root: Path, identifier: str, filename: str, locator: str) -> dict:
    path = Path(f"evidence/excerpts/{ID}/{filename}")
    return {"id": f"excerpt.transporter.{identifier}", "path": path.as_posix(), "locator": locator,
            "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(), "method": "mixed",
            "transcribed_by": "Initial mechanical inventory and primary curator source verification", "reviewed": True}


def load_facts(root: Path = ROOT) -> dict:
    facts = load_json(root / FACTS)
    facts["objects"].update(load_json(root / SPATIAL_FACTS)["objects"])
    return facts


def spatial_review(definition: dict, root: Path = ROOT) -> dict:
    seed = load_json(root / CALLOUT_PATH)
    devices = {(x["binding"]["group"], x["binding"]["device"]): x
               for x in definition["inputs"] + definition["outputs"]}
    measurements = []
    for entry in seed["measurements"]:
        item = devices[entry["group"], entry["address"]]
        page = seed["pages"][entry["page"]]
        transform = drawing_callouts.fit([(tuple(c["pixel"]), tuple(c["xy"])) for c in page["controls"]])
        points = [drawing_callouts.apply(transform, pixel) for pixel in entry["pixels"]]
        item["spatial"] = {"status": "observed", "placements": [
            {"id": f"{item['id']}.{'sensor' if entry['group'].startswith('pinmame.input') else 'emitter'}.{i}",
             "role": "sensor" if entry["group"].startswith("pinmame.input") else "emitter",
             "space": "playfield", "x": round(x, 6), "y": round(y, 6),
             "provenance": prov(MANUAL, CALLOUT_SOURCE, VPX, status="observed")}
            for i, (x, y) in enumerate(points, 1)]}
        if entry["reason"] not in item["physical"]["notes"]:
            item["physical"]["notes"] += " " + entry["reason"]
        measurements.append({**entry, "normalized": [[round(x, 6), round(y, 6)] for x, y in points]})
    positions = {p["id"]: (p["x"], p["y"]) for item in devices.values()
                 for p in item.get("spatial", {}).get("placements", [])}
    result = drawing_callouts.evaluate(seed, positions)
    for item in definition["inputs"]:
        if item["binding"]["group"] != "pinmame.input.switch":
            continue
        table_object = SWITCH_OBJECTS.get(item["binding"]["device"])
        for placement in item.get("spatial", {}).get("placements", []):
            check = result["placements"].get(placement["id"])
            if not check or check["read"] is None:
                continue
            controls = seed["pages"][check["page"]]["controls"]
            independent = [c for c in controls if c["table_object"] != table_object]
            if len(independent) == len(controls):
                continue
            if len(independent) < 4:
                raise ValueError("independent placement check requires four other controls")
            transform = drawing_callouts.fit([(tuple(c["pixel"]), tuple(c["xy"])) for c in independent])
            offset = drawing_callouts.distance(drawing_callouts.apply(transform, check["pixel"]), positions[placement["id"]])
            check.update(control_object_excluded=table_object, control_count=len(independent),
                         independent_control_fit=transform, control_offset=round(offset, 4),
                         agrees=check["agrees"] and offset <= result["limit"])
    for item in devices.values():
        spatial = item.get("spatial", {})
        for p in spatial.get("placements", []):
            check = result["placements"].get(p["id"])
            if check:
                p["provenance"] = prov(VPX, SCRIPT, MANUAL, CALLOUT_SOURCE,
                                       status="validated" if check["agrees"] else "observed")
        if spatial.get("placements"):
            states = {p["provenance"]["status"] for p in spatial["placements"]}
            spatial["status"] = "validated" if states == {"validated"} else "candidate" if "candidate" in states else "observed"
    result["measurements"] = measurements
    photo = load_json(root / PHOTO_PATH)
    photo_fit = drawing_callouts.fit([(tuple(c["pixel"]), (c["table"][0] / WIDTH, c["table"][1] / HEIGHT)) for c in photo["controls"]])
    for observation in photo["candidate_socket_observations"]:
        item = devices["pinmame.output.lamp", observation["public_lamp"]]
        x, y = drawing_callouts.apply(photo_fit, observation["pixel"])
        item["spatial"] = {"status": "observed", "placements": [
            {"id": f"{item['id']}.emitter.1", "role": "emitter", "space": "playfield", "x": round(x, 4), "y": round(y, 4),
             "provenance": prov(PHOTO_SOURCE, MANUAL, SCRIPT, VPX, status="observed")}]}
        base_note = item["physical"]["notes"].split(" Candidate insert-effect anchors")[0].split(" Physical socket-base axis")[0]
        item["physical"]["notes"] = base_note + " Physical socket-base axis observed on the unique six-socket board in IPDB photo 55768, with manual/VPX topology identifying its lamp. Affine photo fit is approximate and remains observed."
    result["photo_sockets"] = {"seed": PHOTO_PATH.as_posix(), "seed_sha256": hashlib.sha256((root / PHOTO_PATH).read_bytes()).hexdigest(),
                               "observed_lamps": [x["public_lamp"] for x in photo["candidate_socket_observations"]],
                               "control_uncertainty_pixels": photo["control_uncertainty_pixels"], "rms_normalized": photo["rms_normalized"],
                               "transform": photo_fit, "limitations": photo["limitations"]}
    result["rule"] = drawing_callouts.RULE + " When a checked placement's own table object is also a control, that object is excluded and its control offset is recomputed from the other four controls; the independent fit and excluded object are recorded per placement."
    result["seed"] = CALLOUT_PATH.as_posix()
    result["seed_sha256"] = hashlib.sha256((root / CALLOUT_PATH).read_bytes()).hexdigest()
    return result


def switch_records(facts: dict) -> list[dict]:
    group = "pinmame.input.switch"
    cells = {c["printed_address"]: c for c in facts["switch_cells"]}
    cols = {int(r[0]): r for r in facts["switch_wiring"] if len(r) == 5 and r[0].isdigit()}
    rows = {int(r[0]): r for r in facts["switch_wiring"] if len(r) == 3 and r[0].isdigit()}
    parts = {int(r[0]): r for r in facts["switch_parts"] if r[0].isdigit()}
    result = []
    for n in range(1, 65):
        cell = cells[n]
        unused = n in UNUSED_SWITCH
        item_id = legacy_id(facts, "inputs", group, n, f"switch.matrix-{n}")
        if n == 2:
            item_id = "switch.ac-select-feedback"
        elif n in (57, 58):
            item_id = f"switch.{'right' if n == 57 else 'left'}-flipper-lane-change"
        label = cell["literal_label"] if not unused else f"Not Used (Matrix Position {n})"
        if n == 2:
            label = "A/C Select Relay Feedback"
        if n in (57, 58):
            label += " Lane Change Opto"
        item = {"id": item_id, "label": label, "kind": "virtual" if unused or n == 2 else "switch",
                "binding": {"group": group, "device": n},
                "aliases": aliases(facts, "inputs", group, n, f"{n:02d}"),
                "availability": "unused" if unused else ("optional" if n == 5 else "used"),
                "provenance": prov(MANUAL, CORE, SCRIPT, RUNTIME)}
        prior = next((x for x in facts["legacy"]["inputs"] if x["binding"] == item["binding"]), {})
        if prior.get("roles"):
            item["roles"] = prior["roles"]
        if n in (3, 4, 5, 6):
            item["roles"] = [{3: "cabinet.start", 4: "cabinet.coin.3", 5: "cabinet.coin.2", 6: "cabinet.coin.1"}[n]]
        col, row = cols[cell["column"]], rows[cell["row"]]
        item["wiring"] = {"board": "CPU board", "driver_transistor": col[1], "drive_wire": col[3],
                          "drive_connection": col[4], "return_wire": row[1], "return_connection": row[2]}
        note = f"Matrix column {cell['column']}, row {cell['row']}; manual label: {cell['literal_label']}."
        if n == 2:
            note += " PinMAME overwrites this virtual A/C relay feedback from output 12; the legacy alias s_ball_roll_tilt does not name a physical tilt."
        elif n in (57, 58):
            note += f" Backbox interconnect lane-change optotransistor; core_updateSw copies {'82' if n == 57 else '84'} here each update, so drive the flipper column instead."
            if n == 57:
                note += " The retained s11.vbs defines swTilt as 1; physical plumb tilt is matrix 1."
        elif n == 5:
            note += " Parts list says Not Used (USA); optional international center coin input."
        elif 19 <= n <= 24:
            note += " Drop-bank opto; normally open describes the comparator's matrix contact, not the beam."
        elif not unused:
            note += " System 11 reads the matrix uninverted with zero game inversion mask; script asserts active at 1."
        item["physical"] = {"notes": note}
        if not unused and n != 2:
            item["normally_closed"] = False
            item["physical"]["switch_type"] = "opto" if n in (*range(19, 25), 57, 58) else (
                "button" if n in (3, 4, 5, 6, 8) else "tilt" if n in (1, 7, 9) else "leaf")
            part = parts.get(n)
            if part and len(part) == 3 and part[2] not in ("[blank]", "Not Used (USA)"):
                item["physical"]["part_number"] = part[2].rstrip("*")
        if n in (63, 64):
            item["physical"]["quantity"] = 2
            item["physical"]["notes"] += " Two physically separate actuating switches share this matrix address (manual B-12459 and B-12715)."
        if n in (11, 12, 13):
            item["initial_active"] = True
        if unused or n == 2:
            item["spatial"] = na("unused" if unused else "virtual", MANUAL, CORE)
        elif n <= 9 or n in (57, 58):
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif n in SWITCH_OBJECTS and SWITCH_OBJECTS[n] in facts["objects"]:
            name = SWITCH_OBJECTS[n]
            item["spatial"] = located(item_id, "sensor", [name], facts)
            item["physical"]["notes"] += f" Observed VPX object {name}; walls use mean drag-point coordinates."
        result.append(item)
    for n, label in ((-7, "Advance"), (-6, "Up/Down"), (-5, "CPU Diagnostics"), (-4, "Sound Diagnostics")):
        item_id = legacy_id(facts, "inputs", group, n, f"switch.diagnostic-{abs(n)}")
        result.append({"id": item_id, "label": label, "kind": "switch", "binding": {"group": group, "device": n},
                       "aliases": aliases(facts, "inputs", group, n), "availability": "used",
                       "physical": {"location": "cabinet or service", "switch_type": "button"},
                       "spatial": na("cabinet_or_service", CORE), "provenance": prov(CORE)})
    flips = flipper_column_inputs(flip_swno=(58, 57), flip_swno_text="FLIP_SWNO(58,57)",
                                  core_refs=(CORE,), button_refs=(SCRIPT, VPM_LIBRARY_SOURCE),
                                  button_notes={"left": "The retained script drives this cabinet button.",
                                                "right": "This cabinet button drives both the lower-right and upper-right physical flippers while enabled. Manual PDF 40 braces both coil branches under Right Flipper: Orn-Vio at 1P19-1 feeds lower-right Blu-Vio and upper-right Blk-Yel (note 2: switch-to-coil). The retained script supplies separate lower/upper right callbacks through the flipper library; public output 34 remains unused."})
    for item in flips:
        n = item["binding"]["device"]
        if n == 82:
            item["label"] = "Right Flipper Button (Lower and Upper Right)"
            item["provenance"]["source_refs"].append(MANUAL)
        item["aliases"] = aliases(facts, "inputs", group, n)
        result.append(item)
    result.append({"id": "switch.dip-0", "label": "Country Jumper", "kind": "dip_switch",
                   "binding": {"group": "pinmame.input.dip", "device": 0}, "aliases": [],
                   "availability": "used", "physical": {"switch_type": "dip", "location": "CPU board in backbox",
                   "notes": "One Country configuration jumper (USA/Germany), not a multi-bank switch array; s11.c reads core_getDip(0)<<7 at PIA2 PA7 and s11.h declares MDRV_DIPS(1)."},
                   "spatial": na("dip_switch", CORE), "provenance": prov(CORE)})
    return result


def output_records(facts: dict) -> list[dict]:
    result = []
    group = "pinmame.output.solenoid"
    numbered = [r for r in facts["solenoid_rows"] if r[0][0].isdigit()]
    table = {}
    for row in numbered:
        printed = row[0].split("[")[0]
        n = int(printed[:2]) + (24 if printed.endswith("C") else 0)
        table[n] = row
    for n in range(1, 51):
        row = table.get(n)
        virtual = n == 23 or n in (24, *range(33, 51))
        unused = n == 13 or n in (24, *range(33, 45), 49, 50)
        item_id = legacy_id(facts, "outputs", group, n, f"device.solenoid-{n}")
        if n in (34, 36):
            item_id = f"device.unused-solenoid-{n}"
        label = row[1] if row else (f"Unused Solenoid {n}" if unused else
                                   "Game On" if n == 23 else f"Synthetic {'Right' if n < 47 else 'Left'} Flipper State {n}")
        kind = "virtual" if virtual or n == 13 else (
            "gi" if n in (9, 22) else "relay" if n == 12 else "flasher" if n in (11, 15, 16, *range(25, 33)) else "coil")
        printed = row[0].split("[")[0] if row else None
        item = {"id": item_id, "label": label, "kind": kind,
                "binding": {"group": group, "device": n}, "aliases": aliases(facts, "outputs", group, n, printed),
                "availability": "unused" if unused else "used", "provenance": prov(MANUAL, CORE, SCRIPT, RUNTIME)}
        notes = f"Manual Solenoid Table {printed}: {row[1]}; type {row[2]}; wire {row[3]}; CPU {row[4]}; playfield/cabinet {row[5]}; transistor {row[6]}; part {row[7]}; quantity {row[8]}." if row else ""
        if n in (34, 36):
            notes += " This address is dead; any legacy upper-flipper alias names a VPX local callback, not a PinMAME output."
        if n == 23:
            notes += " PinMAME game-on signal controls flipper enable and is meaningful virtual state."
        if n in range(45, 49):
            notes += " PinMAME synthesizes identical pairs 45/46 from right and 47/48 from left button while enabled; these are not measured winding or EOS states."
        if n == 9:
            notes += " Enabled output 9 turns the playfield GI off; de-energized output 9 turns it on (embedded SolGI). The table uses output 9 for both GI effects, simplifying factory wiring; 33 VPX bulb meshes are observed but physical count is unproved."
        if n in (27, 28):
            notes += " Manual prints two playfield flashlamps."
        if n in (11, 15, 16, 29, 31):
            notes += " Manual prints one playfield and one insert-board flashlamp; quantity includes both locations."
        if n == 6:
            notes += " The parts list prints AE-23-1200, whereas this table prints AE-26-1200."
        if n == 10:
            notes += " The parts list prints SM2-35-4001-DC, whereas this table prints SM2-35-4000-DC."
        if n == 22:
            notes += " The parts list prints 5580-09555-01 where this table prints 5530-09555-01; both identify the same insert-board GI relay. Its lamp-on/off polarity is unestablished: the retained script has no separate output 22 callback, and the manual identifies the relay coil without showing its GI load contacts. Do not infer polarity from output 9."
        item["physical"] = {"notes": notes or "Unpopulated public output address."}
        if row:
            item["wiring"] = {"board": "CPU and auxiliary power driver boards", "driver_transistor": row[6],
                              "drive_wire": row[3], "drive_connection": row[5]}
            if row[7] not in ("-", "[blank]") and kind == "coil":
                item["physical"]["part_number"] = row[7]
        if kind == "flasher":
            item["physical"]["quantity"] = 2 if n in (11, 15, 16, 27, 28, 29, 31) else 1
        if unused or virtual:
            item["spatial"] = na("unused" if unused else "virtual", CORE, MANUAL)
        elif n in (7, 12, 22):
            item["spatial"] = na("cabinet_or_service", MANUAL)
        elif n == 9:
            names = [x for x in facts["gi_collection"] if facts["objects"][x]["show_bulb_mesh"]]
            if len(names) != 33:
                raise ValueError("expected 33 observed GI bulb meshes")
            item["spatial"] = located(item_id, "emitter", names, facts)
        elif n in COIL_OBJECTS and COIL_OBJECTS[n] in facts["objects"]:
            name = COIL_OBJECTS[n]
            item["spatial"] = located(item_id, "effect", [name], facts)
            item["physical"]["notes"] += f" Projected onto its own mechanism at VPX object {name}, not a measured coil centre."
        elif n in (11, 15, 16, 26, 27, 28):
            names = {11: ["Flasherbase6"], 15: ["Flasherbase5"], 16: ["Turn3Flasher"],
                     26: ["BridgeFlasher"], 27: ["Flasherbase1", "Flasherbase2"],
                     28: ["Flasherbase3", "Flasherbase4"]}[n]
            item["spatial"] = located(item_id, "emitter", names, facts)
            item["physical"]["notes"] += " Playfield bulbs are placed on their own modelled dome axes or show_bulb_mesh Light centres; insert-board bulbs remain cabinet devices."
            if n == 27:
                item["physical"]["notes"] += " Rear-panel domes project to y=0: raw y=-6.3529983 and -6.4993663 VPU, factory drawing 03C on the rear rail and physical photographs."
        result.append(item)
    group = "pinmame.output.lamp"
    lamp_cols = {int(r[0]): r for r in facts["lamp_wiring"] if len(r) == 5 and r[0].isdigit()}
    lamp_rows = {int(r[0]): r for r in facts["lamp_wiring"] if len(r) == 4 and r[0].isdigit()}
    for cell in sorted(facts["lamp_cells"], key=lambda x: x["printed_address"]):
        n = cell["printed_address"]
        unused = n in (18, 56)
        item_id = legacy_id(facts, "outputs", group, n, f"lamp.matrix-{n}")
        item = {"id": item_id, "label": f"Not Used (Lamp {n})" if unused else cell["literal_label"].replace(" **", ""),
                "kind": "virtual" if unused else "lamp", "binding": {"group": group, "device": n},
                "aliases": aliases(facts, "outputs", group, n, str(n)),
                "availability": "unused" if unused else "used", "provenance": prov(MANUAL, CORE, SCRIPT),
                "physical": {"notes": f"Manual lamp matrix column {cell['column']}, row {cell['row']}; literal cell {cell['literal_label']}."}}
        col, row = lamp_cols[cell["column"]], lamp_rows[cell["row"]]
        item["wiring"] = {"board": "CPU board", "driver_transistor": col[1],
                          "drive_wire": col[3], "drive_connection": col[4],
                          "return_wire": row[2], "return_connection": row[3], "return_component": row[1]}
        if not unused:
            item["physical"]["quantity"] = 2 if n in (13, 14, 40, 55) else 1
        if unused:
            item["spatial"] = na("unused", MANUAL, CORE)
        elif n >= 41:
            item["spatial"] = na("cabinet_or_service", MANUAL)
        else:
            names = [f"L{n}"]
            if n in (13, 14):
                names.append(f"L{n}B")
            elif n == 40:
                names.append("L40a")
            item["spatial"] = located(item_id, "emitter", names, facts, status="candidate")
            item["physical"]["notes"] += " Candidate insert-effect anchors from script-bound Light art objects, not observations of physical socket centres. Flood/glow companions are excluded. Factory lamp symbols corroborate identity and order; they do not resolve the individual sockets of a multi-bulb insert."
        result.append(item)
    return result


def build(root: Path = ROOT) -> dict:
    facts = load_facts(root)
    inputs, outputs = switch_records(facts), output_records(facts)
    matrix = {x["binding"]["device"]: x["id"] for x in inputs if x["binding"]["group"] == "pinmame.input.switch"}
    coil = {x["binding"]["device"]: x["id"] for x in outputs if x["binding"]["group"] == "pinmame.output.solenoid"}
    drivers = facts["drivers"]
    for driver in drivers:
        driver["physical_compatibility"] = "identical"
        driver["variant_notes"] = "Uses the same pinned tsptr game data and physical controller and playfield hardware."
    displays = [{"id": f"display.{name}-alphanumeric", "label": f"Alphanumeric sixteen-character controller block {idx}",
                 "kind": "segment", "controller_index": idx, "segment_start": start, "width": 16, "height": 1,
                 "physical_location": "cabinet_or_service", "spatial": na("cabinet_or_service", MANUAL, CORE),
                 "provenance": prov(MANUAL, CORE)} for idx, start, name in ((0, 0, "upper"), (1, 20, "lower"))]
    mechanisms = []
    for name, kind, actuators, sensors, behavior in (
        ("trough", "kicker", [1, 2], [10, 11, 12, 13, 14], "Outhole and three-position ball trough feed the shooter lane."),
        ("left-drop-bank", "drop_target_bank", [3], [19, 20, 21], "Reset raises the left three drop targets; optos signal their matrix states."),
        ("middle-drop-bank", "drop_target_bank", [4], [22, 23, 24], "Reset raises the middle three drop targets; optos signal their matrix states."),
        ("left-lock", "kicker", [5], [33], "Left Orion lock holds and releases a ball."),
        ("right-lock", "kicker", [8], [34], "Right Orion lock holds and releases a ball."),
        ("ball-popper", "kicker", [6], [15], "Popper ejects a ball from the saucer."),
        ("top-flipper-gate", "gate", [10], [], "Controlled gate opens at the upper flipper."),
        ("left-outlane-kicker", "kicker", [14], [59], "Left outlane kicker returns the ball."),
        ("flippers", "other", [], [57, 58, 82, 84], "Two lower and one upper-right physical flippers are cabinet wired. The right cabinet button (input 82) drives both lower-right and upper-right flippers while enabled; the left button (84) drives the lower-left. Manual PDF 40 groups both right coil branches under the right switch. The VPX upper-right local callback 34 combines the key and game-on state; it is not a PinMAME output 34."),
        ("jet-bumpers", "other", [17, 19, 21], [60, 61, 62], "Three C-12872 thumper bumper assemblies pair left, right and bottom switches 60/61/62 with coils 17/19/21; the coil returns the ball after skirt actuation. The physical trigger circuit and the ROM coil test establish the pairing; the driver leaves ssSw empty, so no switch-driven coil simulation is implied."),
        ("slingshots", "other", [18, 20], [63, 64], "Each C-12873 slingshot has two physical leaf actuating switches sharing one matrix address (B-12459/B-12715). Left 63 and right 64 accompany special coils 18 and 20. Their switches release when the rubber returns; the VPX animation is implementation timing."),
        ("transport-ramp-path", "other", [], [17, 31], "Fixed ramp and crossover ball paths are sensed at Top of Ramp 17 and Transport 31. There is no independently driven transport motor in the factory inventory. The VPX speed-up helpers near 31 compensate its ball dynamics and publish no extra switch or mechanism mark."),
    ):
        mechanisms.append({"id": f"mechanism.{name}", "label": name.replace("-", " ").title(), "kind": kind,
                           "actuators": [coil[x] for x in actuators], "sensors": [matrix[x] for x in sensors],
                           "behavior": behavior, "provenance": prov(MANUAL, SCRIPT, CORE)})
    relationships = flipper_column_relationships(flip_swno=(58, 57), matrix_ids=matrix, refs=(CORE,))
    for relation in relationships:
        relation["provenance"]["status"] = "validated"
    definition = {
        "format": "pinmame-machine-definition", "schema_version": 2, "machine": facts["machine"],
        "controller": {"platform": "pinmame.system-11", "hardware_generation": "0x100", "inversion_applied_by_emulator": True},
        "coverage": {"status": "partial", "missing": ["polarity", "spatial_placement"],
                     "dimensions": {"catalog_identity": "validated", "address_enumeration": "validated",
                                    "semantic_naming": "validated", "physical_wiring": "observed", "display_inventory": "validated",
                                    "mechanisms": "validated", "recreation_knowledge": "observed", "polarity": "unknown",
                                    "variant_coverage": "validated", "spatial_placement": "observed"}},
        "drivers": drivers, "inputs": inputs, "outputs": outputs, "displays": displays,
        "mechanisms": mechanisms, "relationships": relationships, "sources": source_records(facts, root),
        "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "partial"}, "conflicts": [],
    }
    definition["machine"].update(kind="physical_pinball", model_number="2008",
                                 playfield={"width": WIDTH, "height": HEIGHT, "units": "vpx"})
    spatial_review(definition, root)
    return definition


def report(definition: dict, root: Path = ROOT) -> dict:
    definition = copy.deepcopy(definition)
    review = spatial_review(definition, root)
    entries = []
    for item in definition["inputs"] + definition["outputs"]:
        spatial = item.get("spatial", {})
        for p in spatial.get("placements", []):
            entries.append({"id": p["id"], "binding": item["binding"], "x": p["x"], "y": p["y"], "status": spatial["status"]})
    return {"format": "pinmame-spatial-blockers", "version": 1,
            "machine_id": ID, "status": "partial", "playfield_bounds": [0, 0, WIDTH, HEIGHT],
            "transform": "x / 952.965, y / 1976.52, rounded to six decimals",
            "source_manifest_sha256": MANIFEST_SHA, "extraction_file_count": 2104,
            "extraction_byte_count": 196647547, "placements": entries, "callout_check": review,
            "extractor": "vpxtool git:v0.33.3",
            "manifest_algorithm": "tools/build_external_evidence_manifest.py: all relative POSIX file paths sorted case-sensitively, byte size and SHA-256; excludes only manifest.json and manifest.sha256; UTF-8 sorted-key compact JSON plus LF, SHA-256 over those bytes",
            "source_hashes": {"table": "4cd27942999d39e6f1e23e6a2d65f24b61dc176f7eb5ede9c720a981c05718ff",
                              "embedded_script": "ac708574ef0cdd488f1ff4c63da2888d622e609fcf88b818448fd03a214756de",
                              "manual": "d1e29962c3bc53733ba61a62d8d814d2a1adbf508f78dfe10c01cd4fb95f2ce9"},
            "omitted": [x["id"] for x in definition["inputs"] + definition["outputs"] if "spatial" not in x],
            "blockers": ["Backbox GI output 22 lamp-on/off polarity is unestablished; the source identifies its relay coil but not its load contacts, and the retained script has no independent callback.",
                         "Factory GI socket quantity is not proved; the 33 table bulb meshes are observations only.",
                         "Apart from six physical socket observations at lamps 1 and 4-8, playfield matrix-lamp anchors remain candidate art-effect positions; multi-bulb inserts 13/14/40 especially need individual physical socket evidence.",
                         "Solenoid flashers 29, 30 and 31 have physical counts but no unambiguous bulb/socket centre in the retained model or location drawing; their spatial keys stay omitted.",
                         "Factory-drawing measurements and unconfirmed table placements remain observed; the report records each checked placement's own affine residual."]}


def knowledge_text() -> str:
    return """# Transporter the Rescue (Bally, 1989)

The 1989 Bally model 2008 is IPDB 2630. The six catalogued game drivers share the same physical controller data. The manual and the retained VPW v1.05 table are cited in the definition.

The manual's A/C relay selects the eight switched A loads (public 1–8) or C loads (25–32). The factory special solenoids 17–22 use the printed identities. The service test names and pulses 13 and 17–22; its sweep pulse on 13 does not imply a fitted load, and both the table and the circuit drawing say Not Used. Public 23 is game-on state, 45/46 and 47/48 are synthesized identical right and left pairs, not measured winding or EOS state.

## Ball path and mechanisms

The outhole kicker (01A) sends a drained ball into a three-position trough; switches 11–13 mark its right, middle and left positions, and the shooter-lane feeder (02A) releases the ball toward switch 14. Switch 10 detects the outhole. The VPX script creates three balls in its startup trough, moves them using the Drain and BallRelease kickers, and clears switch 11 when it fires the feeder. Its trough walls are simulation aids, not evidence of factory dimensions. A persistent occupied trough or outhole switch after a kick is a useful jam symptom; no measured jam timeout is established.

Two three-bank drop target assemblies have three optical receiver/comparator outputs each: left 19–21 (R-E-S) and middle 22–24 (C-U-E). The manual's C-12559 board drawing names the three optos and comparator output rows. Their matrix-side contacts are normally open under the System 11 read path, independently of the beam's rest state. A target hit is routed to its own switch; coil 03A raises the left bank and 04A the middle bank. In the retained table the hit handlers call DTHit for each target; the reset callbacks call DTRaise for all three. The script makes the corresponding shadow visible after reset. It does not prove the hardware's reset travel time or an optical jam timeout.

The left and right Orion lockups use switches 33 and 34 and coils 05A and 08A respectively. Each kick releases a locked ball; the VPX plunger fires and a timer pulls it back. The ball popper's switch 15 detects the saucer ball; 06A kicks it and the script clears switch 15. The manual's 06A table and parts-list coil numbers disagree, so both remain in the excerpts. SB11 records the revised locked-ball search order as right, left, right; it also changes the initial search from 30 to 15 seconds and the locked-ball search interval to 10 seconds. These factory rule timings are not measurements of physical motion.

The upper flipper gate is coil 10 and its VPX callback opens the gate while enabled, closing it when disabled. The left outlane kickback coil 14 returns a ball at switch 59; the script fires and then pulls back its plunger. Switch 31 is Transport, switch 17 is top of ramp, and switches 25–27 are the S-O-S top lanes. The VPX table gives switch 31 two collision helpers that alter ball velocity; those helpers are simulation behavior, not two additional sensors or evidence of the physical transport mechanism's timing. A ball repeatedly remaining in a lock, saucer, gate or outlane after its corresponding kick is a troubleshooting clue; exact hardware failure detection remains undocumented.

Three thumper bumpers use switch 60/61/62 and special coil 17/19/21 respectively. The paired slingshot actuating switches 63/64 correspond to special coils 18/20. Their table hit handlers pulse the switches. The machine has lower-left, lower-right and upper-right flippers, wired through cabinet switches rather than individually numbered CPU solenoid outputs; the two backbox lane-change optos are 57/58. The right cabinet button (input 82) drives both lower-right and upper-right flippers while enabled, and the left button (84) drives the lower-left. Manual PDF 40 groups the lower-right Blu-Vio and upper-right Blk-Yel coil branches under Right Flipper Orn-Vio at 1P19-1; note 2 identifies these as switch-to-coil connections. The manual lists one FL-11630/50VDC coil for each of the three flippers. The retained script supplies separate right callbacks through its flipper library; these records do not invent a separate public binding for the upper-right winding.

PinMAME copies flipper buttons 82 and 84 into lane-change optos 57 and 58; consumers must drive 82/84. The VPX local upper-right callback 34 is wrapped by cvpmFlips2 using the key and game-on state, not published solenoid 34. The retained s11.vbs defines swTilt as 1, the physical plumb tilt. Matrix switch 2 is virtual A/C feedback, not the legacy Ball Roll Tilt alias. Center coin 5 is optional outside the USA.

## Spatial evidence and remaining limits

The lamp matrix has blank cells 18 and 56, named NOT USED by the ROM's lamp test even though its sweep pulses them. Lamp numbers 107 and 109 in the VPX script are local fade indexes, not public lamp addresses. Manual solenoid parts tables disagree for 06A, 10 and the printed relay part at 22; the literal readings and device notes preserve these details. GI output 9 is physically playfield and 22 backbox; the table drives both effects from 9. In the embedded SolGI callback, enabled output 9 turns GI off and de-energized output 9 turns it on. Output 22's lamp-on/off polarity remains unestablished: the manual identifies its relay coil but omits its GI load contacts, and the script has no separate 22 callback. Its polarity must not be copied from 9. Thirty-three playfield table bulb meshes are observed, without inventing an authoritative total socket quantity from their grouping.

Fourteen switch positions agree with independently read factory part locations under both affine fits. For jet switches 60-62, each jet's own Bumper object is excluded from its control fit; the other four controls and the separate leave-one-out callout check still agree. The physical popper and each of the paired sling switches are measured on the factory drawing; the popper's table physics kicker is displaced from its physical drawing position. Six actual lamp socket-base axes (1 and 4-8) are observed in Oliver Paust's raised-playfield photograph, fitted through three flipper shafts and three under-jet ring centres. Camera perspective, component depth and approximate controls keep these measurements observed. The other insert-art anchors remain candidates because the lamp drawing marks insert regions rather than individual sockets; it draws one symbol for each of the two-bulb inserts 13/14/40. Backbox lamps and insert-board flashlamps have controlled cabinet spatial records.

The manual, exact table, eight retained IPDB photographs and all 63 Pinside gallery thumbnails were examined; the available playfield photos retain their plastics and the underside views are partly obscured by wiring. They cannot prove an exhaustive GI inventory or the remaining individual sockets. Flashers 29/30/31 have known presence and quantity but no unambiguous physical bulb centre in the model or factory drawing. These spatial requirements and the unestablished backbox GI output 22 polarity keep the machine partial. The generated spatial report lists the exact retained source hashes, projection classes, measurements and remaining candidate/omitted records; no physical-machine conflict is manufactured from a rendering omission.

Source roles: the factory manual and SB11/SB13 own physical inventory and factory changes; the exact embedded VPW v1.05 script and retained s11/core libraries own runtime behavior; pinned PinMAME owns controller transport and driver grouping; the factory location drawings, exact table and original IPDB photograph own the explicitly differentiated spatial observations. Printed wiring details are transcribed in the adjacent excerpts. Live-emulator evidence is retained as `evidence/runtime/system-11/transporter-l3-service.json` and `transporter-l3-single-lamps.json`; ROM bytes and original copyrighted sources stay outside Git.
"""


def report_text(data: dict) -> str:
    lines = ["# Transporter the Rescue spatial audit", "", "Status: partial; remaining coverage gaps are polarity and spatial placement.", "",
             f"Bounds: {data['playfield_bounds']}. {data['transform']}.",
             f"Extraction manifest SHA-256: `{MANIFEST_SHA}`.", "",
             "Table coordinates are centres or documented mean wall drag points. Fourteen switch placements are independently checked against their own factory callout; the report records both affine residuals. Each jet switch 60-62 excludes its own Bumper object from the control fit, using the other four controls; these per-placement fits and offsets are recorded alongside the separate leave-one-out callout check. Measured factory drawing points are observed, never checked against the same page. Coils project onto their own mechanism; matrix-lamp art anchors stay candidate. Rear-panel domes project explicitly to y=0 from raw negative y values.",
             "GI placements are show-bulb-mesh members of the retained GI collection; the table groups both factory circuits under output 9, so these do not prove physical socket count.",
             "", f"Recorded placements: {len(data['placements'])}.", "",
             "## Omitted spatial records", ""]
    lines += [f"- {x}" for x in data["omitted"]]
    lines += ["", "## Blockers", ""] + [f"- {x}" for x in data["blockers"]] + [""]
    lines += ["## Drawing reconciliation", "", data["callout_check"]["rule"], "",
              f"Checked {len(data['callout_check']['placements'])}; agreeing {sum(x['agrees'] for x in data['callout_check']['placements'].values())}.", "",
              "The factory lamp drawing marks insert regions rather than individual sockets. Six socket bases at lamps 1 and 4-8 are observed on the original raised-playfield photograph; their affine photo fit and uncertainty are in the JSON report. Other retained photographs include intact plastics or partial underside views and cannot prove exhaustive GI fitment or separate the two sockets behind inserts 13/14/40. These gaps remain spatial blockers, with no invented physical-machine conflict.", ""]
    return "\n".join(lines)


def artifacts(root: Path) -> dict[Path, bytes]:
    definition = build(root)
    data = report(definition, root)
    return {DEFINITION: canonical_bytes(definition), SEED: canonical_bytes(definition),
            REPORT: canonical_bytes(data), REPORT_MD: report_text(data).encode("utf-8"),
            KNOWLEDGE: knowledge_text().encode("utf-8")}


def verify_extraction(source_root: Path, root: Path = ROOT) -> None:
    extraction = source_root / EXTRACTION_PATH
    manifest = extraction / "manifest.json"
    expected = manifest_bytes(build_manifest(extraction, "tsptr_l3")) + b"\n"
    actual = manifest.read_bytes()
    if actual != expected or hashlib.sha256(actual).hexdigest() != MANIFEST_SHA:
        raise ValueError("retained extraction manifest or files differ from pinned evidence")
    if (extraction / "manifest.sha256").read_text(encoding="ascii").strip() != MANIFEST_SHA:
        raise ValueError("retained extraction digest file differs")
    for name, obj in load_facts(root)["objects"].items():
        value = next(iter(json.loads((extraction / "gameitems" / obj["file"]).read_text(encoding="utf-8")).values()))
        point = value.get("center") or value.get("position")
        if not point:
            points = value["drag_points"]
            point = {"x": sum(p["x"] for p in points) / len(points), "y": sum(p["y"] for p in points) / len(points)}
        if point["x"] != obj["x"] or point["y"] != obj["y"]:
            raise ValueError(f"retained coordinate drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    mode.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()
    if args.verify_extraction:
        configured = os.environ.get("PINMAME_VPX_SOURCES_ROOT")
        if not configured:
            raise ValueError("PINMAME_VPX_SOURCES_ROOT is required to verify retained extraction")
        verify_extraction(Path(configured))
        print("Extraction manifest, file hashes and pinned coordinates match.")
        return
    if (ROOT / AUTHOR).exists():
        raise ValueError("refusing to overwrite an author-ready definition")
    for path, content in artifacts(ROOT).items():
        target = ROOT / path
        if args.check:
            if not target.exists() or target.read_bytes() != content:
                raise ValueError(f"generated artifact drift: {path}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    print("Transporter artifacts match." if args.check else "Transporter artifacts regenerated.")


if __name__ == "__main__":
    main()
