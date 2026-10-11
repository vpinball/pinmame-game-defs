"""Deterministic, game-scoped spatial curation of Data East Star Wars (1992).

Spatial-only retrofit: adds a `spatial` record to every input and output of the partial
definition, three source records, coverage and the spatial report, from geometry pinned to one
retained VPW v1.2.2 extraction (star_wars_geometry.json, rebuilt by build_star_wars_geometry.py).
Object identity comes from the embedded script's own bindings; every device gets exactly one
disposition and an undecorated address raises. --check regenerates in memory and refuses all drift.
Every placement stays `observed`: one table is retained, nothing is cross-validated and no
drawing callout check exists, so the machine stays partial.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.star-wars.1992"
STEM = "data-east/star-wars-1992"
DEFINITION = ROOT / "machines" / "partial" / "data-east" / "star-wars-1992.json"
REPORT = ROOT / "reports" / "spatial" / "data-east" / "star-wars-1992.json"
TABLE = "vpx-table.star-wars-1992.vpw-1-2-2"
SCRIPT = "vpx-script.star-wars-1992.vpw-1-2-2"
MANUAL = "manual.star-wars-1992"
TABLE_SHA = "ea240a0193d6f3d829fdd0c416d18b8dbe733ce5ad4bbefcb4b17b481b9d11ca"
SCRIPT_SHA = "1d5252b9ef7d1d00646df732661a07b384d6d5cb14798ff86337a00de1c7d144"
MANUAL_SHA = "e2a5dedc7e9529a449151f8b9a7ec8d94eda3054dc1022d1e987e1124f9714d1"
EXTRACTION_MANIFEST = "5407b0aefce8e931e87a154e92ef4186497ecd011bc7ea4e41c085836e616059"
EXTRACTION_FILES, EXTRACTION_BYTES = 1343, 399048009
GEOMETRY = json.loads((ROOT / "tools" / "star_wars_geometry.json").read_text(encoding="utf-8"))
OBJECTS = GEOMETRY["objects"]
BIGUS = "vpx-table.star-wars-1992.bigus-3-0"
BIGUS_SCRIPT = "vpx-script.star-wars-1992.bigus-3-0"
BIGUS_TABLE_SHA = "5057ffe49defd5821c6c5be6b3f5823f9c7cc246572d87ef249c224bf81d832c"
BIGUS_SCRIPT_SHA = "8ca2f5fad6d7337114c61f2023478104d7999d653356fe6b9eb0d1ab35d48809"
BIGUS_EXTRACTION_MANIFEST = "459915810dd150943ff483b9b3343518d7fa80c9e06cc06ca2e2c401beb4b65b"
BIGUS_EXTRACTION_FILES, BIGUS_EXTRACTION_BYTES = 743, 95473255
AGREE = 0.025  # normalized units; the Lord-of-the-Rings multi-table rule
# Addresses in the Bigus conversion-kit region: the Bigus table physically models the kit, so
# these addresses are never validated on its word (disclosed, not merged).
KIT_EXCLUDED = {"switch.34", "switch.35", "switch.41", "switch.42", "coil.9", "coil.15"}
BIGUS_GEOMETRY = json.loads((ROOT / "tools" / "star_wars_bigus_geometry.json").read_text(encoding="utf-8"))
BIGUS_OBJECTS = BIGUS_GEOMETRY["objects"]

# Wall-mounted flash sprites whose drag-point centre lies outside the normalized playfield
# bounds (x < 0). The schema admits only 0..1 coordinates, so they are dropped, not clamped.
DROPPED_BULBS = {
    "f125d": "Flash 1R left-wall sprite centred at x=-8.9 VPU (outside the playfield edge).",
    "f132b": "Flash 8R left-wall sprite centred at x=-8.9 VPU (outside the playfield edge).",
    "f132c": "Flash 8R left-wall sprite centred at x=-8.9 VPU (outside the playfield edge).",
}

# Devices the retained table cannot locate: the disposition is controlled not_applicable,
# each with the script evidence that shows why.
INPUT_NOT_APPLICABLE = {
    1: ("cabinet_or_service", "Plumb-bob tilt on the cabinet; the script binds it via vpmNudge.TiltSwitch = 1 "
        "(script.vbs line 196) and no playfield object carries it. The Bigus 3.0 table binds tilt the same "
        "way (vpmNudge.TiltSwitch, its script.vbs 71)."),
    50: ("cabinet_or_service", "Ball-play launch button. No handler binds switch 50 anywhere in the retained "
        "script, and the table models no launch-button object, so no playfield coordinate can be asserted. "
        "The Bigus 3.0 table emulates the launch button through its shift lever (embedded header line 7) "
        "and has no switch 50 handler."),
    51: ("cabinet_or_service", "Magna-Save button at the coin door (manual switch table, printed p.50); "
        "cabinet hardware with no playfield object in the table. The Bigus 3.0 table has no Magna-Save "
        "handler."),
}
OUTPUT_NOT_APPLICABLE = {
    ("pinmame.output.solenoid", 11): ("internal_nonvisual", "The GI control relay is driven in software: "
        "SolCallback(11) calls SetGI (script.vbs lines 489, 556-566) and the GI bulbs are addressed through the "
        "lamp channel (Lampz.obj(111)), so the relay coil itself has no playfield placement. The Bigus 3.0 "
        "table drives its GI relay in software too (SolCallback(11) -> SetLamp 65, its script.vbs 364, 431)."),
    ("pinmame.output.lamp", 48): ("internal_nonvisual", "The table drives this lamp only through the "
        "JabbasInsert plastic callback (script.vbs line 1058); no Light object is assigned to address 48, "
        "so no bulb coordinate exists. The Bigus 3.0 table names l48 (its script.vbs 590) and contains no "
        "such object either."),
}
# Flash banks 5R (channel 129) and 7R (channel 131): the retained VPW table comments their bulb
# assignment out (lines 1141, 1151), so it models no bulb; the Bigus 3.0 table binds them. They get
# observed placements from the Bigus table alone, stated as such, and 7R's side is flagged for
# physical verification (the Bigus object sits on the left rail while the manual names the bank 7R).
BIGUS_FLASH_PLACEMENTS = {
    29: ("L29", "Flash bank 5R (Death Star): placed on the single flash bulb the Bigus 3.0 table binds to "
            "channel 129 (`FadeL 70, l29`, its script.vbs 531); the retained VPW table comments its bulb "
            "assignment out (script.vbs line 1141) and the manual names this bank."),
    31: ("L58", "Flash bank 7R (R2D2): placed on the single flash bulb the Bigus 3.0 table binds to "
            "channel 131 (`NFadeL 72, l58`, its script.vbs 535). The Bigus object sits on the left rail "
            "while the manual names the bank 7R: single-sourced and the side is flagged for physical "
            "verification; the retained VPW table comments its bulb assignment out (script.vbs line 1151)."),
}
# not_applicable dispositions the Bigus 3.0 table independently corroborates (cabinet devices carry
# no handler there; the GI relay is software-driven there too).
NA_CORROBORATED = {1, 50, 51, ("pinmame.output.solenoid", 11)}
PROJECTIONS = {
    "coil_effect": "A coil's effect projects onto the mechanism object its script binding acts on "
                   "(saucer kicker, plunger, bumper, slingshot wall, flipper), never a winding centre.",
    "flash_bank": "A flash bank is placed at every Light/Flasher object its lamp channel drives "
                   "(Lampz.MassAssign 125-132); banks 5R and 7R, commented out in the retained script, are "
                   "placed on the single bulb the Bigus 3.0 table binds to channels 129 and 131. A bank's "
                   "multi-table check compares the Bigus single emitter to the nearest retained bulb.",
    "lamp_bulb": "A lamp is placed at the Light/Flasher object Lampz.MassAssign binds, never the insert "
                 "plastics its DisableLighting callbacks light.",
    "sensor_object": "A switch is placed on the object its script handler binds (triggers, gates, kickers, "
                     "hit targets, bumpers); slingshots and drop targets on their wall's area centroid; the "
                     "four trough contacts on the trough Kicker the ball stack binds (InitExit BallRelease).",
    "mechanism_mesh": "The Death Star toy, its door bar and the R2D2 head are baked-mesh primitives; they are "
                      "located by the centre of their world-space mesh bounds in the vpxtool obj export, never "
                      "by a stored primitive position.",
}
MANUAL_CROSSCHECKS = [
    "PDF 4-5 (printed p.48-49) coil/flash-lamp wiring: every playfield coil's mechanism agrees with the "
    "table object its script binding drives (saucers, popper, VUKs, bumpers, slingshots, kickback, plunger).",
    "PDF 4-5 flash-lamp rows 1R-8R: banks 1R-4R, 6R and 8R place at their script-driven bulbs; 5R and 7R are "
    "modelled by the factory, commented out in the retained VPW table and placed from the Bigus 3.0 table's "
    "channel-129/131 bindings (recorded, single-sourced).",
    "PDF 6 (printed p.50) switch table: all 39 switch addresses reconcile with the script-bound objects; "
    "switch 50 (launch button) and 51 (Magna-Save/coin door) have no table object.",
    "PDF 7 (printed p.51) lamp wiring and GI table: lamp addresses 1-64 with the table's MassAssign map; the "
    "GI channel places at the 17 playfield GI bulbs of the table's GI collection.",
]
BLOCKERS = [{
    "dimension": "spatial_placement",
    "reason": "Two independent factory-layout tables are retained (VPW v1.2.2 and the Bigus 3.0 "
              "mod, JPSalas lineage). Their raw per-bounds normalizations differ by a frame "
              "artifact; on the pinned frame fit (mechanism controls, lamps/flashers held out) "
              "they agree, and 92 addresses validate within 0.025. Not every placement is "
              "validated: the conversion-kit region (34/35, 41/42, coils 9/15) is excluded by "
              "construction, GI stays observed without quantity per the GI rule, lamp 58 and "
              "flash banks 26/27 disagree beyond 0.025 (Bigus-side readings disclosed, flagged "
              "for physical verification), flash bank 28 agrees at bank level with its emitter "
              "count disclosed, banks 29/31 are placed from the Bigus table alone, and "
              "switches 1/50/51 and lamp 48 have no playfield placement. The manual has no "
              "playfield location drawing, so no callout check exists.",
}]


def prov(*refs: str, status: str = "observed") -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def place(identifier: str, role: str, name: str, key: str | None = None) -> dict:
    obj = OBJECTS[name]
    validated = key is not None and key in VALIDATED
    refs = [TABLE, SCRIPT, MANUAL] + ([BIGUS, BIGUS_SCRIPT] if validated else [])
    return {"id": f"{identifier}.{role}-{name.lower()}", "role": role, "space": "playfield",
            "x": obj["xy"][0], "y": obj["xy"][1], "provenance": prov(*refs, status="validated" if validated else "observed")}


def spatial(identifier: str, role: str, names: tuple[str, ...], key: str | None = None) -> dict:
    placements = [place(identifier, role, name, key) for name in names]
    status = "validated" if placements and placements[0]["provenance"]["status"] == "validated" else "observed"
    return {"status": status, "placements": placements}


def names_of(mapping: dict, address: int) -> tuple[str, ...]:
    """Object names from the geometry file's 'Kind.Name' values."""
    value = mapping[str(address)]
    if isinstance(value, list):
        return tuple(v.split(".", 1)[1] for v in value)
    return (value.split(".", 1)[1],)


