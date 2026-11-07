"""Generate the evidence-bounded X-Men Pro definition without touching the LE.

The portable seeds contain exact coordinate fields and visually read diagnostic
frames. External verification replays the bounded reader and checks the retained
manual, ROM traces and their frames. A partial is intentional while sockets remain
unproved; changing a coverage flag cannot promote this contribution.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
for directory in (ROOT / "src", TOOLS):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from curate_xmen import build_pro, pro_gamedata_evidence, CORE_SOURCE, MANUAL_HIRES_SOURCE, PRO_VPX_TABLE_SOURCE, PRO_VPX_SOURCE
from pinmame_game_defs.conflicts import unresolved_conflicts
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_json, write_text
from xmen_pro_vpt_geometry import RAW_MANIFEST_SHA256, SCRIPT_SHA256, SOURCE_SHA256, FIGURE_PNG_SHA256, figure_image, recover
import drawing_callouts
import xmen_pro_drawing_geometry as drawings

MACHINE_ID = "stern.x-men-pro.2012"
MANUAL_SOURCE = "manual.x-men-pro.redundor.2012"
RUNTIME_SOURCE = "diagnostic.x-men-pro-151.20261106"
GEOMETRY_SOURCE = "geometry.x-men-pro-vpt-biff.20261106"
GI_SOURCE = "review.x-men-pro-gi-partial.20261106"
MAGNETO_SOURCE = "review.x-men-pro-magneto-hardware.20261106"
TROUGH_SOURCE = "review.x-men-pro-trough-contact-projection.20261106"
SPOTLIGHT_SOURCE = "review.x-men-pro-local-spotlight.20261106"
CABINET_SOURCE = "manufacturer.x-men-pro.cabinet.2012"
BOARD_SOURCE = "manufacturer.sam-520-5249.schematic"
BOARD_COMPATIBILITY_SOURCE = "manufacturer.sam.service-bulletin-178"
BOARD_SHA256 = "c09621893c439a966d2c48436b482fdf6326bc99ed5acd45a5634d5ae39c3219"
BOARD_COMPATIBILITY_SHA256 = "9eb0e9f6eaa277a1c4f005d575b3015720f31df0fe083760bfe1b44c152cecf9"
BOARD_PINS = dict(enumerate(
    [f"J8-P{pin}" for pin in (1, 3, 4, 5, 6, 7, 8, 9)]
    + [f"J9-P{pin}" for pin in (1, 2, 4, 5, 6, 7, 8, 9)]
    + [f"J7-P{pin}" for pin in (2, 3, 4, 6, 7, 8, 9, 10)]
    + [f"J6-P{pin}" for pin in range(1, 9)], 1))
COIL_WIRING_RELATIVE = "tools/seeds/stern/x-men-pro-2012-coil-wiring.json"
CABINET_CROP_SHA256 = "f14e9fea00fad5459709177507e81ac5574b20e55b8cc1fdbc5dbf94467eef23"
MANUAL_SHA256 = "d6ae672cf65299ff60e108a6b039275dd2393619b6c9e930c681cd285f635fbe"
MANUAL_RELATIVE = "by-machine/stern.x-men-pro.2012/pinside-redundor-2015/Stern_2012_X-Men_Pro.pdf"
VPX_RELATIVE = "stern/x-men-pro-2012"
REVIEW_RELATIVE = "stern/x-men-pro-2012/session-20261106"
SEED_RELATIVE = "tools/seeds/stern/x-men-pro-2012-vpt-geometry.json"
RUNTIME_RELATIVE = "tools/seeds/stern/x-men-pro-2012-service-readings.json"
NOTE_RELATIVE = "tools/seeds/stern/x-men-pro-2012-knowledge.md"
MANUAL_EXCERPT_DIR = "evidence/excerpts/stern.x-men-pro.2012"

# The Pro's own matrix, PDF 19 / printed 17. Blank functions are not completed
# from the LE matrix or from the names of render objects.
LAMP_NAMES = {
    1: "Start button", 2: "Tournament start button", 3: "Shoot Again", 4: "Left Special",
    5: "Left return lane", 6: "Right return lane 1", 7: "Right return lane 2", 8: "Right Special",
    9: "Left two-bank bottom", 10: "Left two-bank top", 11: "Left ramp entrance", 12: "Dark Phoenix",
    13: "Extra Ball", 14: "Danger Room", 15: "Villain", 16: "Gambit", 17: "Beast", 18: "Left orbit red",
    19: "Storm", 20: "Left ramp red", 21: "Left inner loop red", 22: "Rogue", 23: "Left inner loop green",
    24: "VUK red", 25: "Xavier", 28: "Center targets left", 29: "Center targets right", 30: "Wolverine red",
    31: "Wolverine", 33: "Center Magneto red", 34: "Magneto", 35: "Center Magneto green",
    36: "Right inner loop red", 37: "Cyclops", 38: "Right ramp entrance", 43: "Right ramp red",
    44: "Iceman", 45: "Right orbit red", 46: "Phoenix", 47: "Right orbit green", 48: "Right two-bank top",
    49: "Right two-bank bottom", 50: "Iceman character ring", 51: "Wolverine character ring",
    52: "Xavier character ring", 53: "Storm character ring", 54: "Phoenix character ring",
    55: "Cyclops character ring", 56: "Beast character ring", 57: "Rogue character ring",
    59: "Left eject top", 60: "Left pop bumper", 61: "Right pop bumper", 62: "Bottom pop bumper",
    65: "Sabretooth", 66: "Shadow King", 67: "Hellfire Club", 68: "Juggernaut", 69: "Brotherhood",
    70: "Sentinels", 71: "Omega Red",
}
COIL_LABELS = {
    17: "Left-side flashers", 18: "Right-side flashers", 21: "Wolverine insert flasher",
    22: "Magneto left and right flashers", 25: "Pop bumper flasher", 27: "Magneto spotlight",
    28: "Backpanel left flashers", 29: "Backpanel right flashers", 31: "Magneto figure flasher",
}
FLASHER_QUANTITIES = {17: 2, 18: 2, 21: 1, 22: 2, 25: 1, 27: 1, 28: 3, 29: 3, 31: 1}
FLASHER_IDS = {
    17: "flasher.left-side", 18: "flasher.right-side", 21: "device.wolverine-flasher",
    22: "flasher.magneto-left-right", 25: "device.pop-bumper-flasher", 27: "flasher.magneto-spotlight",
    28: "flasher.backpanel-left", 29: "flasher.backpanel-right", 31: "flasher.magneto-figure",
}
INPUT_OBJECTS = {
    1: "sw1", 2: "sw2", 4: "sw4", 7: "sw7", 8: "sw8", 11: "sw11", 13: "sw13", 14: "sw14",
    23: "sw23", 24: "sw24", 25: "sw25", 26: "LeftSlingShot", 27: "RightSlingShot", 28: "sw28",
    29: "sw29", 30: "Bumper2b", 31: "Bumper1b", 32: "Bumper3b", 33: "sw33", 36: "sw36",
    38: "sw38", 39: "sw39", 40: "sw40", 41: "sw41", 42: "sw42", 47: "sw47", 48: "sw48",
    49: "sw49", 52: "sw52", 53: "sw53", 54: "sw54", 55: "sw55a",
    81: "RightFlipper", 83: "LeftFlipper",
}
COIL_OBJECTS = {
    1: "BallRelease", 2: "sw23", 3: "sw4", 4: "Magnet3", 5: "sw55a", 6: "sw53", 7: "sw53",
    9: "Bumper2b", 10: "Bumper1b", 11: "Bumper3b", 12: "RightFlipper1", 13: "LeftSlingShot",
    14: "RightSlingShot", 15: "LeftFlipper", 16: "RightFlipper", 26: "RampDiverter", 32: "Magnet1",
}
RENDER_NAMES = {"f117", "f117b", "f118", "f118b", "f121", "f122", "f125", "f127", "f128", "f128a", "f128b", "f129", "f129a", "f131", "f59b"}
GEOMETRY_NAMES = set(INPUT_OBJECTS.values()) | set(COIL_OBJECTS.values()) | RENDER_NAMES | {"wr3"} | {
    f"l{number}{suffix}" for number in LAMP_NAMES if number not in {1, 2, 59} for suffix in ("", "a")
}


def provenance(status: str, *refs: str) -> dict:
    return {"status": status, "source_refs": list(dict.fromkeys(refs))}


def not_applicable(device: dict, reason: str, *refs: str) -> None:
    device["spatial"] = {"status": "not_applicable", "reason": reason, "provenance": provenance("validated", *refs)}


def object_position(row: dict) -> tuple[float, float]:
    if row["type"] in {"Flasher", "Primitive", "Decal", "Ramp"}:
        raise ValueError("a sprite, primitive origin, decal or unreviewed Ramp is not a physical anchor")
    if "center" in row:
        return tuple(row["center"])
    points = row.get("drag_points", [])
    if row["type"] != "Surface" or not points:
        raise ValueError(f"no supported anchor for {row.get('name')}")
    return tuple(sum(point[axis] for point in points) / len(points) for axis in (0, 1))


def figure_base_position(row: dict) -> tuple[float, float]:
    """The reviewed figure's bottom endpoint, never a generic Ramp centroid."""
    expected = {"HTBT":50.0, "HTTP":370.0, "WDBT":280.0, "WDTP":280.0,
                "CLDR":0, "RVIS":1, "IMAG":"magneto"}
    if (row.get("name") != "wr3" or row.get("type") != "Ramp"
            or row.get("stream") != "GameStg/GameItem1566"
            or row.get("sha256") != "e4c990ac48e7cdf55f8165f6aeedda9deae3ef0b992d15ecb60b20ba1bdca046"
            or row.get("reviewed_figure_fields") != expected
            or row.get("drag_points") != [[522.0,489.0],[522.5,435.0]]):
        raise ValueError("unreviewed figure billboard geometry")
    return tuple(row["drag_points"][0])


