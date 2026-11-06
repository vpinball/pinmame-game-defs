#!/usr/bin/env python3
"""Reproduce Skateball's spatial blocker reports from the definition and seed.

The checked-in inputs are sufficient; verification of the retained VPX extraction
is a separate gate. Refuse to describe a definition that has drifted from the
seed, so report hashes and unplaced-device lists cannot silently go stale.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pinmame_game_defs.jsonio import canonical_bytes, file_sha256  # noqa: E402

DEFINITION = ROOT / "machines/partial/bally/skateball-1980.json"
SEED = ROOT / "tools/seeds/bally/skateball-1980-spatial.json"
REPORT = ROOT / "reports/spatial/bally/skateball-1980.json"
MARKDOWN = ROOT / "reports/spatial/bally/skateball-1980.md"
MACHINE_ID = "bally.skateball.1980"


def build_report(definition: dict, seed: dict, definition_hash: str, seed_hash: str) -> tuple[dict, str]:
    if definition["machine"]["id"] != MACHINE_ID or seed["machine_id"] != MACHINE_ID:
        raise ValueError("Unexpected machine identity")
    if definition["coverage"]["status"] != "partial" or "spatial_placement" not in definition["coverage"]["missing"]:
        raise ValueError("The report is for a partial machine with spatial placement outstanding")
    devices = {}
    for group in ("inputs", "outputs"):
        for device in definition[group]:
            binding = device["binding"]
            family = {"pinmame.input.switch": "switch", "pinmame.output.solenoid": "solenoid",
                      "pinmame.output.lamp": "lamp"}.get(binding["group"])
            if family:
                devices[f"{family}:{binding['device']}"] = device
    if definition["machine"].get("playfield") != seed["playfield"]:
        raise ValueError("Definition playfield extent differs from seed")
    for key, spatial in seed["device_spatial"].items():
        if key not in devices or devices[key].get("spatial") != spatial:
            raise ValueError(f"Definition spatial data differs from seed: {key}")
    for key, patch in seed.get("device_physical", {}).items():
        if key not in devices:
            raise ValueError(f"Definition is missing physical device: {key}")
        actual = devices[key].get("physical", {})
        for field, value in patch.items():
            if field == "notes":
                if value not in actual.get("notes", ""):
                    raise ValueError(f"Definition is missing spatial note: {key}")
            elif actual.get(field) != value:
                raise ValueError(f"Definition physical data differs from seed: {key}.{field}")
    sources = {source["id"]: source for source in definition["sources"]}
    for source in seed.get("sources", []):
        if sources.get(source["id"]) != source:
            raise ValueError(f"Definition source differs from seed: {source['id']}")

    status_counts: Counter[str] = Counter()
    na_counts: Counter[str] = Counter()
    unplaced = []
    unvalidated = []
    for collection in ("inputs", "outputs", "displays"):
        for device in definition[collection]:
            spatial = device.get("spatial")
            if spatial is None:
                if device.get("availability") == "used":
                    unplaced.append({"id": device["id"], "label": device["label"], "binding": device.get("binding")})
                continue
            if spatial["status"] == "not_applicable":
                na_counts[spatial["reason"]] += 1
                continue
            for placement in spatial["placements"]:
                status = placement["provenance"]["status"]
                status_counts[status] += 1
                if status != "validated":
                    unvalidated.append(placement["id"])
    unplaced.sort(key=lambda item: item["id"])
    unvalidated.sort()
    classes: dict[str, list[str]] = {}
    for key, derivation in seed["derivations"].items():
        classes.setdefault(derivation["method"], []).append(key)
    report = {
        "format": "pinmame-spatial-blockers", "version": 1, "machine_id": MACHINE_ID,
        "coordinate_convention": {"space": "playfield", "x": "0=left, 1=right in player view",
                                  "y": "0=rear/backglass end, 1=front/apron end"},
        "coverage": definition["coverage"], "definition_sha256": definition_hash,
        "transformation": seed["transformation"],
        "source_hashes": {"vpx_table_sha256": seed["source_vpx_sha256"],
                          "vpx_script_sha256": seed["source_script_sha256"],
                          "extraction_manifest_sha256": seed["extraction_manifest_sha256"],
                          "spatial_seed_sha256": seed_hash,
                          "manual_sha256": "0758b23c3d33b28c06be006ba768151075b0f31ae9cddad6739e6c5ab7513a1a",
                          "schematic_sha256": "1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c",
                          "photo_022_sha256": "4e245b595de112cea952a5b344d047fec12c5f7ad5f0b5d762cf16fd67f9fe8e",
                          "photo_026_sha256": sources["human-review.skateball.photo-026"]["sha256"],
                          "photo_036_sha256": "57097770cf916d554c946920385690f01a7d64fbd5096f3e9b32c256b97a6c2e"},
        "extraction": {"file_count": seed["extraction_file_count"], "total_bytes": seed["extraction_total_bytes"],
                       "vpxtool": "vpxtool git:v0.33.3", "bounds": seed["bounds"],
                       "external_path": "vpx-sources/bally/skateball-1980/extracted-vpxtool"},
        "placement_status_counts": dict(sorted(status_counts.items())),
        "not_applicable_counts": dict(sorted(na_counts.items())),
        "projection_classes": {key: sorted(values) for key, values in sorted(classes.items())},
        "lamp_bulb_audit": seed["lamp_bulb_audit"],
        "supplemental_vpw_audit": seed["supplemental_vpw_audit"],
        "lane_orientation": seed["lane_orientation"],
        "unresolved_output_states": seed["unresolved_output_states"],
        "unplaced_physical_devices": unplaced, "unvalidated_placements": unvalidated,
        "promotion_decision": "Partial: undocumented DIP functions, unexplained published startup states at unfitted continuous outputs 17/20, and incomplete spatial placements remain. The outhole switch/coil and remaining controlled playfield sockets are unplaced; all positions remain observed. Replacement-board lane orientation does not authenticate original 1980 artwork.",
    }
    lines = [
        "# Skateball (Bally 1980) spatial blockers", "",
        f"Coverage: **{definition['coverage']['status']}**; missing " + ", ".join(f"`{x}`" for x in definition["coverage"]["missing"]) + ".", "",
        f"The retained VPX table SHA-256 is `{seed['source_vpx_sha256']}`; script `{seed['source_script_sha256']}`; extraction manifest `{seed['extraction_manifest_sha256']}` ({seed['extraction_file_count']} files, {seed['extraction_total_bytes']} bytes). The machine definition is `{definition_hash}` and spatial seed `{seed_hash}`.", "",
        seed["transformation"], "",
        f"The seed holds {len(seed['objects'])} raw object anchors, their individual file hashes and drag points where applicable, and every device derivation. There are {sum(status_counts.values())} placements: " + ", ".join(f"{v} {k}" for k, v in sorted(status_counts.items())) + f". There are {len(unplaced)} used devices without placements.", "",
        "## Evidence and decisions", "",
        "- The manual (SHA-256 `0758b23c3d33b28c06be006ba768151075b0f31ae9cddad6739e6c5ab7513a1a`) PDF 21 lists the switch and coil self-test labels. PDF 13's top-parts drawing and an owner photograph show an upper-left drop bank with the rollover lanes to its right. Figure V on PDF 22 differs in upper-bank and lane geometry; it was not fitted or used to validate placements. All coordinates remain observed.",
        "- The switch positions use script-bound triggers, targets, bumpers, spinner and kicker centers, except for the observed outer-lane override. The manual's self-test table names switch 13 lane #3 and 15 lane #1 without assigning sides; Figure V separately draws rollover circles 15, 14, 13 left-to-right and corroborates relative number order. Its differing upper-playfield geometry is not fitted or used to validate absolute placements/as-built artwork. Photo-026 clearly shows #1 left and #3 right on a physical replacement reproduction, agreeing with the redrawn table artwork; it does not independently authenticate original 1980 artwork. The old-board photo-022 has unreadable lane numerals. Crosswise anchors 13 at Trigger.sw15/right and 15 at Trigger.sw13/left remain observed and cite photo-026 for orientation, the manual for identity/relative order, and table objects for coordinates.",
        "- The table's lane switch/lamp pairing is internally consistent: switch 13 with lamp 24 (Light.l24, x 481.5) at left, switch 15 with lamp 56 (Light.l56, x 685.6491) at right. Both halves differ from the observed replacement-board/artwork orientation; this is not described as a factory-proven lane defect. Lamps 24/56 remain unplaced and no render-light center is adopted as a socket position.",
        "- Switch 17 uses seven script-bound wall drag-point centroids as projections onto three drop-target and four rebound scoring assemblies; the slingshot switch locations likewise use wall centroids. Reset coils use the means of their bank targets; saucer, bumper, slingshot and flipper coils project onto their modeled mechanisms or pivots. None is a measured coil center.",
        "- The schematic (SHA-256 `1a16295a490fb6b3b00c9a88e829dbe9ee0aa3577c3b050dd0159406e241c91c`) PDF 10 names the left, bottom and right thumper lamps. Lamps 25, 41 and 57 use the corresponding bumper centers as projections of hidden bulbs, not observed socket centers. The retained table script swaps left and right bindings for 25 and 57; physical labels determine placement.",
        "- The table's Drain is a destroy/helper below the physical outhole, and BallRelease is a serve helper. Neither establishes the physical outhole center; switch 8 and coil 7 remain unplaced.",
        f"- Of {seed['lamp_bulb_audit']['light_objects']} extracted Light objects, {seed['lamp_bulb_audit']['show_bulb_mesh_true']} show a bulb mesh; all are gi-prefixed. No controlled lamp light shows a bulb mesh. The playfield underside photograph contains sockets but does not supply a registered per-socket map with circuit identities. No other controlled lamp positions are inferred from insert or render-helper centers.",
        f"- The related VPW 1.0 recreation (table SHA-256 `{seed['supplemental_vpw_audit']['table_sha256']}`, script `{seed['supplemental_vpw_audit']['script_sha256']}`, manifest `{seed['supplemental_vpw_audit']['extraction_manifest_sha256']}`; {seed['supplemental_vpw_audit']['extraction_file_count']} files and {seed['supplemental_vpw_audit']['extraction_total_bytes']} bytes) has {seed['supplemental_vpw_audit']['light_objects']} Light objects, none with a visible bulb mesh. It is based on a mod of the earlier table, so it is not independent geometry validation. Its combined `BM_Parts` mesh was exported to world-space OBJ `{seed['supplemental_vpw_audit']['world_obj_sha256']}` and welded at 0.1 VPU into {seed['supplemental_vpw_audit']['connected_pieces']} pieces (inventory `{seed['supplemental_vpw_audit']['component_inventory_sha256']}`). The three largest pieces align with top-lane inserts and have flat profiles; the investigation does not establish a reliable physical socket identity and wiring map. The later lamp 25 and 57 lighting arrays agree with the factory bumper sides.",
        "- The table's always-on GI lights are not PinMAME-controlled GI outputs. The 5.9 VAC factory GI circuit is physical illumination; the table lights do not establish its complete socket count or wiring membership.", "",
        "- Continuous outputs 17/20 are physically unfitted according to the game's own wiring, but their published startup burst is unexplained. All 17-20 rising/falling edges are retained in continuous-startup-observations.md. Inversion and timing alone do not prove the PIA/ROM cause; availability remains unknown and output_semantics stays missing. Their spatial N/A records refer only to physical non-fitment.", "",
        "## Unplaced used devices", "",
        *[f"- `{item['id']}` — {item['label']}" for item in unplaced], "",
        "## Projection and evidence inventory", "",
        *[f"- `{kind}`: {', '.join(f'`{key}`' for key in sorted(keys))}." for kind, keys in sorted(classes.items())], "",
        "Retained evidence: `manuals/by-machine/bally.skateball.1980/` for the originals, rendered pages and OCR; `vpx-sources/bally/skateball-1980/` for the original table, extraction and candidates; `review-artifacts/skateball-1980/photos/` for old-board photos 022/036, replacement-board photo 026 and their download manifest. Photo excerpts are `evidence/excerpts/bally.skateball.1980/playfield-photo-observations.md` and `replacement-playfield-lanes.md`; exact unexplained callback edges are in `continuous-startup-observations.md`.", "",
    ]
    return report, "\n".join(lines)


def artifacts() -> dict[Path, bytes]:
    definition_bytes = DEFINITION.read_bytes()
    definition = json.loads(definition_bytes)
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    if definition_bytes != canonical_bytes(definition):
        raise ValueError("Definition is not canonical")
    report, markdown = build_report(definition, seed, file_sha256(DEFINITION), file_sha256(SEED))
    return {REPORT: canonical_bytes(report), MARKDOWN: markdown.encode("utf-8")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    try:
        generated = artifacts()
        if args.check:
            drift = [str(path.relative_to(ROOT)) for path, content in generated.items()
                     if not path.exists() or path.read_bytes() != content]
            if drift:
                raise ValueError("Spatial report drift: " + ", ".join(drift))
        else:
            for path, content in generated.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
        print("Skateball spatial reports match" if args.check else "Regenerated Skateball spatial reports")
        return 0
    except (KeyError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