def supplement_distances() -> dict[str, float]:
    """Per-address distance between the two pinned geometries, each normalized to its own table's
    bounds (the Lord-of-the-Rings precedent: per-table normalized coordinates are comparable),
    and the same distances after applying the pinned frame fit from the Bigus geometry. Flash
    banks compare the Bigus emitter to the nearest retained placement."""
    def nm(s: str) -> str:
        return s.split(".", 1)[1] if "." in s else s

    affine = BIGUS_GEOMETRY["frame"]["affine"]

    def fit(xy: list[float]) -> list[float]:
        return [affine[0] * xy[0] + affine[1] * xy[1] + affine[2],
                affine[3] * xy[0] + affine[4] * xy[1] + affine[5]]

    def dist(a: list[float], b: list[float]) -> float:
        return round(math.dist(a, b), 4)

    raw: dict[str, float] = {}
    fitted: dict[str, float] = {}
    for section, kind in (("switches", "switch"), ("coils", "coil")):
        for address, obj in BIGUS_GEOMETRY[section].items():
            primary = GEOMETRY[section].get(address)
            if primary is None:
                continue
            raw[f"{kind}.{address}"] = dist(BIGUS_OBJECTS[nm(obj)]["xy"], GEOMETRY["objects"][nm(primary)]["xy"])
            fitted[f"{kind}.{address}"] = dist(fit(BIGUS_OBJECTS[nm(obj)]["xy"]), GEOMETRY["objects"][nm(primary)]["xy"])
    for address, names in BIGUS_GEOMETRY["lamps"].items():
        primary = GEOMETRY["lamps"].get(address)
        if primary is None:
            continue
        raw[f"lamp.{address}"] = dist(BIGUS_OBJECTS[names[0]]["xy"], GEOMETRY["objects"][nm(primary[0])]["xy"])
        fitted[f"lamp.{address}"] = dist(fit(BIGUS_OBJECTS[names[0]]["xy"]), GEOMETRY["objects"][nm(primary[0])]["xy"])
    for address, names in BIGUS_GEOMETRY["flashers"].items():
        primary = GEOMETRY["flashers"].get(address)
        if primary is None:
            continue
        raw[f"flasher.{address}"] = min(dist(BIGUS_OBJECTS[names[0]]["xy"], GEOMETRY["objects"][obj]["xy"]) for obj in primary)
        fitted[f"flasher.{address}"] = min(dist(fit(BIGUS_OBJECTS[names[0]]["xy"]), GEOMETRY["objects"][obj]["xy"]) for obj in primary)
    return {"raw": dict(sorted(raw.items())), "fitted": dict(sorted(fitted.items()))}