def observed_location(device: dict, role: str, row: dict, note: str) -> None:
    x, y = object_position(row)
    nx, ny = x / 959, y / 2162
    if not 0 <= nx <= 1 or not 0 <= ny <= 1:
        raise ValueError(f"out-of-range anchor {row['name']}")
    device["spatial"] = {"status": "observed", "placements": [{
        "id": f"{device['id']}.{role}", "role": role, "space": "playfield", "x": round(nx, 6), "y": round(ny, 6),
        "provenance": provenance("observed", GEOMETRY_SOURCE, PRO_VPX_TABLE_SOURCE, MANUAL_SOURCE),
    }]}
    device.setdefault("physical", {})["notes"] = note + f" Exact VPT {row['type']}.{row['name']} ({row['stream']}), raw ({x!r}, {y!r}); table-derived coordinate. Final spatial provenance records any subsequent independent factory-drawing reconciliation."


def excerpt(root: Path, name: str, locator: str) -> dict:
    path = f"{MANUAL_EXCERPT_DIR}/{name}.md"
    result = {"id": f"excerpt.x-men-pro.{name}", "locator": locator, "path": path, "sha256": file_sha256(root / path),
              "method": "manual", "transcribed_by": "Curator native-resolution visual inspection", "reviewed": True}
    if name.endswith("-locations"):
        image = load_json(root / drawings.SEED)["pages"][name.removeprefix("pro-").removesuffix("-locations")]["excerpt"]
        if file_sha256(root / image["image"]) != image["image_sha256"]:
            raise ValueError("committed Pro drawing excerpt drift")
        result.update(image)
        result.update(method="mixed", transcribed_by="Independent native-pixel readers; curator source-overlay verification and corrections")
    elif name == "pro-gi-partial":
        image = "evidence/excerpts/stern.x-men-pro.2012/pro-factory-backpanel.webp"
        if file_sha256(root/image) != load_json(root/drawings.SEED)["rear_photo_excerpt"]["image_sha256"]:
            raise ValueError("committed Pro rear-photo excerpt drift")
        result.update(image=image, image_sha256=file_sha256(root/image), image_derivation="Native 1120 x 520 crop (550, 1310, 1670, 1830) of Michael Minn 4320 x 3240 factory photograph; no resizing or assumed DPI. Pillow 12.3.0 grayscale WebP quality 80 method 6 via tools/xmen_pro_drawing_geometry.py.")
    elif name == "pro-spotlight-photo":
        image=load_json(root/drawings.SEED)["local_photo_measurements"]["flasher.magneto-spotlight.emitter"]["excerpt"]
        if file_sha256(root/image["image"]) != image["image_sha256"]:
            raise ValueError("committed local spotlight photo drift")
        result.update(image)
    elif name == "pro-cabinet-fitment":
        image = MANUAL_EXCERPT_DIR + "/pro-cabinet-buttons.webp"
        if file_sha256(root/image) != CABINET_CROP_SHA256:
            raise ValueError("manufacturer cabinet crop drift")
        result.update(image=image, image_sha256=CABINET_CROP_SHA256,
                      image_derivation="Manufacturer Pro flyer PDF page 1 embedded xref 8 JPEG 1275x1650 SHA-256 0334a7f5b3e041273d4499fa92f15bd866ef04da3097425ced4d4dc237b720b2; native crop (420, 1000, 650, 1380), 230x380, no resize. Pillow 12.3.0 converts the input to luminance, then saves lossy WebP quality 80 method 6; the retained file decodes as RGB. Original source color shows green Start; the compact crop retains the button and lower plug geometry, without preserving every source pixel value.")
    return result


