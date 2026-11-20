"""Regenerate the Flight 2000 definition and its spatial audit from pinned inputs."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from pinmame_game_defs.identifiers import slug
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256, load_json, write_bytes
from pinmame_game_defs.spatial import extract_spatial_candidates

from build_external_evidence_manifest import build_manifest, check_manifest
import flight_2000_data as data


ROOT = Path(__file__).resolve().parents[1]
ID = "stern.flight-2000.1980"
SLUG = "flight-2000-1980"
CONVERSION_ID = "pinstar.gamatron.1985"
SEEDS = ROOT / "tools/seeds/stern"
EXCERPTS = ROOT / "evidence/excerpts" / ID
DEFINITION = Path(f"machines/partial/stern/{SLUG}.json")
CONVERSION = Path("machines/partial/pinstar/gamatron-1985.json")
KNOWLEDGE = Path(f"knowledge/stern/{SLUG}.md")
CONVERSION_NOTE = Path("knowledge/pinstar/gamatron-1985.md")
REPORT = Path(f"reports/spatial/stern/{SLUG}")
VPX = Path("stern") / SLUG
VPX_NAME = "Flight 2000 (Stern 1980).vpx"
VPX_VERSION = "vpxtool git:v0.33.3"
CORE = "pinmame.core.mpu200.46e1a01a"
MANUAL = "manual.flight-2000.instruction"
SCHEMATIC = "manual.flight-2000.schematics"
SCRIPT = "vpx-script.flight-2000.bord-2-0"
TABLE = "vpx-table.flight-2000.bord-2-0"
UPPER_PHOTO = "photo.flight-2000.ipdb-15827"
LOCK_PHOTO = "photo.flight-2000.ipdb-15842"
SERVE_PHOTOS = ("photo.flight-2000.ipdb-49151", "photo.flight-2000.ipdb-49153")
RUNTIME = "runtime.flight-2000.service"
RUNTIME_EVIDENCE = ROOT / "evidence/runtime/stern/flight-2000-service.json"


def provenance(*refs: str, status: str = "validated") -> dict:
    return {"source_refs": list(refs), "status": status}


def not_applicable(reason: str, *refs: str) -> dict:
    return {"status": "not_applicable", "reason": reason, "provenance": provenance(*refs)}


def excerpt_rows(name: str) -> list[list[str]]:
    text = (EXCERPTS / name).read_text(encoding="utf-8")
    return [[value.strip() for value in line.split("|")[1:-1]]
            for line in text.splitlines() if line.startswith("| ")][2:]


def device(prefix: str, label: str, kind: str, group: str, address: int,
           prov: dict, availability: str = "used") -> dict:
    aliases = []
    if group.startswith("pinmame."):
        aliases.append({"namespace": f"pinmame.{group.rsplit('.', 1)[-1]}", "value": str(address)})
    return {
        "id": f"{prefix}.{slug(label)}", "label": label, "kind": kind,
        "binding": {"group": group, "device": address}, "aliases": aliases,
        "provenance": prov, "availability": availability,
    }


def locate(item: dict, role: str, objects: tuple[str, ...], geometry: dict, *refs: str) -> None:
    item["spatial"] = {"status": "observed", "placements": [
        {
            "id": f"{item['id']}.{role}.{slug(name)}", "space": "playfield", "role": role,
            "x": geometry[name]["x"], "y": geometry[name]["y"],
            "provenance": provenance(TABLE, *refs, status="observed"),
        }
        for name in objects
    ]}


def build_inputs(geometry: dict) -> list[dict]:
    switches = "pinmame.input.switch"
    result = []
    for address, label, notes in (
        (-7, "Self test", "Normally open inside-door switch. A4J3-1 to A3J2-7."),
        (-6, "MPU diagnostic S33", "MPU pushbutton pulls the NMI line low."),
        (-5, "Sound diagnostic / voice selection", "PinMAME routes the generic sound diagnostic state into the ST300 voice-select handler."),
    ):
        physical = address != -5
        item = device("switch" if physical else "input", label, "switch" if physical else "virtual",
                      switches, address, provenance(CORE, MANUAL))
        item["spatial"] = not_applicable("cabinet_or_service" if physical else "virtual", CORE, MANUAL)
        item["physical"] = {"notes": notes}
        if physical:
            item.update(normally_closed=False, roles=["service.test"], pulse=False)
            item["physical"]["switch_type"] = "button"
        result.append(item)

    rows = excerpt_rows("switch-identification.md")
    if [int(row[0]) for row in rows] != list(range(1, 41)):
        raise ValueError("The switch source must account for every matrix address")
    for address, label in enumerate(data.SWITCH_LABELS, 1):
        _, strobe, strobe_pin, wire, pin, _, cap = rows[address - 1]
        item = device("switch", label, "switch", switches, address, provenance(MANUAL, SCHEMATIC, CORE))
        item["aliases"].append({"namespace": "manual.self-test", "value": str(address)})
        item["normally_closed"] = False
        item["pulse"] = address in data.MOMENTARY_SWITCHES
        item["wiring"] = {"board": "A4 MPU-200", "control_wire": strobe,
                          "control_connection": f"A4{strobe_pin}", "return_wire": wire.strip("-"),
                          "return_connection": f"A4{pin}"}
        if address > 3:
            item["wiring"]["return_component"] = "1N4004"
        notes = []
        if cap == "yes":
            notes.append("The factory switch chart marks a .05 capacitor.")
        if address in data.SCHEMATIC_SWITCH_RETURNS:
            notes.append(f"The playfield circuit prints {data.SCHEMATIC_SWITCH_RETURNS[address]} on A4{pin}.")
        if notes:
            item["physical"] = {"notes": " ".join(notes)}
        if address in data.CABINET_SWITCHES:
            item["spatial"] = not_applicable("cabinet_or_service", MANUAL)
            item.setdefault("physical", {})["location"] = "Cabinet / coin door"
        if address in data.SWITCH_OBJECTS:
            objects = data.SWITCH_OBJECTS[address]
            refs = (SCRIPT, MANUAL, UPPER_PHOTO) if address == 17 else (SCRIPT, MANUAL)
            locate(item, "sensor", objects, geometry, *refs)
            item.setdefault("physical", {})["quantity"] = len(objects)
        if address == 17:
            item["physical"]["notes"] += " The lower rollover and both rear stand-ups share this matrix address."
        result.append(item)

    for address, label in (
        (81, "Reserved right EOS position"), (82, "Right flipper cabinet button"),
        (83, "Reserved left EOS position"), (84, "Left flipper cabinet button"),
    ):
        used = address in (82, 84)
        item = device("switch", label, "switch", switches, address, provenance(CORE, MANUAL),
                      "used" if used else "unused")
        item["spatial"] = not_applicable("cabinet_or_service" if used else "unused", CORE, MANUAL)
        if used:
            item.update(normally_closed=False, pulse=False)
            item["physical"] = {"switch_type": "button", "location": "Cabinet side"}
        result.append(item)

    for address, side in enumerate(("Left", "Right"), 1):
        item = device("switch", f"{side} hard-wired flipper EOS", "switch", "physical.input.direct",
                      address, provenance(SCHEMATIC))
        item["normally_closed"] = True
        item["physical"] = {
            "switch_type": "leaf", "quantity": 1, "location": f"{side} under-playfield flipper assembly",
            "notes": "The series bypass contact opens at end of stroke and transfers current through the hold winding.",
        }
        locate(item, "sensor", (f"Flipper.{side}Flipper",), geometry, SCHEMATIC)
        result.append(item)

    item = device("switch", "Door memory clear", "switch", "physical.input.direct", 3, provenance(SCHEMATIC, MANUAL))
    item.update(normally_closed=False, spatial=not_applicable("cabinet_or_service", SCHEMATIC),
                physical={"switch_type": "button", "notes": "Remote bookkeeping reset at A4J3-5."})
    result.append(item)

    for address in range(1, 33):
        label = data.DIP_LABELS.get(address)
        item = device("dip", label or f"Unspecified MPU DIP {address}", "dip_switch", "pinmame.input.dip", address,
                      provenance(CORE, MANUAL, status="validated" if label else "candidate"),
                      "used" if label else "unknown")
        item.update(spatial=not_applicable("dip_switch", CORE, MANUAL),
                    physical={"location": "MPU board", "switch_type": "dip"})
        result.append(item)
    return result


def build_coils(geometry: dict) -> list[dict]:
    coils = "pinmame.output.solenoid"
    rows = excerpt_rows("solenoid-identification.md")
    result = []
    for address, (q, label, anchor) in data.COILS.items():
        number, transistor, connector, wire, _ = rows[q - 1]
        if (number, transistor) != (str(q), f"Q{q}"):
            raise ValueError(f"Coil source row does not match Q{q}")
        item = device("coil" if address != 19 else "relay", label, "coil" if address != 19 else "relay",
                      coils, address, provenance(CORE, MANUAL, SCHEMATIC))
        item["aliases"].append({"namespace": "manual.solenoid-test", "value": str(q)})
        item["wiring"] = {"board": "A3 SDU", "driver_transistor": transistor,
                          "drive_connection": f"A3{connector}", "drive_wire": wire}
        if address in data.COIL_PARTS:
            item["physical"] = {"part_number": data.COIL_PARTS[address]}
        if address == 4:
            item["physical"]["notes"] = "The coil circuit and SDU drawing both print G-R at this connection. The game-specific load chart gives G-P pending a physical wire check."
        if address == 9:
            item["physical"]["assembly_part_number"] = "B-758"
        if address == 10:
            item["physical"]["notes"] = "The two factory mounting versions share the shooter-lane serve point projected here."
        if address in (18, 19):
            item["spatial"] = not_applicable("cabinet_or_service", MANUAL)
        if anchor:
            refs = (SCRIPT, SCHEMATIC, *SERVE_PHOTOS) if address == 10 else (SCRIPT, SCHEMATIC)
            locate(item, "effect", (anchor,), geometry, *refs)
        result.append(item)

    for address, side, winding in ((45, "Right", "power"), (46, "Right", "hold"),
                                   (47, "Left", "power"), (48, "Left", "hold")):
        item = device("coil", f"{side} flipper {winding}", "coil", coils, address, provenance(CORE, SCHEMATIC))
        item["physical"] = {
            "part_number": "J-25-475/34-4500",
            "notes": "One winding of a dual-winding flipper assembly. PinMAME asserts both synthetic outputs together. Physical EOS timing is independent.",
        }
        locate(item, "effect", (f"Flipper.{side}Flipper",), geometry, SCHEMATIC)
        result.append(item)
    return result


def build_lamps() -> list[dict]:
    rows = excerpt_rows("lamp-wiring.md")
    decoder_rows = excerpt_rows("decoder-routing.md")[1:5]
    if len(rows) != 60 or len(decoder_rows) != 4:
        raise ValueError("Incomplete factory lamp transcription")
    result = []
    for bank, (decoder, scrs) in enumerate(decoder_rows):
        if decoder != f"Lamp U{bank + 1}" or len(scrs.split(", ")) != 15:
            raise ValueError(f"Incomplete SCR decode for {decoder}")
        for offset, scr in enumerate(scrs.split(", "), 1):
            address = bank * 16 + offset
            selected = [rows[n - 1] for n in data.LAMP_ROWS.get(address, ())]
            discrepant = data.UNVERIFIED_LAMP_WIRING.get(address)
            if not selected:
                result.append(device("lamp", f"Unidentified lamp output {address} ({scr})", "lamp",
                                     "pinmame.output.lamp", address, provenance(CORE, SCHEMATIC, status="candidate"),
                                     "unknown"))
                continue
            label = data.LAMP_LABELS.get(address, selected[0][0].capitalize())
            item = device("lamp", label, "lamp", "pinmame.output.lamp", address,
                          provenance(CORE, MANUAL, SCHEMATIC, SCRIPT, status="candidate" if discrepant else "validated"),
                          "unknown" if discrepant else "used")
            if discrepant:
                item["physical"] = {"notes": discrepant}
            else:
                description, wire, jack, pin = selected[-1]
                item["wiring"] = {"board": "A5 LDA-100", "driver_transistor": scr,
                                  "drive_connection": f"{jack}-{int(pin)}", "drive_wire": wire}
                item["physical"] = {"quantity": len(selected)}
            if address == 11:
                item["physical"]["notes"] = "Q3 feeds the playfield Shoot Again at J1-26 and the backbox through J2-21."
            if address in data.BACKBOX_LAMPS:
                item["spatial"] = not_applicable("cabinet_or_service", MANUAL)
            result.append(item)

    item = device("gi", "Transformer-fed general illumination", "gi", "physical.output.gi",
                  1, provenance(SCHEMATIC))
    item["wiring"] = {"board": "A2 rectifier", "power_wire": "W", "power_connection": "A2J1-8",
                      "return_wire": "R", "return_connection": "A2J1-2", "nominal_voltage_v": 6, "voltage_type": "ac"}
    item["physical"] = {"notes": "The playfield schematic shows the feed but does not count or locate all sockets. VPX GI uses glow objects without visible mesh bulbs in those groups."}
    result.append(item)
    return result


def build_displays() -> list[dict]:
    labels = ("Player 1", "Player 2", "Player 3", "Player 4", "Credits", "Match / ball in play")
    return [
        {"id": f"display.{slug(label)}", "label": label, "kind": "segment",
         "controller_index": index, "segment_start": start, "width": width, "height": 1,
         "physical_location": "cabinet_or_service", "spatial": not_applicable("cabinet_or_service", CORE, MANUAL),
         "provenance": provenance(CORE, MANUAL, RUNTIME)}
        for index, (label, start, width) in enumerate(zip(labels, (1, 9, 17, 25, 35, 38), (7, 7, 7, 7, 2, 2)))
    ]


def build_mechanisms(inputs: list[dict], coils: list[dict]) -> list[dict]:
    switches = {item["binding"]["device"]: item["id"] for item in inputs
                if item["binding"]["group"] == "pinmame.input.switch"}
    solenoids = {item["binding"]["device"]: item["id"] for item in coils}
    result = []
    for identifier, label, kind, part, outputs, sensors, behavior in data.MECHANISMS:
        references = [MANUAL, SCHEMATIC, SCRIPT]
        if identifier == "ball-walker":
            references.append(LOCK_PHOTO)
        if identifier == "outhole-serve":
            references.extend(SERVE_PHOTOS)
        item = {"id": f"mechanism.{identifier}", "label": label, "kind": kind,
                "actuators": [solenoids[n] for n in outputs], "sensors": [switches[n] for n in sensors],
                "behavior": behavior, "provenance": provenance(*references)}
        if part:
            item["assembly_part_number"] = part
        result.append(item)
    return result


def build_flight(seed: dict, geometry: dict) -> dict:
    inputs = build_inputs(geometry)
    coils = build_coils(geometry)
    return {
        "format": "pinmame-machine-definition", "schema_version": 2,
        "machine": {
            "id": ID, "name": "Flight 2000", "manufacturer": "Stern", "year": 1980, "model_number": "128",
            "kind": "physical_pinball", "ipdb_id": 887, "opdb_id": "G48kY-MDxRV",
            "playfield": {
                "width": seed["geometry"]["bounds"]["right"] - seed["geometry"]["bounds"]["left"],
                "height": seed["geometry"]["bounds"]["bottom"] - seed["geometry"]["bounds"]["top"],
                "units": "vpx", "provenance": provenance(TABLE),
            },
        },
        "controller": {"platform": "pinmame.stern-mpu200", "hardware_generation": "0x1000000",
                       "inversion_applied_by_emulator": True},
        "drivers": [
            dict(driver, physical_compatibility="compatible" if driver["id"] == "flight2mb" else "identical",
                 variant_notes=data.DRIVER_NOTES[driver["id"]])
            for driver in seed["drivers"] if driver["id"] != "gamatron"
        ],
        "inputs": inputs, "outputs": coils + build_lamps(), "displays": build_displays(),
        "mechanisms": build_mechanisms(inputs, coils), "relationships": [], "conflicts": [],
        "sources": seed["sources"],
        "knowledge": {"path": KNOWLEDGE.as_posix(), "status": "complete"},
        "coverage": {"status": "partial",
                     "missing": ["input_semantics", "output_semantics", "mechanism_behavior",
                                 "variant_differences", "spatial_placement"],
                     "dimensions": {
                         "catalog_identity": "validated", "address_enumeration": "validated",
                         "semantic_naming": "candidate", "physical_wiring": "observed",
                         "emulator_normalization": "validated", "runtime_observation": "observed",
                         "mechanisms": "observed", "variant_coverage": "observed",
                         "recreation_knowledge": "validated", "spatial_placement": "observed",
                     }},
    }


def build_report(definition: dict, seed: dict, geometry: dict) -> tuple[dict, bytes]:
    all_devices = definition["inputs"] + definition["outputs"] + definition["displays"]
    placements = [placement for item in all_devices for placement in item.get("spatial", {}).get("placements", [])]
    anchors = {slug(name): name for name in geometry}
    resolved = {placement["id"]: anchors[next(key for key in anchors if placement["id"].endswith("." + key))]
                for placement in placements}
    inserts = {
        item["id"]: geometry[f"Light.L{address}"]
        for item in definition["outputs"]
        if item["binding"]["group"] == "pinmame.output.lamp"
        and (address := item["binding"]["device"]) in data.LAMP_ROWS.keys() - data.BACKBOX_LAMPS
    }
    report = {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": ID,
        "status": definition["coverage"]["status"], "evidence": seed["vpx"],
        "bounds": seed["geometry"]["bounds"],
        "normalization": "x = (x_vpu - 0) / 1122; y = (y_vpu - 0) / 2115; six decimal places",
        "placements": resolved,
        "candidate_insert_apertures": inserts,
        "missing_device_positions": [item["id"] for item in all_devices if "spatial" not in item],
        "projection_classes": {
            "slings": "Centroid of the scripted slingshot wall is the switch and coil effect projection.",
            "drop_banks": "Individual effects use target centers. A bank reset uses its middle target.",
            "flippers": "The pivot projects both windings and the hidden EOS contact.",
            "kickers": "Stage kickers project onto their respective switch triggers. Outhole serve projects onto the VPX release point.",
        },
        "unverified_lamp_public_addresses": sorted(data.UNVERIFIED_LAMP_WIRING),
    }
    note = [
        "# Flight 2000 spatial blockers", "",
        "Coverage remains **partial**.", "",
        f"The retained bord 2.0 table gives {len(resolved)} observed placements in a 1122 × 2115 VPX frame.",
        f"The extracted tree has {seed['vpx']['file_count']} files and {seed['vpx']['file_bytes']} bytes.",
        f"VPX SHA-256: `{seed['vpx']['sha256']}`.",
        f"Extraction manifest SHA-256: `{seed['vpx']['manifest_sha256']}`.",
        "The origin is the rear left. The normalization and object backing each placement are in the JSON report.",
        "", "## Projections", "",
    ]
    note += [f"- {description}" for description in report["projection_classes"].values()]
    note += [
        "", "## Missing physical evidence", "",
        "- The under-apron switch diagram gives relative contact order only. The VPX trough uses three virtual switch slots and one serve kicker.",
        "- The VPX lock script collapses the physical walker to three kickers. The factory view and photos confirm the carrier lane but do not locate the launcher contact and coil linkage precisely.",
        f"- {len(inserts)} script-bound insert aperture centers are retained as candidates in the JSON report. Physical socket centers remain open. GI objects and the schematic leave the socket count and positions incomplete.",
        "- The artwork places both stages and both T inserts. Their wiring and the remaining ambiguous lamp assignments are listed in the JSON report.",
        "- The two serve photographs establish mounting alternatives. The shared placement is the shooter feed effect.",
        "", "### Devices without a coordinate candidate", "",
    ]
    note += [f"- `{identifier}`" for identifier in report["missing_device_positions"] if identifier not in inserts]
    return report, ("\n".join(note) + "\n").encode("utf-8")


def verify_external(seed: dict, require: bool = False) -> None:
    roots = {
        "vpx": os.environ.get("PINMAME_VPX_SOURCES_ROOT"),
        "manuals": os.environ.get("PINMAME_MANUALS_ROOT"),
        "review": os.environ.get("PINMAME_REVIEW_ARTIFACTS_ROOT"),
    }
    if require and not all(roots.values()):
        raise ValueError("Set the VPX, manuals and review-artifacts evidence roots")
    for kind, root in roots.items():
        if root:
            for relative, digest in seed["retained"][kind].items():
                if file_sha256(Path(root) / relative) != digest:
                    raise ValueError(f"Retained {kind} artifact changed: {relative}")
    if roots["review"]:
        runtime = load_json(RUNTIME_EVIDENCE)
        if check_manifest(Path(roots["review"]) / ID / "service-occupied", "flight2k") != runtime["source"]["sha256"]:
            raise ValueError("Retained Flight 2000 service manifest changed")
    if roots["vpx"]:
        vpx_dir = Path(roots["vpx"]) / VPX
        extracted = vpx_dir / "extracted"
        manifest = build_manifest(extracted, "flight2k")
        files = manifest["files"]
        if (check_manifest(extracted, "flight2k") != seed["vpx"]["manifest_sha256"]
                or len(files) != seed["vpx"]["file_count"]
                or sum(entry["size"] for entry in files) != seed["vpx"]["file_bytes"]):
            raise ValueError("Retained extraction manifest changed")
        actual = extract_spatial_candidates(extracted, vpx_dir / VPX_NAME, VPX_VERSION)
        selected = {f"{item['type']}.{item['name']}": item for item in actual["objects"]}
        for name, stored in seed["geometry"]["objects"].items():
            if selected[name] != stored:
                raise ValueError(f"Retained VPX coordinate changed: {name}")
        if actual["bounds"] != seed["geometry"]["bounds"]:
            raise ValueError("Retained VPX bounds changed")


def products() -> dict[Path, bytes]:
    seed = load_json(SEEDS / f"{SLUG}-evidence.json")
    for source in seed["sources"]:
        for excerpt in source.get("excerpts", []):
            if file_sha256(ROOT / excerpt["path"]) != excerpt["sha256"]:
                raise ValueError(f"Reviewed excerpt changed: {excerpt['path']}")
    geometry = seed["geometry"]["objects"]
    definition = build_flight(seed, geometry)
    report, report_md = build_report(definition, seed, geometry)
    return {
        DEFINITION: canonical_bytes(definition),
        KNOWLEDGE: (SEEDS / f"{SLUG}-knowledge.md").read_bytes(),
        REPORT.with_suffix(".json"): canonical_bytes(report),
        REPORT.with_suffix(".md"): report_md,
        CONVERSION: canonical_bytes(load_json(SEEDS / "gamatron-1985.json")),
        CONVERSION_NOTE: (SEEDS / "gamatron-1985-knowledge.md").read_bytes(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-evidence", action="store_true")
    args = parser.parse_args()
    for path in (DEFINITION, CONVERSION):
        if (ROOT / Path(path.as_posix().replace("/partial/", "/author-ready/"))).exists():
            raise SystemExit(f"Refusing to overwrite an author-ready definition: {path}")
    if args.verify_evidence:
        verify_external(load_json(SEEDS / f"{SLUG}-evidence.json"), require=True)
    for relative, payload in products().items():
        path = ROOT / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                raise SystemExit(f"Stale Flight 2000 product: {relative}")
        else:
            write_bytes(path, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