def validated_addresses() -> set[str]:
    """Addresses the multi-table rule validates: every retained factory-layout table agrees within
    0.025 in the shared (fitted) space, the Bigus object is its script's own binding, and the
    address is not in the conversion-kit region. The fit's own controls participate: they are
    script-bound mechanisms checked at their fit residual, exactly as the multi-table rule counts
    each table's script-bound object; lamps and flashers were held out of the fit."""
    fitted = supplement_distances()["fitted"]
    return {key for key, d in fitted.items() if d <= AGREE and key not in KIT_EXCLUDED}


VALIDATED = validated_addresses()


SUPPLEMENT_ANCESTRY = (
    "The Bigus 3.0 table is the JPSalas lineage, not a derivative of the retained VPW v1.2.2 table: "
    "its embedded header (script.vbs lines 1-8) states 'JPSalas Star Wars ... Mod permission granted by "
    "JPSalas' and 'Modders so far: Shoopity, Dark'; its embedded script sha256, its playfield image 'pf' "
    "(against the VPW 'Blank PF Mat' render) and its bounds 0,0,1024,2102 all differ. It is retained as "
    "a second factory-layout table, so per the multi-table rule a placement is validated only when every "
    "retained table agrees within 0.025 normalized; the raw per-bounds distances below do not "
    "agree broadly (independent playfield renders, and the Bigus table models the Bigus "
    "conversion kit), while on the pinned frame fit 92 addresses agree within 0.025 and "
    "validate; the rest stay observed. Every Bigus reading is recorded as a per-address "
    "supplement measurement, exactly as Lord of the Rings records its independent tables."
)