def verify_external(root: Path) -> None:
    """Configured evidence roots are strict; an unset root permits portable checks."""
    if value := os.environ.get("PINMAME_VPX_SOURCES_ROOT"):
        game_root = Path(value) / VPX_RELATIVE
        if file_sha256(game_root / "source/XMen FS (physmod5)/XMen FS  (physmod5).vpt") != SOURCE_SHA256:
            raise ValueError("wrong original Pro VPT")
        recovered = recover(game_root / "extraction/7zip-22.01-20261106")
        figure_image(game_root / "extraction/7zip-22.01-20261106")
        recovered["extracted_item_count"] = len(recovered["items"])
        recovered["items"] = [row for row in recovered["items"] if row.get("name") in GEOMETRY_NAMES]
        if recovered != load_json(root / SEED_RELATIVE):
            raise ValueError("portable geometry seed differs from retained raw streams")
    if value := os.environ.get("PINMAME_MANUALS_ROOT"):
        if file_sha256(Path(value) / MANUAL_RELATIVE) != MANUAL_SHA256:
            raise ValueError("wrong original Pro manual")
        for name, digest in (("Batman_TDK_Manual.pdf", BOARD_SHA256), ("sb178.pdf", BOARD_COMPATIBILITY_SHA256)):
            if file_sha256(Path(value) / "by-machine/stern.x-men-pro.2012/stern-sam-board" / name) != digest:
                raise ValueError("wrong retained SAM board source")
    drawing_callouts.verify_retained(
        load_json(root / drawings.SEED), root,
        Path(os.environ["PINMAME_MANUALS_ROOT"]) if os.environ.get("PINMAME_MANUALS_ROOT") else None,
        Path(os.environ["PINMAME_REVIEW_ARTIFACTS_ROOT"]) if os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT") else None,
    )
    if value := os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"):
        session = Path(value) / REVIEW_RELATIVE
        drawing_seed = load_json(root/drawings.SEED)
        for measurement in drawing_seed.get("local_photo_measurements",{}).values():
            if file_sha256(Path(value)/measurement["image"]["path"]) != measurement["image"]["sha256"]:
                raise ValueError("local Pro photo drift")
        trough_photo=drawing_seed["rejected_trough_contact_projection"]["source_photo"]
        if file_sha256(session/trough_photo["path"]) != trough_photo["sha256"]:
            raise ValueError("actual trough component photograph drift")
        readings = load_json(root / RUNTIME_RELATIVE)
        wiring = load_json(root / COIL_WIRING_RELATIVE)
        if wiring["runtime_seed_sha256"] != file_sha256(root / RUNTIME_RELATIVE):
            raise ValueError("coil wiring audit uses a different diagnostic seed")
        coil_frames = {r["address"]: r for r in readings["runs"]["coil"]["readings"]}
        if {r["address"] for r in wiring["readings"]} != set(coil_frames):
            raise ValueError("coil wiring audit is incomplete")
        for row in wiring["readings"]:
            frame = coil_frames[row["address"]]
            if any(row[key] != frame[key] for key in ("artifact", "artifact_sha256", "pixel_sha256")):
                raise ValueError("coil wiring audit frame drift")
        for kind, bundle in readings["checkpoint_repeats"].items():
            path = session / bundle["path"]
            if file_sha256(path) != bundle["sha256"] or file_sha256(root / bundle["scenario"]) != bundle["scenario_sha256"]:
                raise ValueError(f"{kind}: checkpoint proof drift")
            run = load_json(path)
            matched = [step["matched_text"] for step in run["steps"] if step["type"] == "pulse_until_display"]
            if run["failure"] or run["game"] != "xmn_151" or run["library_sha256"] != readings["library_sha256"] or len(run["steps"]) != bundle["steps"] or len(run["snapshots"]) != bundle["snapshots"] or matched != bundle["checkpoints"]:
                raise ValueError(f"{kind}: failed or wrong checkpoint repeat")
        for kind, bundle in readings["runs"].items():
            path = session / bundle["path"]
            if file_sha256(path) != bundle["sha256"]:
                raise ValueError(f"{kind}: retained ROM trace drift")
            run = load_json(path)
            if run["failure"] or run["game"] != "xmn_151" or run["library_sha256"] != readings["library_sha256"]:
                raise ValueError(f"{kind}: wrong or failed ROM run")
            snapshots = {row["label"]: row for row in run["snapshots"]}
            steps = {row["label"]: row for row in run["steps"]}
            for record in bundle["readings"]:
                snapshot = snapshots[record["snapshot_label"]]
                display = snapshot["displays"][0]
                if display["pixel_sha256"] != record["pixel_sha256"]:
                    raise ValueError(f"{kind}: frame drift")
                if file_sha256(session / record["artifact"]) != record["artifact_sha256"]:
                    raise ValueError(f"{kind}: retained frame drift")
                # Compare callbacks to the displayed device, not selector ordinals.
                key = "lamps" if kind == "lamp" else "solenoids"
                transitions = steps[record["snapshot_label"]]["transitions"][key]
                seen = {row["number"] for row in transitions if any(row["states"])}
                if record["address"] not in seen and record["address"] != 24:
                    raise ValueError(f"{kind}: displayed address has no corresponding output transition")


