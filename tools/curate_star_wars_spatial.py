"""Reproduce observed Star Wars positions from the retained VPW v1.2.2 table.

The full semantic curator supplies the inventory. Missing geometry never
establishes a cabinet location or a nonphysical device.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from drawing_callouts import apply, fit, leave_one_out

ROOT = Path(__file__).resolve().parents[1]
KEY = "data-east.star-wars.1992"
STEM = "data-east/star-wars-1992"
DEFINITION = ROOT / "machines/partial/data-east/star-wars-1992.json"
REPORT = ROOT / "reports/spatial/data-east/star-wars-1992.json"
TABLE = "vpx-table.star-wars-1992.vpw-1-2-2"
SCRIPT = "vpx-script.star-wars-1992.vpw-1-2-2"
TABLE_SHA = "ea240a0193d6f3d829fdd0c416d18b8dbe733ce5ad4bbefcb4b17b481b9d11ca"
SCRIPT_SHA = "1d5252b9ef7d1d00646df732661a07b384d6d5cb14798ff86337a00de1c7d144"
EXTRACTION = f"{STEM}/extractions/vpw-1.2.2-0561bb4"
OBJ = f"{STEM}/obj/vpw-1.2.2-0561bb4"
EXTRACTION_MANIFEST = "8552846c15834c567d4e0b479b06bd11309701a9443c2f5bc968ec0451f40f8b"
EXTRACTION_FILES, EXTRACTION_BYTES = 1343, 399048127
GEOMETRY = json.loads((ROOT / "tools/star_wars_geometry.json").read_text(encoding="utf-8"))
MANUAL = "manual.star-wars-1992.operators"
SCHEMATIC = "manual.star-wars-1992.schematics"
MANUAL_SHA = "dda489f3270e465dc285102a1d311d7538f58de9772542c78ba0fedc3c546ab0"
SCHEMATIC_SHA = "e2a5dedc7e9529a449151f8b9a7ec8d94eda3054dc1022d1e987e1124f9714d1"
EXCERPT_SHA = "0366955066ea26982c0d3b9301fec3a1681fb1c057b4615a321b5bd2dd178d16"
MANUAL_GEOMETRY = json.loads((ROOT / "tools/star_wars_manual_geometry.json").read_text(encoding="utf-8"))
UNPLACED_INPUTS = {}
UNPLACED_OUTPUTS = {
    **{("pinmame.output.lamp", n): "The factory and ROM identify this Death Star sphere lamp, but the retained geometry does not identify an individual physical socket." for n in (29, 30)},
    **{("pinmame.output.solenoid", n): (
        "The VPW bulb assignment is commented out (channels 129/131). The paired toy symbols are far outside the drawing controls and only support a coarse cross-check."
    ) for n in (29, 31)},
    ("pinmame.output.solenoid", 32): "The operator's drawing and VPW show four playfield candidates, but the schematic specifies three playfield bulbs and one insert-panel bulb. Physical count/location reconciliation remains unresolved, including the rear symbol outside the drawing controls.",
}
FLASH_LIGHTS = {25: ("f125a_u", "f125b_u", "f125c_u"), 26: ("f2r",),
                27: ("f3r_a", "f3r_b"), 28: ("f128d_l", "f4r_a", "f4r_b", "f4r_c")}


def drawing_fit(page: dict) -> tuple:
    pairs = [(pixel, GEOMETRY["objects"][name]["xy"]) for name, pixel in page["controls"].items()]
    if len(pairs) < 4 or max(xy[1] for _, xy in pairs) - min(xy[1] for _, xy in pairs) < 0.5:
        raise ValueError("drawing controls need redundancy and playfield span")
    if max(leave_one_out(pairs)) > 0.07:
        raise ValueError("drawing controls disagree")
    return fit(pairs), pairs


def drawn_spatial(identifier: str, page: dict, pixels: list) -> dict:
    transform, _ = drawing_fit(page)
    placements = []
    for index, pixel in enumerate(pixels, 1):
        x, y = (round(v, 3) for v in apply(transform, pixel))
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise ValueError("drawing point outside playfield")
        placements.append({"id": f"{identifier}.emitter-manual-{index}", "role": "emitter",
                           "space": "playfield", "x": x, "y": y,
                           "provenance": {"status": "observed", "source_refs": [MANUAL, TABLE, SCRIPT]}})
    return {"status": "observed", "placements": placements}


def not_applicable(reason: str, refs: list[str]) -> dict:
    return {"status": "not_applicable", "reason": reason,
            "provenance": {"status": "observed", "source_refs": refs}}


def canonical(payload: dict) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def names_of(mapping: dict, address: int) -> tuple[str, ...]:
    value = mapping[str(address)]
    return tuple(v.split(".", 1)[-1] for v in (value if isinstance(value, list) else [value]))


def lamp_names(address: int) -> tuple[str, ...]:
    names = names_of(GEOMETRY["lamps"], address)
    # These three banks use a local Light plus an elevated, larger glow helper.
    # SPATIAL.md: prefer a bulb mesh, then the smallest falloff radius.
    if address in (49, 50, 51):
        return (min(names, key=lambda n: (not GEOMETRY["objects"][n]["light"]["show_bulb_mesh"],
                                        GEOMETRY["objects"][n]["light"]["falloff_radius"])),)
    return names


def spatial(identifier: str, role: str, names: tuple[str, ...]) -> dict:
    placements = []
    for name in names:
        obj = GEOMETRY["objects"][name]
        if obj["type"] == "Flasher":
            raise ValueError(f"render sprite is not a physical placement: {name}")
        if role == "emitter" and (obj.get("light", {}).get("is_image_mode") or
                                  not obj.get("light", {}).get("is_bulb_light")):
            raise ValueError(f"render helper is not a physical bulb: {name}")
        x, y = obj["xy"]
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise ValueError(f"out-of-bounds placement: {name}")
        placements.append({"id": f"{identifier}.{role}-{name.lower()}", "role": role,
                           "space": "playfield", "x": x, "y": y,
                           "provenance": {"status": "observed", "source_refs": [TABLE, SCRIPT]}})
    return {"status": "observed", "placements": placements}


def sources() -> list[dict]:
    common = {"license": "NOASSERTION", "rights": "NOASSERTION", "known_working": True}
    excerpt = {"method": "manual", "path": f"evidence/excerpts/{KEY}/manual-spatial.md",
               "sha256": EXCERPT_SHA, "reviewed": True,
               "transcribed_by": "integration curator; visually checked native-resolution renders, OCR retained as navigation aid"}
    manual_excerpts = []
    for key, xref in (("lamp_page", 105), ("flash_page", 110)):
        page = MANUAL_GEOMETRY[key]
        w, h = page["image_size"]
        crop = ",".join(str(v) for v in page["crop_box"])
        manual_excerpts.append({**excerpt, "id": f"excerpt.star-wars-1992.{key.replace('_', '-')}",
            "locator": f"printed p.{page['printed_page']} / PDF {page['pdf_page']}; cabinet p.30 / PDF 32 and shifter p.42 / PDF 44",
            "image": page["image"], "image_sha256": page["image_sha256"],
            "image_derivation": f"Star_Wars_DE_OPS.pdf page {page['pdf_page']}, crop box {crop}, scanned page rendered at its native resolution (embedded image xref {xref}, 1681px across 8.40in), rendered at 200 dpi, grayscale, {w}x{h} WebP quality 80"})
    return [
        {"id": MANUAL, "kind": "manual", "license": "NOASSERTION", "rights": "NOASSERTION",
         "attribution": "Data East Pinball, Inc., 1992", "sha256": MANUAL_SHA,
         "original_filename": "Star_Wars_DE_OPS.pdf", "excerpts": manual_excerpts,
         "uri": f"external:manuals/by-machine/{KEY}/Star_Wars_DE_OPS.pdf",
         "locator": "Operator's manual, printed pp.27-28,30,42 / PDF 29-30,32,44; downloaded 2026-10-22 from https://www.bmigaming.com/Games/Manuals/pinball-machines/Star_Wars_DE_OPS.pdf"},
        {"id": SCHEMATIC, "kind": "manual", "license": "NOASSERTION", "rights": "NOASSERTION",
         "attribution": "Data East Pinball, Inc., 1992", "sha256": SCHEMATIC_SHA,
         "original_filename": "starwars_schematics.pdf",
         "uri": f"external:manuals/by-machine/{KEY}/starwars_schematics.pdf",
         "locator": "printed pp.48,50 / PDF 4,6; downloaded 2026-10-22 from https://www.maypin.eu/pinsdata/starwars_schematics.pdf",
         "excerpts": [{**excerpt, "id": "excerpt.star-wars-1992.schematics", "locator": "printed pp.48,50 / PDF 4,6; complete flash branch annotations and switch parts chart"}]},
        {**common, "id": TABLE, "kind": "vpx_table", "sha256": TABLE_SHA,
         "attribution": "VPW crew: Dids666, Sixtoe, DJRobX, Jesperpark; embedded table credits",
         "original_filename": "Star Wars (Data East 1992) VPW v1.2.2.vpx",
         "uri": f"external:vpx-sources/{STEM}/tables/vpw-1.2.2-ea240a0193d6/Star Wars (Data East 1992) VPW v1.2.2.vpx",
         "locator": "vpxtool git:0561bb4 extraction and OBJ export, retained 2026-10-22; gamedata.json and gameitems per tools/star_wars_geometry.json; mesh export under " + OBJ},
        {**common, "id": SCRIPT, "kind": "vpx_script", "sha256": SCRIPT_SHA,
         "attribution": "Dids666 and DJRobX; embedded header credits",
         "uri": f"external:vpx-sources/{EXTRACTION}/script.vbs",
         "locator": "Embedded script, lines 176-244,253-300,442-566,819-916,967-1185; acquired 2026-10-22 with vpxtool git:0561bb4"},
    ]


def build(definition: dict | None = None) -> dict:
    if definition is None:
        from curate_star_wars import build as full_definition
        return full_definition()
    if definition["coverage"]["status"] == "author_ready":
        raise ValueError("refusing to overwrite an author-ready definition")
    retired = {TABLE, SCRIPT, MANUAL, SCHEMATIC, "manual.star-wars-1992", "vpx-table.star-wars-1992.bigus-3-0",
               "vpx-script.star-wars-1992.bigus-3-0"}
    definition["sources"] = [s for s in definition["sources"] if s["id"] not in retired] + sources()
    for device in definition["inputs"]:
        address = device["binding"]["device"]
        if device.get("spatial", {}).get("status") == "not_applicable":
            continue
        device.pop("spatial", None)
        if address in (1, 50, 51):
            device["spatial"] = not_applicable("cabinet_or_service", [MANUAL, SCHEMATIC])
            if address in (50, 51):
                device["label"] = "Shift Button" if address == 50 else "Shift Down"
                device["provenance"] = {"status": "observed", "source_refs": [SCHEMATIC, SCRIPT]}
            continue
        device["spatial"] = spatial(device["id"], "sensor", names_of(GEOMETRY["switches"], address))
        if address == 10:
            device["label"] = "Outhole"
            device["provenance"] = {"status": "observed", "source_refs": [SCHEMATIC, SCRIPT]}
            device["spatial"]["placements"][0]["provenance"]["source_refs"].append(SCHEMATIC)
    for device in definition["outputs"]:
        group, address = device["binding"]["group"], device["binding"]["device"]
        if device.get("spatial", {}).get("status") == "not_applicable":
            continue
        device.pop("spatial", None)
        # Remove the notes introduced by the retired second-table retrofit.
        if address == 111 or (group == "pinmame.output.solenoid" and address in (29, 31)):
            physical = device.get("physical", {})
            physical.pop("notes", None)
            if not physical:
                device.pop("physical", None)
        if (group, address) in UNPLACED_OUTPUTS:
            continue
        if group == "pinmame.output.solenoid":
            if address == 11:
                device["spatial"] = spatial(device["id"], "emitter", tuple(GEOMETRY["gi"]))
            elif address == 30:
                page = MANUAL_GEOMETRY["flash_page"]
                device["spatial"] = drawn_spatial(device["id"], page, page["flashers"]["30"])
            elif address in FLASH_LIGHTS:
                device["spatial"] = spatial(device["id"], "emitter", FLASH_LIGHTS[address])
                for placement in device["spatial"]["placements"]:
                    placement["provenance"]["source_refs"].append(MANUAL)
            else:
                device["spatial"] = spatial(device["id"], "effect", names_of(GEOMETRY["coils"], address))
                if address == 1:
                    device["label"] = "Outhole"
                    device["provenance"] = {"status": "observed", "source_refs": [SCHEMATIC, SCRIPT]}
                    device["spatial"]["placements"][0]["provenance"]["source_refs"].append(SCHEMATIC)
        elif group == "pinmame.output.lamp":
            page = MANUAL_GEOMETRY["lamp_page"]
            if str(address) in page["lamps"]:
                device["spatial"] = drawn_spatial(device["id"], page, [page["lamps"][str(address)]])
            else:
                names = tuple(GEOMETRY["gi"]) if address == 111 else lamp_names(address)
                device["spatial"] = spatial(device["id"], "emitter", names)
        else:
            raise ValueError(f"unreviewed output group: {group}")
    definition["coverage"]["dimensions"]["spatial_placement"] = "observed"
    missing = definition["coverage"].setdefault("missing", [])
    for requirement in ("spatial_placement", "unresolved_conflicts"):
        if requirement not in missing:
            missing.append(requirement)
    conflict_id = "conflict.star-wars-flash-bank-counts"
    definition["conflicts"] = [c for c in definition.get("conflicts", []) if c["id"] != conflict_id] + [{
        "id": conflict_id, "path": "outputs[id=device.flasher-4r-upper-playfield]; outputs[id=device.flasher-6r]; outputs[id=device.flasher-8r-back-left-wall]",
        "status": "unresolved", "source_refs": [MANUAL, SCHEMATIC, TABLE],
        "description": "The schematic's 4R and 6R location annotations imply four bulbs but print '(3) NO. 89'. Its 8R annotation specifies three playfield bulbs and one insert-panel bulb, while the operator's location drawing and VPW have four playfield candidates. No complete bank quantity is asserted; 8R remains unplaced. Resolution path: a machine owner photographs and counts the populated sockets and wiring on banks 4R, 6R and 8R, or a curator obtains a later factory schematic revision that reconciles the counts."}]
    return definition


def report(definition: dict) -> dict:
    unplaced = {}
    for section in ("inputs", "outputs"):
        for device in definition[section]:
            if "spatial" not in device:
                binding = device["binding"]
                key = binding["device"] if section == "inputs" else (binding["group"], binding["device"])
                reasons = UNPLACED_INPUTS if section == "inputs" else UNPLACED_OUTPUTS
                unplaced[device["id"]] = reasons[key]
    return {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": KEY,
        "decision": "partial; retained VPW table and factory drawings, all coordinates observed",
        "bounds": GEOMETRY["bounds"], "coordinate_convention": "x=0 left, 1 right; y=0 rear, 1 front",
        "blockers": [{"dimension": "spatial_placement", "reason":
            "All positions remain observed. The retained operator's manual supplies missing lamp and 6R positions and cabinet identification. Three flash banks and two sphere lamps remain unplaced; non-playfield emitter quantities and factory GI socket membership are not validated."}],
        "promotion": {"allowed": False, "missing": sorted(definition["coverage"]["missing"])},
        "selected_extraction": {"root": f"external:vpx-sources/{EXTRACTION}",
            "tool": "vpxtool git:0561bb4", "acquired_at": "2026-10-22",
            "algorithm": "tools/build_external_evidence_manifest.py, game=stwr_106; case-sensitive POSIX paths, full-file hashes and sizes; canonical JSON plus LF",
            "manifest_sha256": EXTRACTION_MANIFEST, "files": EXTRACTION_FILES, "bytes": EXTRACTION_BYTES},
        "obj_export": f"external:vpx-sources/{OBJ}",
        "object_evidence": GEOMETRY["objects"],
        "manual_measurements": MANUAL_GEOMETRY,
        "manual_fits": {key: {"transform": drawing_fit(MANUAL_GEOMETRY[key])[0],
            "control_loo_max": max(leave_one_out(drawing_fit(MANUAL_GEOMETRY[key])[1])),
            "status": "observed; independently read controls, not validation against the coordinate source",
            "extrapolated": "Points beyond the bumper/flipper control extent remain observed; distant rear toy and 8R symbols are cross-checks only and are not published as coordinates."}
            for key in ("lamp_page", "flash_page")},
        "transform": "x=raw_x/946; y=raw_y/2162; six decimals. Walls use polygon-area centroids. Baked meshes use world-space OBJ bounds (x, y); coordinates were unchanged by re-extraction with git:0561bb4.",
        "projections": {
            "shared_rotation_drive": "Solenoid 15's observed anchor is the Death Star; its second R2D2 motor is documented in the combined mechanism but lacks a separately verified motor/effect position.",
            "coil_effect": "Mechanism effect anchor from the script binding, not the winding centre.",
            "outhole": "Switch 10 and solenoid 1 use Drain: the manual names the separate outhole, and the script's SolIn effect and trough-entry event use Drain. The virtual trough's four-switch array is not four physical trough contacts.",
            "trough": "Switches 11-13 share BallRelease from the scripted trough; projected assembly anchor, not three measured contacts. Solenoid 2 uses the ball-release effect anchor.",
            "door_sensors": "Switches 41/42 share the DSDoor mesh anchor; projected mechanism location, not measured sensor hardware.",
            "gi": "The 17 Lights in the GI collection are observed only. The table's grouping does not establish factory wiring or quantity.",
            "flashers": "1R uses the three upper Lights, dropping lower co-located glows; 2R uses the smallest local falloff Light f2r; 3R uses f3r_a/b; 4R uses f128d_l and f4r_a/b/c. The manual supports these playfield regions, not full bank quantities. 6R uses the two drawing symbols. Back-panel and insert-panel bulbs are not playfield placements. Printed 4R and 6R totals disagree with their location annotations."},
        "unplaced_records": unplaced,
        "discarded_candidates": "Flash-bank sprites, non-bulb/image-mode lamps and lamp 24's Flasher remain in the inventory but are not placements. The manual replaces those lamp helpers and locates lamp 48. Lamps 49-51 each retain the smaller 30-unit-falloff Light; the 100-unit-falloff companions at halo height 220 are render doubles, not additional bulbs.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    definition = build()
    for path, payload in ((DEFINITION, definition), (REPORT, report(definition))):
        data = canonical(payload)
        if args.check:
            if path.read_bytes().replace(b"\r\n", b"\n") != data:
                raise SystemExit(f"drift: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print("Star Wars spatial definition and report match" if args.check else "Wrote Star Wars spatial definition and report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