SUPPLEMENT_DISCLOSURES = [
    "Frame fit: raw per-bounds normalization is not comparable across tables (bounds include "
    "shooter lane and furniture); the pinned frame fit (mechanism objects only, lamps and flashers "
    "held out: 58 devices, median fitted distance 0.0083, 52/58 within 0.025) shows the two "
    "tables agree in physical space and the raw spread was a frame artifact. The fit maps "
    "Bigus-normalized onto VPW-normalized coordinates; placement coordinates stay in the "
    "retained VPW space (a corroborating fit does not move the table's coordinate).",
    "Conversion-kit region: switches 34/35, the door bar 41/42 and toy coils 9/15 are never "
    "validated on the Bigus table — it physically models the Bigus kit there.",
    "Lamp 58: the Bigus script binds address 58 to its l58 object, which sits on the left rail, "
    "and drives flash channel 131 on that same object: the raw and fitted distances (0.53+) keep "
    "this device observed and flag it for physical verification.",
    "Flash banks 26, 27, 28: the Bigus table models one emitter per bank while the retained "
    "table places every bulb; fitted distance to the nearest retained placement is above 0.025 "
    "for 26/27 (0.11/0.04), so they stay observed. Bank 28's fitted 0.021 measures bank centres, "
    "not each bulb: its placement validates as the bank's position, its emitter-count divergence "
    "is disclosed here, and no quantity is claimed.",
    "GI: the Bigus GI collection holds 16 bulb Lights against the VPW table's 17; per the GI rule "
    "(a table's GI grouping is not the machine's wiring) GI stays observed without quantity and "
    "the counts are recorded, not paired.",
]