def build(root: Path = ROOT) -> tuple[dict, dict]:
    seed = load_json(root / SEED_RELATIVE)
    if seed["source_sha256"] != SOURCE_SHA256 or seed["raw_manifest_sha256"] != RAW_MANIFEST_SHA256 or seed["script_sha256"] != SCRIPT_SHA256:
        raise ValueError("incorrect portable coordinate provenance")
    objects = {row["name"]: row for row in seed["items"]}
    wiring_audit = load_json(root / COIL_WIRING_RELATIVE)
    runtime = load_json(root / RUNTIME_RELATIVE)
    frames = {row["address"]: row for row in runtime["runs"]["coil"]["readings"]}
    if wiring_audit["runtime_seed_sha256"] != file_sha256(root / RUNTIME_RELATIVE) or len(wiring_audit["readings"]) != len(frames) or {row["address"] for row in wiring_audit["readings"]} != set(frames):
        raise ValueError("incomplete or unpinned coil wiring audit")
    for row in wiring_audit["readings"]:
        if any(row[key] != frames[row["address"]][key] for key in ("artifact", "artifact_sha256", "pixel_sha256")):
            raise ValueError("coil wiring audit is not tied to the retained frame")
    lamp_bindings = {row["address"]: row["objects"] for row in seed["script_fade_l_bindings"]}
    if set(objects) != GEOMETRY_NAMES or len(objects) != len(seed["items"]) or seed["extracted_item_count"] != 1702:
        raise ValueError("incomplete or ambiguous coordinate seed")
    # The legacy seed builder shares a few nested physical dictionaries.
    definition = copy.deepcopy(build_pro())
    definition["schema_version"] = 2
    definition["machine"]["playfield"] = {"width": 959, "height": 2162, "units": "vpx", "provenance": provenance("validated", GEOMETRY_SOURCE)}
    # Only this historical ambiguity is resolved by the new Pro matrix, firmware
    # and physical drawing. An unrelated upstream conflict must survive to the
    # unresolved-conflict gate below.
    definition["conflicts"] = [
        conflict for conflict in definition["conflicts"]
        if not (
            conflict["id"] == "conflict.pro-lamp-59-script-versus-physical-inventory"
            and conflict["path"] == "outputs[pinmame.output.lamp:59]"
        )
    ]
    definition["coverage"]["missing"] = ["output_semantics", "spatial_placement"]
    definition["coverage"]["dimensions"]["semantic_naming"] = "unknown"
    definition["coverage"]["dimensions"]["physical_wiring"] = "unknown"
    definition["coverage"]["dimensions"]["spatial_placement"] = "observed"
    for device in definition["inputs"]:
        address = device["binding"]["device"]
        if device["binding"]["group"] == "pinmame.input.dip":
            not_applicable(device, "dip_switch", MANUAL_HIRES_SOURCE)
        elif device["availability"] == "unused":
            not_applicable(device, "unused", MANUAL_HIRES_SOURCE)
        elif address in INPUT_OBJECTS:
            note = "Controller binding follows the working VPT event handler."
            if address in {81, 83}:
                note = "EOS contact projected onto its own lower-flipper pivot; the exact contact position is not modelled."
            elif address == 55:
                note = "Physical capture VUK sw55a; the separate sw55 ejection helper is ball-routing geometry, not the socket."
            observed_location(device, "sensor", objects[INPUT_OBJECTS[address]], note)
        elif address in {21, 22}:
            observed_location(device, "sensor", objects["BallRelease"], "Vertically stacked exit-opto beam projected onto its own trough exit/eject assembly. The common cut-away identifies 21 below 22 on the same receiver/transmitter boards, and the Pro drawing places 18-22 on this trough. Shared x/y represents the same beam stack in plan. The three microswitches 18-20 remain unplaced: the former photo points were wiring hardware, not actuators.")
            device["spatial"]["placements"][0]["provenance"]["source_refs"].append(MANUAL_HIRES_SOURCE)
        elif address not in {18, 19, 20}:
            not_applicable(device, "cabinet_or_service", MANUAL_HIRES_SOURCE)
        if address == 21 and device["binding"]["group"] == "pinmame.input.switch":
            device["physical"].update(switch_type="opto", assembly_part_number="500-6318-24-ND")
        if address == 15 and device["binding"]["group"] == "pinmame.input.switch":
            device["availability"] = "optional"
            device["physical"]["notes"] = "Optional tournament-start button contact. The manufacturer's Pro cabinet photograph shows a black plug below the fitted green Start button; a named firmware/manual function does not prove that this optional button is fitted. Existing identity, wiring and public switch 15 are preserved."
            device["provenance"]["source_refs"].append(CABINET_SOURCE)
            not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, CABINET_SOURCE)
    for device in definition["outputs"]:
        group, address = device["binding"]["group"], device["binding"]["device"]
        if group == "pinmame.output.gi":
            device["physical"]["notes"] = "Active-high master illumination state. Individually supported physical bodies and own-assembly projections form the explicit partial census in the Pro spatial seed/report. Whole fitted quantity and the disposition of two remaining under-plastic candidates are not proven; no total quantity or factory LED-conversion colors are claimed."
            continue
        if group == "pinmame.output.lamp":
            if address in LAMP_NAMES:
                device["label"] = LAMP_NAMES[address]
                device["availability"] = "optional" if address == 2 else "used"
                device["provenance"] = provenance("validated", MANUAL_SOURCE, RUNTIME_SOURCE, PRO_VPX_TABLE_SOURCE)
                device["physical"] = {"quantity": 1, "notes": "Function follows the Pro matrix and Pro ROM Single Lamp Test; physical fitment follows the Pro chart, with optional cabinet fitment distinguished below. Artwork names are descriptive, not different devices."}
                row, col = divmod(address - 1, 8)
                device["wiring"] = {"board": "I/O Power Driver board lamp matrix", "drive_wire": ["YEL-BRN", "YEL-RED", "YEL-ORG", "YEL-BLK", "YEL-GRN", "YEL-BLU", "YEL-VIO", "YEL-GRY"][col], "drive_connection": f"J13-P{[9,8,7,6,5,4,3,1][col]}", "return_wire": ["RED-BRN", "RED-BLK", "RED-ORG", "RED-YEL", "RED-GRN", "RED-BLU", "RED-VIO", "RED-GRY", "RED-WHT", "RED"][row], "return_connection": f"J12-P{[1,2,3,4,5,6,8,9,10,11][row]}", "driver_transistor": f"Q{33+row}", "nominal_voltage_v": 18, "voltage_type": "dc"}
                if address in {1, 2}:
                    device["provenance"]["source_refs"].append(CABINET_SOURCE)
                    not_applicable(device, "cabinet_or_service", MANUAL_SOURCE, RUNTIME_SOURCE, CABINET_SOURCE)
                    device["physical"]["notes"] = (
                        "Standard fitted green Start button lamp, positively shown in the manufacturer's Pro cabinet photograph."
                        if address == 1 else
                        "Optional tournament-start button lamp. The manufacturer's Pro cabinet photograph shows a black plug below the fitted green Start button. Quantity 1 is per installed optional button, not a claim of population on every unit; ROM lamp 2 remains a supported function when the button is absent."
                    )
                elif address == 59:
                    device["id"] = "lamp.left-eject-top-59"
                    device["physical"]["notes"] = "Pro matrix names LEFT EJECT TOP with one #555 clear lamp, confirmed by Pro ROM #59 and the Pro location drawing. The VPT's f59b is a reflection helper, not a socket, and its raw coordinate is rejected. The independent unverified VPX script binds f59 directly; it is corroboration only."
                else:
                    primary, layer = objects[f"l{address}"], objects[f"l{address}a"]
                    if primary["type"] != "Light" or layer["type"] != "Light" or lamp_bindings.get(address) != [f"l{address}", f"l{address}a"]:
                        raise ValueError(f"wrong lamp binding {address}")
                    observed_location(device, "emitter", primary, "One insert emitter; lN/lNa are render layers, not two physical bulbs. The VPT Light center supplies an observed layout point; individual socket fitment is not inferred from a glow.")
                    if primary.get("timer_interval") != address:
                        device["physical"]["notes"] += f" Stored TMIN={primary.get('timer_interval')} is not the controlling binding: UseLamps=0 and the custom ChangedLamps/FadeL loop explicitly drive public {address}."
            else:
                device["provenance"] = provenance("validated", MANUAL_SOURCE, RUNTIME_SOURCE)
                not_applicable(device, "unused", MANUAL_SOURCE, RUNTIME_SOURCE)
        elif group == "pinmame.output.solenoid":
            if address in {19,23,30}:
                device["kind"] = "control_signal"
                device["label"] = f"Unused Pro driver {address} (blank load cells)"
                device["availability"] = "unused"
                device["provenance"] = provenance("validated", MANUAL_SOURCE)
                device["wiring"] = {key:value for key,value in device["wiring"].items()
                                    if key in {"board","control_wire","control_connection","driver_transistor"}}
                device["physical"] = {"notes": f"Own Pro chart row {address} leaves function, power wire, power connection, voltage and coil/bulb type/part cells blank. Only the I/O Power Driver board, control wire/pin and transistor are printed. This reserved driver has no documented fitted load; no LE lamp, relay or motor type/power fields are transferred."}
            elif address == 20:
                device["label"] = "Unresolved Pro output 20 (#89 chart entry)"
                device["availability"] = "unknown"
                device["provenance"] = provenance("unknown", MANUAL_SOURCE, RUNTIME_SOURCE)
                device.pop("spatial", None)
                device["wiring"].update(power_wire="ORG",power_connection="J6-P10",nominal_voltage_v=20)
                device["wiring"].pop("voltage_type",None)
                device["physical"] = {"notes": "Own Pro row 20 has a blank FUNCTION but prints ORG / J6-P10 / 20 V / #89 BULB / 165-5000-89, plus VIO-YEL / J7-P6 / Q20. The voltage cell has no DC suffix. These printed specifications neither identify a function nor settle whether a load is fitted. The missing Pro callout and coil-selector skip are negative observations, not non-fitment proof; absent LE disc hardware does not rule out another Pro load. No retained positive wiring, erratum or complete physical flasher census resolves it. Availability and physical identity remain unknown, with no invented quantity, socket or unused spatial exemption."}
            if address in COIL_LABELS:
                device["id"] = FLASHER_IDS[address]
                device["label"] = COIL_LABELS[address]
                device["physical"] = {"quantity": FLASHER_QUANTITIES[address], "notes": "Physical name, quantity and lamp type follow the exact Pro chart (PDF 16 / printed 14), corroborated by the Pro ROM coil test. No render-sprite center is promoted as a socket."}
                device["provenance"] = provenance("validated", MANUAL_SOURCE, RUNTIME_SOURCE, PRO_VPX_TABLE_SOURCE)
                device["physical"]["part_number"] = "165-5032-00" if address == 27 else "165-5000-89"
            if 9 <= address <= 16:
                alternate = device["wiring"]["control_connection"]
                literal = f"J8-P{[1,2,4,5,6,7,8,9][address-9]}"
                device["wiring"]["control_connection"] = BOARD_PINS[address]
                device.setdefault("physical", {})["notes"] = f"The Pro chart literally prints {literal}, duplicating Group 1. The exact 520-5249-00 board schematic establishes {BOARD_PINS[address]} for Q{address}; Stern bulletin 178 associates this board with X-MEN. The combined LE chart's {alternate} belongs to the different 520-5317-00 board and does not correct Pro wiring. Source literals remain preserved; no device identity, address or fitment is inferred from a generic board schematic."
            if address == 12:
                device["wiring"]["power_wire"] = "GRY-YEL"
            elif address == 16:
                device["wiring"]["power_wire"] = "BLU-YEL / RED-YEL"
            if address == 14:
                device["wiring"]["control_wire"] = "BLU-BLU"
            if address in {27, 32}:
                device["wiring"].update(power_wire="ORG" if address == 27 else "VIO-YEL", power_connection="J6-P10" if address == 27 else "J10-P8", nominal_voltage_v=20 if address == 27 else 50)
            if 1 <= address <= 32:
                device["provenance"]["source_refs"] = list(dict.fromkeys([
                    *device["provenance"]["source_refs"], MANUAL_SOURCE, BOARD_SOURCE, BOARD_COMPATIBILITY_SOURCE]))
                if device["wiring"]["control_connection"] != BOARD_PINS[address]:
                    raise ValueError(f"Q{address}: structured control pin disagrees with exact Pro board")
            if device["availability"] == "unused":
                not_applicable(device, "unused", MANUAL_SOURCE)
            elif address == 20:
                pass  # Unknown fitment has neither an invented point nor an unused exemption.
            elif device["kind"] == "virtual":
                not_applicable(device, "virtual", device["provenance"]["source_refs"][0])
            elif address in {8, 24}:
                not_applicable(device, "cabinet_or_service", MANUAL_SOURCE)
            elif address == 31:
                x, y = figure_base_position(objects["wr3"])
                device["spatial"] = {"status":"observed", "placements":[{
                    "id":device["id"]+".emitter", "role":"emitter", "space":"playfield",
                    "x":round(x/959,6), "y":round(y/2162,6),
                    "provenance":provenance("observed", GEOMETRY_SOURCE, PRO_VPX_TABLE_SOURCE, MANUAL_SOURCE, MAGNETO_SOURCE),
                }]}
                device["physical"]["notes"] += " Observed projection onto its own Magneto figure assembly: exact visible, noncollidable Ramp wr3 uses the opaque magneto bust/cape image. Its IMAGEBOTTOM endpoint (522, 489), not a generic Ramp center, supplies the projection. Authored bottom/top heights 50/370 and width 280 describe a broad billboard, not physical dimensions. The manufacturer figure-skirt candidate differs by about 0.041 x/0.044 total, with raised geometry and parallax unresolved. The actual bulb-bracket offset is unmeasured; neither the remote 31 box nor the (.563,.082) gate/body candidate becomes a socket."
            elif address in COIL_OBJECTS:
                previous = device.get("physical", {}).get("notes", "")
                observed_location(device, "effect", objects[COIL_OBJECTS[address]], previous + " Actuator/effect projected onto its own modelled assembly. This does not locate any separate switch or lamp socket.")
            if address in {19, 20, 23}:
                device["physical"]["notes"] += " The historical device ID is retained for compatibility; its wording is not a current availability or physical-load assertion."
            audit = next((r for r in wiring_audit["readings"] if r["address"] == address), None)
            if audit and audit["comparison_note"]:
                device.setdefault("physical", {})["notes"] += " " + audit["comparison_note"] + " ROM display text does not establish physical wire; the own Pro chart remains the game-harness authority."
    for display in definition["displays"]:
        not_applicable(display, "cabinet_or_service", MANUAL_SOURCE, CORE_SOURCE)
    # Do not let inherited LE labels, quantities or voltage fields determine Pro facts.
    for source in definition["sources"]:
        if source["id"] == PRO_VPX_SOURCE:
            source["known_working"] = False
            source["locator"] += "; header explicitly says Table not verified yet; corroborating lead only, not the primary runtime authority"
        if source["id"] == PRO_VPX_TABLE_SOURCE:
            source["locator"] += "; successor exact compound extraction via 7-Zip 22.01 at extraction/7zip-22.01-20261106 and bounded BIFF coordinate reader, raw manifest SHA-256 " + RAW_MANIFEST_SHA256 + "; historical full VPXTool image-parser failure is preserved, not the current coordinate blocker"
    definition["sources"] += [
        {"id": BOARD_SOURCE, "kind": "manual", "uri": "https://sternpinball.com/wp-content/uploads/2018/11/Batman_TDK_Manual.pdf", "sha256": BOARD_SHA256, "original_filename": "Batman_TDK_Manual.pdf", "locator": "PDF pages 136/137, printed 116/117, sheet 2 LEFT/RIGHT: complete Q1-Q32 connector regions of I/O Power Driver 520-5249-00; PDF 142, printed 122, component layout confirms the same board. Used only for internal board routing, never Batman game harness, load or fitment. Original and native renders retained in source-evidence-v5. The local source-copy retained_at time is copied from the frozen source-evidence-v5/manufacturer/sam-520-5249/board-provenance.json; it records retained-source-copy time, not first internet-download time", "license": "NOASSERTION", "attribution": "Stern Pinball", "acquired_at": "2026-11-07T01:38:32.536819+00:00", "excerpts": [excerpt(root, "pro-sam-board-connectors", "520-5249-00 schematic, all Q1-Q32 output header pins, keys and +20 V pins")]},
        {"id": BOARD_COMPATIBILITY_SOURCE, "kind": "manual", "uri": "https://sternpinball.com/wp-content/uploads/2018/10/sb178.pdf", "original_filename": "sb178.pdf", "locator": "Stern Service Bulletin 178, page 2 compatibility table: X-MEN uses 520-5249-00, X-MEN (L/E) uses 520-5317-00; Batman also uses 520-5249-00. This identifies the applicable board, not any game harness or fitted load. The bulletin literally prints December 13, 2011; no inferred issue date is substituted.", "license": "NOASSERTION", "attribution": "Stern Pinball", "excerpts": [excerpt(root, "sb178-board-type-table", "Stern Service Bulletin 178, pages 1-2, complete Board Type Table")]},
        {"id":CABINET_SOURCE, "kind":"manual", "uri":"https://pinball-universe.de/mediafiles/pdf/stern-pinball/x-men/x-men-pro-flyer.pdf", "sha256":"120eba395dd40cbb3a1eab3f5a9472e2720e61fdc709c33f23569fd42a113c16", "original_filename":"pro-flyer.pdf", "locator":"Manufacturer Pro flyer PDF page 1, embedded xref 8 JPEG 1275 x 1650; native crop (420, 1000, 650, 1380) shows green Start and black plug below it. Official corroborating manufacturer image https://wp.sternpinball.com/wp-content/uploads/2018/11/XMenPro-Right.png SHA-256 c074f36438177ef2ee5975365c519cf573008f85290493f7710b870d8b045637. Originals, source provenance and native JPEG are retained in the frozen source bundle; cabinet fitment is independent of ROM function naming.", "license":"NOASSERTION", "attribution":"Stern Pinball manufacturer Pro flyer and cabinet photograph", "excerpts":[excerpt(root,"pro-cabinet-fitment","PDF page 1 xref 8: standard Start button and plugged optional tournament-button opening")]},
        {"id": MANUAL_SOURCE, "kind": "manual", "uri": "https://o.pinside.com/5/7c/97/57c9760c4ee131cc69cafd7cb89f8be26535b327.pdf", "sha256": MANUAL_SHA256, "original_filename": "Stern_2012_X-Men_Pro.pdf", "locator": "Original Pro-only service book scanned by owner redundor; https://pinside.com/pinball/forum/topic/x-men#post-2591274. PDF 16 / printed 14 coils, PDF 17 / printed 15 locations, PDF 19 / printed 17 lamp matrix, PDF 20 / printed 18 lamp locations. Original retained at external:pinmame-manuals/" + MANUAL_RELATIVE + "; all 38 pages OCR searched; native-resolution reviewed renders are retained beside it.", "license": "NOASSERTION", "attribution": "Stern Pinball; original Pro service-book scan by Pinside owner redundor", "rights": "NOASSERTION; source PDF stays external", "acquired_at": "2026-11-06T21:05:16.571Z", "excerpts": [excerpt(root, "pro-coils", "PDF 16, printed 14, complete Coils Detailed Chart Table"), excerpt(root, "pro-lamps", "PDF 19, printed 17, complete Lamp Matrix Grid #1-#80")]},
        {"id": GEOMETRY_SOURCE, "kind": "human_review", "uri": "external:pinmame-vpx-sources/" + VPX_RELATIVE + "/extraction/7zip-22.01-20261106", "sha256": RAW_MANIFEST_SHA256, "locator": "Full raw compound streams: 1,940 files, 24,518,088 bytes; official case-sensitive canonical external manifest. tools/xmen_pro_vpt_geometry.py reads explicit NAME/VCEN/FLAX/FLAY/TMIN and drag-point VCEN records only. All streams independently match OpenMcdf byte-for-byte; unsupported decal/font and other semantic payloads are not interpreted. Portable selected coordinate seed: " + SEED_RELATIVE, "license": "NOASSERTION", "attribution": "85vett table; independent local 7-Zip extraction and bounded coordinate inspection", "excerpts": [excerpt(root, "geometry-method", "Exact retained VPT stream records and known-working script bindings")]},
        {"id": RUNTIME_SOURCE, "kind": "service_diagnostic", "uri": "external:pinmame-review-artifacts/" + REVIEW_RELATIVE, "sha256": file_sha256(root / RUNTIME_RELATIVE), "revision": "46e1a01a0f73dc5ce163d98db1ae435883ecc450", "locator": "Fresh xmn_151 V1.51 Single Lamp Test and Coil Test; portable readings at " + RUNTIME_RELATIVE + ". Public output transitions pair actual shown addresses with labels and quantities; optional coil 24 shows no output and is not called observed activity.", "license": "NOASSERTION", "attribution": "Stern Pro firmware diagnostics, run locally using user-authorized ROM; only derived readings and hashes committed", "excerpts": [excerpt(root, "service-tests", "Visually read retained DMD frames for lamp #1-#80 and 28 coil-selector entries")]},
        {"id": drawings.SOURCE, "kind": "human_review", "uri": "repo:" + drawings.SEED, "sha256": file_sha256(root / drawings.SEED), "locator": "Independent original-Pro native pixel reads, primary source-overlay corrections, six exact table controls per page and reproducible 0.07 leave-one-out checks. No LE point or quantity is transferred. Drawing-measured placements are not checked on their own measurement page.", "license": "NOASSERTION", "attribution": "Stern Pro drawings; independent native-pixel readers and curator physical-source verification"},
        {"id": GI_SOURCE, "kind": "human_review", "uri": "repo:" + drawings.SEED, "sha256": file_sha256(root/drawings.SEED), "locator": "Partial Pro GI census and rear factory-photo readings. Original Pro CAD supplies every plan pixel; stock NIB photo, later Pro lamp-body photo, stock owner 4 #44 report and 2012 factory Pro rear-board photograph corroborate the stated physical subsets. Explicit single-component LE profile overlay does not copy count, color or coordinates. Full sources retained in the seed's frozen artifact manifest; rear affine geometry remains observed.", "license": "NOASSERTION", "attribution": "Stern drawings; Pinside Pro owners; Michael Minn 2012 Stern factory photograph; independent source readers and curator verification", "excerpts": [excerpt(root,"pro-gi-partial","Complete owner GI section, actual Pro body correspondence, factory rear-board photograph and calibration limits")]},
        {"id": MAGNETO_SOURCE, "kind": "human_review", "uri": "https://pinside.com/pinball/forum/topic/x-men/page/246#post-6671751", "locator": "D0N actual Pro disassembly: diagnostic 31 inside figure, separate flashers left/right of lock entry; photo 00 shows large standing collar beside steel lock and horizontal socket on lifted figure. Photo 05 detached two-yellow-dome ramp establishes Pro. Actual CAD pair 22 identity is resolved by physical landmarks, not generic profile or absence of a GI leader. Captured post and exact photos are retained in the frozen source bundle.", "license": "NOASSERTION", "attribution": "Pinside member D0N; curator physical-hardware correspondence", "excerpts": [excerpt(root,"pro-magneto-hardware","Full relevant owner repair explanation and actual Pro socket/track/bracket correspondence")]},
        {"id": TROUGH_SOURCE, "kind": "human_review", "uri": "repo:"+drawings.SEED, "sha256":file_sha256(root/drawings.SEED), "locator":"The common labeled cutaway establishes microswitch order 18/19/20 and vertically stacked optos 21/22. The former component-photo points were misidentified cable-tie heads and a harness clip, so all three placements are withdrawn. Historical pixels remain rejected evidence, never active actuator geometry. Whole cutaway length is not measured across its drawing break.", "license":"NOASSERTION", "attribution":"Stern common trough assembly drawing and retained component photograph; curator source verification", "excerpts":[excerpt(root,"pro-trough-projection","Complete common trough parts table, contact topology and rejected wrong-component history")]},
        {"id":SPOTLIGHT_SOURCE,"kind":"human_review","uri":"external:pinmame-review-artifacts/"+REVIEW_RELATIVE+"/gallery-images/sale-22-13.jpg","sha256":"3b772d7e2544f4f3277c148f8174aecb7345af64b5fe0358add5dae60dfe8088","locator":"Actual Pro chrome Q27 head/stem joint image projection, bounded by ten independently reconciled insert controls. The joint is raised above the insert plane; height/parallax remain unmeasured. Passing the control hull and leave-one-out 0.07 checks validates only 2D image calibration. Physical placement and provenance remain observed.","license":"NOASSERTION","attribution":"Pinside Pro owner photo; curator physical-part identification and bounded local calibration","excerpts":[excerpt(root,"pro-spotlight-photo","Own raised spotlight housing, all ten native control reads and unresolved physical-plane limits")]},
    ]
    manual = next(source for source in definition["sources"] if source["id"] == MANUAL_SOURCE)
    board = next(source for source in definition["sources"] if source["id"] == BOARD_SOURCE)
    board["locator"] += "; original external:pinmame-manuals/by-machine/stern.x-men-pro.2012/stern-sam-board/Batman_TDK_Manual.pdf"
    compatibility = next(source for source in definition["sources"] if source["id"] == BOARD_COMPATIBILITY_SOURCE)
    compatibility["sha256"] = BOARD_COMPATIBILITY_SHA256
    compatibility["acquired_at"] = "2026-11-07T01:20:26.238568+00:00"
    compatibility["locator"] += "; original external:pinmame-manuals/by-machine/stern.x-men-pro.2012/stern-sam-board/sb178.pdf"
    next(source for source in definition["sources"] if source["id"] == RUNTIME_SOURCE)["excerpts"].append(
        excerpt(root, "pro-coil-wiring-audit", "All 28 pinned coil-selector wire pairs compared with complete own Pro chart cells"))
    next(source for source in definition["sources"] if source["id"] == GEOMETRY_SOURCE)["locator"] += "; exact wr3 also retains IMAG/HTBT/HTTP/WDBT/WDTP/CLDR/RVIS for the reviewed own-figure projection, not generic Ramp centers. Image52 declared PNG payload SHA-256 " + FIGURE_PNG_SHA256
    manual["excerpts"] += [excerpt(root, f"pro-{key}-locations", f"Original Pro PDF{page}: complete playfield location drawing") for key, page in (("switches", 14), ("coils", 17), ("lamps", 20))]
    callout_seed = load_json(root / drawings.SEED)
    drawings.validate_controls(callout_seed, objects, object_position)
    measurements = drawings.add_measurements(definition, callout_seed, MANUAL_SOURCE)
    decisions = drawing_callouts.apply_to_definition(definition, callout_seed, drawings.SOURCE)
    if unresolved_conflicts(definition):
        raise ValueError("unresolved machine conflicts cannot be silently cleared")
    # This guard is intentionally independent of the migration pending tuple.
    if definition["coverage"]["status"] != "partial" or definition["coverage"]["missing"] != ["output_semantics", "spatial_placement"]:
        raise ValueError("unproved spatial coverage cannot be promoted")
    report = pro_gamedata_evidence()
    report["historical_audit"] = copy.deepcopy(report)
    report["version"] = 2
    report["extraction"]["successor"] = {"reader": "tools/xmen_pro_vpt_geometry.py", "status": "bounded_coordinate_fields_recovered", "raw_stream_count": 1940, "raw_bytes": 24518088, "declared_game_items": 1702, "raw_manifest_sha256": RAW_MANIFEST_SHA256, "full_semantic_parse": False}
    report["transformations"] = [{"class": "observed_coordinate_normalization", "detail": "Exact direct centers or Surface drag-point arithmetic means are divided by 959/2162 and rounded once to six decimals. No clamping."}]
    report["projection_classes"] = [{"class": "observed_assembly_projection", "detail": "Actuators and two EOS inputs project onto their own assembly; no shared exit point substitutes for the three distinct mechanical trough contacts."}, {"class": "render_sprite_rejected", "detail": "All fN and f59b sprite centers remain raw candidates, even where the new Pro chart proves quantity."}, {"class": "edition_transfer_rejected", "detail": "No LE coordinate, total socket count or whole GI map populates Pro. Explicit corresponding-profile keys are reconciled against actual Pro fitted bodies and retain observed circuit status where needed."}]
    report["projection_classes"].append({"class": "vertical_exit_opto_pair", "detail": "21/22 project onto their own exit assembly in plan: the common cutaway proves vertically stacked beams on one receiver/transmitter pair. This does not place the three mechanical track switches 18-20."})
    report["coordinate_convention"]["applies_to"] = "Table-derived locations use exact binary32 centers or Surface drag-point arithmetic means; x/959, y/2162, rounded once to six decimals. Factory measurements use independently calibrated Pro drawing pixels, rounded to three decimals. Render-only sprites remain raw candidates."
    report["successor_evidence"] = {"manual_sha256": MANUAL_SHA256, "raw_manifest_sha256": RAW_MANIFEST_SHA256, "coordinate_seed": SEED_RELATIVE, "runtime_readings": RUNTIME_RELATIVE, "scope": seed["scope"]}
    report["drawing_reconciliation"] = drawing_callouts.summary(callout_seed, decisions, drawings.SEED, file_sha256(root / drawings.SEED))
    report["drawing_measurements"] = measurements
    report["accepted_measurement_count"] = len(measurements)
    report["rejected_trough_contact_projection"] = callout_seed["rejected_trough_contact_projection"]
    report["coil_wiring_audit"] = load_json(root / COIL_WIRING_RELATIVE)
    report["partial_censuses"] = callout_seed["partial_censuses"]
    report["hypothesis_reassessment"] = callout_seed["reassessment"]
    report["candidate_measurements"] = {"q31":callout_seed["q31_candidate"]}
    report["figure_assembly_projection"] = {
        "status":"observed", "object":objects["wr3"], "source_png_sha256":FIGURE_PNG_SHA256,
        "raw_bottom_endpoint":list(figure_base_position(objects["wr3"])),
        "normalized":[round(522/959,6),round(489/2162,6)],
        "manufacturer_candidate_offset":round(drawing_callouts.distance((522/959,489/2162),(.5034,.2104)),6),
        "limit":"Opaque own-figure image establishes assembly identity, not the hidden bulb bracket. Authored height 50/370, width 280 and raised/out-of-hull manufacturer comparison cannot validate this projection. Old gate/body candidate remains rejected.",
    }
    report["rear_photo_calibration"] = {"source":callout_seed["elevations"]["pro-factory-rear"], "status":"observed_only", "reason":"Two visible board ends and one edge define an affine basis. The lower-right corner is concealed; no four-control perspective validation or equal-spacing assumption is asserted."}
    report["settled_facts"] = {"flasher_quantities": {str(k): v for k, v in FLASHER_QUANTITIES.items()}, "lamp_59": "LEFT EJECT TOP, physically populated in Pro chart and Pro diagnostic; f59b reflection is not its socket", "cabinet_lamps": [1, 2], "wolverine_magnet": "Pro Q32, VIO-YEL, J10-P8, 50 VDC", "trough_21": "lower opto beam; 22 upper stacking beam"}
    report["settled_facts"]["cabinet_fitment"] = {"standard_lamps":[1], "optional_lamps":[2], "optional_switches":[15], "assigned_lamp_functions":61, "standard_lamp_functions":60, "source":CABINET_SOURCE}
    report["unresolved_blockers"] = [
        {"id": "gi-0-pro-socket-geometry", "blocker": "Partial census contains 35 actual Pro body/projection records. Positive white-GI component keys plus actual Pro body continuity settle B01, H02, H04; whole quantity remains unset. B02(155, 1226) and UL2(579, 670) still lack positive component/circuit identity. They cannot be included or excluded merely to match owner totals. Rear perspective and observed correspondences also remain below validation."},
        {"id": "physical-emitter-centers", "devices": {"solenoids": [27,28,29,31]}, "blocker": "Calibrated Pro drawings and positive disassembly settle four domes, Q21/Q22/Q25 and 59. Q27's head/stem joint is raised above the insert control plane; its observed image projection has no measured height/parallax correction. Q31 has an observed own-figure projection from reviewed wr3's bottom endpoint; authored billboard height/width and unmeasured bracket offset prevent validation. Six Q28/29 factory-photo projections retain unresolved perspective and stay observed."},
        {"id": "switches-18-through-20-trough-centers", "devices": {"inputs": [18,19,20]}, "blocker": "All three former component-photo points identified wiring hardware rather than switch actuators and are withdrawn. Microswitch order is established by the cutaway, but no retained accepted individual actuator geometry locates 18/19/20. The 21/22 vertical beam stack separately retains its observed exit-assembly projection."},
        {"id": "observed-layout-reconciliation", "blocker": "All 54 independently checkable ordinary lamps and 10 readable switch assemblies agree with Pro factory callouts. Calibration controls do not validate themselves; concealed sensor endpoints and remaining actuator/EOS assembly projections retain their observed status pending further physical reconciliation. The detailed drawing report names each accepted check and measured point."},
    ]
    report["unresolved_blockers"].append({"id":"output-20-fitment-and-function", "devices":{"solenoids":[20]}, "blocker":"Own Pro row 20 prints a possible #89 load specification but no function. No positive retained source settles fitment or non-fitment; selector omission and missing callout cannot decide. Availability/identity remain unknown, with no physical quantity or unused spatial exemption. Owner insert/GI lists are not a complete flasher census."})
    report["promotion_decision"] = {"decision": "remain_partial", "coverage_missing": ["output_semantics", "spatial_placement"], "reason": "Q20's printed residual load specification leaves fitment and function unknown. Spatial evidence still leaves two GI identities/whole census, Q27 raised-housing parallax, Q31 bracket geometry, missing individual trough-actuator geometry, rear perspective and observed assembly projections unresolved. No negative runtime observation, count or status edit waives these gaps."}
    report["canonical_spatial_summary"] = {"observed_devices": sum(d.get("spatial", {}).get("status") == "observed" for d in definition["inputs"] + definition["outputs"]), "not_applicable_devices": sum(d.get("spatial", {}).get("status") == "not_applicable" for d in definition["inputs"] + definition["outputs"]), "unplaced_devices": [d["id"] for d in definition["inputs"] + definition["outputs"] if "spatial" not in d]}
    return definition, report


def generate(root: Path = ROOT, check: bool = False, inputs_root: Path = ROOT) -> None:
    verify_external(inputs_root)
    if (root / "machines/author-ready/stern/x-men-pro-2012.json").exists():
        raise ValueError("refusing to shadow or overwrite an existing author-ready Pro definition")
    definition, report = build(inputs_root)
    outputs = {
        "machines/partial/stern/x-men-pro-2012.json": canonical_bytes(definition),
        "reports/spatial/stern/x-men-pro-2012.json": canonical_bytes(report),
        "knowledge/stern/x-men-pro-2012.md": (inputs_root / NOTE_RELATIVE).read_bytes(),
    }
    for path, payload in outputs.items():
        destination = root / path
        if check:
            if not destination.is_file() or destination.read_bytes() != payload:
                raise ValueError(f"curator output drift: {path}")
        elif path.endswith(".json"):
            write_json(destination, json.loads(payload))
        else:
            write_text(destination, payload.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    generate(check=parser.parse_args().check)