def apply_spatial(inputs: list[dict], outputs: list[dict]) -> list[str]:
    """Give every device exactly one spatial disposition; fail closed on an undecorated address."""
    notes: list[str] = []
    for device in inputs:
        address = int(device["binding"]["device"])
        if str(address) in GEOMETRY["switches"]:
            device["spatial"] = spatial(device["id"], "sensor", names_of(GEOMETRY["switches"], address),
                                        f"switch.{address}")
        elif address in INPUT_NOT_APPLICABLE:
            reason, note = INPUT_NOT_APPLICABLE[address]
            refs = [SCRIPT, MANUAL] + ([BIGUS_SCRIPT] if address in NA_CORROBORATED else [])
            device["spatial"] = {"status": "not_applicable", "reason": reason,
                                 "provenance": prov(*refs)}
            notes.append(f"input {address}: {note}")
        else:
            raise ValueError(f"Star Wars input {address} has no reviewed spatial disposition")

    lamps = {n: tuple(names) for n, names in GEOMETRY["lamps"].items()}
    flashers = {n: tuple(names) for n, names in GEOMETRY["flashers"].items()}
    for device in outputs:
        group = str(device["binding"]["group"])
        address = int(device["binding"]["device"])
        key = (group, address)
        if key in OUTPUT_NOT_APPLICABLE:
            reason, note = OUTPUT_NOT_APPLICABLE[key]
            refs = [SCRIPT, MANUAL] + ([BIGUS_SCRIPT] if key in NA_CORROBORATED else [])
            device["spatial"] = {"status": "not_applicable", "reason": reason,
                                 "provenance": prov(*refs)}
            notes.append(f"output {address}: {note}")
        elif group == "pinmame.output.solenoid" and str(device["kind"]) == "flasher" and address in BIGUS_FLASH_PLACEMENTS:
            name, note = BIGUS_FLASH_PLACEMENTS[address]
            obj = BIGUS_OBJECTS[name]
            device["spatial"] = {"status": "observed", "placements": [{
                "id": f"{device['id']}.emitter-{name.lower()}", "role": "emitter", "space": "playfield",
                "x": obj["xy"][0], "y": obj["xy"][1], "provenance": prov(BIGUS, BIGUS_SCRIPT, MANUAL)}]}
            device.setdefault("physical", {})["notes"] = note
            notes.append(f"output {address}: {note}")
        elif group == "pinmame.output.solenoid" and str(device["kind"]) == "flasher" and str(address) in flashers:
            placed = tuple(name for name in flashers[str(address)]
                           if name.lower() not in {n.lower() for n in DROPPED_BULBS})
            if not placed:
                raise ValueError(f"Star Wars flasher {address} has no in-bounds bulb")
            device["spatial"] = spatial(device["id"], "emitter", placed, f"flasher.{address}")
        elif group == "pinmame.output.solenoid" and str(address) in GEOMETRY["coils"]:
            device["spatial"] = spatial(device["id"], "effect", names_of(GEOMETRY["coils"], address),
                                        f"coil.{address}")
        elif group == "pinmame.output.lamp" and address == 111:
            device["spatial"] = spatial(device["id"], "emitter", tuple(GEOMETRY["gi"]))
            device.setdefault("physical", {})["notes"] = (
                "The GI channel drives the factory's playfield GI strings; the retained table models 17 "
                "playfield bulbs (its GI collection) and omits the backbox strings the manual lists. "
                "The Bigus table's GI collection has 16; GI stays observed without quantity per the GI rule.")
        elif group == "pinmame.output.lamp" and str(address) in lamps:
            device["spatial"] = spatial(device["id"], "emitter", lamps[str(address)], f"lamp.{address}")
        else:
            raise ValueError(f"Star Wars output {group} {address} ({device['kind']}) has no reviewed spatial disposition")
    return notes


def sources() -> list[dict]:
    return [
        {
            "attribution": "VPW crew (Dids666 render, Sixtoe, DJRobX, Jesperpark scanned playfield; "
                           "table credits Neo, Nfozzy, Flupper, Dark, Ninuzzu, Draifet, Alistaircg)",
            "id": TABLE,
            "kind": "vpx_table",
            "known_working": True,
            "license": "NOASSERTION",
            "locator": "complete vpxtool git:v0.37.1 extraction; gamedata.json bounds; gameitems per star_wars_geometry.json",
            "original_filename": "Star Wars (Data East 1992) VPW v1.2.2.vpx",
            "rights": "NOASSERTION",
            "sha256": TABLE_SHA,
            "uri": f"external:vpx-sources/{STEM}/tables/vpw-1.2.2-ea240a0193d6/Star Wars (Data East 1992) VPW v1.2.2.vpx",
        },
        {
            "attribution": "Dids666 & DJRobX; embedded header credits",
            "id": SCRIPT,
            "kind": "vpx_script",
            "known_working": True,
            "license": "NOASSERTION",
            "locator": "script.vbs lines 176-244,253-300,442-526,528-746,819-916,942-1160; embedded script, "
                       "not a corpus sidecar (the same-version corpus sidecar differs from the embedded script)",
            "rights": "NOASSERTION",
            "sha256": SCRIPT_SHA,
            "uri": f"external:vpx-sources/{STEM}/extractions/vpw-1.2.2-ea240a0193d6/script.vbs",
        },
        {
            "attribution": "Data East USA, Inc.",
            "id": MANUAL,
            "kind": "manual",
            "license": "NOASSERTION",
            "locator": "PDF 4-6 (printed p.48-50) coil, flash-lamp, special-coil and switch tables; "
                       "PDF 7 (printed p.51) lamp wiring and GI table",
            "original_filename": "starwars_schematics.pdf",
            "rights": "NOASSERTION",
            "sha256": MANUAL_SHA,
            "uri": f"external:manuals/by-machine/{KEY}/starwars_schematics.pdf",
        },
        {
            "attribution": "Bigus MOD 3.0: Shoopity and Dark on the JPSalas Star Wars table (embedded "
                           "header: 'Mod permission granted by JPSalas', 'Modders so far: Shoopity, Dark')",
            "id": BIGUS,
            "kind": "vpx_table",
            "known_working": True,
            "license": "NOASSERTION",
            "locator": "complete vpxtool git:v0.37.1 extraction; gamedata.json bounds; gameitems per "
                       "star_wars_bigus_geometry.json",
            "original_filename": "Star Wars (Data East 1992)_Bigus(MOD)3.0.vpx",
            "rights": "NOASSERTION",
            "sha256": BIGUS_TABLE_SHA,
            "uri": f"external:vpx-sources/{STEM}/tables/bigus-3.0-5057ffe49def/Star Wars (Data East 1992)_Bigus(MOD)3.0.vpx",
        },
        {
            "attribution": "JPSalas base script with Shoopity's and Dark's modifications; embedded header lines 1-8",
            "id": BIGUS_SCRIPT,
            "kind": "vpx_script",
            "known_working": True,
            "license": "NOASSERTION",
            "locator": "script.vbs lines 71,79-118,214-245,253-345,354-367,431,444-465,519-612; embedded script",
            "rights": "NOASSERTION",
            "sha256": BIGUS_SCRIPT_SHA,
            "uri": f"external:vpx-sources/{STEM}/extractions/bigus-3.0-5057ffe49def/script.vbs",
        },
    ]


def build() -> dict:
    definition = json.loads(DEFINITION.read_text(encoding="utf-8"))
    existing = {s["id"] for s in definition["sources"]}
    for source in sources():
        if source["id"] not in existing:
            definition["sources"].append(source)
    notes = apply_spatial(definition["inputs"], definition["outputs"])
    definition["coverage"]["dimensions"]["spatial_placement"] = "observed"
    missing = definition["coverage"].setdefault("missing", [])
    if "spatial_placement" not in missing:
        missing.append("spatial_placement")
    definition["_spatial_notes"] = notes  # report material, stripped before writing the definition
    return definition


def report(definition: dict) -> dict:
    geometry_objects = GEOMETRY["objects"]
    distances = supplement_distances()
    fitted = distances["fitted"]
    validated = validated_addresses()
    supplement = {
        "ancestry": SUPPLEMENT_ANCESTRY,
        "compare_rule": "raw: Euclidean distance between the positions the two pinned geometries "
                        "record for the same public address, each normalized to its own table's "
                        "bounds; fitted: the same after the pinned frame fit (Bigus-normalized onto "
                        "VPW-normalized). Flash banks compare the Bigus emitter to the nearest "
                        "retained placement. Distances rounded to 4 decimals. A device validates "
                        "when the fitted distance is within 0.025, outside the conversion-kit "
                        "region, and every retained table's object is its own script's binding.",
        "distances": dict(sorted(distances.items())),
        "disclosures": SUPPLEMENT_DISCLOSURES,
        "frame": BIGUS_GEOMETRY["frame"],
        "gi_bulb_counts": {"bigus-3-0": len(BIGUS_GEOMETRY["gi"]), "vpw-1-2-2": len(GEOMETRY["gi"])},
        "kit_excluded": sorted(KIT_EXCLUDED),
        "selected_extraction": {
            "algorithm": "Same canonical manifest algorithm as tools/build_external_evidence_manifest.py "
                         "records for the primary extraction.",
            "bytes": BIGUS_EXTRACTION_BYTES,
            "files": BIGUS_EXTRACTION_FILES,
            "manifest_sha256": BIGUS_EXTRACTION_MANIFEST,
            "root": f"external:vpx-sources/{STEM}/extractions/bigus-3.0-5057ffe49def",
        },
        "script_sha256": BIGUS_SCRIPT_SHA,
        "summary": {"agree_within_0_025_fitted": sum(1 for d in fitted.values() if d <= AGREE),
                    "compared": len(fitted),
                    "max_fitted_distance": max(fitted.values()),
                    "validated_addresses": len(validated)},
        "table_sha256": BIGUS_TABLE_SHA,
        "transform": "x=raw_x/1024; y=raw_y/2102; round to 6 decimals. Walls use the signed area centroid of "
                     "their drag points; kickers, triggers, gates, bumpers, flippers, plungers and Lights use "
                     "object centres; hit targets and the PrBar, PrDS and PrR2D2Head primitives use object "
                     "positions.",
        "unbound": BIGUS_GEOMETRY["unbound"],
    }
    return {
        "blockers": BLOCKERS,
        "bounds": GEOMETRY["bounds"],
        "coordinate_convention": "x=0 left, 1 right; y=0 rear, 1 front",
        "decision": "partial; independent cross-provider review belongs to the coordinator",
        "evidence_paths": {
            "manual": f"external:manuals/by-machine/{KEY}",
            "vpx": f"external:vpx-sources/{STEM}",
        },
        "format": "pinmame-spatial-blockers",
        "machine_id": KEY,
        "manual_crosschecks": MANUAL_CROSSCHECKS,
        "object_evidence": geometry_objects,
        "dropped_bulbs": DROPPED_BULBS,
        "partial_flash_banks": ["device.flasher-5r-death-star", "device.flasher-7r-r2d2"],
        "projections": PROJECTIONS,
        "supplement": supplement,
        "promotion": {"allowed": False,
                      "missing": sorted(definition["coverage"]["missing"])},
        "selected_extraction": {
            "algorithm": "Every relative POSIX path sorted case-sensitively with byte size and full-file "
                         "SHA256; canonical compact JSON (sorted keys, separators (',',':'), ensure_ascii "
                         "False) of {files:[{path,sha256,size}], format, game, version:1} plus one LF "
                         "(tools/build_external_evidence_manifest.py).",
            "bytes": EXTRACTION_BYTES,
            "files": EXTRACTION_FILES,
            "manifest_sha256": EXTRACTION_MANIFEST,
            "root": f"external:vpx-sources/{STEM}/extractions/vpw-1.2.2-ea240a0193d6",
        },
        "transform": "x=raw_x/946; y=raw_y/2162; round to 6 decimals. Slingshot walls, drop-target walls and "
                     "flasher sprites use the signed area centroid of their drag points; the baked-mesh Death "
                     "Star, door bar and R2 head use world-space mesh bounds from the vpxtool obj export.",
        "unplaced_records": [
            "switch.tilt", "switch.launch-button", "switch.right-magna-save-coin-door",
            "device.gi-relay", "lamp.scoop-right-jabba",
        ],
        "unresolved": {"notes": definition["_spatial_notes"]},
        "version": 1,
    }


def canonical(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    definition = build()
    notes = definition.pop("_spatial_notes")
    spatial_payload = canonical(definition)
    report_payload = canonical(report({**definition, "_spatial_notes": notes}))
    if args.check:
        if DEFINITION.read_bytes().replace(b"\r\n", b"\n") != spatial_payload:
            raise SystemExit("definition drift")
        if REPORT.read_bytes().replace(b"\r\n", b"\n") != report_payload:
            raise SystemExit("report drift")
        print("spatial matches")
    else:
        DEFINITION.write_bytes(spatial_payload)
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_bytes(report_payload)
        print(f"wrote {DEFINITION.relative_to(ROOT)} and {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
